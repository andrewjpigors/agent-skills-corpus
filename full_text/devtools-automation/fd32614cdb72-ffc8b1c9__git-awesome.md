---
name: git-awesome
description: >-
  Unified Git automation + reconciliation doctrine. Hardcoded universal defaults, local-only autostash
  via `scripts/bin/git-awesome sync`, NDJSON state ledger, finalizer guard contract, unified Issue+PR
  contract, six-category review rubric (blocker/nit/question), remediation loop, auto-merge gating.
  Use when the user asks to sync, merge, reconcile, audit, recover, clean up divergence, review a PR,
  triage an Issue, or make a repo safe to push/release.
---

# git-awesome: Unified Git Automation & Reconciliation Doctrine

## Purpose

Reconcile the whole repository, not just the current branch. The goal is zero data loss, no secret leaks, no duplicate ghost work, and a main/default branch that is semantically correct, tested, and explainable.

## Doctrine Boundaries

- `/git-awesome` is the source doctrine for Git safety and autonomous-agent reconciliation. Repo docs, generated workflows, and local scripts must either conform to it or explicitly declare a narrower repo-specific policy.
- Universal rules are about preserving work, classifying state, avoiding accidental mutation, and reaching an explainable clean handoff.
- Merge style, branch names, review count, squash-only, no-`develop`, and no-staging-branch are house or repo policy choices. They are good defaults for Wranngle-managed repos, not universal Git law.
- The framework has zero per-repo policy files. Universal defaults are hardcoded in `scripts/bin/git-awesome`; see the **Hardcoded Defaults** section. The single escape hatch is `git-awesome --dry-run <subcommand>`.
- Hosted-provider protections are best-effort unless the repo can actually enforce them. Missing GitHub rulesets or branch protection are policy findings, not proof that local reconciliation is unsafe.

## Non-Negotiables

- Never use destructive commands (`git reset --hard`, `git clean`, branch deletion, reflog expiry, force push, deleting stashes/worktrees) unless the user explicitly asked for that exact operation or you have created a clearly named safety ref/stash and the destructive step is necessary.
- Do not assume the current checkout is the only checkout. Inspect linked worktrees, sibling clones, automation-created clones, stashes, and ignored files before declaring work missing or merged.
- Protect dirty work before integrating. Prefer a safety branch plus `git stash push -u -m "reconcile/<timestamp> ..."`. Include untracked files; inspect ignored files before deciding whether to include them.
- Fetch before judging remote state, and fetch again before pushing. Race with autosync, PR squash merges, and GitHub Actions-generated commits is normal.
- Reconcile code semantically. Diffs are evidence; they are not the decision. Read the changed code, understand behavior, run the relevant tests/checks, and call out risk when validation is missing.
- Keep secrets out. Run redacted secret scans before committing/pushing when available, and treat `.env`, keys, tokens, real data exports, and private PII as blocked until proven safe.
- Do not install ambient Git or agent hooks as a universal guard. Finalization is an explicit baseline/finalize contract that fails closed when no baseline exists.
- Do not force a Wranngle house style onto client or external repos. Inspect branch protection, open PRs, and release tooling before deciding what "clean" means. Client/external repos simply do not install or invoke `git-awesome`.

## Operating Loop

1. **State the Scope**
   - Identify repo root, current branch, default branch, upstream, remote slug, and whether the user wants audit-only or actual reconciliation.
   - If multiple repos are involved, inventory all of them first and process one repo at a time.

2. **Build a Complete Topology Inventory**
   - Core identity: `pwd -P`, `git rev-parse --show-toplevel --git-dir --git-common-dir --is-inside-work-tree --is-bare-repository`, `git status --short --branch --untracked-files=all`, `git remote -v`, `git branch -vv --all`.
   - Fetch safely: `git fetch --all --prune --tags` unless the user asked not to touch remotes.
   - Worktrees: `git worktree list --porcelain`. For each linked worktree, inspect branch, HEAD, path, and dirty state. Do not modify another worktree without saying so.
   - Submodules and nested repos: `git submodule status --recursive`, plus a targeted search for nested `.git` directories. Treat nested repos as independent reconciliation units.
   - Hidden Git mechanics: inspect sparse checkout, shallow/partial clone state, LFS, alternates, replace refs, grafts, hooks, locks, merge/rebase/cherry-pick/bisect state, skip-worktree/assume-unchanged bits, filemode, EOL, and case-sensitivity settings when symptoms point there.
   - Ref inventory: list local heads, remote heads, tags, stashes, `refs/replace`, `refs/original`, `refs/backup`, `refs/wip`, and any nonstandard namespaces with `git for-each-ref`.

