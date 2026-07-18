---
name: roadmap
description: Scan task pipeline health, build or update the project roadmap, and maintain a priority task queue
type: planning
version: v0.14
required_conventions: [alignment-page]
argument-hint: "[--existing] [path-to-spec]"
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Roadmap - Task Pipeline Manager

Use this skill to keep the task execution pipeline healthy and moving. It scans roadmap, todo, manual tasks, record tasks, recurring tasks, history, ideas, specs, and git state, then either builds a roadmap (when none exists) or updates `tasks/todo.md` with a priority task queue.

Do not run the queued skills from this workflow. The job here is to maintain the task queue so the user can resolve all pipeline issues in the right order.

## Process

### 1. Resolve Project Context

1. Read `.agents/project.json` if it exists.
2. Use `project_type` and `enabled_packs` to decide which project-pack skills apply.
3. If `.agents/project.json` is missing, infer the project type from repository signals:
   - game: game engine files, Steam/store assets, playable prototypes, or game-specific README/spec language
   - devtool: SDK, CLI, API, library, infra, docs, examples, or package-first developer workflow
   - business-app: SaaS, marketplace, productivity, workflow, enterprise, or user-facing app
4. If the project type cannot be inferred, default to `business-app`.
5. Read `CLAUDE.md` for project conventions.
6. Read `README.md` or equivalent for project overview.

### 2. Scan Pipeline State

Record existence, content summary, and last-modified timestamps for:

- `tasks/roadmap.md` — full phased plan
- `tasks/todo.md` — current phase working document
- `tasks/todo.md` § `Priority Documentation Todo` — current documentation queue and whether it has unchecked items
- `tasks/manual-todo.md` — pending manual tasks
- `tasks/record-todo.md` — non-blocking condition-gated records and measurements
- `tasks/recurring-todo.md` — cadence-based operational, research, or maintenance tasks
- `tasks/history.md` — completed work log
- `tasks/ideas.md` — unspecced ideas
- `tasks/phases/` — archived phase files
- `tasks/lessons.md` — accumulated lessons
- `specs/` or `spec.md` — specifications
- `specs/user-flow-*.md` — screen-flow maps for user-facing work
- `specs/ui-requirements-*.md` — optional requirements-only UI content contracts for explicit layout-mode work
- `specs/ux-variations-*.md` — UX variation plans for user-facing work
- `specs/ui-*.md` — implementation-ready UI specifications for user-facing work
- `research/journey-map.md` — user/customer journey context for user-facing work

Also gather:

- Git log (last 20 commits) for recent activity
- Working tree status (uncommitted changes, unpushed commits)

### 3. Determine Project State

Route behavior based on the current pipeline state:

| State | Condition | Behavior |
|-------|-----------|----------|
| A0 — No specs, missing journey | User-facing business-app work has no specs and no `research/journey-map.md` | Queue `/journey-map` (customer-lifecycle pack). Done (skip to step 7). |
| A — No specs | No `specs/` files, no `spec.md`, and journey is complete or not applicable | Queue `/feature-interview` (product-design pack) when an idea/research gap exists and the planning destination is not confirmed; queue `/spec-interview` (product-design pack) only when the user already selected full-spec creation. Done (skip to step 7). |
| B0 — Specs, missing design gate | User-facing specs exist, but `research/journey-map.md`, `specs/user-flow-*.md`, `specs/ux-variations-*.md`, `specs/ui-*.md`, consolidated prototype at `prototypes/*/consolidated/`, or production spec is missing | Queue the missing planning item. Done (skip to step 7). |
| B — Specs, no roadmap | Specs exist and required journey/flow/UX-variation/UI planning is complete or not applicable, `tasks/roadmap.md` missing or empty | Go to step 4 (build roadmap), then continue to step 5. |
| C — Work in progress | `tasks/roadmap.md` exists, unchecked phases remain | Skip to step 5 (classify issues). |
| G — Roadmap extension needed | `tasks/roadmap.md` exists, all phases are checked, and a substantive spec exists that is newer than the roadmap or is not represented in any completed phase | Go to step 4 in extension mode: interview only for the new/changed spec scope, append the agreed next phase(s), then seed the first new phase with `/plan-phase N`. Do not queue `/roadmap`. |
| D — All complete, documentation scan needed | All phases in `tasks/roadmap.md` are checked and `tasks/todo.md` has no current `## Priority Documentation Todo` section from a previous `/research-roadmap` (research-admin pack) run | Queue `/research-roadmap` (research-admin pack) for documentation scan. Done (skip to step 7). |
| E — All complete, documentation queue active | All phases in `tasks/roadmap.md` are checked and `tasks/todo.md` has an unchecked `## Priority Documentation Todo` item | Preserve the existing documentation queue and recommend the first unchecked documentation item. Done (skip to step 8; do not add another `/research-roadmap` (research-admin pack) task). |
| F — All complete, documentation current | All phases in `tasks/roadmap.md` are checked and `tasks/todo.md` § `Priority Documentation Todo` says documentation is current with no unchecked documentation items | Report that implementation phases and documentation scan are complete; do not queue `/research-roadmap` (research-admin pack) again. Done (skip to step 8). |

