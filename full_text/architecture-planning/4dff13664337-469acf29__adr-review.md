---
name: adr-review
description: >-
  Reviews Architecture Decision Records for quality, completeness, and
  consistency. Identifies undocumented decisions by analyzing code, specs,
  and threat models. Backfills missing ADRs for past decisions, validates
  cross-references, and checks the decision log for staleness or
  contradictions. Use when auditing ADRs, finding missing decisions,
  reviewing ADR quality, checking for undocumented architecture choices,
  or when spec-review or threat-model-review flags missing ADRs. Triggers:
  review ADR, audit decisions, missing ADRs, ADR quality, backfill ADRs,
  decision log, undocumented decisions.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep Bash(ls *) Bash(find *) Bash(git log *) AskUserQuestion
hooks:
  SessionStart:
    - hooks:
        - type: prompt
          prompt: |
            Context was compacted. Re-assess ADR review state per /adr-review instructions:
            - Check which ADRs exist and their current quality
            - Identify undocumented architectural decisions in the codebase
            - Review cross-references to specs and threat models
            - Continue ADR review from current state
            - Check for stale or contradictory decisions
  Stop:
    - hooks:
        - type: command
          command: python3 "$HOME/.claude/skills/adr-review/scripts/check-completion.py"
          timeout: 120
compatibility: >-
  Hook paths assume global install at $HOME/.claude/skills/adr-review/.
  Adjust the hook command path if you install skills elsewhere.
---

# ADR Review

Audit your decision log for gaps, staleness, and quality issues. It's surprisingly common for teams to make important decisions and never write them down. This skill finds decisions hiding in code that don't have ADRs, checks existing ADRs for completeness, validates cross-references to specs and threat models, and backfills what's missing by analyzing the codebase.

## Quick Start

An ADR review answers: **Are all significant decisions documented?** (completeness) **Are existing ADRs well-written?** (quality) **Do ADRs still reflect reality?** (currency) **Are cross-references intact?** (traceability). When it finds undocumented decisions, it recommends creating ADRs via `adr-create`.

The built-in Stop hook keeps the review running until all gates pass — you don't need to re-invoke it manually. See [HOOKS.md](HOOKS.md) for details.

**Running in opencode:** the `hooks:` frontmatter is ignored, so the loop isn't automatic. Either re-run the skill until it reports no gaps, or opt into the `.opencode/plugins/completion-loop.ts` plugin for this review by setting `OPENCODE_REVIEW_LOOP=adr-review` while it runs. Tool-name mapping (e.g. `AskUserQuestion` → `question`) is in [docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

## When to Use This Skill

- Auditing the decision log before a new team member joins
- Checking whether all technology choices are documented
- The `spec-review` or `threat-model-review` skill flagged missing ADRs
- A major refactoring changed architectural decisions that may invalidate existing ADRs
- Periodic maintenance to keep the decision log current
- Verifying ADR quality before a governance review

## Workflow

```
ADR Review Progress:
- [ ] Phase 0: Locate decision log and identify ADR format in use
- [ ] Phase 1: Inventory existing ADRs
- [ ] Phase 2: Discover undocumented decisions
- [ ] Phase 3: Quality assessment
- [ ] Phase 4: Cross-reference validation
- [ ] Phase 5: Report findings and backfill recommendations
```

### Phase 1: Inventory Existing ADRs

**Find all ADRs:**

```bash
find docs/adr/ -name "*.md" -type f 2>/dev/null | sort
```

**If no ADRs exist:**
- Scan for ADRs in non-standard locations: `docs/decisions/`, `architecture/`, README files, and any `.md` files with "decision" or "architecture" in the name
- **Use `AskUserQuestion`** to ask: "No ADRs found in `docs/adr/`. I found [X candidate locations / no candidates]. Should I scan [list candidates] or start fresh with ADR-0001?"
- Jump to Phase 2 to discover what decisions exist
- Recommend starting with ADR-0001: "Record Architecture Decisions"

**If ADRs exist, catalog them:**

For each ADR, extract:
- Number and title
- Status (proposed, accepted, deprecated, superseded)
- Date
- Whether it has cross-references to spec and threat model

