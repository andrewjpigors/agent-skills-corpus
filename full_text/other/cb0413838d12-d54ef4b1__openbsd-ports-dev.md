---
name: openbsd-ports-dev
description: |
  Port review and porting standards for OpenBSD based on 11677 analyzed
  port reviews from openbsd-ports mailing list (1900-19-37 to Wed, 31 Aug 2022 21:17:38 +0000). Covers
  quality gates for Makefiles, PLIST validation, patch guidelines,
  build patterns, and maintainer preferences. Use when reviewing OpenBSD
  ports, creating new ports, updating existing ports, fixing port issues,
  or when user mentions OpenBSD ports, bsd.port.mk, or port submissions.
version: 1.0.0
triggers:
  - reviewing OpenBSD ports
  - creating new ports for OpenBSD
  - updating existing ports
  - preparing port submissions
  - reviewing port Makefiles
  - fixing port issues
---

# OpenBSD Ports Development

Based on 11677 port reviews from openbsd-ports mailing list (1900-19-37 to Wed, 31 Aug 2022 21:17:38 +0000).

## Quick Start

Before you submit any port:

1. **Makefile structure** — Follow bsd.port.mk conventions
2. **PLIST completeness** — All installed files tracked
3. **Bulk build test** — Must build cleanly
4. **DESCR file** — Clear, concise description
5. **Patch format** — Unified diffs with proper headers
6. **WANTLIB tracking** — Accurate library dependencies
7. **Security review** — CVE tracking, pledge/unveil where applicable

## When to Use This Skill

Use this when you're:

- Creating new ports for OpenBSD
- Updating existing ports to new versions
- Reviewing port submissions
- Fixing issues in existing ports
- Understanding ports infrastructure
- Preparing patches for upstream

## Core Review Workflow

### Step 1: Initial Check

```bash
# Verify port structure
cd /usr/ports/category/portname
ls -la  # Should see: Makefile, pkg/, distinfo, patches/ (if needed)
```

### Step 2: Makefile Review

Check variable ordering, WANTLIB, and LIB_DEPENDS. See [Makefile Patterns](references/makefile-patterns.md).

### Step 3: Build Test

```bash
make clean
make
make fake
```

### Step 4: PLIST Validation

Make sure all files are tracked. See [PLIST Guidelines](references/plist-guidelines.md).


## Key Quality Gates

Top quality requirements (by frequency):

- **Build and compilation** — Must compile cleanly with make (2021 occurrences)
- **Patch format and structure** — Unified diffs with proper headers (1292 occurrences)
- **Testing** — Include unit and integration tests (927 occurrences)
- **Makefile structure** — Follow bsd.port.mk conventions, proper variable ordering (1342 combined occurrences)
- **Code quality** — Pass linting and style checks (693 occurrences)
- **PLIST tracking** — All installed files must be tracked (727 combined occurrences)
- **Description file required** — Clear, concise DESCR file (421 occurrences)

See [Common Mistakes](references/common-mistakes.md) for detailed examples you'll want to avoid.

## Detailed Guidance

For detailed information you'll need, see:

- [Makefile Patterns](references/makefile-patterns.md) — Detailed templates and variable ordering
- [PLIST Guidelines](references/plist-guidelines.md) — PLIST generation and validation
- [Patch Guidelines](references/patch-guidelines.md) — Creating patches for upstream
- [Common Mistakes](references/common-mistakes.md) — Before/after examples
- [Build System](references/build-system.md) — CONFIGURE_ARGS, WANTLIB, modules

## Writing Style

Apply `natural-writing-style` to all review comments and port submission feedback.

Be specific: when flagging a PLIST or Makefile issue, point to the exact variable or file list entry that's wrong. Don't claim a port is ready to commit unless you've run `make fake` and verified the PLIST matches. Mention the bsd.port.mk rule name when relevant.

## Validation

Before you submit, run these validation scripts:

```bash
# Check port structure
bash "$HOME/.claude/skills/openbsd-ports-dev/scripts/check-port.sh" /path/to/port

# Validate Makefile
bash "$HOME/.claude/skills/openbsd-ports-dev/scripts/check-makefile.sh" Makefile

# Check PLIST
bash "$HOME/.claude/skills/openbsd-ports-dev/scripts/check-plist.sh" pkg/PLIST
```
