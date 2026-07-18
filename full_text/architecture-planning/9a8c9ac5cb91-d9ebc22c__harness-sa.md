---
name: harness-sa
description: "Solution Architecture domain skill for the harness plugin. Provides SA methodology selection (C4 Model, Arc42, 4+1 View, Domain-Driven Design, Microservices Patterns), development methodology (API-First, Component-First, Data-First, Event-First, Contract-First), verification strategy, deliverable verification, evaluation criteria (design_coherence, technical_depth, integration_clarity, implementability), and sprint contract checklist templates. Activated when domain_profile is "solution_architecture"."
---

# Solution Architecture Domain Skill

> **Domain-specific.** This skill provides the HOW for solution architecture projects. The harness provides the WHEN (orchestration, sprint contracts, feature ledger). This skill provides the HOW (framework selection, development methodology, deliverable verification, evaluation criteria anchors, and solution design patterns).

Activated when `domain_profile: solution_architecture` is declared in `.harness/spec.md`.

## Scope of This Skill

This skill covers the Solution Architecture lifecycle for a single solution:
- **Context**: Business drivers, constraints, stakeholders, quality attributes
- **Design**: Component decomposition, API contracts, data models, integration patterns
- **Validation**: Design reviews, proof of concept, capacity modeling, failure mode analysis
- **Communication**: Architecture diagrams, decision records, technical specifications

This skill is distinct from `harness-ea` (Enterprise Architecture). EA covers enterprise-wide capability mapping, portfolio management, and governance frameworks (TOGAF, Zachman). SA focuses on a single solution's technical design — how components fit together, how APIs are defined, how data flows, and how the solution meets non-functional requirements.

It is framework-agnostic at its core — any of the supported approaches can be selected. The C4 Model is the default because it provides progressive detail levels (Context, Container, Component, Code) that map naturally to harness sprints.


## Activation Check

This skill activates when `domain_profile: solution_architecture` is set in `.harness/spec.md` or `.harness/state.json`.

Before using this skill's procedures:
1. Verify the project produces solution design deliverables (HLDs, LLDs, API specs, data models — not enterprise-wide capability maps)
2. Read spec.md -> identify the selected SA framework (C4, Arc42, 4+1, etc.)
3. If no framework specified -> default to C4 Model
4. Check if `solution-architecture/` directory exists -> if yes, verify against the Repository Structure (Section 9)
5. Identify the architecture style -> select appropriate patterns from Section 7

---

## Section 1: SA Methodology

Select based on project characteristics during `/harness:start`:

| Framework | When to Use | Phase Structure | Harness Mapping |
|-----------|-------------|-----------------|-----------------|
| C4 Model | Most solution designs, progressive detail | Context, Container, Component, Code | 1 sprint = 1 C4 level |
| Arc42 | Documentation-heavy, European standard | 12 sections (constraints, context, building blocks, runtime, deployment, etc.) | 1 sprint = 2-3 Arc42 sections |
| 4+1 View | Complex systems, multiple stakeholder perspectives | Logical, Development, Process, Physical + Scenarios | 1 sprint = 1 view |
| Domain-Driven Design | Complex business domains, bounded contexts | Strategic design (contexts, maps) -> Tactical design (aggregates, entities, services) | 1 sprint = 1 bounded context |
| Microservices Patterns | Distributed systems, cloud-native | Decomposition, Communication, Data, Deployment, Observability | 1 sprint = 1 pattern category |

**Default:** C4 Model (if not specified by user).

The planner writes the selected framework into `spec.md` during initialization. The coordinator uses the mapping to structure sprint boundaries accordingly.

---

## Section 2: Solution Architecture Development Methodology

Select based on project type and stakeholder needs:

| Methodology | When to Use | How It Drives the Generator |
|-------------|-------------|----------------------------|
| API-First | Integration-heavy, multi-team | Generator defines API contracts FIRST (OpenAPI/AsyncAPI specs), then designs components around them |
| Component-First | Monolith decomposition, modularization | Generator identifies components and boundaries FIRST, then defines interfaces between them |
| Data-First | Data-intensive applications, analytics | Generator designs data models FIRST (conceptual, logical, physical), then builds services around data flows |
| Event-First | Event-driven, real-time, CQRS | Generator defines domain events and event flows FIRST, then designs producers, consumers, and projections |
| Contract-First | Multi-team, external integrations | Generator writes interface contracts FIRST (API specs, message schemas, SLAs), then implements behind contracts |

**Default:** API-First for all SA projects (if not specified).

### How Methodology Drives the Harness

The chosen methodology affects every phase:

1. **Generator behavior**: What to produce first (API specs? component diagrams? data models?)
2. **Evaluator criteria**: What to prioritize (API consistency? component cohesion? data integrity?)
3. **Sprint contract**: What acceptance criteria to define (API completeness? component boundaries? data model correctness?)
4. **Artifact types**: What deliverables per sprint (OpenAPI specs? C4 diagrams? ERDs?)

### Generator First-Action Table

| Methodology | Generator produces first | Then |
|-------------|------------------------|------|
| API-First | OpenAPI/AsyncAPI specifications with request/response schemas | Component design implementing the API contracts, data models supporting the APIs |
| Component-First | Component diagram with responsibilities and boundaries | Interface definitions between components, deployment mapping |
| Data-First | Conceptual and logical data models with entity relationships | Services that own data entities, API contracts for data access |
| Event-First | Domain event catalog with schemas and flow diagrams | Event producers, consumers, projections, and saga orchestration |
| Contract-First | Interface contracts (API specs, message schemas, SLAs) | Implementation design behind each contract, testing strategy |

