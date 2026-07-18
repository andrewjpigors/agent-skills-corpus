---
name: mcp-creator
description: >-
  Guides building production-quality MCP servers in Rust using the rmcp crate.
  Covers protocol design, tool implementation, testing, security hardening, and
  Claude Code integration. Use when user wants to build an MCP server, create MCP
  tools, implement MCP in Rust, add tools/resources/prompts to an MCP server, or
  start a new MCP project.
license: MIT
metadata:
  version: 1.0.0
  author: skills project
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash(cargo *) Bash(mkdir *) Bash(npx @modelcontextprotocol/*) Bash(wc *)
---

# MCP Server Creator

Build MCP servers in Rust with the official `rmcp` crate. You'll follow protocol best practices and production-quality patterns to get a working server that's easy to maintain and test.

## When to Use This Skill

- Building a new MCP server from scratch in Rust
- Adding tools, resources, or prompts to an existing MCP server
- Implementing MCP protocol features (transport, capabilities, lifecycle)
- Integrating an MCP server with Claude Code or other AI coding tools

## Quick Start

When you're asked to build an MCP server:

1. **Clarify the goal** — What tools/resources/prompts does it need? What transport? Local or remote?
2. **Design the architecture** — Pick primitives, plan state management, choose transport
3. **Build iteratively** — Scaffold, implement tools, test at each step
4. **Harden for production** — Security, logging, documentation, integration config

## Workflow

### Phase 1: Discovery

**Before writing any code, clarify these points:**

Use AskUserQuestion to gather:

- **What does this server do?** What data/services does it expose to the LLM?
- **Which primitives?** Tools (actions), resources (read-only data), prompts (templates), or a mix?
- **Transport needs?** stdio for local CLI use, Streamable HTTP for remote/multi-client, or both?
- **State requirements?** Stateless per-request, or shared state across tool calls?
- **External dependencies?** APIs, databases, filesystem access, network services?
- **Deployment target?** Local development, production service, or distributed to users?

**Example questions:**

```
What tools should this server expose? Can you describe each one's purpose and parameters?

Will this run locally via stdio, or remotely over HTTP?

Does the server need to maintain state between tool calls (e.g., a session, a database connection)?

What external services does it need to access?
```

### Phase 2: Architecture Design

Based on discovery, make these decisions:

**Primitive selection:**

| If the LLM needs to... | Use |
|------------------------|-----|
| Perform actions with side effects | Tools |
| Read structured data | Resources |
| Follow pre-defined conversation templates | Prompts |
| Request LLM completions | Sampling (client capability) |

**Transport selection:**

| Scenario | Transport | rmcp Feature Flag |
|----------|-----------|-------------------|
| Local CLI tool | stdio | `transport-io` |
| Remote service, single client | Streamable HTTP | `transport-streamable-http-server` |
| Legacy compatibility | SSE | `transport-sse-server` |
| Both local and remote | Implement both | Both flags |

**State management:**

- Stateless: No shared state needed, each tool call is independent
- Session state: `Arc<Mutex<T>>` or `Arc<RwLock<T>>` in the server struct
- Persistent: Database connection pool (e.g., `sqlx` with `Arc<Pool>`)
- Hybrid: Mix of session state and persistent storage for complex servers

**Server instructions strategy:**

Plan what goes in the `instructions` field — cross-tool workflows, operational constraints, and patterns the LLM can't infer from tool schemas alone. See [references/server-design-patterns.md](references/server-design-patterns.md) for guidance.

### Phase 3: Project Setup

**Create the project:**

```bash
cargo init my-mcp-server
cd my-mcp-server
```

**Configure `rust-toolchain.toml`** (rmcp requires nightly):

```toml
[toolchain]
channel = "nightly"
```

**Configure `Cargo.toml`:**

```toml
[dependencies]
rmcp = { version = "0.15", features = ["server", "transport-io"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
schemars = "1.0"
anyhow = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

Add transport features as needed. You'll find the complete feature flag list in [references/rmcp-implementation.md](references/rmcp-implementation.md).

**Project layout** for larger servers:

```
src/
├── main.rs          # Entry point, tracing, transport
├── server.rs        # ServerHandler impl
├── tools/
│   ├── mod.rs       # Tool router
│   └── my_tool.rs   # Individual tools
├── resources/       # Resource handlers (if needed)
├── prompts/         # Prompt definitions (if needed)
└── models.rs        # Request/response structs
```

For details and reference implementations, see [references/project-and-integration.md](references/project-and-integration.md).

### Phase 4: Implementation

**Follow this order:**

1. **Server struct** — Define with `ToolRouter<Self>` and any shared state
2. **`#[tool_router]` impl** — Add tool methods with `#[tool(description = "...")]`
3. **`#[tool_handler]` on ServerHandler** — Wire up `get_info()` with capabilities and instructions
4. **`main.rs`** — Tracing (to stderr!), transport setup, `serve().waiting()`

**Tool implementation patterns:**

Use aggregate parameters (`#[tool(aggr)]`) for tools with 2+ related params. Use individual parameters (`#[tool(param)]`) for simple ones. Every parameter needs a `#[schemars(description = "...")]` annotation — don't skip these, they're how the LLM understands your tool's inputs.

**Error handling rules:**

- Tool execution errors → `CallToolResult::error()` (LLM can see these)
- Protocol errors → `McpError::invalid_params()` etc. (opaque to LLM)
- Never `unwrap()` or `expect()` in production code paths
- Return actionable error messages — "File not found: config.toml" beats "internal error"

**Critical: stdout is sacred.** For stdio servers, don't write anything to stdout except JSON-RPC messages. All logging goes through `tracing` with a stderr writer.

For complete code examples and the macro system, see [references/rmcp-implementation.md](references/rmcp-implementation.md).

### Phase 5: Testing

Build tests from the bottom up:

**Unit tests** — Call tool methods directly:
```rust
#[tokio::test]
async fn test_my_tool() {
    let server = MyServer::new();
    let result = server.my_tool("input".into()).await.unwrap();
    assert!(!result.is_error);
}
```

**Integration tests** — Full protocol via duplex channels:
```rust
let (client_read, server_write) = tokio::io::duplex(4096);
let (server_read, client_write) = tokio::io::duplex(4096);
// Start server, connect client, test tool listing and calling
```

**MCP Inspector** — Interactive and CI validation:
```bash
npx @modelcontextprotocol/inspector ./target/release/my-mcp-server
npx @modelcontextprotocol/inspector --cli ./target/release/my-mcp-server --method tools/list
```

**Claude Code testing:**
```bash
claude mcp add --transport stdio my-server ./target/release/my-mcp-server
claude --mcp-debug
```

**opencode testing:** register the server in `opencode.json` under `mcp`
instead — there's no equivalent `add` subcommand:
```json
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["./target/release/my-mcp-server"],
      "enabled": true
    }
  }
}
```
See [opencode.ai/docs/mcp-servers](https://opencode.ai/docs/mcp-servers/).

For the complete testing guide with code examples, see [references/testing-strategies.md](references/testing-strategies.md).

### Phase 6: Production Readiness

Before shipping:

**Security hardening:**
- Validate all tool inputs (paths, URLs, commands)
- Load secrets from environment variables
- For HTTP: validate `Origin` headers, bind to `127.0.0.1`
- Use cryptographically secure session IDs for HTTP transport

**Documentation:**
- Tool descriptions with format specs and constraints
- Server instructions for cross-tool workflows
- README with tools, env vars, and configuration examples
- Error messages that are actionable, not cryptic

**Claude Code integration:**
- Create `.mcp.json` for project-scoped config with `${VAR}` syntax for env expansion
- Test discovery and connection flow end-to-end

For the complete security checklist and production patterns, see [references/production-hardening.md](references/production-hardening.md).

### Phase 7: Validation

**Run through this checklist before considering the server complete:**

#### Protocol Compliance
- [ ] Initialization handshake works correctly
- [ ] Capabilities match actual features
- [ ] Tool errors use `isError: true` (not protocol errors)
- [ ] Responds to `ping` and handles unknown methods gracefully

#### Tool Quality
- [ ] Snake_case naming with verb + resource descriptions
- [ ] All parameters have schema descriptions
- [ ] Appropriate annotations (readOnlyHint, destructiveHint)
- [ ] Each tool is atomic (single purpose)

#### Rust Quality
- [ ] `cargo clippy -- -W clippy::pedantic` passes
- [ ] No `unwrap()` or `expect()` in production paths
- [ ] Tracing to stderr (never println to stdout)
- [ ] Thread-safe state management with proper async patterns (no blocking)

#### Security
- [ ] Input validation on all tool parameters
- [ ] No hardcoded secrets
- [ ] Path traversal protection for file operations
- [ ] HTTP Origin validation (if applicable)

#### Testing
- [ ] Unit tests for each tool
- [ ] Integration tests with duplex channels
- [ ] Tested with MCP Inspector
- [ ] Tested in Claude Code

#### Documentation
- [ ] Server instructions written
- [ ] Tool descriptions complete
- [ ] README with setup instructions
- [ ] `.mcp.json` example provided

For the complete review checklist, see [references/review-checklist.md](references/review-checklist.md).

## Anti-Patterns

**Don't write to stdout:**
```rust
// BAD — breaks JSON-RPC framing
println!("Processing...");

// GOOD — use tracing to stderr
tracing::info!("Processing...");
```

**Don't use protocol errors for tool failures:**
```rust
// BAD — LLM can't see this error
Err(McpError::internal_error("file not found", None))

// GOOD — LLM can reason about this
Ok(CallToolResult::error(vec![Content::text("File not found: config.toml")]))
```

**Don't build kitchen-sink servers:**
```
// BAD — 50+ tools, huge token overhead
Server with: read_file, write_file, delete_file, list_files,
             search_files, watch_files, compress_files, ...

// GOOD — focused server, clear purpose
Server with: analyze_query, explain_plan, suggest_index, list_tables
```

**Don't skip server instructions:**
```rust
// BAD — no guidance for the LLM
instructions: None,

// GOOD — tells the LLM how to use tools together
instructions: Some("Call 'list_tables' first to discover available tables. \
    Then use 'analyze_query' with a SQL query to get performance insights. \
    Use 'suggest_index' to get optimization recommendations.".to_string()),
```

## Reference Files

Detailed technical content for each aspect of MCP server development:

- **Protocol fundamentals**: [references/protocol-fundamentals.md](references/protocol-fundamentals.md) — Architecture, lifecycle, JSON-RPC, all primitives, transports
- **Server design patterns**: [references/server-design-patterns.md](references/server-design-patterns.md) — Instructions, tool descriptions, naming, hooks
- **rmcp implementation**: [references/rmcp-implementation.md](references/rmcp-implementation.md) — SDK installation, macros, complete examples, error handling
- **Project and integration**: [references/project-and-integration.md](references/project-and-integration.md) — Layout, reference implementations, Claude Code config
- **Testing strategies**: [references/testing-strategies.md](references/testing-strategies.md) — Unit, integration, Inspector, conformance testing
- **Production hardening**: [references/production-hardening.md](references/production-hardening.md) — Security, logging, performance, versioning
- **Review checklist**: [references/review-checklist.md](references/review-checklist.md) — Complete quality review criteria

## Writing Style

MCP server documentation helps developers build and integrate tools. Apply `natural-writing-style`:

- Reference specific `rmcp` types, traits, and macros by name — not vague "SDK features"
- Don't claim a server is "production-ready" without listing what was tested (transport, error paths, concurrent access)
- Be specific about protocol requirements vs. nice-to-haves; the MCP spec has mandatory and optional parts
- Use contractions naturally; implementation guides should feel like pairing with someone who knows the SDK
