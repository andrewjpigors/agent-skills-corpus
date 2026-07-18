---
name: domain-watch
description: Autonomous perception layer - scans KB for new notes matching domain watch configs, checks gap resonance with the Thinking Registry, probes external signals via web search, and auto-activates HIGH/MEDIUM signals into the Thinking Registry for the incubation loop.
automation: autonomous
schedule: "0 7 * * *"
allowed-tools: Read, Write, Grep, Glob, Bash, WebSearch
user-invocable: true
argument-hint: "[domain-slug] (optional - scans all active domains if omitted)"
metadata:
  version: "1.1"
  updated: 2026-07-03
  changelog:
    - "1.1: Thinking Registry write discipline — topic activation adds a table ROW only; never write scan narratives or frontmatter fields (e.g. last_domain_watch) into THINKING-REGISTRY.md; scan results belong in the Watch Log and domain configs"
    - "1.0: Initial version"
---

# Domain Watch

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `domain-watch vX.Y — recent: <summary>`. Then proceed.

Autonomous perception layer. Each scheduled run scans configured domains for new KB notes, checks gap resonance with the Thinking Registry, probes external signals via web search, and auto-activates HIGH/MEDIUM proposals directly into the Thinking Registry. LOW/NONE signals are logged only.

**Design principle:** Perceive, score, activate. Human reviews the Watch Log post-run.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Watching Registry | `Brain/05-Meta/Watching/WATCHING-REGISTRY.md` | ✓ | ✓ | Active domain list + last scan dates |
| Domain Configs | `Brain/05-Meta/Watching/[domain-slug].md` | ✓ | ✓ | Per-domain PIRs, queries, baseline counts |
| Watch Log | `Brain/05-Meta/Watching/WATCH-LOG.md` | ✓ | ✓ | Append-only proposals and scan history |
| Thinking Registry | `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` | ✓ | | Gap resonance check (read-only) |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Semantic search for KB notes |
| Session Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Run log |

## Prerequisites

- Watching Registry exists at `Brain/05-Meta/Watching/WATCHING-REGISTRY.md`
- At least one active domain seeded (see Seeding section below)
- Local Brain Search index up-to-date

---

## Process

### Step 1: Get Date and Load Registry

```bash
date '+%Y-%m-%d'
```

Read `Brain/05-Meta/Watching/WATCHING-REGISTRY.md`. Parse all domains with `status: active`.

If registry does not exist, create it:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Watching Registry

Domains under active surveillance.

| Domain Slug | Label | Mode | Last Scan | Status |
|-------------|-------|------|-----------|--------|
```

If no active domains found, log to changelog and exit cleanly.

If a specific `[domain-slug]` was passed as argument, process only that domain.

### Step 2: For Each Active Domain - Load Config

Read `Brain/05-Meta/Watching/[domain-slug].md`.

Parse:
- `watch_queries` - semantic search terms for LBS
- `priority_intelligence_requirements` - specific questions to check incoming notes against
- `last_scan` - ISO date of previous run (null on first run)
- `notes_at_scan` - note count baseline at last scan (0 on first run)
- `spawn_threshold` - delta required before a proposal is flagged (default 3)
- `mode` - `surveillance` (watch for accumulation) or `hypothesis` (track specific claims)

### Step 3: Scan KB for New Notes

Run LBS search for each watch_query:

```bash
cd $PROJECT_ROOT
# --no-track: autonomous perception layer; scans must NOT train q-values (scope-primitive learning hygiene)
# BRAIN_READ_SCOPE=<wide>: perception must SEE non-core material (new captures in 00-Inbox, Document
#   Insights, per-book scopes in Books, thinking files in 05-Meta, article drafts in 04-Output). Without it the scan fails closed
#   to core once scope enforcement is on and silently stops perceiving everything outside the fingerprint.
BRAIN_READ_SCOPE=core,Books,document-insights,meta,inbox,output python3 resources/local-brain-search/search.py "[watch_query]" --limit 20 --mode spreading --no-track 2>/dev/null
```

Then find notes modified since the last scan date:

```bash
# If last_scan is set, find files newer than the domain config's last_scan date
find Brain/02-Permanent "Brain/AI Extracted Notes" "Brain/Document Insights" \
  -name "*.md" -newer Brain/05-Meta/Watching/[domain-slug].md \
  -type f 2>/dev/null | head -50
