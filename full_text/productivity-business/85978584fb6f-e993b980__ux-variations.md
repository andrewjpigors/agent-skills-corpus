---
name: ux-variations
description: Interview and plan multiple UX and UI variations for a product, page, or flow, including onboarding, typical workflows, sharing, collaboration, return use, and interface alternatives users can compare before locking a direction — and concrete visual/layout UI variations (component choices, spatial arrangements, information density)
type: planning
version: v0.28
required_conventions: [alignment-page, design-tree-loop, interrogation-page]
argument-hint: "[optional: app, page, flow, feature, or existing UI spec] [--layout-mode] [--no-chunk]"
context_intake: scoped
visual_tier: prototype
---

# UX Variations

Invoke as `/ux-variations`.

Use this skill when the user wants to explore multiple UX/UI directions before committing to a final experience. In the default product-design tree, this skill expands one specific user flow from `/user-flow-map` into alternate progression branches: different ways users can enter, advance, recover, hand off, complete, or abandon the flow. It then creates variation plans for flow progression, layout implications, navigation models, interaction patterns, component choices, content density, visual tone, and behavior so the user can compare, test, and decide which branch should move into `/ui-interview`.

In the normal AFPS product route, use `/user-flow-map` first to establish the wireframe-tree root and name the user-flow branches. Then run `/ux-variations [specific-user-flow]` to explore alternate ways users can progress through that selected flow. After a variation branch is ready for UI treatment, route that branch to `/ui-interview [specific-ux-variation]` for visual mockup, alignment, approval/rejection, and next-branch routing.

When `/state-model` ran between `/user-flow-map` and this skill, **consume `design/domain-model-{topic}.md` (and `design/model-tree-{topic}.yaml`) when present** as the logical substrate every variation re-skins: the entities, state machines, events, and logical contracts are fixed by the flow, while this skill varies how they are presented and progressed through. This is a soft input, not a hard gate — proceed without it when it is absent.

Follow `DESIGN-TREE-LOOP.md` for prototype-phase routing, state storage, approval boundaries, and task classification. UX progression and layout branch state belongs in `design/**/flow-tree-*.yaml`, not Pattern A selected-framework manifests, `research/.progress.yaml`, or `tasks/todo.md`.

Use `/user-flow-map` first when the interface has no credible flow structure. Use this skill directly only when a user-flow map, current implementation, screenshot, prototype, explicit user prompt, or clear feature scope already identifies the flow being varied. Do not require a finalized UI requirements spec before default UX variation work; the point is to compare alternative progression paths before a single branch becomes a UI proposal.

When invoked with `--layout-mode` (or when the user says "layout mode", "layout variations", or "UI variations"), this skill operates at the concrete component/layout level — it varies HOW the same content is presented visually, not WHAT the user flow is. Layout-mode is an explicit bounded mode for cases where both the flow and content contract are already fixed; otherwise default to progression-path UX variations. Layout-mode takes a fixed flow contract from `design/user-flow-[topic].md` plus a fixed content contract from `design/ui-requirements-[topic].md` or equivalent and generates 2-5 concrete visual/spatial approaches: different container patterns, detail views, navigation styles, density levels, and responsive strategies. Each variation is specified well enough to build as a lightweight implementation, then evaluated through `/uat --variant-evaluation` (check `.agents/project.json.enabled_packs` for `product-testing` — if `product-testing` is not enabled, recommend `npx skillpacks install product-testing` from the project shell, first) before `/consolidate-prototypes`.

## Design-Tree Flow

This skill runs the unified **5-stage design-tree flow** (`interrogation → research → design → plan → implement(scoped)`) from `DESIGN-TREE-LOOP.md`, scoped to the **UX-variation branches** it grows (up to five `ux_variations[]` on one modelled user-flow branch). The `## Process` steps below group by stage:

