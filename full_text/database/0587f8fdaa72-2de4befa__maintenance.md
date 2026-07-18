---
name: "maintenance"
tags: [maintenance, dependencies, migration, tech-debt, security, deprecation, optimization]
description: |
  Agentic skill for the "Maintenance & Evolution" phase of the SDLC. Handles
  dependency updates, database migrations, tech debt reduction, security
  patching, feature deprecation, and performance optimization for the full-stack
  architecture.

  Trigger phrases:
    - "update dependencies"
    - "database migration"
    - "tech debt"
    - "security patch"
    - "deprecate feature"
    - "optimize performance"
    - "refactor"

  Tech stack assumptions:
    Frontend — Bun + TypeScript 5.8 (strict) + SolidJS 1.9 + SolidStart (SSG)
               + TailwindCSS 4.1 (CSS-first @theme) + Iconify-Solid
    Backend  — Java 21 (records, sealed interfaces, virtual threads,
               pattern matching) + Micronaut 4.7 + Gradle Kotlin DSL
               + Flyway (database migration) + Shadow JAR
---

# Maintenance & Evolution

> **Ongoing SDLC phase.** Keeps the application healthy, secure, and performant
> throughout its lifetime. Covers dependency management, database schema
> evolution, tech debt reduction, security patching, deprecation workflows,
> and performance optimization across both frontend and backend.

## Commands

| Command | Description |
|---|---|
| `/maintain deps` | Check and update all dependencies |
| `/maintain migrate` | Generate database migration script |
| `/maintain debt` | Generate tech debt reduction plan |
| `/maintain optimize` | Performance optimization analysis |
| `/maintain security` | Security audit and patch |
| `/maintain deprecate` | Deprecate a feature with migration guide |
| `/maintain check` | Full maintenance health check |

---

## Command: `/maintain deps`

Checks and updates all dependencies across the frontend and backend, producing a
report of available updates, breaking changes, and recommended actions.

### Frontend Dependency Management

**Stack:** Bun runtime, TypeScript, SolidJS, SolidStart, TailwindCSS, Iconify

#### Step 1: Audit Current State

```bash
# List outdated packages
bun outdated

# Check for known vulnerabilities
bun audit

# View current dependency tree
bun pm ls
```

#### Step 2: Categorize Updates

Classify each outdated dependency by risk level:

| Risk Level | Criteria | Action |
|------------|----------|--------|
| **Patch** | `x.y.Z` — bug fixes, no API changes | Auto-update after test pass |
| **Minor** | `x.Y.z` — new features, backward-compatible | Update + run full test suite |
| **Major** | `X.y.z` — breaking changes | Manual review, read changelog, plan migration |
| **Security** | CVE or vulnerability advisory | Immediate update per SLA (see Security section) |

#### Step 3: Update Dependencies

```bash
# Interactive update (recommended)
bun update --interactive

# Update specific package
bun update solid-js
bun update @solidjs/router @solidjs/start @solidjs/meta

# Update all patch + minor versions
bun update

# Update to latest major version (caution)
bun update --latest

# Update TailwindCSS ecosystem
bun update tailwindcss @tailwindcss/vite prettier-plugin-tailwindcss

# Update dev tooling
bun update typescript vitest eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser
```

#### Step 4: Post-Update Verification

```bash
bun install                    # Ensure lockfile is consistent
bun run typecheck              # TypeScript strict mode still passes
bun run lint                   # ESLint still passes
bun test                       # All unit tests pass
bun run build                  # Production build succeeds
bun run test:coverage          # Coverage thresholds still met
```

#### Frontend Dependency Version Matrix

| Package | Current Min | Notes |
|---------|------------|-------|
| `solid-js` | ^1.9.5 | Core reactivity framework |
| `@solidjs/start` | ^1.1.3 | Meta framework (SSG mode) |
| `@solidjs/router` | ^0.15.3 | File-based routing |
| `@solidjs/meta` | ^0.29.4 | SSR-safe meta tags |
| `@iconify-icon/solid` | ^2.1.0 | Icon components |
| `tailwindcss` | ^4.1.4 | CSS-first config (no `tailwind.config.js`) |
| `@tailwindcss/vite` | ^4.1.4 | Vite plugin for TailwindCSS 4 |
| `typescript` | ^5.8.3 | Strict mode required |
| `vitest` | ^3.1.2 | Test runner |
| `eslint` | ^9.24.0 | Flat config (`eslint.config.js`) |
| `vinxi` | ^0.6.3 | Build pipeline for SolidStart |

#### Breaking Change Watch List

When updating major versions, check for these known migration paths:

| Package | Breaking Change | Migration |
|---------|----------------|-----------|
| `tailwindcss` 3→4 | Config moves to CSS `@theme`, no `tailwind.config.js` | Replace JS config with `@import "tailwindcss"` + `@theme {}` in CSS |
| `eslint` 8→9 | Flat config required | Migrate `.eslintrc` → `eslint.config.js` |
| `solid-js` 1.x | Minor breaking changes between minor versions | Check SolidJS changelog, test reactivity patterns |
| `vinxi` 0.x | API changes possible between patches | Pin exact version if unstable |
| `typescript` 5.x | Stricter type checks in newer minors | Run `tsc --noEmit` after update |

### Backend Dependency Management

**Stack:** Java 21, Micronaut 4.7, Gradle Kotlin DSL, Shadow JAR

#### Step 1: Audit Current State

```bash
# Check for dependency updates (requires ben-manes plugin)
./gradlew dependencyUpdates

# OWASP dependency check for vulnerabilities
./gradlew dependencyCheckAnalyze

# View dependency tree
./gradlew dependencies --configuration runtimeClasspath
./gradlew dependencies --configuration testRuntimeClasspath

# Check for duplicate dependencies
./gradlew dependencies | grep -A 5 "->"
```

#### Step 2: Gradle Version Catalog (Recommended)

Maintain a centralized version catalog in `gradle/libs.versions.toml`:

```toml
[versions]
micronaut = "4.7.6"
micronaut-plugin = "4.5.2"
shadow-plugin = "8.3.6"
java = "21"
junit = "5.11.4"
logback = "1.5.18"
jakarta-validation = "3.1.1"

[libraries]
micronaut-http-server = { module = "io.micronaut:micronaut-http-server-netty" }
micronaut-serde-jackson = { module = "io.micronaut.serde:micronaut-serde-jackson" }
micronaut-validation = { module = "io.micronaut.validation:micronaut-validation" }
jakarta-validation-api = { module = "jakarta.validation:jakarta.validation-api", version.ref = "jakarta-validation" }
logback-classic = { module = "ch.qos.logback:logback-classic", version.ref = "logback" }
junit-api = { module = "org.junit.jupiter:junit-jupiter-api", version.ref = "junit" }
junit-engine = { module = "org.junit.jupiter:junit-jupiter-engine", version.ref = "junit" }

[plugins]
micronaut-application = { id = "io.micronaut.application", version.ref = "micronaut-plugin" }
micronaut-aot = { id = "io.micronaut.aot", version.ref = "micronaut-plugin" }
shadow = { id = "com.gradleup.shadow", version.ref = "shadow-plugin" }
```

Reference in `build.gradle.kts`:

```kotlin
plugins {
    alias(libs.plugins.micronaut.application)
    alias(libs.plugins.micronaut.aot)
    alias(libs.plugins.shadow)
}

dependencies {
    implementation(libs.micronaut.http.server)
    implementation(libs.micronaut.serde.jackson)
    implementation(libs.micronaut.validation)
    implementation(libs.jakarta.validation.api)
    implementation(libs.logback.classic)

    testImplementation(libs.junit.api)
    testRuntimeOnly(libs.junit.engine)
}
```

#### Step 3: Update Dependencies

```bash
# Update Gradle wrapper
./gradlew wrapper --gradle-version=8.13

# Update Micronaut platform (BOM-managed)
# Edit gradle.properties: micronautVersion=4.7.6 → latest
./gradlew clean build

# Update specific dependency in version catalog
# Edit gradle/libs.versions.toml, then:
./gradlew clean build --refresh-dependencies
```

#### Step 4: Post-Update Verification

```bash
./gradlew clean build          # Full clean build
./gradlew test                 # All tests pass
./gradlew shadowJar            # Fat JAR builds
./gradlew dependencyCheckAnalyze  # No new vulnerabilities
java -jar build/libs/*-all.jar # Application starts
curl -s http://localhost:8080/api/v1/health  # Health check
```

### Dependency Update Report Template

```
Dependency Update Report
═════════════════════════
Date: YYYY-MM-DD
Project: [project-name]

Frontend (Bun):
┌─────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Package                 │ Current  │ Latest   │ Risk     │ Action   │
├─────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ solid-js                │ 1.9.5    │ 1.9.7    │ Patch    │ Auto     │
│ tailwindcss             │ 4.1.4    │ 4.2.0    │ Minor    │ Test     │
│ typescript              │ 5.8.3    │ 6.0.0    │ Major    │ Review   │
└─────────────────────────┴──────────┴──────────┴──────────┴──────────┘

Backend (Gradle):
┌─────────────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Dependency              │ Current  │ Latest   │ Risk     │ Action   │
├─────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│ io.micronaut:*          │ 4.7.6    │ 4.8.0    │ Minor    │ Test     │
│ ch.qos.logback          │ 1.5.18   │ 1.6.0    │ Minor    │ Test     │
│ org.junit.jupiter       │ 5.11.4   │ 5.12.0   │ Minor    │ Test     │
└─────────────────────────┴──────────┴──────────┴──────────┴──────────┘

Vulnerabilities:
  [ ] Critical: ___
  [ ] High: ___
  [ ] Medium: ___
  [ ] Low: ___

Breaking Changes to Review:
  1. ___
  2. ___

Post-Update Status:
  [ ] Frontend build passes
  [ ] Frontend tests pass
  [ ] Backend build passes
  [ ] Backend tests pass
  [ ] Integration tests pass
  [ ] No new vulnerabilities
```

---

## Command: `/maintain migrate`

Generates Flyway database migration scripts following the project naming
convention, with up/down SQL and rollback strategy.

### Flyway Naming Convention

```
src/main/resources/db/migration/
├── V1__create_persons_table.sql
├── V2__create_orders_table.sql
├── V3__add_email_index_to_persons.sql
├── V4__add_status_column_to_orders.sql
├── V5__create_audit_log_table.sql
└── V6__add_soft_delete_to_persons.sql
```

**Naming pattern:** `V{version}__{description}.sql`

- `V` prefix — versioned migration (runs once)
- `{version}` — integer, sequential, no gaps (1, 2, 3, ...)
- `__` — double underscore separator
- `{description}` — lowercase, snake_case description
- `.sql` — SQL file extension

**Repeatable migrations:** `R__{description}.sql` (runs every time checksum changes)

```
src/main/resources/db/migration/
├── V1__create_persons_table.sql
├── V2__create_orders_table.sql
└── R__create_or_replace_function_updated_at.sql
```

### Micronaut Flyway Configuration

`src/main/resources/application.yml`:

```yaml
flyway:
  enabled: true
  datasources:
    default:
      enabled: true
      locations:
        - classpath:db/migration
      baseline-on-migrate: true
      baseline-version: 0
      validate-on-migrate: true
      out-of-order: false
      placeholder-replacement: false

datasources:
  default:
    url: ${DB_URL:`jdbc:postgresql://localhost:5432/appdb`}
    username: ${DB_USERNAME:`app`}
    password: ${DB_PASSWORD:``}
    driver-class-name: org.postgresql.Driver
    schema-generate: NONE
    dialect: POSTGRES
```

**Required dependency in `build.gradle.kts`:**

```kotlin
implementation("io.micronaut.flyway:micronaut-flyway")
runtimeOnly("org.postgresql:postgresql:42.7.5")
```

### Migration Template

When generating a migration, follow this template:

```sql
-- Migration: V{version}__{description}.sql
-- Created: YYYY-MM-DD
-- Author: [author]
-- Description: [what this migration does]

-- ========== UP ==========

-- [SQL statements here]
-- Example: Create table
CREATE TABLE IF NOT EXISTS persons (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(100)   NOT NULL,
    email       VARCHAR(255)   NOT NULL UNIQUE,
    role        VARCHAR(50)    NOT NULL DEFAULT 'user',
    created_at  TIMESTAMPTZ    NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ    NOT NULL DEFAULT now()
);

-- Create index
CREATE INDEX idx_persons_email ON persons (email);
CREATE INDEX idx_persons_role  ON persons (role);

