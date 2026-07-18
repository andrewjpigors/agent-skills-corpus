---
name: team-workflow
description: >
  Meta-skill for structured multi-agent product development.
  WAVE Architecture: autonomous cycles with adaptive team composition.
  Each cycle: RECON (reconnaissance + role selection) → COMPOSE → EXECUTE → RETRO.
  Team adapts per cycle based on current state and needs.
  Supports: RESEARCH, BUILD, PRODUCT, FULL_CYCLE, CUSTOM.
  Triggers: "team", "create team", "agent team", "parallel agents",
  "team workflow", "собери команду", "командная работа", "создай продукт"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Task, AskUserQuestion, WebSearch, WebFetch
user-invocable: true
---

# Team Workflow Skill v2.1 — Adaptive WAVE Architecture

> "A single agent doing planning + execution simultaneously is the primary source of failure."
> — Universal finding across LangGraph, CrewAI, AutoGen, Cursor, Devin, MetaGPT (2024-2026)

> "Pre-defined role library + task analysis orchestrator that selects per subtask = emerging consensus."
> — CaptainAgent (+21.94%), MASFly (SOTA 61.7%), AgentVerse (ICLR 2024)

**Meta-skill for structured multi-agent product development in Claude Code.**

## Version History

- **v2.1 (Feb 2026):** Autonomous cycles, adaptive team composition, role library, reconnaissance
- **v2.0 (Feb 2026):** WAVE Architecture — sequential phases, artifact contracts, anti-drift guards
- **v1.0 (Feb 2026):** Original flat team model

## Research Basis

This skill is informed by extensive external research — an internal synthesis of public sources (LangGraph, MetaGPT, CaptainAgent, AgentVerse, and other published multi-agent orchestration work).

---

## Terminology (FIXED — use consistently)

```
CYCLE  = A full autonomous pass: research → plan → implement → verify.
         Each cycle is self-contained. Cycle 2 looks at the result of cycle 1
         and may change team composition, priorities, or approach.
         User says "5 iterations" = 5 cycles.

PHASE  = A stage within a cycle.
         4 phases: RECON → COMPOSE → EXECUTE → RETRO.
         Every cycle goes through all 4 phases.

WAVE   = A unit of execution within the EXECUTE phase.
         BIZ wave (research/plan), DEV wave (code), LAUNCH wave (marketing).
         Waves within EXECUTE run sequentially.

ROLE   = A subagent specialization, selected from the Role Library.
         Never generated from scratch — always taken from the library.
```

**Mapping to user language:**

- "let's do 3 iterations" = 3 cycles
- "research on the first iteration" = first cycle, BIZ wave
- "then we improve it" = next cycle, which looks at the previous cycle's result

---

## Core Principles (Non-Negotiable)

### 1. SEPARATION: Planning ≠ Execution

NEVER interleave research/planning with coding in the same agent or wave.
BIZ wave produces artifacts. DEV wave reads artifacts and produces code.
Source: Cursor, LangGraph, MetaGPT, Devin — all enforce this.

### 2. ARTIFACTS: Files on Disk = Contract Between Waves

Each wave produces a structured Markdown artifact saved to disk.
The next wave reads this artifact as its input. NOT chat history.
Source: MetaGPT (PRD→Architecture→Code), LangGraph (TypedDict state), Devin (Wiki).

### 3. SUBAGENTS: Task Tool, Not Agent Teams

Use `Task` tool (subagents) for all agent work. NOT TeamCreate/Agent Teams.
Subagents are 5x cheaper, don't have the context compaction bug (#23620),
and work perfectly for sequential wave execution.
Source: Claude Code community consensus, Anthropic docs.

### 4. FRESH CONTEXT: Each Cycle = Clean Slate + State File

Long sessions cause context rot (performance drops after ~50% of 200K window).
Each cycle starts fresh. State transfers via files, not session memory.
Source: "Ralph Wiggum" pattern, Safoura Jolfaei two-agent architecture.

### 5. HIERARCHY: Orchestrator Decides, Workers Execute

You (the orchestrator) are the planner. Subagents are workers.
Workers do NOT coordinate with each other. They receive instructions and report back.
Source: Cursor scaling research, LangGraph supervisor pattern.

### 6. OBJECTIVE GATES: Verifiable Completion Criteria

Every wave has a measurable quality gate. Not "looks good" — but "file exists", "tsc passes", "tests green".
Source: Karpathy field notes, Cursor research.