- **Stage 0 — Interrogation**: the stage-zero loop in `## Interrogation Page` / `INTERROGATION-PAGE.md` plus the variation-scope and concept-set checkpoints — confirm what varies vs. stays fixed and the concept set before authoring.
- **Stage 1 — Research**: resolve context — read the parent user-flow doc, the branch's `design/domain-model-{topic}.md` substrate when present, and existing UI/inspiration evidence.
- **Stage 2 — Design**: author the concept set and up to five build-grade proposed variation specs for review.
- **Stage 3 — Plan**: the approved variation set is the branch-selection input for `/ui-interview`; `/user-flow-map --prototype-build-plan` creates the later prototype ledger only after approved UI experiment branches exist.
- **Stage 4 — Implement (scoped)**: assemble the complete proposed variation plan for the alignment page, then after confirmed approval write the canonical variation specs and grow up to five `ux_variation` child branches on the modelled flow.

**Per-branch iteration contract.** Each session cold-starts, reads the flow-tree manifest, resolves the next eligible modelled user-flow branch lacking `ux_variations`, runs the staged flow scoped to it, grows the child branches on approval, and stops with the handoff in `## Next Work`. Branch selection order: explicit user override, journey_sequence, activation_fit, first_value_fit, evaluation_priority, status, then stable array order. Do not use raw first-pending array order as the default branch selector. A branch will not grow UX branches until its `model_ref` is confirmed. When an explicit user override changes branch order or branch choice, record the override and rationale in the flow-tree manifest before authoring.

**Modify-back.** A downstream `modify` decision can re-open this branch's `model_ref` or its parent user-flow branch via `targets[]`; when an upstream node re-opens, these UX variations are marked stale and re-authored once the upstream node is re-approved.

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

When product path `{slug}` is active, read and write research under `research/{slug}/`, pre-prototype design artifacts under `design/{slug}/`, finalized post-prototype implementation specs under `specs/{slug}/`, and treat top-level `research/*.md` and `design/*.md` files as flat-mode documents or cross-path summaries.

### 0b. Design Flow Tree Manifest

Use `design/flow-tree.schema.json` as the machine-readable contract for the pre-prototype product-design tree.

- Product-path mode reads and updates `design/{slug}/flow-tree-{topic}.yaml`.
- Flat mode reads and updates `design/flow-tree-{topic}.yaml`.
- On approval, add one `ux_variations[]` entry under the selected parent user-flow branch for each approved progression branch. Each entry must include `id`, `label`, `status`, and artifact references.
- Keep UX variation branch state in the design manifest. Do not write ordinary UX branch state to `research/.progress.yaml`; use that file only when a variant or route experiment creates a materially different product path or product line.
- Do not mirror UX progression, layout-variation, UI review, prototype build, or branch decision progress into `tasks/todo.md`.

### 0c. Session model — chunked spec sessions vs. one continuous session

This skill authors up to five full build-grade variation specs (step 7), and holding all of them in one context is the dominant per-session cost. After the concept-set checkpoint (step 6), decide the session model from the approved concept count: if **N ≥ 4** and `--no-chunk` was not passed, enter **chunked mode**; otherwise run straight through in one continuous session exactly as a single pass through steps 0–9. Chunked mode follows the **Intra-Skill Substep Chunking + Shared Context Brief** mechanism in `DESIGN-TREE-LOOP.md`: a setup session (steps 0–6) writes a pure-context brief and stops; one spec session per variation (step 7) authors a single variation's intermediate; and a final assemble+approve session (steps 8–9 + deliverables + the one alignment page) assembles the canonical plan behind the single existing alignment gate. The progress cursor is intermediate-file existence — the brief carries no step list, and there is no schema change and no `tasks/todo.md` use. For N < 4 or when `--no-chunk` is passed, write no brief and no intermediates and behave exactly as v0.20 did, so small runs stay cheap.

#### Required Progress Handoff Block

Every chunked stop (setup, each variation spec session, and the assemble-ready handoff) must start `## Next Work` with the Progress Handoff Block from `DESIGN-TREE-LOOP.md`. The block must include:

- `**Progress Handoff — ux-variations/<topic-or-branch>**` as the first line.
- `Completed: <completed variation count> / <approved variation count>.`
- `Durable cursor: checked design/{slug}/_working/ux-variations-{topic}-brief.md and design/{slug}/ux-variations-{topic}/.`
- `Current phase complete: <setup | variation thesis | assemble preparation> is complete.`
- `Next phase: <plain-English variation thesis or assemble+approve work>.`
- `Why repeat this command: the repeated command is intentional; /ux-variations cold-starts, reads the durable cursor, and advances the next pending variation or assembly.`
- `Session guidance: fresh session recommended for heavy next work; continuing in this session is allowed only if enough context remains.`
- `Exact next command: /ux-variations <literal topic-or-branch>.`

Use the same `/ux-variations` command for setup → first variation, variation → next variation, and final variation → assemble+approve; explain that the repeated command is intentional because filesystem existence is the cursor.

1. **Resolve context**
   - Read `.agents/project.json` if it exists.
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `research/`, task files, screenshots, route files, and component implementations when present.
   - Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Use `active_paths` as the product/app focuses and treat deferred `product_paths[]` as parked product directions, not required UX variants.
   - Prefer existing `design/user-flow-*.md`, product-path-scoped equivalents, and `design/**/flow-tree-*.yaml` as the normal AFPS input; select one named user-flow branch as the variation surface.
   - Read `design/domain-model-*.md` and `design/**/model-tree-*.yaml` when present (a sibling `/state-model` pass) as the fixed logical substrate — entities, state machines, events, and logical contracts the variations must preserve while varying presentation and progression. Soft input only; proceed without it when absent.
   - Also read `design/ui-*.md`, product specs, journey maps, ICP research, positioning research, finalized implementation specs, and user feedback as source evidence.
   - If no credible flow structure exists, run or recommend `/user-flow-map` before developing variants.
   - If the user explicitly requests layout-mode and no credible content/data/action contract exists, run or recommend `/ui-interview --requirements-only` before developing layout-mode variants.

2. **Define the decision surface**
   - Identify what the user is deciding: the selected user flow, onboarding, activation, typical workflow, sharing flow, collaboration model, purchase flow, editor, dashboard, settings, mobile experience, page layout, or another bounded surface.
   - Identify the parent user-flow branch, the upstream `user-flow-map` source, and any sibling user flows or prior UX/UI proposals that this variation must coordinate with.
   - Identify which dimensions may vary: first-run onboarding, activation, core workflow sequencing, sharing, invitations, permissions, collaboration, return-use loops, notifications, reminders, status surfaces, user or device handoffs, failure recovery, information architecture, navigation, page layout, task flow order, component model, data density, visual hierarchy, motion, copy tone, and mobile behavior.
   - Identify fixed constraints: brand, stack, design system, must-keep components, accessibility, launch scope, performance, and business requirements.
   - **Default progression-mode addition**: For each selected user flow, identify which parts may vary: entry route, sequencing, step granularity, user choice points, system automation, handoff points, review/edit loops, save-for-later behavior, cancellation, recovery, permissions, notifications, and completion criteria. Preserve the parent flow boundary while allowing progression branches to differ meaningfully.
   - **Layout-mode addition**: In layout-mode, read `design/user-flow-[topic].md` as the fixed screen-flow contract and `design/ui-requirements-[topic].md` as the fixed content contract. The WHAT and flow order are locked; only the HOW varies. Layout dimensions that can vary:
     - Container pattern: card grid, data table, list, kanban, timeline, tree, masonry
     - Detail pattern: sidebar panel, full-page route, modal, drawer, inline expand, popover
     - Navigation: top-nav, side-nav, tab-based, breadcrumb-driven, command-palette, hybrid
     - Density: compact, comfortable, spacious
     - Hierarchy: content-first, chrome-first, action-first
     - Responsive strategy: reflow, collapse, separate mobile layout, progressive disclosure

