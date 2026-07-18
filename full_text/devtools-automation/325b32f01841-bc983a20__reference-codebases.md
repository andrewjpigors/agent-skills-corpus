---
name: reference-codebases
description: Use when a workspace-local reference catalog exists and the task needs read-only comparison against approved sibling repos or packages.
---

# Reference Codebases

Use only for workspace-approved local references.

## Rules

- Read the local reference catalog first, typically in `local/repo-map.md` or a
  workspace-local `.cursor/references/codebases.md`.
- Pull or inspect references read-only.
- Do not repair reference repo git state unless asked.
- Bring conclusions back to the current repo and implement using current repo
  conventions.
- Do not use prior workplace repos as references for the workspace.

## Workflow

1. Resolve reference path from the catalog.
2. Read that repo's own guidance.
3. Search only for the pattern/API needed.
4. Summarize inputs, outputs, edge cases, and local adaptation notes.

