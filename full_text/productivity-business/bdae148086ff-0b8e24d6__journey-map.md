---
name: journey-map
description: Orchestrator — detect pre-product vs product-exists mode, recommend journey-mapping frameworks, synthesize outputs into unified lifecycle overview
type: research
version: v0.23
argument-hint: "[optional: \"product\" | \"--synthesize\" | app, use case, persona]"
invocation: orchestrator
context_intake: scoped
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Journey Map — Orchestrator

This is an **orchestrator skill** using the parent router delegation pattern, running as a self-advancing **Research Session Loop** (see `docs/research-session-loop-convention.md` and the Execution Model below). It detects context, recommends applicable journey-mapping frameworks, runs each selected framework inline one per session, and synthesizes their outputs. Individual frameworks live as child skills under `frameworks/`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include downstream or cross-skill command recommendations while a scope, framework findings, or synthesis approval is pending. The approval request itself is the next action, and the only terminal command section allowed before approval is `## Recommended Next Command After Compiling YAML` and it must name this same parent orchestrator, such as `$journey-map` plus the same product/research path argument when present. Parent-loop continuation is not downstream routing. Only emit downstream next-skill routing after the synthesized `journey-map.md` artifact has been approved and written.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md` in product-path mode) must exist — run `$customer-discovery` first.
- **Soft**: Read these if they exist:
  - `research/competitive-analysis.md` — competitor landscape
  - `research/customer-feedback.md` — real customer language
  - Specs, README/CLAUDE, and relevant source files for product context

## Execution Model — Research Session Loop

This is a **self-advancing Pattern A research orchestrator** (see `docs/research-session-loop-convention.md`). Each invocation starts cold, resolves its state from **pasted YAML + filesystem**, runs **exactly one heavy phase**, emits the next gate, and stops. The user advances the loop by starting a fresh Codex session and re-invoking `$journey-map`. The user never invokes a framework subskill directly — the orchestrator follows each selected framework's subskill inline.

When a framework is pending, the only user-facing continuation route is re-invoking `$journey-map` with the same product/research path argument when present, for example `$journey-map research/afps-tracker`. Never tell the user to run a path-shaped child framework command; the parent resolves the pending framework from the run manifest and filesystem.


### Terminal Handoff Contract

Every terminal response for this Research Session Loop must end with `## Next Work` and one command section. Use `## Recommended Next Command After Compiling YAML` only while a `review` page is waiting for compiled YAML. Use `## Recommended Next Command` only after approved YAML has been consumed and the approved artifact has been written or updated. Do not put any other section after the applicable command section.

### Self-Routing Continuation Payload

Every `review` alignment page this parent creates must include `agent_routing` in the bottom compiled YAML. The mapping routes a fresh agent back to this parent orchestrator; it does not authorize direct framework invocation or replace parent-owned state resolution. Use this shape, preserving the current product/research path argument when present:

```yaml
agent_routing:
  workflow: pattern-a-research-loop
  parent_skill: journey-map
  command: "$journey-map research/{slug}"
  product_path: research/{slug}        # omit in flat mode
  gate_owner: parent-orchestrator
  gate_type: framework-findings        # or framework-selection, shortcut-selection, synthesis
  framework_slug: <framework-slug>     # only for framework-findings gates
  framework_mode: inline-subskill      # only for framework-findings gates
  run_manifest: research/{slug}/_working/journey-map-run.yaml
  next_resolution: parent-resolves-from-yaml-and-filesystem
```

For framework selection, shortcut, and synthesis gates, omit `framework_slug` and `framework_mode`; `gate_type` must name the actual gate. The `command` field must be the same parent command shown under `## Recommended Next Command After Compiling YAML`. The parent consumes the YAML, writes or amends the artifact, archives consumed sources, derives progress from the run manifest plus canonical-intermediate files, and decides whether to load a framework subskill inline.

