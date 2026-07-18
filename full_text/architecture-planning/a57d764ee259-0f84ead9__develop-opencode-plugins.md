---
name: develop-opencode-plugins
description: OpenCode plugin and platform reference for updating or removing code in agentic/src/modules.
---

# OpenCode Plugins Development

## Applicability

Use this skill only when all are true:

- the target repository is `/Users/michaljarnot/IdeaProjects/agentic`
- the task updates or removes code under `/Users/michaljarnot/IdeaProjects/agentic/src/modules/**`
- the work needs OpenCode platform/plugin architecture or tool/framework reference context

If these signals are missing, do not apply this skill.

Never load this skill for work outside `/Users/michaljarnot/IdeaProjects/agentic/src/modules`.

## OpenCode: complete documentation reference

**OpenCode is an open-source agentic AI coding assistant** available as a terminal TUI, desktop app, and IDE extension. Built on a client/server architecture with a Bun/JS runtime and Hono HTTP server, it supports **75+ LLM providers** via the AI SDK and Models.dev, and it ships with a sophisticated agent system, tool framework, MCP integration, and full-featured TUI. With over **100,000 GitHub stars**, 700 contributors, and 2.5M+ monthly users, it is the leading open-source alternative to proprietary coding agents.

## Architecture and core design

OpenCode follows a **client/server architecture**. Running `opencode` starts both a TUI client and an internal HTTP server. The server can also run headless via `opencode serve`, enabling remote clients (desktop app, web interface, mobile). The server exposes a full **OpenAPI 3.1 REST API** at `/doc`, with a TypeScript SDK (`@opencode-ai/sdk`) generated via Stainless.

The system supports **multi-session** operation — multiple agents can run in parallel on the same project. Sessions persist in a **SQLite database**, and all processing happens locally or through direct provider API calls. OpenCode does not store code or context data on its servers; only the `/share` feature sends data externally.

Key architectural components include the **AI SDK** for provider-agnostic LLM interaction, **ripgrep** for file search operations (`grep`, `glob`, `list`), built-in **LSP client integration** for 30+ languages, an **event bus** for internal communication, and a **plugin system** for extensibility.

## Installation methods

The install script is the fastest path:

```bash
curl -fsSL https://opencode.ai/install | bash
```

Package manager options include **npm** (`npm install -g opencode-ai`), **bun** (`bun install -g opencode-ai`), **pnpm**, **yarn**, **Homebrew** (`brew install anomalyco/tap/opencode` for latest releases; `brew install opencode` for official but less frequently updated formula), **Arch Linux** (`sudo pacman -S opencode` or `paru -S opencode-bin`), **Scoop** (`scoop install opencode`), **Chocolatey** (`choco install opencode`), **Mise** (`mise use -g github:anomalyco/opencode`), **Nix** (`nix run nixpkgs#opencode`), and **Docker** (`docker run -it --rm ghcr.io/anomalyco/opencode`). Binaries are also available from GitHub Releases. For Windows, **WSL is recommended** for best compatibility.

Prerequisites are a modern terminal emulator (WezTerm, Alacritty, Ghostty, Kitty) and API keys for at least one LLM provider.

## Configuration system (opencode.json)

OpenCode uses **JSON/JSONC** configuration files with schema validation at `https://opencode.ai/config.json`. A separate TUI config (`tui.json`, schema `https://opencode.ai/tui.json`) handles UI settings.

### Config loading precedence (later overrides earlier, merged not replaced)

1. **Remote config** — from `.well-known/opencode` endpoint (organizational defaults)
2. **Global config** — `~/.config/opencode/opencode.json`
3. **Custom config** — via `OPENCODE_CONFIG` environment variable
4. **Project config** — `opencode.json` in project root (discovered by traversing up to nearest Git directory)
5. **`.opencode` directories** — agents, commands, plugins, tools, themes
6. **Inline config** — via `OPENCODE_CONFIG_CONTENT` environment variable

### Variable substitution

- **Environment variables**: `{env:VARIABLE_NAME}` — replaced at load time
- **File contents**: `{file:path/to/file}` — relative to config file location or absolute

### Complete opencode.json schema

