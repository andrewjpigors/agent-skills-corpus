---
name: rptc-feat
description: Research -> Plan -> TDD -> Verify in one seamless flow. Use when the user asks for /rptc:feat or the equivalent RPTC Codex workflow intent.
---

# RPTC Feat
Complete feature development: Discovery → Architecture → Implementation → Quality Verification.

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

> **Note**: Codex omits Claude's persistent team commands. For batch work across independent features, use parent-orchestrated `spawn_agent` delegation with clear ownership boundaries.

### 0.1.1 Conditional Skills (Load When Applicable)

**Frontend work** — If the task involves creating or modifying HTML, CSS, UI components, web pages, or frontend interfaces:

```
Use/load the `rptc:frontend-design` skill.
```

> Provides creative direction and distinctive aesthetics. Complements the RPTC `frontend-guidelines.md` SOP (loaded via the SOP Reference Chain): the SOP ensures correctness (accessibility, performance, responsive), the skill ensures distinction (bold aesthetics, memorable design).

> **IMPORTANT**: If the project already has an established design system, style guide, or visual aesthetic, the skill's creative direction MUST work within those constraints. Research existing styles first (CSS variables, component library, brand guidelines) and extend them — do not override with a conflicting aesthetic. The skill adds polish and intentionality, not a new identity.

### 0.1.2 Activate Serena MCP (MANDATORY)

Serena tools are **deferred** in the main context — they require explicit loading before they can be called.

Call ToolSearch now to activate them:

```
ToolSearch(query: "serena")
```

Once loaded, Serena tools appear as `mcp__serena__*` or `mcp__plugin_serena_serena__*`. This activates both read tools (`find_symbol`, `get_symbols_overview`, `search_for_pattern`, etc.) and edit tools (`replace_symbol_body`, `insert_after_symbol`, etc.). Use them throughout this workflow — refer to the Tool Prioritization section for the full map of Serena vs. native tools.

If Serena is unavailable (not installed), skip silently and fall back to native Grep and Glob.

### 0.2 RPTC Workflow Understanding (INTERNALIZE)

You are executing the **RPTC (Research → Plan → TDD → Commit)** workflow.

**Core Philosophy:**
- Research before coding (understand before building)
- Plan with user approval (user is PM)
- Test-first development (tests define behavior)
- Quality gates before shipping (no shortcuts)

**Codex Spawn Barrier (MANDATORY):**
- At every Codex `spawn_agent` point in this workflow, immediately wait for the spawned RPTC agents to finish before moving to the next numbered action or phase.
- Use `wait_agent` for the spawned agent IDs. Do not continue researching, planning, implementing, testing, verifying, or editing in the main context while those agents run.
- The purpose of Codex sub-agents here is context isolation: agents gather or execute the context-heavy work, then the parent session consumes their returned reports.
- Allowed parent-session activity while waiting is coordination only: record spawned agent IDs, call `wait_agent`, and keep `update_plan` accurate. Process agent results only after the required agents return.
- If only some parallel agents return, do not synthesize findings or proceed until all agents required for that spawn point have returned or failed.

**Codex Agent Authorization:**
- The user's `rptc:rptc-feat` invocation is explicit authorization to spawn
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

This workflow has **5 mandatory phases**. Phase ordering is enforced by task dependencies created in Step 0.5.

