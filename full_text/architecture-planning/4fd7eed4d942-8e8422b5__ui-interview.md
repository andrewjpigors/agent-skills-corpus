---
name: ui-interview
description: Interview page by page to define a complete UI specification, including layout, hierarchy, controls, links, spacing, sizing, responsive behavior, visual states, and implementation-ready interface details — supports a requirements-only mode that establishes data, actions, and states without locking layout or component decisions
type: planning
version: v0.28
required_conventions: [alignment-page, design-tree-loop, interrogation-page]
argument-hint: "[optional: app, page, flow, feature, or draft UI] [--no-chunk]"
context_intake: deep
visual_tier: prototype
---

# UI Interview

Invoke as `/ui-interview`.

Use this skill when the user needs to turn a UX variation branch, rough product idea, feature, page, wireframe, screenshot, or existing app surface into a detailed implementation-ready UI specification. In the default product-design tree, this skill evaluates one proposed `/ux-variations` branch for one specific user flow, designs a proposed UI, renders an HTML visual mockup for alignment, and then records whether that branch is approved, rejected, or needs another mockup iteration before routing to the next UX variation or user flow.

Use `/user-flow-map` before this skill when the product or feature has no credible screen/route inventory, task sequence, branch coverage, or state map. Prefer `design/user-flow-*.md` and the scoped flow-tree manifest as source material when they exist; they are the upstream wireframe-tree contract. Use `/ux-variations [specific-user-flow]` before this skill when a flow exists but no UX variation branch has been proposed yet.

Use `/ux-variations` after this skill only when the current UI mockup exposes a missing or rejected variation axis that needs branch exploration before another UI proposal.

When invoked with `--requirements-only` (or when the user says "just requirements", "requirements only", or "content requirements"), this skill stops after establishing what the page needs — data, actions, states, and constraints — without committing to any layout, component, or spatial decisions. This is an explicit bounded mode, not the default route from `/user-flow-map`; use it when the user asks for a content contract or when a layout-mode variation run genuinely requires fixed page requirements.

Default branch-review handoff guard: upstream `/user-flow-map` approval and `/ux-variations` output may provide source evidence, but they do not count as `ui-interview` approval. Upstream approval does not count as `ui-interview` interview completion. Requirements-only runs must still present and confirm its own UI Assumptions Manifest, then its own Content Requirements Manifest. `ui-interview` must still investigate cross-flow and cross-variation coordination, design a proposed UI, render the visual mockup in HTML, ask the user for alignment or feedback, and record an explicit approve/reject/retry branch decision.

Follow `DESIGN-TREE-LOOP.md` for prototype-phase routing, state storage, approval boundaries, and task classification. This skill records UI experiment branch decisions in the flow-tree manifest only after its own approval lifecycle permits canonical writes; checkpoint confirmations are not final approval.

## Design-Tree Flow

This skill runs the unified **5-stage design-tree flow** (`interrogation → research → design → plan → implement(scoped)`) from `DESIGN-TREE-LOOP.md`, scoped to the **UI-experiment branches** it grows (`ui_experiments[]` under one UX variation). The `## Process` steps below group by stage:

- **Stage 0 — Interrogation**: the stage-zero loop in `## Interrogation Page` / `INTERROGATION-PAGE.md` plus the UI Assumptions Manifest — confirm scope, the selected UX variation branch, and the prototype-first boundary.
- **Stage 1 — Research**: resolve context and gather references; consult the `design-inspirations` sub-skill for named patterns and conventions when inspiration is thin.
- **Stage 2 — Design**: author the UI experiment packet and (full mode) the HTML visual mockup — `design/ui-[topic].md`, `design/ui-requirements-[topic].md`.
- **Stage 3 — Plan**: the approved UI packet is the build-plan slice; the branch decision (approve/reject/retry) feeds the prototype build ledger.
- **Stage 4 — Implement (scoped)**: write the UI packet, grow `ui_experiment` child branches under the UX variation, and pass the single binding alignment gate before any canonical write.

