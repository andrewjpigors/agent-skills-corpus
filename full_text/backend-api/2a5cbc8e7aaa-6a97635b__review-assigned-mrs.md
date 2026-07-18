---
name: review-assigned-mrs
description: Find all open GitLab MRs assigned to you for review where you have not yet commented or approved, then review each and post draft comments. Use for batch-reviewing your review queue or clearing your assigned merge requests. Delegates the per-MR review to the mr-review skill.
---

# Review Assigned MRs

Batch-review the open MRs assigned to you for review where you haven't yet interacted. Use the `glab` CLI.

## Step 1 — find MRs needing review

```bash
ME=$(glab api user | jq -r .username)
PROJECT="gitlab-org/gitlab"; PID=278964   # adjust for other projects

glab mr list --reviewer=@me --repo "$PROJECT" --per-page 50 --output json > /tmp/mrs.json

jq -r '.[] | select(.state == "opened") | "\(.iid)|\(.title)"' /tmp/mrs.json | while IFS='|' read -r iid title; do
  approved=$(glab api "projects/$PID/merge_requests/$iid/approvals" 2>/dev/null \
    | jq --arg me "$ME" '[.approved_by[]?.user.username] | map(select(. == $me)) | length')
  commented=$(glab api "projects/$PID/merge_requests/$iid/notes?per_page=100" 2>/dev/null \
    | jq --arg me "$ME" '[.[]? | select(.author.username == $me)] | length')
  [ "$approved" = "0" ] && [ "$commented" = "0" ] && echo "$iid | $title"
done
```

This lists the MRs where you have neither approved nor commented, e.g.:

```
232454 | Resolve "Bug: .well-known/oauth-protected-resource returns resource as an array"
231929 | Fix missing test coverage for SyncFindingEnrichmentWorker
```

## Step 2 — review each MR

For each MR from Step 1, apply the **`mr-review`** skill (`/organizations:mr-review`) to generate and post draft comments.

## Step 3 — summarize

```
Reviewed X MRs:

1. MR !232454 - Posted Y draft comments
2. MR !231929 - Posted Z draft comments

Visit each MR to review and submit the draft comments.
```

## Notes

- `$ME` is derived from `glab api user`; `PID`/`PROJECT` default to `gitlab-org/gitlab` (`278964`) — change for other repos.
- Draft comments are visible only to you until submitted; review each MR before submitting.
