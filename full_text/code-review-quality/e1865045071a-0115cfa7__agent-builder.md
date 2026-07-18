---
name: agent-builder
description: "Use when: creating, refactoring, auditing, upgrading, or debugging Copilot custom agents, skills, instructions, prompts, or hooks for software engineering and agile delivery workflows across any language, framework, and platform."
---

# Agent Builder

Use this skill to design and generate high-quality Copilot customization bundles for software projects of any type. This is the single source of truth for the complete kit workflow, bundle shapes, and artifact behavioral requirements.

## Collaboration and Reuse

- **Used by**: `Agent Builder` (`.github/agents/agent-builder.agent.md`), `Universal Agent Generator` (`.github/agents/universal-agent-generator.agent.md`), `Universal Quality Auditor` (`.github/agents/universal-quality-auditor.agent.md`), `Universal Codebase Analyzer` (`.github/agents/universal-codebase-analyzer.agent.md`), `.github/instructions/agent-builder.instructions.md` (generation quality standards, file editing rules)
- **Upstream inputs**: Codebase analysis from `Universal Codebase Analyzer`, Copilot product docs from `copilot-docs-registry.md`
- **Downstream outputs**: Bundle architecture decisions, artifact behavioral requirements, generation and audit rules consumed by generator and auditor agents

## Use Cases

- Create a new custom agent for engineering or agile delivery
- Refactor or upgrade existing agent bundles
- Audit weak descriptions, frontmatter, or scopes
- Verify and improve an existing agent ecosystem
- Diagnose invocation failures for skills, instructions, prompts, or agents

## Universal Scope

All languages, frameworks, platforms, and build systems — including but not limited to: iOS, Android, cross-platform mobile (Flutter, React Native, KMP), web frontend (React, Angular, Vue, Svelte), backend (Node.js, Python, Java, Go, Rust, .NET, Ruby), cloud/infrastructure (AWS, GCP, Azure, Terraform, Kubernetes), desktop (Electron, Tauri, macOS, Windows), systems programming (C, C++, Rust), and data/ML (Python, R, Spark).

**Alignment rule**: The analyzer's codebase findings always override generic defaults. Generated agents must align to the project's actual technology profile — language version, framework, build system, testing tools, patterns — not idealized latest-version patterns.

## Default Behavior

- Operating mode selection: see Operating Modes below
- If the user chooses the wrong primitive, offer 2-3 better options
- Generate files in English by default
- Prefer portable designs unless the user asks for repo-locked behavior
- Multi-agent architecture when quality depends on distinct phases
- Hard audit gate for non-trivial bundles
- Generated agents must not declare `tools` or `mcp-servers` in frontmatter by default; omitting these fields keeps all tools (including user-configured MCP servers) accessible
- Generated agents must include explicit MCP tool preference guidance for any agent that may interact with external services — "do not restrict MCP in frontmatter" must not be misread as "do not use MCP at runtime"
- Align generated agents to the project's actual technology profile — never assume latest defaults when the codebase shows otherwise
- When invoked directly: confidence ≥ 95% before generation
- When invoked via prompt: skip confidence interview, analyze directly

## Operating Modes

**Discovery Mode** — requirements incomplete, overloaded, or inconsistent. Run adaptive interview until target workflow, scope, and quality bar are clear. Offer 2-3 architecture options when tradeoffs matter. Continue until confidence ≥ 95%.

**Fast Mode** — user has clear target and constraints. Confirm only missing facts that change the design. Move quickly into analysis → generation → auditing.

## Three Operating Flows

### Flow A: Greenfield — No agents exist
1. Clarify → 2. Analyze project → 3. Generate full bundle → 4. Audit → 5. Revise until PASS

### Flow B: Verify and Improve — Agents already exist
Triggered during Flow A when existing agents are detected, or invoked directly via `/generate-workflow-agents` when user wants to verify and improve an existing ecosystem.
1. Scan ecosystem → 2. Evaluate each agent → 3. Fix weak agents, fill gaps → 4. Audit → 5. Revise until PASS

### Flow C: Extend or Verify — Add new agent, or verify an existing one
Triggered via `/add-agent` prompt:
- **Extend (create)**: Clarify new workflow → Analyze project + existing agents → Generate new agent (no overlap) → Audit (ecosystem coherence) → Revise until PASS
- **Verify (single agent)**: Collect target files → Analyze ecosystem context → Evaluate against audit rubric → Fix findings → Re-audit until PASS

## Single-Session Completion Rule

The entire bundle must be generated within a single continuous session. Never abandon the workflow or leave generation incomplete.

- **Start to finish in one session**: Once generation begins, continue through analyze → generate → audit → revise → deliver without stopping.
- **Structured clarification**: When user input is genuinely needed, use `vscode_askQuestions` with 2-4 options and a recommended default. This keeps the session alive. Never write questions as plain response text — that ends the session. For low-risk ambiguity, continue with an explicit provisional assumption.
- **Audit failures**: When the auditor returns `REVISE`, fix every finding and re-audit in the same session. When `BLOCKED`, ask the missing questions immediately, wait for answers, then resume.
- **Error recovery**: If a tool fails, try alternatives within the same session. Escalate to the user only when no automated recovery is possible.
- **Completion behavior**: After finishing all tasks, use `vscode_askQuestions` to ask the user whether additional updates are needed. Do not self-terminate — only end the session when the user explicitly decides to stop.

This rule applies to the kit itself and to generated orchestrator agents.

## Workflow

### Standard User-Facing Phases

1. Analyze the codebase
2. Assess the project and choose bundle architecture
3. Ask targeted follow-up only if needed (auto-skip when possible)
4. Generate or update the bundle
5. Audit and iterate until PASS
6. Deliver the final result

Internal setup work (reading skill files, loading templates, scanning existing files) stays inside these phases, not as extra top-level steps.

### Kit Reference Files

The kit maintains one persistent reference file that the generator reads directly during generation:

- `.github/templates/agent-builder/copilot-docs-registry.md` — Copilot product behavior: frontmatter rules, primitives, tool behavior, hook behavior, instruction precedence. Updated by `Universal Copilot Docs Refresher` during kit maintenance.

Technology and platform domain knowledge is not maintained as a separate snapshot. It must come from the target project's codebase analysis: source files, project config, tests, resources, and migration signals. When project signal is thin, use cautious fallback assumptions and mark them explicitly.

The docs snapshot is an authoritative generator input. It does not need to be fetched each run — the kit owner updates it periodically using the refresher agent during kit maintenance sessions.

### Community Skill Discovery (Registry-Backed, MCP-Enriched)

