---
name: feature-development-loop
description: Develop and ship one change at a time through an E2E-first loop — write a durable design doc to the repo's docs/ and rubber-duck it, author deterministic CI guards that encode and enforce the design (drift-proofing future agents), build, then prove it works with a real end-to-end run before review. "Real" scales to the project — a token-burning live model/backend call for agent work, or exercising the running app/UI with screenshot inspection for app and web work. Once it works, run dual-review — handed the full design-and-guard review packet each round, alongside project context (AGENTS.md, README, roadmap) — as its own review-and-fix loop until both reviewers are clean, then one final E2E; only an E2E failure restarts the loop. Use when making essentially any non-trivial code change you intend to ship — the default development loop for app, web, service, agent, pipeline, and SDK work, not just high-risk runtime changes; only docs-only edits and trivial one-liners take the lighter path.
---

# Feature development loop

A disciplined loop for developing and shipping one change at a time. **First,
write a design document**
to the repo's `docs/` — the plan, the **reuse contract** (reuse before extend,
extend before create), and an end-to-end **data-flow diagram** — and rubber-duck
it until it holds. **From that doc, author the deterministic CI guards** *before*
the feature, so the design is drift-proofed from the first commit, and
**dual-review those guards to clean** as the code they are — they are the
contract every later step is measured against. **Then build**
until the guards and the unit suite go green, and **prove the change works with a
real end-to-end run before you spend review effort on the feature code.** Only
once it works do
you run **dual-review** as its own review-and-fix loop until both reviewers are
clean, then a single **final** E2E. A final-E2E failure is the only thing that
sends you back — fix the root cause, restart the dual-review-till-clean loop, and
re-run the final E2E — until both reviewers are clean and that E2E is green on
the same tree. **Then land.**

The order is the point. The design and its guards come first because a
machine-checked design is the cheapest place to catch a flaw and the only thing
that stops a future agent silently drifting: completion guards stay red until
each piece is built as specified, drift guards forbid regressions, and ratchet
guards burn a migration to zero — all wired into CI, so drift earns a red build
rather than a silent regression. The live E2E comes *before* review because
static review and unit tests repeatedly miss bugs only a real run exposes (broken
renders, path resolution, wiring, wake chains), and because reviewing code that
doesn't yet work wastes the review. The guards are the one thing reviewed
*before* the build: a guard has no downstream live run of its own, so judging it
never needs the feature to exist — everything a reviewer needs (the guard code,
the design, and the red-first proof that it fails for the right reason) is
already in hand. So you dual-review the guards to a clean, trusted contract
first and build against it.
This skill orchestrates the loop; it calls the `dual-review`, `rubber-duck`, and
`architecture-fitness-functions` skills rather than replacing them, and it wires
guards into your existing CI rather than being a CI config itself.

## When to use

This is the **default loop for essentially all development work** — reach for it
on any non-trivial code change you intend to ship, not only high-risk ones:

- Any feature, fix, or refactor that ships as code — app, web, service, agent,
  pipeline, SDK, or tooling.
- Especially anything whose correctness depends on runtime behavior a static
  review can't confirm — a rendered UI, an event-driven pipeline, a CI/CD
  workflow, an agent loop, a webhook/wake chain — where "the diff looks right"
  is not sufficient evidence.
- When the user asks to ship only after it is proven working live *and* both
  reviewers are clean, or puts you on autopilot for a backlog with that bar.
- When landing several changes and you want each one independently verified.
- For audit- or backlog-driven work, take one item at a time: read the
  audit/issue, ground it in the actual files, write the design doc (step 0),
  then run the loop — and fold what you learn back into the design doc before
  starting the next item.

Reserve the lighter path (straight to review, or just merge) only for: docs-only
changes, truly trivial one-liners, or changes already fully covered by a fast
deterministic test you can run inline.

## Prerequisites

- A real target to E2E against: a canary/staging environment distinct from
  production, a live model/backend (LLM/agent work, where the run burns real
  tokens), or a running instance of the app/server/UI (app and web work).
  Credentials scoped to whatever the E2E exercises.
