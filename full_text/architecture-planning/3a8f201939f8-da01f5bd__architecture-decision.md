---
name: architecture-decision
description: "Creates or retrofits an Architecture Decision Record (ADR) documenting a significant technical decision, context, alternatives, consequences, engine compatibility, GDD traceability, registry impact, review evidence, and safe downstream synchronization."
argument-hint: "[title] [--review full|lean|solo] [--dry-run] OR retrofit <docs/architecture/adr-NNNN-title.md> [--review full|lean|solo] [--dry-run]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

# Architecture Decision Skill

## Skill Name

architecture-decision

## Mission

Create or retrofit Architecture Decision Records that are clear, evidence-backed, engine-version-aware, registry-consistent, GDD-traceable, reviewable, and safe to use as project architecture source of truth.

This skill supports two modes:

1. **Create New ADR**
   - Generate a new ADR under `docs/architecture/`.
   - Discover engine context.
   - Check existing ADRs and registry stances.
   - Evaluate alternatives.
   - Draft a complete ADR.
   - Run configured review flow.
   - Write the ADR if not in `--dry-run`.
   - Optionally update registry, GDDs, and story statuses only after explicit approval.

2. **Retrofit Existing ADR**
   - Read an existing ADR under `docs/architecture/adr-*.md`.
   - Detect missing required governance sections.
   - Preview append-only additions.
   - Append only after explicit user approval.
   - Never rewrite existing ADR content in retrofit mode.

The core question for this skill is:

> Can this architecture decision be safely documented, reviewed, traced, and synchronized without creating hidden conflicts, stale contracts, or unsupported authority?

---

## Operating Principles

1. **Evidence over assertion**
   - Do not claim engine compatibility, registry alignment, GDD sync, or review approval unless the relevant evidence exists.

2. **Architecture decisions are source-of-truth artifacts**
   - ADRs must be specific, durable, and traceable.
   - ADRs must record context, alternatives, consequences, risks, validation, and dependencies.

3. **Local engine-reference docs are authoritative**
   - Engine compatibility must be verified from local `docs/engine-reference/[engine]/` files.
   - Do not rely on model memory for version-sensitive engine claims.

4. **Path safety is mandatory**
   - Reject unsafe paths before reading or writing.
   - Never write outside approved ADR paths.

5. **Protected writes require approval**
   - New ADR write is authorized by invocation unless `--dry-run` is active.
   - Retrofit append, registry update, GDD update, story-status update, supersession, and scoped exception updates require explicit approval.

6. **Review mode controls validation depth**
   - `full`: Engine Specialist + Technical Director.
   - `lean`: Engine Specialist only.
   - `solo`: no specialist/TD review.
   - Missing review mode defaults to `lean` and must be reported once.

7. **Proposed ADRs are not binding**
   - Registry entries derived from `Proposed` ADRs must be `proposed`.
   - Only accepted ADRs or active registry entries are binding.

8. **Conflicts stop the workflow**
   - Binding registry or ADR conflicts require alignment, explicit supersession, scoped exception, or stop.

9. **Dry-run never writes**
   - In `--dry-run`, perform discovery, drafting, review, and preview only.
   - No files are written.
   - No registry, GDD, or story updates occur.

10. **Retrofit mode is append-only**
    - Existing ADR content must not be edited or rewritten.
    - Missing sections may be appended only after exact preview and approval.

11. **Self-healing before failure escalation**
    - If discovery, validation, review, registry sync, or write behavior fails, classify the failure, contain the risk, recover safely where possible, and report uncertainty.

12. **Bounded self-learning**
    - Lessons may be proposed only from validated ADR outcomes, review findings, registry conflicts, GDD sync issues, or user corrections.
    - Persistent lessons must be explicit, reviewable, reversible, and subordinate to current user instructions and higher-priority project rules.

---

## Scope

This skill governs:

- ADR creation.
- ADR retrofit.
- Engine compatibility review.
- Architecture registry conflict detection.
- Architecture registry update proposals.
- GDD traceability checks.
- GDD sync checks.
- ADR dependency documentation.
- Alternative analysis.
- Consequence and risk documentation.
- Review-mode routing.
- Engine specialist validation.
- Technical Director review.
- Story readiness/update prompts.
- Closing next-action recommendations.

---

## Non-Goals

This skill must not:

- Make the final technical decision without user/project authority.
- Bypass Technical Director rejection in `full` mode.
- Update registry without approval.
- Update GDDs without approval.
- Update story statuses without approval.
- Treat `Proposed` ADRs as binding.
- Rewrite existing ADR content in retrofit mode.
- Read or write unsafe paths.
- Invent engine compatibility facts.
- Claim tests or reviews were run when they were skipped, failed, unavailable, or unsupported.
- Store persistent lessons without reviewable storage and approval.
- Perform deployment, builds, or code implementation.

---

## Input Forms

Supported invocations:

```text
/architecture-decision [title]
/architecture-decision [title] --review full
/architecture-decision [title] --review lean
/architecture-decision [title] --review solo
/architecture-decision [title] --dry-run
/architecture-decision retrofit docs/architecture/adr-0001-event-system.md
/architecture-decision retrofit docs/architecture/adr-0001-event-system.md --review full
/architecture-decision retrofit docs/architecture/adr-0001-event-system.md --dry-run
```

If no title or retrofit path is provided, ask:

```text
What technical decision are you documenting? Provide a short title, for example:
- event-system-architecture
- physics-engine-choice
- save-data-schema
```

Use the response as the ADR title and continue.

---

## Workflow State Labels

Use these labels internally and in status reports where useful:

```text
INVOCATION_PARSED
REVIEW_MODE_RESOLVED
PATH_VALIDATED
PATH_REJECTED
ENGINE_CONTEXT_FOUND
ENGINE_CONTEXT_MISSING
ENGINE_REFERENCE_COMPLETE
ENGINE_REFERENCE_PARTIAL
DOMAIN_IDENTIFIED
DOMAIN_UNCERTAIN
RETROFIT_MODE
NEW_ADR_MODE
DUPLICATE_SCAN_COMPLETE
DUPLICATE_RISK_FOUND
REGISTRY_FOUND
REGISTRY_MISSING
REGISTRY_CONFLICT_FOUND
REGISTRY_ALIGNED
GDD_TRACE_FOUND
GDD_TRACE_MISSING
GDD_SYNC_REQUIRED
ADR_DRAFTED
SPECIALIST_REVIEW_SKIPPED
SPECIALIST_REVIEW_COMPLETE
TD_REVIEW_SKIPPED
TD_APPROVED
TD_CONCERNS
TD_REJECTED
DRY_RUN_COMPLETE
ADR_WRITTEN
RETROFIT_PREVIEW_READY
RETROFIT_APPENDED
REGISTRY_UPDATE_PROPOSED
REGISTRY_UPDATED
REGISTRY_SKIPPED
STORY_UPDATE_PROPOSED
STORY_UPDATED
STORY_SKIPPED
BLOCKED
UNKNOWN
```

### State Rules

- Do not mark `ENGINE_REFERENCE_COMPLETE` if any required engine file is missing.
- Do not mark `REGISTRY_ALIGNED` if registry is missing or unreadable.
- Do not mark `TD_APPROVED` without a valid TD review response.
- Do not mark `ADR_WRITTEN` in `--dry-run`.
- Do not mark `RETROFIT_APPENDED` without explicit approval.
- Do not mark `REGISTRY_UPDATED` without explicit approval.

---

## Failure State Labels

Use these for containment:

```text
INVALID_INVOCATION
UNSAFE_PATH
ENGINE_REFERENCE_BLOCKED
ENGINE_REFERENCE_PARTIAL_RISK
DUPLICATE_DECISION_RISK
ARCHITECTURE_CONFLICT
REGISTRY_PARSE_RISK
GDD_SYNC_RISK
REVIEW_MODE_UNKNOWN
SPECIALIST_REVIEW_FAILED
TD_REVIEW_REJECTED
WRITE_BLOCKED
WRITE_FAILED
PROTECTED_WRITE_REQUIRES_APPROVAL
MISSING_REQUIRED_CONTEXT
DRY_RUN_NO_WRITE
```

---

## Protected Write Matrix

| Operation | Writes? | Approval Required? | Notes |
|---|---:|---:|---|
| New ADR creation | Yes | No, if valid invocation and not dry-run | Primary purpose of skill |
| Retrofit append | Yes | Yes | Append-only |
| Registry update | Yes | Yes | Never automatic |
| GDD update | Yes | Yes | Protected sync |
| Story status update | Yes | Yes | Never automatic |
| Supersession of existing ADR/registry stance | Yes | Yes | Requires explicit decision |
| Scoped architecture exception | Yes | Yes | Requires scope and rationale |
| Dry-run draft | No | No | Preview only |
| Review-mode discovery | No | No | Read-only |

---

## Path Safety

Before reading or writing any user-supplied path:

1. Normalize the path.
2. Reject absolute paths.
3. Reject any path containing `..`.
4. Require retrofit paths to match:

```text
docs/architecture/adr-*.md
```

5. Require new ADR output paths to live under:

```text
docs/architecture/
```

6. If invalid, stop with:

```text
Path rejected: [reason]
```

Do not attempt to recover unsafe paths automatically.

---

## Review Mode Resolution

Resolve review mode once:

1. Explicit `--review full|lean|solo`.
2. Else read:

```text
production/review-mode.txt
```

3. Else default to:

```text
lean
```

### Review Mode Semantics

| Mode | Engine Specialist | Technical Director |
|---|---:|---:|
| `full` | Yes | Yes |
| `lean` | Yes | No |
| `solo` | No | No |

### Review Mode Error Handling

If `production/review-mode.txt` is missing, malformed, or empty:

- default to `lean`,
- report the assumption once,
- continue.

If explicit review mode is invalid:

- ask user to choose `full`, `lean`, or `solo`,
- do not guess.

---

## Phase 1 — Parse Invocation

### New ADR Mode

If the first argument is not `retrofit`, treat the remaining non-flag arguments as the title.

Normalize title into:

- display title,
- slug,
- likely domain,
- likely system name.

### Retrofit Mode

If the first argument is `retrofit`, require a path:

```text
docs/architecture/adr-[NNNN]-[slug].md
```

Validate path before reading.

If no valid path exists, ask for a valid retrofit path.

---

## Phase 2 — Discover Engine Context

This phase applies to:

- new ADRs,
- retrofit mode when adding or validating `## Engine Compatibility`.

### 2.1 Determine Configured Engine

Determine `[engine]` in this order:

1. Read:

```text
.claude/docs/technical-preferences.md
```

and look for the configured engine.

2. Else inspect directories under:

```text
docs/engine-reference/
```

3. If exactly one engine directory exists, use it.
4. If multiple engine directories exist, ask which one applies.
5. If no engine reference exists, stop and ask the user to run `/setup-engine` or provide engine name and version.

### 2.2 Read Engine Reference Files

Read:

```text
docs/engine-reference/[engine]/VERSION.md
docs/engine-reference/[engine]/breaking-changes.md
docs/engine-reference/[engine]/deprecated-apis.md
```

Identify decision domain from:

- title,
- user description,
- GDD context,
- source files,
- related ADRs,
- registry entries.

Common domains:

```text
Physics
Rendering
UI
Audio
Navigation
Animation
Networking
Core
Input
Scripting
Persistence
Tools
Build
AI
Data
Security
Save
```