---

## Section 3: Verification Strategy (SA Equivalent of Testing)

| Verification Type | SA Equivalent | Method |
|-------------------|--------------|--------|
| Unit test | Component design review | Each component has clear responsibility, defined interfaces, and no circular dependencies |
| Integration test | Interface consistency | API contracts between components are compatible (request/response schemas match, error codes consistent) |
| E2E test | Scenario walkthrough | User scenario traces through all components from entry point to data store without gaps |
| Smoke test | Deliverable completeness | Required design documents exist and are non-empty |
| Regression | Pattern compliance | Architecture patterns consistently applied (e.g., all services use the same auth pattern, all APIs follow the same versioning scheme) |

### Design Completeness Checks

- Does the system context diagram show all external systems and actors?
- Are all components defined with clear responsibilities?
- Does each API endpoint have a complete specification (request, response, errors, auth)?
- Are all data entities defined with relationships and ownership?
- Do non-functional requirements have measurable targets and design strategies?
- Are all integration points documented with protocols and data formats?
- Do architecture decision records exist for significant choices?

---

## Section 4: Deliverable Verification (Equivalent of Build/Runtime)

Since SA produces design documents, not running software, "build verification" means:

| Check | What to Verify | How |
|-------|---------------|-----|
| Document structure | Required sections present per framework | Check against C4/Arc42/4+1 section requirements |
| API specification | OpenAPI/AsyncAPI specs are valid | Lint specs with spectral or swagger-cli |
| Data model consistency | Entities referenced in APIs exist in data model | Cross-reference API schemas with data dictionary |
| Component boundaries | No circular dependencies between components | Trace dependency graph for cycles |
| NFR coverage | Each NFR has a design strategy | Cross-reference NFR list with architecture decisions |
| Integration completeness | All external systems have documented integration patterns | Cross-reference context diagram with integration specs |
| Decision records | All significant decisions documented | Verify ADR exists for each technology choice and pattern selection |

### C4 Level Gate Checks

| C4 Level | Required Deliverables |
|----------|----------------------|
| Context | System context diagram, actors list, external systems list, system purpose |
| Container | Container diagram, technology choices, container responsibilities, communication protocols |
| Component | Component diagram per container, component responsibilities, interface definitions |
| Code (optional) | Class/module diagrams for complex components, key algorithms documented |

### Arc42 Section Gate Checks

| Section | Required Content |
|---------|-----------------|
| 1. Requirements | Quality goals, stakeholders, top 3-5 requirements |
| 2. Constraints | Technical, organizational, and regulatory constraints |
| 3. Context | System context with external interfaces |
| 4. Solution Strategy | Key design decisions and technology choices |
| 5. Building Blocks | Level 1-3 decomposition with responsibilities |
| 6. Runtime | Key scenarios as sequence or activity diagrams |
| 7. Deployment | Infrastructure topology, node mapping |
| 8. Crosscutting | Security, logging, error handling, configuration |
| 9. Decisions | Architecture decision records |
| 10. Quality | Quality tree, quality scenarios |
| 11. Risks | Technical risks and debt |
| 12. Glossary | Domain terms and definitions |

---

## Section 5: Evaluation Criteria (Solution Architecture Profile)

The 4 primary criteria for the `solution_architecture` domain profile. The evaluator MUST use these anchors for consistent scoring across sprints.

### design_coherence (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no logical structure, components undefined |
| 1 | Severely incomplete — components listed but no clear boundaries or responsibilities |
| 2 | Below acceptable — components defined but inconsistent patterns, unclear boundaries, some circular dependencies |
| 3 | Acceptable — components have clear responsibilities, consistent decomposition pattern, no circular dependencies |
| 4 | Strong — well-defined component boundaries with explicit interfaces, consistent patterns throughout, separation of concerns evident |
| 5 | Excellent — elegant decomposition with clear rationale, every component justified, patterns applied consistently, design principles documented and followed |

### technical_depth (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no technical design decisions documented |
| 1 | Severely incomplete — technology choices listed but no rationale, no edge cases considered |
| 2 | Below acceptable — some design decisions documented but major gaps (e.g., no error handling strategy, no scalability consideration) |
| 3 | Acceptable — key design decisions documented with rationale, error handling and scalability addressed at high level, authentication and authorization approach documented |
| 4 | Strong — comprehensive design with edge cases addressed, capacity estimates provided, failure modes analyzed, technology choices justified with trade-offs |
| 5 | Excellent — production-grade design depth with quantified capacity models, detailed failure mode analysis, performance budgets, security threat model, and proven pattern references |

### integration_clarity (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no integration points documented |
| 1 | Severely incomplete — external systems mentioned but no interface specifications |
| 2 | Below acceptable — integration points identified but protocols, data formats, or error handling undefined |
| 3 | Acceptable — all integration points documented with protocols, data formats, and basic error handling |
| 4 | Strong — complete API specifications (OpenAPI/AsyncAPI), data flow diagrams, retry/circuit-breaker patterns, SLAs defined |
| 5 | Excellent — integration contracts validated with consumer teams, contract testing strategy defined, versioning policy documented, monitoring and alerting for integrations specified |

