---
name: writing-note
description: >-
  Use this skill to read, write, search, or modify files in the user's local Obsidian vault
  (markdown notes). This is the user's personal knowledge base stored as local files. Trigger
  whenever the request involves personal notes — including "save this to my notes", "幫我記",
  "幫我存", "daily note", "筆記", "幫我找...筆記", "我之前有存", "更新筆記", "meeting note",
  "project note", or appending entries to today's log. This skill is the default for any request
  to persist, retrieve, or edit personal knowledge when no external service (Jira, GitHub,
  Confluence, Linear, Things, Slack, email) is explicitly specified. Also trigger on any mention
  of "Obsidian", "vault", or "my notes".
metadata:
  argument-hint: "[note-request]"
  model: sonnet
---

# Obsidian Notes

If `$ARGUMENTS` is provided, treat it as the user's note request and proceed directly without asking for clarification. This does not skip the confirmation step in [Before Writing: New Note or Update?](#before-writing-new-note-or-update) — that check always applies.

## Overview

Standard operations for reading, writing, and organizing notes in the Obsidian vault (Obsidian Flavored Markdown with YAML frontmatter and wikilinks). All vault operations access the filesystem directly using the Read, Write, Edit, Glob, and Grep tools.

## Vault Location

| Item | Value |
|------|-------|
| **Vault root** | `~/Documents/obsidian/My Note` |
| **Notes base** | `~/Documents/obsidian` (may contain multiple vaults) |

All paths in this skill are **vault-relative**. Prepend `~/Documents/obsidian/My Note/` to get the full filesystem path.

## Companion Skills

Obsidian supports more than plain markdown notes. Before proceeding, consider whether the user's request is better served by one of these formats:

| Skill | Format | When to use |
|-------|--------|-------------|
| `obsidian-markdown` | `.md` | **Always invoke** when creating or editing notes — ensures correct Obsidian Flavored Markdown (wikilinks, callouts, embeds, properties) |
| `obsidian-bases` | `.base` | a database view, filtered table, card gallery, or summary of notes by properties |
| `json-canvas` | `.canvas` | a visual layout — mind map, flowchart, project board, or spatial arrangement of ideas |

Invoke the relevant skill(s) before writing content so you follow the correct syntax.

## Search Workflow

