---
name: classic-gtk4-rust
description: >
  Build classic-style, high-density, 2000s-era GTK4 user interfaces in Rust
  using the gtk4-rs bindings. Produces functional, low-clutter UIs reminiscent
  of HexChat, Claws Mail, GNOME Evolution, and similar applications. Uses pure
  GTK4 without libadwaita, avoids custom CSS, relies on standard widget
  properties for density control, and follows GTK4 best practices for Rust.
  Trigger this skill whenever the user wants to build a GTK4 desktop application
  in Rust with a classic or traditional look, wants dense/compact UI layouts,
  mentions porting GTK2/GTK3 application UX to GTK4, asks about gtk4-rs widget
  patterns, or references classic GNOME/GTK application design. Also trigger
  when the user mentions HexChat, Claws Mail, Evolution, Pidgin, GIMP classic,
  or similar classic GTK applications as design references, or when they want
  to avoid libadwaita's opinionated spacing and mobile-first design patterns.
compatibility: >
  Requires Rust toolchain (rustc, cargo) and GTK4 development libraries
  (libgtk-4-dev or equivalent). Designed for Claude Code. Does not require
  libadwaita. Target platform is Linux with X11 or Wayland.
allowed-tools: Read Write Edit Bash(cargo *) Bash(rustc *) Bash(python* scripts/*)
metadata:
  author: user
  version: 1.0.0
  gtk4-rs-version: "0.10"
  minimum-rust-version: "1.83"
---

# Classic GTK4 Rust UI skill

Build dense, functional, classic-style desktop applications using Rust and
gtk4-rs — the kind of UI you'd find in HexChat, Claws Mail, or GNOME Evolution.

## When to Use This Skill

- Building a GTK4 desktop application in Rust with a classic or traditional look
- Creating dense, compact UI layouts that avoid libadwaita's mobile-first spacing
- Porting GTK2/GTK3 application UX patterns to GTK4 with gtk4-rs
- Referencing classic GNOME/GTK applications (HexChat, Claws Mail, Evolution, Pidgin, GIMP classic) as design targets

## Quick Start

1. **Set up a new Rust project** with `gtk4` and `gio` crates — no `libadwaita`
2. **Use `gtk::Application`** for the entry point, never `adw::Application`
3. **Build menus with GMenuModel** and toolbars with `gtk::Box` + `gtk::Button`
4. **Control density** through widget properties (margins, spacing), not custom CSS — read the reference files for widget recipes and layout patterns

## Core principles

These four rules govern every decision. Break even one, and you'll end up with
something that's not classic:

1. **Pure GTK4, no libadwaita.** Use `gtk::Application`, never
   `adw::Application`. Libadwaita hardcodes Adwaita spacing, overrides system
   themes, and adds mobile-first padding that'll destroy your density goals.

2. **No custom CSS.** All density control happens through widget properties
   (`set_spacing`, `set_margin_*`, `set_hexpand`, `set_halign`). CSS node
   structure isn't stable API — custom stylesheets break across GTK versions
   and conflict with user themes.

3. **Native window decorations.** Don't call `window.set_titlebar()`. Omit
   this and you'll get the window manager's own title bar — more compact than
   HeaderBar and visually correct for classic apps.

4. **No stubs, no TODOs, no placeholder UI.** Every menu item needs an action.
   Every button does something. Every signal gets connected. Incomplete UI
   elements aren't progress markers — they're bugs.

## When to read reference files

This skill uses progressive disclosure. Read these files from the skill
directory when you need them:

| Need | File | When to read |
|------|------|--------------|
| GTK2/3 widget → GTK4 equivalent | `references/widget-equivalency.md` | Porting an existing app or implementing a classic widget pattern |
| Classic layout architectures | `references/layout-patterns.md` | Starting a new window layout, building multi-pane UIs |
| Idiomatic Rust + gtk4-rs code | `references/rust-patterns.md` | Writing signal handlers, GObject subclasses, async code, state management |
| Spacing and density properties | `references/density-control.md` | Tuning widget density, understanding what properties control spacing |
| Quality gates and guardrails | `references/quality-gates.md` | Before delivering code — run through all gates |
| Anti-patterns and audit checks | `references/anti-patterns.md` | Reviewing existing code, refactoring, or when something looks wrong |

**Always read `references/quality-gates.md` before finalizing any deliverable.**

## Project setup

### Cargo.toml

```toml
[package]
name = "classic-app"
version = "0.1.0"
edition = "2021"
rust-version = "1.83"

[dependencies]
gtk = { version = "0.10", package = "gtk4" }
# Enable newer APIs only if needed — target the lowest GTK4 your users have:
# gtk = { version = "0.10", package = "gtk4", features = ["v4_12"] }

# Required for async, clone macro, action entries:
# (these re-export from gtk, but explicit deps are clearer)
```

**Don't add** `libadwaita` or `adw` to dependencies. If the user's existing
Cargo.toml has these, flag it and recommend removal.

### Application entry point

```rust
use gtk::prelude::*;
use gtk::{glib, Application, ApplicationWindow};

const APP_ID: &str = "org.example.ClassicApp";

fn main() -> glib::ExitCode {
    let app = Application::builder().application_id(APP_ID).build();
    app.connect_activate(build_ui);
    app.run()
}
```

The `build_ui` function constructs the entire window. Check
`references/layout-patterns.md` for the canonical classic layout structure.

## Classic layout skeleton

Every classic application follows this vertical stacking order:

```
ApplicationWindow (native WM titlebar — NO set_titlebar call)
└── Box(Vertical, spacing=0)
    ├── PopoverMenuBar           ← File | Edit | View | Help
    ├── Box.toolbar(Horizontal)  ← Icon buttons, separators
    ├── Paned(Horizontal)        ← Resizable content area
    │   ├── sidebar (ScrolledWindow + ListView/ColumnView)
    │   └── Paned(Horizontal)    ← Inner split (optional)
    │       ├── Notebook          ← Tabbed content
    │       │   └── ScrolledWindow + TextView/ColumnView
    │       └── ScrolledWindow    ← Detail panel
    └── Box.statusbar(Horizontal) ← Status labels
```

Set `spacing(0)` on the outer Box. Set `set_vexpand(true)` on the Paned (the
content area). Set `set_vexpand(false)` on menubar, toolbar, and statusbar.

## Menu bar pattern (required for classic apps)

GTK4 uses GMenu models rendered by PopoverMenuBar. There's no other way to
create menu bars:

```rust
use gtk::gio::{self, Menu, SimpleActionGroup, ActionEntry};

fn build_menubar(window: &ApplicationWindow, app: &Application) -> gtk::PopoverMenuBar {
    let file_menu = Menu::new();
    file_menu.append(Some("_New"), Some("file.new"));
    file_menu.append(Some("_Open…"), Some("file.open"));
    file_menu.append(Some("_Save"), Some("file.save"));
    file_menu.append(Some("_Quit"), Some("app.quit"));

    let edit_menu = Menu::new();
    edit_menu.append(Some("Cu_t"), Some("edit.cut"));
    edit_menu.append(Some("_Copy"), Some("edit.copy"));
    edit_menu.append(Some("_Paste"), Some("edit.paste"));

    let menubar = Menu::new();
    menubar.append_submenu(Some("_File"), &file_menu);
    menubar.append_submenu(Some("_Edit"), &edit_menu);

    // Register action group on the window
    let file_actions = SimpleActionGroup::new();
    file_actions.add_action_entries([
        ActionEntry::builder("new").activate(|_, _, _| { /* impl */ }).build(),
        ActionEntry::builder("open").activate(|_, _, _| { /* impl */ }).build(),
        ActionEntry::builder("save").activate(|_, _, _| { /* impl */ }).build(),
    ]);
    window.insert_action_group("file", Some(&file_actions));

    // Keyboard accelerators — displayed automatically in menus
    app.set_accels_for_action("file.new", &["<Ctrl>n"]);
    app.set_accels_for_action("file.open", &["<Ctrl>o"]);
    app.set_accels_for_action("file.save", &["<Ctrl>s"]);
    app.set_accels_for_action("app.quit", &["<Ctrl>q"]);

    gtk::PopoverMenuBar::from_model(Some(&menubar))
}
```

**Every menu item needs a connected action.** Use `app.` prefix for
application-wide actions (quit, about), `win.` for window-scoped, and custom
prefixes (`file.`, `edit.`) for action groups on the window.

## Toolbar pattern

GtkToolbar was removed in GTK4. Replace with a horizontal Box carrying the
`"toolbar"` CSS class:

```rust
fn build_toolbar() -> gtk::Box {
    let toolbar = gtk::Box::builder()
        .orientation(gtk::Orientation::Horizontal)
        .spacing(2)
        .build();
    toolbar.add_css_class("toolbar");

    // Each button: icon name, tooltip, connected action
    for (icon, tip, action) in [
        ("document-new", "New", "file.new"),
        ("document-open", "Open", "file.open"),
        ("document-save", "Save", "file.save"),
    ] {
        let btn = gtk::Button::from_icon_name(icon);
        btn.set_tooltip_text(Some(tip));
        btn.set_action_name(Some(action));
        toolbar.append(&btn);
    }

    // Group separator
    toolbar.append(&gtk::Separator::new(gtk::Orientation::Vertical));
    toolbar
}
```

Toolbar buttons must have `set_tooltip_text` (accessibility) and
`set_action_name` (functionality). Don't create decorative-only toolbar buttons.

## Density control quick reference

All GTK4 spacing widget properties **default to zero**. The visible whitespace
you see in modern GTK4 apps comes from the Adwaita CSS theme, not widget
properties.

Key properties for tight layouts:

```rust
container.set_spacing(0);           // Box, already default
grid.set_row_spacing(0);            // Grid, already default
grid.set_column_spacing(0);         // Grid, already default
paned.set_wide_handle(false);       // Thin separator, already default
scrolled.set_has_frame(false);      // No border frame
notebook.set_show_border(false);    // No notebook border