**Per-branch iteration contract.** Each session cold-starts, reads the flow-tree manifest, resolves the next UX variation in this order: explicit user override, `evaluation_priority`, first-value/activation fit, status, then stable array order. Run the staged flow scoped to that variation, grow the child branches on approval, and stop with the handoff in `## Next Work`.

**Non-buildout boundary.** Default full UI mode stops at UI requirements, branch packet, static or bounded HTML mockup, and branch decision. The branch packet additionally carries a **per-screen batch plan** — the ordered list of flow-step batches (one batch per flow step) that `/build-ui-screens` will walk when it builds the visual screens. Do not write or route default clickable prototype buildout from `ui-interview`. Route approved clickable route experiment needs to /build-ui-screens [approved-ui-experiment] so a dedicated screen builder can build the screens, then `/logic-wiring` wires them clickable.

**Modify-back.** A downstream `modify` decision can re-open an upstream `model_ref` or user-flow branch via `targets[]`; UI experiments below a re-opened node are marked stale and re-authored once that node is re-approved.

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
- Resolve the next UX variation in this order: explicit user override, `evaluation_priority`, first-value/activation fit, status, then stable array order.
- Write UI branch state to `ui_experiments[]`; add one entry under the selected UX variation branch for each proposed UI experiment. Each entry must include `id`, `status`, artifact references, and `decision_id` when a decision is recorded.
- Record approve/reject/retry decisions in the manifest `decisions[]` list. Do not write UX branch state to `research/.progress.yaml`; that file remains product-path/product-line tracking.
- Do not mirror UI experiment review, approve/reject/retry, prototype build, or branch progress into `tasks/todo.md`.

### 0c. Session model — chunked per-page spec sessions vs. one continuous session

This skill already runs **one UX-variation branch per session**; this subsection adds an optional **finer** chunking *within a single large branch*. In full UI mode the heavy phase is the page-by-page specification (step 6), and holding the full spec for every page in one context is the dominant per-session cost on large branches. After the page inventory is known (step 5), decide the session model from the page count: if **N ≥ 4** pages and `--no-chunk` was not passed, enter **chunked mode**; otherwise run straight through in one continuous session exactly as a single pass through steps 0–9. Chunked mode follows the **Intra-Skill Substep Chunking + Shared Context Brief** mechanism in `DESIGN-TREE-LOOP.md`: a setup session (steps 1–5) writes a pure-context brief and stops; one spec session per page (step 6) authors a single page's intermediate; and a final assemble+approve session (steps 7–9 + deliverables + the one alignment page) assembles the canonical UI branch packet behind the single existing alignment gate. The progress cursor is intermediate-file existence — the brief carries no step list, and there is no schema change and no `tasks/todo.md` use. Keep the **HTML visual mockup whole** in the setup session — it is judged as a whole and is never fragmented across pages. Chunking applies to full UI mode only; requirements-only mode (step 5b) stops before the page-spec fan-out and never chunks. For N < 4, when `--no-chunk` is passed, or in requirements-only mode, write no brief and no intermediates and behave exactly as v0.22 did, so small branches stay cheap.

1. **Resolve context**
   - Read `.agents/project.json` if it exists.
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `research/`, route files, component directories, screenshots, and design artifacts when present.
   - Prefer `design/user-flow-*.md` and `design/**/flow-tree-*.yaml` for screen sequence, route inventory, branches, decisions, states, failure paths, and low-fidelity wireframe notes before inferring UI requirements.
   - Prefer `design/ux-variations-*.md` (or product-path-scoped equivalents) for the selected UX variation branch, sibling variations, unresolved branch decisions, proposed progression paths, and branch-routing expectations.
   - Read `design/**/design-inspirations-{topic}.md` if present and treat it as the pre-gathered "apps you admire" / reference-pattern input for mockup and spec work — named UI/UX patterns, conventions, component-library references, and annotated links. When absent, behavior is unchanged.
   - If the request is for an existing UI, inspect the current implementation before interviewing.
   - If multiple apps or surfaces are plausible, ask the user which app, flow, or page to cover first.
   - If the interface has no credible screen/flow structure from a user-flow spec, existing routes, screenshot, wireframe, or explicit user prompt, stop and recommend `/user-flow-map [topic]` before UI requirements or layout decisions.
   - If the interface has a credible flow but no specific UX variation branch or proposal to judge, stop and recommend `/ux-variations [specific-user-flow]`.

