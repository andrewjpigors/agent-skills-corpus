---
name: migrate-from-e2b
description: Use when migrating sandbox code from E2B (@e2b/code-interpreter or e2b) to Blaxel (@blaxel/core or blaxel). Covers API mapping for sandbox creation, command execution, filesystem operations, pause/resume, and authentication in both TypeScript and Python. Reach for this skill when you encounter E2B SDK imports or need to replace E2B sandbox calls with Blaxel equivalents.
---

# Migrate from E2B to Blaxel

This guide covers migrating cloud sandbox code from **E2B** (`@e2b/code-interpreter` / `e2b`) to **Blaxel** (`@blaxel/core` / `blaxel`).

## Package replacement

| Language | E2B | Blaxel |
|----------|-----|--------|
| TypeScript | `@e2b/code-interpreter` or `e2b` | `@blaxel/core` |
| Python | `e2b-code-interpreter` or `e2b` | `blaxel` |

```bash
# TypeScript
npm uninstall @e2b/code-interpreter e2b
npm install @blaxel/core

# Python
pip uninstall e2b-code-interpreter e2b
pip install blaxel
```

## Authentication

| E2B | Blaxel |
|-----|--------|
| `E2B_API_KEY` env var | `BL_WORKSPACE` + `BL_API_KEY` env vars |
| Single API key, passed via env or `apiKey` option | CLI login, .env, env vars, or config file (auto-detected) |

Blaxel authenticates automatically when logged in via CLI (`bl login YOUR-WORKSPACE`). No need to set API keys in code.

## API mapping

### Imports

**TypeScript:**
```typescript
// BEFORE (E2B)
import { Sandbox } from '@e2b/code-interpreter'

// AFTER (Blaxel)
import { SandboxInstance } from '@blaxel/core'
```

**Python:**
```python
# BEFORE (E2B)
from e2b_code_interpreter import Sandbox

# AFTER (Blaxel)
from blaxel.core import SandboxInstance
```

### Sandbox creation

**TypeScript:**
```typescript
// BEFORE (E2B)
const sandbox = await Sandbox.create()
// With options:
const sandbox = await Sandbox.create({
  timeoutMs: 300_000,  // 5 min default, max 24h (Pro) / 1h (Hobby)
  envs: { NODE_ENV: 'production' },
  metadata: { project: 'my-app' },
})
// With template:
const sandbox = await Sandbox.create('my-template-id', {
  timeoutMs: 600_000,
})

// AFTER (Blaxel)
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/base-image:latest',
  region: 'us-pdx-1',
  memory: 2048,
  ports: [{ target: 3000, protocol: 'HTTP' }],
  envs: [
    { name: 'NODE_ENV', value: 'production' },
  ],
  labels: { project: 'my-app' },
  ttl: '24h',
})
```

**Python:**
```python
# BEFORE (E2B)
sandbox = Sandbox()
# With options:
sandbox = Sandbox(timeout=300, envs={"NODE_ENV": "production"}, metadata={"project": "my-app"})
# With template:
sandbox = Sandbox("my-template-id", timeout=600)

# AFTER (Blaxel)
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "blaxel/base-image:latest",
    "region": "us-pdx-1",
    "memory": 2048,
    "ports": [{"target": 3000, "protocol": "HTTP"}],
    "envs": [
        {"name": "NODE_ENV", "value": "production"},
    ],
    "labels": {"project": "my-app"},
    "ttl": "24h",
})
```

### Parameter mapping

| Parameter | E2B | Blaxel |
|-----------|-----|--------|
| Template / Image | `Sandbox.create('template-id')` | `image: 'blaxel/base-image:latest'` |
| Timeout | `timeoutMs: 300000` (max 24h Pro / 1h Hobby) | `ttl: '24h'` (configurable per quota tier) |
| Environment vars | `envs: { KEY: 'val' }` (flat object, set at creation, inherited by commands) | `envs: [{ name: 'KEY', value: 'val' }]` (array of objects at creation) |
| Secrets | N/A | `envs: [{ name: 'KEY', value: 'val', secret: true }]` |
| Metadata / Labels | `metadata: { k: 'v' }` | `labels: { k: 'v' }` |
| Region | Not configurable | `region: 'us-pdx-1'` |
| Memory | Fixed per template | `memory: 2048` (MB) |
| Ports | Implicit (all ports accessible via `getHost`) | `ports: [{ target: 3000, protocol: 'HTTP' }]` (declared at creation) |
| Name | Auto-generated ID | `name: 'my-sandbox'` (for idempotent creation) |
| Network / Internet | `allowInternetAccess: false`, `network: { allow/deny rules }` | `network: { vpcName: 'my-vpc', egressGatewayName: 'my-gw' }` (VPC + egress gateway). No fine-grained IP/domain rules |
| Secured access | `secure: true`, `sandbox.trafficAccessToken` | Private preview URLs with `public: false` + `preview.tokens.create(expiresAt)` |
| PTY / Terminal | `sandbox.pty.create({ cols, rows, onData })` | N/A (no interactive terminal support) |
| GPU | Not available | N/A |
| Per-command user | `user: 'root'` on commands/pty | N/A (commands run as default user) |
| Metrics | `sandbox.getMetrics()` — CPU, memory, disk | N/A (no metrics API) |

