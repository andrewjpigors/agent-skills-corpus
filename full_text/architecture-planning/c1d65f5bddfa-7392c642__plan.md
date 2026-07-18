---
name: plan
description: Strategic planning with interview, direct, consensus, and review modes.
argument-hint: "[--direct|--consensus|--interactive|--deliberate|--review] <task or artifact>"
---

<Purpose>
Plan creates comprehensive, actionable work plans before implementation. It
auto-detects whether to interview the user or plan directly, supports consensus
planning through Planner -> Architect -> Critic with RALPLAN-DR structured
deliberation, and supports reviewer-only evaluation of existing plans.
</Purpose>

<Use_When>
- The user wants to plan before implementing.
- The request is broad or vague and needs scoping before code changes.
- The user wants structured requirements gathering but not the full deep-interview loop.
- The user asks for multi-perspective consensus planning via `--consensus`.
- The user asks to review an existing plan via `--review`.
</Use_When>

<Do_Not_Use_When>
- The user wants immediate implementation with clear scope and acceptance criteria.
- The user explicitly asks for `/omagy:deep-interview`.
- The user wants autonomous end-to-end execution; use `/omagy:autopilot` once that entrypoint is available. Until then, finish planning and hand off the approved plan to `/omagy:ralph` or `/omagy:team`.
- The task is a simple question that can be answered directly.
</Do_Not_Use_When>

<Execution_Policy>
- Do not implement directly inside Plan. Plan owns planning artifacts and handoff only.
- Auto-detect interview vs direct mode from request specificity unless a flag is provided.
- Ask one question at a time in interview or interactive consensus mode.
- Gather codebase facts with `omagy explore` before asking the user about repository internals; use the `explorer` subagent only when the lookup is too broad for the bounded CLI.
- Use `/omagy:best-practice-research` before planning when correctness depends on current external best practices, official recommendations, standards, or version-aware upstream behavior.
- Use `omagy question` for material preference, scope, risk, feedback, and approval questions when an attached tmux renderer is available; otherwise use Antigravity native structured input when available, falling back to exactly one plain-text question.
- Preserve the user's language for interview questions, approval prompts, and
  final planning summaries unless the user switches language or explicitly asks
  otherwise. Technical identifiers, command names, file paths, code symbols,
  and quoted source text stay unchanged.
- `omagy question` success JSON uses `answers[]` as the primary contract. For single-question prompts, read `answers[0].answer`; treat top-level `answer` only as a legacy fallback. Batch `questions[]` may be used for non-interview grouped preference or approval prompts when one submitted form is clearer than multiple interruptions; interview mode still asks one question per round.
- Map omx `ask_codex(agent_role=...)` semantics to agy native `invoke_subagent` plus `omagy plan record-review`; do not invent an external `omagy ask_codex` CLI.
- Plans must meet quality standards: 80%+ of repository-fact claims cite concrete file/line evidence, and 90%+ of acceptance criteria are testable.
- Implementation step count must be right-sized to task scope; never default to a fixed five-step template.
- Preserve explicit user scope and cardinality. If the user asks for "one",
  "single", "only", or otherwise names a bounded count of same-kind work items,
  the selected implementation choice must not add more same-kind items. Treat
  adding extra same-kind items as a scope decision: ask the user first in
  interactive/interview mode, or keep extras as optional follow-ups in direct
  mode.
- Treat singular or generic README badge requests as minimal scope. If the user
  asks for "a README badge", "README badge", or otherwise does not explicitly
  request multiple badges, plan the smallest conventional single badge for the
  project type, or ask which badge they want. For npm packages, prefer one npm
  version badge when package metadata is available. Do not expand to license,
  runtime, build, CI, coverage, or status badges unless the user requests those
  badge categories or approves the expansion.
- Preserve explicit interaction scope. Parenthetical examples in a question
  option are not user confirmation for every example inside the parentheses.
  If an option label includes an optional affordance such as drag-and-drop,
  selecting that option confirms the broad category only; ask a separate
  question before making that affordance required, or keep it under optional
  follow-ups. Prefer option labels that do not mention unconfirmed affordances.