2. **Treat inputs as draft material**
   - Do not assume the current UI, prompt, screenshot, or mockup is final.
   - Product specs, ICP documents, and journey maps are reference material, not locked constraints. The user may override any product decision during the interview. When a user's interview answer contradicts an existing spec, adopt the interview answer and note the divergence.
   - Preserve explicit constraints, but challenge unclear defaults before they become implementation decisions.
   - Distinguish product behavior decisions from UI presentation decisions.

3. **Surface assumptions before probing**
   - Present a UI Assumptions Manifest before deep questioning.
   - Tag each assumption with `[from spec]`, `[from codebase]`, `[from research]`, `[from artifact]`, or `[inferred]`.
   - Cover product and user context, parent user flow, selected UX variation branch, other user flows touched by this branch, sibling UX variations or existing UI proposals this branch must coordinate with, pages and routes, primary tasks, navigation, hierarchy, layout grid, spatial density, component inventory, button and link semantics, form behavior, empty/loading/error/success states, responsive behavior, accessibility, visual language, implementation constraints, and the prototype-first boundary for new product or substantial feature work: what the user should be able to click through first, whether multiple route-based experiments should be built, what data can be fake, fixture-backed, or in-memory, and which infrastructure must be represented visually but not implemented yet.
   - Use AskUserQuestion to ask the user to confirm, correct, or flag assumptions before continuing.
   - Deliver every manifest/checklist/checkpoint the user must confirm inline as the final message text of its own turn; ask the confirmation question in the next turn. AskUserQuestion option previews may mirror the content as a supplement but are never the sole channel. Never emit it only as mid-turn text in a turn that ends with a tool call — harness rendering does not guarantee mid-turn text is shown. A confirmation question must never reference content the user has not been shown.

4. **Branch review loop**
   - In default mode, run this four-step loop for the selected UX variation branch:
     1. Investigate the specific UX variation proposed for a specific user flow. Determine which other user flows it touches, which sibling UX variations it competes with or depends on, and which existing UI proposals, specs, prototypes, or implementation surfaces it must coordinate with.
     2. Design a proposed UI for that branch and display a visual mockup in HTML. The mockup may be static or lightly interactive, but it must be concrete enough for the user to judge layout, hierarchy, controls, copy, state treatment, and branch viability.
     3. Interview the user for alignment over the UI for this UX variation experiment. If the visual mockup is off-base, collect focused feedback, revise the proposal/mockup, and ask again instead of treating the first mockup as final.
     4. Record whether this branch of the user flow is approved, rejected, or needs another iteration, then route to the next unresolved UX variation or user flow as needed.
   - The branch decision is separate from implementation approval. Approval means the UI direction is a valid branch of the wireframe tree; implementation sequencing remains blocked until prototype build-plan synthesis, prototype evaluation, consolidation, and post-prototype specification work are complete.

