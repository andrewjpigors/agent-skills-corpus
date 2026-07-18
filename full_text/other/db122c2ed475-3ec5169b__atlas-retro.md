---
name: atlas-retro
description: |
  Atlas Reflect-phase stage-conductor (meta-loop closer). Wraps /atlas-learn
  per gstack's learn-vs-retro split — /atlas-learn extracts a sprint's
  lessons; /atlas-retro adds sprint scorecard + cross-sprint trend +
  the operator-approval gate for HIGH-leverage harness amendments + final sprint-DONE
  state transition. Reads full 00..06 artifact chain plus /atlas-learn's
  07-learn-report.md; writes 07-retro-report.md as sibling. Use after
  /atlas-ship-verify completes (deploy_state = VERIFIED or ROLLED_BACK).
  Sprint Done = retro complete. This is what makes Atlas self-improve.
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Skill
  - AskUserQuestion
triggers:
  - atlas-retro
  - retro
  - atlas retro
  - sprint retro
  - close sprint
  - reflect phase
  - atlas reflect
  - meta loop close
---

# atlas-retro

**Atlas Reflect-phase stage-conductor — the meta-loop closer.** Without this stage, sprint lessons stay in heads and the harness can't self-improve. With it, every sprint produces a sealed scorecard + ranked harness-improvement proposals + the operator-approval gate + clean DONE transition. `/atlas-retro` is the conductor; `/atlas-learn` is the leaf that does the load-bearing extraction.

## Mission

For a sprint that has reached Ops-Gate verdict (`deploy_state` in `{VERIFIED, ROLLED_BACK}`):

1. **Delegate lesson extraction to `/atlas-learn`** — it writes `07-learn-report.md`.
2. **Compute sprint scorecard** — the operator-touchpoint count, drift count, time-to-deploy, BLOCKER counts, auto-rollback flag, Coder bounces, memo amendments.
3. **Compute cross-sprint trend** (only if ≥5 completed sprints exist) — rolling 10-sprint median per scorecard metric; surface regressions vs improvements.
4. **Surface HIGH-leverage proposals to the operator for amendment approval** — via `AskUserQuestion`.
5. **Write `07-retro-report.md`** as sibling to `07-learn-report.md` (Option B per parent-session CC pick; see §"File-naming decision" below).
6. **Transition sprint state** — `retro_state: COMPLETE`, `sprint_state: DONE`.
7. **Suggest next** — either kickoff of next sprint to amend the harness, or note that proposals are queued for the next memo as scope-additions.

The mechanical pairing (`atlas-learn` for extraction, `atlas-retro` for scoring + gating + closing) IS the value. Collapsing both into one skill makes the corpus query (gstack `learn` pattern) ambiguous and obscures the operator-approval gate.

## When to invoke

- **Sprint reached Ops-Gate verdict** — `/atlas-ship-verify` has completed; `.atlas-state.json` `deploy_state` is `VERIFIED` (sprint passed) or `ROLLED_BACK` (sprint failed + auto-rolled-back).
- **Resume after the operator interrupt** — `.atlas-state.json` shows `retro_state` in `IN_PROGRESS` or absent; conductor picks up at the next pending sub-step.
- **Manual close-out** — the operator invokes after merging a sprint that bypassed `/atlas-ship-verify` (rare; doc-only sprints in Tier-3 mode).

**Do NOT invoke when:**
- Sprint is mid-flight (`deploy_state` is `null`, `DEPLOYING`, or `PENDING_VERIFY`). Lessons are premature; the artifact chain is incomplete. Wait for `/atlas-ship-verify`.
- Sprint already has `retro_state: COMPLETE` and `sprint_state: DONE`. Re-invocation is idempotent (rewrites the report against same artifacts) but burns context.
- You want a corpus-wide query (e.g., "show me all retros from the last 30 days"). That's a future `/atlas-retro-trends` skill, not this one.

## Scope (what this skill OWNS)

1. Verifying sprint state is `VERIFIED` or `ROLLED_BACK` (else ABORT with clean error).
2. Invoking `/atlas-learn` via the `Skill` tool (delegation; the leaf does extraction).
3. Computing the sprint scorecard from artifact chain + state file + git history.
4. Computing cross-sprint trend across last 10 completed sprints (when N≥5).
5. Surfacing HIGH-leverage proposals via `AskUserQuestion` for the operator-approval.
6. Writing `07-retro-report.md` (sibling to `07-learn-report.md`).
7. Persisting `retro_state`, `sprint_state`, and approved-proposal IDs to `.atlas-state.json`.
8. Final chat announcement (sprint closed; next-step suggestion).

