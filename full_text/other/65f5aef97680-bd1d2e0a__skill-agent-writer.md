---
name: skill-agent-writer
description: >
  Create new agent definition files following the agent-skills standard format.
  Trigger when asked to create, write, or define a new agent, or when a
  recurring role or specialty needs to be formalized as a reusable agent persona.
---

# Skill: Agent Writer

Creates well-structured agent definition files following the agent-skills standard format. Use this skill to define specialized agent personas with clear capabilities, boundaries, and skill dependencies.

## When to Use

- The user asks to create a new agent
- A recurring role or specialty needs to be formalized as a reusable agent definition
- An existing workflow requires a dedicated agent persona with specific constraints

## Prerequisites

- Access to the `agent-skills` repository (or a project using its conventions)
- The agent format spec at `agents/README.md` for reference
- Knowledge of any skills the agent will depend on

## Instructions

1. **Determine the agent's role.** If the user hasn't fully described it, ask:
   - What is this agent's specialty?
   - What tasks will it handle?
   - What skills (if any) should it use?
   - What should it explicitly NOT do?

2. **Choose a name.** Use `lowercase-kebab-case` with an `agent-` prefix. The name should be:
   - Role-oriented: `agent-code-reviewer` not `agent-reviewer`
   - Specific: `agent-python-test-writer` not `agent-test-writer` (unless it's truly language-agnostic)
   - Unique within the `agents/` directory

3. **Identify skill dependencies.** Check `skills/` for existing skills the agent should use. List them with relative paths. If the agent needs a skill that doesn't exist yet, note it — the user may want to create it first.

4. **Create the directory and file:**
   ```
   agents/agent-<agent-name>/agent.md
   ```

5. **Write the agent file** using the template below. Every section is required.

6. **Validate the agent definition:**
   - Are the capabilities specific and testable?
   - Are the constraints clear hard boundaries (not vague suggestions)?
   - Do the skill references point to real files?
   - Could another developer read this and understand exactly what the agent does?

7. **Announce the result** to the user with the file path and a summary of the agent's role.

## Template

```markdown
# Agent: <Agent Name>

<One paragraph: this agent's role, expertise, and when to invoke it.>

## Capabilities

What this agent can do:
- <Specific capability>
- <Another capability>
- <Be concrete — "analyzes Python test files" not "understands testing">

## Skills

Skills this agent uses:
- `skills/skill-<skill-name>/skill.md` — <when/how it uses this skill>

## Tools

Tools and commands this agent should use:
- <Tool or command> — <what for>
- <Or "Standard file read/write tools" if nothing special>

## Instructions

<How the agent behaves when invoked:>

1. <What it does first — gather context, read files, ask questions>
2. <Its main workflow>
3. <How it handles ambiguity or edge cases>
4. <How it reports results>

## Constraints

Hard boundaries:
- <Files/directories it must not modify>
- <Actions requiring user confirmation>
- <Scope limits — what's explicitly out of bounds>
- <Safety rails — things it should never do>
```

## Output Format

- Creates `agents/agent-<agent-name>/agent.md`
- File follows the template above with all required sections populated
- Skill references use relative paths from the repo root
- Agent definition is focused on a single specialty

## Examples

### Example: Creating a "code-reviewer" agent

**Input:** "Create an agent that reviews pull requests for code quality"

**Result:** Creates `agents/agent-code-reviewer/agent.md` with:
- Capabilities: reads diffs, checks style, identifies bugs, suggests improvements
- Skills: references `skills/skill-git-commit-message/skill.md` if it exists
- Instructions: read the diff, check for common issues, provide structured feedback
- Constraints: never pushes code, never approves without listing findings, stays within the diff scope

## Constraints

- Only create files under `agents/` — directory names must be prefixed with `agent-`
- Never overwrite an existing agent without user confirmation
- Every agent must have at least one constraint defined — unbounded agents are dangerous
- Skill references must point to skills that exist (or are being created in the same session)
- Keep agent scope narrow — if an agent does too many things, it should be split
