---
name: migrate-from-modal
description: Use when migrating sandbox code from Modal (modal SDK) to Blaxel (@blaxel/core or blaxel). Covers API mapping for sandbox creation, command execution, filesystem operations, image building, snapshot/resume, tunnels, and authentication in both TypeScript and Python. Reach for this skill when you encounter Modal SDK imports or need to replace Modal sandbox calls with Blaxel equivalents.
---

# Migrate from Modal to Blaxel

This guide covers migrating cloud sandbox code from **Modal** (`modal`) to **Blaxel** (`@blaxel/core` / `blaxel`).

## Package replacement

| Language | Modal | Blaxel |
|----------|-------|--------|
| TypeScript | `modal` | `@blaxel/core` |
| Python | `modal` | `blaxel` |

```bash
# TypeScript
npm uninstall modal
npm install @blaxel/core

# Python
pip uninstall modal
pip install blaxel
```

## Authentication

| Modal | Blaxel |
|-------|--------|
| `MODAL_TOKEN_ID` + `MODAL_TOKEN_SECRET` env vars | `BL_WORKSPACE` + `BL_API_KEY` env vars |
| Or `modal setup` CLI command | Or `bl login YOUR-WORKSPACE` CLI command |
| Requires two secrets (token pair) | CLI login, .env, env vars, or config file (auto-detected) |

Blaxel authenticates automatically when logged in via CLI (`bl login YOUR-WORKSPACE`). No need to manage token pairs.

## API mapping

### Imports

**TypeScript:**
```typescript
// BEFORE (Modal)
import { ModalClient, Sandbox } from 'modal'

// AFTER (Blaxel)
import { SandboxInstance } from '@blaxel/core'
```

**Python:**
```python
# BEFORE (Modal)
import modal

# AFTER (Blaxel)
from blaxel.core import SandboxInstance
```

### Sandbox creation

Modal requires instantiating a client, creating an app, building an image, then creating a sandbox. Blaxel uses a single static method.

**TypeScript:**
```typescript
// BEFORE (Modal)
const client = new ModalClient()
const app = await client.apps.fromName('my-app', { createIfMissing: true })
const image = client.images.fromRegistry('python:3.11-slim')
const sandbox = await client.sandboxes.create(app, image, {
  regions: ['us-west-2'],
  memoryMiB: 2048,
  cpu: 1,
  timeoutMs: 1000 * 60 * 15,
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
})
```

**Python:**
```python
# BEFORE (Modal)
app = modal.App("my-app")
image = modal.Image.debian_slim().pip_install("numpy")
sandbox = app.spawn_sandbox(
    image=image,
    timeout=900,     # seconds (max 24h)
    cpu=1,
    memory=2048,     # MiB
)

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
})
```

### Parameter mapping

| Parameter | Modal | Blaxel |
|-----------|-------|--------|
| Image | `client.images.fromRegistry(...)` (programmatic) | `image: 'blaxel/base-image:latest'` (pre-built or custom Dockerfile) |
| Memory | `memoryMiB: 2048` | `memory: 2048` (MB) |
| CPU | `cpu: 1` | Not needed (auto-allocated: CPU cores = memory / 2048) |
| Region | `regions: ['us-west-2']` | `region: 'us-pdx-1'` |
| Timeout | `timeoutMs: 900000` (max 24h) | `ttl: '24h'` |
| Idle timeout | `idle_timeout: 300` (seconds, terminates) | Auto scale-to-zero (~5s, suspends with <25ms resume). For idle-based *deletion*, use `lifecycle: { expirationPolicies: [{ type: 'ttl-idle', value: '7d', action: 'delete' }] }` |
| Name | `name: 'my-sandbox'` (within app) | `name: 'my-sandbox'` (global) |
| Tags | `tags: { k: 'v' }` | `labels: { k: 'v' }` |
| Ports | `encrypted_ports: [3000]` / `unencrypted_ports: [3000]` | `ports: [{ target: 3000, protocol: 'HTTP' }]` |
| Environment vars | Inline secrets at creation | `envs: [{ name: 'KEY', value: 'val' }]` |
| Secrets | Modal secrets (vault-based) | `envs: [{ name: 'KEY', value: 'val', secret: true }]` |
| Network control | `block_network: true`, `cidr_allowlist: [...]` | N/A (sandboxes have full network access) |
| GPU | `gpu: 'A10G'` (T4, L4, A10G, A100, H100, etc.) | N/A (Blaxel sandboxes do not support GPU) |
| Entrypoint command | `command: ['python3', 'server.py']` at creation | Not supported at creation — use `process.exec()` immediately after |
| Proxy / network routing | `proxy: modal.proxies.fromName(...)` | `network: { vpcName: 'my-vpc', egressGatewayName: 'my-gw' }` (VPC + egress gateway) |
| Cloud bucket mounts | `cloudBucketMounts: { '/mnt': ... }` (S3/GCS) | N/A (use `process.exec()` with AWS CLI/gsutil to sync data) |
| HTTP/2 ports | `h2Ports: [8080]` | N/A (use `ports: [{ target: 8080, protocol: 'HTTP' }]` — HTTPS handled via preview URLs) |
| App | Required `App` object | Not needed |

