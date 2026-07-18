---
name: choose-tests
description: Select optimal test strategy based on change type and system capabilities. Use when validating code changes or determining CI strategy.
allowed-tools: Read Glob Grep
---

# Choose Test Strategy

## Quick Start

1. **Check what changed** — `git diff --name-only HEAD~1` or `git status`
2. **Identify change type** — syntax/type, core logic, security, integration, build/config, or database
3. **Pick from the decision matrix** — cross-reference change type with memory tier
4. **Run primary strategy**, then secondary validation before committing

## When to Use This Skill

- You've just made a change and aren't sure which test command to run
- You're on a memory-constrained machine and need to avoid OOM during `make test`
- You want the fastest feedback loop that still gives adequate confidence for this change type
- You're setting up a pre-commit validation step and need to choose the right target
- The default test command is too slow for the kind of change you're making
- You're switching between codebases with different test conventions and need a quick orientation

Analyzes the type of changes you're making and system constraints to recommend:
- Appropriate test commands for the current changes
- Validation strategy based on development area
- Incremental vs thorough testing approach

## Input Assessment

### Change Type Detection
Analyze current changes to categorize (don't skip this step):
- **Syntax/Type changes**: Refactoring, type updates, interface changes
- **Core logic**: Business logic, algorithms, security functions
- **New features**: Adding new functionality or capabilities
- **Bug fixes**: Targeted fixes for specific issues
- **Build/config**: Cargo.toml, build system, configuration
- **Database/schema**: SurrealDB, migrations, schema changes

### System Context
- Available memory (from assess-system)
- Time constraints (rapid iteration vs thorough validation)
- Development area (core, security, integration, UI)

## Decision Matrix

### By Change Type

| Change Type | Quick Validation (30s) | Development (2min) | Full Suite (5-10min) |
|-------------|------------------------|-------------------|------------------------|
| **Syntax/Type changes** | `make check` | `make dev` | `make ci-fast` |
| **Core logic** | `cargo test -p <crate>` | `make test-core` | `make test-integration` |
| **Security algorithms** | `cargo test -p noelle-behavioral` | `make test-behavior` | `make test` |
| **Integration points** | `make dev` | `make test-integration` | `make test` |
| **New features** | `make dev` | `make ci-fast` | `make test && make test-behavior` |
| **Bug fixes** | Target specific test | `make test-core` | Area-specific full suite |
| **Build/config** | `make build-fast` | `make ci-fast` | `make clean && make test` |

### By Development Area

| Area | Recommended Primary | Secondary Validation |
|------|-------------------|---------------------|
| **Core system** | `make dev` | `make ci-fast` |
| **Security analysis** | `make test-behavior` | `make test-integration` |
| **Integration** | `make test-integration` | `make test` |
| **Database** | `cargo test -p noelle-graph` | Skip failing enum tests |

### By Memory Constraints

| Memory | Primary Strategy | Fallback |
|--------|-----------------|----------|
| **4-8GB** | Targeted crate testing | `make dev` |
| **8-16GB** | `make ci-fast` | `make test-core` |
| **16GB+** | `make test` | Parallel workflows |

## Execution Steps

1. **Assess Changes**:
   ```bash
   git status
   git diff --name-only HEAD~1
   ```

2. **Choose Primary Strategy**:
   Based on change type and system capacity -- you'll want to match the risk level

3. **Select Secondary Validation**:
   For thorough validation before commit -- it's worth the extra time

4. **Execute Targeted Testing**:
   ```bash
   # Example for core logic changes on 8GB system
   cargo test -p noelle-core --profile=fast-test
   make test-core
   ```

## Success Criteria

- [ ] Change type identified correctly
- [ ] System constraints considered
- [ ] Primary test strategy selected
- [ ] Secondary validation planned
- [ ] Execution commands provided

## Example Output

```
Test Strategy for Core Logic Changes:
- Change Type: Core algorithm modifications
- System: 8GB RAM available
- Primary: cargo test -p noelle-core --profile=fast-test
- Secondary: make test-core
- Pre-commit: make ci-fast
- Estimated Time: 2-3 minutes total
```
