---
name: ratatui-accessibility
description: >-
  Ensures ratatui TUI applications meet accessibility standards: NO_COLOR compliance, screen reader compatibility, WCAG contrast requirements, color-independent information design, and keyboard-only navigation. Use when building accessible TUIs, auditing for inclusion, or responding to accessibility bugs.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
  target_ratatui_version: 0.30.0
---

# Ratatui Accessibility

Build inclusive TUI applications that work for all users and all terminal configurations.

## Quick Start

**Color isn't information**: Always pair color with symbols, bold, underline, or reversed style. `✓` vs `✗`, not just green vs red.

**Test with NO_COLOR**: Run `NO_COLOR=1 cargo run` — your TUI must remain usable without any color.

**ANSI 16 colors adapt to themes**: Use `Color::Red`, not `Color::Rgb(255, 0, 0)`. Let users' terminal themes control the actual RGB values.

**Cursor = focus**: Call `frame.set_cursor_position()` to place cursor at active input for screen reader users.

## When to Use This Skill

Use this skill when:

- Building new TUI applications (accessibility from day one)
- User reports "doesn't work in my terminal" or "can't distinguish colors"
- Supporting screen reader users
- Deploying to environments with limited color support (SSH, tmux, old terminals)
- App needs to work in TERM=dumb or 16-color terminals
- Auditing existing TUI for accessibility compliance
- Creating organization-wide TUI guidelines

## Accessibility Requirements

### 1. Color-Independent Information

**Rule**: Never communicate information through color alone (WCAG 1.4.1).

**BAD** — color is the only indicator:

```rust
match status {
    Status::Success => Style::new().fg(Color::Green),
    Status::Error => Style::new().fg(Color::Red),
    Status::Warning => Style::new().fg(Color::Yellow),
}
```

Users who can't see color (NO_COLOR, colorblind, screen readers) can't distinguish these.

**GOOD** — symbol + modifier + color:

```rust
match status {
    Status::Success => ("✓ ", Style::new().fg(Color::Green).bold()),
    Status::Error => ("✗ ", Style::new().fg(Color::Red).bold()),
    Status::Warning => ("⚠ ", Style::new().fg(Color::Yellow)),
    Status::Info => ("ℹ ", Style::new().fg(Color::Cyan)),
}
```

**Other patterns**:

```rust
// Selection indicator
if selected {
    ("> ", Style::new().reversed())
} else {
    ("  ", Style::default())
}

// Checkbox state
match checked {
    true => ("[x] ", Style::new().bold()),
    false => ("[ ] ", Style::new()),
}

// Progress indicator
if completed {
    ("■", Style::new().fg(Color::Green).bold())
} else {
    ("□", Style::new().dim())
}
```

### 2. NO_COLOR Standard

The **NO_COLOR** environment variable (no-color.org) signals "disable all color output."

**Check at startup**:

```rust
fn should_use_color() -> bool {
    // NO_COLOR takes precedence
    if let Ok(val) = env::var("NO_COLOR") {
        if !val.is_empty() {
            return false;
        }
    }

    // FORCE_COLOR overrides detection
    if let Ok(val) = env::var("FORCE_COLOR") {
        if !val.is_empty() {
            return true;
        }
    }

    // TERM=dumb means no color
    if env::var("TERM").map(|t| t == "dumb").unwrap_or(false) {
        return false;
    }

    true
}
```

**Apply globally**:

```rust
struct App {
    theme: Theme,
}

impl App {
    fn new() -> Self {
        let theme = if should_use_color() {
            Theme::default_colored()
        } else {
            Theme::monochrome()
        };
        Self { theme }
    }
}
```

**Monochrome theme**:

```rust
pub fn monochrome() -> Theme {
    Theme {
        fg: Color::Reset,
        bg: Color::Reset,
        title: Style::new().bold().underlined(),
        text: Style::new(),
        text_dim: Style::new().dim(),
        selected: Style::new().reversed(),
        error: Style::new().bold().reversed(),
        warning: Style::new().underlined(),
        success: Style::new().bold(),
        border: Style::new(),
        border_focused: Style::new().bold(),
    }
}
```

**Test**:

```bash
NO_COLOR=1 cargo run
# Must be usable — verify manually
```

### 3. WCAG Contrast Requirements

**4.5:1 minimum for normal text** (AA), **3:1 for large text/UI components** (AA).

