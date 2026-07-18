---
name: tauri-development
description: |
  Comprehensive Tauri v2 desktop application development patterns.
  Triggers: tauri command, tauri state management, tauri event system, tauri plugin,
  tauri capabilities permissions, tauri window management, tauri build distribution,
  tauri auto-updater, tauri ms store, tauri resource bundling, tauri subprocess,
  tauri sqlite database, tauri ipc, tauri webview, tauri security csp,
  tauri testing, tauri nsis installer, tauri configuration, desktop app rust webview
---

# Tauri v2 Development

Production patterns for Tauri v2 desktop applications. Covers the full lifecycle
from architecture through distribution. Derived from patterns proven in
Fincept Terminal (1400+ commands, multi-process architecture, WebSocket state).

---

## Architecture Overview

Tauri v2 apps have two layers:

- **Rust backend** (core process): Handles system calls, file I/O, database access,
  subprocess management, and native APIs. Runs as the main process.
- **WebView frontend**: Renders UI using web technologies (HTML/CSS/JS). Communicates
  with the Rust backend exclusively through IPC (commands and events).

The IPC boundary is the critical design surface. Commands are request-response.
Events are fire-and-forget broadcasts in either direction.

```
┌──────────────────────────────────────────────┐
│  Frontend (WebView2/WebKitGTK/WKWebView)     │
│  ┌────────────────────────────────────────┐   │
│  │  invoke("command_name", { args })      │───┼──► Rust Command Handler
│  │  listen("event-name", callback)        │◄──┼─── Rust app.emit()
│  └────────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

---

## Command Patterns

### Basic Commands

```rust
use tauri::command;

#[command]
pub fn greet(name: &str) -> String {
    format!("Hello, {name}!")
}

// Register in main.rs or lib.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            greet,
            get_records,
            save_record,
            delete_record,
        ])
        .run(tauri::generate_context!())
        .expect("error running tauri app");
}
```

### Async Commands

```rust
use tauri::{command, State};

// Async commands run on the async runtime — use for I/O
#[command]
pub async fn fetch_data(
    url: String,
    state: State<'_, AppState>,
) -> Result<ApiResponse, String> {
    let client = &state.http_client;

    let response = client
        .get(&url)
        .send()
        .await
        .map_err(|e| format!("request failed: {e}"))?;

    let data: ApiResponse = response
        .json()
        .await
        .map_err(|e| format!("parse failed: {e}"))?;

    Ok(data)
}
```

### Error Handling in Commands

```rust
use serde::Serialize;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum CommandError {
    #[error("database error: {0}")]
    Database(#[from] rusqlite::Error),

    #[error("not found: {0}")]
    NotFound(String),

    #[error("validation error: {0}")]
    Validation(String),

    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
}

// Tauri requires errors to be serializable
// Option A: Convert to String
impl From<CommandError> for String {
    fn from(err: CommandError) -> String {
        err.to_string()
    }
}

// Option B: Serialize as structured JSON (preferred)
#[derive(Serialize)]
pub struct SerializedError {
    pub kind: String,
    pub message: String,
}

impl Serialize for CommandError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::Serializer {
        let se = SerializedError {
            kind: match self {
                CommandError::Database(_) => "database",
                CommandError::NotFound(_) => "not_found",
                CommandError::Validation(_) => "validation",
                CommandError::Io(_) => "io",
            }.to_string(),
            message: self.to_string(),
        };
        se.serialize(serializer)
    }
}

