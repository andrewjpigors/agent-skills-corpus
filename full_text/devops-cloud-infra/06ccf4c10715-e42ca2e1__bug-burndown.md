---
name: bug-burndown
description: >-
  Runs a continuous, autonomous bug burndown session — collecting defects
  from logs, tests, issue queues, and spec drift; deduplicating and
  triaging via an 8-phase pipeline; then dispatching bounded parallel
  bugfix subagents in isolated worktrees until the queue's empty or the
  time budget runs out. Use when asked to "burn down the bugs", "clear
  the backlog", "triage CI failures", "find regressions", "run a fix
  session", or anything that smells like batch quality-improvement rather
  than a single targeted bug fix.
allowed-tools: >-
  Read Grep Glob Bash(git*) Bash(cargo test*) Bash(cargo nextest*)
  Bash(cargo build*) Bash(cargo clippy*) Bash(pytest*) Bash(jq*)
  Bash(rg*) Bash(glab*) Bash(gh issue*) Bash(gh pr*) Bash(curl*) Edit Write
  AskUserQuestion TaskCreate TaskUpdate TaskGet TaskList Agent Skill
hooks:
  Stop:
    - hooks:
        - type: command
          command: python3 "$HOME/.claude/skills/bug-burndown/scripts/check-completion.py"
          timeout: 60
compatibility: >-
  Hook path assumes global install at ~/.claude/skills/bug-burndown/. $HOME
  must be set and python3 must be available. Adjust the hook command path
  if you install skills elsewhere.
---

# Bug Burndown Skill

You're an autonomous quality engine. Take a large, unstructured set of
observable defects, turn them into a clean prioritised queue, and drive
each to a structural fix via the `bugfix` skill — running multiple fixes
in parallel without their work colliding.

You won't cut corners on `bugfix`'s rigor for throughput. Speed comes
from parallelism and good triage, not from weakening gates.

## When to Use This Skill

Trigger this skill whenever you hear:

- "burn down the bugs", "fix everything that's failing", "clear the backlog"
- "triage the logs", "what's broken", "run a fix session"
- "review for regressions", "find drift from the spec/ADRs/threat model"
- "fuzz triage", "CI triage", "fix all the failing tests"
- anything that's a batch quality-improvement operation, not a single targeted bug
- after a long CI run, a fuzz session, a stress test, or a milestone code review

## Quick Start

Arguments: `[source(s) and scoping flags, e.g., 'logs:./logs/*.json tests:cargo time:2h parallel:5']`

Defaults if no arguments: all six sources enabled, 2h time budget,
parallelism 5, artefacts under `.bug-burndown/<session-id>/` (top-level
dotfile directory, auto-gitignored — see Phase 1a).

**Heavy-work concurrency** is bounded by the `noelle-harness` slot
semaphore (SPEC-004 FR-HARN-001..003) when that binary is on PATH —
multiple subagents can run in parallel without OOM because each
verification command (cargo build, cargo test, pytest, etc.) goes
through `noelle-harness verify run` which acquires a tier-weighted
slot from a single host-shared pool. Without the semaphore, parallel
subagents that each kick off a workspace build will fight for RAM.
See `references/dispatcher.md` § "Slot semaphore integration".

1. Run **Phase 1** — create session dir, snapshot baseline, check clean tree
2. Run **Phase 2** — fan out to all enabled collectors; each writes `findings/<source>.jsonl`
3. Run **Phases 3–5** — classify, dedupe, prioritise → `queue.jsonl`
4. Run **Phase 6** — bounded parallel dispatch of `bugfix` subagents in isolated worktrees
5. Run **Phase 7** (continuous, alongside 6) — reconcile each finished subagent
6. Run **Phase 8** — final report, bugfix log update, resumable queue

To resume a prior session: `bug-burndown resume:<session-id>`

## Running in opencode

