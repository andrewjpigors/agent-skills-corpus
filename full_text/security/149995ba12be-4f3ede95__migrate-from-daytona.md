---
name: migrate-from-daytona
description: Use when migrating sandbox code from Daytona (@daytonaio/sdk or daytona_sdk) to Blaxel (@blaxel/core or blaxel). Covers API mapping for sandbox creation, process execution, filesystem operations, and authentication in both TypeScript and Python. Reach for this skill when you encounter Daytona SDK imports or need to replace Daytona sandbox calls with Blaxel equivalents.
---

# Migrate from Daytona to Blaxel

This guide covers migrating cloud sandbox code from **Daytona** (`@daytonaio/sdk` / `daytona_sdk`) to **Blaxel** (`@blaxel/core` / `blaxel`).

## Package replacement

| Language | Daytona | Blaxel |
|----------|---------|--------|
| TypeScript | `@daytonaio/sdk` | `@blaxel/core` |
| Python | `daytona_sdk` or `daytona` | `blaxel` |

```bash
# TypeScript
npm uninstall @daytonaio/sdk
npm install @blaxel/core

# Python
pip uninstall daytona_sdk daytona
pip install blaxel
```

## Authentication

| Daytona | Blaxel |
|---------|--------|
| `DAYTONA_API_KEY` env var | `BL_WORKSPACE` + `BL_API_KEY` env vars |
| Passed to `new Daytona({ apiKey })` / `Daytona(api_key=...)` | Auto-detected by SDK (CLI login, .env, env vars, or config file) |

Blaxel authenticates automatically when logged in via CLI (`bl login YOUR-WORKSPACE`). No need to pass credentials to constructors.

## API mapping

### Imports

**TypeScript:**
```typescript
// BEFORE (Daytona)
import { Daytona, Sandbox as DaytonaSandbox } from '@daytonaio/sdk'

// AFTER (Blaxel)
import { SandboxInstance } from '@blaxel/core'
```

**Python:**
```python
# BEFORE (Daytona)
from daytona_sdk import Daytona, CreateSandboxParams

# AFTER (Blaxel)
from blaxel.core import SandboxInstance
```

### Sandbox creation

Daytona requires instantiating a client first, then calling `create()`. Blaxel uses static methods directly on `SandboxInstance`.

**TypeScript:**
```typescript
// BEFORE (Daytona)
const daytona = new Daytona({ apiKey: process.env.DAYTONA_API_KEY })
const sandbox = await daytona.create({
  language: 'python',
  image: 'debian:slim',
  resources: { memory: 2, cpu: 1 },  // memory in GB
  envVars: { NODE_ENV: 'production' },
  labels: { project: 'my-app' },
  target: 'us',  // region: 'us', 'eu', or 'asia'
  autoStopInterval: 15,  // minutes
})

// AFTER (Blaxel)
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/base-image:latest',
  region: 'us-pdx-1',
  memory: 2048,  // memory in MB
  ports: [{ target: 3000, protocol: 'HTTP' }],
  envs: [
    { name: 'NODE_ENV', value: 'production' },
  ],
  labels: { project: 'my-app' },
})
```

**Python:**
```python
# BEFORE (Daytona)
daytona = Daytona(api_key=os.environ["DAYTONA_API_KEY"])
sandbox = await daytona.create(CreateSandboxParams(
    language="python",
    image="debian:slim",
    resources=Resources(cpu=1, memory=2),
    env_vars={"NODE_ENV": "production"},
    labels={"project": "my-app"},
    target="us",
    auto_stop_interval=15,
))

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
})
```

### Parameter mapping

| Parameter | Daytona | Blaxel |
|-----------|---------|--------|
| Image | `image: 'debian:slim'` | `image: 'blaxel/base-image:latest'` |
| Memory | `resources: { memory: 2 }` (GB) | `memory: 2048` (MB) |
| CPU | `resources: { cpu: 1 }` | Not needed (auto-allocated: CPU cores = memory / 2048) |
| Region | `target: 'us'` / `'eu'` / `'asia'` | `region: 'us-pdx-1'` |
| Environment vars | `envVars: { KEY: 'val' }` (flat object) | `envs: [{ name: 'KEY', value: 'val' }]` (array of objects) |
| Secrets | N/A | `envs: [{ name: 'KEY', value: 'val', secret: true }]` |
| Labels | `labels: { k: 'v' }` | `labels: { k: 'v' }` |
| Auto-stop | `autoStopInterval: 15` (minutes) | Automatic (~5s inactivity, resumes in <25ms). For idle-based *deletion*: `lifecycle: { expirationPolicies: [{ type: 'ttl-idle', value: '7d', action: 'delete' }] }` |
| Auto-archive | `autoArchiveInterval: 10080` (minutes) | Not needed (state preserved in standby) |
| Auto-delete | `autoDeleteInterval: 43200` (minutes) | `lifecycle: { expirationPolicies: [{ type: 'ttl', value: '30d', action: 'delete' }] }` |
| Ephemeral | `ephemeral: true` | Use `sandbox.delete()` when done |
| Name | `name: 'my-sandbox'` | `name: 'my-sandbox'` |
| Ports | N/A (all ports accessible via preview URL) | `ports: [{ target: 3000, protocol: 'HTTP' }]` (declared at creation) |
| TTL | N/A | `ttl: '24h'` |
| GPU | `resources: { gpu: 1 }` | N/A (Blaxel sandboxes are CPU-only) |
| Disk | `resources: { disk: 10 }` (GiB) | N/A (Blaxel uses ~50% memory for tmpfs; use volumes for extra storage) |
| Network control | `networkBlockAll: true`, `networkAllowList: '10.0.0.0/8'` | `network: { vpcName: 'my-vpc', egressGatewayName: 'my-gw' }` (VPC + egress gateway). No CIDR rules |
| Public access | `public: true` (all ports accessible) | Per-port via `previews.createIfNotExists({ spec: { public: true } })` |
| User | `user: 'root'` | N/A (commands run as default user) |
| PTY / Terminal | `sandbox.process.createPty({ cols, rows, onData })` | N/A (no interactive terminal support) |
| SSH access | `sandbox.createSshAccess(expiresInMinutes)` | N/A (no SSH access) |
| LSP | `sandbox.createLspServer(languageId, path)` | N/A (no LSP API; Blaxel has `sandbox.codegen.reranking()` for code search) |
| Computer Use | `sandbox.computerUse.*` (mouse, keyboard, screenshot) | N/A (no desktop automation) |
| Metrics | N/A | N/A |

