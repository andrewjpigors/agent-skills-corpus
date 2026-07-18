---
name: adr-create
description: >-
  Creates and manages Architecture Decision Records using MADR 4.0.0 format
  with Nygard's immutability principles. Handles new ADRs, superseding existing
  ones, and retroactively documenting past decisions from code analysis. Links
  decisions to spec requirements and threat model entries. Use when documenting
  an architecture decision, choosing between technologies, recording why a
  design choice was made, or backfilling undocumented decisions. Triggers:
  create ADR, document decision, architecture decision, why did we choose,
  record decision, backfill ADR.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep Bash(ls *) Bash(find *) AskUserQuestion
---

# ADR Create

Capture the "why" behind architectural decisions so future you (and your team) don't have to guess. ADRs are short, immutable records stored in version control alongside the code they describe. This skill handles creating new ADRs, superseding outdated ones, and retroactively documenting decisions that were made but never recorded.

## Quick Start

An ADR answers one question: **"Why did we decide X instead of Y?"** Each ADR has a sequential number, a clear title, the context that drove the decision, the options you considered, and the consequences you expect. Once accepted, an ADR is immutable — new insights get a new ADR that supersedes the old one.

Store ADRs in `docs/adr/` with the naming pattern `NNNN-brief-title.md`.

## When to Use This Skill

- You've chosen a technology, framework, library, or architectural pattern and need to document why
- You're about to make a decision and want to structure your thinking
- An existing project has undocumented decisions embedded in the code that need retroactive ADRs
- A previous decision needs to be revisited — create a new ADR that supersedes the old one
- The `spec-create` or `threat-model-create` skill flagged missing ADRs
- A code review reveals an architectural choice without documented rationale

Don't use this for implementation details — those belong in specs. Don't use this for security threat analysis — that's `threat-model-create`. ADRs capture *decisions*, not *requirements* or *threats*.

## Workflow

```
ADR Creation Progress:
- [ ] Phase 1: Discover existing ADRs and context
- [ ] Phase 2: Identify the decision to record
- [ ] Phase 3: Analyze options
- [ ] Phase 4: Write the ADR
- [ ] Phase 5: Cross-reference and validate
```

### Phase 1: Discovery

**Check for existing ADRs first:**

```bash
ls docs/adr/*.md 2>/dev/null | head -30
```