3. **Surface assumptions before probing**
   - Present a UX Variation Assumptions Manifest before deep questioning.
   - Tag assumptions with `[from spec]`, `[from codebase]`, `[from research]`, `[from artifact]`, or `[inferred]`.
   - Cover target users, usage context, parent user flow, selected branch scope, first-run moment, activation event, "aha" threshold, typical repeat-use workflow, sharing and collaboration assumptions, permissions, return triggers, notifications, re-engagement assumptions, handoffs, pain points, locked versus open decisions including which parent-flow moments may vary, evaluation criteria, required variant breadth, prototype fidelity, implementation budget, success metrics, and selection method.
   - Use AskUserQuestion to ask the user to confirm, correct, or flag assumptions before proceeding.
   - Deliver every manifest/checklist/checkpoint the user must confirm inline as the final message text of its own turn; ask the confirmation question in the next turn. AskUserQuestion option previews may mirror the content as a supplement but are never the sole channel. Never emit it only as mid-turn text in a turn that ends with a tool call — harness rendering does not guarantee mid-turn text is shown. A confirmation question must never reference content the user has not been shown.

4. **Interview for variation goals**
   - Ask 1 to 3 focused questions per turn using AskUserQuestion.
   - Default to maximally contrasting archetypes. Do not ask how different variants should be — assume dramatic contrast unless the user explicitly requests graduated steps.
   - Default evaluation method is: route each approved progression branch to `/ui-interview [specific-ux-variation]` for a concrete UI proposal and review decision before prototype build-plan synthesis. Built comparison and `/uat --variant-evaluation` come later, after `/user-flow-map --prototype-build-plan` creates UI-linked prototype items. Do not ask who will judge — assume solo evaluator building and gut-checking unless the user states otherwise.
   - When presenting a design decision with 3+ plausible answers during the interview, always include "Make this a variant axis (test all approaches)" as an option. When the user has already chosen "test all" for a prior question in the same session, default subsequent ambiguous decisions to variant axes without asking.
   - Establish which user flow from the wireframe tree is being expanded, what the variants must accomplish, which progression moments can vary (entry, sequencing, decision points, handoffs, recovery, completion, and re-entry), how a new user arrives and reaches first value, what the normal repeat workflow looks like, what users create/save/share/export/invite others into, what roles or permission levels exist, what notifications or status updates users expect, how users resume work after time away, what happens when a workflow is abandoned or blocked, which current interface parts work, which parts feel wrong or uncertain, what would make a variant unacceptable, and what evidence will decide the winner.
   - When the user is unsure, recommend a practical default and explain why.
   - **Layout-mode interview additions**: When in layout-mode, also ask:
     - What is the primary user task on this page? (scan, search, create, compare, monitor, triage)
     - How much data will typically be visible? (5 items, 50 items, 500 items)
     - Are there reference apps or pages the user admires for this type of content?
     - Are any layout patterns explicitly off the table?
     - What is the build budget per variation? (quick prototype, medium fidelity, production-ready)
     - What must the user do in each built variant before they are ready to consolidate?

5. **Create distinct variation concepts**
   - Produce 5 variations by default. Present the concepts for adjustment — do not ask the user to choose a count first.
   - Each variation must be meaningfully different, not just a color or spacing change.
   - At this stage, keep each concept lightweight: name, thesis, archetype, best-fit user/context, core workflow difference, major tradeoff, and rough complexity. Do not fully specify screens, controls, or implementation details yet.
   - Useful archetypes include task-first workflow, data-dense operator console, guided step-by-step flow, onboarding-first activation path, collaboration-first workspace, sharing-first artifact flow, notification/status-driven workflow, role-based handoff workflow, visual canvas or board, command/search-first interface, mobile-first progressive disclosure, familiar SaaS dashboard, and editorial or showcase layout.
   - Only choose archetypes that fit the product and user context.
   - **Layout-mode archetypes** (use these instead of the UX-flow archetypes above when in layout-mode):
     - Card grid: visual items in a responsive grid, good for browsing and scanning
     - Data table: dense rows with sortable/filterable columns, good for operators and power users
     - List + detail panel: master list on left, detail sidebar on right, good for email/messaging patterns
     - Full-page detail: list view navigates to full-page item view, good for content-heavy items
     - Kanban / board: columns representing states or categories, good for workflow and status tracking
     - Timeline / feed: chronological stream, good for activity, logs, and social patterns
     - Dashboard mosaic: mixed widget grid with charts, lists, and stats, good for monitoring and overview
     - Split-pane workspace: resizable panels for parallel content, good for editors and comparison
     - Command-first minimal: search/command bar with minimal chrome, good for keyboard-heavy power users
     - Sidebar-driven: persistent sidebar navigation with content area, good for settings and multi-section apps

