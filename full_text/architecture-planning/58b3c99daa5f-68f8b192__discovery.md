---
name: discovery
description: >
  Discovery & Requirements Gathering phase of the SDLC. Systematically elicit, analyze,
  and document product requirements before design or implementation begins. TRIGGER when:
  user mentions "gather requirements", "write PRD", "create user stories", "feasibility check",
  "stakeholder interview", "discovery phase", "requirements elicitation", "define scope",
  "product requirements", "need a spec", "what should we build", "project kickoff",
  "business requirements", "functional requirements", "non-functional requirements",
  "acceptance criteria", "domain model", "competitive analysis", "MoSCoW", "5W1H",
  "user story mapping", "define MVP", "scope the project", or starts a new project with
  ambiguous or incomplete requirements.
license: MIT
metadata:
  compatible_agents:
    - claude-code
  author: agentden
  version: "1.0.0"
  category: sdlc-discovery
  tags:
    - requirements
    - discovery
    - stakeholders
    - prd
    - user-stories
    - feasibility
    - domain-analysis
    - moscow
    - acceptance-criteria
    - competitive-analysis
  tech_stack:
    frontend: "Bun + TypeScript 5.8 (strict) + SolidJS 1.9 + SolidStart (SSG) + TailwindCSS 4.1 + Iconify-Solid"
    backend: "Java 21 + Micronaut 4.7 + Gradle 8.13 (Kotlin DSL)"
    infrastructure: "Docker/Podman, nginx:stable-alpine, bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl"
---

# Discovery & Requirements Gathering

Systematically elicit, analyze, and document product requirements before design or implementation begins. This skill transforms ambiguous ideas into actionable, validated specifications.

## Slash Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `/discovery spec` | Generate a full PRD from gathered context | `docs/prd/<project>-prd.md` |
| `/discovery stories` | Write user stories with acceptance criteria from requirements | `docs/stories/<epic>-stories.md` |
| `/discovery feasibility` | Assess technical feasibility against the tech stack | `docs/feasibility/<project>-feasibility.md` |
| `/discovery check` | Validate existing PRD for completeness and consistency | Inline review report |
| `/discovery domain` | Produce domain model with entities, glossary, and workflows | `docs/domain/<project>-domain.md` |
| `/discovery interview` | Run a structured 5W1H stakeholder interview | Interview notes in conversation |

## Announce

When this skill activates, announce:

> "Using the **discovery** skill to gather and document requirements."

## Phase 0: Triage

Before starting discovery, determine what the user actually needs:

1. **New project with vague idea** → Start from Phase 1 (full discovery)
2. **Existing idea, need spec** → Start from Phase 2 (requirements elicitation), gather quick context first
3. **Have requirements, need user stories** → Jump to Phase 3 (user story writing)
4. **Need feasibility check on an existing spec** → Jump to Phase 5 (feasibility assessment)
5. **Competitive research needed** → Jump to Phase 6 (research & competitive analysis)
6. **PRD exists but needs validation** → Run `/discovery check`

Ask the user which entry point fits, or infer from context and confirm.

---

## Phase 1: Stakeholder Engagement (5W1H)

### 1.1 Identify Stakeholders

Map every person or group who has a stake in the product:

| Stakeholder Type | Examples | Engagement Method |
|-----------------|----------|-------------------|
| Decision Maker | Product owner, VP, CEO | Executive interview (30 min) |
| End User | Daily users, admin users | User interview or survey |
| Technical Lead | Architect, senior engineer | Technical feasibility session |
| Operations | DevOps, SRE, support | Operational requirements session |
| Compliance | Legal, security, accessibility | Compliance checklist review |
| External | Partners, API consumers, regulators | Stakeholder-specific interview |

Create a stakeholder register:

```markdown
## Stakeholder Register

| Name/Role | Type | Influence | Interest | Availability | Interview Status |
|-----------|------|-----------|----------|-------------|-----------------|
| [role] | Decision Maker | High | High | [dates] | Pending |
```

