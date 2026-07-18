---
name: skill-creation
description: Lifecycle skill for creating new Claude Code skills — ensures every new skill gets a GitLab repo, initial commit, and proper directory structure. Use AFTER drafting a skill (via the skill-creator plugin or manually) to finalize it. Triggers on "make a skill", "create a skill", "new skill", "turn this into a skill", or whenever a SKILL.md has been written to a skills directory but not yet committed to GitLab. This skill handles the infrastructure side — the skill-creator plugin handles the content side.
---

# Skill Creation Lifecycle

This skill ensures every new skill gets properly committed to a GitLab repo under the `claude-code-skills` namespace. It complements the skill-creator plugin (which focuses on writing good skill content) by handling the infrastructure and version control side.

## When This Applies

After a SKILL.md has been written (by you, the skill-creator plugin, or the user), this skill ensures it doesn't just sit as an uncommitted file. Every skill should be a tracked git repo so the skill-improver can manage it.

## Process

### Step 1: Verify the Skill Directory

Confirm the skill has been written to the correct location:

- **Project-specific skills:** `<project-root>/.claude/skills/<skill-name>/SKILL.md`
- **Global skills:** `~/.claude/skills/<skill-name>/SKILL.md`

The choice depends on whether the skill is specific to one project or useful across all projects.

### Step 2: Check If Already Tracked

```bash
git -C <skill-dir> rev-parse --git-dir 2>/dev/null
```

If it's already a git repo, the skill is already tracked — skip to Step 5 (verify remote is correct).

### Step 3: Create GitLab Repo

Use `mcp__gitlab-mcp__browse_projects` to check if `claude-code-skills/<skill-name>` already exists.

If not, create it. **Visibility depends on scope:**
- **Project-specific skills** (live under a project's `.claude/skills/`) → `private`
- **Generic/reusable skills** (live under `~/.claude/skills/`) → `public`

```
mcp__gitlab-mcp__manage_project:
  action: create
  name: <skill-name>
  namespace: claude-code-skills
  description: <one-line description from SKILL.md frontmatter>
  visibility: private  # or public for generic skills
```

### Step 4: Initialize and Push

```bash
cd <skill-dir>
git init
git remote add origin git@gitlab.com:claude-code-skills/<skill-name>.git
git add SKILL.md
# Add any bundled resources too
git add scripts/ references/ assets/ 2>/dev/null
git commit -m "init: add SKILL.md"
git push -u origin master
```

### Step 5: Verify

Confirm the push succeeded and the repo is accessible. Report the GitLab URL to the user.

### Step 6: Add .gitignore (if needed)

If the skill directory contains files that shouldn't be tracked (friction logs, temporary files), create a `.gitignore`:

```
.friction-log.json
.improvement-log.txt
.fuse_hidden*
.worktrees/
```

Commit and push it.

### Step 7: Add CI pipeline

Every skill repo must have a `.gitlab-ci.yml` that runs its tests before merge. If a `tests/` directory exists with a `run_tests.sh`, add:

```yaml
stages:
  - test

test:
  stage: test
  image: python:3.11-slim
  before_script:
    - apt-get update -qq && apt-get install -y -qq git jq curl >/dev/null 2>&1
  script:
    - bash tests/run_tests.sh
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

If no tests exist yet, add a placeholder `tests/run_tests.sh` that exits 0 so CI can pass, and note in the issue that tests need to be written:

```bash
#!/usr/bin/env bash
echo "No tests yet — add tests/test_*.sh files"
exit 0
```

Without CI, there is no enforcement that tests pass before merge. This step is required.

Commit and push `.gitlab-ci.yml` (and the placeholder test runner if needed).

## Skills with Hooks/Scripts

Some skills bundle hooks and scripts (e.g. `time-tracking` v2 ships
`hooks/session-end.sh` and `scripts/time-track.py`). Prefer hooks/scripts that
resolve their own location (`${CLAUDE_PLUGIN_ROOT}` when installed as a plugin,
falling back to a path relative to the hook file itself) — then nothing needs
copying into consumer projects at all. If a host project must reference a
skill's files directly, **use symlinks** rather than copying files:

```bash
# In the host project root:
ln -sf ../.claude/skills/<skill-name>/hooks/<hook>.sh     .claude/hooks/<hook>.sh
ln -sf ../.claude/skills/<skill-name>/scripts/<script>    .claude/scripts/<script>
```

Then add to the host project's `.gitignore`:

```
# Skill repo .git directories (skills are cloned repos, their .git is not ours)
.claude/skills/*/.git
```

This keeps `settings.json` pointing at stable `.claude/hooks/` paths while updates flow automatically from a `git pull` inside the skill directory. Never point `settings.json` directly into the skill repo — hook paths should always be stable project-level paths.

## Checklist

Before considering the skill fully created, verify:

- [ ] SKILL.md exists with valid frontmatter (name + description)
- [ ] Skill directory is a git repo
- [ ] Remote points to `git@gitlab.com:claude-code-skills/<skill-name>.git`
- [ ] Initial commit pushed to GitLab
- [ ] `.gitlab-ci.yml` exists and runs `tests/run_tests.sh` on MRs and master
- [ ] If skill has hooks/scripts: symlinks created in host project, `.git` gitignored
- [ ] Skill appears in Claude's available skills list (check the system reminder)

## Outstanding Skills (to onboard)

These skills exist locally but are not yet proper `claude-code-skills/` repo clones. Onboard each using the process above when ready.

| Skill | Location | Status | Notes |
|-------|----------|--------|-------|
| `mcn-after-dark-event` | `~/.claude/skills/mcn-after-dark-event/` | Not a git repo, no GitLab repo | Project-specific; onboard when needed |
| `gitlab-mcp-server` | `/mnt/DATA/dev/arenaams/.claude/skills/gitlab-mcp-server/` | Tracked in arenaams, no GitLab repo | Generic — needs its own `claude-code-skills/gitlab-mcp-server` repo |
| `e2e-testing` | `/mnt/DATA/dev/arenaams/.claude/skills/e2e-testing/` | Tracked in arenaams, no GitLab repo | Currently arenaams-specific; generic version to be created later |

## Relationship to Other Tools

- **skill-creator plugin** — Writes the skill content (SKILL.md). Use it first for drafting, testing, and iterating on skill quality.
- **skill-improver** — Monitors skill execution and spawns improvement agents. Expects skills to be git repos (which this skill ensures).
- **This skill** — Bridges the gap: after content is written, this handles the git/GitLab lifecycle.
