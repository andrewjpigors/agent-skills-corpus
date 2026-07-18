---
name: atlas-ship-verify
description: |
  Atlas Ops Gate stage-conductor. Runs /atlas-ship → /atlas-deploy →
  /atlas-canary (graceful-degrade if missing) → /atlas-verify with
  auto-rollback default per the operator seal. Reads 05-verify-*.md (Tester
  must be PASS), writes 06-verify-report.md and .atlas-state.json ops_state.
  Mandatory post-deploy verify — "deployed, should work" is NOT a finish line.
  Skipped per the Atlas convention for docs-only / brief-only paths. Use after
  /atlas-qa-all PASS. Failure surface: alert + portal /atlas.
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Skill
  - AskUserQuestion
triggers:
  - atlas-ship-verify
  - ship-verify
  - atlas ship
  - run atlas ops gate
  - ops gate phase
  - deploy and verify
---

# atlas-ship-verify

> **Reference implementation.** The commands below target a Convex + Vercel + Clerk stack as a worked example. Swap in your own deployment name, function names, and paths.

**Atlas Ops Gate stage-conductor.** Mechanical sequencer for the post-Tester deploy chain: `/atlas-ship` → `/atlas-deploy` → `/atlas-canary` → `/atlas-verify`. Closes the "deployed, should work" gap — `/atlas-verify` is the mandatory final gate; auto-rollback on FAIL is default per the operator seal.

## Mission

For an Atlas sprint with Tester PASS recorded, execute the deploy chain:

```
read 05-verify-*.md (Tester PASS required)
       ↓
pre-flight (main up-to-date; PR mergeable; not a docs-only skip path)
       ↓
/atlas-ship (merge sprint PR → main)
       ↓
/atlas-deploy (Convex + Vercel push)
       ↓
/atlas-canary (graceful-degrade — skill not yet scaffolded, log TODO + continue)
       ↓
/atlas-verify (mandatory — built-in auto-rollback on FAIL)
       ↓
write 06-verify-report.md (consolidates the chain, links to /atlas-verify's own report)
update .atlas-state.json (ops_state, deploy_sha, verify_outcome)
       ↓
announce: "Run /atlas-retro to close the sprint" (PASS) OR P0 + Architect loopback (FAIL)
```

State persists across the chain via `docs/briefs/<sprint-id>/.atlas-state.json`. Each transition writes state so a crashed/interrupted session can resume.

## When to invoke

- **Tester PASS recorded** — `.atlas-state.json` `tester_state == "PASS"` AND `docs/briefs/<sprint-id>/05-verify-*.md` exists with PASS verdict.
- **Sprint is Tier 1 or Tier 2** — Tier 3 skips Ops Gate per the Atlas convention (Coder + Tester + Reflect only).
- **Not a docs-only skip path** — touches paths that change production state (NOT `docs/`-only, `_explorers/`, `_review/`, `_verification/`, `scripts/` not yet wired).

**Do NOT invoke when:**
- Tester state ≠ PASS — Ops Gate is downstream of Tester per loop authority.
- Sprint is docs-only / brief-only — Tester verdict IS the final gate; Ops Gate is skipped.
- The PR is not yet mergeable — sub-step 1 will abort, but no point starting.

## Scope (what this skill OWNS)

1. Reading sprint state — `docs/briefs/<sprint-id>/.atlas-state.json` + `05-verify-*.md`.
2. Pre-flight checks — main is up-to-date, sprint PR is mergeable, docs-only-skip detection.
3. Sequencing the four sub-stages: `/atlas-ship` → `/atlas-deploy` → `/atlas-canary` (graceful-degrade) → `/atlas-verify` (mandatory).
4. Threading deploy SHA + sprint-id forward through the chain.
5. Writing the consolidated `06-verify-report.md` (links out to `/atlas-verify`'s own per-criterion report; this skill's report is the chain-level summary).
6. Updating `.atlas-state.json` (`ops_state`, `deploy_sha`, `verify_outcome`).
7. Honoring the auto-rollback policy default + per-PR `.no_auto_rollback` override.
8. Graceful-degrading when `/atlas-canary` (Phase 2 skill) doesn't yet exist — log TODO + continue with full-rollout.
9. Announcing the next stage (`/atlas-retro` on PASS) or routing the FAIL escalation (P0 file + Architect loopback).

## Scope (what this skill DOES NOT do)

