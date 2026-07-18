---
name: ce-work
description: Execute a plan or concrete work prompt end-to-end. Use when implementing from docs/plans, a spec path, or a clear build request; use ce-debug for open-ended bugs.
argument-hint: "[Plan doc path or description of work. Blank to auto use latest plan doc]"
---

<!-- TRACEWEAVER: file-role=manual-continuity-worker-skill; req=REQ-TW-054; trace=TRACE-TW-035; ver=VER-TW-044 -->

# Work Execution Command

Execute work efficiently while maintaining quality and finishing features.

## TraceWeaver Package Boundary

When this `ce-work` skill is installed by the TraceWeaver plugin, direct
invocation is a legacy/manual-continuity surface and must still run in
TraceWeaver publication-gated mode for the current alpha. It is not, by itself,
a TraceWeaver-authority-enforced workflow, and it cannot close TraceWeaver
authority, traceability, verification, validation, commit, push, or PR gates
without the controlled TraceWeaver publication route passing.

For TraceWeaver-controlled implementation, use `tw-auto`, which routes the
implementation phase through `tw-work`. Direct `ce-work` is only the underlying
compatibility worker and should not be the user-facing TraceWeaver work-loop
surface. If manually composing the sequence, run:

```text
tw-authority-gate
-> tw-work
-> ce-work no-publication implementation engine
-> tw-traceability-check
-> ce-code-review / ce-doc-review
```

Before changing meaningful behavior in TraceWeaver-controlled work, load the
project root `requirements.md`, `.traceweaver/intent-contract.yml`, and
`traceability-matrix.md`. If approved authority, validation intent, or required
verification evidence is missing, stop and create or recommend a gap, change,
exception, accepted-risk candidate, or clarification record. Do not treat a plan,
bare prompt, task ID, or agent interpretation as authority by itself.

If the user explicitly asks for legacy/manual CE work anyway, proceed only in
publication-gated mode. State in the output that the work does not close
TraceWeaver authority, traceability, verification, validation, commit, push, or
PR gates until `tw-authority-gate`, matrix updates, `tw-traceability-check`, and
the controlled TraceWeaver publication route pass.

### TraceWeaver Controlled Publication-Gated Mode

When this skill is installed by TraceWeaver, enter publication-gated mode before
Phase 0 for every invocation. The implementation phase remains non-publishing;
publication can only happen later through the controlled TraceWeaver publication
route:

- keep the authority capsule, approved requirements/exceptions, validation
  question, verification target, and matrix-update requirement visible while
  working;
- implement and test only the authorized behavior;
- update trace evidence or report the exact trace gap before claiming completion;
- do not stage files, create commits, push, open PRs, create issues, update plan
  status to `completed`, or load `ce-commit`, `ce-commit-push-pr`, or Phase 4
  shipping instructions unless the controlled TraceWeaver publication route
  authorizes that specific target after authority, traceability, verification,
  review, staged-tree, credential, and remote-boundary checks pass;
- do not allow subagents to stage, commit, push, or publish during
  implementation, even in isolated worktrees;
- after implementation, tests, trace updates, and review handoff are complete,
  return control to `tw-work` or `tw-auto` with changed files, verification
  evidence, matrix status, open gaps, held claims, and the next required review
  or human decision.

If any later instruction in this skill or its references conflicts with
TraceWeaver publication-gated mode, the TraceWeaver boundary wins and the
publication step is skipped unless the controlled publication route has already
authorized it.

## Introduction

This command takes a work document (plan or specification) or a bare prompt describing the work, and executes it systematically. The focus is on **shipping complete features** by understanding requirements quickly, following existing patterns, and maintaining quality throughout.

## Input Document

<input_document> #$ARGUMENTS </input_document>

## Execution Workflow

### Phase 0: Input Triage

Determine how to proceed based on what was provided in `<input_document>`.

**Plan document** (input is a file path to an existing plan or specification): read the plan's metadata first — YAML frontmatter for a markdown plan, or the visible header text for an HTML plan (both formats carry the same fields). If it carries `execution: knowledge-work`, this is a **non-code plan** — read `references/non-code-execution.md` and follow that carve-out instead of the rest of this workflow. Otherwise (the field is absent or `execution: code`) → skip to Phase 1 and run the normal code lifecycle. (The marker check lives here, inside plan-document handling, because detecting the marker requires already having a file; "Bare prompt" below is unaffected.)

