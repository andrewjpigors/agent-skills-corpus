---
name: harness-ba
description: "Business Analysis domain skill for the harness plugin. Provides BA methodology selection (Waterfall BA, Agile BA, Lean BA, Design Thinking BA, Six Sigma BA), development methodology (Requirements-First, User-Story-First, Process-First, Data-First, Stakeholder-First), verification strategy, deliverable verification, evaluation criteria (completeness, traceability, stakeholder_alignment, feasibility), and sprint contract checklist templates. Activated when domain_profile is "business_analysis"."
---

# Business Analysis Domain Skill

> **Domain-specific.** This skill provides the HOW for business analysis projects. The harness provides the WHEN (orchestration, sprint contracts, feature ledger). This skill provides the HOW (methodology selection, development methodology, deliverable verification, evaluation criteria anchors, and BA-specific patterns).

Activated when `domain_profile: business_analysis` is declared in `.harness/spec.md`.

## Scope of This Skill

This skill covers the full Business Analysis lifecycle:
- **Elicitation**: Stakeholder interviews, workshops, document analysis, observation
- **Analysis**: Requirements modeling, gap analysis, impact assessment, feasibility studies
- **Specification**: BRDs, use cases, user stories, process models, data dictionaries
- **Validation**: Requirements traceability, stakeholder sign-off, completeness audits
- **Management**: Change control, version management, requirements baseline

It is methodology-agnostic at its core — any of the supported approaches can be selected. Agile BA is the default because it provides the most natural mapping to harness sprint boundaries.


## Activation Check

This skill activates when `domain_profile: business_analysis` is set in `.harness/spec.md` or `.harness/state.json`.

Before using this skill's procedures:
1. Verify the project produces BA deliverables (BRDs, use cases, process maps, data dictionaries — not primarily code)
2. Read spec.md -> identify the selected BA methodology (Waterfall, Agile, Lean, etc.)
3. If no methodology specified -> default to Agile BA
4. Check if `business-analysis/` directory exists -> if yes, verify against the Repository Structure (Section 9)
5. Identify the industry context -> select appropriate reference frameworks from Section 7

---

## Section 1: BA Methodology

Select based on project characteristics during `/harness:start`:

| Methodology | When to Use | Phase Structure | Harness Mapping |
|-------------|-------------|-----------------|-----------------|
| Waterfall BA | Regulated industries, fixed-scope contracts | Inception, Elaboration, Construction, Transition | 1 sprint = 1 phase deliverable set |
| Agile BA | Iterative delivery, evolving requirements | Discovery, Elaboration, Delivery, Validation | 1 sprint = 1 user story cluster |
| Lean BA | Startup/MVP, hypothesis-driven | Problem, Solution, Validate, Pivot/Persevere | 1 sprint = 1 hypothesis + validation |
| Design Thinking BA | User-centric projects, innovation | Empathize, Define, Ideate, Prototype, Test | 1 sprint = 1 design thinking phase |
| Six Sigma BA | Process improvement, quality focus | Define, Measure, Analyze, Improve, Control (DMAIC) | 1 sprint = 1 DMAIC phase |

**Default:** Agile BA (if not specified by user).

The planner writes the selected methodology into `spec.md` during initialization. The coordinator uses the mapping to structure sprint boundaries accordingly.

---

## Section 2: Business Analysis Development Methodology

Select based on project type and stakeholder needs:

| Methodology | When to Use | How It Drives the Generator |
|-------------|-------------|----------------------------|
| Requirements-First | Compliance, regulated, audit-heavy | Generator documents formal requirements FIRST (BRD sections, acceptance criteria), then derives use cases and process models |
| User-Story-First | Agile teams, user-facing products | Generator writes user stories FIRST (persona, goal, acceptance criteria), then derives process flows and data needs |
| Process-First | Business process reengineering | Generator maps current-state processes FIRST (BPMN), then identifies improvement opportunities and requirements |
| Data-First | Data migration, analytics, master data | Generator defines data entities and relationships FIRST (ERD, data dictionary), then derives business rules and processes |
| Stakeholder-First | Political/complex organizations | Generator maps stakeholder concerns and influence FIRST, then derives requirements aligned to stakeholder priorities |

**Default:** Requirements-First for all BA projects (if not specified).

### How Methodology Drives the Harness

The chosen methodology affects every phase:

1. **Generator behavior**: What to produce first (requirements? user stories? process maps?)
2. **Evaluator criteria**: What to prioritize (requirements completeness? story quality? process accuracy?)
3. **Sprint contract**: What acceptance criteria to define (BRD coverage? story acceptance? process validation?)
4. **Artifact types**: What deliverables per sprint (BRDs? user story maps? BPMN diagrams?)

