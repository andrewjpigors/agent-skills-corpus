---
name: skill-para-code
description: >
  Run the PARA CODE pipeline (Capture, Organize, Distill, Express) on content
  to ingest it into the second brain. Trigger when: user wants to ingest content,
  clip a URL, process a file into PARA, distill knowledge, save something to notes,
  or "CODE" any content. Also trigger on "ingest", "second brain", "save to notes",
  "clip this", or "add to knowledge base".
---

# Skill: PARA CODE Pipeline

Runs the full CODE methodology (Capture, Organize, Distill, Express) from Tiago Forte's "Building a Second Brain" on any content — URLs, files, text, or current context — and writes a processed, distilled note into the appropriate PARA location in the second brain at `~/Documents/notes/`. Works from any repo context.

## When to Use

- The user wants to ingest content (URL, file, text) into their second brain
- The user asks to "clip", "save", or "ingest" something to notes
- Processing raw captures through the CODE pipeline
- The user mentions CODE, PARA, second brain, or knowledge base ingestion
- The user wants to distill knowledge from any source into a structured note

## Prerequisites

- The second brain exists at `~/Documents/notes/` organized with PARA:
  - `00_inbox/` — quick capture
  - `01_projects/` — active projects (`personal/`, `work/`)
  - `02_areas/` — ongoing areas (`personal/`, `work/`, `repos/`, `biz/`)
  - `03_resources/` — reference material (`technical/`, `work/`, `ai_chats/`, `academics/`, `book_summaries/`, `food_and_health/`, `news/`, `youtube/`, etc.)
  - `04_archives/` — completed/inactive content
- Web fetching capability for URL captures
- File read access to the second brain directory

## Instructions

### Step 1: Capture

Determine the input type and acquire the content. If no input is provided, prompt the user.

- **URL:** Fetch the page content via web fetch. Convert HTML to clean markdown. Extract metadata: title, author, URL, date.
- **File path:** Read the file. If it's not markdown, convert it (HTML → markdown, etc.).
- **Inline text:** Accept the text as-is.
- **Current context:** If the user says "this file" or "this", read the file they're referencing from the current working directory.

### Step 2: Organize

Analyze the content and determine where it belongs in PARA.

1. **Read the directory structure** of `~/Documents/notes/` to see available categories:
   ```
   ls ~/Documents/notes/00_inbox/
   ls ~/Documents/notes/01_projects/
   ls ~/Documents/notes/02_areas/
   ls ~/Documents/notes/03_resources/
   ```

2. **Classify the content** into a PARA category and subcategory:
   - Is it related to an active project? → `01_projects/{personal|work}/<project>/`
   - Is it an ongoing area of responsibility? → `02_areas/{personal|work|repos|biz}/`
   - Is it reference material for future use? → `03_resources/<topic>/`
   - If unclear, default to `00_inbox/` and note the ambiguity

3. **Suggest tags** based on content analysis (3-7 tags, comma-separated)

4. **Propose a filename** following the convention: `YYYY-MM-DD_descriptive_name.md`
   - Use today's date for the prefix
   - Use underscores, no spaces
   - Keep it concise but descriptive

### Step 3: Distill

Extract the essence of the content using progressive summarization.

1. **TL;DR:** Write a single-sentence summary capturing the core value
2. **Key Insights:** Extract 3-5 bullet points — the most important ideas, facts, or takeaways
3. **Actionable Items:** Identify what the user can *do* with this knowledge — concrete next steps, things to try, ideas to apply
4. **Clean Notes:** Format the original content cleanly in markdown. Remove boilerplate, fix formatting, organize logically. Preserve all substantive content.

### Step 4: Express

Connect this knowledge to the existing second brain.

1. **Search for related notes** in `~/Documents/notes/`:
   - Grep for key terms, names, concepts from the content
   - Look in likely PARA categories for topically related files
   - Check `02_areas/bookmarks.md` for related bookmarks