## Scope (what this skill DOES NOT do)

- **Re-extract lessons or rewrite the drift report** — `/atlas-learn` owns that artifact (`07-learn-report.md`). This skill READS it; it does not regenerate it.
- **Make scope decisions for the next sprint** — surfaces proposals; the operator seals which become memo scope.
- **Modify the Atlas paradigm files directly** — approved HIGH proposals get queued for a separate amendment sprint (Architect → memo → coder edits to skill files). `/atlas-retro` records the approval; it does not edit the harness contract docs or `.claude/skills/atlas-*/SKILL.md`.
- **Skip the operator-approval gate when HIGH proposals exist** — gate is load-bearing; bypassing it defeats the meta-loop.
- **Mark `sprint_state: DONE` before `/atlas-learn` returns OK** — extraction is the prerequisite; DONE without extraction is a contract violation.
- **Run Tester/Ops/Reflect-leaf logic** — those are other skills.
- **Run on more than one sprint at a time** — one invocation = one sprint close.

## File-naming decision (per parent-session CC pick: Option B)

Two layouts considered for the sibling artifact:

| Option | Layout | Outcome |
|---|---|---|
| A | `/atlas-retro` appends retro-framing on top of `/atlas-learn`'s existing `07-learn-report.md` (one artifact) | Simpler; modifies the leaf's output post-hoc; loses clear authorship boundary |
| **B (chosen)** | `/atlas-retro` writes a separate `07-retro-report.md` sibling to `07-learn-report.md` (two artifacts) | Matches gstack's split (`learn` corpus / `retro` periodic analysis); preserves clear authorship; doesn't require modifying `/atlas-learn` |

**Decision: B.** Rationale:
- Clear authorship: `07-learn-report.md` is `/atlas-learn`'s output (raw lessons + drift + proposals); `07-retro-report.md` is `/atlas-retro`'s output (scorecard + trend + approval record).
- Downstream search clarity: future `/atlas-retro-trends` glob (`docs/briefs/*/07-retro-report.md`) yields ONLY retro outputs, not raw learn-reports.
- No mutation of `/atlas-learn` — Atlas conductors compose by chaining, not by patching downstream artifacts.
- Mirrors gstack's `learn` (persistent corpus manager) vs `retro` (periodic snapshot) separation.

The artifact-chain table lists `07-learn-report.md` as `Author: Reflect`; in the Option-B model both `07-learn-report.md` AND `07-retro-report.md` are under the Reflect role — one by the leaf, one by the conductor. The artifact-chain wire-format remains correct; the row enumerates the canonical leaf artifact, and Option B adds a sibling.

## Execution mechanism

This skill dispatches `/atlas-learn` as a **sub-agent via the `Agent` tool**, NOT a chip. `/atlas-learn` returns lessons + drift report + harness-improvement proposals; this conductor adds sprint scorecard + cross-sprint trend + the operator-approval gate.

| Mode | When to use | How |
|---|---|---|
| **`worktree`** | Sub-agent needs file isolation + real branch + opens PR + returns summary | `Agent(subagent_type: "general-purpose", isolation: "worktree", prompt: ...)` |
| **`in-session`** | Sub-agent reads files + summarizes; no isolation needed; lowest latency | `Agent(subagent_type: "general-purpose", prompt: ...)` |
| **`chip`** | the operator wants to monitor long-running work in their IDE | `mcp__ccd_session__spawn_task(...)` |

**Default for Reflect: `in-session`.** **Why:** Retro reads the full `00..06-*.md` artifact chain + computes metrics + writes `07-retro-report.md` — pure read + summarize work. the operator approval at the HIGH-leverage-proposal gate is the only human touchpoint.

**Override:** pass `--mode=<worktree|in-session|chip>` to this skill OR set `.atlas-state.json` `stage_modes.reflect` upstream. Override is persisted for downstream audit (`/atlas-learn` drift report).

## Required prerequisites

| Prerequisite | How verified | If missing |
|---|---|---|
| `.atlas-state.json` exists at `docs/briefs/<sprint-id>/.atlas-state.json` | `jq -e . "$STATE_FILE"` | ABORT — "no sprint to retro" |
| `deploy_state` is `VERIFIED` or `ROLLED_BACK` | `jq -r '.deploy_state'` | ABORT — "sprint not at Ops-Gate verdict; run /atlas-ship-verify first" |
| `00-memo.md` exists | `test -f` | ABORT — "memo missing; sprint state is inconsistent" |
| `06-verify-report.md` exists | `test -f` | WARN — Ops Gate may have skipped report; continue with reduced scorecard fidelity |
| Lessons directory writable | `[ -w "$LESSONS_DIR" ]` | ABORT — `/atlas-learn` will fail to persist; preempt |

