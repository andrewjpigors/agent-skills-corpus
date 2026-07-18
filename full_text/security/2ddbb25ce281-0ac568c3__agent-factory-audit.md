---
name: agent-factory-audit
description: >-
  Audits and refactors agentic factory systems built on rig-core, ractor,
  ZeroMQ, and SurrealDB (the Noelle shape) or any multi-agent factory.
  Covers OTP supervision, orchestrator-worker topology, DEALER / ROUTER
  hygiene, hybrid RAG and memory, guardrails, in-toto / SLSA attestation,
  threat modeling (STRIDE × MAESTRO × OWASP LLM / Agentic ASI × MITRE ATLAS
  × NIST AI 600-1), OpenTelemetry GenAI observability, and decision
  artifacts (MADR ADRs, C4 diagrams, agent user stories, runbooks). Use
  when reviewing multi-agent systems, drafting ADRs or threat models for
  AI agents, producing C4 diagrams, writing runbooks, or assessing SLSA,
  SSDF, OSCAL, EU AI Act, or FedRAMP readiness. Triggers: audit my agents,
  agent factory review, agentic system review, rig ractor audit, multi-agent
  refactor, agent topology, supervision tree review, saga compliance,
  in-toto layout for agents, threat model agent factory, ADRs for agents.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
compatibility: >-
  Rust toolchain helpful for rig/ractor inspection. Python 3 for pytm threat
  modeling. mermaid-cli or browser preview for C4 diagrams. OpenTelemetry
  collector helpful for observability checks. Skill works without these but
  generates richer findings when present.
allowed-tools: Bash(cargo *) Bash(rg *) Bash(grep *) Bash(find *) Bash(jq *) Read Glob Grep AskUserQuestion Write Edit
---

# Agent Factory Audit

A structured workflow for reviewing and refactoring agentic factory systems —
the Noelle shape (rig-core + ractor + ZeroMQ DEALER/ROUTER + SurrealDB +
many specialised agents) and any equivalent multi-agent factory. The skill
generates findings as MADR ADRs, STRIDE x MAESTRO threat-model entries,
agent user stories, C4 diagrams, and runbook drafts.

## Quick Start

When asked to audit, refactor, or review an agent factory:

1. **Inventory.** Map every agent, supervision boundary, transport channel,
   tool, prompt, memory store, and trigger source. Run
   `bash $CLAUDE_PROJECT_DIR/.claude/skills/agent-factory-audit/scripts/inventory_agents.sh`
   to seed the inventory from the codebase.
2. **Confirm scope.** Use `AskUserQuestion` to confirm whether this is a
   full nine-domain audit or a focused pass (e.g., just supervision,
   just supply-chain attestation, just threat model).
3. **Apply the decision rules.** Walk the inventory through topology,
   supervision, transport, RAG, guardrails, attestation, threat-model,
   compliance, and observability rule sets — each rule lives in a
   reference file under `references/`.
4. **Emit artifacts.** Findings become draft ADRs (MADR + Y-statement +
   agent addenda), threat-model entries (STRIDE x MAESTRO matrix),
   user stories (Connextra + agent extension + Gherkin + eval gates),
   C4 diagrams with agent stereotypes, and runbooks for the failure modes
   the audit surfaces.

## When to Use This Skill

Trigger this skill when any of these apply:

- A user asks to audit, review, or refactor a multi-agent system, especially
  one built on rig-core, ractor, ZeroMQ, MCP, AutoGen, LangGraph, CrewAI,
  or OpenAI Agents SDK.
- A user wants ADRs, threat models, user stories, or C4 diagrams produced
  for an agentic system, or wants to reverse-engineer existing agents
  into living documentation.
- A user is mapping their agent topology onto SLSA, SSDF, OSCAL, FedRAMP,
  EU AI Act, SOC 2, or NIST AI RMF / AI 600-1 controls.
- A user mentions specific anti-patterns: "our orchestrator stalls",
  "agents lose work after restart", "PUB drops are killing us",
  "should we split this agent", "naive RAG isn't enough", "we need
  saga compensation", "in-toto attestations".