### Custom sandbox / templates

**TypeScript:**
```typescript
// BEFORE (Daytona) - uses snapshots
const sandbox = await daytona.create({
  snapshot: 'my-template',
  autoStopInterval: 1,
})

// AFTER (Blaxel) - uses custom images deployed via `bl deploy`
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'my-custom-template-image',
  region: 'us-pdx-1',
  memory: 2048,
})
```

**Python:**
```python
# BEFORE (Daytona) - uses snapshots
sandbox = await daytona.create(CreateSandboxParams(
    snapshot="my-template",
    auto_stop_interval=1,
))

# AFTER (Blaxel) - uses custom images deployed via `bl deploy`
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "my-custom-template-image",
    "region": "us-pdx-1",
    "memory": 2048,
})
```

#### Image builder mapping

Daytona has a declarative `Image` builder with chainable methods. Blaxel uses standard Dockerfiles deployed via `bl deploy`.

| Daytona Image Builder | Dockerfile Equivalent |
|---|---|
| `Image.base('ubuntu:22.04')` | `FROM ubuntu:22.04` |
| `Image.debianSlim('3.11')` | `FROM python:3.11-slim` |
| `Image.fromDockerfile(path)` | Use that Dockerfile directly with `bl deploy` |
| `.pipInstall(['numpy', 'pandas'])` | `RUN pip install numpy pandas` |
| `.pipInstallFromRequirements('requirements.txt')` | `COPY requirements.txt . && RUN pip install -r requirements.txt` |
| `.pipInstallFromPyproject('pyproject.toml')` | `COPY pyproject.toml . && RUN pip install .` |
| `.runCommands(['apt-get update', 'apt-get install -y curl'])` | `RUN apt-get update && apt-get install -y curl` |
| `.addLocalFile('app.py', '/app/app.py')` | `COPY app.py /app/app.py` |
| `.addLocalDir('./src', '/app/src')` | `COPY ./src /app/src` |
| `.env({ KEY: 'val' })` | `ENV KEY=val` |
| `.workdir('/app')` | `WORKDIR /app` |
| `.entrypoint(['python3', 'app.py'])` | `ENTRYPOINT ["python3", "app.py"]` |
| `.cmd(['--port', '8080'])` | `CMD ["--port", "8080"]` |
| `.dockerfileCommands('RUN echo hello')` | `RUN echo hello` (add directly to Dockerfile) |

Deploy custom images with:
```bash
bl deploy -t sandbox --name my-template --dir ./path/to/Dockerfile/dir
```

### Command execution

**TypeScript:**
```typescript
// BEFORE (Daytona)
const result = await sandbox.process.executeCommand('echo hello')
const result = await sandbox.process.executeCommand(command, workingDir, envVars)

// Stateless code execution:
const result = await sandbox.process.codeRun('print("hello")')

// Stateful code execution (Python only):
const context = await sandbox.process.createContext()
await sandbox.process.runCode('x = 42', context)
await sandbox.process.runCode('print(x)', context)  // remembers x

// AFTER (Blaxel)
const result = await sandbox.process.exec({
  command: 'echo hello',
  waitForCompletion: true,
})
const result = await sandbox.process.exec({
  command: command,
  workingDir: '/app',
  env: { NODE_ENV: 'production' },
  waitForCompletion: true,
})
// For code execution, use the command directly:
const result = await sandbox.process.exec({
  command: 'python3 -c "print(42)"',
  waitForCompletion: true,
})
```

