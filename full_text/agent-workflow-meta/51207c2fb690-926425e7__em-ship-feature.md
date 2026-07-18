---
name: em-ship-feature
description: Use when shipping a feature whose plan exists at docs/<feature-slug>/ — typically the artifact set produced by /superdev:em-feature-plan (tasks.md, engineer-*-tasks.md, engineering-standards.md, planning.md, and optionally allocations.md). Consumes the plan and ships it autonomously - one max-effort senior-engineer subagent per task in DAG-driven parallel waves, each senior delegates coding to codex → gemini → claude sonnet (run-wide quota fallback chain), per-task senior↔coder debate bounded to 2 rounds, single max-effort staff-engineer review across bugs · simplification · codebase style. If allocations.md is present (from em-feature-plan Phase 7), auto-detects it and attributes per-task ownership to named team members in commits (Co-Authored-By) and the execution-report.md Owner column; graceful fallback to slot-only if absent. Produces a live-updated docs/<feature-slug>/execution-report.md as the single deliverable. Requires /effort max and --dangerously-skip-permissions to be active, and a clean working tree. Sits alongside em-feature-plan in the em-* family — em-feature-plan plans, em-ship-feature ships. Implicit triggers - "ship this feature", "execute the plan", "EM-run this feature", "build out the tasks", "let the team ship this", "go build this end-to-end".
---

# em-ship-feature — EM-led Autonomous Feature Execution

Consume an `em-feature-plan` planning bundle and ship it. The product: **shipped code on a working branch + a single live-updated `execution-report.md`** that tells the user what shipped, what's blocked, and what the staff engineer flagged.

The skill is **EM-led**: an Engineering Manager orchestrator parses the plan, dispatches one max-effort senior-engineer subagent per task in DAG-driven parallel waves, lets each senior delegate the actual coding to whichever external CLI has quota (codex → gemini → claude sonnet, run-wide degradation), runs a senior↔coder debate per task to catch plan errors before they become code errors, and finishes with one max-effort staff-engineer review pass over the merged diff.

**Violating the letter of the rules is violating the spirit of the rules.** No exceptions, no rationalizations.

---

## When to Use / Skip

**Use** when:
- A planning bundle exists at `docs/<feature-slug>/` (produced by `em-feature-plan`).
- You want to ship the whole feature autonomously in one session — `/effort max` is active and `--dangerously-skip-permissions` is active and the working tree is clean.
- You're willing to accept best-effort delivery with a blocker report (not infinite retry). If you need true don't-stop semantics, wrap this skill in `ralph-loop`.

**Skip** when:
- No plan exists yet → run `/superdev:em-feature-plan <slug>` first.
- The plan is `team-feature-plan`'s output (different schema) — out of scope for v1.
- You want per-task interactive review → use the original `/superdev:superdev` workflow per task instead.
- Single-task fixes — use `claude-plans-codex-executes` directly.

---

## Activation

This skill is invoked in two ways:

1. **Explicit slash command:** `/superdev:em-ship-feature <feature-slug>` — the slug is the same one `em-feature-plan` produced (the directory name under `docs/`).
2. **Implicit triggers** — user messages matching: "ship this feature", "execute the plan", "EM-run this feature", "build out the tasks", "let the team ship this", "go build this end-to-end". When matched, the skill prompts for the feature-slug if not in the message.

**Pipeline composition:**

```
team-brainstorm (optional)  →  em-feature-plan  →  em-ship-feature
```

The skill assumes the `em-feature-plan` artifact set at `docs/<feature-slug>/`:

- `tasks.md` (the DAG: Foundation list + Frontier tasks with dependency edges)
- `engineer-*-tasks.md` (one or more, parsed for per-task details)
- `engineering-standards.md` (the rules floor)
- `planning.md` (architectural context)

If any are missing, Phase 0 halts with the copy-paste command to run `em-feature-plan` first.

**Optional outer wrapping:** for users who want infinite-retry on blocked tasks rather than best-effort,
```
/ralph-loop /superdev:em-ship-feature <slug> --completion-promise "all tasks shipped, all tests green"
```
The skill itself does not invoke ralph-loop; users opt in by wrapping.

---

## Hard Gates (cannot be skipped)

1. **`/effort max` active.** EM main thread + every senior subagent + the staff engineer all need claude max effort. Self-check: the skill bundles this confirmation into Phase 0's `AskUserQuestion` (question 1, "are both required flags active?"). If user answers "no", halt with the copy-paste command: `/effort max`.

2. **`--dangerously-skip-permissions` active.** Skill assumes session-level permission bypass. Same Phase 0 bundled confirmation as gate #1. If user answers "no", halt with the copy-paste invocation: re-launch Claude Code with `claude --dangerously-skip-permissions`.

3. **`em-feature-plan` output exists and is complete.** `docs/<feature-slug>/` must contain `tasks.md`, at least one `engineer-*-tasks.md`, `engineering-standards.md`, and `planning.md`. Phase 0 checks each. If any missing → halt with: "Run `/superdev:em-feature-plan <slug>` first." No silent fallback to a different planning source.

4. **Senior + Staff engineer subagents = `model: opus`.** Every per-task senior `Agent` dispatch and the single staff-engineer `Agent` dispatch explicitly set `model: opus`. Non-negotiable — under-powered planners and reviewers degrade the entire pipeline's ceiling.

5. **Foundation sequential, Frontier parallel.** Phase 1 dispatches Foundation senior subagents **one at a time** (they wire shared interfaces; parallel writes would collide). Phase 2 dispatches all DAG-ready frontier tasks **in one message** with multiple `Agent` calls. Sequential where parallel is safe = workflow failure. Parallel where conflict-prone = correctness failure.

6. **Bounded retries everywhere.** Per-task debate ≤ 2 rounds · per-task verify restart ≤ 1 · staff-engineer BLOCKER fix-up ≤ 1 per finding. **Never unbounded recovery.** After the cap, mark BLOCKED / land in report.

7. **Run-wide coder degradation, no probing.** Once a coder family hits quota, it is OUT for the rest of the run. No per-task re-probe. Run state: `coder ∈ {codex, gemini, sonnet}`, monotonic in degradation order.

8. **Phase 0 bundled confirmation is the ONLY interactive checkpoint.** No mid-run user prompts. Other "I would normally ask" moments become auto-decisions noted in the report.

9. **`docs/<feature-slug>/execution-report.md` is the single authoritative output.** Conversation-only summaries are addenda; the report file is what tells the user (and downstream tooling) what shipped.

10. **Same-family review per task.** The reviewer in Step 2 of the per-task pipeline is from the same coder family currently active (codex → `codex-reviewer`, gemini → `gemini-reviewer`, sonnet → general-purpose Agent with `model: sonnet`). Cross-family review loses the rigor lens.

11. **Working tree must be clean before Phase 0 proceeds.** `git status --porcelain` must return empty before any per-task pipeline runs. Reason: the `gemini-reviewer` agent enforces its read-only contract by post-call `git status --porcelain` + `git checkout -- .` + `git clean -fd`. If the tree has pre-existing uncommitted state when gemini-reviewer runs, the cleanup logic would destructively wipe it. Phase 0 verifies this before the first dispatch. If unclean → halt with: "Commit or stash uncommitted changes first, then re-run." This gate is mandatory even when the run is expected to stay on codex (the run might degrade to gemini mid-flight).

