---
name: all-aboard
description: >-
  Orchestrates complete project documentation onboarding by ensuring a threat
  model, Architecture Decision Records, and implementation specification exist
  and are current. Reviews existing artifacts, creates missing ones, updates
  stale ones, backfills undocumented decisions, and validates cross-references
  across all three artifact types. Works for both new projects and existing
  codebases. Use when onboarding project documentation, bootstrapping a new
  project, auditing documentation completeness, ensuring spec-ADR-threat model
  alignment, or bringing an undocumented project up to standard. Triggers:
  all aboard, onboard project, bootstrap docs, documentation audit, project
  setup, ensure documentation, doc completeness.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep AskUserQuestion Bash(find *) Bash(ls *) Bash(mkdir *) Bash(git log *) Bash(grep *)
hooks:
  SessionStart:
    - hooks:
        - type: prompt
          prompt: |
            Context was compacted. Re-assess documentation onboarding state per /all-aboard instructions:
            - Check which documentation artifacts exist (spec, ADRs, threat model)
            - Review completeness and currency of existing artifacts
            - Identify missing or stale documentation
            - Continue onboarding from current state
            - Validate cross-references between spec, ADRs, and threat model
  Stop:
    - hooks:
        - type: command
          command: python3 "$HOME/.claude/skills/all-aboard/scripts/check-completion.py"
          timeout: 120
compatibility: >-
  Hook paths assume global install at $HOME/.claude/skills/all-aboard/.
  Adjust the hook command path if you install skills elsewhere.
---

# All Aboard

Get a project's documentation house in order. This skill orchestrates the creation, review, and alignment of three interconnected artifact types: **implementation specifications**, **Architecture Decision Records**, and **threat models**. It works for brand-new projects that need everything from scratch and for existing codebases where documentation has fallen behind (or never existed). You won't need to run each sub-skill individually — All Aboard handles the coordination.

It coordinates between `spec-create`, `spec-review`, `adr-create`, `adr-review`, `threat-model-create`, and `threat-model-review` so you don't have to remember which skill to run when. You won't need to juggle the individual skills yourself — All Aboard handles the sequencing.

## Quick Start

All Aboard runs a five-stage process: **Assess** (what exists?), **Create** (what's missing?), **Review** (what's stale or incomplete?), **Integrate** (do cross-references work?), **Report** (summarize health and next steps). At the end, every spec requirement traces to tests, every architectural decision has an ADR, every security concern has a threat model entry, and all three artifact types link to each other.

The built-in Stop hook keeps the orchestration running until all gates pass — you don't need to re-invoke it manually. See [HOOKS.md](HOOKS.md) for details.

**Running in opencode:** the `hooks:` frontmatter is ignored, so the loop isn't automatic. Either re-run the skill until it reports no gaps, or opt into the `.opencode/plugins/completion-loop.ts` plugin by setting `OPENCODE_REVIEW_LOOP=all-aboard` while it runs. Tool-name mapping is in [docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

## When to Use This Skill

- Starting a new project and want documentation scaffolding from day one
- Onboarding to an existing codebase that lacks documentation
- Periodic audit to catch documentation drift after active development
- Preparing for a team handoff, security audit, or compliance review
- After a major refactoring or architectural change
- When individual review skills keep flagging missing artifacts from other domains

## Workflow

```
All Aboard Progress:
- [ ] Stage 0: Setup — Create directory structure and confirm plan
- [ ] Stage 1: Assessment — Inventory existing artifacts
- [ ] Stage 2: Creation — Build missing artifacts
- [ ] Stage 3: Review — Validate and update existing artifacts
- [ ] Stage 4: Integration — Cross-reference validation
- [ ] Stage 5: Report — Summary and next steps
```

### Stage 1: Assessment

**Scan the project for existing documentation:**

```bash
# Check for documentation directories
ls -la docs/ 2>/dev/null
find docs/ -name "*.md" -type f 2>/dev/null | sort

# Check specific artifact locations
ls docs/specs/*.md 2>/dev/null
ls docs/adr/*.md 2>/dev/null
ls docs/threat-models/*.md 2>/dev/null

# Check for documentation in other common locations
find . -maxdepth 2 -name "*.md" -path "*/arch/*" -o -name "*.md" -path "*/decisions/*" -o -name "*.md" -path "*/security/*" 2>/dev/null
```

**Scan the codebase for context:**

