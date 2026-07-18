---
name: epic-implementation
description: "Orchestrate delivery of a broken-down epic by planning dependency-aware waves (max three concurrent implementation workstreams), grilling each sub-issue with the navigator, and dispatching implementation subagents under test-driven-development. Keep acceptance-test design and manual testing navigator-led, enforce PR review and CI before merge, and loop through bug-fix sub-issues until manual testing reports zero bugs and the epic is closed."
argument-hint: "Parent epic issue number (e.g. 142)"
---

# Epic Implementation

## Purpose

Take an epic GitHub issue that has already been decomposed into sub-issues (via the `epic-breakdown` skill) and drive it to completion. The orchestrator plans waves of work that respect the epic's dependency map, negotiates the detailed design for each sub-issue with the navigator via `grilling`, and dispatches implementation subagents to work them in parallel — capped at **three concurrent subagents** — each following the `test-driven-development` skill.

Two sub-issue categories are handled specially and are **never dispatched to a subagent**:

- The **acceptance-test design** sub-issue (always the first) is executed by the orchestrator itself in close cooperation with the navigator. The orchestrator authors the design document under `docs/epic-<parent-N>/`, opens the PR, addresses review, and merges it. See step 4a.
- The **manual-testing** sub-issue (always the last, when present) is executed by the navigator alone, on their own machine. The orchestrator only prepares the environment, files bug-fix sub-issues for anything the navigator reports, drives those bug-fix sub-issues through the normal wave flow, and re-opens a fresh manual-test session afterwards. This loops until a manual-test session finds no bugs. See step 8.

This skill does **not** design the decomposition. If the parent issue has no `## Sub-issues` checklist and no dependency map, stop and instruct the navigator to run `/epic-breakdown` first.

## When to Use

Trigger this skill when the navigator asks to:

- "implement / drive / execute / deliver / work through epic #N"
- "start on epic #N — it's been broken down"
- "orchestrate the sub-issues of #N"
- "run the epic plan for #N"

Do **not** use this skill for:

- **Breaking down** an epic — that is `epic-breakdown`.
- **Implementing a single sub-issue by itself** — pick it up directly under `test-driven-development`.
- **Bug fixes** — use `bug-hunter`.
- Issues that do not have the label `epic` — this skill is only for epics that have been broken down into sub-issues.

## Prerequisites

Before doing anything else, verify:

1. `gh` CLI is authenticated (`gh auth status`).
2. Parent issue exists and is readable: `gh issue view <N> --repo rmstdope/memcpy --json number,title,body,labels,state`.
3. Parent issue body contains a `## Sub-issues` checklist **and** a `## Sub-issue dependencies` section (the artifacts produced by `epic-breakdown`). If either is missing, stop and ask the navigator to run `/epic-breakdown` on #N first.
4. Parent issue is `open`. If closed, ask whether to reopen or abort.
5. Working tree is clean (`git status --porcelain` empty). If not, stop and let the navigator commit/stash first — subagents will create branches and cannot start on a dirty tree.
6. Local `main` is up to date: `git fetch origin && git status -sb`. If behind, `git checkout main && git pull origin main` before proceeding.

## Pairing With Other Skills

- **`grilling`** — run before each implementation sub-issue is dispatched, to nail down the detailed implementation approach with the navigator. One question at a time, each with a recommended answer. Also used to co-design the acceptance-test design document with the navigator (step 4a).
- **`test-driven-development`** — every dispatched implementation subagent runs under this skill for RED → GREEN → REFACTOR → COMMIT → PR. After the PR is created it pauses and asks the orchestrator how to proceed (see step 6).
- **Code-review agent** — the orchestrator dispatches this agent after each implementation PR is created. It performs a read-only review of the diff and posts review comments directly on the GitHub PR. Use `code-review` if available; fall back to `rubber-duck`; if neither exists, perform a manual changed-file review from the orchestrator and post the findings as PR comments via `gh pr review --comment`. The orchestrator's own acceptance-test design PR (step 4a) also goes through the code-review agent before merge.
- **`github-issue-designer`** — consulted when the orchestrator files new bug-fix sub-issues from a manual-test session (step 8), and only otherwise if a sub-issue body is missing information the grilling reveals is needed; do not edit sub-issue bodies unless the navigator agrees.
- **`bug-hunter`** — if a subagent uncovers a pre-existing bug that blocks its slice, it should stop and report; the orchestrator surfaces this to the navigator, who decides whether to spawn a bug-fix side-quest. Also referenced (as guidance for style) for bug-fix sub-issues generated by manual testing in step 8; those bug-fix sub-issues themselves still run through this epic-implementation flow as regular implementation sub-issues.