#[command]
pub async fn get_record(
    id: String,
    state: State<'_, AppState>,
) -> Result<Record, CommandError> {
    let db = state.db.lock().map_err(|_| {
        CommandError::Database(rusqlite::Error::ExecuteReturnedResults)
    })?;

    let record = db.query_row(
        "SELECT id, name, data FROM records WHERE id = ?1",
        [&id],
        |row| Ok(Record {
            id: row.get(0)?,
            name: row.get(1)?,
            data: row.get(2)?,
        }),
    ).map_err(|e| match e {
        rusqlite::Error::QueryReturnedNoRows => CommandError::NotFound(id),
        other => CommandError::Database(other),
    })?;

    Ok(record)
}
```

### Command Registration at Scale

For large applications with many commands (100+), organize by module:

```rust
// src-tauri/src/commands/mod.rs
pub mod database;
pub mod network;
pub mod system;
pub mod config;

// src-tauri/src/commands/database.rs
#[command] pub async fn db_query(...) -> Result<...> { }
#[command] pub async fn db_insert(...) -> Result<...> { }
#[command] pub async fn db_migrate(...) -> Result<...> { }

// src-tauri/src/lib.rs — register all at once
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![
        // Database commands
        commands::database::db_query,
        commands::database::db_insert,
        commands::database::db_migrate,
        // Network commands
        commands::network::ws_connect,
        commands::network::ws_send,
        commands::network::http_request,
        // System commands
        commands::system::get_system_info,
        commands::system::open_file_dialog,
        // ... potentially hundreds more
    ])
```

---

## State Management

### Defining and Injecting State

```rust
use std::sync::{Arc, Mutex, RwLock};
use dashmap::DashMap;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;

pub type DbPool = Pool<SqliteConnectionManager>;

pub struct AppState {
    // Database pool — thread-safe by design
    pub db_pool: DbPool,

    // Configuration — read-heavy, rarely written
    pub config: RwLock<AppConfig>,

    // Active WebSocket connections — concurrent read/write
    pub ws_connections: DashMap<String, WsConnectionHandle>,

    // Process handles — needs exclusive access
    pub processes: Mutex<Vec<ProcessHandle>>,

    // Application-wide flags
    pub is_shutting_down: std::sync::atomic::AtomicBool,
}

fn main() {
    let db_pool = create_db_pool("app.db").expect("db init failed");
    let state = AppState {
        db_pool,
        config: RwLock::new(AppConfig::default()),
        ws_connections: DashMap::new(),
        processes: Mutex::new(Vec::new()),
        is_shutting_down: std::sync::atomic::AtomicBool::new(false),
    };

    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![/* ... */])
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

### Accessing State in Commands

```rust
use tauri::State;

#[command]
pub async fn get_connection_count(
    state: State<'_, AppState>,
) -> Result<usize, String> {
    Ok(state.ws_connections.len())
}

#[command]
pub fn update_config(
    key: String,
    value: String,
    state: State<'_, AppState>,
) -> Result<(), String> {
    let mut config = state.config.write()
        .map_err(|_| "config lock poisoned".to_string())?;
    config.set(&key, &value);
    Ok(())
}

// For state that needs the AppHandle (e.g., emitting events)
#[command]
pub async fn start_monitoring(
    app: tauri::AppHandle,
    state: State<'_, AppState>,
) -> Result<(), String> {
    let state_clone = state.inner().clone();

    tokio::spawn(async move {
        loop {
            let count = state_clone.ws_connections.len();
            let _ = app.emit("connection-count", count);
            tokio::time::sleep(std::time::Duration::from_secs(5)).await;
        }
    });

    Ok(())
}
```

---

## Event System

### Emitting Events from Rust

```rust
use tauri::{AppHandle, Emitter};
use serde::Serialize;

#[derive(Clone, Serialize)]
pub struct ProgressEvent {
    pub task_id: String,
    pub progress: f64,
    pub message: String,
}

#[derive(Clone, Serialize)]
pub struct DataUpdateEvent {
    pub table: String,
    pub action: String, // "insert" | "update" | "delete"
    pub id: String,
}

// Emit to all windows
pub fn notify_progress(app: &AppHandle, event: ProgressEvent) {
    let _ = app.emit("task-progress", event);
}

// Emit to a specific window
pub fn notify_window(app: &AppHandle, window_label: &str, event: DataUpdateEvent) {
    if let Some(window) = app.get_webview_window(window_label) {
        let _ = window.emit("data-update", event);
    }
}
```