## Sprint scorecard metrics

Computed in Step 3. Target values codify the Atlas success contract.

| Metric | How computed | Target (Tier-1) |
|---|---|---|
| **the operator touchpoints** | `Telegram alerts from /atlas-ship-verify + memo seals + scope-drift halts` | **≤ 1** (the memo seal). Anything more = Tester/Ops contract gap. |
| **Drift count** | Read from `07-learn-report.md` "Drift" line; files touched outside `in_scope_files`/`in_scope_globs` | 0 (drift ≠ 0 = Architect-under-scope OR Coder-discipline gap) |
| **Time-to-deploy** | `verified_at - sealed_at` (from `.atlas-state.json` timestamps) | < 4h Tier-1 (varies; trend is the signal, not absolute) |
| **Second-model BLOCKERs found** | `grep -c '^- \[BLOCKER\]' 04-review-codex.md` | Any > 0 BLOCKER = good catch (justifies the cost); 0 BLOCKERs across many sprints = maybe over-paying for review |
| **/atlas-cso BLOCKERs found** | `grep -c '^- \[BLOCKER\]' 04-review-cso.md` | Same as above |
| **Auto-rollback fired** | `deploy_state == ROLLED_BACK` | NO (rollback = sprint failed verify; not the desired path) |
| **Coder bounces** | Count of `step_log` entries with `event: "coder_loopback"` | 0–1 (≥2 = Architect plan under-specified) |
| **Memo amendments** | `jq '.memo_version // 1' "$STATE_FILE"` minus 1 | 0 (amendment cycle = Architect under-spec OR genuine mid-sprint discovery) |
| **Total cost (USD)** | `jq '[.step_log[].cost_usd // 0] | add' "$STATE_FILE"` | Within tier cost ceiling |

Each metric is recorded in `07-retro-report.md` with raw value + target + status (`✅ MET` / `⚠️ EXCEEDED` / `🚨 REGRESSION`).

## Cross-sprint trend semantics

Computed in Step 4. Only when **N ≥ 5** completed sprints exist (otherwise sample is too small for median to be meaningful; report writes `INSUFFICIENT_DATA` in trend section).

For each scorecard metric:
- Compute the **rolling 10-sprint median** (most-recent 10 sprints with `retro_state: COMPLETE`).
- Compute this-sprint-vs-median:
  - `⬆ better` if this sprint's value is better than median (lower for touchpoints/drift/cost/time; higher for BLOCKERs-caught-when-real)
  - `→ no change` if within ±10%
  - `⬇ worse` otherwise
- Flag a **regression cluster** if ≥3 metrics show `⬇ worse` simultaneously — surfaces in the report as a HIGH-priority observation.

```bash
# Pseudo-implementation
LAST_10_SPRINTS=$(find docs/briefs -name '.atlas-state.json' -exec sh -c '
  jq -r "select(.retro_state == \"COMPLETE\") | [(.sealed_at // .created_at), input_filename] | @tsv" "$1"
' _ {} \; | sort -r | head -10 | cut -f2)

# For each metric, extract historical values + compute median + compare
```

This trend section is the most-visible "is the harness improving over time" signal — it's what justifies the meta-loop investment.

## State machine

```
                        Ops-Gate verdict (VERIFIED or ROLLED_BACK)
                                       │
                                       ▼
                              INIT ─► VERIFY_PREREQ
                                       │
                                       ▼
                                LEARN_INVOKE ──► (delegates to /atlas-learn)
                                       │           │
                                       │           ▼
                                       │      07-learn-report.md
                                       │      + lessons file written
                                       ▼
                                SCORECARD ──► metrics computed
                                       │
                                       ▼
                                TREND ──► (skipped if N<5; INSUFFICIENT_DATA)
                                       │
                                       ▼
                                OPERATOR_APPROVAL ──► (AskUserQuestion on HIGH proposals)
                                       │
                                       ▼
                                WRITE_REPORT ──► 07-retro-report.md
                                       │
                                       ▼
                                STATE_TRANSITION ──► retro_state: COMPLETE
                                                     sprint_state: DONE
                                       │
                                       ▼
                                ANNOUNCE ──► chat suggestion for next sprint
```

