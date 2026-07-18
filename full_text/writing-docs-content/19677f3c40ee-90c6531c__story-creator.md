---
name: story-creator
description: >-
  Creates formal E2E user stories with BDD acceptance criteria, EARS constraints,
  and INVEST compliance through interactive user prompting. Use when creating new
  feature stories, documenting agent behaviors, writing acceptance criteria for
  multi-agent systems, or starting a new feature that needs behavioral verification
  coverage. Integrates with all-aboard documentation onboarding and rewrite-in-rust
  phase 1 analysis. Triggers: write user story, create story, BDD story, acceptance
  criteria, feature story, E2E behavior, agent story, INVEST story, Gherkin story.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep AskUserQuestion Bash(ls *) Bash(find *) Bash(git log *)
---

# Story Creator

Turns vague feature ideas into precise, testable user stories. You'll answer questions interactively — the skill assembles a story that satisfies INVEST criteria, includes Gherkin acceptance criteria, carries EARS constraints for system-level behavior, and maps to whatever verification standard your project uses (SLSA, SSDF, SCVS, or none). It's designed for multi-agent systems where autonomy boundaries matter, but works just as well for plain web features.

## Quick Start

The workflow starts with a gap analysis — scanning your specs, ADRs, threat model, and implementation to surface candidate stories you might be missing. Then it runs an interactive interview to build each story from scratch. You don't need to know all the answers upfront.

1. **Gap Analysis** — Scan existing docs and code to suggest missing stories
2. **Context** — Who's the user/agent? What triggers the behavior?
3. **Goal** — What should happen and why does it matter?
4. **Acceptance** — Given/When/Then scenarios covering happy path and failures
5. **Constraints** — Autonomy limits, security requirements, and EARS invariants
6. **Write** — Assemble and save the story artifact

The output is a structured story artifact you can commit to `docs/stories/`.

## When to Use This Skill

- Starting a feature that needs formal behavioral verification
- Documenting multi-agent system behaviors where autonomy boundaries matter
- Before running `tdd-workflow` — stories are the spec that drives test creation
- During `all-aboard` onboarding when behavioral specs are missing
- At the start of a `rewrite-in-rust` phase 1 analysis (the behavioral spec IS the story)
- When `story-reviewer` flags a story as incomplete and it needs a rewrite

## Workflow

```
Story Creation Progress:
- [ ] Stage 0: Gap Analysis — Scan docs and code to surface candidate stories
- [ ] Stage 1: Context — Establish role, system, and trigger
- [ ] Stage 2: Goal — Clarify motivation and measurable outcome
- [ ] Stage 3: Acceptance — Draft Given/When/Then scenarios
- [ ] Stage 4: Constraints — Add EARS invariants, autonomy limits, security mapping
- [ ] Stage 5: INVEST check — Validate and refine
- [ ] Stage 6: Write artifact — Save to docs/stories/
```

### Stage 0: Gap Analysis

Before writing any story, scan the project to understand what already exists and what's missing. This surfaces candidate stories you can pick from — or skip entirely if the user already knows what they want to write.

**Scan existing documentation:**

```bash
# Existing stories
find docs/stories -name "*.md" 2>/dev/null | sort

# Spec requirements
find docs/specs -name "*.md" 2>/dev/null | sort
grep -rh "^## FR-\|^## NFR-\|^## IR-" docs/specs/ 2>/dev/null | sort

# Threat model entries and mitigations
grep -rh "^## TM-\|Mitigation\|Trust boundary" docs/threat-models/ 2>/dev/null | head -40

# ADRs — decisions reveal behaviors that need stories
find docs/adr -name "*.md" 2>/dev/null | sort

# Component structure from code
find . -maxdepth 3 \( -name "*.rs" -o -name "*.go" -o -name "*.py" -o -name "*.ts" \) \
  | sed 's|/[^/]*$||' | sort -u | grep -v node_modules | grep -v target | head -30
```

**Build a candidate story list** from what you find. For each gap, derive a candidate story:

| Source | Signal | Candidate Story |
|---|---|---|
| Spec `FR-NNN` with no linked story | Functional requirement | "As a [actor], I want [FR behavior]..." |
| Threat model mitigation with no story | Security flow | "[Actor] handles [attack scenario]" |
| ADR describing a behavioral contract | Architectural decision | "System [behaves as ADR specifies]" |
| Source directory with no story coverage | Undocumented subsystem | End-to-end behavior of that component |
| Trust boundary crossing in threat model | Inter-component interaction | Message flow between services/agents |

**Present candidates using `AskUserQuestion`:**

Use `AskUserQuestion` with type `select` or `multiselect` to let the user choose which story to write (or confirm their own):

