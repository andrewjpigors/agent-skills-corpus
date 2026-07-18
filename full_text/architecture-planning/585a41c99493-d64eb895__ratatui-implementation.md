---
name: ratatui-implementation
description: >-
  Implements production-quality terminal user interfaces with the ratatui Rust library (v0.30+), covering architecture patterns (Elm Architecture, Component Architecture), terminal safety, async event loops, error handling, and quality gates. Use when building new TUI applications or migrating existing terminal UIs to ratatui.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
  target_ratatui_version: 0.30.0
---

# Ratatui TUI Implementation

Build production-quality terminal user interfaces with ratatui v0.30+.

## Quick Start

**Architecture first**: Choose TEA (Elm Architecture) for simple apps, Component Architecture for complex multi-pane UIs. Don't mix the two — commit early.

**Terminal safety's non-negotiable**: Call `color_eyre::install()` *before* `ratatui::init()` so panic hooks'll restore terminal state. Test this works by panicking deliberately during development — it's the only way to verify.

**Channel-based event loops**: Use `tokio::sync::mpsc` with `crossterm::event::EventStream` for testability. Direct `event::read()` blocks're untestable.

**Test with TestBackend from day one**: Render into `Buffer::empty()` for unit tests. Terminal isn't needed — this approach runs without a TTY, including in CI.

## When to Use This Skill

Use this skill when you're:

- Starting a new ratatui TUI application from scratch
- Migrating an existing terminal UI to ratatui — there's a clear upgrade path
- Setting up project structure for a production TUI
- Implementing async event loops with multiple input sources
- Building chat interfaces, system monitors, or interactive CLIs
- Adding TUI functionality to existing Rust applications
- Unsure which architecture pattern to choose — we'll help you decide

## Architecture Decision: TEA vs Component

**The Elm Architecture (TEA)** — Model → Message → Update → View cycle:

```rust
#[derive(Debug, Default)]
struct Model {
    counter: i32,
    running: bool,
}

#[derive(PartialEq)]
enum Message {
    Increment,
    Decrement,
    Quit,
}

fn update(model: &mut Model, msg: Message) -> Option<Message> {
    match msg {
        Message::Increment => model.counter += 1,
        Message::Decrement => model.counter -= 1,
        Message::Quit => model.running = false,
    }
    None // Or Some(next_msg) to chain
}

fn view(model: &Model, frame: &mut Frame) {
    let text = format!("Counter: {}", model.counter);
    frame.render_widget(Paragraph::new(text), frame.area());
}
```

**Good for**: Single-view apps, modal UIs, tools with clear state machines. **Trade-off**: Mutable update (`&mut Model`) differs from pure Elm — ratatui's `StatefulWidget`s require this approach.

**Component Architecture** — Trait-based composition:

```rust
pub trait Component {
    fn handle_key_events(&mut self, key: KeyEvent) -> Action;
    fn update(&mut self, action: Action) -> Action;
    fn render(&mut self, frame: &mut Frame, rect: Rect);
}

struct App {
    sidebar: Box<dyn Component>,
    main_view: Box<dyn Component>,
    footer: Box<dyn Component>,
}
```

**Good for**: Multi-pane layouts, complex UIs with independent regions, plugin systems. **Trade-off**: More boilerplate, trait objects add indirection.

**Decision heuristic**: Single-purpose tool with < 4 distinct views → TEA. Multi-pane dashboard or extensible UI → Component. When you're on the fence, start with TEA — it's simpler to refactor later.

## Project Setup

### Workspace Organization (v0.30+)

Ratatui v0.30.0 reorganized into a workspace with two crates:

- **`ratatui`** (umbrella crate) — Re-exports everything from `ratatui-core`. Use this in applications.
- **`ratatui-core`** — Core functionality without widget re-exports. Use this in widget libraries.

**Application developers** (most people):

```toml
[dependencies]
ratatui = { version = "0.30", features = ["macros"] }
```

You'll get all widgets, backends, and core functionality. This is what you want for building TUIs.

