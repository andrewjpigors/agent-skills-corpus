---
name: interactive-review
description: >-
  Orchestrates spec, ADR, and threat model reviews with interactive human
  confirmation for every significant finding. Runs review analysis, researches
  alternatives using web resources, and presents informed options via
  AskUserQuestion so every implementation, architecture, and security decision
  gets manual verification. Use when auditing project decisions interactively,
  onboarding to a new codebase and want to verify all decisions, reviewing
  architecture choices with human sign-off, or when security and implementation
  decisions must be manually approved. Triggers: interactive review, verify
  decisions, confirm decisions, review with approval, interactive audit,
  human-verified review.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep Bash(find *) Bash(ls *) Bash(git log *) WebSearch WebFetch AskUserQuestion
---

# Interactive Review

Review a project's specs, ADRs, and threat models — but don't just generate a report and hand it over. Instead, pause at every significant finding, research alternatives using the web, and present informed options to the human reviewer. Every critical and important decision gets individual confirmation with context. Suggestions get batched so you don't drown the reviewer in trivial questions.

This skill follows the same analysis logic as `spec-review`, `adr-review`, and `threat-model-review` but wraps it all with an interactive confirmation layer. The output isn't just a report — it's a **decision log** recording what was reviewed, what options were presented, what the human chose, and why.

## Quick Start

Interactive Review runs four stages: **Discover** (scan for artifacts), **Analyze** (run review logic), **Confirm** (present findings with researched options), **Report** (write a decision log). The confirmation stage is where the real value lives — you'll research each finding before presenting it, so the human gets informed choices rather than a blind accept/reject.

## When to Use This Skill

- Auditing a project's architecture, spec, and security decisions with human sign-off
- Onboarding to a codebase where you want to verify every decision, not just read about them
- Compliance or security review where each finding needs documented approval
- When autonomous review skills feel too "fire and forget" — you'd rather have a conversation
- After major changes when existing specs, ADRs, and threat models need re-validation
- Pre-release audit where every open finding must be triaged

## Workflow

```
Interactive Review Progress:
- [ ] Stage 1: Discovery — Scan for existing artifacts
- [ ] Stage 2: Analysis — Run review logic, classify findings
- [ ] Stage 3: Confirmation — Present findings with researched options
- [ ] Stage 4: Report — Write decision log
```

### Stage 1: Discovery & Scope

**Scan the project for existing documentation artifacts:**

```bash
# Check standard documentation locations
ls -la docs/ 2>/dev/null
find docs/ -name "*.md" -type f 2>/dev/null | sort

# Check each artifact type
ls docs/specs/*.md 2>/dev/null
ls docs/adr/*.md 2>/dev/null
ls docs/threat-models/*.md 2>/dev/null

# Look for non-standard locations
find . -maxdepth 2 -name "*.md" -path "*/arch/*" -o -name "*.md" -path "*/decisions/*" -o -name "*.md" -path "*/security/*" 2>/dev/null
```

**Check project context for analysis scope:**

```bash
# Tech stack
ls Cargo.toml package.json go.mod Gemfile requirements.txt pyproject.toml 2>/dev/null

# Git history for change frequency
git log --oneline --since="6 months ago" --stat | head -60
```

**Build an assessment matrix:**

```markdown
| Artifact | Exists? | Count | Last Updated | Review Scope |
|---|---|---|---|---|
| Specs | Yes/No | [N] | [date] | [Pending/Skip] |
| ADRs | Yes/No | [N] | [date] | [Pending/Skip] |
| Threat Model | Yes/No | [N] | [date] | [Pending/Skip] |
```

**Present the scope via AskUserQuestion:**

Ask which artifact types to review, which areas to prioritize, and whether there are off-limits areas. If artifacts are missing entirely, recommend `all-aboard` first but offer to proceed with what exists.

Example question structure:
- "Which artifact types should we review?" (multi-select: Specs, ADRs, Threat Models, All)
- "Focus area?" (options: Full project, Specific subsystem, Recent changes only, Security-critical paths)

### Stage 2: Run Review Analysis

Execute each review skill's analysis patterns for the artifacts in scope. Don't invoke the sub-skills directly — follow their analysis logic yourself so you can control the interactive flow.