// Content areas expand, chrome does not
content.set_hexpand(true);
content.set_vexpand(true);
toolbar.set_vexpand(false);
statusbar.set_vexpand(false);
```

Check `references/density-control.md` for the complete property reference and
what **can't** be changed without CSS.

## Data display: ColumnView over TreeView

TreeView's deprecated (removed in GTK5). Use ColumnView with
SignalListItemFactory for all data-dense displays (mail lists, file browsers,
chat user lists). Check `references/rust-patterns.md` for the complete
ColumnView setup pattern including GObject model definitions.

ColumnView advantages: widget recycling handles 100k+ items, resizable and
sortable columns, row/column separators, and full accessibility.

## Dialogs: no gtk_dialog_run equivalent

All GTK4 dialogs are async. Use `AlertDialog` for simple messages,
`FileDialog` for file operations, and custom `Window` with
`set_modal(true)` + `set_transient_for()` for complex dialogs.
Check `references/widget-equivalency.md` for the complete mapping.

## Validation before delivery

Before delivering any code, run through **all** quality gates in
`references/quality-gates.md`. The gates cover:

- Structural completeness (no stubs, no TODOs)
- Libadwaita contamination check
- CSS contamination check
- Action connectivity (every menu item / button has a handler)
- Density compliance (correct expand/align/spacing settings)
- Async correctness (no GTK calls from background threads)
- Deprecation avoidance (no TreeView, no Dialog, no MessageDialog)
- Accessibility (tooltips, labels, keyboard navigation)
- Theme compatibility (no hardcoded colors or sizes via CSS)

Run `scripts/lint_gtk4.py` on your source tree to catch common violations
automatically. Check `scripts/lint_gtk4.py` for usage.

## What can't be achieved

Be upfront with users about these GTK4 limitations:

- **Toolbar overflow menus** — GtkBox has no overflow handling. Buttons'll clip.
- **Tear-off menus** — Completely removed, no workaround.
- **Programmatic window positioning** — `gtk_window_move()` is gone (Wayland).
- **Identical GTK2 look** — CSS-driven button/entry padding can't be reduced
  without custom CSS, which we avoid. Accept ~32px min button height.
- **Global hotkeys** — No root coordinate or global grab APIs.
- **Synchronous dialogs** — `dialog.run()` doesn't exist. All dialogs're
  async with callbacks.
- **Drag-and-drop to other apps** — External DnD works but GTK4's API is more
  restrictive than GTK3.

These're hard constraints of GTK4, not skill limitations.

## Writing Style

UI implementation guidance needs to be precise and actionable. Apply `natural-writing-style` to all output:

- Reference specific GTK4 widget names and method signatures, not vague "layout approaches"
- Don't claim an implementation matches a classic app "perfectly" — state which patterns were applied and which GTK4 limitations apply
- Be direct about what GTK4 can't do (see the constraints list above) rather than hedging
- Use contractions naturally; implementation notes should read as practical guidance
