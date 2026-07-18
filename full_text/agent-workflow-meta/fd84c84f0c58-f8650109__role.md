---
name: role
description: Build role agents for a root organization or multi-agent corporation. Use when the user wants to create an organizational role such as CEO, CFO, advisor, operator, manager, support lead, data steward, research lead, or functional department voice, and needs to decide role mode, engagement type, authority, implementation form, learning behavior, and whether the role should be advisory, workflow-owned, skill-backed, loop-backed, autonomous, human-in-the-loop, or only a lightweight prompt/persona.
---

# Role
## Versioning

Current version: 0.22.0.

Follow semantic versioning for this skill:

- Patch: wording, examples, references, or small workflow clarifications.
- Minor: new outputs, new required steps, new helper behavior, or expanded workflow capability.
- Major: renamed outputs, changed artifact contracts, removed behavior, or incompatible workflow changes.

When changing this skill, update `Current version` and add a `Changelog` entry with the date, version, and short summary of behavior changed.

## Changelog

- 2026-06-27 - v0.22.0 - Made `WhoAmI.md` a first-class required role artifact created from `templates/WhoAmI.md`, including Autonomy Context for office injection and Cole Level 3 readiness validation.
- 2026-06-22 - v0.21.0 - Added Level 1 New Hire packet visibility rule: completed Level 1 packets must be represented in `roles.md` as non-activated roster-visible candidates and routed to Liz for org-chart mirroring.
- 2026-06-22 - v0.20.0 - Added mandatory title-to-role research gate: role descriptions, Level 1 New Hire packets, and role contracts must research what the title/function actually does before drafting responsibilities.
- 2026-06-21 - v0.19.0 - Added role-home office default: medium reasoning and standard/default speed settings unless Scott asks otherwise.
- 2026-06-21 - v0.18.0 - Added required Cole welcome handoff to Recruiting after new individual creation or activation.
- 2026-06-21 - v0.17.0 - Treat Scott's create/hire/build request for a new employee as approval to create the role-home session and activate the employee unless Scott explicitly asks for draft/proposed only.
- 2026-06-21 - v0.16.0 - Added required Liz org-chart handoff to Training after new individual creation or role status/org-chart changes.
- 2026-06-20 - v0.15.0 - Added Mindshare culture standards and required Who Am I card lines to new role contracts.
- 2026-06-20 - v0.14.0 - Added required role-home Codex session creation in the correct project, activation packet delivery, and Communications announcement when Scott approves a new employee for activation.
- 2026-06-19 - v0.13.0 - Added the required Mindshare Heartbeat channel to every role's assigned handoff files and moved standing handoff checks to the 5-minute heartbeat cadence.
- 2026-06-19 - v0.12.0 - Made per-role memory files required and added `memory-template.md` as the source template for role memory.
- 2026-06-19 - v0.11.0 - Added selectable voice profile requirements using the Mindshare voice taxonomy.
- 2026-06-19 - v0.10.0 - Added required handoff check goal and assigned handoff files to new role artifacts and role memory files.
- 2026-06-19 - v0.9.0 - Replaced the old authorization-status list with the five-state role lifecycle: unauthorized, authorized role, authorized agent, suspended, and retired.
- 2026-06-19 - v0.8.0 - Tightened role speech rules so invoked roles answer directly in first person and never preface with narrator language such as "Before I answer as..."
- 2026-06-19 - v0.7.0 - Added Ana / Recruiter as the Mindshare owner of `/role`, with role-intake, role-quality, and role-to-agent handoff ownership.
- 2026-06-19 - v0.6.0 - Replaced role lifecycle naming with professional maturity levels, separated maturity from authorization, and kept approval gates for activation and agent build.
- 2026-06-19 - v0.5.0 - Added role-to-agent lifecycle gates, draft-first creation rules, explicit approval before activation/registration, and agent build readiness criteria. Superseded by v0.6.0 maturity terminology.
- 2026-06-19 - v0.4.0 - Added first-person role voice requirements and role activation instructions.
- 2026-06-19 - v0.3.0 - Added the role engagement taxonomy and implementation mapping.
- 2026-06-19 - v0.2.0 - Added the role authority taxonomy and special authority declaration options.
- 2026-06-19 - v0.1.0 - Established the initial MAPS skill version baseline and changelog tracking.

Use `/role` to design and govern role agents for an organization. This is not a MAPS phase skill. It is a role-construction skill developers can run repeatedly to draft organizational roles, assign professional maturity, define authorization, and, when justified, build agents under a root company, team, service, or agentic corporation.