`retro_state` transitions persisted to `.atlas-state.json` after every sub-step.

| State | Meaning |
|---|---|
| absent / `null` | retro not yet started for this sprint |
| `IN_PROGRESS` | conductor mid-flight; resume from `current_substep` |
| `WAITING_OPERATOR_APPROVAL` | paused on `AskUserQuestion`; resume by re-invoking |
| `COMPLETE` | retro report written; sprint DONE; no further action |

## Workflow

### Step 0 — Bootstrap

```bash
cd "$(git rev-parse --show-toplevel)"

# Find sprint-id: arg, current branch's sprint, or most-recent verified sprint
SPRINT_ID="${1:-}"
if [ -z "$SPRINT_ID" ]; then
  # Prefer the sprint matching the current branch
  BRANCH=$(git branch --show-current)
  CANDIDATE=$(find docs/briefs -name '.atlas-state.json' -exec sh -c '
    if jq -e --arg b "$2" ".sprint_branch == \$b" "$1" >/dev/null 2>&1; then
      dirname "$1" | xargs basename
    fi
  ' _ {} "$BRANCH" \; | head -1)
  if [ -n "$CANDIDATE" ]; then
    SPRINT_ID="$CANDIDATE"
  else
    # Fallback: most-recent sprint at VERIFIED or ROLLED_BACK
    SPRINT_ID=$(find docs/briefs -name '.atlas-state.json' -exec sh -c '
      state=$(jq -r ".deploy_state" "$1")
      if [ "$state" = "VERIFIED" ] || [ "$state" = "ROLLED_BACK" ]; then
        printf "%s\t%s\n" "$(jq -r ".sealed_at // .created_at" "$1")" "$(dirname "$1" | xargs basename)"
      fi
    ' _ {} \; | sort -r | head -1 | cut -f2)
  fi
fi

[ -z "$SPRINT_ID" ] && { echo "ABORT: no completed sprint found"; exit 1; }

ARTIFACT_DIR="docs/briefs/${SPRINT_ID}"
STATE_FILE="${ARTIFACT_DIR}/.atlas-state.json"
echo "Retro for sprint: $SPRINT_ID"
```

### Step 1 — Verify prerequisite state

```bash
DEPLOY_STATE=$(jq -r '.deploy_state // "null"' "$STATE_FILE")
case "$DEPLOY_STATE" in
  VERIFIED|ROLLED_BACK)
    echo "deploy_state = $DEPLOY_STATE — OK to retro"
    ;;
  *)
    echo "ABORT: deploy_state = $DEPLOY_STATE — sprint not at Ops-Gate verdict."
    echo "Run /atlas-ship-verify first (or wait for it to complete)."
    exit 1
    ;;
esac

# Check artifacts
[ -f "${ARTIFACT_DIR}/00-memo.md" ] || { echo "ABORT: 00-memo.md missing"; exit 1; }
[ -f "${ARTIFACT_DIR}/06-verify-report.md" ] || echo "WARN: 06-verify-report.md missing — reduced scorecard fidelity"

# Idempotency: if already COMPLETE, ask the operator whether to re-run
RETRO_STATE=$(jq -r '.retro_state // "null"' "$STATE_FILE")
if [ "$RETRO_STATE" = "COMPLETE" ]; then
  echo "WARN: retro already COMPLETE for $SPRINT_ID. Re-run is idempotent but burns context."
  # AskUserQuestion: rerun or skip?
fi

# Persist sub-state
jq '.retro_state = "IN_PROGRESS" | .retro_started_at = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' \
  "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"
```

### Step 2 — Invoke /atlas-learn (delegation)

```
Skill(skill: "atlas-learn", args: "sprint_id=<SPRINT_ID>")
```

`/atlas-learn` writes `07-learn-report.md` and a lessons file under your project's lessons directory. Per the leaf's own contract, this includes the drift report, lessons, ranked proposals, and the lessons file path. We READ this output; we do not regenerate any of it.

On `/atlas-learn` failure (skill missing, write error, prerequisite gap it surfaces): HALT, write `retro_state: LEARN_FAILED` to state file, surface to the operator with the skill's exit message.

```bash
LEARN_REPORT="${ARTIFACT_DIR}/07-learn-report.md"
if [ ! -f "$LEARN_REPORT" ]; then
  echo "ABORT: /atlas-learn did not write $LEARN_REPORT — retro cannot proceed"
  jq '.retro_state = "LEARN_FAILED"' "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"
  exit 1
fi
```