### Custom sandbox / templates

**TypeScript:**
```typescript
// BEFORE (E2B) - uses template IDs from E2B dashboard
// Templates are built via e2b CLI: e2b template build
const sandbox = await Sandbox.create('my-template-id')

// AFTER (Blaxel) - uses custom images deployed via `bl deploy`
// 1. Create template: bl new sandbox my-template
// 2. Edit the Dockerfile
// 3. Deploy: bl deploy
// 4. Use the deployed image:
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'my-custom-template-image',
  region: 'us-pdx-1',
  memory: 2048,
})
```

**Python:**
```python
# BEFORE (E2B) - uses template IDs from E2B dashboard
sandbox = Sandbox("my-template-id")

# AFTER (Blaxel) - uses custom images deployed via `bl deploy`
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "my-custom-template-image",
    "region": "us-pdx-1",
    "memory": 2048,
})
```

#### Template building methods mapping

E2B has programmatic template building via `Template.build()` with chainable methods. Blaxel uses standard Dockerfiles deployed with `bl deploy`. All E2B template methods map to Dockerfile instructions:

| E2B Template Method | Blaxel Dockerfile Equivalent |
|----|-----|
| `fromBaseImage()` | `FROM e2b-default-image` (use `blaxel/base-image:latest`) |
| `fromUbuntuImage(tag)` | `FROM ubuntu:tag` |
| `fromDebianImage(tag)` | `FROM debian:tag` |
| `fromPythonImage(tag)` | `FROM python:tag` |
| `fromNodeImage(tag)` | `FROM node:tag` |
| `fromBunImage(tag)` | `FROM oven/bun:tag` |
| `fromImage(name)` | `FROM name` |
| `fromDockerfile(content)` | Use the Dockerfile directly as the Blaxel template |
| `fromTemplate(name)` | Build on top of an existing deployed Blaxel template image |
| `runCmd(cmd)` | `RUN cmd` |
| `aptInstall(['curl', 'git'])` | `RUN apt-get update && apt-get install -y curl git` |
| `pipInstall(['numpy'])` | `RUN pip install numpy` |
| `npmInstall(['express'])` | `RUN npm install -g express` |
| `bunInstall(['hono'])` | `RUN bun install -g hono` |
| `gitClone(url, path)` | `RUN git clone url path` |
| `copy(src, dest)` | `COPY src dest` |
| `remove(path)` | `RUN rm -rf path` |
| `rename(old, new)` | `RUN mv old new` |
| `makeDir(path)` | `RUN mkdir -p path` |
| `makeSymlink(target, link)` | `RUN ln -s target link` |
| `setWorkdir(path)` | `WORKDIR path` |
| `setUser(user)` | `USER user` |
| `setEnvs({KEY: 'val'})` | `ENV KEY=val` |
| `setStartCmd(cmd)` | `CMD cmd` / configured via `entrypoint.sh` |

**Template versioning:** E2B supports `Template.assignTags()` and creation with `Sandbox.create('template:v1.0.0')`. Blaxel templates are deployed via `bl deploy` without version tagging.

**Template pre-building:** E2B's `Template.build()` and `Template.buildInBackground()` with `Template.getBuildStatus()`. Blaxel equivalent is `bl deploy` which builds and caches the image in Blaxel's private registry.

### Command execution

**TypeScript:**
```typescript
// BEFORE (E2B)
const result = await sandbox.commands.run('echo hello')
// result.stdout, result.stderr, result.exitCode

const result = await sandbox.commands.run('npm install', {
  envs: { NODE_ENV: 'production' },
  cwd: '/app',
})

// AFTER (Blaxel)
const result = await sandbox.process.exec({
  command: 'echo hello',
  waitForCompletion: true,
})
const result = await sandbox.process.exec({
  command: 'npm install',
  workingDir: '/app',
  env: { NODE_ENV: 'production' },
  waitForCompletion: true,
})
```