| Phase | Name | Key Deliverable |
|-------|------|-----------------|
| 1 | Discovery | Understanding of what to build |
| 2 | Architecture | User-approved implementation plan |
| 3 | Implementation | Working code with tests |
| 4 | Quality Verification | All findings addressed |
| 5 | Complete | Summary for commit |

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
    {"step": "Phase 1: Discovery - Understand what to build and existing patterns", "status": "pending"},
    {"step": "Phase 2: Architecture - Design implementation approach with user approval", "status": "pending"},
    {"step": "Phase 3: Implementation - Execute plan using appropriate method", "status": "pending"},
    {"step": "Phase 4: Quality Verification - Review agents verify changes", "status": "pending"},
    {"step": "Phase 5: Complete - Summarize what was built", "status": "pending"}
  ]
}
```

**At each phase**: call `update_plan` with the current phase `in_progress`, completed phases `completed`, and future phases `pending`.

### 0.5.1 Codex Phase Hierarchy Protocol

Codex `update_plan` is flat and cannot enforce nested blocking task types. Preserve
RPTC phase structure through naming and ordering.

**Rules**:
- NEVER replace the top-level phase list with bare implementation tasks.
- Keep all five phases visible for the whole workflow.
- When Phase 3 starts, import approved implementation steps as `Phase 3.x` child
  items immediately after the Phase 3 parent item.
- When Phase 4 starts, import verification agent launches, findings, and re-checks
  as `Phase 4.x` child items immediately after the Phase 4 parent item.
- Because only one item can be `in_progress`, the active child item owns
  `in_progress`. The parent phase stays as the phase boundary and is marked
  `completed` only after all of its child items complete.

**Example Phase 3 expansion**:
```json
{
  "plan": [
    {"step": "Phase 1: Discovery - Understand what to build and existing patterns", "status": "completed"},
    {"step": "Phase 2: Architecture - Design implementation approach with user approval", "status": "completed"},
    {"step": "Phase 3: Implementation - Parent phase for approved plan steps", "status": "pending"},
    {"step": "Phase 3.1: RED - Write validation tests", "status": "in_progress"},
    {"step": "Phase 3.2: GREEN - Implement validation behavior", "status": "pending"},
    {"step": "Phase 4: Quality Verification - Review agents verify changes", "status": "pending"},
    {"step": "Phase 5: Complete - Summarize what was built", "status": "pending"}
  ]
}
```

### 0.6 Plan Continuation Detection

Check if the feature description argument contains **"Plan is approved"**:

**If YES** — this is a post-plan-approval re-entry (context was cleared after plan approval):

1. Step 0 initialization is already complete (skills loaded, Serena active, tasks created)
2. **Verify environment**: re-derive `REPO_ROOT` from `git rev-parse --show-toplevel`.
   Check if currently inside a worktree: compare `git rev-parse --show-toplevel` against `git worktree list`. If in a worktree, set `WORKTREE_PATH` accordingly.
3. **Load the approved plan file** and extract its implementation steps.
4. **Expand Phase 3** by adding those implementation steps as `Phase 3.x` child
   items. Do not replace the five-phase workflow list.
5. Mark Phases 1 and 2 complete and start the first implementation child item:
   ```
   Call `update_plan` with the full phase list: Phases 1 and 2 completed,
   Phase 3 parent present, first Phase 3.x child item in_progress, Phases 4
   and 5 pending.
   ```
6. **Proceed directly to Phase 3: Implementation** — the plan is already approved and available in the plan file.

**If NO** — this is a new feature request. Proceed to Phase 1.

---

## Arguments

`rptc:rptc-feat <feature-description>`

**Example**: `rptc:rptc-feat "Add user authentication with OAuth2"`

---

## Task Classification

**Before starting**, classify the task to determine the appropriate workflow:

| Task Type | Examples | TDD Phase | Implementation |
|-----------|----------|-----------|----------------|
| **Code** | New features, bug fixes, refactoring, API changes | ✅ Required | Delegate to tdd-agent |
| **Non-Code** | Documentation, config, markdown, plugin updates | ⏭️ Skip | Main context executes directly |

**Classification rules**:
- **Code tasks**: Create/modify `.ts`, `.js`, `.py`, `.go`, `.rs`, `.java`, or other source files
- **Non-Code tasks**: Create/modify `.md`, `.json`, `.yaml`, `.toml`, config files, or purely documentation

**Result**: Set `task_type` to `code` or `non-code` for Phase 3 routing.

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

**`brainstorming`** - Structured dialogue for requirement clarification:

| When | Apply To |
|------|----------|
| Phase 2 (before architect agents) | Clarify unclear requirements with user |
| Throughout | Explore approaches with 2-3 options, validate incrementally |

**Method**: One question at a time via `request_user_input` once Plan Mode is active; otherwise ask in normal chat and halt. Multiple choice preferred, YAGNI ruthlessly.
**Timing**: Main context uses this BEFORE delegating to architect agents.

**`writing-clearly-and-concisely`** - Apply Strunk's Elements of Style to all prose:

| When | Apply To |
|------|----------|
| Phase 2 | Plan descriptions, rationales, step explanations |
| Phase 5 | Summary output, implementation notes |
| Throughout | Commit messages, documentation updates, user-facing text |

**Key rules**: Active voice, positive form, definite language, omit needless words.

**`tdd-methodology`** - RED-GREEN-REFACTOR enforcement for main context code changes:

| When | Apply To |
|------|----------|
| Phase 3 (Route A or direct code changes) | Any code written in main context (not delegated to tdd-agent) |

**Method**: Surgical coding (search 3 similar patterns first), context discovery (check existing tests), strict RED-GREEN-REFACTOR cycle.
**Timing**: Main context applies this when handling code changes directly. Sub-agent `rptc:tdd-agent` has equivalent guidance built in.

**`rptc:frontend-design`** *(conditional)* - Distinctive, production-grade frontend interfaces:

| When | Apply To |
|------|----------|
| Phase 3 (when task involves frontend) | HTML, CSS, UI components, web pages, visual design |

**Method**: Bold aesthetic direction, distinctive typography, cohesive color themes, purposeful motion/animation. Avoids generic AI aesthetics.
**Timing**: Load in Step 0.1.1 only when the task involves frontend work. Additive creative layer on top of `frontend-guidelines.md` SOP (which always applies for engineering standards).

---

## Phase 1: Discovery

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

**Goal**: Understand what to build and existing patterns.

> 💡 **Tool Reminder**: Use Serena for code exploration.

**Actions**:

0. **Check for RPTC configuration** in project's AGENTS.md:
   - Look for `<!-- RPTC-START` marker in local AGENTS.md
   - If NOT found: Suggest user run `rptc:rptc-config` for best experience
   - If found but outdated: Suggest user run `rptc:rptc-config` to sync with current plugin version

1. **Get repo root**: `Bash("git rev-parse --show-toplevel")` → store as `REPO_ROOT` for use in worktree path computation and the Environment Context Block.

2. **Classify task type** (see Task Classification above)
3. **Create initial todo list** with phases based on task type:
   - Code tasks: Discovery, Architecture, TDD Implementation, Quality Verification, Complete
   - Non-Code tasks: Discovery, Architecture, Implementation, Quality Verification, Complete
4. **If codebase exploration needed**, launch 2-3 research agents in parallel (NOT the built-in Explore agent):

```
IMPORTANT: Use agent_type: "rptc:research-agent", NOT "Explore"

