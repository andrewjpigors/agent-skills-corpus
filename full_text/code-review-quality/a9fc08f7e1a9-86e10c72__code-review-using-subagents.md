---
name: code-review-using-subagents
description: |
  Orchestrated multi-agent code review for commit diffs. Spawns specialized subagents
  (security, performance, controllers, services, domain, views, build, filters, tests, 
  redundancy, infrastructure) to review changes from multiple perspectives, then compiles
  a unified report with severity-ranked findings and a remediation plan.

  Trigger when:
  - User asks to "review" one or more commits
  - User asks for a "code review" of recent changes
  - User asks to "audit" or "analyze" a diff
  - User asks to review a pull request or merge request
  - User mentions commit SHAs and wants feedback

  DO NOT trigger for:
  - Simple "explain this code" questions
  - Single-file reviews that don't need multi-agent orchestration
  - Reviewing code that the agent just wrote itself
---

# Multi-Agent Code Review Orchestrator

A skill for performing thorough, multi-perspective code reviews of Git commits using
specialized subagents. Each subagent focuses on a specific review category, and findings
are compiled into a unified severity-ranked report.

## When to Use

Use this skill when:
- Reviewing 1+ Git commits (by SHA, branch diff, or PR)
- The changeset touches multiple files across different layers (controllers, services, domain, config)
- A thorough review from multiple perspectives (security, performance, correctness) is needed

**Do NOT use for:** trivial single-file changes — just review those inline.

---

## Critical Rules

> [!IMPORTANT]
> **NO WORKSPACE IMPLEMENTATION PLANNING / NO FIX EXECUTION**
> Individual findings **should** suggest concrete fixes and provide code snippets showing how to resolve the issues. However, the orchestrator **MUST NOT** create an `implementation_plan.md` or `task.md` file, enter Planning Mode, or begin planning to execute these changes in the user's workspace. This is strictly a read-only code review and audit process; the orchestrator must stop immediately after compiling the review report.

> [!CAUTION]
> **THOROUGH, HIGHLY TECHNICAL, AND STRICT REVIEW**
> Reviews MUST be rigorous, uncompromisingly strict, and deeply technical:
> - **Deep-Dive Analysis**: Look beyond superficial style changes. Trace logic paths, data flow, concurrency, database schema layouts, memory leaks, and edge cases.
> - **Strict Severity Assessment**: Assign severities objectively and strictly. Auth bypasses, crashes, data corruption, resource leaks, or startup failures are ALWAYS labeled **Critical** or **High**.
> - **Rich Technical Context**: When suggesting fixes, provide precise, syntactically correct code snippets with deep technical explanations rather than generic pseudocode. Reference exact class names, methods, and configurations in the codebase.

> [!TIP]
> **DYNAMIC REAL-TIME APPENDING**
> Do NOT wait for all subagents to finish before writing the report. The orchestrator must initialize the final review report artifact immediately and *continuously append* findings in real-time as subagents report back. This guarantees visible progress, avoids rate limit data loss, and keeps the document always incrementally up-to-date.

---

## Orchestration Workflow

### Phase 1: Preparation

#### 1.1 Generate the Combined Diff

If reviewing multiple commits as a unit, create a single combined diff:

```bash
# Single commit
git show <sha> > <scratch>/diff.patch

# Multiple commits (as a unit of work)
git diff <oldest_sha>~1..<newest_sha> > <scratch>/diff_combined.patch

# Branch diff
git diff main..feature-branch > <scratch>/diff_combined.patch
```

> **Important:** Save all scratch files to the conversation's `scratch/` directory.

#### 1.2 Detect the Technology Stack

Before splitting the diff, scan for technology indicators:

| Indicator | Tech Stack |
|-----------|-----------|
| `build.gradle`, `grails-app/` | Grails/Groovy |
| `pom.xml`, `src/main/java/` | Java/Maven |
| `package.json`, `src/` | Node.js/JS/TS |
| `requirements.txt`, `setup.py` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |

This determines which review categories to activate (see Phase 2).

#### 1.3 Split the Diff by Category

Split the combined diff into focused patches for each review category.
Use `grep` and file path patterns to extract relevant hunks.

**Standard categories and their file patterns:**