### Generator First-Action Table

| Methodology | Generator produces first | Then |
|-------------|------------------------|------|
| Requirements-First | Business Requirements Document with numbered requirements | Use cases, process models, traceability matrix |
| User-Story-First | User story map with personas and acceptance criteria | Process flows, data requirements, non-functional requirements |
| Process-First | Current-state BPMN process models | Gap analysis, future-state processes, derived requirements |
| Data-First | Conceptual data model and data dictionary | Business rules, data flow diagrams, integration requirements |
| Stakeholder-First | Stakeholder register with concerns and influence matrix | Prioritized requirements aligned to stakeholder needs |

---

## Section 3: Verification Strategy (BA Equivalent of Testing)

| Verification Type | BA Equivalent | Method |
|-------------------|--------------|--------|
| Unit test | Requirement validation | Each requirement has a unique ID, is testable, unambiguous, and traced to a business need |
| Integration test | Cross-document consistency | References between BRD, use cases, and process models resolve correctly |
| E2E test | Scenario walkthrough | Business scenario traces through all deliverables without gaps (stakeholder need -> requirement -> use case -> process -> acceptance criteria) |
| Smoke test | Deliverable completeness | Required documents exist and contain all mandatory sections |
| Regression | Standards compliance | BABOK knowledge areas covered, naming conventions followed, template structure maintained |

### Deliverable Completeness Checks

- Does the Business Requirements Document exist with all mandatory sections?
- Are all stakeholder concerns mapped to requirements?
- Does each requirement have a unique ID and acceptance criteria?
- Are all business processes modeled with correct BPMN notation?
- Does the traceability matrix link business needs to requirements to test cases?
- Is the glossary consistent across all documents?

---

## Section 4: Deliverable Verification (Equivalent of Build/Runtime)

Since BA produces documents, not running software, "build verification" means:

| Check | What to Verify | How |
|-------|---------------|-----|
| Document structure | Required sections present per template | Check headings/sections against BA document template |
| Cross-references | References between documents resolve | Grep for requirement IDs, verify targets exist in traceability matrix |
| Requirement quality | Each requirement is SMART (Specific, Measurable, Achievable, Relevant, Time-bound) | Pattern-check requirement text for ambiguous words ("should", "may", "etc.") |
| Naming conventions | Consistent naming across artifacts | Pattern matching on requirement IDs (REQ-xxx), use case IDs (UC-xxx), process IDs (BP-xxx) |
| Traceability | Business needs to requirements to use cases to test cases | Traceability matrix completeness check — no orphan requirements |
| Stakeholder coverage | All identified stakeholders have requirements addressed | Cross-reference stakeholder register with requirements ownership |
| Glossary consistency | Terms defined once and used consistently | Check glossary entries against document usage |

### BRD Section Gate Checks

| Section | Required Content |
|---------|-----------------|
| Executive Summary | Problem statement, proposed solution, business value |
| Stakeholders | Register with roles, concerns, influence, communication plan |
| Business Context | Current state, pain points, opportunity description |
| Scope | In-scope items, out-of-scope items, assumptions, constraints |
| Requirements | Functional requirements (numbered), non-functional requirements, business rules |
| Use Cases | Primary use cases with actors, preconditions, main flow, alternate flows |
| Process Models | Current-state and future-state BPMN diagrams |
| Data Requirements | Conceptual data model, data dictionary, data quality rules |
| Acceptance Criteria | Measurable criteria for each requirement group |
| Appendices | Glossary, traceability matrix, references |

---

## Section 5: Evaluation Criteria (Business Analysis Profile)

The 4 primary criteria for the `business_analysis` domain profile. The evaluator MUST use these anchors for consistent scoring across sprints.

### completeness (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no requirements or BA deliverables produced |
| 1 | Severely incomplete — some requirements listed but no structure, missing major sections |
| 2 | Below acceptable — requirements exist but significant gaps in coverage, missing stakeholder needs or non-functional requirements |
| 3 | Acceptable — all mandatory BRD sections present, functional and non-functional requirements documented, security and privacy requirements captured, no critical gaps |
| 4 | Strong — comprehensive requirements with edge cases addressed, complete use cases, thorough data requirements |
| 5 | Excellent — exhaustive coverage including business rules, exception flows, data quality rules, and measurable acceptance criteria for every requirement |