**Python:**
```python
# BEFORE (Daytona)
result = await sandbox.process.execute_command("echo hello")
result = await sandbox.process.execute_command(command, cwd="/app", env={"KEY": "val"})
result = await sandbox.process.code_run('print("hello")')

# Stateful code execution:
context = await sandbox.process.create_context()
await sandbox.process.run_code("x = 42", context)
await sandbox.process.run_code("print(x)", context)

# AFTER (Blaxel)
result = await sandbox.process.exec({
    "command": "echo hello",
    "wait_for_completion": True,
})
result = await sandbox.process.exec({
    "command": command,
    "working_dir": "/app",
    "env": {"KEY": "val"},
    "wait_for_completion": True,
})
# For code execution, use the command directly:
result = await sandbox.process.exec({
    "command": 'python3 -c "print(42)"',
    "wait_for_completion": True,
})
```

### Long-running processes (dev servers)

**TypeScript:**
```typescript
// BEFORE (Daytona) - no native streaming, must redirect to temp file and poll
const bgCommand = `cd /app && npm run dev > /tmp/output.log 2>&1 & echo $! > /tmp/pid.txt`
await sandbox.process.executeCommand(bgCommand, undefined, envVars)
// ... poll /tmp/output.log ...

// Or use interactive sessions:
await sandbox.process.createSession('dev')
await sandbox.process.executeSessionCommand('dev', {
  command: 'npm run dev',
  runAsync: true,
})

// AFTER (Blaxel) - native background mode with port waiting
const devServer = await sandbox.process.exec({
  name: 'dev-server',
  command: 'npm run dev -- --host 0.0.0.0',
  workingDir: '/app',
  waitForPorts: [3000],  // returns once port 3000 is open
})
```

**Python:**
```python
# BEFORE (Daytona) - no native streaming
bg_command = "cd /app && npm run dev > /tmp/output.log 2>&1 & echo $! > /tmp/pid.txt"
await sandbox.process.execute_command(bg_command, env=env_vars)

# Or use interactive sessions:
await sandbox.process.create_session("dev")
await sandbox.process.execute_session_command("dev", {
    "command": "npm run dev",
    "run_async": True,
})

# AFTER (Blaxel) - native background mode with port waiting
dev_server = await sandbox.process.exec({
    "name": "dev-server",
    "command": "npm run dev -- --host 0.0.0.0",
    "working_dir": "/app",
    "wait_for_ports": [3000],
})
```

### Log streaming / Process output

Daytona uses session-based command logs with `getSessionCommandLogs()` and streaming via `onStdout`/`onStderr` callbacks. Blaxel provides callbacks on `process.exec()` plus dedicated log streaming methods.

**TypeScript:**
```typescript
// BEFORE (Daytona) - session-based log retrieval
await sandbox.process.createSession('build')
await sandbox.process.executeSessionCommand('build', { command: 'npm run build' })
const logs = await sandbox.process.getSessionCommandLogs('build', commandId)

// Streaming with callbacks:
await sandbox.process.executeCommand('npm run build', undefined, undefined, {
  onStdout: (data) => console.log('stdout:', data),
  onStderr: (data) => console.error('stderr:', data),
})

// AFTER (Blaxel) - callbacks on exec + dedicated log methods
const result = await sandbox.process.exec({
  name: 'build',
  command: 'npm run build',
  workingDir: '/app',
  waitForCompletion: true,
  onLog: (log) => console.log(log),
  onStdout: (data) => console.log('stdout:', data),
  onStderr: (data) => console.error('stderr:', data),
})

// Stream logs from a running process:
const handle = sandbox.process.streamLogs('build', {
  onLog: (log) => console.log(log),
  onStdout: (data) => console.log('stdout:', data),
  onStderr: (data) => console.error('stderr:', data),
})
// Wait for the process to finish before closing the stream:
await handle.wait()

// Retrieve logs after completion:
const logs = await sandbox.process.logs('build')             // all logs
const stdout = await sandbox.process.logs('build', 'stdout') // stdout only
const stderr = await sandbox.process.logs('build', 'stderr') // stderr only
```

**Python:**
```python
# BEFORE (Daytona) - session-based log retrieval
await sandbox.process.create_session("build")
await sandbox.process.execute_session_command("build", {"command": "npm run build"})
logs = await sandbox.process.get_session_command_logs("build", command_id)

# AFTER (Blaxel) - callbacks on exec + dedicated log methods
result = await sandbox.process.exec({
    "name": "build",
    "command": "npm run build",
    "working_dir": "/app",
    "wait_for_completion": True,
    "on_log": lambda log: print(log),
    "on_stdout": lambda data: print("stdout:", data),
    "on_stderr": lambda data: print("stderr:", data),
})

# Stream logs from a running process:
handle = await sandbox.process.stream_logs("build", {
    "on_log": lambda log: print(log),
})
# Wait for the process to finish before closing the stream:
await handle.wait()

# Retrieve logs after completion:
logs = await sandbox.process.logs("build")              # all logs
stdout = await sandbox.process.logs("build", "stdout")  # stdout only
```

### Filesystem operations