- Apply the shared workflow guidance pattern: outcome-first framing, concise visible updates for multi-step planning, local overrides for the active workflow branch, evidence-backed planning and validation expectations, explicit stop rules, and automatic continuation for safe reversible steps. Ask only for material, destructive, credentialed, external-production, or preference-dependent branches.
- Use `omagy plan start` to activate mode state and `omagy plan complete` or `omagy plan cancel` to terminate it.
- Persist final PRD and test-spec artifacts by writing the matching markdown files directly under `.omagy/plans/`, following the same artifact-store model as omx `.omx/plans/`.
- Do not use `omagy plan record`, temporary payload files, ad hoc Node files, or shell wrappers for final plan artifact recording.
- Verify execution handoff with `omagy plan handoff --mode <team|ralph>`. Do not use Plan handoff to launch `/omagy:ultrawork`; Ralph may use Ultrawork internally as its execution engine.
- Do not edit `.omagy/state` directly. State belongs to the Omagy runtime.
</Execution_Policy>

<Runtime_Contract>
Start every plan run by reading current state and artifacts:

```bash
omagy plan status --json
omagy memory read --json
omagy artifact list --json
```

Use clear independent tool calls for startup status, memory, artifact, and
explore reads. Do not use long `&&`, `;`, or newline shell chains for planning
context gathering because they hide which evidence source produced which result
and make failures harder to audit.

If the prompt points at a `.omagy/context`, `.omagy/specs`, `.omagy/interviews`,
or `.omagy/plans` artifact, read it through the artifact CLI:

```bash
omagy artifact read --input '{"path":"<repo-relative artifact path>","max_bytes":20000}' --json
```

Plan follows the omx planning boundary: pre-start fact gathering is allowed so
the planner can classify the request and ask informed questions. Before
`omagy plan start`, keep work limited to mode classification, current plan
status, memory/artifact reads, prompt-targeted artifact reads, and bounded
read-only `omagy explore` lookups. Do not ask user interview questions, write
drafts, record reviews, write final PRD/test-spec artifacts, or call
`omagy plan complete` before the selected mode has been started.

Start the selected mode:

```bash
omagy plan start --mode direct --input '{"task":"<task>"}' --json
omagy plan start --mode interview --input '{"task":"<task>"}' --json
omagy plan start --mode consensus --input '{"task":"<task>","deliberate":false,"interactive":false}' --json
omagy plan start --mode review --input '{"task":"<plan artifact or review request>"}' --json
```

Once the mode is selected, `omagy plan start` is the lifecycle gate for all
mode-owned work. In interview mode, start the plan state before the first
preference/scope/risk question. In direct mode, start before writing final
PRD/test-spec artifacts. In consensus mode, start before planner draft
generation, `omagy plan draft`, Architect review, Critic review, or any
`record-review`. In review mode, start before critic evaluation. If planning
cannot continue after start, cancel with `omagy plan cancel --json`.

Record intermediate drafts before review or approval:

```bash
omagy plan draft --input '{"slug":"<slug>","kind":"plan","content":"<markdown draft>"}' --json
```

Write final artifacts directly as markdown files:

```text
.omagy/plans/prd-<YYYYMMDDTHHMMSSZ>-<slug>.md
.omagy/plans/test-spec-<same-YYYYMMDDTHHMMSSZ>-<same-slug>.md
```

Use the same timestamp and slug for the PRD and test spec. Do not create
`payload.json`, `.tmp` wrappers, `.omagy/scratch` wrappers, or scripts to
record plan artifacts. Plan artifacts are append-only during planning: never
delete, rename, overwrite, or "clean up" pre-existing `.omagy/plans/*` files to
make a new plan appear latest. After the files exist, register completion
through the runtime with the exact PRD path that was just written:

```bash
omagy plan complete --input '{"prd_path":".omagy/plans/prd-<timestamp>-<slug>.md"}' --json
```

Run `omagy plan complete --input '{"prd_path":"<new-prd-path>"}' --json` before
`omagy plan handoff --mode <team|ralph> --input '{"prd_path":"<new-prd-path>"}' --json`.
Do not run handoff against an incomplete active plan.

