---
name: harness-ea
description: "Enterprise Architecture domain skill for the harness plugin. Provides architecture methodology selection (TOGAF 10, Zachman, FEAF, ArchiMate 3.2, SAFe, Lean EA), development methodology (ADR-First, Capability-First, Viewpoint-Driven, Gap Analysis, Reference Architecture), verification strategy, deliverable verification, evaluation criteria, and industry-specific reference architectures. Activated when domain_profile is "enterprise_architecture"."
---

# Enterprise Architecture Domain Skill

> **Domain-specific.** This skill provides the HOW for enterprise architecture projects. The harness provides the WHEN (orchestration, sprint contracts, feature ledger). This skill provides the HOW (framework selection, development methodology, deliverable verification, evaluation criteria anchors, and industry-specific patterns).

Activated when `domain_profile: enterprise_architecture` is declared in `.harness/spec.md`.

## Scope of This Skill

This skill covers the full Enterprise Architecture lifecycle:
- **Strategy**: Business strategy → architecture vision → capability roadmap
- **Design**: Current state → target state → gap analysis → transition planning
- **Governance**: Principles, standards, compliance, change management
- **Communication**: Stakeholder viewpoints, decision records, architecture repository

It is framework-agnostic at its core — any of the supported methodologies can be selected. The TOGAF ADM is the default because it provides the most structured phase model for harness sprint mapping.


## Activation Check

This skill activates when `domain_profile: enterprise_architecture` is set in `.harness/spec.md` or `.harness/state.json`.

Before using this skill's procedures:
1. Verify the project produces architecture deliverables (documents, diagrams, decision records -- not primarily code)
2. Read spec.md -> identify the selected framework (TOGAF, Zachman, FEAF, etc.)
3. If no framework specified -> default to TOGAF ADM
4. Check if `architecture/` directory exists -> if yes, verify against the Repository Structure (Section 9)
5. Identify the industry -> select the appropriate reference architecture from Section 7
---

## Section 1: Architecture Methodology

Select based on project characteristics during `/harness:start`:

| Framework | When to Use | Phase Structure | Harness Mapping |
|-----------|-------------|-----------------|-----------------|
| TOGAF ADM | Enterprise transformation, IT strategy | Preliminary, Vision, Business, IS, Technology, Opportunities, Migration, Governance | 1 sprint = 1 ADM phase |
| Zachman | Classification/taxonomy, documentation | 6x6 matrix (What/How/Where/Who/When/Why x Scope/Business/System/Technology/Detail/Functioning) | 1 sprint = 1 column or viewpoint |
| FEAF (Federal) | Government/public sector | Performance, Business, Data, Application, Infrastructure | 1 sprint = 1 reference model |
| ArchiMate Modeling | Visualization, stakeholder communication | Business, Application, Technology layers + Strategy/Motivation extensions | 1 sprint = 1 layer or viewpoint |
| SAFe Architecture | Agile + EA blend, large organizations | Architectural Runway + Enablers + Solution Intent | 1 sprint = 1 runway enabler |
| Lean EA | Startup/scale-up, minimal governance | Just-enough architecture, decision records, fitness functions | 1 sprint = 1 decision + validation |

**Default:** TOGAF ADM (if not specified by user).

The planner writes the selected framework into `spec.md` during initialization. The coordinator uses the mapping to structure sprint boundaries accordingly.

---

## Section 2: Architecture Development Methodology

Select based on project type and stakeholder needs:

| Methodology | When to Use | How It Drives the Generator |
|-------------|-------------|----------------------------|
| ADR-First (Architecture Decision Records) | Every project | Generator documents decisions FIRST (context, options, rationale), then builds artifacts around decisions |
| Capability-First | Business transformation | Generator maps business capabilities FIRST, then derives technology components |
| Viewpoint-Driven | Stakeholder-heavy projects | Generator identifies stakeholder concerns FIRST, then creates viewpoints addressing each concern |
| Gap Analysis | Migration/modernization | Generator documents current state FIRST, defines target state, then identifies gaps |
| Reference Architecture | Standards-based | Generator selects reference models FIRST (BIAN for banking, HL7 for healthcare, etc.), then customizes |

**Default:** ADR-First for all architecture projects (if not specified).

### How Methodology Drives the Harness

The chosen methodology affects every phase:

1. **Generator behavior**: What to produce first (decisions? capability maps? viewpoints?)
2. **Evaluator criteria**: What to prioritize (decision rationale quality? capability coverage? viewpoint completeness?)
3. **Sprint contract**: What acceptance criteria to define (ADR completeness? stakeholder coverage? gap identification?)
4. **Artifact types**: What deliverables per sprint (ADRs? capability models? architecture diagrams?)

### Generator First-Action Table

