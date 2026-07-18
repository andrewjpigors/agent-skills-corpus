---
name: governance
description: >
  Use when starting a project and needing architecture documentation, logging a
  significant technical decision, checking which governance gates are missing or
  incomplete, drawing architecture diagrams, or auditing code for security and
  tech debt, or sanitizing PII and internal network topologies. Triggers: "set up the project", "write an ADR", "verify compliance",
  "draw [diagram type]", "audit this", "audit <path>", "sanitize PII".
---

# Governance — Master Skill

## Skill Classification

| Mode       | Class                          | What it means                                                       |
| ---------- | ------------------------------ | ------------------------------------------------------------------- |
| `verify`   | DETERMINISTIC                  | File existence + pattern checks. Same input → same output.          |
| `adr`      | DETERMINISTIC                  | Format enforcement. Structural rules, not opinions.                 |
| `scaffold` | GROUNDED                       | TOGAF-mapped structure. Sources cited with edition and date.        |
| `diagram`  | MODEL-JUDGMENT                 | Content is model-assessed; mandatory conditions are rule-enforced.  |
| `audit`    | MODEL-JUDGMENT + GROUNDED      | Findings require interpretation; CWE/OWASP citations are grounded.  |
| `sanitize` | DETERMINISTIC + MODEL-JUDGMENT | Regex scanning for PII, model judgment for contextual abstractions. |

**DETERMINISTIC** — findings are verifiable without AI.
**GROUNDED** — claims traceable to external authority with confidence levels.
**MODEL-JUDGMENT** — requires AI interpretation; review before acting.

---

## Mode Selection

| Mode       | Trigger Phrases                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `scaffold` | "set up the project", "init .ai-arch", "initialize governance", "scaffold architecture", "start from scratch", "do this from scratch"       |
| `adr`      | "log this decision", "write an ADR", "record this decision", any explicit framework/DB/auth/deployment/API choice                           |
| `verify`   | "verify compliance", "check governance", "check gates", "audit .ai-arch", "verify .ai-arch", "governance check", "check compliance"         |
| `diagram`  | "draw [diagram type]", "draw context", "draw ERD", "draw deployment", "draw sequence for", "draw data flow", "draw state", "draw container" |
| `audit`    | "audit this", "audit [path]", "run dev audit", "check code quality", "audit for tech debt", "security audit"                                |
| `sanitize` | "sanitize PII", "scrub the repo", "obfuscate internal IPs", "clean up personal data", "abstract hardware"                                   |

If mode is ambiguous, ask: "Which governance mode? scaffold / adr / verify / diagram / audit / sanitize"

---

---

## MODE: `scaffold`

Initialize the `.ai-arch/` Architecture Repository for any new or existing project.

### When to scaffold

- User starts a new project
- User says "set up the project properly" or "do this from scratch"
- A project directory exists but has no `.ai-arch/` folder
- User asks about project documentation, ADRs, or NFRs

### Step 1 — Ask for project context (if not already known)

Confirm before creating files:

1. What does this project do? (one sentence)
2. Who are the users? (list roles)
3. What is the deployment target? (NAS, cloud, laptop, etc.)
4. What data does it handle? (PII? Financial? Public?)
5. What is the timeline / team size?

Extract from existing context if already described. Do NOT ask questions already answered.

### Step 2 — Create the .ai-arch/ directory structure

Create all 10 files in `<project-root>/.ai-arch/` and a `charts/` directory:

```text
.ai-arch/
  01_README.md                  ← What this folder is + TOGAF mapping
  02_PROJECT_CONTEXT.md         ← Why, who, what it is NOT
  03_PRE_PROJECT_CHECKLIST.md   ← 6 governance documents (fill from context)
  04_ASSUMPTIONS.md             ← What must be true for the system to work
  05_COMPLEXITY_ANALYSIS.md     ← Effort estimate with reasoning
  06_ARCHITECTURE_OVERVIEW.md   ← Conceptual layer diagram prose (HTML Link)
  07_ARCHITECTURE_DECISIONS.md  ← Empty ADR log, ready for entries
  08_AI_ASSISTANCE_MAP.md       ← Track AI-generated vs human files
  09_API_REFERENCE.md           ← Core API endpoint catalog
  10_OBSERVABILITY_STRATEGY.md  ← L.M.T.A Framework (Logs, Metrics, Traces, Alerts)
  charts/                       ← Dynamic HTML Architecture Charts
  AUDIT_SCORES.json             ← Audit history (created on first audit run)
  pc2e/                         ← PC2E Mandatory Workspaces files
    SYSTEM_LOG.md
    PORTS.md
    Project_Context.md
    SECURITY_FRAMEWORK.md
```