3. **Find Every Dirty Surface**
   - Tracked/staged/unstaged: `git diff --stat`, `git diff --check`, `git diff`, `git diff --staged --stat`, `git diff --staged`.
   - Untracked: `git ls-files --others --exclude-standard`.
   - Ignored but possibly important: `git status --ignored --short`, `git ls-files --others --ignored --exclude-standard`. Separate build/cache/logs from mock data, fixtures, exports, SQLite files, generated docs, and agent output that may be valuable.
   - Stashes: `git stash list`, then inspect relevant entries with `git stash show --stat` and `git stash show -p`.
   - Submodules: check each submodule for dirty state and detached HEAD.
   - Worktree safety: if any linked worktree is dirty on the same branch, stop and plan around it. Git branch operations can affect all worktrees sharing refs.

4. **Map All Diffs and Divergence**
   - Default branch: compare local default, `origin/<default>`, and current HEAD with `git log --left-right --cherry-pick --oneline A...B`, `git diff --stat A...B`, and `git merge-base`.
   - Feature branches: list active local and remote branches by recency. Inspect branch purpose, unique commits, changed files, and open PR linkage.
   - Tree-equivalent drift: if histories diverge but `git rev-parse A^{tree}` equals `git rev-parse B^{tree}`, treat it as commit-shape drift from squash/rebase/autosync. Align safely instead of hand-merging identical content.
   - Range review: use `git range-diff old-base..old-head new-base..new-head` for rebased or duplicated branches when appropriate.
   - Rename and mode changes: include `--find-renames`, `git diff --summary`, and `git diff --name-status` so deletes, renames, chmod, symlinks, and binary changes do not disappear in a stat-only review.
   - Whitespace vs substance: use `git diff -w` and `git diff --ignore-space-at-eol` only to classify noise; do not use them to hide behavior changes.

5. **Audit Ghosts, Backups, and Evil Twins**
   - Search for sibling clones/workspaces only as broadly as needed: common locations include parent directories, `.symphony/workspaces`, `.codex/.tmp`, `.gemini/tmp`, `.claude`, `old/`, `backup/`, `*.bak`, and copied repo directories.
   - Compare remotes before trusting a twin. Same directory name does not mean same repository; same remote does not mean same branch or state.
   - Inspect bot refs: Dependabot branches, release-prep branches, and stale backup refs. The `wip/**` namespace was retired 2026-05-12; treat any surviving `wip/` ref as a historical artifact to garbage-collect via `git-awesome gc --legacy-wip`.
   - Do not push from a ghost clone unless it is intentionally the source of truth and the user understands that choice.

6. **Read Logs and Automation State**
   - Local logs: inspect repo `logs/`, bootstrap logs, the per-repo events ledger at `<repo>/.artifacts/git-awesome/events.<yyyy-mm-dd>.jsonl` (ECS-shaped JSONL), agent logs, cron logs, and systemd user timers/services when automation is suspected.
   - Git logs: use `git log --graph --decorate --oneline --all --date-order`, reflogs, and stash metadata to reconstruct what happened.
   - Host-level automation: check crontab, systemd user units, long-running agent processes, global dotfiles scripts, and hooks.
   - If patching automation, run syntax checks and a dry run with a disposable log before enabling it.

7. **Inspect GitHub, PRs, and Actions**
   - Auth and repo: `gh auth status`, `gh repo view --json nameWithOwner,defaultBranchRef,visibility,isArchived`.
   - PRs: list open and recently closed PRs, including autosync/bot PRs: `gh pr list --state all --limit 100 --json number,state,title,headRefName,baseRefName,mergeCommit,updatedAt,isDraft`.
   - For relevant PRs, inspect body, commits, files, checks, reviews, merge state, and whether a squash merge already landed equivalent content.
   - Actions: `gh run list --limit 50`, then `gh run view --log-failed` for failing or flaky runs. Correlate failures with the exact commit/branch being reconciled.
   - Workflows: inspect `.github/workflows/**`, disabled workflows, required checks, branch protection/rulesets, repo Actions permissions, CODEOWNERS, PR templates, issue templates, labels, secrets/variables metadata, and environments when they affect mergeability.
   - Never infer green status from a local test alone when branch protection requires GitHub checks.