### Entrypoint command at creation

Modal allows running a command directly at sandbox creation. Blaxel requires creating the sandbox first, then executing:

**TypeScript:**
```typescript
// BEFORE (Modal) - command at creation
const sandbox = await client.sandboxes.create(app, image, {
  command: ['python3', '-m', 'http.server', '8080'],
})

// AFTER (Blaxel) - create then exec
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/base-image:latest',
  ports: [{ target: 8080, protocol: 'HTTP' }],
})
await sandbox.process.exec({
  command: 'python3 -m http.server 8080',
  waitForPorts: [8080],
})
```

**Python:**
```python
# BEFORE (Modal)
sandbox = app.spawn_sandbox(image=image, command=["python3", "-m", "http.server", "8080"])

# AFTER (Blaxel)
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "blaxel/base-image:latest",
    "ports": [{"target": 8080, "protocol": "HTTP"}],
})
await sandbox.process.exec({
    "command": "python3 -m http.server 8080",
    "wait_for_ports": [8080],
})
```

### Custom images / templates

Modal builds images programmatically with chained SDK methods. Blaxel uses standard Dockerfiles deployed via `bl deploy`.

**TypeScript:**
```typescript
// BEFORE (Modal) - programmatic image building
const image = client.images.fromRegistry('ubuntu:22.04')
  .dockerfileCommands([
    'RUN apt-get update && apt-get install -y curl git',
    'RUN curl -fsSL https://bun.sh/install | bash',
    'RUN mkdir -p /workspace',
  ])
const sandbox = await client.sandboxes.create(app, image, { regions: ['us-west-2'] })

// AFTER (Blaxel) - Dockerfile-based templates deployed with `bl deploy`
// 1. Create template: bl new sandbox my-template
// 2. Edit the Dockerfile
// 3. Deploy: bl deploy
// 4. Use the deployed image:
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'my-deployed-template-image',
  region: 'us-pdx-1',
  memory: 2048,
})
```

**Python:**
```python
# BEFORE (Modal) - programmatic image building
image = (
    modal.Image.debian_slim()
    .apt_install("curl", "git")
    .run_commands("curl -fsSL https://bun.sh/install | bash")
    .pip_install("numpy", "pandas")
)
sandbox = app.spawn_sandbox(image=image)

# AFTER (Blaxel) - deploy a Dockerfile via `bl deploy`, then reference it:
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "my-deployed-template-image",
    "region": "us-pdx-1",
    "memory": 2048,
})
```

**Blaxel Dockerfile equivalent:**
```dockerfile
FROM ubuntu:22.04
WORKDIR /workspace
COPY --from=ghcr.io/blaxel-ai/sandbox:latest /sandbox-api /usr/local/bin/sandbox-api
RUN apt-get update && apt-get install -y curl git
RUN curl -fsSL https://bun.sh/install | bash
RUN pip install numpy pandas
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

#### Image building methods mapping

All Modal image building methods map to standard Dockerfile instructions in a Blaxel template:

| Modal Image Method | Blaxel Dockerfile Equivalent |
|----|-----|
| `.debian_slim()` | `FROM python:3.11-slim` |
| `.from_registry("img")` | `FROM img` |
| `.from_dockerfile("./Dockerfile")` | Use the Dockerfile directly as the Blaxel template |
| `.pip_install("numpy")` | `RUN pip install numpy` |
| `.pip_install_from_requirements("r.txt")` | `COPY requirements.txt . && RUN pip install -r requirements.txt` |
| `.pip_install_from_pyproject("p.toml")` | `COPY pyproject.toml . && RUN pip install .` |
| `.poetry_install_from_file(...)` | `COPY pyproject.toml poetry.lock . && RUN poetry install` |
| `.uv_pip_install("numpy")` | `RUN uv pip install numpy` |
| `.uv_sync()` | `COPY pyproject.toml uv.lock . && RUN uv sync` |
| `.apt_install("curl")` | `RUN apt-get update && apt-get install -y curl` |
| `.micromamba_install("numpy")` | `RUN micromamba install numpy` |
| `.add_local_file("f", "/app/f")` | `COPY f /app/f` |
| `.add_local_dir("./src", "/app/src")` | `COPY ./src /app/src` |
| `.run_commands("echo hi")` | `RUN echo hi` |
| `.run_function(fn)` | N/A (use `RUN` with a script instead) |
| `.env({"KEY": "val"})` | `ENV KEY=val` |
| `.workdir("/app")` | `WORKDIR /app` |
| `.entrypoint(["python"])` | `ENTRYPOINT ["python"]` |
| `.shell("/bin/bash")` | `SHELL ["/bin/bash", "-c"]` |
| `.cmd(["serve"])` | `CMD ["serve"]` |

**Image pre-warming:** Modal's `image.build(app)` eagerly caches images before sandbox creation. The Blaxel equivalent is `bl deploy`, which builds and pushes the template image to Blaxel's private registry. Subsequent sandbox creation with that image is instant.

### Command execution

Modal uses `sandbox.exec(['bash', '-c', command])` with stdout/stderr streams. Blaxel uses a single `process.exec()` call.

**TypeScript:**
```typescript
// BEFORE (Modal)
const result = await sandbox.exec(['bash', '-c', 'echo hello'])
const stdout = await result.stdout.readText()
const stderr = await result.stderr.readText()
const exitCode = await result.wait()