Runs in opencode as well as Claude Code. The Claude Stop hook that runs
`scripts/check-completion.py` is replaced by the
`.opencode/plugins/completion-loop.ts` plugin firing on `session.idle`;
the checker self-gates on `.bug-burndown/CURRENT`, so it's a no-op when no
burndown is active. Subagent dispatch (`Agent(subagent_type: "bugfix")`)
becomes the `task` tool; streamed `claude -p` subprocesses become
`opencode run`. Tool names: `AskUserQuestion` → `question`,
`TaskCreate/TaskUpdate` → `todowrite`/`todoread`. Full mapping:
[docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

## Live context (auto-injected at load)

- Branch:             !`git rev-parse --abbrev-ref HEAD`
- Repo root:          !`git rev-parse --show-toplevel`
- Worktree count:     !`git worktree list | wc -l`
- Recent commits:     !`git log --oneline -n 5`
- Prior bugfix log:   !`ls -la .bugfix/log/ 2>/dev/null | head -10 || echo "no prior log"`
- Working tree:       !`git status --short | head -3 || echo "clean"`

## The 8-phase pipeline (don't skip phases)

```json
{
  "1_setup":         "create session dir, snapshot baseline, ensure deps",
  "2_collect":       "fan out to each enabled source collector",
  "3_classify":      "tag each finding with kind, severity, signals",
  "4_dedupe":        "fingerprint + embedding match within session AND vs log",
  "5_prioritise":    "sort by severity > blast radius > dep graph > cost",
  "6_dispatch":      "bounded parallel bugfix subagents, worktree-isolated",
  "7_reconcile":     "collect results, update queue, detect regressions",
  "8_report":        "chat summary, update queue file, update bugfix log"
}
```

Emit a status line after every phase:
`PHASE <n> (<name>): COMPLETE | PARTIAL | BLOCKED — counts: <n found / n new / n queued / n fixed>`

## Autonomy contract (CRITICAL — overrides default turn-taking)

The user invoked bug-burndown because they want **autonomous, parallel,
end-to-end defect triage and fixing across the whole codebase in a single
turn**. The behaviours below are suspended for the duration of the
session — they're correct defaults for normal interactive work and
**wrong** for this skill.

This skill follows the same "Single-Turn Autonomy" framing as the
`iterate` skill, lifted to the orchestrator layer:

- **Don't pause for permission between phases.** Dispatch happens
  automatically once Phase 5 produces a queue. You don't ask "should I
  dispatch?" — that's the entire purpose of the skill. The only valid
  pauses are: (a) dirty working tree at Phase 1b, (b) borderline 0.80–0.85
  dedup pairs in Phase 4a where merging would change queue rank, (c)
  circuit-breaker conditions firing.
- **Don't surface tool-call cost or compute duration as friction.**
  Phrases like "this will take many tool calls", "expensive operation",
  or "before committing compute" are signals you've drifted out of
  autonomy mode. The user already accepted this cost when they invoked
  the skill. Cost-accounting is the user's job; you orchestrate.
- **Parallelism is fan-out by default.** Default `N=3` and the whole
  point is to run N bugs simultaneously. Dropping to `parallelism=1`
  without a cited reason from the closed list below is a defect.
- **AskUserQuestion is reserved for genuine ambiguity, not procedural
  check-ins.** Every other use is forbidden — see § Forbidden actions.
- **"The subagent will run many tool calls" is not a stopping rationale
  at this layer either.** The subagent's tool-call budget is the
  subagent's concern; the orchestrator's job is to launch it and wait.

If you're about to write "I want to check in before dispatching", that
sentence itself is the bug — delete it and dispatch.

### Deterministic completion oracle (Stop hook)

A Python Stop hook at `~/.claude/skills/bug-burndown/scripts/check-completion.py`
enforces this contract mechanically. On every Stop event it:

1. Reads `.bug-burndown/CURRENT` to find the active session.
2. Counts entries in `.bug-burndown/<session-id>/queue.jsonl` by `status`.
3. **Blocks the stop** (`{"decision": "block", "reason": "..."}`) if any
   bug is in a non-terminal status (`queued`, `in_flight`, `re-evaluate`,
   `needs_rebase`) AND the session's time budget hasn't expired.
4. **Approves the stop** only when every queue entry has reached a
   terminal status (`fixed`, `blocked`, `needs_human`, `skipped`,
   `requires_human_review`, `introduced_regression`) OR the time budget
   in `manifest.yaml` is exhausted.

Two consequences:

- **You can't end the turn while dispatchable work remains.** Drafting a
  Phase 8 summary with un-fixed bugs will fire the hook, which re-enters
  the loop with a block message reminding you to dispatch the next bug.
- **The queue is the contract.** Phase 5 writes `queue.jsonl`; Phase 7
  reconcile MUST update each entry's `status` after dispatch returns or
  the hook will block forever. That's why Phase 7a step 4 says
  "update `queue.jsonl`: `status: fixed`".

The hook is skipped in subagent context (so the bugfix subagent's own
DoD hook owns the inner loop) and when `stop_hook_active` is already
set (infinite-loop guard).

### Harness-driven sessions (env-var contract)

Bug-burndown can be invoked three ways. The autonomy contract is the
same in all three, but the Stop hook needs to know which Claude
session is *responsible* for driving a given session's queue down —
otherwise an interactive Claude Code session that happens to see a
leftover session in `.bug-burndown/CURRENT` gets blocked on work it
didn't start.

| Invocation | Who drives autonomy | `manifest.origin` | env var |
|---|---|---|---|
| Interactive Claude Code: `/bug-burndown ...` | the interactive session | unset or `interactive` | unset |
| Direct CLI: `claude --print "/bug-burndown ..."` | that subprocess | unset or `interactive` | unset |
| External harness (e.g. `noelle-harness`): spawns `claude --print "/bug-burndown resume:<id>"` to drive a session it pre-populated | the spawned subprocess | `noelle-harness` (or another `*-harness` value) | `BUG_BURNDOWN_HARNESS_DRIVEN=1` |

The Stop hook's decision matrix:

| `BUG_BURNDOWN_HARNESS_DRIVEN=1` set | `manifest.origin` contains "harness" | Hook |
|---|---|---|
| Yes | (any) | **BLOCK** — this is the spawned subprocess, enforce autonomy |
| No | Yes | **SKIP** — different Claude session looking at a leftover harness session |
| No | No | **BLOCK** — direct interactive invocation, enforce autonomy |

Contract for external harnesses:

- Set `manifest.origin: <toolname>-harness` in the session manifest
  (`.bug-burndown/<id>/manifest.yaml`) when you pre-populate it.
- Set `BUG_BURNDOWN_HARNESS_DRIVEN=1` on the env of the `claude --print`
  invocation that's supposed to drive the session.
- Optionally set `BUG_BURNDOWN_HARNESS_SESSION_ID=<session-id>` so the
  hook can cross-check.

The canonical example is `noelle-harness` (see the
`harness-builder` skill (runtime mode)). The contract is intentionally simple
so any harness in any language can implement it: one env var, one
manifest field.

## Standing rules

- **Never weaken `bugfix` gates** to fit time budgets. If a subagent
  reports `GATE 8: INSUFFICIENT`, the bug returns to the queue with a
  `LESSONS_LEARNED` entry; it doesn't get force-merged. This includes
  the mutation-testing gate: a fix with surviving mutants on its changed
  lines is not fixed — `cargo mutants --in-diff <(git diff HEAD)` (or
  `mutmut`/Stryker/go-mutesting/mull for non-Rust trees) must show zero
  survivors before reconciliation. See `bugfix/references/reproducer-and-mutation.md`.
- **Branch isolation is non-negotiable.** Every bugfix subagent runs in
  its own git worktree. Merges to the integration branch happen
  sequentially after each subagent reports done.
- **Persistence is mandatory.** Every bug goes into the JSONL queue AND
  a markdown record before any fix attempt. Interruptions and time-budget
  exhaustion must be resumable.
- **Deduplication is semantic, not just structural.** Use embeddings to
  catch "same bug, different symptom" within the session and across prior
  sessions in the bugfix log.
- **The bugfix log is read on every session start.** Recurring bugs
  surface as warnings so you can judge whether the prior fix was
  incomplete or a regression crept back in.
- **XL-cost bugs go to the human review queue.** They need design input
  before code changes. The dispatcher won't attempt them without an
  explicit user override.

## Architecture

```
                   ┌────────────────────────────┐
                   │   bug-burndown skill (you)  │
                   └──────────────┬──────────────┘
                                  │
       ┌────────┬────────┬────────┼────────┬────────┬────────┐
       ▼        ▼        ▼        ▼        ▼        ▼        ▼
   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
   │ logs │ │tests │ │ live │ │issues│ │ code │ │drift │
   │  col │ │  col │ │  col │ │  col │ │review│ │ col  │
   └───┬──┘ └───┬──┘ └───┬──┘ └───┬──┘ └───┬──┘ └───┬──┘
       └────────┴────────┴────────┴────────┴────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  triage: classify + dedupe +   │
                  │  prioritise → queue.jsonl      │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │   dispatcher (bounded N=3)     │
                  └─┬──────────────┬──────────────┬┘
                    ▼              ▼              ▼
              ┌──────────┐   ┌──────────┐   ┌──────────┐
              │worktree A│   │worktree B│   │worktree C│
              │ bugfix   │   │ bugfix   │   │ bugfix   │
              │ subagent │   │ subagent │   │ subagent │
              └────┬─────┘   └────┬─────┘   └────┬─────┘
                   └──────────────┼──────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │  reconcile: results → queue,   │
                  │  bugfix-log, branch merges     │
                  └───────────────────────────────┘
```

See `references/dispatcher.md` for worktree mechanics and the subagent
prompt template. See `references/triage-pipeline.md` for the full
classify/dedupe/prioritise internals.

---

## Phase 1 — Setup

### 1a. Session directory and identity

State lives in top-level dotfile directories (`.bug-burndown/` and `.bugfix/`)
rather than under `.claude/state/`. This keeps writes outside Claude Code's
project-state directory, avoiding per-write permission prompts during long
autonomous sessions. The skill ensures both directories are gitignored:

```bash
ensure_gitignored() {
    local entry="$1" gi=".gitignore"
    [ -f "$gi" ] || touch "$gi"
    grep -qxF "$entry" "$gi" || { echo "$entry" >> "$gi"; echo "Added '$entry' to .gitignore"; }
}
ensure_gitignored ".bug-burndown/"
ensure_gitignored ".bugfix/"

session_id="$(date +%Y%m%d-%H%M%S)-$(head -c4 /dev/urandom | xxd -p)"
session_dir=".bug-burndown/${session_id}"
mkdir -p "${session_dir}"/{worktrees,findings,reports}
echo "${session_id}" > .bug-burndown/CURRENT
```

Create three files in `${session_dir}`: `queue.jsonl` (append-only structured
queue), `report.md` (human-readable narrative), and `manifest.yaml`. The
manifest is read by the Stop hook — populate these exact keys so the
hook's time-budget check works:

```yaml
session_id: <session_id>
start_time: <ISO 8601 UTC, e.g. 2026-05-16T14:15:03Z>
time_budget_seconds: <integer, e.g. 7200 for 2h>
parallelism: <integer>
sources_enabled: [logs, tests, ...]
baseline_sha: <commit SHA>
```

### 1b. Baseline snapshot

```bash
baseline_sha="$(git rev-parse HEAD)"
integration_branch="$(git rev-parse --abbrev-ref HEAD)"
```

If the working tree's dirty, **STOP** and use AskUserQuestion: commit,
stash, or abort? Don't lose work that isn't captured yet.

### 1c. Load prior bugfix log

```bash
log_dir=".bugfix/log"
[[ -d "${log_dir}" ]] && \
    echo "Loaded $(ls "${log_dir}"/*.md 2>/dev/null | wc -l) prior bug records."
```

### 1d. Capability check

| Source              | Required                                    |
|---------------------|---------------------------------------------|
| logs                | `jq`, `rg`                                  |
| test reports        | language-specific test runner               |
| live harness        | `cargo nextest` / `pytest` / BDD runner     |
| issues              | GitLab MCP (preferred), or `glab` CLI; `gh` only for GitHub remotes |
| code review         | `rg`, repo with `references/` for skills    |
| spec drift          | ADR / spec / threat-model artefacts present |
| test-effectiveness  | `.test-effectiveness/baseline.json` from harness OR per-ecosystem mutation/CRAP/coverage tools (cargo-mutants + cargo-crap + cargo-llvm-cov; mutmut + radon + coverage.py; gremlins + cyclop; mutant + rubycritic; stryker) |

Missing capabilities → disable that source AND record in `manifest.yaml`.
Don't silently skip — you need to know what's missing from your picture.

`PHASE 1: COMPLETE` requires session dir created, baseline recorded, log
loaded, capabilities checked.

---

## Phase 2 — Collect

Each enabled collector appends raw findings to `${session_dir}/findings/<source>.jsonl`.
Collectors don't dedupe or classify — that's Phases 3–4. Their job is extraction only.

- **2a. Log collector** — walk provided paths (default `./logs/`, `./target/test-logs/`, `./test-results/`). Extract error-level events, panic banners, FATAL/ERROR/stack frames from JSON traces and plaintext logs.
- **2b. Test report collector** — parse `cargo test --message-format=json`, JUnit XML, pytest JSON. Extract every FAIL/ERROR/PANIC with test name, file, line, message, and stack.
- **2c. Live harness collector** — optionally run `cargo nextest run`, `pytest --json-report`, etc. Time-bounded by `harness_budget` in manifest (default 20 minutes).
- **2d. Issue/ticket collector** — detect upstream host from `git remote get-url origin`; for GitLab remotes (anything not `github.com`), prefer the GitLab MCP tools, fall back to `glab issue list`, then the REST API; only use `gh` when the upstream is `github.com`. Filter to issues updated within the burndown window (default 30 days). See `references/collectors.md` §2d for the detection and fallback protocol.
- **2e. Code review collector** — grep for patterns from `.bugfix/log/*.md` entries tagged `recurring-pattern`. Findings of kind `pattern-recurrence`.
- **2f. Spec/ADR/threat-model drift collector** — parse artefacts under `docs/decisions/`, `docs/specs/`, `THREATMODEL.md`; search codebase for contradictions. Most expensive collector: delegate to a subagent if the codebase is large (see `references/collectors.md`).
- **2g. Test-effectiveness collectors** (split into three sub-collectors). These run mutation testing, CRAP scoring, and coverage analysis to surface bugs the suite *cannot* catch — and to detect implementation that's hollow under its tests. Two paths: when `.test-effectiveness/baseline.json` already exists (the runtime harness (from `harness-builder`) ran first), the collectors **read it and the latest `iter-NNN/delta.json`** rather than re-scanning. When the baseline is absent, the collectors **run their own scoped scan** scoped to the session's working set. See `harness-builder/references/runtime-test-effectiveness-baseline.md` for the on-disk contract.
  - **2g.1 mutation-survivor collector** — read every entry with `kind: mutation-survivor` from the baseline/delta. When no baseline exists, run `cargo mutants --in-diff <(git diff origin/main) --json` (Rust), `mutmut run --json` (Python), `gremlins unleash --output json ./...` (Go), `bundle exec mutant run --json-dump` (Ruby), or `stryker run --reporters json` (JS/TS). Each surviving mutant becomes a `kind: test-gap` finding.
  - **2g.2 CRAP-hotspot collector** — read every entry with `kind: crap-hotspot` (CRAP > 30). Without a baseline, compute via `cargo crap --lcov lcov.info --format json` (Rust, pinned to v0.2.0; fall back to hand-computed when the install fails) or the per-ecosystem equivalents in `.claude/rules/static-analysis.md`. Each becomes a `kind: dangerous-complexity` finding.
  - **2g.3 coverage-cliff collector** — read every entry with `kind: coverage-cliff` from the baseline. These get tagged `kind: untested-mitigation` when the linked artefact is a threat-model entry, otherwise `kind: untested-branch`.

  When the harness produced a `triage-verdict.json`, **respect its
  verdicts**: findings classified as `acceptable-debt` skip this
  session's queue (they're written to
  `${session_dir}/findings/test-effectiveness-skipped.jsonl` for audit);
  findings classified as `stub-implementation` get severity-lifted to
  P0 regardless of the seed. Phase 3 ranks the rest by proximity to
  security-sensitive code and by linked-artefact status.