8. **Audit Security, Dependencies, and Repo Policy**
   - Gitleaks: run `gitleaks detect --source . --redact --no-banner` or equivalent when available; before committing staged changes, use `gitleaks protect --staged --redact --no-banner`.
   - If gitleaks is absent, perform a conservative redacted scan for obvious secrets and verify secret patterns in `.gitignore`. Do not print secrets.
   - Dependabot: inspect `.github/dependabot.yml`, open Dependabot PRs, dependency lockfile changes, vulnerable dependency alerts when accessible, and whether dependency updates are grouped or blocked by CI.
   - GitHub workflow safety: flag broad `contents: write`, unsafe `pull_request_target`, unpinned third-party actions, accidental secret exposure to forks, and auto-merge rules that can merge unreviewed code.
   - Config health: review `.gitignore`, `.gitattributes`, `.editorconfig`, pre-commit hooks, LFS tracking, package manager locks, CI config, and release/deploy config for contradictions with the intended repo policy.

9. **Evaluate Code and Feature-Level Semantics**
   - Read changed files, not just commit messages. Identify feature slices, bug fixes, refactors, formatting-only churn, generated artifacts, migrations, and config changes.
   - Decide whether changes should merge together or be split. Preserve atomicity when it lowers risk; consolidate only when separation would be artificial or unsafe.
   - Validate behavior with the repo's actual commands: tests, typecheck, lint, build, format check, migration checks, smoke tests, and targeted app flows. Prefer existing scripts and documented commands.
   - For frontend/app work, inspect user-facing behavior and generated assets when feasible. For libraries/APIs, inspect contract changes and downstream compatibility.
   - If tests are missing or cannot run, say exactly what was not validated and what risk remains.

10. **Plan the Reconciliation Before Mutating**
   - Produce a short action plan when changes are nontrivial: safety refs/stashes, branches to merge or retire, PRs to respect, tests to run, and push strategy.
   - Create safety anchors: named branch/tag refs, stash entries, or patches. Include enough metadata to recover.
   - Prefer merge/rebase/cherry-pick strategies that preserve semantic intent and minimize surprise. Avoid force-push unless explicitly authorized; if needed, use `--force-with-lease` after a fresh fetch.

11. **Execute Safely**
   - Apply one logical step at a time and inspect status between steps.
   - Resolve conflicts by reading both sides and the base. Do not blindly accept ours/theirs except for generated files with a defensible rule.
   - For stale squash-merged branches, preserve the pointer, switch back to the default branch, and align the default branch to `origin/<default>` only after confirming tree equivalence.
   - Delete local/remote branches only after confirming they are merged, tree-equivalent, or intentionally obsolete, and only when deletion is part of the task.

12. **Final Health Gate**
   - Cleanliness: `git status --short --branch --untracked-files=all` and worktree/submodule status.
   - History: local branch ahead/behind, default branch alignment, remaining active branches/PRs, and any safety refs/stashes left intentionally.
   - Validation: tests/checks run, GitHub Actions status, gitleaks/secret scan result, dependency/workflow health, and any skipped checks.
   - Push: fresh fetch before push; handle rejection by comparing trees and PR state before retrying.
   - Handoff: summarize what changed, what was preserved, what was merged/retired, what risks remain, and exact next commands only if the user needs to run them.

## Issue + PR Contract (Unified)

Issues and PRs share one shape. An Issue is a forward-looking PR; a PR is a backward-looking Issue. Apply the same title format, same area taxonomy, same labels, same review rubric, and same severity vocabulary to both. This skill is the canonical reference for both humans and agents; per-repo docs were retired 2026-05-12.

### Title
`<type>(<scope>): <imperative ≤72 chars>` where `<type>` ∈ `feat | fix | bug | chore | docs | refactor | research | security | perf`. Same form for Issue titles, PR titles, and commit messages.

### Canonical body sections (mapped to deployed forms)