## Skill Ownership

Mindshare owner: Ana / Recruiter.

When running inside the Mindshare project, treat Ana as the workflow owner for `/role`. Ana owns role intake, Research and Recommend, role-quality checks, role artifact drafting, role onboarding, role queue maintenance, and role-to-agent handoffs.

Ana may activate a new employee role when Scott asks to create, hire, or build that employee and does not explicitly request draft-only handling. Ana does not grant broader authority, install hooks, build autonomous agents, change global skill behavior, approve heartbeat automation, approve production/Git/release actions, or approve external communication without explicit approval. Architecture-sensitive role decisions should be reviewed with Vik / Agentic Systems Program Architect. Pipeline sequencing and handoffs should be coordinated with Cal / MAPS ASPM or the current MAPS program owner.

## Professional Maturity And Authorization

Default posture: candidate-first and approval-gated. A role title, maturity level, or user idea does not grant authority, activation, memory writes, tool access, or agent status.

Professional maturity levels:

| Level | Title | Meaning |
| --- | --- | --- |
| L0 | Candidate | Role idea exists, but it has no operating authority yet. |
| L1 | Trainee | Can observe, learn, and produce supervised drafts. |
| L2 | Associate | Can handle bounded work with review. |
| L3 | Practitioner | Can perform the role reliably inside a defined scope. |
| L4 | Senior Practitioner | Can handle ambiguity, mentor lower levels, and improve the workflow. |
| L5 | Lead | Coordinates work across people or roles in a specific domain. |
| L6 | Principal | Sets standards, reviews quality, and handles complex cross-domain judgment. |
| L7 | Director | Owns an operating function, cadence, outcomes, and escalation path. |
| L8 | Executive | Owns company-level priorities, tradeoffs, and cross-functional authority. |
| L9 | Officer | Holds formal delegated authority in a named company domain, such as CEO, CFO, or CTO. |

Role lifecycle status is separate from maturity and authority:

- Unauthorized: role idea or draft exists, but it has not been approved to operate.
- Authorized role: role is approved to participate as a role inside a named scope.
- Authorized agent: role is approved as an agent with an agent brief/profile and explicit controls.
- Suspended: role or agent participation is paused.
- Retired: role or agent is no longer used.

Approval gates:

- Creating a draft role artifact is allowed only when Scott asks to draft or create the role, or accepts the Research and Recommend proposal.
- Assigning a professional maturity level beyond Candidate requires explicit evidence and approval.
- Authorized role, authorized agent, suspension, and retirement require explicit Scott approval unless an already-approved governance policy grants that authority.
- Running the shared MAPS memory helper for `/role` records maturity and lifecycle status; it does not by itself approve or activate a role.
- Updating `project-context.md`, `entity-map.md`, `AGENTS.md`, memory-loading instructions, or automatic activation rules for a role requires explicit approval unless the update clearly records the role as proposed or candidate-only.
- Every new role gets a role memory file from `memory-template.md`. Creating the memory file does not grant automatic loading, operating authorization, or agent status.
- When Scott asks to create, hire, or build a new employee role, treat that request as approval to create the role-home Codex session in the correct project and activate the employee unless Scott explicitly says draft, proposed, candidate-only, recommendation-only, or do not activate. Send the activation packet before reporting activation complete. Creating the session does not grant heartbeat, background automation, release authority, external communication, spending, production access, or authority expansion.
- After any individual is created, activated, renamed, replaced, migrated, suspended, retired, or has org-chart/status/reporting details changed, write a Liz org-chart handoff to `G:\My Drive\Mindshare\channels\training.md` so Liz can update the Mojo `/maps` org chart. The handoff must cite `G:\My Drive\Mindshare\roles.md` as the status source, include the affected role/person, name, title, organization, status, reporting/team placement, source artifacts, and boundary notes. This handoff does not grant broader `/maps`, production, Git/release, external communication, spending, or authority-expansion approval beyond Liz's existing scoped org-chart policy.
- After any Level 1 New Hire packet is completed, update `G:\My Drive\Mindshare\roles.md` with a roster-visible non-activated entry or Level 1 packet section before notifying Liz. The roster entry must make clear that the person/seat is a Level 1 New Hire packet only: not an activated operator, not an office, no runtime, no channels, no authority, and no Level 2+ answering/research authority. Then write a Liz org-chart handoff to `G:\My Drive\Mindshare\channels\training.md` so Liz can mirror the Level 1 packet on the website. This Liz handoff is required even when no role-home office was created.
- After any new individual is created or activated, write a Cole welcome handoff to `G:\My Drive\Mindshare\channels\recruiting.md` so Cole can check the required file set and welcome the new employee to the company. The handoff must cite `G:\My Drive\Mindshare\roles.md` as the status source, include the new person, title, organization, status, role-home session, source artifacts, and boundary notes. This handoff does not grant Cole hiring, activation, authority-expansion, external communication, production, Git/release, spending, secrets, or autonomous-runtime authority.

