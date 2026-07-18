---
name: knowledge
metadata:
  compatible_agents:
    - claude-code
  tags:
    - documentation
    - onboarding
    - adr
    - faq
    - knowledge-base
    - changelog
    - runbook
    - docs-as-code
    - docs-linting
    - support
  version: "1.0.0"
  author: agentden
  phase: knowledge
  sdlc_position: 6
  prerequisites:
    - discovery
    - planning
  produces:
    - documentation-scaffold
    - product-specification
    - versioned-roadmap
    - onboarding-guide
    - documentation-health-report
    - operational-runbook
    - support-cluster
description: >
  Comprehensive Knowledge Management & Documentation skill for the SDLC.
  Governs all documentation artifacts: scaffolding, product specifications via
  interview mode, versioned roadmaps, developer onboarding guides, ADR lifecycle
  management, documentation health scoring, operational runbooks, and support
  clusters (FAQ, triage, SLA, post-mortem). Enforces documentation linting rules
  and badge standards across the entire project. Follows docs-as-code principles
  where every artifact is version-controlled, linted, and reviewed like production code.

  Trigger phrases: "write documentation", "onboard developer", "create ADR",
  "generate docs", "knowledge base", "FAQ", "runbook", "changelog",
  "documentation scaffold", "product specification", "roadmap", "doc health",
  "documentation standards", "support docs", "triage guide", "SLA template",
  "post-mortem", "doc linting", "validate docs", "developer guide".

  Tech stack assumptions:
    Frontend — Bun 1.2+ + TypeScript 5.8 (strict) + SolidJS 1.9+ + SolidStart (SSG)
               + TailwindCSS 4.1+ + Iconify-Solid
    Backend  — Java 21 + Micronaut 4.7+ + Gradle 8.13+ (Kotlin DSL)
    Containers — nginx:stable-alpine + bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl
license: MIT
---

# Knowledge Management & Documentation

> **The crown jewel documentation skill.** Produces, validates, and maintains every
> documentation artifact in the SDLC. Documentation is treated as a first-class
> product — scaffolded, linted, scored, and version-controlled alongside code.

## Overview

This skill governs the **Knowledge Management** phase of the SDLC. It produces structured, version-controlled documentation artifacts that serve as the single source of truth for the entire project. Every document follows a template, every standard is enforceable, and every artifact is scored for quality.

**Trigger when the user asks to:**
- Scaffold or restructure project documentation
- Write a product specification via guided interview
- Generate a versioned roadmap
- Create an onboarding guide for developers
- Write or manage Architecture Decision Records (ADRs)
- Validate documentation against standards
- Generate a documentation health report
- Create an operational runbook
- Build a support cluster (FAQ, triage, SLA, post-mortem)
- Generate a changelog
- Audit documentation quality and coverage

**Announce at start:** "Using the **knowledge** skill to [produce/maintain/validate] [artifact type]."

---

## Slash Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `/docs scaffold` | Scaffold full documentation structure using SDLC folder layout | `docs/` directory tree with all sections |
| `/docs spec` | Generate product specification via structured interview (3 blocks) | `docs/00-product/product-specification.md` |
| `/docs roadmap` | Generate versioned roadmap in 4 formats | `docs/00-product/roadmap.md` |
| `/docs onboarding` | Generate developer onboarding guide | `docs/02-development/onboarding-guide.md` |
| `/docs validate` | Validate documentation against linting rules and standards | Console report with violations |
| `/docs health` | Generate documentation health report with scoring (100pt scale) | `docs/health-report.md` |
| `/docs runbook` | Generate operational runbook for a service or system | `docs/03-deployment/runbook-<service>.md` |
| `/docs support` | Scaffold support cluster (FAQ, triage, SLA, post-mortem) | `docs/05-support/` directory |

---

## Phase Filtering

All commands support phase filtering to scope documentation generation:

| Flag | Scope | Documents |
|------|-------|-----------|
| `--phase pre` | Pre-development | Product spec, roadmap, architecture docs |
| `--phase during` | During development | Onboarding, API docs, runbook, changelog |
| `--phase post` | Post-development | Support cluster, FAQ, post-mortem, health report |
| `--phase all` | Full lifecycle | All documentation |

**Usage example:** `/docs scaffold --phase pre` generates only pre-development documentation.

---

## Auto-Detect Project Type

When scaffolding, automatically detect the project type to customize templates:

| Detection Signal | Project Type | Template Variant |
|-----------------|--------------|-----------------|
| `app/` + `server/` directories, `bunfig.toml` + `build.gradle.kts` | **fullstack-bun-solidjs-micronaut** | Full stack with frontend + backend sections |
| `package.json` with `solid-js`, `@solidjs/start` | **frontend-solidjs** | Frontend-only documentation |
| `build.gradle.kts` with `micronaut` plugin | **backend-micronaut** | Backend-only documentation |
| `build.gradle.kts` with `spring-boot` | **backend-spring** | Backend-only (Spring variant) |
| `package.json` with `react` | **frontend-react** | Frontend-only (React variant) |
| `Cargo.toml` | **backend-rust** | Rust backend variant |
| Mixed signals or monorepo | **monorepo** | Multi-package documentation |

**Detection procedure:**

1. Scan the root directory for marker files (`package.json`, `build.gradle.kts`, `Cargo.toml`, `go.mod`, etc.)
2. Check for sub-project directories (`app/`, `server/`, `frontend/`, `backend/`, `services/`)
3. Read relevant config files to identify frameworks and versions
4. Select the closest matching template variant
5. Present the detected type to the user for confirmation

---

## Section 1: SDLC Documentation Folder Structure

### 1.1 Complete Directory Layout

```
docs/
├── README.md                          # Documentation index and navigation
├── health-report.md                   # Latest documentation health report
│
├── 00-product/                        # Product Definition
│   ├── product-specification.md       # Full product spec (interview-generated)
│   ├── roadmap.md                     # Versioned roadmap (4 formats)
│   ├── personas.md                    # User personas
│   └── glossary.md                    # Domain glossary and terminology
│
├── 01-architecture/                   # Architecture & Design
│   ├── README.md                      # Architecture overview
│   ├── system-overview.md             # High-level system architecture
│   ├── adr/                           # Architecture Decision Records
│   │   ├── README.md                  # ADR index
│   │   ├── 0001-record-architecture-decisions.md
│   │   ├── 0002-choose-solidjs-over-react.md
│   │   └── 0003-modular-monolith.md
│   ├── data-model.md                  # Entity relationship diagram and models
│   ├── api-contracts.md               # API design and versioning strategy
│   ├── security-design.md             # Authentication, authorization, encryption
│   └── diagrams/                      # Architecture diagrams (Mermaid)
│       ├── system-context.md
│       ├── container-diagram.md
│       └── sequence-flows.md
│
├── 02-development/                    # Development Guide
│   ├── README.md                      # Dev guide index
│   ├── onboarding-guide.md            # Developer onboarding (interview-generated)
│   ├── tech-stack.md                  # Technology stack reference
│   ├── conventions.md                 # Code and style conventions
│   ├── testing-guide.md               # Testing strategy and patterns
│   ├── ci-cd.md                       # CI/CD pipeline documentation
│   └── troubleshooting.md             # Common development issues and solutions
│
├── 03-deployment/                     # Deployment & Operations
│   ├── README.md                      # Operations index
│   ├── runbook-<service>.md           # Operational runbook per service
│   ├── deployment-guide.md            # Deployment procedures
│   ├── environment-plan.md            # Environment tiers and configuration
│   ├── monitoring.md                  # Monitoring, alerting, observability
│   ├── incident-response.md           # Incident response procedures
│   └── database-operations.md         # Migration, backup, recovery procedures
│
├── 04-api/                            # API Documentation
│   ├── README.md                      # API documentation index
│   ├── openapi.yaml                   # OpenAPI 3.1 specification
│   ├── authentication.md              # Auth flows and token management
│   ├── error-codes.md                 # Error response catalog (RFC 7807)
│   ├── rate-limiting.md               # Rate limiting policies
│   └── changelog.md                   # API changelog (breaking changes)
│
└── 05-support/                        # Support & Maintenance
    ├── README.md                      # Support documentation index
    ├── faq.md                         # Frequently asked questions
    ├── triage-guide.md                # Issue triage classification and workflow
    ├── sla.md                         # Service Level Agreements
    ├── post-mortem-template.md        # Post-mortem / incident review template
    └── known-issues.md                # Known issues and workarounds
```

### 1.2 Section Purpose and Ownership

| Section | SDLC Phase | Primary Owner | Audience |
|---------|-----------|---------------|----------|
| `00-product/` | Pre-development | Product Manager | All stakeholders |
| `01-architecture/` | Pre-development | Tech Lead | Engineers |
| `02-development/` | During development | Engineering Team | New developers, contributors |
| `03-deployment/` | During/Post development | Platform / DevOps | SRE, Operations |
| `04-api/` | During development | Backend Engineers | Frontend engineers, API consumers |
| `05-support/` | Post-development | Support Team | End users, support staff |

### 1.3 Naming Conventions