[Prepend the Environment Context Block to each agent prompt]

Use spawn_agent tool with agent_type: "rptc:research-agent" (launch all 3 in parallel):

Agent 1 prompt: "Find similar features and existing patterns for [feature].
Use code-explorer methodology Phase 1 (Feature Discovery): entry points, core files, boundaries.
Return: files implementing similar functionality, patterns used."

Agent 2 prompt: "Analyze architecture and abstractions for [feature].
Use code-explorer methodology Phase 3 (Architecture Analysis): layers, patterns, cross-cutting concerns.
Return: architectural layers, design patterns, component dependencies."

Agent 3 prompt: "Map integration points and dependencies for [feature].
Use code-explorer methodology Phase 2 (Code Flow Tracing): call chains, data transformations, side effects.
Return: external dependencies, internal dependencies, API boundaries."
```

5. **Codex spawn barrier**: Immediately call `wait_agent` for all Phase 1 research agents and wait for every required report. Do not continue Phase 1 discovery in the main context while research agents run; summarize only after their outputs return.
6. **If web research needed**, use `rptc:research-agent` with Mode B (20+ sources, cross-verification)
7. **If hybrid research needed** (codebase + best practices), use `rptc:research-agent` with Mode C
8. **If additional web or hybrid research agents are spawned**, apply the same Codex spawn barrier: wait for those agents before summarizing or asking follow-up questions.
9. **If unclear about requirements**, ask user for clarification
10. **Summarize findings**: Key patterns, files to modify, dependencies, gap analysis (if hybrid)

### Plan Mode Handoff (Codex Gate)

**After Phase 1 research is complete and before any Branch Strategy or Phase 2 planning/questions**, ask the user to switch Codex into Plan Mode.

Codex does not expose a reliable automatic Plan Mode switch or a dependable way to detect the current mode from skill instructions. Because `request_user_input` is only available in Plan Mode, do not call `request_user_input` until the user confirms Plan Mode is active.

**Required behavior:**

1. Present the Phase 1 summary in normal chat.
2. Ask the user to switch to Plan Mode and reply with confirmation, for example:
   ```
   Phase 1 research is complete. Please switch Codex to Plan Mode, then reply "Plan Mode active" so I can continue with Branch Strategy and Phase 2 planning questions.
   ```
3. Halt. Do not proceed to Branch Strategy, Phase 2, architecture agents, or any `request_user_input` calls until the user confirms Plan Mode is active.
4. If the runtime clearly exposes that Plan Mode is already active (for example, `request_user_input` is available in the current tool set), continue without asking for a mode switch.

### Branch Strategy

**Now that the scope is clear and Plan Mode is active**, ask the user how to organize this work.

**Choose recommendation based on Phase 1 findings:**
- Recommend **New worktree** when: multi-file feature, >3 files to modify, long-running work, or risky changes the user may want to abandon
- Recommend **Current branch** when: small change, single-file fix, quick task, or already on a feature branch

Put your recommended option first and append "(Recommended)" to its label.

**Before asking**, prepare the option labels:

1. **Get current branch name**: `git branch --show-current` → e.g. `main`
2. **Generate worktree branch name** from the feature description:
   - Lowercase, replace spaces with hyphens, strip special characters
   - Prefix with `feature/`
   - Example: `"Add user auth"` → `feature/add-user-auth`

```json
{
  "questions": [{
    "id": "branch_strategy",
    "header": "Branch",
    "question": "How should this feature be organized?",
    "options": [
      {"label": "<recommended-option> (Recommended)", "description": "<description>"},
      {"label": "<other-option>", "description": "<description>"}
    ]
  }]
}
```

Example — small single-file change on a feature branch:
```
  - label: "Current branch [feature/auth] (Recommended)"
  - label: "New worktree [feature/add-user-auth]"