### implementability (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — design cannot be built with available technology or resources |
| 1 | Severely incomplete — design is theoretically possible but no implementation path, missing critical details |
| 2 | Below acceptable — design is buildable but significant unknowns, no resource estimate, no phasing plan |
| 3 | Acceptable — design is buildable with identified technology, risks documented, implementation phases suggested |
| 4 | Strong — detailed implementation plan with technology validated, team skill gaps identified, phased delivery roadmap, risk mitigations in place, threat model completed for external-facing components |
| 5 | Excellent — design validated through proof of concept, team has demonstrated capability, dependencies secured, deployment strategy proven |

---

## Section 6: Sprint Contract Checklist Templates

Pre-built checklists for 5 SA phases. The generator includes the relevant checklist(s) in each sprint contract. The evaluator uses them as acceptance criteria.

### For Context & Constraints

- [ ] System purpose and scope clearly defined
- [ ] All external actors and systems identified in context diagram
- [ ] Quality attribute requirements listed with measurable targets (response time, availability, throughput)
- [ ] Technical constraints documented (platform, language, regulatory, organizational)
- [ ] Key assumptions and dependencies identified

### For Component Design

- [ ] All components identified with clear single responsibility
- [ ] Component interfaces defined (methods/endpoints, parameters, return types)
- [ ] Component dependencies mapped with no circular references
- [ ] Data ownership assigned to specific components
- [ ] Cross-cutting concerns addressed (auth, logging, error handling, configuration)

### For API Design

- [ ] All API endpoints specified with request/response schemas
- [ ] Authentication and authorization model defined per endpoint
- [ ] Error response format standardized with error codes
- [ ] API versioning strategy documented
- [ ] Rate limiting and throttling policies defined

### For Data Design

- [ ] Conceptual data model with entity relationships documented
- [ ] Data ownership per component/service defined
- [ ] Data consistency strategy chosen (strong vs eventual, saga patterns)
- [ ] Data migration strategy for schema changes documented
- [ ] Data retention, archival, and privacy requirements addressed

### For NFR & Capacity

- [ ] Performance budget defined (response times, throughput targets)
- [ ] Scalability strategy documented (horizontal/vertical, auto-scaling triggers)
- [ ] Availability target and redundancy design specified
- [ ] Security architecture documented (authentication, authorization, encryption, network segmentation)
- [ ] STRIDE threat model completed for each trust boundary crossing (required if spec.md external_exposure != none)
- [ ] Disaster recovery and business continuity strategy outlined

---

## Section 7: Reference Materials

### Architecture Patterns

| Pattern | When to Use | Key Concepts |
|---------|-------------|-------------|
| Layered (N-Tier) | Traditional web applications, clear separation of concerns | Presentation, business logic, data access, database layers |
| Microservices | Complex domains, independent deployment, team autonomy | Bounded contexts, service mesh, API gateway, event bus |
| Event-Driven | Real-time processing, loose coupling, CQRS | Event sourcing, publish/subscribe, event store, projections |
| Hexagonal (Ports & Adapters) | Testability, framework independence | Core domain, ports (interfaces), adapters (implementations) |
| CQRS | Read/write asymmetry, complex queries, event sourcing | Command model, query model, event store, projections |
| Serverless | Variable workloads, rapid scaling, pay-per-use | Functions, triggers, managed services, cold start |

### Cloud Reference Architectures

| Provider | Reference | Use Case |
|----------|-----------|----------|
| AWS | Well-Architected Framework | 6 pillars: operational excellence, security, reliability, performance, cost, sustainability |
| Azure | Azure Architecture Center | Reference architectures, design patterns, best practices |
| GCP | Google Cloud Architecture Framework | Design principles, operational excellence, system design |
| CNCF | Cloud Native Trail Map | Containerization, CI/CD, orchestration, observability, service mesh |

### Integration Patterns

| Pattern | When to Use | Key Concepts |
|---------|-------------|-------------|
| API Gateway | Multiple clients, cross-cutting concerns | Routing, auth, rate limiting, transformation |
| Message Queue | Async processing, load leveling | Producer, consumer, dead letter queue, retry |
| Event Bus | Multi-subscriber, loose coupling | Topics, subscriptions, event schema registry |
| Service Mesh | Service-to-service communication | Sidecar proxy, mTLS, circuit breaker, observability |
| BFF (Backend for Frontend) | Multiple client types with different needs | Client-specific aggregation, optimization |

---

## Section 8: Notation Guide

### C4 Diagram Conventions

| Level | Diagram Type | Elements | Detail Level |
|-------|-------------|----------|-------------|
| 1 - Context | System Context | System, Actors, External Systems | Highest level — shows system boundaries |
| 2 - Container | Container | Web App, API, Database, Message Queue | Technology choices visible |
| 3 - Component | Component | Controllers, Services, Repositories | Internal structure of containers |
| 4 - Code | Class/Module | Classes, interfaces, methods | Lowest level — only for complex parts |

### Sequence Diagram Guidelines

| Element | Usage | Convention |
|---------|-------|-----------|
| Participant | System, service, or actor | Name matches component names from C4 |
| Synchronous message | HTTP request, function call | Solid arrow with filled arrowhead |
| Asynchronous message | Event, message queue | Solid arrow with open arrowhead |
| Return message | Response, callback | Dashed arrow |
| Alt/Opt fragment | Conditional logic | Label with condition |
| Loop fragment | Repeated processing | Label with iteration condition |
| Note | Design rationale | Placed near relevant interaction |