### Step 3 — Compute sprint scorecard

```bash
# Read the canonical metrics either from .atlas-state.json or compute fresh
MEMO_SEALS=$(jq -r '.memo_version // 1' "$STATE_FILE")
DEPLOY_STATE=$(jq -r '.deploy_state' "$STATE_FILE")
SEALED_AT=$(jq -r '.sealed_at // ""' "$STATE_FILE")
VERIFIED_AT=$(jq -r '.verified_at // ""' "$STATE_FILE")
TOTAL_COST=$(jq '[.step_log[].cost_usd // 0] | add' "$STATE_FILE")
CODER_BOUNCES=$(jq '[.step_log[] | select(.event == "coder_loopback")] | length' "$STATE_FILE")
TELEGRAM_ALERTS=$(grep -c "Telegram alert" "${ARTIFACT_DIR}"/*.md 2>/dev/null || echo 0)
SCOPE_DRIFT_HALTS=$(grep -l "scope drift" "${ARTIFACT_DIR}"/*.md 2>/dev/null | wc -l | tr -d ' ')

# Reviewer BLOCKER counts
CODEX_BLOCKERS=0
CSO_BLOCKERS=0
[ -f "${ARTIFACT_DIR}/04-review-codex.md" ] && \
  CODEX_BLOCKERS=$(grep -cE '^- \[BLOCKER\]|^\*\*BLOCKER\*\*' "${ARTIFACT_DIR}/04-review-codex.md" || echo 0)
[ -f "${ARTIFACT_DIR}/04-review-cso.md" ] && \
  CSO_BLOCKERS=$(grep -cE '^- \[BLOCKER\]|^\*\*BLOCKER\*\*' "${ARTIFACT_DIR}/04-review-cso.md" || echo 0)

# Drift count — pulled from /atlas-learn's already-computed report
DRIFT_COUNT=$(grep -oE 'Drift \(touched, not planned\): [0-9]+' "$LEARN_REPORT" | grep -oE '[0-9]+' || echo 0)

# Time-to-deploy
if [ -n "$SEALED_AT" ] && [ -n "$VERIFIED_AT" ]; then
  TTD_SEC=$(( $(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$VERIFIED_AT" +%s 2>/dev/null) \
             - $(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$SEALED_AT" +%s 2>/dev/null) ))
  TTD_HRS=$(echo "scale=1; $TTD_SEC / 3600" | bc)
else
  TTD_HRS="n/a"
fi

# the operator touchpoint total
OPERATOR_TOUCHPOINTS=$((MEMO_SEALS + TELEGRAM_ALERTS + SCOPE_DRIFT_HALTS))

# Auto-rollback fired?
AUTO_ROLLBACK="NO"
[ "$DEPLOY_STATE" = "ROLLED_BACK" ] && AUTO_ROLLBACK="YES"
```

### Step 4 — Compute cross-sprint trend (if N≥5)

```bash
COMPLETED_SPRINTS=$(find docs/briefs -name '.atlas-state.json' -exec sh -c '
  jq -e --arg s "$2" "select(.retro_state == \"COMPLETE\" and (.sprint_id // \"\") != $s)" "$1" >/dev/null 2>&1 \
    && dirname "$1" | xargs basename
' _ {} "$SPRINT_ID" \; | sort -u)

N_COMPLETED=$(echo "$COMPLETED_SPRINTS" | grep -cE '.')

if [ "$N_COMPLETED" -lt 5 ]; then
  TREND_SECTION="INSUFFICIENT_DATA ($N_COMPLETED completed sprints; trend requires ≥5)"
else
  # Take most-recent 10 (sorted by sealed_at)
  RECENT_10=$(echo "$COMPLETED_SPRINTS" | tail -10)

  # For each metric, extract historical value, compute median, compare to this sprint
  # (implementation per Step 6 markdown — emit trend rows like:
  #   "the operator touchpoints: this=2 / median=1 / ⬇ worse")

  REGRESSION_COUNT=0
  # Count metrics where this-sprint is worse than median
  # If >= 3, flag REGRESSION_CLUSTER as HIGH-priority observation
fi
```

Cross-sprint trend is the strongest signal for "is the harness self-improving as designed." A single sprint can be noisy; a trend across 10 sprints reveals harness health.

### Step 5 — Surface HIGH-leverage proposals to the operator

Read `07-learn-report.md` and extract proposals classified `HIGH leverage`. Present via `AskUserQuestion`:

```
AskUserQuestion(
  questions: [{
    question: "Sprint <SPRINT_ID> retro complete. <N> HIGH-leverage harness-improvement proposals from /atlas-learn. Approve which to amend into Atlas contract?",
    header: "Harness amend",
    multiSelect: false,  // single-choice routing
    options: [
      { label: "Approve all HIGH",     description: "CC drafts amendments to skill files in next sprint (recommended)" },
      { label: "Approve subset",       description: "the operator names which proposals via free-text" },
      { label: "Defer all to backlog", description: "Proposals queued; no amendment sprint kicked off now" },
      { label: "Reject — none warrant amendment", description: "Proposals do not warrant the harness contract change" }
    ]
  }]
)
```

If the operator is unreachable (autonomous-loop directive scope; rare for retro):
- Default to **Defer all to backlog** — proposals are queued in `next_sprint_proposals` array; surfaced again on next sprint's `/atlas-memo` (NOT amended unilaterally).
- This preserves the operator's reserved authority over paradigm/harness changes.

Per the Atlas convention of always carrying a recommendation on a decision question: the **Approve all HIGH** option is CC's recommendation when HIGH proposals are concrete and well-cited; CC selects this default in the AskUserQuestion ordering (recommended first). If proposals are vague or speculative, CC recommends Defer.

If no HIGH proposals exist: skip the gate (no question to ask). Note "No HIGH proposals this sprint" in the report.

```bash
# Record decision
OPERATOR_DECISION="<from-AskUserQuestion>"
APPROVED_PROPOSAL_IDS="<extracted-from-decision>"

jq --arg d "$OPERATOR_DECISION" --argjson p "$APPROVED_PROPOSAL_IDS" \
  '.retro_state = "OPERATOR_APPROVED" | .tom_amendment_decision = $d | .approved_proposals = $p' \
  "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"
```

### Step 6 — Write 07-retro-report.md

```bash
RETRO_REPORT="${ARTIFACT_DIR}/07-retro-report.md"
cat > "$RETRO_REPORT" <<EOF
# /atlas-retro — Sprint $SPRINT_ID — $(date -u +%Y-%m-%dT%H:%M:%SZ)

**Author:** Reflect stage-conductor (/atlas-retro)
**Sibling:** [07-learn-report.md](07-learn-report.md) (authored by /atlas-learn)
**Sprint outcome:** $DEPLOY_STATE
**Sprint state after retro:** DONE

---

## 1. Sprint scorecard

| Metric | Value | Target (Tier-1) | Status |
|---|---|---|---|
| the operator touchpoints | $OPERATOR_TOUCHPOINTS | ≤ 1 | $([ "$OPERATOR_TOUCHPOINTS" -le 1 ] && echo "✅ MET" || echo "⚠️ EXCEEDED") |
| Drift count (files touched outside IN-SCOPE) | $DRIFT_COUNT | 0 | $([ "$DRIFT_COUNT" -eq 0 ] && echo "✅ MET" || echo "⚠️ EXCEEDED") |
| Time-to-deploy (memo seal → verified) | ${TTD_HRS}h | < 4h | (interpret in context) |
| Second-model BLOCKERs found | $CODEX_BLOCKERS | n/a (any > 0 = good catch) | informational |
| /atlas-cso BLOCKERs found | $CSO_BLOCKERS | n/a (any > 0 = good catch) | informational |
| Auto-rollback fired | $AUTO_ROLLBACK | NO | $([ "$AUTO_ROLLBACK" = "NO" ] && echo "✅ MET" || echo "🚨 REGRESSION") |
| Coder bounces | $CODER_BOUNCES | 0–1 | $([ "$CODER_BOUNCES" -le 1 ] && echo "✅ MET" || echo "⚠️ EXCEEDED") |
| Memo amendments | $((MEMO_SEALS - 1)) | 0 | $([ "$MEMO_SEALS" -le 1 ] && echo "✅ MET" || echo "⚠️ EXCEEDED") |
| Total cost (USD) | \$$TOTAL_COST | within tier ceiling | informational |

## 2. Cross-sprint trend

$TREND_SECTION

(If INSUFFICIENT_DATA, this section will populate once N≥5 completed sprints exist.)

<!-- When populated, format as:

| Metric | This sprint | Median (last 10) | Trend |
|---|---|---|---|
| the operator touchpoints | $OPERATOR_TOUCHPOINTS | <median> | ⬆ better / → no change / ⬇ worse |
| ... | ... | ... | ... |

Regression cluster: <YES/NO — if ≥3 metrics regressed simultaneously, surface as HIGH-priority observation>

-->

## 3. /atlas-learn outputs (delegated)

For raw lesson extraction, drift breakdown, proposal list:
→ **[07-learn-report.md](07-learn-report.md)**

Lessons file written by /atlas-learn:
→ \`<lessons-dir>/<slug>.md\`

## 4. the operator amendment decision

**Decision:** $OPERATOR_DECISION

**Approved proposals (queued for next sprint memo):**

$(if [ -n "$APPROVED_PROPOSAL_IDS" ] && [ "$APPROVED_PROPOSAL_IDS" != "null" ] && [ "$APPROVED_PROPOSAL_IDS" != "[]" ]; then
  echo "$APPROVED_PROPOSAL_IDS" | jq -r '.[] | "- \(.)"'
else
  echo "_None approved (see decision above)._"
fi)

## 5. Next-sprint kickoff suggestion

$(if [ "$OPERATOR_DECISION" = "Approve all HIGH" ] || [ "$OPERATOR_DECISION" = "Approve subset" ]; then
  echo "**Recommended:** Kick off harness-amendment sprint via \`/atlas-autoplan\`. Approved proposals seed the new sprint's memo as IN-SCOPE bullets."
elif [ "$OPERATOR_DECISION" = "Defer all to backlog" ]; then
  echo "**Queued:** Approved-but-deferred proposals will resurface on next \`/atlas-memo\` invocation. Sprint DONE; no follow-up action required tonight."
else
  echo "**Closed:** No amendments. Sprint DONE; no follow-up required."
fi)

## 6. Sprint state transition

\`\`\`
deploy_state:  $DEPLOY_STATE
retro_state:   COMPLETE
sprint_state:  DONE
sealed_at:     $SEALED_AT
verified_at:   $VERIFIED_AT
retro_at:      $(date -u +%Y-%m-%dT%H:%M:%SZ)
\`\`\`

---

*Atlas sprint $SPRINT_ID is DONE. /atlas-retro completes the meta-loop: lessons extracted (→ learn-report), scored (→ this report), surfaced for the operator seal (→ amendment decision), state sealed (→ DONE). Next sprint either amends the harness with approved proposals OR proceeds with backlog-queued proposals visible at next \`/atlas-memo\`.*
EOF
```