### 4. Build or Extend Roadmap (States B and G)

When specs exist but no roadmap does, interview the user to build one. When State G applies, interview only on the new or changed spec scope needed to extend the existing roadmap; preserve completed phases and append the agreed next phase(s).

#### 4a. Synthesize and Present

Present the user with a structured summary:

- List each spec section / feature area identified
- Note dependencies between them
- Highlight any conflicts or overlaps between specs
- Flag specs that seem incomplete or ambiguous

#### 4b. Interview on Strategy

Use the AskUserQuestion tool to align on roadmap decisions. Ask one to three focused questions per turn. Cover:

- **Priority**: Which features/specs are most important? What's MVP vs. later?
- **Grouping**: Should any specs be combined into a single phase? Split apart?
- **Sequencing**: What depends on what? What should ship first for user value or risk reduction?
- **Scope**: Should anything be deferred, dropped, or marked as stretch?
- **Market fit** (when ICP/gap specs exist): Which phases directly address customer pain points or deal-blockers from gap analysis? Prioritise these unless technically impossible. Surface tension between technical sequencing and market urgency.
- **Phase sizing**: Preference for many small phases vs. fewer larger ones?
- **Manual tasks**: Are there human-only external prerequisites (DNS/account setup, OAuth app creation, billing/approval, real-device or production browser verification with subjective sign-off)? Which phases do they block or follow? Do not classify repo edits, SDK wiring, CLI/API work, local tests, or audits as manual.
- **Parallelization**: Which phase work can run independently, which modules or files are shared chokepoints, and where should work stay serial?
- **Review needs**: Which phases need specialized review gates (correctness, tests, security, performance, docs/API conformance, UX)?
- **Agent-team fit**: Which phases are too broad or cross-cutting for local in-session subagents and should instead use branch-backed worktree isolation or Claude agent teams with consolidation/PR review?

When options exist, present pros/cons with a recommendation — same style as `/spec-interview` (product-design pack). Do not manufacture artificial choices.

Continue until the user confirms the phase structure is complete.

#### 4c. Write the Roadmap

Write or update `tasks/roadmap.md` with the agreed phase structure. In State B, create the full roadmap. In State G, append or adjust only the new/changed future phase scope needed for the changed spec; do not rewrite completed phases except to add a short note that a later phase supersedes or extends prior work.

Use this format:

```markdown
# Roadmap: [Project Name]

> Generated from: [source files]
> Date: [current date]
> Total Phases: [N]

## Summary
[2-3 sentence overview of the implementation strategy and sequencing rationale]

## Phase Overview
| Phase | Title | Source Spec(s) | Key Deliverable | Est. Complexity |
|-------|-------|----------------|-----------------|-----------------|
| 1     | ...   | ...            | ...             | S / M / L       |
| 2     | ...   | ...            | ...             | S / M / L       |

---

## Phase 1: [Title]

**Goal**: [What this phase achieves and why it comes first]

**Scope**:
- [Feature/capability 1 from spec section X]
- [Feature/capability 2 from spec section Y]

**Acceptance Criteria:**
- [ ] [Specific, verifiable criterion 1]
- [ ] [Specific, verifiable criterion 2]
- [ ] [Specific, verifiable criterion 3]

**Manual Tasks** (if any):
- [Human-only external prerequisite] _(blocks: Step N.X)_ or _(after: Step N.X)_

**Parallelization:** serial | research-only | review-only | implementation-safe | agent-team

**Coordination Notes:** [dependencies, shared chokepoints, and why this mode was chosen]

**On Completion** (fill in when phase is done):
- Deviations from plan: [none, or describe]
- Tech debt / follow-ups: [none, or list]
- Ready for next phase: yes/no

---

[Repeat for each phase]

---

## Deferred / Future Work
- [Items explicitly descoped during interview, with reasoning]

## Cross-Phase Concerns
### Integration Tests
- [Tests that span multiple phases, and when to write them]
### Non-Functional Requirements
- [Performance, security, accessibility — and which phase addresses each]
```

**Important**: The roadmap defines phases, goals, scope, acceptance criteria, and strategic parallelization mode — but NOT implementation steps, TDD structure, subagent lanes, write ownership, or file-level detail. That's `/plan-phase`'s job.

If a phase has human-gated prerequisites, include only those external prerequisites in `**Manual Tasks:**`. Split mixed work: human account/approval/credential steps belong in `**Manual Tasks:**`; code changes, repo configuration, CLI/API calls with available auth, tests, audits, and generated assets stay in Scope/Acceptance Criteria for `/plan-phase` to turn into `tasks/todo.md`.

Use `serial` when work is tightly coupled or file ownership cannot be separated. Use `research-only` when parallel exploration helps but implementation should remain integrated. Use `review-only` when the build should be serial but post-implementation review benefits from multiple lenses. Use `implementation-safe` only when likely write ownership can be cleanly separated. Use `agent-team` for broad cross-cutting phases that should run in isolated GitHub branches/worktrees or a dedicated multi-agent team rather than one shared local tree; the later `/plan-phase` detail must include branch-backed write lanes and a consolidation/PR review gate.

#### 4d. Seed Phase 1

After writing `tasks/roadmap.md`, immediately invoke `/plan-phase 1` for State B or `/plan-phase N` for the first newly appended State G phase to generate implementation detail. This produces `tasks/todo.md` and, when applicable, `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md`, so the user lands on an actionable starting point rather than an undecomposed roadmap.

Do not decompose later phases — those are generated just-in-time when each phase begins (via `/ship` (exec-loop pack) or `/exec` (exec-loop pack)).

After `/plan-phase` completes, continue to step 5 to scan the freshly-created or freshly-extended roadmap for any pipeline issues.

### 5. Classify Issues (States B-after, G-after, and C)

Check for each issue type in order. Include timestamps or evidence for every finding.

#### 1. Dirty Working Tree
Uncommitted changes or unpushed commits exist. These must be resolved before task pipeline work.

#### 2. Phase Completion Not Advanced
`tasks/todo.md` has all steps checked and milestone criteria met, but the phase has not been archived or the next phase loaded. Evidence: all `- [x]` in todo, no `- [ ]` remaining under implementation steps.

#### 3. Blocking Manual Tasks
`tasks/manual-todo.md` contains unchecked items with `_(blocks: Step N.X)_` annotations for steps that are next in the execution queue. These block automated progress.

#### 4. Stale Todo
`tasks/roadmap.md` was modified more recently than `tasks/todo.md`, suggesting the roadmap was updated but the current working document was not refreshed. Evidence: roadmap mtime vs todo mtime.

#### 5. Missing Implementation Steps
A roadmap phase has acceptance criteria but no implementation steps (no `### Tests First`, `### Implementation`, or `### Green` section). This phase needs `/plan-phase` before `/exec` (exec-loop pack) can execute it.

#### 6. Orphaned Manual Tasks
`tasks/manual-todo.md` references a phase that has already been completed or archived, but unchecked items remain. These need resolution or explicit deferral.