### 1.2 Conduct 5W1H Interviews

For each stakeholder (or in a workshop format), work through these dimensions systematically:

**WHO** — People and actors:
- Who are the end users? (personas, roles, demographics)
- Who are the administrators? (roles, permission levels)
- Who are the secondary users? (API consumers, support staff)
- Who will maintain this system? (team composition, skills)
- Who are the stakeholders NOT in the room? (who else cares?)

**WHAT** — The product and features:
- What problem does this solve? (pain points, unmet needs)
- What does success look like? (measurable outcomes, KPIs)
- What are the core features? (must-have vs nice-to-have)
- What does the user do today without this? (current workaround)
- What data flows in and out? (inputs, outputs, integrations)

**WHEN** — Timeline and triggers:
- When does this need to be live? (hard deadlines, target dates)
- When do users interact with it? (frequency, time of day, seasonality)
- When does data need to be available? (real-time, batch, on-demand)
- When are the review checkpoints? (milestones, demo dates)

**WHERE** — Context and environment:
- Where will users access this? (mobile, desktop, kiosk, embedded)
- Where does the system run? (cloud, on-prem, edge, hybrid)
- Where does data reside? (regions, compliance boundaries)
- Where does this fit in the existing ecosystem? (upstream/downstream systems)

**WHY** — Motivation and business case:
- Why build this now? (market pressure, compliance, strategic initiative)
- Why not buy/off-the-shelf? (differentiation, customization needs)
- Why this approach over alternatives? (build vs buy vs partner analysis)
- Why will users adopt this? (adoption drivers, switching costs)

**HOW** — Process and interaction:
- How do users accomplish their goal today? (current workflow)
- How should the new workflow work? (desired workflow)
- How will we measure adoption? (analytics, success metrics)
- How will this be supported? (training, documentation, SLAs)

### 1.3 Interview Execution Protocol

For each interview:

1. **Prep** (5 min): Review stakeholder background, prepare 5-7 targeted questions
2. **Open** (5 min): State purpose, set scope ("We're gathering requirements, not designing solutions yet")
3. **Probe** (20 min): Work through 5W1H dimensions, prioritize open-ended questions
4. **Validate** (5 min): Read back key points, confirm understanding
5. **Capture** (5 min): Write up notes immediately, flag open questions

**Interview anti-patterns to avoid:**
- Leading questions ("Don't you think we should...?")
- Solutioning during discovery ("What if we used React for...")
- Assuming consensus ("Everyone agrees that...")
- Skipping "dumb" questions (they often reveal hidden assumptions)

### 1.4 Synthesize Stakeholder Input

After all interviews, produce a synthesis:

```markdown
## Stakeholder Synthesis

### Consensus Points
- [What everyone agrees on]

### Divergent Views
- [Where stakeholders disagree, with positions]

### Open Questions
- [Unresolved items requiring follow-up]

### Assumptions Made
- [Assumptions baked into requirements, to be validated]

### Conflicts to Resolve
- [Prioritization conflicts, resource constraints, timeline tension]
```

---

## Phase 2: Requirements Elicitation (MoSCoW)

### 2.1 Raw Requirements Collection

Gather requirements from all sources:

- Stakeholder interviews (Phase 1 output)
- Existing documentation (specs, wikis, tickets)
- User analytics and behavioral data
- Support tickets and bug reports
- Competitive product analysis
- Regulatory and compliance requirements
- Technical constraints and platform limitations

List every requirement as a raw statement, attributed to its source:

```markdown
## Raw Requirements

| ID | Requirement | Source | Type | Priority (TBD) |
|----|------------|--------|------|---------------|
| REQ-001 | "Users must be able to reset their password" | Stakeholder interview - PM | Functional | Must |
| REQ-002 | "Page loads in under 2 seconds" | Analytics review | Non-functional | Must |
| REQ-003 | "Support dark mode" | User survey | Functional | Could |
```

