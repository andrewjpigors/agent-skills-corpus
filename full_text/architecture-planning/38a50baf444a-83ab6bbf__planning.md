---
name: planning
metadata:
  compatible_agents:
    - claude-code
  tags:
    - architecture
    - planning
    - technical-spec
    - adr
    - roadmap
    - milestones
    - task-decomposition
description: >
  Comprehensive Planning & Architecture skill for the Software Development Life Cycle.
  Guides agents through architecture design, technology decisions, task decomposition,
  milestone planning, environment infrastructure, risk mitigation, and CI/CD pipeline design.
  Produces structured artifacts: technical specs, Architecture Decision Records (ADRs),
  roadmaps, task breakdowns, risk registers, and environment plans. Trigger phrases:
  "plan architecture", "write technical spec", "create ADR", "decompose tasks",
  "plan milestones", "architecture decision", "plan roadmap", "plan environment",
  "risk assessment", "CI/CD pipeline design", "technical planning", "sprint planning".
license: MIT
---

# Planning & Architecture

## Overview

This skill governs the **Planning & Architecture** phase of the SDLC. It produces structured, version-controlled artifacts that bridge product requirements and implementation. Every artifact follows a template, every decision is recorded, and every plan is traceable.

**Trigger when the user asks to:**
- Design system or module architecture
- Write a technical specification
- Create an Architecture Decision Record (ADR)
- Decompose epics into features and tasks
- Plan milestones or a delivery roadmap
- Plan environments and infrastructure
- Assess risks and define mitigations
- Design a CI/CD pipeline

**Announce at start:** "I'm using the planning skill to produce [artifact type]."

---

## Slash Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `/plan spec` | Generate a full technical specification | `docs/specs/<feature>-spec.md` |
| `/plan adr` | Create an Architecture Decision Record | `docs/adr/NNNN-<title>.md` |
| `/plan decompose` | Break epics into features → tasks with story points | `docs/plans/<epic>-breakdown.md` |
| `/plan roadmap` | Build a milestone-based delivery roadmap | `docs/plans/roadmap.md` |
| `/plan env` | Design environment & infrastructure topology | `docs/plans/environment-plan.md` |
| `/plan check` | Validate all planning artifacts for completeness | Console report |

---

## Technology Stack Reference

All technology decisions in this skill default to the following stack. Override only with explicit justification recorded in an ADR.

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
| JVM Container | bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl | CRaC + CDS, musl-based, minimal |

### Infrastructure

| Component | Version / Image | Notes |
|-----------|----------------|-------|
| Container Runtime | Docker / Podman | Rootless where possible |
| Reverse Proxy | nginx:stable-alpine | TLS termination, static assets |
| Database | PostgreSQL 16+ | Default RDBMS recommendation |
| CI/CD | GitHub Actions (default) | Swap via ADR if needed |

---

## Section 1: Architecture Design

### 1.1 Default Architecture: Modular Monolith

The default architectural pattern is a **modular monolith** with clear module boundaries, well-defined interfaces, and the ability to extract modules into separate services later.

**Structure:**

```
project-root/
├── app/                          # SolidJS + SolidStart frontend
│   ├── src/
│   │   ├── components/           # UI components (atomic design)
│   │   │   ├── atoms/
│   │   │   ├── molecules/
│   │   │   ├── organisms/
│   │   │   └── templates/
│   │   ├── routes/               # SolidStart file-based routing
│   │   ├── lib/                  # Shared utilities, composables
│   │   │   ├── api/              # API client layer
│   │   │   ├── stores/           # Signal-based state stores
│   │   │   └── utils/
│   │   ├── entry-client.tsx
│   │   └── entry-server.tsx
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── bunfig.toml
├── server/                       # Micronaut backend
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/<org>/<project>/
│   │   │   │   ├── module/       # Each module = bounded context
│   │   │   │   │   ├── user/
│   │   │   │   │   │   ├── controller/
│   │   │   │   │   │   ├── service/
│   │   │   │   │   │   ├── repository/
│   │   │   │   │   │   ├── model/
│   │   │   │   │   │   └── config/
│   │   │   │   │   ├── auth/
│   │   │   │   │   └── <domain>/
│   │   │   │   ├── shared/       # Cross-module shared code
│   │   │   │   │   ├── exception/
│   │   │   │   │   ├── dto/
│   │   │   │   │   ├── security/
│   │   │   │   │   └── config/
│   │   │   │   └── Application.java
│   │   │   └── resources/
│   │   │       ├── application.yml
│   │   │       └── db/migration/  # Flyway migrations
│   │   └── test/
│   │       └── java/
│   └── build.gradle.kts
├── infra/                        # Infrastructure definitions
│   ├── docker/
│   │   ├── Dockerfile.frontend
│   │   ├── Dockerfile.backend
│   │   └── docker-compose.yml
│   └── nginx/
│       └── nginx.conf
├── docs/
│   ├── adr/
│   ├── specs/
│   └── plans/
└── README.md
```