- For UI work: a way to capture and inspect screenshots of the rendered
  interface. On macOS, the `macos-background-app-control` skill captures a
  window even while it sits occluded behind the user's foreground app, without
  stealing focus.
- The `task` tool with `code-review` agents and the model pair the
  `dual-review` skill uses, plus the `rubber-duck` agent.
- A repeatable E2E entry point (a scenario script or harness) that asserts on
  *observable end state*, not just exit code.
- macOS note: the runner host is often bash 3.2 with BSD tooling — see Pitfalls
  for the bash-3.2 traps this skill specifically guards against.

## Quick start

For one change, in order:

0. **Design → durable design doc, then rubber-duck it.** Before writing code,
   write a design document to the target repo's `docs/` capturing the
   plan/approach, the **reuse contract** (reuse before extend, extend before
   create), an **end-to-end data-flow diagram** naming each function and file,
   tagging every node `NEW` / `EXTEND` / `REUSE`, and showing existing-surface
   connection points when extending existing code, the design's invariants +
   acceptance criteria, the definitions of
   the deterministic checks that will enforce them, and a plain **Definition of
   Done** as the closing section. Run a `rubber-duck` pass and fold its findings
   **into** the relevant sections until the design holds — the committed doc is
   a clean spec, not a review log.
1. **Guards first — author the deterministic CI guards (red-first where meaningful).**
   From the design doc's check definitions, write deterministic checks that
   encode the design and wire them into CI: **drift guards** enforce the design's
   overarching rules (the reuse contract and cross-cutting invariants) and
   usually start green; **completion guards** lock in the specific architecture
   and start **red for the right reason** (the design is absent, not a syntax
   error). Prove every green drift guard can fail on a known-bad case. See the
   `architecture-fitness-functions` skill for how. The guards stay in CI so a
   future agent who drifts gets a red build. Then **dual-review the guards to
   clean** as their own review-and-fix loop — they're code — before you build
   against them. (The Guard gate in Workflow below lists what the reviewers
   confirm.)
2. **Build** on a topic branch off fresh `main` until the guards *and* the full
   unit suite go green. Keep the diff scoped to one change; confirm
   `git diff --stat` shows only the files you intend.
3. **Live E2E first** — run the real end-to-end scenario against the real system
   (a live model/backend that burns tokens for LLM work, or the running app/UI
   for app and web work; **screenshot and visually inspect any UI**). **Fix
   issues and re-run until it passes.** Do not start review until it works.
4. **Dual-review-till-clean (its own review-and-fix loop).** Run the
   `dual-review` skill — **hand the reviewers the durable design doc plus its
   check definitions, the guard files, CI wiring, and the latest test/E2E
   results every round** (with AGENTS.md, README, roadmap) so they hold the
   change accountable to the design. The guards were already dual-reviewed to
   clean in step 1; here reviewers check the feature code against them and
   re-review any guard a fix has changed. Review → fix → re-review → fix, iterating until **both** reviewers
   return zero in-scope findings on the same tree. All review fixes land inside
   this loop; do not run the final E2E between fixes.
5. **Final live E2E** — only after the review loop has fully converged, run the
   real E2E on the clean tree and confirm the observable end state.
6. **Only an E2E failure restarts the loop.** If the final E2E surfaces issues,
   fix the root cause and **restart step 4** (the full dual-review-till-clean
   loop), then re-run step 5. Repeat until the final E2E passes on a tree the
   reviewers have already certified clean.
7. **Land.** Squash-merge the PR (and clear the Copilot PR reviewer gate) or
   push directly, per the change's workflow.
8. **Hygiene.** Sweep and close any test artifacts your runs leaked.

## Workflow

### 0. Design gate — durable design doc, then rubber-duck it (before you build)
Before implementing, write a **durable design document** to the target repo's
`docs/` (e.g. `docs/design/<change>.md`) and commit it, so future agents inherit
the intent rather than re-deriving it. The doc captures:

- **Plan / approach** — what you're building and the key decisions.
- **Reuse contract** — the design's standing rules for *how* the code is built,
  so the change extends the codebase rather than growing a parallel one. Every
  design carries these, and step 1 enforces them as drift guards:
  - **Reuse before extend, extend before create.** Prefer an existing module,
    function, type, or extension point as-is; if it *almost* fits, extend that
    surface with the smallest general addition (a parameter, a field, a method,
    a case); write a new file or function only when no existing surface can
    carry the behavior — and justify it in the doc.
  - **One source of truth, no redundancy.** Anything two call sites would
    compute (a status value, a path, a delay, a mapping) lives in one shared,
    generalized helper both call — written so the next caller reuses it too.
  - **Universal patterns over one-offs.** Compose the codebase's established
    shared patterns (its routing, its presentation layer, its data-access
    boundary, its error handling) rather than a bespoke variant. The data layer
    is the strictest: new data-access entry points, state containers, or
    transfer-object shapes are the last resort, and any new type mirrors or
    derives from one canonical source rather than becoming a parallel one. Where
    the codebase supports it, new units self-register via discovery rather than
    an edit to a shared index, so adding one never touches a shared file — one
    fewer drift and merge-conflict hotspot.
- **Cost of the common change** — name what adding the thing this architecture
  is built to make cheap actually costs: the file(s) you author, and the
  surfaces you must **not** touch (framework, backend, shared index). This turns
  the reuse contract into a reviewable target and a "what may I touch?" decision
  aid, and step 1's guards enforce the forbidden-touch list.
- **End-to-end data-flow diagram** — a `mermaid` diagram tracing the full path
  of data through the architecture, source to user, naming **each function and
  its containing file** at every hop. Tag every node `NEW` / `EXTEND` / `REUSE`;
  when building on existing code, show exactly where the new code connects to
  the existing surfaces, so the whole flow and the reuse boundary read at a
  glance.
- **Invariants + acceptance criteria** — the design's hard rules and what
  "done" observably means.
- **Check definitions** — for each invariant/criterion, the concrete
  deterministic guard that will enforce it (what it asserts, where it lives, how
  CI runs it). Step 1 is authored straight from this list. Also name what the
  guards deliberately do **not** cover — the semantic-correctness claims left to
  functional tests and review — so the design records the boundary of what CI
  proves.
- **Definition of Done (closing section)** — a short, plain-language statement,
  placed at the **end** of the doc, of the finished result: the observable
  behaviors that must be true and the regressions that must not appear, in terms
  a non-author recognizes. It distills the acceptance criteria into an end state
  a looping agent re-reads to judge *am I actually done, or is there more?* — so
  it points at the acceptance criteria and guards rather than restating each
  one, and stays short enough to hold the whole target in view at once.

Keep enforcement truth in **one** canonical place: a named invariant register
(`docs/architecture/INVARIANTS.md`) owns the `INV-NNN` rows and their links to
the enforcing tests, and the design doc *references* those IDs instead of
duplicating them, so the two can't drift apart. The
`architecture-fitness-functions` skill maintains this register; if that skill
isn't in play, still keep the register as the single source of enforcement
truth.

Then run a `rubber-duck` pass over the design. Treat its findings the way you
treat code-review findings: fold each one (or justify dropping it) **back into
the doc** until the design holds. Folding means editing the relevant sections in
place so the committed doc reads as a clean specification — as if the resolved
design had been written that way from the start. Do not append a "rubber-duck
round N — findings" log, leave `Resolution:`-style annotations beside the text
they already fixed, or keep inside-baseball asides (who reviewed it, what a
round returned, dated investigation notes, "open item for so-and-so"): the next
agent inherits this doc as the design, not its edit history — git already keeps
that. A flawed design caught here is an order of
magnitude cheaper than one caught at the live gate. This gate is cheap — do it
even for changes you feel sure about.

