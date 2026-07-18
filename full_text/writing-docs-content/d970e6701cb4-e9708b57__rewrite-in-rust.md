---
name: rewrite-in-rust
description: >-
  Rewrites existing codebases from any language (C, C++, Go, Python, Ruby, JavaScript,
  TypeScript, Java) to idiomatic, secure Rust. Handles codebase analysis, testable specs
  from existing implementations, idiomatic pattern translation, incremental migration,
  security hardening, and differential testing. Triggers: rewrite in rust, port to rust,
  migrate to rust, RIIR, rust rewrite, translate to rust, convert to rust, replace with rust.
license: MIT
metadata:
  version: 2.1.0
  author: skills-repo
  tags: rust migration rewrite port idiomatic security testing
compatibility: >-
  Requires rustc 1.70+, cargo. Optional: cargo-fuzz, cargo-audit, cargo-llvm-cov,
  cargo-geiger, miri, proptest, insta.
allowed-tools: Bash(git * cargo * rustc * rustfmt * clippy *) Read Edit Write Glob Grep AskUserQuestion
---

# Rewrite in Rust

Guides complete lifecycle of rewriting software in idiomatic, secure Rust. Based on production migrations (Cloudflare Pingora, Discord, sudo-rs, uutils coreutils, Fish Shell 4.0) and methodologies from Ferrous Systems, ISRG/Prossimo, and Microsoft teams.

**For detailed reference material, see `references/` directory.**

## Quick Start

Every rewrite follows six phases. You'll need to pass quality gates before proceeding:

1. **Codebase analysis** — Understand what the code does (not how)
2. **Migration architecture** — Choose incremental vs. full rewrite
3. **Test infrastructure** — Set up tests before writing code
4. **Idiomatic implementation** — Write Rust, don't transliterate
5. **Differential testing** — Prove identical behavior
6. **Security hardening** — Audit and minimize dependencies

Don't skip phases — that's the primary cause of rewrite failure.

## When to Use This Skill

**Trigger on:**
- User asks to "rewrite in Rust", "port to Rust", "RIIR"
- Modernizing legacy code for safety or performance
- Security review flags memory safety issues
- Team wants better type safety and compile-time guarantees

**Out of scope:**
- Adding Rust FFI to existing C (use `rust-unsafe-ffi-review`)
- Micro-optimizing already-Rust code

## Phase 1: Codebase Analysis

**Goal**: Understand WHAT the code does, not HOW.

```
Analysis Checklist:
- [ ] Map architecture (C4: Context → Containers → Components)
- [ ] Generate call graphs and dependency maps
- [ ] Mine VCS history for hotspots and change frequency
- [ ] Run existing test suite and measure coverage
- [ ] Write characterization tests for undocumented behavior
- [ ] Document all external interfaces (APIs, CLI, file formats)
```

**Run analysis:**

```bash
# Auto-detects language, analyzes structure, identifies hotspots
scripts/analyze-codebase.sh /path/to/source
```

**Output needed:** Behavioral spec describing every public interface, edge case, and side effect. Architecture diagrams at C4 Container and Component levels. User stories for each major behavioral contract.

Convert the behavioral spec to formal stories using the `story-creator` skill. Each external interface or behavioral guarantee becomes a story with Gherkin acceptance criteria. Run `story-reviewer` on each story before proceeding — stories that fail test derivability mean the behavioral spec was too vague and needs more characterization work first. Save stories to `docs/stories/`.

See [references/codebase-analysis.md](references/codebase-analysis.md) and [references/analysis-patterns.md](references/analysis-patterns.md) for detailed techniques.

**Quality gate:** Written behavioral spec exists. Existing test suite passes. Characterization tests cover critical paths. Architecture diagrams exist. User stories created and reviewed for each public interface or major capability.

## Phase 2: Migration Architecture

**Goal**: You'll choose incremental vs. full rewrite and define the migration path.

**You'll want to default to incremental migration** — big-bang rewrites fail 4.2× more often. That's not a risk worth taking.

**Decision framework:**

```
Score factors (+1 to +3): infrastructure costs, security incidents,
  performance needs, team Rust capacity
Score risks (-1 to -3): codebase size, internal dependencies, timeline
  pressure

Total ≥ +8: Strong case for rewrite
Total +3 to +7: Start with pilot
Total 0 to +2: Targeted Rust modules only
Negative: Don't rewrite
```

**Incremental strategy (preferred):**
- Use strangler fig pattern: facade → build new → redirect → retire old
- Identify first targets: leaf modules, parsers, hot paths, security-critical code
- Select FFI strategy (bindgen, CXX, PyO3)

See [references/migration-architectures.md](references/migration-architectures.md) for detailed strategies.

