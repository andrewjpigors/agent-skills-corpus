---
name: emacs-package-create
description: >
  Bootstrap new Emacs Lisp package projects targeting Emacs 29+ with full
  onboarding, security documentation, architecture decisions, specs, threat
  modeling, CI/CD pipelines, testing infrastructure, and CLAUDE.md memories.
  Use this skill whenever the user wants to create a new Emacs package, start
  a new elisp project, scaffold an Emacs minor/major mode, build an Emacs
  extension or plugin, or mentions wanting to write elisp code as a package.
  Also use when the user says "new emacs project", "create elisp package",
  "bootstrap emacs mode", or similar.
license: Apache-2.0
compatibility: >
  Requires Emacs 29.1+, git, and optionally Eask or Cask for dependency
  management. Designed for Claude Code.
metadata:
  author: custom
  version: "1.0"
  target-emacs: "29.1+"
  skill-ecosystem: "all-aboard, adr-create, spec-create, threat-model-create"
allowed-tools: Bash(emacs:*) Bash(git:*) Bash(eask:*) Bash(cask:*) Read Write AskUserQuestion
---

# Emacs Package Create

Create production-quality Emacs Lisp packages with full onboarding, security
documentation, architecture decisions, testing infrastructure, and CI/CD.

## Quick Start

1. Gather requirements: package name, purpose, target Emacs version, distribution target (MELPA/GNU ELPA/private)
2. Run `all-aboard` to produce onboarding docs (ADR + spec + threat model)
3. Scaffold directory structure with main `.el`, tests, CI, and Eask/Cask config
4. Write code following the naming, security, and documentation rules below
5. Run `scripts/elisp-check.sh` — all gates must pass before publishing
6. Verify the package loads cleanly: `emacs -Q --batch --load your-package.el`

## When to Use This Skill

- Creating a new Emacs Lisp package from scratch, including minor/major modes and extensions
- Scaffolding a package that integrates with tools like Magit, Eglot, or Transient
- Starting any elisp project that needs testing infrastructure, CI, and distribution setup
- Preparing a package for MELPA or GNU ELPA submission with full quality gates
- When the user says "new emacs project", "create elisp package", "bootstrap emacs mode", or similar

## When to activate

Use this skill when the user wants to create a new Emacs package or elisp project, scaffold a major or minor mode, or build an extension that integrates with tools like Magit, Eglot, or Transient. It's also the right choice for packages targeting MELPA or GNU ELPA submission.

## Prerequisite skills — invoke these FIRST

This skill orchestrates a full onboarding pipeline. Invoke these companion
skills in order before writing any elisp code:

1. **all-aboard** → Full project onboarding (consolidates steps 2-4 below)
2. **adr-create** → Architecture Decision Records for the package
3. **spec-create** → Functional specification from stated goals
4. **threat-model-create** → Security threat model for the elisp package

If `all-aboard`'s available, use it — it consolidates adr-create, spec-create,
and threat-model-create into a single onboarding flow. Otherwise, run them
individually in order.

After onboarding completes, make sure CLAUDE.md exists with project memories
capturing all decisions.

## Workflow

### Phase 1: Onboard and document

1. Check for any existing `.el` files, `Eask`, or `Cask` in the current directory to understand the context. Then **use `AskUserQuestion`** to ask: "What's the package name, purpose, and distribution target (MELPA / GNU ELPA / private)? [If any .el files found: I see [filename] — is this an existing project to bootstrap docs for, or a new one?]"
2. Run all-aboard (or adr-create → spec-create → threat-model-create)
3. Verify CLAUDE.md exists with project memories
4. Ensure it captures: package prefix, target Emacs version, dependencies,
   distribution target (MELPA/GNU ELPA/private), key ADRs

### Phase 2: Scaffold project structure

Run the init script or manually create the structure. You'll find complete
package structure guidance in
[references/elisp-package-architecture.md](references/elisp-package-architecture.md).

Required project structure:
- Main .el file with lexical-binding header
- Test directory with Buttercup or ERT tests
- CI/CD pipeline (.github/workflows/ci.yml)
- Eask or Cask configuration
- Documentation (README, CHANGELOG, LICENSE)
- Quality tooling (.dir-locals.el, .gitignore)

### Phase 3: Write the package — guardrails

When writing elisp code, always enforce these rules:

**Naming — MANDATORY:**
- Every global symbol: `<package-name>-` prefix
- Private symbols: `<package-name>--` double-dash
- Predicates end in `-p`, hooks in `-hook`

**Security — MANDATORY:**
- NEVER `shell-command` with concatenated user input
- ALWAYS prefer `call-process` with explicit args
- NEVER `make-temp-name` — use `make-temp-file`
- NEVER `eval` or `read` untrusted data
- Validate file paths against traversal

**Documentation — MANDATORY:**
- Every public function has a docstring
- First line: imperative, complete sentence, max 67 chars
- Arguments in UPPERCASE
- File has `;;; Commentary:` section

**Testing — MANDATORY:**
- Write Buttercup tests (primary) or ERT (secondary)
- Test interactive commands, buffer manipulation, modes
- Configure undercover.el for coverage
- Tests pass in `emacs -Q --batch`

### Phase 4: Validate with quality gates

Run [scripts/elisp-check.sh](scripts/elisp-check.sh) for automated validation.

All blocking gates must pass:
- Byte-compile clean (strict warnings-as-errors)
- Package loads in clean Emacs
- checkdoc passes
- package-lint passes
- relint passes
- Tests pass
- Security audit complete

### Phase 5: Configure CI/CD

Read [references/elisp-ci-quality-gates.md](references/elisp-ci-quality-gates.md)
for complete pipeline configuration. Test against Emacs 29.4, 30.1, and snapshot.

### Phase 6: Prepare for distribution

Read [references/elisp-ci-quality-gates.md](references/elisp-ci-quality-gates.md)
for MELPA/GNU ELPA/NonGNU ELPA submission requirements.

## Reference files

| File | When to read |
|------|-------------|
| [elisp-coding-conventions.md](references/elisp-coding-conventions.md) | Writing elisp |
| [elisp-security-hardening.md](references/elisp-security-hardening.md) | Security review |
| [elisp-testing-frameworks.md](references/elisp-testing-frameworks.md) | Writing tests |
| [elisp-linting-tools.md](references/elisp-linting-tools.md) | Quality checks |
| [elisp-package-architecture.md](references/elisp-package-architecture.md) | Package structure |
| [elisp-ecosystem-integration.md](references/elisp-ecosystem-integration.md) | Integrations |
| [elisp-ci-quality-gates.md](references/elisp-ci-quality-gates.md) | CI/CD setup |
| [quality-gates-checklist.md](references/quality-gates-checklist.md) | Final validation |

## Writing Style

Apply `natural-writing-style` to all generated documentation, CLAUDE.md entries, and README content produced by this skill.

State what was scaffolded and what was verified. Don't claim the package is ready for MELPA unless you've run package-lint, checkdoc, and byte-compile clean. List what gates passed and what still needs attention.

## Edge cases

- **Single vs multi-file**: Multi-file needs `<pkg>-pkg.el` descriptor
- **Optional dependencies**: Use `(require 'pkg nil t)` with declare-function
- **Emacs version features**: Guard with `(fboundp 'fn)`
- **GNU ELPA**: Requires FSF copyright assignment for all contributors
