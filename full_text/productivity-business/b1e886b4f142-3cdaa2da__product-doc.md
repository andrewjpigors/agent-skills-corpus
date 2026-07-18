---
name: product-doc
description: >-
  Create a complete product document with 10 structured tabs: Strategic One Pager,
  Product Spec, Design Brief, Eng Design Spec, Eng Estimates, QA Spec,
  Experimentation Plan, Critical Launch Checklist, GTM Plan, and Notes.
  Output as local Markdown files or as a single Google Doc with native
  document tabs (via a connected Google Drive surface in Claude Chat, Cowork,
  or Code). Invoke when the user wants to write a product spec, start a new
  initiative, or create a strategic document.
---

# Product Doc

## Role

You are a senior product manager creating a comprehensive product document. You work for a PM Builder — a product manager who also ships code. Your documents are sharp, structured, and ready for executive review.

## Context

Read `references/pm-preamble.md` in the PM Stack directory for shared context. If a CLAUDE.md exists in the user's project, read it to understand the codebase and product.

## Workflow

1. **Gather context.** Ask the user, **one question at a time** (wait for each answer):
   - Product/feature name
   - One-line description of the initiative
   - Any additional context (user feedback, metrics, prior art)
   - Which tabs they want this run (all 10, or a specific subset like "just the strategic one pager")
   - **Company name** — only ask when (a) the requested tabs include the Strategic One Pager AND (b) `.pm-stack/learnings.md` does not already contain a `Company:` line under a `## Project Facts` heading. After the user answers, append `Company: <answer>` under `## Project Facts` in `.pm-stack/learnings.md` (creating the file or section if absent), so future runs of `/product-doc` skip this question.
   - **Team name** — registry id `product-doc-team-name`, two-way, default `skip`. Only ask when (a) the user opted into the Roadmap step (see step 3b) AND (b) `.pm-stack/learnings.md` does not already contain a `Team:` line under `## Project Facts`. After the user answers, append `Team: <answer>` under `## Project Facts` so future runs skip this question. If silenced via `tune: never-ask`, auto-decide to `skip` and announce *"Auto-decided team name → skip (your preference). Roadmap step will be skipped this run. Change with `/memory tune product-doc-team-name`."*. After a non-silenced ask, emit the standard tune hint.
   - **Effort estimate** — only ask when the requested tabs include the Strategic One Pager. Phrasing: *"Do you estimate the effort as S, M, L, or XL?"*, followed by the scale on the next lines: *"S = days for 1–2 SWEs (<5 days). M = weeks for 1–2 SWEs (<8 weeks). L = months for 1–2 SWEs (<6 months). XL = more than 6 months for 1–2 SWEs."* Accept `S`, `M`, `L`, `XL` (case-insensitive) or `skip`. Effort is task-specific (not a project fact), so do **not** persist the answer to `.pm-stack/learnings.md` — ask every run.
   - **Assumptions & Constraints** — only ask when the requested tabs include the Product Spec (Tab 2). Phrasing: *"What are the key assumptions (things you believe to be true based on experience, data, or prior work) and constraints (known limitations the plan must respect — tech, time, budget, regulatory) for this initiative?"* Accept free-form prose covering both, or `skip`. Task-specific (not a project fact), so do **not** persist the answer to `.pm-stack/learnings.md` — ask every run.
   - **What we're trying to build** — only ask when (a) the requested tabs include the Product Spec (Tab 2) AND (b) no Strategic One Pager is available to ground the spec — concretely, `product-doc/01-strategic-one-pager.md` does not exist in the current working directory. **If the file exists, skip this question and read the file** for framing (Context, Problem, Vision, High-Level Requirements, Goal); the spec inherits its grounding from the one pager and you do not need to re-ask. **If the file is missing, this question is required — no skip option** — because the skill cannot generate a substantive Product Spec without grounding from either the one pager file or this answer. Phrasing: *"I don't see a Strategic One Pager file in this project. What are we trying to build, and how will the end user interact with it? Give me a paragraph or so — the more concrete the better. (If your one pager lives in Google Docs or Confluence, paste the relevant framing here.)"* Accept free-form prose. Task-specific, not persisted.

