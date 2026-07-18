---
name: create-merge-request
description: Create and verify GitLab merge requests for already-pushed branches in projects under the MRS Electronics GitLab group. Use when asked to create or open an MR from the current branch without committing, pushing, or changing branch history.
---

# Create Merge Request

Publish a focused branch through `glab` using the repository's own contribution rules and merge request template.

## Inspect the Repository

1. Read the repository's applicable agent instructions.
2. Confirm that `origin` belongs to `gitlab.com/mrs-electronics/`.
3. Inspect:
   - the current branch and its upstream
   - the remote default branch
   - commits and diff between the remote source and target branches
   - any existing MR for the source branch
   - `.gitlab/merge_request_templates/` and other repository contribution guidance
4. Confirm that the current branch exists on `origin` and that local `HEAD` matches the upstream branch.

If an MR already exists for the branch, report it instead of creating a duplicate.

Do not commit, push, create branches, or change branch history. If the source branch is missing from `origin` or differs from local `HEAD`, stop and tell the user what must be pushed before the MR can be created.

## Write the Merge Request

Use the repository's default MR template when one exists. Preserve its headings and reviewer fields, replacing instructional placeholders with concise, change-specific content.

Choose a title that describes the branch's single outcome and follows repository conventions. Keep the description concise and include:

- a short list of material changes
- a clear scope boundary when the MR implements only part of an issue or plan
- the relevant issue or spec link when known
- a reviewer-facing manual testing checklist

Do not claim that a partial MR closes an issue unless it completes the issue.

### Testing Section

Make `Testing` a Markdown checklist of manual tasks for the reviewer. Each item must describe behavior the reviewer can exercise or observe. Use nested checklist items for commands, setup, and expected results.

Example:

```markdown
### Testing

- [ ] Launch the mobile app through Moon.
  - [ ] Run `moon r mobile:run`.
  - [ ] Confirm the app reaches its normal initial screen.
- [ ] Exercise the updated settings flow.
  - [ ] Change the setting and leave the page.
  - [ ] Return to the page and confirm the value persisted.
```

Do not list automated tests, linters, analyzers, validation commands, pre-commit hooks, or CI jobs in this section. CI/CD is the source of truth for automated checks.

## Create and Verify

1. Create the MR with `glab`, targeting the remote default branch unless the user specifies another target.
2. Create a regular MR unless the user asks for a draft.
3. Apply the requested reviewer, assignee, labels, milestone, squash setting, and source-branch cleanup behavior when known. Do not invent project metadata.
4. Read the created MR back from GitLab.
5. Verify the title, source and target branches, description formatting, issue link, reviewers, and draft state.
6. Report the MR link and any material caveat. Do not wait for the pipeline unless the user asks.