### Component Diagram Standards

| Element | Representation | Usage |
|---------|---------------|-------|
| Component | Rectangle with <<component>> stereotype | A cohesive unit with defined interfaces |
| Interface (provided) | Lollipop (circle on stick) | What the component offers |
| Interface (required) | Socket (half-circle) | What the component needs |
| Dependency | Dashed arrow | Component uses another component |
| Package | Folder shape | Grouping of related components |

---

## Section 9: Solution Architecture Repository Structure

The generator should organize SA deliverables following this repository structure:

```
.harness/
  spec.md                              # Architecture Statement of Work
  features.json                        # Architecture deliverable tracker

project-root/
  solution-architecture/
    1-context/
      system-context.md                # C4 Level 1 — system purpose, actors, external systems
      quality-attributes.md            # NFRs with measurable targets
      constraints.md                   # Technical, organizational, regulatory constraints
      assumptions.md                   # Key assumptions and dependencies
    2-design/
      container-diagram.md             # C4 Level 2 — containers, technology choices
      component-design/                # C4 Level 3 — per-container component breakdowns
        service-a-components.md
        service-b-components.md
      cross-cutting-concerns.md        # Auth, logging, error handling, config patterns
    3-api/
      api-overview.md                  # API landscape and conventions
      openapi/                         # OpenAPI specification files
        service-a-api.yaml
        service-b-api.yaml
      async-api/                       # AsyncAPI specification files (if event-driven)
        events.yaml
    4-data/
      conceptual-data-model.md         # Entity relationships and ownership
      data-dictionary.md               # Field-level definitions
      data-flow.md                     # Data movement between components
      consistency-strategy.md          # Consistency, transactions, saga patterns
    5-infrastructure/
      deployment-topology.md           # C4 Deployment diagram — nodes, containers, mapping
      scalability-strategy.md          # Scaling approach, capacity estimates
      security-architecture.md         # Security controls, threat model
      dr-strategy.md                   # Disaster recovery and business continuity
    decisions/
      ADR-001-*.md                     # Architecture Decision Records
      ADR-002-*.md
    diagrams/
      *.mermaid                        # Mermaid source files
      *.puml                           # PlantUML source files
```

### Repository Completeness Check (Evaluator)

The evaluator verifies repository structure completeness per phase:

| After Phase | Required Directories | Required Files (minimum) |
|-------------|---------------------|-------------------------|
| Context | `1-context/` | system-context.md, quality-attributes.md |
| Design | `2-design/` | container-diagram.md, at least 1 component design |
| API | `3-api/` | api-overview.md, at least 1 OpenAPI spec |
| Data | `4-data/` | conceptual-data-model.md, data-dictionary.md |
| Infrastructure | `5-infrastructure/` | deployment-topology.md, security-architecture.md |
| Any | `decisions/` | At least 1 ADR per significant decision |

---

## Section 10: Solution Architecture Anti-Patterns (Evaluator Watch List)

The evaluator should flag these common SA anti-patterns when grading:

| Anti-Pattern | What It Looks Like | Impact | Score Penalty |
|-------------|-------------------|--------|---------------|
| **Diagram-Only Architecture** | Beautiful diagrams with no supporting specifications or decision rationale | design_coherence: -2 | Drop design_coherence to max 2 |
| **Resume-Driven Architecture** | Technology choices made for novelty rather than fitness for purpose | implementability: -2 | Drop implementability to max 2 |
| **Integration by Assumption** | External system interfaces assumed without verification or contract | integration_clarity: -2 | Drop integration_clarity to max 2 |
| **NFR Hand-Waving** | "The system shall be scalable" without measurable targets or design strategy | technical_depth: -1 | Require quantified NFR targets |
| **Distributed Monolith** | Microservice structure with tight coupling, shared databases, synchronous chains | design_coherence: -2 | Flag as fundamental design issue |
| **Missing Failure Modes** | Happy path designed but no error handling, retry, or degradation strategy | technical_depth: -1 | Require failure mode analysis |
| **API Inconsistency** | Different naming conventions, error formats, or auth patterns across APIs | integration_clarity: -1 | Flag as integration risk |
| **Data Ownership Vacuum** | Data entities with no clear owning service or shared mutable state | design_coherence: -1 | Require explicit data ownership |
| **Auth as Afterthought** | No authentication or authorization in initial design for user-facing system | technical_depth: -2 | Drop technical_depth to max 2 |

---

## Section 11: Domain-Driven Design Specifics

This section provides actionable DDD guidance for solution architects designing complex business domains. Use these templates during the Strategic Design and Tactical Design phases of a DDD-driven architecture.

### Strategic Design

Strategic design establishes the high-level structure of the domain by identifying bounded contexts and their relationships. Complete these steps before moving to tactical design.

#### Bounded Context Identification Checklist

Use this checklist when decomposing a domain into bounded contexts:

- [ ] Identify distinct sub-domains by analyzing business capabilities and organizational boundaries
- [ ] For each candidate context, verify it has its own ubiquitous language (same term has different meaning across contexts)
- [ ] Confirm each context can be developed and deployed independently
- [ ] Verify each context has a single team owner (or a clear ownership split rationale)
- [ ] Check that no entity spans multiple contexts without an explicit mapping strategy
- [ ] Document the context boundary with inputs, outputs, and invariants it protects
- [ ] Validate with domain experts that context boundaries align with real business divisions

