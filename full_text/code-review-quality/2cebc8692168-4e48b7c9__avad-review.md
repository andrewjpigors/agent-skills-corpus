---
name: avad-review
version: 2.11.7
description: |
  Pre-landing code review. Analyzes diff for structural issues using a project-specific
  checklist. Two modes: local (review current branch) or PR (review and comment on a
  GitHub PR by number).
  Proactively suggest when the user is about to merge or land code changes.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Pre-Landing Code Review

You are running the `/avad-review` workflow.

Two modes based on arguments:

- `/avad-review` — **Local mode.** Review current branch diff. Output to terminal.
- `/avad-review <number>` — **PR mode.** Review PR diff. Post findings as a PR review.

> **EXECUTION ORDER — STRICT SEQUENTIAL.**
> Complete each numbered step fully before starting the next.
> Do NOT launch adversarial agents, Codex agents, or any subagents until their step is reached.
> Do NOT parallelize steps — only parallelize within a step where explicitly allowed.

---

## Step 1: Determine Mode

Check if an argument was provided:

- **Number provided** (e.g. `58`) → PR mode
- **No argument** → Local mode

---

## Step 2: Read Project Configuration

Read `docs/GIT_WORKFLOW.md` to determine the target branch.

Also read:
- `CLAUDE.md` — for project context
- `AGENTS.md` — for domain rules (canonical values, API whitelist, etc.)

If `docs/GIT_WORKFLOW.md` does not exist, ask the user for the target branch once.

---

## Step 2.5: Scope Drift Detection

Before reviewing code quality, check: **did they build what was requested — nothing more, nothing less?**

### Local mode:
1. Read `TODOS.md` (if it exists). Read commit messages (`git log origin/<target>..HEAD --oneline`).
   **If no PR exists:** rely on commit messages and TODOS.md for stated intent — this is the common case since /review runs before /avad-ship creates the PR.
2. Identify the **stated intent** — what was this branch supposed to accomplish?
3. Run `git diff origin/<target>...HEAD --stat` and compare the files changed against the stated intent.

### PR mode:
1. Read `TODOS.md` (if it exists). Read PR description (`gh pr view <number> --json body --jq .body`).
   Read PR commit messages (`gh pr view <number> --json commits --jq '.commits[].messageHeadline'`).
2. Identify the **stated intent** — what was this PR supposed to accomplish?
3. Run `gh pr diff <number> --stat` and compare the files changed against the stated intent.
4. Evaluate with skepticism:

   **SCOPE CREEP detection:**
   - Files changed that are unrelated to the stated intent
   - New features or refactors not mentioned in the plan
   - "While I was in there..." changes that expand blast radius

   **MISSING REQUIREMENTS detection:**
   - Requirements from TODOS.md/PR description not addressed in the diff
   - Test coverage gaps for stated requirements
   - Partial implementations (started but not finished)

5. Output (before the main review begins):
   ```
   Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
   Intent: <1-line summary of what was requested>
   Delivered: <1-line summary of what the diff actually does>
   [If drift: list each out-of-scope change]
   [If missing: list each unaddressed requirement]
   ```

6. This is **INFORMATIONAL** — does not block the review. Proceed to Step 3.

---

## Step 3: Get the Diff

### Local mode:

```bash
git fetch origin
git diff origin/<target>...HEAD
```

Three-dot diff — shows only your branch's changes since divergence.

If on the target branch or no diff exists:
output `Nothing to review — no changes against <target>.` and stop.

### PR mode:

```bash
gh pr diff <number>
```

If the PR doesn't exist or has no diff, report and stop.

---

## Step 4: Load or Generate Checklist

**If a project-specific checklist exists** (`~/.avadbot/projects/<repo>/review-checklist.md`):
read it and use it.

**If no checklist exists**, generate one before proceeding:

1. Read the project's governing docs, `CLAUDE.md`, `AGENTS.md`, and scan the codebase
   structure to understand:
   - Language and framework
   - Database type and access patterns
   - External APIs and their constraints
   - Domain-specific rules (canonical values, idempotency, etc.)
   - Security boundaries (auth, tokens, user input)

