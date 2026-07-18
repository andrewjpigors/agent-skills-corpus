---
name: review-tests
description: Systematic review of test code for gaps, weak assertions, cheating or circular tests, and end-to-end data independence. Use when you want a prioritized list of test issues for specific files or directories (even outside Git), focused on correctness and meaningful coverage.
---

# Review Tests

## Overview
Provide a rigorous, test-only review that surfaces gaps, edge cases, circular/cheating patterns, and missing end-to-end coverage using independent data.

## Workflow

1. Confirm scope
- If the user provided file or directory paths, use exactly those.
- If the user gave a root path, search for test files inside it.
- If scope is missing or ambiguous, ask for explicit paths.
- Do not require a Git repo.

2. Gather test files
- Use fast search (`rg --files`) within the provided scope.
- Include common test patterns: `tests/`, `test_*.py`, `*_test.*`, `*.spec.*`, `__tests__`, `spec/`.
- If the user provided explicit files, do not add unrelated tests unless asked.

3. Identify code under test
- From each test, list the production modules, functions, and helpers it exercises.
- Locate the production sources with `rg` or path inspection.
- Keep a map of test -> production code referenced.

4. Cheating / circular test checks
- Flag tests that compute expected outputs using the same production logic under test.
- Flag tests that import production helpers to build expected values unless:
  - The helper does not overlap with the behavior under test, AND
  - That helper is independently tested elsewhere.
- To confirm independent coverage, search for tests targeting the helper module/function.
- If independent coverage is missing or unclear, report it as an issue.

5. Coverage gaps and weak assertions
- Check boundary values, malformed inputs, and error paths.
- Ensure assertions validate meaningful outcomes, not just "no error."
- Flag over-mocking that bypasses core logic.
- Note nondeterminism: time, randomness, filesystem, network dependencies without controls.

6. End-to-end tests
- Verify E2E tests use independent comparison data.
- If data is produced by production code, require a clear reason; otherwise flag it.
- Identify missing E2E scenarios for critical workflows and suggest concrete cases.

7. Output requirements
- Provide a prioritized, actionable list of findings.
- Each finding includes `Severity`, `File:Line`, `Problem`, `Suggestion`.
- Do not modify files.
- If information is missing, ask focused follow-up questions.