## Procedure

Do **not** dispatch any subagent until the navigator has approved both the wave plan **and** that specific sub-issue's grilled implementation plan. The acceptance-test design sub-issue (step 4a) and the manual-testing sub-issue (step 8) are handled by the orchestrator/navigator directly and never dispatched.

### 1. Load the epic

- Fetch the parent issue: `gh issue view <N> --repo rmstdope/memcpy --json number,title,body,labels,state,assignees`.
- Extract from the body:
  - The `## Sub-issues` checklist — the ordered list of child issue numbers, titles, and checked/unchecked state.
  - The `## Sub-issue dependencies` section — parse into an adjacency map `child_number → [prerequisite_numbers]`.
- For each sub-issue, fetch its current state: `gh issue view <child> --repo rmstdope/memcpy --json number,title,state,labels,assignees,body`.
- Also list any open branches and PRs that reference these sub-issues: `git --no-pager branch -a` and `gh pr list --state open --json number,title,headRefName,body`. A sub-issue with an open PR is considered **in flight**, not pending.

### 2. Classify sub-issue status

Bucket every sub-issue into exactly one of:

- **Done** — issue is `closed`, or the corresponding checklist item is checked, or its PR is merged.
- **In flight** — has an open PR or an open feature branch matching its number.
- **Blocked** — at least one prerequisite in the dependency map is not Done.
- **Ready** — issue is Open, has no in-flight PR/branch, and all prerequisites are Done.

Also tag each sub-issue with its **kind**, derived from title/labels/body:

- `design` — the acceptance-test design sub-issue (produces the `docs/epic-<parent-N>/` design document).
- `implementation` — any vertical implementation slice, or the acceptance-test implementation sub-issue, or a bug-fix sub-issue filed during manual testing.
- `manual-test` — the human-executed manual-testing sub-issue.

Present this summary to the navigator before any wave planning. Use a compact table with columns: `#`, `title`, `kind`, `status`, `blocked-by`.

### 3. Plan the next wave

A **wave** is up to three Ready `implementation`-kind sub-issues to be worked on with subagents in parallel. Rules:

- Cap: **at most 3 subagents concurrently.** If more than 3 sub-issues are Ready, choose the 3 highest-priority ones. Priority order:
  1. The acceptance-test **design** sub-issue (always first, always alone in its wave — it usually unblocks everything else and must be reviewed before slices start). This one is **not dispatched**; it is executed directly by the orchestrator per step 4a.
  2. Sub-issues whose completion unblocks the largest number of downstream siblings.
  3. Sub-issues touching independent areas of the codebase (to minimize merge conflict risk).
  4. Sub-issue number ascending, as a stable tie-break.
- The final **acceptance-test implementation** sub-issue is always alone in its own wave — it depends on every implementation slice.
- The final **manual-testing** sub-issue (when present) is always alone in its own wave — it depends on the acceptance-test implementation sub-issue and every implementation slice. It is **not dispatched**; it is driven by the navigator per step 8. Any `bug-fix` sub-issues it spawns are ordinary implementation sub-issues and go through the normal wave flow (steps 3–7).
- If any In-flight sub-issue count would push the concurrency above 3 when added to this wave, shrink the wave accordingly. Never exceed 3 total concurrent workstreams.

If the only Ready sub-issue is the `design`-kind sub-issue, go to step 4a immediately (no subagent dispatch). If the only Ready sub-issue is the `manual-test`-kind sub-issue, go to step 8 immediately (no subagent dispatch).

Otherwise, present the proposed wave to the navigator with an interactive question, e.g. options:
`["Approve wave", "Change which sub-issues are in the wave", "Reduce wave size", "Pause epic — no wave now"]`.

Do not proceed to grilling until the wave is approved.