5. **Interview page by page**
   - Ask 1 to 3 focused questions per turn using AskUserQuestion.
   - Move through the interface in this order unless the user asks otherwise:
     - Global shell: header, sidebar, footer, navigation, account controls, notifications
     - Page inventory: every route, modal, drawer, overlay, and important empty state
     - Page purpose: user goal, task priority, and success condition
     - Prototype calibration: first clickable journey, route-based experiment set, fixture/fake data boundaries, infrastructure-only states to mock rather than implement, and taste/feel questions the prototype must answer before database, auth, payment, analytics, deployment, admin, or multi-tenant work is planned.
   - **Chunked-mode setup handoff**: When chunked mode is active (step 0c — full UI mode, N ≥ 4 pages, no `--no-chunk`), the page inventory established here is the end of the setup session. Keep the HTML visual mockup whole in this session (step 4). Write the shared context brief to `design/{slug}/_working/ui-interview-{topic}-brief.md` (flat mode: `design/_working/ui-interview-{topic}-brief.md`) containing **pure context only** — the confirmed UI Assumptions Manifest, scope boundaries, the page inventory as context, the global-shell/navigation decisions every page shares, the HTML visual mockup reference, the evaluation criteria, and any carried branch decisions — with **no step list and no status field**. Then STOP and emit the **Terminal handoff format** from `DESIGN-TREE-LOOP.md`: state the brief was written, name the **first** page to spec in **plain English** (what that page is, never only the internal `{page-id}`), and give the **exact** resolved next command with `{slug}`/`{topic}` filled in, e.g. `/ui-interview alignment-page-review` writing into `design/alignmeant/ui-interview-alignment-page-review/{page-id}.md`, so each page gets its own cold spec session (step 6). In non-chunked mode, continue directly to step 6 in this same session.

5b. **Requirements gate (requirements-only mode)**
   - In requirements-only mode, stop here — do not proceed to layout anatomy, component inventory, or spatial decisions.
   - Requirements-only mode has two required confirmation gates before any alignment page build: the UI Assumptions Manifest from step 3, then the Content Requirements Manifest in this step. Upstream approval, including approved `/user-flow-map` YAML or an approved flow alignment page, may populate assumptions and source evidence but cannot replace either confirmation; `ui-interview` must still present and confirm its own UI Assumptions Manifest, then its own Content Requirements Manifest.
   - Evidence-synthesis exception: only skip live confirmation questions when the current visible user invocation explicitly asks to skip live interview questions, synthesize from existing evidence only, or avoid asking the user. In that case, label the output as an `evidence-synthesis review`, set Interview provenance to `evidence-synthesis-with-explicit-skip`, do not call it a completed interview, and route unresolved decisions to a resumed `/ui-interview` instead of implying interview completion.
   - For each page, confirm:
     - Data fields and entities (with cardinality: one, many, nested, polymorphic)
     - User actions (create, edit, delete, filter, sort, export, navigate, bulk-select, reorder)
     - States (empty, loading, error, partial, full, offline, permission-denied)
     - Constraints (real-time updates, offline support, accessibility requirements, performance budgets)
     - Content hierarchy (primary / secondary / tertiary information)
     - Relationships between data elements (parent-child, peer, reference, aggregate)
   - Present a **Content Requirements Manifest** summarizing all pages, then use AskUserQuestion to confirm. Deliver the manifest per the inline visibility rule in step 3 (turn-final message text of its own turn; confirmation question in the next turn; option previews only as a supplementary mirror), never as mid-turn text only.
   - This manifest confirmation is non-final: it only confirms the requirements draft is ready for the pre-approval lifecycle in step 9. Route all writes through that lifecycle — working packet at `research/_working/preliminary-ui-interview-research.md` (or `research/{slug}/_working/preliminary-ui-interview-research.md`), then a `review`-state `alignment/ui-interview-{topic}.html` page rendering the Content Requirements Manifest as the candidate/verdict gate, then final compiled YAML approval.
   - Only after final compiled YAML approval, write `design/ui-requirements-[topic].md` (content requirements) and `design/ui-requirements-[topic]-interview.md` (interview log) in flat mode or product-path-scoped equivalents, update the scoped flow-tree manifest, archive the working packet, and convert the page to `confirmed` per step 9.
   - Only after the page is converted to `confirmed` and canonical files are written, recommend `/ux-variations --layout-mode` to explore multiple visual approaches for these requirements, or `/ui-interview` (full mode, no flag) to proceed directly to a single deep UI specification.
   - If requirements-only work exposes missing screen order, branch decisions, or state coverage, recommend `/user-flow-map [topic]` instead of inventing layout variants.
   - Stop. Do not continue to step 6 or beyond; the pre-approval lifecycle in step 9 and the requirements deliverables above are the only remaining work in this mode.