Build a summary table:

```markdown
| ADR | Title | Status | Date | Spec Link | TM Link |
|---|---|---|---|---|---|
| 0001 | Record Architecture Decisions | Accepted | 2024-01-10 | — | — |
| 0002 | Use PostgreSQL for User Data | Accepted | 2024-01-15 | FR-001 | TM-DB-001 |
| 0003 | Use Memcached for Sessions | Superseded | 2024-01-20 | — | — |
```

### Phase 2: Discover Undocumented Decisions

This is the highest-value part of the review. Mine the codebase for decisions that aren't captured in ADRs.

**Technology choices (check dependency files):**

```bash
# Check package managers for technology decisions
cat Cargo.toml package.json go.mod Gemfile requirements.txt pyproject.toml 2>/dev/null
```

Every significant dependency is a decision. Ask: is there an ADR explaining why this library was chosen over alternatives? If there isn't, that's a backfill candidate. Focus on:
- Database technology
- Web framework
- Authentication library
- Cache/queue technology
- Logging/monitoring tools
- Testing frameworks (when non-obvious choices were made)

**Infrastructure decisions (check deployment files):**

```bash
find . -name "Dockerfile" -o -name "docker-compose*" -o -name "*.tf" -o -name "*.nix" -o -name "nginx*" -o -name "Procfile" 2>/dev/null
```

Look for: container orchestration, reverse proxy, cloud provider, deployment strategy, CI/CD pipeline choices.

**Architectural patterns (check code structure):**

- What pattern does the codebase follow? (MVC, hexagonal, microservices, monolith)
- How is authentication implemented? (JWT, sessions, OAuth)
- How is data accessed? (ORM, raw SQL, repository pattern)
- How is configuration managed? (env vars, config files, secrets manager)
- How are errors handled? (global handler, per-module, result types)
- How are services communicating? (REST, gRPC, message queue, shared database)

**Git history for major decisions:**

```bash
# Find large structural changes
git log --oneline --diff-filter=A -- '*.toml' '*.json' '*.yaml' '*.yml' '*.nix' | head -20

# Find migration-like changes
git log --oneline --grep="migrate\|switch\|replace\|upgrade\|deprecate" | head -15
```

**Check spec and threat model for ADR gaps:**
- Read `docs/specs/*.md` — technology choices mentioned without ADR references
- Read `docs/threat-models/*.md` — security decisions without ADR backing

### Phase 3: Quality Assessment

For each existing ADR, check:

**Format compliance:**
- [ ] YAML frontmatter present with status and date
- [ ] Title is a noun phrase (not a sentence or question)
- [ ] Sequential numbering is consistent
- [ ] File naming matches `NNNN-brief-title.md`

**Content quality:**
- [ ] Context describes forces and situation, not conclusions
- [ ] At least 2 options were considered (not just "we decided X")
- [ ] Pros and cons are honest (not strawman arguments against rejected options)
- [ ] Decision outcome connects to decision drivers
- [ ] Consequences include both good and bad outcomes
- [ ] Decision date is present and plausible (not a future date or placeholder)

**Common quality issues:**

| Issue | Example | Fix |
|---|---|---|
| One-option ADR | "We decided to use React" with no alternatives | Add at least one alternative with honest pros/cons |
| Strawman rejection | "Option B was considered but it's terrible" | Provide genuine pros for rejected options |
| Missing consequences | No "Bad" consequences listed | Every decision has trade-offs — document them |
| Context as conclusion | "Because X is best, we chose X" | Describe the situation, not the outcome |
| Status not set | No frontmatter or status field | Add MADR frontmatter |
| Invalid status value | `status: wip` or `status: in-progress` | Must be one of: `proposed`, `accepted`, `deprecated`, `superseded` |
| Accepted ADR with no implementation | `status: accepted` but `## Implementation Location` references missing files | Flag as P1 gap — decision made but code not written |

**Status field validation (see `artifact-status-tracking` rule):**

The iterate skill's completion check script validates ADR statuses. Only these values are recognized:
- `proposed` — skipped (not yet decided)
- `accepted` — checked for implementation evidence (referenced files must exist)
- `deprecated` — skipped
- `superseded` — skipped (must link to replacement ADR)

