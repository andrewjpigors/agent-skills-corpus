---
name: customer-discovery
description: Orchestrator — detect pre-product vs product-exists mode, bootstrap ICP candidates, recommend customer-discovery frameworks, synthesize outputs into unified ICP research
type: research
version: v1.9
argument-hint: "[optional: \"discovery\" | \"validate\" | \"--synthesize\" | concept/idea, spec file path]"
invocation: orchestrator
context_intake: deep
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. After install, tell Claude users to run `/reload-skills`, then `/clear` or restart if the skill remains invisible. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Customer Discovery — Orchestrator

This is an **orchestrator skill** using the parent router delegation pattern. It detects context, bootstraps ICP candidates, recommends applicable customer-discovery frameworks, and synthesizes their outputs into unified ICP research. Individual frameworks live as child skills under `frameworks/`.

Available frameworks:

| Framework | Slug | Creator | Lens |
|-----------|------|---------|------|
| W3 Hypothesis | `w3-hypothesis` | Schwartzfarb | WHO/WHAT/WHY hypothesis generation + disproval |
| JTBD Needs Analysis | `jtbd-needs` | Ulwick / Christensen | Needs-based segmentation via jobs and outcomes |
| Four Forces | `four-forces` | Moesta | Push/Pull/Anxiety/Habit switching moment analysis |
| Five Rings of Buying Insight | `five-rings` | Revella | Decision psychology and buyer journey |
| Seven Dimensions | `seven-dimensions` | Lincoln Murphy | Ready/Willing/Able/Success/Acquisition/Ascension/Advocacy scoring |
| PMF Engine | `pmf-engine` | Vohra / Supan | Empirical ICP from existing user data (Sean Ellis test + HXC) |

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include downstream or cross-skill command recommendations while a scope, framework findings, or synthesis approval is pending. The approval request itself is the next action. Parent-loop continuation is not downstream routing: after framework completion, hand control back to `/customer-discovery`, never an execution-loop command or a direct `customer-discovery/frameworks/...` invocation. Only emit downstream next-skill routing after the synthesized `icp.md` artifact has been approved and written.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved. As part of confirming, reconcile each displayed gate decision against the final compiled YAML and the written canonical artifact, render any `other`/freeform choice as the read-only decision and drop superseded options, and run the post-confirmation self-check from the alignment-page contract before handoff.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

**How this maps onto the Research Session Loop.** This orchestrator runs as a self-advancing loop (see Execution Model below and `docs/research-session-loop-convention.md`): each approval stop above is a **session boundary** — the agent stops, the user reviews and compiles YAML, then clears context and re-invokes `/customer-discovery` to continue. The multi-select framework page is the single scope-and-candidate approval gate (Stage 1) for the whole selected set; synthesis has its own `review` page. When the loop runs a framework subskill inline (state C), that multi-select approval already satisfies the framework's Stage-1 scope gate, so the framework **enters at its research stage (Stage 2)** and produces exactly one findings `review` page — one approval gate per framework. Standalone (non-loop) invocation of a framework subskill still runs its full two-stage workflow.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Prerequisites

- **Hard**: None — this is the first research skill in the AFPS chain.
- **Soft**: Read these if they exist:
  - `research/idea-brief.md` (or `research/{slug}/idea-brief.md`) — concept, hypotheses, ICP readiness notes
  - Specs, README/CLAUDE, and relevant source files for product context
  - `research/customer-feedback.md` — real customer evidence (triggers product-exists mode)

## Execution Model — Research Session Loop

This is a **self-advancing Pattern A research orchestrator** (see `docs/research-session-loop-convention.md`). Each invocation starts cold, resolves its state from **pasted YAML + filesystem**, runs **exactly one heavy phase**, emits the next gate, and stops. The user advances the loop by clearing context and re-invoking `/customer-discovery`. The user never invokes a framework subskill directly — the orchestrator follows each selected framework's subskill inline.

When a framework is pending, the only user-facing continuation route is re-invoking `/customer-discovery` with the same product/research path argument when present, for example `/customer-discovery research/afps-tracker`. Never tell the user to run a path-shaped child framework command; the parent resolves the pending framework from the run manifest and filesystem.