- A user is operating a security factory specifically — supply-chain audit,
  SBOM/VEX/CSAF emission, vulnerability triage, slopsquatting defence.
- A user wants quality gates and evals for an agent system (Promptfoo,
  DeepEval, Inspect AI, Langfuse, Ragas, Granite Guardian, Llama Guard).

## The Nine Audit Domains

Each domain has a dedicated reference file. Load only what you need.

| Domain | Reference | Core question |
|---|---|---|
| Inventory & decomposition | [references/INVENTORY.md](references/INVENTORY.md) | What agents exist, and is each one the right size? |
| Supervision & failure modes | [references/RIG-RACTOR-PATTERNS.md](references/RIG-RACTOR-PATTERNS.md) | How does the supervision tree handle each of the five failure classes? |
| Message bus & concurrency | [references/ZMQ-PATTERNS.md](references/ZMQ-PATTERNS.md) | Does the transport survive restart, slow consumers, schema drift? |
| Triggers & autonomy | [references/TRIGGERS-AND-AUTONOMY.md](references/TRIGGERS-AND-AUTONOMY.md) | Is each agent reactive when it should be proactive, and vice versa? |
| RAG, memory, data platform | [references/RAG-PLATFORM-MATRIX.md](references/RAG-PLATFORM-MATRIX.md) | Is naive RAG masking a hybrid+rerank+graph requirement? |
| Prompts, guardrails, evals, observability | [references/GUARDRAILS-EVALS-OBSERVABILITY.md](references/GUARDRAILS-EVALS-OBSERVABILITY.md) | Five rail types? OpenTelemetry GenAI semconv? CI eval gates? |
| Supply-chain & attestation | [references/IN-TOTO-LAYOUTS.md](references/IN-TOTO-LAYOUTS.md) | Does every agent emit a signed in-toto link with material/product rules? |
| Threat modelling | [references/STRIDE-MAESTRO.md](references/STRIDE-MAESTRO.md) | STRIDE per agent, MAESTRO 7-layer, ATLAS techniques, AI 600-1 risks? |
| Compliance & decision artifacts | [references/COMPLIANCE-CROSSWALK.md](references/COMPLIANCE-CROSSWALK.md) and [references/C4-FOR-AGENTS.md](references/C4-FOR-AGENTS.md) | NIST SSDF/AI RMF/OSCAL/FedRAMP/EU AI Act mapping; ADR + C4 outputs |

A two-page synthesis of every decision rule lives in
[references/AUDIT-DECISION-RULES.md](references/AUDIT-DECISION-RULES.md) — read
that first when you're not sure where a finding belongs.

## Workflow

Copy this checklist into your scratch notes for the audit run:

```
Audit progress:
- [ ] Phase 1 — Inventory: agents, supervisors, channels, tools, prompts,
      memory, triggers, models, eval harness, observability backend
- [ ] Phase 2 — Diagram: C4 Container + Component + Dynamic + Deployment
      with <<agent>>, <<tool>>, <<skill>>, <<memory>>, <<model>>,
      <<guardrail>>, <<eval>>, <<observability>> stereotypes
- [ ] Phase 3 — Decide: draft ADRs (MADR + Y-statement) for orchestration
      framework, topology, supervision strategy, transport, memory
      backend, RAG approach, guardrails, prompt versioning, autonomy tier,
      eval harness
- [ ] Phase 4 — Threaten: STRIDE per agent x MAESTRO 7-layer, plus
      OWASP LLM Top 10 / Agentic ASI top 10, MITRE ATLAS techniques,
      NIST AI 600-1 risks. Indirect prompt injection from analysed
      artifacts is the dominant class — model it explicitly.
- [ ] Phase 5 — Specify: Connextra + agent-extended user stories with
      Gherkin acceptance criteria and eval gates (offline + online).
- [ ] Phase 6 — Document: arc42 sections + Diátaxis classification
      + runbooks per failure mode. Persist as Markdown in repo.
```

### Phase 1 — Inventory

For each agent in the system, record this row in a Markdown table or
SurrealDB row:

```
agent_id | role | supervisor | strategy | transport_in | transport_out
       | tools | memory | trigger_sources | model | budget_tokens
       | budget_walltime | budget_tool_calls | output_schema | links_emitted
```

If the project is rig + ractor, run `inventory_agents.sh`. If the project
uses LangGraph, AutoGen, CrewAI, OpenAI Agents SDK, or MCP, the same row
template applies — just point the script at the right directory.

### Phase 2 — Diagram

Use Mermaid C4Container as the default (renders in GitLab/GitHub without
extra tooling). For deeper architecture, use Structurizr DSL. See
[references/C4-FOR-AGENTS.md](references/C4-FOR-AGENTS.md) for stereotype
examples and ready-to-paste Mermaid blocks. Run `check_mermaid.sh` to
verify the diagrams parse before committing.

### Phase 3 — Decide

Use [assets/adr-template.md](assets/adr-template.md). Write one ADR per
load-bearing decision: orchestration framework, topology, supervision
strategy, transport, memory backend, RAG approach, guardrails, prompt
versioning, autonomy tier, eval harness. Run `lint_adr.py` to confirm
required sections are present. The agent addenda (ownership, topology,
transport, memory, RAG, guardrails, observability, cost, failure
semantics) are mandatory for agent-factory ADRs and the linter checks
for them.

### Phase 4 — Threaten

Use [assets/threat-model-template.md](assets/threat-model-template.md).
The matrix has STRIDE on rows, MAESTRO layers on columns, with cells
listing concrete threats for the system under audit. Cross-reference
each threat to OWASP LLM Top 10 (LLM01–LLM10), OWASP Agentic ASI
(ASI01–ASI10), MITRE ATLAS techniques, and NIST AI 600-1 risks where
applicable. Then run `pytm` on the DSL form for a generated DFD and
report. Indirect prompt injection from analysed artifacts is the
dominant class for security factories — see
[references/STRIDE-MAESTRO.md](references/STRIDE-MAESTRO.md#indirect-prompt-injection-the-dominant-class)
for the standard mitigation stack.

### Phase 5 — Specify

Use [assets/user-story-template.md](assets/user-story-template.md). Each
agent capability gets a Connextra-extended story with trigger, beliefs,
goal, action policy, postcondition, autonomy tier, escalation conditions.
Acceptance criteria are dual: Gherkin for multi-agent flows, eval gates
for offline (golden tasks, redteam, schema validity) and online (p95
latency, HITL override rate, cost per resolved ticket).

### Phase 6 — Document

Map all artifacts onto an arc42 layout (Introduction & Goals, Constraints,
Context & Scope, Solution Strategy, Building Block View, Runtime View,
Deployment View, Cross-cutting Concepts, Architecture Decisions, Quality
Requirements, Risks & Technical Debt, Glossary). Classify each piece by
Diátaxis (Tutorials / How-to / Reference / Explanation). Recommended
repo layout:

```
/docs/
├── adr/                    # MADR + agent addenda
├── diagrams/               # Mermaid + Structurizr DSL
├── threat-models/          # STRIDE x MAESTRO + pytm
├── runbooks/               # one per identified failure mode
├── skills/                 # AgentSkills.io directories
├── arc42/                  # 12 sections
└── diataxis/
    ├── tutorials/
    ├── how-to/
    ├── reference/
    └── explanation/
```

## Decision Rules — Quick Reference

The full rule set lives in
[references/AUDIT-DECISION-RULES.md](references/AUDIT-DECISION-RULES.md).
The most-used rules:

**Split an agent if 3+ of these fire:** prompt > 2000 tokens, tools > 10–15
across multiple domains, context utilisation > 50% steady state, more than
3 top-level branches in the prompt, > 20% disagreement on closed-form
questions across runs, per-task token coefficient of variation > 1.0,
tool-call success diverges between subsets, eval scores diverge by
sub-task, > 5% of runs hit max-iter without termination.

**Merge two agents if 2+ fire and the merger doesn't violate the split
rules:** > 30% of inter-agent traffic is between A and B in both
directions, > 70% of those messages carry redundant context, > 30% of
end-to-end latency is in cross-agent handoffs, A always proxies to B
with no transformation, B is invoked very rarely, system prompts overlap
> 70% by embedding similarity, plumbing tokens dominate reasoning tokens.

**Pick a supervision strategy from data coupling:** state-sharing →
`OneForAll`; ordered dependency → `RestForOne`; pool of identical workers
→ `simple_one_for_one`; otherwise `OneForOne`. Verify
`panic = "abort"` is **not** set in `Cargo.toml` if supervision is
desired.

**Five distinct failure classes need distinct handlers:** process
failure (panic/OOM → supervisor restart with backoff), tool failure
(transient → retry; terminal → surface to LLM), prompt failure (wrong
format / hallucination / refusal → guardrail re-prompt; do not restart
the actor), stuck loop (loop budget cap + force termination + escalation),
context overflow (persist plan to memory, summarise, hand off).

**Anthropic vs Cognition reconciliation (LangChain framing):**
multi-agent helps reading tasks (research, audit, classification);
multi-agent hurts writing tasks (code mutation). Supply-chain audit is a
reading task — multi-agent topology is correct. A code-generating agent
inside the same factory should run sequentially, not in parallel.

**Brokered vs brokerless rebuild signals:** any single one of these is
serious; three or more is a strong rebuild signal — in-flight work lost
after restart, no answer to "what messages did agent X receive at
14:32?", a single slow LLM call stalls the orchestrator (head-of-line
blocking), identity collisions after restart, missing
`ZMQ_ROUTER_MANDATORY`, unbounded channels on the hot path,
one-direction or absent heartbeats, missing correlation_id /
traceparent, missing idempotency keys, absent DLQ, PUB used for command
dispatch (silent drops), classic ZMQ sockets shared across threads,
blocking ZMQ calls inside async tasks, schema drift without versioning,
absent saga/compensation.