**Quality gate:** Migration plan exists specifying: (a) incremental vs. full with justification, (b) ordered component list, (c) FFI strategy for boundaries, (d) dependency budget, (e) rollback plan.

## Phase 3: Test Infrastructure

**Goal**: You'll set up testing BEFORE writing implementation code. Tests first, always.

```bash
# Generate test harness scaffold
scripts/generate-test-harness.sh my-project /path/to/original/binary
```

**Test layers:**

1. **Characterization tests** — Capture existing behavior (Feathers method)
2. **Compatibility tests** — Run both binaries with identical inputs
4. **Differential tests** — Property-based testing with random inputs
6. **Snapshot tests** — Output comparison with `insta`
7. **Fuzz tests** — Edge case discovery with `cargo-fuzz`
8. **Benchmarks** — Performance comparison with `criterion`

**Set up:**

```rust
// tests/characterization/mod.rs
#[test]
fn parse_empty_returns_empty_list() {
    // Documents EXISTING behavior, not desired
    let result = parse("");
    assert_eq!(result, Ok(vec![]));
}
```

**Configure CI:**

```yaml
- cargo test --all-features
- cargo clippy -- -W clippy::all -W clippy::pedantic
- cargo fmt --check
- cargo audit
- cargo llvm-cov --fail-under-lines 80
```

See [references/test-validation-strategies.md](references/test-validation-strategies.md) for detailed testing patterns.

**Quality gate:** `cargo test` runs. All ported characterization tests present (initially `#[ignore]` if not passing). CI configured with clippy, fmt, audit, coverage. Miri configured if `unsafe` planned.

## Phase 4: Idiomatic Implementation

**Goal**: You'll implement using Rust idioms, NOT line-by-line translation.

**Critical rules:**

- **Don't transliterate** — Rewrite using Rust patterns
- Use `Result<T, E>` and `?` for errors, not panics
- Use ownership/borrowing instead of GC or manual memory
- Use enums + pattern matching for closed hierarchies
- Use traits + generics for extension points
- Apply `#![forbid(unsafe_code)]` — allow only where essential

**Translation patterns:**

See [references/language-pattern-mappings.md](references/language-pattern-mappings.md) for source language → Rust mappings.

See [references/idiomatic-rust-patterns.md](references/idiomatic-rust-patterns.md) for Rust design patterns.

**Domain-specific patterns:**

- **For async/networked programs:** See [references/tokio-async-migration.md](references/tokio-async-migration.md) for tokio migration strategies, bridging sync↔async, runtime selection, and async anti-patterns to avoid
- **For TUI programs:** See [references/tui-ratatui-migration.md](references/tui-ratatui-migration.md) for ratatui patterns, Elm architecture (TEA), widget mappings, and event handling
- **For GUI desktop programs:** See [references/gui-desktop-migration.md](references/gui-desktop-migration.md) for toolkit selection (GTK4, Qt/CXX-Qt, Tauri), system tray, D-Bus, video playback, and desktop integration crates

**Example (Python → Rust):**

```python
# Python: duck typing
def process(item):
    return item.transform()
```

```rust
// Rust: trait for polymorphism
trait Transformable {
    fn transform(&self) -> Output;
}

fn process<T: Transformable>(item: &T) -> Output {
    item.transform()
}
```

**Workflow:**

1. Start with data structures (use Rust types, not transliterated)
2. Convert error handling (`Result`, not error codes)
4. Replace unsafe patterns (ownership, not manual memory)
6. Use async I/O for daemons/services (tokio, not blocking)
7. Make characterization tests pass, then add Rust-specific tests
8. Run clippy with pedantic lints

**Quality gate:** All characterization tests pass. Clippy reports zero warnings (pedantic). No `unsafe` without documented safety invariant. Coverage ≥80%. If `unsafe` used, Miri passes.

## Phase 5: Differential Testing

**Goal**: You'll prove the Rust implementation behaves identically to the original.

**Strategies:**

1. **Side-by-side comparison:**
   - CLI tools: run both with identical inputs, diff outputs
   - Services: shadow traffic (mirror requests, compare responses)
   - Libraries: test harness calling both implementations