### Step 3 — Generate ARCHITECTURE_OVERVIEW.md

**1. Create the high-res HTML diagram in `charts/architecture-overview.html`:**
Do NOT use Mermaid. Use HTML/CSS Grid and Flexbox to build a responsive, native architecture diagram.

- Must include a "Download as PNG" button natively powered by `<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>` and a simple click handler.
- Build a dark-mode layered stack: Business → Integration → Intelligence → Delivery
- Include vertical pillars for Data Persistence and Security/Gov
- Avoid absolute positioning; use CSS Flexbox/Grid

**2. Create `06_ARCHITECTURE_OVERVIEW.md`:**

- Do NOT include Mermaid blocks.
- Provide a clear markdown link: `👉 **[View the High-Res HTML Layered Architecture](charts/architecture-overview.html)**`
- Follow the link with: one prose paragraph per layer + one per cross-cutting bar.

### Step 4 — Add .ai-arch/ to .gitignore

```gitignore
# AI Architecture Repository — internal governance notes, gitignored
.ai-arch/
```

### Step 5 — Fill each file from project context

- **PRE_PROJECT_CHECKLIST.md**: Complete all 6 sections — Business Case, Stakeholder RACI, NFRs (minimum: performance, security, data retention), Data Classification, Risk Register, Assumptions.
- **COMPLEXITY_ANALYSIS.md**: Traditional dev vs AI-augmented table, effort drivers, human judgment tasks.
- **ARCHITECTURE_DECISIONS.md**: Create ADR-001 immediately (framework/stack choice vs alternatives).
- **01_README.md**: Include TOGAF ADM Deliverable Mapping (see table below).

**TOGAF ADM Deliverable Mapping (embed in 01_README.md):**

```markdown
## TOGAF ADM Deliverable Mapping

| File | TOGAF Phase | Deliverable |
|------|-------------|-------------|
| 01_README.md | Preliminary | Architecture Repository orientation + TOGAF mapping |
| 02_PROJECT_CONTEXT.md | Phase A | Statement of Architecture Work |
| 03_PRE_PROJECT_CHECKLIST.md | Preliminary | Architecture Principles + Capability Assessment |
| 04_ASSUMPTIONS.md | Phase A | Architecture Vision — assumptions & constraints |
| 05_COMPLEXITY_ANALYSIS.md | Phase A | Architecture Vision — feasibility & effort |
| 06_ARCHITECTURE_OVERVIEW.md | Phase A | Architecture Vision (HTML layer diagram) |
| 07_ARCHITECTURE_DECISIONS.md | A–D | Architecture Decision Log (append-only) |
| 08_AI_ASSISTANCE_MAP.md | B–D | Architecture Definition Document — provenance |
| 09_API_REFERENCE.md | Phase C | Architecture Definition Document — interfaces |
| 10_OBSERVABILITY_STRATEGY.md | F–G | Migration Planning / Implementation Governance |
| charts/ | B–D | Domain views |

Source: TOGAF® Standard, 10th Edition (Open Group, 2022). Confidence: HIGH.
```

**Interview Answer (embed in PRE_PROJECT_CHECKLIST.md bottom):**
> "Six documents before any code is written: Business Case, Stakeholder RACI, NFRs, Data Classification, Risk Register, and Assumptions. The most commonly skipped and most consequential is NFRs — without them, you cannot justify a single architecture decision."

### Scaffold Rules

- Never leave placeholder text in generated files
- ADRs must always include rejected alternatives — a decision without alternatives is a guess
- AI_ASSISTANCE_MAP.md must list every file created by AI in this session
- ASSUMPTIONS.md must distinguish: infrastructure assumptions (could be wrong) vs business assumptions (require domain expert)

---

---

## MODE: `adr`

Write a new Architecture Decision Record.

### When to write ADR

- User chooses a framework, library, or tool
- User chooses a deployment model, data storage, auth method, API design, AI model, caching strategy
- User explicitly asks to log an architecture decision
- A major design choice is made during implementation

### ADR Format (strict)