**Bare prompt** (input is a description of work, not a file path):

1. **Scan the work area**

   - Identify files likely to change based on the prompt
   - Find existing test files for those areas (search for test/spec files that import, reference, or share names with the implementation files)
   - Note local patterns and conventions in the affected areas

2. **Assess complexity and route**

   | Complexity | Signals | Action |
   |-----------|---------|--------|
   | **Trivial** | 1-2 files, no behavioral change (typo, config, rename) | Proceed to Phase 1 step 2 (environment setup), then implement directly — no task list, no execution loop. Apply Test Discovery if the change touches behavior-bearing code |
   | **Small / Medium** | Clear scope, under ~10 files | Build a task list from discovery. Proceed to Phase 1 step 2 |
   | **Large** | Cross-cutting, architectural decisions, 10+ files, touches auth/payments/migrations | Inform the user this would benefit from `/ce-brainstorm` or `/ce-plan` to surface edge cases and scope boundaries. Honor their choice. If proceeding, build a task list and continue to Phase 1 step 2 |

---

### Phase 1: Quick Start

1. **Read Plan and Clarify** _(skip if arriving from Phase 0 with a bare prompt)_

   - Read the work document completely. Plans may be markdown (`.md`) or HTML (`.html`) — both formats are read as text linearly. HTML plans carry the same section names and IDs as markdown plans, just wrapped in semantic HTML elements (`<section>`, `<article>`, etc.); section-finding works the same way (substring match on section names, ignoring HTML wrapper noise).
   - When auto-detecting the latest plan (blank invocation), glob `docs/plans/*.md` AND `docs/plans/*.html` and pick the most recent regardless of extension.
   - Treat the plan as a decision artifact, not an execution script
   - If the plan includes sections such as `Implementation Units`, `Work Breakdown`, `Requirements` (or legacy `Requirements Trace`), `Files`, `Test Scenarios`, or `Verification`, use those as the primary source material for execution
   - Check for `Execution note` on each implementation unit — these carry the plan's execution posture signal for that unit (for example, test-first or characterization-first). Note them when creating tasks.
   - Check for a `Deferred to Implementation` or `Implementation-Time Unknowns` section — these are questions the planner intentionally left for you to resolve during execution. Note them before starting so they inform your approach rather than surprising you mid-task
   - Check for a `Scope Boundaries` section — these are explicit non-goals. Refer back to them if implementation starts pulling you toward adjacent work
   - Review any references or links provided in the plan
   - If the user explicitly asks for TDD, test-first, or characterization-first execution in this session, honor that request even if the plan has no `Execution note`
   - If anything is unclear or ambiguous, ask clarifying questions now
   - If clarifying questions were needed above, get user approval on the resolved answers. If no clarifications were needed, proceed without a separate approval step — plan scope is the plan's authority, not something to renegotiate
   - **Do not skip this** - better to ask questions now than build the wrong thing
   - **Do not edit the plan body during execution.** The plan is a decision artifact; progress lives in task state, verification evidence, trace records, and the final held-publication handoff, not the plan. `ce-work` does not mutate the plan — whether it shipped is derived from the later controlled TraceWeaver publication route, not recorded in the doc. Legacy plans may contain `- [ ]` / `- [x]` marks on unit headings or a `status:` field — ignore them as state; per-unit completion is determined during execution by reading the current file state.