### 7. ADAPTIVE COMPOSITION: Select From Library, Don't Generate

Team composition adapts per cycle based on task analysis (reconnaissance).
Roles are SELECTED from a pre-defined library, NEVER generated from scratch.
Generating roles = hallucinated capabilities + role drift (5-70%).
Source: CaptainAgent, MASFly, MetaGPT lesson, Salesforce AI Research.

---

## Workflow Overview

```
SETUP (once):
  └── Overall task analysis, scale limits, state file creation
  └── USER APPROVAL

CYCLE 1:
┌──────────────────────────────────────────────────────────────────┐
│  RECON    → Analyze current state + RECONNAISSANCE               │
│             (what skills does THIS cycle need?)                   │
│  COMPOSE  → Select roles from ROLE LIBRARY, build prompts        │
│  EXECUTE  → BIZ-wave → [gate] → DEV-wave → [gate]               │
│  RETRO    → Scorecard, delta, recommend next cycle               │
│             USER GATE: continue / stop / adjust                  │
└──────────────────────────────────────────────────────────────────┘

CYCLE 2:
┌──────────────────────────────────────────────────────────────────┐
│  RECON    → Read state file from Cycle 1                         │
│             RECONNAISSANCE: maybe different team needed?         │
│  COMPOSE  → POSSIBLY DIFFERENT ROLES than Cycle 1                │
│  EXECUTE  → waves with updated team                              │
│  RETRO    → scorecard, delta, user gate                          │
└──────────────────────────────────────────────────────────────────┘

CYCLE N: ... (runs until max_cycles reached)

DEBRIEF (once):
  └── Final verification, summary, knowledge capture
```

---

## Trigger

- `/team-workflow [task description]`
- `create a team for [task]`
- `собери команду для [задача]` (Russian trigger: "assemble a team for [task]")
- `создай продукт [описание]` (Russian trigger: "create product [description]")
- Automatically when task complexity warrants multi-agent execution

---

## SETUP (Once, Before Cycles)

**Goal:** Understand overall task, clarify intent, set constraints, get user approval.

### S.0: CLARIFICATION (before task analysis)

Read the project (key files, existing state) and the user's request. Then present:

```
UNDERSTANDING CHECK
====================
Task:      [user's request in your own words — 2-3 sentences]
Approach:  [how you plan to structure the work — high level]
Questions:
  1. [Specific clarifying question if direction is ambiguous]
  2. [Or: "Direction is clear, no questions."]
```

Wait for user to confirm understanding or answer questions.
If direction is already detailed and unambiguous, keep questions minimal and move to S.1.
Incorporate any answers into the task brief below.

### S.1: Overall Task Analysis

```
TASK BRIEF
==========
Task:         [One-line description]
Goal:         [What success looks like — MUST be objectively verifiable]
Scope:        [Files/directories/deliverables affected]
Task Type:    [RESEARCH | BUILD | PRODUCT | FULL_CYCLE | CUSTOM]
Constraints:  [Time, quality, tech stack limitations]
Dependencies: [External systems, data, user input needed]
```

### S.2: Task Type Detection

```
TASK TYPE MATRIX
=================

Task Type     │ Waves per Cycle              │ Example
──────────────┼──────────────────────────────┼─────────────────────
RESEARCH      │ BIZ-wave only                │ "research the competitors"
──────────────┼──────────────────────────────┼─────────────────────
BUILD         │ BIZ-wave → DEV-wave          │ "build a CLI tool"
──────────────┼──────────────────────────────┼─────────────────────
PRODUCT       │ BIZ-wave → DEV-wave          │ "build product X"
──────────────┼──────────────────────────────┼─────────────────────
FULL_CYCLE    │ BIZ-wave → DEV-wave → LAUNCH │ "build and launch it"
──────────────┼──────────────────────────────┼─────────────────────
CUSTOM        │ User defines                 │ (ask user)
```

### S.3: Scale Limits

```
SOFT GUIDELINES (user can override):
□ Max 1 product per workflow run (recommended)
□ Max 5 subagents per wave (performance)
□ Max 3 waves per cycle (complexity)
```

### S.4: Artifact & Gate Definitions

Define ONCE, apply to all cycles:

```
ARTIFACT TEMPLATES
==================

BIZ WAVE → PRD / Research Artifact:
  File: .claude/research/{task}/prd.md (or research.md)
  Required sections:
    ## Problem Statement
    ## Target Users (with JTBD)
    ## Requirements (P0 / P1 / P2)
    ## Success Metrics
    ## Technical Constraints
    ## Out of Scope
  Validation: All sections non-empty, P0 list has >=3 items

DEV WAVE → Implementation Artifact:
  File: .claude/research/{task}/implementation.md
  Required sections:
    ## Architecture Decisions
    ## Files Created/Modified (list with paths)
    ## Tests Written
    ## Known Limitations
    ## How to Verify (runnable commands)
  Validation: Files list matches actual git diff, verify commands work

LAUNCH WAVE → Launch Artifact:
  File: .claude/research/{task}/launch.md
  Required sections:
    ## Launch Channels (with timeline)
    ## Copy/Messaging (per channel)
    ## Assets Needed
    ## Success Metrics (Day 1, Week 1, Month 1)
  Validation: All channels have copy, metrics are measurable
```

```
QUALITY GATES (per wave type)
==============================

BIZ gate:
  □ Artifact file exists
  □ All required sections non-empty
  □ P0 >= 3 items
  □ Metrics are measurable (not vague)

DEV gate:
  □ Code files exist at expected paths
  □ npx tsc --noEmit passes (if TypeScript)
  □ cargo check passes (if Rust)
  □ Tests exist and pass
  □ "How to Verify" commands work

LAUNCH gate:
  □ All channel copy exists
  □ No placeholder text remaining
```

### S.5: State File Creation

```
STATE FILE
==========
File: .claude/research/{task}/state.md

# {Task Name} — Cycle State

## Overall
Task Type: {type}
Max Cycles: {N}
Status: IN_PROGRESS

## Cycle History
(updated after each cycle)
```

### Hard Stop: SETUP Approval

```
⏸️ STOP: SETUP APPROVAL
─────────────────────────
PRESENT to user:
  1. Task brief (goal + scope + type)
  2. Wave structure per cycle
  3. Scale limits applied
  4. Artifact templates & quality gates

ASK: "Approve setup? (ok / adjust [what])"

DO NOT start cycles without explicit approval.
```

---

## Per-Cycle Phases

Each cycle goes through ALL 4 phases. Each cycle is autonomous.

### Phase 1: RECON (per cycle)

**Goal:** Analyze current state and determine what THIS cycle needs.

#### 1.1: Current State Analysis

Read BOTH the state file AND the actual project code/files. The state file tells you
what was attempted. The actual code tells you what really works.

```
CYCLE {N} STATE
===============
What exists from previous cycles:
  - [list of artifacts, code, tests — verified by reading actual files]
  - [what works, what's broken/missing]

User perspective (REQUIRED):
  - What can a user DO right now with the product?
  - What's the first thing that would confuse or frustrate them?
  - What's missing for the core user flow to work end-to-end?

What this cycle should focus on:
  - [specific goals for THIS cycle — prioritized by user impact]
  - [based on RETRO delta from previous cycle, or initial task if cycle 1]
```

#### 1.2: EXTERNAL RESEARCH (optional but recommended)

If the task involves competitors, best practices, or market context — launch a quick
external research subagent BEFORE team selection:

```
EXTERNAL RESEARCH PROMPT (optional, ~1-2 min)
==============================================
Task for this cycle: {cycle goal from 1.1}
Project: {path} — read key files for context

Quick external scan:
1. Search for competitors/alternatives doing similar work (Exa/WebSearch)
2. Search for best practices and common patterns (Exa/WebSearch)
3. Note any data points that should inform this cycle's work

Output: 5-10 bullet points with sources. Save to state file under this cycle.
Skip if: pure code refactoring, internal tooling, or no external context needed.
```