### traceability (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no traceability between artifacts |
| 1 | Severely incomplete — requirements exist but no IDs, no links to business needs |
| 2 | Below acceptable — requirement IDs assigned but traceability matrix incomplete or inconsistent |
| 3 | Acceptable — traceability matrix links business needs to requirements, each requirement has a unique ID and source reference |
| 4 | Strong — bidirectional traceability from business needs through requirements to use cases and acceptance criteria, no orphan requirements |
| 5 | Excellent — full forward and backward traceability with impact analysis capability, every requirement traced from business driver to test case, change impact paths documented |

### stakeholder_alignment (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no stakeholder analysis performed |
| 1 | Severely incomplete — stakeholders mentioned but not systematically identified or analyzed |
| 2 | Below acceptable — stakeholder register exists but concerns not mapped to requirements, no communication plan |
| 3 | Acceptable — all key stakeholders identified with roles and concerns, requirements address stated concerns, sign-off readiness evident |
| 4 | Strong — stakeholder influence matrix complete, conflicting concerns resolved with documented rationale, prioritization reflects stakeholder input |
| 5 | Excellent — stakeholder concerns systematically traced to requirements, conflict resolution documented, communication plan active, feedback incorporated into requirements |

### feasibility (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — requirements are unrealistic or no feasibility consideration |
| 1 | Severely incomplete — requirements exist but no resource, timeline, or technical feasibility assessment |
| 2 | Below acceptable — some feasibility notes but no systematic analysis, risks not identified |
| 3 | Acceptable — requirements are implementable, key risks identified, resource and timeline estimates reasonable |
| 4 | Strong — detailed feasibility analysis with risk mitigations, phased implementation plan, technology constraints documented |
| 5 | Excellent — proven feasibility with comparable case studies, detailed risk register with quantified impact, contingency plans, and stakeholder agreement on trade-offs |

---

## Section 6: Sprint Contract Checklist Templates

Pre-built checklists for 5 BA phases. The generator includes the relevant checklist(s) in each sprint contract. The evaluator uses them as acceptance criteria.

### For Requirements Elicitation

- [ ] Stakeholder register identifies all key stakeholders with roles and influence
- [ ] Elicitation techniques selected and justified (interviews, workshops, surveys, observation)
- [ ] Business context documented (current state, pain points, opportunities)
- [ ] Scope defined with explicit in-scope, out-of-scope, assumptions, and constraints
- [ ] Initial requirement categories identified (functional, non-functional, business rules)

### For Use Case Development

- [ ] All primary actors identified with descriptions
- [ ] Use cases follow standard template (preconditions, main flow, alternate flows, postconditions)
- [ ] Each use case has a unique ID (UC-xxx) and traced to parent requirement
- [ ] Exception and error flows documented for critical use cases
- [ ] Use case diagram shows actor-use case relationships

### For Process Modeling

- [ ] Current-state ("as-is") processes documented in BPMN notation
- [ ] Future-state ("to-be") processes designed with improvement rationale
- [ ] Process participants (lanes/pools) mapped to organizational roles
- [ ] Decision points (gateways) have documented business rules
- [ ] Process metrics identified (cycle time, throughput, error rate)

### For Gap Analysis

- [ ] Current state documented with evidence (metrics, pain points, stakeholder input)
- [ ] Target state defined with measurable success criteria
- [ ] Gaps identified and categorized (process, technology, people, data)
- [ ] Gap closure actions prioritized by business impact and feasibility
- [ ] Dependencies between gap closure actions identified

### For Stakeholder Review

- [ ] Review package assembled with executive summary
- [ ] Requirements prioritized using agreed method (MoSCoW, weighted scoring, Kano)
- [ ] Open issues list with owners and resolution timeline
- [ ] Sign-off criteria defined and communicated
- [ ] Feedback incorporation plan documented

---

## Section 7: Reference Materials

### Industry Standards

| Standard | Scope | Key Concepts |
|----------|-------|-------------|
| BABOK v3 (IIBA) | BA knowledge areas, techniques, competencies | 6 knowledge areas, 50+ techniques, underlying competencies |
| PMI-PBA | Business analysis in project context | Needs assessment, planning, analysis, traceability, evaluation |
| ISO/IEC 29148 | Requirements engineering standard | Requirements processes, documentation templates, quality attributes |
| IEEE 830 | Software requirements specification | SRS template, requirement characteristics (correct, unambiguous, complete, consistent) |
| TOGAF Business Architecture | Business architecture within EA context | Business capability modeling, value streams, organization mapping |

### Common Frameworks

| Framework | When to Use | Key Deliverables |
|-----------|-------------|-----------------|
| Business Model Canvas | Strategy and innovation projects | 9-block canvas covering value proposition, segments, channels |
| Value Stream Mapping | Process improvement, Lean initiatives | Current and future state value stream maps |
| RACI Matrix | Role clarity and governance | Responsibility assignment for processes and decisions |
| Kano Model | Feature prioritization, product management | Feature classification (must-be, one-dimensional, attractive, indifferent) |
| Jobs-to-be-Done | Customer-centric analysis | Job statements, outcome expectations, underserved needs |

