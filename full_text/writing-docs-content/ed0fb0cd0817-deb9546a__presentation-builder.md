---
name: presentation-builder
description: End-to-end skill for creating professional Lunch & Learn style presentations. Produces a markdown transcript, PPTX slide deck, and DOCX presenter reference with diagrams. Supports iterative refinement, fact-checking via research sub-tasks, and optional cross-agent review for content accuracy. Works with any agent CLI (Claude, Codex, Gemini) as the primary session.
tools-needed: file read/write, shell execution, user interaction, parallel sub-tasks
---

# Presentation Builder Skill

> **Foundation:** This skill inherits the quality framework (Quality Dimensions, weakness-weighted review tiers) from `skills/builders/builder-foundation/SKILL.md`.

## Purpose

Create a complete, polished presentation package from a topic brief. The output is three artifacts:

1. **Markdown transcript** (`<topic>-transcriptv<N>.md`) — speaker script with slide-by-slide notes
2. **PPTX slide deck** (`<topic>-presentationv<N>.pptx`) — visual slides for screen sharing
3. **DOCX presenter reference** (`<topic>-transcriptv<N>.docx`) — formatted reading guide with diagrams

## When To Use

- User asks to create a presentation, Lunch & Learn, talk, or lecture
- User has a topic and audience in mind
- Output should be presentation-ready (not just an outline)

## Prerequisites

```bash
# In the working directory:
npm init -y
npm install pptxgenjs docx
```

Ensure `package.json` has `"type": "commonjs"` (both pptxgenjs and docx use CommonJS).

## Workflow Overview

```
Phase 1: Define → Phase 2: Research & Plan Review (Cross-Agent) → Phase 3: Transcript → Phase 3.5: Prose Cleanup Pass → Phase 4: PPTX → Phase 4.5: Deliverable Review (Cross-Agent) → Phase 5: DOCX → Phase 6: Final Review
```

Each phase produces a versioned artifact. Versions increment on user feedback (v1 → v2 → v3).

**Cross-agent review (opt-in) can cover the entire lifecycle** - both planning (Phase 2) and implementation (Phase 4.5). Recommended for regulatory, financial, medical, or high-accuracy technical topics; ask the user before running it.

---

## Phase 1: Define the Presentation

Collect these parameters before writing anything:

| Parameter | Example | Required |
|-----------|---------|----------|
| Topic | "DeFi Under The Hood" | Yes |
| Audience | "DeFi beginners — assume zero crypto knowledge" | Yes |
| Duration | "30 minutes + 10 min Q&A" | Yes |
| Presenter | "<Your Name>" | Yes |
| Slide count | 24 | Yes |
| Date/event | "February 2026 \| Lunch & Learn" | Yes |
| Tone | Conversational, humorous, analogy-heavy | Yes |
| Key constraints | "No financial advice disclaimer", "Must mention Hedera" | Optional |

### Audience Calibration

The audience level drives everything: language register, analogy density, how much jargon needs defining, and Additional Info depth all calibrate to it.

### Timing Budget

Allocate time per slide based on content density:

| Content Type | Time per Slide |
|--------------|----------------|
| Title / intro | 0:30 |
| Concept introduction | 1:00 - 1:30 |
| Technical deep-dive | 1:30 - 2:00 |
| Comparison / walkthrough | 1:15 - 1:45 |
| Summary / takeaways | 1:00 - 1:15 |
| Q&A / resources | Remaining time |

Total must equal stated duration. Build the timing table before writing any transcript - draft the slide outline as a table: `| Slide | Title | Time | Content Type |`.

---

## Phase 2: Research

### Specialized Critic Roles

Each counterpart agent has a specialized focus area that plays to its strengths. Use **role-specific prompts** instead of generic review prompts.

#### Codex — Fact Verification & References

Codex is the fact-checker. Use it to verify every claim, URL, code snippet, and technical detail.

```
Fact-check the following presentation content. For each claim, provide:
  1. Verification status: VERIFIED / OUTDATED / INCORRECT / UNVERIFIABLE
  2. Source URL confirming or correcting the claim
  3. Date of source data
  4. Any version-specific concerns

Also check:
  - All code snippets for syntax correctness
  - All CLI commands for correct flags and syntax
  - All system contract addresses against current documentation
  - All URLs for liveness (LIVE / DEAD / REDIRECT)
  Flag anything outdated, disputed, or missing a reference.
```

#### Gemini — Humor, Engagement & Visual Design

Gemini is the engagement and visual specialist. Use it for humor, audience interaction, analogies, transitions, and image/diagram prompt refinement.

```
For a [duration] presentation on [topic] aimed at [audience]:
  1. Generate 2-3 jokes/funny lines PER SECTION that match the stated tone
  2. Generate 10+ analogies that explain technical concepts using everyday objects
  3. Generate transition lines between major sections
  4. Identify engagement dead zones (3+ slides without humor or strong hooks)
  6. Refine all Image Prompt fields for better visual output:
     - Better composition and focal points
     - Color harmony with the design system
     - Diagram layout improvements and visual hierarchy
  7. Suggest speaker note improvements for natural delivery cadence
```

Both critics run in parallel with **per-agent timeouts**. Codex gets 480s (8 min) because it does 20-30+ web searches per review and frequently falls back from WebSocket to HTTPS transport. Gemini gets 180s (3 min). If Codex times out, fall back to a general-purpose Claude sub-agent with web search for fact verification.

Codex output feeds into the Fact Bank and code verification. Gemini output feeds into transcript writing, speaker notes, and image generation.

### Cross-Agent Plan Review

For presentations with high accuracy requirements (financial data, regulatory claims, technical specifications), run the cross-agent plan review loop with specialized prompts:

1. Draft the slide outline as a "plan"
2. Run Codex with the fact-verification prompt (above)
3. Run Gemini with the engagement/visual prompt (above)
4. Merge, triage, and iterate (max 3 rounds)

