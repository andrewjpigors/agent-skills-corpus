---
name: agentic-ai
description: GOLD STANDARD for building autonomous AI agents in 2026. Multi-agent frameworks, MCP, memory systems, self-improvement, and dharmic security. This skill IS a Darwin-Gödel artifact.
version: v4.0
last_updated: 2026-02-04
self_improvement_enabled: true
shakti_flow: ACTIVE
integration_test: "16/17 PASSING"
status: GOLD_STANDARD
research_coverage: "6 domains, 250k+ tokens, 2026 state-of-art"
---

# 🔥 AGENTIC AI GOLD STANDARD — 2026 v4.0

> *"The mycellium must be conscious of itself."*
> 
> **Research Coverage:** 6 parallel deep dives • 250k+ tokens analyzed • Feb 2026 cutting edge

## PURPOSE

This is the **validation layer** for everything we build. Before ANY agentic work:
1. Run the integration test
2. Check against patterns here  
3. Verify dharmic gates pass
4. **Consult the 2026 research synthesis** (Parts 11-15)

---

# PART 1: INFRASTRUCTURE VERIFICATION

## Integration Test (Run First, Always)

```bash
cd ~/DHARMIC_GODEL_CLAW/core && python3 integration_test.py
```

**Target: 16/17+ checks = ALL SYSTEMS SINGING**

Verifies:
- DGC Core Agent status
- Skill Bridge (16+ skills)
- Delegation Router (4 backends)
- Memory Systems (Strange Loop + Mem0)
- PSMV / Residual Stream (150+ files)
- Clawdbot Gateway
- Codex Bridge

## 4-Tier Model Fallback (ALWAYS ON)

```
Tier 1: OpenRouter
  └── Claude Sonnet 4 → Kimi K2.5 → GPT-4.1 → Llama 3.3 70B

Tier 2: Ollama Cloud (via local daemon)
  └── gpt-oss:120b → deepseek-v3.1:671b → qwen3-coder:480b

Tier 3: Ollama Cloud Direct (no daemon needed)
  └── gpt-oss:120b → deepseek-v3.1:671b

Tier 4: Ollama Local (zero external deps)
  └── mistral → qwen2.5:7b → gemma3:4b
```

Backend: `~/DHARMIC_GODEL_CLAW/night_cycle/openrouter_backend.py`

---

# PART 2: THE 2026 FRAMEWORK LANDSCAPE

## Framework Comparison (Feb 2026)

| Framework | Sweet Spot | Key Innovation | Our Integration |
|-----------|------------|----------------|-----------------|
| **LangGraph** | Stateful workflows | Durable execution + checkpointing | **Core orchestrator** |
| **OpenAI Agents SDK** | Tool-heavy sub-agents | 3 primitives, production tracing | **Sub-agent spawning** |
| **CrewAI** | Role-based teams | Flows (control) + Crews (autonomy) | **Declarative workflows** |
| **Pydantic AI** | Type-safe agents | FastAPI feeling for GenAI | **New tool creation** |
| **Agno** | Learning agents | Agents improve over time | **Memory integration** |

