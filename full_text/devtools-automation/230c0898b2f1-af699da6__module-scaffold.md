---
name: module-scaffold
description: Use when creating a new frontend feature module. Follow existing monorepo layout, core/types conventions, data hooks, mappers, and feature-organized UI.
---

# Module Scaffold

Use when adding a new feature module.

## Workflow

1. Inspect nearby modules before creating structure.
2. Follow the repo's feature organization. Avoid generic `components/`, `hooks/`,
   or `utils/` folders unless the repo already uses them there.
3. Keep runtime constants and derived unions in `core.ts` when that convention
   exists.
4. Keep pure type definitions in `types.ts`.
5. Place API/query hooks and pure mappers under the repo's data convention.
6. Export through existing barrel patterns only if the repo uses them.
7. Add focused tests or stories when the feature surface warrants it.

Do not introduce a new module pattern when an existing one is visible.