```
Which story would you like to create?

Suggested candidates based on gap analysis:
  (a) [Candidate from FR-001: user auth flow — no story exists]
  (b) [Candidate from TM-AUTH-002: brute force mitigation — no behavioral story]
  (c) [Candidate from docs/adr/0003: rate limiting decision — behavior undocumented]
  (d) [Candidate from src/agent/ — no story covers agent orchestration behavior]
  (e) Something else — I'll describe it
```

If the user already described what they want to write (e.g. invoked with a specific topic), skip directly to Stage 1 using their description as context. Still run the scan so you can cross-reference spec requirements and threat entries during Stage 4.

If no docs exist yet (brand new project), skip straight to Stage 1 and note in the artifact that it's a greenfield story with no current spec cross-references.

### Stage 1: Context

Start by understanding who this story is about and what kicks off the behavior.

**Use `AskUserQuestion`** to ask:

```
Who is the primary actor? Choose one:
  (a) A human user role (customer, admin, reviewer, operator)
  (b) An AI agent (describe its capability)
  (c) An external system (API, service, CI pipeline)
  (d) A scheduled job or background process
```

If (b) — agent — **use `AskUserQuestion`** to follow up:
- What data does it consume? (files, API responses, database records, messages)
- What tools does it have access to?
- What can it NOT do? (prohibited actions)

Then **use `AskUserQuestion`** to ask:
```
What event or condition triggers this behavior?
Examples: "user clicks Deploy", "agent receives a ZeroMQ message",
          "CI pipeline completes", "scheduled daily at midnight"
```

Record: `actor`, `actor_type`, `trigger`.

### Stage 2: Goal

**Use `AskUserQuestion`** to ask:
```
What does the actor want to achieve?
Be specific — "process the request" is too vague.
"Parse the SARIF file and normalize findings into canonical CVE records" is good.
```

Then **use `AskUserQuestion`** again:
```
Why does this matter? What business or system outcome does it enable?
```

Use this to write the story title and role-goal-benefit statement:

```
Title: [Actor Name] — [Capability]
As a <role>, I want <action>, so that <outcome>.
```

Validate: does the "so that" describe a real benefit, not just echo the action?

Record: `title`, `story_statement`.

### Stage 3: Acceptance Criteria

This is where the story gets testable. Walk through each scenario type.

**Happy path — use `AskUserQuestion`:**
```
Describe the normal, successful flow.
What must be true before it starts? (Given)
What action triggers it? (When)
What must be true when it completes? (Then)
```

Write as:
```gherkin
Scenario: [name]
  Given <precondition>
  When <trigger>
  Then <measurable outcome>
```

**Failure/error scenarios — use `AskUserQuestion`:**
```
What can go wrong? Name the top failure modes.
For each: what should the system do instead?
```

Add one scenario per failure mode. At minimum cover:
- Input validation failure
- Downstream dependency unavailable
- Timeout or partial completion

**Boundary conditions — use `AskUserQuestion`:**
```
Are there edge cases that stress the limits?
Examples: empty inputs, max-size payloads, concurrent requests,
          rate limits hit, permissions revoked mid-operation.
```

Add scenarios for the important ones.

**Target:** 2-4 acceptance criteria total. More than 4 means the story should split.

Record: `acceptance_criteria` (array of Gherkin scenarios).

### Stage 4: Constraints

**EARS invariants — use `AskUserQuestion`:**
```
Are there system-level guarantees that must always hold?
Examples:
  "While processing, the agent shall not modify source data."
  "If authentication fails, the system shall log the attempt and halt."
  "The system shall complete within 30 seconds."
```

Map to EARS templates:
- `While <state>, the <Actor> shall <behavior>.` — State-driven
- `If <failure>, then the <Actor> shall <fallback>.` — Unwanted behavior
- `When <event>, the <Actor> shall <response>.` — Event-driven
- `The <Actor> shall <invariant>.` — Ubiquitous

**For agent actors, also use `AskUserQuestion`:**
```
What are the autonomy limits?
  - Maximum actions per cycle?
  - When should it escalate to a human?
  - What is it explicitly prohibited from doing?
```

**Security mapping — use `AskUserQuestion`:**
```
Does this story involve any of these? (answer yes/no for each)
  - Authentication or authorization checks
  - Data that crosses a trust boundary
  - External inputs (user data, file uploads, network responses)
  - Writes to a database or persistent store
  - Secrets, tokens, or credentials
```

For each "yes", add a corresponding acceptance criterion or EARS constraint.

If the project uses supply chain security standards, map to them:
```
SLSA Level: [1/2/3 or N/A]
SCVS Controls: [list or N/A]
SSDF Practices: [list or N/A]
OpenSSF Scorecard checks: [list or N/A]
```

