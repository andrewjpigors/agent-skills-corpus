---
name: pre-pr-check
description: Use before opening or updating any MR/PR, before marking work done, or whenever asked to verify a change meets the definition of done. Runs the gate — lint clean, type check clean, tests green, imperative commit messages — plus any project-specific requirements, and reports a clear go/no-go.
---

# Skill: Pre-PR / Definition-of-Done check

The gate that runs **before every MR/PR**. The canonical definition of done lives in
[`AGENTS.md`](../../AGENTS.md) ("Definition of done"); use the exact commands from its
"Common commands" table — never ad-hoc variants.

## Procedure
Run each check in order. Stop and report the first failure with its output; do not "fix and
hide" — surface what failed.

1. **Lint + format** — run the project's lint command. Must be clean.
2. **Type check** — run the project's type-check command. Must be clean.
3. **Tests** — run the test command. All green. New functionality must ship with tests;
   if a change adds behavior without tests, that is a **no-go**.
4. **Commit messages** — imperative mood, short and descriptive, in English
   (e.g. "Add order repository", not "added repo" / "fixes stuff").
5. **Project-specific requirements** — whatever is listed as item 5 of the definition of
   done in `AGENTS.md` (e.g. changelog entry, issue update, migration file).
6. **No secrets** — no `.env` values, tokens, or hard-coded credentials in the diff.
7. **Dependencies recorded** — any new dependency is added via the package manager, not
   pasted in by hand.

## Output
A short checklist with ✅/❌ per item, each failure quoting the actual command output, and a
final **GO** or **NO-GO** verdict. On NO-GO, list exactly what must change before the MR/PR.

## Notes
- This skill verifies; it does not implement fixes. Failing tests/lint are routed back to the
  implementer (or the `test-engineer` / `refactorer` roles).
- Pair with **[`open-issue-branch`](../open-issue-branch/SKILL.md)** — this is its Step 2 gate.
- The optional CI gate (`.gitlab-ci.yml` / `.github/workflows/dod.yml`) runs the same
  lint/typecheck/test commands server-side on the MR/PR — one gate, enforced twice.
