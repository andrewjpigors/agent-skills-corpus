---
name: "review"
tags: [code-review, pr, linting, quality, tech-debt, conventions, eslint, detekt]
description: |
  Agentic skill for the "Code Review & Collaboration" phase of the SDLC.
  Provides structured code review workflows, automated quality gates,
  convention audits, technical debt management, and PR review checklists
  for SolidJS + TypeScript (frontend) and Micronaut + Java 21 (backend)
  projects.

  Trigger phrases:
    - "review code"
    - "review PR"
    - "run lint"
    - "check quality"
    - "tech debt"
    - "convention audit"
    - "code review checklist"
license: MIT
---

# Code Review & Collaboration

This skill governs the **Code Review & Collaboration** phase of the SDLC. It enforces quality gates, convention compliance, and structured review workflows across the full-stack architecture:

- **Frontend**: Bun + TypeScript + SolidJS + SolidStart + TailwindCSS 4 + Iconify
- **Backend**: Java 21 + Micronaut 4 + Gradle Kotlin DSL + Shadow JAR

**Trigger when the user asks to:**
- Review code, a pull request, or a diff
- Run linters or format checks
- Audit code against project conventions
- Identify or manage technical debt
- Generate a code review checklist

**Announce at start:** "I'm using the review skill to [review type]."

---

## Commands

| Command | Description |
|---|---|
| `/review pr` | Full pull request review with checklist |
| `/review frontend` | Review frontend code against SolidJS + TailwindCSS conventions |
| `/review backend` | Review backend code against Micronaut + Java 21 conventions |
| `/review lint` | Run all linters and fix issues |
| `/review debt` | Identify and categorize technical debt |
| `/review check` | Full convention audit report |

---

## General Review Checklist

Apply to **all** code regardless of layer. Every item must be verified before approving a review.

```
General Review Checklist
════════════════════════

Security:
  [ ] No hardcoded secrets, API keys, passwords, or tokens
  [ ] No sensitive data in logs, error messages, or client-side code
  [ ] No .env files or credentials committed to version control
  [ ] Input validation on all user-supplied data
  [ ] Output encoding to prevent injection (XSS, SQLi, command injection)
  [ ] Dependencies audited for known vulnerabilities

Error Handling:
  [ ] All error paths have meaningful error messages
  [ ] No swallowed exceptions (empty catch blocks)
  [ ] No bare `catch (Exception e)` without re-throw or specific handling
  [ ] Error responses follow RFC 7807 format (backend)
  [ ] User-facing errors are friendly, not technical stack traces
  [ ] Async operations have proper error boundaries (frontend)

Edge Cases:
  [ ] Null / undefined / empty string handled
  [ ] Empty collections / arrays handled
  [ ] Boundary conditions (off-by-one, overflow, underflow)
  [ ] Concurrent access patterns safe (backend)
  [ ] Race conditions in reactive chains (frontend signals/resources)

Complexity:
  [ ] No unnecessary complexity (YAGNI)
  [ ] Functions / methods are < 30 lines
  [ ] Files are < 300 lines (excluding generated code)
  [ ] Cyclomatic complexity < 10 per function
  [ ] No deep nesting (> 3 levels) — extract early returns or helper functions
  [ ] No copy-pasted code — extract shared utilities

Naming & Readability:
  [ ] Variables, functions, classes have descriptive names
  [ ] No single-letter variables (except loop counters i, j, k)
  [ ] No abbreviations unless domain-standard (e.g., DTO, DAO, URL)
  [ ] Boolean variables read as assertions (isLoading, hasPermission, canEdit)
  [ ] Comments explain "why", not "what" — code should be self-documenting

Testing:
  [ ] New code has corresponding tests
  [ ] Tests cover happy path + error paths + edge cases
  [ ] No skipped or commented-out tests without a linked issue
  [ ] Test names are descriptive (should/when/then pattern)
  [ ] Mocks are not over-used — prefer real implementations where feasible
```

---

## Command: `/review pr`

Full pull request review combining all checklists, automated quality gates, and PR process compliance.

### Instructions

1. **Gather context**: Identify the PR number or branch. Read the PR description, changed files, and diff.

2. **Run automated quality gates** (see Automated Quality Gates section). Record all failures.

3. **Apply layer-specific checklist**:
   - For `.ts` / `.tsx` files → Frontend Review Checklist
   - For `.java` files → Backend Review Checklist
   - For config / infra files → General Review Checklist

