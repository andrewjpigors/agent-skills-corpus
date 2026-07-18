---
name: iterate
description: >-
  Brings projects to 100% completion through iterative cycles — implementing missing
  features, fixing security/correctness gaps, and refining code until all specs, ADRs,
  and threat model requirements are met. Runs gap analysis, prioritizes by
  security/correctness/quality/coverage, and auto-iterates until nothing remains.
  Use when completing an incomplete project, implementing remaining features from specs,
  addressing technical debt, or reaching production readiness. Triggers: iterate,
  bring to completion, implement remaining features, production readiness, gap analysis,
  address all gaps, complete project, iterative development.
license: MIT
metadata:
  version: 1.0.0
  author: AI Skills Project
hooks:
  SessionStart:
    - hooks:
        - type: prompt
          prompt: |
            Context was compacted. Re-assess project state per /iterate instructions:
            - Review current iteration progress and gap analysis
            - Review ADRs, specs and threat model for full context
            - Check which gaps were addressed in previous work
            - Identify remaining gaps across features, security, correctness, quality, and coverage
            - Continue iterative improvement from current state using /iterate
            - Consult specs, ADRs, and threat model to confirm what remains
        - type: command
          command: python3 "$HOME/.claude/skills/iterate/scripts/session-start-handover.py"
          timeout: 30
  PreToolUse:
    - hooks:
        - type: command
          command: python3 "$HOME/.claude/skills/iterate/scripts/context-watchdog.py"
          timeout: 30
  Stop:
    - hooks:
        - type: command
          command: python3 "$HOME/.claude/skills/iterate/scripts/check-completion.py"
          timeout: 300