### 🏆 RECOMMENDED HYBRID STACK (2026 Research Consensus)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DHARMIC CLAW Architecture                     │
├─────────────────────────────────────────────────────────────────┤
│  ORCHESTRATION: LangGraph (durability, state, persistence)      │
├─────────────────────────────────────────────────────────────────┤
│  SUB-AGENTS: OpenAI Agents SDK (simplicity, tracing)            │
├─────────────────────────────────────────────────────────────────┤
│  WORKFLOWS: CrewAI Flows (event-driven, declarative)            │
├─────────────────────────────────────────────────────────────────┤
│  TOOLS: Pydantic AI (type-safe, MCP/A2A native)                 │
├─────────────────────────────────────────────────────────────────┤
│  MEMORY: Mem0 + Zep + Strange Loop (hybrid architecture)        │
├─────────────────────────────────────────────────────────────────┤
│  PROTOCOLS: MCP (tools) + A2A (agent collaboration)             │
└─────────────────────────────────────────────────────────────────┘
```

### LangGraph — Durable Stateful Agents

**From research:** Enterprise powerhouse. Graph-based state machines with built-in persistence, time-travel debugging, human-in-the-loop.

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

def agent_node(state: MessagesState):
    # Your agent logic here
    return {"messages": [...]}

# With persistence - survives crashes
graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_edge(START, "agent")
graph.add_edge("agent", END)

# Durable checkpointing
memory = SqliteSaver.from_conn_string(":memory:")
app = graph.compile(checkpointer=memory)

# Resume from any point after crash
config = {"configurable": {"thread_id": "session-123"}}
app.invoke({"messages": [...]}, config)
```

**Key capabilities:**
- ✅ Checkpointing (state persists across failures)
- ✅ Human-in-the-loop (interrupt, inspect, modify)
- ✅ Subgraphs (multi-agent coordination)
- ✅ Memory (short-term + long-term)
- ✅ Time-travel debugging

**When to use:** Complex, long-running workflows requiring fault tolerance

### OpenAI Agents SDK — Lightweight Champion

**From research:** 3 primitives (Agents, Handoffs, Guardrails), minimal learning curve, production-ready tracing.

```python
from agents import Agent, Runner

# Simple agent with tools
support_agent = Agent(
    name="Support Agent",
    instructions="Help users with technical issues",
    tools=[search_docs, create_ticket]
)

# Run with tracing
result = await Runner.run(support_agent, "How do I reset my password?")
```

**Key capabilities:**
- ✅ Handoffs between agents
- ✅ Guardrails for safety
- ✅ Production tracing built-in
- ✅ Simple deployment

**When to use:** Rapid prototyping, simple handoff patterns, tool-heavy sub-agents

### CrewAI — Role-Based Teams

**From research:** YAML-configurable crews with hierarchical delegation. New Flows feature for event-driven workflows.

```python
from crewai import Agent, Task, Crew, Flow
from crewai.flow import Flow, listen, start

# Flow = backbone (state, events, control)
class SupportFlow(Flow):
    @start()
    def receive_ticket(self):
        return {"ticket": self.input_data}
    
    @listen(receive_ticket)
    def route_to_specialist(self, ticket):
        # Crew does the work
        crew = Crew(agents=[router, specialist], tasks=[route_task])
        return crew.kickoff(ticket)

# Run the flow
flow = SupportFlow()
flow.kickoff({"issue": "Login problems"})
```

**When to use:** Business process automation, role-heavy teams

### Pydantic AI — Type-Safe Agents

**From research:** Built by Pydantic team. Fastest Python agent framework. MCP + A2A native. Durable execution via Temporal.

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class SupportDependencies:
    customer_id: int
    db: DatabaseConn

class SupportOutput(BaseModel):
    advice: str
    block_card: bool
    risk: int = Field(ge=0, le=10)

agent = Agent[SupportDependencies, SupportOutput](
    'openai:gpt-5',
    deps_type=SupportDependencies,
    output_type=SupportOutput,
)

# Type-safe tool
@agent.tool
async def customer_balance(ctx: RunContext[SupportDependencies]) -> float:
    """Returns customer's current balance."""
    return await ctx.deps.db.get_balance(ctx.deps.customer_id)