### Step 7 — Final state transition + announce

```bash
jq '.retro_state = "COMPLETE"
    | .sprint_state = "DONE"
    | .retro_completed_at = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' \
  "$STATE_FILE" > /tmp/s.json && mv /tmp/s.json "$STATE_FILE"

git add "${ARTIFACT_DIR}/" 2>/dev/null

# Commit only if there are staged changes
if ! git diff --cached --quiet; then
  git commit -m "$(cat <<EOF
atlas(retro): close sprint $SPRINT_ID — $DEPLOY_STATE / $OPERATOR_DECISION

the operator touchpoints: $OPERATOR_TOUCHPOINTS (target ≤1)
Drift: $DRIFT_COUNT files
Time-to-deploy: ${TTD_HRS}h
Auto-rollback: $AUTO_ROLLBACK
the operator amendment decision: $OPERATOR_DECISION
EOF
)"
fi
```

Announce in chat (single concise sentence):

> *"✅ Sprint `<SPRINT_ID>` DONE. Scorecard: <N> the operator-touchpoints (target ≤1), <M> drift, <K>h to deploy. Amendment decision: <OPERATOR_DECISION>. <follow-up suggestion per §5 of retro-report>."*

## the operator approval gate semantics

**Why this gate exists:** harness amendments change the contract every subsequent sprint runs under. The operator's reserved decisions include paradigm changes. `/atlas-learn` produces proposals; `/atlas-retro` is where the operator seals which become the contract.

**Decision routing:**

| the operator decision | Effect on state | Effect on next sprint |
|---|---|---|
| **Approve all HIGH** | `approved_proposals` = all HIGH ids | Next `/atlas-autoplan` kickoff includes them as memo IN-SCOPE bullets; suggested action: kickoff amendment sprint now |
| **Approve subset** | `approved_proposals` = subset the operator named | Same as above; subset only |
| **Defer all to backlog** | `approved_proposals` = []; `deferred_proposals` = all HIGH ids | Resurface on next `/atlas-memo`; the operator sees them again at memo time |
| **Reject** | `rejected_proposals` = all HIGH ids; recorded with rejection reason if the operator provided one | NOT resurfaced on next memo; the operator owns the kill |