**Python:**
```python
# BEFORE (E2B)
result = sandbox.commands.run("echo hello")
# result.stdout, result.stderr, result.exit_code

result = sandbox.commands.run("npm install", envs={"NODE_ENV": "production"}, cwd="/app")

# AFTER (Blaxel)
result = await sandbox.process.exec({
    "command": "echo hello",
    "wait_for_completion": True,
})
result = await sandbox.process.exec({
    "command": "npm install",
    "working_dir": "/app",
    "env": {"NODE_ENV": "production"},
    "wait_for_completion": True,
})
```

### Background / streaming commands

**TypeScript:**
```typescript
// BEFORE (E2B) - background mode with callbacks
const command = await sandbox.commands.run('npm run dev', {
  background: true,
  cwd: '/app',
  envs: { NODE_ENV: 'development' },
  onStdout: (data) => console.log(data),
  onStderr: (data) => console.error(data),
})
// Later:
await sandbox.commands.kill(command.pid)

// AFTER (Blaxel) - native background mode with port waiting
const devServer = await sandbox.process.exec({
  name: 'dev-server',
  command: 'npm run dev -- --host 0.0.0.0',
  workingDir: '/app',
  waitForPorts: [3000],  // returns once port 3000 is open
})
// Or with log callbacks:
const proc = await sandbox.process.exec({
  name: 'dev-server',
  command: 'npm run dev -- --host 0.0.0.0',
  workingDir: '/app',
  waitForCompletion: false,
  onLog: (log) => console.log(log),
})
// Later:
await sandbox.process.kill('dev-server')
```

**Python:**
```python
# BEFORE (E2B) - background mode
command = sandbox.commands.run("npm run dev", background=True, cwd="/app",
    envs={"NODE_ENV": "development"},
    on_stdout=lambda data: print(data),
    on_stderr=lambda data: print(data),
)
# Later:
sandbox.commands.kill(command.pid)

# AFTER (Blaxel) - native background mode with port waiting
dev_server = await sandbox.process.exec({
    "name": "dev-server",
    "command": "npm run dev -- --host 0.0.0.0",
    "working_dir": "/app",
    "wait_for_ports": [3000],
})
# Later:
await sandbox.process.kill("dev-server")
```

### Log streaming / Process output

E2B streams output via `onStdout`/`onStderr` callbacks and returns results with `stdout`, `stderr`, `exitCode`. Blaxel offers similar callbacks plus additional methods for log retrieval and streaming.

**TypeScript:**
```typescript
// BEFORE (E2B) - callbacks + result properties
const result = await sandbox.commands.run('npm run build', {
  cwd: '/app',
  onStdout: (data) => console.log(data),
  onStderr: (data) => console.error(data),
})
console.log(result.stdout, result.stderr, result.exitCode)

// AFTER (Blaxel) - callbacks on exec
const result = await sandbox.process.exec({
  command: 'npm run build',
  workingDir: '/app',
  onLog: (log) => console.log(log),
  onStdout: (out) => process.stdout.write(out),
  onStderr: (err) => process.stderr.write(err),
  waitForCompletion: true,
})
// result.stdout, result.stderr, result.exitCode available after completion

// Stream logs from a running process:
const handle = sandbox.process.streamLogs('dev-server', {
  onLog: (log) => console.log(log),
  onStdout: (out) => process.stdout.write(out),
  onStderr: (err) => process.stderr.write(err),
  onError: (err) => console.error(err),
})
// Wait for the process to finish before closing the stream:
await handle.wait()

// Retrieve logs after the fact:
const logs = await sandbox.process.logs('dev-server')             // all
const stdout = await sandbox.process.logs('dev-server', 'stdout')
const stderr = await sandbox.process.logs('dev-server', 'stderr')
```

**Python:**
```python
# BEFORE (E2B)
result = sandbox.commands.run("npm run build", cwd="/app",
    on_stdout=lambda data: print(data),
    on_stderr=lambda data: print(data, file=sys.stderr),
)
print(result.stdout, result.stderr, result.exit_code)

# Background command wait (Python):
cmd = sandbox.commands.run("long-task", background=True)
cmd.wait()  # blocks until complete

# AFTER (Blaxel)
result = await sandbox.process.exec({
    "command": "npm run build",
    "working_dir": "/app",
    "on_log": lambda log: print(log),
    "wait_for_completion": True,
})

# Wait for a running process:
result = await sandbox.process.wait("dev-server", {
    "max_wait": 300000,  # 5 minutes in ms
    "interval": 2000,
})
```

### Sandbox lifecycle management