#### 7. Eligible Record Tasks
`tasks/record-todo.md` contains unchecked items whose condition appears to be true. These are advisory by default. Queue promotion to `tasks/todo.md` only when the item is now concrete execution work; otherwise leave it in `tasks/record-todo.md` with updated evidence or revisit timing.

#### 8. Due Recurring Tasks
`tasks/recurring-todo.md` contains unchecked or active items whose `Next due` is today or earlier. These are advisory by default. Queue promotion to `tasks/todo.md` only when the due item requires real execution work; otherwise leave it in `tasks/recurring-todo.md` with updated exec/evidence state.

#### 9. History Gap
Work has been completed (checked-off steps in todo, archived phases) but `tasks/history.md` is missing, empty, or its last entry predates the most recent phase archive. Evidence: phase archive timestamps vs history mtime.

#### 10. Spec-Task Drift
Specs have been modified more recently than the roadmap, suggesting the plan may not reflect the current specifications. Evidence: spec mtime vs roadmap mtime. Only flag when the spec modification is substantive (not just formatting). If the drift is a new or changed implementation scope after all roadmap phases are complete, handle it as State G in this run by extending the roadmap and seeding the first new phase; do not queue `/roadmap`. Queue `/spec-interview` (product-design pack) only when the changed spec is incomplete or ambiguous enough that roadmap sequencing cannot proceed.

#### 11. Missing Journey/Flow/UI/UX Planning
User-facing specs exist, but one or more required design-planning artifacts are missing:

- `research/journey-map.md` — run `/journey-map` (customer-lifecycle pack) first to define discovery, onboarding, aha, conversion, retention, and advocacy.
- `specs/user-flow-*.md` — run `/user-flow-map` (product-design pack) after positioning/journey context to define screen flow, branches, decisions, states, failure paths, and handoffs.
- `specs/ux-variations-*.md` — run `/ux-variations [specific-user-flow]` (product-design pack) after user-flow mapping to explore alternate progression branches for a selected flow.
- `specs/ui-*.md` — run `/ui-interview [specific-ux-variation]` (product-design pack) after UX variation planning to render an HTML visual mockup and record approve/reject/retry for a specific branch.
- `specs/ui-requirements-*.md` — run `/ui-interview --requirements-only` (product-design pack) only when the user explicitly needs a fixed content/data/action contract before `/ux-variations --layout-mode` (product-design pack).

For `/journey-map` (customer-lifecycle pack), `/user-flow-map` (product-design pack), `/ui-interview` (product-design pack), and `/ux-variations` (product-design pack), apply the Pack Availability Guard — if the target skill's pack is not in `.agents/project.json` `enabled_packs`, recommend `npx skillpacks install <pack>` from the project shell, before the skill.

Only flag this for user-facing product work. Skip for pure backend, CLI, library, infrastructure, or internal automation specs unless they include a meaningful human workflow or interface.

#### 12. Missing Roadmap (internal consistency fallback)
Specs exist in `specs/` (or `spec.md`) but `tasks/roadmap.md` does not exist. Do not queue `/roadmap` for this. This means State B was misclassified or the roadmap disappeared during the run. Re-enter State B in the same run, build the roadmap through step 4, then seed `/plan-phase 1`. If the roadmap cannot be built because required input is missing, queue the missing upstream input skill (`/spec-interview` (product-design pack), `/journey-map` (customer-lifecycle pack), `/user-flow-map` (product-design pack), `/ux-variations [specific-user-flow]` (product-design pack), `/ui-interview [specific-ux-variation]` (product-design pack), or explicit `/ui-interview --requirements-only` / `/ux-variations --layout-mode` detours) with evidence.

#### 13. Lessons Not Reviewed
`tasks/lessons.md` was updated more recently than the current phase's implementation steps were written, suggesting new lessons may apply to in-progress work.

#### 14. Unspecced Ideas
`tasks/ideas.md` contains ideas that have no corresponding spec in `specs/`. These are candidates for `/feature-interview` (product-design pack) triage. Use `/spec-interview --ideas` (product-design pack) or individual `/spec-interview` (product-design pack) runs only when the user explicitly wants full specs for every selected idea.