// With env vars and working directory (manual shell construction):
const envStr = Object.entries(envVars).map(([k, v]) => `export ${k}="${v}"`).join(' && ')
const fullCommand = `${envStr} && cd /app && npm install`
const result = await sandbox.exec(['bash', '-c', fullCommand])

// AFTER (Blaxel)
const result = await sandbox.process.exec({
  command: 'echo hello',
  waitForCompletion: true,
})

// With env vars and working directory (native support):
const result = await sandbox.process.exec({
  command: 'npm install',
  workingDir: '/app',
  env: { NODE_ENV: 'production' },
  waitForCompletion: true,
})
```

**Python:**
```python
# BEFORE (Modal)
process = sandbox.exec("bash", "-c", "echo hello")
stdout = process.stdout.read()
stderr = process.stderr.read()
process.wait()

# With env vars (manual shell construction):
process = sandbox.exec("bash", "-c", "export NODE_ENV=production && cd /app && npm install")

# AFTER (Blaxel)
result = await sandbox.process.exec({
    "command": "echo hello",
    "wait_for_completion": True,
})

# With env vars and working directory (native support):
result = await sandbox.process.exec({
    "command": "npm install",
    "working_dir": "/app",
    "env": {"NODE_ENV": "production"},
    "wait_for_completion": True,
})
```

### Long-running processes (dev servers)

**TypeScript:**
```typescript
// BEFORE (Modal) - must redirect to temp file and poll
const bgCommand = `export PATH=... && cd /app && npm run dev > /tmp/output.log 2>&1 & echo $! > /tmp/pid.txt`
await sandbox.exec(['bash', '-c', bgCommand])
// ... poll /tmp/output.log for readiness ...
// ... kill process via: sandbox.exec(['bash', '-c', 'kill $(cat /tmp/pid.txt)'])

// AFTER (Blaxel) - native background mode with port waiting
const devServer = await sandbox.process.exec({
  name: 'dev-server',
  command: 'npm run dev -- --host 0.0.0.0',
  workingDir: '/app',
  waitForPorts: [3000],  // returns once port 3000 is open
})
// Later: await sandbox.process.kill('dev-server')
```

**Python:**
```python
# BEFORE (Modal) - must redirect to temp file and poll
bg_command = "export PATH=... && cd /app && npm run dev > /tmp/output.log 2>&1 & echo $! > /tmp/pid.txt"
sandbox.exec("bash", "-c", bg_command)
# ... poll /tmp/output.log for readiness ...

# AFTER (Blaxel) - native background mode with port waiting
dev_server = await sandbox.process.exec({
    "name": "dev-server",
    "command": "npm run dev -- --host 0.0.0.0",
    "working_dir": "/app",
    "wait_for_ports": [3000],
})
# Later: await sandbox.process.kill("dev-server")
```

### Log streaming / Process output

Modal uses pipe-based stdout/stderr streams on the sandbox entrypoint or on `exec()` results. Blaxel captures output via callbacks, log retrieval, or stream subscriptions.

**TypeScript:**
```typescript
// BEFORE (Modal) - pipe-based streams
const result = await sandbox.exec(['bash', '-c', 'echo hello && echo err >&2'])
const stdout = await result.stdout.readText()
const stderr = await result.stderr.readText()
const exitCode = await result.wait()

