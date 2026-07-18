---
name: atlas-goal
description: |
  Atlas autonomous-loop wrap. Hands off from /atlas-autoplan (memo sealed,
  state=READY_FOR_CODER) and drives the remaining 5 stages — Coder →
  /atlas-review-all → /atlas-qa-all → /atlas-ship-verify → /atlas-retro —
  in the CURRENT CC session with a goal artifact as terminal condition.
  Pauses + alerts the operator on any non-PASS gate. Auto-rollback default at Ops
  Gate (inherited from /atlas-verify). Cost-gated against a configurable cost
  ceiling. NO bare /goal trigger (collides with other tools' built-in /goal);
  explicit atlas-goal namespace only. Use after
  /atlas-autoplan completes — one command takes the sprint from sealed-
  scope to shipped. This is the "the operator is approval-points, not orchestrator"
  target state for Tier-1 sprints.
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Skill
  - AskUserQuestion
  - Agent
triggers:
  - atlas-goal
  - atlas goal
  - autonomous loop
  - ship to goal
  - run sprint to ship
  - atlas auto-ship
  - goal loop
  - atlas full loop
---

# atlas-goal

> **Reference implementation.** Examples below target a Convex + Vercel + Clerk stack. Swap in your own commands.

**Atlas autonomous-loop wrap — the meta-conductor that turns a sealed memo into a shipped sprint without the operator in the orchestration seat.** `/atlas-autoplan` ends the Architect phase at `READY_FOR_CODER`; `/atlas-goal` picks up there and drives the remaining five stages mechanically in the CURRENT CC session.

Sister-conductor pattern (`/atlas-autoplan`) orchestrates the Architect-phase skill chain; this skill orchestrates everything AFTER the Architect phase. Together they cover the full sprint loop. The mechanical hand-off is the value — it closes the "operator-as-orchestrator" gap that produces silent-failure-spiral-class incidents.

## Mission

For a sprint at `state == READY_FOR_CODER` with a goal artifact, execute:

```
verify hand-off (state == READY_FOR_CODER; eng-review present)
       ↓
extract goal (explicit arg → state.sprint_goal → memo SUCCESS CRITERIA)
       ↓
─── Stage 1: Coder ──────────────────────────────────────────────
execute the eng-review plan in CURRENT worktree (standard CC dispatch)
/atlas-memo-check at every commit (scope-drift halt)
push + open PR
       ↓
─── Stage 2: Reviewer ───────────────────────────────────────────
Agent(opus → atlas-review-all)   ── pause-and-surface on BLOCKED
       ↓                                       ↑
       │                                       └── the operator loops back to Coder
       ▼
─── Stage 3: Tester ─────────────────────────────────────────────
Agent(opus → atlas-qa-all)       ── pause-and-surface on FAIL
       ↓                                       ↑
       │                                       └── the operator loops back to Coder
       ▼
─── Stage 4: Ops Gate ───────────────────────────────────────────
Agent(opus → atlas-ship-verify)  ── auto-rollback inherited from /atlas-verify
       ↓                                       ↑
       │                                       └── P0 + Architect loopback
       ▼
goal-achievement check (memo SUCCESS CRITERIA against deploy verdict)
       ↓
─── Stage 5: Reflect ────────────────────────────────────────────
Agent(fable → atlas-retro)       ── sprint DONE = retro complete
       ↓
GOAL_ACHIEVED — announce + emit final state
```

State persists across stages via `docs/briefs/<sprint-id>/.atlas-state.json`. Each transition writes the state file so a crashed/interrupted loop can resume from the last completed stage.

## Naming exception

**This skill ships WITHOUT a bare `/goal` trigger.** Atlas's usual default (bare + `atlas-`-prefixed) is exception-cased here because some other tools ship `/goal` as a built-in. Bare-name collision risk outweighs namespace-discoverability benefit. Acceptable triggers are all `atlas-` prefixed or descriptive phrases (`autonomous loop`, `ship to goal`, etc.). Future contributors: do NOT add bare `goal` as a trigger — the collision will silently route the operator's invocations to whichever tool wins the disambiguation.

## When to invoke

- **Sprint at READY_FOR_CODER** — `/atlas-autoplan` just completed; memo is sealed; `03-plan-eng-review.md` exists; the operator is ready to walk away.
- **Tier-1 / Tier-2 sprint** — Tier-3 fast-path (Coder + Tester + Reflect only) does not invoke `/atlas-review-all` or `/atlas-ship-verify`; if the operator wants Tier-3 autonomy, use direct skill invocation or a future `/atlas-goal-fast` variant.
- **Resume after pause-and-surface** — the operator returns from a pause decision; re-invoke `/atlas-goal` to resume from the last completed stage (state file is the truth).

**Do NOT invoke when:**
- Sprint state is NOT `READY_FOR_CODER` — refuses to run (the Architect phase is /atlas-autoplan's job; this skill does not run /ultraplan or author memos).
- Memo has not been sealed (`memo_state != SEALED`) — the goal-loop runs against a sealed contract or not at all.
- The current CC session has unrelated work in progress — the goal-loop owns the session for its duration and any concurrent edits will be flagged by `/atlas-memo-check` as scope drift.
- You want individual stage invocation — use the stage-conductor skill directly (`/atlas-review-all`, `/atlas-qa-all`, `/atlas-ship-verify`, `/atlas-retro`).

## Scope (what this skill OWNS)

1. **Hand-off verification** — refuses to run unless sprint state is `READY_FOR_CODER` and required upstream artifacts are present.
2. **Goal-artifact extraction** — three-source priority (explicit arg → state.sprint_goal → memo SUCCESS CRITERIA derivation).
3. **Stage 1 — Coder execution** — standard CC dispatch against `03-plan-eng-review.md` in the CURRENT worktree; `/atlas-memo-check` at every commit; push + open PR.
4. **Stages 2–5 — sequential stage dispatches** (via `Agent` carrying the per-stage `model:` — see Execution mechanism) in order: `atlas-review-all` → `atlas-qa-all` → `atlas-ship-verify` → `atlas-retro`.
5. **Verdict handling at every stage** — PASS advances; non-PASS pauses the loop and surfaces to the operator via `AskUserQuestion`.
6. **Goal-achievement check** at Ops Gate PASS — verifies the goal-artifact's success criteria are met (memo SUCCESS CRITERIA mapped through `/atlas-verify`'s probe results).
7. **Per-stage cost emissions** to `.atlas-state.json` `stage_costs[]` + running total + the Tier-1 cost-ceiling hard-gate.
8. **State persistence** — `goal_loop_state`, `current_stage`, `stage_costs[]`, `goal_status`, `paused_at`, `resumed_at`.
9. **Goal-loop log authorship** — `06-goal-loop-log.md`, a sibling artifact in the sprint's `docs/briefs/<sprint-id>/`; tracks goal-loop progress + cost + pause/resume events (Ops-Gate report itself remains owned by `/atlas-ship-verify`).
10. **Graceful degradation** when a downstream stage-conductor is missing — log TODO marker, pause, surface to the operator.
11. **Failure surface** — notification alert stub (Phase 1) + portal/dashboard state row + P0 file on Ops-Gate auto-rollback.

## Scope (what this skill DOES NOT do)

- **Run the Architect phase.** Architect = `/atlas-autoplan`'s job. This skill is post-/atlas-autoplan and refuses to run if `READY_FOR_CODER` is not the current state.
- **Make scope decisions.** Scope was sealed by the operator at `/atlas-memo` before this skill is invoked. Any commit drifting from `00-memo.md` IN-SCOPE is mechanically halted by `/atlas-memo-check`.
- **Bypass any individual stage's contract.** Each stage-conductor enforces its own forbidden actions; `/atlas-goal` sequences them, does not weaken them.
- **Auto-merge past BLOCKERs.** Reviewer-phase contract forbids merge with BLOCKER findings; `/atlas-goal` respects.
- **Skip `/atlas-verify`.** Ops-Gate contract makes it mandatory on production state changes; `/atlas-goal` respects.
- **Skip `/atlas-retro`.** Reflect-phase contract makes sprint Done = retro complete; `/atlas-goal` respects.
- **Override `/atlas-ship-verify`'s auto-rollback policy.** Auto-rollback default is owned by `/atlas-verify`; this skill inherits the behavior by invocation; it does not add or remove rollback logic.
- **Run more than one sprint at a time.** One invocation = one sprint loop.
- **Spawn chips for stages** — in-session dispatch is the default (Agent-dispatch carrying the per-stage `model:`). Chips defeat the autonomous-loop point (the operator would have to click).

## Execution mechanism

`/atlas-goal` runs in the CURRENT Claude Code session — it IS the parent orchestrator. Each downstream stage is dispatched via the **`Agent` tool**, NOT chips. Sub-agents return summaries to /atlas-goal, which decides whether to proceed to the next stage OR pause + alert the operator.

| Mode | When to use | How |
|---|---|---|
| **`worktree`** | Sub-agent needs file isolation + real branch + opens PR + returns summary | `Agent(subagent_type: "general-purpose", isolation: "worktree", prompt: ...)` |
| **`in-session`** | Sub-agent reads files + summarizes; no isolation needed; lowest latency | `Agent(subagent_type: "general-purpose", prompt: ...)` |
| **`chip`** | the operator wants to monitor long-running work in his IDE | `mcp__ccd_session__spawn_task(...)` |

**Per-stage defaults (the load-bearing table):**

| Stage | Default mode | Default model | Rationale |
|---|---|---|---|
| **Coder** | **`worktree` (mandatory by default)** | `fable` | Writes code + commits + opens PR — file isolation + autonomous return = the right primitive |
| **Reviewer** (`/atlas-review-all` → second model + /atlas-cso parallel) | `in-session` | `opus` (/atlas-cso half — see row note) | Reads diff + summarizes findings; second model + /atlas-cso run as 2 parallel `Agent` calls |
| **Tester** (`/atlas-qa-all` → probes) | `in-session` | `opus` | Probes execute external commands + return verdicts |
| **Ops Gate** (`/atlas-ship-verify` → deploy + verify) | `in-session` | `opus` | Deploy from main; verify reads prod state |
| **Reflect** (`/atlas-retro` → /atlas-learn) | `in-session` | `fable` | Reads artifact chain + summarizes |

> **Reviewer row note:** the Reviewer's **correctness half runs an independent second-model review** (e.g. a different frontier model via its own CLI/runtime) — it is NOT an `Agent` `model:` param and is left exactly as-is. Only the /atlas-cso (security) half takes `model: "opus"`.

**Override:** per-stage, pass `stage_modes` overrides in the initial /atlas-goal invocation OR set `.atlas-state.json` `stage_modes.<role>` upstream. Override is persisted for downstream audit (`/atlas-learn` drift report).

**Per-stage model selection** (*"one model builds, a different model checks"*):

Model defaults come from the **Default model** column above. Governing principle: **a model is never the sole checker of its own output** — the build-side model builds/plans/synthesizes (Architect, Coder, Reflect); a different model on the checking roles (/atlas-cso, Tester, Ops Gate) + the independent second-model reviewer (Reviewer) check it. Model diversity on the checking roles is the load-bearing constraint.

- Each `Agent(...)` stage dispatch passes `model:` = `stage_models.<role> ?? <table default>`.
- **Override:** per-stage, pass `--model=<role>:<model>` at invocation (mirrors `--mode=`) OR set `.atlas-state.json` `stage_models.<role>` upstream. The chosen model is persisted for downstream audit (`/atlas-learn` drift report) — same mechanism as `stage_modes`.
- **Dispatch-tool consequence:** in-session `Skill()` = session model; `Agent(model:…)` = per-stage model — use Agent-dispatch wherever the stage model must differ from the session. Stages 2–5 below therefore dispatch via `Agent(subagent_type: "general-purpose", model: "<role-model>", prompt: "invoke /<stage-skill> …")` rather than a bare inline `Skill()`.

**Why this beats chips:** chips fragment the conversational loop — spawn-and-die without a callback. Sub-agents via `Agent` tool keep the loop closed; /atlas-goal sees each stage's summary and proceeds OR pauses. The operator is approval-points (memo seal + alerts on non-PASS), not orchestrator.

## Required prerequisites

**Sprint state (must all be true to start):**

| Prereq | How verified | If missing |
|---|---|---|
| `.atlas-state.json` exists at `docs/briefs/<sprint-id>/.atlas-state.json` | `jq -e . "$STATE_FILE"` | ABORT — "no sprint to run; invoke `/atlas-autoplan` first" |
| `current_step == "READY_FOR_CODER"` | `jq -r '.current_step'` | ABORT — "sprint state is `<actual>`; goal-loop requires READY_FOR_CODER" |
| `memo_state == "SEALED"` | `jq -r '.memo_state'` | ABORT — "memo not sealed; re-enter `/atlas-autoplan` to seal" |
| `00-memo.md` + `03-plan-eng-review.md` both present | `test -f` | ABORT — "artifact chain broken; do not advance" |
| Working tree clean OR contains only sprint-scope WIP | `git status --porcelain` + memo-check | WARN — first Coder commit will surface scope drift if WIP is unrelated |
| Tier is 1 or 2 | `jq -r '.tier'` | ABORT — "Tier 3 fast-path does not invoke goal-loop; use individual skills" |

**Downstream stage-conductor skills (this skill orchestrates):**

| Stage | Skill | Status | Graceful-degrade? |
|---|---|---|---|
| 2 — Reviewer | `/atlas-review-all` | **EXISTS** | No — pause + surface to the operator if missing |
| 3 — Tester | `/atlas-qa-all` | **EXISTS** | No — pause + surface to the operator if missing |
| 4 — Ops Gate | `/atlas-ship-verify` | **EXISTS** | No — pause + surface to the operator if missing |
| 5 — Reflect | `/atlas-retro` | **EXISTS** | No — pause + surface to the operator if missing |
| In-loop | `/atlas-memo-check` (Coder commit gate) | **EXISTS** | HARD ABORT if missing — drift detection is load-bearing |

All four stage-conductors ship with Atlas. The graceful-degradation column codifies defensive behavior for the case where a future refactor renames or removes a stage-conductor without amending this skill — the loop pauses for the operator rather than silently skipping a phase. **`/atlas-memo-check` is the lone HARD-ABORT prereq** because without it, scope-drift can land silently and the goal-loop becomes the very anti-pattern Atlas exists to prevent.

## Goal-artifact extraction (3-source priority order)

The goal is the terminal condition the loop verifies at Ops-Gate PASS. Three sources, checked in order:

| Priority | Source | When chosen | Format |
|---|---|---|---|
| 1 | **Explicit argument** to `/atlas-goal "<one-line goal>"` | the operator passed a goal string at invocation | Free-form one-liner; persisted as `.atlas-state.json` `goal_artifact.source = "arg"` |
| 2 | `.atlas-state.json` `sprint_goal` field | Architect set it during `/atlas-autoplan` (Phase 2 enhancement; today usually absent) | Single string; persisted as `goal_artifact.source = "state"` |
| 3 | **Memo SUCCESS CRITERIA section derivation** (default) | No explicit arg, no state field — extract from `00-memo.md` | Auto-extract: first numbered criterion OR aggregate of all criteria if ≤3; persisted as `goal_artifact.source = "memo"` |

Extraction is **idempotent** — re-invocation re-uses the previously extracted goal (stored in `.atlas-state.json` `goal_artifact`) unless the operator explicitly passes a new one.

```bash
# Extraction precedence (pseudo-implementation)
EXPLICIT_ARG="${1:-}"
STATE_FILE="docs/briefs/${SPRINT_ID}/.atlas-state.json"
MEMO_FILE="docs/briefs/${SPRINT_ID}/00-memo.md"

if [ -n "$EXPLICIT_ARG" ]; then
  GOAL="$EXPLICIT_ARG"
  SOURCE="arg"
elif jq -e '.sprint_goal // empty' "$STATE_FILE" > /dev/null; then
  GOAL=$(jq -r '.sprint_goal' "$STATE_FILE")
  SOURCE="state"
else
  # Auto-extract from memo SUCCESS CRITERIA section
  GOAL=$(awk '/^## SUCCESS CRITERIA/,/^## /' "$MEMO_FILE" | grep -v '^## ' | grep -E '^[0-9-]' | head -3 | paste -sd ' | ' -)
  SOURCE="memo"
fi

# Persist the goal artifact so re-invocation is idempotent
jq --arg g "$GOAL" --arg s "$SOURCE" '.goal_artifact = { goal: $g, source: $s, extracted_at: "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'" }' "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"
```

If extraction yields an empty goal (memo missing SUCCESS CRITERIA section, no explicit arg, no state field): HALT + raise to the operator — "Goal artifact undefined. Pass an explicit arg or amend the memo to include SUCCESS CRITERIA."

## State machine

```
INIT ─► VERIFY_HANDOFF ─► EXTRACT_GOAL ─► STAGE_CODER ─► STAGE_REVIEWER ─► STAGE_TESTER ─► STAGE_OPS_GATE ─► GOAL_CHECK ─► STAGE_REFLECT ─► GOAL_ACHIEVED
                                              │                  │                 │              │
                                              ▼                  ▼                 ▼              ▼
                                       PAUSED_CODER       PAUSED_REVIEWER   PAUSED_TESTER  PAUSED_OPS
                                       (memo-check        (BLOCKED;         (FAIL; the operator     (FAIL or
                                        halt; the operator         the operator decides       decides loop-  ROLLED_BACK;
                                        decides           loop-back)        back vs        the operator decides
                                        amend vs                            replan)        retry vs
                                        kill loop)                                         escalate)
                                              │                  │                 │              │
                                              └──── the operator resumes via re-invocation of /atlas-goal ──┘
```

State persisted to `.atlas-state.json` after every transition.

**Transition rules:**

| From | Trigger | To |
|---|---|---|
| INIT | invoked | VERIFY_HANDOFF |
| VERIFY_HANDOFF | all prereqs met | EXTRACT_GOAL |
| VERIFY_HANDOFF | any prereq fails | ABORT (clean exit; no state mutation) |
| EXTRACT_GOAL | goal extracted | STAGE_CODER |
| EXTRACT_GOAL | extraction yields empty | HALT + raise to the operator |
| STAGE_CODER | Coder commits clean + push + PR opened | STAGE_REVIEWER |
| STAGE_CODER | `/atlas-memo-check` HALT (scope drift) | PAUSED_CODER |
| STAGE_CODER | cost cap hit (Tier-1 ceiling) | PAUSED_COST |
| STAGE_REVIEWER | `/atlas-review-all` returns PASS | STAGE_TESTER |
| STAGE_REVIEWER | `/atlas-review-all` returns BLOCKED | PAUSED_REVIEWER |
| STAGE_REVIEWER | stage-conductor skill missing | PAUSED_MISSING_SKILL |
| STAGE_TESTER | `/atlas-qa-all` returns PASS | STAGE_OPS_GATE |
| STAGE_TESTER | `/atlas-qa-all` returns FAIL | PAUSED_TESTER |
| STAGE_TESTER | stage-conductor skill missing | PAUSED_MISSING_SKILL |
| STAGE_OPS_GATE | `/atlas-ship-verify` returns PASS | GOAL_CHECK |
| STAGE_OPS_GATE | `/atlas-ship-verify` returns FAIL + auto-rollback | PAUSED_OPS (P0 + Architect loopback) |
| STAGE_OPS_GATE | `/atlas-ship-verify` returns SKIPPED_DOCS_ONLY (docs-only) | GOAL_CHECK (no deploy probes; goal-check is memo-completion only) |
| STAGE_OPS_GATE | stage-conductor skill missing | PAUSED_MISSING_SKILL |
| GOAL_CHECK | goal-artifact success criteria satisfied | STAGE_REFLECT |
| GOAL_CHECK | criteria NOT satisfied despite Ops-Gate PASS | PAUSED_GOAL_MISMATCH (rare; usually means memo SUCCESS CRITERIA were poorly written) |
| STAGE_REFLECT | `/atlas-retro` returns OK | GOAL_ACHIEVED |
| STAGE_REFLECT | stage-conductor skill missing | PAUSED_MISSING_SKILL |
| any PAUSED_* | the operator resumes via re-invocation | resumes at the stage-conductor that was paused (rerun the stage's skill against the same artifacts) |
| any | unrecoverable error | HALT + raise to the operator |

**HALT + raise to the operator** per the Atlas loop-authority convention — auto-retry past a HALT signal is forbidden.

## Workflow

### Step 0 — Bootstrap + verify hand-off

```bash
cd "$(git rev-parse --show-toplevel)"
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
  echo "ABORT: Run /atlas-goal from a sprint branch, not main."
  exit 1
fi

# Find the active sprint state file (most-recently-modified)
STATE_FILE=$(ls -t docs/briefs/*/.atlas-state.json 2>/dev/null | head -1)
if [ -z "$STATE_FILE" ]; then
  echo "ABORT: no .atlas-state.json found under docs/briefs/. Run /atlas-autoplan first."
  exit 1
fi
SPRINT_ID=$(jq -r '.sprint_id' "$STATE_FILE")

# Verify all prereqs
CURRENT_STEP=$(jq -r '.current_step' "$STATE_FILE")
MEMO_STATE=$(jq -r '.memo_state' "$STATE_FILE")
TIER=$(jq -r '.tier' "$STATE_FILE")

[ "$CURRENT_STEP" = "READY_FOR_CODER" ] || { echo "ABORT: state is $CURRENT_STEP, not READY_FOR_CODER"; exit 1; }
[ "$MEMO_STATE" = "SEALED" ]            || { echo "ABORT: memo_state is $MEMO_STATE, not SEALED"; exit 1; }
[ -f "docs/briefs/${SPRINT_ID}/00-memo.md" ]            || { echo "ABORT: 00-memo.md missing"; exit 1; }
[ -f "docs/briefs/${SPRINT_ID}/03-plan-eng-review.md" ] || { echo "ABORT: 03-plan-eng-review.md missing"; exit 1; }
[ "$TIER" = "1" ] || [ "$TIER" = "2" ]  || { echo "ABORT: Tier $TIER does not use goal-loop (use individual skills)"; exit 1; }
```

### Step 1 — Extract goal artifact + initialize loop-log

Per "Goal-artifact extraction" §. Persist to `.atlas-state.json`.

Initialize `docs/briefs/${SPRINT_ID}/06-goal-loop-log.md` with header:

```markdown
# Goal-loop log — <sprint-id>

**Goal:** <extracted-goal>
**Goal source:** <arg | state | memo>
**Loop started:** <ISO timestamp>
**Tier:** <1 | 2>
**Cost ceiling:** <configured Tier-1 ceiling> (Tier 1) / <configured Tier-2 ceiling> (Tier 2)

## Stage progression
```

Append a row per stage transition as the loop progresses (chronological).

### Step 2 — Stage 1: Coder

The Coder runs in the CURRENT CC session in the CURRENT worktree. Standard CC dispatch — read `03-plan-eng-review.md`, implement top-to-bottom, commit incrementally.

**Coder model:** when the Coder stage is Agent-dispatched (`worktree` mode per the per-stage defaults table), the dispatch passes the configured build-side model (= `stage_models.coder ?? <build-side default>`).

**At every commit (Coder discipline):**

```bash
# Pseudo-flow per commit
git add <staged-files>
# Invoke /atlas-memo-check BEFORE running git commit
Skill(skill: "atlas-memo-check", args: "staged")
# If memo-check returns HALT → PAUSED_CODER, surface to the operator (memo amend or kill loop)
# If memo-check returns OK → proceed with commit
git commit -m "<message>"
```

After all commits land:
```bash
git push -u origin "$BRANCH"
gh pr create --title "<sprint-title>" --body "<memo-summary; cites 00-memo.md + 03-plan-eng-review.md>"
```

Persist `stage_costs[]` entry: `{ stage: "coder", cost_usd: <accumulated>, completed_at: <ts> }`. Transition `current_stage = "STAGE_REVIEWER"`.

### Step 3 — Stage 2: Reviewer (Agent dispatch)

```
Agent(subagent_type: "general-purpose", model: "opus",
      prompt: "invoke /atlas-review-all with args: sprint_id=<sprint_id>")
```

Stage model `opus` = `stage_models.reviewer ?? opus` — pins the /atlas-cso half; the correctness half runs the independent second-model review regardless (not an `Agent` `model:` param).

`/atlas-review-all` runs the second-model review + `/atlas-cso` in parallel, writes `04-review-codex.md` + `04-review-cso.md`, sets `reviewer_state` to PASS / BLOCKED / NEEDS-REVISION.

Post-skill: re-read state, branch on verdict:

```bash
REVIEWER_STATE=$(jq -r '.reviewer_state' "$STATE_FILE")
case "$REVIEWER_STATE" in
  PASS)
    # Advance to Stage 3
    ;;
  BLOCKED|NEEDS-REVISION)
    # Pause; surface to the operator for decision
    # AskUserQuestion: "Reviewer returned $REVIEWER_STATE. Loop back to Coder? Escalate to Architect? Kill loop?"
    exit 0
    ;;
  *)
    # HALT + raise to the operator
    exit 1
    ;;
esac
```

Persist `stage_costs[]` entry. Append row to `06-goal-loop-log.md`.

### Step 4 — Stage 3: Tester (Agent dispatch)

```
Agent(subagent_type: "general-purpose", model: "opus",
      prompt: "invoke /atlas-qa-all with args: sprint_id=<sprint_id>")
```

Stage model `opus` = `stage_models.tester ?? opus`.

`/atlas-qa-all` runs the mechanical Tester chain (`/atlas-probe` → `/atlas-investigate` → `/atlas-browse` → `/atlas-browser-cookies` → `/qa`). Writes `05-verify-<probe>.md` per probe. Sets `tester_state`.

Post-skill: same verdict branch as Stage 2.

```bash
TESTER_STATE=$(jq -r '.tester_state' "$STATE_FILE")
case "$TESTER_STATE" in
  TESTER_PASS|PASS) ;;
  TESTER_FAIL|FAIL|INCONCLUSIVE)
    # Pause + surface
    exit 0
    ;;
esac
```

Persist `stage_costs[]` + log row.

### Step 5 — Stage 4: Ops Gate (Agent dispatch)

```
Agent(subagent_type: "general-purpose", model: "opus",
      prompt: "invoke /atlas-ship-verify with args: sprint_id=<sprint_id>")
```

Stage model `opus` = `stage_models.ops_gate ?? opus`.

`/atlas-ship-verify` runs the deploy chain (`/ship` → `atlas-deploy` → `/atlas-canary` → `/atlas-verify`). **Auto-rollback is inherited from `/atlas-verify`** — this skill adds no separate rollback logic.

Post-skill: read `ops_state`.

```bash
OPS_STATE=$(jq -r '.ops_state' "$STATE_FILE")
case "$OPS_STATE" in
  COMPLETED|VERIFIED|SKIPPED_DOCS_ONLY)
    # Advance to goal-check
    ;;
  ROLLED_BACK)
    # P0 file already filed by /atlas-verify; Telegram alert already sent
    # Pause + surface: "Auto-rollback fired. Loop back to Architect for root cause?"
    exit 0
    ;;
  HOLD_FOR_OPERATOR)
    # /atlas-verify FAIL with .no_auto_rollback set
    # Pause + surface: "FAIL with rollback override. Manual rollback / hold / re-verify?"
    exit 0
    ;;
esac
```

Persist `stage_costs[]` + log row.

### Step 6 — Goal-achievement check

At Ops-Gate PASS (or SKIPPED_DOCS_ONLY), verify the goal-artifact's success criteria are met. The memo's SUCCESS CRITERIA were authored under `/atlas-memo`'s contract to be `/atlas-verify`-checkable; goal-check reads `/atlas-verify`'s per-criterion probe results from `06-verify-report.md`.

```bash
# Pseudo-check (reads 06-verify-report.md PASS verdicts against memo SUCCESS CRITERIA)
GOAL_CRITERIA=$(jq -r '.goal_artifact.goal' "$STATE_FILE")
VERIFY_PASS=$(jq -r '.verify_outcome // "UNKNOWN"' "$STATE_FILE")

if [ "$VERIFY_PASS" = "PASS" ]; then
  # Goal achieved
  jq '.goal_status = "ACHIEVED"' "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"
else
  # Rare: Ops-Gate PASS but goal-criteria not met (poorly-written memo criteria)
  # PAUSED_GOAL_MISMATCH — surface to the operator
  jq '.goal_status = "MISMATCH" | .current_stage = "PAUSED_GOAL_MISMATCH"' "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"
  exit 0
fi
```

For SKIPPED_DOCS_ONLY sprints (docs-only): goal-check defaults to PASS if the docs were merged successfully (`gh pr view --json mergedAt`).

### Step 7 — Stage 5: Reflect (Agent dispatch)

```
Agent(subagent_type: "general-purpose", model: "fable",
      prompt: "invoke /atlas-retro with args: sprint_id=<sprint_id>")
```

Stage model `fable` = `stage_models.reflect ?? fable` (Reflect synthesizes — a build-side role; checking already happened upstream at Reviewer/Tester/Ops Gate).

`/atlas-retro` invokes `/atlas-learn` internally, computes sprint scorecard + cross-sprint trend, surfaces HIGH-leverage proposals to the operator for approval, writes `07-retro-report.md`, sets `retro_state: COMPLETE` + `sprint_state: DONE`.

Post-skill: transition `current_stage = "GOAL_ACHIEVED"`. Commit the final state.

### Step 8 — Announce sprint DONE

```bash
OPERATOR_TOUCHPOINTS=$(jq -r '[.step_log[] | select(.event == "tom_touchpoint")] | length' "$STATE_FILE")
TOTAL_COST=$(jq -r '[.stage_costs[].cost_usd] | add' "$STATE_FILE")
DURATION=$(echo "$(date -u +%s) - $(jq -r '.goal_loop_started_at' "$STATE_FILE" | xargs -I{} date -d {} +%s)" | bc)

echo "
🎯 Goal achieved — sprint <sprint-id> DONE

Goal:           <extracted-goal>
the operator touchpoints: $OPERATOR_TOUCHPOINTS
Total cost:     \$$TOTAL_COST
Duration:       $((DURATION / 60))m
Stages:         Coder ✅ → Reviewer ✅ → Tester ✅ → Ops Gate ✅ → Reflect ✅
Artifacts:      docs/briefs/<sprint-id>/00..07-*.md

Sprint state: DONE
Next: /atlas-autoplan for the next sprint (or read 07-retro-report.md for harness-amendment proposals the operator approved).
"
```

Final commit:

```bash
git add "docs/briefs/${SPRINT_ID}/"
git commit -m "atlas(goal): sprint ${SPRINT_ID} DONE — goal achieved

operator touchpoints: $OPERATOR_TOUCHPOINTS
Total cost: \$$TOTAL_COST
Stages: Coder → Reviewer → Tester → Ops Gate → Reflect (all PASS)"
```

## Pause-and-surface semantics

At every non-PASS gate, the loop pauses. the operator is the resumer.

| Pause | the operator decision (via AskUserQuestion) |
|---|---|
| `PAUSED_CODER` (memo-check halt) | Amend memo via `/atlas-memo` in amendment mode / Kill loop and exit |
| `PAUSED_REVIEWER` (BLOCKED) | Loop back to Coder (Coder rework against findings) / Escalate to Architect (replan) / Kill loop |
| `PAUSED_TESTER` (FAIL) | Loop back to Coder (Coder fixes Tester findings) / Escalate to Architect (replan) / Kill loop |
| `PAUSED_OPS` (FAIL or ROLLED_BACK) | Loop back to Architect (root cause) / Manual rollback (if `.no_auto_rollback`) / Kill loop |
| `PAUSED_GOAL_MISMATCH` (rare) | Amend memo SUCCESS CRITERIA / Accept current state as DONE / Loop back to Coder for more work |
| `PAUSED_MISSING_SKILL` | Authorize manual cascade (the operator drives the missing stage by hand) / Wait for scaffold + retry / Kill loop |
| `PAUSED_COST` (Tier-1 ceiling hit) | Raise the cap (note in `06-goal-loop-log.md`) / Kill loop |

**Re-invocation behavior:** After the operator decides, re-invoke `/atlas-goal`. The loop reads `.atlas-state.json`, sees the `current_stage` is `PAUSED_*`, and resumes by re-running the stage's skill against the (possibly updated) artifacts. Resume is **idempotent** — re-running `/atlas-review-all` against the same diff yields the same verdict; the re-run only does work if the diff changed (Coder rework, memo amendment, etc.).

## Per-stage cost emissions + total loop ceiling

Atlas enforces a configurable cost ceiling per tier (set the values to match your own budget policy):

| Tier | Alert | Hard gates |
|---|---|---|
| **1** | configurable | escalating thresholds, loop pauses at the Tier-1 hard ceiling |
| **2** | configurable | loop pauses at the Tier-2 hard ceiling |

**Second-model reviewer sub-cap (Tier 1+2):** an optional per-pass + per-day ceiling — enforced by `/atlas-review-all` internally; `/atlas-goal` aggregates the reviewer cost into the total but does NOT enforce the sub-cap (that's `/atlas-review-all`'s contract).

After each stage:

```bash
STAGE_COST=$(jq -r '.last_stage_cost_usd // 0' "$STATE_FILE")
TOTAL_COST=$(jq -r '[.stage_costs[].cost_usd] | add' "$STATE_FILE")
# Tier ceilings come from your own budget config; substitute real numbers.
CEILING=$(jq -r 'if .tier == 1 then .tier1_ceiling elif .tier == 2 then .tier2_ceiling else 1e9 end' "$STATE_FILE")

if [ "$(echo "$TOTAL_COST > $CEILING" | bc -l)" = "1" ]; then
  jq '.current_stage = "PAUSED_COST"' "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"
  echo "💸 PAUSED_COST — total \$$TOTAL_COST exceeded Tier $TIER ceiling \$$CEILING"
  exit 0
fi
```

Per-stage cost emissions append to `06-goal-loop-log.md` as a running ledger.

## Auto-compact behavior

The loop may compact mid-flight as context fills. Compact preserves continuity because:

1. `.atlas-state.json` is the source of truth — re-read on resume.
2. `06-goal-loop-log.md` carries the chronological narrative — re-read on resume.
3. Each stage-conductor invocation is fresh (Skill tool boundary) — no cross-stage in-context state required.

If compact fires mid-stage (e.g., mid-Coder), the loop resumes by re-reading state + log + the in-progress diff. Pre-compact memory: any uncommitted Coder edits MUST be staged + committed before compact OR the compact summary will lose them. **Recommendation:** the loop commits incrementally at every logical breakpoint, never accumulates >1 hour of uncommitted work.

## Failure surface

Three channels, fire in this order on any non-PASS:

1. **Notification alert** (chat/messaging surface of your choice; Phase 1 may stub this as a console log). Latency: seconds. Includes sprint-id, paused stage, verdict, link to the portal/dashboard state view.
2. **Portal/dashboard state row** (state file is the source; a dashboard may read it from your state store). Latency: visible on next refresh.
3. **P0 incident file** at `docs/incidents/p0-<date>-<sprint-id>.md` — written ONLY on Ops-Gate auto-rollback (`/atlas-ship-verify` → `/atlas-verify` writes this; goal-loop does not duplicate). Other pause types do NOT file P0.

Reasoning: a low-latency notification for the operator, a dashboard for the permanent record, and P0 only for production breakage. Goal-loop pauses (Reviewer BLOCKED, Tester FAIL) are sprint-internal and do not warrant P0 escalation.

## Graceful degradation (missing stage-conductor)

All four stage-conductors ship with Atlas. This section is **defensive design** for the case where a future refactor renames or removes a stage-conductor without amending `/atlas-goal`.

When `Skill(skill: "<stage-conductor>", ...)` fails with "skill not found":

```bash
# Pseudo-flow
echo "# PENDING — <skill> not yet scaffolded" >> "docs/briefs/${SPRINT_ID}/06-goal-loop-log.md"
echo "  Stage: <N>, paused at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "docs/briefs/${SPRINT_ID}/06-goal-loop-log.md"

jq --arg skill "<skill>" '.current_stage = "PAUSED_MISSING_SKILL" | .missing_skill = $skill' "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"

# AskUserQuestion: the operator decides authorize manual cascade / wait for scaffold + retry / kill loop
exit 0
```

This is **not silent skip** — the gap is logged, the state file records the missing skill, the loop pauses for the operator. Atlas's discipline is mechanical, not aspirational; never let a missing scaffold silently advance the loop.

## Loop-back semantics

Re-invocation of `/atlas-goal` after a pause:

| Paused at | What re-invocation does |
|---|---|
| `PAUSED_CODER` (memo-check halt) | Reads state. If `memo_state` flipped to AMENDED via `/atlas-autoplan` re-entry, advance to STAGE_REVIEWER (or back to STAGE_CODER if Coder needs to rework against amended scope). If memo unchanged, ABORT (the operator must amend or kill). |
| `PAUSED_REVIEWER` | Re-invokes `/atlas-review-all`. Idempotent — same diff = same verdict. Loop advances only if Coder pushed new commits. |
| `PAUSED_TESTER` | Re-invokes `/atlas-qa-all`. Same idempotency. |
| `PAUSED_OPS` | Re-invokes `/atlas-ship-verify`. Re-deploy + re-verify. Idempotent if diff unchanged; loop advances only if new deploy SHA was generated. |
| `PAUSED_GOAL_MISMATCH` | Re-checks goal-artifact against `06-verify-report.md`. The operator must have either amended SUCCESS CRITERIA OR ack'd the mismatch as "good enough" (in which case loop transitions to GOAL_ACHIEVED). |
| `PAUSED_MISSING_SKILL` | Re-checks skill availability. If now present, re-invokes the stage. If still missing, re-pauses. |
| `PAUSED_COST` | Re-checks cap (the operator may have manually bumped the ceiling in state file or accepted overrun). |

**Cap re-invocation depth at 3** for the same pause state. If a stage pauses, the operator resumes, and the same pause fires again 3 times — HALT + raise to the operator permanently. Convergence failure = needs human re-architect, not more cycles.

## Failure-mode playbook

- **Sprint branch is `main`** → ABORT. `/atlas-goal` requires a sprint branch (per Coder's worktree contract).
- **`.atlas-state.json` exists but `current_step` is not `READY_FOR_CODER`** → ABORT with the actual state value; do NOT auto-correct.
- **Stage-conductor returns error (not just missing)** → log to `step_log`; HALT + raise to the operator. Errors aren't graceful-degraded; only the "skill not found" case gets the PAUSED_MISSING_SKILL treatment.
- **Cap re-invocation depth (3x same pause)** → HARD HALT + raise to the operator. The loop is no longer converging; human re-architect required.
- **Concurrent `/atlas-goal` invocation in same sprint** → detected via `.atlas-state.json` `current_stage` already in non-terminal-non-paused state; later invocation logs warning + exits without re-running.
- **State file write fails** → HARD ABORT. State persistence is load-bearing; without it, the loop cannot safely resume.
- **`/atlas-ship-verify` returns inconsistent verdict** (e.g., `ops_state = COMPLETED` but `verify_outcome = FAIL`) → HALT + raise to the operator. State inconsistency is never auto-corrected.
- **Coder dispatch produces no commits** (Coder decides plan is unimplementable) → loop pauses with note in `06-goal-loop-log.md`; the operator routes to Architect for replan (or kills loop).
- **Memo SUCCESS CRITERIA section absent** → `EXTRACT_GOAL` HALT — "memo lacks SUCCESS CRITERIA; goal-loop cannot derive terminal condition; amend memo via `/atlas-memo` and re-invoke."
- **Auto-rollback fires + revert PR fails** → `/atlas-verify` writes the P0 file; `/atlas-goal` sees `ROLLED_BACK` + an `incident_file` reference and pauses for the operator; manual intervention required.

## What this skill forbids

- **Running before `/atlas-autoplan` completes.** Hand-off contract: `current_step == READY_FOR_CODER` or refuse.
- **Modifying the memo or eng-review.** Architect artifacts are upstream; this skill READS them.
- **Skipping `/atlas-memo-check` at Coder commits.** Drift detection is load-bearing — bypassing it makes goal-loop itself the silent-failure-spiral mechanism.
- **Skipping `/atlas-ship-verify` on production state changes.** docs-only skip is `/atlas-ship-verify`'s contract (docs-only paths); `/atlas-goal` does not pre-judge.
- **Skipping `/atlas-retro`.** Sprint Done = retro complete (per `/atlas-retro` contract); `/atlas-goal` cannot mark `sprint_state = DONE` without retro PASS.
- **Auto-resuming past a HALT.** HALT = the operator decision required; this skill never retries past a HALT signal.
- **Spawning chips for stages.** In-session dispatch only (Agent-dispatch carrying the per-stage `model:`, not chips). Chips defeat the autonomous-loop point (the operator would have to click).
- **Mutating `in_scope_files` / `in_scope_globs`.** Architect-owned via `/atlas-memo`; this skill threads them but does not modify.
- **Running on Tier 3 sprints.** Tier 3 fast-path skips Reviewer + Ops Gate per the Atlas convention; goal-loop is for Tier 1/2 only.
- **Filing P0 for non-Ops-Gate pauses.** Only Ops-Gate auto-rollback warrants P0; Reviewer BLOCKED and Tester FAIL are sprint-internal.
- **Concurrent invocation against the same sprint.** One goal-loop per sprint; second invocation no-ops.
- **Exceeding the cost cap silently.** The configured Tier-1/Tier-2 ceiling is a hard pause, not a soft alert.

## Cost discipline

| Tier | Alert | Hard pause |
|---|---|---|
| 1 | configurable | escalating thresholds up to the Tier-1 hard ceiling |
| 2 | configurable | Tier-2 hard ceiling |

`/atlas-goal` aggregates per-stage `cost_usd` into `.atlas-state.json` `stage_costs[]`. Total computed on every transition. On hard-pause trigger: persist `current_stage = "PAUSED_COST"` + surface to the operator + exit cleanly.

The second-model reviewer sub-cap (per-pass + per-day) is enforced inside `/atlas-review-all`; `/atlas-goal` does NOT duplicate the enforcement, but DOES include reviewer spend in the rolling total against the loop ceiling.

## Tier classification

**Tier 2 itself** — pure orchestration, no production state change directly. The sprints `/atlas-goal` drives span Tier 1 / Tier 2 (Tier 3 sprints do NOT use goal-loop per the contract above).

## References

- `.claude/skills/atlas-autoplan/SKILL.md` (sister Architect-phase orchestrator)
- `.claude/skills/atlas-review-all/SKILL.md` (Stage 2 — Reviewer)
- `.claude/skills/atlas-qa-all/SKILL.md` (Stage 3 — Tester)
- `.claude/skills/atlas-ship-verify/SKILL.md` (Stage 4 — Ops Gate; owns auto-rollback)
- `.claude/skills/atlas-retro/SKILL.md` (Stage 5 — Reflect; sprint DONE = retro complete)
- `.claude/skills/atlas-memo-check/SKILL.md` (Coder commit gate; HARD ABORT if missing)

## gstack alignment note

gstack does NOT have an equivalent god-conductor — gstack's autoplan is stage-conductor-only and stops at sprint planning. `/atlas-goal` is an **Atlas-original innovation** layered on top of the gstack-shaped stage-conductors that already exist (Reviewer / Tester / Ops Gate / Reflect). gstack's `office-hours` skill provides goal-shaped framing patterns we drew on for the goal-artifact extraction logic (specifically the 3-source priority precedent: explicit > state > derived), but the autonomous-loop wrap itself is Atlas-original. This is consistent with Atlas's pattern of borrowing gstack's stage-conductor backbone while diverging on substrate (in-session Skill invocation vs. meta-prompting) and adding the autonomous-loop layer. gstack reference: `github.com/garrytan/gstack`.