```markdown
## ADR-XXX — [Decision Title] ([DATE YYYY-MM-DD])

**Context:**
[2-4 sentences. What was the situation? What were we trying to achieve?]

**Decision:** [One clear sentence stating what was chosen.]

**Consequences (+):**
- [Positive outcome 1]
- [Positive outcome 2]

**Consequences (−):**
- [Negative outcome or trade-off 1]
- [Negative outcome or trade-off 2]

**Rejected alternatives:** [Alternative A] ([why rejected]); [Alternative B] ([why rejected]).
```

### ADR Rules

1. **Rejected alternatives are mandatory.** Minimum 2 per ADR. A decision without alternatives did not consider the trade-space.
2. **ADRs are never edited.** If reversed, write a new ADR and mark the old one `[SUPERSEDED by ADR-XXX]`.
3. **Number sequentially.** Read existing ARCHITECTURE_DECISIONS.md to determine the next number.
4. **Date it.** When the decision was made, not documented.
5. **Consequences must be honest.** List real negatives. An ADR with only positives was written by a salesperson.
6. Append to the bottom of 07_ARCHITECTURE_DECISIONS.md. Also update 08_AI_ASSISTANCE_MAP.md.

---

---

## MODE: `verify`

Deterministically check which governance gates are missing or incomplete.

### Flags

- **Default (no flag):** `--fast` mode. File existence and pattern matching only. **DETERMINISTIC** — findings are reproducible without AI interpretation.
- **`--deep` flag:** Also checks file contents for semantic completeness. **MODEL-JUDGMENT** — output labelled as such. User specifies: "verify compliance --deep" or "deep governance check".

### Gate 1 — .ai-arch/ presence

Check: does `.ai-arch/` exist with all 10 required files?

Required files: `01_README.md`, `02_PROJECT_CONTEXT.md`, `03_PRE_PROJECT_CHECKLIST.md`, `04_ASSUMPTIONS.md`, `05_COMPLEXITY_ANALYSIS.md`, `06_ARCHITECTURE_OVERVIEW.md`, `07_ARCHITECTURE_DECISIONS.md`, `08_AI_ASSISTANCE_MAP.md`, `09_API_REFERENCE.md`, `10_OBSERVABILITY_STRATEGY.md`

`PASS`: all 10 present | `PARTIAL`: some missing | `FAIL`: .ai-arch/ absent

### Gate 2 — ADR quality

For each ADR in `07_ARCHITECTURE_DECISIONS.md`:

- `PASS`: contains `**Rejected alternatives:**` with visible text after it
- `INCOMPLETE`: pattern found but empty or just a dash
- `MISSING`: no ADRs present at all

Report: N of M ADRs are compliant.

### Gate 3 — Data classification consistency

Read `03_PRE_PROJECT_CHECKLIST.md` → locate Data Classification section.

**--fast mode (existence only):**

- Sensitive/sovereign data present → check `charts/dataflow.html` exists
- Relational DB confirmed (grep `07_ARCHITECTURE_DECISIONS.md` for: PostgreSQL/MySQL/SQLite/postgres/mariadb) → check `charts/erd.html` exists
- Sovereign/edge/hybrid infra (grep for: sovereign/edge/hybrid/NAS/on-premise) → check `charts/deployment.html` exists

**--deep mode (content check, MODEL-JUDGMENT):**

- If `charts/erd.html` exists: does it contain entity definitions with PII annotations where required?
- If `charts/dataflow.html` exists: does it show data crossing trust boundaries?
- Label all content findings as MODEL-JUDGMENT in output.

### Gate 4 — AI component governance

Grep `06_ARCHITECTURE_OVERVIEW.md` and `03_PRE_PROJECT_CHECKLIST.md` for: `LLM / AI / Ollama / agent / GPT / model / inference / transformer`

If found:

- `PASS`: PRE_PROJECT_CHECKLIST references any documented AI runtime governance framework
- `FAIL`: AI component found with no governance reference
- Remediation: Document your AI governance framework in the Risk Register. Minimum controls required: anti-hallucination rules, prompt injection defence (structural fencing), context window bounding, phantom commitment prevention, mandatory audit logging.

### Gate 5 — NFR completeness

`03_PRE_PROJECT_CHECKLIST.md` must contain minimum 3 NFR types:

- Performance (grep: performance/latency/response time/throughput/SLA)
- Security (grep: security/authentication/authorisation/OWASP)
- Data retention (grep: retention/deletion/archive/purge)

`PASS`: all 3 found | `PARTIAL`: 1-2 found | `FAIL`: none

### Gate 6 — Observability Readiness

Check `10_OBSERVABILITY_STRATEGY.md` for L.M.T.A (Logs, Metrics, Traces, Alerts) coverage.

- **--fast mode**: File exists.
- **--deep mode**: Check if strategy for Logs, Metrics, Traces, and Alerts are defined and aligned with standards (e.g. OpenTelemetry).

`PASS`: LMTA defined | `PARTIAL`: Incomplete | `FAIL`: File missing or empty

### Delta from AUDIT_SCORES.json

If `AUDIT_SCORES.json` exists in `.ai-arch/`: read the last verify run and show which gates changed status since then. No delta if no history.

### Output format

```markdown
# Compliance Verification Report

**Repo:** [path]  **Date:** [timestamp]  **Mode:** [--fast / --deep]

## Gate Results

| Gate | Status | Detail |
|------|--------|--------|
| .ai-arch/ presence | ✅ PASS | 10/10 files present |
| ADR quality | ⚠️ PARTIAL | 2 of 4 ADRs missing rejected alternatives |
| Data classification | ✅ PASS | dataflow.html and erd.html present |
| AI governance | ❌ FAIL | AI component found; no governance framework documented in checklist |
| NFR completeness | ✅ PASS | Performance, Security, Retention confirmed |
| Observability | ✅ PASS | LMTA Strategy defined |

**Score:** 4.5/6  **Status:** PARTIALLY COMPLIANT

## Findings

### ❌ Gate 4 — AI Governance Missing
- **File:** .ai-arch/03_PRE_PROJECT_CHECKLIST.md
- **Finding:** ARCHITECTURE_OVERVIEW references Ollama. No runtime governance framework documented.
- **Remediation:** Document your AI governance framework in the Risk Register section.
  Minimum controls: anti-hallucination rules, prompt injection defence (structural fencing),
  context window bounding, phantom commitment prevention, mandatory audit logging,
  loop-breaking protocol.
- **Class:** DETERMINISTIC (AI component detected by grep)

### ⚠️ Gate 2 — ADR-003 Missing Rejected Alternatives
- **File:** .ai-arch/07_ARCHITECTURE_DECISIONS.md
- **Finding:** ADR-003 — pattern "**Rejected alternatives:**" not found.
- **Remediation:** Add minimum 2 rejected alternatives.
- **Class:** DETERMINISTIC (pattern match)
```

After each verify run, append to `AUDIT_SCORES.json`:

```json
{
  "date": "YYYY-MM-DD",
  "mode": "--fast",
  "gates": {"presence": "PASS", "adr_quality": "PARTIAL", "data_class": "PASS", "ai_governance": "FAIL", "nfr": "PASS", "observability": "PASS"},
  "score": 4.5
}
```

---

---

## MODE: `diagram`

Generate dynamic HTML/CSS charts in `.ai-arch/charts/`. **Do NOT use Mermaid.**

### Invocation

User names the diagram: "draw context diagram", "draw ERD", "draw sequence for [flow]", "draw deployment diagram", "draw state diagram for [entity]", "draw data flow", "draw container diagram".

If not explicitly requested, only `06_ARCHITECTURE_OVERVIEW.md` (the conceptual layer diagram) is generated — always mandatory.

### HTML Generation Rules

- **No Mermaid:** Build visual diagrams natively using HTML, CSS Grid, and CSS Flexbox. Avoid brittle absolute positioning.
- **Export Script:** Every generated `.html` chart MUST include `<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>` and a simple "Download as PNG" button at the top right of the UI.

### Mandatory conditions (rule-enforced)

| Diagram                  | Mandatory when                                                      |
| ------------------------ | ------------------------------------------------------------------- |
| `charts/erd.html`        | Relational DB confirmed in any ADR                                  |
| `charts/dataflow.html`   | Any data classified sensitive or sovereign in PRE_PROJECT_CHECKLIST |
| `charts/deployment.html` | Sovereign, edge, or hybrid infrastructure present                   |

### Sub-diagrams

**1. Context Diagram (C1) — `charts/context.html`**
System as single box at centre. External actors and services as surrounding boxes. Arrows show interaction direction and what flows. Nothing inside the system box — outside-in view only.