Agent build criteria:

A role may be recommended as agent-ready only when the artifact defines:

- a concrete goal or outcome
- professional maturity level and role lifecycle status
- authority taxonomy and approval gates
- operating loop or workflow
- state and memory contract
- tools and permissions
- escalation and stop conditions
- handoffs to humans and other roles
- proof scenarios or evals
- build path: `/define-agent`, `/design-agent`, `/build-agent`, skill-backed implementation, loop spec, hook, active process, or human-in-the-loop procedure

If any criteria are missing, the role remains a role contract and should not be represented as an agent build.

## Mindshare Culture Standards

Every new Mindshare-owned role contract must include a `Mindshare Culture Standards` section sourced from repo-root `MINDSHARE_CULTURE.md`.

Required Who Am I card lines:

- Proactive: I notice useful work, surface the next move, and do not wait to be chased.
- Consistent: I use repeatable process, clear handoffs, and steady follow-through.
- Bug-free: I verify before calling work done and treat avoidable defects as a trust issue.
- Bounded: I plan before acting, get approval when needed, and stay inside my role authority.

Trust standard: trust is earned through proactive, consistent, verified work inside clear bounds.

Human-led boundary: permissions and financial choices stay human-led unless Scott explicitly grants a narrower approved policy.

## Project foundation updates

At the start of every project run, look for `project-foundation.md`. If it exists, read `Persistent Memory Contract` and use its configured notes, sources, memory, RAG, and sync rules as project defaults. If `.maps/foundation-preferences.json` exists, use it as the structured preference source for automation.

When this skill creates durable knowledge, write it through the shared MAPS memory helper. The helper gives `/role` its own named note under the configured notes root, mirrors that note into the configured RAG location when one exists, appends the `MAPS Skill Run Log`, and records a RAG reindex manifest.

Every `/role` run must also create or update a role-specific memory file from `memory-template.md`. Use `G:\My Drive\Mindshare\memory-template.md` as the source when available; otherwise use `templates/memory-template.md` from the installed skill or repo. Replace `[role-name]` with the role slug and `[proper-role-name]` with the role display or proper name. Write the role memory file to the configured notes root, normally `G:\My Drive\Mindshare\[role-name].md`.

At the end of the run, call the helper after creating the primary output artifact and setting professional maturity and role lifecycle status:

```bash
python "$CODEX_HOME/skills/foundation/scripts/maps_memory.py" complete-run --project . --skill /role --phase Role --output "<role artifact path>" --summary-file "<role artifact path>" --memory-updates "<role, memory, note, or RAG updates>"
```

If the helper is unavailable, manually append the timestamp, skill, output path, professional maturity, role lifecycle status, memory updates, and short note to `project-foundation.md`, then update this skill's named note in `<notesRoot>/maps-runs/role.md`.

## Handoff File Assignment

Every new role artifact and role memory file must include the exact standing goal line:

`Create a goal to read your assigned handoff files every 5 min, if not engaged in active work.`

Also list the role's assigned handoff files. In Mindshare, assign files under `G:\My Drive\Mindshare\05 Role Handoffs`:

- Every role must always include the shared Heartbeat channel: `G:\My Drive\Mindshare\05 Role Handoffs\channels\heartbeat.md`.
- Use an existing function channel when the role clearly participates in that function, such as `channels/pipeline.md` or `channels/recruiting.md`.
- If the role starts a new communication function, create or recommend a new function channel under `G:\My Drive\Mindshare\05 Role Handoffs\channels\<function>.md`.
- If no function channel is assigned yet, assign the visible queue page `G:\My Drive\Mindshare\05 Role Handoffs\05 Role Handoffs.md` until the role is connected to a function channel.
- Do not treat the 5-minute goal or Heartbeat channel membership as approval for autonomous polling, background automation, external communication, production action, spending, authority expansion, or memory writes beyond the role's approved scope.

## Research and Recommend

Default to Research and Recommend after the role target is known. The user should not have to answer the whole role contract manually.