**Widget library authors**:

```toml
[dependencies]
ratatui-core = "0.30"
```

This prevents circular dependencies when your widget library gets included in apps. Apps depend on `ratatui`, your library depends on `ratatui-core`, and it all composes cleanly.

**Why this matters**: Before v0.30, widget libraries that depended on ratatui couldn't be used by apps that also depended on ratatui without version conflicts. The workspace split fixes this.

### Cargo.toml essentials

**For applications**:

```toml
[dependencies]
ratatui = { version = "0.30", features = ["macros"] }
crossterm = { version = "0.28", features = ["event-stream"] }
tokio = { version = "1", features = ["full"] }
color-eyre = "0.6"

[dev-dependencies]
insta = "1"
proptest = "1"
```

**Clippy configuration** (add to `Cargo.toml` or `.clippy.toml`):

```toml
[lints.clippy]
unwrap_used = "warn"      # Panics corrupt terminal
print_stdout = "warn"     # println! corrupts alternate screen
print_stderr = "warn"
exit = "warn"             # Bypasses terminal restoration
```

## Terminal Safety (CRITICAL)

When a TUI panics without cleanup, the terminal stays broken — cursor hidden, input garbled, alternate screen stuck. Users'll hate this.

**Correct initialization order**:

```rust
fn main() -> color_eyre::Result<()> {
    color_eyre::install()?;           // FIRST
    let mut terminal = ratatui::init(); // SECOND (auto panic hook)
    let result = App::new().run(&mut terminal);
    ratatui::restore();                // ALWAYS runs (Drop impl)
    result
}
```

**Why this order**: `ratatui::init()` installs a panic hook that'll restore terminal state. `color_eyre::install()` must come first so the ratatui hook runs before color-eyre's pretty printer.

**Test it works**:

```rust
#[test]
fn panic_restores_terminal() {
    // Spawn your app in a child process, send it a panic-inducing input,
    // verify terminal state is clean afterward
}
```

**Windows compatibility**: Always filter `KeyEventKind::Press` — it's critical:

```rust
match event::read()? {
    Event::Key(key) if key.kind == KeyEventKind::Press => handle_key(key),
    _ => {}
}
```

Windows reports both Press and Release; macOS/Linux report only Press. Without this filter, you'll get double input on Windows.

## Channel-Based Async Event Loop

Direct `event::read()` blocks the main thread — you can't handle ticks, can't inject test events. Channel-based loops fix this.

**Pattern**:

```rust
use tokio::sync::mpsc;
use crossterm::event::{EventStream, Event as CEvent};
use futures::StreamExt;

enum Event {
    Key(KeyEvent),
    Tick,
    Render,
}

async fn event_loop(tx: mpsc::UnboundedSender<Event>) -> Result<()> {
    let mut reader = EventStream::new();
    let mut tick_interval = tokio::time::interval(Duration::from_millis(250));
    let mut render_interval = tokio::time::interval(Duration::from_millis(33)); // 30fps

    loop {
        tokio::select! {
            _ = tick_interval.tick() => { tx.send(Event::Tick)?; }
            _ = render_interval.tick() => { tx.send(Event::Render)?; }
            Some(Ok(CEvent::Key(key))) = reader.next() => {
                if key.kind == KeyEventKind::Press {
                    tx.send(Event::Key(key))?;
                }
            }
        }
    }
}
```

**Benefits**: Testable (send synthetic events via `tx`), clean shutdown (drop sender or use `CancellationToken`), it decouples event production from consumption.

## Error Handling

**Use `thiserror` for domain errors**:

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("Failed to load config: {0}")]
    ConfigLoad(#[from] std::io::Error),
    #[error("Invalid state transition: {from} -> {to}")]
    InvalidTransition { from: String, to: String },
}
```

**Use `color_eyre::Result` as return type**:

```rust
fn run(&mut self, terminal: &mut Terminal<impl Backend>) -> Result<()> {
    // ...
}
```

**Never `unwrap()` in production code** — enforce this with `clippy::unwrap_used`. Use `?` with `.context()` for error propagation:

```rust
std::fs::read_to_string(path)
    .context("Failed to load theme file")?