### Listening to Events from Rust

```rust
use tauri::Listener;

fn setup_event_listeners(app: &tauri::App) {
    // Listen for events from the frontend
    app.listen("user-action", |event| {
        let payload = event.payload();
        tracing::info!("user action: {payload}");
    });

    // One-time listener
    app.once("app-ready", |_event| {
        tracing::info!("frontend signaled ready");
    });
}
```

### Frontend Event Handling (TypeScript)

```typescript
import { invoke } from "@tauri-apps/api/core";
import { listen, emit } from "@tauri-apps/api/event";

// Listen for backend events
const unlisten = await listen<ProgressEvent>("task-progress", (event) => {
  console.log(`Task ${event.payload.task_id}: ${event.payload.progress}%`);
  updateProgressBar(event.payload);
});

// Clean up when component unmounts
unlisten();

// Emit event to backend
await emit("user-action", { type: "button-click", target: "refresh" });

// Invoke a command (request-response)
const result = await invoke<Record>("get_record", { id: "123" });
```

---

## Plugin System

### Using Built-in Plugins

```rust
fn main() {
    tauri::Builder::default()
        // File system access
        .plugin(tauri_plugin_fs::init())
        // Shell command execution
        .plugin(tauri_plugin_shell::init())
        // Native dialogs (open/save file, message box)
        .plugin(tauri_plugin_dialog::init())
        // HTTP client
        .plugin(tauri_plugin_http::init())
        // Auto-updater
        .plugin(tauri_plugin_updater::init())
        // Process info
        .plugin(tauri_plugin_process::init())
        // Open URLs in default browser
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

### Plugin Usage from Frontend

```typescript
import { open, save } from "@tauri-apps/plugin-dialog";
import { readTextFile, writeTextFile } from "@tauri-apps/plugin-fs";
import { Command } from "@tauri-apps/plugin-shell";
import { fetch } from "@tauri-apps/plugin-http";

// File dialog
const filePath = await open({
  multiple: false,
  filters: [{ name: "JSON", extensions: ["json"] }],
});
if (filePath) {
  const content = await readTextFile(filePath);
}

// Shell command
const output = await Command.create("git", ["status"]).execute();
console.log(output.stdout);

// HTTP request
const response = await fetch("https://api.example.com/data", {
  method: "GET",
  headers: { Authorization: `Bearer ${token}` },
});
```

---

## Capabilities and Permissions

### Default Capability Configuration

```json
// src-tauri/capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:window:allow-create",
    "core:window:allow-close",
    "core:webview:default",
    "fs:default",
    "fs:allow-read-text-file",
    "fs:allow-write-text-file",
    "dialog:default",
    "dialog:allow-open",
    "dialog:allow-save",
    "shell:default",
    "shell:allow-spawn",
    "http:default",
    {
      "identifier": "http:default",
      "allow": [
        { "url": "https://api.example.com/**" },
        { "url": "https://*.github.com/**" }
      ]
    },
    {
      "identifier": "fs:scope",
      "allow": [
        { "path": "$APPDATA/**" },
        { "path": "$RESOURCE/**" }
      ]
    }
  ]
}
```

### Security Scoping

```json
// Restrict file system access to specific directories
{
  "identifier": "fs:scope",
  "allow": [
    { "path": "$APPDATA/**" },
    { "path": "$HOME/Documents/MyApp/**" },
    { "path": "$RESOURCE/**" }
  ],
  "deny": [
    { "path": "$HOME/.ssh/**" },
    { "path": "$HOME/.gnupg/**" }
  ]
}
```

---

## Window Management

### Creating and Managing Windows

```rust
use tauri::{WebviewUrl, WebviewWindowBuilder};