```bash
# Identify project type and tech stack
ls Cargo.toml package.json go.mod Gemfile requirements.txt pyproject.toml flake.nix 2>/dev/null

# Check for infrastructure
ls Dockerfile docker-compose* *.tf *.nix Procfile 2>/dev/null

# Count source files by language
find . -name "*.rs" -o -name "*.py" -o -name "*.go" -o -name "*.js" -o -name "*.ts" -o -name "*.c" -o -name "*.h" | head -50 | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

**Build an assessment matrix:**

```markdown
## Documentation Assessment

| Artifact | Exists? | Count | Last Updated | Quality |
|---|---|---|---|---|
| Specs | Yes/No | [N] | [date] | Unknown |
| ADRs | Yes/No | [N] | [date] | Unknown |
| Threat Model | Yes/No | [N] | [date] | Unknown |
| User Stories | Yes/No | [N] | [date] | Unknown |
| README | Yes/No | — | [date] | — |
| Design docs | Yes/No | [N] | [date] | — |

## Project Context

| Aspect | Details |
|---|---|
| Primary language | [from analysis] |
| Framework | [from dependencies] |
| Database | [from config/deps] |
| External services | [from config/deps] |
| Deployment | [from infrastructure files] |
| Test coverage | [from test files] |
```

**Build a Story Gap Map** from the assessment data:

For each spec functional requirement (`FR-NNN`), check whether a story already exists that covers it:

```bash
# Find existing stories and extract their spec cross-references
find docs/stories -name "*.md" 2>/dev/null | xargs grep -l "FR-" 2>/dev/null
# Find spec requirements with no story link
grep -rh "^## FR-" docs/specs/ 2>/dev/null | sed 's/^## //'
```

For each threat model mitigation, check if a behavioral story covers the security flow:

```bash
grep -rh "^## TM-\|Mitigation\|Acceptance" docs/threat-models/ 2>/dev/null | head -30
```

For each major source module or service (a subdirectory under `src/`, a microservice, an agent), check if there's a story covering its primary behavior end-to-end.

Produce a **Story Gap Map** — the list of candidate stories derived from the above analysis, ranked by coverage risk:

```markdown
## Story Gap Map

