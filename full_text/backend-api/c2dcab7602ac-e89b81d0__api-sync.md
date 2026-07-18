---
name: api-sync
description: Use when syncing frontend API clients or generated types with backend contracts. Regenerate from the source contract and repair call sites.
---

# API Sync

Use when backend contracts, generated clients, or API mappers change.

## Workflow

1. Identify the source contract and generation command from repo docs/scripts.
2. Regenerate clients/types with the repo command.
3. Repair TypeScript errors without casting API shapes into desired domain types.
4. Keep API-to-domain mappers pure and exhaustive for external discriminants.
5. Update query keys, invalidation, and error handling where endpoint behavior
   changed.
6. Run scoped quality gates for affected apps/packages.

Do not hand-edit generated files unless the repo explicitly permits it.