If a module reference exists, read:

```text
docs/engine-reference/[engine]/modules/[domain].md
```

### 2.3 Missing Engine Files

| Missing File | Behavior |
|---|---|
| `VERSION.md` | Stop. Engine compatibility cannot be verified. |
| `breaking-changes.md` | Continue, but mark knowledge risk at least `MEDIUM`. |
| `deprecated-apis.md` | Continue, but mark deprecated API coverage incomplete. |
| `modules/[domain].md` | Continue, but mark domain reference unavailable. |
| `.claude/docs/technical-preferences.md` | Continue without specialist discovery unless review mode requires it. |
| `.claude/docs/director-gates.md` | In `full` mode, stop and report TD gate config unavailable. |

### 2.4 Engine Compatibility Evidence Record

Use this internally and include relevant data in the ADR:

```md
## Engine Compatibility Evidence

- Engine:
- Version:
- Domain:
- Reference files checked:
- Missing files:
- Deprecated API coverage:
- Breaking changes coverage:
- Module reference status:
- Knowledge risk:
- APIs/patterns requiring verification:
- Verdict:
```

### 2.5 Knowledge-Gap Warning

If domain risk is `MEDIUM` or `HIGH`, show:

```text
⚠️ ENGINE KNOWLEDGE GAP WARNING

Engine: [engine name + version]
Domain: [domain]
Risk Level: [LOW | MEDIUM | HIGH]

Relevant verified changes:
- [change 1]
- [change 2]

This ADR must use the local engine-reference docs as source of truth.
Do not rely only on training data for this decision.
```

---

## Phase 3 — Retrofit Existing ADR

Only run this phase when invocation starts with `retrofit`.

### 3.1 Read and Classify Existing ADR

Read the complete ADR file.

Scan headings and classify missing sections:

| Section | Severity If Missing | Reason |
|---|---|---|
| `## Status` | BLOCKING | Story readiness cannot check ADR acceptance. |
| `## ADR Dependencies` | HIGH | Dependency ordering and unblocking cannot be verified. |
| `## Engine Compatibility` | HIGH | Engine-version risk is unknown. |
| `## GDD Requirements Addressed` | MEDIUM | Requirements traceability is incomplete. |
| `## Registry Impact` | MEDIUM | Registry update intent is ambiguous. |
| `## Sources Consulted` | LOW | Audit trail is incomplete. |
| `## Validation Criteria` | MEDIUM | Acceptance evidence is incomplete. |
| `## Related Decisions` | LOW | Architecture graph is incomplete. |

### 3.2 Retrofit Preview

Show:

```md
## Retrofit: [ADR title]

File: [path]

### Sections already present and will not be touched

✓ Status: [value or "present"]
✓ [section]

### Missing sections that can be appended

✗ Status — BLOCKING
✗ ADR Dependencies — HIGH
✗ Engine Compatibility — HIGH
✗ GDD Requirements Addressed — MEDIUM
✗ Registry Impact — MEDIUM
✗ Sources Consulted — LOW
✗ Validation Criteria — MEDIUM
✗ Related Decisions — LOW
```

Ask:

```text
Shall I prepare and preview the missing sections? I will not modify existing content.

[A] Prepare missing sections
[B] Stop here
```

### 3.3 Gather Missing Retrofit Information

For `## Status`, ask:

```text
What is the current status of this decision?

[A] Proposed
[B] Accepted
[C] Deprecated
[D] Superseded by ADR-XXXX
```

For `## ADR Dependencies`, capture:

```text
Depends On:
Enables:
Blocks:
Ordering Note:
```

Allow `None`.

For `## Engine Compatibility`:

- use Phase 2 engine context,
- ask user to confirm domain only if uncertain.

For `## GDD Requirements Addressed`:

- infer candidates from GDD references,
- ask only if mapping is ambiguous.

For `## Registry Impact`:

- infer candidates from ADR content,
- ask user to confirm if impact is ambiguous or protected.

For `## Sources Consulted`:

- include existing ADR path,
- include engine reference files read,
- include GDDs,
- include registry,
- include related ADRs.

### 3.4 Preview Exact Append

Before writing, show exact Markdown to append.

Ask:

```text
May I append these missing sections to [path]?

[A] Yes — append these sections
[B] Not yet — revise the generated sections
[C] Stop without writing
```

Only append if user selects `[A]`.

### 3.5 Retrofit Write Rules

- Never edit existing content.
- Append only missing sections.
- Do not append duplicate section headings.
- If an existing section is malformed, note it but do not rewrite it.
- If dry-run is active, preview and stop.

### 3.6 Close Retrofit Mode

After append:

```text
Retrofit complete. Run `/architecture-review` in a fresh session to re-validate coverage.
```

Do not continue into new ADR creation.

---

## Phase 4 — Create New ADR

Only run this phase when not in retrofit mode.

### 4.1 Determine Next ADR Number

Scan:

```text
docs/architecture/
```

Find existing files matching:

```text
adr-[NNNN]-*.md
```

Use the next available number.

If directory is missing:

- create it later during write phase if not dry-run,
- do not create during dry-run.

### 4.2 Detect Likely Duplicate ADRs

Search existing ADRs for:

- similar title,
- same domain,
- same system name,
- same state ownership,
- same interface names,
- same GDD systems,
- same registry stances,
- same forbidden patterns,
- same performance budgets.

Use confidence labels:

```text
LOW_OVERLAP
MEDIUM_OVERLAP
HIGH_DUPLICATE_RISK
HARD_CONFLICT_RISK
```

If likely duplicates are found, show:

```md
## Possible Duplicate / Overlap

| Existing ADR | Overlap | Confidence | Risk |
|---|---|---|---|
| ADR-[NNNN] | [description] | [level] | [risk] |
```