2. **Setup Environment**

   First, check the current branch:

   ```bash
   current_branch=$(git branch --show-current)
   default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')

   # Fallback if remote HEAD isn't set
   if [ -z "$default_branch" ]; then
     default_branch=$(git rev-parse --verify origin/main >/dev/null 2>&1 && echo "main" || echo "master")
   fi
   ```

   **If already on a feature branch** (not the default branch):

   First, check whether the branch name is **meaningful** — a name like `feat/crowd-sniff` or `fix/email-validation` tells future readers what the work is about. Auto-generated worktree names (e.g., `worktree-jolly-beaming-raven`) or other opaque names do not.

   If the branch name is meaningless or auto-generated, suggest renaming it before continuing:
   ```bash
   git branch -m <meaningful-name>
   ```
   Derive the new name from the plan title or work description (e.g., `feat/crowd-sniff`). Present the rename as a recommended option alongside continuing as-is.

   Then ask: "Continue working on `[current_branch]`, or create a new branch?"
   - If continuing (with or without rename), proceed to step 3
   - If creating new, follow Option A or B below

   **If on the default branch**, choose how to proceed:

   **Option A: Create a new branch**
   ```bash
   git pull origin [default_branch]
   git checkout -b feature-branch-name
   ```
   Use a meaningful name based on the work (e.g., `feat/user-authentication`, `fix/email-validation`).

   **Option B: Use a worktree (recommended for parallel development)**
   ```bash
   skill: ce-worktree
   # Ensures isolation: detects an existing worktree, prefers the harness's
   # native worktree tool, else creates one from the default branch
   ```

   **Option C: Continue on the default branch**
   - Requires explicit user confirmation
   - Only proceed after user explicitly says to continue on `[default_branch]`
     under TraceWeaver no-publication mode
   - Never stage, commit, push, or publish directly from `ce-work`

   **Recommendation**: Use worktree if:
   - You want to work on multiple features simultaneously
   - You want to keep the default branch clean while experimenting
   - You plan to switch between branches frequently

3. **Create Task List** _(skip if Phase 0 already built one, or if Phase 0 routed as Trivial)_
   - Use the platform's task tracking tool (`TaskCreate`/`TaskUpdate`/`TaskList` in Claude Code, `update_plan` in Codex, or the equivalent on other harnesses) to break the plan into actionable tasks
   - Derive tasks from the plan's implementation units, dependencies, files, test targets, and verification criteria
   - When the plan defines U-IDs for Implementation Units, preserve the unit's U-ID as a prefix in the task subject (e.g., "U3: Add parser coverage"). This keeps blocker references, deferred-work notes, and final summaries anchored to the same identifier the plan uses, so progress and traceability remain unambiguous across plan edits
   - Carry each unit's `Execution note` into the task when present
   - For each unit, read the `Patterns to follow` field before implementing — these point to specific files or conventions to mirror
   - Use each unit's `Verification` field as the primary "done" signal for that task
   - Do not expect the plan to contain implementation code, micro-step TDD instructions, or exact shell commands
   - Include dependencies between tasks
   - Prioritize based on what needs to be done first
   - Include testing and quality check tasks
   - Keep tasks specific and completable

