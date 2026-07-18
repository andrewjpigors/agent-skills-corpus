---
name: project-qa
description: Use for browser QA scoped to the current diff. Spot-check changed user/admin flows, responsive states, loading/error/empty states, and risky casino behavior.
---

# Project QA

Use this for a focused browser QA pass after implementation.

## Workflow

1. Identify user-visible flows touched by the diff.
2. Start the documented dev server only if needed.
3. Test happy path plus loading, error, empty, disabled, and responsive states.
4. For admin flows, verify permission-sensitive UI does not imply authorization.
5. For casino flows, verify balances, payment-like actions, responsible gambling,
   and compliance copy are not silently altered.
6. Capture exact blockers when a scenario cannot be verified.

Report scenarios tested, results, and remaining risk.