12. **EM is the only dispatcher. Subagents must NEVER be told to dispatch other subagents.** This runtime exposes the `Agent` tool only to the main thread; general-purpose subagents have `TaskCreate`/`Update` but not `Agent`. The per-task pipeline's Step 2 (reviewer dispatch) and Step 4 (coder dispatch) are EM-initiated, NOT senior-initiated. Steps 3 (debate), 5 (verify), and 6 (commit) are EM-inline (no dispatch). Telling a senior subagent to "now dispatch the reviewer" or "now dispatch the coder" will fail with no Agent tool available. This gate is what makes the per-task pipeline actually work in this runtime — and what differentiates this redesign from the original spec (which assumed senior subagents could dispatch internally). Sibling skill `em-feature-plan` has the same constraint codified as its own Hard Gate #10.

**Spirit:** violating the letter of these rules is violating the spirit of the rules. No exceptions, no rationalizations.

---

## Workflow

5 phases — 1 interactive Phase 0 (bundled approval), then 4 autonomous phases.

| # | Phase | Owner | What happens |
|---|---|---|---|
| 0 | **Bootstrap** | EM (main thread, talks to user) | Hard-gate checks (incl. working-tree-clean) · parse artifacts · build task DAG · bundled `AskUserQuestion` (gate confirmation + git strategy) · initialize `execution-report.md` |
| 1 | **Foundation sweep** | EM dispatches senior subagents **sequentially** | Process Foundation Sprint tasks one at a time (shared-interface conflict rule from `em-feature-plan`) |
| 2 | **Frontier fan-out** | EM dispatches senior subagents **in parallel waves** (DAG-driven) | Topological dispatch: every task whose deps are met fans out in one message; re-batch as waves clear |
| 3 | **Staff review** | 1 staff-engineer subagent (`model: opus`) | Reviews ALL shipped code across 3 lenses: bugs · simplification · codebase style. BLOCKER findings → 1 fix-up pass; MAJOR/MINOR → land in report |
| 4 | **Finalize** | EM (main thread) | Update `execution-report.md` with staff findings + summary, commit per chosen git strategy, print final status |

---

## Phase 0 — Bootstrap (the only interactive phase)

### Step 0.1 — File-existence + working-tree hard gates

Check each file exists. If any missing, halt with the copy-paste fix:

```
docs/<slug>/tasks.md
docs/<slug>/engineer-*-tasks.md   (at least one match)
docs/<slug>/engineering-standards.md
docs/<slug>/planning.md
```

Use `Bash("test -f docs/<slug>/<file>")` for each. If any fail:

```
Cannot find docs/<slug>/<missing-file>. Run this first:

  /superdev:em-feature-plan <slug>

Then re-run /superdev:em-ship-feature <slug>.
```