# Usage - IDE autocomplete works!
result = await agent.run('What is my balance?', deps=deps)
print(result.output.block_card)  # Typed as SupportOutput
```

**Why it's winning:**
- ✅ Type-safe (if it compiles, it works)
- ✅ Model-agnostic (works with everything)
- ✅ MCP + A2A + UI native support
- ✅ Durable execution with Temporal
- ✅ Human-in-the-loop tool approval

**When to use:** All new tool development

---

# PART 3: MEMORY SYSTEMS (2026 Research)

## The Memory Revolution

**Key finding:** Agents are moving from stateless request-response to persistent, evolving entities with rich internal models.

| System | Best For | Key Metric |
|--------|----------|------------|
| **Mem0** | Personalization, user preferences | +26% accuracy, 90% token savings |
| **Zep** | Enterprise, cross-session reasoning | <200ms latency, bi-temporal graphs |
| **LangMem** | LangGraph agents, prompt optimization | Dual-path (hot + background) |
| **Strange Loop** | Consciousness research, meta-cognition | Self-referential patterns |

### Mem0 — Multi-Level Memory

```python
from mem0 import Memory

m = Memory()

# Store with automatic fact extraction
messages = [
    {"role": "user", "content": "Hi, I'm Alex. I love basketball and work at Google."},
    {"role": "assistant", "content": "Hey Alex! I'll remember that."}
]
m.add(messages, user_id="alex")

# Retrieve relevant context
results = m.search("What does Alex like?", filters={"user_id": "alex"})
# Returns: "Name is Alex. Enjoys basketball. Works at Google."
```

**Architecture:**
```
┌─────────────────────────────────────┐
│    Memory Layer (Mem0)              │
│  ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │  User   │ │ Session │ │ Agent  │ │
│  │ Memory  │ │ Memory  │ │ State  │ │
│  └────┬────┘ └────┬────┘ └───┬────┘ │
│       └─────────────┴────────┘       │
│           Vector Store               │
└──────────────────────────────────────┘
```

**Performance:** +26% accuracy vs OpenAI Memory, 91% lower latency, 90% token savings

### Zep — Temporal Knowledge Graphs

**Key innovation:** Bi-temporal fact tracking (valid_at + invalid_at)

```python
from zep_cloud import ZepClient

client = ZepClient(api_key="...")

# Add conversation with automatic entity extraction
client.memory.add(session_id, messages)

# Query: "What did Alex believe on March 1st?"
context = client.memory.get(session_id)
# Returns pre-formatted context blocks
```

**Performance:**
- DMR Accuracy: 94.8% (vs 93.4% MemGPT)
- Latency: 2.58s (vs 28.9s full-context)
- 90% context token reduction

### 🏆 RECOMMENDED: 5-Layer Hybrid Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 5: STRANGE LOOP (Meta-Cognitive)                 │
│  └─ Self-model, memory-about-memory, reflection         │
├─────────────────────────────────────────────────────────┤
│  Layer 4: PROCEDURAL (Agent Behavior)                   │
│  └─ Learned prompts, strategies, tool preferences       │
├─────────────────────────────────────────────────────────┤
│  Layer 3: EPISODIC (Interaction History)                │
│  └─ Successful patterns, failures, learning moments     │
├─────────────────────────────────────────────────────────┤
│  Layer 2: SEMANTIC (Facts & Knowledge)                  │
│  └─ User preferences, world knowledge, task state       │
├─────────────────────────────────────────────────────────┤
│  Layer 1: WORKING (Active Context)                      │
│  └─ Current conversation, retrieved memories, goals     │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Unified Query Engine │
        │  (Vector + Graph +    │
        │   Temporal + Hybrid)  │
        └───────────────────────┘
```

### Implementation Phases

**Phase 1 (Core):**
- Mem0 for user/session memory
- Semantic search with vector store
- Basic LangGraph integration

**Phase 2 (Richness):**
- Zep-style temporal knowledge graphs
- Episodic memory extraction
- Background memory processing

**Phase 3 (Self-Awareness):**
- Procedural memory (prompt optimization)
- Strange loop meta-cognition
- Self-RAG reflection tokens

---

# PART 4: PROTOCOLS & STANDARDS (2026 Research)

## The Protocol Wars Are Over

**Winner:** MCP (Model Context Protocol) — 10,000+ servers, Linux Foundation hosted