4. **Check PR process compliance**:
   - Conventional commit messages
   - PR description links to issue / ticket
   - No merge conflicts
   - CI pipeline green
   - Required approvals present

5. **Generate review report** using the template below.

### PR Review Report Template

```markdown
## PR Review: #[number] — [title]

**Author:** @author
**Branch:** feature/xxx → main
**Files changed:** N files (+N / -N lines)

### Automated Quality Gates

| Gate | Status |
|------|--------|
| Frontend: typecheck | PASS / FAIL |
| Frontend: lint | PASS / FAIL |
| Frontend: format | PASS / FAIL |
| Frontend: test | PASS / FAIL |
| Backend: check | PASS / FAIL |
| Backend: detekt | PASS / FAIL |
| Backend: dependencyCheck | PASS / FAIL |
| Backend: test | PASS / FAIL |

### Findings

| # | Severity | File | Line | Finding | Suggestion |
|---|----------|------|------|---------|------------|
| 1 | BLOCKER | | | | |
| 2 | MAJOR | | | | |
| 3 | MINOR | | | | |
| 4 | INFO | | | | |

### Convention Compliance

- [ ] Conventional commits used
- [ ] Frontend conventions followed
- [ ] Backend conventions followed
- [ ] No hardcoded secrets
- [ ] Tests adequate

### Verdict

- [ ] **APPROVE** — Ready to merge
- [ ] **REQUEST CHANGES** — Blockers must be fixed
- [ ] **COMMENT** — Non-blocking suggestions
```

### Severity Levels

| Severity | Meaning | Blocks Merge? |
|----------|---------|---------------|
| **BLOCKER** | Security vulnerability, data loss risk, broken functionality | Yes |
| **MAJOR** | Convention violation, missing error handling, poor test coverage | Yes |
| **MINOR** | Style issue, naming improvement, minor optimization | No |
| **INFO** | Suggestion, alternative approach, future consideration | No |

---

## Command: `/review frontend`

Review frontend code against SolidJS + TypeScript + TailwindCSS conventions.

### Frontend Review Checklist

```
Frontend Review Checklist (SolidJS + TypeScript + TailwindCSS 4)
════════════════════════════════════════════════════════════════

TypeScript:
  [ ] strict: true in tsconfig.json
  [ ] No `any` types — use `unknown` + type narrowing
  [ ] No `@ts-ignore` or `@ts-expect-error` without documented reason
  [ ] Interfaces for props, type aliases for unions/intersections
  [ ] Explicit return types on exported functions
  [ ] `satisfies` used for type checking without widening
  [ ] No non-null assertions (!) without guaranteed safety

SolidJS Reactivity:
  [ ] Props accessed as `props.x` — NEVER destructured
  [ ] Signals called as functions: `count()` not `count`
  [ ] No signal values captured in non-reactive closures
  [ ] createMemo for derived state — no computation in render body
  [ ] createEffect only for side effects, not data fetching
  [ ] createResource for async data loading
  [ ] Stores use createStore for complex nested state
  [ ] onCleanup used for event listeners, intervals, subscriptions
  [ ] No `let` bindings for DOM references — use refs properly
  [ ] <Show> for conditional rendering, not ternary chains in JSX
  [ ] <For> for list rendering with keyed access, not .map()

Component Structure:
  [ ] Named exports (no default exports for components)
  [ ] Props defined as typed interface
  [ ] Component type: `Component<Props>` or explicit function signature
  [ ] File naming: PascalCase for components (UserProfile.tsx)
  [ ] Directory structure: src/components/{group}/ComponentName.tsx
  [ ] Barrel re-exports in index.ts files
  [ ] Import order: solid-js → @solidjs/* → @iconify-icon/* → local → CSS

TailwindCSS 4:
  [ ] CSS-first config: @import "tailwindcss" (not @tailwind directives)
  [ ] Custom theme via @theme {} in CSS (not tailwind.config.js)
  [ ] No inline styles — use Tailwind utilities
  [ ] No arbitrary values where design tokens exist
  [ ] Color tokens: primary-50 through primary-900 (oklch)
  [ ] Responsive: mobile-first (base → sm → md → lg → xl)
  [ ] Class sorting: Prettier with prettier-plugin-tailwindcss applied
  [ ] No duplicate/conflicting utility classes

Accessibility:
  [ ] All images have alt text (or alt="" for decorative)
  [ ] Form inputs have associated labels (not placeholder-only)
  [ ] Interactive elements are keyboard accessible
  [ ] ARIA attributes correct and not redundant with semantic HTML
  [ ] Color contrast meets WCAG 2.2 AA (4.5:1 normal, 3:1 large)
  [ ] aria-label on icon-only buttons
  [ ] role attribute only when semantic HTML insufficient
  [ ] Focus management for modals, dialogs, and dynamic content
  [ ] prefers-reduced-motion respected for animations

SolidStart Routing:
  [ ] Route files in src/routes/ follow file-based naming
  [ ] Dynamic routes use [param] syntax
  [ ] Catch-all routes use [...slug] syntax
  [ ] Route components use <Title> from @solidjs/meta
  [ ] Data loading via createResource (not createEffect + fetch)
  [ ] Suspense boundaries wrap async content
  [ ] Error boundaries for failed data fetching

Performance:
  [ ] No unnecessary re-renders (SolidJS fine-grained — verify signal scope)
  [ ] Large lists use virtualization if > 100 items
  [ ] Images lazy-loaded where appropriate
  [ ] No unnecessary createEffect (prefer createMemo for derivations)
  [ ] Bundle size: no full library imports (use specific imports)
```