This is opt-in. Ask the user before running it. Cost scales with critic count.

---

## Phase 3: Transcript (Markdown)

### File: `<topic>-transcriptv<N>.md`

Structure for each slide:

```markdown
---

## SLIDE <N> - <Title> (<start> - <end>)

**[On screen: <description of what the audience sees on the slide>]**

<Transcript line 1 — natural speaking style, not read-word-for-word>

<Transcript line 2 — **bold** for emphasis, _(italics)_ for stage directions>

<Transcript line 3>

**[Advance]**

### Additional Info — Slide <N>
- **Term/concept 1**: Deep explanation at implementation level — what it is, how it
  works internally, why it matters. For technical talks: function signatures, API
  endpoints, protocol internals, error codes. For strategic talks: market data with
  sources, competitive details, regulatory specifics. The presenter should be able
  to answer any follow-up question from this section alone. 2-4 sentences per bullet.
- **Term/concept 2**: Same depth. Every concept the slide mentions gets its own
  bullet with enough detail to satisfy the most skeptical audience member.
- **Common question**: "Why does X happen?" — prepared answer with specifics
- **Edge case**: What breaks, what's unsupported, what's surprising
- ...8-15 bullets per content slide, each with genuine depth

### Diagrams (on slides with visual/flow/architecture content)

**<Diagram title>:**

<Multi-paragraph prose description explaining every element of the diagram.
Each box, arrow, and flow should be explained — what it represents, why it's
there, and how it connects to the concepts being discussed. Include anticipated
questions inline: "If someone asks 'why does X route through Y?' — the answer
is..." This section should be 2-5 paragraphs, rich enough that someone who
cannot see the diagram still understands the full picture.>

` ` `mermaid
<Mermaid diagram code — single-line labels only, no \n or <br/>>
` ` `
```

