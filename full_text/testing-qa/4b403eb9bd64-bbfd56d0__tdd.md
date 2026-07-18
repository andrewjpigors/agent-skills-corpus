---
name: tdd
description: Test-driven development with red-green-refactor cycle
argument-hint: "<feature-description>"
---

Implement the requested feature using test-driven development (TDD). Follow the red-green-refactor cycle strictly.

## 1. Understand the Feature

- Clarify what needs to be built
- Identify acceptance criteria
- Determine the testing framework (pytest, vitest, jest, etc.)
- Find existing test patterns in the codebase

## 2. Red Phase - Write Failing Tests

Write tests FIRST, before any implementation:

- Start with the simplest test case (happy path)
- One test at a time
- Tests must be runnable and must FAIL
- Test names describe expected behavior: `test_<what>_when_<condition>_then_<result>`

Run the tests to confirm they fail. Show the failure output.

## 3. Green Phase - Minimal Implementation

Write the MINIMUM code to make the failing test pass:

- Don't write more than what's needed for the current test
- Don't optimize or clean up yet
- Don't handle edge cases that aren't tested yet
- The goal is to go from red to green as fast as possible

Run the tests to confirm they pass. Show the output.

## 4. Refactor Phase

Now improve the code while keeping tests green:

- Remove duplication
- Improve naming
- Extract functions if needed
- Simplify logic

Run tests after each refactoring step to confirm nothing breaks.

## 5. Iterate

Repeat the cycle for each new behavior:

1. Add the next test (edge case, error condition, etc.)
2. Watch it fail (red)
3. Make it pass (green)
4. Refactor
5. Confirm all tests still pass

Suggested test progression:
1. Happy path (simplest valid input)
2. Boundary values (empty input, zero, max values)
3. Error conditions (invalid input, missing data)
4. Edge cases (unicode, concurrent access, large data)

## 6. Summary

After all cycles, show:
- Total tests written
- All test names and what they verify
- Final implementation
- Coverage of acceptance criteria
- Any remaining edge cases not yet covered

## Rules

- NEVER write implementation before the test
- NEVER skip running the tests between phases
- NEVER write multiple tests at once (one at a time)
- Show the test output at each phase transition
- If a refactoring breaks a test, revert and try a smaller refactoring