### 2.2 Classify Requirements

Categorize each requirement:

**By type:**
- **Functional** — What the system does (features, behaviors, data operations)
- **Non-functional** — How the system performs (performance, security, accessibility, reliability)
- **Constraint** — Hard limitations (budget, timeline, technology, compliance)
- **Implicit** — Assumed requirements not stated by stakeholders (discover these!)

**Non-functional requirement categories to probe:**

| Category | Key Questions | Typical Targets |
|----------|--------------|-----------------|
| Performance | Response time, throughput, concurrency? | < 200ms p95, 1000 RPS |
| Scalability | User growth, data growth, peak loads? | 10x current in 2 years |
| Availability | Uptime SLA, maintenance windows? | 99.9% uptime |
| Security | Data classification, auth model, compliance? | OWASP Top 10, SOC 2 |
| Accessibility | WCAG level, assistive tech, regulations? | WCAG 2.2 AA |
| Internationalization | Languages, locales, RTL, currencies? | en-US first, i18n-ready |
| Observability | Logging, metrics, tracing, alerting? | Structured logs, APM |
| Reliability | RPO, RTO, disaster recovery? | RPO 1hr, RTO 4hr |

### 2.3 MoSCoW Prioritization

Rank every requirement using MoSCoW:

| Priority | Meaning | Criteria | Typical Allocation |
|----------|---------|----------|--------------------|
| **Must** | Non-negotiable for launch | Without this, the product fails its core purpose | ~60% of effort |
| **Should** | Important but not critical | Adds significant value, workaround exists | ~20% of effort |
| **Could** | Nice to have | Enhances experience, low cost of deferral | ~15% of effort |
| **Won't** (this time) | Explicitly excluded | Acknowledged but deferred to future release | ~5% documentation |

**Prioritization exercise:**

For each requirement, ask:
1. Does the product fundamentally work without this? → No = **Must**
2. Is there a painful but viable workaround? → Yes = **Should**
3. Would users notice and appreciate this? → Yes but not Must/Should = **Could**
4. Is this a future-phase item or out of scope? → Yes = **Won't**

**Conflict resolution:**
- If stakeholders disagree on priority, use a forced-ranking exercise
- If everything is "Must", challenge: "If you could only ship 3 things, which 3?"
- Document the reasoning behind each priority decision

### 2.4 Requirements Quality Checklist

Validate each requirement meets INVEST-like qualities for requirements:

- [ ] **Specific** — Precisely stated, no ambiguity
- [ ] **Measurable** — Has acceptance criteria or quantitative threshold
- [ ] **Achievable** — Technically feasible within constraints
- [ ] **Relevant** — Traces to a stakeholder need or business goal
- [ ] **Traceable** — Has a unique ID and source attribution
- [ ] **Testable** — Can be verified through testing
- [ ] **Unambiguous** — Only one interpretation possible

Rewrite any requirement that fails this checklist. Common fixes:

| Problem | Before | After |
|---------|--------|-------|
| Vague | "The system should be fast" | "API responses return in < 200ms at p95" |
| Untestable | "Good user experience" | "Task completion rate > 90% in usability test" |
| Compound | "Users can register and login" | Split into REQ-001a (register) and REQ-001b (login) |
| Missing criteria | "Support file upload" | "Support file upload ≤ 50MB for JPEG, PNG, PDF" |

---

## Phase 3: User Story Writing

### 3.1 Epic Decomposition

Break the product into epics — large bodies of work that deliver cohesive value:

```markdown
## Epic Map

| Epic ID | Epic Name | Description | # Stories | MoSCoW |
|---------|-----------|-------------|-----------|--------|
| EPIC-001 | User Management | Registration, auth, profiles | 8 | Must |
| EPIC-002 | Dashboard | Main user workspace | 5 | Must |
| EPIC-003 | Reporting | Data export and visualization | 4 | Should |
```