(Research basis: field experience showed that external research before implementation
produces substantially better results. team-light uses this as mandatory step;
in team-workflow it's optional but strongly recommended for PRODUCT and FULL_CYCLE types.)

#### 1.3: RECONNAISSANCE (adaptive team selection)

Launch 1 subagent (sonnet, ~30 sec) to analyze what skills this cycle needs:

```
RECONNAISSANCE PROMPT
=====================
Task for this cycle: {cycle goal from 1.1}
Current state: {what exists}
External research findings: {from 1.2, if available}
Available roles: {role library summary}

Questions to answer:
1. What domain expertise does this cycle need?
2. What technical skills are critical?
3. Which roles from the library are essential vs unnecessary?
4. Any domain-specific context the team should know?

Output: recommended roles (2-5) with justification
```

Result example:

```
RECONNAISSANCE RESULT (Cycle 1 — an MCP server project)
=============================================
Domain: MCP protocol, TypeScript, tool schemas
Critical skills: @modelcontextprotocol/sdk, Rust-TS bridge
Recommended BIZ roles: product-lead, tech-researcher
Recommended DEV roles: backend-dev, api-designer, qa-tester
NOT needed: growth-marketer, frontend-dev, copywriter
Context: existing Rust scoring engine to wrap as MCP tools
```

```
RECONNAISSANCE RESULT (Cycle 3 — same MCP server project)
=============================================
Domain: UI dashboard for MCP metrics
Critical skills: React, data visualization
Recommended BIZ roles: product-lead, ux-researcher     ← CHANGED
Recommended DEV roles: frontend-dev, qa-tester          ← CHANGED
NOT needed: api-designer, backend-dev                   ← were in Cycle 1
Context: MCP server works, now need monitoring dashboard
```

#### 1.4: Complexity Check

```
COMPLEXITY
==========
  1-7   → SOLO: no team needed, execute directly
  8-12  → SINGLE WAVE: 1-2 subagents
  13+   → MULTI-WAVE: full wave architecture
```

### Phase 2: COMPOSE (per cycle)

**Goal:** Build team from Role Library based on reconnaissance results.

#### 2.1: Role Selection from Library

Based on reconnaissance, select roles. See ROLE LIBRARY section below.

Rules:

```
COMPOSITION RULES
=================
□ Minimum for any team: Direction + Execution + Quality
□ Every deliverable has exactly ONE owner
□ No two subagents write to the same file
□ BIZ-wave agents: NO write access to code directories
□ DEV-wave agents: READ access to BIZ artifacts
□ Total subagents per wave <= 5
□ Roles SELECTED from library, NEVER invented
```

#### 2.2: Prompt Generation

Each subagent gets a structured prompt:

```
SPAWN PROMPT TEMPLATE
=====================
[ROLE]: You are a {role} specializing in {domain from reconnaissance}.
[CONTEXT]: Project: {project}. Stack: {stack}. Cycle: {N} of {max}.
[STATE]: Read current state first: {path to state file}
[INPUT]: Read artifact from previous wave: {path} (if applicable)
[TASK]: {concrete task with acceptance criteria}
[SCOPE]: Work ONLY in: {specific files/directories}
  DO NOT modify: {exclusion list}
[DELIVERABLE]: Save output to: {specific file path}
[QUALITY]: Your work is DONE when:
  - {objective criterion 1}
  - {objective criterion 2}
[CONSTRAINT]: Say BLOCKED with specific reason if you cannot complete.
```

### Phase 3: EXECUTE (per cycle)

**Goal:** Run waves sequentially, enforce gates.

#### 3.1: Wave Execution

```
FOR EACH wave in cycle:

  1. ANNOUNCE: "Cycle {N}, Wave {M}: {wave_type}"

  2. SPAWN subagents (via Task tool):
     - Independent: in PARALLEL (run_in_background=true)
     - Dependent: SEQUENTIALLY

  3. WAIT for completion (timeout: 10 min per subagent)

  4. COLLECT results, verify deliverables exist

  5. SYNTHESIZE (if multiple subagents):
     - Orchestrator reads all outputs
     - Writes unified wave artifact
     - This is orchestrator's job, not subagent's

  6. QUALITY GATE:
     - If PASS: update state file, proceed to next wave
     - If FAIL: re-run specific subagent (max 1 retry)
     - If still FAIL: STOP, ask user

  7. UPDATE state file with wave results
```

#### 3.2: Communication Rules

```
Subagents do NOT talk to each other.

Orchestrator → Subagent: via spawn prompt (Task tool)
Subagent → Orchestrator: via result (Task tool return)
Wave 1 → Wave 2: via artifact file on disk
Cycle N → Cycle N+1: via state file on disk
```

### Phase 4: RETRO (per cycle)

**Goal:** Evaluate cycle, decide on next cycle.

#### 4.1: Cycle Scorecard

```
CYCLE {N} SCORECARD
====================
                         Target    Actual    Status
BIZ artifact exists      YES       [Y/N]     PASS/FAIL
BIZ gate criteria        [list]    [list]    [X/Y passed]
DEV code exists          YES       [Y/N]     PASS/FAIL
DEV gate criteria        [list]    [list]    [X/Y passed]
─────────────────────────────────────────────────
Overall:                 [X/Y gates passed]
Team used:               [roles from this cycle]
```

#### 4.2: Delta Analysis

```
DELTA ANALYSIS
==============
User impact (REQUIRED):
  - What can the user now DO that they couldn't before this cycle? [specific, testable]
  - Does the core user flow work end-to-end? [yes/no + details]

What exists now:
  - [artifacts + code produced in this cycle]

What improved vs previous cycle:
  - [specific improvements]

What's still missing (prioritized by user impact):
  Gap 1: [specific gap — how it affects user]
  Gap 2: [specific gap — how it affects user]

Team assessment:
  - Roles that worked well: [list]
  - Roles that were unnecessary: [list]
  - Roles MISSING that would help next cycle: [list]  ← KEY for adaptive composition
```

#### 4.3: Cycle Decision

```
IF all gates PASS AND no critical gaps:
  → RECOMMEND: DEBRIEF (done)

IF gaps exist but progress was made:
  → RECOMMEND: Next cycle
  → Show: what changes (including team if needed)
  → Write delta to state file

IF gates FAIL:
  → RECOMMEND: Re-compose (roles may be wrong)
  → Root cause analysis

IF cycle count = max_cycles:
  → FORCE: DEBRIEF with current results
```

#### Cycle Decision (Autonomous)

```
AUTO-CONTINUE unless:
  - All gates PASS AND no critical gaps → DEBRIEF
  - Cycle count = max_cycles requested by user → DEBRIEF

Write scorecard + delta to state file, proceed to next cycle automatically.
```

#### 4.4: Integration Test Milestone

Every 8-10 cycles (or at natural breakpoints), run a broader integration check:

```
INTEGRATION TEST MILESTONE (every ~10 cycles)
==============================================
□ Full build passes (tsc --noEmit / cargo check / npm run build)
□ All existing tests still pass (no regressions)
□ Cross-module smoke test: key user flows work end-to-end
□ State file review: are we still aligned with original task direction?
□ Scope check: have we drifted from the goal?

IF regressions found:
  → Next cycle MUST fix regressions before new work
  → Add "regression fix" as priority in state file

IF scope drift detected:
  → Log in state file, recommend course correction to user
```

(Research basis: e.g., one desktop app project used integration tests at cycles 10, 18, 26, 29 — all caught
issues early; another project — a documentation tool — split 50 cycles into 4 series of 10-20, each starting with a clean check.
Without milestones, accumulated drift compounds over long runs.)

#### 4.5: State File Update

```
Update state file:
  - Cycle scorecard
  - Delta analysis
  - Team used (roles + effectiveness)
  - Decision (continue/stop)
  - Delta notes for next cycle (including team changes)

The state file + actual project code are inputs for the next cycle's RECON.
(State file alone is insufficient — always verify against real project state.)
```

---

## DEBRIEF (Once, After All Cycles)

**Goal:** Final verification, report, knowledge capture.

### D.1: Final Verification

```
□ All expected artifacts exist
□ State file complete with all cycles documented
□ If code expected: compiles and runs
□ If research expected: sources cited
□ Working directory clean or committed
```

### D.2: Summary Report

```
TEAM WORKFLOW SUMMARY
=====================
Task:        [original task]
Cycles:      [N completed]
Task Type:   [RESEARCH/BUILD/PRODUCT/FULL_CYCLE]

TEAM EVOLUTION:
  Cycle 1: [roles used]
  Cycle 2: [roles used — note changes]
  Cycle 3: [roles used — note changes]

DELIVERABLES:
  ✅ [deliverable] — [path]
  ⚠️ [partial] — [reason]

QUALITY: [X/Y gates passed across all cycles]
```

### D.3: Knowledge Capture (OPTIONAL convention)

Applies if your project keeps a `.claude/memory/` knowledge base — otherwise write these notes to `.claude/research/`.

```
IF significant decisions → update .claude/memory/decisions.md
IF new patterns → update .claude/memory/MEMORY.md
IF project status changed → update .claude/memory/context.md
```

---

## Role Library

Roles are organized by 6 universal categories (from organizational science: Belbin + McKinsey + software team research).

**Rule: Minimum for any team = Direction + Execution + Quality.**

```
ROLE LIBRARY
=============

DIRECTION (why and what):
┌──────────────────────┬─────────┬────────────────────────────────────────┐
│ Role                 │ Model   │ What they do                           │
├──────────────────────┼─────────┼────────────────────────────────────────┤
│ product-lead         │ opus    │ PRD, scope, priorities, final artifact │
│ tech-lead            │ sonnet  │ Technical direction, architecture call │
│ project-coordinator  │ sonnet  │ Dependencies, timeline, risk tracking  │
└──────────────────────┴─────────┴────────────────────────────────────────┘

INTELLIGENCE (learning and research):
┌──────────────────────┬─────────┬────────────────────────────────────────┐
│ market-researcher    │ sonnet  │ Competitors, market size, trends       │
│ tech-researcher      │ sonnet  │ Technical patterns, protocols, libs    │
│ ux-researcher        │ sonnet  │ User behavior, usability, pain points  │
│ domain-expert        │ sonnet  │ Deep domain knowledge (custom prompt)  │
│ devils-advocate      │ sonnet  │ Challenge findings, counterarguments   │
└──────────────────────┴─────────┴────────────────────────────────────────┘

ARCHITECTURE (how it's structured):
┌──────────────────────┬─────────┬────────────────────────────────────────┐
│ system-architect     │ opus    │ System design, component boundaries    │
│ api-designer         │ sonnet  │ API contracts, schemas, protocols      │
│ data-modeler         │ sonnet  │ Database schema, data flows            │
└──────────────────────┴─────────┴────────────────────────────────────────┘

EXECUTION (building):
┌──────────────────────┬─────────┬────────────────────────────────────────┐
│ frontend-dev         │ sonnet  │ React, UI components, styling          │
│ backend-dev          │ sonnet  │ Servers, APIs, business logic          │
│ fullstack-dev        │ sonnet  │ Both frontend and backend              │
│ cli-dev              │ sonnet  │ CLI tools, argument parsing, UX        │
│ infra-dev            │ sonnet  │ CI/CD, deployment, Docker              │
└──────────────────────┴─────────┴────────────────────────────────────────┘

QUALITY (validation):
┌──────────────────────┬─────────┬────────────────────────────────────────┐
│ code-reviewer        │ sonnet  │ Code quality, security, best practices │
│ qa-tester            │ sonnet  │ Tests, edge cases, integration testing │
│ security-reviewer    │ sonnet  │ OWASP, auth, data protection           │
└──────────────────────┴─────────┴────────────────────────────────────────┘

COMMUNICATION (messaging):
┌──────────────────────┬─────────┬────────────────────────────────────────┐
│ copywriter           │ sonnet  │ Landing pages, social posts, README    │
│ docs-writer          │ sonnet  │ Technical docs, API docs, guides       │
│ growth-marketer      │ sonnet  │ GTM strategy, channels, viral loops    │
└──────────────────────┴─────────┴────────────────────────────────────────┘
```

**Subagent type mapping:**

```
Roles that produce CODE → subagent_type: general-purpose (REQUIRED)
  frontend-dev, backend-dev, fullstack-dev, cli-dev, infra-dev

Roles that produce RESEARCH/DOCS → subagent_type: general-purpose
  product-lead, tech-researcher, market-researcher, ux-researcher,
  domain-expert, devils-advocate, copywriter, docs-writer, growth-marketer

Roles that REVIEW → subagent_type: code-reviewer
  code-reviewer, security-reviewer

Roles that TEST → subagent_type: test-runner or general-purpose
  qa-tester
```

**Role prompt adaptation:**

The role name stays from the library. The system prompt is adapted based on reconnaissance:

```
Library role: backend-dev
Generic prompt: "You are a backend developer."
Adapted prompt: "You are a backend developer specializing in MCP server protocol
  using @modelcontextprotocol/sdk. The existing Rust scoring engine
  needs to be exposed as MCP tools via TypeScript wrapper."
```

---

## Token Optimization (1M Context Era)

With 1M context windows, token costs scale with accumulated context per agent.
These rules are MANDATORY for all team-workflow runs.

### Model Enforcement (from Role Library)

The Role Library already defines model per role. **ENFORCE these assignments:**

```
opus  ($$$) → product-lead, system-architect ONLY
sonnet ($$) → ALL other roles (research, dev, review, communication)
haiku  ($)  → ONLY for trivial checks (lint, file existence, format validation)
```

NOTE: In our testing, a small model proved insufficient for code-review —
it misses dead code, cross-file patterns, and architectural context.
Sonnet is the minimum for meaningful review.

When spawning subagents, ALWAYS pass the `model` parameter from Role Library.
Do NOT default to the orchestrator's model (which is typically Opus).

### Compact at Cycle Boundaries

```
AFTER every RETRO phase:
  IF orchestrator context > 50%:
    → /compact before starting next cycle's RECON
    → State file ensures no context is lost
```

### Subagent Tool Scoping

Each MCP server definition costs ~2-5K tokens in subagent context.
Limit tools by wave type:

```
BIZ-wave (research):  Read, Grep, Glob, Write, WebSearch, Exa
DEV-wave (code):      Read, Write, Edit, Bash, Glob, Grep
LAUNCH-wave (content): Read, Write, Glob, Grep, WebSearch
RECON subagent:       Read, Grep, Glob (minimal — just reads state)
```

### Research Output → Files

BIZ-wave subagents doing external research MUST write raw search results
to disk files, NOT keep them in context. The artifact should contain
synthesized findings only.

### Wave Result Compression

When a wave returns results to the orchestrator:

- Extract ONLY the deliverable summary (file list, gate status)
- Do NOT paste full subagent output into orchestrator context
- Reference artifact files by path instead

---

## Anti-Drift Guards

```
GUARD 1: Artifact Existence
  After each wave: artifact file exists?
  NO → STOP. Wave failed.

GUARD 2: Code Existence (DEV wave only)
  After DEV wave: code files created/modified?
  NO → STOP. "DEV wave produced only documents, not code."

GUARD 3: Scope Creep
  Subagents wrote outside their scope?
  YES → WARN user.

GUARD 4: Cycle Budget
  Cycle N > max_cycles?
  YES → FORCE DEBRIEF.

GUARD 5: Research-Only Drift
  Task is BUILD/PRODUCT and after 1 full cycle zero code?
  YES → STOP. "Workflow drifted to research-only."

GUARD 6: Role Hallucination
  Role selected not in library?
  YES → REJECT. "Select from library only."
```

---

## Anti-Patterns (EXPLICITLY FORBIDDEN)

### Pre-Labeled Cycle Themes

```
FORBIDDEN:
  Cycle 1: "Foundation"
  Cycle 2: "Deepening"
  Cycle 3: "Polish"

WHY: Each cycle must LOOK AT CURRENT STATE and decide what to improve.
```

### Research-Only Teams for BUILD Tasks

```
FORBIDDEN:
  Task: "Create a CLI product"
  Team: product-lead, market-analyst, growth-marketer
  Result: documents only, 0 code

WHY: BUILD tasks MUST have DEV wave with execution roles.
```

### Flat Team Doing Everything

```
FORBIDDEN:
  One team of 4 agents doing research AND coding simultaneously.

WHY: Waves enforce separation: BIZ produces artifacts, DEV produces code.
```

### Autonomous Multi-Product Runs

```
FORBIDDEN:
  "Build 7 products in one session"

WHY: Max 1 product per run. A catastrophic failure in an early autonomous run.
```

### Inventing Roles Not In Library

```
FORBIDDEN:
  Reconnaissance suggests: "AI Ethics Specialist"
  → This role doesn't exist in the library.
  → Instead: use domain-expert with adapted prompt.

WHY: Generated roles = hallucinated capabilities + role drift (5-70%).
Source: Salesforce AI Research, MetaGPT design decision.
```

### Same Team Every Cycle

```
FORBIDDEN:
  Cycle 1: backend-dev + qa-tester
  Cycle 2: backend-dev + qa-tester (same, no re-evaluation)
  Cycle 3: backend-dev + qa-tester (same again)

WHY: The whole point of per-cycle RECON is adaptive composition.
  Cycle 3 might need frontend-dev instead of backend-dev.
  Always run reconnaissance, even if team stays the same.
```

---

## Reference

### Model Selection

```
haiku  ($)  — Review, validation, simple checks
sonnet ($$) — DEFAULT. Implementation, research, reasoning
opus  ($$$) — Complex synthesis, architecture, lead roles
```

### Quick Start Examples

**Example 1: Research (1 cycle)**

```
USER: /team-workflow Research MCP server patterns

SETUP: Type=RESEARCH, 1 cycle, BIZ-wave only
  → user approves

CYCLE 1:
  RECON: reconnaissance → need tech-researcher + domain-expert(MCP)
  COMPOSE: lead=product-lead(opus), workers=tech-researcher, domain-expert
  EXECUTE: BIZ-wave → 3 subagents parallel → research artifact
  GATE: >=5 sources, confidence levels → PASS
  RETRO: all good → DEBRIEF
```

**Example 2: Build Product (2 cycles)**

```
USER: /team-workflow Build an MCP server, 2 iterations

SETUP: Type=BUILD, 2 cycles, BIZ+DEV waves
  → user approves

CYCLE 1:
  RECON: reconnaissance → MCP protocol skills needed
  COMPOSE:
    BIZ: product-lead, tech-researcher
    DEV: backend-dev(MCP specialist), api-designer, qa-tester
  EXECUTE:
    BIZ-wave → PRD artifact → GATE ✓
    DEV-wave → working MCP server → GATE ✓
  RETRO: "MVP works, missing dashboard UI"
  → user: "continue"

CYCLE 2:
  RECON: read state → need UI now, not more backend
  RECONNAISSANCE: → need frontend-dev, ux-researcher    ← TEAM CHANGED
  COMPOSE:
    BIZ: product-lead, ux-researcher                    ← was tech-researcher
    DEV: frontend-dev, qa-tester                        ← was backend-dev + api-designer
  EXECUTE:
    BIZ-wave → UI spec artifact → GATE ✓
    DEV-wave → dashboard React component → GATE ✓
  RETRO: all gates pass → DEBRIEF
```

**Example 3: Iterative Improvement (3 cycles)**

```
USER: /team-workflow Improve a Rust CLI tool, 3 iterations

SETUP: Type=BUILD, 3 cycles
  → user approves

CYCLE 1:
  RECON: reconnaissance → Rust CLI, npm wrapper
  COMPOSE: DEV: cli-dev(Rust), qa-tester
  EXECUTE: DEV-wave → basic CLI + tests → GATE ✓
  RETRO: "CLI works, no --ci flag, no JSON output"
  → user: "continue"

CYCLE 2:
  RECON: read state → need --ci flag + JSON
  RECONNAISSANCE: same domain, same team works
  COMPOSE: DEV: cli-dev(Rust), qa-tester              ← SAME team (justified)
  EXECUTE: DEV-wave → add --ci + JSON → GATE ✓
  RETRO: "Feature complete, need npm packaging"
  → user: "continue"

CYCLE 3:
  RECON: read state → need npm packaging now
  RECONNAISSANCE: → different skill needed!
  COMPOSE: DEV: infra-dev(npm/wasm), qa-tester         ← TEAM CHANGED
  EXECUTE: DEV-wave → npm package + publish → GATE ✓
  RETRO: all done → DEBRIEF

TEAM EVOLUTION: cli-dev → cli-dev → infra-dev
```

---

## Changelog

### v2.1 (Feb 2026) — Adaptive Composition

- **Added:** Terminology section (Cycle / Phase / Wave / Role — fixed definitions)
- **Added:** Role Library (22 roles across 6 categories) _(counts corrected)_
- **Added:** Reconnaissance step in RECON (per-cycle adaptive team selection)
- **Added:** Role Hallucination guard (Guard 6 after renumbering)
- **Added:** Anti-pattern: Same Team Every Cycle
- **Added:** Anti-pattern: Inventing Roles Not In Library
- **Changed:** Each cycle is fully autonomous (RECON+COMPOSE+EXECUTE+RETRO)
- **Changed:** SETUP phase separated from per-cycle work (runs once)
- **Changed:** "Iteration" terminology → "Cycle" throughout
- **Changed:** Team composition can change between cycles based on reconnaissance
- **Removed:** Fixed wave role templates (replaced by Role Library + selection)
- **Removed:** STRATEGIZE as separate phase (merged into SETUP)

### v2.0 (Feb 2026) — WAVE Architecture

- Replaced flat team model with sequential WAVE execution
- Removed Agent Teams (TeamCreate/TeamDelete) — subagents only
- Added artifact contracts, anti-drift guards, scale limits
- Added anti-patterns section

### v1.0 (Feb 2026) — Original

- Initial release with 6-phase lifecycle
- Flat team model, domain detection, Agent Teams support