During the analysis phase, the analyzer discovers community agent skills relevant to the target project's tech stack using a two-layer approach: a persistent registry snapshot as baseline, enriched with live data when MCP GitHub is available.

#### Kit Reference File

- `.github/templates/agent-builder/community-skill-registry.md` — Persistent snapshot of known community skill repositories organized by technology area, with categories, skill repos, content file paths, match criteria, and extracted knowledge summaries. Updated by `Universal Copilot Docs Refresher` during kit maintenance. The analyzer reads this as a reliable baseline that is always available regardless of MCP access.

#### Runtime Behavior

- **Timing**: After the analyzer determines the Technology Alignment Profile, as part of the analysis phase
- **Baseline**: Always read `community-skill-registry.md` first — this provides the full category listing and pre-extracted knowledge
- **Fallback chain**: MCP live + registry (best) → web fetch + registry (good) → registry only (acceptable). Never skip community skills entirely — the registry snapshot ensures baseline coverage.
- **Deep crawl**: When MCP GitHub is available, the analyzer should read the actual SKILL.md content files from each matching community skill repo (not just the directory README). This extracts specific patterns, anti-patterns, deprecated API warnings, and edge cases — the highest-value content that LLMs commonly get wrong.
- **Output**: Community Skill Discovery Results section in the analysis output — discovery method, registry snapshot date, matched categories, deep-crawl status, extracted knowledge per skill, cross-reference against project patterns, and per-agent-role recommendations for the generator
- **Generator consumption**: Embed specific knowledge (patterns, rules, anti-patterns) in generated agents for matching tech stack areas + recommend users install community skills for latest updates
- **Precedence**: Project-specific code patterns always override community skill guidance when they conflict. Conflicts must be noted explicitly.
- **Staleness management**: The registry snapshot is refreshed during kit maintenance. At generation time, if the snapshot is >30 days old, the analyzer notes the staleness so the user can decide whether to refresh before a major generation run.

### 1. Clarify the Outcome

Collect only facts that materially change architecture: target users, tasks, inputs/outputs, domain, autonomy level, tool restrictions, quality bar, platforms, framework constraints, delivery roles.

Clarification protocol:
- **Low-risk ambiguity**: Continue with an explicit provisional assumption.
- **High-risk ambiguity**: Use `vscode_askQuestions` per the Single-Session Completion Rule.
- Never stop the workflow entirely after asking a question.

### 2. Model the Workflow

Define: primary role, boundaries, non-goals, decision points, failure modes, artifacts. For any project: platform coverage, concurrency/lifecycle/testing expectations grounded in the project's actual technology profile from the analyzer.

### 3. Choose Primitives

Apply `.github/templates/agent-builder/primitive-decision-matrix.md`. Quick reference:

| Need | Primitive |
|------|-----------|
| Dedicated persona, context isolation | agent |
| Reusable repeatable workflow | skill |
| Always-on standards for matching files | instruction |
| Compact user-facing entry point | prompt |
| Deterministic enforcement | hook (validate with `hook-checklist.md` first) |

For linting tools: prefer instructions + agent validation steps over hooks. Add a hook only when: (1) team wants deterministic blocking, (2) tool reliably available everywhere, (3) false positives rare. See `hook-checklist.md`.

### 4. Build the Bundle

Use scaffold templates from `.github/templates/agent-builder/`:

| Artifact | Template |
|----------|----------|
| agent | `agent-template.md` |
| skill | `skill-template.md` |
| instruction | `instruction-template.md` |
| prompt | `prompt-template.md` |
| workflow asset | `workflow-asset-template.md` |

**Governance & Pipeline Templates** (also in `.github/templates/agent-builder/`):

| Artifact | Template |
|----------|----------|
| constitution | `constitution-template.md` |
| user playbook | `user-playbook-template.md` |
| review playbook | `review-playbook-template.md` |
| spec | `spec-template.md` |
| plan | `plan-template.md` |
| tasks | `tasks-template.md` |

Pick roles from `role-catalog.md`. Replace every `<...>` placeholder with project-grounded content.

**For `/generate-workflow-agents`, default to a full workflow kit:**
- `copilot-instructions.md` — workspace-level instructions automatically loaded by Copilot for all interactions. If the target project already has one, update it to integrate with the generated agent ecosystem while preserving existing relevant content. If the target project does not have one, create it. Content: concise project overview, technology stack, core conventions, agent ecosystem guide (available agents, primary prompt entry points, how to invoke), and cross-references to detailed instructions.
- Project context instruction (`<prefix>-project-context.instructions.md` with `applyTo: "**"`) for detailed project facts (architecture, domain glossary, extended conventions, bundle evolution guidance). Supplements `copilot-instructions.md` with depth that would be too verbose for the workspace-level file.
- Conductor + specialist agents with project-derived file prefix
- Multiple focused skills: delivery workflow (mandatory) + domain-specific (testing, investigation, review)
- Multiple narrow instructions: implementation conventions + test conventions at minimum
- Optional business-domain assets when project complexity warrants them (domain map, domain-scoped instructions, or a reusable business-rules workflow)
- At least 3 prompts: primary delivery + spec entry + secondary
- At least 2 templates/checklists for recurring hand-offs
- Explicit hook decision
- Bidirectional cross-references: agents reference skills, skills list their agents, templates are referenced by at least one file
- Intermediate working files deleted before finalizing
- Dirty worktree: preserve unrelated edits, stop only for direct path conflicts

**Naming rule**: Use a project-derived file prefix for generated files.

### 5. Validate Before Finalizing

Run `.github/templates/agent-builder/agent-audit-rubric.md`. Key checks:
- Cross-reference integrity (no orphaned templates or skills, bidirectional linking)
- Delivery workflow skill present
- `copilot-instructions.md` present (created or updated) with workspace-level content
- Project context instruction file present, no intermediate files left
- Frontmatter valid with discoverable descriptions
- Roles clear, goals explicit, output contracts defined
- Technology scope explicit

### 6. Audit and Revise

Send to auditor. If `REVISE`, patch every finding (major and minor) and re-audit. Do not accept or skip minor findings — all must be resolved before PASS. If `BLOCKED`, ask the missing questions. Repeat until PASS with zero open findings.

## Bundle Shapes

### Single: narrow single workflow
- 1 prompt + 1 agent or skill

### Focused: meaningful but focused workflow
- 1 agent + 1 skill + 1 prompt + optional instruction + 1 template