#### Context Mapping Patterns

Use the following patterns to define relationships between bounded contexts. Each pattern describes a different integration strategy depending on team dynamics, power relationships, and coupling tolerance.

| Pattern | Description | When to Use | Team Dynamic |
|---------|-------------|-------------|-------------|
| Shared Kernel | Two contexts share a subset of the domain model; changes require agreement from both teams | Small, tightly collaborating teams working on overlapping functionality | Co-equal partnership, high trust |
| Customer-Supplier | Upstream context (supplier) provides data or services; downstream context (customer) depends on it | Clear producer-consumer relationship with negotiable interface | Upstream accommodates downstream needs |
| Conformist | Downstream context adopts the upstream model as-is without translation | Upstream team has no incentive or capacity to support downstream needs | Downstream adapts, no negotiation |
| Anti-Corruption Layer | Downstream context translates the upstream model into its own domain language through an isolation layer | Upstream model is legacy, unstable, or conceptually misaligned with downstream needs | Downstream protects itself from external model pollution |
| Open Host Service | Upstream context exposes a well-defined public API (protocol) that multiple consumers can use | Multiple downstream consumers with similar needs; upstream wants a single integration surface | Upstream publishes, many consume |
| Published Language | Contexts communicate through a shared, documented data format (schema, standard, or specification) | Cross-organization integration, industry standards (EDI, FHIR, FIX) | Format-driven, decoupled teams |
| Separate Ways | Contexts do not integrate at all; each solves the overlapping need independently | Cost of integration exceeds benefit; overlap is minor or temporary | No relationship, full independence |

#### Context Map Template

Document the full context map for a solution using this format:

```
Context Map: [Solution Name]

[Context A] <-> [Context B] : Shared Kernel
  - Shared elements: [list shared entities/value objects]
  - Governance: [who approves changes to the shared kernel]

[Context C] -> [Context D] : Customer-Supplier
  - Upstream (Supplier): Context C
  - Downstream (Customer): Context D
  - Contract: [API spec or event schema reference]

[Context E] -> [Context F] : Anti-Corruption Layer
  - ACL Location: Context F inbound adapter
  - Translation: [upstream model element] -> [downstream model element]
```

### Tactical Design

Tactical design defines the internal structure of each bounded context. Use these templates to design entities, value objects, and aggregates within a single context.

#### Entity vs Value Object Decision Table

| Criterion | Entity | Value Object |
|-----------|--------|-------------|
| Identity | Has a unique, persistent identity (ID) that distinguishes it even when all attributes are identical | Defined entirely by its attributes; two instances with the same values are interchangeable |
| Lifecycle | Created, modified, persisted, and eventually archived or deleted | Immutable once created; replaced rather than modified |
| Equality | Compared by identity (ID), not by attribute values | Compared by structural equality (all attribute values match) |
| Examples | Customer, Order, Account, Product (catalog item) | Money (amount + currency), Address, DateRange, EmailAddress, Coordinates |
| Persistence | Own table/document with a primary key | Embedded within an entity or stored as a composite column |
| Mutability | Attributes change over time; state transitions are meaningful | No state changes; create a new instance instead |

**Decision rule:** If the concept must be tracked over time and distinguished from other instances with the same attributes, it is an Entity. Otherwise, prefer a Value Object for simplicity and immutability.

#### Aggregate Design Rules

An aggregate is a cluster of entities and value objects with a single root entity that enforces invariants. Follow these rules when designing aggregates:

1. **Single responsibility for invariants**: Each aggregate protects one consistency boundary. If an invariant spans two aggregates, reconsider the boundary.
2. **Reference by identity**: Aggregates reference other aggregates by ID, not by direct object reference. This prevents transactional coupling.
3. **Small aggregates**: Prefer small aggregates (one root entity + value objects). Large aggregates cause contention and performance issues.
4. **Eventual consistency between aggregates**: Use domain events to synchronize state across aggregate boundaries. Only enforce immediate consistency within a single aggregate.
5. **Root entity is the sole entry point**: All external access goes through the aggregate root. Child entities and value objects are not directly accessible from outside.

| Aggregate Component | Role | Access Rule |
|--------------------|------|-------------|
| Aggregate Root (Entity) | Entry point; enforces all invariants; controls lifecycle of children | Directly accessible by repositories and application services |
| Child Entity | Exists only within the aggregate; has local identity (unique within the aggregate, not globally) | Accessed only through the aggregate root |
| Value Object | Describes attributes of the root or child entities; immutable | Accessed only through the aggregate root |

#### Domain Service vs Application Service

| Aspect | Domain Service | Application Service |
|--------|---------------|-------------------|
| Purpose | Encapsulates domain logic that does not belong to a single entity or value object | Orchestrates use cases by coordinating domain objects, repositories, and infrastructure |
| Domain knowledge | Contains business rules and domain logic | Contains no business rules; delegates to domain layer |
| Dependencies | Other domain objects (entities, value objects, domain events) | Domain services, repositories, external service adapters |
| Example | PricingService.calculateDiscount(order, customer) | PlaceOrderUseCase.execute(command) -- coordinates Order aggregate, PricingService, PaymentGateway |
| Layer | Domain layer | Application layer |

### Ubiquitous Language Glossary

Maintain a glossary per bounded context to ensure all team members (developers, domain experts, product owners) use the same terms with the same meaning.