// Entrypoint streams:
await sandbox.stdin.writeText('input\n')
const output = await sandbox.stdout.readText()

// AFTER (Blaxel) - callbacks on exec
const result = await sandbox.process.exec({
  command: 'echo hello && echo err >&2',
  onLog: (log) => console.log('[LOG]', log),
  onStdout: (out) => process.stdout.write(out),
  onStderr: (err) => process.stderr.write(err),
  waitForCompletion: true,
})
// result.stdout, result.stderr, result.exitCode available after completion

// Stream logs from a running process:
const handle = sandbox.process.streamLogs('my-process', {
  onLog: (log) => console.log(log),
  onStdout: (out) => process.stdout.write(out),
  onStderr: (err) => process.stderr.write(err),
  onError: (err) => console.error(err),
})
// Wait for the process to finish before closing the stream:
await handle.wait()

// Retrieve logs after the fact:
const logs = await sandbox.process.logs('my-process')          // all
const stdout = await sandbox.process.logs('my-process', 'stdout')
const stderr = await sandbox.process.logs('my-process', 'stderr')
```

**Python:**
```python
# BEFORE (Modal) - pipe-based streams
process = sandbox.exec("bash", "-c", "echo hello && echo err >&2")
stdout = process.stdout.read()
stderr = process.stderr.read()
process.wait()

# AFTER (Blaxel) - callbacks on exec
result = await sandbox.process.exec({
    "command": "echo hello && echo err >&2",
    "on_log": lambda log: print("[LOG]", log),
    "on_stdout": lambda out: print(out, end=""),
    "on_stderr": lambda err: print(err, end="", file=sys.stderr),
    "wait_for_completion": True,
})
# result.stdout, result.stderr, result.exit_code available

# Stream logs from a running process:
handle = await sandbox.process.stream_logs("my-process", {
    "on_log": lambda log: print(log),
})
# Wait for the process to finish before closing the stream:
await handle.wait()

# Retrieve logs after the fact:
logs = await sandbox.process.logs("my-process")           # all
stdout = await sandbox.process.logs("my-process", "stdout")
stderr = await sandbox.process.logs("my-process", "stderr")
```

> **Note:** Blaxel does not support `stdin` writes or pseudo-terminal (`pty`) mode. There is no equivalent to Modal's `pty: true` parameter.

### Secrets

Modal has vault-based secrets (`Secret.from_name()`, `Secret.from_dict()`, `Secret.from_dotenv()`). Blaxel uses environment variables with an optional `secret: true` flag.

**TypeScript:**
```typescript
// BEFORE (Modal) - vault-based secrets
const secret = await modal.Secret.fromName('my-secret')
const ephemeralSecret = modal.Secret.fromDict({ API_KEY: 'sk-...' })
const dotenvSecret = modal.Secret.fromDotenv()
const sandbox = await client.sandboxes.create(app, image, {
  secrets: [secret, ephemeralSecret],
})
// Per-exec secrets:
const result = await sandbox.exec(['bash', '-c', 'echo $API_KEY'], {
  secrets: [ephemeralSecret],
})

// AFTER (Blaxel) - environment variables with secret flag
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/base-image:latest',
  envs: [
    { name: 'API_KEY', value: 'sk-...', secret: true },  // marked as secret
    { name: 'PUBLIC_VAR', value: 'visible' },
  ],
})
// Per-exec env vars:
const result = await sandbox.process.exec({
  command: 'echo $API_KEY',
  env: { API_KEY: 'sk-...' },
  waitForCompletion: true,
})
```

**Python:**
```python
# BEFORE (Modal) - vault-based secrets
secret = modal.Secret.from_name("my-secret")
ephemeral_secret = modal.Secret.from_dict({"API_KEY": "sk-..."})
dotenv_secret = modal.Secret.from_dotenv()
sandbox = app.spawn_sandbox(image=image, secrets=[secret, ephemeral_secret])

# AFTER (Blaxel) - environment variables with secret flag
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "blaxel/base-image:latest",
    "envs": [
        {"name": "API_KEY", "value": "sk-...", "secret": True},
        {"name": "PUBLIC_VAR", "value": "visible"},
    ],
})
# Per-exec env vars:
result = await sandbox.process.exec({
    "command": "echo $API_KEY",
    "env": {"API_KEY": "sk-..."},
    "wait_for_completion": True,
})
```

> **Note:** Blaxel does not have a vault-style secret management API. For production, use the Variables-and-secrets page in the Blaxel Console. The SDK auto-detects `.env` files for authentication (similar to `Secret.from_dotenv()`).

### Connect tokens / Sessions

Modal's `createConnectToken()` provides authenticated access to a sandbox. Blaxel has two equivalents: preview tokens (for HTTP access to sandbox services) and sessions (for SDK-based sandbox access from frontends).

**TypeScript:**
```typescript
// BEFORE (Modal) - connect token for sandbox access
const { url, token } = await sandbox.createConnectToken({ userMetadata: 'user-123' })