2. **Property-based differential:**

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn differential_test(input in "\\PC{0,100}") {
        let original = original_impl::process(&input);
        let rust = rust_impl::process(&input);
        prop_assert_eq!(original, rust);
    }
}
```

3. **Run original test suite** against Rust implementation
4. **Fuzz testing** with `cargo-fuzz` to find edge cases
6. **Snapshot testing** with `insta` for output regression
7. **Track quantitatively**: X of Y tests passing, % API coverage

See [references/test-validation-strategies.md](references/test-validation-strategies.md) for complete strategies.

**Quality gate:** ≥95% of original test suite passes (document divergences). Differential testing shows zero unexplained differences. Fuzz testing ran ≥1 hour with no crashes. **Mutation testing on the Rust port (`cargo mutants --in-diff <(git diff origin/main)`) shows zero surviving mutants** — a passing differential test that survives mutation isn't actually constraining the Rust port; it's just memorising input/output pairs. The `bugfix` skill's `references/reproducer-and-mutation.md` has the runbook.

## Phase 6: Security Hardening

**Goal**: You'll meet or exceed the original's security posture.

**Checklist:**

```
Security Validation:
- [ ] cargo audit — zero known vulnerabilities
- [ ] cargo deny check — license/source policy passes
- [ ] cargo geiger — document unsafe in dependency tree
- [ ] All unsafe blocks have // SAFETY: comments
- [ ] Dependencies minimized and justified
- [ ] Compiler flags: overflow-checks, debug-assertions
- [ ] ANSSI Secure Rust Guidelines addressed
```

**Commands:**

```bash
cargo audit
cargo deny check
cargo geiger --all-features
cargo clippy -- -W clippy::unwrap_used -W clippy::expect_used
```

See [references/security-patterns.md](references/security-patterns.md) for detailed security guidance.

**Quality gate:** `cargo audit` clean. All `unsafe` documented. Dependencies minimized. ANSSI checklist addressed. Third-party audit if security-critical.

## Critical Agent Rules

1. **ALWAYS read relevant `references/` files** before starting a phase
2. **NEVER skip characterization testing** — existing implementation IS the spec
3. **NEVER do line-by-line translation** — idiomatic Rust is the goal
4. **ALWAYS prefer incremental migration** unless documented case for full rewrite
5. **ALWAYS set up tests BEFORE implementation** — test-first is non-negotiable
6. **ALWAYS run clippy with pedantic lints** to catch non-idiomatic patterns
7. **ALWAYS use `#![forbid(unsafe_code)]`** unless justified
8. **ALWAYS track feature parity quantitatively** with pass/fail counts
9. **Document every intentional behavioral divergence** with rationale
10. **Run original project's test suite** against Rust implementation

## Decision Tree

```
User requests Rust rewrite
├─ Source code available?
│  ├─ YES → Phase 1 (analysis)
│  └─ NO → Ask for source/docs
├─ Existing test suite?
│  ├─ YES → Use as baseline + write characterization tests
│  └─ NO → Must write extensive characterization tests
├─ Small enough for full rewrite? (<10K LOC, well-understood)
│  ├─ YES → Full rewrite acceptable if user agrees
│  └─ NO → Incremental migration (strangler fig)
├─ Security-critical? (auth, crypto, untrusted input, runs as root)
│  ├─ YES → Phase 6 strictly applied, minimize dependencies
│  └─ NO → Standard practices apply
└─ Side-by-side compatibility needed?
   ├─ YES → FFI bridging required
   └─ NO → Can replace after validation
```

## Domain-Specific Patterns

### CLI Tools

**Structure:**
```
cli-tool/
├── src/
│   ├── main.rs    # clap argument parsing
│   ├── lib.rs     # Core logic (testable)
│   └── commands/  # Subcommands
└── tests/
    └── cli/       # assert_cmd integration tests
```

**Crates:** `clap`, `anyhow`, `assert_cmd`

### Systems Daemons

**Structure:**
```
daemon/
├── src/
│   ├── main.rs    # tokio runtime, signal handling
│   ├── server.rs  # Listener
│   └── worker.rs  # Background tasks
└── systemd/       # Service files
```

**Crates:** `tokio`, `nix` (privilege separation), `tracing`

**Privilege separation:**

```rust
use nix::unistd::{setuid, setgid};

#[tokio::main]
async fn main() -> Result<()> {
    let config = load_config()?;

    // Drop privileges before serving
    setgid(Gid::from_raw(config.gid))?;
    setuid(Uid::from_raw(config.uid))?;

    let server = Server::new(config).await?;
    server.run().await
}
```

### Network Services

**Structure with axum:**

```rust
use axum::{Router, routing::get, extract::State};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    db: sqlx::PgPool,
}

#[tokio::main]
async fn main() -> Result<()> {
    let db = sqlx::PgPool::connect(&db_url).await?;
    let state = Arc::new(AppState { db });

    let app = Router::new()
        .route("/api/resource", get(handler))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;
    Ok(())
}
```

**Crates:** `axum`, `sqlx` (compile-time query checks), `tokio`

### Domain-Specific Quality Gates

**GUI apps:** Cross-platform compilation, accessibility (screen readers), IME support, HiDPI rendering, dark/light mode, memory leak detection. See [gui-desktop-migration.md](references/gui-desktop-migration.md).

**TUI apps:** Terminal restore on panic, cross-platform key handling, responsive layout (80×24 min), view purity, alternate screen cleanup, color fallback. See [tui-ratatui-migration.md](references/tui-ratatui-migration.md).

