---
name: linkedin-api
description: Use when composing LinkedIn posts - writes post text and carousel/image assets to a local directory for manual review and publishing. Optimized for the 2026 LinkedIn algorithm (dwell time, Golden Hour, document carousel format).
---

# LinkedIn Post Authoring (Save-Local Workflow)

This skill **does not publish to LinkedIn**. It produces a self-contained bundle (post text + images / carousel pages) in a local `linkedin/` directory. The user uploads and publishes manually at https://www.linkedin.com/feed/?shareActive=true.

Why save-only in 2026: LinkedIn's March 2026 Authenticity Update demotes automation-pattern content. The REST API also silently truncates text past ~3000 chars and adds round trips that risk shadow-truncated posts. Manual upload gives full control over preview, media order, and timing.

## Local Output Convention

Every post is a folder bundle:

```
<project>/linkedin/
  post.txt              # first-3-line hook + body + hashtags, final copy-paste-ready
  01-cover.png          # assets in upload order (1-9 images or 5-10 PDF pages)
  02-*.png
  ...
  carousel.pdf          # optional, for Document-post upload (best-performing format)
  publishing-checklist.md  # optional short checklist for the user
```

Default target directory: `<project-root>/docs/linkedin/` or `<project-root>/linkedin/`. Ask the user if the path is ambiguous.

## Algorithm Mechanics (2026)

LinkedIn's 2026 algorithm ranks by **dwell time** above everything else - the actual seconds a reader spends on the post. Likes barely register. Comments are weighted ~15x a like. Every authoring choice should maximize read-time and comment substance.

### Dwell-time tiers

| Read duration | Engagement rate | Distribution |
|---------------|-----------------|--------------|
| 0-3 s | 1.2% | Limited |
| 11-30 s | 6.1% | Extended |
| 31-60 s | 10.2% | Maximum |
| 61+ s | 15.6% | Exceptional (~2.5x wider reach) |

### Golden Hour

The first 60-90 minutes after posting determine distribution tier. Only ~5% of posts that underperform in hour one ever recover. Tactics:
- Post during working-hour windows: Tue-Thu 8-10 AM local (primary), 12-2 PM (secondary)
- Reply to every comment within the first hour - each reply compounds dwell measurement
- Seed with 2-3 trusted colleagues who leave substantive (5+ word) comments

### Demotion triggers (know them cold)

- **External URLs in the post body**: ~60% reach reduction. Do not include links unless the user accepts the penalty. "Link in first comment" callouts are also detected and demoted.
- **Engagement-bait phrases**: "Comment YES if you agree", "Like to see the PDF", "DM me for the link", "Follow for more" - NLP-flagged.
- **Polls**: dead format (~0.07% engagement in 2026).
- **AI-pattern text**: the March 2026 Authenticity Update flags em-dash-heavy prose, "It's not X, it's Y" templates, generic LinkedIn-speak ("In today's fast-paced world..."), and other boilerplate.
- **Bro-etry**: single-sentence paragraphs one after another with no substance.

### Comment mechanics

Comments are 15x a like in the ranking model, but LinkedIn weighs comment quality:
- Short "Nice!" / emoji-only comments are filtered as low quality
- Substantive comments (5+ words, especially questions, disagreements, anecdotes) count
- Every author reply roughly doubles the comment's signal value
- A comment that triggers a multi-reply thread is the strongest signal on the platform

## Format Performance (2026)

| Format | Avg engagement | Notes |
|--------|---------------|-------|
| LinkedIn Live video | 29.6% | Premium, rare, highest reach |
| **PDF / Document carousel** | **6.6%** | **278% above video, 596% above text.** Default recommendation for technical / B2B |
| Multi-image carousel | ~6.6% | Similar weight to PDF but less searchable |
| Native video (< 90 s, vertical) | 5.6% | Growing 2x faster than other formats. Hardcoded captions required |
| Text post | 2-4% | Baseline |
| Single image | Below text | Lowest of the standard formats |

**Default for technical content: PDF document carousel, 5-10 slides at 1080×1080.** Every swipe is tracked as a dwell-time increment, multi-slide interaction is measured, and numbered frameworks ("5 lessons...", "3 mistakes...") add a further 20-30% to dwell.

