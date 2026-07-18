---
name: TauriCourvux
description: >
  Expert knowledge of the Courvux + Tauri 2 desktop-app blueprint (reference
  repo: `courvux-tauri-example`, aka "Courvux Notepad"). Use when the user
  works on: a Courvux UI running inside a Tauri webview, the
  `courvux-precompile` Vite plugin + strict CSP (`script-src 'self'`, no
  `unsafe-eval`), thin `invoke()` wrappers, native menus via
  `MenuBuilder`/`PredefinedMenuItem`, file associations with
  `tauri-plugin-single-instance`, the `asset://` protocol +
  `convertFileSrc`, atomic Rust file IO (tmp + fsync + rename),
  `tauri-plugin-dialog` / `-opener` / `-window-state`, capability
  allowlists, or the `pnpm tauri:dev` / `pnpm tauri:build` pipeline.
---

# Courvux + Tauri 2 Desktop App Expert

A Tauri 2 desktop app whose webview UI is built with the
[Courvux](https://github.com/vanjexdev/courvux) reactive framework instead
of React/Vue/Svelte. The reference repo is **`courvux-tauri-example`**
(also called *Courvux Notepad*). The defining tradeoff is **strict CSP**:
`script-src 'self'` with no `unsafe-eval`, made possible by the
`courvux-precompile` Vite plugin compiling every template expression to
a JS arrow function at build time.

All paths below are relative to the repo root unless noted.

| | |
|---|---|
| Repo root | `vanjexdev/node/courvux-tauri-example` |
| Courvux version | `0.7.1` (pinned via `github:vanjexdev/courvux#v0.7.1`) |
| Tauri version | `2` |
| Tailwind version | `4` (via `@tailwindcss/vite`, no config file) |
| Bundle identifier | `dev.vanjex.courvux-tauri-notepad` |
| Frontend entry | `src/main.js` (one big `createApp({...}).mount('#app')`) |
| Rust entry | `src-tauri/src/lib.rs` (`pub fn run()` + commands) |
| Mount target | `<div id="app">` in `index.html` |
| Build outputs | `dist/` (Vite) → `src-tauri/target/release/bundle/*` |
| Reference | This skill is the project-level companion to the `courvux` skill |

---

## Project layout

```
courvux-tauri-example/
├── package.json                  # Vite + frontend deps; Tauri CLI as devDep
├── vite.config.js                # tailwindcss + courvuxPrecompile plugins
├── index.html                    # Strict CSP meta + #app mount point
├── src/
│   ├── main.js                   # createApp({...}).mount('#app') — entire UI
│   ├── tauri.js                  # invoke() wrappers — one fn per Rust command
│   ├── markdown.js               # marked + Prism + DOMPurify pipeline
│   ├── pdf-export.js             # jsPDF DOM walker (dyn-imported on demand)
│   ├── icons.js                  # Lucide → static SVG strings (cv-html.raw)
│   ├── style.css                 # @import "tailwindcss"; + print + .markdown-body
│   └── assets/                   # logo, etc.
├── src-tauri/
│   ├── Cargo.toml                # tauri + plugins + serde + serde_yaml + base64
│   ├── build.rs                  # `tauri_build::build()`
│   ├── tauri.conf.json           # productName, window, CSP, fileAssociations, bundle
│   ├── capabilities/default.json # core:default + dialog open/save + opener scope
│   ├── icons/                    # generated via `cargo tauri icon`
│   └── src/
│       ├── main.rs               # windows_subsystem guard + delegates to lib
│       └── lib.rs                # #[tauri::command] fns + AppState + Builder::run
├── docs/                         # GH Pages site (separate)
└── site/                         # docs site source
```

---

## The defining trick — strict CSP via `courvux-precompile`

This is the whole reason to use Courvux instead of Alpine/Vue inside Tauri.
A standard `cv-on="..."` / `:attr="..."` / `{{ expr }}` template needs
`new Function(expr)` at runtime, which requires CSP `script-src 'unsafe-eval'`.
The `courvux/plugin/precompile` Vite plugin **rewrites every static template
expression to a JS arrow function at build time**, inserting them as a
sibling `exprs:` property on the same component config. The runtime checks
`exprs` first and only falls back to `new Function` when an expression is
missing.

```js
// vite.config.js
import courvuxPrecompile from 'courvux/plugin/precompile';

export default defineConfig({
    plugins: [
        tailwindcss(),
        courvuxPrecompile(),
    ],
    base: './',
    server: {
        port: 1420,
        strictPort: true,
        host: process.env.TAURI_DEV_HOST || false,
        hmr: process.env.TAURI_DEV_HOST
            ? { protocol: 'ws', host: process.env.TAURI_DEV_HOST, port: 1421 }
            : undefined,
        watch: { ignored: ['**/src-tauri/**'] },
    },
    envPrefix: ['VITE_', 'TAURI_'],
    build: {
        outDir: 'dist',
        emptyOutDir: true,
        target: process.env.TAURI_ENV_PLATFORM === 'windows' ? 'chrome105' : 'safari13',
        sourcemap: !!process.env.TAURI_ENV_DEBUG,
    },
});
```

**The Vite build log MUST end in `0 template(s) fell back to runtime new Function`.**
Anything else means there is at least one template the runtime will try to
`new Function`, and the strict CSP will block it (the UI silently goes dead
for that part of the app).

Healthy build output:

```
[courvux-precompile] processed 1 file(s), 134 expression(s) precompiled, 0 template(s) fell back to runtime new Function.
```

### Template authoring rules the precompiler imposes

The precompiler walks every JS module looking for `template:` properties.
It only processes templates whose value is:

- A static string literal: `template: '<div>...</div>'`
- A template literal with **no `${}` interpolations**: `` template: `<div>...</div>` ``

That means **the whole UI lives in one big static `template:` string** inside
`createApp({ template: `...` })` — no per-component template builders, no
`html\`...\``-tagged fragments, no concatenation. Sub-components defined via
`components: { ... }` follow the same rule.

### CSP that actually works

```html
<!-- index.html — the meta CSP and tauri.conf.json's must agree. -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self';
               style-src 'self' 'unsafe-inline';
               img-src 'self' data:;
               font-src 'self';
               connect-src 'self' ipc: http://ipc.localhost;
               object-src 'none';
               base-uri 'self';
               form-action 'self'" />
```

`tauri.conf.json` ships a matching CSP that **also** opens `asset:` /
`http://asset.localhost` / `https://asset.localhost` for `img-src` (needed
once `assetProtocol` is enabled for project mode — see the asset-protocol
section below):

```json
"security": {
    "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: asset: http://asset.localhost https://asset.localhost; font-src 'self'; connect-src 'self' ipc: http://ipc.localhost; object-src 'none'; base-uri 'self'; form-action 'self'",
    "assetProtocol": { "enable": true, "scope": [] }
}
```

`style-src 'unsafe-inline'` stays because Tailwind dev-mode emits inline
`<style>` for utility classes; can drop once a CSS-hashing step ships.

---

## End-to-end: add a new Tauri command

The repo's convention is "one Rust command = one JS wrapper". Stick to it.

**1. Rust side** (`src-tauri/src/lib.rs`):

```rust
#[tauri::command]
fn my_command(state: State<'_, AppState>, arg: String) -> Result<String, String> {
    // ... business logic, all errors as String for the frontend
    Ok(format!("got: {}", arg))
}

// Register in the invoke_handler! macro at the bottom of pub fn run():
.invoke_handler(tauri::generate_handler![
    list_notes, read_note, write_note, /* ... existing ... */
    my_command,
])
```

**2. JS wrapper** (`src/tauri.js`):

```js
import { invoke } from '@tauri-apps/api/core';

/** One-line JSDoc explaining the command. */
export const myCommand = (arg) => invoke('my_command', { arg });
```

**3. Caller** (`src/main.js`):

```js
import { myCommand } from './tauri.js';

methods: {
    async doThing() {
        try {
            const result = await myCommand('hello');
            this.message = result;
        } catch (err) {
            console.error('[notepad] my_command failed:', err);
        }
    },
}
```

Rust → JS argument naming: Tauri converts `snake_case` Rust args to
`camelCase` for the JS payload only when using `#[serde(rename_all =
"camelCase")]` on a struct. **For top-level function args, pass the JS
payload with the same snake_case keys** (look at how `write_note` takes
`created_at: u64` and the JS calls `invoke('write_note', { ..., createdAt:
note.createdAt })` — the bridge handles that one, but it's the only
implicit conversion).

---

## Plugins this app uses

Plugins are added in order in `tauri::Builder::default()`. The single-instance
plugin **MUST** be registered first per its docs.

| Plugin | Why | Cargo dep | JS package |
|---|---|---|---|
| `tauri-plugin-single-instance` | Forward double-clicks of a `.md` file to the running app | `tauri-plugin-single-instance = "2"` | — (Rust-only) |
| `tauri-plugin-dialog` | Native folder/file pickers + save dialogs | `tauri-plugin-dialog = "2"` | `@tauri-apps/plugin-dialog` |
| `tauri-plugin-window-state` | Persist window size/pos/maximized across launches | `tauri-plugin-window-state = "2"` | `@tauri-apps/plugin-window-state` |
| `tauri-plugin-opener` | Open `https://…` URLs in the OS default browser | `tauri-plugin-opener = "2"` | `@tauri-apps/plugin-opener` |

```rust
tauri::Builder::default()
    .plugin(tauri_plugin_single_instance::init(|app, args, _cwd| {
        // Runs once per *subsequent* launch — first launch goes through .setup().
        let paths = collect_md_paths(args);
        if let Some(win) = app.get_webview_window("main") {
            let _ = win.show();
            let _ = win.unminimize();
            let _ = win.set_focus();
        }
        if !paths.is_empty() {
            let _ = app.emit("open-files", paths);
        }
    }))
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_window_state::Builder::default().build())
    .plugin(tauri_plugin_opener::init())
    .setup(|app| { /* ... */ Ok(()) })
    .invoke_handler(tauri::generate_handler![ /* ... */ ])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

---

## Capabilities (allowlist)

`src-tauri/capabilities/default.json` is the gatekeeper for every plugin
permission. Tauri 2 requires every IPC capability to be declared explicitly:

```json
{
    "$schema": "https://schema.tauri.app/config/2/capabilities",
    "identifier": "default",
    "description": "Default capabilities — base IPC + dialog + opener scope.",
    "windows": ["main"],
    "permissions": [
        "core:default",
        "dialog:allow-open",
        "dialog:allow-save",
        {
            "identifier": "opener:allow-open-url",
            "allow": [
                { "url": "https://github.com/*" },
                { "url": "https://tauri.app/*" }
            ]
        }
    ]
}
```

**Gotcha:** if the JS calls `openDialog()` or `openUrl()` and the permission
isn't listed, the call resolves to an opaque IPC error with no UI feedback.
Whenever you add a new plugin call from JS, double-check the capability is
also added here.

For the **opener** plugin, the `allow` array is a scope filter — only URLs
matching one of the patterns can be opened. This is on purpose: it stops a
hostile paste from doing `openUrl('javascript:...')` even if it somehow
reached `openUrl()`.

---

## Frontend ↔ Tauri integration patterns

### Thin `invoke` wrappers in `src/tauri.js`

Every Rust command gets a one-line JS wrapper. The Courvux app **never
imports `invoke` directly** — it imports the named wrapper from `tauri.js`.
That gives one obvious place to mock, refactor, or rename a command.

```js
import { invoke } from '@tauri-apps/api/core';

/** Sidebar payload — id, title, updatedAt for every persisted note. */
export const listNotes = () => invoke('list_notes');

export const readNote  = (id) => invoke('read_note', { id });
export const writeNote = (note) => invoke('write_note', {
    id: note.id,
    title: note.title,
    body: note.body,
    createdAt: note.createdAt,
});
```

### Listening to Rust-emitted events

`@tauri-apps/api/event` `listen(name, cb)` returns a promise resolving to
an unlisten function. In this app the listeners live for the entire window
lifetime, so we don't bother storing the unlisten — but if you wire one
inside a Courvux component, **call `this.$addCleanup(unlisten)`** so it
clears on component destroy.

```js
import { listen } from '@tauri-apps/api/event';

// onMount() inside the Courvux app config
listen('open-files', async (e) => {
    const paths = Array.isArray(e.payload) ? e.payload : [];
    for (const path of paths) await this.importExternalMd(path);
}).catch(err => console.error('[notepad] open-files listener failed:', err));

listen('menu', async (e) => {
    switch (e.payload) {
        case 'new':  this.newNote();  break;
        case 'save': await this.forceSave(); break;
        // ...
    }
});
```

### Dialog plugin — native open/save pickers

```js
import { open as openDialog, save as saveDialog } from '@tauri-apps/plugin-dialog';

const picked = await openDialog({
    directory: true,            // folder picker
    multiple: false,
    title: 'Choose notes folder',
});
// → string | null (null = user cancelled)

const file = await openDialog({
    multiple: false,
    filters: [{ name: 'Markdown', extensions: ['md', 'markdown'] }],
    title: 'Open Markdown file',
});

const dest = await saveDialog({
    defaultPath: 'untitled.md',
    filters: [{ name: 'Markdown', extensions: ['md'] }],
    title: 'Save note as Markdown',
});
```

### Opener plugin — external URLs from the About dialog

The Tauri webview sandboxes `<a target="_blank">` (no browser context), so
the standard `<a>` does nothing. Route every external link through the
opener plugin:

```js
import { openUrl } from '@tauri-apps/plugin-opener';

async openExternal(url) {
    try { await openUrl(url); }
    catch (err) { console.error('[notepad] open_url failed:', err); }
}
```

Template:

```html
<a href="#" @click.prevent="openExternal('https://github.com/vanjexdev/courvux')">
    Courvux
</a>
```

The href stays `"#"` so the link renders correctly with `@click.prevent`
stopping the default. **Never** pass a user-controllable URL to
`openUrl()` — the capability scope is the safety net but defense in depth.

### Asset protocol — serving local files into the webview

The app's "Project mode" renders inline images from arbitrary user folders.
That needs Tauri's `asset://` protocol (or `http://asset.localhost` on
Windows). Two steps are required:

**1. Enable in `tauri.conf.json`:**

```json
"security": {
    "assetProtocol": { "enable": true, "scope": [] }
}
```

**2. Grant scope at runtime** when the user opens a project folder
(don't grant statically — the path is unknown at build time):

```rust
// In a #[tauri::command] handler that takes &AppHandle:
if let Err(err) = app.asset_protocol_scope().allow_directory(&abs, true) {
    eprintln!("[notepad] asset scope grant failed for {}: {}", abs_str, err);
}
```

`allow_directory(_, true)` is recursive.

**3. Convert paths to URLs on the JS side:**

```js
import { convertFileSrc } from '@tauri-apps/api/core';

// Absolute filesystem path → URL the webview can fetch:
const url = convertFileSrc('/home/user/photo.jpg');
// → 'asset://localhost/...'   on Linux/macOS
// → 'https://asset.localhost/...'  on Windows
```

Add `tauri` Cargo feature `"protocol-asset"`:

```toml
tauri = { version = "2", features = ["protocol-asset"] }
```

**Sanitization caveat:** DOMPurify rejects the `asset:` scheme by default.
The notepad extends the allowlist regex to permit it (see `markdown.js`):

```js
const ALLOWED_URI_REGEXP = /^(?:(?:https?|ftp|mailto|tel|callto|sms|cid|xmpp|asset):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i;
DOMPurify.sanitize(html, { ADD_ATTR: ['class'], ALLOWED_URI_REGEXP });
```

---

## Native menus

Built in Rust during `setup()`, with two strategies:

- **Custom items** (`MenuItemBuilder::with_id`) — emit a `"menu"` event with
  the item's id; the frontend listens and dispatches to its own handler.
- **Predefined items** (`PredefinedMenuItem::undo|redo|cut|copy|paste|select_all|quit`)
  — trigger the focused element's native handler with **no IPC bounce**.
  This is what makes `<textarea>` / `<input>` get working Cut/Copy/Paste
  on every OS for free.

```rust
let new_item = MenuItemBuilder::with_id("new", "New Note")
    .accelerator("CmdOrCtrl+N").build(app)?;
let save_item = MenuItemBuilder::with_id("save", "Save")
    .accelerator("CmdOrCtrl+S").build(app)?;
let quit_item = PredefinedMenuItem::quit(app, Some("Quit"))?;

let file_menu = SubmenuBuilder::new(app, "File")
    .item(&new_item).item(&save_item).separator().item(&quit_item)
    .build()?;

let undo = PredefinedMenuItem::undo(app, Some("Undo"))?;
let cut  = PredefinedMenuItem::cut(app, Some("Cut"))?;
// ...
let edit_menu = SubmenuBuilder::new(app, "Edit")
    .item(&undo).separator().item(&cut)
    .build()?;

let menu = MenuBuilder::new(app).items(&[&file_menu, &edit_menu]).build()?;
app.set_menu(menu)?;

app.on_menu_event(|app, event| {
    let id = event.id().as_ref();
    if matches!(id, "new" | "save" /* | ... */) {
        let _ = app.emit("menu", id);
    }
});
```

**Accelerator collision gotcha:** keep the JS `keydown` handler in sync with
the menu accelerators. In the notepad, `Ctrl+P` is the JS-only `cycleView`
shortcut (no menu accel), and `Export PDF` uses `Ctrl+Shift+P` because
`Ctrl+P` would otherwise bind to it. The menu accelerator wins if both
exist for the same chord.

---

## File associations + single-instance forwarding

Two coupled pieces:

**`tauri.conf.json`:**

```json
"fileAssociations": [
    {
        "ext": ["md", "markdown"],
        "name": "Markdown",
        "description": "Markdown document",
        "role": "Editor",
        "mimeType": "text/markdown"
    }
]
```

Linux installers (`.deb` / `.rpm` / `.appimage`) generate the matching
`.desktop` file with a `MimeType=` entry. macOS / Windows pick this up
from the platform-native metadata.

After `pnpm tauri:build` and installing, register the app as the default
handler:

```bash
sudo dnf upgrade src-tauri/target/release/bundle/rpm/*.rpm
xdg-mime default dev.vanjex.courvux-tauri-notepad.desktop text/markdown
```

**Two argv-handling paths converge in the frontend:**

1. **First launch** (`<app> note.md` from a file manager double-click) —
   webview isn't mounted yet when Rust's `setup()` runs, so the paths
   are *queued* in `AppState` and the frontend drains them on `onMount`:

   ```rust
   // setup():
   let pending_opens = collect_md_paths(std::env::args());
   app.manage(AppState { inner: Mutex::new(AppStateInner { pending_opens, /* ... */ }) });

   #[tauri::command]
   fn take_pending_open_files(state: State<'_, AppState>) -> Vec<String> {
       let mut inner = state.inner.lock().unwrap();
       std::mem::take(&mut inner.pending_opens)
   }
   ```

   ```js
   // onMount():
   const pending = await takePendingOpenFiles();
   for (const path of pending) await this.importExternalMd(path);
   ```

2. **Every subsequent launch** is intercepted by
   `tauri-plugin-single-instance`, which calls its registered callback
   with the *new* argv inside the *already-running* process. The
   callback raises the existing window and emits `open-files` with the
   paths:

   ```rust
   .plugin(tauri_plugin_single_instance::init(|app, args, _cwd| {
       let paths = collect_md_paths(args);
       if let Some(win) = app.get_webview_window("main") {
           let _ = win.show();
           let _ = win.unminimize();
           let _ = win.set_focus();
       }
       if !paths.is_empty() { let _ = app.emit("open-files", paths); }
   }))
   ```

   ```js
   // onMount():
   listen('open-files', async (e) => {
       for (const path of e.payload ?? []) await this.importExternalMd(path);
   });
   ```

The frontend handler should be **idempotent** — both paths can deliver the
same file (e.g. user has the app open and double-clicks a file that's
already imported).

---

## Atomic file IO in Rust

Every persisting command uses **tmp → fsync → rename** so a crash mid-write
can never leave a corrupted file on disk:

```rust
use std::fs;
use std::io::Write;

let tmp_path = new_path.with_extension("md.tmp");
{
    let mut f = fs::File::create(&tmp_path).map_err(|e| format!("create tmp: {}", e))?;
    f.write_all(payload.as_bytes()).map_err(|e| format!("write tmp: {}", e))?;
    f.sync_all().map_err(|e| format!("fsync: {}", e))?;
}
fs::rename(&tmp_path, &new_path).map_err(|e| format!("rename: {}", e))?;
```

For project mode, the temp file is hidden (leading `.`) and lives in the
same directory as the target so the rename is guaranteed-atomic on POSIX
(can't cross a filesystem boundary). Use the same pattern in any new
write-command.

---

## Shared mutable state via `tauri::State`

```rust
struct AppState {
    inner: Mutex<AppStateInner>,
}

struct AppStateInner {
    notes_dir: PathBuf,
    default_notes_dir: PathBuf,
    config_path: PathBuf,
    pending_opens: Vec<String>,
}

// setup():
app.manage(AppState { inner: Mutex::new(AppStateInner { /* ... */ }) });

// In any command:
#[tauri::command]
fn list_notes(state: State<'_, AppState>) -> Result<Vec<NoteSummary>, String> {
    let dir = state.inner.lock().unwrap().notes_dir.clone();
    // ... read dir, build summaries
}
```

**Locking discipline:** hold the lock only long enough to clone the data
you need (paths, ids), then release before doing IO. The pattern in this
repo is `let dir = state.inner.lock().unwrap().notes_dir.clone();` — the
guard drops at the end of that statement.

---

## Persistence — three layers

| Layer | Where | Owner | What |
|---|---|---|---|
| User prefs that need OS access | `<app-data>/config.json` | Rust | Notes folder override, autoSave toggle, recent projects list |
| UI prefs (cheap, browser-only) | `localStorage` | JS | Sidebar width/open, view mode, last-active mode + project path |
| Window geometry | `<app-data>/window-state.json` | `tauri-plugin-window-state` | Size, position, maximized, fullscreen |

The split is deliberate: anything that needs to read/write *outside* the
webview sandbox (folder paths, recent projects) has to be a Rust command,
while pure UI knobs live in `localStorage` so they don't need an IPC round-
trip on every tweak.

```js
// Pattern for localStorage prefs:
const SIDEBAR_WIDTH_KEY = 'courvux-notepad:sidebar-width';

// onMount:
try {
    const w = parseInt(localStorage.getItem(SIDEBAR_WIDTH_KEY), 10);
    if (!isNaN(w)) this.sidebarWidth = Math.min(MAX, Math.max(MIN, w));
} catch {}

// On change:
try { localStorage.setItem(SIDEBAR_WIDTH_KEY, String(this.sidebarWidth)); } catch {}
```

Every `localStorage` access is wrapped in `try{}catch{}` because some Tauri
configurations (private browsing-mode webviews on some platforms) can throw
on access.

---

## Courvux-specific gotchas inside Tauri

The general Courvux skill covers framework rules. The ones that hit *because*
this is a Tauri app:

### `cv-cloak` is non-optional

Without it the user sees the raw `{{ expr }}` template flash for a frame on
launch. The webview is faster than a normal browser, so it's brief but
visible. The notepad puts it on the root:

```html
<div cv-cloak class="flex h-full"> ... </div>
```

```css
/* style.css — courvux ships this rule, but bundling it explicitly avoids
   a single-frame layout shift if the framework loads late. */
[cv-cloak] { display: none !important; }
```

### `cv-html.raw` is **only** for trusted strings

`cv-html` is sanitized by default. `cv-html.raw` opts out. The notepad uses
`cv-html.raw` for Lucide SVG icons:

```js
// icons.js
export const ICONS = {
    plus: lucideToSvg(Plus),  // → '<svg ...><path/></svg>'
    // ...
};
```

```html
<span cv-html.raw="icons.plus" aria-hidden="true"></span>
```

The SVG strings are **trusted because they originate from this module**. Do
NOT pass user-controllable HTML through `cv-html.raw`. The strict CSP
prevents inline `<script>` execution even if it slips through, but
event-handler attributes and `data:` URLs in `<img>` are still vectors.

### `window.prompt()` is dead on macOS

WKWebView (macOS) strips `window.prompt()` for security and returns `null`
silently. The notepad replaces it with a `cv-if`-gated modal whose state is
a `nameInput: { title, hint, value, resolve }` object, with a `Promise`
backed by the resolver:

```js
askName(title, defaultValue, hint) {
    return new Promise(resolve => {
        this.nameInput = { title, hint: hint || '', value: defaultValue || '', resolve };
        this.$nextTick(() => {
            const input = this.$el.querySelector('[data-name-input]');
            if (input) { input.focus(); input.select(); }
        });
    });
},
confirmNameInput() {
    if (!this.nameInput) return;
    const { value, resolve } = this.nameInput;
    this.nameInput = null;
    resolve(value);
},
cancelNameInput() {
    if (!this.nameInput) return;
    const { resolve } = this.nameInput;
    this.nameInput = null;
    resolve(null);
},
```

Same logic applies to `window.alert()` (works, but yanks focus) and
`window.confirm()` (works on every Tauri platform, but ugly) — replace with
inline banners or modal dialogs where the UX matters.

### Debounced autosave with identity snapshotting

The autosave timer is created in `onMount()` and held in a closure-captured
variable so it doesn't pollute reactive state. **Crucially**, it snapshots
the active note/file identity at schedule time and verifies it again when
the timer fires — without that check, a pending save scheduled against
note A could write A's content into the file for note B after the user
switched:

```js
// onMount():
let autoSaveTimer = null;
this.scheduleAutoSave = () => {
    if (autoSaveTimer) clearTimeout(autoSaveTimer);
    const scheduledMode = this.mode;
    const scheduledKey = scheduledMode === 'project'
        ? this.openFile?.path ?? null
        : this.selectedId;
    autoSaveTimer = setTimeout(() => {
        autoSaveTimer = null;
        if (this.mode !== scheduledMode) return;
        const currentKey = scheduledMode === 'project'
            ? this.openFile?.path ?? null
            : this.selectedId;
        if (currentKey !== scheduledKey) return;
        const status = scheduledMode === 'project' ? this.projectSaveStatus : this.saveStatus;
        if (status === 'dirty') this.persist();
    }, 600);
};
this.cancelAutoSave = () => {
    if (autoSaveTimer) { clearTimeout(autoSaveTimer); autoSaveTimer = null; }
};
```

Also call `this.cancelAutoSave?.()` on any "leaving this thing" path:
selecting a different note, switching mode, force-saving, closing the
project. Otherwise a stale timer can fire after the navigation.

### `beforeunload` to guard against quit-while-dirty

```js
window.addEventListener('beforeunload', (e) => {
    if (this.saveStatus === 'unsaved' || this.saveStatus === 'dirty') {
        e.preventDefault();
        e.returnValue = '';
    }
});
```

Tauri webviews honor `beforeunload`, but only on the user-triggered close
path (`Cmd+Q`, window-X). It does *not* fire on `tauri-plugin-window-state`'s
graceful-shutdown hooks. If you have non-trivial work to flush, also wire
a `tauri::WindowEvent::CloseRequested` handler in Rust and gate the close.

### Object reactivity needs assignment, not mutation

```js
// WRONG — Courvux doesn't notice deep key changes:
this.expanded[node.path] = true;

// RIGHT — spread then assign:
const next = { ...this.expanded };
next[node.path] = true;
this.expanded = next;
```

This is in the Courvux skill but bites hard with tree state because the
expanded-path map mutates on every click.

---

## Imports / exports flow (single-file & batch)

The notepad has two flavors:

- **Per-file** via the dialog plugin (`Save As`, `Open File`). The Rust
  command takes a destination path and writes there directly.
- **Project bundle** via dynamic import of a heavy library
  (`pdf-export.js` → `jspdf`). jsPDF + html2canvas weighs ~600 KB, so the
  Vite chunk only loads when the user actually exports:

```js
async exportProjectPdf() {
    // ...
    const { buildProjectPdf } = await import('./pdf-export.js');
    const base64 = await buildProjectPdf({ sections });
    await writeBinaryFile(dest, base64);
}
```

The heavy library generates a base64 string in JS; Rust decodes it and writes
the binary. This **avoids shipping `tauri-plugin-fs`** (whose capability
surface is much broader than this app needs):

```rust
#[tauri::command]
fn write_binary_file(path: String, base64: String) -> Result<(), String> {
    use base64::Engine;
    let bytes = base64::engine::general_purpose::STANDARD
        .decode(base64.as_bytes())
        .map_err(|e| format!("base64 decode: {}", e))?;
    let p = PathBuf::from(&path);
    if let Some(parent) = p.parent() { fs::create_dir_all(parent).map_err(|e| format!("mkdir: {}", e))?; }
    fs::write(&p, bytes).map_err(|e| format!("write {}: {}", path, e))
}
```

---

## Build / dev commands

| Workflow | Command (from repo root) |
|---|---|
| Run with HMR | `pnpm tauri:dev` |
| Production build (current host platform only) | `pnpm tauri:build` |
| Frontend dev only (no Tauri shell) | `pnpm dev` |
| Frontend build only | `pnpm build` |

First `pnpm tauri:dev` compiles all of Tauri + the platform's webview
bindings (WebKit GTK on Linux, WebView2 on Windows, WKWebView on macOS) —
takes minutes. Subsequent runs are seconds. HMR works for `src/main.js`
and `src/style.css`; Rust changes inside `src-tauri/` trigger a re-link,
not a full rebuild.

### Cross-platform builds

A Tauri build always produces artifacts **for the host platform only**.
The webview side can't cross-compile. To ship for Linux + macOS + Windows
you need three machines, or three GitHub Actions matrix jobs
(`ubuntu-latest` / `macos-latest` / `windows-latest`) each running
`pnpm tauri:build`.

### Fedora 40+ AppImage gotcha

`linuxdeploy` ships an old `strip` that doesn't recognize `.relr.dyn`
emitted by recent glibc:

```bash
NO_STRIP=true pnpm tauri:build
```

Same applies to Arch, openSUSE Tumbleweed. Debian/Ubuntu rarely hit this.

---

## Release-mode profile (size-optimized)

```toml
# src-tauri/Cargo.toml
[profile.release]
panic = "abort"
codegen-units = 1
lto = true
opt-level = "s"
strip = true
```

These are deliberate: the Rust binary is the *biggest* per-platform asset
because the webview engine itself is shared from the OS. `panic = "abort"`
and `opt-level = "s"` together shave several MB. `strip = true` removes
debug symbols at the linker stage so we don't need a separate `strip` pass
(also dodges the Fedora 40 issue above on non-AppImage targets).

---

## Identifier / `app_data_dir()` discipline

Every "where do we persist" question routes through `app.path().app_data_dir()`,
which respects the bundle `identifier` in `tauri.conf.json`:

- Linux: `$XDG_DATA_HOME/dev.vanjex.courvux-tauri-notepad/`
- macOS: `~/Library/Application Support/dev.vanjex.courvux-tauri-notepad/`
- Windows: `%APPDATA%\dev.vanjex.courvux-tauri-notepad\`

Renaming the identifier moves the entire app data dir. **Don't change it
without a migration path** — the previous install's notes, config, and
window state become invisible to the new bundle. The notepad's migration
pattern (legacy `notes.json` → per-note `.md` files) is in `lib.rs` at
`migrate_legacy_json()`; copy that shape if you need one.

---

## Quick references

### Rust commands (`#[tauri::command]`) in this repo

Library mode: `list_notes`, `read_note`, `write_note`, `delete_note`,
`get_notes_dir`, `get_default_notes_dir`, `set_notes_dir`, `reset_notes_dir`,
`get_auto_save`, `set_auto_save`, `import_md_file`, `export_md_file`,
`take_pending_open_files`.

Project mode: `open_project_folder`, `list_project_tree`, `read_project_file`,
`write_project_file`, `create_project_file`, `create_project_dir`,
`write_binary_file`, `get_recent_projects`.

### Emitted events the frontend listens to

- `"open-files"` — payload `string[]` — file association forwarding via
  single-instance.
- `"menu"` — payload `string` (item id) — emitted from
  `app.on_menu_event(...)` for custom menu items.

### JS plugin packages installed

`@tauri-apps/api`, `@tauri-apps/plugin-dialog`, `@tauri-apps/plugin-opener`,
`@tauri-apps/plugin-window-state`.

### Courvux precompile-friendly template patterns used

Everything in `src/main.js`'s root `template:` is static. Sub-strings:

- `cv-if` / `cv-else-if` / `cv-else`
- `cv-for="item in list" :key="item.id"`
- `cv-model` (with `cv-model="x"` on `<input>` / `<textarea>` / `<select>`)
- `:attr="expr"` for class / style / data attrs
- `@event="handler($event)"` + modifiers (`.prevent`, `.stop`, `.self`,
  `.enter`, `.escape`)
- `cv-html.raw="icons.X"` for trusted SVG strings
- `cv-html="renderedBody"` for sanitized markdown HTML
- `cv-show` for cheap visibility toggling (kept in DOM, drives `display`)
- `cv-cloak` on the root

No `cv-data` islands, no dynamic `<component :is>`, no `<router-view>` —
the whole app is one mounted instance.

---

## When you're about to break the strict-CSP guarantee

These are the patterns that silently *re-introduce* `unsafe-eval`:

- A `template:` value that is anything other than a static string /
  template literal (interpolated `${}`, function returning a string, etc.)
  — the precompiler skips it and the runtime falls back to `new Function`.
- Inline `style="font-size: ${expr}px"` mixed with template-string
  interpolation in the JS module — the *whole* template literal becomes
  dynamic and the precompiler drops it.
- A new external dep that uses `new Function` or `eval` internally (rare
  in dev tools, common in some templating / config libs). Check
  `pnpm run build` output — `[courvux-precompile]` only catches Courvux
  templates; runtime `new Function` from a vendor lib will only blow up
  in production when the CSP kicks in.

Always check the Vite build report ends with **`0 template(s) fell back to
runtime new Function`** before shipping. If the count is non-zero, search
the codebase for `template:` and look at each match — one of them isn't a
plain static string anymore.