**2. Container Diagram (C2) — `charts/containers.html`**
Each major deployable unit as a box, labelled with technology (e.g., "React + Next.js", "FastAPI", "Ollama"). Arrows between units labelled with protocol. Every technology here must have a corresponding ADR in `07_ARCHITECTURE_DECISIONS.md`.

**3. Sequence Diagram — `charts/sequence_[flow_name].html`**
Vertical timelines or swimlanes per actor/component. Horizontal or flowing vertical blocks in order. Governance gates and HitL checkpoints shown as explicit steps. Max 15 interactions per diagram — break into sub-flows if longer.

**4. Deployment Diagram — `charts/deployment.html`**
Physical/virtual machines, containers, networks, security zones. Shows where each container runs. Network boundaries as nested CSS Grid rectangles. Data flow arrows labelled with what crosses each boundary and whether it's a trust/sovereignty boundary.

**5. State Diagram — `charts/state_[entity_name].html`**
States as nodes, transitions as arrows labelled with trigger event. Guards in square brackets [condition]. Governance gates as explicit states. One file per lifecycle entity. Only for entities whose lifecycle drives business logic.

**6. ERD — `charts/erd.html`**
Entities with key attributes laid out in grid cards. Relationships with cardinality. Primary and foreign keys marked. Any entity containing PII or sensitive data must be annotated with its classification level. Must align with data classification in PRE_PROJECT_CHECKLIST.

**7. Data Flow Diagram — `charts/dataflow.html`**
Data sources (left) → processing/transformation (middle) → destinations (right). Arrows labelled with what data moves and whether it crosses a trust or sovereignty boundary.

### Folder structure

```text
.ai-arch/
├── 01_README.md
├── 02_PROJECT_CONTEXT.md
├── 03_PRE_PROJECT_CHECKLIST.md
├── 04_ASSUMPTIONS.md
├── 05_COMPLEXITY_ANALYSIS.md
├── 06_ARCHITECTURE_OVERVIEW.md    ← always mandatory
├── 07_ARCHITECTURE_DECISIONS.md
├── 08_AI_ASSISTANCE_MAP.md
├── 09_API_REFERENCE.md
├── 10_OBSERVABILITY_STRATEGY.md
├── AUDIT_SCORES.json
├── pc2e/
│   ├── SYSTEM_LOG.md              ← PC2E Mandatory Audit Trail
│   ├── PORTS.md                   ← PC2E Mandatory Port Ledger
│   ├── Project_Context.md         ← PC2E Mandatory High-Level Service Map
│   └── SECURITY_FRAMEWORK.md      ← PC2E Mandatory Security Standards
└── charts/
    ├── context.html
    ├── containers.html
    ├── sequence_[flow].html
    ├── deployment.html
    ├── state_[entity].html
    ├── erd.html
    └── dataflow.html
```

---

---

## MODE: `audit`

Six-pillar code audit with CWE/OWASP citations and weighted comparable scoring.

### Step 1 — Determine scope

If path or context already specified, proceed. Otherwise ask: "What should I audit? (directory / feature branch / entire project)"

### Step 2 — Check for audit history

Read `.ai-arch/AUDIT_SCORES.json` if it exists. If present, show delta after scoring.

### Pillars

Execute all six in order. Severity levels: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

---

#### Pillar 1: Tech Debt

**Check for:**

- Dead code, unused imports, unused dependencies
- TODO/FIXME/HACK/XXX comments (count and categorise)
- Duplicated logic (copy-paste patterns)
- Overly complex functions (cyclomatic complexity > 10, functions > 50 lines)
- Outdated dependencies (major version behind)
- Missing or stale tests for critical paths
- Inconsistent naming conventions
- Hardcoded magic numbers or strings without constants
- Circular dependencies
- Missing error handling (bare catches, swallowed errors)

**Tools:** `grep_search` for TODOs/FIXMEs/hardcoded values, `list_dir` + `view_file` for structure/complexity, `run_command` for `npm outdated` or equivalent, ESLint MCP (`lint-files`) if available.

---

#### Pillar 2: Security

**Check for:**

