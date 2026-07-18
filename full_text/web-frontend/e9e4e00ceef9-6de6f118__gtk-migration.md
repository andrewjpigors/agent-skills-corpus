---
name: gtk-migration
description: >
  Guides migration of GTK2 applications through GTK3 to GTK4, and optionally
  to idiomatic Rust using gtk4-rs. Covers widget replacement, drawing model
  evolution (GDK primitives → Cairo → GtkSnapshot), event controller migration,
  container API changes, CSS theming, and incremental migration strategy. Trigger
  when the user is porting a GTK2 or GTK3 C application forward, mentions
  GdkPixmap/GdkGC/expose-event/gtk_main, asks about GTK version migration, wants
  a Rust rewrite of a GTK C application, or asks how GTK APIs changed across
  versions. Also trigger for questions about GtkTable→GtkGrid, GtkBox orientation,
  GdkWindow→GdkSurface, event signals→event controllers, or gtkrc→CSS theming.
license: MIT
metadata:
  version: 1.0.0
  author: user
  gtk3-min-version: "3.0"
  gtk4-min-version: "4.0"
  gtk4-rs-version: "0.9"
  minimum-rust-version: "1.83"
allowed-tools: Read Write Edit Bash(pkg-config *) Bash(gtk4-builder-tool *) Bash(cargo *) Bash(grep *) Bash(sed *) AskUserQuestion
---

# GTK Migration Skill

Port GTK2 applications to GTK3, GTK4, and optionally to idiomatic Rust — in
stages, without burning everything down at once.

## When to Use This Skill

- Porting a GTK2 C application to GTK3 or GTK4 (especially with GdkPixmap,
  GdkGC, GtkHBox, GtkVBox, GtkTable, expose-event, gtkrc, or gtk_main)
- Migrating a GTK3 application to GTK4 (GdkWindow, event signals, GtkContainer,
  gtk_widget_show_all, GtkMenu, GtkToolbar)
- Rewriting a GTK C application in Rust with gtk4-rs
- Asking how a specific GTK2/3 API maps to its modern equivalent
- Evaluating whether a GTK2/3 codebase is ready to migrate

## Quick Start

Scan the codebase first — check `pkg-config` usage and grep for `GdkPixmap`, `GdkWindow`, `gtk_main`, `GtkContainer` to identify which GTK version you're starting from and the rough scope of work. Then **use `AskUserQuestion`** to confirm: "I found [GTK2/3 indicators] in [N files]. Are you targeting GTK3, GTK4, or the full Rust rewrite path? And are you doing an incremental migration or switching all at once?"

Pick your path and work through it in order — don't try to do everything at once:

```
GTK2 → GTK3: harden → switch build target → fix containers → fix drawing → fix events
GTK3 → GTK4: fix events → fix containers → fix drawing → fix dialogs → fix build
   + Rust:   set up gtk4-rs → translate types → translate signals → translate subclassing
```

Read reference files as needed — they hold the full API tables.

**Must-read before any migration:**
- `references/migration-strategy.md` — incremental approach and build system changes
- `references/api-tables.md` — complete widget and API replacement tables

## GTK2 → GTK3: The Three Big Changes

Three things dominate this migration. Get these right and the rest is mostly mechanical.
But first — harden your codebase before you switch build targets.

### Harden first (still on GTK 2.24)

Add these defines before switching to GTK3 — they'll flag everything that
needs fixing while you still have a working build:

```makefile
CFLAGS += -DGTK_DISABLE_SINGLE_INCLUDES
CFLAGS += -DGDK_DISABLE_DEPRECATED -DGTK_DISABLE_DEPRECATED
CFLAGS += -DGSEAL_ENABLE
```

Fix everything that breaks. Then switch `pkg-config --cflags --libs gtk+-2.0`
to `gtk+-3.0`.

Also introduce `GtkApplication` now — it'll give you D-Bus, single-instance
behavior, and session management for free:

```c
/* GTK3: replace gtk_init() + gtk_main() */
GtkApplication *app = gtk_application_new("org.example.App",
                                           G_APPLICATION_DEFAULT_FLAGS);
g_signal_connect(app, "activate", G_CALLBACK(activate_cb), NULL);
return g_application_run(G_APPLICATION(app), argc, argv);
```

### 1. Drawing: expose-event → draw signal

Replace every `"expose-event"` handler with a `"draw"` signal handler:

```c
/* GTK2 */
g_signal_connect(widget, "expose-event", G_CALLBACK(on_expose), NULL);

static gboolean
on_expose(GtkWidget *widget, GdkEventExpose *event, gpointer data)
{
    GdkDrawable *drawable = GDK_DRAWABLE(gtk_widget_get_window(widget));
    GdkGC *gc = gdk_gc_new(drawable);
    gdk_draw_rectangle(drawable, gc, TRUE, 10, 10, 100, 50);
    g_object_unref(gc);
    return FALSE;
}

/* GTK3 */
g_signal_connect(widget, "draw", G_CALLBACK(on_draw), NULL);

static gboolean
on_draw(GtkWidget *widget, cairo_t *cr, gpointer data)
{
    cairo_set_source_rgb(cr, 0, 0, 1);
    cairo_rectangle(cr, 10, 10, 100, 50);
    cairo_fill(cr);
    return FALSE;
}
```

GTK provides the `cairo_t*` pre-clipped and pre-transformed. Don't create or
destroy it — GTK owns it. Coordinates are widget-relative, not window-relative.

See `references/drawing-migration.md` for the GDK→Cairo function mapping
and the GtkSnapshot path for GTK4.

### 2. Containers and layout widgets

Replace these one-for-one:

| GTK2 | GTK3 |
|---|---|
| `GtkTable` | `GtkGrid` |
| `GtkHBox` / `GtkVBox` | `gtk_box_new(GTK_ORIENTATION_H/V, spacing)` |
| `GtkHPaned` / `GtkVPaned` | `gtk_paned_new(GTK_ORIENTATION_H/V)` |
| `GtkAlignment` | `gtk_widget_set_halign()`, `set_valign()`, margins |
| `GtkComboBoxEntry` | `gtk_combo_box_new_with_entry()` |
| `GtkFontSelection` | `GtkFontChooserWidget` / `GtkFontChooserDialog` |
| `GtkColorSelection` | `GtkColorChooserWidget` / `GtkColorChooserDialog` |
| `GtkStatusIcon` | `GNotification` / libnotify |
| `GtkUIManager` / `GtkActionGroup` | `GtkBuilder` + `GAction` / `GSimpleAction` |
| `GtkStock` IDs | Named icons from the icon theme |

For the complete table including GDK types, see `references/api-tables.md`.

### 3. Theming: gtkrc → CSS

Throw away your `gtkrc`. Write a CSS file instead.

```c
/* Load application CSS in GTK3 */
GtkCssProvider *provider = gtk_css_provider_new();
gtk_css_provider_load_from_data(provider,
    "button { color: #333; }"
    "button:hover { background-color: #eee; }",
    -1, NULL);
gtk_style_context_add_provider_for_screen(
    gdk_screen_get_default(),
    GTK_STYLE_PROVIDER(provider),
    GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);
```

State mapping: `NORMAL` → default, `PRELIGHT` → `:hover`, `ACTIVE` → `:active`,
`SELECTED` → `:checked`, `INSENSITIVE` → `:disabled`.

## GTK3 → GTK4: Four Architectural Shifts

GTK4's a deeper break than GTK3 was. These four changes touch almost every file.

### 1. Events: signals → controllers

Replace every event signal with its `GtkEventController` equivalent:

| GTK3 signal | GTK4 controller |
|---|---|
| `::button-press/release-event` | `GtkGestureClick` |
| `::motion-notify-event` | `GtkEventControllerMotion` |
| `::key-press/release-event` | `GtkEventControllerKey` |
| `::scroll-event` | `GtkEventControllerScroll` |
| `::enter/leave-notify-event` | `GtkEventControllerMotion` (enter/leave signals) |
| `::focus-in/out-event` | `GtkEventControllerFocus` |
| `::delete-event` | `GtkWindow::close-request` signal |
| Drag-and-drop signals | `GtkDragSource` / `GtkDropTarget` |

```c
/* GTK3 */
g_signal_connect(widget, "button-press-event", G_CALLBACK(on_click), NULL);

/* GTK4 */
GtkGestureClick *click = gtk_gesture_click_new();
g_signal_connect(click, "pressed", G_CALLBACK(on_click), NULL);
gtk_widget_add_controller(widget, GTK_EVENT_CONTROLLER(click));
```

Controllers are owned by the widget after `gtk_widget_add_controller()` —
you don't need to keep a reference.

### 2. Containers: GtkContainer is gone

`GtkContainer` and `GtkBin` were removed. Each widget type has its own API:

```c
/* GTK3 — generic add */
gtk_container_add(GTK_CONTAINER(box), child);
gtk_container_remove(GTK_CONTAINER(box), child);

/* GTK4 — type-specific */
gtk_box_append(GTK_BOX(box), child);       /* or prepend/insert_child_after */
gtk_box_remove(GTK_BOX(box), child);

gtk_window_set_child(GTK_WINDOW(window), child);
gtk_frame_set_child(GTK_FRAME(frame), child);
gtk_grid_attach(GTK_GRID(grid), child, col, row, colspan, rowspan);
```

