---
name: dev-iteration
description: Execute optimal development iteration workflow with testing and validation. Use when actively developing, implementing features, or debugging issues.
allowed-tools: Read Write Edit Bash(cargo *) Bash(npm *) Bash(pytest *) Bash(go *)
---

# Development Iteration Cycle

## Quick Start

1. **Run `assess-system`** to confirm memory tier and recommended workflow
2. **Check what changed** — `git status` and `git diff --name-only`
3. **Pick the right loop** — `make dev` for core, `cargo test -p <crate>` for targeted, `make test-behavior` for security
4. **Code → test → repeat** until the feature works, keeping the cycle under 2 minutes

Provides a structured approach to development iteration that won't waste your time:
- Maximizes feedback speed
- Ensures code quality
- Adapts to system constraints
- Minimizes context switching

## When to Use This Skill

- Actively developing features or fixing bugs in an iterative loop
- Setting up a rapid build-test-fix cycle for a new codebase
- Debugging failures that need systematic iteration with fast feedback
- Switching between codebases and needing to re-establish your dev loop

## Standard Development Loop

### 1. **Assessment Phase**
```bash
# Quick system check (if not done recently)
make check-memory

# Understand current state
git status
git diff --name-only
```

**Before your first iteration on an unfamiliar project, check that the build cache is healthy.** A project that's rebuilding the world on every change usually isn't doing so because of your code — it's stale cache hygiene. Three checks:

```bash
# Disk not full (target dirs at 95%+ fail with "No space left on device")
df -h .

# Deps aren't duplicated across profile lineages (count > 1 = trouble)
ls target/debug/.fingerprint/ 2>/dev/null \
  | grep -oE '^[a-z0-9_-]+-[a-f0-9]{16}$' \
  | sed 's/-[a-f0-9]*$//' | sort | uniq -c | sort -rn | head

# Toolchain pinned? Unpinned means rustup update silently invalidates
# the entire target/ dir.
ls rust-toolchain.toml 2>/dev/null || echo "NOT PINNED"
```

For Rust projects specifically: if deps are duplicated, the fix is declaring `[profile.test.package."*"]` / `[profile.bench.package."*"]` mirrors of the `[profile.dev.package."*"]` override so all modes share one artifact lineage. The `rust-compile-memory` skill's refactoring-strategies reference covers this in detail.

### 2. **Rapid Iteration Cycle**

**For Core Changes** (30-90 seconds):
```bash
# Make your changes
# Then validate quickly
make dev
# Repeat until feature works
```

**For Security Changes** (1-2 minutes):
```bash
# Make your changes
# Then validate security-specific functionality
cargo test -p noelle-behavioral --profile=fast-test
make test-behavior
```

**For Integration Changes** (2-3 minutes):
```bash
# Make your changes
# Then validate integration points
make test-integration
```

### 3. **Feature Completion Validation**

Once feature is working, you'll want a full check:
```bash
make ci-fast  # 2-5 minute full validation
```

### 4. **Pre-Commit Validation**

Before committing, based on change impact:
- **Core changes**: `make ci-fast`
- **Security changes**: `make test-behavior`
- **Integration changes**: `make test-integration`
- **Major features**: `make test`

## Memory-Adapted Workflows

### Low Memory (4-8GB)
```bash
# Primary iteration
make dev

# Feature validation
cargo test -p <relevant-crate> --profile=fast-test

# Pre-commit
make ci-fast
```

### Medium Memory (8-16GB)
```bash
# Primary iteration
make ci-fast

# Feature validation
make test-integration

# Pre-commit
make test-behavior
```

### High Memory (16GB+)
```bash
# Primary iteration
make test

# Feature validation
Parallel workflows acceptable

# Pre-commit
make test && make test-behavior
```

## Development Area Workflows

### Core System Development
1. **Quick feedback**: `make check` (15-30 seconds)
2. **Core validation**: `make dev` (30-90 seconds)
3. **Full suite**: `make ci-fast` (2-5 minutes)
4. **Pre-commit gate**: `make test` (thorough, run before pushing)

### Security Development
1. **Quick feedback**: `cargo test -p noelle-behavioral --profile=fast-test`
2. **Security validation**: `make test-behavior` (CPU intensive)
3. **Integration check**: `make test-integration`
4. **Full regression sweep**: `make test && make test-behavior`

### Bug Fixes
1. **Target specific test**: `cargo test -p <crate> <test-name> -- --nocapture`
2. **No regressions**: `make test-core`
3. **Security validation** (if security-related): `make test-behavior`
4. **Confirm the fix sticks**: `make ci-fast` (catches side effects)

## Success Criteria

- [ ] Rapid feedback loop established (< 2 minutes)
- [ ] Change-appropriate validation selected
- [ ] Memory constraints respected
- [ ] Feature completion criteria defined
- [ ] Pre-commit strategy planned

## Writing Style

Development status updates guide iteration decisions. Apply `natural-writing-style` to all output:

- Be precise about build/test results — report exact commands run and their output
- Don't claim features are "working" or "complete" unless tests pass and you've verified behavior
- Use contractions naturally; keep the tone conversational during rapid iteration
- State what you built, what you tested, what you didn't verify yet
- When recommending workflow changes, cite specific metrics — "make dev takes 45s vs make test at 8m" beats "this is faster"

## Debugging Workflow

When tests fail, don't panic:
```bash
# Debug specific failure
cargo test -p <crate> <failing-test> -- --nocapture

# Check resource issues
make check-memory

# Clean rebuild if mysterious failures
make clean && make build-fast
```

## Example Session

```bash
# 1. Start session
/assess-system

# 2. Begin iteration
/dev-iteration
# -> Recommends: make dev for core changes

# 3. Code -> Test cycle
# Make changes...
make dev  # 45 seconds - passes
# More changes...
make dev  # 52 seconds - passes

# 4. Feature complete
make ci-fast  # 3m 15s - full validation

# 5. Ready to commit
```