6. **Concept selection checkpoint**
   - Before fully specifying any variant, ask the user to adjust the concept set.
   - Use bounded wording such as: "How should I adjust these UX variants before writing the final spec?"
   - Present clear options:
     - Keep all concepts
     - Make one concept bolder or more extreme
     - Add another concept
   - Do not ask the user to remove or merge concepts before they have been built. Pre-build narrowing is consistently rejected.
   - Ask the user to name the affected concept and briefly describe the change when they choose anything other than keeping all concepts.
   - Recommend a practical default when evidence supports it; do not imply that variants have already been built or committed.
   - Revise the concept set based on the answer before moving on.
   - **Chunked-mode setup handoff**: When chunked mode is active (step 0c — N ≥ 4 approved concepts and no `--no-chunk`), this checkpoint is the end of the setup session. Write the shared context brief to `design/{slug}/_working/ux-variations-{topic}-brief.md` (flat mode: `design/_working/ux-variations-{topic}-brief.md`) containing **pure context only** — the decision surface, confirmed assumptions, locked shared constraints (technical stack and design system), the N concept theses, the evaluation criteria, and any carried decisions — with **no step list and no status field**. Record proposed branch IDs and artifact paths in the brief/intermediates only; do not initialize or update scoped flow-tree `ux_variations[]` entries before alignment approval. Then STOP and emit the **Terminal handoff format** from `DESIGN-TREE-LOOP.md` plus the required Progress Handoff Block: state the brief was written, name the **first** variation to spec in **plain English** (its concept thesis, never only the internal `{variation-id}`), explain why the same `/ux-variations` command is repeated, and give the **exact** resolved next command with `{slug}`/`{topic}` filled in, e.g. `/ux-variations alignment-page-review` writing into `design/alignmeant/ux-variations-alignment-page-review/{variation-id}.md`, so each variation gets its own cold spec session (step 7). In non-chunked mode, continue directly to step 7 in this same session.

