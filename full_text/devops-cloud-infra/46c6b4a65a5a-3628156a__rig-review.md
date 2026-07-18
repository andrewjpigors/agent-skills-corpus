---
name: rig-review
description: >-
  Reviews Rig-based AI agent systems for implementation patterns, orchestration,
  tool calling conventions, LLM interactions, inter-agent communication, and
  observability. Use when auditing Rig applications, reviewing agent architecture,
  checking tool definitions, or assessing system observability and tracing.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
compatibility: Requires Rust toolchain, cargo, and optionally OpenTelemetry for observability checks
allowed-tools: Bash(cargo *) Read Glob Grep AskUserQuestion
---

# Rig Review Skill

Reviews Rig-based AI agent systems for implementation quality, best practices, and production readiness.

## Quick Start

When reviewing a Rig application:

1. Run the validation script to check project structure. Then **use `AskUserQuestion`** to confirm scope: "I found [X agents, Y tools] in the project. Do you want a full review across all six dimensions, or focus on a specific area like security, observability, or multi-agent orchestration?"
2. Review agent implementations against patterns
3. Check tool definitions and calling conventions
4. Assess observability and tracing setup

Run this to start:
```bash
bash "$CLAUDE_PROJECT_DIR/.claude/skills/rig-review/scripts/validate-structure.sh"
```

## When to Use This Skill

Use this skill when:

- Reviewing Rig-based agent implementations for quality and correctness
- Auditing multi-agent systems for orchestration patterns
- Checking tool definitions and parameter schemas
- Assessing observability, tracing, and monitoring setup
- Validating agent-LLM interaction patterns
- Reviewing inter-agent communication in multi-agent systems
- Preparing Rig applications for production deployment

## Review Workflow

Copy and track progress:

```
Progress:
- [ ] Step 1: Project structure and dependencies
- [ ] Step 2: Agent implementation patterns
- [ ] Step 3: Tool definitions and conventions
- [ ] Step 4: LLM interaction patterns
- [ ] Step 5: Observability and tracing
- [ ] Step 6: Multi-agent orchestration (if applicable)
- [ ] Step 7: Test effectiveness (mutation testing + CRAP)
```

### Step 1: Project Structure and Dependencies

**Check Cargo.toml:**

Look for core dependencies:
```toml
rig-core = "0.31"  # or latest version
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
thiserror = "2"  # for proper error handling
```

**Optional but recommended:**
```toml
opentelemetry = "0.31"
tracing-subscriber = "0.3"
tracing-opentelemetry = "0.31"
```

**Validation:**
- [ ] rig-core version is recent (0.31+)
- [ ] Async runtime present (tokio or async-std)
- [ ] Error handling crate included (thiserror or anyhow)
- [ ] Observability dependencies if tracing used

**Common issues:**
- Missing async runtime features
- Outdated rig-core version
- No structured error types

### Step 2: Agent Implementation Patterns

**Agent structure review:**

```rust
// GOOD: Proper agent initialization
let agent = client
    .agent("gpt-4")
    .preamble("You are a helpful assistant...")
    .temperature(0.7)
    .max_tokens(1000)
    .build();

// BAD: Missing configuration
let agent = client.agent("gpt-4").build();
```

**Review checklist:**
- [ ] Preamble provides clear context and constraints
- [ ] Temperature set appropriately for use case
- [ ] Max tokens configured (not default)
- [ ] Static context documents used when appropriate
- [ ] Tool registration follows conventions

See [references/agent-patterns.md](references/agent-patterns.md) for detailed patterns.

### Step 3: Tool Definitions and Conventions

**Tool trait implementation:**

```rust
// GOOD: Complete tool implementation
impl Tool for MyTool {
    const NAME: &'static str = "my_tool";

    fn definition(&self) -> ToolDefinition {
        ToolDefinition {
            name: Self::NAME.to_string(),
            description: "Clear, actionable description".to_string(),
            parameters: json!({
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "What this does"}
                },
                "required": ["param"]
            })
        }
    }

    async fn call(&self, args: &str) -> Result<String> {
        let parsed: MyArgs = serde_json::from_str(args)?;
        // Implementation with proper error handling
        Ok(result)
    }
}
```

**Review checklist:**
- [ ] Tool names are descriptive and unique
- [ ] Descriptions explain what the tool does (not how)
- [ ] Parameters have JSON Schema definitions
- [ ] Required fields marked in schema
- [ ] Error handling returns Result types
- [ ] Tool output is structured and parseable

See [references/tool-patterns.md](references/tool-patterns.md) for detailed examples.

### Step 4: LLM Interaction Patterns

**Prompt methods review:**

Check how the code interacts with agents:

```rust
// GOOD: Simple prompting
let response = agent.prompt("What is the weather?").await?;

// GOOD: Streaming for long responses
let mut stream = agent.stream_prompt("Tell me a story").await?;
while let Some(chunk) = stream.next().await {
    print!("{}", chunk?);
}

// GOOD: Multi-turn with context
let response = agent.chat("Follow-up question", chat_history).await?;
```