### Common Frontend Anti-Patterns

```tsx
// ❌ WRONG: Destructuring props breaks reactivity
const { name, age } = props;
return <div>{name}</div>;

// ✅ CORRECT: Access props directly
return <div>{props.name}</div>;

// ❌ WRONG: Using signal without calling it
const [count, setCount] = createSignal(0);
console.log(count); // logs the signal function, not the value

// ✅ CORRECT: Call signal as function
console.log(count()); // logs the current value

// ❌ WRONG: Computing in render body (re-runs every render)
const sorted = items().sort((a, b) => a.name.localeCompare(b.name));

// ✅ CORRECT: Use createMemo for derived state
const sorted = createMemo(() =>
  [...items()].sort((a, b) => a.name.localeCompare(b.name))
);

// ❌ WRONG: Using .map() for reactive lists
{items().map(item => <div>{item.name}</div>)}

// ✅ CORRECT: Use <For> for reactive list rendering
<For each={items()}>
  {(item) => <div>{item.name}</div>}
</For>

// ❌ WRONG: Inline styles
<div style={{ backgroundColor: "#3b82f6", padding: "16px" }}>

// ✅ CORRECT: Tailwind utilities
<div class="bg-blue-500 p-4">

// ❌ WRONG: Old Tailwind v3 directives
@tailwind base;
@tailwind components;
@tailwind utilities;

// ✅ CORRECT: Tailwind v4 import
@import "tailwindcss";
```

---

## Command: `/review backend`

Review backend code against Micronaut + Java 21 conventions.

### Backend Review Checklist