// AFTER (Blaxel) - Option 1: Preview token for HTTP access
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'app-preview' },
  spec: { port: 3000, public: false },
})
const token = await preview.tokens.create(new Date(Date.now() + 3600000)) // 1 hour
const accessUrl = `${preview.spec?.url}?bl_preview_token=${token.value}`

// AFTER (Blaxel) - Option 2: Session for SDK-based frontend access
const session = await sandbox.sessions.create({
  expiresAt: new Date(Date.now() + 3600000),
})
// Pass session token to frontend, then reconstruct the SDK client:
const frontendSandbox = await SandboxInstance.fromSession(session.token)
```

**Python:**
```python
# BEFORE (Modal)
result = sandbox.create_connect_token(user_metadata="user-123")

# AFTER (Blaxel) - Preview token for HTTP access
preview = await sandbox.previews.create_if_not_exists({
    "metadata": {"name": "app-preview"},
    "spec": {"port": 3000, "public": False},
})
token = await preview.tokens.create(datetime.now() + timedelta(hours=1))
access_url = f"{preview.spec.url}?bl_preview_token={token.value}"

# AFTER (Blaxel) - Session for SDK-based frontend access
session = await sandbox.sessions.create({
    "expires_at": datetime.now() + timedelta(hours=1),
})
# Pass session token to frontend
```

### Filesystem operations

Modal uses low-level file handles (`open`, `read`, `write`, `close`) or newer `ls`/`mkdir`/`rm` methods. Blaxel has high-level methods throughout.

| Operation | Modal | Blaxel |
|-----------|-------|--------|
| Write file | `file = sandbox.open(path, 'w')` → `file.write(encoded)` → `file.close()` | `sandbox.fs.write(path, content)` |
| Read file | `file = sandbox.open(path, 'r')` → `file.read()` → `file.close()` | `sandbox.fs.read(path)` |
| List files | `sandbox.ls(path)` or `sandbox.exec(['ls', path])` | `sandbox.fs.ls(path)` |
| Create dir | `sandbox.mkdir(path)` or `sandbox.exec(['mkdir', '-p', path])` | `sandbox.fs.mkdir(path)` |
| Delete file | `sandbox.rm(path)` | `sandbox.fs.rm(path)` / `sandbox.fs.rm(path, { recursive: true })` |
| Copy file | `sandbox.exec(['cp', ...])` | `sandbox.fs.cp(src, dest)` |
| Watch files | `sandbox.watch(path)` (Alpha) | `sandbox.fs.watch(path, callback, { withContent: true, ignore: ['node_modules'] })` |
| Fuzzy search | N/A | `sandbox.fs.search(query, path)` |
| Write tree | N/A | `sandbox.fs.writeTree(files, basePath)` / `write_tree(files, base)` |
| Write binary | `file.write(bytes)` | `sandbox.fs.writeBinary(path, buffer)` / `write_binary(path, bytes)` |
| Read binary | `file.read()` | `sandbox.fs.readBinary(path)` / `read_binary(path)` |
| Search content | N/A | `sandbox.fs.grep(pattern, path)` |
| Find files | N/A | `sandbox.fs.find(path, { patterns: ['*.ts'] })` |

**TypeScript:**
```typescript
// BEFORE (Modal) - low-level file handles
const file = await sandbox.open('/app/file.txt', 'w')
await file.write(new TextEncoder().encode('hello'))
await file.close()

const rFile = await sandbox.open('/app/file.txt', 'r')
const data = await rFile.read()
await rFile.close()
const content = new TextDecoder().decode(data)

const p = await sandbox.exec(['ls', '/app'])
const listing = await p.stdout.readText()

// AFTER (Blaxel) - high-level one-liners
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
# BEFORE (Modal) - low-level file handles
with sandbox.open("/app/file.txt", "w") as f:
    f.write(b"hello")

with sandbox.open("/app/file.txt", "r") as f:
    content = f.read().decode()

process = sandbox.exec("ls", "/app")
listing = process.stdout.read()

# AFTER (Blaxel) - high-level one-liners
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

### Preview URLs / Tunnels

Modal uses tunnels for exposing sandbox ports. Blaxel has dedicated preview URL management.

