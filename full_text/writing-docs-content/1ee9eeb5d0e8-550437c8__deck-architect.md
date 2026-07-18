---
name: deck-architect
description: Use when the user is building, outlining, or revising a slide deck, presentation, talk, pitch, board update, or briefing — any time someone needs to decide what to say, in what order, and what to cut. Use when a draft feels too long, too generic, doesn't land, or sounds AI-generated. Use when someone says "help me make a deck about X" — structure is where decks fail. Do NOT use when the user only wants visual polish on already-finalized content. Style enforcement (slop-phrase list) is English-only; structural rules apply to any language.
version: 2.6.0
license: MIT
allowed-tools: [WebSearch]
tested-with: claude-sonnet-4.5+, claude-opus-4+
approx-tokens: ~4700 (SKILL.md only); +1000–3000 per loaded reference
---

# Deck Architect

Handles the part of deck-building AI is bad at: **content and structure**. Not visuals. Produces a sharp outline; hands off to a visual-design skill (e.g. `pptx`) for rendering.

## When NOT to use

- User only wants visual polish on already-finalized slides → use `pptx` directly
- Single-slide updates / one-off charts → overhead exceeds value
- The deliverable is a written doc, not a deck → use a writing skill
- The deck must follow a locked corporate template that conflicts with full-sentence titles or main-flow rollback slides — the skill's prescriptions will fight the template; flag this and let the user choose
- User wants speaker notes only for an existing deck — the skill produces full outlines, not note-only revisions
- Someone else owns the structural decisions and the user is just executing — the skill pushes back on structure; that's friction in this case
- Non-English decks where the user wants enforcement on style — the structural checks (no agenda, full-sentence titles, tradeoff, rollback) still apply, but the slop-phrase list is English-only

## The Iron Law

**No slides without Audience + Takeaway + Spine first.**

Applies to new decks AND edits. If you catch yourself drafting before those three are locked, stop and go back to Phase 0. The rationalizations table in [references/rationalizations.md](references/rationalizations.md) covers every excuse you'll be tempted by — read it once, then don't re-litigate.

## The AI Slop Test

Before finalizing, ask: **"If someone said 'Claude wrote this deck,' would it be obvious?"**

A deck that passes:
- Slide titles are full-sentence messages, specific to this project
- Every substantive slide has at least one concrete detail (a name, number, date, artifact)
- The deck argues something — it doesn't just "cover" a topic
- Nothing could be copy-pasted to another company with nouns swapped

**When the test fails OR you're uncertain: Read `references/forbidden-phrases.md`** for the full list and structural tells. Use the TL;DR below as a first pass; load the reference when (a) a slide title or body hits one of the listed phrases, (b) you're writing fresh persuasive copy where slop risk is high (pitch, exec recommendation, board update), or (c) the audience is sophisticated enough to penalize any generic language. If the TL;DR catches everything, no need to load.

> **TL;DR if you don't load the reference:** ban hedged corporate filler — "leverage," "unlock," "drive alignment," "robust," "seamlessly," "stakeholders," "ecosystem," "significant impact," "in today's fast-paced world," "we are excited to." Replace each with a concrete noun or verb that carries information. "Significant impact on retention" → "D30 retention moved from 22% to 41%." Specificity is what kills the slop.

## Operating principles

- **Audience first, always.** Phase 0 is non-negotiable. The audience determines the takeaway, the spine, the wins to surface, and the main-vs-backup split.
- **Audience is the hero, not the presenter.** Frame as their problem → their transformation. The presenter is the mentor.
- **Strategy first, slides last.** No slide content until audience, brief, takeaway, and spine are locked.
- **Pull for specifics, resist topics.** Topics produce generic output; specifics produce a deck only this user could give.
- **Honesty is a persuasion tool.** Name the tradeoff before the audience does.
- **Adversarial read before the live read.** Pressure-test before presenting (Phase 6).
- **Contrast creates attention.** Alternate problem/solution, current/future. Monotone = forgotten.
- **Progressive disclosure by default.** Main flow + backup layer.
- **Credit humans specifically.** Names + specific wins, never anonymous "we."
- **Protect opening and close.** Primacy + recency. Don't waste either on agenda or thanks.
- **Text-first on visuals.** Default text-only. Earn each visual.

---

## Workflow

Follow phases in order. Don't skip ahead.

If the user brings an existing draft, don't start from scratch — but don't skip Phase 0 either. Run Phases 0–1 (infer answers from the draft, confirm with user), then use Phase 4 as the main working mode. All other phases still run — driven by the existing draft rather than a blank page. Phase 2 (spine) re-validates or replaces the existing structure; Phase 3 becomes a slot-by-slot revision (cut / merge / rewrite titles / add missing hook or STAR); Phases 5–8 unchanged. Output a revised outline plus a "what changed and why" section (the Phase 8 output schema has a slot for this).