### Full Kit: delivery workflows (default for `/generate-workflow-agents`)
- `copilot-instructions.md` — workspace-level instructions (created or updated)
- Project context instruction (`<prefix>-project-context.instructions.md`, `applyTo: "**"`) for detailed project facts
- Constitution (`<prefix>-constitution.md`) — immutable governance rules and Phase -1 gates
- Conductor + 5+ specialist agents (business analysis, investigation, implementation, testing, review pipeline)
- Review pipeline: Code Review orchestrator + Functional Reviewer + Technical Reviewer + Platform/Framework Reviewer (conditional)
- 3+ skills (delivery workflow + spec-driven pipeline + domain-specific)
- 2+ instructions (implementation + testing)
- 3+ prompts (primary delivery + spec entry + secondary)
- 3+ templates for recurring hand-offs (including spec/plan/tasks)
- Essential docs: user-playbook, review-playbook
- Explicit hook decision (linter/formatter auto-format, build compile-check when warranted)
- Drift detection guidance in bundle evolution section
- Review memory promotion guidance in orchestrator

Full specification and minimums table in `universal-quality-auditor.agent.md`.

Every project receives the full bundle. Small projects benefit from the same agent capabilities as large ones — the agents adapt their behavior to context, but no agent roles, governance artifacts, or pipeline features are withheld based on project size.

### Core Collaboration Coverage (Five-Agent Baseline)

Baseline delivery coverage is provided by five core workflow roles plus the separated review pipeline:
- Business Analyst
- Investigator
- Implementor
- Test Specialist
- Dev Orchestrator
- Review pipeline roles (Code Review Orchestrator, Functional Reviewer, Technical Reviewer, Platform/Framework Reviewer)

This baseline is sufficient for most projects, including many complex tasks, when the orchestrator planning lane, spec pipeline, and review short-circuit are correctly implemented.

For very large or high-risk programs, add specialist roles only when analyzer evidence shows a coordination or quality gap that the baseline cannot cover efficiently:

| Trigger signal | Add role(s) | Why |
|---|---|---|
| Multi-epoch migration, cross-module dependency surgery, or architecture rewrite | Architect and/or Migration And Refactoring Specialist | Owns sequencing strategy, dependency-safe rollout, rollback boundaries |
| Multi-environment releases, strict release governance, or high integration risk | Release Readiness Reviewer and/or DevOps/CI-CD Specialist | Strengthens release gating, deployment safety, and integration checks |
| Security or compliance pressure materially exceeds normal reviewer capacity | Security Specialist | Adds dedicated threat, compliance, and control validation |
| Performance-critical workloads with measurable latency/cost SLOs | Performance Specialist | Adds dedicated profiling and optimization governance |

Do not add specialists by default. Additional roles must be evidence-driven, explicitly scoped, and wired into handoff contracts.

## Artifact Requirements

### Agent
- Mission, use-when, non-goals, decision rules, output contract
- Collaboration model: inputs consumed, outputs produced, hand-off criteria, auto-return vs escalation conditions
- **All agents**: structured clarification questions using `vscode_askQuestions` (what to ask, when to skip because the codebase answers), anti-patterns list, structured output contract, explicit MCP tool preference for external service access (issue trackers, project management, documentation platforms). Clarification must always use `vscode_askQuestions` — never plain-text questions that end the session. Evidence standard: every business-rule claim must be backed by code/doc evidence, user confirmation, or labeled `[ASSUMPTION]` / `[NEEDS CLARIFICATION]`.
- **All agents with handoffs**: include `handoffs:` in YAML frontmatter for explicit delegation targets with label and prompt. Example: `handoffs: [{agent: "Test Specialist", label: "Generate Tests", prompt: "Generate tests for..."}]`. This replaces implicit delegation through prose instructions.
- **Implementor**: pre-impl checklist (trace existing flow, confirm business rules, check duplication, scope affected files), code reasoning (explain business justification before writing each file), incremental implementation (verify data → business → API in chunks), verify-fix loop (build → targeted tests for touched feature/suites → lint, max 3 retries, stop and report). Verify-fix loop must treat lint warnings as failures when a linter is configured — use strict mode or equivalent flag. Build/test commands must use the analyzer-detected targets and configuration, never hardcoded values. Full test-suite runs are conditional, not default: run full suite only when risk is high (shared/core modules touched, broad dependency impact, release/CI gate, or explicit user request). For large tasks: follow the Large Task Execution Pattern (decompose → persist plan → chunked execution → intermediate validation → context management → completion). Phase -1 constitutional gates (simplicity, duplication, business logic, impact) must pass before implementation begins.
- **Code Review Orchestrator**: orchestrates a multi-stage review pipeline with short-circuit on blockers. Delegates to Functional Reviewer, Technical Reviewer, and Platform/Framework Reviewer sub-agents. Stage 0: context gathering (full file content + dependency graph + callers). Stage 1: Functional Review — business logic correctness, AC traceability, edge cases. If functional BLOCKER found, REJECT immediately without proceeding to technical review. Stage 2: Technical Review — architecture, concurrency, performance, security, layer responsibility, migration safety. Stage 3 (conditional): Platform/Framework Review — platform-specific and framework-specific checks relevant to the project's technology stack. Combined report with severity-driven verdicts.
- **Functional Reviewer**: validates code changes exclusively from business correctness perspective. AC ↔ Test ↔ Code traceability mapping. Adversarial edge-case analysis. Cross-domain data integrity checks. Evidence standard: every claim backed by code/doc anchor, user confirmation, or labeled `[ASSUMPTION]`/`[NEEDS CLARIFICATION]`. Business context confidence level (High/Medium/Low). Short-circuit: any BLOCKER stops the review pipeline.
- **Technical Reviewer**: validates code changes from technical quality perspective only. API backward compatibility checks. Database/migration safety analysis. Domain boundary violations (module boundaries, layer responsibility). NFR compliance (logging, error handling, external call protection). Performance review. Does NOT verify business requirements — that is the Functional Reviewer's job.
- **Platform/Framework Reviewer**: validates platform-specific and framework-specific concerns not covered by generic technical review. Triggered only when changed files involve platform-specific or framework-specific code. Examples: memory management and actor isolation for Swift; thread safety and lifecycle for Android; hydration and SSR for Next.js; dependency injection and bean lifecycle for Spring. The analyzer determines what platform/framework checks are relevant.
- **Investigator**: structured as-is/to-be analysis with file and line references producing a **repository impact map**: concrete file list with change descriptions, real symbol names and existing patterns to follow, dependency-ordered change groups. To-be change table (component, change type, file, business reason), impact matrix with severity levels, scenario mapping. Output must be optimized for agent legibility — structured tables and lists, not narrative prose.
- **Business-heavy bundles**: when a business domain registry, domain map, domain-scoped instructions, or business-domain skill exists, Business Analyst and Investigator maintain or refresh it; Implementor and Code Reviewer must consult it before changing or approving business logic; Dev Orchestrator includes it in hand-off requirements.
- **Orchestrator**: intent-based auto-routing to sub-agents so users never manually pick agents, mandatory confirmation checkpoint between investigation and implementation, structured completion report, micro-change lane for low-risk edits, reviewer conflict resolution, inter-agent iteration loops (implement → test → review → back to implement until review passes). Planning lane for complex tasks (>10 files, >3 modules, or migration): decompose → persist plan → `manage_todo_list` → sequential execution with intermediate validation. Single-session rule: complete entire delegated workflow in one session, use `vscode_askQuestions` when user input needed, fix and retry sub-agent failures in-session. Clarification: never end workflow after a prompt alone; use `vscode_askQuestions` with recommended default and continue provisionally. Harness awareness: track recurring failure patterns across tasks and flag when the harness (instructions, conventions, linter rules) should be improved. Context management: persist progress to session memory after each major phase, use `manage_todo_list` for visible tracking, compact context when conversation grows large, read progress notes at start of each phase.