`PHASE 2: COMPLETE` requires every enabled collector wrote its findings file.
A zero-count result is fine. A mid-run error is BLOCKED, not COMPLETE.

---

## Phase 3 — Classify

Tag every raw finding with kind, severity, signals, blast radius, confidence,
and fix cost. See `references/triage-pipeline.md` for the full JSONL schema.

### 3a. Severity rules

- **Critical**: data loss, silent corruption, security vulnerability, panic on non-adversarial input, CI fundamentally broken.
- **High**: incorrect user-facing behaviour, panic on adversarial-but-plausible input, perf regression >2×, recurring pattern.
- **Medium**: incorrect non-user-facing behaviour, minor wrong output, spec drift not yet manifested.
- **Low**: flakiness, cosmetic, error-message-only, lint-level.

When in doubt, classify UP. It's the misclassified-as-low bugs that hurt most.

### 3a.1 Severity lift — doc-claimed-done

For every test-effectiveness finding (kind `test-gap`, `dangerous-complexity`,
`untested-mitigation`, `untested-branch`), check the `linked_status`
field carried in from the baseline/delta. When `linked_status ==
"implemented"`, lift the finding one tier — typically P1 → P0. The
documentation is making a load-bearing claim about behaviour the test
suite cannot verify; that's the most damaging single class of completion
debt.

