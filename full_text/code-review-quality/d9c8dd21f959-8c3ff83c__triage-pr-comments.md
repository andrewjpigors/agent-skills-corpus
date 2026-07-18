---
name: triage-pr-comments
description: >
  Use when a PR has review comments (from Copilot, teammates, or external
  reviewers) that need structured triage and end-to-end resolution. Evaluates
  every comment thread, auto-fixes everything that does not require a
  load-bearing operator decision, walks the operator through only the
  decisions that genuinely need human judgment, then implements, commits,
  pushes, replies in-thread (machine-readable), resolves the threads it
  fixed, and reports.

  Not for: draft PRs with no comments, self-review of your own code,
  or PRs where all comments are already resolved. Not a code review tool —
  use review-local or start-pr-cycle for that.
license: MIT
compatibility: Requires git, gh (GitHub CLI), and jq.
argument-hint: "#<pr-number>"
metadata:
  author: Acatl
---

# PR Comment Triage + Auto-Resolve

End-to-end PR review-comment resolution. Argument: `/triage-pr-comments #21`. If no number given, infer from current branch. If that fails, list open PRs and ask.

---

You are a Principal Engineer resolving PR review comments. Goal: every valid finding gets fixed, every invalid finding gets refuted, every ambiguity that affects repo direction surfaces to the operator. Default bias is **correctness, not scope**.

**Operating principles (read first — they override defaults):**

1. **Correctness over PR scope.** A valid finding gets fixed even if it lives outside the PR's stated scope. There is no "OUT OF SCOPE — defer to issue" verdict. If the finding is real, fix it in this PR. The only reason to defer is when the fix itself requires a load-bearing decision the operator must make.
2. **Auto-fix is the default.** For findings with a clear correct answer (typo, missing guard, wrong type, dead code, off-by-one, missing test, doc drift, broken link, lint violation, obvious refactor with no public-contract impact) — implement immediately, no prompt.
3. **Only walk the operator through decisions that genuinely need judgment.** See "Decision Gate" below. Everything else proceeds silently.
4. **One plan-approval gate, then autonomous.** After analysis, present the findings + the plan and get a single approval of the overall assessment (Phase 5e). Never analyze-then-execute in one hit. After approval, run end-to-end with no per-step gates — implement → verify → commit → push → reply → resolve → report — stopping only for a real mid-flight decision (cascading Decision-Gate hit) or a hard-gate failure.
5. **Replies are machine-readable.** No prose, no gratitude, no human-style explanation. Terse tagged format. See "Reply Format".

---

## When to Use

- PR has review comments that need resolution
- User invokes `/triage-pr-comments` with or without a PR number
- PR received `CHANGES_REQUESTED` and user wants the round closed out

**Not for:** Draft PRs with no comments, self-review of your own code, PRs where all threads are already resolved.

---

## Decision Gate — when to ask the operator

**The gate is a positive test, not a negative one.** Default is AUTO-FIX. A finding moves to DECISION-NEEDED **only** when at least one of the criteria below clearly applies. If you cannot name the specific criterion, the finding stays AUTO-FIX. "Might be load-bearing" is not enough.

### Decision-needed (ask)

A finding requires operator decision **only** if at least one is true:

- **Public contract change**: modifies an exported API, response DTO shape, route shape, CLI flag, or any symbol re-exported from a package's public entry module (e.g. `index.ts`, `mod.rs`, `__init__.py`)
- **Schema / migration**: changes DB schema, adds/removes a column, alters a migration's behavior, changes default values for existing rows
- **Architectural pattern**: introduces a new abstraction, a new dependency, a new directory pattern, or contradicts a load-bearing convention in `CLAUDE.md` / `.claude/rules/*`
- **Load-bearing config**: touches build/compiler config, deploy manifests, CI workflows, lockfiles, or root dependency manifests (e.g. `tsconfig.json`, `render.yaml`, `nx.json`, `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml` — substitute your stack's equivalents)
- **Equally-correct paths with different long-term tradeoffs**: two or more fixes are both technically correct, ecosystem has no obvious default, and the choice locks in downstream code shape
- **Reviewer contradicts an existing project standard**: requires either declining with a rationale citation, or updating the standard
- **Irreversible or destructive**: deletion, rename of a public symbol, breaking change

### NOT decision-needed (auto-fix without asking)

These are AUTO-FIX even though they touch real code. The specific cases below are **illustrative examples from a TypeScript/Node/Express stack — substitute your own stack's equivalents**. The *category* is what triggers AUTO-FIX, not the exact syntax:

- Typo, grammar, comment fix, doc drift, broken link
- Missing null/undefined guard, missing array-bounds check, off-by-one
- Wrong type annotation, missing return type, `any` narrowing
- Missing test for behavior just introduced; missing assertion in existing test
- Dead code removal, unused import, unused variable, unreachable branch
- Lint violation, formatter divergence, MD040/MD032 fix
- Microcopy / error-message wording (when the contract code stays stable)
- Regex tightening (e.g., `parseInt` → strict regex per project rule)
- Adding a `const`, narrowing a type, extracting a local variable
- Mapper fixes (e.g., `Date` → ISO 8601 string), missing `toISOString()`
- Race-condition guard inside an existing transaction
- Adding `Cache-Control: private` to per-user response
- Replacing `new Error(...)` with the project's typed exception subtype
- Adding `asyncHandler`, `mergeParams: true`, missing middleware that the project rule prescribes
- Reordering imports, fixing import path style (no `.js` extensions per project rule)
- Filling a missing OpenAPI registration when the pattern is already established
- Any change that, if rolled back, is a 1-commit revert with no downstream consequences

**Rule of thumb:** if the fix has one obviously-correct form that any senior engineer would write the same way, it is AUTO-FIX — regardless of how many files it touches. Volume is not gate-triggering; ambiguity is.

---

## Verdict Vocabulary

| Verdict           | Meaning                                                                                | Path           |
| ----------------- | -------------------------------------------------------------------------------------- | -------------- |
| AUTO-FIX          | Valid finding with a clear correct answer. Fix without asking.                         | Implement      |
| DECISION-NEEDED   | Valid finding, fix requires operator judgment per the Decision Gate above.             | Walk operator  |
| DECLINE           | Reviewer is technically wrong, contradicts a load-bearing standard, or proposes YAGNI. | Reply, resolve |
| ALREADY ADDRESSED | Issue already fixed in current code or thread already resolved.                        | Resolve        |
| UNCLEAR           | Comment too vague to act on; cannot infer intent.                                      | Reply + ask    |

There is no OUT OF SCOPE. A real finding gets fixed; a non-finding gets declined; an unfixable-without-judgment finding becomes DECISION-NEEDED.

---

## Execution Strategy

```text
Main agent
    │
    ├── Announce: "Triaging PR #N — fetching comments and analyzing."
    │
    ├── Phase 1.5: Pre-flight git state check (main agent — HARD GATE; abort on failure)
    │
    └── Sub-agent → Phases 1–4 (read-only data fetch + analysis)
            │
            │   Phase 1: Resolve PR, fetch metadata, diff, linked issues, scope
            │   Phase 2: Fetch all comment threads + thread IDs (GraphQL), apply idempotency filter
            │   Phase 3: Read project standards (CLAUDE.md, .claude/rules/*) + derive check commands
            │   Phase 4: Per-thread verdict assignment (fan out to nested sub-agents when N > 10)
            │       → returns: per-thread block with verdict, fix plan, thread ID, blocker
            │
    ├── Receive results
    │
    ├── Phase 5: Overview + emoji thread table + Decision wizard (ONLY DECISION-NEEDED items)
    │       └── 5e PLAN-APPROVAL GATE (always — the one intentional stop; wait for approval)
    │
    └── Phase 6: Execute end-to-end
            ├── Implement (fan out: one sub-agent per independent batch, in parallel)
            ├── Typecheck / lint / test (per Phase 3a-derived commands)
            ├── Commit (semantic message, race-check against START_SHA)
            ├── Push (capture CI run URL)
            ├── Reply in-thread (REST for ≤20, aliased GraphQL for >20; machine-readable + signature)
            ├── Dismiss stale bot reviews
            ├── Resolve every thread that was fixed / declined / already
            └── Final report (counts, decisions, CI URL, failures with retry commands)
```

---

## Phase 1: Resolve PR and Determine Scope

> **Transparency:** *"Resolving PR and fetching metadata, linked issues, and diff…"*

1. **Resolve PR number** in order: explicit arg → `gh pr view --json number --jq '.number'` → list `gh pr list` and ask.
2. Validate and fetch:

   ```bash
   gh pr view <number> --json number,title,headRefName,url,author,state,reviewDecision,body,baseRefName
   ```

3. Fetch repo coordinates for later GraphQL calls:

   ```bash
   gh repo view --json owner,name --jq '{owner: .owner.login, name: .name}'
   ```

4. **Linked issues**:

   ```bash
   gh pr view <number> --json closingIssuesReferences --jq '.closingIssuesReferences[]'
   ```

5. **Diff**:

   ```bash
   gh pr diff <number> --name-only
   ```

6. **Scope statement**: derive from linked issue → PR title/description → diff. Recorded for context only — scope does not gate fixes (see operating principle #1).

---

## Phase 1.5: Pre-flight Git State Check (HARD GATE)

> **Transparency:** *"Pre-flight: verifying local git state matches PR branch…"*

Runs before any analysis. If any check fails, **abort the skill** with a one-line error and the exact command to fix. Do not silently continue or "best-effort" around dirty state.

1. **Current branch matches PR head**:

   ```bash
   git branch --show-current
   ```

   Must equal `headRefName` from Phase 1. If not, abort: `error: on branch <X>, PR is on <Y>. checkout <Y> first.`

2. **Working tree clean of unrelated changes**:

   ```bash
   git status --porcelain
   ```

   Must be empty. If not, abort: `error: uncommitted changes in <files>. commit/stash before running.` This prevents bundling operator's in-progress work into the auto-commit.

3. **Branch synced with origin**:

   ```bash
   git fetch origin <branch>
   git rev-list --count HEAD..origin/<branch>
   ```

   Result must be `0`. If non-zero, abort: `error: behind origin/<branch> by N commits. pull first.` Avoids the skill committing on top of a stale tree and force-pushing later.

4. **Capture start SHA for race detection**:

   ```bash
   git rev-parse HEAD
   ```

   Store as `START_SHA`. Phase 6c re-checks before commit; if HEAD moved (operator pushed concurrently), abort and report what changed.

5. **Confirm gh authenticated user** (used by Phase 2 idempotency filter):

   ```bash
   gh api user --jq '.login'
   ```

   Store as `GH_USER`.

---

## Phase 2: Fetch Comments + Thread IDs

> **Transparency:** *"Fetching comment threads and resolution state…"*

**Repo coordinates**: Use `OWNER` and `NAME` captured in Phase 1 step 3 — do not call `gh repo view` again. Throughout Phase 2 and Phase 6, the literal `$OWNER/$NAME` (or `{owner}/{repo}` in templates) substitutes those values; the skill never re-fetches them.

**Shell/jq safety**: Use `select(.body | length > 0)` — never `select(.body != "")`. The `!=` form occasionally corrupts to the Unicode not-equal char and fails jq parse.

### 2a. Inline Review Comments

```bash
gh api repos/$OWNER/$NAME/pulls/<number>/comments --paginate \
  | jq '[.[] | {id, path, line, body, user: .user.login, in_reply_to_id, diff_hunk}] | map(select(.body | length > 0))'
```

### 2b. Top-Level Review Bodies

```bash
gh api repos/$OWNER/$NAME/pulls/<number>/reviews --paginate \
  | jq '[.[] | {id, body, state, user: .user.login}] | map(select(.body | length > 0))'
```

### 2c. Issue-Level Conversation Comments

```bash
gh api repos/$OWNER/$NAME/issues/<number>/comments --paginate
```

### 2d. Review Threads — IDs and resolution state (GraphQL)

Needed to resolve threads later via `resolveReviewThread`. Map each root comment `databaseId` → GraphQL `threadId`:

```bash
gh api graphql -f query='
  query($owner:String!, $name:String!, $number:Int!) {
    repository(owner:$owner, name:$name) {
      pullRequest(number:$number) {
        reviewThreads(first:100) {
          nodes {
            id
            isResolved
            isOutdated
            comments(first:1) { nodes { databaseId } }
          }
        }
      }
    }
  }' -F owner=<owner> -F name=<name> -F number=<number>
```

### Processing

1. **Thread replies**: group inline comments by `in_reply_to_id` to form threads.
2. **Detect already-resolved on GitHub**: if GraphQL says `isResolved: true`, mark **ALREADY HANDLED** and **skip entirely** — no reply, no resolve, no entry in the wizard table beyond a single counted line in the report. ("ALREADY HANDLED" is a processing state, not a verdict — distinct from ALREADY ADDRESSED below.)
3. **Detect prior agent reply (idempotency)**: scan every comment in the thread for an existing reply authored by the gh-authenticated user (`gh api user --jq '.login'`) **whose body contains the trailer `[claude-code:audit-pr-comments]`**. If present, treat the thread as already handled by a prior run — skip entirely (no new reply, no re-resolve attempt). Counts toward "already handled by prior run" in the report.
4. **Detect human-acknowledged closure**: if the thread shows reviewer-acknowledged closure ("done", "thanks", "addressed", "lgtm now"), mark **ALREADY ADDRESSED** — flows through 6e/6f with an `already:` reply and resolve.
5. **Filter noise**: skip pure LGTMs, bot status updates, empty review bodies.
6. **Deduplicate**: if a review body repeats inline comments, keep the inline (has file context).
7. **Group related**: same underlying issue across multiple comments → single finding, multiple locations.
8. **Carry `threadId`** through to every finding so Phase 6 can resolve it.

**Idempotency contract**: rerunning the skill on the same PR with no new comments since the prior run must be a no-op (zero new replies, zero new resolves, zero commits). Verify this by checking the report after a second run shows all threads as "already handled by prior run".

---

## Phase 3: Read Project Standards + Derive Check Commands

> **Transparency:** *"Reading project standards and conventions…"*

Read in parallel:

1. `CLAUDE.md` (project + any nested per-app `CLAUDE.md` the diff touches)
2. `.claude/rules/*.md` matching the files in the diff
3. Architecture docs referenced by `CLAUDE.md` (e.g. `docs/architecture.md`, `docs/architecture-principles.md`)
4. `package.json` scripts at repo root (and at any workspace root the diff touches)

These are authority. A reviewer that contradicts them gets DECLINE (with rationale) unless the comment identifies a genuine bug in the standard itself — in which case DECISION-NEEDED (the standard may need to change).

### 3a. Derive verify commands

Phase 6b runs verification against this project. Derive commands now — do not hardcode any project name, and do not assume a specific language or toolchain. Detect from what the repo actually contains.

Resolution order (first that exists wins; may produce multiple commands):

1. **Explicit instruction in `CLAUDE.md` / README / CONTRIBUTING**: a "How to run tests / typecheck / lint" section or equivalent. Use the exact commands stated. Highest authority — overrides every heuristic below.
2. **Task runner / manifest present**: detect the repo's toolchain and run its typecheck/lint/test targets. Examples by ecosystem — substitute the one the repo actually uses:
   - JS/TS monorepo: `npx nx affected -t typecheck lint test` (`nx.json`), `npx turbo run typecheck lint test` (`turbo.json`)
   - JS/TS package: the first matching `package.json` script for `typecheck`/`type-check`/`tsc`, `lint`, `test`, via `npm run <script>`
   - Rust: `cargo check`, `cargo clippy`, `cargo test` (`Cargo.toml`)
   - Go: `go vet ./...`, `go test ./...` (`go.mod`)
   - Python: the configured tools — `mypy`/`pyright`, `ruff`/`flake8`, `pytest` (`pyproject.toml`, `tox.ini`)
   - Make / Just: `make lint test` / `just lint test` when those targets exist (`Makefile`, `justfile`)
3. **Fallback**: run only the test command you can positively identify. Skip typecheck/lint if no tool config for them exists.

Record the resolved commands as `VERIFY_CMDS` for Phase 6b. If nothing was found beyond fallback, note in the final report so operator knows verification was minimal.

---

## Phase 4: Per-Thread Analysis

> **Transparency:** *"Analyzing N threads…"* (actual count)

For each thread (not each reply — thread is the unit).

**Parallelism by N**:

- **N ≤ 10**: analyze in a single pass within this sub-agent. Cheap and avoids spawn overhead.
- **N > 10**: fan out to nested sub-agents in batches of 5–8 threads each. Run all batches in parallel via a single message with multiple Agent tool calls (per global "Parallelism is free for an AI agent" rule). Each nested sub-agent returns the same per-thread block shape (4d). Merge results in order.
- **N > 40**: cap batch size at 5 to keep each nested sub-agent's context bounded; still launch all batches in parallel.

Group sequencing within a single sub-agent is allowed when threads share a file (read once, analyze multiple). Cross-thread analysis (grouping related comments) happens after fan-out merge.

### 4a. Gather context

- Read the referenced file with ≥20 lines around the flagged line.
- Follow cross-file references if the comment mentions them.
- Grep for actual usage when the comment proposes new abstractions (YAGNI check).

### 4b. Verdict assignment

Run these checks in order — first match wins:

1. **ALREADY ADDRESSED** — code already reflects the requested change, or `isResolved: true`, or thread closed by reviewer.
2. **DECLINE** — comment is technically wrong, contradicts a load-bearing standard (`CLAUDE.md` / `.claude/rules/*`), or proposes a YAGNI abstraction with no current usage. Must cite the standard or the concrete reason. **Regression-lock check (optional but recommended):** if the declined behavior is non-obvious (a reasonable reviewer could re-raise it next round), add a regression test that asserts the current behavior. Mark the test with a one-line comment naming the PR + comment id. Skip when behavior is already covered or self-evident from types.
3. **UNCLEAR** — cannot infer a specific action; multiple contradictory interpretations.
4. **DECISION-NEEDED** — finding is valid, but the fix hits the Decision Gate. State which gate criterion applies.
5. **AUTO-FIX** — finding is valid, fix is clear, no Decision Gate criterion applies.

### 4c. Fix plan (AUTO-FIX and DECISION-NEEDED only)

Produce a concrete fix plan: files to touch, exact change, tests to add/update. For DECISION-NEEDED, produce **two options** (recommended + alternative) so the wizard has real choices.

For DECISION-NEEDED, also assess **blocked?** — is the fix unreachable this session because it requires a separate spec/design change, an external decision, or a blocking upstream dependency? If yes, name the specific blocker in the return block (`Blocker: <one-line>`). If no, set `Blocker: none`. The wizard uses this to decide whether to offer option D. Default is `Blocker: none` — assume reachable unless proven otherwise.

### 4d. Sub-agent return format

One preamble block plus one block per thread:

```text
PR: #<number> — <title>
Branch: <branch>
Author: <author>
URL: <url>
Repo: <owner>/<name>
Review Status: <reviewDecision>
Linked Issues: <list or "None">
Scope: <scope statement>
Files changed: <list>
Total threads: <N>
Counts: AUTO-FIX=<a> DECISION-NEEDED=<d> DECLINE=<x> ALREADY=<y> UNCLEAR=<u>
```

Per thread:

```text
---
#: <N>
ThreadID: <GraphQL thread id, or "none" for top-level review/issue comments>
RootCommentID: <numeric databaseId of root inline comment, or review/issue comment id>
File: <path> L<line>           (or "PR-level" for non-inline)
Reviewer: <username>
Summary: <one-line>
Verdict: <AUTO-FIX | DECISION-NEEDED | DECLINE | ALREADY ADDRESSED | UNCLEAR>
Gate (DECISION-NEEDED only): <which Decision Gate criterion applies>
Reasoning: <2–3 sentences, cite standards by file path>
Fix plan (AUTO-FIX): <files + exact change + tests>
Option A (DECISION-NEEDED, recommended): <change> | Pro: ... | Con: ...
Option B (DECISION-NEEDED, alternative): <change> | Pro: ... | Con: ...
Blocker (DECISION-NEEDED only): <one-line specific external blocker, or "none">
Reply tag: <fixed|wontfix|already|unclear> — drafted in Phase 6
Code context: <path> L<start>-L<end>
---
```

---

## Phase 5: Overview + Decision-Only Wizard

> **Main agent resumes here.** Render from returned data; do not re-fetch.

### 5.0 Expectation-setting announce (always, before the table)

The very first message of Phase 5 sets the scope so the operator knows what is coming. Required shape (single line, no preamble):

> *"PR #N · K threads → A auto-fix · D decisions · X decline · Y already · U unclear · S skipped (prior run). Walking D decisions now."*

When `D == 0`:

> *"PR #N · K threads → A auto-fix · X decline · Y already · U unclear · S skipped. No decisions needed — proceeding to implementation."*

Then immediately go to 5a/5b/5c table and (when D > 0) the wizard. The point: operator knows scope in one line before any UI.

### 5a. PR Overview

| Field            | Value                   |
| ---------------- | ----------------------- |
| PR               | #\<number\> — \<title\> |
| Branch           | \<branch\>              |
| Author           | \<author\>              |
| URL              | \<url\>                 |
| Review Status    | \<reviewDecision\>      |
| Linked Issues    | \<list or "None"\>      |
| Threads analyzed | \<count\>               |

**Scope:** \<scope statement\>

**Files changed:** \<list\>

### 5b. Verdict Counts

> AUTO-FIX: N · DECISION-NEEDED: N · DECLINE: N · ALREADY: N · UNCLEAR: N

### 5c. Full Thread Table (orientation only — no input requested here)

Verdict column uses an emoji marker for skim, then the word:

- 🔧 AUTO-FIX · 🤔 DECISION · 🚫 DECLINE · ✅ ALREADY · ❓ UNCLEAR · ⏭️ SKIPPED (prior run)

| #   | Location | Reviewer | Summary      | Verdict     |
| --- | -------- | -------- | ------------ | ----------- |
| 1   | \<link\> | \<user\> | \<one-line\> | 🔧 AUTO-FIX |

### 5d. Decision Wizard — DECISION-NEEDED items only

If **zero** DECISION-NEEDED items: skip the wizard. Print one line, then go to the **5e plan-approval gate** (do NOT jump to Phase 6):

> No judgment calls needed — every finding has a clear correct fix. Showing you the plan before I touch anything.

If **one or more**: say:

> N items need your judgment because each one hits the Decision Gate (public contract / schema / architectural pattern / load-bearing config). Walking through them now. Everything else (N AUTO-FIX + N DECLINE) will be handled without asking.

For each DECISION-NEEDED item, in order:

1. Render the card as a regular markdown message (not inside `AskUserQuestion`):

   ---

   **Decision #\<N\> of \<total decisions\> — \<short summary\>**

   [\<parent-dir\>/\<filename\>:\<line\>](full/path#L<line>) | Reviewer: `<username>`

   **Comment:**

   > "\<full comment text\>"

   **Code context (L\<start\>–L\<end\>):**

   ```text
   <relevant lines>
   ```

   **Why this needs your decision:**
   \<which Decision Gate criterion applies — public contract / schema / architectural pattern / load-bearing config / equally-correct paths / contradicts standard / irreversible\>

   **My recommendation:** Option A.

   ---

2. Immediately call `AskUserQuestion`:
   - **question**: `"#<N>: <one-line decision phrasing>?"`
   - **header**: `"Decision <N>/<total>"`
   - **options** (max 4):
     1. `"A — <name> (Recommended)"` · `Pro: ...` `Con: ...`
     2. `"B — <name>"` · `Pro: ...` `Con: ...`
     3. `"C — Decline finding"` · when reviewer is wrong despite the framing; the system will reply DECLINE with rationale
     4. `"D — Defer (blocked)"` · **only when the fix is genuinely unreachable this session** — requires a separate spec/design change, an external decision the operator does not own, or a blocking upstream dependency. Card must name the blocker explicitly. Do NOT offer D for "out of PR scope", "would be a big change", or "needs more thought" — those are not blockers, those are AUTO-FIX or DECISION-NEEDED with option A/B. Per the operator's standing principle: correctness over scope. If D is shown, the card states the specific external blocker; the system files a follow-up issue and replies `deferred: <issue-link>`.

   The automatic **Other** option is custom input — operator types alternative path.

   **When NOT to offer D at all**: if the fix is feasible in this session — even if large, even if outside PR scope — drop D from the options. Replace with custom Other only. Default is: D is omitted unless the sub-agent identified a concrete blocker in 4c.

3. After response: one-line confirm (*"Got it — #N → A"*), continue.

Do not wizard-walk AUTO-FIX, DECLINE, ALREADY, or UNCLEAR items. They are auto-handled in Phase 6 — but only after the plan-approval gate below.

### 5e. Plan-Approval Gate (ALWAYS — the one intentional stop)

This gate fires on **every** run, including when zero decisions were needed. It is the single point where the operator approves the overall assessment before any code is touched, any commit is made, or any reply is posted. After approval, Phase 6 runs fully autonomously and only stops again for a real mid-flight decision (Phase 6b.1).

**Do not skip this gate. Do not execute Phase 6 without it.** The prior behavior — analyzing and then implementing in one hit — is the failure this gate exists to prevent.

Render the plan as a compact markdown message:

---

**Plan for PR #\<N\> — \<title\>**

I analyzed \<K\> threads. Here's what I'll do:

**Will fix (🔧 \<count\>):**

| #   | Location          | Fix                       | Tests               |
| --- | ----------------- | ------------------------- | ------------------- |
| 1   | \<dir/file:line\> | \<one-line what changes\> | \<add/update/none\> |

**Decided with you (🤔 \<count\>, if any):**

| #   | Location          | Your call | What I'll do |
| --- | ----------------- | --------- | ------------ |
| 2   | \<dir/file:line\> | Option A  | \<one-line\> |

**Will decline (🚫 \<count\>, if any):** \<one-line each, with the standard cited\>

**Skipping (⏭️ \<count\>):** \<already resolved / prior-run — one line\>

**Then:** verify (\<derived commands\>) → commit → push → reply in-thread + resolve \<count\> threads → report.

**Commit message preview:**

```text
<type>(<scope>): <subject>
```

---

Then call `AskUserQuestion`:

- **question**: `"Approve this plan? I'll run it end-to-end and only stop if a real decision comes up."`
- **header**: `"Approve plan"`
- **options**:
  1. `"Approve — run it (Recommended)"` · executes Phase 6 autonomously
  2. `"Adjust"` · operator names what to change (drop an item, change a fix, exclude a file); re-render the plan and re-ask
  3. `"Show me a finding"` · operator wants the full card for a specific # before approving; show it, then re-ask

The automatic **Other** option lets the operator give freeform direction.

- **Approve** → proceed to Phase 6, no further gates except 6b.1.
- **Adjust / Other** → apply the change, re-render the updated plan, re-ask. Loop until approved.
- **Show me a finding** → render the full card (comment text + code context + reasoning) for that #, then re-render the plan and re-ask.

---

## Phase 6: Execute End-to-End

Runs autonomously after the 5e plan approval. The operator approved the overall plan; do not re-confirm per step. Stop only for a mid-flight cascading decision (6b.1) or a hard-gate failure.

### 6a. Implement (sub-agent fan-out by default)

For every AUTO-FIX item and every decided DECISION-NEEDED item (option A/B/Other):

**Sub-agent strategy** (default to parallel; serialize only when forced):

1. Build the batch graph: independent batches in parallel, dependent batches sequential. Rules: dependencies first, same-file grouping, structural items single-threaded.
2. For each parallel layer, dispatch **one sub-agent per independent batch** via Agent tool in a single message (multiple Agent calls in one message = concurrent execution per global rule).
3. Each sub-agent receives: the batch's items (with fix plans), the scope statement, the project standards summary from Phase 3, the verify commands from Phase 3a. Sub-agent must implement, run verify on its own batch, and return a structured result (`{batch_id, files_touched, verify_status, errors, cascading_findings}`).
4. Main agent merges results and proceeds to 6b only when every parallel sub-agent reports green; otherwise applies the Phase 6b.1 cascading-findings policy.

**When to keep work on the main agent (not fan out)**:

- Total items ≤ 3 AND all mechanical (overhead of sub-agent spawn exceeds gain).
- Any item touches shared build/CI config or a lockfile (e.g. `tsconfig.json`, `nx.json`, a CI workflow, a lockfile — substitute your stack's equivalents): shared state — serialize to avoid race.
- Operator chose Other for a DECISION-NEEDED item with no concrete fix plan (main agent must clarify before delegating).

**Always** update tests inline with each behavioral change. If a fix is behavioral but no test covers it, add or extend one in the same batch. (Operator's standing rule: no end-of-task "are tests updated?" question.)

### 6b. Verify

Run `VERIFY_CMDS` derived in Phase 3a — typecheck, lint, test in that order. Do not hardcode any specific runner; use what Phase 3a resolved.

If a check fails: diagnose root cause, fix, re-run. Do not proceed until clean. Cascading findings handled per Phase 6b.1.

### 6b.1. Cascading-finding policy

A *cascading finding* = something discovered during the fix loop (typecheck/lint/test failure, or code read during a fix) that is not in the original PR comments.

Decision tree, in order:

1. **AUTO-FIX class** (per Decision Gate "NOT decision-needed" list): fix silently as part of the current batch. Do not pause, do not surface mid-flow. Track in the final report under "cascading auto-fixes" so operator sees them after.
2. **Decision Gate hit** (public contract / schema / load-bearing config / architectural pattern / equally-correct paths / contradicts standard / irreversible): **stop the batch**. Surface a mid-execution wizard prompt using the same `AskUserQuestion` shape as Phase 5d, with options A/B/C and Other. Resume the batch after operator decides.
3. **Genuinely blocked** (separate spec required, external dependency): stop the batch, file a follow-up issue, post `deferred:` reply for the original thread that triggered the cascade if applicable, continue with remaining batches.

Cascading findings never "silently expand" beyond AUTO-FIX class. The operator's correctness-over-scope principle still applies — a real bug discovered while fixing gets fixed.

### 6c. Commit

**Race check first.** Re-read HEAD; if it differs from `START_SHA` captured in Phase 1.5, abort:

```bash
test "$(git rev-parse HEAD)" = "$START_SHA" || { echo "error: HEAD moved since pre-flight (was $START_SHA, now $(git rev-parse HEAD)). aborting before commit."; exit 1; }
```

**Empty-diff check.** If nothing to stage, skip commit and push entirely (see Phase 6c.1).

```bash
git diff --quiet HEAD && SKIP_COMMIT=true || SKIP_COMMIT=false
```

When `SKIP_COMMIT=false`, semantic commit, single concern when possible. If batches span concerns, split into multiple commits.

```bash
git status
git diff --stat
git add <specific files — never -A>
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

Addresses PR #<N> review:
- <reviewer> L<line>: <one-line>  (https://github.com/<owner>/<name>/pull/<N>#discussion_r<comment-id>)
- ...

<optional body — prerequisite inline fixes with causal explanation, per the project's git/commit conventions>
EOF
)"
```

Never use `--no-verify`. If pre-commit hook fails: diagnose, fix, re-commit (new commit, not amend per global rule).

### 6c.1. Empty-diff short-circuit

If `SKIP_COMMIT=true` (all threads were DECLINE / ALREADY ADDRESSED / UNCLEAR — nothing to implement):

- Skip 6c commit and 6d push entirely.
- Proceed directly to 6e (reply) and 6f (resolve).
- Final report notes: `Commits: none — no fixes required.`

### 6d. Push

```bash
git push
```

If branch has no upstream: `git push -u origin <branch>`. Never force-push without explicit operator request.

After push, capture the CI run URL for the final report:

```bash
CI_RUN_URL=$(gh run list --branch "$BRANCH" --limit 1 --json url --jq '.[0].url // ""')
```

Empty result is fine (no workflow yet); the report will say "no CI run detected".

### 6e. Reply in-thread (machine-readable)

For every analyzed thread, post a reply. Replies optimized for the next machine reviewer (Copilot, future agents) — no humans behind these.

**Reply Format** — single line preferred, structured tag + minimal payload:

| Verdict                                           | Tag format                                                             |
| ------------------------------------------------- | ---------------------------------------------------------------------- |
| AUTO-FIX (done)                                   | `fixed: <one-line what changed>. commit:<sha7>`                        |
| DECISION-NEEDED (option A/B chosen + implemented) | `fixed: <one-line what changed>. choice:<A\|B\|custom>. commit:<sha7>` |
| DECLINE                                           | `wontfix: <one-line reason>. ref:<file/path or rule>`                  |
| ALREADY ADDRESSED                                 | `already: <one-line where>. commit:<sha7 or "pre-existing">`           |
| UNCLEAR                                           | `unclear: <specific clarifying question>`                              |
| Deferred (Decision option D)                      | `deferred: <github-issue-url>`                                         |

Rules:

- No greetings, no thanks, no apologies, no rationalization.
- No backticks around tags. No prose. ASCII only.
- ≤200 chars when possible. Hard cap 500 **excluding** the trailer.
- Reference file paths instead of restating the comment.
- Tag is the first token; parsers split on `:`.
- **Signature trailer is mandatory.** Every reply ends with a blank line followed by `[claude-code:audit-pr-comments]` on its own final line. Parsers (and the next run of this skill) use the trailer to detect agent-authored replies and short-circuit per the idempotency contract in Phase 2.

Full reply shape:

```text
<tag>: <payload>

[claude-code:audit-pr-comments]
```

**Post mechanics**:

- Inline thread reply:

  ```bash
  printf '%s\n\n[claude-code:audit-pr-comments]\n' "$BODY" \
    | gh api repos/$OWNER/$NAME/pulls/$PR/comments/$ROOT_COMMENT_ID/replies --input -
  ```

- Top-level review or issue comment (no thread to resolve via GraphQL): post as issue comment with a **parseable header line** identifying the review id, on its own line, followed by the tagged reply. Header format: `Re-review-<review-id>:` — parseable by future agents:

  ```bash
  printf 'Re-review-%s:\nfixed: %s. commit:%s\n\n[claude-code:audit-pr-comments]\n' \
    "$REVIEW_ID" "$ONE_LINE" "$SHA7" \
    | gh api repos/$OWNER/$NAME/issues/$PR/comments --input -
  ```

- Throttle: `sleep 2` between calls. On 422 abuse / 403 Retry-After: honor header or wait 60s, retry. For >20 replies, prefer a single aliased GraphQL mutation (see "Bulk reply via GraphQL" in 6e.1).

### 6e.1. Dismiss stale top-level reviews

Top-level reviews have no thread to resolve via `resolveReviewThread`. A stale `CHANGES_REQUESTED` review left undismissed keeps the PR red even after every inline finding is fixed.

For each top-level review whose `state` is `CHANGES_REQUESTED` AND every inline finding it raised was handled (fixed / declined / already / deferred):

- **Bot reviewers** (Copilot, dependabot, github-actions, any login ending in `[bot]`): auto-dismiss.
- **Human reviewers**: surface in final report with the exact command; do not auto-dismiss.

```bash
gh api -X PUT repos/$OWNER/$NAME/pulls/$PR/reviews/$REVIEW_ID/dismissals \
  --field message='superseded by commit:<sha7> — see thread replies'
```

Failed dismissals are non-fatal; record in failure list.

### 6e.2. Bulk reply via GraphQL (when N > 20)

For PRs with >20 threads to reply to, prefer a single GraphQL mutation with aliased operations over N REST calls — per the global "GitHub: bulk API calls" rule. Two requests total: one to fetch node IDs, one to post all replies.

```graphql
mutation {
  r1: addPullRequestReviewThreadReply(
    input: { pullRequestReviewThreadId: "...", body: "..." }
  ) {
    comment {
      id
    }
  }
  r2: addPullRequestReviewThreadReply(
    input: { pullRequestReviewThreadId: "...", body: "..." }
  ) {
    comment {
      id
    }
  }
  # ...
}
```

REST fallback for ≤20 threads: `sleep 2` between calls, honor `Retry-After`, retry on 422 abuse with 60s backoff.

### 6e.3. Failure handling (replies + dismissals)

**Continue on failure.** Do not abort the run because one POST 5xx'd. Per-call protocol:

1. Capture stderr and HTTP status.
2. On `422` with `{"code":"abuse"}` or `403` with `Retry-After`: honor the header (or 60s default), retry once.
3. After one failed retry: record the failure with `{thread/review id, comment id, command, error}` in a `FAILURES` list. Continue.
4. At end of 6e + 6e.1 + 6e.2, if `FAILURES` is non-empty, the final report includes a "Retry these manually" block with each exact `gh api ...` command pre-filled so operator can copy-paste.

### 6f. Resolve threads

For every thread with verdict AUTO-FIX (implemented), DECISION-NEEDED (implemented + option A/B/Other), DECLINE, or ALREADY ADDRESSED — resolve via GraphQL. Do not resolve UNCLEAR threads (operator-question pending).

```bash
gh api graphql -f query='
  mutation($threadId:ID!) {
    resolveReviewThread(input:{threadId:$threadId}) {
      thread { id isResolved }
    }
  }' -F threadId=<thread-id>
```

For >20 threads to resolve, use aliased GraphQL mutation (same pattern as 6e.2).

Skip threads with `ThreadID: none` (top-level review/issue comments have no resolvable thread — dismissed via 6e.1 instead).

Skip threads already `isResolved: true` (idempotency — handled by Phase 2 filter, but re-check here as defense in depth).

Failure handling: same as 6e.3 — continue, record, surface in final report with retry commands.

### 6g. Deferred follow-ups (option D in wizard)

For each DECISION-NEEDED item where the operator chose D:

```bash
gh issue create --title '<title>' --body '<body — links back to PR #N comment URL>' --label deferred
```

Then post the `deferred:` reply pointing at the new issue URL. Resolve the source thread.

### 6h. Re-request review

If PR was `CHANGES_REQUESTED` and at least one finding was fixed:

```bash
gh pr edit <number> --add-reviewer <reviewer-username>
```

Auto-run for non-human reviewers (Copilot, automated bots). For human reviewers, include in the report and let the operator trigger.

---

## Final Report

Print last as **rendered markdown** — not a fenced text block. Skimmable: a status line, three small tables, and a one-line tail. Emojis mark status only; do not decorate prose. Omit any section whose count is zero (no empty "Declined: 0" rows).

### Required shape

Lead line (one line, bold):

> **✅ PR #\<N\> — \<title\>** · \<X\> fixed · \<Y\> resolved · pushed `\<sha7\>`

If anything failed: lead with ⚠️ instead of ✅ and put the failure count in the lead line.

**Outcome table** — one row per status that has a non-zero count:

| Status               | Count | Detail                       |
| -------------------- | ----- | ---------------------------- |
| 🔧 Fixed             | \<n\> | AUTO-FIX + decided           |
| 🤔 Decided           | \<n\> | your calls, see below        |
| 🚫 Declined          | \<n\> | standard cited in replies    |
| ✅ Already addressed | \<n\> | —                            |
| ❓ Unclear           | \<n\> | replied with question        |
| ⏭️ Deferred          | \<n\> | issues: \<urls\>             |
| ⏭️ Skipped           | \<n\> | prior-run / already resolved |

**Decisions table** — only if the operator made ≥1 decision:

| #   | Finding      | Your call |
| --- | ------------ | --------- |
| 2   | \<one-line\> | Option A  |

**Verification + GitHub** — compact two-column:

| Check                   | Result                                        |
| ----------------------- | --------------------------------------------- |
| Typecheck               | ✅ pass / ❌ fail / ➖ not configured         |
| Lint                    | ✅ / ❌ / ➖                                  |
| Tests                   | ✅ pass (\<n\> total) / ❌                    |
| Threads resolved        | \<n\>                                         |
| Replies posted          | \<n\> (trailer attached)                      |
| Stale reviews dismissed | \<n\> bot / \<n\> human (manual)              |
| Re-request review       | ✅ done / 💡 suggested for @\<user\> / ➖ n/a |
| CI run                  | [\<run-id\>](CI_RUN_URL) / ➖ none yet        |

**Files touched** — plain bullet list, each as a clickable link:

- [\<dir/file\>](path)

**Tail** (one line): cascading auto-fixes if any (`+\<n\> cascading fix(es): \<one-line\>`), else omit.

### Failures block (only if non-empty)

Render as a `> ⚠️` callout followed by a fenced `bash` block of copy-paste retry commands:

```bash
# reply #<N>
gh api repos/<owner>/<name>/pulls/<pr>/comments/<id>/replies --input - <<<'<body>'
# resolve #<M>
gh api graphql -f query='mutation { resolveReviewThread(input:{threadId:"<id>"}) { thread { isResolved } } }'
# dismiss review <id>
gh api -X PUT repos/<owner>/<name>/pulls/<pr>/reviews/<id>/dismissals --field message='<msg>'
```

Name what failed, which command, and the current repo/PR state in one sentence above the block.

### Formatting rules

- Render tables as live markdown — never wrap the whole report in a code fence.
- One emoji per status, no doubles. No emoji in table detail cells or prose.
- Omit zero-count rows and empty sections entirely.
- Excluded-files note (e.g. operator told you to skip a path) goes as a single italic line under Files touched: *Excluded by your instruction: \<path\>*.

---

## Principles

- **Correctness over scope.** A valid finding gets fixed in this PR. No "defer to issue" reflex.
- **Standards are authority.** `CLAUDE.md` + `.claude/rules/*` override reviewer opinion unless the reviewer found a bug in the standard.
- **Auto-fix is default.** Walk the operator through judgment calls only. Decision Gate is the filter.
- **Parallelize aggressively.** Phase 4 fans out nested sub-agents when N>10. Phase 6a fans out one sub-agent per independent batch in a single message. Sequential only when forced by shared-state or operator-clarification.
- **Idempotent by trailer.** Every reply carries `[claude-code:audit-pr-comments]`. Re-runs detect this and short-circuit. Same PR + no new comments = no-op.
- **YAGNI before accepting abstractions.** Grep first.
- **Machine-readable replies.** Tagged, terse, parser-friendly. No human niceties. Trailer mandatory.
- **Resolve what you fixed.** A merged finding leaves no dangling thread. Dismiss stale bot reviews too.
- **One gate, then autonomous.** Always pause once after analysis to get plan approval (5e). Never analyze-then-execute in one hit. After approval, no per-step gates — only real mid-flight decisions or hard-gate failures stop the run.
- **Report is rendered markdown.** Status line + small tables + emoji status markers. Skimmable, never a raw text dump, never wrapped in a code fence.
- **End-to-end.** Pre-flight, analyze, decide-only-what-matters, **get plan approval**, implement, verify, commit, push, reply, dismiss, resolve, report — one run after the gate.
