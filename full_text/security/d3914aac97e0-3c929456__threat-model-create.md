---
name: threat-model-create
description: >-
  Creates and updates threat models using STRIDE-per-element analysis, DREAD
  risk scoring, and Data Flow Diagram decomposition. Handles new projects,
  existing systems without threat models, and updating models when
  implementation changes. Links threats to spec requirements and ADRs for
  mitigation tracking. Use when creating a threat model, analyzing security
  threats, performing STRIDE analysis, assessing attack surface, updating
  a threat model after changes, or when spec-create flags missing security
  analysis. Triggers: threat model, STRIDE, security analysis, attack surface,
  identify threats, risk assessment, create threat model.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep Bash(find *) Bash(ls *) AskUserQuestion
---

# Threat Model Create

Systematically identify what can go wrong with your system and figure out what you're going to do about it. This skill produces threat models using STRIDE for threat identification and DREAD for risk scoring, built on Data Flow Diagrams with explicit trust boundaries. It works for new systems being designed and existing systems that don't have security analysis yet.

## Quick Start

A threat model answers four questions: **What are we building?** (system decomposition) **What can go wrong?** (STRIDE threats) **How bad is it?** (DREAD scoring) **What are we going to do about it?** (mitigations). Every identified threat gets a unique ID (`TM-XXX`), a severity score, and traces to spec requirements and ADRs that implement its mitigations. If you don't have a threat model, you're flying blind on security.

## When to Use This Skill

- Designing a new system and need to identify security risks before building
- An existing system has no threat model and needs retroactive analysis
- Implementation has changed and the threat model needs updating
- The `spec-create` skill flagged security requirements without threat analysis
- Preparing for a security review or audit
- A new feature introduces new trust boundaries, data flows, or external integrations

For code-level vulnerability scanning (buffer overflows, injection flaws), use `c-security-review` or `rust-unsafe-ffi-review` instead. This skill doesn't dig into individual lines of code — it's focused on the *architectural* level.

## Workflow

```
Threat Model Progress:
- [ ] Phase 1: System decomposition
- [ ] Phase 2: Threat identification (STRIDE)
- [ ] Phase 3: Risk assessment (DREAD)
- [ ] Phase 4: Mitigation planning
- [ ] Phase 5: Cross-reference and validate
```

### Phase 1: System Decomposition

Scan for entry points, config files, and existing docs first, then **use `AskUserQuestion`** to confirm scope: "I found [X entry points / Y services]. Is this a new system design or an existing one needing retroactive analysis? Any particular trust boundaries or data flows I should focus on?"

**Build a Data Flow Diagram (DFD)** — see [references/dfd-construction.md](references/dfd-construction.md) for detailed guidance.

Identify these elements:

**External Entities** — actors outside the system boundary:
- Users (authenticated, unauthenticated, admin)
- Third-party services (payment processors, auth providers, APIs)
- Partner systems and B2B integrations
- Automated clients (bots, scrapers, CI/CD pipelines)

**Processes** — code that transforms data:
- Web servers, API handlers, background workers
- Authentication services, authorization middleware
- Data processing pipelines
- Scheduled tasks and cron jobs

**Data Stores** — where data lives:
- Databases, caches, file systems
- Message queues, log stores
- Secrets stores, config files
- Temporary storage (upload directories, session files)

**Data Flows** — how data moves between elements:
- HTTP/HTTPS requests and responses
- Database queries and results
- Inter-service communication (gRPC, message queues)
- File reads and writes

**Trust Boundaries** — where trust levels change:
- Internet → DMZ → Internal network
- Unauthenticated → Authenticated
- User role → Admin role
- Application → Database
- Your code → Third-party code
- Container → Host OS

**For existing systems**, derive the DFD from the codebase:

```bash
# Find entry points
find . -name "*.rs" -o -name "*.py" -o -name "*.go" -o -name "*.js" | head -20
# Check for API routes, database connections, external service calls
grep -r "route\|handler\|endpoint\|connect\|fetch\|http" --include="*.rs" -l
```