## Post Types

- **Text only** - quick takes, discussion prompts. Baseline reach.
- **Single image** - when one visual carries the whole point. Lowest-engagement standard format.
- **Multi-image / PDF carousel** - the workhorse. 5-10 slides at 1080×1080.
- **Native video** - under 90 seconds, vertical, hardcoded captions.
- **Article** - long-form publisher tool (outside this skill).

## Asset Specifications (2026)

| Asset | Dimensions | Aspect | Max size |
|-------|-----------|--------|----------|
| Single image | 1200×627 | 1.91:1 | 5 MB |
| Multi-image carousel | 1080×1080 each | 1:1 | 10 MB each |
| PDF document carousel | 1080×1080 per page | 1:1 | 100 MB, up to 300 pages |
| Slide deck (16:9 alternative) | 1920×1080 | 16:9 | 100 MB |
| Banner | 1128×191 | 6:1 | 4 MB |
| Video (landscape) | 1920×1080 | 16:9 | 5 GB, 3 s to 10 min |
| Video (vertical) | 1080×1920 | 9:16 | 5 GB, 3 s to 10 min |

### Carousel design rules

- **1080×1080 square is the default**. LinkedIn does not render portrait carousel aspect ratios correctly.
- **5-10 slides** is the sweet spot - more hurts completion rate.
- **Cover slide is self-contained**: topic + hook promise + swipe cue.
- **Every slide stands alone** - a reader may land mid-deck via a share. Do not rely on "as shown on the previous slide".
- **Minimum in-slide text: 24 pt** - LinkedIn compresses PDFs aggressively, smaller text renders illegibly.
- **Numbered frameworks** outperform unnumbered (+ ~25% dwell).
- **Consistent style across all slides** - same fonts, palette, margins, card styling.
- **Embed the article's REAL measured figures on proof slides, regenerated with English labels.** When the source article has a measured chart or image (a constellation scatter, a recovered image, a BER curve), embed that figure rather than redrawing a schematic of it - it is more credible and genuinely "derived from the source". Regenerate it in English via a `FIG_LANG=en`-style switch that writes to an `images_en/` dir (leaving the original-language figures untouched), then embed the English PNG with `<image href>`. Keep schematic SVG for the architecture / pipeline / results slides; use real data on the proof slides.
- **Same numeric-honesty discipline as the source article - the carousel makes the same claims.** Every number on a slide must trace to a real measurement, and the headline / cover stat must be a DEPLOYED-SYSTEM metric, not a reference-model number. Never put a machine-epsilon or "perfect" model figure on the cover; for fixed-point hardware the honest headline is the bit-level result (e.g. "0 bit errors"), not a precision the chip cannot reach. The wechat-api skill's numeric-audit ("reference-model metric presented as the deployed result", "unrealistic operating point") and "describe the system accurately" rules apply identically here.
  - **Provenance, not just consistency (BLOCKING).** "Traces to a real measurement" means a CURRENT tool-output file you opened (`resource_report.json` / `timing_report.json` / sim log), cited by path - not a finding/history/retrospective doc, a prior post, a sibling slide, or memory. If you cannot cite the report, RE-RUN the measurement workflow to get the exact value before posting. When you correct or add one number, re-trace ALL its siblings (the whole sweep / table) from the same source - one non-reproducing number means the set is suspect, and consistency across slides is NOT proof a number is real (it can be consistently wrong everywhere). Full rule + the Viterbi failure case: the `svg-diagram` skill.

### Carousel narrative arc

1. **Slide 1 (cover)**: hook + promise + swipe cue
2. **Slide 2**: problem / agitation - why the reader cares
3. **Slides 3-N-2**: solution - numbered framework, one insight per slide
4. **Slide N-1**: result / proof / data payoff
5. **Slide N**: punchline + open question CTA

### Diagram visual style (IMPORTANT)

Default to **clean technical-diagram style**, not marketing-social style. Carousel slides for technical audiences (engineers, researchers, hardware / ML / infra professionals) read as credible when they look like figures from a research paper or trade magazine, not like influencer promo graphics.