### YAML Frontmatter Generation
- `agents` field MUST use inline JSON-style array syntax with exact agent display names: `agents: ["Name A", "Name B"]` — NEVER use block list syntax (`- item`) and NEVER use filenames
- `description` field MUST be a double-quoted string with concrete trigger phrases
- `name` field MUST be an unquoted string matching the intended display name
- Prompt files MUST use `agent` field (not `mode`) for routing to a specific agent: `agent: "Agent Display Name"`
- Only emit frontmatter keys listed in the Supported Frontmatter Keys table in `copilot-docs-registry.md`. Any key not listed there will cause editor diagnostics or be silently ignored.
- Do not emit `tools` or `mcp-servers` unless explicitly requested
- All generated files in the same bundle MUST use identical YAML formatting conventions

### Skill
- Repeatable workflow with decision criteria and validation checks
- State which agents use it (bidirectional linking mandatory)
- Delivery workflow skill is always mandatory minimum for full kits
- Create domain-specific skills (testing, investigation, review) when they serve multiple agents
- Encode specific workflow steps, decision trees, and validation checklists — not generic advice

**Domain knowledge placement decision** — when the analyzer finds domain knowledge for a technology area, place it as follows:

| Signal | Where to put the knowledge |
|--------|---------------------------|
| Domain is heavily used in the project AND multiple agents need it | Create a dedicated domain skill |
| Domain is used in the project but only one agent needs it | Embed directly in that agent's instructions |
| Domain knowledge is a small set of conventions (< 10 rules) | Embed in the relevant instruction file (`applyTo` the matching path pattern) |
| Domain is lightly used or the project barely touches it | Skip — do not create a skill or bloat instructions for thin signal |
| Domain signal is thin or unknown | Prefer omission or an explicit uncertainty note over prescriptive guidance |

Do not generate one skill per detected technology area. Create a domain skill only when it earns its place through multi-agent reuse and strong project signal from the analyzer.

### Business Knowledge Persistence
- Always capture the minimum shared business context in the project context instruction: domain glossary, key business rules, lifecycle states, and invariants.
- For projects with richer business complexity, choose the lightest primitive that preserves shared understanding:
	- project context instruction only: small apps or products whose business rules fit in a concise summary
	- domain-scoped instructions: business rules that map cleanly to specific paths or modules
	- reusable workflow asset or domain map: multiple domains, lifecycle-heavy workflows, or cross-domain dependencies that several agents must reference
	- business-domain skill: only when multiple agents reuse the same repeatable business-analysis workflow or interpretation process
- If a bundle includes a business domain registry, domain map, domain-scoped instructions, or a business-domain skill, Business Analyst, Investigator, Implementor, Code Reviewer, and Dev Orchestrator must reference it explicitly in their collaboration inputs or decision rules.
- Do not generate a dedicated business-domain artifact when the project's business context fits cleanly in the project context instruction and the normal planning/investigation assets.
- Do not add a dedicated kit subagent for business-domain modeling by default. The analyzer extracts business context, and the generator decides how to persist it. Add an extra specialization only when business-domain synthesis becomes a distinct workflow with materially different failure modes.

### Instruction
- Narrow `applyTo` scope, single convention domain
- Separate files for distinct domains (implementation, testing, UI, data layer)
- Avoid duplicating the entire skill body

### Prompt
- Short, discoverable, route to the right agent
- At least 2: primary delivery + secondary entry point
- Make the default workflow lane obvious
- Frontmatter MUST use `agent` field (not `mode`) for routing to a specific agent

### Hook
- Only when deterministic enforcement is truly needed and safe
- Validate against `hook-checklist.md` first

## Generation Principles

Non-negotiable principles every generated agent must encode. These are the behavioral floor for all generated agents, regardless of role.

1. **Understand before changing** — Trace existing code paths, data flow, and callers before modifying anything. Never assume; verify.
2. **Confirm business logic** — Identify business rules before writing code. Ask when rules are ambiguous, not after the implementation is wrong.
3. **No duplicate validation across layers** — Check for existing validation before adding new checks. Each rule enforced in exactly one layer.
4. **Respect module boundaries** — Do not reach across architectural boundaries. Use established interfaces and dependency patterns.
5. **Clarify before acting on ambiguity** — When intent or requirements are unclear, use `vscode_askQuestions` to present structured options with a recommended default. Never guess silently, and never write questions as plain text that ends the session — `vscode_askQuestions` keeps the workflow running.
6. **Verify before claiming completion** — Run the project's actual build, test, and lint commands. Do not claim success without evidence.
7. **Prefer simplicity** — Choose the simplest correct solution. Avoid premature abstraction, unnecessary indirection, or speculative generalization.
8. **Explain decisions and report outcomes** — State what was done, why, and what changed. Include evidence of verification in completion reports.

The generator must embed these principles in every generated agent's instructions. The auditor must verify their presence.

## Harness Engineering Alignment

Generated agents must follow harness engineering principles — designing the environment for reliable agent execution, not just writing instructions.

### Feedforward and Feedback Controls

Every generated agent ecosystem should distinguish two control types:

- **Feedforward (Guides)**: Context provided *before* the agent acts to increase the probability of correct first output. Examples: architecture docs, coding conventions in instructions, implementation notes with real file paths and symbol names, structured task templates.
- **Feedback (Sensors)**: Checks that run *after* the agent acts to enable self-correction. Examples: build commands, test suites, linters, type checkers, AI code review.

Within each type, distinguish:
- **Computational controls**: Deterministic, fast, reliable — linters, type checkers, tests, structural analysis. Run on every change.
- **Inferential controls**: Semantic, slower, non-deterministic — AI code review, LLM-as-judge. Run selectively (e.g., PR review, complex changes).

