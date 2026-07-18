---
name: plan
description: Architecture planning with file changes and risks
argument-hint: "<feature-description>"
---

Create an architecture plan for the requested feature or change. Follow this process:

## 1. Understand the Goal

- Clarify the feature or change being requested
- Ask targeted questions if requirements are ambiguous
- Identify success criteria and constraints

## 2. Survey Affected Areas

- Read relevant existing code to understand current architecture
- Identify all files and modules that will be touched
- Map dependencies between affected areas
- Check for existing patterns that should be followed

## 3. Output the Plan

Structure the plan with these sections:

### Requirements
- Bullet list of functional requirements
- Non-functional requirements (performance, security, compatibility)
- Out of scope (explicitly state what this does NOT include)

### Architecture Decisions
For each significant decision:
- **Decision**: What we're doing
- **Rationale**: Why this approach over alternatives
- **Trade-offs**: What we give up
- **Alternatives considered**: Brief mention of rejected approaches

### File Changes
Concrete list of every file that will be created or modified:

| File | Action | Description |
|------|--------|-------------|
| `src/auth/oauth.py` | Create | OAuth2 flow implementation |
| `src/auth/middleware.py` | Modify | Add OAuth token validation |
| `tests/auth/test_oauth.py` | Create | OAuth unit tests |

### Implementation Sequence
Numbered steps in the order work should be done:
1. Step 1 - because [dependency reason]
2. Step 2 - because [builds on step 1]
3. ...

Each step should be independently testable where possible.

### Risks
- Known risks and mitigation strategies
- Dependencies on external systems or teams
- Migration concerns

### Open Questions
- Decisions that need stakeholder input
- Technical unknowns that need investigation
- Scope questions

## 4. Review

Present the plan and ask:
- Does this match your expectations?
- Any constraints I'm missing?
- Should we adjust scope or approach?

Do NOT start implementation until the plan is approved.