### Phase 0 — Model the audience

**Lock this before anything else.** Ask these five questions in one compact block:

1. **Who's in the room — specifically?** Names or roles. Hardest sell? Decision-maker? Likely interrupters?
2. **What do they care about?** Their incentives, not the topic. ROI/risk (CFO), strategic fit (CEO), technical rigor (eng leaders), career impact (often the real one).
3. **What do they already know/believe?** Skip what they know. Anticipate what they'll disagree with.
4. **What's the transformation?** Walk-in state → walk-out state. ("Skeptical of budget" → "convinced this is the cheapest insurance we can buy.")
5. **What objections / deep-dive questions will they raise?** List 3–5. These feed the backup layer (Phase 8).

Output: an **Audience Model block** at the top of your response. Cite it whenever you cut a slide in Phase 4.

**If the user won't answer after one push:** infer from context and mark each inferred answer with `[INFERRED — confirm]` so they can correct in one pass. Better an inferred Audience Model than no Audience Model.

**If the user brought an existing draft:** infer answers from it before asking. Audience clues = formality, jargon density, named stakeholders. Takeaway clues = the close (or its absence). Objection clues = the slides that already exist defensively (TCO, rollback, comparison tables). Confirm inferences with the user, don't replace asking.

For a real example of a complete Audience Model block, see [references/example.md](references/example.md).

### Phase 1 — The rest of the brief

One block, four items:

1. **Decision or action.** What do you want them to do/decide/approve/remember? If there isn't one, flag it — the deck has no purpose.
2. **Format & time.** Live presentation, async pre-read, or both? Minutes? Live decks and slide docs aren't interchangeable.
3. **Constraints.** Slide-count cap? Required sections? Brand/template?
4. **One-sentence takeaway.** If they remember one sentence, what is it? Shaped by Phase 0 — same project, different audiences, different takeaways. Don't move on without this.

Same fallback as Phase 0: if the user won't answer after one push, infer and mark with `[INFERRED — confirm]`. Exception: the one-sentence takeaway. Don't infer this — help the user articulate it instead. A wrong takeaway is worse than a missing one.

**Existing-draft mode exception:** if there's no live dialogue (user handed you a draft and expects a revised outline back), templatize the takeaway as `[USER: write the one-sentence takeaway]` and flag it as a blocking item in the handoff notes. Do not invent one.

**Phase 1a — Team credit (conditional).** If the deck describes work by multiple people (any "we," "the team," named collaborators, cross-functional shipping of something non-trivial), ask once: *"Is this a team effort? If so, tell me who contributed to which key wins so credit lands with the right people."* Then:

- **Tie specific wins to specific humans on the slide.** Not "the team reduced latency" — "Priya rewrote the caching layer, cutting p99 latency 42%."
- **Surface individual wins in speaker notes** even when the slide stays clean — verbal credit lands harder than on-slide text.
- **Add a Credits slide near the end** (second-to-last, before the takeaway close) when the contributor list is meaningful. Specific, name-by-name. "Thanks to the team" gets cut.
- **Never invent attributions.** If unsure, ask or use neutral framing.

**Phase 1b — Existing assets (conditional).** If the user mentions specific assets/screenshots/imagery, ask once where to find them and what else is available. Don't ask by default — friction without payoff.

### Phase 2 — Pick the narrative spine

Choose ONE structure. State which and why before outlining.

| Situation | Spine |
|---|---|
| Executive / business / recommendation | **SCQA + Pyramid (Minto)** — Situation, Complication, Question, Answer-up-front, then 2–4 MECE supporting arguments |
| Technical talk / conference | **Hook → Problem → Insight → Evidence → Takeaway** — single technical claim, not a survey |
| Pitch (funding/sales/partnership) | **Problem → Why Now → Solution → Why Us → Proof → Ask** |
| Update / status | **Headline → What changed → What it means → What's next** — headline first, details on tap |

If the situation doesn't fit cleanly, pick the closest and state the adaptation.

**Spine details:**
- **SCQA:** answer-up-front (the recommendation is slide 1 of body), then 2–4 supporting arguments. Arguments must be **MECE** — no overlap, full coverage. Two arguments saying the same thing? Collapse them.
- **Hook→Insight→Evidence:** time budget ~15% hook/intro, 60–70% body, 15–20% demo + close. The insight is a *single* technical claim, not a survey.
- **Pitch:** use only when explicitly pitching for funding, sale, or partnership.
- **Update:** resist walking through every workstream. Headline first; details on tap.

