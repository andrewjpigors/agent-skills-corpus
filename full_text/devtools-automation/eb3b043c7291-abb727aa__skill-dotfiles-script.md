---
name: skill-dotfiles-script
description: >
  Create new scripts following dotfiles conventions — bash, Python, or C/crispy.
  Trigger when adding scripts to dotfiles, creating CLI tools, or writing
  utility scripts with proper argument parsing, license headers, and help output.
---

# Skill: Dotfiles Script Generator

Generates scripts that follow the exact conventions of an established dotfiles repository. Supports three script types: bash (primary), Python, and C/crispy. All scripts include AGPLv3 license headers, proper argument parsing, help/license output, and error handling.

## When to Use

- When creating a new utility script for the dotfiles
- When the user says "write a script", "add a command", or "create a tool"
- When porting functionality from one language to another within dotfiles
- When adding a wrapper script for a container or flatpak application

## Instructions

### 1. Gather Requirements

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| **Script name** | Yes | — | kebab-case or snake_case (e.g., `record-audio`, `cache_cmd`) |
| **Language** | No | bash | `bash`, `python`, or `crispy` (C) |
| **Description** | Yes | — | One-line description of what it does |
| **Arguments** | No | none | CLI arguments and flags |
| **Dependencies** | No | none | Required tools/libraries |
| **Distrobox** | No | auto | Whether it needs the `dev` container |

### 2. File Location

Scripts go in `~/.dotfiles/bin/scripts/{script_name}`. They are symlinked to `~/.local/bin/scripts/` via `stow`.

### 3. Generate Bash Script

```bash
#!/bin/bash

# dotfiles - Personal configuration files and scripts
# Copyright (C) 2026  Zach Podbielniak
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

set -euo pipefail

readonly SCRIPT_NAME=$(basename "$0")

# ============================================================================
# Help
# ============================================================================

usage () {
	cat << EOF
${SCRIPT_NAME} - {One-line description}

USAGE:
	${SCRIPT_NAME} [OPTIONS] ARG1 [ARG2...]

OPTIONS:
	-h, --help      Show this help message
	--license       Show license information
	-v, --verbose   Verbose output
	{additional options}

EXAMPLES:
	${SCRIPT_NAME} file.txt
	${SCRIPT_NAME} --verbose input.csv output.csv

DESCRIPTION:
	{Detailed description of what the script does, how it works,
	and any important notes about behavior.}

EOF
}

show_license () {
	cat << 'EOF'
dotfiles - Personal configuration files and scripts
Copyright (C) 2026  Zach Podbielniak — AGPLv3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
EOF
}

# ============================================================================
# Parse arguments
# ============================================================================

verbose=false
{other_defaults}

if [[ $# -lt 1 ]]; then
	usage >&2
	exit 1
fi

while [[ $# -gt 0 ]]; do
	case "$1" in
		-h|--help)
			usage
			exit 0
			;;
		--license)
			show_license
			exit 0
			;;
		-v|--verbose)
			verbose=true
			shift
			;;
		--)
			shift
			break
			;;
		-*)
			echo "${SCRIPT_NAME}: unknown option '$1'" >&2
			echo "Try '${SCRIPT_NAME} --help' for more information." >&2
			exit 1
			;;
		*)
			break
			;;
	esac
done

# ============================================================================
# Main
# ============================================================================

{implementation}
```

**Key conventions:**
- `set -euo pipefail` — always
- `readonly SCRIPT_NAME=$(basename "$0")` — for self-referencing in help
- `usage()` function with heredoc showing USAGE, OPTIONS, EXAMPLES, DESCRIPTION
- `show_license()` function with AGPLv3 summary
- Parse arguments with `while/case` loop (not getopts — supports long options)
- Unknown options print error to stderr and exit 1
- `--` separator support for positional args after flags

### 4. Generate Python Script