#[command]
pub async fn open_settings_window(app: tauri::AppHandle) -> Result<(), String> {
    // Check if window already exists
    if let Some(window) = app.get_webview_window("settings") {
        window.set_focus().map_err(|e| e.to_string())?;
        return Ok(());
    }

    WebviewWindowBuilder::new(
        &app,
        "settings",
        WebviewUrl::App("settings.html".into()),
    )
    .title("Settings")
    .inner_size(800.0, 600.0)
    .min_inner_size(600.0, 400.0)
    .resizable(true)
    .center()
    .build()
    .map_err(|e| e.to_string())?;

    Ok(())
}
```

### Window Events

```rust
use tauri::Listener;

fn setup_window_events(app: &tauri::App) {
    let window = app.get_webview_window("main").unwrap();

    // Handle close request — ask for confirmation
    window.on_window_event(|event| {
        if let tauri::WindowEvent::CloseRequested { api, .. } = event {
            // Prevent default close, handle it yourself
            api.prevent_close();
            // Show confirmation dialog, then call window.close()
        }
    });
}
```

### Multi-Window Configuration in tauri.conf.json

```json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "title": "My Application",
        "width": 1280,
        "height": 800,
        "minWidth": 900,
        "minHeight": 600,
        "resizable": true,
        "fullscreen": false,
        "decorations": true,
        "transparent": false
      }
    ]
  }
}
```

---

## Build and Distribution

### tauri.conf.json — Key Sections

```json
{
  "$schema": "https://raw.githubusercontent.com/nicehash/tauri/refs/heads/dev/crates/tauri-cli/schema.json",
  "productName": "MyApp",
  "version": "1.0.0",
  "identifier": "com.mycompany.myapp",
  "build": {
    "beforeDevCommand": "npm run dev",
    "devUrl": "http://localhost:5173",
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../dist"
  },
  "app": {
    "withGlobalTauri": false,
    "security": {
      "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://api.example.com wss://ws.example.com; img-src 'self' data: https:"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "resources": [
      "resources/**/*"
    ],
    "windows": {
      "nsis": {
        "installMode": "both",
        "displayLanguageSelector": false,
        "languages": ["English"],
        "startMenuFolder": "MyApp"
      },
      "wix": {
        "language": ["en-US"]
      }
    },
    "macOS": {
      "entitlements": null,
      "signingIdentity": null,
      "minimumSystemVersion": "10.15"
    },
    "linux": {
      "deb": {
        "depends": ["libwebkit2gtk-4.1-0"]
      },
      "appimage": {
        "bundleMediaFramework": true
      }
    }
  }
}
```

### NSIS Installer (Windows)

```json
// Custom NSIS configuration
{
  "bundle": {
    "windows": {
      "nsis": {
        "installMode": "both",
        "installerIcon": "icons/icon.ico",
        "headerImage": "icons/header.bmp",
        "sidebarImage": "icons/sidebar.bmp",
        "startMenuFolder": "MyCompany",
        "shortDescription": "My Desktop Application",
        "license": "LICENSE.txt"
      }
    }
  }
}
```

---

## Auto-Updater

### Configuration

```json
// tauri.conf.json
{
  "plugins": {
    "updater": {
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "endpoints": [
        "https://github.com/myorg/myapp/releases/latest/download/latest.json"
      ]
    }
  }
}
```

### Rust-Side Update Check

```rust
use tauri_plugin_updater::UpdaterExt;

#[command]
pub async fn check_for_update(app: tauri::AppHandle) -> Result<Option<UpdateInfo>, String> {
    let updater = app.updater().map_err(|e| e.to_string())?;

    match updater.check().await {
        Ok(Some(update)) => {
            Ok(Some(UpdateInfo {
                version: update.version.clone(),
                body: update.body.clone(),
                date: update.date.map(|d| d.to_string()),
            }))
        }
        Ok(None) => Ok(None),
        Err(e) => Err(format!("update check failed: {e}")),
    }
}

#[command]
pub async fn install_update(app: tauri::AppHandle) -> Result<(), String> {
    let updater = app.updater().map_err(|e| e.to_string())?;

    if let Some(update) = updater.check().await.map_err(|e| e.to_string())? {
        // Download and install
        update.download_and_install(
            |chunk, content_length| {
                // Progress callback
                tracing::debug!("downloaded {chunk} of {content_length:?}");
            },
            || {
                // Download complete
                tracing::info!("download complete, restarting");
            },
        ).await.map_err(|e| e.to_string())?;
    }

    Ok(())
}
```

### GitHub Release Format (latest.json)

```json
{
  "version": "1.2.0",
  "notes": "Bug fixes and performance improvements",
  "pub_date": "2025-01-15T12:00:00Z",
  "platforms": {
    "windows-x86_64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "url": "https://github.com/myorg/myapp/releases/download/v1.2.0/MyApp_1.2.0_x64-setup.nsis.zip"
    },
    "darwin-x86_64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "url": "https://github.com/myorg/myapp/releases/download/v1.2.0/MyApp_1.2.0_x64.app.tar.gz"
    },
    "darwin-aarch64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "url": "https://github.com/myorg/myapp/releases/download/v1.2.0/MyApp_1.2.0_aarch64.app.tar.gz"
    },
    "linux-x86_64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "url": "https://github.com/myorg/myapp/releases/download/v1.2.0/MyApp_1.2.0_amd64.AppImage.tar.gz"
    }
  }
}
```

---

## Microsoft Store Distribution

### WiX MSI Configuration

```json
{
  "bundle": {
    "targets": ["msi"],
    "windows": {
      "wix": {
        "language": ["en-US"],
        "template": "wix-template.wxs"
      }
    }
  }
}
```

### Azure Key Vault Code Signing

```powershell
# Sign the MSI with Azure Key Vault
# Requires AzureSignTool
AzureSignTool sign ^
  -kvu "https://myvault.vault.azure.net" ^
  -kvi "client-id" ^
  -kvs "client-secret" ^
  -kvc "certificate-name" ^
  -kvt "tenant-id" ^
  -tr "http://timestamp.digicert.com" ^
  -td sha256 ^
  "target/release/bundle/msi/MyApp_1.0.0_x64.msi"
