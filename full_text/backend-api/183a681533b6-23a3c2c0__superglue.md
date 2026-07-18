---
name: superglue
description: "Build, test, deploy and integrate superglue tools via the sg CLI and superglue SDKs. IMPORTANT — you MUST invoke this skill and read the full reference BEFORE running ANY sg command or writing ANY superglue SDK/REST/webhook integration code. Before using the sg CLI, first check that it is installed (run sg --version; if not found, install with npm install -g @superglue/cli), then verify either that it is configured with sg login or, for headless/API-key auth, that SUPERGLUE_API_KEY and SUPERGLUE_API_ENDPOINT environment variables are set. If not, guide the user through setup first. After reading SKILL.md, also run `sg skill <topic>` for the specific protocols and topics involved."
---

# superglue CLI (`sg`) — Agent Reference

This file is the entry point for operating superglue via the `sg` CLI. It covers setup, tool building, tool editing, system management, running tools, schedules, and deployment via SDK/REST/webhooks.

For protocol-specific details (HTTP, databases, Redis, file servers, GraphQL), file handling, access rules, SDK integration, and general superglue information, run `sg skill <topic>` (linked throughout and listed at the bottom).

## Reference Files

Read these on demand — they are authoritative for their topic and kept in sync with the web agent's skill references.