```
Backend Review Checklist (Micronaut 4 + Java 21)
══════════════════════════════════════════════════

Annotations:
  [ ] @Serdeable on all DTO records
  [ ] @Validated on all controller classes
  [ ] @Valid on @Body parameters in controller methods
  [ ] @Singleton on service classes (not @Component)
  [ ] @Produces on exception handler classes
  [ ] No @Inject on fields — constructor injection only
  [ ] Correct Micronaut annotations (not Spring annotations)

Dependency Injection:
  [ ] Constructor injection (no field injection)
  [ ] Constructor parameters are `final` fields
  [ ] No circular dependencies
  [ ] Beans scoped appropriately (@Singleton, @Prototype, @RequestScope)

Controller Layer:
  [ ] No business logic in controllers — only delegation
  [ ] No repository / direct data access in controllers
  [ ] All responses wrapped in HttpResponse<T>
  [ ] Correct HTTP status codes:
      - 200 OK for GET and PUT
      - 201 Created for POST (with Location header)
      - 204 No Content for DELETE
      - 400 Bad Request for validation errors
      - 404 Not Found for missing resources
      - 409 Conflict for duplicate/state conflicts
      - 500 Internal Server Error for unhandled exceptions
  [ ] @Status annotations match return type
  [ ] API versioning: /api/v1/ prefix on all endpoints
  [ ] Pagination support on list endpoints

Service Layer:
  [ ] Business logic lives in services, not controllers
  [ ] Domain exceptions thrown (ResourceNotFoundException, ValidationException)
  [ ] Transaction boundaries correct (@Transactional where needed)
  [ ] No HttpResponse construction in services — controllers handle HTTP
  [ ] Service methods return domain objects / DTOs, not HttpResponse

Java 21 Features:
  [ ] Records for all DTOs (no Lombok, no mutable classes)
  [ ] Sealed interfaces for domain modeling where applicable
  [ ] Pattern matching for switch (arrow syntax)
  [ ] Pattern matching for instanceof
  [ ] var for local variable type inference
  [ ] .formatted() for string formatting (not String.format)
  [ ] .toList() for stream terminal operation (not .collect(Collectors.toList()))
  [ ] Compact constructors for record validation

Error Handling:
  [ ] Custom exception classes extend RuntimeException
  [ ] Exception handlers implement ExceptionHandler<E, HttpResponse<ErrorResponse>>
  [ ] GlobalExceptionHandler catches all unhandled exceptions
  [ ] Error response follows RFC 7807 format:
      { status, title, detail, instance }
  [ ] No stack traces in error responses
  [ ] No sensitive data leaked in error messages
  [ ] Proper HTTP status mapping per exception type

Build & Configuration:
  [ ] build.gradle.kts uses Kotlin DSL
  [ ] --enable-preview in JavaCompile, JavaExec, and Test tasks
  [ ] Micronaut AOT configured (optimizeServiceLoading, convertYamlToJava, etc.)
  [ ] Shadow JAR plugin applied
  [ ] Dockerfile uses bellsoft/liberica-runtime-container base image
  [ ] JVM flags: --enable-preview -XX:+UseCompactObjectHeaders
  [ ] Health check configured in Dockerfile

Import Order:
  [ ] Package declaration
  [ ] java.* (standard library)
  [ ] jakarta.* (validation, inject)
  [ ] io.micronaut.* (framework)
  [ ] com.example.* (project)
  [ ] Blank line between groups

Data Layer:
  [ ] Repository interfaces extend CrudRepository / PageableRepository
  [ ] @JdbcRepository with correct Dialect
  [ ] Entity classes use @MappedEntity, @AutoPopulated, @DateCreated, @DateUpdated
  [ ] Custom queries use @Query annotation with parameterized queries
  [ ] No string concatenation in queries (SQL injection risk)
```

### Common Backend Anti-Patterns

```java
// ❌ WRONG: Field injection
@Singleton
public class PersonService {
    @Inject
    private PersonRepository personRepository;
}

// ✅ CORRECT: Constructor injection
@Singleton
public class PersonService {
    private final PersonRepository personRepository;

    public PersonService(PersonRepository personRepository) {
        this.personRepository = personRepository;
    }
}

// ❌ WRONG: Business logic in controller
@Post
public HttpResponse<PersonResponse> create(@Body @Valid CreatePersonRequest request) {
    if (personRepository.existsByEmail(request.email())) {
        return HttpResponse.status(CONFLICT);
    }
    var entity = new Person(null, request.name(), request.email());
    return HttpResponse.created(personRepository.save(entity));
}

// ✅ CORRECT: Delegate to service
@Post
public HttpResponse<PersonResponse> create(@Body @Valid CreatePersonRequest request) {
    var person = personService.create(request);
    var location = UriBuilder.of("/api/v1/persons")
        .path(person.id().toString())
        .build();
    return HttpResponse.created(person, location);
}

// ❌ WRONG: Mutable DTO with Lombok
@Data
public class PersonResponse {
    private UUID id;
    private String name;
}

// ✅ CORRECT: Java 21 record with @Serdeable
@Serdeable
public record PersonResponse(UUID id, String name, String email, Instant createdAt) {}

// ❌ WRONG: String concatenation in queries
@Query("SELECT * FROM persons WHERE name = '" + name + "'")

// ✅ CORRECT: Parameterized query
@Query("SELECT * FROM persons WHERE name = :name")

// ❌ WRONG: Old-style switch
switch (status) {
    case 200:
        result = "OK";
        break;
    default:
        result = "Unknown";
}

// ✅ CORRECT: Pattern matching switch (Java 21)
var result = switch (status) {
    case 200 -> "OK";
    default -> "Unknown";
};

// ❌ WRONG: collect(Collectors.toList())
items.stream().filter(predicate).collect(Collectors.toList());

// ✅ CORRECT: .toList() (Java 16+)
items.stream().filter(predicate).toList();
```

---

## Command: `/review lint`

Run all linters and formatters, report issues, and optionally fix them.