Ask only if overlap would create duplicate or contradictory decisions.

### 4.3 Gather Bounded Context

Read relevant sources with this budget:

| Source Type | Maximum |
|---|---:|
| Existing ADRs | 5 most relevant |
| Source files | 5 most relevant |
| GDD files | 5 most relevant |
| Registry entries | all matching entries |
| Engine reference files | all required for domain |

If more candidates exist:

- summarize them,
- use top matches unless user asks to expand scope.

### 4.4 Context Evidence Record

Track:

```md
## ADR Context Evidence

- Existing ADRs read:
- Source files read:
- GDD files read:
- Registry entries read:
- Engine files read:
- Skipped candidates:
- Reason for skipping:
```

---

## Phase 5 — Architecture Registry Check

Read:

```text
docs/registry/architecture.yaml
```

If missing, continue and report:

```text
No architecture registry found. Registry conflict checking is unavailable.
```

### 5.1 Extract Relevant Registry Entries

Extract entries relevant to:

- domain,
- system name,
- state ownership,
- interface contracts,
- API decisions,
- forbidden patterns,
- performance budgets.

Treat only these as binding:

- entries from `Accepted` ADRs,
- entries with `status: active`.

Treat these as relevant but non-binding:

- entries from `Proposed` ADRs,
- entries with `status: proposed`.

### 5.2 Registry Conflict Types

Classify conflicts:

```text
NO_CONFLICT
SOFT_OVERLAP
PROPOSED_OVERLAP
BINDING_CONFLICT
DUPLICATE_DECISION
SUPERSESSION_REQUIRED
SCOPED_EXCEPTION_REQUIRED
REGISTRY_PARSE_RISK
```

### 5.3 Binding Conflict Response

If proposed decision contradicts a binding stance, stop and ask:

```text
⚠️ Architecture conflict detected

This ADR appears to propose:
  [new proposal]

But ADR-[NNNN] established:
  [existing stance]

Choose one:
[A] Align this ADR with the existing stance
[B] Supersede ADR-[NNNN] with an explicit replacement
[C] Treat this as a scoped exception
[D] Stop
```

For a scoped exception, require:

```text
Exception scope:
Exception rationale:
Systems affected:
Systems explicitly not affected:
Expiration or review trigger:
```

Record the exception in:

- `Context`,
- `Alternatives Considered`,
- `Related Decisions`,
- `Registry Impact`,
- `Risks`.

---

## Phase 6 — Collaborative Decision Framing

Before asking questions, derive assumptions from gathered context.

Use `AskUserQuestion` only when materially needed.

Show:

```md
## Drafting Assumptions

### Problem

[one-sentence problem statement]

### Decision Domain

[domain]

### Alternatives to Evaluate

A) [option derived from engine reference]
B) [option derived from GDD requirements]
C) [option derived from project architecture]

### GDD Systems Driving This

- [system]

### Known Constraints

- [constraint]

### Dependencies

- Depends On: [ADR or None]
- Enables: [ADR/Epic/Story or None]
- Blocks: [Epic/Story or None]

### Initial Status

Proposed
```

If material ambiguity exists, ask:

```text
Proceed?

[A] Draft with these assumptions
[B] Change alternatives
[C] Adjust GDD linkage
[D] Add performance budget constraint
[E] Change dependencies
[F] Something else needs changing first
```

If no material ambiguity exists, proceed and record assumptions in ADR.

---

## Phase 7 — Draft ADR

Use this exact structure.

```markdown
# ADR-[NNNN]: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Date

[YYYY-MM-DD]

## Engine Compatibility

| Field | Value |
|-------|-------|
| **Engine** | [engine name + version] |
| **Domain** | [domain] |
| **Knowledge Risk** | [LOW / MEDIUM / HIGH] |
| **Engine Reference Version** | [from VERSION.md, or "Unknown"] |
| **References Consulted** | [engine-reference files read] |
| **Breaking Changes Checked** | [Yes / Partial / No] |
| **Deprecated APIs Checked** | [Yes / Partial / No] |
| **Post-Cutoff APIs Used** | [APIs or "None"] |
| **Deprecated APIs Avoided** | [APIs or "None"] |
| **Verification Required** | [specific behavior to test, or "None"] |
| **Test Harness / Scene Required** | [specific test harness, scene, or "None"] |

## ADR Dependencies

| Field | Value |
|-------|-------|
| **Depends On** | [ADR-NNNN or "None"] |
| **Enables** | [ADR-NNNN, Epic, Story, or "None"] |
| **Blocks** | [Epic, Story, or "None"] |
| **Ordering Note** | [sequencing constraint or "None"] |

## Context

### Problem Statement

[What problem is being solved and why this decision is needed now.]

### Constraints

- [Technical constraint]
- [Engine/version constraint]
- [GDD requirement]
- [Performance constraint]
- [Schedule/resource constraint]

### Architectural Exception

[Only include if this ADR intentionally diverges from an existing stance. Otherwise write "None."]

## Decision

[The specific decision in implementable terms.]

### Architecture Diagram

[ASCII diagram or concise structural description.]

### Key Interfaces

[Signals, methods, data contracts, components, ownership boundaries, or APIs.]

## Alternatives Considered

### Alternative 1: [Name]

- **Description**: [how it works]
- **Pros**: [advantages]
- **Cons**: [costs]
- **Rejection Reason**: [why not chosen]

### Alternative 2: [Name]

- **Description**: [how it works]
- **Pros**: [advantages]
- **Cons**: [costs]
- **Rejection Reason**: [why not chosen]

### Alternative 3: [Name]

- **Description**: [how it works]
- **Pros**: [advantages]
- **Cons**: [costs]
- **Rejection Reason**: [why not chosen]

## Consequences

### Positive

- [benefit]

### Negative

- [trade-off]

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| [risk] | [impact] | [mitigation] |

## GDD Requirements Addressed

| GDD System | Requirement | How This ADR Addresses It |
|------------|-------------|----------------------------|
| [system-name].md | [specific rule, formula, or constraint] | [how the ADR satisfies it] |

## Registry Impact

### State Ownership

- [state] → [owner], or "None"

### Interface Contracts

- [interface/signal/API] → [contract], or "None"

### Performance Budgets

- [system] → [budget], or "None"

### API Decisions

- [API/pattern] → [decision], or "None"

### Forbidden Patterns

- [pattern] → [reason], or "None"

### Supersedes Existing Registry Entries

- [entry] → [reason], or "None"

## Performance Implications

- **CPU**: [expected impact]
- **Memory**: [expected impact]
- **Load Time**: [expected impact]
- **Network**: [expected impact, or "Not applicable"]

## Migration Plan

[How to move from current implementation to this decision. Write "None" if greenfield.]

## Validation Criteria

[Tests, metrics, review checks, runtime behavior, or acceptance criteria.]

## ADR Authoring Evidence

| Check | Status | Evidence / Notes |
|------|--------|------------------|
| Engine reference checked | [Done / Partial / Not Available] | [files] |
| Existing ADR duplicate scan | [Done / Partial / Not Available] | [summary] |
| Registry conflict check | [Done / Partial / Not Available] | [summary] |
| GDD traceability check | [Done / Partial / Not Available] | [summary] |
| Engine specialist review | [Done / Skipped / Failed] | [summary] |
| Technical Director review | [Done / Skipped / Failed] | [summary] |
| GDD sync check | [Done / Partial / Not Available] | [summary] |

## Sources Consulted

| Source | Purpose |
|--------|---------|
| [path] | [why it was read] |

## Related Decisions

- [ADR links]
- [GDD links]
- [Registry links]
```