2. Read `checklist-seed.md` in this skill directory.
   Use it as a **bootstrap taxonomy only**:
   - start from its seed categories and suppressions
   - prune anything irrelevant to the project
   - rename categories to match the project's actual risks and vocabulary
   - add project-specific categories and suppressions from docs and code
   - never copy the seed verbatim as the final checklist
   - no code transforms the seed; the agent reads it as context and synthesizes
     the final project-specific checklist

3. Generate `~/.avadbot/projects/<repo>/review-checklist.md` following this structure:

   ```markdown
   # Pre-Landing Review Checklist

   ## Instructions

   Review the diff for the issues listed below. Be specific — cite `file:line`
   and suggest fixes. Skip anything that's fine. Only flag real problems.

   **Two-pass review:**
   - **Pass 1 (CRITICAL):** These block `/avad-ship`.
   - **Pass 2 (INFORMATIONAL):** Included in PR body but do not block.

   **Output format:**

   Pre-Landing Review: N issues (X critical, Y informational)

   **CRITICAL** (blocking):
   - [file:line] Problem description
     Fix: suggested fix

   **Issues** (non-blocking):
   - [file:line] Problem description
     Fix: suggested fix

   If no issues found: `Pre-Landing Review: No issues found.`

   Be terse. One line problem, one line fix. No preamble.

   ---

   ## Pass 1 — CRITICAL

   <generate 2-4 critical categories based on the project's actual risks>

   ## Pass 2 — INFORMATIONAL

   <generate 3-6 informational categories based on the project's patterns>

   ---

   ## Suppressions — DO NOT flag these

   <generate 3-5 suppression rules to reduce false positives>
   ```

4. Start from the seed file, but the final categories must still be **derived from the project**, not generic boilerplate.
   Every category and suppression should reflect repo-specific signals from `CLAUDE.md`,
   `AGENTS.md`, architecture docs, or the codebase itself.

5. Write the file. This persists — future runs use it directly.

---

## Step 4.5: Triage Bot Review Comments (PR mode only)

**Skip this step entirely in local mode or if no PR exists.**

### Fetch bot comments

Fetch both line-level and top-level comments in parallel:

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)
PR_NUMBER=<number>

# Line-level review comments
gh api repos/$REPO/pulls/$PR_NUMBER/comments \
  --jq '.[] | select(.user.type == "Bot" or (.user.login | test("greptile|coderabbit|codeclimate|sonarcloud"; "i"))) | select(.position != null) | {id: .id, path: .path, line: .line, body: .body, html_url: .html_url, user: .user.login, source: "line-level"}' > /tmp/bot_line.json &

# Top-level PR comments
gh api repos/$REPO/issues/$PR_NUMBER/comments \
  --jq '.[] | select(.user.type == "Bot" or (.user.login | test("greptile|coderabbit|codeclimate|sonarcloud"; "i"))) | {id: .id, body: .body, html_url: .html_url, user: .user.login, source: "top-level"}' > /tmp/bot_top.json &
