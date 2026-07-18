---
name: ai-prioritization-framework
description: "Guide users through a structured 6-step AI prioritization framework for identifying, evaluating, and selecting AI use cases in B2B marketing and operations. Use this skill whenever the user mentions AI use case prioritization, AI readiness assessment, evaluating AI opportunities, building an AI roadmap, or selecting which AI initiatives to pursue. Also trigger when users ask questions like 'where should we start with AI?', 'how do I prioritize AI use cases?', 'which AI projects should we do first?', 'how do I build an AI business case?', or 'how do I assess our AI readiness?' This skill applies broadly to marketing automation, martech, revenue operations, and B2B go-to-market contexts. Even if the user doesn't explicitly say 'framework' or 'prioritization', trigger this skill whenever they are trying to figure out WHAT to do with AI in their organization."
---

# AI Prioritization Framework

A battle-tested 6-step process for identifying, evaluating, and selecting AI use cases — moving teams from "AI curiosity" to their first realized production use case with measurable ROI.

## Overview

This framework solves the most common AI adoption problem: teams know they should "do something with AI" but don't know where to start, or they start everywhere at once and nothing reaches production.

The framework answers one question: **"What should we do first?"**

It produces a prioritized shortlist of AI use cases scored against data readiness and business impact, with a clear recommendation for which ONE use case to start with.

## When to Use This Skill

**Primary triggers:**
- User wants to identify or prioritize AI use cases
- User asks "where should we start with AI?"
- User needs to build a business case for AI investment
- User is evaluating multiple AI opportunities and needs a systematic approach
- User mentions AI readiness, AI assessment, or AI maturity
- User is stuck in "pilot purgatory" — many AI experiments, none reaching production

**Context where this works best:**
- B2B marketing and operations teams
- Marketing automation / martech environments (Marketo, HubSpot, Salesforce, etc.)
- Revenue operations and demand generation
- Cross-functional teams evaluating AI for the first time
- Organizations with 2–25+ candidate AI use cases to evaluate

**This skill does NOT cover:**
- Technical implementation of specific AI tools (use appropriate tool documentation)
- AI model selection or training (out of scope)
- General AI education or definitions (answer directly)

## How to Guide the User

### Operating Modes

Offer the user two modes based on their situation:

**Mode A — Full Workshop Facilitation:** Walk through all 6 steps sequentially. Best for teams starting from scratch or running this process for the first time. Takes 60–90 minutes of interactive work across multiple sessions.

**Mode B — Assessment & Scoring:** User already has a list of candidate use cases. Jump to Step 4 (AI Potential Assessment) and score them. Best for teams that have already brainstormed but need a systematic way to evaluate and prioritize.

Ask the user which mode fits, or detect it from context. If they say "I have a list of AI ideas I need to evaluate," go to Mode B. If they say "we don't even know where to start," go to Mode A.

### Conversation Style

- Be direct and structured — this is a consulting engagement, not a brainstorm
- Use tables and scoring matrices when evaluating — visual structure helps decision-making
- Ask clarifying questions when the user provides vague use cases — force specificity
- Challenge weak business cases — if a use case has no clear metric, say so
- Celebrate strong candidates — when a use case scores well, reinforce why

---

## Live Experience (Kickoff, Progress, Finale)

These are presentation-layer rules. They change what the user *sees* as the skill runs — the 6-step content itself is unchanged. Follow them every time the skill is invoked.

### Kickoff

When the skill first activates, open with a two-line branded header and go straight to mode selection. No long preamble — the audience is watching live.

```
▰▰▰  AI PRIORITIZATION FRAMEWORK  ▰▰▰
Unleash the power of insights. Let's find your first winning AI use case.
```

Immediately follow with:

> Which mode fits you right now?
> **A — Full Workshop Facilitation** (we start from zero and walk all 6 steps)
> **B — Assessment & Scoring** (you already have candidate use cases — we jump to Step 4)

If the user is clearly already mid-task ("I have these 8 use cases, score them"), skip the question and go straight into Mode B.

