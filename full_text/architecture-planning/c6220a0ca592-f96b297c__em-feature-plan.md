---
name: em-feature-plan
description: Use when planning a non-trivial feature for multi-engineer parallel implementation via EM-led peer-debate planning. Translates requirements into a complete planning bundle at docs/<feature-slug>/ (README, planning, tasks, engineer-N-tasks, engineering-standards, and optionally allocations.md) by dispatching 2 max-effort senior-engineer subagents in parallel (default biases - Pragmatism vs Rigor), running a bounded peer debate (≤ 2 rounds, EM-orchestrated alternating turns), handing the result to a max-effort staff-engineer subagent for adjudication + task decomposition, and optionally allocating engineer slots to named team members (Phase 7, only when a team roster is provided in Phase 3). Sits alongside em-ship-feature in the em-* family — em-feature-plan plans, em-ship-feature ships. Implicit triggers - "plan this feature", "two engineers debate this design", "EM plan this", "split this across the team with debate", "act as engineering manager to plan this feature", "plan and allocate this feature to my team". Composes with team-brainstorm upstream and em-ship-feature downstream.
---

# em-feature-plan — EM-led Peer-Debate Feature Planning

Turn a feature request into a complete planning bundle — architecture, plan, task DAG, per-engineer task packets, engineering standards, and a wrap-up README — via an **Engineering Manager orchestrator** that dispatches **two max-effort senior-engineer subagents in parallel** (default biases: Pragmatism vs Rigor), runs a **bounded peer debate** between them (≤ 2 rounds, EM-orchestrated alternating turns), and hands the result to a **max-effort staff-engineer subagent** that adjudicates, decomposes tasks, and assembles the standards file.

The skill is the **planning counterpart** to `em-ship-feature` in the `em-*` family. Where `em-ship-feature` ships an already-planned feature, `em-feature-plan` produces the plan that `em-ship-feature` consumes. Together they form an end-to-end pipeline: `team-brainstorm` (optional) → `em-feature-plan` → `em-ship-feature`.

It is also a *different shape* than `team-feature-plan`: where `team-feature-plan` is architect-critique (one author, three specialist critics), `em-feature-plan` is peer-debate (two independent authors, debate to consensus, single max-effort adjudicator). Both shapes coexist; the user picks based on which lens fits the feature better.

**Violating the letter of the rules is violating the spirit of the rules.** No exceptions, no rationalizations.

---

## When to Use / Skip

**Use** for:
- Any non-trivial feature implementation that more than one engineer will touch.
- Any feature spanning more than one module or layer.
- Any feature requiring a new domain concept, aggregate, or major architectural decision.
- Any feature where peer-debate (two independent designs argued to consensus) is a better fit than architect-critique (one design with multiple lenses).
- Features where the team-shipping concerns (headcount, hand-offs, calendar trade-offs) deserve as much weight as the architectural concerns.

**Skip** for:
- Typo fixes, single-line behavior tweaks, refactors with no design surface.
- Single-engineer single-day work.
- Features where architectural rigor matters more than peer disagreement — `team-feature-plan` is the right shape there.
- Throwaway scripts / spikes.

---

## Activation

Invoked in two ways:

1. **Explicit slash command:** `/superdev:em-feature-plan [feature-name-or-description]`
2. **Implicit triggers** — user messages matching any of: "plan this feature", "two engineers debate this design", "EM plan this feature", "act as engineering manager to plan this", "split this across the team with debate", "peer-review this design".

**Pipeline composition:**

```
team-brainstorm (optional)  →  em-feature-plan  →  em-ship-feature  (autonomous downstream)
                                              OR
                                              →  /superdev:superdev per engineer packet  (interactive downstream)
```

`em-feature-plan` accepts requirements input from any of:
- A brainstorm doc at `docs/brainstorm/*<feature>*.md` (typical `team-brainstorm` output).
- A spec / PRD / Linear or Jira ticket (file path or pasted text).
- The user's own restatement.

The output at `docs/<feature-slug>/` is consumed by either `em-ship-feature` (autonomous shipping) or by per-engineer `/superdev:superdev` invocations (interactive shipping).

---

## Hard Gates (cannot be skipped)

1. **Effort = max.** If `/effort max` is not active, instruct the user to run it once, then halt. Reason: this skill dispatches 4-8 senior subagent calls and 1-2 staff calls, all `model: opus`. The main thread also needs max-effort reasoning to orchestrate peer debate cleanly.

2. **Requirements input is bounded.** Phase 1 must produce a concrete, restated requirements list (the R-list) — pulled from a brainstorm doc, a spec, a Linear/Jira ticket, or the user's own text. "Plan a new feature" without scope is not a valid input — clarify first.

3. **Codebase grounded before design.** Phase 2 reads CLAUDE.md, AGENTS.md, and any architecture / layering / DI / test-harness documentation **in parallel, in ONE message**. Designing in ignorance of the codebase's conventions is a workflow failure.

4. **Every requirement validated against the existing system.** Phase 2 maps each requirement to one of `{exists, partial, greenfield}` with the integration point named. "We'll figure it out later" is not a valid mapping.

5. **Clarifying questions surfaced BEFORE Phase 4.** Phase 3 is the only phase where the user is asked design questions; ambiguities discovered later become Open Questions in `planning.md`, not silent picks.

6. **Both senior subagents dispatched in parallel.** Phase 4 is **ONE message with two `Agent` calls**. Sequential dispatch is a workflow failure (Phase 4 is the foundation of the peer-debate shape — sequential dispatch defeats the parallel-generation principle).

7. **Senior A + Senior B + Staff engineer subagents all = `model: opus`.** Every dispatch in Phases 4, 5, 6 explicitly sets `model: opus`. Non-negotiable — under-powered planners and adjudicators degrade the entire pipeline's ceiling. Independent drafting quality is the ceiling for the whole pipeline; debate and adjudication can only choose between (or refine) what was actually generated.

8. **Bounded debate: ≤ 2 rounds in Phase 5, ≤ 1 follow-up in Phase 6.** Never unbounded recovery. If convergence isn't reached after the cap, both plans persist and the staff engineer adjudicates with full debate transcript.