State lives in two places only:

- **Run manifest** — `research/_working/customer-discovery-run.yaml` (flat) or `research/{slug}/_working/customer-discovery-run.yaml` (product-path). Records the selected framework set and each framework's intermediate path. Written when the multi-select YAML is approved. Shape:

  ```yaml
  orchestrator: customer-discovery
  slug: skills-showcase            # omit in flat mode
  selected_frameworks:
    - slug: w3-hypothesis
      intermediate: research/skills-showcase/customer-discovery-w3-hypothesis.md
    - slug: jtbd-needs
      intermediate: research/skills-showcase/customer-discovery-jtbd-needs.md
  ```

- **Canonical-intermediate existence** — a selected framework is *done* when `research/customer-discovery-{framework}.md` (or `research/{slug}/customer-discovery-{framework}.md`) exists, *pending* otherwise. `pending = selected − existing-intermediates`. The manifest stores selection only, not per-framework status.

`research/.progress.yaml` stays coarse — its `pipeline_stage` is a pointer, not per-framework status.

### State resolution (resolve the first match; YAML first, then most-progressed A→F)

On each invocation, after Product-Path Scope Resolution (step 0), resolve state:

| State | Detected when | Heavy phase this session | Emits / stops with |
|---|---|---|---|
| **0 — pasted YAML** | a compiled alignment YAML is pasted | branch on `approval_status`: `ready-for-agent-review` → apply the approval for the gate it answers (light: write manifest and/or prior framework intermediate, archive consumed source), then fall through to the next pending state below; `not-approved` → amend the named page (refinement session) and stop | amended page, or proceeds ↓ |
| **A — done** | canonical `research/icp.md` (or `research/{slug}/icp.md`) exists | — | done; emit next-skill route (step 9) |
| **B — synthesize** | run manifest exists, all selected intermediates exist, no canonical `icp.md` (also forced by `--synthesize`) | **synthesis** (step 6) | synthesis `review` page |
| **C — run framework** | run manifest exists, ≥1 selected framework pending | **run next pending framework inline at its research stage** (step 5b) | that framework's findings `review` page |
| **E — build selection** | preliminary interview handoff exists, no run manifest, no multi-select page | mode detect → candidate bootstrap → build multi-select page (steps 1–5a) | multi-select `review` page |
| **F — interview** | nothing yet (no handoff, no manifest) | deep interview (Interview Protocol) | preliminary interview handoff, stop |

