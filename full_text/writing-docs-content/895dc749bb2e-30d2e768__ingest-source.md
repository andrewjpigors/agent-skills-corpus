---
name: ingest-source
description: Fully autonomous end-to-end ingestion of a SINGLE source (book, paper, article, transcript) into the knowledge base - prepare to markdown, extract insights against the live index, refresh the index, auto-link to existing knowledge, and changelog. One source per invocation.
automation: autonomous
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Task, Skill]
user-invocable: true
argument-hint: <source path or URL> [session name]
effort: high
metadata:
  version: "1.0"
  created: 2026-06-03
  author: Cornelius
---

# Ingest Source

Fully autonomous pipeline that takes **one** source from raw file to integrated, connected knowledge. Each invocation handles a single source; drive a whole corpus by invoking once per source (e.g. via `/loop` or a shell loop over a file list), then run the corpus-level finalize steps **once** at the end.

`ultrathink`

## Purpose

The unit of work for building a knowledge base from a book corpus. One source in → deduplicated, epistemically-classified notes out, embedded in the graph and linked to existing knowledge, with every auto-action logged for post-hoc review.

The design principle (established in the architecture discussion): **insights are extracted *against the current KB, not in a vacuum*** — retrieval-augmented extraction. The index is the KB's queryable state, so it must be refreshed *before* connection discovery, and refreshed again on the next source so each source builds on the last.

## Configuration (safety rails that replace human gates)

| Knob | Default | Purpose |
|------|---------|---------|
| `AUTO_LINK_THRESHOLD` | `0.75` | Only auto-write links at or above this cosine similarity. Below → logged as review candidates, not written. |
| `LINKS_PER_NOTE` | `5` | Max auto-links written per new note (top-k). Caps combinatorial blowup. |
| `MUTATE_EXISTING_NOTES` | `false` | If false, only the NEW notes get edited (links written FROM new → existing). Existing/hub notes are never mutated by auto-linking. |
| `REJECT_ON_TIER` | `rejected` | If the extractor tiers the source `rejected` (content-farm / regurgitated), abort and notify. |

These are the autonomous substitute for the two approval gates a `gated` version would have. See **Architecture Note** for why.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Source file | arg path / URL | ✓ | | Book, paper, article, transcript, or YouTube URL |
| Working markdown | `resources/ingest-workspace/<slug>/` | ✓ | ✓ | Extracted/prepared markdown + checkpoint |
| Book scope (books) | `Brain/Books/<book-slug>/` | ✓ | ✓ | Per-book scope: notes + `_book.md` hub land here |
| Document Insights (non-books) | `Brain/Document Insights/<session>/` | ✓ | ✓ | Papers / articles / web extracted notes land here |
| FAISS index + BDG | `resources/local-brain-search/`, `resources/brain-graph/` | ✓ | ✓ | Refreshed mid-pipeline |
| Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Per-source ingestion report |
| Ingest ledger | `resources/ingest-workspace/INGEST-LEDGER.md` | ✓ | ✓ | Corpus progress: which sources done |
| Checkpoint | `resources/ingest-workspace/<slug>/.checkpoint` | ✓ | ✓ | Resume marker for the 45-min rule |

## Prerequisites

- Local Brain Search installed (`resources/local-brain-search/run_index.sh`, `run_connections.sh`)
- Brain Dependency Graph engine (`resources/brain-graph/run_brain_graph.sh`)
- Extractor agents available: `document-insight-extractor`
- Source-prep skills available: `epub-chapter-extractor`, `multi-format-book-extractor`, `get-youtube-transcript`

## Process

### Step 0: Read inputs and checkpoint

Parse `$ARGUMENTS`: first token = source path/URL, optional remainder = session name. Derive a `<slug>` and, if no session name given, derive one from the source title (e.g. `"<Book Title>"`).

```bash
date '+%Y-%m-%d'
test -f resources/ingest-workspace/<slug>/.checkpoint && cat resources/ingest-workspace/<slug>/.checkpoint || echo "phase=start"
```

If a checkpoint exists, **resume from the next phase** rather than restarting (re-running earlier phases is safe — they are idempotent — but wasteful for large books).