Read configuration files, Docker setup, and infrastructure code to map the deployment architecture. You'll often find connections here that aren't obvious from the source code alone.

### Phase 2: Threat Identification (STRIDE)

Apply STRIDE to each DFD element. See [references/stride-guide.md](references/stride-guide.md) for the complete mapping.

**Which threats apply to which elements:**

| Element Type | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| External Entity | X | | X | | | |
| Process | X | X | X | X | X | X |
| Data Store | | X | | X | X | |
| Data Flow | | X | | X | X | |

For each applicable threat, document:

```markdown
### TM-[COMPONENT]-NNN: [Threat Title]

**Element:** [DFD element name]
**Category:** [Spoofing | Tampering | Repudiation | Information Disclosure | DoS | Elevation of Privilege]
**Description:** [What could happen — be specific, not vague]
**Attack Vector:** [How an attacker would exploit this]
**Affected Assets:** [What data or functionality is at risk]
```

**Common threats by category:**

| Category | Violated Property | Typical Threats |
|---|---|---|
| **Spoofing** | Authentication | Credential theft, session hijacking, token forgery |
| **Tampering** | Integrity | SQL injection, request modification, config manipulation |
| **Repudiation** | Non-repudiation | Missing audit logs, unsigned transactions |
| **Info Disclosure** | Confidentiality | Data leaks, verbose errors, missing encryption |
| **Denial of Service** | Availability | Resource exhaustion, algorithmic complexity attacks |
| **Elevation of Privilege** | Authorization | IDOR, privilege escalation, missing authz checks |

### Phase 3: Risk Assessment (DREAD)

Score each threat using DREAD (see [references/dread-scoring.md](references/dread-scoring.md)):

| Factor | Question | 0-10 Scale |
|---|---|---|
| **Damage** | How bad if exploited? | 0=none, 10=complete compromise |
| **Reproducibility** | How easy to reproduce? | 0=very hard, 10=always works |
| **Exploitability** | How much skill/tooling needed? | 0=expert only, 10=script kiddie |
| **Affected Users** | How many users impacted? | 0=none, 10=all users |
| **Discoverability** | How easy to find? | 0=hidden, 10=obvious |

**Total = D + R + E + A + D** (0-50)

| Score Range | Severity | Response Time |
|---|---|---|
| 40-50 | Critical | Address within 72 hours |
| 25-39 | High | Resolve within 2 weeks |
| 11-24 | Medium | Resolve within 1 month |
| 1-10 | Low | Monitor quarterly |

Add the scoring to each threat entry:

```markdown
**DREAD Score:** D:8 R:7 E:6 A:9 D:5 = **35 (High)**
```

### Phase 4: Mitigation Planning

For each threat, choose a response:

| Response | When to Use |
|---|---|
| **Mitigate** | Implement a control to reduce risk (most common) |
| **Accept** | Risk is low enough to live with (document why) |
| **Transfer** | Shift risk to another party (insurance, SLA, managed service) |
| **Eliminate** | Remove the feature or component that creates the risk |

Document mitigations with implementation status. See the global `artifact-status-tracking` rule for how these statuses integrate with the iterate skill's completion checking.

**IMPORTANT:** Use ONLY these status values — the iterate completion script parses them to determine remaining implementation work.

| Status Value | When to use | Iterate blocks? |
|---|---|---|
| `**Status:** Not Started` | Mitigation not begun | Yes (P0) |
| `**Status:** ⚠️ **PARTIAL** (details...)` | Some criteria met, work remains | Yes (P1) |
| `**Status:** ✅ **DESIGNED** — ADR-NNN describes approach` | Architecture decided, code not written | Yes (P1) |
| `**Status:** ✅ **IMPLEMENTED** (SR-NNN complete, date)` | Code written, tested, verified | No |

