---
name: deep-qa
description: Use for exhaustive browser QA on high-risk flows - deposits / withdrawals, balance changes, settlement, claims, KYC / AML, RG, admin actions, permission boundaries, and large UI changes.
---

# Deep QA

Use when a change is too risky for a spot check.

## Workflow

1. Build a scenario matrix before testing: happy path, blocked path, loading,
   error, empty, permission-denied, mobile, desktop, refresh/retry, and recovery.
2. Use the repo's browser tooling when available.
3. Test user client and admin dashboard boundaries separately.
4. Verify that failed or blocked user actions produce explicit feedback.
5. For casino-sensitive flows, include idempotency/retry behavior, audit trail
   expectations, and compliance copy verification.
6. Fix verified frontend defects if the task scope allows it, then rerun the
   scenario.

Report tested scenarios, failures found, fixes made, and remaining unverified
coverage.