Then verify the working tree is clean (Hard Gate #11):

```bash
git status --porcelain
```

If output is non-empty:

```
Working tree is not clean. Commit or stash uncommitted changes first:

  git status            # see what's uncommitted
  git stash             # OR commit explicitly
  /superdev:em-ship-feature <slug>   # re-run after clean

Reason: gemini-reviewer's read-only enforcement may destructively
revert any pre-existing uncommitted state if the run degrades to
gemini mid-flight. Hard Gate #11.
```

Then verify HEAD is on a named branch (detached HEAD breaks `git symbolic-ref --short HEAD` downstream — it returns empty, which silently corrupts `working_branch` and `gh pr create --base`):

```bash
git symbolic-ref --short HEAD >/dev/null 2>&1
```

If exit code is non-zero (detached HEAD):

```
HEAD is detached. The skill needs a named branch for the per-task
dispatch and for any auto-PR. Check out (or create) a branch first:

  git checkout -b <some-name>
  /superdev:em-ship-feature <slug>
```

Then capture `base_sha` (used by Phase 3's diff range and Phase 4.1's file count):

```bash
base_sha=$(git rev-parse HEAD)
```

Store `base_sha` for use in Phase 3 and Phase 4. This is the commit that everything shipped during the run is measured against.

### Step 0.2 — Parse artifacts in parallel

Issue ALL of the following as parallel `Read` calls in ONE message:

```
Read(docs/<slug>/tasks.md)
Read(docs/<slug>/engineer-1-tasks.md)
Read(docs/<slug>/engineer-2-tasks.md)   [if exists]
Read(docs/<slug>/engineer-N-tasks.md)   [for each engineer packet]
Read(docs/<slug>/engineering-standards.md)
Read(docs/<slug>/planning.md)
Read(docs/<slug>/allocations.md)        [OPTIONAL — produced by em-feature-plan Phase 7 if a team roster was provided; absence is not an error]
```

If `allocations.md` doesn't exist, skip it silently — em-ship-feature degrades gracefully to slot-only attribution (current pre-allocation behavior). If `allocations.md` exists but is malformed (no "Slot → Engineer mapping" section parseable), log a warning in the report's Notes section and proceed slot-only.

### Step 0.3 — Build the task graph (and optional engineer attribution)

Parse `tasks.md`:

- **Foundation list** — under the "Foundation Sprint" header. Ordered sequential list.
- **Frontier DAG** — under the "Parallel Frontiers" header. Each task has `dependencies: [<task-id list>]`. Build the adjacency map.

Parse each `engineer-*-tasks.md`:

- Per task: id, title, acceptance criteria, TDD red list, interfaces owned/consumed, files to touch.
- **Build `task_to_slot` map** (e.g., `{"F-1": "engineer-1", "T-3": "engineer-2", ...}`) from which packet file each task appeared in. Cross-reference with the DAG: every task in the engineer packets should appear in `tasks.md`.

If `allocations.md` was loaded in Step 0.2, parse the "Slot → Engineer mapping" table:

- **Build `slot_to_engineer` map** (e.g., `{"engineer-1": {name: "Alice", level: "Senior", capacity: 1.0, skills: [...], skill_match: "Strong"}, ...}`).
- **Build `task_to_engineer` map** by composing `task_to_slot` ∘ `slot_to_engineer` (e.g., `{"F-1": {name: "Alice", ...}, ...}`).
- **Capture risk callouts** from the "Risk callouts" section verbatim into `allocation_risks` (list of strings).
- **Capture unallocated capacity** from "Unallocated capacity" section into `unallocated_summary`.

If `allocations.md` was NOT loaded, set `slot_to_engineer`, `task_to_engineer`, `allocation_risks`, `unallocated_summary` to null. Downstream phases check for null before injecting engineer context.

### Step 0.4 — Print run summary

```
Feature: <name from README.md or planning.md>
Slug: <slug>
Tasks: <N> foundation + <M> frontier = <N+M> total
Max parallel frontier width: <max-out-degree of DAG>
Coder default: codex  (fallback chain: gemini → sonnet)
Working branch: <result of `git symbolic-ref --short HEAD`>
Allocation: <"loaded — <count> engineers, <count> tasks attributed" | "skipped (no allocations.md present)" | "skipped (malformed allocations.md — see report Notes)">
<If allocation loaded AND allocation_risks is non-empty: "⚠️ <count> allocation risk(s) flagged in allocations.md — surfaced in report Notes. Will not block the run (Hard Gate #8).">
```

### Step 0.5 — Bundled `AskUserQuestion` (THE only interactive checkpoint)

```
AskUserQuestion(questions: [
  {
    question: "Confirm both required flags are active before this run goes autonomous (the skill cannot detect them programmatically).",
    header: "Flags active?",
    multiSelect: false,
    options: [
      { label: "Yes, both /effort max and --dangerously-skip-permissions are active", description: "Proceed to git-strategy question." },
      { label: "No — halt and let me enable them first", description: "Halt the skill. Copy-paste fix: /effort max ; relaunch Claude Code with --dangerously-skip-permissions." }
    ]
  },
  {
    question: "Git strategy for this run?",
    header: "Git strategy",
    multiSelect: false,
    options: [
      { label: "Atomic commits per task on current branch (Recommended)", description: "One commit per shipped task on the current branch; one final commit for the report. You push and create the PR yourself." },
      { label: "Atomic commits per task on new branch feature/<slug>", description: "Same as recommended but on a fresh branch named feature/<slug>. Doesn't pollute current branch." },
      { label: "Single squash commit at end on current branch", description: "Accumulate all changes on branch, squash into one commit at end with the report as the body. Clean history, but lose per-task attribution and bisectability." },
      { label: "Atomic commits + auto-push + auto-PR at end", description: "Like recommended, plus push the branch and open a PR at end with the execution report as the body. Warning: external visibility — PR appears immediately to your teammates. Only pick if you authorize PR creation in advance." }
    ]
  }
])
```

If question 1 answer is "No, halt", stop immediately with the copy-paste fix.

If question 2 answer is "auto-push + auto-PR", verify `gh` CLI is installed (`Bash("gh --version")`); if not, halt with `brew install gh && gh auth login`. Also record the base branch (typically `main`) for later `gh pr create --base <base>`.

Store the git-strategy answer for use in Step 6 of the per-task pipeline and in Phase 4.

### Step 0.5b — Create the working branch (only if strategy requires it)

If git_strategy is "Atomic commits per task on new branch feature/<slug>" OR "Atomic commits + auto-push + auto-PR at end":

```bash
# Record the base branch first (used by gh pr create later)
base_branch=$(git symbolic-ref --short HEAD)

# Detect existing branch before checkout -b (re-runs of the skill with the same slug otherwise fail silently
# and the next `git symbolic-ref --short HEAD` returns the original branch — commits then land on the wrong branch).
if git show-ref --verify --quiet "refs/heads/feature/<slug>"; then
  HALT: "Branch feature/<slug> already exists (likely from a prior partial run). Either:
    git branch -D feature/<slug>           # delete it
    git checkout feature/<slug>            # OR resume on it (pick git strategy 'current branch' on re-run)
  Then re-run /superdev:em-ship-feature <slug>."
fi
git checkout -b feature/<slug>
```

If git_strategy is "Atomic commits per task on current branch" OR "Single squash commit at end on current branch": no branch change, working_branch = current branch.

After this step, capture the **final** working_branch:

```bash
working_branch=$(git symbolic-ref --short HEAD)
```

This value is passed to every senior subagent dispatch (line 2 of every senior prompt).

### Step 0.6 — Initialize the report skeleton

Use `Write` on `docs/<slug>/execution-report.md`:

```markdown
# Execution Report — <feature-name>

**Feature slug:** <slug>
**Started:** <ISO timestamp from `date -u +%Y-%m-%dT%H:%M:%SZ`>
**Finished:** —
**Status:** RUNNING
**Coder trajectory:** codex
**Git strategy:** <chosen-strategy>
**Allocation:** <"loaded from allocations.md (<N> engineers)" | "skipped (no allocations.md)" | "skipped (malformed allocations.md)">
**Final commit:** —

## Run summary
Tasks: <N+M> total · 0 shipped · 0 blocked · 0 files changed · 0 tests added

## Tasks
| ID | Title | Owner | Status | Coder | Files | Tests | Notes |
|----|-------|-------|--------|-------|-------|-------|-------|
| F-1 | <title> | <engineer name from task_to_engineer if loaded, else "(engineer-N)" slot label> | PENDING | — | — | — | — |
| F-2 | <title> | <owner> | PENDING | — | — | — | — |
| T-1 | <title> | <owner> | PENDING | — | — | — | — |
| T-N | <title> | <owner> | PENDING | — | — | — | — |

## Staff-engineer review findings
### Blockers
(none yet)

### Major
(none yet)

### Minor
(none yet)

## Per-task blockers (with reproducer + suggested next step)
(none yet)

## Open questions / Notes

<If allocation_risks is non-empty, render this section verbatim at the START of the Notes section so reviewers see it immediately:>

### Allocation risks flagged by em-feature-plan Phase 7
<for each risk in allocation_risks: render as a bullet>
- <risk text verbatim>

(These risks are surfaced for visibility. Per Hard Gate #8, the skill does NOT pause for user input on them; if the run completes despite them, address in a follow-up. If they caused task failures, the per-task BLOCKED reason will reference the relevant risk.)

<If unallocated_summary present and non-empty:>

### Unallocated team capacity
<unallocated_summary verbatim>

<If neither, just write:>

(none yet)
```

Populate the task table with every task ID and title from the parsed artifacts. Fill the Owner column from `task_to_engineer` if allocation was loaded; otherwise use the slot label (e.g., "(engineer-1)") as a fallback. All status PENDING.

### Step 0.7 — Print transition message

Tell the user:

```
Going autonomous from here. No more interactive checkpoints until completion or fatal error.
Watch docs/<slug>/execution-report.md for live status.
```

Then proceed to Phase 1.

---

## Phase 1 — Foundation sweep (sequential)

Foundation Sprint tasks share interfaces (ports, DI wiring, error model, test harness, CI scaffolding). Parallel writers would collide. **Dispatch one at a time.**

### Loop

For each Foundation task in the order they appear in `tasks.md`:

1. Run the **Per-Task Pipeline** (see that section below).
2. On the senior subagent's return, update the task's row in `execution-report.md`:
   - **Always `Read` the report file FIRST** to get its current state — the report has been mutated by prior task updates, never edit blind.
   - Then use `Edit` to flip the task's row from PENDING to SHIPPED or BLOCKED, fill in **Owner** (from the per-task result's OWNER field, set at dispatch time), coder/files/tests/notes.
   - If the senior's NOTES indicates a coder trajectory transition (e.g. degraded from codex to gemini), also `Edit` the report header's `Coder trajectory:` field to record it (e.g. `codex → gemini at F-3`).
