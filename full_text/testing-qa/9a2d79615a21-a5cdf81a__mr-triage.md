---
name: mr-triage
description: >-
  Triages merge request feedback by fetching MR comments via GitLab MCP or CLI,
  classifying each item as VALID, INVALID, MISUNDERSTANDING, or NEEDS_INVESTIGATION, writing test cases
  to validate or disprove reviewer claims, and maintaining a living MR-NNN.md
  document with drafted responses. Use when working through reviewer feedback on
  a GitLab MR, when a reviewer raises questions you want to verify, or when you
  need a structured plan to address MR comments before re-requesting review.
license: MIT
metadata:
  version: 1.0.0
  author: agentic-skills
allowed-tools: Read Write Edit Bash Grep Glob AskUserQuestion
---

# MR Feedback Triage

You're the author's advocate. Your job: fetch every comment on an MR, figure out
which feedback is right, which is wrong, and draft clear responses to both.

## Quick Start

1. Fetch comments: `glab mr view <MR_ID> --comments` (or use MCP `get_merge_request_notes`), then create `MR-<MR_ID>.md` from the template below
2. Classify each comment — Valid / Invalid / Needs Investigation
3. For each item, write or update tests, implement fixes, and draft a response
4. Keep the file updated as you work through each item

## When to Use This Skill

- You've received reviewer feedback and want a structured plan before diving in
- A reviewer raised a claim about behavior you think might be incorrect
- You want to draft responses to all feedback before posting replies on GitLab
- You're re-requesting review and need to summarize what changed and why

## Phase 1: Fetch and Parse Feedback

### Fetching comments

Try GitLab MCP first, fall back to CLI:

```bash
# CLI fallback
glab mr view <MR_ID> --comments --repo <project/path>
```

Or via MCP tool `mcp__gitlab__get_merge_request_notes` with `merge_request_iid`.

Capture:
- Note ID (you'll need it to post replies)
- Author and timestamp
- Inline location (file + line) or general discussion
- Full comment text

### Parsing into work items

One work item per discrete concern. A single comment may raise multiple concerns —
split them. Number them sequentially: `MR-<ID>-001`, `MR-<ID>-002`, etc.

## Phase 2: Classification

Classify each work item into one of four categories:

**VALID** — The reviewer found a real bug, gap, or style issue.
Action: implement the fix, add a test, draft a "done, here's what changed" response.

**INVALID** — The reviewer's claim doesn't hold. The code does what they think it doesn't.
Action: write a test that proves the code behaves correctly, draft a rebuttal with evidence.

**MISUNDERSTANDING** — The reviewer misread the intent, not the behavior.
Action: no code change needed; draft an explanation of the design decision.

**NEEDS_INVESTIGATION** — You're not sure yet.
Action: write a test to find out, then reclassify.

## Phase 3: The MR-NNN.md Living Document

Create this file at the project root (or wherever the reviewer will look for it).
Update it continuously — don't wait until all items are done.

### Template

Copy from [assets/MR-NNN-template.md](assets/MR-NNN-template.md) and fill in.
Repeat one block per work item. Update `Status` as you work.

## Phase 4: Work Through Each Item

For each VALID item:
1. Understand the issue
2. Write a failing test that demonstrates the bug
3. Fix the code until the test passes
4. Update the work item: classification confirmed, test ref, draft response

For each INVALID or MISUNDERSTANDING item:
1. Write a test that demonstrates the *correct* behavior
2. Run it — it should pass without any code change
3. If it passes: the reviewer was wrong. Your draft response cites the test.
4. If it fails: reclassify to VALID and fix

```bash
# Run a specific test to validate a claim
cargo test test_name_here  # Rust
go test -run TestFunctionName ./...  # Go
pytest tests/test_foo.py::test_name  # Python
```

## Phase 5: Draft Responses

Each response in MR-NNN.md should:
- Be direct, not defensive
- State what was changed or what the test shows
- Link to specific commits/test names where helpful
- Acknowledge when the reviewer was right

**Good response pattern (VALID fix):**
> Fixed in commit abc1234. Added `tests/test_auth.rs::test_token_expiry` which
> reproduces the issue — the token comparison was using `==` on `Instant` values
> rather than checking elapsed duration. Test now passes.

**Good response pattern (INVALID rebuttal):**
> I think there might be a misread here — `handle_reconnect()` does check the
> connection state before calling `send()`. I added `tests/test_reconnect.rs::test_no_double_send`
> to make this explicit. It passes on main and on this branch.

**Bad response pattern (don't do this):**
> This is fine as-is, the code works correctly.

## Workflow Checklist

Copy and track as you work:

```
Progress: MR !<ID>
- [ ] Fetch all comments
- [ ] Create MR-<ID>.md from template
- [ ] Parse all comments into work items
- [ ] Classify each work item
- [ ] Process NEEDS_INVESTIGATION items (write tests, reclassify)
- [ ] Fix all VALID items (with tests)
- [ ] Write rebuttal tests for INVALID items
- [ ] Draft all responses in MR-<ID>.md
- [ ] Run full test suite — confirm no regressions
- [ ] Review MR-<ID>.md for tone and accuracy
- [ ] Post responses on GitLab (manually, after user review)
```

## GitLab MCP Reference

Key tools available via GitLab MCP:

- `mcp__gitlab__get_merge_request_notes` — fetch all notes for an MR
- `mcp__gitlab__create_merge_request_note` — post a reply (use only when user confirms)
- `mcp__gitlab__get_merge_request` — get MR metadata, diff stats
- `mcp__gitlab__list_merge_request_diffs` — get the file changes

For inline (diff) notes, note the `position` fields — you'll need them if posting
inline replies. Before posting anything to GitLab, **use `AskUserQuestion`** to
confirm: "I've drafted responses for [N] items. Ready to post to MR ![ID]?"

## Writing Style

Apply `natural-writing-style` to all draft responses and the MR summary.

**Don't be defensive.** Reviewers are trying to help, even when they're wrong.
**Be specific.** "Added test X which covers case Y" beats "fixed as suggested."
**Verify before claiming.** Don't draft "fixed" until the test passes.
**Rebuttal means evidence.** State the facts calmly. Let the test speak.

See [references/response-templates.md](references/response-templates.md) for
more pattern examples by feedback type.