### 3.2 User Story Format

Every user story follows this structure:

```markdown
### US-XXX: [Story Title]

**As a** [persona/role]
**I want** [action/capability]
**So that** [business value/outcome]

**Priority:** Must / Should / Could
**Epic:** EPIC-XXX
**Estimate:** [story points or T-shirt size]
**Sprint:** [target sprint or phase]

#### Acceptance Criteria (Given/When/Then)

**AC-1: [Scenario Name]**
- **Given** [precondition/context]
- **When** [action/trigger]
- **Then** [expected outcome]

**AC-2: [Scenario Name]**
- **Given** [precondition/context]
- **When** [action/trigger]
- **Then** [expected outcome]

#### Edge Cases
- [Edge case 1]: [expected behavior]
- [Edge case 2]: [expected behavior]

#### Dependencies
- [US-YYY must complete first]
- [External API ZZZ must be available]

#### Design Notes
- [Link to mockup or wireframe]
- [Interaction pattern reference]

#### Questions / Open Items
- [ ] [Unresolved question]
```

### 3.3 Persona Definitions

Before writing stories, define the personas:

```markdown
## Personas

### Persona: [Name] ([Role])

**Demographics:** [relevant context]
**Technical Proficiency:** [low/medium/high]
**Primary Goals:** [what they want to accomplish]
**Pain Points:** [current frustrations]
**Usage Pattern:** [frequency, device, context]
**Success Metrics:** [how they measure success]
```

Every user story must reference a defined persona. If no persona fits, define a new one.

### 3.4 Acceptance Criteria Standards

**Every acceptance criterion must be:**
- Testable with a clear pass/fail
- Written from the user's perspective (not implementation)
- Specific about expected behavior (not "works correctly")
- Independent of other acceptance criteria

**Anti-patterns to avoid in acceptance criteria:**
- Implementation details ("uses React state management") — describe behavior, not implementation
- Vague outcomes ("looks good", "works properly") — specify exact expected behavior
- Missing error cases — every happy path needs corresponding error/edge case criteria
- Untestable statements ("seamless experience") — must be verifiable

**Acceptance criteria completeness check:**
- [ ] Happy path covered
- [ ] Error/invalid input covered
- [ ] Empty/zero/null state covered
- [ ] Permission/access boundary covered
- [ ] Concurrent/conflict scenario covered (if applicable)

### 3.5 Story Mapping

Arrange stories in a release-oriented flow:

```
                    ┌─────────────────────────────────────────────┐
                    │           User Journey Steps                │
                    ├──────────┬──────────┬──────────┬────────────┤
Release 1 (MVP)    │ Reg/Login│ Dashboard│ Basic Ops│ Settings   │
(Must)             │ US-001   │ US-010   │ US-020   │ US-030     │
                    │ US-002   │ US-011   │ US-021   │ US-031     │
                    ├──────────┼──────────┼──────────┼────────────┤
Release 2          │ SSO      │ Filters  │ Bulk Ops │ Profiles   │
(Should)           │ US-003   │ US-012   │ US-022   │ US-032     │
                    ├──────────┼──────────┼──────────┼────────────┤
Release 3          │ Social   │ Charts   │ Export   │ Prefs      │
(Could)            │ US-004   │ US-013   │ US-023   │ US-033     │
                    └──────────┴──────────┴──────────┴────────────┘
```

---

## Phase 4: Domain Analysis

### 4.1 Entity Identification

Identify all domain entities from requirements and user stories:

```markdown
## Domain Entities

| Entity | Description | Key Attributes | Relationships | Primary User Stories |
|--------|-------------|----------------|---------------|---------------------|
| User | A registered person | id, email, name, role, status | has many Projects | US-001, US-002 |
| Project | A user's workspace | id, name, owner_id, status | belongs to User, has many Tasks | US-010, US-011 |
| Task | A unit of work | id, title, status, assignee_id | belongs to Project, assigned to User | US-020, US-021 |
```