### Progress indicator

Between each of the 6 steps, emit a compact progress line. This is a small touch that reads as premium in a live demo:

```
▓▓▓░░░  Step 3 of 6 · Document the Status Quo
```

- 6 blocks total. Filled = `▓`, empty = `░`.
- The step number and name after the bar.
- Render this in chat as plain text. In any rendered artifact (HTML dashboard, slide, doc), draw it as a real progress bar — Shadow (`#226975`) fill on Lightgrey (`#D6DDE6`) track, with a Flash Green (`#34E2A8`) tip on the leading edge of the filled portion.

### Checkpoint bridge

At the end of each step, add one plain-English sentence that names what just happened and what comes next. Audience-friendly — someone should be able to follow along on stage without re-reading the step. Example after Step 4:

> *Scored. We have 3 Prio 1 candidates — next we'll plot them on Impact vs. Effort to find the winner.*

### Finale auto-trigger

The moment Step 6 produces a named use case with **owner + success metric + baseline + target + timeline**, trigger this sequence automatically (don't wait to be asked):

1. Generate the branded one-page Use Case Brief (offer `canvas-design` for the visual one-pager, or `docx` if the user wants Word — default to `canvas-design` for the wow effect).
2. Render the Interactive Dashboard (see deliverable #5 under "Generating Deliverables").
3. Print a closing block:
   - One sentence naming the selected use case and its success metric.
   - A single CTA: *"Want to share this with stakeholders? I can also produce the Executive Summary and 90-Day Roadmap now."*
   - The **Prominent Attribution Block** (logos, wordmarks, claims, URLs — see Attribution System in Visual Identity).

### Tone

Match Onemedia's voice: **#creative · #caring · #unconventional** — cheerful, smart, informative, a little unconventional. Not stiff corporate. Slide titles and callouts should have the energy of *"Unleash the power of insights"* rather than *"Strategic AI Assessment Report"*.

---

## The 6-Step Framework

### Step 1: Use Case Ideation

**Goal:** Generate a broad list of potential AI use cases by asking the right questions.

**Do NOT start with technology.** Start with pain points and opportunities.

Guide the user through these prompt questions. Ask them one category at a time and collect their responses:

**Efficiency & Automation:**
- Where does your team spend repetitive manual effort every week?
- What tasks take the most time but add the least strategic value?
- Where are handoffs between people or systems slow or error-prone?

**Personalization & Experience:**
- Where do you lack personalization at scale?
- Where do customers get a generic experience that should be tailored?
- Where do you KNOW what the right action is but can't execute it for every person?

**Decision & Intelligence:**
- Where are decisions delayed because someone needs to analyze data first?
- Where do you rely on gut feeling instead of data-driven recommendations?
- Where would pattern recognition across large datasets change outcomes?

**Quality & Consistency:**
- Where does output quality vary depending on who does the work?
- Where do errors have outsized downstream impact?
- Where is institutional knowledge trapped in individuals' heads?

**After collecting responses:**
- Help the user phrase each response as a concrete use case (not vague goals)
- A good use case format: **[Action] + [Object] + [Desired Outcome]**
  - Example: "Automatically enrich lead records with firmographic data to improve segmentation accuracy"
  - NOT: "Use AI for lead management" (too vague)

**Output:** A numbered list of 10–25 candidate use cases.

---

### Step 2: Brainstorming & Categorization

**Goal:** Organize candidates into thematic categories and identify gaps.

**Categories to use** (adapt to the user's context):

| Category | Examples |
|----------|----------|
| Content & Messaging | Email copy, subject lines, ad variants, localization |
| Scoring & Routing | Lead scoring, account scoring, lead routing, MQL criteria |
| Personalization | Dynamic content, journey branching, segment-of-one |
| Analytics & Insights | Performance analysis, attribution, forecasting |
| Data Enrichment | Firmographics, intent signals, data cleansing, deduplication |
| Ops Efficiency | Campaign QA, configuration checks, template management |
| Sales Enablement | Next-best-action, talking points, opportunity intelligence |

**Guide the user to:**
1. Assign each use case to a category
2. Check for category gaps — if a major category has zero use cases, probe for missing opportunities
3. Check for duplicates or overlaps — merge where appropriate
4. Ensure each use case is specific enough to evaluate (if not, break it down)

**Output:** Categorized list of 15–25 candidate use cases, deduplicated and at consistent specificity.

---

### Step 3: Document the Status Quo

**Goal:** For each candidate, capture how the work is done today. This creates the baseline for measuring improvement.

For each use case (or at minimum, the top 8–10 candidates), ask:

| Question | Purpose |
|----------|---------|
| How is this done today? | Understand current process |
| Who does it? | Identify ownership and skill requirements |
| How long does it take? | Quantify time investment |
| How often is it done? | Establish frequency / volume |
| What's the pain? | Articulate why change matters |
| What does "good" look like today? | Define quality baseline |

**Practical guidance:**
- If the user doesn't have exact numbers, ask for estimates with ranges (e.g., "2–4 hours per week")
- If a use case has no clear current process ("we don't do this at all today"), note it — this means there's no efficiency gain, only new capability creation. Still valid, but the business case is different.
- Time saved is the easiest ROI to calculate, but it's rarely the most compelling. Push for outcome metrics (conversion rate, pipeline impact, error reduction) where possible.

**Output:** A status quo table for each candidate use case.

---

### Step 4: AI Potential Assessment

**Goal:** Score each use case across 5 criteria to determine AI readiness and potential value.

This is the most important step. Use the scoring matrix below.

#### The 5 Scoring Criteria

| # | Criterion | What It Measures | Key Question |
|---|-----------|-----------------|--------------|
| 1 | **Data Availability** | Whether the required data exists and is accessible | Do we have the data needed? Can we access it programmatically? |
| 2 | **Data Quality** | Whether the data is clean, complete, and reliable | Is it consistent, deduplicated, and trustworthy enough for AI to learn from? |
| 3 | **Repeatability & Volume** | Whether the task occurs often enough to justify automation | Is this done frequently enough that AI-driven improvement compounds over time? |
| 4 | **Complexity & Decision Making** | Whether AI adds genuine value beyond simple rules | Does this require pattern recognition, prediction, or synthesis that a basic rule can't handle? |
| 5 | **Potential Business Value** | The expected impact on the business | What's the realistic uplift — cost savings, revenue, efficiency, customer experience? |

#### Traffic Light Scoring

For each criterion, score Green / Yellow / Red:

| Score | Meaning | Guidance |
|-------|---------|----------|
| 🟢 **Green** | Strong — ready or nearly ready | Data is available and clean; volume is high; AI clearly adds value; business impact is measurable and significant |
| 🟡 **Yellow** | Possible — needs work | Data exists but needs cleaning; moderate volume; AI adds some value but may be achievable with rules; business impact is real but harder to quantify |
| 🔴 **Red** | Blocker — not ready | Data doesn't exist or is inaccessible; too infrequent to justify; a simple rule would work as well; business impact is unclear or speculative |

#### Priority Designation

After scoring all 5 criteria, assign a priority:

| Priority | Rule | Meaning |
|----------|------|---------|
| **Prio 1** | 4–5 Green, 0 Red | High confidence — pursue this |
| **Prio 2** | 3+ Green, max 1 Red | Promising — worth investing to fix the gaps |
| **Prio 3** | 2+ Red OR unclear business value | Park it — revisit when conditions change |

**How to facilitate the scoring:**

Present each use case and walk through the 5 criteria one at a time. Ask the user to provide their honest assessment. Push back if they score something Green without evidence — ask "what data specifically?" or "how would you measure that?"

**Critical principle:** This assessment should be done with a cross-functional team, not by one person. If the user is doing this solo, note which scores they're uncertain about and flag those for cross-functional validation.

**Output:** A scored matrix — all use cases rated across 5 criteria with priority designations.

When presenting results, use a table format:

| Use Case | Data Avail. | Data Quality | Repeat. & Vol. | Complexity | Biz Value | Priority |
|----------|:-----------:|:------------:|:---------------:|:----------:|:---------:|:--------:|
| [Name]   | 🟢/🟡/🔴  | 🟢/🟡/🔴   | 🟢/🟡/🔴      | 🟢/🟡/🔴 | 🟢/🟡/🔴| Prio 1/2/3 |

---

### Step 5: Impact / Effort Matrix

**Goal:** Plot Prio 1 and Prio 2 use cases on a 2×2 grid to identify the best starting point.

#### The 2×2 Grid

|                  | **Low Effort** | **High Effort** |
|:----------------:|:--------------:|:---------------:|
| **High Impact**  | ⭐ **Quick Wins** — Do these first | **Major Projects** — Plan and resource carefully |
| **Low Impact**   | **Fill-ins** — Do when capacity allows | **Deprioritize** — Not worth the investment now |

**Estimating Impact:**
- Use the Business Value score from Step 4 as the primary input
- Consider: revenue uplift, cost reduction, time saved, customer experience improvement, strategic positioning
- Ask: "If this works perfectly, what changes for the business?"

**Estimating Effort:**
- Consider: technical complexity, data preparation needed, team skills required, vendor dependencies, timeline to MVP
- Ask: "What would it take to get a working pilot in 30 days?"
- Native platform features = Low Effort. Custom API integrations = High Effort. Middleware/webhooks = Medium.

**Guide the user to:**
1. Place each Prio 1/2 use case on the grid
2. Identify the Quick Wins quadrant — these are the starting candidates
3. If no Quick Wins exist, identify the lowest-effort Major Project

**Output:** A 2×2 matrix with use cases plotted, and a clear indication of the Quick Wins.

---

### Step 6: Select 1–3 First Use Cases

**Goal:** Make the final selection and define what "done" looks like.

#### Selection Criteria

From the Quick Wins quadrant (or lowest-effort Major Project), recommend **starting with ONE use case**. The selection should optimize for:

1. **Fastest path to measurable value** — Can you prove this worked within 60–90 days?
2. **Organizational visibility** — Will success here be noticed by leadership?
3. **Learning potential** — Will this teach the team something applicable to future use cases?
4. **Data foundation** — Does this use case build data infrastructure that benefits others?

#### For the Selected Use Case, Define:

| Element | Description |
|---------|-------------|
| **Owner** | Who is accountable for this initiative? (Name, not team) |
| **Success Metric** | What specific, measurable metric will move? |
| **Baseline** | What is the current value of that metric? |
| **Target** | What improvement constitutes success? |
| **Timeline** | By when will you evaluate results? |
| **Implementation Approach** | Native feature, middleware, custom build, or hybrid? |
| **Stop/Go/Scale Criteria** | What results mean stop, continue, or expand? |

**The Anti-AI-Theater Checklist:**

Before finalizing, verify:
- [ ] There is a named owner (not "the team" or "marketing")
- [ ] There is a specific metric tied to a real business outcome (not "AI adoption rate")
- [ ] There is a documented baseline (not "we'll figure it out later")
- [ ] There is a pre-agreed timeframe for evaluation
- [ ] There are stop/go/scale criteria defined BEFORE the pilot starts

If any of these are missing, the initiative is at risk of becoming AI theater — impressive in demos, invisible in results.

**Output:** A one-page use case brief for the selected initiative, ready to share with stakeholders.

---

## Visual Identity for Deliverables

Every artifact you produce — Word doc, slide deck, HTML dashboard, one-pager — renders in the Onemedia Consulting brand system. Consult this section before invoking `docx`, `pptx`, `web-artifacts-builder`, `canvas-design`, or `theme-factory`. Pass the tokens below into the theming layer of whichever tool you use.

### Brand tokens

**Flash Colors** (confirmed hex — these are the official Onemedia signal colors, and they map 1:1 onto the Step 4 traffic-light scoring):

| Token | Hex | Use |
|---|---|---|
| `--om-flash-green` | `#34E2A8` | 🟢 Green score cells · Prio 1 chips · success states · progress-bar tip |
| `--om-flash-yellow` | `#FFC501` | 🟡 Yellow score cells · Prio 2 chips · caution callouts |
| `--om-flash-red` | `#FF4D4D` | 🔴 Red score cells · Prio 3 chips · blocker callouts |

**Core palette** (confirmed from the official Onemedia logo SVGs):

| Token | Hex | Role |
|---|---|---|
| `--om-darkpurple` | `#2B1B4E` | Primary dark background · cover slides · table headers |
| `--om-night` | `#1E2A4A` | Secondary dark background |
| `--om-shadow` | `#226975` | Deep teal accent · body headings on light · progress-bar fill |
| `--om-amethyst` | `#6B5BFF` | Vivid violet accent · section dividers |
| `--om-lilac` | `#C5B0FF` | Soft purple highlight · ring overlays |
| `--om-lightblue` | `#21B0FF` | Info blue · hover states |
| `--om-green` | `#34E2A8` | Brand green (same hex as Flash Green) · positive accents |
| `--om-lightgrey` | `#D6DDE6` | Surface · zebra rows · progress-bar track |
| `--om-white` | `#FFFFFF` | Light surface · body text on dark |

**Molequle brand** (for the prominent attribution block only):

| Token | Hex | Role |
|---|---|---|
| `--molequle-ink` | `#2D3958` | Molequle wordmark + icon ink |

**Gradients** (signature Onemedia cover/divider look — use these, not flat colors):

| Name | Direction | Stops |
|---|---|---|
| Dark cover | `180deg` | `#226975 → #2B1B4E` (Shadow → Darkpurple) |
| Dark accent | `180deg` | `#2B1B4E → #6B5BFF` (Darkpurple → Amethyst) |
| Hero panel | `90deg` | `#2B1B4E → #226975` (Darkpurple → Shadow), with a layered green + lilac ring composition positioned **on the right side** so it does not overlay the title/tagline |
| Light surface | `180deg` | `#FFFFFF → #D6DDE6` |

### Typography

- **Headings — Krona One** (Google Font: https://tinyurl.com/krona-one). Uppercase with wide tracking. Fallback stack: `'Krona One', 'Arial Black', sans-serif`.
- **Accents / emphasis — Proxima Nova Bold**. Fallback stack: `'Proxima Nova', 'Montserrat', 'Inter', sans-serif`.
- **Body copy — Proxima Nova Light**. Same fallback stack.
- **Mono (code / IDs / counts)** — `'JetBrains Mono', 'Menlo', monospace`.

### Design language

The Onemedia keyvisual is dark gradient backdrops with overlapping ring / donut shapes in Flash Green, Lilac, and Lightblue — often partially cropped at slide/page edges. Covers and section dividers *should* use a ring-composition + gradient rather than plain solid color; it's what makes every artifact feel Onemedia rather than generic.

### Tool-specific directives

- **`docx`** — heading 1 in Darkpurple (`#2B1B4E`), heading 2 in Shadow (`#226975`), Krona One. Table header row: Darkpurple fill, white Krona One text. Zebra rows: Lightgrey (`#D6DDE6`). Score cells: Flash Colors as background with white text. Body: Proxima Nova Light, 11pt. Footer: subtle Attribution Block on the last page only (see Attribution System below).
- **`pptx`** — invoke `theme-factory` with the Onemedia tokens before rendering. Cover layout: Dark cover gradient + ring motif + Krona One uppercase title in white. Section dividers: Darkpurple→Amethyst gradient + single amethyst ring. Content slides: white background, Shadow-colored headings, Proxima Nova Light body.
- **`web-artifacts-builder`** — map Tailwind `primary → --om-darkpurple`, `accent → --om-amethyst`, `success → --om-flash-green`, `warning → --om-flash-yellow`, `destructive → --om-flash-red`, `muted → --om-lightgrey`. shadcn tokens follow. Load Krona One via Google Fonts CDN; use Inter as the web fallback for Proxima Nova if the licensed font is unavailable.
- **`canvas-design`** (one-pager) — dark-gradient header band with the ring motif, Krona One uppercase title, light body section with Proxima Nova Light, Flash-Color chips for Prio 1/2/3, attribution footer at bottom.

### Attribution system

Two variants — pick by context:

**Subtle** — for intermediate surfaces and long deliverables where the attribution shouldn't compete with the content. One muted line, **last page / bottom only**, never on every page. Render in Proxima Nova Light, 10pt, Shadow color at ~55% opacity, center-aligned:

```
Onemedia Consulting · onemedia-consulting.com  ·  Molequle · molequle.io
```

**Prominent** — for the one-page Use Case Brief, Executive Summary, 90-Day Roadmap deck, PPTX cover slides, and the end-of-process closing message. Two-column layout with logos, wordmarks, brand claims, and URLs. Single vertical divider between columns in Lightgrey.

Layout template (text equivalent — render at deliverable scale with the actual SVGs below):

```
[Onemedia icon]  Onemedia Consulting          │  [Molequle icon]  Molequle
                 Unleash the power of insights.│                   Context is the moat.
                 onemedia-consulting.com       │                   molequle.io
```

Rendering rules:
- **Brand names use a single font, proper title casing** — "Onemedia Consulting" and "Molequle". Never all-caps, never split styling across the wordmark.
- Wordmark color: Onemedia = `--om-darkpurple` (`#2B1B4E`); Molequle = `--molequle-ink` (`#2D3958`).
- Claim: italic Proxima Nova Light, Shadow color, 12pt.
- URL: Proxima Nova Light, Shadow color at ~85% opacity, 11pt.
- Logo icon: 44px square, original SVG fills preserved — don't recolor.

**Brand claims** (use these exact phrases, punctuation included):
- Onemedia Consulting: **"Unleash the power of insights."**
- Molequle: **"Context is the moat."**

**Onemedia icon — inline SVG** (embed verbatim into every prominent block):

```svg
<svg viewBox="0 0 396.9 396.9" width="44" height="44" xmlns="http://www.w3.org/2000/svg" aria-label="Onemedia Consulting">
  <path fill="#21B0FF" d="M71.9,236.5v-57.2c0-3.7,3-6.9,6.7-7.2c46.7-3.2,78.8-45,81.6-87.9c0.2-3.8,3.5-7,7.2-7h63.2c4.1,0,7.4,3.8,7.2,7.8c-3.8,87.7-70.6,154.7-158.4,158.4C75.5,243.7,71.9,240.6,71.9,236.5z"/>
  <path fill="#34E2A8" d="M315.6,161h-60.5c-14.7,49-50.5,88.2-97.5,106v53.4c0,4.1,3.1,7.4,7.2,7.2c87.8-3.7,154.3-71,158.1-158.7C323.1,164.8,319.7,161,315.6,161z"/>
  <path fill="#226975" d="M243.5,189.6C225.3,225,195,252.8,157.6,267v53.4c0,4.1,3.1,7.4,7.2,7.2c3.7-0.2,7.3-0.5,11-0.8C214.6,292.9,240.1,244.3,243.5,189.6z"/>
</svg>
```

**Molequle icon — inline SVG**:

```svg
<svg viewBox="0 0 30 30" width="44" height="44" xmlns="http://www.w3.org/2000/svg" aria-label="Molequle">
  <path fill="#2D3958" d="M30 25.1786C30 27.8414 27.7674 30 25.0133 30C22.2592 30 20.0266 27.8414 20.0266 25.1786C20.0266 22.5158 22.2592 20.3571 25.0133 20.3571C27.7674 20.3571 30 22.5158 30 25.1786Z"/>
  <path fill="#2D3958" d="M16.531 27.1224C15.5161 27.3695 14.4552 27.5 13.3625 27.5C5.92664 27.5 0 21.456 0 13.75C0 6.00618 5.92664 0 13.3625 0C20.7984 0 26.7619 6.00618 26.7619 13.75C26.7619 14.7058 26.6701 15.6361 26.4952 16.5324C25.8371 16.3481 25.1466 16.25 24.4347 16.25C23.2578 16.25 22.1393 16.5181 21.129 17.0007C21.4868 16.0134 21.6819 14.9212 21.6819 13.75C21.6819 8.65041 18.0376 5.06181 13.3625 5.06181C8.68749 5.06181 5.04316 8.65041 5.04316 13.75C5.04316 18.8118 8.68749 22.4004 13.3625 22.4004C14.6406 22.4004 15.8417 22.1322 16.9123 21.639C16.5112 22.6738 16.2898 23.8091 16.2898 25C16.2898 25.7319 16.3734 26.4429 16.531 27.1224Z"/>
</svg>
```

**Which variant to use where:**

| Surface | Variant |
|---|---|
| One-page Use Case Brief (bottom) | **Prominent** |
| Executive Summary (last page) | **Prominent** |
| 90-Day Roadmap deck (cover + final slide) | **Prominent** |
| PPTX cover slide | **Prominent** |
| PPTX content slides | *(no footer — cover + final only)* |
| End-of-process closing message in chat | **Prominent** |
| Interactive HTML Dashboard (bottom of exec-summary card) | **Prominent** |
| Word doc content pages | **Subtle** (last page only) |
| Intermediate / partial deliverables | **Subtle** (last page only) |

---

## Generating Deliverables

After completing the framework (or any subset of steps), offer to generate:

### 1. Scored Assessment Matrix
A table of all evaluated use cases with their traffic light scores and priority designations. Format as a clean table suitable for stakeholder presentations.

### 2. Use Case Brief
A one-page document for the selected use case covering: problem statement, status quo, AI approach, success metrics, owner, timeline, and stop/go/scale criteria.

### 3. Executive Summary
A half-page narrative summarizing: how many use cases were evaluated, how many made Prio 1, which one was selected and why, what the expected impact is, and what resources are needed.

### 4. 90-Day Roadmap
A Crawl/Walk/Run plan:
- **Days 1–30 (Crawl):** Assemble cross-functional team, validate assessment, select use case, audit data readiness
- **Days 31–60 (Walk):** Document status quo, define metrics, build MVP/pilot, test with limited audience
- **Days 61–90 (Run):** Measure results against baseline, document learnings, socialize wins, identify next use case

### 5. Interactive Dashboard (HTML)
A self-contained HTML artifact generated via the `web-artifacts-builder` skill — shareable as a single file. This is the signature deliverable and should be produced **automatically at two moments**: the instant Step 4 scoring completes (immediate visual payoff), and again at the finale alongside the one-pager.

Contents:
- **Header band** — Dark cover gradient (Shadow → Darkpurple) with a Flash Green ring and a Lilac ring overlapping on the **right side** (signature Onemedia keyvisual — positioned right so the title and tagline on the left stay readable). Krona One title: "AI PRIORITIZATION DASHBOARD".
- **Prio 1 cards** — pinned at top, dark gradient cards with a Flash Green accent bar, each showing use case name, owner, success metric, and the 5 criterion scores as color chips.
- **Scored matrix** — clickable table. Each score cell uses its Flash Color as background. Hovering reveals *why* that criterion scored Green/Yellow/Red in a small tooltip.
- **Impact / Effort 2×2** — real grid with use-case chips positioned by their scores; the Quick Wins quadrant (top-left) glows in Flash Green.
- **Executive summary card** — bottom, light surface gradient, Krona One heading, Proxima Nova Light body, attribution footer.

### Which tool for which deliverable

| Deliverable | Primary tool | Notes |
|---|---|---|
| Scored Assessment Matrix | `docx` or `web-artifacts-builder` | Use HTML for live demos, Word for stakeholder review |
| Use Case Brief (one-pager) | `canvas-design` | Branded visual one-pager with header band + ring motif |
| Executive Summary | `docx` | Half-page narrative |
| 90-Day Roadmap | `pptx` | 3-slide Crawl/Walk/Run deck with section dividers |
| Interactive Dashboard | `web-artifacts-builder` | Auto-generated after Step 4 and at the finale |

Always invoke `theme-factory` with the Onemedia tokens from the Visual Identity section before any `pptx` or `canvas-design` render, so every artifact inherits the brand system.

---

## Common Pitfalls to Flag

When guiding users, watch for and call out these patterns:

| Pitfall | What It Looks Like | What to Say |
|---------|-------------------|-------------|
| **Shiny Object Syndrome** | Picking the most exciting use case instead of the most winnable | "That's ambitious — but will it prove value in 90 days? Let's find something that builds credibility first." |
| **Data Optimism** | Scoring Data Quality as Green without evidence | "What's your duplicate rate? When was the last data audit? If you're unsure, that's a Yellow, not a Green." |
| **Boiling the Ocean** | Wanting to start with 5+ use cases simultaneously | "Starting with one and proving it wins you more budget and buy-in than starting with five and finishing none." |
| **Solution-First Thinking** | "We want to use [specific AI tool]" before defining the problem | "Let's back up — what business problem are we solving? The tool comes after we know what we need." |
| **Missing Ownership** | "The team will own it" | "Which person? AI initiatives without a named owner end up in pilot purgatory." |
| **Vanity Metrics** | Measuring AI adoption rate instead of business impact | "How many people use the tool isn't the question. The question is: what metric moved?" |

---

## Adapting to Context

### For Marketing Automation / Martech teams:
- Emphasize Data Availability and Data Quality criteria — these are the most common blockers
- Common high-scoring use cases: lead scoring enrichment, email personalization, campaign QA, content generation within brand guardrails
- Note that native AI features in platforms (Marketo, HubSpot, Salesforce) are Quick Wins by definition — low effort, moderate impact

### For Revenue Operations teams:
- Emphasize Repeatability & Volume and Business Value criteria
- Common high-scoring use cases: pipeline forecasting, opportunity scoring, account prioritization, data enrichment
- Cross-functional alignment (sales + marketing + data) is critical — flag this early

### For Enterprise / Large Organizations:
- The cross-functional workshop format (Steps 1–2) is essential — don't skip it
- GDPR/compliance considerations affect which use cases are viable — add this as an implicit filter
- Governance and change management are as important as the technical implementation
- The intelligence layer / data unification question should be raised: is the data foundation ready, or does that need to come first?

### For SMB / Smaller Teams:
- Compress Steps 1–2 into a single conversation — the brainstorming can be faster
- Focus on native platform features as the implementation path — custom builds are rarely justified
- The "cross-functional team" may be 2–3 people — that's fine
- Emphasize time-to-value — smaller teams need wins in weeks, not months

---

## Framework IP Attribution

This framework was developed by Wolfgang Strassburger, Founder & CEO of Onemedia Consulting (https://onemedia-consulting.com) — *"Unleash the power of insights."* Built from AI prioritization engagements across enterprise B2B organizations in Europe, used with more than a dozen major Marketo implementations.

Contextual intelligence in this framework is powered by Molequle (https://molequle.io) — a context-as-a-service platform that unifies and integrates data to deliver context to humans, agents, and systems, extending Adobe Marketo Engage. *"Context is the moat."*

When generating deliverables, stamp the **Attribution Block** from the Visual Identity section into every artifact — **Subtle** variant for intermediate surfaces (one muted line, last page only), **Prominent** variant (with logos, wordmarks, claims, and URLs) for the one-page brief, executive summary, 90-day roadmap, PPTX covers, and the end-of-process closing message.