### 4a. Execute the acceptance-test design sub-issue (orchestrator + navigator, no subagent)

When the design sub-issue is the current Ready work item, the orchestrator handles it directly in close cooperation with the navigator. Do not dispatch a subagent for this sub-issue.

1. Assign the sub-issue to the navigator (or to the orchestrator user), per the repository's convention.
2. Ensure `main` is fresh (`git fetch origin && git checkout main && git pull origin main`) and create the design branch in the main worktree: `<sub-issue-number>-<slug>`. The design work is document-only, so a dedicated worktree is not required, but the branch must be created from latest `main`.
3. Run the `grilling` skill against the design sub-issue with the navigator to co-author the acceptance-test design. Grill at least: user outcomes to cover, Given/When/Then scenarios, edge cases and failure modes, data/test-vector shapes, UX branches, non-goals, traceability to parent-epic acceptance criteria, and — if the epic has a UI — which surfaces the eventual manual-testing sub-issue must exercise.
4. Write the versioned design document at `docs/epic-<parent-N>/acceptance-test-design.md` (or the path named in the sub-issue). Commit and open a PR referencing the sub-issue.
5. Dispatch the code-review agent against the design PR (same code-review flow as step 6, but the review focuses on scenario coverage, test-vector clarity, and traceability to the parent epic's acceptance criteria — not on production code).
6. Address review comments with the navigator, push, wait for CI green (if any CI runs on docs PRs), and merge the PR yourself using the repository's default merge strategy. Delete the branch.
7. Comment on the design sub-issue with the merged PR URL and the committed document path, then close it: `gh issue close <sub-issue-number> --comment "Design merged in #<pr>. Document: docs/epic-<parent-N>/acceptance-test-design.md."`.
8. Tick the checkbox in the parent epic body and record the outcome in the parent's `## Updates` section.
9. Return to step 2 (re-classify) and step 3 (plan next wave).

### 4. Grill each implementation sub-issue in the wave, one at a time

For each sub-issue in the approved wave, in the order chosen for the wave (design and manual-test sub-issues do not enter this step — they go through 4a and 8 respectively):

1. Announce which sub-issue is being grilled.
2. Read the sub-issue body plus any spec/PRD files it references (`/spec/spec-*.md`, `/docs/PRD.md`).
3. Explore the codebase for the modules the slice will touch **before** asking the navigator anything the code can answer.
4. Run the `grilling` skill against this specific sub-issue. Grill at least these axes, one question at a time, each with a recommended answer:
   - **Test strategy** — which layer(s) get tests (Rust unit, Vitest, integration), what naming, what fixtures.
   - **Public interface** — new Tauri commands, Svelte props/events, IPC types (must be `serde`-compatible).
   - **State ownership** — Svelte 5 runes (`$state`, `$derived`, `$effect`), never wrap Milkdown/editor objects in `$state`, respect the array-index update rule.
   - **Data & storage** — plain `.md` files only, no YAML frontmatter, respect `Journals/` write restrictions, use `plugin-store` for settings and `secrets.json` for secrets.
   - **UX decisions** — no `alert`/`confirm`/`prompt` (use `PromptModal`), custom drag-and-drop only (no HTML5 DnD).
   - **LLM/network paths** — must go through `@tauri-apps/plugin-http` and be capability-declared in `src-tauri/capabilities/default.json`.
   - **Specification updates** — which `spec/spec-*.md` files describe the behavior/contracts touched by this slice, and what must be updated after implementation; if no `spec/` update is expected, capture the explicit rationale.
   - **Definition of done** — which pre-merge checkpoints must pass (`npm run check`, `npm run build`, `cargo clippy -D warnings`, `cargo fmt`, `cargo test --lib`, `npm test`).
   - **Risk / unknowns** — the riskiest part of this slice, and whether the RED test can be aimed straight at it.
5. Stop grilling when a further question would not change the implementation. Summarize the resolved decisions into a **Design Brief** for this sub-issue (see template below).
6. Present the Design Brief to the navigator with options like:
   `["Approve brief — ready to dispatch", "Revise brief", "Re-grill a specific area", "Skip this sub-issue for now"]`.

Only sub-issues with an approved Design Brief make it into the dispatch batch. If the navigator revises the wave composition during grilling, restart step 3 for the new wave.

### 5. Dispatch the wave

Once every sub-issue in the wave has an approved Design Brief:

- Fire **all** subagents in the wave in a **single turn**, by making up to three parallel `runSubagent` calls in the same tool block. Do not dispatch them sequentially across turns — that defeats the concurrency cap's intent.
- Choose an appropriate subagent (default is the current agent). Use the `Explore` subagent only for pure read-only investigation offshoots, never for implementation.
- **Always pass `model: "Auto (copilot)"`** to every implementation `runSubagent` call, regardless of the model the orchestrator is running on. Implementation subagents must run on Auto — do not omit the `model` parameter (which would inherit the orchestrator's model) and do not pin a specific model. This applies to every dispatch in this step and to the re-dispatch in step 7.
- Every repository-writing implementation subagent must work in its **own git worktree**, created from the latest `main` for its issue branch. The main orchestrator worktree must stay untouched so parallel subagents cannot overwrite each other's checkouts or dirty state. The subagent prompt must name the worktree path convention, for example `../memcpy-worktrees/<sub-issue-number>-<slug>`, and must tell the subagent to verify `pwd`, `git worktree list`, and `git status -sb` before every git phase. If an existing worktree already owns the branch, the subagent must reuse it or report the conflict; it must not force-remove another worktree.
- Each subagent's prompt must contain, verbatim:
  - The Design Brief from step 4.
  - The sub-issue number, title, and full body.
  - The parent epic number.
  - Explicit instruction: _"Assign yourself to the sub-issue. Create or reuse a dedicated git worktree for this sub-issue at `../memcpy-worktrees/<sub-issue-number>-<slug>` and create a branch from latest `main` named `<sub-issue-number>-<slug>` inside that worktree. Verify `pwd`, `git worktree list`, and `git status -sb` before every git phase, and never perform repository-writing work in the orchestrator's main worktree. Follow the `test-driven-development` skill for RED → GREEN → REFACTOR → COMMIT → PR. Work autonomously without stopping at phase gates. As part of the implementation, inspect the relevant `spec/spec-*.md` files identified in the Design Brief and update every specification that must change to reflect the implemented behavior, contracts, UX, storage, or quality-process changes. If no `spec/` file needs an update, state the reason explicitly in the PR body and in your final return. After the PR is created and all pre-merge checkpoints (`npm run check`, `npm run build`, `cd src-tauri && cargo clippy --all-targets -- -D warnings`, `cd src-tauri && cargo fmt`, `cd src-tauri && cargo test --lib`, `npm test`) pass, **stop and return control to the orchestrator**. Return the PR number, PR URL, branch name, worktree path, a short summary of what was implemented, and the `spec/` files updated or the no-update rationale. Do not address review comments yet, do not merge — the orchestrator will send you back in for those steps."_
  - The list of pre-merge checkpoints from the repository's `copilot-instructions.md`.
  - The reminder to verify the correct dedicated git worktree before any git operation, and to check for open sibling feature branches before branching from `main`.

While the wave is running, do not start grilling the next wave — the orchestrator has no useful work to do until the wave returns, and starting the next grilling would risk stale assumptions about the codebase.

### 6. Collect wave results and dispatch code review

When the parallel `runSubagent` calls return:

- **Let every sibling in the wave finish** before acting — subagents run in parallel in one turn and cannot be cancelled mid-flight. Present all wave results together, not one at a time.
- For each returned result, **verify** rather than trust: read the actual PR (`gh pr view <n>`), confirm the branch exists on origin, and confirm the pre-merge checks all pass. A subagent's reply describes what it intended to do; the PR is ground truth.
- For each returned result, verify that the PR either updates the relevant `spec/spec-*.md` files for the implemented changes or documents a credible "no spec update needed" rationale in the PR body. If neither is true, treat the PR as incomplete and send it back to the implementing subagent before review.
- If any subagent failed (compile error, test failure, hit a design fork), summarize the failure alongside its siblings' successes and give the navigator options:
  `["Re-dispatch same sub-issue with revised brief", "Re-grill this sub-issue", "Escalate to bug-hunter", "Skip and re-plan wave", "Abort epic run"]`.
- If any subagent stopped because it uncovered a scope gap that changes another sibling's plan, pause the whole epic run and return to step 2 to re-classify.

For each successful PR in the wave, **dispatch a code-review subagent**. Reviews may run in parallel across the wave (they do not count toward the 3-concurrent implementation cap because they are the natural next step of an already-paused implementation workstream — each sub-issue is still one workstream). The review-agent prompt must contain:

- The PR number and URL.
- The sub-issue number, title, body, and its Design Brief.
- Explicit instruction: _"Perform a code review of PR #<n>. Focus on the diff only. Check for: correctness against the Design Brief and sub-issue acceptance criteria, clean-code violations, missed edge cases, adherence to the repository's framework decisions in `.github/copilot-instructions.md` (Svelte 5 runes rules, Milkdown editor rules, LLM plugin-http rules, no `alert`/`confirm`/`prompt`, no HTML5 DnD, plain-markdown storage), and whether the relevant `spec/spec-*.md` files were updated to reflect all implementation changes. If no spec update is present, verify that the PR body contains a credible no-update rationale; otherwise post an actionable review comment requiring the missing spec update. Post every actionable finding as an inline PR review comment via `gh pr review --comment` or `gh api`. When done, return a summary: number of comments posted, severity breakdown (blocker / suggestion / nit), whether spec coverage is adequate, and whether the PR is safe to merge after comments are addressed."_

Use the `code-review` subagent if available; fall back to `rubber-duck`; if neither exists, perform the review from the orchestrator itself and post findings via `gh pr review --comment`.

### 7. Send the implementing subagent back to address review comments and merge

After the review agent returns for a PR:

- If the review found **zero blockers and zero suggestions** (only nits or nothing), summarize to the navigator and ask:
  `["Skip straight to merge", "Address nits first", "Hold — I want to review manually"]`.
- Otherwise, dispatch the **original implementing subagent** back in to address comments. Pass `model: "Auto (copilot)"` to this `runSubagent` call as well — the model rule from step 5 applies to every re-dispatch of an implementation subagent. The prompt must contain:
  - The PR number, URL, and branch name.
  - The dedicated worktree path used by the implementing subagent, or an instruction to recreate/reuse the branch's worktree at the same convention (`../memcpy-worktrees/<sub-issue-number>-<slug>`) before making repository changes.
  - The Design Brief (unchanged from step 4).
  - Explicit instruction: _"Reopen work on branch `<branch>` in its dedicated git worktree; verify `pwd`, `git worktree list`, and `git status -sb` before changing files. Fetch all review comments on PR #<n> (`gh pr view <n> --comments` plus `gh api repos/:owner/:repo/pulls/<n>/comments`). For each comment: address it in code/docs/specs, then reply to the comment on GitHub acknowledging the fix (per `test-driven-development`'s MERGE-phase guidance). Before pushing, re-check the relevant `spec/spec-*.md` files and update them for any implementation changes made while addressing review; if no spec update is needed, ensure the PR body still contains a credible no-update rationale. Re-run every pre-merge checkpoint (`npm run check`, `npm run build`, `cd src-tauri && cargo clippy --all-targets -- -D warnings`, `cd src-tauri && cargo fmt`, `cd src-tauri && cargo test --lib`, `npm test`) unfiltered and confirm all pass. Push. Wait for CI to go green on the pushed commit (`gh pr checks <n> --watch`). Once CI is green, every review thread has a reply, and the spec update/no-update rationale is present, **merge the PR yourself** using `gh pr merge <n> --squash --delete-branch` (or the repo's default merge strategy). Close the sub-issue: `gh issue close <sub-issue-number> --comment "Delivered via #<n>."`. Return the merge commit SHA, confirmation that the branch was deleted, whether the dedicated worktree was removed or intentionally left, and the `spec/` files updated or the no-update rationale."_

Merge sequencing within a wave:

1. If two PRs in the same wave touch overlapping files, do not send both address-comments subagents in parallel. Merge them one at a time: dispatch the first, wait for merge, then dispatch the second (which must first rebase onto the updated `main` before pushing and merging).
2. If they are fully independent, the address-comments subagents can run in parallel.

After each successful merge (confirmed by the returning subagent and cross-checked with `gh pr view <n> --json state,mergedAt`):

- Verify the sub-issue is closed (`gh issue view <sub-issue-number> --json state`).
- Tick the checkbox next to that sub-issue in the parent epic body (`gh issue edit <parent-N> --body-file <edited>`).
- Record in the parent epic's `## Updates` section which `spec/` files were updated for the sub-issue, or the explicit reason no specification update was needed.
- Confirm the local and remote branch are gone (respect the "branch checked out in another worktree" caveat from `test-driven-development` — if a worktree owns the branch, report it but do not force-delete).

### 8. Loop until the epic is done

After every merge, return to step 2 (re-classify), then step 3 (plan next wave). Continue until every sub-issue except the manual-testing sub-issue (if present) is Done.

Once the acceptance-test implementation sub-issue is merged and the manual-testing sub-issue is the only Ready sub-issue left, hand control to the navigator per **step 8a**.

### 8a. Manual-testing sub-issue (navigator-only, iterative bug-fix loop)

The manual-testing sub-issue is executed by the navigator on their own machine. The orchestrator does **not** dispatch any subagent for it and does **not** try to automate any of its steps.

1. Confirm the sub-issue is assigned to the navigator (assign it if not).
2. Ensure the local checkout is on the fully merged `main` (`git checkout main && git pull origin main`) so the navigator tests against the integrated epic. Report which merge commit represents "the epic as delivered".
3. Point the navigator at the manual-test plan document referenced by the sub-issue (typically `docs/epic-<parent-N>/manual-test-plan.md`, containing the scripted checklist + exploratory charters).
4. Instruct the navigator to run one full **test session** (scripted checklist + at least one exploratory charter, per the plan) and report back with:
   - Which scripted items passed / failed.
   - Notes from exploratory charters.
   - A structured list of any bugs found (one entry per bug: user-visible symptom, steps to reproduce, expected vs actual, severity).
   - The environment (OS, build/commit tested).
5. Post a summary comment on the manual-testing sub-issue for this session, capturing the results verbatim. Prefix the comment with `Manual-test session N — <date>` so successive sessions are distinguishable.
6. Branch on the result:

   **a. If the navigator reports zero bugs from this session:**
   - Confirm with the navigator that the manual test pass is complete (`["Close manual-testing sub-issue and epic", "One more session first", "Re-scope the plan"]`).
   - On confirmation, close the manual-testing sub-issue: `gh issue close <manual-test-#> --comment "Manual-test session N found no bugs. Closing."`, tick the checkbox in the parent epic body, and proceed to step 9 (close the epic).

   **b. If the navigator reports one or more bugs from this session:**
   - For each reported bug, file a new **bug-fix sub-issue** using the `github-issue-designer` skill's template. Each bug-fix sub-issue must:
     - Have title prefix `Sub-issue (<parent-N>): Fix <short bug description>`.
     - Include a `Parent: #<parent-N>` line and reference the manual-testing sub-issue that surfaced it (`Found in: manual-test session N of #<manual-test-#>`).
     - Include steps to reproduce, expected vs actual behavior, severity, and any relevant environment info.
     - Carry labels `bug` and `enhanced`. Do **not** apply the `epic` label.
     - Not be assigned at creation (assignment happens at pickup).
   - Link each bug-fix sub-issue to the parent epic (`gh issue-child-add <parent-N> <bug-fix-#>` if the extension is present, otherwise append to the parent's `## Sub-issues` checklist).
   - Update the parent epic body's `## Sub-issues` checklist to include the new bug-fix entries, and update the `## Sub-issue dependencies` map: the manual-testing sub-issue now additionally depends on every new bug-fix sub-issue.
   - Update the manual-testing sub-issue body (or comment) with a `Blocked by:` list of the new bug-fix sub-issue numbers.
   - Do **not** close the manual-testing sub-issue — it stays Open and becomes Blocked until all new bug-fix sub-issues are Done.
   - Return to step 2. The bug-fix sub-issues are ordinary implementation sub-issues and go through the normal wave flow (3 → 4 → 5 → 6 → 7). They may be grouped into waves under the concurrency cap just like any other implementation slice.
   - Once every new bug-fix sub-issue is merged and closed, the manual-testing sub-issue becomes Ready again — restart step 8a with a **fresh test session** (session N+1). Do not skip the session; the fix might have missed something or introduced a regression.

Repeat step 8a until a test session finds no bugs and the manual-testing sub-issue is closed. Then — and only then — proceed to step 9.

### 9. Close the epic

When every sub-issue is Done (including the manual-testing sub-issue, which is only closed after a clean session per step 8a):

- Update the parent epic body's `## Updates` section with a short summary of what shipped, referencing each merged PR and every manual-test session that was run (including bugs found and their fix PRs).
- Close the parent epic: `gh issue close <N> --repo rmstdope/memcpy --comment "All sub-issues merged and manual testing passed. Epic delivered."`.
- Run the **Iteration Retrospective Gatherer** agent on the completed epic (not per-PR — one retro for the whole epic).
- Report to the navigator: number of waves, total sub-issues delivered (including bug-fix sub-issues spawned from manual testing), total PRs merged, number of manual-test sessions run, any deferred follow-ups, and any newly-discovered scope that should become a fresh issue.

## Design Brief Template

Every Design Brief handed to a subagent must have this exact shape:

```md
# Design Brief — Sub-issue #<N>: <title>

## Parent epic

#<parent-N> — <parent title>

## Slice outcome (one line)

<user-visible outcome this slice delivers>

## Grilled decisions

- Test strategy: <Rust unit | Vitest | integration | ...> — <file locations, naming>
- Public interface: <Tauri commands / Svelte props / IPC types>
- State ownership: <runes used, editor object placement, array-index rules>
- Data & storage: <files touched, storage location, invariants>
- UX decisions: <modal, drag-and-drop, dark mode, etc.>
- LLM/network paths: <plugin-http usage, capability entries>
- Specification updates: <relevant `spec/spec-*.md` files and expected changes, or explicit no-update rationale>
- Definition of done: <exact checkpoints that must pass>
- Risk / unknowns: <riskiest part, and how the first RED test targets it>

## Files expected to change

- <relative path> — <why>

## Out of scope

- <thing that could reasonably be part of this slice but is deferred, and to which sibling sub-issue>

## Acceptance criteria (copied from sub-issue)

- [ ] <criterion 1>
- [ ] <criterion 2>

## Pre-merge checkpoints (must all pass before PR)

- `npm run check`
- `npm run build`
- `cd src-tauri && cargo clippy --all-targets -- -D warnings`
- `cd src-tauri && cargo fmt`
- `cd src-tauri && cargo test --lib`
- `npm test`
```

## Specification update rule

Every sub-issue PR must keep the repository specifications under `spec/` synchronized with the implementation it delivers:

- During grilling, identify the relevant `spec/spec-*.md` files and expected updates before dispatch.
- During implementation, update every affected `spec/` file in the same PR as the code or design change.
- If a sub-issue genuinely does not affect any specification, the PR body and subagent return must state the no-update rationale explicitly.
- During review, missing spec updates or missing no-update rationales are actionable findings.
- Before merge, verify that the PR contains either the relevant `spec/` changes or the explicit no-update rationale.

## Concurrency Rules (hard limits)

- **Never** more than 3 sub-issue workstreams in flight at once. A workstream is a sub-issue in any stage from dispatch through merge (implementation, review, address-comments). Unmerged PRs count. The orchestrator's own work on the acceptance-test design sub-issue (step 4a) counts as one workstream while it is in flight. The navigator's manual-test session (step 8a) does **not** count against the cap because it is executed off-agent by the human.
- **Code-review agents do not add** to the cap — they are the paused implementation workstream's next serialized step, not a new workstream.
- **Never** dispatch a sub-issue whose prerequisites are not all Done.
- **Never** dispatch the acceptance-test design sub-issue to a subagent — the orchestrator authors it with the navigator (step 4a).
- **Never** dispatch the manual-testing sub-issue to a subagent, and never attempt to execute the manual-test plan from the orchestrator — it is run by the navigator on their machine (step 8a).
- **Never** dispatch the acceptance-test implementation sub-issue while any implementation slice is still In-flight or unmerged.
- **Never** start the manual-testing sub-issue while any implementation slice or the acceptance-test implementation sub-issue is still unmerged, and never start a new manual-test session while any bug-fix sub-issue from a previous session is still unmerged.
- **Never** run a fresh grilling session for a sub-issue that is already In-flight.
- **Never** let two concurrent subagents branch from the same base if they will touch overlapping files — either sequence them into separate waves or have the later one branch from the earlier one's feature branch (and note the dependency).
- **Never** dispatch two address-comments subagents in parallel against overlapping files — merge them one at a time.
- **Never** merge without CI green on the pushed commit and every review comment replied to.
- **Never** dispatch an implementation subagent without `model: "Auto (copilot)"`. Implementation and address-comments subagents always run on Auto, no matter what model the orchestrator is running on. The code-review agent and the retrospective agent are not covered by this rule — they use their own model configuration.

## Anti-patterns

- **Dispatching the acceptance-test design sub-issue to a subagent** — that sub-issue is co-authored by the orchestrator and the navigator (step 4a). Subagent dispatch would lose the interactive design conversation with the navigator.
- **Dispatching the manual-testing sub-issue to a subagent, or attempting to "simulate" the manual-test plan from the orchestrator** — the whole point is a human running the software; the orchestrator only supports the loop.
- **Auto-closing the manual-testing sub-issue after filing bug-fix sub-issues** — the manual-testing sub-issue must stay Open, become Blocked on the new bug-fix sub-issues, and be resumed with a fresh session once they merge. Only a clean session (zero bugs) closes it.
- **Skipping the fresh manual-test session after bug fixes** and declaring the epic done — the fixes may have missed the bug or introduced a regression; a new session is mandatory.
- **Filing manual-test bugs as a batch comment on the manual-testing sub-issue only, without creating separate bug-fix sub-issues** — each bug must be a trackable sub-issue with its own PR, review, and merge, so the epic's history stays auditable.
- **Dispatching without grilling** — skipping detailed design and letting the subagent invent it produces slices that diverge from what the navigator wants and get re-worked.
- **Grilling all sub-issues up front, then dispatching everything at once** — decisions made now may be invalidated by what earlier waves reveal. Grill wave-by-wave.
- **Dispatching serially in separate turns to "stay under 3"** — the cap is 3 _concurrent_, not 3 _ever_. Batch them into one turn.
- **Skipping the code-review step and going straight from PR to merge** — the review agent is a required part of every implementation sub-issue's workstream (including the orchestrator's own design PR in step 4a), not optional.
- **Shipping implementation changes without synchronized `spec/` updates** — every sub-issue PR must update relevant `spec/spec-*.md` files or explicitly justify why no spec update is needed.
- **Merging before CI is green on the pushed commit** — the address-comments subagent must wait for `gh pr checks --watch` to succeed before merging.
- **Merging before every review comment has a reply** — reviewers must be able to see what was done for each thread.
- **Trusting subagent self-reports** — always verify with `gh pr view`, `gh issue view`, `git log`, and actual checkpoint output.
- **Skipping re-classification after a merge** — sub-issues that were Blocked may now be Ready, and the next wave depends on that.
- **Starting a new wave while the previous wave has unmerged PRs** — this violates the concurrency cap (in-flight PRs count as workstreams).
- **Editing sub-issue bodies mid-flight** based on grilling outcomes — the Design Brief lives in the subagent prompt, not the issue body. Only update the issue if the navigator explicitly asks. (Exception: the manual-testing sub-issue body is updated in step 8a to track the current blocking bug-fix sub-issues.)
- **Silently dropping a failed subagent** — surface every failure with options; never re-plan around it without navigator input.
- **Dispatching a different subagent to address review comments** than the one that implemented the slice — the original subagent has the full mental model of the implementation. Re-dispatch a fresh subagent only if the original is unavailable or the navigator explicitly asks.

## Related Skills

- `epic-breakdown` — required prerequisite. Produces the sub-issues and dependency map this skill consumes.
- `grilling` — invoked once per sub-issue before dispatch.
- `test-driven-development` — the workflow every dispatched subagent runs under.
- `github-issue-designer` — consulted only if a sub-issue body needs a documented update mid-flight.
- `bug-hunter` — escalation path when a subagent uncovers a defect that blocks its slice.