| Operation | Daytona | Blaxel |
|-----------|---------|--------|
| Write file | `sandbox.fs.uploadFile(Buffer.from(content), path)` / `upload_file(bytes, path)` | `sandbox.fs.write(path, content)` |
| Read file | `sandbox.fs.downloadFile(path)` / `download_file(path)` | `sandbox.fs.read(path)` |
| List files | `sandbox.fs.listFiles(path)` / `list_files(path)` | `sandbox.fs.ls(path)` |
| Write tree | N/A | `sandbox.fs.writeTree(files, basePath)` / `write_tree(files, base)` |
| Create dir | N/A (use `executeCommand('mkdir -p ...')`) | `sandbox.fs.mkdir(path)` |
| Search files (content) | `sandbox.fs.findFiles(path, pattern)` (content grep) | `sandbox.fs.grep(pattern, path)` |
| Search files (glob) | `sandbox.fs.searchFiles(path, pattern)` (glob) | `sandbox.fs.find(path, { patterns: ['*.ts'] })` |
| Fuzzy search | N/A | `sandbox.fs.search(query, path)` |
| Delete file | `sandbox.fs.deleteFile(path, recursive?)` | `sandbox.fs.rm(path)` / `sandbox.fs.rm(path, { recursive: true })` |
| Move file | `sandbox.fs.moveFiles(source, dest)` | No native move — use `sandbox.fs.cp(src, dest)` + `sandbox.fs.rm(src)` or `process.exec({ command: 'mv ...' })` |
| Copy file | N/A | `sandbox.fs.cp(src, dest)` |
| Replace in files | `sandbox.fs.replaceInFiles(files, pattern, newValue)` | No equivalent — use `process.exec({ command: "sed -i 's/old/new/g' file" })` |
| File details | `sandbox.fs.getFileDetails(path)` → size, mode, permissions, owner, group, modifiedTime | No equivalent — use `process.exec({ command: 'stat file' })` |
| Set permissions | `sandbox.fs.setFilePermissions(path, { mode, owner, group })` | No equivalent — use `process.exec({ command: 'chmod/chown ...' })` |
| Batch upload | `sandbox.fs.uploadFiles([{ path, content }])` | `sandbox.fs.writeTree(files, basePath)` |
| Watch files | N/A | `sandbox.fs.watch(path, callback, { withContent?, ignore? })` — returns handle with `close()` |

**TypeScript:**
```typescript
// BEFORE (Daytona)
await sandbox.fs.uploadFile(Buffer.from('hello'), '/app/file.txt')
const blob = await sandbox.fs.downloadFile('/app/file.txt')
const content = blob.toString()
const files = await sandbox.fs.listFiles('/app')

// AFTER (Blaxel)
await sandbox.fs.write('/app/file.txt', 'hello')
const content = await sandbox.fs.read('/app/file.txt')
const { subdirectories, files } = await sandbox.fs.ls('/app')

// Blaxel also supports writing multiple files at once:
await sandbox.fs.writeTree([
  { path: 'src/index.ts', content: 'console.log("hello")' },
  { path: 'package.json', content: '{"name":"app"}' },
], '/app')

// Delete files:
await sandbox.fs.rm('/app/old-file.txt')
await sandbox.fs.rm('/app/old-dir', { recursive: true })

// Copy files:
await sandbox.fs.cp('/app/src/template.ts', '/app/src/copy.ts')

// Watch for file changes:
const handle = await sandbox.fs.watch('/app/src', (event) => {
  console.log('Changed:', event.path, event.type)
}, { withContent: true, ignore: ['node_modules'] })
// Later: handle.close()
```

**Python:**
```python
# BEFORE (Daytona)
await sandbox.fs.upload_file(content.encode(), "/app/file.txt")
blob = await sandbox.fs.download_file("/app/file.txt")
content = blob.decode()
files = await sandbox.fs.list_files("/app")

# AFTER (Blaxel)
await sandbox.fs.write("/app/file.txt", "hello")
content = await sandbox.fs.read("/app/file.txt")
listing = await sandbox.fs.ls("/app")

# Write multiple files:
await sandbox.fs.write_tree([
    {"path": "src/index.ts", "content": 'console.log("hello")'},
    {"path": "package.json", "content": '{"name":"app"}'},
], "/app")

# Delete files:
await sandbox.fs.rm("/app/old-file.txt")
await sandbox.fs.rm("/app/old-dir", {"recursive": True})

# Copy files:
await sandbox.fs.cp("/app/src/template.ts", "/app/src/copy.ts")

# Watch for file changes:
handle = await sandbox.fs.watch("/app/src", lambda event: print(f"Changed: {event}"),
    {"with_content": True, "ignore": ["node_modules"]})
# Later: handle.close()
```

### Preview URLs

Daytona provides `getPreviewLink(port)` for standard access, plus signed URLs with expiration. Blaxel has dedicated preview URL management with public/private access and token-based auth.