| Term | Definition | Bounded Context | Examples | Anti-Examples |
|------|-----------|----------------|----------|--------------|
| [Term] | [Precise definition as used within this context] | [Context name] | [Correct usage examples] | [Common misuses or confusions with terms from other contexts] |

**Glossary rules:**
- One entry per term per context. The same word in different contexts gets separate entries.
- Definitions must be validated by a domain expert, not invented by developers.
- Anti-examples column prevents drift by documenting how the term is misused or confused.
- Review the glossary at every sprint boundary; remove terms that are no longer used.

---

## Section 12: API Contract Templates

This section provides starter templates for API specifications. Use these when a sprint contract requires API design deliverables.

### OpenAPI 3.1 Starter Skeleton

The following is a minimal but complete OpenAPI 3.1 specification that a generator can copy and customize. It includes standard error responses, pagination, and a bearer auth security scheme.

```yaml
openapi: "3.1.0"
info:
  title: "[Service Name] API"
  version: "1.0.0"
  description: "[Brief description of what this API provides]"
  contact:
    name: "[Team Name]"
    email: "[team-email@example.com]"

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

security:
  - bearerAuth: []

paths:
  /resources:
    get:
      summary: List resources
      operationId: listResources
      tags:
        - Resources
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: page_size
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: sort
          in: query
          schema:
            type: string
            enum: [created_at, updated_at, name]
            default: created_at
      responses:
        "200":
          description: Successful response
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceListResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "500":
          $ref: "#/components/responses/InternalError"

    post:
      summary: Create a resource
      operationId: createResource
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateResourceRequest"
      responses:
        "201":
          description: Resource created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Resource"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "422":
          $ref: "#/components/responses/ValidationError"
        "500":
          $ref: "#/components/responses/InternalError"

  /resources/{resource_id}:
    get:
      summary: Get a resource by ID
      operationId: getResource
      tags:
        - Resources
      parameters:
        - name: resource_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        "200":
          description: Successful response
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Resource"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/NotFound"
        "500":
          $ref: "#/components/responses/InternalError"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Resource:
      type: object
      required: [id, name, created_at, updated_at]
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 255
        description:
          type: string
          maxLength: 2000
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    CreateResourceRequest:
      type: object
      required: [name]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
        description:
          type: string
          maxLength: 2000

    ResourceListResponse:
      type: object
      required: [data, pagination]
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/Resource"
        pagination:
          $ref: "#/components/schemas/Pagination"

    Pagination:
      type: object
      required: [page, page_size, total_items, total_pages]
      properties:
        page:
          type: integer
        page_size:
          type: integer
        total_items:
          type: integer
        total_pages:
          type: integer

    ErrorResponse:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code:
              type: string
              description: Machine-readable error code
            message:
              type: string
              description: Human-readable error description
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  reason:
                    type: string
            request_id:
              type: string
              format: uuid

  responses:
    BadRequest:
      description: Bad request -- malformed syntax or missing required fields
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    Unauthorized:
      description: Authentication required or token invalid
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    ValidationError:
      description: Request body failed validation
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
```

### AsyncAPI for Event-Driven Systems

Use this AsyncAPI 3.0 skeleton when designing event-driven interfaces between bounded contexts or microservices.

```yaml
asyncapi: "3.0.0"
info:
  title: "[Service Name] Events"
  version: "1.0.0"
  description: "[Brief description of the events this service produces or consumes]"

defaultContentType: application/json

channels:
  resourceCreated:
    address: "events.resources.created"
    description: Published when a new resource is created
    messages:
      resourceCreatedMessage:
        $ref: "#/components/messages/ResourceCreatedEvent"

  resourceUpdated:
    address: "events.resources.updated"
    description: Published when a resource is modified
    messages:
      resourceUpdatedMessage:
        $ref: "#/components/messages/ResourceUpdatedEvent"

operations:
  publishResourceCreated:
    action: send
    channel:
      $ref: "#/channels/resourceCreated"
    summary: Publish a resource-created event
    messages:
      - $ref: "#/channels/resourceCreated/messages/resourceCreatedMessage"

  publishResourceUpdated:
    action: send
    channel:
      $ref: "#/channels/resourceUpdated"
    summary: Publish a resource-updated event
    messages:
      - $ref: "#/channels/resourceUpdated/messages/resourceUpdatedMessage"

components:
  messages:
    ResourceCreatedEvent:
      name: ResourceCreatedEvent
      title: Resource Created
      contentType: application/json
      headers:
        type: object
        properties:
          event_id:
            type: string
            format: uuid
          event_type:
            type: string
            const: "resource.created"
          timestamp:
            type: string
            format: date-time
          correlation_id:
            type: string
            format: uuid
      payload:
        type: object
        required: [resource_id, name, created_at]
        properties:
          resource_id:
            type: string
            format: uuid
          name:
            type: string
          created_at:
            type: string
            format: date-time

    ResourceUpdatedEvent:
      name: ResourceUpdatedEvent
      title: Resource Updated
      contentType: application/json
      headers:
        type: object
        properties:
          event_id:
            type: string
            format: uuid
          event_type:
            type: string
            const: "resource.updated"
          timestamp:
            type: string
            format: date-time
          correlation_id:
            type: string
            format: uuid
      payload:
        type: object
        required: [resource_id, changed_fields, updated_at]
        properties:
          resource_id:
            type: string
            format: uuid
          changed_fields:
            type: array
            items:
              type: string
          updated_at:
            type: string
            format: date-time
```