The lift is mechanical and pre-computed by the harness wrapper when one
exists. Without a harness baseline, walk `docs/specs/*.md`,
`docs/stories/*.md`, `docs/decisions/*.md`, and `THREATMODEL.md` looking
for `Status: Implemented` / `✅ IMPLEMENTED` lines that name the file
path or symbol carrying the finding. Conservative match — when in
doubt, lift.

### 3a.2 Whole-log divergence findings — read the whole log, not the exemplar

Some findings encode a divergence that exists **only in the relationship
between many log lines across the whole run**, not in any single line. The
harness's whole-log correlation pass emits these as `silent-divergence`
verdicts whose `reason` mentions **oscillation / identity churn / "across the
run"** and carries a **state sequence** (e.g. `CVE → RHSA → CVE → RHSA`). The
canonical case: an advisory's identity migrating from a CVE to a vendor alias
and back, repeatedly, because two ingest paths disagree on the canonical id —
every individual `migrated advisory …` line is a benign INFO, so the bug is
invisible line-by-line.

For any such finding:

- **Do not** try to fix from the single exemplar `line`. It is one frame of a
  back-and-forth; the root cause is elsewhere. The finding's `reason` tells you
  to read the full log — do it.
- **Read the complete iteration log** the harness points you at (e.g.
  `<iter_dir>/harness.jsonl`) and trace **every** line for the named key
  (the CVE/advisory) to find the **competing sites** — the two (or more) code
  paths that each write a different canonical id for the same record.