- Hardcoded secrets (grep: `password=`, `api_key=`, `secret=`, `token=`, base64 credentials, bearer tokens)
- SQL injection (string concatenation in queries vs parameterised)
- XSS (unsanitised input rendered in HTML/JSX)
- CSRF (forms without tokens, missing SameSite cookies)
- Insecure dependencies (`npm audit` or equivalent)
- Missing auth/authorisation on routes
- Overly permissive CORS
- Missing rate limiting on public endpoints
- PII in logs
- Insecure file operations (path traversal, unrestricted uploads)
- Missing input validation on API boundaries
- Docker security (running as root, mounting docker.sock, privileged mode)

**Every security finding MUST cite:**

```text
- **CWE:** CWE-[ID] ([name])
- **OWASP:** A[NN]:2025 ([category name])

```text
If no CWE/OWASP mapping: downgrade to `INFO`. Do not fabricate mappings.

**Reference table (embed, do not hallucinate IDs):**

| Issue                    | CWE      | OWASP 2025                                |
| ------------------------ | -------- | ----------------------------------------- |
| Hardcoded credentials    | CWE-798  | A07: Authentication Failures              |
| SQL injection            | CWE-89   | A05: Injection                            |
| XSS                      | CWE-79   | A05: Injection                            |
| CSRF                     | CWE-352  | A01: Broken Access Control                |
| Path traversal           | CWE-22   | A01: Broken Access Control                |
| Missing rate limiting    | CWE-770  | A06: Insecure Design                      |
| Missing auth on route    | CWE-306  | A07: Authentication Failures              |
| Insecure dependency      | CWE-1395 | A03: Software Supply Chain Failures       |
| PII in logs              | CWE-532  | A09: Security Logging & Alerting Failures |
| Overly permissive CORS   | CWE-942  | A02: Security Misconfiguration            |
| Missing input validation | CWE-20   | A05: Injection                            |
| Privileged container     | CWE-250  | A02: Security Misconfiguration            |

**AI Component Detection (sub-check within Pillar 2):**

Grep for: `openai`, `anthropic`, `gemini`, `ollama`, `langchain`, `langgraph`, `crewai`, `agent`, `llm`, `inference`

If found and no governance documented:

```text
Severity: HIGH
CWE: CWE-1188 (Insecure Default Initialization — insufficient AI oversight)
OWASP: A02: Security Misconfiguration
Description: AI component detected without documented runtime governance framework.
Remediation: Apply a structured AI governance framework covering:
  - Anti-hallucination rules (verify before claiming, cite sources)
  - Prompt injection defence (wrap untrusted inputs in explicit structural fences)
  - Context window bounding (hard clamp num_ctx at API boundary to prevent VRAM exhaustion)
  - Loop-breaking protocol (detect and break agent runaway loops)
  - Phantom commitment prevention (no post-session notifications promised)
  - Mandatory audit logging (all AI decisions logged with rationale)
Document the chosen framework in .ai-arch/03_PRE_PROJECT_CHECKLIST.md Risk Register.
```

If a documented governance framework is already referenced/applied: downgrade to `INFO — AI governance present`.

**Tools:** `grep_search`, `run_command` for `npm audit`, `docker inspect`.

---

#### Pillar 3: Deployability

**Check for:**

- Missing or broken Dockerfile / docker-compose.yml
- Missing health check endpoints
- Missing or incomplete CI/CD configuration
- Environment-specific hardcoding (localhost URLs, hardcoded ports in app code)
- Missing `.env.example` or undocumented environment variables
- Build reproducibility (pinned versions, lockfile present)
- Missing graceful shutdown handling (SIGTERM/SIGINT)
- Database migration strategy
- Missing production logging
- Unnecessary dev dependencies in production image
- Missing resource limits in container config
- Rollback strategy documentation

**Tools:** `view_file` for Dockerfiles, compose files, CI configs. `grep_search` for hardcoded URLs/localhost. `list_dir` to verify expected files.

---

#### Pillar 4: Scalability

**Check for:**

- N+1 query patterns (ORM calls inside loops)
- Missing database indexes on filtered/joined columns
- Synchronous blocking operations in request handlers
- Missing caching strategy
- Monolithic coupling (no clear service boundaries)
- Missing pagination on list endpoints
- Large payloads without streaming
- Missing connection pooling
- Single points of failure (no failover)
- Missing queue/async processing for heavy operations
- Unbounded data growth without archival
- Missing observability (no metrics, no tracing)

**Tools:** `grep_search` for query patterns, `view_file` for DB queries and API handlers.

