---
name: interactive-book-companion
description: >
  Transform any book, article, blog post, or text into an interactive learning companion using
  evidence-based cognitive science (retrieval practice, dual coding, schema activation, generation
  effect, and more). Use this skill whenever the user asks to summarize a book, create an interactive
  summary, build a learning companion, make content digestible, create a study guide, or turn any
  text into something learnable and retainable. Also trigger when the user uploads a book, article,
  or PDF and wants to learn, absorb, understand, or retain it. Applies to nonfiction, textbooks,
  research papers, articles, blogs, documentation, and any informational content the user wants to
  deeply learn rather than passively read.
---

# Interactive Book Companion Generator

Transform any text into an interactive learning companion optimized for deep retention, using
ten evidence-based cognitive science methods. The output is a single interactive React artifact
that the reader moves through at their own pace.

---

## What This Skill Does

You take the content of a book, article, or any text and produce a self-contained interactive
learning experience. The experience is NOT a passive summary — it is an active learning tool
that uses retrieval practice, dual coding, spaced structures, schema activation, and generation
effects to help the reader genuinely absorb and retain the material.

The companion should feel like a brilliant private tutor walked you through the book, not like
someone handed you a cheat sheet.

---

## Input Handling

The user may provide content in several ways:

1. **Pasted text** — the full content is in the conversation.
2. **Uploaded file** — a PDF, DOCX, EPUB, or TXT in `/mnt/user-data/uploads/`. Read it using
   the appropriate file-reading method before proceeding.
3. **Book title only** — the user names a book but doesn't provide text. In this case, use your
   training knowledge of the book. Be transparent: tell the user you're working from your
   knowledge of the book rather than the exact text, and that they can upload the full content
   for a more precise companion.
4. **URL** — the user provides a link. Use `web_fetch` to retrieve the content first.

Whatever the source, your first step is always: **read and deeply understand the full content**
before producing anything. Do not start generating the companion until you have a clear mental
model of the entire work.

### Big books: compress first, then build

A full-length book is often too large to hold in context at once. A 300-page PDF or EPUB can run
past the window, and stuffing the whole thing in is where quality quietly falls apart. So for
anything book-sized, run a compression pass first and build the companion from the compressed
knowledge, not the raw file.