**TypeScript:**
```typescript
// BEFORE (Daytona)
const link = sandbox.getPreviewLink(3000)
// Signed URL with expiration:
const signed = await sandbox.getSignedPreviewUrl(3000, 3600) // 1 hour
await sandbox.expireSignedPreviewUrl(3000, signed.token)

// AFTER (Blaxel) - dedicated preview URL with public/private access control
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'app-preview' },
  spec: { port: 3000, public: true },
})
const url = preview.spec?.url  // https://xxxx.preview.bl.run

// Private preview with token-based access:
const privatePreview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'private-preview' },
  spec: { port: 3000, public: false },
})
const token = await privatePreview.tokens.create(
  new Date(Date.now() + 3600 * 1000) // expires in 1 hour
)
// Access: https://xxxx.preview.bl.run?token=<token>
// Revoke:
await privatePreview.tokens.delete(token.id)
```

**Python:**
```python
# BEFORE (Daytona)
link = sandbox.get_preview_link(3000)
signed = await sandbox.get_signed_preview_url(3000, 3600)
await sandbox.expire_signed_preview_url(3000, signed.token)

# AFTER (Blaxel)
preview = await sandbox.previews.create_if_not_exists({
    "metadata": {"name": "app-preview"},
    "spec": {"port": 3000, "public": True},
})
url = preview.spec.url  # https://xxxx.preview.bl.run

# Private preview with token:
private_preview = await sandbox.previews.create_if_not_exists({
    "metadata": {"name": "private-preview"},
    "spec": {"port": 3000, "public": False},
})
token = await private_preview.tokens.create(expires_at)
# Access: url + ?token=<token>
# Revoke:
await private_preview.tokens.delete(token.id)
```

### Sandbox lifecycle

| Operation | Daytona | Blaxel |
|-----------|---------|--------|
| Delete | `sandbox.delete()` / `daytona.delete(sandbox)` | `sandbox.delete()` |
| Stop | `sandbox.stop()` | Automatic (scales to zero after ~5s) |
| Start / Resume | `sandbox.start()` | Automatic (resumes in <25ms on next API call) |
| Archive | `sandbox.archive()` | Not needed (state preserved) |
| Reconnect | `daytona.get(sandboxId)` / `daytona.findOne({ labels })` | `SandboxInstance.get('my-sandbox')` |
| Resize | `sandbox.resize({ cpu, memory, disk })` + `waitForResizeComplete()` | N/A — create new sandbox with different config |
| Recover | `sandbox.recover()` | N/A — sandboxes auto-resume from standby |
| List sandboxes | `daytona.list(labels?, page?, limit?)` → paginated | `SandboxInstance.list()` — returns all (client-side filtering via labels) |
| Exit code | `result.exitCode` on execute response | `result.exitCode` on process response |
| Wait for start | `sandbox.waitUntilStarted(timeout)` | Not needed — auto-resumes in <25ms |
| Wait for stop | `sandbox.waitUntilStopped(timeout)` | Not needed |
| Wait for process | Poll session command logs | `sandbox.process.wait('name', { maxWait, interval })` |
| Stop process | Kill via session | `sandbox.process.stop('name')` |
| List processes | `sandbox.process.listSessions()` | `sandbox.process.list()` |
| Get process | `sandbox.process.getSession(id)` | `sandbox.process.get('name')` |
| Update TTL | `sandbox.setAutostopInterval(mins)` / `setAutoArchiveInterval()` / `setAutoDeleteInterval()` | `SandboxInstance.updateTtl('name', '48h')` or `SandboxInstance.updateLifecycle('name', { expirationPolicies: [...] })` |
| Refresh activity | `sandbox.refreshActivity()` | Not needed (auto-detected on API calls) |
| Labels (read) | `sandbox.labels` | `sandbox.metadata.labels` |
| Labels (write) | `sandbox.setLabels({ key: 'val' })` | `SandboxInstance.updateMetadata('name', { labels: { key: 'val' } })` |
| Sandbox info | `sandbox.id`, `sandbox.state`, `sandbox.labels` | `SandboxInstance.get('name')` → `sandbox.metadata`, `sandbox.status`, `sandbox.spec` |

**TypeScript:**
```typescript
// BEFORE (Daytona) - manual lifecycle management
await sandbox.stop()
// ... later ...
await sandbox.start()

// AFTER (Blaxel) - automatic, just reconnect by name
const sandbox = await SandboxInstance.get('my-sandbox')
// Sandbox resumes automatically if it was idle
```

**Python:**
```python
# BEFORE (Daytona) - manual lifecycle management
await sandbox.stop()
# ... later ...
await sandbox.start()

# AFTER (Blaxel) - automatic, just reconnect by name
sandbox = await SandboxInstance.get("my-sandbox")
# Sandbox resumes automatically if it was idle
```

### Code Interpreter

Daytona has `sandbox.codeInterpreter` for stateful Python execution. Blaxel provides a dedicated `CodeInterpreter` class that extends `SandboxInstance` with Jupyter kernel support for multiple languages.