| Operation | E2B | Blaxel |
|-----------|-----|--------|
| Kill | `sandbox.kill()` or `Sandbox.kill(sandboxId)` | `sandbox.delete()` or `SandboxInstance.delete('name')` |
| Get info | `sandbox.getInfo()` → sandboxId, templateId, metadata, startedAt, endAt | `SandboxInstance.get('name')` → sandbox.metadata, sandbox.status, sandbox.spec, sandbox.lastUsedAt, sandbox.expiresIn |
| List sandboxes | `Sandbox.list({ query: { state, metadata }, limit, nextToken })` — paginated, filterable | `SandboxInstance.list()` — returns all sandboxes. Labels in metadata for client-side filtering |
| Update timeout | `sandbox.setTimeout(timeoutMs)` / `sandbox.set_timeout(timeout)` — resets countdown from "now" | `SandboxInstance.updateTtl('name', '48h')` — updates TTL. Also `SandboxInstance.updateLifecycle()` for expiration policies |
| Exit code | `result.exitCode` / `result.exit_code` | `result.exitCode` on process response, or `(await sandbox.process.get('name')).exitCode` |
| Process wait | `command.wait()` (Python background) | `sandbox.process.wait('name', { maxWait, interval })` |
| Process stop | `sandbox.commands.kill(pid)` (by PID) | `sandbox.process.stop('name')` (SIGTERM) or `sandbox.process.kill('name')` (SIGKILL) — by name |
| Process list | N/A | `sandbox.process.list()` |
| Process get | N/A | `sandbox.process.get('name')` — status, exitCode, pid, logs |
| Update labels | Via metadata at creation only | `SandboxInstance.updateMetadata('name', { labels: {...} })` |

### Filesystem operations

| Operation | E2B | Blaxel |
|-----------|-----|--------|
| Write file | `sandbox.files.write(path, content)` | `sandbox.fs.write(path, content)` |
| Read file | `sandbox.files.read(path)` | `sandbox.fs.read(path)` |
| List files | `sandbox.files.list(path)` | `sandbox.fs.ls(path)` |
| Create dir | `sandbox.files.makeDir(path)` / `make_dir(path)` | `sandbox.fs.mkdir(path)` |
| Delete file | `sandbox.commands.run('rm path')` | `sandbox.fs.rm(path)` / `sandbox.fs.rm(path, { recursive: true })` |
| Copy file | `sandbox.commands.run('cp ...')` | `sandbox.fs.cp(src, dest)` |
| File info | `sandbox.files.getInfo(path)` → size, mode, permissions, owner, modifiedTime | N/A (`fs.ls()` returns names only, no detailed metadata) |
| Watch files | `sandbox.files.watchDir(path, cb, { recursive? })` | `sandbox.fs.watch(path, callback, { withContent: true, ignore: ['node_modules'] })` |
| Write tree | `sandbox.files.write(files[])` (batch) | `sandbox.fs.writeTree(files, basePath)` / `write_tree(files, base)` |
| Write binary | `sandbox.files.write(path, buffer)` | `sandbox.fs.writeBinary(path, buffer)` / `write_binary(path, bytes)` |
| Read binary | `sandbox.files.read(path, { format: 'bytes' })` | `sandbox.fs.readBinary(path)` / `read_binary(path)` |
| Upload URL | `sandbox.uploadUrl(filename)` — pre-signed URL | N/A (use `sandbox.fs.write()` / `writeBinary()` via SDK. Auto multipart for >5MB) |
| Download URL | `sandbox.downloadUrl(path)` — pre-signed URL | N/A (use `sandbox.fs.read()` / `readBinary()` via SDK) |
| Fuzzy search | N/A | `sandbox.fs.search(query, path)` |
| Search content | N/A | `sandbox.fs.grep(pattern, path)` |
| Find files | N/A | `sandbox.fs.find(path, { patterns: ['*.ts'] })` |

**TypeScript:**
```typescript
// BEFORE (E2B)
await sandbox.files.write('/app/file.txt', 'hello')
const content = await sandbox.files.read('/app/file.txt')
const files = await sandbox.files.list('/app')

// AFTER (Blaxel)
await sandbox.fs.write('/app/file.txt', 'hello')
const content = await sandbox.fs.read('/app/file.txt')
const { subdirectories, files } = await sandbox.fs.ls('/app')

// Write multiple files at once:
await sandbox.fs.writeTree([
  { path: 'src/index.ts', content: 'console.log("hello")' },
  { path: 'package.json', content: '{"name":"app"}' },
], '/app')

// Delete files:
await sandbox.fs.rm('/app/temp.txt')
await sandbox.fs.rm('/app/old-dir', { recursive: true })

// Copy files:
await sandbox.fs.cp('/app/file.txt', '/backup/file.txt')

// Watch for file changes:
const handle = sandbox.fs.watch('/app/src', (event) => {
  console.log(event.op, event.path)
}, { withContent: true, ignore: ['node_modules', '.git'] })
// Later: handle.close()
```