### 4.2 Entity Relationship Diagram (Textual)

```
User ──1:N──▶ Project ──1:N──▶ Task
  │                          │
  └──1:N──▶ Comment    ──N:1─┘
                    │
               ┌────┴────┐
               ▼         ▼
            Label    Attachment
```

### 4.3 Domain Glossary

Create an unambiguous vocabulary:

```markdown
## Domain Glossary

| Term | Definition | Also Known As | Usage Context |
|------|-----------|---------------|---------------|
| Project | A container for related tasks, owned by a single user | Workspace | Domain model, UI |
| Task | A discrete unit of work within a project, assignable to a user | Item, Ticket | Domain model, UI |
| Owner | The User who created and has administrative rights over a Project | Creator | Authorization logic |
| Assignee | The User responsible for completing a Task | Responsible | Task management |
| Status | The current lifecycle state of a Task (Draft, In Progress, Done, Archived) | State | Workflow engine |
```

**Rules for glossary entries:**
- One definition per term — no ambiguity
- Cross-reference related terms
- Note when a term has different meanings in different contexts
- Include acronyms and their expansions
- Include "Do Not Use" terms that create confusion

### 4.4 Workflow Analysis

Document state machines and business processes:

```markdown
## Workflow: Task Lifecycle

States: Draft → In Progress → In Review → Done → Archived

```
  ┌───────┐    start     ┌─────────────┐   assign    ┌───────────┐
  │ Draft │─────────────▶│ In Progress │────────────▶│ In Review │
  └───────┘              └─────────────┘             └───────────┘
     ▲                       │    ▲                      │     │
     │                       │    │                      │     │
     │                  reopen│    │                      │     │
     │                       ▼    │                      ▼     │
     │                   ┌───────┴──┐   approve    ┌──────────┐│
     │                   │ Blocked  │─────────────▶│   Done   ││
     │                   └──────────┘              └──────────┘│
     │                                                │        │
     └────────────────────────────────────────────────┘        │
                                                         archive
                                                                │
                                                          ┌──────────┐
                                                          │ Archived │
                                                          └──────────┘
```

Transitions:
| From | To | Trigger | Guard Condition | Side Effect |
|------|----|---------|-----------------|-------------|
| Draft | In Progress | User clicks "Start" | User is assignee | Set started_at timestamp |
| In Progress | In Review | User clicks "Submit" | All required fields filled | Notify reviewer |
| In Review | Done | Reviewer approves | Reviewer has permission | Set completed_at |
| In Review | In Progress | Reviewer requests changes | Reviewer has permission | Add comment with feedback |
| Done | Archived | Auto after 30 days | No activity in 30 days | Remove from active views |
| Any | Blocked | User marks blocked | User is assignee | Notify project owner |
```

### 4.5 Business Rules Catalog

```markdown
## Business Rules

| Rule ID | Name | Description | Enforced In | Exception Handling |
|---------|------|-------------|-------------|-------------------|
| BR-001 | Single Owner | A project has exactly one owner; ownership cannot be shared | ProjectService.create() | Return error if owner_id is null |
| BR-002 | Assignee Must Be Member | Only project members can be assigned tasks | TaskService.assign() | Return 403 with membership message |
| BR-003 | Status Transition | Tasks follow the defined lifecycle; backward transitions require justification | TaskService.transition() | Reject invalid transitions, log attempt |
| BR-004 | Soft Delete | Entities are soft-deleted and recoverable for 30 days | All delete endpoints | Mark as deleted, schedule hard delete |
```

---

## Phase 5: Feasibility Assessment

### 5.1 Technical Feasibility Matrix

Evaluate each requirement against the tech stack:

```markdown
## Technical Feasibility

### Frontend Assessment (Bun + SolidJS 1.9 + SolidStart SSG + TailwindCSS 4.1)

| Requirement | Feasible? | Approach | Risk | Notes |
|-------------|-----------|----------|------|-------|
| Real-time updates | Yes | Server-Sent Events or WebSocket via SolidJS resource | Low | SolidStart supports SSE natively |
| Offline support | Partial | Service Worker + IndexedDB | Medium | SSG pages are cacheable; dynamic data needs sync strategy |
| Complex forms | Yes | SolidJS reactive primitives + custom validation | Low | Fine-grained reactivity handles form state well |
| Data visualization | Yes | Chart library (e.g., Chart.js, D3) via SolidJS wrapper | Low | Ensure library is SSR-compatible for SSG |
| Accessibility | Yes | Semantic HTML + ARIA + TailwindCSS | Low | SolidJS has no virtual DOM overhead for a11y tree |

### Backend Assessment (Java 21 + Micronaut 4.7)

| Requirement | Feasible? | Approach | Risk | Notes |
|-------------|-----------|----------|------|-------|
| REST API | Yes | Micronaut HTTP Server with @Controller | Low | Core framework capability |
| Authentication | Yes | Micronaut Security (JWT, OAuth, session) | Low | Built-in module |
| File storage | Yes | S3-compatible API or local storage | Low | Micronaut supports multipart upload |
| Background jobs | Yes | Micronaut's @Scheduled or integrate with job queue | Low | CRaC may affect scheduled tasks — verify |
| WebSocket | Yes | Micronaut WebSocket support | Medium | Verify compatibility with CRaC checkpoint/restore |
| Database | Yes | Micronaut Data with JDBC/JPA or R2DBC | Low | PostgreSQL recommended |

### Infrastructure Assessment (Docker + nginx + Liberica CRaC)

| Requirement | Feasible? | Approach | Risk | Notes |
|-------------|-----------|----------|------|-------|
| Horizontal scaling | Yes | Stateless containers behind load balancer | Low | nginx handles upstream routing |
| SSL/TLS | Yes | nginx terminates TLS | Low | Standard reverse proxy pattern |
| CDN | Yes | nginx caches SSG output or use external CDN | Low | Static assets from nginx or offload to CDN |
| CI/CD | Yes | GitHub Actions / GitLab CI with Docker builds | Low | Multi-stage Dockerfiles provided in templates |
| Monitoring | Yes | Prometheus metrics + Micronaut management endpoint | Low | Micronaut has built-in metrics endpoint |
```

### 5.2 Risk Assessment

```markdown
## Risk Register

| Risk ID | Risk Description | Probability | Impact | Mitigation | Owner |
|---------|-----------------|-------------|--------|------------|-------|
| RISK-001 | CRaC checkpoint/restore conflicts with runtime state changes | Medium | High | Test early; have fallback to standard JDK container | Platform |
| RISK-002 | SolidStart SSG limitations for highly dynamic content | Low | High | Identify dynamic vs static boundaries; consider SPA mode for dynamic sections | Frontend |
| RISK-003 | TailwindCSS 4.1 breaking changes from 3.x patterns | Low | Medium | Lock version; review migration guide if upgrading existing project | Frontend |
| RISK-004 | Micronaut 4.7 compatibility with required libraries | Low | Medium | Verify each dependency against Micronaut BOM; check community support | Backend |
```

### 5.3 Technology Decision Record

For each significant technology choice, document:

```markdown
## Technology Decision: [Topic]

**Decision:** [What was chosen]
**Alternatives Considered:** [What else was evaluated]
**Rationale:** [Why this choice]
**Trade-offs:** [What we gain and lose]
**Reversibility:** [How hard to change later]
**Constraints:** [What must be true for this to work]
```

### 5.4 Go/No-Go Checklist

Before proceeding to design phase:

- [ ] All **Must** requirements are technically feasible
- [ ] No unresolved high-impact/high-probability risks
- [ ] Tech stack can support all non-functional requirements
- [ ] Team has (or can acquire) necessary skills
- [ ] Third-party dependencies are available and supported
- [ ] Infrastructure can meet deployment requirements
- [ ] Security and compliance requirements can be met
- [ ] Performance targets are achievable with chosen architecture
- [ ] Budget and timeline are realistic given technical scope
- [ ] All stakeholder concerns have been addressed

---

## Phase 6: Research & Competitive Analysis

### 6.1 Market Landscape

```markdown
## Competitive Analysis

| Competitor | Positioning | Key Features | Strengths | Weaknesses | Differentiation Opportunity |
|-----------|-------------|-------------|-----------|------------|---------------------------|
| [Competitor A] | [Market position] | [Top 5 features] | [What they do well] | [What they lack] | [How we differentiate] |
| [Competitor B] | [Market position] | [Top 5 features] | [What they do well] | [What they lack] | [How we differentiate] |
```

### 6.2 Feature Parity Matrix

```markdown
## Feature Comparison

| Feature | Us | Competitor A | Competitor B | Industry Standard |
|---------|----|-------------|-------------|--------------------|
| [Feature 1] | Planned | Yes | Yes | Expected |
| [Feature 2] | Planned (MVP) | Yes | Partial | Nice-to-have |
| [Feature 3] | Not planned | Yes | No | Emerging |
```

### 6.3 Best Practices Research

For the domain, research and document:

- **Industry standards**: Relevant RFCs, specs, compliance frameworks
- **Design patterns**: Proven architectural patterns for this problem space
- **Anti-patterns**: Known failure modes to avoid
- **Open-source options**: Libraries, tools, or frameworks that solve sub-problems
- **Performance benchmarks**: Expected performance characteristics for similar systems

### 6.4 Technology Spikes

For high-risk or unknown areas, define technology spikes:

```markdown
## Spike: [Topic]

**Goal:** [What we need to learn]
**Timebox:** [Hours or days]
**Approach:** [What we'll build/test]
**Success Criteria:** [What answer we need]
**Output:** [Prototype, benchmark results, or documented findings]
```

---

## Phase 7: Generate PRD

### 7.1 PRD Document Structure

Generate the PRD using the template at `references/prd-template.md`. The complete PRD contains:

```markdown
# Product Requirements Document: [Product Name]

## Document Control
| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Draft / Review / Approved |
| Author | [Name] |
| Stakeholders | [List] |
| Last Updated | [Date] |

## 1. Executive Summary
[2-3 paragraphs: What, Why, For Whom, Expected Outcome]

## 2. Problem Statement
[What problem exists, who experiences it, how severe is it, evidence]

## 3. Product Vision & Goals
### Vision
[1-2 sentences describing the aspirational future state]

### Goals & Success Metrics
| Goal | Metric | Target | Measurement Method |
|------|--------|--------|-------------------|
| [Goal 1] | [KPI] | [Target] | [How measured] |

## 4. Target Users & Personas
[Personas from Phase 3.3]

## 5. Scope
### In Scope (This Release)
[Feature list with MoSCoW priorities]

### Out of Scope (Future Releases)
[Explicitly excluded items]

### Non-Goals
[Things this product will never do]

## 6. Functional Requirements
[Requirements from Phase 2, organized by epic/feature area]

### 6.1 [Epic/Feature Area]
| ID | Requirement | MoSCoW | User Stories | Acceptance Criteria |
|----|------------|--------|-------------|-------------------|
| REQ-001 | [Description] | Must | US-001, US-002 | AC-1, AC-2 |

## 7. Non-Functional Requirements
| ID | Category | Requirement | Target | Measurement |
|----|----------|-------------|--------|-------------|
| NFR-001 | Performance | API response time | < 200ms p95 | APM monitoring |
| NFR-002 | Availability | Uptime | 99.9% | Uptime monitoring |
| NFR-003 | Security | Authentication | JWT + refresh tokens | Security audit |
| NFR-004 | Accessibility | WCAG compliance | 2.2 AA | Automated + manual audit |

## 8. User Stories
[Complete user stories from Phase 3, or reference to stories document]

## 9. Domain Model
[Entities, relationships, glossary, workflows from Phase 4]

## 10. Business Rules
[Business rules catalog from Phase 4.5]

## 11. Technical Constraints
[From feasibility assessment — what must be true]

## 12. Assumptions & Dependencies
### Assumptions
- [Assumption 1]
- [Assumption 2]

### Dependencies
- [External dependency 1]
- [Third-party service 2]

## 13. Risks & Mitigations
[Risk register from Phase 5.2]

## 14. Competitive Landscape
[Competitive analysis summary from Phase 6]

## 15. Open Questions
| ID | Question | Owner | Due Date | Status |
|----|----------|-------|----------|--------|
| OQ-001 | [Question] | [Who decides] | [Date] | Open |

## 16. Approval
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | | | |
| Tech Lead | | | |
| Design Lead | | | |
```

