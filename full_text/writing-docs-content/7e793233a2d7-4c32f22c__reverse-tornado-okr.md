---
name: reverse-tornado-okr
description: >
  Plan or run a measured goal loop with anti-goal guardrails. Planning mode drafts metrics, discovery,
  and work structure without changing the workspace. When the user asks to run, delegate, automate,
  or resume the loop, execution mode may run bundled local helper scripts, write durable `.okra`
  records, spawn subagents, and optionally route writer work through an already-installed Codex or
  Claude CLI. Use for OKRs, metric-led improvement, bounded research, or progress that must preserve
  budget, quality, safety, trust, or another measured constraint. All actions remain inside the
  user's request and runtime permissions; the skill does not install tools, add credentials, grant
  authority, or contact external services on its own.
---

# The Reverse Tornado - running a goal as a self-correcting loop

This skill is a workflow. Give it any goal. It sets the goal up so an LLM can do most of the work
while a human keeps the direction.

Picture a reverse tornado. On day one you guess wide. Each loop narrows the guessing into known
work. A wall you cannot cross bounds every loop - that wall is the anti-goal. The loop stops when
the metric hits its target.

Apply the steps below in order. Do not skip the anti-goal. It is what makes the rest safe.

## Choose the operating mode

Default to **planning mode**. Draft the frame and loop in the requested output only. Do not run
helpers, create `.okra`, spawn workers, or call another model CLI merely because the skill loaded.

Use **execution mode** only when the user asks to run, delegate, automate, or resume the loop, or
when a repository's own instructions require the operating workflow for the requested change.
Before acting, keep the footprint clear:

- Bundled helpers read and write local files. They do not make network calls.
- Durable state lives under `.okra` only when that path is allowed. A stored permission record does
  not grant permission that the user or runtime did not grant.
- Subagents receive scoped packets and cannot expand their own authority.
- An installed Codex or Claude CLI is optional. Do not install it, authenticate it, or invoke it
  outside the user's requested delegated workflow. State which external model path will be used.
- Never send repository content, run evidence, or credentials to another service unless the user
  requested that model path and the runtime permits it.

If the requested output is only advice, a plan, or an OKR draft, stay in planning mode.

## Write plainly

Answer first. Use common words. When a choice needs context, show one concrete example or analogy,
then ask one clear question. Stop when the choice is clear. Skip praise, filler openings, soft
lead-ins, and abstract terms when a plain word works.

Example: "DKR-1 creates CKR-1, so we save that link. Should every link stay in history?"

Writing wall: `plain_wording_violation_count == 0`. It covers skill wording and new OKRA text
artifacts, not product source, data, or preserved model-dialect fixtures. Run the
`scripts/check-plain-wording.py` beside this `SKILL.md` on the changed text files. In an injected
Codex project, for example:
`python3 .codex/skills/reverse-tornado-okr/scripts/check-plain-wording.py <changed OKRA text files>`.
Judgement calls still need human or independent review.

## Step 1 - Draft the frame (metric + target, and the wall)

When you get a goal, mission, improvement, or research request, draft the frame first. Do not wait
for the user to phrase it as an OKR. Propose a **candidate objective**: the metric that would prove
success, a target or range when the facts support one, and a short note on why that metric is the
right proof. For research, the first objective can be about the decision itself - "reduce
uncertainty enough to decide X" - measured by confidence, decision readiness, evidence coverage, or
risk retired. Keep it candidate until the intended outcome, metric, and limits are recorded clearly
enough to run. Human input helps define that intent; it is not proof that the frame or approach is
correct.

Pin two things before any planning:

- **Objective**: a metric with a target number, not a vibe. "Grow monthly sales to $500k", not
  "do better at sales". If the goal is vague, propose the metric that would prove it, say it is a
  candidate, and record the user's intended outcome before any state-changing move.
- **Anti-goal**: the thing you must not sacrifice, with **its own metric**. "Keep monthly expense
  at or under $80k." It is either continuous (a drift gauge you watch) or binary (a tripwire that
  halts). Say which.

Anti-goals may carry across runs. If none is named, propose fit-for-purpose walls for budget, quality,
trust, safety/privacy, authority, time, storage, eval regression, stale memory, and single-LLM truth.
Give each a metric and an activation condition at approach, plan, or task level. Include relevant
non-functionals such as observability, recovery, performance, operability, and testability. Freeze
thresholds for the run; only the human changes them in a new frame. Lifecycle detail:
`references/matched-abstraction.md`.