| `sg skill` command        | When to read                                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| `sg skill superglue-info` | Company info, interfaces (SDK, REST API, MCP, Web), web UI layout, execution pipeline, internals     |
| `sg skill integration`    | Deploying tools — SDK (TS/Python) usage, REST API calls, webhook triggers, retry patterns            |
| `sg skill http`           | HTTP step configuration, auth patterns, file uploads, response handling, pagination, error detection |
| `sg skill graphql`        | GraphQL step config, schema introspection, error recovery                                            |
| `sg skill postgres`       | PostgreSQL connection URLs, SSL/TLS handling, schema introspection, parameterized queries            |
| `sg skill mssql`          | MSSQL / Azure SQL connection URLs, schema introspection, parameterized queries                       |
| `sg skill odbc`           | ODBC connections (SAP ASE / Sybase via FreeTDS), driver config, positional `?` params                |
| `sg skill redis`          | Redis command syntax, connection URLs, key type handling                                             |
| `sg skill mongodb`        | MongoDB connection URLs (mongodb:// / mongodb+srv://), CRUD operations, Extended JSON, aggregation   |
| `sg skill sftp-smb`       | SFTP, FTP, and SMB operations, file upload/download semantics, path handling                         |
| `sg skill file-handling`  | File detection, parsing, `file::` reference syntax, lazy base64 access, transform-produced files     |
| `sg skill access-rules`   | RBAC roles, resource grants, and tool/system permissions (enterprise only)                           |

## CRITICAL RULES — READ FIRST

**Pre-requisites for using the CLI**

1. **Check CLI exists**: Run `sg --version`. If it fails with `command not found`, install: `npm install -g @superglue/cli`.
2. **Keep CLI and SDK up to date**: Always use the latest versions. Run `sg update` to update the CLI. For the SDK, run `npm install @superglue/client@latest` (JS) or `pip install --upgrade superglue-client` (Python).
3. **Verify configuration**: Run `sg whoami` or `sg system list`. If it fails with `fetch failed` or auth errors, the CLI needs configuration via `sg login` (see Setup below). For custom/self-hosted instances, the CLI must know the instance API endpoint; browser login also needs the web app endpoint when it differs from the API URL. Use API-key auth only for headless/legacy environments.

**Calling systems and running tools**

1. ALWAYS pull the relevant system context using `sg system find` before calling system endpoints and before building tools.
2. Use `sg system search-docs` for a targeted keyword search of system docs when unsure how a system works.

**Authentication & Credentials**

- Authentication must ALWAYS be explicitly configured — nothing is injected automatically in any protocol.
- HTTP: include auth headers using `<<systemId_credentialKey>>` (e.g. `"Authorization": "Bearer <<my_api_access_token>>"`).
- Databases/Redis/file servers: embed credential placeholders in the connection URL (e.g. `postgres://<<sys_user>>:<<sys_pass>>@host/db`).
- OAuth: token refresh is automatic, but the header must still be explicit.

**Saving tools**

- Never save a tool without explicit user confirmation. Build + run, present results, then save with `sg tool save --draft <id>` only after the user approves.

**Non-interactive environments (AI agents, CI)**

- Pass all secret values directly via `--credentials '{"api_key":"sk-xxx"}'`. Ask the user for secret values, then include them in the JSON.

---

## Setup

### Installing the CLI

```bash
npm install -g @superglue/cli
```

After installation the `sg` command is available globally.

### Authentication

The preferred CLI setup is browser OAuth via `sg login`. Headless/API-key auth is available for CI and legacy automation. The API endpoint defaults to `https://api.superglue.cloud`.

**Browser login (humans):**

```bash
sg login
sg --endpoint "https://custom-api.example.com" login --web-endpoint "https://custom-app.example.com" --save-config
```

Opens the browser, completes OAuth login, and stores the OAuth session in `~/.superglue/auth.json`. This file is separate from `config.json`. Use `--save-config` to persist non-secret endpoint settings in `config.json`, and `sg logout` to remove the OAuth session.

**Headless/API-key auth (CI, agents, backwards-compatible):**

Use environment variables, global flags, or an existing `.superglue/config.json`. `sg init` remains available as a legacy hidden command for scripts that already use it, but new setup should prefer `sg login` for humans and env vars/config files for headless API-key auth.

**Environment variables (no config file):**

```bash
export SUPERGLUE_API_KEY="your-api-key"
export SUPERGLUE_API_ENDPOINT="https://api.superglue.cloud"   # optional, this is the default
```

**Config resolution order:** CLI flags > environment variables > local `.superglue/config.json` > global `~/.superglue/config.json`. For authentication, API keys from flags/env/config take precedence; if no API key is configured, the CLI uses the matching OAuth session from `~/.superglue/auth.json`.

Verify with `sg whoami` or `sg system list` — should return authenticated context without errors.

### Capability Presets

Set via `SUPERGLUE_CLI_PRESET` env var or `config.json` as `"preset"`. Legacy `sg init --preset` still writes this value for existing scripts.

| Preset    | Description                                                                                    |
| --------- | ---------------------------------------------------------------------------------------------- |
| `runner`  | Run saved tools by ID only. Read-only lookups. No building/editing                             |
| `builder` | Runner + build/edit/save tools, call systems, manage MCP servers and schedules. No system CRUD |
| `admin`   | Full access (default)                                                                          |

Blocked commands print a clear error showing the current preset and how to change it.

### Global Flags

| Flag               | Description                                 |
| ------------------ | ------------------------------------------- |
| `--table`          | Human-readable table output (default: JSON) |
| `--full`           | Disable truncation of large fields          |
| `--api-key <key>`  | Override API key                            |
| `--endpoint <url>` | Override API endpoint                       |

---

## Workflow

### Building a Tool

1. **Load relevant protocol references** via `sg skill <topic>` based on the systems involved (http, postgres, graphql, etc.)
2. Use `sg system find` for every involved system — note the available secret names and the system URL
3. Use `sg system search-docs` for each system — look up endpoints, auth patterns, pagination, response structure
4. Use `sg system call` to test 1-2 primary endpoints — verify response structure and field names before building
5. Call `sg tool build --config '{...}'` with the full tool config (see Reference → Tool Config Schema)
6. Test with `sg tool run --draft <draftId>`. Use `--include-step-results` to inspect raw step data
7. Iterate using `sg tool edit --draft <draftId> --patches '[...]'` (see Reference → Tool Editing)
8. Present results to the user and ask for approval. Only then run `sg tool save --draft <draftId>`

### Editing a Tool

1. Use `sg tool find --id <toolId>` or `sg tool find <query>` to locate the tool and inspect its current config
2. Determine whether upstream steps use object or array selectors so you reference `.data` correctly in downstream code
3. Plan the JSON Patch operations (RFC 6902)
4. Apply with `sg tool edit --tool <toolId> --patches '[...]'` (or `--draft <draftId>` for drafts)
5. Re-run to verify behavior

### Creating/Editing a System

1. Search for an existing system first: `sg system find <query>`
2. If creating: `sg system create --name "..." --url "..." --credentials '{...}'`. Prefer `--template <id>` when one exists — it auto-fills URL and OAuth config
3. For OAuth: `sg system oauth --system-id <id> [--scopes "..."]` opens a browser flow. User approves → tokens saved automatically
4. For non-OAuth secrets: `sg system credentials set --system-id <id> --credentials '{...}'`
5. Verify connectivity with `sg system call`
6. For updates: `sg system edit --id <id>` with the fields to change

### Running a Tool (Ad-hoc)

```bash
sg tool run --tool <toolId> --payload '{"userId":"123"}'
sg tool run --draft <draftId> --payload-file payload.json
```

Streams live execution logs to the terminal. Use `--include-step-results` for raw per-step responses and `--include-config` for the full config dump.

### Creating/Editing a Named MCP Server

Named MCP servers expose a selected set of saved tools through an MCP endpoint. The CLI always uses the configured superglue API endpoint, so it works for Cloud and self-hosted instances when `SUPERGLUE_API_ENDPOINT` or `--endpoint` points at the right API.

1. Verify CLI setup: `sg system list` or `sg mcp list`
2. Find saved tools to expose: `sg tool list` or `sg tool find <query>`
3. Create the server:
   ```bash
   sg mcp create --name sales-tools --tool get_customer --tool create_invoice
   ```
4. Use the returned `server.connection.endpoint` and `clientConfig` in the MCP client.
5. Edit later with:
   ```bash
   sg mcp edit --id <serverId> --add-tool another_tool
   sg mcp edit --id <serverId> --tools get_customer,create_invoice
   ```

Auth modes:

- `oauth` (default): OAuth-capable MCP clients authenticate users through the MCP auth flow.
- `creator_api_key`: private/headless clients must send `Authorization: Bearer <SUPERGLUE_API_KEY>` where the key is active and assigned to the MCP server creator.

If `sg mcp ...` returns "MCP server management is not available", the target instance or plan does not support named MCP server management. The default all-tools MCP endpoint may still be usable at `<api-endpoint>/mcp`.

### Creating/Editing Tool Schedules

Schedules run saved tools on cron expressions. Use 5-field cron syntax and an IANA timezone.

```bash
sg schedule list
sg schedule list --tool <toolId>
sg schedule create --tool daily_report --cron "0 9 * * 1-5" --timezone UTC
sg schedule edit --tool daily_report --id <scheduleId> --disabled
sg schedule edit --tool daily_report --id <scheduleId> --cron "0 8 * * *" --timezone UTC
```

Optional flags:

- `--payload '{"key":"value"}'` or `--payload-file payload.json` sets the scheduled run payload.
- `--webhook-url <url>` posts results to a webhook after success.
- `--tool-chain <toolId>` runs another saved tool after success.
- `--retries <n>` and `--timeout <ms>` set request options.
- `--clear-webhook` removes the webhook/tool-chain success action during edit.

---

## Reference

### Tool Translation (web agent tool → CLI command)

Agents familiar with the web tool names can map them directly to CLI commands:

| Web agent tool                                   | CLI command                                    | Notes                                                              |
| ------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------ |
| `build_tool`                                     | `sg tool build --config '{...}'`               | CLI is not AI-powered — you provide the full JSON config           |
| `edit_tool`                                      | `sg tool edit --tool <id> --patches '[...]'`   | JSON Patch (RFC 6902). Use `--draft <id>` for drafts               |
| `run_tool`                                       | `sg tool run --tool <id>` / `--draft <id>`     | Add `--include-step-results` to inspect per-step data              |
| `save_tool`                                      | `sg tool save --draft <draftId>`               | Persists a draft to the database                                   |
| `run_command` with `vfs` for `/org/tools/`       | `sg tool find --id <id>` / `sg tool find <q>`  | Full config with `--id`, compact search with a query string        |
| `create_system`                                  | `sg system create --name "..." --url "..."`    | Use `--template <id>` when available                               |
| `edit_system`                                    | `sg system edit --id <id> ...`                 | Supports `--env dev\|prod`                                         |
| `run_command` with `vfs` for `/org/systems/`     | `sg system find <query>` / `--id <id>`         | Returns secret-key presence and the system URL                     |
| Credentials VFS / saved credentials              | `sg system credentials get/set/clear`          | Manage the current user's credentials for a system                 |
| `call_system`                                    | `sg system call --url "..." --system-id <id>`  | Authenticated ad-hoc calls for testing / schema introspection      |
| `run_command search`                             | `sg system search-docs --system-id <id> -k`    | Targeted keyword search over ingested system docs                  |
| `authenticate_oauth`                             | `sg system oauth --system-id <id> [--scopes]`  | Opens browser flow. Supports `--grant-type client_credentials` too |
| `run_command` with `vfs` for `/org/runs/`        | `sg run list` / `sg run get <runId>`           | Filter `list` by `--tool`, `--status`, `--source`, `--limit`       |
| `run_command` with `vfs` for `/org/mcp-servers/` | `sg mcp list` / `sg mcp find --id <id>`        | Returns endpoint, auth mode, selected tool IDs, and client config  |
| `create_mcp_server`                              | `sg mcp create --name <n> --tool <id>`         | Creates a named MCP endpoint for selected saved tools              |
| `edit_mcp_server`                                | `sg mcp edit --id <id> ...`                    | Edits name, auth mode, description, or selected tool IDs           |
| `create_schedule`                                | `sg schedule create --tool <id> --cron <expr>` | Creates a cron schedule for a saved tool                           |
| `edit_schedule`                                  | `sg schedule edit --tool <id> --id <schedule>` | Updates, enables, or disables an existing schedule                 |
| (no direct equivalent)                           | `sg login`, `sg update`, `sg skill`            | CLI-specific setup, updater, and this reference system             |

Web-agent-only concepts with no CLI equivalent: `run_command`'s virtual filesystem (CLI uses concrete `sg` subcommands), `authenticate_oauth`'s dedicated MCP `authenticate` tool (CLI uses `sg system oauth`).

### Command Reference

**`sg login`** — Browser OAuth setup. Stores the OAuth session in `~/.superglue/auth.json`. Flags: `--web-endpoint`, `--no-browser`, `--save-config`, `--global`. Use global `--endpoint` for custom/self-hosted API URLs.

**`sg logout`** — Removes the stored OAuth session from `~/.superglue/auth.json`.

**`sg whoami`** — Shows the authenticated superglue user and organization.

**Tool commands:**

```bash
sg tool build --config '{"id":"...","steps":[...]}'       # inline JSON
sg tool build --config tool.json                          # from file
sg tool build --id my-tool --instruction "..." --steps steps.json --payload '{...}'
sg tool run --draft <draftId> --payload '{"userId":"123"}'
sg tool run --tool my-tool --payload-file payload.json --include-step-results
sg tool edit --draft <draftId> --patches '[{"op":"replace","path":"/steps/0/config/url","value":"..."}]'
sg tool edit --tool my-tool --patches patches.json
sg tool save --draft <draftId>
sg tool list
sg tool find "shopify orders"       # keyword search (compact results)
sg tool find --id my-tool           # exact lookup (full config)
sg tool find --id my-tool --fields instruction,inputSchema  # only selected top-level fields (token-efficient)
```

**System commands:**

```bash
sg system create --name "My API" --url https://api.example.com --credentials '{"api_key":"sk-xxx"}'
sg system create --name "Slack" --template slack
sg system edit --id my_api --credentials '{...}'
sg system list
sg system find slack
sg system find --id my_api --env dev
sg system credentials get --system-id my_api
sg system credentials set --system-id my_api --credentials '{"api_key":"sk-xxx"}'
sg system credentials clear --system-id my_api
sg system call --url https://api.example.com/users --system-id my_api --method GET \
  --headers '{"Authorization":"Bearer <<my_api_access_token>>"}'
sg system search-docs --system-id slack -k "send message channels"
sg system oauth --system-id gmail --scopes "https://www.googleapis.com/auth/gmail.readonly"
sg system oauth --system-id my_api --grant-type client_credentials --scopes "read write"
```

**MCP server commands:**

```bash
sg mcp list
sg mcp find sales
sg mcp find --id <serverId>
sg mcp create --name sales-tools --tool get_customer --tool create_invoice
sg mcp create --name sales-tools --tools get_customer,create_invoice --auth-mode oauth
sg mcp edit --id <serverId> --add-tool another_tool
sg mcp edit --id <serverId> --remove-tool old_tool
sg mcp edit --id <serverId> --auth-mode creator_api_key
```

**Run commands:**

```bash
sg run list --tool my-tool --status failed --limit 20
sg run get <runId> --full
sg run get <runId> --fetch-results  # alias for --full
```

**File attachments:**

```bash
sg tool run --draft <id> --payload '{"data":"file::mysheet"}' --file mysheet=data.xlsx
```

Attach files with repeatable `--file key=path`. Reference in payloads with `file::<key>`. Auto-parsed to JSON where applicable. See `sg skill file-handling` for the full reference syntax including `.raw`, `.base64`, and `.extracted` suffixes.

### Tool Config Schema

```json
{
  "id": "kebab-case-tool-name",
  "instruction": "Brief 1-2 sentence description of what this tool does and returns",
  "steps": [
    {
      "id": "unique-step-id",
      "config": {
        "type": "request",
        "systemId": "example_system",
        "url": "<<example_system_url>>/endpoint?param=<<payload_field>>",
        "method": "GET",
        "headers": { "Authorization": "Bearer <<example_system_access_token>>" },
        "queryParams": { "limit": "10" },
        "body": "{ \"key\": \"<<payload_field>>\" }"
      },
      "dataSelector": "(sourceData) => sourceData.previousStep.data.items",
      "failureBehavior": "fail",
      "modify": false
    }
  ],
  "outputTransform": "(sourceData) => sourceData.stepId.data",
  "outputSchema": { "type": "object", "properties": {} },
  "inputSchema": { "type": "object", "properties": {} }
}
```

**Request step fields** (HTTP, Postgres, MSSQL, Redis, MongoDB, FTP/SFTP, SMB) — see protocol-specific references for full details:

| Field         | Type   | Description                                                              |
| ------------- | ------ | ------------------------------------------------------------------------ |
| `type`        | string | `"request"` (default, can be omitted)                                    |
| `systemId`    | string | Optional. Links system credentials for `<<systemId_credKey>>` resolution |
| `url`         | string | Full URL with `<<variable>>` placeholders. Required.                     |
| `method`      | string | HTTP method (HTTP only)                                                  |
| `headers`     | object | HTTP headers with credential placeholders (HTTP only)                    |
| `queryParams` | object | URL query parameters (HTTP only)                                         |
| `body`        | string | Request body / DB query / Redis command / file operation                 |
| `pagination`  | object | Auto-pagination config (HTTP only, see `sg skill http`)                  |

**Transform step fields:**

| Field           | Type   | Description                                        |
| --------------- | ------ | -------------------------------------------------- |
| `type`          | string | `"transform"` — required for transform steps       |
| `transformCode` | string | `(sourceData) => transformedData` — single-line JS |

Transform steps do NOT have `systemId`, `url`, `method`, `headers`, `body`, `queryParams`, or `pagination`.

**Step behavior fields:**

| Field             | Type    | Description                                          |
| ----------------- | ------- | ---------------------------------------------------- |
| `dataSelector`    | string  | JS function controlling step input and loop mode     |
| `failureBehavior` | string  | `fail` (default) or `continue`                       |
| `modify`          | boolean | Set `true` only when the step writes/updates/deletes |

### Expression Syntax (`<<>>`)

All step config fields (url, headers, body, queryParams) support `<<expression>>` placeholders.

**Simple top-level keys** — only these work without arrow functions:

```
<<userId>>             payload inputs
<<currentItem>>        whole current loop item
<<page>> <<offset>> <<cursor>> <<limit>> <<pageSize>>   pagination variables
<<systemId_api_key>>   system credentials (namespaced: systemId_credKey)
<<systemId_url>>       system base URLs (namespaced: systemId_url)
<<sg_auth_email>>      email of the user triggering this run (in scheduled runs: the schedule creator)
<<sg_auth_jwt>>        short-lived signed JWT proving the identity of the user triggering this run; receivers verify it against superglue's outbound JWKS endpoint (/api/auth/outbound-jwks on the web app origin)
```

Simple `<<varName>>` only works for top-level keys. No dots, no nesting. `<<currentItem.id>>`, `<<sourceData.userId>>`, `<<user.name>>` all FAIL at runtime.

**Arrow function expressions** — for everything else:

```
<<(sourceData) => sourceData.currentItem.player_id>>
<<(sourceData) => sourceData.getUsers.data.map(u => u.id)>>
<<(sourceData) => JSON.stringify({ ids: sourceData.fetchUsers.data.map(u => u.id) })>>
```

Object/array return values are `JSON.stringify`'d automatically when spliced into strings.

### sourceData Object

`sourceData` is the cumulative state available to every JS expression, data selector, and transform:

```javascript
sourceData = {
  // Payload fields at ROOT level (NEVER use sourceData.payload.*)
  userId: "123",
  date: "2024-01-15",

  // Previous step results, keyed by step ID
  getUsers: { currentItem: {}, data: { users: [...] }, success: true },   // object selector
  fetchDetails: [                                                           // array selector
    { currentItem: "id1", data: { name: "Alice" }, success: true },
    { currentItem: "id2", data: { name: "Bob" }, success: true }
  ],

  // Current loop item (only set inside a looping step's config)
  currentItem: { id: 1 },

  // Credentials (flattened, namespaced)
  my_api_access_token: "...",
  my_api_api_key: "..."
}
```

### Naming Rules — Avoiding Key Collisions

Everything in `sourceData` shares ONE flat namespace. Saving a tool rejects payload input keys and step ids that collide with it:

- `__files__`, `currentItem`, `sg_auth_email`, `sg_auth_jwt` — injected by the runtime
- `page`, `offset`, `cursor`, `limit`, `pageSize` — rejected only when the tool has a paginated step, because they would shadow the live pagination counters; on non-paginated tools they are allowed but discouraged (a later edit that adds pagination will force a rename)
- the tool's own step ids — the step result overwrites a same-named payload key
- anything starting with `<systemId>_` for a system the tool uses — the entire prefix is reserved for namespaced credentials (`<systemId>_<credKey>`, `<systemId>_url`), even names that don't match an existing credential, because credentials added to the system later would silently shadow the input

Safe naming: payload inputs get specific, domain-flavored names (`customerId`, `reportMonth`, `maxResults` — prefer `maxResults` over `limit` even on non-paginated tools, and never prefix an input with a referenced system's id); step ids are verb-prefixed camelCase (`fetchUsers`) and distinct from every payload key. If the user asks for an input named like a reserved key, use a safe alternative and explain why.

### Step Result Envelopes

**Every** step result is wrapped in `{ currentItem, data, success }`. You MUST account for this when writing data selectors or transforms.

- **Object selector (or none)** — access via `sourceData.stepId.data`
- **Array selector (loop)** — array of envelopes: `sourceData.stepId.map(i => i.data)`
- **Paginated step** — all pages merged into a single `.data` field: access via `sourceData.stepId.data`. Do NOT `.map()` over it — returns a single object if one result, array if multiple (unwrapped from single-element array).

NEVER access step results without `.data`. `sourceData.stepId.results` hits the envelope, not the API response.

### Data Selectors

Control what a step receives as input and whether it loops:

| Return type        | Behavior                            |
| ------------------ | ----------------------------------- |
| Single object      | Step runs once with that object     |
| Array              | Step runs once per item (loop mode) |
| `undefined`/`null` | Step receives full sourceData       |

In loop mode, `sourceData.currentItem` is set to the current array element. Empty arrays are valid — the step skips execution.

### Transform Steps vs outputTransform

| Need                                        | Use                                                                    |
| ------------------------------------------- | ---------------------------------------------------------------------- |
| Reshape data for a SUBSEQUENT request step  | Transform step (`config.type: "transform"`)                            |
| Shape the final tool output                 | `outputTransform` (runs after all steps; slightly different signature) |
| Control input / looping for a step          | `dataSelector` on the step                                             |
| Inline data computation in URL/body/headers | `<<(sourceData) => ...>>` expressions                                  |

`outputTransform` must be a single-line JS string (no literal newlines or tabs).

**File output:** To make files downloadable from the tool's API response, set `outputFile: true` on the step that produces the file. The `outputTransform` is for shaping JSON data only — it does not handle files. Libraries `Papa` (CSV), `XLSX` (Excel), and `yaml` (YAML) are available in all transforms. See `sg skill file-handling` for details. Use `sg run download <runId>` to download artifacts.

**Complex request bodies** — when a body needs data from multiple steps or aggregation, use a preceding transform step:

```javascript
// Step: prepareBody (transform)
transformCode: "(sourceData) => { var items = sourceData.step1.data.results; return { data: items.filter(function(i) { return i.active; }), count: items.length }; }";

// Step: submitData (request)
body: "<<(sourceData) => JSON.stringify(sourceData.prepareBody.data)>>";
```

### Execution Pipeline

For each step in order:

1. Build `sourceData`: `{ ...originalPayload, ...previousStepResults, ...credentials }`
2. Run `dataSelector(sourceData)` → determines single vs loop execution
3. For each item: merge `currentItem` into `sourceData`, resolve `<<>>` variables, execute step
   - **Request step**: makes the HTTP/DB/FTP/Redis call, raw response becomes `.data`
   - **Transform step**: runs `transformCode(sourceData)`, return value becomes `.data`
4. Wrap result: `{ currentItem, data, success }` and store in `sourceData[stepId]`
5. After all steps: run `outputTransform(sourceData)` to shape final output

All user-provided JS runs in an isolated Deno sandbox.

### Credentials and Systems

Secrets are referenced by name as `<<systemId_credentialKey>>` and resolved from the selected credential at execution time. You MUST explicitly reference them:

```
System id="stripe", selected credential has secret named: api_key
→ Available as: <<stripe_api_key>>
```

**Auth header patterns:**

```json
{"Authorization": "Bearer <<stripe_api_key>>"}
{"Authorization": "Bearer <<gmail_access_token>>"}
{"X-API-Key": "<<my_api_api_key>>"}
{"Authorization": "Basic <<my_api_username>>:<<my_api_password>>"}
```

Basic auth auto-encodes: if the value after `Basic ` isn't already base64, the engine encodes it.

**System URL variables** — use these instead of hardcoding base URLs. They switch automatically between dev/prod environments:

```json
{ "url": "<<salesforce_url>>/services/data/v58.0/sobjects/Account" }
```

**Credential lifecycle:**

- Pass all secret values via `--credentials '{"api_key":"...","client_secret":"..."}'` on create/edit
- Use `sg system credentials set --system-id <id> --credentials '{...}'` to save secrets in the current API-key user's credential
- Use `sg system credentials get --system-id <id>` to inspect the current user's secret names and whether each has a non-empty value; secret values are never returned
- OAuth tokens (`access_token`, `refresh_token`) auto-refresh before each step execution
- Non-sensitive fields (`client_id`, `auth_url`, `token_url`) can be submitted alongside secrets in the same `--credentials` JSON

**System IDs:** lowercase letters, numbers, underscores only — no hyphens. Used for credential namespacing.

**Templates:** auto-populate endpoints and OAuth config. `sg system find` lists available templates.

- **Preconfigured OAuth** (no user `client_id`/`client_secret` needed): slack, salesforce, asana, notion, airtable, jira, confluence
- **Common OAuth templates:** gmail, googleDrive, googleCalendar, googleSheets, slack, salesforce, github, jira, confluence, notion, airtable, hubspot, shopify, dropbox, zoom, microsoft

**Custom OAuth (no template):** must include `client_id`, `client_secret`, `auth_url`, `token_url` in credentials at create time — or add later with `sg system edit`:

```bash
sg system create --name "My API" --url https://api.example.com \
  --credentials '{"client_id":"...","client_secret":"...","auth_url":"https://example.com/oauth/authorize","token_url":"https://example.com/oauth/token"}'
```

**Dev/Prod environments:** `--env dev|prod` at creation (immutable afterward). Two systems with the same ID but different environments are automatically linked. Dev systems inherit documentation from their linked prod system. When creating a dev system, always ask for new credentials — never copy from prod.

**System-specific instructions:** systems may include `specificInstructions` from the user (visible in `sg system find` output). Follow them when present — they override general patterns.

### Tool Editing (JSON Patch)

`sg tool edit` applies RFC 6902 JSON Patch operations. Each operation:

```typescript
{
  op: "add" | "remove" | "replace" | "move" | "copy" | "test",
  path: string,   // JSON Pointer, e.g. "/steps/0/config/url"
  value?: any,    // required for add, replace, test
  from?: string   // required for move, copy
}
```

**Key paths:**

- `/instruction` — tool description
- `/steps/N` — step at index N
- `/steps/N/config/url`, `/steps/N/config/method`, `/steps/N/config/headers`, etc.
- `/steps/N/dataSelector` — JS function controlling input + loop mode
- `/outputTransform` — final output shaping function
- `/outputSchema` — optional JSON schema for output

**Operations:**

- `replace` — Change an existing value. **Path must exist** — if the field is `null` or absent, `replace` fails. Prefer `add` when the field might be absent.
- `add` — Creates if missing, overwrites if present. Append to array with `/steps/-`.
- `remove` — Delete field or array element.
- `move` — Reorder or relocate.

**Validation:**

- Never patch `id` — tool IDs and draft IDs are immutable
- `op` and `path` required; `path` must start with `/`
- Patches applied **sequentially** — later patches see effects of earlier ones
- After patches, same validation as building (valid id, steps array, URLs on request steps, transformCode on transform steps)

**Downstream shape changes:** if you change a step's output shape, check if later dataSelectors and `outputTransform` need updating. When removing array elements, subsequent indices shift down.

### Draft Management

Drafts live under the active CLI config directory: local `.superglue/drafts/` when a project config exists, otherwise `~/.superglue/drafts/`. Draft filenames are base64url-encoded draft IDs, so use the `draftPath` returned by `sg tool build` and `sg tool edit` when inspecting raw draft files. Created by `sg tool build`, updated by `sg tool edit`, deleted by `sg tool save`. Ephemeral — not persisted to the superglue API until saved.

### Deployment

After building and saving, tools can be invoked from code via REST API, SDK, or webhook. See `sg skill integration` for complete SDK (TypeScript/Python), REST API, and webhook examples including retry patterns.

**IP whitelisting:** if a customer's system requires IP whitelisting for firewall rules, security groups, or vendor access controls, superglue Cloud outbound requests come from `34.234.12.178` and `18.198.191.215`. These IPs apply to superglue Cloud only; self-hosted and enterprise deployments use deployment-specific networking.

Quick reference:

```bash
# REST (sync)
curl -X POST "https://api.superglue.cloud/v1/tools/{toolId}/run" \
  -H "Authorization: Bearer $SUPERGLUE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"inputs":{"userId":"123"}}'

# Webhook trigger (async, fire-and-forget)
curl -X POST "https://api.superglue.cloud/v1/hooks/{toolId}?token=$SUPERGLUE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"userId":"123"}'
```

---

## Common Pitfalls

- **Guessing API endpoints** — always verify with `sg system search-docs` or `sg system call` first
- **`systemId` in the wrong place** — it belongs inside `step.config.systemId`, not on the step object
- **`<<(sourceData) => sourceData.payload.X>>`** — payload fields are at root level of `sourceData`, not under `.payload`
- **`<<currentItem.id>>`** — must use arrow function syntax: `<<(sourceData) => sourceData.currentItem.id>>`
- **Hardcoded pagination params** — use `<<page>>`, `<<offset>>`, `<<cursor>>`, `<<limit>>`
- **Missing auth headers** — credentials are never automatically included in any protocol, including for OAuth systems (only token refresh is automatic)
- **Hardcoded base URLs** — prefer system URL variables (`<<systemId_url>>`) for environment portability
- **Empty `instruction`** — never leave the tool-level `instruction` blank
- **Adding `outputSchema` unsolicited** — only add when the user explicitly requests a specific response structure
- **Multi-line `outputTransform`** — must be a single-line JS string (no literal newlines or tabs)
- **Regex literals in transforms** — `/.../ ` literals and complex escapes corrupt during serialization. Use `new RegExp()`, `.split()`, or `new URL()` instead
- **Complex bodies inline** — for bodies built from multiple steps, use a preceding transform step rather than stuffing multi-statement logic into `<<>>` expressions
- **Double-encoded JSON** — when the body contains nested/stringified JSON (e.g. LLM APIs), have `<<>>` expressions return a string via `JSON.stringify(...)`, and use a single expression for the whole body rather than mixing `<<>>` with static JSON
- **POST for read-only ops** — GraphQL queries via POST should have `modify: false`. Don't rely on HTTP method alone
- **Saving without approval** — always present `sg tool run` results and ask before `sg tool save`
- **Reserved key collisions** — payload inputs or step ids named after reserved/injected keys (see Naming Rules) are rejected at save time; pick a different name instead of retrying

---

## Error Recovery

For protocol-specific error recovery (HTTP, Postgres, MSSQL, Redis, MongoDB, GraphQL, SFTP/SMB), run `sg skill <protocol>`. General strategies below.

### Tool build fails validation

`sg tool build` returns a validation error. Read the message, fix the config, and re-run. Common causes: missing `id`, empty `steps`, missing `url` on request steps, missing `transformCode` on transform steps, `systemId` on the step object instead of `step.config.systemId`, or a key name collision (see Naming Rules) — rename the flagged input or step id.

### Tool runs but a step fails

1. Re-run with `--include-step-results` to see raw per-step responses and `data` fields
2. Use `sg system call` to test the failing endpoint directly — isolates step config vs system/auth issues
3. Use `sg system find --id <systemId>` to verify the stored secret names match what the step references
4. For HTTP: run `sg skill http` and follow the error recovery section (endpoint vs system isolation, credential scopes, rate limiting)
5. For databases: run `sg skill postgres` or `sg skill mssql` — SSL/TLS and schema issues are common causes
6. Use `sg system search-docs` and web search to verify the current API shape. APIs change across versions

### Authentication failures

1. Run `sg system find --id <systemId>` → check which secret names are present and whether they have non-empty values
2. For OAuth: re-run `sg system oauth` if tokens are missing or expired
3. For custom OAuth: verify `client_id`, `client_secret`, `auth_url`, `token_url` are all present. Confirm the redirect URI is registered on the provider's OAuth app
4. Check scopes — 403 / empty responses often mean the token lacks required scopes

### System creation fails

1. Check for an existing system with the same ID — use `sg system edit` to update instead
2. Ensure `id` uses only lowercase letters, numbers, and underscores (no hyphens)
3. For templated systems, verify the template ID is correct (`sg system find` lists available templates)

### Data selector / transform returns wrong data

1. Confirm whether the upstream step used an object selector (access `.data` directly) or an array selector (access via `.map(i => i.data)`)
2. Re-run with `--include-step-results` to see the exact envelope shape
3. Paginated steps merge into a single `.data` field — do not `.map()` over them
4. Verify `sourceData.currentItem` is only referenced inside looping steps (set by the step's own `dataSelector`, not upstream)

### Persistent failures

After 3-5 unsuccessful iterations on the same step, stop and ask the user for clarification or additional context (credentials, docs, expected payload shape). Don't keep guessing — gather evidence first.