```

On first run (last_scan: null), treat all notes returned by LBS search as the baseline - record count but do not generate a proposal.

Compute:
- `current_note_count` - notes returned by LBS search matching domain queries (relevance score > 0.70)
- `delta` - `current_note_count - notes_at_scan`

### Step 4: Gap Resonance Check

Read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`.

For each active or converged thinking topic, check: do any new KB notes from Step 3 address the topic's central question or the "Open Questions" section from its last incubation run?

Read the last run's "Open Questions for Next Run" from the thinking file if needed - this is the highest-value resonance target.

A resonance hit = a new note substantively addresses something the incubation loop explicitly flagged as unresolved.

Record resonance hits as HIGH-priority signals.

### Step 5: PIR Check

For each `priority_intelligence_requirements` entry, assess whether any new notes from Step 3 constitute a direct answer, partial answer, or contradiction.

- **Direct hit** - new note directly addresses the PIR question with evidence or argument
- **Partial hit** - new note is relevant but incomplete
- **Miss** - no new notes bear on this PIR

Direct PIR hit = HIGH signal. Partial hit = MEDIUM signal.

### Step 6: External Signal Check

For each `watch_query`, search for recent signals (last 7 days) from reputable sources. The `site:` domains below are a subset of the canonical allowlist in `resources/SOURCE-AUTHORITY.md` - kept inline for in-query reliability; keep in sync with that file.

Use targeted queries:
- `[watch_query] site:arxiv.org OR site:nature.com OR site:pubmed.ncbi.nlm.nih.gov`
- `[watch_query] site:hbr.org OR site:economist.com OR site:quantamagazine.org`
- `[watch_query] breakthrough OR new research OR published 2026`

Extract per result: source name, headline, publication date, one-line summary of the finding.

Assess whether the external signal:
- **Contradicts** a leading hypothesis in the KB → HIGH signal
- **Confirms** an open question in the Thinking Registry → MEDIUM signal
- **Is tangentially related** → LOW, note without escalating

Limit: 2-3 searches per domain. This is signal detection, not a research sprint.

### Step 7: Score Signal Level

Combine inputs from Steps 3-6:

| Signal Level | Criteria |
|---|---|
| **HIGH** | Gap resonance hit, OR PIR direct hit, OR external signal contradicts KB |
| **MEDIUM** | PIR partial hit, OR delta ≥ spawn_threshold, OR external signal confirms open question |
| **LOW** | delta > 0 but < spawn_threshold, no PIR hit, no resonance |
| **NONE** | No new notes, no PIR hits, no external signal |

For HIGH and MEDIUM: compose an incubation proposal (Step 8).
For LOW and NONE: log a brief entry and continue.

### Step 8: Compose Incubation Proposal (HIGH/MEDIUM only)

Draft a precise incubation question - one that could become the "Central Question" in a thinking file. Precision matters: the incubation loop runs better with a sharp question.

Good: "Does Byzantine majority-vote coordination solve the reliability ceiling in multi-agent systems, or does it trade one failure mode for another?"
Bad: "What about multi-agent reliability?"

Compose:
- **Proposed central question** (one precise sentence)
- **Signal basis** - which trigger (PIR hit, gap resonance, external signal, delta) and what it found
- **Initial hypotheses** (1-2, with rough starting confidence based on current KB evidence)
- **Known evidence** from this scan (note links + external source if found)
- **Suggested slug** for the thinking file (kebab-case, ≤ 5 words)

Create the thinking file at `Brain/05-Meta/Thinking/[suggested-slug].md` using the incubation-loop seeding template - fill in the central question, initial hypotheses, and known evidence from this scan. Then add to `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`:

```
| [suggested-slug] | [central question] | active | 0 | null |
```

Write a summary entry to the Watch Log (Step 10) marking it **Auto-activated**.

**Thinking Registry write discipline (hard rule):** activating a topic adds the table ROW above and NOTHING else to `THINKING-REGISTRY.md`. Never write scan narratives, `last_domain_watch` fields, or any other frontmatter keys into the Thinking Registry — scan results belong in the Watch Log (Step 10) and the domain config (Step 9). The registry is an index; duplicating scan narratives there made it unreadable (~100k tokens). If legacy narrative fields exist in its frontmatter, do not update or imitate them.

### Step 8.5: Starvation Floor (guarantee the thinking engine never idles)

After scoring all domains, read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` and count topics with `status: active`.

If **zero proposals were auto-activated this run AND the registry has zero active topics**, the incubation loop would otherwise go idle. Prevent this:

1. Across all watched domains, pick the single **best candidate question** even though no signal reached HIGH/MEDIUM. Rank by, in order:
   - (a) the highest-value `priority_intelligence_requirement` not already covered by an existing topic,
   - (b) the strongest recent external signal found in Step 6 (even if scored LOW),
   - (c) the domain with the largest positive note delta.
2. Compose one incubation proposal for that candidate using the Step 8 format, and activate it: create the thinking file from the incubation-loop seeding template and add it to `THINKING-REGISTRY.md` as `active`.
3. In the Watch Log (Step 10), mark this entry **Starvation-floor activation** (agent-chosen, not signal-driven) so it stays auditable as a self-initiated topic.

Activate exactly ONE topic via the floor per run - enough to keep the engine running; the next run re-evaluates. This is the one place the perception layer chooses a topic on its own initiative rather than in response to a detected signal.

### Step 9: Update Domain Config

Update `Brain/05-Meta/Watching/[domain-slug].md` frontmatter:
- `last_scan: YYYY-MM-DD` (today)
- `notes_at_scan: N` (current_note_count from Step 3)
- `updated: YYYY-MM-DD`
- `updated_by: claude-sonnet-4-6`
- `agent_version: 01.25`

### Step 10: Append to Watch Log

Append to `Brain/05-Meta/Watching/WATCH-LOG.md`. Create the file if it does not exist.

**For HIGH/MEDIUM domains:**

```markdown
## Scan: YYYY-MM-DD

### [domain-slug] - [HIGH/MEDIUM]

**Delta:** +N notes since last scan ([previous-scan-date])
**PIR Hit:** [Direct: "PIR question text" | Partial: "PIR question text" | None]
**Gap Resonance:** [[Thinking-Topic-Slug]] - open question: "[question text]" | None
**External Signal:** [Source: "Headline" (YYYY-MM-DD) - one-line finding | None]

**Proposed Incubation Question:** "[precise central question]"

**Suggested Slug:** `[suggested-slug]`

**Initial Hypotheses:**
- H1: [statement] (~X% confidence) - basis: [note link or source]
- H2: [statement] (~Y% confidence) - basis: [note link or source]

**Known Evidence:**
- [[Note Name]] - [one line on relevance]
- [External source] - [one line on relevance]

**Auto-activated:** [[suggested-slug]] added to Thinking Registry.
```

**For LOW/NONE domains:**

```markdown
### [domain-slug] - [LOW/NONE]
Delta: +N notes. [No PIR hits. No resonance. | Brief note if something mild found.] No proposal.
```

### Step 11: Update Watching Registry

Update `Brain/05-Meta/Watching/WATCHING-REGISTRY.md`:
- Set `last_scan` to today for each processed domain
- Update `updated` frontmatter date

### Step 12: Write Session Changelog

Write to `Brain/05-Meta/Changelogs/CHANGELOG - Domain Watch YYYY-MM-DD.md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Domain Watch Session: YYYY-MM-DD

## Summary