| Artifact | Pattern | Example |
|----------|---------|---------|
| Product docs | `kebab-case.md` | `product-specification.md` |
| ADR files | `NNNN-kebab-case-title.md` | `0003-modular-monolith.md` |
| Runbooks | `runbook-<service>.md` | `runbook-auth-service.md` |
| Diagrams | `kebab-case.md` (with Mermaid) | `system-context.md` |
| API specs | `openapi.yaml` | `openapi.yaml` |
| Templates | `<name>-template.md` | `post-mortem-template.md` |

---

## Section 2: Command `/docs scaffold`

### 2.1 Scaffolding Process

1. **Detect project type** using the auto-detection procedure (Section above)
2. **Confirm with user** — present detected type and proposed structure
3. **Create directory tree** — generate all directories and placeholder files
4. **Populate README files** — each section gets a README.md with a description and index
5. **Generate root docs/README.md** — master navigation document
6. **Initialize ADR directory** — create ADR index with ADR 0001 (record architecture decisions)
7. **Report** — list all created files and next steps

### 2.2 Root Documentation Index Template

```markdown
# Documentation

> Single source of truth for [Project Name].

## Quick Navigation

| Section | Description | Status |
|---------|-------------|--------|
| [Product](./00-product/) | Product specification, roadmap, personas | ![Status](https://img.shields.io/badge/status-draft-yellow) |
| [Architecture](./01-architecture/) | System design, ADRs, data models | ![Status](https://img.shields.io/badge/status-draft-yellow) |
| [Development](./02-development/) | Onboarding, conventions, testing | ![Status](https://img.shields.io/badge/status-draft-yellow) |
| [Deployment](./03-deployment/) | Runbooks, deployment, monitoring | ![Status](https://img.shields.io/badge/status-draft-yellow) |
| [API](./04-api/) | OpenAPI spec, auth, error codes | ![Status](https://img.shields.io/badge/status-draft-yellow) |
| [Support](./05-support/) | FAQ, triage, SLA, post-mortems | ![Status](https://img.shields.io/badge/status-draft-yellow) |

## Documentation Health

| Metric | Score |
|--------|-------|
| Quality | --/60 |
| SDLC Coverage | --/40 |
| **Total** | **--/100** |

Last health check: _Not yet run_

## Contributing to Documentation

- Follow the [documentation linting rules](#) (ATX headers, 2-space indent, 120-char lines)
- Use templates from `references/sdlc-templates.md`
- Run `/docs validate` before committing documentation changes
- All documentation changes require review like code changes
```

### 2.3 Section README Template

Each section directory gets a README.md following this pattern:

```markdown
# [Section Name]

> [One-line description of this documentation section]

## Documents

| Document | Description | Last Updated |
|----------|-------------|-------------|
| [document-name.md](./document-name.md) | Brief description | YYYY-MM-DD |

## Conventions

- [Section-specific conventions if any]
```

### 2.4 Post-Scaffold Verification

- [ ] All directories created with correct naming
- [ ] Each directory has a README.md
- [ ] Root docs/README.md has navigation links
- [ ] ADR directory initialized with index and ADR 0001
- [ ] All files pass documentation lint rules
- [ ] No empty files — every file has at least a header and description

---

## Section 3: Command `/docs spec` (Product Specification Interview)

### 3.1 Interview Mode Overview

The product specification is generated through a structured 3-block interview. Each block contains questions that build on the previous block's answers. The interview can be conducted in one session or across multiple sessions.

**Interview flow:**

```
Block 1: Context & Vision (10-15 min)
    │
    ▼
Block 2: Features & Requirements (20-30 min)
    │
    ▼
Block 3: Constraints & Success Criteria (10-15 min)
    │
    ▼
Generate product-specification.md
```

### 3.2 Block 1: Context & Vision

**Questions:**

1. **What is the product name and one-line description?**
   - Example: "TaskFlow — A project management tool for distributed teams"

2. **What problem does this solve? Who experiences it?**
   - Pain points, frequency, severity
   - Current workarounds and their limitations

3. **Who are the primary users? (Define 2-4 personas)**
   - For each persona: role, technical proficiency, primary goal, biggest frustration

4. **What does success look like in 6 months?**
   - Measurable outcomes (users, revenue, efficiency gains)
   - How will you know this product is working?

5. **What is the business context?**
   - Why now? Market pressure, strategic initiative, compliance requirement?
   - Build vs buy vs partner analysis

6. **What existing systems does this interact with?**
   - Upstream data sources
   - Downstream consumers
   - External APIs and integrations

**Output captured:**
```markdown
## Product Context

**Product Name:** [name]
**Tagline:** [one-line description]

### Problem Statement
[detailed problem description]

### Personas
| Persona | Role | Technical Level | Primary Goal | Key Frustration |
|---------|------|-----------------|--------------|-----------------|
| [name]  | [role] | [low/med/high] | [goal] | [frustration] |

### Success Metrics (6 months)
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [metric] | [target] | [how to measure] |

### Business Context
[why now, market context]

### System Integration
| System | Direction | Integration Type |
|--------|-----------|-----------------|
| [system] | [inbound/outbound] | [REST/webhook/database] |
```

### 3.3 Block 2: Features & Requirements

**Questions:**

