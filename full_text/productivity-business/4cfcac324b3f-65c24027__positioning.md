---
name: positioning
description: Orchestrator — detect market vs product mode, recommend positioning frameworks, synthesize outputs into unified positioning
type: research
version: v0.26
required_conventions: [alignment-page, interrogation-page]
argument-hint: "[optional: \"product\" | \"--synthesize\" | focus area]"
context_intake: scoped
visual_tier: visual
invocation: orchestrator
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. After install, tell Claude users to run `/reload-skills`, then `/clear` or restart if the skill remains invisible. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Positioning — Orchestrator

This is an **orchestrator skill** using the parent router delegation pattern (see `docs/orchestrator-convention.md`). It detects context, recommends applicable positioning frameworks, and synthesizes their outputs. Individual frameworks live as child skills under `frameworks/`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language while a scope, framework findings, or synthesis approval is pending. The approval request itself is the next action, and the only terminal command section allowed before approval is `## Invoke With YAML`, which names the parent command to invoke with the compiled YAML, such as `/positioning` plus the same product/research path argument when present. Parent-loop continuation is not downstream routing. Only emit downstream next-skill routing after the synthesized `positioning.md` artifact has been approved and written.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `/customer-discovery` first and stop.
- **Hard**: `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) must exist. If not, tell the user to run `/competitive-analysis` first and stop.
- **Strong default**: `research/journey-map.md` (or `research/{slug}/journey-map.md`) should exist before writing canonical positioning. If missing, recommend `/journey-map` first unless the user explicitly needs a provisional positioning analysis.
- **Soft**: Read these if they exist:
  - `research/journey-map.md` — where value is delivered, the aha moment
  - `research/customer-feedback.md` — real customer language about what makes the product different
  - `research/monetization.md` — pricing context for value perception

## Execution Model — Research Session Loop

This is a **self-advancing Pattern A research orchestrator** (see `docs/research-session-loop-convention.md`). Each invocation starts cold, resolves its state from **pasted YAML + filesystem**, runs **exactly one heavy phase**, emits the next gate, and stops. The user advances the loop by clearing context and re-invoking `/positioning`. The user never invokes a framework subskill directly — the orchestrator follows each selected framework's subskill inline.

When a framework is pending, the only user-facing continuation route is re-invoking `/positioning` with the same product/research path argument when present, for example `/positioning research/afps-tracker`. Never tell the user to run a path-shaped child framework command; the parent resolves the pending framework from the run manifest and filesystem.


### Terminal Handoff Contract

Every terminal response for this Research Session Loop must end with `## Next Work` and one command section. Use `## Invoke With YAML` only while a `review` page is waiting for compiled YAML; it names the parent command to invoke with the compiled YAML. Use `## Recommended Next Command` only after approved YAML has been consumed and the approved artifact has been written or updated. Do not put any other section after the applicable command section.

### Self-Routing Continuation Payload

Every `review` alignment page this parent creates must include `agent_routing` in the bottom compiled YAML. The mapping routes a fresh agent back to this parent orchestrator; it does not authorize direct framework invocation or replace parent-owned state resolution. Use this shape, preserving the current product/research path argument when present:

```yaml
agent_routing:
  workflow: pattern-a-research-loop
  parent_skill: positioning
  command: "/positioning research/{slug}"
  product_path: research/{slug}        # omit in flat mode
  gate_owner: parent-orchestrator
  gate_type: framework-findings        # or framework-selection, shortcut-selection, synthesis
  framework_slug: <framework-slug>     # only for framework-findings gates
  framework_mode: inline-subskill      # only for framework-findings gates
  run_manifest: research/{slug}/_working/positioning-run.yaml
  next_resolution: parent-resolves-from-yaml-and-filesystem
```

For framework selection, shortcut, and synthesis gates, omit `framework_slug` and `framework_mode`; `gate_type` must name the actual gate. The `command` field must be the same parent command shown under `## Invoke With YAML`. The parent consumes the YAML, writes or amends the artifact, archives consumed sources, derives progress from the run manifest plus canonical-intermediate files, and decides whether to load a framework subskill inline.