```

**Display errors in the TUI**: For recoverable errors, show a status bar or popup. For fatal errors, exit the main loop, restore terminal, then let color-eyre display what went wrong.

## Rendering Pattern

Ratatui uses **immediate-mode rendering with double-buffer diffing**. You've got to render all widgets every frame — selective rendering isn't supported.

**Basic render function**:

```rust
fn render(&self, frame: &mut Frame) {
    let area = frame.area();

    // Layout
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3),    // Header
            Constraint::Min(0),       // Content
            Constraint::Length(1),    // Footer
        ])
        .split(area);

    // Widgets
    frame.render_widget(self.header_widget(), chunks[0]);
    frame.render_widget(self.content_widget(), chunks[1]);
    frame.render_widget(self.footer_widget(), chunks[2]);

    // Cursor positioning for screen readers
    if let Some(input_pos) = self.input_cursor_position() {
        frame.set_cursor_position(input_pos);
    }
}
```

**Performance**: Don't allocate strings in `render()` — precompute them in `update()` instead. Use `Span::raw()` with `&str` instead of `String::from()`.

## Testing Strategy

**Unit test widgets directly against Buffer**:

```rust
#[test]
fn test_counter_display() {
    let app = App { counter: 42 };
    let mut buf = Buffer::empty(Rect::new(0, 0, 20, 2));

    app.render(buf.area, &mut buf);

    let expected = Buffer::with_lines(vec![
        "Counter: 42         ",
        "                    ",
    ]);
    assert_eq!(buf, expected);
}
```

**Snapshot test with insta**:

```rust
#[test]
fn test_full_ui() {
    let app = App::default();
    let backend = TestBackend::new(80, 24);
    let mut terminal = Terminal::new(backend).unwrap();

    terminal.draw(|f| app.render(f)).unwrap();

    insta::assert_snapshot!(terminal.backend());
}
```

**State transition tests**:

```rust
#[test]
fn test_navigation() {
    let mut app = App::default();
    app.handle_key(KeyCode::Down.into());
    assert_eq!(app.selected, 1);

    app.handle_key(KeyCode::Enter.into());
    assert_eq!(app.screen, Screen::Detail);
}
```

**Property-based testing with proptest**:

```rust
proptest! {
    #[test]
    fn app_never_panics(actions in vec(any_action(), 0..100)) {
        let mut app = App::default();
        for action in actions {
            app.handle(action); // Must not panic
        }
    }
}
```

See [references/testing.md](references/testing.md) for advanced patterns and strategies you'll want as your app grows.

## Quality Gates Checklist

Before considering your TUI complete, verify these checkpoints:

**Terminal safety**:
- [ ] `color_eyre::install()` comes before `ratatui::init()` — order matters
- [ ] Panic hook's tested (trigger a panic, verify terminal restores)
- [ ] No `std::process::exit()` bypassing restoration
- [ ] No `println!`/`eprintln!` corrupting TUI operation

**Error handling**:
- [ ] `clippy::unwrap_used` enabled and it's passing
- [ ] All errors're propagated with `?` + `.context()`
- [ ] Recoverable errors're displayed in TUI, not silently swallowed

**Async correctness**:
- [ ] `tokio::sync::mpsc` used (not `std::sync::mpsc` — they don't mix)
- [ ] No `std::sync::Mutex` held across `.await` points — deadlock risk
- [ ] Blocking I/O's wrapped in `spawn_blocking()`

**Rendering**:
- [ ] All widgets're rendered every frame — ratatui diffs internally
- [ ] Frame rate's limited (you're not drawing on every single event)
- [ ] Layout tested at minimum viable size — it handles small terminals
- [ ] Cursor's positioned for screen reader focus when there's input

**Testing**:
- [ ] Unit tests for state transitions
- [ ] Snapshot tests for visual output
- [ ] CI runs tests with TestBackend (no terminal needed)

**Performance**:
- [ ] Idle CPU < 1% (proper event polling)
- [ ] Draw time < 16ms for 60fps
- [ ] Bounded channels prevent unbounded growth

See [references/quality-gates.md](references/quality-gates.md) for complete assessment rubric.

## Common Patterns

**Modal dialogs** — Use `Clear` to prevent bleed-through:

```rust
let popup_area = centered_rect(60, 20, frame.area());
frame.render_widget(Clear, popup_area);
frame.render_widget(
    Paragraph::new("Confirm? [y/n]")
        .block(Block::bordered().title("Confirm")),
    popup_area
);
```

**Tab navigation**:

```rust
let tabs = Tabs::new(vec!["Files", "Settings", "Logs", "Help"])
    .select(selected)
    .highlight_style(Style::new().yellow().bold());