```

---

## Resource Bundling

### Configuring Resources

```json
// tauri.conf.json
{
  "bundle": {
    "resources": [
      "resources/python/**/*",
      "resources/models/**/*",
      "resources/config.json"
    ]
  }
}
```

### Accessing Bundled Resources at Runtime

```rust
use tauri::{AppHandle, Manager};

#[command]
pub fn get_resource_path(
    app: AppHandle,
    resource_name: String,
) -> Result<String, String> {
    let resource_path = app.path()
        .resource_dir()
        .map_err(|e| format!("resource dir error: {e}"))?
        .join(&resource_name);

    if resource_path.exists() {
        Ok(resource_path.to_string_lossy().to_string())
    } else {
        Err(format!("resource not found: {resource_name}"))
    }
}

// App data directory for user-generated data
#[command]
pub fn get_data_dir(app: AppHandle) -> Result<String, String> {
    let data_dir = app.path()
        .app_data_dir()
        .map_err(|e| format!("data dir error: {e}"))?;

    std::fs::create_dir_all(&data_dir)
        .map_err(|e| format!("create dir error: {e}"))?;

    Ok(data_dir.to_string_lossy().to_string())
}
```

### Embedding Python/Bun Runtimes

```rust
// Pattern from Fincept Terminal: dual Python venv setup
#[command]
pub async fn setup_python_env(app: AppHandle) -> Result<(), String> {
    let resource_dir = app.path().resource_dir()
        .map_err(|e| e.to_string())?;

    let python_dir = resource_dir.join("python");
    let venv_path = app.path().app_data_dir()
        .map_err(|e| e.to_string())?
        .join("venvs");

    // Create virtual environments
    let main_venv = venv_path.join("main");
    if !main_venv.exists() {
        let status = std::process::Command::new(python_dir.join("python.exe"))
            .args(["-m", "venv", main_venv.to_str().unwrap()])
            .status()
            .map_err(|e| format!("venv creation failed: {e}"))?;

        if !status.success() {
            return Err("venv creation failed".into());
        }
    }

    Ok(())
}
```

---

## Cross-Process Communication

### Subprocess Management

```rust
use std::process::Stdio;
use tokio::process::{Command, Child};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