**TypeScript:**
```typescript
// BEFORE (Modal) - tunnels for port access
const sandbox = await client.sandboxes.create(app, image, {
  encrypted_ports: [3000],
})
const tunnels = await sandbox.tunnels()
const url = tunnels.get(3000)?.url

// AFTER (Blaxel) - dedicated preview URL with access control
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/node:latest',
  region: 'us-pdx-1',
  memory: 2048,
  ports: [{ target: 3000, protocol: 'HTTP' }],
})

const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'app-preview' },
  spec: { port: 3000, public: true },
})
const url = preview.spec?.url  // https://xxxx.preview.bl.run
```

**Python:**
```python
# BEFORE (Modal) - tunnels for port access
sandbox = app.spawn_sandbox(image=image, encrypted_ports=[3000])
tunnels = sandbox.tunnels()
url = tunnels[3000].url

# AFTER (Blaxel) - dedicated preview URL with access control
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "blaxel/node:latest",
    "region": "us-pdx-1",
    "memory": 2048,
    "ports": [{"target": 3000, "protocol": "HTTP"}],
})

preview = await sandbox.previews.create_if_not_exists({
    "metadata": {"name": "app-preview"},
    "spec": {"port": 3000, "public": True},
})
url = preview.spec.url  # https://xxxx.preview.bl.run
```

### Snapshot / Pause / Resume

Modal uses filesystem snapshots for pause/resume. Blaxel handles this automatically with scale-to-zero.

**TypeScript:**
```typescript
// BEFORE (Modal) - manual snapshot and restore
const snapshotImage = await sandbox.snapshotFilesystem()
await sandbox.terminate()
// ... later ...
const newSandbox = await client.sandboxes.create(app, snapshotImage, {
  regions: ['us-west-2'],
})

// AFTER (Blaxel) - automatic: sandboxes auto-pause after ~5s inactivity
// and resume in <25ms on the next API call. No explicit snapshot needed.
// State (memory + filesystem) is preserved automatically.
const sandbox = await SandboxInstance.get('my-sandbox')
```

**Python:**
```python
# BEFORE (Modal) - manual snapshot and restore
snapshot_image = sandbox.snapshot_filesystem()
sandbox.terminate()
# ... later ...
new_sandbox = app.spawn_sandbox(image=snapshot_image)

# AFTER (Blaxel) - automatic, just reconnect by name
sandbox = await SandboxInstance.get("my-sandbox")
```

> **Directory snapshots:** Modal's `snapshotDirectory()` / `mountImage()` for sharing directory state between sandboxes has no direct Blaxel equivalent. Blaxel auto-preserves sandbox state across scale-to-zero. To share pre-built directory state across multiple sandboxes, use volume templates (`bl new volume-template`) to create volumes pre-populated with files.

### Volumes

**TypeScript:**
```typescript
// BEFORE (Modal) - mount volumes and cloud buckets
const sandbox = await client.sandboxes.create(app, image, {
  mounts: [modal.Mount.from_local_dir('./data', remote_path='/data')],
  volumes: { '/persistent': myVolume },
})
await sandbox.reloadVolumes()

// AFTER (Blaxel) - attach volumes at creation
import { VolumeInstance, SandboxInstance } from '@blaxel/core'

const volume = await VolumeInstance.createIfNotExists({
  name: 'my-volume',
  size: 1024,
  region: 'us-pdx-1',
})
const sandbox = await SandboxInstance.createIfNotExists({
  name: 'my-sandbox',
  image: 'blaxel/base-image:latest',
  region: 'us-pdx-1',
  memory: 2048,
  volumes: [{ name: 'my-volume', mountPath: '/data', readOnly: false }],
})
```

**Python:**
```python
# BEFORE (Modal) - mount volumes
volume = modal.Volume.from_name("my-volume", create_if_missing=True)
sandbox = app.spawn_sandbox(image=image, volumes={"/data": volume})

# AFTER (Blaxel) - attach volumes at creation
from blaxel.core import VolumeInstance, SandboxInstance

volume = await VolumeInstance.create_if_not_exists({
    "name": "my-volume",
    "size": 1024,
    "region": "us-pdx-1",
})
sandbox = await SandboxInstance.create_if_not_exists({
    "name": "my-sandbox",
    "image": "blaxel/base-image:latest",
    "region": "us-pdx-1",
    "memory": 2048,
    "volumes": [{"name": "my-volume", "mount_path": "/data", "read_only": False}],
})
```

> **`reloadVolumes()` not needed:** Modal requires `sandbox.reload_volumes()` / `sb.reloadVolumes()` to sync volume changes. Blaxel volumes are persistent block storage mounted directly — changes are immediately visible without reload.