Use a real current UTC timestamp for final artifact filenames. If you obtain
the timestamp with `date -u +"%Y%m%dT%H%M%SZ"`, use that value consistently for
both files. Do not rename plan artifacts to invented placeholder timestamps
such as `20260524T000000Z`.

Cancel instead of leaving active state if planning stops early:

```bash
omagy plan cancel --json
```
</Runtime_Contract>

<Modes>

| Mode | Trigger | Behavior |
|------|---------|----------|
| Interview | broad/vague request | ask one focused question at a time, gather repo facts first |
| Direct | `--direct` or detailed request | generate PRD/test-spec directly |
| Consensus | `--consensus` | Planner -> Architect -> Critic loop with RALPLAN-DR |
| Interactive Consensus | `--consensus --interactive` | pauses for structured user feedback and final approval |
| Review | `--review` | critic-only review of an existing planning artifact |

## Interview Mode

1. Classify the request. Broad requests with missing acceptance criteria, vague verbs, or cross-area scope use interview mode.
2. Gather discoverable codebase facts with `omagy explore` before asking the user. This may happen before `omagy plan start` only while classifying the request or preparing informed questions.
3. Start interview lifecycle with `omagy plan start --mode interview ...` before the first user preference, scope, risk, or acceptance-criteria question.
4. Ask one focused question at a time about scope, constraints, priority, risk tolerance, or acceptance criteria.
5. For broad or vague interview requests, ask at least one user preference, scope, or requirement question and receive a user answer before creating final PRD/test-spec artifacts. The only exception is an original prompt that already contains explicit feature direction, scope boundaries, and acceptance criteria sufficient for direct planning.
6. Do not treat an agent-suggested feature direction as user-selected. If repository facts reveal candidate directions, present candidate directions as options in one focused question and wait for the user's choice.
7. Treat optional interaction details, secondary capabilities, and product affordances as scope decisions. Examples include drag-and-drop, permissions, notifications, real-time sync, custom workflow columns, audit history, and local persistence/storage. Ask the user before making them acceptance criteria; otherwise put them under optional follow-ups.
   - Do not treat parenthetical examples in a structured option as confirmed requirements. Example: if the user selects "task assignment and kanban management (for example assigning tasks, dragging status)" and later narrows to "basic fixed status columns", the final plan may require task cards, assignees, and fixed columns, but must not require drag-and-drop or persistence unless separately confirmed.
   - If the selected scope can be implemented with simpler controls, prefer explicit buttons, menus, or status selectors in the required plan; put drag-and-drop, real-time sync, notifications, custom columns, audit history, and persistence under Follow-ups unless the user explicitly requested them.
8. Create final PRD/test-spec artifacts only when the user signals readiness, for example "create the plan", "I'm ready", "make it a work plan", "可以生成计划", or "就按这个做". If the user has not signaled readiness, ask the next focused question or summarize the current scope and ask whether to create the plan.
9. Treat skipped, cancelled, empty, or non-confirming readiness prompts as no readiness. Do not infer consent from `(skipped)`, `Skip`, `Esc`, timeout, silence, or answer options such as "I have more requirements". In those cases, continue interviewing or cancel the active plan state with `omagy plan cancel --json`; never write final artifacts, complete the plan, or run handoff.
10. Use the `analyst` subagent before finalizing when hidden requirements, edge cases, or risk tradeoffs remain material.
11. Stop interviewing when requirements are clear enough to plan and the user has signaled readiness; do not over-interview.
12. Produce the same PRD and test-spec artifacts as direct mode.

## Direct Mode

1. Read provided task and relevant artifacts.
2. Perform quick `omagy explore` lookups when file/module references are implied.
3. Use the `analyst` subagent for large-scope, high-risk, or ambiguous direct plans.
4. Create a PRD and matching test spec immediately.
   - For small direct plans, keep the artifacts concise but concrete: select the exact implementation choice, state scope boundaries and non-goals, cite files when known, and include a Verification Matrix with concrete checks.
   - For small direct plans with explicit cardinality, mirror that cardinality
     in the selected implementation choice. Example: if the task says "add one
     README badge", plan one badge; do not silently expand to license + runtime
     + CI badges. Put additional badge ideas in Follow-ups or ask first.
   - Do not use a fixed Unit / Integration / Regression / Manual template for small direct plans. Model omx by specifying testable acceptance criteria and concrete verification steps. Complex or deliberate plans may expand into unit / integration / e2e / observability.