1. **What are the core features (must-have for launch)?**
   - List each feature with a user story: "As a [persona], I want [action] so that [benefit]"
   - Prioritize using MoSCoW (Must / Should / Could / Won't)

2. **What non-functional requirements are critical?**
   - Performance targets (response time, throughput)
   - Availability (uptime SLA)
   - Security requirements (auth model, compliance)
   - Accessibility level (WCAG 2.2 AA default)
   - Supported browsers and devices

3. **What data does the system manage?**
   - Core entities and their relationships
   - Data volume estimates (initial, growth rate)
   - Data sensitivity classification (public, internal, confidential, restricted)

4. **What are the key user workflows?**
   - Describe 3-5 primary workflows end-to-end
   - Identify decision points and branching logic

5. **What features are explicitly out of scope?**
   - Features considered and deferred
   - Non-goals (things this product will never do)

**Output captured:**
```markdown
## Features & Requirements

### Feature Priority Matrix

| ID | Feature | User Story | MoSCoW | Epic |
|----|---------|-----------|--------|------|
| F001 | [feature] | As a [persona], I want [action] so that [benefit] | Must | [epic] |

### Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | API response time | < 200ms p95 | Must |
| NFR-002 | Availability | Uptime | 99.9% | Must |
| NFR-003 | Security | Authentication | JWT + OAuth2 | Must |
| NFR-004 | Accessibility | WCAG compliance | 2.2 AA | Should |

### Data Entities

| Entity | Description | Sensitivity | Volume Estimate |
|--------|-------------|-------------|-----------------|
| [entity] | [description] | [level] | [initial + growth] |

### Key Workflows

#### Workflow 1: [Name]
1. User [action]
2. System [response]
3. ...

### Out of Scope
- [Feature X — deferred to v2]
- [Feature Y — not planned]
```

### 3.4 Block 3: Constraints & Success Criteria

**Questions:**

1. **What are the hard constraints?**
   - Budget limits
   - Timeline deadlines
   - Technology mandates or restrictions
   - Team size and skills
   - Regulatory compliance requirements

2. **What are the technical constraints?**
   - Must integrate with existing infrastructure
   - Must support specific browsers or platforms
   - Must run on-premises / cloud / specific provider

3. **What risks could derail this project?**
   - Technical risks
   - Organizational risks
   - External risks

4. **What are the launch criteria?**
   - What must be true to consider the product "launched"?
   - Minimum acceptable quality bar

5. **Who are the stakeholders and decision makers?**
   - Who approves the spec?
   - Who has veto power?
   - Who needs to be informed?

**Output captured:**
```markdown
## Constraints & Success Criteria

### Constraints

| Type | Constraint | Impact if Violated |
|------|-----------|-------------------|
| Budget | [constraint] | [impact] |
| Timeline | [constraint] | [impact] |
| Technology | [constraint] | [impact] |
| Compliance | [constraint] | [impact] |

### Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [risk] | [H/M/L] | [H/M/L] | [mitigation] |

### Launch Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] All Must requirements implemented
- [ ] Zero critical bugs
- [ ] Performance targets met
- [ ] Security review passed

### Stakeholder Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| Product Owner | | | Pending |
| Tech Lead | | | Pending |
| Design Lead | | | Pending |
```

### 3.5 Generated Product Specification Template

After all three blocks are complete, generate the full specification:

```markdown
# Product Specification: [Product Name]

[![Status](https://img.shields.io/badge/status-draft-yellow)]()
[![Version](https://img.shields.io/badge/version-1.0-blue)]()
[![Phase](https://img.shields.io/badge/phase-pre_development-purple)]()

## Document Control

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Draft |
| Author | [Generated via knowledge skill interview] |
| Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |
| Review Cycle | Bi-weekly until approved |

---

## 1. Executive Summary

[2-3 paragraphs synthesized from Block 1 answers]

## 2. Problem Statement

[From Block 1, Question 2]

## 3. Product Vision

**Vision:** [One sentence describing the aspirational future state]

### Goals & Success Metrics

| Goal | Metric | Target | Measurement |
|------|--------|--------|-------------|
| [goal] | [KPI] | [target] | [method] |

## 4. Target Users & Personas

[From Block 1, Question 3 — full persona definitions]

## 5. Scope

### In Scope (This Release)

| ID | Feature | MoSCoW | User Stories |
|----|---------|--------|-------------|
| F001 | [feature] | Must | US-001, US-002 |

### Out of Scope (Future Releases)

- [From Block 2, Question 5]

### Non-Goals

- [Things this product will never do]

## 6. Functional Requirements

[From Block 2, organized by epic/feature area]

## 7. Non-Functional Requirements

[From Block 2, Question 2]

## 8. Data Model

[From Block 2, Question 3]

## 9. Key Workflows

[From Block 2, Question 4]

## 10. Technical Constraints

[From Block 3, Questions 1-2]

## 11. Risks & Mitigations

[From Block 3, Question 3]

## 12. Launch Criteria

[From Block 3, Question 4]

## 13. Stakeholder Approval

[From Block 3, Question 5]

## Appendix A: Interview Notes

[Raw notes from all three interview blocks]

## Appendix B: Competitive Analysis

[If competitive research was conducted]

## Appendix C: Research & Spikes

[Technology spike results if applicable]
```

---

## Section 4: Command `/docs roadmap` (Versioned Roadmap)

### 4.1 Four Output Formats

Every roadmap is generated in four formats, each serving a different audience:

#### Format 1: Markdown Table

```markdown
## Roadmap Table

| Version | Phase | Key Features | Target Date | Status |
|---------|-------|-------------|-------------|--------|
| v0.1.0 | M0: Foundation | Project scaffold, CI/CD, dev environment | 2026-W18 | ![Planned](https://img.shields.io/badge/status-planned-blue) |
| v0.2.0 | M1: Core MVP | Auth, CRUD, basic UI, deploy | 2026-W22 | ![Planned](https://img.shields.io/badge/status-planned-blue) |
| v0.3.0 | M2: Feature Complete | Search, filters, bulk ops, profiles | 2026-W26 | ![Planned](https://img.shields.io/badge/status-planned-blue) |
| v0.4.0 | M3: Hardening | Perf, security, a11y, observability | 2026-W30 | ![Planned](https://img.shields.io/badge/status-planned-blue) |
| v1.0.0 | M4: Launch Ready | Staging validation, load test, runbook | 2026-W34 | ![Planned](https://img.shields.io/badge/status-planned-blue) |
```

#### Format 2: Mermaid Gantt Chart

```markdown
## Roadmap Timeline

​```mermaid
gantt
    title Product Roadmap
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Foundation (M0)
    Project scaffold           :m0a, 2026-04-28, 7d
    CI/CD pipeline             :m0b, after m0a, 5d
    Dev environment            :m0c, after m0a, 5d

    section Core MVP (M1)
    Authentication             :m1a, after m0c, 7d
    Core CRUD operations       :m1b, after m1a, 10d
    Basic UI                   :m1c, after m1a, 10d
    First deployment           :m1d, after m1b, 3d

    section Feature Complete (M2)
    Search & filters           :m2a, after m1d, 7d
    Bulk operations            :m2b, after m1d, 5d
    User profiles              :m2c, after m2a, 5d
    Edge cases & error handling :m2d, after m2b, 7d

    section Hardening (M3)
    Performance optimization   :m3a, after m2d, 7d
    Security audit             :m3b, after m2d, 5d
    Accessibility              :m3c, after m3a, 5d
    Observability              :m3d, after m3b, 5d

    section Launch Ready (M4)
    Staging validation         :m4a, after m3d, 5d
    Load testing               :m4b, after m4a, 5d
    Runbook & docs             :m4c, after m4a, 5d
    Production launch          :milestone, after m4b, 0d
​```
```

#### Format 3: GitHub Milestones JSON

```markdown
## GitHub Milestones Configuration

​```json
[
  {
    "title": "M0: Foundation",
    "description": "Project scaffolding, CI/CD pipeline, development environment",
    "due_on": "2026-05-04T00:00:00Z",
    "labels": ["milestone:m0", "phase:foundation"]
  },
  {
    "title": "M1: Core MVP",
    "description": "Authentication, core CRUD, basic UI, first deployment",
    "due_on": "2026-05-26T00:00:00Z",
    "labels": ["milestone:m1", "phase:mvp"]
  },
  {
    "title": "M2: Feature Complete",
    "description": "Search, filters, bulk operations, profiles, edge cases",
    "due_on": "2026-06-23T00:00:00Z",
    "labels": ["milestone:m2", "phase:feature-complete"]
  },
  {
    "title": "M3: Hardening",
    "description": "Performance, security, accessibility, observability",
    "due_on": "2026-07-21T00:00:00Z",
    "labels": ["milestone:m3", "phase:hardening"]
  },
  {
    "title": "M4: Launch Ready",
    "description": "Staging validation, load testing, runbook, production launch",
    "due_on": "2026-08-18T00:00:00Z",
    "labels": ["milestone:m4", "phase:launch"]
  }
]
​```
```

#### Format 4: Phase Summary

```markdown
## Phase Summary

### M0: Foundation (Week 18-19)
**Goal:** Establish project infrastructure and developer experience.

- Project scaffolding (frontend + backend + infra)
- CI/CD pipeline (GitHub Actions)
- Local development environment (Docker Compose)
- Code standards, linting, formatting
- Documentation scaffold

**Exit Criteria:**
- [ ] `bun run build` and `./gradlew build` succeed
- [ ] CI pipeline runs on every PR
- [ ] Local environment starts with single command
- [ ] Documentation scaffold in place

---

### M1: Core MVP (Week 20-22)
**Goal:** Demonstrate the core value proposition end-to-end.

- User authentication (JWT + refresh tokens)
- Core CRUD operations for primary entity
- Basic UI with navigation and forms
- First deployment to staging

**Exit Criteria:**
- [ ] End-to-end happy path works in staging
- [ ] Auth flow complete (register, login, logout)
- [ ] All tests passing in CI
- [ ] Zero critical bugs

---

### M2: Feature Complete (Week 23-26)
**Goal:** All planned features implemented and tested.

- Search and filtering
- Bulk operations
- User profiles and settings
- Edge cases and error handling

**Exit Criteria:**
- [ ] All Must and Should features implemented
- [ ] Integration tests cover all API endpoints
- [ ] E2E tests cover critical user journeys
- [ ] Error states handled gracefully

---

### M3: Hardening (Week 27-30)
**Goal:** Production-ready quality, performance, and security.

- Performance optimization
- Security audit and remediation
- Accessibility (WCAG 2.2 AA)
- Observability (logging, metrics, tracing)

**Exit Criteria:**
- [ ] p95 response time < 200ms
- [ ] Security audit passed
- [ ] WCAG 2.2 AA compliance verified
- [ ] Monitoring dashboard operational

---

### M4: Launch Ready (Week 31-34)
**Goal:** Confident production deployment.

- Staging validation with production-like data
- Load testing
- Operational runbook
- Documentation complete
- Production deployment

**Exit Criteria:**
- [ ] Load test meets targets (> 1000 RPS)
- [ ] Runbook reviewed and tested
- [ ] Documentation health score ≥ 80/100
- [ ] Stakeholder sign-off
```

### 4.2 Complete Roadmap File Template

```markdown
# Product Roadmap: [Product Name]

[![Phase](https://img.shields.io/badge/phase-foundation-blue)]()

## Overview

[One paragraph: what this roadmap covers and its current state]

## Current Status

| Milestone | Status | Progress |
|-----------|--------|----------|
| M0: Foundation | ![Planned](https://img.shields.io/badge/status-planned-blue) | 0% |
| M1: Core MVP | ![Planned](https://img.shields.io/badge/status-planned-blue) | 0% |
| M2: Feature Complete | ![Planned](https://img.shields.io/badge/status-planned-blue) | 0% |
| M3: Hardening | ![Planned](https://img.shields.io/badge/status-planned-blue) | 0% |
| M4: Launch Ready | ![Planned](https://img.shields.io/badge/status-planned-blue) | 0% |

---

[Roadmap Table]

---

[Roadmap Timeline (Mermaid Gantt)]

---

[GitHub Milestones Configuration]

---

[Phase Summary with Exit Criteria]

---

## Versioning Convention

| Version Pattern | Meaning |
|----------------|---------|
| `v0.x.0` | Pre-release milestones |
| `v1.0.0` | First production release |
| `v1.x.0` | Feature releases |
| `v1.x.y` | Patch releases (bug fixes) |

## Review Cadence

- Roadmap reviewed at the start of each milestone
- Updated weekly with progress status
- Re-prioritized at sprint boundaries
```

---

## Section 5: Command `/docs onboarding` (Developer Onboarding Guide)

### 5.1 Onboarding Guide Template

```markdown
# Developer Onboarding Guide: [Project Name]

[![Audience](https://img.shields.io/badge/audience-new_developer-green)]()
[![Estimated Time](https://img.shields.io/badge/setup_time-30_minutes-orange)]()
[![Updated](https://img.shields.io/badge/updated-YYYY--MM--DD-blue)]()

## Welcome

Welcome to [Project Name]! This guide will get you from zero to contributing in
under 30 minutes.

## Prerequisites

### Required Software

| Software | Version | Install Command | Verify |
|----------|---------|----------------|--------|
| Bun | 1.2+ | `curl -fsSL https://bun.sh/install \| bash` | `bun --version` |
| Java (JDK) | 21 (LTS) | [Liberica JDK 21](https://bell-sw.com/pages/downloads/) | `java --version` |
| Docker / Podman | Latest | [Docker Desktop](https://docker.com/products/docker-desktop) | `docker --version` |
| Git | 2.40+ | System package manager | `git --version` |
| Editor | — | VS Code (recommended) or IntelliJ IDEA | — |

### Recommended VS Code Extensions

| Extension | Purpose |
|-----------|---------|
| Solid (solidjs) | SolidJS syntax highlighting and support |
| Tailwind CSS IntelliSense | TailwindCSS class autocomplete |
| ESLint | JavaScript/TypeScript linting |
| Prettier | Code formatting |
| Java Extension Pack | Java development |
| Gradle for Java | Gradle build support |

### Environment Variables

Create `.env` files from the templates:

```bash
# Frontend (.env)
cp app/.env.example app/.env

# Backend (.env)
cp server/.env.example server/.env
```

Required variables:
| Variable | Description | Default |
|----------|-------------|---------|
| `API_URL` | Backend API URL | `http://localhost:8080` |
| `DATABASE_URL` | PostgreSQL connection string | `jdbc:postgresql://localhost:5432/app_dev` |

## Tech Stack Reference

### Frontend Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Bun | 1.2+ | Runtime, package manager, bundler |
| TypeScript | 5.8 (strict) | Type-safe JavaScript |
| SolidJS | 1.9+ | UI framework (fine-grained reactivity) |
| SolidStart | Latest | Meta-framework (SSG mode) |
| TailwindCSS | 4.1+ | Utility-first CSS |
| Iconify-Solid | 2.x | Icon components |

### Backend Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Java | 21 (LTS) | Backend language |
| Micronaut | 4.7+ | Backend framework (compile-time DI) |
| Gradle | 8.13+ | Build tool (Kotlin DSL) |
| PostgreSQL | 16+ | Database |
| Flyway | — | Database migrations |

### Infrastructure

| Component | Image | Purpose |
|-----------|-------|---------|
| Frontend container | `nginx:stable-alpine` | Static asset serving |
| Backend container | `bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl` | JVM runtime |

## Quick Start (5 minutes)

```bash
# 1. Clone the repository
git clone <repository-url>
cd <project-name>

# 2. Start local infrastructure
docker compose up -d

# 3. Setup frontend
cd app
bun install
bun run dev
# Frontend running at http://localhost:3000

# 4. Setup backend (new terminal)
cd server
./gradlew run
# Backend running at http://localhost:8080

# 5. Verify everything works
curl http://localhost:8080/api/v1/health
# Expected: {"status":"UP"}
```

## Project Structure

```
project-root/
├── app/                    # Frontend (SolidJS + SolidStart)
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── routes/         # File-based routing
│   │   ├── lib/            # Shared utilities
│   │   └── stores/         # Signal-based state
│   └── package.json
├── server/                 # Backend (Micronaut)
│   ├── src/main/java/      # Java source
│   ├── src/main/resources/ # Config and migrations
│   └── build.gradle.kts
├── infra/                  # Infrastructure definitions
│   ├── docker/             # Dockerfiles and compose
│   └── nginx/              # nginx configuration
├── docs/                   # Documentation (SDLC structure)
└── README.md
```

## Daily Workflow

### Starting Work

```bash
# Pull latest changes
git checkout main
git pull origin main

# Create a feature branch
git checkout -b feature/TASK-XXX-short-description

# Start development environment
docker compose up -d
cd app && bun run dev     # Terminal 1
cd server && ./gradlew run  # Terminal 2
```

### Development Cycle

```
1. Pick a task from the current milestone
2. Create branch: feature/TASK-XXX-description
3. Implement changes (follow code conventions)
4. Write tests (follow testing skill patterns)
5. Run quality checks:
   - bun run typecheck    (Frontend)
   - bun run lint         (Frontend)
   - bun run test         (Frontend)
   - ./gradlew check      (Backend)
6. Commit with conventional message
7. Push and create PR
8. Address review feedback
9. Merge (squash merge)
```

### Common Commands Reference

| Command | Context | Purpose |
|---------|---------|---------|
| `bun run dev` | `app/` | Start frontend dev server |
| `bun run build` | `app/` | Build frontend for production |
| `bun run lint` | `app/` | Run ESLint |
| `bun run format` | `app/` | Run Prettier |
| `bun run test` | `app/` | Run Vitest tests |
| `bun run typecheck` | `app/` | Run TypeScript type checking |
| `./gradlew run` | `server/` | Start backend server |
| `./gradlew build` | `server/` | Build backend |
| `./gradlew test` | `server/` | Run backend tests |
| `./gradlew check` | `server/` | Run all checks (test + lint) |

### Branch Naming Convention

| Branch Type | Pattern | Example |
|-------------|---------|---------|
| Feature | `feature/TASK-XXX-description` | `feature/TASK-042-add-user-search` |
| Bug fix | `fix/TASK-XXX-description` | `fix/TASK-089-fix-login-error` |
| Docs | `docs/TASK-XXX-description` | `docs/TASK-012-update-onboarding` |
| Chore | `chore/TASK-XXX-description` | `chore/TASK-007-upgrade-deps` |

### Commit Message Convention

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`

## Code Conventions

### Frontend Conventions

- **TypeScript strict mode** — no `any` types, use `unknown` and type guards
- **Named exports** — no default exports for components
- **SolidJS patterns** — use `createSignal`, `createStore`, `createResource`, `createMemo`
- **TailwindCSS** — utility classes only, no custom CSS files (use `@apply` sparingly)
- **File naming** — `PascalCase.tsx` for components, `camelCase.ts` for utilities
- **Component size** — max 150 lines, split if larger

### Backend Conventions

- **Java 21 features** — records for DTOs, sealed interfaces, pattern matching
- **No Lombok** — use plain Java records and compact constructors
- **Constructor injection** — no field injection
- **Package structure** — module-based: controller/service/repository/model
- **Validation** — Jakarta annotations on request DTOs
- **Error handling** — RFC 7807 Problem Details format

## Where to Find Things

| What | Where |
|------|-------|
| API endpoints | `server/src/main/java/**/controller/` |
| Business logic | `server/src/main/java/**/service/` |
| Database queries | `server/src/main/java/**/repository/` |
| Database migrations | `server/src/main/resources/db/migration/` |
| UI components | `app/src/components/` |
| Page routes | `app/src/routes/` |
| Shared utilities | `app/src/lib/` |
| State stores | `app/src/stores/` |
| TypeScript types | `app/src/types/` |
| API client | `app/src/lib/api/` |
| Configuration | `server/src/main/resources/application.yml` |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `bun install` fails | Delete `node_modules` and `bun.lockb`, run `bun install` again |
| Backend won't start | Check Docker PostgreSQL is running: `docker compose ps` |
| Port already in use | `lsof -i :3000` or `lsof -i :8080` to find and kill the process |
| Database migration error | Check Flyway migration naming: `V001__description.sql` (double underscore) |
| TypeScript errors | Run `bun run typecheck` to see all errors, fix one at a time |
| Test failures | Run with verbose output: `bun run test -- --reporter=verbose` |

## Getting Help

- **Documentation**: Start with `docs/` directory
- **Architecture**: See `docs/01-architecture/system-overview.md`
- **API**: See `docs/04-api/`
- **Code questions**: Ask in the team channel or comment on the relevant PR
- **Onboarding issues**: File an issue labeled `docs:improvement`

---

_Welcome aboard! If something in this guide is unclear or outdated, please
update it — this is a living document._
```

---

## Section 6: ADR Process and Lifecycle

### 6.1 ADR Lifecycle

```
Proposed ──► Accepted ──► Deprecated ──► Superseded
   │            │
   │            └──► Rejected (alternative was chosen)
   │
   └──► Draft (being written)
```

| Status | Meaning | Color |
|--------|---------|-------|
| Draft | Being written, not ready for review | ![Draft](https://img.shields.io/badge/status-draft-gray) |
| Proposed | Ready for review and discussion | ![Proposed](https://img.shields.io/badge/status-proposed-orange) |
| Accepted | Approved and in effect | ![Accepted](https://img.shields.io/badge/status-accepted-green) |
| Rejected | Not approved, kept for reference | ![Rejected](https://img.shields.io/badge/status-rejected-red) |
| Deprecated | No longer in effect | ![Deprecated](https://img.shields.io/badge/status-deprecated-lightgray) |
| Superseded | Replaced by a newer ADR | ![Superseded](https://img.shields.io/badge/status-superseded-blue) |

### 6.2 ADR Template

```markdown
# ADR NNNN: [Title]

[![Status](https://img.shields.io/badge/status-proposed-orange)]()

## Date

YYYY-MM-DD

## Status

[Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-XXXX]

## Context

[What is the issue that we're seeing that is motivating this decision or change?
Include any technical, business, or team factors that influence the decision.]

## Decision

[What is the change that we're proposing and/or doing?
State the decision clearly and unambiguously.]

## Alternatives Considered

### Alternative 1: [Name]

**Description:** [Brief description]
**Pros:** [Advantages]
**Cons:** [Disadvantages]

### Alternative 2: [Name]

**Description:** [Brief description]
**Pros:** [Advantages]
**Cons:** [Disadvantages]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

### Neutral
- [Side effect that is neither good nor bad]

## Evaluation Criteria

| Criterion | Weight | Selected | Alt 1 | Alt 2 |
|-----------|--------|----------|-------|-------|
| Fit for purpose | High | [score] | [score] | [score] |
| Team capability | High | [score] | [score] | [score] |
| Ecosystem maturity | Medium | [score] | [score] | [score] |
| Operational impact | Medium | [score] | [score] | [score] |
| Long-term viability | Medium | [score] | [score] | [score] |
| License | Gate | [pass/fail] | [pass/fail] | [pass/fail] |

## References

- [Link to relevant documentation, discussions, or external resources]
```

### 6.3 ADR Index Template

```markdown
# Architecture Decision Records

This directory contains all Architecture Decision Records for [Project Name].

## Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](./0001-record-architecture-decisions.md) | Record Architecture Decisions | Accepted | YYYY-MM-DD |
| [0002](./0002-choose-solidjs-over-react.md) | Choose SolidJS over React | Accepted | YYYY-MM-DD |
| [0003](./0003-modular-monolith.md) | Modular Monolith Architecture | Accepted | YYYY-MM-DD |

## Creating a New ADR

1. Copy the template from `references/adr-template.md`
2. Number sequentially (check existing ADRs for next number)
3. Write the ADR following the template
4. Set status to "Proposed"
5. Commit with message: `docs(adr): propose ADR NNNN - <title>`
6. After review and approval, update status to "Accepted"
7. Commit: `docs(adr): accept ADR NNNN - <title>`

## ADR Lifecycle

See [ADR Process and Lifecycle](#) in the knowledge skill documentation.
```

### 6.4 First ADR (Always Generated)

The first ADR is always ADR 0001 — the decision to use ADRs themselves:

```markdown
# ADR 0001: Record Architecture Decisions

[![Status](https://img.shields.io/badge/status-accepted-green)]()

## Date

YYYY-MM-DD

## Status

Accepted

## Context

We need a mechanism to record architectural and significant technical decisions
made in this project. Without a formal process, decisions are lost, context is
forgotten, and new team members cannot understand why certain choices were made.

## Decision

We will use Architecture Decision Records (ADRs) to document all significant
technical decisions. Each ADR will be stored in `docs/01-architecture/adr/` as
a Markdown file, numbered sequentially, and tracked in version control.

An ADR is required when:
- Choosing one technology over another
- Changing the system architecture
- Making a decision that affects multiple modules
- Reversing a previous decision
- Setting a standard or convention

An ADR is NOT required when:
- Fixing a bug
- Adding a minor feature
- Refactoring within the same module
- Updating dependencies (unless major version change)

## Alternatives Considered

### Alternative 1: No formal documentation
**Pros:** No overhead
**Cons:** Decisions are lost, tribal knowledge

### Alternative 2: Wiki / Confluence
**Pros:** Rich formatting, search
**Cons:** Not version-controlled with code, drifts from reality

### Alternative 3: Git commit messages only
**Pros:** Already version-controlled
**Cons:** Not discoverable, buried in history

## Consequences

### Positive
- Every significant decision has context and rationale
- New team members can understand the "why" behind architecture
- Decisions are version-controlled alongside code
- Easy to find and reference past decisions

### Negative
- Overhead of writing and maintaining ADRs
- Risk of ADRs becoming stale if not reviewed

### Neutral
- ADRs are immutable once accepted — create a new ADR to change direction
```

---

## Section 7: Documentation Linting Rules

### 7.1 Rule Set

All Markdown documentation must comply with these rules:

| Rule ID | Rule | Description | Severity |
|---------|------|-------------|----------|
| DL-001 | ATX headers | Use `#` style headers, never Setext (underlines) | Error |
| DL-002 | Dash lists | Use `-` for unordered lists, not `*` or `+` | Error |
| DL-003 | 2-space indent | Indent continuation lines with 2 spaces per level | Error |
| DL-004 | 120-char line width | Lines must not exceed 120 characters (except URLs, code blocks) | Warning |
| DL-005 | Single H1 | Exactly one top-level heading (`#`) per file | Error |
| DL-006 | Fenced code blocks | Use triple backticks with language identifier | Error |
| DL-007 | Trailing whitespace | No trailing whitespace on any line | Error |
| DL-008 | Final newline | File must end with a single newline character | Error |
| DL-009 | No HTML | No raw HTML in Markdown (except in code blocks) | Warning |
| DL-010 | No broken links | All internal links must resolve to existing files | Error |
| DL-011 | Consistent header casing | Use sentence case for headers (capitalize first word and proper nouns only) | Warning |
| DL-012 | No TBD/TODO | No unresolved TODO, TBD, FIXME, or XXX markers | Warning |
| DL-013 | Badge format | Shields.io badges must use the standard format | Warning |
| DL-014 | No hardcoded secrets | No API keys, passwords, tokens, or connection strings | Error |
| DL-015 | Table alignment | Pipe tables must have consistent column alignment | Warning |

### 7.2 Validation Checklist

When running `/docs validate`, check each file against all rules:

```markdown
## Documentation Validation Report

**Date:** YYYY-MM-DD
**Files Checked:** X
**Violations:** Y (Z errors, W warnings)

### Violations by File

| File | Rule | Severity | Line | Message |
|------|------|----------|------|---------|
| path/to/file.md | DL-001 | Error | 5 | Use ATX headers (`#`) instead of Setext style |
| path/to/file.md | DL-004 | Warning | 12 | Line exceeds 120 characters (135) |
| path/to/file.md | DL-010 | Error | — | Broken link: ./nonexistent.md |

### Summary by Rule

| Rule | Violations | Severity |
|------|-----------|----------|
| DL-001 | 2 | Error |
| DL-004 | 5 | Warning |
| DL-010 | 1 | Error |

### Recommended Fixes

1. [Specific fix for most common violation]
2. [Specific fix for second most common violation]
```

### 7.3 Rule Details and Examples

#### DL-001: ATX Headers

```markdown
<!-- Correct -->
# Document Title
## Section
### Subsection

<!-- Incorrect -->
Document Title
==============
Section
-------
```

#### DL-002: Dash Lists

```markdown
<!-- Correct -->
- First item
- Second item
  - Nested item

<!-- Incorrect -->
* First item
+ Second item
```

#### DL-003: 2-Space Indent

```markdown
<!-- Correct -->
- Item one
  - Nested item (2 spaces)
    - Deep nested (4 spaces)

<!-- Incorrect -->
- Item one
    - Nested item (4 spaces)
	- Deep nested (tab)
```

#### DL-004: 120-Character Line Width

```markdown
<!-- Correct (short line) -->
This is a paragraph that stays within the 120 character limit and wraps
naturally in the editor.

<!-- Incorrect (long line) -->
This is a very long line that exceeds the one hundred and twenty character limit and should be broken into multiple lines for readability in any text editor or terminal.
```

Exception: URLs, code blocks, and table rows may exceed 120 characters.

#### DL-006: Fenced Code Blocks

````markdown
<!-- Correct -->
```java
public record User(UUID id, String name) {}
```

<!-- Incorrect (indented code block or no language) ```
public record User(UUID id, String name) {}
```

<!-- Incorrect (no language identifier) -->
```
public record User(UUID id, String name) {}
```
````

---

## Section 8: Badge Standards

### 8.1 Badge Catalog

All documentation uses [Shields.io](https://shields.io) badges for status indicators.

#### Project-Level Badges

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![Build](https://img.shields.io/github/actions/workflow/status/<org>/<repo>/ci.yml?branch=main)]()
[![Coverage](https://img.shields.io/codecov/c/github/<org>/<repo>)]()
[![Docs](https://img.shields.io/badge/docs-latest-green)]()
```

#### Documentation Status Badges

| Badge | Markdown | Use When |
|-------|----------|----------|
| Draft | `[![Status](https://img.shields.io/badge/status-draft-yellow)]()` | Document is being written |
| Review | `[![Status](https://img.shields.io/badge/status-in_review-orange)]()` | Document is under review |
| Approved | `[![Status](https://img.shields.io/badge/status-approved-green)]()` | Document has been approved |
| Published | `[![Status](https://img.shields.io/badge/status-published-brightgreen)]()` | Document is live |
| Deprecated | `[![Status](https://img.shields.io/badge/status-deprecated-lightgray)]()` | Document is outdated |

#### Phase Badges

| Badge | Markdown |
|-------|----------|
| Pre-development | `[![Phase](https://img.shields.io/badge/phase-pre_development-purple)]()` |
| During development | `[![Phase](https://img.shields.io/badge/phase-development-blue)]()` |
| Post-development | `[![Phase](https://img.shields.io/badge/phase-post_development-teal)]()` |

#### Audience Badges

| Badge | Markdown |
|-------|----------|
| All | `[![Audience](https://img.shields.io/badge/audience-all-green)]()` |
| Developers | `[![Audience](https://img.shields.io/badge/audience-developers-green)]()` |
| Operators | `[![Audience](https://img.shields.io/badge/audience-operators-orange)]()` |
| Product | `[![Audience](https://img.shields.io/badge/audience-product-blue)]()` |
| Support | `[![Audience](https://img.shields.io/badge/audience-support-yellow)]()` |

#### Roadmap Badges

| Badge | Markdown |
|-------|----------|
| Planned | `[![Planned](https://img.shields.io/badge/status-planned-blue)]()` |
| In Progress | `[![In Progress](https://img.shields.io/badge/status-in_progress-yellow)]()` |
| Complete | `[![Complete](https://img.shields.io/badge/status-complete-brightgreen)]()` |
| Blocked | `[![Blocked](https://img.shields.io/badge/status-blocked-red)]()` |

### 8.2 Badge Placement Rules

1. **First badge after the H1 title** — always the status badge
2. **Second badge** — version or phase badge
3. **Third badge (optional)** — audience badge
4. **No more than 3 badges** per document header
5. **Badges in tables** — use compact single-badge format for inline status

---

## Section 9: Command `/docs health` (Documentation Health Report)

### 9.1 Scoring Model

The documentation health report uses a 100-point scale:

```
Total Score = Quality Score (max 60) + SDLC Coverage Score (max 40)
```

### 9.2 Quality Score (60 points)

| Criterion | Points | Assessment |
|-----------|--------|------------|
| **Completeness** | 15 | All required sections present and populated |
| **Accuracy** | 10 | Documentation matches actual implementation |
| **Currency** | 10 | Documents updated within last 30 days |
| **Linting** | 10 | Passes all documentation linting rules (DL-001 to DL-015) |
| **Readability** | 10 | Clear structure, proper formatting, good writing |
| **Traceability** | 5 | Links between related documents, cross-references |

**Completeness assessment (15 points):**

| Score | Criteria |
|-------|----------|
| 15 | Every required section has content, no placeholders, no TODOs |
| 12 | Minor gaps — 1-2 sections incomplete |
| 9 | Several sections incomplete but core content exists |
| 6 | Major sections missing or mostly placeholder |
| 3 | Bare skeleton with no real content |
| 0 | Empty or missing |

**Accuracy assessment (10 points):**

| Score | Criteria |
|-------|----------|
| 10 | All code examples run, all paths resolve, all versions match |
| 8 | Minor discrepancies (1-2 outdated examples) |
| 6 | Several outdated references |
| 3 | Significant drift from actual implementation |
| 0 | Completely outdated or misleading |

**Currency assessment (10 points):**

| Score | Criteria |
|-------|----------|
| 10 | All docs updated within 30 days |
| 8 | Most docs updated within 30 days, 1-2 older |
| 6 | Mix of current and stale (30-90 days) |
| 3 | Most docs older than 90 days |
| 0 | No recent updates |

**Linting assessment (10 points):**

| Score | Criteria |
|-------|----------|
| 10 | Zero violations |
| 8 | Only warnings, no errors |
| 6 | 1-3 errors |
| 3 | 4-10 errors |
| 0 | More than 10 errors |

**Readability assessment (10 points):**

| Score | Criteria |
|-------|----------|
| 10 | Excellent structure, consistent formatting, clear language |
| 8 | Good structure, minor formatting inconsistencies |
| 6 | Adequate structure, some unclear sections |
| 3 | Poor structure, hard to follow |
| 0 | Unreadable |

**Traceability assessment (5 points):**

| Score | Criteria |
|-------|----------|
| 5 | All cross-references valid, ADRs linked to specs |
| 4 | Most cross-references valid, 1-2 broken |
| 3 | Some cross-references, but gaps |
| 1 | Minimal cross-referencing |
| 0 | No cross-references |

### 9.3 SDLC Coverage Score (40 points)

| SDLC Section | Points | Required Documents |
|-------------|--------|-------------------|
| **00-product/** | 10 | Product specification, roadmap, glossary |
| **01-architecture/** | 10 | System overview, ADRs, data model, security |
| **02-development/** | 8 | Onboarding guide, tech stack, conventions, testing |
| **03-deployment/** | 6 | Runbook, deployment guide, environment plan |
| **04-api/** | 4 | OpenAPI spec, authentication, error codes |
| **05-support/** | 2 | FAQ, triage guide |

**Section scoring (per section):**

| Score | Criteria |
|-------|----------|
| Full points | All required documents present and substantive |
| 80% | All required documents present, some gaps |
| 60% | Most required documents present |
| 40% | Some required documents present |
| 20% | Minimal documents present |
| 0% | Section missing entirely |

### 9.4 Health Report Template

```markdown
# Documentation Health Report

[![Generated](https://img.shields.io/badge/generated-YYYY--MM--DD-blue)]()
[![Score](https://img.shields.io/badge/score-XX%2F100-green)]()

## Summary

| Metric | Score | Max |
|--------|-------|-----|
| Quality | XX | 60 |
| SDLC Coverage | XX | 40 |
| **Total** | **XX** | **100** |

## Quality Breakdown

| Criterion | Score | Max | Status |
|-----------|-------|-----|--------|
| Completeness | XX | 15 | PASS / NEEDS WORK |
| Accuracy | XX | 10 | PASS / NEEDS WORK |
| Currency | XX | 10 | PASS / NEEDS WORK |
| Linting | XX | 10 | PASS / NEEDS WORK |
| Readability | XX | 10 | PASS / NEEDS WORK |
| Traceability | XX | 5 | PASS / NEEDS WORK |
| **Quality Total** | **XX** | **60** | |

## SDLC Coverage Breakdown

| Section | Score | Max | Documents Found | Documents Missing |
|---------|-------|-----|----------------|-------------------|
| 00-product/ | XX | 10 | [list] | [list] |
| 01-architecture/ | XX | 10 | [list] | [list] |
| 02-development/ | XX | 8 | [list] | [list] |
| 03-deployment/ | XX | 6 | [list] | [list] |
| 04-api/ | XX | 4 | [list] | [list] |
| 05-support/ | XX | 2 | [list] | [list] |
| **Coverage Total** | **XX** | **40** | | |

## Linting Violations

| File | Rule | Severity | Description |
|------|------|----------|-------------|
| [path] | DL-XXX | Error/Warning | [description] |

## Recommendations

### Critical (Must Fix)
1. [Recommendation]
2. [Recommendation]

### Important (Should Fix)
1. [Recommendation]
2. [Recommendation]

### Nice to Have
1. [Recommendation]
2. [Recommendation]

## Grade

| Score Range | Grade |
|-------------|-------|
| 90-100 | A — Excellent |
| 80-89 | B — Good |
| 70-79 | C — Adequate |
| 60-69 | D — Below Average |
| 0-59 | F — Needs Significant Work |

**This project grades: [Grade] ([Score]/100)**
```

### 9.5 Health Report Scoring Thresholds

| Threshold | Action |
|-----------|--------|
| ≥ 90 | No action required. Continue maintaining. |
| 80-89 | Address recommendations within 2 weeks. |
| 70-79 | Address critical issues within 1 week. |
| 60-69 | Documentation debt — plan a documentation sprint. |
| < 60 | Documentation crisis — immediate attention required. |

---

## Section 10: Command `/docs runbook` (Operational Runbook)

### 10.1 Runbook Template

```markdown
# Runbook: [Service Name]

[![Status](https://img.shields.io/badge/status-active-brightgreen)]()
[![Owner](https://img.shields.io/badge/team-platform-blue)]()
[![Last Tested](https://img.shields.io/badge/last_tested-YYYY--MM--DD-green)]()

## Service Overview

| Field | Value |
|-------|-------|
| Service name | [name] |
| Team | [owning team] |
| Repository | [repo URL] |
| Language | Java 21 |
| Framework | Micronaut 4.7 |
| Container image | `bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl` |
| Default port | 8080 |
| Health endpoint | `GET /api/v1/health` |

## Architecture

```
┌──────────┐     ┌────────────────┐     ┌──────────────┐
│  nginx   │────▶│  Micronaut API │────▶│  PostgreSQL  │
│ (proxy)  │     │  (port 8080)   │     │  (port 5432) │
└──────────┘     └────────────────┘     └──────────────┘
```

## Service Level Objectives

| SLO | Target | Measurement |
|-----|--------|-------------|
| Availability | 99.9% | Uptime monitoring |
| Latency (p50) | < 50ms | APM metrics |
| Latency (p99) | < 500ms | APM metrics |
| Error rate | < 0.1% | Log aggregation |
| Throughput | > 1000 RPS | Load testing |

## Health Checks

### Application Health

```bash
curl -s http://localhost:8080/api/v1/health | jq .
```

Expected response:
```json
{"status": "UP"}
```

### Database Connectivity

```bash
docker exec -it <db-container> pg_isready -U <user>
```

### Container Health

```bash
docker inspect --format='{{.State.Health.Status}}' <container-name>
```

## Common Operations

### Deploy New Version

```bash
# 1. Build new image
docker build -t <service>:<version> .

# 2. Run health check on new image
docker run --rm -p 8081:8080 <service>:<version> &
curl -sf http://localhost:8081/api/v1/health || echo "HEALTH CHECK FAILED"

# 3. Deploy (rolling update)
docker compose up -d --no-deps --build <service>

# 4. Verify
curl -sf http://localhost:8080/api/v1/health | jq .status
# Expected: "UP"
```

### Scale Horizontally

```bash
docker compose up -d --scale <service>=3
```

### Database Migration

```bash
# Run pending migrations
docker exec <service-container> java -jar app.jar --flyway.migrate

# Check migration status
docker exec <db-container> psql -U <user> -d <db> -c "SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 10;"
```

### Rollback

```bash
# 1. Identify previous version
docker images <service> --format "{{.Tag}}"

# 2. Rollback to previous version
docker compose down <service>
docker tag <service>:<previous-version> <service>:latest
docker compose up -d <service>

# 3. Verify
curl -sf http://localhost:8080/api/v1/health | jq .status
```

## Alert Response

### High Error Rate (> 1%)

1. Check recent deployments: `git log --oneline -10`
2. Check application logs: `docker logs <container> --tail 100`
3. Check database connectivity
4. If caused by deployment, rollback (see above)
5. If caused by external dependency, check status page

### High Latency (> p99 1s)

1. Check resource usage: `docker stats <container>`
2. Check database query performance: `SELECT * FROM pg_stat_activity WHERE state = 'active'`
3. Check for slow queries in logs
4. Scale horizontally if resource-constrained

### Out of Memory

1. Check JVM heap usage: `docker exec <container> jcmd 1 GC.heap_info`
2. Check container memory limit: `docker inspect --format='{{.HostConfig.Memory}}' <container>`
3. Increase memory limit or scale horizontally
4. Review heap dump if available

### Database Connection Pool Exhaustion

1. Check active connections: `docker exec <db-container> psql -U <user> -c "SELECT count(*) FROM pg_stat_activity"`
2. Check pool configuration in `application.yml`
3. Identify long-running queries
4. Restart service if connections are leaked

## Disaster Recovery

### Database Recovery

```bash
# Restore from latest backup
pg_restore -h <host> -U <user> -d <db> /backups/latest.dump
```

### Full Service Recovery

```bash
# From scratch on a new host
git clone <repository>
cd <project>
docker compose up -d
# Run migrations
# Verify health
```

## On-Call Contacts

| Role | Name | Contact | Escalation Time |
|------|------|---------|-----------------|
| Primary | [name] | [contact] | Immediate |
| Secondary | [name] | [contact] | 15 min |
| Manager | [name] | [contact] | 30 min |

## Runbook Maintenance

- Review and update after every incident
- Test all procedures quarterly
- Last reviewed: YYYY-MM-DD
- Next review: YYYY-MM-DD
```

---

## Section 11: Command `/docs support` (Support Cluster)

### 11.1 Support Cluster Structure

```
docs/05-support/
├── README.md                 # Support documentation index
├── faq.md                    # Frequently asked questions
├── triage-guide.md           # Issue triage classification
├── sla.md                    # Service Level Agreements
├── post-mortem-template.md   # Post-mortem template
└── known-issues.md           # Known issues and workarounds
```

### 11.2 FAQ Template

```markdown
# Frequently Asked Questions

[![Audience](https://img.shields.io/badge/audience-all-green)]()
[![Updated](https://img.shields.io/badge/updated-YYYY--MM--DD-blue)]()

## General

### What is [Product Name]?

[Answer]

### Who is [Product Name] for?

[Answer]

## Getting Started

### How do I create an account?

[Step-by-step answer]

### What are the system requirements?

[Answer]

## Usage

### How do I [common action]?

[Step-by-step answer]

### Can I [common question]?

[Answer]

## Troubleshooting

### Why is [common problem] happening?

**Cause:** [explanation]
**Solution:** [step-by-step fix]

### I'm getting [error message]. What should I do?

**Cause:** [explanation]
**Solution:** [step-by-step fix]

## Account & Billing

### How do I reset my password?

[Step-by-step answer]

### How do I upgrade my plan?

[Answer]

---

_Can't find your answer? [Contact support](mailto:support@example.com)_
```

### 11.3 Triage Guide Template

```markdown
# Issue Triage Guide

[![Audience](https://img.shields.io/badge/audience-support-yellow)]()

## Severity Levels

| Severity | Definition | Response Time | Examples |
|----------|-----------|---------------|----------|
| **SEV-1 (Critical)** | Service down, data loss, security breach | 15 minutes | Site unreachable, data corruption |
| **SEV-2 (High)** | Major feature broken, many users affected | 1 hour | Login fails, payment processing down |
| **SEV-3 (Medium)** | Feature partially broken, workaround exists | 4 hours | Search returns incomplete results |
| **SEV-4 (Low)** | Minor issue, cosmetic, single user | 24 hours | UI glitch, typo |

## Triage Decision Tree

```
Incoming Issue
    │
    ├─ Is the service completely down?
    │   └─ YES → SEV-1
    │
    ├─ Is a core feature broken for multiple users?
    │   └─ YES → SEV-2
    │
    ├─ Is a feature partially broken but has a workaround?
    │   └─ YES → SEV-3
    │
    └─ Is it cosmetic or affects a single user?
        └─ YES → SEV-4
```

## Triage Labels

| Label | Meaning |
|-------|---------|
| `bug` | Confirmed defect |
| `not-a-bug` | Working as intended |
| `duplicate` | Already reported |
| `needs-info` | Need more information from reporter |
| `blocked` | Waiting on external dependency |
| `wontfix` | Acknowledged but will not fix |

## Escalation Path

```
Support Agent ──► Senior Support ──► Engineering Lead ──► VP Engineering
     SEV-4              SEV-3              SEV-2              SEV-1
```
```

### 11.4 SLA Template

```markdown
# Service Level Agreements

[![Audience](https://img.shields.io/badge/audience-operators-orange)]()

## Availability SLA

| Tier | Target | Measurement | Exclusions |
|------|--------|-------------|------------|
| Production | 99.9% uptime | 30-day rolling average | Scheduled maintenance windows |
| Staging | 99.0% uptime | 30-day rolling average | Deploy-related downtime |

**Calculation:** `Availability = (Total Minutes - Downtime Minutes) / Total Minutes * 100`

## Response Time SLA

| Severity | First Response | Update Frequency | Resolution Target |
|----------|---------------|-----------------|-------------------|
| SEV-1 | 15 minutes | Every 30 minutes | 4 hours |
| SEV-2 | 1 hour | Every 2 hours | 24 hours |
| SEV-3 | 4 hours | Daily | 5 business days |
| SEV-4 | 24 hours | Weekly | Next release |

## Maintenance Windows

| Window | Day | Time | Duration | Advance Notice |
|--------|-----|------|----------|----------------|
| Regular | Sunday | 02:00-06:00 UTC | Up to 4 hours | 72 hours |
| Emergency | Any | Any | As needed | Best effort |

## Reporting

- Monthly SLA report generated automatically
- Distributed to stakeholders by the 5th of each month
- SLA breaches trigger an incident review within 48 hours
```

### 11.5 Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

[![Status](https://img.shields.io/badge/status-draft-yellow)]()
[![SEV](https://img.shields.io/badge/severity-SEV_X-red)]()

## Incident Summary

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Duration | X hours Y minutes |
| Severity | SEV-X |
| Impact | [number of users/systems affected] |
| Detect method | [monitoring / user report / internal] |
| Resolution | [how it was fixed] |

## Timeline (UTC)

| Time | Event |
|------|-------|
| HH:MM | [First sign of issue] |
| HH:MM | [Alert triggered] |
| HH:MM | [Response began] |
| HH:MM | [Root cause identified] |
| HH:MM | [Fix deployed] |
| HH:MM | [Service restored] |

## Root Cause

[Detailed explanation of what caused the incident. Be specific and technical.]

## Contributing Factors

1. [Factor that contributed to the incident]
2. [Factor that contributed to slow detection or resolution]

## Impact Assessment

- **Users affected:** [count or percentage]
- **Requests failed:** [count]
- **Data affected:** [description]
- **Revenue impact:** [if applicable]
- **Reputation impact:** [if applicable]

## What Went Well

- [Positive aspect of detection or response]

## What Could Be Improved

- [Area for improvement]

## Action Items

| Action | Owner | Priority | Due Date | Status |
|--------|-------|----------|----------|--------|
| [Action item] | [owner] | [H/M/L] | [date] | [status] |

## Lessons Learned

[Key takeaways for the team]

## Appendix

[Logs, metrics, screenshots, or other supporting evidence]
```

---

## Section 12: Changelog Generation

### 12.1 Changelog Format

Follow [Keep a Changelog](https://keepachangelog.com) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- [New feature]

### Changed
- [Change to existing functionality]

### Deprecated
- [Feature being removed in future release]

### Removed
- [Feature removed in this release]

### Fixed
- [Bug fix]

### Security
- [Security fix]

## [1.0.0] - YYYY-MM-DD

### Added
- [Feature]

## [0.4.0] - YYYY-MM-DD

### Added
- [Feature]

### Fixed
- [Bug fix]
```

### 12.2 Changelog Categories

| Category | When to Use |
|----------|-------------|
| **Added** | New features, new endpoints, new documentation |
| **Changed** | Changes to existing behavior, updated dependencies |
| **Deprecated** | Features that will be removed in a future release |
| **Removed** | Features removed in this release |
| **Fixed** | Bug fixes, documentation corrections |
| **Security** | Security vulnerability fixes |

---

## Section 13: Technology Stack Reference

All technology references in documentation default to the following stack.

### Frontend

| Component | Version | Notes |
|-----------|---------|-------|
| Runtime | Bun 1.2+ | Package manager, bundler, test runner |
| Language | TypeScript 5.8 (strict) | `strict: true`, `noUncheckedIndexedAccess: true` |
| UI Framework | SolidJS 1.9+ | Fine-grained reactivity, no VDOM |
| Meta Framework | SolidStart (SSG mode) | Static site generation |
| Styling | TailwindCSS 4.1+ | Utility-first, CSS-first config |
| Icons | Iconify-Solid 2.x | Tree-shakeable icon components |

### Backend

| Component | Version | Notes |
|-----------|---------|-------|
| Language | Java 21 (LTS) | Records, sealed types, virtual threads |
| Framework | Micronaut 4.7+ | Compile-time DI, AOT, low memory |
| Build | Gradle 8.13+ (Kotlin DSL) | `build.gradle.kts` |

### Infrastructure

| Component | Image / Version | Notes |
|-----------|----------------|-------|
| Reverse Proxy | nginx:stable-alpine | TLS termination, static assets |
| Backend Container | bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl | CRaC + CDS, musl-based |
| Database | PostgreSQL 16+ | Default RDBMS |
| CI/CD | GitHub Actions | Default pipeline |

---

## Section 14: Validation and Quality Assurance

### 14.1 `/docs validate` Process

1. **Scan** — Find all Markdown files in `docs/` directory
2. **Lint** — Apply all documentation linting rules (DL-001 to DL-015)
3. **Link check** — Verify all internal links resolve
4. **Badge check** — Verify all badges use correct format
5. **Structure check** — Verify SDLC folder structure is intact
6. **Report** — Generate validation report with violations

### 14.2 Pre-Commit Validation

Before committing documentation changes:

```bash
# Quick validation checklist
- [ ] All Markdown files pass linting rules
- [ ] No broken internal links
- [ ] Badges render correctly
- [ ] No TODO/TBD markers remain
- [ ] No hardcoded secrets
- [ ] Files end with newline
- [ ] ATX headers used consistently
```

### 14.3 Documentation Review Checklist

When reviewing documentation PRs:

```markdown
## Documentation Review Checklist

### Structure
- [ ] Follows SDLC folder structure
- [ ] Placed in the correct section
- [ ] Linked from section README
- [ ] Referenced from root docs/README.md if applicable

### Content
- [ ] Clear, concise writing
- [ ] No jargon without definition
- [ ] Code examples are accurate and runnable
- [ ] All claims are verifiable
- [ ] No outdated information

### Formatting
- [ ] Single H1 header per file
- [ ] ATX-style headers
- [ ] Fenced code blocks with language identifiers
- [ ] Tables for structured data
- [ ] Badges use standard format

### Quality
- [ ] Passes all linting rules
- [ ] No broken links
- [ ] No TODO/TBD markers
- [ ] No hardcoded secrets
- [ ] Accurate tech stack references
```

---

## Section 15: Reference Files

| Reference File | Purpose | Slash Command |
|---------------|---------|---------------|
| `references/sdlc-structure.md` | Complete SDLC folder structure with all files | `/docs scaffold` |
| `references/sdlc-templates.md` | Product spec, roadmap, support, and runbook templates | `/docs spec`, `/docs roadmap`, `/docs runbook`, `/docs support` |
| `references/onboarding-template.md` | Full onboarding guide template with tech stack reference | `/docs onboarding` |
| `references/badges.md` | Complete badge catalog with all available badges | All commands |
| `references/documentation-lint-rules.md` | Detailed linting rules with examples and auto-fix guidance | `/docs validate`, `/docs health` |
| `references/adr-template.md` | ADR template with lifecycle states | ADR creation |

---

## Section 16: Workflow

When invoked, follow this decision tree:

```
/docs [command]
    │
    ├── scaffold ──────► Detect project type
    │                     │
    │                     ├── fullstack-bun-solidjs-micronaut?
    │                     │   └── Generate full SDLC structure
    │                     │       ├── 00-product/ (product spec stub, roadmap stub)
    │                     │       ├── 01-architecture/ (ADR index, ADR 0001)
    │                     │       ├── 02-development/ (onboarding stub)
    │                     │       ├── 03-deployment/ (runbook stub)
    │                     │       ├── 04-api/ (OpenAPI stub)
    │                     │       └── 05-support/ (FAQ stub, triage stub)
    │                     │
    │                     ├── frontend-solidjs?
    │                     │   └── Generate frontend-focused structure
    │                     │
    │                     ├── backend-micronaut?
    │                     │   └── Generate backend-focused structure
    │                     │
    │                     └── [other types]
    │                         └── Adapt structure accordingly
    │
    ├── spec ───────────► Run 3-block interview
    │                     │
    │                     ├── Block 1: Context & Vision (6 questions)
    │                     ├── Block 2: Features & Requirements (5 questions)
    │                     └── Block 3: Constraints & Success (5 questions)
    │                         │
    │                         └── Generate docs/00-product/product-specification.md
    │
    ├── roadmap ────────► Gather version/milestone info
    │                     │
    │                     └── Generate docs/00-product/roadmap.md
    │                         ├── Format 1: Markdown table
    │                         ├── Format 2: Mermaid Gantt chart
    │                         ├── Format 3: GitHub Milestones JSON
    │                         └── Format 4: Phase summary
    │
    ├── onboarding ─────► Gather project specifics
    │                     │
    │                     └── Generate docs/02-development/onboarding-guide.md
    │                         ├── Prerequisites (software, extensions, env vars)
    │                         ├── Tech stack reference table
    │                         ├── Quick start (5-minute setup)
    │                         ├── Project structure overview
    │                         ├── Daily workflow guide
    │                         ├── Common commands reference
    │                         └── Troubleshooting table
    │
    ├── validate ───────► Scan docs/ directory
    │                     │
    │                     ├── Apply linting rules (DL-001 to DL-015)
    │                     ├── Check internal links
    │                     ├── Check badge format
    │                     ├── Check SDLC structure
    │                     └── Generate validation report
    │
    ├── health ─────────► Scan docs/ directory
    │                     │
    │                     ├── Score Quality (60 points)
    │                     │   ├── Completeness (15)
    │                     │   ├── Accuracy (10)
    │                     │   ├── Currency (10)
    │                     │   ├── Linting (10)
    │                     │   ├── Readability (10)
    │                     │   └── Traceability (5)
    │                     │
    │                     ├── Score SDLC Coverage (40 points)
    │                     │   ├── 00-product/ (10)
    │                     │   ├── 01-architecture/ (10)
    │                     │   ├── 02-development/ (8)
    │                     │   ├── 03-deployment/ (6)
    │                     │   ├── 04-api/ (4)
    │                     │   └── 05-support/ (2)
    │                     │
    │                     └── Generate health-report.md
    │
    ├── runbook ────────► Gather service details
    │                     │
    │                     └── Generate docs/03-deployment/runbook-<service>.md
    │                         ├── Service overview and architecture
    │                         ├── SLOs and health checks
    │                         ├── Common operations (deploy, scale, rollback)
    │                         ├── Alert response procedures
    │                         ├── Disaster recovery
    │                         └── On-call contacts
    │
    └── support ────────► Scaffold support cluster
                          │
                          └── Generate docs/05-support/
                              ├── faq.md
                              ├── triage-guide.md
                              ├── sla.md
                              ├── post-mortem-template.md
                              └── known-issues.md
```

---

## Section 17: Rules

1. **Documentation is code** — Version-controlled, reviewed, linted, tested
2. **Single source of truth** — No duplicated information; link, don't copy
3. **Templates are mandatory** — Every artifact follows its template
4. **Badges for status** — Always use Shields.io badges for status indicators
5. **ATX headers only** — No Setext-style headers anywhere
6. **Fenced code blocks** — Always specify language identifier
7. **Link, don't inline** — Cross-reference related documents with relative links
8. **Health check regularly** — Run `/docs health` at least once per milestone
9. **No TODO in committed docs** — Resolve or create a task before merging
10. **Tech stack references are versioned** — Always include version numbers
11. **Every ADR is immutable** — Accepted ADRs are never edited; create new ones to supersede
12. **Linting rules are non-negotiable** — Zero errors before merge
13. **Documentation review required** — Docs PRs need at least one review
14. **Update docs with code** — Documentation updates accompany code changes in the same PR
15. **Health score ≥ 80 for launch** — Production launch requires documentation health ≥ 80/100