Record: `ears_constraints`, `autonomy_limits`, `security_mapping`.

### Stage 5: INVEST Check

Validate against each criterion. Ask the user to confirm or flag issues:

| Criterion | Question to ask |
|---|---|
| Independent | Can this be built without another incomplete story? |
| Negotiable | Is the HOW open, or is it over-specified? |
| Valuable | Does the "so that" describe real value? |
| Estimable | Do you have enough information to scope this? |
| Small | Can this be completed in one sprint/iteration? |
| Testable | Does each acceptance criterion have a clear pass/fail? |

If Small fails, ask:
```
Let's split this. What's the smallest version that still delivers value?
That becomes story 1. What's left becomes the backlog.
```

If Testable fails, return to Stage 3 and add concrete measurable outcomes.

### Stage 6: Write the Artifact

Assemble everything into the story format. See the global `artifact-status-tracking` rule for how story statuses integrate with the iterate skill's completion checking.

**Story status lifecycle (MUST use these exact values):**

| Status | Meaning | Set when | Iterate blocks? |
|---|---|---|---|
| `Draft` | Written, not yet implemented | Story first created | Yes (P1) |
| `Revision N` | Revised after review, not implemented | After story-reviewer feedback | Yes (P1) |
| `Implemented` | Acceptance criteria coded and tested | All scenarios have passing tests | No |
| `Complete` | Fully finished and verified | Post-implementation validation | No |

Stories in `Draft` or `Revision N` status represent planned but unfinished work. The iterate skill's completion script counts them and blocks iteration until they're `Implemented`. When you finish implementing a story's acceptance criteria with passing tests, update its status to `Implemented`.

```markdown
# Story: [Title]

**Story ID:** STORY-[NNN]
**Status:** Draft
**Created:** [date]

## Statement

As a <role>, I want <action>, so that <outcome>.

## Trigger

<trigger condition>

## Acceptance Criteria

### Scenario: [Happy path name]
```gherkin
Given <precondition>
When <trigger>
Then <measurable outcome>
```

### Scenario: [Error case name]
```gherkin
Given <precondition>
When <trigger>
Then <error outcome>
```

[Additional scenarios...]

## EARS Constraints

- While <state>, the <Actor> shall <behavior>.
- If <failure>, then the <Actor> shall <fallback>.
[Additional EARS...]

## Autonomy Limits (agent actors only)

- Maximum actions per cycle: <N>
- Escalation threshold: <condition>
- Prohibited actions: <list>

## Security Mapping

| Concern | Addressed By |
|---|---|
| [STRIDE category] | [Scenario or EARS constraint] |

## Standards Mapping

- SLSA Level: [N or N/A]
- SSDF Practices: [list or N/A]
- SCVS Controls: [list or N/A]

## Dependencies

- Depends on: [STORY-NNN or none]
- Blocks: [STORY-NNN or none]
- Related ADR: [ADR-NNNN or none]
- Related spec requirement: [FR-NNN or none]

## Notes

[Any open questions or negotiation points]
```

Save to `docs/stories/STORY-NNN-[kebab-title].md`.

After saving, tell the user:
```
Story saved. Run story-reviewer on it before adding it to a sprint — you'll catch testability
issues now rather than during implementation.
```

## Integration Points

**`all-aboard`:** When the all-aboard onboarding skill detects that a project has implementation code but no behavioral stories, it should call story-creator to bootstrap story coverage for each major subsystem.

**`rewrite-in-rust` Phase 1:** The behavioral spec output from codebase analysis maps directly to this story format. Each external interface or behavioral contract from the characterization phase becomes a story. Run story-creator during Phase 1 to capture that spec as formal stories before rewriting.

**`tdd-workflow`:** Each story's acceptance criteria become the failing tests in the Red phase. The Gherkin scenarios map to `#[test]` functions or BDD feature files.

**`feature-development`:** Run story-creator at Phase 3 (understand requirements) to produce the formal story before the spec-writing step.

## Writing Style

Apply `natural-writing-style` to story artifacts. Stories should read like they were written by a knowledgeable teammate, not a requirements document generator. The "so that" clause in particular should sound like something a real person actually cares about.

Don't:
- "The system shall process the input in a manner consistent with the requirements."

Do:
- "The scanner agent parses the SARIF file and stores normalized findings — so the dashboard can show current status without manual data entry."

## References

- [Methodology guide](references/methodologies.md) — INVEST, Gherkin, EARS, Agent Stories in depth
- [Security mapping guide](references/security-mapping.md) — STRIDE, SLSA, SCVS, SSDF reference
- [Story templates](assets/story-template.md) — Blank templates by story type
- [Examples](references/examples.md) — Worked examples for human, agent, and system actors