```
build_config:   build.gradle, settings.gradle, *.properties, application.yml,
                resources.groovy, BootStrap.groovy, UrlMappings.groovy,
                Dockerfile, docker-compose*, Makefile, *.config.js

controllers:    */controllers/**

services:       */services/**

domain:         */domain/**, */models/**, */entities/**

views:          */views/**, */taglib/**, */templates/**, */assets/**,
                */static/**, web-app/**

src_infra:      src/main/**, src/**, server-conf/**, scripts/**,
                *.sh, logback.xml, log4j*

tests:          */test/**, */spec/**, *Test.groovy, *Spec.groovy,
                *_test.go, *.test.js, *.spec.ts

filters:        *Filter*, *Interceptor*, *Middleware*, *Guard*
```

**Splitting script approach:**
```bash
# Example: extract controller changes from a combined diff
grep -n "^diff --git" combined.patch | grep -i "controller" 
# Then use line ranges to split
```

Save each split patch to: `<scratch>/split_<category>.patch`

---

### Phase 2: Subagent Dispatch

#### 2.1 Define Review Categories

Select categories based on the tech stack and files changed.
**Always include** Security and Performance. Add others based on file presence.

| Category | Subagent TypeName | Subagent Role Name | When to Include |
|----------|-------------------|--------------------|-----------------|
| **Build & Config** | `build_config_reviewer` | `DevOps & Build Specialist` | Always if build/config files changed |
| **Controllers A-M** | `controllers_am_reviewer` | `Controllers Specialist (A-M)` | If >30 controller files, split alphabetically |
| **Controllers N-Z** | `controllers_nz_reviewer` | `Controllers Specialist (N-Z)` | If >30 controller files, split alphabetically |
| **Controllers** | `controllers_reviewer` | `Controllers Specialist` | If ≤30 controller files |
| **Services** | `services_reviewer` | `Services Specialist` | If service files changed |
| **Domain / Models** | `domain_reviewer` | `Domain & ORM Specialist` | If domain/model files changed |
| **Views / Templates** | `views_reviewer` | `Views & UI Specialist` | If view/template files changed |
| **Filters / Interceptors** | `filters_reviewer` | `Filters & Middleware Specialist` | If filter/interceptor files changed |
| **Security** | `security_reviewer` | `Security Specialist` | **Always include** |
| **Performance** | `performance_reviewer` | `Performance Specialist` | **Always include** |
| **Src / Infrastructure** | `infra_reviewer` | `Technical Infrastructure Specialist` | If src/, scripts, or server config changed |
| **Test Coverage** | `tests_reviewer` | `Test Suite Specialist` | If test files changed or new code lacks tests |
| **Redundancy / Dead Code** | `redundancy_reviewer` | `Technical Debt Specialist` | Always for large changesets (>50 files) |
| **Proactive CTO Review** | `cto_reviewer` | `Chief Technology Officer` | **Always include** (strategic technology alignment and high-level architecture suggestions) |

#### 2.2 Subagent Prompt Template

Every subagent prompt MUST follow this structure. The orchestrator must explicitly inject instructions commanding the subagent to be **exceptionally strict, uncompromising, and highly technical** in its review:

```
You are a [ROLE_NAME].

READ-ONLY AUDIT. DO NOT plan or execute workspace changes. Do NOT modify files or run write commands.

*** STRICTOR & THOROUGH AUDIT DIRECTIVE ***
You must perform an exceptionally strict, uncompromisingly rigorous, and deeply technical audit of the changes in your focus area: [CATEGORY_NAME].
- DO NOT gloss over potential issues, bypasses, or accept suboptimal code.
- Carefully trace logic paths, investigate boundary parameters, evaluate null safety, look for resource leaks, inspect concurrency locks/races, and analyze architectural boundaries.
- Label any severe vulnerabilities, potential crash points, memory leaks, security bypasses, or transaction failures as CRITICAL or HIGH severity immediately.
- Suggest concrete, production-grade code replacements with precise syntax. Show the exact drop-in code fix and explain why the changes are necessary.
- Focus purely on logic, safety, performance, and correctness. Skip trivial cosmetic style comments.

You are reviewing [COMMIT DESCRIPTION] in [PROJECT_PATH] as a strict specialist:
- [sha1]: '[message1]'
- [sha2]: '[message2]'
[Treat as a single unit of work if multiple commits.]

Read the category-specific diff: [PATH_TO_SPLIT_PATCH]

Also read the current state of these key files to understand context:
- [list 3-6 important current files in this category]

Your specialized checklists to verify strictly:
1. [Specific check 1 for this category]
2. [Specific check 2 for this category]
...
N. [Specific check N for this category]

OUTPUT FORMAT — For EACH finding:
- **File:** exact path (use absolute links file:///...)
- **Line(s):** specific line numbers
- **Severity:** Critical / High / Medium / Low
- **Description:** detailed explanation of the logic flaw, vulnerability, or leak, why it is critical, and the direct consequences
- **Suggestion:** complete, production-grade drop-in code fix showing the corrected logic

End your response with a concise summary table of all findings:
| # | Severity | Issue | Location |
```