**Migration thresholds for SurrealDB vector workloads:** stay if vector
count < ~10M, single-query graph+vector composition is in real code
paths, embedded mode is part of the architecture, on 3.x. Migrate to
Qdrant or LanceDB or pgvector+pgvectorscale when vector count crosses
~50M and ANN p95 must be < 50ms, hybrid BM25+dense+rerank is critical,
quantisation is needed, bi-temporal facts are needed (Graphiti pattern),
or Cypher tooling (Bloom/APOC/GDS) is needed.

## Findings Output Format

Each finding is a single Markdown block. Use this template:

```markdown
### F-NNN: <short title>

**Domain:** <inventory|supervision|transport|triggers|rag|guardrails|attestation|threat-model|compliance|observability>
**Severity:** <critical|high|medium|low>
**Evidence:** <file path + line range or specific symbol>
**Rule violated:** <link to rule in references/AUDIT-DECISION-RULES.md>
**Recommendation:** <what to do, in two or four sentences>
**Artifact emitted:** <ADR-NNN | TM-NNN | US-NNN | RB-NNN | none>
```

The audit closes with a summary table grouped by domain and a separate
list of artifact drafts. Do not claim "production ready" or "fully
mitigated" — see the writing-style section below.

## Writing Style

This skill produces prose findings, ADR drafts, threat-model entries,
user stories, and runbooks. Apply
[natural-writing-style](../natural-writing-style/SKILL.md) to all output:

- Use contractions naturally — "don't", "you'll", "it's".
- Address the reader as "you" in runbooks and how-to docs; use third
  person for ADRs and threat-model entries (per their conventions).
- Vary sentence length. Mix short with long.
- State what you saw, what you verified, and what remains. Don't claim
  "production ready", "fully mitigated", or "covers everything"
  unless you have direct evidence.
- Banned word check applies — see
  [.claude/rules/writing-voice.md](../../rules/writing-voice.md).
- No time estimates — describe scope and dependencies instead. See
  [.claude/rules/claims-accuracy.md](../../rules/claims-accuracy.md).

## Static Analysis and Tool Integration