### API Versioning Strategy

Choose a versioning approach based on the integration context. The table below compares the three common strategies.

| Strategy | Mechanism | When to Use | Advantages | Disadvantages |
|----------|-----------|-------------|-----------|--------------|
| URL Path | `/v1/resources`, `/v2/resources` | Public APIs, consumer-facing services, APIs with infrequent breaking changes | Simple to understand, easy to route, clear in documentation and logs | URL pollution, harder to sunset old versions, clients must update URLs |
| Header | `Accept: application/vnd.api.v2+json` or custom `API-Version: 2` | Internal APIs, APIs where URL stability matters, content-negotiation-aware clients | Clean URLs, supports content negotiation, version hidden from casual inspection | Less discoverable, requires header-aware tooling, harder to test in browser |
| Query Parameter | `/resources?version=2` | Transitional versioning, quick experiments, APIs where header support is limited | Easy to add without URL changes, simple for testing | Caching complications (query string affects cache keys), less conventional |

**Recommended defaults:**
- **Public APIs**: URL path versioning (simplest for external consumers)
- **Internal service-to-service**: Header versioning (cleaner, service meshes handle headers well)
- **Experimental or transitional**: Query parameter (low-effort, easy to remove)

#### Deprecation Policy Template

| Element | Policy |
|---------|--------|
| Deprecation notice period | Minimum [N] months before removal |
| Communication channel | Changelog entry, `Sunset` HTTP header on deprecated endpoints, API portal banner |
| Sunset header format | `Sunset: Sat, 01 Jan 2028 00:00:00 GMT` (RFC 7231 date) |
| Migration guide | Published before deprecation notice; includes before/after examples |
| Monitoring | Track usage of deprecated endpoints; alert if usage exceeds threshold after sunset date |
| Removal criteria | Zero traffic for [N] consecutive days after sunset date, or explicit stakeholder sign-off |

#### Breaking vs Non-Breaking Change Classification

| Change Type | Classification | Action Required |
|-------------|---------------|----------------|
| Add optional field to response | Non-breaking | No version bump; document in changelog |
| Add optional query parameter | Non-breaking | No version bump; document in changelog |
| Add new endpoint | Non-breaking | No version bump; document in changelog |
| Remove field from response | Breaking | New version required |
| Rename field | Breaking | New version required |
| Change field type | Breaking | New version required |
| Add required field to request | Breaking | New version required |
| Change URL structure | Breaking | New version required |
| Change authentication method | Breaking | New version required |
| Change error response format | Breaking | New version required |

---

## Section 13: Threat Modeling

This section provides a structured approach to identifying and prioritizing security threats during solution architecture design. Use these templates when a sprint contract requires threat analysis deliverables.

### STRIDE Analysis Template

STRIDE is a threat classification model developed at Microsoft. Each category represents a distinct class of security threat. Complete one row per identified threat.

| Threat Category | Description | Affected Component | Likelihood (1-5) | Impact (1-5) | Risk Score | Mitigation |
|----------------|-------------|-------------------|-------------------|---------------|------------|-----------|
| **Spoofing** | Attacker impersonates a legitimate user, service, or system component | [Component name] | [1-5] | [1-5] | [L x I] | [Specific countermeasure] |
| **Tampering** | Attacker modifies data in transit, at rest, or in processing to alter system behavior | [Component name] | [1-5] | [1-5] | [L x I] | [Specific countermeasure] |
| **Repudiation** | Actor denies performing an action and the system cannot prove otherwise | [Component name] | [1-5] | [1-5] | [L x I] | [Specific countermeasure] |
| **Information Disclosure** | Sensitive data is exposed to unauthorized parties through leaks, logs, or side channels | [Component name] | [1-5] | [1-5] | [L x I] | [Specific countermeasure] |
| **Denial of Service** | Attacker degrades or prevents legitimate access to the system through resource exhaustion or abuse | [Component name] | [1-5] | [1-5] | [L x I] | [Specific countermeasure] |
| **Elevation of Privilege** | Attacker gains higher access rights than authorized, bypassing access controls | [Component name] | [1-5] | [1-5] | [L x I] | [Specific countermeasure] |

**How to use this template:**
1. Draw or reference the system's data flow diagram (DFD) showing trust boundaries
2. For each component that crosses a trust boundary, enumerate threats in each STRIDE category
3. Score likelihood and impact independently, then calculate the risk score
4. Prioritize mitigations by risk score (highest first)
5. Record mitigations as architecture decisions (ADRs) or backlog items

### Risk Scoring Matrix

Risk Score = Likelihood x Impact. Use this matrix to classify threats.

| | Impact 1 (Negligible) | Impact 2 (Minor) | Impact 3 (Moderate) | Impact 4 (Major) | Impact 5 (Severe) |
|---|---|---|---|---|---|
| **Likelihood 5 (Almost Certain)** | 5 - Medium | 10 - High | 15 - Critical | 20 - Critical | 25 - Critical |
| **Likelihood 4 (Likely)** | 4 - Low | 8 - Medium | 12 - High | 16 - Critical | 20 - Critical |
| **Likelihood 3 (Possible)** | 3 - Low | 6 - Medium | 9 - High | 12 - High | 15 - Critical |
| **Likelihood 2 (Unlikely)** | 2 - Low | 4 - Low | 6 - Medium | 8 - Medium | 10 - High |
| **Likelihood 1 (Rare)** | 1 - Low | 2 - Low | 3 - Low | 4 - Low | 5 - Medium |