-- ========== ROLLBACK (for reference) ==========
-- DROP TABLE IF EXISTS persons;
```

### Common Migration Patterns

#### Add Column

```sql
-- V{version}__add_status_to_orders.sql
ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending';
CREATE INDEX idx_orders_status ON orders (status);

-- Rollback:
-- ALTER TABLE orders DROP COLUMN status;
```

#### Add Foreign Key

```sql
-- V{version}__add_user_ref_to_orders.sql
ALTER TABLE orders ADD COLUMN user_id UUID NOT NULL REFERENCES persons(id) ON DELETE CASCADE;
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Rollback:
-- ALTER TABLE orders DROP COLUMN user_id;
```

#### Create Join Table

```sql
-- V{version}__create_order_items_table.sql
CREATE TABLE IF NOT EXISTS order_items (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id    UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id  UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_order_items_order_id   ON order_items (order_id);
CREATE INDEX idx_order_items_product_id ON order_items (product_id);

-- Rollback:
-- DROP TABLE IF EXISTS order_items;
```

#### Add Soft Delete

```sql
-- V{version}__add_soft_delete_to_persons.sql
ALTER TABLE persons ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX idx_persons_deleted_at ON persons (deleted_at) WHERE deleted_at IS NOT NULL;

-- Rollback:
-- ALTER TABLE persons DROP COLUMN deleted_at;
```

#### Data Migration

```sql
-- V{version}__migrate_user_roles.sql
-- Normalize role strings to enum values
UPDATE persons SET role = 'ADMIN' WHERE role = 'admin';
UPDATE persons SET role = 'USER'  WHERE role = 'user';
UPDATE persons SET role = 'USER'  WHERE role NOT IN ('ADMIN', 'USER');

-- Rollback: (reverse the mapping)
-- UPDATE persons SET role = 'admin' WHERE role = 'ADMIN';
-- UPDATE persons SET role = 'user'  WHERE role = 'USER';
```

#### Create Audit Log

```sql
-- V{version}__create_audit_log.sql
CREATE TABLE IF NOT EXISTS audit_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name  VARCHAR(100) NOT NULL,
    record_id   UUID NOT NULL,
    action      VARCHAR(10)  NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data    JSONB,
    new_data    JSONB,
    changed_by  VARCHAR(255),
    changed_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_log_table_record ON audit_log (table_name, record_id);
CREATE INDEX idx_audit_log_changed_at   ON audit_log (changed_at);

-- Rollback:
-- DROP TABLE IF EXISTS audit_log;
```

### Migration Workflow

```
/maintain migrate
        │
        ├── Ask: What schema change?
        │   ├── New table
        │   ├── Add/remove column
        │   ├── Add index/constraint
        │   ├── Data migration
        │   └── Custom SQL
        │
        ├── Determine next version number
        │   └── List existing migrations, find max version + 1
        │
        ├── Generate migration file
        │   ├── V{next}__{description}.sql
        │   ├── Include rollback comment
        │   └── Include indexes for foreign keys
        │
        ├── Verify locally
        │   ├── ./gradlew flywayMigrate
        │   ├── ./gradlew flywayInfo
        │   └── ./gradlew test (against migrated DB)
        │
        └── Generate migration report
            ├── Version, description, author
            ├── Up SQL summary
            ├── Rollback SQL summary
            └── Risk assessment (data loss? locking?)
```

---

## Command: `/maintain debt`

Generates a prioritized tech debt reduction plan based on codebase analysis.

### Tech Debt Prioritization Matrix

Priority is determined by **impact on safety, performance, and maintainability**:

```
Priority Order (Highest → Lowest):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Security        ← Vulnerabilities, exposed secrets, outdated auth
2. Performance     ← Slow queries, memory leaks, N+1 queries, large bundles
3. Readability     ← Dead code, magic numbers, inconsistent naming, complex methods
4. Tests           ← Missing coverage, flaky tests, untested edge cases
5. Documentation   ← Stale docs, missing API docs, outdated README
```

### Tech Debt Detection Checklist

When scanning the codebase, look for these signals:

#### Security Debt

```
[ ] Hardcoded secrets or API keys
[ ] Outdated dependencies with known CVEs
[ ] Missing input validation on endpoints
[ ] SQL queries using string concatenation
[ ] Missing authentication on sensitive endpoints
[ ] CORS configured to allow all origins
[ ] Sensitive data logged in plaintext
[ ] Missing rate limiting
[ ] Insecure session management
[ ] Missing security headers (CSP, HSTS, X-Frame-Options)
```

#### Performance Debt

```
[ ] N+1 query patterns (check loops with DB calls)
[ ] Missing database indexes on frequently queried columns
[ ] Large frontend bundle size (> 300KB JS)
[ ] Unoptimized images (no WebP/AVIF, missing lazy loading)
[ ] Missing connection pool tuning
[ ] Synchronous blocking calls that could be virtual threads
[ ] Unnecessary re-renders in SolidJS components
[ ] Missing pagination on list endpoints
[ ] No caching strategy for frequently accessed data
[ ] GC pressure from excessive object allocation
```

#### Readability Debt

```
[ ] Methods longer than 30 lines
[ ] Classes with more than 10 dependencies
[ ] Magic numbers / strings without named constants
[ ] Inconsistent naming conventions
[ ] Dead code (unused imports, unreachable branches)
[ ] Complex nested conditionals (> 3 levels)
[ ] Missing or misleading comments
[ ] Copy-pasted code (DRY violations)
[ ] God classes / God components (too many responsibilities)
[ ] Mixed languages in comments (consistency issue)
```

#### Test Debt

```
[ ] Code coverage below 80%
[ ] Untested error paths
[ ] Missing integration tests for API endpoints
[ ] No E2E tests for critical user journeys
[ ] Flaky tests (non-deterministic)
[ ] Tests that depend on execution order
[ ] Missing tests for edge cases (null, empty, boundary)
[ ] Hardcoded test data (not using factories)
[ ] No performance regression tests
[ ] Mocking implementation details instead of behavior
```

#### Documentation Debt

```
[ ] Stale API documentation
[ ] Missing JSDoc / Javadoc for public APIs
[ ] Outdated README (wrong commands, wrong versions)
[ ] Missing architecture decision records (ADRs)
[ ] Undocumented environment variables
[ ] Missing deployment documentation
[ ] No changelog or release notes
[ ] Undocumented configuration options
```

### Tech Debt Plan Template

```markdown
# Tech Debt Reduction Plan

**Project:** [project-name]
**Date:** YYYY-MM-DD
**Review Period:** [e.g., Sprint 15, Q2 2026]

## Summary

| Category | Items | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Security | _     | _        | _    | _      | _   |
| Performance | _ | _     | _        | _    | _      | _   |
| Readability | _  | _     | _        | _    | _      | _   |
| Tests | _         | _     | _        | _    | _      | _   |
| Documentation | _| _    | _        | _    | _      | _   |

## Priority Items (Do First)

### 1. [SEC-001] [Title]
- **Category:** Security
- **Severity:** Critical
- **Effort:** [hours/days]
- **File(s):** `path/to/file`
- **Description:** [what the issue is]
- **Remediation:** [how to fix it]
- **Verification:** [how to confirm it's fixed]

### 2. [PERF-001] [Title]
- **Category:** Performance
- **Severity:** High
- **Effort:** [hours/days]
- **File(s):** `path/to/file`
- **Description:** [what the issue is]
- **Remediation:** [how to fix it]
- **Verification:** [how to confirm it's fixed]

## Backlog Items (Do Later)

| ID | Category | Title | Effort | Priority |
|----|----------|-------|--------|----------|
| READ-001 | Readability | Extract magic numbers | 2h | Medium |
| TEST-001 | Tests | Add integration tests for /orders | 4h | Medium |
| DOC-001 | Documentation | Update API docs | 3h | Low |

## Metrics Tracking

| Metric | Before | Target | After |
|--------|--------|--------|-------|
| Frontend bundle size | ___KB | <300KB | ___KB |
| Backend p95 latency | ___ms | <500ms | ___ms |
| Test coverage | ___% | >80% | ___% |
| Open vulnerabilities | ___ | 0 | ___ |
| Lines of dead code | ___ | 0 | ___ |
```

---

## Command: `/maintain optimize`

Performs a comprehensive performance optimization analysis across frontend and
backend, producing actionable recommendations with measurable targets.

### Frontend Performance Optimization

#### Bundle Analysis

```bash
# Analyze bundle size with vinxi
bun run build
ls -la .output/public/assets/

# Check individual asset sizes
du -sh .output/public/assets/*.js
du -sh .output/public/assets/*.css

# Install bundle analyzer (if not present)
bun add -d rollup-plugin-visualizer

# Add to app.config.ts vite config:
# plugins: [tailwindcss(), visualizer({ open: true, gzipSize: true })]
```

**Bundle size targets:**

| Asset Type | Target | Maximum |
|------------|--------|---------|
| Total JS | < 150KB gzipped | 300KB gzipped |
| Total CSS | < 50KB gzipped | 100KB gzipped |
| Images per page | < 200KB | 500KB |
| First-party JS | < 100KB gzipped | 200KB gzipped |

#### Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | 200ms - 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |
| FCP (First Contentful Paint) | ≤ 1.8s | 1.8s - 3.0s | > 3.0s |
| TTFB (Time to First Byte) | ≤ 800ms | 800ms - 1800ms | > 1800ms |

#### Frontend Optimization Checklist

```
Bundle Optimization:
  [ ] Tree-shaking verified (no unused exports in bundle)
  [ ] Code splitting by route (SolidStart file-based routing)
  [ ] Dynamic imports for heavy components
  [ ] No duplicate dependencies (check with bun pm ls)
  [ ] Externalize large libraries not needed at runtime

CSS Optimization:
  [ ] TailwindCSS purge configured (automatic in v4 production builds)
  [ ] No unused CSS classes in production build
  [ ] Critical CSS inlined (if using SSR/SSG)
  [ ] CSS loaded via @import "tailwindcss" (v4 pattern)

Image Optimization:
  [ ] Images served in WebP or AVIF format
  [ ] Responsive images with srcset
  [ ] Lazy loading for below-fold images (loading="lazy")
  [ ] Width/height attributes to prevent layout shift
  [ ] Image CDN or optimized asset pipeline

SolidJS Specific:
  [ ] Components use fine-grained signals (no unnecessary re-renders)
  [ ] createMemo for derived computations
  [ ] createResource for async data loading (no waterfall)
  [ ] <Show> / <For> for conditional rendering (no array .map)
  [ ] onCleanup for proper resource disposal
  [ ] No signal reads in setTimeout/setInterval without proper tracking

Network Optimization:
  [ ] HTTP/2 or HTTP/3 enabled
  [ ] Gzip/Brotli compression enabled (nginx)
  [ ] Cache headers set correctly (assets: immutable, HTML: no-cache)
  [ ] Preconnect/preload critical resources
  [ ] No render-blocking resources
```

#### TailwindCSS Purge Verification

TailwindCSS 4 automatically purges unused classes in production builds. Verify:

```bash
# Build and check CSS size
bun run build
gzip -c .output/public/assets/*.css | wc -c  # Should be < 20KB gzipped

# If CSS is too large, check for:
# 1. Dynamic class construction (doesn't work with TailwindCSS)
#    BAD:  class={`bg-${color}-500`}
#    GOOD: class={color === "red" ? "bg-red-500" : "bg-blue-500"}
# 2. Third-party libraries adding untracked classes
# 3. Safelist configuration if needed
```

### Backend Performance Optimization

#### JVM Profiling

```bash
# JFR (Java Flight Recorder) — built into JDK 21
# Start application with JFR:
java -XX:StartFlightRecording=duration=60s,filename=app.jfr \
  --enable-preview -XX:+UseCompactObjectHeaders -jar app.jar

# Analyze JFR file:
# Use JDK Mission Control (JMC) or jfr tool
jfr print --events CPULoad,GarbageCollection,JavaMonitorWait app.jfr

# Quick GC analysis
java -Xlog:gc*:file=gc.log -jar app.jar
```

#### GC Tuning (Java 21)

```bash
# Default: G1GC (recommended for most workloads)
java -XX:+UseG1GC \
  -Xms512m -Xmx512m \
  --enable-preview -XX:+UseCompactObjectHeaders \
  -jar app.jar

# For low-latency: ZGC
java -XX:+UseZGC \
  -Xms1g -Xmx1g \
  --enable-preview -XX:+UseCompactObjectHeaders \
  -jar app.jar

# For throughput: Parallel GC
java -XX:+UseParallelGC \
  -Xms1g -Xmx1g \
  --enable-preview -XX:+UseCompactObjectHeaders \
  -jar app.jar
```

**GC Selection Guide:**

| Collector | Best For | Pause Time | Throughput |
|-----------|----------|------------|------------|
| G1GC (default) | General purpose | < 200ms | High |
| ZGC | Low-latency services | < 10ms | Good |
| Shenandoah | Low-latency, large heaps | < 20ms | Good |
| Parallel | Batch processing, analytics | Variable | Highest |

#### Slow Query Detection

```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, total_exec_time, mean_exec_time,
       max_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- PostgreSQL: Find missing indexes
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY abs(n_distinct) DESC;

-- PostgreSQL: Find unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- PostgreSQL: Check table bloat
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

#### N+1 Query Detection

Scan the codebase for common N+1 patterns:

```java
// BAD: N+1 query — executes one query per person
List<Person> persons = personRepository.findAll();
for (Person p : persons) {
    List<Order> orders = orderRepository.findByPersonId(p.id()); // N queries!
}

// GOOD: Batch query or JOIN
// Option 1: Batch fetch
Map<UUID, List<Order>> ordersByPerson = orderRepository
    .findByPersonIdIn(persons.stream().map(Person::id).toList())
    .stream()
    .collect(Collectors.groupingBy(Order::personId));

// Option 2: Custom query with JOIN
@Query("SELECT p.*, o.* FROM persons p LEFT JOIN orders o ON p.id = o.person_id WHERE p.id IN (:ids)")
List<PersonWithOrders> findWithOrders(List<UUID> ids);
```

#### Connection Pool Tuning

```yaml
# src/main/resources/application.yml
datasources:
  default:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    driver-class-name: org.postgresql.Driver
    dialect: POSTGRES
    # HikariCP settings (Micronaut default pool)
    maximum-pool-size: 20          # CPU cores * 2 + effective spindles
    minimum-idle: 5                # Keep 5 warm connections
    idle-timeout: 300000           # 5 minutes
    max-lifetime: 1800000          # 30 minutes
    connection-timeout: 30000      # 30 seconds to acquire
    leak-detection-threshold: 60000 # Alert on connections held > 60s
```

**Pool sizing formula:**

```
connections = ((core_count * 2) + effective_spindle_count)

Example:
  4 CPU cores, 1 SSD = (4 * 2) + 1 = 9 connections
  Round up to 10-20 for safety margin
```

#### Backend Optimization Checklist

```
Database:
  [ ] All foreign key columns indexed
  [ ] Frequently queried columns indexed
  [ ] Composite indexes for multi-column WHERE clauses
  [ ] No SELECT * — specify needed columns
  [ ] Pagination on all list endpoints
  [ ] Query timeout configured
  [ ] Connection pool properly sized

Application:
  [ ] No N+1 query patterns
  [ ] Virtual threads enabled for blocking I/O
  [ ] Proper use of Micronaut compile-time DI
  [ ] No reflection-based serialization (use @Serdeable)
  [ ] Async/non-blocking where possible
  [ ] Proper caching headers on static responses
  [ ] Compression enabled (gzip/deflate)

Memory:
  [ ] Heap size appropriate for workload
  [ ] GC selected based on latency requirements
  [ ] No memory leaks (check with JFR/heap dump)
  [ ] Large objects handled efficiently (streams, pagination)
  [ ] Object pooling for expensive allocations (if applicable)
```

### Performance Audit Report Template

```markdown
# Performance Audit Report

**Date:** YYYY-MM-DD
**Environment:** [local / staging / production]

## Frontend Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| LCP | ___ms | ≤ 2500ms | PASS/FAIL |
| INP | ___ms | ≤ 200ms | PASS/FAIL |
| CLS | ___ | ≤ 0.1 | PASS/FAIL |
| FCP | ___ms | ≤ 1800ms | PASS/FAIL |
| TTFB | ___ms | ≤ 800ms | PASS/FAIL |
| JS Bundle (gzip) | ___KB | < 150KB | PASS/FAIL |
| CSS Bundle (gzip) | ___KB | < 50KB | PASS/FAIL |
| Total page weight | ___KB | < 500KB | PASS/FAIL |

## Backend Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| p50 latency | ___ms | < 100ms | PASS/FAIL |
| p95 latency | ___ms | < 500ms | PASS/FAIL |
| p99 latency | ___ms | < 1000ms | PASS/FAIL |
| Throughput | ___RPS | > 1000 | PASS/FAIL |
| Error rate | ___% | < 0.1% | PASS/FAIL |
| GC pause (max) | ___ms | < 200ms | PASS/FAIL |
| Heap usage | ___MB | < 80% | PASS/FAIL |
| DB connections | ___/___ | < 80% | PASS/FAIL |

## Findings

### Critical
1. ___

### High
1. ___

### Medium
1. ___

### Low
1. ___

## Recommendations (Prioritized)
1. ___
2. ___
3. ___
```

---

## Command: `/maintain security`

Performs a security audit and generates a patch plan based on vulnerability
severity and SLA commitments.

### Security Patch SLA

| Severity | SLA | Examples |
|----------|-----|---------|
| **Critical** | **24 hours** | Remote code execution, data exfiltration, auth bypass |
| **High** | **7 days** | SQL injection, XSS with significant impact, privilege escalation |
| **Medium** | **30 days** | Information disclosure, CSRF, misconfigured headers |
| **Low** | **Next release** | Minor info leak, best practice violations |

### Security Audit Workflow

```
/maintain security
        │
        ├── Step 1: Dependency Audit
        │   ├── Frontend: bun audit
        │   ├── Backend: ./gradlew dependencyCheckAnalyze
        │   └── Container: trivy image / grype image
        │
        ├── Step 2: Code Scan
        │   ├── Hardcoded secrets (grep patterns)
        │   ├── SQL injection patterns
        │   ├── XSS vectors
        │   ├── Insecure deserialization
        │   └── Sensitive data exposure
        │
        ├── Step 3: Configuration Audit
        │   ├── CORS configuration
        │   ├── Security headers
        │   ├── Authentication/Authorization
        │   ├── Rate limiting
        │   └── Environment variable handling
        │
        ├── Step 4: Container Security
        │   ├── Base image vulnerabilities
        │   ├── Secret scanning
        │   ├── Container privileges
        │   └── Network policies
        │
        └── Step 5: Generate Report
            ├── Vulnerability list with CVSS scores
            ├── SLA deadlines per severity
            ├── Remediation steps per finding
            └── Verification commands
```

### Container Scanning

```bash
# Trivy — comprehensive container scanner
trivy image --severity HIGH,CRITICAL myapp:latest
trivy image --format json --output trivy-report.json myapp:latest
trivy image --exit-code 1 --severity CRITICAL myapp:latest  # Fail on critical

# Grype — alternative scanner
grype myapp:latest
grype myapp:latest --fail-on critical

# Scan Dockerfile for best practices
docker run --rm -i hadolint/hadolint < Dockerfile

# Multi-stage scan
trivy fs .                    # Scan filesystem (source code)
trivy image myapp:build       # Scan build stage
trivy image myapp:latest      # Scan runtime stage
```

### Secret Scanning

```bash
# Detect hardcoded secrets in source
git log --all --oneline | while read commit rest; do
  git diff-tree --no-commit-id -r "$commit" | while read mode1 mode2 hash1 hash2 status file; do
    git show "$commit:$file" 2>/dev/null | grep -iE '(password|secret|api.key|token).*=.*["\x27]' && echo "  ^ in $file @ $commit"
  done
done

# Using trufflehog (recommended)
trufflehog filesystem --directory .

# Using gitleaks
gitleaks detect --source . --verbose
```

### Security Header Verification

```bash
# Check backend security headers
curl -sI http://localhost:8080/api/v1/health | grep -iE '(x-frame|content-type|strict-transport|x-xss|referrer|content-security)'

# Check frontend security headers (nginx)
curl -sI http://localhost:3000 | grep -iE '(x-frame|content-type|strict-transport|x-xss|referrer|content-security)'

# Expected headers:
# X-Frame-Options: SAMEORIGIN
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Strict-Transport-Security: max-age=31536000; includeSubDomains
# Referrer-Policy: strict-origin-when-cross-origin
# Content-Security-Policy: default-src 'self'; ...
```

### Secret Rotation Checklist

```
Secret Rotation:
  [ ] Database credentials rotated
  [ ] API keys regenerated
  [ ] JWT signing keys rotated
  [ ] OAuth client secrets updated
  [ ] Encryption keys rotated
  [ ] Service account credentials updated
  [ ] CI/CD tokens regenerated
  [ ] Docker registry tokens rotated
  [ ] Third-party integration keys updated
  [ ] Old credentials revoked (not just new ones created)

Verification:
  [ ] Application still functional after rotation
  [ ] No hardcoded credentials remain in code
  [ ] All secrets in environment variables or secret manager
  [ ] .gitignore excludes .env files
  [ ] No secrets in git history (use git-filter-repo if found)
```

### Micronaut Security Configuration Template

```yaml
# application.yml — security hardening
micronaut:
  server:
    cors:
      enabled: true
      configurations:
        all:
          allowedOrigins:
            - ${FRONTEND_URL:`http://localhost:3000`}
          allowedMethods:
            - GET
            - POST
            - PUT
            - DELETE
          allowedHeaders:
            - Content-Type
            - Authorization
          maxAge: 3600
    max-request-size: 1MB
    idle-timeout: 300s

  # If using micronaut-security
  security:
    enabled: true
    authentication: bearer
    token:
      jwt:
        signatures:
          secret:
            generator:
              secret: ${JWT_SECRET}
              jws-algorithm: HS256
        generator:
          access-token-expiration: 3600
          refresh-token-expiration: 86400
    intercept-url-map:
      - pattern: /api/v1/health
        access: isAnonymous()
      - pattern: /api/v1/**
        access: isAuthenticated()
```

### Security Audit Report Template

```markdown
# Security Audit Report

**Date:** YYYY-MM-DD
**Auditor:** [auditor]
**Scope:** [full / dependencies / code / configuration]

## Executive Summary

| Severity | Count | Within SLA | Overdue |
|----------|-------|------------|---------|
| Critical | _     | _          | _       |
| High     | _     | _          | _       |
| Medium   | _     | _          | _       |
| Low      | _     | _          | _       |

## Findings

### [CVE-XXXX-XXXXX] Critical — [Title]
- **Severity:** Critical (CVSS: 9.8)
- **SLA Deadline:** YYYY-MM-DD (24h from discovery)
- **Affected Component:** `package-name@version`
- **Description:** [what the vulnerability is]
- **Remediation:** Upgrade to `package-name@X.Y.Z`
- **Verification:** `bun audit` / `./gradlew dependencyCheckAnalyze`
- **Status:** [ ] Patched [ ] Pending [ ] Accepted Risk

### [SEC-002] High — [Title]
- **Severity:** High (CVSS: 7.5)
- **SLA Deadline:** YYYY-MM-DD (7d from discovery)
- **Affected Component:** [file / endpoint / configuration]
- **Description:** [what the issue is]
- **Remediation:** [how to fix]
- **Verification:** [how to verify fix]
- **Status:** [ ] Patched [ ] Pending [ ] Accepted Risk

## Container Scan Results

| Image | Critical | High | Medium | Low |
|-------|----------|------|--------|-----|
| myapp:latest | _ | _ | _ | _ |
| frontend:latest | _ | _ | _ | _ |

## Post-Audit Actions
1. ___
2. ___
3. ___
```

---

## Command: `/maintain deprecate`

Manages the lifecycle of features that need to be deprecated, including
annotations, migration guides, and removal scheduling.

### Deprecation Workflow

```
/maintain deprecate
        │
        ├── Ask: What is being deprecated?
        │   ├── API endpoint
        │   ├── Component / module
        │   ├── Configuration option
        │   ├── Library / utility
        │   └── Database column / table
        │
        ├── Step 1: Add deprecation annotations
        │   ├── Backend: @Deprecated + @deprecated Javadoc
        │   ├── Frontend: @deprecated JSDoc
        │   └── Document removal timeline
        │
        ├── Step 2: Create migration guide
        │   ├── Current usage → New usage mapping
        │   ├── Code examples (before/after)
        │   └── Automated migration script (if feasible)
        │
        ├── Step 3: Update documentation
        │   ├── API docs (mark as deprecated)
        │   ├── README / guides
        │   └── CHANGELOG entry
        │
        ├── Step 4: Set removal version
        │   ├── Mark for removal in next major version
        │   └── Add to deprecation tracker
        │
        └── Step 5: Notify consumers
            ├── Update CHANGELOG
            ├── Log warning at runtime
            └── Return Deprecation HTTP header
```

### Backend Deprecation (Java / Micronaut)

#### Deprecating an API Endpoint

```java
/**
 * List all persons.
 *
 * @deprecated Use {@link #listPaginated(int, int, String, String)} instead.
 *             This endpoint will be removed in v2.0.0.
 *             Migration: Add page/size query parameters.
 * @since 1.5.0
 */
@Deprecated(since = "1.5.0", forRemoval = true)
@Get("/persons")
public HttpResponse<List<PersonResponse>> list() {
    return HttpResponse.ok(personService.findAll())
        .header("Deprecation", "true")
        .header("Sunset", "Sat, 01 Nov 2026 00:00:00 GMT")
        .header("Link", "</api/v1/persons?page=0&size=20>; rel=\"successor-version\"");
}

@Get("/persons")
public HttpResponse<Page<PersonResponse>> listPaginated(
        @QueryValue(defaultValue = "0") int page,
        @QueryValue(defaultValue = "20") int size,
        @QueryValue(defaultValue = "name") String sort,
        @QueryValue(defaultValue = "asc") String order) {
    return HttpResponse.ok(personService.findAll(page, size, sort, order));
}
```

#### Deprecating a Service Method

```java
/**
 * Find person by email address.
 *
 * @deprecated Use {@link #findByContact(String)} which supports multiple contact methods.
 *             Scheduled for removal in v2.0.0.
 * @param email the email address to search for
 * @return optional person response
 */
@Deprecated(since = "1.6.0", forRemoval = true)
public Optional<PersonResponse> findByEmail(String email) {
    log.warn("findByEmail is deprecated, use findByContact instead");
    return personRepository.findByEmail(email).map(this::toResponse);
}

public Optional<PersonResponse> findByContact(String contact) {
    return personRepository.findByEmail(contact)
        .or(() -> personRepository.findByPhone(contact))
        .map(this::toResponse);
}
```

#### Deprecating a DTO Field

```java
@Serdeable
public record PersonResponse(
    UUID id,
    String name,
    String email,

    /**
     * @deprecated Use {@code role} instead. Will be removed in v2.0.0.
     */
    @Deprecated(since = "1.5.0", forRemoval = true)
    @JsonProperty("type")
    String type,

    String role
) {}
```

### Frontend Deprecation (TypeScript / SolidJS)

#### Deprecating a Component

```tsx
/**
 * @deprecated Use `UserCard` instead. Will be removed in v2.0.0.
 * Migration: Replace `<UserProfile>` with `<UserCard user={user} />`.
 * The `UserCard` component supports the same props plus additional features.
 *
 * @example
 * // Before
 * <UserProfile name={user.name} email={user.email} />
 *
 * // After
 * <UserCard user={user} />
 */
export function UserProfile(props: UserProfileProps) {
  console.warn(
    "[DEPRECATED] UserProfile is deprecated. Use UserCard instead. " +
    "See migration guide: docs/migrations/user-profile-to-user-card.md"
  );
  // ... existing implementation
}
```

#### Deprecating a Utility Function

```ts
/**
 * @deprecated Use `formatUserName` instead. Will be removed in v2.0.0.
 *
 * @example
 * // Before
 * const display = getUserDisplayName(user);
 *
 * // After
 * const display = formatUserName(user.firstName, user.lastName);
 */
export function getUserDisplayName(user: User): string {
  console.warn("[DEPRECATED] getUserDisplayName is deprecated. Use formatUserName.");
  return `${user.firstName} ${user.lastName}`.trim();
}

export function formatUserName(firstName: string, lastName: string): string {
  return `${firstName} ${lastName}`.trim();
}
```

### Migration Guide Template

```markdown
# Migration Guide: [Deprecated Feature] → [New Feature]

**Deprecated Since:** vX.Y.Z
**Removal Version:** vA.0.0
**Status:** [Active Deprecation / Scheduled Removal / Removed]

## Summary

Brief description of what changed and why.

## What Changed

| Aspect | Before | After |
|--------|--------|-------|
| API Endpoint | `GET /persons` | `GET /persons?page=0&size=20` |
| Response | `Person[]` | `Page<Person>` |
| Parameters | None | `page`, `size`, `sort`, `order` |

## Migration Steps

### Step 1: Update API Calls

**Before:**
```typescript
const response = await fetch('/api/v1/persons');
const persons: Person[] = await response.json();
```

**After:**
```typescript
const response = await fetch('/api/v1/persons?page=0&size=20');
const page: Page<Person> = await response.json();
const persons = page.content;
```

### Step 2: Update Types

**Before:**
```typescript
interface PersonResponse {
  id: string;
  name: string;
  type: string; // deprecated
}
```

**After:**
```typescript
interface PersonResponse {
  id: string;
  name: string;
  role: string; // replaces type
}
```

### Step 3: Update UI Components

[Component-specific migration steps]

## Breaking Changes

1. **Response format changed** from array to paginated object
2. **Field renamed** from `type` to `role`
3. **Default behavior** now returns first 20 results instead of all

## Automated Migration

```bash
# Run automated migration script (if available)
npx migrate-person-endpoint ./src

# Or use this sed command:
find src -name '*.ts' -exec sed -i 's/\.type/.role/g' {} +
```

## Rollback

If issues arise after migration:
1. Revert to previous API version header: `Accept: application/vnd.api.v1+json`
2. Deploy previous frontend build
3. Report issue: [issue tracker link]

## Timeline

| Date | Event |
|------|-------|
| YYYY-MM-DD | Feature deprecated in vX.Y.Z |
| YYYY-MM-DD | Warning logs added |
| YYYY-MM-DD | Migration guide published |
| YYYY-MM-DD | Feature removed in vA.0.0 |

## Questions?

Contact: [team/channel/link]
```

### Deprecation Tracker

Maintain a tracking file at `docs/deprecations.md`:

```markdown
# Active Deprecations

| Feature | Deprecated | Removal | Replacement | Guide |
|---------|-----------|---------|-------------|-------|
| `GET /persons` (unpaginated) | v1.5.0 | v2.0.0 | `GET /persons?page=&size=` | [link] |
| `UserProfile` component | v1.6.0 | v2.0.0 | `UserCard` component | [link] |
| `getUserDisplayName()` | v1.6.0 | v2.0.0 | `formatUserName()` | [link] |
| `PersonResponse.type` field | v1.5.0 | v2.0.0 | `PersonResponse.role` | [link] |

# Removed Features

| Feature | Removed | Replacement | Migration |
|---------|---------|-------------|-----------|
| `GET /users/legacy` | v1.5.0 | `GET /persons` | [link] |
```

---

## Command: `/maintain check`

Performs a full maintenance health check across all dimensions, producing a
comprehensive status report.

### Health Check Workflow

```
/maintain check
        │
        ├── 1. Dependencies
        │   ├── Frontend: bun outdated + bun audit
        │   ├── Backend: ./gradlew dependencyUpdates + dependencyCheckAnalyze
        │   └── Container: trivy image / grype image
        │
        ├── 2. Database Migrations
        │   ├── ./gradlew flywayInfo
        │   ├── Check for pending migrations
        │   └── Validate applied migrations (checksum)
        │
        ├── 3. Tech Debt
        │   ├── Scan for signals (see /maintain debt)
        │   ├── Calculate debt score
        │   └── List top 5 priority items
        │
        ├── 4. Security
        │   ├── OWASP Top 10 quick scan
        │   ├── Dependency vulnerabilities
        │   ├── Container vulnerabilities
        │   └── Secret scanning
        │
        ├── 5. Performance
        │   ├── Frontend bundle size
        │   ├── Backend build time
        │   ├── Test suite execution time
        │   └── Key endpoint response times
        │
        ├── 6. Deprecations
        │   ├── List active deprecations
        │   ├── Check upcoming removal dates
        │   └── Verify migration guides exist
        │
        └── 7. Generate Health Report
```

### Health Check Commands

```bash
# === Frontend ===
bun outdated 2>&1                    # Outdated packages
bun audit 2>&1                       # Vulnerabilities
bun run typecheck 2>&1               # TypeScript health
bun run lint 2>&1                    # Code quality
bun test 2>&1                        # Test status
bun run build 2>&1                   # Build health
du -sh .output/public/assets/        # Bundle size

# === Backend ===
./gradlew dependencyUpdates 2>&1     # Outdated dependencies
./gradlew dependencyCheckAnalyze 2>&1 # OWASP check
./gradlew flywayInfo 2>&1            # Migration status
./gradlew test 2>&1                  # Test status
./gradlew build 2>&1                 # Build health
du -sh build/libs/                   # JAR size

# === Container ===
trivy image myapp:latest 2>&1        # Runtime image scan
trivy image frontend:latest 2>&1     # Frontend image scan
```

### Health Report Template

```markdown
# Maintenance Health Report

**Project:** [project-name]
**Date:** YYYY-MM-DD
**Generated by:** /maintain check

## Overall Health Score: [A/B/C/D/F]

| Dimension | Score | Status |
|-----------|-------|--------|
| Dependencies | [A/B/C/D/F] | [details] |
| Database | [A/B/C/D/F] | [details] |
| Tech Debt | [A/B/C/D/F] | [details] |
| Security | [A/B/C/D/F] | [details] |
| Performance | [A/B/C/D/F] | [details] |
| Deprecations | [A/B/C/D/F] | [details] |

## Scoring Criteria

| Score | Meaning |
|-------|---------|
| A | Excellent — no issues, all within targets |
| B | Good — minor issues, no critical/high items |
| C | Fair — some issues, at least one high item |
| D | Poor — multiple issues, critical items present |
| F | Critical — immediate action required |

## Dependencies

### Frontend (Bun)
- Outdated packages: ___
- Vulnerabilities: ___ critical, ___ high, ___ medium, ___ low
- Last updated: YYYY-MM-DD

### Backend (Gradle)
- Outdated dependencies: ___
- OWASP vulnerabilities: ___ critical, ___ high, ___ medium, ___ low
- Last updated: YYYY-MM-DD

## Database Migrations

- Applied migrations: ___
- Pending migrations: ___
- Failed migrations: ___
- Last migration: V{version}__{description}.sql

## Tech Debt Summary

| Category | Items | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Security | ___ | ___ | ___ | ___ | ___ |
| Performance | ___ | ___ | ___ | ___ | ___ |
| Readability | ___ | ___ | ___ | ___ | ___ |
| Tests | ___ | ___ | ___ | ___ | ___ |
| Documentation | ___ | ___ | ___ | ___ | ___ |

## Security Status

- **Critical vulnerabilities:** ___ (SLA: 24h)
- **High vulnerabilities:** ___ (SLA: 7d)
- **Container CVEs:** ___
- **Last full audit:** YYYY-MM-DD
- **Secret rotation:** [current / overdue]

## Performance Status

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Frontend bundle (gzip) | ___KB | <150KB | PASS/FAIL |
| Backend p95 latency | ___ms | <500ms | PASS/FAIL |
| Test suite duration | ___s | <300s | PASS/FAIL |
| Build time | ___s | ___ | PASS/FAIL |

## Active Deprecations

- Total active: ___
- Due for removal: ___ (in next major version)
- Missing migration guides: ___

## Action Items (Prioritized)

1. [CRITICAL] ___
2. [HIGH] ___
3. [HIGH] ___
4. [MEDIUM] ___
5. [MEDIUM] ___
```

---

## Reference Files

| Reference | Content |
|-----------|---------|
| `references/dependency-update-checklist.md` | Step-by-step dependency update checklist, rollback procedures |
| `references/migration-template.md` | Flyway migration templates for common schema changes |
| `references/tech-debt-plan-template.md` | Tech debt reduction plan template with tracking |
| `references/performance-audit-template.md` | Performance audit report template with benchmark targets |
| `references/deprecation-template.md` | Deprecation notice, migration guide, and removal tracking templates |

---

## Rules

1. **Never skip tests after updates** — every dependency update must pass full test suite
2. **Always include rollback SQL** — every migration must have a documented rollback
3. **Follow priority order** — Security → Performance → Readability → Tests → Docs
4. **Deprecation before removal** — never remove a feature without a deprecation cycle
5. **Automate what you can** — use scripts for repetitive maintenance tasks
6. **Document every change** — all maintenance actions go in CHANGELOG
7. **Test in staging first** — never apply migrations or patches directly to production
8. **Respect SLAs** — security patches must meet their severity deadline
9. **Keep a paper trail** — all maintenance reports are committed to `docs/maintenance/`
10. **Verify, don't assume** — run actual commands, don't trust stale documentation