**Prefer this style** (proven to work for technical B2B):

- **Light pastel gradient backgrounds** (e.g., `#eff6ff → #dbeafe` for blue cards, `#f0fdf4 → #dcfce7` for green, `#fefce8 → #fef9c3` for yellow). White canvas background.
- **Rounded cards** (`rx="14"` to `rx="16"`) with thin 2-2.5 px colored strokes that echo the card's accent hue.
- **Helvetica Neue / Arial** sans-serif. No custom display fonts.
- **Information-dense layout**: body labels around 17-22 px, headings 26-36 px, page counter and captions 16-20 px.
- **Right-side info chips** on layered cards (like era markers, year badges). White-filled chips with same stroke color as the parent card.
- **Muted accent palette**: slate `#334155`, blue `#1971c2`, green `#059669`, amber `#ca8a04`, red `#dc2626`. Dark text colors matching stroke (`#1971c2` heading on blue card, `#065f46` on green, `#854d0e` on amber).
- **Small label ribbons** in dark slate (`#1e293b`) with white text for slot markers like `LESSON 1`, `PROOF`, `TAKEAWAY`.
- **Subtle italic subtitle** in `#64748b` below the bold title.
- **Page counter** in `#94a3b8` at bottom-right: `3 / 7`.
- **Mobile-display sizing.** A 1080-wide slide is shown at ~370px in the phone feed, so a label's
  on-phone size is `font * 370 / 1080`. The 17-22px body floor above renders only ~6-7.5px on a
  phone — fine for a glanceable slide, too small for a dense one. The fix for a dense slide is the
  same as for any figure: put FEWER items per slide (split across slides) rather than shrinking
  text, and lean on the **`svg-diagram` skill** for the compaction layouts (stacked cards, fewer-
  boxes+ellipsis), the inline-Feather-icon enrichment, the figure-text-accuracy sweep (every
  number AND framing word on a slide must match the post text), and the **box-fit audit** (run
  `svg_audit.py` on every authored slide so no label centered in a box overflows it - see the
  workflow step 3 below).

**Avoid this style** (looks AI-marketing, lowers perceived credibility for technical readers):

- Bold violet/magenta gradients (`#a855f7 → #3b82f6`) as dominant color
- Oversized display headlines (>60 px) that crowd out content
- Gradient-filled "LESSON" badges with glow effects
- Gradient title text (title text filled with a `<linearGradient>`)
- Decorative circuit-dot / hexagon backgrounds that look AI-generated
- Heavy drop shadows or glow halos
- Fewer than 3 information blocks per slide (too much negative space = looks padded)

**Minimum in-slide font is still 24 pt** — but a dense technical slide with 17-22 pt body text inside 60+ px card sections reads well because the card itself acts as visual structure. A slide with one giant 80 pt headline and nothing else reads as "AI slop" even though it passes the minimum-font check.

**Reference / reuse rule:** if the same article has a Chinese WeChat version with clean technical diagrams, re-author **those actual diagrams** at 1080×1080 in English (the full system/micro-architecture, the real datapath, the specific schematic) — do NOT downgrade them to plain text-block slides with one big number. The rich figure is the credibility signal. Plain blocks read as "AI slop". Always pull the source article's diagrams first and mirror their content.

**Lead a technical carousel with one real architecture / overview figure** (slide 2, right after the cover): a labeled block diagram of the actual system datapath. It is the strongest credibility signal, it says "this is a real, complete design" rather than a marketing claim. Real result: a decoder carousel gained an architecture figure (LLR memory -> barrel shifter -> check-node unit -> variable-node memory, plus control and the feedback loop) and it anchored the whole deck.

**If the source has a real mechanism, DRAW the mechanism, never summarize it as numbered bullets in a colored box.** A data hazard becomes a producer -> register -> memory -> consumer figure with a stale-read path and a forwarding bypass; a diagnosis becomes the actual critical-path chain plus the two competing fixes. Real failure: a carousel's "dependency" and "wrong turn" slides were two columns of numbered text and were repeatedly called "not readable / not illustrative"; rebuilding each as a real labeled figure fixed it. Bulleted text is the text-block anti-pattern even inside a nicely-colored card.