| Section | bug_report.yml | feature_request.yml | research.yml | PULL_REQUEST_TEMPLATE.md |
|---|---|---|---|---|
| What | `### What & how to reproduce` | (combined with Why) | `### Question / hypothesis` | `### Summary` |
| Why | (embedded in repro Expected/Actual) | `### Problem & Why now` | (embedded in question) | (embedded in Summary) |
| How | n/a | `### Proposed approach` | `### Deliverable` + `### Timebox` | `### Testing Notes` + `### Change Type` |
| Area | `### Area` | `### Area` | `### Area` | inherited from linked issue |
| Env/Logs | `### Environment`, `### Logs / traceback` | n/a | n/a | n/a |
| Linkage | n/a | `### Alternatives considered` (related issues) | n/a | `### Related Issue` — MUST use `Closes #N` / `Fixes #N` / `Resolves #N` |

The inline `gh-issue` bash function in `~/.agents/AGENTS.md` (and per-repo `.agents/AGENTS.md`) generates the form body from a one-liner via `llm.sh`, preserving the canonical headings. Do not invent new headings; the `issue-triage.yml` workflow parses `### Area` by exact match.

### Labels (static facets only)
- `t.<type>` — exactly 1 per Issue/PR; assigned at creation by form/template defaults.
- `a/<area>` — 0–N; applied automatically by `issue-triage.yml` reading the `### Area` value.
- `triage` — applied on open; removed when classified.
- `blocked` — applied when work cannot proceed; reason in the latest comment.
- `automerge` — PR command label; arms `automerge.yml` after checks pass.
- `pr-needs-issue` — auto-applied by `pr-link-check.yml` when PR body lacks `Closes/Fixes/Resolves #N`; auto-removed on edit.

Status / Priority / Effort live in the user-level Projects v2 `Triage` board, never as labels.

### Projects v2 board

A single user-level `Triage` Projects v2 board (one per `gh` user) gathers issues across every managed repo. Cross-repo visibility is the point.

| Field | Source | Values |
|---|---|---|
| Status | Projects v2 default | Todo · In Progress · Done |
| Priority | seeded by bootstrap | P0 · P1 · P2 · P3 |
| Effort | seeded by bootstrap | XS · S · M · L · XL |
| Repository | Projects v2 auto-fill | populated on item-add |

The board is discovered or created on every bootstrap run by `ensureUserLevelTriageProject` in `.dotfiles.sh`. Per-repo wiring sets repo variables `TRIAGE_PROJECT_NUMBER` + `TRIAGE_PROJECT_OWNER`, which `issue-triage.yml` reads to call `gh project item-add` on every newly-opened issue.

One-time setup: add `PROJECTS_TOKEN=ghp_…` to `~/.agents/.env` (classic PAT with `project`, `read:project`, `repo` scopes). Bootstrap uses it for both local project ops and as the per-repo workflow secret.

### Why not labels for status / priority / effort?

- Labels lose ordering. You cannot sort "P0 oldest first."
- Filtering composite views ("P1 + In progress + due this week") needs SQL-grade slicing; labels cannot.
- Labels rot when applied manually. Projects v2 fields appear as required defaults at item-add time.
- The `gh project` CLI is fully scriptable; the label REST API is rate-limited and noisier.

## Review Rubric (Issues and PRs)

Apply six categories on every review pass. The categories are universal — same rubric for PR code review and for Issue triage.

1. **Correctness** — does the change/report match its title and linked Issue? Read the code or repro, not just the diff.
2. **Tests** — covered by tests or proven manually? Missing tests is a `nit` unless the change touches an invariant, payment, auth, migration, schema, or data shape — then `blocker`. For Issues, "tests" means: is the repro deterministic and minimal?
3. **Secrets** — no `.env`, keys, tokens, real PII, or production credentials in the diff, logs, screenshots, or comments. Run `gitleaks protect --staged --redact --no-banner` (or `gitleaks detect`) before approving. For Issues: redact before posting any pasted log.
4. **Scope** — change matches the linked Issue and the title. Drive-by refactors only when explicitly declared in the PR body; otherwise `nit` to split. For Issues: one symptom per Issue; "and also" → file a second Issue.
5. **Docs** — README, CHANGELOG, `AGENTS.md`, `docs/`, or inline WHY comments updated when behavior changed. The conventional-commit type drives doc expectations: `feat`/`fix`/`security` usually needs CHANGELOG; `docs` is the change itself.
6. **Blast radius** — migrations, public API surface, build artifacts, deploy config, branch protection, secrets/variables, CODEOWNERS. Flag any change that crosses these surfaces. On `client` / `external` / `repo-default` overlay repos, require human review here regardless of label.