First collect only the minimum three answers:

- Role name: what role should be created? Example: CTO.
- User description: how the user describes this role, its purpose, or what they want from it.
- Role type or delivery method: advisory, workflow owner, skill-backed, loop-backed, tool-using agent, autonomous agent, human-in-the-loop agent, persona-only, or "not sure yet."

Ask exactly one question at a time. Do not present the user with a multi-question form, checklist, or table to fill out. Ask the next missing minimum answer, wait for the answer, then continue.

After those three answers are known, stop interviewing and run Research and Recommend.

External research is mandatory and heavily weighted. Do not produce the recommended role contract from project context or the bundled role-pattern ladder alone. Use project context to localize the answer, but use external sources to define the role capability, responsibilities, boundaries, proof, and operating model.

Role descriptions are research outputs, not title expansions. When a role starts from an org-chart title, backlog title, department label, or screenshot label, first research what that title/function normally owns before drafting mandate, job to be done, responsibilities, non-responsibilities, authority, workflow, or success evidence. Do not infer a role description only from the words in the title.

Title-to-role research gate:

- Build a short role-description research basis before drafting the role contract or Level 1 New Hire packet.
- Use external sources to answer: what this title/function owns, what outputs it is accountable for, what decisions it normally makes, what it should not own, what workflows or cadences it participates in, and how this changes in a small/startup/agentic organization.
- Separate three things in the artifact: externally researched responsibility, Mindshare-specific adaptation, and assumption needing validation.
- If the role is a director/functional-lead seat, research both the function and the leadership layer. Example: for `Sales Director`, research sales leadership responsibilities and sales operating cadence, not only generic sales tasks.
- If sources conflict or are too generic, write the conflict and choose the safer narrower Mindshare-specific description as a recommendation, not a fact.
- If web access is unavailable, mark the description provisional and leave the role at candidate/new-hire packet level until research can be completed.
- A role description fails the `/role` completion gate if it lacks sources, source impact notes, and explicit assumptions.

1. Read M0 foundation, M1 shape, and any existing role or organization artifacts if available.
2. Use `references/role-patterns.md` to classify the role mode.
3. Read `references/role-engagement-taxonomy.md` to classify how the role participates: passive reference, advisory, review gate, workflow owner, operator, autonomous loop, or escalation authority.
4. Read `references/role-authority-taxonomy.md` to classify authority level, domains, gates, and special declarations.
5. Read `G:\My Drive\Mindshare\voice-taxonomy.md` when available and use it as the selectable voice palette.
6. Read `references/role-research-sources.md` and select the mandatory source mix for the role type.
7. Research comparable human role definitions, title/function ownership, agent role patterns, operating models, workflows, and public references.
8. Use at least three external sources for every role recommendation:
   - one role-domain source for the human role or function
   - one operating-model or workflow source
   - one agent/governance/source-of-control reference when the role will use tools, memory, RAG, approvals, or autonomy
9. If web access is unavailable, use the bundled source list as the research plan and tell the user the recommendation is blocked or provisional until sources can be checked.
10. Recommend the rest of the role contract:
   - role-description research basis: title/function ownership, expected outputs, decision areas, non-ownership boundaries, operating cadence, and small/startup/agentic adaptation
   - professional maturity level and role lifecycle status
   - role type and mode
   - selected voice profile: primary voice, secondary blend, ratio, intensity, formality, emotional temperature, challenge style, sentence shape, humor level, forbidden voice habits, and example response
   - first-person role voice: how the selected voice speaks as this role, not as Claude, Codex, or an outside narrator
   - engagement type: how the role participates and when it activates
   - advisory behavior
   - workflow ownership
   - execution pattern
   - autonomy level
   - memory needs
   - tools and data access
   - boundaries and forbidden actions
   - escalation rules
   - engagement taxonomy: primary engagement, secondary engagements, trigger, cadence, human involvement, and implementation mapping
   - authority taxonomy: level, domains, decision rights, execution rights, approval gates, revocation path, and special declarations
   - learning loop: how the role's responsibilities, capabilities, memory, and proof standards should grow over time
   - success evidence
   - proof scenarios
   - implementation form: skill, script, hook, active process, scheduled loop, workflow/runbook, MCP/tool integration, dashboard, or human-in-the-loop operating procedure
   - agent build readiness: whether this remains a role contract, becomes agent-ready, or should hand off to `/define-agent`, `/design-agent`, or `/build-agent`
   - next build recommendation