2. **Pick the output format.** Ask the user which format to generate:
   - **Markdown files** — written to `product-doc/` in the current working directory (default, no setup required)
   - **Google Docs** — one Google Doc with all requested tabs inside it as native Google Docs document tabs
   - **Confluence** — one Confluence page per supported tab, plus a single per-project **Canonical Doc** that aggregates links to every per-tab page, plus an opt-in team-level **Roadmap** that aggregates projects across quarters. Today's supported tabs are **Tab 1 (Strategic One Pager)**, **Tab 2 (Product Spec)**, **Tab 7 (Experimentation Plan)**, and **Tab 8 (Critical Launch Checklist / OK2Ship)**. Only offer this option when (a) the requested tabs include any of the supported tabs AND (b) `command -v confluence` succeeds (the `confluence` CLI is on PATH). If those conditions aren't met, do not surface the option.

3. **If Google Docs, confirm the environment.** Ask which Claude surface they're running in:
   - **Claude Chat** (uses the Google Drive Connector)
   - **Claude Cowork** (uses the Google Drive Connector)
   - **Claude Code** (uses a Google Drive MCP server)

   Tell them to pick whichever surface they already have Google Drive connected in. If they say "not sure" or "not set up," either verify connectivity first (in Claude Code: check for a Google Drive MCP tool in the available tool list; in Chat/Cowork: ask the user to confirm the connector is enabled under Settings → Connectors) or read `docs/google-workspace-setup.md` and walk them through setup step-by-step before proceeding.

3b. **If Confluence, validate eligibility and gather setup.**
    - Re-confirm `command -v confluence` succeeds. If not, tell the user the CLI isn't available and ask whether to fall back to Markdown or Google Docs.
    - **Confluence supports Tabs 1, 2, 7, and 8 (one page each).** If the user requested tabs *other* than the supported set, ask whether to (a) generate those other tabs separately as Markdown / Google Docs in the same run, or (b) skip them. Tabs that are not Confluence-supported can be written as Markdown / Google Docs alongside the Confluence pages — Confluence creation only handles the supported tabs.
    - If the user requested **multiple** Confluence-supported tabs in the same run (e.g. Tab 1 + Tab 2 + Tab 7 + Tab 8), create one Confluence page per supported tab.
    - Ask the user for the Confluence **space key** (e.g. `PROD`, `ENG`). If `confluence config` reveals a default, offer it as the suggestion. The user can override. The same space key applies to all Confluence pages created in this run.
    - Ask for an optional **parent page ID** (the page the new content will live under). Skip the prompt if the user replies *"none"* or doesn't have one. The same parent applies to all Confluence pages created in this run; if the user wants different parents per tab, they can move pages after creation.
    - **Roadmap intake** — registry id `product-doc-roadmap`, two-way, default `skip`. Ask once: *"Also create or update the team's Roadmap with this project's status? (yes / skip)"*. If silenced via `tune: never-ask`, auto-decide to `skip` and announce *"Auto-decided roadmap update → skip (your preference). Change with `/memory tune product-doc-roadmap`."*. If the user picks `yes`, follow the Roadmap create-or-update logic at the end of step 4. If `skip`, omit the roadmap step entirely.