The challenge: ANSI 16 named colors have **unknown RGB values** — the terminal theme defines them. You can't programmatically validate contrast for named colors.

**Decision matrix**:

| Approach | Pros | Cons |
|---|---|---|
| **ANSI 16 named** (`Color::Red`) | Adapts to user theme, works everywhere | Can't validate contrast |
| **RGB** (`Color::Rgb(r,g,b)`) | Predictable contrast | Breaks user themes, may not work (macOS Terminal.app), clashes with dark/light backgrounds |
| **Ansi256** (`Color::Indexed(n)`) | Middle ground | Still may clash with backgrounds |

**Recommendation**: Use ANSI 16 named colors + monochrome theme option. Let users choose theme that works for them.

**If using RGB**, validate contrast:

```rust
fn relative_luminance(r: u8, g: u8, b: u8) -> f64 {
    let linearize = |c: u8| -> f64 {
        let c = c as f64 / 255.0;
        if c <= 0.03928 { c / 12.92 } else { ((c + 0.055) / 1.055).powf(2.4) }
    };
    0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)
}

fn contrast_ratio(fg: (u8, u8, u8), bg: (u8, u8, u8)) -> f64 {
    let l1 = relative_luminance(fg.0, fg.1, fg.2);
    let l2 = relative_luminance(bg.0, bg.1, bg.2);
    let (lighter, darker) = if l1 > l2 { (l1, l2) } else { (l2, l1) };
    (lighter + 0.05) / (darker + 0.05)
}

#[test]
fn test_contrast() {
    let fg = (255, 255, 255); // White
    let bg = (0, 0, 0);       // Black
    let ratio = contrast_ratio(fg, bg);
    assert!(ratio >= 4.5, "Contrast {:.1}:1 < 4.5:1", ratio);
}
```

### 4. Screen Reader Compatibility

Terminal TUIs are **hostile to screen readers** by default. Grid-based rendering with cursor jumping causes fragmented announcements. Full-screen redraws trigger constant re-reading.

**Mitigations**:

**Position cursor at active input**:

```rust
fn render(&self, frame: &mut Frame) {
    // ... render widgets ...

    // Place cursor where user is typing
    if let Some(input_area) = self.input_area {
        let cursor_pos = Position {
            x: input_area.x + self.cursor_offset,
            y: input_area.y,
        };
        frame.set_cursor_position(cursor_pos);
    }
}
```

Screen readers track cursor position — this signals focus.

**Minimize redraws**:

```rust
struct App {
    needs_redraw: bool,
}

impl App {
    fn handle_event(&mut self, event: Event) {
        match event {
            Event::Key(_) => {
                // State changed, need redraw
                self.needs_redraw = true;
            }
            Event::Tick if self.animating => {
                // Animation frame
                self.needs_redraw = true;
            }
            _ => {
                // No visual change
                self.needs_redraw = false;
            }
        }
    }
}

// In main loop
if app.needs_redraw {
    terminal.draw(|f| app.render(f))?;
    app.needs_redraw = false;
}
```

**Avoid animated spinners in accessible mode**:

```rust
struct App {
    accessible_mode: bool, // Set from --accessible flag or env var
}

fn progress_indicator(&self, progress: f64) -> Span {
    if self.accessible_mode {
        // Static progress bar
        let filled = (progress * 20.0) as usize;
        let bar = format!("[{:=<filled$}{:.<empty$}] {:.0}%",
            "", "", progress * 100.0,
            filled = filled,
            empty = 20 - filled);
        Span::raw(bar)
    } else {
        // Animated spinner
        let frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
        Span::raw(frames[self.frame_counter % frames.len()])
    }
}
```

**Note**: **AccessKit doesn't work with terminal apps** — it's for GUI toolkits. There's no way to inject accessibility trees into terminal emulators.

### 5. Keyboard-Only Navigation

**All functionality must be keyboard-accessible** — mouse is optional.

**Requirements**:

- [ ] Tab / Shift+Tab cycles focus between UI regions
- [ ] Arrow keys move through items within regions
- [ ] Enter/Space activates buttons and selects items
- [ ] Esc cancels dialogs and returns to previous screen
- [ ] Keyboard shortcuts documented in help screen or status bar

**Example focus management**:

```rust
enum FocusedRegion {
    Sidebar,
    MainView,
    Footer,
}

impl App {
    fn handle_key(&mut self, key: KeyEvent) {
        match key.code {
            KeyCode::Tab => {
                self.focused = match self.focused {
                    FocusedRegion::Sidebar => FocusedRegion::MainView,
                    FocusedRegion::MainView => FocusedRegion::Footer,
                    FocusedRegion::Footer => FocusedRegion::Sidebar,
                };
                self.needs_redraw = true;
            }
            KeyCode::BackTab => {
                // Shift+Tab goes backward
                self.focused = match self.focused {
                    FocusedRegion::Sidebar => FocusedRegion::Footer,
                    FocusedRegion::MainView => FocusedRegion::Sidebar,
                    FocusedRegion::Footer => FocusedRegion::MainView,
                };
                self.needs_redraw = true;
            }
            _ => {
                // Delegate to focused region
                match self.focused {
                    FocusedRegion::Sidebar => self.sidebar.handle_key(key),
                    FocusedRegion::MainView => self.main_view.handle_key(key),
                    FocusedRegion::Footer => self.footer.handle_key(key),
                }
            }
        }
    }
}
```

### 6. Terminal Compatibility

**Works in**:

- 16-color terminals
- 256-color terminals
- Truecolor (24-bit) terminals
- tmux and screen
- SSH sessions
- TERM=dumb (degraded but functional)

**Test matrix**:

```bash
# 16-color
TERM=xterm cargo run

# Dumb terminal
TERM=dumb cargo run

# Inside tmux
tmux new-session cargo run

# Over SSH
ssh remote "cd /path && cargo run"

# NO_COLOR
NO_COLOR=1 cargo run
```

All should work without crashes or garbled output.

**Capability detection** (optional):

```rust
use termbg::theme; // Detects dark vs light background
use termprofile::{TermProfile, DetectorSettings}; // Detects color capabilities

let profile = TermProfile::detect(&stdout(), DetectorSettings::default());
match profile {
    TermProfile::NoTTY => { /* Piped output */ }
    TermProfile::Ansi16 => { /* Use ANSI 16 only */ }
    TermProfile::Ansi256 => { /* Can use 256 colors */ }
    TermProfile::TrueColor => { /* 24-bit RGB works */ }
}
```

## Accessibility Checklist

Before shipping:

- [ ] NO_COLOR tested — app usable without color
- [ ] TERM=dumb tested — graceful degradation
- [ ] Information not conveyed by color alone (symbols, modifiers)
- [ ] Cursor positioned at active input
- [ ] Full keyboard navigation (no mouse required)
- [ ] Works in tmux/screen
- [ ] Works over SSH
- [ ] Help screen or status bar documents keybindings
- [ ] `--accessible` flag or env var to disable animations
- [ ] Contrast validated for RGB colors (if used)
- [ ] Works in 16-color terminals

## References

**Deep dives** (see `references/` directory):

- [Theming System](references/theming-system.md) — Complete theme architecture, capability detection, hot-reloading
- [WCAG Guidelines](references/wcag-guidelines.md) — WCAG 2.2 Level AA adapted for terminal UIs

**External resources**:

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/?currentsidebar=%23col_customize&levels=aaa)
- [NO_COLOR standard](https://no-color.org/)
- [FORCE_COLOR standard](https://force-color.org/)
- [ratatui accessibility discussion](https://github.com/ratatui/ratatui/discussions/879)

**Related skills**:

- [ratatui-implementation](../ratatui-implementation/) — Build accessible TUIs from day one
- [ratatui-review](../ratatui-review/) — Audit existing apps for accessibility compliance

## Writing Style

Apply `natural-writing-style` to all output. Accessibility guidance should be warm and empowering, not preachy. Use "you" and contractions. Frame requirements as opportunities to reach more users.

**Good**:

> Placing the cursor at the active input helps screen reader users know where they're typing. Add `frame.set_cursor_position()` at the end of your render function — takes one line, makes a big difference.

**Bad**:

> It is imperative to ensure that cursor positioning is utilized appropriately for optimal accessibility.

## Validation Steps

Before claiming accessible:

1. **Run with NO_COLOR** — verify usability manually
2. **Test in tmux** — `tmux new-session cargo run`
3. **Test with TERM=dumb** — verify no crashes
4. **Try on 16-color terminal** — test visual clarity
5. **Verify keyboard-only** — unplug mouse, use only keyboard
6. **Check help screen** — all keybindings documented
7. **Test focus indicators** — visually clear what's focused

Don't claim "accessible" without completing these tests.