For review-pending framework, selection, shortcut, or synthesis pages, `## Next Work` tells the user to review the alignment page and compile YAML, and the command section names `$journey-map` with the same product/research path argument when present, then start a fresh Codex session if the skill list or context is stale. For post-write pending-framework states, `## Next Work` reports progress as "k of N frameworks complete" and says the next run executes the next pending framework; `## Recommended Next Command` names `$journey-map`.

After every framework write, recalculate pending frameworks from the run manifest and canonical-intermediate files before writing this handoff. If no selected frameworks remain and canonical `journey-map.md` is missing, `## Next Work` says the next run builds the unified synthesis review page, and `## Recommended Next Command` names `$journey-map --synthesize` with the same product/research path argument when present. After approved synthesis writes canonical `journey-map.md`, the final command section names only the first downstream command selected by the Next Steps decision tree.


State lives in two places only:

- **Run manifest** — `research/_working/journey-map-run.yaml` (flat) or `research/{slug}/_working/journey-map-run.yaml` (product-path). Records the selected framework set and each framework's intermediate path. Written when the multi-select YAML is approved. Shape:

  ```yaml
  orchestrator: journey-map
  slug: skills-showcase            # omit in flat mode
  selected_frameworks:
    - slug: jtbd-timeline
      intermediate: research/skills-showcase/journey-map-jtbd-timeline.md
    - slug: experience-map
      intermediate: research/skills-showcase/journey-map-experience-map.md
  ```

- **Canonical-intermediate existence** — a selected framework is *done* when `research/journey-map-{framework}.md` (or `research/{slug}/journey-map-{framework}.md`) exists, *pending* otherwise. `pending = selected − existing-intermediates`. The manifest stores selection only, not per-framework status. Do not add `status`, `approval`, `blocking_feedback`, notes, timestamps, or gate metadata to framework entries; preserve only `slug` and `intermediate` (plus top-level `orchestrator` and optional `slug`).

`research/.progress.yaml` stays coarse — its `pipeline_stage` is a pointer, not per-framework status.

### State resolution (resolve the first match; YAML first, then most-progressed A→E)

On each invocation, after Product-Path Scope Resolution (step 0), resolve state:

| State | Detected when | Heavy phase this session | Emits / stops with |
|---|---|---|---|
| **0 — pasted YAML** | a compiled alignment YAML is pasted | branch on `approval_status`: `ready-for-agent-review` → apply the approval for the gate it answers (light: write manifest and/or prior framework intermediate, archive consumed source), then fall through to the next pending state below; `not-approved` → amend the named page (refinement session) and stop | amended page, or proceeds ↓ |
| **A — done** | canonical `research/journey-map.md` (or `research/{slug}/journey-map.md`) exists | — | done; emit next-skill route (step 6) |
| **B — synthesize** | run manifest exists, all selected intermediates exist, no canonical `journey-map.md` (also forced by `--synthesize`) | **synthesis** (step 4) | synthesis `review` page |
| **C — run framework** | run manifest exists, ≥1 selected framework pending | **run next pending framework inline at its research stage** (step 3b) | that framework's findings `review` page |
| **E — build selection** | no run manifest and no canonical (cold start) | mode detect → load context → recommend frameworks → build multi-select page (steps 1–3a) | multi-select `review` page |

**Cold entry (no state F).** This orchestrator uses `context_intake: scoped` — there is **no deep-interview phase**. A cold start (nothing on disk, after the hard `research/icp.md` prerequisite is satisfied) resolves directly to **state E**; the `product` shortcut short-circuits E→C with a fixed framework set (step 5).