**Async/tokio apps:** No blocking in async, minimal feature flags, graceful shutdown, backpressure control, tracing instrumentation, no nested runtimes, cancellation safety. See [tokio-async-migration.md](references/tokio-async-migration.md).

## Common Pitfalls

**Don't transliterate:**

```rust
// Bad: Direct translation
let mut buffer: [u8; 1024] = [0; 1024];
let n = read_data(&mut buffer)?;

// Good: Idiomatic
let data = read_data_vec()?;
```

**Don't ignore errors:**

```rust
// Bad
config.unwrap()

// Good
config?
```

**Don't block async:**

```rust
// Bad: Blocks executor
async fn handler() {
    std::fs::read("file")?;
}

// Good: Async I/O
async fn handler() {
    tokio::fs::read("file").await?;
}
```

## Cargo Analysis Tools

Run these at each migration phase:

```bash
cargo clippy -- -W clippy::pedantic                  # Catch non-idiomatic patterns during implementation
cargo +nightly miri test                              # Verify unsafe code correctness
cargo audit && cargo deny check                       # Dependency security before release
cargo geiger                                          # Measure unsafe surface area
cargo +nightly udeps                                  # Remove unused dependencies
cargo llvm-cov --html                                 # Coverage report for validation
cargo mutants --in-diff <(git diff origin/main)      # Mutation testing — verify the ported tests catch real bugs
cargo crap --lcov lcov.info                          # CRAP score — find complex Rust code with thin coverage
```

See [references/cargo-analysis-tools.md](references/cargo-analysis-tools.md) for tool selection by migration phase (analysis, implementation, testing, validation, security hardening).

## Writing Style

Migration specs and rewrite documentation guide teams through changes. Apply `natural-writing-style`:

- Don't claim rewrites will be "faster" or "safer" without benchmarks or audit evidence
- Describe migration scope through concrete metrics: crate count, FFI boundary count, test coverage delta
- Never estimate migration timelines — describe dependencies and sequencing instead
- Use contractions; keep technical writing accessible without sacrificing precision

## Validation Requirements

```
Final Checklist:
- [ ] All original functionality replicated
- [ ] Test coverage ≥ original (or ≥ 80%)
- [ ] Zero clippy warnings (-W clippy::pedantic)
- [ ] cargo audit clean
- [ ] cargo mutants: zero surviving mutants on the ported modules (proves ported tests aren't theatrical)
- [ ] cargo crap: no Rust module scores above 30 (Savoia & Evans 2007 formula; see `.claude/rules/static-analysis.md`)
- [ ] Performance within 20% (or better)
- [ ] Documentation complete (README, CHANGELOG)
- [ ] CI/CD configured
- [ ] Integration tests for all public APIs
```

**Run final validation:**

```bash
bash scripts/validate-rust-rewrite.sh
cargo llvm-cov --fail-under-lines 80
RUSTFLAGS="-Z sanitizer=address" cargo +nightly test
```

## Reference Files

| Topic | Reference |
|---|---|
| Production migrations | [reference-projects.md](references/reference-projects.md) |
| Migration strategies | [migration-architectures.md](references/migration-architectures.md) |
| Codebase analysis | [codebase-analysis.md](references/codebase-analysis.md) |
| Analysis patterns | [analysis-patterns.md](references/analysis-patterns.md) |
| Language mappings | [language-pattern-mappings.md](references/language-pattern-mappings.md) |
| Idiomatic Rust | [idiomatic-rust-patterns.md](references/idiomatic-rust-patterns.md) |
| Security patterns | [security-patterns.md](references/security-patterns.md) |
| Testing strategies | [test-validation-strategies.md](references/test-validation-strategies.md) |
| Tokio & async | [tokio-async-migration.md](references/tokio-async-migration.md) |
| TUI with ratatui | [tui-ratatui-migration.md](references/tui-ratatui-migration.md) |
| GUI desktop apps | [gui-desktop-migration.md](references/gui-desktop-migration.md) |

## Helper Scripts

- `scripts/analyze-codebase.sh` — Analyzes existing codebase (VCS hotspots, LOC, tests)
- `scripts/generate-test-harness.sh` — Scaffolds Rust project with test infrastructure
- `scripts/validate-rust-rewrite.sh` — Runs full validation suite

## External Resources

- [Rust Book](https://doc.rust-lang.org/book/)
- [Rustonomicon](https://doc.rust-lang.org/nomicon/) — Unsafe Rust
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [ANSSI Rust Security Guide](https://anssi-fr.github.io/rust-guide/)
- [Thoughtworks on Evolutionary Rewrites](https://www.thoughtworks.com/insights/blog/amortizing-software-rewrites-evolutionary-approach)