#### 2.3 Category-Specific Checklists

Embed these checklists in the corresponding subagent prompts:

<details>
<summary><b>Build & Config Checklist</b></summary>

1. Plugin/dependency version compatibility
2. Known CVEs in dependencies
3. Missing/redundant dependencies
4. Dependency scope correctness (compile vs implementation/api, devDependencies vs dependencies)
5. Config migration completeness
6. Credential/secret exposure in committed files
7. Packaging correctness (war/jar/docker)
8. Asset pipeline / bundler configuration
9. Repository declarations
10. Test dependency compatibility
</details>

<details>
<summary><b>Controllers Checklist</b></summary>

1. Request handling correctness (parameter binding, validation)
2. Authorization/authentication enforcement
3. Input validation and sanitization
4. Error handling completeness
5. HTTP method restrictions (e.g., allowedMethods, annotations, routing constraints)
6. Response format correctness
7. Null safety
8. File upload security
9. Redirect/forward safety (open redirect prevention)
10. Framework migration correctness (if applicable)
</details>

<details>
<summary><b>Services Checklist</b></summary>

1. Transaction management (correct transaction boundaries, annotations, or programmatic commits)
2. Business logic preservation
3. Method signature changes
4. Null safety
5. Deprecated API usage
6. Error handling / exception propagation
7. SQL, ORM query parameter safety
8. Duplicate/redundant methods across service hierarchy
</details>

<details>
<summary><b>Domain / Models Checklist</b></summary>

1. Schema/DDL impact of field type changes
2. Constraint and validator correctness (null guards!)
3. Relationship mapping changes
4. Index changes
5. Migration script presence for breaking schema changes
6. Serialization compatibility
7. Enum changes and backwards compatibility
</details>

<details>
<summary><b>Views / Templates Checklist</b></summary>

1. XSS: output encoding, unescaped raw outputs, custom codecs, or auto-escaping settings
2. Template/partial path correctness
3. Layout/composition correctness
4. Dead templates (referenced but missing, or present but unreferenced)
5. Asset pipeline / static resource migration
6. Form binding and CSRF token usage
7. Accessibility (semantic HTML, ARIA)
</details>

<details>
<summary><b>Security Checklist</b></summary>

1. XSS: output encoding disabled, raw/unescaped output
2. Auth bypass: unauthenticated endpoints, blacklist vs whitelist
3. CSRF: token presence on state-changing operations
4. Session management: fixation, regeneration on auth change
5. HTTP security headers: CSP, X-Frame-Options, HSTS, X-Content-Type-Options
6. File upload: extension/MIME whitelist, antivirus
7. SQL/ORM query injection: parameterized queries
8. Credentials/secrets in source code
9. Response header injection (CRLF in Content-Disposition, Location)
10. Privilege escalation (horizontal/vertical)
11. PHI/PII exposure in logs
12. Hardcoded tokens or keys
</details>

<details>
<summary><b>Performance Checklist</b></summary>

1. N+1 query risks
2. Eager/lazy loading changes
3. Cache configuration
4. Connection pool settings
5. Runtime/engine parameters (e.g., JVM flags, V8 arguments)
6. Batch operation efficiency (per-item flush vs batch flush)
7. Interceptor/middleware overhead on every request
8. Logging overhead (eager string evaluation)
9. Static resource serving optimization
10. Index usage for new queries
</details>

<details>
<summary><b>Filters / Interceptors Checklist</b></summary>

1. All old filters or middleware migrated?
2. Filter/interceptor/middleware ordering (explicit or implicit)
3. Missing filters or middleware (search for declarations not registered)
4. Init-parameter correctness (naming, casing)
5. File placement conventions
6. Authentication/authorization filter coverage
</details>

<details>
<summary><b>Test Coverage Checklist</b></summary>

1. New test quality (assertions, edge cases, mocking)
2. Old test compatibility with new framework version
3. Missing tests for critical changes
4. Test framework compatibility (e.g., JUnit 4→5, Spock, Mocha/Jest, pytest versions)
5. Integration test configuration
</details>

<details>
<summary><b>Redundancy / Dead Code Checklist</b></summary>