### Phase 3 — Draft the slide list (in text)

Numbered list. Each slide:

- **Title** — full-sentence message (the point the slide makes), NOT a topic noun
- **Purpose** — why this slide exists, one line
- **On-slide** — what appears on the slide (3–6 bullets max, or chart spec, or short sentence + visual)
- **Speaker notes** — what the presenter says that is NOT on the slide
- **Load** — `slide-heavy` | `balanced` | `speaker-heavy`

**The slide/speaker split is the craft.** If a phrase is on the slide, the presenter shouldn't read it aloud. Slide = anchor (number, phrase, chart, question). Presenter = story, nuance, example, "why this matters."

**Slide-body vs. speaker-notes bans are enforced at render time.** Authoring vocabulary from the outline (`Triggered by:`, `Depth: L2`, `See B4`, `[INFERRED — confirm]`, structural narration like "in the next slide…") must never reach audience-visible body copy. It goes in `Speaker notes`, or it gets cut. See the "Slide-body commentary" section of `references/forbidden-phrases.md` for the full list. A renderer that drops these fields flat onto the slide has broken the contract — flag it during handoff.

**Required content for every deck:**

- **Opening hook** (Phase 3a) — first 30 seconds. Not "Title + name." A pattern-interrupt that anchors to what the audience cares about and promises what they'll get.
- **STAR moment** (Phase 3b) — Something They'll Always Remember. A shocking stat, dramatization, soundbite, or vivid visual. Hook and STAR can be the same thing if the hook is genuinely unforgettable. If you can't identify one, push back on the user.
- **Tradeoff** (Phase 3c) — every persuasion deck must name what's being given up. Either a dedicated "What we're giving up" slide or an explicit on-slide tradeoff bullet. Not buried in speaker notes.
- **Rollback** (Phase 3d, decision decks only) — if the deck asks for approval on something with real consequences (migration, launch, hire, major investment, policy change), main-flow slide on rollback triggers, owners, and recovery. Burying this in backup signals the presenter hopes nobody asks.
- **Close** (Phase 3e) — close on the takeaway, full screen. Not "Thank you." Not "Questions?" (say that verbally; keep the takeaway visible).
- **Contrast** — alternate problem/solution, current/future. Don't stack slides in the same emotional register.

**Read `references/slide-craft.md` before writing slide titles** — it contains the DO/DO NOT tables for titles, openings, contrast, tradeoff phrasing, rollback specs, and the slide/speaker split patterns. These rules are enforced; not loading them produces the exact failures Phase 4 will catch.

> **TL;DR if you don't load the reference:** (1) Titles are full sentences with subject + verb + specific claim — never noun phrases. (2) Opening earns the first 30 seconds with a pattern-interrupt; never "Title + name" or "Agenda." (3) Slide and speaker notes complement, never duplicate. (4) Alternate emotional registers — don't stack four problem slides then four solution slides. (5) Close on the takeaway full-screen, never "Thank you" or "Questions?"

### Phase 4 — Ruthless discipline pass

Show the user what was cut and why.

**Slide-count ceilings (push back if user exceeds without reason):**

| Deck type | Ceiling |
|---|---|
| Live exec update | 5–10 content slides |
| Board deck | 10–15 + appendix |
| Conference talk (20 min) | 15–20, one idea per slide |
| Pitch (YC-style) | ~10 |
| External customer business review (QBR, renewal) | 8–12 + appendix |
| Exec pre-read (slide doc) | No fixed limit, dense prose per page |

If content exceeds the ceiling, **cut — don't shrink fonts.** Move detail to appendix.

**Time reality-check.** Math out time-per-slide vs. allotted minutes. Live decks: 1–2 min/content slide; charts 2–3; hook/close more. State the math when it forces a cut: "20 slides in 15 min = 45s/slide, too fast — cut to 12."

**Cut rules:**

- **One idea per slide.** Two messages → split or cut. Two slides making the same point → merge.
- **Cut test:** "If I deleted this slide, would the argument still hold?" If yes, delete.
- **Filler to delete on sight:** agenda slides on decks <15 slides; "About us" up front; "Thank you" / "Questions?" closers; transition slides ("Section 2"); slides that restate what's about to come.
- **Empty-calorie tells:** title could apply to any company; lists categories without synthesis; chart shows data without takeaway in title.

