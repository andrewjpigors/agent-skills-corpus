---
name: real-browser-qa
description: Use when built-in browser QA is insufficient and policy allows real Chrome/Playwright testing for auth sessions, extensions, or Chrome-specific behavior.
---

# Real Browser QA

Use only after workspace policy allows browser automation on the target environment.

## Workflow

1. Prefer the repo's documented Playwright setup.
2. Use incremental observe -> act -> verify steps. Avoid monolithic scripts with
   hardcoded sleeps.
3. Reuse signed-in sessions only when policy allows it and the account is safe
   for testing.
4. Never pass credentials, seed phrases, payment data, or private documents in
   prompts or command arguments.
5. Save only screenshots needed for verification.
6. Clean up browser state if the test created risky local state.

Report exact URLs/environments, scenarios, screenshots, and unverified blockers.