5. Save matching PRD/test-spec markdown files under `.omagy/plans/`, then complete plan state with `omagy plan complete --input '{"prd_path":"<new-prd-path>"}' --json`.

## Consensus Mode

Consensus mode follows omx `$plan --consensus`: short RALPLAN-DR by default,
deliberate RALPLAN-DR when `--deliberate` is present or the work is explicitly
high risk: auth/security, data migration, destructive/irreversible changes,
production incident, compliance/PII, or public API breakage.

Consensus must preserve the same explicit scope and cardinality constraints as
direct planning. RALPLAN-DR may improve clarity, alternatives, risks, and
verification, but it must not broaden the requested product surface. For
example, a singular or generic README badge plan stays one selected badge unless
the user asked for multiple badges or approved that expansion.

The sequence is strict and sequential:

1. **Planner** creates the initial PRD/test-spec draft and compact RALPLAN-DR summary, then records the full draft with `omagy plan draft` before Architect review:
   - Principles (3-5)
   - Decision Drivers (top 3)
   - Viable Options (at least 2) with bounded pros/cons
   - If only one viable option remains, explicit invalidation rationale
   - Deliberate mode only: pre-mortem (3 failure scenarios) and expanded test plan covering unit / integration / e2e / observability
2. Launch and record consensus lanes through the Omagy/agy mapping:

   ```bash
   omagy plan start --mode consensus --input '{"task":"<task>","deliberate":false,"interactive":false}' --json
   ```

   The JSON includes `invoke_subagent_tool` for the next agy native subagent.
   It may also include `runtime.scope_constraints`. Treat that object as a
   hard planning contract, not advisory text. Every Planner, Architect, and
   Critic lane must receive and enforce it. If the constraint says exactly one
   README badge, the draft, final PRD, and test spec must require exactly one
   README badge. Do not turn "make it concrete" feedback into npm downloads,
   license, Node/runtime, CI, coverage, build, or status badges unless those
   categories were explicitly requested or approved by the user.

   Invoke that native subagent, then record the lane output:

   ```bash
   omagy plan record-review --input '{"role":"planner","verdict":"draft","summary":"<draft summary>"}' --json
   ```

3. **Architect** reviews the draft for architectural soundness, strongest counterargument, tradeoff tension, and synthesis path. Wait for Architect before Critic. Record the architect result; the returned JSON includes the critic subagent spec.
4. **Critic** evaluates principle-option consistency, fair alternatives, risk mitigation, testable acceptance criteria, and concrete verification. Critic runs only after Architect. Record the critic result:

   ```bash
   omagy plan record-review --input '{"role":"critic","verdict":"approve|iterate|reject","summary":"<critic review>"}' --json
   ```

5. If Critic says `iterate` or `reject`, collect all Architect + Critic feedback, invoke the returned Planner revision subagent, record the revised full draft with `omagy plan draft`, then repeat Architect -> Critic, up to 5 iterations.
6. If Critic approves with improvements, deduplicate and categorize accepted suggestions, merge them into the final PRD/test-spec markdown files under `.omagy/plans/`, and add a brief changelog section.
   Accepted improvements may make the selected implementation more precise
   with exact markdown, URLs, risks, and verification; they must not add extra
   same-kind required items beyond the runtime scope constraint or original
   user scope.
7. If max iterations are reached without approval, present the best current plan with a residual-risk warning and complete only if the user explicitly accepts the risk.

## Interactive Consensus

When `--interactive` is present, use `omagy question` twice:

1. After Planner draft, present the draft plus RALPLAN-DR summary:
   - Proceed to review
   - Request changes
   - Skip review and go to final approval
2. After Critic approval, present final approval options:
   - Approve and execute through `/omagy:ralph`
   - Approve and implement through `/omagy:team`
   - Request changes
   - Reject