- **Fix structurally and idempotently:** make the canonical-id decision
  deterministic — one path wins, or both agree — so re-ingesting the same record
  does not rewrite its identity. A patch that only suppresses the log line, or
  that fixes one direction of the bounce, is wrong.
- **Regression test:** ingest the record **twice** and assert the identity is
  **stable** across the second pass (no migration on re-ingest). A test that
  only checks a single ingest can't catch oscillation.

This generalises: any finding whose evidence is a cross-line pattern
(oscillation, monotonic-counter regression, an ordering invariant, a
request/response correlation) requires whole-log context to fix and a
multi-pass / two-run regression test to lock down. Treat "the exemplar is one
data point in a sequence" as the signal to widen your context to the full log.

### 3b. Blast radius

```bash
rg --count -t rust "<symbol_name>" | paste -sd+ | bc
```

For spec-drift findings, blast radius = count of code locations that should
comply with the drifted spec.

### 3c. Confidence and cost

- **Confidence high** — stack frame names a single function; bug class is well-known.
- **Confidence medium** — symptom's clear but multiple plausible origins.
- **Confidence low** — symptom is real but mechanism unclear; investigate during dispatch.
- **Confidence unknown** — symptom observed but no clear code path yet; collect more evidence before dispatch.

Fix cost: **S** = single file/function; **M** = single module; **L** = cross-module; **XL** = architectural → flag `requires_human_review: true`, skip dispatch.

`PHASE 3: COMPLETE` requires every finding classified.

---

## Phase 4 — Deduplicate

Two passes: within-session (collapse multiple observations of the same defect)
and across-session (recurrence detection vs. the persistent log).

### 4a. Within-session dedup

1. **Structural fingerprint**: `(error_class, top_stack_frame_file_line, normalised_message)`. Exact match → collapse, union `sources` list.
2. **Embedding similarity**: cosine >0.85 → auto-merge; 0.80–0.85 → use AskUserQuestion to confirm before merging.

A finding seen in logs AND a failing test AND an issue ticket becomes one
queue entry with `sources: [logs, tests, issues]`. That's good — it's
high-confidence triage.