pub struct SubprocessManager {
    processes: DashMap<String, Child>,
}

impl SubprocessManager {
    pub async fn spawn(
        &self,
        id: String,
        program: &str,
        args: &[&str],
        app: AppHandle,
    ) -> Result<(), AppError> {
        let mut child = Command::new(program)
            .args(args)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .kill_on_drop(true)
            .spawn()
            .map_err(|e| AppError::Io(e))?;

        // Stream stdout to frontend
        let stdout = child.stdout.take().unwrap();
        let app_clone = app.clone();
        let id_clone = id.clone();
        tokio::spawn(async move {
            let reader = BufReader::new(stdout);
            let mut lines = reader.lines();
            while let Ok(Some(line)) = lines.next_line().await {
                let _ = app_clone.emit(
                    &format!("process-output-{id_clone}"),
                    line,
                );
            }
        });

        // Stream stderr
        let stderr = child.stderr.take().unwrap();
        let app_clone = app.clone();
        let id_clone = id.clone();
        tokio::spawn(async move {
            let reader = BufReader::new(stderr);
            let mut lines = reader.lines();
            while let Ok(Some(line)) = lines.next_line().await {
                let _ = app_clone.emit(
                    &format!("process-error-{id_clone}"),
                    line,
                );
            }
        });

        self.processes.insert(id, child);
        Ok(())
    }

    pub async fn send_stdin(&self, id: &str, data: &str) -> Result<(), AppError> {
        if let Some(mut entry) = self.processes.get_mut(id) {
            if let Some(stdin) = entry.stdin.as_mut() {
                stdin.write_all(data.as_bytes()).await
                    .map_err(AppError::Io)?;
                stdin.write_all(b"\n").await
                    .map_err(AppError::Io)?;
                stdin.flush().await.map_err(AppError::Io)?;
            }
        }
        Ok(())
    }

    pub async fn kill(&self, id: &str) -> Result<(), AppError> {
        if let Some((_, mut child)) = self.processes.remove(id) {
            child.kill().await.map_err(AppError::Io)?;
        }
        Ok(())
    }
}
```

### MCP Server Spawning Pattern

```rust
// Spawn an MCP (Model Context Protocol) server as a subprocess
#[command]
pub async fn start_mcp_server(
    app: AppHandle,
    state: State<'_, AppState>,
    server_config: McpServerConfig,
) -> Result<String, String> {
    let id = uuid::Uuid::new_v4().to_string();

    let program = match server_config.runtime.as_str() {
        "node" => "node",
        "python" => "python",
        "bun" => "bun",
        _ => return Err("unsupported runtime".into()),
    };

    state.subprocess_manager
        .spawn(id.clone(), program, &[&server_config.script_path], app)
        .await
        .map_err(|e| e.to_string())?;

    Ok(id)
}
```

---

## Database Integration

### SQLite Setup with app_data_dir

```rust
use rusqlite::Connection;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use tauri::{AppHandle, Manager};

