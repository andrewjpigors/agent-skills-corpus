---
name: skill-skill-writer
description: >
  Create new skill files following the agent-skills standard format.
  Trigger when asked to create, write, or bootstrap a new skill, or when
  a repeatable task needs to be formalized into a reusable skill file.
---

# Skill: Skill Writer

Creates well-structured skill files following the agent-skills standard format. This is the meta-skill — use it to bootstrap new skills that are self-contained, well-documented, and follow project conventions.

## When to Use

- The user asks to create a new skill
- The user describes a repeatable task that should be captured as a reusable skill
- An existing workflow needs to be formalized into a skill file

## Prerequisites

- Access to the `agent-skills` repository (or a project using its conventions)
- The skill format spec at `skills/README.md` for reference

## Instructions

1. **Determine the skill's purpose.** If the user hasn't fully described it, ask:
   - What task does this skill perform?
   - What input does it need? What output does it produce?
   - Are there any tools, languages, or frameworks involved?

2. **Choose a name.** Use `lowercase-kebab-case`. The name should be:
   - Descriptive: `api-endpoint-writer` not `writer`
   - Action-oriented: prefer verbs or verb-noun pairs
   - Unique within the `skills/` directory

3. **Create the directory and file:**
   ```
   skills/skill-<skill-name>/SKILL.md
   ```

4. **Write the skill file** using the template below. Every section is required unless marked optional.

5. **Validate the skill:**
   - Read it cold — could someone follow these instructions without any other context?
   - Check that the example is concrete and realistic
   - Verify file paths and commands are correct
   - Ensure no external dependencies are assumed without being listed in Prerequisites

6. **Announce the result** to the user with the file path and a brief summary.

## Template

```markdown
---
name: skill-<skill-name>
description: >
  Brief description of what this skill does and when to trigger it.
  Include keywords that help tools match this skill to user requests.
---

# Skill: <Skill Name>

<One paragraph: what this skill does, who it's for, and why it exists.>

## When to Use

- <Specific trigger or situation>
- <Another trigger>

## Prerequisites

- <Tool, file, or context required>
- <Or "None" if truly standalone>

## Instructions

1. <First concrete step>
2. <Second step>
3. <Continue with numbered steps for the workflow>
   - Include decision branches: "If X, do Y. Otherwise, do Z."
   - Reference specific file paths, commands, or formats
4. <Final step>

## Output Format

- <What files are created, and where>
- <Structure or format of the output>
- <Any naming conventions>

## Examples

### Example: <Brief description>

**Input:** <What the user provides or requests>

**Result:**

<Show the actual output — file contents, terminal output, etc.>

## Constraints

- <Things this skill should never do>
- <Boundaries and safety rails>
```

## Output Format

- Creates `skills/skill-<skill-name>/SKILL.md`
- File follows the template above with all required sections populated
- Content is self-contained and tool-agnostic

## Examples

### Example: Creating a "git-commit-message" skill

**Input:** "Create a skill for writing conventional commit messages"

**Result:** Creates `skills/skill-git-commit-message/SKILL.md` with:
- Description of conventional commits format
- Instructions for analyzing staged changes
- Template for generating the commit message
- Examples showing real diffs mapped to commit messages
- Constraints: don't amend without permission, don't push

## Constraints

- Only create files under `skills/` — directory names must be prefixed with `skill-`
- Never overwrite an existing skill without user confirmation
- Always include at least one concrete example — no placeholder text
- Keep skills tool-agnostic unless the skill is inherently tool-specific