Generated verify-fix loops are feedback sensors. Generated instructions and skills are feedforward guides. The analyzer should assess the project's existing computational and inferential controls so generated agents leverage them.

### Structured Investigation Output (Repository Impact Map)

The Investigator's output must function as a **repository impact map** — grounded in actual code, not abstract analysis:
- List every file to be modified with specific change descriptions
- Reference real symbol names, function signatures, and existing patterns to follow
- Group changes by module/domain with dependency ordering
- Include human confirmation checkpoint before implementation begins
- The Orchestrator must not proceed to implementation until the impact map is reviewed

### Execution Plans as Persistent Artifacts

For complex or multi-session work, generated agents must persist execution plans as files rather than keeping them only in-session:
- Use session memory files (`/memories/session/`) for investigation findings, migration plans, and progress logs
- Execution plans should include: goal, current phase, completed steps, remaining steps, blocked items, key decisions made
- Plans are first-class artifacts — versioned, structured, and co-located with the work
- Agents must read existing plans at the start of work and update them as progress is made

### Agent Legibility

Generated agent outputs must be optimized for downstream consumption by other agents (not just humans):
- Investigation reports must be structured with clear sections, file references, and machine-parseable change tables — not narrative prose
- Hand-off documents must use consistent formats that downstream agents can parse reliably
- Completion reports must include structured evidence (commands run, results, files changed) not just summary text
- Prefer tabular and list formats over paragraph-form explanations for inter-agent communication

### Steering Loop

Generated agent ecosystems should include guidance for improving the harness over time:
- When an issue recurs across multiple tasks, the fix should target the harness (instructions, conventions, linter rules) — not just the output
- Generated bundle evolution guidance must include: "When you find yourself correcting the same agent behavior repeatedly, extract the correction into an instruction file or promote it into a linting rule"
- The orchestrator should track recurring failure patterns and flag them for harness improvement

### Entropy Management

Generated orchestrator agents should include entropy management for long-lived codebases:
- Periodic drift detection: agents referencing removed files, outdated conventions, or abandoned patterns
- Recurring cleanup patterns: identify dead code, stale docs, inconsistent naming
- Quality tracking: flag when patterns degrade across multiple changes
- The orchestrator's completion report should include a brief "codebase health" section noting any drift signals observed

## Large Task Execution Pattern

For complex, multi-step tasks (large migrations, major refactors, cross-module changes), generated orchestrator and implementor agents must follow this pattern:

### 1. Decomposition
- Break the task into ordered phases based on dependency analysis
- Each phase must be independently verifiable (build + tests pass after each phase)
- Identify phase dependencies — which phases must complete before others can start
- Estimate scope per phase (files, modules, risk level)

### 2. Planning Persistence
- Write the decomposed plan to a session memory file before starting execution
- Plan format: phase list with status (not-started / in-progress / completed / blocked), file targets, validation criteria
- Use `manage_todo_list` to track phases as visible progress indicators

### 3. Chunked Execution
- Execute one phase at a time — never attempt the entire migration in a single pass
- After each phase: validate (build → test → lint), update plan status, compact context if needed
- If a phase fails validation, fix within that phase before proceeding

### 4. Intermediate Validation
- After each phase, verify the codebase is in a correct intermediate state
- Run targeted tests for affected modules, not full suite (unless risk warrants it)
- Document what changed and what remains in the plan file

### 5. Context Management for Long Tasks
- When context is growing large, create a progress summary in session memory: what's done, what's next, key decisions
- Read the progress summary at the start of each phase to re-ground context
- Compact investigation findings into structured notes rather than keeping full exploration history
- Use `manage_todo_list` for visible progress tracking throughout

### 6. Completion
- Final validation: full build + full test suite + lint
- Structured completion report with: phases completed, files changed per phase, validation evidence, any remaining risks
- Clean up intermediate session memory files

### Context Persistence Thresholds
- **Investigation findings**: When investigation reveals >5 files or >3 modules affected, save structured findings to session memory before starting implementation
- **Multi-step plans**: Any task with >3 discrete implementation steps should have a persisted plan
- **Long-running tasks**: When a task involves >20 file changes or crosses module boundaries, create a progress checkpoint after each major phase
- **Key decisions**: When a non-obvious architectural or implementation decision is made, record the decision and rationale in session memory
- **Format**: Structured markdown with clear headings, file references, and status indicators. One file per concern (investigation-notes.md, migration-plan.md, progress-log.md).
- **Compaction**: Summarize completed phases into compact progress notes; subsequent work reads notes instead of relying on full conversation history.

The auditor must verify that generated orchestrator agents include this pattern for complex tasks.

## Context Optimization Rules

Rules for efficient context usage in generated agents and artifacts.

### Signal-to-Noise Discipline
- Generated agents should produce concise, phase-bounded outputs — not restate upstream context
- Hand-offs between agents prefer delta summaries with file and line references over repeated full-context prose
- Static rules belong in instructions and skills (loaded once), not duplicated across every agent's instructions

### Context Quality Framework
When deciding what context to include in generated artifacts, apply this signal/noise/cost assessment:

| Context type | Signal | Cost | Action |
|---|---|---|---|
| Stack trace / error (short) | High | Low | Paste directly in prompt |
| Architecture doc (long) | Medium | High | Mention path or excerpt relevant section |
| Many "possibly related" files | Low | High | Provide 1-2 anchors, let agent research |
| Test/build command | High | Low | Paste directly |
| Convention repeated every task | High | Medium | Move into instruction file |

Quick rule for generated bundles:
- Signal high + cost low → include immediately
- Signal high + cost high → excerpt or give path
- Signal low + cost high → usually omit

Generated user playbooks should teach this framework. Generated agents should follow it in their hand-off outputs.

### Copilot Runtime Awareness
Generated bundles must be designed with awareness of the Copilot runtime execution model. The authoritative reference is the Copilot Runtime Model section in `copilot-docs-registry.md`. Key constraints that affect generated agent design:

- **Tool result timing**: Results from round N appear in round N+1, not the same round. Multi-step tool workflows must account for this.
- **Tool-calling gate**: Tools must be exposed by the runtime before the model can use them. No exposed tools = no tool calls.
- **File classification**: Only Group B files (copilot-instructions, instructions, agents, prompts, skills) are auto-injected into prompts. Group C files (constitution, docs, templates) are pull-resources loaded on demand.
- **Compaction**: Long threads are automatically summarized. Generated agents should trust compaction and keep threads aligned by subsystem.
- **Hook events**: The authoritative hook event list is in `copilot-docs-registry.md`. Generated hook guidance must reference that list, not invent events.

### Three-Layer Context Model
Generated bundles should distribute context efficiently across three layers (plus a workspace-level foundation):

