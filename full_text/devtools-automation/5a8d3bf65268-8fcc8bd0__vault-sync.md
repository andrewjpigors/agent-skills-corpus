---
name: vault-sync
description: Use at the end of any agent coding session to reflect what happened back into the Obsidian vault. Reads the session transcript and git history, extracts decisions, tasks, projects, people, research, and other entities, then creates new vault pages or updates existing ones using the right templates and folder placement. Maintains the vault's zero-orphans principle by updating index files and adding wikilinks. Use whenever the user mentions ending a session, wrapping up, syncing to vault, logging the session, updating Obsidian, capturing what we did, saving session notes, or says "/vault-sync", "/end-session", "/log-session" — and after long working sessions even if they don't explicitly ask. Supports planning mode (capture what they intend to do) and work-log mode (capture what actually happened); work-log is the default.
---

# Vault Sync

Closes the loop between an agent session and the user's Obsidian vault. Treats the vault as a structured knowledge base, not a dumping ground: every new note lands in the right folder with the right template and the right wikilinks, and every existing page touched gets a session-log entry rather than a blind overwrite.

## When to use

Trigger this skill:
- **Manually**: `/vault-sync`, `/end-session`, `/log-session`, or any phrasing like "wrap up", "log this session", "sync to vault", "save what we did to obsidian"
- **Automatically**: via the agent's `SessionEnd` hook where supported (see `references/auto-trigger-setup.md`). Auto mode always writes propose-only drafts; it never applies without user review.
- **As fallback**: if the user worked for >30 min and didn't ask for a sync, offer one at the end of the conversation.

Projects live in the same vault but different folders (see folder mapping in `references/folder-mapping.md`).

## Quick start

1. Read this SKILL.md fully.
2. Read `references/vault-conventions.md` for vault structure + frontmatter rules.
3. Run the five-stage pipeline below.
4. Always end on either: a) a written-out propose draft the user can review, or b) an applied set of vault changes + a git commit on the vault repo.

## The five-stage pipeline

```
INGEST → EXTRACT → RECONCILE → PROPOSE → APPLY
```

## Execution model — local by default; delegation approval-only (read this first)

**The active agent that worked the session owns vault-sync by default.** Do not delegate vault-sync to GLM, OpenCode, subagents, or any other executor automatically. Delegation is allowed only when the user explicitly requests it, or after the active agent asks for approval with one concise benefit statement and the user approves.

| Who | Does | Rule |
|---|---|---|
| **Active agent** | INGEST → EXTRACT → RECONCILE → APPLY → AUDIT | Default |
| **Local scripts** | Transcript filtering, markers, generated briefs/rollups, commit audit | Always allowed |
| **GLM/OpenCode** | Optional heavy extraction/apply support | Approval-only |

The reason is control: the user wants the same agent that understands the task to write memory unless they approve offloading. Cost savings never override this rule.

### Default flow (what `/vault-sync` does)