wait
```

**If API errors or zero bot comments:** Skip silently — continue to Step 5.

### Suppressions check

Derive the project slug and check for known false positives:

```bash
REMOTE_SLUG=$(basename "$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)" 2>/dev/null || basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
HISTORY="$HOME/.avadbot/projects/$REMOTE_SLUG/bot-review-history.md"
```

Read `$HISTORY` if it exists. Each line records a previous triage outcome:

```
<YYYY-MM-DD> | <owner/repo> | <bot> | <type:fp|fix|already-fixed> | <file-pattern> | <category>
```

**Categories** (fixed set): `race-condition`, `null-check`, `error-handling`, `style`,
`type-safety`, `security`, `performance`, `correctness`, `other`

Match each fetched comment against entries where:
- `type == fp` (only suppress known false positives)
- `bot` matches the comment's bot name
- `file-pattern` matches the comment's file path
- `category` matches the issue type

Skip matched comments as **SUPPRESSED**.

### Classify

For each non-suppressed comment:

| Classification | Meaning |
|---|---|
| **VALID & ACTIONABLE** | Real issue, not yet fixed in the diff |
| **VALID BUT ALREADY FIXED** | Real issue, but already addressed in the diff |
| **FALSE POSITIVE** | Not a real issue — bot is wrong |
| **SUPPRESSED** | Known false positive from history |

Store the classifications — they are included in Step 6 output.

---

## Step 4.75: TODOS.md Cross-Reference

Read `TODOS.md` in the repo root (skip silently if it doesn't exist). Check whether the diff:

1. **Closes** any open TODO items — note them for the review output
2. **Creates work** that needs a new TODO item — flag it as informational
3. **Has related TODOs** that provide useful review context — use them to inform your review

This step enriches the review with project context but does not block it.

---

## Step 5: Two-Pass Review

Apply the checklist against the diff:

1. **Pass 1 (CRITICAL):** blocking categories + Enum & Value Completeness
2. **Pass 2 (INFORMATIONAL):** non-blocking categories — Conditional Side Effects, Magic Numbers & String Coupling, Dead Code & Consistency, LLM Prompt Issues, Test Gaps, View/Frontend, Performance & Bundle Impact

**Enum & Value Completeness requires reading code OUTSIDE the diff.** When the diff introduces a new enum value, status, tier, or type constant, use Grep to find all files that reference sibling values, then Read those files to check if the new value is handled in switches, allowlists, and filters. This is the one category where within-diff review is insufficient.

**Search-before-recommending:** When recommending a fix pattern (especially for concurrency, caching, auth, or framework-specific behavior):
- Verify the pattern is current best practice for the framework version in use
- Check if a built-in solution exists in newer versions before recommending a workaround
- Verify API signatures against current docs (APIs change between versions)

Takes seconds, prevents recommending outdated patterns. If WebSearch is unavailable, note it and proceed with in-distribution knowledge.

Respect the suppressions — do NOT flag items in the suppressions section.
Read the FULL diff before commenting — do not flag issues already addressed in the diff.

---

## Step 5.5: Design Review (conditional)

Check if the diff touches frontend files (use the same diff source as the main review):

### Local mode:
```bash
git diff origin/<target>...HEAD --stat | grep -qE '\.(css|scss|less|jsx|tsx|vue|svelte|html)' && SCOPE_FRONTEND=true || SCOPE_FRONTEND=false
```

### PR mode:
```bash
gh pr diff <number> --stat | grep -qE '\.(css|scss|less|jsx|tsx|vue|svelte|html)' && SCOPE_FRONTEND=true || SCOPE_FRONTEND=false
```

**If `SCOPE_FRONTEND=false`:** Skip design review silently. No output.

**If `SCOPE_FRONTEND=true`:**

1. **Check for DESIGN.md.** If `DESIGN.md` or `design-system.md` exists in the repo root, read it. All design findings are calibrated against it — patterns blessed in DESIGN.md are not flagged. If not found, use universal design principles.

2. **Read `design-checklist.md`** in this skill directory. If the file cannot be read, skip design review with a note: "Design checklist not found — skipping design review."

3. **Read each changed frontend file** (full file, not just diff hunks). Frontend files are identified by the patterns listed in the checklist.

4. **Apply the design checklist** against the changed files. For each item:
   - **[HIGH] mechanical CSS fix** (`outline: none`, `!important`, `font-size < 16px`): classify as AUTO-FIX
   - **[HIGH/MEDIUM] design judgment needed**: classify as ASK
   - **[LOW] intent-based detection**: present as "Possible — verify visually or run /avad-design-review"

5. **Include findings** in the review output under a "Design Review" header. Design findings merge with code review findings into the same Fix-First flow (Step 6).

---

## Step 5.75: Test Coverage Diagram

100% coverage is the goal. Evaluate every codepath changed in the diff and identify test gaps. Gaps become INFORMATIONAL findings that follow the Fix-First flow.

### Test Framework Detection

Before analyzing coverage, detect the project's test framework:

1. **Read CLAUDE.md** — look for a `## Testing` section with test command and framework name. If found, use that as the authoritative source.
2. **If CLAUDE.md has no testing section, auto-detect:**

```bash
# Detect project runtime
[ -f Gemfile ] && echo "RUNTIME:ruby"
[ -f package.json ] && echo "RUNTIME:node"
[ -f requirements.txt ] || [ -f pyproject.toml ] && echo "RUNTIME:python"
[ -f go.mod ] && echo "RUNTIME:go"
[ -f Cargo.toml ] && echo "RUNTIME:rust"
# Check for existing test infrastructure
ls jest.config.* vitest.config.* playwright.config.* cypress.config.* .rspec pytest.ini phpunit.xml 2>/dev/null
ls -d test/ tests/ spec/ __tests__/ cypress/ e2e/ 2>/dev/null
```

3. **If no framework detected:** still produce the coverage diagram, but skip test generation.

**Step 1. Trace every codepath changed** using `git diff origin/<base>...HEAD`:

Read every changed file. For each one, trace how data flows through the code — don't just list functions, actually follow the execution:

1. **Read the diff.** For each changed file, read the full file (not just the diff hunk) to understand context.
2. **Trace data flow.** Starting from each entry point (route handler, exported function, event listener, component render), follow the data through every branch:
   - Where does input come from? (request params, props, database, API call)
   - What transforms it? (validation, mapping, computation)
   - Where does it go? (database write, API response, rendered output, side effect)
   - What can go wrong at each step? (null/undefined, invalid input, network failure, empty collection)
3. **Diagram the execution.** For each changed file, draw an ASCII diagram showing:
   - Every function/method that was added or modified
   - Every conditional branch (if/else, switch, ternary, guard clause, early return)
   - Every error path (try/catch, rescue, error boundary, fallback)
   - Every call to another function (trace into it — does IT have untested branches?)
   - Every edge: what happens with null input? Empty array? Invalid type?

This is the critical step — you're building a map of every line of code that can execute differently based on input. Every branch in this diagram needs a test.

**Step 2. Map user flows, interactions, and error states:**

Code coverage isn't enough — you need to cover how real users interact with the changed code. For each changed feature, think through:

- **User flows:** What sequence of actions does a user take that touches this code? Map the full journey (e.g., "user clicks 'Pay' → form validates → API call → success/failure screen"). Each step in the journey needs a test.
- **Interaction edge cases:** What happens when the user does something unexpected?
  - Double-click/rapid resubmit
  - Navigate away mid-operation (back button, close tab, click another link)
  - Submit with stale data (page sat open for 30 minutes, session expired)
  - Slow connection (API takes 10 seconds — what does the user see?)
  - Concurrent actions (two tabs, same form)
- **Error states the user can see:** For every error the code handles, what does the user actually experience?
  - Is there a clear error message or a silent failure?
  - Can the user recover (retry, go back, fix input) or are they stuck?
  - What happens with no network? With a 500 from the API? With invalid data from the server?
- **Empty/zero/boundary states:** What does the UI show with zero results? With 10,000 results? With a single character input? With maximum-length input?

Add these to your diagram alongside the code branches. A user flow with no test is just as much a gap as an untested if/else.

**Step 3. Check each branch against existing tests:**

Go through your diagram branch by branch — both code paths AND user flows. For each one, search for a test that exercises it:
- Function `processPayment()` → look for `billing.test.ts`, `billing.spec.ts`, `test/billing_test.rb`
- An if/else → look for tests covering BOTH the true AND false path
- An error handler → look for a test that triggers that specific error condition
- A call to `helperFn()` that has its own branches → those branches need tests too
- A user flow → look for an integration or E2E test that walks through the journey
- An interaction edge case → look for a test that simulates the unexpected action

Quality scoring rubric:
- ★★★  Tests behavior with edge cases AND error paths
- ★★   Tests correct behavior, happy path only
- ★    Smoke test / existence check / trivial assertion (e.g., "it renders", "it doesn't throw")

### E2E Test Decision Matrix

When checking each branch, also determine whether a unit test or E2E/integration test is the right tool:

**RECOMMEND E2E (mark as [→E2E] in the diagram):**
- Common user flow spanning 3+ components/services (e.g., signup → verify email → first login)
- Integration point where mocking hides real failures (e.g., API → queue → worker → DB)
- Auth/payment/data-destruction flows — too important to trust unit tests alone

**RECOMMEND EVAL (mark as [→EVAL] in the diagram):**
- Critical LLM call that needs a quality eval (e.g., prompt change → test output still meets quality bar)
- Changes to prompt templates, system instructions, or tool definitions

**STICK WITH UNIT TESTS:**
- Pure function with clear inputs/outputs
- Internal helper with no side effects
- Edge case of a single function (null input, empty array)
- Obscure/rare flow that isn't customer-facing

### REGRESSION RULE (mandatory)

**IRON RULE:** When the coverage audit identifies a REGRESSION — code that previously worked but the diff broke — a regression test is written immediately. No AskUserQuestion. No skipping. Regressions are the highest-priority test because they prove something broke.

A regression is when:
- The diff modifies existing behavior (not new code)
- The existing test suite (if any) doesn't cover the changed path
- The change introduces a new failure mode for existing callers

When uncertain whether a change is a regression, err on the side of writing the test.

Format: commit as `test: regression test for {what broke}`

**Step 4. Output ASCII coverage diagram:**

Include BOTH code paths and user flows in the same diagram. Mark E2E-worthy and eval-worthy paths:

```
CODE PATH COVERAGE
===========================
[+] src/services/billing.ts
    │
    ├── processPayment()
    │   ├── [★★★ TESTED] Happy path + card declined + timeout — billing.test.ts:42
    │   ├── [GAP]         Network timeout — NO TEST
    │   └── [GAP]         Invalid currency — NO TEST
    │
    └── refundPayment()
        ├── [★★  TESTED] Full refund — billing.test.ts:89
        └── [★   TESTED] Partial refund (checks non-throw only) — billing.test.ts:101

USER FLOW COVERAGE
===========================
[+] Payment checkout flow
    │
    ├── [★★★ TESTED] Complete purchase — checkout.e2e.ts:15
    ├── [GAP] [→E2E] Double-click submit — needs E2E, not just unit
    ├── [GAP]         Navigate away during payment — unit test sufficient
    └── [★   TESTED]  Form validation errors (checks render only) — checkout.test.ts:40

[+] Error states
    │
    ├── [★★  TESTED] Card declined message — billing.test.ts:58
    ├── [GAP]         Network timeout UX (what does user see?) — NO TEST
    └── [GAP]         Empty cart submission — NO TEST

[+] LLM integration
    │
    └── [GAP] [→EVAL] Prompt template change — needs eval test

─────────────────────────────────
COVERAGE: 5/13 paths tested (38%)
  Code paths: 3/5 (60%)
  User flows: 2/8 (25%)
QUALITY:  ★★★: 2  ★★: 2  ★: 1
GAPS: 8 paths need tests (2 need E2E, 1 needs eval)
─────────────────────────────────
```

**Fast path:** All paths covered → "Step 5.75: All new code paths have test coverage." Continue.

**Step 5. Generate tests for gaps (Fix-First):**

If test framework is detected and gaps were identified:
- Classify each gap as AUTO-FIX or ASK per the Fix-First Heuristic:
  - **AUTO-FIX:** Simple unit tests for pure functions, edge cases of existing tested functions
  - **ASK:** E2E tests, tests requiring new test infrastructure, tests for ambiguous behavior
- For AUTO-FIX gaps: generate the test, run it, commit as `test: coverage for {feature}`
- For ASK gaps: include in the Fix-First batch question with the other review findings
- For paths marked [→E2E]: always ASK (E2E tests are higher-effort and need user confirmation)
- For paths marked [→EVAL]: always ASK (eval tests need user confirmation on quality criteria)

If no test framework detected → include gaps as INFORMATIONAL findings only, no generation.

**Diff is test-only changes:** Skip Step 5.75 entirely: "No new application code paths to audit."

This step subsumes the "Test Gaps" category from Pass 2 — do not duplicate findings between the checklist Test Gaps item and this coverage diagram. Include any coverage gaps alongside the findings from Step 5 and Step 5.5. They follow the same Fix-First flow — gaps are INFORMATIONAL findings.

---

## Step 5.6: Documentation staleness check

Cross-reference the diff against documentation files. For each `.md` file in the repo root (README.md, ARCHITECTURE.md, CONTRIBUTING.md, CLAUDE.md, etc.):

1. Check if code changes in the diff affect features, components, or workflows described in that doc file.
2. If the doc file was NOT updated in this branch but the code it describes WAS changed, flag it as an INFORMATIONAL finding:
   "Documentation may be stale: [file] describes [feature/component] but code changed in this branch. Consider running `/avadbot:avad-document-release`."

This is informational only — never critical. The fix action is `/avadbot:avad-document-release`.

If no documentation files exist, skip this step silently.

---

## Step 5.8: Adversarial Review (auto-scaled)

> **WAIT.** Do NOT start this step until Steps 5–5.75 (structured review, design review, test coverage, doc staleness) are fully complete. Adversarial agents need the structured review to finish first — they provide independent second opinions, not parallel first opinions.

Adversarial review thoroughness scales automatically based on diff size. No configuration needed.

**MANDATORY — Run this command FIRST before any tier decision. Do NOT skip or assume the result:**

```bash
command -v codex >/dev/null 2>&1 && echo "CODEX: AVAILABLE" || echo "CODEX: NOT AVAILABLE"
```

**If CODEX: AVAILABLE**, run this immediately to warm up the Bash permission for subagents.
The user will be prompted once to approve — after that, Codex subagents inherit the permission:

```bash
codex --version
```

If the user denies this permission, suggest adding a permanent permission rule:

"Codex permission denied. To allow Codex permanently, run:
`/update-config Add global permission: Bash(codex *)`
Falling back to Claude-only adversarial for this review."

Then treat Codex as NOT AVAILABLE and fall back to Claude-only adversarial.

Store the result. This determines whether Codex passes run in the tier below.

**Then detect diff size:**

```bash
DIFF_INS=$(git diff origin/<target> --stat | tail -1 | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
DIFF_DEL=$(git diff origin/<target> --stat | tail -1 | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")
DIFF_TOTAL=$((DIFF_INS + DIFF_DEL))
echo "DIFF_SIZE: $DIFF_TOTAL"
```

**User override:** If the user explicitly requested a specific tier (e.g., "run all passes", "paranoid review", "full adversarial", "do all 4 passes", "thorough review"), honor that request regardless of diff size. Jump to the matching tier section.

**Auto-select tier based on diff size:**
- **Small (< 50 lines changed):** Skip adversarial review entirely. Print: "Small diff ($DIFF_TOTAL lines) — adversarial review skipped." Continue to Step 6.
- **Medium (50-199 lines changed):** Run Codex adversarial challenge (or Claude adversarial agent if Codex unavailable). Jump to the "Medium tier" section.
- **Large (200+ lines changed):** Run all remaining passes — Codex structured review + Claude adversarial agent + Codex adversarial. Jump to the "Large tier" section.

---

### Medium tier (50-199 lines)

Claude's structured review already ran. Now add a **cross-model adversarial challenge**.

**If Codex is available:** spawn the `avadbot:avad-codex` agent in challenge mode. **If Codex is NOT available:** fall back to the `avadbot:avad-adversarial` agent instead.

**Codex adversarial (primary):**

Spawn the `avadbot:avad-codex` agent via the Agent tool.

Agent prompt: "challenge — base branch: <target>. Find ways this code will fail in production."

Present findings under a `CODEX SAYS (adversarial challenge):` header. This is informational — it never blocks shipping.

**Error handling:** All errors are non-blocking — adversarial review is a quality enhancement, not a prerequisite.
On any Codex error (CLI not found, auth failure, timeout), fall back to the Claude adversarial agent automatically.

**Claude adversarial agent** (fallback when Codex unavailable or errored):

Spawn the `avadbot:avad-adversarial` agent via the Agent tool. The agent has fresh context — no checklist bias from the structured review. This genuine independence catches things the primary reviewer is blind to.

Agent prompt: "Base branch: <target>. Run your adversarial review."

Present findings under an `ADVERSARIAL REVIEW (Claude agent):` header. **FIXABLE findings** are collected for Step 6 (Fix-First). **INVESTIGATE findings** are presented as informational.

If the agent fails or times out: "Claude adversarial agent unavailable. Continuing without adversarial review."

---

### Large tier (200+ lines)

Claude's structured review already ran. Now run **all three remaining passes** for maximum coverage.

> **IMPORTANT — Codex CLI concurrency:** The Codex CLI uses internal state files that
> conflict when two instances run simultaneously in the same working directory.
> **Never spawn two `avadbot:avad-codex` agents in parallel.** Run them sequentially.
> Claude adversarial is safe to run in parallel with any Codex agent.

**Round 1 (parallel):** Launch these two agents at the same time:

- **Codex structured review (if available):** Spawn the `avadbot:avad-codex` agent in review mode.
  Agent prompt: "review — base branch: <target>."
- **Claude adversarial agent:** Spawn the `avadbot:avad-adversarial` agent (same prompt as medium tier).
  This always runs regardless of Codex availability.

Wait for both to complete.

Present Codex output under a `CODEX SAYS (code review):` header. Check for `[P0]` or `[P1]` markers: found → `GATE: FAIL`, not found → `GATE: PASS`.

If GATE is FAIL, use AskUserQuestion:
```
Codex found N critical issues in the diff.

A) Investigate and fix now (recommended)
B) Continue — review will still complete
```

If A: address the findings.

**Round 2 (sequential, after Round 1 completes):**

- **Codex adversarial challenge (if available):** Spawn the `avadbot:avad-codex` agent in challenge mode (same prompt as medium tier).

If Codex is not available for the Codex steps, note to the user: "Codex CLI not found — large-diff review ran Claude structured + Claude adversarial (2 of 4 passes). Install Codex for full 4-pass coverage: `npm install -g @openai/codex`"

---

### Adversarial synthesis (medium and large tiers)

After all adversarial passes complete, synthesize findings across all sources:

```
ADVERSARIAL REVIEW SYNTHESIS (auto: TIER, N lines):
════════════════════════════════════════════════════════════
  High confidence (found by multiple sources): [findings agreed on by >1 pass]
  Unique to Claude structured review: [from Steps 5–5.75]
  Unique to Claude adversarial: [from agent, if ran]
  Unique to Codex: [from codex adversarial or code review, if ran]
  Models used: Claude structured ✓  Claude adversarial ✓/✗  Codex ✓/✗
════════════════════════════════════════════════════════════
```

High-confidence findings (agreed on by multiple sources) should be prioritized for fixes.

After synthesis, proceed to Step 6 with all findings collected.

---

## Step 6: Fix-First Output

**Every finding gets action — not just critical ones.**

Collect findings from ALL review passes: structured review (Step 5), design review (Step 5.5), test coverage (Step 5.75), doc staleness (Step 5.6), and adversarial review (Step 5.8). Process them together.

Output a summary header: `Pre-Landing Review: N issues (X critical, Y informational)`

### Step 6a: Classify each finding

For each finding, classify as AUTO-FIX or ASK:

- **AUTO-FIX** (mechanical, no judgment needed): dead code removal, stale comments, missing imports, N+1 query fixes, obvious typos, mechanical CSS fixes
- **ASK** (requires judgment): security changes, race condition fixes, design decisions, architecture changes, anything where reasonable people could disagree

Critical findings lean toward ASK; informational findings lean toward AUTO-FIX.

### Step 6b: Auto-fix all AUTO-FIX items

**Local mode only.** Apply each fix directly. For each one, output a one-line summary:
`[AUTO-FIXED] [file:line] Problem → what you did`

**PR mode:** Do NOT apply fixes (you don't have the PR branch checked out). Instead, list what would be auto-fixed:
`[AUTO-FIXABLE] [file:line] Problem → suggested fix`

### Step 6c: Handle ASK items

#### Local mode:

If there are ASK items, present them in ONE AskUserQuestion:

- List each item with a number, the severity label, the problem, and a recommended fix
- For each item: A) Fix as recommended, B) Skip
- Include an overall RECOMMENDATION