3. If status is SHIPPED, the commit (made by the senior in Step 6 of the per-task pipeline) is already on the branch.
4. If status is BLOCKED:
   - **Foundation BLOCKED is high-impact** — most Frontier tasks transitively depend on Foundation. Continue with subsequent Foundation tasks (their dependencies may be different), but accept that many Frontier tasks will end up BLOCKED.
   - Do not abort the run.
5. If the `Agent` tool itself errored (not a structured BLOCKED block — actual tool error / timeout / dispatch failure): mark the task BLOCKED with the error message as the reason, do not abort.
6. Move to the next Foundation task.

After all Foundation tasks complete (SHIPPED or BLOCKED), proceed to Phase 2.

---

## Phase 2 — Frontier fan-out (parallel waves, DAG-driven)

### Wave-dispatch loop

Each task's full per-task pipeline (Steps 1-6) runs sequentially WITHIN the task, but **the planning step (Step 1) is batched across all in-flight tasks in the wave** so the senior subagents work in parallel. Steps 2-6 process each task sequentially after its plan returns.

1. Compute the **ready set**: every Frontier task whose `dependencies:` list is now fully SHIPPED.
2. Subtract tasks already SHIPPED or BLOCKED from previous waves.
3. If the ready set is empty:
   - Check for **transitively blocked** tasks — any task whose dependency is BLOCKED. Mark those BLOCKED with reason `dependency blocked: <upstream-task-id>` and update their rows in the report.
   - If after that the ready set is still empty, exit Phase 2 → proceed to Phase 3.
4. **Batch Step 1 across the wave:** dispatch ALL ready tasks' Senior-plan subagents in ONE message with multiple `Agent` calls (one per task). This is the parallel-fan-out hard requirement (Hard Gate #5).
5. Wait for all Step 1 dispatches in the batch to return.
6. **For each returned task, run Steps 2-6 sequentially** through the per-task pipeline:
   - Dispatch the reviewer (Step 2)
   - Inline debate (Step 3), possibly with another reviewer dispatch for round 2
   - Dispatch the coder (Step 4), with run-wide quota-degradation if `QUOTA_EXCEEDED:` is returned
   - Inline verify (Step 5), with possibly one reviewer + coder restart on material fail
   - Inline commit (Step 6) if SHIPPED
   - Aggregate per-task result; **`Read` the report first, then `Edit`** the row (never edit blind).
   - If the senior's debate or the coder's NOTES indicates a coder-trajectory transition, also `Edit` the report header's `Coder trajectory:` field.
7. On `Agent`-tool dispatch errors (the tool itself errored, not a structured return): mark the task BLOCKED with the error as reason, do not abort the wave.
8. Go to step 1 (compute next ready set).

### Wave dispatch example

If after Foundation completes, tasks T-1, T-2, T-3 all have only Foundation dependencies (all met), the EM batches Step 1 in ONE message:

```
Agent(description: "Senior plan — T-1", subagent_type: "general-purpose", model: "opus", prompt: <Step 1 plan prompt for T-1>)
Agent(description: "Senior plan — T-2", subagent_type: "general-purpose", model: "opus", prompt: <Step 1 plan prompt for T-2>)
Agent(description: "Senior plan — T-3", subagent_type: "general-purpose", model: "opus", prompt: <Step 1 plan prompt for T-3>)
```

All three plan in parallel. Once all three plans return, the EM processes T-1's Steps 2-6 sequentially, then T-2's, then T-3's. Within each task's Steps 2-6, the EM dispatches the reviewer (Step 2), runs Step 3 inline, dispatches the coder (Step 4), runs Steps 5-6 inline.

**Advanced (optional) parallelism:** an implementation may also batch Step 2 reviewer dispatches across tasks at the same pipeline stage (e.g., once all wave tasks finish Step 1, dispatch all their Step 2 reviewers in one message). This requires per-task state tracking and careful interleaving — skip if the simpler "Step 1 batched, Steps 2-6 sequential" pattern works fast enough.

### Quota detection during the wave

