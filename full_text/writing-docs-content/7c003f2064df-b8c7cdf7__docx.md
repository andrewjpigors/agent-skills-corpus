---
name: docx
description: Create, inspect, edit, and review Microsoft Word .docx files on the local filesystem. Use this whenever the user wants a real Word document, wants structured content turned into .docx, needs to inspect paragraphs or tables before editing, wants a template-based .docx, or asks to revise/review an existing Word file while preserving document formatting as much as possible. Prefer this over generic text editing when the final deliverable must be .docx.
compatibility: Requires python3, python-docx, lxml, and latex2mathml for native Word equation support. Optional local/URL image insertion uses standard library networking.
---

# DOCX

Use this skill for local `.docx` work only.

## Setup

```bash
python3 -m pip install --break-system-packages -r "${PI_CODING_AGENT_DIR:-${HOME}/.pi/agent}/skills/docx/requirements.txt"
```

## Start here

1. If creating a new file, write a JSON spec and run `scripts/docx_tool.py create`.
2. If changing an existing file, run `inspect` first and use the returned IDs.
3. Prefer saving to a new output path unless the user explicitly wants in-place replacement.
4. If the user provides a template `.docx`, pass it with `--template`.

## Commands

```bash
python3 agent/skills/docx/scripts/docx_tool.py inspect input.docx
python3 agent/skills/docx/scripts/docx_tool.py create spec.json output.docx
python3 agent/skills/docx/scripts/docx_tool.py create spec.json output.docx --template template.docx
python3 agent/skills/docx/scripts/docx_tool.py edit input.docx edits.json output.docx
python3 agent/skills/docx/scripts/docx_tool.py review input.docx review.json output.docx
```

## Recommended workflow

### Create

- Use structured content instead of one giant paragraph.
- Prefer these block types: `title`, `subtitle`, `heading`, `subheading`, `paragraph`, `list`, `table`, `image`, `equation`.
- Use `equation` blocks when the user wants a real editable Word equation, not plain text that only looks like math.
- Equation content supports either `latex` or `mathml` and is converted into native Word OMML using the bundled `MML2OMML.XSL` flow.
- `paragraph` blocks can also use `runs` so you can mix normal text and inline equations in one paragraph.
- Put complex tables into `table` blocks instead of trying to fake them with tabs.

### Inspect before editing

Run `inspect` first. The output uses these IDs:

- Paragraphs: `pid:1`, `pid:2`, ...
- Tables: `tid:1`
- Cells: `tid:1/cell:0:0`, `tid:1/cell:2:3`, ...

Equation paragraphs are included in the paragraph IDs, so native equations can be edited or reviewed the same way as normal paragraphs.

`inspect` may add:

- `contains_equation: true` when a paragraph or cell contains OMML math
- `math_text` as an approximate text extraction from the equation XML
- `type: "equation"` for equation-only paragraphs

Use those exact IDs in edit and review specs.

### Edit

- Use `ops` for structure changes such as inserting or deleting paragraphs.
- Use `content_edits` for text replacement, paragraph rewrites, inline paragraph runs, or native equation insertion.
- A `content_edits` value can still be plain text, but it can also be an object like `{"type": "equation", "latex": "\\frac{1}{2}"}`.
- New paragraphs created by structural edits are referenced as `n1`, `n2`, etc.
- Table cells can also receive equation objects when you need editable math inside a table.

### Review

This skill adds inline review notes into the document rather than native Word comment bubbles. That keeps the workflow local and dependency-light.

## References

Read `references/schema.md` when you need the JSON formats for create, edit, or review specs.