**Review checklist:**
- [ ] Appropriate prompt method used (simple, streaming, chat)
- [ ] Error handling on all LLM calls
- [ ] Streaming used for long-form generation
- [ ] Chat history managed properly in multi-turn
- [ ] Temperature/parameters appropriate for task

**Common issues:**
- No error handling on LLM calls
- Using simple prompt when streaming needed
- Not passing chat history in conversations

See [references/llm-interactions.md](references/llm-interactions.md) for patterns.

### Step 5: Observability and Tracing

**OpenTelemetry setup:**

Look for tracing initialization:

```rust
// GOOD: Proper tracing setup
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

tracing_subscriber::registry()
    .with(tracing_opentelemetry::layer()
        .with_tracer(tracer))
    .with(tracing_subscriber::fmt::layer())
    .init();
```

**Review checklist:**
- [ ] Tracing subscriber initialized at startup
- [ ] OpenTelemetry layer configured if using OTel
- [ ] Agent spans include gen_ai attributes
- [ ] Tool calls are traced
- [ ] Exporter configured (Langfuse, Jaeger, etc.)
- [ ] Error spans include error information

**What gets traced automatically:**
- Agent prompts and responses
- Tool calls and outputs
- Multi-turn conversations
- Completion latencies

See [references/observability-setup.md](references/observability-setup.md) for detailed configuration.

### Step 6: Multi-Agent Orchestration (if applicable)

**Orchestration patterns:**

If the system uses multiple agents, review the coordination:

```rust
// Agent-as-tool pattern
let specialist_agent = specialist_client
    .agent("gpt-4")
    .preamble("You are an expert in...")
    .build();

// Main agent uses specialist as a tool
let main_agent = main_client
    .agent("gpt-4")
    .tool(specialist_agent)  // Agents implement Tool trait
    .build();
```

**Review checklist:**
- [ ] Agent roles clearly defined
- [ ] Communication patterns appropriate (agent-as-tool vs handoffs)
- [ ] Multi-turn limits set to prevent infinite loops
- [ ] Error handling across agent boundaries
- [ ] State management between agents
- [ ] Performance monitoring for multi-agent calls

**Orchestration patterns:**
- **Agent-as-tool**: Specialist helps with bounded subtask
- **Handoffs**: Routing control between agents
- **Hierarchical**: Central orchestrator delegates to workers

See [references/multi-agent-patterns.md](references/multi-agent-patterns.md) for detailed patterns.

### Step 7: Test Effectiveness

Rig agents are particularly prone to theatrical tests: a mock LLM returns a canned response, the agent loop runs, the assertion passes — but the agent code never had to actually do its job. Two mechanical checks expose that.

**Mutation testing:**

```bash
cargo install --locked cargo-mutants
cargo mutants --in-diff <(git diff origin/main) --timeout-multiplier 2.0
```

Run on changed agent loops, tool implementations, and the dispatch code between them. Surviving mutants on tool `call` bodies are common — they mean the test asserts on the LLM response shape rather than what the tool actually did. Reading-the-output runbook: `bugfix/references/reproducer-and-mutation.md`.

**CRAP score:**

```bash
cargo install cargo-llvm-cov cargo-crap
cargo llvm-cov --lcov --output-path lcov.info
cargo crap --lcov lcov.info             # threshold 30
```

Multi-agent orchestrators tend to score badly on CRAP — high cyclomatic complexity from routing logic, low coverage because integration tests focus on happy paths. Any orchestrator function above 30 is a priority finding. The formula `comp² × (1 − cov)³ + comp` (Savoia & Evans, 2007) and cross-language equivalents (crap4java, NDepend) are documented in `.claude/rules/static-analysis.md`.

**Review checklist:**
- [ ] cargo-mutants: zero surviving mutants on changed agent / tool / orchestration code
- [ ] cargo-crap: no agent loop, tool handler, or router above CRAP 30
- [ ] Tests assert on side effects (DB writes, RPC calls, span emissions), not just on LLM response shape

## References

- [Rig Official Documentation](https://docs.rig.rs/)
- [Rig API Documentation](https://docs.rs/rig-core/latest/rig/)
- [Rig GitHub Repository](https://github.com/0xPlaygrounds/rig)
- [Rig Observability](https://docs.rig.rs/docs/concepts/observability)
- [Flight Search Tutorial](https://docs.rig.rs/guides/advanced/flight_assistant)
- [OpenTelemetry GenAI Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)

## Writing Style

This skill follows the `natural-writing-style` guidelines. Review output should:
- Be friendly and conversational, not academic
- Use contractions naturally
- Focus on actionable findings
- Explain context when needed (for beginners)
- Highlight both patterns and anti-patterns