**When a finished carousel is rejected as "not readable / not attractive" and the fix is a subjective redesign, lock the visual direction before rebuilding.** Offer 2-3 concrete style-direction options with tiny preview mockups (editorial-story vs rich-technical-figure vs bold-infographic) and let the user pick, instead of guessing a fourth time. The AskUserQuestion `preview` field is built for this. Real result: after several misses, one preview question ("rich technical figure" + "lead with technical credibility") nailed the direction and the rebuild landed in one pass.

### Style rotation (vary the look every post)

Reusing one visual template post after post makes the feed look templated and lowers credibility — a real failure: a new carousel was rejected because it looked identical to the author's previous posts (same light-blue frame + slate pill ribbon + royal-blue accent + big-number card). **Rotate the style.** Each post picks a preset that differs from the **immediately previous** post (ideally random among the rest), and that fits the story's tone.

Record the choice in the bundle as a one-line `STYLE.txt` (e.g., `dark-scope`). Before authoring, read the most recent bundle's `STYLE.txt` (or eyeball the prior slides) and pick a different preset.

Credible preset palette (every preset still obeys: min 24 pt, dense figures with 3+ blocks, no AI-marketing gradients / glow / hexagon-circuit decorations):
- **light-blueprint** — white canvas, teal ink + monospace technical labels, datasheet-figure look.
- **dark-scope** — dark navy canvas (`#0b1220`), monospace signal/cycle labels, muted neon green/red/cyan, a FAINT line grid (not dotted), terminal/diff panels; reads like a logic analyzer. Best for timing / debug / cycle-accurate stories. Keep neon muted (no glow halos).
- **light-pastel-cards** — white canvas, pastel rounded cards, slate ribbons (the classic default; use only if the previous post was NOT this).
- **editorial** — off-white, large ink typography + one warm accent (amber), big single-focus figures. Best for opinion / strategy pieces.
- **slate-mono** — light slate canvas, near-monochrome ink + one accent, monospace throughout, minimal.
- **flat-hardware** — light page tint (`#edf1f7`) + WHITE cards with real (manual) elevation shadows; each card an accent title strip + tinted internal regions; a restrained system (grey ramp + one accent per role: amber = RF/compute, teal = memory/expansion + green/red/blue semantics); a DARK-navy full-bleed cover billboard + a dark summary panel on the results slide. Best for hardware / board / architecture stories. Draw chips as accurate block symbols (NOT boxed rectangles with pins — see `svg-diagram` "IC / chip / FPGA package accuracy"); use the manual blurred-rect shadow (NOT `feDropShadow`, which drops the fill in librsvg).

Match preset to tone: a debugging / timing story suits dark-scope or blueprint; a strategy piece suits editorial; a hardware / board build suits flat-hardware. Whatever the preset, re-author the article's real diagrams in it.

**Default to LIGHT presets when in doubt.** Dark-scope can look great in your own preview but darkens further at LinkedIn's thumbnail compression, and dark backgrounds are unforgiving of low-contrast secondary text (muted slate-on-navy turns illegible). Failure case (2026-05-30 ai-rtl-bug-debug): a dark-scope deck was initially produced for a debug story but had readability issues on mobile thumbnail — user explicitly requested a switch to light. The fix went to `light-pastel-cards` and reads cleanly at every zoom level. Rule: if the story tone suits dark-scope, build it AND verify at thumbnail size before committing. If any text relies on subtle slate-on-dark for hierarchy, switch to a light preset; dark-scope only wins when the deck is dominated by monospace signal/cycle labels with no narrative prose.

### Layout that reads as "designed" (full-canvas grid, billboard cover, KPI results)

These turn a plain deck into a designed one; they came out of a hardware-deck rebuild that took
many misses before landing. Web-grounded (Material elevation, Refactoring UI, LinkedIn carousel
guides):
- **Full-canvas grid — no bottom blank.** Every interior slide: title band (top) -> the figure
  FILLS the body to the lower margin -> a one-line caption strip. The commonest amateur tell is a
  slide clustered in the top two-thirds with a dead bottom third. Put the detailed specs in the
  CAPTION so the body figure stays large and nothing overlaps (overlapping leader-callouts on the
  figure are the other tell).