| Key                  | Type                | Description                                                                                                                                           |
| -------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`            | string              | `"https://opencode.ai/config.json"`                                                                                                                   |
| `model`              | string              | Default model, format `provider/model` (e.g. `"anthropic/claude-sonnet-4-5"`)                                                                         |
| `small_model`        | string              | Lightweight model for titles/summaries; defaults to `gpt-5-nano` via Zen                                                                              |
| `default_agent`      | string              | Default primary agent (`"build"` or `"plan"` or custom)                                                                                               |
| `autoupdate`         | boolean\|`"notify"` | Auto-update behavior; `true` (default), `false`, or `"notify"`                                                                                        |
| `share`              | string              | Sharing mode: `"manual"` (default), `"auto"`, `"disabled"`                                                                                            |
| `provider`           | object              | Custom provider configs with `timeout`, `setCacheKey`, `options`, `models`                                                                            |
| `tools`              | object              | Enable/disable tools globally by name (boolean values)                                                                                                |
| `permission`         | string\|object      | Permission config — `"allow"`, or per-tool object with patterns                                                                                       |
| `agent`              | object              | Agent definitions with `description`, `model`, `prompt`, `tools`, `permission`, `temperature`, `top_p`, `mode`, `color`, `steps`, `hidden`, `disable` |
| `command`            | object              | Custom commands with `template`, `description`, `agent`, `model`, `subtask`                                                                           |
| `instructions`       | array               | Paths, globs, or URLs to instruction files (combined with AGENTS.md)                                                                                  |
| `compaction`         | object              | `{ auto: true, prune: true, reserved: 10000 }`                                                                                                        |
| `watcher`            | object              | `{ ignore: ["node_modules/**", "dist/**"] }`                                                                                                          |
| `mcp`                | object              | MCP server definitions (local/remote)                                                                                                                 |
| `plugin`             | array               | npm plugin packages to load                                                                                                                           |
| `formatter`          | object\|false       | Formatter configs per tool, or `false` to disable all                                                                                                 |
| `lsp`                | object\|false       | LSP server configs, or `false` to disable all                                                                                                         |
| `server`             | object              | `{ port, hostname, mdns, mdnsDomain, cors }`                                                                                                          |
| `disabled_providers` | array               | Provider IDs to disable (takes priority)                                                                                                              |
| `enabled_providers`  | array               | Allowlist of providers                                                                                                                                |
| `experimental`       | object              | Unstable options: `chatMaxRetries`, `disable_paste_summary`, `hook`                                                                                   |

## Permission system

Permissions control whether tool actions run automatically, prompt the user, or are blocked entirely. Three actions exist: **`"allow"`** (run without approval), **`"ask"`** (prompt user who can choose once/always/reject), and **`"deny"`** (block entirely).

### Configuration granularity

Permissions can be set at four levels of specificity. **Global shorthand** (`"permission": "allow"`) sets all tools. **Per-tool** (`"permission": { "bash": "ask", "edit": "deny" }`) targets individual tools. **Wildcard** (`"*": "ask"`) provides a catch-all. **Granular patterns** allow per-command or per-path rules:

```json
{
  "permission": {
    "bash": { "*": "ask", "git *": "allow", "rm *": "deny" },
    "edit": { "*": "deny", "src/**/*.ts": "allow" }
  }
}
```

Pattern matching uses `*` (zero or more characters) and `?` (exactly one character). **Last matching rule wins**. Home directory expansion (`~`, `$HOME`) is supported.

### Permission keys and what they match

| Key                      | Matches Against                                                    |
| ------------------------ | ------------------------------------------------------------------ |
| `read`                   | File path                                                          |
| `edit`                   | All file modifications (edit, write, patch, multiedit)             |
| `glob`                   | Glob pattern                                                       |
| `grep`                   | Regex pattern                                                      |
| `list`                   | Directory path                                                     |
| `bash`                   | Parsed commands (e.g. `git status --porcelain`)                    |
| `task`                   | Subagent type                                                      |
| `skill`                  | Skill name                                                         |
| `lsp`                    | Non-granular                                                       |
| `todoread`/`todowrite`   | Non-granular                                                       |
| `webfetch`               | URL                                                                |
| `websearch`/`codesearch` | Query                                                              |
| `external_directory`     | Paths outside project (default: `"ask"`)                           |
| `doom_loop`              | Same tool call repeated 3× with identical input (default: `"ask"`) |

Defaults: most permissions are `"allow"`. The `read` tool denies `.env` files by default (`*.env` → deny, `*.env.*` → deny, `*.env.example` → allow). Agent-specific permissions merge with global config, with agent rules taking precedence.

## Agents: the core abstraction

OpenCode's agent system is its central architectural feature. **Agents are specialized AI assistants** with configurable prompts, models, tool access, and permissions. There are two types: **primary agents** (direct user interaction, switchable via Tab key) and **subagents** (invoked by primary agents or via `@mention`).

### Built-in agents

- **Build** (primary) — Default agent with all tools enabled for full development work
- **Plan** (primary) — Restricted agent for analysis/planning; `edit` and `bash` set to `"ask"` by default
- **General** (subagent) — Full tool access except todo; for researching and multi-step tasks
- **Explore** (subagent) — Read-only, fast codebase exploration; cannot modify files
- **Compact** (hidden) — Auto-compacts long context into summaries
- **Title** (hidden) — Generates session titles
- **Summary** (hidden) — Creates session summaries

### Agent configuration options

Agents can be defined in `opencode.json` or as markdown files in `.opencode/agents/` (project) or `~/.config/opencode/agents/` (global). The markdown filename becomes the agent name.

| Option        | Description                                                              |
| ------------- | ------------------------------------------------------------------------ |
| `description` | Required for custom agents; brief purpose description                    |
| `mode`        | `"primary"`, `"subagent"`, or `"all"` (default)                          |
| `model`       | Override model; format `provider/model-id`                               |
| `prompt`      | Custom system prompt; supports `{file:./path}` references                |
| `temperature` | 0.0–1.0; default varies by model (0 for most, 0.55 for Qwen)             |
| `tools`       | Object enabling/disabling tools by name (booleans); supports wildcards   |
| `permission`  | Per-agent permission overrides; merges with global config                |
| `steps`       | Max agentic iterations before forced text-only response                  |
| `hidden`      | Boolean; hides subagent from `@` autocomplete (still invokable by model) |
| `disable`     | Boolean; disables agent entirely                                         |
| `color`       | Hex color or theme color name for UI                                     |
| `top_p`       | Alternative diversity control (0.0–1.0)                                  |

Any unrecognized options are **passed through to the provider** as model options (e.g., OpenAI's `reasoningEffort`).

### Creating agents

Run `opencode agent create` for an interactive wizard, or create markdown files directly:

```markdown
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
write: false
edit: false
bash: false
permission:
edit: deny
bash:
'\*': ask
'git diff': allow