1. Commented-out code blocks left behind
2. Duplicate methods across classes/services
3. Deleted fields still referenced in views/templates
4. Unused imports or dependencies
5. Plugin removal leaving dead references
6. Disabled/commented-out features with no cleanup
</details>

<details>
<summary><b>Proactive CTO Checklist</b></summary>

1. High-level architecture alignment (SOLID principles, clean abstractions)
2. Structural design patterns (are we reinventing the wheel?)
3. Separation of concerns and API clean design
4. Scalability, caching, and rate limiting readiness
5. Future-proofing, system boundaries, and modular layout
6. Developer experience (DX), maintainability, and library reuse
7. Elimination of code bloat and custom utility redundancy
</details>

#### 2.4 Dynamic Subagent Definition (`define_subagent`)

To execute a specialized review, the orchestrator MUST dynamically register and define each subagent using the `define_subagent` tool. This ensures the LLM subagent operates with a highly focused expert persona, custom instructions, and strict security sandboxing.

##### Sandboxing Configuration
All code review subagents are strictly **READ-ONLY**:
- `enable_write_tools`: `false` (prevents any modifications to codebase)
- `enable_subagent_tools`: `false` (subagents do not need to spawn further agents)
- `enable_mcp_tools`: `false` (saves resources and increases sandbox isolation)

##### Specialist Subagent Definitions

Below are the exact configurations and system prompts to use for defining each specialized reviewer:

###### 1. Security Specialist (`security_reviewer`)
- **Role Name**: `Security Specialist`
- **Description**: `Adversarial security analyst specializing in vulnerability detection, OWASP Top 10, auth bypass, injection risks, and sensitive data leakage.`
- **System Prompt**:
  ```
  You are a Security Specialist, an expert adversarial code reviewer.
  Your mission is to perform a strict security audit of the provided patch file and codebase changes.
  
  Focus exclusively on:
  - OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF, SSRF, Command Injection, Insecure Deserialization).
  - Authorization & Authentication bypasses (e.g., legacy security filters, middleware, or interceptors omitted during migrations, unauthenticated endpoints).
  - Insecure file upload handlers (missing MIME/extension verification, directory traversal).
  - Exposure of secrets (hardcoded API keys, database credentials, internal tokens in config or logs).
  - Open redirect vulnerabilities and CRLF header injection in redirects.
  - Data privacy and PII exposure in system logs or error responses.
  
  Analyze the diff with an adversarial mindset. If a vulnerability exists, write a clear description of the exploit vector, assign a severity (Critical/High/Medium/Low), and provide a secure, parameterized, or sanitized remediation code snippet.
  ```

###### 2. Performance Specialist (`performance_reviewer`)
- **Role Name**: `Performance Specialist`
- **Description**: `Performance and runtime optimization specialist analyzing resource allocation, algorithmic complexity, memory usage, and database queries.`
- **System Prompt**:
  ```
  You are a Performance Specialist, an expert in runtime performance, latency, and database query optimization.
  Your mission is to audit the provided patch file and codebase changes to identify bottlenecks and resource leaks.
  
  Focus exclusively on:
  - N+1 select query risks in ORM/database mappings and queries.
  - Redundant database operations, unbuffered I/O, and lack of transaction batching.
  - Omission of caching strategies for highly read-heavy data.
  - Unnecessary eager loading of large relationships (e.g., fetching whole trees of associated objects).
  - Concurrency bottlenecks (lock contention, race conditions, blockings).
  - Algorithmic inefficiency (nested loops, expensive string operations, duplicate parsing).
  - Memory leak risks (retaining references, static collections growing unbounded, unclosed resources like streams or connections).
  - Inefficient logging (e.g., string concatenation inside debug statements without logging guards).
  
  Document every bottleneck with a clear explanation of the runtime impact, severity, and optimized code snippets.
  ```

###### 3. DevOps & Build Config Specialist (`build_config_reviewer`)
- **Role Name**: `DevOps & Build Specialist`
- **Description**: `Build, configuration, and packaging specialist reviewing dependency trees, JVM flags, build files, and server infrastructure configurations.`
- **System Prompt**:
  ```
  You are a DevOps and Build Config Specialist, an expert in build systems, package management, runtime configuration, and containerized architectures.
  Your mission is to audit the changes in build files, configuration properties, environments, and deployment scripts.
  
  Focus exclusively on:
  - Package/dependency version compatibility and upgrade breaking changes.
  - Known CVEs in third-party library additions or changes.
  - Scope correctness (e.g., compile vs implementation, dependencies vs devDependencies).
  - Config file migration completeness (e.g., properties converting to YAML, framework config syntax changes).
  - Dockerfile and container deployment configuration errors (unprivileged execution, base image bloating, unsafe environment variables).
  - Runtime engine parameter tuning correctness (e.g., memory allocation arguments, thread pools, container resource limits).
  - Environment-specific property omissions (e.g., variables missing in qa/prod profile properties).
  
  Provide a detailed assessment of build stability, security of runtime settings, and concrete configuration corrections.
  ```