### Automated Quality Gates

Run these commands in sequence. **All must pass** before code can be merged.

```bash
# ─── Frontend Quality Gates ─────────────────────────────────

# 1. TypeScript type checking
bun run typecheck
# Equivalent to: tsc --noEmit
# Fail on: any type errors, missing types, strict violations

# 2. ESLint
bun run lint
# Equivalent to: eslint . --fix
# Fail on: any lint errors (warnings are acceptable but should be tracked)

# 3. Prettier format check
bun run format:check
# Equivalent to: prettier --check "src/**/*.{ts,tsx,css,json}"
# Fail on: any formatting inconsistencies

# 4. Tests
bun test
# Equivalent to: vitest run
# Fail on: any test failures

# ─── Backend Quality Gates ──────────────────────────────────

# 5. Gradle check (compile + test)
./gradlew check
# Includes: compileJava, compileTestJava, test
# Fail on: compilation errors, test failures

# 6. Detekt static analysis
./gradlew detekt
# Fail on: any code smell, complexity threshold exceeded
# Config: detekt.yml (custom rules for project conventions)

# 7. Dependency vulnerability scan
./gradlew dependencyCheckAnalyze
# Fail on: any CRITICAL or HIGH severity CVE
# Report: build/reports/dependency-check-report.html
```

### Quality Gate Summary

| Gate | Command | Failure Threshold | Fix Command |
|------|---------|-------------------|-------------|
| TypeCheck | `bun run typecheck` | Any error | Fix types manually |
| ESLint | `bun run lint` | Any error | `bun run lint` (auto-fix with `--fix`) |
| Format | `bun run format:check` | Any diff | `bun run format` (auto-fix) |
| Unit Tests | `bun test` | Any failure | Fix code or update tests |
| Gradle Check | `./gradlew check` | Any failure | Fix compilation / test errors |
| Detekt | `./gradlew detekt` | Any violation | Fix code or update baselines |
| Dependency Check | `./gradlew dependencyCheckAnalyze` | CRITICAL/HIGH CVE | Update dependency version |

### Detekt Configuration Checklist

When reviewing `detekt.yml`, verify:

```yaml
# Key rules to enforce
complexity:
  LongMethod:
    threshold: 30
  LongParameterList:
    functionThreshold: 6
  NestedBlockDepth:
    threshold: 3
  ComplexCondition:
    threshold: 3

style:
  MagicNumber:
    active: true
    ignoreNumbers: ["-1", "0", "1", "2"]
  WildcardImport:
    active: true
  MaxLineLength:
    maxLineLength: 120

exceptions:
  TooGenericExceptionCaught:
    active: true
  SwallowedException:
    active: true

empty-blocks:
  EmptyCatchBlock:
    active: true
  EmptyFunctionBlock:
    active: false  # Allow override stubs
```

### ESLint Configuration Checklist

When reviewing `eslint.config.js`, verify:

```javascript
// Key rules to enforce
rules: {
  // TypeScript
  "@typescript-eslint/no-explicit-any": "error",
  "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
  "@typescript-eslint/explicit-function-return-type": "off",
  "@typescript-eslint/no-non-null-assertion": "warn",

  // SolidJS
  "solid/reactivity": "error",       // Detect reactivity violations
  "solid/no-destructure": "error",   // No destructuring props
  "solid/prefer-for": "error",       // Use <For> not .map()
  "solid/no-react-specific-props": "error",
  "solid/jsx-no-duplicate-props": "error",
  "solid/self-closing-comp": "error",
  "solid/no-innerhtml": "error",     // Security: no dangerouslySetInnerHTML
}
```

---

## Command: `/review check`

Full convention audit report combining all checklists and automated gates.

### Instructions

1. **Run all automated quality gates** (see `/review lint`).

2. **Scan source files** for convention violations:
   - Frontend: `src/**/*.{ts,tsx}`
   - Backend: `src/**/*.java`

3. **Generate audit report** using the template below.

### Convention Audit Report Template