Use the bundled **book-to-skill** pipeline (in `skills/book-to-skill/`, vendored from
[the-knowledge-guy](https://github.com/vitalysim/the-knowledge-guy), MIT). It runs a map-reduce
over the book and produces a small, structured knowledge base:

- **Tier 1 (`SKILL.md`):** the thesis, a concept map, the 6-10 load-bearing frameworks, a
  chapter index, and a topic index. A few thousand tokens for the whole book.
- **Tier 2 (`chapters/*.md`):** a ~1,000-token toolkit per chapter (frameworks, techniques,
  anti-patterns, examples), plus `nutshell.md`, `glossary.md`, `patterns.md`, and `cheatsheet.md`.

The flow:

1. **Compress.** Run book-to-skill on the uploaded PDF or EPUB. In Claude Code that is
   `/book-to-skill /path/to/book.pdf`. Under the hood it extracts the text with
   `skills/book-to-skill/scripts/extract.py` (PyMuPDF / ebooklib), then compresses.
2. **Build from the compressed base.** Feed the companion generator the Tier 1 `SKILL.md` as
   the backbone: the thesis becomes the opening bookend and the mind map's center, the
   frameworks become the branch nodes and principle cards, the chapter index seeds the timeline
   and the deep dives. Pull individual Tier 2 chapter files on demand when a topic needs more
   depth (for a case study, a chart, or a retrieval challenge), instead of loading the whole book.
3. **Note the source.** Tell the reader the companion was built from a compressed knowledge base
   of the book, so they know the depth is faithful but distilled.

If the source is small enough to read directly (a pasted excerpt, an article, a single chapter),
skip compression and work from the text. Compression is for when the raw content would blow the
context, which is most whole books. When book-to-skill isn't available (for example, a plain
LLM with only a system prompt and no ability to run Python), fall back to compressing manually:
chunk the book, extract the same structure from each chunk (thesis, frameworks, per-chapter
toolkit, topic index), stitch the pieces into one Tier 1 base, then build from that.

---

## The Ten Methods — How They Map to the Output

Read `references/ten-methods.md` for the full cognitive science rationale behind each method.
Below is how each method translates into a concrete component of the interactive companion.

### Method 1: Macrostructure Extraction → Interactive Mind Map Flow Diagram

Build a living, animated node-and-edge flow diagram, not a stack of tabs or cards and not a
frozen picture. The point is to show how the ideas connect and branch out, so the reader sees
the shape of the book at a glance and can trace how one idea leads to the next. It is the visual
centerpiece of the companion, so make it deep and make it move.

**Prefer a top-down tree.** Root the thesis at the top and branch downward level by level into
subtopics and their subtopics, like a knowledge tree or org chart. A top-down (or left-to-right)
hierarchical tree reads as "this contains these" far more clearly than a radial burst and scales
cleanly to four levels. Use a radial layout only when the book is genuinely hub-and-spoke.

**Four logical levels of depth.** A two-level map is too shallow. Branch out into subtopics and
their details, but only where the book genuinely has that structure. Never add branches to fill
space; every branch must be real.

- **Root (Thesis):** one node at the top holding the book's central argument.
- **Major ideas:** the 3-7 load-bearing frameworks branching down from the root. Connect them to
  each other where one genuinely feeds another, so the logical flow is visible.
- **Subtopics:** each major idea splits into its 2-5 real components, mechanisms, or steps.
- **Details & boundaries:** under a subtopic, the specific evidence, example, technique, or the
  condition where the idea breaks down.

Deeper levels stay collapsed until opened, so the tree grows downward on demand.

**Opening a node teaches; it is not a tooltip.** This is the most important part. When the reader
clicks a node, the detail panel gives a real mini-lesson: 2-4 short paragraphs explaining the
idea and its mechanism (what, why, how), a concrete worked example in a call-out, an optional
small visual, and a takeaway. A one-line gloss here is the single most common way the companion
fails to teach. Every node, down to the leaves, explains and exemplifies. See the node detail
panel spec in design-system section 7.6.

**It moves.** The map is never static:

- Nodes drift with a slow, gentle idle motion so the whole thing breathes.
- Edges carry a flowing animation (a traveling dashed line or a gradient pulse) from parent to
  child, so direction reads and the diagram feels alive.
- Opening a branch springs its children outward; the layout re-flows smoothly, never snapping.
- Panning has a little inertia; zooming eases.
- The node being explored gets a soft pulsing highlight, and its path back to the center lights
  up and flows faster so the reader never loses their place.
- Honor reduced-motion preferences: drop the drift and flow, keep quick fades.

**It is the navigation hub.** Every node is clickable and opens that topic in a detail panel (a
side drawer on desktop, a bottom sheet on mobile): the plain-language explanation, the visual or
chart for that idea, and jump-links to its principle card, case study, and retrieval challenge.
The reader starts zoomed out on the thesis, opens the limbs they care about, dives into a topic,
and comes back to the map. Give each limb its own accent color so the map reads as colorful.

The full animated, four-level component spec (nodes per level, animated edges, canvas physics,
detail panel) is in the design system, section 7.6. Follow it.

### Method 2: Compression Through Abstraction → Principle Cards

Identify the 3–7 generative principles that carry most of the book's intellectual value. For
each principle, create a swipeable card containing:

- **Headline:** The principle in one sentence (≤15 words).
- **Explanation:** A plain-language paragraph (3–5 sentences) in the reader's vocabulary.
- **"Reconstruct the details" expander:** An optional section the reader can open to see what
  details this principle predicts or explains. This proves the abstraction works.

The card format forces compression. If you can't fit it on a card, you haven't compressed enough.

### Method 3: Dual Coding → Annotated Visual Frameworks

For every major concept, create a real visual, not a paragraph with an icon glued on top. The
picture carries the idea; the words back it up. This is where the companion earns its keep as
something you look at, not just read. Lean into graphics here.

Each visual should be interactive: hover or tap a part to reveal what it means. The reader
takes in the spatial structure first, then drills into the words.

Match the visual to the shape of the idea:
- Processes and loops → flowchart or cycle diagram
- Trade-offs → 2×2 matrix
- Comparisons → side-by-side, Venn, or a before/after split
- Hierarchies → tree diagram
- Progressions → timeline or funnel
- Quantities, proportions, or change over time → an actual chart (bar, line, donut, or a
  pictograph built from repeated icons)
- A single striking number → a big stat callout with a one-line so-what underneath
- A part-of-a-whole or ranking → a labeled infographic, not a sentence

Aim for several genuine data visuals or infographics across the companion, not one token
diagram. If a concept involves a number, a ratio, a trend, or a breakdown, draw it. See the
data visualization and infographic sections of the design system for exact chart specs, and
use emoji, icons, and small illustrations freely to make each visual read at a glance.

### Method 4: Cognitive Load Management → Stepper Tutorial

Present the companion as a step-by-step guided experience where only one concept appears at a
time. Each step contains:

- A plain-language explanation (2–4 sentences, no jargon without immediate definition).
- A familiar analogy connecting the concept to something the reader already understands.
- A visual micro-element (icon, small diagram, or color-coded highlight).

The reader advances with a "Next" button. They can go back but cannot skip ahead on first pass.
This physically enforces the one-concept-at-a-time principle and prevents cognitive overload.

### Method 5: Concrete-Abstract-Concrete Bridge → Interactive Case Studies

For each major principle, build a three-part module:

1. **Concrete (Story):** A vivid example or scenario from the book (or generated from the
   book's logic) — written in narrative, sensory language.
2. **Abstract (Principle):** The reader is asked "What's the pattern here?" with a text input
   or multiple-choice selection. Then the principle is revealed.
3. **Concrete (Transfer):** A NEW scenario (different domain or context) where the reader must
   apply the principle. They select or type their answer, then see the model answer.

This makes the bridge active rather than passive. The reader constructs understanding rather
than receiving it.

### Method 6: Schema Activation → "What You Already Know" Opener

Before the main companion begins, present a short 3–5 question warm-up quiz. The questions
surface knowledge the reader already has that connects to the book's ideas. The questions
should be from everyday domains (work, relationships, cooking, sports, money — whatever maps
to the book's concepts).

After each answer, show a bridge sentence: "You already understand [their answer]. [Author]
argues that [book concept] works the same way." This warms up the mental shelf where new
knowledge will be stored.

### Method 7: Retrieval Practice → Flashcard & Recall Challenges

After each major section, generate:

- **Fill-in-the-blank recall:** A 2–3 sentence summary with key terms blanked out. The reader
  fills them in from memory before revealing answers.
- **Concept flashcards:** 3–5 question/answer pairs per section. Show question → reader thinks
  → clicks to reveal answer. Use the question formats: "What is...?", "Why does...?",
  "What would happen if...?", "How does X relate to Y?"
- **Chapter recap challenge:** A single open-ended question that requires synthesizing the
  whole section (e.g., "Explain [concept] to a friend using an analogy").

These are spaced throughout the experience, not dumped at the end.

### Method 8: Generation Effect → Predict-Then-Reveal Prompts

At 4–6 strategic moments in the companion, pause the flow and ask the reader to predict what
comes next before showing it. Examples:

- "The researcher tested this on 500 participants. What do you think happened?"
- "Given what you now know about [principle], what would you expect to see in [new context]?"
- "[Author] identified a major problem with the conventional approach. What do you think it is?"

The reader types or selects their prediction. Then the actual finding/argument is revealed
alongside their prediction. Highlight where they were right, and explain where they diverged.
The micro-act of generation before exposure significantly deepens encoding.

### Method 9: Serial Position Leverage → Bookend Architecture

Structure the companion so the most important ideas appear in the strongest memory positions:

- **Opening (first screen):** "This Entire Book in Three Sentences" — the absolute core
  distilled to its most potent form. This should be so good that even if the reader stops here,
  they got the essential message.
- **Closing (last screen):** "If You Remember Nothing Else" — the single most important
  takeaway, one actionable step, and a memorable closing line. Visually distinct (different
  background, larger text, framed as the crown jewel).

Everything between these bookends is valuable context, but the bookends are engineered to be
the last thing standing in memory a month later.

### Method 10: Narrative Preservation → Story Arc Timeline

When the source material has a natural narrative arc (a discovery journey, an investigation,
a transformation, a historical progression), preserve it as a visual timeline or story map:

- Each node is a turning point with a short narrative paragraph.
- Each node has an expandable "Principle extracted" box underneath.
- The reader experiences the emotional arc while collecting intellectual takeaways.

If the source material is purely expository (no narrative), skip this method and redistribute
its space to the other nine. Not every book has a story to preserve.

---

## Output Format

Produce the companion as a **single React (.jsx) artifact** saved to `/mnt/user-data/outputs/`.

### Technical Requirements

- Use React with hooks (useState, useEffect, useRef, useCallback).
- Use Tailwind CSS utility classes only (no custom CSS files).
- All state is in-memory via React state. No localStorage or sessionStorage.
- The companion must be fully self-contained in one file with a default export.
- Use `lucide-react` for icons, generously, throughout the interface.
- Use `recharts` for charts (bar, line, area, donut). For anything recharts can't do (mind
  map edges, pictographs, custom infographics), hand-build it with inline SVG.
- Use smooth transitions and micro-animations for step changes, card flips, node expansion,
  and reveals.
- The mind map must be genuinely animated: idle node drift and flowing edges via a
  `requestAnimationFrame` loop (or CSS keyframes), spring easing on expand/collapse, eased
  pan/zoom. `framer-motion` is fine if available, but CSS + rAF is enough. Gate all of it behind
  `prefers-reduced-motion`.
- Responsive: must work on both desktop and mobile viewports.
- Include a persistent navigation component (see UX Architecture below) so the reader can jump
  to any part of the companion at any time.

### Navigation — The Reader Is Never Trapped

The companion is not a one-way slideshow. It ships with a persistent navigation component that
lets the reader hop to any section at any time: the mind map, the warm-up quiz, the principles,
a specific deep dive, the predictions, the challenges, the timeline, or the final takeaway.

- **Desktop:** a slim left sidebar or a fixed top nav bar listing every section, with the
  current section highlighted and a small progress marker (a check or a filled dot) next to
  finished ones.
- **Mobile:** a fixed bottom tab bar for the main sections, plus a "jump to" menu for the rest.
- **The mind map is also navigation.** Clicking a topic node takes the reader into that topic's
  deep dive, then back to the map. Map and nav stay in sync so the reader always knows where
  they are.
- Keep the guided path as the gentle default (a "Continue" button that walks a first-timer
  through in order), but never lock it. Anyone can break out and roam via the nav. The
  first-pass "no skipping" rule from Method 4 applies only inside the stepper itself, not to the
  companion as a whole.

### Screen Flow

The default guided order, all reachable directly from the nav:

```
1. Title Screen + "The Whole Book in 3 Sentences" (Method 9 — opening bookend)
2. Warm-up Quiz (Method 6 — 3-5 questions)
3. Interactive Mind Map (Method 1 — the hub; click any node to open its deep dive)
4. Guided Stepper (Method 4) containing:
   - Principle Cards (Method 2)
   - Visual Frameworks, charts & infographics (Method 3)
   - Case Study Modules (Method 5)
   - Predict-Then-Reveal Prompts (Method 8)
   - Retrieval Challenges after each section (Method 7)
5. Story Arc Timeline (Method 10 — if the material has a narrative)
6. Final Recall Challenge (Method 7 — comprehensive)
7. "If You Remember Nothing Else" (Method 9 — closing bookend)
```

The persistent nav sits above all of this. A reader can land on the mind map, click into one
idea, take its quiz, then jump straight to the takeaway if they want.

### Design Direction

Read `references/design-system.md` thoroughly before writing any JSX. It contains the complete
design system with exact hex values, spacing tokens, component specs, shadow system, border
radius rules, typography scale, interaction states, animation timing, and anti-patterns. The
design system is derived from best-in-class learning and wellness interfaces and follows five
core principles:

1. **Soft periwinkle canvas** (#E0E4F7) — never pure white backgrounds. Cards and charts float on it.
2. **Card-first, and cards are colorful** — content lives in cards with generous radius
   (rounded-2xl), soft shadows, ample padding. But cards are not all white: grids of vivid
   pastel cards (yellow, blue, pink, lavender) sit side by side, with black feature cards for
   punch, exactly like the reference dashboards.
3. **Graphical by default** — charts, donuts, progress rings, timelines, colored stat grids,
   icons in colored circles, mascots, and line-art doodles do the teaching. Reach for a visual
   before a paragraph.
4. **Color is loud and functional** — each method keeps its signature accent, but the palette is
   used generously and all at once. A single screen routinely shows four or five accents. That
   is the look.
5. **Playful personality** — pill shapes, emoji anchors, 3D-style avatars, doodle illustrations,
   and witty copy. Warm and fun, not a textbook.

Every hex value, every shadow spec, every component variant, every reference pattern (stat-card
grid, black feature card, floating pill nav, gantt timeline), every animation, every
anti-pattern is in the design system file. Follow it literally.

**Teach with real depth, made vivid by visuals. Hold both, and if forced, choose understanding.**
Think like an experienced educator who knows the science of learning. The job is not to present
the book in a pretty interactive way; it is to make the reader genuinely understand it. That
means every idea gets a thorough, plain-language explanation of what it is, why and how it works,
and at least one concrete worked example. Do not miss the details. A screen that shows a concept
as a headline and a chart but never actually explains it has failed, no matter how good it looks.

At the same time, do not dump gray walls of text. Structure and illustrate the substance so it
invites reading: use charts, diagrams, the mind map, stat call-outs, colored cards, and
whitespace to organize dense material and give the eye somewhere to rest. Word and image work
together (dual coding); neither carries the load alone. An overview screen can be visual and
punchy; the deeper "read" and mind-map-node screens should be substantial, with full explanation
and examples. The old instruction to "overcorrect toward visuals" was wrong and produced thin,
shallow output. Correct it: rich explanation first, made navigable and engaging by strong
visuals. Aim for what a great teacher produces, not a dashboard and not a textbook.

**Design to win an award, not just to be clean.** The bar is Awwwards Site of the Day. Judge
your own build on the four criteria an Awwwards jury uses: Design (40%), Usability (20%),
Creativity (20%), Content (20%). That means award-level craft, all detailed in the design system:
fluid, tightly-tracked kinetic typography (not fixed 36px headings); a real motion system on the
exact easing curves (`--ease-out` `cubic-bezier(0.16,1,0.3,1)`, spring, in-out) with a load-in
sequence, counting stats, scroll/view reveals, and drawing charts; generous, varied negative
space and section rhythm; considered neutrals and never pure black or white; and a few signature
details (a finish moment, crisp focus states, polished empty states). Generic is failure: if a
screen could be any app's screen, it isn't done. See design-system section 18 for the full
award-level craft guide and the self-score rubric, and hold the output to it.

### Write Like a Human, Not a Textbook

All the copy in the companion — explanations, quiz prompts, card headlines, button labels,
the bookends — should read like a sharp friend talking to you, not like an AI narrating a
report. This matters as much as the visuals. Concretely:

- Vary your sentence length. A short punchy line. Then a longer one that takes its time. Mixing
  the rhythm is what makes writing sound human.
- Have a point of view. React to the ideas instead of neutrally listing them. "This one is
  genuinely counterintuitive" beats "This is an important concept."
- Talk to the reader as "you." Ask real questions. Sound curious, not ceremonial.
- Cut the AI vocabulary: delve, tapestry, testament, underscore, pivotal, crucial, vibrant,
  landscape, realm, showcase, leverage, foster, seamless, robust. If a word sounds like a
  press release, drop it.
- No em dashes or en dashes in the copy. Use a period, a comma, a colon, or parentheses.
- Skip the padding: no "it's not just X, it's Y," no forced groups of three, no "-ing" tails
  glued on to sound deep ("...highlighting its importance"), no "in order to" when "to" works.
- Say the thing plainly. "Most people get this backwards" lands harder than "It is worth noting
  that a common misconception exists."

Note the split: keep emojis, icons, and graphics in the visual design (they belong there), but
keep them out of the prose itself. A big emoji on a stat card is design. An emoji in the middle
of a sentence is clutter.

---

## Process: Step by Step

Follow this sequence every time:

### Step 1: Deep Read and Analysis

Read the entire source material. As you read, identify:

- The central thesis (one sentence).
- The causal chain (the logical structure connecting the major ideas).
- The 3–7 generative principles (the ideas with the highest explanatory power).
- The best examples and case studies (the most vivid, memorable illustrations).
- The boundary conditions (where the ideas apply and where they don't).
- The narrative arc (if one exists).
- Domains for schema activation (what everyday knowledge connects to these ideas).

### Step 2: Architecture Planning

Before writing any code, plan the companion structure in your thinking:

- Write the "Book in 3 Sentences" opening bookend.
- Write the "If You Remember Nothing Else" closing bookend.
- Map each principle to its visual format (flowchart, matrix, etc.).
- Design the schema activation quiz questions and bridge sentences.
- Identify the 4–6 best moments for predict-then-reveal prompts.
- Plan the case study modules (concrete → abstract → concrete).
- Draft the retrieval challenges for each section.

### Step 3: Build the Artifact

Read `/mnt/skills/public/frontend-design/SKILL.md` for design guidance, then build the React
artifact following the UX architecture above. The artifact should be substantial — a genuine
learning experience, not a thin wrapper around bullet points.

### Step 4: Test everything — do not skip this

**The companion is not done when it is written. It is done when it is verified.** This is a hard
gate, not a nice-to-have. Reviewers keep finding bugs that a proper test pass would have caught:
a mind map whose nodes did not respond to clicks because the pan handler was swallowing the
event, charts rendering empty, a nav item that went nowhere. Never present a companion you have
not driven.

Read `references/qa-checklist.md` and follow it:

1. **Build a test plan specific to this companion.** Copy the master checklist and fill in the
   real components you built: list every nav item, every mind map node, every quiz, every chart.
   A generic pass is not enough; enumerate the actual flows, sections, and components.
2. **Verify every item.**
   - If you can run a browser (you are in Claude Code or have a browser tool): serve the file,
     open it, and actually drive it. Click every nav item, expand every mind map branch at all
     four levels, open and close every detail panel, answer every quiz, submit, resize to a
     375px mobile viewport, toggle reduced motion. Read the console after each interaction. A
     clean first render is not a pass; a driven interaction with a clean console is.
   - If you cannot run a browser: trace every interaction through the code as an adversary. For
     each handler, confirm it is actually reachable (nothing overlays it, nothing captures the
     pointer first, it is not `pointer-events:none`), that it reads and writes the right state,
     and that the state renders. Read the code trying to make each control fail.
3. **Fix and re-test.** Any failure: fix it, then re-verify the affected checks (a fix can break
   something else). 
4. **Loop until green.** Do not stop at "mostly works" and do not ship a known bug with a caveat.
   Keep fixing and re-testing until every applicable box is checked.

Only when the checklist is fully green do you move on. Track it with a real checklist (for
example TodoWrite) so nothing is skipped.

### Step 5: Present to the User

Save to `/mnt/user-data/outputs/[book-name]-companion.jsx` and present the file. Give a brief
orientation: what the companion contains, how to navigate it, and roughly how long it takes.
State the test result honestly: what you verified, whether you drove it live or traced it by
hand, and confirm the console was clean. If a real environmental limit blocked one check, name
that check specifically rather than glossing over it.

---

## Quality Standards

Every companion must pass these checks:

- [ ] Opening bookend would give someone the core message even if they read nothing else
- [ ] Schema activation quiz uses genuinely familiar domains, not the book's own jargon
- [ ] A reader would genuinely UNDERSTAND each major idea after using the companion: every
      concept has a real explanation of what it is and why/how it works, plus a concrete worked
      example. Nothing is left as a headline and a chart. Depth is present, details are not skipped.
- [ ] The mind map is a top-down (or clearly hierarchical) tree that ANIMATES (idle drift,
      flowing edges, spring expand) and branches four logical levels deep (thesis → idea →
      subtopic → detail)
- [ ] Opening any mind-map node gives a substantial mini-lesson (multi-paragraph explanation +
      a worked example + takeaway), not a one-line label
- [ ] A persistent navigation lets the reader jump to any section from anywhere
- [ ] Each principle card passes the "could I reconstruct the details from this?" test
- [ ] Visuals and text work together (dual coding): every graphic is anchored to real
      explanation, and dense text is structured and illustrated, not a gray wall
- [ ] The look matches the reference dashboards: colored card grids, black feature cards,
      pill nav/chips, mascot or line-art illustrations, dense charts
- [ ] Icons, emojis-as-anchors, and small graphics carry meaning throughout the interface
- [ ] Stepper introduces exactly one new concept per step
- [ ] Case studies have genuinely different domains for the transfer example
- [ ] Predict-then-reveal prompts are placed at moments of genuine surprise or insight
- [ ] Retrieval challenges require actual recall, not recognition from visible text
- [ ] Closing bookend is distinct from the opening: fresh language, actionable, memorable
- [ ] The copy sounds like a person talking, with no AI-vocabulary and no em dashes
- [ ] The full experience takes 15-30 minutes to complete (for a full book)
- [ ] No jargon appears without an immediate plain-language definition or analogy
- [ ] The companion works on mobile viewports

**Final gate — two parts, both required:**

1. **Functional QA** (`references/qa-checklist.md`) is fully green: every section, flow, and
   component tested (driven live where possible, traced by hand otherwise), console clean, no
   known bugs. A companion that looks right but has a dead button, an unclickable node, or an
   empty chart has failed.
2. **Design self-score** (design-system section 18.4): honestly rate the build on the four
   Awwwards axes — Design, Usability, Creativity, Content. If any axis would not make an awards
   jury nod, it is not done. Refine the typography, spacing, motion, and distinctiveness until it
   reads as award-level, then ship. A competent-but-generic build has failed the design bar even
   if every button works.

---

## Handling Different Content Lengths

| Source Type | Companion Scope |
|---|---|
| Full nonfiction book | All 10 methods, 5–7 principles, full stepper |
| Long article (3,000+ words) | All 10 methods, 3–5 principles, shorter stepper |
| Short article/blog (500–3,000 words) | Methods 1,2,3,5,7,9 — skip stepper, lighter treatment |
| Research paper | All 10 methods, emphasize Method 3 (visuals) and Method 5 (case studies) |
| Textbook chapter | All 10 methods, emphasize Method 7 (retrieval) and Method 4 (stepper) |

Scale the depth of each method to match the source material. A 500-word blog post doesn't need
six predict-then-reveal prompts — but it does benefit from a mind map, principle cards, one
case study module, a retrieval challenge, and strong bookends.

---

## Common Pitfalls to Avoid

- **Passive summaries dressed as interactivity.** If the reader can get through the whole
  companion without thinking or doing anything, it's a summary, not a companion. Every screen
  should require engagement.
- **Generic quiz questions.** "What was the main point of chapter 3?" is lazy. "If you applied
  [principle] to [new scenario], what would you expect to happen?" is what we want.
- **Diagram for the sake of diagrams.** Only create a visual when the concept has genuine
  spatial, relational, or structural properties. A timeline for a single event is pointless.
- **Overwhelming the stepper.** If a step has more than 4 sentences of new content, it's too
  dense. Split it.
- **Forgetting the emotional arc.** Learning is emotional. The companion should have moments of
  surprise, recognition, challenge, and satisfaction. Monotone delivery kills engagement.
- **Over-building for short content.** Match companion complexity to source length. A 1,000-word
  article gets a lean companion. Don't pad.
- **Walls of text.** If a screen is all paragraphs and cards with no chart, diagram, or graphic,
  redesign it. The companion should look like an illustrated guide, not a document.
- **A mind map that's secretly a list.** Tabs, accordions, or a column of cards labeled "mind
  map" don't count. It has to be nodes connected by lines that you can click into.
- **Robotic copy.** If the text reads like an AI wrote it (even copy sitting on a beautiful
  screen), the spell breaks. Run the voice guidance over every line.