2. **Suggest 2-5 connections** with brief explanations of relevance
3. **Identify served goals:** Which projects or areas does this knowledge support?

### Step 5: Present and Apply

1. **Present the proposal** to the user:
   - Target path: `~/Documents/notes/<para_path>/<filename>`
   - Frontmatter preview
   - Distilled content preview
   - Connections found
2. **On approval:** Write the file to the target location
3. **Suggest next steps:** "Run `just sync` in ~/Documents/notes/ to update the vectordb"

## Output Format

Each processed note follows this structure:

```yaml
---
title: [AI-generated descriptive title]
source: [URL, file path, or "manual"]
captured: [date content was originally created or found]
processed: [today's date in YYYY-MM-DD format]
para: [category/subcategory path, e.g., "03_resources/technical"]
tags: [comma-separated tags]
status: processed
connections: [comma-separated list of related note paths]
author: Zach
created: [current datetime in YYYY-MM-DD HH:MM format]
updated: [current datetime in YYYY-MM-DD HH:MM format]
version: 1.0.0
---

# [Title]

> **TL;DR:** [One-line distillation of the core value]

## Key Insights
- [Most important insight]
- [Second insight]
- [Third insight]
- [Additional insights as needed, up to 5]

## Actionable Items
- [Concrete action the user can take]
- [Another action or experiment to try]

## Notes
[Original content, cleaned up, formatted, and organized in markdown]

## Connections
- [path/to/related_note.md] - [brief explanation of relevance]
- [path/to/another_note.md] - [brief explanation of relevance]

## Source
[Full source attribution: URL, author name, publication date, etc.]
```

## Examples

### Example: Ingesting a URL

**Input:** `/skill-para-code https://example.com/article-about-kubernetes-networking`

**Result:**

1. Fetches the article, extracts content via web fetch
2. Classifies as `03_resources/technical/` (reference material, technical topic)
3. Tags: `kubernetes, networking, containers, infrastructure`
4. Filename: `2026-03-21_kubernetes_networking_deep_dive.md`
5. Distills: TL;DR, 4 key insights about CNI plugins and service mesh, 2 actionable items
6. Finds connections: existing k8s notes in `03_resources/technical/`, related project docs
7. Writes to `~/Documents/notes/03_resources/technical/2026-03-21_kubernetes_networking_deep_dive.md`

### Example: Ingesting a file from current repo context

**Input:** `/skill-para-code ./docs/architecture.md` (from a project repo)

**Result:**

1. Reads `./docs/architecture.md` from the current working directory
2. Classifies as `02_areas/repos/<project_name>/` or `03_resources/technical/`
3. Distills the architecture doc into key decisions, patterns, and rationale
4. Connects to existing repo notes and related technical resources
5. Writes processed note to the second brain

### Example: Ingesting inline text

**Input:** User says "ingest this: The key insight from today's meeting is that we need to migrate off the legacy auth system by Q3 due to compliance requirements. The new system will use OAuth2 with PKCE flow."

**Result:**

1. Captures the inline text
2. Classifies as `02_areas/work/` (work-related, ongoing area)
3. Tags: `auth, migration, compliance, oauth2`
4. Distills: TL;DR about auth migration deadline, key insight about PKCE, actionable item to track migration
5. Connects to existing work notes, any auth-related resources
6. Writes to `~/Documents/notes/02_areas/work/2026-03-21_auth_migration_q3.md`

## Constraints

- Never overwrite an existing note without explicit user confirmation
- Always present the proposed classification and content before writing — never auto-file without approval
- If PARA classification is ambiguous, default to `00_inbox/` rather than guessing wrong
- Preserve all substantive content from the original source — distillation adds structure, it does not delete information
- Always include source attribution — never strip provenance from captured content
- Do not fabricate connections — only suggest related notes that actually exist in the second brain
- Respect the existing directory structure — do not create new PARA subcategories without user approval
