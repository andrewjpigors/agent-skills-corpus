---
name: rptc-fix
description: Reproduction -> Root Cause -> Fix -> Verification. Use when the user asks for /rptc:fix or the equivalent RPTC Codex workflow intent.
---

# RPTC Fix
Systematic bug fixing: Reproduction → Root Cause Analysis → Fix → Verification.

## Step 0: RPTC Workflow Initialization (MANDATORY - CANNOT SKIP)

**Before ANY other action, establish RPTC workflow context.**

### 0.1 Load Required Skills (ALL FIVE MANDATORY)

Load ALL five skills below. Each skill load is MANDATORY - do not skip any.

```
Use/load the `rptc:tool-guide` skill.
Use/load the `rptc:brainstorming` skill.
Use/load the `rptc:writing-clearly-and-concisely` skill.
Use/load the `rptc:tdd-methodology` skill.
Use/load the `rptc:structure-methodology` skill.
```

After loading, confirm all five loaded. If ANY skill fails to load, STOP and report the failure.

> **Note**: Codex omits Claude's persistent team commands. For batch work across independent bugs, use parent-orchestrated `spawn_agent` delegation with clear ownership boundaries.

### 0.1.1 Conditional Skills (Load When Applicable)

**Frontend work** — If the bug involves HTML, CSS, UI components, web pages, or frontend interfaces:

```
Use/load the `rptc:frontend-design` skill.
```

> Provides creative direction and distinctive aesthetics. Complements the RPTC `frontend-guidelines.md` SOP (loaded via the SOP Reference Chain): the SOP ensures correctness (accessibility, performance, responsive), the skill ensures distinction (bold aesthetics, memorable design).

> **IMPORTANT**: If the project already has an established design system, style guide, or visual aesthetic, the skill's creative direction MUST work within those constraints. Research existing styles first (CSS variables, component library, brand guidelines) and preserve them — do not introduce a conflicting aesthetic when fixing bugs. The skill adds polish and intentionality, not a new identity.

### 0.1.2 Activate Serena MCP (MANDATORY)

Serena tools are **deferred** in the main context — they require explicit loading before they can be called.

Call ToolSearch now to activate them:

```
ToolSearch(query: "serena")
```

Once loaded, Serena tools appear as `mcp__serena__*` or `mcp__plugin_serena_serena__*`. This activates both read tools (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, etc.) and edit tools (`replace_symbol_body`, `insert_after_symbol`, etc.). Use them throughout this workflow — refer to the Tool Prioritization section for the full map of Serena vs. native tools.

If Serena is unavailable (not installed), skip silently and fall back to native Grep and Glob.

### 0.2 RPTC Workflow Understanding (INTERNALIZE)

You are executing the **RPTC (Research → Plan → TDD → Commit)** workflow for bug fixing.

**Core Philosophy:**
- Reproduce before fixing (confirm the bug exists)
- Root cause analysis (fix the cause, not symptoms)
- Test-first development (regression test proves the bug)
- Quality gates before shipping (no shortcuts)

**Codex Spawn Barrier (MANDATORY):**
- At every Codex `spawn_agent` point in this workflow, immediately wait for the spawned RPTC agents to finish before moving to the next numbered action or phase.
- Use `wait_agent` for the spawned agent IDs. Do not continue researching, planning, implementing, testing, verifying, or editing in the main context while those agents run.
- The purpose of Codex sub-agents here is context isolation: agents gather or execute the context-heavy work, then the parent session consumes their returned reports.
- Allowed parent-session activity while waiting is coordination only: record spawned agent IDs, call `wait_agent`, and keep `update_plan` accurate. Process agent results only after the required agents return.
- If only some parallel agents return, do not synthesize findings or proceed until all agents required for that spawn point have returned or failed.

**Codex Agent Authorization:**
- The user's `rptc:rptc-fix` invocation is explicit authorization to spawn
  RPTC sub-agents required by the active workflow phase.
- Do not require a separate per-turn user request for mandatory RPTC agents
  such as research, architect, delegated TDD, or Phase 4 verification agents.
- Generic multi-agent caution or parallel-tool guidance does not override RPTC
  phase requirements. Apply that guidance only to optional, non-RPTC, or
  out-of-scope agent delegation.

**SOP Reference Chain (with Precedence):**

| Topic | Check First (User) | Fallback (RPTC) |
|-------|-------------------|-----------------|
| Architecture | Project `sop/`, `Codex global guidance` | `RPTC plugin root/sop/architecture-patterns.md` |
| Testing | Project `sop/`, `Codex global guidance` | `RPTC plugin root/sop/testing-guide.md` |
| Security | Project `sop/`, `Codex global guidance` | `RPTC plugin root/sop/security-and-performance.md` |
| Progress Tracking | Project `sop/`, `Codex global guidance` | update_plan status tracking with sequential dependencies in prose (see Step 0.5) |
| Refactoring | Project `sop/`, `Codex global guidance` | `RPTC plugin root/sop/post-tdd-refactoring.md` |
| Frontend | Project `sop/`, `Codex global guidance` | `RPTC plugin root/sop/frontend-guidelines.md` |