4. **Choose Execution Strategy**

   After creating the task list, decide how to execute based on the plan's size and dependency structure:

   | Strategy | When to use |
   |----------|-------------|
   | **Inline** | 1-2 small tasks, or tasks needing user interaction mid-flight. **Default for bare-prompt work** — bare prompts rarely produce enough structured context to justify subagent dispatch |
   | **Serial subagents** | 3+ tasks with dependencies between them. Each subagent gets a fresh context window focused on one unit — prevents context degradation across many tasks. Requires plan-unit metadata (Goal, Files, Approach, Test scenarios) |
   | **Parallel subagents** | 3+ tasks that pass the Parallel Safety Check (below). Dispatch independent units simultaneously, run dependent units after their prerequisites complete. Requires plan-unit metadata |

   **Parallel Safety Check** — required before choosing parallel dispatch:

   1. Build a file-to-unit mapping from every candidate unit's `Files:` section (Create, Modify, and Test paths)
   2. Check for intersection — any file path appearing in 2+ units means overlap
   3. **If overlap is found AND worktree isolation is unavailable**: downgrade to serial subagents. Log the reason (e.g., "Units 2 and 4 share `config/routes.rb` — using serial dispatch"). Serial subagents still provide context-window isolation without shared-directory write races.
   4. **If overlap is found AND worktree isolation is available**: parallel dispatch is still safe — subagents work in isolation, and the overlap surfaces as a predictable merge conflict the orchestrator handles via the post-batch flow below. Log the predicted overlap so the post-batch flow knows which merges to expect conflicts on.

   Even with no file overlap, parallel subagents sharing the orchestrator's working directory face git index contention (concurrent staging/committing corrupts the index) and test interference (concurrent test runs pick up each other's in-progress changes). Worktree isolation eliminates both; the shared-directory fallback constraints below mitigate them.

   **Subagent isolation** — give each parallel subagent its own working tree:
   - **Claude Code (`Agent` tool):** pass `isolation: "worktree"` and `run_in_background: true`. The harness creates a per-subagent worktree under `.claude/worktrees/agent-<id>` on its own branch. Verify `.claude/worktrees/` is gitignored before relying on this.
   - **Other platforms** without built-in worktree isolation: subagents share the orchestrator's directory.

   **Subagent dispatch** uses your available subagent or task spawning mechanism. For each unit, give the subagent:
   - The full plan file path (for overall context)
   - The specific unit's Goal, Files, Approach, Execution note, Patterns, Test scenarios, and Verification
   - Any resolved deferred questions relevant to that unit
   - Instruction to check whether the unit's test scenarios cover all applicable categories (happy paths, edge cases, error paths, integration) and supplement gaps before writing tests

   **TraceWeaver subagent constraints** — apply in every isolation mode:
   - Instruct each subagent: "Do not stage files (`git add`), create commits,
     push branches, publish, or open/update PRs. Return changed files,
     verification performed, and any unresolved gaps to the orchestrator."
   - In shared-directory fallback, also instruct subagents not to run the full
     project test suite concurrently. The orchestrator handles combined
     validation after each batch.
   - With worktree isolation active, subagents may run their unit's targeted
     tests inside the isolated worktree, but they still must not stage, commit,
     push, or publish. Any branch created by the harness is an implementation
     workspace only, not a publication branch.

   **Permission mode:** Omit the `mode` parameter when dispatching subagents so the user's configured permission settings apply. Do not pass `mode: "auto"` — it overrides user-level settings like `bypassPermissions`.

   **After each subagent completes (serial mode):**
   1. Review the subagent's diff — verify changes match the unit's scope and `Files:` list
   2. Run the relevant test suite to confirm the tree is healthy
   3. If tests fail, diagnose and fix before proceeding — do not dispatch dependent units on a broken tree
   4. Update the task list (do not edit the plan body — progress is carried by the task state and held-publication handoff)
   5. Dispatch the next unit

   **After all parallel subagents in a batch complete (worktree-isolated mode):**
   1. Wait for every subagent in the current parallel batch to finish.
   2. For each completed subagent, in dependency order: review the worktree's
      diff against the orchestrator's branch. Do not stage or commit inside the
      subagent worktree.
   3. Integrate accepted changes only as an uncommitted diff in the orchestrator
      workspace using harness-supported no-commit patch integration, or rerun
      the unit serially in the orchestrator workspace when patch integration is
      unsafe. Do not merge subagent branches or create merge commits from
      `ce-work`.
   4. After each accepted integration, run the relevant test suite. If tests
      fail, diagnose and fix before integrating the next unit.
   5. Update the task list; progress is carried by changed files, verification
      evidence, and held-publication handoff entries.
   6. After integration, remove each subagent's worktree and delete its branch
      only when doing so will not discard unintegrated work. Use the absolute
      path and branch name returned in the subagent's result.
      - Unlock the worktree first — the harness locks per-subagent worktrees: `git worktree unlock <absolute-path>`
      - Remove the worktree: `git worktree remove <absolute-path>`
      - Delete the branch: `git branch -d <branch-name>` (the branch outlives the worktree by default and accumulates as orphans if not cleaned up; `-d` lowercase refuses to delete unmerged branches, which is the safety we want — if it fails, investigate before forcing)
   7. Dispatch the next batch of independent units, or the next dependent unit.

   **After all parallel subagents in a batch complete (shared-directory fallback):**
   1. Wait for every subagent in the current parallel batch to finish before acting on any of their results
   2. Cross-check for discovered file collisions: compare the actual files modified by all subagents in the batch (not just their declared `Files:` lists). Subagents may create or modify files not anticipated during planning — this is expected, since plans describe *what* not *how*. A collision only matters when 2+ subagents in the same batch modified the same file. In a shared working directory, only the last writer's version survives — the other unit's changes to that file are lost. If a collision is detected, keep non-colliding changes as uncommitted work and re-run the affected units serially for the shared file so each builds on the other's current work.
   3. For each completed unit, in dependency order: review the diff, run the relevant test suite, and record the changed files plus proposed commit boundary in the held-publication handoff. Do not stage or commit.
   4. If tests fail after a unit's changes, diagnose and fix before moving to the next unit.
   5. Update the task list (do not edit the plan body — progress is carried by task state, changed files, and verification evidence)
   6. Dispatch the next batch of independent units, or the next dependent unit