### 6. Order the Priority Queue

Order action items so the user can resolve pipeline issues without guessing:

1. Dirty working tree (uncommitted/unpushed work).
2. Phase completion not advanced (work is done but pipeline is stuck).
3. Blocking manual tasks (human action needed before automation can continue).
4. Stale todo (working document out of sync with roadmap).
5. Missing implementation steps (phase needs decomposition before execution).
6. Orphaned manual tasks (leftover from completed phases).
7. Eligible record tasks (advisory unless promoted to execution work).
8. Due recurring tasks (advisory unless promoted to execution work).
9. History gap (completed work not recorded).
10. Spec-task drift (plan may be outdated).
11. Missing journey/UX/UI planning (user-facing specs are not ready for roadmap).
12. Missing roadmap fallback (recover in this run by building the roadmap or queueing the missing upstream input; never queue `/roadmap`).
13. Lessons not reviewed (new lessons may apply).
14. Unspecced ideas (ideas waiting for interview).

Within each category, prefer items that unblock the most downstream work.

### 7. Update `tasks/todo.md`

Write a single top-level section named exactly:

```md
## Priority Task Queue
```

Rules:

1. If `tasks/todo.md` does not exist, create it with only this section.
2. If a previous `## Priority Task Queue` section exists, replace only that section.
3. Put the section before existing implementation work. If the file starts with a title or status block, keep that orientation text at the top and insert the priority section immediately after it.
4. Preserve all other todo content exactly unless it is inside the old priority section.
5. Do not mark existing implementation steps complete.
6. Do not remove unrelated todo sections.
7. Use unchecked boxes for unresolved issues.
8. Use checked boxes only when an issue is already resolved.
9. Never write `/roadmap` into `## Priority Task Queue`. If an issue appears to require `/roadmap`, resolve the underlying state in this run:
   - specs missing: queue `/feature-interview` (product-design pack) for idea triage, `/spec-interview` (product-design pack) when full spec creation is already confirmed, or the relevant upstream planning command
   - user-facing design gate missing: queue `/journey-map` (customer-lifecycle pack), `/user-flow-map` (product-design pack), `/ux-variations [specific-user-flow]` (product-design pack), `/ui-interview [specific-ux-variation]` (product-design pack), or explicit requirements/layout detours when needed
   - specs exist but roadmap missing: build `tasks/roadmap.md` through State B and seed `/plan-phase 1`
   - existing queue already contains `/roadmap`: replace it with `/reconcile-dev-docs fix tasks` (docs-health pack) because the queue is stale/self-referential

Action item format:

```md
- [ ] `/skill [args]` - [action description] because [reason with evidence].
```

For external manual tasks that block progress (browser/service-console work with
no reliable authenticated CLI/API path, such as DNS, OAuth, Stripe/Vercel/GitHub
dashboard setup, signups, paid account approval, or production smoke checks that
need a real account/device or human sign-off):

```md
- [ ] Complete manual task: "[task description]" _(blocks: Step N.X)_ — resolve before `/exec` (exec-loop pack) can continue.
```

Do not use this format for agent-executable work or for bookkeeping/documentation
reconciliation just because the finding mentions `tasks/manual-todo.md`. If the
work is repo edits, SDK wiring, generated assets, local commands, tests, audits,
or CLI/API work with available auth, put it in `tasks/todo.md`. If the work is
auditing, classifying, checking off, moving, or reconciling task-doc entries
against repo reality, route it to `/reconcile-dev-docs fix tasks` (docs-health pack) or describe it
as a direct dev-doc audit task.

For advisory record or recurring tasks:

```md
- [ ] Review `tasks/record-todo.md`: "[task description]" — condition appears eligible; promote to `tasks/todo.md` only if this is now concrete execution work.
- [ ] Review `tasks/recurring-todo.md`: "[task description]" — next due is today or earlier; promote to `tasks/todo.md` only if this requires execution work.
```

For dirty tree:

```md
- [ ] `/ship-end --no-deploy` (exec-loop pack) - commit and push uncommitted changes before continuing task work.
```