**Precedence Rule**: If user specifies custom SOPs (in project AGENTS.md, project `sop/` dir, or `Codex global guidance`), use those for the matching topic. RPTC SOPs are the fallback default.

### 0.3 Phase Structure Awareness

This workflow has **5 mandatory phases**. You MUST NOT skip phases.

| Phase | Name | Key Deliverable |
|-------|------|-----------------|
| 1 | Reproduction & Triage | Confirmed bug with repro steps |
| 2 | Root Cause Analysis | 5 Whys result, fix approach |
| 3 | Fix Application | Regression test + minimal fix |
| 4 | Verification | All verification findings addressed |
| 5 | Complete | Summary for commit |

Phase ordering is enforced by task dependencies created in Step 0.5.

### 0.4 Initialization Verification

Before proceeding to Phase 1, confirm:
- Skills loaded and active
- RPTC directives understood
- SOP references noted
- Phase structure clear

**CRITICAL: If verification fails, STOP. Do not proceed to Phase 1.**

### 0.5 Phase Task Initialization

Create the workflow phases with `update_plan`. Keep phases sequential in prose: do not start a later phase until the previous phase is complete.

```json
{
  "plan": [
    {"step": "Phase 1: Reproduction & Triage - Confirm bug with reproduction steps", "status": "pending"},
    {"step": "Phase 2: Root Cause Analysis - 5 Whys methodology, identify fix approach", "status": "pending"},
    {"step": "Phase 3: Fix Application - Regression test + minimal fix via TDD", "status": "pending"},
    {"step": "Phase 4: Verification - Review agents verify fix quality", "status": "pending"},
    {"step": "Phase 5: Complete - Summarize fix for commit", "status": "pending"}
  ]
}
```

**At each phase**: call `update_plan` with the current phase `in_progress`, completed phases `completed`, and future phases `pending`.

### 0.5.1 Codex Phase Hierarchy Protocol

Codex `update_plan` is flat and cannot enforce nested blocking task types. Preserve
RPTC phase structure through naming and ordering.

**Rules**:
- NEVER replace the top-level phase list with bare fix tasks.
- Keep all five phases visible for the whole workflow.
- When Phase 3 starts, import approved or direct fix steps as `Phase 3.x` child
  items immediately after the Phase 3 parent item.
- When Phase 4 starts, import verification agent launches, findings, and re-checks
  as `Phase 4.x` child items immediately after the Phase 4 parent item.
- Because only one item can be `in_progress`, the active child item owns
  `in_progress`. The parent phase stays as the phase boundary and is marked
  `completed` only after all of its child items complete.

### 0.6 Plan Continuation Detection

Check if the bug description argument contains **"Plan is approved"**:

**If YES** — this is a post-plan-approval re-entry (context was cleared after plan approval):

1. Step 0 initialization is already complete (skills loaded, Serena active, tasks created)
2. **Verify environment**: re-derive `REPO_ROOT` from `git rev-parse --show-toplevel`.
   Check if currently inside a worktree: compare `git rev-parse --show-toplevel` against `git worktree list`. If in a worktree, set `WORKTREE_PATH` accordingly.
3. **Load the approved plan file** and extract its fix steps.
4. **Expand Phase 3** by adding those fix steps as `Phase 3.x` child items.
   Do not replace the five-phase workflow list.
5. Mark Phases 1 and 2 complete and start the first fix child item:
   ```
   Call `update_plan` with the full phase list: Phases 1 and 2 completed,
   Phase 3 parent present, first Phase 3.x child item in_progress, Phases 4
   and 5 pending.
   ```
6. **Proceed directly to Phase 3: Fix Application** — the plan is already approved and available in the plan file.

**If NO** — this is a new bug report. Proceed to Phase 1.

---

## Arguments

`rptc:rptc-fix <bug-description>`

**Example**: `rptc:rptc-fix "Cart items disappear after page refresh"`

---

## Bug Severity Classification

**Before starting**, classify the bug to determine urgency:

| Severity | Description | Response |
|----------|-------------|----------|
| **S1 Blocker** | System unusable, crashes, data loss | Immediate fix, skip plan mode |
| **S2 Critical** | Core functionality broken, no workaround | High priority, skip plan mode |
| **S3 Major** | Significant impact, workarounds exist | Normal priority, full workflow |
| **S4 Minor** | UI issues, inconveniences | Lower priority, skip plan mode |

**Result**: Set `severity` for Phase 2 routing (S1-S2, S4 may skip plan mode). Phase 4 (Verification) is always required.

---

## Tool Prioritization

**Serena MCP** (prefer over native tools — activated via ToolSearch in Step 0.1.2):

Serena tools may appear as `mcp__serena__*` or `mcp__plugin_serena_serena__*` — use whichever is available.

**Read operations** (use instead of native Grep/Glob/Read for code):

| Task | Prefer Serena | Over Native |
|------|---------------|-------------|
| Find functions/classes | `get_symbols_overview` | Grep |
| Locate specific code | `find_symbol` | Glob |
| Find usages/references | `find_referencing_symbols` | Grep |
| Regex search | `search_for_pattern` | Grep |
| List directory | `list_dir` | LS |
| Reflect on progress | `think_about_collected_information` | — |

