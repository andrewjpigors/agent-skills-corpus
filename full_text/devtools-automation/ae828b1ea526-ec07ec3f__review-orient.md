---
name: review-orient
description: Session startup for review context — load rules, conventions, detect harnex-build specs
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: session-start
---

## Review Orientation Protocol

Every review session starts with orientation.

### Step 1: Identify the Review Target

Determine what is being reviewed:
- **Branch diff**: Use branch from `/gl-review` argument, or current branch.
  Read `base_branch` from `framework/branch-config.yml` (default: `master`).
  **Fetch latest refs before computing diff:**
  `git fetch origin <base_branch> --quiet` and
  `git fetch origin <branch> --quiet 2>/dev/null || true`.
  Use `origin/` refs for the diff to avoid stale local state.
  Compute the diff range using THREE-DOT merge-base syntax:
  `git log --oneline origin/<base_branch>...origin/<branch>` for commits,
  `git diff origin/<base_branch>...origin/<branch>` for the diff.
  **CRITICAL:** Always use three-dot (`...`) not two-dot (`..`).
  Three-dot finds the merge-base and shows ONLY the branch's own
  changes. Two-dot on a stale branch includes upstream changes.
  **CRITICAL:** When reading source files to verify findings, use
  `git show origin/master:<path>` — not the local checkout which
  may be stale.
- **MR**: human provides an MR number or URL
- **File**: human names specific files
- **Staged**: human says "review what I'm about to commit"

### Step 1.5: Load MR & Issue Context

If the review target is a branch:

1. Search for an open MR with this source branch. The
   `gitlab_list_merge_requests(search=...)` parameter matches
   MR **title**, not source_branch — so use the GitLab REST API
   with `?source_branch=<branch>&state=opened` for exact matching.
   Alternatively, use `gitlab_list_merge_requests` and filter the
   results by checking the `source_branch` field in each result.
2. If an MR exists, load:
   - **MR description** — for acceptance criteria, scope notes
   - **MR labels** — for label compliance checking (CHK-LABELS-TRAILERS)
   - **Unresolved discussions** — active reviewer concerns that
     may inform the review or flag already-known issues.
     Use `gitlab_list_discussions(resolved=false)`.
   - **Linked issue** — parse from "Closes" references in the
     MR description and commit trailers
3. If a linked issue is found, load:
   - **Issue description** — for requirements context
   - **Issue comments** — fetch all using `gitlab_list_notes`.
     Summarize key decision points: scope decisions, approach
     agreements, requirement changes, acceptance criteria
     clarifications. Extract the decisions, not the raw
     discussion thread.
4. Unresolved reviewer comments are treated as pre-existing
   concerns — if the diff doesn't address them, flag as WARN
   in the CHK-MR-CONTEXT check during the analyze phase.
5. Pass all context to the analyze phase alongside the diff.

### Step 2: Load Review Rules

Read the static review criteria in `framework/review/rules/`:
- `constraints.yml` — commit discipline, security, test coverage
- `stability.yml` — stability protocol for flagging protected file changes
- `code-conventions.yml` — universal code conventions

### Step 3: Load Project Conventions

If `project/review/conventions/_index.yml` exists:
1. Read the index (one line per convention — compact)
2. Classify the files in the diff by scope (api, testing, general, etc.)
3. Load only the matching scoped convention files

If the index does not exist, this is the first review. Framework rules only.

### Step 4: Detect Harnex-Build Specs

Check if `project/specs/` exists. If so:
- Note which domains have specs
- These will be checked during the analyze phase for contract/invariant compliance

### Step 5: Load Relevant History

If `project/review/history/_index.yml` exists:
1. Read the index
2. Find past reviews that touched similar files or directories
3. Load 0-3 relevant past reviews for pattern context
