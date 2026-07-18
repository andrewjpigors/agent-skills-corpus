---
name: analyze-build
description: Analyze build performance and recommend optimizations. Use when builds are slow, after configuration changes, or for performance optimization.
allowed-tools: Read Glob Bash(time *) Bash(cargo *) Bash(npm *) Bash(make *)
---

# Analyze Build Performance

## Quick Start

1. **Establish a baseline** — run `time make clean && time make build` and record the numbers
2. **Check memory** — `make check-memory` or `free -h` to see available RAM
3. **Inspect dependency tree** — `cargo tree | head -20` to spot heavy deps
4. **Compare before/after** — after any change, re-run the timing commands and diff the results

## When to Use This Skill

- Builds are taking noticeably longer than they used to
- You've just changed `Cargo.toml`, `Cargo.lock`, or `.cargo/config.toml` and want to verify impact
- You're setting up a new development machine and need to configure build jobs for the available RAM
- A CI pipeline is timing out and you suspect the build phase
- You want to establish performance baselines before a major dependency update
- You're debugging an OOM kill during compilation and need to find the high-memory crates

Here's what it covers for build performance analysis:
- Identifies build time bottlenecks
- Analyzes compilation resource usage
- Recommends optimization strategies
- Tracks performance changes over time

## Execution Steps

### 1. **Current Performance Baseline**
```bash
# Analyze current build artifacts and performance
make analyze-build

# Get detailed timing information
time make clean && time make build-fast
```

### 2. **Resource Usage Analysis**
```bash
# Check memory usage during build
make check-memory

# Monitor resource usage during compilation
# (This step is observational during actual builds)
```

### 3. **Build Configuration Audit**
```bash
# Review current Cargo configuration
cat .cargo/config.toml

# Check build profiles
grep -A 10 "\[profile\." Cargo.toml
```

### 4. **Dependency Analysis**
```bash
# Check for unnecessary dependencies
cargo tree | head -20

# Analyze feature flags
cargo tree -f "{p} {f}"
```

## Performance Metrics

### Build Time Targets
- **Quick check**: < 30 seconds (`make check`)
- **Development build**: 30-90 seconds (`make dev`)
- **Fast build**: 1-2 minutes (`make build-fast`)
- **Full build**: 3-5 minutes (`make build`)
- **Clean build**: 5-10 minutes

### Memory Usage Targets
- **4GB systems**: Won't need swap if configured right
- **8GB systems**: Comfortable development experience
- **16GB+ systems**: Can run parallel builds

### Compilation Jobs Optimization
- **4-8GB RAM**: `CARGO_BUILD_JOBS=2-3`
- **8-16GB RAM**: `CARGO_BUILD_JOBS=3-4`
- **16GB+ RAM**: `CARGO_BUILD_JOBS=auto` (default)

## Common Optimizations

### 1. **Dependency Optimization**
```bash
# Review Tokio features (already tuned)
grep -A 5 "tokio.*features" Cargo.toml

# Check SurrealDB features (already tuned)
grep -A 3 "surrealdb.*features" Cargo.toml
```

### 2. **Build Profile Tuning**
```bash
# Fast test profile optimization
grep -A 5 "\[profile.fast-test\]" Cargo.toml

# Integration profile optimization
grep -A 5 "\[profile.integration\]" Cargo.toml

# Dep-override coverage — every profile the repo uses should have a
# matching [profile.<p>.package."*"] block, otherwise deps rebuild
# under different flags per mode and target/ holds multiple copies
grep -E '^\[profile\.[a-z_-]+(\.package\."\*")?\]' Cargo.toml
```

**Build-cache duplication check.** Cargo scopes `[profile.<p>.package."*"]` to the profile that declares it — overrides don't inherit. If only `[profile.dev.package."*"]` is declared, `cargo test` and `cargo bench` rebuild every dep under different flags. Verify:

```bash
ls target/debug/.fingerprint/ 2>/dev/null \
  | grep -oE '^[a-z0-9_-]+-[a-f0-9]{16}$' \
  | sed 's/-[a-f0-9]*$//' | sort | uniq -c | sort -rn | head
```

Any row with count > 1 is a duplicated dep. Fix by mirroring the override across every profile in use (`test`, `bench`, plus any custom profiles that inherit from them):

```toml
[profile.test.package."*"]
opt-level = 1
debug = false

[profile.bench.package."*"]
opt-level = 1
debug = false
```

### 3. **Incremental Compilation**
```bash
# Verify incremental compilation is enabled
grep incremental .cargo/config.toml
```

## Troubleshooting Slow Builds

### Common Issues and Solutions

**Issue**: Builds taking > 10 minutes — you can't ignore this
```bash
# Check memory constraints
make check-memory
# Reduce parallel jobs if memory-constrained
export CARGO_BUILD_JOBS=2
```

**Issue**: Random build failures
```bash
# Clean and rebuild
make clean && make build-fast
# Check for dependency conflicts
cargo tree --duplicates
```

**Issue**: High memory usage
```bash
# Check current memory usage
free -h
# Adjust build jobs
export CARGO_BUILD_JOBS=1
```

**Issue**: Slow incremental builds — it's usually a stale cache
```bash
# Clean incremental cache
rm -rf target/debug/incremental
# Rebuild with fresh cache
make build-fast
```

## Performance Comparison

### Before/After Analysis
```bash
# Establish baseline
time make clean && time make build > build-before.log 2>&1

# Apply optimizations
# ... make changes ...

# Measure improvements
time make clean && time make build > build-after.log 2>&1

# Compare results
diff build-before.log build-after.log
```

## Success Criteria

- [ ] Baseline performance established
- [ ] Resource bottlenecks identified
- [ ] Optimization opportunities found
- [ ] Target performance metrics defined
- [ ] Improvement strategy recommended

## Optimization Recommendations

Based on analysis, you'll want to provide recommendations like:

### Memory Optimization
- Adjust `CARGO_BUILD_JOBS` for system capacity
- Enable/disable specific features
- Consider build profile adjustments

### Speed Optimization
- Use fast-test profile for iteration
- Enable incremental compilation
- Trim dependency features

### Resource Management
- Configure appropriate build targets
- Balance parallelization with memory usage
- Use targeted testing strategies

## Example Output

```
Build Performance Analysis:
- Current clean build time: 5m 32s
- Incremental build time: 1m 15s
- Memory usage peak: 6.2GB
- Parallel jobs: 4
- Bottleneck: SurrealDB compilation (2m 15s)

Recommendations:
1. Build time within target ranges
2. Memory usage appropriate for 8GB system
3. Consider caching SurrealDB compilation
4. Use make dev for faster iteration (45s vs 5m32s)
```