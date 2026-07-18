---
name: human-review
description: >-
  Interactively resolves items that iteratotron and bug-burndown have
  escalated to needs_human or requires_human_review status. Reads the
  active session queues, reconstructs each item's context from linked
  specs / ADRs / threat-model entries plus the current gap analysis,
  generates 2-4 candidate resolutions consistent with the in-flight
  scope, and runs an AskUserQuestion interview per item. Records each
  decision and re-queues actionable items so the parent skill's Stop
  hook re-engages the dispatcher. Scans all sessions by default —
  including the bug-burndown sessions a harness-builder runtime harness
  spawns per iteration (origin: noelle-harness) — and asks how to scope
  the drain when items span multiple sessions. Use when iteratotron or
  bug-burndown has parked items for human design input, when a
  harness-builder loop won't converge because of parked needs_human
  items, when you want to clear the human review queue between sessions,
  or whenever the parent skill's Phase 8 summary lists `needs_human`
  counts greater than zero. Triggers: human review, clear needs_human,
  resolve human items, unblock backlog, unblock harness, interview
  backlog, decide needs_human, escalation queue, design input, human
  decision queue.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: >-
  Read Write Edit Glob Grep Bash(git*) Bash(jq*) Bash(rg*) Bash(find*)
  Bash(python3*) Bash(ls*) Bash(cat*) Bash(test*) AskUserQuestion
  WebSearch WebFetch Agent Skill
compatibility: >-
  Scans all `.iteratotron/<id>/` and `.bug-burndown/<id>/` sessions
  (default), including harness-builder-spawned bug-burndown sessions
  (`manifest.yaml` `origin: noelle-harness`), produced by iteratotron
  v1.0+, bug-burndown v1.0+, and harness-builder runtime harnesses. Hook
  path assumes global install at ~/.claude/skills/human-review/ (or the
  opencode skills dir). Requires python3.
---

# Human Review — interactive resolver for parked items

You're the human-in-the-loop bridge between two autonomous orchestrators
(`iteratotron` and `bug-burndown`) and the humans who have to make the
calls those orchestrators can't make mechanically. When a scope or bug
hits `needs_human` or `requires_human_review`, it sits in a JSONL queue
until someone decides what to do. You're that someone's assistant.

You don't make the calls yourself. You research each parked item against
the project's specs, ADRs, threat model, and current gap analysis, draft
2-4 well-reasoned options ranked by consistency with the work already
in flight, then ask the human via `AskUserQuestion`. Once they pick,
you record the decision and flip the queue entry's status so the
parent skill's Stop hook re-engages the dispatcher.

## When to Use This Skill

- A `bug-burndown` or `iteratotron` session finished and the chat summary lists `needs_human` items > 0
- You're about to run `bug-burndown resume:<id>` or `iteratotron resume:<id>` and want to clear human-input blockers first
- The `human_review_queue.md` artefact accumulated items across sessions and needs draining
- A subagent's adversarial review returned `NEEDS_HUMAN` and you want to act on it without re-running the whole pipeline
- You want to audit prior `needs_human` decisions for consistency with the current scope
- A `harness-builder` runtime harness loop won't converge because its burndown bridge parked items as `needs_human` in the per-iteration sessions it spawned — drain those (default `scope:all` or `scope:harness`) to unblock the fixpoint

## Quick Start

Arguments: `[session:<id>] [skill:iteratotron|bug-burndown|both] [scope:all|current|harness] [include-blocked:yes|no]`

Defaults: **scan every session**, not just `CURRENT`. The default scope is
`all` — the collector runs with `--all-sessions`, enumerating every
`.iteratotron/<id>/` and `.bug-burndown/<id>/` directory, including the
many bug-burndown sessions spawned by a `harness-builder` runtime harness
(one per `.harness/iter-NNN/` capture). `needs_human` and
`requires_human_review` statuses are included; `blocked` is excluded
unless you pass `include-blocked:yes`; sessions that already have a
non-empty `human_decisions/` directory are skipped unless you pass
`scope:all include-decided:yes`.

Why all-sessions by default: a harness loop parks items in the session
*it* spawned, never in `.bug-burndown/CURRENT`. A CURRENT-only scan
reports "nothing to review" while dozens of parked items quietly block
the harness's global fixpoint. Scanning everything is the safe default;
narrow with `scope:current` or `session:<id>` only when you mean to.