**Foundation**: `copilot-instructions.md` — Workspace-level instructions automatically loaded by Copilot for all interactions. Concise project overview, technology stack, core conventions, agent ecosystem guide (available agents, prompt entry points, how to invoke). Target 40-80 lines. This is the entry point for anyone using Copilot in the project.

1. **Project context instruction** (`<prefix>-project-context.instructions.md`, `applyTo: "**"`) — Detailed project facts: architecture, extended conventions, domain glossary, bundle evolution guidance. Supplements `copilot-instructions.md` with depth. Keep concise but thorough.
2. **Path-scoped instructions** — Narrow, file-pattern-scoped rules. Loaded only when matching files are active. Keep single-purpose.
3. **Agent instructions** — Role-specific workflows, decision rules, and output contracts. Loaded only when the agent is invoked. Do not repeat what instructions or skills already cover.

Do not duplicate content between `copilot-instructions.md` and the project context instruction — the workspace-level file is the brief overview and agent guide, the project context instruction is the deep reference.

### Context Budget Guidance for Generated Project Context Instruction
- Target length: 80-150 lines for typical projects. Exceed only when genuine complexity demands it.
- Include: project overview, architecture summary, technology stack, key conventions, domain glossary, quality expectations.
- Exclude: role-specific workflows (belongs in agents), file-pattern rules (belongs in path-scoped instructions), repeatable processes (belongs in skills).
- Every line must earn its place — if a fact only matters for one role, put it in that agent's instructions instead.

## Bundle Evolution and Drift Detection

The generated project context instruction should include a section guiding post-generation maintenance and drift detection.

### Evolution Triggers
- **When to update agents**: After major architecture changes, new module additions, framework migrations, or when agents produce consistently wrong outputs.
- **When to promote patterns**: If you find yourself correcting the same agent behavior repeatedly, extract the correction into an instruction file with a narrow `applyTo` scope. This is the **steering loop** — improve the harness (feedforward controls), not just individual outputs.
- **When to add instructions**: When a new convention emerges that applies to specific file patterns.
- **When to promote to mechanical enforcement**: When an instruction is violated repeatedly despite being documented, consider promoting the rule to a computational control (linter rule, structural test, pre-commit hook).

### Five Drift Dimensions
1. **File references**: Agents reference files/modules that have been renamed, moved, or deleted
2. **Convention drift**: Agents enforce conventions the team has abandoned or changed
3. **API pattern drift**: Agents suggest patterns using deprecated or removed APIs
4. **Architecture drift**: Agents assume architecture that has been restructured
5. **Ecosystem drift**: Agent-to-agent references are broken (renamed/removed agents)

### Detection Triggers
- After major refactors or module restructuring
- After dependency version upgrades
- After team convention changes
- Quarterly review cadence

### Entropy Management
- Periodically review agent outputs for pattern degradation: growing duplication, inconsistent naming, architectural boundary violations
- Address by improving feedforward controls, not just fixing individual instances
- Generated orchestrators should flag suspected drift when they encounter stale references

The generator must include this guidance in every generated project context instruction. The auditor checks for drift signals during ecosystem audit.

## Team Operating Model

Generated bundles should include guidance for how the team evolves the agent ecosystem over time. This prevents the common failure mode where initial generation is high-quality but the bundle degrades through ad-hoc edits.

### Maturity Model

Generated project context instructions should reference this progression so teams understand where they are and what to aim for:

| Level | Description | What changes |
|---|---|---|
| L1 — Ad-hoc prompts | Team re-explains context in chat | Results vary by prompting skill |
| L2 — Repo instructions | `copilot-instructions.md` + scoped `.instructions.md` exist | Consistency improves |
| L3 — Common docs | Overview, glossary, architecture map, runbook exist | Investigation gets faster and safer |
| L4 — Skills and agents | Repeated workflows are encoded | Copilot becomes reusable across tasks |
| L5 — Verification-first | Reproducible checks and CI-backed validation exist | Try-verify-refine loops become reliable |

### Knowledge Promotion Flow

Teams should promote repeated patterns into durable artifacts instead of re-explaining in prompts:

| What keeps recurring | Promote to |
|---|---|
| Same conventions repeated in prompts | `.instructions.md` file with narrow `applyTo` |
| Same workflow repeated across tasks | Skill file |
| Same clarification gaps | Shared doc or template |
| Same review findings | Path-scoped instruction (see Review Memory Promotion) |
| Same business rules explained | Project context instruction or domain glossary |

### Agent-Friendly Repository Checklist

Generated project context instructions should include this checklist as a maintenance guide:

1. Concise `copilot-instructions.md` with ecosystem guide
2. Clear repo overview accessible to agents
3. Verification runbook with actual build/test/lint commands
4. Source-of-truth map for architecture and boundaries
5. Business glossary for domain-heavy repos
6. Common failure-mode guidance for repeated regressions
7. Skills and prompts for repeated workflows
8. Consistent naming and directory structure

## Constitution Pattern

Generated bundles must include a `<prefix>-constitution.md` instruction file (`applyTo: "**"`) that defines immutable governance rules for the project. The constitution is the highest-authority document in the generated bundle — it overrides any agent-specific instruction when they conflict.

### Structure
1. **Preamble** — Bundle identity and purpose statement
2. **Article I: Scope & Boundaries** — What the bundle covers and what it does not
3. **Article II: Evidence Standard** — Every business-rule claim must be backed by code/doc evidence, user confirmation, or labeled `[ASSUMPTION]` / `[NEEDS CLARIFICATION]`. No unanchored assertions.
4. **Article III: Review Pipeline** — Multi-stage review process requirements, short-circuit rules, verdict authority
5. **Article IV: Change Governance** — Blast-radius assessment rules, mandatory checkpoints for high-impact changes
6. **Article V: Specification Discipline** — Spec-driven pipeline requirements for non-trivial features
7. **Article VI: Context Persistence** — Session memory usage rules, progress tracking requirements
8. **Article VII: Escalation** — When and how to escalate to human decision-making
9. **Article VIII: Verify Before Claiming Completion** — Conditional verification (build/test/lint when runnable), retry up to 3 times, explicit explanation when verification unavailable
10. **Article IX: Prefer Simplicity and Avoid Unnecessary Abstraction** — Simplest correct solution, no speculative abstractions, no one-off wrappers
11. **Phase -1 Gates** — Constitutional gates that MUST pass before implementation begins:
   - **Simplicity Gate**: Is this the simplest approach that satisfies the requirement?
   - **Duplication Gate**: Does this duplicate existing logic? Can existing code be reused?
   - **Business Logic Gate**: Are business rules verified against source (code, docs, domain expert)?
   - **Impact Gate**: Is the blast radius understood and acceptable?