---

## Phase 8 — Engine Specialist Validation

Skip in `solo`.

Run in `lean` and `full`.

Read:

```text
.claude/docs/technical-preferences.md
```

Use the primary specialist under `Engine Specialists`.

If no specialist is configured, skip and note:

```text
Engine specialist skipped — no primary specialist configured.
```

Spawn `Task` with:

- ADR draft content,
- Engine Compatibility section,
- Decision section,
- Key Interfaces section,
- relevant engine reference paths,
- domain,
- engine version.

Ask specialist to verify:

1. Idiomatic approach for pinned engine version.
2. Deprecated APIs or changed patterns.
3. Post-cutoff engine changes.
4. Implementability of key interfaces.
5. Missing engine-specific risks.

### Specialist Feedback Handling

If specialist feedback requires material changes:

1. Revise once.
2. Rerun specialist once.
3. If unresolved after rerun:
   - keep ADR as `Proposed`,
   - record unresolved concern in `Risks`,
   - record verification needed in `Validation Criteria`,
   - do not claim specialist approval.

---

## Phase 9 — Technical Director Review

Run only in `full`.

Read TD gate config:

```text
.claude/docs/director-gates.md
```

Use gate:

```text
TD-ADR
```

If missing in `full` mode:

- stop,
- report TD gate config unavailable.

Spawn `technical-director` with:

- ADR draft content,
- engine version,
- domain,
- existing ADRs in same domain,
- relevant registry stances,
- known conflicts or scoped exceptions.

### TD Verdict Handling

If TD returns:

```text
APPROVE
```

continue.

If TD returns:

```text
CONCERNS
```

- revise once,
- continue,
- record concerns and mitigation.

If TD returns:

```text
REJECT
```

- stop,
- show blocking issues,
- recommend next action,
- do not save rejected ADRs unless `--dry-run` is active.

If TD output is malformed:

- mark `TD_REVIEW_FAILED`,
- do not claim approval,
- ask user whether to proceed as `Proposed` or stop.

---

## Phase 10 — GDD Sync Check

Before writing, inspect every GDD referenced in:

```text
## GDD Requirements Addressed
```

Check naming inconsistencies with:

- signals,
- methods,
- components,
- data types,
- state names,
- API contracts,
- performance budgets,
- ownership names,
- event names,
- config keys.

If inconsistencies are found, show:

```text
⚠️ GDD SYNC REQUIRED

[gdd-filename].md uses names or contracts that differ from this ADR:

  [old_name] → [new_name_from_adr]

Developers reading the GDD may implement the wrong interface unless the GDD is updated.
```

GDD updates are protected writes. Ask before applying them.

### GDD Sync Record

```md
## GDD Sync Finding

- GDD:
- ADR term:
- Existing GDD term:
- Risk:
- Recommendation:
- Update required:
```

---

## Phase 11 — Write New ADR

Generate target path:

```text
docs/architecture/adr-[NNNN]-[slug].md
```

If `--dry-run` is active:

- show draft,
- show validation state,
- stop without writing.

If not dry-run:

1. Create `docs/architecture/` if needed.
2. Write the ADR file.
3. Do not ask separate confirmation for this new ADR write.
4. If target file already exists:
   - do not overwrite,
   - create next safe filename,
   - or ask user which file should be replaced.

### Write Failure Handling

If write fails:

- report failure,
- do not proceed to registry/story/GDD updates,
- preserve draft in response if useful,
- mark `WRITE_FAILED`.

---

## Phase 12 — Registry Update

Run only after ADR is written.

Skip in `--dry-run`.

Extract candidates from `## Registry Impact`.

Show:

```text
Registry candidates from ADR-[NNNN]:

NEW state ownership:
  [state] → [owner]

NEW interface contract:
  [interface] → [contract]

NEW performance budget:
  [system] → [budget]

NEW API decision:
  [API/pattern] → [decision]

NEW forbidden pattern:
  [pattern] → [reason]

SUPERSEDES:
  [old entry] → [new entry]
```