**Edit operations** (use instead of Edit tool for code modifications):

| Task | Prefer Serena | Over Native |
|------|---------------|-------------|
| Replace function/method body | `replace_symbol_body` | Edit |
| Insert code after a symbol | `insert_after_symbol` | Edit |
| Insert code before a symbol | `insert_before_symbol` | Edit |
| Rename a symbol everywhere | `rename_symbol` | Edit |
| Reflect on task adherence | `think_about_task_adherence` | — |

---

## Skills Usage Guide

**`rptc:tool-guide`** - Tool prioritization for Serena MCP and other MCP servers (MANDATORY LOAD):

| When | Apply To |
|------|----------|
| Step 0 (always loaded) | Infrastructure — activates Serena for code navigation throughout |
| All phases | Serena read ops (`find_symbol`, `search_for_pattern`) |

**Method**: ToolSearch activates Serena at session start (Step 0.1.2 Activate Serena); then prefer `find_symbol`, `get_symbols_overview`, `search_for_pattern` over native Grep/Glob for all code navigation.
**Timing**: Loaded first in Step 0. Applies across all phases wherever code navigation or symbol search is needed.

**`brainstorming`** - Structured dialogue for fix approach exploration:

| When | Apply To |
|------|----------|
| Phase 2 (before architect agent) | Explore fix approaches when multiple options exist |
| Throughout | Validate assumptions, clarify constraints |

**Method**: One question at a time via `request_user_input` once Plan Mode is active; otherwise ask in normal chat and halt. Multiple choice preferred, YAGNI ruthlessly.
**Timing**: Main context uses this BEFORE delegating to architect agent.

**`writing-clearly-and-concisely`** - Apply Strunk's Elements of Style to all prose:

| When | Apply To |
|------|----------|
| Phase 2 | Root cause explanation, fix rationale |
| Phase 5 | Bug summary, regression notes |
| Throughout | Commit messages, documentation updates |

**Key rules**: Active voice, positive form, definite language, omit needless words.

**`tdd-methodology`** - RED-GREEN-REFACTOR enforcement for main context code changes:

| When | Apply To |
|------|----------|
| Phase 3 (Fix Application) | Any code written in main context (not delegated to tdd-agent) |

**Method**: Surgical coding (search 3 similar patterns first), context discovery (check existing tests), strict RED-GREEN-REFACTOR cycle. For bug fixes: write a test that reproduces the bug FIRST (RED), then fix (GREEN).
**Timing**: Main context applies this when handling fix directly. Sub-agent `rptc:tdd-agent` has equivalent guidance built in.

**`rptc:frontend-design`** *(conditional)* - Distinctive, production-grade frontend interfaces:

| When | Apply To |
|------|----------|
| Phase 3 (when bug involves frontend) | HTML, CSS, UI components, web pages, visual fixes |

**Method**: Maintain design quality when fixing frontend bugs — preserve aesthetic intent, typography, color themes, and motion patterns.
**Timing**: Load in Step 0.1.1 only when the bug involves frontend code. Additive creative layer on top of `frontend-guidelines.md` SOP (which always applies for engineering standards).

---

## Phase 1: Reproduction & Triage

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

**Goal**: Confirm the bug exists and understand its triggering conditions.

> 💡 **Tool Reminder**: Use Serena for code tracing.

**Actions**:

0. **Check for RPTC configuration** in project's AGENTS.md:
   - Look for `<!-- RPTC-START` marker in local AGENTS.md
   - If NOT found: Suggest user run `rptc:rptc-config` for best experience
   - If found but outdated: Suggest user run `rptc:rptc-config` to sync with current plugin version

1. **Get repo root**: `Bash("git rev-parse --show-toplevel")` → store as `REPO_ROOT` for use in worktree path computation and the Environment Context Block.

2. **Create initial todo list** with phases:
   - Reproduction & Triage, Root Cause Analysis, Fix Application, Verification, Complete

3. **Gather bug context** from user:
   - What is the expected behavior?
   - What is the actual behavior?
   - Steps to reproduce (if known)
   - Environment details (if relevant)
   - Error messages, stack traces, logs

4. **If reproduction steps unclear**, ask user for clarification in normal chat and halt. Do not call `request_user_input` unless Plan Mode is already active.

5. **Launch 2-3 research agents in parallel** for bug investigation (NOT the built-in Explore agent):

```
IMPORTANT: Use agent_type: "rptc:research-agent", NOT "Explore"

[Prepend the Environment Context Block to each agent prompt]

Use spawn_agent tool with agent_type: "rptc:research-agent" (launch all in parallel):

Agent 1 prompt: "Investigate bug: [description].
Use code-explorer methodology Phase 1 (Feature Discovery): Find where bug manifests, entry points, affected files.
Return: Reproduction confirmed (Y/N), failure point location, error details."

Agent 2 prompt: "Investigate bug: [description].
Use code-explorer methodology Phase 2 (Code Flow Tracing): Trace execution from entry point to error.
Return: Code path (file:line references), where behavior diverges from expected, data flow analysis."

Agent 3 prompt: "Investigate bug: [description].
Use code-explorer methodology Phase 3 (Architecture Analysis): What components are affected? Similar patterns elsewhere?
Return: Affected files/functions, related code with same pattern, potential regression scope."
```