> **Ephemeral volumes:** Modal's `modal.volumes.ephemeral()` for temporary shared storage between sandboxes has no Blaxel equivalent. Blaxel only supports persistent named volumes. Workaround: create a named volume and delete it when done, or use the sandbox filesystem (data persists across auto-pause/resume).

### Sandbox lifecycle

| Operation | Modal | Blaxel |
|-----------|-------|--------|
| Terminate | `sandbox.terminate()` | `sandbox.delete()` |
| Detach (release connection) | `sandbox.detach()` | N/A (stateless API calls) |
| Wait for completion | `sandbox.wait()` | `sandbox.process.exec({ waitForCompletion: true })` (max 60s) or `sandbox.process.wait('name', { maxWait: 300000 })` for longer |
| Exit code | `sandbox.returncode` / `result.wait()` | `result.exitCode` on process response, or `(await sandbox.process.get('name')).exitCode` |
| Poll exit code | `sandbox.poll()` | `sandbox.process.get('name')` — check `.status` and `.exitCode` |
| List sandboxes | `Sandbox.list(app, tags={...})` | `SandboxInstance.list()` (SDK) or `bl get sandboxes` (CLI). Labels in metadata for filtering |
| Get by ID | `Sandbox.from_id(id)` | `SandboxInstance.get('name')` (Blaxel uses human-readable names, not opaque IDs) |
| Get by name | `Sandbox.from_name(name, app)` | `SandboxInstance.get('name')` |
| Tags / Labels (read) | `sandbox.get_tags()` | `sandbox.metadata.labels` |
| Tags / Labels (write) | `sandbox.set_tags({...})` | Set `labels` at creation; update via `SandboxInstance.updateMetadata('name', { labels: {...} })` |
| Process management | `result.wait()` / `result.terminate()` | `sandbox.process.get('name')`, `.stop('name')` (SIGTERM), `.kill('name')` (SIGKILL), `.list()`, `.wait('name')` |

**TypeScript:**
```typescript
// BEFORE (Modal)
await sandbox.terminate()

// AFTER (Blaxel)
await sandbox.delete()
```

**Python:**
```python
# BEFORE (Modal)
sandbox.terminate()

# AFTER (Blaxel)
await sandbox.delete()
```

## Key differences

- **No client/app boilerplate**: Modal requires `ModalClient` → `App` → `Image` → `Sandbox` (TS) or `modal.App()` → `Image` → `spawn_sandbox()` (Python). Blaxel uses a single `SandboxInstance.createIfNotExists()` / `create_if_not_exists()` call
- **No programmatic image building**: Modal builds images via chained SDK methods (`fromRegistry().dockerfileCommands()`, `.pip_install()`, `.apt_install()`). Blaxel uses standard Dockerfiles deployed with `bl deploy`
- **No GPU support**: Modal supports GPU-accelerated sandboxes (T4, A10G, A100, H100, etc.). Blaxel sandboxes are CPU-only
- **No entrypoint command at creation**: Modal allows `command: [...]` at sandbox creation. Blaxel requires creating the sandbox first, then calling `process.exec()`
- **High-level filesystem API**: Modal uses low-level file handles (`open`/`read`/`write`/`close`). Blaxel has `fs.write()`, `fs.read()`, `fs.ls()`, `fs.rm()`, `fs.cp()`, `fs.writeTree()` / `write_tree()`
- **Log streaming model**: Modal uses pipe-based stdout/stderr streams. Blaxel uses callbacks (`onLog`, `onStdout`, `onStderr`) on `process.exec()`, `process.streamLogs()`, and `process.logs()` for retrieval
- **Native env vars and working dir**: Modal requires manual shell string construction for env vars. Blaxel accepts `env` and `workingDir` / `working_dir` as parameters
- **Environment variables as secrets**: Modal has vault-based `Secret.from_name()`. Blaxel uses `envs: [{ name: 'KEY', value: 'val', secret: true }]` — no separate vault API
- **Auto scale-to-zero**: Blaxel sandboxes auto-pause after ~5s of inactivity and resume in <25ms. No manual snapshots needed. Modal requires explicit `snapshotFilesystem()` / `snapshot_filesystem()` + `terminate()`. For idle-based *deletion*, Blaxel uses lifecycle expiration policies (`ttl-idle`)
- **Region format**: Modal uses cloud provider regions (`us-west-2`, `us-central1`). Blaxel uses `us-pdx-1`
- **Ports declared at creation**: Blaxel requires ports at sandbox creation time; they cannot be added later. Ports 80, 443, 8080 are reserved
- **Preview URLs vs Tunnels**: Modal uses `encrypted_ports` + `tunnels()`. Blaxel has dedicated `previews.createIfNotExists()` / `create_if_not_exists()` with public/private access control and token-based authentication
- **Named sandboxes**: Blaxel supports `createIfNotExists` / `create_if_not_exists` with a `name` for idempotent creation (globally unique, not scoped to an app). Blaxel uses human-readable names, not opaque IDs
- **Process naming and management**: Blaxel processes can be named for later reference (`get`, `stop`, `kill`, `list`, `wait`, `logs` by name). Modal returns `ContainerProcess` objects
- **Dev server binding**: Dev servers must bind to `0.0.0.0` (not `localhost`) for preview URLs to work in Blaxel
- **Async Python**: Blaxel Python SDK is async-first (all calls use `await`); Modal Python SDK is sync by default
- **~50% memory reserved for tmpfs**: Blaxel uses half of sandbox memory for the in-memory filesystem. Use volumes for extra storage
- **Proxy/VPC**: Modal uses `modal.proxies.fromName(...)`. Blaxel uses VPC + egress gateway via `network: { vpcName: '...', egressGatewayName: '...' }` at sandbox creation