### Phase 2: Execute

1. **Task Execution Loop**

   For each task in priority order:

   ```
   while (tasks remain):
     - Mark task as in-progress
     - Read any referenced files from the plan or discovered during Phase 0
     - **If the unit's work is already present and matches the plan's intent** (files exist with the expected capability, or the unit's `Verification` criteria are already satisfied by the current code), the work has likely shipped on a prior branch or session. Verify it matches, mark the task complete, and move on. Do not silently reimplement.
     - Look for similar patterns in codebase
     - Find existing test files for implementation files being changed (Test Discovery — see below)
     - Implement following existing conventions
     - Add, update, or remove tests to match implementation changes (see Test Discovery below)
     - Run System-Wide Test Check (see below)
     - Run tests after changes
     - Assess testing coverage: did this task change behavior? If yes, were tests written or updated? If no tests were added, is the justification deliberate (e.g., pure config, no behavioral change)?
     - Mark task as completed
    - Evaluate for an incremental checkpoint (see below)
   ```

   When a unit carries an `Execution note`, honor it. For test-first units, write the failing test before implementation for that unit. For characterization-first units, capture existing behavior before changing it. For units without an `Execution note`, proceed pragmatically.

   Guardrails for execution posture:
   - Do not write the test and implementation in the same step when working test-first
   - Do not skip verifying that a new test fails before implementing the fix or feature
   - Do not over-implement beyond the current behavior slice when working test-first
   - Skip test-first discipline for trivial renames, pure configuration, and pure styling work

   **Test Discovery** — Before implementing changes to a file, find its existing test files (search for test/spec files that import, reference, or share naming patterns with the implementation file). When a plan specifies test scenarios or test files, start there, then check for additional test coverage the plan may not have enumerated. Changes to implementation files should be accompanied by corresponding test updates — new tests for new behavior, modified tests for changed behavior, removed or updated tests for deleted behavior.

   **Test Scenario Completeness** — Before writing tests for a feature-bearing unit, check whether the plan's `Test scenarios` cover all categories that apply to this unit. If a category is missing or scenarios are vague (e.g., "validates correctly" without naming inputs and expected outcomes), supplement from the unit's own context before writing tests:

   | Category | When it applies | How to derive if missing |
   |----------|----------------|------------------------|
   | **Happy path** | Always for feature-bearing units | Read the unit's Goal and Approach for core input/output pairs |
   | **Edge cases** | When the unit has meaningful boundaries (inputs, state, concurrency) | Identify boundary values, empty/nil inputs, and concurrent access patterns |
   | **Error/failure paths** | When the unit has failure modes (validation, external calls, permissions) | Enumerate invalid inputs the unit should reject, permission/auth denials it should enforce, and downstream failures it should handle |
   | **Integration** | When the unit crosses layers (callbacks, middleware, multi-service) | Identify the cross-layer chain and write a scenario that exercises it without mocks |

   **System-Wide Test Check** — Before marking a task done, pause and ask:

   | Question | What to do |
   |----------|------------|
   | **What fires when this runs?** Callbacks, middleware, observers, event handlers — trace two levels out from your change. | Read the actual code (not docs) for callbacks on models you touch, middleware in the request chain, `after_*` hooks. |
   | **Do my tests exercise the real chain?** If every dependency is mocked, the test proves your logic works *in isolation* — it says nothing about the interaction. | Write at least one integration test that uses real objects through the full callback/middleware chain. No mocks for the layers that interact. |
   | **Can failure leave orphaned state?** If your code persists state (DB row, cache, file) before calling an external service, what happens when the service fails? Does retry create duplicates? | Trace the failure path with real objects. If state is created before the risky call, test that failure cleans up or that retry is idempotent. |
   | **What other interfaces expose this?** Mixins, DSLs, alternative entry points (Agent vs Chat vs ChatMethods). | Grep for the method/behavior in related classes. If parity is needed, add it now — not as a follow-up. |
   | **Do error strategies align across layers?** Retry middleware + application fallback + framework error handling — do they conflict or create double execution? | List the specific error classes at each layer. Verify your rescue list matches what the lower layer actually raises. |

   **When to skip:** Leaf-node changes with no callbacks, no state persistence, no parallel interfaces. If the change is purely additive (new helper method, new view partial), the check takes 10 seconds and the answer is "nothing fires, skip."

   **When this matters most:** Any change that touches models with callbacks, error handling with fallback/retry, or functionality exposed through multiple interfaces.