**For specs (following `spec-review` logic):**
- Discover all spec files and their structure
- Gap analysis: compare requirements against implementation
- Quality assessment: testability, ambiguity, RFC 2119 keyword usage
- Cross-reference validation: spec → ADR links, spec → threat model links
- Traceability matrix completeness

**For ADRs (following `adr-review` logic):**
- Inventory all ADRs with status (Accepted, Deprecated, Superseded)
- Discover undocumented decisions by analyzing code and dependencies
- Quality assessment: MADR format compliance, alternatives documented, consequences listed
- Staleness check: do accepted ADRs still match the current implementation?
- Cross-reference validation: ADR → spec links, ADR → threat model links

**For threat models (following `threat-model-review` logic):**
- Locate threat model artifacts
- DFD validation: does the diagram match current architecture?
- STRIDE coverage: are all element-threat combinations addressed?
- Risk score validation: are DREAD scores reasonable and current?
- Mitigation audit: are mitigations implemented, tracked, or deferred?

**Classify all findings by severity:**

| Severity | Label | Confirmation Style |
|---|---|---|
| P0 | Critical | Individual confirmation with researched alternatives |
| P1 | Important | Individual confirmation with researched alternatives |
| P2 | Suggestion | Batched, multi-select confirmation |
| P3 | Minor | Batched, multi-select confirmation |

### Stage 3: Interactive Confirmation

This is the core of the skill. Each finding gets human review with context.

**For Critical (P0) and Important (P1) findings — one at a time:**

1. **Present the finding clearly:**
   - What was found, where (file path and line if applicable)
   - Why it matters — concrete risk or impact
   - Current state vs. expected state

2. **Research alternatives using web resources:**
   - For spec gaps: search for best practices for that requirement type (e.g., "EARS syntax authentication requirements best practice")
   - For ADR decisions: search for technology comparisons (e.g., "PostgreSQL vs CockroachDB vs SQLite comparison 2026")
   - For threat findings: search OWASP guidance, CWE entries, or security best practices (e.g., "OWASP session management cheat sheet")
   - For stale findings: search for what's changed since the decision was made

3. **Present via AskUserQuestion with 2 or 4 options** (never exactly 3 or 5):

   For a missing spec requirement:
   - "Add this requirement to the spec (Recommended)" — with suggested EARS wording
   - "Add with different wording" — let them specify
   - "Defer — document as known gap" — with justification prompt
   - "Reject — not needed" — with explanation prompt

   For an undocumented architecture decision:
   - "Create ADR documenting the current choice (Recommended)" — with researched context
   - "Create ADR but with a different rationale" — let them provide reasoning
   - "Defer — document later" — with timeframe
   - "Reject — this isn't an architectural decision" — with explanation

   For a threat model gap:
   - "Add this threat and implement mitigation (Recommended)" — with OWASP guidance
   - "Add threat but accept the risk" — with documented risk acceptance
   - "Add threat with alternative mitigation" — from research results
   - "Reject — not applicable to our context" — with explanation

4. **Record the decision** immediately — finding details, options shown, user choice, rationale provided, research sources consulted.

**For Suggestions (P2) and Minor (P3) — batched:**

Group related suggestions into batches of 4-6 items. Present as a multi-select AskUserQuestion:

"These suggestions came up during [spec/ADR/threat model] review. Select which ones to accept:"
- Option 1: "[Finding summary]" — what it does
- Option 2: "[Finding summary]" — what it does
- Option 3: "[Finding summary]" — what it does
- Option 4: "[Finding summary]" — what it does

Accepted items get added to the action items. Rejected items get logged as "Reviewed — declined." You won't need to explain every rejection.

**Confirmation order:**

Process findings in this order for each artifact type:
1. Critical (P0) — all, one by one
2. Important (P1) — all, one by one
3. Suggestions (P2) — batched
4. Minor (P3) — batched

Process artifact types in this order: threat model first (security context informs other decisions), then ADRs (architecture context informs spec review), then specs.

### Stage 4: Decision Log & Report

