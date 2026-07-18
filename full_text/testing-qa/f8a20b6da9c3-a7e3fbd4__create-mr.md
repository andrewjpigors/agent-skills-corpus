---
name: create-mr
description: Use when preparing a GitLab merge request or GitHub pull request. Pushes the branch and opens via `glab mr create` / `gh pr create` (preferred non-interactive) or hands the user a copy-paste body if the CLI is not authenticated. Includes ticket link, test plan, risk notes.
---

# Create MR / PR

Use after implementation, review, and checks.

## Workflow

1. Inspect branch, diff, commits, and issue context.
2. Confirm quality gates and QA evidence are in hand.
3. Draft a merge request title and body matching observed team
   conventions:
   - Title mirrors the commit subject: `type(scope): <TICKET> subject`.
   - Body sections: Summary, Test plan (checklist), Risk / residual
     gaps, Linked issue (`Closes <TICKET>`), Design link if UI.
4. Push the branch with `git push -u origin HEAD`.
5. Open the MR / PR with the forge's CLI in non-interactive form:

GitLab via `glab`:

```sh
glab mr create \
  --title "type(scope): <TICKET> subject" \
  --description "$(cat <<'EOF'
## Summary

<one-paragraph intent>

## Test plan

- [ ] ...

## Risk / residual

- <known limits>

Closes <TICKET>
EOF
)" \
  --target-branch main \
  --remove-source-branch \
  --squash-before-merge=false
```

GitHub via `gh`:

```sh
gh pr create \
  --title "type(scope): <TICKET> subject" \
  --body "$(cat <<'EOF'
## Summary

<one-paragraph intent>

## Test plan

- [ ] ...

## Risk / residual

- <known limits>

Closes <TICKET>
EOF
)" \
  --base main
```

6. Return the MR / PR URL.

## If the forge CLI is not authenticated

- Detect via `glab auth status` or `gh auth status`. If 401 / "No
  token found":
  - Stop. Tell the user to run `glab auth login` / `gh auth login`
    once.
  - In the meantime, output the title + body as a copy-paste block
    so the user can open the MR / PR from the web UI.

## Autonomous flow

This skill is safe to run end-to-end without user confirmation as long
as: the forge CLI is authenticated, the commit is signed (signing
hardware tap already happened during `commit-prep`), and the branch
passed `pr-audit`.

The non-interactive flag form above opens the MR / PR immediately. Use
the non-interactive form for autonomous flows; never invoke the
interactive prompt.

## Do not

- Do not push without `commit-prep` having run.
- Do not open the MR / PR before `pr-audit` returned GREEN or YELLOW
  with the remediation loop done.
- Do not assign reviewers, mark ready, or mutate the ticket tracker
  from this skill - those go through follow-up steps with
  confirmation.