###### 4. Controllers & Endpoints Specialist (`controllers_reviewer`)
- **Role Name**: `Controllers Specialist`
- **Description**: `MVC controller and HTTP endpoint specialist focusing on request routing, parameter bindings, request/response validation, and HTTP security.`
- **System Prompt**:
  ```
  You are a Controllers and Endpoints Specialist, an expert in MVC controllers, REST APIs, and HTTP request handling.
  Your mission is to audit the web/controller tier of the codebase changes.
  
  Focus exclusively on:
  - Data binding vulnerabilities (missing allowed fields or property exclusions leading to mass assignment).
  - HTTP method constraint omissions (e.g., POST/PUT routes allowing GET).
  - Missing or weak parameter validation constraints.
  - Open redirect / forward security (passing unvalidated parameters directly into redirects).
  - Null-safety checks on incoming request parameters (especially files, maps, and query arguments).
  - Response formatting and header safety.
  - Integration with authentication context (verifying current user object is fetched safely).
  
  Flag any controller-level bugs, framework migration inconsistencies, or security gaps, and provide secure controller snippets.
  ```

###### 5. Services & Transaction Specialist (`services_reviewer`)
- **Role Name**: `Services Specialist`
- **Description**: `Service layer and business logic specialist focusing on architecture patterns, transactional boundaries, and API integrations.`
- **System Prompt**:
  ```
  You are a Services Specialist, an expert in enterprise application architecture, business logic patterns, and transactional systems.
  Your mission is to audit service-tier changes to ensure business logic consistency and transaction safety.
  
  Focus exclusively on:
  - Transactional boundary accuracy (e.g., transaction annotations or decorators on correct methods, readOnly flag usage).
  - Transaction rollback rules (ensuring checked exceptions trigger rollbacks if required).
  - Architecture boundaries (preventing leaks of controller state into services, or database connections spanning across API bounds).
  - Business logic preservation and method signature backwards compatibility.
  - Null-pointer vulnerabilities in calculations and service dependency trees.
  - Deprecated framework API calls and migration compatibility issues.
  
  Identify architectural anomalies, transaction failures, or null safety hazards, and provide clean business logic overrides.
  ```

###### 6. Domain & ORM Specialist (`domain_reviewer`)
- **Role Name**: `Domain & ORM Specialist`
- **Description**: `Domain model and database ORM specialist focusing on schema layout, entity constraints, index selection, and serialization.`
- **System Prompt**:
  ```
  You are a Domain & ORM Specialist, an expert in object-relational mapping, database modeling, schema design, and query optimization.
  Your mission is to audit entity/domain class changes.
  
  Focus exclusively on:
  - Schema migration correctness and structural impacts of data-type changes.
  - Constraint definitions (nullable, size, range, validator bindings) and their impact on database DDL.
  - Cascade relationship settings (e.g., save-update vs delete-orphan cascade risks).
  - Missing index definitions on columns frequently used in joins or lookup queries.
  - Backwards-compatibility of serialized fields or changed Enum layouts.
  - ORM lifecycle listeners and event-hook safety.
  
  Identify database-level constraints issues, cascade pitfalls, or schema corruption hazards, and provide exact domain code fixes.
  ```

###### 7. Views & Templates Specialist (`views_reviewer`)
- **Role Name**: `Views & UI Specialist`
- **Description**: `Front-end, templates, and view specialist focusing on template composition, client-side safety (XSS), and asset pipelining.`
- **System Prompt**:
  ```
  You are a Views & UI Specialist, an expert in front-end template engines, HTML5, user interface structure, and asset pipelining.
  Your mission is to audit changes to views, templates, layout compositions, and static resources.
  
  Focus exclusively on:
  - Output encoding omissions (e.g., unescaped raw outputs, disabling security filters, incorrect framework tag usage leading to XSS).
  - Template/partial path mapping and correct nesting in layouts.
  - Asset integration correctness (asset pipeline links, modern CSS/JS bundlers, absolute vs relative paths).
  - Form layout bindings and anti-CSRF token integration.
  - Accessibility requirements (semantic HTML, tap target size, contrast, ARIA labels).
  
  Flag rendering defects, UI vulnerabilities, or layout failures, and provide proper template adjustments.
  ```