**Light vs heavy.** Recording the approved selection into the run manifest (state 0→C head), writing an already-reviewed framework intermediate, and archiving a consumed source are *light* — they fold into the head of the next heavy session. The heavy phase (one framework's research, synthesis) is the only thing isolated per session.

**Shortcuts.** `$journey-map --synthesize` forces state B. `$journey-map product` is the product-exists shortcut (step 5): after the user approves the shortcut plan, it writes a fixed framework set (`service-blueprint`, `user-story-map`) into the run manifest and enters state C.

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

0b. **Product-path manifest**: Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the journey map to the active product path by default. When journey mapping reveals lifecycle stages or user flows that only apply to a deferred product path, add a `## Product Path Implications` section noting the finding and recommending `$product-line fork` if it implies a new product surface.

### 1. Mode Detection

Detect **pre-product mode** (default) or **product-exists mode**:

**Pre-product mode** activates when:
- No production codebase with live users detected, AND
- No `research/customer-feedback.md` with post-launch customer evidence, AND
- `$ARGUMENTS` does not contain "product"

Available frameworks in pre-product mode:
- `jtbd-timeline` (default) — Moesta/Switch timeline with push/pull/anxiety/habit forces
- `experience-map` (default) — Adaptive Path emotional arc with doing/thinking/feeling
- `customer-journey-canvas` (optional) — Stickdorn stage×touchpoints×actions canvas
- `service-blueprint` (optional) — Shostack front-stage/backstage/support lines
- `user-story-map` (optional) — Jeff Patton activity→task→story hierarchy

**Product-exists mode** activates when:
- Production code or deployment exists, OR
- `research/customer-feedback.md` exists with real customer data, OR
- `$ARGUMENTS` contains "product"

Available frameworks in product-exists mode:
- `service-blueprint` (default) — operational gaps visible with a running product
- `user-story-map` (default) — release slicing grounded in real usage
- `customer-journey-canvas` (optional) — full-stage touchpoint audit
- `experience-map` (optional) — emotional arc refresh with real feedback
- `jtbd-timeline` (optional) — switching timeline with post-launch evidence

### 2. Load Context

- Read `research/icp.md` — ICP segments, pain points, value props, trigger events
- Read `research/competitive-analysis.md` if it exists — competitor landscape
- Read `research/customer-feedback.md` if it exists — real customer language
- Read CLAUDE.md, README for product context
- Read any existing `research/journey-map-*.md` intermediate artifacts (from prior runs)

### 3a. State E — Framework Selection & Build Multi-Select Page

Build the framework multi-select `review` alignment page with:

1. **Mode explanation**: which mode was detected and why (evidence for detection)
2. **Available evidence summary**: what research exists and what's missing
3. **Multi-select framework section**: checkboxes for each available framework with:
   - Framework name and one-line description
   - Why it's recommended or optional for this context
   - Pre-checked defaults based on detected mode (see mode detection above)
4. **Loop explanation**: the selected set is the scope-and-candidate approval gate; each selected framework will then be run inline (one findings page per framework) and the run advances by re-invoking `$journey-map`
5. **Approval gate**: framework selection confirmation

This multi-select approval **is** the Stage-1 scope approval for the whole selected set. Stop for compiled YAML. Do **not** write the run manifest or run any framework in this session — that is state C.

### 3b. State C — Run Next Pending Framework (inline)

This session consumes the approved multi-select YAML (state 0→C) or advances after a prior framework's approval. At the **head** of the session, do the light bookkeeping first:

1. **Write the run manifest** if it does not yet exist: `research/_working/journey-map-run.yaml` (flat) or `research/{slug}/_working/journey-map-run.yaml` (product-path), recording `selected_frameworks` with each framework's `slug` and canonical `intermediate` path. Include only frameworks the user selected.
2. **If a prior framework's reviewed content was just approved** by the pasted YAML, write its canonical intermediate `research/journey-map-{fw}.md` (or `research/{slug}/journey-map-{fw}.md`) from the already-reviewed working packet, and archive that framework's working packet and superseded review page. Do not mark framework completion inside the run manifest; completion is inferred from canonical intermediate existence only.

Then run the **one heavy phase**: determine the next pending framework (first selected framework whose canonical intermediate does not yet exist), then **load and follow that framework subskill's `SKILL.md` inline, entering at its research stage (Stage 2)** — the multi-select approval already satisfied the framework's Stage-1 scope gate, so perform the research, write its working packet, and build a single findings `review` page. Stop for that framework's compiled YAML.

**Advance the loop by self-re-invocation.** When a framework findings page is in `review`, end the terminal message with `## Next Work` telling the user to review the page and compile YAML, followed by `## Recommended Next Command After Compiling YAML` naming `$journey-map` with the same product/research path argument when present. After a framework's compiled YAML is approved and its canonical intermediate is written, recalculate pending frameworks from the manifest and filesystem before writing the handoff. If pending frameworks remain, end with `## Next Work` reporting progress as "k of N frameworks complete" and saying the next run executes the next pending framework, followed by `## Recommended Next Command` naming `$journey-map`. If no pending frameworks remain and canonical `journey-map.md` is missing, end with `## Next Work` saying the next run builds the unified synthesis review page, followed by `## Recommended Next Command` naming `$journey-map --synthesize` with the same product/research path argument when present. Do not emit cross-skill routing here — that happens only after synthesis.


### 4. State B — Synthesis (auto-detected; also `$journey-map --synthesize`)

Enter synthesis when the run manifest exists, **all** selected framework intermediates exist, and no canonical `research/journey-map.md` yet exists. An explicit `$journey-map --synthesize` also forces this state.

Read all intermediate framework outputs:
- `research/journey-map-jtbd-timeline.md`
- `research/journey-map-experience-map.md`
- `research/journey-map-customer-journey-canvas.md`
- `research/journey-map-service-blueprint.md`
- `research/journey-map-user-story-map.md`

At least one must exist. If none exist, tell user to run framework selection first.

Synthesize into unified `research/journey-map.md`:

**Synthesis includes:**
- Unified customer lifecycle: trigger, discovery, evaluation, onboarding, aha moment, conversion, transaction, retention, expansion, advocacy, churn, recovery
- User journey map per key persona with core use cases, entry points, task steps, decision points, happy path, failure modes
- Critical moments: the 3-5 moments where the product wins or loses the user/customer
- Evidence matrix: each claim mapped to which framework(s) support it
- Confidence levels per claim (strong/moderate/hypothesized)
- Stage detail index: links to deeper stage docs when they exist
- Journey gaps: stages needing deeper analysis
- Mode header: `> Mode: Pre-Product (hypothesized)` or `> Mode: Product-Exists (grounded)`

Build alignment page for synthesis approval with:
- Full proposed `research/journey-map.md` content
- Evidence matrix combining all framework sources
- Confidence/assumption register
- Critical-moment evidence matrix
- Proposed file changes gate
- Approval gate

After approval: write `research/journey-map.md`, then on this canonical write **archive the run manifest** (`journey-map-run.yaml`) and the synthesis working packet under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, update `research/.progress.yaml` `pipeline_stage` to `journey-map`, and emit the downstream next-step routing (step 6). This is the one place cross-orchestrator routing is allowed.

### 5. State C via Product-Exists Shortcut (`$journey-map product`)

Skip multi-select. Build a `review` alignment page for the shortcut plan with:

1. **Shortcut explanation**: product-exists shortcut selected and why `service-blueprint` + `user-story-map` are the fixed defaults
2. **Evidence readiness**: available product/customer evidence and any caveats
3. **Proposed framework set**: the fixed set that will be recorded in the run manifest
4. **Approval gate**: require final compiled YAML approval before writing the run manifest

Do not write the run manifest before alignment approval. The next action is review of the HTML alignment page.

After user approval via final compiled YAML, write this fixed framework set straight into the run manifest (`research/_working/journey-map-run.yaml` or the product-path equivalent):

```yaml
orchestrator: journey-map
selected_frameworks:
  - slug: service-blueprint
    intermediate: research/journey-map-service-blueprint.md
  - slug: user-story-map
    intermediate: research/journey-map-user-story-map.md
```

Then enter **state C** and run framework 1 inline per step 3b. The loop advances by re-invoking `$journey-map`.

### 6. Next Steps (after synthesis only)

Priority-ordered decision tree — recommend the **first** match:

1. **Blocking optional research trigger** — the overview exposed a stage, fit, measurement, or product-loop risk that must be resolved before positioning or UX choices harden → use the Optional Research Trigger Map below. Cite the exact journey evidence, why it blocks the next AFPS step, and which existing framework skill owns it.
2. **Positioning missing** (`research/positioning.md` does not exist) → check `.agents/project.json.enabled_packs` for `business-research` — if `business-research` is not enabled, recommend `npx skillpacks install business-research` from the project shell; if `business-research` is enabled, recommend `$positioning` — Positioning needs ICP, competitive analysis, and journey evidence, so it is the natural next step.
3. **Positioning done, user-flow map missing** → check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `npx skillpacks install product-design` from the project shell; if `product-design` is enabled, recommend `$user-flow-map` — Map screen flow, decisions, branches, states, and low-fidelity wireframe structure before UI requirements.
4. **Never** recommend `$spec-interview` from this skill — it is many steps downstream in the AFPS chain.

## Optional Research Trigger Map

These detours are conditional framework owners, not required AFPS chain links. Use them only when the journey evidence shows that the answer will change positioning, product-loop direction, flow/design shape, or prototype choices. When the trigger is absent, continue to `$positioning` or `$user-flow-map` using the decision tree above.

| Journey signal | Existing owner | Trigger threshold |
| --- | --- | --- |
| Signup, setup, activation, first-success, or time-to-value path is unclear | `$onboarding-map` | The journey cannot identify the first success path, onboarding drop-offs, or activation criteria well enough to shape UX. |
| Evaluation, trial, pricing decision, objections, or buyer roles are unresolved | `$conversion-map` | Conversion decision logic affects the primary screen flow, offer, or proof sequence. |
| Purchase, checkout, payment, fulfillment, refund, dispute, or trust state is material | `$transaction-map` | Transaction mechanics create product risk before UX/prototype choices. |
| Repeat-use job, return trigger, churn risk, recovery path, or retention signal is unclear | `$retention-map` | The product needs a natural return model before designing engagement, lifecycle messages, or saved state. |
| Stage instrumentation, leading indicators, or lifecycle handoff metrics are unclear | `$lifecycle-metrics` | The journey has stage risks but needs measurement before growth or implementation planning. Prefer this over `$hook-model` for enterprise, infrastructure, transactional, or naturally infrequent products. |
| Product value depends on repeat use, habit formation, engagement loops, retention triggers, saved state, social rewards, or investment compounding | Check `.agents/project.json.enabled_packs` for `business-growth` — if missing, recommend `npx skillpacks install business-growth` from the project shell; if enabled, recommend `$hook-model` | Use only for consumer, prosumer, PLG, marketplace, community, or B2B-with-consumer-component products where habit-loop design should shape flow and prototype choices before `$user-flow-map`. Do not force this on B2B/enterprise, infrastructure, transactional, or naturally infrequent products; route those to `$lifecycle-metrics` or, when `business-growth` is enabled and a broader success framework is needed, `$metrics`. |
| Expansion, upgrade, seat growth, referral, advocacy, or land-and-expand path is material | `$expansion-map` | Expansion mechanics change lifecycle sequencing, account roles, or product surface priorities. |
| Jobs, pains, gains, aha moment, or solution fit are weak, disputed, or need explicit scoring | Check `.agents/project.json.enabled_packs` for `business-research` — if missing, recommend `npx skillpacks install business-research` from the project shell; if enabled, recommend `$value-prop-canvas` | Use the existing Strategyzer-style framework only when fit risk would make positioning or UX premature. |
| Revenue, channel, cost, defensibility, or unfair-advantage assumptions are material risks | Check `.agents/project.json.enabled_packs` for `business-research` — if missing, recommend `npx skillpacks install business-research` from the project shell; if enabled, recommend `$lean-canvas` | Use the existing Ash Maurya Lean Canvas framework when the journey exposes business-model risk before UX/prototype decisions. |
| Pricing gates, packaging, free-to-paid timing, or willingness-to-pay moments are central to the journey | Check `.agents/project.json.enabled_packs` for `business-growth` — if missing, recommend `npx skillpacks install business-growth` from the project shell; if enabled, recommend `$monetization` | Use when pricing architecture must be grounded before conversion, transaction, or prototype choices. |
| Acquisition source, launch channel, messaging route, or early traction mechanism is a journey blocker | Check `.agents/project.json.enabled_packs` for `business-growth` — if missing, recommend `npx skillpacks install business-growth` from the project shell; if enabled, recommend `$gtm` | Use after enough ICP/competitive/journey evidence exists and the channel path changes product or UX priorities. |

`$growth-model` is an existing Reforge-style framework owner for compounding acquisition, retention, and monetization loops, but do not route to it directly from `journey-map` unless metrics/GTM prerequisites are already satisfied. In most AFPS cases, `$hook-model`, `$metrics`, `$monetization`, or `$gtm` is the earlier business-growth detour.

## Output

### State E output: framework multi-select `review` page + working packet

The multi-select page (see step 3a). The run manifest `research/_working/journey-map-run.yaml` is written at the head of the first state-C session on approval, not in state E.

### State C output: per-framework findings `review` page + `research/journey-map-{framework}.md`

One findings page per selected framework; the canonical intermediate is written on that framework's approval (see step 3b).

### State B output (synthesis): `research/journey-map.md` (or `research/{slug}/journey-map.md`)

```markdown
# Journey Map

> Based on: [list of framework outputs used]
> Date: [current date]
> Mode: Pre-Product (hypothesized) | Product-Exists (grounded)
> Frameworks applied: [list]

## Summary

## User Journeys

## Customer Lifecycle

## Critical Moments

## Evidence Matrix

| Claim | Supporting Framework(s) | Evidence | Confidence |
|-------|------------------------|----------|------------|
| [claim] | JTBD Timeline / Experience Map / Service Blueprint / User Story Map / Customer Journey Canvas | [source] | Strong / Moderate / Hypothesized |

## Stage Detail Index

## Journey Gaps

## Next Steps
```

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/journey-map-{topic}.html`.

**Journey research translation.** Render the lifecycle overview as approval-ready research, not a chat-only summary. The alignment page must include the proposed `research/journey-map.md` content, proposed file changes, evidence coverage by journey stage, assumptions/confidence register, critical-moment evidence matrix, and approval gates before canonical research files are created or updated.

Before approval, the next action is review of `alignment/journey-map-{topic}.html` and compiled YAML answers from that page. Do not treat a plain-text lifecycle summary as a substitute for the HTML alignment preview.

## Constraints

- **Parent self-advances one phase per invocation** and follows the next pending framework's subskill inline (entering at its research stage). It records the selected framework set in the run manifest, runs each selected framework inline, and synthesizes; progress is the existence of canonical intermediates. The loop advances by re-invoking `$journey-map` (fresh Codex session between sessions). Do not queue framework work in `tasks/todo.md` or hand it to `$exec`.
- **Synthesis requires at least one framework output.** Do not synthesize from zero evidence.
- **Mode detection is evidence-based.** Do not override mode detection without user confirmation.
- Ground every important step in ICP, research, specs, feedback, or codebase evidence.
- Do not prescribe UI or architecture.
- Present findings before writing.
- Follow the archive-first replacement policy for canonical research/spec documents.
- Do not overwrite existing `research/journey-map.md` without asking the user first.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