For missing journey/flow/UI/UX planning:

```md
- [ ] `/journey-map` (customer-lifecycle pack) - create `research/journey-map.md` before roadmap because user-facing specs need lifecycle context.
- [ ] `/user-flow-map` (product-design pack) - create `specs/user-flow-[topic].md` before roadmap because user-facing specs need screen-flow structure.
- [ ] `/ux-variations [specific-user-flow]` (product-design pack) - create `specs/ux-variations-[topic].md` before roadmap because user-facing specs need progression-branch alternatives before branch UI approval.
- [ ] `/ux-variations --layout-mode` (product-design pack) - create `specs/ux-variations-[topic].md` before roadmap because user-facing specs need layout alternatives.
- [ ] `/ui-interview` (product-design pack) - create `specs/ui-[topic].md` before roadmap only if the selected experience still needs implementation-ready interface detail.
```

If all pipeline checks pass:

```md
- [x] Task pipeline is healthy; no issues found. Ready for `/exec` (exec-loop pack).
```

### 8. Output to User

After editing, summarize:

```
## Roadmap Updated

- Wrote/updated `tasks/todo.md`
- Priority task items: N
- Blocking issues: N (must resolve before `/exec` (exec-loop pack))
- Advisory issues: N (should resolve soon)

Next: start at the first unchecked item in `tasks/todo.md`.
```

For State A (no specs):

```
## No Specs Found

- No specifications found in `specs/` or `spec.md`
- Queued `/journey-map` (customer-lifecycle pack) first if user-facing lifecycle context is missing; otherwise queued `/feature-interview` (product-design pack) to confirm whether to create a new spec, update an existing spec, or route elsewhere

Next: `/journey-map` (customer-lifecycle pack) to define the customer/user lifecycle, or `/feature-interview` (product-design pack) when journey context is already present or not applicable.
```

For State D (all complete, documentation scan needed):

```
## All Phases Complete

- All roadmap phases are checked off
- No current `## Priority Documentation Todo` section from a previous `/research-roadmap` (research-admin pack) run was found
- Queued `/research-roadmap` (research-admin pack) for documentation scan

Next: `/research-roadmap` (research-admin pack) to check documentation health.
```

For State E (all complete, documentation queue active):

```
## Documentation Queue Active

- All roadmap phases are checked off
- Existing `## Priority Documentation Todo` contains unchecked documentation work

Next: start at the first unchecked item in `tasks/todo.md` § `Priority Documentation Todo`.
```

For State F (all complete, documentation current):

```
## Roadmap Complete

- All roadmap phases are checked off
- Documentation scan is current; no missing or stale documentation work is queued

Next: no roadmap or documentation pipeline work is queued.
```

If the pipeline is fully healthy:

```
## Roadmap Updated

- Task pipeline is healthy
- No blocking or advisory issues found