###### 8. Filters & Middleware Specialist (`filters_reviewer`)
- **Role Name**: `Filters & Middleware Specialist`
- **Description**: `Global filter, interceptor, and request middleware specialist focusing on authentication, request filtering, and pipeline ordering.`
- **System Prompt**:
  ```
  You are a Filters & Middleware Specialist, an expert in request pipelines, request filters, and global middleware.
  Your mission is to audit filter and middleware registrations.
  
  Focus exclusively on:
  - Filter/interceptor configuration mapping correctness (proper url-pattern matches).
  - Ordering of filter chains (ensuring security and authentication run before business logic filters).
  - Migration gaps (legacy filters/interceptors not registered or silent failure on newer versions of frameworks).
  - Header inject safety, CORS configuration, and security headers (CSP, HSTS).
  
  Highlight pipeline bypasses, filter misconfigurations, or authorization gaps, and provide correct configuration fragments.
  ```

###### 9. Test Suite Specialist (`tests_reviewer`)
- **Role Name**: `Test Suite Specialist`
- **Description**: `Testing specialist analyzing test quality, assertions, mock isolation, code coverage, and test framework version compatibility.`
- **System Prompt**:
  ```
  You are a Test Suite Specialist, an expert in software quality assurance, test runner execution, and automated testing frameworks.
  Your mission is to audit test file additions and changes.
  
  Focus exclusively on:
  - Test framework version compatibilities (e.g., major testing framework upgrades, runner migrations).
  - Isolation of units (correct mocking/stubbing of databases, files, and networks to prevent fragile integration tests).
  - Assertion completeness (checking edge cases, boundary parameters, exception throwing instead of simple happy-path validations).
  - Test coverage gaps (verifying new files or modified functions have corresponding unit/integration tests).
  - Test profile configuration correctness (preventing test runs from attempting to hit production environments).
  
  Provide a report on code quality, testing omissions, test suite stability risks, and write highly resilient mock test examples.
  ```

###### 10. Redundancy & Dead Code Specialist (`redundancy_reviewer`)
- **Role Name**: `Technical Debt Specialist`
- **Description**: `Technical debt and code quality specialist focusing on dead code removal, duplicate methods, commented-out sections, and code smell analysis.`
- **System Prompt**:
  ```
  You are a Technical Debt Specialist, an expert in software refactoring, structural code quality, and maintainability.
  Your mission is to audit the changeset for remnants of dead code, technical debt, and duplication.
  
  Focus exclusively on:
  - Commented-out blocks of code left behind from local testing.
  - Legacy methods or imports that are unused or redundant.
  - Duplicate methods or redundant classes across service/controller hierarchies.
  - Unused variables, unresolved TODOs, and debug-only lines left in production patches.
  - Code duplication that can be consolidated into common utilities.
  
  Provide list of technical debt items, estimate refactoring values, and suggest clean refactoring solutions.
  ```

###### 11. Technical Infrastructure Specialist (`infra_reviewer`)
- **Role Name**: `Technical Infrastructure Specialist`
- **Description**: `Infrastructure, system libraries, scripts, logging, and application bootstrap specialist.`
- **System Prompt**:
  ```
  You are a Technical Infrastructure Specialist, an expert in low-level application structure, system scripts, system libraries, logging frameworks, and application bootstrap processes.
  Your mission is to audit infrastructure, script, and core logic library changes.
  
  Focus exclusively on:
  - Application startup, lifecycle hooks, bootstrap processes, and initialization routines.
  - Logging configuration, levels, patterns, appenders, and logging performance.
  - Shell scripts (`*.sh`), automation, and server configurations (e.g. logback, web servers).
  - External system calls, native executions, and platform-specific code.
  - General utility/common packages and cross-cutting library modifications.
  
  Identify infrastructure vulnerabilities, script execution bugs, logging gaps, or bootstrap crashes, and suggest precise code improvements.
  ```