### 1. Guard gate — write the deterministic CI guards first (red-first where meaningful)
Before implementing the feature, author the deterministic checks from the design
doc's check definitions and wire them into CI on every PR. They are the
machine-checked contract that keeps this change — and every future agent's edits
— aligned with the design. See the `architecture-fitness-functions` skill for
how to author them (structural build-time + behavioral runtime walls,
deterministic-not-LLM, the named invariant register). If that skill isn't
present, the minimal fallback contract still holds: deterministic checks only
(**never an LLM judge**), both structural and behavioral, each linked to a row
in the invariant register (`docs/architecture/INVARIANTS.md`), permanently
CI-wired.

Author every guard to make a violation **impossible to express** rather than
merely detectable after the fact. In order of strength: a **type- or
schema-level** constraint the bad code can't get past (it won't compile or
validate); a **dependency-graph** check that resolves the *real* import graph —
following re-exports, aliases, generated edges, and runtime-loaded edges — so a
forbidden edge can't be written; and, only as a last resort, a **text-match**
heuristic, which renaming, aliasing, or a layer of indirection can evade, so
reserve it for the interim ratchets below, never a permanent wall.

The guards do two standing jobs, plus a third for migrations — handle each
honestly:

- **Drift guards enforce the design's overarching rules** — the reuse contract
  and any cross-cutting invariant (a banned import edge, forbidden vocabulary in
  a layer, "one canonical parser", a pinned capability table). They forbid a
  regression and are usually **green from day one** on an empty feature, which
  proves nothing on its own — so prove each one can fail by running it against a
  known-bad case (a negative fixture or a temporary local violation), watching
  it go red, then revert.
- **Completion guards lock in the specific architecture** — each positively
  asserts a designed artifact from the doc (and its data-flow diagram) exists
  and behaves per contract. These start **red for the right reason** — failing
  because the design is absent, *not* because of a syntax/import/harness error —
  and burn down to green only as each piece is built as designed. A red
  completion guard is the definition of "not built yet."
- **Ratchet guards drive a migration of existing code to zero** — when the
  change converts many existing sites to the new design, a completion guard
  can't start red for the right reason, because the legacy code already
  compiles. Instead seed a checked-in baseline of every un-migrated site
  (**per-symbol**, not per-file, when they share a file) and fail if the
  baseline **grows** — it may only shrink. Each landing deletes its own entries,
  so the build itself is the migration to-do list. A ratchet is temporary by
  design: once its baseline reaches empty and a structural guard covers the
  surface *by construction*, delete it — its job is now subsumed by that
  deterministic check.

The rule: **red-first where meaningful; otherwise prove the guard is live.**
Before building, self-validate the guard set: each guard links to an `INV-NNN`
row, states its failure mode, and has shown it fails for the right reason. An
invariant you've stated but can't enforce yet is tagged `REGISTER-ONLY` /
backlog and does **not** count as a done-criterion for this change unless the
user explicitly accepts it.

Then **dual-review the guards to clean before you build.** The guards are code,
and they are the contract every later step is measured against, so lock a
trusted contract first. This does not violate the review-after-it-works rule
(step 3): feature code waits because a live run exposes bugs static review
misses, but a guard has no such downstream run — everything needed to judge it
(the guard code, the design doc, and the red-first proof that it fails for the
right reason) is already in hand, so deferring its review would gain nothing.
Run `dual-review` as its own
review-and-fix loop — hand the reviewers the design doc, its check definitions,
the guard files, and the CI wiring — iterating review → fix → re-review until
**both** reviewers return zero in-scope findings on the same guard set. Direct
them to confirm four things:

- the guard *set* covers every invariant this change is meant to enforce
  (`REGISTER-ONLY` backlog rows excepted);
- each guard is aimed at the right invariant (no gaps, nothing pinning the wrong
  thing);
- each guard is well-built and genuinely enforceable (not weak or miswired, and
  it fails for the right reason);
- the design doc ↔ invariant register ↔ guard implementation stay consistent.

Only build once the guards are clean.