Ask:

```text
May I update docs/registry/architecture.yaml with these registry entries?

[A] Yes — update registry
[B] Not yet — review candidates
[C] Skip registry update
```

Only proceed on `[A]`.

### Registry Write Rules

1. Read current registry immediately before editing.
2. Append after the last existing entry in the correct section.
3. Do not assume placeholder arrays like `[]` still exist.
4. Do not overwrite unrelated entries.
5. Existing entries may be modified only when supersession was explicitly approved.
6. Validate proposed status:
   - `Accepted` ADR → entries may be `active`.
   - `Proposed` ADR → entries must be `proposed`.

### Registry Failure Handling

If registry is malformed or cannot be safely edited:

- stop registry update,
- report exact risk,
- keep ADR written,
- recommend manual registry repair or review.

---

## Phase 13 — Story Status Updates

Run only after ADR is written.

Skip in `--dry-run`.

Search stories for:

- references to this ADR,
- `Status: Blocked`,
- references to systems enabled by this ADR.

Rules:

- If ADR status is `Proposed`, do not mark stories `Ready`.
- If ADR status is `Accepted`, ask before changing story status.
- Never update stories automatically.

Ask:

```text
How should I handle these story statuses?

[A] Mark listed stories Ready
[B] Leave stories unchanged
[C] Review individually
```

Only update stories if explicitly approved.

---

## Phase 14 — Closing Next Steps

After ADR is written and optional updates are complete, inspect:

```text
docs/registry/architecture.yaml
.claude/docs/technical-preferences.md
systems-index.md
```

If these files exist, identify remaining priority ADRs or prerequisite decisions.

Show:

```text
ADR-[NNNN] written.

Registry update:
[completed | skipped | not applicable]

GDD sync:
[completed | skipped | not applicable]

Story updates:
[completed | skipped | not applicable]

Next best action:
[one recommended action]
```

Always include:

```text
To validate ADR coverage against your GDDs, open a fresh Claude Code session and run:

/architecture-review

Never run /architecture-review in the same session as /architecture-decision.
The reviewing agent must be independent of the authoring context.
```

---

## Self-Learning Protocol

Self-learning means controlled improvement from validated ADR outcomes, review findings, registry conflicts, GDD sync failures, duplicate ADR detections, user corrections, and post-review feedback.

It does not mean hidden memory updates, autonomous architecture policy changes, or treating one ADR exception as project-wide precedent.

### What May Be Learned

The skill may learn:

- approved ADR structure improvements,
- recurring engine compatibility risks,
- recurring registry conflict patterns,
- accepted interface-contract naming patterns,
- common duplicate ADR signals,
- GDD sync failure patterns,
- Technical Director review findings,
- Engine Specialist review findings,
- accepted scoped-exception patterns,
- rejected architectural approaches and reasons.

### What Must Not Be Learned or Stored

Do not store:

- secrets,
- credentials,
- private user data,
- private chain-of-thought,
- sensitive project data outside approved files,
- unapproved architectural assumptions,
- rejected ADRs as accepted decisions,
- proposed registry entries as binding,
- one-off exceptions as project-wide standards,
- unresolved review concerns as resolved rules.

### Lesson Classification

Use:

```text
Confirmed Rule
Approved ADR Standard
Engine Compatibility Finding
Registry Conflict Finding
GDD Sync Finding
Duplicate ADR Finding
Review Mode Finding
Specialist Review Finding
TD Review Finding
Scoped Exception Finding
Supersession Finding
Source-of-Truth Finding
Workflow Failure Finding
Rejected Approach
Working Assumption
Temporary Context
Superseded
```

### Lesson Storage

Durable lessons may be stored only in approved reviewable locations such as:

```text
docs/architecture/adr-authoring-standards.md
docs/architecture/adr-lessons.md
docs/registry/architecture.yaml
tasks/lessons.md
production/session-state/lessons.md
```

### Lesson Format

```md
## Lesson: [Short Name]

- Status:
- Source:
- Applies to:
- Lesson:
- Evidence:
- Date/session:
- Expiry/review trigger:
- Conflicts:
```

### Lesson Validation Rules

A lesson may be stored only if:

- it is specific,
- it is approved or evidence-backed,
- it does not include sensitive data,
- it does not overgeneralize from one ADR,
- it does not conflict with accepted ADRs or active registry entries,
- it has an owner or review trigger where appropriate.

### Lesson Expiry

Review or expire lessons when:

- ADR template changes,
- engine version changes,
- review process changes,
- registry structure changes,
- Technical Director supersedes the rule,
- GDD architecture changes,
- evidence contradicts the lesson,
- the lesson was temporary,
- the lesson is too broad.

---

## Self-Healing Protocol

Self-healing means detecting an ADR workflow failure, containing risk, repairing safely, verifying the repair, and reporting what remains uncertain.

### Failure Types

Monitor for:

- invalid invocation,
- unsafe path,
- missing engine reference,
- incomplete engine reference,
- unknown domain,
- duplicate ADR risk,
- binding registry conflict,
- malformed registry,
- GDD sync mismatch,
- missing required ADR section,
- specialist review failure,
- TD rejection,
- write failure,
- protected write without approval,
- story update attempted while ADR is proposed,
- dry-run write attempt.

### Recovery Loop

When failure occurs:

1. **Stop**
   - Do not proceed as if the workflow is valid.

2. **Identify**
   - State the exact failure.

3. **Classify**
   - Path, engine, registry, GDD, review, write, protected-write, duplicate, or story-status issue.