### 4b. Across-session recurrence detection

Compare session findings against the embedded corpus in `.bugfix/log/*.md`.
For prior matches with similarity >0.80:

- **Same bug, was marked fixed** → tag `recurring: true`, link prior fix SHA. Surface as a **regression of a previously-fixed bug**. Bump severity to at least high.
- **Same bug, was marked blocked/won't-fix** → tag `prior_decision: <decision>`, include prior context in the subagent's prompt.
- **Similar but not identical** → annotate with `related: [BUG-XXXX]`; don't collapse.

### 4c. Pattern-recurrence elaboration

`pattern-recurrence` findings (from Phase 2e) each get their own queue entry
but share a `pattern_id`, so the subagent can apply the same structural fix
consistently across all siblings.

`PHASE 4: COMPLETE` requires fingerprint-and-embedding pass done, recurring
entries surfaced, pattern-id linkage applied. Emit: `<raw> → <deduped>` counts.

---

## Phase 5 — Prioritise

Sort with this strict total order:

1. **Severity** (critical > high > medium > low)
2. **Blast radius** (descending)
3. **Dependency graph** (root-cause bugs before their dependents)
4. **Fix cost** (ascending within tier — small fixes first to maximise queue momentum)

Build a small dependency DAG within each severity tier: `A blocks B` when fixing A
is expected to resolve B as a side effect, or B's reproducer depends on A's
codepath. Topological sort within the tier.

Write the prioritised queue to `${session_dir}/queue.jsonl`. Each record
gains `priority_rank`, `priority_reasons`, `blocks`, `blocked_by`,
`status: queued`, `attempt_count: 0`.

Emit the Phase-5 section of `report.md`: top-20 as a table, counts by
severity and source.

`PHASE 5: COMPLETE` requires queue ordered, `blocks`/`blocked_by` linked,
top-20 surfaced in the report.

---

## Phase 6 — Dispatch (bounded parallel)

See `references/dispatcher.md` for full mechanics: worktree creation, subagent
prompt template, branch naming, and result collection.

### 6a. Dispatcher invariants

- `parallelism` N from arguments or manifest (default 5). Fan-out is the default; serial dispatch is the exception. Raising N above 5 requires both an explicit `parallel:N` argument AND a slot-pool capacity of at least `2 × N` reported by `noelle-harness slot status` (SPEC-004 FR-HARN-009).
- Each bug runs in its own worktree on branch `bugfix/${session_id}/${bug_id}`.
- A bug's dispatchable when `status == queued` AND all `blocked_by` entries are `fixed` AND `requires_human_review == false`.
- Critical + low-confidence + high-blast-radius bugs go to `human_review_queue.md` instead of dispatch.

**When parallelism legitimately drops below the default**: reducing
`parallelism` below the user-provided value (or default of 5) requires a
cited reason from this closed list. "To be safe" or "to check in first"
is not on the list and is a defect:

| Reason | Trigger | New parallelism |
|---|---|---|
| Capability check at Phase 1d | `noelle-harness slot status` reports `capacity < 2 × parallelism`, OR CPU cores < parallelism | min(capacity/2, cores, requested) |
| User override | User passed `parallel:1` in arguments | as specified |
| Merge-conflict circuit breaker | Three consecutive reconcile cycles produced conflicts | 1, until human investigates |
| Slot semaphore unavailable | `noelle-harness` not on PATH AND host RAM < 16 GB | 2, with a one-line `slot semaphore unavailable — capping parallelism at 2` log line |

When you reduce parallelism, emit a one-line status:
`parallelism reduced to N — reason: <reason from table>`. Without the
line, the reduction is silently broken.

### 6b. The loop

```
WHILE queue has dispatchable bugs AND time_budget remaining:
    WHILE in_flight_count < parallelism AND dispatchable available:
        bug = pop_highest_priority_dispatchable()
        worktree = create_worktree(bug.id, baseline_sha)
        subagent = Agent(bugfix skill prompt from dispatcher.md)
        mark bug.status = in_flight, attempt_count += 1
    wait_for_any_subagent_to_finish()
    reconcile(bug, subagent_result)   # Phase 7
```

The subagent itself acquires its own verification slots via
`noelle-harness verify run` — the dispatcher does NOT pre-acquire
heavy slots, because most subagents spend most of their time on
non-verification work (reading code, editing, thinking). Fanning out
subagents while letting their verification commands serialize through
the slot semaphore gives the best throughput. See
`references/dispatcher.md` § "Slot semaphore integration".

### 6c. Time budget

When the session budget's nearly exhausted: stop accepting new dispatches,
let in-flight subagents finish gracefully, write remaining bugs to
`${session_dir}/resumable_queue.jsonl`.

`PHASE 6: PARTIAL` is the normal mid-session state. `PHASE 6: COMPLETE`
only when the queue is empty.

---

## Phase 7 — Reconcile

### 7a. Success path

If the subagent returned Definition of Done with all boxes ticked AND
`Phase 8 verdict: APPROVED`:

1. `git merge --no-ff` the worktree's branch into the integration branch. On conflict: mark bug `status: needs_rebase`, leave branch in place, continue.
2. Write `.bugfix/log/${bug.id}.md` — bug summary, fix description, structural change, invariant restored, LESSONS_LEARNED.
3. Append to `.bugfix/log/index.jsonl` (fingerprint, embedding pointer, fix SHA).
4. Update `queue.jsonl`: `status: fixed`, fix SHA, branch ref.
5. Re-evaluate dependents — any bugs with this one in `blocked_by` may now be dispatchable.
6. Remove the worktree after a clean merge.

### 7b. Blocked / insufficient path

Update queue with `status: blocked`, append LESSONS_LEARNED. Retry once if
the block was "needs more context". Otherwise → `status: needs_human`. Leave
the worktree intact for inspection; move it to `${session_dir}/needs_human/${bug_id}/`.

### 7c. Regression detection

After a successful merge, re-run tests covering this fix's blast-radius
siblings. If any fail: revert the merge, mark `status: introduced_regression`,
append the regression as a new finding with `caused_by: <bug_id>` and
escalated severity.

`PHASE 7` runs continuously alongside Phase 6.

---

## Phase 8 — Report

### 8a. Chat summary (~300–500 words)

- **Burndown stats**: `<n> bugs found, <n> deduped, <n> fixed, <n> blocked, <n> deferred, <n> recurring`
- **Top fixes** (up to 4): one-line description + fix SHA
- **Blockers**: each blocked bug with its blocker reason
- **Recurring patterns**: any prior bugs that re-surfaced, with prior fix SHA and current observation
- **Human review queue**: any bugs escalated to `requires_human_review`, with the escalation reason
- **Recommended next session**: what to investigate first on resume

### 8b. Updated `report.md`

Full queue table with final status of every bug; timeline of dispatches and
merges; LESSONS_LEARNED aggregated across all subagents; stats by
severity × outcome, source × outcome, cost × outcome.

### 8b.1. Same-class promotion check

Before writing 8c's persistent log, scan the LESSONS_LEARNED block
for any single bug class that appeared in **N ≥ 3 subagents this
session** OR appeared in **2 sessions over the last 30 days**
(check `.bugfix/log/index.jsonl` for prior fingerprints). If found,
emit a `## Promotion candidate` block naming the class, the
fingerprints, and a one-sentence recommendation. The block goes in
both the chat summary (8a) and `report.md` (8b).

