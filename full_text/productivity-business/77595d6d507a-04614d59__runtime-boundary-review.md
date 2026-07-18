---
name: runtime-boundary-review
description: Use when code crosses web, admin, extension, desktop, mobile, worker, server, storage, or bridge/runtime boundaries.
---

# Runtime Boundary Review

Use when behavior crosses runtimes or platform layers.

## Workflow

1. Identify each runtime involved.
2. Verify import direction and package boundaries.
3. Confirm data crossing the boundary is serializable and validated.
4. Keep bridge layers thin and business logic in shared modules.
5. Verify cleanup for timers, subscriptions, sockets, reconnects, and pending
   requests.
6. Run the app-specific quality gate for every affected runtime.