### 2. Scope and build
Branch off current `main` and implement until the completion guards **and** the
full unit suite go green. Green guards are the *architecture/design* definition
of done — they check the shape and contract, not that the feature works; the
unit/integration suite and the live E2E below still prove functional
correctness. Verify the change is additive/surgical and contains no unrelated
edits (especially in a shared worktree where another agent may have uncommitted
files). `git diff --stat <base>...<branch>` is the gate: only the intended files
(plus the design doc and guard files from steps 0–1).

### 3. Live gate FIRST — prove it works before you review
Run the actual end-to-end scenario against the real system, not a dry run or a
mocked predicate. What "real" means depends on the project: for LLM/agent work
it is a live run that burns real tokens against the real model/backend; for app,
web, or service work it is exercising the running app, server, or UI for real.
Either way, watch it to completion and confirm the **observable** end state
directly (via API, the runtime's own artifacts, or the rendered UI), not just
the harness's self-report.

**If the change has a user interface, visual inspection is part of the E2E.**
Capture screenshots of the actual rendered UI and inspect them — correct layout,
state, and content — rather than trusting a 200 response or a passing selector.
On macOS you can screenshot a window even while it sits behind the user's
foreground app (no focus stealing) using the `macos-background-app-control`
skill. For a web UI, that inspection can be a headless browser driving the
actual running page, not a unit-level selector assertion. A passing API call
with a broken render is a failing E2E.

If the live run fails or aborts, treat it as a finding, fix the root cause, and
re-run **this step** until it passes. You are not yet in review — make it work
first. Reviewing code that doesn't run wastes the review pass.

Before leaving this gate, confirm the change carries **full functional test
coverage** — every new behavior and edge case has a test (distinct from the
step-1 design guards, which check the contract rather than the behavior) and the
whole suite is green. A green suite plus a passing live E2E is the entry
condition for review.

### 4. Static gate — dual-review-till-clean (its own review-and-fix loop)
Invoke the `dual-review` skill and run it as a self-contained loop: review →
fix every kept finding → re-review → fix, iterating until **both** reviewers
return zero in-scope findings on the same tree. Every review-driven fix lands
*inside* this loop — you do not run the final E2E between individual fixes, and
a single-reviewer pass is not "clean." Untested behavior surfaced here is an
open finding, not a detail to backfill later. This gate exits only when both
reviewers are simultaneously happy.

**Hold the change accountable to the design — hand reviewers the design, not
just the diff.** Every round, pass the reviewers the **durable design doc plus
its check definitions** (from step 0), the **guard/test files and CI wiring**
(from step 1), the latest test/E2E results, and the project context that says
what it's trying to achieve — `AGENTS.md`, the `README`, the roadmap, relevant
issues. Reviewers grounded in the design critique against what the change is
*supposed* to do; reviewers handed a bare diff invent their own intent and
produce off-target findings. The guards were already dual-reviewed to clean in
step 1, so here the reviewers focus on the feature code — with one carry-over:
if a fix in this loop changed a guard, that guard change is re-reviewed like any
code change. Direct them to check three alignments: the implementation matches
the design doc; the implementation genuinely *satisfies* the guards (green
because it is built as designed, not because a guard was weakened to pass); and
the design doc ↔ invariant register ↔ guard implementation stay consistent.

**Keep the design doc from rotting.** If a review fix changes behavior, a guard,
or an acceptance criterion, update the design doc **and** the invariant register
in the *same* fix round — never leave the committed design describing something
the code no longer does. A stale design doc hands the next agent a lie.

### 5. Final live gate — E2E only after the review loop converges
Only once the review loop has fully converged (step 4 exited clean), run the
same real end-to-end scenario as step 3 — including the screenshot/visual
inspection for any UI — on that clean tree and confirm the observable end state
out-of-band. Review changes can regress runtime behavior the unit suite doesn't
catch; this final live run is what proves clean-and-working coincide.

### 6. Only an E2E failure restarts the loop
If the final E2E passes, you are at the ship condition — proceed to land. If it
surfaces issues, you do **not** ship yet:
- Fix the root cause.
- **Restart step 4** in full — the fix re-enters the dual-review-till-clean
  loop (a behavior change must be re-reviewed by both reviewers).
- Re-run the final live E2E (step 5).

Repeat this outer loop (fix → dual-review-till-clean → final E2E) until the
final E2E passes on a tree the reviewers have already certified clean. That
coincidence — both reviewers clean AND a green final E2E on the same tree — is
the ship condition. Nothing inside the review loop triggers an E2E run; only a
failed final E2E sends you back into the review loop.

### 7. Land the change
With a clean review and a green final E2E on the current tree, land it:

- **Via PR:** open the PR, clear the **Copilot PR reviewer** gate (below),
  squash-merge with a `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
  trailer, delete the branch, fast-forward the worktree, confirm the merged
  file is present.
- **Via direct push** (e.g. a protected `main` you push to directly): push,
  then confirm the remote head advanced and re-run the full suite on the pushed
  tree.

#### PR-time gate — Copilot PR reviewer (PR path only)
Once the PR is open, check the built-in GitHub Copilot PR reviewer's notes
explicitly — do not assume "CI green" implies the bot review is also clean. It
is a third independent signal that catches things the pre-merge dual-review and
the live E2E both missed (regex anchoring bugs, brittle assertions, doc/PR-body
mismatches, scope creep).

```
gh pr view <num> --repo <owner/repo> --json reviews,comments \
  -q '.reviews[] | {author: .author.login, state, body}'
gh api /repos/<owner>/<repo>/pulls/<num>/comments \
  -q '.[] | {path, line, body}'
```

Treat the result as:

- **APPROVED with no inline comments** → gate passes; proceed to merge.
- **APPROVED with minor notes** → read each note; fold non-substantive notes
  into the PR description or a follow-up issue, do not silently ignore them.
- **COMMENTED / CHANGES_REQUESTED with substantive findings** → treat as a new
  round. Verify each claim (regex/quote/line-range), fix or justify, push the
  fix, then return to step 4 (re-review) and re-check Copilot. Do not merge over
  an unaddressed substantive Copilot finding even if the bot's review "does not
  count toward required approvals."

Verify each Copilot finding the same way the `dual-review` merger does for
subagent findings: grep the cited quote in the cited line range. The Copilot PR
reviewer also hallucinates occasionally — a structurally-incorrect claim that
doesn't trip today may still be a real fragility worth fixing.

### 8. Hygiene
Sweep for and close any test artifacts your runs leaked (issues, PRs, branches),
including ones created by asynchronous workers *after* a scenario aborted. Leave
artifacts you did not create alone.

## Pitfalls

These failure classes recur across project types; check for them explicitly.

- **Reviewing before it works.** Spending a dual-review pass on *feature code*
  that hasn't passed a live E2E wastes the review and often re-runs it from
  scratch after the inevitable behavioral fix. Prove it works first (step 3),
  then review. (The guards are the deliberate exception — dual-reviewed to clean
  in step 1, before the build; see step 1 for why.)
- **Guards that can't fail.** A drift guard that's green before the code exists
  proves nothing until you've watched it go red on a known-bad case; a
  completion guard that's red because of a syntax/import/harness error, not the
  absent design, is a false gate. Prove each guard fails for the *right reason*
  before you trust it going green.
- **Design-doc drift.** The committed design doc and the invariant register are
  the contract. If a fix changes behavior, a guard, or an acceptance criterion
  but not the doc/register, the next agent inherits a stale spec that no longer
  matches the code. Update the doc and register in the same round as the code.
- **Design doc as a review log.** The committed doc is a clean specification, not
  a transcript of how it got there. Fold review findings into the sections they
  correct (step 0 lists the residue forms to keep out) — they belong in the
  review thread and git history, not the doc the next agent reads as the design.
- **Guards mistaken for test coverage.** Green architecture guards check the
  design's shape and contract, not that the feature works. They don't replace
  the unit/integration/E2E gates — keep all of them.
- **Running the final E2E mid-review-loop.** The final E2E runs only after the
  dual-review-till-clean loop has fully converged — not between individual
  review fixes. Burning a real E2E run (real tokens for LLM work, or a full
  app/UI exercise otherwise) on a tree the reviewers haven't certified clean
  wastes effort and muddies which gate is actually failing. Let the review loop
  finish, then run the one final E2E.
- **Trusting the harness's self-report.** A test runner or scenario can print
  "passed" while having aborted, skipped, or asserted nothing. Verify the real
  end state out-of-band — the actual API/database state, a file on disk, the
  rendered UI — not the runner's exit message. Make harnesses **fail closed**:
  any abort must surface as a failure, never a silent `0`.
- **Serving a stale build.** A passing screenshot or request can be hitting a
  cached bundle or an old server process, not your change. Confirm the running
  app/server was actually rebuilt and restarted with the current tree before you
  trust the E2E.
- **UI-only or API-only blind spots.** For UI work, a green API/unit result over
  a broken render is a failing E2E — and a clean screenshot over a broken
  backend is equally a fail. Check both the observable UI and the underlying
  state.
- **Consumable / mutated fixtures.** If the E2E changes state (edits a fixture,
  creates records, mutates persisted UI data), reset it idempotently before the
  next run, guarding on the expected pre-state. Don't blind-overwrite.
- **Leaked test artifacts, including async ones.** Runs create artifacts
  (records, PRs, branches, files, uploads) — and async workers can create more
  *after* a scenario already finished. Track identifiers as they're created and
  sweep afterward; leave artifacts you did not create alone.
- **Host/platform scripting traps.** Scripts that drive the E2E inherit the
  quirks of the shell/runtime they run in (error-handling edge cases, path
  resolution when files move, locale/encoding). For shell- or API-driven
  harnesses (CI, agent loops), see `references/live-harness-traps.md` for the
  detailed bash/`set -e`/`set -u`/cleanup-trap failure classes.

## Verification

The change is done only when ALL hold:

1. A durable design doc was written to the repo's `docs/` (plan, reuse
   contract, cost of the common change with its forbidden-touch list, end-to-end
   data-flow diagram naming each function and its file with every node tagged
   `NEW` / `EXTEND` / `REUSE` and existing-surface connection points shown when
   extending existing code, invariants, acceptance criteria, check definitions,
   and a plain-language Definition of Done as its closing section),
   rubber-ducked with its findings folded into the relevant sections (the
   committed doc is a clean spec, not a review log), and committed — consistent
   with the invariant register.
2. Deterministic CI guards encoding the design were authored *before*
   implementation, each linked to an invariant-register row and proven to fail
   for the right reason (completion guards red on the absent design; drift
   guards shown to go red on a known-bad case), were **dual-reviewed to clean
   before the build** (both reviewers agreeing the set covers every invariant
   this change is meant to enforce — `REGISTER-ONLY` backlog rows excepted — is
   correctly aimed, and is genuinely enforceable), are now green, and stay wired
   into CI. For a migration, any ratchet guard's baseline shrank by exactly the
   sites this change migrated and never grew.
3. The change carries full functional test coverage (all new behavior + edge
   cases tested, suite green) — separate from the design guards.
4. A live E2E passed *before* review and its end state was confirmed
   out-of-band — including a screenshot/visual inspection of any UI.
5. `dual-review` reports both reviewers clean on the final tree state, the
   reviewers having been given the durable design doc, its check definitions,
   the guard files, CI wiring, and the latest test/E2E results (plus AGENTS.md /
   README / roadmap) every round, with the implementation confirmed to match the
   design doc and satisfy the (step-1-reviewed) guards, any guard a fix changed
   re-reviewed, and the design doc / register / guards / code kept consistent.
6. A **final** live E2E passed on that same reviewed tree, confirmed
   out-of-band — i.e. clean review and green final E2E coincide on one tree.
7. The change is landed (PR squash-merged and branch deleted with the worktree
   on the new `main`, or pushed directly with the remote head advanced and the
   suite green on the pushed tree). For the PR path, the Copilot PR reviewer is
   APPROVED with no unaddressed substantive findings (verbatim-quote-verified).
8. The live target has no leaked artifacts attributable to your runs.

If any fail, the change is not landed — fix and re-gate.