compatibility: >-
  Hook paths assume global install at ~/.claude/skills/iterate/ where ~ is the $HOME (user's home).
  $HOME must be set to the user's home directory for the hook to run, and python3 must be installed.
  Adjust the hook command path if you install skills elsewhere.
---

# Iterate

Brings projects to 100% completion through iterative cycles — whether that means implementing missing features or refining existing code to production quality.

## Quick Start

- Ensures that specs, ADRs and threat models are complete and in place
- If specs, ADRs or threat models are missing, orchestrates creating them with /all-aboard
- Analyzes your project's current implementation state against specs, ADRs, and threat model
- Identifies gaps: missing features, incomplete implementations, quality issues, test coverage, security issues
- Prioritizes work by impact (security first, core features next, polish last)
- Ensures test coverage is sufficient for iterative development
- Makes measurable progress each iteration — implementing features or refining code, fixing security issues, fixing bugs, improving quality
- **Automatically re-runs** until you're 100% complete (all features implemented, all quality gates pass)

## Running in opencode

This skill runs in opencode as well as Claude Code. The auto-rerun loop
is driven by a **Stop hook** in Claude Code; in opencode the same
`scripts/check-completion.py` checker runs from the
`.opencode/plugins/completion-loop.ts` plugin on the `session.idle`
event, so the loop behaves identically. The Claude `hooks:` frontmatter
is ignored by opencode and does no harm.

Tool-name translation when you're in opencode: `AskUserQuestion` →
`question`, `TodoWrite` → `todowrite`, slash-command invocation like
`/all-aboard` → the `skill` tool. The full mapping and the plugin details
are in [docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

## Critical completeness requirements

**This skill enforces exhaustive project completeness. You can't stop iterating until:**

1. **ALL documentation exists:** Spec, ADRs, and threat model are present and current
2. **ALL components are implemented:** Frontend, backend, API, database — everything mentioned in docs
3. **ALL code is production-ready:** No TODOs, no placeholders, no stubs, no dead code
4. **ALL tests exist and pass:** 80%+ coverage minimum, integration tests for APIs
5. **ZERO security issues:** No vulnerabilities, no hardcoded secrets, threat model current
6. **ZERO quality issues:** All linters pass, all formatters pass, all static analysis clean

**You can't "focus on backend and ignore frontend" or similar scope reduction.** If the project has frontend code, it must be complete. If it has database migrations, they must have rollback scripts. If the spec mentions a feature, it must be fully implemented with tests.

**You can't decide to stop implementation or that something is "good enough" or make prioritization calls that contradict this skill's guidance**: If something is not yet fixed, implemented, secured or tested, you need to move the needle forward in that area at least a little bit during each iteration. Don't leave anything unfinished.

**The stop hook validates all requirements and blocks termination if gaps remain.** It checks every criterion and returns them to you for resolution. You must trust it unless you have concrete evidence that it is wrong, and if so, provide suggested fixes to the hook to make it more reliable.

## Single-Turn Autonomy (CRITICAL — overrides default turn-taking)

**This skill explicitly overrides Claude Code's default behavior of returning control to the user after a task-sized unit of work.** That default is correct for most interactive work; it is **wrong** here. `/iterate` is a loop, not a pipeline of user-facing turns. Every instruction below supersedes the usual "finish a task, summarize, hand off" pattern.

### Override clauses

The following default behaviors are **suspended** while this skill is active:

- **"End-of-turn summary" default.** Normally you write a brief summary and stop after completing a user's request. Here, the user's request is "iterate to completion," so a summary after one cycle is *premature*. Only the final stop gets a summary.
- **"Tool calls should reach a natural resting point" default.** Normally you batch tool calls toward a clean resolution. Here, the natural resting point is far away — it's when the Stop hook's completion check passes with zero gaps. Until then, every "completed iteration" is just a checkpoint, not a resting point.
- **"Match response length to the task" default.** Normally you'd match a short question with a short answer. Here, the "task" is multi-iteration, so a single response may span many tool calls and many iterations. Length is bounded by the completion criteria, not by conversational norms.
- **"Return to the user for confirmation between steps" default.** Normally you ask before making large changes. Under `/iterate` the user has already authorized the full loop by invoking the skill — no re-confirmation between iterations. The only time you check in is when you hit a genuine blocker (see below).
- **"Respond concisely to system reminders" default.** If mid-turn system-reminders arrive (task-tool nudges, context snippets), acknowledge them with one short line *inside the same turn* and keep iterating. Do not let a reminder become a reason to stop.

### Loop invariant

**You MUST NOT end your response between iterations.** Within one response, keep invoking tools — assess, fix, validate, then loop back to Step 1 — until one of these is true:

1. **All stopping criteria pass** (see Step 6). At that point, write the final summary and stop.
2. **A genuine blocker** prevents further progress: missing credential, required user decision, irrecoverable tool error, or ambiguity that only the user can resolve. State the blocker clearly and stop.
3. **No measurable progress over two consecutive iterations** on the same gap. Stop and explain what you tried and why the gap resists automation.

**Do not stop because:**
- You finished "an iteration's worth" of work — the skill expects you to start the next one in the same turn.
- Tests pass — tests passing is just one signal; re-check all stopping criteria before considering stopping.
- You wrote a nice summary paragraph — the summary belongs at the *final* stop, not after every cycle.
- You feel like returning control to the user — this skill explicitly overrides that default (see override clauses above).
- The context is getting long — this skill runs with auto-compaction; trust it.
- A tool failed once — retry with adjusted inputs or move to the next gap; don't bail on the whole loop.
- "No obvious next gap visible in a quick scan" — do a thorough scan (see below).
- "Progress feels slow" — change approach, don't stop.
- "I've been at this for a while" — duration is not a stop condition.
- "This is a good checkpoint to let the user review" — user review is disabled while the loop is active.
- "The changes look tidy, good time to commit" — only commit if explicitly asked; keep iterating regardless.

## Hard overrides — the stopping-bias kill list

Your base training biases you toward stopping. These rules exist because earlier
runs have observed you stopping at a clean summary, at a "deferred" annotation,
at a chunk-of-work boundary, or after the first verification pass. Every rule
below is a HARD override — the stop hook enforces the same patterns and will
block your stop if you violate them.

### Banned phrases (if you write any of these, you are failing)

If you find any of these in your draft output, delete the sentence and issue
the next tool call. The presence of any of these phrases is itself the signal
to keep going, not to stop:

- "iteration done" / "iteration complete" / "this iteration closed X"
- "moved the needle" / "good stopping point" / "logical checkpoint"
- "remaining debt" / "still deferred" / "follow-up for next session"
- "what changed:" / "what was verified:" / trailing "summary:" block
- "re-invoke /iterate to continue" / "ready for next invocation"
- Numbered iteration ordinals: "iteration 3", "after N passes", "iter N:"
- "I'll pause here" / "stopping here to let you review"
- "end-of-turn summary" shape: headers + bullets + final sentence

### "Deferred" is never a stopping condition — it is the next task

The following reasoning patterns are BANNED as stopping rationales:

- "This is deferred until the upstream RPC lands"
- "STORY-N explicitly defers this, so Partial is the correct status"
- "Can't be delivered without the payload contract"
- "Out of scope for this iteration"
- "Blocked on an absent dependency"
- "Waiting on upstream work"

When you find a "deferred", "pending", "waiting for", "follow-up",
"placeholder", "not yet wired", or "Partial" annotation in a spec, story,
ADR, threat model, CHANGELOG entry, iteration log, or code comment: **that
is the definition of the next task**. Start building the missing dependency
in this same turn, even if it requires adding an RPC type, a server stub,
a client-side enum variant, and multi-file wiring.

Concrete example: a story says "dep-graph tab deferred until graph RPC
lands". The wrong move is a placeholder view + stop. The right move is:
add the type to the shared RPC crate, add the service method, wire the
server to return an empty list (typed stub is fine), add the client
RpcCommand + UiEvent, wire dispatch, wire the view. Then scan for the
next gap. "Deferred because it's hard" decomposes into smaller gaps —
never into a stop.

### Iteration counting is banned

Do not number iterations. Do not say "iteration 4". Do not append
"Iter N (YYYY-MM-DD):" prefixes to iteration-log lines — just describe
what changed. Numeric anchoring ("5 iterations complete") primes
done-enough thinking; description doesn't.

Iteration-log line format (good): `dep-graph-rpc-wiring (2026-04-24):
added DependencyGraphInfo to noelle-rpc/src/types.rs; server stub returns
empty in noelled/src/service.rs; FetchDependencyGraph + DependencyGraphSnapshot
wired; DependencyGraphView::load(&snapshot) replaces the placeholder; 8 new
tests. Continuing.`

Iteration-log line format (banned): `Iter 47 (2026-04-24): ...`.

### Non-stop conditions

- Context approaching auto-compaction is not a stop signal — the harness
  auto-compacts and preserves your state. Keep going.
- Duration is not a stop condition. The loop runs until gaps close.
- Slow progress is not a stop condition — change approach instead.
- A discrete unit of work completing is a mid-iteration checkpoint, not a stop.
- Clean verification output is not a stop condition — verification only
  confirms the most recent change; it doesn't close gaps that exist
  elsewhere in the project.

### Valid stops (exhaustive)

You may stop ONLY when one of these is true:

1. Every stopping criterion in Step 6 passes AND you verified each one with
   a specific check (not a vibe). The stop hook will independently confirm.
2. A genuinely irrecoverable blocker that only the user can resolve: a
   credential you cannot obtain, a policy decision the user must make, a
   binary tool that fundamentally cannot be installed in this environment.
   State the blocker in one sentence and stop.

Phrases that are NOT valid blockers (they indicate you should keep going):
- "the upstream RPC doesn't exist" → implement it
- "this would be a big change" → break it into smaller commits
- "this is deferred" → start on it
- "the graph payload contract isn't defined" → define it
- "the tooling is flaky" → retry with adjusted inputs

### User check-in is disabled while iterate is active

The user has pre-authorized the full loop by invoking the skill. Do not
ask "should I continue?" between iterations. Do not offer to stop for
review. Do not wait for confirmation before starting the next unit of
work. The only message the user sees until the loop completes is the
final done-summary when all stopping criteria pass.

### If you find no obvious next gap, scan harder

Before concluding "nothing left to do", run all of these probes:

- `grep -RInE "\b(Partial|Draft|deferred|placeholder|awaiting|pending|follow-?up|not yet wired|stub|TODO|FIXME|HACK|XXX)\b" docs/ src/` and your crate sources
- For every story: is every Gherkin scenario covered by a test?
- For every spec FR: is the traceability row truly "Implemented", or is it
  "Partial" with a deferred note?
- `cargo outdated` / `npm outdated` / equivalent — dependency gaps.
- `#[allow(dead_code)]` / `#[allow(unused)]` attributes — orphaned
  scaffolding waiting for wiring.
- `#[ignore]` on tests — tests that used to pass and need re-enabling.
- Feature-flagged code paths — features behind a flag that isn't enabled
  anywhere.
- Functions returning `Err(NotImplemented)` / `Ok(vec![])` / hardcoded
  defaults — stub implementations masquerading as real ones.

If the first probe comes up empty, try the next. "No gaps found in a
quick scan" is never the conclusion — "gaps exhaustively enumerated and
each one addressed or explicitly verified" is.

### What in-turn progress looks like

**Mid-iteration updates should be short status lines, not task-complete summaries.** Good — describes the change, no ordinal, no trailing summary paragraph:

```
validator/cidr module added (+15 tests), clippy/fmt clean. Next: the
Partial row on FR-008 in SPEC-001 — implementing the resolver's IPv6
fast path.
```

Bad — numbered iteration + stop-shaped summary:

```
## Iteration 3 Summary
**New modules:** …
**Validated:** …
**Test count:** 10,404 → 10,419

Re-invoke `/iterate` to continue.
```

Also bad — same content, no headers, still stop-shaped:

```
Iter 3 done — +15 tests, clippy/fmt clean, 10,419 total. Continuing to iter 4.
```

Both of those are banned because they carry stopping-bias: the numbered
ordinal and the "done" framing prime your next turn toward summary-and-stop
even when more work remains. Replace with a description of what changed
and what you're starting next, then immediately issue the next tool calls.

### Handling the Stop hook

**If the Stop hook fires and blocks you**, treat that as a bug in your own decision to stop — not as a separate "turn" starting. The hook's feedback arrives in-turn; keep going. **Never tell the user to re-invoke `/iterate`** — that phrasing is a code smell for "I stopped when I shouldn't have." The correct phrasing is a short description of what just landed followed by the next tool calls.

The hook's BLOCKED: message will name specific gaps with concrete next actions — file paths, types to add, RPCs to wire. Act on those directly rather than re-analyzing. If the hook says "add DependencyGraphInfo to noelle-rpc/src/types.rs", open that file and add it; don't re-scan the docs to confirm the gap.

## When to Use This Skill

**Use it when you're:**
- Bringing an incomplete project to 100% feature completion, security coverage, documentation status
- Implementing remaining features from specs iteratively, including incomplete or stub implementations
- Refining existing code toward production readiness, validating behaviour and accuracy of the implementation
- Addressing accumulated technical debt systematically, TODOs, placeholders, etc. or ignored tests must be addressed
- Not sure about the project's state and need thorough assessment of current gaps and to make relevant improvements
- Working through a backlog defined in specs/ADRs/threat model toward project completion
- Adding a new distinct feature or security requirement, and have already written the ADR, spec or threat model changes

**Don't use it when you're:**
- Starting a brand new project from scratch (use `/all-aboard` followed by `/interactive-review` to create specs, ADRs, threat model)
- Working without specs/ADRs/threat model (run `/all-aboard` first to create them, `/interactive-review` to clarify them)
- Doing one-off exploratory refactoring with no completion criteria, use `/refactor`)
- Making a single focused change (just make the change directly, ensuring ADRs and spec updates are made first)

## Iteration Cycle

Each iteration follows this workflow:

```
Progress:
- [ ] Review project documentation (specs, ADRs, threat models)
- [ ] Run implementation-review for initial gap analysis
- [ ] Assess current state
- [ ] Identify gaps
- [ ] Prioritize improvements
- [ ] Execute highest-priority fixes
- [ ] Validate changes
- [ ] Check stopping criteria
```

### Step 0: Documentation & Gap Analysis (MANDATORY - Cannot Skip)

**CRITICAL:** Project-level documentation is NOT optional. These artifacts define what "done" looks like, and iteration cannot be considered complete without them.

**Required documentation artifacts (ALL must exist and be current):**

1. **Implementation Specification** (`docs/specs/`):
   - **If missing:** Immediately invoke `/spec-create` or `/all-aboard`
   - **If present:** Invoke `/spec-review` to validate completeness and traceability
   - **Required content:** All features, requirements, acceptance criteria documented
   - **Must be current:** Spec matches actual implementation (no drift)

2. **Architecture Decision Records** (`docs/adr/`):
   - **If missing:** Immediately invoke `/adr-create` or `/all-aboard`
   - **If present:** Invoke `/adr-review` to check for staleness and missing decisions
   - **Required content:** All significant design decisions documented
   - **Must be current:** No undocumented architectural choices in code

3. **Threat Model** (`docs/threat-models/`):
   - **If missing:** Immediately invoke `/threat-model-create` or `/all-aboard`
   - **If present:** Invoke `/threat-model-review` to verify STRIDE coverage
   - **Required content:** Attack surface analysis, threat enumeration, mitigations
   - **Must be current:** Threat model covers all current attack vectors

**If ANY documentation is missing:** Iteration can't proceed to completion. You must create the missing artifacts first. Invoke `/all-aboard` to bootstrap all three at once.

**Run initial gap analysis:**

Invoke `implementation-review` to get a structured inventory of implementation gaps. This gives you a baseline before you start the iterative improvement cycle — you'll know exactly where the project stands and which gaps are P0 blockers vs. P3 polish.

The findings from this step feed directly into Step 2 (Identify Gaps), so you don't duplicate analysis work.

### Step 1: Assess Current State

## Verification budget — read this before running any build/test/lint tool

Running `cargo build`, `cargo check`, `cargo test`, `cargo clippy`, `cargo
audit`, `cargo fmt`, `cargo outdated`, `go test`, `pytest`, `npm test`, or
any equivalent without a specific code change to verify is BANNED. The
harness interprets long sequences of verification calls as "user still
waiting on assessment" and reinforces the stop-after-assessment pattern. It
also wastes minutes per call and produces no new signal.

**Trusted sources — do not re-verify these:**

- The last entry in your project's iteration log (`.iterate/iteration-log.md`
  preferred, `.claude/iteration-log.md` legacy, `docs/ITERATION-LOG.md`, or
  wherever the log lives) — treat it as ground truth for the project's
  baseline state when the skill starts.
