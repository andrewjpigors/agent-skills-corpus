---
name: competitive-analysis
description: Orchestrator — select competitive-analysis frameworks, run them inline one per session, and synthesize market landscape findings
type: research
version: v0.25
argument-hint: "[optional: \"--synthesize\" | \"core\" | concept/category/competitors]"
invocation: orchestrator
context_intake: scoped
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. After install, tell Claude users to run `/reload-skills`, then `/clear` or restart if the skill remains invisible. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Competitive Analysis — Orchestrator

Invoke as `/competitive-analysis`.

This is a **Pattern A framework-decomposition orchestrator** that runs as a self-advancing **Research Session Loop** (see `docs/research-session-loop-convention.md` and the Execution Model below). It resolves product/research scope, recommends competitive-analysis frameworks, runs each selected framework inline one per session, and synthesizes the approved framework outputs into the canonical competitive landscape report. Individual frameworks live as child skills under `frameworks/`.

Available frameworks:

| Framework | Slug | Lens | Default |
|-----------|------|------|---------|
| Porter's Five Forces | `porter-five-forces` | Industry structure, power dynamics, substitutes, entrants, rivalry | Yes |
| SWOT | `swot` | Strengths, weaknesses, opportunities, threats against market evidence | Yes |
| Strategic Group Map | `strategic-group-map` | Competitive clusters, positioning axes, whitespace by segment | Optional |
| Feature/Pricing Matrix | `feature-pricing-matrix` | Capability, package, and price comparisons across alternatives | Yes |

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include downstream or cross-skill command recommendations while a scope, framework findings, or synthesis approval is pending. The approval request itself is the next action, and the only terminal command section allowed before approval is `## Recommended Next Command After Compiling YAML` and it must name this same parent orchestrator, such as `/competitive-analysis` plus the same product/research path argument when present. Parent-loop continuation is not downstream routing. Only emit downstream next-skill routing after the synthesized `competitive-analysis.md` artifact has been approved and written.

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

**Detect mode before proceeding:**

- **Concept-validation mode** activates when: no `research/icp.md` exists AND (no meaningful codebase — i.e. no README, no source files, no package config — OR `$ARGUMENTS` contains "concept" or "validate"). Use this mode to validate market gaps after a concept has been shaped by `/idea-scope-brief` or an equivalent brief; if no concept is clear, recommend `/idea-scope-brief` first. In this mode, announce to the user: "Running in concept-validation mode — no ICP or product detected. I'll evaluate the market gap for your concept." Then ask the user to describe the concept, the problem it addresses, and the intended audience.
- **Standard mode** (default): Read the codebase, README, CLAUDE.md, and existing research/specs (`research/icp.md` or `research/{slug}/icp.md`, `research/enterprise-icp.md` or `research/{slug}/enterprise-icp.md`, `research/mvp-gap.md` or `research/{slug}/mvp-gap.md`) to understand what the product does, who it's for, and what value it claims to provide. This context is essential for identifying the right competitors and evaluating positioning. If no codebase or specs exist but `research/icp.md` is present, proceed in standard mode using the ICP as context.
- Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. In standard mode, scope the full competitive analysis to the first entry in `active_paths` by default. Treat `product_paths[]` entries with `status: deferred` or `status: revisit_candidate` as parked product paths, not as extra full research tracks.

**Provisional product-path evidence.** When a referenced product path is not present in `research/.progress.yaml` (either absent entirely or not in `active_paths` or `product_paths[]`), do not treat it as a canonical active path. Before using it as source context, require an explicit provisional-path evidence reference: a `review-only-approved` alignment page (e.g., `alignment/idea-scope-brief-{topic}.html` with `approval_status: review-only-approved`) that fully renders the proposed path's concept, brief, and manifest entry. If no such evidence exists, ask the user whether to proceed with the path as unverified context or to run `/idea-scope-brief` first.

## Execution Model — Research Session Loop

This is a **self-advancing Pattern A research orchestrator** (see `docs/research-session-loop-convention.md`). Each invocation starts cold, resolves its state from **pasted YAML + filesystem**, runs **exactly one heavy phase**, emits the next gate, and stops. The user advances the loop by clearing context and re-invoking `/competitive-analysis`. The user never invokes a framework subskill directly — the orchestrator follows each selected framework's subskill inline.