Also replace these removed widgets:
- `GtkMenu` / `GtkMenuBar` / `GtkMenuItem` → `GtkPopoverMenu` + `GMenuModel`
- `GtkToolbar` → `GtkBox` with buttons
- `GtkRadioButton` → `GtkCheckButton` with `set_group()`
- `GtkFileChooserButton` → custom button opening `GtkFileChooserNative`

### 3. Drawing: draw signal → snapshot vfunc

For `GtkDrawingArea`, switch from the `"draw"` signal to `gtk_drawing_area_set_draw_func()`:

```c
/* GTK3 */
g_signal_connect(da, "draw", G_CALLBACK(on_draw), NULL);

/* GTK4 */
gtk_drawing_area_set_draw_func(da, draw_func, NULL, NULL);
/* draw_func signature: (GtkDrawingArea*, cairo_t*, int w, int h, gpointer) */
```

For custom widget subclasses, replace the `draw` vfunc with `snapshot`:

```c
/* GTK4 custom widget */
static void
my_widget_snapshot(GtkWidget *widget, GtkSnapshot *snapshot)
{
    /* Option A: Cairo fallback (CPU-rendered, then uploaded to GPU) */
    cairo_t *cr = gtk_snapshot_append_cairo(snapshot,
        &GRAPHENE_RECT_INIT(0, 0, width, height));
    /* ... your Cairo drawing code unchanged ... */
    cairo_destroy(cr);

    /* Option B: Native GPU path (prefer for simple shapes, GTK 4.14+) */
    gtk_snapshot_append_color(snapshot, &color,
        &GRAPHENE_RECT_INIT(x, y, w, h));
}
```

Use the Cairo fallback for complex path drawing. Use native snapshot nodes
for simple fills, gradients, and textures — they're GPU-accelerated.

### 4. Visibility and lifecycle

```c
/* GTK3 — must show widgets explicitly */
gtk_widget_show_all(window);    /* removed in GTK4 */
gtk_widget_show(widget);        /* still available */
gtk_widget_destroy(widget);     /* removed */

/* GTK4 — widgets are visible by default */
gtk_widget_set_visible(widget, FALSE);   /* hide explicitly when needed */
gtk_window_destroy(GTK_WINDOW(window)); /* for toplevel windows */
g_object_unref(widget);                  /* for freestanding widgets */
```

`GtkApplication` is now mandatory — `gtk_main()` was removed.

**Automate UI file conversion:**
```bash
gtk4-builder-tool simplify --3to4 input.ui > output.ui
gtk4-builder-tool validate output.ui
```

### CSS changes in GTK4

Providers target `GdkDisplay` instead of `GdkScreen`:

```c
gtk_style_context_add_provider_for_display(
    gdk_display_get_default(),
    GTK_STYLE_PROVIDER(provider),
    GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);
```

Per-widget providers were removed. `GtkStyleContext` is deprecated since 4.10 —
use `gtk_widget_add_css_class()` and `remove_css_class()` instead.

## Optional: Porting to Rust with gtk4-rs

Once you're on GTK4 (or porting directly), gtk4-rs gives you compile-time
thread safety, automatic reference counting, and Rust's error handling instead
of `GError**` out-parameters.

### Cargo.toml setup

```toml
[dependencies]
gtk = { version = "0.9", package = "gtk4" }
# For newer APIs:
# gtk = { version = "0.9", package = "gtk4", features = ["v4_12"] }
```

Don't add `libadwaita` unless you specifically want it.

### C → Rust type mapping

| C GTK pattern | Rust gtk4-rs pattern |
|---|---|
| `g_object_new(TYPE, ...)` | `Widget::builder().prop(val).build()` |
| `g_object_ref/unref` | Automatic via `Clone` / `Drop` |
| `g_signal_connect(obj, "sig", cb, data)` | `obj.connect_sig(\|...\| { ... })` |
| `GError **out` | `-> Result<T, glib::Error>` |
| `GTK_WIDGET(obj)` cast | `.upcast::<gtk::Widget>()` |
| `G_DEFINE_TYPE` | `#[glib::object_subclass]` + `ObjectSubclass` trait |
| `gtk_builder_get_object()` | `builder.object::<gtk::Button>("id")?` |
| `GMainContext` async | `glib::spawn_future_local(async { ... })` |

### Ownership and closures

GTK objects in Rust use reference-counted `Clone` — every `clone()` is a
`g_object_ref()`. Signal closures must be `Fn + 'static`, which means interior
mutability for shared state:

```rust
// Simple shared state
let count = Rc::new(Cell::new(0u32));
let count_clone = count.clone();
button.connect_clicked(move |_| {
    count_clone.set(count_clone.get() + 1);
});

// Complex state
let state = Rc::new(RefCell::new(AppState::default()));
let state_clone = state.clone();
button.connect_clicked(move |_| {
    state_clone.borrow_mut().do_something();
});

// glib::clone! macro (cleaner for long closures)
button.connect_clicked(glib::clone!(#[weak] state, move |_| {
    state.borrow_mut().do_something();
}));
```