Never ask for approval in plain text when `omagy question` or native structured
input is available.

On user approval, do not implement directly. Invoke `/omagy:ralph` with the
approved plan path plus staffing guidance for persistent single-owner execution,
or invoke `/omagy:team` with the approved plan path plus explicit worker roles,
launch hints, and team verification path for coordinated parallel execution.
When `/omagy:autopilot` is implemented, it becomes the preferred entrypoint for
hands-off `ralplan -> ralph -> code-review` delivery; Plan still must not
implement source changes itself.

## Review Mode

1. Treat review as reviewer-only. The context that authored the plan must not approve it.
2. Read the plan or draft artifact through `omagy artifact read`.
3. Use the `critic` subagent to evaluate clarity, testability, risks, verification, and handoff quality.
4. For cleanup/refactor/anti-slop work, verify that the artifact includes a cleanup plan, regression tests or an explicit test gap, smell-by-smell passes, and quality gates.
5. Return verdict: APPROVED, REVISE, or REJECT.
6. If the current context authored the artifact, hand the review to `/omagy:code-review`, `critic`, `quality-reviewer`, `security-reviewer`, or `verifier` as appropriate.
7. Do not edit source code or silently rewrite the plan in review mode.
</Modes>

<Output_Requirements>
Every final PRD must include:

- Requirements Summary
- Acceptance Criteria with concrete pass/fail checks
- Implementation Steps sized to the actual scope, with file references where applicable
- Selected implementation choice, scope boundaries, and non-goals for small direct plans
- Explicit cardinality preservation when the user provides a bounded count
  such as one/single/only; extra same-kind work belongs in follow-ups or an
  explicit scope question, not the selected implementation choice
- Any `runtime.scope_constraints` returned by `omagy plan start`, including
  its original scope quote, selected cardinality, selected default, forbidden
  required expansions, and how the PRD/test spec preserves it
- Risks and Mitigations
- Verification Steps
- For consensus: RALPLAN-DR summary
- For consensus final output: ADR with Decision, Drivers, Alternatives considered, Why chosen, Consequences, Follow-ups
- For consensus execution handoff: Available-Agent-Types Roster, Follow-up Staffing Guidance, suggested reasoning levels by lane, explicit `/omagy:team` and `/omagy:ralph` Launch Hints, and Team Verification Path
- For deliberate consensus: pre-mortem with 3 failure scenarios and expanded test plan covering unit / integration / e2e / observability
- Execution Handoff with visible launch hints, for example:

```text
Launch via /omagy:team 3:implementer "<approved task>"
Launch via /omagy:ralph "<approved task>"
```

Every matching test spec must include concrete verification, preferably as a
Verification Matrix:

```markdown
| Risk | Check | Type | Expected Result |
|---|---|---|---|
| <what could fail> | <exact command, static inspection, or manual check> | static/manual/unit/integration/e2e/observability | <pass condition> |
```

- Small direct plans should use the matrix instead of placeholder sections.
- Do not write bare `N/A` test sections. If a category is not applicable, omit it from the matrix and include the real check that covers the risk.
- Use fixed Unit / Integration / Regression / Manual sections only when they add real signal for the task.
- Deliberate consensus and high-risk plans must include an expanded test plan covering unit / integration / e2e / observability.

Intermediate drafts are saved to `.omagy/drafts/` through `omagy plan draft`.
Final PRD and test-spec artifacts are saved directly to `.omagy/plans/` with
matching timestamped filenames. `omagy plan complete --input
'{"prd_path":"<new-prd-path>"}' --json` records runtime completion state for
the PRD written in this run.
</Output_Requirements>

<Handoff_Gate>
After recording PRD and test spec, complete the plan state, then verify the
intended handoff before invoking execution:

```bash
omagy plan complete --input '{"prd_path":"<new-prd-path>"}' --json
omagy plan handoff --mode team --input '{"prd_path":"<new-prd-path>"}' --json
omagy plan handoff --mode ralph --input '{"prd_path":"<new-prd-path>"}' --json
```