**Light vs heavy.** Recording the approved selection into the run manifest (state 0→C head), writing an already-reviewed framework intermediate, and archiving a consumed source are *light* — they fold into the head of the next heavy session and do not get their own round-trip. The heavy phase (interview, one framework's research, synthesis) is the only thing isolated per session.

**Shortcuts.** `/customer-discovery discovery` and `/customer-discovery validate` short-circuit states E→C: they write a fixed framework set straight into the run manifest after the user approves the shortcut plan, then enter state C (steps 7–8).

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

0b. **Product-path manifest**: Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection.

### 1. Mode Detection

Runs in **state E** (the build-selection session, after reading the interview handoff). Detect **pre-product mode** (default) or **product-exists mode**:

**Pre-product mode** activates when:
- No production codebase with live users detected, AND
- No `research/customer-feedback.md` with post-launch customer evidence, AND
- `$ARGUMENTS` does not contain "product" or "validate"

Available frameworks in pre-product mode:
- `w3-hypothesis` (default) — Schwartzfarb WHO/WHAT/WHY hypothesis generation + disproval
- `jtbd-needs` (default) — Ulwick/Christensen needs-based segmentation via jobs and outcomes
- `four-forces` (default) — Moesta Push/Pull/Anxiety/Habit switching moment analysis
- `five-rings` (optional) — Revella decision psychology and buyer journey. Pre-check when idea brief indicates B2B model.
- `seven-dimensions` (optional) — Lincoln Murphy ICP scoring with post-sale dimensions
- `pmf-engine` (unavailable) — requires real user data; grayed out with explanation

**Product-exists mode** activates when:
- Production code or deployment exists, OR
- `research/customer-feedback.md` exists with real customer data, OR
- `$ARGUMENTS` contains "product" or "validate"

Available frameworks in product-exists mode:
- `pmf-engine` (default) — Vohra/Supan empirical ICP from existing user data
- `seven-dimensions` (default) — Lincoln Murphy structured scoring with post-sale dimensions
- `four-forces` (optional) — switching analysis grounded in real churn/adoption data
- `five-rings` (optional) — buying insight refresh with real buyer evidence
- `jtbd-needs` (optional) — job validation against actual usage
- `w3-hypothesis` (unavailable) — superseded by empirical data; grayed out with explanation

### 2. Load Context

- Read `$ARGUMENTS`: if file path, read it; if text, treat as concept; if empty, check for idea brief
- Read `research/{slug}/idea-brief.md` or `research/idea-brief.md` — treat as starting hypotheses, not settled truth
- Read CLAUDE.md, README for product context
- Read codebase (if it exists): package config, key source files, routes, data models
- Read existing `research/icp.md` if it exists (prior run — ask user if they want to refine or start fresh)
- Read any existing `research/customer-discovery-*.md` intermediate artifacts (from prior framework runs)

**Provisional product-path evidence.** When a referenced product path is not present in `research/.progress.yaml` (either absent entirely or not in `active_paths` or `product_paths[]`), do not treat it as a canonical active path. Before using it as source context, require an explicit provisional-path evidence reference: a `review-only-approved` alignment page that fully renders the proposed path's concept, brief, and manifest entry. If no such evidence exists, ask the user whether to proceed with the path as unverified context or to run `/idea-scope-brief` first.

### 3. Marketplace Side Preflight

Before identifying ICP candidates, resolve market-structure side coverage:

- Read any `Market Structure Handoff` or marketplace/platform/B2B2C/multi-sided notes from the idea brief, especially `## ICP Readiness`. Treat side names and value exchange as hypotheses from the idea-scope brief, not validated ICPs.
- If no idea brief exists, infer likely sides from `$ARGUMENTS`, README, specs, codebase context, or product description when the concept suggests a marketplace/platform/B2B2C/multi-sided model.
- During broad market research, validate or refute the marketplace/platform/B2B2C/multi-sided classification with evidence; log the evidence for or against each apparent side and value exchange.
- Before candidate generation, write a side-coverage note in the working packet that names material sides, buyer/customer/user distinctions, and any uncertain or unsupported side assumptions.
- Candidate generation must cover each material side or explicitly explain why a side is excluded, deferred, or not a customer side.

### 4. Candidate Bootstrapping

This step runs in **state E** only (and is skipped when `research/icp.md` already exists and user chooses to refine rather than start fresh).

**Broad market research** using WebSearch with **8–12 diverse query strategies**:

1. Direct persona searches — "who buys [category]", "[category] buyer persona"
2. Pain point searches — "[domain] biggest challenges", "[workflow] frustrations"
3. Market segment searches — "[category] market segments", "[category] by company size"
4. Trend searches — "[category] trends 2025 2026", "future of [domain]"
5. Competitor user searches — "[competitor] customers", "[competitor] case studies"
6. Forum/community searches — "[domain] reddit complaints", "[domain] community pain points"
7. Job posting searches — "[related role] job description responsibilities"
8. Industry report searches — "[category] market report", "[category] TAM"
9. Switching trigger searches — "why switch from [incumbent]", "[category] migration"
10. Adjacent market searches — "[related category] users", "[upstream/downstream] tools"
11. Geographic/regulatory searches — "[category] by region", "[domain] regulations by country"
12. Business model searches — "[category] business model", "[product] PLG vs sales-led"
13. WTP signal searches — "[category] pricing complaints", "[category] ROI", "[competitor] pricing reviews"
14. Named account searches (B2B) — "[competitor] customer list", "companies using [incumbent]"

**Classify the business model** into one or more of: B2B SaaS (PLG), B2B SaaS (SLG), B2C, B2C subscription, marketplace/platform, B2B2C, D2C, open-source/open-core, API/developer-first.

**Identify 2–5 ICP candidates.** For each, note:
- Who they are (role, company type, size)
- What pain evidence exists
- How accessible they are
- How much value we could deliver
- How strong the WTP signal is

Write candidates to `research/_working/preliminary-customer-discovery-research.md` (the working packet that subskills will read).

**Checkpoint — Present candidates to the user.** Show ICP candidates with pain evidence, accessibility signals, and value reasoning. Ask:
- "Do any of these surprise you? Is there a segment I'm missing?"
- "Any of these clearly wrong for your situation?"

Incorporate feedback before proceeding to framework selection.

### 5a. State E — Build Framework Multi-Select Page

Build the framework multi-select `review` alignment page with:

1. **Mode explanation**: which mode was detected and why (evidence for detection)
2. **ICP candidates summary**: validated candidates from step 4 (or from existing `research/icp.md`)
3. **Available evidence summary**: what research exists and what's missing
4. **Multi-select framework section**: checkboxes for each available framework with:
   - Framework name, creator, and one-line description
   - Why it's recommended or optional for this context
   - Which ICP sections this framework primarily feeds (see synthesis mapping)
   - Pre-checked defaults based on detected mode (see mode detection above)
5. **Loop explanation**: the selected set is the scope-and-candidate approval gate; each selected framework will then be run inline (one findings page per framework) and the run advances by re-invoking `/customer-discovery`
6. **Approval gate**: framework selection confirmation

This multi-select approval **is** the Stage-1 scope approval for the whole selected set. Stop for compiled YAML. Do **not** write the run manifest or run any framework in this session — that is state C.

### 5b. State C — Run Next Pending Framework (inline)

This session consumes the approved multi-select YAML (state 0→C) or advances after a prior framework's approval. At the **head** of the session, do the light bookkeeping first:

1. **Write/append the run manifest** if it does not yet exist: `research/_working/customer-discovery-run.yaml` (flat) or `research/{slug}/_working/customer-discovery-run.yaml` (product-path), recording `selected_frameworks` with each framework's `slug` and canonical `intermediate` path. Include only frameworks the user selected.
2. **Archive the preliminary interview handoff** at this selection-commit point (move it under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`). A rejected multi-select page must still be able to rebuild from the handoff, so do not archive it earlier.
3. **If a prior framework's reviewed content was just approved** by the pasted YAML, write its canonical intermediate `research/customer-discovery-{fw}.md` (or `research/{slug}/customer-discovery-{fw}.md`) from the already-reviewed working packet, and archive that framework's working packet and superseded review page.

Then run the **one heavy phase** for this session:

4. **Determine the next pending framework** = the first framework in `selected_frameworks` whose canonical intermediate does not yet exist.
5. **Load and follow that framework subskill's `SKILL.md` inline**, entering at its **research stage (Stage 2)**: the multi-select approval already satisfied the framework's Stage-1 scope gate, so perform the framework's research, write its working packet, and build a single findings `review` page for that framework. Stop for that framework's compiled YAML.

**Advance the loop by self-re-invocation.** The confirmed-page handoff and the terminal message name `/customer-discovery` and tell the user to clear context and re-invoke; report progress as "k of N frameworks complete":

```
✔ Framework 1 (W3 Hypothesis) findings ready for review.
Next: review the page and compile YAML, then clear context and run  /customer-discovery
(the next run writes this framework's intermediate and picks up the next pending framework automatically.)
```

Do not emit cross-skill routing here — that happens only after synthesis (step 9).

### 6. State B — Synthesis (auto-detected; also `/customer-discovery --synthesize`)

Enter synthesis when the run manifest exists, **all** selected framework intermediates exist, and no canonical `research/icp.md` yet exists. An explicit `/customer-discovery --synthesize` also forces this state.

Read all intermediate framework outputs:
- `research/customer-discovery-w3-hypothesis.md`
- `research/customer-discovery-jtbd-needs.md`
- `research/customer-discovery-four-forces.md`
- `research/customer-discovery-five-rings.md`
- `research/customer-discovery-seven-dimensions.md`
- `research/customer-discovery-pmf-engine.md`

At least one must exist. If none exist, tell user to run framework selection first.

**Synthesis mapping** — how framework outputs merge into the canonical 9+1 section format:

| Canonical Section | Primary Source | Secondary Sources |
|---|---|---|
| Customer Profile | w3-hypothesis (WHO), pmf-engine (HXC) | seven-dimensions (Ready/Willing/Able) |
| User Profile(s) | w3-hypothesis (WHO detail), pmf-engine (daily users) | jtbd-needs (job performers) |
| Trigger Events | four-forces (Push), five-rings (Priority Initiative) | jtbd-needs (unmet outcomes) |
| Current State Journey | jtbd-needs (current job map) | four-forces (Habit) |
| Pain Map | jtbd-needs (underserved outcomes) | four-forces (Push intensity) |
| Current Alternatives (User Perspective) | four-forces (Habit, current solution language) | five-rings (Decision Criteria) |
| Market Sizing | Aggregated across frameworks | seven-dimensions (Acquisition Efficiency) |
| Stated Value Drivers | w3-hypothesis (WHAT/WHY), jtbd-needs (desired outcomes) | five-rings (Success Factors), pmf-engine (user language) |
| Customer ↔ User Dynamics | seven-dimensions (post-sale dimensions) | five-rings (Buyer's Journey) |
| Discovery & Evaluation Behavior | five-rings (all 5 rings) | four-forces (Active Looking stage) |

**Cross-ICP handling**: Each framework intermediate analyzes all ICP candidates. The synthesis merges per-candidate evidence across frameworks into the canonical sections, selects a primary ICP using seven-dimensions scoring (or value × accessibility matrix when seven-dimensions was not run), and populates "Additional ICPs" and "Cross-ICP Analysis" sections.

**Score & select primary ICP** using a **Value × Accessibility** scoring matrix:

Value score (how much we can help): pain severity/frequency, WTP quality, segment size, alignment with what's built.

Accessibility score (how easy to reach and convert): channel reachability, sales cycle length, DMU complexity, champion availability, budget alignment.

**Cross-ICP analysis**: shared pains, conflicts/trade-offs, product line recommendations, build sequence, discovery & evaluation comparison.

Convert secondary ICPs and product-line recommendations into `research/.progress.yaml` `product_paths[]` entries when they imply a different product surface. Keep primary ICP in `active_paths`. Mark non-selected paths `status: deferred` or `status: revisit_candidate`.

**Evidence matrix**: Each claim in the synthesized output maps back to which framework(s) produced it and at what confidence level.

Build alignment page for synthesis approval with:
- Full proposed `research/icp.md` content
- Evidence matrix combining all framework sources
- Confidence/assumption register
- Cross-ICP analysis with scoring matrix
- Proposed file changes gate
- Approval gate

After approval: write `research/icp.md` and `research/icp-search-log.md`. Then, on this canonical write, **archive the run manifest** (`customer-discovery-run.yaml`) and the synthesis working packet under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, **update `research/.progress.yaml`** `pipeline_stage` to `customer-discovery`, and emit the downstream next-step routing (step 9). This is the one place cross-orchestrator routing is allowed.

### 7. State C via Discovery Shortcut (`/customer-discovery discovery`)

Pre-product shortcut — short-circuits states E→C with a fixed framework set. Build a `review` alignment page for the shortcut plan with:

1. **Shortcut explanation**: discovery sprint selected — three core pre-product frameworks (`w3-hypothesis`, `jtbd-needs`, `four-forces`)
2. **Evidence readiness**: available context and any caveats
3. **Proposed framework set**: the fixed set that will be recorded in the run manifest
4. **Approval gate**: require final compiled YAML approval before writing the run manifest

After user approval via final compiled YAML, write the fixed framework set straight into the run manifest (`research/_working/customer-discovery-run.yaml` or the product-path equivalent), then enter **state C** and run framework 1 inline per step 5b. The loop advances by re-invoking `/customer-discovery`.

### 8. State C via Validation Shortcut (`/customer-discovery validate`)

Product-exists shortcut — short-circuits states E→C with a fixed framework set. Build a `review` alignment page for the shortcut plan with:

1. **Shortcut explanation**: validation sprint selected — empirical ICP from existing users (`pmf-engine`, `seven-dimensions`)
2. **Evidence readiness**: available product/customer evidence and any caveats
3. **Proposed framework set**: the fixed set that will be recorded in the run manifest
4. **Approval gate**: require final compiled YAML approval before writing the run manifest

After user approval via final compiled YAML, write the fixed framework set straight into the run manifest, then enter **state C** and run framework 1 inline per step 5b. The loop advances by re-invoking `/customer-discovery`.

### 9. Next Steps (after synthesis only)

Before writing, check which files exist to populate the `## Next Steps` section contextually. Include 3–5 applicable items with a "Recommended + Other options" framing — the first matching condition becomes the **Recommended** item, remaining items become **Other options**:

- ALWAYS: `/competitive-analysis` — Research competitors and market gaps for this ICP
- IF no `specs/` directory or it's empty: `/competitive-analysis` — Map the competitive landscape for this ICP's market
- IF `specs/` exist but no `research/journey-map.md`: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if not enabled, recommend `npx skillpacks install customer-lifecycle` from the project shell; if enabled, recommend `/journey-map`
- IF codebase exists: check `.agents/project.json.enabled_packs` for `business-ops` — if not enabled, recommend `npx skillpacks install business-ops` from the project shell; if enabled, recommend `/mvp-gap`
- IF `research/competitive-analysis.md` exists: check `.agents/project.json.enabled_packs` for `product-design` — if not enabled, recommend `npx skillpacks install product-design` from the project shell; if enabled, recommend `/brainstorm`

**Impact-aware adjustments:**
- IF downstream impact is **Major**: prepend `/reconcile-research — [N] conflicts found in downstream docs` as the first item
- IF downstream impact is **Minor**: annotate relevant skill suggestions with "(stale — [brief description])"

### 10. Downstream Impact Check

After writing, check for downstream research documents that may be affected. Only check documents that exist on disk.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/competitive-analysis.md`
- `research/journey-map.md`
- `research/metrics.md`
- `research/gtm.md`
- `research/monetization.md`
- `research/enterprise-icp.md`
- `research/customer-feedback.md`

For each existing downstream document:
1. Read it — focus on `> Based on:` header, `## Summary`, and sections that reference concepts this skill just defined or changed
2. Identify specific conflicts: claims, assumptions, or references that contradict what was just decided
3. Note each conflict: downstream file, section, the stale claim (quote it), and what it should now say

**Classify the impact**:
- **None**: No downstream documents exist, or no conflicts found. Skip display entirely.
- **Minor** (1–2 small conflicts): Display conflicts to user inline.
- **Major** (3+ conflicts OR a foundational assumption changed): Display conflicts and strongly recommend `/reconcile-research`.

## Output

### State E output: framework multi-select `review` page + `research/_working/preliminary-customer-discovery-research.md`

Validated ICP candidates in the working packet, plus the multi-select framework page. The run manifest `research/_working/customer-discovery-run.yaml` is written at the head of the first state-C session (when the multi-select YAML is approved), not in state E.

### State C output: per-framework findings `review` page + `research/customer-discovery-{framework}.md`

One findings page per selected framework; the canonical intermediate is written on that framework's approval.

### State B output (synthesis): `research/icp.md` (or `research/{slug}/icp.md`)

```markdown
# ICP: [Primary ICP Name]

> Primary ICP selected from [N] candidates. See Additional ICPs and Cross-ICP Analysis below.
> Search log: research/icp-search-log.md
> Frameworks applied: [list of frameworks used]
> Date: [current date]

## Customer Profile
[Buyer persona, budget authority, discovery channels]

### Geographic Focus
[Include only if the product has regulatory, language, or market-specific constraints.
 Initial target geography/region, why that region first, expansion sequence.]

### Named Accounts
[Include for B2B ICPs. 5–10 real companies that fit this profile.
 For each: company name, approximate size, industry, and why they fit.]

## User Profile(s)
[Daily user persona(s), technical sophistication, goals, frustrations]

## Trigger Events
[What causes them to start looking NOW — ranked by frequency and urgency.
 Job changes, growth milestones, compliance deadlines, tool sunsets, contract renewals, etc.]

## Current State Journey
[Step-by-step workflow without our product]

## Pain Map
[Where the current state breaks down — severity, frequency]

## Current Alternatives (User Perspective)
[What users say they currently use or have tried — tool/process names in user language, not a competitive breakdown]

## Market Sizing
[TAM / SAM / SOM with methodology and confidence level.
 Bottom-up: number of target companies × estimated deal size.
 Top-down: industry reports, competitor revenue signals.]

## Stated Value Drivers
[What customers say matters — their language for the value they need, the "aha moment" as they describe it]

### Willingness-to-Pay Signals
[Evidence only: current paid alternatives, current spend or time-cost proxy, budget owner/context, switching-cost tolerance,
economic urgency, procurement or subscription constraints, and pricing sensitivity cues.
Do not recommend pricing or packaging; route raw signals to monetization.]

## Customer ↔ User Dynamics
[Post-purchase buyer-user relationship: provisioning, onboarding, admin vs end-user dynamics.
 For B2B, the detailed buying process and DMU live in Discovery & Evaluation Behavior below;
 this section focuses on the post-purchase relationship.]

## Discovery & Evaluation Behavior

### How They Find Solutions
[Where this persona searches — communities, review sites, peer recommendations, Google, events]
[Who they ask — colleagues, online communities, consultants, analysts]

### How They Evaluate
[What they compare — features, pricing, reviews, case studies, free trials]
[Decision-making process — solo, team, committee; timeline]

### How They Choose
[What tips the decision — peer recommendation, trial experience, brand trust, integration fit]
[Deal-breakers and must-haves from the user's perspective]

## Additional ICPs

### [ICP 2 Name]
#### Customer Profile
[Include Geographic Focus, Named Accounts, and Business Model & Go-to-Market Motion sub-sections where applicable]
...
#### User Profile(s)
...
#### Trigger Events
...
#### Current State Journey
...
#### Pain Map
...
#### Current Alternatives (User Perspective)
...
#### Market Sizing
...
#### Stated Value Drivers
...
#### Willingness-to-Pay Signals
...
#### Customer ↔ User Dynamics
...
#### Discovery & Evaluation Behavior
[Condensed: how they find, evaluate, and choose solutions — include only sub-sections relevant to this ICP]

### [ICP 3 Name]
...

## Cross-ICP Analysis

### Prioritization Matrix
| ICP | Value Score | Accessibility Score | Combined | Rationale |
|-----|------------|-------------------|----------|-----------|
| ... | | | | |

Scoring rationale must explicitly distinguish pain intensity from WTP quality.

### Shared Pain Points
[Pains that appear across multiple ICPs]

### Conflicts & Trade-offs
[Where serving one ICP would hurt another]

### Product Line Recommendations
[How different ICPs could map to tiers, plans, or product variants]

### Recommended Build Sequence
[Which ICP to target first → second → third, with reasoning]

### Discovery & Evaluation Comparison
[How discovery and evaluation behavior differs across ICPs]

### Evidence Matrix
| Claim | Framework Source(s) | Evidence | Confidence |
|-------|-------------------|----------|------------|
| [claim] | W3 / JTBD / Four Forces / Five Rings / Seven Dimensions / PMF Engine | [source] | Strong / Moderate / Hypothesized |

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

**Recommended:** [first matching item from step 9]

**Other options:**
- [remaining conditional items from step 9 — only include items whose conditions are met]

## Signals for Downstream Research

> Raw signals captured during research. These are unvalidated observations —
> use the linked skill to verify, validate, and explore alternatives.

### → /competitive-analysis
- [signal]: competitor names mentioned by users
- [signal]: tools users compare or say they evaluated
- [signal]: stated alternatives and what users say about them

### → /positioning
- [signal]: value language users use to describe what matters
- [signal]: differentiation claims users respond to
- [signal]: how users describe the problem in their own words

### → /monetization
- [signal]: budget ownership/context and willingness-to-pay evidence
- [signal]: current paid alternatives, spend proxies, or time-cost proxies
- [signal]: switching-cost tolerance and cost-of-inaction language
- [signal]: pricing sensitivity cues from user conversations

### → /gtm
- [signal]: where users say they found or heard about solutions
- [signal]: community or channel mentions during research
- [signal]: peer recommendation patterns observed
```

### `research/icp-search-log.md`

Raw research log containing:
- Every WebSearch query executed and why (from orchestrator bootstrapping and each framework subskill)
- Key findings from each search (with source attribution)
- Evidence that supported or contradicted each ICP candidate
- Marketplace Side Preflight validation/refutation plus side coverage/exclusion rationale
- The scoring rationale for primary ICP selection
- Any data gaps or areas where research was inconclusive

### `research/.progress.yaml`

Product-path manifest created or updated when secondary ICPs, Cross-ICP Analysis, or product-line recommendations create parked or promotable paths.

### Product-Path Output Convention

When multiple active product paths exist or the user asks for cross-path ICP output, write:
- `research/{slug}/icp.md` — full 9-section ICP per product path
- `research/{slug}/icp-search-log.md` — search log per product path
- `research/icp.md` — unified cross-path summary with top-level prioritization

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`.
- One-time condition-gated records go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.

## Constraints

- **Parent self-advances one phase per invocation** and follows the next pending framework's subskill inline (entering at its research stage). It bootstraps candidates, builds the multi-select selection, runs each selected framework inline, and synthesizes. The run manifest records the selected framework set; progress is the existence of canonical intermediates. The loop advances by re-invoking `/customer-discovery` (clear context between sessions).
- **Synthesis requires at least one framework output.** Do not synthesize from zero evidence.
- **Mode detection is evidence-based.** Do not override mode detection without user confirmation.
- **Stay in problem space.** Do not propose features, architecture, UI, or technical solutions. That is `/spec-interview`'s job.
- **Evidence-based.** Every claim in the ICP document must trace back to research evidence. Do not fabricate personas from assumptions.
- **In existing-project mode**, note misalignments between what's built and what the ICP research suggests, but do not prescribe fixes — that's `/mvp-gap`'s job.
- **Primary ICP must use the canonical 9 top-level `##` sections** — downstream skills (`/spec-interview`, `/mvp-gap`, `/roadmap`, `/journey-map`, `/competitive-analysis`) parse these exact headers.
- **Section 10 captures behavioural signals only** — how personas find, evaluate, and choose solutions. Do not include GTM strategy, channel analysis, budget authority, procurement process, or pricing expectations — those belong in downstream skills.
- **WTP is evidence, not pricing strategy.** Capture budget ownership, paid alternatives, current spend/time-cost proxies, switching-cost tolerance, economic urgency, and price sensitivity cues only as segment-fit and urgency evidence. Do not convert WTP evidence into pricing recommendations; route raw signals to `/monetization`.
- **Do not overwrite existing `research/icp.md`** without asking the user first.
- **Minimum research depth for bootstrapping**: at least 8 WebSearch queries before identifying ICP candidates.
- **Present before writing.** Never write output files until findings have been presented to the user and validated.

## Interview Protocol

**Step 1 — Gather context.** Read `.agents/project.json`, README, CLAUDE.md, existing research and specs, git history, and any argument-provided context. Build an internal evidence base before asking questions.

**Step 2 — Assumptions manifest.** Present 3–7 assumptions about the user's situation, goals, and constraints. Tag each with source (`[from prompt]`, `[from repo]`, `[from research]`, `[inferred]`). Ask the user to confirm, correct, or flag before proceeding.

**Step 3 — Focused interview.** Ask 1–3 questions per turn via `AskUserQuestion`. Research and recommend by default — present options with a recommended default. Continue until all areas are covered or the user signals enough.

**Step 4 — Coverage checkpoint and handoff (state F).** Present a summary of everything established and ask the user to confirm completeness. The deep interview is the **state-F heavy phase**: once coverage is confirmed, write the preliminary interview handoff to `research/_working/preliminary-customer-discovery-interview.md` (or `research/{slug}/_working/preliminary-customer-discovery-interview.md`) and **stop** — do not bootstrap candidates or build the multi-select page in this session. The handoff is a complete context transfer for the next cold session (state E), carrying: a provisional mode signal (pre-product vs product-exists, with the evidence seen so far), a context summary, the recommended framework subset with rationale, and all user answers that shape candidate generation and framework selection. The next `/customer-discovery` run reads only this file to perform authoritative mode detection, candidate bootstrap, and build the multi-select page.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/customer-discovery-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