You are a code reviewer. Focus on security, performance, and maintainability.
```

## All built-in tools

OpenCode ships with **15+ built-in tools** that the LLM can invoke during conversations. All are enabled by default.

### Tool reference

**`bash`** — Execute shell commands in the project environment. Granular permissions match parsed command strings (e.g., `"git *": "allow"`).

**`edit`** — Modify existing files via exact string replacements. The primary way the LLM edits code.

**`write`** — Create new files or overwrite existing ones.

**`multiedit`** — Apply multiple edits to files in one operation.

**`patch`** — Apply patch/diff files to the codebase.

**`read`** — Read file contents; supports specific line ranges for large files. Denies `.env` files by default.

**`grep`** — Fast regex content search across the codebase. Uses ripgrep internally, respects `.gitignore`.

**`glob`** — Find files using glob patterns (e.g., `**/*.ts`). Returns paths sorted by modification time. Uses ripgrep.

**`list`** — List directory contents with optional glob filtering. Uses ripgrep.

**`lsp`** (experimental) — Interact with configured LSP servers. Requires `OPENCODE_EXPERIMENTAL_LSP_TOOL=true`. Operations: `goToDefinition`, `findReferences`, `hover`, `documentSymbol`, `workspaceSymbol`, `goToImplementation`, `prepareCallHierarchy`, `incomingCalls`, `outgoingCalls`.

**`skill`** — Load a `SKILL.md` file on-demand into conversation context. Agents see available skills and request them by name.

**`todowrite` / `todoread`** — Create/read task lists for tracking multi-step operations. Disabled for subagents by default.

**`webfetch`** — Fetch and read web pages. Granular permissions match URLs.

**`websearch`** — Search the web using Exa AI. Available when using OpenCode provider or `OPENCODE_ENABLE_EXA=true`.

**`question`** — Ask the user questions during tasks, with structured options and custom answer support.

**`task`** — Launch subagents for delegated work. Granular permissions match subagent names.

### Custom tools

Custom tools are TypeScript/JavaScript files placed in `.opencode/tools/` (project) or `~/.config/opencode/tools/` (global). The filename becomes the tool name. Multiple named exports create separate tools (`math.ts` with `add` and `multiply` → `math_add`, `math_multiply`).

```typescript
import { tool } from '@opencode-ai/plugin'
export default tool({
  description: 'Query the project database',
  args: { query: tool.schema.string().describe('SQL query to execute') },
  async execute(args, context) {
    // context provides: agent, sessionID, messageID, directory, worktree
    return `Result: ${args.query}`
  },
})
```

Custom tools with the same name as built-in tools **take precedence**. Tool definitions must be TypeScript/JavaScript but can invoke any language via shell commands.

## MCP server integration

OpenCode supports the **Model Context Protocol** for integrating external tool servers. MCP tools become automatically available to the LLM alongside built-in tools. Configuration lives in `opencode.json` under the `mcp` key.

### Local MCP servers

```json
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-everything"],
      "environment": { "API_KEY": "{env:MY_KEY}" },
      "enabled": true,
      "timeout": 5000
    }
  }
}
```

### Remote MCP servers

```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "headers": { "Authorization": "Bearer {env:SENTRY_TOKEN}" },
      "oauth": {},
      "enabled": true,
      "timeout": 5000
    }
  }
}
```

**OAuth support** is automatic — OpenCode detects 401 responses and initiates OAuth via Dynamic Client Registration (RFC 7591). Pre-registered credentials can be set via `oauth.clientId`, `oauth.clientSecret`, `oauth.scope`. Set `"oauth": false` for API-key-only servers. OAuth tokens are stored in `~/.local/share/opencode/mcp-auth.json`.

### MCP CLI management

- `opencode mcp add` — Interactive server addition
- `opencode mcp list` — List servers and status
- `opencode mcp auth <name>` — Manually authenticate
- `opencode mcp logout <name>` — Remove credentials
- `opencode mcp debug <name>` — Diagnose connection issues

MCP tools are namespaced with the server name prefix (e.g., `mymcp_toolname`). They can be controlled via `tools` config with glob patterns: `"mymcp_*": false` disables all tools from that server. Permission control works similarly: `"permission": { "mymcp_*": "ask" }`.

**Important caveat**: MCP servers add to context, which can quickly exceed context limits. The GitHub MCP server is specifically noted as heavy.

## All supported AI providers

OpenCode supports **75+ providers** through Models.dev. Providers are configured via the `/connect` TUI command (which stores keys in `~/.local/share/opencode/auth.json`) or directly in `opencode.json`.

### OpenCode's own services

- **OpenCode Zen** — Pay-as-you-go curated models (30+ models including GPT 5.x, Claude 4.x, Gemini 3.x, GLM, Kimi, MiniMax). Pricing ranges from free (GPT 5 Nano, MiniMax M2.5 Free) to premium (Claude Opus 4.1 at $15/$75 per 1M tokens). Auto-reload when balance drops below $5.
- **OpenCode Go** — $10/month subscription for open models (GLM-5, Kimi K2.5, MiniMax M2.5). Usage limits: $4/5-hour, $10/weekly, $20/monthly. Hosted in US, EU, Singapore.

### Major providers (non-exhaustive)

**Direct API providers**: OpenAI (including ChatGPT Plus/Pro OAuth), Anthropic (including Claude Pro/Max OAuth), Google Vertex AI, Amazon Bedrock (multiple auth methods: access keys, named profiles, bearer tokens, Web Identity), Azure OpenAI, Azure Cognitive Services, DeepSeek, xAI, Groq, Cerebras, Together AI, Fireworks AI, Deep Infra, Baseten, MiniMax, Moonshot AI, Z.AI.

**Gateway/aggregator providers**: OpenRouter, Helicone (observability gateway), Cloudflare AI Gateway, Vercel AI Gateway, ZenMux, Hugging Face (17+ inference providers).

**Enterprise/specialized**: GitLab Duo (OAuth or PAT, self-hosted support, plugin for MR/issue management), GitHub Copilot (device code auth, Pro+ for some models), SAP AI Core, STACKIT (European sovereign), OVHcloud, Scaleway, Nebius, 302.AI, Cortecs, IO.NET, Venice AI.

**Local model providers**: Ollama (tip: increase `num_ctx` to 16k–32k for tool calls), LM Studio, llama.cpp, Ollama Cloud. All configured via `@ai-sdk/openai-compatible` with appropriate `baseURL`.

### Custom provider configuration

```json
{
  "provider": {
    "myprovider": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Display Name",
      "options": {
        "baseURL": "https://api.myprovider.com/v1",
        "apiKey": "{env:MY_API_KEY}"
      },
      "models": {
        "my-model": {
          "name": "My Model",
          "limit": { "context": 200000, "output": 65536 }
        }
      }
    }
  }
}
```

## Model configuration and variants

### Model selection priority

1. `--model` / `-m` CLI flag
2. `model` key in `opencode.json`
3. Last used model
4. First model via internal priority

### Model options

Global model options are set under `provider.<id>.models.<model>.options`. Agent-level model options override global. Pass-through options go directly to the provider (e.g., `reasoningEffort`, `thinking.budgetTokens`).

### Variants

Variants provide different configurations for the same model without duplicating entries. Built-in variants exist for Anthropic (`high`, `max` thinking budgets), OpenAI (`none` through `xhigh` reasoning effort), and Google (`low`, `high`). Cycle through variants with `ctrl+t` (configurable `variant_cycle` keybind). Custom variants:

```json
{
  "provider": {
    "opencode": {
      "models": {
        "gpt-5": {
          "variants": {
            "high": { "reasoningEffort": "high" },
            "low": { "reasoningEffort": "low" }
          }
        }
      }
    }
  }
}
```

## TUI interface in detail

### Layout and interaction

The TUI is built with **Bubble Tea** (Go-based terminal UI framework in the original, now JS-based). It features a message area, input prompt, sidebar (togglable), status bar showing current agent/model, and diff viewer.

- **File references**: Type `@` to fuzzy-search project files and include them in context
- **Shell shortcuts**: Prefix with `!` to run shell commands (output added to conversation)
- **Image support**: Drag and drop images into the terminal
- **Agent switching**: Tab key cycles primary agents; `@mention` invokes subagents
- **External editor**: `/editor` opens `$EDITOR` for composing long messages

### TUI configuration (tui.json)

| Option                | Description                                               |
| --------------------- | --------------------------------------------------------- |
| `theme`               | Theme name (default: `"opencode"`)                        |
| `keybinds`            | Custom key bindings                                       |
| `scroll_speed`        | Scroll speed (default: 3, minimum 0.001)                  |
| `scroll_acceleration` | `{ enabled: boolean }` — macOS-style acceleration         |
| `diff_style`          | `"auto"` (adapts to width) or `"stacked"` (single-column) |

### Built-in TUI slash commands

| Command     | Aliases                | Keybind     | Purpose                                         |
| ----------- | ---------------------- | ----------- | ----------------------------------------------- |
| `/connect`  |                        |             | Add provider credentials                        |
| `/models`   |                        | `<leader>m` | Browse and select models                        |
| `/new`      | `/clear`               | `<leader>n` | Start new session                               |
| `/sessions` | `/resume`, `/continue` | `<leader>l` | List/switch sessions                            |
| `/init`     |                        | `<leader>i` | Create/update AGENTS.md                         |
| `/compact`  | `/summarize`           | `<leader>c` | Compact session context                         |
| `/undo`     |                        | `<leader>u` | Undo last message + file changes (requires Git) |
| `/redo`     |                        | `<leader>r` | Redo undone message                             |
| `/share`    |                        | `<leader>s` | Create shareable URL                            |
| `/unshare`  |                        |             | Remove share link                               |
| `/export`   |                        | `<leader>x` | Export conversation to Markdown                 |
| `/editor`   |                        | `<leader>e` | Open external editor                            |
| `/details`  |                        | `<leader>d` | Toggle tool execution details                   |
| `/themes`   |                        | `<leader>t` | Switch themes                                   |
| `/thinking` |                        |             | Toggle thinking block visibility                |
| `/help`     |                        | `<leader>h` | Show help dialog                                |
| `/exit`     | `/quit`, `/q`          | `<leader>q` | Exit                                            |

### Key bindings system

All keybinds are configurable in `tui.json` and use a **leader key** system (default: `ctrl+x`). Set a keybind to `"none"` to disable it.

**Essential keybinds**:

- `escape` — Interrupt running session
- `tab` / `shift+tab` — Cycle agents forward/backward
- `ctrl+t` — Cycle model variants
- `f2` / `shift+f2` — Cycle recent models
- `ctrl+p` — Command palette
- `<leader>right/left` — Navigate child sessions
- `<leader>up` — Navigate to parent session
- `<leader>g` — Session timeline
- `<leader>b` — Toggle sidebar
- `<leader>y` — Copy last message
- `<leader>a` — Agent list

**Input keybinds** include standard readline-style navigation (`ctrl+a/e` for line start/end, `ctrl+k/u` for kill to end/start, `ctrl+w` for word delete, `alt+b/f` for word movement), selection (`shift+arrows`), and undo/redo (`ctrl+-` and `ctrl+.`). Newlines via `shift+return`, `ctrl+return`, `alt+return`, or `ctrl+j`.

## Session management

Sessions persist all conversation history in SQLite. Key capabilities include:

- **Continue sessions**: `opencode --continue` (or `-c`) resumes last session; `opencode --session <id>` resumes specific session
- **Fork sessions**: `opencode --fork` creates a branch from current session state
- **Child sessions**: Subagents create child sessions navigable via `<leader>right/left/up`
- **Export/import**: `opencode export [sessionID]` produces JSON; `opencode import <file>` accepts JSON files or share URLs
- **Statistics**: `opencode stats` shows token usage and costs (flags: `--days`, `--tools`, `--models`, `--project`)
- **Sharing**: `/share` creates a public URL at `opencode.ai/s/<id>`; `/unshare` removes it and deletes server-side data

### Context compaction

When sessions grow long, OpenCode auto-compacts context using a hidden Compact agent. Configuration: `"compaction": { "auto": true, "prune": true, "reserved": 10000 }`. Manual trigger via `/compact`. The `prune` option removes old tool outputs to save tokens.

## Custom instructions and AGENTS.md

**AGENTS.md** is the primary mechanism for providing project-specific context to the LLM. It's included in the system prompt and should contain project structure, coding standards, conventions, and operational instructions.

### Creating and locating AGENTS.md

Run `/init` in the TUI to auto-generate by scanning the project. Locations with precedence:

1. **Project**: `AGENTS.md` in project root (traverse up from cwd; committed to Git)
2. **Global**: `~/.config/opencode/AGENTS.md`
3. **Claude Code fallback**: `CLAUDE.md` (project) and `~/.claude/CLAUDE.md` (global)

First matching file wins per category. Disable Claude Code compatibility with `OPENCODE_DISABLE_CLAUDE_CODE=1`.

### Additional instruction sources

The `instructions` config key accepts an array of paths, glob patterns, and URLs (fetched with 5-second timeout):

```json
{ "instructions": ["CONTRIBUTING.md", "docs/guidelines.md", ".cursor/rules/*.md", "https://example.com/rules.md"] }
```

## Skills system

Skills are **reusable instructions** loaded on-demand via the `skill` tool. Agents see available skills listed in their tool description and load full content when needed.

### File structure

Create `skills/<name>/SKILL.md` in `.opencode/`, `~/.config/opencode/`, `.claude/`, or `.agents/` directories. OpenCode walks up from the current directory to the git worktree root, loading all matching skills.

### SKILL.md format

```markdown
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
audience: maintainers

## What I do

- Draft release notes from merged PRs
- Propose a version bump
```

Names must be **1–64 lowercase alphanumeric characters** with single-hyphen separators, matching the directory name. Skills can have per-agent permissions with pattern matching (e.g., `"internal-*": "deny"`).

## Custom commands

Custom commands define prompt templates invoked via `/command-name` in the TUI. They can override built-in commands.

### Definition methods

**Markdown files** in `.opencode/commands/` (project) or `~/.config/opencode/commands/` (global):

```markdown
description: Run tests with coverage
agent: build
model: anthropic/claude-sonnet-4-20250514

Run the full test suite with coverage report and show any failures.
```

**JSON config** in `opencode.json`:

```json
{ "command": { "test": { "template": "Run tests...", "description": "Run tests", "agent": "build", "model": "...", "subtask": false } } }
```

### Prompt placeholders

- **`$ARGUMENTS`** — All arguments after the command name
- **`$1`, `$2`** — Positional parameters
- **`` !`command` ``** — Inject shell command output
- **`@filename`** — Include file content

## GitHub Actions and CI automation

OpenCode integrates directly with GitHub workflows. Mention **`/opencode`** or **`/oc`** in issue/PR comments, and OpenCode executes tasks inside GitHub Actions runners.

### Capabilities

- **Triage issues**: Analyze and explain issues
- **Fix and implement**: Creates branches, implements changes, opens PRs
- **PR review**: Automated code review on PR events
- **Scheduled tasks**: Cron-based automation (e.g., weekly dependency checks)
- **Code-line comments**: Comment on specific lines in PR diffs with `/oc` to get targeted changes

### Installation

Run `opencode github install` for automated setup, or manually: install the GitHub App at `github.com/apps/opencode-agent`, add the workflow YAML, and configure secrets.

### Supported event types

Issue comments, PR review comments, issue opened/edited, PR opened/updated, scheduled (cron), and manual workflow dispatch. The action reference is `anomalyco/opencode/github@latest` with parameters: `model` (required), `agent`, `share`, `prompt`, `token`, `use_github_token`.

## LSP server integration

OpenCode includes a built-in LSP client supporting **30+ languages**. When a file is opened, OpenCode checks the extension and starts the appropriate server. Currently, **only diagnostics are exposed** to the LLM (the experimental LSP tool adds more operations).

Built-in LSP servers include TypeScript, Python (Pyright), Go (gopls), Rust (rust-analyzer), C/C++ (clangd), Java (jdtls), Ruby, PHP (Intelephense), Dart, Swift, Kotlin, Lua, Haskell, Elixir, Gleam, Zig, Terraform, Vue, Svelte, Astro, Bash, YAML, Nix, OCaml, Clojure, C#, F#, Julia, Prisma, and more. Many auto-install when the relevant project is detected.

Configuration per server: `disabled` (boolean), `command` (string[]), `extensions` (string[]), `env` (object), `initialization` (object). Disable all with `"lsp": false`. Disable auto-download with `OPENCODE_DISABLE_LSP_DOWNLOAD=true`.

## Theming system

OpenCode ships with **12 built-in themes**: `opencode` (default), `system` (adapts to terminal colors), `tokyonight`, `everforest`, `ayu`, `catppuccin`, `catppuccin-macchiato`, `gruvbox`, `kanagawa`, `nord`, `matrix`, and `one-dark`. Select via `/themes` command or `tui.json`.

Custom themes are JSON files placed in `~/.config/opencode/themes/` (global) or `.opencode/themes/` (project). Schema at `https://opencode.ai/theme.json`. Colors accept hex (`"#ffffff"`), ANSI (0–255), references (`"primary"`), dark/light variants, or `"none"`. Color keys cover UI elements (primary, secondary, accent, error, warning, success, info), text, backgrounds, borders, diff highlighting, markdown rendering, and syntax highlighting.

Requires **truecolor** terminal support (`COLORTERM=truecolor`).

## Plugin system

Plugins extend OpenCode by hooking into events and customizing behavior. They're JS/TS modules loaded from `.opencode/plugins/` (project), `~/.config/opencode/plugins/` (global), or npm packages specified in the `plugin` config array.

```typescript
import type { Plugin } from '@opencode-ai/plugin'
export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree }) => ({
  'event': async ({ event }) => {
    /* handle events */
  },
  'tool.execute.before': async (input, output) => {
    /* intercept tool calls */
  },
  'shell.env': async (input, output) => {
    output.env.MY_KEY = 'value'
  },
  'tool': {
    mytool: tool({
      /* custom tool definition */
    }),
  },
})
```

Plugins can listen to **50+ event types** across categories: command, file, installation, LSP, message, permission, server, session, todo, shell, tool, and TUI events. Key hooks include `tool.execute.before/after` (intercept tool calls), `shell.env` (inject environment variables), and `experimental.session.compacting` (customize context compaction).

## HTTP server API

The `opencode serve` command exposes a comprehensive REST API with **60+ endpoints** covering sessions, messages, files, config, providers, agents, tools, LSP, MCP, and TUI control. The OpenAPI spec is available at `/doc`. Key endpoint groups:

- **Sessions**: CRUD, fork, abort, share, summarize, revert, diff, permissions
- **Messages**: Send (sync and async), list, command execution, shell execution
- **Files**: Search content, find files/directories, read files, get file status
- **Config**: Read/update config, list providers
- **Provider**: List, OAuth authorize/callback
- **Agents/Tools/MCP/LSP**: List and status endpoints

Authentication via `OPENCODE_SERVER_PASSWORD` (HTTP basic auth). The SDK (`@opencode-ai/sdk`) provides type-safe TypeScript client access.

## Complete CLI reference

| Command                                       | Description                                          |
| --------------------------------------------- | ---------------------------------------------------- |
| `opencode`                                    | Start TUI                                            |
| `opencode [project]`                          | Start TUI for specific directory                     |
| `opencode run [message]`                      | Non-interactive mode (all permissions auto-approved) |
| `opencode agent create\|list`                 | Manage agents                                        |
| `opencode attach [url]`                       | Attach to remote backend                             |
| `opencode auth login\|list\|logout`           | Manage provider credentials                          |
| `opencode github install\|run`                | GitHub Actions integration                           |
| `opencode mcp add\|list\|auth\|logout\|debug` | MCP server management                                |
| `opencode models [provider]`                  | List available models                                |
| `opencode serve`                              | Start headless HTTP server                           |
| `opencode session list`                       | List sessions                                        |
| `opencode stats`                              | Token usage and cost statistics                      |
| `opencode export [sessionID]`                 | Export session as JSON                               |
| `opencode import <file>`                      | Import session from JSON/URL                         |
| `opencode web`                                | Start server with web interface                      |
| `opencode acp`                                | Start ACP server via stdin/stdout                    |
| `opencode uninstall`                          | Remove OpenCode                                      |
| `opencode upgrade [version]`                  | Update to latest or specific version                 |

### Global flags

`--help`/`-h`, `--version`/`-v`, `--print-logs`, `--log-level` (DEBUG/INFO/WARN/ERROR).

### Key per-command flags

`--model`/`-m` (provider/model), `--agent`, `--continue`/`-c`, `--session`/`-s`, `--fork`, `--prompt`, `--port`, `--hostname`, `--file`/`-f` (attach files), `--format` (default/json), `--share`, `--title`.

## Formatters

OpenCode auto-formats files after write/edit operations. **22+ built-in formatters** cover Go (`gofmt`), Elixir (`mix`), JavaScript/TypeScript (`prettier`, `biome`, experimental `oxfmt`), Zig, C/C++ (`clang-format`), Kotlin (`ktlint`), Python (`ruff`, `uv`), Rust (`rustfmt`, `cargofmt`), Ruby (`rubocop`, `standardrb`), ERB (`htmlbeautifier`), R (`air`), Dart, OCaml, Terraform, Gleam, Nix, Shell (`shfmt`), and PHP (`pint`). Custom formatters use `$FILE` placeholder: `"command": ["deno", "fmt", "$FILE"]`. Disable all with `"formatter": false`.

## Environment variables

OpenCode supports **30+ standard** and **12+ experimental** environment variables. The most important ones:

- `OPENCODE_CONFIG` / `OPENCODE_TUI_CONFIG` / `OPENCODE_CONFIG_DIR` — Custom config paths
- `OPENCODE_CONFIG_CONTENT` — Inline JSON config
- `OPENCODE_PERMISSION` — Inline JSON permissions
- `OPENCODE_SERVER_PASSWORD` / `OPENCODE_SERVER_USERNAME` — HTTP auth
- `OPENCODE_DISABLE_AUTOUPDATE` — Skip update checks
- `OPENCODE_DISABLE_AUTOCOMPACT` — Disable context compaction
- `OPENCODE_DISABLE_CLAUDE_CODE` — Disable `.claude` compatibility
- `OPENCODE_ENABLE_EXA` — Enable web search tool
- `OPENCODE_EXPERIMENTAL` — Enable all experimental features
- `OPENCODE_EXPERIMENTAL_LSP_TOOL` — Enable LSP tool
- `OPENCODE_EXPERIMENTAL_BASH_DEFAULT_TIMEOUT_MS` — Bash timeout
- `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` — Max output tokens

## Project structure conventions

### `.opencode/` directory (uses plural subdirectory names)

```
.opencode/
├── agents/          # Project-specific agent markdown files
├── commands/        # Custom command markdown files
├── plugins/         # Project plugins (JS/TS)
├── skills/          # Skills (each a subfolder with SKILL.md)
├── tools/           # Custom tool definitions (JS/TS)
├── themes/          # Custom theme JSON files
└── plans/           # Plan agent output files
```

### Global config directory

```
~/.config/opencode/
├── opencode.json    # Global server/runtime config
├── tui.json         # Global TUI settings
├── AGENTS.md        # Global instructions
├── agents/          # Global agents
├── commands/        # Global commands
├── plugins/         # Global plugins
├── skills/          # Global skills
├── tools/           # Global tools
└── themes/          # Global themes
```

### Credentials and data

- `~/.local/share/opencode/auth.json` — Provider API keys
- `~/.local/share/opencode/mcp-auth.json` — MCP OAuth tokens
- `~/.cache/opencode/node_modules/` — Cached npm plugin installations