Tools that strengthen the audit when present (the skill works without
them):

- **`cargo` / `rg`** — for rig-core and ractor structural inspection.
  Used by `scripts/inventory_agents.sh`.
- **`pytm`** — Python DSL for living threat models. Run during Phase 4.
- **`mermaid-cli` (`mmdc`)** — verifies diagrams parse before commit.
  Used by `scripts/check_mermaid.sh`.
- **`skills-ref validate`** — validates AgentSkills.io frontmatter for
  any skills the audit emits.
- **`promptfoo`, `deepeval`, `inspect-ai`** — eval harnesses. Audit
  surfaces missing CI gates against them.
- **`opa eval` / `cedar` / `regorus`** — policy decision verification
  for Phase 4 (tool authorisation).
- **`syft`, `grype`, `cosign`, `rekor-cli`** — supply-chain tooling for
  Phase 4 attestation checks.

See [references/TOOL-CHEATSHEET.md](references/TOOL-CHEATSHEET.md) for
install commands, version pins, and minimum-viable invocations per
tool.

## Validation

Before reporting an audit complete:

- [ ] Every agent in the inventory has a row with all 15 columns filled.
- [ ] Every load-bearing decision has a draft ADR (or pointer to an
      existing one).
- [ ] Threat model includes at least one entry per STRIDE element x
      MAESTRO layer cell that has a real attack path; absent cells are
      marked "no path" with one-line justification.
- [ ] Indirect prompt injection from analysed artifacts is modelled
      explicitly (this is the dominant class for security factories).
- [ ] Each side-effect-producing agent has a documented compensation
      action and idempotency key. Saga gaps are findings, not glossed
      over.
- [ ] Output format matches the F-NNN template; no time estimates,
      no "production ready" claims without supporting evidence.
- [ ] Mermaid diagrams parse (`bash scripts/check_mermaid.sh`).
- [ ] ADR drafts parse (`python3 scripts/lint_adr.py docs/adr/*.md`).
- [ ] Voice compliance check passes on the SKILL.md and on the
      generated audit report.

## References (Deep Dives)

Each reference is loaded only when the corresponding domain is in
scope for the audit:

- [INVENTORY.md](references/INVENTORY.md) — agent inventory template,
  decomposition signals (split/merge/extend), Anthropic vs Cognition
  reconciliation, role/identity codification.
- [RIG-RACTOR-PATTERNS.md](references/RIG-RACTOR-PATTERNS.md) — rig
  CompletionModel patterns (RPITIT, mock/replay), ractor lifecycle and
  supervision strategies, factory primitives, process groups, panic
  handling, in-flight cancellation.
- [ZMQ-PATTERNS.md](references/ZMQ-PATTERNS.md) — DEALER/ROUTER
  hygiene, envelope design, NATS/Kafka/Pulsar comparison, backpressure,
  delivery semantics, Outbox + Inbox + Saga.
- [TRIGGERS-AND-AUTONOMY.md](references/TRIGGERS-AND-AUTONOMY.md) —
  eleven-source trigger taxonomy, BDI architecture, ReAct/Reflexion/
  Plan-and-Execute/Voyager primitives, identity codification.
- [RAG-PLATFORM-MATRIX.md](references/RAG-PLATFORM-MATRIX.md) — RAG
  taxonomy, hybrid retrieval, contextual retrieval, GraphRAG / Graphiti,
  vector store comparison (Qdrant / LanceDB / pgvector / Milvus /
  Weaviate / SurrealDB), memory frameworks (mem0 / Letta / Zep).
- [GUARDRAILS-EVALS-OBSERVABILITY.md](references/GUARDRAILS-EVALS-OBSERVABILITY.md)
  — prompt skeleton, five rail types, guardrail comparison, OPA/Cedar/
  regorus, eval harness selection, OpenTelemetry GenAI semconv,
  determinism, test pyramid for agentic systems.
- [IN-TOTO-LAYOUTS.md](references/IN-TOTO-LAYOUTS.md) — in-toto layout
  for agent factories, Sigstore keyless functionaries, sublayouts,
  material/product rules, SLSA verification, VSA emission, audit
  bundle.