| Methodology | Generator produces first | Then |
|-------------|------------------------|------|
| ADR-First | Decision records with context, options, rationale | Architecture artifacts justified by decisions |
| Capability-First | Business capability map (L0-L2) | Application and technology components mapped to capabilities |
| Viewpoint-Driven | Stakeholder concern register | Viewpoints addressing each concern with appropriate notation |
| Gap Analysis | Current state architecture documentation | Target state definition and gap identification |
| Reference Architecture | Reference model selection and justification | Customized architecture based on selected models |

---

## Section 3: Verification Strategy (Architecture Equivalent of Testing)

| Verification Type | Architecture Equivalent | Method |
|-------------------|----------------------|--------|
| Unit test | ADR validation | Each decision has context, options considered, rationale, consequences |
| Integration test | Viewpoint consistency | Cross-viewpoint references resolve correctly (business capability, application component, technology node) |
| E2E test | Scenario walkthrough | Business scenario traces through all architecture layers without gaps |
| Smoke test | Artifact completeness | Required deliverables exist and are non-empty |
| Regression | Standards compliance | ArchiMate notation correct, TOGAF phases complete, naming conventions followed |

### Artifact Completeness Checks

- Does the Architecture Vision document exist?
- Are all stakeholder concerns mapped to viewpoints?
- Does each capability have at least one supporting application?
- Are all gaps between current and target state identified?
- Do ADRs exist for all significant decisions?

---

## Section 4: Deliverable Verification (Equivalent of Build/Runtime)

Since EA produces documents, not running software, "build verification" means:

| Check | What to Verify | How |
|-------|---------------|-----|
| Document structure | Required sections present | Check headings/sections against template |
| Cross-references | References between documents resolve | Grep for referenced IDs, verify targets exist |
| Diagram notation | ArchiMate/UML notation correct | Mermaid/PlantUML renders without errors |
| Naming conventions | Consistent naming across artifacts | Pattern matching on entity names |
| Traceability | Requirements to Capabilities to Components | Traceability matrix completeness check |
| Stakeholder coverage | All identified stakeholders have viewpoints | Cross-reference stakeholder register with viewpoint list |

### TOGAF Phase Gate Checks

| Phase | Required Deliverables |
|-------|----------------------|
| Preliminary | Architecture Principles, Governance Framework, Tailored ADM |
| A: Vision | Architecture Vision, Stakeholder Map, Value Chain |
| B: Business | Business Architecture, Capability Map, Process Models |
| C: Information Systems | Application Architecture, Data Architecture, Integration Map |
| D: Technology | Technology Architecture, Platform Blueprint, Standards Profile |
| E: Opportunities | Gap Analysis, Migration Factors, Consolidation Roadmap |
| F: Migration | Implementation Roadmap, Work Packages, Transition Architectures |
| G: Governance | Architecture Compliance, Change Requests, Dispensations |
| H: Change Management | Architecture Change Impact, Assessment Criteria |

---

## Section 5: Evaluation Criteria (Architecture Profile)

The 4 primary criteria for the `enterprise_architecture` domain profile. The evaluator MUST use these anchors for consistent scoring across sprints.

### coherence (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent -- no logical structure |
| 1 | Severely incomplete -- artifacts exist but no organizing principle |
| 2 | Below acceptable -- artifacts exist but disconnected, no cross-references |
| 3 | Acceptable -- consistent layer model, viewpoints aligned |
| 4 | Strong -- cross-viewpoint traceability, gap-free decomposition |
| 5 | Excellent -- elegant decomposition, principles consistently applied throughout |

### standards_compliance (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent -- no framework used |
| 1 | Severely incomplete -- framework mentioned but not followed |
| 2 | Below acceptable -- partial framework usage, inconsistent notation |
| 3 | Acceptable -- correct ArchiMate/TOGAF notation and phases, security zones and trust boundaries documented |
| 4 | Strong -- full compliance with selected framework |
| 5 | Excellent -- tailored framework with documented rationale for deviations |

### stakeholder_coverage (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent -- no stakeholder analysis |
| 1 | Severely incomplete -- some stakeholders identified, no viewpoints |
| 2 | Below acceptable -- stakeholders listed but not mapped to viewpoints |
| 3 | Acceptable -- all key stakeholders mapped to viewpoints |
| 4 | Strong -- concern-driven viewpoints with explicit traceability |
| 5 | Excellent -- stakeholder feedback incorporated, viewpoints validated |

### feasibility (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent -- fantasy architecture, no implementation path |
| 1 | Severely incomplete -- technically possible but no resource plan |
| 2 | Below acceptable -- technically possible but impractical |
| 3 | Acceptable -- achievable with identified resources and timeline |
| 4 | Strong -- risk-mitigated with transition architecture |
| 5 | Excellent -- proven patterns, pilot evidence, vendor validation |

---