### 1.2 Architecture Decision Checklist

Before finalizing architecture, verify:

1. **Module boundaries** — Each module owns its data, exposes an API, and can be tested independently.
2. **Dependency direction** — Modules depend inward (shared kernel) never sideways. No cross-module direct repository access.
3. **API contract** — Frontend communicates with backend exclusively through REST/GraphQL endpoints. No shared database access.
4. **Database schema** — Each module owns its tables. Shared tables go through a shared kernel with explicit ownership.
5. **Error handling** — Module-specific exceptions map to shared error DTOs at the controller boundary.
6. **Testing strategy** — Each module has unit, integration, and contract test boundaries.
7. **Extraction path** — Any module can be extracted to a separate service by wrapping its API in HTTP. No distributed transactions.

### 1.3 Frontend Architecture Patterns

- **SolidStart file-based routing** — Routes live in `app/src/routes/`. Use `routeData` for data loading.
- **Signal-based state** — Use `createSignal`, `createMemo`, `createStore`. Avoid global mutable state. See solidjs-patterns skill.
- **API client layer** — Centralized in `app/src/lib/api/`. All API calls go through typed client functions. Never fetch directly in components.
- **Component hierarchy** — Atoms → Molecules → Organisms → Templates. Props flow down, events flow up.
- **TailwindCSS utility classes** — No custom CSS files. Use `@apply` sparingly in layout components only.
- **SSG by default** — Pre-render static pages. Use client-side data fetching for dynamic content.

### 1.4 Backend Architecture Patterns

- **Micronaut module structure** — Each module is a Java package with controller/service/repository/model layers.
- **Compile-time DI** — Use `@Singleton`, `@Requires`, `@Factory`. No runtime reflection.
- **Virtual threads** — Use `@ExecuteOn(TaskExecutors.VIRTUAL)` for I/O-bound operations.
- **Flyway migrations** — Versioned SQL migrations in `resources/db/migration/`. Never modify a committed migration.
- **Configuration** — `application.yml` for defaults. Environment variables for overrides. Use Micronaut `@Value` and `@ConfigurationProperties`.
- **API versioning** — Prefix all endpoints with `/api/v1/`. Plan for version headers if needed.

---

## Section 2: Technology Decisions

### 2.1 Decision Framework

Every technology choice must be justified against these criteria:

| Criterion | Weight | Questions |
|-----------|--------|-----------|
| Fit for purpose | High | Does it solve the actual problem? Is it the right level of abstraction? |
| Team capability | High | Can the team use it effectively? Is the learning curve justified? |
| Ecosystem maturity | Medium | Is it actively maintained? Does it have good documentation and community? |
| Operational impact | Medium | What's the deployment complexity? Monitoring? Debugging story? |
| Long-term viability | Medium | Is it backed by a foundation or major vendor? What's the bus factor? |
| Performance | Low-Medium | Does it meet SLA requirements? At what cost? |
| License | Hard gate | Must be compatible with project license. No AGPL without explicit approval. |

### 2.2 Stack Decision Matrix

Record technology decisions in ADRs. The following are the defaults — override only with a written ADR:

| Decision | Default | Alternative (requires ADR) |
|----------|---------|---------------------------|
| Frontend framework | SolidJS 1.9+ | React, Vue, Svelte |
| Frontend runtime | Bun 1.2+ | Node.js 22+, Deno 2.x |
| Frontend meta-framework | SolidStart (SSG) | Vite SSR, custom |
| CSS approach | TailwindCSS 4.1+ | CSS Modules, Vanilla Extract |
| Backend language | Java 21 | Kotlin, GraalVM native |
| Backend framework | Micronaut 4.7+ | Spring Boot 3.x, Quarkus |
| Build tool | Gradle 8.13+ (Kotlin DSL) | Maven |
| Database | PostgreSQL 16+ | MySQL, MariaDB, CockroachDB |
| ORM/Data access | Micronaut Data | jOOQ, MyBatis, raw JDBC |
| Migrations | Flyway | Liquibase |
| API style | REST + JSON | GraphQL, gRPC |
| Auth | JWT + refresh tokens | Session-based, OAuth2-only |
| Container runtime | Docker / Podman | N/A |
| Reverse proxy | nginx:stable-alpine | Caddy, Traefik |
| CI/CD | GitHub Actions | GitLab CI, Jenkins, CircleCI |

### 2.3 ADR Creation Workflow

1. Identify the decision point (what needs to be decided and why now).
2. Gather context: requirements, constraints, existing systems.
3. List alternatives with pros/cons using the decision framework criteria.
4. Select an option and document the rationale.
5. Document consequences (both positive and negative).
6. Save as `docs/adr/NNNN-<kebab-case-title>.md` using the ADR template.
7. Commit with message: `docs: add ADR NNNN - <title>`.

**ADR numbering:** Zero-padded, sequential. Check `docs/adr/` for the next number.

---

## Section 3: Task Decomposition

### 3.1 Decomposition Hierarchy

```
Epic
 └── Feature
      └── Task (story point estimate)
           └── Sub-task (optional, no estimate — rolls up to task)
```

### 3.2 Decomposition Process

**Step 1: Start with the Epic**

An epic is a large body of work that delivers significant user value. It should be expressible in one sentence: "As a [user], I want [outcome] so that [benefit]."

**Step 2: Break into Features**

A feature is a testable, deliverable slice of an epic. It can be deployed independently (even if behind a feature flag). Each feature should be completable within 1-3 development days.

For each feature, define:
- **User story** — Who, what, why.
- **Acceptance criteria** — Given/When/Then format. All must be testable.
- **Dependencies** — What must be done first (other features, infrastructure, data).
- **Risk** — What could go wrong and how likely it is.

**Step 3: Break Features into Tasks**

A task is a discrete unit of development work completable in a single focused session (1-4 hours). Each task produces a testable change.

Task template:
```
- [ ] TASK-XXX: <imperative description>
  - Files: list of files to create/modify
  - Estimate: <story points>
  - Depends on: TASK-YYY (if any)
  - Test: how to verify completion
```

**Step 4: Estimate with Story Points**

Use Fibonacci sequence: 1, 2, 3, 5, 8, 13, 21.

| Points | Meaning | Guideline |
|--------|---------|-----------|
| 1 | Trivial | Config change, typo fix, simple CSS |
| 2 | Simple | Small component, straightforward API endpoint |
| 3 | Moderate | Feature with 2-3 files, some logic |
| 5 | Complex | Cross-cutting feature, new module interaction |
| 8 | Significant | New module, complex integration, schema design |
| 13 | Large | Multi-module feature, architectural change |
| 21 | Epic-level | Break it down further |

### 3.3 Decomposition Rules

1. **Every task is testable** — If you can't write a test for it, split it further.
2. **Every task has exact file paths** — No ambiguous "update relevant files."
3. **Every task has a commit** — Each task ends with a specific git commit.
4. **Dependencies are explicit** — Tasks that must be sequential are marked.
5. **No task exceeds 13 points** — If a task is 13+, decompose further.
6. **Backend tasks include migration** — Database tasks include the Flyway migration file.
7. **Frontend tasks include types** — TypeScript tasks include type definitions.
8. **Cross-cutting concerns are separate tasks** — Auth, logging, error handling get their own tasks.

### 3.4 Dependency Mapping

After decomposition, produce a dependency graph:

```
TASK-001 (schema migration)
  └── TASK-002 (repository layer)
       ├── TASK-003 (service layer)
       │    └── TASK-004 (controller)
       │         └── TASK-005 (integration test)
       └── TASK-006 (frontend API client)
            └── TASK-007 (UI component)
                 └── TASK-008 (E2E test)
```

Identify the critical path. Highlight tasks that can run in parallel.

---

## Section 4: Milestone Planning

### 4.1 Milestone Structure

```
M0: Foundation         ← Project scaffolding, CI/CD, dev environment
M1: Core MVP           ← Minimum viable product, end-to-end happy path
M2: Feature Complete   ← All planned features, edge cases, error handling
M3: Hardening          ← Performance, security, accessibility, observability
M4: Launch Ready       ← Staging validation, load testing, runbook, documentation
```

### 4.2 Milestone Definition

For each milestone, document:

```markdown
## Milestone Mn: <Name>

**Goal:** <one sentence>

**Exit Criteria:** (ALL must be met)
- [ ] <measurable criterion 1>
- [ ] <measurable criterion 2>
- [ ] All tasks in milestone completed and merged
- [ ] All tests passing in CI
- [ ] Zero critical/high bugs
- [ ] <demo/deploy/review requirement>

**Scope:**
- Feature A
- Feature B

**Explicitly Out of Scope:**
- Feature C (deferred to Mn+1)

**Estimated Effort:** <total story points>

**Risk Buffer:** 20% of estimated effort reserved for unknowns

**Key Dependencies:**
- External API access
- Design assets
- Third-party licenses
```

### 4.3 MVP Planning (M1)

The MVP must demonstrate the core value proposition end-to-end. Apply these filters:

1. **User can complete the primary workflow** — End-to-end, not just a slice.
2. **Data persists** — Database is real, not mocked.
3. **Auth works** — At least basic authentication.
4. **Deployable** — Can be deployed to a real environment.
5. **Observable** — Logs and basic health checks work.

**What to defer from MVP:**
- Edge cases and error recovery polish
- Advanced features and settings
- Performance optimization (beyond "acceptable")
- Comprehensive accessibility
- Admin interfaces
- Email notifications
- Analytics dashboards

### 4.4 Incremental Delivery

After MVP, deliver features incrementally. Each increment must:

1. Be deployable independently.
2. Add measurable user value.
3. Include its own tests and documentation.
4. Not break existing functionality (backward compatible).

**Release cadence:** Target 1-2 week increments. Each increment maps to 1-2 milestones worth of tasks.

### 4.5 Velocity Tracking

Track story points per increment to establish velocity:

```
Increment 1: 34 points (planned) → 41 points (actual) → 1.2x multiplier
Increment 2: 40 points (planned) → 38 points (actual) → 0.95x multiplier
Running average: 1.08x multiplier → apply to future estimates
```

---

## Section 5: Environment & Infrastructure Planning

### 5.1 Environment Tiers

| Environment | Purpose | Data | Deployment | Access |
|-------------|---------|------|------------|--------|
| **local** | Developer workstation | Seeded/mocked | Manual (`docker compose up`) | localhost |
| **CI** | Automated testing | Ephemeral | Per PR / per commit | Internal only |
| **staging** | Pre-production validation | Production-like (anonymized) | On merge to main | Team + stakeholders |
| **production** | Live users | Real | On tag / release | Public |

### 5.2 Local Development Environment