**When the discovered items span more than one session or origin, ask the
user how to scope the drain before interviewing** (see Phase 1d) — that's
the ambiguity gate.

The skill runs six phases:

1. **Discover** — enumerate sessions (all by default), gather parked items, resolve scope ambiguity
2. **Contextualise** — load linked artefacts and current gap inventory per item
3. **Research** — draft 2-4 informed resolution options per item, ranked by consistency
4. **Interview** — present each item via `AskUserQuestion` with the recommended option first
5. **Persist** — write decision records and mutate queue status atomically
6. **Hand back** — return a status block so the parent skill's Stop hook re-engages

## Live context (auto-injected at load)

- Active iteratotron session:  !`cat .iteratotron/CURRENT 2>/dev/null || echo "none"`
- Active bug-burndown session: !`cat .bug-burndown/CURRENT 2>/dev/null || echo "none"`
- Bug-burndown sessions total: !`ls -1d .bug-burndown/*/ 2>/dev/null | wc -l | tr -d ' '`
- Harness-origin bb sessions:  !`grep -rl 'origin:[[:space:]]*noelle-harness' .bug-burndown/*/manifest.yaml 2>/dev/null | wc -l | tr -d ' '`
- Harness iteration dirs:      !`ls -1d .harness/iter-*/ 2>/dev/null | wc -l | tr -d ' '`
- Repo root:                   !`git rev-parse --show-toplevel 2>/dev/null || echo "not a git repo"`
- Current branch:              !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "n/a"`

## Architecture

```
   you (human-review)
        │
        ▼
   Phase 1: discover ALL sessions (CURRENT + harness-spawned + prior),
            filter to needs_human items, resolve scope ambiguity (ask)
        │
        ▼
   Phase 2-3: for each item — load artefacts, draft options
        │
        ▼
   Phase 4: AskUserQuestion (one item at a time)
        │
        ▼
   Phase 5: write decision record, mutate queue.jsonl atomically
        │
        ▼
   parent skill's Stop hook re-engages on next turn:
   - needs_human (terminal) → queued (non-terminal) → dispatcher resumes
   - a harness-spawned bug-burndown session unblocks its loop the same way
```

### Session sources

`needs_human` items live in three places, all scanned by default:

| Source | Path | Discriminator |
|---|---|---|
| Interactive iteratotron | `.iteratotron/<CURRENT>/scope_queue.jsonl` | pointed at by `.iteratotron/CURRENT` |
| Interactive bug-burndown | `.bug-burndown/<CURRENT>/queue.jsonl` | pointed at by `.bug-burndown/CURRENT` |
| **Harness-spawned bug-burndown** | `.bug-burndown/<id>/queue.jsonl` | `manifest.yaml` has `origin: noelle-harness` + a `log_files: .harness/iter-NNN/...` link; **not** in CURRENT |

The harness-spawned sessions are the ones a CURRENT-only scan misses. See
"Phase 1 — the harness-builder layout" below.

The parent skill's Stop hook treats `needs_human` as terminal and `queued`
as non-terminal. Flipping the status is the entire integration — no
parent-side glue beyond a single Skill invocation.

---

## Phase 1 — Discover

### The harness-builder layout

`harness-builder` scaffolds a runtime quality harness that runs the loop
`INSTRUMENT → DRIVE → OBSERVE → TRIAGE → SCHEDULE → BURN DOWN → repeat`
until a global fixpoint. Each iteration is captured under:

```
.harness/iter-NNN/
  noelled.log      # the daemon/app log gathered during DRIVE/OBSERVE
  cargo.log        # build output
  burndown.log     # transcript of the BURN DOWN phase (present once reviewed)
```

The BURN DOWN phase drives its bridge by launching a **new
`bug-burndown` session per iteration**. That session lands at
`.bug-burndown/<id>/` with a `manifest.yaml` carrying:

```yaml
origin: noelle-harness
log_files:
  - .harness/iter-003/noelled.log
