---
name: start-project
description: Use to create a local, gitignored project-memory skill for a long workspace task so future sessions preserve context without committing private notes.
---

# Start Project

Create local project memory for a long-running task.

## Workflow

1. Resolve repo root with `git rev-parse --show-toplevel`.
2. Pick a short kebab-case slug.
3. Create `.cursor/skills/project-<slug>/SKILL.md`.
4. Ensure `.cursor/skills/project-*/` is gitignored before writing.
5. Do not overwrite an existing project memory without confirmation.
6. Capture scope, branch, affected paths, mental model, decisions, open
   questions, dead ends, commands, links, and casino-policy unknowns.
7. Update the memory before final response whenever the task context changes.

Project memory is local-only and disposable. Harvest durable lessons into this
private harness only after the task ships.