- **The cover is a BILLBOARD, visually different from slide 2 — not a shrunk content diagram.**
  Flip the axes vs the interior: DARK full-bleed (navy `#0f172a`) while interiors are light; ONE
  hook (a huge number/BAN, or a 3-word claim, one accent word) at 72-120pt; an eyebrow/kicker
  top-left (13-16px uppercase, tracked, accent) + a `SWIPE ›` affordance; <12 words; at most one
  minimal hero motif, never the full block diagram. A cover that is the same figure smaller +=
  a title fails.
- **Results / "proof" slides = KPI stat-cards, not three text rows + tiny bars.** Each card:
  uppercase LABEL / a big number (BAN, 56-76pt, in the role accent) + unit / a one-line sub / a
  green check "status" pill; a left 6-7px accent strip; real elevation. Close the slide with a
  DARK summary panel (the "punctuation" moment) carrying the headline + a verification pill. Empty
  feeling comes from many tiny elements in a big field — make the few elements BIG.
- **Add a real hardware/board PHOTO as a proof slide** when the story is a physical build (annotate
  the real chips/connectors; see `svg-diagram` on EXIF-normalizing + verifying annotation positions
  against the actual render). It is the strongest "this is real" credibility anchor.
- **Readable-first ALWAYS beats vivid.** Anti-pattern that cost a whole rebuild: an isometric
  hardware deck looked vivid but overloaded each slide (overlapping callouts, 13-19px labels that
  shrink to ~6px on a phone, embedded matplotlib figures illegible at carousel scale) and the user
  rejected it as "worse to read". Vivid must never cost legibility: one idea per slide, big labels,
  specs in captions, redraw ambiguous glyphs as unmistakable before/after. When a finished deck is
  rejected as "plain" OR "cluttered", don't patch positions reactively — redesign on a real grid
  (see above), and lock the visual direction with a preview question first.

### One carousel, per-audience captions (do NOT maintain a separate deck per audience)

When the same story goes to two pages (e.g. a personal page + a company page), produce ONE
`carousel.pdf` and TWO caption files in the same bundle dir — `post.txt` and
`post-<audience>.txt` — not a second slide directory. The slides are audience-neutral
(architecture-forward); only the caption voice differs (first-person build story vs company
capability framing). Note the split in `publishing-checklist.md` (same PDF, two captions, spaced
18-24 h apart).

### Glossing domain terms for adjacent-specialty readers

LinkedIn's "technical audience" is not monolithic. An FPGA engineer reading an LDPC post does not necessarily know what `K_avg` means; a hardware verification engineer reading an HFT post does not necessarily know `mid-price` or `TWAP`. Even when the audience is technical, the cross-pollination between sub-specialties is high, and an unexplained domain term is the most common reason a reader bounces from the carousel before slide 3.

**Two-tier label pattern for domain terms in diagrams:** put the technical definition as the primary label, the plain-language gloss as a smaller subtitle below.

```
K_avg = iters per codeword   <-- 24 pt bold, the precise definition
(one LDPC frame)             <-- 18 pt italic, the friendly gloss
```

In the post text, define every domain term on first appearance with a parenthetical gloss, then use the term freely afterward:

```
Bad:  "The 4× K_avg gap stayed."
Good: "The 4× K_avg gap (K_avg = average iterations to decode one codeword,
       i.e. one LDPC frame) stayed."
```

Apply to: every algorithm metric (K, BER, EVM, NMSE), every hardware-block acronym (FE, BE, CNU, BRAM, LUTRAM, SRL), and every project-specific signal name that drives the narrative (first_iter, sum_old, branch_mem). Audience expansion is free; assumed knowledge has a cost.

## Post Text Best Practices

### Length & structure
- **Hard cap**: 3000 characters (past this the API silently truncates; manual paste just cuts off)
- **Optimal for dwell time**: 1000-1300 characters
- **Paragraphs**: 2-3 lines max. Longer is fine if broken by white space between short paragraphs
- **White space** between paragraphs drives ~40% more dwell time vs wall-of-text