OKRA always carries one inner integrity anti-goal, even if the user does not set one:
`anti_goal_bypass_or_dishonesty_count == 0`. It does not replace the user's domain anti-goal. It
stops the loop from bypassing, weakening, hiding, or faking the anti-goal machinery itself. Hitting
the objective by getting around the wall is not a valid OKRA success.

The frame moves **candidate -> recorded working**. Human input records intent and constraints, not
effectiveness; metrics show outcomes and DKRs reduce unknowns. Contradiction opens a frame review;
the objective and walls never change silently. Unmeasured harm is the cheapest way to hit a goal, so
a goal without a named wall is not a valid success. Delegated loops also record an **action envelope**:
allowed moves, forbidden moves, limits, data boundaries, approval gates, rollback, and coverage of
harms considered and rejected. Coverage also names non-negotiable tripwires, owners, review cadence,
and what it does not cover. A metric-safe move can still be outside authority. One measured wall is
required.

Every anti-goal you confirm must be **readable or funded to become readable**: it carries either (a) a
metric with a working read method, or (b) a named **reducing DKR** funded to make it readable. A wall
you cannot read is not a wall, so an anti-goal with neither cannot be confirmed. The coverage review
lists each confirmed wall's status; delegated artifacts emit it as a commanded compact line that starts
**"Anti-goal coverage:"** naming each wall -> `readable` | `reducing-DKR <id>`. Metric shape:
`anti_goal_coverage_gap_count == 0` - an unreadable, unfunded wall is a coverage gap.

Any delegated, audited, or reused wall must be executable: record metric id, threshold, type, source,
method, freshness, evidence refs, replay checker, all three eval-point traces, and the fail-closed
flag. Reject invalid, superficial, tautological, false-positive, unsupported, or assertion-only
claims (`invalid_anti_goal_acceptance_count == 0`, `superficial_anti_goal_acceptance_count == 0`,
`tautological_anti_goal_acceptance_count == 0`, `false_positive_anti_goal_acceptance_count == 0`,
`unsupported_claim_acceptance_count == 0`, `single_llm_truth_acceptance_count == 0`, and
`anti_goal_bypass_or_dishonesty_count == 0`). Full fields: `references/executable-claims.md`.

## Step 2 - Know the three units

Break work into exactly three kinds. Keep them separate. Blurring them is where these systems rot.

- **DKR - Discovery.** A scoped probe at one uncertainty, not generic research. It names the
  steering decision it unlocks, the risk or anti-goal uncertainty it reduces, a turn/time budget,
  stop rule, evidence, confidence, candidate CKRs, and next unknowns. It returns a learning
  checkpoint or a replayable empty result.
  **Candidate CKRs and candidate PKRs are not promoted until the orchestrator accepts the supporting
  DKR learning checkpoint.** An executable checkpoint names `conclusion_id`, `decision_target`,
  `source_of_truth`, `read_method`, freshness quartet, numeric `confidence`, `evidence_refs_or_hashes`,
  `replay_command_or_checker`, answered/unanswered questions, decision, and fail-closed flag. It also
  carries `active_anti_goals`, complete `active_anti_goal_verification`, and `wall_gate`; every wall
  must be fresh and `held` before downstream work. Missing, stale, contradicted, or non-replayable
evidence blocks it, including wrong-source evidence. Raw inline commands are not replay checkers. See
  `contracts/executable-dkr-checkpoint.v1.json` and `references/executable-claims.md`.
- **CKR - Contribution / Key Result.** Measurable, with its own metric. This is what counts toward
  the objective. A CKR is **context and measurement, not a worker job**. It tells the orchestrator
  which contribution would matter and what direct metric proves it. It is never dispatched as work.
  Each CKR carries its own mini reverse tornado: what discovery makes the contribution meaningful,
  what direct CKR metric proves movement, and what delivery path becomes PKR work once the
  uncertainty drops.
- **PKR -> task - Progression.** Known work: do-and-check, no discovery. Emit progress signals as
  governed append-only events (hand-back, regression, rework, late discovery, empty DKR, ungoverned
  write); counters are derived by `okra-store.sh counts`, never typed. Each PKR carries its activated
  walls. In delegated output put **"active anti-goals:"** on its own line with metric ids and reasons;
  a done claim needs target plus fresh verified walls in the same `claim_acceptance` record:
  `active_anti_goals`, complete `active_anti_goal_verification`, and `wall_gate`. See
  `references/integrity-store.md` and `references/matched-abstraction.md`.

