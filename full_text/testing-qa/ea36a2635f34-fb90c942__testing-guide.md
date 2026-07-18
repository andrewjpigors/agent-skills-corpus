---
name: testing-guide
description: Use when deciding what tests to write or run for a change - unit, integration, API, browser E2E, mutation, regression. Match the test type to the risk surface (money, auth, idempotency, race conditions, UI).
---

# Testing Guide

Choose tests by risk.

- Pure mapper/helper logic: unit tests for boundary values and unknown variants.
- Query/mutation behavior: integration tests around cache, invalidation, rollback,
  and error paths.
- Forms: validation, blocked submit feedback, and successful submit.
- UI flows: browser tests for user-visible behavior and responsive states.
- Admin or permission flows: test authorized, unauthorized, and hidden-control
  cases.
- Payment-like or casino-sensitive flows: test idempotency assumptions, disabled
  states, and recovery paths with approved fixtures.

Prefer existing repo test utilities and commands. Do not add a new framework
unless explicitly scoped.