### 7.2 PRD Quality Validation

Run `/discovery check` to validate the PRD:

**Completeness check:**
- [ ] Every stakeholder concern is addressed
- [ ] Every feature maps to at least one user story
- [ ] Every user story has acceptance criteria
- [ ] Every non-functional requirement has a measurable target
- [ ] All entities from user stories appear in domain model
- [ ] Business rules cover all workflow transitions
- [ ] Open questions have owners and due dates

**Consistency check:**
- [ ] Terminology is consistent with domain glossary (no synonyms used)
- [ ] Priority levels don't conflict (nothing is both Must and Won't)
- [ ] Dependencies don't create circular references
- [ ] MoSCoW allocation is realistic (not 100% Must)
- [ ] Non-functional targets don't contradict each other

**Traceability check:**
- [ ] Every requirement traces to a stakeholder source
- [ ] Every user story traces to a requirement
- [ ] Every acceptance criterion traces to a user story
- [ ] Every risk traces to a requirement or constraint
- [ ] Every assumption is documented

### 7.3 Output Files

After PRD generation, produce these deliverables:

| File | Location | Content |
|------|----------|---------|
| PRD | `docs/prd/<project>-prd.md` | Full product requirements document |
| User Stories | `docs/stories/<epic>-stories.md` | User stories with acceptance criteria (one file per epic or consolidated) |
| Domain Model | `docs/domain/<project>-domain.md` | Entities, relationships, glossary, workflows |
| Feasibility Report | `docs/feasibility/<project>-feasibility.md` | Technical feasibility assessment |
| Stakeholder Notes | `docs/discovery/<project>-stakeholders.md` | Interview notes and synthesis |

---

## Quick Reference: Discovery Checklist

Use this as a fast-path when time is limited:

- [ ] Problem statement articulated (5W1H)
- [ ] Stakeholders identified and interviewed
- [ ] Requirements collected and MoSCoW prioritized
- [ ] Personas defined
- [ ] User stories written with Given/When/Then acceptance criteria
- [ ] Domain entities and glossary documented
- [ ] Workflows mapped with state transitions
- [ ] Business rules cataloged
- [ ] Technical feasibility confirmed against tech stack
- [ ] Risks identified with mitigations
- [ ] Competitive landscape researched
- [ ] PRD generated and validated
- [ ] PRD reviewed and approved by stakeholders

---

## Reference Files

| File | Purpose | When to Use |
|------|---------|-------------|
| [references/prd-template.md](references/prd-template.md) | PRD document template with full structure | Generating a new PRD |
| [references/user-story-template.md](references/user-story-template.md) | User story format with acceptance criteria patterns | Writing user stories |
| [references/feasibility-checklist.md](references/feasibility-checklist.md) | Technical feasibility checklist for the tech stack | Assessing feasibility |
| [references/domain-glossary-template.md](references/domain-glossary-template.md) | Domain glossary and entity model template | Documenting domain analysis |