---

## Section 8: Notation Guide

### BPMN Basics

| Element | Symbol | Usage |
|---------|--------|-------|
| Start Event | Circle (thin border) | Beginning of a process flow |
| End Event | Circle (thick border) | Termination of a process flow |
| Task | Rounded rectangle | A unit of work performed by a participant |
| Gateway (Exclusive) | Diamond with X | Decision point — one path selected |
| Gateway (Parallel) | Diamond with + | Fork/join — all paths executed |
| Gateway (Inclusive) | Diamond with O | One or more paths selected |
| Sequence Flow | Solid arrow | Order of activities |
| Message Flow | Dashed arrow | Communication between pools |
| Pool/Lane | Horizontal container | Organization/role boundary |
| Data Object | Document icon | Data input/output for activities |

### Use Case Diagram Conventions

| Element | Representation | Usage |
|---------|---------------|-------|
| Actor | Stick figure | External entity interacting with the system |
| Use Case | Oval/ellipse | A goal the actor achieves using the system |
| System Boundary | Rectangle | Scope of the system under analysis |
| Include | Dashed arrow with <<include>> | Mandatory sub-behavior |
| Extend | Dashed arrow with <<extend>> | Optional/conditional behavior |
| Generalization | Solid arrow with open arrowhead | Actor or use case inheritance |

### Data Flow Notation

| Element | Symbol | Usage |
|---------|--------|-------|
| Process | Circle or rounded rectangle | Transforms data inputs into outputs |
| Data Store | Open-ended rectangle (parallel lines) | Persistent data repository |
| External Entity | Rectangle | Source or destination outside system boundary |
| Data Flow | Arrow with label | Movement of data between elements |

---

## Section 9: Business Analysis Repository Structure

The generator should organize BA deliverables following this repository structure:

```
.harness/
  spec.md                              # BA Statement of Work
  features.json                        # BA deliverable tracker

project-root/
  business-analysis/
    1-elicitation/
      stakeholder-register.md          # Stakeholder identification and analysis
      elicitation-plan.md              # Techniques, schedule, participants
      interview-notes/                 # Raw interview/workshop outputs
      business-context.md              # Current state, pain points, opportunities
    2-requirements/
      brd.md                           # Business Requirements Document
      functional-requirements.md       # Detailed functional requirements (REQ-xxx)
      non-functional-requirements.md   # Performance, security, usability requirements
      business-rules.md                # Business rules catalog
    3-use-cases/
      use-case-model.md                # Use case diagram and overview
      UC-001-*.md                      # Individual use case specifications
      UC-002-*.md
    4-process-models/
      current-state/                   # As-is BPMN process models
      future-state/                    # To-be BPMN process models
      gap-analysis.md                  # Process gaps and improvements
    5-data/
      conceptual-data-model.md         # Entity-relationship overview
      data-dictionary.md               # Field-level data definitions
      data-quality-rules.md            # Validation and quality constraints
    6-validation/
      traceability-matrix.md           # Requirements traceability (needs -> requirements -> use cases -> tests)
      acceptance-criteria.md           # Measurable acceptance criteria
      sign-off-tracker.md             # Stakeholder sign-off status
    glossary.md                        # Consistent term definitions
    diagrams/
      *.bpmn                           # BPMN source files
      *.mermaid                        # Mermaid source files
```

### Repository Completeness Check (Evaluator)

The evaluator verifies repository structure completeness per phase:

| After Phase | Required Directories | Required Files (minimum) |
|-------------|---------------------|-------------------------|
| Elicitation | `1-elicitation/` | stakeholder-register.md, business-context.md |
| Requirements | `2-requirements/` | brd.md, functional-requirements.md |
| Use Cases | `3-use-cases/` | use-case-model.md, at least 1 UC spec |
| Process Modeling | `4-process-models/` | at least 1 current-state model, gap-analysis.md |
| Data Analysis | `5-data/` | conceptual-data-model.md, data-dictionary.md |
| Validation | `6-validation/` | traceability-matrix.md, acceptance-criteria.md |
| Any | root | glossary.md |

---

## Section 10: Business Analysis Anti-Patterns (Evaluator Watch List)

The evaluator should flag these common BA anti-patterns when grading:

| Anti-Pattern | What It Looks Like | Impact | Score Penalty |
|-------------|-------------------|--------|---------------|
| **Requirements Amnesia** | Requirements gathered but not documented or traced | traceability: -2 | Drop traceability to max 2 |
| **Stakeholder Blindspot** | Key stakeholders missing from analysis, only IT consulted | stakeholder_alignment: -2 | Drop stakeholder_alignment to max 2 |
| **Gold Plating** | Excessive detail on low-priority requirements while critical ones are vague | completeness: -1 | Flag as scope risk |
| **Solution Jumping** | Requirements describe a specific solution instead of business needs | feasibility: -1 | Require needs-based rewrite |
| **Scope Creep Enablement** | No explicit out-of-scope list, assumptions undocumented | completeness: -1 | Require scope boundary definition |
| **Ambiguity Tolerance** | Requirements use vague language ("should", "may", "appropriate", "etc.") | completeness: -2 | Cannot verify without measurable criteria |
| **Traceability Theater** | Traceability matrix exists but links are incorrect or incomplete | traceability: -1 | Require matrix validation |
| **Analysis Paralysis** | Attempting exhaustive analysis of every edge case before any validation | feasibility: -1 | Flag as delivery risk |
| **Security Requirements Omission** | BRD has zero security or privacy requirements despite handling user data | completeness: -2 | Drop completeness to max 2 |

---

## Section 11: Elicitation Interview Template

Stakeholder interviews are a core elicitation technique for business analysis. This section provides a structured interview guide that the generator uses when producing elicitation artifacts, and the evaluator uses to verify interview documentation quality.

### Pre-Interview Preparation Checklist

Complete before every stakeholder interview:

- [ ] **Identify the stakeholder**: Name, role, department, influence level (from stakeholder register)
- [ ] **Define the interview objective**: What specific information do you need from this stakeholder?
- [ ] **Review existing materials**: Read relevant documents, prior interview notes, and process documentation related to this stakeholder's domain
- [ ] **Prepare question set**: Select and customize questions from the categories below; tailor to the stakeholder's role and knowledge area
- [ ] **Schedule logistics**: Confirm date, time, duration (30-60 minutes recommended), location or virtual platform
- [ ] **Send pre-read materials**: Provide context document or agenda at least 2 business days before the interview
- [ ] **Prepare recording method**: Confirm note-taking approach (scribe, recording with consent, or self-notes)

### Question Categories

Organize interview questions into these categories. Select 2-4 questions per category based on the interview objective.

