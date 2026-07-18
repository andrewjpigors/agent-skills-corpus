---
name: run-security
description: Run security vulnerability checks on a Python package or project. Use when the user wants to audit code for security issues or check dependencies for known CVEs.
disable-model-invocation: true
argument-hint: "<package>"
arguments: package
allowed-tools:
  - Bash(pip freeze *)
  - Bash(bandit *)
  - Bash(pip-audit *)
---

Run security vulnerability checks on `$package` using `bandit` (static analysis) and `pip-audit` (dependency CVEs).

**Rules:**
- Run directly in this conversation — do not use agents or subagents.
- Run each tool **one at a time**, in order.
- If a tool exits with findings, **stop immediately** and ask the user whether they want to address the issues before continuing.

## Pre-execution: check availability

Before running any tool, verify each is installed:

```bash
pip freeze | grep -E "^(bandit|pip-audit)=="
```

For any tool that is missing, **stop and inform the user**. Suggest either:
- Installing the missing tools individually (e.g. `pip install bandit pip-audit`), or
- Installing `core-dev-tools`, which bundles all of them and is the default in the ecosystem.

Only proceed once both tools are available.

## Steps

1. ```bash
   bandit -r $package
   ```
2. ```bash
   pip-audit
   ```

> `bandit` scans `$package` for insecure code patterns. `pip-audit` scans the entire environment's installed dependencies for known CVEs — no package argument is needed.