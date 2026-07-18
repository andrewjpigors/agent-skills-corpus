---
name: mr-review
description: Review a single GitLab merge request as a staff-level maintainer using Conventional Comments — covering Ruby quality, database migrations, test coverage, and security — then post findings as draft notes on the diff lines via glab. Use when reviewing one GitLab MR, giving maintainer-level feedback, or posting draft review comments to an MR.
---

# GitLab MR Review

Review a merge request as a staff-level GitLab maintainer. Use the `glab` CLI to interact with GitLab.

## Workflow

1. **Fetch context**: `glab mr view <MR_IID>` (description) and `glab mr diff <MR_IID>` (diff). Alternatively append `/diffs.diff` to the MR URL.
2. **Assess** the changes against the review checklist — read `references/review-checklist.md` (Ruby, migrations, tests, database, security, general standards).
3. **Write comments** in Conventional Comments format — read `references/conventional-comments.md` for labels, decorations, and examples. Leave at least one `praise:`.
4. **Post as drafts** on the specific diff lines via the GitLab API — read `references/posting-drafts.md`. Drafts are visible only to the author until submitted.
5. **Summarize** and tell the user to review and submit the drafts.

## Output format

1. **Summary**: 2–3 sentence overview of the MR and its readiness.
2. **Findings**: each comment with file, line, and the conventional comment text.
3. **Drafts posted**: confirm what was posted, then:

> Draft review comments have been posted. Visit the MR to review and submit:
> `https://gitlab.com/gitlab-org/gitlab/-/merge_requests/<MR_IID>`

Cite guideline URLs when drawing conclusions.
