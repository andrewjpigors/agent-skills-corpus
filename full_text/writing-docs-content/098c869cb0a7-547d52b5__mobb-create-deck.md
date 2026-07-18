---
name: mobb-create-deck
description: Use when creating a presentation deck from a situation or existing project, before writing any slides—interview the user to clarify intent, audience, and scope
---

# Creating Compelling Decks

Creating a deck is a discovery problem, not a writing problem. Without clarity on **who** you're talking to and **why**, you'll generate slides about the wrong thing. Interview first, write once.

## When to Use

**Symptoms:**
- User says "create a deck about X" without full context
- Project exists but you don't know which aspects to highlight
- Ambiguity about audience, goal, or tone
- Risk of generic, unfocused slides

**Don't use if:**
- User explicitly says "just make assumptions and get started"
- Deck structure and content are already fully specified
- This is refinement of an existing draft (use feedback loop instead)

## Demo Mode

When the user invokes this skill with the argument **"demo"**, run this flow instead of the standard opening:

### Step 1 — Present the demo brief

Tell the user:

> I have a pre-written deck brief you can use to see the full skill in action. Here it is:
>
> ---
> **Deck:** Why OpenShift Is an Application Platform — and Why That Makes It Superior to Vanilla Kubernetes
>
> **For:** A 30-minute technical talk aimed at platform engineers and architects who are evaluating whether to adopt vanilla Kubernetes (EKS, AKS, GKE, or self-managed kubeadm) or OpenShift. They know Kubernetes. They've run it in production. They are skeptical of vendor marketing. The goal is to show them — with specifics, not adjectives — that Kubernetes is an engine and OpenShift is a car: teams that choose vanilla Kubernetes spend 30–50% of their platform engineering time building things OpenShift ships on day one, and they never fully catch up.
>
> **Audience:** Platform engineers, architects, and technical leads at mid-to-large enterprises. Deep Kubernetes knowledge. Budget authority or strong influence over it. Care about: developer velocity, security posture, operational burden, and total cost of ownership. Will push back immediately on any claim that sounds like marketing.
>
> **Thesis:** Kubernetes solves container orchestration. OpenShift solves application delivery. These are different problems, and conflating them is the root cause of most "vanilla Kubernetes is fine" decisions that come back painful two years later.
>
> **Five key messages:**
> 1. Developer experience out of the box — Source-to-Image, Developer Hub, Tekton Pipelines, and ArgoCD ship integrated, not assembled from community tutorials
> 2. Security by default — Security Context Constraints, hardened defaults, image signing with Sigstore, FIPS compliance, and NetworkPolicy enforcement from day one; not a post-hoc audit item
> 3. Operational completeness — Cluster Logging, user workload monitoring (Prometheus stack), OLM for operator lifecycle, and `must-gather` for support — integrated and supported, not duct-taped together
> 4. Enterprise lifecycle guarantees — RHEL CoreOS base, Extended Update Support channels, CVE SLAs, and 24/7 Red Hat support; not a community Slack at 2am
> 5. Platform portability without re-platforming — the same platform runs on AWS (ROSA), Azure (ARO), GCP, on-prem bare metal, and fully disconnected environments; your runbooks transfer
>
> **Feel:** Confidence that OpenShift is leverage, not lock-in. Relief that the hard problems — security, observability, developer onboarding — are solved decisions, not deferred ones.
>
> **Do:** Start a 60-day ROSA trial or request an OpenShift proof-of-concept cluster from your Red Hat account team.
>
> **Tone:** Data-driven and direct. Skeptical engineers, not executives. Show the math. Name the specific Kubernetes gap each OpenShift feature closes. No adjectives without evidence.
>
> **Length:** 30 minutes. SCR narrative (the situation and complication are immediately relatable to the audience; no need for an extended SCQA research phase).
>
> ---

### Step 2 — Give the user a choice

Ask:

> You can use this brief as-is, customise it, or describe your own deck topic instead.
> Which would you like?
> - **A** — Use this brief (I'll confirm each section and move straight to the remaining interview questions)
> - **B** — Customise it (tell me what to change)
> - **C** — Write my own (start the standard interview from question 1)

### Step 3 — Proceed

- **A or B:** Accept or apply edits. Pre-populate DECK_DESIGN.md with the brief answers (questions 1–7 are effectively answered). Then ask questions 8–10 one at a time as normal — reference material, tone confirmation, and diagram approach. After all 10 are answered, show the complete design doc and ask for approval before writing slides. Output the deck to `decks/demo/`.
- **C:** Run the standard interview from question 1. Output the deck to `decks/demo/`.

## Before the Interview: Template Setup

**Special case: If you're inside the mobb-deck-template repo itself**
- ✅ Template is at `./template/`
- Decks will be created in `./decks/[deck-name]/`
- Proceed directly to the interview

**Normal case: If you're in a different project**
- Check if you have `mobb-deck-template` available locally
- If template exists, confirm location with user
- If template doesn't exist, ask user which setup option they prefer (project-local or central)
- Once template location is confirmed, proceed to interview

## Every Deck: Mandatory First Slide

The very first slide of every deck must be an AI disclaimer. It goes before the title slide — slide 1, always.

**Why:** These decks are AI-assisted. The audience deserves to know the visuals may be polished but the content may have inaccuracies.

Use this pattern (centered via flex wrapper — Slidev does not support per-slide `layout:` frontmatter on slide 1):

```markdown
---
theme: red-hat-deck
title: "Your Presentation Title"
info: |
  Short description.
  Author · Role · Year
highlighter: shiki
lineNumbers: false
fonts:
  sans: Red Hat Text
  serif: Red Hat Display
  mono: JetBrains Mono
addons:
  - slidev-addon-red-hat-components
---

<div class="h-full flex flex-col items-center justify-center text-center">

# A Note on This Presentation

<div class="mt-6 max-w-2xl mx-auto text-[var(--rh-muted)] leading-relaxed">

This presentation was created with the assistance of AI. While the visuals are polished and the structure is sound, the content may contain inaccuracies. Please verify any technical claims, pricing figures, or roadmap dates before relying on them.

</div>

<div class="mt-8 text-xs text-[var(--rh-muted)] italic">

AI-assisted · verify before you trust

</div>

</div>

---

# Your Title Slide Here
```

**Technical note:** Do NOT use `layout: center` for slide 1. Slidev parses any content between the global frontmatter closing `---` and the first slide separator `---` as slide 1 content — there is no way to attach per-slide frontmatter to it. Use the flex wrapper instead.

## After Design Doc Approval: Deck Setup

Create a minimal deck directory that depends on the theme and addon packages.

### Option A: Inside mobb-deck-template repo (local development)

```bash
mkdir -p decks/[deck-name]/public
cd decks/[deck-name]
```

Create `package.json`:
```json
{
  "name": "[deck-name]-deck",
  "version": "1.0.0",
  "description": "Your deck description",
  "private": true,
  "scripts": {
    "dev": "slidev slides.md --open",
    "build": "slidev build slides.md",
    "export": "slidev export slides.md"
  },
  "dependencies": {
    "@slidev/cli": "^0.49.0",
    "slidev-theme-red-hat-deck": "file:../../theme",
    "slidev-addon-red-hat-components": "file:../../addon"
  }
}
```

Then:
```bash
npm install
```

### Option B: External project (not in mobb-deck-template)

Create `package.json` in your project:
```json
{
  "name": "[deck-name]-deck",
  "version": "1.0.0",
  "description": "Your deck description",
  "private": true,
  "scripts": {
    "dev": "slidev slides.md --open",
    "build": "slidev build slides.md",
    "export": "slidev export slides.md"
  },
  "dependencies": {
    "@slidev/cli": "^0.49.0",
    "slidev-theme-red-hat-deck": "github:paulczar/mobb-deck-template/theme",
    "slidev-addon-red-hat-components": "github:paulczar/mobb-deck-template/addon"
  }
}
```

Then:
```bash
npm install
```

**Why this approach (Slidev theme + addon):**
- **Theme** (`slidev-theme-red-hat-deck`) — Provides all Red Hat styling, typography, and CSS variables globally
- **Addon** (`slidev-addon-red-hat-components`) — Provides reusable Vue components (RhTwoColumn, RhTable, RhTimeline, RhSpectrum)
- **Your deck** — Only contains `slides.md` (content), `DECK_DESIGN.md` (design doc), and `public/` (images/assets)

**No copying or duplication.** Each deck is lean and references the shared theme/addon. Changes to the theme or addon automatically apply to all decks.

## The Interview Pattern

**Ask questions one at a time.** After each answer, capture it and update DECK_DESIGN.md incrementally. This keeps the conversation conversational and lets you refine as you go.

After all 10 questions are answered and the design doc is complete, ask for approval before writing slides.

### 1. **What is the deck for?**

Understand the actual goal and context.

- Hiring pitch / portfolio showcase / technical deep-dive / conference talk / internal training / sales enablement?
- Is the user seeking a role, or recruiting someone else?
- Are you demonstrating a project, or yourself?

### 2. **Who is the audience?**

Tone and content depend entirely on who's listening.

- Internal team / external conference / hiring committee / customers / potential investors?
- Technical depth (engineers, architects, CISOs, executives)?
- What are their constraints? (budget-conscious, time-pressed, risk-averse, etc.)
- How familiar are they with the domain?

### 3. **Core thesis?** (One sentence.)

This is the single idea they should leave knowing.

- "Paul is a systems architect who can scale cloud infrastructure."
- "This benchmarking framework found a 40% performance gap in common patterns."
- "Here's why Kubernetes-native monitoring matters for on-prem shops."

### 4. **KNOW: What are your 5 key messages?**

What specific takeaways or mental models do you want them to have? **Limit to 5—this is your constraint.** (Fewer for lightning talks, but don't go over 5 or you dilute the message.)

- Example: "Resource limits, health checks, graceful shutdown, security policies, audit tools"
- Example: "Problem statement, root cause, three solution options, recommended approach, next steps"

**Pacing rule:** Each key message gets ~5 slides (title + 3-4 content + transition). Each section takes ~5 minutes.

- 30-min talk: 5 sections × 5 slides × 1 min per slide = ~25 min content + 5 min Q&A
- 10-min lightning: Pick your top 3 messages, compress to 2-3 slides each

### 5. **FEEL: What emotional response do you want to create?**

Beyond information, what should they feel? This drives the story arc.

- Urgency (we need to act now)
- Confidence (this is achievable/we can do this)
- Clarity (finally makes sense)
- Motivation (inspired to change)
- Responsibility (this matters and is my job)
- Other?

### 6. **DO: What should they do after?**

Every deck has a purpose beyond "show up to talk."

- Contact / hire / invest / adopt this tool / fund this research?
- Audit their cluster / change a process / sponsor work?
- Where does the conversation go next?

### 7. **Talk length and structure.**

Deck pacing depends on time.

- Lightning talk (10 min) / standard (30 min) / deep-dive (45+ min)?
- Flow: Problem-solution-results? Narrative arc? Comparison of approaches? Historical context?

**Follow-up question after they answer:**
> "Is your audience skeptical or unfamiliar with the domain, or are they mostly ready to move forward? That helps me know if we should use a simple SCR story (problem → solution → next steps) or a more data-heavy SCQA story (problem → research → justified answer)."

(This locks in the narrative framework before writing the design doc.)

### 8. **What existing material should I read?**

If this is about an existing project, point at the best reference.

- README, ARCHITECTURE.md, KNOWLEDGE.md, GitHub stats, past talks, related artifacts?
- Any particularly rich section that deserves special attention?

### 9. **Tone and visual style.**

Should this feel formal, conversational, data-driven, storytelling?

- Red Hat / corporate / scrappy-startup / academic?
- Heavy visuals or text-minimal?
- Humor / serious / motivational?

### 10. **Diagrams and animations?**

For architectural, flow, or concept diagrams, the default is Vue-based components. Ask only if there's a reason to deviate.

**Default: Vue-based components**
- Custom scoped Vue components in the deck's `components/` directory
- Supports color coding, layout control, and animation
- Best for: architecture comparisons, before/after diagrams, network topology, anything with a clear visual story
- Animation: only add it when the animation itself tells the story (see animation rule below)

**Exception: Mermaid**
- Use only for simple throwaway flows or when the user explicitly asks
- Flowcharts, sequences, state diagrams where interactivity adds no value
- Never use Mermaid inside Vue component slots — it won't render

**The animation rule:** Only animate a diagram when there is a compelling visual story that the motion itself communicates. Ask: "Does the animation reveal something that a static image cannot?" If yes, animate. If no, keep it static.

- ✅ Animate: an attacker packet traveling and being blocked vs. breaching — motion shows the security model working
- ✅ Animate: a pod being evicted and replaced — motion shows the scheduler acting
- ✗ Don't animate: a node count comparison (Classic has 9, HCP has 3) — that's a static fact; animation adds noise, not clarity
- ✗ Don't animate: a cost table — numbers don't benefit from transitions

## Interview → Design Doc → Write Workflow

**Phase 1: Conversational Interview (one question at a time)**

1. Ask question 1, capture answer, update DECK_DESIGN.md with that section
2. Ask question 2, capture answer, update relevant section
3. Continue through all 10 questions, building the design doc incrementally
4. After each answer, show the updated design doc excerpt so user can approve/refine
5. Once all 10 questions are answered and design doc is complete, ask for final approval

**Design doc template to build incrementally:**

```markdown
# Deck Design Doc: [Title]

## Core Thesis
One sentence. What's the big idea?

## Know — Feel — Do Framework

### Know: 5 Key Messages (Use the 5-5-5 Rule)
| Message | ~Slides | ~Minutes |
|---------|---------|----------|
| 1. [Topic] | 5 | 5 |
| 2. [Topic] | 5 | 5 |
| 3. [Topic] | 5 | 5 |
| 4. [Topic] | 5 | 5 |
| 5. [Topic] | 5 | 5 |
| **Total** | **~25** | **~25** |

(Adjust: 10-min lightning = 3 messages × 2-3 slides each; 45+ min = up to 8 messages but start with 5)

### Feel
What emotional response do you want to create for each section? (motivation, urgency, confidence, clarity, etc.)

### Do
What action should they take after? (specific, measurable)

## Audience Profile
- Who: [role/title/discipline]
- Technical depth: [beginner/intermediate/expert]
- Existing knowledge: [what they know already]
- Constraints: [what they care about: budget, time, risk, etc.]

## Talk Structure
- Length: [10 min / 30 min / 45+ min]
- Flow: [problem → solution → results / narrative arc / comparison / other]
- **Narrative framework:** [SCR or SCQA and why]
- Sections: [list 3-6 main sections with 1 sentence each]

## Pyramid Principle: Hierarchical Organization

- **Apex (main idea):** [What's the single conclusion/answer?]
- **Tier 2 (arguments):** [3–5 supporting points that prove the apex]
  - Argument 1: [statement]
  - Argument 2: [statement]
  - Argument 3: [statement]
  - etc.
- **Tier 3 (evidence):** [Data/examples that support each argument — organized below each one]

## Narrative Arc / Storyboard: [SCR or SCQA] + Dot-Dash + Pyramid

**Step 1: Choose your narrative framework**

### SCR (Situation-Complication-Resolution) — For clear, decisive messages
Use SCR when your story is **straightforward and the audience is ready to act**:
- Problem is obvious; solution is clear
- Audience has context and doesn't need extensive justification
- Deck is 10–30 minutes and moves quickly
- Examples: "Classic ops burden → HCP solves it → here's the ROI"

**SCR Framework:**
- **Situation:** What is important / the context that matters?
- **Complication:** What is the problem / challenge?
- **Resolution:** Here's what we need to do / the path forward

### SCQA (Situation-Complication-Questions-Answer) — For complex, data-heavy stories
Use SCQA when your story requires **exploration, justification, and skepticism**:
- Audience is skeptical or unfamiliar with your domain
- You need to show research, data, and reasoning before the answer
- Deck is 30+ minutes with deep analysis
- Examples: "Here's the problem, here's what research shows, here's why option X is best"

**SCQA Framework:**
- **Situation:** What is important / the context that matters? (same as SCR)
- **Complication:** What is the problem / challenge? (same as SCR)
- **Questions:** What do we need to understand? What data will clarify? (NEW: gives the audience permission to think skeptically)
- **Answer:** Here's the resolution, backed by the research and logic from "Questions" (stronger than SCR because it's earned)

---

**Step 2: Organize using the Pyramid Principle**

The Pyramid Principle organizes information hierarchically:
- **Apex (top):** Main conclusion or answer (what they should believe/do)
- **Second tier:** 3–5 supporting arguments/insights that prove the apex
- **Third tier and below:** Evidence, data, examples that support each argument

**In practice (for a 30-min talk):**
\`\`\`
Main idea: "HCP migration is justified" (apex)
├── Argument 1: Cost savings (6 fewer instances = $X/mo)
│   └── Data: Instance pricing, cluster baseline, ROI timeline
├── Argument 2: Operational simplification
│   └── Data: Hours saved on control plane management
├── Argument 3: Feature roadmap advantage
│   └── Data: Timeline of Classic sunset vs HCP features
└── Argument 4: Security & compliance improvements
    └── Data: PrivateLink isolation, audit capabilities
\`\`\`

When read top-down, only the tier-2 arguments, the story is complete. Readers can drill down for evidence if they want.

---

**Step 3: Present using Dot-Dash Structure**

Dots and dashes map directly to the Pyramid tiers:
- **Dots** = Top-level insights (slide headlines). When read in sequence, the dots alone should tell the complete story (Pyramid apex + tier-2 arguments in narrative order).
- **Dashes** = Supporting data and evidence (Pyramid tier-3 and below, organized under each dot).

**How the story unfolds, beat by beat:**

\`\`\`
Opening (Slides 1-2) — SITUATION [or SITUATION phase of SCQA]
[Hook: Set the scene. What's important? What's the context?]
↓ [Emotional beat: What should they feel?]

Section 1: [Message 1 — DOT (a tier-2 Pyramid argument)]
[Key insight that addresses the situation]
→ [Supporting dashes: tier-3 data that proves the dot]
↓ [Emotional transition: Relief? Clarity? Confidence?]

Section 2: [Message 2 — DOT (another tier-2 argument)]
[How this builds on Section 1]
→ [Supporting dashes: data that proves the dot]
↓ [Emotional transition: Deepening relief/confidence?]

Section 3: [Message 3 — DOT] — COMPLICATION [or QUESTIONS phase of SCQA]
[Next layer of the story: the problem emerges / the research reveals]
→ [Supporting dashes: evidence of the complication / research findings]
↓ [Emotional transition]

Section 4: [Message 4 — DOT]
[Compound the understanding of the issue]
→ [Supporting dashes: why this matters]
↓ [Emotional transition]

Section 5: [Message 5 — DOT] — RESOLUTION [or ANSWER phase of SCQA]
[Urgency/solution angle, backed by research if SCQA]
→ [Supporting dashes: path forward, action items]
↓ [Emotional beat: Motivation to act?]

Closing (CTA slide)
[What's next? How do they move forward?]
\`\`\`

**The Golden Rule:** Read only the slide headlines (dots) from beginning to end. If the complete story makes sense without the body text, you've nailed it. This is the Pyramid apex + tier-2 arguments in narrative order.

## Key Stories & Examples
- What's the most compelling example or incident to open with?
- Any surprising findings or counterintuitive insights?
- What makes this different from the obvious approach?

## Visual Style
- Tone: [official / conversational / data-driven / storytelling]
- Red Hat branding: [yes/no and how prominent]
- Emphasis: [visuals-heavy / text-minimal / balanced]

## Diagrams & Animations

### Diagram Approach
- Mermaid (simple, fast): [list sections with flowcharts/sequences/architecture]
- Vue animations (stunning, time-intensive): [list sections where visual impact matters]
- Hybrid: [Mermaid for X, Vue for Y]

### Key Diagrams Needed
- Section 1: [type of diagram, concept]
- Section 3: [type of diagram, concept]
- etc.

### Animation Ideas (if using Vue)
- [Describe what animates and why it matters to the message]
- Example: "Information flows left-to-right showing pipeline stages"
- Example: "State machine showing failure scenarios and recovery"

## Success Criteria
- How will you know this deck worked?
- Metric or outcome to measure against
\`\`\`

**Phase 2: Design Doc Review**

6. Show the complete design doc to user
7. Ask: "Does this capture your vision? Any changes before we write slides?"
8. Refine if needed

**Phase 3: Write Slides**

9. **Study reference material:**
   - Read `template/AGENTS.md` for authoring rules, component usage, Mermaid constraints, and the mandatory browser review workflow.
   - Open `template/slides.md` (the pattern library) as a side reference for all slide formats. Use it to decide: "What layout fits this content type best?"
   - Refer to `addon/README.md` to see the API for `RhTwoColumn`, `RhTable`, `RhTimeline`, `RhSpectrum` components.
   - Refer to `theme/README.md` to see available CSS classes (`.cols-2`, `.rh-tag`, etc.) and CSS variables (`--rh-red`, `--rh-surface`, etc.).
   - If building custom Vue animations, study `template/components/PhaseAnimation.vue` as a reference implementation (Pattern B: reactive phase animation).
   - **For Slidev platform questions** (`v-click`, `magic-move`, code block features, export, layout slots, slide hooks, etc.): invoke the `slidev` skill. It is authoritative for Slidev internals; this skill governs Red Hat workflow and branding. If the `slidev` skill is not installed, prompt the user to run `npx skills add slidevjs/slidev` first.

10. **Write slides.md** in `decks/[deck-name]/slides.md`. Start with the frontmatter and AI disclaimer slide shown in the "Every Deck" section above, then write the real content slides. Match each content type to the closest slide format from the pattern library. Use the design doc as your north star.

11. **Verify against thesis.** Every slide should ladderize to the core thesis and support the Know-Feel-Do objectives. Use the Golden Rule: read only the slide headlines (dots) in sequence—the complete story should be clear without body text.

12. **Build and preview:** 
    - Run `npm install` (if not already done)
    - Run `make dev` (or `npm run dev`)
    - Navigate to http://localhost:3030
    - **Mandatory browser review (per AGENTS.md):** For every slide you materially changed, screenshot it in the browser and evaluate:
      - Is anything clipped, overflowing, or overlapping?
      - Does the slide have one clear main idea?
      - Does the red accent, typography, and spacing read well at full-slide scale?
      - If there's a diagram/animation, does it support the spoken story?
    - Fix any layout issues before declaring the deck ready.

## Why a Design Doc First?

The design doc is your constraint system. It prevents three common failures:

1. **Meandering slides** — Without a clear Know-Feel-Do, you write about everything instead of what matters.
2. **Tone-audience mismatch** — Writing the design doc forces you to explicitly choose audience, jargon level, and emotional arc before you start.
3. **Slides without purpose** — A good design doc shows exactly which slides support which objective. Slides that don't ladder to Know-Feel-Do are cut.

**The design doc is not overhead.** It's the fastest way to avoid rework. Spend 15 minutes writing it; saves 1 hour of slide rewriting.

## Common Mistakes

**Skipping the interview:** "I'll just ask one or two clarifying questions and get started." → Results in generic deck that doesn't focus.

**Skipping the design doc:** "I know what I want to say, let me just write slides." → Slides become unfocused, tone drifts, half the slides don't ladder to the thesis. Rework costs more than the design doc would have.

**Weak thesis.** "It's about a cool project" vs. "This project reveals a critical gap in monitoring for on-prem shops." → Second one gives every slide a clear purpose.

**Know-Feel-Do misalignment.** Design doc says "make them feel urgent" but slides are data dumps. → Review the design doc before writing slides.

**Forgetting the call to action.** Deck ends with "questions?" → Should end with what's next (hire, adopt, invest, etc.). This belongs in the design doc's "Do" section.

**Tone mismatch.** Writing a "technical deep-dive" for an audience of executives, or vice versa → Design doc explicitly captures audience; use it to calibrate jargon and detail level.

**Skipping the framework choice:** "I'll just use SCR for everything." → SCR works for simple, decisive stories. But if your audience is skeptical or the data is dense, SCQA gives you room to build the case. Choose consciously based on Question 7's follow-up.

**Pyramid without narrative:** "I have the arguments but no story connecting them." → Arguments alone aren't narrative. The Pyramid shows which info goes where, but SCR/SCQA shows *why*—what's the emotional or logical progression that makes the argument land?

**Dots without dashes (or dashes without dots):** "All my slides are headlines" or "All my slides are data." → Neither alone works. Dots tell the story, dashes prove it. Both matter.

## Quick Reference

| Question | Impact | Feeds into DECK_DESIGN.md |
|----------|--------|----------|
| What is it for? | Determines scope | Context |
| Who is the audience? | Determines tone, jargon level | Audience Profile |
| Core thesis? | Determines which details matter | Core Thesis |
| KNOW: What concepts? | Determines core content | Know section |
| FEEL: What emotion? | Determines story arc | Feel section |
| DO: What action? | Determines closing and framing | Do section |
| Talk length? | Determines section count and pacing | Talk Structure |
| Reference material? | Determines which stories to extract | Key Stories & Examples |
| Tone/style? | Determines visual approach | Visual Style |

## Diagram Approaches

**Default: Vue components (scoped, in `components/`)**
- Write: A self-contained `.vue` file with scoped CSS
- Rendering: full control over layout, color, and optionally animation
- Best for: architecture comparisons, before/after layouts, network topology, anything with a visual story
- Maintenance: more code than Mermaid, but far more expressive

**Exception: Mermaid**
- Write: fenced code block with `mermaid` language tag
- Best for: simple flowcharts, sequences, or state diagrams where a static graph is sufficient
- Never place inside Vue component slots — Mermaid won't render there

**Animation rule (applies to Vue components):**
Only add animation when the motion itself communicates something a static image cannot. The test: "Does watching this move tell the story better than seeing it frozen?" If yes, animate. If no, static is cleaner.

- ✅ Good animation: attacker packet traveling and being blocked — the motion IS the security story
- ✅ Good animation: pod eviction and rescheduling — motion shows the system acting
- ✗ Skip animation: node count comparison — it's a fact, not a story
- ✗ Skip animation: cost tables, architecture labels, bullet reveals

## The 5-5-5 Rule

**5 key messages | 5 slides per message | 5 minutes per section**

This is your pacing engine:

- **5 key messages:** Constraints force focus. You can't say everything, so prioritize ruthlessly.
- **~5 slides per message:** Title slide + 3-4 content slides + transition to next message.
  - Not literal—some sections need 3 slides, others need 7. But 5 is your anchor.
- **~5 minutes per section:** At a natural pace, you spend roughly 1 minute per slide.
  - 30-min talk = 5 sections × 5 slides × 1 min = 25 min content + 5 min Q&A
  - 10-min lightning = 3 sections × 2-3 slides each

**Why it works:**
- Audiences remember ~5 ideas, not 20
- Slides constrained to ~25 forces narrative discipline
- Pacing is predictable and fits standard talk slots

**When to break the rule:**
- Lightning talks: compress to 3 key messages, 2-3 slides each
- Deep dives (45+ min): can go to 7-8 messages, but add visual variety to maintain energy
- Always: if a message needs 7 slides to be clear, use 7. But then cut elsewhere.

## Template Authoring Rules

If using mobb-deck-template, follow these constraints (full rules in template/AGENTS.md):

- **Frontmatter:** Use the template's default (theme, fonts, highlighter)
- **Slide matching:** 15 standard formats cover 95% of content needs
  - Titles, agendas, section headers, comparisons, bullets, code, tables, flowcharts, timelines, images, quotes, spectrums, CTAs
- **Component use:** `<RhTwoColumn>`, `<RhTable>`, `<RhTimeline>`, `<RhSpectrum>` when they fit naturally—don't force them
- **Every slide must have speaker notes** (HTML comment block with `<!-- ... -->`)
- **Mermaid diagrams:** Place in plain Markdown, NOT inside Vue slots
- **Bullets:** 4–5 per slide max; split rather than scroll
- **Build before shipping:** Run `npm install && npm run build` and fix any errors

## Real-World Impact

- **Baseline (no interview):** Generic slides, multiple rewrites because audience/goal wasn't clear.
- **With interview:** Focused deck, thesis-driven slides, ready on first or second pass.

Time saved: One rewrite = 30 min to 1 hour. Interview takes 5–10 minutes.
