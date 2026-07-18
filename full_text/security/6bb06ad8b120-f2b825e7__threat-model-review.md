---
name: threat-model-review
description: >-
  Reviews threat models for completeness, accuracy, and alignment with current
  implementation. Identifies drift between threat model and code, uncovered
  attack surfaces, missing STRIDE categories, incorrect risk scores, and
  unlinked mitigations. Creates threat models when none exist. Use when
  auditing a threat model, checking security coverage, finding unmodeled
  threats, validating risk scores, or when implementation has changed since
  the threat model was written. Triggers: review threat model, audit threats,
  threat model drift, security coverage, unmodeled threats, validate risk,
  threat model gaps.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep Bash(find *) Bash(ls *) Bash(git log *)
hooks:
  SessionStart:
    - hooks:
        - type: prompt
          prompt: |
            Context was compacted. Re-assess threat model review state per /threat-model-review instructions:
            - Check which threat models exist and their coverage
            - Review STRIDE analysis completeness for current implementation
            - Identify unmodeled threats or missing mitigations
            - Continue threat model review from current state
            - Validate that mitigations link to ADRs and spec requirements
  Stop:
    - hooks:
        - type: command
          command: python3 "$HOME/.claude/skills/threat-model-review/scripts/check-completion.py"
          timeout: 120
compatibility: >-
  Hook paths assume global install at $HOME/.claude/skills/threat-model-review/.
  Adjust the hook command path if you install skills elsewhere.
---

# Threat Model Review

Check whether your threat model still reflects reality. Systems change — new endpoints get added, authentication flows evolve, dependencies update, and infrastructure shifts. If you haven't reviewed your threat model recently, it's probably out of date. This skill identifies where the threat model has drifted from what's actually deployed, discovers unmodeled attack surfaces, and validates that risk scores and mitigations aren't stale.

## Quick Start