**Python:**
```python
# BEFORE (E2B)
sandbox.files.write("/app/file.txt", "hello")
content = sandbox.files.read("/app/file.txt")
files = sandbox.files.list("/app")

# AFTER (Blaxel)
await sandbox.fs.write("/app/file.txt", "hello")
content = await sandbox.fs.read("/app/file.txt")
listing = await sandbox.fs.ls("/app")

# Write multiple files at once:
await sandbox.fs.write_tree([
    {"path": "src/index.ts", "content": 'console.log("hello")'},
    {"path": "package.json", "content": '{"name":"app"}'},
], "/app")

# Delete files:
await sandbox.fs.rm("/app/temp.txt")
await sandbox.fs.rm("/app/old-dir", recursive=True)

# Copy files:
await sandbox.fs.cp("/app/file.txt", "/backup/file.txt")

# Watch for file changes:
def on_change(event):
    print(event.op, event.path)

handle = sandbox.fs.watch("/app/src", on_change, {
    "with_content": True,
    "ignore": ["node_modules", ".git"]
})
# Later: handle["close"]()
```

### Preview URLs

E2B provides `getHost()` / `get_host()` for accessing sandbox ports. Blaxel has dedicated preview URL management with access control.

**TypeScript:**
```typescript
// BEFORE (E2B) - all ports accessible via getHost
const host = sandbox.getHost(3000)
// Returns: xxxx-3000.e2b.dev (always public, no access control)

// AFTER (Blaxel) - dedicated preview URL with public/private access control
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'app-preview' },
  spec: { port: 3000, public: true },
})
const url = preview.spec?.url  // https://xxxx.preview.bl.run
```

**Python:**
```python
# BEFORE (E2B)
host = sandbox.get_host(3000)
# Returns: xxxx-3000.e2b.dev

# AFTER (Blaxel)
preview = await sandbox.previews.create_if_not_exists({
    "metadata": {"name": "app-preview"},
    "spec": {"port": 3000, "public": True},
})
url = preview.spec.url  # https://xxxx.preview.bl.run
```

#### Secured / Private access

E2B uses `secure: true` with `sandbox.trafficAccessToken` for restricted access. Blaxel uses private preview URLs with token-based authentication.

**TypeScript:**
```typescript
// BEFORE (E2B) - secured sandbox
const sandbox = await Sandbox.create({ secure: true })
const host = sandbox.getHost(3000)
// Access requires X-Access-Token header: sandbox.trafficAccessToken

// AFTER (Blaxel) - private preview with token
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'app-preview' },
  spec: { port: 3000, public: false },
})
const token = await preview.tokens.create(new Date(Date.now() + 3600000))
// Access: preview.spec?.url + "?bl_preview_token=" + token.value

// Or use sessions for SDK-based frontend access:
const session = await sandbox.sessions.create({
  expiresAt: new Date(Date.now() + 3600000),
})
// Pass session token to frontend
```

### Pause / Resume

E2B has explicit `pause()` / `resume()` methods (beta). Blaxel auto-scales to zero and resumes transparently.

**TypeScript:**
```typescript
// BEFORE (E2B) - explicit pause/resume (beta)
const sandboxId = sandbox.sandboxId
await sandbox.pause()
// ... later ...
const sandbox = await Sandbox.connect(sandboxId)  // auto-resumes if paused

// AFTER (Blaxel) - automatic: sandboxes auto-pause after ~5s inactivity
// and resume in <25ms on the next API call. No explicit pause/resume needed.
// Just reconnect by name:
const sandbox = await SandboxInstance.get('my-sandbox')
```

**Python:**
```python
# BEFORE (E2B) - explicit pause/resume (beta)
sandbox_id = sandbox.sandbox_id
sandbox.pause()
# ... later ...
sandbox = Sandbox.connect(sandbox_id)  # auto-resumes if paused

# AFTER (Blaxel) - automatic, just reconnect by name
sandbox = await SandboxInstance.get("my-sandbox")
```

#### Snapshots

E2B supports explicit snapshots for saving and restoring sandbox state. Blaxel auto-preserves state through scale-to-zero.

**TypeScript:**
```typescript
// BEFORE (E2B) - explicit snapshots
const snapshot = await sandbox.createSnapshot()
const snapshotId = snapshot.snapshotId
await sandbox.kill()
// ... later - restore from snapshot:
const restored = await Sandbox.create(snapshotId)

// List and manage snapshots:
const snapshots = await Sandbox.listSnapshots()
await Sandbox.deleteSnapshot(snapshotId)

// AFTER (Blaxel) - automatic state preservation
// State (memory + filesystem) persists through auto scale-to-zero.
// No explicit snapshots needed — just reconnect:
const sandbox = await SandboxInstance.get('my-sandbox')

// To share pre-built state across multiple sandboxes,
// use volume templates: bl new volume-template
```