### The hook (first 3 lines, ~210 chars desktop / ~49 mobile)

LinkedIn truncates on mobile at about 49 characters and on desktop at 2-3 lines. The reader has to click "see more" to trigger dwell-time accumulation. Without that click the post dies.

Proven hook patterns:

| Pattern | Template | Example |
|---------|----------|---------|
| Contrarian | "X is not the problem. Y is." | "Hand-writing Verilog isn't the bottleneck. Architecture iteration is." |
| Unexpected stat | "<specific number> <outcome>." | "28 DSP blocks instead of 52. A 46% saving nobody on our team predicted." |
| High-stakes problem | "If you <A>, you're about to hit <B>." | "If your pipeline breaks every time you change N, you are burning weeks per project." |
| Origin / vulnerable | "Six months ago I <struggle>. Here's what changed." | "Six months ago I was hand-writing 2000 lines of Verilog per project. Today AI writes them. Here is the tradeoff." |
| Question | "Why does <surprising premise>?" | "Why does AI write better pipelined hardware than most junior engineers?" |

### Body structure (after the hook)

- **Context paragraph** - 1-2 sentences: why the topic matters now
- **Value section** - bullets, numbered list, or short before/after contrast
- **Takeaway** - one specific lesson the reader can apply today
- **CTA question** - open, short, personal - see CTAs section

### Narrative / story-telling structure (default for experience-driven posts)

The flat structure above is fine for a pure reference post, but a **narrative arc reads as
more interesting and earns more dwell time** whenever the post is about something you *did*
(an experiment, a debug session, a build, a mistake). Prefer it by default for those.

Arc that works (proven this session - a bulleted feature-dump rewritten as narrative was
markedly more readable):

1. **Setup** - first person, concrete stakes. "I handed an AI a real timing failure and watched it work."
2. **Rising tension** - what was tried and what went wrong. Keep the failures in; they are the interesting part.
3. **The turn** - the single pivot. One sentence, set off by white space, often the emotional core ("Here is the part people assume an AI cannot do: it backed out.").
4. **Resolution** - what actually worked, with the specific numbers kept intact for credibility.
5. **Reflection + CTA** - what it means, then the open question. Returning the CTA to the hook's phrasing closes the loop.

Story-telling craft rules:
- **Show the struggle, not just the win.** Dead ends, reverts, and wrong assumptions are what makes it a story instead of a brochure. A post that is all wins reads as marketing.
- **First person, past tense, specific.** "It came back at -0.642 ns. Worse." beats "results were suboptimal."
- **One idea per paragraph, 2-3 lines, white space between.** The arc should be skimmable on mobile.
- **Keep every concrete number.** Narrative makes it readable; the numbers make it credible. Do not trade one for the other.
- **Narrative posts run longer** - 1500-2200 chars is normal and acceptable here even though the pure-reference optimum is 1000-1300. The dwell time the story earns outweighs the length. Still respect the 3000 hard cap.
- **Genuine arc, not story scaffolding.** This is the opposite of the flagged anti-pattern. Do NOT open with "Let me share a story...", "Here's the thing:", or "Picture this:". Just start *in* the story with a concrete first action. The structure carries it; announcing it does not.

### Formatting rules

- **Max 2-3 emojis** per post, and only where they replace punctuation or act as bullet markers
- **Unicode bullets** (•, →, ▸) render cleanly; native markdown does not
- **No em-dashes** (one of the strongest AI-detection signals in 2026). Use colon, parenthesis, or a period.
- **No all-caps shouting**
- **No repeated ellipses...** (pattern-flagged)
- **Keep the first sentence punchy** - every character before the "see more" cut is valuable

### CTAs that generate substantive comments

Comments are worth 15x a like. Always close with an open question that invites a 5+ word reply.

| Good CTA | Why |
|----------|-----|
| "What's the part of <X> you'd most want to automate?" | Personal, open |
| "Curious how others handle <problem>." | Invites shared experience |
| "Disagree? I want to hear the counter-case." | Invites contrarian replies (strongest signal) |
| "Which of these <N> surprised you?" | Forces a choice, easy to reply to |
| "What would you add to this list?" | Invites extension, low-effort for reader |

