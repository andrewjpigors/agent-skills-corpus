---
name: academic-army-coding-style
description: >-
  Maintain clean, local, low-coupling code trajectories in existing research
  repositories. Use when Codex writes or edits code, refactors modules,
  implements features, harnesses, tests, methods, baselines, metrics, result
  exports, or framework docs. This skill does not initialize template
  repositories or generate full project scaffolds from empty directories.
---

# Academic Army Coding Style

## Mission

Use this skill as a code-quality and framework-consistency layer for an
existing repository. The upstream task decides what to build; this skill decides
how to keep the implementation readable, local, low-coupling, testable, and
consistent with the current framework.

Do not use this skill to initialize a repository template or recreate a project
scaffold from an empty directory. Repository initialization is out of scope.
This skill may add files, modules, tests, harness support, or docs only when
the current task and current repository need them.

## Operating Boundary

Respect the existing source layout, naming style, language ecosystem, tests,
harnesses, docs, and project configuration. Improve local structure when it
makes the current change clearer or safer, but do not redesign the whole
repository because a plan describes future systems.

Ignore unrelated drafts, logs, historical outputs, old runs, and nearby files
unless the user makes them part of the task.

Keep these experiment directories when they already exist:

- `data/`: input data, pointers, traces, manifests, fixtures, or samples.
- `output/`: program-run outputs and intermediate artifacts.
- `results/`: experiment results and curated artifacts.
- `harness/`: harness code, contracts, configs, schemas, samples, and support.

Do not force a fixed test directory. Tests follow the repository's existing
layout, project configuration, initialization docs, or adjacent test style.

### Git Workflow Discipline

**No-git environments.** When the task's Boundaries or environment constraints
state that git is unavailable (air-gapped lab machine, container without git,
no-version-control sandbox), skip all git-dependent operations: no branching,
no committing, no diff verification.  Fall back to filesystem-level discipline:
maintain a manual change log in the task's working notes, keep a copy of the
pre-edit file state for rollback, and verify correctness through import smoke
and test runs rather than git diff.  A task that says "no-git" is a hard
constraint — do not attempt git operations and report them as skipped.

**Branch before committing.** Never commit refactoring or feature work to the
default branch. Create a named branch from the current HEAD before the first
commit of a change series. Commits on the default branch conflate review,
bisect, and rollback surfaces.

**Commit between completed slices.** When a multi-slice refactoring plan is
executed slice-by-slice, commit each completed, test-green slice before starting
the next. Starting a new slice on top of uncommitted work from the prior slice
conflates two independent changes in one diff, making review and bisect
impossible. An uncommitted green suite is not the same as a committed slice.

For extraction slices, a slice is "completed" when the extraction's staged
verification gates (Gates A–G in "Code extraction" below) pass — at minimum:
module smoke, test baseline matches, consumer audit confirms migration status,
and `git diff --check` is clean.

**Stage selectively.** Verify with `git status` that only the intended change
set is staged. If unrelated files, scratch artifacts, debug outputs, or
next-slice work is present in the working tree, stage selectively rather than
using `git add -A`. A commit that sweeps in P(n+1) files alongside P(n) work
cannot be reviewed or reverted at slice granularity.

**Commit message quality.** The body enumerates what changed and why — layers
cleaned, modules extracted, boundaries narrowed, config weight reduced, suite
status. Close with the `Co-Authored-By` trailer unless the project convention
specifies otherwise.

**Do not push unless the user asks.** A task that says "commit, do not push" is
a scope fence. Pushing expands the blast radius of un-reviewed work. If the git
remote helper (e.g., `gh`) is unavailable, fall back to local-only commit tools;
do not interpret a missing push tool as license to skip the commit.

**Working tree clean after commit.** After the commit lands, `git status` should
report no staged and no tracked-modified files for the committed change set.
Untracked files that are explicitly out of scope (e.g., next-phase planning
docs, future harness scripts) may remain, but they must be the same set the task
named as exclusions.

### Task Boundary Respect

**Stop at the task's completion boundary.** When a task says "commit only, then
stop" or "verify, do not edit," the task is complete when that bounded action is
done. Do not self-expand into the next phase, start the next slice, or begin
"while we're here" edits. Self-expansion conflates task scope and produces diffs
that cannot be reviewed against the task's acceptance contract.

A task that ends with "ready for P1 Phase 1a" is complete — it is not an
invitation to start P1 Phase 1a in the same session.

**Verify completion against the task's scope fence.** Before reporting
completion, confirm: (a) every deliverable category from the task Boundaries was
satisfied, (b) no deliverable from a future phase was started, and (c) the
working tree state matches the task's stated end state (committed, clean, or
with specific known exclusions).

### Before You Touch Anything

Before any edit or execution, verify the task's premises against reality.
Stale task memories and outdated plans are the most expensive mistake in
research codebases — they cause re-implementation of already-completed work
and silent acceptance of stale evidence.

**Three mandatory checks:**

1. **Git state vs. task claims**: `git status`, `git log --oneline -5`, `git diff --stat`. If the task says something is uncommitted or pending but the tree is clean and the commits are already there, the task premise is stale.

   **Resolve the target repo path from the task preamble.** The task preamble
   (or Context) states the target repository path — e.g., `Target repository at
   /home/<user>/<workspace>/codebase/`.  Use that exact path for every git
   command in this step.  Do not assume the repo lives at the workspace root, at
   `$PWD`, or at a sibling directory.  A git command run against the wrong
   directory silently reports state for the wrong repo — the most insidious form
   of a stale-premise error.
2. **File/module existence vs. task claims**: If the task says "create module X" or "split file Y," verify the code doesn't already exist at the claimed path or a semantically equivalent location. Search for the class/module name, check registries, factory mappings, harness enumerations, and figure-generator style maps.
3. **Document consultation**: If the task's Boundaries or Context list documents to read (blueprints, plans, specs, reference docs, status files), read ALL of them before proceeding. The task's document list is a scope fence, not a suggestion.

   **Path resolution from Context.** When the task references files by relative paths
   (e.g., `current_status.md`, `memory/...`, `experiment_plan.md`), resolve
   their concrete location using the Context's own document-path conventions.  If the
   Context places planning documents at an absolute workspace-level path
   (e.g., `~/<workspace>/`), then status, memory, and tracking files the task
   references likely live there too — not at the repository root.  Verify the file
   exists on disk at the resolved path before editing.  Do not assume every
   externally-referenced file lives under the repo root when the Context already
   shows documents at a different directory level.
4. **Version and dependency compatibility**: If the task involves running or
   importing dependency code (installed packages, vendored libraries, external
   tool executables), verify the current environment's versions against the
   dependency's known compatibility window.  The two most expensive
   version-compatibility failures in research codebases are: (a) a newer
   framework version (PyTorch, NumPy, CUDA toolkit) silently rejects operations
   that worked in the version the upstream code was written for — in-place
   tensor aliasing, dtype coercion, or deprecated API signatures; and (b) a
   task claims an environment constraint (e.g., "CPU-only," "no GPU available")
   that is factually false because the environment has the hardware or the
   software stack.  Verify both directions: is the constraint real, and does
   the dependency code actually run under the actual environment?  Report
   version-compatibility gaps as blocking findings, not as footnotes — a
   silent `RuntimeError` on a key operation is a blocker, not an observation.

5. **Execution-vs-implementation classification against task verbs**: Scan the
   task's Objective and Boundaries for the primary action verb.  If the verb is
   "run," "execute," "sweep," "benchmark," "evaluate," or "regenerate" AND the
   task names a specific existing component to exercise ("via `<decode_core>`,"
   "through `<harness_runner>`," "using `<codec>`"), the task is execution — the
   deliverable is fresh output from that component, not new analysis code.  Do
   not confuse an experiment name ("C2," "ablation," "stress regime") with a
   feature to build.  If the verb is execution and pre-existing cached data
   exists on disk, building a summarizer or figure generator that reads those
   cached files is NOT completing the task — the task requires fresh execution
   through the named component, and cached data from prior runs is not a
   substitute.  Classify the task as execution before any code is written.

**Six build-or-skip states** after verification:

- **Fully absent**: no module, no class, no registration — build it.
- **Partially complete**: exists on disk and in registries but never wired into the active harness or enumeration. This is a wiring gap, not an implementation gap. Wire; do not re-implement.
- **Fully complete on disk**: wired, tested, evidence generated — verify and update memory/trajectory files.
- **Task premise is stale**: the task describes something as missing that is already done. Verify, run the validation command, report, and stop. Do not redo completed work. A stale task memory is a documentation problem, not an implementation gap — update the memory, don't rebuild the code.
- **Infrastructure-blocked**: code can be written and tests pass, but the task's required evidence re-run or behavioral verification needs hardware (GPU, specific device), data, or tools not available in the current environment. This is a **blocked task**, not a completed one. Report BLOCKED with the exact infrastructure needed and the exact commands to run when it becomes available. Do not report DONE. An infrastructure gap does not turn a required deliverable into an optional one.
- **Upstream-bug-blocked**: the needed capability exists in a dependency but a version-compatibility bug, missing module, or incorrect calling convention prevents it from working correctly end-to-end.  The code is not missing — it is installed and importable — but a runtime barrier (e.g., a PyTorch version rejecting an in-place op, a string-replace bug on path handling, a module that was never ported from the reference repo) blocks the full pipeline.  Document the bug with: exact location (file, line), reproduction command, root cause, and impact on the current task — but do **not** fix it during a read-only reconnaissance task.  Fixing upstream bugs is a separate implementation task with its own scope fence.  The reconnaissance deliverable is the bug report, not the fix.

The most expensive form of partially-complete is **wired but never enumerated**:
the module is implemented, registered, and importable, but no harness or sweep
entry point includes it in its iteration. This produces zero results on disk
while every surface claims the component exists. Verify mechanically: factory
entry? Harness import? Spec-builder iteration? If yes to all three and results
are still zero, the gap is execution (the sweep was never run), not
implementation. Run; do not re-implement.

## Task Classification

Classify the task before editing.

**Dominant-verb check — do this first, before any other classification step.**
Scan the task's Objective and Boundaries for the primary action verb and its
direct object.  Execution-dominant verbs include: "run," "execute," "sweep,"
"benchmark," "evaluate," "regenerate," "re-run."  When the dominant verb is
execution AND the task names a specific component to exercise ("run X via Y,"
"execute Z through W," "sweep using V"), the task is **execution**, not
implementation.  An experiment name (e.g., "C2," "ablation study," "stress
regime") is the *thing to run*, not a feature to build.  Do not confuse "build
the C2 analysis framework" with "run the C2 experiment" — the former builds new
code; the latter exercises existing components and produces fresh data artifacts.

When the dominant verb is execution, classify the task as **Execution or
evidence** below, even if the task's description mentions analysis dimensions or
metric names.  The fact that a run will produce data that a downstream summarizer
consumes does not make the task "build the summarizer" — the task is to run the
experiment that produces the data.

**Cached-data trap.** When pre-existing cached outputs or prior-run batch
artifacts exist on disk, building a post-hoc aggregator, summarizer, or figure
generator that reads those cached files is NOT completing an execution task.
Cached data from prior runs is not the same as fresh data produced by the
current task's required execution path.  If the task says "run experiment via
component Y" and Y was never invoked, the task is incomplete regardless of what
downstream analysis code was written.  A summarizer built over stale cache is
useful code, but it is not the task that was requested — it is a different task
that jumped the gun on the execution prerequisite.

- **Feature or implementation**: add the smallest clear code path that
  satisfies the requested behavior.

  **Hybrid-task check.** Before classifying as pure feature/implementation, scan
  the task Boundaries and Reviewer Focus for evidence or behavioral verification
  criteria — phrases like "verify `X > 0`," "confirm Y is non-degenerate,"
  "re-run harness H then figure generator F," "demonstrably achieved on at
  least one scene."  If any such criteria exist, the task is **hybrid** (code +
  evidence re-run), not pure implementation.  Classify it as hybrid and apply
  the Hybrid Tasks rules below.  A task whose acceptance criteria require
  running code — not just writing it — cannot be completed by code alone.