### Sandbox info & cleanup

**TypeScript:**
```typescript
// BEFORE (E2B)
const info = await sandbox.getInfo()  // sandboxId, templateId, metadata, etc.
await sandbox.kill()

// AFTER (Blaxel)
const sandbox = await SandboxInstance.get('my-sandbox')  // full sandbox details
await sandbox.delete()
```

**Python:**
```python
# BEFORE (E2B)
info = sandbox.get_info()
sandbox.kill()

# AFTER (Blaxel)
sandbox = await SandboxInstance.get("my-sandbox")
await sandbox.delete()
```

### Reconnect to existing sandbox

**TypeScript:**
```typescript
// BEFORE (E2B) - connect by opaque ID
const sandbox = await Sandbox.connect(sandboxId)

// AFTER (Blaxel) - connect by human-readable name
const sandbox = await SandboxInstance.get('my-sandbox')
```

**Python:**
```python
# BEFORE (E2B) - connect by opaque ID
sandbox = Sandbox.connect(sandbox_id)

# AFTER (Blaxel) - connect by human-readable name
sandbox = await SandboxInstance.get("my-sandbox")
```

### Code Interpreter

E2B's `@e2b/code-interpreter` package provides `runCode()` for executing code in isolated interpreters with result/chart detection. Blaxel has a `CodeInterpreter` class with similar capabilities.

**TypeScript:**
```typescript
// BEFORE (E2B) - code interpreter
import { Sandbox } from '@e2b/code-interpreter'

const sandbox = await Sandbox.create()
const execution = await sandbox.runCode('print("hello")', {
  language: 'python',
  onStdout: (data) => console.log(data),
  onStderr: (data) => console.error(data),
})
console.log(execution.results, execution.logs, execution.error)

// Code contexts for stateful execution:
const context = await sandbox.createCodeContext({ language: 'python', cwd: '/app' })
await sandbox.runCode('x = 42', { context })
await sandbox.runCode('print(x)', { context })  // prints 42

// AFTER (Blaxel) - CodeInterpreter class
import { CodeInterpreter } from '@blaxel/core'

const interpreter = await CodeInterpreter.createIfNotExists({
  name: 'my-interpreter',
  // Automatically uses "blaxel/jupyter-server" image
  // Default lifecycle: ttl-idle: 30m
})
const result = await interpreter.runCode({
  code: 'print("hello")',
  language: 'python',
  onStdout: (out) => console.log(out),
  onStderr: (err) => console.error(err),
})

// Stateful code contexts:
const context = await interpreter.createCodeContext({ language: 'python', name: 'my-ctx' })
await interpreter.runCode({ code: 'x = 42', context: 'my-ctx' })
await interpreter.runCode({ code: 'print(x)', context: 'my-ctx' })  // prints 42
```

**Python:**
```python
# BEFORE (E2B)
from e2b_code_interpreter import Sandbox

sandbox = Sandbox()
execution = sandbox.run_code("print('hello')", language="python")
print(execution.results, execution.logs, execution.error)

# AFTER (Blaxel)
from blaxel.core import CodeInterpreter

interpreter = await CodeInterpreter.create_if_not_exists({
    "name": "my-interpreter",
})
result = await interpreter.run_code({
    "code": "print('hello')",
    "language": "python",
})
```

> **Note:** E2B automatically detects Matplotlib charts and returns them as base64 PNG or structured chart objects. Blaxel's CodeInterpreter does not have automatic chart detection — chart output is captured as standard output from the Jupyter kernel.

### Git integration

E2B provides a full `sandbox.git.*` API for git operations. Blaxel has no dedicated git API — use `process.exec()` with git commands instead.

**TypeScript:**
```typescript
// BEFORE (E2B) - dedicated git API
await sandbox.git.clone('https://github.com/user/repo.git', { path: '/app', depth: 1 })
await sandbox.git.configureUser('name', 'email@example.com')
const status = await sandbox.git.status('/app')
await sandbox.git.add('/app')
await sandbox.git.commit('/app', 'my commit')
await sandbox.git.push('/app', { remote: 'origin', branch: 'main' })

// AFTER (Blaxel) - git via process.exec
await sandbox.process.exec({
  command: 'git clone --depth 1 https://github.com/user/repo.git /app',
  waitForCompletion: true,
})
await sandbox.process.exec({
  command: 'git config user.name "name" && git config user.email "email@example.com"',
  workingDir: '/app',
  waitForCompletion: true,
})
await sandbox.process.exec({
  command: 'git add . && git commit -m "my commit" && git push origin main',
  workingDir: '/app',
  env: { GIT_TOKEN: 'your-token' },
  waitForCompletion: true,
})
```