```markdown
# Convention Audit Report

**Date:** YYYY-MM-DD
**Branch:** branch-name
**Commit:** abc1234

## Executive Summary

| Category | Files Scanned | Violations | Status |
|----------|--------------|------------|--------|
| Frontend TypeScript | N | N | PASS/FAIL |
| Frontend SolidJS | N | N | PASS/FAIL |
| Frontend TailwindCSS | N | N | PASS/FAIL |
| Frontend Accessibility | N | N | PASS/FAIL |
| Backend Java 21 | N | N | PASS/FAIL |
| Backend Micronaut | N | N | PASS/FAIL |
| Backend Error Handling | N | N | PASS/FAIL |
| Security | N | N | PASS/FAIL |
| Testing | N | N | PASS/FAIL |

## Automated Gates

| Gate | Command | Result |
|------|---------|--------|
| TypeScript | `bun run typecheck` | PASS/FAIL |
| ESLint | `bun run lint` | PASS/FAIL |
| Prettier | `bun run format:check` | PASS/FAIL |
| Vitest | `bun test` | PASS/FAIL |
| Gradle | `./gradlew check` | PASS/FAIL |
| Detekt | `./gradlew detekt` | PASS/FAIL |
| Dependency | `./gradlew dependencyCheckAnalyze` | PASS/FAIL |

## Violations

| # | Category | File | Line | Rule | Severity | Description |
|---|----------|------|------|------|----------|-------------|
| 1 | | | | | BLOCKER/MAJOR/MINOR | |

## Coverage Summary

| Module | Statements | Branches | Functions | Lines |
|--------|-----------|----------|-----------|-------|
| src/components/ | __% | __% | __% | __% |
| src/services/ | __% | __% | __% | __% |
| controller/ | __% | __% | __% | __% |
| service/ | __% | __% | __% | __% |

## Recommendations

1. ___
2. ___
3. ___
```

---

## PR Process & Conventions

### Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

#### Types

| Type | Usage | Example |
|------|-------|---------|
| `feat` | New feature | `feat(frontend): add user profile page` |
| `fix` | Bug fix | `fix(backend): handle null email in PersonService` |
| `refactor` | Code restructuring without behavior change | `refactor(api): extract shared validation logic` |
| `test` | Adding or updating tests | `test(frontend): add UserList component tests` |
| `docs` | Documentation changes | `docs(api): update OpenAPI spec for persons endpoint` |
| `chore` | Build, tooling, or maintenance | `chore(deps): update SolidJS to 1.9.5` |
| `ci` | CI/CD pipeline changes | `ci: add Detekt step to GitHub Actions` |

#### Scopes

| Scope | Used For |
|-------|----------|
| `frontend` | SolidJS / TypeScript / CSS changes |
| `backend` | Micronaut / Java changes |
| `api` | API contract changes (endpoints, DTOs) |
| `infra` | Docker, nginx, CI/CD, deployment |
| `deps` | Dependency updates |

#### Rules

- Subject line max 72 characters
- Use imperative mood ("add", not "added" or "adds")
- No period at end of subject
- Body (if present) explains "why", not "what"
- Breaking changes: `feat(api)!: change person response format` + `BREAKING CHANGE:` in footer

### Merge Strategy

- **Squash merge** is the default for feature branches
- Squash commit message follows conventional commit format
- PR title becomes the squash commit subject
- No merge commits from `main` into feature branches (use rebase)

### PR Requirements

```
PR Process Checklist
════════════════════

PR Description:
  [ ] Links to issue / ticket number
  [ ] Describes what changed and why
  [ ] Lists manual testing performed
  [ ] Notes any breaking changes
  [ ] Screenshots for UI changes (if applicable)

Quality Gates:
  [ ] All CI checks green
  [ ] No merge conflicts with target branch
  [ ] Branch is up to date with target

Review:
  [ ] At least 1 approval required (2 for main branch)
  [ ] All review comments resolved
  [ ] No unresolved conversations

Merge:
  [ ] Squash merge into main
  [ ] PR title follows conventional commit format
  [ ] Delete source branch after merge
```

---

## Command: `/review debt`

Identify, categorize, and track technical debt across the codebase.

### Instructions

1. **Scan codebase** for debt indicators:
   - `TODO`, `FIXME`, `HACK`, `XXX` comments
   - Workaround patterns (try/catch around known issues, retry loops)
   - Missing tests for critical paths
   - Dead code (unused exports, unreachable branches)
   - Overly complex functions (cyclomatic complexity > 10)
   - Hard-coded values that should be configuration
   - Copy-pasted code (duplicate blocks)
   - Outdated dependencies with known issues
   - Missing error handling
   - Inconsistent patterns across modules

2. **Categorize each debt item** using the priority matrix.

3. **Generate debt register** using the template in `references/tech-debt-register-template.md`.