For review-pending framework, selection, shortcut, or synthesis pages, `## Next Work` tells the user to review the alignment page, compile YAML, and paste it into a session invoking `/positioning` with the same product/research path argument when present. For post-write pending-framework states, `## Next Work` reports progress as "k of N frameworks complete" and says the next run executes the next pending framework; `## Recommended Next Command` names `/positioning`.

After every framework write, recalculate pending frameworks from the run manifest and canonical-intermediate files before writing this handoff. If no selected frameworks remain and canonical `positioning.md` is missing, `## Next Work` says the next run builds the unified synthesis review page, and `## Recommended Next Command` names `/positioning --synthesize` with the same product/research path argument when present. After approved synthesis writes canonical `positioning.md`, the final command section names only the first downstream command selected by the Next Steps decision tree.


State lives in two places only:

- **Run manifest** — `research/_working/positioning-run.yaml` (flat) or `research/{slug}/_working/positioning-run.yaml` (product-path). Records the selected framework set and each framework's intermediate path. Written when the multi-select YAML is approved. Shape:

  ```yaml
  orchestrator: positioning
  slug: skills-showcase            # omit in flat mode
  selected_frameworks:
    - slug: jtbd-positioning
      intermediate: research/skills-showcase/positioning-jtbd-positioning.md
    - slug: strategic-canvas
      intermediate: research/skills-showcase/positioning-strategic-canvas.md
  ```

- **Canonical-intermediate existence** — a selected framework is *done* when `research/positioning-{framework}.md` (or `research/{slug}/positioning-{framework}.md`) exists, *pending* otherwise. `pending = selected − existing-intermediates`. The manifest stores selection only, not per-framework status.

`research/.progress.yaml` stays coarse — its `pipeline_stage` is a pointer, not per-framework status.

### State resolution (resolve the first match; YAML first, then most-progressed A→G)

On each invocation, after Product-Path Scope Resolution (step 0), resolve state:

| State | Detected when | Heavy phase this session | Emits / stops with |
|---|---|---|---|
| **0 — pasted YAML** | a compiled alignment YAML is pasted | branch on `approval_status`: `ready-for-agent-review` → apply the approval for the gate it answers (light: write manifest and/or prior framework intermediate, archive consumed source), then fall through to the next pending state below; `not-approved` → amend the named page (refinement session) and stop | amended page, or proceeds ↓ |
| **A — done** | canonical `research/positioning.md` (or `research/{slug}/positioning.md`) exists | — | done; emit next-skill route (step 6) |
| **B — synthesize** | run manifest exists, all selected intermediates exist, no canonical `positioning.md` (also forced by `--synthesize`) | **synthesis** (step 4) | synthesis `review` page |
| **C — run framework** | run manifest exists, ≥1 selected framework pending | **run next pending framework inline at its research stage** (step 3b) | that framework's findings `review` page |
| **E — build selection** | interrogation completion handoff exists, no run manifest, no canonical | mode detect → load context → recommend frameworks → build multi-select page (steps 1–3a) | multi-select `review` page |
| **G — interrogate** | nothing on disk (cold start), after the hard prerequisites are satisfied | **run one stage-zero interrogation round** (see **State G — Stage-Zero Interrogation Loop** below) | an `interrogation/positioning-r{N}-{branch}.html` round page; on confidence-gate pass, the interrogation completion handoff |

**Cold entry (state G).** This orchestrator uses `context_intake: scoped`, but elicitation is no longer a 1–3-question terminal cap — it runs as the **stage-zero interrogation loop** in HTML. A cold start (nothing on disk, after the hard `research/icp.md` + `research/competitive-analysis.md` prerequisites are satisfied) resolves to **state G**; positioning **cannot advance to stage one (state E) until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. The completion handoff then feeds state E. The `product`/`post-launch`/`obviously-awesome` shortcut still short-circuits E→C with a fixed framework set (step 5) after its own interrogation round.

