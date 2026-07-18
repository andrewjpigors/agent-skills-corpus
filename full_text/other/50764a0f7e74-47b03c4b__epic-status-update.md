---
name: epic-status-update
description: Generate a weekly status update for a GitLab epic — achievements, blockers, and next steps — in the team's standard format. Supports a quick mode (summarize an epic already in context) and a deep mode (crawl the full epic hierarchy, child issues, and MRs via glab). Use for weekly epic status updates, epic summaries, or a status report on a GitLab epic.
---

# Epic Status Update

Choose the mode that fits the request:

- **Quick** — the epic is already in context (e.g. Duo viewing the epic) and a
  lightweight summary of the last week is enough. Use the format below.
- **Deep** — you need to crawl the whole epic hierarchy, related MRs, and estimate
  hours. Read `references/deep-crawl.md` and follow it.

## Quick mode

Summarize activity over the last 7 days (or the window the user gives).

- **Achievements**: issues closed in the window, each with a 1–2 sentence summary of what it delivers for customers.
- **Blockers**: issues whose status is blocked (may be empty / N/A).
- **Next**: issues with an assignee whose status is `in dev` or `in review`.

Output format (return **only** this Markdown, wrapped in backticks so the user can copy it):

```markdown
## <!-- YYYY-MM-DD --> – <!-- Epic title -->

<!-- High-level summary -->

### :tada: **Achievements**:

- <!-- ... -->

### :issue-blocked: **Blockers**:

- <!-- ... or N/A -->

### :arrow_forward: **Next**:

- <!-- issue link: summary (assignee, workflow status) -->
```

## Rules (both modes)

- Be sure, or be conservative. Beware hallucinations; use qualifying language when uncertain.
- Make every referenced issue/MR/ticket a Markdown link; read linked URLs when it improves the answer.
- Conversational and readable — avoid business speak.