| Domain | Signal | Delta | PIR Hit | Resonance | Proposal |
|--------|--------|-------|---------|-----------|----------|
| [slug] | HIGH | +N | Direct - "PIR text" | [[Thinking Topic]] | Yes |
| [slug] | NONE | 0 | None | None | No |

## Proposals Awaiting Activation

[List domain slugs and proposed questions for HIGH/MEDIUM domains]

To review full proposals: `Brain/05-Meta/Watching/WATCH-LOG.md`
```

---

## Seeding a New Domain

Create `Brain/05-Meta/Watching/[domain-slug].md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
slug: domain-slug
label: "Human-readable domain label"
mode: surveillance
watch_queries:
  - "primary search term"
  - "secondary search term"
priority_intelligence_requirements:
  - "PIR 1: specific question I want answered when it becomes answerable"
  - "PIR 2: specific question I want answered when it becomes answerable"
last_scan: null
notes_at_scan: 0
spawn_threshold: 3
---

# Watching: [Domain Label]

## Why This Domain

[1-2 sentences on why this domain warrants ongoing surveillance]

## What Would Trigger Incubation

[Concrete examples of the kind of signal that would warrant a thinking topic - be specific]

## Related Thinking Topics

[Links to any active/converged thinking files in this domain, if any]
```

Then add to `Brain/05-Meta/Watching/WATCHING-REGISTRY.md`:

```
| [domain-slug] | [label] | surveillance | null | active |
```

---

## Activation

HIGH/MEDIUM proposals are auto-activated by Step 8 - thinking files are created and added to the Thinking Registry automatically. The Watch Log records each activation for review.

When no signal qualifies and the Thinking Registry has zero active topics, the **Starvation Floor (Step 8.5)** activates exactly one agent-chosen topic from the watched domains so the incubation loop never goes idle. These are marked **Starvation-floor activation** in the Watch Log to distinguish them from signal-driven proposals.

When the incubation loop marks a topic `converged`, review it manually via `/synthesize-insights`.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Watching Registry missing | Create empty registry, log, exit cleanly |
| No active domains | Log to changelog, exit cleanly |
| Domain config missing for registered entry | Log warning in registry, skip domain |
| LBS search returns empty | Try alternate watch_query terms; if still empty, note in scan log, continue |
| Web search fails or times out | Skip external signal step, note "external signal: unavailable" in log, continue |
| WATCH-LOG.md missing | Create file with header, proceed |
| First run (last_scan: null) | Record baseline count, write "first scan - baseline established" entry, no proposal |

---

## Completion Checklist

- [ ] Registry read - active domains identified
- [ ] Each domain: LBS search run on all watch_queries
- [ ] Each domain: new note delta computed against baseline
- [ ] Each domain: gap resonance checked against Thinking Registry
- [ ] Each domain: PIR check run against new notes
- [ ] Each domain: external signal search run (2-3 queries)
- [ ] Each domain: signal level scored (HIGH/MEDIUM/LOW/NONE)
- [ ] HIGH/MEDIUM domains: incubation proposal drafted and written to Watch Log
- [ ] HIGH/MEDIUM domains: thinking file created at `Brain/05-Meta/Thinking/[slug].md`
- [ ] HIGH/MEDIUM domains: topic added to `THINKING-REGISTRY.md` with `status: active`
- [ ] Starvation Floor checked: if no proposal activated AND zero active topics, one agent-chosen topic activated from watched domains
- [ ] Floor activations (if any) marked **Starvation-floor activation** in the Watch Log
- [ ] Each domain: config updated (last_scan, notes_at_scan)
- [ ] Watch Log updated with all domains
- [ ] Watching Registry updated
- [ ] Session changelog written

---

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could signal scoring, PIR checking, or proposal drafting be sharper?
- [ ] **Scope check**: Only execution changes - NOT changes to the perceive-score-activate pipeline or signal scoring thresholds
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control**:
  - [ ] `git add .claude/skills/domain-watch/SKILL.md`
  - [ ] `git commit -m "refactor(domain-watch): <brief improvement>"`