If the handoff command reports missing or ambiguous launch hints, fix the PRD
markdown file and rerun `omagy plan complete --input
'{"prd_path":"<new-prd-path>"}' --json`. Do not rely on stale or ambient plans.
</Handoff_Gate>

<Tool_Usage>
- Use `omagy explore --prompt "<narrow lookup>" --json` for bounded read-only codebase fact gathering.
- Use `explorer` only when `omagy explore` returns `unsupported_prompt` or the investigation requires richer synthesis.
- Before relying on MCP-backed planning helpers, run `omagy tool-search --input '{"query":"mcp","scope":"all","limit":50}' --json`. This is the Omagy adaptation of omx `ToolSearch("mcp")`; do not pretend agy exposes a literal `ToolSearch` host API. If no suitable MCP tool exists, fall back to the CLI/subagent path; never block planning on optional MCP capability.
- For every `omagy question`, Antigravity native structured prompt, or
  plain-text fallback question, match the user's language. If the user prompt
  is Chinese, ask Chinese planning questions and summarize in Chinese while
  preserving technical names such as `omagy team`, `tmux`, file paths, and
  command snippets.
- Use agy native `invoke_subagent` for the `ask_codex(agent_role=...)` equivalent; persist every lane with `omagy plan record-review`.
- Use `omagy plan draft` for full planner drafts and revisions before final approval.
- Use `analyst` for hidden requirements, edge cases, risk analysis, and direct/interview plans that are not yet crisp.
- Use `planner` for PRD/test-spec drafting on substantial plans.
- Use `plan-architect` for consensus architecture review.
- Use `critic` for consensus critic and review mode.
- Use `/omagy:ai-slop-cleaner` for cleanup/refactor/anti-slop execution plans,
  and use `quality-reviewer` for artifact quality gates or plan review.
- Use `security-reviewer` for auth, secrets, permissions, data exposure, injection, sandbox, plugin, MCP, subprocess, dependency, and compliance risk checks.
- Use `verifier` for PASS/FAIL evidence validation before treating a plan or handoff as complete.
- Consensus mode agent calls must be sequential, never parallel.
- Use `omagy plan record-review` after each analyst/planner/architect/critic lane result and follow the returned `invoke_subagent_tool`.
- Use `omagy plan complete` only after matching `.omagy/plans/prd-*.md` and `.omagy/plans/test-spec-*.md` files exist.
</Tool_Usage>

<Stop_Conditions>
- Stop interviewing only after requirements are clear enough and the user explicitly signaled readiness, or the original prompt already contained sufficient feature direction, scope boundaries, and acceptance criteria. Do not stop solely because the agent invented a plausible direction. A skipped/cancelled/empty readiness prompt is not readiness.
- Stop consensus after 5 Planner/Architect/Critic iterations and present the best version with residual risk.
- Consensus mode outputs the plan by default; with `--interactive`, user can approve and hand off to `/omagy:ralph` or `/omagy:team`.
- If the user says "just do it" or "skip planning" and wants hands-off end-to-end delivery, route to `/omagy:autopilot` when available. Until `/omagy:autopilot` is implemented, record any existing PRD/test-spec and hand off to `/omagy:ralph` by default.
- Use `/omagy:team` for explicit parallel work and `/omagy:ralph` for persistent execution and verification.
- Escalate to the user when irreconcilable tradeoffs require a product or business decision.
- Never make source edits from the planning context.
</Stop_Conditions>

