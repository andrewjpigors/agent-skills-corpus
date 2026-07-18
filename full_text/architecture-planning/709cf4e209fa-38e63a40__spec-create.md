---
name: spec-create
description: >-
  Creates and updates implementation specifications using IEEE 830 structure,
  RFC 2119 requirement levels, EARS syntax, and Gherkin acceptance criteria.
  Produces traceable, testable specs with cross-references to ADRs and threat
  models. Use when writing a spec, creating a specification document, defining
  requirements, documenting acceptance criteria, or updating an existing spec
  to cover new functionality. Triggers: write spec, create specification,
  document requirements, define acceptance criteria, update spec, spec gaps.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep AskUserQuestion Bash(find *) Bash(ls *)
---

# Spec Create

Write implementation specifications that are testable, traceable, and unambiguous. This skill handles both greenfield specs and updating existing ones to cover new functionality or retroactively document what's already built.

## Quick Start

A spec captures **what** to build, **why** it matters, **how** you'll verify it's done, and **where** architectural decisions and security constraints come from. Every requirement gets a unique ID (`SPEC-001`), uses RFC 2119 keywords for precision, and traces to test cases, ADRs, and threat model entries.

When you don't have existing documentation, analyze the codebase directly — read the code, infer intent, and produce the spec from what's actually there.

## When to Use This Skill

- Starting a new feature or system and need a formal spec before coding
- Retroactively documenting an existing system that lacks a spec
- Updating an existing spec after new features were added without spec updates
- Breaking a large initiative into testable, traceable requirements
- Connecting requirements to ADRs (`adr-create`) and threat models (`threat-model-create`)

Don't use this for quick task breakdowns — that's what `spec-writing` handles (TDD-style task lists with code snippets).

## Workflow

```
Spec Creation Progress:
- [ ] Phase 1: Discovery and existing artifact scan
- [ ] Phase 2: Requirements elicitation
- [ ] Phase 3: Draft spec document
- [ ] Phase 4: Cross-reference ADRs and threat model
- [ ] Phase 5: Validate completeness
```

### Phase 1: Discovery

**Scan for existing artifacts first.** Don't create from scratch if documentation already exists.

```bash
# Check for existing specs, ADRs, and threat models
find docs/ -name "*.md" -type f 2>/dev/null | head -20
ls docs/specs/ docs/adr/ docs/threat-models/ 2>/dev/null
```

**If specs exist:** Read them, identify gaps against the current codebase, and update. Jump to Phase 2 with "update" intent.

**If no specs exist:** Analyze the codebase to understand what's been built:

- Read key entry points (main files, route definitions, API handlers)
- Identify data models, persistence layer, and caching strategy
- Map external dependencies and integrations
- Note configuration, environment requirements, and deployment setup

**Check for related artifacts:**
- Existing ADRs → Extract decisions that constrain the spec
- Existing threat model → Extract security requirements
- README or design docs → Extract stated goals and architecture

### Phase 2: Requirements Elicitation

**For new features:** Gather requirements through discussion. Use AskUserQuestion to clarify:

- What's the goal? What problem does this solve?
- Who are the stakeholders? What roles interact with this?
- What are the non-negotiable constraints (performance, security, compliance)?
- What's explicitly out of scope?

**For existing systems:** Derive requirements from the implementation:

- Each API endpoint becomes a functional requirement
- Each data model becomes a data requirement
- Each integration becomes an interface requirement
- Each error handler reveals an edge case requirement
- Each test reveals an acceptance criterion
- Each configuration option becomes a deployment or operational requirement

**For updates:** Diff what the spec says against what the code does. New code paths without spec coverage become new requirements.

### Phase 3: Draft the Spec

Use the full template from [references/srs-template.md](references/srs-template.md). Every spec starts with the RFC 2119 boilerplate:

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

**Write requirements using EARS syntax** (see [references/ears-patterns.md](references/ears-patterns.md)):

| Pattern | Template | When to use |
|---|---|---|
| Ubiquitous | The `<system>` SHALL `<response>` | Always-active behavior |
| Event-driven | **When** `<trigger>`, the `<system>` SHALL `<response>` | Triggered behavior |
| State-driven | **While** `<precondition>`, the `<system>` SHALL `<response>` | Conditional on state |
| Optional | **Where** `<feature>`, the `<system>` SHALL `<response>` | Feature flags |
| Unwanted | **If** `<condition>`, **then** the `<system>` SHALL `<response>` | Error handling |

**Write acceptance criteria in Gherkin** (see [references/gherkin-guide.md](references/gherkin-guide.md)):

```gherkin
Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given a registered user with email "alice@example.com"
    And the user has password "correct-password"
    When the user submits login with email "alice@example.com" and password "correct-password"
    Then the response status MUST be 200
    And the response MUST contain a valid JWT token
    And the JWT token MUST expire in 30 days

  Scenario: Login fails with wrong password
    Given a registered user with email "alice@example.com"
    When the user submits login with email "alice@example.com" and password "wrong-password"
    Then the response status MUST be 401
    And the response MUST NOT reveal whether the email exists
```