> **Note:** Git must be installed in the sandbox image. Most Blaxel base images include git. For private repos, pass credentials via `env` parameter or configure git credential storage.

### MCP integration

E2B provides MCP gateway access via `getMcpUrl()` / `getMcpToken()`. Blaxel sandboxes have a built-in MCP server.

**TypeScript:**
```typescript
// BEFORE (E2B) - MCP gateway
const mcpUrl = sandbox.getMcpUrl()
const mcpToken = sandbox.getMcpToken()
// Connect via HTTP transport with Bearer token

// AFTER (Blaxel) - built-in MCP server per sandbox
// Every sandbox exposes MCP at https://<SANDBOX_URL>/mcp
// Use SDK helpers for framework-specific tool definitions:
import { blTools } from '@blaxel/vercel'  // or @blaxel/langgraph, @blaxel/mastra, etc.
const tools = await blTools(['sandbox/my-sandbox'])
```

**Python:**
```python
# BEFORE (E2B)
mcp_url = sandbox.get_mcp_url()
mcp_token = sandbox.get_mcp_token()

# AFTER (Blaxel)
from blaxel.openai import bl_tools  # or blaxel.langgraph, blaxel.pydantic, etc.
tools = await bl_tools(["sandbox/my-sandbox"])
```

## Key differences

- **No API key in code**: Blaxel SDK auto-detects credentials from CLI login, .env, env vars, or config file
- **Named sandboxes**: Blaxel supports `createIfNotExists` / `create_if_not_exists` with a `name` for idempotent creation; E2B uses opaque auto-generated IDs. Blaxel uses human-readable names, not opaque IDs
- **Ports declared at creation**: Blaxel requires ports at sandbox creation time; they cannot be added later. Ports 80, 443, 8080 are reserved. E2B exposes all ports implicitly
- **Region selection**: Blaxel lets you choose a region (`us-pdx-1`); E2B does not expose region selection
- **Auto scale-to-zero**: Blaxel sandboxes auto-pause after ~5s of inactivity and resume in <25ms. No explicit pause/resume needed. E2B requires explicit `pause()`/`resume()` (beta) or `createSnapshot()`
- **Preview URLs vs getHost**: Blaxel has a dedicated preview URL system with public/private access control and token-based auth; E2B uses `getHost(port)` / `get_host(port)` which provides public access only (unless `secure: true`)
- **Async by default**: Blaxel Python SDK is async-first (all calls use `await`); E2B Python SDK is sync by default
- **Environment variables**: E2B uses a flat object at creation (`envs: { KEY: 'val' }`), inherited by all commands. Blaxel uses an array at creation (`envs: [{ name: 'KEY', value: 'val' }]`) and a flat object per-command (`env: { KEY: 'val' }`). Blaxel supports `secret: true` for sensitive values
- **Process naming and management**: Blaxel processes can be named for later reference (`get`, `stop`, `kill`, `list`, `wait`, `logs` by name); E2B returns command objects with PIDs
- **Log streaming**: E2B has `onStdout`/`onStderr` callbacks. Blaxel additionally offers `onLog` callback, `process.streamLogs()` with handle (`close`/`wait`), and `process.logs()` with type filtering (stdout/stderr/all)
- **`waitForPorts`** / **`wait_for_ports`**: Blaxel can wait for a port to be open before returning; E2B requires manual polling
- **Dev server binding**: Dev servers must bind to `0.0.0.0` (not `localhost`) for preview URLs to work in Blaxel
- **~50% memory reserved for tmpfs**: Blaxel uses half of sandbox memory for the in-memory filesystem. Use volumes for extra storage
- **No PTY / interactive terminal**: E2B has full `sandbox.pty.*` API. Blaxel has no interactive terminal support
- **No dedicated git API**: E2B has `sandbox.git.*` for git operations. Blaxel uses `process.exec()` with git commands
- **No sandbox metrics**: E2B provides `getMetrics()` for CPU/memory/disk usage. Blaxel has no metrics API
- **No webhooks/events**: E2B has lifecycle events API and webhook registration. Blaxel has no equivalent
- **No pre-signed URLs**: E2B has `uploadUrl()`/`downloadUrl()` for direct browser-to-sandbox file transfer. Blaxel uses SDK methods (`fs.write`/`fs.read`) instead
- **Template building**: E2B has programmatic `Template.build()` with chainable methods. Blaxel uses standard Dockerfiles + `bl deploy`
- **MCP integration**: E2B uses `getMcpUrl()`/`getMcpToken()`. Blaxel has a built-in MCP server per sandbox + framework-specific `blTools()` helpers
- **Volumes**: Blaxel supports persistent volumes (`VolumeInstance`) attached at sandbox creation. E2B does not have a volumes concept
- **Code Interpreter**: E2B has `runCode()` with chart detection. Blaxel has `CodeInterpreter` class with `runCode()` and code contexts (no chart detection)

