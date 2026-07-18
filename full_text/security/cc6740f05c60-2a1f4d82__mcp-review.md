---
name: mcp-review
description: >-
  Reviews and improves existing MCP server implementations for protocol compliance,
  tool quality, Rust best practices, security, and testing coverage. Lists available
  MCP servers for selection when none specified. Use when reviewing an MCP server,
  auditing MCP tool quality, checking protocol compliance, improving MCP server code,
  or when user mentions MCP review, MCP audit, or MCP server quality.
license: MIT
metadata:
  version: 1.0.0
  author: skills project
allowed-tools: Read Edit Glob Grep AskUserQuestion Bash(cargo *) Bash(npx @modelcontextprotocol/*) Bash(python* tests/*) Bash(bash tests/*)
---

# MCP Server Reviewer

Review and improve MCP server implementations against protocol standards, Rust best practices, and production quality criteria. You'll catch issues that are easy to miss — from subtle protocol violations to security gaps.

## When to Use This Skill

- Reviewing an existing MCP server implementation for quality and protocol compliance
- Auditing MCP tool descriptions, input schemas, and error handling
- Checking Rust patterns in async MCP handlers (state management, concurrency, logging)
- Assessing MCP server security posture and test coverage before deployment

## Quick Start

When reviewing an MCP server:

1. **Pick a server** — If none specified, help identify what to review
2. **Understand the goals** — Full review or focused on specific areas?
3. **Run automated checks** — Cargo clippy, tests, build verification
4. **Analyze protocol compliance** — Initialization, capabilities, tool quality
5. **Review Rust patterns** — Async, error handling, state, logging
6. **Check security and testing** — Input validation, secrets, test coverage

## Review Workflow

### Phase 0: Server Selection

If you weren't told which server or project to review:

**Discover MCP server code in the project:**

Look for `Cargo.toml` files with `rmcp` as a dependency, or `src/main.rs` files with MCP-related imports. Don't forget to check for `.mcp.json` or MCP configuration in the project root.

```bash
# Find Cargo.toml files mentioning rmcp
grep -rl "rmcp" --include="Cargo.toml" .

# Find MCP configuration files
find . -name ".mcp.json" -o -name "mcp-config.*"
```

**Present options with AskUserQuestion:**

Build options from discovered servers. Each option's label should be the server/project name and description should summarize what it does (from README or Cargo.toml metadata).

### Phase 1: Initial Assessment

**Ask about review goals:**

Use AskUserQuestion to clarify:

- **Review scope**: Full review, or specific areas (protocol, tools, security, testing)?
- **Priority concerns**: What's most important to check?
- **Breaking changes OK**: Can we refactor, or just identify issues?
- **Deployment context**: Local tool, production service, or distributed?

**Example questions:**
```
What aspects concern you most — protocol compliance, tool quality, security, or testing?

Are you looking for a full review, or focusing on specific areas?

Can we make breaking changes to improve the server, or should we limit to non-breaking fixes?
```

### Phase 2: Automated Analysis

**Run all automated checks first:**

1. **Build verification:**
   ```bash
   cargo build 2>&1
   cargo clippy -- -W clippy::pedantic 2>&1
   ```

2. **Test suite:**
   ```bash
   cargo test 2>&1
   ```

3. **Dependency audit:**
   ```bash
   cargo audit 2>&1
   ```

4. **MCP Inspector** (if binary builds):
   ```bash
   npx @modelcontextprotocol/inspector --cli ./target/release/server-name \
     --method tools/list
   ```

Report automated results before diving into manual analysis. Don't skip straight to detailed review — it's better to surface quick wins first.

### Phase 3: Protocol Compliance Review

Check the server's MCP protocol implementation. See [references/review-checklist.md](references/review-checklist.md) for the complete checklist.

**Initialization and capabilities:**
- Does `get_info()` return correct capabilities matching actual features?
- Are there capabilities that are declared but aren't implemented (or vice versa)?
- Does the server set appropriate `protocolVersion`?
- Are server instructions provided and useful?

**Tool error handling:**
```rust
// Look for this anti-pattern: protocol errors for tool failures
Err(McpError::internal_error("file not found", None))  // BAD

// Should be:
Ok(CallToolResult::error(vec![Content::text("...")]))   // GOOD
```

**Tool quality assessment:**

For each tool, check:
- [ ] Name uses snake_case with verb + resource description
- [ ] All parameters have `schemars(description = "...")`
- [ ] Appropriate annotations (readOnlyHint, destructiveHint, etc.)
- [ ] Tool is atomic (single purpose)

**Server instructions quality:**

Check if instructions cover cross-tool workflows and operational patterns, not just repeat tool descriptions. See [references/server-design-patterns.md](references/server-design-patterns.md) for what good instructions look like.

### Phase 4: Rust Quality Review

**Logging patterns:**

```rust
// CRITICAL for stdio servers — check that stdout is clean
// Search for println!, print!, or any stdout writes
```

Verify tracing is configured with stderr writer and `with_ansi(false)`.

**Async patterns:**

Look for blocking operations in async contexts:
- `std::thread::sleep` (should be `tokio::time::sleep`)
- Blocking I/O without `spawn_blocking`
- `std::sync::Mutex` held across `.await` (should be `tokio::sync::Mutex`)
- DNS resolution or file I/O on the main runtime without offloading

**Error handling:**

- No `unwrap()` or `expect()` in production paths
- Proper `?` propagation with `From` impls or `.map_err()`
- Tool errors go through `CallToolResult::error()`, not `McpError`
- Error messages are actionable and don't leak internal details

**State management:**

- Thread-safe types (`Arc<Mutex<T>>`, `Arc<RwLock<T>>`)
- Minimal lock duration (no computation while holding lock)
- Uses `tokio::sync::Mutex` when lock spans `.await` points
- No deadlock potential from nested locks

**rmcp macro usage:**

- `#[tool_router]` on the impl block
- `#[tool_handler]` on `impl ServerHandler`
- `ToolRouter<Self>` stored in server struct
- `schemars` v1 (not v0.8) for schema generation

For the complete Rust review checklist, see [references/review-checklist.md](references/review-checklist.md).

### Phase 5: Security Review

**Input validation:**
- [ ] All tool inputs validated before processing
- [ ] Path traversal protection for file operations
- [ ] URL validation (scheme, host, no internal IPs)
- [ ] No shell command injection and size limits enforced on inputs

**Secrets management:**
- [ ] Loaded from environment (not hardcoded)
- [ ] Not logged, returned in error messages, or exposed in tool results

**Transport security (HTTP servers):**
- [ ] `Origin` header validation
- [ ] Bound to `127.0.0.1` for local (not `0.0.0.0`)
- [ ] Cryptographically secure session IDs
- [ ] TLS for remote connections

**Supply chain:**
- [ ] Dependencies pinned in `Cargo.lock`
- [ ] `cargo audit` clean, no suspicious or unmaintained dependencies

For the complete security checklist, see [references/production-hardening.md](references/production-hardening.md).

### Phase 6: Testing Coverage Review

**Check what exists:**
- [ ] Unit tests for individual tool handlers
- [ ] Integration tests using `tokio::io::duplex()` (full protocol)
- [ ] Error case coverage (invalid inputs, edge cases)
- [ ] CI pipeline configuration
- [ ] **Mutation testing** — `cargo mutants --in-diff <(git diff origin/main) --timeout-multiplier 2.0` shows zero surviving mutants on changed tool-handler code. MCP servers tend to acquire integration tests that assert on JSON-RPC envelopes without checking that the underlying tool actually did anything useful — mutation testing catches that class of theatrical test.
- [ ] **CRAP score** — `cargo crap --lcov lcov.info` shows no tool handler scoring above 30. Dispatch tables and tool routers tend to be high-cyclomatic, and the easiest to under-test by relying on a single golden-path integration test. See `.claude/rules/static-analysis.md`.

**Check what's missing:**

Compare the test suite against the tools exposed. Every tool should have at least these — if they're missing, that's a gap worth flagging:
- One happy-path unit test
- One error-case unit test
- Integration test coverage through the full protocol
- Concurrent access testing (if server is stateful)

**Verify testing patterns:**

Look for the duplex channel pattern in integration tests. If it's missing, that's a significant gap — you won't find a more effective way to test MCP protocol compliance without subprocess overhead.

For testing strategy details and code examples, see [references/testing-strategies.md](references/testing-strategies.md).

### Phase 7: Provide Feedback

**Structure feedback by priority:**

#### Critical Issues (must fix)
- Protocol violations (wrong error handling, broken initialization)
- Security vulnerabilities (injection, path traversal, leaked secrets)
- Stdout pollution in stdio servers (breaks JSON-RPC)
- Build failures or clippy errors

#### Important Issues (should fix)
- Missing tool descriptions or poor quality descriptions
- No server instructions
- `unwrap()`/`expect()` in production paths
- Missing tests for exposed tools
- Blocking operations in async code
- Poor state management patterns

#### Suggestions (nice to have)
- Better tool annotations (readOnlyHint, etc.)
- Improved server instructions
- Additional test coverage and documentation
- Performance optimizations

**Provide specific, actionable feedback:**

```
# BAD feedback
"The error handling could be better."

# GOOD feedback
"In src/tools/search.rs:45, `unwrap()` on the file read will panic if the
file doesn't exist. Change to:
  let content = fs::read_to_string(&path)
      .map_err(|e| format!("Can't read {}: {}", path.display(), e))?;
And return via CallToolResult::error() so the LLM can see the failure."
```

### Phase 8: Implementation Guidance

**After providing feedback, ask:**

Use AskUserQuestion:

```
Which issues should we prioritize?

Should I implement the fixes, or would you like to review the feedback first?

Any changes you disagree with?
```

**When implementing fixes:**

1. Start with critical issues (security, protocol violations)
2. Move to important issues (tool quality, error handling)
3. Apply suggestions if user agrees
4. Re-run `cargo clippy` and `cargo test` after each change

## Common Review Findings

These are the issues that come up most often — you'll spot them in nearly every first review:

| Finding | Frequency | Fix |
|---------|-----------|-----|
| `println!` in stdio server | Very common | Replace with `tracing::info!` to stderr |
| Protocol errors for tool failures | Very common | Use `CallToolResult::error()` instead |
| Missing tool descriptions | Common | Add `schemars(description = "...")` to all params |
| No server instructions | Common | Add `instructions` in `get_info()` |
| `unwrap()` in production paths | Common | Replace with `?` and proper error mapping |
| No integration tests | Common | Add duplex channel tests |
| Blocking in async context | Occasional | Use `tokio::task::spawn_blocking` |
| Hardcoded secrets | Occasional | Move to environment variables |

## Quality Checklist

Use this for every review:

### Protocol
- [ ] Capabilities match implementation
- [ ] Tool errors via `CallToolResult::error()` (not `McpError`)
- [ ] Server instructions present and useful
- [ ] Responds to ping, handles unknown methods

### Tools
- [ ] Snake_case names, verb + resource descriptions
- [ ] All parameters have schema descriptions
- [ ] Appropriate annotations set
- [ ] Atomic design (single purpose per tool)

### Rust
- [ ] Tracing to stderr, no stdout pollution
- [ ] No `unwrap()`/`expect()` in production paths
- [ ] Proper async patterns (no blocking)
- [ ] Thread-safe state management

### Security
- [ ] Input validation on all parameters
- [ ] No hardcoded secrets
- [ ] Path traversal protection
- [ ] HTTP Origin validation (if applicable)

### Testing
- [ ] Unit tests for each tool handler
- [ ] Integration tests with duplex channels
- [ ] Error cases covered
- [ ] Tested with MCP Inspector

## Reporting Results

**Structure your review report:**

### Assessment Summary

- Rating: Excellent / Good / Needs Work / Critical Issues
- Top 2-4 strengths and top 2-4 issues to address

### Issues by Priority

List critical, important, and suggested fixes with specific file locations and code examples.

### Next Steps

Ask which issues to prioritize and whether they'd like you to implement fixes.

## Reference Files

Detailed technical content for each review dimension:

- **Protocol fundamentals**: [references/protocol-fundamentals.md](references/protocol-fundamentals.md) — Architecture, lifecycle, JSON-RPC, all primitives
- **Server design patterns**: [references/server-design-patterns.md](references/server-design-patterns.md) — Instructions, tool descriptions, naming
- **rmcp implementation**: [references/rmcp-implementation.md](references/rmcp-implementation.md) — SDK patterns, macros, examples
- **Project and integration**: [references/project-and-integration.md](references/project-and-integration.md) — Layout, Claude Code config
- **Testing strategies**: [references/testing-strategies.md](references/testing-strategies.md) — Unit, integration, Inspector, conformance
- **Production hardening**: [references/production-hardening.md](references/production-hardening.md) — Security, logging, performance
- **Review checklist**: [references/review-checklist.md](references/review-checklist.md) — Complete quality review criteria

## Writing Style

Review reports drive decisions about code changes. Apply `natural-writing-style`:

- Categorize findings by severity (critical, important, suggested) — reviewers need to know what to fix first
- Reference specific protocol sections and `rmcp` types when citing issues
- Don't claim a server "passes review" unless you've checked every dimension; state what you examined and what you didn't
- Use contractions naturally; review output should be direct and collegial, not bureaucratic