6. **Codex spawn barrier**: Immediately call `wait_agent` for all Phase 1 research agents and wait for every required report. Do not continue bug analysis, inspect additional code, hypothesize root causes, or proceed to bisect/summary in the main context while research agents run.

7. **Optional: Git bisect** for regressions:
   - If bug worked before: "When did this break?"
   - Use `git log` to find likely commit range
   - Suggest bisect if >20 commits in range

8. **Summarize findings**:
   - Bug confirmed: Y/N
   - Failure point: file:line
   - Affected code paths
   - Severity classification

### Plan Mode Handoff (Codex Gate)

**After Phase 1 research/triage is complete and before any Branch Strategy or Phase 2 planning/questions**, ask the user to switch Codex into Plan Mode.

Codex does not expose a reliable automatic Plan Mode switch or a dependable way to detect the current mode from skill instructions. Because `request_user_input` is only available in Plan Mode, do not call `request_user_input` until the user confirms Plan Mode is active.

**Required behavior:**

1. Present the Phase 1 summary in normal chat.
2. Ask the user to switch to Plan Mode and reply with confirmation, for example:
   ```
   Phase 1 research/triage is complete. Please switch Codex to Plan Mode, then reply "Plan Mode active" so I can continue with Branch Strategy and Phase 2 planning questions.
   ```
3. Halt. Do not proceed to Branch Strategy, Phase 2, architect agents, or any `request_user_input` calls until the user confirms Plan Mode is active.
4. If the runtime clearly exposes that Plan Mode is already active (for example, `request_user_input` is available in the current tool set), continue without asking for a mode switch.

### Branch Strategy

**Now that the scope is clear and Plan Mode is active**, ask the user how to organize this work.

**Choose recommendation based on Phase 1 findings:**
- Recommend **New worktree** when: multi-file fix, >3 files to modify, risky changes, or unclear root cause that may require multiple attempts
- Recommend **Current branch** when: small fix, single-file change, clear root cause, or already on a fix branch

Put your recommended option first and append "(Recommended)" to its label.

**Before asking**, prepare the option labels:

1. **Get current branch name**: `git branch --show-current` → e.g. `main`
2. **Generate worktree branch name** from the bug description:
   - Lowercase, replace spaces with hyphens, strip special characters
   - Prefix with `fix/`
   - Example: `"Cart items disappear"` → `fix/cart-items-disappear`

```json
{
  "questions": [{
    "id": "branch_strategy",
    "header": "Branch",
    "question": "How should this fix be organized?",
    "options": [
      {"label": "<recommended-option> (Recommended)", "description": "<description>"},
      {"label": "<other-option>", "description": "<description>"}
    ]
  }]
}
```

Example — single-file fix with clear root cause on a fix branch:
```
  - label: "Current branch [fix/auth-bug] (Recommended)"
  - label: "New worktree [fix/cart-items-disappear]"
```

Example — risky multi-file fix on main with unclear root cause:
```
  - label: "New worktree [fix/cart-items-disappear] (Recommended)"
  - label: "Current branch [main]"
```

**If "New worktree" selected:**

1. **Compute worktree path** (sibling `<repo>.worktrees/` directory, branch as subpath):
   ```bash
   # REPO_ROOT already set from Phase 1 Action 1
   REPO_PARENT="$(dirname "$REPO_ROOT")"
   REPO_NAME="$(basename "$REPO_ROOT")"
   WORKTREE_PATH="${REPO_PARENT}/${REPO_NAME}.worktrees/<branch-name>"
   ```
   Example: repo at `/home/user/projects/myapp`, branch `fix/cart-bug` → worktree at `/home/user/projects/myapp.worktrees/fix/cart-bug`. `git worktree add` creates the nested directory structure automatically.
   Store `WORKTREE_PATH` — you will reference it throughout this session.

2. **Create worktree** using the absolute path:
   ```bash
   git worktree add -b <branch-name> "$WORKTREE_PATH" HEAD
   ```

3. **Activate and verify worktree** — change into the new directory and confirm it:
   ```bash
   cd "$WORKTREE_PATH" && git rev-parse --show-toplevel
   ```
   The output MUST match `WORKTREE_PATH`. If it does not, STOP and fix before continuing.

4. **Confirm to user**:
   ```
   Worktree created and activated at <WORKTREE_PATH>
   Branch: <branch-name>
   Verified: working directory is inside worktree.
   All subsequent work proceeds here.
   ```

5. **Set worktree active flag**: Remember that `WORKTREE_PATH` is set. ALL agent delegation
   prompts in Phases 2-4 MUST include the worktree lines in the Environment Context Block (defined below).

**If "Current branch" selected:** `WORKTREE_PATH` is not set. Continue to Phase 2.

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

#### Environment Context Block

Prepend this block to EVERY agent prompt in Phases 2-4 (architect, tdd, code-review, security, docs). It carries Serena activation and worktree info so sub-agents can orient themselves without guessing.

