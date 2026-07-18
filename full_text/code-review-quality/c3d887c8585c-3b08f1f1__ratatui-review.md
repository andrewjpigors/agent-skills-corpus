---
name: ratatui-review
description: >-
  Reviews existing ratatui Rust TUI applications for terminal safety, async correctness, performance issues, accessibility compliance, and production-readiness. Use when auditing ratatui code for quality, debugging terminal corruption issues, or assessing TUI applications for production deployment.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
  target_ratatui_version: 0.30.0
---

# Ratatui Code Review

Audit existing ratatui TUI applications for quality and production-readiness.

## Quick Start

**Terminal safety first**: Check `color_eyre::install()` comes before `ratatui::init()`. Verify panic hooks restore terminal. Test by triggering a panic — it's the only way to know it works.

**Search for `unwrap()`**: Run `grep -rn "\.unwrap()" src/` — each one's a potential terminal-corrupting crash. Require `.context()` instead.

**Check event loop**: Async channel-based = testable. Direct `event::read()` blocking = untestable and it's hard to reason about.

**Measure performance**: Run with `top` — idle CPU should be < 1%. Frame drops that're visible = performance issue.

## When to Use This Skill

Use this skill when:

- Reviewing pull requests for ratatui applications
- Debugging terminal corruption or crashes in TUI apps
- Assessing production-readiness before deployment
- Migrating TUI code and need to verify quality
- User reports "terminal gets stuck" or "crashes leave terminal broken"
- Investigating performance issues (lag, high CPU, memory leaks)

## Review Checklist

Work through these in order. Stop at first critical failure — terminal safety issues'll block everything else.

### 1. Terminal Safety (CRITICAL — Zero tolerance)

- [ ] `color_eyre::install()` called before `ratatui::init()`
- [ ] Panic hook present (or using `ratatui::init()` auto-install)
- [ ] `ratatui::restore()` on all exit paths
- [ ] No `std::process::exit()` without restoration
- [ ] No `println!` or `eprintln!` during TUI operation
- [ ] Windows `KeyEventKind::Press` filtering present

**Test**: Add `panic!("test")` in your event handler, run the app, verify terminal restores.

**Common failures**:

```rust
// BAD — wrong order
let terminal = ratatui::init();
color_eyre::install()?; // Too late — panic hook order's wrong

// BAD — no restoration on exit()
if error { std::process::exit(1); } // Terminal'll stay broken

// BAD — println! corrupts alternate screen
println!("Debug: {}", value); // Use a logging framework instead
```

**Fix**:

```rust
// GOOD
fn main() -> color_eyre::Result<()> {
    color_eyre::install()?;           // FIRST
    let terminal = ratatui::init();    // SECOND
    let result = run_app(&mut terminal);
    ratatui::restore();                // ALWAYS
    result
}
```

### 2. Error Handling

- [ ] No raw `unwrap()` or `expect()` in production paths
- [ ] All errors use `?` with `.context()` for propagation
- [ ] `clippy::unwrap_used` lint's enabled in `Cargo.toml` or `.clippy.toml`
- [ ] Recoverable errors're displayed in TUI (not silent failures)
- [ ] `thiserror` for domain errors, `color_eyre::Result` as return type

**Search for violations**:

```bash
grep -rn "\.unwrap()" src/
grep -rn "\.expect(" src/
grep -rn "\.ok()" src/ | grep -v "// Intentionally ignore"
```

**Common failures**:

```rust
// BAD — crashes'll corrupt terminal
let config = std::fs::read_to_string("config.toml").unwrap();
let items = response.json::<Vec<Item>>().unwrap();

// BAD — error's swallowed
api_call().ok(); // No logging, no user feedback
```

**Fix**:

```rust
// GOOD
let config = std::fs::read_to_string("config.toml")
    .context("Failed to load config.toml")?;

// GOOD — display error in TUI
match api_call().await {
    Ok(data) => self.items = data,
    Err(e) => {
        self.error_message = Some(format!("API error: {}", e));
        self.state = AppState::Error;
    }
}
```

### 3. Async Correctness

- [ ] Uses `tokio::sync::mpsc` (not `std::sync::mpsc`) in async code
- [ ] No `std::sync::Mutex` held across `.await` points
- [ ] Blocking I/O's wrapped in `spawn_blocking()`
- [ ] Event loop uses `tokio::select!` for multiplexing
- [ ] Clean shutdown mechanism (channel close or `CancellationToken`)

**Search for violations**:

```bash
grep -rn "std::sync::mpsc" src/
grep -rn "std::sync::Mutex" src/ # Then check for .await nearby
grep -rn "std::fs::" src/ | grep "async fn" # Blocking I/O in async
```

**Common failures**:

```rust
// BAD — std mpsc doesn't integrate with tokio
use std::sync::mpsc;
let (tx, rx) = mpsc::channel();

// BAD — mutex's held across await (deadlock risk)
let data = self.mutex.lock().unwrap();
let result = async_call().await; // Mutex's held during await
process(data);

// BAD — blocks tokio thread
async fn load_file(&self) -> Result<String> {
    std::fs::read_to_string("data.txt") // Blocks executor
}
```

**Fix**:

```rust
// GOOD
use tokio::sync::mpsc;
let (tx, rx) = mpsc::unbounded_channel();

// GOOD — release mutex before await
let data = {
    let guard = self.mutex.lock().unwrap();
    guard.clone()
}; // Mutex's dropped here
let result = async_call().await;

// GOOD — spawn_blocking for I/O
async fn load_file(&self) -> Result<String> {
    tokio::task::spawn_blocking(|| {
        std::fs::read_to_string("data.txt")
    }).await?
}
```

### 4. Rendering Performance

- [ ] All widgets're rendered every frame (no selective rendering)
- [ ] Frame rate's limited (not drawing on every event)
- [ ] No allocations in hot render path
- [ ] Layout handles resize — it's tested at small sizes
- [ ] Virtual scrolling for large datasets (> 1000 items)

**Profile**:

```bash
cargo flamegraph --bin app-name
# Look for hot spots in render path — there should be minimal allocations
```

**Common failures**:

```rust
// BAD — allocates every frame
fn render(&self, frame: &mut Frame) {
    let text = format!("Count: {}", self.count); // String alloc per frame — don't do this
    // ...
}

// BAD — draws on every single event
loop {
    match event::read()? {
        Event::Key(_) | Event::Mouse(_) | Event::Resize(_, _) => {
            terminal.draw(|f| app.render(f))?; // Every event = wasteful
        }
    }
}

// BAD — renders all 10,000 items
let items: Vec<ListItem> = self.all_items.iter()
    .map(|item| ListItem::new(item.as_str()))
    .collect();
```

**Fix**:

```rust
// GOOD — precompute in update
struct App {
    count: i32,
    count_display: String, // Precomputed
}

fn update(&mut self, msg: Message) {
    self.count += 1;
    self.count_display = format!("Count: {}", self.count);
}

fn render(&self, frame: &mut Frame) {
    let text = self.count_display.as_str(); // No allocation
}

// GOOD — frame rate limiting
let mut render_interval = tokio::time::interval(Duration::from_millis(33)); // 30fps

loop {
    tokio::select! {
        _ = render_interval.tick() => {
            terminal.draw(|f| app.render(f))?;
        }
        // ... other branches
    }
}

// GOOD — virtual scrolling
let visible_height = area.height as usize;
let start = self.scroll_offset;
let end = (start + visible_height).min(self.all_items.len());
let items: Vec<ListItem> = self.all_items[start..end]
    .iter()
    .map(|item| ListItem::new(item.as_str()))
    .collect();
```

### 5. Accessibility

