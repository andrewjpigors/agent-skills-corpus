---
name: run-coverage
description: Run test coverage for the current project. Use when the user wants to check, measure, or report test coverage.
disable-model-invocation: true
allowed-tools:
  - Bash(pip freeze *)
  - Bash(python manager.py *)
  - Bash(find tests *)
  - Bash(pytest *)
---

Run test coverage directly in this conversation — do not use agents or subagents.

**Functional tests must never be executed.**

## Steps

1. Check whether `core-tests` is installed and `manager.py` exists:
   ```bash
   pip freeze | grep -E "^core-tests=="
   ```

2. **If both conditions are met**, run:
   ```bash
   python manager.py run-coverage
   ```

3. **Otherwise**, check if `pytest` and `pytest-cov` are available and use them
   as a fallback:

   a. Inspect the test directory structure to determine the file naming convention:
      ```bash
      find tests -name "*.py" ! -name "__init__.py" | head -10
      ```
      Collect all distinct filename prefixes/suffixes (e.g. `test_*.py`, `tests_*.py`,
      `*_test.py`) that are actually present.

   b. Build the `--override-ini` flag to match every pattern found, then run:
      ```bash
      pytest tests/unit tests/integration --cov --cov-report=term-missing \
        --override-ini="python_files=<patterns>"
      ```
      Example for a repo using both conventions:
      ```bash
      pytest tests/unit tests/integration --cov --cov-report=term-missing \
        --override-ini="python_files=tests_*.py test_*.py"
      ```

   c. After a successful run, persist the discovered pattern in the project's
      `CLAUDE.md` so future invocations skip the inspection step. Add a section:

      ```markdown
      ## Test conventions
      Test files follow the `tests_*.py` naming pattern (or whichever was found).
      Use `pytest tests/unit tests/integration --cov --cov-report=term-missing --override-ini="python_files=<patterns>"`
      when running coverage without `manager.py`.
      ```

      On subsequent runs, read `CLAUDE.md` first — if the pattern is already
      recorded there, skip step 3a and use it directly.

4. If neither `core-tests` nor `pytest`/`pytest-cov` is available, stop and
   advise the user to install `core-tests` (the default in the ByteCode
   Solutions ecosystem) or `pytest` with `pytest-cov`.

## Reporting

After a successful run, parse the coverage output and report to the user:

- The **total coverage %** of the project.
- Any modules below **100 %** coverage, listed with their individual percentage.

If coverage is not 100 %, ask the user whether they want to achieve 100 % coverage.
If yes, create one task per file below 100 % using the TaskCreate tool, then work
through them one by one:
- Write or fix tests until that module reaches 100 %.
- Re-run coverage for that module to verify:
  ```bash
  pytest tests/unit tests/integration --cov=<module> --cov-report=term-missing \
    --override-ini="python_files=<patterns>"
  ```
- Mark the task complete, then move to the next.

## On failure

If any tests fail during the coverage run, invoke the `/run-tests` skill
immediately — it handles failure identification, user confirmation, per-test
task creation, and iterative fixing.