7. **Specify each approved variation enough to build**
   - **Chunked-mode spec session (one variation per session)**: When chunked mode is active, each spec session reads the brief at `design/{slug}/_working/ux-variations-{topic}-brief.md` and scans which `{variation-id}.md` files already exist under `design/{slug}/ux-variations-{topic}/`. Pick the first variation whose intermediate file does **not** yet exist, write its full build spec (the attribute list below, plus the layout-mode additions when applicable) to `design/{slug}/ux-variations-{topic}/{variation-id}.md`, append any cross-variation facts to the brief, then STOP and emit the **Terminal handoff format** from `DESIGN-TREE-LOOP.md` plus the required Progress Handoff Block: state the intermediate just written, name the next missing variation in **plain English** (its concept thesis, never only the internal `{variation-id}`), explain why the same `/ux-variations` command is repeated, and give the **exact** resolved next command, e.g. `/ux-variations alignment-page-review`. When the variation just written was the last one, the handoff points to the assemble+approve session instead of another spec session. Continue-vs-stop framing follows that convention's Routing Rules. Context per session is the brief plus one spec. In non-chunked mode, specify all approved variations in this same session as before. The spec content below is identical in both modes — chunking changes only how many variations one session writes.
   - For each variation, define name and thesis, parent user flow and branch relationship, target user fit, onboarding and activation model, typical workflow sequence, progression model (how the user advances through the flow and how this differs from sibling variations), sharing and collaboration model, permissions model, return-use and notification model, failure recovery behavior, page and flow changes, navigation model, screen-by-screen layout, key components and controls, button and link behavior, spatial density, sizing, hierarchy, responsive behavior, visual tone, strengths, risks, failure modes, implementation complexity, UI review scope, and the user signal that would make this branch ready for `/ui-interview`.
   - **Layout-mode variation spec additions**: In layout-mode, each variation spec must also include:
     - Content-to-component mapping: which content requirement maps to which UI component
     - Page regions with approximate proportions (e.g., sidebar 280px, content fluid, detail panel 400px)
     - Primary content component (the main way items are displayed)
     - Detail view pattern (how a single item's full details are accessed)
     - Action placement (where create, edit, delete, and bulk actions live)
     - Navigation pattern and placement
     - Responsive behavior at 3 breakpoints (mobile ≤640px, tablet ≤1024px, desktop >1024px)
     - Density approach (line-height, padding, font sizes, information per viewport)
     - States rendering (how empty, loading, error, and partial states appear in this layout)
     - Implementation file list (components, routes, layouts to create or modify)
     - Estimated build time (hours)
     - Variant evaluation task: the user task to perform in this variation before consolidation
     - Evidence to capture: screenshots, notes, time-to-complete, friction points, and acceptance/rejection signals

8. **Plan experimentation**
   - **Chunked-mode assemble+approve session**: When chunked mode is active, begin this session only once every approved variation's `{variation-id}.md` intermediate exists under `design/{slug}/ux-variations-{topic}/`. Assemble those per-variation intermediates into proposed whole-set review content for the final `design/{slug}/ux-variations-[topic].md` deliverable, then run this experimentation step and the coverage checkpoint (step 9) over the whole proposed set and build the **one** alignment page before any canonical writes. Before stopping for approval, emit the required Progress Handoff Block with the completed count equal to the approved variation count, the durable cursor checked, and the next phase described as whole-set alignment review and approval. On approval, write the final variation plan and interview log, create or update the scoped flow-tree `ux_variations[]` status/artifact entries, and archive the brief and the per-variation intermediates per the convention's archive-at-canonical-write timing. There is exactly one alignment gate for the whole set, not one per variation, so whole-set comparison is preserved.
   - Recommend serial full buildout of all approved variants only when the user is using `--layout-mode` or explicitly records an ad hoc bypass that asks to compare built interfaces before UI interview approval. Do not recommend building a subset first unless the user asks for a smaller experiment.
   - In default progression mode, route experiments are proposed validation targets only until an approved `/ui-interview` branch exists. Name potential future experiment routes, such as `/experiments/table-first`, `/experiments/command-first`, or the project's equivalent, but do not write prototype buildout instructions, `/prototype` routing, or build-plan items from default UX variation output alone. Keep shared production infrastructure out of those future routes unless explicitly approved.
- If route experiments imply materially different products, apps, ICPs, or product lines, update `research/.progress.yaml` with experiment product-path entries instead of making every divergent path a required UX variation. Include `id`, `label`, `source_skill: ux-variations`, `scope_path`, `status`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `pipeline_stage: ux-variations`, and `last_touched`.
   - Product paths are not git branches; keep route-experiment product-path tracking in `research/.progress.yaml` distinct from git workflow branch terminology.
   - After progression variants are specified, route the next selected branch to `/ui-interview [specific-ux-variation]` for visual mockup and approval/rejection. If the user explicitly bypasses that default and asks to build variants before UI interview, record the bypass and rationale in the variation plan and recommend `/uat --variant-evaluation` (check `.agents/project.json.enabled_packs` for `product-testing` — if `product-testing` is not enabled, recommend `npx skillpacks install product-testing` from the project shell, first) before `/consolidate-prototypes`. Consolidation is premature until evaluation evidence exists or the user explicitly says they reviewed the variants and is ready to converge.
   - Define comparison criteria before selecting a winner.
   - Include a lock-in checklist so the chosen direction becomes a decision record, not a vague preference.
   - Include a UAT handoff checklist: target task for each variant, success criteria, side-by-side comparison questions, evidence to capture, tradeoffs to notice, and readiness criteria for `/consolidate-prototypes`.

9. **Coverage checkpoint**
   - Before concluding, summarize the variants, decision criteria, and experiment plan inline as the final message text of its own turn.
   - In the next turn, use AskUserQuestion to ask whether any decision criteria, risks, validation steps, or implementation constraints are missing before writing deliverables.

## Deliverables

Before approval, build `alignment/ux-variations-{topic}.html` from the complete proposed variation plan, proposed interview-log content, proposed branch-routing section, and proposed flow-tree changes. Stop for compiled YAML.

On approval (compiled YAML with no unresolved negative feedback):

- Write the variation plan to `design/ux-variations-[topic].md` in flat mode or `design/{slug}/ux-variations-[topic].md` in product-path mode.
- Write the interview log to `design/ux-variations-[topic]-interview.md` in flat mode or `design/{slug}/ux-variations-[topic]-interview.md` in product-path mode.
- Update the scoped flow-tree manifest with UX variation branch IDs, statuses, artifact references, and the recommended next `/ui-interview [specific-ux-variation]` branch.
- Update `research/.progress.yaml` only when variant or route experiments create materially different product paths; downstream research remains active-path-only until a path is activated. Do not use `research/.progress.yaml` for ordinary UX branch approve/reject/retry state.
- Include a branch-routing section that names the parent user flow, each UX variation branch, sibling flow/variation dependencies, and the recommended next `/ui-interview [specific-ux-variation]` branch.
- Archive the brief and per-variation intermediates under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>` at canonical-write timing.

### Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/ux-variations-{topic}.html`.

## Next Work

**Next work:** after the variation plan is approved, route the chosen variation branch to `/ui-interview [specific-ux-variation]` for visual mockup and UI-experiment growth. In layout-mode, build the variations via `/prototype`, then evaluate with `/uat --variant-evaluation` before `/consolidate-prototypes`.

**Recommended next command:** `/ui-interview [specific-ux-variation]`.

## Invoke With YAML

Emit the `agent_routing` payload with the exact resolved next-invocation command, `{slug}`/`{topic}`/branch filled to literal values: `/ui-interview [specific-ux-variation]` for the selected variation; in layout-mode, `/prototype` then `/uat --variant-evaluation`.

## Constraints

- Do not present superficial variants that differ only by color palette, typography, or decorative treatment.
- Do not treat default UX variation work as only visual layout exploration. Default variations should compare different ways users progress through a named user flow.
- Do not choose a winner for the user unless the evidence clearly supports it and the user asked for a recommendation.
- Do not defer all decisions to testing. State a recommended variant or experiment when evidence is sufficient.
- Do not ignore implementation cost. A compelling variation still needs a validation path and selection criteria, with prototype buildout deferred until UI experiment approval unless layout-mode or an explicit bypass applies.
- Do not route directly from built UI variants to `/consolidate-prototypes`; insert `/uat --variant-evaluation` (check `.agents/project.json.enabled_packs` for `product-testing` — if `product-testing` is not enabled, recommend `npx skillpacks install product-testing` from the project shell, first) unless the user explicitly confirms they have already evaluated the variants.
- Do not skip `/ui-interview` for a UX variation branch that needs a proposed UI, HTML visual mockup, or approval/rejection decision.
- Do not recommend or write `/prototype` buildout, prototype build-plan items, or built route experiments from default progression-mode UX variation output before an approved UI experiment branch exists. Pre-UI buildout is allowed only in `--layout-mode` or when the user explicitly records an ad hoc bypass.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, recommend `npx skillpacks install <pack-name>` from the project shell, before the target skill.
- Do not enforce shared design constraints across variations. Each variation independently decides layout, density, color, navigation, and component choices. Only technical stack (framework, renderer, design system tokens) is shared unless the user explicitly locks a shared constraint.
- Do not write pre-prototype UX variation plans to `specs/`. `design/` is the canonical home for flow maps, UX variation plans, UI branch packets, branch decisions, mockup references, and flow-tree manifests.
- Do not use `tasks/todo.md` for UX/design branch progress or human variant review. Human prototype/UAT evaluation belongs in `tasks/manual-todo.md`; implementation fixes may enter `tasks/todo.md` only after human evidence exists.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/design/spec document (`research/**/*.md`, `design/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.

## Interrogation Page

Before producing research, run the stage-zero interrogation loop following `INTERROGATION-PAGE.md` in this skill's directory. Build one HTML page per round at `interrogation/ux-variations-r{N}-{branch}.html`, starting with the assumptions manifest as round 1, and loop until the confidence gate passes. This skill **cannot advance to stage one** (the framework/scope alignment page) **until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. Each round page must contain at least one genuinely open input (`data-open-input`).

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