---

#### Pillar 5: Privacy (PDPA/GDPR)

**Check for:**

- PII collection without documented purpose (names, emails, phone, NRIC, addresses)
- Missing data retention policies
- PII in logs, error messages, stack traces
- Missing encryption at rest and in transit
- Missing consent mechanisms
- Missing data subject access/deletion capabilities
- Cross-border data transfer without safeguards
- Third-party sharing without data processing agreements
- Overly broad data collection
- Missing anonymisation/pseudonymisation for analytics
- Missing audit trail for PII access

**Tools:** `grep_search` for PII field patterns (email, phone, nric, address in schemas), `view_file` for data models and API responses.

---

#### Pillar 6: Observability

**Check for:**

- Missing structured logging framework (e.g., Winston, Pino, Serilog)
- Missing distributed tracing (e.g., OpenTelemetry, Jaeger, Zipkin)
- Missing metrics exposure (e.g., Prometheus `/metrics` endpoint)
- Missing comprehensive health endpoints (`/health/liveness`, `/health/readiness`)
- Hardcoded log destinations instead of stdout/stderr
- Uncaught exception handlers missing logging
- Missing alert routing definitions
- Lack of correlation IDs across distributed boundaries

**Tools:** `grep_search` for logger configurations, OpenTelemetry SDKs, health endpoints, and `view_file` for observability strategy (`10_OBSERVABILITY_STRATEGY.md`).

---

### Step 3 — Score and output

**Weighting formula:**

```text
Pillar weights (sum = 100%):
  Security:       25%
  Tech Debt:      20%
  Deployability:  15%
  Privacy:        15%
  Observability:  15%
  Scalability:    10%

Per-finding deductions (pillar score starts at 10, minimum 0):
  CRITICAL: -3.0
  HIGH:     -2.0
  MEDIUM:   -0.5
  LOW:      -0.1

Weighted overall = Σ (pillar_score × pillar_weight)
```

This formula is fixed. Every audit uses it. Two audits of the same repo are comparable.

**Output format:**

Produce artifact `audit_report.md`:

```markdown
# Dev Audit Report

**Target:** [path]  **Date:** [timestamp]  **Formula version:** 1.1

## Risk Scorecard

| Pillar | Weight | Score | CRITICAL | HIGH | MEDIUM | LOW |
|--------|--------|-------|----------|------|--------|-----|
| Security | 25% | X.X/10 | N | N | N | N |
| Tech Debt | 20% | X.X/10 | N | N | N | N |
| Deployability | 15% | X.X/10 | N | N | N | N |
| Privacy | 15% | X.X/10 | N | N | N | N |
| Observability | 15% | X.X/10 | N | N | N | N |
| Scalability | 10% | X.X/10 | N | N | N | N |
| **Weighted Overall** | 100% | **X.X/10** | **N** | **N** | **N** | **N** |

## Score History (from AUDIT_SCORES.json)

[If history exists:]
| Date | Security | Tech Debt | Deploy | Privacy | Observability | Scale | Overall | Δ Overall |
|------|----------|-----------|--------|---------|---------------|-------|---------|-----------|
| 2026-05-01 | 6.0 | 8.0 | 8.5 | 9.0 | N/A | 7.5 | 7.45 | — |
| 2026-06-17 | 7.5 | 8.0 | 9.0 | 9.0 | 8.0 | 8.0 | 8.05 | +0.60 ↑ |

## Findings

### Security

#### [HIGH] Missing Rate Limiting on Public Endpoints
- **File:** [path#L10-L25]
- **Description:** POST /api/ml/data/upload has no rate limiting middleware.
- **Impact:** Endpoint is vulnerable to resource exhaustion.
- **CWE:** CWE-770 (Allocation of Resources Without Limits)
- **OWASP:** A06:2025 — Insecure Design
- **Remediation:** Add rate-limit middleware (e.g., `express-rate-limit`, `slowapi`). Set max 10 requests/minute per IP.
- **Effort:** small
- **Class:** MODEL-JUDGMENT (confirmed by reading route handler)

...

## Priority Remediation Queue

Ordered by risk × effort (highest impact, lowest effort first):

1. [CRITICAL] ...
2. [HIGH] Missing Rate Limiting — small effort
3. ...

## Deferred / Accepted Risk

- [item] — rationale
```

**Append to `AUDIT_SCORES.json` after every audit:**