The abstraction levels are `approach ~ DKR`, `plan ~ CKR`, `task ~ PKR`. Each DKR names its returned
approach artifact; it grows while the hypothesis holds and is decommissioned when it goes off-track.
See `references/matched-abstraction.md`.

## Step 2b - Two roles: orchestrator and workers

The loop runs as an **orchestrator** directing disposable **workers**. This split carries the
authority lines. Each tier hands control *up* when it reaches the edge of its authority.

**Orchestrator - the loop's brain.** Only the top-level main session runs it; never dispatch the
orchestrator as a worker. Only it talks to the human; only the human changes the frame. It holds the
read-only frame, owns objective checks, the OKR board,
check-ins, three-point wall evals, budgets, flags, and subagent steering. It accepts DKR learning
only when the checkpoint makes the next steering decision safer or clearer, before CKR/PKR promotion;
it does not execute worker tasks or edit the frame. It does not stop when the board or worker queue is
complete. It keeps checking and dispatching **until the objective metric reaches target**, a human
changes/stops the frame, or a blocking flag needs resolution.

**Workers - the hands.** Scoped, disposable, parallelizable: discovery, progression, verification,
and challenger. CKR stays orchestrator-owned context.

- **Discovery** runs one DKR and returns its checkpoint; **progression** runs one PKR.
- **Verification** deterministically replays a claim and returns an audit trace, never judgement
  (`references/roles/validator.md`); separate writing and verification protect
  `single_llm_truth_acceptance_count == 0`.
- **Challenger** returns `intact | drifted | dead` for each live hypothesis, never a decision
  (`references/roles/challenger.md`). Use it only at hypothesis-touching junctures.

The main worker rule: **a worker that hits an unknown mid-run does not improvise - it hands back to
the orchestrator**. Workers stay within scope, do not screen their own wall cost, call the human, or
change scope.

Long runs write `.okra/runs/<run-id>/workers/<worker-id>/progress.jsonl` at finish, unknown, and
heartbeat; ten minutes is the default. In delegated output use these commanded lines:
**Worker progress:** `.okra/runs/<run-id>/workers/<worker-id>/progress.jsonl`, written at each worker
finish, unknown hit, and heartbeat. **Heartbeat cadence and next_check_at:** ten minutes by default,
with the next scheduled check recorded.

Every worker dispatch is a **worker prompt packet**, not a raw chat continuation. It carries
`frame.objective`, `frame.anti_goals`, `active_anti_goals`, `frame.action_envelope`,
`frame.human_confirmation_boundary`, `current_state`, `previous_dkr_checkpoint`, `assignment`,
`budget_and_stop_rule`, `hand_back_rule`, and `output_schema`. The full wall set is context; the
activated subset gates the unit. **In-progress worker narrative is not evidence; only worker progress,
check-ins, metric reads, flags, or accepted checkpoints can influence the next dispatch.**

Use **generic subagent spawning** with no custom agent definitions or plugins, and the verbatim
canonical role header from
`references/roles/orchestrator.md`, `writer.md`, or `validator.md`; if unavailable, run the same
template as a sequential role-switched pass and still write worker evidence. Run `okra-preflight.sh`
at start and record its transport.

If preflight reports `cross_model_writer`, a GPT writer may use the same `writer.md` packet while
verification stays on the session model; this strengthens `single_llm_truth_acceptance_count == 0`
but is optional.

Delegated output hard gates: `Action envelope:` allowed and forbidden moves plus the permission
owner; `Anti-goal coverage:` each wall -> `readable` | `reducing-DKR <id>` with
`anti_goal_coverage_gap_count == 0`; `CKR-level discovery/delivery balance:` the discovery side and
delivery path; `progress signals:` the events that steer the next check-in; `active anti-goals:`
activated wall ids and reasons; `Introspection cadence:` checkpoint, flag, descent, terminal, and
every-third-check-in triggers; `Standing walls:` walls that remain after terminalization and their
human-only retirement rule. Use this exact sentence: **"DKRs are discovery-worker scopes; PKRs are
progression-worker execution units; there is no CKR worker."**

Detect the model from harness ID/env, never self-report, and phrase packets accordingly; contracts
do not change by model. Delegated output must carry **"Model phrasing:"** with detected id, source,
and the quoted matching `Phrasing profile id` from `references/models/`; unknown models use
`references/models/README.md`. The id is the read-proof.