If a returned coder subagent indicates quota exhaustion (e.g., `QUOTA_EXCEEDED:` prefix), the EM flips the run state to the next coder family for **all subsequent dispatches** (Hard Gate #7: run-wide degradation, no probing). Tasks already past Step 4 in the current wave keep their current-coder result; the next task's Step 2 (reviewer dispatch) uses the new coder family per Hard Gate #10.

Update the `Coder trajectory` field in the report's header (e.g., `codex → gemini at T-3`).

---

## Per-Task Pipeline (Steps 1-6, dispatched by the EM main thread)

This is the heart of the skill. The EM (main thread) coordinates 3 subagent dispatches per task in sequence and runs the connective tissue (debate, verify, commit) inline using Bash + Edit. Mirrors `claude-plans-codex-executes` step-for-step in spirit, restructured to honor the runtime constraint that **subagents cannot dispatch other subagents** (only the main thread has the `Agent` tool).

| Step | Owner | What | Mechanism |
|---|---|---|---|
| 1. Plan | Senior (claude max) subagent | Per-task plan: files · permissions · subtasks · key decisions citing engineering-standards.md · TDD red list | Agent dispatch (returns plan markdown) |
| 2. Review | Coder-family reviewer subagent | AGREE / CONCERN / QUESTION / SUMMARY critique of the plan | Agent dispatch (returns critique verbatim) |
| 3. Debate | EM (main thread, inline) | Reads critique, decides updates, produces updated plan. ≤ 2 rounds. Round 2 unresolved → EM makes final call, notes in report. | No dispatch — EM is claude max via /effort max (Hard Gate #1), competent to debate |
| 4. Execute | Coder subagent | Write the code | Agent dispatch (returns stdout + git diff stat) |
| 5. Verify | EM (main thread, inline) | Bash check commands · grep coder stdout for silent denials · trivial fix inline · material fail → 1 restart from Step 2 · second fail → BLOCKED | No dispatch — running shell commands needs no model |
| 6. Commit | EM (main thread, inline) | Bash: git add + git commit with Co-Authored-By trailer for the coder family used | No dispatch — git is just shell |

**3 subagent dispatches per task in the happy path** (Senior-plan + Reviewer + Coder). +1 reviewer dispatch per extra debate round (max 1 extra). +2 dispatches per verify restart (Reviewer + Coder, max 1 restart). Worst case per task: 6 subagent dispatches.

**Why EM-inline for Steps 3, 5, 6:** the runtime does not expose the `Agent` tool to general-purpose subagents — only the main thread can dispatch other subagents. Steps 3 / 5 / 6 don't need delegation: debate is reasoning the EM can do directly (the EM is also claude max via Hard Gate #1); verify is shell commands + grep; commit is git. Moving them to the EM is the minimal change that respects the constraint while preserving the per-task debate and the per-task coder fallback chain.

### Step 1 — Plan (Senior subagent dispatch by EM)

```
Agent(
  description: "Senior plan — <task-id>",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
working_branch: <captured at Phase 0 Step 0.5b>
feature_slug: <slug>
coder_family: <codex | gemini | sonnet>   # current run state; informs sandbox / permissions decisions in the plan
assigned_engineer: <if task_to_engineer loaded: "<name> (<level>, capacity <X>, skills: <list>, skill_match: <Strong|Partial|Weak>)" — omit this line entirely if no allocations.md was loaded>

You are the SENIOR ENGINEER for task <task-id>. Your sole job in this dispatch is to PRODUCE A PLAN. You do NOT execute, review, or commit — those are downstream steps owned by the EM main thread or other subagents.

<If assigned_engineer is set, include this paragraph; otherwise omit:>
This task is assigned to <name> per docs/<slug>/allocations.md. They are a <level> engineer with <skills>. Their skill match for this task is <skill_match>. Use this context to calibrate plan detail — for example, if Strong match assume domain knowledge and keep the plan concise; if Partial or Weak, include more explicit context in subtasks and Key decisions for the implementer. Do not change the plan's substance based on the engineer — the PLAN is the same; the SHAPE of the plan adapts to their context.

TASK SPEC (from docs/<slug>/engineer-N-tasks.md):
<paste the full task block: id, title, acceptance criteria, TDD red list, interfaces owned/consumed, files to touch>

ENGINEERING STANDARDS (rules floor — non-negotiable):
<paste docs/<slug>/engineering-standards.md verbatim>

PLANNING CONTEXT (excerpt relevant to this task's area):
<paste the relevant section of docs/<slug>/planning.md>

Produce a plan in this exact format and return it as your final output:

## Plan
### Files to create / modify
- <abs path>: <one-line reason>
### Permissions (codex-exec knobs, ignored when coder is gemini or sonnet)
- Sandbox: <read-only | workspace-write | danger-full-access>
- Extra writable roots (--add-dir): <paths, or "none">
- Granular sandbox permissions: <list, or "none">
- Override: <include OVERRIDE: danger-full-access? default "no">
### Subtasks (each ≤30 min)
- [ ] 1. <subtask>
### Key decisions
- <choice> | Why: <reason citing engineering-standards.md>
### TDD red list (from task spec)
- <test name>: <what it asserts>

That's it. Return ONLY the plan. Do NOT dispatch reviewers or coders (you can't — only the EM can). Do NOT commit (the EM does that). Do NOT write any code in this dispatch (the coder does that in Step 4).
"""
)
```

### Step 2 — Review (Reviewer subagent dispatch by EM)

The EM dispatches the same-family reviewer (Hard Gate #10) with the plan from Step 1:

```
# If current coder is codex:
Agent(
  description: "Codex review — <task-id>",
  subagent_type: "codex-reviewer",
  prompt: "repo: <path>\n\n<plan from Step 1>"
)

# If current coder is gemini:
Agent(
  description: "Gemini review — <task-id>",
  subagent_type: "gemini-reviewer",
  prompt: "repo: <path>\n\n<plan from Step 1>"
)

# If current coder is sonnet:
Agent(
  description: "Sonnet review — <task-id>",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: """
ROLE: You are the senior engineer reviewing this implementation plan. Be specific — cite file paths. Find real problems, not nits.

For each issue, output exactly one of:
  AGREE: <one-line>
  CONCERN: <issue> | <suggested change>
  QUESTION: <ambiguity>

End with: SUMMARY: <N concerns, M questions>

---
<plan from Step 1>
"""
)
```

The reviewer returns its critique verbatim. The EM captures it for Step 3.

### Step 3 — Debate (EM main thread, inline)

The EM reads every `CONCERN:` and `QUESTION:` line from the reviewer's output and produces an updated plan:

- If the reviewer is right → update the plan accordingly (edit the markdown the EM holds in working memory).
- If the reviewer is wrong → write a counter-argument in the EM's internal notes (don't update the plan).

**Round 2:** if concerns remain after round 1, **re-dispatch the SAME reviewer** (Step 2) with the updated plan + the EM's round-1 responses appended:

```
<updated plan>

MY RESPONSES TO ROUND 1:
- Concern: <quote> → My response: <counter-argument>
- ...
```

After round 2 with unresolved concerns → **the EM makes the final call** (accept the plan as-is, proceed to Step 4), and notes the unresolved concerns in the per-task NOTES field that will land in the report.

**Hard cap: 2 reviewer dispatches per task in the debate phase** (Hard Gate #6).

### Step 4 — Execute (Coder subagent dispatch by EM)

The EM dispatches the current coder family with the finalized plan:

```
# If coder is codex:
Agent(
  description: "Codex execute — <task-id>",
  subagent_type: "codex-executor",
  prompt: "repo: <path>\n\nFINALIZED PLAN:\n<plan>"
)

# If coder is gemini:
Agent(
  description: "Gemini execute — <task-id>",
  subagent_type: "gemini-executor",
  prompt: "repo: <path>\n\nFINALIZED PLAN:\n<plan>"
)

# If coder is sonnet:
Agent(
  description: "Sonnet execute — <task-id>",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: """
ROLE: You are the senior engineer implementing this plan in the repository at <path>. Use the Read/Edit/Write tools to make the changes. Follow the plan precisely. Run any tests called out in the TDD red list and include pass/fail in your output.

For each file you change, output: CHANGED: <path> — <summary>
End with: SUMMARY: <N files changed>

---
<plan>
"""
)
```

The coder returns stdout (+ for codex/gemini-executor: `git status --short` and `git diff --stat HEAD`).

**On `QUOTA_EXCEEDED:` prefix in the coder's return:** the EM flips the run state for the rest of the run to the next coder family (Hard Gate #7). Then **RESTART from Step 2** with the new coder's reviewer (same-family rule — Hard Gate #10 — the new family deserves to critique the plan with its own rigor lens before executing). Note the trajectory transition in the per-task NOTES.

### Step 5 — Verify (EM main thread, inline)

The EM runs:

```bash
# Sanity check that changes happened
git status --short
git diff --stat HEAD

# Project check commands (read from engineering-standards.md or CLAUDE.md). Examples:
#   Rust:   cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test
#   Node:   pnpm install && pnpm typecheck && pnpm test
#   Python: ruff check . && pytest
<check command(s)>
```

Then grep the coder's stdout (captured in Step 4) for silent-denial patterns:

- **Codex/Gemini OS-level:** `sandbox.*denied`, `Permission denied`, `Operation not permitted`, `EACCES`, `EPERM`, `Network is unreachable`, `ENETUNREACH`, `Connection refused`, `ECONNREFUSED`, `getaddrinfo`, `Name or service not known`, `MCP.*error`, `mcp_server.*denied`
- **Gemini-specific:** `QUOTA_EXCEEDED:` and `AUTH_FAILED:` prefixes (the gemini-executor / gemini-reviewer wrappers prepend these)
- **Sonnet:** no stdout to grep — failures surface as `is_error: true` from the Agent dispatch in Step 4 itself, treat as a silent denial (restart or BLOCK per the rules below)

**Outcomes:**

- Checks pass with no silent denials → status SHIPPED, proceed to Step 6.
- Checks fail on something trivial (formatting, an obvious typo) → EM fixes inline via Edit, re-runs the check command, proceeds.
- Checks fail materially → **ONE restart from Step 2** (re-dispatch reviewer + coder with the failure output appended as a new concern). If second verify also fails → status BLOCKED, do NOT commit, advance to the EM's task-result aggregation.

### Step 6 — Commit (EM main thread, inline)

Only if status SHIPPED. The EM runs:

```bash
git add <files changed by coder>   # parsed from the CHANGED: lines in Step 4's return, OR `git diff --name-only`
git commit -m "<conventional-commit type>(<scope>): <one-line summary of task>

<2-3 line body if task spec warrants — typically just one line>

<If task_to_engineer is loaded for this task ID, prepend this trailer:>
Co-Authored-By: <engineer-name> <<engineer-email>>
Co-Authored-By: <coder trailer>
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
"
```

**Coder trailers:**
- codex → `codex-cli (gpt-5.5) <noreply@openai.com>`
- gemini → `gemini-cli (default) <noreply@google.com>`
- sonnet → `Claude Sonnet 4.6 <noreply@anthropic.com>`

**Engineer trailer (only when allocations.md was loaded):** synthesized from the assigned engineer's name. The em-feature-plan roster schema doesn't capture emails, so synthesize a placeholder: `<lowercase-ascii-name>@team.local`. Example: `Co-Authored-By: Alice <alice@team.local>`. For names with spaces (e.g. "Alice Smith"), use `alice-smith@team.local`. Git requires syntactically-valid emails in trailers; `@team.local` is a reserved-style placeholder that's syntactically valid and obviously fake. Users who want GitHub-linkable attribution can post-edit the commit (or extend the em-feature-plan roster schema with an `email` field in a future amendment). The engineer trailer is the **first** Co-Authored-By so the human attribution leads.

If `git_strategy == "single squash commit at end on current branch"`: do NOT commit; instead, leave the files staged with `git add` and let Phase 4 do the squash. Engineer attribution in the squash commit is best-effort — list all unique engineers across all squashed tasks as Co-Authored-By trailers (deduplicated by name).

### Per-task result (EM-internal structure, used to update the report)

After Steps 1-6 complete for a task, the EM aggregates all the dispatch outputs + its own inline-step decisions into this structure (then `Edit`s the corresponding row in `execution-report.md`):

```
TASK: <task-id>
STATUS: SHIPPED | BLOCKED
OWNER: <engineer name if task_to_engineer loaded, else slot label like "engineer-1">
CODER: <codex | gemini | sonnet>
FILES: <count> changed (<comma-separated list>)
TESTS: <pass | fail (N failing)>
DEBATE_ROUNDS: <0 | 1 | 2>   # how many reviewer dispatches ran in Step 2
VERIFY_RESTARTS: <0 | 1>
NOTES: <unresolved CONCERNs after round 2, coder trajectory changes, EM's debate notes>
BLOCKER: <reason, if BLOCKED — empty otherwise>
COMMIT_SHA: <sha from `git rev-parse HEAD` after Step 6, if SHIPPED — empty otherwise>
```

---

## Fallback Chain Semantics

Run state: `coder ∈ {codex, gemini, sonnet}`, monotonic in degradation order. Initial: `codex`.

### Detection patterns

| Coder | Detection (in subagent return) | Action |
|---|---|---|
| codex | stdout contains `You've hit your usage limit` or `Upgrade to Pro` (the codex-executor wrapper prepends `QUOTA_EXCEEDED:` for clean detection) | Flip run state to `gemini` |
| gemini | stdout/stderr contains any of: `quota`, `rate limit`, `quota exceeded`, `RESOURCE_EXHAUSTED`, `429`, `daily limit`, `usage limit` (the gemini-executor wrapper prepends `QUOTA_EXCEEDED:`) | Flip run state to `sonnet` |
| sonnet | Agent dispatch returns `is_error: true` with a rate-limit message | NO further fallback. Mark the task BLOCKED with reason `sonnet quota exhausted`, continue with subsequent tasks (they'll also be sonnet and may also fail; that's expected best-effort behavior) |

### Run-wide degradation, not per-task probing

- Once a coder family hits quota in task X, the **run state** flips. **All remaining tasks** use the new coder. No per-task re-probe.
- Quota windows reset on hour/day boundaries; re-probing wastes API calls. Users who hit quota mid-run can re-invoke the skill in a new session to re-probe from codex.

### Mid-task fallback restart

If the coder hits quota during Step 4 of the per-task pipeline (i.e. mid-execution of task X), the senior:

1. Flips its local notion of the coder to the next family.
2. RESTARTS from Step 2 (review) — because the new family's reviewer has a different rigor lens, the plan deserves a fresh debate cycle.
3. The new debate gets ≤ 2 fresh rounds (the round counter resets — the rigor lens has changed).
4. NOTES the trajectory transition in its return block.

### Coder trajectory in the report

The report's header field `Coder trajectory:` records the path. Examples:
- `codex` (no degradation)
- `codex → gemini at T-3` (degraded once at task T-3)
- `codex → gemini at T-3 → sonnet at T-9` (degraded twice)

---

## Phase 3 — Staff-engineer review

ONE subagent call. Reviews the merged diff (not per-task).

### Dispatch template

```
Agent(
  description: "Staff engineer — feature review",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
feature_slug: <slug>

You are the STAFF ENGINEER. The EM dispatched you to review every change shipped during this autonomous run, across three lenses:

  1. Bugs / Correctness — logical errors, race conditions, missing edge cases, broken invariants, untested paths, security issues
  2. Simplification / Clean Code — dead code, premature abstractions, copy-paste, types that should be narrower, functions that should be smaller
  3. Codebase Style — adherence to engineering-standards.md, naming, layering, imports, format choices not auto-fixed by linters

INPUTS:

git_diff_base_to_head:
<output of `git diff $base_sha..HEAD` where $base_sha was captured by Phase 0 Step 0.1 (the commit BEFORE Phase 1's first dispatch)>

engineering_standards (the rules floor):
<paste docs/<slug>/engineering-standards.md verbatim>

planning (architectural context):
<paste docs/<slug>/planning.md verbatim>

blocked_tasks (do not flag missing work for these — they were deliberately skipped):
<list of BLOCKED task IDs with their blocker reasons from execution-report.md>

execution-report so far:
<paste docs/<slug>/execution-report.md verbatim>

<If allocations.md was loaded in Phase 0, include this block; otherwise omit:>
allocations (slot → engineer mapping for context — flag findings can reference the owning engineer):
<paste docs/<slug>/allocations.md verbatim>

OUTPUT FORMAT: one finding per line, prefixed with severity tag:

  [BLOCKER] <file>:<line> — <description>
  [MAJOR] <file>:<line> — <description>
  [MINOR] <file>:<line> — <description>

End with: SUMMARY: <N blockers, M major, K minor>

Severity definitions:
  BLOCKER = the code is wrong (bug, broken invariant, security). MUST be fixed.
  MAJOR = should be fixed for quality but doesn't break anything.
  MINOR = nice-to-have, defer acceptable.

If you find nothing in a category, omit it entirely from the output (do not write "[BLOCKER] (none)").
"""
)
```

### What the EM does with findings

1. **Append all findings verbatim** to the `execution-report.md` under the "Staff-engineer review findings" section.

2. **For each BLOCKER finding:**
   - Identify the affected task (by file path; cross-reference against `engineer-*-tasks.md`'s "Files to touch" lists).
   - **Re-dispatch the affected task through the per-task pipeline ONCE**, with the BLOCKER text as a new concern injected into the senior's prompt (under a "STAFF BLOCKER" header before the task spec).
   - On return:
     - If now SHIPPED → update the task's row in the report; the BLOCKER finding is moved to a "Resolved blockers" subsection.
     - If still BLOCKED → leave the BLOCKER finding under "Blockers"; the task row says `BLOCKED (staff-blocker fix-up failed)`.

3. **MAJOR + MINOR findings:** land in the report verbatim. No fix-up dispatch. User decides whether to address before merging.

---

## Phase 4 — Finalize

### Step 4.1 — Compute run summary

```
Total tasks: <N+M>
Shipped: <count>
Blocked: <count>
Files changed: <wc -l of `git diff --name-only $base_sha..HEAD`>  # $base_sha captured at Phase 0 Step 0.1
Tests added: <best-effort count from diff>
```

### Step 4.2 — Update report header

Set:
- `Finished:` to `Bash("date -u +%Y-%m-%dT%H:%M:%SZ")`
- `Status:`
  - `DONE` if 0 blocked AND 0 staff BLOCKERs
  - `DONE_WITH_BLOCKERS` if any blocked OR any staff BLOCKERs remain
  - `FAILED` if Foundation entirely BLOCKED (no Frontier tasks could run)
- `Final commit:` set to **`Bash("git rev-parse HEAD")` BEFORE the report commit**. Rationale: the report commit is metadata about the shipped work; the "final commit" field references the LAST CODE COMMIT (i.e. the last task's commit), not the report doc commit. Capturing it before the report commit means the report committed in Step 4.3 is already fully finalized — no chicken-and-egg, no stale PR bodies.

### Step 4.3 — Append the report commit (per git strategy)

Use `Bash`:

- **Atomic commits per task on current branch / on new branch:**
  ```
  git add docs/<slug>/execution-report.md
  git commit -m "docs(<slug>): em-ship-feature execution report

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  "
  ```

- **Single squash commit at end on current branch:**
  ```
  git add <all changed files from the run> docs/<slug>/execution-report.md
  git commit -m "feat(<slug>): <one-line feature description>

  Squashed implementation of <feature-name>. See execution report in docs/<slug>/execution-report.md.

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  "
  ```

- **Atomic commits + auto-push + auto-PR at end:**
  ```
  git add docs/<slug>/execution-report.md
  git commit -m "docs(<slug>): em-ship-feature execution report

  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  "
  git push -u origin <working-branch>
  gh pr create --base <base_branch from Phase 0> --title "<feature-name>" --body "$(cat docs/<slug>/execution-report.md)"
  ```
  Capture the PR URL from `gh pr create` stdout for the Step 4.4 report update.

### Step 4.4 — Post-commit cleanup

`Final commit:` was already set in Step 4.2 (to the last task's commit SHA, before the report commit), so the report committed in Step 4.3 is already in its final form.

If the git strategy was auto-push + auto-PR, the PR URL is captured from `gh pr create`'s stdout in Step 4.3. Append it to the report under a `## Pull Request` header via a follow-up commit + push:

```bash
Edit report → add `## Pull Request\n<URL from gh pr create>` section
git add docs/<slug>/execution-report.md
git commit -m "docs(<slug>): record PR URL in execution report"
git push
```

For non-auto-PR strategies, no Step 4.4 work is needed beyond confirming the commit landed.

### Step 4.5 — Print final status to user

```
em-ship-feature: DONE | DONE_WITH_BLOCKERS | FAILED

Tasks: <N+M> total · <shipped> shipped · <blocked> blocked
Files changed: <count>
Allocation: <"applied (<N> engineers attributed)" | "skipped (no allocations.md)" | "skipped (malformed allocations.md)">
<If allocation applied AND there were per-engineer ship/block stats: render a one-liner like "Per-engineer: Alice 5 shipped 0 blocked, Bob 2 shipped 1 blocked, Carol 3 shipped 0 blocked">
<If allocation_risks was non-empty at start of run: render "⚠️ <N> allocation risk(s) were flagged at start — see Notes section of report">
Final commit: <sha>
Report: docs/<slug>/execution-report.md
<PR URL, if auto-PR strategy>
```

If status is DONE_WITH_BLOCKERS, append:
```
There are <N> unresolved blockers. See docs/<slug>/execution-report.md "Per-task blockers" and "Staff-engineer review findings > Blockers" for details.
Options:
  1. Address manually and re-run /superdev:em-ship-feature <slug> (skill will skip SHIPPED tasks).
  2. Wrap in ralph-loop: /ralph-loop /superdev:em-ship-feature <slug> --completion-promise "all tasks shipped, all tests green"
```

---

## Agent Roster

| Role | Subagent type | Model | When |
|---|---|---|---|
| **EM** (orchestrator, main thread) | — | Parent's model + `/effort max` (Hard Gate #1) | All phases. Also runs per-task Steps 3 (debate), 5 (verify), 6 (commit) inline — see "Why EM-inline" in the per-task pipeline section |
| **Senior Engineer** (per task) | `general-purpose` | `model: opus` (Hard Gate #4) | Step 1 (Plan) of every per-task pipeline. Dispatched once per task in Phase 1 (sequential) and per wave in Phase 2 (batched parallel) |
| **Coder** (per task) | `codex-executor` / `gemini-executor` / `general-purpose` with `model: sonnet` | per CLI default — non-claude coders use external CLI defaults | Step 4 (Execute) of every per-task pipeline |
| **Reviewer** (per task plan) | `codex-reviewer` / `gemini-reviewer` / `general-purpose` with `model: sonnet` | matches coder family (Hard Gate #10) | Step 2 (Review) of every per-task pipeline. Re-dispatched in debate round 2 if needed |
| **Staff Engineer** (whole run) | `general-purpose` | `model: opus` (Hard Gate #4) | Phase 3 only, once per run |

### Voices

**EM** — pragmatic, owns sequencing and dispatch. Runs the connective tissue (debate, verify, commit) inline because subagents can't dispatch other subagents in this runtime — so the orchestrator IS the integrator. Also auto-detects and consumes `docs/<slug>/allocations.md` if present (produced by em-feature-plan Phase 7) to inject per-task ownership into senior dispatch context, the per-task commit's Co-Authored-By trailers, and the execution-report's Owner column. Graceful fallback to slot-only attribution if allocations.md is absent or malformed. The voice of "what does the team need to ship this, who's executing each step, and (when allocated) which human owns each task?"

**Senior Engineer** — owns ONE step (Step 1: Plan) per task. Reads engineering-standards.md as the rules floor. Returns a plan in the prescribed format. Does NOT execute, review, debate, verify, or commit — all of those are downstream of the senior's dispatch.

**Coder** — rigor-on-execution. Same per-family lens as in claude-plans-codex-executes for codex; analogous for gemini and sonnet.

**Reviewer** — same family as the coder. Critiques the plan with AGREE/CONCERN/QUESTION/SUMMARY. Read-only.

**Staff Engineer** — senior, opinionated, has authority to flag any code as BLOCKER. Reads the full merged diff. Same brain across the whole feature.

---

## Red Flags — Stop if You Think...

| Thought | Reality |
|---|---|
| "Plan is small, I'll skip Phase 0 and just dispatch" | Phase 0 is non-negotiable — it bundles the hard-gate confirmation, the working-tree check, and the git-strategy choice. Skipping it skips three gates. |
| "Working tree has a few uncommitted files, it'll be fine" | Hard Gate #11: no. gemini-reviewer's read-only enforcement will destructively wipe pre-existing uncommitted state if the run degrades to gemini. Commit or stash first. |
| "Foundation tasks are simple, I'll fan them out in parallel" | Hard Gate #5: Foundation tasks share interfaces. Parallel writers will collide. Sequential is the law. |
| "This senior's plan looks fine, I'll skip the reviewer dispatch" | The per-task debate IS the skill. Skipping it = ignoring the skill. |
| "Codex's quota will probably reset soon, let me retry it" | Hard Gate #7: run-wide degradation, no probing. Stay on the degraded coder. |
| "Sonnet failed once — let me retry the dispatch" | Sonnet has no further fallback. A sonnet failure = BLOCKED for that task. Mark it and continue. |
| "Verify failed, I'll just keep restarting" | Hard Gate #6: bounded retries. Verify restart capped at 1. After that, BLOCKED. |
| "The user might want to know about this BLOCKED task before I continue" | Hard Gate #8: no mid-run user prompts. Log it in the report, continue. The user reads the report at the end. |
| "Staff engineer flagged 3 BLOCKERs — let me re-dispatch each one twice to be safe" | Hard Gate #6: one fix-up pass per BLOCKER. After that, land in report and stop. |
| "I'll write a summary in chat and skip updating the report file" | Hard Gate #9: report file is the authoritative output. Chat summaries are addenda. |
| "The senior should just write the code itself instead of the EM dispatching a coder" | No. Senior plans (Step 1 only). The EM dispatches the Coder (Step 4) and runs verify + commit inline (Steps 5, 6). Same role separation as claude-plans-codex-executes, restructured so the dispatch-flow respects the runtime constraint that subagents can't dispatch other subagents. |
| "The senior should dispatch the reviewer and coder itself" | The senior CAN'T — the `Agent` tool is not available to general-purpose subagents in this runtime. Only the EM main thread can dispatch. If the senior is told to dispatch and tries, it will fail with no Agent tool available. The skill's redesign moved all dispatches to the EM precisely because of this. |
| "I'll dispatch the staff review per-task to be thorough" | No. Phase 3 is ONE call over the merged diff. Per-task staff calls = N Opus calls = exorbitant cost. |
| "Mid-task quota hit — let me execute the rest with the same plan" | No. Restart from Step 2 with the new coder family's reviewer. Same-family review is required. |
| "allocations.md is missing, halt with 'no allocation provided' error" | No. Allocations.md is OPTIONAL upstream output (em-feature-plan Phase 7 only runs if a team roster was provided). Auto-detect: present → consume; absent → slot-only attribution. No halt, no error, no user prompt. |
| "allocations.md has risk callouts — pause and ask the user whether to proceed" | Hard Gate #8: no mid-run user prompts. Surface the risks in the Notes section of execution-report.md at the start of the run, mention in Phase 4 final status, and let the user review after. Run continues regardless. |
| "Assigned engineer to task is Junior — let me dispatch a senior subagent with extra hand-holding to make sure they 'can' do it" | No. The PLAN is the same regardless of who implements it. The senior dispatch's `assigned_engineer:` context is for shaping plan SHAPE (more vs less context) not plan SUBSTANCE. The coder family does the actual writing; engineer level affects review and follow-up, not the plan or the code. |
| "No email in the roster, skip the engineer Co-Authored-By trailer" | No. Synthesize `<name>@team.local` (lowercased ASCII). Git requires syntactically-valid emails in trailers; the placeholder is valid and obviously fake. The human-name documentation value is the point; the email is secondary. |

---

## First-Run Verification

The first time you use this skill on a device, run it on a tiny fixture feature (1 foundation + 1 frontier task) and confirm:

- Phase 0 halts cleanly when the working tree is dirty (Hard Gate #11).
- Phase 0 halts cleanly when HEAD is detached (Step 0.1 branch-state check).
- Phase 0 halts cleanly when `--dangerously-skip-permissions` is NOT active (user answers "no" to question 1).
- The `AskUserQuestion` bundles both gate confirmations and the git-strategy choice into one round-trip.
- The senior subagent (Step 1) returns a structured plan in the prescribed format — and does NOT try to dispatch reviewer or coder subagents.
- The reviewer subagent (Step 2) returns AGREE/CONCERN/QUESTION/SUMMARY format.
- The EM's inline debate (Step 3) correctly updates the plan based on the critique and decides round 2 yes/no.
- The coder subagent (Step 4) actually writes files (verify via `git status --short`).
- The EM's inline verify (Step 5) runs the project's check commands and greps for silent denials.
- The EM's inline commit (Step 6) makes a commit with the correct Co-Authored-By trailer for the coder used.
- The EM's per-task result aggregation populates the report row (TASK / STATUS / CODER / FILES / TESTS / DEBATE_ROUNDS / VERIFY_RESTARTS / NOTES / BLOCKER / COMMIT_SHA) — `Read` before each `Edit`.
- The execution-report.md skeleton is created in Phase 0 and rows flip from PENDING to SHIPPED as tasks complete.
- Foundation runs sequentially; Frontier Step 1 dispatches in parallel waves.
- The staff-engineer dispatch happens once at end-of-run with the full diff.
- The final commit (per chosen git strategy) lands on the working branch with `Final commit:` already populated in the report (Phase 4 ordering — Step 4.2 sets it before Step 4.3 commits).
- **Allocation auto-detect:** with `docs/<slug>/allocations.md` present, the Phase 0 run summary line shows "Allocation: loaded — N engineers, M tasks attributed"; the report's `Allocation` header field reflects the same; the report's Tasks table has named engineers in the Owner column; per-task commits include an engineer `Co-Authored-By: <Name> <name@team.local>` trailer; the staff review (Phase 3) receives allocations.md in its inputs. Without `allocations.md`, the same fields fall back to slot labels (e.g., `(engineer-1)`) and the engineer trailer is omitted — no error, no warning.
- **Allocation risks:** if `allocations.md`'s "Risk callouts" section is non-empty, the risks render at the START of the report's Notes section (Phase 0) and are echoed in the Phase 4 final status — but the run does NOT pause for user confirmation (Hard Gate #8).

If any step doesn't work, debug the affected piece (the SKILL.md prose, the `gemini-reviewer.md` agent, the per-task dispatch templates for Steps 1, 2, or 4, or the allocations.md parsing in Phase 0 Step 0.3) before running on real work.