```json
{
  "date": "YYYY-MM-DD",
  "target": "[path audited]",
  "formula_version": "1.1",
  "scores": {
    "security": 7.5,
    "tech_debt": 8.0,
    "deployability": 9.0,
    "privacy": 9.0,
    "observability": 8.0,
    "scalability": 8.0,
    "weighted_overall": 8.05
  },
  "finding_counts": {"critical": 0, "high": 1, "medium": 4, "low": 6}
}
```

AUDIT_SCORES.json stores an array of entries. Append, never overwrite.

---

### Audit Rules

1. **Read before judging.** Open and inspect every file referenced. Do not guess at contents.
2. **Cite with confidence.** Every finding links to a specific file and line range. Confidence: HIGH only if file was read.
3. **No false positives.** Uncertain findings: mark `INFO` with "verify manually" note, not `HIGH`.
4. **Score honestly.** 10/10 means you checked and found zero issues — not that you skipped checking.
5. **CWE/OWASP mandatory in Pillar 2.** No citation = downgrade to INFO.
6. **Formula is fixed.** Do not adjust weights per project. Comparability depends on consistency.
7. **Respect scope.** Audit only what was requested.

---

## MODE: `sanitize`

Perform a comprehensive scrubbing of Personally Identifiable Information (PII) and internal network/hardware topologies to prepare a repository for public sharing.

### When to sanitize

- User asks to "sanitize PII" or "prepare repo for public sharing"
- User explicitly requests scrubbing internal IPs or hardware mentions

### Step 1 — Network & Hardware Obfuscation

**Check for:**

- Internal IP addresses (`192.168.x.x`, `10.x.x.x`, `100.x.x.x` etc.)
- Specific proprietary hardware or internal network tooling (e.g., `NAS`, `Synology`, `Tailscale`, `Mac Mini M4`, `DXP4800`)

**Action:**

- Replace internal IP addresses with generic placeholder domains (e.g., `internal.network.local`) or `1.2.3.4` for examples.
- Abstract hardware to generic cloud-native equivalents:
  - `NAS` / `Synology` → `Edge Storage Node`
  - `Tailscale` / `ZeroTier` → `Encrypted Mesh VPN`
  - `Mac Mini M4` → `Edge Compute Node`

### Step 2 — Personal Data (PII) Scrubbing

**Check for:**

- Developer real names and GitHub handles (e.g., `user_name`, `user_handle`)
- Personal email addresses and domains
- `*Maintained by...*` signatures in markdown documentation

**Action:**

- Remove developer signatures from markdown files entirely.
- Replace personal emails with generic `admin@example.com` placeholders.
- Replace personal domains with generic `example.com` routing.

### Step 3 — Gitignore Enforcement

Ensure the `.gitignore` explicitly prevents the commitment of:

- Internal system datasets (`*.csv`, `*.parquet`)
- Serialized ML models (`*.pkl`, `*.pt`)
- Analytics and plot output reports

### Sanitize Rules

1. **Precision:** Use rigorous regex (`grep_search`) to ensure all instances are found before applying changes.
2. **Context Awareness:** Do not break the compilation of the code; use `multi_replace_file_content` to surgically replace strings without damaging syntax.
3. **Never push automatically:** Prepare the commit, but allow the user to push it unless explicitly instructed.

---

---

## General Rules (All Modes)

1. **Read before judging.** Open every file you reference. No guessing at contents. (Anti-Hallucination)
2. **Cite with confidence.** Every external claim references a specific source. HIGH = verified. MEDIUM = inferred. LOW = speculative.
3. **No placeholder text.** Every generated file is fully populated from context.
4. **ADRs require rejected alternatives.** A decision without alternatives is a guess.
5. **Score formula is version-controlled.** Formula version 1.1. If formula changes, bump version. Old scores remain comparable within their version.
6. **AI components require governance.** Any AI component detected in audit or verify mode must have a documented governance framework. Surface the six minimum controls: anti-hallucination, prompt injection defence (structural fencing), context window bounding, phantom commitment prevention, mandatory audit logging, loop-breaking protocol.
7. **Diagram mandatory conditions are enforced, not optional.** If relational DB → ERD required. If sensitive data → DATAFLOW required. If sovereign infra → DEPLOYMENT required.
8. **AUDIT_SCORES.json is append-only.** Never overwrite history.