```yaml
# docker-compose.yml (development)
services:
  frontend:
    build:
      context: ./app
      dockerfile: ../infra/docker/Dockerfile.frontend
      target: dev
    ports:
      - "3000:3000"
    volumes:
      - ./app/src:/app/src
    environment:
      - API_URL=http://localhost:8080

  backend:
    build:
      context: ./server
      dockerfile: ../infra/docker/Dockerfile.backend
      target: dev
    ports:
      - "8080:8080"
    volumes:
      - ./server/src:/app/src
    environment:
      - DATABASE_HOST=postgres
      - DATABASE_PORT=5432
      - DATABASE_NAME=app_dev
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: app_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### 5.3 Container Build Strategy

**Frontend Dockerfile stages:**

| Stage | Purpose | Base Image |
|-------|---------|------------|
| `dev` | Hot-reload development | `oven/bun:1` |
| `build` | Compile and bundle | `oven/bun:1` |
| `production` | Serve static assets | `nginx:stable-alpine` |

**Backend Dockerfile stages:**

| Stage | Purpose | Base Image |
|-------|---------|------------|
| `dev` | Hot-reload development | `bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl` |
| `build` | Compile with Gradle | `bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl` |
| `production` | Run optimized JAR | `bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl` |

**Production optimizations:**
- CRaC (Coordinated Restore at Checkpoint) for fast startup
- CDS (Class Data Sharing) for reduced warmup
- musl-based for minimal image size
- Multi-stage build to exclude build tooling

### 5.4 nginx Configuration Plan

```
nginx responsibilities:
├── TLS termination (production)
├── Static asset serving (frontend build output)
├── Reverse proxy /api/* → backend:8080
├── Gzip compression
├── Security headers
│   ├── X-Frame-Options: DENY
│   ├── X-Content-Type-Options: nosniff
│   ├── X-XSS-Protection: 1; mode=block
│   ├── Referrer-Policy: strict-origin-when-cross-origin
│   └── Content-Security-Policy: <configured per environment>
├── Cache headers
│   ├── /assets/* → immutable, 1 year
│   └── /index.html → no-cache
└── Health check endpoint → 200 OK
```

### 5.5 Database Planning

| Decision | Default | Notes |
|----------|---------|-------|
| RDBMS | PostgreSQL 16+ | Default recommendation |
| Schema management | Flyway | Versioned migrations, repeatable migrations |
| Naming convention | snake_case | Tables, columns, indexes |
| Connection pooling | HikariCP (via Micronaut) | Configure pool size per environment |
| Migrations location | `server/src/main/resources/db/migration/` | Follow Flyway conventions |
| Migration naming | `V{version}__{description}.sql` | Double underscore, descriptive |
| Seed data | `R__seed_data.sql` | Repeatable migration, dev/staging only |
| Backup strategy | pg_dump daily + WAL archiving | Production. Point-in-time recovery. |
| Index strategy | Add indexes with migrations | Never add without measuring query plans |

### 5.6 Secrets Management

| Environment | Approach |
|-------------|----------|
| local | `.env` file (git-ignored), docker-compose environment |
| CI | Repository secrets (GitHub Actions encrypted secrets) |
| staging | Environment secrets + vault (if available) |
| production | Dedicated secrets manager (HashiCorp Vault, AWS Secrets Manager, etc.) |

**Rules:**
- Never commit secrets to the repository.
- Never log secrets at any log level.
- Use environment variable injection for all configuration.
- Rotate secrets on a schedule (quarterly minimum for production).

---

## Section 6: Risk Planning and Mitigation

### 6.1 Risk Identification Framework

For each risk, assess:

| Dimension | Scale | Meaning |
|-----------|-------|---------|
| **Likelihood** | 1-5 | 1=rare, 2=unlikely, 3=possible, 4=likely, 5=almost certain |
| **Impact** | 1-5 | 1=trivial, 2=minor, 3=moderate, 4=major, 5=critical |
| **Risk Score** | L × I | Prioritize by score |

### 6.2 Common Risk Categories

| Category | Examples |
|----------|----------|
| **Technical** | Technology unfamiliarity, performance bottlenecks, integration failures |
| **Architectural** | Module coupling, schema migration issues, API breaking changes |
| **Infrastructure** | Environment downtime, deployment failures, scaling limits |
| **Security** | Authentication bypass, data leaks, dependency vulnerabilities |
| **Schedule** | Underestimated complexity, blocked dependencies, scope creep |
| **Team** | Knowledge silos, bus factor, onboarding friction |
| **External** | Third-party API changes, license changes, regulatory requirements |

### 6.3 Risk Register Template

For each identified risk:

```markdown
### RISK-NNN: <title>

- **Category:** <Technical|Architectural|Infrastructure|Security|Schedule|Team|External>
- **Likelihood:** <1-5>
- **Impact:** <1-5>
- **Risk Score:** <L × I>
- **Status:** <Open|Mitigating|Accepted|Closed>
- **Trigger:** <What indicates this risk is materializing>
- **Mitigation:** <Action to reduce likelihood or impact>
- **Contingency:** <Action if risk materializes despite mitigation>
- **Owner:** <Role responsible for monitoring>
- **Review Date:** <When to reassess>
```

### 6.4 Risk Response Strategies

| Strategy | When to Use | Action |
|----------|-------------|--------|
| **Avoid** | High risk, high impact | Change plan to eliminate the risk |
| **Mitigate** | Moderate risk | Reduce likelihood or impact through proactive action |
| **Transfer** | External risk | Shift to third party (insurance, SLA, outsourcing) |
| **Accept** | Low risk, low impact | Document and monitor. No proactive action needed |

### 6.5 Technical Risk Mitigations (Common)

| Risk | Mitigation |
|------|------------|
| SolidJS unfamiliarity | Spike task first. Pair with solidjs-patterns skill. |
| Database migration failures | Test migrations on staging with production-like data. Never modify committed migrations. |
| Performance unknowns | Define SLA targets early. Load test in M4. Profile in development. |
| Dependency vulnerabilities | Automated dependency scanning in CI (Dependabot/Renovate). |
| Integration failures | Contract tests. Mock external APIs in development. Integration test suite in CI. |
| Scope creep | Strict milestone exit criteria. New scope goes to backlog, not current milestone. |

---

## Section 7: CI/CD Pipeline Design

### 7.1 Pipeline Stages

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│   Source     │───▶│   Build      │───▶│    Test       │───▶│   Deploy     │
│             │    │              │    │               │    │              │
│ • PR opened │    │ • Frontend   │    │ • Lint        │    │ • Staging:   │
│ • Push to   │    │   (bun build)│    │ • Unit tests  │    │   on merge   │
│   main      │    │ • Backend    │    │ • Integration │    │ • Production:│
│ • Tag       │    │   (gradle    │    │   tests       │    │   on tag     │
│             │    │    build)    │    │ • E2E tests   │    │              │
│             │    │ • Docker     │    │ • Security    │    │              │
│             │    │   images     │    │   scan        │    │              │
└─────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
```

### 7.2 Pipeline Configuration

**PR Pipeline (on pull request):**

```yaml
name: PR Check
on: pull_request

jobs:
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest
      - working-directory: app
        run: bun install --frozen-lockfile
      - working-directory: app
        run: bun run typecheck
      - working-directory: app
        run: bun run lint
      - working-directory: app
        run: bun run test
      - working-directory: app
        run: bun run build

  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: app_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: liberica
          java-version: 21
      - working-directory: server
        run: ./gradlew check
      - working-directory: server
        run: ./gradlew integrationTest

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - working-directory: app
        run: npx audit-ci --moderate
      - working-directory: server
        run: ./gradlew dependencyCheckAnalyze
```

**Deploy Pipeline (on merge to main):**

```yaml
name: Deploy
on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build-and-push:
    # Build Docker images, push to registry
    # Deploy to staging on main push
    # Deploy to production on tag push
```

### 7.3 Pipeline Quality Gates

Every merge to main must pass:

| Gate | Requirement | Blocking |
|------|-------------|----------|
| Type check | `tsc --noEmit` passes | Yes |
| Lint | Zero warnings (strict) | Yes |
| Unit tests | 100% pass rate | Yes |
| Integration tests | 100% pass rate | Yes |
| Code coverage | ≥ 80% line coverage (new code) | Configurable |
| Security scan | No critical/high vulnerabilities | Yes |
| Build | Docker images build successfully | Yes |
| Database migration | Migrations apply cleanly on test DB | Yes |

### 7.4 Deployment Strategy

| Environment | Strategy | Rollback |
|-------------|----------|----------|
| staging | Rolling update | Redeploy previous image |
| production | Blue-green or canary | Instant traffic switch to previous version |

**Production deployment checklist:**
- [ ] All CI gates pass
- [ ] Staging validation complete
- [ ] Database migrations tested on staging with production-like data
- [ ] Runbook updated for new features
- [ ] Monitoring alerts configured
- [ ] Rollback procedure documented and tested

### 7.5 Branch Strategy

```
main ──────────────────────────────────────────────▶
  │                                           │
  ├── feature/TASK-XXX-short-description ─────┤  (PR → squash merge)
  ├── fix/TASK-XXX-short-description ─────────┤  (PR → squash merge)
  │                                           │
  └── v1.0.0 (tag) ─── release/1.0 (if needed)
```

**Rules:**
- `main` is always deployable.
- All changes via PR. Minimum one approval required.
- Squash merge to keep history clean.
- Feature branches named `feature/TASK-XXX-description`.
- Fix branches named `fix/TASK-XXX-description`.
- Tags trigger production deployment.

---

## Section 8: Planning Validation (`/plan check`)

### 8.1 Completeness Checklist

Run this validation against all planning artifacts before moving to implementation:

```markdown
## Planning Completeness Check

### Architecture
- [ ] Architecture diagram exists and reflects actual planned structure
- [ ] Module boundaries are defined with clear responsibilities
- [ ] Data flow is documented (frontend → API → backend → database)
- [ ] All ADRs are filed for non-default technology choices
- [ ] Frontend-backend API contract is sketched

### Technical Specification
- [ ] Feature scope is bounded with explicit in/out lists
- [ ] Acceptance criteria are testable (Given/When/Then)
- [ ] Non-functional requirements are quantified (latency, throughput, availability)
- [ ] Security requirements are addressed
- [ ] Error handling strategy is defined

### Task Breakdown
- [ ] All epics are decomposed into features
- [ ] All features are decomposed into tasks
- [ ] Every task has story point estimate
- [ ] Every task has exact file paths
- [ ] Dependencies are mapped (critical path identified)
- [ ] No task exceeds 13 story points
- [ ] Parallelizable tasks are identified

### Milestone Planning
- [ ] Milestones have clear exit criteria
- [ ] MVP scope is defined and minimal
- [ ] Risk buffer is included (20%)
- [ ] Increment delivery plan exists

### Environment & Infrastructure
- [ ] All environment tiers are defined
- [ ] Docker Compose configuration covers local development
- [ ] Database migration strategy is defined
- [ ] Secrets management approach is specified per environment
- [ ] nginx configuration is planned

### Risk Management
- [ ] Risk register is populated
- [ ] Top 5 risks have mitigations
- [ ] Contingency plans exist for high-score risks
- [ ] Risk owners are assigned

### CI/CD
- [ ] Pipeline stages are defined
- [ ] Quality gates are specified
- [ ] Deployment strategy is defined per environment
- [ ] Rollback procedures are documented
- [ ] Branch strategy is agreed

### Documentation
- [ ] All planning artifacts are committed to the repository
- [ ] README reflects current project state
- [ ] ADR index is up to date
```

### 8.2 Artifact Inventory

| Artifact | Location | Format |
|----------|----------|--------|
| Technical Specification | `docs/specs/<feature>-spec.md` | Markdown (template) |
| Architecture Decision Record | `docs/adr/NNNN-<title>.md` | Markdown (template) |
| ADR Index | `docs/adr/README.md` | Markdown |
| Task Breakdown | `docs/plans/<epic>-breakdown.md` | Markdown (template) |
| Roadmap | `docs/plans/roadmap.md` | Markdown (template) |
| Environment Plan | `docs/plans/environment-plan.md` | Markdown |
| Risk Register | `docs/plans/risk-register.md` | Markdown (template) |
| Docker Compose | `infra/docker/docker-compose.yml` | YAML |
| nginx Config | `infra/nginx/nginx.conf` | Nginx config |
| CI Pipeline | `.github/workflows/` | YAML |

---

## Section 9: Reference Files

| Reference File | Purpose | Slash Command |
|---------------|---------|---------------|
| `references/technical-spec-template.md` | Template for writing technical specifications | `/plan spec` |
| `references/adr-template.md` | Template for Architecture Decision Records | `/plan adr` |
| `references/roadmap-template.md` | Template for milestone-based roadmaps | `/plan roadmap` |
| `references/risk-register-template.md` | Template for risk identification and tracking | `/plan check` |
| `references/task-breakdown-template.md` | Template for epic → feature → task decomposition | `/plan decompose` |
