---
name: icp
description: Research-driven ICP discovery — web search + codebase analysis to identify multiple ICPs, pain points, value props, and cross-ICP prioritization
type: research
version: v0.8
argument-hint: <spec file path, concept/idea, or empty to use idea brief>
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `/pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# ICP — Research-Driven Customer Discovery

## Report-First Approval Gate

Default to report-only: present findings, evidence coverage, assumptions, recommended artifact path, and proposed file changes in a pre-approval alignment page plus a concise conversation summary for user approval before creating or updating canonical research, spec, or task files.

Do not write or overwrite synthesized deliverables until the user explicitly approves, unless the user invoked an explicit write/update/fix mode or clearly asked to write files upfront. Raw evidence capture may be persisted before analysis when reproducibility requires it; report those raw paths separately and still gate synthesized research/report writes.

When stopping for approval, build and attempt to open the alignment preview page first, then ask the user to review it and approve, question, or request adjustments. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

Automated research that identifies **multiple ICP candidates**, maps their pain points and value props, scores them, and selects a primary ICP. Replaces interview-driven approaches with web search + codebase analysis. Input is a spec file path, concept/idea as `$ARGUMENTS`, or `research/idea-brief.md` / `research/{slug}/idea-brief.md` when present.

The output preserves the canonical 9-section format at the top level (for downstream compatibility with `/spec-interview`, `/mvp-gap`, `/roadmap`, `/journey-map`) while adding multi-ICP analysis, cross-ICP prioritization, and a supplementary section 10 (`## Discovery & Evaluation Behavior`) that captures how personas find, evaluate, and choose solutions.

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

### 1. Parse Input & Gather Context

**Read `$ARGUMENTS`:**
- If it's a file path, read the file for product/concept context
- If it's text, treat it as the concept or idea description
- If empty, check for `research/{slug}/idea-brief.md` in product-path scope or `research/idea-brief.md` in flat scope first; then check `specs/spec.md`, `specs/plan.md`, or README for context — if nothing exists, ask the user what product or idea to research

**Read product-path manifest if present:**
Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Use `active_paths` to identify current product/app/ICP focuses and `product_paths[]` to preserve secondary product paths without treating them as git branches or parallel implementation lanes.

**Read idea brief if present:**
Read `research/{slug}/idea-brief.md` in product-path scope, or `research/idea-brief.md` in flat scope, whenever it exists. Treat it as starting context and source hypotheses, not as settled truth. Use its problem hypothesis, beneficiary hypothesis, value wedge, constraints, non-goals, and ICP readiness notes to frame search queries and candidate generation. If `$ARGUMENTS` conflicts with the idea brief, flag the mismatch at the first checkpoint and ask which premise should guide ICP research.

**Read codebase (if it exists):**
Read CLAUDE.md, README, package config, key source files, routes, and data models to understand what's been built. This grounds the research in reality rather than pure market abstraction.

**Read existing research** (`research/icp.md`, `research/competitive-analysis.md`, etc.) and specs if they exist — use as background context but do not treat as settled. This research may reshape direction.

