---
name: iterating-pr-reviews
description: "Use after opening a PR (sprint or phase) when the project has a reviewer registry configured (see docs/automated-review.md). Drives a registry-driven wait-fetch-address-retrigger loop until comments stabilise. Iterates over all active reviewer records, graduating each reviewer out of the rotation after its first clean review and treating two consecutive silent rounds as a broken-reviewer signal. Reviewers may be comment-bots (retriggered by a magic comment) or cli-subagents (invoked by shelling out and posting via gh pr comment). Default comment-bot is OpenAI Codex (round-0, seq=10); GitHub Claude, GLM, Gemini, and PR-Agent are manual-only and are not activated by default. CLI-subagent fleet defaults to the tier-matched opener only: sonnet-opener (mandatory opener, sprint-tier PRs) or opus-opener (mandatory opener, epic/phase PRs). codex-exec is manual-only (per P11 thesis) and NOT part of the default round-0 fan-out — invoke explicitly with --only codex-exec when wanted. Kilo/Antigravity have been removed from the runner — passing `--only kilo`/`--only antigravity` now fails fast as unknown reviewer IDs and must not be invoked. The active opener is tier-matched to the PR (see docs/automated-review.md reviewer registry). Uses ScheduleWakeup to free the session between iterations. Bounded by four independent caps: max_turns (default 5, hard runaway ceiling), semantic recurrence trip (same blocking finding persists >= N=2 consecutive rounds), fleet-invocation cap (max_fleet_invocations=3, prevents 30+ live model spawns), and convergence_round_cap (default 4, #1402 — trips on plain round count regardless of recurrence, with a tier-differentiated mandatory escalation: TL dispositive at sprint/hotfix, freeze+PL sign-off+TL adjudication at epic/phase/main) - auto-escalates to the Epic Lead on any cap hit instead of churning. The soft review-convergence discipline (~2-3 opener rounds, lead cap-and-ships at zero-BLOCKING) is separate from all four mechanisms."
---

# Iterating PR Reviews

## When to use

Invoked by `implementing-as-sprint` and `orchestrating-as-phase` after a PR is opened against a real merge target. This skill drives the bot-feedback iteration loop so the agent — not the user — owns the feedback-to-fix cycle.

The active reviewer set follows `docs/automated-review.md` → "Reviewer lens policy": Codex owns adversarial current-head implementation review, the tier-matched Claude CLI opener owns architecture/readability/role-context review, and RM/DevOps own gate and automation integrity outside this loop. GitHub Claude (`@claude review`) is manual-only; do not add legacy/manual reviewers merely to increase reviewer count. Add them only when a lead explicitly needs a missing lens for a one-off audit.

**Sprint 0 trial PRs are an exception.** Those PRs are `[DO NOT MERGE]` reference-only artefacts. Codex review of Sprint 0 PRs is user-driven (per `running-sprint-zero-trial/SKILL.md`). Do NOT enter this loop for Sprint 0 PRs.

---

## Precondition checks

Before starting:

1. Load `.claude/orchestration.yaml`. Verify `github_repo` is set and non-null. If missing, stop and tell the user to run `/update-orchestration-config` to add `github_repo`.
2. Confirm the PR number is known (passed in by the calling skill or visible in the current session context).
3. Confirm this skill is being invoked deliberately after PR creation — it is NOT auto-triggered after every commit.
4. Confirm the PR is NOT a Sprint 0 trial PR (title does not start with `[DO NOT MERGE]`, `[NOT FOR MERGE]`, or `[Codex S0]`). Codex S0 dry-run PRs (`[Codex S0]` prefix) are reference-only artefacts and must never enter this merge-bound review loop.
5. **Load cap configuration** — read the following from `.claude/orchestration.yaml`. Record all values for use in **Step 0** of every iteration.

   | Field | Default | Description |
   |---|---|---|
   | `review_loop.max_turns` | **5** | Hard round cap — force-escalate at this iteration count |
   | `review_loop.max_budget_usd` | (absent) | Optional budget cap in USD; skip check if absent |
   | `review_loop.recurrence_n` | **2** | Semantic recurrence threshold — escalate when the SAME blocking finding persists ≥ N consecutive rounds |
   | `review_loop.max_fleet_invocations` | **3** | Hard fleet-invocation cap — escalate when `run-cli-reviewers.sh` has been called this many times; prevents 30+ live model spawns |
   | `review_loop.convergence_round_cap` | **4** | (#1402) Round-count cap independent of recurrence — escalate at this iteration regardless of whether findings differ each round. Tier-differentiated mandatory escalation action (see Hard bound 4 below). |

   **Four hard bounds — all deterministic, all independent, never conflate with the soft bound:**
   - **Soft bound — review-convergence discipline:** the lead cap-and-ships after ~2–3 opener rounds at zero-BLOCKING. This is a judgment call by the lead, NOT any of these mechanisms.
   - **Hard bound 1 — round cap:** the deterministic force-escalate default of **5** sits just above the soft band — clear of false-trips, but trips a genuine runaway ~3–4× sooner than human judgment did on #217 (lead intervened at ~16). 20 is only the documented **UPPER CEILING** (enforced in code; `max_turns > 20` exits with a precondition error).
   - **Hard bound 2 — semantic recurrence trip (S4):** escalates when the SAME blocking finding (identified by its stable fingerprint from `.claude/bin/fingerprint-verdict.sh`) persists across N=2 consecutive rounds. Catches the exact failure mode that produced S1's 35-round runaway: a persistent unresolvable P1 keeps `has-blocking=true`, so the round cap is the only backstop unless recurrence is detected separately.
   - **Hard bound 3 — fleet-invocation cap (S4):** escalates when `.claude/bin/run-cli-reviewers.sh` has been invoked `max_fleet_invocations` (default **3**) times this loop. Each round-0 fan-out and each serial `--only <id>` invocation counts. Prevents 30+ live `claude --model claude-opus-4-8` (opus-opener) spawns — the exact token-burn the S1 deaf loop caused before it was SIGKILLed at round 35.
   - **Hard bound 4 — convergence-round cap (#1402):** escalates at iteration ≥ `convergence_round_cap` (default **4**) regardless of whether the SAME finding recurs — closes the gap Hard bound 2 does NOT catch: **disjoint** finding sets each round (a fresh nitpick every time, never the same fingerprint twice), the exact #1328 (6-7 GLM rounds)/#1383 (7 opener rounds in ~70 min, nitpicking its own prior rounds' fixes)/#1386 (9 rounds at 9 heads) shape. The escalation action is **tier-differentiated**, never a generic "notify the lead": **sprint/hotfix tier** → mandatory TL dispositive review (#1317, one mechanically-valid pass); **epic/phase/main tier** → mandatory freeze + PL sign-off + TL adjudication. "The EL decides" is never an acceptable third path at this bound.

     Note (round-2 review finding, resolved round 3): an earlier revision shipped this default at **3**, which sits AT the soft band's own documented upper edge (~2–3 opener rounds) — a project whose HEALTHY normal convergence regularly takes the full 3 rounds would hit this hard bound on ordinary PRs, not just runaways. Raised the shipped default to **4** (below, and in the `orchestration.yaml` example) so the mechanism no longer ships in its own known-false-tripping configuration. All three motivating incidents (#1328, #1383, #1386) badly exceeded even 3 rounds (6–9), so **4** still catches every documented incident shape while giving normal convergence one full round of headroom above the soft band. Still a per-project tuning knob, not a hardcoded value in `review-loop-cap.sh` itself (`--convergence-cap` remains strictly opt-in, no default in the script) — raise it further via `orchestration.yaml` if your project's own history shows the soft band regularly needs more than 3 rounds.

     **Important (review finding, round 4; mislabeled bound number fixed round 5):** the "default 4" above is a documentation/`orchestration.yaml`-layer convention, NOT a fallback inside `review-loop-cap.sh` itself. The Invoke-the-helper step below reads `convergence_round_cap` from `orchestration.yaml` and passes it explicitly as `--convergence-cap "$CONVERGENCE_ROUND_CAP"` — if a caller omits `--convergence-cap` entirely (e.g. forgets to read/pass the YAML value), **Hard bound 4** (the convergence-round cap) is NOT silently evaluated at the documented default; it is disabled outright for that invocation (see `review-loop-cap.sh`'s own "OPT-IN, no default is applied here" comment). (This note previously said "bound 2" — that number refers to the PER-ITERATION CHECK ORDER, not the Hard-bound numbering used everywhere else in this file, where Hard bound 2 is the semantic-recurrence cap; a reader following the stale "bound 2" reference would have concluded the wrong cap gets disabled.) This is deliberate backward-compatibility for callers outside `iterating-pr-reviews` (see Critical Invariant 3 in this sprint's `REGRESSION-GUIDE.md`), but within THIS skill's own loop, always resolve and pass `--convergence-cap` explicitly — never assume the bound is "on by default."

   ```yaml
   # .claude/orchestration.yaml — optional review loop cap settings
   review_loop:
     max_turns: 5                # hard round cap (default 5; 20 is the documented max ceiling)
     max_budget_usd: 10.00       # optional; omit to skip budget check
     recurrence_n: 2             # same-blocking-finding consecutive-round threshold (default 2)
     max_fleet_invocations: 3    # fleet runner invocation cap (default 3; aligns with ~3-round discipline)
     convergence_round_cap: 4    # (#1402) plain round-count cap, independent of recurrence (default 4 — one round above the ~2-3-round soft band; see Hard bound 4 note)
   ```

   Write `max_turns`, `recurrence_n`, `max_fleet_invocations`, `convergence_round_cap`, and (if set) `max_budget_usd` into the tracking comment on first write so they survive `ScheduleWakeup` invocations and the resume path can recover them without re-reading YAML.

---

## The iteration loop

### Round structure (#51) — round-0 parallel, rounds 1..N serial

The loop runs in numbered **rounds**, with deliberately different concurrency:

- **Round 0 — parallel fan-out.** On PR open, ALL `activation: round-0` and `activation: opener`
  reviewers review the PR **concurrently** (the `opener` is invoked first but the others do not wait
  for it). This is the broad first pass: every default reviewer sees the original diff at once.
  _Implementation note:_ the **comment-bot** reviewers genuinely fire concurrently (independent GitHub
  Apps/Actions). The **cli-exec** fleet is driven by `.claude/bin/run-cli-reviewers.sh`, which is **serial** —
  it invokes each CLI one at a time in `sequence_position` order (opener first). This is still the
  round-0 "fan-out" in effect (all round-0 cli reviewers run against the original diff in one cycle),
  but the runner does not spawn them in parallel; opener-first ordering is preserved so the gate stays
  sound.
- **Rounds 1..N — strictly serial (one reviewer per commit).** After round 0, the loop processes
  findings one reviewer at a time, ordered by `sequence_position`. Each serial round: address the
  current reviewer's actionable findings → produce exactly **one fix commit** → (re)trigger/invoke
  **only that one reviewer** on the new HEAD → wait → classify. Do NOT fan out all reviewers in
  parallel in rounds 1..N. Rationale: serial rounds keep a 1:1 mapping between a fix commit and the
  reviewer that verifies it, so `last_clean_commit`/`invoked=` attribution stays unambiguous and two
  reviewers never race on the same HEAD (which previously made stale-marker and HEAD-advance bugs
  possible — see the #52 design notes). The mandatory `opener` takes the lowest `sequence_position`,
  so it leads each serial pass and is the last gate to clear on the terminal commit.
- **Convergence.** Rounds 1..N repeat until the [stop condition](#step-8--stop-condition-check) holds
  (all activated reviewers `dropped-clean` on the terminal commit, mandatory opener included). A
  reviewer that re-activates (new findings, or HEAD advanced past its clean commit) re-enters the
  serial queue at its `sequence_position`.

Steps 0–8 below specify one round's mechanics; the round number is tracked as `iteration` in the
state-persistence block.

### Step 0 — Cap check ⚑ (FIRST action on every iteration, including the resume after ScheduleWakeup)

**This is the first step executed on every iteration, including after every `ScheduleWakeup` resume.** It mirrors the "check mailbox between iterations" discipline: a deaf loop that ignores its cap is the exact failure being fixed (#217/#223). The cap is a **runaway ceiling** — it fires EARLY (default 5, just above the ~2–3 normal-convergence band), not after a catastrophe has played out.

**State bootstrapping for Step 0** — the cap check requires `iteration`, `max_turns`, `fleet_invocations`, `max_fleet_invocations`, `blocking_fp_counts` (and `max_budget_usd`/`spent_usd` if budget tracking is enabled) before Step 2 (full comment fetch) runs:

- **First iteration** (no tracking comment exists yet): `iteration = 0`, `fleet_invocations = 0`, `blocking_fp_counts = {}` (empty JSON object `{}`), all other caps from precondition check #5. Cap cannot be hit at iteration 0; proceed directly to Step 1.
- **ScheduleWakeup resume** (tracking comment exists): perform a **minimal tracking-comment fetch** — fetch the most recent comment from the orchestrator account whose body starts with `<!-- review-state-v1`, then parse ONLY the header block between `<!--` and `-->`. Extract ALL of the following (reading uninitialised would silently break the checks — do NOT skip):

  | Field to extract | Default if absent |
  |---|---|
  | `iteration` | 0 |
  | `max_turns` | from precondition #5 |
  | `fleet_invocations` | 0 |
  | `max_fleet_invocations` | from precondition #5 |
  | `blocking_fp_counts` | `{}` — **critical**: if this field is absent the recurrence check starts from scratch, losing the prior-round counts. A missing `blocking_fp_counts` means any fingerprint that recurred in the previous round will NOT be caught on the NEXT round. Initialize to `{}` only on first iteration; on resume, treat absence as a state corruption warning (log and continue with empty, but do not silently skip the field). |
  | `max_budget_usd` | (absent = skip budget check) |
  | `spent_usd` | (absent = skip budget check) |
  | `convergence_round_cap` | from precondition #5 (default 4; #1402) |

  Once Step 0 passes, proceed to Step 1 (wait) and then Step 2 (full comment + state recovery).

**Check all bounds in order (all five evaluated every iteration):**

1. **Round cap:** if `iteration >= max_turns` → **ESCALATE** (see below). Do NOT proceed to Step 1.
2. **Convergence-round cap (#1402):** if `iteration >= convergence_round_cap` → **ESCALATE** with the tier-differentiated action (TL dispositive at sprint/hotfix tier; freeze + PL sign-off + TL adjudication at epic/phase/main tier). Do NOT proceed to Step 1. Fires independently of whether this round's findings are the same as a prior round's — see Hard bound 4 above.
3. **Budget cap (if `max_budget_usd` is set):** if `spent_usd >= max_budget_usd` → **ESCALATE**. Do NOT proceed to Step 1.
4. **Fleet-invocation cap:** if `fleet_invocations >= max_fleet_invocations` → **ESCALATE**. Do NOT proceed to Step 1. This check fires BEFORE invoking `run-cli-reviewers.sh` for this round — if the cap is already hit, the loop halts without spawning another live model call.
5. **Semantic recurrence cap:** compute current-round blocking fingerprints and update the per-fingerprint consecutive-count map (see below). If any fingerprint's count ≥ `recurrence_n` → **ESCALATE**. Do NOT proceed to Step 1.

If no cap is hit → continue to Step 1.

**Note on bound interaction under defaults (review finding, round 3; check/Hard-bound numbering disambiguated round 6):** this note uses two DIFFERENT numbering schemes that happen to overlap — the per-iteration check order above (check #1 = round cap ... check #5 = recurrence cap) and the conceptual Hard-bound numbering used everywhere else in this file (Hard bound 1 = round cap, Hard bound 2 = recurrence cap, Hard bound 3 = fleet-invocation cap, Hard bound 4 = convergence-round cap). To avoid the exact ambiguity a round-5 edit accidentally reintroduced here: check #1 (Hard bound 1, round cap) is evaluated FIRST in the per-iteration order above, but with `max_turns=5` and `convergence_round_cap=4` (both defaults), check #2 (Hard bound 4, convergence-round cap) always reaches its own threshold at an EARLIER iteration number than check #1 — so at default settings, the convergence-round cap is the one that actually fires first in practice; the round cap's `max_turns=5` ceiling is not reachable under default configuration unless `convergence_round_cap` is raised to 5 or above. This is intentional (the whole point of Hard bound 4 is to catch disjoint-finding non-convergence one round before the round cap's runaway ceiling would), but worth stating explicitly so a future reader does not assume `max_turns=5` is the operative early bound under defaults.

**Computing the recurrence cap state (Step 0, sub-step for check #5 / Hard bound 2):**

After assembling the current-round verdict via `.claude/bin/assemble-verdict.sh` (or from the tracking comment's last assembled state), compute fingerprints and update the consecutive-count map:

```bash
# 1. Compute current-round blocking fingerprints.
VERDICT_FILE="$(mktemp)"
# ... (assemble verdict or load from tracking comment state)
# Resolver: finds script in .claude/bin/ (consumer) or bin/ (dogfood), whichever is present.
_pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }
"$(_pd_lib fingerprint-verdict.sh)" --verdict "$VERDICT_FILE" > /tmp/current_fps.txt

# 2. Load previous counts (from tracking comment blocking_fp_counts field) into a temp JSON file.
# On first iteration: previous counts = "{}"
printf '%s' "$BLOCKING_FP_COUNTS" > /tmp/prev_counts.json

# 3. Update consecutive counts (Python one-liner — no model calls, pure text).
#    For each fp in current set: increment its count. For fps NOT in current set: drop (or set 0).
#    NOTE: the output redirect MUST be on the invoking line — a here-doc terminator is only
#    recognized when the line contains the delimiter alone, so `PYEOF > file` never writes (opus-opener P2).
/usr/bin/python3 - /tmp/current_fps.txt /tmp/prev_counts.json <<'PYEOF' > /tmp/updated_counts.json
import json, sys
fps_file, prev_file = sys.argv[1], sys.argv[2]
with open(fps_file) as f: fps = [l.strip() for l in f if l.strip()]
with open(prev_file) as f: prev = json.load(f)
updated = {fp: prev.get(fp, 0) + 1 for fp in fps}
print(json.dumps(updated))
PYEOF

# 4. Persist updated_counts.json into BLOCKING_FP_COUNTS for tracking comment write.
BLOCKING_FP_COUNTS="$(cat /tmp/updated_counts.json)"
```

**Invoke the helper (with all four bounds):**

```bash
# Resolver: finds script in .claude/bin/ (consumer) or bin/ (dogfood), whichever is present.
_pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }

# Always required (turn + recurrence + fleet + convergence):
"$(_pd_lib review-loop-cap.sh)" \
  --iteration "$ITERATION" \
  --max-turns "$MAX_TURNS" \
  --fp-counts-file /tmp/updated_counts.json \
  --recurrence-n "$RECURRENCE_N" \
  --fleet-invocations "$FLEET_INVOCATIONS" \
  --max-fleet-invocations "$MAX_FLEET_INVOCATIONS" \
  --convergence-cap "$CONVERGENCE_ROUND_CAP" \
  --tier "$PR_TIER" \
  --pr "$PR" \
  --repo "$GITHUB_REPO" \
  --lead "$LEAD_SESSION"

# Include --spent-usd and --max-budget-usd only when tracking budget:
# "$(_pd_lib review-loop-cap.sh)" ... --spent-usd "$SPENT_USD" --max-budget-usd "$MAX_BUDGET_USD"
```

**`--tier "$PR_TIER"` is required for the convergence-cap bound to pick the correct tier-differentiated escalation action** (`$PR_TIER` is the same `sprint|epic|phase|main` value already resolved for `run-cli-reviewers.sh --tier` and `ca2-merge-gate.py --tier` elsewhere in this loop — see Step 5/Step 8). Omitting `--tier` still traps the round-4 non-convergence (the bound still fires), but the escalation reason falls back to a generic "pass --tier explicitly" message instead of naming the TL-dispositive or freeze+adjudication path — always pass it. Note: `review-loop-cap.sh`'s own `case` also accepts a `hotfix` tier value for callers outside this standard skill flow, but `$PR_TIER` as derived here never produces `hotfix` — hotfix-shape sprints skip this loop entirely per the sprint-agent "Hotfix lane exception" (see `review-loop-cap.sh`'s inline comment at the tier-differentiated `case` block for the full explanation).

**Fleet invocation counter increment:** increment `fleet_invocations` by 1 **after** invoking `.claude/bin/run-cli-reviewers.sh` in Step 5, and persist the updated count to the tracking comment before `ScheduleWakeup`. This ensures Step 0 on the next wakeup sees the accurate count and can trip the cap if warranted.

**Persisting `blocking_fp_counts` (critical for cross-round recurrence):** after computing the updated count map in the recurrence sub-step above, write `BLOCKING_FP_COUNTS` to the tracking comment **before** invoking `ScheduleWakeup`. The resume path at the top of this Step 0 reads `blocking_fp_counts` back from that comment; if the write is skipped, the per-round consecutive counts are lost and the recurrence trip is silently disabled for the following rounds. The persistence happens at the SAME tracking-comment update as all other state (Step 5 or after Step 7); do NOT write a separate comment just for this field.

`$LEAD_SESSION` is the Epic Lead's canonical session id, e.g. `P6/E2/enforcement-layer`. **`--lead` is required for production use.** The helper has an auto-discovery fallback (reads state files under `$BOARD/sessions/`) but it is unreliable in multi-session epics (multiple `.state` files → refuses; missing state file → no signal written). In a headless/autonomous sprint session, an unresolvable lead means the cap-hit escalation is silently lost and the Epic Lead is never notified — defeating the auto-escalate guarantee. Always set `LEAD_SESSION` before entering the loop (read from `orchestration.yaml` or passed down from the calling skill).

Exit code `0` → continue. Exit code `1` → cap hit (or missing lead with no auto-resolvable state file — the helper warns and exits 1); follow the **Escalation on cap** procedure below. Exit code `2` → precondition error (explicitly-empty `--lead ""`, missing required option value, or invalid input); **do not silently continue** — surface the error to the user and halt the loop until the precondition is fixed (check that all required args are set and non-empty before invoking the helper).

**Budget cap note:** `--spent-usd` requires an external provider — the loop does not auto-compute cumulative cost. If a calling context tracks per-round cost (e.g. via Claude API usage headers), pass it via `--spent-usd "$SPENT_USD"` and set `max_budget_usd` in `orchestration.yaml`. If no external provider exists, omit both flags; the budget branch never fires and the round cap (`max_turns`) is the sole bound. This sprint ships the mechanism; wiring it to a live cost source is deferred.

#### Escalation on cap

When `.claude/bin/review-loop-cap.sh` exits `1` (any of the five caps: round, convergence, budget, recurrence, or fleet):

1. **Do NOT iterate further.** Do NOT address comments, retrigger bots, or advance HEAD.
2. **Do NOT merge.** Set `ready_to_merge: false` in the tracking comment.
3. The helper has **attempted** to write an escalation signal to the Epic Lead's inbox (`signals/<dirname(LEAD)>/<basename(LEAD)>.<TS>-<HEX>.signal`, event `review-loop-cap-escalation`). The signal body includes a `reason=` field identifying which cap fired and the relevant counts. The signal is written only when `--lead` was resolved — either passed explicitly or auto-discovered from a state file. If `--lead` was not passed explicitly and auto-resolution failed (helper warns "could not resolve lead session"), the signal was NOT written; in that case, notify the Epic Lead manually and ensure `--lead` is set on future invocations.
4. **Post a PR comment** explaining the cap was hit so the PR timeline is auditable. Tailor the message to the cap that fired (the `reason=` field in the escalation signal body identifies it):
   ```bash
   # Example for round cap:
   gh pr comment "$PR" --repo "$GITHUB_REPO" --body \
     "⚑ Review loop cap reached (iteration=$ITERATION >= max_turns=$MAX_TURNS). \
   Escalating to Epic Lead — loop stopped. No merge until lead reviews and re-arms. \
   To increase the cap: set \`review_loop.max_turns\` in \`.claude/orchestration.yaml\`."

   # Example for convergence-round cap (#1402) — tier-differentiated, never generic:
   # "⚑ Convergence-round cap reached (iteration=$ITERATION >= convergence_round_cap=$N),
   #  tier=$PR_TIER. Findings differ each round — this is NOT a recurrence trip.
   #  Mandatory next step (sprint/hotfix tier): TL dispositive review (#1317), one pass.
   #  Mandatory next step (epic/phase/main tier): freeze this PR + PL sign-off + TL adjudication.
   #  Do NOT proceed to round $((ITERATION + 1)) without that step completing."

   # Example for recurrence cap:
   # "⚑ Recurring-P1 trip: finding '$FP' persisted $COUNT consecutive rounds (>= recurrence_n=$N).
   #  Same finding recurred unfixed — escalating. Per escalate-don't-iterate discipline."

   # Example for fleet cap:
   # "⚑ Fleet-invocation cap reached ($FLEET_INVOCATIONS invocations >= max_fleet_invocations=$MAX).
   #  Loop stopped to prevent live model overrun. Epic Lead re-arms."
   ```
5. Update the tracking comment: set `ready_to_merge: false`, add `cap_hit: true` and `cap_reason: <reason>`.
6. **Halt.** Do not invoke `ScheduleWakeup`. The loop is stopped until the Epic Lead re-arms it explicitly.

**The Epic Lead's inbox watcher will deliver the escalation signal.** The lead decides whether to:
- Increase `max_turns` or `max_fleet_invocations` in `orchestration.yaml` and re-invoke the skill. **`max_turns` must be ≤ 20** — the cap helper enforces a hard upper ceiling of 20 and exits 2 (precondition error) for any value above it. If more than 20 rounds are genuinely needed, restructure the review process rather than raising the ceiling further.
- For a recurrence-cap hit: the lead reviews whether the recurrent finding is a genuine blocker or a false positive, then either fixes the code, rejects the finding with evidence, or defers it — and re-arms the loop.
- **For a convergence-cap hit (#1402): the lead does NOT unilaterally re-arm.** Sprint/hotfix tier requires a TL dispositive review (#1317) completing first; epic/phase/main tier requires PL sign-off + TL adjudication first. Only after that step completes may the loop be re-armed — re-arming without it reproduces the exact #1328/#1383/#1386 self-feeding-loop failure this bound exists to stop.
- Review the current PR state and merge/close manually.

**Never** silently continue past any cap — an unbounded loop is the failure mode this mechanism exists to prevent.

---

### Step 1 — Wait 10 minutes

Invoke `ScheduleWakeup` with `delaySeconds=600`. Set the `prompt` to a self-resuming value that re-enters this skill at Step 2, e.g.:

> "Resume iterating-pr-reviews for PR {{PR}} on repo {{github_repo}}. Start at Step 2: fetch bot comments."

This frees the user's session. The agent wakes automatically when the timer fires.

**Why 10 minutes?** PR review bots typically comment within 1–2 minutes on small PRs. Large PRs can take longer; 10 minutes is a safe upper bound for OpenAI Codex and any explicitly invoked manual bot.

### Step 2 — Fetch reviewer comments and recover state

```bash
gh api --paginate repos/{{github_repo}}/issues/{{PR}}/comments
gh api --paginate repos/{{github_repo}}/pulls/{{PR}}/comments
```

**Always `--paginate`.** A PR with more than one page of comments (the default page is 30) will otherwise silently drop reviewer findings and the most-recent tracking-comment state — the same truncation class the gate-poller's paginated `reviewThreads` already guards against. Both the issue-comment and pull-review-comment fetches must paginate to completion.

**Registry-driven filter:** iterate the reviewer registry (see `docs/automated-review.md` — Reviewer registry). For each record, filter results for that record's `author_login`. Skip records where `author_login` is `null` — those reviewers (`cli-subagent` records) post under the orchestrator's own account and their output is handled separately.

For the seed records, this is equivalent to filtering for:
- `chatgpt-codex-connector[bot]` (id: `codex`)
- `gemini-code-assist[bot]` (id: `gemini`, legacy/manual opt-in)
- `github-actions[bot]` (id: `pr-agent`, legacy/manual opt-in)
- `claude[bot]` (id: `claude`) — manual-only; include in the scan only when a lead/human explicitly invoked `@claude review` for this PR.

Collect the full text of every comment from these authors. Record each comment with: author, reviewer record id, comment ID, URL, and body.

**CLI-subagent marker recovery (`author_login: null` records).** `cli-subagent` reviewers post under the orchestrator's own account, so they cannot be recovered by `author_login`. Instead, scan the orchestrator-account issue comments for the marker `<!-- cli-review id=<reviewer-id> commit=<SHA> -->` (see `docs/automated-review.md` — CLI-subagent invocation protocol). Attribute each marked comment to the registry record whose `id` matches, and treat `commit=<SHA>` as the review marker's reviewed-commit reference (the analogue of Codex's `Reviewed commit:`). These comments then feed the same clean-review / stall checks as comment-bot reviews.

**Recovering reviewer state across ScheduleWakeup invocations:** After fetching issue comments, scan all comments from the PR author (including yourself — the agent account that opened the skill) for the most recent one whose body starts with the line `<!-- review-state-v1`. Parse the key=value header block between the opening `<!--` and closing `-->` to recover the previous iteration's reviewer states. If no such comment exists, initialise the tracking state from the registry: place all records with `activation == round-0` or `activation == opener` into `active` state with `stalls=0`. Do NOT hardcode a fixed list of reviewer ids — iterate the registry at loop start so newly added `round-0`/`opener` records are automatically included without changing loop control flow. The full format is documented in the [State persistence](#state-persistence) section.

### Step 3 — Categorize by severity

Apply the rubric below (also in `commands/review-phase-pr.md`):

| Severity | Label | Description |
|---|---|---|
| HIGH | P1 | Must fix before merge: security issues, data loss, broken acceptance criteria, incorrect logic |
| MEDIUM | P2 | Should fix or explicitly track: performance concerns, maintainability, missing error handling |
| LOW | P3 | Nice-to-have: style suggestions, minor naming, optional improvements |

### Step 4 — Address actionable comments

For each P1 and P2 comment:

**Option A — Fix it:**
1. Make the change in code.
2. Commit with a focused message referencing the bot comment.
3. Push to the PR branch.
4. Reply on the comment thread acknowledging the fix, referencing the commit SHA.
   Branch on where the comment came from:
   - **Inline review comment** (sourced from `GET pulls/{{PR}}/comments` or a `reviewThread`):
     ```bash
     gh api repos/{{github_repo}}/pulls/{{PR}}/comments/{{comment_id}}/replies \
       --method POST --field body="Fixed in commit <SHA>: <brief explanation>"
     ```
   - **Top-level PR/issue comment** (sourced from `GET issues/{{PR}}/comments`):
     GitHub issue comments have no replies endpoint; post a new top-level acknowledgement instead:
     ```bash
     gh api repos/{{github_repo}}/issues/{{PR}}/comments \
       --method POST --field body="Addressed in commit <SHA>: <brief explanation> (re: comment {{comment_id}})"
     ```
   This reply is required for the merge-gate poller (Condition 3 in `docs/automated-review.md`) to recognise the thread as addressed. A bare commit without a thread reply does not satisfy the gate.

**Option B — Reject it (with stated reason):**
1. Reply on the comment thread via:
   ```bash
   gh api repos/{{github_repo}}/issues/comments/{{comment_id}}/replies \
     --method POST --field body="Rejecting: <reason>"
   ```
   Or use a PR review comment reply as appropriate.
2. Document the rejection reason clearly. "Won't fix" without a reason is not acceptable.

**Option C — Defer to a future phase/sprint:**
1. Create a GitHub issue:
   ```bash
   cat > /tmp/deferred-review-issue-body.md <<'EOF'
<!-- pd-priority-routing -->
## Routing Prioritization
- Routing tier: Medium
- Sort order: 2
- WSJF: N/A - deferred review finding; score during phase planning
- RICE: N/A - deferred review finding; score during phase planning
- MoSCoW: Should
- Rationale: Deferred from review comment.
<!-- /pd-priority-routing -->

## Deferred Work

<detail from bot comment>
EOF
   gh issue create --repo {{github_repo}} \
     --title "<short description>" \
     --body-file /tmp/deferred-review-issue-body.md \
     --label "P{{N}}"
   rm -f /tmp/deferred-review-issue-body.md
   ```
2. Add a row to `PHASE-ROADMAP.md`'s Issue Summary Table assigning the issue to the target phase, including `Routing tier`, `Sort`, `WSJF`, `RICE`, and `MoSCoW`.
3. Ensure that target phase's `ORCHESTRATION-PROMPT.md` (or the relevant sprint `PROMPT.md`) lists the issue in scope.
4. Post a reply on the original PR comment thread linking to the new issue.

All four steps are required for a valid deferral. See `docs/deferred-issues.md` for the full process.

P3 comments that are out of scope for the current sprint should be deferred following the four-step process in `docs/deferred-issues.md`. P3 comments that are genuinely not worth tracking (subjective style preferences, duplicate suggestions, etc.) may be rejected with a brief reply ("noted, out of scope / won't fix") — but every P3 comment must still be acknowledged.

**Never silently skip comments.** Every bot comment must result in one of: fix, rejection with reason, or tracked deferral.

### Step 4a — Loop-discipline rules (#1402 — mechanize, don't just document)

Three incidents behind #1402 (#1328, #1383, #1386) share ONE mechanism: the EL treats every finding — including non-blocking P3s, and including nitpicks the reviewer raised about the PR's OWN prior-round fixes — as something to push a fix for, which moves HEAD and voids the review that was just clean. These four rules close that reflex (the "three" above counts INCIDENTS, not rules — do not conflate with the differing rule counts named in `templates/PROMPT.md.tmpl` ["Four rules"] and `templates/EPIC-PROMPT.md.tmpl` ["Five rules", which adds the epic-only merge-guard rule] — each file's own count is internally correct for its own scope):

1. **P3-file-don't-fix.** A P3 finding is **never fixed on the PR** by pushing a commit for it alone. File it as a GitHub issue per the Option C deferral process above (or reject it per Option B if genuinely not worth tracking) and move on. The ONLY reason to touch the diff again this round is an open P1/P2.
2. **Clean-round-is-a-merge-trigger.** When a round comes back with **zero P1/P2** (a clean review at the exact current HEAD), that is the signal to **merge**, not to push one more polish/P3 commit. A push after a clean round voids the very review that just cleared the PR — see the mechanical guard below.
3. **Batched-fix discipline.** When a round DOES have open P1/P2 findings, address **all of them together in one push** — nothing else in the diff. Do not dribble out separate pushes per finding (each push re-triggers reviewers and burns a round); do not smuggle in unrelated cleanup, refactors, or P3 fixes alongside the blocking-finding fix. One round, one push, only the blocking findings.
4. **Round-cap escalation** (Step 0, Hard bound 4 above): if a genuine question of "is this actually converging" persists past round `convergence_round_cap` (default 4) regardless of these rules, that is handled mechanically, not by lead judgment — see Hard bound 4.

**Mechanical enforcement — not just doctrine prose:** a push to a branch whose PR has a clean review (zero P1/P2) at the exact current HEAD is intercepted by the `block-push-after-clean-review.sh` PreToolUse hook (`examples/hooks/block-push-after-clean-review.sh`, backed by `bin/check-no-push-after-clean.sh`) — it fires a loud, visible warning ("clean review at head exists — pushing voids it; merge instead, file P3s as issues") on the EL's own `git push` invocation, not a doc a diligent EL might read. See `docs/automated-review.md` §"No-push-after-clean guard" for the full mechanism and override path.

### Step 4.5 — Determine which reviewers are active

The reviewer record schema is defined authoritatively in `docs/automated-review.md` — Reviewer record. This step operates on the registry of typed records, not a hardcoded list of logins.

Both `comment-bot` and `cli-subagent` reviewers participate in the **same** state machine below. They differ only in how they are (re)invoked — comment-bots via a trigger comment (Step 5), cli-subagents via the [CLI-subagent invocation protocol](../../docs/automated-review.md#cli-subagent-invocation-protocol-52) (shell out + post a `<!-- cli-review … -->` marker). The state transitions (`active` → `dropped-clean` / `dropped-broken`) apply **identically** to both kinds, keyed on each reviewer's review marker (see Clean review / Silent stall below). This is what lets a `cli-exec` reviewer — including the mandatory `opus-opener` — reach `dropped-clean` and clear the Step 8 gate.

#### Reviewer state machine

Each active reviewer (`comment-bot` or `cli-subagent`) has one of three states:

| State | Meaning | When entered |
|---|---|---|
| `active` | reviewer is currently in the trigger rotation | initial state on PR open; or re-activated after new findings |
| `dropped-clean` | reviewer has given one clean review on the current HEAD; omitted from the next retrigger | after a clean review is confirmed (see below) |
| `dropped-broken` | reviewer has stalled twice without posting an active review marker; omitted from all future retriggers | when `stall_count >= 2` |

**Initial state is determined by the `activation` field** (defined in `docs/automated-review.md` — Reviewer record):

| `activation` value | Initial loop state |
|---|---|
| `round-0` | Placed into `active` state at loop start; joins the round-0 parallel fan-out |
| `fallback-only` | Starts **inactive** (not tracked, not triggered); reserved for future use (no seed record currently uses this value) |
| `manual-only` | Starts **inactive** (not tracked, not triggered); scanned only if a lead/human explicitly invoked it |
| `opener` | Placed into `active` state at loop start; mandatory round-0 opener (pairs with `mandatory: true` and lowest `sequence_position`) |

Start each new PR loop with **all** reviewers (`comment-bot` AND `cli-subagent`) whose `activation == round-0` or `activation == opener` placed into `active` state with `stall_count=0` — **subject to the `tier` field** (see `docs/automated-review.md` — Reviewer record schema). Opener records are tier-scoped: `sonnet-opener` (`tier: sprint`) is the mandatory opener for sprint-tier PRs; `opus-opener` (`tier: epic,phase`) is the mandatory opener for epic→phase, production-cascade, **and epic→planning-target (PR B)** PRs — the full-fleet tier. The loop must determine the PR tier from **head + target** together (not target alone): sprint-branch head → `sprint`; **epic-branch head targeting the phase base (PR A) → `epic`**; **epic-branch head targeting the configured planning branch (PR B) → `phase`-tier full-fleet** (opus-opener, per `docs/review-depth-gradient.md` and `commands/authorize-prb.md`); phase-branch head targeting planning/`main` (cascade phase PR) → `phase`. Then activate only the opener whose `tier` matches. (Target alone is ambiguous — a phase-base target is PR A `epic`, but a planning/`main` target is either PR B or a cascade phase PR; the head disambiguates.) (PR B runs the opus-opener full-fleet pass to zero-BLOCKING; per-event operator authorization is a separate FINAL gate handled by `/authorize-prb` only when the planning target is production `main`, not by this loop.) The `opener` is invoked first (lowest `sequence_position`). For the configured records: `codex` (comment-bot, seq=10) and the **tier-matched opener** (`sonnet-opener` for sprint PRs; `opus-opener` for epic/phase PRs) start active. `claude`, `glm-5.2-action`, `codex-exec`, `gemini`, and `pr-agent` have `activation: manual-only` — they do NOT start active in the default round-0 fan-out. Invoke `codex-exec` explicitly with `--only codex-exec` for on-demand CLI coverage; invoke GitHub Claude only as a deliberate manual audit. Kilo/Antigravity have been removed from the runner (unknown `--only` selectors now fail fast as unknown reviewer IDs).

#### Clean review definition

A reviewer's review for the current HEAD is **clean** if BOTH of the following hold:

1. **Active review marker present.** The reviewer posted a review-marker comment after the most recent retrigger/invocation and referencing the current HEAD SHA:
   - **Codex:** a comment whose body starts with `### 💡 Codex Review` AND contains the substring `Reviewed commit: <current HEAD SHA>`.
   - **Claude:** a comment from `claude[bot]` whose body starts with `### Claude Review` AND contains the substring `**HEAD:** \`<current HEAD SHA>\`` (the bold HEAD line in the review header). Fall back: any comment from `claude[bot]` posted after the most recent retrigger whose body starts with `### Claude Review` counts as a marker regardless of SHA line format — document the observed format in the tracking comment for future reference. _Observed format on PR #976: `### Claude Review — PR #976 (Round-N, Epic Tier)` with `**HEAD:** \`<8-char short SHA>\``._
   - **Gemini:** a comment whose body contains both "Gemini" and a `Reviewed commit:` reference OR any review-state submission from `gemini-code-assist[bot]` posted after the most recent retrigger and against the current HEAD. _Note: Gemini's exact marker format is unverified at the time of this writing. If the marker pattern above does not match, fall back to: any review comment from `gemini-code-assist[bot]` posted after the most recent retrigger counts as a review marker regardless of body format. Document the actual marker text observed in the tracking comment for future reference._
   - **CLI-subagent (`cli-exec`, incl. `opus-opener`):** a comment under the orchestrator account whose body contains the marker `<!-- cli-review id=<reviewer-id> commit=<current HEAD SHA> invoked=<invocation-ts> -->`. To count for the **current** cycle ALL of: (a) `commit=` equals the current HEAD SHA, (b) `id=` matches the record, and (c) the marker is fresh — its `invoked=` value equals the reviewer's `last_invoked_ts` recorded in the tracking comment for this cycle (equivalently, the comment's `createdAt` is **after** that `last_invoked_ts`). A *stale* marker from a **prior** invocation on the same HEAD (e.g. the opener cleared HEAD X last cycle, then a P1 was rejected without a commit so HEAD is still X, and this cycle's invocation produced nothing) must NOT be reused — without a fresh marker the reviewer **stalls**. This is the marker recovered in Step 2.
2. **Zero new P1 or P2 comments** from that reviewer posted since the most recent retrigger/invocation. P3 comments are allowed and do not block a clean classification.

A reviewer that meets both conditions transitions `active` → `dropped-clean` (record `last_clean_commit` = current HEAD, `last_clean_ts`). This applies to comment-bots and cli-subagents alike, so the mandatory `opus-opener` reaches `dropped-clean` and the Step 8 gate can clear.

#### Silent stall definition

After the 10-minute wait following a retrigger (for comment-bots), or after a cli-subagent was invoked this cycle, if a reviewer in `active` state has **not** posted an active review marker on the current HEAD — for `cli-exec` reviewers this means it was invoked but produced no `<!-- cli-review id=… commit=<HEAD> -->` marker (e.g. the CLI errored, returned empty, or is unauthenticated):
- Increment that reviewer's `stall_count`.
- If `stall_count >= 2`: transition the reviewer to `dropped-broken`. (If the reviewer is `mandatory`, this also fails the Step 8 gate — surface the broken mandatory reviewer to the user.)
- If the reviewer DOES post a marker (whether clean or with findings): reset `stall_count` to 0.

#### Re-activation from dropped-clean

A reviewer in `dropped-clean` can re-activate two ways:

1. **New findings on its own cadence (comment-bots).** After the wait in Step 6, check whether a `dropped-clean` comment-bot posted new P1 or P2 comments without being triggered. If yes: transition it back to `active` and clear its clean status.
2. **HEAD advanced past its clean commit (REQUIRED — all reviewers, critical for `cli-exec`).** Whenever a fix commit advances HEAD, any `dropped-clean` reviewer whose `last_clean_commit != current HEAD SHA` is **re-activated** (transition back to `active`, clear `last_clean_commit`) so it reviews the new terminal commit. This is essential for `cli-subagent` reviewers: unlike comment-bots, they do NOT auto-re-review on push — Step 5 only invokes `cli-exec` reviewers when `state == active`, so without this rule a `dropped-clean` cli-subagent (including the mandatory `opus-opener`) would never see commits made after its clean review, and the gate could clear on a commit it never reviewed. Re-activating forces re-invocation in the next round. (Optional non-mandatory comment-bots that auto-re-review may rely on rule 1 instead, but mandatory reviewers MUST follow this rule.)

#### Usage-limit fallback

Before composing the retrigger comment, check whether Codex is **currently** usage-limited. A bot is **currently usage-limited** if both:

1. Its most recent comment **since the previous retrigger** (i.e., posted after `last_retrigger_ts` from the tracking comment, or after PR creation on the first cycle) is an explicit usage / quota / rate-limit message — e.g., "I've reached my usage limit for this period", "rate limited", "quota exceeded".
2. It has not posted a real review marker (`### 💡 Codex Review` — see the [Clean review definition](#clean-review-definition)) since that usage-limit message.

**Scope the scan to the current cycle's window** — do NOT scan the full PR comment history. A historical limit that the bot has since recovered from must not stick: once a bot posts a real review marker (whether clean or with findings), the usage-limit overlay is cleared. Do NOT mark a bot as limited based on transient errors, empty replies, or unrelated comments — only an explicit limit-related message counts.

Since `codex` is the only default `round-0` comment-bot, a Codex usage limit does **not** promote GitHub Claude. The limited reviewer's own state-machine entry (`active`, `stalls`, etc.) is **not changed** — it may resume on the next cycle if the limit clears. The tier-matched CLI opener remains the mandatory review gate for the current head.

The limited-reviewer substitution rule is now:

| Limited reviewer | Behaviour |
|---|---|
| `codex` limited | omit `@codex review` this cycle; continue/invoke the tier-matched CLI opener; record the limit in the tracking comment |
| manual-only `claude` limited | no default-loop action; omit any manual Claude retrigger unless a lead explicitly asks for another manual attempt |
| both limited simultaneously | surface to user; do not auto-promote another comment-bot |

If `@codex review` is limited or the Codex reviewer is in a `dropped-*` state, simply omit its trigger line (standard retrigger algorithm). Append a one-line note in the comment body when a reviewer's usage limit was detected, e.g.:

> `(chatgpt-codex-connector[bot] reported a usage limit this cycle; default loop continues with the tier-matched CLI opener.)`

**Manual-only precondition:** `@claude review` requires the Claude GitHub App to be installed on the repo, but this is not a default-loop precondition. If a lead explicitly asks for manual GitHub Claude and the app is absent, surface that manual-audit blocker; do not convert absence into a default-loop failure.

### Step 5 — Re-trigger reviewers

After addressing all actionable comments, build the retrigger comment body by iterating the reviewer registry (after applying usage-limit overrides from Step 4.5):

1. Iterate records ordered by `sequence_position` (ascending).
2. For each record: if `state == active` **and** `trigger_mode == comment-trigger` **and** NOT usage-limited in the current cycle, emit its `trigger_command` value as one line in the retrigger comment body — **subject to the round scope below.**
   - **Round scope (enforces the #51 serial invariant — the same restriction the cli-exec runner applies via `--only`):** in **round 0** emit the trigger for *every* qualifying active comment-bot (the parallel fan-out). In **rounds 1..N** emit ONLY the single comment-bot whose serial turn it is on this fix-commit (one reviewer per commit, by `sequence_position`); do NOT re-trigger the others until their turn. Re-triggering all comment-bots every serial round would race multiple reviewers on one HEAD — exactly the attribution hazard the serial structure exists to prevent.
3. Skip records where `state` is `dropped-clean` or `dropped-broken` — those are out of the trigger rotation.
4. For records with `trigger_mode == cli-exec` and `state == active`, do NOT emit a comment trigger line. Instead invoke them **deterministically via the runner** — do not shell out ad hoc. The runner is **serial** (it iterates the fleet one CLI at a time in `sequence_position` order, opener first; it is not a concurrent fan-out), so which reviewers it invokes depends on the round:

   - **Round 0 (fan-out):** invoke the whole active `cli-exec` fleet (all `activation: round-0` cli-subagents plus the `activation: opener`) — omit `--only` so the runner walks the full fleet.
     Pass `--tier` so the runner selects the tier-matched opener (`sonnet-opener` for sprint PRs;
     `opus-opener` for epic/phase PRs). `PR_TIER` is derived at the top of each bash block by
     calling the shared `bin/derive-pr-tier.sh` script (T7/#1280 — one implementation, no
     inlined logic) — each block re-derives independently because each is executed as a
     separate `bash -c` invocation and does not share shell state with prior blocks:

     ```bash
     # BEGIN-PR-TIER-DERIVATION
     # Canonical, single-implementation PR_TIER derivation (T7/#1280) — extracted from
     # what were 4 inlined, byte-identical copies into bin/derive-pr-tier.sh. Fix once,
     # test once. See bin/derive-pr-tier.sh for the full derivation contract (hotfix-head
     # recognition, review_tier= marker precedence/escalation, fail-closed behavior).
     _pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }
     PR_TIER="$("$(_pd_lib derive-pr-tier.sh)" --pr {{PR}} --repo {{github_repo}})" || exit 1
     # END-PR-TIER-DERIVATION
     ```

     ```bash
     # BEGIN-PR-TIER-DERIVATION
     # Canonical, single-implementation PR_TIER derivation (T7/#1280) — extracted from
     # what were 4 inlined, byte-identical copies into bin/derive-pr-tier.sh. Fix once,
     # test once. See bin/derive-pr-tier.sh for the full derivation contract (hotfix-head
     # recognition, review_tier= marker precedence/escalation, fail-closed behavior).
     _pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }
     PR_TIER="$("$(_pd_lib derive-pr-tier.sh)" --pr {{PR}} --repo {{github_repo}})" || exit 1
     # END-PR-TIER-DERIVATION
     CYCLE_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"     # one timestamp for this cycle
     # Resolver: finds script in .claude/bin/ (consumer) or bin/ (dogfood), whichever is present.
     _pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }
     # #1396: this loop's OWN session is the mid-action priority-signal-gate target —
     # pass --session/--board so a pending freeze/idle-hard/stop-work signal addressed
     # to THIS session gates the round BEFORE any reviewer CLI spawns (see
     # docs/dispatch-protocol.md §7b). SESSION uses the same branch-name-is-session-name
     # convention role capsules already use to arm self-poll (e.g.
     # templates/roles/internal/epic-lead.md "Start of session — arm wake loop").
     SESSION="$(git rev-parse --abbrev-ref HEAD)"
     . "$(_pd_lib _board.sh)"
     "$(_pd_lib run-cli-reviewers.sh)" --pr {{PR}} --repo {{github_repo}} --head "$HEAD_SHA" \
       --invoked "$CYCLE_TS" --tier "$PR_TIER" --session "$SESSION" --board "$BOARD"
     ```

   - **Rounds 1..N (serial — one reviewer per fix-commit):** invoke exactly the ONE `cli-exec` reviewer whose turn it is on this fix-commit via `--only <id>`, matching the documented serial flow (1:1 commit↔verifying-reviewer mapping). The mandatory opener leads each serial pass and is the last to clear on the terminal commit:

     ```bash
     # BEGIN-PR-TIER-DERIVATION
     # Canonical, single-implementation PR_TIER derivation (T7/#1280) — extracted from
     # what were 4 inlined, byte-identical copies into bin/derive-pr-tier.sh. Fix once,
     # test once. See bin/derive-pr-tier.sh for the full derivation contract (hotfix-head
     # recognition, review_tier= marker precedence/escalation, fail-closed behavior).
     _pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }
     PR_TIER="$("$(_pd_lib derive-pr-tier.sh)" --pr {{PR}} --repo {{github_repo}})" || exit 1
     # END-PR-TIER-DERIVATION
     CYCLE_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
     # Resolver: finds script in .claude/bin/ (consumer) or bin/ (dogfood), whichever is present.
     _pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }
     # #1396: same mid-action priority-signal-gate wiring as the round-0 fan-out above —
     # see that block's comment for the full rationale.
     SESSION="$(git rev-parse --abbrev-ref HEAD)"
     . "$(_pd_lib _board.sh)"
     "$(_pd_lib run-cli-reviewers.sh)" --pr {{PR}} --repo {{github_repo}} --head "$HEAD_SHA" \
       --invoked "$CYCLE_TS" --only "$REVIEWER_ID" --tier "$PR_TIER" --session "$SESSION" --board "$BOARD"
     ```

   The runner (`.claude/bin/run-cli-reviewers.sh`) iterates the selected `cli-exec` reviewers in `sequence_position` order (the `opener` first), invokes each reviewer's CLI with the PR diff, and posts each one's findings under the orchestrator account with the `<!-- cli-review id=… commit=<HEAD_SHA> invoked=<CYCLE_TS> -->` marker. On first review, or when no safe same-reviewer anchor exists, the runner reviews the full PR diff. On later single-reviewer reruns it auto-selects the latest verified clean same-reviewer anchor and reviews only `<base>..HEAD`, stamping `base_review=<base>`; use `--full` when a lead explicitly wants a full rerun, or `--since <sha>` to force a specific verified anchor. It posts a skip-note for any reviewer whose CLI is unauthenticated/unconfigured. **Write `last_invoked_ts = $CYCLE_TS` for each invoked cli-exec reviewer in the tracking comment** — the runner stamps the same value into `invoked=`, so the freshness check (Step 7 rejects stale same-HEAD markers from a prior invocation) lines up. **Runner exit code (#139/#150/#1156 calibration):** `0` = ran, cleanly-skipped, or honest-PENDING on transient friction → proceed normally. **`3` = the gate MUST block** — either (a) the always-mandatory opener failed to produce a real review for ANY reason, OR (b) a PRESENT mandatory-when-available reviewer (codex-exec) hit a GENUINE credential failure (rc 15) on its CLI stderr/exit channel. **`4` = runner-owned fleet cap refused the invocation before spawning another reviewer; surface the cap-hit signal and escalate instead of retrying.** **On `3` or `4`: surface it to the user and do NOT set `ready_to_merge`.** A non-opener reviewer's empty/non-conforming output, quota, rate-limit, free-tier paid-model/capacity, or not-installed state is honest-PENDING and the runner exits `0` — that is NOT a block and does not gate `ready_to_merge`. The full per-reviewer contract is the [CLI-subagent invocation protocol](../../docs/automated-review.md#cli-subagent-invocation-protocol-52); the runner is its executable implementation, so triggering the CLI fleet does not depend on the agent shelling out by hand.
5. Skip records that are **currently usage-limited** in this cycle (emitting a limited reviewer's trigger pings an exhausted bot and wastes a cycle; do not promote manual-only GitHub Claude as an automatic substitute).
6. If no records qualify because all remaining `active` records are usage-limited: **do NOT skip to Step 8**. Instead, post no retrigger comment but still proceed to Step 6 (wait) and Step 7 (re-fetch). In Step 7, apply the stall-count increment to each usage-limited `active` reviewer that has not posted a real review marker. After 2 stalls they transition to `dropped-broken`. This allows the loop to converge when active reviewers stay quota-limited. _Only skip to Step 8 when the trigger list is empty because ALL active records are `dropped-*` — with no usage-limited active records remaining AND no `cli-exec` reviewer invoked this cycle (an invoked cli-exec reviewer still needs a wait+classify pass; see the empty-trigger-list dispositions below)._

For the default seed record (`codex` seq=10) the algorithm above produces:

| codex state | Trigger lines |
|---|---|
| active | `@codex review` |
| dropped-* | **no comment-bot retrigger** — go to cli-exec/Step 8 handling |

_This table is illustrative for the seed configuration only. The authoritative decision is the registry-driven algorithm (steps 1–6 above): the "no retrigger" outcome applies only when the algorithm produces an empty trigger list for ALL active reviewers (including any promoted fallback reviewers and invoked cli-exec reviewers), not merely when Codex is dropped. Legacy/manual records such as `gemini` and `pr-agent` are not included unless a lead explicitly activated them for a one-off audit._

Post the retrigger comment via:

```bash
gh pr comment {{PR}} --repo {{github_repo}} --body "<trigger lines>"
```

All triggers appear on separate lines in the same comment body. Posting them together avoids two notification events and keeps the PR timeline tidy.

**After posting the retrigger comment, update the PR's review-state tracking comment** with the current bot states (format and update mechanism documented in the [State persistence](#state-persistence) section below). Do this before invoking `ScheduleWakeup` so the state is durably recorded.

If the registry-driven loop from steps 1–6 above produces an empty trigger list, the next action depends on WHY the list is empty:

- **All active reviewers are `dropped-*` AND no `cli-exec` reviewer was invoked this cycle** → skip posting a retrigger comment and proceed to Step 8 (stop condition check).
- **One or more `active` `cli-exec` reviewers were invoked this cycle** (they emit no trigger line, so the *comment* trigger list is empty even though work is pending — e.g. comment-bots are all `dropped-clean` but `opus-opener` is still `active`) → do NOT skip to Step 8. Proceed to Step 6 (wait) and Step 7 (re-fetch), where each invoked cli-exec reviewer is classified: its `<!-- cli-review … commit=<HEAD> -->` marker → clean/findings, or no marker → stall increment (→ `dropped-broken` at 2). This is what lets a cli-only active round (including a lone mandatory opener) converge instead of leaving the opener `active` indefinitely.
- **One or more active reviewers are usage-limited** (their trigger was skipped by step 5) → do NOT skip to Step 8. Proceed to Step 6 (wait) so their stall rounds can advance and they can eventually reach `dropped-broken`. Usage-limited reviewers must exhaust the stall cycle before the loop can terminate.

The key criterion is the reviewer _state_, not merely whether the trigger list is non-empty. A quota-limited `active` reviewer is not `dropped-*` and must be counted in the wait path.

### Step 6 — Wait another 10 minutes

Invoke `ScheduleWakeup` again with `delaySeconds=600`. Self-resuming prompt:

> "Resume iterating-pr-reviews for PR {{PR}} on repo {{github_repo}}. Start at Step 7: re-fetch and compare."

### Step 7 — Re-fetch and compare

Repeat Step 2 (including recovering state from the tracking comment; include `claude[bot]` only if GitHub Claude was explicitly invoked manually for this PR). Compare newly fetched reviewer comments against the set already addressed in the previous iteration.

A comment is "new" if its comment ID was not present in the previous fetch. Only count comments posted AFTER the Step 5 re-trigger.

For each **`active`** bot, evaluate against the clean-review definition:
- **Marker present + zero new P1/P2:** clean review. Transition to `dropped-clean`. Record `last_clean_commit` (current HEAD SHA) and `last_clean_ts`.
- **Marker present + new P1/P2 found:** not clean. Keep `active`. Reset `stall_count` to 0. Return to Step 4 to address the new findings.
- **No marker present (silent stall):** increment `stall_count`. If `stall_count >= 2`, transition to `dropped-broken`. Otherwise keep `active` and proceed.

For each **`dropped-clean`** bot, check whether it posted new P1 or P2 comments since the last retrigger on its own cadence:
- **New P1/P2 found:** re-activate (transition back to `active`, clear `last_clean_commit`). Return to Step 4.
- **No new actionable findings:** remain `dropped-clean`.

Also re-run the Step 4.5 usage-limit check on the freshly fetched comments — a bot that was available in earlier iterations may post a usage-limit message in this round.

After evaluating all bots, update the tracking comment with the new states, then proceed to Step 8.

### Step 8 — Stop condition check

Evaluate the current states of all **activated** reviewers — i.e., reviewers whose `activation` is `round-0` or `opener`, plus any `fallback-only` reviewer that was promoted via a usage-limit overlay and whose comments were fetched. This set spans **both** `comment-bot` and `cli-subagent` reviewers — the `cli-exec` fleet (#52) participates in the stop condition exactly like the comment-bots, recovered via their `<!-- cli-review … -->` markers (Step 2). Reviewers with `activation: fallback-only` that were never promoted (i.e. no usage-limit substitution occurred) do not appear in the tracking comment and are excluded from stop checks. The **tier-matched mandatory opener** (`sonnet-opener` for sprint PRs; `opus-opener` for epic/phase PRs — see `docs/automated-review.md` reviewer registry `tier` field) must be `dropped-clean` **on the terminal commit** before `ready_to_merge` — i.e. its `last_clean_commit` MUST equal the current HEAD SHA. **An opener's `dropped-clean` on a prior commit does NOT satisfy the stop condition if the HEAD has since changed** (#161) — a `last_clean_commit != HEAD` opener re-activates per rule 2 (see [Re-activation from dropped-clean](#re-activation-from-dropped-clean)) and must review the new terminal commit. A mandatory reviewer that is `dropped-broken`, that never reached `dropped-clean` (e.g. unauthenticated and skipped), or whose `last_clean_commit != HEAD` blocks the gate. This prevents setting `ready_to_merge` on a terminal commit the mandatory reviewer never saw.

- **All reviewers `dropped-clean`:** loop terminated successfully. Before setting `ready_to_merge`, run the **c-a2 enforced merge-gate** (see [C-a2 gate at terminal-SHA](#c-a2-enforced-merge-gate-at-terminal-sha) below). If the gate PERMITs (exit 0): return control to the caller with a merge-ready report listing which reviewers gave clean reviews and on which commits. Set `ready_to_merge: true` in the tracking comment. If the gate REFUSEs (exit 2) or returns MALFORMED (exit 3): surface the gate's refusal reason, do NOT set `ready_to_merge: true`, and halt the loop.
- **All optional reviewers are in a terminal state (`dropped-clean` OR `dropped-broken`) AND all mandatory activated reviewers are `dropped-clean` AND at least one activated reviewer is `dropped-clean`:** loop terminated, ready to merge (#163). `dropped-broken` optional reviewers satisfy the stop condition when all mandatory reviewers are `dropped-clean` — a broken optional reviewer does not block the gate. The backstop "AND at least one reviewer is `dropped-clean`" prevents a false-ready signal when ALL activated reviewers (including any mandatory ones) are `dropped-broken` and no reviewer was ever clean — that degenerate case is a broken pipeline, not a successful review. Before setting `ready_to_merge`, run the **c-a2 enforced merge-gate** (see below). If the gate PERMITs: note in the report which reviewers cleared and which were broken. Set `ready_to_merge: true` in the tracking comment. If the gate REFUSEs or MALFORMED: surface the reason and do NOT set `ready_to_merge: true`. _If a mandatory reviewer is `dropped-broken`, this condition does NOT apply — treat it as a broken pipeline even if optional reviewers cleared._
- **All reviewers `dropped-broken` (none clean), OR any `mandatory` reviewer is `dropped-broken`:** the review pipeline is broken. Do NOT silently proceed. Surface to the user with per-reviewer stall counts — e.g., "codex and the tier-matched opener both stalled N times — no reviewer gave a clean review. Options: wait for reviewers to recover, or merge anyway with explicit acknowledgement." Set `ready_to_merge: false`. Halt the loop.
- **At least one reviewer still `active`:** continue the loop. Return to Step 4 (if new actionable comments were found in Step 7) or Step 5 (if no new findings but the reviewer is active due to a single stall only).
- **User explicitly requests a stop:** honour immediately. Report the current state of open comments and exit the loop regardless of reviewer states.

### C-a2 enforced merge-gate at terminal-SHA

> **HARD LINE (operator + Phase Lead): mechanism-only, zero model calls.** The gate
> CONSUMES the assembled verdict; it does NOT generate reviews. Any model/SDK/anthropic
> call in the gate or assembly path is drift into the deferred review-quality half —
> stop and escalate.

When the stop condition evaluates to "ready to merge" (both `dropped-clean`/`dropped-broken` cases above), the loop MUST run the programmatic merge-gate before setting `ready_to_merge: true`. The gate is a **deterministic safety net**: it re-parses the raw `<!-- cli-review … -->` marker comments to verify the verdict independently of the state-machine bookkeeping. This catches any residual blocking findings even if the state machine had a bookkeeping error.

**Gate invocation (terminal-SHA = current HEAD):**

     ```bash
     # BEGIN-PR-TIER-DERIVATION
     # Canonical, single-implementation PR_TIER derivation (T7/#1280) — extracted from
     # what were 4 inlined, byte-identical copies into bin/derive-pr-tier.sh. Fix once,
     # test once. See bin/derive-pr-tier.sh for the full derivation contract (hotfix-head
     # recognition, review_tier= marker precedence/escalation, fail-closed behavior).
     _pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }
     PR_TIER="$("$(_pd_lib derive-pr-tier.sh)" --pr {{PR}} --repo {{github_repo}})" || exit 1
     # END-PR-TIER-DERIVATION
HEAD_SHA="$(git rev-parse HEAD)"   # or the tracked terminal commit SHA

# Use mktemp for the verdict file: avoids predictable /tmp path and TOCTOU clobber.
VERDICT_FILE="$(mktemp "${TMPDIR:-/tmp}/ca2-verdict-XXXXXX.json")"
trap 'rm -f "$VERDICT_FILE"' EXIT

# Resolver: finds script in .claude/bin/ (consumer) or bin/ (dogfood), whichever is present.
_pd_lib(){ local r; r="$(git rev-parse --show-toplevel)"; for d in "$r/.claude/bin" "$r/bin"; do [ -f "$d/$1" ] && { printf '%s' "$d/$1"; return 0; }; done; return 1; }

# Step 1 — assemble verdict from already-posted cli-review markers (parsing only).
# Capture assembler exit status explicitly; a non-zero rc means a fetch or parse failure
# (not a gate REFUSE), and its stderr describes the actual problem.
ASSEMBLE_RC=0
"$(_pd_lib assemble-verdict.sh)" \
  --pr "{{PR}}" --repo "{{github_repo}}" --head "$HEAD_SHA" \
  > "$VERDICT_FILE" || ASSEMBLE_RC=$?

if [ "$ASSEMBLE_RC" -ne 0 ]; then
  echo "[ca2-gate] assembly failed (rc=$ASSEMBLE_RC) — see assemble-verdict stderr above" >&2
  # Treat assembler failure as fail-closed: surface the error, do not set ready_to_merge.
  # Do NOT run the gate on a partial/empty verdict file.
  # NOTE: GATE_RC=3 here is an ASSEMBLER error (fetch / auth / parse), NOT a gate "MALFORMED verdict".
  # It is fail-closed in both cases, but the cause is different:
  #   - ASSEMBLE_RC != 0 → infrastructure/fetch/parse error in assemble-verdict.sh (retryable)
  #   - GATE_RC=3 from the gate → no parseable JSON object in the verdict (malformed input, needs investigation)
  # Check assemble-verdict.sh stderr output to distinguish the two.
  GATE_RC=3
else
  # Step 2 — run the enforced gate.
  # Pass --tier so the gate applies the correct opener requirement:
  #   sprint → sonnet-opener (or opus-opener as fallback)
  #   epic/phase/main (or omitted) → opus-opener
  GATE_RC=0
  /usr/bin/python3 "$(_pd_lib ca2-merge-gate.py)" \
    --verdict "$VERDICT_FILE" \
    --terminal-sha "$HEAD_SHA" \
    --tier "$PR_TIER" || GATE_RC=$?
fi
```

**Gate exit codes and dispositions:**

| Exit | Meaning | Action |
|---|---|---|
| `0` | PERMIT — `reviewed_sha == terminal_sha`, opener completed, optional-mandatory completed-or-skipped, `blocking == []` | Proceed: set `ready_to_merge: true`, surface merge-ready report |
| `2` | REFUSE — one or more gate conditions failed (stale SHA / missing opener / missing optional-mandatory / open blockers) | Do NOT set `ready_to_merge`. Surface the gate's stderr output. Return to Step 4 to address the identified gap. |
| `3` | MALFORMED — either (a) assembler failure: `.claude/bin/assemble-verdict.sh` exited non-zero (fetch/auth/parse error — check its stderr; may be retryable), or (b) gate MALFORMED: no parseable JSON object in the assembled verdict (malformed input — investigate the verdict file). | Halt the loop. Surface the error. For case (a), retry after resolving the infrastructure issue. For case (b), inspect the verdict file directly. |

**Gate contract (schema: `docs/ca2-verdict-contract.md` — FROZEN, reshaped per E2/S1 Epic Lead ruling):**
1. `reviewed_sha == terminal_sha` — verdict covers the exact commit being gated; a stale/drifted verdict cannot clear the gate.
2a. `REQUIRED_OPENER ⊆ reviewers_completed` — the tier-matched mandatory opener (`sonnet-opener` for sprint PRs; `opus-opener` for epic/phase PRs) must be in `reviewers_completed`; a skip is NOT acceptable for the opener.
2b. `OPTIONAL_MANDATORY ⊆ reviewers_completed ∪ reviewers_skipped` — for any `activation: round-0` cli-subagent (NOT the opener) that was activated in this loop, it must appear in `reviewers_completed` OR `reviewers_skipped`. In the default P11 configuration `codex-exec` is `manual-only` and is NOT in OPTIONAL_MANDATORY unless explicitly activated via `--only codex-exec`; in that case the `<!-- cli-skip … -->` marker satisfies completeness for it.
3. `verdict.blocking == []` — no open blocking (P1/P2) findings remain.

**Why this gate cannot be bypassed mid-loop:** the schema in `docs/ca2-verdict-contract.md` is frozen. Changing the verdict shape or the reviewer-policy constants (`REQUIRED_OPENER`/`OPTIONAL_MANDATORY`) requires updating the contract doc, the gate script, AND the test suite (`bin/test-ca2-merge-gate.sh`) together — the tests fail immediately on drift. This was the fix for issues #217/#223 (unfrozen spec relitigation mid-loop broke the enforcement invariant).

---

## Post-merge convergence and issue-spawning (#51)

Reaching `ready_to_merge: true` and merging is NOT the end of review. Blockers (any security finding;
any correctness P1/CRITICAL; anything that breaks behaviour or fails requirements) MUST already have
been fixed pre-merge — they are never deferred. But **non-blockers** (style/nits, low-severity
hardening, edge cases not affecting correctness/security) may have been deferred during the loop;
those are reconciled after merge:

1. **Spawn tracking issues.** For every deferred non-blocker, open a GitHub issue labelled
   `review-fleet-spawned` (one per finding, or grouped by theme), linking the PR + the originating
   review comment. The deferral reply on the PR thread MUST link the spawned issue (the third
   resolution mode in "What 'addressed' means").
   ```bash
   cat > /tmp/review-fleet-spawned-body.md <<'EOF'
<!-- pd-priority-routing -->
## Routing Prioritization
- Routing tier: Medium
- Sort order: 2
- WSJF: N/A - spawned from post-merge review follow-up
- RICE: N/A - score during VP grooming
- MoSCoW: Should
- Rationale: Deferred review-loop finding.
<!-- /pd-priority-routing -->

## Deferred Work

Deferred from #<PR> (<reviewer-id>): <detail> - <comment-url>
EOF
   gh issue create --repo {{github_repo}} --label review-fleet-spawned \
     --title "<deferred finding>" --body-file /tmp/review-fleet-spawned-body.md
   rm -f /tmp/review-fleet-spawned-body.md
   ```
2. **Keep reviewing to convergence.** If a reviewer posts further findings after merge (e.g. a slow
   re-review lands), triage them: blockers → immediate follow-up fix PR; non-blockers → additional
   `review-fleet-spawned` issues. The loop's review obligation converges, it does not stop at merge.
3. **VP weekly grooming.** `review-fleet-spawned` issues are groomed weekly by the VP (prioritise,
   schedule into a sprint, or close as won't-fix). This keeps deferred work visible and bounded
   rather than silently dropped.

This closes the gate-poller's blocker-vs-non-blocker contract: blockers gate the merge; non-blockers
are *tracked*, never lost.

---

## State persistence

The skill writes and updates a single tracking comment on the PR after every cycle. This comment is the durable store for bot states across `ScheduleWakeup` invocations.

### Tracking comment format

```
<!-- review-state-v1
iteration: 3
max_turns: 5
max_budget_usd: 10.00
spent_usd: 0.84
recurrence_n: 2
fleet_invocations: 2
max_fleet_invocations: 3
blocking_fp_counts: {"opus-opener:P1:auth bypass in login handler": 1}
last_retrigger_ts: 2026-05-14T15:23:00Z
codex: state=dropped-clean stalls=0 last_clean_commit=abc1234 last_clean_ts=2026-05-14T15:23:00Z
opus-opener: state=active stalls=1 last_clean_commit= last_clean_ts= last_invoked_ts=2026-05-14T15:23:00Z
ready_to_merge: false
cap_hit: false
-->

### 🔄 Review iteration state (auto-maintained by iterating-pr-reviews)

Round: 3 / 5 max | Budget: $0.84 / $10.00 | Fleet: 2 / 3 invocations

| Reviewer | State | Stalls | Last clean commit |
|---|---|---|---|
| Codex       | dropped-clean | 0 | abc1234 (2026-05-14T15:23Z) |
| Opus opener | active        | 1 | — |

Next action: invoke `opus-opener` through `run-cli-reviewers.sh --only opus-opener`.
```

`last_retrigger_ts` is the UTC timestamp of the most recent retrigger comment the skill posted (or the PR creation time if no retrigger has happened yet). It anchors the cycle-scoped scans for usage-limit messages and active review markers (see [Usage-limit fallback](#usage-limit-fallback) and [Clean review definition](#clean-review-definition)) — comments older than this timestamp are out of scope for the current cycle's checks.

The HTML comment block (`<!-- review-state-v1 … -->`) is machine-readable and must remain parseable. The human-readable table below it is for PR readers; keep both sections in sync.

### Writing and updating the tracking comment

**First write (no existing tracking comment):** post via the GitHub API directly so the response JSON gives you the comment ID for later PATCH calls. `gh pr comment` is the convenient wrapper but does NOT expose the comment ID in its output — using it for the initial post breaks the in-place update flow below.

```bash
COMMENT_JSON="$(gh api repos/{{github_repo}}/issues/{{PR}}/comments \
  --method POST \
  --field body="<full tracking comment body>")"
TRACKING_COMMENT_ID="$(printf '%s\n' "$COMMENT_JSON" | jq -r .id)"
```

**Subsequent updates:** PATCH the existing comment in-place using the captured ID (or the one recovered from the resume fetch — see below):

```bash
gh api repos/{{github_repo}}/issues/comments/$TRACKING_COMMENT_ID \
  --method PATCH \
  --field body="<updated tracking comment body>"
```

**Reading on resume:** when the skill resumes after `ScheduleWakeup`, it recovers state by fetching all issue comments and finding the most recent one from the PR author whose body starts with `<!-- review-state-v1`. The comment ID is the `id` field of that comment in the fetch response — use it for subsequent PATCH calls. Parse the key=value pairs from the header block to recover bot states.

### Field definitions

| Field | Type | Description |
|---|---|---|
| `iteration` | integer | increments each full cycle (Steps 2–8); checked against `max_turns` in Step 0 |
| `max_turns` | integer | hard round cap loaded from `orchestration.yaml` `review_loop.max_turns` (default **5** — the shipped default; 20 is only the documented upper ceiling). Written on first write so the resume path recovers it without re-reading YAML. |
| `max_budget_usd` | float or empty | optional budget cap in USD. Empty string if not configured — budget check is skipped. |
| `spent_usd` | float or empty | cumulative USD spend tracked across iterations. Empty if budget tracking is not enabled. |
| `recurrence_n` | integer | consecutive-round threshold for the semantic recurrence cap (default **2**). Written on first write from `orchestration.yaml` `review_loop.recurrence_n`. |
| `fleet_invocations` | integer | count of `.claude/bin/run-cli-reviewers.sh` invocations this loop. Incremented after each invocation in Step 5. |
| `max_fleet_invocations` | integer | fleet-invocation cap (default **3**). Loaded from `orchestration.yaml` `review_loop.max_fleet_invocations`; written on first write. |
| `convergence_round_cap` | integer | (#1402) plain round-count cap independent of recurrence (default **4**). Loaded from `orchestration.yaml` `review_loop.convergence_round_cap`; written on first write. |
| `blocking_fp_counts` | JSON object (inline) | `{"<fingerprint>": <consecutive-count>}` map — updated each round at Step 0 before the cap check. Fingerprints are produced by `.claude/bin/fingerprint-verdict.sh`. A fingerprint's count increments when it appears in consecutive rounds; it is dropped when it does not appear. |
| `cap_hit` | `true` \| `false` | set to `true` when the loop was stopped by Step 0 cap check (any of the five bounds). When `true`, loop is halted until Epic Lead re-arms. |
| `cap_reason` | string or empty | human-readable reason for the cap hit (populated when `cap_hit: true`). Mirrors the `reason=` field in the escalation signal body. |
| `last_retrigger_ts` | ISO-8601 UTC | timestamp of the most recent retrigger comment posted by the skill (or PR creation time on cycle 1). Anchors cycle-scoped scans for usage-limit messages and review markers. |
| `<reviewer-id>: state` | `active` \| `dropped-clean` \| `dropped-broken` | state for the reviewer with that registry id (e.g. `codex: state`, `opus-opener: state`) |
| `<reviewer-id>: stalls` | integer | consecutive silent rounds without a review marker from that reviewer |
| `<reviewer-id>: last_clean_commit` | SHA or empty | HEAD SHA when this reviewer last gave a clean review |
| `<reviewer-id>: last_clean_ts` | ISO-8601 or empty | timestamp of the clean review |
| `<reviewer-id>: last_invoked_ts` | ISO-8601 or empty | **cli-exec reviewers only** — UTC timestamp the loop invoked this reviewer in the current cycle (written in Step 5 at invocation). A `<!-- cli-review … invoked=<ts> -->` marker counts for the current cycle only if its `invoked=` matches this value (defeats stale same-HEAD marker reuse — see Clean review definition). |
| `ready_to_merge` | `true` \| `false` | set to `true` when the termination condition is met |

One set of `<reviewer-id>:` fields per active record in the registry — **both `comment-bot` AND `cli-exec` records** (for those that were activated). The default comment-bot field set is `codex:` only. Legacy/manual comment-bots such as `claude:`, `gemini:`, and `pr-agent:` appear only when explicitly activated for a one-off audit. The `cli-exec` mandatory opener (`sonnet-opener:` or `opus-opener:`, the only default `cli-exec` record in the default P11 fleet) ALSO persists its field set — in particular its `last_invoked_ts` (and `state`/`stalls`/`last_clean_commit`) — so opener state survives across `ScheduleWakeup` invocations and the freshness check (marker `invoked=` == tracking `last_invoked_ts`) lines up. `codex-exec` is `manual-only` — it appears in the tracking comment ONLY when explicitly invoked via `--only codex-exec`. Legacy explicit CLI paths such as Kilo/Antigravity have been removed — they are no longer active records and must not be invoked. Do NOT restrict the field sets to `comment-bot` records: dropping the opener's state across wakeups would lose the mandatory-gate freshness anchor.

---

## What "addressed" means

A bot comment is considered addressed when ANY ONE of the following is true:

- **(a) Fixed:** a code change was committed and pushed to the PR branch that resolves the concern raised.
- **(b) Rejected:** a reply was posted on the comment thread explicitly explaining why the comment will not be actioned.
- **(c) Deferred to a future phase/sprint:** a GitHub issue was created with `gh issue create`, a row was added to `PHASE-ROADMAP.md`'s Issue Summary Table assigning the issue to the target phase, that target phase's `ORCHESTRATION-PROMPT.md` (or the relevant sprint `PROMPT.md`) lists the issue in scope, AND a reply was posted on the original PR comment thread linking to the new issue. All four steps are required for a valid deferral.

Addressing means closing the loop on every comment — the bot, the user, and future reviewers can all see the outcome.

**Convergence — when the loop is "done."** The loop terminates on **all-findings-addressed**, NOT on "every reviewer emits zero findings." Adversarial LLM review of a non-trivial diff is non-convergent toward a clean sweep — each run surfaces new latent/edge/defensive observations, many of them false positives or already-handled — so "the mandatory opener must post zero findings" is unreachable on a large diff and chasing it is an infinite loop. A PR is **gate-clear** when (1) there are **zero open blockers** (security HIGH/CRITICAL or MEDIUM-untriaged; correctness P1/CRITICAL; broken behaviour) AND (2) **every** finding is addressed via (a) fix, (b) reject-with-evidence (incl. reviewer false-positives — cite the code that already handles it), or (c) track-with-justification (a `review-fleet-spawned` issue). The mandatory opener clears when its findings are *addressed*, not when it emits none. See `docs/automated-review.md` → "Gate convergence criterion" for the authoritative statement.

---

## Tier-aware round budget

The number of rounds to drive before cap-and-ship depends on the PR tier. This is the **soft** review-convergence discipline — separate from the hard caps (`max_turns`, recurrence, fleet-invocation). See `docs/review-depth-gradient.md` for the full table.

| PR tier | Round budget | Disposition |
|---|---|---|
| Sprint → epic base | **LOW end of 2–3 opener rounds** | Cap-and-ship at zero-BLOCKING is the **norm**, not the fallback. Once blockers are cleared, merge — do not iterate into style nits or latent observations. |
| Epic → phase base | 2–3+ rounds (DEEPER) | Full opener pass + address material findings; more latitude for cross-sprint coherence checks. |
| Phase → main | Full fleet (FULL gate) | Drive to convergence per `commands/review-phase-pr.md`; all checklist gates must clear. |

**Sprint-tier decision rule:** at zero-BLOCKING (no security HIGH/CRITICAL/MEDIUM-untriaged; no correctness P1/CRITICAL; no broken behaviour), the Epic Lead merges. Remaining observations are addressed via reject-with-evidence or deferred as `review-fleet-spawned` issues. No further rounds required unless the Epic Lead explicitly re-arms.

---

## Sprint 0 exception

This loop does NOT run for Sprint 0 trial PRs.

Sprint 0 PRs are `[DO NOT MERGE]` reference artefacts. Their Codex review is manually invoked by the user (per `running-sprint-zero-trial/SKILL.md` — "After opening the PR, stop and report the PR URL. The user invokes Codex to review."). The iteration loop is reserved for merge-bound PRs only.

**Codex S0 dry-run PRs** (`[Codex S0]` title prefix) are also reference-only artefacts opened by the Codex Sprint-0 lifecycle (`skills/running-sprint-zero-trial/SKILL.md`). They must NOT enter this loop — their review is user-driven.

Detect Sprint 0 / Codex S0 PRs by checking the PR title for `[DO NOT MERGE]`, `[NOT FOR MERGE]`, or `[Codex S0]` prefix before entering the loop.

---

## Never

- Never silently skip a bot comment — every comment must be addressed (fix, reject, or defer).
- Never address a comment by adding code that doesn't fully resolve the concern (e.g., adding a TODO comment in place of a real fix counts as a silent skip).
- Never retrigger the bots without having addressed all P1 and P2 comments from the previous round.
- Never enter this loop for Sprint 0 trial PRs.
- Never block the user's session by polling — always use `ScheduleWakeup` between iterations.
- Never silently merge when all bots are `dropped-broken` and none gave a clean review — surface the broken pipeline to the user first.
- Never post a retrigger comment with a trigger line for a `dropped-clean` or `dropped-broken` bot — those bots are out of the retrigger rotation.
- **Never iterate past any cap.** Step 0 runs first on every wakeup — no exceptions. An unbounded loop that ignores its cap is the failure mode #217, #223, and S1's round-35 runaway demonstrated. Escalate and stop; do NOT merge.
- Never invoke `.claude/bin/run-cli-reviewers.sh` when `fleet_invocations >= max_fleet_invocations` — check the fleet cap BEFORE invoking the runner.
- Never silently continue past a recurrence cap hit — if the same P1 persists 2 consecutive rounds, escalate per the same path as all other caps. Escalate-don't-iterate applies to bot-review loops just as it does to coding work.
- Never silently continue past a convergence-round cap hit (#1402) just because each round's findings differ from the last — disjoint findings are NOT proof of progress; they are the #1328/#1383/#1386 failure shape. Escalate per the tier-differentiated path (TL dispositive at sprint/hotfix; freeze + PL sign-off + TL adjudication at epic/phase/main) — never let the lead self-classify around it.
- Never increase `max_turns`, `max_fleet_invocations`, or `convergence_round_cap` unilaterally — only the Epic Lead may re-arm after reviewing the cap-hit escalation signal, and a convergence-cap re-arm additionally requires the tier-appropriate TL/PL step to have actually completed first.
- Never confuse the **soft** review-convergence discipline (~2–3 opener rounds, lead judgment) with the **hard** runaway ceilings (round cap, convergence-round cap, recurrence cap, fleet cap — all four are deterministic force-escalates). The hard caps fire early on a genuine runaway — they are NOT substitutes for the lead's cap-and-ship judgment on a normal PR.