- **Modify application code.** Coder territory.
- **Bypass pre-deploy gates from Tester or Reviewer.** Sprint must show Tester PASS first.
- **Ship without an apply/revert pair when the change touches production state.** Auto-rollback is built into `/atlas-verify`; this skill respects it.
- **Treat "deployed, should work" as a finish line.** `/atlas-verify` runs unconditionally on production state changes; success requires the verify-PASS row, not just deploy-completed.
- **Skip Ops Gate when production state IS touched.** The skip is for docs-only paths; if the diff touches `apps/`, `services/`, runtime config, etc., this skill runs the full chain.
- **Execute Retro work.** Hands off to `/atlas-retro` via state transition + chat announcement.
- **Run inside the worktree where Coder built the change.** Run from main checkout after PR merge.

## Execution mechanism

This skill dispatches `/atlas-ship`, `/atlas-deploy`, `/atlas-canary` (when present), and `/atlas-verify` as **sub-agents via the `Agent` tool**, NOT chips. Sub-agents return deploy + verify outcomes to this conductor.

| Mode | When to use | How |
|---|---|---|
| **`worktree`** | Sub-agent needs file isolation + real branch + opens PR + returns summary | `Agent(subagent_type: "general-purpose", isolation: "worktree", prompt: ...)` |
| **`in-session`** | Sub-agent reads files + summarizes; no isolation needed; lowest latency | `Agent(subagent_type: "general-purpose", prompt: ...)` |
| **`chip`** | the operator wants to monitor long-running work in his IDE | `mcp__ccd_session__spawn_task(...)` |

**Default for Ops Gate: `in-session`** (each sub-step as a sub-agent, run sequentially). **Why:** Ops Gate runs against `main` after PR merge — deploy + verify probes operate on the already-merged code; no worktree isolation needed. Auto-rollback (the operator seal) inherits from `/atlas-verify`'s built-in behavior regardless of mode.

**the operator-oversight special case — chip for irreversible deploys:** for irreversible production changes (DB migrations, customer-facing comms), the operator may want to monitor the deploy step explicitly. Set `stage_modes.ops_gate = "chip"` in the sprint state to spawn a chip the operator can watch.

**Override:** pass `--mode=<worktree|in-session|chip>` to this skill OR set `.atlas-state.json` `stage_modes.ops_gate` upstream. Override is persisted for downstream audit (`/atlas-learn` drift report).

Per the Atlas convention for stage-conductor execution mechanism (Agent-tool dispatch over chips).

## Required prerequisites

**Upstream artifacts:**
- `docs/briefs/<sprint-id>/.atlas-state.json` with `tester_state == "PASS"`
- `docs/briefs/<sprint-id>/05-verify-*.md` (at least one PASS verdict file)
- Sprint PR open, mergeable, with branch-protection checks green

**Downstream skills this orchestrator invokes:**

| Sub-stage | Skill | Status |
|---|---|---|
| 1 | `/atlas-ship` (merge sprint PR → main) | **EXISTS** at `.claude/skills/atlas-ship/SKILL.md`. Squash-merge ceremony |
| 2 | `/atlas-deploy` (Convex + Vercel push) | **EXISTS** at `.claude/skills/atlas-deploy/SKILL.md` |
| 3 | `/atlas-canary` (gradual rollout) | **EXISTS** at `.claude/skills/atlas-canary/SKILL.md`. Vercel+Convex watch-period model — honest about no native traffic-splitting |
| 4 | `/atlas-verify` (post-deploy probes against live deployment) | **EXISTS** at `.claude/skills/atlas-verify/SKILL.md`. Built-in auto-rollback per the operator seal. **MANDATORY** — never skipped |

When a graceful-degradation sub-stage skill is missing, this conductor MUST:
1. Log `WARNING: sub-stage skill <name> not yet scaffolded — graceful-degrading` to chat.
2. Write `sub_stage_<N>: { state: "TODO_MISSING_SKILL", skill: "<name>" }` into `.atlas-state.json`.
3. Continue to the next sub-stage.

**`/atlas-verify` is the exception** — it is mandatory and MUST exist. If it doesn't, this skill HARD ABORTS with "Ops Gate requires /atlas-verify scaffold — author the skill before running ship-verify."

## Docs-only skip rule (when Ops Gate is bypassed entirely)

Per the Atlas convention, Ops Gate is SKIPPED for:

- ADR-only changes (`docs/decisions/`)
- Doc-only changes (`docs/`)
- `_explorers/` / `_review/` / `_verification/` paths
- `scripts/` paths not yet wired into deployment