**If ADRs exist:**
- Read them to understand numbering, format, and conventions
- Check if this decision is already recorded (don't duplicate)
- Identify the next available number

**If no ADRs exist:**
- Create the directory: `mkdir -p docs/adr`
- Start with ADR-0001: "Record Architecture Decisions" (the meta-ADR documenting that you're using ADRs)
- Use the template from [assets/adr-full-template.md](assets/adr-full-template.md)

**Check for related artifacts:**
- Existing spec → What decisions does the spec assume but not document?
- Existing threat model → What security decisions need ADRs?
- README or design docs → What choices are mentioned but not formally recorded?
- Git history → What major changes imply decisions that were never documented?

### Phase 2: Identify the Decision

**For new decisions** — scan Phase 1 findings first, then **use `AskUserQuestion`** to ask:
- What's the specific decision point? ("Which database?" not "How to build the app")
- What constraints or forces are driving this decision?
- Who needs to be involved or informed?
- Is this reversible? How costly would it be to change later?

Pre-populate the question with candidate decision points you found in Phase 1 (undocumented dependencies, infrastructure choices, architectural patterns).

**For retroactive documentation** — mine the codebase:

- Look at `package.json`, `Cargo.toml`, `go.mod`, `Gemfile` — every dependency is a decision
- Check infrastructure files (Dockerfile, docker-compose, Terraform, Nix) — deployment choices
- Read configuration files — they reveal architectural patterns
- Check git log for major structural changes: `git log --oneline --diff-filter=A -- '*.toml' '*.json' '*.yaml'`
- Look for comments like "we chose X because..." or "TODO: reconsider this"
- Review CI/CD configuration — pipeline choices are often undocumented decisions

**For superseding decisions** — when a previous ADR needs updating:

- Don't modify the original ADR (it's immutable)
- Create a new ADR that references and supersedes the old one
- Update the old ADR's status to "Superseded by ADR-NNNN"

### Phase 3: Analyze Options

For each option considered, document:

- **What it is** (one sentence)
- **Pros** — concrete benefits, not marketing language
- **Cons** — real drawbacks, not strawman dismissals

You MUST consider at least 2 options. If there's genuinely only one viable choice, document why alternatives were ruled out. "We didn't consider alternatives" is a red flag — it usually means you haven't thought hard enough.

**Be honest about trade-offs.** Every option has cons. If your analysis shows one option with only pros and another with only cons, you're not being objective.

### Phase 4: Write the ADR

Use MADR 4.0.0 format (see [references/madr-template.md](references/madr-template.md) for the full template). At minimum, every ADR needs:

```markdown
---
status: accepted
date: 2024-01-15
decision-makers: [names]
---

# ADR-NNNN: [Decision Title as Noun Phrase]

## Context and Problem Statement

[2-4 sentences describing the situation and the decision that needs to be made.
Value-neutral — describe forces at play, not conclusions.]

## Decision Drivers

- [Force 1 — what's pushing toward a decision]
- [Force 2]
- [Force 4] (yes, skip 3 — don't use exactly 3 or 5 items)

## Considered Options

1. [Option A]
2. [Option B]

## Decision Outcome

Chosen option: "[Option A]", because [1-2 sentence justification connecting
back to decision drivers].

### Consequences

**Good:**
- [Positive consequence]
- [Another positive consequence]

**Bad:**
- [Negative consequence — be honest]
- [Trade-off accepted]

**Neutral:**
- [Side effect that's neither good nor bad]
```

### Phase 5: Cross-Reference and Validate

**Link to spec requirements.** If this decision constrains or enables specific requirements:

```markdown
## More Information

- Implements: [SPEC-003: Session Storage](../specs/auth-spec.md#fr-003)
- Driven by: [TM-AUTH-003: Session Hijacking](../threat-models/auth-threat-model.md#tm-auth-003)
- Supersedes: [ADR-0003](0003-use-memcached.md) (if applicable)
```

**Link to threat model.** Security-driven decisions should reference the specific threat:

```markdown
This decision addresses [TM-AUTH-001: Credential Theft] by selecting bcrypt
over MD5 for password hashing, accepting the performance trade-off of
~300ms per hash operation.
```

**Flag missing artifacts.** If the decision implies requirements or threats that aren't documented:

```markdown
> **Action needed:** This decision affects session management requirements
> not yet in the spec. Run `spec-create` to add FR-XXX for session handling.

> **Action needed:** This introduces a new trust boundary (app → Redis) not
> in the threat model. Run `threat-model-create` to analyze.
```

**Validate the ADR:**

- [ ] Status is set (proposed, accepted, deprecated, or superseded)
- [ ] Date is present
- [ ] Context describes forces, not conclusions
- [ ] At least 2 options were considered
- [ ] Chosen option is justified with connection to decision drivers
- [ ] Consequences include both good and bad (honest trade-offs)
- [ ] Title is a noun phrase, not a sentence
- [ ] Cross-references to spec and threat model are present or flagged

## The ADR-0001 Bootstrap

Every project's first ADR records the decision to use ADRs:

```markdown
---
status: accepted
date: [today]
decision-makers: [team]
---

# ADR-0001: Record Architecture Decisions

## Context and Problem Statement

Architectural decisions are made throughout the project but aren't documented.
New team members can't understand why things are built the way they are, leading
to either blind acceptance or blind reversal of past decisions.

## Considered Options

1. Use Markdown ADRs in version control (MADR format)
2. Track decisions in a wiki

## Decision Outcome

Chosen option: "Markdown ADRs in version control", because decisions stay
alongside the code they describe, get reviewed in PRs, and have full git
history.

### Consequences

**Good:**
- Decisions are versioned and reviewable
- New team members can read the decision log

**Bad:**
- Requires discipline to write ADRs for significant decisions
- Adds files to the repository
```

## Status Lifecycle

See [references/status-lifecycle.md](references/status-lifecycle.md) for full details. See also the global `artifact-status-tracking` rule for how these statuses integrate with the iterate skill's completion checking.

```
Proposed → Accepted → [Deprecated | Superseded by ADR-NNNN]
```

**IMPORTANT:** These are the ONLY valid values for the `status:` frontmatter field. The iterate skill's completion check script validates these and checks `accepted` ADRs for implementation evidence.

| Status | Meaning | Set when | Iterate check |
|---|---|---|---|
| `proposed` | Under discussion | ADR first drafted, before team agreement | Skipped |
| `accepted` | Decision in effect (immutable) | Team agrees via PR merge or review | Implementation files checked |
| `deprecated` | No longer relevant | Feature removed or constraint gone | Skipped |
| `superseded` | Replaced by newer ADR | New ADR written with different decision | Skipped |

**For `accepted` ADRs:** If you include an `## Implementation Location` section referencing code files (e.g., `` `crates/foo/src/bar.rs` ``), the completion checker verifies those files exist. Missing files are flagged as P1 gaps. This is how the iterate skill knows an architectural decision has been coded, not just documented.

**Setting the status:**
```yaml
---
status: accepted
date: 2026-04-01
decision-makers: [team-member]
---
```

## Retroactive ADR Workflow

When documenting decisions that were made in the past:

1. **Identify the decision** from code, config, or git history
2. **Reconstruct the context** — what was true when this choice was made?
3. **Infer alternatives** — what else could have been chosen? Why wasn't it?
4. **Write the ADR** with the original decision date if known
5. **Set status to "accepted"** — it was accepted implicitly by being implemented
6. **Note in "More Information"**: "Retroactively documented on [today's date]"

## Writing Style

Apply the `natural-writing-style` skill. ADRs should read like a thoughtful memo from a colleague, not a legal contract. The context section especially should tell a story — what situation you were in, what pressures you faced, why this decision mattered.

Be direct about trade-offs. "We accepted slower hash times for better security" is more useful than "the solution was deemed appropriate."

## Resources

- [MADR Template](references/madr-template.md) — Full MADR 4.0.0 template with all optional sections
- [Status Lifecycle](references/status-lifecycle.md) — ADR status transitions and rules
- [Full ADR Template](assets/adr-full-template.md) — Copy-paste starter with all sections
- [Minimal ADR Template](assets/adr-minimal-template.md) — Bare-minimum ADR for quick decisions