6. **Full UI specification** (no `--content-only` flag):

   - **Chunked-mode spec session (one page per session)**: When chunked mode is active, each spec session reads the brief at `design/{slug}/_working/ui-interview-{topic}-brief.md` and scans which `{page-id}.md` files already exist under `design/{slug}/ui-interview-{topic}/`. Pick the first page whose intermediate file does **not** yet exist, write its full spec (the attribute list below — layout anatomy, component inventory, control inventory, copy, states, spatial details, responsive behavior, accessibility) to `design/{slug}/ui-interview-{topic}/{page-id}.md`, append any cross-page facts worth carrying to the brief, then STOP and emit the **Terminal handoff format** from `DESIGN-TREE-LOOP.md`: state the intermediate just written, name the next missing page in **plain English** (what that page is, never only the internal `{page-id}`), and give the **exact** resolved next command, e.g. `/ui-interview alignment-page-review`. When the page just written was the last one, the handoff points to the assemble+approve session instead of another spec session. Continue-vs-stop framing follows that convention's Routing Rules. Context per session is the brief plus one page. In non-chunked mode, specify all pages in this same session as before. The per-page spec content below is identical in both modes — chunking changes only how many pages one session writes.
   - Layout anatomy: top-to-bottom and left-to-right regions, alignment, density, scroll behavior
     - Component inventory: tables, lists, cards, forms, charts, media, editors, maps, canvases
     - Controls: every button, icon button, segmented control, checkbox, radio, toggle, input, menu, tab, link, and destructive action
     - Copy: headings, labels, helper text, validation text, confirmation text, empty-state text
     - States: default, hover, focus, active, selected, disabled, loading, error, success, partial, offline
     - Spatial details: element prominence, approximate sizes, gaps, padding, fixed or fluid dimensions, sticky regions, overlap rules, max widths
     - Responsive behavior: desktop, tablet, mobile, wide desktop, touch target sizing, collapsed controls
     - Accessibility: keyboard order, focus traps, labels, contrast, reduced motion, screen reader names. Include color-blind safe patterns, keyboard navigation, reduced motion support, and screen reader labels by default in every spec. Do not present accessibility features as optional checkboxes. Only ask about domain-specific accessibility (gamepad support, dyslexia fonts) when the product context warrants it.
   - When a page includes repeated items, define one canonical item and its variations rather than asking about every row individually.

7. **Research and recommend by default**
   - Use project evidence and established UI conventions before asking the user to invent details.
   - For material decisions, present options, a recommendation, rationale, tradeoffs, and mitigation.
   - Recommend familiar controls over novel patterns unless the product has a strong reason to deviate.
   - Respect the existing design system, component library, and implementation patterns.
   - Reference and inspiration questions ("apps you admire?") are low-priority. Ask once early, accept any answer including "none" or "let's experiment," and move on. Do not block the interview on reference input. When a `design/**/design-inspirations-{topic}.md` artifact exists (from `/design-inspirations`), it supplies that pre-gathered inspiration input, so you need not ask the reference question; still favor local project evidence and established conventions over external references.

8. **Coverage checkpoint**
   - Before concluding, use AskUserQuestion to present a concise checklist of pages, components, controls, states, responsive behavior, and unresolved risks.
   - Deliver the checklist per the inline visibility rule in step 3 (turn-final message text of its own turn; confirmation question in the next turn; option previews only as a supplementary mirror), never as mid-turn text only.
   - Ask whether anything is missing or should be revisited before building the alignment page.
   - This confirmation is non-final: it only establishes that the draft is ready for the pre-approval lifecycle in step 9. It does not authorize canonical spec writes.