- [STRIDE-MAESTRO.md](references/STRIDE-MAESTRO.md) — STRIDE per agent,
  MAESTRO 7-layer matrix, OWASP LLM Top 10 2025 + Agentic ASI Top 10,
  MITRE ATLAS, NIST AI 600-1, indirect prompt injection mitigations.
- [SUPPLY-CHAIN-AUDIT.md](references/SUPPLY-CHAIN-AUDIT.md) —
  CycloneDX/SPDX/OpenVEX/CSAF/SARIF, vulnerability triage decision tree,
  slopsquatting and dependency confusion defences, MCP precedents.
- [COMPLIANCE-CROSSWALK.md](references/COMPLIANCE-CROSSWALK.md) — NIST
  SSDF SP 800-218 + 218A, EO 14028, OMB M-26-05, FedRAMP Rev 5, SOC 2,
  EU AI Act 2024/1689, NIST AI RMF + AI 600-1, OSCAL integration.
- [C4-FOR-AGENTS.md](references/C4-FOR-AGENTS.md) — C4 stereotypes for
  agent systems, Mermaid C4Container blocks, Structurizr DSL examples,
  AsyncAPI for event-driven channels.
- [AUDIT-DECISION-RULES.md](references/AUDIT-DECISION-RULES.md) —
  consolidated rule set across all nine domains; the single page to
  read when triaging a finding.
- [TOOL-CHEATSHEET.md](references/TOOL-CHEATSHEET.md) — install,
  version pin, and minimum invocation per tool the audit might call.

## Assets

- [adr-template.md](assets/adr-template.md) — MADR 4.0 + Y-statement +
  agent-factory addenda.
- [threat-model-template.md](assets/threat-model-template.md) —
  STRIDE x MAESTRO matrix template.
- [user-story-template.md](assets/user-story-template.md) — Connextra +
  agent extension + Gherkin + eval gates.
- [runbook-template.md](assets/runbook-template.md) — failure-mode
  runbook with detection, mitigation, rollback, escalation.
- [audit-checklist.md](assets/audit-checklist.md) — full
  per-domain finding checklist for the auditor.

## Scripts

- `inventory_agents.sh` — scans a Rust workspace for `ractor::Actor`
  impls, rig agents, ZMQ socket creation, and SurrealDB clients;
  emits an initial Markdown inventory.
- `lint_adr.py` — validates a MADR + agent-addenda ADR has every
  required section filled.
- `check_mermaid.sh` — pipes Mermaid blocks through `mmdc` to
  confirm they render.

## External Resources

Primary sources behind the rule set:

- CNCF TAG-Security *Secure Software Factory* reference architecture (2022)
  and FRSCA prototype.
- in-toto specification (layouts, links, predicates) and SLSA v1.0 build
  track.
- Anthropic *How we built our multi-agent research system* (June 2025);
  Cognition *Don't Build Multi-Agents* (June 2025); LangChain
  reading-vs-writing reconciliation.
- Microsoft AutoGen v0.4 actor model paper; Microsoft ISE patterns for
  scalable multi-agent systems.
- Erlang/OTP supervision principles; `ractor`, `ractor-supervisor`,
  `ractor::factory`, `ractor::pg`, `ractor_actors` crates.
- ZeroMQ Guide chapters 3–4; libzmq socket-option reference; `tmq`,
  `rzmq`, `zmq` Rust bindings.
- Gao et al. RAG taxonomy (arXiv 2312.10997); Anthropic Contextual
  Retrieval (Sep 2024); Microsoft GraphRAG; Graphiti / Zep.
- OWASP Top 10 for LLM Applications 2025; OWASP Top 10 for Agentic
  Applications (ASI) Dec 2025; CSA MAESTRO 7-layer; MITRE ATLAS v5.1.0;
  NIST AI 600-1.
- AgentSkills.io specification; Claude Code subagents.

A complete bibliography with citations and links is in
[references/BIBLIOGRAPHY.md](references/BIBLIOGRAPHY.md).