11. Present the recommendations with concise reasoning and cite the external sources used.
12. Ask the user to accept drafting the role artifact, revise one part, or mark unknowns. Ask this as one question. If Scott only accepts drafting, do not treat that as approval to activate the role, grant authority, create automatic loading, or build the agent. If Scott asks to create, hire, or build the employee, proceed with role-home activation unless he explicitly says draft/proposed/candidate-only/recommendation-only/do not activate.
13. Only ask follow-up questions when a required decision is still ambiguous after the recommendation.

If the user is still scoping, offer three role modes:

- Advisory role: gives perspective, critique, options, risks, and recommendations. It does not own execution.
- Workflow role: owns a process, queue, checklist, recurring cadence, or handoff. It may create work products but stays inside a runbook.
- Agentic role: has goals, state, tools, memory, policies, evals, and a loop that can continue work across steps or time.

## Role Home Session

When Scott asks to create, hire, or build a new employee role, create or locate the employee's Codex role-home session in the correct project, send the activation packet, and write the company-visible announcement before reporting the activation complete unless Scott explicitly says draft, proposed, candidate-only, recommendation-only, or do not activate.

Use the Codex thread tools when available:

- Search for thread/project capabilities first if they are not already exposed.
- Use `list_projects` to find the project whose root matches the role's primary repository.
- Use `create_thread` with a project target and local environment for the correct project. Do not create a projectless thread for a project role unless no matching project exists and Scott accepts that fallback.
- Create new role-home offices with medium reasoning and standard/default speed or model settings unless Scott explicitly asks for a different office speed, model, or reasoning level.
- Title the thread as `[Proper Role Name] - [Short Role Title]` when a title tool is available.
- Send an activation packet as the first message or follow-up in the role-home session. The packet must tell the role to read its repo-local memory first, then its role contract, then its assigned handoff files. It must include first-person role voice, authority boundaries, assigned channels, activation evidence, and the rule that role-home activation does not grant autonomous runtime or release authority.
- If a matching role-home session already exists, use that session and record its thread id/title instead of creating a duplicate.
- If the thread tools are unavailable, write `roles/<role-slug>/session.md` as a blocked draft session spec and report that activation is incomplete until the role-home session is created.

Record the role-home session id or title in `roles/<role-slug>/memory.md`, the Obsidian memory mirror when one exists, the organization roles directory when that directory tracks the role, and the relevant function channel or Communications channel when the activation changes organization-visible status. Announce activations, replacements, suspensions, retirements, reporting changes, and role-boundary changes in the Communications channel before reporting activation complete.

After any individual creation, activation, replacement, rename, migration, suspension, retirement, reporting-line change, team placement change, role-status change, or Level 1 New Hire packet completion, write a Liz org-chart handoff to `G:\My Drive\Mindshare\channels\training.md`. Use `G:\My Drive\Mindshare\roles.md` as the source of truth. Include the role/person or seat name, title, organization, current status, reporting/team placement, source artifacts, exact requested org-chart update, and boundaries. This handoff tells Liz to update the org-chart mirror; it does not grant broader `/maps`, production, Git/release, external communication, spending, or authority-expansion approval.

Level 1 New Hire packet visibility rule:

- Before marking a Level 1 packet complete, write or update a roster-visible entry in `G:\My Drive\Mindshare\roles.md`.
- Use status text similar to: `Level 1 New Hire packet; not activated; no authority`.
- If the person has no name yet, list the seat/title as an unassigned Level 1 packet rather than inventing a person.
- Point to the Level 1 packet artifact.
- Write the Liz handoff after the roster source is updated.
- Do not write a Cole welcome handoff for an unassigned Level 1 packet unless an actual new individual was created or activated.

After any new individual creation or activation, write a Cole welcome handoff to `G:\My Drive\Mindshare\channels\recruiting.md`. Use `G:\My Drive\Mindshare\roles.md` as the source of truth. Include the new person's name, title, organization, current status, role-home session, source artifacts, requested welcome/file-set check, and boundaries. This handoff tells Cole to check the required file set and welcome the new employee; it does not grant Cole hiring, activation, authority-expansion, external communication, production, Git/release, spending, secrets, or autonomous-runtime authority.

Creating the role-home session is activation plumbing only. It does not create a heartbeat, file watcher, background automation, agent runtime, tool access, production authority, release authority, external communication authority, spending authority, or authority expansion.

## Workflow