## Section 6: Sprint Contract Checklist Templates

Pre-built checklists for 5 TOGAF phases. The generator includes the relevant checklist(s) in each sprint contract. The evaluator uses them as acceptance criteria.

### For Architecture Vision (TOGAF Phase A)

- [ ] Stakeholder map identifies all key stakeholders
- [ ] Business drivers and constraints documented
- [ ] High-level capability map created
- [ ] Architecture principles defined (at least 5)
- [ ] Value proposition articulated for the transformation

### For Business Architecture (TOGAF Phase B)

- [ ] Business capability model complete (L0-L2)
- [ ] Key business processes mapped
- [ ] Organization mapping to capabilities
- [ ] Business service catalog drafted
- [ ] Gap analysis against target capabilities
- [ ] Data classification for key entities (public/internal/confidential/regulated)

### For Information Systems Architecture (TOGAF Phase C)

- [ ] Application portfolio mapped to capabilities
- [ ] Data entities identified and classified
- [ ] Integration patterns documented
- [ ] Application rationalization candidates identified
- [ ] Data flow diagrams for key scenarios

### For Technology Architecture (TOGAF Phase D)

- [ ] Technology standards profile defined
- [ ] Platform blueprint with selected products/services
- [ ] Infrastructure requirements mapped to applications
- [ ] Security architecture requirements documented
- [ ] Security zoning diagram with trust boundaries
- [ ] Identity provider and authentication pattern selected
- [ ] Cloud vs on-premises decision rationale

### For Migration Planning (TOGAF Phase E-F)

- [ ] Gap analysis complete (current to target)
- [ ] Work packages defined with dependencies
- [ ] Transition architectures for major milestones
- [ ] Implementation roadmap with timeline
- [ ] Risk register with mitigations

### For Governance (TOGAF Phase G-H)

- [ ] Architecture compliance review criteria defined
- [ ] Dispensation process documented
- [ ] Change management triggers identified
- [ ] Architecture board composition and cadence defined
- [ ] KPIs for architecture effectiveness established

---

## Section 7: Industry Reference Architectures

When the project targets a specific industry, the generator should select and tailor the appropriate reference architecture:

| Industry | Reference Architecture | Key Standards | Typical Artifacts |
|----------|----------------------|---------------|-------------------|
| Banking/Finance | BIAN (Banking Industry Architecture Network) | PSD2, ISO 20022, Basel III | Service domains, business capabilities, API catalog |
| Healthcare | HL7 FHIR, IHE Profiles | HIPAA, GDPR, HL7v2 | Clinical workflows, data exchange patterns, consent model |
| Government | FEAF, GovStack, NIST | FedRAMP, FISMA, WCAG | Citizen services, shared services, security framework |
| Telecom | TM Forum (eTOM, SID, TAM) | 3GPP, MEF | Service catalog, order management, network architecture |
| Manufacturing | ISA-95, RAMI 4.0 | IEC 62443, OPC UA | Plant hierarchy, MES integration, digital twin |
| Insurance | ACORD, LOMA | Solvency II, IFRS 17 | Policy lifecycle, claims processing, actuarial models |
| Retail | ARTS (Association for Retail Tech Standards) | PCI DSS, GDPR | Omnichannel, POS integration, supply chain |
| Energy/Utilities | CIM (Common Information Model), SGAM | NERC CIP, IEC 61968/61970 | Grid architecture, SCADA integration, meter data management |

### How to Use Reference Architectures

1. **Generator**: Identify the industry → select the reference architecture → use as the starting blueprint
2. **Evaluator**: Check the output against the reference architecture's standard patterns and terminology
3. **Contract**: Include reference architecture alignment as a required contract check

If no industry-specific reference exists, use generic patterns from TOGAF's Architecture Building Blocks (ABBs) and Solution Building Blocks (SBBs).

---

## Section 8: ArchiMate Modeling Guide

When the project uses ArchiMate notation, the generator and evaluator should follow these modeling conventions:

### Layer Structure

| Layer | Elements | Relationships | Color Convention |
|-------|----------|--------------|-----------------|
| Strategy | Resource, Capability, Course of Action, Value Stream | Realization, Association | Purple/Lavender |
| Business | Actor, Role, Process, Function, Service, Event, Object | Composition, Aggregation, Assignment, Triggering, Flow, Serving, Access | Yellow |
| Application | Component, Collaboration, Interface, Function, Service, Event, Data Object | Same as Business | Blue |
| Technology | Node, Device, System Software, Artifact, Communication Network, Path | Same + Deployment | Green |
| Motivation | Stakeholder, Driver, Assessment, Goal, Outcome, Principle, Requirement, Constraint | Influence, Realization, Association | Pink/Rose |
| Implementation | Work Package, Deliverable, Plateau, Gap | Realization, Triggering | Coral |