## Severity Vocabulary

Three tags exactly, used in every review comment, PR review body, and Issue triage note:

- `blocker` — must fix before merge or close. Wrong behavior, secret leak, missing required check, broken migration, scope mismatch on a `style` PR, ambiguous repro on a security Issue. Stops auto-merge.
- `nit` — should fix but does not block. Style, redundancy, missing WHY comment, light refactor opportunity, missing low-risk test, missing optional Issue field. Author may merge over a `nit`.
- `question` — clarification needed. May or may not lead to a change. Resolve before merge if it affects correctness; otherwise carry to a follow-up Issue.

Order findings by severity. Within severity, order by the Failure Precedence list below (in-progress git ops → dirty tree → divergence → PR/CI → policy).

## Review Feedback Format

One consolidated review per pass, not drip comments. Drip-commenting fragments the audit trail and re-triggers notifications.

Body shape for `gh pr review <N> --body @-` (or `gh issue comment <N> --body @-` for Issue triage):

```
## Summary
<one-paragraph judgement: approve | request-changes | comment>

## blocker
- <file:line — finding — recommended fix>
- ...

## nit
- <file:line — finding>
- ...

## question
- <file:line — what is unclear>
- ...

## Validation run
- <commands run, results>
- <commands skipped, with reason>
```

Posting:
- `gh pr review <N> --approve --body @-` when zero `blocker` items and the work matches scope.
- `gh pr review <N> --request-changes --body @-` when any `blocker` is present.
- `gh pr review <N> --comment --body @-` when only `nit` or `question` items.
- Inline line comments via `gh api repos/<owner>/<repo>/pulls/<N>/comments` ONLY when the finding is unambiguously line-local; otherwise keep it in the consolidated body. Maximum 5 inline comments per review pass — anything more belongs in the body.

For Issue triage, post the same shape as a single Issue comment. Apply or remove `triage`, `blocked`, `automerge`, `pr-needs-issue` only after the body is posted, so reviewers see the rationale before the label change.

## Remediation Loop

The world-standard flow is: push new commits to the PR head branch; do not rewrite shared history.

1. **Reproduce locally on the PR branch.** `gh pr checkout <N>`, then run the rubric's validation commands.
2. **Push fix commits to the same branch.** New commits attach to the PR automatically. Auto-merge stays armed; checks re-run on the new head SHA; the 2-stable-green-poll gate in `automerge.yml` picks up the new head.
3. **Never force-push a shared branch** unless rebasing onto an updated default branch is required. When you must, use `git push --force-with-lease=<branch>:<expected-oid>` immediately after a fresh `git fetch`. Plain `--force` is banned because it races against autosync, Dependabot, and any human reviewer who pushed in the interim.
4. **Re-request review** only when human reviewers are mandated by CODEOWNERS or branch protection. Use `gh pr ready <N>` to flip out of draft, `gh pr edit <N> --add-reviewer <handle>` to re-request. Agents do not self-approve agent-authored PRs.
5. **Resolve every `blocker`** with a commit message that references it: `fix: <what> — resolves blocker from review`. Reference the reviewing agent or human with `Co-authored-by:` when applicable.
6. **Disarm auto-merge if scope changed** mid-loop: `gh pr merge <N> --disable-auto`. Re-arm only after a fresh review pass.

## Auto-Merge Invocation

Auto-merge is gated. Do not invoke it unilaterally.

### When `automerge.yml` arms it for you (no action needed)
- PR carries the `automerge` label.
- Author is `dependabot[bot]` and `update-type` ∈ `version-update:semver-patch` or `version-update:semver-minor`.

The workflow polls 2× stable green across the required-checks set (`shell-lint,yaml-lint,test,gitleaks,actionlint,zizmor,workflow-lint`) before calling `gh pr merge <N> --squash --delete-branch`. Required checks are listed in the **Hardcoded Defaults** section below.

