---
name: troubleshoot-dev
description: Diagnose and resolve development environment issues. Use when tests fail, builds break, or performance degrades.
allowed-tools: Read Bash(cargo *) Bash(npm *) Bash(git *) Bash(docker *) AskUserQuestion
---

# Development Troubleshooting

You'll find systematic troubleshooting here for common development issues:
- Test failures and debugging strategies
- Build errors and compilation issues
- Performance problems and bottlenecks
- Database and integration issues
- Environment configuration problems

## Quick Start

1. Run `git diff HEAD~1 --name-only` and check `free -h` to gather context, then **use `AskUserQuestion`** to identify the issue category: "I see [recent changes to X / low memory / no obvious changes]. Is this a test failure, build error, performance issue, or environment problem? Any error message I should start with?"
2. Run the relevant diagnostic command (e.g., `cargo test -- --nocapture` for test failures, `free -h` for memory)
3. If nothing obvious turns up, escalate to a clean slate: `make clean && make build-fast`

## When to Use This Skill

- Tests are failing and you can't figure out why from the error output alone
- Build breaks after pulling changes or updating dependencies
- Performance degradation in the dev environment (slow builds, tests, or startup)
- Docker, database, or integration service issues blocking development

## Common Issue Categories

### 1. Test Failures

**Systematic Debugging Approach:**
```bash
# Run failing test with full output
cargo test -p <crate> <test-name> -- --nocapture

# Check for resource issues
make check-memory

# Clean and retry
make clean && cargo test -p <crate> <test-name>
```

**Specific Test Issues:**
- **SurrealDB enum serialization**: Known issue, use `cargo test -p noelle-core -p noelle-bus`
- **Integration test timeouts**: Use `--profile=fast-test` or target specific tests
- **Memory-related failures**: Reduce `CARGO_BUILD_JOBS`, use `make dev`

### 2. Build Errors

**Compilation Failures:**
```bash
# Clean build
make clean && make build-fast

# Check dependency conflicts
cargo tree --duplicates

# Update dependencies if needed
cargo update
```

**Linker Issues:**
```bash
# Remove problematic linker settings
# Check .cargo/config.toml for linker configurations

# Use system default linker
cargo build --config target.x86_64-unknown-linux-gnu.linker=""
```

### 3. Performance Issues

**Slow Builds:**
```bash
# Check system resources
make check-memory

# Reduce build parallelization
export CARGO_BUILD_JOBS=2

# Use faster profiles
make build-fast instead of make build
```

**Slow Tests:**
```bash
# Use targeted testing
cargo test -p <crate> --profile=fast-test

# Skip problematic tests temporarily
cargo test -- --skip <test-name>
```

### 4. Database Issues

**SurrealDB Problems:**
```bash
# Skip database tests during development
cargo test -p noelle-core -p noelle-bus

# Known enum serialization issues in noelle-graph
# These are pre-existing and not blocking core functionality
```

### 5. Environment Issues

**Missing Dependencies:**
```bash
# Install required tools
# For integration tests: trivy, grype
# Check tool availability with which <tool>

# Update system packages if needed
```

## Troubleshooting Workflows

### When Tests Suddenly Won't Pass

1. **Check Recent Changes:**
   ```bash
   git diff HEAD~1 --name-only
   git status
   ```

2. **Isolate the Issue:**
   ```bash
   # Test specific component
   cargo test -p <affected-crate> -- --nocapture
   ```

3. **Check Environment:**
   ```bash
   make check-memory
   free -h
   ```

4. **Clean Slate Approach:**
   ```bash
   make clean
   cargo update
   make build-fast
   ```

### When Builds Won't Complete Mysteriously

1. **Full Clean:**
   ```bash
   make deep-clean
   rm -rf target/
   cargo clean
   ```

2. **Incremental Rebuild:**
   ```bash
   make check        # Quick syntax check
   make build-fast   # Optimized build
   make dev         # Core functionality
   ```

3. **Dependency Check:**
   ```bash
   cargo tree --duplicates
   cargo update
   ```

### When Performance Degrades

1. **Resource Assessment:**
   ```bash
   /assess-system
   ```

2. **Build Analysis:**
   ```bash
   /analyze-build
   ```

3. **Memory Optimization:**
   ```bash
   /memory-optimize <!-- voice-ok -->
   ```

## Issue-Specific Debugging

### SurrealDB Enum Serialization Errors
```bash
# Expected behavior: Known issue, not blocking
# Workaround: Test core functionality without noelle-graph
cargo test -p noelle-core -p noelle-bus

# These tests should pass: 45 bus tests + 173 core tests
```

### Integration Test Failures
```bash
# Use targeted testing
cargo test -p noelle-integration-tests <specific-test> --profile=fast-test -- --nocapture

# Check for missing tools
which trivy
which grype
```

### Memory-Related Build Failures
```bash
# Immediate fix
export CARGO_BUILD_JOBS=1

# Check swap usage
free -h
swapon --show

# Use memory-efficient alternatives
make dev instead of make test
```

### Dependency Conflicts
```bash
# Check for version conflicts
cargo tree --duplicates

# Update problematic dependencies
cargo update <dependency-name>

# Force clean rebuild
make clean && cargo build
```

## Recovery Strategies

### Nuclear Options (When All Else Fails)

```bash
# Complete environment reset
make deep-clean
rm -rf target/ ~/.cargo/registry/cache/
cargo clean

# Rebuild from scratch
cargo fetch
make build-fast
```

### Partial Recovery

```bash
# Clean incremental caches only
rm -rf target/debug/incremental
rm -rf target/release/incremental

# Clean specific crate
cargo clean -p <problematic-crate>
```

## Success Criteria

- [ ] Issue category identified
- [ ] Root cause diagnosed
- [ ] Appropriate fix applied
- [ ] Functionality restored
- [ ] Prevention measures noted

## Prevention Strategies

### Regular Maintenance
```bash
# Weekly cleanup
make clean

# Monthly dependency updates
cargo update

# Monitor resource usage
make check-memory
```

### Development Best Practices
- Don't run the full suite when targeted testing during development is faster
- Monitor memory usage on constrained systems
- Keep incremental builds enabled
- It's worth using appropriate build profiles for the task

## Example Troubleshooting Session

```bash
# Issue: Tests suddenly failing
git diff HEAD~1  # Check recent changes

# Issue: Memory error during build
export CARGO_BUILD_JOBS=1
make clean && make build-fast

# Issue: SurrealDB serialization errors
# Known issue - test core functionality instead
cargo test -p noelle-core -p noelle-bus

# Issue: Integration test timeout
cargo test -p noelle-integration-tests specific_test --profile=fast-test
```