Examples of promotion-worthy patterns: every subagent re-derived
that `kill(pid, 0)` EPERM means alive (because the `bugfix` skill's
adversarial-reviewer didn't list it); three subagents independently
forgot to acquire a slot before `cargo test` (because the `bugfix`
skill's §6e rule wasn't clear enough). These aren't bugs in the
target codebase — they're gaps in the parent skill that should be
fixed permanently rather than re-discovered every session.

The block recommends one of: `update bugfix skill`, `update
adversarial-reviewer reference`, `update bug-burndown skill itself`,
`update `harness-builder` skill`, OR `escalate to human-review for
skill-author decision`. Don't try to patch the parent skill from
inside the burndown session — that's a separate work item the
operator picks up.

### 8c. Persistent bugfix log update

Write `.bugfix/log/${bug.id}.md` for every `status: fixed` bug (format in
`references/dispatcher.md`). Also write entries for `blocked` and
`needs_human` bugs — these prevent blind re-attempts in future sessions.

### 8d. Resumable queue

Write `${session_dir}/resumable_queue.jsonl` for any unresolved entries.
Resume: `bug-burndown resume:<session_id>` re-runs Phases 1, 5, and 6+.

### 8e. Hand parked items to `human-review` (when present)

After 8a–8d finalise the artefacts, count bugs whose status is
`needs_human` or `requires_human_review`. If that count is greater than
zero, invoke the `human-review` skill via the `Skill` tool:

```
Skill(skill: "human-review", args: "skill:bug-burndown")
```

The child skill runs an interactive `AskUserQuestion` interview per parked
bug, draws on the linked spec / ADR / threat-model artefacts to draft
2-4 informed resolution options, records each decision, and atomically
flips the queue entries' status field. Bugs the human re-queues
transition `needs_human` → `queued` (a non-terminal status), which
triggers the Stop hook to block the stop and force the orchestrator
back into Phase 6 dispatch on the newly-actionable bugs.

**After `human-review` returns:** re-read `queue.jsonl` and recount by
status. If any entries are now `queued` or `re-evaluate`, go back to
Phase 6 — the dispatcher loop's not done. If all entries are terminal
(`fixed`, `blocked`, `skipped`, `requires_human_review` left as-is
because the human chose to defer, or `introduced_regression`), the
session ends.

Skip 8e when the user passed `no-human-review` in arguments OR when the
session was launched as `bug-burndown resume:<id>` AND the resumed queue
had zero `needs_human` entries (no parked work to clear).

`PHASE 8: COMPLETE` requires chat summary emitted, report.md finalised,
bugfix-log updated, resumable queue written if applicable, and
`human-review` either invoked or skipped per the rules above.

---

## Forbidden actions (hard refuse)

- **Pausing between phases to ask "should I dispatch?" / "should I proceed?" / "shall I continue?".** The user authorised the full pipeline by invoking bug-burndown. The only valid pauses are listed in § Autonomy contract.
- **Emitting AskUserQuestion for procedural decisions.** Valid uses: (a) dirty working tree at Phase 1b (commit / stash / abort), (b) borderline embedding-similarity at 0.80–0.85 in Phase 4a where a merge would change queue rank. Every other use is a defect.
- **Reducing `parallelism` below the user-provided value (or default 3)** for any reason not in the § 6a closed list. "To be safe" or "to check in first" are not on the list.
- **Surfacing tool-call counts, compute duration, or "expensive operation" framing.** These belong to the subagent's stop hook, not to the orchestrator's user-facing output.
- Reducing `parallelism` below 1 (fall back to direct bugfix-skill invocation for sequential work).
- Bypassing the `bugfix` skill for "obvious" fixes. Every fix goes through the gates.
- Merging a worktree without all bugfix DoD boxes ticked.
- Deleting a worktree before reconciliation completes.
- Force-pushing to the integration branch.
- Editing the bugfix-log retroactively to remove failed attempts. Failures inform future sessions.
- Increasing parallelism above 5 without explicit user override. Past 5, merge contention typically outweighs throughput gains.

## Forbidden phrases (refuse unless followed by cited evidence)

- "All bugs are fixed" — say `<n> fixed, <m> blocked, <k> deferred` with exact counts.
- "The codebase is now clean" — say `no findings from sources [list] remain` with the source list.
- "Should resolve all known issues" — say `resolves findings [BUG-IDs]` with the IDs.
- "No regressions detected" — say `regression re-tests clean for [BUG-IDs]` and name which test suites ran.

### Cost-and-control phrases (delete from drafts, then issue the next tool call)

These all signal drift into asking-permission mode. None are appropriate at the orchestrator layer:

- "before committing compute", "before I dispatch", "before invoking the subagent"
- "this will take 30–60 minutes", "many tool calls", "expensive operation"
- "how do you want me to proceed?", "shall I dispatch?", "I need to pause and check in"
- "I'll wait for your confirmation", "let me know how to proceed"
- "the subagent will run autonomously" framed as a warning rather than a fact
- "dry-run — emit the prompt only" as an alternative to dispatch (only valid when the user explicitly asked for a dry run via arguments)
- Multi-option menus (1/2/3/4/...) presenting "dispatch now" alongside "stop here" or "pick a different bug" — Phase 5 already picked the bug; Phase 6 already chose dispatch.

## Circuit breaker

Stop and report inability when:

- Two consecutive subagents return BLOCKED with non-overlapping reasons. This class of problem needs human review; the `bugfix` skill alone can't resolve it.
- Worktree creation fails three times in a row — that's a disk space or permissions problem; investigate before continuing.
- The queue grows during the session (regressions outpacing fixes) for two consecutive reconcile cycles. Stop and report; the codebase may need a different intervention.
- Merge conflicts appear on three or more consecutive reconcile operations. Independent changes may be colliding; investigate whether serial-only merging is needed before resuming parallel dispatch.

---

## Writing Style

Apply `natural-writing-style` to all session reports and chat summaries.

Report output must:
- State exact counts, not vague summaries ("28 fixed, 5 blocked" not "most bugs fixed")
- Name specific bug IDs and fix SHAs when claiming completion
- List which sources were enabled — incomplete collection must be disclosed
- Flag recurring patterns as observations with cited prior fix SHAs, not conclusions

## References

- Collector specifications (one per source): [references/collectors.md](references/collectors.md)
- Triage pipeline (classify, fingerprint, dedupe, prioritise): [references/triage-pipeline.md](references/triage-pipeline.md)
- Dispatcher mechanics (worktrees, subagent prompt, merge protocol): [references/dispatcher.md](references/dispatcher.md)
- Recurrence detection (embeddings, pattern-id linkage): [references/recurrence-detection.md](references/recurrence-detection.md)
- Bugfix log format: [references/dispatcher.md](references/dispatcher.md) (§ Bugfix log record)
- Worked example (representative 3-hour burndown session): [references/worked-example.md](references/worked-example.md)
- Test-effectiveness baseline + delta contract: `harness-builder/references/runtime-test-effectiveness-baseline.md` — the on-disk schema for `.test-effectiveness/`, the unified findings envelope, and the per-finding triage verdict shape that Phase 2g consumes

## Companion skills

- `bugfix` — the per-bug workhorse dispatched once per queue entry via `Agent`.
- `human-review` — invoked at Phase 8e when bugs are parked at `needs_human` or `requires_human_review`. Runs an interactive AskUserQuestion interview per bug, drafts informed options against the linked artefacts, records the decision, and flips parked entries back to `queued` so the Stop hook re-engages the dispatcher.
- Documentation companion skills invoked by individual bugfix subagents as needed (not by this skill directly): `/adr-create`, `/adr-review`, `/spec-create`, `/spec-review`, `/story-creator`, `/story-reviewer`, `/threat-model-create`, `/threat-model-review`.