**Note:** Replace `` ` ` ` `` above with actual triple backticks (shown spaced to avoid markdown parsing issues in this skill file).

### Presentation Type Adaptation

Before writing the transcript, check the plan's North Star for the declared **Presentation Type** (Executive / Technical / Community / Educational / Investor Pitch) and adapt the transcript to the matching "When writing the transcript" note in the shared conventions reference. For **Investor Pitch**, also load `skills/presentations/pitch-deck-genre.md` and keep the spoken narrative on the Problem -> Solution -> ... -> Ask thread.

> **Reference:** Presentation Type Profiles (with per-type transcript-adaptation notes) live in `skills/presentations/presentation-conventions.md`. The Investor Pitch genre's per-slide goals, red flags, and credibility checks live in `skills/presentations/pitch-deck-genre.md`.

If no type is declared, default to **Executive** (the most constrained profile - it is easier to add depth than to remove it).

### Transcript Writing Rules

1. **Write how you talk, not how you write.** Short sentences. Sentence fragments are fine. Conversational tone.
2. **One idea per paragraph.** Each `>` block is one thought.
3. **Bold the punchlines.** The key insight in each section should be bold.
4. **Stage directions in italics.** Use sparingly — `_(pause)_`, `_(smile)_` for key moments. Avoid excessive `_(gesture left)_`, `_(point to chart)_` — trust the presenter to know where to gesture.
5. **Analogies anchor every concept.** If you can't explain it with an analogy, simplify further.
6. **Humor is earned.** One or two jokes per slide max. Self-deprecating > punching down.
7. **Transitions are explicit.** Don't just advance — tell the audience where you're going.
8. **"Additional Info" sections are deeply detailed and encyclopedic** - the presenter's lifeline during Q&A: thorough enough to answer any follow-up without external research. Full depth spec (8-15 bullets per content slide, 2-4 sentences each, `**bold prefix**:` headers) lives in the Phase 3 template block and `skills/presentations/presentation-conventions.md`.
9-13. **Content discipline rules** - no redundant explanations across slides, no-repetition (max twice in the transcript), mixed-audience language, executive structure, and follow-the-thread. These five rules are shared with `presentation-planner`; full text in `skills/presentations/presentation-conventions.md`.

### Natural Delivery Rules (Critical)

The transcript should sound like a real human talking to a room, not an AI reading slide content out loud. Follow these rules strictly:

#### Anti-Patterns — NEVER Do These

1. **Never enumerate slide content.** If the slide shows three bullet points, do NOT say "Number one... Number two... Number three..." or "First... Second... Third..." The audience can read. Your job is to add context, stories, and color around what's on screen — not narrate it like a teleprompter.
   - BAD: "Three things make DeFi work. **Permissionless** — no application forms. **Transparent** — every transaction is auditable. **Composable** — protocols plug into each other."
   - GOOD: "What makes it actually work? Well, it's **permissionless** — meaning no application forms, no credit checks. Your wallet is your ID, full stop. It's **transparent** — every line of code is public. Imagine if your bank had to publish every decision it ever made — they'd shut down voluntarily. And it's **composable** — this one's the sleeper. We'll come back to it because it's honestly the most powerful idea in all of DeFi."

2. **Never use uniform paragraph structure across slides.** If every slide follows the same pattern (introduce concept → list items → bold conclusion), the presentation sounds monotonous. Vary the rhythm — some slides lead with a story, some with a question, some with a surprising fact.

3. **Never describe the slide layout as a script.** Avoid "As you can see on the left side of the slide..." or "The flow diagram at the bottom shows..." unless the visual is genuinely confusing. The audience has eyes. Instead, let your words complement what's on screen, not describe it.

4. **Never make every sentence informational.** Real speakers have "breathing room" lines — throwaway comments, personal reactions, rhetorical asides. These are essential for pacing. A presentation that's 100% information is exhausting to listen to.

#### Positive Patterns — ALWAYS Do These

1. **Weave in tidbits from Additional Info.** Pull 1-2 small facts, origin stories, or "did you know" moments from the Additional Info section into the spoken transcript. This adds texture that the slide alone doesn't provide.
   - Example: "Fun fact — this formula was first sketched out by Vitalik Buterin in a Reddit post in 2017. A Reddit post! That's how some of the most important financial infrastructure in the world got started."

2. **Use conversational bridges.** Real people use connective phrases: "Here's the thing...", "What's interesting is...", "So picture this...", "I'll be honest...", "This blew my mind when I first learned it...", "And here's the part that trips people up..."

3. **Add personal reactions.** The presenter should react to their own content as a human would — "When I first learned about this, I spent two hours staring at the screen going 'wait, that can't be right.'" This builds rapport and signals authenticity.

4. **Vary sentence rhythm aggressively.** Mix long flowing explanatory sentences with punchy short ones. A paragraph with five same-length sentences sounds robotic. Interrupt yourself. Use dashes. Drop a one-word sentence for emphasis. Like that.

5. **Let the slide do its job.** If the slide shows a comparison table, don't read both columns. Pick one side and tell a story about it. The audience will read the other column themselves.

6. **Connect ideas across slides.** Reference earlier concepts: "Remember the vending machine from earlier? Same idea here, but now..." This makes the presentation feel like a coherent story instead of 24 disconnected slides.

7. **Include at least one "off-script" moment per 3-4 slides.** A brief aside, a personal anecdote, a "just between us" moment. These are what make a talk feel human rather than rehearsed. They can be planned — the audience won't know.

### Timing Markers

Every slide header includes timing: `(start - end)`. The sum of all slide durations must equal the stated presentation duration. Q&A time is separate and listed on the final slide.

### Versioning

- **v1**: First draft from outline + research
- **v2**: After user feedback (language, coverage, timing adjustments)
- **v3**: After second feedback round (simplified language, more analogies, fact corrections)

**Only keep the latest version.** Delete previous versions when a new one is created (e.g., delete transcriptv1.md when transcriptv2.md is written).

---

## Phase 3.5: Prose Cleanup Pass (Mandatory)

After completing the transcript draft, run it through your prose-cleanup pass (remove AI-writing tells and tighten clarity). This is a mandatory step, not optional.

### What the Prose-Cleanup Pass Does

Applies 24 pattern-detection rules to remove AI writing tells:
- Significance inflation ("serves as", "testament to", "pivotal moment")
- Copula avoidance ("serves as" -> "is")
- Promotional language ("groundbreaking", "vibrant", "showcasing")
- Rule-of-three forcing
- Em-dash overuse
- Filler phrases ("In order to", "It is important to note that")
- Generic positive conclusions
- Uniform paragraph structure

### Process

1. Re-read the full transcript after completing the draft
2. Apply the prose-cleanup patterns systematically
3. Apply the 7 spoken/transcript rules (vary structure, mix paragraph lengths, add off-script moments, avoid spoken enumeration)
4. Run the anti-AI audit: "What makes this obviously AI generated?" - list remaining tells
5. Fix remaining tells
6. Update the transcript file in place

### When to Skip

Never. The prose-cleanup pass is always applied to transcripts. The only content exempted is structured data: tables, Mermaid diagrams, Fact Bank entries, and appendix reference material.

---

## Phase 3.7: Shared Transcript Parser (Drift Prevention)

### File: `workspace/<project>/transcript-parser.js`

The PPTX speaker notes (Phase 4) and the DOCX presenter reference (Phase 5) BOTH need the same slide-by-slide spoken content from the transcript. Hardcoding speaker-note strings inside `generate-pptx.js` creates a drift mode: every transcript edit (Phase 3.5 prose-cleanup polish, Phase 4.5 cross-agent fixes, last-minute corrections) updates the DOCX at next regenerate but leaves PPTX speaker notes pointing at stale text. The presenter ends up showing a deck whose notes contradict the printed reference.

**Fix:** both generators import a small shared parser that reads `transcript-v<N>.md` at generation time. One source of truth, zero manual sync. The parser is dependency-free (just `fs`) and lives next to the two generators in the project workspace.

### Parser Template

Write `workspace/<project>/transcript-parser.js` once per project. The template below is the verbatim reference shipped with the H3 context-engineering talk (`workspace/context-engineering-talk/transcript-parser.js`):

```javascript
// Shared transcript parser for presenter bundles.
// Consumed by generate-pptx.js (speaker notes) and generate-docx.js (presenter reference).
// One source of truth (transcript-v<N>.md) eliminates the manual-sync drift mode
// where hardcoded speaker notes diverge from the transcript as the talk gets edited.
//
// Exports parseTranscript(transcriptPath, opts?) -> { slides, qaItems }.
//   slides[i] = { num, title, timing, onScreen, spokenParas, infoBullets, diagrams }
//   qaItems[i] = { question, answer }
//
// opts.stripStageDirections (default false): when true, removes _(pause)_-style
// italic stage directions entirely. PPTX speaker notes use true (clean prose for
// presenter view); DOCX presenter reference uses false (preserves cues in print).

const fs = require("fs");

function clean(text, opts = {}) {
  const stripStage = !!opts.stripStageDirections;
  let out = text
    .replace(/\*\*\[On screen: ([\s\S]+?)\]\*\*/g, "")
    .replace(/\*\*\[Advance\]\*\*/g, "")
    .replace(/\*\*\[Advance to Q&A\]\*\*/g, "")
    .replace(/\*\*(.+?)\*\*/g, "$1")
    .replace(/(?<!\*)\*([^*\n]+?)\*(?!\*)/g, "$1");

  if (stripStage) {
    out = out
      .replace(/\s*_\([^)]+\)_\s*/g, " ")
      .replace(/[ \t]+/g, " ");
  } else {
    out = out.replace(/_(\([^)]+\))_/g, "$1");
  }

  out = out
    .replace(/_(\w[^_\n]*?)_/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .trim();

  return out;
}