```

Crucially, **`.bug-burndown/CURRENT` is not updated to point at these
harness-spawned sessions** — CURRENT tracks the operator's interactive
session. So when the harness's burndown agent escalates a bug to
`needs_human`, that item sits in a session the default CURRENT-only scan
never looks at, and it silently blocks the harness from ever reaching its
fixpoint (a `needs_human` item is terminal-`WorkRemaining` for the loop).

This skill's job for a harness is: **find those parked items across every
harness-spawned session, get the human to decide, and flip the status to
a non-terminal value (`queued` / `re-evaluate`) so the next harness round
re-dispatches and the loop can converge.**

### 1a. Enumerate sessions — all by default

The default scope is `all`. Don't restrict to CURRENT unless the user
asked for `scope:current` or a specific `session:<id>`.

```bash
mkdir -p .human-review
SC="$HOME/.config/opencode/skills/human-review/scripts/collect-human-items.py"
# (the canonical path is the opencode skills dir; the ~/.claude path is a
#  symlink alias on this host and also works)
```

### 1b. Gather parked items

Run the collector in the scope the user selected (default `all`):

```bash
# DEFAULT — every iteratotron + bug-burndown session, harness-spawned included:
python3 "$SC" --all-sessions > .human-review/work.jsonl

# scope:harness — only harness-origin bug-burndown sessions + CURRENT:
python3 "$SC" --scan-harness > .human-review/work.jsonl

# scope:current — legacy CURRENT-only behaviour (narrowest):
python3 "$SC" \
    --session-iteratotron "$(cat .iteratotron/CURRENT 2>/dev/null)" \
    --session-bug-burndown "$(cat .bug-burndown/CURRENT 2>/dev/null)" \
    > .human-review/work.jsonl
```

Add `--include-blocked` when `include-blocked:yes`. Add `--include-decided`
to re-surface sessions that already have a `human_decisions/` directory
(off by default so re-running the drain doesn't re-ask resolved items).

The collector produces one JSONL line per parked item with the fields:
`source_skill`, `session_id`, `item_id`, `status`, `kind`, `priority`,
`title`, `linked_artefacts`, `attempt_count`, `last_error`, `queue_path`,
`needs_human_dir`, **`origin`** (e.g. `noelle-harness`), and
**`harness_iter`** (the `iter-NNN` that spawned a harness session, or
null). See [references/queue-mutation.md](references/queue-mutation.md)
for the full schema and the difference between source-skill shapes.

### 1c. Honour the filter args

If `skill:iteratotron` was passed, drop bug-burndown items. If
`session:<id>` was passed, drop entries with a different `session_id`.
If `include-blocked:no` (default), drop entries with `status: blocked`
and keep only `needs_human` / `requires_human_review` ones.

### 1d. Resolve scope ambiguity — ASK before interviewing

The all-sessions default can surface items from many sessions and origins
at once. **When the gathered items span more than one session, or mix
harness-spawned and interactive origins, you don't silently interview all
of them — you ask the user how to scope the drain first.** Group the items
by `(origin, session_id, harness_iter)` and present the breakdown via
`AskUserQuestion`:

```
question: "Found <n> parked items across <s> sessions
           (<h> harness-spawned, <i> interactive). How should I scope this drain?"
header:   "Drain scope"
options:
  - label:       "All sessions (Recommended)"
    description: "Interview all <n> items across all <s> sessions. Each
                  resolution unblocks its own session — harness loops and
                  interactive sessions alike. Best when draining a backlog."
  - label:       "Harness sessions only"
    description: "Interview only the <h> items from origin:noelle-harness
                  sessions. Unblocks the harness fixpoint loop; leaves
                  interactive sessions untouched."
  - label:       "Active (CURRENT) only"
    description: "Interview only items in .iteratotron/CURRENT and
                  .bug-burndown/CURRENT. Narrowest; ignores prior + harness
                  sessions."
  - label:       "Pick one session"
    description: "Show the per-session counts and drain a single session id."
