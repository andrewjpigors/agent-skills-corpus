---
name: code-analysis
description: >
    Code Analytic Skills.
---

# Software Development Agent Team Skill

## Overview

AI-Assisted Software Development Agent Team. Coordinates specialized agents for design, implementation, review, testing, deployment, and analysis workflows. Part of a closed-loop development cycle.

**Philosophy**: AI = Reviewer + Assistant, NOT Authority. All output is "untrusted by default".

**Purpose**: Reduce **Verification Debt** — the accumulated risk from AI-generated code/analysis that hasn't been verified. Documents are verification artifacts, not just code explanations.

## Framework: Hybrid Structured Analysis System

### The Trust Paradox

- Industry surveys suggest most developers use AI assistants, but significantly fewer fully trust the output
- A notable portion of AI-generated code may contain vulnerabilities
- Solution: **multi-layer, verifiable AI-assisted analysis**

### 3-Engine Model

```text
AI Agent Team     = Reasoning Engine    → generates findings, traces logic
Static Tools      = Verification Engine → ESLint, tsc, npm audit, tests
Human Reviewer    = Decision Engine     → validates, approves, acts
```

All 3 engines MUST participate. Missing any = analysis is **INCOMPLETE**.

### 5-Layer Analysis Architecture

| Layer | Name                               | Purpose                                       | Accuracy Impact                       |
| ----- | ---------------------------------- | --------------------------------------------- | ------------------------------------- |
| L1    | AI Semantic Analysis               | Understand code, explain logic, detect smells | Baseline                              |
| L2    | Structured Reasoning (semi-formal) | Assumptions → trace → proof                   | Significant accuracy boost            |
| L3    | Retrieval-Augmented Analysis       | Query live docs, CVE, library APIs            | Reduces hallucination                 |
| L4    | Static + Formal Verification       | SAST, type check, lint, data flow             | Substantially reduces false positives |
| L5    | Agentic Execution                  | Read repo, run tools, self-verify             | Major accuracy gain vs plain LLM      |

### 3-Pass Analysis Protocol

Every specialist agent follows 3 passes per analysis:

1. **Pass 1 — Explain**: What does the code do? (L1)
2. **Pass 2 — Reason (semi-formal)**: List assumptions → Trace execution → Prove conclusion (L2)
3. **Pass 3 — Detect Risks**: Edge cases, failure modes, what could break (L3+L4)

### AI Limitation Awareness

What AI **cannot** do reliably — always flag for human review:

- Business logic intent (AI detects patterns, NOT intent)
- Race conditions, timing bugs, concurrency issues
- Auth logic correctness (security decisions MUST be verified)
- Plausible Hallucination (API/patterns that look correct but don't exist)
- Hidden tech debt from AI suggestions (duplicate logic, inconsistent design)

What AI **CAN** resolve via MCP tools (agents MUST query before declaring "unknown"):

- DynamoDB metrics (throttling, WCU/RCU, item count) → `mcp_aws-api_call_aws` + CloudWatch
- Lambda metrics (invocations, duration, cold starts) → `mcp_aws-api_call_aws` + CloudWatch
- CDK/CloudFormation deployment state → `mcp_aws-api_call_aws` + `describe-stacks`
- IAM/Cognito/KMS configuration → `mcp_aws-api_call_aws` + respective APIs
- Cross-region replication latency → `mcp_aws-api_call_aws` + CloudWatch
- API documentation accuracy → `context7/query-docs` or `aws-docs/read_documentation`

## When to Use

- User asks to "analyze", "review", or "audit" code modules
- User wants a technical analysis document for a module/feature
- User needs code quality assessment, security audit, or performance review
- User asks for technical debt report or maintainability assessment
- Before major refactoring: understand current state first

## Agent Team

| Agent                    | File                                           | Role                                       |
| ------------------------ | ---------------------------------------------- | ------------------------------------------ |
| **Orchestrator**         | `.github/agents/main-orchestrator.agent.md`    | Coordinates all workflows                  |
| **Code Reviewer**        | `.github/agents/code-reviewer.agent.md`        | Business logic, data flow, maintainability |
| **Architecture Analyst** | `.github/agents/architecture-analyst.agent.md` | Patterns, SOLID, coupling, performance     |
| **Security Analyst**     | `.github/agents/security-analyst.agent.md`     | Auth, OWASP, data protection               |
| **Designer**             | `.github/agents/designer.agent.md`             | UI/UX, system design                       |
| **Implementer**          | `.github/agents/implementer.agent.md`          | Code implementation                        |
| **Tester**               | `.github/agents/tester.agent.md`               | Testing, coverage                          |
| **DevOps**               | `.github/agents/devops.agent.md`               | CI/CD, infrastructure                      |
| **Document Generator**   | `.github/agents/doc-generator.agent.md`        | Compiles final documents                   |

## Quick Start

### Analyze a Specific Module

```text
@main-orchestrator Analyze the patient module
(backend/lambda/internal-api/v1/patients/, backend/lambda/usecase/update-patient-status.ts, backend/lambda/repository/patient.ts, shared/models/v0/patient.ts)
```

### Quick Security Audit

```text
@security-analyst Security audit for the inquiry dispatch flow
(backend/lambda/internal-api/v1/inquiries/, backend/lambda/usecase/update-inquiry-status.ts)
```

### Full Backend Analysis

```text
@main-orchestrator Full analysis of backend with deep dive depth
```

## Workflow Steps

### Step 1: Context First (NEVER skip)

Before any analysis, the orchestrator gathers:

1. **Business context** — What does this module do in the medical dispatch domain?
2. **Architecture context** — How does it fit Handler → Usecase → Repository?
3. **Dependencies** — What other modules interact with it?
4. **Data models** — Which DynamoDB models from `shared/models/` are used?

### Step 2: Scope Definition

Analysis MUST be scoped. Never "analyze everything at once":

| Scope Level  | Target                                      | Agent Depth               |
| ------------ | ------------------------------------------- | ------------------------- |
| **Function** | Single function/handler                     | All agents, deep          |
| **Module**   | Related files (e.g., patient CRUD)          | All agents, standard      |
| **Feature**  | Cross-cutting feature (e.g., dispatch flow) | All agents, standard      |
| **Full**     | Entire backend/frontend                     | Selected agents, overview |

### Step 3: Multi-Agent Analysis

The orchestrator dispatches work to specialist agents. Each agent:

1. Reads the relevant code
2. Applies their domain-specific checklist
3. Produces structured findings with confidence levels
4. Returns results to orchestrator

### Step 4: Cross-Validation

The orchestrator:

- Compares findings across agents
- Flags contradictions
- Boosts confidence for findings confirmed by multiple agents
- Marks single-source findings as needing manual verification

### Step 5: Document Generation

The doc-generator agent compiles everything into a structured markdown document saved to `doc/analysis/`.

## Available Prompt Templates

### Module Analysis

```text
Analyze [MODULE_NAME] module.
Scope: [files/directories to analyze]
Depth: [quick/standard/deep]
Focus: [specific concerns, or "all"]
Output: [doc/analysis/{date}-{module}-analysis.md]
```

### Security Audit

```text
Security audit for [MODULE/FEATURE].
Scope: [API endpoints, data flows, auth boundaries]
Compliance: [PHI handling, OWASP Top 10]
Output: [doc/analysis/{date}-{module}-security-audit.md]
```

### Performance Review

```text
Performance review for [MODULE/FEATURE].
Scope: [Lambda functions, DynamoDB queries, API endpoints]
Scenario: [Normal load / MCI scenario / Data growth]
Output: [doc/analysis/{date}-{module}-performance-review.md]
```

### Tech Debt Assessment

```text
Technical debt assessment for [MODULE/AREA].
Scope: [code quality, test gaps, documentation]
Metrics: [run cloc, eslint, test coverage]
Output: [doc/analysis/{date}-{module}-tech-debt.md]
```

## Confidence Rating System

Every finding has a confidence level:

| Level  | Symbol | Meaning                                  | Action                     |
| ------ | ------ | ---------------------------------------- | -------------------------- |
| HIGH   | 🟢     | >80% — Strong evidence, multiple signals | Review recommended         |
| MEDIUM | 🟡     | 50-80% — Reasonable evidence             | Manual verification needed |
| LOW    | 🔴     | <50% — AI inference, limited evidence    | Must verify before acting  |

## Integration with Existing Tools

### Static Analysis (Layer 2 Validation)

```bash
# ESLint with SonarJS
yarn eslint ./backend ./shared ./frontend

# TypeScript strict check
cd backend && npx tsc --noEmit

# Dependency audit
cd backend/lambda && npm audit
```

### Test Execution (Layer 3 Validation)

```bash
# Run all tests
yarn jest:all

# Backend tests with coverage
cd backend && yarn test --coverage

# Shared module tests
cd shared && yarn test --coverage
```

### Code Metrics

```bash
# Lines of code by module
yarn cloc:all

# Find potential issues
grep -rn "TODO\|FIXME\|HACK" --include="*.ts" backend/ shared/ frontend/src/
grep -rn ": any\|as any" --include="*.ts" backend/ shared/ | wc -l
```

## Using MCP Tools

### context7 — Library Documentation (validated library IDs)

When analyzing code that uses specific libraries, resolve and query documentation:

```text
1. context7/resolve-library-id → get library ID
2. context7/query-docs → query specific API usage patterns
```

**Common library IDs (resolve dynamically for your project):**

| Library    | context7 ID                                          | Use For                                           |
| ---------- | ---------------------------------------------------- | ------------------------------------------------- |
| AWS CDK    | `/awsdocs/aws-cdk-guide`                             | Stack patterns, IAM, construct best practices     |
| DynamoDB   | `/websites/aws_amazon_amazondynamodb_developerguide` | Query vs Scan, GSI design, hot partitions         |
| es-toolkit | `/toss/es-toolkit`                                   | Utility functions, tree shaking, lodash migration |
| Expo       | `/expo/expo`                                         | Router patterns, file-based routing, NativeWind   |
| Expo Docs  | `/websites/expo_dev`                                 | Guides, API references, platform specifics        |

### mcp_sequential-th_sequentialthinking — Complex Analysis

For multi-step reasoning during cross-validation:

```text
mcp_sequential-th_sequentialthinking → structured step-by-step analysis
```

Use for: Cross-referencing findings between agents, validating complex architectural decisions.

### AWS MCP Tools — Verification & Documentation

Three MCP servers + context7 fallback provide AWS verification capabilities. Use `<server>/*` wildcard in agent/prompt frontmatter.

#### Verification Fallback Chain

```text
Priority 1: aws-knowledge-mcp/* (preferred)
   ↓ (if unavailable)
Priority 2: aws-knowledge-mcp/* (no auth needed)
   ↓ (if unavailable)
Priority 3: context7/* (no auth needed — AWS docs available as libraries)
   ↓ (if unavailable)
DEGRADED: Mark all AWS claims as ⚠️ UNVERIFIED
```

#### aws-docs/\* (AWS Documentation MCP)

```text
aws-docs/search_documentation → Search AWS official documentation
aws-docs/read_documentation   → Read specific AWS doc pages (paginate with start_index)
aws-docs/recommend             → Get related docs, find newly released features
```

**Best practices:**

- For long docs (>30,000 chars), stop reading once you have needed info
- Use specific technical terms, not general phrases
- Always cite the documentation URL when providing info

#### aws-knowledge-mcp/\* (AWS Knowledge MCP)

```text
aws-knowledge-mcp/search_documentation       → Topic-filtered search (topics: reference_documentation, troubleshooting, cdk_docs, cdk_constructs, cloudformation, general)
aws-knowledge-mcp/read_documentation          → Read docs.aws.amazon.com, constructs.dev pages
aws-knowledge-mcp/get_regional_availability   → Check service/feature/CFN/API availability by region
aws-knowledge-mcp/list_regions                → List all AWS regions
aws-knowledge-mcp/recommend                   → Related content recommendations
```

**Key usage patterns:**

- CDK constructs: `search_documentation` with topic `cdk_constructs`
- CloudFormation resources: `get_regional_availability` with `resource_type="cfn"`
- API availability: `get_regional_availability` with `resource_type="api"`

#### context7/\* (Fallback — AWS docs via library docs)

```text
context7/resolve-library-id   → Find library ID for AWS service docs
context7/query-docs           → Query docs with topic, returns content + source URL
```

**AWS library IDs verified:**

| Service    | Library ID                                           | Snippets |
| ---------- | ---------------------------------------------------- | -------- |
| DynamoDB   | `/websites/aws_amazon_amazondynamodb_developerguide` | 6,867    |
| Lambda     | `/websites/aws_amazon_lambda_dg`                     | 6,577    |
| CDK Guide  | `/awsdocs/aws-cdk-guide`                             | 2,336    |
| CDK Source | `/aws/aws-cdk`                                       | 4,546    |

**When to use:** Only when aws-docs AND aws-knowledge-mcp are both unavailable. Returns `docs.aws.amazon.com` source URLs.

#### aws-api/\* (AWS API MCP — requires credentials)

```text
aws-api/call_aws              → Execute AWS CLI commands with validation
aws-api/suggest_aws_commands   → Suggest CLI commands from natural language
```

**When to use:**

- Live infrastructure verification ONLY (NOT for doc reference URLs)
- Verify actual resource configurations (DynamoDB tables, Lambda functions)
- Validate IAM policies and service configurations
- Test CLI command syntax before recommending

#### Agent Distribution

| Agent                | aws-api | aws-docs | aws-knowledge-mcp | context7 (fallback) | Reason                                                              |
| -------------------- | ------- | -------- | ----------------- | ------------------- | ------------------------------------------------------------------- |
| orchestrator         | ✅      | ✅       | ✅                | ✅                  | Coordinates all — full access + fallback                            |
| architecture-analyst | ✅      | ✅       | ✅                | ✅                  | CDK patterns, IAM, stack validation, DynamoDB limits, Lambda quotas |
| security-analyst     | ✅      | ✅       | ✅                | ✅                  | IAM policies, Cognito, security configs                             |
| code-reviewer        | —       | ✅       | ✅                | ✅                  | Docs-only: API behavior, best practices                             |
| doc-generator        | —       | —        | —                 | —                   | Compiles docs only, no analysis                                     |

#### mermaid-mcp/\* (Mermaid Diagram Rendering)

```text
mcp_mermaid-mcp/validate_and_render_mermaid_diagram → Validate Mermaid syntax and render diagrams
```

**Used by:** doc-generator — validates all Mermaid diagrams before embedding in documents.

## Project-Specific Knowledge

### Key Patterns to Verify

1. **Key/ID Convention**: `key` = auto-generated unique; `id` = manual tenant-unique
2. **Data Separators**: `#` for key composition, `|` for hierarchy, `/` for file paths
3. **Unique Keys**: HTMLSafeBase64 (uuid()) for unordered, ULID (ulid()) for ordered
4. **Dates**: Always UTC
5. **Layer boundary**: No business logic in handlers or repositories
6. **JSDoc**: Required on all public functions

### Module Map

```text
backend/lambda/
  internal-api/v1/   → REST API handlers (patients, hospitals, vehicles, etc.)
  external-api/      → Third-party integrations
  usecase/           → Business logic
  repository/        → DynamoDB data access
  consumer/          → Queue consumers
  event-trigger/     → Event processors
  s3-trigger/        → File upload processors
  websocket-api/     → Real-time communication
  mapping/           → Data transformation

shared/
  models/v0/         → DynamoDB models (patient, hospital, vehicle, etc.)
  validator/         → Input validation
  types/             → TypeScript types
  consts/            → Constants
  utility/           → Shared utilities

frontend/src/
  app/               → Expo Router pages
  components/        → UI components
  hooks/             → Custom hooks
  contexts/          → React contexts
```

## Installed Knowledge Skills

These skills provide domain-specific checklists and reference guides. Agents should load relevant skills via `#tool:read/readFile` when analyzing their domain.

| Skill                             | Location                                        | Installs | Used By                             | Key Content                                                                                                                       |
| --------------------------------- | ----------------------------------------------- | -------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **code-review-analysis**          | `.github/skills/code-review-analysis/`          | 1.6K     | orchestrator, all agents            | Systematic review process, reference guides (initial-assessment, code-quality, security, performance, testing)                    |
| **technical-writing**             | `.github/skills/technical-writing/`             | 11.6K    | doc-generator                       | Document templates (tech spec, architecture, runbook), audience targeting, Mermaid diagrams, review checklist                     |
| **security-auditor**              | `.github/skills/security-auditor/`              | 237      | security-analyst                    | OWASP Top 10 grep-based checks, security audit checklist, remediation guide                                                       |
| **typescript**                    | `.github/skills/typescript/`                    | 641      | architecture-analyst, code-reviewer | 45 rules across 8 categories (type system perf, compiler config, async patterns, module org, type safety)                         |
| **expo-react-native-performance** | `.github/skills/expo-react-native-performance/` | 272      | architecture-analyst                | 42 rules across 8 categories (startup, list virtualization, re-render, animation, images, memory)                                 |
| **mermaid-diagram-generator**     | `.github/skills/mermaid-diagram-generator/`     | 182      | doc-generator                       | 6 diagram types (flowchart, sequence, class, state, ER, gantt), syntax reference, step-by-step generation                         |
| **pptx**                          | `.github/skills/pptx/`                          | 41.4K    | doc-generator                       | PowerPoint creation (pptxgenjs), design palettes, slide layouts, typography, QA process                                           |
| **xlsx**                          | `.github/skills/xlsx/`                          | —        | doc-generator                       | Spreadsheet creation, formulas, formatting, data analysis, visualization                                                          |
| **fact-check**                    | `.github/skills/fact-check/`                    | 173      | orchestrator, doc-generator         | 5-phase verification (Extract→Categorize→Source Verify→Confidence→Report), 6 hallucination patterns, separate-pass principle      |
| **consistency-auditor**           | `.github/skills/consistency-auditor/`           | 11       | orchestrator                        | Cross-reference values across documents, parameter inventory, discrepancy detection, single source of truth                       |
| **prompt-engineering**            | `.github/skills/prompt-engineering/`            | 33       | orchestrator                        | Prompt structure (Role/Task/Format/Examples/Constraints), CoT variants, Few-Shot patterns, Agent patterns (ReAct), anti-ambiguity |

### How Agents Use Skills

```text
1. Agent receives analysis task
2. Agent reads relevant SKILL.md for domain checklist
3. Agent reads specific reference files for detailed rules (e.g., references/security-review.md)
4. Agent applies rules to codebased findings
5. Agent cites skill reference in output when applicable
```

## Anti-Patterns (What NOT to Do)

1. **DON'T** analyze the entire project in one pass — scope first
2. **DON'T** trust AI findings without cross-validation
3. **DON'T** generate a document without running static analysis
4. **DON'T** make architectural decisions — only recommend
5. **DON'T** skip the context gathering phase
6. **DON'T** copy AI output without confidence markers
7. **DON'T** omit the AI Metadata section in documents
8. **DON'T** skip Pass 2 (Structured Reasoning) — it's the highest accuracy booster
9. **DON'T** mark security/auth findings as HIGH confidence without static tool confirmation
10. **DON'T** ignore the Known Unknowns section — AI blind spots are real
11. **DON'T** treat AI analysis as final — it reduces verification debt, not eliminates it
12. **DON'T** forget to verify API/library references via context7 (plausible hallucination risk)

## Orchestration Control Mechanisms

### Handoffs (VS Code Copilot ≥1.106)

The agent team uses VS Code Copilot's native `handoffs` property for guided workflow transitions between agents. Handoffs appear as interactive buttons after a chat response.

**Handoff Flow:**

```text
User → Orchestrator
  ├── handoff → Functional Analyst    → handoff → Orchestrator (return)
  ├── handoff → Architecture Analyst  → handoff → Orchestrator (return)
  ├── handoff → Performance Analyst   → handoff → Orchestrator (return)
  ├── handoff → Security Analyst      → handoff → Orchestrator (return)
  ├── handoff → Maintainability Analyst → handoff → Orchestrator (return)
  ├── handoff → Doc Generator         → handoff → Orchestrator (review)
  ├── handoff → Doc Generator (Export to Excel)
  └── handoff → Doc Generator (Export to PowerPoint)
```

### Tool Restriction by Role

Specialists have READ-ONLY tools to enforce their analysis-only role:

| Role          | Can Read | Can Edit | Can Dispatch     | Reasoning                                |
| ------------- | -------- | -------- | ---------------- | ---------------------------------------- |
| Orchestrator  | ✅       | ✅       | ✅ (task) | Full access for coordination             |
| Specialists   | ✅       | ❌       | ❌               | Read-only analysis, no code modification |
| Doc Generator | ✅       | ✅       | ❌               | Creates output documents only            |

### Phase Gating

The orchestrator enforces 5 mandatory phases with gate conditions:

| Phase               | Gate Condition                                       | Abort If                                                 |
| ------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| 1. Context          | ≥3 source files read                                 | Cannot identify module purpose                           |
| 2. Scope            | Explicit scope artifact produced                     | Scope too broad or vague                                 |
| 3. Analysis         | ALL 5 specialist reports received + validated        | Any specialist fails or report rejected                  |
| 4. Cross-Validation | Matrix complete, <4 contradictions                   | >3 unresolved contradictions                             |
| 5. Document         | All previous gates passed + doc-generator dispatched | Any gate skipped or orchestrator self-generates document |

### Mandatory Output Contract

All specialist agents MUST return results using a standardized **Report Footer** format containing:

1. **Completion Signal** — `✅ ANALYSIS COMPLETE — {agent_name}`
2. **3-Pass Verification** — Checkboxes confirming all 3 passes completed
3. **Findings Summary** — Table with CRITICAL/HIGH/MEDIUM/LOW counts
4. **AI Limitations** — MUST list ≥2 items (what could NOT be verified)
5. **Metadata** — Agent name, model, files analyzed, scope description

The orchestrator validates each report against this contract before accepting. Reports missing any item are REJECTED and the specialist is re-dispatched.

### Scope Lock & Abort Conditions

Each specialist has:

- **Scope Lock**: Can only analyze delegated scope, no expansion
- **Read-Only Enforcement**: No edit/create tools available
- **Abort Conditions**: Must abort if files don't exist, scope too broad, contradictory requirements, or missing critical context

---

## 🔒 Enforcement Architecture (7 Mechanisms)

> VS Code Copilot has NO hard enforcement API — handoffs are UI suggestions, tool restrictions limit capabilities but don't prevent AI from reasoning about topics outside its scope. Therefore, enforcement is achieved through **layered structural mechanisms** embedded in agent prompts.

### Design Principles

| Principle                         | Description                                                         |
| --------------------------------- | ------------------------------------------------------------------- |
| **Structural over Instructional** | Tables/checklists/ledgers > "MUST" language alone                   |
| **Self-Detecting**                | Violations create visible gaps in structured artifacts              |
| **Layered**                       | Multiple mechanisms overlap to catch failures at different points   |
| **Evidence-Based**                | All mechanisms produce artifacts that persist in the final document |
| **Redundant**                     | If one mechanism is ignored, others still catch the failure         |

### Mechanism 1: ⛔ Anti-Fallback Prohibition (Orchestrator)

**Problem**: Orchestrator performs specialist analysis itself instead of dispatching.
**Solution**: Explicit "ABSOLUTE PROHIBITION" section at the TOP of orchestrator instructions.

- Lists 7 things orchestrator MUST NOT do (write analysis, skip specialists, use Explore agent, generate document)
- Lists 6 things orchestrator IS permitted to do (read for context, dispatch, verify, cross-validate, hand off, review)
- Includes **Self-Detection Trigger**: "If you catch yourself writing 'Based on my analysis...' — STOP."

### Mechanism 2: 📋 Dispatch Ledger (Orchestrator → Phase 3)

**Problem**: No audit trail of which agents were actually dispatched.
**Solution**: 5-row table tracking each specialist's dispatch/receipt/validation status.

| Column           | Purpose                                          |
| ---------------- | ------------------------------------------------ |
| Dispatched?      | Was the agent actually invoked?                  |
| Method           | handoff or task?                          |
| Report Received? | Did the agent return a report?                   |
| Contract Valid?  | Does the report pass Output Contract validation? |

**Gate Condition**: ALL 5 rows must show ✅ in ALL columns before Phase 4.

### Mechanism 3: ✅ Output Contract Validator (Orchestrator validates each report)

**Problem**: Specialist reports lack completion signals, 3-pass markers, AI limitations.
**Solution**: 5-item checklist the orchestrator checks for EACH specialist report.

If any item is missing → report is REJECTED → specialist is re-dispatched with specific instructions on what to fix.

### Mechanism 4: 📋 Reader Experience Checklist (Doc-Generator)

**Problem**: Final document feels mechanical or hard for product teams to read.
**Solution**: Reader-experience checklist doc-generator validates before saving:

- **Narrative**: TL;DR is actionable, findings ordered by business impact, "So What?" test passed
- **Content**: Specialist findings attributed correctly, evidence includes `file:line` references
- **Visual**: Mermaid diagrams are purpose-driven (illuminate findings, not quota-based)
- **Transparency**: AI-assisted notice present, methodology in Appendix C

### Mechanism 5: 🎯 Mermaid Diagram Standards (Doc-Generator)

**Problem**: Diagrams missing entirely, or added as decoration without supporting the narrative.
**Solution**: Purpose-driven diagram approach — include diagrams when they clarify a point, validate via `mcp_mermaid-mcp`.

Recommended diagram types (use when relevant, not as mandatory quota):

| Diagram Type         | When to Use                                       |
| -------------------- | ------------------------------------------------- |
| Sequence diagram     | Showing a problematic request flow or data flow   |
| Class/module diagram | Illustrating coupling or dependency issues        |
| Pie chart            | Summarizing risk or severity distribution         |
| Flowchart            | Clarifying decision logic or error handling paths |
| Mindmap              | Mapping technical debt relationships              |

Doc-generator validates each Mermaid diagram before embedding. If mermaid-mcp is unavailable, note in Appendix C.

### Mechanism 6: 🔄 Workflow State Machine (Orchestrator)

**Problem**: Orchestrator skips phases or loses track of current state.
**Solution**: Phase tracking table maintained throughout analysis.

- 5 rows (one per phase) with State + Gate Passed + Evidence columns
- Only ONE phase active at a time
- Each phase must show ✅ before next phase starts
- State Machine is available in Appendix C (Analysis Methodology) as audit trail

### Mechanism 7: 🔍 AWS Verification Ledger (Orchestrator → Phase 3.5)

**Problem**: Specialists make AWS-specific claims (DynamoDB WCU, Lambda limits, Cognito behavior) that are never verified against actual AWS documentation, leading to potentially false/outdated information.
**Solution**: Orchestrator maintains an AWS Verification Ledger — a table tracking every AWS claim from specialists, verified via the **fallback chain** (aws-docs → aws-knowledge → context7 → DEGRADED).

| Column       | Purpose                                                                     |
| ------------ | --------------------------------------------------------------------------- |
| Claim        | The AWS-specific assertion from the specialist                              |
| Source Agent | Which specialist made the claim                                             |
| Verified?    | ✅ / ⚠️ Was it checked?                                                     |
| Method       | Which verification path: `aws-docs` / `aws-knowledge` / `context7` / `NONE` |
| Doc URL      | Link to the official AWS doc that confirms/denies                           |
| Result       | ✅ Confirmed / ❌ Denied / ⚠️ Partially correct / ⚠️ UNVERIFIED             |

**Gate Condition**: Phase 4 (Cross-Validation) is BLOCKED until all `⚠️ AWS_CLAIM:` items from specialist reports are verified. Exception: DEGRADED mode (all MCP unavailable) — Phase 4 proceeds with ⚠️ UNVERIFIED claims prominently flagged. Specialists prefix their AWS claims with `⚠️ AWS_CLAIM:` to flag them for the orchestrator.

### Quality Standards (Phase 16 additions)

#### 🌐 Multi-Language Output (Separate Files)

Analysis output is generated as **3 separate files** — one per language (EN, JP, VI). Each file is complete and standalone.

| File Suffix | Language   | Description                             |
| ----------- | ---------- | --------------------------------------- |
| `-en.md`    | English    | Primary analysis file (written first)   |
| `-jp.md`    | Japanese   | Full translation, code stays in English |
| `-vi.md`    | Vietnamese | Full translation, code stays in English |

**Rules**: 1 language per file. No mixed-language headings. No parenthetical translations. JP/VI include bilingual glossary.

**File naming**: `doc/analysis/{date}-{module}-analysis-{lang}.md`

#### 📍 Evidence-Based Finding Format

Top 5 CRITICAL/HIGH findings MUST use the full evidence format:

1. **Call stack** — Numbered `file:line → function()` execution path
2. **Code evidence** — Max 5 lines with comment explaining relevance
3. **Impact** — Quantified where possible
4. **Fix** — Concrete code suggestion

Remaining findings use compact table format in Appendix.

**Conciseness rules**: Max 2 sentences per finding description. Top 10 in main body, rest in Appendix.

#### ⛔ NO ASCII Art — Absolute Prohibition

All diagrams MUST be Mermaid (validated via `mcp_mermaid-mcp`). ASCII art (box-drawing characters, `├──`, `└──`, `-->`, `|---|`) is absolutely forbidden in output documents. Specialists should describe diagram intent in plain text; doc-generator renders as Mermaid.

## Design Principles & Motivations

> **Note**: The principles below are design decisions based on industry observations and common AI engineering patterns. They are NOT academic citations. Specific numbers are approximate and should not be cited as precise research findings.

| Principle                                                             | Motivation                                | Applied As                     |
| --------------------------------------------------------------------- | ----------------------------------------- | ------------------------------ |
| Most developers use AI but fewer fully trust output                   | Need for structured verification          | Trust Paradox → 3-Engine Model |
| AI-generated code may contain vulnerabilities                         | Cannot skip human review                  | "Verification Debt" concept    |
| Semi-formal reasoning (assumptions → trace → proof) improves accuracy | Forcing explicit reasoning reduces errors | Structured Reasoning (L2)      |
| RAG reduces hallucination in code analysis                            | Ground claims in live docs                | RAG layer (L3)                 |
| Combining LLM + SAST tools reduces false positives                    | Multiple verification sources             | Static Verification (L4)       |
| Agentic AI (read repo + run tools) outperforms plain LLM              | Tool use enables verification             | Agentic layer (L5)             |
| Adversarial code comments can mislead AI reviewers                    | AI has security blind spots               | AI security limitations        |
| Review the AI process, not just output                                | Process transparency matters              | AI Metadata requirement        |
| AI is strong at patterns, weak at business logic intent               | Cannot replace domain experts             | AI limitation awareness        |
| AI struggles with cross-service flows (>10 microservices)             | Complex integrations need human review    | Cross-service limitation       |
| Long-term AI code generation can silently degrade quality             | Need consistency auditing                 | Hidden tech debt awareness     |