pub fn init_database(app: &AppHandle) -> Result<Pool<SqliteConnectionManager>, AppError> {
    let data_dir = app.path().app_data_dir()
        .map_err(|e| AppError::Config(format!("app data dir: {e}")))?;

    std::fs::create_dir_all(&data_dir)?;
    let db_path = data_dir.join("app.db");

    let manager = SqliteConnectionManager::file(&db_path)
        .with_init(|conn| {
            conn.execute_batch("
                PRAGMA journal_mode = WAL;
                PRAGMA synchronous = NORMAL;
                PRAGMA foreign_keys = ON;
                PRAGMA busy_timeout = 5000;
            ")?;
            Ok(())
        });

    let pool = Pool::builder()
        .max_size(4)
        .build(manager)?;

    // Run migrations
    let conn = pool.get()?;
    run_migrations(&conn)?;

    Ok(pool)
}

fn run_migrations(conn: &Connection) -> Result<(), AppError> {
    conn.execute_batch("
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        );
    ")?;

    let current: i64 = conn.query_row(
        "SELECT COALESCE(MAX(version), 0) FROM schema_version",
        [], |r| r.get(0),
    ).unwrap_or(0);

    let migrations = vec![
        // v1
        "CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
        );",
        // v2
        "CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
            expires_at INTEGER
        );
        CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);",
    ];

    for (i, sql) in migrations.iter().enumerate() {
        let version = (i + 1) as i64;
        if version > current {
            conn.execute_batch(sql)?;
            conn.execute("INSERT INTO schema_version (version) VALUES (?1)", [version])?;
        }
    }

    Ok(())
}
```

---

## Performance

### WebView2 Optimization

```rust
// Preload WebView with custom data directory to avoid cold starts
fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Pre-warm the database on startup
            let state: State<AppState> = app.state();
            let conn = state.db_pool.get()?;
            conn.execute("SELECT 1", [])?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

### IPC Batching

```rust
// Instead of many small IPC calls, batch data
#[command]
pub fn get_dashboard_data(
    state: State<'_, AppState>,
) -> Result<DashboardData, String> {
    // Single IPC call returns all dashboard data
    let conn = state.db_pool.get().map_err(|e| e.to_string())?;

    Ok(DashboardData {
        recent_items: get_recent_items(&conn, 20)?,
        stats: get_stats(&conn)?,
        notifications: get_unread_notifications(&conn)?,
        active_connections: state.ws_connections.len(),
    })
}

#[derive(Serialize)]
pub struct DashboardData {
    pub recent_items: Vec<Item>,
    pub stats: Stats,
    pub notifications: Vec<Notification>,
    pub active_connections: usize,
}
```

### Lazy Loading Pattern

```typescript
// Frontend: only load what's visible
async function loadRecords(page: number, pageSize: number) {
  return await invoke<PaginatedResult>("get_records", {
    offset: page * pageSize,
    limit: pageSize,
  });
}

// Virtual scrolling: request data as user scrolls
let currentPage = 0;
const observer = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting) {
    currentPage++;
    const moreData = await loadRecords(currentPage, 50);
    appendToList(moreData.items);
  }
});
observer.observe(document.querySelector("#load-trigger")!);
```

---

## Security

### Content Security Policy

```json
{
  "app": {
    "security": {
      "csp": {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "https:"],
        "connect-src": [
          "'self'",
          "https://api.example.com",
          "wss://ws.example.com"
        ],
        "font-src": ["'self'", "data:"]
      }
    }
  }
}
```

### Capability Scoping Best Practices

```json
// Minimal capability for a settings window — no file access, no shell
{
  "identifier": "settings-window",
  "description": "Restricted capability for settings",
  "windows": ["settings"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:window:allow-close"
  ]
}

// Main window gets broader access
{
  "identifier": "main-window",
  "description": "Full capability for main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "fs:default",
    "dialog:default",
    "shell:default",
    "http:default"
  ]
}
```

---

## Testing