```

Skip the question only when discovery is unambiguous: all items belong to
a single session, or the user already passed an explicit `scope:` /
`session:` / `skill:` argument that fully determines the set. Re-run the
collector with the narrower flag if the user picks a tighter scope.

If the chosen set still exceeds the circuit-breaker ceiling (30 items),
apply the circuit breaker: split across sessions, prioritise by the
`priority` field, defer the rest, and tell the user how many were held
back.

Emit a status line:
`Phase 1: COMPLETE — <n> items parked across <s> sessions (<i> iteratotron, <b> bug-burndown; <h> harness-spawned)`.
If `n == 0`, exit cleanly with the message "no parked items to review"
(and, if `scope:current` was the scope, suggest re-running with the
default `scope:all` in case harness-spawned items are waiting).

---

## Phase 2 — Contextualise

For each item, build a context bundle the human will read alongside the
options. The bundle has four parts; each is short, citable, and
linked back to a file in the repo.

| Part                       | Source                                        | Length |
|----------------------------|-----------------------------------------------|--------|
| Item summary               | `${session_dir}/needs_human/<item_id>/` or queue entry | ≤6 lines |
| Linked artefact excerpts   | spec FR rows / ADR Decision / threat entry    | ≤10 lines each |
| Current gap analysis row   | Phase 3 audit / triage entry for this item    | ≤4 lines |
| Recent activity on this scope | `git log -- <path>` last 5 entries         | ≤5 lines |

Push deep methodology to [references/decision-research.md](references/decision-research.md);
the goal at this phase is enough context that the human can recognise
"this is the X discussion we had last week" without re-reading the
whole thread.

**Don't skip artefact loading.** A decision made without the linked
spec / ADR / threat-entry visible is a decision made blind, which is
how parked items end up parked twice.

Emit: `Phase 2: COMPLETE — context bundled for <n> items`.

---

## Phase 3 — Research

For each item, draft 2-4 candidate resolutions. The first option is
always the **recommended** one — the one most consistent with the
current scope, in-flight work, and the linked artefact's intent.

### 3a. The four candidate slots

You won't always fill all four slots. 2 is the floor; 4 is the ceiling
the `AskUserQuestion` tool enforces. The "Other" option is added by
the tool automatically — don't include it manually.

| Slot                             | When to use it                                |
|----------------------------------|-----------------------------------------------|
| Scope-aligned design (preferred) | Always present. Most consistent with current artefacts |
| Adjacent-pattern adaptation      | Another part of the codebase solved a similar problem |
| Defer with explicit follow-up    | The item is real but premature; capture as a future story |
| Reject as won't-fix              | Item is mis-triaged or no longer relevant     |

### 3b. Consistency rules for option drafting

- Cite the artefact ID for each option: `FR-12`, `ADR-005`, `TM-AUTH-003`. Options without a citation are guesses; rewrite them.
- Don't propose options that contradict an `accepted` ADR unless the option explicitly supersedes it. Supersession is a heavy choice — flag it in the description.
- Don't propose options that would re-introduce a stop-bias pattern (stub, placeholder, deferred annotation) — those are how items end up parked in the first place.
- If the parent skill's circuit breaker fired on this item, include "Investigate why circuit breaker fired" as an explicit option.

### 3c. Optional research deepening via subagent

For an item where the options aren't obvious from the artefacts alone,
delegate to a cold-context `Agent` subagent that reads only the linked
artefacts and recent commits and returns 2-4 candidate resolutions
with citations. This keeps your context lean and reduces the chance
that prior conversation drift influences the framing.

See [references/decision-research.md](references/decision-research.md)
for the subagent prompt template.

Emit: `Phase 3: COMPLETE — options drafted for <n> items`.

---

## Phase 4 — Interview

This is where you actually talk to the human. One item per
`AskUserQuestion` call. Don't batch — bundling makes context-switching
costly and dilutes the decision quality.

### 4a. Question construction

Each question follows this shape:

```
question: "How should <item_id> (<short title>) be resolved?"
header:   "<item_id short>"   (≤12 chars)
options:
  - label:       "<Action verb, 1-5 words>"
    description: "Cites FR-12 / ADR-005 / TM-AUTH-003. Names the
                  observable change. States the trade-off."
  ... (2-4 options total, recommended first with "(Recommended)" suffix)
```

The user always gets an automatic "Other" option so they can supply
free-form text. Don't add "Other" yourself.

### 4b. What goes in `description` per option

The description field is what helps the human decide. It has to:

- Cite the artefact this option aligns with (or contradicts, if you're flagging supersession)
- State the next concrete action — what file gets edited, what status flips, what subagent gets dispatched
- Name the trade-off in one phrase ("requires SR-3 update", "delays milestone M2", "needs ADR supersession")
- Be honest about uncertainty — "if subagent re-runs cleanly, this finishes the scope; otherwise it returns to needs_human"

### 4c. The preview field

When two options diverge in something visually comparable (a code
snippet, a diff fragment, a config layout), use the `preview` field
on each option to render the comparison side-by-side. The
`AskUserQuestion` tool renders previews in a monospace box. Use this
sparingly — only when the human really benefits from seeing both
shapes at once.

### 4d. Pacing — one item at a time

Resist the urge to ask all questions in one batch. The
`AskUserQuestion` tool allows up to 4 questions per call, but each
parked item deserves its own context bundle alongside the question.
Batching collapses the context and makes it easy to miss the
trade-off in any single decision.

The exception: if two items are tightly coupled (cross-scope partners,
same `pattern_id`), present them in the same call so the human can
keep the relationship visible.

See [references/interview-patterns.md](references/interview-patterns.md)
for the full phrasing playbook with worked examples.

Emit after each interview: `<item_id>: <user_choice> — <follow-up action>`.

---

## Phase 5 — Persist

For each item the human decided on, write two artefacts and mutate the
parent's queue.

### 5a. Decision record

Write to `${session_dir}/human_decisions/<item_id>.md`:

```markdown
# Decision: <item_id>