<Final_Checklist>
- [ ] Active plan state started with `omagy plan start`.
- [ ] Plan has concrete acceptance criteria.
- [ ] Plan references specific files/areas where applicable.
- [ ] Small direct plans name the selected implementation choice, scope boundaries, and non-goals.
- [ ] Explicit user cardinality is preserved; same-kind extras were not added without asking or marking them as follow-ups.
- [ ] Risks have mitigations.
- [ ] Test spec includes a Verification Matrix or equally concrete verification steps.
- [ ] No bare `N/A` test sections are used as placeholders.
- [ ] Verification steps are executable, static, observable, or explicitly marked manual.
- [ ] Consensus plans include RALPLAN-DR summary.
- [ ] Consensus final plans include ADR.
- [ ] PRD and matching test spec saved directly under `.omagy/plans/`.
- [ ] No `omagy plan record`, temporary payload file, helper script, or ad hoc wrapper was used to record the plan.
- [ ] Intermediate drafts, if any, recorded with `omagy plan draft`.
- [ ] Interview-mode PRD/test-spec artifacts were created only after at least one user answer, explicit readiness, or a sufficiently scoped original prompt.
- [ ] Agent-suggested directions were confirmed by the user before becoming the selected implementation choice.
- [ ] Secondary capabilities such as drag-and-drop, permissions, notifications, real-time sync, custom columns, audit history, or persistence were either confirmed by the user or kept as optional follow-ups.
- [ ] Parenthetical examples inside question options were not promoted into required acceptance criteria without separate user confirmation.
- [ ] Interview-mode final artifacts were created only after the user signaled readiness or the original prompt was already sufficiently scoped.
- [ ] Skipped, cancelled, empty, timed-out, or non-confirming readiness prompts did not produce final artifacts, `omagy plan complete`, or handoff.
- [ ] Final artifact filenames use the same real current UTC timestamp and were not renamed to invented placeholder timestamps.
- [ ] Pre-existing `.omagy/plans/*` files were not deleted, renamed, or overwritten during planning.
- [ ] `omagy plan complete --input '{"prd_path":"<new-prd-path>"}' --json` ran before `omagy plan handoff --mode <team|ralph> --input '{"prd_path":"<new-prd-path>"}' --json`.
- [ ] Handoff hint resolves with `omagy plan handoff` for the PRD path written in this run.
- [ ] Plan state completed or cancelled.
- [ ] No direct implementation performed in this mode.
</Final_Checklist>

## Scenario Examples

**Good:** The user says `continue` after the workflow already has a clear next
step. Continue the current branch of work instead of restarting or re-asking the
same question.

**Good:** The user changes only the output shape or downstream delivery step,
for example `make a PR`. Preserve earlier non-conflicting workflow constraints
and apply the update locally.

**Bad:** The user says `continue`, and the workflow restarts discovery or stops
before the missing verification or evidence is gathered.

<Examples>
<Good>
Adaptive interview, gathering facts before asking:
```text
Planner: omagy explore --prompt "find authentication implementation" --json
Planner: "I see auth is implemented in src/auth with JWT.
For this feature, should we extend that flow or add a separate auth path?"
```
Why good: The planner answers codebase questions itself, then asks an informed
preference question.
</Good>

<Good>
Single question at a time:
```text
Q1: "What is the main goal?"
A1: "Improve performance"
Q2: "For performance, what matters more: latency or throughput?"
A2: "Latency"
Q3: "For latency, are we optimizing p50 or p99?"
```
Why good: Each question builds on the previous answer.
</Good>

<Bad>
Asking about things Omagy can look up:
```text
Planner: "Where is authentication implemented in your codebase?"
User: "Somewhere in src/auth, I think."
```
Why bad: Use `omagy explore` or an explorer subagent first.
</Bad>

<Bad>
Batching multiple interview questions:
```text
"What is the scope? What is the timeline? Who is the audience?"
```
Why bad: Interview mode asks one focused question per round.
</Bad>

<Bad>
Presenting all design options at once:
```text
"Here are four approaches: Option A... Option B... Option C... Option D..."
```
Why bad: Design-option interviews should be chunked to avoid shallow decisions.
</Bad>

<Bad>
Self-selecting an interview direction:
```text
User: /omagy:plan 做一个团队协作功能
Planner: "I chose Task Board as the feature and wrote the PRD."
```
Why bad: A broad interview request did not receive a user scope answer. The
planner may suggest Task Board as one candidate direction, but must ask the
user to choose or confirm before writing final artifacts.
</Bad>

<Bad>
Upgrading an unconfirmed secondary capability to a requirement:
```text
User: "任务分配与看板管理，固定状态列即可。"
Planner: "The PRD requires drag-and-drop card movement."
```
Why bad: Drag-and-drop is a product affordance and scope decision. Ask whether
card movement should use drag-and-drop or buttons/commands, or keep
drag-and-drop as an optional follow-up.
</Bad>