### Testing Tauri Commands

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_record_serialization() {
        let record = Record {
            id: "test-1".into(),
            name: "Test".into(),
            data: serde_json::json!({"key": "value"}),
        };

        let json = serde_json::to_string(&record).unwrap();
        let deserialized: Record = serde_json::from_str(&json).unwrap();
        assert_eq!(deserialized.id, "test-1");
    }

    #[test]
    fn test_error_serialization() {
        let err = CommandError::NotFound("user-123".into());
        let json = serde_json::to_string(&err).unwrap();
        assert!(json.contains("not_found"));
    }

    #[tokio::test]
    async fn test_subprocess_lifecycle() {
        let manager = SubprocessManager::new();

        // Test with a simple command
        // In real tests, use a mock or a simple echo script
        let result = manager.spawn(
            "test-1".into(),
            "echo",
            &["hello"],
            mock_app_handle(),
        ).await;

        assert!(result.is_ok());
    }
}
```

### WebDriver Testing

```rust
// Run with: cargo test --test webdriver -- --ignored
#[cfg(test)]
mod webdriver_tests {
    use fantoccini::{Client, ClientBuilder};

    #[tokio::test]
    #[ignore] // requires running app + WebDriver
    async fn test_main_window_loads() {
        let client = ClientBuilder::native()
            .connect("http://localhost:4444")
            .await
            .expect("connect to WebDriver");

        // Wait for the app title
        let title = client.title().await.unwrap();
        assert!(title.contains("My Application"));

        // Click a button
        let btn = client.find(fantoccini::Locator::Css("#refresh-btn")).await.unwrap();
        btn.click().await.unwrap();

        client.close().await.unwrap();
    }
}
```

---

## Fincept Terminal Patterns

### Large-Scale Command Registration

Fincept Terminal registers 1400+ commands. Key patterns:

```rust
// Use a macro to reduce boilerplate for similar commands
macro_rules! register_data_commands {
    ($($name:ident => $handler:path),* $(,)?) => {
        tauri::generate_handler![
            $($handler),*
        ]
    };
}

// Group commands by domain module
// src-tauri/src/commands/market_data.rs — 200+ commands
// src-tauri/src/commands/portfolio.rs — 150+ commands
// src-tauri/src/commands/analytics.rs — 300+ commands
// etc.
```

### WebSocket State Management

```rust
pub struct WsState {
    pub connections: DashMap<String, WsConnection>,
    pub subscriptions: DashMap<String, Vec<String>>,  // topic -> [connection_ids]
    pub broadcast_tx: tokio::sync::broadcast::Sender<WsMessage>,
}

impl WsState {
    pub fn subscribe(&self, conn_id: &str, topic: &str) {
        self.subscriptions
            .entry(topic.to_string())
            .or_insert_with(Vec::new)
            .push(conn_id.to_string());
    }

    pub fn broadcast_to_topic(&self, topic: &str, message: WsMessage) {
        if let Some(subscribers) = self.subscriptions.get(topic) {
            for conn_id in subscribers.value() {
                if let Some(conn) = self.connections.get(conn_id) {
                    let _ = conn.sender.try_send(message.clone());
                }
            }
        }
    }
}
```

### Dual Python Venv Setup

```rust
// Fincept uses two Python environments:
// 1. Main venv: core financial computations
// 2. Analysis venv: ML/data science with heavier dependencies

pub struct PythonManager {
    main_venv: PathBuf,
    analysis_venv: PathBuf,
}

impl PythonManager {
    pub fn python_for_task(&self, task_type: TaskType) -> &Path {
        match task_type {
            TaskType::CoreComputation => &self.main_venv,
            TaskType::MLAnalysis | TaskType::DataScience => &self.analysis_venv,
        }
    }

    pub async fn ensure_venvs(&self, resource_dir: &Path) -> Result<(), AppError> {
        for venv in [&self.main_venv, &self.analysis_venv] {
            if !venv.exists() {
                create_venv(resource_dir, venv).await?;
            }
        }
        Ok(())
    }
}
```
