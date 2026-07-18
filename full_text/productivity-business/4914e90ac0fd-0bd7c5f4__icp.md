---
name: icp
description: Research-driven ICP discovery — web search + codebase analysis to identify multiple ICPs, pain points, value props, and cross-ICP prioritization
type: research
version: v0.1
argument-hint: <spec file path, concept/idea, or empty to use concept brief>
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `/pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# ICP — Research-Driven Customer Discovery

## Report-First Approval Gate

Default to report-only: present findings, evidence coverage, assumptions, recommended artifact path, and proposed file changes in a pre-approval alignment page plus a concise conversation summary for user approval before creating or updating canonical research, spec, or task files.

Do not write or overwrite synthesized deliverables until the user explicitly approves, unless the user invoked an explicit write/update/fix mode or clearly asked to write files upfront. Raw evidence capture may be persisted before analysis when reproducibility requires it; report those raw paths separately and still gate synthesized research/report writes.

When stopping for approval, build and attempt to open the alignment preview page first, then ask the user to review it and approve, question, or request adjustments. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

Automated research that identifies **multiple ICP candidates**, maps their pain points and value props, scores them, and selects a primary ICP. Replaces interview-driven approaches with web search + codebase analysis. Input is a spec file path, concept/idea as `$ARGUMENTS`, or `research/concept-brief.md` / `research/{app}/concept-brief.md` when present.

The output preserves the canonical 9-section format at the top level (for downstream compatibility with `/spec-interview`, `/mvp-gap`, `/roadmap`, `/journey-map`) while adding multi-ICP analysis, cross-ICP prioritization, and a supplementary section 10 (`## Discovery & Evaluation Behavior`) that captures how personas find, evaluate, and choose solutions.

## Process

### 0. App Scope Resolution (Monorepo Support)

Before parsing input, determine the app scope:

1. If `$ARGUMENTS` specifies an app name matching a subdirectory of `research/`, use it.
2. If `research/` contains subdirectories (excluding files), list them and ask the user which app to target. If only one subdirectory exists, use it automatically.
3. If no subdirectories exist, proceed with flat structure (single-product mode).

When app scope `{app}` is active:
- Read/write research from `research/{app}/` instead of `research/`
- Read/write specs from `specs/{app}/` instead of `specs/`
- Prefer `research/{app}/concept-brief.md` as concept context when present
- Also read `research/icp.md` (cross-app overview) for broader context

### 1. Parse Input & Gather Context

**Read `$ARGUMENTS`:**
- If it's a file path, read the file for product/concept context
- If it's text, treat it as the concept or idea description
- If empty, check for `research/{app}/concept-brief.md` in app scope or `research/concept-brief.md` in flat scope first; then check `specs/spec.md`, `specs/plan.md`, or README for context — if nothing exists, ask the user what product or idea to research

**Read concept brief if present:**
Read `research/{app}/concept-brief.md` in app scope, or `research/concept-brief.md` in flat scope, whenever it exists. Treat it as starting context and source hypotheses, not as settled truth. Use its problem hypothesis, beneficiary hypothesis, value wedge, constraints, non-goals, and ICP readiness notes to frame search queries and candidate generation. If `$ARGUMENTS` conflicts with the concept brief, flag the mismatch at the first checkpoint and ask which premise should guide ICP research.

**Read codebase (if it exists):**
Read CLAUDE.md, README, package config, key source files, routes, and data models to understand what's been built. This grounds the research in reality rather than pure market abstraction.

**Read existing research** (`research/icp.md`, `research/competitive-analysis.md`, etc.) and specs if they exist — use as background context but do not treat as settled. This research may reshape direction.