**Use code/app hints secondarily:**
Check for monorepo indicators (`turbo.json`, `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, or `package.json` workspaces), app folders, or package folders only after product-path resolution. If multiple active product paths exist, or if this run is explicitly producing a cross-path overview, run the full ICP process separately for each product path — produce `research/{slug}/icp.md` per path, plus a unified `research/icp.md` that cross-references all product-path ICPs with top-level prioritization. If code clearly exposes a user-facing app without a matching product path, suggest creating `research/{slug}/` instead of treating monorepo detection as a gate.

**Migrate flat files when product paths are introduced:** If canonical flat `research/*.md` files exist and the user chooses or creates a product path, offer to move path-specific canonical docs into `research/{chosen-slug}/`. Leave or regenerate top-level files only when they are cross-path summaries.

**Migrate old convention:** If `research/icp-{slug}.md` files exist (old naming), offer to move them to `research/{slug}/icp.md` (and corresponding search logs to `research/{slug}/icp-search-log.md`). Create the subdirectories as needed.

### 2. Broad Market Research

Use WebSearch with **8–12 diverse query strategies** to cast a wide net. Log every search query and key findings to the research log.

Query strategies (adapt to the specific domain):
1. **Direct persona searches** — "who buys [category]", "[category] buyer persona"
2. **Pain point searches** — "[domain] biggest challenges", "[workflow] frustrations"
3. **Market segment searches** — "[category] market segments", "[category] by company size"
4. **Trend searches** — "[category] trends 2025 2026", "future of [domain]"
5. **Competitor user searches** — "[competitor] customers", "[competitor] case studies", "[competitor] reviews"
6. **Forum/community searches** — "[domain] reddit complaints", "[domain] community pain points"
7. **Job posting searches** — "[related role] job description responsibilities" (reveals workflows)
8. **Industry report searches** — "[category] market report", "[category] TAM"
9. **Switching trigger searches** — "why switch from [incumbent]", "[category] migration"
10. **Adjacent market searches** — "[related category] users", "[upstream/downstream] tools"
11. **Geographic/regulatory searches** (if the domain has regional constraints) — "[category] by region", "[domain] regulations by country", "[category] adoption [region]"
12. **Named account searches** (B2B) — "[competitor] customer list", "companies using [incumbent]", "[industry] companies that [trigger event]", "[category] case studies"
13. **Business model searches** — "[category] business model", "[product] PLG vs sales-led", "[category] B2B vs B2C", "[category] marketplace", "[category] go-to-market motion"
14. **Willingness-to-pay signal searches** — "[category] pricing complaints", "[category] budget", "[category] ROI", "[category] cost of manual process", "[competitor] pricing reviews", "[category] switching cost"

Use WebFetch to pull in particularly relevant pages for deeper analysis when search snippets aren't enough.

**Classify the business model** into one or more of: B2B SaaS (PLG), B2B SaaS (SLG), B2C, B2C subscription, marketplace/platform, B2B2C, D2C, open-source/open-core, API/developer-first. Document the classification with evidence in the search log. This classification gates which sub-sections appear in the `## Discovery & Evaluation Behavior`.

### 3. Identify ICP Candidates — Present & Validate

From the research evidence, cluster findings into **2–5 distinct ICP candidates**. For each candidate, note:
- Who they are (role, company type, size)
- What pain evidence exists
- How accessible they are (can we reach them?)
- How much value we could deliver
- How strong the WTP signal is: paid alternatives, budget owner/context, current spend or time-cost proxy, switching-cost tolerance, economic urgency, and pricing sensitivity cues

**Checkpoint 1 — Present candidates to the user.** Use the AskUserQuestion tool to show the ICP candidates with a brief rationale for each — cite the pain evidence found, accessibility signals, and value delivery reasoning from your search findings for each candidate. Then ask:
- "Do any of these surprise you? Is there a segment I'm missing?"
- "Any of these clearly wrong for your situation?"

Incorporate feedback before proceeding.

### 4. Deep Research Per ICP

For each validated ICP candidate, run **targeted searches** to fill the 9-section framework:

- **Customer Profile** — buyer persona, budget authority, discovery channels. Include conditional sub-sections:
  - **Geographic Focus** (include only if the product has regulatory, language, compliance, or market-specific constraints) — initial target geography/region, why that region first, and expansion sequence. Search for "[category] by region", "[domain] regulations by country".
  - **Named Accounts** (include for B2B ICPs) — 5–10 real companies that fit this ICP. For each, note company name, approximate size, industry, and why they fit (e.g., uses the incumbent, recently hit a trigger event, posted a relevant job listing). Search for "[competitor] customer list", "companies using [incumbent]", "[industry] companies that [trigger event]".
  - **Business Model & Go-to-Market Motion** — model type (B2B/B2C/marketplace/B2B2C/D2C/hybrid) with evidence; primary motion (PLG, sales-led, community-led, partner-led, or hybrid); buyer-user relationship (same person, different people, or multi-sided).
- **User Profile(s)** — daily users, technical sophistication, goals, frustrations
- **Trigger Events** — what causes someone to start looking NOW? Job changes, growth milestones, compliance deadlines, tool sunsets, contract renewals, team scaling pain, funding events, new regulations. Search for "[category] buying triggers", "why companies switch [category]", "[incumbent] churn reasons". Rank by frequency and urgency.
- **Current State Journey** — step-by-step workflow without our product
- **Pain Map** — where the current state breaks down, severity, frequency
- **Current Alternatives (User Perspective)** — what users say they currently use or have tried, in their own words. Capture tool/process names without analysing competitors
- **Market Sizing** — TAM (total addressable market), SAM (serviceable), SOM (obtainable). Search for "[category] market size", "[category] TAM", "[category] number of companies". Use company counts, average deal size signals, and segment data to build bottom-up estimates. Flag confidence level (strong data vs. rough extrapolation).
- **Stated Value Drivers** — what customers say matters to them in their own language; the "aha moment" as users describe it, not strategic positioning. Include **Willingness-to-Pay Signals** as a bounded evidence subsection: paid alternatives, budget owner/context, current spend or time-cost proxy, switching-cost tolerance, economic urgency, and pricing sensitivity cues. Do not recommend prices, packages, or monetization strategy here.
- **Customer ↔ User Dynamics** — post-purchase buyer-user relationship: provisioning, onboarding, admin vs end-user dynamics. For B2B, the detailed buying process and decision-making unit live in `## Discovery & Evaluation Behavior`; this section focuses on the post-purchase relationship.
- **Discovery & Evaluation Behavior** — how this persona found, evaluated, and chose solutions. Capture behavioural signals only (where they searched, who they asked, what they compared) — not channel strategy or GTM analysis. Use findings to populate section 10.

### 5. Score & Select Primary ICP — Present & Validate

Build a **Value x Accessibility** scoring matrix:

**Value score** (how much we can help):
- Pain severity and frequency
- Willingness to pay quality: active spend on alternatives, clear budget owner/context, high cost of inaction, tolerance for switching costs, urgency tied to measurable economic outcomes
- Size of the segment
- Alignment with what we've built (if codebase exists)

**Accessibility score** (how easy to reach and convert):
- Can we reach them through available channels?
- How long is the sales cycle?
- How complex is the buying process?
- Is there an existing community we can tap?
- Sales cycle length (shorter = higher score)
- DMU complexity (how many people must say yes)
- Champion availability (obvious internal advocate?)
- Budget alignment (budget cycle favors near-term purchase?)

**Checkpoint 2 — Present the scoring matrix and primary ICP selection to the user.** Use the AskUserQuestion tool to show the full matrix with scores and rationale, then ask:
- "Does this ranking match your intuition? Any factors I'm not weighing correctly?"
- If scores are close between candidates, ask which trade-offs the user prefers

Incorporate feedback before proceeding.

### 6. Cross-ICP Analysis — Present & Validate

Analyze across all ICP candidates:
- **Shared pains** — what pain points appear across multiple ICPs?
- **Conflicts** — where would serving one ICP hurt another?
- **Product line recommendations** — could different ICPs be served by different tiers/plans?
- **Build sequence** — which ICP to target first, second, third and why?
- **Lowest-hanging fruit x most value** — the prioritization sweet spot
- **Discovery & evaluation comparison** — how discovery and evaluation behavior differs across ICPs; do different ICPs find and choose solutions through different paths?

Convert secondary ICPs, product-line recommendations, and materially different Cross-ICP Analysis outcomes into `research/.progress.yaml` `product_paths[]` entries when they imply a different product surface, product-path scope, audience-first path, or future pivot. Manifest entries must include `id`, `label`, `source_skill: icp`, `scope_path`, `status`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `last_touched`, and `pipeline_stage: icp`.

Keep the selected primary ICP in `active_paths` by default. Recommend `/product-line activate` when secondary ICPs suggest a materially different product surface worth exploring again. Mark non-selected ICP/product paths `status: deferred` or `status: revisit_candidate`; do not run full competitive analysis, positioning, journey mapping, UX, or specs for every deferred path unless the user activates one.

**Checkpoint 3 — Present the cross-ICP analysis and recommended build sequence to the user.** Use the AskUserQuestion tool to show the analysis with evidence: shared pains with source data from each ICP, conflicts with specific examples, and build sequence rationale grounded in the scoring matrix. Then ask:
- "Does this sequencing make sense for where you are right now?"
- If conflicts exist between ICPs, ask the user to weigh in on the trade-offs

Incorporate feedback before proceeding.

### 7. Populate Next Steps

Before writing, check which files exist to populate the `## Next Steps` section contextually. Include 3–5 applicable items with a "Recommended + Other options" framing — the first matching condition becomes the **Recommended** item, remaining items become **Other options**:

- ALWAYS: `/competitive-analysis` — Research competitors and market gaps for this ICP
- IF no `specs/` directory or it's empty: `/competitive-analysis` — Map the competitive landscape for this ICP's market
- IF `specs/` exist but no `research/journey-map.md`: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if `customer-lifecycle` is not enabled, recommend `/pack install customer-lifecycle` first; if `customer-lifecycle` is enabled, recommend `/journey-map` — Map how this ICP flows through the product
- IF codebase exists: check `.agents/project.json.enabled_packs` for `business-ops` — if `business-ops` is not enabled, recommend `/pack install business-ops` first; if `business-ops` is enabled, recommend `/mvp-gap` — Evaluate what's built against this ICP
- IF `research/competitive-analysis.md` exists: check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `/pack install product-design` first; if `product-design` is enabled, recommend `/brainstorm` — Generate ideas from ICP needs + competitive gaps

**Impact-aware adjustments:**
- IF downstream impact is **Major**: prepend `/reconcile-research — [N] conflicts found in downstream docs` as the first item
- IF downstream impact is **Minor**: annotate relevant skill suggestions with "(stale — [brief description])"
- If downstream impact has not been classified yet, run the downstream impact check against the proposed output before selecting the final recommendation. Do not emit a Minor/Major impact recommendation speculatively.

### 8. Final Review & Write

Present the **complete findings summary** to the user — primary ICP, key sections, cross-ICP analysis, and build sequence. Ask:
- "Ready to write this to `research/icp.md`? Anything to adjust first?"

Only after the user confirms, write the output files.

**After writing is complete, repeat the Recommended next step from the generated `## Next Steps` section in the final chat response.**

### 9. Downstream Impact Check

After writing, check for downstream research documents that may be affected by what was just decided. Only check documents that exist on disk.

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
2. Identify **specific conflicts**: claims, assumptions, or references that contradict what was just decided. Examples:
   - A persona name or description that no longer matches the ICP
   - Competitive analysis positioning built on a different primary ICP
   - Journey stages mapped for a different user profile
   - Metric targets anchored to assumptions about a different ICP segment
   - GTM messaging addressing pain points that shifted
   - Monetization pricing tied to willingness-to-pay signals from a different ICP
   - Enterprise ICP referencing a primary ICP that changed
   - Customer feedback categorized against ICP segments that were restructured
3. Note each conflict: downstream file, section, the stale claim (quote it), and what it should now say

**Classify the impact**:
- **None**: No downstream documents exist, or no conflicts found. Skip display entirely.
- **Minor** (1–2 small conflicts): Display conflicts to user inline.
- **Major** (3+ conflicts OR a foundational assumption changed — e.g., primary ICP shifted, key pain points redefined, user profiles restructured, value proposition changed): Display conflicts and strongly recommend `/reconcile-research`.

Display to the user after showing the written file confirmation. This should be quick — one read per downstream doc, scan for conflicts against key decisions. Not a deep reconciliation.

## Output

Write two files:

### `research/icp.md`

Structure — the **Primary ICP** fills the canonical top-level sections:

```markdown
# ICP: [Primary ICP Name]

> Primary ICP selected from [N] candidates. See Additional ICPs and Cross-ICP Analysis below.
> Search log: research/icp-search-log.md

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

Scoring rationale must explicitly distinguish pain intensity from WTP quality. Strong WTP evidence includes active spend on alternatives, clear budget owner/context, high cost of inaction, tolerance for switching costs, and urgency tied to measurable economic outcomes. Weak WTP evidence includes verbal interest without budget, free-only behavior, unclear owner, or price sensitivity that outweighs pain.

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
[Do different ICPs find and choose solutions through different paths?]

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

**Recommended:** [first matching item from step 7]

**Other options:**
- [remaining conditional items from step 7 — only include items whose conditions are met]

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
- [signal]: how users describe cost of current alternatives

### → /gtm
- [signal]: where users say they found or heard about solutions
- [signal]: community or channel mentions during research
- [signal]: peer recommendation patterns observed
```

### `research/icp-search-log.md`

Raw research log containing:
- Every WebSearch query executed and why
- Key findings from each search (with source attribution)
- Evidence that supported or contradicted each ICP candidate
- The scoring rationale for primary ICP selection
- Any data gaps or areas where research was inconclusive

### `research/.progress.yaml`

Product-path manifest created or updated when secondary ICPs, Cross-ICP Analysis, or product-line recommendations create parked or promotable paths. Status values include `active`, `deferred`, `archived`, `promoted`, and `revisit_candidate`.

Create the `research/` directory if it doesn't exist.

### Product-Path Output Convention

When multiple active product paths exist or the user asks for cross-path ICP output, write:
- `research/{slug}/icp.md` — full 9-section ICP per product path (same structure as above)
- `research/{slug}/icp-search-log.md` — search log per product path
- `research/icp.md` — unified cross-path summary that references each product-path ICP, with a top-level prioritization of which product path and ICP combination to pursue first

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Stay in problem space.** Do not propose features, architecture, UI, or technical solutions. That is `/spec-interview`'s job.
- **Evidence-based.** Every claim in the ICP document must trace back to research evidence logged in `research/icp-search-log.md`. Do not fabricate personas from assumptions.
- **In existing-project mode**, note misalignments between what's built and what the ICP research suggests, but do not prescribe fixes — that's `/mvp-gap`'s job.
- **Primary ICP must use the canonical 9 top-level `##` sections** — downstream skills (`/spec-interview`, `/mvp-gap`, `/roadmap`, `/journey-map`, `/competitive-analysis`) parse these exact headers. The renamed sections (`Current Alternatives (User Perspective)`, `Stated Value Drivers`) replace the former `Market Landscape` and `Value Proposition` headers. Section 10 (`## Discovery & Evaluation Behavior`) is supplementary and does not affect downstream parsing.
- **Section 10 captures behavioural signals only** — how personas find, evaluate, and choose solutions. Do not include GTM strategy, channel analysis, budget authority, procurement process, or pricing expectations — those belong in downstream skills (`/gtm`, `/monetization`, `/enterprise-icp`).
- **WTP is evidence, not pricing strategy.** Capture budget ownership, paid alternatives, current spend/time-cost proxies, switching-cost tolerance, economic urgency, and price sensitivity cues only as segment-fit and urgency evidence. Do not convert WTP evidence into pricing recommendations, packaging, discounting, ARPA targets, or monetization strategy; route those raw signals to `/monetization`.
- **Do not overwrite existing `research/icp.md`** without asking the user first.
- **Minimum research depth**: at least 8 WebSearch queries before identifying ICP candidates, then at least 2–3 targeted queries per candidate.
- **Present before writing.** Never write output files until findings have been presented to the user and validated through the checkpoint questions. The user must see and approve the analysis before anything is written to disk.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/icp-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
