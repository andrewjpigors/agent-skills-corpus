---
name: run-linters
description: Run all linters and type checkers on a Python package. Use when the user wants to lint, type-check, or run static analysis on a Python package or module.
disable-model-invocation: true
argument-hint: "<package>"
arguments: package
allowed-tools:
  - Bash(pip freeze *)
  - Bash(ty check *)
  - Bash(ruff check *)
  - Bash(mypy *)
  - Bash(pyright *)
  - Bash(pylint *)
---

Run all linters and type checkers on `$package`, excluding `tests/`.

**Rules:**
- Run directly in this conversation — do not use agents or subagents.
- Run each tool **one at a time**, in order.
- If a tool exits with errors, **stop immediately** and ask the user whether they want to fix the issues before continuing.

## Pre-execution: check availability

Before running any linter, verify each tool is installed:

```bash
pip freeze | grep -E "^(ty|ruff|mypy|pyright|pylint)=="
```

For any tool that is missing, **stop and inform the user**. Suggest either:
- Installing the missing tools individually (e.g. `pip install ruff mypy`), or
- Installing `core-dev-tools`, which bundles all of them and is the default in the ByteCode Solutions ecosystem.

Only proceed once all five tools are available.

## Steps

1. ```bash
   ty check $package
   ```
2. ```bash
   ruff check $package
   ```
3. ```bash
   mypy --explicit-package-bases $package
   ```
4. ```bash
   pyright $package
   ```
5. ```bash
   pylint $package
   ```

> `tests/` is excluded — test code is not required to comply with linters and type checkers.