**Detection:** at pre-flight, parse `git diff main..HEAD --name-only` (run on the sprint PR's head SHA). If EVERY changed path matches a Q3-skip glob, this skill aborts cleanly:

```
Q3-SKIP — sprint <sprint-id> changes docs-only / brief-only paths.
Tester verdict is the final gate for this sprint class.
Marking ops_state = "SKIPPED_Q3" and exiting.
Run /atlas-retro to close.
```

`.atlas-state.json` is updated with `ops_state: "SKIPPED_Q3"`. The verify report is NOT written (no deploy happened). `/atlas-retro` reads the SKIPPED_Q3 marker and skips its own deploy-related sections.

## Auto-rollback policy (the operator seal)

Per the Atlas convention + `/atlas-verify` Step 7:

- **Default: auto-rollback on `/atlas-verify` FAIL.** This is built into `/atlas-verify` itself (the leaf skill) — this conductor inherits the behavior by invoking `/atlas-verify`. Prod-broken > inconvenience-of-rollback.
- **Override: per-PR `.no_auto_rollback: true` in `.atlas-state.json`** for irreversible changes (DB migrations, customer-facing comms, ANY state mutation that can't be unwound by reverting a commit). The Architect seals this flag at memo-time; this skill respects whatever is in `.atlas-state.json` and does NOT toggle it.
- **On FAIL with auto-rollback:** `/atlas-verify` executes the revert + re-deploy, writes the P0 incident file at `docs/incidents/p0-<date>-<sprint-id>.md`, sends the operator alert (Phase 2 — stub in Phase 1). This conductor reads the FAIL verdict + announces Architect loopback.
- **On FAIL with `.no_auto_rollback: true`:** `/atlas-verify` produces FAIL + alert-and-hold; this conductor surfaces the verdict to the operator via `AskUserQuestion` (manual rollback / hold / re-verify).

## State machine

```
INIT ─► PREFLIGHT ─► (Q3_SKIP?) ──► ABORT_CLEAN
            │
            ▼  (no — production state changes)
        SHIPPING ─► DEPLOYING ─► CANARY ─► VERIFYING ──► (verdict?)
                                                          │
                                ┌─────────────────────────┤
                                ▼                         ▼
                            PASS                       FAIL
                                │                         │
                                ▼                         ▼
                          REPORTING               (auto-rollback?)
                                │                  │            │
                                ▼                 yes           no
                            COMPLETED              │            │
                                                   ▼            ▼
                                            ROLLED_BACK    HOLD_FOR_OPERATOR
                                                   │            │
                                                   ▼            ▼
                                            P0_FILED      AWAIT_DECISION
```

State persisted to `.atlas-state.json` after every transition.

**Transition rules:**

| From | Trigger | To |
|---|---|---|
| INIT | invoked, sprint state read | PREFLIGHT |
| PREFLIGHT | all changed paths match Q3-skip globs | ABORT_CLEAN (`ops_state: "SKIPPED_Q3"`) |
| PREFLIGHT | production state changes detected | SHIPPING |
| PREFLIGHT | main is stale / PR not mergeable / Tester state ≠ PASS | HALT + raise to the operator |
| SHIPPING | `gh pr merge` (or `/atlas-ship` if scaffolded) returns OK | DEPLOYING |
| DEPLOYING | `atlas-deploy` returns OK + deploy SHA captured | CANARY |
| CANARY | `/atlas-canary` returns OK | VERIFYING |
| CANARY | `/atlas-canary` skill missing | VERIFYING (graceful-degrade with TODO marker) |
| VERIFYING | `/atlas-verify` returns PASS | REPORTING (PASS) |
| VERIFYING | `/atlas-verify` returns FAIL + auto-rollback executed | ROLLED_BACK → P0_FILED |
| VERIFYING | `/atlas-verify` returns FAIL + `.no_auto_rollback` set | HOLD_FOR_OPERATOR |
| any | unrecoverable error from sub-stage | HALT + raise to the operator |

`HALT + raise to the operator` per the Atlas loop-authority convention. Ops Gate never retries past a HALT signal.

## Workflow

### Step 0 — Bootstrap + read sprint state

```bash
cd "$(git rev-parse --show-toplevel)"

# Find the active sprint state file
SPRINT_STATE=$(find docs/briefs -name '.atlas-state.json' -newer docs/briefs/.created 2>/dev/null | head -1)
[ -z "$SPRINT_STATE" ] && SPRINT_STATE=$(ls -t docs/briefs/*/.atlas-state.json 2>/dev/null | head -1)

if [ -z "$SPRINT_STATE" ]; then
  echo "ABORT: no .atlas-state.json found under docs/briefs/. Run Architect (/atlas-autoplan) first."
  exit 1
fi

SPRINT_ID=$(jq -r '.sprint_id' "$SPRINT_STATE")
SPRINT_DIR="docs/briefs/${SPRINT_ID}"
echo "Sprint: $SPRINT_ID"
echo "State file: $SPRINT_STATE"

# Gate on Tester state
TESTER_STATE=$(jq -r '.tester_state // "UNKNOWN"' "$SPRINT_STATE")
if [ "$TESTER_STATE" != "PASS" ]; then
  echo "ABORT: tester_state is '$TESTER_STATE' (expected PASS)."
  echo "Run /atlas-qa-all first; Ops Gate is downstream of Tester."
  exit 1
fi

# Confirm at least one Tester report exists
VERIFY_FILES=$(ls "${SPRINT_DIR}"/05-verify-*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$VERIFY_FILES" -eq 0 ]; then
  echo "ABORT: no 05-verify-*.md files in $SPRINT_DIR (Tester contract violation — should have at least one)."
  exit 1
fi
echo "Tester reports: $VERIFY_FILES file(s)"

# Capture PR number from sprint state
PR_NUMBER=$(jq -r '.pr_number // empty' "$SPRINT_STATE")
if [ -z "$PR_NUMBER" ]; then
  # Try to derive from current branch's open PR
  BRANCH=$(git branch --show-current)
  PR_NUMBER=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number' 2>/dev/null)
fi

if [ -z "$PR_NUMBER" ]; then
  echo "ABORT: no PR number in sprint state and no open PR for current branch. Architect must record pr_number in .atlas-state.json."
  exit 1
fi
echo "Sprint PR: #$PR_NUMBER"

# Transition INIT → PREFLIGHT
jq --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   '.ops_state = "PREFLIGHT" | .ops_started_at = $now | .current_role = "ops_gate"' \
   "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
```

### Step 1 — Pre-flight checks (Q3-skip detection + mergeability)

```bash
# Fetch latest main
git fetch origin main --quiet

# Get the PR head SHA + check mergeable status
PR_INFO=$(gh pr view "$PR_NUMBER" --json mergeable,mergeStateStatus,headRefOid,baseRefName)
PR_HEAD=$(echo "$PR_INFO" | jq -r '.headRefOid')
PR_MERGEABLE=$(echo "$PR_INFO" | jq -r '.mergeable')
PR_MERGE_STATE=$(echo "$PR_INFO" | jq -r '.mergeStateStatus')
PR_BASE=$(echo "$PR_INFO" | jq -r '.baseRefName')

echo "PR head: $PR_HEAD"
echo "Mergeable: $PR_MERGEABLE / $PR_MERGE_STATE"
echo "Base branch: $PR_BASE"

if [ "$PR_BASE" != "main" ]; then
  echo "ABORT: PR base is '$PR_BASE' (expected 'main'). Ops Gate only runs on main-targeted PRs."
  exit 1
fi

if [ "$PR_MERGEABLE" != "MERGEABLE" ]; then
  echo "ABORT: PR #$PR_NUMBER is $PR_MERGEABLE / $PR_MERGE_STATE. Resolve conflicts or wait for checks."
  exit 1
fi

# Q3-skip detection — list every file changed by the PR
CHANGED_FILES=$(gh pr diff "$PR_NUMBER" --name-only)
echo "Changed files: $(echo "$CHANGED_FILES" | wc -l | tr -d ' ')"

# Docs-only skip globs per the Atlas convention
# (egrep is OR-pattern; if EVERY file matches, the whole sprint is a docs-only skip)
SKIP_PATTERN='^(docs/|_explorers/|_review/|_verification/|scripts/)'
NON_SKIP_FILES=$(echo "$CHANGED_FILES" | grep -vE "$SKIP_PATTERN" || true)

if [ -z "$NON_SKIP_FILES" ] && [ -n "$CHANGED_FILES" ]; then
  # All changed paths are docs / explorers / review / verification / scripts
  # → Q3-skip; Tester is final gate
  echo "Q3-SKIP — sprint $SPRINT_ID changes docs-only / brief-only paths."
  echo "Tester verdict is the final gate for this sprint class."

  jq --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.ops_state = "SKIPPED_Q3" | .ops_completed_at = $now' \
     "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"

  git add "$SPRINT_STATE"
  git commit -m "atlas(ship-verify): SKIPPED_Q3 — ${SPRINT_ID} is docs-only" || true

  echo ""
  echo "✅ Ops Gate skipped (docs-only). Run /atlas-retro to close."
  exit 0
fi

echo "Production state changes detected — full Ops Gate chain will run."
echo "Non-skip files: $(echo "$NON_SKIP_FILES" | wc -l | tr -d ' ')"

# Transition PREFLIGHT → SHIPPING
jq '.ops_state = "SHIPPING"' "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
```

### Step 2 — `/atlas-ship` sub-stage (merge PR → main)

Prefer the `/atlas-ship` leaf (`Skill(skill: "atlas-ship", args: "pr=$PR_NUMBER")`), which adds the four-gate pre-flight + audit-trail state write. Inline fallback when the leaf is unavailable:

```bash
echo ""
echo "=== Sub-stage 1/4: SHIP (merge PR #$PR_NUMBER → main) ==="

# Squash-merge with branch deletion
gh pr merge "$PR_NUMBER" --squash --delete-branch --auto 2>&1
MERGE_EXIT=$?

if [ $MERGE_EXIT -ne 0 ]; then
  echo "ABORT: gh pr merge exited $MERGE_EXIT. Resolve manually."
  jq --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.ops_state = "HALT_SHIP_FAILED" | .ops_halted_at = $now' \
     "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
  exit 1
fi

# Pull main to capture the merge SHA
git checkout main
git pull origin main --ff-only
MERGE_SHA=$(git rev-parse HEAD)
echo "Merged. SHA on main: $MERGE_SHA"

jq --arg sha "$MERGE_SHA" --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   '.ops_state = "DEPLOYING" | .merge_sha = $sha | .shipped_at = $now' \
   "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
```

### Step 3 — `atlas-deploy` sub-stage (Convex + Vercel push)

```bash
echo ""
echo "=== Sub-stage 2/4: DEPLOY (Convex prod:your-deployment + Vercel) ==="
```

Invoke the deploy skill via the `Skill` tool:

```
Skill(skill: "atlas-deploy", args: "auto-confirm=true sprint_id=<sprint_id>")
```

`/atlas-deploy` runs Convex push + Vercel verify + smoke test; it captures its own report.

Post-skill, read the result back:

```bash
DEPLOY_EXIT=$?  # The Skill tool returns the leaf skill's verdict
DEPLOY_SHA=$(git rev-parse HEAD)  # Should match MERGE_SHA

if [ $DEPLOY_EXIT -ne 0 ]; then
  echo "ABORT: atlas-deploy failed. Investigate before re-running."
  jq --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.ops_state = "HALT_DEPLOY_FAILED" | .ops_halted_at = $now' \
     "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
  echo ""
  echo "❌ Deploy failed. Sprint state HALT_DEPLOY_FAILED. the operator decides re-deploy vs rollback."
  exit 1
fi

jq --arg sha "$DEPLOY_SHA" --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   '.ops_state = "CANARY" | .deploy_sha = $sha | .deployed_at = $now | .deploy_state = "DEPLOYED"' \
   "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
```

### Step 4 — `/atlas-canary` sub-stage (graceful-degrade)

```bash
echo ""
echo "=== Sub-stage 3/4: CANARY (gradual rollout cohort) ==="

# Check if /atlas-canary skill exists
if [ -f ".claude/skills/atlas-canary/SKILL.md" ]; then
  # Invoke via Skill tool (when scaffolded)
  # Skill(skill: "atlas-canary", args: "sprint_id=<sprint_id> deploy_sha=$DEPLOY_SHA")
  CANARY_EXIT=$?
  echo "Canary verdict: $([ $CANARY_EXIT -eq 0 ] && echo OK || echo FAIL)"
else
  echo "GRACEFUL DEGRADATION: /atlas-canary not yet scaffolded (Phase 2 chip)."
  echo "Continuing with FULL-ROLLOUT (no canary cohort)."

  # Log TODO marker per graceful-degradation contract
  jq '.sub_stage_canary = { state: "TODO_MISSING_SKILL", skill: "atlas-canary", note: "Phase 2 chip — full-rollout used" }' \
     "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
fi

jq '.ops_state = "VERIFYING"' "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
```

### Step 5 — `/atlas-verify` sub-stage (MANDATORY)

```bash
echo ""
echo "=== Sub-stage 4/4: VERIFY (probes against LIVE deployment) ==="
echo "Auto-rollback policy: $(jq -r '.no_auto_rollback // false' "$SPRINT_STATE" | sed 's/true/DISABLED (per memo seal)/;s/false/ENABLED (default)/')"

# /atlas-verify is mandatory. Hard abort if missing.
if [ ! -f ".claude/skills/atlas-verify/SKILL.md" ]; then
  echo "HARD ABORT: /atlas-verify is mandatory. Author the skill before running ship-verify."
  jq --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.ops_state = "HALT_NO_VERIFY_SKILL" | .ops_halted_at = $now' \
     "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
  exit 1
fi
```

Invoke `/atlas-verify`:

```
Skill(skill: "atlas-verify", args: "sprint_id=<sprint_id>")
```

`/atlas-verify` does the heavy lifting:
- Confirms deploy landed (Convex function-spec + Vercel status)
- Runs memo SUCCESS CRITERIA probes (via `/atlas-probe`, `/atlas-browse`, `/atlas-browser-cookies`, `/atlas-investigate`)
- Cost-regression smoke check
- On FAIL + auto-rollback enabled: executes the revert + re-deploy + writes P0 file + operator alert (Phase 1 stub)
- On FAIL + auto-rollback disabled: alert-and-hold
- Writes its own per-criterion report at `06-verify-report.md` (NOTE: this conductor and `/atlas-verify` BOTH target the same file; conductor wraps and links if needed — see Step 6)

Read the verdict back from `.atlas-state.json` (which `/atlas-verify` updated):

```bash
VERIFY_OUTCOME=$(jq -r '.deploy_state // "UNKNOWN"' "$SPRINT_STATE")
# /atlas-verify sets deploy_state to one of:
#   VERIFIED       — all criteria PASS
#   VERIFIED_ALERT — criteria PASS but cost-regression suspect
#   ROLLED_BACK    — FAIL + auto-rollback executed
#   HOLD_FOR_OPERATOR   — FAIL + auto-rollback disabled (alert-and-hold)
#   FAILED_DEPLOY  — verify itself failed to run (e.g., deploy didn't land)

echo "Verify outcome: $VERIFY_OUTCOME"

jq --arg outcome "$VERIFY_OUTCOME" \
   '.verify_outcome = $outcome' \
   "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"
```

### Step 6 — Write conductor-level `06-verify-report.md` summary

`/atlas-verify` writes its own per-criterion report; this conductor writes a chain-level summary that consolidates the sub-stages. If `/atlas-verify` already wrote `06-verify-report.md`, this conductor's summary is prepended with a `## Ops Gate chain summary` section above the existing content. (Implementation: read existing file, prepend, write back.)

```bash
SUMMARY_BLOCK=$(cat <<EOF
# /atlas-ship-verify — Sprint ${SPRINT_ID} — $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Ops Gate chain summary

| Sub-stage | Result | Notes |
|---|---|---|
| Pre-flight | PASS | $(echo "$NON_SKIP_FILES" | wc -l | tr -d ' ') non-skip file(s) changed |
| /atlas-ship | OK | PR #${PR_NUMBER} squash-merged → ${MERGE_SHA} |
| /atlas-deploy | OK | Convex pushed to your-deployment + Vercel auto-deployed |
| /atlas-canary | $(jq -r '.sub_stage_canary.state // "OK"' "$SPRINT_STATE") | $(jq -r '.sub_stage_canary.note // "ran successfully"' "$SPRINT_STATE") |
| /atlas-verify | ${VERIFY_OUTCOME} | See per-criterion detail below |

## Deploy metadata
- **PR:** #${PR_NUMBER}
- **Merge SHA:** ${MERGE_SHA}
- **Deploy SHA:** ${DEPLOY_SHA}
- **Auto-rollback policy:** $(jq -r '.no_auto_rollback // false' "$SPRINT_STATE" | sed 's/true/DISABLED/;s/false/ENABLED/')

## Next action
$(case "$VERIFY_OUTCOME" in
   VERIFIED|VERIFIED_ALERT) echo "✅ Sprint Done — run \`/atlas-retro\` to close." ;;
   ROLLED_BACK) echo "❌ FAIL — auto-rolled-back. Architect loopback for root-cause. P0 file at docs/incidents/" ;;
   HOLD_FOR_OPERATOR) echo "⚠️ FAIL — alert-and-hold. the operator decision required (manual rollback / hold / re-verify)." ;;
   *) echo "INCONCLUSIVE — investigate \`.atlas-state.json\` and verify-report." ;;
 esac)

---

EOF
)

REPORT_FILE="${SPRINT_DIR}/06-verify-report.md"
if [ -f "$REPORT_FILE" ]; then
  # /atlas-verify already wrote its per-criterion report; prepend our summary
  EXISTING=$(cat "$REPORT_FILE")
  echo "$SUMMARY_BLOCK" > "$REPORT_FILE"
  echo "$EXISTING" >> "$REPORT_FILE"
else
  # /atlas-verify didn't write (likely docs-only skip or HALT path — shouldn't happen here)
  echo "$SUMMARY_BLOCK" > "$REPORT_FILE"
fi
```

### Step 7 — Final state transition + commit

```bash
case "$VERIFY_OUTCOME" in
  VERIFIED|VERIFIED_ALERT)
    FINAL_STATE="COMPLETED"
    ;;
  ROLLED_BACK)
    FINAL_STATE="ROLLED_BACK"
    ;;
  HOLD_FOR_OPERATOR)
    FINAL_STATE="HOLD_FOR_OPERATOR"
    ;;
  *)
    FINAL_STATE="INCONCLUSIVE"
    ;;
esac

jq --arg state "$FINAL_STATE" --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   '.ops_state = $state | .ops_completed_at = $now | .current_role = "reflect"' \
   "$SPRINT_STATE" > /tmp/state.json && mv /tmp/state.json "$SPRINT_STATE"

git add "$REPORT_FILE" "$SPRINT_STATE"
git commit -m "$(cat <<EOF
atlas(ship-verify): ${VERIFY_OUTCOME} — sprint ${SPRINT_ID}

- PR #${PR_NUMBER} merged to ${MERGE_SHA}
- Deployed Convex prod + Vercel
- /atlas-verify verdict: ${VERIFY_OUTCOME}
- Next: $([ "$FINAL_STATE" = "COMPLETED" ] && echo "/atlas-retro" || echo "Architect loopback")
EOF
)"
git push origin main
```

### Step 8 — Announce next stage

Tight chat summary:

```
=== /atlas-ship-verify summary — sprint <sprint_id> ===

Result: ✅ COMPLETED  |  ❌ ROLLED_BACK  |  ⚠️ HOLD_FOR_OPERATOR
PR: #<n> merged → <sha>
Deploy: Convex your-deployment + Vercel
Verify: <outcome>

<one of:>
✅ Ops Gate PASS. Run /atlas-retro to close the sprint.
❌ /atlas-verify FAIL — auto-rolled-back to <prior-sha>; operator alert sent; P0 file at docs/incidents/p0-<date>-<sprint-id>.md. Loop back to Architect for root-cause.
⚠️ /atlas-verify FAIL — auto-rollback DISABLED per memo; the operator decision required.
```

## Loop authority

Per the Atlas loop-authority convention:

| Trigger | This skill does |
|---|---|
| Tester state ≠ PASS | ABORT at Step 0 with "run /atlas-qa-all first" |
| PR not mergeable | ABORT at Step 1 |
| Q3-skip globs match all files | ABORT cleanly with `ops_state: "SKIPPED_Q3"` |
| `/ship` (gh pr merge) fails | HALT + raise to the operator — do not auto-retry; conflicts/protections need human |
| `atlas-deploy` fails | HALT + raise to the operator — `ops_state: "HALT_DEPLOY_FAILED"` |
| `/atlas-canary` missing | Graceful-degrade with TODO marker; continue |
| `/atlas-canary` fails (when scaffolded) | HALT + raise to the operator (canary FAIL is a deploy-class signal) |
| `/atlas-verify` returns FAIL + auto-rollback enabled | `/atlas-verify` handles rollback + P0 + alert; this skill announces Architect loopback |
| `/atlas-verify` returns FAIL + `.no_auto_rollback` set | This skill surfaces to the operator via `AskUserQuestion` |
| `/atlas-verify` skill missing | HARD ABORT — verify is mandatory |
| Auto-rollback itself fails | Escalate to the operator IMMEDIATELY — prod is in unknown state (handled inside `/atlas-verify`) |

## Failure mode playbook

- **Sprint state file missing.** Architect (`/atlas-autoplan`) didn't run; ABORT and tell the operator to start at Architect.
- **Multiple sprints have recent state files.** Pick the one matching the current branch's open PR; if ambiguous, ABORT with "specify sprint_id explicitly via arg."
- **PR is mergeable but branch-protection check is pending.** Wait at most 60s, re-check; if still pending, surface to the operator — don't auto-merge while checks are running.
- **`gh pr merge --auto` enabled and merges happen later.** This skill is designed for synchronous merge; if `--auto` is enabled in repo settings, `gh pr merge` returns immediately with "queued." Detect this and either (a) poll for actual merge or (b) ABORT with "auto-merge enabled — use manual `/atlas-deploy` after merge lands."
- **Convex deploy throws "non-interactive terminal" error.** `CONVEX_DEPLOY_KEY` missing on this machine; `atlas-deploy` already handles this — surface its error verbatim.
- **`/atlas-verify` runs but doesn't update sprint state file.** Bug in `/atlas-verify`; surface to the operator + don't claim PASS. `ops_state` stays at `VERIFYING` until manually resolved.
- **`/atlas-verify` PASSES but the operator reports broken in next hour.** Tester contract gap — memo's SUCCESS CRITERIA were under-specified. `/atlas-learn` writes this up as a Tester-contract improvement proposal.
- **Auto-rollback itself fails.** Most severe failure. `/atlas-verify` handles internally — escalate to the operator IMMEDIATELY via the operator alert channel (Phase 1 stub) + log to incident file + abort.
- **Cost-regression detected post-deploy.** `/atlas-verify` produces `VERIFIED_ALERT` — this conductor surfaces but does NOT rollback (cost alone isn't a rollback trigger; could be expected for a new feature).
- **Concurrent invocation in same sprint.** Detected via `.atlas-state.json` `ops_state` already in `SHIPPING` / `DEPLOYING` / `VERIFYING`; later invocation logs warning + exits without re-running.
- **State file write fails (disk full, permission).** HARD ABORT. State persistence is load-bearing; without it the chain can't safely resume.

## What this skill forbids

- **Skipping `/atlas-verify`.** Mandatory. Hard abort if the skill file is missing rather than silently proceeding.
- **"Deployed, should work" as a finish line.** Mechanically forbidden — `ops_state` does NOT transition to `COMPLETED` until `/atlas-verify` returns PASS.
- **Toggling `.no_auto_rollback` mid-flight.** That flag is Architect-owned at memo-time; this skill respects whatever the sprint state has and does not mutate.
- **Auto-retrying past a HALT signal.** HALT = the operator decision required.
- **Running outside an Atlas sprint** (no `.atlas-state.json` → ABORT Step 0).
- **Advancing past `tester_state ≠ PASS`.** Tester is the upstream gate; Ops Gate never bypasses it.
- **Modifying application code.** Coder territory. If Ops Gate finds a bug, it goes back to Architect via memo amendment, not patched here.
- **Suppressing the rollback when policy is auto-rollback.** Override requires the `.no_auto_rollback` flag in `.atlas-state.json`, sealed by Architect at memo time.
- **Marking sprint COMPLETED without writing `06-verify-report.md`.**
- **Skipping the docs-only skip detection.** If the diff is docs-only, Ops Gate ABORTS cleanly with `SKIPPED_Q3`; never invents a deploy for docs-only sprints.

## Cost discipline (per the Atlas convention)

This skill is orchestration only — the cost ceiling is whatever the chain runs:

| Tier | Cost ceiling on this skill's invocation chain |
|---|---|
| 1 | $200 alert; $300/$500/$800/$1000 hard gates (full chain including `/atlas-verify` cost regression check) |
| 2 | $100 alert; $200 hard gate |
| 3 | (Ops Gate skipped for Tier 3) |

Cost tracking is downstream-skill responsibility; the conductor aggregates from `step_log[].cost_usd` if leaf skills populate it.

## Tier classification (per the Atlas convention)

**This skill itself is Tier 2** — a docs-class addition to the Atlas skill library. But it ORCHESTRATES Tier 1 production changes via `/atlas-deploy` + `/atlas-verify`. Independent review on this skill's logic is the standard Tier-2 review (no self-review of Ops Gate logic — the conductor itself is the orchestrator, not the gate).

## References

- `.claude/skills/atlas-verify/SKILL.md` (the mandatory leaf — owns auto-rollback)
- `.claude/skills/atlas-deploy/SKILL.md` (Convex + Vercel push)
- `.claude/skills/atlas-ship/SKILL.md` (the merge leaf invoked at Step 2)
- `.claude/skills/atlas-canary/SKILL.md` (the watch-period soak between deploy and verify)
- `.claude/skills/atlas-autoplan/SKILL.md` (canonical sister stage-conductor — Architect side)
- `.claude/skills/atlas-memo/SKILL.md` (where `.no_auto_rollback` is sealed)
- gstack reference: `github.com/garrytan/gstack` — `/ship`, `/land-and-deploy`, `/canary` (Atlas's chain maps to gstack `/land-and-deploy`; we adopt the shape, reject the heavy preamble)