A threat model review answers: **Is the DFD current?** (does it match what's actually deployed?), **Are all threats identified?** (did STRIDE analysis miss anything?), **Are risk scores accurate?** (have mitigations changed the picture?), and **Are mitigations tracked?** (do they link to spec requirements and ADRs?). When no threat model exists, this skill creates one first using `threat-model-create`.

The built-in Stop hook keeps the review running until all gates pass — you don't need to re-invoke it manually. See [HOOKS.md](HOOKS.md) for details.

**Running in opencode:** the `hooks:` frontmatter is ignored, so the loop isn't automatic. Either re-run the skill until it reports no gaps, or opt into the `.opencode/plugins/completion-loop.ts` plugin by setting `OPENCODE_REVIEW_LOOP=threat-model-review` while it runs. Tool-name mapping is in [docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

## When to Use This Skill

- Implementation has changed since the threat model was last updated
- New features added trust boundaries, data flows, or external integrations
- Preparing for a security audit or compliance review
- The `spec-review` or `adr-review` skill flagged security gaps
- A project has no threat model and needs one created
- Dependencies were updated and may introduce new attack surface
- A security incident revealed threats the model didn't cover

## Workflow

```
Threat Model Review Progress:
- [ ] Phase 1: Locate and inventory threat model
- [ ] Phase 2: DFD validation (model vs. implementation)
- [ ] Phase 3: STRIDE coverage check
- [ ] Phase 4: Risk score validation
- [ ] Phase 5: Mitigation and cross-reference audit
- [ ] Phase 6: Report findings
```

### Phase 1: Locate and Inventory

**Find existing threat models:**

```bash
find docs/threat-models/ -name "*.md" -type f 2>/dev/null
find docs/ -name "*threat*" -o -name "*security*" 2>/dev/null
```

**If no threat model exists:**
- Alert the user: "No threat model found. I'll analyze the system and create one."
- Use `threat-model-create` to produce a threat model from codebase analysis
- Mark the newly created model's date so future reviews can track drift
- Then continue with review phases below

**If threat models exist, inventory them:**
- Count DFD elements (entities, processes, stores, flows)
- Count identified threats and their severities
- Note the last-modified date
- Check which STRIDE categories are covered

### Phase 2: DFD Validation

Compare the threat model's Data Flow Diagram against the actual implementation. This is where most drift hides — it's the highest-value check you'll do.

**Check external entities:**
- Are all current users/roles represented?
- Have new third-party integrations been added?
- Were any external services removed?
- Are trust levels still correct for each entity?

**Check processes:**
```bash
# Find all services/handlers
grep -r "fn main\|func main\|if __name__\|app.listen\|server.start" --include="*.rs" --include="*.go" --include="*.py" --include="*.js" --include="*.ts" -l
```

- Are all current services represented in the DFD?
- Have any been added, removed, or split?
- Do process descriptions match current responsibilities?
- Have any processes changed their privilege level or data access patterns?

**Check data stores:**
```bash
# Find database/storage references
grep -r "DATABASE_URL\|REDIS_URL\|S3_BUCKET\|connection_string\|create_pool" --include="*.rs" --include="*.py" --include="*.go" --include="*.js" --include="*.env*" --include="*.toml" -l
```

- Are all current databases, caches, and storage systems in the DFD?
- Have data sensitivity levels changed?

**Check data flows:**
- Are all API endpoints represented?
- Have protocols changed (HTTP → gRPC, REST → WebSocket)?
- Are inter-service communication patterns current?
- Are there new data flows crossing trust boundaries that weren't in the model?

**Check trust boundaries:**
- Have new network boundaries been introduced? (new container, new service mesh)
- Have authentication boundaries changed?
- Are new authorization levels represented?
- Have container or process isolation boundaries shifted?

**Document DFD drift:**

```markdown
| DFD Element | In Model | In Code | Status |
|---|---|---|---|
| Redis cache | Yes | Yes | Current |
| S3 file storage | No | Yes | **Missing from model** |
| Memcached | Yes | No | **Removed from code** |
| WebSocket endpoint | No | Yes | **Missing from model** |
```

### Phase 3: STRIDE Coverage Check

For each DFD element (current, not from the stale model), verify STRIDE was applied:

**External Entities** — should have Spoofing + Repudiation analysis:
- [ ] Can each entity be impersonated?
- [ ] Can each entity deny actions?

**Processes** — should have all six categories:
- [ ] Spoofing: Can the process be impersonated?
- [ ] Tampering: Can inputs be manipulated?
- [ ] Repudiation: Are actions logged?
- [ ] Information Disclosure: Does it leak sensitive data?
- [ ] Denial of Service: Can it be overwhelmed?
- [ ] Elevation of Privilege: Can authorization be bypassed?

**Data Stores** — should have Tampering + Information Disclosure + DoS:
- [ ] Can data be modified without authorization?
- [ ] Can data be accessed without authorization?
- [ ] Can storage be exhausted?
- [ ] Are backups and replicas protected to the same standard as the primary store?

**Data Flows** — should have Tampering + Information Disclosure + DoS:
- [ ] Can data be modified in transit?
- [ ] Can data be intercepted?
- [ ] Can the flow be disrupted?
- [ ] Is encryption enforced end-to-end for sensitive data crossing trust boundaries?

**Flag uncovered combinations:**

```markdown
| Element | Missing STRIDE Category | Recommended Analysis |
|---|---|---|
| P-3: Payment Service | Repudiation | Are payment actions audit-logged? |
| DF-7: Webhook delivery | DoS | Can webhook targets slow/block the system? |
| DS-2: Redis cache | Information Disclosure | Is cached data encrypted? |
```

### Phase 4: Risk Score Validation

For each existing threat entry, check whether the scores still make sense:

**Check if DREAD scores are still accurate:**
- Has the Damage potential changed? (more users, more sensitive data)
- Have Reproducibility or Exploitability changed? (new protections, new exposure, public exploit released, tooling available)
- Have Affected Users or Discoverability changed? (user base grew, new user types, new documentation or exposure)
- Has the broader risk context shifted since the original scoring? (new regulations, changed deployment model, different threat actors)

**Check if severity mapping is current:**
- Were any threats scored before mitigations but not re-scored after?
- Do any Critical threats still have "Not Started" mitigation status?
- Are there threats scored Low that should be higher given new context?
- Have any mitigations been removed or degraded, requiring a re-score upward?

**Check for score consistency:**
- Similar threats should have similar scores
- A SQL injection on a public endpoint shouldn't be scored lower than a missing HSTS header

### Phase 5: Mitigation and Cross-Reference Audit

**Mitigation status check (see `artifact-status-tracking` rule for valid values):**

The iterate skill's completion check script parses `**Status:**` lines within each `### TM-XXX-NNN:` entry. Only these status values are recognized:

| Status | Meaning | Iterate blocks? |
|---|---|---|
| `**Status:** Not Started` | No work done | Yes (P0) |
| `**Status:** ⚠️ **PARTIAL** (details...)` | Some mitigations done | Yes (P1) |
| `**Status:** ✅ **DESIGNED** — description` | ADR exists, code not written | Yes (P1) |
| `**Status:** ✅ **IMPLEMENTED** (SR-NNN complete, date)` | Code + tests verified | No |

**Validate during review:**
- [ ] Every threat entry has a `**Status:**` line using one of the values above
- [ ] Every threat with DREAD >= 11 has a mitigation
- [ ] Mitigation statuses are current (not "Not Started" for months while code exists)
- [ ] Entries marked `IMPLEMENTED` reference a specific SR-NNN and include a verification date
- [ ] Entries marked `PARTIAL` list what's done and what remains
- [ ] "Accepted" risks have documented justification
- [ ] No non-standard status values (e.g., "In Progress", "WIP", "Done" — these won't be tracked)

**Verify mitigations are actually in place:**

For each "Implemented" or "Verified" mitigation:
```bash
# Example: check if rate limiting exists for a login endpoint
grep -r "rate.limit\|throttle\|limiter" --include="*.rs" --include="*.py" --include="*.go" --include="*.js" -l
```

**Cross-reference to specs:**
- [ ] Mitigations trace to spec requirements (FR-XXX or NFR-XXX)
- [ ] Spec requirements with security implications trace back to threats
- [ ] No broken links between threat IDs and spec requirement IDs
- [ ] Newly added spec requirements have been checked for threat model coverage

**Cross-reference to ADRs:**
- [ ] Security decisions trace to ADRs
- [ ] ADRs for security choices reference the threats they address
- [ ] No broken links between threat IDs and ADR identifiers
- [ ] Superseded ADRs haven't orphaned their linked threat mitigations

**Flag missing connections:**

```markdown
| Threat ID | Missing Link | Action |
|---|---|---|
| TM-AUTH-001 | No spec requirement | Add FR-XXX for rate limiting |
| TM-DATA-003 | No ADR | Document encryption decision via /adr-create |
| TM-SESSION-002 | Mitigation "Implemented" but code not found | Verify or update status |
```

### Phase 6: Report Findings

Write the report to `docs/threat-model-review-report.md` (the Stop hook checks this location).

```markdown
## Threat Model Review Report

### Summary
- **Threats reviewed:** [count]
- **DFD elements current:** [X] of [Y]
- **Missing DFD elements:** [count]
- **Uncovered STRIDE categories:** [count]
- **Stale risk scores:** [count]
- **Mitigation status issues:** [count]

### DFD Drift
[Table from Phase 2]

### Missing STRIDE Coverage
[Table from Phase 3]

### Risk Score Issues
| Threat | Current Score | Recommended Score | Reason |
|---|---|---|---|
| TM-AUTH-001 | 25 (High) | 35 (High) | User base grew 10x |
| TM-DATA-002 | 33 (High) | 20 (Medium) | Encryption now implemented |

### Mitigation Issues
| Threat | Issue | Action |
|---|---|---|
| TM-AUTH-003 | Status "In Progress" since 6 months | Verify or escalate |
| TM-DATA-001 | Marked "Implemented" but not in code | Investigate |

### New Threats Discovered
[Threats identified during the review that weren't in the original model]

### Recommendations
[Prioritized: 1) Address new critical/high threats, 2) Update DFD,
3) Fix stale scores, 4) Update mitigation statuses, 5) Add cross-references]
```

## Writing Style

Apply the `natural-writing-style` skill. Findings should be specific and actionable. "TM-AUTH-001 was scored at 25 (High) before rate limiting was implemented; with rate limiting now in place on the login endpoint, the Exploitability factor drops from 8 to 4, bringing the score to 21 (Medium)" is useful. "Some risk scores may need updating" is not.

State what you examined and what you didn't. Don't claim a threat model review is "thorough" or "complete" — it's always a snapshot of what you looked at. You can't catch everything, but you can be honest about what wasn't covered.

## Resources

- [Review Checklist](references/review-checklist.md) — Detailed threat model review criteria
- [Stop Hook](HOOKS.md) — Auto-continuation hook that keeps the review going until all gates pass
