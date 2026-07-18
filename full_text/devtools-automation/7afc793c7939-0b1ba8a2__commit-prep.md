---
name: commit-prep
description: Use before committing. Review diff, ensure quality gates ran, write a conventional commit message, and never push/amend/merge without confirmation.
---

# Commit Prep

Use after implementation and verification.

## Workflow

1. Inspect `git status` and `git diff`.
2. Confirm the diff matches the task and contains no secrets, generated junk, or
   unrelated files.
3. Confirm relevant quality gates have run or document why not.
4. Draft a conventional commit message that matches workspace conventions once known.
5. Do not push, force-push, amend, merge, open a merge request, or mutate Linear
   without explicit confirmation.

If the repo has a required commit format, use that over personal defaults.