When a framework is pending, the only user-facing continuation route is re-invoking `/competitive-analysis` with the same product/research path argument when present, for example `/competitive-analysis research/afps-tracker`. Never tell the user to run a path-shaped child framework command; the parent resolves the pending framework from the run manifest and filesystem.


### Terminal Handoff Contract

Every terminal response for this Research Session Loop must end with `## Next Work` and one command section. Use `## Recommended Next Command After Compiling YAML` only while a `review` page is waiting for compiled YAML. Use `## Recommended Next Command` only after approved YAML has been consumed and the approved artifact has been written or updated. Do not put any other section after the applicable command section.

### Self-Routing Continuation Payload

Every `review` alignment page this parent creates must include `agent_routing` in the bottom compiled YAML. The mapping routes a fresh agent back to this parent orchestrator; it does not authorize direct framework invocation or replace parent-owned state resolution. Use this shape, preserving the current product/research path argument when present:

```yaml
agent_routing:
  workflow: pattern-a-research-loop
  parent_skill: competitive-analysis
  command: "/competitive-analysis research/{slug}"
  product_path: research/{slug}        # omit in flat mode
  gate_owner: parent-orchestrator
  gate_type: framework-findings        # or framework-selection, shortcut-selection, synthesis
  framework_slug: <framework-slug>     # only for framework-findings gates
  framework_mode: inline-subskill      # only for framework-findings gates
  run_manifest: research/{slug}/_working/competitive-analysis-run.yaml
  next_resolution: parent-resolves-from-yaml-and-filesystem
```

For framework selection, shortcut, and synthesis gates, omit `framework_slug` and `framework_mode`; `gate_type` must name the actual gate. The `command` field must be the same parent command shown under `## Recommended Next Command After Compiling YAML`. The parent consumes the YAML, writes or amends the artifact, archives consumed sources, derives progress from the run manifest plus canonical-intermediate files, and decides whether to load a framework subskill inline.

For review-pending framework, selection, shortcut, or synthesis pages, `## Next Work` tells the user to review the alignment page and compile YAML, and the command section names `/competitive-analysis` with the same product/research path argument when present, then clear context before continuing. For post-write pending-framework states, `## Next Work` reports progress as "k of N frameworks complete" and says the next run executes the next pending framework; `## Recommended Next Command` names `/competitive-analysis`.

After every framework write, recalculate pending frameworks from the run manifest and canonical-intermediate files before writing this handoff. If no selected frameworks remain and canonical `competitive-analysis.md` is missing, `## Next Work` says the next run builds the unified synthesis review page, and `## Recommended Next Command` names `/competitive-analysis --synthesize` with the same product/research path argument when present. After approved synthesis writes canonical `competitive-analysis.md`, the final command section names only the first downstream command selected by the Next Steps decision tree.


State lives in two places only:

- **Run manifest** — `research/_working/competitive-analysis-run.yaml` (flat) or `research/{slug}/_working/competitive-analysis-run.yaml` (product-path). Records the selected framework set and each framework's intermediate path. Written when the multi-select YAML is approved. Shape:

  ```yaml
  orchestrator: competitive-analysis
  slug: skills-showcase            # omit in flat mode
  selected_frameworks:
    - slug: porter-five-forces
      intermediate: research/skills-showcase/competitive-analysis-porter-five-forces.md
    - slug: swot
      intermediate: research/skills-showcase/competitive-analysis-swot.md
  ```

- **Canonical-intermediate existence** — a selected framework is *done* when `research/competitive-analysis-{framework}.md` (or `research/{slug}/competitive-analysis-{framework}.md`) exists, *pending* otherwise. `pending = selected − existing-intermediates`. The manifest stores selection only, not per-framework status.

`research/.progress.yaml` stays coarse — its `pipeline_stage` is a pointer, not per-framework status.

### State resolution (resolve the first match; YAML first, then most-progressed A→E)