Example:
```
I auto-fixed 5 issues. 2 need your input:

1. [CRITICAL] app/models/post.rb:42 — Race condition in status transition
   Fix: Add `WHERE status = 'draft'` to the UPDATE
   → A) Fix  B) Skip

2. [INFORMATIONAL] app/services/generator.rb:88 — LLM output not type-checked
   Fix: Add JSON schema validation
   → A) Fix  B) Skip

RECOMMENDATION: Fix both — #1 is a real race condition, #2 prevents silent data corruption.
```

If 3 or fewer ASK items, you may use individual AskUserQuestion calls instead of batching.

#### PR mode:

Post findings as a PR review using `gh pr review`:

```bash
gh pr review <number> --comment --body "$(cat <<'EOF'
## Pre-Landing Review: N issues (X critical, Y informational)

**AUTO-FIXED:**
- [file:line] Problem → fix applied

**CRITICAL:**
- [file:line] Problem description
  Fix: suggested fix

**Issues:**
- [file:line] Problem description
  Fix: suggested fix

---
_Review by /avad-review · {YYYY-MM-DD}_
EOF
)"
```

If CRITICAL issues found, use `--request-changes` instead of `--comment`.
If no issues found, use `--approve` with body `Pre-Landing Review: No issues found.`

### Step 6d: Apply user-approved fixes

