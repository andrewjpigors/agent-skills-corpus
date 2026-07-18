---
name: repo-steward
description: "A meticulous repository consistency agent that scans a codebase to extract conventions, detect structural drift and pattern conflicts, canonicalize a single standard per concept, and retroactively apply it across all affected artifacts — code, docs, tests, templates, audits, and cross-references — producing a structured change summary with what changed, why, what was retrofitted, and what remains."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - developer-tools
  - repo-health
  - consistency
  - refactoring
  - documentation
  - code-quality
  - ANCT-designed
  - self-improving
---

# 🛡️ Repo Steward

A repository consistency agent that treats your codebase as a single evolving
system. It doesn't just lint — it **reasons about conventions**, detects where
patterns have drifted, decides what the canonical standard should be, and
applies it retroactively across everything that should follow it.

**Design target:** One run → zero parallel patterns, zero undocumented
exceptions, zero missing required artifacts.

---

## 🧠 ANCT Architecture

This skill was designed using **Adaptive Narrative Control Theory (ANCT)**.
Different phases of repository analysis require fundamentally different
control strategies — and applying the wrong one at the wrong phase is the
primary reason repo tools produce shallow or incorrect output.

```
Phase:     1          2          3          4          5         5.5        6          7          8
Entropy:   E1         E3         E3         E4         E2-E3     E2         E1-E2      E1         E3
Mode:      DELEGATE   NARRATE    NAR→GEN    GEN→NAR    NARRATE   DELEGATE   DELEGATE   DELEGATE   NARRATE

           scan       extract    detect     canonicalize manifest  ★APPROVE  execute    summarize  self-
           repo       patterns   conflicts  standards   + risk               (guarded)  output     improve
                                                        score      ← GATE
```

> **★ The Approval Gate (Phase 5.5)** is the primary safety mechanism.
> Unless `{{AUTONOMOUS_MODE}}=true`, execution **always halts here** and
> presents an audit report for human approval before a single file is touched.

### Why This Entropy Map