9. **README.md written LAST.** Phase 8 writes files in the order `planning.md` → `tasks.md` → `engineer-*-tasks.md` → `engineering-standards.md` → `allocations.md` (only if Phase 7 ran) → `README.md`. Writing the README first tends to under-spec the other files; writing it last is a forcing function for completeness across the full document set.

10. **EM is the only dispatcher. Subagents must NEVER be told to dispatch other subagents.** This runtime exposes the `Agent` tool only to the main thread; general-purpose subagents have `TaskCreate`/`Update` but not `Agent`. **Phase 5's "alternating turns" debate is EM-orchestrated** — the EM re-dispatches Senior A with Senior B's latest content, then Senior B with Senior A's latest content, accumulating the debate transcript in EM working memory. **Phase 6's "follow-up round" is also EM-orchestrated** — if the staff engineer's first dispatch includes follow-up questions for either senior, the EM dispatches them, captures the response, and re-dispatches the staff with the answers appended. Telling a senior subagent to "now dispatch the other engineer" will fail with no Agent tool available. This gate is what makes the peer-debate pipeline actually work in this runtime.

11. **The artifacts at `docs/<feature-slug>/` are the single authoritative output.** Conversation-only summaries are addenda; the 5+ markdown files are what the team and any downstream `em-ship-feature` or `superdev:superdev` invocation work from.

**Spirit:** violating the letter of these rules is violating the spirit of the rules. No exceptions, no rationalizations.

---

## Workflow

7 phases — Phases 1 (input) and 3 (clarifying questions) are interactive with the user; Phases 0, 2, 4, 5, 6, 7 are autonomous.

