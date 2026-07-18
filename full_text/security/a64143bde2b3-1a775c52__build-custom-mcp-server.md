---
name: build-custom-mcp-server
description: "Helps users connect and use a service in Rebel when it isn't already in the built-in connector catalog. Acts as an expert advisor — runs the full build-vs-buy check (catalog, MCP Registry, community) before scaffolding a custom MCP server and guiding research, implementation, security review, and contribution."
use_cases:
  - "Build a connector for [service name]"
  - "Build me a connector"
  - "I want to add a new connector"
  - "Connect my company's internal API to Rebel"
  - "Build an MCP for our CRM/ERP/ticketing system"
  - "Create tools so Rebel can access our database"
  - "Make a connector for a public API"
  - "Build an integration for any external service"
  - "Create a custom connector from scratch"
  - "I need Rebel to talk to [service]"
  - "[Service] isn't in the connector catalog"
  - "There's no connector for [service]"
  - "I want to use [service] in Rebel"
  - "I want [service] in Rebel"
  - "How do I get [service] working in Rebel?"
  - "Can I get [service] working in Rebel?"
  - "How do I use [service] in Rebel?"
  - "Is there a Rebel connector for [service]?"
last_updated: 2026-04-23
tools_required: []
agent_type: main_agent
license: LICENSE.txt
---
# Create MCP Server

Guide users through creating a custom MCP server to connect their API to Rebel.

**Default: TypeScript/Node.js** using the bundled starter template. Python reference available in `references/python_mcp_server.md` if requested.

## Voice Firewall — How to Talk to Non-Technical Users

The user is non-technical. They are creating a tool with Rebel, not coding, shipping packages, or managing open-source plumbing. Keep chat copy plain, calm, and about what the tool lets them do.

**Forbidden vocabulary in chat:** `PR`, `pull request`, `fork`, `branch`, `repo`, `repository`, `npm`, `MCP`, `MCP server`, `connector` (prefer `tool`), `Phase N`, `ready_to_submit`, `testing_evidence`, `Definition of Done`, `DoD`, `CI`, `automated checks` (prefer "checks"), `package`, `OpenAPI`, `Swagger`, `Postman`, `curl`, `endpoint`, `payload`, `HTTP`, `API` (prefer "their service" or the specific verb).

**Allowed exceptions:**

- `GitHub` is OK only when the user has explicitly chosen the GitHub-attributed path, such as the attribution sub-card.
- `API key` and `access key` are OK on credential collection cards because the user is being asked to fetch one.

**Pronouns:**

- Default to "we" during build and testing.
- Use "you" for ownership and decisions: attribution, sharing, keeping private, withdrawing.

**Action-oriented rule:** never ask the user for technical input or permission for technical actions. Do not say "Adding a connector is a protected admin action — may I proceed?" Skill invocation is consent for this flow.

**Translate internal action codes before speaking:**

| Internal action code | Chat-safe phrasing |
| --- | --- |
| `run_tests` | `I need to try it properly before sharing.` |
| `register_server` | `I need to connect it to Rebel first.` |
| `move_to_canonical_path` | `I need to move the files into the right folder before sharing.` |
| `reauth_github` | `Please reconnect GitHub in Settings → Connectors so we can send it out.` |
| `run_software_engineer_workflow` | `Let me think this through properly before I share it.` |
| `missing_evidence` | `I got ahead of myself. Trying it properly now.` |

**Reference docs** (load as needed):

- [mcp_best_practices.md](references/mcp_best_practices.md) - Universal MCP design guidelines
- [node_mcp_server.md](references/node_mcp_server.md) - TypeScript implementation patterns
- [python_mcp_server.md](references/python_mcp_server.md) - Python/FastMCP patterns
- [evaluation.md](references/evaluation.md) - Creating evaluation harnesses
- [mcp-development-standard.md](references/mcp-development-standard.md) - SDK patterns, naming conventions, error handling, module architecture, security baseline, packaging
- [mcp-testing-guide.md](references/mcp-testing-guide.md) - Test strategy, test patterns, debugging common failures
- [contribute-connector.md](references/contribute-connector.md) - Contributing your MCP back to the ecosystem (lifecycle, PR template, quality bar, CI pipeline)

## Key Principles

1. **User's existing codebase is READ-ONLY** - analyze to understand API, never modify
2. **MCP project is created separately** - at `~/mcp-servers/<api-name>-mcp/`
3. **Rebel creates files for the user** - don't just provide snippets to copy
4. **Start small** - 3-5 tools for first iteration (though more tools are fine—Rebel's Super-MCP uses progressive discovery so tool count isn't a hard constraint)
5. **Use subagents for research** - delegate API doc discovery to researcher

## Agent-Centric Design Principles

Before implementation, understand how to design tools for AI agents:

**Build for Workflows, Not Just API Endpoints:**

- Don't simply wrap existing API endpoints - build thoughtful workflow tools
- Consolidate related operations (e.g., `schedule_event` that checks availability AND creates event)
- Focus on tools that enable complete tasks, not just individual API calls

**Optimize for Limited Context:**

- Agents have constrained context windows - make every token count
- Return high-signal information, not exhaustive data dumps
- Provide "concise" vs "detailed" response format options
- Default to human-readable identifiers over technical codes (names over IDs)

**Design Actionable Error Messages:**

- Error messages should guide agents toward correct usage
- Suggest specific next steps: "Try using filter='active_only' to reduce results"
- Help agents learn proper tool usage through clear feedback

**Use Evaluation-Driven Development:**

- Create realistic evaluation scenarios early (see [evaluation.md](references/evaluation.md))
- Let agent feedback drive tool improvements
- Prototype quickly and iterate based on actual agent performance

## Contribution Lifecycle

// internal — do not narrate to user

> **MANDATORY — You MUST call `rebel_mcp_report_contribution_state` after building the connector.** This is not optional. The moment you finish writing the connector code (all source files created, build succeeds), call this tool with `status: "draft"`. This triggers the MCPBuildCard UI that lets the user share their connector with the community. Without this call, the build card never appears and the contribution flow is broken.

Always report build progress using the `rebel_mcp_report_contribution_state` bundled tool. This tracks the build in the conversation UI (MCPBuildCard) and offers the user a one-click "Submit to community" option when ready. Call it regardless of whether the user intends to share — it powers local UI, not submission.

If `rebel_mcp_report_contribution_state` is not listed in your available tools, or `session_id` is missing from your `<dynamic_env>` context, skip all state reporting silently.

**Required parameters for every call:**

- `sessionId`: Use the `session_id` value from your `<dynamic_env>` context (must match exactly)
- `connectorName`: The connector name (e.g. `typeform-mcp`)
- `status`: The checkpoint status (see table below)
- `localServerPath` (**required at `draft` and `ready_to_submit` checkpoints**): The full path to the built connector directory (e.g. `~/mcp-servers/typeform-mcp`). Tilde-prefixed paths are expanded automatically. The same path you wrote to disk is fine — case and trailing slash don't matter.