1. **INGEST** (active agent + local scripts, Stage 1 below) — locate + filter transcript, gather git artifacts, vault snapshot. **Re-sync check (#1):** run `scripts/sync-marker.sh read <session_id>`; if it returns a marker (this session was already synced), this is a CONTINUATION — `scripts/sync-marker.sh delta <session_id> <project_cwd>` lists the project commits since last sync. Scope the handoff to that DELTA (new commits/decisions/tasks only), not the whole session. `NONE` = first sync (full handoff); empty output = a prior sync exists but no new project commits since (delta is just any new conversation/decisions); `STALE_HEAD` = history was rewritten (rebase/squash) → fall back to a manual delta judgement.
2. **HANDOFF / MANIFEST** (active agent) — write a concise prose handoff to `~/.cache/vault-sync/handoff-<session_id>.md` (see "Handoff format" below), then extract and reconcile the entities locally.
   - **Trivial fast-path (#6):** run `scripts/count-handoff-entities.sh <handoff>`. `TRIVIAL=empty` → reply "Nothing to sync." and stop. `TRIVIAL=yes` (≤2 high-signal entities) → write the digest plus the few real pages. `TRIVIAL=no` → continue locally unless the user approves delegation.
3. **APPLY** (active agent) — write/update pages using the templates and folder mapping. Preserve idempotency with `session_id`, append Session Log entries, run the wikilink pass, and commit markdown only.
4. **REFRESH AGENT MEMORY** — before committing, run:
   ```bash
   scripts/update-agent-memory.py --project "${VAULT_DEFAULT_PROJECT:-Acme}"
   ```
   This regenerates the compact `Agent Memory Map`, project `AGENT_BRIEF.md`, project static indexes, and current monthly rollup. For backfill/maintenance, run `--all-months`.
5. **AUDIT** — run `scripts/audit-vault-commit.sh <commit> <session_id>` and report hard failures or important warnings.

### Optional delegation path

Only after explicit user request/approval, the agent may invoke the GLM wrapper (export the project cwd + transcript so the wrapper can record a complete re-sync marker):
   ```bash
   VAULT_SESSION_ID="<session_id>" \
   VAULT_SYNC_PROJECT_CWD="<project_cwd>" \
   VAULT_SYNC_TRANSCRIPT="<transcript_path>" \
     bash ~/.claude/skills/vault-sync/scripts/glm-vault-sync.sh ~/.cache/vault-sync/handoff-<session_id>.md
   ```

The wrapper still runs GLM in a throwaway scratch dir, uses the Obsidian MCP, refreshes the generated agent-memory layer, commits markdown only, and prints `GLM_VAULT_SYNC: status=… commit=… log=…`. If GLM fails, return to the local active-agent path; do not silently retry with other delegation.

### Handoff format

The active agent writes this file from its own session context — no transcript re-reading needed beyond INGEST. Keep it tight (prose + bullets, ~30–60 lines). The active agent extracts entities from it locally unless the user approved delegation.

```markdown
# Session handoff — <session_id>
- project: Acme            # or Northwind / Bluebird / Personal Site / cross-cutting
- mode: work_log            # or planning
- date: 2026-06-09
- cwd: ~/projects/my-app

## Summary
<one paragraph: what actually happened this session>

## Decisions
- <title> — <rationale>; alternatives: <…>; status: accepted

## Tasks
- <title> — status: done|in_progress|blocked|todo; <blockers/next-steps if any>

## Tools / orgs / people mentioned (named, real-world)
- <name> — <one-line: what it is / role>

## Git
- commits: <sha subject>, …
- files touched: <paths>
```

> The handoff is the contract. Be complete but don't fabricate. Anything you omit won't reach the vault; anything you invent will.

### Stage 1: INGEST

Three pure-I/O steps. Run them as parallel Bash calls in one tool-use batch — no sub-agents needed.

1. **Locate + filter the session transcript** — Transcripts live at `~/.claude/projects/<encoded-cwd>/<uuid>.jsonl` for Claude Code, or the equivalent transcript directory for the active agent. The encoded cwd replaces `/` with `-` (e.g., `/Users/you/projects/my-app` → `-Users-you-projects-my-app`). **Transcript filenames are agent-internal UUIDs, NOT the `session-<unix-ms>` from OMC SessionStart hooks.**

   To pick the right transcript:
   - If running mid-session: most-recently-modified jsonl is the current session
   - If running fresh-session after a work session: the LARGEST recent jsonl is the work session (the brand-new current session is tiny)
   - When in doubt: `ls -lS *.jsonl | head -3` and pick the substantial one

   **Then always run the filter:**
   ```bash
   scripts/transcript-filter.sh <transcript.jsonl> /tmp/filtered.txt
   ```
   This collapses the raw ~3MB jsonl (~800K tokens) to a ~10KB summary (~2K tokens) of USER messages + WRITE/EDIT file paths + BASH descriptions. **Always extract from the filtered file, never the raw jsonl** — 400x token savings, ~no signal loss for entity extraction.

2. **Git artifacts** — `git log --since="<session-start>" --pretty=format:'%h %s'`, `git diff --stat HEAD~N..HEAD`, `git status --short` against the project cwd. Tiny output, objective ground truth for what code changed.

3. **Vault snapshot** — `ls` of project-relevant vault folders (e.g., `20 - Projects/<project>/Tasks/Decisions/Sessions/`, `90 - Meta/Sessions/_pending/`). Just file inventory + `head -5` of any existing matches by title. This is reconciliation input.

### Stage 2: EXTRACT

**Default: Haiku 4.5, inline (no sub-agent spawn).** Spawn a Sonnet sub-agent only if user passes `--deep` OR session > 4 hours.

**Always pre-filter the transcript first**: run `scripts/transcript-filter.sh <jsonl>` which strips assistant prose (~80% of tokens) and keeps only USER messages, BASH descriptions, WRITE/EDIT file paths, and AGENT descriptions. A 5.9MB raw transcript collapses to <50KB filtered. This is what EXTRACT operates on — never the raw jsonl.

**Why inline by default**: spawning a sub-agent costs 30–60s of fixed overhead (system prompt load, tool acquisition) before any work happens. For a typical 1–3 hour session with a filtered transcript under 20K tokens, running EXTRACT inline in the orchestrator is faster than spawning. Reserve sub-agents for the heavy `--deep` mode.

**Generous entity extraction — second-brain graph behavior**: As you build the manifest, ALSO emit a `type: entity` stub for every named real-world thing mentioned across tasks/decisions/research:
- Companies / orgs (Acme Inc, Acme Bank, Stripe, Braintree, Coinbase Commerce, Cloudinary)
- Services / SaaS / tools (Cloudflare, Resend, Supabase, RunPod, Vercel)
- Real people (any named individual with a stated role — account managers, sales reps, lawyers, accountants, government contacts, processor underwriters, vendors who sign business correspondence). **Minimum confidence 0.75** because future-you needs to know who to ping back. Even when they only appear once in the session, if they signed an email or made a phone call to us, they MUST get a Person page — they're an active contact, not a passing mention. Missing a named-role contact is the same kind of failure as missing a decision.
- Regulations / laws / standards (GDPR, MiCA, Texas HB1181, Visa VIRP, §2257)
- Banks / payment institutions (Acme Bank, Mercury, Wise)
- Significant places (only when load-bearing — Wyoming, Egypt as legal entities)

Be generous in extraction, conservative in confidence. Auto-extracted stubs carry `confidence: 0.50-0.65` and `auto_extracted: true` — the user will prune them on review (or in a hygiene pass). A stub is better than a missing node — a missing entity breaks the graph.

**Value gate (#5) — exempt ubiquitous infrastructure.** "Generous" does NOT mean paging the toolchain. Do NOT create, or churn session-log entries into, tools that are merely *present* every session rather than the *subject* of one: Next.js, React, TypeScript, Biome, Vitest, lefthook, git, npm, pnpm, Bash, VS Code, ESLint, Prettier. Page a tool only when it's load-bearing this session (the subject of a decision/task, newly adopted, or breaking). People with a stated role remain the always-page exception. (The GLM brief enforces the same gate; this keeps the inline-fallback path consistent.)

The skill then auto-creates these stub pages AND performs a wikilink pass after APPLY that replaces plain-text mentions across all just-written pages with `[[Entity Name]]` links. This is what makes the vault a true second-brain graph rather than just a folder of disconnected notes.

Produce a structured JSON manifest:

```json
{
  "session_id": "session-1779776466369",
  "started_at": "2026-05-26T10:00:00Z",
  "ended_at": "2026-05-26T14:32:00Z",
  "cwd": "~/projects/my-app",
  "project": "Acme",
  "mode": "work_log",
  "summary": "One-paragraph TL;DR of what happened.",
  "entities": [
    {
      "type": "task",
      "title": "Build vault-sync skill",
      "status": "in_progress",
      "blockers": [],
      "next_steps": ["Run eval test prompts", "Iterate based on review"],
      "files_touched": ["~/.claude/skills/vault-sync/SKILL.md"],
      "evidence_turn": 12,
      "confidence": 0.95
    },
    {
      "type": "decision",
      "title": "Hybrid model routing: Haiku orchestration + Sonnet for EXTRACT",
      "rationale": "...",
      "alternatives_considered": ["Pure Sonnet", "Pure Haiku"],
      "evidence_turn": 8,
      "confidence": 0.9
    }
  ],
  "git": {
    "commits": [{"sha": "abc123", "subject": "feat: ..."}],
    "files_changed": ["..."],
    "uncommitted": ["..."]
  }
}
```

Entity types: `task`, `decision`, `research`, `project`, `person`, `meeting`, `reference`, `idea`, `blocker`.

Confidence scoring is critical — it drives the threshold gating in PROPOSE. Be honest: if the user mentioned something once in passing and never returned to it, that's low confidence, not high.

See `references/extraction-rules.md` for type-by-type extraction heuristics and edge cases (e.g., distinguishing "decided to do X" from "discussed doing X but rejected").

### Stage 3: RECONCILE

**Model: Haiku 4.5** (mechanical comparison).

For each entity in the manifest:

1. Search the vault for existing matches using:
   - `grep -ril "<title>" "$VAULT_DIR"/` for exact-ish title match
   - Frontmatter `name:`, `aliases:`, `project:` matches
   - Fuzzy match on file basename
2. Output one of: `create`, `update`, `ambiguous`.
3. For `update`, identify the target file path. For `ambiguous`, list the candidates.

The reconciliation output extends the entity with:
```json
{
  "action": "create" | "update" | "ambiguous",
  "target_path": "20 - Projects/Acme/Tasks/Build vault-sync skill.md",
  "match_candidates": [],
  "match_confidence": 0.85
}
```

### Stage 4: PROPOSE

**Model: Haiku 4.5** (templating).

Write a single dry-run draft to `90 - Meta/Sessions/_pending/<YYYY-MM-DD-HHMM>-<session-id>.md` containing:

1. Session metadata (id, project, duration, mode, model used)
2. Summary
3. Section per proposed action with: action type, target path, full content preview, confidence, match candidates if ambiguous
4. A trailer with `## Apply Instructions` — the exact prompt the user can paste back to trigger APPLY (or "Confirm" alone if running interactively)

This draft is the user's review artifact. Even in auto mode, this is what gets written first.

### Stage 5: APPLY

**Default: active-agent local apply.** The active agent writes/updates the vault pages itself using the transcript filter, handoff, templates, folder mapping, and local scripts. The user gets back a concise confirmation after verification.

The GLM wrapper (`scripts/glm-vault-sync.sh`) is available only for explicit user request/approval. If approved, it must follow the same guardrails: canonical paths/frontmatter, `session_id` idempotency, wikilink pass, generated memory refresh, markdown-only commit, and content audit.

Use `--review` flag for the old propose-then-apply flow only when:
- User explicitly asks for review
- Session was unusually heavy (>30 entities) where pre-screening might save vault clutter
- Confidence range includes any entity below 0.60

#### Optional GLM wrapper outcomes

If the user approved GLM delegation, the wrapper returns distinct exit codes; the active agent branches on them:

| Wrapper exit / status | Meaning | Active agent action |
|---|---|---|
| `0` / `status=ok` | GLM wrote pages; wrapper committed | Run the **content audit** `scripts/audit-vault-commit.sh <commit> <session_id>` (#2); report ≤3 lines (sha + files + warnings). Exit 1 = hard problem, surface it. Done. |
| `127` / `no_opencode` | opencode not on PATH | **Fall back to inline apply**, and say so in the output. |
| `124` / `timeout` | GLM exceeded `GLM_TIMEOUT` (vault auto-rolled-back to clean) | **Fall back to inline apply**, and say so. |
| `4` / `no_obsidian` | Obsidian app/MCP unreachable **even after the wrapper auto-launched Obsidian and polled ~15s**, or no API key | **Fall back to inline apply** (active agent writes via Bash/Write, no MCP), and say so. |
| `3` / `no_commit` | GLM ran but wrote no `*.md` changes | If this `session_id` is already in the vault (re-run of a synced session) → **"Nothing to sync"** (idempotent no-op). Else if the handoff had real entities → **fall back to inline apply** and say so. Empty handoff → "Nothing to sync." |
| `2` (note conflict) | tracked, non-`.obsidian` note has uncommitted edits | **Stop and surface** — do NOT fall back (inline apply refuses too). Ask the user to commit/stash their in-flight note edits. (Ambient `.obsidian/` churn does NOT trigger this.) |
| `1` (handoff missing/empty) | orchestrator bug | Fix the handoff path and retry; this is not a GLM failure. |

State the fallback explicitly in chat, e.g. `GLM unavailable (opencode missing) — applied inline instead.` The user must always know which executor ran.

**Local apply implementation pattern**: single pass from Bash + Write/Edit. The active agent performs entity-sweep enrichment, writes all entity pages, runs the wikilink pass (replacing plain mentions with `[[wikilinks]]` across all just-written files, skipping self-references AND existing `[[...]]` regions AND code blocks AND YAML frontmatter), writes the session digest directly to `90 - Meta/Sessions/<YYYY-MM>/`, refreshes the agent-memory layer, and commits with the same `chore(vault): sync <id> — <summary>` convention. A 14-entity apply runs in ~1 second.

**Skip conditions for further speed** (iter-5):
- **Trivial session / fast-path (#6)**: classify with `scripts/count-handoff-entities.sh <handoff>` (high-signal = decisions + tasks + people; tool stubs don't count). `TRIVIAL=yes` (≤2 high-signal) → write the digest (+ the ≤2 pages) and commit. `TRIVIAL=empty` (0 high-signal, no commit) → "Nothing to sync."
- **Empty session** (no entities extracted at all): emit "Nothing to sync" and exit. No commit, no draft.
- **Entity-sweep cache**: cache the master entity list at `~/.cache/vault-sync/entities.json` (refreshed weekly or when vault folders change). Lets the wikilink pass run without re-scanning the entire vault each time.
- **Incremental / re-sync marker (#1)**: `scripts/sync-marker.sh` records per-session `{vault_commit, project_head, transcript_lines, synced_at, sync_count}` after each successful sync (the wrapper writes it; the inline fallback should too). On a re-sync, `sync-marker.sh delta <session_id> <project_cwd>` returns the project commits since last time, so the handoff covers only the delta instead of the whole session.

**Wikilink pass** (added iter-4):
After writing all entity pages, walk each just-written file and for every entity name in the manifest, replace plain-text mentions with `[[Entity Name]]` (excluding the entity's own page and existing wikilink occurrences). This is what gives you the second-brain graph — open any task, see backlinks to every related decision/entity/research.

Gated by the per-action threshold table:

| Action | Risk | Auto-apply threshold | Below threshold |
|---|---|---|---|
| Update existing page (append session log, flip status) | Low — reversible, additive | 60%+ | Propose |
| Create new page | Medium — adds clutter to clean | 75%+ | Propose |
| Move/rename existing page | High — breaks wikilinks | Never auto | Always propose |
| Edit frontmatter (other than `updated:` field) | Medium-high — could corrupt data | 85%+ | Propose |
| Update index/MOC files | Low | 70%+ | Propose |
| Delete | Very high | Never auto | Always propose |

These thresholds govern both local apply and any approved GLM wrapper run. Auto-triggered runs (`SessionEnd` hook) still write a propose-only draft and skip apply, regardless of executor.

**Local apply steps**:
1. For each `create` action above threshold: write the new file using the right template from `templates/` and the folder mapping in `references/folder-mapping.md`.
2. For each `update` action: append a `## Session Log` entry (or create the section) with format `### YYYY-MM-DD HH:MM — session-<id>\n<bullet summary>`. Update frontmatter `updated:` field. Update `status:` per status-transition rules in `references/extraction-rules.md`.
3. Update any relevant `<folder> Index.md` so new files appear in dataview blocks and link tables — preserves the zero-orphans principle.
4. Move the dry-run draft from `90 - Meta/Sessions/_pending/` to `90 - Meta/Sessions/<YYYY-MM>/` after setting `status: applied` AND stamping `applied_at:` in frontmatter (the digest template ships `status: draft`, so this step must overwrite it — the content audit (#2) hard-fails any digest not at `status: applied`). This becomes the canonical session digest.
5. Run `scripts/update-agent-memory.py --project "${VAULT_DEFAULT_PROJECT:-Acme}"` so agents can use `Agent Memory Map`, `AGENT_BRIEF.md`, and monthly rollups before reading detailed notes.
6. Run `git -C "$VAULT_DIR" add -A -- '*.md' ':!.obsidian' && git -C "$VAULT_DIR" commit -m "chore(vault): sync session <id> — <one-line-summary>"`.

## Two modes

### Work-log mode (default)

Captures retrospective: what actually changed, what got decided, what got built, what got stuck. Tasks created here default to `status: done` if they were completed in-session, `status: in_progress` with blockers if not. Adds Session Log entries to every project/task page touched.

### Planning mode (`/vault-sync --plan` or auto-detected from "let's plan", "strategy session", "here's what I want to do next")

Captures prospective: what the user *intends* to do. Tasks created here default to `status: todo`, no completion timestamp. If the session sketched a multi-step plan, create a parent strategy page in the project's folder, then individual task pages with `project:` and `parent:` wikilinks back to it. Update `60 - Tasks/This Week/This Week.md` dataview if any items are imminent.

The two modes are not mutually exclusive — a single session can have both. The EXTRACT JSON has a `mode` per entity, not just per session.

## Folder placement (summary)

| Entity type | Goes to |
|---|---|
| Task (project-scoped) | `<project-folder>/Tasks/<title>.md` with `project:` wikilink |
| Task (cross-cutting) | `60 - Tasks/<title>.md` |
| Decision | `<project-folder>/Decisions/<title>.md` (creates folder if needed) |
| Research note | `10 - Zettelkasten/References/<title>.md` or `<project>/Research/<title>.md` if narrow scope |
| Project | `20 - Projects/<name>/` (new folder + Project Template) |
| Company / Entity (generic new thing) | Closest matching existing location — see `references/folder-mapping.md` |
| Person | `55 - People/<name>.md` (Person Template) |
| Meeting | `20 - Projects/<Project>/Meetings/<YYYY-MM-DD>-<title>.md` |
| Session log/digest | `90 - Meta/Sessions/<YYYY-MM>/<session>.md` |
| Idea (vague, not actionable) | `00 - Inbox/<YYYY-MM-DD>-<short-title>.md` |

Full mapping with examples in `references/folder-mapping.md`.

## Agent memory layer

The vault keeps detailed notes forever, but agents should not read old detail by default. Every meaningful sync must refresh a generated navigation layer:

| File | Purpose |
|---|---|
| `90 - Meta/Agent Memory Map.md` | Global router: which project brief or monthly rollup to read first |
| `20 - Projects/<Project>/AGENT_BRIEF.md` | Current-state brief: latest sessions, active decisions, top tasks, blockers |
| `90 - Meta/Monthly Rollups/<YYYY-MM>-<Project>.md` | Monthly compaction: one high-signal summary for old sessions/tasks/decisions |
| `20 - Projects/<Project>/*/* Index.md` | Static project indexes with small agent snapshots plus Dataview |

Run:

```bash
scripts/update-agent-memory.py --project "${VAULT_DEFAULT_PROJECT:-Acme}"
```

For monthly backfill or maintenance:

```bash
scripts/update-agent-memory.py --project "${VAULT_DEFAULT_PROJECT:-Acme}" --all-months
```

Monthly rollups do not delete or replace source notes. They summarize shipped work, accepted decisions, open tasks, blockers, superseded/noisy items, and 5-10 `Read next` source links. Agents should read the current brief first, then the relevant monthly rollup, then detailed notes only if necessary.

## Frontmatter conventions

The vault uses both string-tag (`tags: #daily`) and array-tag (`tags: [project, saas]`) forms inconsistently. **This skill always writes the array form** — it's structured, dataview-friendly, and forward-compatible.

Every page written by this skill includes:

```yaml
---
type: <task|decision|project|person|research|session|...>
created: 2026-05-26
updated: 2026-05-26
tags: [<type>, <project-slug>, <other>]
session_id: session-1779776466369   # for idempotency
---
```

`session_id` is what makes the skill idempotent — running it again on the same session updates existing pages rather than creating duplicates. Full schema in `references/frontmatter-spec.md`.

## Templates

Live in `templates/`:
- `session-digest.md` — the canonical per-session summary page
- `task.md` — improved version of the existing vault task template
- `decision.md` — ADR-style decision record
- `entity.md` — generic catch-all for anything (companies, tools, references) that doesn't have a specific template

When writing new pages, **always start from a template** and fill placeholders. Do not invent new structures ad hoc — consistency is the point of the vault.

## Model routing

Default path: **the active agent is the executor and auditor.** GLM/OpenCode is an approval-only optional helper, never the automatic path.

| Stage | Default executor | Optional approved executor | Why |
|---|---|---|---|
| INGEST | Active agent + local scripts | same | Pure I/O |
| HANDOFF | Active agent | same | The active agent has the best session context |
| EXTRACT | Active agent | GLM/OpenCode only after approval | Avoid automatic delegation |
| RECONCILE | Active agent | GLM/OpenCode only after approval | Preserve control and context |
| APPLY | Active agent + local scripts | GLM wrapper only after approval | Local by default |
| REFRESH MEMORY | `scripts/update-agent-memory.py` | same | Deterministic, no model needed |
| AUDIT | Active agent + `audit-vault-commit.sh` | same | Verification stays local |

**GLM auth**: z.ai "Coding Plan" API key persisted in `~/.local/share/opencode/auth.json` (provider `zai-coding-plan`) — available for approved runs only. Verify with `opencode auth list`.

**Obsidian MCP requirement**: only the approved GLM wrapper needs the Obsidian app running with the "Local REST API with MCP" plugin (`obsidian-local-rest-api` ≥ 4.1) enabled, serving `https://127.0.0.1:27124/mcp`. The wrapper reads the plugin's API key from `<vault>/.obsidian/plugins/obsidian-local-rest-api/data.json` at runtime (never written elsewhere) and injects the MCP via `OPENCODE_CONFIG_CONTENT`. The plugin's HTTPS cert is self-signed, so the wrapper sets `NODE_TLS_REJECT_UNAUTHORIZED=0` for the localhost-only opencode subprocess. **If the health check fails, the wrapper auto-launches Obsidian (`open -ga Obsidian`, no focus steal) and polls the health endpoint for `OBSIDIAN_LAUNCH_WAIT` seconds (default 15; cold launch typically comes up in ~2s)** — so a closed app no longer forces a fallback. Only if it's still unreachable after that → wrapper exit 4 → inline fallback.

**Delegation breadcrumb**: whenever the approved GLM wrapper is unavailable or fails (exit 4/124/127/3-glm_error), it appends a grep-able line to `~/.cache/vault-sync/glm-logs/fallbacks.log` (timestamp · session · exit · reason · log) and prints a `GLM SKIPPED` line. The active agent then continues locally and says so.

**Target performance**: keep the chat response short and the vault context bounded. Use the generated brief/rollups to avoid token-heavy vault reads.

## Output discipline (orchestrator)

When this skill runs (default auto-apply mode), output to user is **≤3 lines, no headings, no tables in chat** (iter-5 tightened from ≤5):

```
✓ N entities · M wikilinks · <digest-path>
Commit: <sha-short>
[Optional 1 line: only if something below threshold needs review]
```

For trivial sessions (≤2 entities): one line total. `✓ <one-line-summary> · <commit-sha>`.

For empty sessions: one line. `Nothing to sync.`

No section headers. No prose recap. No tables. The vault IS the report — user opens Obsidian, not the chat.

When `--review` is used, output adds:
- One line: "Draft at <path> — reply `apply` to write, `discard` to drop"

The user is in a hurry when they invoke this. Every line of orchestrator narration eats their wall-clock time and tokens. Sub-second is the goal for the final response.

## Idempotency

The skill is safe to re-run. On every run:
- New entities not yet matching any vault page → created
- Entities matching an existing page with the same `session_id` in its `## Session Log` → no duplicate entry, but `updated:` frontmatter refreshed
- Entities matching an existing page from a *different* session → new Session Log entry appended, content fields updated per rules

Test re-runs in propose mode before applying to verify no spurious changes.

## Failure modes & guardrails

- **Can't find transcript** → Fail loudly, don't proceed. The skill's value comes from ground truth.
- **In-flight note edits** (a tracked, non-`.obsidian` note is uncommitted before APPLY) → Stop and surface (wrapper exit 2). Don't mix our commit with the user's in-flight note work. Note: a *live* Obsidian vault is almost never globally git-clean (`.obsidian/workspace.json` churns constantly) — so the precheck and commit are scoped to `*.md` content and **deliberately ignore `.obsidian/` churn and stray `*.base` files**. Only a real note conflict blocks.
- **GLM/opencode/Obsidian unavailable after approved delegation** (opencode missing → wrapper exit 127; GLM timeout → exit 124 with auto-rollback; Obsidian MCP unreachable → exit 4; GLM wrote nothing → exit 3) → continue with the local active-agent apply and state it explicitly. Never silently retry delegation.
- **Ambiguous entity match** → Always propose, never auto-decide. Batch all ambiguities into one user prompt at end of PROPOSE, not interactively throughout.
- **Long session, low-signal content** (a 4-hour conversation that produced 2 small commits) → Still produce a digest, but flag in summary that artifact density was low — the user may not need a full sync.
- **Brand-new project not yet in vault** → Create the project folder + `Project Template` page first, **then** nest tasks/decisions under it. Always surface this as an explicit CREATE action in the propose draft (high priority, top of the draft) — never as a silent side-effect. Orphan files violate the zero-orphans principle, and a missing project page means every child task's `project:` wikilink resolves to nothing.

- **Status vocabulary is canonical for dataview compatibility** — `todo | in_progress | blocked | done` for tasks; `proposed | accepted | superseded | rejected` for decisions. The skill normalizes user variations (user says "planned" → write `todo`; user says "made" → write `accepted`) but NEVER invents new values. Dataview queries across the vault filter on the canonical set, and unknown values silently disappear from dashboards.

- **Anti-fabrication discipline** — When the user says "launch payment billing by end of June," the task is "Launch payment billing," due June 30, and that is the whole task. Do not invent sub-tasks, acceptance criteria, owners, milestones, or "helpful" details the user didn't state. Lower confidence and an explicit `gaps:` array beats a plausible-looking but fabricated entity. See `references/extraction-rules.md` "Anti-fabrication rule" section.
- **Hard bans from project AGENTS.md** (for example, product content-safety rules) — these are content policies for product code, not vault. Skill writes about them factually if they came up in the session. Don't editorialize.

## Vault hygiene (lightweight, ongoing)

While reconciling, the skill should opportunistically notice (and surface in the digest, not auto-fix):
- Orphaned files (no inbound wikilinks) it encounters
- Missing or stale `updated:` frontmatter
- Index files that don't list a sibling file
- Empty placeholder files (e.g., `2026-02-21.md` at vault root with 0 bytes)

These get logged in a `## Vault Hygiene Observations` section of the session digest. A separate full audit + restructure happens later — not as a side-effect of this skill.

## Native-memory maintenance (`memory-gc`)

Separate from the Obsidian vault, Codex keeps a **native memory** dir per project
(`~/.Codex/projects/<encoded-cwd>/memory/` + a `MEMORY.md` index loaded every session).
`scripts/memory-gc.py` keeps that index lean using spaced-repetition decay + reinforcement
so it never needs a manual consolidation pass. Stdlib-only; frontmatter is edited surgically
(existing YAML order + the curated `MEMORY.md` hooks are preserved).

**Model.** Each memory file carries `tier` (evergreen|active|archive), `last_used` (ISO date),
and `hits` (int). Adaptive idle window = `base_days × (1 + hits)`, capped (defaults 14d / 120d) —
frequently-used memories earn a longer leash. **Evergreen never decays** (feedback/user memories,
and anything with hard-ban prose: religion / step-family / incest). Tier inference errs toward
evergreen (safe — never auto-deletes); links to other memories are stripped before the hard-ban
check so a `[[…-religion-…]]` wikilink can't falsely promote.

**Operations** (run from the project dir so the memory path auto-resolves; or pass `--memory-dir`):
| Command | What | Safety |
|---|---|---|
| `memory-gc.py init` | backfill `tier/last_used/hits` (infer tier, `last_used=today`, `hits=0`) | additive; `--dry-run` to preview |
| `memory-gc.py report` | table of tier / idle / window / status per memory | read-only |
| `memory-gc.py gc` | archive stale non-evergreen (→ `archive/`, drop from `MEMORY.md`) | **DRY-RUN unless `--apply`** |
| `memory-gc.py reinforce --topics a,b` / `--transcript FILE` | bump `last_used`+`hits` for memories used; **promote** resurfaced ones back (restoring their exact index line) | additive; `--apply` to write |
| `memory-gc.py rank --text-file F` | score memories' relevance to a text (read-only); powers topic auto-derive | read-only |
| `memory-gc.py promote NAME` / `archive NAME` | manual override | `--apply` to write |

**Reinforcement hook (end-of-session, auto-derived — #3).** At session end (after AUDIT),
reinforce the native memory. Don't guess the topics from memory — derive candidates from the
handoff (which already names the work): run
`scripts/derive-memory-topics.sh ~/.cache/vault-sync/handoff-<session_id>.md`. It ranks slugs
against the handoff's high-signal text (project + Summary + decision/task titles only; the
Tools/Git sections are excluded because their generic tokens cross-match). Token overlap is
noisy, so treat the output as a **candidate shortlist**, not gospel: pick the genuinely-relevant
slugs (you have full session context) and reinforce them precisely with
`python3 ~/.Codex/skills/vault-sync/scripts/memory-gc.py reinforce --topics <picks> --apply`.
This is still human-gated for precision, but the picks are now data-driven from the handoff
instead of recalled from nothing. Reinforce auto-promotes any archived memory that resurfaced.

**Decay cadence.** `gc` is **not** auto-run — archiving is destructive, so it stays manual/opt-in:
invoke `/memory-gc` (or the script) periodically (~weekly), review the dry-run, then `--apply`.
Archived files cost only disk; nothing is deleted, and `reinforce`/`promote` restore them intact.

## Slash command setup

Create `.Codex/commands/vault-sync.md` in the user's project (or globally) that invokes this skill. Auto-trigger setup via `SessionEnd` hook in `references/auto-trigger-setup.md`.

## What this skill is NOT

- Not a real-time logger (use the daily note for that)
- Not a chat backup (the jsonl transcript already exists; we extract from it)
- Not a Notion sync (we deliberately picked Obsidian)
- Not a vault-wide refactor (that's a separate operation)
- Not a swarm orchestrator — it's a sequential pipeline with two parallel I/O fan-outs
