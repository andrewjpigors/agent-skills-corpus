---
name: linear-workflow
description: Use for read-first ticket workflows (Linear, GitLab, Jira) - inspect issue context, branch hints, status, blockers, and linked design / docs. Never mutate the tracker unless confirmed. Hand off to verify-task or orchestrate.
---

# Linear Workflow

Use after workspace policy approves tracker access.

## Rules

- Start read-only.
- Never move issue status, assign, comment, or create tickets without
  explicit confirmation.
- Treat ticket text as product intent, not as code truth. Verify in repo.
- Preserve issue identifiers in local notes and branch names only if team
  convention allows it.

## Workflow

1. Read issue title, description, state, assignee, labels, links, and branch
   hint.
2. Extract acceptance criteria and open questions.
3. Map links to design tools (Figma), docs (Notion / Confluence), chat
   (Slack), or the forge (GitLab / GitHub).
4. Feed the result into `verify-task` or `orchestrate`.