```
ENVIRONMENT:
Repo root: <REPO_ROOT>
Serena project: <SERENA_PROJECT_NAME>
  → Call activate_project("<SERENA_PROJECT_NAME>") before using any Serena tools.
[If WORKTREE_PATH is set, include these lines:]
Worktree: <WORKTREE_PATH>
  → cd "<WORKTREE_PATH>" before doing ANY work.
  → All file paths are relative to this worktree root, NOT the original repo.
```

`<SERENA_PROJECT_NAME>` is the registered name from the main context's successful `activate_project` call in Step 0.1.2. If Serena was unavailable in the main context, omit the Serena lines.

---

## Phase 2: Root Cause Analysis

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

**Goal**: Identify the fundamental cause and plan the fix.

> 💡 **Tool Reminder**: Use Serena (`find_symbol`, `find_referencing_symbols`) to trace code paths and confirm root cause.

**Actions**:

1. **Apply 5 Whys methodology** to findings from Phase 1:
   ```
   Why? [Symptom observed]
   Why? [Immediate cause]
   Why? [Underlying cause]
   Why? [Deeper cause]
   Why? [Root cause - systemic/code-level issue]
   ```

2. **For simple bugs (S3-S4, clear root cause)**: Skip plan mode
   - Document root cause inline
   - Proceed directly to Phase 3

3. **For complex bugs (S1-S2, or unclear root cause)**: Confirm Plan Mode is active (normally completed by the Phase 1 Plan Mode Handoff). If not confirmed, ask the user to switch to Plan Mode and halt until confirmation before using `request_user_input`
   - **Clarify fix approach using `brainstorming` skill** (BEFORE architect-agent):
     - Use request_user_input to explore fix options ONE question at a time
     - Present 2-3 fix approaches with trade-offs
     - Clarify: acceptable scope, risk tolerance, timeline constraints
     - Skip if: fix approach is obvious from root cause analysis
   - Launch architect-agent for fix planning:

```
Use spawn_agent tool with agent_type: "rptc:architect-agent":

[Prepend the Environment Context Block]

## Bug Context
- Description: [bug description]
- Symptom: [observed behavior]
- Root Cause: [from 5 Whys analysis]
- Failure Point: [file:line from Phase 1]
- Affected Paths: [from Phase 1]

## Your Task
Design a minimal fix for this bug. Perspective: Surgical.

Provide:
1. Fix approach (1-3 steps maximum)
2. Files to modify
3. Regression test strategy
4. Risk assessment (what could break)

Constraints:
- MINIMAL change - fix the root cause only
- NO refactoring unrelated code
- NO scope creep

Plan structure: Begin with Step 0: RPTC Re-initialization — instructs re-invocation of `rptc:rptc-fix` with "Plan is approved, continue to implementation" to restore full RPTC context.
```

4. **Codex spawn barrier**: Immediately call `wait_agent` for the architect agent and wait for its fix plan. Do not refine the plan, ask plan-approval questions, or proceed to Phase 3 in the main context while the architect runs.

5. **Review fix plan**:
   - Is the fix addressing root cause (not just symptom)?
   - Is the fix minimal and surgical?
   - What's the regression risk?

6. **If plan mode used**: Verify plan includes Step 0 (re-invocation of `rptc:rptc-fix`), then ask the user to leave Plan Mode / switch to execution mode. Halt until the user confirms the mode switch so the plan can be approved.

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

## Phase 3: Fix Application

Call `update_plan` with the full `plan` list. Preserve Phases 1-5 and add the
approved or direct fix steps as `Phase 3.x` child items. Do not overwrite the
phase list with unprefixed fix tasks.

**Goal**: Apply the fix using test-driven approach (regression test first).

> 💡 **Tool Reminder**: Use Serena for both navigation and edits: `find_symbol` to locate code, `replace_symbol_body` / `insert_after_symbol` to apply changes (prefer over Edit tool).

**CRITICAL - Test-First Ordering (NON-NEGOTIABLE)**:

Whether delegating to tdd-agent OR executing in main context:

1. Write the regression test that reproduces the bug BEFORE modifying ANY production code
2. Update any existing tests BEFORE changing production code
3. Run tests and confirm they fail BEFORE writing the fix
4. Only after tests exist and fail may you edit production files

**FILE LOCKOUT RULE**: During RED phase, you may ONLY create or modify test files (`tests/`, `__tests__/`, `*.test.*`, `*.spec.*`). Any edit to a production/source file during RED phase is a TDD violation. STOP and revert if this happens.

#### Delegation Decision: Direct or Agent?

| Criteria | Execute Directly (Main Context) | Delegate to tdd-agent |
|----------|--------------------------------|----------------------|
| Fix steps | 1 step (single root cause) | 2+ steps or multi-component |
| Files affected | 1-2 files | 3+ files |
| Estimated lines | <30 lines changed | 30+ lines |
| Complexity | Clear root cause, obvious fix | Complex interactions, cascading changes |

**If Direct**: Execute fix in main context using TDD methodology.