function parseTranscript(transcriptPath, opts = {}) {
  const transcript = fs.readFileSync(transcriptPath, "utf-8");
  const slideRegex = /^## SLIDE (\d+) - (.+?) \(([^)]+)\)\s*$/m;
  const sections = transcript.split(/^---\s*$/m);

  const slides = [];
  sections.forEach(section => {
    const headerMatch = section.match(slideRegex);
    if (!headerMatch) return;
    const [, num, title, timing] = headerMatch;

    const onScreenMatch = section.match(/\*\*\[On screen:\s*([\s\S]+?)\]\*\*/);
    const onScreen = onScreenMatch ? onScreenMatch[1].trim().replace(/\s+/g, " ") : "";

    const spokenMatch = section.match(/\*\*\[On screen:[\s\S]+?\]\*\*\s*([\s\S]*?)\s*\*\*\[Advance/);
    const spokenRaw = spokenMatch ? spokenMatch[1] : "";
    const spokenParas = spokenRaw
      .split(/\n\n+/)
      .map(p => clean(p, opts))
      .filter(p => p.length > 0 && !p.startsWith("###"));

    const infoMatch = section.match(/### Additional Info - Slide \d+\s*\n([\s\S]+?)(?=\n---|\n## |\n### |$)/);
    let infoBullets = [];
    if (infoMatch) {
      infoBullets = infoMatch[1]
        .split(/\n- /)
        .map(line => line.replace(/^- /, "").trim())
        .filter(line => line.length > 0)
        .map(line => clean(line, opts));
    }

    const diagMatch = section.match(/### Diagrams - Slide \d+\s*\n([\s\S]+?)(?=\n### Additional Info|\n---|\n## |$)/);
    const diagrams = diagMatch ? diagMatch[1].trim() : null;

    slides.push({
      num: parseInt(num, 10),
      title, timing, onScreen, spokenParas, infoBullets, diagrams,
    });
  });

  slides.sort((a, b) => a.num - b.num);

  const qaMatch = transcript.match(/## Anticipated Q&A \(Presenter Prep\)\s*\n([\s\S]+?)(?=\n## |$)/);
  const qaText = qaMatch ? qaMatch[1] : "";
  const qaItems = [];
  if (qaText) {
    const qBlocks = qaText.split(/\n### Q: /).slice(1);
    qBlocks.forEach(block => {
      const lines = block.split("\n");
      const question = lines[0].replace(/^"|"$/g, "").trim();
      const answer = lines.slice(1).join("\n").trim();
      qaItems.push({ question, answer: clean(answer, opts) });
    });
  }

  return { slides, qaItems };
}

module.exports = { parseTranscript, clean };
```

### Two Cleaning Modes (Same Source, Surface-Appropriate Output)

- **PPTX speaker notes** show in PowerPoint's presenter view at delivery time. Pass `stripStageDirections: true` so stage cues like `_(pause)_` get removed - cleanest possible prose, zero visual noise during the talk.
- **DOCX presenter reference** is the read-through artifact (paper or screen) used for rehearsal. Use the default (`stripStageDirections: false`) so stage cues stay as `(pause)` text - they remind the presenter where to pause, slow down, or beat for emphasis during read-aloud.

Same transcript, surface-appropriate cleaning. Both surfaces auto-update from a transcript edit at next regenerate.

### Markdown Conventions the Parser Expects

The parser assumes the markdown transcript follows the structure documented in Phase 3:

- Slide blocks separated by `---` on its own line
- Each block opens with `## SLIDE <N> - <Title> (<timing>)`
- `**[On screen: ...]**` line for the visual cue (parser strips it from spoken output)
- Spoken prose between the on-screen line and `**[Advance]**` / `**[Advance to Q&A]**`
- Stage directions as `_(pause)_`, `_(beat)_`, etc. (italic markdown, parens inside)
- `### Additional Info - Slide <N>` bullet list for presenter-reference depth
- `### Diagrams - Slide <N>` for optional diagram description block
- `## Anticipated Q&A (Presenter Prep)` appendix with `### Q: "<question>"` blocks

Deviating from these conventions breaks the parser silently (empty `spokenParas`, missing Q&A). If a project needs a different transcript shape, fork the parser into the project. Do NOT generalize this skill's reference template to support multiple shapes - the multi-format-support tax compounds fast and degrades the failure-loud behavior the silent-deviation rule depends on.

### Sync-Divergence Discipline When Adopting On An Existing Deck

When retrofitting an existing deck whose `generate-pptx.js` has hardcoded speaker notes, the runtime-parsed notes may differ from the hardcoded ones in subtle ways (most commonly: stage directions present in transcript but absent from hand-polished hardcoded notes; whitespace collapse; bold/italic markdown stripping). Before swapping the source of truth, run a one-slide sample diff (e.g., spot-check slide 1 + slide N/2 + last slide) so the user knows whether speaker-note content will change at next regenerate. If divergence is purely stage-direction stripping (covered by `stripStageDirections: true`), the swap is safe. Other divergences warrant naming explicitly before commit.

---

## Phase 4: PPTX Slide Deck

### File: `workspace/<project>/generate-pptx.js` → `workspace/<project>/<slug>-presentation-v<N>.pptx`

Use `pptxgenjs` to generate visual slides programmatically.

### Design System

**Read `DESIGN.md` at the idea-forge repo root before defining any palette.** It is the single source of truth for idea-forge's visual identity (PPTX dark palette, DOCX light palette, typography, components, do's and don'ts). Do not invent a new color set; copy the relevant tokens from DESIGN.md into the project's `generate-pptx.js`.

For PPTX specifically, the palette to use is the dark / presentation mode from DESIGN.md. The minimum tokens to copy:

```javascript
// Copy from DESIGN.md (presentation palette - dark mode, "Ember & Ink")
const C = {
  bgDark:    "14161B",   // surfaceDark (iron)
  bgMid:     "1A1D24",   // surfaceMid (forge)
  bgCard:    "1D2026",   // surfaceCard (steel)
  purple:    "8259EF",   // primary - STRUCTURE (section bars, card accent bars)
  ember:     "FF6B35",   // EMPHASIS - the strike; at most one per slide
  yellow:    "FFB454",   // spark - stat highlights
  shipped:   "34D399",   // emerald - shipped/done indicators
  warn:      "F87171",   // semantic.warn (PPTX variant)
  white:     "F4F2EE",   // textOnDark (warm white)
  body:      "CDCFD4",   // textOnDarkBody
  dim:       "6E7178",   // muted text
};
```

**Conventions inherited from DESIGN.md:**
- Dark backgrounds for projector visibility (warm-white-on-`bgDark` exceeds WCAG AAA).
- Ration the ember: ONE strike (0.25in x 0.06in ember tick above the key element) per slide max. Purple is structural and may repeat; ember marks the single thing the slide exists to say.
- Sharp-edged rectangles only - never rounded corners.
- Typography: Arial Black for titles only (32pt+); Calibri for body (14-18pt at projection distance); Consolas for code.

**If a project's tone genuinely calls for a different palette** (e.g., a brand-required color not in idea-forge's identity), document the deviation in the project's North Star and capture the chosen palette in the project's own `north-star.md` rather than mutating DESIGN.md. DESIGN.md describes idea-forge's identity, not per-project overrides.

### Slide Types

Build helper functions for each slide type:

| Type | Use For | Key Elements |
|------|---------|--------------|
| Title slide | Opening/closing | Large title, subtitle, gradient background |
| Concept slide | Introducing ideas | Title, 2-3 cards with icons, supporting text |
| Comparison slide | A vs B | Two-column layout, colored headers |
| Flow/timeline | Process, evolution | Numbered steps with arrows |
| Data table | Numbers, comparisons | Styled table with header row |
| Formula/code | Technical detail | Monospace font, highlighted box |
| Callout slide | Key stat or warning | Large number/emoji, minimal text |
| Diagram slide | Architecture, flow, relationships | Native pptxgenjs shapes (rectangles, lines, arrows) |

### Diagram Approach: Native Shapes Default, Mermaid for Markdown Only

Two separate diagram surfaces exist in this skill, with different defaults:

| Surface | Renderer | Default | Why |
|---------|----------|---------|-----|
| Markdown transcript (`<slug>-transcript-v<N>.md`) | Notion / GitHub / markdown viewer | **Mermaid** | The consumer's tool already renders Mermaid. Code blocks are diff-friendly. Authoring is text-only. |
| PPTX deck (`<slug>-presentation-v<N>.pptx`) | PowerPoint / Keynote / Google Slides | **Native `pptxgenjs` shapes** | The renderer does NOT speak Mermaid. Producing in-deck Mermaid requires `mmdc` (Mermaid CLI) to render to PNG, then embedding the PNG - an extra runtime dependency rarely installed on Mac dev machines (`brew install mermaid-cli` is opt-in). Native shapes are deterministic, scriptable in the same JS file, version-controlled as code, and have zero external dependencies. |

**Use native shapes for PPTX diagrams.** Compose flow / architecture / relationship diagrams from `slide.addShape(pres.shapes.RECTANGLE, ...)`, `pres.shapes.LINE`, and `pres.shapes.RIGHT_TRIANGLE` (for arrowheads). The pattern shipped in `workspace/context-engineering-talk/generate-pptx.js` (Slide 4 - five slot boxes in three group containers with central question node + connecting lines) is the reference - check it before writing your own.

**When Mermaid in PPTX is acceptable:**
- High-complexity diagrams (10+ nodes, multiple interconnections) where native-shape positioning math becomes more code than the Mermaid source.
- Diagrams already authored as Mermaid for the markdown transcript and the visual is identical (avoids duplication).

In those cases, install `mmdc` (`npm install -g @mermaid-js/mermaid-cli`), render to PNG out-of-band, and embed via `slide.addImage(...)`. The Visual Self-QA gate's primary path (or its degraded XML-grep variant) MUST run on PNG-embedded diagrams - PNG renders are an opaque blob and structural grep cannot validate them at all.

**Keep Mermaid for the markdown transcript regardless.** The transcript's diagram section serves the presenter as reference material and renders inline in Notion or any markdown viewer. The PPTX shape diagram and the transcript Mermaid diagram describe the same content from different surfaces; both can exist for the same slide.

### Speaker Notes via Shared Parser (No Hardcoded Strings)

Speaker notes MUST be loaded from `transcript-v<N>.md` at generation time via the shared parser from Phase 3.7. Do NOT inline note strings inside `generate-pptx.js` - hardcoded notes are the drift mode Phase 3.7 exists to prevent.

At the top of `generate-pptx.js`:

```javascript
const path = require("path");
const pptxgen = require("pptxgenjs");
const { parseTranscript } = require("./transcript-parser");

const { slides: transcriptSlides } = parseTranscript(
  path.join(__dirname, "transcript-v1.md"),
  { stripStageDirections: true },
);
const notesBySlide = Object.fromEntries(
  transcriptSlides.map(s => [s.num, s.spokenParas.join("\n\n")]),
);
```

At each slide block:

```javascript
{
  let s = pres.addSlide();
  // ...visual content...
  s.addNotes(notesBySlide[N]);  // N matches the slide's number in the transcript
}
```

The slide-number key (`N`) matches `## SLIDE <N>` in the transcript markdown; the parser indexes by that number so slide order in source code can differ from slide order in the deck without breaking notes (the parser sorts by `num` internally).

If a transcript slide is missing its corresponding `s.addNotes(notesBySlide[N])`, the Visual Self-QA degraded-mode `notesSlide*.xml` count check (Phase 4, below) catches it - that's why "Speaker notes present per slide" is a structural-check pass condition.

### Execution

```bash
node workspace/<project>/generate-pptx.js
# Produces: workspace/<project>/<slug>-presentation-v<N>.pptx
```

### Visual Self-QA Checkpoint (Mandatory Before Declaring Build Done)

This is a Completion Gate item per `builder-foundation/SKILL.md` Section 4 (Visual Honesty, Binary Outputs). The agent writes JS code that emits a binary PPTX it never sees. Without this checkpoint, visible bugs (Mermaid `\n` line-break renders, autofit collapse, hex/RGBA mismatch, font overflow) surface only when the user opens the deck. This step makes the agent the first reader of its own output.

**Procedure (Primary Path - requires `soffice` CLI):**

1. Convert the generated PPTX to PDF:
   ```bash
   python scripts/office/soffice.py --headless --convert-to pdf workspace/<project>/<slug>-presentation-v<N>.pptx
   ```
2. Convert at least 3 representative slides (title, one mid-deck content slide containing a diagram, conclusion) to JPEG:
   ```bash
   pdftoppm -jpeg -r 150 -f <N> -l <N> workspace/<project>/<slug>-presentation-v<N>.pdf workspace/<project>/qa-slide
   ```
3. Read each generated `qa-slide-*.jpg` via Claude Code's image-reading capability.
4. Verify per slide:
   - Diagrams render fully (no `\n` literal text appearing; labels not cut off; native shapes positioned correctly)
   - No text overflow, no autofit collapse, no overlapping shapes
   - Colors match the plan (hex format applied correctly)
   - Font choices and sizes match the template
5. If any visible issue is found, fix the generator script and re-render before proceeding.
6. Optional but recommended: run the same check on every slide for high-stakes presentations.
7. After the build is approved, delete the temporary `qa-slide-*.jpg` files (they are throwaway QA artifacts).

**Degraded Mode (when `soffice` is unavailable):**

The primary path requires LibreOffice's `soffice` CLI for PPTX -> PDF conversion. On machines without it (typical macOS dev machines unless `brew install --cask libreoffice` ran), the gate cannot render visually. Do NOT skip silently - run the XML-grep fallback below, then explicitly mark visual rendering as NOT verified in the completion summary. This catches structural breakage (missing slides, dropped speaker notes, lost titles, missing diagram labels) but does NOT catch visual failure modes the gate exists for: autofit collapse, hex/RGBA mismatch, font overflow, color clash, label cutoff, shape positioning bugs. Treat the gate as PARTIALLY PASSED.

1. Probe for `soffice` first: `command -v soffice >/dev/null && echo "primary" || echo "degraded"`. If `degraded`, proceed below.
2. Unpack the PPTX (it is a zip) and run structural checks:
   ```bash
   unzip -o workspace/<project>/<slug>-presentation-v<N>.pptx -d /tmp/pptx-qa-<slug>
   # Slide count matches plan:
   ls /tmp/pptx-qa-<slug>/ppt/slides/slide*.xml | wc -l
   # Speaker notes present per slide:
   ls /tmp/pptx-qa-<slug>/ppt/notesSlides/notesSlide*.xml | wc -l
   # No literal \n leaking into diagram labels (Mermaid-era failure mode):
   grep -l '\\n' /tmp/pptx-qa-<slug>/ppt/slides/slide*.xml || echo "OK no literal \\n"
   # Each slide title appears in its XML (sanity check on title rendering):
   for n in $(seq 1 <SLIDE_COUNT>); do
     grep -q "<expected-title-substring-for-slide-$n>" /tmp/pptx-qa-<slug>/ppt/slides/slide${n}.xml \
       && echo "slide $n title OK" || echo "slide $n title MISSING"
   done
   # DESIGN.md hex tokens appear at expected frequency (color application sanity):
   grep -o 'val="[0-9A-Fa-f]\{6\}"' /tmp/pptx-qa-<slug>/ppt/slides/slide*.xml | sort | uniq -c
   ```
3. Cleanup: `rm -rf /tmp/pptx-qa-<slug>` after the probe.
4. EXPLICITLY document what was NOT verified in the completion summary (see Reporting below). The signal is load-bearing - "degraded mode + silent pass" collapses to "skipped" and defeats the gate's purpose.
5. Surface every degraded-mode run as a `[Notice]` candidate for the quarterly Skill Health Audit: is this machine missing `soffice` by design (no install allowed), by oversight (install it), or by tradeoff (acceptable for the deck's use context)? Three different answers, three different follow-ups.

**Reporting:**

- Primary path: `Visual Self-QA: <N> slides rendered and verified.`
- Degraded path: `Visual Self-QA: DEGRADED MODE (no soffice CLI). Structural checks passed (<N> slides, <M> speaker notes, <K> title-presence checks). Visual rendering NOT verified - presenter MUST open the deck in PowerPoint, Keynote, or Google Slides before any live use. Failure modes NOT caught by this gate: autofit collapse, hex/RGBA mismatch, font overflow, color clash, label cutoff, shape positioning.`

**Why this isn't optional:** PPTX is the one place the builder pipeline violates the agent-native-substrate principle (the agent writes JS, JS emits a binary, the binary is opaque to the agent). The recurring failure modes documented in CLAUDE.md (literal `\n` leaks, autofit, color formats) all fall in this gap. The gate's intent is to make the agent the first reader of its own output. The primary path closes the gap fully; the degraded path closes the structural half and ships an explicit signal for the visual half. Silent skip is the failure mode the gate exists to prevent.

---

## Phase 4.5: Cross-Agent Deliverable Review (Opt-In; Recommended for High-Stakes Topics)

After generating the transcript, PPTX, and any code artifacts, optionally run a cross-agent review on the **deliverables themselves** — not just the plan. It catches errors that single-agent generation misses; ask the user first (opt-in, per the lifecycle overview).

### North Star Alignment

Every review round must reference the **North Star** from the plan to prevent drift:
- Extract the North Star statement from the plan (e.g., "A hands-on workshop where attendees build and deploy...")
- Include it in every critic prompt so reviewers can verify deliverables serve the original vision
- Reject any critic suggestion that contradicts or dilutes the North Star

### Critic Roles for Deliverable Review

#### Codex — Code & Fact Verification

```
Review the following generated deliverables against the plan's North Star:

NORTH STAR: [paste from plan]

Verify:
1. All Solidity code compiles and follows best practices (if code repo exists)
2. All import paths are correct (e.g., @hiero/system-contracts/ — use the current package, not the legacy one)
3. All CLI commands (Foundry, cast, forge) use correct syntax and flags
4. All URLs are valid and point to correct resources
5. All technical claims in transcript match the plan's Fact Bank
6. Speaker notes in PPTX match transcript content
7. No placeholder text remains in any deliverable
8. Code examples in slides match the actual contract code

Output format:
1) CRITICAL_ISSUES (bugs, wrong facts, broken commands)
2) NON_CRITICAL_IMPROVEMENTS (style, clarity)
3) NORTH_STAR_ALIGNMENT (does the output serve the stated goal?)
4) READY_FOR_DELIVERY (yes/no + reason)
```

#### Gemini — Engagement & Visual Quality

```
Review the following generated deliverables for engagement and visual quality:

NORTH STAR: [paste from plan]

Verify:
1. Transcript flows naturally as spoken word (not robotic reading)
2. Humor lands and is appropriately placed
3. Slide layouts are visually balanced (no overcrowding, proper spacing)
4. Code blocks are readable (font size, contrast)
5. Transitions between slides are smooth
6. Engagement is driven by content hooks, humor, and pacing (never audience interaction prompts)
7. Timing allocations are realistic for each slide's content density
8. Visual hierarchy guides the eye correctly on each slide
9. NO slide-narration: spoken words add context beyond what's on screen, not repeat it
10. NO monotonous enumeration: slides don't follow "here are N things" + read each one
11. NO audience interaction prompts: never write "show of hands", "raise your hand", "who here has", polls, or any line that requires the audience to respond. Assume zero interaction except Q&A at the end. Engagement comes from content, humor, pacing, and rhetorical questions (ones you answer yourself immediately).
12. Tidbits from Additional Info woven into spoken parts (origin stories, fun facts, personal reactions)
12. Varied paragraph structure across slides (not the same intro-list-conclusion pattern)
13. Conversational bridges used ("Here's the thing...", "What's interesting is...")
14. At least one "off-script" human moment per 3-4 slides

Output format:
1) ENGAGEMENT_ISSUES (dead zones, missing humor, awkward transitions)
2) SLIDE_NARRATION_ISSUES (slides that read like bullet-point recitation)
3) VISUAL_ISSUES (layout problems, readability concerns)
4) NORTH_STAR_ALIGNMENT (does the output serve the stated goal?)
5) READY_FOR_DELIVERY (yes/no + reason)
```

### Procedure

1. Concatenate deliverable content into inline prompts (never reference file paths for critics)
2. Run Codex and Gemini critics in parallel with per-agent timeouts
3. Merge feedback, prioritizing consensus items
4. Apply accepted changes to deliverables
5. Re-generate PPTX if slide code was modified
6. Max 2 rounds for deliverable review (lighter than plan review)

### Integration with Code Repos

When the deliverables include a code repository (e.g., workshop code), Codex should also verify:
- Solidity syntax and pragma version
- Import path correctness against the target library structure
- Test coverage matches specification
- README accuracy against actual project structure
- Build configuration (foundry.toml, remappings) is correct

---

## Phase 5: DOCX Presenter Reference

### File: `workspace/<project>/generate-docx.js` → `workspace/<project>/<slug>-transcript-v<N>.docx`

Use the `docx` npm package to generate a formatted Word document.

### Data: Shared Parser (Default Mode, Preserves Stage Cues)

Load slide data and Q&A from the transcript via the shared parser from Phase 3.7. Default mode preserves stage directions like `(pause)` as cues in the printed presenter reference (PPTX strips them for clean presenter-view notes; DOCX keeps them for read-through rehearsal).

```javascript
const path = require("path");
const { parseTranscript } = require("./transcript-parser");

const transcriptPath = path.join(__dirname, "transcript-v1.md");
const { slides, qaItems } = parseTranscript(transcriptPath);
// slides[i] = { num, title, timing, onScreen, spokenParas, infoBullets, diagrams }
// qaItems[i] = { question, answer }
```

The DOCX renders `slides[].spokenParas` as body text, `slides[].onScreen` as the visual-cue bar, `slides[].infoBullets` as the Additional Info box, and `qaItems` as the Anticipated Q&A appendix. Every regenerate picks up the latest transcript edits with zero manual sync.

### Design System (DOCX)

```javascript
const C = {
  purple: "6B46C1",      // Primary heading color
  purpleLight: "EFEAFB",  // Light background (lavender tint)
  ember: "C2410C",        // Burnt ember - rationed emphasis runs
  emberLight: "FFEDD5",   // Light ember tint
  dark: "231F20",         // Ink - headings
  body: "4A4A52",         // Graphite - body text
  border: "D6D3CE",       // Warm gray table borders
  blue: "2563EB",         // Info boxes
  blueLight: "DBEAFE",    // Info box background
  warn: "DC2626",         // Warning color
  green: "059669",        // Success/defense
};
```

### Component Library

Build these reusable functions:

| Function | Purpose | Visual |
|----------|---------|--------|
| `slideHeader(num, title, timing)` | Purple badge + title + timing | Numbered header bar |
| `onScreen(text)` | Gray bar describing slide visual | "On screen: ..." |
| `transcript(lines)` | Indented speaker lines | Bold/italic formatting |
| `infoBox(title, bullets)` | Blue bordered box | "Additional Info" section |
| `comparisonTable(left, right)` | Two-column comparison | Colored headers |
| `flowArrow(steps)` | Numbered vertical flow | Steps with arrows |
| `diagramTable(items)` | Label + description rows | Colored left column |

### Key docx-js Rules

- **Always use `WidthType.DXA`** — never `WidthType.PERCENTAGE` (breaks in Google Docs)
- **US Letter**: width 12240, height 15840, content width 9360 (with 1" margins)
- **Table width = sum of columnWidths** — both `columnWidths` array AND cell `width` must match
- **Use `ShadingType.CLEAR`** — never `SOLID` for table shading
- **Colors must be exactly 6 hex digits** — never append opacity suffixes
- **Never use `\n`** — use separate `Paragraph` elements
- **PageBreak must be inside a Paragraph**

### Validation

```bash
python scripts/office/validate.py output.docx
python3 -m markitdown output.docx | head -100
```

Check that all slides and Additional Info sections are present.

---

## Phase 6: Review & Iterate

### User Review Cycle

1. Present the transcript (markdown) first — it's fastest to review
2. Generate PPTX only after transcript is approved
3. Generate DOCX after PPTX is approved (or in parallel)
4. Each round of feedback creates a new version (v1 → v2 → v3)

### Fact Verification Checklist

Before finalizing any version, verify:

- [ ] All numbers/statistics have a source and date
- [ ] No outdated claims (check if data is > 6 months old)
- [ ] Technical claims are accurate (protocol features, supported assets)
- [ ] Historical events have correct dates and amounts
- [ ] Disclaimers are present where required (financial, legal, medical)

---

## File Structure

```
workspace/<project>/
  north-star.md                         # North Star guardrail
  <slug>-plan-v<N>.md                   # Document plan
  <slug>-research.md                    # Research brief (if applicable)
  <slug>-transcript-v<N>.md             # Versioned transcript
  <slug>-presentation-v<N>.pptx         # Final slide deck
  <slug>-transcript-v<N>.docx           # Final presenter reference
  generate-pptx.js                      # PPTX generator script (project-specific)
  generate-docx.js                      # DOCX generator script (project-specific)
  critique-r<N>-*.md                    # Cross-agent review output
  demo-repo/                            # Tutorial/demo code (if applicable)
```

---

## Lessons Learned

These patterns emerged from building real presentations; the content-craft lessons are encoded inline as Transcript Writing Rules 1-8 and the Natural Delivery Rules (above).

### Shared Authoring Conventions (Mermaid, Additional Info, Demo-Heavy, Host Q&A)

Mermaid diagram requirements, Additional Info depth, Demo-heavy format, and Host Q&A
format are shared with `presentation-planner` and live in
`skills/presentations/presentation-conventions.md`. Apply them when writing the
transcript and appendices.

### Process

- **Transcript first, slides second.** The words drive the visuals, not the other way around.
- **Research sub-tasks run in parallel.** Don't block on fact-checking — spawn them early.
- **Cross-agent review is overkill for most presentations** but valuable for regulatory, financial, or medical topics where accuracy is critical.
- **The presenter should NOT read word-for-word.** The transcript is a guide, not a teleprompter script. Say this explicitly in the document.

---

## Cross-Agent Review Integration

Opt-in, via the global `cross-agent-review` skill (full procedure lives there). Plan review (Phase 2): max 3 rounds, stop when `CRITICAL_GAPS_REMAINING` is `none`. Deliverable review (Phase 4.5): max 2 rounds, lighter touch - implementation errors, not redesign; always reference the North Star. Error-class strengths: Claude - structure/logic; Codex - facts, code, URLs; Gemini - engagement, visuals, delivery.

---

## Output Rules

- Never write files larger than 200 lines in a single response
- For large files, write in sequential chunks and continue automatically
- If you hit an output token limit, resume exactly where you stopped

---

**Version:** 1.5.0

**Changelog:**
- **1.5.0** (2026-06-12): Recognize the **Investor Pitch** presentation type - load `skills/presentations/pitch-deck-genre.md` and hold the Problem -> Solution -> ... -> Ask thread when writing the transcript. Source: workspace/idea-forge-meta/pitch-deck-audience-learn-improve-v1.md.
- **1.4.0** (2026-06-11): Leanness trim after the model-upgrade ablation review - Quick Start, feedback-patterns and audience-calibration tables, helper-code example, and inline-duplicated lessons bullets removed; cross-agent integration compressed and made consistently opt-in (resolves the always-vs-opt-in contradiction in favor of CLAUDE.md's "optional"); "never overwrite versions" bullet removed (the keep-latest Versioning rule stands). No new behavior.
- **1.3.0** (2026-06-08): Extracted six authoring conventions shared with `presentation-planner` - Presentation Type Profiles, content-discipline rules (no-redundancy, no-repetition, mixed-audience, executive-structure, follow-the-thread), Additional Info depth spec, Mermaid diagram requirements, Host Q&A format, and Demo-heavy format - into `skills/presentations/presentation-conventions.md`. SKILL.md now points to that single source of truth. No behavior change; transcript-craft rules 1-8 and all phase workflow stay inline.
- **1.2.0** (2026-05-17): Phase 3.7 Shared Transcript Parser - PPTX speaker notes and DOCX both load from `transcript-v<N>.md`; no hardcoded note strings.
- **1.1.0** (2026-05-17): Visual Self-QA degraded mode; Diagram Approach (native shapes for PPTX, Mermaid for markdown transcript).
- **1.0.0**: Initial skill.