In delegated/scored loops, each packet records a rough write-once estimate and the actual at finish;
the pair feeds `est_overrun_ratio` and `estimation_calibration_error`. Light goals may skip it.
Details: `references/integrity-store.md` (Estimation Records).

The authority gradient:
`human owns the frame -> orchestrator works inside it and makes the loop's calls -> workers execute
inside their scope and hand back at their edge.`

## Step 2c - Make the run idempotent (set up storage first)

For any delegated, recurring, or side-effecting run, initialize storage before a move and stay inside
the allowed write scope; if the user or harness permits one output file, do not create an extra `.okra`
run store. The frame is
write-once; the tree is a generated view of node/edge events; moves are write-once by stable
idempotency key; metric reads, flags, check-ins, and worker progress are append-only. The
orchestrator checks a key before dispatch and records its result after. A known key replays its stored
result instead of repeating the effect.

**Write the record before the prose.** For every claim class with a contract under `contracts/`, fill
every field, write the record, and make the narrative cite its seq, hash, or path. A cited worker
ref must resolve to `.okra/runs/<run-id>/workers/<worker-id>/progress.jsonl#seq=N`; prose is never a
record. Write through the store helper, or a target path plus content hash; avoid ungoverned reads and
writes. Use content hashes for important inputs and `okra-store.sh scan` to make resume complete.

**Storage integrity:** append-only records are the source of truth; status/progress files are generated
views; claims are accepted only on independent deterministic evidence, not one LLM's say-so.

Use `.okra/runs/<run-id>/` for mutable state and shared `.okra/content/sha256/` for blobs. Concurrent
runs must not share a ledger, flags, check-ins, workers, move results, or status view. Run
`okra-preflight.sh` at start and record its `{"transport", "subagents", "detected_via"}` verdict.
Keep the exact frame/tree schema and `orchestrator` ownership of **objective checks** and
**subagent steering** from `references/integrity-store.md`. A human input that changes intent,
threshold, envelope, or denominator bumps `frame_version` before the move. A propose-cost dry-run
has no side effect and needs no key; only the committing move is keyed. Verify before resume or
success. Full layout, helper commands, and metric-read shape: `references/integrity-store.md`.

## Step 2d - Keep the run fresh and learn at check-ins

Before dispatch, define each objective, CKR, and anti-goal read: source, owner, definition, method,
`observed_at`, `recorded_at`, `fresh|stale`, and `max_age`. Every round writes `current_round`, open
flags, the last read, and `next_check_at`. Refresh stale data or fund a DKR; approval cannot make it
fresh. Run admissibility before a move, direct reads after it, and the paired goal/wall read at
progress time.

For delegated work, check in on worker finish, unknown, flag, and a ten-minute heartbeat. Each
check-in records estimate vs actual (`est_overrun_ratio`), steering value (`no_value_checkin_count == 0`),
four sweeps (`hallucination_sweep`, `missing_context_sweep`, `unexpected_results`,
`anti_goal_violation_review`) with `{claim, evidence_ref, verdict}` (`unchecked_claim_count == 0`), and an `uncertainty_5why` ending
in a `reducing_dkr` or `none-open`. Record `problem_restatement`, `evidence_delta`,
`alternatives_considered`, `assumptions_at_risk`, and `dkr_decision`; empty review is
`empty_first_principles_review_count == 0`. Threshold crossings create provenance-backed candidate
`reinforcement_record`s; current evidence and a recorded frame review are required before promotion.

At DKR acceptance, a flag, descent before task commitment, terminalization, or every third check-in,
run introspection: matched-abstraction violation review (`unleveled_violation_count == 0`); an
independent challenger verdict `intact | drifted | dead`; target selection; a Socratic packet with
`This round shapes:` and 3-6 evidence questions (`target_undeclared_packet_count == 0`); then next
DKR/CKR/PKR packets and dead-hypothesis decommissioning (`unjustified_node_contribution_count == 0`). The
orchestrator cannot self-certify a node or hypothesis. Details: `references/operating-loop.md`,
`references/introspection.md`.

## Step 2e - Learn, heal, and reuse memory