## Complete migration example

### TypeScript

**BEFORE (E2B):**
```typescript
import { Sandbox } from '@e2b/code-interpreter'

const sandbox = await Sandbox.create({
  timeoutMs: 600_000,
  envs: { NODE_ENV: 'production' },
  metadata: { project: 'demo' },
})

await sandbox.files.write('/app/index.js', 'console.log("hello")')
const result = await sandbox.commands.run('node /app/index.js')
console.log(result.stdout)

// Start dev server in background
const cmd = await sandbox.commands.run('cd /app && npm run dev', {
  background: true,
  onStdout: (data) => console.log(data),
})

const host = sandbox.getHost(3000)
console.log(`Preview: https://${host}`)

await sandbox.commands.kill(cmd.pid)
await sandbox.kill()
```

**AFTER (Blaxel):**
```typescript
import { SandboxInstance } from '@blaxel/core'

const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/node:latest',
  region: 'us-pdx-1',
  memory: 2048,
  ports: [{ target: 3000, protocol: 'HTTP' }],
  envs: [{ name: 'NODE_ENV', value: 'production' }],
  labels: { project: 'demo' },
  ttl: '24h',
})

await sandbox.fs.write('/app/index.js', 'console.log("hello")')
const result = await sandbox.process.exec({
  command: 'node /app/index.js',
  workingDir: '/app',
  waitForCompletion: true,
})

// Start dev server, wait for port
await sandbox.process.exec({
  name: 'dev-server',
  command: 'npm run dev -- --host 0.0.0.0',
  workingDir: '/app',
  waitForPorts: [3000],
})

// Get a shareable preview URL
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'app-preview' },
  spec: { port: 3000, public: true },
})
console.log(`Preview: ${preview.spec?.url}`)

await sandbox.process.kill('dev-server')
await sandbox.delete()
```

### Python

**BEFORE (E2B):**
```python
from e2b_code_interpreter import Sandbox

sandbox = Sandbox(timeout=600, envs={"NODE_ENV": "production"}, metadata={"project": "demo"})

sandbox.files.write("/app/index.js", 'console.log("hello")')
result = sandbox.commands.run("node /app/index.js")
print(result.stdout)

# Start dev server in background
cmd = sandbox.commands.run("cd /app && npm run dev", background=True,
    on_stdout=lambda data: print(data),
)

host = sandbox.get_host(3000)
print(f"Preview: https://{host}")

sandbox.commands.kill(cmd.pid)
sandbox.kill()
```

**AFTER (Blaxel):**
```python
import asyncio
from blaxel.core import SandboxInstance

async def main():
    sandbox = await SandboxInstance.create_if_not_exists({
        "name": "my-sandbox",
        "image": "blaxel/node:latest",
        "region": "us-pdx-1",
        "memory": 2048,
        "ports": [{"target": 3000, "protocol": "HTTP"}],
        "envs": [{"name": "NODE_ENV", "value": "production"}],
        "labels": {"project": "demo"},
        "ttl": "24h",
    })

    await sandbox.fs.write("/app/index.js", 'console.log("hello")')
    result = await sandbox.process.exec({
        "command": "node /app/index.js",
        "working_dir": "/app",
        "wait_for_completion": True,
    })

    # Start dev server, wait for port
    await sandbox.process.exec({
        "name": "dev-server",
        "command": "npm run dev -- --host 0.0.0.0",
        "working_dir": "/app",
        "wait_for_ports": [3000],
    })

    # Get a shareable preview URL
    preview = await sandbox.previews.create_if_not_exists({
        "metadata": {"name": "app-preview"},
        "spec": {"port": 3000, "public": True},
    })
    print(f"Preview: {preview.spec.url}")

    await sandbox.process.kill("dev-server")
    await sandbox.delete()

asyncio.run(main())
```

## Resources

- Blaxel docs: https://docs.blaxel.ai
- Blaxel sandbox images: https://github.com/blaxel-ai/sandbox/tree/main/hub
- E2B docs: https://e2b.dev/docs
- SDK reference (TypeScript): `@blaxel/core` — see ./references/sdk-typescript.md
- SDK reference (Python): `blaxel` — see ./references/sdk-python.md