```python
#!/usr/bin/python3

# dotfiles - Personal configuration files and scripts
# Copyright (C) 2026  Zach Podbielniak
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import subprocess
import sys

# ============================================================================
# Distrobox re-execution (BEFORE any other imports)
# ============================================================================

ctr_id: str = os.environ.get("CONTAINER_ID", "")
no_dbox_check: bool = os.environ.get("NO_DBOX_CHECK", "").lower() in ("1", "true")
if not no_dbox_check and ctr_id != "dev":
    cmd: list[str] = ["distrobox", "enter", "dev", "--", *sys.argv]
    subprocess.run(cmd)
    sys.exit(0)

# ============================================================================
# Imports (safe to import third-party packages now)
# ============================================================================

import argparse
{additional_imports}

# ============================================================================
# Constants
# ============================================================================

NO_COLOR: bool = os.environ.get("NO_COLOR", "") != ""


def _c(code: str, text: str) -> str:
    """Apply ANSI color code to text, respecting NO_COLOR."""
    if NO_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


def _green(text: str) -> str:
    return _c("32", text)


def _red(text: str) -> str:
    return _c("31", text)


def _yellow(text: str) -> str:
    return _c("33", text)


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="{One-line description}"
    )
    parser.add_argument(
        "input",
        help="Input file or value"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--license",
        action="store_true",
        help="Show license information"
    )
    {additional_arguments}

    args = parser.parse_args()

    if args.license:
        print("dotfiles — Copyright (C) 2026 Zach Podbielniak — AGPLv3")
        return 0

    {implementation}

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Key conventions:**
- `#!/usr/bin/python3` — always (not `env python3`)
- Distrobox re-execution block comes BEFORE any non-stdlib imports
- `NO_COLOR` support via environment variable
- Color helper functions (`_c`, `_green`, `_red`, `_yellow`)
- `argparse` for argument parsing (not manual)
- `main() -> int` function with `sys.exit(main())` entry
- Type hints on all function signatures and variables
- `--license` flag for AGPLv3 info

**When distrobox is NOT needed** (pure stdlib, no third-party deps):

```python
#!/usr/bin/python3

# [license header...]

import argparse
import sys

# No distrobox check needed — stdlib only
```

### 5. Generate C/Crispy Script

```c
#!/usr/bin/env crispy
#define CRISPY_PARAMS "-std=gnu89 -O2 $(pkg-config --cflags --libs glib-2.0)"

/*
 * {script_name} — {One-line description}
 * Copyright (C) 2026  Zach Podbielniak — AGPLv3
 *
 * {Extended description if needed.}
 */

#include <glib.h>
#include <glib/gstdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ═══════════════════════════════════════════════════════════════════════════
 * Constants
 * ═══════════════════════════════════════════════════════════════════════════ */

static gboolean g_no_color = FALSE;

static gchar *
_c(const gchar *code, const gchar *text)
{
	if (g_no_color)
		return g_strdup(text);
	return g_strdup_printf("\033[%sm%s\033[0m", code, text);
}

/* ═══════════════════════════════════════════════════════════════════════════
 * CLI
 * ═══════════════════════════════════════════════════════════════════════════ */

static gboolean opt_verbose = FALSE;
static gboolean opt_license = FALSE;
{additional_options}

static GOptionEntry entries[] = {
	{ "verbose", 'v', 0, G_OPTION_ARG_NONE, &opt_verbose,
	  "Verbose output", NULL },
	{ "license", 0, 0, G_OPTION_ARG_NONE, &opt_license,
	  "Show license information", NULL },
	{additional_entries}
	{ NULL }
};

static void
show_license(void)
{
	g_print("dotfiles — Copyright (C) 2026 Zach Podbielniak — AGPLv3\n");
}

/* ═══════════════════════════════════════════════════════════════════════════
 * Main
 * ═══════════════════════════════════════════════════════════════════════════ */

int
main(int argc, char **argv)
{
	GOptionContext *context;
	GError *error = NULL;

	/* Respect NO_COLOR */
	if (g_getenv("NO_COLOR") != NULL)
		g_no_color = TRUE;

	context = g_option_context_new("{USAGE_ARGS} - {description}");
	g_option_context_add_main_entries(context, entries, NULL);

	if (!g_option_context_parse(context, &argc, &argv, &error)) {
		g_printerr("Error: %s\n", error->message);
		g_error_free(error);
		g_option_context_free(context);
		return 1;
	}

	g_option_context_free(context);

	if (opt_license) {
		show_license();
		return 0;
	}

	/* Validate required arguments */
	if (argc < 2) {
		g_printerr("Usage: %s {USAGE_ARGS}\n", argv[0]);
		g_printerr("Try '%s --help' for more information.\n", argv[0]);
		return 1;
	}

	{implementation}

	return 0;
}
```