### When to arm it manually
Only when ALL hold:
- A consolidated review with zero `blocker` items has been posted.
- Required checks are configured as required in branch protection.
- The PR's base branch is `main` or `master`; head is not under `wip/**`, `scratch/**`, or `dependabot/**`.

Command:
```sh
gh pr merge <N> --squash --auto --delete-branch
```

### When to leave hands off
- Repo is client/external (no Wranngle house style); defer to repo policy and human approval. Symptom: `git-awesome` is not installed or not invoked there.
- Branch protection missing — auto-merge needs real enforcement.
- Cron is paused (`crontab -e` shows the `git-awesome sync` line commented).

### Symmetry on close (Issues)
A merged PR with `Closes #N` closes the Issue automatically via GitHub. Do not also call `gh issue close`; that races the close-by-PR event and produces double close notifications. If the Issue should stay open for follow-up (e.g., partial fix), edit the PR body to remove the `Closes` keyword and use `Related: #N` instead.

## Minimum Evidence Checklist

For a serious reconcile, gather evidence for:

- all worktrees and nested repos
- all dirty tracked, staged, unstaged, untracked, ignored, submodule, and stash state
- all local, remote, WIP, backup, replace, and tag refs
- all relevant diffs, including rename/mode/binary/whitespace classification
- all sibling/automation clones likely to be ghost sources of truth
- recent git reflog, automation logs, and host-level autosync/timer state
- all open/recent PRs and failing/relevant GitHub Actions runs
- workflow, Dependabot, branch protection, CODEOWNERS, and repo config health
- gitleaks or equivalent secret-scan status
- feature-level code review and test/build/lint validation

## Failure Precedence

When multiple problems exist, report and act in this order:

1. In-progress Git operations: merge, rebase, cherry-pick, revert, bisect, locks.
2. Dirty worktree or index changes, including untracked files.
3. Divergence and tree-equivalence decisions between local/default/upstream refs.
4. Open PR, required-check, review, or Actions failures.
5. Missing or advisory-only hosted-provider protections.
6. Repo policy drift that is not immediately blocking local work preservation.

This ordering prevents automation from "fixing" a policy smell while a repo is
mid-rebase or contains uncheckpointed work.

## Hardcoded Defaults

The framework has zero per-repo configuration. These constants are embedded in
`scripts/bin/git-awesome` and apply uniformly across every managed repo:

| key | value |
|---|---|
| stash slug | `git-awesome/<session-uuid>/<base>/<ts>` (no hostname) |
| events ledger | `<repo>/.artifacts/git-awesome/events.<yyyy-mm-dd>.jsonl` (ECS-shaped JSONL, date-keyed for rotation) |
| patch archive | `<repo>/.artifacts/git-awesome/stash.<uuid>.patch` (flat) |
| baseline | `<repo>/.artifacts/git-awesome/baseline.<session>.tsv` |
| stash TTL | 30 days (`git-awesome gc` drops older) |
| integrate branches | `main`, `master` |
| skip branches | `wip/**`, `scratch/**`, `dependabot/**` |
| required checks | `shell-lint yaml-lint test gitleaks actionlint zizmor workflow-lint` |
| auto-merge gates | `automerge` label OR dependabot patch/minor |
| finalizer | required: `git-awesome guard baseline` at turn start, `git-awesome guard finalize` before handoff |
| cron cadence | `*/15 * * * * /home/wranngle/.dotfiles/scripts/bin/git-awesome sync` |
| host exposure | none — no hostname in stash names, no remote push from autosync |

`.automation/policy.json`, `schemas/automation-policy.v1.json`, `.autosync/*`
markers, ownership leases, the `wip/<agent-kind>/<session-id>/<base>` remote
ref namespace, autosync-driven PRs, and overlay variants (`client` / `external`
/ `repo-default`) were retired 2026-05-12. Pause = `crontab -e` and comment the
cron line. Single escape hatch: `git-awesome --dry-run <subcommand>` demotes
any mutating subcommand to a print-only preview.

## Local Protection Loop (autostash)

`git-awesome sync` runs every 15 minutes via cron. The loop is purely local:
no remote refs are created, no autosync-driven PRs exist, no hostname leaks.

1. **Observe.** Inspect tracked / staged / unstaged / untracked state without
   reading secrets or large diffs.