Flag any ADR using a non-standard status value (e.g., "draft", "wip", "in-progress", "todo"). These won't be tracked correctly by the iterate skill.

For `accepted` ADRs with an `## Implementation Location` section, verify that referenced code files actually exist. Missing files mean the decision was made but not yet coded — that's a gap the iterate skill will flag.

**Staleness check:**
- [ ] Accepted ADRs still reflect current architecture
- [ ] No accepted ADRs describe technology that's been replaced
- [ ] Superseded ADRs correctly reference their replacements
- [ ] Deprecated ADRs have a reason documented

### Phase 4: Cross-Reference Validation

**Spec cross-references:**
- [ ] ADRs for technology choices reference the spec requirements they enable
- [ ] Spec requirements that cite ADRs link to existing, accepted ADRs
- [ ] No broken links between specs and ADRs
- [ ] Superseded ADRs don't still appear as active references in specs

**Threat model cross-references:**
- [ ] Security-related ADRs reference the threats they mitigate
- [ ] Threat model mitigations that cite ADRs link to existing, accepted ADRs
- [ ] No broken links between threat models and ADRs
- [ ] Deprecated or superseded ADRs cited in threat models have updated references

**Internal consistency:**
- [ ] Superseded ADRs correctly chain to their replacements
- [ ] No circular supersession (A supersedes B supersedes A)
- [ ] Numbering is sequential with no duplicates
- [ ] No two accepted ADRs make contradictory decisions about the same concern

### Phase 5: Report and Recommendations

Write the report to `docs/adr-review-report.md` (the Stop hook checks this location).

```markdown
## ADR Review Report

### Summary
- **Existing ADRs:** [count]
- **Status breakdown:** [X] accepted, [Y] superseded, [Z] deprecated
- **Undocumented decisions found:** [count]
- **Quality issues:** [count]
- **Missing cross-references:** [count]
- **Stale ADRs (no longer reflect reality):** [count]

### Undocumented Decisions (Backfill Needed)
| Decision | Source | Recommended ADR Title | Priority |
|---|---|---|---|
| PostgreSQL for data | Cargo.toml, docker-compose | Use PostgreSQL for Persistent Storage | High |
| JWT for auth | auth.rs, config | JWT-Based Authentication | High |
| Redis for caching | docker-compose, cache.rs | Redis for Application Caching | Medium |
| Monorepo structure | directory layout | Monorepo Project Structure | Low |

### Quality Issues
| ADR | Issue | Fix |
|---|---|---|
| ADR-002 | Only one option considered | Add alternatives analysis |
| ADR-005 | No bad consequences listed | Document trade-offs honestly |
| ADR-007 | Status missing | Add MADR frontmatter |

### Cross-Reference Gaps
| ADR | Missing Link To | Action |
|---|---|---|
| ADR-002 | Spec FR-001 | Add spec reference in "More Information" |
| ADR-003 | Threat TM-AUTH-001 | Link to threat model entry |

### Recommendations
[Prioritized actions — typically: 1) backfill critical undocumented decisions,
2) fix quality issues in existing ADRs, 3) update cross-references]
```

## Backfilling ADRs

When the review identifies undocumented decisions:

1. **Prioritize** — Document decisions with security implications first, then technology choices, then patterns
2. **Use `adr-create`** with retroactive workflow for each decision
3. **Cross-reference immediately** — link new ADRs to spec and threat model
4. **Don't backfill everything at once** — 4-6 ADRs per session is sustainable

## Writing Style

Apply the `natural-writing-style` skill. Review findings should be specific: "ADR-003 lists no alternatives — it just says 'we chose Redis.' Add at least one alternative (Memcached, in-process cache) with honest pros and cons."

Don't claim the decision log is "complete" — state what you reviewed, how many decisions you identified, and what areas of the codebase weren't examined.

## Resources

- [Review Checklist](references/review-checklist.md) — Detailed ADR review criteria
- [Stop Hook](HOOKS.md) — Auto-continuation hook that keeps the review going until all gates pass