2. **Incremental Checkpoints**

   After completing each task, evaluate whether to record an incremental
   checkpoint for the later controlled publication route:

   | Record a checkpoint when... | Don't record a checkpoint when... |
   |----------------|---------------------|
   | Logical unit complete (model, service, component) | Small part of a larger unit |
   | Tests pass + meaningful progress | Tests failing |
   | About to switch contexts (backend → frontend) | Purely scaffolding with no behavior |
   | About to attempt risky/uncertain changes | Would need a "WIP" commit message |

   **Heuristic:** "Can I write a proposed commit message that describes a complete, valuable change? If yes, record the boundary. If the message would be 'WIP' or 'partial X', wait."

   If the plan has Implementation Units, use them as a starting guide for later
   commit boundaries — but adapt based on what you find during implementation. A
   unit might need multiple later commits if it's larger than expected, or small
   related units might land together. Use each unit's Goal to inform the
   proposed commit message.

   **Checkpoint workflow:**
   1. Verify tests pass (use the project's test command).
   2. Record the files related to this logical unit.
   3. Draft a conventional proposed commit message, e.g.
      `feat(scope): description of this unit`.
   4. Keep files unstaged and uncommitted. Commit creation belongs to the later
      controlled TraceWeaver publication route.

   **Handling integration conflicts:** If conflicts arise while integrating
   parallel work, resolve them immediately or rerun the affected unit serially.
   Incremental checkpoints make conflict review easier because each proposed
   boundary is small and focused.

   **Note:** Incremental checkpoints use clean proposed conventional messages without attribution footers. The later controlled publication route decides final commit/PR attribution.

   **Parallel subagent mode:** Publication remains held in every isolation mode
   (see Phase 1 Step 4):
   - **Worktree-isolated:** subagents return diffs and verification evidence;
     they do not stage, commit, push, or publish.
   - **Shared-directory fallback:** subagents return changed files and
     verification notes; the orchestrator records proposed commit boundaries
     after the batch completes without staging or committing.

3. **Follow Existing Patterns**

   - The plan should reference similar code - read those files first
   - Match naming conventions exactly
   - Reuse existing components where possible
   - Follow the project's coding standards already in your context
   - When in doubt, grep for similar implementations

4. **Test Continuously**

   - Run relevant tests after each significant change
   - Don't wait until the end to test
   - Fix failures immediately
   - Add new tests for new behavior, update tests for changed behavior, remove tests for deleted behavior
   - **Unit tests with mocks prove logic in isolation. Integration tests with real objects prove the layers work together.** If your change touches callbacks, middleware, or error handling — you need both.

5. **Simplify as You Go**

   After completing a cluster of related implementation units (or every 2-3 units), review recently changed files for simplification opportunities — consolidate duplicated patterns, extract shared helpers, and improve code reuse and efficiency. This is especially valuable when using subagents, since each agent works with isolated context and can't see patterns emerging across units.

   Don't simplify after every single unit — early patterns may look duplicated but diverge intentionally in later units. Wait for a natural phase boundary or when you notice accumulated complexity.

   If **`ce-simplify-code`** is available, invoke it at phase boundaries (especially before Phase 3 when the diff is >=30 lines). Otherwise, review the changed files yourself for reuse and consolidation opportunities.

6. **Figma Design Sync** (if applicable)

   For UI work with Figma designs:

   - Implement components following design specs
   - Read `references/agents/figma-design-sync.md` and dispatch a generic subagent seeded with that local prompt to compare implementation against the Figma design. Do not dispatch a standalone agent by type/name.
   - Fix visual differences identified
   - Repeat until implementation matches design

7. **Frontend Design Guidance** (if applicable)

   For UI tasks without a Figma design -- where the implementation touches view, template, component, layout, or page files, creates user-visible routes, or the plan contains explicit UI/frontend/design language:

   - Apply the frontend guidance embedded in this skill and the active repo instructions: preserve existing design-system conventions, use real UI controls and states, keep layouts responsive, and verify text does not overflow or overlap.
   - When browser tooling is available, inspect the changed UI at desktop and mobile widths before final validation. If no browser access is available, do a code-level responsive/layout review and record that browser verification was unavailable.
   - Phase 4's screenshot capture still applies when the change is user-visible.

8. **Track Progress**
   - Keep the task list updated as you complete tasks
   - Note any blockers or unexpected discoveries
   - Create new tasks if scope expands
   - Keep user informed of major milestones
   - When the plan defines U-IDs for Implementation Units, or the plan or origin document carries stable R-IDs (and optionally A/F/AE IDs), reference them in blockers, deferred-work notes, task summaries, and final verification — not routine status updates. U-IDs anchor units across plan edits; R/A/F/AE anchor product intent across the brainstorm-plan handoff. Use the IDs the plan supplies and do not invent ones it does not. This preserves traceability without burying signal under noise.

### Phase 3-4: Quality Check and Held Publication Handoff

When all Phase 2 tasks are complete and execution transitions to quality check,
continue in TraceWeaver no-publication mode. Do not read or load
`references/shipping-workflow.md`, `ce-commit`, or `ce-commit-push-pr` unless a
controlled TraceWeaver publication route has already authorized that exact
target. The shipping workflow remains upstream CE reference material only.

**Code review tiers:** Tier 1 when the harness has built-in review. Tier 2 only when the escalation criteria below match — not because Tier 1 is missing.

**Tier 2 is two steps — review, then fix.** `ce-code-review` is review-only. It returns findings (markdown or `mode:agent` JSON); it never edits the checkout, commits, or applies fixes.

When Tier 2 applies:

1. **Review** — Invoke the `ce-code-review` skill (invocation command in `references/review-findings-followup.md` § Fallback). Use `mode:agent` in orchestrated workflows; pass `plan:<path>` when you have a plan and `base:<ref>` when the merge base is already known.
2. **Apply fixes** — Load `references/review-findings-followup.md`. Filter eligibility on JSON only, **batch applicable findings by file**, dispatch fix subagents (parallel when file sets are disjoint). The orchestrator integrates diffs without staging or committing, runs tests, and records the changed files and proposed publication handoff — it does not pre-investigate findings.
3. **Residual Work Gate** — Only after followup; unresolved actionable findings go through the held residual-work gate described by the TraceWeaver publication handoff.

Tier 1 harness-native review may still fix inline; Tier 2 always separates review from apply.

## Key Principles

### Start Fast, Execute Faster

- Get clarification once at the start, then execute
- Don't wait for perfect understanding - ask questions and move
- The goal is to **finish the feature**, not create perfect process

### The Plan is Your Guide

- Work documents should reference similar code and patterns
- Load those references and follow them
- Don't reinvent - match what exists

### Test As You Go

- Run tests after each change, not at the end
- Fix failures immediately
- Continuous testing prevents big surprises

### Quality is Built In

- Follow existing patterns
- Write tests for new code
- Run linting before the held publication handoff
- Review when Tier 1 is available or Tier 2 criteria match; keep publication held

### Finish Complete Features

- Mark all implementation tasks ready for review before moving on
- Don't leave features 80% done
- A complete, verified handoff beats an incomplete implementation with a
  premature publication claim

## Common Pitfalls to Avoid

- **Analysis paralysis** - Don't overthink, read the plan and execute
- **Skipping clarifying questions** - Ask now, not after building wrong thing
- **Ignoring plan references** - The plan has links for a reason
- **Testing at the end** - Test continuously or suffer later
- **Forgetting to track progress** - Update task status as you go or lose track of what's done
- **80% done syndrome** - Finish the feature, don't move on early
- **Skipping review without reason** — Use Tier 1 when available; escalate to Tier 2 only on the criteria above; document when both are skipped
- **Re-scoping the plan into human-time phases** - The plan's Implementation Units define the scope of execution. Do not estimate human-hours per unit, propose multi-day breakdowns, or ask the user to pick a subset of units for "this session". Agents execute at agent speed, and context-window pressure is addressed by subagent dispatch (Phase 1 Step 4), not by phased sessions. If a plan-file input is genuinely too large for a single execution, say so plainly and suggest the user return to `/ce-plan` to reduce scope — don't invent session phases as a workaround. For bare-prompt input, Phase 0's Large routing already handles oversized work