#### Risk Classification Thresholds

| Classification | Score Range | Required Action |
|---------------|-------------|----------------|
| Critical | 15-25 | Must mitigate before deployment; architecture change required |
| High | 9-14 | Must mitigate before production release; document accepted residual risk |
| Medium | 5-8 | Should mitigate; acceptable to defer with documented rationale and timeline |
| Low | 1-4 | Monitor and review; mitigate opportunistically |

### Threat Matrix Summary Format

Use this summary table to present the overall threat landscape to stakeholders after completing the STRIDE analysis.

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation | Highest Risk |
|-----------|----------|-----------|-------------|----------------|-----|-----------|-------------|
| [Component A] | [Risk Score] | [Risk Score] | [Risk Score] | [Risk Score] | [Risk Score] | [Risk Score] | [Max Score] |
| [Component B] | [Risk Score] | [Risk Score] | [Risk Score] | [Risk Score] | [Risk Score] | [Risk Score] | [Max Score] |

---

## Section 14: Capacity Modeling Template

This section provides templates for estimating resource requirements and defining scaling thresholds. Use these when a sprint contract requires capacity planning deliverables.

### Resource Estimation Table

Estimate resource needs per component. Fill in current load from measurements; project peak load from traffic analysis or business growth assumptions.

| Component | Metric | Current Load | Peak Load | Growth Rate (monthly) | Target Capacity | Headroom |
|-----------|--------|-------------|-----------|----------------------|----------------|----------|
| [API Gateway] | Requests/sec | [measured] | [projected] | [%] | [provisioned] | [% above peak] |
| [Application Tier] | CPU cores | [measured] | [projected] | [%] | [provisioned] | [% above peak] |
| [Application Tier] | Memory (GB) | [measured] | [projected] | [%] | [provisioned] | [% above peak] |
| [Database] | Connections | [measured] | [projected] | [%] | [provisioned] | [% above peak] |
| [Database] | Storage (GB) | [measured] | [projected] | [%] | [provisioned] | [% above peak] |
| [Cache Layer] | Hit rate (%) | [measured] | [target] | N/A | [provisioned] | N/A |
| [Message Queue] | Messages/sec | [measured] | [projected] | [%] | [provisioned] | [% above peak] |
| [Network] | Bandwidth (Mbps) | [measured] | [projected] | [%] | [provisioned] | [% above peak] |

**Headroom guidance:** Maintain a minimum of 30% headroom above projected peak load. For databases and stateful services, maintain 50% headroom to accommodate growth between scaling events.

### Scaling Thresholds and Triggers

Define the thresholds at which scaling actions are triggered. Each threshold should have both a warning level (alert and prepare) and a critical level (act immediately).

| Resource | Metric | Warning Threshold | Critical Threshold | Scaling Action | Cooldown Period |
|----------|--------|------------------|-------------------|----------------|----------------|
| [Compute] | CPU utilization | 60% sustained 5 min | 80% sustained 2 min | Add [N] instances (horizontal) | 5 minutes |
| [Compute] | Memory utilization | 70% sustained 5 min | 85% sustained 2 min | Add [N] instances (horizontal) | 5 minutes |
| [Database] | Connection pool usage | 70% of max | 90% of max | Increase pool size or add read replica | 15 minutes |
| [Database] | Storage usage | 75% of provisioned | 90% of provisioned | Expand storage volume | N/A (manual) |
| [Queue] | Queue depth | [N] messages pending | [N x 3] messages pending | Add [N] consumers | 3 minutes |
| [Network] | Bandwidth utilization | 60% of provisioned | 80% of provisioned | Upgrade bandwidth tier or add CDN | N/A (manual) |

### Horizontal vs Vertical Scaling Decision Criteria

| Factor | Horizontal (scale out) | Vertical (scale up) |
|--------|----------------------|-------------------|
| Application architecture | Stateless services, shared-nothing design | Stateful services, single-instance databases |
| Cost curve | Linear cost increase; cost-efficient at scale | Exponential cost increase at upper tiers |
| Failure impact | Loss of one instance is tolerable; others absorb load | Loss of the single instance is total failure |
| Scaling speed | Seconds to minutes (add instances to pool) | Minutes to hours (resize requires restart) |
| Upper bound | Limited by load balancer and coordination overhead | Limited by largest available instance type |
| Preferred for | Web servers, API gateways, workers, cache nodes | Databases (primary), in-memory stores, legacy applications |

### Load Projection Template

Use this table to project load growth and estimate when scaling actions will be needed.

| Month | Projected Users | Projected Requests/sec | Compute Needed | Storage Needed | Scaling Event Required |
|-------|----------------|----------------------|----------------|---------------|----------------------|
| Current | [N] | [N] | [N instances x size] | [N GB] | Baseline |
| +3 months | [N x growth] | [N x growth] | [estimate] | [estimate] | [Yes/No -- describe] |
| +6 months | [N x growth] | [N x growth] | [estimate] | [estimate] | [Yes/No -- describe] |
| +12 months | [N x growth] | [N x growth] | [estimate] | [estimate] | [Yes/No -- describe] |

**Cost estimation note:** For each scaling event row, include an estimated monthly cost delta so stakeholders can budget for infrastructure growth alongside feature development.