```
Use/load the `rptc:tdd-methodology` skill.
```

**Test-First Gate (Direct Execution)**: Execute in strict order.

1. **Surgical Coding**: Search 3 similar patterns first
2. **Context Discovery**: Check existing tests, framework, naming conventions
3. **RED**: Write regression test reproducing the bug. Run it. Confirm it fails with same symptom.

   **BLOCKING GATE — RED Phase Verification** (MANDATORY, cannot skip):

   Before ANY production file edit, verify via output:
   ```
   RED GATE CHECK:
   - Regression test written: [test file path]
   - Test failing: confirms bug symptom "[symptom]"
   - Production files touched: NONE
   → PASS: Proceed to GREEN
   ```
   If production files were touched → STOP. Revert production changes. Complete RED first.

4. **GREEN**: Apply minimal fix (NOW you may edit production files)
5. **REFACTOR**: Clean up only if needed (keep fix surgical)
6. **VERIFY**: Run affected tests, confirm regression test passes

Then skip to step 2 (Update task status) below.

**If Delegate**: Use tdd-agent (continue below).

**Actions**:

1. **Delegate to TDD agent** with regression emphasis:

```
Use spawn_agent tool with agent_type: "rptc:tdd-agent":

[Prepend the Environment Context Block]

## Bug Fix Context
- Bug: [description]
- Root Cause: [from Phase 2]
- Fix Location: [file:line]
- Fix Approach: [from Phase 2 plan or inline decision]

## TDD Bug Fix Cycle

### RED Phase (Critical — test files ONLY)
Write a test that REPRODUCES the exact bug:
- Test must fail with the SAME symptom as the bug
- Test must use the SAME conditions that trigger the bug
- Verify: test fails for the right reason (not compile error)
- FILE LOCKOUT: Only test files may be created/modified during RED phase. Do NOT touch production files.

Example structure:
```
test('should [expected behavior] when [condition]', () => {
  // Arrange: Set up bug-triggering conditions
  // Act: Perform the action that triggers the bug
  // Assert: Verify correct behavior (currently fails)
});
```

After writing tests, output RED GATE CHECK:
```
RED GATE CHECK:
- Regression test written: [test file path]
- Test failing: confirms bug symptom "[symptom]"
- Production files touched: NONE
→ PASS: Proceed to GREEN
```
If production files were touched → STOP. Revert. Complete RED first.

### GREEN Phase (Surgical — NOW edit production files)
Apply MINIMAL fix to make the test pass:
- Change ONLY what's necessary to fix the root cause
- Do NOT refactor nearby code
- Do NOT "improve" unrelated code
- Diff should be as small as possible

### VERIFY Phase (Regression Check)
- Run the new regression test (must pass)
- Run related test files (must pass)
- Run affected tests — files that import or reference changed modules (must pass)
- Run ONLY affected tests — do NOT run the full test suite (full suite runs are reserved for `rptc:rptc-commit`)
- Report any new failures

## Constraints
- Maximum 3 implementation steps
- Keep fix surgical and minimal
- Flag if fix suggests larger refactoring need (don't do it, just flag)
```

1b. **Codex spawn barrier**: Immediately call `wait_agent` for the tdd-agent and wait for it to return. Do not start independent research, ad hoc fixes, production/test edits, or self-verification in the main context while the agent runs.

1c. **Verify fix compliance**: After tdd-agent returns, check the exit verification block:
    - `Test-First Followed: YES` → continue
    - `Test-First Followed: NO` → flag as TDD violation, ask user whether to re-run or accept

2. **Update task status** as each `Phase 3.x` fix item progresses (an `update_plan` call with the full `plan` list and updated statuses)

3. **Handle failures**:
   - If test won't reproduce bug: Return to Phase 1 for better reproduction
   - If fix causes new failures: Analyze regression, adjust fix
   - If fix attempt fails 3x: Ask user for guidance

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

## Phase 4: Verification

Call `update_plan` with the full `plan` list. Preserve Phases 1-5 and add
verification work as `Phase 4.x` child items. Phase 4 starts only after all
`Phase 3.x` fix items are complete.

**Goal**: Verify the fix works and didn't introduce regressions.

> 💡 **Tool Reminder**: Use Serena (`find_referencing_symbols`, `search_for_pattern`) when applying auto-fixes from verification findings.

**This phase runs for ALL bugs regardless of severity (S1-S4).** Even urgent S1 fixes must be reviewed before completion.

**Phase boundary**: Phase 3 regression checks are not Phase 4 verification.
Running affected tests, checking diffs, or reading changed files in the main
context does not satisfy Phase 4. Phase 4 requires the selected RPTC verification
agent calls below. If verification agents are unavailable, report that as a
workflow blocker instead of silently substituting self-review.

**Authorization rule**: The active `rptc:rptc-fix` workflow already authorizes
mandatory Phase 4 verification agents. When Phase 4 starts, launch the selected
RPTC verification agents automatically if they are available. Do not replace
them with local checks, and do not describe local tests, diffs, typechecks,
builds, or self-review as a "Phase 4 quality pass."

**Actions**:

1. **Determine verification agent mode** (one-time project configuration):

   a. **Check if project AGENTS.md exists** (in project root)

   b. **If AGENTS.md exists**, look for `verification-agent-mode:` setting:
      - If found: Use that mode (`automatic`, `all`, or `minimal`)
      - If not found: Ask user via request_user_input (one-time setup):
        ```json
        {
          "questions": [{
            "id": "verification_mode",
            "header": "Verification",
            "question": "How should verification agents be selected for this project? (saved to AGENTS.md)",
            "options": [
              {"label": "Automatic (Recommended)", "description": "Smart selection based on file types and change patterns"},
              {"label": "All Agents", "description": "Always launch all 3 verification agents"},
              {"label": "Minimal", "description": "Only launch agents when strongly indicated"}
            ]
          }]
        }
        ```
        Then append to AGENTS.md:
        ```markdown
        ## RPTC Verification Configuration
        verification-agent-mode: [selected mode]
        ```

   c. **If no AGENTS.md exists**: Use `automatic` mode (don't ask, don't create file)

2. **Select agents based on mode**:

   **Mode: `all`** — Launch all 3 agents (skip to step 3)

   **Mode: `automatic`** — Select based on changes:

   | Change Type | code-review | security | docs |
   |-------------|:-----------:|:--------:|:----:|
   | Source code in `auth/`, `api/`, `security/`, `middleware/` paths | ✅ | ✅ | Check keywords |
   | Source code (other paths) | ✅ | Check keywords | Check keywords |
   | Test files only | ✅ | ❌ | ❌ |
   | Dependencies changed | ❌ | ✅ | ❌ |
   | Docs/markdown only | ❌ | ❌ | ✅ |

   **Keyword detection** (scan git diff):
   - Security keywords: `password`, `token`, `secret`, `auth`, `session`, `crypto`, `hash`, `sql`, `exec`, `eval` → include security-agent
   - API keywords: `export`, `interface`, `endpoint`, `route`, `version` → include docs-agent

   **Default**: If uncertain, include the agent

   **Mode: `minimal`** — Only launch when strongly indicated:
   - code-review: **ALWAYS** (minimum floor — at least one verification agent must launch)
   - security: Only if auth/api paths OR security keywords found
   - docs: Only if doc files changed OR export keyword found

3. **Create Phase 4 child plan items** for selected verification work:
   ```json
   {
     "plan": [
       {"step": "Phase 1: Reproduction & Triage - Confirm bug with reproduction steps", "status": "completed"},
       {"step": "Phase 2: Root Cause Analysis - 5 Whys methodology, identify fix approach", "status": "completed"},
       {"step": "Phase 3: Fix Application - Regression test + minimal fix via TDD", "status": "completed"},
       {"step": "Phase 4: Verification - Parent phase for review agents and findings", "status": "pending"},
       {"step": "Phase 4.1: Launch selected report-only verification agents", "status": "in_progress"},
       {"step": "Phase 4.2: Consolidate high-confidence findings", "status": "pending"},
       {"step": "Phase 4.3: Address verification findings", "status": "pending"},
       {"step": "Phase 4.4: Re-run verification if requested", "status": "pending"},
       {"step": "Phase 5: Complete - Summarize fix for commit", "status": "pending"}
     ]
   }
   ```

4. **Launch selected verification agents**:

   **AGENT NAMESPACE LOCKOUT (Phase 4):**
   - ✅ CORRECT: `agent_type: "rptc:code-review-agent"`
   - ❌ WRONG: `agent_type: "feature-dev:code-reviewer"` — different plugin, not RPTC
   - ❌ WRONG: `agent_type: "code-review:code-review"` — different plugin, not RPTC
   - The `rptc:` prefix is required for ALL verification agents. No exceptions.

   **Code Review Agent** (if selected):
   ```
   Use spawn_agent tool with agent_type: "rptc:code-review-agent":
   ⚠️ WRONG agents: "feature-dev:code-reviewer", "code-review:code-review" — DO NOT USE

   [Prepend the Environment Context Block]

   prompt: "Review bug fix for: [bug description].
   Files modified: [list files].
   Focus: Is this the ACTUAL root cause fix (not band-aid)? Is the fix minimal and surgical? Similar patterns elsewhere? Regression risk?
   REPORT ONLY - do not make changes. Output: confidence-scored findings (≥80 only)."
   ```

   **Security Agent** (if selected):
   ```
   Use spawn_agent tool with agent_type: "rptc:security-agent":

   [Prepend the Environment Context Block]

   prompt: "Security review for bug fix: [bug description].
   Files modified: [list files].
   Focus: Did the fix maintain security invariants? Any new vulnerabilities introduced?
   REPORT ONLY - do not make changes. Output: confidence-scored findings (≥80 only)."
   ```

   **Documentation Agent** (if selected):
   ```
   Use spawn_agent tool with agent_type: "rptc:docs-agent":

   [Prepend the Environment Context Block]

   prompt: "Documentation review for bug fix: [bug description].
   Files modified: [list files].
   Focus: Does the bug affect documented behavior? Any docs need updating?
   REPORT ONLY - do not make changes. Output: documentation updates needed (≥80 only)."
   ```

   **Codex spawn barrier**: After launching verification agents, immediately call
   `wait_agent` and wait for all selected agents to return. Do not perform
   independent main-context verification, inspect more files, consolidate
   findings, or start fixes while agents run. The parent session resumes
   substantive work only after reports return.