**Context Questions** (establish the stakeholder's perspective):
- What is your role in the current process and how long have you been involved?
- Can you walk me through a typical day/week in terms of this business area?
- What systems, tools, or data sources do you use regularly?
- Who else should I speak with to understand this area completely?

**Pain Point Questions** (identify problems and frustrations):
- What are the biggest challenges you face in the current process?
- Where do bottlenecks or delays most frequently occur?
- What manual or duplicate work do you find yourself doing regularly?
- What information do you need but cannot easily access today?
- When things go wrong, what is the typical impact (time, cost, quality)?

**Goal Questions** (understand desired outcomes):
- If you could change one thing about the current process, what would it be?
- What does success look like for this initiative from your perspective?
- What capabilities or features would make the biggest difference to your work?
- How would you measure whether the new solution is working well?

**Constraint Questions** (identify boundaries and limitations):
- Are there regulatory, compliance, or policy requirements that must be met?
- What budget, timeline, or resource constraints should we be aware of?
- Are there existing systems or contracts that cannot be changed?
- What organizational or political factors could affect this initiative?

**Security & Privacy Questions** (identify protection needs):
- What data is sensitive or personally identifiable?
- What regulations or compliance requirements apply (GDPR, HIPAA, PCI-DSS)?
- Who should NOT have access to this data or functionality?
- What happens if data is breached or unauthorized access occurs?

**Success Criteria Questions** (define measurable acceptance):
- How will you know the requirements have been implemented correctly?
- What metrics or KPIs would indicate the solution is delivering value?
- What would cause you to reject or escalate a proposed solution?
- What is the minimum viable outcome that would be acceptable?

### Interview Documentation Format

```markdown
# Interview Record: [Stakeholder Name]

## Metadata
- **Stakeholder**: [Name], [Role], [Department]
- **Interviewer**: [Name]
- **Date**: [YYYY-MM-DD]
- **Duration**: [Actual duration]
- **Interview Objective**: [What information was sought]

## Key Findings

### Context
- [Summary of stakeholder's perspective and domain knowledge]

### Pain Points Identified
| ID | Pain Point | Severity (H/M/L) | Frequency | Affected Process |
|----|-----------|-------------------|-----------|-----------------|
| PP-01 | [Description] | [H/M/L] | [Daily/Weekly/Monthly] | [Process name] |

### Goals and Desired Outcomes
| ID | Goal | Priority (H/M/L) | Measurable Outcome |
|----|------|-------------------|-------------------|
| GL-01 | [Description] | [H/M/L] | [How to measure] |

### Constraints Identified
- [Constraint 1: description and impact]
- [Constraint 2: description and impact]

### Requirements Candidates
| Candidate ID | Description | Type (Functional/Non-Functional/Rule) | Source (this interview) |
|-------------|------------|---------------------------------------|------------------------|
| RC-01 | [Description] | [Type] | [Stakeholder name, date] |

## Follow-Up Actions
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action item] | [Name] | [Date] |

## Interviewer Notes
[Observations about stakeholder engagement, concerns not explicitly stated, potential conflicts with other stakeholder views]
```

---

## Section 12: Prioritization Templates

Prioritization is critical for managing stakeholder expectations and allocating development effort. This section provides three complementary techniques. Select based on project context, or use multiple techniques for cross-validation.

### MoSCoW Matrix

MoSCoW classifies requirements into four categories based on delivery necessity within the current time-box.

| Category | Definition | Decision Criteria | Typical Allocation |
|----------|-----------|-------------------|-------------------|
| **Must have** | Non-negotiable for this release; without it the solution has no value or fails compliance | Legal/regulatory requirement, core business process dependency, safety-critical | 60% of effort |
| **Should have** | Important but workaround exists; painful to omit but solution is still viable | Significant business value, high stakeholder demand, but deferral does not break core functionality | 20% of effort |
| **Could have** | Desirable; included if time and budget permit after Must and Should items are delivered | Nice-to-have improvements, efficiency gains, user experience enhancements | 15% of effort |
| **Won't have (this time)** | Explicitly excluded from this release; acknowledged for future consideration | Low priority, high cost relative to value, dependent on deferred capability, or stakeholder agreed to defer | 5% of effort (planning only) |

**MoSCoW Classification Template:**

| Req ID | Requirement | MoSCoW | Rationale | Stakeholder Agreement |
|--------|------------|--------|-----------|----------------------|
| REQ-001 | [Description] | Must | [Why this classification] | [Stakeholder name, date] |
| REQ-002 | [Description] | Should | [Why this classification] | [Stakeholder name, date] |
| REQ-003 | [Description] | Could | [Why this classification] | [Stakeholder name, date] |
| REQ-004 | [Description] | Won't | [Why this classification] | [Stakeholder name, date] |

### Kano Model Classification

The Kano model classifies features based on their relationship between implementation and customer satisfaction.

| Category | Customer Expectation | If Present | If Absent | Example |
|----------|---------------------|-----------|-----------|---------|
| **Must-be (Basic)** | Taken for granted; expected as baseline | No increase in satisfaction | Strong dissatisfaction | Login functionality, data validation, error messages |
| **One-dimensional (Performance)** | Explicitly requested; satisfaction proportional to fulfillment | Satisfaction increases proportionally | Dissatisfaction proportional to gap | Response time, report detail level, search accuracy |
| **Attractive (Delighter)** | Not expected; pleasantly surprised | Disproportionate satisfaction increase | No dissatisfaction (not missed) | Predictive suggestions, auto-generated reports, smart defaults |
| **Indifferent** | No impact on satisfaction either way | No effect | No effect | Internal logging format, backend implementation details |
| **Reverse** | Actively unwanted by some users | Dissatisfaction for some users | Satisfaction for those who dislike it | Mandatory tutorials, forced update prompts |

**Kano Classification Template:**

| Feature ID | Feature | Functional Question Response | Dysfunctional Question Response | Classification | Confidence |
|-----------|---------|-----------------------------|---------------------------------|---------------|------------|
| F-001 | [Description] | [Like/Expect/Neutral/Tolerate/Dislike] | [Like/Expect/Neutral/Tolerate/Dislike] | [Must-be/One-dimensional/Attractive/Indifferent/Reverse] | [High/Medium/Low] |

To classify: ask stakeholders two questions per feature: (1) "How would you feel if this feature is present?" (functional) and (2) "How would you feel if this feature is absent?" (dysfunctional). Map the response pair to the Kano category using the evaluation matrix:

| | Like (functional) | Expect | Neutral | Tolerate | Dislike |
|---|---|---|---|---|---|
| **Like (dysfunctional)** | Questionable | Attractive | Attractive | Attractive | One-dimensional |
| **Expect** | Reverse | Indifferent | Indifferent | Indifferent | Must-be |
| **Neutral** | Reverse | Indifferent | Indifferent | Indifferent | Must-be |
| **Tolerate** | Reverse | Indifferent | Indifferent | Indifferent | Must-be |
| **Dislike** | Reverse | Reverse | Reverse | Reverse | Questionable |

### Weighted Scoring Model

Weighted scoring provides a quantitative comparison when stakeholder priorities conflict or when MoSCoW is too coarse.

**Step 1: Define Criteria and Weights**

| Criterion | Description | Weight (%) |
|-----------|-----------|-----------|
| Business Value | Revenue impact, cost reduction, strategic alignment | [e.g., 30%] |
| User Impact | Number of users affected, frequency of use, pain severity | [e.g., 25%] |
| Implementation Effort | Development time, complexity, dependencies | [e.g., 20%] |
| Risk Reduction | Compliance, security, operational risk mitigation | [e.g., 15%] |
| Strategic Alignment | Alignment with organizational goals and roadmap | [e.g., 10%] |
| **Total** | | **100%** |

Weights are agreed upon by stakeholders before scoring begins. Adjust criteria to match project context.

**Step 2: Score Requirements**

| Req ID | Requirement | Business Value (1-5) | User Impact (1-5) | Effort (1-5, inverted) | Risk Reduction (1-5) | Strategic (1-5) | Weighted Score | Rank |
|--------|------------|---------------------|-------------------|----------------------|---------------------|----------------|---------------|------|
| REQ-001 | [Description] | [Score] | [Score] | [Score] | [Score] | [Score] | [Calculated] | [#] |

**Weighted Score Formula:** `Score = SUM(criterion_score * criterion_weight)`

Note: For the Effort criterion, invert the scale (5 = low effort, 1 = high effort) so that higher scores consistently mean "more desirable."

---

## Section 13: Requirements Sign-Off Workflow

This section defines the approval lifecycle for BA deliverables, the stakeholder sign-off process, and the change control procedure for post-baseline modifications.

### Approval Stages

| Stage | Status | Description | Entry Criteria | Exit Criteria | Responsible |
|-------|--------|------------|---------------|---------------|-------------|
| 1 | **Draft** | Initial authoring; requirements being elicited and documented | Sprint contract accepted | All mandatory BRD sections populated; internal consistency check passed | Business Analyst |
| 2 | **Internal Review** | Peer review by BA team and technical leads | Draft complete, no known gaps | All review comments resolved or deferred with rationale | BA Lead, Technical Lead |
| 3 | **Stakeholder Review** | Business stakeholders review for accuracy and completeness | Internal review passed | All stakeholder comments addressed; no open blockers | Business Owners, SMEs |
| 4 | **Approved** | Formally accepted by designated approvers | Stakeholder review passed; sign-off criteria met | All required signatures obtained | Executive Sponsor, Business Owner |
| 5 | **Baselined** | Version-locked; changes require formal change control | Approved status reached; version number assigned | Baseline published to repository; change control activated | Configuration Manager or BA Lead |

### Stakeholder Sign-Off Format

```markdown
# Requirements Sign-Off Record

## Document
- **Title**: [BRD / Requirements Specification title]
- **Version**: [Version number]
- **Baseline Date**: [YYYY-MM-DD]

## Scope of Sign-Off
[Brief description of what is being approved -- e.g., "Functional requirements for Phase 1 of the Order Management System"]

## Sign-Off Register

| Name | Role | Department | Decision | Comments | Date |
|------|------|-----------|----------|----------|------|
| [Name] | Executive Sponsor | [Dept] | Approved / Approved with conditions / Rejected | [Comments or conditions] | [Date] |
| [Name] | Business Owner | [Dept] | Approved / Approved with conditions / Rejected | [Comments or conditions] | [Date] |
| [Name] | Technical Lead | [Dept] | Approved / Approved with conditions / Rejected | [Comments or conditions] | [Date] |

## Conditions (if any)
| Condition ID | Description | Resolution Owner | Resolution Date |
|-------------|------------|-----------------|----------------|
| COND-01 | [Description of condition] | [Name] | [Target date] |

## Result
- **Overall Decision**: [Approved | Approved with Conditions | Rejected]
- **Next Step**: [Baseline and activate change control | Revise and re-submit | Escalate to steering committee]
```

### Change Control Process

Once requirements are baselined, all modifications must follow this change control procedure:

**Step 1: Change Request**

| Field | Description |
|-------|-----------|
| **CR ID** | Unique identifier (CR-NNN) |
| **Requestor** | Name and role of the person requesting the change |
| **Date Submitted** | Date the change request was raised |
| **Affected Requirements** | List of Requirement IDs impacted (REQ-NNN) |
| **Description** | Clear description of the proposed change |
| **Business Justification** | Why this change is needed; what happens if it is not made |
| **Priority** | Critical / High / Medium / Low |

**Step 2: Impact Assessment**

| Assessment Area | Analysis |
|----------------|---------|
| **Scope Impact** | Which requirements, use cases, and processes are affected? |
| **Effort Impact** | Estimated additional effort (hours/days) for implementation |
| **Schedule Impact** | Effect on delivery timeline -- slip, compression, or no impact |
| **Cost Impact** | Additional cost or budget reallocation required |
| **Risk Impact** | New risks introduced or existing risks changed |
| **Dependency Impact** | Other requirements or features affected by this change |

**Step 3: Approval Authority**

| Change Priority | Approval Authority | Turnaround Target |
|----------------|-------------------|-------------------|
| Critical | Executive Sponsor + Business Owner | 1 business day |
| High | Business Owner + BA Lead | 3 business days |
| Medium | BA Lead + Technical Lead | 5 business days |
| Low | BA Lead (sole authority) | 10 business days |

**Step 4: Implementation**

After approval: update affected requirements, increment version number, update traceability matrix, notify affected stakeholders, and update the baseline. Record the CR resolution in the change log.

---

## Section 14: Traceability Matrix Template

The traceability matrix links business needs to requirements, features, test cases, and acceptance criteria. It serves as the primary tool for verifying requirements completeness and impact analysis.

### Matrix Template

| Requirement ID | Requirement Title | Business Need / Source | Feature / Capability ID | Test Case ID | Acceptance Criteria | Status | Priority | Owner |
|---------------|------------------|----------------------|------------------------|-------------|-------------------|--------|----------|-------|
| REQ-001 | [Short title] | [BN-001 or stakeholder interview reference] | [F-001 or CAP-001] | [TC-001, TC-002] | [Measurable criterion] | [Draft / Reviewed / Approved / Implemented / Verified] | [Must / Should / Could] | [Name] |
| REQ-002 | [Short title] | [BN-002] | [F-001, F-003] | [TC-003] | [Measurable criterion] | [Draft] | [Must] | [Name] |

### Status Definitions

| Status | Meaning |
|--------|---------|
| **Draft** | Requirement documented but not yet reviewed |
| **Reviewed** | Requirement reviewed by BA team; no outstanding issues |
| **Approved** | Requirement approved by stakeholder sign-off |
| **Implemented** | Requirement implemented in the solution (for software) or addressed in the deliverable (for documents) |
| **Verified** | Requirement verified through test execution or deliverable review |
| **Deferred** | Requirement moved to a future release or phase |
| **Rejected** | Requirement rejected during review; rationale documented |

### Usage Instructions

1. **Create early**: Start the matrix during elicitation. Add Requirement ID and Business Need columns first.
2. **Maintain continuously**: Update the matrix every sprint. Add Feature, Test, and Acceptance columns as those artifacts are produced.
3. **Review at phase gates**: Use the matrix as the primary review artifact at each approval stage (Section 13).
4. **Bidirectional trace**: Every requirement should trace forward (to features, tests, acceptance) and backward (to business needs and stakeholders).

### Completeness Validation Rules

Run these checks to validate matrix completeness:

| Check | Rule | Severity |
|-------|------|----------|
| **No orphan requirements** | Every REQ-NNN must have at least one Business Need reference | Blocker |
| **No untested requirements** | Every Approved or Implemented REQ-NNN must have at least one Test Case ID | Blocker |
| **No unlinked features** | Every Feature/Capability ID must trace to at least one REQ-NNN | Warning |
| **No missing acceptance criteria** | Every REQ-NNN with Status = Approved or later must have an Acceptance Criteria entry | Blocker |
| **No stale statuses** | Requirements with Status = Draft should not persist beyond 2 sprint rounds after creation | Warning |
| **Priority consistency** | Must-have requirements should not have Status = Deferred unless a change request (CR-NNN) justifies it | Blocker |

### Gap Analysis Procedure

Use the traceability matrix to identify gaps:

1. **Forward gap (requirement without implementation)**: Filter for requirements where Feature/Capability ID is empty. These are documented needs that have not been mapped to any solution component.
2. **Backward gap (feature without requirement)**: Filter for features that appear in features.json but have no corresponding row in the traceability matrix. These are solution components without a documented business justification.
3. **Test gap (requirement without test)**: Filter for requirements with Status = Approved or later where Test Case ID is empty. These are accepted requirements that cannot be verified.
4. **Acceptance gap (requirement without criteria)**: Filter for requirements where Acceptance Criteria is empty. These requirements cannot be objectively evaluated.

Report gaps in the evaluation as non-blocking issues (unless the gap affects a Must-have requirement, in which case it is a blocker).