**Key conventions:**
- Crispy shebang: `#!/usr/bin/env crispy`
- `CRISPY_PARAMS` with `-std=gnu89 -O2` and `pkg-config` calls
- `GOptionContext` for CLI parsing (not manual)
- `NO_COLOR` environment variable support
- Color helpers as functions (not macros that allocate — remember to `g_free`)
- Section headers with box-drawing characters
- All variables declared at block top (gnu89)
- `/* */` comments only
- License as comment block at file top

### 6. Wrapper Script Pattern

For wrapping container or flatpak applications:

```bash
#!/bin/bash

# dotfiles - Personal configuration files and scripts
# Copyright (C) 2026  Zach Podbielniak
#
# [license header...]

set -euo pipefail

exec flatpak --user run com.example.App "$@"
```

Or for distrobox wrapping:

```bash
#!/bin/bash

# [license header...]

set -euo pipefail

if [[ "${CONTAINER_ID:-}" != "dev" ]]; then
	exec distrobox enter dev -- "$0" "$@"
fi

exec /usr/bin/actual-command "$@"
```

### 7. Conventions Summary

| Aspect | Bash | Python | C/Crispy |
|--------|------|--------|----------|
| **Shebang** | `#!/bin/bash` | `#!/usr/bin/python3` | `#!/usr/bin/env crispy` |
| **Safety** | `set -euo pipefail` | — | `g_return_*` preconditions |
| **Args** | `while/case` loop | `argparse` | `GOptionContext` |
| **Help** | `usage()` heredoc | `argparse` auto | `GOptionContext` auto |
| **License** | `show_license()` | `--license` flag | `--license` flag |
| **Colors** | ANSI inline | `_c()` helper | `_c()` helper |
| **NO_COLOR** | `$NO_COLOR` check | `os.environ` check | `g_getenv()` check |
| **Distrobox** | manual check | auto re-exec block | not needed (crispy) |
| **Errors** | `echo >&2; exit 1` | `sys.exit(1)` | `g_printerr; return 1` |

## Output Format

1. Single script file at `~/.dotfiles/bin/scripts/{script_name}`
2. File should be executable (`chmod +x`)

## Examples

**Input:** "Create a bash script called `json-fmt` that reads JSON from stdin or a file argument and pretty-prints it"

**Output:** `~/.dotfiles/bin/scripts/json-fmt` with:
- AGPLv3 header
- `set -euo pipefail`
- `usage()` showing: `json-fmt [OPTIONS] [FILE]`, reads stdin if no file
- `--compact` flag for minified output
- Uses `python3 -m json.tool` or `jq` as backend
- Proper error handling for invalid JSON

## Constraints

- Never omit the AGPLv3 license header
- Never omit `set -euo pipefail` in bash scripts
- Never use `//` comments in C scripts
- Never import third-party Python packages before the distrobox check
- Always include `-h/--help` and `--license` flags
- Always respect `NO_COLOR` environment variable for colored output
- Always validate required arguments before proceeding
- Always write to stderr for error messages, stdout for normal output