**Detect monorepo structure:**
Check for monorepo indicators (`turbo.json`, `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, or `package.json` workspaces). If found, identify sub-apps or packages that serve **distinct user-facing products** (ignore shared libraries, configs, and internal tooling). When multiple distinct products exist, run the full ICP process separately for each — produce `research/{app-name}/icp.md` per app, plus a unified `research/icp.md` that cross-references all app-level ICPs with a top-level prioritization of which app/ICP to pursue first. If the monorepo contains only one user-facing product, proceed as normal with a single `research/icp.md`.

**Migrate old convention:** If `research/icp-{app}.md` files exist (old naming), offer to move them to `research/{app}/icp.md` (and corresponding search logs to `research/{app}/icp-search-log.md`). Create the subdirectories as needed.

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

Use WebFetch to pull in particularly relevant pages for deeper analysis when search snippets aren't enough.

**Classify the business model** into one or more of: B2B SaaS (PLG), B2B SaaS (SLG), B2C, B2C subscription, marketplace/platform, B2B2C, D2C, open-source/open-core, API/developer-first. Document the classification with evidence in the search log. This classification gates which sub-sections appear in the `## Discovery & Evaluation Behavior`.

### 3. Identify ICP Candidates — Present & Validate

From the research evidence, cluster findings into **2–5 distinct ICP candidates**. For each candidate, note:
- Who they are (role, company type, size)
- What pain evidence exists
- How accessible they are (can we reach them?)
- How much value we could deliver

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
- **Stated Value Drivers** — what customers say matters to them in their own language; the "aha moment" as users describe it, not strategic positioning
- **Customer ↔ User Dynamics** — post-purchase buyer-user relationship: provisioning, onboarding, admin vs end-user dynamics. For B2B, the detailed buying process and decision-making unit live in `## Discovery & Evaluation Behavior`; this section focuses on the post-purchase relationship.
- **Discovery & Evaluation Behavior** — how this persona found, evaluated, and chose solutions. Capture behavioural signals only (where they searched, who they asked, what they compared) — not channel strategy or GTM analysis. Use findings to populate section 10.

### 5. Score & Select Primary ICP — Present & Validate

Build a **Value x Accessibility** scoring matrix:

**Value score** (how much we can help):
- Pain severity and frequency
- Willingness to pay (budget signals)
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

**Checkpoint 3 — Present the cross-ICP analysis and recommended build sequence to the user.** Use the AskUserQuestion tool to show the analysis with evidence: shared pains with source data from each ICP, conflicts with specific examples, and build sequence rationale grounded in the scoring matrix. Then ask:
- "Does this sequencing make sense for where you are right now?"
- If conflicts exist between ICPs, ask the user to weigh in on the trade-offs

Incorporate feedback before proceeding.

### 7. Populate Next Steps

Before writing, check which files exist to populate the `## Next Steps` section contextually. Include 3–5 applicable items with "Pick one:" framing:

- ALWAYS: `/competitive-analysis` — Research competitors and market gaps for this ICP
- IF no `specs/` directory or it's empty: `/spec-interview` — Design the solution for this ICP's pain points
- IF `specs/` exist but no `research/journey-map.md`: `/journey-map` — Map how this ICP flows through the product
- IF codebase exists: `/mvp-gap` — Evaluate what's built against this ICP
- IF `research/competitive-analysis.md` exists: `/brainstorm` — Generate ideas from ICP needs + competitive gaps

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

**Downstream documents to check** (use `{app}/` prefix when app scope is active):
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

Pick one:
- `/competitive-analysis` — Research competitors and market gaps for this ICP
- [conditional items from step 7 — only include items whose conditions are met]

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
- [signal]: budget signals or willingness-to-pay mentions
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

Create the `research/` directory if it doesn't exist.

### Monorepo Output Convention

When a monorepo has multiple distinct user-facing products, write:
- `research/{app-name}/icp.md` — full 9-section ICP per app (same structure as above)
- `research/{app-name}/icp-search-log.md` — search log per app
- `research/icp.md` — unified cross-app summary that references each app-level ICP, with a top-level prioritization of which app/ICP combination to pursue first

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
- **Do not overwrite existing `research/icp.md`** without asking the user first.
- **Minimum research depth**: at least 8 WebSearch queries before identifying ICP candidates, then at least 2–3 targeted queries per candidate.
- **Present before writing.** Never write output files until findings have been presented to the user and validated through the checkpoint questions. The user must see and approve the analysis before anything is written to disk.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/icp-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.

**Discovery-specific gates.** Render evidence coverage, assumptions/confidence, recommended path, artifact destination, proposed file changes, approval, and post-approval route as gates before creating or updating canonical discovery artifacts.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/icp-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/spec document (`research/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.
- Keep any existing user approval requirement before overwriting or replacing a document; archiving does not replace asking when the skill already requires approval.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>` so the next operator has a concrete handoff.
- If this skill creates or modifies tracked repository files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping, even if the user did not explicitly ask for commit/push.
- Do not leave tracked changes or unpushed commits behind. If unrelated tracked work is already present, either include it in sensible commits too or stop and explain the blocker.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, or production deploy confirmation.