```markdown
**Mitigation:** Implement rate limiting on login endpoint (max 6 attempts per minute)
**Status:** Not Started
**ADR:** [ADR-008: Rate Limiting Strategy](../adr/0008-rate-limiting.md)
**Spec Requirement:** [FR-012](../specs/auth-spec.md#fr-012)
```

**Updating status during implementation:** When mitigations are partially or fully implemented, update the `**Status:**` line to reflect progress. Include the SR reference and date when marking as IMPLEMENTED. The iterate skill re-checks these on every cycle — gaps close automatically as you update statuses.

**Standard mitigations by STRIDE category:**

| Category | Standard Mitigations |
|---|---|
| Spoofing | MFA, certificate pinning, strong session tokens |
| Tampering | Input validation, integrity hashing, digital signatures |
| Repudiation | Audit logging, signed transactions, tamper-evident logs |
| Info Disclosure | Encryption (at rest + in transit), access controls, minimal error messages |
| DoS | Rate limiting, resource quotas, circuit breakers, CDN |
| Elevation of Privilege | RBAC/ABAC, least privilege, authorization at every layer |

### Phase 5: Cross-Reference and Validate

**Link to spec requirements.** Every mitigation should trace to a spec requirement:

```markdown
> TM-AUTH-001 mitigation → FR-007: Password Hashing (SPEC)
> TM-AUTH-001 decision → ADR-005: Bcrypt for Password Hashing
```

**Link to ADRs.** Security decisions (encryption algorithm, auth mechanism, rate limiting strategy) should have ADRs:

```markdown
> **Missing ADR:** The choice of bcrypt over argon2 for password hashing
> should be documented. Run `adr-create` to capture this decision.
```

**Flag missing spec requirements:**

```markdown
> **Missing Spec Requirement:** TM-SESSION-002 identifies session fixation
> risk, but no spec requirement mandates session rotation after login.
> Run `spec-create` to add this requirement.
```

**Validate completeness:**

- [ ] Every DFD element has been analyzed against applicable STRIDE categories
- [ ] Every trust boundary crossing is documented
- [ ] Every threat has a DREAD score
- [ ] Every threat with score >= 11 has a mitigation plan
- [ ] Every mitigation traces to a spec requirement or ADR
- [ ] Critical and High threats have concrete implementation plans
- [ ] Assumptions are documented (each assumption is a risk if wrong)
- [ ] Residual risks are acknowledged

## Output Location

Save threat models to `docs/threat-models/` in the project:

```
docs/threat-models/
├── system-threat-model.md        # Full system threat model
├── auth-threat-model.md          # Authentication-specific model
├── data-pipeline-threat-model.md # Data handling threats
└── template.md                   # Project-specific template
```

## Updating Existing Threat Models

When the system changes:

1. **Read the current threat model** and identify what's changed in the DFD elements
2. **Add new elements** — new services, data stores, or external integrations
3. **Re-analyze changed trust boundaries** — did a new data flow cross a boundary?
4. **Add new threats** with the next available `TM-XXX` ID
5. **Re-score existing threats** if mitigations were implemented (update status)
6. **Don't delete old threats** — mark them as "Eliminated" if the attack surface was removed
7. **Update the changelog** at the bottom of the threat model

## Writing Style

Apply the `natural-writing-style` skill. Threat descriptions should be concrete and specific — "an attacker can steal session tokens by sniffing unencrypted HTTP traffic" is useful; "security could be compromised" is not.

State what you analyzed and what you didn't. Don't claim a threat model is "complete" — you can only state what was examined and what was found.

## Resources

- [STRIDE Guide](references/stride-guide.md) — Complete STRIDE-per-element analysis methodology
- [DREAD Scoring](references/dread-scoring.md) — Risk scoring rubric with calibration examples
- [DFD Construction](references/dfd-construction.md) — How to build Data Flow Diagrams
- [Threat Model Template](assets/threat-model-template.md) — Copy-paste starter template