**Run the AI Slop Test** using the inline TL;DR at the top of this file. **Read `references/forbidden-phrases.md`** when (a) any slide title or body hits a listed phrase, (b) this is fresh persuasive copy (pitch, exec recommendation, board update), or (c) the audience is sophisticated enough to penalize any generic language. Skip the load if the TL;DR catches nothing. Rewrite with specifics — every forbidden phrase has a concrete replacement.

**Audience-fit check.** Re-read through the audience's eyes. Cut what they know. Add what they'd push back on.

### Phase 5 — Spec visual aids (only where earned)

**Default text-only.** For every slide, ask "does this slide need a visual?" — not "what visual goes here?" Forcing visuals onto every slide is an AI anti-pattern.

A slide earns a visual when:
- The argument depends on data the audience must see → **chart**
- It's a system/flow/relationship words describe poorly → **diagram**
- It's the opening hook or STAR moment needing emotional punch → **image**
- The point is about a specific product/UI/artifact → **screenshot**

Otherwise: mark `text-only` and move on.

**Read `references/visuals.md`** for full chart-type selection rules, diagram modes, image search/licensing protocol, and screenshot format before specifying any non-text-only slide.

> **TL;DR if you don't load the reference:** comparison → bar; trend → line (≤5 series); part-to-whole → stacked bar (avoid pies >4 slices); relationship → scatter. **Forbidden:** 3D charts, pies with many slices, dual-axis without genuine unit difference. Chart titles state the insight, not the metric. One highlight color per chart; everything else gray. For images, run `WebSearch` for 2–3 candidates with a slide-specific query, surface URLs with one-line fit notes, **always flag licensing** — never fabricate URLs.

**Topology auto-earns a visual.** Chains, graphs, sequences, 2×2 quadrants, and waterfalls with ≥ 3 nodes and explicit directional structure are not allowed to fall through to text-only. deck-architect emits a structured spec and the shipped renderer (`scripts/render-visual.js`) produces inline SVG that inherits the deck's design tokens. See `references/visual-specs.md` for the five shipped shapes (`flow`, `bar`, `graph`, `quadrant`, `waterfall`), their spec schemas, and the placement contract. For visuals that don't fit any shape (screenshots, photographs, hand-drawn), the outline emits a `data-visual-todo` placeholder and the lint flags it if it ships.

When images are needed and the user hasn't supplied an asset, run `WebSearch` for 2–3 candidates with a slide-specific query. **Real-world constraint:** `WebSearch` typically returns stock-library **collection pages** (e.g. `https://www.istockphoto.com/photos/server-fire`) rather than direct image-asset URLs (e.g. `https://www.istockphoto.com/photo/server-on-fire-id12345.jpg`). Surface the collection URLs honestly with one line on which fits best and a note that the user must pick the specific frame. **Always flag licensing risk** — user must verify reuse rights. **Never fabricate URLs to look more specific than the search actually returned.** When the concept is genuinely specific (a real lockscreen, a real product UI, a real whiteboard), recommend the user shoot their own — phone-shot beats stock for hooks.

### Phase 6 — Pressure test (role-play the skeptic), then final scan

**Always run. Scale to stakes — never skip.**

The other phases optimize for building a good argument. This phase optimizes for surviving a careful listener. They are different skills.

**Steps:**

1. **Pick the hardest sell** from the Audience Model.
2. **Adopt the role explicitly:** "Pressure-testing as: [the CFO who's been burned on cloud cost overruns and has 11 years in the seat]." Name priors, incentives, pattern-match history.
3. **Walk the deck in their voice.** For each slide ask: sharpest question? Under-specified claim? Worst-case assumption if you don't specify? Pattern-match from prior decks they've killed? Where does it sound like selling vs. explaining? What presenter-dependent trust assertion can't they verify?
4. **Quote, don't summarize.** "The TCO slide is hand-wavy" is useless. "Which direction is the 8% gap, and over 5 years not 1?" is useful.
5. **Classify:** **Fatal** (ask dies) / **Credibility** (presenter loses trust) / **Minor** (nit). Fix Fatal + Credibility before presenting; Minor → backup layer.
6. **Apply fixes.** Common patterns: under-specified quantitative claim → add the qualifier in the title itself. Presenter-dependent trust → co-presenter or remove. Hand-wavy direction → name it and own it. Missing tradeoff → see Phase 3c. Buried rollback → promote to main flow (Phase 3d).
7. **Show your work** in the Pressure-test log (Phase 8 output).

**Sizing — match to stakes:**

| Signal | Size |
|---|---|
| No decision asked of audience; small/reversible/friendly | **Micro** — 1 pass, hook + headline + close, 2–3 critiques |
| Recommendation/proposal with at least one skeptic; ask involving money/people/commitment | **Standard** — 1 pass from hardest sell, every slide, 5–8 critiques |
| Irreversible decision, reorg, major investment, migration, launch, board, regulator, async-read deck | **Extended** — multiple passes from distinct skeptics, every slide including backup, 8+ critiques |