9. **Build pre-approval alignment page**
   - **Chunked-mode assemble+approve session**: When chunked mode is active, begin this session only once every page's `{page-id}.md` intermediate exists under `design/{slug}/ui-interview-{topic}/`. Assemble those per-page intermediates plus the brief into the single working packet below, then run step 7 (research/recommend) and step 8 (coverage checkpoint) over the whole assembled branch spec and build the **one** alignment page. On final compiled YAML approval, write the canonical UI branch packet, flip the scoped flow-tree `ui_experiments[]` decision, and archive the brief and the per-page intermediates per the convention's archive-at-canonical-write timing. There is exactly one alignment gate for the whole branch, not one per page (the existing one-gate-per-branch behavior is unchanged).
   - Before writing any canonical `design/ui-[topic].md`, `design/ui-requirements-[topic].md`, or interview log, write the full draft (spec or requirements content plus interview record) only to the working packet `research/_working/preliminary-ui-interview-research.md` (or `research/{slug}/_working/preliminary-ui-interview-research.md` when a product path is active).
   - Build `alignment/ui-interview-{topic}.html` as a `review`-state page rendering the complete working-packet substance as structured HTML review UI: the manifest, branch investigation, HTML visual mockup, page-by-page decisions, coverage checkpoint, proposed canonical file destinations, and approval/rejection gates.
   - Include **Interview provenance** in the page and working packet with exactly one of these values: `live-ui-interview` when this run completed the required manifest confirmations with the user; `evidence-synthesis-with-explicit-skip` when the current invocation explicitly asked to skip live questions or synthesize from evidence; `invalid-missing-ui-interview` when neither condition is true. `invalid-missing-ui-interview` pages must route unresolved decisions to a resumed `/ui-interview` and must not imply interview completion or readiness for canonical writes.
   - At the top of the page, include a plain-language **Interview stage** explainer naming the invocation, whether the run is requirements-only, full UI mode, or branch-review mode, what user/agent interview work has already happened or was inferred from approved upstream evidence, and what the reviewer should do next. If requirements were synthesized primarily from approved specs or code evidence rather than live Q&A, say so directly and route missing answers through section feedback or a resumed interview instead of implying the interview is complete.
   - Render the working packet as structured HTML, not as a raw Markdown preview: headings become sections, lists stay readable lists, and every Markdown table becomes an HTML `<table>` inside a `.table-wrap` container with a concise `data-tts-narrative`. A raw Markdown `<pre><code>` dump may appear only as a supplemental source view after the rendered packet, never as the primary review surface.
   - Attempt to open the page in the browser and point the user at the repo-relative path.
   - Treat every AskUserQuestion checkpoint confirmation in steps 3–8 as non-final; each only confirms the draft is ready for review. Only final compiled YAML from the alignment page authorizes canonical writes.
   - When feedback-only YAML is provided, revise the working packet and the alignment page, then ask again; the work stays pre-approval.
   - Before final compiled YAML approval, the next action is review or revision of the HTML alignment page. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after final compiled YAML approval has been provided and the approved canonical files have been written.

## Deliverables

Before writing anything in this section, verify the alignment page has final compiled YAML approval. Do not write canonical UI specs or interview logs until `alignment/ui-interview-{topic}.html` has been reviewed and the user has provided final compiled YAML approval; checkpoint confirmations are not final approval and do not authorize these writes.

- Write the completed UI branch packet to `design/ui-[topic].md` in flat mode or `design/{slug}/ui-[topic].md` in product-path mode.
- Write the interview log to `design/ui-[topic]-interview.md` in flat mode or `design/{slug}/ui-[topic]-interview.md` in product-path mode.
- Update the scoped flow-tree manifest with the UI experiment status, artifact references, and approve/reject/retry decision record.

After the canonical files are written, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, and convert the alignment page from `review` to `confirmed`.

The UI specification must include source evidence, the confirmed UI Assumptions Manifest, parent user flow, selected UX variation branch, touched sibling flows, coordination dependencies, HTML visual mockup path or embedded review section for the proposed UI, branch decision record (approved, rejected, or retry needed) with next branch/user-flow route, page inventory, route map, global shell rules, page-by-page anatomy, component inventory, control inventory, link inventory, layout and responsive rules, visual style direction, interaction states, accessibility requirements, implementation notes, open questions, risks, and non-goals. For new product interfaces or substantial feature interfaces, include a prototype-first section naming the first clickable journey, experiment route map when multiple alternatives should be tested, fake/fixture data, visually mocked infrastructure states, deferred production infrastructure, and the evidence required before implementation planning promotes any deferred infrastructure.