- [ ] Information's not conveyed by color alone (symbols, modifiers)
- [ ] NO_COLOR environment variable's respected
- [ ] Works in 16-color terminals
- [ ] Cursor's positioned for screen reader focus
- [ ] Full keyboard navigation (mouse isn't required)

**Test**:

```bash
NO_COLOR=1 cargo run  # Should work without colors — test this manually
TERM=dumb cargo run   # Should degrade gracefully — verify it doesn't crash
```

**Common failures**:

```rust
// BAD — color's the only indicator
match status {
    Status::Good => Style::new().fg(Color::Green),
    Status::Bad => Style::new().fg(Color::Red),
}

// BAD — RGB colors may not work everywhere
Style::new().fg(Color::Rgb(255, 0, 0)) // Not all terminals'll support this
```

**Fix**:

```rust
// GOOD — symbol + color
match status {
    Status::Good => ("✓ ", Style::new().fg(Color::Green).bold()),
    Status::Bad => ("✗ ", Style::new().fg(Color::Red).bold()),
}

// GOOD — ANSI 16 named colors adapt to theme
Style::new().fg(Color::Red) // Terminal theme controls actual RGB
```

See [ratatui-accessibility](../ratatui-accessibility/) skill for complete audit.

### 6. Testing

- [ ] Unit tests exist for state transitions
- [ ] Snapshot tests exist for visual output
- [ ] Tests use `TestBackend` or `Buffer` (terminal isn't needed)
- [ ] CI runs tests successfully — they're passing in automated builds
- [ ] Coverage > 60% (run `cargo tarpaulin` or `cargo llvm-cov`)
- [ ] **Mutation testing** — zero surviving mutants on changed widget / event-handler code. TUI test suites often assert on terminal output buffers without checking the underlying model, so a buggy event handler can still produce the "right" frame for the wrong reason. Mutation testing exposes that.
- [ ] **CRAP score** ≤ 30 on event-handling and state-reducer functions. State reducers tend to be the highest-cyclomatic code in a TUI and the easiest to undertest.

**Check**:

```bash
cargo test
cargo tarpaulin --out Stdout                              # or: cargo llvm-cov --lcov --output-path lcov.info

cargo install --locked cargo-mutants cargo-crap
cargo mutants --in-diff <(git diff origin/main) --timeout-multiplier 2.0
cargo crap --lcov lcov.info                                # default threshold 30
```

See `.claude/rules/static-analysis.md` for the canonical test-effectiveness guidance and cross-language tool table.

**Common failures**:

- No tests at all
- Tests require real terminal (won't run in CI)
- Only manual testing — it's not sustainable
- Tests use `unwrap()` everywhere

### 7. Code Quality

- [ ] `clippy::pedantic` passing or it's intentionally allowed
- [ ] No warnings on `cargo build --release`
- [ ] Clear module separation (everything isn't in `main.rs`)
- [ ] Inline docs for public API
- [ ] Comments explain *why*, not *what* — they're for future maintainers

**Run**:

```bash
cargo clippy -- -W clippy::unwrap_used -W clippy::print_stdout
cargo build --release 2>&1 | grep warning
```

## Performance Audit

Run these checks to verify performance:

**Idle CPU**:

```bash
# Terminal 1
cargo run --release

# Terminal 2
top -p $(pgrep app-name)
# Should be < 1% CPU when idle — if it's higher, you've got a problem
```

**Frame time**:

Add instrumentation:

```rust
fn render(&self, frame: &mut Frame) {
    let start = std::time::Instant::now();
    // ... rendering ...
    let elapsed = start.elapsed();
    if elapsed > Duration::from_millis(16) {
        log::warn!("Slow frame: {:?}", elapsed);
    }
}
```

Target: < 16ms for 60fps, < 33ms for 30fps.

**Memory stability**:

```bash
cargo build
valgrind --leak-check=full --show-leak-kinds=all ./target/debug/app-name
# Or run overnight with `top` monitoring
```

## Security Review

- [ ] No `.unwrap()` on user input — it's untrusted
- [ ] Path traversal checks if you're handling file paths
- [ ] Command injection checks if you're spawning processes
- [ ] No secrets in error messages or logs — they'll leak to logs

## Review Report Template

Use this format for review findings:

```markdown
# Ratatui Code Review: [App Name]

## Summary
[Assessment: Production-ready / Needs work / Blocking issues / Requires major refactoring]

## Critical Issues (MUST FIX)
- Terminal safety: [findings]
- Error handling: [findings]

## Performance Issues
- Idle CPU: [measured value]
- Frame time: [measured value]
- Memory: [findings]

## Quality Issues
- Testing: [findings]
- Code quality: [findings]

## Accessibility Issues
- NO_COLOR: [tested? findings]
- Color-only info: [findings]

## Recommendations
1. [Critical fixes — must complete before deployment]
2. [High-priority improvements — should complete this sprint]
4. [Medium-priority enhancements — include in next release]
6. [Low-priority polish — backlog items]
```

## References

**Deep dives** (see `references/` directory):

- [Terminal safety deep dive](references/terminal-safety.md) — Panic hooks, signal handling, Windows compatibility
- [Performance profiling guide](references/profiling.md) — CPU, memory, and async performance analysis
- [Quality assessment rubric](references/quality-rubric.md) — Quantitative scoring matrix across 6 dimensions
- [Common anti-patterns](references/antipatterns.md) — What to look for and how to fix it

**Related skills**:

- [ratatui-implementation](../ratatui-implementation/) — Build new TUI applications from scratch
- [ratatui-accessibility](../ratatui-accessibility/) — Accessibility guidelines and compliance checks

## Writing Style

Apply `natural-writing-style` to all review output. Review comments should be warm and constructive — point out what's working before diving into issues. Use contractions ("don't" not "do not"), be specific about problems and fixes. Don't hedge when you're certain about a bug.

**Good review comment**:

> The event loop structure's solid — channel-based design makes this testable. One concern: `std::sync::Mutex` is held across an `.await` point at line 145, which can deadlock the tokio executor. Move the lock inside a block so it drops before the await, or switch to `tokio::sync::Mutex` if you need to hold it.

**Bad review comment** (avoid this pattern): <!-- voice-ok -->

> Using std::sync::Mutex across await boundaries creates a deadlock risk that needs fixing.

## Validation Steps

Before submitting review:

1. **Run the app** — experience it firsthand, don't just read the code
2. **Trigger errors** — test error paths, verify what the user sees
3. **Test panic** — add a temporary panic, verify terminal's restored properly
4. **Measure performance** — get actual numbers, not guesses
5. **Test accessibility** — try NO_COLOR=1, TERM=dumb, run it in tmux
6. **Verify claims** — don't say "tests pass" unless you've run them yourself

Don't claim code's "production-ready" without completing this checklist.
