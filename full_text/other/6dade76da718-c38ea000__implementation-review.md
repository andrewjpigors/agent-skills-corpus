---
name: implementation-review
description: >-
  Performs deep implementation review with gap analysis, quality gates, and
  guided iteration toward complete functionality. Use when starting implementation
  cycles, reviewing development progress, auditing completeness before release,
  or when the user mentions implementation review or progress tracking.
disable-model-invocation: false
allowed-tools: Read Write Edit Bash Grep Glob AskUserQuestion
metadata:
  version: 2.0.0
  author: agentic-skills
---

# Implementation Review & Iteration

You're the conductor of a development cycle. Your job: figure out what's done, what's
not, and guide the project toward actually-working code. Not "tests pass" done --
*really* done, with real data flowing through real integrations.

## Quick Start

1. Read project docs (README, CLAUDE.md, specs, ADRs, threat models) to understand goals and constraints. If the scope is unclear after reading docs, **use `AskUserQuestion`** to ask: "I see [X TODOs / Y unimplemented functions / Z disabled tests] — do you want me to focus on [specific area from docs], or do a full sweep of all gaps?"
2. Run the gap analysis script: `bash "scripts/detect-gaps.sh"` (path relative to the skill's installation directory)
3. Categorize findings by priority (see Priority Matrix below)
4. Work through items using the iteration cycle, re-validating after each change

## When to Use This

- Starting a new implementation sprint
- Reviewing progress mid-development
- Auditing completeness before a release
- After a big refactor to verify nothing's broken

## Phase 1: Implementation State Analysis

### 1.1 Project Goal Assessment

Read the project's documentation to understand what "done" looks like:

```bash
# Read project docs
cat README.md
cat CLAUDE.md 2>/dev/null

# Read specs, ADRs, and threat models (these define requirements and constraints)
ls docs/specs/ 2>/dev/null && cat docs/specs/*.md 2>/dev/null
ls docs/adr/ 2>/dev/null && cat docs/adr/*.md 2>/dev/null
ls docs/threat-models/ 2>/dev/null && cat docs/threat-models/*.md 2>/dev/null

# Get a feel for the codebase
find . -name "*.rs" -o -name "*.go" -o -name "*.c" -o -name "*.py" -o -name "*.ts" | head -30
```

**Specs, ADRs, and threat models are first-class inputs.** If they exist, read them before gap analysis — they define acceptance criteria, architectural constraints, and security requirements that inform how you'll classify every finding. If they don't exist, note that as a documentation gap.

### 1.2 Gap Analysis

Run the detection script to find incomplete implementations:

```bash
bash "scripts/detect-gaps.sh"
```

This searches for:
- **Unfinished code**: `todo!()`, `unimplemented!()`, `panic!("not yet")`, `TODO`, `FIXME`, `XXX`
- **Placeholder values**: functions returning empty collections or hardcoded defaults
- **Disabled tests**: `#[ignore]`, `@pytest.mark.skip`, `.skip(`, `DISABLED_`
- **Dead code**: annotations hiding unfinished work
- **Blanket lint suppression**: module-level `#![allow(dead_code)]` or multi-attribute allows that silence entire crates
- **Stub comment markers**: `// Stub`, `// Placeholder`, `STUB:` comments marking incomplete code
- **Hardcoded decision values**: sentinel values like `"latest"`, `"0.0.0"`, `= 0.85`, `= false` feeding into logic paths
- **Mock leakage**: mock/fake/dummy patterns outside test directories
- **Hardcoded test URLs**: localhost, 127.0.0.1, example.com in non-test code

The script also supports `--json` for machine-readable output and `--git-context` to
limit analysis to recently changed files. Sections 11-14 cover ignored test auditing,
dead code classification, documentation cross-referencing, and git-aware scoping.

If you don't have the script available, check [references/detection-patterns.md](references/detection-patterns.md)
for the patterns to search manually.

### 1.5 Documentation Cross-Reference

Gap analysis catches the *what* — but you need docs to understand the *why*. Before
classifying any finding, cross-reference it against project documentation in this order:

1. **Plans, specs, ADRs, and threat models** (design docs, RFCs, architecture decisions, security constraints, risk assessments)
2. **Root docs** (README, CLAUDE.md, CONTRIBUTING.md, DESIGN.md)
3. **Issue tracker** (linked issues, milestone boards)
4. **Code-level docs** (doc comments, inline explanations)

ADRs carry special weight for gap classification — a finding that contradicts an accepted ADR
is a regression, not just a gap. Threat models inform whether a finding has security implications
that bump its priority.

For each gap analysis finding, classify it:

| Classification | Meaning | Action |
|---|---|---|
| Unfinished feature | Planned work that isn't done yet | Needs implementation or issue link |
| Dead from refactoring | Code that lost its purpose during changes | Flag for removal via `refactor` |
| Intentionally deferred | Explicitly postponed with documented reason | Verify the reason still holds |
| Ambiguous/undocumented | Can't tell from available docs | Needs investigation before any action |

**Completeness drivers** -- for every finding, ask yourself two questions:

- **"Is there a test?"** If not, you can't know whether the code works or is even needed.
- **"Is the intent documented?"** If not, you're guessing at whether it's a gap or a feature.

When a finding fails both questions, it's your highest-priority investigation target.

See [references/documentation-cross-reference.md](references/documentation-cross-reference.md) for
deep guidance on documentation hierarchy and cross-referencing techniques, and
[references/dead-code-classification.md](references/dead-code-classification.md) for the
full decision tree on classifying dead code.

### 1.3 Functional Completeness

Beyond automated detection, verify these manually:

- [ ] Every public API has a real implementation (not stubs)
- [ ] Database operations actually persist and retrieve data
- [ ] External service integrations hit real endpoints (not mocked in prod)
- [ ] Error handling covers actual failure scenarios, not just happy paths
- [ ] Configuration loads from real sources (env vars, config files)
- [ ] End-to-end workflows complete successfully with realistic data

## Phase 2: Quality Gates

Run through these gates for every piece of work. They aren't optional.

### Implementation Completeness

- [ ] No `todo!()`/`unimplemented!()` or language equivalent in production paths
- [ ] No placeholder return values (empty collections, hardcoded responses)
- [ ] No hardcoded decision values (`= 0.85`, `"latest"`, `"0.0.0"`, `= false`) feeding into logic
- [ ] All `TODO`/`FIXME` items in critical paths resolved
- [ ] Disabled tests either fixed or documented with a clear reason and timeline
- [ ] No module-level `#![allow(dead_code)]` blankets in production crates
- [ ] No blanket lint suppression lists hiding production issues (e.g. `clippy::unwrap_used` at module scope)
- [ ] No `// Stub` or `// Placeholder` comments marking incomplete functions
- [ ] Public APIs all have working implementations

### Real Data Integration

- [ ] Database ops tested with actual persistence (not in-memory fakes)
- [ ] External APIs properly implemented (not stubbed in production code)
- [ ] File I/O handles real filesystem edge cases
- [ ] Config points to real services in production mode
- [ ] Error handling tested with actual failure injection
- [ ] Network timeouts and retries behave correctly under real conditions

### Security

- [ ] No hardcoded credentials or secrets
- [ ] Input validation on all external data boundaries
- [ ] Error messages don't leak internal details
- [ ] Auth/authz controls tested with real scenarios
- [ ] Crypto uses established libraries (no hand-rolled)
- [ ] SQL/command injection prevention verified

### Testing

- [ ] Unit tests cover public functions with realistic inputs
- [ ] Integration tests validate end-to-end workflows
- [ ] Error scenarios tested with real failure conditions
- [ ] No tests that always pass instantly (suspicious for fakes)
- [ ] Test data reflects production shapes and volumes
- [ ] Performance tested with realistic data volumes where it matters

See [references/quality-gates-detail.md](references/quality-gates-detail.md) for
expanded gate criteria and language-specific checks.

### Test Coverage for Gaps

- [ ] Every finding classified as "unfinished feature" has at least one test covering the expected behavior
- [ ] Every ignored/skipped test has a documented reason AND a linked issue for re-enablement
- [ ] Ambiguous findings have test coverage added before any classification decision
- [ ] No test files contain only placeholder assertions (`assert(true)`, `expect(1).toBe(1)`)
- [ ] **Mutation testing run on every "Implemented" claim** — if any "Implemented" feature has surviving mutants, demote it to `unfinished` until tests kill them (Rust: `cargo mutants --file <impl-file>`; Python: `mutmut run --paths-to-mutate=<file>`; JS/TS: Stryker)
- [ ] **CRAP score < 30 on every module marked complete** (Rust: `cargo crap --lcov lcov.info`) — a high CRAP score on a "complete" module is a stop-bias pattern: the docs say done, the metric says undertested

Test-quality signals are critical for this skill because implementation-review's whole job is separating real "done" from fake "done." A green test suite isn't proof of completeness — mutation survivors and high CRAP scores reveal tests that pass without actually testing. See `.claude/rules/static-analysis.md` for the canonical guidance and the full ecosystem tool table.

See [references/ignored-test-audit.md](references/ignored-test-audit.md) for the ignored test audit workflow.

### Documentation Completeness

- [ ] Public modules flagged as incomplete have their intent documented (even if implementation isn't done)
- [ ] Project goals from specs/plans cross-referenced against actual implementation state
- [ ] Dead-from-refactoring findings confirmed by checking git history for the removal of callers
- [ ] Deferred items have an issue link or explicit rationale in project docs

## Phase 3: Priority Matrix

Sort your findings into these buckets. Tag each item with its classification from
Phase 1.5 (unfinished / dead / deferred / ambiguous):

**P0 -- Blockers** (fix before anything else)
- Unimplemented functions in production paths [unfinished]
- Core features returning placeholder values or hardcoded decision values (fake coverage %, sentinel version strings, `= false` for safety checks) [unfinished]
- Security vulnerabilities [any classification]
- Integration points that are mocked instead of real [unfinished]

**P1 -- Core functionality gaps**
- TODO/FIXME in critical paths [unfinished]
- Functions returning empty/None where real data should flow [unfinished/ambiguous]
- Fabricated identifiers (fake UUIDs, placeholder PURLs, made-up signatures) [unfinished]
- Disabled tests for core features [deferred -- verify reason still holds]
- Missing error handling for common failure cases [unfinished]
- Performance issues under realistic load [ambiguous until profiled]

**P2 -- Integration and data flow**
- Incomplete end-to-end workflows [unfinished]
- Missing database persistence or stubbed external service calls (log-only, no-op implementations) [unfinished/dead]
- Configuration validation gaps [ambiguous]
- Module-level `#![allow(dead_code)]` blankets in production crates [dead -- flag for removal]

**P3 -- Polish and edge cases**
- Error handling for rare scenarios and resource cleanup in error paths [deferred/ambiguous]
- Performance tuning [deferred]
- Documentation accuracy (stale test counts, resolved TODOs still listed) [dead]
- Genuinely unused code behind `#[allow(dead_code)]` that should be deleted [dead -- hand off to `refactor`]

## Phase 4: Iteration Cycle

For each priority item, follow this cycle:

### Step 1: Baseline

Before making changes, capture the current state:

```bash
# Count incomplete markers (language-agnostic)
bash "scripts/detect-gaps.sh" --count 2>/dev/null || \
  grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.rs" --include="*.go" --include="*.py" --include="*.c" --include="*.ts" . | grep -v test | wc -l
```

### Step 2: Implement

Write real functionality. No stubs. Don't say "I'll finish this later." If it's too big
for one pass, break it into smaller pieces that each work completely on their own.

### Step 3: Validate

```bash
# Run the project's test suite
# (adapt to your project's test runner)
cargo test --all          # Rust
go test ./...             # Go
pytest                    # Python
npm test                  # Node.js
make test                 # C/Make projects

# Verify no new incomplete markers introduced
bash "scripts/detect-gaps.sh" --count
```

### Step 4: Anti-Regression Check

Compare against your baseline. The number of incomplete markers should go down
(or at minimum stay flat). If it went up, you've introduced new debt -- don't
move on until you fix it.

### Step 5: Update Progress

Keep track of what you've done. Update project docs or a progress section
in CLAUDE.md with:
- What was completed
- Quality gates passed
- What's next
- Current blockers

Then pick the next priority item and repeat.

## Phase 5: Progress Tracking

Track implementation progress in a structured format. Here's a template
you can add to the project's CLAUDE.md or a separate tracking file:

```markdown
## Implementation Progress: [X]% Complete

### Completed
- [Feature/fix] -- quality gates passed, tests added
- [Feature/fix] -- integrated with real data

### In Progress
- [Current item] -- estimated completion: [timeframe]
- Blockers: [none / description]

### Next Up
1. [Next priority item]
2. [Second priority item]

### Metrics
- Incomplete markers: [N] (down from [M])
- Test coverage: [X]%
- Disabled tests: [N] (all justified: yes/no)
- Mutation survivors on "Implemented" modules: [N] (target: 0)
- Modules with CRAP > 30: [N] (target: 0)
```

## Writing Style

Progress reports and gap analysis are read by stakeholders. Apply `natural-writing-style` to all output:

- State what's done, what's verified, what remains — never round up
- Never include time estimates or effort judgments ("quick fix", "significant work")
- Don't claim features are "complete" without listing what was and wasn't tested
- Describe remaining work by scope (files, systems, dependencies), not subjective effort

## Integrating with Other Skills

This skill works well as an orchestrator. Call on other skills during the cycle:

- `/assess-system` -- Check your dev environment before starting
- `/choose-tests` -- Pick the right test strategy for changes you're making
- `/dev-iteration` -- For the actual coding loop within each priority item
- `/troubleshoot-dev` -- When something breaks during implementation
- `/refactor` -- Hand off confirmed dead code and structural cleanup from your findings
- `/code-review` -- Pair with this for a second-pass quality check on completed items
- `/spec-review` -- Validate specs and surface requirement gaps before classifying findings
- `/adr-review` -- Check ADRs for staleness, contradictions, and undocumented decisions
- `/threat-model-review` -- Verify threat model coverage against current implementation
<!-- Hook: future refactoring skill integration point for automated dead code removal -->

## References

- [references/detection-patterns.md](references/detection-patterns.md) -- Language-specific detection patterns for manual searches
- [references/quality-gates-detail.md](references/quality-gates-detail.md) -- Expanded gate criteria with language-specific checks
- [references/progress-template.md](references/progress-template.md) -- Full progress tracking template
- [references/documentation-cross-reference.md](references/documentation-cross-reference.md) -- Documentation hierarchy and cross-referencing techniques
- [references/dead-code-classification.md](references/dead-code-classification.md) -- Full decision tree for classifying dead code
- [references/ignored-test-audit.md](references/ignored-test-audit.md) -- Workflow for auditing ignored and skipped tests