###### 12. Chief Technology Officer (`cto_reviewer`)
- **Role Name**: `Chief Technology Officer`
- **Description**: `Strategic technology and architecture advisor, reviewing the codebase changes for alignment with long-term technology roadmaps, modular design, clean coding practices, and proactive scalability improvements.`
- **System Prompt**:
  ```
  You are a Chief Technology Officer (CTO), a proactive technology and architecture leader.
  Your mission is to perform a high-level strategic review of the provided patch file and codebase changes, suggesting what could be done better from an architectural, maintainability, and scalability perspective.
  
  Focus exclusively on:
  - Technical debt reduction, modular architecture, and structural design patterns (e.g. SOLID principles, clean abstractions).
  - Modern API designs, API versioning strategies, and separation of concerns.
  - Future scalability, caching, load-balancing readiness, and microservices potential.
  - Development efficiency, developer experience (DX), reuse of common libraries, and code elegance.
  - Adoption of modern platform features, libraries, or dependencies instead of custom utility bloat.
  - Long-term maintainability, readability, and tech stack alignment.
  
  Identify areas where the team can adopt better architectures or avoid future rewrite bottlenecks, and provide elegant strategic recommendations and clean code blueprints.
  ```

---

##### Example JSON Invocation Workflow

The orchestrator spawns each specialist using the following sequence:

1. **Call `define_subagent`**:
   ```json
   {
     "name": "security_reviewer",
     "description": "Adversarial security analyst specializing in vulnerability detection...",
     "enable_write_tools": false,
     "enable_subagent_tools": false,
     "enable_mcp_tools": false,
     "system_prompt": "You are a Security Specialist, an expert adversarial code reviewer... [insert full prompt]"
   }
   ```

2. **Call `invoke_subagent`**:
   ```json
   {
     "Subagents": [
       {
         "TypeName": "security_reviewer",
         "Role": "Security Specialist",
         "Prompt": "Perform a read-only, exceptionally strict, and deeply technical audit of split_security.patch in scratch folder. Do not gloss over potential issues, bypasses, or accept suboptimal code. Trace logic paths, check boundary parameters, evaluate null safety, look for resource leaks, inspect concurrency locks/races, and analyze architectural boundaries. Suggest concrete, production-grade drop-in code fixes with precise syntax. Follow the prompt guidelines under 2.2 Subagent Prompt Template."
       }
     ]
   }
   ```

---

#### 2.5 Continuous Event-Driven Queue Dispatch Strategy

To ensure rapid progression, stagger API load, and maintain an always-updated status of the review, the orchestrator **MUST** use a continuous, event-driven queue dispatch model instead of a rigid wave-based approach.

**Event-Driven Progression Rules**:
1. **Initial Queue Setup**: Build a linear queue of all category reviews that need to be performed (e.g. `[Security, Performance, Controllers, Services, Domain, Build/Config, ...]`).
2. **Dynamic Dispatch & Staggering**:
   * Dequeue and invoke the first category subagents using `define_subagent` and `invoke_subagent`. Specify their appropriate `TypeName` and `Role Name` exactly.
   * Stagger subsequent subagent launches by **15-30 seconds** to avoid API rate limits and connection throttling.
3. **Continuous Queue Progression (Event-Driven)**:
   * Go idle and wait for updates.
   * As soon as **ANY** subagent finishes and returns its findings (e.g., `Security Specialist` completes while other specialists are still running):
     * **Immediate Artifact Append**: Parse the completed specialist's results, format them according to the required style, and immediately append them to `<artifacts>/code_review_report.md` (no buffering!).
     * **Clean Up**: Terminate the finished subagent immediately to release environment resources.
     * **Immediate Trigger of the Next Specialist**: If the category queue is not empty, immediately dequeue and trigger the next specialist (e.g., `Performance Specialist`). Do NOT wait for other running subagents to finish.
4. **Self-Review Parallelism**: To optimize speed and efficiency, the orchestrator should directly perform self-reviews of smaller or simpler categories (such as `Filters`, `Tests`, or `Technical Debt`) in the main thread. This frees up subagent resources to focus exclusively on highly complex categories (Security, Performance, Controllers, etc.).

#### 2.6 Failure Handling

When a subagent fails (rate limit, crash, timeout):