**Scope routing (book vs. non-book).** Decide the destination scope now:

| Source is… | Destination dir | Scope token (for read-scope mounts) |
|------------|-----------------|-------------------------------------|
| a **book** — `.epub` / `.pdf` / `.mobi` / `.azw3`, or `--book` is passed | `Brain/Books/<book-slug>/` | `Books/<book-slug>` (its own pluggable scope) |
| anything else — paper / article / web / transcript / YouTube | `Brain/Document Insights/<session>/` | `document-insights` (the shared bucket) |

A book gets **its own scope** (`Books/<slug>`): non-core (never pollutes the core fingerprint or trains q-values), cognitive (its gems can graduate to core via the human `/graduate-insights` act), and pluggable (mount with `BRAIN_READ_SCOPE=core,Books/<slug>` or the whole shelf with `core,Books`). Set `TARGET_DIR` and `BOOK_SLUG` accordingly and use them in Steps 2/4/6 below.

### Step 1: Prepare source → markdown

Detect format by extension/URL and convert to markdown:

| Input | Action |
|-------|--------|
| `.epub` | `Skill: epub-chapter-extractor` → per-chapter `.md` |
| `.pdf` / `.mobi` / `.azw3` | `Skill: multi-format-book-extractor` |
| YouTube URL | `Skill: get-youtube-transcript` |
| `.md` / `.txt` | use directly (no conversion) |

Write prepared markdown into `resources/ingest-workspace/<slug>/`.
Checkpoint: `phase=prepared`.

### Step 2: Extract insights (against the live index)

Spawn the extractor directly (autonomous — skip the interactive insight-interview suggestion).

**For a book** (Step-0 routing → `Brain/Books/<book-slug>/`), invoke in **Book Mode**:

```
Task(
  subagent_type="document-insight-extractor",
  prompt="BOOK MODE. Extract insights from <prepared markdown path(s)> into the book scope
          Brain/Books/<book-slug>/ (NOT Document Insights). Follow your Book Mode doctrine:
          mine like a scientist THROUGH THE KB LENS (contextualize against the CURRENT index
          as a GATE); capture ONLY genuine frameworks / mental models / methods / evidenced
          contrarian claims; REJECT narrative, anecdote, biography, he-said-she-said, and
          restatements of the obvious or of concepts the KB already holds; MECE + atomic
          (one idea per note, no overlap within the book scope); expected shape ~10 core
          concepts + up to ~20 supporting nodes as REFERENCE POINTS not caps; prefer
          statistically-meaningful research (N, effect size, replication, year) over one-off
          examples and record dates. Apply Gate 1 source-tiering and provenance: encountered;
          SEARCH FOR DUPLICATES (mount BRAIN_READ_SCOPE=core,Books,document-insights) and
          merge/link rather than re-create; create the _book.md literature hub; update the
          changelog. Return: list of new note file paths, total count, epistemic split,
          assigned source-tier, and the book scope path."
)
```

**For non-books** (paper / article / web → `Brain/Document Insights/<session>/`):

```
Task(
  subagent_type="document-insight-extractor",
  prompt="Extract insights from <prepared markdown path(s)> into session '<session name>'.
          Follow your mandatory workflow: contextualize against the CURRENT index,
          apply Gate 1 source-tiering and Gate 2 provenance (provenance: encountered),
          epistemically classify each note, SEARCH FOR DUPLICATES and merge/link rather
          than re-create, write notes to Brain/Document Insights/<session>/, update the
          session changelog. Return: list of new note file paths, total count,
          epistemic split, and the assigned source-tier."
)
```

**Safety rail (replaces Gate 1):** if the returned source-tier is `REJECT_ON_TIER`, abort, log the rejection to the changelog, and notify. Low-confidence/speculative notes are kept but flagged in the changelog, never silently dropped.

Capture the new note paths — **only these notes are processed downstream** (this keeps connection discovery linear, not all-vs-all).
Checkpoint: `phase=extracted` (persist the note list).

### Step 3: Refresh the index

The FAISS index does not auto-update, and connection discovery looks notes up **by title in the index** — so new notes are invisible until reindexed. Refresh now, before discovery:

```bash
resources/local-brain-search/run_index.sh
resources/brain-graph/run_brain_graph.sh bootstrap --force
resources/local-brain-search/run_connections.sh --stats --json   # verify count grew
```

(This is exactly `/refresh-index`; one full rebuild per source also sweeps in the prior source's auto-links.)
Checkpoint: `phase=indexed`.

### Step 4: Discover connections (bounded, new → existing)

For **each new note only**, query its neighbors. Use a wide read-scope so a new
note resolves and links against existing non-core neighbors (core-only would miss
them once scope enforcement is on). **Mount the destination scope:** for a book use
`core,Books` (so it links to core and across the whole shelf); for a non-book use
`core,document-insights`:

```bash
# book:
BRAIN_READ_SCOPE=core,Books resources/local-brain-search/run_connections.sh "<New Note Title>" --json
# non-book:
BRAIN_READ_SCOPE=core,document-insights resources/local-brain-search/run_connections.sh "<New Note Title>" --json
resources/brain-graph/run_brain_graph.sh inspect "<New Note Title>" --json   # edge type + lifecycle
```

Collect top-`LINKS_PER_NOTE` connections per note with similarity scores and BDG edge type. **Do not** run all-pairs or hub/bridge sweeps here — that is the combinatorial explosion this step is designed to avoid. New→existing is linear in the source's note count.
Checkpoint: `phase=connections-discovered` (persist the connection report).

### Step 5: Auto-write links (the gated step, made safe)

For each new note, write wiki-links to its qualifying connections:

- **Threshold:** only connections with similarity ≥ `AUTO_LINK_THRESHOLD`.
- **Cap:** at most `LINKS_PER_NOTE` per note.
- **Idempotent:** skip if the `[[link]]` already exists in the note.
- **Labeled + reversible:** append under a clearly marked section in the NEW note only:
  ```markdown
  ## Related (auto-linked by /ingest-source)
  <!-- AI-discovered via semantic similarity; review critically. similarity ≠ conceptual validity -->
  - [[Target Note]] — 0.82, derives-from
  ```
- **Never mutate existing notes** when `MUTATE_EXISTING_NOTES=false` — links go FROM the fresh notes outward, so hub notes are never polluted and every auto-edit is confined to notes created this run (trivially reversible by deleting the session folder).
- **Below-threshold** connections → recorded in the changelog as "candidates for human review," not written.
- **Tension preservation:** if a high-similarity connection is to a note with an **opposing** claim (BDG edge type `tension`, or the extractor flagged a contradiction), DO NOT collapse or dedupe it away. Record it in the changelog under "Tension candidates" for the manual `/detect-tensions` pass. Never auto-resolve a contradiction.

Use `Edit` on the new note files (their paths are known from Step 2).
Checkpoint: `phase=linked`.

### Step 6: Changelog

Write `Brain/05-Meta/Changelogs/CHANGELOG - Source Ingestion <session> YYYY-MM-DD.md`:

```markdown
## Source Ingestion: <session> — YYYY-MM-DD

**Source:** <path/URL>  |  **Tier:** <primary|credible-interpreter>  |  **Format:** <epub/pdf/...>
**Notes created:** N  (confirmed: X · theoretical: Y · speculative: Z)

### Auto-linked (≥ AUTO_LINK_THRESHOLD)
- [[New Note]] → [[Existing]] (0.82, derives-from)

### Review candidates (below threshold)
- [[New Note]] ~ [[Existing]] (0.71)

### Tension candidates (DO NOT auto-resolve — for /detect-tensions)
- [[New Note]] vs [[Existing]] — opposing claims at 0.78

### Isolated notes (0 connections ≥ threshold) — priority for human attention
- [[New Note]]
```

Checkpoint: `phase=changelogged`.

### Final Step: Write ledger + state, notify

Append to `resources/ingest-workspace/INGEST-LEDGER.md`:

```markdown
| YYYY-MM-DD | <session> | <source> | N notes | done |
```

Print a summary and the **after-the-corpus reminder** (these are manual — judgment work, per the architecture):

> Source ingested. After the LAST source in the corpus, run once:
> `/detect-tensions` → `/coherence-sweep` → `/graduate-insights`
> (cross-source contradictions, structural health, and canonicalization into permanent notes).

Notify on completion. On any unrecoverable failure, notify with the failed phase and the checkpoint path so the run can be resumed. Then clear the checkpoint (`phase=done`).

## Outputs

- Deduplicated, epistemically-classified notes in the destination scope — `Brain/Books/<book-slug>/` (books, plus a `_book.md` literature hub) or `Brain/Document Insights/<session>/` (non-books)
- Refreshed FAISS index + BDG enrichments
- AI-labeled wiki-links from the new notes into the existing graph
- Per-source ingestion changelog (auto-links, review candidates, tension candidates, isolated notes)
- Updated corpus ledger entry

## Error Recovery

| Failure | Recovery |
|---------|----------|
| Source-prep fails (unsupported format) | Log, notify, abort. Markdown/text passthrough always works as fallback. |
| Source tiered `rejected` | Log rejection to changelog, notify, abort — do not extract. |
| Extractor returns 0 notes | Log "no extractable insights," notify, mark ledger `empty`, exit. |
| `run_index.sh` fails | Abort before linking (linking on a stale index would mislink). Resume from `phase=extracted`. |
| BDG bootstrap fails | Non-critical — LBS links still work. Log and continue without edge-type labels. |
| Connection query fails for a note | Log, skip that note, continue with the rest. |
| Interrupted mid-run (45-min rule) | Re-invoke with same source; the `.checkpoint` resumes from the next phase. |

## Autonomous Validation Checklist

- [x] **No approval gates** — none present; the two judgment points are replaced by threshold + cap + label + audit rails.
- [x] **No human decision points** — runs unattended start to finish.
- [x] **Complete error handling** — every phase has a recovery path.
- [x] **Notifications on failure** — failed phase + checkpoint path reported.
- [x] **Under 45 minutes** — one source per invocation; extractor chunks large files internally; refresh cost equals the daily scheduled refresh. Checkpointing resumes if exceeded.
- [x] **Idempotent / safe to retry** — extractor dedups; refresh is idempotent; link-writing checks for existing links; resume via checkpoint.
- [x] **Single-task scope** — exactly one source per invocation; the scheduler / loop drives the corpus.

## Architecture Note (deliberate deviation)

`ARCHITECTURE.md` and the autonomy principle state: *"Automate measurement and maintenance. Never automate creation or judgment,"* and list connection-writing as manual-only. This skill **deliberately crosses that line for connection-writing** because the use case is bulk ingestion of a book corpus, where per-source human gating does not scale.

The deviation is bounded, not unbounded. The architecture's real concern is **un-auditable, irreversible auto-judgment**. This skill substitutes:

- a **similarity threshold + per-note cap** for the "which links are valid" judgment,
- **AI-labeled, new-notes-only edits** so every auto-action is transparent and reversible (delete the session folder),
- a **changelog audit trail** enabling *review-after* instead of *approve-before*,
- **tension-preservation** so contradictions are surfaced, never auto-collapsed.

This mirrors how `/auto-discovery` and the incubation loop already auto-write AI-labeled content to the graph. What remains strictly manual — and is intentionally NOT in this skill — is the corpus-level judgment work: `/detect-tensions`, the final `/coherence-sweep`, and canonicalization via `/graduate-insights`. If you want the conservative posture instead, set `MUTATE_EXISTING_NOTES=false` (already default), raise `AUTO_LINK_THRESHOLD`, or fork a `gated` variant that stops at Step 4 and emits the connection report for human approval.

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies (e.g. extractor timeouts, mislinks, threshold too loose/tight)?
- [ ] **Identify improvements**: Could error handling, step ordering, the safety-rail defaults, or instructions be clearer?
- [ ] **Scope check**: Only tactical/execution changes — NOT changes to core purpose (the per-source pipeline shape) or the architecture-deviation rationale.
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control** (if in a git repository):
  - [ ] Stage: `git add .claude/skills/ingest-source/SKILL.md`
  - [ ] Commit: `git commit -m "refactor(ingest-source): <brief improvement description>"`