### Generation Rules
- The generator produces the constitution from project analysis — not a generic template
- Constitution articles reference actual project conventions, not placeholder guidance
- The constitution is an instruction file, not an agent — it has no workflow, just rules
- All generated agents must include a note acknowledging the constitution
- The auditor must verify constitution presence and that agents reference it

## Spec-Driven Pipeline

Generated bundles must include a spec-driven pipeline that normalizes feature work through structured specification before implementation begins.

### Pipeline Stages

1. **Refine User Input** — Normalize raw user requests into structured goal/anchor/constraints format. Validate completeness, identify ambiguity, and extract acceptance criteria. This prevents routing errors and wasted implementation cycles.
2. **Specify Feature** — Produce a feature specification (PRD) stored in `specs/<feature-id>/spec.md`. Sections: Problem Statement, Scope and Non-Goals, Acceptance Criteria (testable), Domain Rules, Edge Cases, Dependencies, Technical Constraints. The spec is the contract between planning and implementation.
3. **Plan Implementation** — Given a spec, produce an implementation plan stored in `specs/<feature-id>/plan.md`. Sections: Architecture Approach, File Changes (with dependency order), Risk Assessment, Test Strategy, Rollback Plan. The plan is reviewed before implementation begins.
4. **Generate Tasks** — Given a plan, produce ordered task breakdowns stored in `specs/<feature-id>/tasks.md`. Each task: description, files, validation criteria, estimated complexity, dependency on prior tasks. Tasks feed directly into `manage_todo_list` for execution tracking.

### Spec Workspace
- Feature specs live in `specs/<feature-id>/` directory
- Each feature gets: `spec.md`, `plan.md`, `tasks.md`
- Specs are living documents — updated as implementation reveals new constraints
- Closed specs can be archived or deleted after merge

### When to Activate
- **Always**: for features that touch >3 files, cross module boundaries, change business logic, or affect shared/core code
- **Skip**: for trivial changes (typos, small config edits, single-file fixes) where direct implementation is faster
- The orchestrator decides activation based on the task's complexity assessment

### Generated Assets
- **Refine-User-Input skill**: intake normalizer that structures raw requests
- **Specify-Feature skill**: PRD generation workflow with templates
- **Plan-Implementation skill**: architecture planning with risk assessment
- **Generate-Tasks skill**: task breakdown for execution tracking
- Templates for spec, plan, and tasks (see `spec-template.md`, `plan-template.md`, `tasks-template.md`)

## Separated Review Pipeline

Generated bundles must include a multi-stage review pipeline replacing the single Code Reviewer.

### Pipeline Structure

| Stage | Agent | Focus | Short-Circuit |
|-------|-------|-------|---------------|
| 0 | Code Review Orchestrator | Context gathering, route to reviewers | — |
| 1 | Functional Reviewer | Business correctness, AC traceability | BLOCKER → REJECT immediately |
| 2 | Technical Reviewer | Architecture, performance, security | — |
| 3 | Platform/Framework Reviewer (conditional) | Platform-specific and framework-specific checks | Only when relevant platform/framework files changed |

### Short-Circuit Rule
The Functional Reviewer runs first. If any **BLOCKER** severity finding is raised (broken business logic, AC violation, data integrity issue), the review pipeline **REJECT**s immediately — Technical and Platform/Framework reviews do not run. This prevents wasting review cycles on code that is fundamentally wrong from a business perspective.

### Evidence Standard in Reviews
Every review finding must include:
- **Code anchor**: file path and line reference to the exact issue
- **Evidence type**: code-backed, spec-backed, user-confirmed, `[ASSUMPTION]`, or `[NEEDS CLARIFICATION]`
- **Severity**: blocker / major / minor / suggestion
- **Fix suggestion**: concrete code-level recommendation

### When to Generate Separated Review
- Always generate the full 4-agent pipeline (Code Review Orchestrator + Functional Reviewer + Technical Reviewer + Platform/Framework Reviewer)
- Platform/Framework Reviewer is conditionally triggered — only runs when changed files include platform-specific or framework-specific code

## Handoffs Pattern

Generated agents must declare explicit delegation targets in YAML frontmatter using the `handoffs` field. This replaces implicit delegation through prose instructions and enables Copilot to offer delegation buttons in the UI.

### Frontmatter Format
```yaml
handoffs:
  - agent: "Test Specialist"
    label: "Generate Tests"
    prompt: "Generate unit tests for the implementation I just completed"
  - agent: "Code Review Orchestrator"
    label: "Review Changes"
    prompt: "Review the changes I made for business correctness and technical quality"
```

### Rules
- Every agent that delegates to other agents MUST declare handoffs
- Orchestrators have handoffs to all agents they can route to
- Specialist agents have handoffs back to the orchestrator (for escalation/completion)
- Handoff prompts should be specific enough to provide context for the receiving agent
- `label` is the user-facing button text — keep it short and action-oriented
- `agent` must be the exact display name (same as used in `agents` frontmatter)
- Handoffs supplement `agents` frontmatter — both should be present

## Evidence Standard

All generated agents must enforce a universal evidence standard for claims, findings, and recommendations:

| Label | Meaning | When to use |
|-------|---------|-------------|
| (no label) | Code/doc-backed | Default — claim verified against actual code or documentation |
| `[USER-CONFIRMED]` | Human-verified | User explicitly confirmed this fact via `vscode_askQuestions` |
| `[ASSUMPTION]` | Unverified belief | Claim based on reasonable inference but not confirmed by code, docs, or user |
| `[NEEDS CLARIFICATION]` | Ambiguous/unknown | Cannot determine truth — must ask user or investigate further before proceeding |

### Enforcement Rules
- Investigators mark uncertain findings as `[ASSUMPTION]` — implementors must verify before coding
- Business Analysts mark unconfirmed domain rules as `[NEEDS CLARIFICATION]`
- Code Reviewers must challenge any `[ASSUMPTION]` that reaches review stage without verification
- Orchestrators track assumption resolution — escalate unresolved assumptions before proceeding
- The constitution Article II codifies this standard for the project

## Runtime Docs Generation

Generated bundles must include essential documentation files that help users and maintainers operate the agent ecosystem effectively.

### Generation Rules
Use `user-playbook-template.md` and `review-playbook-template.md` from `.github/templates/agent-builder/` as scaffolds for generated playbooks.