2. **Autostash.** `git stash push -u -m "git-awesome/<uuid>/<base>/<ts>"`.
   De-dup: if the previous `git-awesome` stash exists and `git diff stash@{0}`
   is empty, skip stash creation and touch the patch file's mtime instead.
   Untracked files are included; ignored files are not.
3. **Archive.** Write the patch to `<repo>/.artifacts/git-awesome/stash.<uuid>.patch`
   (flat, per-repo). The patch survives `git stash drop` and lets the user
   rsync the `.artifacts/` tree offsite for cross-machine backup (out of
   scope for the framework itself). Layout mirrors the canonical artifact
   resolver in `composio-orchestrator/src/artifactPaths.ts`.
4. **Stop.** On semantic conflicts, secrets in the diff, or unsafe Git states
   (merge / rebase / cherry-pick / bisect in progress, lock files present),
   refuse to stash and log the reason to the ledger.

Integration to `main` is the user's normal commit + push flow. The framework
never pushes for the user, never opens PRs from autosync, and never advances
the current branch.

## Universal GitHub Failure Prevention

All generated artifacts pass through the same local contract before they are
written: normalize trailing whitespace, parse by file type, block shellcheck
warnings when shellcheck is installed, block yamllint failures when yamllint
is installed. GitHub Actions confirm the same checks; they should not be the
first place a deterministic bootstrap defect is discovered.

Repository-administration advisory scans (OpenSSF Scorecard, missing branch
protection) are non-blocking. Findings upload SARIF and annotations but must
not fail generated repo-content workflows.

Legacy self-repair or AI-review workflows that create notification loops are
retired to `old/` during bootstrap. Routine policy failures use check
conclusions and labels, not repeated bot comments. Comments are reserved for
durable review findings or security context that cannot be represented as a
check annotation, label, or workflow summary.

Private / free repos may not enforce required checks via branch protection.
In that case, `automerge.yml` gates the PR itself: wait for expected checks,
fail on any observed failing check, require two stable green polls, verify
the PR head SHA is unchanged, then squash-merge. It must not keep pushing
failing repairs into the same branch.

## Finalizer Contract

`git-awesome guard` is the explicit finalization layer. It is not installed
as an ambient prompt hook.

`git-awesome sync` is deliberately conservative: it autostashes local work to
a neutral local stash slot and never mutates the user's current branch. That
protects work, but it does not make an agent finish cleanly.

The guard closes that gap:

1. On prompt start, `git-awesome guard baseline` records a baseline for dirty
   paths and unpushed commit state.
2. On agent stop, `git-awesome guard finalize` scans the same repositories.
3. It ignores dirty paths that already existed and did not change.
4. It blocks newly dirty paths, pre-existing dirty paths changed during the
   turn, and new unpushed commits.
5. It reports whether the repo is managed or out-of-scope.

### Invocation Contract

Call baseline at the start of a bounded agent turn and finalize before handoff:

```sh
GIT_AWESOME_SESSION=<id> $HOME/.dotfiles/scripts/bin/git-awesome guard baseline --scope roots
GIT_AWESOME_SESSION=<id> $HOME/.dotfiles/scripts/bin/git-awesome guard finalize --scope roots
```

Default root scanning covers:

```sh
$HOME/projects:$HOME/.dotfiles
```

Override with `GIT_AWESOME_ROOTS` for another machine layout.

The guard emits NDJSON. Exit `0` means clean, exit `1` means newly dirty or
unpushed agent-owned work remains, and exit `2` means the guard is
misconfigured or the baseline is missing. Missing baseline is a hard failure,
not a silent seed. Finalize never resets, stashes, commits, or pushes.

## Inline `gh-issue` snippet

The retired `scripts/bin/gh-issue.sh` is now an inline bash function in
`~/.agents/AGENTS.md` (and per-repo `.agents/AGENTS.md`). Filing a conventional
Issue: call `gh-issue -t bug|feat|research [-a area] "<description>"`. The
function calls `llm.sh` to render the form body against the canonical headings
in the **Issue + PR Contract** section, then `gh issue create` with the right
`t.<type>` and `triage` labels.

## Why this exists

An AI agent should not rely on memory to commit, push, or open a PR. The system
should make unfinished Git work impossible to miss. The guard does that while
preserving the non-destructive rule: it does not reset, stash, or blindly commit
files it cannot prove are agent-owned.