| Candidate Story | Source | Priority | Reason |
|---|---|---|---|
| [Actor] [behavior] | FR-001, FR-002 | High | Core user flow, no story exists |
| [Service] receives [message] | TM-API-003 mitigation | High | Security flow, no behavioral story |
| [Agent] orchestration cycle | src/agent/ directory | Medium | Undocumented subsystem |
| [User] onboarding journey | inferred from ADR-0005 | Low | Nice to have |
```

**Present the assessment and Story Gap Map, then confirm the plan.**

Use `AskUserQuestion` to ask:
- Which artifacts should we prioritize?
- Any specific concerns driving this documentation effort?
- Should we focus on breadth (all artifacts at basic level) or depth (one artifact done thoroughly)?
- Are there areas of the codebase that are off-limits or shouldn't be documented yet?

### Stage 2: Creation

Create missing artifacts in dependency order. The threat model informs security requirements in the spec, and both the spec and threat model reveal decisions that need ADRs.

**Recommended creation order:**

**Step 2.1: Set up directory structure**

```bash
mkdir -p docs/specs docs/adr docs/threat-models
```

**Step 2.2: Threat model first** (if missing)

The threat model identifies security constraints that feed into the spec and decisions that need ADRs.

Use `threat-model-create` workflow:
- Decompose the system into DFD elements
- Identify trust boundaries between components
- Apply STRIDE to each element
- Score threats with DREAD
- Plan mitigations
- Note decisions that need ADRs and requirements that need spec entries

**Step 2.3: ADRs second** (if missing)

Decisions are already being made — they just aren't documented. Start with the bootstrap ADR, then backfill from the codebase.

Use `adr-create` workflow:
- Create ADR-0001: Record Architecture Decisions
- Mine the codebase for technology and architecture decisions
- Prioritize: security decisions first, then technology choices, then patterns
- Cross-reference to threat model entries where applicable

**Step 2.4: Spec last** (if missing)

The spec can now reference both the threat model and ADRs.

Use `spec-create` workflow:
- Analyze codebase for functional requirements
- Write requirements using EARS syntax with RFC 2119 keywords
- Add Gherkin acceptance criteria
- Map each requirement to existing test coverage
- Cross-reference ADRs and threat model entries
- Build the traceability matrix

**Step 2.5: User stories** (if missing or incomplete)

The Story Gap Map from Stage 1 is your input here. Don't start from scratch — work through the candidate list in priority order.

For each High-priority candidate story, invoke `story-creator`:
- Pass the story candidate title and source (FR-NNN, TM-XXX, or component name) as context
- `story-creator` will run its own gap analysis, which will confirm or refine the candidate
- After creating each story, run `story-reviewer` to validate quality before saving
- Save to `docs/stories/STORY-NNN-[kebab-title].md`
- Cross-reference to spec requirements (FR-NNN) and threat model entries (TM-COMPONENT-NNN)

After completing High-priority stories, use `AskUserQuestion` to confirm whether to continue with Medium-priority candidates or move on.

A project that has a spec and ADRs but no stories lacks behavioral verification — there's nothing that says "this is what correct end-to-end behavior looks like" in terms a test can check. The Story Gap Map makes that gap visible and gives you a concrete backlog to work from.

**If ALL artifacts already exist:** Skip to Stage 3.

**If SOME artifacts exist:** Create only the missing ones, referencing existing artifacts for context and cross-linking.

### Stage 3: Review

Review all artifacts — both pre-existing and newly created. The creation process may have been incomplete or the existing artifacts may be stale.

**Step 3.1: Review the threat model**

Use `threat-model-review` workflow:
- Validate DFD matches current implementation
- Check STRIDE coverage
- Verify risk scores
- Audit mitigation statuses

**Step 3.2: Review ADRs**

Use `adr-review` workflow:
- Check quality of existing ADRs
- Identify undocumented decisions
- Validate staleness (do accepted ADRs still apply?)
- Recommend backfills

**Step 3.3: Review the spec**

Use `spec-review` workflow:
- Gap analysis between spec and implementation
- Quality assessment (testability, ambiguity)
- Traceability matrix completeness
- Cross-reference integrity with ADRs and threat model

**Step 3.4: Review user stories** (if present)

Use `story-reviewer` workflow on each story in `docs/stories/`:
- Check INVEST compliance, Gherkin correctness, EARS constraints
- Validate security coverage for stories that cross trust boundaries
- Verify traceability links to spec requirements and threat model entries
- Any story scoring below 3 on any dimension is a documentation gap — add to the report

### Stage 4: Integration

This is the unique value of All Aboard — ensuring the three artifact types work together as a coherent whole.

**Cross-reference validation matrix:**

| Check | Artifact A | Artifact B | Status |
|---|---|---|---|
| Security requirements → Threat entries | Spec | Threat Model | [Pass/Gap] |
| Tech choices → ADRs | Spec | ADRs | [Pass/Gap] |
| Security decisions → Threat entries | ADRs | Threat Model | [Pass/Gap] |
| Mitigations → Spec requirements | Threat Model | Spec | [Pass/Gap] |
| Mitigations → ADRs | Threat Model | ADRs | [Pass/Gap] |
| ADR implications → Spec updates | ADRs | Spec | [Pass/Gap] |

**For each gap, determine the fix:**

- Missing spec requirement for a threat mitigation → Add requirement via `spec-create`
- Missing ADR for a technology choice in the spec → Create via `adr-create`
- Missing threat entry for a security requirement → Analyze via `threat-model-create`
- Broken cross-reference link → Fix the link in the artifact that references it
- Stale cross-reference (links to superseded ADR) → Update to current ADR
- Orphaned artifact (referenced by nothing) → Either link it or mark it for deprecation

**ID consistency check:**
- Spec uses `SPEC-XXX`, `FR-XXX`, `NFR-XXX` pattern
- ADRs use `ADR-NNNN` pattern with sequential numbering
- Threat model uses `TM-[COMPONENT]-NNN` pattern
- All cross-references use the correct ID format

### Stage 5: Report

Write the report to `docs/all-aboard-report.md` (the Stop hook checks this location).

```markdown
## All Aboard Report: [Project Name]