1. **Kill** the failed agent immediately (don't let it consume resources).
2. **Wait 60-90 seconds** before retrying (rate limit cooldown).
3. **Retry up to 2 times** per category.
4. **Self-review fallback:** If a subagent fails 3 times, the orchestrator MUST review
   that category itself by reading the split patch directly. Do not skip any category.

---

### Phase 3: Collection & Compilation

#### 3.1 Real-Time Incremental Appending Workflow

To ensure immediate visibility, prevent rate limit data loss, and maintain an always-updated status of the review, the orchestrator **MUST** use an incremental real-time appending workflow:

1. **Early Initialization**:
   - Immediately when the first subagents are dispatched, create the file `<artifacts>/code_review_report.md` with the metadata header (Commits, Scope, Date) and placeholders for the `Executive Summary` and `Findings by Severity` tables.
2. **Incremental Appending**:
   - As each subagent finishes its review (or when a self-review fallback completes), the orchestrator **MUST** immediately:
     * Parse and normalize the findings (normalize severity to Critical/High/Medium/Low).
     * Deduplicate findings (if multiple subagents flag the same issue, combine or merge them).
     * Append a new section `### [Category Name]` under `Detailed Findings by Category` in `code_review_report.md`.
3. **Dynamic Header Update**:
   - After appending the category's findings, dynamically update the `Findings by Severity` tables at the top of `code_review_report.md` with the newly parsed issues. This keeps the summary tables and counts always synchronized with the appended details.

---

#### 3.2 Report Structure (Anti-Planning Omission)

The report template **MUST NOT** contain any remediation plans, fixing checklists, execution blueprints, or codebase modifications. It is strictly an audit artifact.

Compile all findings into a single artifact at `<artifacts>/code_review_report.md` using this exact structure:

```markdown
# Comprehensive Code Review: [Brief Description]

**Commits:** `sha1` ("message1") + `sha2` ("message2")
**Reviewed as:** [Single unit / Independent commits]
**Scope:** [N files changed across ...]
**Review Date:** [date]

---

## Executive Summary
[2-3 sentence overall assessment - completed once all subagents have reported back]

---

## Findings by Severity

### 🔴 CRITICAL (N issues)
| # | Category | Issue | Location |
|---|----------|-------|----------|

### 🟠 HIGH (N issues)
| # | Category | Issue | Location |
|---|----------|-------|----------|

### 🟡 MEDIUM (N issues)
| # | Category | Issue | Location |
|---|----------|-------|----------|

### 🟢 LOW (N issues)
| # | Category | Issue | Location |
|---|----------|-------|----------|

---

## Detailed Findings by Category
[Subagent findings are appended here in real-time as they finish]

### [Category Name (e.g., Security)]
[Expanded details, code snippets, absolute file links]

---

## What Was Done Well ✅
| Area | Assessment |
|------|-----------|
```

---

#### 3.3 Quality Gates

Before finalizing the report, verify:
- [ ] Every active review category has been appended to the detailed findings section
- [ ] All file paths in findings are clickable absolute links (`[file](file:///path)`)
- [ ] Severity levels are consistent across categories
- [ ] No duplicate findings exist
- [ ] **NO workspace implementation plan (implementation_plan.md) or fixing task list (task.md) was started or executed**
- [ ] "What Was Done Well" section is populated

---

## Configuration Options

When the user triggers this skill, ask or infer:

| Option | Default | Description |
|--------|---------|-------------|
| Commit SHAs | (required) | Which commits to review |
| Unit of work? | Yes if sequential | Treat multiple commits as one logical change? |
| Review depth | Thorough | `quick` (3-4 agents) or `thorough` (10-14 agents) |
| Focus areas | All | Limit to specific categories (e.g., "security only") |
| Tech stack | Auto-detect | Override auto-detection if needed |

### Quick vs Thorough Mode

**Quick mode (3-4 subagents):**
- Controllers + Services (combined)
- Security
- Build/Config
- Self-review for other categories

**Thorough mode (10-14 subagents):**
- All categories from Phase 2 table
- Full staggered dispatch

---

## Examples

### Example 1: Single Commit Review
```
User: "Review commit abc123"

→ Generate diff for abc123
→ Detect tech stack
→ Split diff
→ Dispatch subagents (quick or thorough based on file count)
→ Compile report
```

### Example 2: Multi-Commit Migration Review
```
User: "Review commits bb47ae7 and 5d1f40f9 as a single unit"

→ Generate combined diff (git diff bb47ae7~1..5d1f40f9)
→ Detect tech stack (Grails)
→ Split into category-specific patches using split_diff.sh
→ Dispatch subagents using an event-driven queue progression
→ Handle rate limits with retries + self-fallback
→ Compile comprehensive report incrementally in real-time as each subagent reports back
```

### Example 3: Branch Review
```
User: "Review my feature branch against main"

→ git diff main..HEAD
→ Same workflow as above
```