Use this workflow whenever the user explicitly asks to find or search notes (e.g. "幫我找...筆記",
"search my notes for X"), and internally whenever [Before Writing](#before-writing-new-note-or-update)
needs to check whether a related note already exists. Never read every match — always end with a
bounded `Read` of the top few candidates. Vault size can grow into the hundreds or thousands of notes,
so always narrow before reading file content, not after.

1. **Classify by type**: if the query names or clearly implies a Project, Meeting, or a specific date,
   skip content search entirely and resolve the path directly — these types always have deterministic
   paths, so there is nothing to search for:
   - Project → `Glob '{Personal,Work}/Projects/**/*.md'`, match by name (exact or fuzzy)
   - Meeting → `Glob '{Personal,Work}/Meetings/<YYYY>/<MM>/*<Title>*.md'` if year/month is known, else
     `Glob '{Personal,Work}/Meetings/**/*<Title>*.md'`
   - DailyNote → direct path `DailyNote/<YYYY>/<MM>/<YYYY-MM-DD>.md`
2. **Path/name narrowing** (General notes or unclassified queries only): `Glob '{Personal,Work}/**/*<keyword>*.md'`,
   excluding the `Projects/` and `Meetings/` subtrees. Pure filename matching — no file content is read yet.
3. **Frontmatter-only narrowing**: grep the `title` and `tags` fields on the Phase 2 candidate set (or
   the full content roots if Phase 2 produced nothing).
   - `title` is always a single line, so an anchored match is enough: `rg -i "^title:.*<keyword>" <path>`.
   - `tags` is normally written as a YAML block list (`tags:` on its own line, followed by one
     `  - value` per line), though a few older notes still use an inline list (`tags: [a, b]`). A
     single-line anchored regex like `^tags:.*<keyword>` only catches the inline form and misses almost
     every block-style note. A fixed-line-count window (e.g. `-A 5`) is **not** safe either — a note
     with more than 5 tags silently drops the extra ones. Instead, extract the whole tags block —
     the `tags:` line plus every following line that stays indented (tolerating a stray blank line
     inside the list), stopping only once a non-indented (top-level) line is reached — so neither the
     tag count nor an incidental blank line can cause a miss:
     ```
     awk '/^[Tt]ags:/{f=1;print;next} f&&/^[[:space:]]*$/{next} f&&/^[[:space:]]/{print;next} {f=0}' <path> | rg -i "<keyword>"
     ```
4. **Body grep on the narrowed set only**: `rg -i -l -F "<keyword>" <candidate-paths-from-phase-2/3>`
   (`-F` for literal terms — faster, and avoids the user's search text being misread as a regex). Only
   fall back to a full-content-root scan (`rg -i -l -F "<keyword>" Personal Work -g '*.md'`) if phases
   2–3 produced zero candidates. Treat "no match" as conclusive only once this full fallback has also
   returned zero — an earlier-phase miss only means the keyword didn't appear in a path name or
   frontmatter field, not that it's absent from every note body.
5. **Bounded read**: `Read` only the top 3–5 files from Phase 4, ranked by match count and/or `updated`
   frontmatter recency — never blindly read every hit.

This is the vault's one documented search procedure — both the write-time existence check and any
explicit search request use the same steps. No index or cache file is created or maintained for this;
plain `Glob`/`Grep` narrowing is fast enough at this vault's scale and never goes stale.

## Before Writing: New Note or Update?

Even when the request sounds like "create a note," never write one — new or updated — without first checking whether a related note already exists.

- **Project** → run [Search Workflow](#search-workflow) phase 1 (`Glob '{Personal,Work}/Projects/**/*.md'`) to check both roots for an existing match (exact or fuzzy name) — a project can exist under either root, so never search just one. Confirm update vs. create with the user before writing.
- **Meeting** → exempt; always create at the fixed path (see [Structured Types](#structured-types-fixed-paths)). To update an existing meeting, follow the [Note Update Workflow](#note-update-workflow) below.
- **General notes** → the check is folded into [General Notes (dynamic discovery)](#general-notes-dynamic-discovery) below — its Discover step looks for a related note at the same time it surveys placement.

In every case: decide **update** vs. **new**, confirm the decision with the user, and only then write. Skip the check only when the user has already named a specific note **and** explicitly stated the intent (e.g., "update the API-Gateway project note", "create a brand-new note called X").

## Note Placement

### Special-Purpose Directories

These vault-root directories sit outside the Personal/Work split entirely. They are not general content notes, and this skill does not write general notes into them:

| Directory | Purpose |
|-----------|---------|
| `assets/` | Non-markdown attachments referenced by notes (images, PDFs) |
| `Clippings/` | Temporary holding area for the Obsidian web-clipper plugin — raw, uncurated, not a real note |
| `DailyNote/` | Obsidian daily notes (see [Structured Types](#structured-types-fixed-paths)) |
| `templates/` | Obsidian template files — skeletons, not real notes |

Exclude these when searching for "related existing notes" (see [General Notes (dynamic discovery)](#general-notes-dynamic-discovery)) — a template or a stray clipping must never be mistaken for an existing note.

### Personal vs Work

Besides the special-purpose directories above, the vault root has exactly two content areas: `Personal/` and `Work/`. Every real note — Project, Meeting, General — lives under one of these; `DailyNote/` is the only structured type that stays at the vault root instead (see [Structured Types](#structured-types-fixed-paths)). Never write a note directly at the vault root.

- **Work** → tied to job responsibilities: Jira tickets, employer projects/teams, meetings with colleagues, work infrastructure.
- **Personal** → everything else: personal projects, hobbies, side learning, life admin.

Decide which one applies using the signals above, then **confirm the choice with the user** before writing — do not silently guess when signals are weak or absent.

### Structured Types (fixed paths)

Project and Meeting notes have fixed, reserved path patterns nested under `Personal/` or `Work/` (see [Personal vs Work](#personal-vs-work) for how to pick one). `DailyNote/` is the one exception — it stays at the vault root, not split by Personal/Work.

| Type | Path pattern |
|------|-------------|
| Project | `[Personal\|Work]/Projects/[ProjectName]/[ProjectName].md` |
| Meeting | `[Personal\|Work]/Meetings/YYYY/MM/[Title] YYYY-MM-DD.md` |
| DailyNote | `DailyNote/YYYY/MM/YYYY-MM-DD.md` |

Always create project and meeting notes at these paths.

### General Notes (dynamic discovery)

For all other notes, **always** explore the vault before deciding anything — never assume where a note should go, or that it needs to be created at all, without checking first.

1. **Discover**: run [Search Workflow](#search-workflow) phases 1–4 for the topic, treating any hit as
   a candidate existing note. If all phases return zero hits (confirming no related note exists), follow
   up with a broader `Glob` (`{Personal,Work,DailyNote}/**/*.md`) to survey the target root's existing
   directories and naming conventions before deciding where to place a new note — the Search Workflow
   narrows for matches, but placing a genuinely new note still needs the wider structural picture.
   Exclude `templates/`, `Clippings/`, and `assets/` (see [Special-Purpose Directories](#special-purpose-directories))
   from either pass so they're never mistaken for real notes.
1. **Decide**:
   - A related note already exists → this is an **update** — proceed to the [Note Update Workflow](#note-update-workflow)
   - No related note exists → this is a **new note** — decide placement:
     - **Existing location fits** → place the note there; follow local naming conventions exactly
     - **No existing location fits** → pick [Personal or Work](#personal-vs-work), then create a new path under that root consistent with the vault's overall style; briefly explain the choice to the user
     - **Restructuring needed** → explain why and get user confirmation before moving any files
1. **Confirm with the user**: state the decision (update at `X` / create at `Y`) and wait for explicit confirmation before writing anything.
1. **Execute**: only after confirmation, follow the [Note Creation Checklist](#note-creation-checklist) or [Note Update Workflow](#note-update-workflow).

**Depth constraint**: Below `Personal/` or `Work/` (excluding their `Projects/` and `Meetings/` subtrees) and below `DailyNote/`, directory nesting must not exceed **3 levels** (e.g., `Personal/Area/Topic/SubTopic/note.md` is the maximum depth). Do not create deeper hierarchies.

**Principles**: Prefer existing structure over creating new folders. Observe local conventions — different vault areas may use different patterns. When content doesn't fit any existing category, create a new folder but justify the choice.

## Templates

| Type | Template |
|------|----------|
| Project | *(free-form body)* — frontmatter fields per `references/note-organization.md` |
| Meeting | `assets/meeting.md` |
| DailyNote | *(plugin-managed)* — see [Structured Types](#structured-types-fixed-paths) |

## Note Creation Checklist

> This applies to all note types. For General notes, this is the entry point only after completing [General Notes (dynamic discovery)](#general-notes-dynamic-discovery) and getting user confirmation. For Project notes, this is the entry point after the existence check in [Before Writing](#before-writing-new-note-or-update).

1. Determine note type (meeting / daily / general / project)
1. **Determine placement**:
   - Meeting / Project → use the fixed path (see [Structured Types](#structured-types-fixed-paths))
   - General → placement was already decided by [dynamic discovery](#general-notes-dynamic-discovery)
1. Select template if applicable (Project has none — free-form body)
1. Create with `Write` at the full filesystem path
1. Verify frontmatter fields: `created`, `updated`, `tags` (plus `title` for general notes — Project/Meeting use the filename as the title instead), plus any type-specific fields per `references/note-organization.md` (e.g., `jira`, `status` for Project)
1. Verify creation: `Read` the file to confirm it was created and YAML is valid

## Note Update Workflow

> Entry point: the user explicitly asked to update/add to/modify a named note, or you arrived here via [General Notes (dynamic discovery)](#general-notes-dynamic-discovery) after finding a related existing note. This same workflow applies to Project note updates — since the body is free-form, integrate new content under whatever existing heading fits best.

When updating an existing note, do NOT blindly append new content to the end. Instead, follow this workflow:

1. **Read**: `Read` the file at its full filesystem path to get the full current content
1. **Analyze**: Identify the note's headings, sections, and organizational structure
1. **Integrate**: Compose the updated note by merging new content into the existing structure:
   - Place new content under the most relevant existing heading
   - Merge overlapping or duplicate information — keep the more complete or up-to-date version
   - Add a new section only when no existing heading fits; position it logically, not at the end by default
1. **Write**: Overwrite the note with `Write` (or use `Edit` for targeted changes)
1. **Verify**: `Read` the file again to confirm the result is well-structured

### When append IS appropriate

Use append only when the note is inherently chronological and the new content is a discrete new entry:

- **Daily notes**: adding log entries or timestamps
- **Meeting notes**: adding follow-up items after the meeting
- **The user explicitly says** "append", "add to the end", or "加在後面"

Use `Edit` to insert content at the correct position, or `Bash` (`echo >> file`) for a simple append to end of file.

If unsure, default to the integrate workflow above.

## Reference Files

| File | When to read |
|------|-------------|
| `references/note-organization.md` | Naming, tag system, frontmatter standards |