On each invocation, after Product-Path Scope Resolution (step 0), resolve state:

| State | Detected when | Heavy phase this session | Emits / stops with |
|---|---|---|---|
| **0 — pasted YAML** | a compiled alignment YAML is pasted | branch on `approval_status`: `ready-for-agent-review` → apply the approval for the gate it answers (light: write manifest and/or prior framework intermediate, archive consumed source), then fall through to the next pending state below; `not-approved` → amend the named page (refinement session) and stop | amended page, or proceeds ↓ |
| **A — done** | canonical `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) exists | — | done; emit next-skill route (synthesis step) |
| **B — synthesize** | run manifest exists, all selected intermediates exist, no canonical `competitive-analysis.md` (also forced by `--synthesize`) | **synthesis** (step 4) | synthesis `review` page |
| **C — run framework** | run manifest exists, ≥1 selected framework pending | **run next pending framework inline at its research stage** (step 3) | that framework's findings `review` page |
| **E — build selection** | no run manifest and no canonical (cold start) | establish context → mode detect → recommend frameworks → build multi-select page (steps 1–2) | multi-select `review` page |

### Re-entry Routing Guard

When a user re-invokes `/competitive-analysis`, treat existing progress as routing evidence before doing any status, audit, cleanup, or cold-start selection work:

- If a run manifest exists and at least one selected framework intermediate is missing, resolve directly to **State C** and run the first pending framework inline through this parent orchestrator.
- If no run manifest exists but legacy `tasks/todo.md` contains an approved `## Competitive Analysis Framework Execution` queue with child framework rows, treat that queue as compatibility evidence only: identify the first unchecked framework row, reconstruct the selected framework order from the queue, and run that first pending framework inline through this parent orchestrator.
- Do not rerun State E, perform a status audit, do bookkeeping-only cleanup, route to `/exec`, or tell the user to invoke path-shaped framework commands.
- Exception: if the user explicitly asks for status, re-scoping, queue cleanup, or synthesis, honor that explicit request instead of forcing State C.

**Cold entry (no state F).** This orchestrator uses `context_intake: scoped` — there is **no deep-interview phase**. A cold start (nothing on disk) resolves directly to **state E**; the 1–3 light scope questions in Context Gathering fold into the head of the E session rather than getting their own round-trip.