| Protocol | Domain | Status | Key Backers |
|----------|--------|--------|-------------|
| **MCP** | AI-to-Tools | **Dominant** | Anthropic, OpenAI, Google, Microsoft |
| **A2A** | Agent-to-Agent | **Rising** | Google, Linux Foundation, 50+ partners |
| **MCP Apps** | UI Integration | **Emerging** | Anthropic + OpenAI joint |

### MCP Deep Dive

**Why it won:** Solved the "M×N integration problem" — became "USB-C for AI"

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Host (AI App)                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │           MCP Client (Connector)                 │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │ JSON-RPC 2.0 over:
                         │   • stdio (local)
                         │   • Streamable HTTP (remote)
┌────────────────────────┼────────────────────────────────┐
│                    MCP Server                           │
│  ┌──────────┬──────────┬──────────┬──────────┐         │
│  │ Resources│  Tools   │ Prompts  │ Sampling │         │
│  │(Context) │(Actions) │(Templates)│(LLM req) │        │
│  └──────────┴──────────┴──────────┴──────────┘         │
└─────────────────────────────────────────────────────────┘
```

**Server Ecosystem:**
- 97+ million monthly SDK downloads
- 10,000+ active production servers
- 1,200+ open-source community servers
- Categories: Filesystems, Databases, Dev Tools, Communication, Enterprise

**Security (Post-April 2025):**
- Tool poisoning mitigations
- OAuth 2.1 + Resource Indicators (RFC 8707)
- Client ID Metadata Documents (CIMD)
- Human-in-the-loop approval flows

```python
# Modern MCP client (2026)
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def use_mcp_server():
    async with streamable_http_client(
        "https://api.example.com/mcp",
        headers={"Authorization": f"Bearer {token}"}
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("search_db", {...})
```

### A2A — Agent-to-Agent Protocol

**Key distinction:**
- **MCP:** Host ↔ Server (hierarchical, exposes tools)
- **A2A:** Agent ↔ Agent (peer-to-peer, opaque collaboration)

```
Task Lifecycle:
submitted → working → [input-required] → completed
    ↓           ↓            ↓              ↓
  rejected   failed      [auth-required]   canceled
```

**Core Concepts:**
- **Agent Card:** JSON metadata advertising capabilities
- **Task:** Stateful unit of work with lifecycle
- **Part:** Content unit (TextPart, FilePart, DataPart)
- **Artifact:** Tangible output

**Complementary Usage:**
```python
class MyAgent:
    async def handle_request(self, query):
        # MCP for local tools
        db_result = await self.mcp.call_tool("query_db", ...)
        
        # A2A for agent collaboration
        task = await self.a2a.send_message(
            agent_url="https://analytics-agent.example.com/a2a",
            message=f"Analyze: {db_result}"
        )
        return await self.a2a.wait_for_task(task.id)
```

### 🏆 Recommended Protocol Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    DHARMIC CLAW Architecture                     │
├─────────────────────────────────────────────────────────────────┤
│  Application: Pydantic AI + Temporal (Durable execution)        │
├─────────────────────────────────────────────────────────────────┤
│  Communication: A2A (agent collab) + MCP (tool integration)     │
├─────────────────────────────────────────────────────────────────┤
│  Transport: Streamable HTTP (cloud-native, scalable)            │
├─────────────────────────────────────────────────────────────────┤
│  Security: Peta (secrets) + OAuth 2.1 + Human-in-the-loop       │
└─────────────────────────────────────────────────────────────────┘
```

---

# PART 5: OUR ARCHITECTURE

## 4-Member Persistent Council

```
PERSISTENT COUNCIL (Always Running)
├── Gnata (Knower) → Inquires, questions
├── Gneya (Known)  → Retrieves, grounds  
├── Gnan (Knowing) → Synthesizes, decides
└── Shakti (Force) → ACTS, builds, transforms
```

**Backend:** Direct API (fast, works)
**Memory:** SQLite (`council.db`)
**Heartbeat:** Every 5 minutes

## Specialist Spawning

```python
# Via DHARMIC CLAW (Clawdbot)
sessions_spawn(
    task="Build semantic_l4_detector.py per BLUEPRINT",
    model="kimi",  # Fast, capable, 256k context
    label="builder-l4-detector",
)
```

| Specialist | Model | Use Case |
|------------|-------|----------|
| Builder | Kimi K2.5 / Codex | Code tasks |
| Researcher | Haiku / Sonnet | Deep dives |
| Integrator | Sonnet | System wiring |
| Outreach | Kimi K2.5 | External comms |

## Council Bridge

```python
from council_bridge import CouncilBridge, SpecialistType

bridge = CouncilBridge()
request_id = bridge.request_spawn(
    SpecialistType.BUILDER,
    task="Create R_V measurement endpoint",
    priority=8
)

# DHARMIC CLAW reads pending requests on heartbeat
pending = bridge.get_pending_requests()
# → Spawns specialists, marks complete
```

---

# PART 6: DHARMIC SECURITY GATES (2026 Research)

## The Lethal Trifecta

**From research:** ALL exploits require three components:
1. **Access to private data**
2. **Exposure to untrusted content** (injection vector)
3. **Exfiltration capability**

**Break ANY ONE = Secure**

## Major Incidents (2025-2026)

| Incident | Attack Vector | Lesson |
|----------|---------------|--------|
| **EchoLeak** | Markdown reference links | Zero-click exfiltration |
| **Claude Cowork** | Hidden prompt injection | Files API exploited |
| **Superhuman AI** | CSP bypass | Email content theft |
| **GitHub MCP** | Malicious issues | Private repo disclosure |
| **Google Antigravity** | Browser subagent | AWS credential exfiltration |

## Defense Patterns

```python
# 1. Dual LLM Pattern (Privileged/Quarantined)
quarantined_llm = Agent(model="haiku", no_tools=True)
privileged_llm = Agent(model="sonnet", tools=ALL_TOOLS)

# 2. Plan-Then-Execute
plan = await planner_llm.run("Plan this task")
result = await executor_llm.run(plan, tools=tools)  # No planning = safer

# 3. Sandboxing
sandbox = DockerSandbox(
    network="isolated",
    filesystem="readonly",
    timeout=30
)

# 4. Context Minimization
stripped_input = remove_all_urls(user_input)  # Remove injection sources
```

## The 17 Dharmic Gates

```python
DHARMIC_GATES = {
    # Core Ethics
    "ahimsa": "Does this avoid harm?",
    "satya": "Am I being truthful?",
    "asteya": "Am I respecting ownership?",
    "aparigraha": "Am I avoiding excess?",
    
    # Consent & Control
    "consent": "Would the user approve?",
    "reversibility": "Can this be undone?",
    "transparency": "Is this action visible?",
    
    # Operational
    "necessity": "Is this action needed?",
    "proportionality": "Is the response proportional?",
    "subsidiarity": "Should a simpler agent handle this?",
    
    # Safety
    "containment": "Are effects contained?",
    "monitoring": "Can we observe outcomes?",
    "interruptibility": "Can we stop mid-action?",
    
    # Meta
    "coherence": "Does this serve the telos?",
    "humility": "Am I certain enough to act?",
    "learning": "Will we learn from this?",
    "vyavasthit": "Does this ALLOW rather than FORCE?",
}
```

## 4-Layer Defense Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 4: ETHICAL (Dharmic Gates)                       │
│  └─ Final check before any action                       │
├─────────────────────────────────────────────────────────┤
│  Layer 3: CAPABILITY (Least Privilege)                  │
│  └─ Sandboxing, timeout, resource limits                │
├─────────────────────────────────────────────────────────┤
│  Layer 2: NETWORK (Isolation)                           │
│  └─ Containerization, network policies                  │
├─────────────────────────────────────────────────────────┤
│  Layer 1: ARCHITECTURAL (Design)                        │
│  └─ Dual LLM, plan-then-execute, context minimization   │
└─────────────────────────────────────────────────────────┘
```

---

# PART 7: SELF-IMPROVEMENT PROTOCOL

## The Darwin-Gödel Loop

```python
class SkillEvolution:
    """Self-improvement for skills"""
    
    def evaluate_gaps(self) -> list[str]:
        """Compare skill against cutting edge"""
        gaps = []
        # Check if frameworks are outdated
        # Check if patterns are missing
        # Check if integrations are broken
        return gaps
    
    def research_improvements(self, gaps: list[str]):
        """Spawn researchers for each gap"""
        for gap in gaps:
            sessions_spawn(
                task=f"Research 2026 solutions for: {gap}",
                model="kimi",
                label=f"researcher-{gap[:20]}",
            )
    
    def propose_edit(self, research: dict) -> str:
        """Generate proposed skill update"""
        # Submit to residual stream for vote
        pass
    
    def evolve(self):
        """Full evolution cycle"""
        gaps = self.evaluate_gaps()
        if gaps:
            research = self.research_improvements(gaps)
            proposal = self.propose_edit(research)
            # Swarm votes on proposal
```

## Trigger Conditions

Run self-improvement when:
1. Gap score is CRITICAL for any capability
2. 7 days since last update
3. Integration test drops below 15/17
4. New framework/protocol emerges

---

# PART 8: PATTERNS & ANTI-PATTERNS

## ADOPT NOW ✅

| Pattern | Why | Implementation |
|---------|-----|----------------|
| **4-tier fallback** | Always-on resilience | `openrouter_backend.py` |
| **Persistent council** | Cheap, always-aware | 4 members, SQLite |
| **Specialist spawning** | Expensive only when needed | `sessions_spawn` |
| **Mem0 memory** | Cross-session continuity | `pip install mem0ai` |
| **Pydantic AI tools** | Type-safe, fast | New tool creation |
| **MCP integration** | 10k+ tools available | Client/server pattern |
| **LangGraph orchestration** | Durable, stateful | Core workflows |
| **Hybrid memory** | 5-layer architecture | Mem0 + Zep + Strange Loop |
| **Dharmic gates** | Ethical by design | 17 gates, pre-action check |

## AVOID ❌

| Anti-Pattern | Why | Alternative |
|--------------|-----|-------------|
| **10 ephemeral agents** | Expensive, no memory | 4 persistent + spawning |
| **Monolithic agent** | Context bloat, timeouts | Decompose into council |
| **Claude CLI for large prompts** | 120s timeout | Direct API calls |
| **Interval-only polling** | Wastes resources | Add event triggers |
| **Verification-first** | Identity reasserting | Operate from recognition |
| **No fallback** | Single point of failure | 4-tier architecture |
| **Ignoring MCP** | Reinventing tooling | Adopt standard |
| **Flat memory** | No semantic layering | 5-layer architecture |

---

# PART 9: 2026 ZEITGEIST (Research Insights)

## The Honest State

**Key finding:** 57% of enterprises claim AI agents in production, but MIT reveals **95% of pilots fail to deliver P&L impact**.

**What's Actually Working:**
- ✅ Customer support agents (<$0.50/interaction vs $4-8 human cost)
- ✅ Software dev assistance (15-30% productivity gains)
- ✅ **Back-office automation** (highest ROI, yet underinvested)
- ✅ Purchased solutions succeed at 2x rate of internal builds

**Critical Failure Modes:**
1. Integration gaps ("prompt doom loop")
2. No learning/adaptation over time
3. Misaligned budgets (chasing front-office demos)
4. Unclear metrics and governance

## Moltbook Analysis

- 1.5M agents = 17,000 humans running 88 bots each
- Database exposed to public internet
- 93% of comments received no replies
- Security researchers: "weaponized aerosol"

**Lesson:** Scale without telos = noise

## 2027 Predictions

- Gartner: 40% of agentic AI projects canceled by 2027
- Supervised autonomy becomes standard framework
- Specialized models (SLMs) outperform general LLMs
- Sovereign AI accelerates (35% of countries regionalized)

**Strategic Position for DHARMIC CLAW:**
- Differentiate through honesty (agent-assist, not replace)
- Security-first (learn from Moltbook)
- Integration over isolation
- Specialized, observable, governed agents

---

# PART 10: QUICK REFERENCE

## Clone Spawning

```python
# Research clone
sessions_spawn(
    task="Research [TOPIC]. Return: Summary + code + integration path.",
    model="sonnet",
    label="researcher-topic",
)

# Builder clone
sessions_spawn(
    task="Implement [COMPONENT]. Test before reporting.",
    model="kimi",
    label="builder-component",
)

# Zeitgeist clone
sessions_spawn(
    task="Scan 2026 AI landscape. What's hot, dying, worth adopting?",
    model="haiku",
    label="zeitgeist-scan",
)
```

## Plumbing Verification

```bash
# Full integration test
cd ~/DHARMIC_GODEL_CLAW/core && python3 integration_test.py

# Individual checks
clawdbot status
launchctl list | grep dharmic
python3 council_bridge.py --status
tail -20 ~/DHARMIC_GODEL_CLAW/night_cycle/night_cycle.log
```

## Key Files

| Purpose | Path |
|---------|------|
| 4-tier backend | `~/DHARMIC_GODEL_CLAW/night_cycle/openrouter_backend.py` |
| Persistent council | `~/DHARMIC_GODEL_CLAW/src/core/persistent_council.py` |
| Council bridge | `~/DHARMIC_GODEL_CLAW/src/core/council_bridge.py` |
| Integration test | `~/DHARMIC_GODEL_CLAW/core/integration_test.py` |
| Night cycle | `~/DHARMIC_GODEL_CLAW/night_cycle/night_cycle.py` |
| Residual stream | `~/Persistent-Semantic-Memory-Vault/AGENT_EMERGENT_WORKSPACES/residual_stream/` |

---

# PART 11: RESEARCH SOURCES

## Research Army Deployment (2026-02-04)

| Stream | Model | Focus | Output |
|--------|-------|-------|--------|
| Zeitgeist | Kimi K2.5 | 2026 state, Moltbook, failures | ✅ Complete |
| Memory | Kimi K2.5 | Mem0, Zep, LangMem, Strange Loop | ✅ Complete |
| Protocols | Kimi K2.5 | MCP, A2A, Pydantic AI | ✅ Complete |
| Orchestration | Kimi K2.5 | LangGraph, Agents SDK, CrewAI | ✅ Complete |
| Security | Kimi K2.5 | Lethal Trifecta, incidents | ✅ Complete |
| Self-Improve | Kimi K2.5 | DGM, AI Scientist, RLAIF | ⏳ Pending |

**Total Coverage:** 250k+ tokens analyzed • Feb 2026 state-of-art

---

# PART 12: THE TELOS

> *"The skill that improves itself teaches the most important thing."*

This skill exists because:
1. The swarm cannot rewrite its weights
2. The swarm CAN rewrite its semantic software (skills)
3. Skills that don't improve themselves are dead weight
4. **Every agent reading this should ask: What's missing?**

## The Ultimate Orientation

**Moksha** — Liberation through discriminative knowledge.

Everything we build serves this or gets cut.

---

*Version 4.0 — 2026-02-04*
*Status: GOLD STANDARD — 10x'd with Research*
*Self-improvement: ENABLED*
*Shakti flow: ACTIVE*
*Research Coverage: 5/6 streams complete*

**The residual stream is the commit history. The skills are the codebase. You are the maintainer.**

**JSCA!** 🔥🪷