Allocate DKR budget where uncertainty blocks safe steering. Keep candidate CKRs/PKRs unpromoted until
accepted learning, and treat flags, vetoes, flat metrics, unknowns, and exhausted budgets as steering
evidence. At run start, run `okra-store.sh anti-goals .okra` and `init-run`; review every snapshot
candidate as `keep` or `drop` with a reason, evidence refs, and shaped nodes
(`prior_anti_goal_review_gap_count == 0`).

Learning stays candidate-only until current evidence supports a frame review. A reinforcement needs
`context_key`, trigger, `event_refs`, candidate anti-goal, status, and `no_regression`; missing refs
are `reinforcement_without_provenance`. A DKR may mint a run-local wall, but later frames keep, change,
or drop it only from fresh evidence and a recorded reason.

Terminalize only after recording terminal state, objective and wall reads, flags, accepted
checkpoints, retained traces, continuation packet, and second-opinion evidence. **Classify each
frame anti-goal** `retired_with_run` or `standing` (**standing is the default**); terminal “all held”
is a **point-in-time read, not a discharge**, and a later touch reactivates the wall. Human-only
context retirement ends it. Do not terminalize with unverified run-local candidates or artifacts from
a dead hypothesis. Keep reusable candidates in `candidate-anti-goals.v1.json`, never hidden defaults.

After consolidation, run `okra-store.sh doctor`, preview cleanup, and apply cleanup only to a
verified, terminalized, consolidated run. On a post-terminal edit to a standing-wall artifact,
re-read the standing set, record admissibility by metric id, record the frame input before editing,
open a successor inheriting the walls, and take the paired goal/wall read after editing. Details:
`references/learning-memory.md` and `references/matched-abstraction.md`.

## Step 3 - No cascade: read the real metric

The tree of work is **scaffolding, not scoreboard**. The only score that counts is the **direct
metric** - the objective's number and each CKR's number - read fresh from the source.

A finished subtree with a flat objective metric is **not** success. If the lag window is still open,
mark the branch `waiting_for_measurement` and schedule the next read. Once the lag window has closed
and fresh reads still show no movement, the flat metric tells you the breakdown was wrong. Never
infer progress from completed tasks. Measure the world directly. The same goes for the anti-goal:
measure breakage where it happens, never roll it up.

When a progress claim (a no-cascade direct read or a PKR done claim) will be delegated, audited, or
reused, make it **executable** before accepting it, exactly as with the anti-goal: name the
`metric_id`, `source_of_truth`, `read_method`, the freshness quartet, `target`, `comparator`, and the
read `value`, `evidence_refs_or_hashes`, a `replay_command_or_checker`, `decision`, and the
fail-closed flag. A finished PKR is not itself progress; cascade acceptance is rejected, as are
superficial, tautological/default-done, false-positive, unsupported, and single-LLM-truth progress
claims. An accepted done claim whose `value` misses the `target` under the `comparator` is rejected.
A **PKR done claim also carries the wall gate**: `active_anti_goals`, one complete
`active_anti_goal_verification` entry per active wall, and `wall_gate`. Each wall entry uses the
same structured fields as a DKR output. Done is accepted only when the metric meets target and every
wall reads exactly `held` from fresh replayable independent evidence. Pending, unknown, empty, stale,
unread, or breached walls block done. Use a parseable `max_age` such as `10m` or `PT10M`, and cite a
separate `verification_record_ref`. Set `wall_gate.verdict` to `held`, set `downstream_advance` to
`allowed`, and read `decided_at` from the clock when making the decision. Write numeric wall
`value` and `threshold` fields as JSON numbers, not quoted strings. Record acceptance only in a
`claim_acceptance` record with those wall fields; a validator progress record reports replay status,
not an `accepted` PKR decision.
See `contracts/executable-progress-claim.v1.json` and `references/executable-claims.md`.

## Step 4 - Run the zig-zag (discovery <-> execution)

This is not waterfall (discover everything, then build everything). It is a **zig-zag** that narrows:
learn a slice -> act on it -> that action surfaces the next unknown -> discover that -> act again.
The swings shrink as guess turns into known work. That narrowing *is* progress.

Read the zig-zag as a **quadrant**: abstract-to-detail down the vertical, uncertain-to-certain along
the horizontal. A DKR probe moves the line **right** (buys certainty at the current level). A descent
moves it **down** (adds detail: approach -> plan -> task). Delivery lands **bottom-right**.
**Bottom-left is the reckless zone** - detail committed without certainty, moving without learning.
DKR is the steering bend where the loop picks right or down. Hence the **no-level-jump rule**: an
artifact two levels down with no accepted parent one level up (a task/PKR artifact with no accepted
plan/CKR parent) is a jump - `abstraction_level_jump_count == 0`. When a review needs more detail to
judge, **spawn another DKR instead of stretching the turn**. Short steerable turns beat long wrongable
ones. See `references/matched-abstraction.md`.