**No gate when no HIGH proposals exist.** Recorded in report as "No HIGH proposals this sprint." This is the GOOD signal — the harness produced a clean sprint with no contract-amendable lesson.

**MEDIUM and LOW proposals are NOT gated** at this step. They live in `07-learn-report.md` as backlog; future `/atlas-retro-trends` can surface them when a cluster of MEDIUMs across N sprints justifies promoting to HIGH.

## Failure mode playbook

- **`deploy_state` is not `VERIFIED` / `ROLLED_BACK`** → ABORT with "run /atlas-ship-verify first." Do NOT silently delay; sprint isn't done.
- **`/atlas-learn` Skill invocation fails** → write `retro_state: LEARN_FAILED` to state file; raise to the operator; do NOT attempt to compute scorecard or fabricate proposals.
- **`07-learn-report.md` missing after /atlas-learn returns OK** → state inconsistency; HALT + raise to the operator.
- **AskUserQuestion times out / the operator unreachable** → default to `Defer all to backlog`; do NOT auto-approve (the operator's reserved authority).
- **Idempotency re-run** (retro already COMPLETE) → warn; ask whether to re-run; default to skip.
- **Git commit fails** → state and report files are still written; surface the commit error; the operator can `git add` + `git commit` manually.
- **Sprint state file is corrupt JSON** → ABORT with `jq` error; manual repair only (do NOT auto-rewrite).
- **Scorecard metric value missing** (no `sealed_at`, missing reviewer file, etc.) → emit "n/a" in the cell + note the gap in the report; do NOT abort the entire retro.
- **Cross-sprint trend computation errors** (mtime parse fails, corrupted historical state file) → skip the trend section with `TREND_COMPUTATION_FAILED: <reason>`; do NOT abort the retro.
- **the operator selects "Approve subset" but provides no subset** → re-prompt; do NOT default-approve.

## What this skill forbids

- **Re-extracting lessons** — `/atlas-learn` owns extraction; this skill READS its output.
- **Modifying `07-learn-report.md`** — leaf artifact; conductor does not patch.
- **Editing `.claude/skills/atlas-*/SKILL.md` files** — amendments require a separate sprint (Architect → Coder); recording the approval is this skill's scope, not executing it.
- **Editing the harness contract docs** — same as above; rule changes require separate sprint.
- **Auto-approving HIGH proposals** when the operator is unreachable — default to defer, never approve.
- **Skipping the operator-approval gate when HIGH proposals exist** — gate is load-bearing; bypassing defeats the meta-loop.
- **Marking `sprint_state: DONE` before `/atlas-learn` returns OK** — DONE = retro complete; partial DONE is a contract violation.
- **Computing scorecard from `/atlas-learn`'s prose** when the same metric is available from `.atlas-state.json` — state file is the source of truth; report is the derived view.
- **Running on multiple sprints in one invocation** — one invocation = one sprint close. Use `/loop` if you need batch-retro across multiple stale sprints.
- **Running past a HALT signal from `/atlas-learn` or from the operator interruption** — HALT = the operator decision required.
- **Glossing the the operator-touchpoint count** to make the sprint look better — accuracy beats narrative; every avoidable touchpoint is a contract gap.

## Cost discipline

`/atlas-retro` itself is cheap:
- 1 Skill invocation (`/atlas-learn`)
- 1 AskUserQuestion round-trip (only if HIGH proposals exist)
- File reads + writes, no LLM calls beyond /atlas-learn's own cost

**Estimated cost per invocation:** < $5 (mostly /atlas-learn's reading of the artifact chain).

Aggregate sprint cost is reported in the scorecard (sum of all `step_log[].cost_usd`) and compared against the tier ceiling. /atlas-retro does not enforce gates — that's `/atlas-autoplan` / Ops-Gate territory.

## Tier classification

**Tier 3** — pure docs authoring + state transition + the operator-approval gate. No production state change. Same as `/atlas-learn`.

(The sprints `/atlas-retro` closes span Tier 1/2/3; this skill itself is always Tier 3.)

## References

- `.claude/skills/atlas-learn/SKILL.md` (the leaf this conductor wraps)
- `.claude/skills/atlas-autoplan/SKILL.md` (canonical sister stage-conductor pattern)
- gstack reference: `github.com/garrytan/gstack` — `learn/SKILL.md` (corpus manager) + `retro/SKILL.md` (periodic snapshot) — Atlas's split mirrors gstack's
