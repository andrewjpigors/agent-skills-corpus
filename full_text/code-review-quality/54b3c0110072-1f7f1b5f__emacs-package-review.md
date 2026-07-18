---
name: emacs-package-review
description: >
  Multi-dimensional review of existing Emacs Lisp packages and codebases for
  security, code quality, testing, UX, accessibility, refactoring opportunities,
  integration patterns, and distribution readiness. Use this skill whenever the
  user wants to review an existing elisp package, audit emacs code, improve an
  existing emacs project, refactor elisp, assess elisp package quality, or
  prepare an existing package for MELPA/GNU ELPA submission. Also use when the
  user mentions "review my emacs code", "audit this elisp", "refactor this
  package", "is this ready for MELPA", or similar.
license: Apache-2.0
compatibility: >
  Requires Emacs 29.1+, git. Designed for Claude Code.
metadata:
  author: custom
  version: "1.0"
  target-emacs: "29.1+"
  skill-ecosystem: "all-aboard, adr-review, spec-review, threat-model-review"
allowed-tools: Bash(emacs:*) Bash(git:*) Bash(grep:*) Bash(eask:*) Read Write AskUserQuestion
---

# Emacs Package Review

Review existing Emacs Lisp packages across security, code quality, testing,
UX, accessibility, refactoring, and distribution readiness.

## Quick Start

1. Scan the package: count `.el` files, check if tests exist, check for `Eask`/`Cask`, look for `shell-command`/`eval` usage. Then **use `AskUserQuestion`** to confirm: "I found [X .el files], [tests: yes/no], distribution target [from package headers if present]. What aspect should I focus on — security, MELPA readiness, or a full review?"
2. Run `scripts/elisp-review.sh` (or byte-compile + checkdoc + package-lint manually) to get automated findings
3. Work through the seven review dimensions in order: security, quality, testing, refactoring, UX, integration, packaging
4. Classify each finding: CRITICAL / IMPORTANT / MINOR / INFO
5. Write a structured findings report with severity ratings and concrete fixes

## When to Use This Skill

- Reviewing or auditing an existing Emacs Lisp package before publishing or submitting to MELPA/GNU ELPA
- Running a security assessment on elisp code that calls shell commands, evaluates data, or handles file paths
- Refactoring a codebase to fix naming convention violations, DRY issues, or deprecated API usage
- Checking test coverage and quality before releasing a new package version
- When the user says "review my emacs code", "audit this elisp", "is this ready for MELPA", or similar

## When to activate

Use this skill when the user wants to review, audit, or improve existing elisp code — whether that's preparing a package for MELPA or GNU ELPA, refactoring a codebase, running a security assessment, or checking if something's ready for submission.

## Prerequisite skills — invoke when relevant

This skill can operate standalone or integrate with companion review skills:

- **all-aboard** → If the project lacks documentation, run onboarding first
- **adr-review** → Review Architecture Decision Records
- **spec-review** → Review functional specification completeness
- **threat-model-review** → Review security threat model completeness

If `all-aboard`'s available and the project lacks docs/spec/threat-model,
suggest running it before review. If docs exist, proceed with review directly.

## Review workflow

### Phase 1: Automated quality scan

Run [scripts/elisp-review.sh](scripts/elisp-review.sh) — it'll execute all
automated checks and produce a findings summary. Don't skip this step; it'll
catch things that are easy to miss in manual review.

Alternatively, run individual checks:
- Byte-compile (strict warnings-as-errors)
- checkdoc validation
- package-lint metadata check
- relint regexp linting
- Test suite execution
- Security pattern grep

### Phase 2: Manual review — seven dimensions

Review across all dimensions. You'll find detailed checklists in the
corresponding reference files — they're worth reading before diving in.

**Dimension 1: Security** → [security-review-checklist.md](references/security-review-checklist.md)
- Grep for dangerous patterns (shell-command, eval, read, make-temp-name)
- Trace data flow from user input to process/eval/file operations
- Validate file path operations against traversal
- Assess supply chain risk from dependencies

**Dimension 2: Code quality** → [review-dimensions.md](references/review-dimensions.md)
- Verify naming conventions (prefix, double-dash, predicates)
- Check lexical-binding on all files
- Verify headers complete and correct
- Check for deprecated APIs

**Dimension 3: Testing** → [review-dimensions.md](references/review-dimensions.md)
- Assess test coverage adequacy
- Check test quality (behavior vs code exercise)
- Verify tests run in clean `emacs -Q --batch`
- Check edge case coverage

**Dimension 4: Refactoring** → [refactoring-patterns.md](references/refactoring-patterns.md)
- Identify code duplication (DRY violations)
- Find macro extraction opportunities
- Check polymorphism usage (cl-defgeneric)
- Identify dead code

**Dimension 5: UX and accessibility** → [ux-accessibility-checklist.md](references/ux-accessibility-checklist.md)
- Check completing-read usage
- Verify defcustom for all options
- Check keyboard accessibility
- Verify face definitions

**Dimension 6: Integration** → [review-dimensions.md](references/review-dimensions.md)
- Check conditional dependency patterns
- Verify declare-function for optional deps
- Check autoload cookies
- Verify mode cleanup

**Dimension 7: Packaging** → [quality-gates-checklist.md](references/quality-gates-checklist.md)
- Verify MELPA/GNU ELPA requirements
- Check CI pipeline completeness
- Verify CHANGELOG maintenance
- Assess documentation completeness

### Phase 3: Generate review report

Produce structured findings with severity ratings:
- CRITICAL: Security vulnerability, data loss risk, crash
- IMPORTANT: Quality gate failure, missing tests, wrong API usage
- MINOR: Style issue, minor DRY violation
- INFO: Suggestion, nice-to-have

## Reference files

| File | When to read |
|------|-------------|
| [review-dimensions.md](references/review-dimensions.md) | Code quality, testing, integration |
| [security-review-checklist.md](references/security-review-checklist.md) | Security audit |
| [refactoring-patterns.md](references/refactoring-patterns.md) | DRY, macros, polymorphism |
| [ux-accessibility-checklist.md](references/ux-accessibility-checklist.md) | UX, accessibility |
| [quality-gates-checklist.md](references/quality-gates-checklist.md) | Final validation |

## Writing Style

Apply `natural-writing-style` to all review findings, reports, and recommendations.

Findings should be specific: name the function, file, and line where the issue appears. Don't claim a security issue is "resolved" or a quality gate is "passing" unless you've run the relevant tool and seen clean output. List what was checked and what wasn't.

## Edge cases

- **No tests**: Flag as CRITICAL and generate a test plan — you can't ship without them
- **No threat model**: Flag as IMPORTANT, recommend threat-model-create
- **Legacy code (pre-Emacs 29)**: Note deprecated API usage
- **Very large codebase**: Prioritize security, then quality gates, then refactoring