The interview log must include the manifest, branch investigation notes and cross-flow/variation coordination findings, visual mockup feedback, retry notes, final branch decision, every question asked, options and recommendations presented, user responses, final decisions, and notable changes from the initial draft, current implementation, or artifact.

Only after the page is converted to `confirmed` and canonical files are written, route based on the branch decision: recommend `/build-ui-screens [approved-ui-experiment]` when an approved branch needs a clickable route experiment, `/ui-interview [next-specific-ux-variation]` for the next UX variation branch, `/ux-variations [next-specific-user-flow]` when the next user flow still needs progression variants, or `/user-flow-map --prototype-build-plan [topic]` when all target user-flow and UI branch decisions are complete enough to synthesize the prototype build ledger. Do not route from `ui-interview` directly to `/prototype`, `/roadmap`, `agent-work-admin`, implementation planning, or production sequencing during the research/prototype phase.

### Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/ui-interview-{topic}.html`.

The page is built pre-approval in `review` state per step 9, before any canonical spec write, and converts to `confirmed` only after final compiled YAML approval and canonical writes.

## Next Work

**Next work:** route based on the branch decision recorded in the prototype build ledger. When an approved UI branch needs a clickable route experiment, hand it to `/build-ui-screens [approved-ui-experiment]`; when the variation's UI experiments are all approved and evaluated, synthesize the build plan with `/user-flow-map --prototype-build-plan [topic]`; when more UX variations remain to explore, route back to `/ux-variations [specific-user-flow]`.

**Recommended next command:** `/build-ui-screens [approved-ui-experiment]`.

## Invoke With YAML

Emit the `agent_routing` payload with the exact resolved next-invocation command, `{slug}`/`{topic}`/branch filled to literal values: `/build-ui-screens [approved-ui-experiment]` when an approved UI branch needs a clickable route experiment, `/user-flow-map --prototype-build-plan [topic]` once the variation's UI experiments are decided and evaluated, or `/ux-variations [specific-user-flow]` for the next unexplored flow.

## Constraints

- Do not skip small interface elements. Buttons, links, icons, menus, and empty states are part of the spec.
- Do not collapse UI detail into generic phrases such as "standard dashboard layout" or "normal form behavior."
- Do not create implementation plans until the page anatomy and control behavior are decision-complete.
- Do not treat visual polish as separate from implementation. Size, spacing, hierarchy, and responsive behavior must be specified well enough for a developer to build.
- Do not treat upstream `ux-variations` output as UI approval. The branch still needs an HTML visual mockup and explicit approve/reject/retry decision.
- Do not route to broad implementation planning while unresolved UX variation branches or touched user flows still need review.
- Do not write pre-prototype UI branch packets to `specs/`. `design/` is the canonical home for flow maps, UX variation plans, UI branch packets, branch decisions, mockup references, and flow-tree manifests.
- Do not use `tasks/todo.md` for UI/design branch progress. Human prototype/UAT evaluation belongs in `tasks/manual-todo.md`; implementation fixes may enter `tasks/todo.md` only after human evidence exists.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, recommend `npx skillpacks install <pack-name>` from the project shell, before the target skill.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/design/spec document (`research/**/*.md`, `design/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.

## Interrogation Page

Before producing research, run the stage-zero interrogation loop following `INTERROGATION-PAGE.md` in this skill's directory. Build one HTML page per round at `interrogation/ui-interview-r{N}-{branch}.html`, starting with the assumptions manifest as round 1, and loop until the confidence gate passes. This skill **cannot advance to stage one until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. Each round page must contain at least one genuinely open input (`data-open-input`).

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