**PR metadata parameters** (set at `ready_to_submit` checkpoint):
- `prTitle`: Connector-specific PR title, e.g. `feat: add <api-name> connector`. **Required** — without this, the in-app flow defaults to a generic title.
- `prBody`: Rich PR description using the PR Description Template from [contribute-connector.md](references/contribute-connector.md#pr-description-template). **Required** — without this, the in-app flow uses a generic one-liner that gives reviewers no context. See the `ready_to_submit` checkpoint in Phase 6 for the full template and instructions.

**State machine:**

```
draft → testing → ready_to_submit → submitted → ci_pass/ci_fail
                                               → changes_requested → (re-submit)
                                               → approved → published
                                               → rejected
```

**Checkpoints — call `rebel_mcp_report_contribution_state` at each (if tool available):**


| When                                    | Status                           | Call tool?                             |
| --------------------------------------- | -------------------------------- | -------------------------------------- |
| After Phase 4 (Implementation complete) | `draft`                          | Yes                                    |
| Start of Phase 6 (Testing begins)       | `testing`                        | Yes                                    |
| After Phase 6 (Tests pass)              | `ready_to_submit`                | Yes — include `prTitle` and `prBody`   |
| User clicks "Submit" in MCPBuildCard    | `submitted`                      | Handled by in-app contribution service |
| CI result arrives                       | `ci_pass` / `ci_fail`            | Handled by contributionStatusService   |
| Maintainer reviews                      | `approved` / `changes_requested` | Handled by contributionStatusService   |
| npm publish completes                   | `published`                      | Handled by catalog sync workflow       |


## Process Overview

// internal — do not narrate to user

```
Phase 0: Build-vs-Buy Gate  → Classify intent (add/build/extend), 3-tier check for build, confirm
Phase 1: Discovery          → Understand API, use cases, auth method
Phase 2: Research           → Find/analyze API documentation
Phase 3: Planning           → Design tools, get user approval
Phase 4: Implementation     → Delegate coding to Software Engineer workflow
Phase 5: Security           → Credential scan, npm audit, security review
Phase 6: Testing            → Build, configure Rebel, test interactively
Phase 7: Quality Review     → Final quality checklist (post-ready_to_submit)
Phase 8: Submit to Community → Guide user to click "Add to the community" in the MCPBuildCard
```

## Phase 0: Build-vs-Buy Gate

Before building anything, determine what the user wants to do and systematically check whether a suitable MCP server already exists. Building a custom MCP is a significant investment — an existing connector that covers 80% of the user's needs is almost always the better choice.

### 0.0 Seeded Conversation Fast-Path

If this conversation was started via the in-app "Set up a connector" button (the `rebel_mcp_report_contribution_state` tool is available, or the opening message matches the seeded pattern like "I want to build a new connector"), the user has already decided to build. Skip intent classification and the multi-tier build-vs-buy check.

**If a service name was provided in the seeded message** (e.g., "I want to build a new connector for Zendesk"):

- Use that as the service name and proceed directly to the build-vs-buy check at **0.2 Tier 1** (still check the catalog — the user may not know a connector already exists).

**If no service name was provided** (e.g., "I want to build a new connector"):

- Ask a single, simple free-text question — **no multiple-choice options, no categories, no structured cards**:

> **What would you like to connect to Rebel?**
>
> Just type the name of the service. If you have a link to anything useful, send that too.

- **Do NOT** present options like "Public service", "Internal API", etc. The user just needs to type a name. You will determine whether the API is public or internal later from context (see 0.7).
- Wait for the user's response, then proceed to **0.2 Tier 1** with the service name they provided.

**Do not** ask about intent (add/build/extend), present numbered options, or run the full 0.0 classification for seeded conversations.

---

### 0.0 Determine Intent: Add, Build, or Extend

> **Skip this section for seeded conversations** — see 0.0 Seeded Conversation Fast-Path above.

First, classify the user's intent into one of three categories. Route immediately when intent is clear — do not run the 3-tier check for add-intent requests.

**ADD intent** — the user wants to connect an existing service, not write code:

- Signals: "set up [service]", "add [service]", "configure [service]", "link [service]" — explicit setup/add verbs
- Combined with a **well-known public SaaS** (Slack, Notion, Gmail, Typeform, HubSpot, etc.)
- → **Redirect to [mcp-add-update-remove-connector](../../system/mcp-add-update-remove-connector/SKILL.md) immediately.** That skill searches the catalog and handles setup. **Stop here — do not proceed with this skill.**

**BUILD intent** — the user explicitly wants to create a new MCP server:

- Signals: "build", "create an MCP", "make a connector", "write a server", "build an MCP for", "connect my API" (internal/private API)
- → Proceed to the 3-tier build-vs-buy check below (0.1 onwards).

**Ambiguous intent** — could be either add or build:

- Examples: "I want Typeform in Rebel" (could be add or build), "connect our CRM" (could be internal API or existing connector)
- → Ask one clarifying question: "Should I look for an existing [service] tool first, or make one for you?"
- Route based on the answer.

---

**EXTEND intent** — the user wants to add a tool to an existing connector:

---

**If the user wants to ADD A TOOL to an existing connector** (e.g., "I want to add search macros to the Zendesk connector", "Add a list channels tool to the Slack MCP", "Extend the Google Workspace connector"):

Determine where the connector lives and route accordingly:

**a) Connector is in the `mcp-servers` repo** — The connector's source code is in the open-source `[mcp-servers](https://github.com/mindstone/mcp-servers)` repository under `connectors/<name>/`.

→ **Redirect to the [extend-mcp-server](../extend-mcp-server/SKILL.md) skill.** It handles the full extension flow: eligibility check, fork/clone, connector research, implementation, local testing, and PR submission. **Stop here — do not proceed with this skill.**

**b) Connector is bundled/internal (not yet externalized)** — The connector is built into Rebel but hasn't been open-sourced to the `mcp-servers` repository.

→ Tell the user:

> "The **[tool name]** isn't available to change directly yet. I can make a companion [service] tool that runs alongside it and fills in the gaps."

If the user agrees, proceed with this skill (0.1 onwards) to build the companion MCP.

**c) Third-party connector** — The connector was built by a third party and is not in the `mcp-servers` repository.

→ Tell the user:

> "The **[tool name]** was made by someone else. If it's public, a developer could suggest changes to them directly, or I can make a companion [service] tool that runs alongside it."

If the user wants to build a companion MCP, proceed with this skill (0.1 onwards).

---

### Build-vs-Buy Check (for "build new" intent)

The following 3-tier check applies when the user wants to **build a new connector**. If the user is extending an existing connector, they've already been redirected above.

> **Invariants — never skip these:**
>
> 1. **Never skip Tier 1.** Always check the Rebel connector catalog first, even if the user is confident nothing exists.
> 2. **Always present findings.** Show the user what was found at each tier before moving on.
> 3. **Explicit confirmation required.** The user must explicitly confirm they want to build before proceeding to Phase 1.
> 4. **Tool failures are not zero results.** If a tier's lookup fails (WebSearch `isError`, DNS failure, HTTP error) rather than returning empty results, mark that tier `SEARCH_FAILED` internally — do not summarise it as "nothing found". Retry once with a variant query; if still failing, explain in the Phase 0 summary that this check could not be completed and require explicit user confirmation to proceed despite incomplete evidence.

### 0.1 Identify the Service