- **Source skill:** iteratotron | bug-burndown
- **Session:** <session_id>
- **Decided:** <ISO 8601 UTC>
- **Chose:** <option label>
- **Rationale:** <user's "Other" notes if present, else the option description>

## Linked artefacts (at decision time)

- Spec: <FR-id> in <path>
- ADR:  <ADR-id> in <path>
- Threat: <TM-id> in <path>

## Next action

<exact next step: re-queue with notes / mark blocked / write follow-up story / supersede ADR>

## Options presented

1. (chosen) <label> — <description>
2. <label> — <description>
...
```

### 5b. Queue mutation

Run the queue updater:

```bash
python3 "$HOME/.claude/skills/human-review/scripts/update-queue-status.py" \
    --queue "$queue_path" \
    --item-id "$item_id" \
    --new-status "$new_status" \
    --decision-record "${session_dir}/human_decisions/${item_id}.md"
```

Status transitions per choice:

| Human choice                  | iteratotron status     | bug-burndown status   |
|-------------------------------|------------------------|-----------------------|
| Scope-aligned design          | `queued`               | `queued`              |
| Adjacent-pattern adaptation   | `queued`               | `queued`              |
| Defer with follow-up          | `blocked` + reason     | `blocked` + reason    |
| Reject as won't-fix           | `skipped_recently_complete` | `skipped`        |
| Investigate circuit breaker   | `re-evaluate`          | `re-evaluate`         |

The updater rewrites the JSONL file atomically (`write → fsync → rename`),
writes a `.bak` alongside, and appends a `human_decision` field to the
mutated entry pointing at the decision record. See
[references/queue-mutation.md](references/queue-mutation.md) for the
exact algorithm and recovery semantics.

**Harness-spawned sessions mutate identically.** The `queue_path` the
collector emits is the absolute path to that session's `queue.jsonl`
(e.g. `.bug-burndown/<harness-session-id>/queue.jsonl`), so the same
updater call unblocks a harness session — flipping `needs_human` →
`queued` / `re-evaluate` is exactly what lets the next harness round's
burndown phase re-dispatch the item and the loop reach its fixpoint.
Write the decision record under that session's own
`human_decisions/` dir (`${session_dir}/human_decisions/<item_id>.md`),
not the interactive session's, so the per-session skip-if-decided check
sees it on the next drain.

### 5c. Update `human_review_queue.md` if present

If the parent wrote a `human_review_queue.md`, strike through resolved
items and append a "Resolved" section pointing at the decision records.
Don't delete the entry — historical accountability matters.

Emit: `Phase 5: COMPLETE — <m> queue entries updated, <n - m> deferred / open`.

---

## Phase 6 — Hand back to the parent

If the parent skill that produced these items is still in-context (the
user invoked `human-review` via `/human-review` mid-pipeline), return a
short status block:

```
human-review summary
  iteratotron items resolved: <count>
  bug-burndown items resolved: <count>
  re-queued (status: queued): <count>
  newly blocked: <count>
  newly skipped: <count>
  open / Other-with-notes: <count>
```

If the parent's Stop hook now sees `queued` entries where it previously
saw `needs_human`, the next turn will re-enter the dispatcher loop
automatically. You don't need to invoke the parent — its hook does.

If the user invoked `human-review` directly (no parent in-context), tell
them how to resume:

- `iteratotron resume:<session_id>` to dispatch re-queued scopes
- `bug-burndown resume:<session_id>` to dispatch re-queued bugs

### Harness sessions — unblock the loop

When the resolved items came from harness-spawned sessions
(`origin: noelle-harness`), the unblock path is the harness's own loop,
not a manual `bug-burndown resume`. Report which harness sessions were
unblocked and tell the user to re-run the harness so its next burndown
round picks up the now-`queued` items:

```
human-review summary
  harness sessions unblocked: <count>  (<session-id> ← iter-NNN, ...)
  bug-burndown items resolved: <count>
  re-queued (status: queued): <count>
  re-evaluate: <count>
  newly blocked: <count>
  newly skipped: <count>
  open / Other-with-notes: <count>

