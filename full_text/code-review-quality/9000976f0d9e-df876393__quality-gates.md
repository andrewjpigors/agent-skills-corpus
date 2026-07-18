---
name: quality-gates
description: Use before claiming completion. Detect workspace monorepo tooling (pnpm / npm / yarn, Turbo, Nx) and run scoped lint, typecheck, tests, build, or generated-client checks for changed packages.
---

# Quality Gates

Run this before final completion on code changes.

## Workflow

1. Inspect lockfiles and workspace config to identify pnpm / yarn / npm,
   Turbo, Nx, or custom scripts.
2. Inspect changed files and map them to apps / packages / services.
3. Prefer repo scripts and CI-required commands.
4. Scope checks to changed packages / apps if the workspace tool supports
   it (`pnpm --filter=<pkg>`, `turbo run lint --filter=<pkg>`, `nx affected`).
5. Check `package.json` BEFORE running a script - not every service in a
   monorepo declares every script (some have no `lint`, some have a
   custom `test:e2e`).
6. If generated clients or schemas changed, run the repo regeneration /
   check command.
7. Report exact commands, pass/fail status, and skipped checks with
   reason.

## Per-package caveats

Forks often have idiosyncratic packages - one where `lint` silently
autofixes legacy code, one where `test` actually runs against a
container, one without typecheck. Document these in the fork's
`AGENTS.md` so the agent picks the right command on the first try.

## Never

- Never invent a command if the repo already documents one.
- Never run a workspace-wide lint without filtering when one of the
  packages has a known autofix hazard (the fork's
  `block-dangerous-flags` hook should catch this, but the rule lives
  here too).