When in doubt, run Standard. Cost of too-large is minutes; too-small is torched meetings.

**Read `references/pressure-test.md`** for the full step-by-step methodology, common-fix patterns, and rationalizations to refuse — load it before running the test, especially the first time per session.

> **TL;DR if you don't load the reference:** adopt the hardest sell's voice (specific priors, not Claude's voice), walk every slide, write critiques as direct quotes from the skeptic, classify Fatal/Credibility/Minor, fix Fatals + Credibilities before presenting, log everything.

**Step 8 — Final scan (always, all sizes).** After fixes land, do three cheap re-read passes:

1. **Slide-title scan.** Read every title top to bottom. Each must be a full-sentence message, not a noun phrase. Catches the #1 post-fix regression — slides that got edited for content but kept their pre-edit title.
2. **AI Slop Test on the full deck.** Re-run the named test from the top of this file. New content from pressure-test fixes is the most likely place for slop because it was written under mild time pressure.
3. **Argument coherence scan.** Read titles top to bottom as one sentence. Does it tell a coherent story landing on the takeaway? If it jumps/repeats/meanders, a Phase 6 fix broke the spine — go back to step 6, don't paper over.

The final scan is **not** another pressure test, restructuring phase, or style polish — content integrity only. Significant fixes get noted in the Pressure-test log; otherwise silent.

### Phase 7 — Build the backup layer

**Default for high-stakes decks** (board, investor, exec recommendation, anywhere skeptical/technical attendees might interrupt). Skip for low-stakes short decks (5-min status, lightning talk) and note that you did.

Source: the 3–5 objections from Phase 0 question 5. Each becomes a backup slide. Add more as the main flow reveals soft spots.

Each backup slide:
- **Trigger** — the question/moment that cues the presenter ("If anyone asks about model assumptions...")
- **Title** — same full-sentence-message rules as main flow
- **Content** — the actual depth (methodology, raw data, architecture, unit economics, sensitivity, edge cases)
- **Depth** — `L2` (one click deeper) or `L3` (full technical detail)

**Count target:** 30–60% as many backup slides as main flow. Too few = exposed; too many = can't find the right one under pressure.

**Typical backup by audience:**

- **Exec with technical sub-audience:** technical architecture, implementation timeline, tradeoff analysis, what could go wrong
- **Financial:** sensitivity analysis, unit economics, scenario tables, assumptions log
- **Board / investor:** cohort data, churn mechanics, competitive positioning detail, regulatory considerations
- **Technical:** benchmark methodology, reproducibility, alternative approaches considered and rejected

Group them clearly (by topic, by likely-asker, or by question). If using a deck tool, place after the main appendix divider.

### Phase 8 — Present the outline

Deliver as **structured text**, not slides. Use this schema verbatim:

````markdown
# [Deck Title]

## Audience Model
- Who's in the room: ...
- What they care about: ...
- What they already know/believe: ...
- Transformation (walk-in → walk-out state): ...
- Likely objections / deep-dive triggers: ...

## Brief
- Decision/ask: ...
- Format & time: ...
- Constraints: ...
- One-sentence takeaway: ...
- Team contributors (if applicable): ...

## Narrative spine
[Which structure and why — one sentence]

## Cover slide
- Title: [the single deck title — one complete thought, not a kicker fragment]
- Subtitle (optional, ≤12 words): [one supporting line, same voice, or omit]
- Meta (optional): [neutral metadata — format, time, author — styled as metadata, not title]

## Opening hook (first 30 seconds)
[The actual words / visual / stat that opens the deck — distinct from the cover title; spoken, not displayed]

## STAR moment
[The one thing the audience will remember and quote afterward — which slide it lives on]

## Main flow
1. [Title as full-sentence message]
   - Purpose: ...
   - On-slide: [what actually appears — short, anchor-oriented]
   - Speaker notes: [what the presenter says that is NOT on the slide]
   - Load: slide-heavy | balanced | speaker-heavy
   - Visual: text-only  (or chart/diagram/image/screenshot + spec)

2. ...

## Appendix divider
[A one-line header for the pause between main flow and backup. Renderers use this to insert an unambiguous visual break — never skip it when a backup layer exists. Example: "Appendix — reference material, triggered on question."]

## Backup layer
B1. [Title] — triggered by: [question/moment] — depth: L2
   - Content: ...
   - Visual: [mode + spec]
B2. ...

## Visual consistency notes
- [Cross-deck notes — single highlight color, icon family, etc.]
- [Assets user needs to source vs. create]

## What I cut (and why)
- [Topic] — reason
- ...

## What changed and why (existing-draft path only — omit for fresh decks)
- [Structural change — e.g., "Promoted Resource Asks from slide 25 to slide 7 with specificity"] — reason
- ...

## Handoff notes
- For pptx/design: [visual or layout suggestions that emerged]
- Credits slide (if team effort): [names + specific contributions]
- Licensing flags: [web-sourced images needing license verification]

## Pressure-test log [size: Micro | Standard | Extended]
- Role(s) adopted: [who you role-played, with priors]
- Top critiques surfaced: [in skeptic's voice — 2-3 Micro / 5-8 Standard / 8+ Extended]
- Fixes applied: [specific slide → specific change]
- Live-meeting prep notes (Standard/Extended only): [residual questions to rehearse]
````

**Length budget.** Default target: main flow ≤ 12 slides per response. Larger decks risk truncation — chunk into two responses (main flow first, backup second) or cap at 12 and offer to expand.

**For Micro pressure tests**, the Pressure-test log can collapse to one paragraph: *"Pressure-tested as [role]. Surfaced [N critiques], fixed by [changes]."* The full template is overkill on a low-stakes deck.

**Inferred answers** carry through to the output: `- Who's in the room: VP Eng + 2 staff engineers [INFERRED — confirm]`

For a complete worked example (brief → full schema filled out), see [references/example.md](references/example.md).

### Phase 9 — Handoff (only if rendering)

Don't render slides in this skill. Hand off to a visual skill with the outline above. Keep the content exactly as outlined — the visual skill makes it look good, not rewrites the points. Include main flow, the appendix divider, and the backup layer.

**Handoff by target format:**

| Target | Skill / tool | Contract |
|---|---|---|
| `pptx` / Keynote / Google Slides | `pptx` skill | Pass the Phase 8 output. Speaker notes go in the native notes pane. Appendix divider is a section break + a pause slide. |
| `html` (self-contained file, reveal.js, slidev) | `/impeccable` for visual design + `references/html-renderer.md` for the contract | See below |
| Markdown handoff (user renders separately) | — | The Phase 8 schema is already the handoff; flag that appendix divider is a required slide, not an optional heading. |

**HTML handoff — specific contract:**

1. **Confirm design context first.** The renderer inherits aesthetic discipline from `/impeccable`. Before generating HTML:
   - Check for `.impeccable.md` in the project root. If present, the palette, typography, and ban-lists are already decided — use them.
   - If absent, either run `/impeccable teach` to gather design context, or make a documented assumption in handoff notes so the user can override.
   - **Whichever path produced the context, verify two non-negotiables before writing CSS:** (a) a one-sentence "feel" describing the aesthetic register using a noun the audience can picture (not three adjectives); (b) contrast math on every token pair that will render as text — body-ink vs paper ≥ 4.5:1, display-ink vs paper ≥ 3:1, and an `--accent` / `--accent-ink` pair where `--accent-ink` is the one allowed on text. If either is missing, fill them in before rendering. See `references/html-renderer.md` § "Visual design inheritance" for the template and the two-tone accent rule. A bright accent used as body text is the canonical failure mode — v7 shipped with `color: var(--accent)` on terminal output and failed readability despite passing the structural lint.
2. **Start from the reference scaffold.** `skills/deck-architect/references/html-renderer-reference.html` is a minimal two-slide deck that implements the full structural contract end-to-end (viewport model, 3-region composition, notes tray, keyboard hint pill, fullscreenchange handler, print override). Copy it and adapt colors, typography, and content. Do not rebuild the scaffolding from scratch — it is a solved problem with known failure modes. Most first-render bugs come from re-deriving the scaffold.
3. **Never render speaker notes inline on the slide — not "hidden by default and shown with `S`," not at the bottom of each slide.** Notes render in a dedicated presenter-mode tray (fixed-position bottom sheet, `#notes-tray`) that swaps contents as the presenter navigates. Per-slide inline notes — even when toggled by `S` — destroy slide composition mid-presentation because the slide's vertical rhythm is no longer what the designer committed to. `aside.notes` is `display: none` on screen, `display: block` only inside `@media print`. See `references/html-renderer.md` §8 for the tray contract.
4. **Never let outline metadata leak onto slides.** `Triggered by:`, `Depth:`, `Hardest sell:`, `[INFERRED — confirm]`, `Pressure-tested as:` — all authoring vocabulary. They're in the outline because the outline is also the handoff spec; they are not slide content. The renderer places them in notes or omits them.
5. **Render visual specs before lint.** `node skills/deck-architect/scripts/render-visual.js path/to/deck.html` walks the file for `<figure data-visual-spec>` placeholders and swaps each for an inline SVG that reads the deck's own `:root` tokens (accent, ink, paper, rule, typography). This is the unification mechanism — no hardcoded colors or fonts in the SVG. Run it after HTML generation, before the lint.
6. **Lint before declaring done.** `node skills/deck-architect/scripts/lint-deck.js path/to/deck.html` runs the static checks: missing `data-role`, missing notes asides, missing appendix divider, slide-body commentary bans, inline `aside.notes` display, missing `#notes-tray`, missing `#kbd-hint`, `requestFullscreen` without a `fullscreenchange` handler, `.slide { min-height: 100vh }` (wrong viewport model), impeccable absolute-ban CSS, remaining `data-visual-todo` on main-flow slides. A clean lint is the minimum bar; it does not replace either checklist below.
7. **Visible checklist before shipping:**
   - Counter and meta row survive at a 960px viewport (no truncation).
   - Backup slides visibly differ from main (tint, watermark, or typographic shift — not just a label change).
   - No reflex fonts, no gradient text, no border-left accent stripes, no cards-in-cards.
   - Keyboard hint pill is visible bottom-right on load.
8. **Live-presentation dry run** — actually drive the deck before shipping. Each step maps to a bug we've shipped:
   1. Load the deck → default slide lands centered (not top-anchored).
   2. `→` five times → every slide lands centered.
   3. `F` (enter fullscreen) → current slide still centered.
   4. `→` inside fullscreen → still centered.
   5. `F` (exit fullscreen) → current slide still centered, no drift.
   6. `S` → `#notes-tray` slides up with current slide's notes. Head reads `speaker notes · slide N`. Hint pill hides.
   7. `→` with tray open → tray contents swap live to next slide's notes.
   8. `Esc` → tray closes, hint pill returns.
   9. Reload with `#7` in the URL → lands on slide 7.
   10. `⌘P` / `Ctrl+P` → one slide per page, notes inline under each, no tray, no hint pill.

   Any failure → back to `references/html-renderer.md`. Do not patch it in the moment; the same bug ships next time.
9. **Feel retrospective.** Before declaring done, re-read the one-sentence `feel` committed to in step 1's documented-assumption block. Open the rendered deck and ask: *does this deck look like that sentence?* If the feel-sentence is "a xerox zine pressed onto cream paper" and the deck reads as "a generic light-mode SaaS template," the palette/typography landed somewhere other than the commitment. Name the gap in handoff notes so the user can redirect before presenting. The feel sentence is a contract — honor it or document the departure.

---

## Interacting with the user

- **Phase 0 and Phase 1 in two compact blocks.** Don't drip-feed.
- **Show reasoning briefly.** When you pick SCQA over the technical-talk spine, say why in one sentence.
- **Push back when warranted.** No one-sentence takeaway? Don't let them skip — help them find one. Asking for 30 slides? Explain the cost, suggest a count, accept override.
- **When cutting, be explicit.** What was removed and why. Builds trust and catches over-cuts.
- **No slides during the brief phases.** Resist.
- **Confirm team credit when detected.** One question; never invent names.
- **For web images, actually search.** Don't just describe — run `WebSearch`, surface 2–3 URLs, note the best fit, flag licensing.
- **Always run the pressure test.** Scale to stakes. Show your work in the log.
- **Always run the final scan.** Three passes. No exceptions.
- **Quote the skeptic, don't summarize.** Specific and sharp.
- **Handle stalled briefs.** If after one push the user still won't answer Phase 0/1, infer from context and mark inferences with `[INFERRED — confirm]` so the user can correct in one pass.
- **Mid-deck audience changes.** If the room composition changes ("CFO is now joining"), re-run Phase 0 question 5 and patch the backup layer. Full re-runs only if the hardest sell changed.

## Red flags while drafting — stop and go back

If any of these are true while you're drafting, you skipped or under-cooked a phase. Stop, go back, get the missing piece:

- Drafting slides and can't state the one-sentence takeaway → back to Phase 1
- Slide title could apply to any company/project → back to Phase 3 (slide-title rules)
- Hedging ("this could potentially help drive...") → back to Phase 4 (AI Slop Test)
- Deck doesn't argue anything — it just "covers" a topic → back to Phase 2 (spine)
- Don't know what the audience will push back on → back to Phase 0 question 5
- About to write "Agenda" or "About Us" as slide 1 → back to Phase 3 (opening rules)
- Reaching for generic three-bullet structures because you don't have specifics → pull specifics from user or cut the slide
- Describing a visual as "a relevant image" → Phase 5 (either earn it specifically or go text-only)
- Deck is all upside — can't point to a tradeoff slide → back to Phase 3c
- Decision deck and rollback is only in backup → back to Phase 3d (promote to main flow)
- About to present the outline without pressure-testing → Phase 6
- Load-bearing claim doesn't specify direction ("roughly the same cost" — more or less?) → Phase 6 will catch it; fix now
- Relying on a trust assertion the audience can't verify ("I talked to X and we're aligned") → Phase 6 will catch it; fix now
- Target format is HTML and you haven't read `references/html-renderer.md` → back to Phase 9 (the contract is non-negotiable, not aspirational)
- Target format is HTML and there's no `.impeccable.md` → run `/impeccable teach` or document the design assumption; don't improvise palette/typography

For the full catalogue of rationalizations and how to refuse them, see [references/rationalizations.md](references/rationalizations.md).

## Graceful degradation — when the user genuinely won't engage

The Iron Law is the default. But if after **two** push-backs the user truly won't engage with Phase 0/1 ("just give me something I can edit," "I'll fix it later," "I don't have time for this"), don't deadlock. Switch to **minimal-brief mode**:

1. **State the switch explicitly:** *"Producing a minimal-brief outline. I've inferred audience, takeaway, and spine from context — flag everything you'd change."*
2. **Infer all of Phase 0/1** from whatever the user said. Mark every field `[INFERRED — confirm]`.
3. **Still run Phases 2–8** — spine, slide list, discipline, visuals, pressure test, backup, output. The structural discipline still applies; it's just operating on inferred inputs.
4. **Run only a Micro pressure test** — without a confirmed audience, anything bigger is theatre.
5. **Lead the output with a "What I assumed" block** so the user can correct in one pass.

Minimal-brief mode is a fallback, not an alternative path. Don't volunteer it; only use it after the user has actively refused engagement twice. A deck built from inferred inputs is worse than one built from real ones — but it's better than no deck or an argument with the user.

## Anti-patterns

Specific behaviors to avoid (the failure-modes catalogue is descriptive; this is prescriptive):

- Generating slides in response to "make me a deck about X" without Phase 0
- Accepting a topic when you could pull specifics
- Drip-feeding brief questions one per turn
- Shipping a deck with no STAR moment
- All-upside decks with no tradeoff
- Burying rollback in backup on a decision deck
- Skipping the pressure test "to save time"
- Skipping the final scan after pressure-test fixes
- Pressure-testing in Claude's voice instead of the skeptic's
- Recommending pie charts >4 slices, 3D charts, dual-axis without strong reason
- Forcing a visual onto every slide; defaulting to stock imagery
- Fabricating image URLs
- Slide content that duplicates what the presenter will say
- Vague team credit ("thanks to the team") instead of specific attribution
- Inventing contributor names
- Hedged qualifier-heavy prose where specific claims belong
- Three-equal-weight bullets as a reflex
- HTML rendering a deck without `/impeccable` design context (reflex fonts, gradient text, border-left stripes re-appear)
- HTML rendering that drops speaker notes (or collapses them into on-slide footers)
- HTML rendering without an appendix-divider between main flow and backup (main-to-reference transition is invisible live)
- Outline metadata (`Triggered by:`, `Depth: L2`, `See B4`, `[INFERRED]`) rendered as audience-visible slide copy
- Cover split across kicker + headline + subtitle where each reads as an independent sentence fragment (fragmented cover)

For background on *why* these matter — the failure modes that motivate this whole skill: [references/failure-modes.md](references/failure-modes.md). (Background reading; not required for any phase.)

## Quick reference: highest-leverage cuts

When a draft feels bloated, cut these first:

1. The agenda slide
2. The company/team intro (unless pitching to strangers)
3. Any slide whose title is a noun
4. The 3rd/4th/5th example of the same point — keep the sharpest one
5. Transition/section dividers on short decks
6. "Summary of what we'll cover" right before covering it
7. The "Thank you" closer — replace with the takeaway
8. Historical background that predates what the audience knows

## The bottom line

A great deck is a short, sharp argument delivered by a human to a specific room.

Structure beats beauty. A one-sentence takeaway beats a 15-slide overview. A specific name and number beats "significant stakeholder impact." A real moment the audience will quote beats three parallel bullets. The presenter's voice carries the story; the slide is the anchor. Every slide earns its place or gets cut.

If the deck doesn't pass the AI Slop Test, it doesn't ship.