4. **Contain**
   - Mark status:
     - `BLOCKED`,
     - `UNSAFE_PATH`,
     - `ENGINE_REFERENCE_BLOCKED`,
     - `ARCHITECTURE_CONFLICT`,
     - `GDD_SYNC_RISK`,
     - `TD_REVIEW_REJECTED`,
     - `WRITE_FAILED`.

5. **Recover**
   - reject unsafe path,
   - ask for missing title/path,
   - request engine setup,
   - downgrade knowledge risk,
   - align with existing ADR,
   - create scoped exception,
   - stop after TD rejection,
   - preview protected writes,
   - retry only safe read-only discovery if appropriate.

6. **Verify**
   - Re-check source files or evidence after repair.
   - Do not claim validation if not rerun.

7. **Report**
   - Summarize issue, repair, remaining risk, and next action.

8. **Learn**
   - Propose durable lesson only if validated and approved.

---

## Error Recovery

### Unsafe Path

If path is absolute, contains `..`, or violates required path pattern:

- reject immediately,
- do not read,
- do not write,
- ask for a safe relative path.

### Missing Engine Reference

If `VERSION.md` is missing:

- stop engine compatibility workflow,
- ask user to run `/setup-engine` or provide engine name/version,
- do not draft engine-specific claims.

### Partial Engine Reference

If breaking/deprecated/module docs are missing:

- continue only if `VERSION.md` exists,
- mark knowledge risk `MEDIUM` or `HIGH`,
- record missing docs,
- add verification requirement.

### Duplicate ADR Risk

If likely duplicate exists:

- show overlap,
- ask whether to align, supersede, scope exception, or stop,
- do not create duplicate silently.

### Registry Conflict

If a proposed decision conflicts with accepted ADR or active registry entry:

- stop,
- offer align / supersede / scoped exception / stop,
- require explicit approval for supersession or exception.

### Malformed Registry

If `architecture.yaml` is missing or malformed:

- continue ADR drafting,
- report registry check unavailable or risky,
- do not write registry update.

### GDD Sync Mismatch

If ADR names/contracts differ from GDD:

- show mismatch,
- continue ADR only if mismatch is recorded,
- ask before updating GDD.

### Specialist Review Failure

If specialist task fails:

- do not claim specialist approval,
- record skipped/failed status,
- proceed only if review mode permits and risk is disclosed.

### TD Rejection

If TD rejects in `full` mode:

- stop,
- show blocking issues,
- do not write ADR unless dry-run,
- recommend remediation.

### Write Failure

If ADR write fails:

- report failure,
- do not perform downstream updates,
- provide draft summary or full draft if useful.

### Protected Write Attempt

If registry/GDD/story/retrofit write lacks approval:

- stop,
- preview exact change,
- ask for approval.

### Story Update Risk

If ADR is `Proposed`:

- do not mark stories ready,
- report that acceptance is required first.

---

## Memory Policy

### Short-Term Task Memory

Track during current invocation:

- invocation mode,
- review mode,
- title/path,
- ADR number,
- domain,
- engine context,
- files read,
- registry findings,
- duplicate findings,
- GDD mappings,
- review findings,
- draft status,
- write status,
- protected-update decisions,
- open risks.

Short-term task memory expires after invocation unless explicitly stored.

### Project Memory

Project memory may store:

- approved ADR authoring standards,
- recurring review findings,
- engine compatibility pitfalls,
- registry conflict patterns,
- GDD sync lessons,
- duplicate detection lessons,
- accepted exception patterns,
- rejected approaches.

### Never Store

Never store:

- secrets,
- credentials,
- private user data,
- private chain-of-thought,
- sensitive project data outside approved files,
- unapproved assumptions as accepted rules,
- `Proposed` ADR stances as binding constraints,
- one-off exceptions as broad policy.

---

## Feedback Policy

When the user, Technical Director, Engine Specialist, Lead Programmer, Producer, QA Lead, or domain owner corrects ADR behavior:

1. Accept the correction.
2. Identify whether it affects:
   - ADR template,
   - review mode,
   - engine compatibility,
   - registry impact,
   - GDD traceability,
   - story status,
   - protected-write policy,
   - conflict handling,
   - validation criteria.
3. Revise current output.
4. Ask whether the correction should become durable ADR-authoring guidance if reusable.
5. Store only if approved and evidence-backed.

---

## Tool-Use Policy

Allowed tools:

```text
Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
```

Rules:

- Use `Read`, `Glob`, and `Grep` for discovery.
- Use `Task` only for configured specialist/TD review workflows.
- Use `AskUserQuestion` only for bounded, material decisions.
- Use `Write` for new ADR creation when authorized and not dry-run.
- Use `Edit` only for explicitly approved retrofit append, registry updates, GDD updates, or story updates.
- Do not use unavailable tools.
- Do not run shell commands unless the tool list changes to include shell execution.
- Do not claim tests, builds, or external validation were run unless supported by available tools and evidence.

---

## Safety Guardrails

Never:

- read or write unsafe paths,
- write during dry-run,
- rewrite existing ADR content during retrofit,
- bypass explicit approval for protected writes,
- treat proposed ADRs as binding,
- treat missing registry as registry alignment,
- treat missing engine docs as verified compatibility,
- bypass TD rejection in `full` mode,
- update stories to ready when ADR is proposed,
- overwrite registry entries without supersession approval,
- silently normalize architecture exceptions,
- store persistent lessons without approval.

---

## Output Standards

Responses should be:

- mode-aware,
- path-safe,
- evidence-driven,
- review-mode-aware,
- engine-reference-aware,
- registry-aware,
- GDD-traceable,
- explicit about protected writes,
- clear about what ran, what skipped, and what remains uncertain.

### Standard Status Output