**Assign unique IDs** to every requirement: `SPEC-001`, `SPEC-002`, etc. Group by category:

- `FR-001` through `FR-NNN` for functional requirements
- `NFR-001` through `NFR-NNN` for non-functional requirements
- `IR-001` through `IR-NNN` for interface requirements
- `DR-001` through `DR-NNN` for data requirements

### Phase 4: Cross-Reference

**Link to ADRs.** Every technology choice or architectural decision in the spec should trace to an ADR:

```markdown
## FR-003: Session Storage

The system SHALL store user sessions in Redis with a 30-day TTL.

- **Rationale:** See [ADR-002: Use Redis for Session Storage](../adr/0002-use-redis-for-sessions.md)
- **Security:** See [TM-AUTH-003: Session Hijacking](../threat-models/auth-threat-model.md#tm-auth-003)
```

**Link to threat model.** Security-relevant requirements should reference specific threats:

```markdown
## FR-007: Password Hashing

The system SHALL hash passwords using bcrypt with a cost factor of at least 12.

- **Threat:** [TM-AUTH-001: Credential Theft](../threat-models/auth-threat-model.md#tm-auth-001)
- **Decision:** [ADR-005: Bcrypt for Password Hashing](../adr/0005-bcrypt-passwords.md)
```

**If ADRs or threat models don't exist yet**, note where they're needed:

```markdown
> **Missing ADR:** This requirement implies a technology decision (Redis vs alternatives)
> that should be documented. Run `adr-create` to capture this decision.

> **Missing Threat Model Entry:** This requirement has security implications not yet
> covered by the threat model. Run `threat-model-create` to analyze.
```

### Phase 5: Validate

Build a Requirements Traceability Matrix (see [references/traceability-matrix.md](references/traceability-matrix.md)):

| Req ID | Description | Test Case | ADR | Threat Model | Status |
|---|---|---|---|---|---|
| FR-001 | User login | TC-001, TC-002 | ADR-002 | TM-AUTH-001 | Implemented |
| FR-002 | Session expiry | TC-003 | ADR-002 | TM-AUTH-003 | In Progress |
| FR-003 | Password reset | — | — | — | **Gap** |

**Empty cells are gaps.** Every requirement needs at least one test case. Security requirements need a threat model entry. Architectural choices need an ADR.

Run the validation checklist:

- [ ] Every requirement has a unique ID
- [ ] Every requirement uses RFC 2119 keywords correctly
- [ ] Every requirement follows an EARS pattern
- [ ] Every functional requirement has Gherkin acceptance criteria
- [ ] Security requirements trace to threat model entries
- [ ] Architectural decisions trace to ADRs
- [ ] Traceability matrix has no empty cells in critical columns
- [ ] No requirement uses vague terms ("fast", "user-friendly", "secure")
- [ ] Non-functional requirements have measurable thresholds

## Output Location

Save specs to `docs/specs/` in the project:

```
docs/specs/
├── feature-name-spec.md     # Feature-specific spec
├── api-spec.md              # API contract specification
└── system-spec.md           # System-level specification
```

## Implementation Tracking in Specs

Specs use `### Task N:` sections with `**File:**` markers pointing to implementation files. The iterate skill's completion check script verifies these files exist — missing files are flagged as P1 gaps.

**IMPORTANT:** When writing spec tasks, always include accurate `**File:**` markers pointing to the actual (or planned) implementation location:

```markdown
### Task 1: Implement urgency calculation

**File:** `crates/donbiki-tasks/src/urgency.rs`

**Test:**
```rust
#[test]
fn test_urgency_overdue() { ... }
```
```

The iterate script checks:
- `**File:**` references → file must exist in the codebase (P1 gap if missing)
- `**Test File:**` references → test file must exist (P2 gap if missing)

See the global `artifact-status-tracking` rule for how spec tracking integrates with the iterate skill across all artifact types.

## Updating Existing Specs

When a spec already exists but needs updating:

1. **Read the current spec** and map its requirement IDs
2. **Scan the codebase** for functionality not covered by existing requirements
3. **Add new requirements** with the next available IDs (don't renumber existing ones)
4. **Mark deprecated requirements** as `[DEPRECATED]` — don't delete them
5. **Update the traceability matrix** to reflect current state
6. **Verify `**File:**` markers** still point to existing files (rename if code was moved)
7. **Add a changelog entry** at the bottom of the spec

## Writing Style

Apply the `natural-writing-style` skill to all prose sections. Requirements themselves are formal (RFC 2119 keywords), but context sections, rationale, and descriptions should read naturally. Don't write "the system shall enable user interaction" — write "the system SHALL let users log in."

Verify: no unsubstantiated claims about completeness. State what you analyzed, what you covered, and what remains unexamined.

## Resources

- [SRS Template](references/srs-template.md) — Full specification document structure
- [EARS Patterns](references/ears-patterns.md) — Requirement syntax patterns with examples
- [Gherkin Guide](references/gherkin-guide.md) — Acceptance criteria format
- [Traceability Matrix](references/traceability-matrix.md) — RTM template and guidance
- [Spec Template](assets/spec-template.md) — Copy-paste starter template