- **Targeted regression fix**: fix a test failure or behavioral regression that
  is confined to a single file or a small, well-understood surface.  The fix
  should be minimal — identify the root cause, make the smallest change that
  corrects it, and verify the test now asserts the intended condition rather
  than passing vacuously.  Do not refactor adjacent code, restructure
  production modules, or expand scope beyond the regression.

  **Mechanism-first diagnosis.** Before writing fix code, reproduce the failure
  at a single datapoint and inspect diagnostic output (rejection reasons,
  budget values, intermediate state) to confirm the root cause.  A task's
  Boundaries often prescribe this directly (\"before editing, reproduce a
  single scene's X and inspect Y\") — do not skip it and guess the root cause.
  Confirm whether the killer is mechanism A, mechanism B, or both; the fix
  differs by root cause.

  **Aliasing-chain diagnosis.** When the regression involves silent state
  corruption (a tensor changes shape, a model mutates unexpectedly, a cached
  value is stale), the root cause is often a Python object-identity alias:
  two names refer to the same mutable object, and one name's mutation
  corrupts the other.  Trace the full identity chain through every
  assignment and argument pass — use `is` checks, `id()`, or a breakpoint —
  and document the chain end-to-end in the fix's docstring or comment:
  which assignment established the alias, which mutation corrupts it, and at
  which call site the corruption becomes observable.  A fix that suppresses
  the symptom without documenting the aliasing chain is incomplete — the
  next developer who touches either end of the chain will reintroduce the
  bug.

  **Defensive copy as root-cause fix.** When a dependency's in-place
  mutation (e.g., an in-place `<quantize_op>(replace=True)`, a tensor
  `.resize_()`, or a mutating library call) cannot be changed — because
  the non-mutating variant would raise a shape mismatch, because the
  library's API offers no non-mutating path, or because fixing the
  dependency is out of scope — defensive
  copying (`copy.deepcopy`, `.clone()`, `.detach()`) IS the root-cause fix,
  not a workaround.  Document: (a) the full aliasing chain showing why the
  copy is necessary, (b) why each alternative (`.clone()`, `.detach()`,
  non-mutating API, parameter replacement) is infeasible or insufficient,
  and (c) the invariant the copy preserves.  A fix comment that says only
  "workaround for aliasing" is underspecified — state what is aliased to
  what, why the copy is the only isolation, and what would break without it.

  **WORKAROUND blocks must describe what they annotate.** When a file
  contains multiple aliasing issues with distinct root causes (e.g., a
  tensor-storage aliasing fixed by `.clone()` in one function, and an
  identity aliasing fixed by `deepcopy` in another), keep each explanation
  scoped to its own fix.  A module-level WORKAROUND block that describes
  only one aliasing layer should either be co-located with that fix or
  should note which aliasing issue it addresses and which it does not.  Do
  not let a WORKAROUND describing issue A sit near fix B without comment —
  readers will misattribute the explanation to the wrong code.

  **Regression fix deliverables are not limited to code.** When the task's
  Boundaries or Context require re-running evidence suites or harnesses after
  the fix, those re-runs are REQUIRED deliverables — the task is not complete
  until they produce verified results.  A regression fix that lands correct
  code but skips the required evidence re-run has not satisfied the task's
  acceptance contract.  See \"Hybrid Tasks (Code + Evidence Re-run)\" below.
- **Refactor or cleanup**: move, split, merge, rename, or delete code only to
  improve locality, readability, or testability. Pure relocation carries an
  absolute boundary: no new logic, defaults, fields, or helpers — only the move
  plus import-depth adjustments.

  Renames come in two forms.  A **code-internal rename** changes the symbol and
  all call sites; no frozen keys exist.  An **evidence-surface rename** changes a
  class or function whose name propagates into artifact metadata, registry keys,
  or harness string references — some of which may be frozen public contracts.
  Evidence-surface renames use the rename-with-frozen-key protocol: update the
  class, keep the registry key via an import alias, and add a dated WORKAROUND
  docstring explaining the key-name debt.

- **Behavior-change refactor**: restructure modules AND close a specific
  behavioral gap in the same slice.  Example: extract a projection boundary to
  make a metric observable to a downstream consumer where it was previously
  invisible.  This is distinct from pure relocation — new wiring, injection
  logic, or data-flow connections are in scope.  It is distinct from a
  standalone feature — the structural change and the behavioral fix are one
  atomic slice; splitting them into separate tasks would produce an intermediate
  state where the new structure exists but the claimed benefit is absent.

  Behavior-change refactors carry a dual verification obligation: (a) all
  structural verification from pure relocation (import hygiene, test baseline,
  scope fences), and (b) **end-to-end data-flow verification** — trace the
  complete path from the changed input through every intermediate step to the
  observable output, and confirm no data is computed but never consumed.  When
  the task's Boundaries or Reviewer Focus explicitly ask for a test
  demonstrating the behavior change, that test is a required deliverable, not a
  suggestion.

  **Post-behavior-change naming audit.** When a refactor changes what a class,
  function, or module does, the name must be re-verified against the new behavior.
  A class renamed from ``<HeuristicScheduler>`` to ``<OptimalScheduler>`` after
  upgrading from greedy to 0/1 knapsack DP is a required rename — the old name is
  a correctness defect because it claims the opposite of what the code does.
  A name that was accurate before a behavior change and became misleading after
  it must be updated in the same change, not deferred.  For class renames where
  a registry key is a frozen public contract, use the rename-with-frozen-key
  protocol (preserve the key
  via import alias, add a dated WORKAROUND docstring).

  Common failure modes:
  - A module is extracted and rewired, but the new data (e.g., alignment PSNR)
    is computed in one function and never consumed by the downstream metric —
    the structural refactor passes import hygiene but the behavioral gap stays
    closed.
  - A data-injection path exists but is only active in one dispatch branch
    (e.g., a specific algorithm present) and silently no-ops in others (skip,
    error fallback) — the behavior change is partial, and the claim of "fixed"
    is false.
  - The developer reports "already wired before this refactor" when tracing
    shows the data flow stops one step short of the claimed consumer —
    structural proximity is not the same as a complete data flow.
  - The behavior changes fundamentally (heuristic → optimal, greedy → DP,
    approximate → exact) but the class/function name keeps the pre-change
    descriptor (e.g., "Heuristic" in the name after upgrading to genuine MPC).
    A misleading name in a class that appears in registry keys, harness output,
    or evidence manifests is a correctness defect — fix it in the same change.
- **Harness work**: keep harness code under the relevant `harness/` area; make
  objective, inputs, metrics, raw artifacts, and run loop explicit.
- **Test work**: place tests in the existing test system's natural location and
  keep each test focused on one behavior with small fixtures or toy inputs.
- **Method, baseline, metric, or export work**: keep the change near the owning
  extension point and update registration, docs, exports, and tests only when
  those surfaces are in scope.
- **Framework or docs sync**: update framework docs when module boundaries,
  extension points, harness/test organization, or artifact schemas change and
  docs are in scope.
- **Seam introduction** (composition root, factory, adapter interface, registry
  wrapper): introduce a new abstraction boundary and prove it works.  This task
  type carries a dual proof obligation — (a) unit tests that exercise the new
  code and (b) at least one real consumer migration that proves the seam fits
  the existing call sites.  Unit tests prove the code is correct; consumer
  migration proves the interface shape, import surface, and resolution contract
  work in practice.  Never substitute test-only proof for consumer migration
  when the task explicitly requests it.  When the task is silent, prefer
  migrating exactly one consumer — enough to validate the seam without
  expanding scope into a full migration sweep.

  **Seam introduction verification checklist.** After introducing a new seam,
  verify: (1) the spec is pure-data — `dataclasses.asdict(spec)` succeeds and
  produces JSON-serializable output; (2) the composition root is the only
  place that instantiates concrete implementations from the registry or
  factory; (3) at least one existing caller was migrated and its behavior
  matches the pre-seam baseline; (4) the pre-existing import direction
  constraints (e.g., `config` must not import `experiments`) are preserved;
  (5) the test suite green-line count is unchanged or higher, with no new
  failures.
- **Execution or evidence**: run existing sweeps, regenerate evidence suites,
  rebuild batch indexes, produce paper figures, or verify evidence integrity.
  This is not a code-writing task — the components already exist. Validate
  that execution produces complete, non-empty artifacts and that downstream
  evidence surfaces ingest the new data.

  **The task is to invoke the named components, not to build analysis around
  them.** When the task says "run experiment X via component Y" and component Y
  exists, the deliverable is fresh output from Y — not a new summarizer,
  aggregator, or figure generator that reads pre-existing cached data.  Building
  a new analysis module is a separate implementation task; it does not satisfy an
  execution contract.  If downstream analysis code (summarizers, figure
  generators) doesn't exist yet, that is a prerequisite gap to report, not a
  reason to substitute analysis-code authorship for execution.

  **Component-invocation verification.** After execution, mechanically verify
  that the named component was actually invoked: check process logs for the
  component's log messages, verify output timestamps are after execution start,
  confirm the component's expected output artifacts exist and are non-empty.  A
  report that claims "experiment X executed" when component Y was never called is
  a false claim.  If the component couldn't be invoked (environment mismatch,
  missing dependency, broken path), the task is BLOCKED — not DONE.

  **Data-source verification.** When the task specifies a particular data source
  (e.g., "use `<refinement_dir>/` as refinement source," "pull from
  `<specific_dir>/`"), verify that source was actually read: check that file
  opens, reads, or imports from the specified path appear in the execution trace
  or process output.  A run that silently used a different source or fell back to
  a default is a false execution — the data is from the wrong provenance.
- **Reconnaissance or verification**: verify baseline state, confirm blockers,
  audit import graphs, or identify the highest-leverage next step.  This is a
  read-only task — no code changes, no refactors, no sweeps.  The output is a
  verified state report and a single concrete recommendation.  The task's
  required reading list (planning documents, blueprints, specs, status files)
  is a scope fence: read every document the task names, not just the one that
  appears most directly relevant.  A task may name multiple documents because
  each provides partial or cross-referencing context — skipping any of them
  violates the task's boundary contract, even when the skipped documents would
  not have changed the recommendation.

  **Reconnaissance self-verification gate.** Before reporting a quantitative
  claim (count, line number, file list), search again with the broadest plausible
  pattern.  If you claim 27 occurrences of `Mapping[str, Any]`, also search
  `dict[str, Any]` and `Dict[str, Any]` — the actual count may be 5× higher
  because the first pattern missed equivalent forms.  If you claim a file is
  N lines long, also check with `wc -l` — a `grep -c` may have matched something
  different than you intended.  The counter-search must complete before the
  report is submitted.  A quantitative claim that collapses under a broader
  search is a correctness defect in the report, not a minor inaccuracy.

  **Pipeline-gap detection.** When reconnaissance investigates whether a
  capability exists, distinguish four states — conflating them produces the
  wrong next task:
  (a) **exists and works end-to-end** — import succeeds, key operations
  produce correct output, no runtime errors;
  (b) **exists but partially blocked** — the module is installed and
  importable, but a version-compatibility bug, missing sub-module, or
  calling-convention mismatch prevents some operations from completing;
  (c) **does not exist** — no module, no class, no function at the claimed
  path, and no equivalent surface under a different name;
  (d) **exists and works correctly — behavior is an expected structural
  constraint, not a defect** — the code path is intact and logic is correct,
  but the output appears degenerate or indistinguishable because of dataset
  properties, budget tightness, or design invariants (e.g., two ablation
  arms that share the same scheduler implementation by design; the
  distinction is measured through mechanism-attribution metrics, not
  ABR-level QoE).
  State (b), (c), and (d) demand different follow-up tasks.  (b) needs a
  targeted bugfix task scoped to the blocking operation.  (c) needs an
  implementation task to build the missing capability — or a redesign task
  to substitute a different approach.  (d) needs no code change; the
  deliverable is the diagnostic evidence (file:line trace, budget/value
  computation, evidence cross-reference) and a status-doc update recording
  the finding.  A report that lumps (b) and (c) into "doesn't work"
  misroutes the next developer to implementation when the actual need is a
  one-line bugfix, or vice versa.  A report that treats (d) as a bug and
  applies an unnecessary code change introduces spurious complexity.  Verify
  the distinction mechanically: for (b), produce the exact traceback and the
  line that fails; for (c), confirm with `grep`, `find`, and
  `python -c "import <module>"` that no equivalent exists; for (d), compute
  the actual values from on-disk data, trace the flag/config path
  end-to-end, and cross-reference against existing evidence artifacts.

  **Stale-premise contradiction.** When the task's premise directly contradicts
  reality — e.g., the task says "CPU-only env" but `torch.cuda.is_available()`
  returns `True`, or the task says "module X is missing" but `import X` succeeds
  — state the contradiction in the report's opening section before any other
  findings.  A task built on a false premise may have drawn incorrect boundaries,
  overestimated blockers, or recommended unnecessary work.  The contradiction
  itself is a finding — it changes what the next task should be.  Do not bury
  it in a footnote or treat it as a minor correction.

  **Upstream bugs are reconnaissance findings, not fix targets.** When a
  read-only investigation discovers a bug in dependency code (installed
  packages, vendored libraries, reference implementations), document it
  precisely: the file and line, the reproduction command, the root cause, and
  the impact on the current task pipeline.  Do not fix it during reconnaissance.
  The fix is a separate implementation task — it needs its own scope fence,
  its own test verification, and its own review.  A reconnaissance task that
  silently patches an upstream bug produces an un-reviewed code change with
  no test coverage and no audit trail.  The deliverable is the bug report,
  not the patch.

  **Component tracer.** When the task asks whether a suspected defect (low
  variance, indistinguishability, silent no-op) is a code bug or an expected
  structural constraint, use the component-tracer pattern:

  1. **Trace the flag/config path end-to-end**: start from the registry key
     or config flag, follow it through every dispatch point (factory,
     builder, spec constructor, runner argument) to the code branch that
     executes or is gated.  Report each hop with file:line evidence.
  2. **Compute the actual values from on-disk data**: if the claim is about
     runtime values (budget, layer sizes, metric deltas), compute them
     mechanically from the actual compressed output, batch artifacts, or
     evidence files — not from design reasoning or parameter defaults.
  3. **Cross-reference against existing evidence artifacts**: compare the
     computed values against the evidence tables and manifests already on
     disk.  If the evidence already shows nonzero deltas for mechanism-
     attribution metrics, the component is working — the indistinguishability
     is at a different measurement surface.
  4. **State the finding as a four-state pipeline-gap classification**:
     (a) bug → fix, (b) blocked → unblock, (c) missing → implement,
     (d) expected constraint → document.  The classification determines
     whether code changes are needed; (d) is a documentation deliverable,
     not a code change.

  **Reconnaissance report structure.** A reconnaissance report must include,
  in this order:
  1. **Premise check** — which task claims were verified, which were
     contradicted, and the mechanical evidence for each.
  2. **Capability map** — a table or structured list of the capabilities the
     task asked about, each tagged with one of: works / partially-blocked
     (with exact blocker) / does-not-exist / not-applicable /
     expected-constraint (code is correct; behavior follows from dataset,
     budget, or design invariants).
  3. **Component traces** (when applicable) — for each suspected defect that
     was diagnosed, the end-to-end flag/config trace (registry → factory →
     builder → spec → runner) with file:line evidence at each hop, the actual
     values computed from on-disk data, and the cross-reference against
     existing evidence.
  4. **Blocker analysis** — for each blocked or partially-blocked capability,
     the exact barrier (traceback, missing file, version mismatch), the
     evidence that confirms it, and whether the barrier is in project code
     or in an upstream dependency.
  5. **Single concrete recommendation** — the next bounded task, stated as:
     what to build or fix, which module(s) it touches, what the acceptance
     criteria are, and what this unblocks.  The recommendation must follow
     from the capability map — if the map shows no code change is needed
     (state d), the recommendation is a documentation or status-file update,
     not a code fix.  If the map shows a bugfix is needed, the recommendation
     must be a bugfix task, not a redesign.
  6. **Status-doc update** — when the diagnosis refutes, confirms, or
     refines a prior hypothesis recorded in status/memory files
     (e.g., `current_status.md`, `evidence-gap-assessment.md`), update the
     file to record the finding.  A stale status file that still lists a
     refuted hypothesis as an open concern is a documentation defect.  Before
     editing, resolve the file's concrete path using the Context's
     document-path conventions (see "Document consultation" in "Before You
     Touch Anything").  Verify the file exists on disk at the resolved path.
     If the task explicitly asks for status-file updates, this is a required
     deliverable, not a suggestion.

- **Evidence consumer / typed bridge**: build a read-only module that consumes
  raw evidence artifacts (batch JSONs, sweep outputs) and produces typed
  dataclass bridges for downstream consumers (figures, tables, reports,
  analysis scripts).  This task type is distinct from execution (no sweeps, no
  harness runs) and from feature work (no business logic).  The module's
  contract is: typed dataclass shapes, builders that ingest raw artifacts,
  query methods for downstream consumers, and an optional thin CLI entrypoint.
  
  **Evidence consumer module design rules:**
  - The module depends only on stdlib and data-format libraries (json, csv,
    pathlib, dataclasses).  Zero imports from business-logic packages
    (``<scheduling>``, ``<runtime>``, ``<adapters>``, harness runners).  This is a purity
    contract — the module is a leaf in the dependency graph, readable by
    anyone who understands the data schema, not the full codebase.
  - Use frozen dataclasses for evidence records, not bare dicts.  A
    typed evidence container (e.g. ``<EvidenceContainer>``) with typed fields
    and query methods (``by_scene()``, ``by_scheduler()``,
    ``metric_values_for()``) is the canonical interface — downstream consumers
    should import it rather than
    re-parse raw JSONs.
  - Provide builders that are independent of each other: one that reads a
    precomputed summary JSON, one that scans raw batch artifacts.  Both
    builders must produce identical records for the same underlying data —
    verify this mechanically.
  - When a typed evidence bridge exists and a figure generator or table
    builder needs the same data, prefer consuming the bridge over re-reading
    raw JSONs.  A figure generator that re-parses raw JSONs when a typed
    bridge already exists is code duplication — the bridge is the canonical
    source of derived evidence records.
  - The module is importable (``from <pkg>.<module> import <symbol>``) — it
    is not a one-off script.  A thin ``if __name__ == "__main__"`` block may
    provide CLI convenience, but the public API is the importable surface.
  
  **Test expectations for evidence bridge modules:** A pure-data bridge module
  (JSON → dataclass → query methods) where every query method is a simple
  dict/list traversal needs at minimum a smoke test: load from real or toy
  data, verify the count matches expectation, verify key methods return
  non-empty results, and verify the builders produce identical output.  A
  bridge module that performs non-trivial computation (aggregation, filtering,
  derived metrics) needs unit tests for each computation.  A module whose
  only logic is ``json.load`` + ``dataclass`` construction still benefits
  from a one-line count assertion — it catches silent JSON schema drift.
  
  **CLI entrypoint pattern:** When the module also serves as a CLI entrypoint
  (``python -m <pkg>.<module>``), use this pattern to avoid ``__init__.py``
  double-import warnings:
  
  ```python
  # At module bottom:
  def main() -> None:
      ...  # argparse, load, print summary
  
  if __name__ == "__main__":
      main()
  ```
  
  Do not import the module at package ``__init__.py`` level if it is also
  invoked via ``-m`` — the module import at init time triggers ``main()``
  before ``__name__ == "__main__"`` is true, producing a double-run or
  double-import warning.  Either (a) keep ``__init__.py`` imports lazy
  (inside functions), or (b) re-export only the symbols consumers need via
  explicit ``from .module import Symbol`` in ``__init__.py``, not a blanket
  ``import`` of the module.

## Execution and Evidence Tasks

When the task is execution (sweeps, evidence regeneration, figure generation)
rather than code edits, apply the rules below.  When the task is hybrid (code
fix + required evidence re-run), apply both this section and the Hybrid Tasks
section that follows.

### Stale Cache Is an Evidence-Integrity Threat

**The most dangerous silent failure mode in research execution tasks is stale
cached outputs.** A code fix lands, the sweep re-runs, but the harness reads
pre-fix cached results from disk and no one notices. The evidence tables show
the old degenerate numbers, and the task is accepted with a false claim of
"fix verified."

Before any re-execution that follows a code fix:

1. **Identify every cache surface the target harness uses**: per-scene batch
   caches, derived evidence subdirectories, precomputed indexes, intermediate
   artifact directories, the batch directory itself (prior-run raw artifacts
   from a different experiment configuration), and any `skip_cached_outputs`
   or workspace-cache mechanisms the harness employs.
2. **Clear every cache that could serve pre-fix data for the fixed component.**
   A cache keyed by `<scheduler>_<scene>` that was written before the fix
   must be deleted. A derived evidence subdirectory computed from pre-fix raw
   artifacts must be deleted. **Prior-run raw batch artifacts** in the batch
   directory that were produced by a different scheduler subset, a different
   spec enumeration, or a different experiment configuration must be deleted
   before re-sweeping into the same directory.  A batch directory that
   accumulates artifacts from multiple runs with different enumerations
   produces misleading counts (e.g., 305 JSONs for 304 specs) and silently
   pollutes downstream evidence surfaces.  Do not clear caches for unrelated
   components (other schedulers, other scenes) unless they share a cache key
   with the fixed component.
3. **Verify clearance**: grep or list the cache directories and the batch
   directory to confirm entries for the fixed component are absent before
   launching the re-run.  When re-running a full sweep, verify the batch
   directory is empty or contains only the expected experiment_id artifacts
   from the current sweep configuration — not artifacts from prior runs with
   different enumerations.

This applies equally to pure execution tasks (re-running after a prior
session's fix) and hybrid tasks (code fix + re-run in the same session).
A re-run that serves stale cache is a re-run that didn't happen.  A re-run
into a batch directory that still holds prior-run artifacts is a re-run
whose evidence surface is contaminated.

### Execution Protocol

**Pre-execution: confirm the components are wired.** Before running a sweep,
verify that every component the task claims to exercise is actually enumerated
in the sweep spec builders. A common failure mode: scheduler X is in the
registry but the sweep spec builder iterates a hardcoded list that omits X.
Fix the enumeration gap before execution — this is a one-line spec change,
not a rewrite.

For figure-generation tasks, the parallel check is **display-map completeness**:
verify that every evidence component present in the data matrix has a
corresponding entry in the display map (label, color, marker). A component
that exists in the data but has no display-map entry silently renders with
fallback styling — gray dots, raw key strings, default markers. Fix the
display map before rendering; do not accept fallback rendering. See "Figure
Generation and Evidence Visualization" below for the full protocol.

**Scope discipline for execution.** An execution task's scope is the sweep or
evidence target named in the request. Do not expand to new scenes, new
schedulers, new ablation regimes, or new stress conditions unless the task
explicitly includes them. Do not attempt refactors, rewrites, or "while we're
here" cleanups during an execution task — they risk changing the behavior being
measured.

**Run sweeps with continue-on-error semantics.** Long-running multi-scene
sweeps should use `continue_on_error=True` so one scene failure does not block
the rest. Collect failure records and report them; do not silently discard
failures.

**After execution, rebuild aggregate artifacts if needed.** Sweep runners that
write batch index files may produce partial or overwritten indexes after
incremental runs. After any sweep execution that adds experiments to an
existing batch directory, verify the index covers all experiments on disk.
If the index is partial, rebuild it from the on-disk artifact files before
running downstream evidence suites.

**Evidence regeneration is downstream of artifact completion.** After sweep
execution completes and the batch index is whole, regenerate evidence suites
and paper figures that depend on the new data. Run the evidence-integrity
manifest check and confirm `data_gaps` reflects the actual state — zero gaps
when all expected experiments produced artifacts, explicit gap descriptions
when some are missing.

**Map verification criteria to actual output schemas.** When a task's
verification criterion uses schema terminology that does not match the
framework's actual output format (e.g., the task says "confirm `data_gaps:
{}`" but the evidence suite writes `failure_context` instead), do not
silently translate between schemas.  Map the task's term to the actual output
field explicitly in the verification report, state why the mapping is correct,
and verify the actual field satisfies the task's intent.  A silent translation
where the reviewer cannot see the mapping is an evidence-integrity risk.  If
the mapping is ambiguous or the actual field cannot satisfy the task's intent,
flag it as a scope-clarification need before reporting completion.

**Verify field existence at the claimed path; do not assume.** Before reporting
that a field (``data_gaps``, ``failure_context``, ``<metric_summary_field>``) is present in a
file (``summary.json``, ``manifest.json``), verify mechanically that the field
exists at that exact path in that file — `python -c "import json;
d=json.load(open('path')); print(d.get('field', 'NOT FOUND'))"` or equivalent.
A field that appears in one artifact (the figure-generator output) does not
necessarily appear in another (the sweep summary).  Reporting a field as present
at a path where it doesn't exist — because the field lives in a different file
or is injected by a downstream processor — produces a false verification claim.
If the field is absent, find its actual location and report the mapping
explicitly.  Never report `data_gaps: {}` or `failure_context: 0` without
confirming the field key exists in the claimed file and the value matches.

**Record degenerate results; do not hide them.** When an experiment produces
technically-valid artifacts but the metrics are degenerate (all-zero QoE,
100% frame-drop rate, zero bytes selected, zero deadline hits), record this
as the finding. Do not massage, filter, or exclude these artifacts from
evidence surfaces. Degenerate results are scientific data — hiding them
creates an evidence-integrity gap. Downstream paper narrative can explain
degenerate outcomes (e.g., "parameter-sensitive at default configuration")
but the data must be present and visible.

**Disaggregate failure counts; do not collapse them into a single "0 failures"
or "N failures" claim.** When an evidence artifact contains multiple failure
categories (coupled_stress, deadline_hit, mechanism_attribution, etc.), report
each category's failure count separately.  Expected structural entries from
cross-suite aggregation (e.g., "missing stress condition" entries injected
because one sweep doesn't produce stress data that a different sweep owns) are
not the same as real failures (e.g., deadline-hit scoring failures, degenerate
QoE, zero-lifecycle scenes).  Collapsing both into one "0 failures" claim when
the structural entries number in the hundreds is a correctness defect — the
report claims zero when the file shows 285.  Report the actual counts per
category and explain which categories represent expected cross-suite artifacts
vs. real failures.  Verify the counts mechanically: `grep` or `python -c` the
actual file; do not report them from memory or expectation.

### Figure Generation and Evidence Visualization

When the task is figure generation (producing paper figures, plots, or tables
from existing evidence), apply the rules below in addition to the general
execution and evidence rules above.  Figure generation is a read-only operation
over evidence — the components and data already exist; the task is faithful
rendering, not re-execution or re-implementation.

**Pre-generation display-map inventory.** Before rendering any figure, inventory
the display map (style map, label map, color map, marker map) that translates
evidence component names to visual attributes.  Verify that every component
present in the evidence suite (schedulers, methods, baselines, scenes,
conditions) has an entry.  A component that exists in the evidence but has no
display-map entry silently renders with fallback styling (gray dots, raw key
strings in legends, default markers) — the figure is technically non-empty but
the fallback is wrong.  A display map with M entries against N evidence
components (M < N) is a pre-generation defect.  Fix the display map before
rendering; do not accept fallback rendering as correct.

Also cross-reference the display map against the scheduling registry and the
harness spec-builder that produced the sweep.  A scheduler that exists in the
registry but is absent from the display map will render as a fallback gray dot.
A scheduler that exists in the display map but not in the sweep data is dead
styling.  Extract the key set from the registry (``<registry_dict>.keys()``
or equivalent), from the harness enumeration, and from the display map — all
three sets must agree.  This is a mechanical check, not a design-reasoning
check: run the extraction command and compare.

**Pre-generation cardinality verification.** Before rendering, mechanically
verify the evidence cardinality against the expected figure dimensions.  For a
per-scene × per-scheduler grid: count artifact files on disk, verify N
schedulers × M scenes = N×M artifacts, confirm no duplicates and no extra
artifacts from prior runs with different enumerations.  A figure that renders
from a partial evidence set (silent row/column drops) is an evidence-integrity
gap.  Verify cardinality from the filesystem, not from design reasoning — run
`ls` or `find`, count, and compare.

**Degenerate panel handling.** Before rendering, analyze the evidence matrix
for structurally degenerate cells: scenes with zero reference-lifecycle data,
configurations with non-positive QoE on all scenes, budget constraints that
make certain metrics structurally zero, or configurations whose output is
bit-identical to another configuration.  Record each category in the figure
manifest or a companion diagnostic log.  Render degenerate cells with their
actual values — do not drop, skip, or filter them.  Degenerate cells are
scientific data; hiding them creates an evidence-integrity gap.  An empty or
missing panel (no data at all) is not the same as a degenerate panel (data
exists but metrics are zero/extreme) — log the difference explicitly.

**Data-property vs. rendering-bug distinction.** Before attributing a visual
artifact (overlapping bars, narrow band, crowded legend, flat line) to a
rendering bug, verify the underlying data.  Low-variance schedulers that produce
QoE in a narrow band (e.g., 1.0–4.0 across all scenes) will visually overlap in
bar charts — this is a data property, not a rendering defect.  All-drop
schedulers that produce zero QoE on many scenes will have thin bars — this too
is a data property.  Verify by inspecting the actual per-scene values: if the
data ranges are genuinely narrow, the visual artifact is correct.  Document
low-variance or low-discriminating-power schedulers as evidence findings (they
are insensitive to scene variation).  Do not misclassify a data property as a
"figure-generation issue" or "plot layout bug" — this misleads the next
developer about where the fix should land.

**Aliasing detection.** When multiple labeled configurations produce identical
output values across all scenes (e.g., scheduler A and scheduler B have the
same per-scene QoE for every scene), this is a data-quality signal.  Record
it — do not silently accept it as correct.  Aliasing may be by design (e.g.,
schedulers that share the "no reference images" baseline path) or it may be a
wiring defect (two registry keys resolve to the same implementation).  Verify
the aliasing count by comparing the actual data matrix column-by-column, not by
design reasoning alone — design reasoning can undercount or misclassify aliased
pairs.  Document which sets of configurations are aliased and whether the
aliasing is intentional or suspicious.  Aliased configurations are still real
evidence; do not drop them.

**Figure-specific verification gates.** After rendering, verify:

- **File-size gate:** every rendered image (PNG, PDF) is above a minimum size
  threshold (e.g., 80 KB for a multi-panel PNG, 18 KB for a single-panel PDF).
  A file below the threshold is likely blank, empty, or rendered from zero data
  points — a silent failure that looks like success.
- **Per-panel data presence:** for multi-panel figures (grids, subplots, small
  multiples), verify every panel or cell contains actual data points, not empty
  axes, NaN-only regions, or single-point degenerate plots.  A figure with N×M
  grid cells should have N×M populated cells — zero empty.
- **Legend/scheduler completeness:** every evidence component that appears in
  the data matrix must appear in the figure legend (or equivalent label surface).
  A legend with fewer entries than the data matrix is missing evidence.
- **Display-map completeness:** the display map (label, color, marker) must
  cover all evidence components present in the data matrix.  A component that
  exists in the evidence but has no display-map entry silently renders with
  fallback styling (gray dots, raw key strings, default markers).  Fix the
  display map before rendering; do not accept fallback rendering as correct.
  This check was already performed in the pre-generation inventory — re-verify
  it mechanically against the rendered output.
- **Cross-surface registry/display-map/harness sync:** the figure generator's
  display map and scene/scheduler lists must match the scheduling registry
  and the harness enumeration that produced the sweep.  A scheduler present
  in the registry but absent from the display map is a pre-generation defect.
  A scene present in the harness sweep but absent from the figure's per-scene
  axis is an evidence gap.  Verify mechanically: extract the key set from the
  registry, from the harness spec-builder, and from the display map — all
  three must agree.
- **Cross-reference against paper blueprint:** if the task's Context or
  Boundaries reference a paper blueprint document, enumerate the figure families
  the blueprint requires and verify every required family was generated.  A
  blueprint that requires N figure families and the generator produces M (M < N)
  is incomplete — flag the missing families explicitly in the manifest, not as a
  silent skip.
- **Degenerate and aliased categories recorded:** the figure manifest or
  companion log must explicitly record degenerate categories (zero-lifecycle
  scenes, budget-constrained scenes, all-drop schedulers) and aliased
  configurations (different labels producing identical output).  Aliasing must
  be verified mechanically against the data matrix, not from design reasoning
  alone.  Degenerate and aliased data are still evidence — record them, do not
  drop them.
- **Data-property vs. rendering-bug confirmed:** before attributing a visual
  artifact (overlapping bars, narrow band, crowded legend, flat line) to a
  rendering bug, verify the underlying data.  Low-variance schedulers with a
  narrow QoE band will visually overlap — this is a data property, not a
  rendering defect.  All-drop schedulers will have thin/absent bars — this too
  is a data property.  Inspect the actual per-scene values before reporting a
  rendering issue.

**Post-execution verification checklist:**

- batch artifacts exist on disk and are non-empty for every expected experiment;
- the batch artifact count matches the expected spec count (N schedulers × M scenes
  = N×M artifacts); extra artifacts from prior runs with different enumerations are
  absent;
- the batch index (if used) covers all on-disk artifacts with no duplicates;
- the evidence suite ingested the new data (all expected rows, no silent drops);
- paper figures and tables reflect the new data (not stale pre-execution state);
- the evidence-integrity manifest reports accurate gap status;
- the test suite has no regressions (sweep execution should not change test
  behavior, but verify anyway);
- degenerate results are present in figures/tables, not filtered out;
- all figure-specific verification gates (above) passed when figures were
  in scope.

## Hybrid Tasks (Code + Evidence Re-run)

When a task requires both code changes AND subsequent re-execution of evidence
suites (the most common form: fix a regression, then re-run harnesses to
confirm the evidence tables are no longer degenerate), the task is a single
unit with two phases — code fix, then evidence re-run.  Neither phase alone
satisfies the acceptance contract.

**Do not report completion after the code fix alone.** Tasks often embed the
re-run requirement in the Boundaries section (e.g., "Re-run: after the fix, run
``<harness_script>.py`` then ``<figure_generator>.py``. Confirm manifest.json
``data_gaps: {}``").  Treat this as a required deliverable with the same weight as a
requested test.  A developer report that says "fix complete, next step harness
re-run required" is a progress checkpoint, not a completion claim.

**Phase 1 exit / Phase 2 entry gates:**
- the code fix passes all existing and new tests;
- the fix has been verified at a single datapoint (in-process reproduction);
- the mechanism (root cause) is confirmed, not guessed;
- **stale caches for the fixed component have been cleared** (see "Stale Cache
  Is an Evidence-Integrity Threat" above) — entering Phase 2 without clearing
  caches that could serve pre-fix data invalidates the re-run.

**Phase 2 exit conditions:**
- the evidence table containing the fixed entry shows non-degenerate numbers
  (not the same all-drop failure as before the fix);
- the evidence-integrity manifest confirms zero gaps for the fixed entry;
- all scene/environment counts match expectations;
- figures and aggregate tables reflect the new data.

**When the fix is sufficient (all exit conditions met):**
- Report the before/after values for every acceptance-criteria metric;
- Update the project's status/memory files to record that the blocker is
  resolved — a stale status file that still lists the blocker as open is a
  documentation defect;
- If the task's Context references specific status documents (e.g.,
  `current_status.md`), update them to reflect the resolved state.
  Before editing, resolve the file's concrete path using the Context's
  document-path conventions (see "Document consultation" in "Before You
  Touch Anything") and verify the file exists on disk.  A report that
  claims to have updated a status file that does not exist at the claimed
  path is a correctness defect — the update either went to the wrong path
  or was never written.

**When the fix is insufficient (evidence row still degenerate):**
- **Stop.** Do not iterate, do not attempt a second diagnosis pass, do not
  expand scope. The task's contract is "confirm the fix resolves the blocker
  OR document that deeper diagnosis is needed" — not "keep debugging until
  it works."
- Document the exact values that are still degenerate (which metrics, which
  scenes, what numbers), contrasting them against the acceptance criteria.
- State the conclusion: "Deeper diagnosis needed — the fix alone does not
  resolve the all-drop. Possible causes: [list]. Recommended next step: [one
  concrete action]."
- Do not silently accept a task where the fix's own row is still degenerate.
  A task accepted with stale pre-fix evidence is an evidence-integrity
  failure.

When the re-run produces errors unrelated to the code fix (e.g., an unrelated
scene times out, a network fetch fails), record them but do not block acceptance
on them — the fix's evidence row is the acceptance surface.

**When diagnosis finds no code change is needed.** If the hybrid task's code
phase concludes that the suspected defect is an expected structural constraint
(pipeline-gap state d) and no code was changed, Phase 2 (evidence re-run) is
not required — there is no fix to verify.  The deliverable is the diagnostic
evidence (component traces, computed values, evidence cross-reference) and the
status-doc update.  Do not skip Phase 2 when code WAS changed — even a
one-line fix requires re-verification of the evidence row to confirm the fix
resolved the target regression.

**When Phase 2 is infrastructure-blocked.** The code fix passes all tests, but
the required evidence re-run cannot execute because the current environment
lacks the necessary hardware (GPU, specific device), data, or tools.  This task
is **BLOCKED**, not complete.  Report:

- the exact infrastructure missing (GPU model/VRAM, CUDA version, specific
  data file, CLI tool, python executable, conda env);
- the exact commands that will run the evidence re-run when the infrastructure
  becomes available;
- confirmation that the code half (Phase 1) is complete and tests pass
  (baseline count preserved + new tests green).

Do NOT report the task as DONE or ACCEPT.  Do NOT accept the task from a
developer who reports "blocked on GPU" without the BLOCKED classification and
the infrastructure inventory.  An infrastructure gap is a scheduling problem
for the user, not a completion of the task's acceptance contract.

## Pre-Edit Inventory (Refactoring Tasks)

For tasks that move, split, rename, or restructure code, establish the
following inventory before editing. These checks are mechanical surface
audits — they supplement the mandatory "Before You Touch Anything" checks
above, not replace them.

**Scope and surface inventory:**
- files and directories relevant to the requested change;
- expected source, test, harness, export, docs, and dependency surfaces;
- files that must be left untouched by scope;
- any explicit allowed-file list or explicit excluded surfaces from the user
  request, treated as a hard scope fence;
- existing test and harness layout when relevant;
- current dirty or untracked files, without reverting user work;
- prerequisite data: when a task adds a scene, method, or variant to an
  existing pipeline, verify the on-disk prerequisites exist before editing.

**Deliverable extraction:** Before editing, extract explicit deliverables from
the task's Boundaries, Reviewer Focus, and Objective sections. Deliverables
fall into three categories:
- (a) **code deliverables**: "add a test for X," "rename class Y," "extract
  module Z" — produce the artifact and verify it passes/fits;
- (b) **behavioral demonstration deliverables**: "verify that metric M changes
  when algorithm A is toggled," "confirm no all-drop at operating budget" —
  the test or in-process reproduction must show the delta;
- (c) **execution/evidence deliverables**: "re-run harness H then figure
  generator F and confirm manifest data_gaps: {}" — the re-run must complete
  and the evidence row must show non-degenerate numbers. When a code-fix task
  carries an execution deliverable in its Boundaries, the task is not complete
  until the evidence surfaces reflect the fix.
Before reporting completion, verify ALL deliverable categories are satisfied.
These are part of the task's acceptance contract, not suggestions.

**Import surface inventory (for module moves and extractions):**
- search every import form that touches the affected module, classify each
  consumer as source-internal or test;
- search test files for `monkeypatch.setattr(<module>, ...)` — every
  monkeypatched name must appear in any re-export shim;
- check relative-import depth changes when files cross package boundaries;
- check for circular-import risk when extracted modules need to reference
  types still in the parent module.

**Package-boundary inventory (for narrowing re-exports):**
- grep for consumers that import through the package namespace (not the
  canonical module path); classify as source-internal, test, or external;
- if zero consumers: delete the blanket import directly; if consumers exist:
  redirect them or keep explicit single-symbol re-exports.

Treat a suddenly empty or partially missing tree as an integrity blocker. Do
not reconstruct missing code from memory, plans, or old outputs unless the user
asks for restoration from a trusted source.

If the request names an exact allowed-file set, edit only those files. Do not
self-expand the allowed-file list.

## Implementation Style

Prefer code that is short, direct, and easy to read in execution order. The
data flow should be visible: inputs, validation, transformation, calls,
outputs, and side effects should appear in a natural order.

Code should not be more complex than necessary. If a simple implementation
clearly satisfies the current task, keep it simple. Inline or use local helpers
when logic is used once and remains readable.

**No redundant conditional branches.**  When two or more arms of an
``if``/``elif``/``else`` or ``match``/``case`` perform the same operation,
merge them.  Redundant branches are a readability defect — they force the
reader to compare arms to discover they are identical.  This includes:

- ``if cond: do_X() else: do_X()`` — delete the conditional;
- ``if a: do_X() elif b: do_X() else: do_Y()`` — merge ``a`` and ``b`` with
  ``or``, or extract the shared predicate;
- two ``case`` arms with identical bodies — merge into one.

Use names from the current domain contract and existing code semantics. Keep
one concept's spelling consistent across code, config, tests, harnesses,
artifacts, prompts, and docs.

When a dataclass is described as JSON-serializable, default to standard-library
serialization (`dataclasses.asdict` + `json.dumps`).  Do not add custom
`to_dict()`, `asdict()`, or `to_json()` methods unless the standard path is
insufficient — and even then, document why.  A frozen pure-data dataclass
should serialize mechanically from its fields with zero transformation.

### Centralized Domain Predicates

When a centralized function already classifies a domain concept (e.g.,
``_<classify_priority>`` that determines whether a candidate is a base layer),
do not scatter literal string comparisons (``candidate.layer == "base"``) that
duplicate that classification in other modules.  The scattered literal will
drift from the centralized function when the data format evolves (e.g., real
data uses ``<real_label_format>`` but the literal only matches the synthetic
``"<test_fixture_label>"`` from test fixtures).

This anti-pattern — a centralized classification function exists but call sites
bypass it with ad-hoc string comparisons — is a correctness defect.  The fix is
a shared predicate that delegates to the centralized function and replaces every
scattered literal comparison.  Place the shared predicate in the same module
that owns the centralized classification logic, and import it in every consumer
that previously performed the literal comparison.

### Abstraction and Interfaces

Abstraction must have real semantic value. Delete abstractions that provide no
reuse value, boundary value, invariant value, or testability value.

Extract helpers, adapters, registries, factories, contexts, or interfaces only
when they:

- eliminate real duplication (the same logic written in multiple places);
- define a stable boundary that isolates a genuine change point;
- preserve a cross-module invariant;
- shorten caller code measurably;
- make tests simpler by narrowing what must be set up;
- separate conceptually distinct concerns into named modules with clear
  ownership.

Do not create abstractions that:

- only rename, wrap, unwrap, or reassemble data (the "拆开又合上" pattern);
- add a thin forwarding layer that each caller must pass through;
- exist solely because "we might need to extend this later";
- make callers write more boilerplate than the abstraction saves.

**Do not add dead future-proofing placeholders.**  This anti-pattern — adding a
CLI option, enum value, ``Literal`` member, config flag, or code branch that
raises ``NotImplementedError`` or is otherwise non-functional — violates the
"no extension for future" rule at the code surface.  Specific forms to avoid:

- ``choices=["working", "not_yet_implemented"]`` in argparse where the
  second choice raises ``NotImplementedError``;
- ``Literal["current", "aspirational"]`` with a dead member that no
  code path exercises;
- ``if mode == "now": ... else: raise NotImplementedError`` — dead code
  that promises behavior the implementation does not deliver;
- config flags, enum members, or registry entries that exist only because
  a future task might need them.

Add the option, branch, or member in the same change that implements it.
A ``NotImplementedError`` in a code path the CLI advertises is a correctness
defect — the interface claims a capability the code does not have.

**Domain model field is the typed interface.** When a domain-layer dataclass
already carries the relevant field (e.g., `<record_type>.<field_name>:
Sequence[float]`), that field is the typed contract.  A component that produces
values matching that field's type is already wired to the domain interface — no
separate Protocol, ABC, or adapter interface is needed.  Add a Protocol or ABC
only when a second implementation with polymorphic dispatch is imminent, and
even then consider whether a simple union type, callback, or optional field
suffices before introducing an interface hierarchy.

For each core abstraction (registry, adapter, factory, config object, runner,
pipeline, plugin interface), evaluate its cost against its benefit: does it
reduce repeated implementation? Does it shorten caller code? Does it make
method replacement clearer? Does it make harnesses easier to run? Does it make
tests simpler?

A **composition root** (`spec → resolve → resolved`) is one of the
highest-value abstractions in research codebases.  Break a messy inline
resolution path into three clean layers:

1. **Spec**: frozen, pure-data, JSON-serializable dataclass that records
   *what* to run — no instances, callables, closures, or adapter objects.
2. **Resolution function** (the composition root): the single place that binds
   a spec to concrete implementations via the registry or factory.
3. **Resolved object**: frozen dataclass holding the fully-instantiated
   dependencies, ready for execution.

This pattern pays for itself immediately: (a) the spec is serializable and
auditable, (b) all instantiation logic lives in one auditable function, (c)
downstream code receives fully-resolved objects and never mixes config-reading
with execution, and (d) adding a new experiment variant is a one-line spec
change.  Use it when inline resolution is scattered across multiple functions,
when config objects leak implementation details, or when a task explicitly
asks for a composition root.

An **evidence pipeline** (`raw artifacts → typed bridge → downstream consumers`)
is the read-side parallel to the composition root.  When a full-sweep produces
hundreds of raw batch JSONs and multiple consumers (figures, tables, reports,
analysis) need to read them, break the consumption path into three layers:

1. **Raw artifacts**: batch JSONs, per-experiment outputs, sweep manifests —
   write-once, read-many, the ground-truth evidence.
2. **Typed evidence bridge** (summarizer / evidence container): a pure-leaf
   module that reads raw artifacts, validates shape, and produces typed frozen
   dataclasses with query methods (``by_scene()``, ``by_scheduler()``,
   ``metric_values_for()``).  This module depends on nothing but stdlib and
   data-format libraries — it is the single parse point for raw evidence.
3. **Downstream consumers**: figure generators, table builders, report scripts,
   analysis notebooks — they import the typed bridge and query it, never
   re-reading raw JSONs.

This pattern prevents the most common evidence-integrity failure mode: multiple
consumers parsing the same raw JSONs with slightly different key lookups,
default values, or filter logic, producing inconsistent numbers across figures
and tables.  When a typed bridge exists, all consumers get the same data through
the same parse path.  A figure generator that re-parses raw JSONs when a typed
bridge already exists is code duplication — migrate it to consume the bridge.

The typed bridge is NOT a dependency of business-logic packages.
``<scheduling>``, ``<runtime>``, ``<adapters>``, and harness runners must not
import the evidence bridge.  The dependency direction is one-way: business logic
produces artifacts; the evidence bridge reads them.

If an abstraction causes boilerplate (e.g., every new method must touch
multiple registration points, write multiple config blocks, or add multiple
wrappers), prefer a more direct design.

**Do not add config plumbing for components that don't need it.** A config
flag, CLI argument, or dataclass field for a component is only justified when
the component's behavior meaningfully varies by configuration AND experiments
need to sweep that variance.  If a component has no configurable surface (no
tunable parameters, no algorithm variants, no on/off toggle that changes
observable behavior), it should carry zero config plumbing.  Adding a
`use_<component>: bool = True` flag that no code path would ever set to
`False` is dead config — a maintenance liability, not future-proofing.
When a component gains configurable behavior later, add the config plumbing
in the same change that introduces the variance.

If an interface forces every caller to pass many parameters, consolidate stable
context into config objects, run contexts, or explicit data structures — but do
not introduce a heavy framework to do so.

If a config system requires simple experiments to write large config files,
prefer lighter defaults, local overrides, or command-line semantics.

**Place imports at module level unless there is a specific, justified reason to
defer them.**  An import inside a function body adds visual noise, makes the
dependency surface harder to inventory, and forces re-import on every call.
The only justifying reasons are: (a) the import is expensive and the function is
rarely called, (b) the import would create a circular-import cycle at module-load
time, or (c) the module is conditionally available (optional dependency).
"Used only in one function" is not a reason — the import still belongs at the
top of the file.  Stdlib modules (``copy``, ``os``, ``json``, ``math``, etc.)
have no plausible justification for function-body import — they are always fast
and always available.

**Do not add function-local imports that duplicate module-level imports.** When
a symbol is already imported at module level in the same file, adding a local
import of the same symbol inside a function body (with or without an alias —
e.g., ``from <stdlib_module> import <Symbol> as <alias>`` when ``<Symbol>`` is
already a module-level import) creates a dead import path.  The module-level
import is already available in the function's closure; the local import is
redundant code — it adds visual noise and misleads the reader about
availability.  This applies equally to aliased forms: ``import X as Y`` at
module level followed by ``from package import X`` locally, and vice versa.
Delete the local duplicate; use the module-level import.

The same rule applies across the whole file: if two functions each add a local
``from <stdlib_module> import <Symbol>`` or similar, and one of those imports is
never used, it is an unused import — remove it.  A function-local import is
only justified when the symbol is NOT already available at module level AND the
import is expensive or creates a circular-import risk at module-load time.

If splitting modules creates many cross-module forwarding functions, thin
wrappers, or single-use abstraction layers, merge or simplify those modules.

### TypedDict Pitfalls

When using `typing.TypedDict` (especially with `Required` and `NotRequired`):

**Do not use `from __future__ import annotations` in a file that defines
TypedDicts with `Required` or `NotRequired`.**  PEP 563 defers all
annotations to strings at class-definition time.  `typing.Required` wraps
its argument in an annotation that cannot be resolved when annotations are
strings — `TypedDict.__required_keys__` silently becomes empty
`frozenset()`.  The `Required` annotations look meaningful but have zero
runtime effect.

This is a correctness defect, not a style preference.  If the file also
needs `from __future__ import annotations` for other reasons (forward
references), move the TypedDict definitions to a separate file, or use
`TYPE_CHECKING`-guarded imports plus string-literal forward annotations
on the referenced types — never on the `Required`/`NotRequired` wrapper
itself.

After defining a TypedDict with `Required` keys, mechanically verify
that `__required_keys__` is non-empty at runtime.  An empty frozenset
means annotations are unresolved — the `__future__` import, a string
annotation, or an indirect reference is breaking resolution.

**TypedDict `Required` and `NotRequired` are static-analysis signals
only.**  They do not enforce anything at runtime — constructing a
TypedDict with a missing `Required` key does not raise.  When the
task's docstring or comment says certain keys cause a `ValueError` or
other runtime failure, the enforcement must come from real validation
code (a loader function, a `_require_*` helper, a JSON schema check).
Document the real enforcement site, not the annotation.

**Prefer `total=False` for backward compatibility** when existing
callers pass plain `dict[str, Any]`.  A `total=False` TypedDict is
structurally compatible with arbitrary dicts — all keys are optional
at the type-checking level, with `Required` carving out the
non-optional subset.  TypedDict is a `dict` subclass, so plain-dict
callers continue to work at runtime.

**Match TypedDict field names to actual dict keys** produced and
consumed by existing loaders, parsers, and callers.  Renaming a field
to a "cleaner" name when JSON keys use the old name breaks every caller
that accesses the dict by key.  If a rename is warranted, it is a
separate slice with consumer migration — do not rename keys inside a
TypedDict introduction.

**Genuinely-open-ended dicts stay as `Mapping[str, Any]`.**  When a
dict shape is per-scheduler, per-operation, or carries arbitrary
user metadata with no stable key set, wrapping it in a `total=False`
TypedDict adds documentation weight without type safety.  The
TypedDict should document the keys that every legitimate consumer
actually reads — if no consumer reads a key in a typed way, there is
nothing to type.

### File Granularity and Module Decomposition

File length is a design signal, not a fixed line-count rule. Judge it against
the target language, framework ecosystem, existing repo style, and the
function's complexity.

Each file should carry a single clear theme: one interface, one adapter family,
one metric family, one data-processing step, one harness entry, one export
shape, or one test group.

If a file mixes config parsing, data processing, method implementation, metric
computation, harness execution, and result export, split it into smaller
logical files or modules.

Before organizing files, first identify sub-responsibilities: input parsing,
core processing, external calls, result computation, artifact export, error
handling, test support. Then place related content into appropriate modules.

Avoid creating or keeping "god files," mega-runners, all-in-one utils, or misc
helpers. A general utility file should only contain stable, narrow, genuinely
multi-consumer code. If a utility file accumulates unrelated helpers, split by
semantic area rather than piling more into the same file.

Conversely, do not over-split into thin wrappers, pure forwarding files, or
fragmented modules that exist only to have more files. The goal of splitting is
higher cohesion and better change locality, not a higher file count.

After extraction from a god-module, a target module may still be long (e.g.,
a 700-line loader module).  If every line serves the module's single clear
theme, the length is acceptable — coherence, not line count, is the test.
Flag the file for potential further decomposition in framework docs, but do
not force a second split when no clear sub-theme boundary exists.

When adapting or porting external code that is itself long or mixed-responsibility,
split it adaptively (within license terms) and record the source and main
changes in a comment or third-party notice.

### Subfolder Organization in Existing Repos

This skill does not initialize repositories, but it should organize
subfolders within an existing repo when the current function's natural boundary
calls for it.

Subfolder splits should come from real needs of the current task and existing
framework: a harness growing complex, a test category needing independent
fixtures, a method needing multiple variants, an export pipeline needing an
independent schema.

Name subfolders semantically to express their functional purpose. Do not use
abstract numbering (`c1/c2/c3`, `b1/b2/b3`).

If complex functionality is crowded into one file or directory, consider
splitting into clearer sub-modules and sub-directories. If splitting would make
paths more complex, call chains longer, or introduce boilerplate, prefer the
simpler flat structure.

Keep subfolder organization consistent with the existing repo style. Do not
force a different directory philosophy.

Public/shared layers should only contain genuinely common, stable capabilities
needed by multiple consumers. Locally-used helpers, data structures, configs,
state, or special logic should stay near their use sites. Special cases should
stay at their use sites — do not pollute shared layers for a minority use case.

**Package ``__init__.py`` should expose the public API.**  When a package has
callers, its ``__init__.py`` should re-export the symbols callers need so they
can ``from <package> import <Symbol>`` rather than importing from hidden
submodule paths (``from <package>._internal_module import <Symbol>``).  An
empty ``__init__.py`` (0 bytes) for a package with external callers forces every
caller to discover and depend on internal module paths — a coupling defect.
Re-export only the genuinely public symbols; private helpers stay in their
defining modules.  A package whose only callers are internal (same parent
package) may omit re-exports — the internal submodule paths are already the
canonical interface within the parent.

## Change Locality

Before writing code, identify the natural owner of the change:

- a method change should mainly touch method code and necessary comparison or
  registration surfaces;
- a baseline change should mainly touch baseline code and focused tests;
- a metric change should mainly touch metric definition, computation, export
  normalization if needed, and tests;
- a harness change should mainly touch the relevant harness area plus necessary
  shared interfaces;
- a result-artifact change should mainly touch artifact schema, export logic,
  and tests;
- a loader or manifest change should mainly touch the input layer and tests.

If one feature requires unrelated edits across many areas, treat that as a
framework-boundary risk. Do the smallest local refactor that brings related code
together, or report the coupling if a safe local refactor is outside scope.

Keep code that changes together close. Keep unrelated reasons to change in
separate modules. Public/shared layers should contain only stable capabilities
needed by multiple users; special cases should stay near their use sites.

### Breaking Import Cycles

When two packages have a bidirectional dependency (A imports B and B imports
A), break one direction first — do not try to sever both directions in one
slice. Choose the direction with fewer edges (fewer consumer imports to repoint).
Sever that direction completely, verify with grep that zero imports remain in
that direction, and leave the reverse direction for a separate, later slice.

The first direction broken is typically the "wrong way": the package that
imports from a package that should conceptually be its dependent. In the
canonical layered dependency, A depends on B; if B also imports A, break the
B → A direction by repointing B's consumers to their canonical modules.
The legitimate A → B direction stays until a later slice restructures the
composition (e.g., moving batch-execution logic into a dedicated runner or
composition root).

This is the safe, mechanical prerequisite for larger refactors: a bidirectional
cycle cannot be split, moved, or restructured until one direction is severed.

### Layered-Architecture Import Direction

Import-direction discipline applies even when no cycle exists.  A layered
architecture where package A depends on package B (A may import B) but B must
not import A is a one-way dependency contract.  Violating it — importing from
a lower layer into a higher layer in the wrong direction — silently couples
packages that the architecture intends to keep separate.  The symptom is the
same as a cycle (one package cannot change without re-verifying the other) but
the detection is harder because no circular-import error fires.

When a task's Boundaries or an architecture spec (e.g., ``<refactor_spec>.md``)
states an import-direction constraint (e.g., "``<package_a>`` must not import
``<package_b>``"), treat it as a hard scope fence.  Verify with `grep` before and
after every change that introduces a new import into the constrained package.
If the needed functionality lives in a package that the constrained package
must not import, place the shared logic in a common/dependency layer that both
packages may legitimately import (e.g., ``<common_pkg>/``), or restructure
so the higher layer passes the needed data down through the call chain rather
than the lower layer reaching up.

### When An External Refactor Spec Conflicts With Minimal Change

The "minimal change" default has two exceptions where an external spec's
recommendation should override it:

1. **The spec identifies a correctness defect that the current task will
   propagate.** This includes (a) evidence-facing labels (figure legends, table
   headers, chart titles) and (b) class or module names that appear in artifact
   metadata, registry keys, or harness output — misleading class names are
   correctness defects because they propagate into every figure, table, and
   evidence manifest that references the class. Fix the evidence-facing names
   now. For class renames where a registry key is a frozen public contract, use
   the rename-with-frozen-key protocol: update the class, preserve the key via an
   import alias, and add a dated WORKAROUND docstring.

2. **The spec identifies a structural change that would make the current task
   unnecessary or drastically simpler.** If the spec says "move the registry
   from config to a dedicated module" and the current task needs to add to that
   registry, moving it first avoids adding to a file the spec says should shrink.

For all other external-spec recommendations, keep the current change minimal
and flag deferred items in memory or the manifest with a reason.

When an external spec defines multiple independent structural changes (e.g.,
a refactor plan with numbered items), treat each independent change as a
self-contained slice: inventory that slice's surface, make the change, verify
with import smoke and targeted tests, confirm scope fences intact, then move
to the next slice. Each slice completes before the next begins. Do not batch
independent slices into one large change — per-slice audit precision (consumer
inventory, import graph, nontouch scope) degrades as the change surface grows.

### Relocation Protocols

When a task relocates a module, choose the protocol before editing:

1. **Inventory source-internal consumers** (search `src/` for all import forms
   of the module, excluding tests).
2. **Zero source-internal consumers** → **No-Shim Direct Relocation**: move the
   file to its canonical location, adjust import depths, redirect test imports,
   delete the old file. No shim, no later deletion slice.
3. **Source-internal consumers exist** → choose between direct redirection and
   a shim based on consumer count and dispersal:

   - **1–2 consumers in the same or adjacent packages** → redirect them
     directly in the same slice; no shim.  Creating and later deleting a shim
     for two import lines costs more than updating the two imports.
   - **3+ consumers, or consumers spread across distant/unrelated packages** →
     **Staged Package Migration (Re-Export Shim)**: move the module, leave a
     thin re-export shim at the old path.  Source consumers migrate later; the
     shim is deleted once all consumers are redirected.

**No-Shim Direct Relocation:**

1. Move the file to its canonical location (`git mv`, keeping content
   byte-identical).
2. Adjust relative-import depth inside the moved file.
3. Redirect every test consumer's import to the new canonical path.
4. Delete the old file — no shim, no re-exports, no later deletion slice.
5. Clear `__pycache__` under the source tree.
6. Verify: import smoke at new path, full test suite, grep for leftover
   references to old path, whitespace check, scope-fence audit.

**Partial extraction (symbol moves but old module lives on):** When a public
symbol is extracted from a module that retains other content — the old module
is not deleted — this is neither pure relocation nor full code extraction.
The relocation protocol still applies for the moved symbol: inventory consumers,
choose direct-redirect or shim by consumer count, update imports, and verify.
The old module's remaining content is untouched beyond removing the moved symbol
and cleaning orphaned imports.  No shim in the old module unless consumer count
justifies it (3+ as above).  Private helpers that stay in the old module and
were only used by the moved symbol should be moved with it or deleted if
now-unused; private helpers with remaining callers stay.

**Staged Package Migration (Re-Export Shim):**

Leave the old path as a thin re-export shim that imports every public name from
the new canonical location. The shim:

- imports every public name the old module previously exported;
- also re-exports any name that tests access as a module attribute for
  monkeypatching;
- has no logic, no side effects, and no new imports beyond the re-export line;
- is deleted once all consumers have migrated.

**Shim deletion:** When all consumers are migrated, inventory the shim's
import surface, monkeypatch bindings, and `__init__.py` gates. Migrate every
remaining consumer, verify the full test suite matches baseline, delete the
shim with `git rm`, and run absence grep to confirm no leftover imports of the
old path.

When the shim was created during a code extraction (see "Code extraction"
above), shim deletion is the final verification gate — Gate F in the
extraction verification sequence.  After deletion, re-run the full test suite
to confirm the baseline is unchanged and the shim was the only path providing
those symbols to consumers.

**Pure relocation constraint:** Every relocation slice carries an absolute
boundary: no new logic, no new defaults, no new fields, no new helper
functions. The only permitted changes are the file move, relative-import depth
adjustments, consumer-import redirections, and stale bytecode sweep.

### Boundary Changes Outside Relocation

Not every import-structure change is a file relocation. Three common patterns:

**Package-boundary narrowing (removing blanket re-exports):** When a package
`__init__.py` or public re-export surface leaks internal symbols through a
blanket import, narrow it to only deliberate, justified re-exports.

1. Inventory consumers that import through the package namespace (not the
   canonical module path). Grep for all import forms that reach the symbols
   through the package boundary.
2. If zero consumers: delete the blanket import directly. No shim needed.
3. If consumers exist: redirect them to the canonical module, or keep explicit
   single-symbol re-exports for genuinely public names. Never keep the blanket
   import as a "safe default" — it is the problem, not a safety net.
4. After deletion, run the import smoke test and the test suite that exercises
   the package boundary.

**Import repoint to canonical module (no file moved):** When a symbol is
defined in one module but consumers import it through a re-export surface (e.g.,
`<pkg_a>.<mod_a>` re-exports a symbol whose defining module is `<pkg_c>.<mod_c>`),
repoint the consumer import directly to the canonical
module. The symbol, defining module, and runtime behavior are all identical —
only the import path changes.

This is the primary technique for breaking a dependency cycle at the import
level without moving files. The canonical module is already the owner; the
re-export surface is the cycle edge.

1. Confirm the canonical module already defines the symbol (not just re-exports
   it). The canonical module's `def <symbol>` or `class <symbol>` is the ground
   truth.
2. Replace the import in each consumer: `from ..<re_export_pkg>.<mod> import
   <symbol>` becomes `from ..<canonical_pkg>.<canonical_mod> import <symbol>`.
3. If multiple consumers import through the same re-export surface, repoint them
   all in the same slice — leaving some consumers on the old path preserves the
   unwanted dependency direction.
4. After repointing, grep the consumer package for the old import path (`from
   ..<re_export_pkg>` or `import <re_export_pkg>`). Zero matches confirms the
   dependency direction is severed.
5. Do not delete the re-export in the old module during this slice. Other
   packages may still legitimately import through it. Narrowing or deleting the
   re-export is a separate, later boundary-narrowing task.
6. Verify: import smoke on both packages, targeted tests that exercise the
   repointed consumers, and an import-graph direction check — the consumer
   package should no longer import from the old re-export package.

The pure-relocation constraint applies to repoint slices: no new logic, no new
defaults, no new fields, no new helpers. Only the import path changes.

**Code extraction (carving logic into a new canonical module):** When a
god-module contains a coherent body of logic that belongs in its own module,
extract it while keeping the old module intact for its remaining
responsibilities.

-1. **Capture the pre-extraction baseline mechanically.** Before moving any
   code, run the full test suite and record the actual pass/fail/skip counts.
   This is the baseline.  The task description's claimed test count may be
   stale — prior slices may have added or removed tests without updating the
   task memory, and the task's own memory of the test count may date from
   before those slices.  The actual pre-extraction run count is the ground
   truth.  If it differs from the task's claim by more than can be explained
   by known prior-slice changes, flag it before proceeding — the task premise
   is stale and the baseline is ambiguous.  Record this baseline in the
   developer report so the reviewer can verify Gate C against it.

0. **Dependency ordering (multi-target only).** When a god-module will be split
   into multiple target modules across several slices, extract in dependency
   order — leaf-first. A dataclass/schema module depends on nothing internal;
   extract it first. A loader module depends on the schema; extract it second.
   A validation module depends on schema + load; extract it last. Each slice
   completes (code moved, consumers migrated, tests green) before the next
   begins. Do not batch independent extractions — per-slice verification
   precision degrades as the change surface grows.

1. **Name and create the new canonical module.** Before creating the module,
   verify the name describes the content being extracted, not an aspirational
   future state. A module that contains quality math (PSNR, SSIM) and a quality
   bridge should be named `render_quality/` or `quality_math/`, not `projection/`
   (which implies camera→raster pipeline code). After confirming the name
   matches the content, move the extracted code — no new business logic,
   defaults, fields, or helpers. Import-plumbing adjustments that are necessary
   for correctness are permitted: `TYPE_CHECKING` guards, inner-function lazy
   imports to avoid circular dependencies, and relative-import depth changes.
   These are mechanical correctness changes, not new logic.

   **Give the new module a single-line docstring** that states its single reason
   to change — e.g., ``"""Render module X output to pipeline Y frame inputs."""``
   or ``"""Shared validation and requirement helpers for <package>."""``.  The
   docstring is the first thing a future developer reads when asking "does this
   module own the change I'm about to make?"  It should be a fact about the
   module's content, not an aspirational claim about future state.
   
   **Do not add `# noqa: F401` on `TYPE_CHECKING` imports.**  Linters (ruff,
   flake8) already recognize `typing.TYPE_CHECKING` and do not flag
   `TYPE_CHECKING`-guarded imports as unused.  An explicit `# noqa: F401` is
   harmless but adds noise — omit it.

2. **Adjust relative-import depth** inside the extracted module (it now lives
   in a different package). Update internal imports to point at their canonical
   locations from the new path.

3. **Handle circular-import risk.** When the extracted module needs to
   reference a type or function still defined in the parent module (e.g., an
   `isinstance` check against a class), use `TYPE_CHECKING`-guarded imports for
   type annotations, plus lazy inner-function imports for runtime
   `isinstance`/`issubclass` checks. This breaks the cycle at module-load time
   while keeping the check at call time.

   **Do not add `from __future__ import annotations` to a file that defines
   TypedDicts with `Required` or `NotRequired`.** PEP 563 defers annotations to
   strings, which silently breaks `TypedDict.__required_keys__`.  If the
   extracted module contains TypedDicts with `Required`/`NotRequired`, avoid the
   `__future__` import and use string-literal forward annotations on the
   *referenced types* instead — never on the `Required`/`NotRequired` wrapper.
   See "TypedDict Pitfalls" above for the full diagnosis.

4. **Clean orphaned imports from the old module.** After the extracted code
   is removed, scan the old module's imports. Delete every import line that
   was used only by the extracted code — keeping orphaned imports adds dead
   dependencies and misleads readers about what the old module still does.
   Verify with `python -c "import <old_module>"` after cleanup.

5. **Add a re-export alias at the old site (shim).** If call sites still
   import the extracted symbols from the old module, add a thin re-import.
   This alias may be permanent (the old module retains other content and the
   re-import is the clean delegation path) or temporary (a later slice
   migrates all consumers and deletes the alias). A temporary shim carries a
   dated `WORKAROUND(YYYY-MM-DD)` docstring recording the constraint and
   removal condition:

   ```python
   # WORKAROUND(2026-06-26): shim re-exports — <symbols> live in
   # <canonical_module> now, but consumers still import from here.
   # Constraint: shim deletion requires all consumers migrated first.
   # Removal: when no imports of these symbols from <old_module> remain.
   from .<canonical_module> import <symbols>
   ```

   When a `_`-prefixed internal helper was extracted to the canonical module
   but is still used by functions that remain in the old module, do not import
   it at module level in the shim. A module-level `from .<canonical> import
   _helper` pollutes the shim's public namespace with a private name. Import it
   lazily inside the consuming function body instead:

   ```python
   # WRONG — leaks private name into shim's module-level namespace:
   from .<canonical> import _internal_helper  # polluting

   # RIGHT — lazy import inside the function that needs it:
   def <old_module_function>(...):
       from .<canonical> import _internal_helper  # contained to the function body
       ...
   ```

   This matches the existing lazy-import pattern for heavy dependencies and
   keeps the shim's module-level namespace clean.

   When the shim is temporary, plan its deletion lifecycle before adding it:
   (a) identify every consumer category (source-internal, test, harness);
   (b) migrate them in dependency order — **test consumers first** (they
   should point at the defining module, not the shim), then source-internal,
   then harness scripts; (c) when zero consumers remain, delete the shim
   following the shim-deletion protocol in "Staged Package Migration."  Do
   not leave a temporary shim as permanent debt without a planned removal
   slice.

6. **Retarget test monkeypatches.** If tests monkeypatch extracted symbols
   through the old module, retarget them to the canonical module. Import the
   canonical module in the test and pass it as the first argument to
   `monkeypatch.setattr`. Do not leave monkeypatches wired through the shim
   when a canonical path exists — the shim is for unmigrated source consumers;
   monkeypatches should point at the defining module.

7. **Migrate consumers by category.** After the shim is in place and
   monkeypatches are retargeted, migrate remaining consumers to the canonical
   module. Migrate one category at a time and verify after each category:
   (a) source-internal consumers (`src/`), (b) test consumers (`tests/`),
   (c) harness scripts (`harness/`).  After migrating a category, grep for
   leftover imports of the old module path in that category — zero matches
   before moving to the next category.

8. **Clear `__pycache__`** for both the old module directory and every
   new module directory.  After a multi-target extraction (N new modules),
   sweep `__pycache__` for the old module name AND all N new module names
   (e.g., `find <pkg>/__pycache__ -name '<old_module>*' -delete` plus
   `find <pkg>/__pycache__ -name '<new_module_1>*' -delete` for each new
   module).  A stale `.pyc` for a new module name that predates the
   extraction can cause import-time errors or serve stale bytecode.

9. **Verify — staged gates:**
   - **Gate A0 (module name):** the canonical module's name describes the code
     being extracted now, not an aspirational future state.  Re-read the module's
     public symbols and its `__init__.py` docstring: do they match the name?  A
     quality-math + quality-bridge module named `projection/` fails this gate
     (the name implies camera→raster pipeline code that isn't there).  Rename
     the module before proceeding — the name is the public surface every future
     developer reads first.
   - **Gate A (module smoke):** `python -c "import <canonical_module>"` and
     `python -c "import <old_module>"` — both import cleanly, no cycles.
   - **Gate A+ (re-export completeness):** every symbol that was previously
     importable from the old module (both public and private if privates are
     consumed by known callers) is still importable from the old module path.
     Verify mechanically: `from <old_module> import <symbol>` for each symbol
     in the old module's pre-extraction `__all__` or export surface, plus any
     private symbols that known consumers import via module attribute access.
     This gate catches the most common extraction defect: a symbol moved to a
     new module but not wired through the re-export shim.
   - **Gate B (consumer audit):** grep for `from <old_module> import` in
     `src/`, `tests/`, and `harness/` — confirms migration status per category.
   - **Gate C (test baseline):** full test suite — must match the
     mechanically-captured pre-extraction baseline pass/fail/skip count
     exactly.  The baseline is the count from step -1, not the count claimed
     by the task description.  A discrepancy between the task's claimed count
     and the actual pre-extraction count is a stale-premise signal, not a
     blocker — but a discrepancy between the pre- and post-extraction counts
     IS a blocker.  If the task claimed 883 but the pre-extraction run showed
     881, the baseline is 881 — verify the post-extraction count matches 881,
     not 883.
   - **Gate D (import direction):** the new module must not depend on the old
     module for core logic (lazy runtime imports for isinstance guards are
     acceptable).  The old module may depend on the new module (canonical
     delegation direction).
   - **Gate E (monkeypatch retargeting complete):** grep test files for
     `monkeypatch.setattr.*<old_module>` referencing extracted symbols — zero.
   - **Gate F (shim lifecycle):** when all consumer categories are migrated,
     delete the shim (following the shim-deletion protocol), verify absence
     grep, re-run test suite to confirm baseline unchanged.
   - **Gate G (whitespace):** `git diff --check` clean.
   - **Gate H (cross-module duplication):** when extraction produces N ≥ 2 new
     modules, scan the new modules for private helpers or constants duplicated
     across module boundaries (same name, same body).  The extraction itself
     must not introduce new duplication, but pre-existing duplication that was
     previously invisible inside a single god-file is now structurally visible
     as cross-module duplication.  Flag each duplicated helper in the developer
     report under a "pre-existing duplication surfaced by extraction" note —
     these are consolidation candidates for a separate follow-up slice, not
     part of the current extraction.  Do not consolidate during the extraction
     slice (that would violate the pure-extract constraint).  The flag is the
     deliverable; consolidation is deferred.

The pure-extract constraint: no new business logic, no new defaults, no new
fields, no new helpers. Import-plumbing adjustments (`TYPE_CHECKING` guards,
lazy inner imports) are permitted and necessary for correctness. Relative
import-depth changes, consumer-import redirections, and orphaned-import
cleanup are part of the move.

**Developer report minimum for extraction tasks.** After completing an
extraction slice, the developer report must include:
(a) the mechanically-captured pre-extraction test baseline count and the
post-extraction test count (must match);
(b) `git diff --stat` against the prior commit so the reviewer can verify
the change is bounded to the claimed files;
(c) the list of symbols preserved in the re-export surface and confirmation
that each is importable from the old module path;
(d) the `__pycache__` sweep commands actually run, covering all old and new
module names;
(e) when extraction produced N ≥ 2 new modules, a "pre-existing duplication
surfaced by extraction" note listing any private helpers or constants that
now appear with identical name and body in multiple extracted modules (Gate H
above).  These are consolidation candidates, not extraction defects — flag
them, do not fix them.
These are verification-surface items — the reviewer cannot confirm gate
passage without them.

**Do not report estimated line counts.** The `git diff --stat` in (b) is the
canonical size signal.  If the report volunteers per-file line counts anyway
(e.g., "148 lines"), produce them from `wc -l`, never from manual estimation.
An estimated line count that is wrong forces the reviewer to re-measure
mechanically — it adds verification cost without adding information.  Report
only the items listed above; do not volunteer extra quantitative claims that
the reviewer must debunk.

### Multi-Target Extraction (1 God-Module → N Target Modules)

When a single god-module contains multiple independent bodies of logic that
each deserve their own module, the extraction is a sequence of single-target
extractions — one per target module, executed in dependency order.

**Dependency order:** Extract leaf modules first (modules with no internal
dependencies on other modules being extracted).  A common decomposition
pattern is `schema → load → validation`:
- `schema` depends on nothing internal outside the module being extracted;
  extract it first.
- `load` depends on `schema`; extract it second, importing from the already-
  extracted `schema` module.
- `validation` may depend on `schema` and `load`; extract it last.

**Each slice is self-contained.** A slice moves one target module's content
into its canonical file, cleans orphaned imports from the old module, adds a
shim if consumers remain, and migrates that slice's consumers.  The test suite
must pass after each slice before the next begins.  Do not extract two target
modules in one slice — per-slice audit precision (import inventory, import
graph, monkeypatch surface, nontouch scope) degrades as the change surface
grows.

**Old-module final state.** After all target modules are extracted, the old
module may still exist with residual content (e.g., re-exports of symbols now
defined elsewhere, or symbols that genuinely belong there).  This is normal —
extraction is complete when all *targeted* content is moved, not when the old
file is empty.  If the residual content is exclusively re-exports and those
re-exports have zero consumers, delete them (package-boundary narrowing).  If
they have consumers, keep them as permanent delegation aliases or plan a
separate migration slice.

Two common extraction patterns produce different re-export-surface locations:

- **God-module as re-export surface**: the original module retains core types
  and/or execution dispatch, and re-exports symbols from extracted private
  submodules.  Callers continue to `from <pkg>.<original_module> import <X>`
  unchanged.  The extracted submodules are underscore-prefixed (`_render.py`,
  `_validation.py`) and are not imported directly by external consumers.
- **Package `__init__.py` as re-export surface**: the old module was the sole
  source file in the package and also served as the public namespace.  After
  extraction, the `__init__.py` carries the re-exports (or the symbols moved
  there).  This is the pattern addressed below.

**`__init__.py` during multi-target extraction (package-as-namespace
pattern).** When a package transitions from a god-module to submodules and the
*package `__init__.py`* previously served as the public re-export surface, each
consumer should import from the canonical submodule path
(`from <pkg>.<submodule> import <symbol>`), not through the package namespace.
If the old `__init__.py` had blanket re-exports, remove them during the
extraction sequence — this is a package-boundary narrowing applied alongside
extraction, not a separate task.  A `__init__.py` with only a docstring is the
correct end state for this pattern.

When the god-module (not `__init__.py`) is the public surface, leave
`__init__.py` untouched unless it independently needs narrowing.  Do not
conflate the two surfaces — narrowing `__init__.py` when the god-module is the
actual import target produces zero benefit and risks breaking unrelated
consumers.

A new package's `__init__.py` docstring must describe actual import dependencies
and package content — not aspirational boundaries that the code doesn't yet
hold.  A docstring that claims "this package does NOT import X" when a submodule
does import X is a correctness defect.  Describe the package's real dependency
profile.  If a dependency direction is aspirational (you want it to be true but
it isn't yet), state what is true now and note the constraint: "<submodule>
imports <upstream_types> — pre-existing coupling, not new with this extraction."

**Private-module naming for extracted modules.** When extracting code into
modules that are implementation details of the package (not part of its public
import surface), use an underscore-prefixed module name: `_validation.py`,
`_render.py`, `_cache.py`.  This is the standard Python convention for "private
internal module — import at your own risk."  The package's public surface
(either `__init__.py` or the retained god-module) re-exports the symbols that
callers need; the underscore prefix signals that direct imports of the private
module are not part of the stable contract.

Private helpers extracted into a private module keep their `_` prefix
(e.g., `_require_non_empty_str`).  When a private helper is imported across a
module boundary by the re-export surface, the `_` prefix stays — it is still an
implementation detail, even though it now lives in a different file.  Do not
rename private helpers to drop the `_` prefix just because they crossed a file
boundary during extraction.

**Scaffolding overhead is expected.** Extracting a god-module into focused
submodules will increase total line count across files — each new module needs
its own imports, docstring, and `TYPE_CHECKING` block.  This overhead is
typically 10–30% of the extracted lines and is a one-time cost paid for
cohesion.  Line-count increase from scaffolding is not a reason to avoid
extraction.  Judge the result by single-reason-to-change quality, not by raw
line count.

### Rename With Frozen Keys

When a class or function name is misleading but its registry key, config key,
or harness string reference is a frozen public contract (used by batch specs,
sweep manifests, ablation manifests, or evidence packages), rename the symbol
while preserving the key:

1. **Rename the class** in its defining module. Update the module docstring to
   describe the actual algorithm. Add a class docstring with a dated
   `WORKAROUND(YYYY-MM-DD)` note: state which key is retained, why it is
   misleading, and the removal condition (e.g., "remove when <component> is
   upgraded to <target_behavior>").

2. **Preserve the registry key** via an import alias in the registry module:
   `from .module import NewName as FrozenAlias`. The registry dict entry keeps
   the frozen string key and resolves to the aliased class. Harness code that
   references the key via string-based specs (e.g.,
   `<spec_class>(name="frozen_key")`) is unaffected.

3. **Update all call sites that reference the class directly**: constructor
   calls in tests, direct imports in source code, type annotations. Do not
   rename test functions that are named after the config key (not the class) —
   they test config-key behavior and should keep their names.

4. **Verify the frozen-key contract**:
   - `<build_scheduler>("frozen_key")` returns an instance of the renamed class;
   - scheduler name enumeration output is unchanged;
   - harness entry points that reference the key still work;
   - ablation aliases that resolve to the same class are untouched;
   - figure generators and evidence manifests that reference the key are
     unaffected.

5. **Verify no stale old-class-name references**: grep `.py` files for the old
   class name. Documentation-only references (README, design notes) may remain
   as historical record but should not mislead about current behavior.

## Harness And Test Discipline

Harnesses serve paper goals, performance comparison, method screening, module
optimization, and experiment evaluation. Tests serve functional correctness,
interfaces, data formats, config parsing, metrics, export behavior, and basic
module interaction.

Keep harness and test responsibilities separate:

- harnesses should expose stable entry semantics, input protocols, metric
  names, raw artifacts, seeds, splits, config snapshots, and parseable outputs;
- harnesses should output raw, low-processed artifacts (per-example predictions,
  raw scores, timing traces, resource usage, intermediate decisions, error
  cases, log metadata, config snapshots, seeds, splits, metric values);
- aggregation, plotting, and paper-table generation belong to downstream
  analysis or paper-writing skills, not in harness core logic;
- tests should use small fixtures, toy inputs, and clear pass/fail assertions;
- each test should have one named behavioral responsibility;
- harness code should not become functional test code;
- test code should not become paper-performance evaluation.

When a harness grows, split support modules inside that harness's own
`harness/` subfolder before pushing special logic into shared layers. When
tests grow, split them in the existing test system's style.

Tests should follow the repository's existing test placement conventions. Do
not force a fixed `test/` directory unless that is the existing convention.

A harness should support the "modify module → run harness → read results →
modify again" loop through stable entry semantics, fixed input protocols,
parseable output formats, and clear metric definitions.

### Test Assertion Precision

Each assertion in a test should state the strongest correct condition the
fixture guarantees.  Weak assertions mask regressions; imprecise boundary
comments mislead future debuggers.

**Use the strongest correct logical connective.** When two conditions are both
known true for the fixture, assert both independently — do not use `or` when
`and` holds.  An `or` that passes vacuously when one side is true will silently
stop checking the other side after a regression breaks it.

**Boundary-condition assertions and comments must be precise.** When a test
asserts eligibility at a boundary (e.g., frame N is within horizon H), verify
the inequality is the correct one (`<=` vs `<`, `>=` vs `>`).  A comment that
says "frame 3 beyond horizon-1" when the actual condition is `3 <= 2+1` (frame
is at the boundary, not beyond it) misleads the reader about what the test
verifies.  Match the comment to the actual inequality.

**Assert the mechanism, not just the outcome.** Beyond asserting that the
scheduler does not all-drop, assert the specific mechanism that enables it:
the right candidates pass the eligibility filter, the right rejection reasons
fire, the budget is sufficient for the selected candidates.  An outcome-only
assertion ("at least one selected") passes even if the selection path is wrong
for an unintended reason; a mechanism assertion catches a regression that
selects by a different path.

**Boundary stress in regression tests.** When the fix corrects a boundary
condition (e.g., a filter cutoff), include at least one assertion at each side
of the boundary: the just-inside-the-window case and the just-outside case.
This confirms the fix shifts the boundary to the correct coordinate, not that
it simply disabled the filter.

**Test fixtures must exercise real-data label paths.** When a centralized
classification function accepts multiple representations (e.g., ``"<synthetic_label>"``,
``<real_label_format>``, and ``metadata["<classify_field>"] == 0`` all mean
"base layer"), tests that only exercise the synthetic label
(e.g., ``layer="<synthetic_label>"``) pass vacuously — they never touch the
code path that real data uses.  This is the most common cause of regression-fix
gaps: the tests pass because they use the label the developer wrote, not the
label the data produces.  After a fix that broadens a predicate to accept
real-data labels, add at least one test fixture that uses the real-data label
shape that triggered the original bug, and assert the predicate recognizes it.
Do not re-test only the synthetic label
that was already covered by pre-existing fixtures.

**No vacuous catch-all tests.** A test whose body catches all expected
exception types (e.g., ``try: ... except (FileNotFoundError, SystemExit): pass``)
and asserts nothing is a correctness defect — it passes identically on success
and failure, and its pass/fail status carries zero information about the code
under test.  Delete such tests.  When testing CLI ``main()`` or other code that
may raise, assert at least one concrete output property: stdout text, return
code, a side-effect on the filesystem, or a specific exception type raised for
a specific error condition.  A test that catches both ``FileNotFoundError`` and
``SystemExit`` without asserting anything is vacuous — it cannot distinguish
"code ran correctly and exited" from "code crashed with a different exception
that the except clause didn't name."  Do not write them; review them as
``delete:`` findings.

### Test Environment Isolation From Installed Packages

When a test creates mock or fake modules that collide with the same package
name installed in the venv (e.g., testing a preflight check that imports
``<pkg>.<sub>.<module>`` when ``<pkg>`` is already installed), Python's import
machinery can silently resolve to the installed copy.  The test then passes
vacuously — the assertion succeeds but the mock module was never exercised.

Two mechanisms combine to cause this:

1. **``sys.path`` ordering**: the installed package's site-packages entry
   usually appears before runtime paths that are appended.  Python searches
   ``sys.path`` in order and finds the installed package first.
2. **``sys.modules`` caching**: even when ``sys.path`` is reordered, parent
   packages (``<pkg>``, ``<pkg>.<sub>``) cached in ``sys.modules`` from a
   prior import can short-circuit the import machinery.

The fix is a **double-clear**: strip the offending site-packages entry from
``sys.path`` **and** evict all keys for that package and its submodules from
``sys.modules``.  Use the pytest ``monkeypatch`` fixture so state is
auto-restored at teardown:

.. code:: python

    def _isolate_from_installed_<pkg>(monkeypatch: pytest.MonkeyPatch) -> None:
        # 1. Remove only the site-packages entry that contains the installed
        #    package — leave other entries (stdlib, src/) intact.
        entries = [p for p in sys.path
                   if Path(p).is_dir() and (Path(p) / "<pkg>" / "__init__.py").exists()]
        if entries:
            monkeypatch.setattr(sys, "path", [p for p in sys.path if p not in entries])

        # 2. Evict the package and all its submodules from sys.modules so
        #    stale parent-package caches don't short-circuit the fake source.
        for key in list(sys.modules):
            if key == "<pkg>" or key.startswith("<pkg>."):
                monkeypatch.delitem(sys.modules, key, raising=False)

Apply this pattern only to tests that genuinely create fake package modules
that collide with installed packages.  Do not strip site-packages globally or
for tests that don't need it — the isolation should be as narrow as the
collision surface.

Always verify the fix produces the **right reason**: after isolation, the test
that expects errors (missing executables, missing modules) genuinely reads the
fake module and fails for the intended reason, and the sibling test that
expects success genuinely reads the fake module's real tool paths.

## Framework Docs

Maintain framework docs (`FRAMEWORK.md` and `FRAMEWORK.zh-CN.md`) only when
docs are in scope or the accepted change would leave a documented surface
materially misleading. Keep docs about current reality, not template
initialization or aspirational status.

`FRAMEWORK.md` uses English; `FRAMEWORK.zh-CN.md` uses Chinese with English
module names, harness names, test names, method names, metrics, commands,
config keys, and code identifiers preserved.

Framework docs should explain where future local changes should happen:

- stable boundaries and extension points;
- change map from feature type to module, harness, test, or export area;
- harness purposes, metrics, and raw artifacts;
- test organization actually used by the repository;
- raw-first export approach and downstream analysis boundary;
- complex-function decomposition into sub-modules and how this supports high
  cohesion and local modification;
- framework risks where future changes cannot yet stay local.

Queue a docs sync when the current change materially alters module boundaries,
extension points, harness/test organization, artifact schemas, or the
decomposition of a complex function into sub-modules — structural changes that
would leave a documented surface misleading to the next developer.  Do not queue
docs sync for narrowly-local edits (single-function bugfix, variable rename) or
for changes whose scope is fully captured by existing docs.

## Naming, State, And References

Names must reflect real meaning and data shape. Do not keep historical,
placeholder, or overgeneral names after the concept changes.

**Type annotations must match runtime behavior.**  A type annotation is a claim
about what the code accepts and produces.  A ``Literal["a", "b"]`` that only
works for ``"a"`` (``"b"`` raises ``NotImplementedError``) is a lying type — the
annotation claims two valid values but only one is implemented.  A ``Sequence``
annotation on a parameter that only works with ``list`` is a lying type.  Match
the annotation to the implemented surface.  Add the wider annotation in the same
change that implements the missing variant — never annotate ahead of
implementation.

Use content names for content and reference names for paths, handles, IDs,
URLs, or external resources. Do not let a variable named like a reference carry
loaded content, or a content name carry a location.

Rename atomically across the full chain. For research-code renames, inventory
these surfaces before editing:

- **Registry or factory keys**: may be frozen public contracts used by batch
  specs, sweep manifests, or harness string references — preserve them via
  import aliases when the key is a stable contract (rename-with-frozen-key
  protocol);
- **Harness references**: harness code often references symbols by string key
  (e.g., spec objects with `name="<key>"`), not by class import — these are
  typically unaffected by a class rename but must be verified;
- **Ablation aliases**: short-name registry entries that resolve to the same
  class — do not rename these keys;
- **Figure generators and evidence manifests**: these may reference symbols by
  name in dicts, style maps, or manifest entries;
- **Test imports and constructor calls**: update all class-name references;
- **Test function names**: tests named after config-key behavior (not the class)
  should keep their names unchanged;
- **Source call sites**: all `import`, `from ... import`, and constructor
  references;
- **Docs**: README, FRAMEWORK.md, design notes — update if in scope;
- **Artifact metadata**: `metadata={"algorithm": "key_name"}` fields inside the
  class may use the frozen key and should stay unchanged.

Do not leave old-concept residue in any surface.

Names should be as short as possible while remaining semantically complete.
Delete prefixes, suffixes, and wrapper words that add no information.

Names in evidence-facing surfaces (figure legends, chart titles, table headers,
CSV column names) are claims to readers. A misleading name in these surfaces is
a correctness defect. An aspirational name (naming something for what you hope
it will become) is disallowed in evidence surfaces — describe the experiment
actually run, not the experiment you plan to run after upgrading.

Aspirational naming is also disallowed for new packages and modules created
during refactoring. A package or module name must describe the code that is
being placed there now, not code that will land there in a future slice.
Naming a quality-math package `projection/` because it will someday hold a
camera→raster pipeline creates a misleading surface: future developers looking
for projection code will find PSNR/SSIM math instead. Name the package for the
extracted content's actual semantics. If the content will change substantially
in a planned later slice, rename the package then — not now.

Place each variable, state object, config, and data structure at the layer that
actually owns it. Local intermediate content should stay local. Only stable
cross-boundary data should enter shared structures.

When outer orchestration owns saving, archiving, or exporting, inner business
logic should return values rather than also writing files. Write, save, export,
and return responsibilities should be single-owner.

Code order should help the reader follow the flow. When execution order is
clear, arrange code in that order. Keep related code physically close. Keep
field order, parameter order, and definition order consistent across
semantically corresponding structures.

## Prompts And Comments

If repository code includes prompts, task instructions, or embedded agent text,
write them as direct task instructions — short, clear, task-oriented. Do not
use role-playing openings. Clearly distinguish external references from direct
content and state who returns, saves, or exports each output.

Use code comments sparingly. Comments should explain non-obvious decisions,
constraints, provenance, or special cases. If clearer names or structure make a
comment unnecessary, simplify the code instead.

Do not write skill rules, debugging process, generation process, or style
analysis into code comments. Do not explain what the code does when the code
already says it through naming and structure.

Merge adjacent comments that annotate the same code block. Two comment blocks
separated only by whitespace can drift apart during later edits; a single merged
block stays consistent.

When a file contains multiple related-but-distinct issues (e.g., two separate
aliasing bugs with different root causes), keep each explanation scoped to the
fix it describes.  A WORKAROUND block at the top of a module that describes
only aliasing issue A should state explicitly that it does not cover aliasing
issue B (fixed elsewhere in the file), or should be updated to reference both
when the second fix lands.  Do not let a reader encounter a WORKAROUND block
describing issue A, then scroll to fix B and assume the WORKAROUND explains it.

For intentional, dated debt that has a known removal condition, use a
WORKAROUND docstring comment on the affected class or function:

```python
# WORKAROUND(2026-06-26): registry key "old_misleading_key" is retained for
# batch-spec / sweep artifact compatibility.  Remove when <canonical_component>
# is upgraded to <target_behavior>.
```

A WORKAROUND annotation records (a) the date the debt was accepted, (b) what
constraint forces the debt, and (c) the precise removal condition.  This is
distinct from a TODO — a WORKAROUND is intentional and stable until its removal
condition is met, while a TODO is aspirational and may never be addressed.

## Open-Source Reuse

When the task needs mature existing functionality, first decide whether
reuse is better than custom implementation. Reuse preference:

1. direct dependency with stable packaging and compatible license;
2. adapter around a stable API;
3. small copied or ported snippet when license permits;
4. custom implementation when reuse would add more cost than value.

Before copying or porting external code, check license compatibility. Code
without a clear license or with an incompatible license may be read for design
reference but not copied.

Preserve required notices (copyright, license) near copied or ported code. Add
a source comment including: original project name, repository URL, original
file or module, original license, reference commit/tag/version, reuse method
(direct copy / adapted from / ported from), and main changes made.

When the repository accumulates copied external code, maintain a
`THIRD_PARTY.md` or equivalent that centrally records external sources,
licenses, and modification summaries.

Reused code should make the current framework cleaner and more reliable — not
add extra configuration, over-abstraction, or caller burden.

## Deep Research

Use deep research when the current task involves unfamiliar language
conventions, framework organization, harness/test practice, open-source reuse,
or ecosystem-specific style. Use it to learn transferable patterns, not to copy
a public repository's structure mechanically.

Reference high-quality, well-maintained, clearly-licensed public codebases that
are close to the current task domain. Study their file granularity, module
decomposition, harness organization, and test layout — not to replicate their
structure, but to inform better local decisions.

If the current repository already has clear conventions, prefer the local style
and improve it only when a concrete readability, locality, or testability
problem appears.

## Code Review

When reviewing code, prioritize checks for unnecessary abstraction, wrong-layer
ownership, imprecise naming, unstable state, inconsistent ordering, unclear
data flow, overweight files, confused module boundaries, and poor change
locality.

Review suggestions should preferentially point toward deletion, inlining,
moving to use site, unifying names, aligning order, splitting responsibilities,
and clarifying boundaries. Do not default to suggesting more abstraction, more
config layers, more wrappers, or more defensive processing.

**Categorize every finding.** Every reviewer finding should carry one of three
tags so the developer can triage immediately without re-reading the surrounding
prose:

- ``delete:`` — unused code to remove (unused import, dead variable, vacuous
  test, redundant local import, dead config flag).  State what replaces it
  (often "nothing").
- ``change:`` — logic or structure to alter (wrong boundary, imprecise name,
  misplaced ownership, poor data flow, over-abstraction).  State the direction
  of the change.
- ``add:`` — missing coverage or documentation (untested code path, missing
  assertion, missing error-case test, stale framework doc).  State the minimum
  addition needed.

A finding without a tag forces the developer to guess whether you want deletion
or a rewrite.  Use the tag even for one-line findings.  Group findings by tag
so the developer's cleanup path is clear: all ``delete:`` items are mechanical
removal; all ``change:`` items are substantive edits; all ``add:`` items are
new coverage.

If code is already direct enough, do not suggest extracting another layer "for
cleanliness."

If a variable belongs to the wrong layer, suggest moving it to its true owner —
not wrapping it in a new type or adapter.

If content and reference semantics are mixed, require the distinction to be
made through naming and data flow.

If temporary state is modeled as long-lived state, suggest making it a stable
concept or moving it back to the local flow.

If obsolete concepts linger in names, text, config, or interfaces, require
cleanup and contract unification.

If a feature change touches multiple unrelated modules, flag the coupling risk
and suggest a clearer local boundary.

If redundant conditional branches exist (two arms doing the same operation),
flag them with ``change: merge identical arms``.

If a ``NotImplementedError`` appears in a code path reachable through the public
interface (CLI, enum, ``Literal``, registry), flag it with ``delete: dead
future-proofing`` — the interface claims a capability the code does not have.

When reviewing a defensive-copy fix (``copy.deepcopy``, ``.clone()``,
``.detach()``), verify: (a) the docstring or comment traces the full aliasing
chain — which assignment established the alias, which mutation corrupts it,
which call site observes the corruption; (b) each alternative (``.clone()``,
``.detach()``, non-mutating API, parameter replacement) was considered and
shown infeasible; (c) the round-trip test confirms the source object survives
the mutating call un-corrupted, not just that the copy is correct.  A
``deepcopy`` call with a comment that says only "workaround" or "avoid
aliasing" without the full chain is flagged as ``change: document the
aliasing chain`` — the next developer needs the chain to avoid reintroducing
the bug, not just the fix location.

If a WORKAROUND block in a file describes only one of multiple aliasing issues
but sits in a shared header or near a different fix, flag it with ``change:
scope WORKAROUND to its actual fix`` or ``add: note which aliasing issue this
WORKAROUND addresses``.

If an ``__init__.py`` is empty (0 bytes) for a package with external callers,
flag it with ``change: re-export public API from __init__.py`` — callers should
not depend on internal submodule paths.

If a type annotation (``Literal``, ``Sequence``, etc.) claims wider acceptance
than the code implements, flag it with ``change: match annotation to implemented
surface`` — a type annotation that lies is a correctness defect.

**Before reviewing any code, verify the task's deliverable completeness against
its Boundaries and Reviewer Focus.** A task that requires both a code change AND
evidence/behavioral verification has not been satisfied by the code change alone.
Check: (a) are all required deliverables present (code, tests, evidence re-run,
status-file updates)? (b) if the task says "verify X > 0" or "confirm Y is
non-degenerate," does the developer report show the actual measured values? (c)
if the developer reported "blocked on GPU" or similar infrastructure gap, was
the task classified as BLOCKED rather than DONE?  A code review that accepts
clean code without checking whether the task's acceptance criteria were met
creates an evidence-integrity gap that is much harder to detect later.

When an O(n·m) membership check against a short sequence is harmless (e.g.,
``sys.path`` with ~15 entries), do not block on it — flag it only if the
collections are unbounded or the quadratic cost is measurable.  A ``set``
guard is a one-line improvement but never a correctness issue for small N.

When evicting keys from ``sys.modules`` via ``monkeypatch.delitem``, always
pass ``raising=False`` — the key may already be absent if the module was never
loaded, and the default ``raising=True`` aborts the test on a missing key.
Iterate over a snapshot of keys (``list(sys.modules)``) to avoid mutating the
dict during iteration.

## Validation

Run the validation command the user requested. Run it literally from the
repository root unless the user gave another working directory. Do not
substitute a broader suite, omit arguments, or add environment variables.

Before reporting success, run the repository's whitespace check (e.g. `git diff
--check`). Treat trailing whitespace, conflict markers, and blank-line-at-EOF
warnings as blockers.

Before reporting a quantitative claim (a count, a line length, a file list
produced by grep), verify it with the broadest plausible search.  If you claim
"N occurrences of pattern P across K files," search the equivalent forms of P
that a different author might have used (e.g., `Mapping[str, Any]`, `dict[str,
Any]`, and `Dict[str, Any]` are the same type annotation written three ways).
A claim that holds only for the narrowest pattern is misleading — report the
aggregate count across all equivalent forms, or state explicitly which form you
matched and why the others are excluded.

After import-path changes (file moves, boundary narrowing, or code extraction),
run `python -c "import <package>"` against every affected package as a minimum
smoke test before running the full test suite.

After validation, remove only generated cache/build/test artifacts created by
the run. Do not clean unrelated dirty or untracked user work.

When a verification task discovers a pre-existing defect that predates the
current task scope, do not fix it. Document it in memory files as deferred
reconciliation work. Task-induced defects are blocking and must be fixed before
acceptance.

**Cross-environment verification.** When the task Boundaries explicitly flag a
multi-environment risk (\"verify on the conda/torch 2.5.1 env,\" \"dual-venv,\"
\"may behave differently on GPU vs CPU\"), the fix must be verified on each
named environment before completion.  An environment passed in the task's
Boundaries is part of the acceptance contract — a fix verified on only one
environment when the task names two is incomplete.  If one of the named
environments is unavailable, the task is BLOCKED — report which environment is
missing and the commands to run when it becomes available.  Do not silently
substitute a different environment and report DONE.

**Aliasing-specific round-trip verification.** For fixes that introduce a
defensive copy to break an aliasing chain, verify mechanically: (a) the copy
source is unchanged after the mutating call runs — check structural integrity
(NaN, Inf, shape, parameter count) on the original object; (b) the copy and
source are independent (mutating one after the copy does not affect the
other); (c) downstream consumers that depend on the original's un-mutated
state produce correct output.  A test that only checks the copy is correct
without verifying the source survived is incomplete — the aliasing chain
corrupts the source, and if the copy is somehow the same object (shallow copy
error, `.detach()` on a non-leaf), the source is still corrupted.

**Before reporting completion,** verify every deliverable category extracted
from the task's Boundaries: code deliverables (artifact exists), behavioral
demonstration deliverables (delta confirmed), and execution/evidence deliverables
(re-run completed, evidence row non-degenerate).  A task that landed correct code
but skipped the required evidence re-run is incomplete.  The final report must
state the re-run outcome and the new evidence-table values — not a forward
reference to a "next step."

## Readability Audit

After edits, audit:

- names match real meaning and data shape; **after a behavior-change refactor,
  every name in the changed surface was re-verified against the new behavior** —
  a class or function that changed from heuristic to optimal, greedy to DP, or
  approximate to exact must not keep the pre-change descriptor in its name;
  misleading names that propagate into registry keys, harness output, or evidence
  manifests are correctness defects, not style preferences;
- data flow is direct and naturally ordered;
- functions, files, and modules have clear single responsibilities;
- abstractions reduce real complexity rather than add jumps or boilerplate;
  **no scattered literal string comparisons duplicate an existing centralized
  classification function** — domain predicates delegate to the centralized
  function, not to ad-hoc string matching;
- no avoidable global state, hidden paths, repeated registration points, or
  heavy config burden were added;
- the change stayed local to the natural owner;
- after restructuring, the import graph has no incidental backflow — verify
  that package dependencies point the intended direction and no cycle was
  introduced; **no new import violates a layered-architecture import-direction
  constraint** (e.g., a lower layer importing from a higher layer it must not
  depend on) — verify with `grep` against the architecture spec or task
  Boundaries;
- no over-splitting into thin wrappers, empty-shell files, single-use
  abstraction layers, or fragmented modules;
- **no redundant conditional branches** — no ``if``/``elif``/``else`` or
  ``match``/``case`` with two or more arms that perform the same operation;
  identical arms were merged;
- harness and test responsibilities remain separate;
- artifact schemas, exporters, docs, and tests agree when any changed;
- framework docs were updated or confirmed current when in scope;
- tests follow the existing test layout (not a forced `test/` directory);
- external reused code has compatible license and attribution;
- explicit allowed-file scope was preserved and explicitly excluded files or
  modules were not modified;
- excluded capabilities are absent from source, tests, docs, and untracked
  files, with no explanatory stubs or placeholders left behind;
- stale `__pycache__` directories for deleted or moved modules were swept;
- **unused imports** were not left in — every import in every changed file is
  actually used by the file's remaining code; orphaned imports that serviced
  extracted or deleted code were removed;
- **no redundant function-local imports** duplicate module-level imports —
  symbols already imported at module level in the same file are not re-imported
  inside function bodies (with or without alias); a function-local import is
  only justified when the symbol is not available at module level AND the import
  is expensive or creates a circular-import risk;
- **no vacuous catch-all tests** — no test catches all expected exception types
  and asserts nothing; every test asserts at least one concrete output property
  (value, exception type, side-effect, return code);
- **dead config** was not left in — any config parameter that no code path
  reads is dead config; remove it;
- **dead parameters** were not left in — any parameter whose accepted value
  range does not produce observably different behavior is a dead parameter;
- **no dead future-proofing placeholders** — no CLI options, enum values,
  ``Literal`` members, or code branches that raise ``NotImplementedError``;
  the interface surface matches the implemented surface;
- **no function-local imports without justification** — imports are at module
  level unless the import is expensive+cold-path, avoids a circular import, or
  is an optional dependency; stdlib modules (``copy``, ``os``, ``json``, etc.)
  have no plausible justification for function-body placement;
- **package ``__init__.py`` exposes the public API** — when a package has
  external callers, its ``__init__.py`` re-exports the symbols callers need;
  an empty ``__init__.py`` (0 bytes) for a package with external consumers is
  a coupling defect;
- **type annotations match runtime behavior** — no ``Literal`` member that
  raises ``NotImplementedError``; no annotation that claims wider acceptance
  than the code implements;
- **behavior-change claims are verified end-to-end** — when the task claims to
  fix a behavioral gap (e.g., "makes X observable to Y," "metric changes when
  <algorithm> is toggled"), trace the complete data flow from the changed input through every
  intermediate step to the observable output.  Verify no data is computed in one
  function but never consumed by the downstream consumer that the task claims to
  have rewired.  Verify the new data flow is active in all dispatch branches
  (not just the happy path).  If the task requested a specific test
  demonstrating the behavior change, verify the test exists and the delta
  assertion is numerically concrete (not a pass-through of identical values);
- **regression-fix tests assert for the right reason** — when a test was
  passing vacuously because an environmental override (installed package,
  ambient config, cached state) masked the code path it intended to exercise,
  verify the fix genuinely eliminates the override.  The isolated test must
  exercise the mock/fake module, not the installed copy, and the sibling
  positive-case test must also read the fake module (not silently fall back to
  the installed copy); **new tests for a predicate fix exercise real-data label
  paths** — at least one test fixture uses the real-data label shape that
  triggered the original bug, not only the synthetic label already covered by
  pre-existing fixtures;
- **structural proximity ≠ complete data flow** — a module that lives in the
  right package and is imported by the right consumer does not automatically
  mean the data flows correctly.  Verify that the downstream consumer actually
  reads the field the upstream code sets, that the field name matches across the
  boundary, and that no intermediate transformation silently drops the value;
- adjacent comments and working annotations were merged when they annotate
  the same code block;
- after code extraction, monkeypatch targets in tests point at the canonical
  module, not at the old-module shim (the shim is for unmigrated source
  consumers; monkeypatches should use the defining module);
- after code extraction, the old module has no orphaned imports — every
  import the old module still carries is used by its remaining code (verify
  with `python -c "import <old_module>"` after removing extracted code);
- **TypedDict `__required_keys__` is non-empty** — when a file defines
  TypedDicts with `Required` keys, verify at runtime that
  `__required_keys__` contains the declared required keys (an empty
  frozenset means `from __future__ import annotations` or string
  annotations are breaking resolution).  TypedDict `Required` docstrings
  and comments correctly attribute runtime enforcement to the loader
  function, not to the annotation;
- **aliasing chains are documented end-to-end** — defensive copies carry a
  comment or docstring tracing the full identity chain (which assignment
  established the alias, which mutation corrupts it, at which call site the
  corruption becomes observable) and stating why the copy is the only viable
  isolation (alternatives infeasible, shape mismatch, dependency cannot be
  changed); a WORKAROUND block near an aliasing fix describes that fix's
  aliasing chain, not a different aliasing issue elsewhere in the file;
- **old-concept residue** was cleaned from names, text, config, and interfaces;
- **frozen keys preserved** — after a class or function rename, registry keys,
  config keys, and harness string references that are public contracts still
  resolve correctly (verify via builder lookup, name enumeration output, and
  harness smoke);
- updated memory/trajectory files are intra-file consistent: every header
  counter matches every inline enumeration, and the files exist on disk at the
  concrete paths resolved from the task Context (not at a default or assumed
  location);
- **task deliverable completeness** — every deliverable category extracted from
  the task's Boundaries during pre-edit inventory was satisfied:
  (a) code deliverables exist and pass;
  (b) behavioral demonstration deliverables show the concrete delta;
  (c) execution/evidence deliverables completed and the evidence row is
  non-degenerate.  A code fix whose required evidence re-run was not executed
  is incomplete, regardless of code quality;
- **metadata-surface accuracy** — any code comment, docstring, or metadata
  string that asserts factual claims about on-disk state (scene lists, directory
  existence, data availability, scheduler counts, artifact format) was verified
  against the filesystem.  Count-to-list consistency was checked: the numeric
  claim matches the number of items in the parenthesized enumeration.  Aggregate
  arithmetic (X categories × Y items = Z total) was recomputed from the actual
  enumeration.  Stale docstrings describing pre-refactor state were updated;

For execution or hybrid tasks, also audit all items in the
"Post-execution verification checklist" above, plus these additional checks:

- **stale cached outputs and prior-run batch artifacts were cleared before
  re-execution** — any batch cache, derived evidence, or workspace cache that
  could serve pre-fix data was identified and deleted; the batch directory
  contains no artifacts from prior runs with different enumerations;
- **fresh timestamps confirm the re-run actually happened** — artifact
  modification times are after the code fix, not before;
- **verification-criterion/schema mapping is explicit** — when the task's
  verification criterion uses schema terminology that differs from the
  framework's actual output format, the mapping was stated explicitly in the
  verification report and the reviewer can trace it;
- **named component was actually invoked** — when the task says "run experiment
  X via component Y" or "execute Z through W," the process output, logs, or
  execution trace confirms that Y/W were called and produced output.  A report
  that claims completion without invoking the named component is a category error
  — a code-writing deliverable cannot substitute for an execution deliverable.
  If component Y could not be invoked (environment mismatch, missing dependency,
  broken import), the task is BLOCKED, not DONE;
- **named data source was actually read** — when the task specifies a particular
  data source (e.g., "use `<refinement_dir>/` as refinement source," "pull from
  `<specific_dir>/`"), the execution trace or component logs confirm that source
  was opened/read, not silently substituted with a different directory or a
  default fallback.  A run that used a different source produced data from the
  wrong provenance;
- **the task did not silently morph into a different task type** — when the task
  is classified as execution but the developer produced new code (summarizer,
  aggregator, figure generator) instead of invoking the named component, the
  work delivered is a different task than what was requested.  This is a
  task-substitution error, not a completion — the code may be well-formed but it
  does not satisfy the execution contract.  If the downstream analysis code
  genuinely didn't exist and is a prerequisite, report it as a prerequisite gap,
  not as the completed task.

For skill edits, also perform a **project leakage audit**. Remove or generalize
any real project path, symbol, dataset, method, metric, harness, test, artifact
field, or one-off debug lesson that does not hold across repositories.

## Final Response

Keep the final response concise: changed paths, behavior or contract covered,
validation performed, and caveats that affect the user's next action.

For a pure verification pass where no new edits are needed, describe the checks
performed and their results, and state "no new changes made" or "prior work
confirmed intact on disk."

When a task's stated premises are stale (the work it describes as pending is
already done), the response should report: what the task claimed, what the
actual state is, which verification steps confirmed the existing state is
correct, and that the stated blocker no longer applies. Do not redo, re-commit,
or re-create already-existing work.

When a hybrid task's Phase 2 (evidence re-run) is blocked by missing
infrastructure, do NOT report DONE.  Report BLOCKED with: the infrastructure
gap, the commands to run when infrastructure becomes available, and the Phase 1
code/test status.  A "blocked on GPU — to verify end-to-end: [steps]" report
that the developer or reviewer treats as DONE is an evidence-integrity failure.

After completing a hybrid task (code fix + evidence re-run), the completion
report must include the before/after evidence-table values for every
acceptance-criteria metric.  When the task's Context or Boundaries reference
specific status/memory files (e.g., `current_status.md`), verify those files
have been updated to reflect the resolved state — a stale status file that
still lists the blocker as open is a documentation defect.

Do not explain skill internals, tool mechanics, or style theory unless the user
asked for a skill optimizer report.

## Report-Versus-Reality Gate

**Developers must apply this gate to their own reports before submitting.**
This is not only a reviewer tool — it is a mandatory pre-submission self-check.
A developer who reports completion without mechanically verifying the claims
below is producing a claim, not a verified fact.  The reviewer will check these
mechanically; the developer should find the mismatch first.

A developer report that describes code changes, evidence state, or behavioral
properties is a claim about file state, data, or behavior.  Before accepting the
report, verify the claim against reality mechanically — not from memory,
expectation, or design reasoning.

- **Code claims.** A report that says "X lines changed in Y files" must survive
  `git diff --stat`: the actual diff against the last commit should show changes
  in the claimed files with the claimed shape.  If the tree is clean or the
  claimed symbols are absent, the report is false.  A report that says "N
  schedulers added to registry" must survive a mechanical lookup:
  ``len(<registry_dict>)`` should match the claimed count, and the claimed
  names should appear in the registry keys.
- **Evidence claims.** A report that says "0 failures" or "data_gaps: {}" or
  "N evidence files" must survive mechanical inspection of the actual evidence
  file.  ``python -c`` the claimed field at the claimed path; count entries with
  ``grep`` or ``jq``.  A field that exists in one artifact but not in the claimed
  file is a false claim.  A failure count that collapses multiple categories into
  one number is a misleading claim.  Verify each claim against the bytes on disk.
- **Naming claims.** A report that says "no references to old name remain" must
  survive ``grep -rn "old_name"`` across the codebase — zero matches.  A report
  that says "class renamed" must survive ``grep`` for the old name.  Do not
  report a rename as complete when the old name still appears in source, tests,
  or docs.
- **Data-property claims.** A report that says "overlapping bars are a
  figure-generation issue" must survive data inspection: check the per-scene
  values.  If the data ranges are genuinely narrow, the artifact is a data
  property, not a rendering bug.  Do not attribute visual artifacts to rendering
  without first inspecting the underlying data.
- **Plan ≠ implementation.** A report that says "the plan is written at `<path>`"
  and then summarizes the plan as if it were implemented is describing intent, not
  state.  If zero files were modified, the work is not done — the plan describes
  what to build, not what was built.
- **Acceptance-criteria verification claims.** A report that says "Done" or
  "Complete" for a task whose Boundaries require behavioral/evidence verification
  (e.g., "verify `<metric> > 0`," "confirm `<scheduler>` is non-degenerate on
  `<scene_set>`,"
  "re-run harness and confirm `data_gaps: {}`") but provides only code changes and
  a forward-looking "to verify end-to-end: [steps]" is a progress checkpoint, not
  a completion claim.  The acceptance criteria require measured values, not a
  plan for future measurement.  If the required verification was not executed
  (regardless of reason), the task is incomplete.  If the verification was
  blocked by missing infrastructure, the task is BLOCKED — not DONE.
  A "blocked on GPU" report accepted as DONE is an evidence-integrity failure.
- **Component-invocation claims.** A report that says "C2 experiment complete"
  or "experiment X ran end-to-end" must survive a mechanical check that the
  named component was actually invoked.  If the task says "run X via component
  Y" and component Y does not appear in any process log, import trace, or
  execution output, the claim of completion is false — a different task was
  performed.  Check: does the process output mention Y?  Are output artifacts
  from Y present with timestamps after execution start?  Did the task's
  specified data source (e.g., `<refinement_dir>/`) appear in any file-open,
  read, or import log?  A "complete" claim where Y was never invoked is a
  task-substitution error — the developer built analysis code around Y instead
  of invoking Y.
- **Task-type fidelity.** A report that describes new code (summarizers,
  aggregators, figure generators) when the task's dominant verb was "run" or
  "execute" is describing a different task than what was requested.  New code
  is an implementation deliverable; fresh execution output is an execution
  deliverable.  They are not interchangeable.  If the report's primary
  evidence of completion is new files in `src/` rather than new or updated
  artifacts in `results/` or `output/`, verify that the task was actually an
  implementation task, not an execution task that was misclassified.

This applies equally to developer self-reports and reviewer verification.  A
false claim of completion that passes review creates an evidence-integrity gap
that is much harder to detect later than at the review surface.

## Metadata-Surface Verification

Code comments, docstrings, and metadata strings that assert factual claims about
on-disk data (which scenes have what directories, what data is available, which
scheduler exists, what artifact format is produced) are evidence-facing claims.
They must be verified against the filesystem before acceptance, just as code
correctness is verified against tests.

Common failure modes:

- **Scene classification errors.** A coverage note says "scene S has directory D"
  but `ls <scene>/D/` fails.  Guessing scene membership from memory is not
  verification; run the `ls` or `find` command.
- **Count-to-list mismatch.** A comment says "N scenes (a, b, c, ...)" but the
  parenthesized list contains M items where M ≠ N.  Count the listed items and
  verify they match the numeric claim.  A common cause: moving one item between
  groups but updating only one count, or editing the list without recounting.
- **Aggregate-count arithmetic errors.** A note says "X categories, Y items each,
  Z total" but X × Y ≠ Z.  Recompute the arithmetic from the actual enumeration.
- **Stale metadata after structural change.** A docstring describes a module's
  content or dependency profile as it was before a refactor.  After extraction,
  repointing, or boundary narrowing, verify the docstring still describes the
  module's actual content — not its pre-refactor state.

Before accepting any change that introduces or updates a metadata string with
factual claims, run the mechanical check: list the claimed items, count them,
and verify the count matches the numeric claim.  If a scene list is claimed, run
`ls` or `find` to confirm each scene's on-disk state matches the claim.