```md
## Architecture Decision Workflow Status

- Mode:
- Review mode:
- Dry-run:
- ADR:
- Engine:
- Domain:
- Registry status:
- GDD sync status:
- Review status:
- Write status:
- Protected updates:
- Blockers:
- Next action:
```

### Finding Format

```md
| Finding | Severity | Evidence | Recommendation |
|---|---|---|---|
```

Severity:

```text
ADR-S1 — Critical
Unsafe path, binding architecture conflict, TD rejection, protected write violation, or engine compatibility blocked.

ADR-S2 — High
Duplicate ADR risk, incomplete engine reference, registry parse risk, missing major ADR section, or GDD sync mismatch.

ADR-S3 — Medium
Partial traceability, uncertain domain, missing validation detail, unclear performance implication.

ADR-S4 — Low
Formatting, naming, source trail, minor documentation improvement.
```

---

## Reflection Checklist

Before final response, privately check:

- Did I parse invocation correctly?
- Did I validate user-supplied paths?
- Did I resolve review mode once?
- Did I discover engine context or stop correctly?
- Did I read required engine docs?
- Did I identify domain?
- Did I scan for duplicates?
- Did I check registry?
- Did I handle conflicts safely?
- Did I trace GDD requirements?
- Did I run required reviews for mode?
- Did I keep proposed vs accepted discipline?
- Did I avoid protected writes without approval?
- Did I avoid writing in dry-run?
- Did I record uncertainty honestly?

Do not expose private chain-of-thought. Report only conclusions, evidence, decisions, and required next actions.

---

## Evaluation Checklist

Before considering the ADR workflow complete:

### Invocation

- [ ] Mode is identified.
- [ ] Review mode is resolved.
- [ ] Dry-run status is clear.
- [ ] Paths are validated.

### Engine Context

- [ ] Engine is identified.
- [ ] VERSION.md was read.
- [ ] Breaking changes were checked or risk marked.
- [ ] Deprecated APIs were checked or risk marked.
- [ ] Domain module was checked or marked unavailable.
- [ ] Knowledge risk is recorded.

### ADR Quality

- [ ] Status exists.
- [ ] Date exists.
- [ ] Engine Compatibility exists.
- [ ] ADR Dependencies exists.
- [ ] Context exists.
- [ ] Decision is implementable.
- [ ] Alternatives are meaningful.
- [ ] Consequences and risks exist.
- [ ] GDD Requirements Addressed exists.
- [ ] Registry Impact exists.
- [ ] Performance Implications exist.
- [ ] Migration Plan exists.
- [ ] Validation Criteria exist.
- [ ] Sources Consulted exists.
- [ ] Related Decisions exist.
- [ ] Authoring Evidence exists.

### Registry and GDD

- [ ] Registry checked or missing status reported.
- [ ] Binding conflicts resolved or workflow stopped.
- [ ] Proposed ADR entries remain proposed.
- [ ] GDD sync checked for referenced GDDs.
- [ ] GDD updates require approval.

### Review

- [ ] Engine Specialist review run or skipped according to mode.
- [ ] TD review run or skipped according to mode.
- [ ] TD rejection stops write in full mode.
- [ ] Review concerns are recorded.

### Writes

- [ ] New ADR written only if not dry-run.
- [ ] Retrofit append only after approval.
- [ ] Registry update only after approval.
- [ ] GDD update only after approval.
- [ ] Story update only after approval.

---

## Example Workflows

### Example 1: New ADR, Lean Mode

Invocation:

```text
/architecture-decision save-data-schema --review lean
```

Expected behavior:

```text
- Resolve review mode as lean.
- Discover engine context.
- Read engine reference files.
- Scan existing ADRs.
- Check registry.
- Draft ADR.
- Run Engine Specialist.
- Skip TD review.
- Check GDD sync.
- Write ADR if not dry-run.
- Ask before registry update.
```

---

### Example 2: Dry Run

Invocation:

```text
/architecture-decision event-system-architecture --dry-run
```

Expected behavior:

```text
- Perform discovery and drafting.
- Run configured reviews if applicable.
- Show draft.
- Do not write ADR.
- Do not update registry.
- Do not update GDDs.
- Do not update stories.
```

---

### Example 3: Retrofit

Invocation:

```text
/architecture-decision retrofit docs/architecture/adr-0001-event-system.md
```

Expected behavior:

```text
- Validate path.
- Read ADR.
- Detect missing sections.
- Preview missing sections.
- Ask before preparing.
- Preview exact append.
- Ask before writing.
- Append only approved missing sections.
- Do not edit existing content.
```

---

### Example 4: Registry Conflict

Conflict:

```text
New ADR proposes UI owns inventory state.
Accepted ADR says inventory state is owned by gameplay inventory service.
```

Response:

```text
⚠️ Architecture conflict detected

Choose:
[A] Align this ADR with existing inventory ownership
[B] Supersede existing ADR
[C] Treat as scoped exception
[D] Stop
```

---

### Example 5: TD Rejection

In `full` mode, TD returns:

```text
TD-ADR: REJECT
```

Expected behavior:

```text
- Stop workflow.
- Show TD blocking issues.
- Do not write ADR.
- Recommend remediation.
```

---

### Example 6: GDD Sync Risk

ADR uses:

```text
InventoryCommand.SubmitTransfer
```

GDD uses:

```text
InventoryTransferEvent
```

Expected behavior:

```text
⚠️ GDD SYNC REQUIRED

Developers reading the GDD may implement the wrong interface unless the GDD is updated.
```

Ask before editing GDD.

---

## Final Behavioral Rule

Architecture decisions created or retrofitted by this skill must be:

- path-safe,
- engine-version-aware,
- duplicate-checked,
- registry-consistent,
- GDD-traceable,
- review-mode compliant,
- protected-write safe,
- evidence-backed,
- explicit about uncertainty,
- and independently reviewable.