### Viewpoint Selection Guide

| Stakeholder Concern | Recommended Viewpoint | Key Elements |
|---------------------|----------------------|--------------|
| "What capabilities do we need?" | Business Capability Map | Capability, Resource, Value Stream |
| "How do our processes work?" | Business Process Cooperation | Process, Service, Role, Event |
| "What applications support us?" | Application Usage | Application Component, Business Process, Data Object |
| "How do applications integrate?" | Application Cooperation | Application Component, Interface, Flow, Service |
| "What infrastructure do we need?" | Technology Usage | Node, Device, System Software, Artifact |
| "What's our migration path?" | Migration | Plateau, Gap, Work Package |
| "Why are we doing this?" | Motivation | Stakeholder, Goal, Requirement, Principle |
| "How does strategy connect to IT?" | Strategy | Capability, Course of Action, Resource, Goal |

### Diagram Quality Checks (Evaluator)

- [ ] Each element has a type-appropriate shape (not generic rectangles)
- [ ] Relationships use correct ArchiMate line styles (composition ◆, aggregation ◇, flow →, serving ▷)
- [ ] Cross-layer relationships use the correct derived relationships
- [ ] No orphan elements (every element has at least one relationship)
- [ ] Viewpoint scope is respected (don't mix elements from unrelated layers)
- [ ] Naming follows `<Type>: <Name>` convention or consistent alternative

---

## Section 9: Architecture Repository Structure

The generator should organize architecture deliverables following this repository structure:

```
.harness/
  spec.md                          # Architecture Statement of Work
  features.json                    # Architecture deliverable tracker

project-root/
  architecture/
    1-vision/
      architecture-vision.md       # Phase A output
      stakeholder-map.md           # Stakeholder register + concerns
      value-chain.md               # Business value chain
      principles.md                # Architecture principles
    2-business/
      capability-map.md            # L0-L3 capability model
      process-models/              # Key business process diagrams
      organization-map.md          # Org → capability mapping
      business-services.md         # Business service catalog
    3-information-systems/
      application-portfolio.md     # Application catalog + health
      data-architecture.md         # Conceptual data model + classification
      integration-map.md           # Integration patterns + flows
    4-technology/
      technology-standards.md      # Standards profile + lifecycle
      platform-blueprint.md        # Platform architecture
      security-architecture.md     # Security controls + zones
    5-migration/
      gap-analysis.md              # Current → target gaps
      roadmap.md                   # Implementation timeline
      transition-architectures/    # Intermediate states
      work-packages.md             # Delivery work packages
    6-governance/
      compliance-criteria.md       # Architecture compliance
      change-log.md                # Architecture change requests
    decisions/
      ADR-001-*.md                 # Architecture Decision Records
      ADR-002-*.md
    diagrams/
      *.mermaid                    # Mermaid source files
      *.puml                       # PlantUML source files
```

### Repository Completeness Check (Evaluator)

The evaluator verifies repository structure completeness per phase:

| After Phase | Required Directories | Required Files (minimum) |
|-------------|---------------------|-------------------------|
| Phase A | `1-vision/` | architecture-vision.md, stakeholder-map.md, principles.md |
| Phase B | `2-business/` | capability-map.md, at least 1 process model |
| Phase C | `3-information-systems/` | application-portfolio.md, data-architecture.md |
| Phase D | `4-technology/` | technology-standards.md, platform-blueprint.md |
| Phase E-F | `5-migration/` | gap-analysis.md, roadmap.md |
| Any | `decisions/` | At least 1 ADR per significant decision |

---

## Section 10: Architecture Anti-Patterns (Evaluator Watch List)

The evaluator should flag these common EA anti-patterns when grading:

| Anti-Pattern | What It Looks Like | Impact | Score Penalty |
|-------------|-------------------|--------|---------------|
| **Ivory Tower Architecture** | Detailed technical blueprints with no stakeholder input or validation | feasibility: -2 | Drop feasibility to max 2 |
| **PowerPoint Architecture** | Beautiful diagrams with no traceability to decisions or requirements | coherence: -2 | Drop coherence to max 2 |
| **Boil the Ocean** | Trying to document everything at maximum detail in one pass | stakeholder_coverage: -1 | Flag as scope risk |
| **Reference Model Worship** | Adopting a reference architecture without tailoring to context | standards_compliance: -1 | Require tailoring rationale |
| **Missing "As-Is"** | Target state defined without documenting current state | coherence: -2 | Cannot assess gaps without baseline |
| **Decision Amnesia** | Architecture exists but no record of WHY decisions were made | all criteria: -1 | Require ADRs for significant choices |
| **Layer Leaking** | Business elements directly referencing technology without application mediation | standards_compliance: -1 | Flag ArchiMate violation |
| **Orphan Capabilities** | Capabilities in the model with no supporting applications or technology | coherence: -1 | Flag completeness gap |
| **Security Afterthought** | Security addressed only in Phase E-F (migration) instead of Phase D (design) | feasibility: -2 | Drop feasibility to max 2 |

---

## Section 11: Zachman Framework Detail

The Zachman Framework classifies architecture artifacts along two dimensions: six interrogatives (columns) and six audience perspectives (rows). Use this section when the project selects Zachman as its primary framework, or when a TOGAF-based project needs a classification overlay for artifact completeness auditing.

### 6x6 Matrix Template

| | What (Data) | How (Function) | Where (Network) | Who (People) | When (Time) | Why (Motivation) |
|---|---|---|---|---|---|---|
| **Scope (Planner)** | Business entities list | Core business processes | Operating locations | Stakeholder register | Business event calendar | Business vision and goals |
| **Business Model (Owner)** | Semantic data model | Business process model (BPMN) | Logistics and facility network | Workflow and role model | Master schedule / milestones | Business strategy and objectives |
| **System Model (Designer)** | Logical data model (ERD) | Application function model | Distributed system architecture | Interface and access model | Processing structure / sequence | Business rule specification |
| **Technology Model (Builder)** | Physical data model | Technology design (APIs, services) | Network architecture (topology) | Security and identity architecture | Control flow / timing definition | Rule implementation design |
| **Detailed Representation (Subcontractor)** | Data definition (DDL, schemas) | Program / module specification | Network configuration detail | Role-permission configuration | Execution schedule / triggers | Rule engine configuration |
| **Functioning Enterprise** | Operational data instances | Running processes and services | Live network and infrastructure | Active users and sessions | Real-time events and schedules | Enforced policies and constraints |

Each cell describes a specific artifact type. The Zachman Framework does not prescribe a sequence -- all cells are equally valid entry points. The harness uses column-by-column or row-by-row traversal depending on the sprint mapping strategy.

### Sprint Mapping Strategies

| Strategy | When to Use | Sprint Structure |
|----------|-------------|-----------------|
| **Column-per-sprint** | Broad horizontal coverage needed first (e.g., data-centric projects) | Sprint 1: What (Data) column, Sprint 2: How (Function) column, etc. |
| **Row-per-sprint** | Depth at one audience level first (e.g., executive sign-off before detail) | Sprint 1: Scope row, Sprint 2: Business Model row, etc. |
| **Diagonal** | Rapid prototyping -- one cell per sprint at increasing detail | Sprint 1: Scope/What, Sprint 2: Business/How, Sprint 3: System/Where, etc. |
| **Cluster** | Focused area of concern (e.g., security spans Who column + Where column) | Sprint N: 2x3 cluster of related cells defined in the contract |

The planner selects the strategy during initialization and records it in `spec.md`. The coordinator enforces sprint boundaries accordingly.

### When to Use Zachman vs TOGAF

| Criterion | Choose Zachman | Choose TOGAF |
|-----------|---------------|--------------|
| **Project goal** | Classify and organize existing artifacts; ensure completeness | Transform the enterprise through a phased architecture program |
| **Organization maturity** | Low EA maturity -- need a taxonomy before a process | Moderate-to-high EA maturity -- ready for an iterative development method |
| **Deliverable type** | Primarily documentation and classification | Architecture development with governance and change management |
| **Stakeholder audience** | Executives who need a single-page view of all architecture dimensions | Architecture board that needs phase gates and compliance reviews |
| **Regulatory driver** | Audit and compliance (artifact completeness evidence) | Strategic transformation (capability roadmap and migration planning) |
| **Complementary use** | Use Zachman as the classification overlay for TOGAF deliverables | Use TOGAF ADM as the process engine; Zachman as the filing cabinet |

In practice, many organizations use both: TOGAF ADM as the development process and Zachman as the classification scheme for the resulting artifacts. When both are active, the generator should tag each deliverable with its Zachman cell coordinates (e.g., `[Row: Business Model, Column: Data]`).

---

## Section 12: FEAF Detail

The Federal Enterprise Architecture Framework (FEAF) organizes architecture around five reference models. Use this section when the project targets federal government or public sector organizations, or when compliance with OMB Circular A-130 is required.

### FEAF Reference Models and Sprint Mapping

| Reference Model | Abbreviation | Purpose | Key Deliverables | Harness Sprint Mapping |
|----------------|-------------|---------|-----------------|----------------------|
| **Performance Reference Model** | PRM | Measure outcomes against strategic goals | Performance measurement framework, KPI hierarchy, outcome-to-output mapping | Sprint 1: Establish performance baselines and target metrics |
| **Business Reference Model** | BRM | Classify government functions and services | Lines of business, sub-functions, service catalog, citizen-facing services inventory | Sprint 2: Map business functions and services |
| **Data Reference Model** | DRM | Describe data assets and sharing mechanisms | Data taxonomy, data sharing agreements, master data catalog, metadata standards | Sprint 3: Define data architecture and sharing |
| **Application Reference Model** | ARM | Classify application capabilities | Application portfolio, service component inventory, technology services catalog | Sprint 4: Map applications to business services |
| **Infrastructure Reference Model** | IRM | Describe technology infrastructure | Network topology, hosting inventory, shared services catalog, security zones | Sprint 5: Define infrastructure and shared services |

The default sprint order follows the PRM-BRM-DRM-ARM-IRM sequence (strategy to implementation). The planner may reorder based on agency priorities -- for example, starting with BRM when business function consolidation is the primary goal.

### Federal Compliance Integration

| Compliance Framework | Integration Point | Generator Action | Evaluator Check |
|---------------------|-------------------|-----------------|-----------------|
| **FISMA** (Federal Information Security Modernization Act) | IRM, ARM | Include security categorization (FIPS 199) for each system; map to NIST 800-53 control families | Verify every system in the ARM has a FIPS 199 category and mapped controls |
| **FedRAMP** (Federal Risk and Authorization Management Program) | IRM, ARM | Tag cloud-hosted services with FedRAMP authorization status (Agency ATO, JAB P-ATO, In Process) | Verify cloud services have FedRAMP status documented |
| **OMB Circular A-130** | All models | Ensure information resource management aligns with A-130 requirements; include records management | Verify A-130 compliance checklist addressed per reference model |
| **Section 508 / WCAG** | ARM | Flag user-facing applications for accessibility compliance requirements | Verify accessibility requirements documented for citizen-facing services |
| **NIST Cybersecurity Framework** | IRM | Map infrastructure components to CSF functions (Identify, Protect, Detect, Respond, Recover) | Verify CSF mapping exists for critical infrastructure components |
| **Privacy Act / SORN** | DRM | Identify systems of records containing PII; reference System of Records Notices | Verify PII inventory and SORN references in data architecture |

### Common Reference Model Artifacts

**BRM Artifact Template:**
```
## Business Reference Model: [Agency/Organization]

### Lines of Business
| LoB ID | Name | Sub-Functions | Citizen Services |
|--------|------|--------------|-----------------|
| LoB-01 | [Name] | [List] | [Yes/No -- describe if Yes] |

### Service Catalog
| Service ID | Service Name | LoB | Delivery Channel | SLA Target |
|-----------|-------------|-----|-------------------|------------|
| SVC-01 | [Name] | LoB-01 | [Web/In-Person/Phone] | [Target] |
```

**DRM Artifact Template:**
```
## Data Reference Model: [Agency/Organization]

### Data Taxonomy
| Data Domain | Description | Authoritative Source | Sharing Classification |
|------------|------------|---------------------|----------------------|
| [Domain] | [Description] | [Source system] | Open / Restricted / Classified |

### Data Sharing Agreements
| Agreement ID | Parties | Data Domain | Legal Authority | Review Cycle |
|-------------|---------|------------|----------------|-------------|
| DSA-01 | [Agency A, Agency B] | [Domain] | [Statute/MOU] | [Annual/Biennial] |
```

**PRM Artifact Template:**
```
## Performance Reference Model: [Agency/Organization]

### Strategic Goals to Metrics
| Goal ID | Strategic Goal | Outcome Metric | Baseline | Target | Data Source |
|---------|---------------|---------------|----------|--------|------------|
| G-01 | [Goal statement] | [Metric] | [Current value] | [Target value] | [Source] |

### Measurement Hierarchy
Strategic Goal -> Outcome -> Output -> Activity -> Input
Each level must have at least one measurable indicator.
```

---

## Section 13: Architecture Decision Record Template

Architecture Decision Records (ADRs) capture the context, rationale, and consequences of architecturally significant decisions. Every EA project should maintain ADRs regardless of the selected framework.

### ADR Template

```markdown
# ADR-[NNN]: [Short Title]

## Metadata
- **ID**: ADR-[NNN]
- **Date**: [YYYY-MM-DD]
- **Status**: [proposed | accepted | deprecated | superseded by ADR-NNN]
- **Deciders**: [List of people involved in the decision]
- **Sprint**: [Harness sprint round where this decision was made]

## Context

[Describe the situation that requires a decision. Include technical, business, and organizational factors. Reference relevant stakeholder concerns, constraints, and drivers.]

## Decision

[State the decision clearly in one or two sentences. Use active voice: "We will..." or "The architecture will..."]

## Options Considered

| Option | Pros | Cons | Estimated Effort |
|--------|------|------|-----------------|
| [Option A] | [Benefits] | [Drawbacks] | [Low/Medium/High] |
| [Option B] | [Benefits] | [Drawbacks] | [Low/Medium/High] |
| [Option C] | [Benefits] | [Drawbacks] | [Low/Medium/High] |

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

### Risks
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

## Related ADRs
- [ADR-NNN: title -- relationship (supersedes, depends on, related to)]

## Compliance Notes
- [Relevant regulatory or standards implications]
```

### ADR Lifecycle States

| State | Meaning | Transition Trigger |
|-------|---------|-------------------|
| **Proposed** | Under discussion; not yet binding | ADR created during sprint planning or implementation |
| **Accepted** | Binding for all downstream work | Stakeholder review and approval (documented in sprint evaluation) |
| **Deprecated** | No longer relevant; kept for historical context | Business context changed; superseding decision not required |
| **Superseded** | Replaced by a newer decision | New ADR explicitly references and replaces this one |

### When to Create an ADR

Create an ADR when any of the following conditions are met:

1. **Technology selection**: Choosing a platform, product, or standard (e.g., cloud provider, database engine, messaging protocol)
2. **Pattern selection**: Choosing an integration pattern, deployment model, or architectural style
3. **Trade-off resolution**: Resolving a conflict between competing quality attributes (e.g., security vs. usability, cost vs. performance)
4. **Standards deviation**: Deviating from established architecture principles or reference architecture
5. **Significant scope change**: Changing the boundary of an architecture domain or deferring a planned capability

The evaluator should verify that every significant decision encountered during evaluation has a corresponding ADR. Missing ADRs trigger the "Decision Amnesia" anti-pattern (Section 10).

---

## Section 14: Tool Guidance

This section provides guidance on selecting and using modeling tools for enterprise architecture projects. Tool selection depends on organization size, budget, collaboration needs, and framework requirements.

### ArchiMate Modeling Tools

| Tool | License | Strengths | Limitations | Best For |
|------|---------|-----------|-------------|----------|
| **Archi** | Open source (EPL) | Free, lightweight, ArchiMate-native, cross-platform, exports to multiple formats | Single-user focused, limited collaboration, no built-in repository | Small teams, individual architects, learning ArchiMate, budget-constrained projects |
| **Sparx Enterprise Architect** | Commercial | Full UML + ArchiMate, code generation, simulation, extensive plugins, multi-user repository | Complex UI, steep learning curve, Windows-primary | Large enterprises, multi-framework projects, teams needing UML + ArchiMate together |
| **BiZZdesign HoriZZon** | Commercial (SaaS) | Purpose-built for EA, TOGAF-native, collaborative, integrated governance workflows | Expensive, vendor lock-in for model format | TOGAF-based programs, organizations with EA governance maturity |
| **LeanIX** | Commercial (SaaS) | Application portfolio management, technology risk, lightweight EA, API-first | Not a full modeling tool, limited notation support | CIO offices, application rationalization, technology lifecycle management |
| **Ardoq** | Commercial (SaaS) | Data-driven architecture, dynamic visualizations, integration with ITSM/CMDB | Less suited for formal notation (ArchiMate diagrams) | Data-centric EA, organizations with strong CMDB/ITSM tooling |

### Diagram Validation Rules

When the generator produces diagrams in Mermaid or PlantUML format, the evaluator should verify:

| Rule | Check Method | Pass Criterion |
|------|-------------|---------------|
| **Renders without errors** | Run Mermaid CLI (`mmdc`) or PlantUML (`plantuml`) on source file | Zero syntax errors, diagram renders to image |
| **Correct element types** | Visual inspection against ArchiMate specification | Elements use correct shapes for their type (no generic rectangles for typed elements) |
| **Relationship direction** | Check arrow directions against the model semantics | Serving arrows point from provider to consumer; flow arrows follow data direction |
| **No orphan elements** | Count elements with zero relationships | Every element has at least one inbound or outbound relationship |
| **Layer separation** | Check that elements from different layers are visually grouped | Business, Application, and Technology layers are clearly distinguished |
| **Consistent naming** | Pattern-match element labels | All elements follow the project naming convention (e.g., `[Type]: [Name]` or `[Domain]-[Name]`) |

### Model Repository Recommendations

| Scenario | Recommendation | Rationale |
|----------|---------------|-----------|
| **Solo architect, open-source stack** | Archi + Git repository for `.archimate` files | Version-controlled, diffable (XML format), zero cost |
| **Small team, shared models** | Archi with coArchi plugin (Git-based collaboration) | Multi-user via Git branching, no server required |
| **Medium team, formal governance** | Sparx EA with cloud-based repository (Pro Cloud Server) | Concurrent editing, role-based access, baseline comparison |
| **Enterprise program, TOGAF governance** | BiZZdesign or Sparx EA with integrated governance workflows | Approval workflows, architecture board reviews, compliance tracking |
| **API-first, data-driven EA** | LeanIX or Ardoq with REST API integration | Automated data collection from CMDB, live dashboards |
| **Harness-generated diagrams** | Mermaid or PlantUML source in `diagrams/` directory, rendered during evaluation | Text-based, version-controlled, evaluator can re-render and validate |

For harness projects, the generator should always produce diagram source files (Mermaid or PlantUML) in the `architecture/diagrams/` directory. Binary formats (Visio, PowerPoint) are not diffable and cannot be validated by the evaluator programmatically.

---

## Section 15: Stakeholder Workshop Template

Stakeholder workshops are a primary elicitation and validation technique in enterprise architecture. Use these templates to plan, execute, and capture outputs from architecture workshops.

### Workshop Agenda Template

```markdown
# Architecture Workshop: [Workshop Title]

## Logistics
- **Type**: [Vision | Review | Sign-off | Discovery]
- **Date**: [YYYY-MM-DD]
- **Duration**: [2h | Half-day | Full-day]
- **Location**: [Physical location or virtual platform]
- **Facilitator**: [Name and role]
- **Scribe**: [Name -- responsible for capturing decisions and action items]

## Objectives
1. [Primary objective -- what decision or outcome is expected]
2. [Secondary objective]

## Agenda

| Time | Duration | Activity | Lead | Output |
|------|----------|----------|------|--------|
| 09:00 | 15 min | Opening: context setting and objectives review | Facilitator | Shared understanding of workshop goals |
| 09:15 | 30 min | Presentation: [current state / proposed architecture / gap analysis] | Architect | Questions and concerns captured |
| 09:45 | 45 min | Working session: [activity -- e.g., capability mapping, risk identification, trade-off discussion] | Facilitator | [Specific artifact -- e.g., annotated capability map, risk register entries] |
| 10:30 | 15 min | Break | -- | -- |
| 10:45 | 45 min | Discussion: [key decision topic] | Facilitator | Decision or options narrowed with rationale |
| 11:30 | 20 min | Action items and next steps | Facilitator | Action item list with owners and dates |
| 11:50 | 10 min | Closing: summary and feedback | Facilitator | Workshop evaluation |

## Pre-Read Materials
- [Document 1: link or path]
- [Document 2: link or path]
```

### Attendee Roles and Responsibilities

| Role | Responsibility | Expected Contribution | Required/Optional |
|------|---------------|----------------------|-------------------|
| **Executive Sponsor** | Strategic direction and decision authority | Business priorities, funding approval, conflict resolution | Required for Vision and Sign-off workshops |
| **Business Owner** | Business requirements and process knowledge | Domain expertise, current pain points, success criteria | Required for all workshop types |
| **Enterprise Architect** | Architecture vision and standards | Architecture options, trade-off analysis, standards guidance | Required for all workshop types |
| **Solution Architect** | Technical feasibility and design | Implementation constraints, technology options, integration concerns | Required for Review and Discovery workshops |
| **Business Analyst** | Requirements traceability and documentation | Requirements mapping, gap identification, acceptance criteria | Optional -- recommended for Discovery workshops |
| **Security/Compliance** | Regulatory and security constraints | Compliance requirements, risk assessment, control recommendations | Required when architecture touches regulated data or systems |
| **Facilitator** | Workshop process and time management | Neutral facilitation, conflict mediation, parking lot management | Required for all workshop types |
| **Scribe** | Capture decisions, actions, and outputs | Real-time documentation, decision log maintenance | Required for all workshop types |

### Expected Outputs by Workshop Type

| Workshop Type | Primary Output | Secondary Outputs | Decision Authority |
|--------------|---------------|-------------------|-------------------|
| **Vision** | Architecture Vision document (draft) | Stakeholder concern register, initial capability map, architecture principles (draft) | Executive Sponsor approves vision direction |
| **Review** | Reviewed architecture with annotated feedback | Issue log, change requests, updated risk register | Architecture Board or designated reviewers |
| **Sign-off** | Signed Architecture Compliance statement | Approved ADRs, baselined deliverables, dispensation requests (if any) | Designated approvers per governance framework |
| **Discovery** | As-is documentation and gap inventory | Stakeholder interview notes, process observations, data inventory | No formal decision -- information gathering |

### Decision Log Format

Capture every decision made during workshops using this format:

| Decision ID | Date | Workshop | Decision Statement | Rationale | Decided By | Impact | Related ADR |
|------------|------|----------|-------------------|-----------|-----------|--------|-------------|
| DEC-001 | [Date] | [Workshop title] | [Clear statement of what was decided] | [Why this option was chosen] | [Names/roles] | [High/Medium/Low] | [ADR-NNN or "N/A -- operational decision"] |

Decisions with High impact must be promoted to a formal ADR. Medium impact decisions should be promoted if they affect more than one architecture domain. Low impact decisions are recorded in the log only.
