---
name: memory-optimize
description: Configure memory usage for optimal development performance. Use on memory-constrained systems, when experiencing swap usage, or build failures.
allowed-tools: Read Bash(free) Bash(swapon) Bash(swapoff)
---

# Memory Optimization

Here's how it tunes your development environment for available system memory:
- Configures build parallelization for memory capacity
- Adjusts development workflows for memory constraints
- Provides memory-efficient alternatives
- Monitors and prevents memory exhaustion

## When to Use This Skill

- Builds failing with OOM kills or running into swap thrashing
- Working on a memory-constrained machine (CI runners, VMs, older hardware)
- Compiling large Rust or C++ projects that exhaust RAM during linking
- Needing to tune cargo, make, or webpack parallelism for available memory

## Quick Start

1. Run `free -h` to see available memory
2. Set `CARGO_BUILD_JOBS` based on your tier (2 for 4-8GB, 3 for 8-16GB, unset for 16GB+)
3. Swap heavy commands for lighter alternatives (e.g., `cargo test -p <crate>` instead of `make test`)
4. Add your settings to `~/.bashrc` so they persist

## System Memory Assessment

### 1. **Check Available Memory**
```bash
make check-memory
# or manually:
free -h
cat /proc/meminfo | grep MemAvailable
```

### 2. **Identify Memory Pressure**
```bash
# Check for swap usage
swapon --show
free -h | grep Swap

# Monitor during build
# (observe memory usage during compilation)
```

## Memory Configuration Strategies

### Low Memory Systems (4-8GB)

**Build Configuration:**
```bash
# Set conservative build jobs
export CARGO_BUILD_JOBS=2

# Use memory-efficient profiles
cargo build --profile=fast-test
```

**Development Workflow:**
```bash
# Primary iteration - memory efficient
make dev

# Avoid memory-intensive commands
# Instead of: make test
# Use: cargo test -p <crate> --profile=fast-test
```

**Environment Variables:**
```bash
# Add to shell profile
export CARGO_BUILD_JOBS=2
export RUST_MIN_STACK=8388608  # 8MB stack size
```

### Medium Memory Systems (8-16GB)

**Build Configuration:**
```bash
# Moderate parallelization
export CARGO_BUILD_JOBS=3

# Use balanced profiles
cargo build --profile=integration
```

**Development Workflow:**
```bash
# Primary iteration
make ci-fast

# Secondary validation
make test-integration
```

### High Memory Systems (16GB+)

**Build Configuration:**
```bash
# Use default parallelization
unset CARGO_BUILD_JOBS  # Let Cargo decide

# Use all available profiles
make test  # Full test suite acceptable
```

**Development Workflow:**
```bash
# Full workflows available
make test
make test-behavior
# Parallel development acceptable
```

## Memory-Efficient Alternatives

You don't always need the full workspace commands. Here are lighter options.

**Memory-Heavy Command** → **Memory-Efficient Alternative**
- `make test` → `make test-core`
- `make test-integration` → `cargo test -p noelle-integration-tests <specific-test>`
- `make test-behavior` → `cargo test -p noelle-behavioral --profile=fast-test`
- `cargo build` → `cargo build --profile=fast-test`

### Targeted Testing Strategies

```bash
# Test specific crate instead of workspace
cargo test -p noelle-core --profile=fast-test

# Test specific functionality
cargo test -p noelle-integration-tests behavioral_analysis --profile=fast-test

# Use lighter test profiles
cargo test --profile=integration
```

## Memory Monitoring

### During Development
```bash
# Check memory before starting work
free -h

# Monitor memory usage during builds
# (This is observational - watch memory usage)
```

### Build Memory Management
```bash
# Clear build caches if memory constrained
make clean

# Use incremental builds to reduce memory
# (Already configured in .cargo/config.toml)
```

## Troubleshooting Memory Issues

If things aren't going well, here are the most common problems and fixes.

### Out of Memory (OOM) Errors
```bash
# Immediate fix: Reduce build parallelization
export CARGO_BUILD_JOBS=1

# Clear memory-intensive caches
make clean
rm -rf target/debug/incremental

# Restart with conservative settings
make build-fast
```

### Swap Thrashing
```bash
# Check swap usage
swapon --show
free -h

# Reduce memory pressure
export CARGO_BUILD_JOBS=2

# Use targeted commands
make dev instead of make test
```

### Build Failures Due to Memory

You'll need the nuclear option if nothing else works:
```bash
# Nuclear option: Clean everything
make deep-clean

# Restart with minimal parallelization
export CARGO_BUILD_JOBS=1
make build-fast

# Gradually increase if successful
export CARGO_BUILD_JOBS=2
```

## Configuration Persistence

It's worth making these settings permanent so you won't have to reconfigure after restarting.

### Shell Profile Configuration
```bash
# Add to ~/.bashrc or ~/.zshrc based on system memory
echo 'export CARGO_BUILD_JOBS=2' >> ~/.bashrc  # for 4-8GB systems
echo 'export CARGO_BUILD_JOBS=3' >> ~/.bashrc  # for 8-16GB systems
```

### Project-Specific Configuration
```bash
# Create .env file in project root
echo 'CARGO_BUILD_JOBS=2' > .env

# Or add to .cargo/config.toml (already configured)
```

## Success Criteria

- [ ] Available memory assessed
- [ ] Build parallelization optimized
- [ ] Development workflow adapted
- [ ] Memory monitoring in place
- [ ] Backup strategies defined

## Memory Optimization Checklist

### For 4-8GB Systems
- [ ] `CARGO_BUILD_JOBS=2` configured
- [ ] Primary workflow: `make dev`
- [ ] Avoid `make test` (use targeted testing)
- [ ] Use `--profile=fast-test` for iterations
- [ ] Monitor swap usage

### For 8-16GB Systems
- [ ] `CARGO_BUILD_JOBS=3-4` configured
- [ ] Primary workflow: `make ci-fast`
- [ ] Use `make test-integration` for validation
- [ ] Full `make test` only when necessary

### For 16GB+ Systems
- [ ] Default build jobs acceptable
- [ ] All workflows available
- [ ] Parallel development possible
- [ ] Can run full test suites

## Example Output

```
Memory Optimization for 8GB System:
- Available Memory: 7.2GB
- Recommended CARGO_BUILD_JOBS: 3
- Primary Workflow: make ci-fast (2-3 minutes)
- Avoid: make test (memory intensive)
- Use: cargo test -p <crate> --profile=fast-test
- Configuration: Added to ~/.bashrc
- Monitor: Check swap usage during builds
```