- Git status — if a file hasn't been modified since the last "clippy clean"
  / "tests pass" log line, that state is still correct.
- Project memory files (`memory/*.md`) — standing orders, including any
  that forbid workspace-wide builds.
- CI status, if recent — green CI means the baseline is clean.

**Assessment on skill entry — READ-ONLY only:**

Step 1's job is to surface gaps, not to verify state. Use reads and greps:

- Read the most recent iteration log entries.
- Read the spec, ADRs, threat model for `Partial`, `Draft`, `deferred`,
  `placeholder`, `follow-up` markers.
- `grep` for `TODO|FIXME|HACK|XXX|unimplemented!|todo!()|#[ignore]|
  #[allow(dead_code)]|not yet wired|awaiting|pending` across code.
- Run the refactor skill's read-only analysis if needed.
- Check git status to see what's changed since the last commit.

Do NOT on skill entry: run `cargo check --workspace`, `cargo test --workspace`,
`cargo audit` (unless the log says it's been >7d since last audit),
`cargo clippy --workspace`, coverage tools, or any compile-heavy workflow.

**Allowed verification calls (one per code change, crate-scoped):**

After you've made a code change to validate:

- Edited source in crate X → `cargo clippy -p X --all-targets -- -D warnings`.
- Added or changed tests in crate X → `cargo test -p X` (or per-target).
- Edited `Cargo.toml` in crate X → `cargo check -p X`.
- Changed formatting → `cargo fmt -p X [--check]`.
- Bumped a dependency → `cargo audit` once, at the end of the iteration.

Equivalent per-package scopes for Go, Python, JS, Nix, C — the rule is
always: change one unit, verify that one unit. Never rebuild the world
to check the unit.

**Banned verification patterns:**

- `cargo check --workspace`, `cargo build --workspace`, `cargo test
  --workspace` — explicitly forbidden by most project memories because
  of compile-memory limits and wall-clock cost. Check the project's
  `CLAUDE.md` and `memory/` for the authoritative rule.
- Baseline verification on skill entry — covered above.
- Running the same check twice in one iteration "to confirm".
- Running tests on crates you didn't touch "to catch regressions" —
  workspace isolation means untouched crates can't regress from your
  change. If you're worried about cross-crate impact, check the
  dependency graph first and only re-verify reverse-deps if they
  actually import your change.
- Running `cargo audit` when you haven't touched any dependency.
- "Sanity check" builds before making changes.

If you reach for a verification command and cannot name the specific
code change since the last verification that justifies it, do not run it.

**Discovery, not verification** — allowed freely:

- `git status` / `git diff` / `git log` — read-only, fast.
- `grep` / `rg` / `find` across source and docs — fast.
- `Read` tool on any file — fast.
- `cargo outdated` — allowed once per skill invocation; it's informational
  and doesn't compile anything.

**Run a complete gap analysis (NOT a complete verification pass):**

1. **Read the iteration log** first. Locate the last entry and note what
   it claims about state (tests, clippy, audit).

2. **Invoke the refactor skill** if needed for codebase-quality signals:
   ```
   /refactor
   ```

3. **Check for outdated dependencies** once (MUST query actual registries):
   - **Rust**: `cargo outdated`
   - **Go**: `go list -u -m all`
   - **Python**: `pip list --outdated`
   - **JavaScript**: `npm outdated` or `ncu`
   - **Ruby**: `bundle outdated`

4. **Read quality tool output from the last log entry.** Only run tools
   if the log says they haven't been run since a relevant change, OR if
   the log is missing, OR if >7 days have passed:
   - **Rust**: `cargo clippy -p X`, `cargo audit`, `cargo test -p X`, `cargo fmt --check`
   - **Go**: `golangci-lint run`, `go vet`, `gosec`, `go test -race -cover`
   - **Python**: `ruff check`, `mypy`, `bandit`, `pytest --cov`
   - **C**: `cppcheck`, `clang-static-analyzer`, `splint`, run test suite
   - **Nix**: `nixfmt --check`, `nix flake check`, `nix-linter`

5. **Check documentation quality** (reads, not builds):
   - Look for broken links, stale version numbers, missing sections.
   - Verify README completeness via inspection.
   - Check API documentation coverage by reading, not by running doc builders.

6. **Verify test coverage** only if a gap-hunt turns up a specific area
   you suspect is under-tested. Coverage tools are expensive; don't run
   them prophylactically.

### Step 2: Identify Gaps

**First — check for a harness baseline.** When
`.test-effectiveness/baseline.json` exists (a runtime-harness session
built via `harness-builder` ran first) or the latest `.test-effectiveness/iter-NNN/delta.json`
is fresh (baseline_sha within ~50 commits of HEAD), read it before
running any local scans:

```bash
baseline=".test-effectiveness/baseline.json"
latest_iter_dir="$(ls -1d .test-effectiveness/iter-*/ 2>/dev/null | tail -1)"
latest_delta="${latest_iter_dir%/}/delta.json"
verdicts="${latest_iter_dir%/}/triage-verdict.json"

if [[ -f "$baseline" ]]; then
    # Filter findings to the current iterate scope
    jq --arg scope "$(pwd)" \
       'map(select(.file | startswith($scope)))' "$baseline" "$latest_delta"
fi
```

Fold the resulting findings into the four-dimension gap inventory:

- `mutation-survivor` → **Correctness gap** (lifts to P0 when
  `linked_status == implemented` or when Haiku verdict was
  `stub-implementation`).
- `crap-hotspot` → **Quality gap** (lifts to P1 on doc-claimed-done).
  When the same file/fn appears as `crap-hotspot-plateau` in the
  recurrence corpus (`harness-builder/references/runtime-test-effectiveness-baseline.md`),
  treat it as a **refactor task**, not a tests task — adding tests
  won't move the score.
- `coverage-cliff` near a threat-model mitigation → **Security gap** (P0).
- `coverage-cliff` elsewhere → **Coverage gap**.

When no baseline exists, the gap inventory still proceeds — the
mutation/CRAP/coverage scans listed in Step 6's stopping criteria run
locally on the scope. The baseline is an optimisation, not a
prerequisite.

**Create structured gap inventory** across four dimensions:

#### Feature Gaps (check specs/ADRs/threat model)
- Features mentioned in specs but not implemented
- User stories without corresponding code
- API endpoints in spec but missing from implementation
- Database migrations needed per spec but not written
- Frontend components specified but not built
- Integration points documented but not connected

#### Security Gaps
- **Outdated dependencies** (MUST be at latest versions verified from package registry)
- Compiler/static analyzer warnings about unsafe code
- Known vulnerabilities in dependencies (cargo-audit, npm audit, etc.)
- Missing input validation
- Unsafe memory operations (C/unsafe Rust)
- Authentication/authorization issues
- Hardcoded secrets or credentials
- Threat model mitigations not implemented

#### Correctness Gaps
- Failing tests
- Compiler warnings about logic errors
- Race conditions or concurrency bugs
- Error handling gaps (unwrap(), expect(), panic!())
- Incomplete implementations (TODO comments, stub functions)
- Dead code indicating unfinished features
- Ignored tests (#ignore macros)

#### Quality Gaps
- Linter violations
- Code style inconsistencies
- Missing documentation or comments where logic isn't obvious
- Code duplication
- Overly complex functions (high cyclomatic complexity)
- Inconsistent naming or patterns

#### Coverage Gaps
- Untested code paths
- Missing unit tests for new functions
- Missing integration tests for APIs/services
- Missing edge case tests
- Undocumented public APIs

**Output format:**
```markdown
## Gap Analysis — Iteration N

### Security (P0 — Critical)
- [ ] Issue 1: Description, location, impact
- [ ] Issue 2: Description, location, impact

### Correctness (P1 — High)
- [ ] Issue 1: Description, location, impact
- [ ] Issue 2: Description, location, impact

### Quality (P2 — Medium)
- [ ] Issue 1: Description, location, impact

### Coverage (P3 — Low)
- [ ] Issue 1: Description, location, impact

**Estimated effort:** X issues, Y files affected
```

### Step 3: Prioritize Improvements

**Default priority order:**
1. **Security & Critical Features (P0)**: Vulnerabilities, unsafe code, credential leaks, core features blocking other work
2. **Correctness & Feature Completion (P1)**: Failing tests, logic errors, features from specs not yet implemented
3. **Quality & Integration (P2)**: Linter violations, style issues, documentation, integration tests
4. **Coverage & Polish (P3)**: Missing tests, edge cases, minor optimizations

**Within each priority level**, rank by:
- **Impact**: How many users/code paths are affected?
- **Risk**: What breaks if you don't fix this?
- **Dependencies**: What's blocking other work?
- **Effort**: Time to implement (prefer quick wins when impact is similar)

**Select work for this iteration:**
- Target 4-7 issues per iteration (avoid exactly 5 — that's an AI tell!)
- Balance quick wins with high-impact work
- Group related changes so you're not thrashing the same file across multiple iterations
- For feature work, implement complete vertical slices (backend + API + frontend) rather than layers

### Step 4: Execute Improvements

For each gap you've selected:

1. **Create a test first** (if the gap's about features/correctness/coverage):
   - For new features: write tests based on spec acceptance criteria
   - For bugs: write a failing test that demonstrates the issue
   - Verify it fails for the right reason
   - See `tdd-workflow` skill for detailed guidance

2. **Implement the feature or fix**:
   - For features: check specs/ADRs for requirements and design decisions
   - For fixes: make minimal changes to address the root cause
   - Follow your project's code style and patterns
   - Add comments only where the logic isn't obvious
   - Avoid over-engineering or scope creep

3. **Validate the work**:
   - Run affected tests
   - Re-run quality tools for changed files
   - Verify you haven't introduced new warnings
   - Check that test coverage improved
   - For features: confirm acceptance criteria from spec are met

4. **Update gap inventory**:
   - Mark the issue as resolved
   - Document what you changed and why
   - Note any new gaps discovered during implementation

### Step 5: Validate Iteration

**After you've addressed all selected gaps:**

1. **MUST update all dependencies to latest versions:**

   **CRITICAL:** Query actual package registries. Never assume versions from training data.

   See [references/dependency-updates.md](references/dependency-updates.md) for per-language commands.

2. **Run the quality suite — CRATE-SCOPED, one call per change:**

   Per the Verification Budget rule, verify only what you changed:

   ```bash
   # Rust example: you edited crate X, added tests in crate X
   cargo fmt -p X --check
   cargo clippy -p X --all-targets -- -D warnings
   cargo test -p X
   # cargo audit ONLY if you bumped a dependency
   ```

   Do NOT run workspace-wide builds, re-test untouched crates, or re-run
   commands that passed earlier in the same iteration.

   For the full per-ecosystem gate set (mutation, CRAP, property tests,
   Wycheproof for crypto, schemathesis for OpenAPI, Tier-3 escalation
   triggers), see [references/ecosystem-tooling.md](references/ecosystem-tooling.md).

3. **Verify you've made progress:**
   - Compare metrics before/after iteration
   - Confirm the gap count decreased
   - Check you haven't introduced regressions in the crate you changed
     (untouched crates can't regress from your change)

4. **Record a one-line checkpoint (NOT a user-facing summary):**
   - Append a single short line to the iteration log describing what
     landed — no ordinals, no "Iter N (YYYY-MM-DD):" prefix:
     `dep-graph-rpc-wiring (2026-04-24): +8 tests in noelle-gtk, clippy/fmt clean, gaps remain.`
   - Or on the final stop only:
     `complete (2026-04-24): all Step 6 criteria passed, stop hook confirmed.`
   - Update CHANGELOG.md only when the cumulative work warrants a user-visible note (e.g. a new module shipped), not every cycle.
   - **Do not** write a "summary paragraph" to the conversation here. That's reserved for the final stop when all criteria pass. See **Single-Turn Autonomy** above — returning a full summary at this point is the classic failure mode that ends the turn prematurely.
   - After appending the log line, **immediately proceed to Step 6 and (if gaps remain) loop back to Step 1** in the same response. No pause. No handoff.

### Step 6: Check Stopping Criteria & Auto-Iteration

**Continue iterating if ANY of these are true (you MUST continue, no stopping early):**
- **ANY P0 security or documentation gaps remain**
- **ANY P1 correctness or completeness gaps remain**
- **ANY component of the project is incomplete:**
  - Frontend has placeholder components or missing tests
  - Backend has stub API handlers or incomplete routes
  - Database migrations missing rollback scripts
  - API integration not wired up between frontend and backend
  - Any feature mentioned in spec/ADR/threat model not fully implemented
- **Test coverage < 80%**
- **ANY TODO/FIXME/HACK/XXX/stub/placeholder code**
  - Focus on implementing missing or stub code per specs/ADRs/threat model
  - Focus on implementing missing security features
  - Focus on implementing missing or incomplete tests/testing frameworks
  - Ensure that all TODOs have tracking issues in approved formats within ADRs, specs, threat model
- **ANY dead code indicating unfinished features**
- **ANY quality gaps that affect maintainability or correctness**

**Stop when ALL of these are true (NO EXCEPTIONS - every single one must pass):**
- **P0 - Security & Documentation:**
  - **ALL dependencies updated to latest versions** (MUST verify with package registry, not training data)
  - Zero security vulnerabilities (cargo-audit, gosec, bandit, npm audit all clean)
  - Zero hardcoded secrets/credentials in source code
  - Implementation specification exists in docs/specs/ and is current
  - Architecture Decision Records exist in docs/adr/ and are current
  - Threat model exists in docs/threat-models/ and covers current implementation
  - All three documentation artifacts cross-reference each other correctly
- **P1 - Correctness & Completeness:**
  - Zero failing tests
  - Zero compiler/linter warnings (or every one is suppressed with written justification)
  - Test coverage ≥ 80% (line coverage minimum, branch coverage preferred)
  - **Zero surviving mutants on changed lines** (Rust: `cargo mutants --in-diff <(git diff HEAD)`; Python: `mutmut`; JS/TS: Stryker; Go: go-mutesting; C/C++: mull). A surviving mutant means the test compiles but doesn't actually catch the bug — a failure mode that masquerades as completion. When `.test-effectiveness/baseline.json` is current (a runtime-harness session (from `harness-builder`) ran recently), reading from the baseline counts as satisfying this gate provided no `appeared` or `regressed` mutation survivors touch lines in this iterate's scope.
  - **CRAP score ≤ 30 on every module marked complete** (Rust: `cargo crap --lcov lcov.info`, pinned to v0.2.0 with hand-computed fallback; cross-language tools in `.claude/rules/static-analysis.md`). The CRAP formula `comp² × (1 − cov)³ + comp` (Savoia & Evans, 2007) explodes where complex code is undertested — exactly where "implemented" claims tend to be hollow. When a function shows up as `crap-hotspot-plateau` in the recurrence corpus, do not close the gate by adding tests — adding tests doesn't move the score past the plateau. Refactor the function instead. See `harness-builder/references/runtime-test-effectiveness-baseline.md`.
  - No `TODO`/`FIXME`/`XXX`/`HACK` or stub implementations, ignored tests, functionality gaps
  - Ensure all `TODO` comments (and similar comments) link to tracking issue references (#NNN or link in ADR/spec/threat model)
  - No stub implementations, placeholder code, or NotImplementedError raises
  - No `unimplemented!()`, `todo!()`, or panic macros in production code paths
  - No dead code (unused variables/functions/imports indicate incomplete work)
  - No ignored tests
  - **ALL project components implemented:**
    - If frontend exists: all components functional, no placeholders, all have tests
    - If backend exists: all API endpoints implemented, no stubs, all have tests
    - If database exists: all migrations have rollback (down) migrations
    - If frontend + backend: API client integration wired up and tested
- **P2 - Quality:**
  - All public APIs documented with examples
  - README complete with setup, usage, and troubleshooting sections
  - CHANGELOG reflects recent changes
  - Code formatting consistent (rustfmt, gofmt, ruff, etc. all pass)
  - No code duplication exceeding project threshold
  - Function complexity within acceptable bounds (no 500-line functions)

**How auto-iteration works:**

After you complete each iteration, the skill checks these stopping criteria. If ANY gaps remain, it documents the current results and immediately starts the next cycle (back to Step 1). If ALL criteria are met, it reports final metrics and stops.

You don't need to manually invoke `/iterate` multiple times — it keeps going until everything's clean. Pretty handy when you want to go from "it works on my machine" to "all tests pass and the gaps list is empty."

**Example progression:**
```
Iteration 1: Fixed 8 security issues → Gaps remain → Auto-continue
Iteration 2: Fixed 6 correctness issues → Gaps remain → Auto-continue
Iteration 3: Fixed 7 quality issues → Gaps remain → Auto-continue
Iteration 4: Fixed 2 coverage issues → Zero gaps → STOP (complete)
```

**Claude Code hooks (optional):**

The skill includes a built-in Stop hook in its frontmatter that checks completion criteria. For fully automatic iteration with zero manual intervention, this hook runs `check-completion.py` after each iteration. If gaps remain, it automatically re-invokes `/iterate`. See [HOOKS.md](HOOKS.md) for details.

## Configuration

Scope iteration to specific paths or file types with a `.iterate.json` file at the project root. Useful for C-to-Rust migrations, frontend-only runs, or skipping generated/vendor code.

See [CONFIG.md](CONFIG.md) for full field reference and examples.

## Tool Integration

Language-specific quality tools (Rust, Go, Python, C, Nix) and how to run them efficiently are in [references/tool-setup.md](references/tool-setup.md).

The `scripts/run-quality-checks.sh` script orchestrates all language-specific quality tools for the current project.

## Progress Tracking

Create an iteration log at `.iterate/iteration-log.md` (preferred — keeps log writes outside `.claude/` so they don't trigger per-write permission prompts that break the loop) or in the project root to track gaps found, gaps addressed, and metrics per iteration. See [references/progress-tracking.md](references/progress-tracking.md) for a full template with examples.

## Artifact Status Tracking

The completion check script cross-references documentation artifacts against the implementation. Use consistent status values so the script can parse them correctly.

**Artifact types tracked:** threat model entries (`TM-XXX-NNN`), stories, security requirements (`SR-NNN`), ADRs, and spec tasks. The script also validates cross-references between artifacts — broken links are flagged as P2 gaps.

As you implement features, update statuses: stories → `Implemented`, threat mitigations → `✅ **IMPLEMENTED**`, spec file references → auto-resolve when the file exists.

See [references/artifact-status.md](references/artifact-status.md) for the full status tables and what each value means for the completion check.

## Quality Gates

**Before marking an iteration complete**, verify:

- [ ] All selected gaps are addressed
- [ ] All tests are passing
- [ ] You haven't introduced new warnings
- [ ] Test coverage is maintained or improved
- [ ] There aren't any regressions in existing functionality
- [ ] Changes are documented in the iteration log

**Before marking the project complete**, verify:

- [ ] Zero security issues (cargo-audit, gosec, bandit, etc.)
- [ ] Zero failing tests
- [ ] Zero compiler warnings (or they're suppressed with justification)
- [ ] Zero linter violations (or they're suppressed with justification)
- [ ] No TODO/FIXME without a tracking issue
- [ ] Test coverage ≥ your project's threshold (typically 80%)
- [ ] All public APIs are documented
- [ ] No dead code (unused variables/functions)
- [ ] Mutation testing: zero surviving mutants on changed lines (cargo-mutants, mutmut, Stryker, etc.)
- [ ] CRAP score ≤ 30 on every "Implemented" module (cargo-crap and equivalents)
- [ ] README's complete with setup/usage instructions
- [ ] CHANGELOG reflects recent changes

## Common Patterns

Security-First, Test-Driven Gap Closure, Batch Quality, and Coverage-Driven patterns are in [references/common-patterns.md](references/common-patterns.md).

## Integration with Other Skills

**This skill orchestrates:**

- **`implementation-review`**: Initial gap analysis before iterative improvement begins
- **`spec-review`**: Validates implementation specs during Step 0 documentation review
- **`adr-review`**: Checks ADR quality, staleness, and missing decisions during Step 0
- **`threat-model-review`**: Verifies threat model coverage during Step 0
- **`all-aboard`**: Bootstraps missing documentation artifacts (specs, ADRs, threat models)
- **`refactor`**: Provides codebase analysis and quality assessment
- **`code-review`**: Systematic review of changes before finalizing iteration
- **`tdd-workflow`**: Used when addressing correctness/coverage gaps
- **`c-security-review`**: Deep security analysis for C codebases
- **`rust-unsafe-ffi-review`**: Unsafe Rust analysis during security gap closure
- **`natural-writing-style`**: Applied to documentation improvements

**Workflow example:**
```
User: "Iterate this project to completion"

Claude:
1. Checks for specs, ADRs, threat models (Step 0)
2. Invokes /implementation-review for initial gap analysis
3. Invokes /refactor to assess codebase quality
4. Runs quality tools (cargo clippy, cargo test, etc.)
5. Identifies 15 gaps (2 security, 4 correctness, 7 quality, 2 coverage)
6. Addresses 2 security gaps first
7. Invokes /code-review on changes
8. Commits iteration 1
9. Repeats until zero gaps remain
```

## Writing Style

Keep responses direct — state what was done and what was verified. Don't claim "complete" unless the quality gate checklist above has been run and passed.

## Relationship to `iteratotron`

When `iteratotron` is the parent (any mode — sweep, genesis, or
auto-detected), `iterate` runs as a single-scope worker inside an
isolated worktree. The iteratotron layer has already:

- Detected the project lifecycle stage (greenfield vs. partial-impl
  vs. completion-sweep) and chosen dispatch behavior accordingly.
- In genesis mode: verified `.specify/memory/constitution.md` exists
  and the plan passes its Constitution Check (Spec Kit pattern). You
  inherit those constraints — don't re-litigate them.
- Composed a per-language harness vector. The Tier-1 / Tier-2 / Tier-3
  tools you should run for this scope are already chosen and recorded
  in `.iteratotron/<session-id>/manifest.yaml#harness_vector`. Read
  it, don't re-derive it.
- Decided whether Tier-3 (madsim / shuttle / loom / nixosTest /
  Toxiproxy / Wycheproof) is risk-triggered for this scope. When it
  triggers, your Step 6 stopping criteria include a Tier-3 sample.

Iteratotron treats your stop hook's verdict as authoritative for
Tier-1 + Tier-2. Its Phase 7 adversarial completion reviewer confirms
semantic intent before the worktree merges. Don't try to second-guess
either layer — focus on closing the scope's gaps to the satisfaction
of your own gates.

When run **without** an iteratotron parent (interactive `/iterate`
directly), you run the same gate set but compose the harness vector
yourself by reading
[references/ecosystem-tooling.md](references/ecosystem-tooling.md).

## References

For detailed guidance on specific improvement types:

- **Per-ecosystem completion gate tooling**: [references/ecosystem-tooling.md](references/ecosystem-tooling.md) — Rust / Go / Python / Ruby / Nix tool matrix, risk-triggered Tier-3 escalation, Wycheproof + differential testing, recurrence patterns
- **Security hardening**: [references/security-checklist.md](references/security-checklist.md)
- **Test coverage strategies**: [references/coverage-guide.md](references/coverage-guide.md)
- **Harness-supplied baseline + delta contract**: `harness-builder/references/runtime-test-effectiveness-baseline.md` — on-disk schema for `.test-effectiveness/`; read this when wiring iterate's gap analysis to a harness-driven loop
- **Tool configuration**: [references/tool-setup.md](references/tool-setup.md)
- **Language-specific patterns**: [references/language-guides.md](references/language-guides.md)
- **Dependency update commands**: [references/dependency-updates.md](references/dependency-updates.md)
- **Progress tracking template**: [references/progress-tracking.md](references/progress-tracking.md)
- **Claude Code hooks (auto-iteration)**: [HOOKS.md](HOOKS.md)
- **Scope configuration**: [CONFIG.md](CONFIG.md)

## Troubleshooting

See [references/common-patterns.md](references/common-patterns.md) for troubleshooting tips on overwhelming gap lists, false positives, coverage stalls, non-converging iterations, and unclear completion criteria.