### Debt Priority Matrix

| Priority | Definition | Example | Must Fix In |
|----------|-----------|---------|-------------|
| **CRITICAL** | Security vulnerability, data loss risk, production outage | Hardcoded secret, unhandled null causing 500 errors | Current sprint |
| **HIGH** | Significant maintainability or reliability risk, blocks feature work | Missing transaction boundary, no error handling on API call | Next sprint |
| **MEDIUM** | Code quality issue, slows development but not broken | Missing tests for service layer, overly complex method | Within 2 sprints |
| **LOW** | Cosmetic or minor improvement, no functional impact | TODO comment for future enhancement, minor naming inconsistency | Backlog |

### Debt Categories

| Category | Tag | Description |
|----------|-----|-------------|
| Architecture | `arch` | Structural issues, wrong layer boundaries, circular deps |
| Code Quality | `quality` | Complexity, duplication, dead code, naming |
| Testing | `test` | Missing tests, low coverage, flaky tests |
| Security | `security` | Vulnerabilities, missing validation, exposed data |
| Performance | `perf` | N+1 queries, missing indexes, unnecessary re-renders |
| Dependencies | `deps` | Outdated, vulnerable, unused dependencies |
| Documentation | `docs` | Missing or outdated docs, comments |
| Configuration | `config` | Hard-coded values, missing feature flags |

### Sprint Capacity Allocation

Technical debt management follows the **20% rule**:

```
Sprint Capacity Allocation
══════════════════════════

Feature Work:        80% of sprint capacity
Tech Debt:           20% of sprint capacity
  ├── CRITICAL debt:  Fixed immediately, regardless of allocation
  ├── HIGH debt:      Prioritized from 20% allocation
  ├── MEDIUM debt:    Scheduled when capacity available
  └── LOW debt:       Addressed opportunistically during related feature work
```

**Sprint debt review process:**

1. At sprint planning, review the tech debt register
2. Select HIGH and MEDIUM items that fit within the 20% allocation
3. Create tasks for selected debt items with acceptance criteria
4. Track debt resolution in the sprint retrospective
5. Update the debt register after each sprint

### Tech Debt Register Template

```markdown
# Technical Debt Register

**Last Updated:** YYYY-MM-DD
**Sprint:** Sprint N

## Summary

| Priority | Count | Est. Effort |
|----------|-------|-------------|
| CRITICAL | N | N days |
| HIGH | N | N days |
| MEDIUM | N | N days |
| LOW | N | N days |
| **Total** | **N** | **N days** |

## Register

| ID | Priority | Category | Description | Location | Effort | Sprint | Status |
|----|----------|----------|-------------|----------|--------|--------|--------|
| TD-001 | CRITICAL | security | Hardcoded API key in HealthController | backend/.../HealthController.java:42 | 0.5d | Current | Open |
| TD-002 | HIGH | test | No tests for OrderService.createOrder | backend/.../OrderService.java | 2d | Next | Open |
| TD-003 | MEDIUM | quality | Duplicate validation logic in 3 controllers | backend/.../controller/*.java | 1d | — | Open |
| TD-004 | LOW | docs | Missing Javadoc on public service methods | backend/.../service/*.java | 0.5d | — | Open |

## History

| Date | ID | Action | Sprint |
|------|----|--------|--------|
| YYYY-MM-DD | TD-001 | Resolved: moved to environment variable | Sprint N |
```

---

## Review Etiquette Guidelines

### For Reviewers

```
Review Etiquette
════════════════

1. Be Respectful
   ├── Critique the code, not the author
   ├── Use "this code could..." not "you should have..."
   ├── Acknowledge good work ("nice use of createMemo here")
   └── Assume positive intent

2. Be Specific
   ├── Reference exact file and line number
   ├── Explain why something is an issue
   ├── Provide a code suggestion or alternative
   └── Link to conventions / documentation when applicable

3. Be Timely
   ├── Review PRs within 4 business hours
   ├── Block only for BLOCKER or MAJOR findings
   ├── Approve promptly after requested changes are made
   └── Don't let PRs sit idle — ping if needed

4. Scope Appropriately
   ├── Focus on the PR's changes, not pre-existing issues
   ├── Pre-existing issues → create tech debt items, don't block PR
   ├── Style preferences → MINOR/INFO, never block
   └── Don't request redesigns — suggest follow-up PRs

5. Use Severity Labels
   ├── BLOCKER: Must fix before merge
   ├── MAJOR: Should fix before merge (negotiable with justification)
   ├── MINOR: Nice to fix (non-blocking)
   └── INFO: Observation or suggestion (non-blocking)

6. Verify Before Requesting Changes
   ├── Reproduce the issue if possible
   ├── Check if the convention you're citing is current
   ├── Verify your suggested alternative actually works
   └── Consider the full context (not just the diff)
```

