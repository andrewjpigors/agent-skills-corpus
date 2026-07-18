---
name: openbsd-base-dev
description: |
  Code review and coding standards for OpenBSD base system development.
  Based on analysis of 846 code reviews from openbsd-tech
  mailing list (+0000 to Wed, 30 Mar 2016 14:31:13 +0000). Covers quality gates, style rules,
  security patterns, API guidance, and developer preferences from 20+ years
  of OpenBSD development. Use when reviewing OpenBSD patches, writing code
  for OpenBSD base, or when user mentions openbsd-tech, style(9), or OpenBSD
  development standards.
version: 1.0.0
triggers:
  - reviewing OpenBSD base system code
  - writing C code for OpenBSD
  - following KNF style
  - OpenBSD kernel development
  - OpenBSD userland development
---

# OpenBSD Base System Development

Based on 846 code reviews from openbsd-tech mailing list (+0000 to Wed, 30 Mar 2016 14:31:13 +0000).

## Quick Start

Before you submit code:

1. **KNF compliance** — Follow style(9) exactly; don't guess
2. **Build cleanly** — No warnings with -Wall
3. **Security review** — Use err(3), check bounds, validate input
4. **API usage** — Use OpenBSD-specific APIs (strlcpy, arc4random, queue)
5. **Error handling** — Proper error reporting
6. **Testing** — Add regress tests if applicable

## When to Use This Skill

Use this when you're working on:

- Writing C code for OpenBSD's base system
- Reviewing patches for the base system
- Working with kernel or userland code
- Following KNF style guidelines

## Core Review Workflow

### Step 1: Style Check

```bash
# Check KNF compliance
bash scripts/check-knf.sh file.c
```

### Step 2: Build Test

```bash
cd /usr/src
make obj
make
```

### Step 3: Security Review

Make sure you've checked for proper error handling, bounds checking, and input validation. It's easy to miss an edge case here. See [Security Patterns](references/security-patterns.md).


## Key Quality Gates

Top quality requirements (by frequency):

- **Maintain proper socket locking and assertions** (10 occurrences)
- **All regression tests must pass before commit** (7 occurrences)
- **Memory safety** — Handle edge cases in buffer/memory allocation and ensure resource cleanup on error paths (8 combined occurrences)
- **Minimize critical section scope** (4 occurrences)
- **RFC compliance verification** (3 occurrences)
- **Code quality** — Use const for static read-only structures, keep changes minimal and focused, and run static analysis tools (7 combined occurrences)
- **Manpage documentation must accompany feature additions** (2 occurrences)

See [Common Mistakes](references/common-mistakes.md) for detailed examples you'll want to avoid.

## Detailed Guidance

For detailed information you'll need, see:

- [KNF Style Guide](references/knf-style.md) — Detailed style(9) patterns
- [Security Patterns](references/security-patterns.md) — pledge(2), unveil(2), err(3)
- [API Guidelines](references/api-guidelines.md) — queue(3), arc4random(3), strlcpy(3)
- [Common Mistakes](references/common-mistakes.md) — Before/after examples

## Writing Style

Apply `natural-writing-style` to all review comments and patch feedback.

Review comments should be direct: say what's wrong and where, not just that something looks off. Don't claim a patch is ready for commit unless you've verified it builds clean and passes regress tests. Cite specific style(9) rule names when flagging KNF violations.

## Validation

Before you submit, run these validation scripts:

```bash
# Check KNF compliance
bash "$HOME/.claude/skills/openbsd-base-dev/scripts/check-knf.sh" file.c

# Validate style(9)
bash "$HOME/.claude/skills/openbsd-base-dev/scripts/check-style.sh" file.c
```