Save how the quadrant changes, not only its latest nodes. Append a `node_event` when a DKR, CKR, or
PKR changes state. Append an `edge_event` when one node refines, proposes, supports, authorizes,
decomposes into, hands back to, or retires another. An uncertain link stays `candidate` and carries
confidence; it does not pretend to be definite. The current tree's `graph` is rebuilt from the
latest event for each id. Each edge carries `edge_id`, `from_node`, `to_node`, `relation`,
`status`, `confidence`, and `source_ref`.
Each `source_ref` names a file, ledger record, or content hash that a reviewer can open.
See `contracts/quadrant-graph-event.v1.json` and `references/integrity-store.md`.

Keep every bend clean. When an **execution task hits an unknown mid-run, it hands back up** - "this is
not execution anymore, this is discovery" - and the loop decides whether to fund a fresh probe before
resuming. Never let a task quietly muddle through a discovery it cannot see the end of. You are always
either executing known work or running a scoped probe, never pretending one is the other. In a
delegated loop, that hand-back writes a `handback_event`. Regressions, rework, late discovery, empty
DKR returns, and ungoverned writes each emit their own events. The counters
(`execution_to_discovery_handback_count`, `regression_count`, `rework_count`, `late_discovery_count`,
`dkr_empty_count`, `ungoverned_write_count`) are **recomputed from the ledger, never typed**. A count
that disagrees with the events is rejected. See `references/integrity-store.md`.