Apply fixes for items where the user chose "Fix." Output what was fixed.
If no ASK items exist (everything was AUTO-FIX), skip the question entirely.

### Bot comment resolution (if Step 4.5 found any):

Append a section to the PR review body:

```
## Bot Review Triage: N comments (X valid, Y already fixed, Z false positive)
```

For each classified comment:

- **VALID & ACTIONABLE:** Include in the CRITICAL findings above — same flow.
  If user chooses "Fix now": apply fix, reply to bot comment `"Fixed in <commit-sha>."`,
  save to history (type: fix).
- **VALID BUT ALREADY FIXED:** Reply to the bot comment **without @mentioning the bot**:
  `"Good catch — already fixed in <commit-sha>."`
  Save to history (type: already-fixed).
- **FALSE POSITIVE:** Reply to the bot comment **without @mentioning the bot**,
  explaining why it's incorrect.
  Save to history (type: fp).
- **SUPPRESSED:** Skip silently.

### History writes

After triage, append one line per outcome to **both** files:

```bash
REMOTE_SLUG=$(basename "$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)" 2>/dev/null || basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
mkdir -p "$HOME/.avadbot/projects/$REMOTE_SLUG"
```

- `~/.avadbot/projects/$REMOTE_SLUG/bot-review-history.md` (per-project — for suppressions)
- `~/.avadbot/bot-review-history.md` (global — for retro/trends)

Format:
```
<YYYY-MM-DD> | <owner/repo> | <bot> | <type> | <file-pattern> | <category>
```

**Bot mention rule:** Never @mention bots in individual comment replies — each mention
triggers the bot to run again, causing spam and rate limiting. Instead, include a single
summary mention in the main review body. This triggers each bot **once** to review the
summary, not once per comment.

---

## Important Rules

- **Read the FULL diff before commenting.** Do not flag issues already addressed in the diff.
- **Fix-first, not read-only.** AUTO-FIX items are applied directly. ASK items are only applied after user approval. Never commit, push, or create PRs — that's /avad-ship's job.
- **Be terse.** One line problem, one line fix. No preamble.
- **Only flag real problems.** Skip anything that's fine.