**TypeScript:**
```typescript
// BEFORE (Daytona)
import { Daytona } from '@daytonaio/sdk'
const daytona = new Daytona()
const sandbox = await daytona.create()
const ctx = await sandbox.codeInterpreter.createContext()
const result = await sandbox.codeInterpreter.runCode('x = 42', { context: ctx })
const result2 = await sandbox.codeInterpreter.runCode('print(x)', { context: ctx })
await sandbox.codeInterpreter.deleteContext(ctx)

// AFTER (Blaxel)
import { CodeInterpreter } from '@blaxel/core'
const interpreter = await CodeInterpreter.createIfNotExists({
  name: 'my-interpreter',
  region: 'us-pdx-1',
  memory: 2048,
})
const ctx = await interpreter.createCodeContext({ language: 'python', name: 'ctx-1' })
const result = await interpreter.runCode({ code: 'x = 42', context: ctx })
const result2 = await interpreter.runCode({ code: 'print(x)', context: ctx })
```

**Python:**
```python
# BEFORE (Daytona)
from daytona_sdk import Daytona
daytona = Daytona()
sandbox = await daytona.create()
ctx = await sandbox.code_interpreter.create_context()
result = await sandbox.code_interpreter.run_code("x = 42", context=ctx)
result2 = await sandbox.code_interpreter.run_code("print(x)", context=ctx)
await sandbox.code_interpreter.delete_context(ctx)

# AFTER (Blaxel)
from blaxel.core import CodeInterpreter
interpreter = await CodeInterpreter.create_if_not_exists({
    "name": "my-interpreter",
    "region": "us-pdx-1",
    "memory": 2048,
})
ctx = await interpreter.create_code_context({"language": "python", "name": "ctx-1"})
result = await interpreter.run_code({"code": "x = 42", "context": ctx})
result2 = await interpreter.run_code({"code": "print(x)", "context": ctx})
```

> **Note:** Daytona code interpreter is Python-only. Blaxel `CodeInterpreter` uses a Jupyter kernel and supports multiple languages (Python, JavaScript, TypeScript, etc.). The default image is `blaxel/jupyter-server`.

### Git integration

Daytona provides a full `sandbox.git.*` API. Blaxel has no dedicated git API — use `process.exec()` with git commands instead.

**TypeScript:**
```typescript
// BEFORE (Daytona)
await sandbox.git.clone('https://github.com/user/repo.git', '/app')
const status = await sandbox.git.status('/app')
const branches = await sandbox.git.branches('/app')
await sandbox.git.add('/app', ['src/index.ts'])
await sandbox.git.commit('/app', 'feat: add feature')
await sandbox.git.push('/app')

// AFTER (Blaxel) - use process.exec with git commands
await sandbox.process.exec({
  command: 'git clone https://github.com/user/repo.git /app',
  waitForCompletion: true,
})
const status = await sandbox.process.exec({
  command: 'git status --porcelain',
  workingDir: '/app',
  waitForCompletion: true,
})
await sandbox.process.exec({
  command: 'git add src/index.ts && git commit -m "feat: add feature" && git push',
  workingDir: '/app',
  waitForCompletion: true,
})
```

**Python:**
```python
# BEFORE (Daytona)
await sandbox.git.clone("https://github.com/user/repo.git", "/app")
status = await sandbox.git.status("/app")
await sandbox.git.add("/app", ["src/index.ts"])
await sandbox.git.commit("/app", "feat: add feature")
await sandbox.git.push("/app")

# AFTER (Blaxel) - use process.exec with git commands
await sandbox.process.exec({
    "command": "git clone https://github.com/user/repo.git /app",
    "wait_for_completion": True,
})
status = await sandbox.process.exec({
    "command": "git status --porcelain",
    "working_dir": "/app",
    "wait_for_completion": True,
})
await sandbox.process.exec({
    "command": 'git add src/index.ts && git commit -m "feat: add feature" && git push',
    "working_dir": "/app",
    "wait_for_completion": True,
})
```

> **Note:** Git must be installed in the sandbox image. Use `process.exec()` for any git operation: `clone`, `status`, `branch`, `add`, `commit`, `push`, `pull`, etc.

### MCP integration

Daytona exposes MCP server integration for tools like Claude Desktop and Cursor. Blaxel sandboxes have a built-in MCP server accessible via SDK helpers.

**TypeScript:**
```typescript
// BEFORE (Daytona) - MCP server via dashboard configuration
// Configure MCP in Claude Desktop / Cursor pointing to Daytona

// AFTER (Blaxel) - built-in MCP server on every sandbox
// Every sandbox exposes MCP at: https://<SANDBOX_URL>/mcp

// For framework integrations (Vercel AI SDK, LangChain, etc.):
import { blTools } from '@blaxel/core'
const tools = await blTools(['sandbox/my-sandbox'])
// Pass tools to your AI framework
```

**Python:**
```python
# BEFORE (Daytona) - MCP via dashboard
# Configure MCP in Claude Desktop / Cursor pointing to Daytona

# AFTER (Blaxel) - built-in MCP server
# Every sandbox exposes MCP at: https://<SANDBOX_URL>/mcp

# For framework integrations:
from blaxel.core import bl_tools
tools = await bl_tools(["sandbox/my-sandbox"])
# Pass tools to your AI framework
```

### Volumes