**Light vs heavy.** Recording the approved selection into the run manifest (state 0→C head), writing an already-reviewed framework intermediate, and archiving a consumed source are *light* — they fold into the head of the next heavy session. The heavy phase (one framework's research, synthesis) is the only thing isolated per session.

**Shortcuts.** `/competitive-analysis --synthesize` forces state B. `/competitive-analysis core` presets the state-E multi-select defaults to `porter-five-forces`, `swot`, and `feature-pricing-matrix` (the user may still add `strategic-group-map`); it does not skip the selection gate.

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

### 1. Establish Product Context

**Standard mode:**
- Read CLAUDE.md, README, package config, and key source files to understand the product
- Read `research/icp.md` (or `research/{slug}/icp.md`) if it exists — the customer profile, pain map, and value prop define the competitive frame
- Read `research/enterprise-icp.md` (or `research/{slug}/enterprise-icp.md`) and `research/mvp-gap.md` (or `research/{slug}/mvp-gap.md`) if they exist for additional context
- If `$ARGUMENTS` names specific competitors, preserve those as seeded competitors for framework subskills
- Summarise what the product does, who it's for, and what problem it solves

**Concept-validation mode:**
- Use `research/idea-brief.md` when present, otherwise use the concept description from Prerequisites to establish the problem space
- Summarise what the concept proposes (problem it addresses, intended audience, hypothesised approach)
- Confirm this understanding with the user before building the multi-select page

Write the context summary, resolved mode, candidate competitor categories, known competitors from arguments, and source gaps to `research/_working/preliminary-competitive-analysis-research.md` (or `research/{slug}/_working/preliminary-competitive-analysis-research.md`) so framework subskills inherit the same scope.

### 2. State E — Recommend Frameworks & Build Multi-Select Page

Recommend framework defaults based on context:

- **Always default**: `porter-five-forces`, `swot`, and `feature-pricing-matrix`.
- **Default `strategic-group-map`** when the category has more than five likely competitors, multiple segments, multiple buyer types, or the user asks for landscape/positioning whitespace.
- **Concept-validation mode**: keep `porter-five-forces` and `swot` defaulted; use `feature-pricing-matrix` only when named competitors or visible pricing alternatives exist; use `strategic-group-map` when the concept competes across multiple categories.
- **`core` shortcut**: default only `porter-five-forces`, `swot`, and `feature-pricing-matrix`; still allow the user to add `strategic-group-map`.

Build the framework multi-select `review` alignment page that includes: mode, product-path scope, context summary, selected/default frameworks, optional frameworks, which canonical sections each framework feeds, output paths, source coverage gaps, a loop explanation (the selected set is the scope-and-candidate approval gate; each selected framework is then run inline — one findings page per framework — and the run advances by re-invoking `/competitive-analysis`), and the approval gate.

This multi-select approval **is** the Stage-1 scope approval for the whole selected set. Stop for compiled YAML. Do **not** write the run manifest or run any framework in this session — that is state C.

### 3. State C — Run Next Pending Framework (inline)

This session consumes the approved multi-select YAML (state 0→C) or advances after a prior framework's approval. At the **head** of the session, do the light bookkeeping first:

1. **Write the run manifest** if it does not yet exist: `research/_working/competitive-analysis-run.yaml` (flat) or `research/{slug}/_working/competitive-analysis-run.yaml` (product-path), recording `selected_frameworks` with each framework's `slug` and canonical `intermediate` path. Include only frameworks the user selected.
2. **If a prior framework's reviewed content was just approved** by the pasted YAML, write its canonical intermediate `research/competitive-analysis-{fw}.md` (or `research/{slug}/competitive-analysis-{fw}.md`) from the already-reviewed working packet, and archive that framework's working packet and superseded review page.

Then run the **one heavy phase** for this session:

3. **Determine the next pending framework** = the first framework in `selected_frameworks` whose canonical intermediate does not yet exist.
4. **Load and follow that framework subskill's `SKILL.md` inline**, entering at its **research stage (Stage 2)**: the multi-select approval already satisfied the framework's Stage-1 scope gate, so perform the framework's research, write its working packet, and build a single findings `review` page for that framework. Stop for that framework's compiled YAML.

Framework intermediate paths (`research/{slug}/` in product-path mode):

- `research/competitive-analysis-porter-five-forces.md`
- `research/competitive-analysis-swot.md`
- `research/competitive-analysis-strategic-group-map.md`
- `research/competitive-analysis-feature-pricing-matrix.md`

**Advance the loop by self-re-invocation.** When a framework findings page is in `review`, end the terminal message with `## Next Work` telling the user to review the page and compile YAML, followed by `## Recommended Next Command After Compiling YAML` naming `/competitive-analysis` with the same product/research path argument when present. After a framework's compiled YAML is approved and its canonical intermediate is written, recalculate pending frameworks from the manifest and filesystem before writing the handoff. If pending frameworks remain, end with `## Next Work` reporting progress as "k of N frameworks complete" and saying the next run executes the next pending framework, followed by `## Recommended Next Command` naming `/competitive-analysis`. If no pending frameworks remain and canonical `competitive-analysis.md` is missing, end with `## Next Work` saying the next run builds the unified synthesis review page, followed by `## Recommended Next Command` naming `/competitive-analysis --synthesize` with the same product/research path argument when present. Do not emit cross-skill routing here — that happens only after synthesis.


### 4. State B — Synthesis (auto-detected; also `/competitive-analysis --synthesize`)

Enter synthesis when the run manifest exists, **all** selected framework intermediates exist, and no canonical `research/competitive-analysis.md` yet exists. An explicit `/competitive-analysis --synthesize` also forces this state. Read all existing `research/competitive-analysis-*.md` framework outputs for the active scope. At least one approved framework output must exist; if none exist, stop and ask the user to run `/competitive-analysis` to select and run frameworks first.

Synthesize across framework outputs into the canonical deliverables below:

- competitor landscape and categories
- company/product profiles
- observable GTM and pricing patterns
- market gaps and white-space opportunities
- implications for deferred product paths when evidence materially changes them
- concept-validation `## Gap Assessment` when the orchestrator context selected concept-validation mode
- `## Next Steps` using the unchanged routing contract below

Build the report-first alignment page before writing. Only after final compiled YAML approval, write canonical artifacts, then on this canonical write **archive the run manifest** (`competitive-analysis-run.yaml`) and the synthesis working packet under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, update `research/.progress.yaml` `pipeline_stage` to `competitive-analysis` (and any deferred-path evidence that changed), and emit the downstream next-step routing. This is the one place cross-orchestrator routing is allowed.

**Standard mode next steps:** `## Next Steps` section with a **Recommended** item and **Other options** (2-4 alternatives). Choose the recommended item by the first matching condition:

1. IF no `research/journey-map.md`: check `.agents/project.json.enabled_packs` for `customer-lifecycle` - if `customer-lifecycle` is not enabled, recommend `npx skillpacks install customer-lifecycle` from the project shell, first; if `customer-lifecycle` is enabled, recommend `/journey-map` - map the customer and user journey before solution-value decisions, using competitive gaps as inspiration
2. IF no `research/positioning.md`: `/positioning` - frame the market category and alternatives after journey evidence shows where value is delivered
3. IF no `specs/user-flow-*.md`: check `.agents/project.json.enabled_packs` for `product-design` - if `product-design` is not enabled, recommend `npx skillpacks install product-design` from the project shell, first; if `product-design` is enabled, recommend `/user-flow-map [top journey-backed market gap or positioning opportunity]` - map flow structure before UI requirements, layout variants, and production specification
4. IF no `research/value-prop.md` AND solution-customer fit is weak, disputed, or needs explicit fit scoring: `/value-prop-canvas` - validate contested solution-fit evidence as an optional detour
5. IF no `research/gtm.md`: check `.agents/project.json.enabled_packs` for `business-growth` - if `business-growth` is not enabled, recommend `npx skillpacks install business-growth` from the project shell, first; if `business-growth` is enabled, recommend `/gtm` - build go-to-market plan leveraging competitive gaps
6. IF codebase exists and no `research/mvp-gap.md`: check `.agents/project.json.enabled_packs` for `business-ops` - if `business-ops` is not enabled, recommend `npx skillpacks install business-ops` from the project shell, first; if `business-ops` is enabled, recommend `/mvp-gap` - check if the codebase exploits the gaps found

Use this format in the output:

## Next Steps

**Recommended:** `[first matching command above]` - [reason grounded in this analysis]

Other options:
- `npx skillpacks install customer-lifecycle` from the project shell, or `/journey-map` - map the customer journey to find where competitors fall short (if no `research/journey-map.md` and not recommended; check `.agents/project.json.enabled_packs` for `customer-lifecycle` - if not enabled, recommend `npx skillpacks install customer-lifecycle` from the project shell; if enabled, recommend `/journey-map`)
- `/positioning` - frame the market category and competitive alternatives after journey evidence exists (if no `research/positioning.md` and not recommended)
- check `.agents/project.json.enabled_packs` for `product-design` - if `product-design` is not enabled, recommend `npx skillpacks install product-design` from the project shell, first; if `product-design` is enabled, recommend `/user-flow-map [top journey-backed market gap or positioning opportunity]` - map flow structure before UI requirements, layout variants, and production specification (if positioning exists and not recommended)
- `/value-prop-canvas` - optional detour only when solution-customer fit is weak, disputed, or needs explicit fit scoring before positioning/spec work
- check `.agents/project.json.enabled_packs` for `business-growth` - if `business-growth` is not enabled, recommend `npx skillpacks install business-growth` from the project shell, first; if `business-growth` is enabled, recommend `/gtm` - build go-to-market plan leveraging competitive gaps (if no `research/gtm.md` and not recommended)
- check `.agents/project.json.enabled_packs` for `business-ops` - if `business-ops` is not enabled, recommend `npx skillpacks install business-ops` from the project shell, first; if `business-ops` is enabled, recommend `/mvp-gap` - check if the codebase exploits the gaps found (if codebase exists, no `research/mvp-gap.md` exists, and not recommended)
- check `.agents/project.json.enabled_packs` for `product-design` - if `product-design` is not enabled, recommend `npx skillpacks install product-design` from the project shell, first; if `product-design` is enabled, recommend `/brainstorm` - generate alternative solution ideas (only if the analysis found multiple plausible market gaps and product direction is still unclear)

Only include items whose conditions are met. Do not recommend brainstorm just because competitive whitespace exists.

**Concept-validation mode next steps:** Use the same Recommended + Other options format, but choose the recommendation from the validated `## Gap Assessment` verdict:

## Next Steps

**Recommended:** [verdict-based next step] - [reason grounded in the gap assessment]

Other options:
- IF verdict is **Proceed to Customer Discovery**: recommend `/customer-discovery` - the competitive gap is validated; define who to build for
- IF verdict is **Pivot concept**: recommend `/brainstorm` - the market has a gap, but this concept needs a different angle before ICP work is useful
- IF verdict is **Abandon**: recommend `No follow-up skill recommended` - the analysis did not find a meaningful gap worth pursuing; include `/brainstorm` only if the user wants to explore a new concept
- `/competitive-analysis` - re-run in standard mode after ICP is defined (only after a proceed verdict and after `/customer-discovery` creates `research/icp.md`)

## Output

### `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`)

```markdown
# Competitive Analysis

> Product: [product name and one-line description]
> Category: [market category]
> Date: [current date]
> Sources: [number of competitors analysed]

## Summary
[3-5 sentences: competitive landscape overview, our positioning, and the biggest opportunity]

## Competitive Landscape

### Direct Competitors
For each:
- **[Competitor Name]** — [one-line description]
  - Stage: [pre-launch / early / growth / mature / declining]
  - Founded: [year] | Funding: [amount or "bootstrapped"] | Team: [size estimate]
  - Pricing: [model and range]
  - GTM: [primary strategy]
  - Strengths: [2-3 bullets]
  - Weaknesses: [2-3 bullets]
  - Key takeaway: [what we can learn]

### Indirect Competitors
[Same format]

### Incumbents & DIY Alternatives
[Same format, briefer]

### Emerging Players
[Same format, briefer]

## Observable GTM Patterns
- **Dominant acquisition model**: [PLG / sales-led / community-led / etc. — as observed]
- **Pricing models seen**: [what competitors charge and how — from public pricing pages]
- **Common channels**: [where competitors are visibly present]
- **What works in this market**: [patterns from successful competitors]
- **What doesn't work**: [patterns from struggling competitors]

## Gap Assessment (concept-validation mode only)

### Market State
[Virgin / Sparse / Crowded — with evidence]

### Incumbent Quality
[Dominant-and-loved / Dominant-but-resented / Fragmented-and-mediocre / Emerging-and-unproven — with evidence]

### Gap Quality
[Clear unmet need / Underserved segment / UX/approach gap / Minor improvement / No meaningful gap — with evidence]

### Verdict
[Proceed to Customer Discovery / Pivot concept / Abandon — with reasoning]

## Market Gaps
- **[Gap title]** — [Description of the unmet need, who it affects, and why it exists]
- ...

## Competitive Positioning

### Market Gaps Identified
[Specific gaps, unserved segments, and white-space opportunities with evidence]

### Lessons from Competitors
- **Do this** (learned from [competitor]): [what they did well that we should emulate]
- **Avoid this** (learned from [competitor]): [what they did poorly that we should avoid]
- ...

Positioning recommendations ("where we fit", "recommended positioning") belong in `/positioning`.

<!-- Include this section only when downstream impact is Minor or Major. Omit entirely for None. -->
## Downstream Impact

> Checked: [list of downstream docs checked]
> Impact: Minor | Major

### Conflicts Found

1. **research/[file].md** — [Section Name]
   - **Stale**: "[exact quote from downstream doc]"
   - **Now**: [what this skill's output says instead]

[For Major only:]
> **Recommended action**: Run `/reconcile-research` to audit and fix all affected downstream documents.

## Next Steps

**Recommended:** [first matching item from the step 4 synthesis routing list]

**Other options:**
- [remaining conditional items from the step 4 synthesis routing list — only include items whose conditions are met]

## Signals for Downstream Research

> Raw signals captured during research. These are unvalidated observations —
> use the linked skill to verify, validate, and explore alternatives.

### → /positioning
- [signal]: positioning gaps identified in the landscape
- [signal]: category whitespace or unclaimed territory
- [signal]: differentiation opportunities from competitor weaknesses

### → /gtm
- [signal]: competitor channel strategies observed
- [signal]: pricing models and tiers seen across competitors
- [signal]: messaging patterns that appear effective

### → /monetization
- [signal]: competitor pricing tiers and structures
- [signal]: freemium vs. paid patterns in the market
- [signal]: enterprise pricing signals from competitor pages

### → /value-prop-canvas
- [signal]: competitor strengths and weaknesses mapped to customer jobs
- [signal]: unmet customer needs revealed by competitor gaps
- [signal]: value delivery patterns across the landscape
```

### `research/competitive-analysis-search-log.md` (or `research/{slug}/competitive-analysis-search-log.md`)
Raw research log — every search query, key findings with source attribution, and the reasoning behind categorisation and positioning recommendations.

### `research/.progress.yaml`
Update only when active-path evidence changes a deferred product path's status, reason, evidence refs, revisit trigger, or next skill. Use `product_paths` terminology instead of branch terminology. When writing manifest entries, include `pipeline_stage: competitive-analysis` on the active path entry.

Create the `research/` (or `research/{slug}/`) directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Use web search extensively.** Framework execution and synthesis must be grounded in real, current market data — not assumptions or hallucinated competitor names. Every competitor cited must come from a web search result.
- **Cite sources.** When stating facts about competitors (funding, features, pricing), note where the information came from.
- **Be honest about uncertainty.** If information couldn't be verified, say so. Don't fabricate metrics.
- **Stay in analysis mode.** Do not propose product changes, architecture, features, or positioning recommendations — product changes are for `/spec-interview` and `/mvp-gap`; positioning is for `/positioning`.
- **Focus on actionable insights.** Raw competitor lists are easy; the value is in the synthesis — gaps, patterns, positioning angles.
- **Do not overwrite existing `research/competitive-analysis.md`** (or `research/{slug}/competitive-analysis.md`) without asking the user first.
- **Keep research current.** Prefer recent sources (last 12 months). Flag any information that may be outdated.
- **Search breadth over depth initially.** Cast a wide net to find all competitors before going deep on each one. It's better to identify 15 competitors and research 8 deeply than to miss half the landscape.
- **Present before writing.** Never write output files until findings have been presented to the user and validated through the checkpoint questions. The user must see and approve the analysis before anything is written to disk.
- **Parent self-advances one phase per invocation** and follows the next pending framework's subskill inline (entering at its research stage). It records the selected framework set in the run manifest, runs each selected framework inline, and synthesizes; progress is the existence of canonical intermediates. The loop advances by re-invoking `/competitive-analysis` (clear context between sessions). Do not queue framework work in `tasks/todo.md` or hand it to `/exec`.
- **Keep framework subskills parent-owned.** Framework subskills must not emit `Recommended next skill`, path-shaped child framework commands, execution-loop commands, or downstream commands. Inline framework handoffs use only the parent-owned `## Next Work` and command sections.

## Context Gathering

**Step 1 — Scope questions.** Before building the multi-select page, ask the user 1–3 questions via `AskUserQuestion` only if the product/service, target audience, or decision goal is unclear from the repository and arguments. These light questions fold into the head of the state-E session.

**Step 2 — Framework selection.** Use the answers plus repo context to choose defaults and present the framework multi-select `review` alignment page (state E). The run manifest is written at the head of the first state-C session on approval, not in state E.

**Step 3 — Synthesis validation.** In `/competitive-analysis --synthesize`, present the 3–5 most important cross-framework findings before building the final approval alignment page.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/competitive-analysis-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