### Executive Summary
[2-4 sentences: what was the starting state, what was done, what's the current state]

### Assessment Results

| Artifact | Before | After | Status |
|---|---|---|---|
| Specs | [none/stale/partial] | [count] requirements documented | [Done/Needs work] |
| ADRs | [none/stale/partial] | [count] decisions documented | [Done/Needs work] |
| Threat Model | [none/stale/partial] | [count] threats identified | [Done/Needs work] |

### Work Performed

#### Created
- [List of new artifacts created]

#### Updated
- [List of existing artifacts that were updated]

#### Cross-References Added
- [List of new cross-reference links between artifacts]

### Remaining Gaps

| Gap | Artifact | Priority | Recommended Action |
|---|---|---|---|
| [description] | [which] | [High/Medium/Low] | [what to do] |

### Cross-Reference Health

| Link Type | Total | Valid | Broken | Missing |
|---|---|---|---|---|
| Spec → ADR | [N] | [N] | [N] | [N] |
| Spec → Threat Model | [N] | [N] | [N] | [N] |
| ADR → Spec | [N] | [N] | [N] | [N] |
| ADR → Threat Model | [N] | [N] | [N] | [N] |
| Threat Model → Spec | [N] | [N] | [N] | [N] |
| Threat Model → ADR | [N] | [N] | [N] | [N] |

### Artifact Status Summary

Report the implementation status of all artifacts using the standard status values (see `artifact-status-tracking` rule). The iterate skill's completion check script validates these — inconsistent statuses will cause false positives or missed gaps.

| Artifact Type | Total | Implemented | Partial | Not Started | Blocked by |
|---|---|---|---|---|---|
| Threat model entries (TM-*) | [N] | [N] ✅ IMPLEMENTED | [N] ⚠️ PARTIAL | [N] Not Started | Iterate P0/P1 |
| Stories (STORY-*) | [N] | [N] Implemented | — | [N] Draft/Revision | Iterate P1 |
| Security requirements (SR-*) | [N] | [N] | [N] Partial | [N] Not Started | Iterate P0 |
| ADRs (accepted) | [N] | [N] with code | — | [N] missing impl files | Iterate P1 |
| Spec tasks (File refs) | [N] | [N] files exist | — | [N] missing files | Iterate P1 |

**Valid status values (MUST use these — the iterate completion script parses them):**

- **Threat model:** `Not Started` → `⚠️ **PARTIAL**` → `✅ **DESIGNED**` → `✅ **IMPLEMENTED**`
- **Stories:** `Draft` → `Revision N` → `Implemented` → `Complete`
- **ADRs:** `proposed` → `accepted` → `deprecated` / `superseded`
- **Security requirements:** `Not Started` → `Partial` → `Implemented`
- **Specs:** No status field — tracked by file existence of `**File:**` references

### Story Gap Map

| Candidate Story | Source | Priority | Status |
|---|---|---|---|
| [story candidate] | [FR-NNN / TM-XXX / component] | [High/Medium/Low] | [Created / Backlog / Deferred] |

Stories created this session:
- [STORY-NNN: title] — covers [FR-NNN], [TM-XXX]

Stories remaining in backlog:
- [brief description] — suggest running `/story-creator` with context: "[candidate title from source FR-NNN]"

### Maintenance Recommendations
[How to keep artifacts current going forward — suggest triggers for updates.
Include: "Run `/iterate` to validate all artifact statuses against the implementation.
The completion script cross-references every TM entry, story, SR, ADR, and spec task
against the codebase and blocks until all gaps are closed."]
```

## For New Projects (No Code Yet)

When there's no code to analyze:

1. **Start with requirements** — Use `spec-create` to capture what will be built
2. **Threat model the design** — Use `threat-model-create` on the planned architecture
3. **Document initial decisions** — Use `adr-create` for technology and architecture choices
4. **Cross-reference everything** — Link specs to threat entries and ADRs from the start

This front-loads the documentation effort but it's worth it — security issues are caught in design, decisions are recorded while context is fresh, and requirements are clear before coding starts.

## For Large Existing Projects

When the codebase is substantial and undocumented:

1. **Don't try to document everything at once.** You'll burn out. Focus on one subsystem or feature area.
2. **Start with the riskiest area** — the part with the most security implications, the most complexity, or the most recent changes.
3. **Create the threat model first** — it reveals what's important to document.
4. **Timebox ADR backfilling** — aim for 4-6 ADRs per session, covering the biggest decisions.
5. **Spec the current state** honestly — note gaps and areas where code behavior is unclear.
6. **Iterate** — run All Aboard again on the next area once the first is complete.

## Writing Style

Apply the `natural-writing-style` skill to all reports and documentation. The All Aboard report should give a clear, honest picture of documentation health — not "everything looks great!" but "here's where we stand, here's what was done, and here's what still needs attention."

## Resources

- [Cross-Reference Guide](references/cross-reference-guide.md) — How the three artifact types connect
- [Stop Hook](HOOKS.md) — Auto-continuation hook that keeps the orchestration going until all gates pass