Write the decision log to `docs/decision-log-YYYY-MM-DD.md` using the [decision log template](assets/decision-log-template.md).

The decision log captures:

**For each finding:**
- Finding ID (e.g., `IR-001`)
- Source artifact type and location
- Severity classification
- Description of the finding
- Options presented (with research sources)
- Human decision: Confirmed / Modified / Deferred / Rejected
- Rationale provided by the reviewer
- Action items (if confirmed or modified)

**Summary section:**
- Total findings by severity and status
- Action items grouped by artifact type
- Deferred items with documented justification
- Research sources consulted (web links)
- Recommendations for follow-up

## Decision Categories

Each review skill produces different types of findings that need confirmation. See the [decision categories reference](references/decision-categories.md) for the full breakdown, including example WebSearch queries and AskUserQuestion patterns for each category.

**Summary of what gets confirmed:**

| Category | Source | What Gets Confirmed |
|---|---|---|
| Missing spec requirements | spec-review | Should this be specced? What requirement type? |
| Unimplemented requirements | spec-review | Still needed? Remove or prioritize? |
| Requirement quality issues | spec-review | Accept fix? Use alternative wording? |
| Undocumented decisions | adr-review | Right choice? Present researched alternatives |
| Stale ADRs | adr-review | Supersede, deprecate, or keep? |
| ADR quality issues | adr-review | Accept fix, rewrite, or mark acceptable? |
| DFD drift | threat-model-review | Confirm element added/removed? |
| Missing STRIDE coverage | threat-model-review | Threat relevant? What mitigations? |
| Risk score changes | threat-model-review | Accept score? Adjust? |
| Unimplemented mitigations | threat-model-review | Implement now, accept risk, or defer? |
| New threats discovered | threat-model-review | Add to model? What priority? |

## Research Patterns

Before presenting each Critical or Important finding, do targeted web research. This ensures the human gets informed options, not just a yes/no prompt. It's what separates this skill from a basic report.

**For technology decisions (ADRs):**
```
WebSearch: "[technology A] vs [technology B] comparison [current year]"
WebSearch: "[technology] alternatives [current year]"
```
Summarize the top alternatives with tradeoffs in 2-4 sentences when presenting the finding.

**For security findings (threat models):**
```
WebSearch: "OWASP [topic] cheat sheet"
WebSearch: "CWE-[number] mitigation guidance"
WebFetch: "https://cheatsheetseries.owasp.org/cheatsheets/[topic].html"
```
Include the recommended mitigation strategy from authoritative sources.

**For spec requirement patterns:**
```
WebSearch: "IEEE 830 [requirement type] examples"
WebSearch: "EARS syntax [requirement pattern] examples"
```
Suggest concrete EARS wording based on best practices.

## Working with Partial Artifacts

Not every project has all three artifact types — that's fine. Interactive Review adapts:

- **All artifacts exist:** Full review across all three types with cross-reference validation
- **Some artifacts exist:** Review what's available, flag what's missing as a Critical finding (since the human should decide whether to create what's missing)
- **No artifacts exist:** Recommend `all-aboard` first to bootstrap, but if the human wants to proceed anyway, do a code-based analysis and present findings as "things that should be documented"

## Integration with Other Skills

- **Analysis follows patterns from:** `spec-review`, `adr-review`, `threat-model-review`
- **Recommends creation via:** `spec-create`, `adr-create`, `threat-model-create`
- **Bootstrapping:** Points to `all-aboard` when artifacts don't exist
- **Writing style:** Applies `natural-writing-style` to the decision log
- **Feeds into:** `iterate` (confirmed decisions inform gap priorities), `implementation-review` (decision log informs classification)

## Writing Style

Apply `natural-writing-style` to the decision log and all finding summaries presented to the reviewer.

Be specific: when presenting a finding, name the artifact and location. When recording decisions, state exactly what was chosen and why. Don't claim a finding is resolved unless the reviewer explicitly confirmed it. The decision log is a record of what happened, not a polished summary — keep it accurate over tidy.

## Resources

- [Decision Categories Reference](references/decision-categories.md) — Full breakdown by review type with example queries and options
- [Decision Log Template](assets/decision-log-template.md) — Template for the output decision log