## Complete migration example

### TypeScript

**BEFORE (Modal):**
```typescript
import { ModalClient } from 'modal'

const client = new ModalClient()
const app = await client.apps.fromName('my-app', { createIfMissing: true })
const image = client.images.fromRegistry('python:3.11-slim')

const sandbox = await client.sandboxes.create(app, image, {
  regions: ['us-west-2'],
  memoryMiB: 2048,
  cpu: 1,
  timeoutMs: 1000 * 60 * 15,
  encrypted_ports: [3000],
})

// Write a file
const file = await sandbox.open('/app/index.js', 'w')
await file.write(new TextEncoder().encode('console.log("hello")'))
await file.close()

// Run a command
const result = await sandbox.exec(['bash', '-c', 'node /app/index.js'])
const stdout = await result.stdout.readText()
await result.wait()
console.log(stdout)

// Get tunnel URL
const tunnels = await sandbox.tunnels()
console.log(`Preview: ${tunnels.get(3000)?.url}`)

await sandbox.terminate()
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
})

// Write a file
await sandbox.fs.write('/app/index.js', 'console.log("hello")')

// Run a command
const result = await sandbox.process.exec({
  command: 'node /app/index.js',
  workingDir: '/app',
  waitForCompletion: true,
})

// Get a shareable preview URL
const preview = await sandbox.previews.createIfNotExists({
  metadata: { name: 'app-preview' },
  spec: { port: 3000, public: true },
})
console.log(`Preview: ${preview.spec?.url}`)

await sandbox.delete()
```

### Python

**BEFORE (Modal):**
```python
import modal

app = modal.App("my-app")
image = modal.Image.debian_slim().pip_install("numpy")

sandbox = app.spawn_sandbox(
    image=image,
    timeout=900,
    cpu=1,
    memory=2048,
    encrypted_ports=[3000],
)

# Write a file
with sandbox.open("/app/main.py", "w") as f:
    f.write(b'print("hello")')

# Run a command
process = sandbox.exec("bash", "-c", "python3 /app/main.py")
stdout = process.stdout.read()
process.wait()
print(stdout)

# Get tunnel URL
tunnels = sandbox.tunnels()
print(f"Preview: {tunnels[3000].url}")

sandbox.terminate()
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
        "ports": [{"target": 3000, "protocol": "HTTP"}],
        "envs": [{"name": "NODE_ENV", "value": "production"}],
    })

    # Write a file
    await sandbox.fs.write("/app/main.py", 'print("hello")')

    # Run a command
    result = await sandbox.process.exec({
        "command": "python3 /app/main.py",
        "working_dir": "/app",
        "wait_for_completion": True,
    })

    # Get a shareable preview URL
    preview = await sandbox.previews.create_if_not_exists({
        "metadata": {"name": "app-preview"},
        "spec": {"port": 3000, "public": True},
    })
    print(f"Preview: {preview.spec.url}")

    await sandbox.delete()

asyncio.run(main())
```

## Resources

- Blaxel docs: https://docs.blaxel.ai
- Blaxel sandbox images: https://github.com/blaxel-ai/sandbox/tree/main/hub
- Blaxel sandbox templates (custom Dockerfiles): https://docs.blaxel.ai/Sandboxes/Sandbox-Templates
- Modal sandbox docs: https://modal.com/docs/guide/sandboxes
- Modal sandbox networking: https://modal.com/docs/guide/sandbox-networking
- SDK reference (TypeScript): `@blaxel/core` — see ./references/sdk-typescript.md
- SDK reference (Python): `blaxel` — see ./references/sdk-python.md