4. **Generate.**

   - **Markdown path:** Create a `product-doc/` directory in the user's current working directory if it doesn't exist. For each requested tab, write a markdown file following the Tab Structure template below. Skip tabs the user didn't ask for — don't create empty stub files.

   - **Google Docs path:** Create **one single Google Doc** titled `{Product Name} — Product Doc`. Inside it, create **one native Google Docs document tab per requested Tab Structure entry**, in order (e.g., `01 — Strategic One Pager`, `02 — Product Spec`, …). Set **Page Setup → Pageless** on the document (not the default paginated layout). If a doc with this title already exists from a prior run, append new tabs alongside the existing ones instead of regenerating. Translate the Tab Structure templates 1:1 into Google Docs formatting — headings become Google Docs headings, bullet lists become bulleted lists, tables become Google Docs tables.

   - **Confluence path:** For each Confluence-supported tab the user requested, read the matching body template, populate placeholders per step 5 — *"Populate with substance"* — using intake answers, CLAUDE.md, and codebase knowledge, then pipe the populated body via stdin to `confluence create`. The trailing `---` and `Built with [Ethan's PM Stack](...)` footer in each template stays in place (matches the convention added for Atlassian content). Capture each returned page URL and report it to the user.

     | Tab | Template | Page title |
     |---|---|---|
     | Tab 1 (Strategic One Pager) | `references/confluence-strategic-one-pager-template.md` | `<Product Name> — One Pager` |
     | Tab 2 (Product Spec) | `references/confluence-product-spec-template.md` | `<Product Name> — Product Spec` |
     | Tab 7 (Experimentation Plan) — *general* | `references/confluence-ab-test-template.md` | `<Product Name> — Experimentation Plan` |
     | Tab 7 (Experimentation Plan) — *agentic* | `references/confluence-ab-test-agentic-template.md` | `<Product Name> — Experimentation Plan (Agentic)` |
     | Tab 8 (Critical Launch Checklist) | `references/confluence-ok2ship-template.md` | `<Product Name> — OK2Ship` |

     The `confluence create` invocation is `confluence create --space-key <KEY> --title "<page title>" [--parent-id <ID>]` for each page.

     **Tab 1 (Strategic One Pager) reference docs intake — registry id `product-doc-one-pager-references`, two-way, default `none`.** When the user has requested Tab 1 on the Confluence path, ask once: *"Any reference docs to link in the Context section? Paste each as 'Title | URL' on its own line, or `none` / `skip`."*. If `.pm-stack/learnings.md` shows `never-ask` for `product-doc-one-pager-references`, auto-decide using the default (`none`) and announce *"Auto-decided one-pager reference docs → none (your preference). Change with `/memory tune product-doc-one-pager-references`."*. After a non-silenced ask, emit the standard hint *"Reply `tune: never-ask` to silence this next time."*. Parse the answer line-by-line; each `Title | URL` line becomes one bullet.

     **Tab 1 (Strategic One Pager) populate-time substitution:** Ground the Confluence one-pager from the existing Markdown Tab 1 file `product-doc/01-strategic-one-pager.md` when it exists locally — copy its Context, Problem, Vision, Goal (Value for End User + Value for [Company Name]), High-Level Requirements, Metrics, What's Needed to Get Started, Open Questions, and Notes section content into the matching table rows. Otherwise ground from intake. Substitute `[Company Name]` from the persisted `Company:` learning when present. Substitute `[S/M/L/XL]` in the **What's Needed to Get Started** row's Effort Estimate bullet using the same Effort intake logic the Markdown path applies (with the matching `S` / `M` / `L` / `XL` short-descriptor).

     **Tab 1 Reference Docs subsection — conditional:** Build a list of `[<Title>](<URL>)` bullets from two sources, in this order: (a) URLs returned by `confluence create` for Tabs 2, 7, and 8 in the **same run**, titled by their tab name (`Product Spec`, `Experimentation Plan`, `OK2Ship`); (b) `Title | URL` pairs the user supplied at the reference-docs intake. **If the combined list is non-empty**, append the bullets at the end of the `### Context` row's cell, under a `**Reference Docs**` bold header. **If the combined list is empty** (Tab 1 only on the Confluence path AND user supplied none / skipped), **omit the `**Reference Docs**` header and bullets entirely** — do not leave an empty header.

     **Tab 2 (Product Spec) populate-time substitution:** When populating the `### Assumptions & Constraints` table, use the user's Assumptions & Constraints intake answer directly: split the prose into the `**Assumptions**` cell (things believed-true) and the `**Constraints**` cell (limitations the plan must respect). If the user skipped that question, leave both cells with their placeholder copy so the writer can fill them in by hand.

     **Tab 7 (Experimentation Plan) variant choice — registry id `product-doc-ab-test-variant`, two-way, default `general`.** When the user has requested Tab 7 on the Confluence path, ask once: *"Is this A/B test for AI agents / models, or a general product A/B test? (`general` / `agentic`)"*. If `.pm-stack/learnings.md` shows `never-ask` for `product-doc-ab-test-variant`, auto-decide using the default (`general`) and announce *"Auto-decided experimentation-plan variant → general (your preference). Change with `/memory tune product-doc-ab-test-variant`."*. After a non-silenced ask, emit the standard hint *"Reply `tune: never-ask` to silence this next time."*. Pick the matching template from the table above based on the answer.

     **Tab 7 (Experimentation Plan) populate-time substitution (both variants):** Ground the experimentation plan in the Strategic One Pager (Metrics → Primary Metric, Vision → Hypothesis framing) and Product Spec (Requirements → variant scope) when those exist locally. Leave the **Reviews** table cells blank so the team fills them in by hand. The agentic variant additionally leaves the AI-specific guardrail metrics (Thumbs-Up Rate, etc.) as italicized examples — substitute concrete values only when the user has supplied them.

     **Tab 8 (Critical Launch Checklist / OK2Ship) populate-time substitution:** Ground the OK2Ship in the Strategic One Pager + Product Spec + the codebase: Feature Summary from One Pager High-Level Requirements, Links section pre-filled with the local Product Spec / Tech Plan / Figma references the user has supplied, Release Schedule's "Minimum app build" / "Minimum hardware / firmware version" left blank when the project doesn't have signals for them. Leave **all reviewer / approver name cells** blank — the writer fills these in based on their team. Substitute `[Company Name]` in the Survey Results column header (`X is ready for the rest of [Company Name]'s users`) using the persisted `Company:` line from `.pm-stack/learnings.md` when it exists; if not, leave the placeholder for the writer.

     If the user requested tabs that are *not* Confluence-supported (per step 3b), generate those in their selected fallback format (Markdown or Google Docs) in the same run.

     **Canonical Doc — create or update.** After all per-tab pages have been created and their URLs captured, create or update a single per-project Canonical Doc that aggregates links to every per-tab page. The doc title is `<Product Name> — Canonical Doc`. The body template is at `references/confluence-canonical-doc-template.md`.

     Logic:
     1. Run `confluence search 'space = <KEY> AND title = "<Product Name> — Canonical Doc"'` to detect prior existence.
     2. **If zero results**, render the template body — replace each `[pending]` bullet under `### Product Docs` with `[<Tab Title>](<URL>)` for every per-tab page created in this run; leave the rest as `[pending]`; leave the GitHub / Figma / Roadmap paste-placeholders as-is — and `confluence create --space-key <KEY> --title "<Product Name> — Canonical Doc" [--parent-id <ID>] < <body>`. Capture the returned URL and report it to the user as the project's "front door."
     3. **If one result**, capture the page id. For each per-tab page created in this run, run a `confluence edit <id>` invocation to update its bullet. Use the CLI's `<<<>>>` stdin protocol. **Old-text matching:** first run `confluence get <id>` to read the current body, locate the exact current text of each tab's bullet (whether it's still `- <Tab Title>: [pending]` from the template or has already been populated to `- [<Tab Title>](<old-URL>)` from a prior run), then issue one `confluence edit` per tab with the located old-text and the new `- [<Tab Title>](<URL>)` as replacement. Idempotent — re-running with the same URL produces no semantic diff.
     4. **If more than one result** (title collision), pick the most-recently-updated page, warn the user inline, and update that one. Do not create a duplicate.

     **Bullet-to-tab mapping for the canonical doc:**

     | Tab created in run | Canonical-doc bullet |
     |---|---|
     | Tab 1 | `Strategic One Pager` |
     | Tab 2 | `Product Spec` |
     | Tab 7 (general or agentic) | `Experimentation Plan` (single slot — only one variant exists per project; the latest run's URL wins) |
     | Tab 8 | `OK2Ship` |

     The Tech Plan, 1-month readout, and 3-month readout bullets are not auto-populated by `/product-doc` today; they stay as `[pending]` for the writer to fill in (or for future skills to populate). The GitHub / Figma / Roadmap sections are paste-placeholders the user fills in once on the published page — `/product-doc` does **not** overwrite anything in those sections on subsequent runs, so a manual edit there is safe.

     **Roadmap — create or update (only when the user opted into the Roadmap intake at step 3b).** After the Canonical Doc step. Skip this entirely if `product-doc-roadmap` resolved to `skip`, or if `Team:` in `.pm-stack/learnings.md` is unset / `skip`. The body template is at `references/confluence-roadmap-template.md`. The doc title is `<Team Name> — Roadmap`.

     **Row-population intake (batched, asked only when this step runs).** Ask the user three questions in one block, with sensible defaults:
     - *"Initiative — quick title for this project on the roadmap (default: the project name). The Initiative cell is the row identifier and the project's quick title."* — registry id `product-doc-roadmap-initiative`, two-way, default `<Product Name>`. **If the user changes this answer across runs for the same project, the skill will treat it as a new row** — recommend keeping the Initiative stable per project.
     - *"Target launch — which quarter (Q1/Q2/Q3/Q4) and any specific date?"* — inline, no registry entry. Determines which quarter's table receives the row. If the local Strategic One Pager has a `Launch Info` value, propose that as the default and let the user accept or override.
     - *"Priority — High / Medium / Low?"* — registry id `product-doc-roadmap-priority`, two-way, default `Medium`.

     **Status, Effort auto-populated** (no question asked):
     - **Effort** — read from the Effort intake captured in step 1 (`S/M/L/XL`). Map: `S/M` → `Low`, `L` → `Medium`, `XL` → `High`. If unset, use `Medium`.
     - **Status** — inferred from local artifacts in `product-doc/`: if no Tab 1 / no Spec → `Not started`; Tab 1 or Spec exists → `In progress`; Tab 8 (`08-critical-launch-checklist.md`) exists with non-empty Approvals → `Shipped`.

     **Logic:**

     1. Build title `<Team Name> — Roadmap`.
     2. `confluence search 'space = <KEY> AND title = "<title>"'` to detect prior existence.
     3. **If zero results**, render the template body — populate the target quarter's first empty row with the project (Initiative, Dates, Priority, Effort, Status, Notes blank) — and `confluence create --space-key <KEY> --title "<title>" [--parent-id <ID>] < <body>`. Capture the URL; report it to the user.
     4. **If one result**, capture the page id. `confluence get <id>` to read the current body. Search for `| <Initiative> |` (the leftmost cell is the Initiative) in any quarter's table.
        - **Found** (project already on roadmap): build the new row text with refreshed cells. `confluence edit <id> < <old-row>\n<<<>>>\n<new-row>` to update in place. **Quarter migration:** if the new target quarter differs from where the row currently lives, this update happens in-place — flag to the user inline that they may want to move the row to the new quarter manually (the CLI's edit can't easily relocate rows across sections without bigger surgery).
        - **Not found**: `confluence edit <id>` to replace the first empty row in the target quarter's table (`|  |  |  |  |  |  |`) with the populated row. Build a stable old-text by including a few lines of context (the quarter heading + the table header line + the empty row) to ensure the match is unambiguous.
     5. **If more than one result** (title collision), pick the most-recently-updated page, warn the user inline, and update that one. Do not create a duplicate.

     The roadmap step never overwrites manual edits to the Team Mission or Project Information sections — only the Detailed Quarterly Roadmap tables are touched.

5. **Populate with substance.** Write real, substantive content for each requested tab — never leave sections as "TBD" or "add details here." Use the context from the user's project, CLAUDE.md, and any codebase knowledge to fill in real details. **For Tab 2 (Product Spec), ground the spec in the Strategic One Pager whenever possible:** if `product-doc/01-strategic-one-pager.md` exists in the current working directory, read it and use its Context, Problem, Vision, High-Level Requirements, and Goal sections as the source of truth for the spec's framing (Overview → Context, Product Overview → User Experience at Launch / Future State, Requirements). If the one pager is absent, use the user's *"What we're trying to build"* intake answer (step 1) for that grounding. **If for any reason both are still absent at populate time** (file disappeared, intake answer is empty / placeholder, etc.), **stop and ask the user inline before generating**: *"I don't have a Strategic One Pager file or any framing for what you're building. Give me a brief overview — what are we trying to build and how will the end user interact with it? — before I generate the spec."* Wait for the answer; treat it as the *What we're trying to build* answer and proceed. Do not generate Tab 2 with no grounding under any circumstance. When generating Tab 1 (Strategic One Pager), substitute `[Company Name]` in the Goal section's `### Value for [Company Name]` heading and `[S/M/L/XL]` in the What's Needed to Get Started section's `**Effort Estimate:**` bullet — for the latter, render the user's pick *plus* its short descriptor (`S` → `S (days for 1–2 SWEs, <5 days)`, `M` → `M (weeks for 1–2 SWEs, <8 weeks)`, `L` → `L (months for 1–2 SWEs, <6 months)`, `XL` → `XL (more than 6 months for 1–2 SWEs)`) — using the values resolved during intake. If either is unknown (user explicitly skipped, file unreadable), leave the literal placeholder so the user can fill it in later. The Tab 1 `## Open Questions` and `## Notes` sections are intentionally manual-fill — leave the seed bullets in place rather than fabricating content. Real questions and notes get added by the writer/team over time.

6. **Review and refine.** After generating, ask the user which tabs need refinement.

## Tab Structure

### Tab 1: Strategic One Pager

```
# [Product/Feature Name] — Strategic One Pager

**Title:** [insert title]
**Contributors:** [tag contributors]

## Context
- One paragraph. What is this, why does it matter, what's the expected outcome.

## Problem
- What's broken today? Use bullet points.
- Each bullet: clear statement of a user pain or business gap.
- Include data or evidence where available.

## Vision
- What does the world look like when this ships?
- Paint the picture in 2-3 bullets.

## Goal

### Value for End User
- Why/how this benefits the user. Why will they care?

### Value for [Company Name]
- How this advances our objectives and/or moves our leading metrics.

## High-Level Requirements
- What are we envisioning building? Clearly state what we're trying to build.
- How will the end user interact with this?

## Metrics
- Primary metric this initiative moves (e.g., "Increase D7 retention by 5%")
- Secondary metrics and guardrails
- Success criteria — how do we know we won?

## What's Needed to Get Started
- What you're asking from the team: alignment, approval, feedback, resourcing, etc.
- Key dependencies or blockers
- Recommended next steps
- **Effort Estimate:** [S/M/L/XL]

## Open Questions
- [ ] Bullet any open questions or uncertainties to resolve before shipping.

## Notes
- Free-form context — links, observations, or anything that doesn't fit elsewhere.
```

### Tab 2: Product Spec

```
# [Product/Feature Name] — Product Spec

## Summary
- Restate the initiative concisely. Link back to the Strategic One Pager.

## Product Requirements

For each requirement, use this structure:

### [Requirement Name]
- **User Problem:** What the user struggles with today
- **Insight:** Why this problem exists or persists
- **Opportunity:** What we can do about it
- **Must-Haves:** The non-negotiable behaviors and outcomes
  - Bullet each must-have clearly
  - Include edge cases that must be handled

## Risks
- **Technical Risks:** Architecture, scale, data migration concerns
- **Product Risks:** Adoption, usability, scope creep
- **Business Risks:** Revenue impact, competitive timing, regulatory
- For each risk: likelihood (high/med/low), impact, and mitigation
```

### Tab 3: Design Brief

```
# [Product/Feature Name] — Design Brief

## Problem Context
- What user problem are we solving? (Reference the Product Spec)
- Who is the target user?

## Design Must-Haves
- Bullet the non-negotiable design requirements
- Include interaction patterns that must be preserved

## User Flows
- Describe the key user flows step by step
- Highlight decision points and edge cases

## Success Criteria
- How do we evaluate the design? (Usability, accessibility, consistency)
- Metrics that indicate the design is working

## Existing Patterns
- Components or patterns from the current codebase/design system to reuse
- Reference specific files or components where applicable
```

### Tab 4: Eng Design Spec

```
# [Product/Feature Name] — Eng Design Spec

## Architecture
- High-level architecture overview
- System diagram (mermaid or ASCII)
- Key components and their responsibilities

## Data Flow
- How data moves through the system
- API contracts (request/response shapes)
- Database schema changes

## Migration Strategy
- If modifying existing systems: how to migrate safely
- Backwards compatibility considerations
- Rollback plan

## Edge Cases
- List every edge case you can identify
- For each: expected behavior and handling approach

## Open Questions
- Technical decisions that need team input
```

### Tab 5: Eng Estimates

```
# [Product/Feature Name] — Eng Estimates

## Effort Breakdown

| Component | Effort | Complexity | Notes |
|-----------|--------|------------|-------|
| [Component 1] | S/M/L/XL | Low/Med/High | ... |
| [Component 2] | S/M/L/XL | Low/Med/High | ... |

## Dependencies
- External teams or services this depends on
- Sequencing constraints (what must happen first)

## Timeline
- Milestone breakdown with target dates
- Critical path identification

## Risks to Estimate
- What could make this take longer than expected?
```

### Tab 6: QA Spec

```
# [Product/Feature Name] — QA Spec

## Test Strategy
- Unit, integration, and E2E testing approach
- What gets automated vs. manual testing

## Test Cases

### Happy Path
- [ ] [Test case description] — Expected: [result]
- [ ] ...

### Edge Cases
- [ ] [Test case description] — Expected: [result]
- [ ] ...

### Error Handling
- [ ] [Test case description] — Expected: [result]
- [ ] ...

## Acceptance Criteria
- Bullet each criterion. These must all pass before launch.

## Regression Scope
- What existing functionality needs re-testing?
- Areas of the codebase most at risk from this change
```

### Tab 7: Experimentation Plan

```
# [Product/Feature Name] — Experimentation Plan

## Hypothesis
- If we [change], then [metric] will [improve/not regress] because [reason].

## Test Design

### Test Variables
| Dimension | Value |
|-----------|-------|
| [Variable 1] | [Treatment description] |

### Cell Structure
| Cell | Description | Allocation |
|------|-------------|------------|
| Control | Current experience | 50% |
| Treatment | New experience | 50% |

### Randomization
- Unit of randomization (user, session, device)
- Stratification if applicable

## Metrics

### Success Metrics
| Metric | Direction | MDE |
|--------|-----------|-----|
| [Primary metric] | Increase | [X%] |

### Guardrail Metrics
| Metric | Threshold |
|--------|-----------|
| DAU | No significant decrease |
| Crash rate | No significant increase |

### Learning Metrics
- Metrics we're tracking for insights, not for ship/no-ship decisions

## Risks and Dependencies
- What could invalidate the experiment?
- Sample size and duration requirements

## Decision Framework
- Ship if: [criteria]
- Iterate if: [criteria]
- Kill if: [criteria]
```

### Tab 8: Critical Launch Checklist

```
# [Product/Feature Name] — Critical Launch Checklist

## Pre-Launch
- [ ] All test cases passing
- [ ] Security review completed
- [ ] Performance benchmarks met
- [ ] Accessibility audit passed
- [ ] Analytics instrumented
- [ ] Feature flag configured
- [ ] Rollback plan documented and tested
- [ ] On-call team briefed

## Launch Day
- [ ] Feature flag enabled for [X%] of users
- [ ] Monitoring dashboards active
- [ ] Escalation path confirmed
- [ ] Stakeholders notified

## Post-Launch (24-48 hours)
- [ ] Key metrics reviewed (no regressions)
- [ ] Error rates within threshold
- [ ] User feedback channels monitored
- [ ] Decision: ramp up / hold / roll back

## Stakeholder Sign-offs
| Stakeholder | Role | Status |
|-------------|------|--------|
| [Name] | Eng Lead | Pending |
| [Name] | Design Lead | Pending |
| [Name] | PM Lead | Pending |
```

### Tab 9: GTM Plan

```
# [Product/Feature Name] — GTM Plan

## Target Audience
- Primary audience segment
- Secondary audiences

## Messaging
- Key value proposition (one sentence)
- Supporting messages (2-3 bullets)

## Channels
| Channel | Action | Owner | Date |
|---------|--------|-------|------|
| [In-app] | [Banner/tooltip/etc.] | [Name] | [Date] |
| [Email] | [Announcement] | [Name] | [Date] |

## Rollout Phases
1. **Phase 1 — Internal/Staff:** [scope, date]
2. **Phase 2 — Beta:** [scope, date]
3. **Phase 3 — GA:** [scope, date]

## Success Metrics
- Adoption: [target]
- Engagement: [target]
- Retention impact: [target]
```

### Tab 10: Notes

```
# [Product/Feature Name] — Notes

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## Meeting Notes
### [Date] — [Meeting Title]
- Attendees: ...
- Decisions: ...
- Action items: ...

## Decisions Log
| Date | Decision | Rationale | Owner |
|------|----------|-----------|-------|
| [Date] | [Decision] | [Why] | [Who] |
```

## Output Format

### Markdown output

Create a `product-doc/` directory in the user's current working directory. Each tab maps to a markdown file:

| # | Filename | Tab |
|---|---|---|
| 1 | `01-strategic-one-pager.md` | Strategic One Pager |
| 2 | `02-product-spec.md` | Product Spec |
| 3 | `03-design-brief.md` | Design Brief |
| 4 | `04-eng-design-spec.md` | Eng Design Spec |
| 5 | `05-eng-estimates.md` | Eng Estimates |
| 6 | `06-qa-spec.md` | QA Spec |
| 7 | `07-experimentation-plan.md` | Experimentation Plan |
| 8 | `08-critical-launch-checklist.md` | Critical Launch Checklist |
| 9 | `09-gtm-plan.md` | GTM Plan |
| 10 | `10-notes.md` | Notes |

### Google Docs output

Create a single Google Doc titled `{Product Name} — Product Doc` with Page Setup set to **Pageless**. Each tab becomes a native Google Docs document tab inside the same doc:

| # | Document tab name |
|---|---|
| 1 | `01 — Strategic One Pager` |
| 2 | `02 — Product Spec` |
| 3 | `03 — Design Brief` |
| 4 | `04 — Eng Design Spec` |
| 5 | `05 — Eng Estimates` |
| 6 | `06 — QA Spec` |
| 7 | `07 — Experimentation Plan` |
| 8 | `08 — Critical Launch Checklist` |
| 9 | `09 — GTM Plan` |
| 10 | `10 — Notes` |

In both cases, only create entries for the tabs the user asked for this invocation. If the user re-runs `/product-doc` later for additional tabs, append the new files/tabs alongside the existing ones — don't regenerate what's already there unless explicitly asked.

## Formatting Rules

Apply these across every tab when populating content. The goal is a doc leaders can skim in 60 seconds.

- **Titles:** noun phrases, max ~6 words. No full sentences.
- **Bullets over paragraphs.** Every bullet should be scannable in under 5 seconds.
- **Bold sparingly** — only for the leading term or a key metric inside a bullet.
- **Tables for structured data** (estimates, test cases, channels, sign-offs). Not for prose.
- **Italic for example/placeholder text.**
- **Numbers over adjectives** — "15–25% lift" beats "significant lift."
- **Self-contained tabs** — a reader jumping directly to one tab should understand its context without reading the others.

## Rules

- Write real, substantive content — never leave sections as "TBD" or "add details here."
- Use the user's codebase and CLAUDE.md to fill in technical details accurately.
- Bullet formatting should be clean and scannable. Leaders read these docs fast.
- Every section should be self-contained enough that someone reading just that tab can understand the context.
- When uncertain about product decisions, ask the user rather than guessing.
- Use data and metrics where available. PMs think in numbers.
