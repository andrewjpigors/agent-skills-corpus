---
name: improve-skill
description: >
  Analyze skill execution quality and trigger improvements, onboard an existing skill
  into the improvement pipeline, or log issues/ideas against the skill-improver system
  itself. Use when: the user runs /improve or /improve-skill [name], the user says a
  skill didn't work well or produced wrong results, you notice a skill was corrected or
  deviated during this session, the user asks to review or improve any skill, the user
  asks to onboard/setup a skill for improvement tracking, or the user wants to file a
  bug, feature request, or idea related to how skill improvement works.
  Trigger on: /improve, /improve-skill, "improve skill", "skill didn't work",
  "skill was wrong", "improve all skills", "onboard skill", "setup skill",
  "add skill to improver", "log issue", "add issue", "file a bug", "feature request
  for the improver", natural language friction about skill behavior.
---

# Skill Improver

## Overview

Analyze the current session for skill friction, write a friction log, and spawn the
improvement sub-agent for one or all skills used this session.

## When invoked

- `/improve-skill [name]` — target a specific skill (default: last skill used this session)
- `/improve` — analyze all skills invoked this session
- "log issue / file a bug / add a feature request" — create an issue on the skill-improver's own repo

## Process

### Step 1: Identify target skills

If a skill name was given, use it. Otherwise, review the conversation history and identify
every skill invoked this session — look for Skill tool calls in the transcript. For `/improve`,
process each identified skill. If no skills were invoked this session, tell the user there is
nothing to improve.

### Step 1b: Resolve skill directory

For each skill name, find the actual directory. Check in order:

1. `~/.claude/skills/<skill-name>/SKILL.md` (global)
2. `<project-root>/.claude/skills/<skill-name>/SKILL.md` (project-level, where `<project-root>` is the current working directory or git root)

Use the first match. If neither exists, tell the user the skill was not found and skip it.

Store the resolved **full path** to the skill directory (e.g. `/home/user/.claude/skills/brainstorming`
or `/mnt/DATA/dev/myproject/.claude/skills/time-tracking`). Use this path — referred to as
`<skill-dir>` below — for all subsequent steps.

### Step 2: For each skill — detect friction

Review the conversation for the skill's execution. Look for:

- **Deviation:** Did Claude deviate from what the skill instructed?
- **Correction:** Did the user correct Claude's behavior during the skill?
- **Ambiguity:** Were skill instructions ambiguous — did Claude have to guess?
- **Missed step:** Did a step turn out to be missing?
- **Counterproductive:** Did a step cause problems, waste effort, or lead to wrong outcomes?

**Not friction:** A step that was unnecessary this time but would be needed in other contexts.

### Step 3: Write friction log

If friction was found, write `.friction-log.json` to the skill's directory
(`<skill-dir>/.friction-log.json`):

```json
{
  "timestamp": "<ISO-8601 UTC>",
  "skill": "<skill-name>",
  "friction_points": [
    {
      "type": "<deviation|correction|ambiguity|missed_step|counterproductive>",
      "severity": "<low|medium|high>",
      "description": "<what happened>",
      "context": "<user/session context>"
    }
  ]
}
```

If no friction was found, do not write the file. The sub-agent will do a cold review.

### Step 4: Ensure skill has a GitLab repo

All GitLab operations in this skill use the `glab` CLI (the gitlab-mcp MCP server has
been removed from the setup). The `Bash` tool is sufficient — no `ToolSearch` is needed.

Check if the skill directory is already a git repo:

```bash
git -C <skill-dir> rev-parse --git-dir 2>/dev/null
```

If it **is** a git repo, skip to Step 5.

If it is **not** a git repo:

1. Check whether `claude-code-skills/<skill-name>` already exists on GitLab:

   ```bash
   glab repo view claude-code-skills/<skill-name> --output json
   ```

   `glab` exits non-zero (404) if the project does not exist.

2. If it does not exist, create it as a public repo in the `claude-code-skills` group:

   ```bash
   glab repo create claude-code-skills/<skill-name> --public \
     --description "Claude Code skill: <skill-name>"
   ```

3. Read the SSH clone URL from the create output (or via `glab repo view ... --output json`),
   then initialize and push:

   ```bash
   cd <skill-dir>
   git init
   git remote add origin <ssh-url-from-glab>
   git add SKILL.md
   git commit -m "init: add SKILL.md"
   git push -u origin master
   ```

4. Tell the user the repo was created and the skill is now tracked.

### Step 5: Spawn sub-agent

Determine trigger type and spawn via the dedicated script (which hardcodes
`--allowedTools` for security):

```bash
TRIGGER="explicit"
FRICTION_LOG=""
if [[ -f <skill-dir>/.friction-log.json ]]; then
  TRIGGER="friction"
  FRICTION_LOG=<skill-dir>/.friction-log.json
fi
$HOME/.claude/skills/skill-improver/spawn-improver.sh "<skill-dir>" "$TRIGGER" "$FRICTION_LOG"
```

### Step 6: Notify

Tell the user:

```
Starting improvement analysis for '<skill-name>'...
Check progress: tail -f <skill-dir>/.improvement-log.txt
```

If multiple skills: list each one.

---

## Logging an issue against the skill-improver

When the user wants to file a bug, feature request, or idea related to how skill improvement works (not about a specific skill's content), create an issue directly on the skill-improver's own repo using the `glab` CLI.

For multi-paragraph descriptions, write the body to a temp file and pass it via
`--description-file`. **Never** use single-quoted strings with `\n` — the escape
passes through as the literal two characters and renders verbatim in the issue.

```bash
ISSUE_BODY_FILE=$(mktemp)
# Use the Write tool (or printf) to populate $ISSUE_BODY_FILE with the
# user's description plus any relevant session context.
glab issue create -R claude-code-skills/skill-improver \
  --title "<concise summary>" \
  --description-file "$ISSUE_BODY_FILE"
```

If the installed `glab` build does not support `--description-file`, fall back to
`glab api`:

```bash
glab api -X POST projects/claude-code-skills%2Fskill-improver/issues \
  --field "title=<concise summary>" \
  --field description=@$ISSUE_BODY_FILE
```

Report the issue URL back to the user once created.