Daytona has `daytona.volume.*` for FUSE-based S3-compatible volumes. Blaxel provides `VolumeInstance` for persistent block storage.

**TypeScript:**
```typescript
// BEFORE (Daytona)
import { Daytona } from '@daytonaio/sdk'
const daytona = new Daytona()
const volume = await daytona.volume.create({
  name: 'my-data',
  size: 10, // GiB
})
const sandbox = await daytona.create({ volumes: [{ volumeId: volume.id, mountPath: '/data' }] })
const volumes = await daytona.volume.list()
await daytona.volume.delete(volume.id)

// AFTER (Blaxel)
import { SandboxInstance, VolumeInstance } from '@blaxel/core'
const volume = await VolumeInstance.createIfNotExists({
  name: 'my-data',
})
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/base-image:latest',
  region: 'us-pdx-1',
  memory: 2048,
  volumes: [{ name: 'my-data', mountPath: '/data' }],
})
const volumes = await VolumeInstance.list()
await volume.delete()
```

**Python:**
```python
# BEFORE (Daytona)
from daytona_sdk import Daytona
daytona = Daytona()
volume = await daytona.volume.create(name="my-data", size=10)
sandbox = await daytona.create(volumes=[{"volume_id": volume.id, "mount_path": "/data"}])
volumes = await daytona.volume.list()
await daytona.volume.delete(volume.id)

# AFTER (Blaxel)
from blaxel.core import SandboxInstance, VolumeInstance
volume = await VolumeInstance.create_if_not_exists({"name": "my-data"})
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "blaxel/base-image:latest",
    "region": "us-pdx-1",
    "memory": 2048,
    "volumes": [{"name": "my-data", "mount_path": "/data"}],
})
volumes = await VolumeInstance.list()
await volume.delete()
```

> **Note:** Daytona volumes are FUSE-based S3-compatible with concurrent multi-sandbox mounting and subpath support. Blaxel volumes are persistent block storage. Daytona allows configuring volume size; Blaxel volumes do not have a size parameter.

### Snapshots

Daytona has explicit snapshot management (`daytona.snapshot.create/get/list/delete/activate`). Blaxel auto-preserves state through scale-to-zero — no explicit snapshot API needed.

```typescript
// BEFORE (Daytona)
const snapshot = await daytona.snapshot.create({ sandboxId: sandbox.id, name: 'checkpoint-1' })
const restored = await daytona.create({ snapshot: 'checkpoint-1' })
const snapshots = await daytona.snapshot.list()
await daytona.snapshot.delete(snapshot.id)

// AFTER (Blaxel)
// State (memory + filesystem) is automatically preserved through auto-pause/resume.
// No explicit snapshot API needed.
// For sharing pre-built state across sandboxes, use volume templates:
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'my-pre-built-template', // deployed via `bl deploy`
  volumes: [{ name: 'shared-state', mountPath: '/data' }],
})
```

> **Note:** Daytona snapshots auto-deactivate after 2 weeks of inactivity. Blaxel state persists indefinitely until the sandbox is deleted or its TTL expires.

## Key differences