### State G — Stage-Zero Interrogation Loop

Run elicitation as the stage-zero interrogation loop defined in `INTERROGATION-PAGE.md` / `docs/interrogation-page-convention.md` before building the framework multi-select page. Round 1 builds `interrogation/positioning-r1-{branch}.html` rendering 3–7 source-tagged assumptions as confirm/correct/flag controls plus the first open questions (each marked `data-open-input`), with `data-interrogation-round="1"`, `data-interrogation-gate="continue"`, and the answer sidecar `research/_working/interrogation-positioning-r1.yaml` (or product-path equivalent). Rounds 2..N are adaptive follow-ups seeded by the prior round's compiled answers. The coverage-checkpoint round (`data-interrogation-gate="coverage-checkpoint"`) summarizes everything established; on the user's completeness confirmation, write the interrogation completion handoff (`research/_working/interrogation-positioning-handoff.md` or the product-path equivalent) and stop. Each round ends the terminal message with `## Next Work` and `## Invoke With YAML` naming `/positioning`. Terminal questioning is the degraded fallback only when the HTML page cannot be opened.

**Light vs heavy.** Recording the approved selection into the run manifest (state 0→C head), writing an already-reviewed framework intermediate, and archiving a consumed source are *light* — they fold into the head of the next heavy session. The heavy phase (one framework's research, synthesis) is the only thing isolated per session.

**Shortcuts.** `/positioning --synthesize` forces state B. `/positioning product` (also `post-launch`, `obviously-awesome`) is the product-positioning shortcut (step 5): after the user approves the shortcut plan, it writes a fixed single-framework set (`obviously-awesome`) into the run manifest and enters state C. Do not queue framework work in `tasks/todo.md` or hand it to `/exec`.

---

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Mode Detection

Detect **market-positioning mode** (default) or **product-positioning mode**:

**Market-positioning mode** activates when:
- No `research/customer-feedback.md` with post-launch customer evidence, AND
- No production codebase with live users detected, AND
- `$ARGUMENTS` does not contain "product", "post-launch", or "obviously-awesome"

Available frameworks in market mode:
- `jtbd-positioning` — Jobs-to-be-Done positioning analysis
- `strategic-canvas` — Blue Ocean strategic canvas (eliminate/reduce/raise/create)
- `moore-positioning` — Geoffrey Moore positioning hypothesis
- `category-design` — Play Bigger category creation

**Product-positioning mode** activates when:
- `research/customer-feedback.md` exists with real customer data, OR
- `$ARGUMENTS` contains "product", "post-launch", or "obviously-awesome", OR
- Production spec exists AND customer feedback references real users

Available frameworks in product mode:
- `obviously-awesome` — April Dunford (requires real customer evidence)
- `strategic-canvas` — optionally, for category refresh

### 2. Load Context

- Read `research/icp.md` — ICP segments, pain points, value props, trigger events
- Read `research/competitive-analysis.md` — competitor landscape, gaps
- Read `research/journey-map.md` if it exists — aha moment, value delivery
- Read `research/customer-feedback.md` if it exists — real language, satisfaction drivers
- Read CLAUDE.md, README for product context
- Read any existing `research/positioning-*.md` intermediate artifacts (from prior runs)

### 3a. State E — Framework Selection & Build Multi-Select Page

Build the framework multi-select `review` alignment page with:

1. **Mode explanation**: which mode was detected and why (evidence for detection)
2. **Available evidence summary**: what research exists and what's missing
3. **Multi-select framework section**: checkboxes for each available framework with:
   - Framework name and one-line description
   - Why it's recommended or optional for this context
   - Pre-checked defaults based on available evidence:
     - Market mode defaults: `jtbd-positioning` + `strategic-canvas` + `moore-positioning` pre-checked; `category-design` unchecked (recommended only when strategic canvas shows no existing category fits)
     - Product mode defaults: `obviously-awesome` pre-checked; `strategic-canvas` unchecked (optional refresh)
4. **Loop plan explanation**: the selected set is the scope-and-candidate approval gate; each selected framework will then be run inline (one findings page per framework) and the run advances by re-invoking `/positioning`
5. **Approval gate**: framework selection confirmation

This multi-select approval **is** the Stage-1 scope approval for the whole selected set. Stop for compiled YAML. Do **not** write the run manifest or run any framework in this session — that is state C.

### 3b. State C — Run Next Pending Framework (inline)

This session consumes the approved multi-select YAML (state 0→C) or advances after a prior framework's approval. At the **head** of the session, do the light bookkeeping first:

1. **Write the run manifest** if it does not yet exist: `research/_working/positioning-run.yaml` (flat) or `research/{slug}/_working/positioning-run.yaml` (product-path), recording `selected_frameworks` with each framework's `slug` and canonical `intermediate` path. Include only frameworks the user selected. Example (market mode):

   ```yaml
   orchestrator: positioning
   selected_frameworks:
     - slug: jtbd-positioning
       intermediate: research/positioning-jtbd-positioning.md
     - slug: strategic-canvas
       intermediate: research/positioning-strategic-canvas.md
     - slug: moore-positioning
       intermediate: research/positioning-moore-positioning.md
   ```

2. **If a prior framework's reviewed content was just approved** by the pasted YAML, write its canonical intermediate `research/positioning-{fw}.md` (or `research/{slug}/positioning-{fw}.md`) from the already-reviewed working packet, and archive that framework's working packet and superseded review page.

Then run the **one heavy phase** for this session:

3. **Determine the next pending framework** = the first framework in `selected_frameworks` whose canonical intermediate does not yet exist.
4. **Load and follow that framework subskill's `SKILL.md` inline**, entering at its **research stage (Stage 2)**: the multi-select approval already satisfied the framework's Stage-1 scope gate, so perform the framework's research, write its working packet, and build a single findings `review` page for that framework. Stop for that framework's compiled YAML.

**Advance the loop by self-re-invocation.** When a framework findings page is in `review`, end the terminal message with `## Next Work` telling the user to review the page and compile YAML, followed by `## Invoke With YAML` naming `/positioning` with the same product/research path argument when present. After a framework's compiled YAML is approved and its canonical intermediate is written, recalculate pending frameworks from the manifest and filesystem before writing the handoff. If pending frameworks remain, end with `## Next Work` reporting progress as "k of N frameworks complete" and saying the next run executes the next pending framework, followed by `## Recommended Next Command` naming `/positioning`. If no pending frameworks remain and canonical `positioning.md` is missing, end with `## Next Work` saying the next run builds the unified synthesis review page, followed by `## Recommended Next Command` naming `/positioning --synthesize` with the same product/research path argument when present. Do not emit cross-skill routing here — that happens only after synthesis.


### 4. State B — Synthesis (auto-detected; also `/positioning --synthesize`)

Enter synthesis when the run manifest exists, **all** selected framework intermediates exist, and no canonical `research/positioning.md` yet exists. An explicit `/positioning --synthesize` also forces this state. Read all selected intermediate framework outputs (the `intermediate` paths recorded in the run manifest), e.g.:
- `research/positioning-jtbd-positioning.md`
- `research/positioning-strategic-canvas.md`
- `research/positioning-moore-positioning.md`
- `research/positioning-category-design.md`
- `research/positioning-obviously-awesome.md`

At least one must exist. If none exist, tell user to run framework selection first.

Synthesize into unified `research/positioning.md`:

**Market-positioning synthesis includes:**
- Combined positioning hypothesis drawing from all framework outputs
- Moore template filled with evidence from JTBD + Canvas + Category analysis
- Evidence matrix: each claim mapped to which framework(s) support it
- Confidence levels per claim (strong/moderate/hypothesized)
- Validation plan: what needs testing before the position is canonical
- Mode header: `> Mode: Market Positioning (hypothesized, pre-product)`

**Product-positioning synthesis includes:**
- Positioning statement (Obviously Awesome output)
- Evidence matrix grounded in customer feedback
- Confidence levels (most should be "strong" — backed by customer data)
- Mode header: `> Mode: Product Positioning (customer-grounded)`

Build alignment page for synthesis approval with:
- Full proposed `research/positioning.md` content
- Evidence matrix combining all framework sources
- Confidence/assumption register
- Proposed file changes gate
- Approval gate

After approval: write `research/positioning.md`, then on this canonical write **archive the run manifest** (`positioning-run.yaml`) and the synthesis working packet under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, update `research/.progress.yaml` `pipeline_stage` to `positioning`, and emit the downstream next-step routing (step 6). This is the one place cross-orchestrator routing is allowed.

### 5. State C via Product-Positioning Shortcut (`/positioning product`)

Skip multi-select. Build an alignment page for the shortcut execution plan with:

1. **Shortcut explanation**: product-positioning shortcut selected and why `obviously-awesome` is the only queued framework
2. **Evidence readiness**: customer-feedback requirement and any missing evidence caveats
3. **Proposed loop plan**: the single `obviously-awesome` framework that will be recorded in the run manifest
4. **Approval gate**: require final compiled YAML approval before writing the run manifest

Do not write the run manifest before alignment approval. The next action is review of the HTML alignment page.

After user approval via final compiled YAML, write this selected set to the run manifest and enter the next pending framework session:

```yaml
orchestrator: positioning
selected_frameworks:
  - slug: obviously-awesome
    intermediate: research/positioning-obviously-awesome.md
```

Then enter **state C** and run `obviously-awesome` inline per step 3b. The loop advances by re-invoking `/positioning`.

### 6. Next Steps (after synthesis only)

Include 3–5 applicable items with "Recommended + Other options" framing:

- IF no `research/journey-map.md`: check for `customer-lifecycle` pack → recommend `/journey-map`
- DEFAULT: check `.agents/project.json.enabled_packs` for `product-design` — if not enabled, recommend `npx skillpacks install product-design` from the project shell; if enabled, recommend `/user-flow-map [positioning-backed product direction]`
- IF solution-customer fit is weak/disputed: `/value-prop-canvas`
- IF revenue/channels/cost/defensibility risks exposed: `/lean-canvas`
- IF no `research/gtm.md`: check for `business-growth` pack → recommend `/gtm`
- IF `research/gtm.md` exists: recommend `/gtm` refresh
- IF no `research/monetization.md`: check for `business-growth` pack → recommend `/monetization`
- IF codebase exists: check for `business-ops` pack → recommend `/mvp-gap`

### 7. Downstream Impact Check (after synthesis write)

Check for downstream research documents that may be affected:
- `research/gtm.md`

Classify impact as None/Minor/Major per standard pattern.

## Optional Research Trigger Map

These detours are conditional framework owners, not required AFPS chain links. Apply after synthesis.

| Positioning signal | Owner | Trigger threshold |
|---|---|---|
| Solution-customer fit weak/disputed, value mapping low confidence | `/value-prop-canvas` | Trigger: unique attributes can't be confidently mapped to value. Skip: value mapping clear even if hypothesized. |
| Business-model risk (revenue/channels/cost/defensibility) exposed by category strategy | `/lean-canvas` | Trigger: risk would change UX or prototype choices. Skip: normal competitive findings. |
| Pricing architecture central to positioning (premium vs value changes direction) | `/monetization` | Trigger: category/value mapping requires grounded pricing. Skip: pricing not a differentiator. |

## Output

### State E / State C output: run manifest plus per-framework findings review page

The state-E multi-select page; then, per state-C session, the run manifest `research/_working/positioning-run.yaml` (or `research/{slug}/_working/positioning-run.yaml`, written at the head of the first state-C session) plus the next pending framework's findings review page. One findings page per selected framework; the canonical intermediate `research/positioning-{framework}.md` is written on that framework's approval.

### State B output (synthesis): `research/positioning.md` (or `research/{slug}/positioning.md`)

```markdown
# Positioning

> Based on: [list of framework outputs used]
> Date: [current date]
> Mode: Market Positioning (hypothesized, pre-product) | Product Positioning (customer-grounded)
> Frameworks applied: [list]

## Positioning Statement

**For** [target segment]
**who** [key pain / trigger event]
**[product name] is a** [market category]
**that** [key value / unique benefit]
**Unlike** [primary competitive alternative]
**[product name]** [key differentiator]

## Summary
[2-3 sentences: the positioning thesis]

## Evidence Matrix

| Claim | Supporting Framework(s) | Evidence | Confidence | Assumption Status |
|-------|------------------------|----------|------------|-------------------|
| [claim] | JTBD / Canvas / Moore / Category / OA | [source] | Strong / Moderate / Hypothesized | Validated / Needs testing |

## Framework Synthesis

### From JTBD Analysis
[Key findings — primary job, outcome positioning]

### From Strategic Canvas
[Key findings — eliminate/reduce/raise/create moves, competitive gaps]

### From Moore Hypothesis
[Key findings — positioning template, evidence gaps]

### From Category Design
[Key findings — category diagnosis, POV if new category]

### From Obviously Awesome
[Key findings — if product mode]

## Target Segment
[Best-fit segment with evidence from multiple frameworks]

## Market Category
[Chosen category with evidence from multiple frameworks]

## Confidence Register

| Element | Confidence | Evidence Source | What Would Change It |
|---------|-----------|----------------|---------------------|
| [element] | [level] | [source] | [condition] |

## Validation Plan (market mode only)
[What needs testing before this position is canonical]

## Positioning Implications

### For Messaging
### For Product
### For Sales
### For Pricing

## Downstream Impact
[Standard pattern]

## Next Steps
[Standard routing]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`.
- One-time condition-gated records go in `tasks/record-todo.md`.
- Cadence-based reviews go in `tasks/recurring-todo.md`.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless promoted.

## Constraints

- **Requires ICP + competitive analysis.** Positioning without knowing the customer and the competition is guesswork.
- **Customer-grounded.** Every positioning decision must connect to real customer behavior or research evidence.
- **Mode detection is evidence-based.** Do not override mode detection without user confirmation.
- **Parent owns the research loop.** It records selected frameworks in the run manifest and runs one pending framework inline per invocation. Do not queue framework work in `tasks/todo.md` or hand it to `/exec`.
- **Synthesis requires at least one framework output.** Do not synthesize from zero evidence.
- **Do not overwrite existing `research/positioning.md`** without asking the user first.

## Context Gathering

**Step 1 — Stage-zero interrogation.** Before researching, elicit context through the **state-G stage-zero interrogation loop** (see **State G — Stage-Zero Interrogation Loop** above and `INTERROGATION-PAGE.md`): build `interrogation/positioning-r{N}-{branch}.html` rounds — round 1 is the assumptions manifest plus the first open questions — and loop until the confidence gate passes. Do not cap elicitation at 1–3 terminal questions; the loop runs until coverage. Terminal questioning is the degraded fallback only when an HTML page cannot be opened.

**Step 2 — Research.** Conduct research scoped by the elicited answers.

**Step 3 — Findings validation.** Surface critical findings for validation inside the stage-one framework/scope alignment page and its review gates.

## Interrogation Page

Follow the shared interrogation-page convention via the packaged convention resolver; output path is `interrogation/positioning-r{N}-{branch}.html`. Before producing research, run the stage-zero interrogation loop, starting with the assumptions manifest as round 1, and loop until the confidence gate passes. This skill **cannot advance to stage one until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. Each round page must contain at least one genuinely open input (`data-open-input`).

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/positioning-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