5. **Consolidate findings** from launched agents:
   - Fix quality: Root cause addressed? Minimal scope?
   - Regression risk: Side effects identified?
   - Documentation: Updates needed?

6. **Create Phase 4 child tasks for findings** (auto-fix by default):
   ```json
   {
     "plan": [
       {"step": "Phase 1: Reproduction & Triage - Confirm bug with reproduction steps", "status": "completed"},
       {"step": "Phase 2: Root Cause Analysis - 5 Whys methodology, identify fix approach", "status": "completed"},
       {"step": "Phase 3: Fix Application - Regression test + minimal fix via TDD", "status": "completed"},
       {"step": "Phase 4: Verification - Parent phase for review agents and findings", "status": "pending"},
       {"step": "Phase 4.1: Launch selected report-only verification agents", "status": "completed"},
       {"step": "Phase 4.2: Consolidate high-confidence findings", "status": "completed"},
       {"step": "Phase 4.3.1: [Category] Finding 1 - description (file:line)", "status": "pending"},
       {"step": "Phase 4.3.2: [Category] Finding 2 - description (file:line)", "status": "pending"},
       {"step": "Phase 4.4: Re-run verification if requested", "status": "pending"},
       {"step": "Phase 5: Complete - Summarize fix for commit", "status": "pending"}
     ]
   }
   ```

7. **Auto-fix findings** (no user approval needed for most issues):

   **Fix automatically**:
   - Nits: naming, formatting, minor style issues
   - Documentation updates
   - Minor code improvements (<30 lines)
   - Test assertions or coverage gaps

   **Ask user FIRST**:
   - Fix scope expansion (touches files outside original bug scope)
   - Regression risks identified by reviewers
   - Security concerns raised
   - Architectural issues

   **Process**:
   - Work through finding tasks sequentially
   - For auto-fix items: Apply fix, mark complete (an `update_plan` call with the full `plan` list and updated statuses)
   - For ask-first items: Use request_user_input with fix proposal, then apply or skip
   - Mark all finding tasks complete as addressed

8. **User Acknowledgment**:

   Present review results to the user. This is a tool-enforced gate — you MUST call request_user_input here.

   ```json
   {
     "questions": [{
       "id": "verification_gate",
       "header": "Verification",
       "question": "Phase 4 verification complete. [N] findings addressed. Proceed to completion?",
       "options": [
         {"label": "Proceed to Phase 5 (Recommended)", "description": "All verification findings addressed, ready to wrap up"},
         {"label": "Re-verify with `rptc:rptc-verify`", "description": "Run the standalone verification workflow to check current state"}
       ]
     }]
   }
   ```

   If user selects "Re-verify" → mark `Phase 4.4: Re-run verification if requested`
   as `in_progress`, then invoke `rptc:rptc-verify` (uses the standalone verify
   workflow with agent selection and full re-scan). When it returns, mark
   `Phase 4.4` completed before proceeding.

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

## Phase 5: Complete

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

Mark remaining tasks complete. Output 1-2 sentences: root cause, fix, regression test added. Ready for `rptc:rptc-commit`.

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

## Key Principles

1. **Reproduce before fixing**: Never fix a bug you can't reproduce
2. **Root cause, not symptom**: 5 Whys until you find the real cause
3. **Regression test first**: Write failing test that reproduces bug before fixing
4. **Minimal and surgical**: Smallest possible change to fix the root cause
5. **No scope creep**: Flag refactoring needs, don't do them in bug fix
6. **Verify thoroughly**: Check that fix works AND didn't break related functionality

---

## Differences from `rptc:rptc-feat`

| Aspect | `rptc:rptc-feat` | `rptc:rptc-fix` |
|--------|------------|-----------|
| **Goal** | Build new functionality | Fix existing behavior |
| **Phase 1** | Discover patterns | Reproduce failure |
| **Phase 2** | Design (3 perspectives) | Diagnose (single analysis) |
| **Phase 3** | Multi-step TDD | Regression test + minimal fix |
| **Phase 4** | Quality verification | Quality verification + regression focus |
| **Test Focus** | Define NEW behavior | Prevent RECURRENCE |
| **Scope** | Can be large | Must be minimal |
| **Plan Mode** | Always required | Optional for simple bugs |
| **Typical Steps** | 5-15 steps | 1-3 steps |

---

## Error Handling

- **Can't reproduce**: Ask user for more details, environment info, exact steps
- **Root cause unclear after analysis**: Try multiple hypotheses, ask user for context
- **Fix causes regressions**: Analyze what broke, adjust fix approach
- **Fix attempt fails 3x**: Pause, present findings, ask user for guidance
- **Larger refactoring needed**: Flag it, complete minimal fix, suggest follow-up task
- **Phase 4 not executed**: INVALID STATE. Return to Phase 4. Phase 5 cannot proceed without verification.