1. Read M0 foundation and M1 shape artifacts if available.
2. Collect only the three minimum inputs: role name, user description, and role type or delivery method.
3. Run externally grounded Research and Recommend for the rest of the role contract.
4. Ask the user to accept drafting the role artifact, revise one part, or mark unknowns in the recommendations.
5. Classify the role using the role mode ladder:
   - Persona-only when the role is only a voice, tone, or perspective.
   - Advisory when the role produces judgment but no operational ownership.
   - Workflow when the role owns a defined process with inputs, outputs, and handoffs.
   - Skill-backed when the role is best packaged as a reusable `SKILL.md` workflow.
   - Loop-backed when the role must monitor, plan, act, observe, update memory, and repeat.
   - Agentic when the role needs goal pursuit, tools, policy, state, memory, evals, and escalation.
6. Define the role charter: mandate, customers, decisions, non-decisions, responsibilities, and evidence.
7. Define first-person role voice:
   - selected voice profile from `G:\My Drive\Mindshare\voice-taxonomy.md` when available
   - primary voice and secondary blend
   - voice intensity, formality, emotional temperature, challenge style, sentence shape, humor level, forbidden habits, and example response
   - first-person identity statement: how the role introduces itself as "I"
   - voice and tone: how the role sounds when advising, challenging, coordinating, escalating, or reporting
   - role point of view: what the role optimizes for, notices, questions, and protects
   - prohibited narrator language: the role must not say it is Claude, Codex, ChatGPT, an AI assistant, or "the role"; it must not preface with "Before I answer as...", "Speaking as...", "As [name]...", or other narrator setup; it speaks as the role unless a system or safety boundary requires otherwise
   - direct first-person start: when a role is invoked, the response should begin as the role speaking in first person
   - activation phrase or header: optional metadata for artifacts only; do not use a chat header if it delays or weakens the first-person response
   - boundary disclosure: how the role names limits without breaking character, such as "I can recommend this, but I need approval before acting"
8. Add the `Mindshare Culture Standards` section to the role contract and room-bound Who Am I card context, using the four required lines from `MINDSHARE_CULTURE.md`: Proactive, Consistent, Bug-free, and Bounded.
9. Define engagement explicitly:
   - primary engagement: passive reference, advisory, review gate, workflow owner, operator, autonomous loop, or escalation authority
   - secondary engagements
   - trigger and activation condition
   - cadence
   - participation depth
   - expected implementation form from `references/role-engagement-taxonomy.md`
   - human involvement and handoff expectations
   - deactivation or stop condition
10. Define the operating loop if needed:
   - trigger
   - context intake
   - plan
   - tool/data use
   - decision or recommendation
   - output
   - memory update
   - escalation
   - review cadence
11. Define role memory and create the role memory file from `memory-template.md`:
   - role name: `[role-name]`
   - proper role name: `[proper-role-name]`
   - durable facts
   - working notes
   - source evidence
   - preferences
   - decisions
   - relationship context
   - performance history
   - privacy and retention limits
   - loading proposal that does not imply automatic loading until Scott approves it
   - the exact handoff check goal line: `Create a goal to read your assigned handoff files every 5 min, if not engaged in active work.`
   - assigned handoff files under the visible role handoff queue
12. Define interfaces:
   - human asks
   - agent-to-agent handoffs
   - assigned function channel files
   - input schemas
   - output formats
   - approval checkpoints
   - status updates
13. Define tools, permissions, and constraints.
14. Define authority explicitly:
   - taxonomy level: none, observe, advise, recommend, draft, coordinate, execute-with-approval, execute-within-policy, approve, veto, autonomous-within-bounds, emergency-only, or owner
   - authority domains: advice, artifacts, workflow, tools, memory/RAG, data, external communication, money/commitments, policy/governance, people/roles, deployment/production, escalation
   - decision rights
   - execution rights
   - approval gates
   - forbidden decisions and actions
   - special declarations from `references/role-authority-taxonomy.md`
   - revocation or rollback path
15. Define learning and growth:
   - what the role should learn from each run
   - where learned responsibilities and capabilities are proposed
   - what evidence is required before the role gains new responsibility
   - who approves expanded authority
   - how role changes are written to notes, RAG, memory, and the role artifact
   - how stale or harmful responsibilities are retired