Next: `/exec` (exec-loop pack) to continue execution.
```

## Next-Step Routing

Before handing back, identify the next concrete work item from project state, then recommend the executor and invocation.

Output exactly two lines beyond the normal report:

- **Next work:** <specific planning, priority-queue, research, or execution task>
- **Recommended next command:** <one command or route>

Rules:

- Make the next work item primary. Derive it from the roadmap state, the first unchecked priority-queue item, the next unplanned phase, advisory queues, or the absence of remaining work. Do not use agent mode itself as the next work item.
- Never recommend `/roadmap` as the next command from a `/roadmap` run. It is the scanner/router; once it has updated the queue, the next command must be the first queued actionable skill (`/feature-interview` (product-design pack), `/spec-interview` (product-design pack), `/journey-map` (customer-lifecycle pack), `/user-flow-map` (product-design pack), `/ux-variations` (product-design pack), `/ui-interview` (product-design pack), `/prototype` (product-design pack), `/consolidate-prototypes` (product-design pack), `/research-roadmap` (research-admin pack), `/plan-phase N`, `/ship-end --no-deploy` (exec-loop pack), `/reconcile-dev-docs fix tasks` (docs-health pack), `/exec` (exec-loop pack), `/guide` (guided-walkthrough pack), or `none`). If the first unchecked item itself says `/roadmap`, treat that as a stale/self-referential queue item and route to `/reconcile-dev-docs fix tasks` (docs-health pack) with evidence.
- Use `./scripts/agent-mode.sh` only to choose command text. If it is missing, unset, or non-zero, infer routing from the current invocation and task type instead of asking the user to select a mode by default.
- Inference defaults:
  - Claude slash invocation (`/roadmap`, `/plan-phase`, `/exec` (exec-loop pack), `/delegate` (agent-bridge pack)) or orchestration-heavy work → recommend the matching `/...` route.
  - Imported Codex dollar routes → normalize to the matching Claude `/...` command unless the next action is explicitly a cross-agent handoff.
  - External manual work or browser-gathered evidence with no reliable authenticated CLI/API path (DNS/OAuth/service dashboards, auth setup, production smoke checks that need real account/device or human sign-off) → recommend `/guide` (guided-walkthrough pack) or a Claude-guided manual step.
  - Task-doc bookkeeping, stale `tasks/manual-todo.md` cleanup, or reconciliation against repo/history reality → recommend `/reconcile-dev-docs fix tasks` (docs-health pack) or a direct dev-doc audit, not `/guide` (guided-walkthrough pack).
- Only present multiple commands when the ambiguity materially changes execution safety or there are equally valid next work items. Otherwise choose the best route and mention degraded mode lookup inline.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/roadmap-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Constraints

- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, include `npx skillpacks install <pack-name>` from the project shell, as the install prerequisite before the recommendation.
- **Always interview for new roadmaps.** Do not produce a roadmap without user input on priorities and sequencing when building one from scratch (State B).
- **Respect existing specs.** Do not modify files in `specs/` (or `spec.md`) — the roadmap references specs, it doesn't rewrite them.
- **Phase headers must use `## Phase N: [Title]` format** for compatibility with `/exec` (exec-loop pack), `/ship` (exec-loop pack), and phase transition logic.
- **Acceptance criteria must be specific and checkable** — not vague statements like "works correctly."
- **Do not include TDD steps or file-level implementation detail** in the roadmap. That belongs in `/plan-phase`.
- **`tasks/roadmap.md` is the source of truth** for the full phased plan. `tasks/todo.md` holds only the current phase.
- **Do not put roadmap content in CLAUDE.md** — CLAUDE.md is for project conventions only.
- **Keep the interview focused.** This is about sequencing and priority, not re-litigating spec decisions. If a spec question comes up, note it and suggest running `/spec-interview` (product-design pack) again for that topic.
- Update `tasks/todo.md` and `tasks/roadmap.md`; it must not run queued priority items. It may invoke `/plan-phase 1` only as the explicit Phase 1 seed described above.
- Preserve user-authored todo content outside `## Priority Task Queue`.
- Every issue must include evidence (timestamps, checked-item counts, file existence).
- Do not directly modify `tasks/manual-todo.md`, `tasks/record-todo.md`, `tasks/recurring-todo.md`, `tasks/history.md`, or any specs (except to create `tasks/roadmap.md` in State B). `/plan-phase 1` may create or update task files during the explicit Phase 1 seed.
- Do not put agent-executable work in `**Manual Tasks:**` or `tasks/manual-todo.md`. Manual means human-only external prerequisite; automatable repo, CLI, API, test, audit, or asset work belongs in `tasks/todo.md`.
- Do not treat `tasks/record-todo.md` or `tasks/recurring-todo.md` as execution queues. They are advisory surfaces unless an item is explicitly promoted into `tasks/todo.md`.
- Do not create or modify source code.
- Do not archive phases, advance the pipeline, or execute implementation steps.
- Prefer actionable skill invocations (`/ship` (exec-loop pack), `/exec` (exec-loop pack), `/plan-phase N`, `/research-roadmap` (research-admin pack)) over vague guidance.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/spec document (`research/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.
- Keep any existing user approval requirement before overwriting or replacing a document; archiving does not replace asking when the skill already requires approval.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