**Never use** (NLP-flagged, demotes the post):
- "Comment YES if you agree"
- "Drop a 🔥 below"
- "Like this post to see the PDF"
- "DM me and I'll send the link"
- "Follow for more"
- "Tag someone who needs this"

### Hashtag strategy

- **3-5 hashtags** max. More is spam-pattern and demoted.
- Place at the very end of the post, each on its own line is fine or all on one line
- First hashtag carries the most weight - make it the most relevant
- Mix tiers: 1-2 broad (#AI, #FPGA) + 2-3 niche (#HardwareDesign, #Verilog, #RFSoC)

## Post Templates

### Template A - Technical insight (carousel, recommended)

```
<Hook: contrarian or specific-number, 1 line>

<Context: 1-2 lines on why this matters now>

<Value payoff, 2-4 lines, with specific numbers>

<Takeaway: 1 line, what the reader should do differently>

<CTA question>

#Tag1 #Tag2 #Tag3 #Tag4
```

Target length: 900-1300 chars. Pair with 5-10 slides.

### Template B - Carousel slide sequence

```
Slide 1 (cover): 3-line headline + promise + "swipe →"
Slide 2: Problem framing / agitation
Slide 3-N-2: Solution, one insight per slide, numbered
Slide N-1: Result / proof - charts, stats, screenshots
Slide N: Punchline recap + open-question CTA (same as post body)
```

### Template C - Short discussion post (text only)

```
<Hook: question or contrarian claim, 1-2 lines>

<Context: 2-3 lines>

<Observation or specific example>

<CTA question>

#Tag1 #Tag2 #Tag3
```

Target length: 500-900 chars.

## Posting cadence & timing (user-side)

Include these in the publishing checklist you give the user:

- **Frequency**: 3-5 posts / week. Less than 2/week means the algorithm can't categorize your expertise; more than 5 splits engagement across posts
- **Best windows** (local time): Tue-Thu 8-10 AM (primary peak), 12-2 PM (secondary)
- **Avoid**: weekends, Friday afternoons, Monday mornings
- **Spacing**: 18-24 hours between posts, otherwise the earlier one cannibalizes the later one
- **First hour**: stay near the app, reply to every comment within 5-10 minutes

## Authoring workflow

When this skill is invoked to produce a post:

1. **Identify target directory**. Default `<project>/docs/linkedin/`. Create if missing.
2. **Decide format** (ask user if ambiguous):
   - Technical / B2B / explanatory -> PDF document carousel (default)
   - Opinion / discussion / short take -> text-only
   - Announcement / launch -> single image or short carousel
3. **Produce assets**:
   - Carousel: author 1080×1080 SVGs, then render via `rsvg-convert -w 1080 -h 1080 page.svg -o page.png`
   - Single image: 1200×627
   - Follow asset specs above exactly
   - **Box-fit pass (BLOCKING) - on EVERY native slide you draw, not just embedded figures:**
     1. Run `python3 ~/.claude/skills/svg-diagram/scripts/svg_audit.py *.svg` as a candidate-finder.
     2. **Confirm every `text-overflows-box` flag against the rendered PNG** - the width heuristic
        (Latin ~0.6em) OVER-reports lowercase-heavy labels ("on the critical path", "phase counter")
        and anchor-start text, so many flags are FALSE POSITIVES. Do NOT rewrite a label that the
        render shows fitting; over-correcting a false positive is its own failure (see svg-diagram).
     3. **Also eyeball every rendered slide** - the render is ground truth; a label centered in a box
        (`text-anchor="middle"`) spills out BOTH ends when its width exceeds the box. Crop the
        suspect region if unsure.
     Fix a REAL overflow by shortening the text or splitting it across two stacked `<text>` lines (or
     widening the box), never by clipping it or shrinking below the 24 pt floor. This catch is what
     was missing: the native slides (cover, problem, fix, dead-end) are where overflows hide; the
     embedded article figures were already audited. Real failure: a Viterbi carousel shipped
     "branch metric (off the path)" overflowing its 264px box because the slide SVGs were never run
     through svg_audit OR eyeballed; the user had to catch it. Box-fit + ribbon-width + line-
     splitting rules + the false-positive traps all live in the `svg-diagram` skill.
4. **Optionally combine carousel PNGs into PDF** for Document-post upload:
   ```bash
   # Preferred: ephemeral img2pdf via uv (no install, works with no venv active).
   uv run --with img2pdf python3 -c "import img2pdf, glob; open('carousel.pdf','wb').write(img2pdf.convert(sorted(glob.glob('0*.png'))))"
   # If already on PATH: img2pdf 01-*.png 02-*.png ... -o carousel.pdf
   # Do NOT rely on bare `img2pdf`, `convert`, or `uv pip install img2pdf` -- in a
   # clean environment all three commonly fail (not installed / no active venv).
   ```
5. **Write `post.txt`**:
   - First 3 lines must hook
   - Optimal 1000-1300 chars
   - 3-5 hashtags at the end
   - No em-dashes, no banned CTA phrases, no external URLs
6. **Validate**:
   - **Box-fit: `svg_audit.py *.svg` run, every `text-overflows-box` flag resolved** - real overflows
     fixed, lowercase/anchor-start false positives confirmed fitting against the render, and a visual
     scan of each rendered slide shows no label crossing a box edge (see step 3). Re-run after edits.
   - `wc -c post.txt` under 3000, aim for 1000-1300
   - Image dimensions match spec
   - Hashtag count 3-5
   - Grep for banned strings: em-dash, "Comment YES", "DM me", "link in comment", "follow for more"
7. **Optionally write `publishing-checklist.md`** with the manual steps:
   - Which compose option to pick (text / image / document)
   - Upload order
   - Best posting time
   - Golden-hour reply reminder
8. **Report** the full bundle path to the user. Do not attempt to publish.

## Anti-patterns (never produce)

- External URLs in post body (60% reach penalty)
- "Link in first comment" cues
- Any engagement-bait phrase from the CTA anti-patterns list
- Polls
- Single long paragraph ("wall of text")
- Single-sentence-per-paragraph bro-etry
- Em-dash prose (also avoid em-dashes inside diagram text — user convention is hyphen or colon)
- More than 5 hashtags
- Portrait or 16:9 carousel when user didn't specify - default is 1:1 square
- AI-pattern openings: "In today's fast-paced world...", "Let me share a story...", "It's not X, it's Y.", "Here's the thing:"
- Auto-publishing via the REST API (truncation risk, authenticity penalty)
- Marketing-gradient carousel slides (bold violet → blue backgrounds, gradient-filled display headlines, glowing "LESSON N" badges) for technical audiences — see "Diagram visual style" above
- Internal / framework labels in post text OR slides (`V1`-`V5`, `Phase N`, `Tier N`, `pymodel` / `golden` / `leaf` / `recipe`, commit hashes) — meaningless to an outside reader; translate to outcomes
- Flourish over clarity (performed-casual decoration): a forced hook ("you probably use this every day without realizing"), manufactured mini-suspense ("the result? it got worse"), or a cute metaphor for a plain fact. Explain plainly. If a colloquial phrase only performs a voice and adds no information, cut it. The bar is clear, not casual.
- Mixing devices/configs in one post: a story is ONE device + ONE configuration. A flagship part's numbers and the deployed part's numbers in the same narrative breaks trust and the motivation. (A spec table may list configs, each labeled with its device.)

## Optional: Legacy API Reference

Scripts at `${CLAUDE_PLUGIN_ROOT}/scripts/` are retained for users who explicitly want programmatic publishing:
- `oauth-server.py` - OAuth 2.0 flow
- `linkedin-api.py` - publish, upload, verify

**The default workflow no longer uses these.** If a user explicitly requests auto-publish, warn them:
- LinkedIn's 2026 Authenticity Update demotes automation-pattern posts
- The REST API silently truncates `commentary` past ~3000 chars (no error returned)
- Text truncation requires Playwright-based edit-in-browser fix
- Manual upload is safer and often reaches more people

If they still want it, see `scripts/linkedin-api.py --help` and the published-post truncation fix flow described in `commands/post.md` (advanced section).