```

Example — large multi-file feature on main:
```
  - label: "New worktree [feature/add-user-auth] (Recommended)"
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
   Example: repo at `/home/user/projects/myapp`, branch `feature/add-auth` → worktree at `/home/user/projects/myapp.worktrees/feature/add-auth`. `git worktree add` creates the nested directory structure automatically.
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

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

## Phase 2: Architecture

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

**Goal**: Design the implementation approach with user approval.

> 💡 **Tool Reminder**: Use Serena (`get_symbols_overview`, `search_for_pattern`) to verify architects' assumptions against the actual codebase.

**Actions**:

1. **Confirm Plan Mode is active** (normally completed by the Phase 1 Plan Mode Handoff). If not confirmed, ask the user to switch to Plan Mode and halt until confirmation before using `request_user_input`.

2. **Clarify requirements using `brainstorming` skill** (BEFORE launching agents):
   - Use request_user_input to clarify unclear requirements ONE question at a time
   - Prefer multiple choice options when possible
   - Focus on: purpose, constraints, success criteria, scope boundaries
   - Continue until requirements are clear enough for planning

   **Skip if**: Requirements are already crystal clear from Phase 1 discovery.

3. **Launch 3 plan agents in parallel** with different perspectives:

```
Use spawn_agent tool with agent_type: "rptc:architect-agent" (launch all 3 in parallel):

[Prepend the Environment Context Block to each agent prompt]

Agent 1: "Design implementation for [feature]. Perspective: Minimal. Provide: files to modify, component design, data flow, build sequence. [If code task: include test strategy]"

Agent 2: "Design implementation for [feature]. Perspective: Clean. Provide: files to modify, component design, data flow, build sequence. [If code task: include test strategy]"

Agent 3: "Design implementation for [feature]. Perspective: Pragmatic. Provide: files to modify, component design, data flow, build sequence. [If code task: include test strategy]"
```

4. **Codex spawn barrier**: Immediately call `wait_agent` for all three architect agents and wait for every architecture report. Do not inspect files, refine the plan, ask architecture-selection questions, or otherwise continue Phase 2 in the main context while architects run.

5. **Review all 3 approaches**, form an opinion on which fits best for this specific feature