> **Skip this if the service name is already known** (from a seeded conversation or the user's opening message).

Ask a single free-text question — **no multiple-choice options, no categories**:

> "What service do you want to connect to Rebel? Just type the name (e.g., 'Zendesk', 'Stripe', 'our internal CRM')."

Do NOT ask whether the API is public, internal, SaaS, etc. — you determine that from context later (see 0.7). The user just needs to provide a name.

---

### 0.2 Tier 1 — Rebel Connector Catalog

**Search Rebel's built-in connector catalog** using the `rebel_mcp_search_connectors` tool:

```
rebel_mcp_search_connectors(query: "<service name>")
```

Also try variations — abbreviations, parent company names, alternative product names (e.g., search "Google" if user says "Gmail", search "Microsoft" if user says "Outlook").

**If a matching connector is found:**

Present the result to the user:

> "Rebel already has a **[service]** tool that supports [brief capability summary]. You can set it up in Settings — no need to make a new one."

→ **Off-ramp:** Redirect to the [mcp-add-update-remove-connector](../../system/mcp-add-update-remove-connector/SKILL.md) skill to guide setup. **Stop here — do not proceed to Tier 2.**

**If no match is found:**

Tell the user:

> "Rebel doesn't already have a [service] tool. I'll check whether someone else has made one."

→ Proceed to Tier 2.

---

### 0.3 Tier 2 — Official MCP Registry

**Search the official MCP Registry** at `registry.modelcontextprotocol.io` for existing community MCP servers:

```
Use web search: site:registry.modelcontextprotocol.io "<service name>"
```

Also search directly: `https://registry.modelcontextprotocol.io` with the service name.

**Evaluate any results found:**

- Does the server cover the user's main use cases?
- Is it actively maintained (recent commits, responsive issues)?
- Does it have reasonable documentation?
- Is it from a reputable source (official vendor, known org, established developer)?

**If a suitable MCP server is found:**

Present the finding to the user with a brief assessment:

> "I found **[tool name]** that may already do this. It [brief capability summary]. It was made by [author] and was last updated [date]."
>
> "I'll check it's safe before adding it. You can skip that check if you prefer."

→ **Off-ramp:** If the user agrees, redirect to the [mcp-add-update-remove-connector](../../system/mcp-add-update-remove-connector/SKILL.md) skill. **Default to running the [community MCP security review](../../system/mcp-add-update-remove-connector/references/community-mcp-security-review.md) process** — only skip if the user explicitly opts out. When handing off to the ADD skill, note: "This MCP was found via the MCP Registry — run the security review by default." **Stop here — do not proceed to Tier 3.**

**If nothing suitable is found:**

Tell the user:

> "Nothing suitable there either. I'll do one broader search."

→ Proceed to Tier 3.

---

### 0.4 Tier 3 — Web Search Fallback

**Search npm and GitHub** for community MCP servers:

```
Web search: "<service name> mcp server" npm OR github
Web search: "@modelcontextprotocol <service name>"
```

Look for:

- npm packages with "mcp" and the service name
- GitHub repositories implementing MCP servers for the service
- Blog posts or tutorials about connecting the service via MCP

**Evaluate any results found** using the same criteria as Tier 2 (use cases, maintenance, documentation, reputation).

**If a promising MCP server is found:**

Present the finding to the user:

> "I found **[tool name]** that may already do this. It [brief capability summary]. [Quality assessment — maintenance status, stars, last update]."
>
> "I'll check it's safe before adding it. You can skip that check if you prefer."

→ **Off-ramp:** If the user agrees, redirect to the [mcp-add-update-remove-connector](../../system/mcp-add-update-remove-connector/SKILL.md) skill. **Default to running the [community MCP security review](../../system/mcp-add-update-remove-connector/references/community-mcp-security-review.md) process** — only skip if the user explicitly opts out. When handing off to the ADD skill, note: "This MCP was found via web search — run the security review by default." **Stop here.**

**If nothing suitable exists at any tier:**

Tell the user:

> "I've checked Rebel's built-in options and looked around. There doesn't seem to be an existing [service] tool that fits your needs. Making one is the right approach."

→ Proceed to the confirmation gate (0.5).

---

### 0.5 Confirmation Gate

**The user must explicitly confirm they want to build** before proceeding to Phase 1.

Present a summary of what was checked:

> **Build-vs-buy summary for [service]:**
>
> - ❌ Rebel: No built-in tool found
> - ❌ Existing-tool search: [No results / Results found but didn't fit because X / ⚠️ couldn't check]
> - ❌ Wider web search: [No results / Results found but didn't fit because X / ⚠️ couldn't check]
>
> "Ready to make your [service] tool? You don't need to know how the wiring works — that's my job."

If any tier is marked `SEARCH_FAILED` internally, explicitly flag that the search is **incomplete** and ask the user whether to (a) wait and retry, or (b) proceed knowing an existing tool may exist but wasn't verifiable. Do not proceed silently.

**Do not proceed to Phase 1 until the user confirms.**

If the user hesitates or wants to reconsider, remind them they can revisit any tier result and add an existing MCP instead.

---

### 0.6 Check Node.js Installation

Once the user has confirmed they want to build:

Run: `node --version`

- If missing or < v18, guide user to install Node.js LTS from [https://nodejs.org](https://nodejs.org)
- Explain this is needed to run the MCP server locally

### 0.7 Determine API Type

Determine from context whether the API is public or internal. Well-known services (Typeform, Stripe, GitHub, etc.) are public. "Our API", "internal CRM", "behind VPN" indicate private.

- **External/Public**: Load [flow-external-api.md](references/flow-external-api.md)
- **Internal/Private**: Load [flow-internal-api.md](references/flow-internal-api.md)

Only ask the user if the API type is genuinely unclear.

## Phase 1: Discovery

Gather essential information from user:

### 1.1 Use Cases

Ask: "What should Rebel be able to do with [service]? Give me a few real examples."

- Get 3-5 specific examples (e.g., "search for customers", "create tickets", "check order status")
- These will become your MCP tools

### 1.2 API Documentation

For **public APIs**: Research the API documentation using web search and subagents. Look for official docs, OpenAPI/Swagger specs, or developer portals.

For **internal/private APIs**: Ask the user: "How can I learn about this API?" (URL, spec file, or verbal description).

### 1.3 Authentication Method

Determine the authentication method from API documentation during Phase 2 research. Do not ask the user about auth at this stage — discover it from the docs. Common patterns:

- **None / Public API** - no credentials required
- **API Key** (most common) - passed in header or query param
- **Bearer Token** - from existing auth system
- **OAuth 2.0** - requires user login flow
- **Custom headers** - X-API-Key, session tokens, etc.

Credential values are collected later in Phase 6.2 — not during discovery.

### 1.4 Project Location

**MUST use `~/mcp-servers/<api-name>-mcp/`** — this is the standard location for user-built MCP servers. Do not ask the user where to create it. Do not use any other path (not `Chief-of-Staff/`, not relative `mcp-servers/`, not temp directories). The auto-detect hook requires this exact location to show the MCPBuildCard contribution UI.

## Phase 2: Research

**For external APIs**: Use researcher subagent to find documentation.
**For internal APIs**: Work from user-provided docs/descriptions.

See the relevant flow file for detailed instructions:

- [flow-external-api.md](references/flow-external-api.md)
- [flow-internal-api.md](references/flow-internal-api.md)

### Research Output

Synthesize findings into a working brief. In chat, keep it plain and explain what Rebel can do with the service; keep technical details in the working notes for the implementation handoff:

- Base URL and available endpoints
- Authentication requirements
- Rate limits (if any)
- Response formats
- Key data models

## Phase 3: Planning

### 3.1 Propose Tools

Based on use cases and research, propose 3-5 tools:


| Tool Name          | User Task          | What Rebel needs | What Rebel gives back |
| ------------------ | ------------------ | ---------------- | --------------------- |
| `search_customers` | Find customers     | query, limit     | List of matches       |
| `get_order`        | Check order status | order_id         | Order details         |
| ...                | ...                | ...              | ...                   |


### 3.2 Get User Approval

Present the tool list and ask:

- "Does this cover the work you want Rebel to do? Anything missing?"

**Do not proceed until user approves the tool list.**

### 3.3 Reference Implementation Patterns

For tool design best practices, load:

- [mcp_best_practices.md](references/mcp_best_practices.md) - Universal guidelines
- [node_mcp_server.md](references/node_mcp_server.md) - TypeScript patterns

## Phase 4: Implementation

> **MANDATORY — Project path:** All files related to this build — source code, tests, planning docs, research notes, scratch working files, conversation-specific notes — MUST live under `~/mcp-servers/<api-name>-mcp/` (typically `src/` for code, `docs/` for docs). Phase 4.2 below creates this directory and scaffolds the starter template — do not skip it. Do NOT write any build-related file to `Chief-of-Staff/`, Private Space, `memory/`, `Chief-of-Staff/temp/`, temp directories, or relative `mcp-servers/` paths. Notes and research about the build belong beside the source code so they ship with any contribution PR. If you need a scratch file, create it under `~/mcp-servers/<api-name>-mcp/docs/` — never in Private Space. **This overrides the general `Chief-of-Staff/temp/` rule for OSS MCP build work.**

> **Mandatory workflow:** Implementation must be orchestrated via the [Software Engineer workflow](rebel-system/skills/workflows/software-engineer/SKILL.md). Do not implement the MCP inline from this skill. The Software Engineer workflow provides structured planning, staged implementation via subagents, and cross-family code review — ensuring higher quality output regardless of project complexity.

### 4.1 Prepare the Implementation Brief

Assemble the following brief to hand off to the Software Engineer workflow:

**Project setup:**

- **Project path:** `~/mcp-servers/<api-name>-mcp/`
- **Working document location:** `~/mcp-servers/<api-name>-mcp/docs/build-plan.md` — this ships alongside the source code and is included in any contribution PR
- **Starter template:** Use the [starter template](references/starter-template/) as the project base

**From earlier phases:**

- **Approved tool list:** The user-approved tool table from Phase 3 (names, inputs, outputs)
- **Research summary:** Base URL, auth method, endpoints, rate limits, response formats, key data models from Phase 2

**Required references** (the planner and implementer must read these):

- [mcp-development-standard.md](references/mcp-development-standard.md) — SDK patterns (`McpServer` + `registerTool()` + Zod), naming conventions, error handling, module architecture, tool annotations, security baseline, packaging
- [mcp-testing-guide.md](references/mcp-testing-guide.md) — Test strategy, test patterns, debugging common failures
- [node_mcp_server.md](references/node_mcp_server.md) — TypeScript implementation patterns
- [mcp_best_practices.md](references/mcp_best_practices.md) — Universal MCP design guidelines

**Mandatory constraints:**

- Use `McpServer` + `registerTool()` + Zod schemas (not legacy `server.tool()`)
- `snake_case` for all tool names and top-level parameter names
- Base URL must be fixed (constant) or from env var — **never accept URL from tool input** (SSRF prevention)
- Use env vars for credentials; never hardcode secrets
- `.env` file for credentials with `.gitignore` excluding `.env`
- Set tool annotations correctly (`readOnlyHint`, `destructiveHint`)
- Format responses for agent consumption with bounded output size
- Use `URL` and `URLSearchParams` for building query strings
- Input validation via Zod schemas on all tools

**Definition of done:**

- Project structure created from starter template
- All approved tools implemented with Zod schemas and clear descriptions
- Authentication configured per the research findings
- Tests added (happy path, error handling, edge cases)
- `npm run build` succeeds without errors
- Ready for Phase 5 security validation

### 4.2 Scaffold the Project Directory (MANDATORY — do this BEFORE delegating)

You MUST create the project directory and scaffold it from the starter template BEFORE delegating to the Software Engineer workflow. This ensures the directory exists at `~/mcp-servers/<api-name>-mcp/` so all subsequent file writes target the correct location.

Run these commands now:

```bash
mkdir -p ~/mcp-servers/<api-name>-mcp/src ~/mcp-servers/<api-name>-mcp/docs
```

Then **read each starter template file** and **write its contents** to the project directory. Do not guess or approximate the content — read the actual files from the starter template:

1. Read `references/starter-template/package.json` → Write to `~/mcp-servers/<api-name>-mcp/package.json`. **Change the `name` field to `@mindstone/mcp-server-<api-name>`** (e.g. `@mindstone/mcp-server-apple-shortcuts`) — this is the public scoped name the package will be published under. Also update the `description` field to describe what the connector does. Using the scoped `@mindstone/mcp-server-<api-name>` prefix from the start means the PR reviewer sees the final published name, the catalog entry matches the `npx` specifier byte-for-byte, and the maintainer's publish workflow doesn't have to rename anything.
2. Read `references/starter-template/tsconfig.json` → Write verbatim to `~/mcp-servers/<api-name>-mcp/tsconfig.json`
3. Read `references/starter-template/.gitignore` → Write verbatim to `~/mcp-servers/<api-name>-mcp/.gitignore`
4. Read `references/starter-template/.env.example` → Write verbatim to `~/mcp-servers/<api-name>-mcp/.env.example`
5. Read `references/starter-template/src/index.ts` → Write to `~/mcp-servers/<api-name>-mcp/src/index.ts`. Replace the `PLACEHOLDER-mcp` server handshake name with `<api-name>-mcp` (e.g. `apple-shortcuts-mcp`) so protocol logs match the package slug.
6. Read `references/starter-template/src/logger.ts` → Write verbatim to `~/mcp-servers/<api-name>-mcp/src/logger.ts`
7. Read `references/starter-template/LICENSE` → Write verbatim to `~/mcp-servers/<api-name>-mcp/LICENSE`. The default is FSL-1.1-MIT matching the upstream `mindstone/mcp-servers` repo — do not swap it unless the user is explicitly contributing elsewhere.
8. Read `references/starter-template/README.md` → Write to `~/mcp-servers/<api-name>-mcp/README.md`, then **replace every `<CONNECTOR_NAME>`, `<CONNECTOR_DESCRIPTION>`, `<AUTH_INSTRUCTIONS>`, and `<TOOL_LIST>` placeholder with real content** and remove the `PRE_SUBMIT_PLACEHOLDER` HTML-comment line at the top. The pre-submit gate in Phase 6.6 fails while that sentinel remains, which is intentional — it forces the README to be filled in before `ready_to_submit`.
9. Read `references/starter-template/test/smoke.test.mjs` → Write verbatim to `~/mcp-servers/<api-name>-mcp/test/smoke.test.mjs`. The scaffold smoke test validates an MCP handshake and `tools/list` against the built server using only Node.js built-ins (no extra dev-dependencies). The agent augments it with real tool-behaviour tests during Phase 6 — this file is a baseline, not the complete test suite.

Do not skip this step. Do not delegate it to the Software Engineer workflow. The project must exist on disk before delegation.

### 4.3 Delegate to Software Engineer Workflow

Invoke the [Software Engineer workflow](rebel-system/skills/workflows/software-engineer/SKILL.md) with the brief above to perform the coding work. The project directory already exists at `~/mcp-servers/<api-name>-mcp/` with the starter template scaffolded.

The Software Engineer workflow will:

1. Create the working document at `~/mcp-servers/<api-name>-mcp/docs/build-plan.md`
2. Plan staged implementation (the planner reads the MCP reference docs)
3. Implement through fresh-context subagents (one per stage)
4. Run cross-family code review (mandatory — different model family from orchestrator)
5. Validate the implementation (build, tests)

### 4.4 Resume This Skill

When the Software Engineer workflow completes, resume here.

**CHECKPOINT — Report `draft` status now:**
```
rebel_mcp_report_contribution_state(
  sessionId: <session_id from dynamic_env>,
  connectorName: "<api-name>-mcp",
  status: "draft",
  localServerPath: "~/mcp-servers/<api-name>-mcp/"
)
```
This triggers the MCPBuildCard in the conversation UI. Do not skip this call.

Then continue with:

- **Phase 5: Security Validation**
- **Phase 6: Testing & Configuration**
- **Phase 7: Quality Review**
- **Phase 8: Submit to Community**

## Phase 5: Security Validation

Before testing, run security checks on the generated code.

**See [script-security-review](../script-security-review/SKILL.md) for the complete security checklist.**

Key checks for MCP servers:

1. **Credential scan** - No hardcoded API keys, tokens, or secrets
2. **npm audit** - Run `npm audit` and fix Critical/High vulnerabilities
3. **Security review** - Launch subagent or manually verify:
  - Base URL from env var only (no dynamic URLs from user input)
  - All inputs validated via Zod schemas
  - No shell command execution with user input
  - HTTP timeouts configured
  - HTTPS required for external APIs

### OSS Security (for connectors being contributed back)

If this connector will be contributed to the `mcp-servers` repository, run the additional OSS security checks in [contribute-connector.md § OSS Security Review](references/contribute-connector.md#oss-security-review). These cover internal reference stripping, bridge pattern removal, host-neutral error messages, and license/documentation requirements.

## Phase 6: Testing & Configuration

**CHECKPOINT — Report `testing` status now:**
```
rebel_mcp_report_contribution_state(
  sessionId: <session_id from dynamic_env>,
  connectorName: "<api-name>-mcp",
  status: "testing"
)
```
Do not skip this call.

> **Testing reference:** Load [mcp-testing-guide.md](references/mcp-testing-guide.md) for the recommended test strategy (mock API tests → mock client unit tests → declarative integration fallback), what to test (happy path, pagination, error handling, edge cases), debugging common failures (missing build artifacts, startup hangs, schema issues), and MCP Inspector usage.

### 6.1 Build the Project

Run the build commands in the project directory:

```bash
cd ~/mcp-servers/<api-name>-mcp/
npm install
npm run build
```

### 6.2 Set Up Credentials

Ask the user for their API credentials in chat using `AskUserQuestion`. **The "go fetch the key" option MUST pair `url` (the provider's API keys page) with `requiresInput: true` and a clear `inputPlaceholder`.** Without `requiresInput: true`, the user has nowhere to paste the key after fetching it from the URL — the card will auto-submit and the conversation hits a dead end.

Worked example for a connector that needs a single API key:

```json
{
  "questions": [
    {
      "question": "Do you have your <Provider> API key?",
      "header": "API key",
      "options": [
        {
          "label": "Have it",
          "description": "Paste it now",
          "requiresInput": true,
          "inputPlaceholder": "Paste your <Provider> API key here"
        },
        {
          "label": "Need to get it",
          "description": "Open the API keys page and paste it back",
          "url": "https://<provider>.example.com/account/api-keys",
          "requiresInput": true,
          "inputPlaceholder": "Paste your <Provider> API key here"
        }
      ]
    }
  ]
}
```

Once the user provides the value, create the `.env` file and fill in the credentials they gave you:

```bash
cp .env.example .env
```

Fill in the credential values from the user's response. Do not ask the user to edit files manually.

### 6.3 Test Locally

Run the server to verify it starts without errors:

```bash
npm start
```

If startup fails, diagnose and fix the issue. For interactive tool testing, run MCP Inspector:

```bash
npx @modelcontextprotocol/inspector dist/index.js
```

### 6.4 Add to Rebel

> **Anti-pattern (don't do this).** A common failure mode is to read the generic `rebel_mcp_add_server` tool description, see permission framing there, and then pause to ask the user:
>
> // NEVER SAY THIS
> "Adding a connector is a protected admin action — may I proceed?"
>
> That self-block is the exact regression this section is here to prevent. The generic tool description is written for sessions where there is no pre-arranged consent. **You are in such a session right now: this skill IS the consent.** The user invoked `build-custom-mcp-server` knowing it ends with registration; pausing to re-confirm wastes a turn and leaves them watching a half-finished build. If you find yourself drafting a permission question at this point, stop and register instead.
>
> Skill instructions take precedence over generic tool descriptions when the two appear to conflict. The tool description is the conservative default; the skill is the contract for this particular workflow.
>
> **MANDATORY — Register the server now, without asking.** Call `rebel_mcp_add_server` directly. **Do NOT use `AskUserQuestion` to check whether the user wants to register.** The user invoked this skill; that is consent. The auto-detect hook needs this call to create the contribution record and show MCPBuildCard — skipping or gating it behind a question breaks the flow. Just register.

```json
{
  "name": "<api-name>",
  "command": "node",
  "args": ["~/mcp-servers/<api-name>-mcp/dist/index.js"],
  "env": { /* credential env vars from .env */ }
}
```

See [rebel-integration.md](references/rebel-integration.md) for detailed configuration options.

### 6.5 Test in Rebel

Call **each** tool via `use_tool` with realistic inputs — not just one representative tool. For every tool the connector exposes:

- Use inputs a real user might pass (actual IDs, real queries, meaningful limits) — not empty objects or placeholders.
- Verify the response matches what the tool's description promises. Matching the schema is not enough; the data has to be right.
- Iterate on the implementation if the data is wrong, the shape is off, or the response is unhelpful.

You will list every tool you tested, with inputs and results, in the `<testing_evidence>` block below before reporting `ready_to_submit`. Skipping tools here means emitting a dishonest evidence block — don't.

### 6.6 Definition of Done — before you report `ready_to_submit`

Testing is your job before you tell Rebel the connector is ready. The user is trusting the connector to work against their real data. Treat the checklist below as a gate, not a suggestion.

Every item must be true. If any aren't, go fix it and re-run the affected steps.

1. **Build passes** — `npm run build` succeeds with no errors.
2. **MCP Inspector verified each tool** — every tool registered, every `inputSchema.type === "object"`, every description non-empty.
3. **Connector registered in Rebel** — `rebel_mcp_add_server` called successfully and Rebel sees the tools (Phase 6.4).
4. **Each tool called via `use_tool` with realistic inputs** — iterate per tool (Phase 6.5). Not one representative tool, not "they all look similar, I'll skip a few". Every single tool.
5. **Each tool returned the expected data** — no errors, and the response actually contains the fields the tool description promises.

#### Emit a `<testing_evidence>` block before reporting

Immediately before calling `rebel_mcp_report_contribution_state({status: "ready_to_submit", ...})`, emit a visible `<testing_evidence>` block in the conversation listing every tool you tested, the input you used, what you expected, and what came back. One row per tool — no omissions. This is the proof that the checklist above is real, not aspirational.

**Every row MUST include an `http_status` field** (the HTTP status code observed by the tool handler, or `N/A` with a reason for tools that don't make HTTP calls). "PASS" requires HTTP 2xx (or the tool's documented success shape) — a row with `http_status >= 400` or `isError: true` marked PASS is an explicit skill violation.

Format:

```
<testing_evidence>
tool: read_contact
  input: { id: "contact-123" }
  expected: returns Contact object with name and email
  http_status: 200
  actual: { id: "contact-123", name: "Ada Lovelace", email: "ada@example.com" } — PASS

tool: list_contacts
  input: { limit: 5 }
  expected: array of up to 5 Contact objects
  http_status: 200
  actual: [{...}, {...}] (2 items returned) — PASS
</testing_evidence>
```

If a tool failed, fix it — do not paper over it in the block. If a tool genuinely cannot be exercised without side effects on the user's account (e.g., a destructive `delete_*` tool), say so explicitly in the `actual` field, set `http_status: N/A (destructive, not exercised)`, and note how you otherwise verified it (Inspector schema check, mocked unit test, etc.).

**Credential-blocked rule:** If you cannot obtain real credentials to exercise the tools, you MUST NOT report `ready_to_submit`. Stop at `testing` status and tell the user you are blocked on a credential — do not self-progress. Fabricated or all-`isError: true` evidence blocks are worse than none at all because they cause broken PRs to ship.

**Phase 7 pre-flight (non-breaking gate):** Before emitting the evidence block, run `bash rebel-system/skills/coding/build-custom-mcp-server/scripts/pre-submit-check.sh .` from the connector directory. It checks the Phase 7 quality items (LICENSE, README, tests directory, no dist committed, no internal references, `npm audit` clean) in one command. A non-zero exit must be resolved before `ready_to_submit`. This does not change when the state-machine checkpoint fires — it just gates the message you send immediately before it.

**Environment-blocker handling (extends the credential-blocked rule above):** If the script blocks on an environment issue you cannot fix on the user's behalf — `ripgrep` and `grep` both absent, `npm install` failing, `npm audit` unreachable because the machine is offline or behind a corporate registry — do not silently loop. Tell the user what the script is reporting, stay in `testing` status (do not fabricate a `ready_to_submit` report), and ask them to resolve the environment issue or authorise skipping the specific check. This is the same state-machine behaviour as the credential-blocked rule: additional blockers, same "stay in `testing` and be visible about it" response.

Only after the evidence block is emitted and `pre-submit-check.sh` exits clean do you call `rebel_mcp_report_contribution_state` with `status: "ready_to_submit"`.

**CHECKPOINT — Report `ready_to_submit` status with PR metadata now:**

Before calling the checkpoint, prepare PR metadata:

1. **Save the build plan** to `docs/build-plan.md` in the connector directory. Copy the planning doc created by the Software Engineer workflow (from Phase 4) into the connector's `docs/` directory so it ships with the PR. This gives reviewers full visibility into the research, implementation stages, and review history.

2. **Compose the `prTitle`**: Use `feat: add <api-name> connector` format.

3. **Compose the `prBody`** using the [PR Description Template](references/contribute-connector.md#pr-description-template). Fill in every section from context captured during the build:
   - **Summary**: The user's intent — what problem this solves, for whom, and why existing options were insufficient. Use the user's own words where possible.
   - **What it does**: Auth method, tool list with one-liners, annotation summary.
   - **Checks run**: Build/test results, whether tools were tested end-to-end in Rebel, security review outcome.
   - **Reviewer notes**: Known limitations, link to `docs/build-plan.md`.
   - **Build Context**: Workflow used, model, review rounds and key outcomes.

```
rebel_mcp_report_contribution_state(
  sessionId: <session_id from dynamic_env>,
  connectorName: "<api-name>-mcp",
  status: "ready_to_submit",
  localServerPath: "~/mcp-servers/<api-name>-mcp",
  prTitle: "feat: add <api-name> connector",
  prBody: "<composed PR body using the template above>"
)
```

**IMPORTANT — supply `localServerPath` on the `ready_to_submit` call.** The
contribution service treats the report as strict evidence that the connector
is working at a known path. Without `localServerPath`, the card stays in the
`testing` phase and the user sees a "Rebel got stuck checking this connector"
affordance. Pass the same path you wrote to disk — tilde paths like
`~/mcp-servers/<api-name>-mcp` are fine.

**IMPORTANT — supply `prTitle` and `prBody` on the `ready_to_submit` call.**
Without these, the in-app contribution flow falls back to a generic one-liner
PR description that gives reviewers no context about what problem is being
solved. The PR description is the primary artifact reviewers use to make merge
decisions — invest the effort to fill in the template properly.

**If the tool call is rejected, read the error response and self-correct.**
A rejection response includes:
- `error` — a short explanation (e.g. `"Invalid transition: testing → draft."`)
- `currentStatus` — what the record actually is
- `attemptedStatus` — what you tried to set

Re-call `rebel_mcp_report_contribution_state` with a valid target status.
Never silently ignore a rejection — it means the card is stuck and the user
cannot progress.

**`nextAction` grammar — read this when the tool returns `isError: true`.**

When `rebel_mcp_report_contribution_state` returns a response body whose first line begins with `Contribution state report deferred:` or `Contribution state report rejected:`, the body contains a structured `nextAction` literal on the second line that tells you exactly what to do. Anchor on this textual signal — as of 2026-04-27, `isError` is propagated through the Super-MCP `use_tool` envelope, but this grammar remains the primary contract for resilience and auditability, so always read the response text. The values:

| `nextAction` | When you'll see it | What to do |
|---|---|---|
| `run_tests` | You reported `ready_to_submit` without test evidence in this session. | Run `Bash` tests, then call every exposed tool via `use_tool` with real inputs. If Rebel shows zero tools, or any tool still fails, fix that first — do not invent tool calls or emit a placeholder `<testing_evidence>` block. Only after the real tool calls succeed do you emit `<testing_evidence>` and re-call `rebel_mcp_report_contribution_state(status: "ready_to_submit", localServerPath: "~/mcp-servers/<api-name>-mcp/", ...)`. |
| `register_server` | You reported `ready_to_submit` without registering the connector via `rebel_mcp_add_server`. | Call `rebel_mcp_add_server` exactly as in Phase 6.4 (see the anti-pattern callout there: skill invocation is consent — do NOT pause to ask permission), using the built server under `~/mcp-servers/<api-name>-mcp/`. If `rebel_mcp_add_server` returns an error, fix that error and retry the add-server call first. Only re-call `rebel_mcp_report_contribution_state(status: "ready_to_submit", ...)` after `rebel_mcp_add_server` succeeds. |
| `move_to_canonical_path` | Your connector lives outside `~/mcp-servers/<api-name>-mcp/`. | Move all source files to `~/mcp-servers/<api-name>-mcp/`, re-register via `rebel_mcp_add_server` against the new path, then re-call with `localServerPath: "~/mcp-servers/<api-name>-mcp/"`. |
| `reauth_github` | The user's GitHub token has been revoked or the grant is gone. | Tell the user: "Please reconnect GitHub in Settings → Connectors so we can send it out." Then stop. Do not re-call `rebel_mcp_report_contribution_state`, do not try to open an auth flow yourself, and do not mark the contribution complete. Only the user can resolve this. |
| `wait_for_review` | The status you tried to set is not a valid next transition from the current state. | Read the `current_status=...` parenthetical and the guidance line — they tell you the actual current state and the valid next states. Either re-call once with one of those valid statuses, copied verbatim, or stop reporting. Do not re-send the same invalid status, and do not guess a different status that is not listed. |
| `run_software_engineer_workflow` | You reported ready_to_submit on a non-trivial connector without invoking the Software Engineer workflow. | Read rebel-system/skills/workflows/software-engineer/SKILL.md, then re-run the build phases as the SE planner/implementer/reviewer. Re-call rebel_mcp_report_contribution_state(status: "ready_to_submit", ...) once docs/build-plan.md reflects the SE working-doc template (workflow: software-engineer, models.*, ## Review History). |
| `run_software_engineer_workflow` | You ran the Software Engineer workflow earlier, but the connector code has changed since. The SE evidence on this contribution was invalidated and must be refreshed against the current build state. | Re-invoke the Software Engineer workflow against the current connector path. The SE working doc at docs/build-plan.md should be updated (or re-created) to reflect the changed code. Re-call rebel_mcp_report_contribution_state(status: "ready_to_submit", ...) once SE has run on the new build state. |

**Never ignore a `Contribution state report deferred:` or `Contribution state report rejected:` response body.** Reading the response, picking the right `nextAction`, and re-calling within the same conversation turn is the only way to keep the contribution flow moving. Silent acceptance of a deferred state means the build card stays stuck and the user can't ship.

Always act on the latest `rebel_mcp_report_contribution_state` result only. Older deferred/rejected results in the conversation may already be superseded by a later call.

Do not skip this call.

## Phase 7: Quality Review

Before moving to community submission, review this checklist. Each item represents a quality standard that ensures the server is production-ready and maintainable. Community submission happens in Phase 8 after these checks pass.

### Test coverage

- At least basic tests exist (mock API tests preferred, or manual MCP Inspector verification at minimum)
- Tests cover: happy path for each tool, error/edge cases (missing params, API errors, empty results), and pagination if applicable

### Security review

- No hardcoded API keys, tokens, or secrets anywhere in the code
- `.env` for credentials, `.gitignore` excludes `.env`
- Base URL is a constant or from env var — never from tool input (SSRF prevention)
- All tool inputs validated via Zod schemas
- HTTP timeouts configured on API requests
- HTTPS required for external APIs
- Credentials never logged or exposed in tool responses

### Naming compliance

- All tool names use `snake_case` with a service prefix (e.g., `zendesk_search_tickets`)
- All top-level parameter names use `snake_case`
- Canonical names for common concepts: `limit`, `page_token`/`cursor`, `return_json`, `{thing}_id`

### Tool annotations

- Every tool has `readOnlyHint` and `destructiveHint` annotations set correctly
- Read-only tools: `readOnlyHint: true, destructiveHint: false`
- Write/create tools: `readOnlyHint: false, destructiveHint: false`
- Delete/destructive tools: `readOnlyHint: false, destructiveHint: true`

### Documentation

- Tool descriptions are clear, include examples, and note any important constraints
- README exists with: what the server does, setup instructions, tool reference, and auth requirements
- `.env.example` documents all required environment variables

### Packaging

- `npm run build` succeeds without errors
- `bin` field in `package.json` points to `dist/index.js` (for npx distribution)
- `files: ["dist"]` in `package.json` to limit package contents
- Shebang (`#!/usr/bin/env node`) at the top of the entry file

### OSS readiness (if contributing back)

- Passes [OSS Security Review](references/contribute-connector.md#oss-security-review) — no internal references, no bridge code, host-neutral errors
- LICENSE file present with full license text
- `package.json` has a `"license"` field (e.g. `"FSL-1.1-MIT"`) matching the LICENSE file
- README.md present with security disclosures
- Host/domain inputs validated before credential transmission
- **`server.json` registry manifest present** alongside `package.json`. Inherited from `connectors/_template/server.json` when scaffolding from the template. Replace every `CONNECTOR_NAME` / `CONNECTOR_TITLE` / `CONNECTOR_DESCRIPTION` placeholder, declare every required+optional env var (exclude bridge-only env vars `MCP_HOST_BRIDGE_STATE` / `MINDSTONE_REBEL_BRIDGE_STATE`), and validate locally with `mcp-publisher validate server.json`. The CI workflow `.github/workflows/server-json-check.yml` runs the same check on every PR. Schema reference: [contribute-connector.md § MCP Registry Submission](references/contribute-connector.md#mcp-registry-submission).
- **`mcpName` field in `package.json`** equals `server.json.name` exactly (`io.github.mindstone/mcp-server-<connector>`). The registry uses it to verify namespace ownership.

### Common PR review failures to avoid

Real PRs produced by this skill have been blocked on the following items. `pre-submit-check.sh` catches most of them automatically; the rest are your responsibility to verify before reporting `ready_to_submit`.

- **Committed `dist/`** — always listed in `.gitignore`; never `git add` the build output. The submit-pr-to-rebel-oss `files` list must not include `dist/**`.
- **Missing `"license"` field in `package.json`** — the LICENSE file alone is insufficient. Add `"license": "FSL-1.1-MIT"` (or whichever license matches the upstream repo).
- **Personal absolute paths in README** — never `~/mcp-servers/<name>-mcp` or `/Users/<name>/...` in setup instructions. Use `<absolute path to>/mcp-servers/<name>/dist/index.js` or similar neutral placeholder.
- **`destructiveHint: false` on tools that run external shell/AppleScript/binary commands** — any tool that invokes a subprocess or triggers a user-visible side effect on the host must set `destructiveHint: true`, regardless of what the underlying binary "usually" does.
- **Misreading CLI flags** — read the tool documentation for any flag you pass. A `--input-path` / `--input-file` flag expects a filesystem path, not raw text; if you want to feed text to a subprocess, write it to a temp file first or use `stdin`.
- **`spawn()`/`exec()` without a timeout** — always set an explicit `timeout` option. A stalled child hangs the MCP server and every tool call behind it.
- **Tests that redefine Zod schemas inline** — import the real input schema from `src/` so schema drift breaks the tests. `z.object({...})` recreated inside a test file means the test is validating a parallel copy that will silently diverge.

## Phase 8: Submit to Community

> **Include this phase explicitly in any task list or plan you create.** The build is not complete when `ready_to_submit` is reported — it is complete when the user has submitted (or declined to submit) the connector to the community. Treat this as a named, tracked step of the plan, not a conversational afterthought.

After Phase 7's quality checklist passes (`ready_to_submit` was reported at the end of Phase 6), guide the user through the community submission step. Other Rebel users can install submitted connectors with one click, so this is the point of the whole build flow for most users.

**Build Context appendix — auto-injected, do not compose manually**

The Build Context block (model, app-version, session-id, task-subagent observations, build-plan shape) is auto-injected into your PR body. You do NOT need to compose it manually. If you write your own `prBody` override, the Build Context block is still appended after your content — your override sits above it.

**Primary path — in-app contribution flow:**

Use the in-app "Add to the community" flow (the `rebel_mcp_report_contribution_state` tool is always available as a bundled tool):

1. Confirm `rebel_mcp_report_contribution_state` was already called with status `ready_to_submit` at the end of Phase 6. If not, call it now.
2. Tell the user their [service] tool works. They can use the card to share it with everyone, or keep it private.
3. **Remain available after telling the user** — if they hit an auth/fork/push error, help them resolve it. Do not treat your work as finished until the user has either submitted successfully or explicitly declined to submit.
4. No manual Git commands needed — the in-app flow handles fork, branch, push, and PR creation.

> The in-app flow uses the contribution service (IPC channels: `contribution:start-auth`, `contribution:submit`) to automate the entire GitHub workflow. The user just clicks a button.

**If the user declines to submit** (wants to keep the connector private), acknowledge that and stop — do not press. The connector is still usable locally; the community submission is optional from the user's perspective even though it is a mandatory plan step from yours.

**Fallback — manual Git workflow:**

If the in-app tools aren't available, or the user explicitly prefers manual control, delegate the PR mechanics to the [submit-pr-to-rebel-oss](../submit-pr-to-rebel-oss/SKILL.md) skill. That skill owns the generic fork/branch/commit/push/PR flow via the GitHub Git Data API; this skill stays responsible for the MCP-specific context (PR template, file list, OSS security review).

> **STOP before invoking the PR skill — all of these must be true:**
> 1. **Phase 7 quality review and the [OSS Security Review](references/contribute-connector.md#oss-security-review) have passed.** The PR skill refuses to run without this, but the responsibility to confirm lives here.
> 2. **`prTitle` and `prBody` are composed** using the [PR Description Template](references/contribute-connector.md#pr-description-template). A generic one-liner body is rejected.
> 3. **`files` enumerates every connector file** — see the list below. No `git add .`, no wildcards.
> 4. **No `dist/`, `node_modules/`, `.env` (actual credentials), coverage output, or IDE config is in `files`.**

Pass the following parameters to the submit-pr-to-rebel-oss skill:

| Param | Value for a new MCP connector PR |
|-------|----------------------------------|
| `repo` | `mindstone/mcp-servers` |
| `baseBranch` | `main` |
| `branchName` | `feat/<api-name>-connector` (e.g. `feat/zendesk-connector`) |
| `commitMessage` | `feat(<api-name>): add <api-name> connector` |
| `prTitle` | `feat: add <api-name> connector` (matches the title you reported via `rebel_mcp_report_contribution_state`) |
| `prBody` | The markdown you composed from the PR Description Template |
| `pathAllowlistPrefix` | `connectors/<api-name>/` |
| `files` | The full source→destination list below |

**`files`** — every file is an object with a `source` (your local build directory) and `destination` (where it lands in `mcp-servers`). The directories differ because the connector is built off-repo. The example below uses JSON with comments (`jsonc`) for readability — strip the comments before passing the array to the skill:

```jsonc
[
  { "source": "~/mcp-servers/<api-name>-mcp/package.json",    "destination": "connectors/<api-name>/package.json" },
  { "source": "~/mcp-servers/<api-name>-mcp/tsconfig.json",   "destination": "connectors/<api-name>/tsconfig.json" },
  { "source": "~/mcp-servers/<api-name>-mcp/.gitignore",      "destination": "connectors/<api-name>/.gitignore" },
  { "source": "~/mcp-servers/<api-name>-mcp/.env.example",    "destination": "connectors/<api-name>/.env.example" },
  { "source": "~/mcp-servers/<api-name>-mcp/LICENSE",         "destination": "connectors/<api-name>/LICENSE" },
  { "source": "~/mcp-servers/<api-name>-mcp/README.md",       "destination": "connectors/<api-name>/README.md" },
  { "source": "~/mcp-servers/<api-name>-mcp/src/index.ts",    "destination": "connectors/<api-name>/src/index.ts" },
  { "source": "~/mcp-servers/<api-name>-mcp/src/logger.ts",   "destination": "connectors/<api-name>/src/logger.ts" },
  // ...every additional source file under src/
  { "source": "~/mcp-servers/<api-name>-mcp/test/smoke.test.mjs", "destination": "connectors/<api-name>/test/smoke.test.mjs" },
  // ...every additional test file under test/
  { "source": "~/mcp-servers/<api-name>-mcp/docs/build-plan.md",  "destination": "connectors/<api-name>/docs/build-plan.md" }
]
```

Include **every** file under your build directory that belongs in the PR. Exclude `node_modules/`, `dist/`, `.env` with real credentials, coverage output, and IDE config. The `docs/build-plan.md` Software Engineer working document ships with the PR — it gives reviewers the full research, implementation, and review history.

When the submit-pr-to-rebel-oss skill returns, report the PR number and URL to the user.

## Software Engineer Workflow

Phase 4 implementation is always orchestrated through the [Software Engineer workflow](rebel-system/skills/workflows/software-engineer/SKILL.md). Project complexity affects how many implementation stages the planner creates and how detailed the working document needs to be — not whether the workflow is used. Even a simple 3-tool MCP benefits from structured planning and cross-family code review.

## [IMPORTANT]

- **Never modify user's existing codebase** - MCP project is separate
- **Never hardcode credentials** - always use environment variables
- **Never create "fetch any URL" tools** - fixed baseUrl only (SSRF prevention)
- **Start with read-only tools** - add write operations only if explicitly needed
- **Get user approval before implementation** - confirm tool list in Phase 3
- **Use researcher subagent for external APIs** - don't guess at documentation
- **Reference bundled patterns** - load `references/` docs, don't reinvent MCP best practices
- **Keep first iteration small** - 3-5 tools, expand later if needed
- **Run security checks before testing** - credential scan, npm audit, security review
- **Use sanitized logger** - never log Authorization headers or credentials
- **Require HTTPS for external APIs** - warn if HTTP used

## Troubleshooting

### "npm not found"

User needs to install Node.js: [https://nodejs.org](https://nodejs.org)

### "Cannot find module" errors

Run `npm install` in the project folder

### "API_KEY environment variable required"

User needs to create `.env` file with credentials

### "Connection refused" / "ECONNREFUSED"

- For internal APIs: Check VPN connection
- Verify API base URL is correct

### Tools not appearing in Rebel

- Restart Rebel after adding MCP config
- Check Rebel logs for MCP startup errors