<Bad>
Treating a parenthetical option example as confirmation:
```text
Planner option: "任务分配与看板管理（例如指派任务、拖拽状态）"
User selects that option, then selects "基本固定状态列".
Planner: "The required PRD includes drag-and-drop and LocalStorage persistence."
```
Why bad: The user confirmed the category and then narrowed scope. Parenthetical
examples are not independent confirmation for drag-and-drop or persistence.
Require explicit confirmation for those affordances, or list them as optional
follow-ups.
</Bad>

<Bad>
Writing final artifacts before readiness:
```text
User: "不需要自定义列。"
Planner: [writes PRD and test spec immediately]
```
Why bad: Interview mode creates the plan when the user signals readiness, such
as "可以生成计划" or "就按这个做". Otherwise summarize the scope and ask whether
to create the plan.
</Bad>

<Bad>
Long chained context gathering:
```bash
omagy plan status --json && omagy memory read --json && omagy artifact list --json && omagy explore --prompt "team" --json
```
Why bad: Planning context must keep evidence sources auditable. Use clear
independent calls so failures and outputs can be attributed to the right step.
</Bad>

<Bad>
Treating skipped readiness as approval:
```text
Planner: "是否可以生成计划？"
User: (skipped)
Planner: [writes PRD and test spec]
```
Why bad: `(skipped)` is not approval. Continue interviewing or cancel the active
plan state; never write final artifacts or run handoff from a skipped readiness
prompt.
</Bad>

<Bad>
Inventing a fixed artifact timestamp:
```bash
date -u +"%Y%m%dT%H%M%SZ"
mv .omagy/plans/prd-20260523T042417Z-task.md .omagy/plans/prd-20260524T000000Z-task.md
```
Why bad: Plan artifact names must use the same real current UTC timestamp for
the PRD and test spec. Do not rename files to placeholder timestamps.
</Bad>

<Bad>
Handoff before completed state:
```bash
omagy plan handoff --mode team --json
omagy plan complete --json
```
Why bad: Handoff must be resolved from a completed PRD/test-spec pair, not an
incomplete active plan.
</Bad>

<Bad>
Deleting older plan artifacts so the current plan becomes "latest":
```bash
rm .omagy/plans/prd-20260523T114500Z-team-task-board.md
rm .omagy/plans/test-spec-20260523T114500Z-team-task-board.md
omagy plan complete --json
```
Why bad: Plan artifacts are append-only. Always complete and hand off the exact
PRD written in this run by passing `prd_path`; never delete or rename old plans
to influence latest-plan selection.
</Bad>
</Examples>

<Advanced>
## Design Option Presentation

When presenting design choices during interviews, chunk them:

1. Overview in 2-3 sentences.
2. Option A with tradeoffs.
3. Wait for user reaction.
4. Option B with tradeoffs.
5. Wait for user reaction.
6. Recommendation only after options are discussed.

Format each option:
```text
### Option A: <name>
Approach: <one sentence>
Pros: <bullets>
Cons: <bullets>

What is your reaction to this approach?
```

## Question Classification

Before asking any interview question, classify it:

| Type | Examples | Action |
|------|----------|--------|
| Codebase Fact | "What patterns exist?", "Where is X?" | Explore first; do not ask the user |
| User Preference | "Priority?", "Timeline?" | Ask through `omagy question` or native structured input |
| Scope Decision | "Include feature Y?" | Ask the user |
| Cardinality Decision | "Add one README badge" but considering two or more badges | Preserve the requested count in direct mode; ask before expanding in interactive/interview mode |
| Requirement | "Performance constraints?" | Ask the user |

## Review Quality Criteria

| Criterion | Standard |
|-----------|----------|
| Clarity | 80%+ repository-fact claims cite file/line evidence |
| Testability | 90%+ acceptance criteria are concrete |
| Verification | All file references exist or are clearly marked as planned new files |
| Specificity | No vague terms without metrics or pass/fail language |

## Deprecation Notice

`/omagy:ralplan` is an alias for `/omagy:plan --consensus`. Prefer
`/omagy:plan` for interview, direct, consensus, and review planning workflows.
</Advanced>
