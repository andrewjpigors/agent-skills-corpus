---
name: resolve-pr-comments
description: Use to triage and address GitLab merge request review comments, including AI-review comments, while validating every claim before changing code.
---

# Resolve Review Comments

Use for unresolved merge request comments.

## Workflow

1. Fetch unresolved discussions through GitLab UI, `glab`, or API.
2. Classify comments as human, automated, or mixed.
3. Verify every claim against actual code and behavior.
4. Fix real correctness, security, typing, test, or behavior issues.
5. Skip speculative style churn and large refactors disguised as review comments.
6. Ask before dismissing human or mixed comments that involve product judgment.
7. Run relevant checks.
8. Do not resolve human/mixed threads or push without confirmation until workspace
   norms are learned.

AI labels are claims, not facts.