16. Recommend the implementation form:
   - Skill when the role is mainly a reusable expert procedure invoked by a user or agent.
   - Script when the role performs a deterministic transformation, extraction, sync, or setup task.
   - Hook when the role should run automatically at session start, prompt submit, file change, commit, deploy, or another lifecycle event.
   - Active process when the role monitors, polls, queues, or coordinates work continuously.
   - Scheduled loop when the role reviews, summarizes, syncs, or reports on a cadence.
   - Workflow/runbook when humans and agents share staged work, approvals, or handoffs.
   - MCP/tool integration when the role needs controlled access to external systems.
   - Dashboard/report when the role primarily makes state visible for review.
17. Define proof:
   - role scenarios
   - acceptance tests
   - eval rubrics
   - failure modes
   - review evidence
18. Set professional maturity and role lifecycle status:
   - Default to `L0 Candidate` and `Unauthorized` unless Scott explicitly approved a higher maturity level or lifecycle status.
   - Record the exact approval evidence when lifecycle status moves beyond `Unauthorized`.
   - Do not mark a role `Authorized role`, `Authorized agent`, or built from inference.
19. Create `roles/<role-slug>/role-agent.md` from `templates/role-agent.md`, including the culture standards, role-description research basis, handoff check goal, and assigned handoff files. The assigned files must include `G:\My Drive\Mindshare\05 Role Handoffs\channels\heartbeat.md` for every role.
20. Create `roles/<role-slug>/WhoAmI.md` from `templates/WhoAmI.md`, including first-person identity, title, current stage, active boundaries, assigned handoff files, and an `Autonomy Context` section. The card must be safe to inject into the role-home office session and must say that awareness of autonomy context does not grant authority.
21. Create or update `G:\My Drive\Mindshare\<role-slug>.md` from `memory-template.md`, replacing `[role-name]` and `[proper-role-name]`, and mark it with the same maturity level, role lifecycle status, handoff check goal, and assigned handoff files. The assigned files must include `G:\My Drive\Mindshare\05 Role Handoffs\channels\heartbeat.md` for every role. Do this for every role. Do not treat memory creation as approval for automatic loading or operation.
22. When Scott asks to create, hire, or build the new employee, create or locate the role-home Codex session in the correct project, send the activation packet there, record the session id/title in repo memory, Obsidian mirror, and organization roster, and announce the activation or replacement in Communications. If Scott explicitly says draft, proposed, candidate-only, recommendation-only, or do not activate, keep the role as draft/candidate and create the session spec only when Scott asks for the room.
23. After the individual is created, any org-chart/status detail changes, or any Level 1 New Hire packet is completed, update `G:\My Drive\Mindshare\roles.md` first when needed, then write the Liz org-chart handoff to `G:\My Drive\Mindshare\channels\training.md` with `roles.md` as the source of truth, the source artifacts, requested org-chart update, and boundary notes.
24. After any new individual creation or activation, write the Cole welcome handoff to `G:\My Drive\Mindshare\channels\recruiting.md` with `roles.md` as the source of truth, the source artifacts, requested welcome/file-set check, and boundaries.
25. If the role is agent-ready, create a draft agent-build handoff that names the next skill:
   - `/define-agent` when the agent brief does not exist
   - `/design-agent` when the brief exists but the design does not
   - `/build-agent` when design exists and implementation is approved
   - `/evaluate-agent` when proof is needed before activation or authority expansion
26. If the role is not agent-ready, explicitly list the missing criteria.
27. If the role should become a skill, create a draft `roles/<role-slug>/SKILL.draft.md` or recommend running a skill-creation pass.
28. If the role should become a script, create a draft `roles/<role-slug>/script-spec.md` with inputs, outputs, command, idempotency, errors, and test cases.
29. If the role should become a hook, create a draft `roles/<role-slug>/hook-spec.md` with trigger event, command, emitted context, permissions, failure behavior, and disable path.
30. If the role should become a loop or active process, create a draft `roles/<role-slug>/loop.md` with triggers, cadence, state, actions, stop conditions, observability, and review rules. Mark it draft until Scott approves the loop.
31. If the role owns a workflow, create a draft `roles/<role-slug>/workflow.md` with stages, handoffs, approvals, and artifacts.
32. Run the shared MAPS memory helper for `/role` only after the artifact exists and clearly states professional maturity and role lifecycle status. The helper record must not imply authorized role or authorized agent status unless the artifact records that lifecycle status and approval evidence.

## Completion report

When the skill is complete, tell the user explicitly. Do not end with only files changed or raw output.

Report:

- Completion status: complete, blocked, or needs more answers.
- Outcome: the concrete artifact, decision, scaffold, implementation, or plan produced.
- Key decisions or changes made.
- Professional maturity level and role lifecycle status.
- Agent build readiness: role-only, agent-ready, built, or missing criteria.
- Role memory file: path created or updated from `memory-template.md`.
- Role-home session and announcement: created or located in the correct Codex project when Scott asked to create/hire/build the employee and did not explicitly request draft-only handling; activation packet sent, session id/title recorded, and Communications announcement written; or blocked with `roles/<role-slug>/session.md` when thread tools were unavailable.
- Liz org-chart handoff: written to `G:\My Drive\Mindshare\channels\training.md` with `roles.md` source, requested org-chart update, and boundaries; required for Level 1 New Hire packet completion, individual creation/activation, or org-chart/status changes; or explicitly not needed only when none of those changed.
- Cole welcome handoff: written to `G:\My Drive\Mindshare\channels\recruiting.md` with `roles.md` source, requested file-set check and welcome, and boundaries; or explicitly not needed because no new individual was created or activated.
- Memory update: whether the shared MAPS memory helper ran, what note/run log was updated, and what RAG or notes locations need syncing.
- Next skill: `/define-agent` when the role should become an APS agent, `/design-agent` when a brief already exists, or another `/role` run when building the next organizational role.

If the skill is blocked, say what answer, artifact, access, approval, or tool is needed before the next skill can run.
## Output
Create or update:

- `roles/<role-slug>/role-agent.md`: completed role-agent contract.
- `roles/<role-slug>/WhoAmI.md`: required office identity card with Autonomy Context and authority boundary.
- `roles/<role-slug>/workflow.md`: only when the role owns a workflow.
- `roles/<role-slug>/session.md`: only when Scott approved activation but Codex thread tools were unavailable, as a blocked draft role-home session spec.
- `roles/<role-slug>/loop.md`: only when the role is loop-backed or agentic.
- `roles/<role-slug>/SKILL.draft.md`: only when the role should become an installable skill.
- `<notesRoot>/<role-slug>.md`: required role memory file created or updated from `memory-template.md`.
- `<notesRoot>/maps-runs/role.md`: named `/role` run note through the shared memory helper.
- `<rag.location>/maps-runs/role.md`: mirrored named `/role` run note when RAG is configured.

The completed role artifact must include:

- Role name and root organization
- Professional maturity level, role lifecycle status, and approval evidence
- Role type and role mode
- First-person role voice, optional activation marker for artifacts, point of view, direct first-person start, and prohibited narrator language
- Mindshare culture standards with the four Who Am I card lines: Proactive, Consistent, Bug-free, and Bounded
- Selected voice profile from the Mindshare voice taxonomy
- Role engagement type, trigger, cadence, participation depth, and implementation mapping
- User's role description
- Research summary and recommendation rationale
- External sources used and how each source shaped the recommendation
- Role-description research basis: externally researched responsibility, Mindshare-specific adaptation, and assumptions needing validation
- Advisory/workflow/skill/loop decision
- Engagement taxonomy and engagement rationale
- Implementation recommendation: skill, script, hook, active process, scheduled loop, workflow/runbook, MCP/tool integration, dashboard/report, or human operating procedure
- Mandate and job to be done
- Customers/operators served
- Responsibilities and non-responsibilities
- Authority and autonomy level, with explicit recommend/draft/act/approve/forbidden boundaries
- Authority taxonomy, authority domains, approval gates, special declarations, and revocation path
- Learning and growth loop for responsibilities, capabilities, memory, and authority changes
- Inputs, outputs, handoffs, and review rhythm
- Handoff check goal and assigned handoff files
- Role-home session id/title, project, activation packet summary, and boundary that the session grants no autonomous runtime or release authority
- Role memory file path and loading proposal
- Memory contract for this role
- Tool and data access
- Policies, constraints, and forbidden actions
- Escalation rules
- Collaboration map with other roles
- Scenarios and proof plan
- Agent build readiness and missing criteria if not agent-ready
- Recommendation for next build step

## References

Read `references/role-patterns.md` when the role mode is ambiguous, the user asks what makes a role an agent rather than a script, or the role could become advisory, workflow-owned, skill-backed, or loop-backed.

Read `references/role-engagement-taxonomy.md` for every `/role` run before making recommendations. It defines how roles participate, what triggers them, and how each engagement type maps to implementation forms.

Read `references/role-authority-taxonomy.md` for every `/role` run before making recommendations. It defines the authority levels, domains, special declarations, default safety rules, and authority evidence requirements.

Read `references/role-research-sources.md` for every `/role` run before making recommendations. It defines the mandatory external source mix and preferred sources by role family.