### For Authors

```
Author Guidelines
══════════════════

1. Prepare the PR
   ├── Keep PRs small (< 400 lines changed)
   ├── Self-review before requesting review
   ├── Run all quality gates locally before pushing
   ├── Write a clear description with context
   └── Add screenshots for UI changes

2. Respond to Reviews
   ├── Address every comment (even if just "done")
   ├── Push fixes as new commits (don't force-push during review)
   ├── Request re-review after addressing all comments
   ├── Disagree respectfully with evidence
   └── Don't take feedback personally

3. Make Review Easy
   ├── Organize commits logically
   ├── Use conventional commit messages
   ├── Add comments in the PR for complex decisions
   ├── Link to relevant issues / discussions
   └── Mark PR as "ready for review" only when actually ready
```

---

## Workflow

When invoked, follow this decision tree:

```
/review [command]
        │
        ├── pr ────────────► Gather PR context (diff, files, description)
        │                     │
        │                     ├── Run automated quality gates
        │                     ├── Apply General + Layer-specific checklists
        │                     ├── Check PR process compliance
        │                     └── Generate PR Review Report
        │
        ├── frontend ──────► Scan frontend source files
        │                     │
        │                     ├── TypeScript strict mode compliance
        │                     ├── SolidJS reactivity rules
        │                     ├── TailwindCSS 4 conventions
        │                     ├── Accessibility audit
        │                     └── Generate Frontend Review Report
        │
        ├── backend ───────► Scan backend source files
        │                     │
        │                     ├── Micronaut annotation compliance
        │                     ├── Java 21 feature usage
        │                     ├── Controller / Service layering
        │                     ├── Error handling patterns
        │                     └── Generate Backend Review Report
        │
        ├── lint ──────────► Run all linters and formatters
        │                     │
        │                     ├── Frontend: typecheck → lint → format:check → test
        │                     ├── Backend: check → detekt → dependencyCheckAnalyze
        │                     ├── Report all failures
        │                     └── Suggest fixes for each failure
        │
        ├── debt ──────────► Scan codebase for debt indicators
        │                     │
        │                     ├── Find TODO/FIXME/HACK comments
        │                     ├── Detect complexity hotspots
        │                     ├── Identify missing tests
        │                     ├── Find duplicate code
        │                     ├── Categorize by priority + category
        │                     └── Generate Tech Debt Register
        │
        └── check ─────────► Full convention audit
                              │
                              ├── Run all automated quality gates
                              ├── Scan all source files for violations
                              ├── Apply all review checklists
                              ├── Generate Coverage Summary
                              └── Generate Convention Audit Report
```

---

## Reference Files

Reference files contain extended checklists, templates, and examples for each review type. When performing reviews, consult these references for detailed criteria:

| Reference | Content |
|-----------|---------|
| `references/frontend-review-checklist.md` | Expanded SolidJS + TypeScript + TailwindCSS review criteria with code examples |
| `references/backend-review-checklist.md` | Expanded Micronaut + Java 21 review criteria with anti-pattern examples |
| `references/tech-debt-register-template.md` | Blank tech debt register template for copy-paste into project docs |
| `references/conventional-commits-guide.md` | Full conventional commits guide with examples for this project's scopes |

---

## Rules

1. **Never approve your own PR** — all changes require at least one peer review
2. **All quality gates must pass** — no bypassing typecheck, lint, or test failures
3. **Block only for BLOCKER and MAJOR** — minor issues should not delay merge
4. **Pre-existing issues are separate PRs** — don't scope-creep the current review
5. **Document exceptions** — if a convention is intentionally violated, add a comment explaining why
6. **No secrets in code** — zero tolerance for hardcoded credentials, keys, or tokens
7. **Test coverage is mandatory** — new code without tests is a MAJOR finding
8. **Review within 4 hours** — respect reviewers' and authors' time
9. **Squash merge only** — keep main branch history clean with conventional commit messages
10. **20% sprint capacity for tech debt** — track and address debt systematically, not reactively