### Widget subclassing in Rust

```rust
// In imp.rs
#[derive(Default)]
pub struct MyWidget {
    label: RefCell<String>,
}

#[glib::object_subclass]
impl ObjectSubclass for MyWidget {
    const NAME: &'static str = "MyWidget";
    type Type = super::MyWidget;
    type ParentType = gtk::Widget;
}

impl ObjectImpl for MyWidget {}   // minimal — add constructed() etc. as needed
impl WidgetImpl for MyWidget {
    fn snapshot(&self, snapshot: &gtk::Snapshot) {
        // Draw here
    }
}

// In lib.rs or mod.rs
glib::wrapper! {
    pub struct MyWidget(ObjectSubclass<imp::MyWidget>) @extends gtk::Widget;
}
```

See `references/rust-patterns.md` for async patterns, `GtkApplication` setup,
and GObject property definitions with `#[derive(Properties)]`.

## Migration Ordering (Large Codebases)

Port in this order to keep a working build at each step:

```
1. Infrastructure    — GtkApplication, build system (Autotools → Meson)
2. Deprecated API    — apply disable macros, fix warnings
3. Drawing code      — GDK → Cairo (GTK2→3), draw → snapshot (GTK3→4)
4. Container/layout  — GtkTable → Grid, remove GtkContainer calls
5. Event handling    — event signals → controllers (GTK3→4 only)
6. Dialogs           — sync → async dialogs, GtkFileChooserNative
7. Custom widgets    — size negotiation vfuncs, subclass structure
8. UI files          — run gtk4-builder-tool --3to4
9. New features      — list widgets (ListView/ColumnView over TreeView)
```

GTK2, GTK3, and GTK4 coexist in parallel on the same system (different
sonames) — you can run the old binary alongside the new one while migrating.

## Documentation at Each Stage Gate

Before crossing each stage boundary, write a spec entry and any ADRs for
decisions made in that stage. This keeps context fresh and creates a record
of why you made irreversible choices (dropping GTK2 compatibility, adopting
Meson, committing to Rust) while you still remember the tradeoffs.

**At each stage gate, do this:**

```
Stage complete → run adr-create for any decisions made
              → update spec with behavioral changes verified
              → run adr-review + spec-review on new content
              → only then move to the next stage
```

Use `adr-create` for architecture and technology decisions. Use `spec-create`
(or update an existing spec) for behavioral requirements that changed.

**What to document at each stage — see `references/documentation-gates.md`**
for the specific decisions and spec sections that apply to each migration stage.

The short version: if you chose between two approaches and the other approach
is now harder to reach, that's an ADR. If the widget behaves differently for
users after your change, that's a spec update.

## Reference Files

| Need | File |
|---|---|
| Complete widget/API replacement tables | `references/api-tables.md` |
| Drawing model: GDK→Cairo→GtkSnapshot | `references/drawing-migration.md` |
| Event controller patterns | `references/event-controllers.md` |
| Build system: Autotools → Meson | `references/migration-strategy.md` |
| gtk4-rs Rust patterns | `references/rust-patterns.md` |
| Incremental migration strategy | `references/migration-strategy.md` |
| ADR and spec gates per stage | `references/documentation-gates.md` |

## Static Analysis

Run these to find API usage before and after migration:

```bash
# Find all deprecated GTK2 API in a C codebase
grep -rn "gdk_draw_\|GdkGC\|GdkPixmap\|expose.event\|gtk_main\b\|GtkHBox\|GtkVBox\|GtkTable\b" src/

# Find GTK3 API that won't compile on GTK4
grep -rn "GdkWindow\b\|gtk_container_add\|gtk_widget_show_all\|gtk_widget_destroy\|GtkMenu\b\|GtkToolbar\b" src/

# Validate UI files after conversion
gtk4-builder-tool validate --deprecations data/ui/*.ui

# Check pkg-config dependency version
pkg-config --modversion gtk4
pkg-config --modversion gtk+-3.0
```

For C: run `cppcheck` and compile with `-DGTK_DISABLE_DEPRECATED -DGDK_DISABLE_DEPRECATED`
to surface every deprecated call as a warning.

For Rust: `cargo clippy -- -D warnings` catches most gtk-rs anti-patterns.

## Writing Style

Apply `natural-writing-style` to all migration guidance output:

- Reference specific API names (`gtk_widget_add_controller`, `GtkGestureClick`),
  not vague descriptions
- Be direct about what changes are required vs. what's optional
- Don't claim a migration is "complete" without verifying it compiles and runs
- Admit when a GTK4 replacement is worse than the GTK2/3 original
  (e.g., async-only dialogs, no toolbar overflow menus)
