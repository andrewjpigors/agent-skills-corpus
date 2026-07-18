---
name: fix-ci
description: Use to diagnose and repair failing GitLab CI or local check failures on the current branch without bundling unrelated work.
---

# Fix CI

Use for failed GitLab pipelines or local quality gates.

## Workflow

1. Identify the failing job from GitLab UI, `glab`, or pipeline logs.
2. Read the failing command and logs. Do not guess from the job name alone.
3. Reproduce locally when practical with the smallest equivalent command.
4. Fix only the real failure.
5. Run the mapped local check or explain why it is CI-only.
6. Stage only CI-fix paths.
7. Do not push, retry pipelines, or mutate merge requests without confirmation
   during the first-month safety period.

Stop after two unclear fix cycles and report the blocker.

