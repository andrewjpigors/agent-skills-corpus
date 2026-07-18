---
name: rust-compile-memory
description: >-
  Profiles Rust compilation memory usage with rustc nightly and measureme tools,
  identifies high-memory patterns (monomorphization, large types, LLVM bottlenecks),
  and refactors code to reduce compilation RSS. Use when Rust builds trigger OOM
  killer or consume excessive memory. Triggers: "compilation memory", "rustc OOM",
  "reduce compile memory", "profile compilation".
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
compatibility: >-
  Requires Rust nightly, Linux/macOS (heaptrack Linux-only), Nix recommended.
  Works with any Cargo workspace. Creates flake.nix if missing.
allowed-tools: Bash(cargo * rustc * nix *) Read Edit Write Glob Grep
---

# Rust Compilation Memory Profiling and Optimization

When rustc starts eating gigabytes of RAM and the OOM killer shows up, you'll need to profile what's consuming memory during compilation and refactor the code to bring it down.

## Quick Start

Here's the workflow when compilation memory spirals out of control:

1. **Switch to nightly** — Set up via Nix flake or rustup
2. **Profile compilation** — Use `-Z self-profile` and heaptrack to establish baseline
3. **Refactor automatically** — Apply known patterns to reduce memory (split types, reduce monomorphization)
4. **Verify improvements** — Re-profile and compare RSS reduction

## When to Use This Skill

Use when you encounter:

- **OOM killer terminating rustc** during builds
- **RSS > 8GB** for compilation on systems with limited memory
- **Incremental builds failing** due to memory pressure
- **CI builds crashing** with out-of-memory errors
- **Multi-crate workspaces** where some crates consume excessive memory
- **Generic-heavy code** causing monomorphization explosion

## Workflow

### Phase 1: Environment Setup

**Switch to Rust nightly:**

Check for existing Nix configuration:

```bash
if [ -f flake.nix ]; then
  echo "Found flake.nix, will modify"
elif [ -f shell.nix ]; then
  echo "Found shell.nix, will create flake.nix"
else
  echo "No Nix config, creating flake.nix"
fi
```

**If no flake.nix exists, create one:**

```nix
{
  description = "Rust project with nightly for compilation profiling";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, rust-overlay, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };
        rustToolchain = pkgs.rust-bin.nightly.latest.default.override {
          extensions = [ "rust-src" "rust-analyzer" ];
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            rustToolchain
            pkgs.heaptrack
            pkgs.cargo-llvm-lines
            pkgs.inferno  # flamegraph generation
          ];

          CARGO_BUILD_RUSTC = "${rustToolchain}/bin/rustc";
          RUSTC_WRAPPER = "";
        };
      }
    );
}
```

**If flake.nix exists, modify it:**

You'll need to add these to buildInputs:
- `pkgs.heaptrack` (Linux only, skip on macOS)
- `pkgs.cargo-llvm-lines`
- `pkgs.inferno`

Make sure the rust toolchain's set to nightly:
```nix
rustToolchain = pkgs.rust-bin.nightly.latest.default.override {
  extensions = [ "rust-src" ];
};
```

**Fallback for non-Nix environments:**

```bash
# Install nightly via rustup
rustup toolchain install nightly
rustup override set nightly

# Install tools
cargo install cargo-llvm-lines
cargo install inferno
# heaptrack: install via package manager (apt, brew, etc.)
```

### Phase 2: Baseline Profiling

**Pre-flight: check for things that silently invalidate the cache**

Before you profile, rule out the non-code causes of "everything rebuilds from scratch" — those will dominate the numbers and hide whatever you're actually trying to measure. Two quick checks:

1. **Disk free.** `df -h .` — when the partition holding `target/` passes ~95% full, builds fail with "No space left on device" which looks like OOM in downstream logs. `target/debug/incremental` is regeneratable cache and often the easiest win.
2. **Unpinned toolchain.** `ls rust-toolchain.toml 2>/dev/null` — if missing, `rustup update` silently invalidates every fingerprint. For a reproducible baseline you want a pinned `channel = "nightly-YYYY-MM-DD"` (see `references/refactoring-strategies.md`).
3. **Profile hash duplication.** `ls target/debug/.fingerprint/ | grep -oE '^[a-z0-9_-]+-[a-f0-9]{16}$' | sed 's/-[a-f0-9]*$//' | sort | uniq -c | sort -rn | head` — any dep with count > 1 means the repo is building it under multiple profile lineages (usually `cargo build` + `cargo test` + `cargo check`). Peak RSS is doubled and time is wasted. See [references/refactoring-strategies.md](references/refactoring-strategies.md#unify-per-package-overrides-across-profiles) for the `[profile.test.package."*"]` mirror fix.

**Determine profiling scope:**

First, figure out if you're dealing with a small or large workspace. Count the crates:
```bash
cargo metadata --format-version 1 | jq '.workspace_members | length'
```

- **≤ 3 crates**: Profile entire workspace
- **> 3 crates**: Profile per-crate

**Per-workspace profiling:**

```bash
# Clean build for accurate profiling
cargo clean

# Profile with self-profiler
CARGO_PROFILE_RELEASE_DEBUG=true cargo rustc --release -- \
  -Z self-profile=rustc-profile \
  -Z self-profile-events=default,args

# Profile with heaptrack (Linux only)
heaptrack cargo build --release

# LLVM IR analysis
cargo llvm-lines --release > llvm-lines-baseline.txt
```

**Per-crate profiling (workspaces > 3 crates):**

```bash
for crate in $(cargo metadata --format-version 1 | jq -r '.workspace_members[] | split(" ")[0]'); do
  echo "Profiling $crate..."

  cargo clean -p "$crate"

  # Self-profile
  CARGO_PROFILE_RELEASE_DEBUG=true cargo rustc -p "$crate" --release -- \
    -Z self-profile="profile-$crate" \
    -Z self-profile-events=default,args

  # Heaptrack (if available)
  if command -v heaptrack &> /dev/null; then
    heaptrack -o "heaptrack-$crate" cargo build -p "$crate" --release
  fi

  # LLVM lines
  cargo llvm-lines -p "$crate" --release > "llvm-lines-$crate.txt"
done
```

### Phase 3: Analysis

**Generate visualizations:**

Now let's turn that profile data into something you can actually look at.

```bash
# Convert self-profile data to Chrome tracing format
crox rustc-profile.mm_profdata > trace.json

# Generate flamegraph from self-profile
inferno-collapse-cargo rustc-profile.mm_profdata | inferno-flamegraph > flamegraph.svg

# Analyze heaptrack data (interactive)
heaptrack_gui heaptrack.cargo.*.zst
# Or generate report
heaptrack_print heaptrack.cargo.*.zst > heaptrack-report.txt
```

**Identify memory hotspots:**

From `heaptrack-report.txt`, look for:
- **Peak RSS** — Maximum memory used
- **Allocation hotspots** — Functions allocating most memory
- **Temporary allocations** — Short-lived allocations causing churn

From `llvm-lines-baseline.txt`, look for:
- **Top LLVM IR generators** — Generic functions instantiated many times
- **Monomorphization explosion** — Same function appearing 50+ times

From `trace.json` (Chrome DevTools Performance tab), look for:
- **LLVM passes** consuming high memory
- **Type checking** for large types
- **Codegen** bottlenecks

**Categorize findings:**

Create a report structure:

```markdown
## Compilation Memory Profile

**Peak RSS**: [X GB]

### High-Memory Crates
1. crate-name: [peak RSS]
   - Primary issue: [monomorphization/large types/LLVM backend]

### Monomorphization Hotspots
- Function: [name]
  - Instantiations: [count]
  - LLVM IR lines: [count]

### Large Type Issues
- Type: [name]
  - Size: [bytes]
  - Usage: [where it's used]

### LLVM Backend Bottlenecks
- Pass: [name]
  - Memory: [usage]
```

### Phase 4: Refactoring Patterns

Apply these patterns based on findings:

**Pattern 1: Split Large Enums**

```rust
// BEFORE: Large enum causes high memory during type checking
pub enum HugeEnum {
    Variant1(Vec<String>),
    Variant2(HashMap<String, Data>),
    // ... 20 more variants
}

// AFTER: Split into smaller enums
pub enum SmallEnum1 {
    Variant1(Vec<String>),
    Variant2(HashMap<String, Data>),
}

pub enum SmallEnum2 {
    Variant3(Data),
    // ... rest
}

pub enum HugeEnum {
    Group1(SmallEnum1),
    Group2(SmallEnum2),
}
```

**Pattern 2: Box Large Fields**

```rust
// BEFORE: Large inline fields
pub struct Config {
    settings: LargeSettings,  // 2KB struct
    cache: CacheData,         // 5KB struct
}

// AFTER: Box large fields to reduce stack size
pub struct Config {
    settings: Box<LargeSettings>,
    cache: Box<CacheData>,
}
```

**Pattern 3: Reduce Generic Instantiations**

```rust
// BEFORE: Generic function instantiated many times
pub fn process<T: Serialize>(data: Vec<T>) {
    for item in data {
        // Complex logic duplicated per instantiation
        let json = serde_json::to_string(&item).unwrap();
        println!("{}", json);
    }
}

// AFTER: Extract non-generic code
fn process_json(json: String) {
    println!("{}", json);
}

pub fn process<T: Serialize>(data: Vec<T>) {
    for item in data {
        let json = serde_json::to_string(&item).unwrap();
        process_json(json);  // Only serialization is generic
    }
}
```

**Pattern 4: Use Dynamic Dispatch**

```rust
// BEFORE: Many trait implementations cause monomorphization
pub fn handle<T: Handler>(handler: T, event: Event) {
    handler.handle(event);
}

// AFTER: Use trait objects
pub fn handle(handler: &dyn Handler, event: Event) {
    handler.handle(event);
}
```

**Pattern 5: Consolidate Feature Gates**

```rust
// BEFORE: Many feature combinations
#[cfg(all(feature = "a", feature = "b"))]
mod impl_ab;

#[cfg(all(feature = "a", not(feature = "b")))]
mod impl_a;

#[cfg(all(not(feature = "a"), feature = "b"))]
mod impl_b;

// AFTER: Reduce feature matrix
#[cfg(any(feature = "a", feature = "b"))]
mod impl_combined;
```

**Pattern 6: Lazy Static Replacement**

```rust
// BEFORE: lazy_static creates complex initialization
lazy_static! {
    static ref CACHE: Mutex<HashMap<String, Data>> = {
        // Complex initialization
        Mutex::new(HashMap::new())
    };
}

// AFTER: Use OnceCell for simpler initialization
static CACHE: OnceCell<Mutex<HashMap<String, Data>>> = OnceCell::new();

fn get_cache() -> &'static Mutex<HashMap<String, Data>> {
    CACHE.get_or_init(|| Mutex::new(HashMap::new()))
}
```

**Refactoring workflow:**

For each hotspot you've identified:

1. **Read the source file**
2. **Identify which pattern applies** (monomorphization → patterns 3-4, large types → patterns 1-2)
3. **Apply refactoring**
4. **Verify with tests and re-profile** — Make sure tests pass and measure the memory improvement

See [references/refactoring-strategies.md](references/refactoring-strategies.md) for detailed refactoring techniques.

### Phase 5: Validation

**Re-profile after changes:**

```bash
# Clean build
cargo clean

# Re-run profiling (same commands as Phase 2)
CARGO_PROFILE_RELEASE_DEBUG=true cargo rustc --release -- \
  -Z self-profile=rustc-profile-after \
  -Z self-profile-events=default,args

heaptrack cargo build --release

cargo llvm-lines --release > llvm-lines-after.txt
```

**Compare results:**

```bash
# Compare peak RSS
echo "Before: $(grep 'peak heap memory' heaptrack-report.txt)"
echo "After: $(grep 'peak heap memory' heaptrack-report-after.txt)"

# Compare LLVM IR lines
echo "Before: $(head -1 llvm-lines-baseline.txt)"
echo "After: $(head -1 llvm-lines-after.txt)"

# Calculate reduction percentage
```

**Document improvements:**

```markdown
## Memory Reduction Results

**Before**: [X GB peak RSS]
**After**: [Y GB peak RSS]
**Reduction**: [Z%]

### Changes Applied
- Split enum [name] into smaller variants: -[N MB]
- Reduced generic instantiations in [module]: -[N MB]
- Boxed large fields in [struct]: -[N MB]

### Remaining Hotspots
- [Item]: [remaining memory usage]
  - Recommendation: [next steps]
```

## Validation Steps

Before considering the work complete:

- [ ] Nightly Rust toolchain active (verify with `rustc --version`)
- [ ] Profiling tools installed (heaptrack, cargo-llvm-lines, inferno)
- [ ] Baseline profile collected (self-profile, heaptrack, LLVM lines)
- [ ] Hotspots identified and categorized
- [ ] Refactoring patterns applied to top 4 hotspots
- [ ] Tests pass after refactoring (`cargo test`)
- [ ] Post-refactoring profile shows improvement
- [ ] Memory reduction documented with before/after numbers

## Writing Style

Apply `natural-writing-style` to profiling reports, memory reduction summaries, and any documentation produced.

Be specific about what was measured: report actual RSS numbers from heaptrack or self-profile output, not estimates. Don't claim improvements until the post-refactoring profile shows lower peak RSS than the baseline. List what was checked and what hotspots remain.

## References

- [Profiling Rust Compilation](https://rustc-dev-guide.rust-lang.org/profiling.html)
- [measureme Self-Profiler](https://github.com/rust-lang/measureme)
- [Heaptrack Memory Profiler](https://github.com/KDE/heaptrack)
- [cargo-llvm-lines](https://github.com/dtolnay/cargo-llvm-lines)
- [Refactoring Strategies](references/refactoring-strategies.md)
- [Tool Installation Guide](references/tool-installation.md)
- [Pattern Detection Script](scripts/detect-patterns.sh)

## Notes

**Platform limitations:**
- Heaptrack is Linux-only; on macOS use Instruments or valgrind
- Self-profiling works on all platforms with nightly

**Incremental compilation:**
- Disable incremental builds during profiling for accurate results
- Set `CARGO_INCREMENTAL=0` environment variable

**Debug vs Release:**
- Profile release builds (where memory matters most)
- Use `CARGO_PROFILE_RELEASE_DEBUG=true` to get symbols without debug overhead