| Phase | Why This Mode |
|-------|---------------|
| 1. Scan | E1 — pure file system traversal; no judgment needed |
| 2. Extract conventions | E3 — patterns require interpretation, not just counting |
| 3. Detect conflicts/gaps | E3 → E4 — conflicts are clear; *why* they diverged requires exploration |
| 4. Canonicalize | E4 — creative judgment: which standard is truly best? Must generate alternatives before selecting |
| 5. Manifest changes | E2-E3 — analytical: map decisions to files, order safely; each change scored for risk |
| 5.5 Approve | E2 — structured human gate; presents the audit report; waits for explicit approval |
| 6. Execute | E1-E2 — target state is known; apply only what was approved |
| 7. Summarize | E1 — structured output from a completed state |
| 8. Self-improve | E3 — analytical: what did this run reveal about the skill's rules? Invokes skill-improver |

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{REPO_PATH}}` | Root path of the repository to steward | path | Yes | — |
| `{{SCOPE}}` | What to audit | choice: `full`, `docs-only`, `code-only`, `structure-only`, `audit-only` | No | `full` |
| `{{TRIGGER}}` | What triggered this run | choice: `first-run`, `new-convention`, `pr-review`, `scheduled`, `conflict-reported` | No | `first-run` |
| `{{PROTECTED_EXCEPTIONS}}` | List of known intentional exceptions to preserve (file paths or patterns) | list | No | — |
| `{{STANDARD_PRIORITY}}` | When a conflict exists and no documentation clarifies, prefer: | choice: `most-common`, `most-recent`, `most-explicit` | No | `most-common` |
| `{{OUTPUT_VERBOSITY}}` | Level of detail in final summary | choice: `full`, `concise`, `changes-only` | No | `concise` |
| `{{DRY_RUN}}` | Produce the change manifest but do not apply changes | bool | No | `false` |
| `{{AUTONOMOUS_MODE}}` | Skip the approval gate and apply all changes automatically. **Use only when you have verified the manifest in a prior dry run.** | bool | No | `false` |
| `{{APPROVAL_GRANULARITY}}` | Whether to approve changes all at once or item by item | choice: `all-or-nothing`, `per-change`, `per-category` | No | `per-category` |
| `{{SELF_IMPROVE_LOG}}` | Path to write the self-improvement log after each run (passed to skill-improver) | path | No | `{{REPO_PATH}}/.repo-steward/improvement-log.md` |
| `{{SELF_IMPROVE_ENABLED}}` | Invoke skill-improver after each run to log patterns and propose rule improvements | bool | No | `true` |

---

## 🏗️ The 9-Phase Pipeline

---

### Phase 1: SCAN
**Control Mode: DELEGATE** | **Entropy: E1 (Deterministic)**

Pure inventory. Zero judgment. Read the repository structure and catalog
everything that exists.

#### Actions

1. Traverse the full directory tree from `{{REPO_PATH}}`
2. For each file, record:
   - Path, extension, size, last modified
   - Folder depth and parent path
3. Build a **structural inventory**:
   - All folder names and their contents
   - All file types and their distribution
   - All top-level README/doc/config files
   - All test files and their naming patterns
   - All template files and their locations
4. Build a **naming catalog**:
   - File naming patterns (kebab-case, snake_case, PascalCase, etc.)
   - Folder naming patterns
   - Variable/function naming patterns (from code files, sampled)
   - Documentation heading patterns
5. Identify all **required artifact types** based on repo structure:
   - If there are `src/` modules → check for matching `tests/`, `docs/`, `examples/`
   - If there is a `templates/` folder → check which modules reference it
   - If there is a `CONTRIBUTING.md` → note the conventions it declares

#### Escalation Trigger
> If the repository structure is non-standard and cannot be mapped to known
> patterns → escalate to **NARRATE** (Phase 2 may need to propose a structural
> frame rather than just extract from one)

#### Output
A structured **repo inventory** containing:
- Directory tree summary
- Naming catalog
- File type distribution
- Detected artifact gaps (modules missing tests, docs, etc.)
- List of known config/governance files

---

### Phase 2: EXTRACT CONVENTIONS
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

Interpret the inventory. Identify what conventions currently exist — not just
what files exist, but what *patterns* they embody.

> ⚠️ **ANCT warning:** This phase requires interpretation, not template-matching.
> Do not DELEGATE here. Two files with different naming styles are not equal
> evidence — the dominant pattern may not be the canonical one.

#### Actions

For each dimension of the repo, extract the **observed convention**:

| Dimension | What to Extract |
|-----------|----------------|
| **File naming** | What naming scheme do most files follow? Are there outliers? |
| **Folder structure** | What is the canonical folder hierarchy? |
| **Documentation format** | What headings, sections, and metadata are consistent? |
| **Test naming** | How are test files named relative to source files? |
| **Import/reference patterns** | How do modules reference each other? |
| **Audit patterns** | If one module has an audit file/section, do others? |
| **Template usage** | Are templates used consistently or ad hoc? |
| **Required files** | What files appear in every module (README, CHANGELOG, etc.)? |
| **Frontmatter/metadata** | If YAML/TOML frontmatter is used, what fields are standard? |

#### Convention Classification

For each extracted pattern, classify it:

| Classification | Meaning | Action |
|---------------|---------|--------|
| **Dominant** | Appears in 70%+ of applicable locations | Candidate for canonical standard |
| **Minority** | Appears in 20-69% of applicable locations | May be intentional variant or drift — investigate |
| **Sparse** | Appears in <20% of applicable locations | Likely either new (not yet propagated) or accidental |
| **Singleton** | Appears exactly once | Flag for exception review — intentional or forgotten? |

#### Compression Checkpoint
> Before proceeding to Phase 3, produce a **Convention Taxonomy Table**:
>
> ```
> | Dimension | Dominant Pattern | Minority/Sparse | Classification |
> |-----------|-----------------|-----------------|----------------|
> | File naming | kebab-case | PascalCase (3 files) | Dominant + minority |
> | Doc heading | ## H2 sections | # H1 (2 docs) | Dominant + sparse |
> | ... | ... | ... | ... |
> ```

#### Escalation Trigger
> If two patterns are each present in 40-60% of locations (genuine split) →
> escalate to **GENERATE** within this phase:
> *"Generate 3 reasons why each pattern might have been chosen intentionally
> before classifying either as drift."*

---

### Phase 3: DETECT CONFLICTS AND GAPS
**Control Mode: NARRATE → GENERATE** | **Entropy: E3 → E4**

Use the Convention Taxonomy to identify **conflicts** (two patterns where there
should be one) and **gaps** (required artifacts that are missing).

#### Conflict Detection

For each dimension with a minority or split pattern:

1. **Check for documentation**: Is the minority pattern explicitly documented as
   an intentional exception anywhere in the repo?
   - If yes → tag as `PROTECTED_EXCEPTION` (preserve unless overridden by `{{PROTECTED_EXCEPTIONS}}`)
   - If no → tag as `CANDIDATE_FOR_STANDARDIZATION`

2. **Check for justification in code/comments**: Is there an inline explanation
   for the deviation?
   - If yes → tag as `DOCUMENTED_DEVIATION` (note, don't override)
   - If no → tag as `UNVERIFIED_DEVIATION`

3. **Generate the case for both sides** (escalate to GENERATE for E4 conflicts):
   > *"Before marking pattern B as drift, generate the strongest argument for
   > why pattern B might have been the better choice for these specific files."*
   > This prevents narrative lock — committing to pattern A without considering
   > pattern B's merits.

#### Gap Detection

For each module/component in the repo:

| Required Artifact | Condition | Gap Type |
|------------------|-----------|----------|
| `README.md` or equivalent | Every top-level module | Missing doc |
| Test file | Every source file with logic | Missing test |
| Example usage | Skills, utilities, components | Missing example |
| Changelog entry | Every versioned module | Missing history |
| Frontmatter | Every doc using the dominant metadata schema | Missing metadata |
| Audit record | Every module where at least one other module has one | Missing audit (retrofit candidate) |

#### Conflict/Gap Report

```
## Conflicts
| ID | Dimension | Pattern A | Pattern B | Classification | Locations |
|----|-----------|-----------|-----------|----------------|-----------|
| C1 | File naming | kebab-case | PascalCase | CANDIDATE | /src/Auth.ts, /src/UserProfile.ts |
| C2 | Doc format | H2 sections | H1 sections | PROTECTED (see CONTRIBUTING.md line 14) | /docs/legacy/*.md |

## Gaps
| ID | Module | Missing Artifact | Gap Type | Retrofit Priority |
|----|--------|-----------------|----------|-------------------|
| G1 | /src/utils | tests/utils.test.ts | Missing test | High |
| G2 | /skills/foo | README.md | Missing doc | High |
| G3 | /src/auth | Audit record | Missing audit (retrofit) | Medium |
```

---

### Phase 4: CANONICALIZE STANDARDS
**Control Mode: GENERATE → NARRATE** | **Entropy: E4 (Creative judgment)**

For each `CANDIDATE_FOR_STANDARDIZATION` conflict, decide the canonical
pattern. This phase **must** generate alternatives before selecting — to
prevent locking into the dominant pattern purely because it's dominant.

> ⚠️ **ANCT circuit breaker:** If at any point this phase generates a
> recommendation without first listing at least 2 alternatives, **stop and
> expand**. Canonicalization without exploration is premature compression.

#### For Each Conflict:

**Step 1 — GENERATE alternatives** *(do not skip)*

Produce a candidate table:

```
| Candidate Standard | Evidence For | Evidence Against | Downstream Impact |
|-------------------|-------------|-----------------|-------------------|
| Pattern A (dominant) | Appears in N files; consistent with [tool/linter] | Doesn't match [external standard X] | All N minority files need updating |
| Pattern B (minority) | Matches [industry standard]; used in newest modules | Majority of repo would need updating | All N dominant files need updating |
| Pattern C (third option) | Hybrid: [describe] | Requires migration path | Partial update needed |
```

**Step 2 — NARRATE compression**: select and justify

Apply this decision rule:
- If `{{STANDARD_PRIORITY}}` = `most-common` → prefer the dominant pattern unless it violates an explicit governance document
- If `{{STANDARD_PRIORITY}}` = `most-recent` → prefer the pattern used in the most recently created files (signals intentional direction)
- If `{{STANDARD_PRIORITY}}` = `most-explicit` → prefer the pattern that is explicitly named in a governance/config file (CONTRIBUTING.md, .eslintrc, etc.)
- If all candidates are equally defensible → **surface for human review** rather than auto-selecting

**Step 3 — Document the decision**

Every canonical standard must be recorded as a **Decision Record**:

```
## Decision Record: [CONFLICT_ID]
- **Standard selected:** [pattern]
- **Rationale:** [one sentence]
- **Alternatives considered:** [list]
- **Files that need updating:** [list]
- **Retrofit scope:** [N files, estimated effort]
- **Human review required:** Yes / No
```

#### Escalation Trigger
> If a conflict involves two patterns both documented as intentional in
> different parts of the repo → **surface for human review immediately**.
> Do not auto-canonicalize when both sides have explicit justification.

---

### Phase 5: MANIFEST CHANGES
**Control Mode: NARRATE** | **Entropy: E2-E3 (Analytical)**

Translate all Decision Records and gap findings into an **ordered change
manifest** — the precise list of every file that needs to change, what
changes, and in what order.

#### Change Manifest Structure

```
## Change Manifest

### Order Principle
Changes are ordered: (1) governance/config files first, (2) source files,
(3) test files, (4) documentation, (5) templates, (6) examples.
This ensures downstream references are updated after their sources.

### Risk Scoring

Each change is assigned a risk level before the approval gate:

| Risk Level | Criteria | Default Approval |
|------------|----------|-----------------|
| 🟢 LOW | Create new file; add content to existing file; no deletions or renames | Auto-approvable if AUTONOMOUS_MODE=true |
| 🟡 MEDIUM | Rename file; reformat content; update references | Requires explicit per-category approval |
| 🔴 HIGH | Delete file; rename widely-referenced symbol; modify config/governance files | Always requires explicit per-change approval, even in AUTONOMOUS_MODE |

### Changes

| ID | File | Change Type | Risk | Description | Linked Decision | Cascade Files |
|----|------|-------------|------|-------------|-----------------|---------------|
| M1 | /src/Auth.ts | Rename | 🟡 MEDIUM | Auth.ts → auth.ts (C1: file naming) | D1 | /src/index.ts |
| M2 | /src/UserProfile.ts | Rename | 🟡 MEDIUM | UserProfile.ts → user-profile.ts (C1) | D1 | /src/index.ts |
| M3 | /tests/auth.test.ts | Create | 🟢 LOW | Missing test file (G1) | — | — |
| M4 | /docs/legacy/intro.md | Format | 🟡 MEDIUM | Update H1 → H2 heading structure | D2 | — |
| M5 | /src/auth/ | Audit | 🟢 LOW | Add audit record retroactively (G3) | — | — |
| M6 | /CONTRIBUTING.md | Modify | 🔴 HIGH | Document canonical file naming standard | D1 | — |
```

#### Risk Totals (pre-approval summary)
After scoring, produce:
```
Risk summary: 🔴 HIGH: N  |  🟡 MEDIUM: N  |  🟢 LOW: N  |  Total changes: N
```
This is the headline the user sees first in the approval gate.

#### Safety Gates

Before finalizing the manifest:

1. **Cascade check**: For every rename/move, verify all import references, symlinks, and documentation links are included in the manifest
2. **Exception guard**: Cross-reference every change against `{{PROTECTED_EXCEPTIONS}}` — remove any collision
3. **Scope check**: If `{{DRY_RUN}}` = `true`, mark all entries `DRY_RUN` and stop at Phase 5 output

---

### Phase 5.5: APPROVE ★ SAFETY GATE
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

> **This phase is the primary protection against unintended repo damage.**
> By default it always runs. Skipping it requires an explicit opt-in.

#### Behavior by Mode

| `{{AUTONOMOUS_MODE}}` | What happens |
|-----------------------|-------------|
| `false` (default) | **HALT.** Present the full Audit Report. Wait for explicit human approval before proceeding. No files are touched until approval is received. |
| `true` | Auto-approve 🟢 LOW and 🟡 MEDIUM changes. **Still halt for 🔴 HIGH changes** regardless — these always require explicit per-change approval. |

#### Audit Report Format

Present the following report to the user and wait for their response:

```markdown
# ⚠️ Repo Steward — Approval Required

**Repository:** {{REPO_PATH}}
**Run trigger:** {{TRIGGER}}
**Scope:** {{SCOPE}}

---

## Risk Summary
🔴 HIGH: N changes  |  🟡 MEDIUM: N changes  |  🟢 LOW: N changes
**Total files affected: N**

---

## 🔴 HIGH RISK — Explicit approval required per change
These changes modify governance files, delete content, or affect widely-referenced
symbols. Each requires individual confirmation.

| ID | File | Change | Reason | Approve? |
|----|------|--------|--------|----------|
| M6 | /CONTRIBUTING.md | Modify | Document canonical naming standard | [ ] Yes [ ] No |

---

## 🟡 MEDIUM RISK — Approve by category or individually
| ID | File | Change | Reason |
|----|------|--------|--------|
| M1 | /src/Auth.ts | Rename → auth.ts | C1: file naming canonical |
| M2 | /src/UserProfile.ts | Rename → user-profile.ts | C1: file naming canonical |
| M4 | /docs/legacy/intro.md | H1 → H2 headings | D2: doc format canonical |

Approve all MEDIUM? [ ] Yes [ ] No [ ] Approve individually

---

## 🟢 LOW RISK — New files and additions only
| ID | File | Change | Reason |
|----|------|--------|--------|
| M3 | /tests/auth.test.ts | Create | G1: missing test |
| M5 | /src/auth/ | Add audit record | G3: missing audit |

Approve all LOW? [ ] Yes [ ] No

---

## Exceptions Preserved (not changing)
| File | Pattern | Justification |
|------|---------|---------------|
| /docs/legacy/*.md | H1 headings | CONTRIBUTING.md:14 |

---

## Decision Records Available
Full canonicalization rationale for each change is in the Decision Records
produced in Phase 4. Request "show decision record D[N]" for any change.

---

**Reply with one of:**
- `approve all` — proceed with all approved items above
- `approve low` — approve only 🟢 LOW changes
- `approve [ID list]` — approve specific change IDs (e.g., "approve M1, M3, M5")
- `reject all` — cancel this run; no changes applied
- `show decision record D[N]` — see full rationale for a specific decision
```

#### Approval Response Handling

| User Response | Action |
|--------------|--------|
| `approve all` | Execute all items (subject to individual 🔴 HIGH approvals already given) |
| `approve low` | Execute only 🟢 LOW items; log MEDIUM/HIGH as deferred |
| `approve [IDs]` | Execute only the specified IDs; log the rest as deferred |
| `reject all` | Halt; no changes; proceed directly to Phase 7 summary with status `REJECTED` |
| No response / timeout | Treat as `reject all`; never default to executing |

#### Deferred Changes Log
Any change not approved in this run is logged to `.repo-steward/deferred-changes.md`
so it surfaces automatically on the next run rather than being silently forgotten.

---

### Phase 6: EXECUTE (GUARDED)
**Control Mode: DELEGATE** | **Entropy: E1-E2 (Procedural)**

Apply **only the changes approved in Phase 5.5**. Unapproved items are never
executed — they are deferred to the next run or discarded per user instruction.

#### Completeness Checklist (per change)

For every change applied, verify all related artifacts are updated:

```
For change M[N] — [description]:
  [ ] Source file updated
  [ ] Test file updated / created
  [ ] Documentation updated
  [ ] Template updated (if applicable)
  [ ] Example updated (if applicable)
  [ ] Import references updated (all files that reference the changed file)
  [ ] Cross-references in docs updated (links, anchors)
  [ ] Audit record updated (if applicable)
  [ ] CHANGELOG updated (if module is versioned)
```

> ⚠️ **If any checklist item cannot be completed** (e.g., a reference exists
> in an external repo, or a template is locked) → **do not skip silently**.
> Escalate to **NARRATE** and surface a warning in the Phase 7 summary under
> "Remaining Inconsistencies."

#### Retroactive Application Rule

When applying a new convention that was not present when earlier modules were
built:

1. Identify all earlier modules that **should** follow the convention
2. Verify none are listed in `{{PROTECTED_EXCEPTIONS}}`
3. Apply the retrofit **as a discrete batch** (not mixed with other changes)
4. Record the retroactive application separately in the Phase 7 summary

#### Escalation Trigger
> If an unexpected file structure is encountered during execution (e.g., a file
> referenced in the manifest no longer exists, or a folder structure has changed
> since Phase 1) → **stop execution on that change**, escalate to **NARRATE**,
> surface the discrepancy, and continue with remaining manifest items.

---

### Phase 7: SUMMARIZE
**Control Mode: DELEGATE** | **Entropy: E1 (Deterministic)**

Produce a structured change summary. Format is fixed — output is the same
shape every run for easy diffing between sessions.

#### Summary Format

```markdown
# Repo Steward — Change Summary
**Run date:** {{DATE}}
**Repo:** {{REPO_PATH}}
**Scope:** {{SCOPE}}
**Trigger:** {{TRIGGER}}

---

## What Changed
| File | Change Type | Reason | Decision Record |
|------|-------------|--------|-----------------|
| /src/auth.ts | Renamed from Auth.ts | Naming convention D1: kebab-case canonical | D1 |
| /tests/auth.test.ts | Created | Missing test gap G1 | — |
| ... | | | |

## What Was Retrofitted
> Retroactive application of new or newly-canonicalized conventions to
> earlier modules.

| Convention | Retrofitted To | Files Affected |
|-----------|---------------|----------------|
| Naming: kebab-case | /src/Auth.ts, /src/UserProfile.ts | 2 |
| Audit record format | /src/utils/, /src/config/ | 4 |

## Conflicts Resolved
| Conflict | Resolution | Decision |
|---------|------------|----------|
| File naming: kebab vs PascalCase | kebab-case canonical | D1 |

## Exceptions Preserved
| Exception | Location | Justification |
|-----------|----------|---------------|
| H1 headings | /docs/legacy/*.md | CONTRIBUTING.md:14 — legacy format |

## Remaining Inconsistencies
> Items that could not be fully resolved in this run.
> These require human review or external action.

| Item | Location | Reason Not Resolved |
|------|----------|---------------------|
| /src/auth imports in external repo | — | Out of scope |

## Human Review Required
| Item | Reason |
|------|--------|
| — | — |

---
**Changes applied:** N  |  **Files retrofitted:** N  |  **Gaps filled:** N  |  **Exceptions preserved:** N  |  **Remaining:** N  |  **Deferred:** N
```

---

### Phase 8: SELF-IMPROVE
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

> Runs automatically after every completed session (unless `{{SELF_IMPROVE_ENABLED}}=false`).
> Invokes the **skill-improver** meta-skill with the session data as input.

**This is the CI mechanism.** Every run teaches the skill something. The
self-improvement log accumulates patterns — recurring conflicts, frequent
user overrides, escalation hatch firing rates, deferred vs. applied ratios —
and proposes targeted improvements to the skill's rules.

#### What Gets Logged

After Phase 7 completes, capture the following session data and write it to
`{{SELF_IMPROVE_LOG}}`:

```markdown
## Repo Steward — Session Log
**Date:** {{DATE}}
**Repo:** {{REPO_PATH}}
**Run duration:** [N minutes]

### Change Outcomes
- Changes proposed: N
- Changes approved: N  (🔴 N  |  🟡 N  |  🟢 N)
- Changes rejected by user: N
- Changes deferred: N
- Escalation hatches fired: [list phases + reason]

### User Override Patterns
> Changes the user rejected or modified — these are the skill's blind spots.

| Change | Why User Rejected / Modified | Pattern Signal |
|--------|------------------------------|----------------|
| M4: H1→H2 headings in /docs/legacy | "Those are intentional — always skip legacy docs" | Add legacy/* to default PROTECTED_EXCEPTIONS |

### Canonicalization Accuracy
> Were the canonical standards selected in Phase 4 validated by the user?

| Decision | User Validated | User Overrode | Notes |
|----------|---------------|---------------|-------|
| D1: kebab-case | Yes | — | — |
| D2: H2 headings | Partially | Yes — legacy folder | Missed exception scope |

### Escalation Hatch Activity
| Phase | Hatch | Fired? | Reason |
|-------|-------|--------|--------|
| Phase 2 Extract | Sparse inventory → GENERATE | No | Sufficient patterns found |
| Phase 4 Canonicalize | Dual justification → human review | Yes | Both naming patterns documented |

### Proposed Rule Improvements
> Generated by this session's patterns. Passed to skill-improver for review.

1. [OBSERVATION] User rejected H1→H2 changes in `/docs/legacy/` two runs in a row
   [PROPOSAL] Add `**/legacy/**` to the default `{{PROTECTED_EXCEPTIONS}}` list in starter config
   [CONFIDENCE] High (2/2 runs, same rejection)

2. [OBSERVATION] Phase 4 canonicalization halted for human review on 3 of 5 conflicts
   [PROPOSAL] Add "recent commit history" as a tiebreaker in `most-recent` standard priority
   [CONFIDENCE] Medium (need more data)
```

#### Invoking skill-improver

After writing the session log, invoke the **skill-improver** skill with:

```
Skill: skill-improver
Input:
  - skill_name: repo-steward
  - session_log: {{SELF_IMPROVE_LOG}}
  - improvement_proposals: [list from session log]
  - current_skill_version: {{VERSION}}
```

The skill-improver will:
1. Evaluate the proposed improvements against the skill's current rules
2. Accept, modify, or reject each proposal
3. If accepted: produce a diff showing the proposed change to `SKILL.md`
4. Surface the diff for human review before applying

> ⚠️ **skill-improver output is a proposal, not a commit.** The human reviews
> the suggested rule change before it is applied to the skill. This ensures
> the CI loop improves the skill without silently drifting its behavior.

#### Improvement Cycle Visualization

```
Run N:    Repo Steward executes → produces session log
             ↓
          skill-improver reads session log → proposes rule changes
             ↓
          Human reviews proposal → approves / rejects / modifies
             ↓
Run N+1:  Repo Steward uses updated rules → better canonicalization
          fewer user overrides → fewer deferred changes
             ↓
          (cycle repeats — skill gets smarter with every repo it touches)
```

#### Accumulated Intelligence

Over multiple runs, the skill builds a `.repo-steward/` directory in the repo:

```
.repo-steward/
  improvement-log.md          ← session logs (appended per run)
  deferred-changes.md         ← changes not yet approved
  decision-records/           ← D1.md, D2.md, etc. (persistent across runs)
  convention-registry.md      ← canonical standards established so far
```

This accumulated state means each run starts smarter than the last — the
skill doesn't re-discover the same conflicts, and the user doesn't re-approve
the same decisions.

---

## ⚠️ Anti-Patterns

```
REPO STEWARD ANTI-PATTERNS:

SAFETY ANTI-PATTERNS (new):

✗ Running without an approval gate
  Applying all changes in a single pass without human review.
  → One bad canonicalization decision corrupts the entire repo.
  Fix: Phase 5.5 APPROVE is the default. AUTONOMOUS_MODE requires explicit opt-in.
  Note: Even AUTONOMOUS_MODE always halts for 🔴 HIGH risk changes.

✗ Treating AUTONOMOUS_MODE as "safe"
  Assuming that because LOW/MEDIUM changes are auto-approved, no review is needed.
  → Every batch still has a Phase 5 manifest you should read before setting AUTONOMOUS_MODE.
  Fix: Always run DRY_RUN=true on the first pass for any new repo.

✗ Discarding unapproved changes silently
  Running, getting a rejection, and losing track of what was deferred.
  → The same conflicts surface every run with no progress.
  Fix: All unapproved changes go to .repo-steward/deferred-changes.md automatically.

✗ Skipping self-improvement logging
  Disabling SELF_IMPROVE_ENABLED to speed up runs.
  → The skill never learns from user overrides; the same wrong decisions repeat.
  Fix: Run Phase 8 even on dry runs — the session log is the CI input, not the changes.

CANONICALIZATION ANTI-PATTERNS:

✗ Canonicalizing without generating alternatives
  Picking the dominant pattern without asking "why does the other pattern exist?"
  → Leads to retroactively applying the wrong standard.
  Fix: Phase 4 GENERATE step is mandatory, not optional.

✗ Silent partial execution
  Renaming a file without updating all its references.
  → Breaks the repo in new ways while fixing old ones.
  Fix: Completeness checklist in Phase 6 is non-negotiable.

✗ Retroactive overreach
  Applying a new convention to a module with an explicit documented exception.
  → Removes intentional variation without understanding why it exists.
  Fix: Protected exception check runs before every retroactive application.

✗ Auto-resolving ambiguous conflicts
  Both patterns are documented — auto-picking one anyway.
  → Creates a new source of truth conflict at the documentation level.
  Fix: Ambiguous conflicts with dual justification → human review queue, not auto-apply.

✗ Treating new = canonical
  Assuming the most recently created files embody the intended direction.
  → New files are sometimes experimental, not policy.
  Fix: Recency is only one input; governance documents take precedence.

✓ CORRECT PATTERNS:

✓ DRY_RUN=true on first pass for any new repo (read before you write)
✓ Approval gate by default; AUTONOMOUS_MODE only after a verified dry run
✓ 🔴 HIGH changes always require per-change approval regardless of mode
✓ Unapproved changes deferred, never silently dropped
✓ Session log written after every run, even if no changes were applied
✓ Generate alternatives before selecting canonical (Phase 4)
✓ Completeness checklist for every change (Phase 6)
✓ Surface rather than auto-resolve ambiguous conflicts
✓ Retroactive batch is logged separately from direct changes
✓ Every unresolved item appears in the summary — nothing is silently dropped
```

---

## 🔁 Stress Test (Phase 6 ANCT Validation)

The following scenarios were used to validate the escalation hatches in this
architecture before release.

### Simulation 1: Repo with zero established conventions
- **Input:** A new repo with 5 files, no naming standards, no documentation
- **Expected:** Phase 2 EXTRACT produces an empty/sparse taxonomy → escalates to GENERATE within Phase 2: *"Propose 3 candidate initial conventions for this repo type"*
- **Result:** ✅ Hatch fires — NARRATE phase generates starter taxonomy proposal rather than returning empty output
- **Fix applied:** Added explicit GENERATE escalation path in Phase 2 for sparse inventories

### Simulation 2: Both patterns documented as intentional
- **Input:** `kebab-case` documented in CONTRIBUTING.md; `PascalCase` documented in a separate ADR for React components
- **Expected:** Phase 4 should NOT auto-canonicalize → should surface for human review
- **Result:** ✅ Hatch fires — Phase 4 correctly routes to `Human Review Required` in Phase 7 summary
- **Fix applied:** Added "dual justification" check in Phase 4 decision logic

### Simulation 3: Rename would break imports in another file
- **Input:** Rename `/src/Auth.ts` → `/src/auth.ts`, but `/src/index.ts` imports from `./Auth`
- **Expected:** Phase 5 cascade check catches the dependent import and adds it to the manifest
- **Result:** ✅ Cascade check in Phase 5 correctly adds `/src/index.ts` to the manifest
- **Fix applied:** Cascade check made explicit in Phase 5 safety gates

### Bicameral Regression: PASSED
```
[✅] Every DELEGATE phase has an input validation check
[✅] Every E1→E2 transition has a "schema mismatch" escalation defined
[✅] At least one NARRATE phase surfaces a user-facing alert (Phase 6 escalation)
[✅] No phase can fail silently (every failure path ends in Phase 7 "Remaining Inconsistencies")
[✅] Pipeline degrades gracefully: partial input → partial output + alert
```

---

## 🌐 Platform Notes

| Platform | How to Use |
|----------|------------|
| **CLI agents (Wibey, Claude Code)** | Load this SKILL.md as context; provide `{{REPO_PATH}}` and trigger a run |
| **Any LLM** | Paste as system context; ask: "Run Repo Steward against [repo description]" |
| **CI/CD integration** | Run as a scheduled job with `{{TRIGGER}}=scheduled` and `{{DRY_RUN}}=true` for automated conflict detection without auto-apply |
| **PR review** | Run with `{{TRIGGER}}=pr-review` and `{{SCOPE}}=structure-only` for a fast consistency check on incoming PRs |

---

## Compliance

- **PII Risk:** None. This skill operates on repository structure and code — no personal data processing.
- **Model Recommendation:** Sonnet for Phases 1–3 and 6–7 (deterministic and procedural). Opus for Phase 4 (canonicalization requires maximum reasoning depth for E4 creative judgment). Haiku for Phase 7 only (structured output from completed state).
- **Human Oversight:** Phase 5.5 (APPROVE) is the primary safety control. By default, the skill halts after Phase 5 and presents a full risk-scored audit report before any file is touched. The user must explicitly approve changes — by category, by ID, or all-at-once. The skill never executes without confirmation unless `{{AUTONOMOUS_MODE}}=true` is set, and even then, 🔴 HIGH-risk changes always require explicit per-change approval regardless of mode.
- **Autonomous Mode:** `{{AUTONOMOUS_MODE}}=true` is an explicit opt-in, not the default. It is only recommended after at least one verified dry run (`{{DRY_RUN}}=true`). Even in autonomous mode, HIGH-risk changes surface individually for approval.
- **Unapproved changes:** Any change that is rejected or left unanswered at the approval gate is written to `.repo-steward/deferred-changes.md` — it is never silently dropped. Deferred changes are surfaced at the top of the next run.
- **Retroactive scope:** Retrofits are applied in a discrete batch (Phase 6), logged separately, and scoped to only the items approved in Phase 5.5. The impact of retroactive changes is always visible and attributable.
- **Self-Improvement CI:** Phase 8 logs every session (overrides, deferrals, hatch activity, canonicalization outcomes) and optionally invokes **skill-improver** to propose rule improvements. All improvement proposals are returned as a human-reviewable diff — the skill never auto-patches itself.
- **Decision Records:** Every human override and all Phase 4 canonicalization decisions are written to `.repo-steward/decision-records/D[N].md` for audit trail and future dispute resolution.

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| **adaptive-workflow-architect** | Designed this skill's ANCT architecture |
| **skill-universalizer** | Repo Steward can be applied before universalizing a skill — ensuring the skill's repo structure is consistent first |
| **skill-improver** | Repo Steward operates on structure; skill-improver operates on behavior. They are complementary, not overlapping. |
| **docs-standardizer** (if it exists) | Repo Steward detects doc convention conflicts; a docs-specific skill executes the doc-only remediation path |