```

**Scrollable lists** with `StatefulWidget`:

```rust
let mut list_state = ListState::default();
list_state.select(Some(0));

let list = List::new(items)
    .highlight_style(Style::new().reversed());

frame.render_stateful_widget(list, area, &mut list_state);

// In event handler:
list_state.select_next(); // or select_previous()
```

**Long-running operations**:

```rust
tokio::spawn(async move {
    for progress in 0..=100 {
        tx.send(Event::Progress(progress)).ok();
        tokio::time::sleep(Duration::from_millis(50)).await;
    }
});
```

## References

**Deep dives** (see `references/` directory):

- [Architecture patterns](references/architecture.md) — TEA vs Component detailed comparison
- [Testing strategies](references/testing.md) — Property-based, mocking, CI integration
- [Quality gates](references/quality-gates.md) — Complete assessment rubric
- [Performance optimization](references/performance.md) — Profiling and optimization techniques
- [State machines](references/state-machines.md) — smlang and statig for modal UIs and complex state flows
- [Visual design](references/visual-design.md) — Unicode blocks, Braille patterns, box drawing symbols
- [Ecosystem crates](references/ecosystem.md) — Companion crates for widgets, effects, and utilities (tui-widgets, ratatui-splash-screen, etc.)

**Official ratatui resources**:

- [ratatui.rs concepts](https://ratatui.rs/concepts/) — Architecture, patterns, best practices
- [Component template](https://github.com/ratatui/templates/tree/main/component) — Project structure
- [Widget gallery](https://ratatui.rs/examples/) — Example implementations

**Related skills**:

- [ratatui-review](../ratatui-review/) — Audit existing TUI applications for production-readiness
- [ratatui-accessibility](../ratatui-accessibility/) — Ensure your TUI works for all users

**Ecosystem crates**:

- `tui-textarea` (0.7.0) — Multi-line editor with vim-style modal editing
- `tachyonfx` (0.11.1) — 40+ shader-like effects and animations
- `tui-big-text` (0.7.1) — Oversized pixel text rendering
- `ratatui-macros` (built-in) — `span!`, `line!`, `text!` macros

## Writing Style

This skill produces Rust code with inline comments explaining *why*, not *what*. Comments use contractions and active voice:

```rust
// Good: "Skip render if nothing changed — saves terminal I/O"
// Bad: "This function is utilized to determine if rendering is necessary"
```

Documentation follows project conventions in [natural-writing-style](../natural-writing-style/SKILL.md) — warm, approachable, technically precise.

## Validation Steps

Before claiming implementation is complete:

1. **Run tests**: `cargo test` must pass
2. **Check clippy**: `cargo clippy -- -W clippy::unwrap_used` must pass
3. **Test panic recovery**: Trigger a panic, verify terminal restores
4. **Resize test**: Run TUI, aggressively resize terminal — no crashes
5. **Minimum size**: Test at 10×3 terminal size — graceful degradation
6. **CI verification**: Tests pass in GitHub Actions/GitLab CI with TestBackend

Don't claim the TUI is "production-ready" or "fully tested" until you've verified these steps pass.