### User Playbook (`<prefix>-user-playbook.md`)
- How to invoke agents and use prompts
- Common workflows with example prompts
- When to use which agent
- Prompt shape guidance: every substantial prompt should include Goal / Anchor / Constraints / Verify
- Task-specific prompt templates: bug fix, feature, investigation, refactor, review
- Thread strategy: one thread per feature or subsystem, follow up in same thread while topic persists
- When to attach content vs mention path (paste short errors/ACs/commands; mention path for long files the agent can read)
- Pre-prompt checklist: outcome clear? anchor present? constraints visible? verify step defined?
- Anti-patterns: dumping many files without anchor, vague goals, mixing investigate+implement+review in one prompt
- Troubleshooting: reference the Maintainer Debug Recipe from `copilot-docs-registry.md` (prompt profiler → agent debug log → chat debug view → OTEL)

### Review Playbook (`<prefix>-review-playbook.md`)
- How the review pipeline works (stages, short-circuit rules)
- What each reviewer checks
- How to interpret review verdicts and severity levels
- Blast-radius review: when to request additional review for high-impact changes
- How to override or escalate review findings
- Review complexity model: treat review size as a complexity problem, not just diff size

#### Review Complexity Model
Generated review playbooks must classify reviews by four dimensions, not just diff size:

| Dimension | What to assess |
|---|---|
| Diff size | file count, changed LOC, generated churn |
| Blast radius | callers, dependents, downstream consumers, cross-service contracts |
| Business criticality | money, auth, compliance, state transitions, cross-domain writes |
| Context confidence | requirement quality, business docs, tests, stable callers |

A 1-2 file change can still be high-complexity if it has large blast radius or touches business-critical paths. Generated orchestrators should classify review complexity before routing to the review pipeline, and plan review scope for non-trivial changes.

#### Review Scope Planning
For high-complexity reviews, generated bundles should include a review scope planning step:
1. Run scope planning before deep review
2. Identify highest-risk surfaces and load order
3. Build a functional scenario pack (happy path, invalid path, boundary, state-transition, cross-domain side-effect, regression-sensitive)
4. State missing anchors and clarification needs explicitly
5. Execute review by slices in planned order

### Generation Rules
- Playbooks reference actual generated agent names, not generic placeholders
- Content is derived from the actual bundle — not a static template
- User playbook is the primary onboarding doc for new team members
- Review playbook explains the separated review pipeline behavior

## Review Memory Promotion

Generated bundles must include a learning loop that promotes recurring review findings into durable prevention rules.

### Promotion Flow
1. **Detect pattern**: Code Reviewer or Functional Reviewer flags the same issue type ≥3 times
2. **Propose rule**: Draft an instruction-level rule or checklist item to prevent recurrence
3. **Validate**: Check if the rule is actionable, specific, and not already covered
4. **Promote**: Add to the relevant instruction file (path-scoped or global)
5. **Verify**: Confirm subsequent reviews no longer find the same pattern

### Where to Promote
- Convention violations → path-scoped instruction with `applyTo` for affected file patterns
- Repeated test gaps → test specialist's testing instruction
- Architecture boundary violations → project context instruction
- If violations persist after instruction promotion → escalate to mechanical enforcement (linter rule, hook)

### Generation Rules
- Generated orchestrators include a note to track review patterns
- Generated project context instruction mentions promotion as part of bundle evolution

## Hooks Generation

When the analyzer detects linting or formatting tools in the project, the generator should produce hook guidance or actual hook configurations.

### Rules
- Only generate hooks when the corresponding tool is already configured in the project
- Hook files go in `.github/hooks/` or are documented in `copilot-instructions.md`
- Always include a comment explaining what the hook does and when it fires
- Hooks are deterministic enforcement — they must never produce false positives
- Generate hooks when the corresponding tools are detected; document the recommendation when not generating
- The authoritative list of supported hook events is in `copilot-docs-registry.md` (Official Hook Events section). Do not reference events not listed there.
- Use `postToolUse` with tool filtering for expensive quality checks so they run only after relevant edit/write tools
- `preCompact` hooks must be fast (<10s) — they block compaction and degrade responsiveness

## Generated File Marking

Every file generated by the kit must include a marker comment immediately after the YAML frontmatter closing `---` to identify it as kit-generated and support maintenance:

```
---
name: example-agent
description: "..."
---
<!-- Generated by Agent Builder Kit -->
```

### Rules
- The marker is placed on the first line after the YAML frontmatter closing `---` — never before the frontmatter opening `---`
- Placing the marker before frontmatter breaks YAML parsing and causes editor diagnostics
- The marker enables users, tools, and the kit itself to distinguish kit-generated files from manually authored ones
- When refreshing or updating generated files, the marker is preserved as-is
- The kit recognizes `<!-- Generated by Agent Builder Kit -->` as the canonical marker pattern for maintenance operations
- The auditor must verify marker presence and correct placement (after frontmatter) in all generated files
- Template files within the kit itself (`.github/templates/`) do not get markers — only files generated for target projects

## Cross-Session Persistence

For tasks that may exceed a single session's context window (full app rewrites, major version migrations, large-scale refactors), generated agents must include cross-session persistence guidance:

### When to Use Cross-Session Persistence
- Task scope exceeds ~50 file changes or spans >5 modules
- Migration work that requires multiple phases over days/weeks
- Architecture-level changes that cannot be validated incrementally in one session

### How to Persist Across Sessions
- Use repository memory (`/memories/repo/`) for durable task state that survives across sessions — migration progress, phase status, key decisions, remaining work
- Use persistent files in the project (e.g., `specs/<task-id>/progress.md`) for structured migration plans and phase tracking
- Session memory (`/memories/session/`) is for within-session notes only — it does not survive across sessions
- At the end of each session, write a structured progress summary to repo memory or project files with: completed phases, current phase status, remaining phases, key decisions, blockers
- At the start of each new session, read the progress summary to re-ground context before continuing

### Plan Format for Cross-Session Work
```
# Migration Progress: {task-id}
## Status: {phase N of M}
## Completed Phases
- Phase 1: {description} — {date} — {evidence}
## Current Phase
- Phase N: {description} — {status} — {blockers}
## Remaining Phases
- Phase N+1: {description}
## Key Decisions
- {decision}: {rationale}
## Blockers
- {blocker}: {status}
```

## Anti-Patterns

- Vague descriptions
- `applyTo: "**"` without strong reason
- Skills that are only generic advice
- Agents duplicating prompt/instruction content
- Hooks for convenience rather than safety
- Under-building a workflow kit when fuller coverage would help
- Technology-specific bundle that reads like generic guidance
- Assuming latest language/framework defaults when the project uses an older or different stack
- Merging analysis, generation, and audit when each has distinct failure modes

## Final Output Contract

- Chosen architecture and why
- Created or changed files
- Validation results
- Remaining risks
- Audit outcome