| # | Phase | Owner | What happens |
|---|---|---|---|
| 0 | **Bootstrap** | EM (main thread, talks to user) | `/effort max` check · bias-pair selection (`AskUserQuestion`) |
| 1 | **Input Acquisition & Feature Slug** | EM (with user) | Accept requirements input (brainstorm doc / spec / ticket / text) · slugify feature name · produce R-list |
| 2 | **Codebase Grounding & Requirement Validation** | EM, parallel reads in ONE message | Detect platform/layering/DI/tests · per-requirement validation table |
| 3 | **Clarifying Questions** | EM ↔ user | Bundle Blocker + High-signal questions via `AskUserQuestion` · low-signal logged as Open Questions |
| 4 | **Parallel Drafting** | EM dispatches 2 senior subagents in ONE message | Each engineer returns a FULL plan with their bias |
| 5 | **Peer Debate (EM-orchestrated)** | EM re-dispatches each senior with the other's content, alternating | ≤ 2 rounds — round 1 = critique, round 2 = response. Converged → Reconciled Plan. Diverged → Plan A / Plan B + transcript. |
| 6 | **Staff-Engineer Review & Adjudication** | EM dispatches 1 staff subagent (+1 follow-up round if requested) | Adjudicates · decomposes tasks · assembles standards · writes debate provenance |
| 7 | **Allocate** (optional — only runs if team roster provided in Phase 3) | EM dispatches 1 staff subagent | Matches engineer slots → real team members based on skill fit · level · capacity · produces `allocations.md` with rationale + risk callouts |
| 8 | **Write Artifacts** | EM (main thread) | Write `planning.md` → `tasks.md` → `engineer-*-tasks.md` → `engineering-standards.md` → `allocations.md` (if Phase 7 ran) → `README.md` (LAST per Hard Gate #9) |

---

## Phase 0 — Bootstrap

### Step 0.1 — Effort gate

If `/effort max` is not active, halt with the copy-paste fix:

```
This skill requires /effort max. Run:

  /effort max

Then re-invoke /superdev:em-feature-plan <feature>.
```

The skill cannot programmatically detect the effort setting; trust-but-verify via the user. (Same approach `em-ship-feature` uses for its hard gates.)

### Step 0.2 — Bias pair selection

```
AskUserQuestion(questions: [
  {
    question: "Which bias pair should the two senior engineers use during Phase 4 drafting?",
    header: "Bias pair",
    multiSelect: false,
    options: [
      { label: "Pragmatism vs Rigor (Recommended default)", description: "Senior A: 'Simpler is better. YAGNI. Ship the smallest correct thing. Reuse what exists. Bias to fewer abstractions, fewer new modules.' Senior B: 'Correctness and resilience first. Anticipate edge cases, define invariants, model the domain explicitly. Bias to explicit types, explicit error categories, avoiding future regret.'" },
      { label: "Speed vs Quality", description: "Senior A: 'Ship in 1-2 sprints, cut scope before complexity, prefer flags + iteration.' Senior B: 'Long-term maintainability, durable abstractions, slower initial pace is acceptable.'" },
      { label: "Greenfield vs Reuse", description: "Senior A: 'Build it new — existing modules carry baggage.' Senior B: 'Extend what exists — new modules carry hidden cost (DI, tests, ownership).'" }
    ]
  }
])
```

Store the user's choice as `bias_pair`. Each pair has two bias prompts; the EM uses them in Phase 4 dispatch prompts.

### Step 0.3 — Transition

Print to user:

```
Bootstrap complete. Bias pair: <chosen>. Proceeding to Phase 1.
```

---

## Phase 1 — Input Acquisition & Feature Slug

### Step 1.1 — Restate the feature in one sentence

Read what the user provided (the slash-command argument, or any pasted text in the message). If only a feature name was given (e.g. "OAuth Google sign-in"), ask the user one focused question via plain chat (NOT `AskUserQuestion` — this is a brief acknowledgment, not a structured choice): "Restated as: 'Add Google sign-in to the OAuth flow.' Confirm or correct."

### Step 1.2 — Acquire the requirements input

Accept any of:
- A brainstorm document at `docs/brainstorm/<date>-<feature>.md`.
- A spec / PRD / Linear or Jira ticket (file path the user provides, or pasted text in the user's message).
- The user's own restatement in chat.

If a brainstorm doc exists and the user pointed at it, Read it via the Read tool. If a file path is provided, Read it. Otherwise use the chat content.

### Step 1.3 — Slugify the feature name

Lowercase, hyphenated, no spaces. Examples: `inventory-rebalance`, `oauth-google-signin`, `payments-stripe-integration`.

If a brainstorm doc exists, reuse its slug. Confirm the slug with the user before continuing:

```
Slug for this feature: <slug>. Artifacts will be written to docs/<slug>/. Confirm or override.
```

### Step 1.4 — Restated requirements list (the R-list)

Convert the input into a numbered list of crisp, atomic requirements:

```
R1: <one-sentence testable requirement referring to a concrete user-visible behavior or system invariant>
R2: <...>
R3: <...>
...
```

Each requirement is one sentence, testable, refers to a concrete user-visible behavior or system invariant. Compound requirements get split into atoms.

**Output of Phase 1:** the R-list — saved in EM working memory; the spine of every downstream phase.

---

## Phase 2 — Codebase Grounding & Requirement Validation

### Step 2.1 — Parallel reads (ONE message)

Issue ALL of the following as parallel `Read` calls in ONE message — designing without knowing the codebase's layering, DI pattern, error model, and test harness is the most common planning failure:

- Project standards: `CLAUDE.md`, `AGENTS.md`, any root-level architecture docs, `README.md` (architecture sections only).
- Layering / dependency rules: `ARCHITECTURE.md`, `LAYERING.md`, hex/clean-arch docs (whichever exist).
- DI / IoC convention: search for the project's DI container, factory pattern, or constructor-injection style (use Grep/Glob if filenames aren't known).
- Test harness: test framework, runner, mocking convention, integration vs unit split, fixture/factory pattern.
- Error model: project's error hierarchy, result type, error-mapping convention at layer boundaries.
- 3-5 representative existing modules whose layering / style the seniors will mirror.

### Step 2.2 — Detect platform + conventions

From the reads, identify:

- **Platform(s)** — Android / iOS / web / backend / multi.
- **Language(s) and framework(s)**.
- **Layering convention** — strict Clean Architecture? Hexagonal? Layered MVC? CQRS? Pure DDD? Document which one and what the dependency direction looks like.
- **DI mechanism** — constructor injection? Hilt? Dagger? Koin? Spring? `tower::Layer`? Manual factories?
- **Interface convention** — trait? abstract class? protocol? interface?
- **Test convention** — TDD-aligned? test-after? property-based? snapshot?

### Step 2.3 — Per-requirement validation table

For each R in the R-list, classify:

| Class | Meaning | What to record |
|---|---|---|
| `exists` | The capability is already in the codebase. | Name the module / function / endpoint. |
| `partial` | Some of the capability exists; gaps must be filled. | Name what exists + what gap. |
| `greenfield` | None of it exists; new code required. | Name the module(s) that will be new. |

**Edge cases** (per requirement): empty state, error state, slow network, no network, permission denied, expired session, large data, pagination boundary, concurrent updates, race conditions, idempotency violation, stale cache, time-zone, i18n, accessibility, dark mode, offline.

**Bottlenecks** (per requirement): DB hot spots, N+1 queries, large payloads, lock contention, scheduler thundering herd, rate-limit boundaries, third-party SLA, cache invalidation, schema migration cost.

### Step 2.4 — Outputs

- **Grounding Note** — ≤ 10 bullets covering platform, frameworks, layering, DI, errors, test harness, naming conventions.
- **Validation Table** — one row per requirement: `R# | class | integration point | edge cases | bottlenecks`.

Both saved in EM working memory; passed into every Phase 4 + Phase 6 dispatch.

---

## Phase 3 — Clarifying Questions

**The only phase where the user is asked design questions.** Surface every ambiguity now, before Phase 4.

### Step 3.1 — Categorize ambiguities

For every ambiguity discovered in Phase 1 or Phase 2:

- **Blocker** — architecture-changing; must be resolved before drafting can start.
- **High-signal** — the answer materially alters the plan shape.
- **Low-signal** — log as Open Question with a recommended default; do NOT pause the pipeline.

### Step 3.2 — Bundle and ask Blocker + High-signal questions

Use `AskUserQuestion`. Up to 4 questions per call; if more than 4 questions need answers, make MULTIPLE `AskUserQuestion` calls — but ALL Phase 3 questions must complete before Phase 4 starts.

Example categories of questions:

- **Scope:** out-of-scope items, MVP cut, future-phase items.
- **Data model:** identity / authority / source-of-truth for shared data.
- **Concurrency & consistency:** strong vs eventual, transactional boundaries, ordering guarantees.
- **Failure semantics:** retry policy, idempotency keys, dead-letter behavior, partial-failure handling.
- **Observability:** metrics, logs, tracing needs.
- **Performance targets:** latency budget, throughput targets, RPO/RTO.
- **Security & privacy:** PII handling, audit trail, authz boundaries.

### Step 3.3 — Ask for team roster (for optional Phase 7 Allocation)

Before exiting Phase 3, ask the user whether to enable Phase 7 (Allocate). This is a separate `AskUserQuestion` call AFTER the Blocker/High-signal bundle:

```
AskUserQuestion(questions: [
  {
    question: "Do you want Phase 7 (Allocate) to map engineer slots to specific team members? Requires a team roster (name, level, skills, capacity).",
    header: "Allocation",
    multiSelect: false,
    options: [
      { label: "Yes — paste the roster now", description: "After this question, you'll paste a team roster in chat. Format: one entry per engineer with name, level (Senior/Mid/Junior), skills (list), and capacity_this_feature (0.0-1.0). Phase 7 will use it to produce allocations.md." },
      { label: "Yes — read from docs/team-roster.md", description: "Skill will read the roster from docs/team-roster.md if it exists. If the file is missing, skill will fall back to asking you to paste the roster." },
      { label: "Skip allocation — produce slot-based packets only (current default)", description: "Phase 7 is skipped. Output is engineer-N-tasks.md as today. Use this for solo planning, when team composition isn't known yet, or when you'll allocate manually later." }
    ]
  }
])
```

If user picks "paste the roster now": follow up with a brief chat message ("Paste the team roster now (any format with name + level + skills + capacity per person)") and capture their next message into `team_roster`. If user picks "read from docs/team-roster.md": `Read` that file; if it doesn't exist, fall back to the paste flow.

Store the result as `team_roster` (or null if "Skip allocation" was chosen). This drives whether Phase 7 runs.

### Step 3.4 — Outputs

- **Answered-Questions Note** — the user's answers to Blocker + High-signal questions.
- **Open-Questions list** — low-signal items with recommended defaults; written into `planning.md` in Phase 8 so engineers see them with recommendations.
- **`team_roster`** (optional, set if user opted into Phase 7).

---

## Phase 4 — Parallel Drafting

**Hard Gate #6:** ONE message with two `Agent` calls. Sequential dispatch defeats parallel generation.

### Dispatch template

The EM dispatches both seniors in one message. Each receives the same Phase 1+2+3 outputs, plus their assigned bias from `bias_pair`.

```
# Dispatched together (one message, two Agent calls):

Agent(
  description: "Senior A (<bias A name>) — Phase 4 draft",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
feature_slug: <slug>
bias: <bias_pair.A.name>   # e.g. "Pragmatism"

You are Senior Engineer A for the planning of <feature-slug>. Your bias for this work is:

<bias_pair.A.prompt verbatim>   # e.g. "Simpler is better. YAGNI. Ship the smallest correct thing..."

You are working in parallel with Senior Engineer B (who has the opposite bias). You will NOT see B's plan until Phase 5. Your output is ONLY your plan, no commentary about B.

REQUIREMENTS (R-list from Phase 1):
<paste verbatim>

GROUNDING (Phase 2 Grounding Note):
<paste verbatim>

VALIDATION TABLE (Phase 2):
<paste verbatim>

ANSWERED QUESTIONS (Phase 3):
<paste verbatim>

OPEN QUESTIONS (Phase 3, with recommended defaults):
<paste verbatim>

Produce your plan in this exact format and return it as your final output:

## Plan
### 1. Architecture summary
<modules · aggregates · ports · data flow>
### 2. Per-requirement implementation sketch
<R1 → how I would build this; R2 → ...; one entry per R from the R-list>
### 3. Test strategy
<unit / integration / e2e coverage choices>
### 4. Sequencing proposal
<what comes first, what blocks what; identify Foundation candidates>
### 5. Risks + mitigations
### 6. Recommended team headcount + rationale
<my view; staff engineer reconciles in Phase 6>
### 7. Three things I explicitly chose NOT to do, and why
<the deferred items + reasoning>

That's it. Return ONLY the plan. Do NOT dispatch other subagents (you can't — only the EM can). Do NOT debate with Senior B in this dispatch (that happens in Phase 5, EM-orchestrated).
"""
)

Agent(
  description: "Senior B (<bias B name>) — Phase 4 draft",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
<same template as A, with B's bias prompt swapped in>
"""
)
```

EM captures both plans into working memory as `plan_a` and `plan_b`.

---

## Phase 5 — Peer Debate (EM-orchestrated alternating turns)

**Hard Gate #10** makes this phase EM-orchestrated: each "turn" is a fresh EM-initiated Agent dispatch; subagents do not dispatch each other. Hard Gate #8 caps the debate at 2 rounds.

### Round 1 — each engineer critiques the other

Two sequential dispatches (one per engineer). Order doesn't matter; do them one at a time for clean EM state tracking.

#### Senior A critiques B

```
Agent(
  description: "Senior A — Round 1 critique of B",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
feature_slug: <slug>
bias: <bias_pair.A.name>

You are Senior Engineer A. You produced YOUR plan in Phase 4 (shown below for context). Senior Engineer B (opposite bias) produced THEIR plan, also shown below. The EM dispatched you for Round 1 of the peer debate.

Your job: read B's plan and return your top 3-5 DISAGREEMENTS with rationale. Each disagreement is a specific point where B's approach is wrong or suboptimal, with WHY citing your bias and concrete evidence (file paths, architectural patterns, requirements, edge cases B missed).

YOUR PLAN (Phase 4):
<plan_a verbatim>

B's PLAN (Phase 4):
<plan_b verbatim>

Return ONLY a list in this format:

## Round 1 Critique of B
1. **Disagreement:** <one-line statement of the issue with B's approach>
   **Rationale:** <why I think this is wrong, citing my bias and evidence>
2. ...

If you find FEWER than 3 substantive disagreements (i.e. you mostly converge with B), say so explicitly at the END:
  "CONVERGED: I have fewer than 3 substantive disagreements with B's plan."
The EM uses this signal to skip Round 2.

Do NOT dispatch other subagents (you can't — only the EM can). Do NOT try to "talk to B directly" — the EM is the only entity that sees both sides; you only respond when re-dispatched.
"""
)
```

#### Senior B critiques A

```
Agent(
  description: "Senior B — Round 1 critique of A",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
<mirror of A's prompt: B's bias, B's plan as 'YOUR PLAN', A's plan as 'A's PLAN', return 'Round 1 Critique of A' in same format>
"""
)
```

EM aggregates: `round1_critique_of_a_by_b`, `round1_critique_of_b_by_a`, `round1_a_converged?`, `round1_b_converged?`.

**Skip Round 2 if** both engineers self-reported CONVERGED. Otherwise continue.

### Round 2 — each engineer responds to the other's critique

Same dispatch pattern, both engineers respond to the OTHER's Round 1 critique.

#### Senior A's Round 2 response

```
Agent(
  description: "Senior A — Round 2 response",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
feature_slug: <slug>
bias: <bias_pair.A.name>

You are Senior Engineer A. Round 1 of peer debate completed. Below is YOUR Phase 4 plan, B's Phase 4 plan, B's Round 1 critique of you, AND your Round 1 critique of B.

Your job: respond to each of B's Round 1 disagreements with your plan. For each:
  - If B is right → CONCEDE and update your plan accordingly.
  - If B is wrong → write a counter-argument citing evidence.
  - If partially right → CONCEDE the valid part, push back on the rest.

YOUR PLAN (Phase 4):
<plan_a verbatim>

B's PLAN (Phase 4):
<plan_b verbatim>

B's ROUND 1 CRITIQUE OF YOU:
<round1_critique_of_a_by_b verbatim>

YOUR ROUND 1 CRITIQUE OF B (for context — you don't respond to your own critique here):
<round1_critique_of_b_by_a verbatim>

Return in this format:

## Round 2 Response to B's Critique
1. **B's critique:** <quote one of B's round-1 disagreement points>
   **My response:** CONCEDE / REJECT / PARTIAL — <rationale>
2. ...

## My updated plan (post-debate, with concessions applied)
<inline the FULL updated plan, in the same format as Phase 4 — this is your FINAL plan for the staff engineer to consider>

## Convergence signal
CONVERGED: yes (with B's plan / with a synthesis) | DIVERGED: <list of irreconcilable points>

Do NOT dispatch other subagents (you can't — only the EM can). Do NOT try to "talk to B directly" — return your response in the format above; the EM relays it to B (or to the staff engineer if Phase 6 starts).
"""
)
```

#### Senior B's Round 2 response

```
Agent(
  description: "Senior B — Round 2 response",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """<mirror of A's Round 2 prompt with A and B swapped>"""
)
```

EM aggregates: `final_plan_a`, `final_plan_b`, `a_converged?`, `b_converged?`, full `debate_transcript`.

### EM decides outcome

```
if (round1_a_converged AND round1_b_converged) OR (a_converged AND b_converged):
    outcome = "Reconciled Plan"
    reconciled_plan = <EM synthesizes the two final plans, applying both engineers' concessions>
    # Optional: EM may dispatch ONE engineer (Senior A by default) with a "produce the reconciled
    # plan" prompt if the synthesis is non-trivial. Skip this dispatch if EM can do it inline.

else:
    outcome = "Diverged"
    # Both final_plan_a and final_plan_b persist verbatim
    # logged_disagreements = <list of unresolved points from round 2>
    # The staff engineer (Phase 6) adjudicates
```

**Phase 5 produces:** `debate_transcript` (all rounds verbatim), `outcome` (`Reconciled` or `Diverged`), `final_plan_a`, `final_plan_b`, and if Reconciled: `reconciled_plan`.

---

## Phase 6 — Staff-Engineer Review, Adjudication & Task Decomposition

**Hard Gate #7:** staff engineer subagent dispatched with `model: opus`, non-negotiable.

### First staff dispatch

```
Agent(
  description: "Staff engineer — adjudicate + decompose",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
feature_slug: <slug>

You are the STAFF ENGINEER. The EM dispatched you to:
  1. Adjudicate the peer debate (pick Plan A, pick Plan B, or synthesize a third option).
  2. Decompose the chosen plan into a Foundation Sprint task list + Parallel Frontiers task list + per-engineer task packets.
  3. Assemble the engineering-standards.md content (inherited from Phase 2 grounding + your feature-specific commitments).
  4. Write a 1-paragraph debate provenance summary for planning.md.

You have authority to override either engineer on any specific point with written rationale.

If you need ONE follow-up debate round with either engineer (Hard Gate #8: cap of 1 follow-up), include a "Follow-up questions" section at the END of your output — the EM will dispatch them with your specific questions, capture the response, and re-dispatch you with the answers appended.

INPUTS:

R-list (Phase 1):
<paste verbatim>

Grounding Note + Validation Table (Phase 2):
<paste verbatim>

Answered + Open Questions (Phase 3):
<paste verbatim>

Senior A's final plan (post-debate):
<final_plan_a>

Senior B's final plan (post-debate):
<final_plan_b>

Peer debate transcript:
<debate_transcript>

Outcome: <"Reconciled Plan" | "Diverged">
Reconciled plan (if outcome=Reconciled):
<reconciled_plan, or "N/A">

PRODUCE all outputs in one response, in this order:

## 1. Final adjudicated plan
<the version that becomes planning.md's substantive plan section — full architecture, sequencing rationale, risks, test strategy, definition of done>

## 2. Foundation Sprint task list
<senior-only tasks that establish shared interfaces — ports + traits, DI wiring, shared error model, test harness, CI scaffolding (as applicable). These run sequentially in em-ship-feature Phase 1.>

## 3. Parallel Frontiers task list
<engineer-claimable tasks with: ID, owner-engineer-slot, dependencies, acceptance criteria, TDD red list, owned vs consumed interfaces, files to touch.>
<Include a DAG visualization (ASCII tree showing dependencies).>
<Include the conflict rule at the top: "two tasks owned by different engineers may not write to the same module.">

## 4. Per-engineer task packets
### Engineer 1 packet
<ordered, self-contained — an engineer reading ONLY this packet should be able to start work without opening other files>
### Engineer 2 packet
<...>
### ... (one per recommended engineer slot, where N = your recommended headcount based on max DAG frontier width)

## 5. Engineering-standards content
### Inherited from codebase
<bullets distilled from the Phase 2 grounding note — naming, layering, DI, errors, tests, conventions>
### Feature-specific commitments
<new aggregate names, new port/trait names, new error types introduced, feature flag name (if any), coverage floor, migration approach, any other team-level pledge for this feature>

## 6. Debate provenance summary (1 paragraph for planning.md)
<what was debated, what each engineer argued, why the current path was chosen>

## (Optional) Follow-up questions
If you need ONE follow-up round (Hard Gate #8), list specific questions here:
### For Senior A: <questions, or omit if none>
### For Senior B: <questions, or omit if none>
If no follow-up needed, omit this section entirely.
"""
)
```

### EM-orchestrated follow-up (only if staff requested it)

If the staff engineer's first response includes a "Follow-up questions" section:

1. Dispatch Senior A and/or Senior B with the staff's questions:

```
Agent(
  description: "Senior A — staff follow-up",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
feature_slug: <slug>
bias: <bias_pair.A.name>

You are Senior Engineer A. The STAFF ENGINEER (reviewing the peer debate) has a follow-up question for you before finalizing the adjudication.

YOUR PLAN (Phase 4):
<plan_a verbatim>

YOUR FINAL PLAN (post-debate):
<final_plan_a verbatim>

STAFF'S FOLLOW-UP QUESTION(S):
<staff's "For Senior A:" section, verbatim>

Answer the staff's questions specifically and briefly. Cite evidence (file paths, requirements, your prior debate position). Do NOT re-litigate the entire debate — just answer the specific questions.

Return:

## Response to staff follow-up
<your answers>
"""
)
```

(Mirror for Senior B if questions exist for B.)

2. Capture the senior responses; re-dispatch staff with the answers appended:

```
Agent(
  description: "Staff engineer — final adjudication (post-follow-up)",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
<same prompt as first staff dispatch, PLUS:>

PRIOR STAFF OUTPUT (your previous response):
<first staff response verbatim>

SENIOR A's RESPONSE TO YOUR FOLLOW-UP:
<senior A's response, or "no questions for A">

SENIOR B's RESPONSE TO YOUR FOLLOW-UP:
<senior B's response, or "no questions for B">

Produce the FINAL adjudicated outputs in the same 6-section format. This is your second and FINAL dispatch — Hard Gate #8 caps you at one follow-up round. No more rounds regardless of remaining ambiguity.
"""
)
```

The second staff dispatch's output IS the final adjudication regardless of any remaining ambiguity.

**Phase 6 produces:** the 6 staff outputs (final plan, foundation tasks, frontier tasks, per-engineer packets, engineering standards, debate provenance) — ready for Phase 7 (Allocate, if team roster provided) or directly Phase 8 (Write Artifacts) if allocation was skipped.

---

## Phase 7 — Allocate (optional)

**Skip entirely if `team_roster` is null** (user picked "Skip allocation" in Phase 3). Proceed directly to Phase 8.

If `team_roster` was provided, the EM dispatches the staff engineer a second time to match per-engineer packets to real team members.

### Why a separate phase (not folded into Phase 6)

Phase 6 decomposes the plan into slot-based packets (`engineer-1`, `engineer-2`, …). Allocation is a separate judgment call: which packet best fits which team member's skills, level, and capacity? Separating them:
- Keeps Phase 6's staff dispatch focused on decomposition.
- Lets allocation be optional (no roster → skip cleanly).
- Produces a single-purpose `allocations.md` artifact that can be updated when team composition changes WITHOUT rewriting the rest of the planning bundle.
- Mirrors em-ship-feature's pattern of one focused staff-engineer dispatch per concern.

### Staff dispatch template

```
Agent(
  description: "Staff engineer — allocate packets to engineers",
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
repo: /Users/eslam/linkify/<repo-name>
feature_slug: <slug>

You are the STAFF ENGINEER, dispatched a second time (after Phase 6's decomposition) to ALLOCATE the per-engineer packets to specific team members based on the team roster.

INPUTS:

Per-engineer packets (from Phase 6 Output #4):
### Engineer 1 packet
<paste content from Phase 6's "Engineer 1 packet" section verbatim>
### Engineer 2 packet
<...>
### Engineer N packet
<...>

Foundation Sprint task list (from Phase 6 Output #2):
<paste verbatim — context for Foundation-vs-Frontier work distribution>

Parallel Frontiers task list (from Phase 6 Output #3):
<paste verbatim — context for skill-match decisions>

Team roster (from Phase 3):
<paste team_roster verbatim — entries with name, level, skills, capacity_this_feature, notes>

PRODUCE the allocation document in this exact format and return it as your final output:

## Slot → Engineer mapping

For each engineer-N packet, assign the best-fit team member. Order rows by slot ID:

| Slot | Engineer | Level | Capacity | Skill match | Rationale |
|---|---|---|---|---|---|
| engineer-1 | <name> | <level> | <0.0-1.0> | Strong / Partial / Weak | <one-line: why this assignment, citing skill overlap and capacity fit> |
| engineer-2 | <name> | <level> | <0.0-1.0> | <...> | <...> |
| engineer-N | <name> | <level> | <0.0-1.0> | <...> | <...> |

## Risk callouts

List any of:
- **Overallocation:** "<name> is <X> capacity but engineer-N's packet has ~<Y> work-units. Recommendation: <de-scope task T-Z / extend timeline by N sprints / split packet>."
- **Skill gaps:** "No team member has <skill X>. engineer-N requires it. Recommendation: <spike time / pair with senior / bring in contractor>."
- **Seniority mismatch:** "engineer-N has senior-level architectural work (<task IDs>) but assigned <Mid/Junior name>. Recommendation: <pair with senior on those tasks / reassign packet>."
- **Dependency/timeline conflicts:** "<name> is assigned engineer-N (depends on Foundation F-1) but also assigned engineer-M (Foundation owner). They'll be blocked on themselves. Recommendation: <swap one packet / sequence sprints>."

If no risks, write "None identified."

## Unallocated capacity

List team members from the roster NOT assigned to any packet, with their free capacity. Format:
- <name> (<level>, <capacity> free) — available for stretch work, code review, or out-of-feature commitments.

If everyone is allocated, write "None — all team members assigned."

## Recommendations

Optional. Use this section if you think the EM should consider headcount or scope changes:
- Add a team member (specify skill profile needed).
- De-scope a packet (specify which tasks and why).
- Extend timeline (specify which packets and by how much).
- Pair up specific engineers on specific tasks (justify the pairing).

If no recommendations, omit this section entirely.

That's it. Return ONLY the allocation document in the format above. Do NOT dispatch other subagents (you can't — only the EM can). Do NOT modify the per-engineer packets themselves (Phase 6 already finalized them; this phase is metadata).
"""
)
```

The staff engineer's response becomes the body of `docs/<feature-slug>/allocations.md` — Phase 8 writes it verbatim with a small header (feature slug, date, source).

### EM-side post-processing

After the staff returns, the EM:
1. Captures the allocation document into working memory as `allocations_body`.
2. If "Risk callouts" lists any overallocation or skill gap, the EM **does NOT pause to ask the user about it** — it's a callout for the EM to surface in the Phase 8 hand-off message and the README.md "Where to look" section. The user reviews allocations.md after the run.
3. Proceeds to Phase 8.

**Phase 7 produces:** `allocations_body` (markdown content for the allocations.md file).

---

## Phase 8 — Write Artifacts

EM (main thread) writes all files to `docs/<feature-slug>/`. **Order matters — Hard Gate #9 requires README.md is written LAST.**

### Step 8.1 — Write `planning.md`

Sections (per spec §6.2):
- Restated requirements (R-list).
- Codebase grounding summary (distilled from Phase 2).
- Per-requirement validation table.
- Architecture choices: aggregates, ports/traits, module layout, data flow, error mapping.
- Sequencing rationale (why Foundation → Frontier order is what it is).
- Risks + mitigations.
- Open Questions (with recommended defaults so engineers aren't blocked).
- Test strategy + Definition of Done.
- Debate provenance — 1-paragraph summary from staff engineer's output.

### Step 8.2 — Write `tasks.md`

Sections (per spec §6.3):
- Conflict rule at the top: "two tasks owned by different engineers may not write to the same module."
- **Foundation Sprint** (senior-only, blocks all parallel work) — from staff engineer's Output 2.
- **Parallel Frontiers** — from staff engineer's Output 3.
- **DAG visualization** — ASCII tree showing dependencies.

### Step 8.3 — Write `engineer-N-tasks.md` (one per recommended engineer slot)

For each engineer slot (1, 2, ..., N where N is the staff engineer's recommended headcount):

- Engineer slot ID + recommended seniority.
- Tasks in dependency order (this engineer's slice only).
- For each task: ID, title, acceptance criteria, TDD red list, interfaces owned, interfaces consumed, hand-off contracts, files to touch.
- Coordination notes: when to sync with which other engineer.
- **Self-contained** — this file alone is enough to execute the work.

### Step 8.4 — Write `engineering-standards.md`

Two sections from staff engineer's Output 5:
- `## Inherited from codebase` — bullets with `(CLAUDE.md §X)` style attributions.
- `## Feature-specific commitments` — new aggregate, port traits, error types, feature flag, coverage floor, migration approach.

### Step 8.5 — Write `allocations.md` (only if Phase 7 ran)

If `allocations_body` was produced by Phase 7, write `docs/<slug>/allocations.md` with:

```markdown
# Allocations — <feature-name>

**Feature slug:** <slug>
**Date allocated:** <ISO date>
**Source:** em-feature-plan Phase 7 (staff-engineer dispatch)
**Roster as of:** <date the team_roster was provided>

<allocations_body verbatim from Phase 7>
```

If Phase 7 was skipped, omit this file entirely. The README.md "Where to look" index in Step 8.6 conditionally lists allocations.md based on whether the file exists.

### Step 8.6 — Write `README.md` LAST (Hard Gate #9)

Sections (per spec §6.1, ~80-120 lines):
- Feature one-liner, slug, status.
- Where the requirements came from (link to brainstorm doc / ticket / spec).
- **Recommended engineer headcount** + rationale (from staff engineer's Output 1).
- "Where to look" index — one-line pointer to every other file in this folder. **Include allocations.md if Phase 7 ran.**
- **Allocation summary (if Phase 7 ran):** one-paragraph summary of slot→engineer mapping + any risk callouts the staff engineer flagged, with a pointer to allocations.md for full details.
- Pipeline next step (typical: `/superdev:em-ship-feature <slug>` OR `/superdev:superdev` per engineer packet — if allocated, each engineer claims their assigned slot per allocations.md).
- **Definition of Done** for the whole feature.
- Date written + which skill version produced it.

### Step 8.7 — Hand-off message in chat

```
em-feature-plan: DONE

Feature: <name>
Slug: <slug>
Files written:
  docs/<slug>/
  ├── planning.md
  ├── tasks.md
  ├── engineer-1-tasks.md
  ├── engineer-N-tasks.md  (one per recommended slot)
  ├── engineering-standards.md
  ├── allocations.md          (only if Phase 7 ran)
  └── README.md

Recommended headcount: <N> engineer(s). See README.md "Where to look" for the per-engineer index.
Allocation: <"see allocations.md" if Phase 7 ran, OR "skipped — slot-based packets only" if not>.
<If allocations.md has risk callouts: "⚠️ <N> allocation risk(s) flagged — see allocations.md 'Risk callouts' section.">

Pipeline next steps:
  Autonomous:  /superdev:em-ship-feature <slug>
  Interactive: /superdev:superdev (run per engineer packet — each engineer claims their assigned slot per allocations.md if it exists)
```

---

## Agent Roster

| Role | Subagent type | Model | When |
|---|---|---|---|
| **EM** (orchestrator, main thread) | — | Parent's model + `/effort max` (Hard Gate #1) | All phases. Orchestrates the peer-debate alternation in Phase 5 (re-dispatches each engineer with the other's prior turn) and the staff follow-up round in Phase 6 (Hard Gate #10) |
| **Senior Engineer A** | `general-purpose` | `model: opus` (Hard Gate #7) | Phase 4 (parallel with B), Phase 5 Round 1 + Round 2 (one dispatch per round), Phase 6 follow-up (if requested) |
| **Senior Engineer B** | `general-purpose` | `model: opus` (Hard Gate #7) | Symmetric to A |
| **Staff Engineer** | `general-purpose` | `model: opus` (Hard Gate #7) | Phase 6 (decomposition — one dispatch + optional one follow-up) and Phase 7 (allocation — one dispatch, only if team roster provided). Same brain across both phases, separate dispatches per concern. |

### Voices

**EM** — pragmatic, owns sequencing and dispatch. Owns the peer-debate alternation (Phase 5) and the staff follow-up round (Phase 6) — these are EM-orchestrated because subagents cannot dispatch each other in this runtime. The voice of "I'm the only one who can dispatch, so I'm the integrator of the debate."

**Senior Engineer A & B** — opposite biases (per `bias_pair`). Each returns: plan in Phase 4, critique of the other in Phase 5 Round 1, response in Phase 5 Round 2, optional answer in Phase 6 follow-up. Does NOT dispatch other subagents (can't — only EM can). The two engineers represent different design priors; the asymmetry is what makes peer debate productive.

**Staff Engineer** — has authority to override either engineer with written rationale. Adjudicates + decomposes + assembles standards in Phase 6 (one or two dispatches if follow-up). Allocates packets to real engineers in Phase 7 (one dispatch, only if team roster provided). Same brain across decomposition and allocation — no hand-off drift, but separate dispatches so each concern gets focused context.

---

## Red Flags — Stop if You Think...

| Thought | Reality |
|---|---|
| "I'll have Senior A dispatch Senior B for the debate alternation" | Hard Gate #10: subagents cannot dispatch other subagents in this runtime. The EM must orchestrate each turn as a fresh dispatch with the prior turn's content injected. Telling a senior to dispatch will fail. |
| "I'll skip Phase 2 grounding and let the seniors figure out the codebase from scratch" | Hard Gate #3: designing in ignorance of the codebase is a workflow failure. Both seniors need the same grounding context to debate productively. |
| "I'll dispatch the 2 seniors sequentially in Phase 4 because it's easier to manage" | Hard Gate #6: ONE message, two `Agent` calls. Sequential dispatch defeats parallel generation — the whole point of peer debate is independent drafts that didn't influence each other. |
| "Let the debate go 3+ rounds because they haven't converged" | Hard Gate #8: ≤ 2 rounds. Unbounded LLM debate has fork-bomb economics. If diverged after round 2, the staff engineer adjudicates with the full transcript. |
| "Let the staff engineer have multiple follow-up rounds" | Hard Gate #8: 1 follow-up max. Staff's second dispatch is FINAL. |
| "Skip Phase 3 questions — the engineers can figure out ambiguities during drafting" | Hard Gate #5: Phase 3 is the ONLY user-question phase. Ambiguities discovered later become silent picks (bad) or Open Questions written into planning.md (acceptable but should be rare). |
| "Write the README first to scope the work" | Hard Gate #9: README LAST. Writing it first under-specs the other files. |
| "Skip the Foundation Sprint — every task can run in parallel from the start" | Most features have shared interfaces. If "every task is independent" feels true, you haven't modeled the foundation correctly. Foundation tasks exist to prevent shared-interface conflicts during downstream parallel execution. |
| "Drop the bias-pair selection — Pragmatism vs Rigor is always the right pair" | The bias pair IS the debate's character. Different features benefit from different biases (Speed vs Quality for tight-deadline features, Greenfield vs Reuse for refactoring-heavy work). Ask the user. |
| "Skip the structured `## 7. Three things I chose NOT to do` section in seniors' plans" | The deferred-list is what makes the debate productive — the OTHER engineer often picks up exactly those deferred items and argues for them. Without it, the debate misses the most useful disagreements. |
| "User skipped Phase 7 — I'll allocate the packets myself in the README anyway" | No. If `team_roster` is null, Phase 7 is skipped entirely — no `allocations.md`, no allocation summary in README. The user chose slot-based output deliberately (solo planning, roster-unknown, or manual allocation later). Don't second-guess by inventing allocations from thin air. |
| "Bake allocation into Phase 6's staff dispatch to save a round-trip" | No. Phase 6 is decomposition; Phase 7 is allocation. Separating them lets allocation be optional, gives each concern focused context, and produces a single-purpose `allocations.md` artifact that can be updated when team composition changes without rewriting the rest of the planning bundle. The marginal cost of one extra Opus dispatch is worth the design clarity. |
| "Allocation has risk callouts — let me ask the user before continuing" | Hard Gate #5: Phase 3 was the only user-question phase. Risk callouts go in `allocations.md` and the README hand-off; the user reviews them after the run, not during. If risks are severe, the user can re-run em-feature-plan with an updated roster or de-scope. |
| "Rename `engineer-N-tasks.md` to `engineer-Alice-tasks.md` so the file names reflect ownership" | No. Slot-based filenames stay. `em-ship-feature` consumes slot-named packets; coupling planning artifacts to specific human names ties them to a team snapshot that may shift. `allocations.md` is the slot→name mapping; the mapping changes independently of the packets. |

---

## First-Run Verification

The first time you use this skill on a device, run it on a small feature and confirm:

- Phase 0 halts cleanly when `/effort max` is NOT active.
- Phase 0's bias-pair `AskUserQuestion` presents 3 options with the correct bias prompts as descriptions.
- Phase 1 produces a clean R-list (atomic, testable, one sentence each).
- Phase 2 issues ALL the reads in ONE message (verify by checking the conversation log).
- Phase 3 bundles Blocker + High-signal questions via `AskUserQuestion` (max 4 per call; multiple calls if more than 4).
- Phase 4 dispatches BOTH seniors in ONE message with `model: opus` and the correct bias prompts.
- Phase 5 Round 1 dispatches happen as TWO separate EM-initiated Agent calls (not subagent-to-subagent).
- Phase 5 Round 2 is skipped if both engineers self-report CONVERGED in Round 1.
- Phase 5 produces a clean `outcome` (Reconciled or Diverged) and a `debate_transcript`.
- Phase 6 staff dispatch returns all 6 sections (final plan, foundation, frontiers, per-engineer packets, standards, debate provenance).
- Phase 6 follow-up round only happens if the staff includes a "Follow-up questions" section in its first response.
- Phase 7 (Allocate) is SKIPPED entirely when the user picked "Skip allocation" in Phase 3 — no extra staff dispatch, no allocations.md.
- Phase 7 (Allocate), when it runs, dispatches the staff engineer ONCE with team roster + packets, and produces an allocations.md body with slot→engineer mapping, risk callouts, unallocated capacity, and optional recommendations.
- Phase 8 writes 5-6 files in the order `planning.md` → `tasks.md` → `engineer-*-tasks.md` → `engineering-standards.md` → `allocations.md` (only if Phase 7 ran) → `README.md` (LAST — Hard Gate #9).
- README's "Where to look" index includes `allocations.md` only if it was written; the allocation summary paragraph in README is conditional on Phase 7 having run.
- Hand-off message includes the pipeline-next-step pointer (`/superdev:em-ship-feature <slug>` or `/superdev:superdev` per packet) and flags any allocation risk callouts.

If any step doesn't work, debug the affected piece (the SKILL.md prose or the relevant dispatch template) before running on real work.