6. **MANDATORY: Ask user to choose** via request_user_input (put recommended option first with "(Recommended)" suffix):

   **Skip asking ONLY if ALL of these are true:**
   - Single-file change with <20 lines
   - No architectural decisions involved
   - Only one approach is viable (others don't apply)

   **Otherwise, ALWAYS ask the user** - even if one option seems obviously better.

   **Before asking, present a brief summary of each approach:**

```markdown
## Architecture Options

### Minimal Approach
- **Files**: [list from agent 1]
- **Key idea**: [1-sentence summary]
- **Trade-off**: Fast, reuses existing code, may accumulate tech debt

### Clean Approach
- **Files**: [list from agent 2]
- **Key idea**: [1-sentence summary]
- **Trade-off**: Maintainable, elegant abstractions, takes longer

### Pragmatic Approach
- **Files**: [list from agent 3]
- **Key idea**: [1-sentence summary]
- **Trade-off**: Balanced, good enough without over-engineering
```

   **Then ask:**

```json
{
  "questions": [{
    "id": "architecture_approach",
    "header": "Architecture",
    "question": "Which architecture approach would you like to use for this feature?",
    "options": [
      {"label": "[Best fit] (Recommended)", "description": "[1-sentence why this fits best + file count]"},
      {"label": "[Second option]", "description": "[1-sentence trade-off + file count]"},
      {"label": "[Third option]", "description": "[1-sentence trade-off + file count]"}
    ]
  }]
}
```

7. **Write selected plan to plan file** with:
   - **Step 0: RPTC Re-initialization (ALWAYS FIRST)** — instructs re-invocation of `rptc:rptc-feat` with "Plan is approved, continue to implementation" to restore full RPTC context
   - Approach used (with rationale)
   - Implementation steps (ordered)
   - Files to create/modify
   - Test strategy per step (code tasks only)

8. **Verify plan includes Step 0** (re-invocation of `rptc:rptc-feat`), then ask the user to leave Plan Mode / switch to execution mode. Halt until the user confirms the mode switch so the plan can be approved.

**Plan file format** (flexible):

- Simple features: List steps directly
- Complex features: Overview + numbered implementation steps

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

## Phase 3: Implementation

Call `update_plan` with the full `plan` list. Preserve Phases 1-5 and add the
approved implementation steps as `Phase 3.x` child items. Do not overwrite the
phase list with unprefixed plan steps.

**Goal**: Execute the plan using the appropriate method for the task type.

> 💡 **Tool Reminder**: Use Serena for both navigation (`find_symbol`, `get_symbols_overview`) and edits (`replace_symbol_body`, `insert_after_symbol`) — prefer over native Grep/Edit.

### Route A: Non-Code Tasks (Direct Execution)

**When**: `task_type = non-code` (documentation, config, markdown, plugin updates)

**Actions**:

1. **Execute steps directly** in main context (no sub-agent delegation)
2. **For each step**:
   - Read target files
   - Make changes using Edit/Write tools
   - Verify changes are correct
3. **Update task status** as each `Phase 3.x` child item completes

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

### Route B: Code Tasks (TDD)

**When**: `task_type = code` (source files, tests, application logic)

**Goal**: Build with tests first, maintaining TDD discipline whether delegated or direct.

**CRITICAL - Test-First Ordering (NON-NEGOTIABLE)**:

Whether delegating to tdd-agent OR executing in main context:

1. Write/update ALL tests BEFORE modifying ANY production code
2. Run tests and confirm they fail BEFORE writing production code
3. Only after tests exist and fail may you edit production files

**FILE LOCKOUT RULE**: During RED phase, you may ONLY create or modify test files (`tests/`, `__tests__/`, `*.test.*`, `*.spec.*`). Any edit to a production/source file during RED phase is a TDD violation. STOP and revert if this happens.

#### Delegation Decision: Direct or Agent?

**Before batching**, decide how to execute based on plan complexity:

| Criteria | Execute Directly (Main Context) | Delegate to tdd-agent |
|----------|--------------------------------|----------------------|
| Plan steps | 1-2 steps | 3+ steps |
| Files affected | 1-2 files | 3+ files |
| Estimated lines | <50 lines of new/changed code | 50+ lines |
| Complexity | Straightforward, clear pattern | Complex logic, multi-component |

**If Direct**: Execute code changes in main context using TDD methodology.

```
Use/load the `rptc:tdd-methodology` skill.
```

**Test-First Gate (Direct Execution)**: Execute in strict order.

1. **Surgical Coding**: Search 3 similar patterns first
2. **Context Discovery**: Check existing tests, framework, naming conventions
3. **RED**: Write failing tests. Run them. Confirm they fail.

   **BLOCKING GATE — RED Phase Verification** (MANDATORY, cannot skip):

   Before ANY production file edit, verify via output:
   ```
   RED GATE CHECK:
   - Tests written: [list test files created/modified]
   - Tests failing: [X] tests fail as expected
   - Production files touched: NONE
   → PASS: Proceed to GREEN
   ```
   If production files were touched → STOP. Revert production changes. Complete RED first.

4. **GREEN**: Minimal code to pass (NOW you may edit production files)
5. **REFACTOR**: Improve while green
6. **VERIFY**: Run affected tests, check coverage

Then skip to step 8 (Update task status) below.

**If Delegate**: Use smart batching with tdd-agent (continue below).

#### Smart Batching (tdd-agent delegation)

Combines related steps into fewer tdd-agent calls, reducing overhead while maintaining TDD discipline.

**Actions**:

1. **Extract steps from plan** and analyze each step for:
   - Target files (create/modify)
   - Dependencies (detect using these rules):
     - **Explicit**: Step description contains "after step N" or "requires step N"
     - **Implicit write-read**: Step B reads/imports file that Step A creates or modifies
     - **Implicit shared write**: Both steps modify the same file → must be sequential
     - **Independent**: No shared files, no explicit ordering mentioned
   - Complexity and estimated lines:
     - Simple (1 file): ~30 lines, ~15 tests
     - Medium (1-2 files): ~60 lines, ~30 tests
     - Complex (3+ files): ~100 lines, ~50 tests

2. **Group steps into batches** using these criteria:
   - **File cohesion**: Steps targeting same/related files → batch together
   - **Sequential chain**: Step N+1 depends only on N → batch together
   - **Size threshold**: Combined estimated lines < 150 → batch together
   - **No blockers**: No user approval needed between steps

3. **Calculate test allocation per batch**:
   - Use complexity-based counts: simple (~15), medium (~30), complex (~50)
   - **Batch cap**: 100 tests maximum
   - If sum exceeds 100, distribute proportionally: `adjusted = (step_count / total) × 100`
   - Example: [50, 50, 15] over cap → [43, 43, 14] after proportional reduction

4. **Identify parallel batches**: Batches with no inter-dependencies can run simultaneously
   - Build dependency graph from step analysis (step 1)
   - Batches are independent if: no batch contains steps that depend on steps in other batch

5. **Create Phase 3 child plan items per batch** (with dependencies described in prose):
   ```json
   {
     "plan": [
       {"step": "Phase 1: Discovery - Understand what to build and existing patterns", "status": "completed"},
       {"step": "Phase 2: Architecture - Design implementation approach with user approval", "status": "completed"},
       {"step": "Phase 3: Implementation - Parent phase for approved plan steps", "status": "pending"},
       {"step": "Phase 3.1: Batch 1 [Steps 1-3] - User model + validation + tests", "status": "pending"},
       {"step": "Phase 3.2: Batch 2 [Steps 4-5] - UserService + tests", "status": "pending"},
       {"step": "Phase 3.3: Batch 3 [Step 6] - API endpoint; wait for Phase 3.2", "status": "pending"},
       {"step": "Phase 4: Quality Verification - Review agents verify changes", "status": "pending"},
       {"step": "Phase 5: Complete - Summarize what was built", "status": "pending"}
     ]
   }
   ```

   **Do not** replace the plan with only batch items. The Phase 3 parent and
   Phases 4-5 must remain visible.

6. **For each batch, invoke tdd-agent** using the spawn_agent tool:

```
Use spawn_agent tool with agent_type: "rptc:tdd-agent":

[Prepend the Environment Context Block]

## Context
- Feature: [description]
- Batch: Steps [N, N+1, ...] - [batch summary]
- Previous batches completed: [list]

## Steps in This Batch

### Step N: [name]
- Files: [list]
- Tests to generate: [calculated count]
- Complexity: [simple|medium|complex]

### Step N+1: [name]
- Files: [list]
- Tests to generate: [calculated count]
- Complexity: [simple|medium|complex]

## Test Allocation
Generate tests for ALL steps in batch (~[total] tests):
- Allocate per step based on complexity scores above
- Cover: happy paths, edge cases, errors, integration

## TDD Cycle (per step in batch)
For each step in order:
1. RED: Write ALL tests for this step. Run them. Confirm they fail.
   FILE LOCKOUT: Only test files may be created/modified during RED.
   Output RED GATE CHECK before proceeding to GREEN.
2. GREEN: Implement minimal code to pass (NOW edit production files)
3. REFACTOR: Improve while green
Then move to next step in batch.
```

7. **Launch parallel batches** simultaneously when independent:
   - Identify batches with no inter-dependencies (from step 4)
   - Invoke ALL independent spawn_agent calls in the same message (parallel execution)
   - Wait for all to complete before processing dependent batches
   - Example: Batch A and B independent → invoke both `spawn_agent` calls with `agent_type: "rptc:tdd-agent"` together

   **Codex spawn barrier**: After launching tdd-agent batches, the main
   context waits for those batches to return. Do not start independent research,
   ad hoc implementation, or self-verification in the same scope while the agents
   run. Allowed parent work while waiting is coordination only: record spawned
   agent IDs, call `wait_agent`, and keep `update_plan` accurate. Process
   agent results only after the required batches return.

7b. **Verify batch compliance**: After each tdd-agent batch returns, check the exit verification block:
    - `Test-First Followed: YES` → mark batch complete
    - `Test-First Followed: NO` → flag as TDD violation, ask user whether to re-run or accept

8. **Update task status** as each `Phase 3.x` batch completes (an `update_plan` call with the full `plan` list and updated statuses)
9. **Handle failures**: If batch fails after 3 attempts, ask user for guidance

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

**Example Batching**:
```
Plan steps:                          Batched execution:
1. Create User model      ─┐
2. Add validation         ├─► Batch A [1,2,3] → 1 agent ─┐
3. Write User tests       ─┘                             ├─ parallel
4. Create UserService     ─┬─► Batch B [4,5] → 1 agent ──┘
5. Write Service tests    ─┘
6. Add API endpoint       ───► Batch C [6] → 1 agent (waits for B)

Result: 6 steps → 3 agents (vs 6 agents), ~40% token reduction
```

---

## Phase 4: Quality Verification

Call `update_plan` with the full `plan` list. Preserve Phases 1-5 and add
verification work as `Phase 4.x` child items. Phase 4 starts only after all
`Phase 3.x` implementation items are complete.

**Goal**: Verify changes and report findings for main context to address.

> 💡 **Tool Reminder**: Use Serena (`find_referencing_symbols`, `search_for_pattern`) when applying auto-fixes from verification findings.

**Mode**: Report-only. Verification agents DO NOT make changes—they report findings. Main context handles all fixes.

**Phase boundary**: Phase 3 implementation checks are not Phase 4 verification.
Running affected tests, checking diffs, or reading changed files in the main
context does not satisfy Phase 4. Phase 4 requires the selected RPTC verification
agent calls below. If verification agents are unavailable, report that as a
workflow blocker instead of silently substituting self-review.

**Authorization rule**: The active `rptc:rptc-feat` workflow already authorizes
mandatory Phase 4 verification agents. When Phase 4 starts, launch the selected
RPTC verification agents automatically if they are available. Do not replace
them with local checks, and do not describe local tests, diffs, typechecks,
builds, or self-review as a "Phase 4 quality pass."

**Actions**:

1. **Collect files modified** during Phase 3 for verification

2. **Determine verification agent mode** (one-time project configuration):

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

3. **Select agents based on mode**:

   **Mode: `all`** — Launch all 3 agents (skip to step 4)

   **Mode: `automatic`** — Select based on changes:

   | Change Type | code-review | security | docs |
   |-------------|:-----------:|:--------:|:----:|
   | Source code in `auth/`, `api/`, `security/`, `middleware/` paths | ✅ | ✅ | Check keywords |
   | Source code (other paths) | ✅ | Check keywords | Check keywords |
   | Source code with `export` statements | ✅ | Check keywords | ✅ |
   | Test files only | ✅ | ❌ | ❌ |
   | Dependencies changed (`package.json`, `requirements.txt`, etc.) | ❌ | ✅ | ❌ |
   | Docs/markdown only | ❌ | ❌ | ✅ |
   | Config files (non-sensitive) | ❌ | ❌ | ✅ |

   **Keyword detection** (scan git diff):
   - Security keywords: `password`, `token`, `secret`, `auth`, `session`, `crypto`, `hash`, `sql`, `exec`, `eval` → include security-agent
   - API keywords: `export`, `interface`, `endpoint`, `route`, `version`, `deprecated` → include docs-agent

   **Default**: If uncertain, include the agent

   **Mode: `minimal`** — Only launch when strongly indicated:
   - code-review: **ALWAYS** (minimum floor — at least one verification agent must launch)
   - security: Only if auth/api paths OR security keywords found
   - docs: Only if doc files changed OR `export` keyword found

4. **Create Phase 4 child plan items** for selected verification work:
   ```json
   {
     "plan": [
       {"step": "Phase 1: Discovery - Understand what to build and existing patterns", "status": "completed"},
       {"step": "Phase 2: Architecture - Design implementation approach with user approval", "status": "completed"},
       {"step": "Phase 3: Implementation - Execute approved plan steps", "status": "completed"},
       {"step": "Phase 4: Quality Verification - Parent phase for review agents and findings", "status": "pending"},
       {"step": "Phase 4.1: Launch selected report-only verification agents", "status": "in_progress"},
       {"step": "Phase 4.2: Consolidate high-confidence findings", "status": "pending"},
       {"step": "Phase 4.3: Address verification findings", "status": "pending"},
       {"step": "Phase 4.4: Re-run verification if requested", "status": "pending"},
       {"step": "Phase 5: Complete - Summarize what was built", "status": "pending"}
     ]
   }
   ```

5. **Launch selected verification agents** — Make spawn_agent calls for each selected agent:

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

   prompt: "Review code quality for these files: [list files].
   Focus: complexity, KISS/YAGNI violations, dead code, readability.
   REPORT ONLY - do not make changes. Output: confidence-scored findings (≥80 only)."
   ```

   **Security Agent** (if selected):
   ```
   Use spawn_agent tool with agent_type: "rptc:security-agent":

   [Prepend the Environment Context Block]

   prompt: "Security review for these files: [list files].
   Focus: input validation, auth checks, injection vulnerabilities, data exposure.
   REPORT ONLY - do not make changes. Output: confidence-scored findings (≥80 only)."
   ```

   **Documentation Agent** (if selected):
   ```
   Use spawn_agent tool with agent_type: "rptc:docs-agent":

   [Prepend the Environment Context Block]

   prompt: "Review documentation impact for these files: [list files].
   Focus: README updates, API doc changes, inline comment accuracy, breaking changes.
   REPORT ONLY - do not make changes. Output: documentation updates needed (≥80 only)."
   ```

   **Codex spawn barrier**: After launching verification agents, immediately call
   `wait_agent` and wait for all selected agents to return. Do not perform
   independent main-context verification, inspect more files, consolidate
   findings, or start fixes while agents run. The parent session resumes
   substantive work only after reports return.

6. **Consolidate findings** from launched agents:
   - Categorize: bugs, security, style, structural, documentation
   - Filter to high-confidence issues only (≥80)

7. **Create Phase 4 child tasks for findings** (auto-fix by default):
   ```json
   {
     "plan": [
       {"step": "Phase 1: Discovery - Understand what to build and existing patterns", "status": "completed"},
       {"step": "Phase 2: Architecture - Design implementation approach with user approval", "status": "completed"},
       {"step": "Phase 3: Implementation - Execute approved plan steps", "status": "completed"},
       {"step": "Phase 4: Quality Verification - Parent phase for review agents and findings", "status": "pending"},
       {"step": "Phase 4.1: Launch selected report-only verification agents", "status": "completed"},
       {"step": "Phase 4.2: Consolidate high-confidence findings", "status": "completed"},
       {"step": "Phase 4.3.1: [Category] Finding 1 - description (file:line)", "status": "pending"},
       {"step": "Phase 4.3.2: [Category] Finding 2 - description (file:line)", "status": "pending"},
       {"step": "Phase 4.4: Re-run verification if requested", "status": "pending"},
       {"step": "Phase 5: Complete - Summarize what was built", "status": "pending"}
     ]
   }
   ```

8. **Auto-fix findings** (no user approval needed for most issues):

   **Fix automatically** (Tier 2-4):
   - Nits: naming, formatting, minor style issues
   - Dead code removal
   - Missing error handling
   - Documentation updates
   - Test coverage gaps
   - Minor refactoring (<30 lines)

   **Ask user FIRST** (Tier 1 or significant work):
   - Architecture changes (layer violations, new abstractions)
   - Security vulnerabilities (may need broader review)
   - Breaking API changes
   - Major refactoring (>50 lines or multiple files)
   - Integration issues (orphan code - user decides: wire up or remove)

   **Process**:
   - Work through finding tasks sequentially
   - For auto-fix items: Apply fix, an `update_plan` call with the full `plan` list and updated statuses
   - For ask-first items: Use request_user_input with fix proposal, then apply or skip
   - Mark all finding tasks complete as addressed

9. **User Acknowledgment**:

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

Mark remaining tasks complete. Output 1-2 sentences: what changed, ready for `rptc:rptc-commit`.

Call `update_plan` with the full `plan` list, setting completed items to `completed`, the active item to `in_progress`, and future items to `pending`.

---

## Key Principles

1. **Single approval point**: ask the user to leave Plan Mode / switch to execution mode, then halt until confirmed after Architecture phase
2. **Ask when uncertain**: Use request_user_input only when genuinely unclear
3. **Smart parallelism**: Parallelize independent steps, sequence dependent ones
4. **Task-appropriate workflow**: TDD for code, direct execution for non-code
5. **Auto-fix by default**: Fix Tier 2-4 issues automatically; ask only for Tier 1 or major changes
6. **Confidence filtering**: Only surface issues ≥80 confidence
7. **Goal+Actions format**: Trust agents to handle details

---

## Error Handling

- **Discovery fails**: Ask user for more context
- **All plans miss requirements**: Re-run planning with additional constraints from user
- **TDD step fails 3x**: Pause, ask user for guidance
- **Quality verification finds critical issues**: Block completion, show findings
- **Phase 4 not executed**: INVALID STATE. Return to Phase 4 and execute it. Phase 5 cannot proceed without verification.
