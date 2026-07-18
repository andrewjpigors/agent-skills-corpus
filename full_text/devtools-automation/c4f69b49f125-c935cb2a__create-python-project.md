---
name: create-python-project
description: Scaffold a new Python project from the ByteCode Solutions blueprint template. Use when the user wants to create, initialize, bootstrap, or start a new Python project.
disable-model-invocation: true
argument-hint: "[project-name]"
allowed-tools:
  - Bash(git clone *)
  - Bash(mv *)
---

Scaffold a new Python project from the ByteCode Solutions blueprint template.

## Steps

1. Determine the project name:
   - If `$ARGUMENTS` is provided, use it as the directory name.
   - Otherwise, ask the user for a project name.

2. Ask the user for the target parent directory. Default to the current working directory if not specified.

3. Clone the blueprint template:
   ```bash
   git clone https://gitlab.com/bytecode-solutions/templates/blueprint-python.git <project-name>
   ```

4. Confirm success and show the resulting directory structure.