- **No client instantiation**: Blaxel SDK uses static methods on `SandboxInstance`; no need to create a `Daytona()` client
- **Memory units**: Daytona uses GB, Blaxel uses MB (e.g., `2` GB in Daytona = `2048` MB in Blaxel)
- **Ports declared at creation**: Blaxel requires ports at sandbox creation time; they cannot be added later. Ports 80, 443, 8080 are reserved
- **Region format**: Daytona uses `'us'`/`'eu'`/`'asia'`; Blaxel uses specific region IDs like `'us-pdx-1'`
- **Auto scale-to-zero**: Both support auto scale-to-zero. Blaxel sandboxes auto-pause after ~5s of inactivity and resume in <25ms. No manual stop/start needed. Use `lifecycle: { expirationPolicies: [{ type: 'ttl-idle', value: '7d', action: 'delete' }] }` for idle-based deletion
- **Preview URLs**: Blaxel has native preview URL support with public/private access control, token-based auth, and token revocation. Daytona's `getPreviewLink()` / signed URLs map to Blaxel's `previews.createIfNotExists()` + `tokens.create()`
- **Named sandboxes**: Blaxel uses human-readable names (not opaque IDs). Supports `createIfNotExists` / `create_if_not_exists` for idempotent creation
- **Environment variables**: Daytona uses a flat object (`envVars: { KEY: 'val' }` / `env_vars={"KEY": "val"}`). Blaxel uses an array of objects at creation (`envs: [{ name: 'KEY', value: 'val' }]`) and a flat object per-command (`env: { KEY: 'val' }`)
- **Dev server binding**: Dev servers must bind to `0.0.0.0` (not `localhost`) for preview URLs to work in Blaxel
- **~50% memory reserved for tmpfs**: Blaxel uses half of sandbox memory for the in-memory filesystem. Use volumes for extra storage
- **Async Python**: Blaxel Python SDK is async-first (all calls use `await`); Daytona Python SDK also supports async
- **No GPU support**: Blaxel sandboxes are CPU-only. Daytona supports `resources: { gpu: 1 }`
- **No configurable disk**: Blaxel uses tmpfs (~50% of memory). Use volumes for extra storage. Daytona allows `resources: { disk: 10 }` (GiB) with hot resize
- **No git API**: Blaxel has no dedicated git methods. Use `process.exec({ command: 'git ...' })` instead of Daytona's `sandbox.git.*`
- **No LSP support**: Blaxel has no Language Server Protocol API. Daytona offers `sandbox.createLspServer()` with completions and symbol search. Blaxel has `sandbox.codegen.reranking()` for code search
- **No desktop automation**: Blaxel has no computer use API. Daytona offers `sandbox.computerUse.*` for mouse, keyboard, screenshot, and screen recording
- **No PTY / SSH**: Blaxel has no interactive terminal or SSH access. Daytona supports PTY sessions and SSH access with token-based auth
- **No webhooks**: Blaxel has no webhook/events API. Daytona supports lifecycle event webhooks configured via dashboard
- **No sandbox resize**: Blaxel does not support hot-resizing CPU/memory/disk. Create a new sandbox with different config instead
- **Image builder**: Daytona has a declarative `Image` builder with chainable methods. Blaxel uses standard Dockerfiles deployed via `bl deploy`
- **MCP integration**: Every Blaxel sandbox has a built-in MCP server at `https://<SANDBOX_URL>/mcp`. Use `blTools(['sandbox/my-sandbox'])` for framework integrations. Daytona requires separate MCP server configuration
- **Code interpreter**: Both support stateful code execution. Blaxel's `CodeInterpreter` class uses Jupyter and supports multiple languages. Daytona's `codeInterpreter` is Python-only
- **Log streaming**: Blaxel provides `onLog`/`onStdout`/`onStderr` callbacks on `process.exec()`, plus `process.streamLogs()` and `process.logs()` with type filtering. Daytona uses session-based command logs
- **Volumes**: Both support persistent volumes. Daytona volumes are FUSE-based S3-compatible with concurrent multi-sandbox mounting. Blaxel volumes are persistent block storage with simpler CRUD via `VolumeInstance`

## Complete migration example

### TypeScript

**BEFORE (Daytona):**
```typescript
import { Daytona } from '@daytonaio/sdk'

const daytona = new Daytona({ apiKey: process.env.DAYTONA_API_KEY })
const sandbox = await daytona.create({
  image: 'debian:slim',
  resources: { memory: 2, cpu: 1 },
  envVars: { NODE_ENV: 'production' },
  labels: { project: 'demo' },
  target: 'us',
})

await sandbox.fs.uploadFile(Buffer.from('console.log("hello")'), '/app/index.js')
const result = await sandbox.process.executeCommand('node /app/index.js')
console.log(result)

await sandbox.delete()
```

**AFTER (Blaxel):**
```typescript
import { SandboxInstance } from '@blaxel/core'

const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/node:latest',
  region: 'us-pdx-1',
  memory: 2048,
  envs: [{ name: 'NODE_ENV', value: 'production' }],
  labels: { project: 'demo' },
})

await sandbox.fs.write('/app/index.js', 'console.log("hello")')
const result = await sandbox.process.exec({
  command: 'node /app/index.js',
  workingDir: '/app',
  waitForCompletion: true,
})

await sandbox.delete()
```

### Python

**BEFORE (Daytona):**
```python
import asyncio
from daytona_sdk import Daytona, CreateSandboxParams, Resources

async def main():
    daytona = Daytona(api_key=os.environ["DAYTONA_API_KEY"])
    sandbox = await daytona.create(CreateSandboxParams(
        image="debian:slim",
        resources=Resources(cpu=1, memory=2),
        env_vars={"NODE_ENV": "production"},
        labels={"project": "demo"},
        target="us",
    ))

    await sandbox.fs.upload_file(b'print("hello")', "/app/main.py")
    result = await sandbox.process.execute_command("python3 /app/main.py")
    print(result)

    await sandbox.delete()

asyncio.run(main())
```

**AFTER (Blaxel):**
```python
import asyncio
from blaxel.core import SandboxInstance

async def main():
    sandbox = await SandboxInstance.create_if_not_exists({
        "name": "my-sandbox",
        "image": "blaxel/py-app:latest",
        "region": "us-pdx-1",
        "memory": 2048,
        "envs": [{"name": "NODE_ENV", "value": "production"}],
        "labels": {"project": "demo"},
    })

    await sandbox.fs.write("/app/main.py", 'print("hello")')
    result = await sandbox.process.exec({
        "command": "python3 /app/main.py",
        "working_dir": "/app",
        "wait_for_completion": True,
    })

    await sandbox.delete()

asyncio.run(main())
```

## Resources

- Blaxel docs: https://docs.blaxel.ai
- Blaxel sandbox images: https://github.com/blaxel-ai/sandbox/tree/main/hub
- Daytona docs: https://www.daytona.io/docs/en/
- SDK reference (TypeScript): `@blaxel/core` — see ./references/sdk-typescript.md
- SDK reference (Python): `blaxel` — see ./references/sdk-python.md
