---
name: wire-mock-to-api
description: Use when replacing mock / static UI data with real API hooks, generated types from a generated-clients package, or verified backend data.
---

# Wire Mock To API

Use when a screen currently depends on mock/static data.

## Workflow

1. Locate the mock source and every consumer.
2. Identify the real endpoint, generated type, query hook, or backend contract.
3. Verify the endpoint shape before mapping.
4. Create or reuse pure API-to-domain mappers.
5. Render query state with the repo's query-state pattern.
6. Define invalidation/refetch behavior for mutations.
7. Remove stale mocks only when no consumer remains.

For domain-sensitive values (balances, bonuses, wagering, payments, KYC), do not infer semantics.
Verify the contract or ask.

