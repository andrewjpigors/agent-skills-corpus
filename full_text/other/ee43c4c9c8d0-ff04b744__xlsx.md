---
name: xlsx
description: Create, inspect, edit, and review Microsoft Excel .xlsx workbooks on the local filesystem. Use this whenever the user wants a real spreadsheet, needs tabular data written into Excel, wants workbook structure or cell inspection before edits, needs row/column insertion or deletion, wants comments added to cells for review, or asks for a template-based spreadsheet deliverable. Prefer this over generic CSV or plain-text editing when the final output must be .xlsx.
compatibility: Requires python3 and openpyxl.
---

# XLSX

Use this skill for local `.xlsx` work only.

## Setup

```bash
python3 -m pip install --break-system-packages -r "${PI_CODING_AGENT_DIR:-${HOME}/.pi/agent}/skills/xlsx/requirements.txt""
```

## Start here

1. For new spreadsheets, write a JSON spec and run `scripts/xlsx_tool.py create`.
2. For changes to an existing workbook, inspect first.
3. Use `SheetName!A1` style references in edits and review specs.
4. Save to a new output path unless the user clearly asked to overwrite.

## Commands

```bash
python3 agent/skills/xlsx/scripts/xlsx_tool.py inspect workbook.xlsx
python3 agent/skills/xlsx/scripts/xlsx_tool.py create spec.json output.xlsx
python3 agent/skills/xlsx/scripts/xlsx_tool.py create spec.json output.xlsx --template template.xlsx
python3 agent/skills/xlsx/scripts/xlsx_tool.py edit workbook.xlsx edits.json output.xlsx
python3 agent/skills/xlsx/scripts/xlsx_tool.py review workbook.xlsx review.json output.xlsx
```

## Recommended workflow

### Create

- Put the main grid in `rows`.
- Use `sheet_name` to control the primary worksheet name.
- Use a template workbook when the user already has styles, formulas, or formatting they want preserved.

### Inspect before editing

`inspect` outputs all non-empty cells with references like `Summary!B4`.

### Edit

Supported structure ops:

- insert/delete row
- insert/delete column

Supported content edits:

- set a cell by `Sheet!A1`
- if no sheet prefix is given, the active sheet is used

### Review

Review comments are written as native Excel cell comments.

## References

Read `references/schema.md` for JSON examples and supported edit operations.
