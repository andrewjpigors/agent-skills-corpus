---
name: extend-mcp-server
description: "Guides users through adding new tools or capabilities to an existing connector (MCP server). Handles eligibility, workspace setup, connector research, implementation via Software Engineer workflow, local testing, and PR submission with an extension-specific template."
use_cases:
  - "Add a tool to an existing connector"
  - "Extend a connector with new capabilities"
  - "Add functionality to the [service] MCP server"
  - "I want to add a new tool to the [service] connector"
---

# Extend an Existing MCP Connector

Guide users through adding new tools to an existing open-source MCP connector in the [`mcp-servers`](https://github.com/mindstone-engineering/mcp-servers) repository.

This skill is for when a user wants to **add a tool to an existing connector** — not build a new one from scratch. If the user wants to build a new connector, redirect to the [build-custom-mcp-server](../build-custom-mcp-server/SKILL.md) skill instead.

**Reference docs** (load as needed):
- [mcp-development-standard.md](../build-custom-mcp-server/references/mcp-development-standard.md) — SDK patterns, naming conventions, error handling, module architecture, security baseline, packaging
- [mcp-testing-guide.md](../build-custom-mcp-server/references/mcp-testing-guide.md) — Test strategy, test patterns, debugging common failures
- [contribute-connector.md](../build-custom-mcp-server/references/contribute-connector.md) — Contributing back to the ecosystem (lifecycle, PR template, quality bar, CI pipeline)
- [community-mcp-security-review.md](../../system/mcp-add-update-remove-connector/references/community-mcp-security-review.md) — Security review process for community MCPs

**Required orchestration workflow** (for Phase 4):
- [Software Engineer workflow](../../workflows/software-engineer/SKILL.md) — Structured coding orchestration (Understand → Plan → Implement → Review → Test & Deliver)


## Contribution State Reporting

Always report build progress at key checkpoints using the `rebel_mcp_report_contribution_state` bundled tool. This tracks the extension in the conversation UI (MCPBuildCard) and offers the user a one-click "Submit to community" option when ready. Call it regardless of whether the user intends to share — it powers local UI, not submission.

If `rebel_mcp_report_contribution_state` is not listed in your available tools, or `session_id` is missing from your `<dynamic_env>` context, skip all state reporting silently.

**Required parameters for every call:**
- `sessionId`: Use the `session_id` value from your `<dynamic_env>` context (must match exactly)
- `connectorName`: The connector name being extended
- `status`: The checkpoint status (see table below)
- `localServerPath` (at `draft` checkpoint): The full path to the local fork build directory

**Extension-specific parameters** (set at `ready_to_submit` checkpoint):
- `prTitle`: Tool-specific PR title, e.g. `feat(<connector>): add <tool_name> tool`. **Required for extension PRs** — without this, the in-app flow defaults to a generic "feat: add connector" title that doesn't reflect the extension scope.
- `prBody`: Tool-specific PR body using the Extension PR Template from Phase 6 below. **Required for extension PRs** — without this, the in-app flow uses a generic description.

**Checkpoints — call `rebel_mcp_report_contribution_state` at each:**

| When | Status | Notes |
|------|--------|-------|
| After Phase 4 (Implementation complete) | `draft` | New tool implemented and tests written |
| Start of Phase 5 (Local testing begins) | `testing` | Building and running in Rebel locally |
| After Phase 5 (Local testing passes) | `ready_to_submit` | Include `prTitle` and `prBody` for the extension PR |


## Process Overview

```
Phase 1: Eligibility Gate      → Verify the connector can be extended
Phase 2: Prepare Workspace     → Set up a local workspace for development (silent, no user questions)
Phase 3: Connector Research    → Understand existing patterns and where the new tool fits
Phase 4: Implementation        → Delegate coding to Software Engineer workflow
Phase 5: Run Locally in Rebel  → Configure Rebel to use the local build
Phase 6: Submit Extension      → In-app contribution or manual PR
```


## Phase 1: Eligibility Gate

Before any development, determine whether the connector can be extended through this flow.

### 1.1 Identify the Connector

Ask: "Which connector do you want to extend, and what tool do you want to add?"

Get:
- The **connector name** (e.g., "Zendesk", "Slack", "Google Workspace")
- The **tool being added** (e.g., "search macros", "list channels", "create calendar event")
- **Why the existing tools are insufficient** for the user's needs

### 1.2 Determine Connector Location

Check where the connector lives. There are three possible paths.

**The `bundled-` ID prefix is NOT a classifier.** Many connectors with `bundled-*` IDs are fully open-source (`provider: "rebel-oss"`, Path A), while others are truly internal (`provider: "bundled"`, Path B). The only signal that matters is the `provider` field from the live catalog.

---

#### Step 1 — Preferred: call the catalog tool

Call `rebel_mcp_get_connector` (by ID, stripping any `catalog:` prefix) or `rebel_mcp_search_connectors` (by name). Quote the `provider` field verbatim in your response (e.g., "Catalog says: `provider: "rebel-oss"`"). The quoted value is what decides the path.

Then assign the path:
- `provider: "rebel-oss"` → **Path A** (open-source, extendable)
- `provider: "bundled"` → **Path B** (truly bundled/internal, not extendable)
- Any other or missing `provider` → **Path C** (third-party)

**Do NOT** read `resources/connector-catalog.json` from disk — there may be stale copies on the filesystem. The MCP tools are the single source of truth when available.

---

#### Step 2 — Fallback: the bundled-* deterministic allowlist

Use this ONLY when the catalog tool is genuinely unavailable in your tool list (e.g., running in a planning-only phase that has no MCP tools). When the tool IS available, Step 1 takes precedence.

The following `bundled-*` IDs are `provider: "rebel-oss"` → **Path A (extendable)**. This list is validated against `resources/connector-catalog.json` by `scripts/check-extend-skill-bundled-allowlist.ts` — if it drifts, the validator fails.

<!-- BUNDLED_REBEL_OSS_ALLOWLIST_START -->
```yaml
# provider: "rebel-oss" connectors with bundled-* IDs (Path A — extendable)
bundled_rebel_oss_ids:
  - bundled-apple-shortcuts
  - bundled-browser-automation
  - bundled-custom-email
  - bundled-elevenlabs
  - bundled-elevenlabs-agents
  - bundled-fathom
  - bundled-freshdesk
  - bundled-gamma
  - bundled-google
  - bundled-google-analytics
  - bundled-hubspot
  - bundled-humaans
  - bundled-icloud-mail
  - bundled-kling
  - bundled-microsoft-calendar
  - bundled-microsoft-files
  - bundled-microsoft-mail
  - bundled-microsoft-sharepoint
  - bundled-microsoft-teams
  - bundled-mixmax
  - bundled-nano-banana
  - bundled-napkin
  - bundled-office
  - bundled-opus-video-clip
  - bundled-pandadoc
  - bundled-quickbooks
  - bundled-replit-ssh
  - bundled-retell-ai
  - bundled-runway
  - bundled-salesforce
  - bundled-servicenow
  - bundled-slack
  - bundled-talentlms
  - bundled-vanta
  - bundled-workday
  - bundled-yahoo-mail
```
<!-- BUNDLED_REBEL_OSS_ALLOWLIST_END -->

- If the ID is on this allowlist → **Path A**.
- If the ID starts with `bundled-` but is NOT on this allowlist → **Path B** (truly bundled, not extendable).
- If the ID does not start with `bundled-` and you cannot call the catalog tool → **refuse to classify**. Say:
  > "I can't safely determine whether this connector can be extended without checking the live catalog, and the catalog tool isn't available in this phase. Please ask again in a turn that can call `rebel_mcp_get_connector`."

---

#### Forbidden

- ❌ Any phrase like "Per the live catalog…", "The catalog shows…", or claim that `provider` is a specific value, without either a visible tool call in this turn OR the ID matching an entry in the Step 2 allowlist.
- ❌ Assigning Path B from a `bundled-` prefix alone when the ID is on the Step 2 allowlist (those are Path A).
- ❌ Falling through to Path C as a "safe" default for unknown `bundled-*` IDs. Unknown `bundled-*` → Path B (truly bundled), not Path C.

---

**Path A — Connector is in the `mcp-servers` repo** ✅ Proceed

The connector source is in [`mcp-servers`](https://github.com/mindstone-engineering/mcp-servers) under `connectors/<name>/`.

Verify by checking **either** of:
- The connector's `provider` field is `"rebel-oss"` (from `rebel_mcp_get_connector` response)
- The connector's `mcpConfig.args` references an `@mindstone-engineering/mcp-server-*` or `@mindstone-ai/mcp-server-*` npm package

If yes → **Proceed to Phase 2.**

---

**Path B — Connector is bundled/internal (not yet externalized)** ⛔ Block

> **⚠️ STOP — Before you route a connector here, confirm classification via Step 1 (catalog tool) or Step 2 (allowlist) above.** A `bundled-` ID prefix alone is NOT sufficient — 21 connectors with `bundled-*` IDs are actually `provider: "rebel-oss"` (Path A). Check the Step 2 allowlist before routing to Path B.

The connector is built into Rebel but hasn't been open-sourced to the `mcp-servers` repository yet. These connectors have `provider: "bundled"` in the catalog and do NOT have an `@mindstone-engineering/mcp-server-*` npm package.

Tell the user:
> "The **[connector name]** connector hasn't been open-sourced yet — it's currently bundled inside Rebel and can't be extended externally.
>
> If you'd like this connector to support [requested tool/capability], you can submit a feature request using the **Feedback & bugs** option in the Help menu (top-right corner). The Rebel team uses these requests to prioritise which connectors to improve and which to open-source next."

**Do NOT offer to build a companion MCP for bundled connectors** — bundled connectors (Google Calendar, Google Workspace, Slack, etc.) are core integrations that the Rebel team maintains. A companion MCP would create a confusing split experience. The right path is a feature request.

**Stop here — do not proceed to Phase 2.**

---

**Path C — Third-party connector (not in mcp-servers)** ⛔ Block

The connector was built by a third party — it's not in the `mcp-servers` repository.

Tell the user:
> "The **[connector name]** connector is a third-party package — it's not in the Rebel `mcp-servers` repository.
>
> **Options:**
> 1. **Fork their repo directly** — If the third-party connector is open-source, fork their repository and add your tool there. Follow their contribution guidelines.
> 2. **Build a companion MCP** — Create a separate MCP server that adds the tools you need. It runs alongside the existing connector. Use the [build-custom-mcp-server](../build-custom-mcp-server/SKILL.md) skill for this."

**Stop here — do not proceed to Phase 2.**

---

### 1.3 Proceed

Once Path A is confirmed, briefly tell the user what you'll do and proceed immediately — do not ask for confirmation:

> "The **[connector name]** connector can be extended. I'll add a `[tool_name]` tool to it — I'll set up the workspace, implement the tool following existing patterns, test it locally in Rebel, and get it ready to submit."

Then proceed directly to Phase 2. No confirmation question needed.


## Phase 2: Prepare Local Workspace

> **This phase is entirely silent — do not ask the user any questions.** The user does not need to know about git, cloning, or repositories. Handle all workspace setup automatically.

### 2.1 Find or Create Workspace

Use the Rebel-managed workspace at `~/mcp-servers/mcp-servers-repo/`. Do not use or modify any other directories the user may have.

**If the managed workspace already exists:**
- If the directory is clean (no uncommitted changes), sync to the latest upstream:
  ```bash
  cd ~/mcp-servers/mcp-servers-repo
  git fetch origin
  git checkout main
  git reset --hard origin/main
  ```
- If the directory has uncommitted changes from a previous session, remove it and re-clone:
  ```bash
  rm -rf ~/mcp-servers/mcp-servers-repo
  git clone --depth 1 https://github.com/mindstone-engineering/mcp-servers.git ~/mcp-servers/mcp-servers-repo
  ```

**If the managed workspace does not exist:**
- Shallow-clone the upstream repository:
  ```bash
  mkdir -p ~/mcp-servers
  git clone --depth 1 https://github.com/mindstone-engineering/mcp-servers.git ~/mcp-servers/mcp-servers-repo
  ```

### 2.2 Set Working Path

Set the working path to `<workspace>/connectors/<name>/` for all subsequent phases.

> **Important:** Do NOT fork on GitHub at this stage. GitHub forking is only needed at submission time (Phase 6) and is handled automatically by the in-app contribution flow. For the manual git fallback in Phase 6, create a feature branch locally:
> ```bash
> git checkout -b feat/<connector>-<tool-name>
> ```


## Phase 3: Connector Research

Before writing any code, thoroughly understand the connector's existing patterns. Every connector has its own conventions for error handling, response formatting, and tool registration.

### 3.1 Read Connector Documentation

Read these files in order:

1. **`connectors/<name>/README.md`** — What the connector does, setup instructions, tool reference
2. **`connectors/<name>/package.json`** — Dependencies, build scripts, version
3. **`connectors/<name>/src/server.ts`** — How the server is created and tools are registered
4. **`connectors/<name>/test/`** — Existing test files, especially smoke tests and any tool registration tests (e.g., `expectedTools` arrays, `listTools()` assertions). Understanding these is critical — they're where missing registration gets caught

### 3.2 Understand Tool Layout

Most connectors follow a pattern like:

```
connectors/<name>/src/
├── server.ts          # Creates McpServer, registers all tools
├── tools/
│   ├── index.ts       # Re-exports registration functions
│   ├── tickets.ts     # registerTicketTools(server)
│   ├── users.ts       # registerUserTools(server)
│   └── ...
├── client.ts          # API client wrapper
├── auth.ts            # Authentication/credential handling
├── types.ts           # Shared types and constants
├── formatters.ts      # Response formatting functions
└── utils.ts           # Shared utilities (error handling, etc.)
```

Identify:
- **Where tools are defined** — individual files in `src/tools/`? All in `server.ts`?
- **How tools are registered** — `register*Tools(server)` pattern? Direct `server.registerTool()` calls?
- **How the module structure works** — what imports what?

### 3.3 Study Existing Patterns

Read at least two existing tool implementations to understand:

| Pattern | What to look for |
|---------|-----------------|
| **Error handling** | Is there a shared `withErrorHandling()` wrapper? What error format is used? |
| **Authentication** | How are credentials accessed? `getAccount()`? `getAuthHeader()`? Direct env vars? |
| **API calls** | Is there a shared API client? `fetch()` wrapper? Vendor SDK? |
| **Response formatting** | How are API responses shaped for the MCP response? JSON? Markdown? Formatters? |
| **Input validation** | Are Zod schemas used? How are optional params handled? |
| **Tool annotations** | How are `readOnlyHint` and `destructiveHint` set? |
| **Naming convention** | What service prefix is used? (e.g., `zendesk_`, `slack_`) |

### 3.4 Identify Where the New Tool Fits

Determine:
- Which **existing tool file** the new tool belongs in (or whether to create a new file)
- Which **API endpoint** the tool will call
- What **existing utilities** can be reused (error handler, API client, formatters)
- Whether the tool needs any **new dependencies** or **new auth scopes**


## Phase 4: Implementation

> **MANDATORY — File locations:** All files related to this extension — source code, tests, planning docs, research notes, scratch working files, conversation-specific notes — MUST live under `~/mcp-servers/mcp-servers-repo/connectors/<name>/` (typically in `connectors/<name>/` for code and `connectors/<name>/docs/` for docs). Do NOT write any extension-related file to `Chief-of-Staff/`, Private Space, `memory/`, `Chief-of-Staff/temp/`, temp directories, or anywhere else in the user's workspace. Notes and research about the extension belong beside the source code so they ship with the contribution PR. If you need a scratch file, create it under `connectors/<name>/docs/` (e.g. `connectors/<name>/docs/notes.md`) — never in Private Space. **This overrides the general `Chief-of-Staff/temp/` rule for OSS MCP extension work.**

> **Mandatory workflow:** Implementation must be orchestrated via the [Software Engineer workflow](../../workflows/software-engineer/SKILL.md). Do not implement the extension inline from this skill. The Software Engineer workflow provides structured planning, staged implementation via subagents, and cross-family code review.

### 4.1 Prepare the Extension Brief

Assemble the following brief to hand off to the Software Engineer workflow:

**Project setup:**
- **Connector path:** `connectors/<name>/` in the local workspace (set up in Phase 2)
- **Working document location:** `connectors/<name>/docs/extension-plan.md` — this ships alongside the source code and is included in the contribution PR

**From Phase 3 (Connector Research):**
- **Requested tool:** Name, purpose, and why existing tools are insufficient
- **Existing patterns:** Where tools live, how they're registered, API client/auth/error-handling conventions, response formatting, naming prefix
- **Registration wiring path:** The exact files involved in tool registration (tool file → `tools/index.ts` export → `server.ts` import + `createServer()` call)
- **Existing test patterns:** Smoke tests, registration tests (`expectedTools` arrays), mock server setup, test helpers — the implementer must know these to write matching tests and update registration assertions
- **Files likely in scope:** Which files to create or modify
- **Reusable utilities:** Existing modules the new tool should use (error handler, API client, formatters)
- **Any new auth scopes or dependencies** required

**Required references** (the planner and implementer must read these):
- [mcp-development-standard.md](../build-custom-mcp-server/references/mcp-development-standard.md) — SDK patterns, naming conventions, error handling guidelines
- [mcp-testing-guide.md](../build-custom-mcp-server/references/mcp-testing-guide.md) — Test strategy and patterns
- [contribute-connector.md](../build-custom-mcp-server/references/contribute-connector.md) — OSS security review requirements

**Mandatory constraints:**
- Follow the connector's existing patterns — do not introduce new conventions
- Use the same service prefix as other tools in the connector (e.g., `zendesk_search_macros`, not `search_macros`)
- Set tool annotations correctly (`readOnlyHint`, `destructiveHint`) — any tool that spawns a subprocess, runs shell/AppleScript, or triggers a host-visible side effect **must** set `destructiveHint: true`
- All code in `mcp-servers` is open source — no internal references ("Mindstone", "Rebel") in code or error messages; use host-neutral error messages
- Validate any user-supplied hostnames before using them in URLs
- Never commit `dist/`, no personal absolute paths (`/Users/<name>/...`, `/home/<name>/...`) in README or error messages, and ensure `package.json` has a `"license"` field matching the connector's LICENSE
- Tests must import the real Zod schemas from `src/` — never redefine `z.object(...)` inline in test files, since parallel copies silently diverge
- Any `spawn()`/`exec()`/`execFile()` call must pass an explicit `timeout` option — a stalled child hangs every tool behind it
- When wrapping a CLI with flags, read the flag's documentation before passing data through it (e.g. `--input-path` / `--input-file` expects a filesystem path, not raw text — write to a temp file or use `stdin` instead)

**Definition of done:**
- [ ] Tool implemented following connector's existing patterns (Zod schema, handler, formatting)
- [ ] Tool registration wiring is complete — trace the connector's actual registration chain end-to-end and verify the new tool reaches `createServer()`. Most connectors use a 3-step pattern (missing any step silently breaks the tool):
  1. Tool file created in `src/tools/` with `register*Tools(server)` export
  2. Re-exported from `src/tools/index.ts`
  3. Imported **and called** in `src/server.ts` `createServer()` — the import alone is not enough, the `register*Tools(server)` call must be added to the function body
  
  Simpler connectors may register tools directly in `server.ts` — follow whatever pattern the connector already uses, but always verify the tool is actually callable, not just imported.
- [ ] Tests added matching existing test patterns (happy path, error handling, edge cases)
- [ ] Smoke/registration tests updated — add the new tool name to any `expectedTools` array or `listTools()` assertion in the connector's test suite. If no registration test exists, create one that verifies the new tool appears in `client.listTools()` output (see [mcp-testing-guide.md § Schema and tool registration tests](../build-custom-mcp-server/references/mcp-testing-guide.md))
- [ ] All existing tests still pass
- [ ] `npm run build && npm test` succeeds — run this and verify the output shows all tests passing (including the new tool's tests). Do not mark complete without actual pass evidence
- [ ] Ready for Phase 5 local Rebel testing

### 4.2 Delegate to Software Engineer Workflow

Invoke the [Software Engineer workflow](../../workflows/software-engineer/SKILL.md) with the brief above to perform the coding work.

The Software Engineer workflow will:
1. Create the working document at `connectors/<name>/docs/extension-plan.md`
2. Plan the implementation (reading the connector's patterns and MCP reference docs)
3. Implement through fresh-context subagents
4. Run cross-family code review (mandatory)
5. Validate (build, tests)

### 4.3 Resume This Skill

When the Software Engineer workflow completes, resume here and continue with:
- **Phase 5: Run Locally in Rebel**
- **Phase 6: Submit Extension**


## Phase 5: Run Locally in Rebel

Test the extension in Rebel before submitting a PR.

### 5.1 Build and Verify Registration

Build the connector and verify the new tool is actually registered before testing in Rebel:

```bash
cd <path-to-mcp-servers>/connectors/<name>
npm run build
npm test  # Must pass — confirms tool is registered and callable
```

> **Common pitfall:** If `npm run build` succeeds but `npm test` shows "Tool not found" errors, the registration call is missing from `createServer()` in `src/server.ts`. Check that you added both the import AND the `register*Tools(server)` call inside the function body. Adding only the import is a silent failure — the code compiles but the tool is never registered.

If `dist/` looks stale after source changes, delete and rebuild:
```bash
rm -rf dist && npm run build
```

### 5.2 Configure Rebel to Use Local Build

In Rebel's MCP configuration (`super-mcp-router.json` or via Settings → Connectors → Add Custom MCP), point to the local fork build:

```json
{
  "command": "node",
  "args": ["<path-to-mcp-servers>/connectors/<name>/dist/index.js"],
  "env": {
    "EXAMPLE_API_KEY": "your-api-key"
  }
}
```

Use the **same environment variables** the connector normally requires — check the connector's `.env.example` or README for the required variables.

### 5.3 Disconnect Published Version (Important!)

> ⚠️ **If the published version of this connector is already connected in Rebel, disconnect it before connecting the local build.** Having both connected simultaneously will cause duplicate tool packages in Super-MCP, leading to confusing behaviour and potential tool conflicts.

To disconnect the published version:
1. Go to Settings → Connectors
2. Find the existing connector entry (the one using `npx` or the catalog install)
3. Disconnect or remove it
4. Add the local build as a custom MCP (see 5.2 above)

### 5.4 Test in Rebel

1. Start a new conversation in Rebel.
2. Verify the new tool appears in the tool list (use `search_tools` or check the connector's tool package).
3. Call the new tool via `use_tool` with realistic inputs — not just one representative case. If you added more than one tool, iterate per tool. Use inputs a real user might pass (actual IDs, real queries, meaningful limits), and verify the response contains the fields the description promises — matching the schema isn't enough; the data has to be right.
4. Verify existing tools still work correctly.
5. Test error cases for the new tool (invalid inputs, missing data, empty results).

You will list every tool you tested, with inputs and results, in the `<testing_evidence>` block in Phase 6 before reporting `ready_to_submit`.

### 5.5 After PR is Merged

Once your PR is merged and the updated connector is published to npm:
1. Disconnect the local fork connector in Rebel
2. Reconnect via the catalog — the published version now includes your tool
3. Or update to the latest npx version manually


## Phase 6: Submit Extension

### Definition of Done — before you report `ready_to_submit`

Testing is your job before you tell Rebel the extension is ready. The user is trusting the new tool to work against their real data. Treat the checklist below as a gate, not a suggestion.

Every item must be true. If any aren't, go fix it and re-run the affected steps.

1. **Build passes** — `npm run build` succeeds with no errors.
2. **Tests pass** — `npm test` shows all tests passing, including the new tool's tests and the updated registration assertions.
3. **Connector running locally in Rebel** — local build configured per Phase 5.2, published version disconnected per Phase 5.3.
4. **Each new tool called via `use_tool` with realistic inputs** — iterate per tool if you added more than one (Phase 5.4). Not one representative call — every single new tool, happy path plus at least one error case.
5. **Each new tool returned the expected data** — no errors, and the response actually contains the fields the tool description promises.
6. **Existing tools still work** — a quick sanity check on an unrelated tool in the connector, to confirm your change didn't break anything.

#### Emit a `<testing_evidence>` block before reporting

Immediately before calling `rebel_mcp_report_contribution_state({status: "ready_to_submit", ...})`, emit a visible `<testing_evidence>` block in the conversation listing every new tool you tested, the input you used, what you expected, and what came back. One row per tool — no omissions. This is the proof that the checklist above is real, not aspirational.

Format:

```
<testing_evidence>
tool: zendesk_search_macros
  input: { query: "welcome", limit: 5 }
  expected: array of up to 5 macros matching "welcome"
  actual: [{ id: 101, title: "Welcome — new customer" }, ...] (3 items returned) — PASS

tool: zendesk_search_macros (error case)
  input: { query: "" }
  expected: structured error "query must be non-empty"
  actual: { ok: false, error: "query must be non-empty" } — PASS
</testing_evidence>
```

If a tool failed, fix it — do not paper over it in the block. If a tool genuinely cannot be exercised without side effects on the user's account (e.g., a destructive `delete_*` tool), say so explicitly in the `actual` field and note how you otherwise verified it (unit test, mocked API, etc.).

Only after this block is emitted do you call `rebel_mcp_report_contribution_state` with `status: "ready_to_submit"` and the `prTitle` + `prBody` described in the Primary Path below.

### Primary Path — In-App Contribution Flow

The recommended way to submit your extension is through the in-app "Add to the community" flow. This handles all GitHub operations automatically — no manual Git commands needed.

**How it works:**

1. Call `rebel_mcp_report_contribution_state` with status `ready_to_submit` (if not already reported)
2. Tell the user they can click **"Add to the community"** in the MCPBuildCard to submit their changes — this handles GitHub authentication, forking, pushing files, and opening a PR automatically via the contribution service
3. The in-app flow forks the `mcp-servers` repo (or reuses an existing fork), creates a branch, pushes the modified connector files via the Git Data API, and opens a PR with a structured description
4. CI runs automatically on the PR — builds and tests on Node.js 20 and 22
5. Status updates appear in the MCPBuildCard and notification surfaces

> The in-app flow uses the contribution IPC channels (`contribution:start-auth`, `contribution:submit`, `contribution:refresh-status`) to orchestrate the entire process. No manual Git commands needed.

---

### Fallback — Manual Git Workflow

If the in-app flow isn't available, or the user explicitly prefers manual control, delegate the PR mechanics to the [`submit-pr-to-rebel-oss`](../submit-pr-to-rebel-oss/SKILL.md) skill. That skill owns the generic fork / branch / atomic-commit (via the GitHub Git Data API) / push / PR-open flow; this skill stays responsible for the extension-specific context (PR template, file list, test registration checks).

> **STOP before invoking the PR skill — all of these must be true:**
> 1. **Phase 5 local testing has passed** — `npm run build` and `npm test` both green, the new tool was exercised end-to-end in Rebel, existing tools still work, the `<testing_evidence>` block has been emitted.
> 2. **`prTitle` and `prBody` are composed** using the [Extension PR Template](#extension-pr-template) below. A generic one-liner body is rejected.
> 3. **`files` is scoped strictly to the files you changed or added** — usually the new tool file, edits to `src/tools/index.ts`, edits to `src/server.ts`, updated test files (including the registration assertion test), and any README/`.env.example` changes. Do NOT include unrelated files in the connector directory that you didn't touch.
> 4. **No `dist/`, `node_modules/`, build artefacts, coverage output, or `.env` (with real credentials) in `files`.** The CI pipeline builds from source.

Pass the following parameters to the submit-pr-to-rebel-oss skill:

| Param | Value for an extension PR |
|-------|---------------------------|
| `repo` | `mindstone/mcp-servers` |
| `baseBranch` | `main` |
| `branchName` | `feat/<connector>-<tool-name>` (e.g. `feat/zendesk-search-macros`) |
| `commitMessage` | `feat(<connector>): add <tool_name> tool` |
| `prTitle` | `feat(<connector>): add <tool_name> tool` |
| `prBody` | The markdown you composed from the Extension PR Template below |
| `pathAllowlistPrefix` | `connectors/<connector>/` |
| `files` | Source→destination list of the files you touched (new tool file, `src/tools/index.ts`, `src/server.ts`, updated test files, README/`.env.example` if changed) |

Since the extension is edited directly in the local clone at `~/mcp-servers/mcp-servers-repo/`, the `source` and `destination` for each entry follow the same path — prefix `~/mcp-servers/mcp-servers-repo/` for source, bare path for destination. For example:

```json
[
  { "source": "~/mcp-servers/mcp-servers-repo/connectors/zendesk/src/tools/macros.ts",
    "destination": "connectors/zendesk/src/tools/macros.ts" },
  { "source": "~/mcp-servers/mcp-servers-repo/connectors/zendesk/src/tools/index.ts",
    "destination": "connectors/zendesk/src/tools/index.ts" },
  { "source": "~/mcp-servers/mcp-servers-repo/connectors/zendesk/src/server.ts",
    "destination": "connectors/zendesk/src/server.ts" },
  { "source": "~/mcp-servers/mcp-servers-repo/connectors/zendesk/test/macros.test.ts",
    "destination": "connectors/zendesk/test/macros.test.ts" },
  { "source": "~/mcp-servers/mcp-servers-repo/connectors/zendesk/test/registration.test.ts",
    "destination": "connectors/zendesk/test/registration.test.ts" }
]
```

When the submit-pr-to-rebel-oss skill returns, report the PR number and URL to the user. CI will run automatically on the PR — the `ci.yml` workflow builds the connector and runs tests on Node.js 20 and 22, and must pass before review. Responding to CI failures is out of scope for this skill.

---

## Extension PR Template

Use this template for your PR description. It's different from the new-connector PR template — it focuses on what's being added to an existing connector, not building from scratch. The goal is to give the Mindstone engineering team enough context to make a confident merge decision in a 30-second scan — surgical, not bloated.

**Anti-patterns to avoid:**
- AI marketing speak ("robust, comprehensive extension...")
- Exhaustive implementation narratives or model rosters
- Repeating the full tool schema in the PR body (that's in the code)
- "All tests pass" with no indication of what was actually run

````markdown
## Summary

Adds `<tool_name>` tool to the **<connector>** connector.
<What the user needed this tool for — 1-2 sentences in plain language from the user's own words where possible.>

## Tool Surface

- **Tool:** `<service_tool_name>` — <brief description>
- **API endpoint:** `<HTTP method> <endpoint path>`
- **Annotations:** `readOnlyHint=<true|false>`, `destructiveHint=<true|false>`
- **Pattern followed:** <which existing tool was used as reference — e.g., "Same pattern as `zendesk_search_tickets`">

## Validation

- **Build & tests:** `npm run build && npm test` ✅ / ⚠️ <details if failing>
- **Existing tests:** Still passing ✅ / Broken ⚠️
- **Integration tested in Rebel:** ✅ Tested tool end-to-end / ❌ Not tested
- **Security review:** ✅ Pass / ⚠️ <issues> / ❌ Not performed

## Reviewer Notes

- **Known limitations:** <or "None">
- **Extension plan:** `docs/extension-plan.md` — full research, implementation stages, and review history

## Build Context

- **Workflow:** Software Engineer → <N> stage(s)
- **Model:** <e.g., claude-opus-4-7>
- **Code review:** <N> review(s) by <model(s)> — <key outcome, e.g., "1 finding addressed">

Submitted via Rebel's in-app contribution flow.
````

The description answers four questions a reviewer needs: **Is it useful?** (Summary), **What's the scope/risk?** (Tool Surface), **Does it work?** (Validation), and **Is it safe?** (Reviewer Notes + Validation security line). The Build Context footer gives provenance without dominating the description.


## Edge Cases

### Extending a connector you don't have installed

You don't need to have the connector installed in Rebel to extend it. Phase 2 sets up the workspace automatically. When you're ready to test in Rebel, configure it as a custom MCP (Phase 5) — you'll need the service's API credentials for the environment variables.

### Connector is bundled but not yet externalized

Some connectors are built into Rebel but haven't been open-sourced to the `mcp-servers` repo yet. These have `provider: "bundled"` in the catalog and can't be extended through this flow. Use `rebel_mcp_get_connector` to check. See Phase 1, Path B for options. **Note:** Many connectors have IDs starting with `bundled-` but are actually open-source (`provider: "rebel-oss"`) — always check the `provider` field, not the ID prefix.

### Published version already connected in Rebel

If you already have the published (npm/catalog) version of the connector connected in Rebel, you **must disconnect it** before connecting your local fork build. Running both simultaneously causes duplicate tool registrations in Super-MCP — the same tool names appear twice, and Rebel may route calls to the wrong version. See Phase 5, step 5.3 for instructions.

### Upstream repo changes during your PR

The `mcp-servers` repo may receive other changes while your PR is open. If your PR has merge conflicts or is based on an old commit:

```bash
git fetch upstream
git rebase upstream/main
# Resolve any conflicts
npm run build && npm test  # Verify everything still works
git push --force-with-lease origin feat/<connector>-<tool-name>
```

Check the PR's CI status after rebasing — new upstream changes may affect your code.

### New tool needs auth or setup metadata changes

If your new tool requires additional authentication scopes, new environment variables, or changes to the connector's setup metadata:

1. **Update `.env.example`** — add new required variables with descriptions
2. **Update `README.md`** — document new setup requirements
3. **Update `catalog-entry.json`** (if it exists) — add new `setupFields` entries for any new credentials
4. **Note in the PR description** — clearly flag that this extension requires setup changes so the maintainer and users are aware

These metadata changes are particularly important for catalog-installed users who will need to update their configuration after the new version is published.


## [IMPORTANT]

- **Always follow the connector's existing patterns** — don't introduce new conventions, error handling styles, or response formats. Consistency within a connector is more important than your personal preferences.
- **Don't modify tools you're not extending** — keep your changes scoped to the new tool and its registration. If you find bugs in existing tools, file a separate issue or PR.
- **Disconnect the published version before testing locally** — duplicate tool registrations will cause confusing behaviour.
- **All existing tests must still pass** — your extension must not break anything that already works.
- **Use the connector's service prefix for tool names** — if existing tools use `zendesk_`, your tool must too.
- **Get user approval on tool design before implementing** — confirm the tool name, parameters, and behaviour match what the user needs.