Next: re-run the harness (cargo run -p <project>-harness ...) — its
burndown bridge will re-dispatch the re-queued items, and the global
fixpoint can now converge. Or run `bug-burndown resume:<session-id>` to
drive a single harness session's queue directly.
```

---

## Forbidden actions (hard refuse)

- **Deciding for the user.** This skill researches and presents options. The human picks. Auto-selecting an option without `AskUserQuestion` defeats the purpose.
- **Bundling more than 2 unrelated items into one AskUserQuestion call.** Each parked item deserves its own context. Coupling is the only exception.
- **Mutating the queue before the decision is recorded.** Always write the markdown decision record first, then run the updater. If the updater fails after the record exists, the record is the source of truth and replay is safe.
- **Editing the queue JSONL with `sed` or `Edit` directly.** Use the `update-queue-status.py` script — it preserves field order and writes atomically. Hand-editing breaks the schema in subtle ways.
- **Proposing options that contradict an `accepted` ADR without flagging supersession.** ADR drift is how completion-readiness collapses.
- **Skipping the linked-artefact load in Phase 2 "to save time".** A decision made blind is a worse outcome than no decision.
- **Calling `Skill` to re-enter the parent skill mid-interview.** Let the Stop hook do its job — that's the integration seam.

## Forbidden phrases (refuse unless followed by cited evidence)

- "This is the obvious choice" — say "Option N aligns with FR-12 and ADR-005, which is why it's recommended."
- "We should just defer this" — say "Deferral is option N; the follow-up story is <story-id> and the milestone target is M-X."
- "The user will know what to do" — that's why we're asking. Present options.
- "All items resolved" — say "<n> items resolved, <m> deferred, <k> open with notes" with exact counts.

## Circuit breaker

Stop and report inability when:

- The collector returns more than 30 items in one scope (one session, or the aggregate across an all-sessions drain). Resolving 30+ items in one interview is decision fatigue — split across sessions (the all-sessions default makes this common with a harness backlog), prioritise by the `priority` field, defer the rest, and tell the user how many were held back and which `session:<id>` to drain next.
- The same item has been through human review more than twice in the prior log. Something about how the item is framed isn't sticking; surface the prior decisions and ask the user whether the framing itself needs rework.
- An item's linked artefact can't be loaded (file missing, ADR ID dangling). Don't proceed without the artefact — surface the broken link as a separate finding for the relevant doc skill (`/spec-review`, `/adr-review`, `/threat-model-review`).
- The session has no `manifest.yaml` or the manifest is malformed. The parent skill's state is corrupted; don't try to mutate the queue blindly — surface and let the user investigate.

---

## Writing Style

Apply `natural-writing-style` to all decision records, status blocks,
and interview prose.

Decision records must:

- State exact item IDs, artefact IDs, and SHAs when claiming linkage
- Quote the user's own words when they pick "Other" with notes — don't paraphrase
- Name the next concrete action with the file path or queue field that will change
- Avoid claims about completeness or readiness — record what was decided, not what the consequences will be

## References

- Decision research methodology (subagent prompt, citation rules, option-drafting checklist): [references/decision-research.md](references/decision-research.md)
- Interview patterns (AskUserQuestion phrasing, preview usage, coupled-item handling): [references/interview-patterns.md](references/interview-patterns.md)
- Queue mutation protocol (JSONL atomic update, schema preservation, recovery): [references/queue-mutation.md](references/queue-mutation.md)

## Companion skills

- `iteratotron` — produces `needs_human` and `requires_human_review` scopes in `.iteratotron/<session>/scope_queue.jsonl`. Calls this skill via Skill at Phase 8b when parked items exist.
- `bug-burndown` — produces `needs_human` and `requires_human_review` bugs in `.bug-burndown/<session>/queue.jsonl`. Calls this skill via Skill at Phase 8b when parked items exist.
- `/spec-review`, `/adr-review`, `/threat-model-review` — invoked when an item's linked artefact is missing or stale; resolves the artefact before re-running this skill.
- `/all-aboard` — invoked when an item's resolution requires creating a missing spec / ADR / threat-model entry before the queue entry can re-dispatch.