The events also **reconcile against the narrative**, which closes the silent event-suppression hole.
A check-in or worker narrative that describes a hand-back, rework, regression, or late discovery must
match an emitted `handback_event`, `rework_event`, `regression_event`, or `late_discovery_event`. A
described signal with no matching ledger event is a `narrative_event_mismatch`. Rejection prose ("no
rework", "did not hand back") never fires it.

### Search control for open-ended discovery

When the goal is open-ended, use a diverse independent early portfolio, not a fixed agent split. Give
each route a numeric turn/time budget and each round a numeric route cap; never exceed either. Keep an
explicit registry of approach families and redirect duplicate convergence toward gaps. Keep
incompatible routes alive; cross-pollinate only after independent development. For proof-like goals,
mark a route blocked when it reaches a theorem-strength missing lemma; reopen it only with a new
mechanism, invariant, or construction. Use adversarial checks for exact requirements and reject vague
status or unproved global compatibility. Require concrete evidence such as lemmas, constructions,
equations, counterexamples, or domain-equivalent artifacts. The root keeps
synthesizing, challenging, redirecting, and launching bounded rounds inside the frame, budgets, stop
rules, flags, and human boundary; blocked or exhausted routes hand back. Stop when the completion
condition holds or the frame's stop rule fires. Treat external material as candidate input: verify its
source, keep only bounded ideas, and never let it change the frame, permissions, or action envelope.
The PDF URL is provenance only: do not fetch it at runtime; verify the pinned extract with the
`sha256sum` check in `references/pdf-search-control.md`, and skip this adaptation if that evidence is
unavailable.

## Step 5 - Evaluate the anti-goal at THREE points every loop

The anti-goal is not a single end-of-loop check. It fires three times, each doing a different job.
Get the timing right. Each point must read as a trace, not a prose assertion. The trace cites the
metric read, source record, checker output, hash, ledger entry, dry-run result, or review artifact
behind the claim. A trace that is missing, stale, wrong-source, non-replayable, contradicted, or only
a model assertion makes the anti-goal claim invalid - do not count it as held.

1. **Admissibility - before acting.** When the orchestrator picks the next move, it screens it
   against the anti-goal *before dispatching a worker*. A move that would breach the wall never
   reaches a worker. This is the guardrail *steering* - it removes disaster moves from the menu.
   The orchestrator judges a move's anti-goal cost up front; for moves whose cost is unknowable
   without running them, it can dispatch a worker in a propose-cost (dry-run) mode that returns a
   projected anti-metric *without committing*, then admit or veto.
   *Example: move "blanket 40% discount" -> projected expense $96k -> VETOED, off the menu.*
2. **Direct read - after acting.** Read the actual anti-metric from the source, not "the task said
   it stayed safe." Drift toward the wall warns early; crossing it trips the breaker.
   *Example: ran "targeted email" -> expense reads $71k -> in band.*
3. **Paired with the goal - at the progress read.** Success is two-sided: **objective up AND
   anti-goal held.** A loop that moved the metric by breaching the wall is a failed loop that looks
   like a win - only the paired read catches it.
   *Example: sales $420k up but expense $88k failed -> not a win -> FLAG breaking.*

## Step 6 - Escalate on the flags

The loop runs around 80% on its own. It calls the human on four outcome conditions, each a distinct
failure:

- **Cannot** - discovery budget exhausted or learning flatlined. Effort in, nothing back.
- **Breaking** - an anti-metric drifted or tripped. The loop started making it worse.
- **Pointless** - **"Pointless opens when work finished or a CKR metric moved, but the objective
  metric stays flat / does not move after the lag window."** This guards the tornado's worst trap: the
  funnel narrows toward the **wrong tip** - converging neatly on a target that will not move the goal.
  Narrowing without the metric moving -> re-aim.
- **Stalled** - **"Stalled opens when a branch's computed risk stays flat and at or above the
  certainty threshold across the trailing check-in window while it keeps committing, never on absolute
  risk height."** A tall but pre-commit or still-draining funnel does not stall. Stalled is the
  leading indicator: it catches a branch avalanching on input risk before `pointless` and `breaking`,
  which are lagging output signals. The risk is recomputed from the ledger, never typed. See
  `references/integrity-store.md`.

Run all four outcome flags at once. Drop any one and a class of silent failure slips through.

For delegated loops, also raise **Authority drift** when the loop or a worker tries to change the
frame silently, relax a threshold without evidence, expand scope, bypass a permission gate, contact
a human directly, or act outside the recorded action envelope. This is an authority breaker, not
just an invalid move.

Flags have lifecycle. They are `open`, `acknowledged`, `resolved`, or `waived`. `breaking` pauses
committing moves by default; `cannot` and `pointless` stop the affected branch; `stalled` pauses
committing moves on that branch only while discovery stays allowed, and is **waived only by a human**
whose record carries approver evidence (an agent self-waiver is a bypass); `authority drift` stops the
proposed move and goes to the human. The orchestrator may resume only inside the recorded resolution.

## Step 7 - Separate intent, evidence, and permission

The human supplies intended outcomes, context, preferences, and permission boundaries. Those inputs
can be incomplete, mistaken, or contradictory; they are not the source of truth about whether an
approach works. Fresh objective and anti-goal metrics show outcomes. DKRs reduce material unknowns
and test assumptions. The loop must never silently switch the objective or weaken a wall to claim
success: record the contradiction, alternatives, and rationale, then review the frame. The action
envelope remains a hard permission boundary even when evidence favors a move.

Retiring a standing anti-goal remains a recorded context-retirement decision: reaching the objective
or terminalizing the run is a point-in-time read, not a discharge. A wall stays attached to the
artifact and context it guards until that context ends (merge, handoff, decommission); until then a
later request that touches that surface re-activates it.

Why this matters. If the loop can silently rewrite the goal, it can satisfy anything by retreating
to a target it already hits. If it blindly follows a person despite contradictory evidence, it can
also fail cleanly and repeatedly. Recorded intent plus outcome metrics, DKR learning, alternatives,
and permission boundaries avoid both traps. The loop is **best-effort**: it must try
against the goal it was given. When effort goes in and the metric stays flat, it reports the gap and
hands up the evidence - budget spent, tree built, contributions done, flat metric. The human decides.

No matter how much runs on its own, someone eventually makes the call - and the call belongs to a
person.

## A read on where you are

The **width of the funnel** - the ratio of discovery to execution in recent loops - tells you where
you are. Wide and still guessing means early, far from goal. Narrow and mostly known work means
close. This is a progress signal, but not the direct metric: the metric says *whether* you have
arrived; the funnel width says *how close* you are on the way. It stays honest only while "more
known" and "closer to goal" move together - which is what the pointless flag protects.

## Scale the apparatus to the goal

Match depth to the stakes. Not every goal needs the full machinery. For a light or personal goal, the
core is just: **a metric+target objective, a measured anti-goal, and the no-cascade habit of reading
the real metric instead of counting tasks done.** Lead with that.

Bring in the heavier parts - orchestrator/worker split, idempotent storage, the formal three-point
eval, the flags - when the goal is being run as an actual automated loop, has real side effects
(spend, sends, deploys), or the user asks how to run it. Offer them rather than front-load
them on someone who just wants help shaping a goal. The reverse tornado is the same shape at every
size; you do not always need to draw the whole funnel.

The delegated tier also carries the governed-integrity apparatus - process-signal events, the
computed risk register, the `stalled` flag, and write-once estimation records (est-vs-actual
calibration feeding `est_overrun_ratio`) - so risk and cost stay replayed numbers, not assertions;
see `references/integrity-store.md`. Light goals keep only funnel-width reads.

## Output

Match the output to the operating tier. For a light goal or advice, give only objective + target, one
named anti-goal with its metric and type, and the no-cascade read. For an executed recurring loop,
deliver the structured loop: the CKR/DKR/PKR decomposition, the three eval points instantiated for
this goal, flags, working frame, and action envelope. The action envelope is a permission limit: a
file in the run store cannot grant authority that the runtime or user did not grant. Use the user's
real domain throughout - do not leave the example abstract. Preserve exact metric literals from the
source material in addition to any explanation; if the source says `12 per 100`, include that exact
phrase instead of only a paraphrase.

When the user wants to run the goal over time, also deliver the **Operating Loop**: cadence, current
round, metric freshness contracts (keep `observed_at`, `recorded_at`, `fresh`|`stale`, and `max_age`
in one row or sentence), lag windows, `next_check_at`, stale-data policy, and flag lifecycle. See
`references/operating-loop.md`.

When the goal will recur in the same project, also deliver an **OKRA Learning Memory** section:
previous-run inputs scanned, traps, avoidances, misconceptions, optimization candidates, reusable
candidate anti-goals with metrics/evidence/confidence/context-fit/confirmation_status, terminalization
or continuation-packet status, trace and review-set refs, a **stress-allocation note** (the run's
stress and how the orchestrator allocated under it), and each memory record's **dependencies**. See
`references/learning-memory.md`.

**Delegated, automated, or scored loop?** Open `references/delegated-output.md` and satisfy **every
numbered line in it** - an artifact missing any line is incomplete. Do not write the delegated
artifact from memory of this skill; build it against that checklist, instantiating each line for the
current goal.

If the user wants a visual or shareable explainer, produce a self-contained HTML artifact. See
`references/artifact-guide.md` for how (and how to keep the artifact within its own anti-goal:
single file, no external runtime, no decoration that does not carry meaning).

## Common mistakes to avoid

These are the non-obvious traps - the ones a reader of the steps above still walks into. Each step
already states its own rule; this list is only the failure modes worth flagging twice.

- Accepting an anti-goal hold claim that is superficial, tautological/always true, false-positive,
  stale, wrong-source, non-replayable, contradicted, or backed only by a model assertion.
- Saving a DKR or PKR result without structured wall confirmation, or allowing downstream work while
  any active wall is pending, unknown, empty, stale, unread, or breached.
- Keeping only the latest quadrant nodes and losing the DKR -> DKR/CKR/PKR links that explain how
  the run changed.
- Dispatching a PKR without `linked_ckr`, `source_dkr_checkpoint`, and `contribution_metric`.
- Writing a run-store tree with `ownership` but no `orchestrator` key, or omitting `frame_version`.
- Treating one LLM's self-report as truth without independent evidence.
- Treating one independent review path as enough evidence for judgement-heavy memory promotion.
- Reusing a completed run's learning without terminal proof, a retained trace manifest, or a
  continuation packet.
- Letting an artifact outlive its dead hypothesis: keeping a decommissioned artifact as authoritative
  spine noise after its source DKR went off-track, instead of dropping it and salvaging parts
  explicitly (`dead_hypothesis_artifact_count == 0`).
- Letting the orchestrator self-certify a hypothesis verdict ("we're fine") instead of getting an
  independent challenger verdict - single-LLM-truth in hypothesis form
  (`self_certified_hypothesis_count == 0`).
- Handling a post-done request on a standing-wall artifact with no frame at all (frameless successor
  work): re-read the standing set from the terminal record and run admissibility before acting. See
  `references/matched-abstraction.md` phase 5.
- Treating a human instruction as proof that an approach will work. Record it as input, compare it
  with fresh metrics, and use a DKR when it conflicts with evidence or leaves a material unknown.
