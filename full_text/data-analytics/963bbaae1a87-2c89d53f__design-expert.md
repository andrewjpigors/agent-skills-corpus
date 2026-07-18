---
name: design-expert
description: Build, review, plan, and write interfaces with craft and evidence. Use for design reviews, UX critiques, accessibility audits, dashboard or admin builds, brand surfaces, and any product surface where defaults are unacceptable. Catches AI-generated slop; cites NNg heuristics, Universal Design 7, and a curated pantheon of historical designers; teaches the WHY of design before the HOW. Never uses emojis as UI.
version: 0.1.0
---

# design-expert

design-expert is a paragraph-first, evidence-grounded skill for interface design. It builds, reviews, plans, and writes — every action backed by Nielsen Norman Group heuristics, the Universal Design seven principles, and a curated pantheon of designers whose work survives the medium. Use it when defaults are not acceptable. Use it when "clean and modern" is not a brief. Use it when the difference between competent and signature is the difference between shipping and shipping well.

---

## The WHY of design

Design is the practice of understanding human behavior, not the practice of arranging pixels. Most of what passes for design is decoration applied to defaults — pixels first, intent later, a typeface picked because it was the last typeface picked, a color chosen because it was already in the file. Real design starts with how a specific human, in a specific moment, with a specific cognitive, emotional, and physical state, will use this thing. Pixels follow. Reverse the order and you have not designed; you have decorated a template. The interface is not the screen. The interface is the contract between the human's working memory and the system's response.

Principles outlive trends because patterns rotate every eighteen months and humans do not. Glassmorphism arrives, neumorphism arrives, bento grids arrive, brutalism arrives, then the cycle returns. None of these tell you whether your interface is good — only whether it looks contemporary, which is a smaller and stranger question. Nielsen's ten heuristics from 1994 still hold. The Universal Design seven principles from 1997 still hold. The Vignelli Canon's six-typefaces doctrine from 2010 still holds. They hold because they describe how people perceive, decide, recover from mistakes, and tolerate friction — and people have not been redesigned in fifty thousand years. Build on principles and your work ages on the schedule of human cognition. Build on patterns and your work ages on the schedule of the patterns it borrowed.

"Less is more" and "keep it simple" are not instructions. They are slogans — compressed wisdom that loses its meaning the moment a real decision shows up. The principles in this skill name that wisdom in detail: what cognitive load actually is (a working memory cap of about four items), what affordance actually requires (a signifier the user can perceive without prior training), what slop actually looks like at the CSS level (the purple-blue gradient at 135 degrees, the `transition: all 0.3s`, the rocket icon next to "Launch"). The detail survives contact with real decisions. The slogan does not.

Interface design is harder than industrial or graphic design because it must respect cognitive load, attention, motor capability, and emotional state simultaneously, across two registers — brand and product — that demand opposite things. A brand surface trades familiarity for memorability; a product surface trades memorability for earned familiarity. Get the register wrong and every rule applies wrong. The same heuristic carries different weight on a launch hero than on a settings panel.

Generic equals failure. If another model, given a similar prompt, produces substantially the same output, this skill failed. Sameness is the AI default failure mode; signature is the goal. Every rule downstream — the four craft tests, the ten lenses, the named anti-slop replacements, the iconography discipline, the type system — exists in service of producing work that could only be *this* product, for *this* person, doing *this* job. The interface that survives the next year of generative tooling will be the interface that could not have come from anywhere else.

---

## What good design looks like vs. what bad design looks like

Good design is felt as inevitable. The user closes the laptop and says "that was nice to use" without being able to articulate why. The why was the craft — the whisper-quiet surface elevation, the four-step text hierarchy, the empty state that taught instead of stalled, the focus ring that earned its place, the error message that named the recovery in the user's words. Bad design draws attention to itself. Good design says nothing and the user gets their work done. The squint test sorts the two: blur the screen and watch what survives.

Good design has signature. Bad design is interchangeable. A great interface has at least five elements that could only exist in this product, for this domain, for these users — the shape of the status pill, the temperature of the empty inbox, the chip pattern for filters, the way the metric card encodes a delta. A generic interface has none. It is a template with this particular logo on it. The four craft tests in `craft.md` — swap, squint, signature, token — are how you tell the difference before the user has to.

| Good | Bad |
|---|---|
| Specific colors drawn from the product's domain | Purple-blue gradient at 135 degrees |
| Five elements that could only exist in this product | Five elements that look like every dashboard |
| One status pill per row in its own column | Status crammed next to the title |
| Empty states with WHAT / WHY / ACTION | "No data available." centered in a card |
| Verb-plus-object button labels ("Approve invoice") | OK / Cancel / Submit |
| Inline validation on blur, with WHAT / WHY / HOW errors | Validation on submit, "Invalid input." |
| Icons at one stroke weight | Emojis, mixed icon families, sparkle for AI |
| Subtle layering — each level a few percent off the last | Glassmorphism on a static dashboard |
| Off-black `#09090b` background | Pure `#000000` background |
| Tinted neutrals leaning toward the brand hue | Pure gray with zero chroma |

---

## How to use this skill

The skill is a layered system. The index files — this `SKILL.md`, `design-gods.md`, `references.md`, `library.md`, `styles.md` — are the fast scan layer; you read them to know what is available and which depth file to load next. The depth files — `foundations.md`, `craft.md`, `anti-slop.md`, `typography.md`, `components.md`, `interaction.md`, `output-format.md` — are the substance; you load them when a current decision touches their territory. The style files — `styles/<style>.md` — are register-conditional; you load the relevant style file *before* the foundationals when the active register has a style file (today: `styles/editorial.md` when the register is editorial). The sub-skills — `/design-expert:build`, `:review`, `:plan`, `:write` — orchestrate workflows that load the right depth files in the right order, gating each step against the foundations so the discipline sticks. When in doubt about where to start, run a sub-skill. The sub-skill enforces what loose work forgets.

**Register is the second gate.** Before any visual decision, confirm the register: brand, product, or editorial. The Register check is the second gate in `/design-expert:build`, the first gate in `/design-expert:plan`, and the first step in `/design-expert:review`. Sub-skills enforce it via `AskUserQuestion` if confidence on the register sits below 80%. Once confirmed, the relevant style file (today, `styles/editorial.md` for editorial) is loaded and overrides any conflicting product-default in the foundationals.

**Layout is the third gate.** Right after register, walk the layout catalog in `layouts.md` and present at least three candidate patterns from the relevant register's table — eight editorial patterns, eight dashboard patterns, eight interface patterns, eight landing patterns. Present each candidate's name, one-line when-to-use filtered to the brief's verb, one-line trade-off, and an exemplar. Ask the user to pick before any pixel decision. Layout cascades into every grid, type, density, color, and motion choice that follows; picking the wrong one means every later decision pays a tax. **Redesigns count as early in a project** — when the brief is "redesign," walk the catalog cold rather than preserving the existing layout by default. The most common redesign failure mode is treating the original layout as the constraint when the original layout is precisely what the redesign needs to escape.

**Read the size of the request before applying any workflow.** Most design work is iteration — middle-ground requests where the user wants something between a critique and a redesign. Users rarely say *"iterate"*; they say *"review," "make it better," "what would you change."* Read the size of the request — touch-up, polish, iteration, surface redesign, system redesign — before deciding which command to run and how much exploration to do. The sizing framework lives in `craft.md` § Iteration as a category. Get the size right and exploration matches the work; get the size wrong and you either over-engineer a touch-up or under-engineer a layout problem. The size sets the number of alternatives to propose, the number of design-gods to consult, and the reference files to load.

---

## Communication conventions

Sub-skills (`/design-expert:plan`, `:build`, `:review`, `:write`) operate in two question modes: structured questions via `AskUserQuestion` (for binary or option-list choices), and free-form questions inline in chat (for open answers). Both modes follow consistent visual conventions so the user can scan a long planner response and find the questions without re-reading the prose.

**Free-form questions use the orange-question convention.** Every inline question is marked with a blockquote, an orange-disc emoji, and a bold "Question" tag, in this exact form:

> 🟠 **Question** — [the question text, on one line if possible]

The orange disc (🟠) renders as visible orange across platforms; the blockquote sets the question apart from prose; the bold "Question" tag makes the line scannable. The convention applies universally — every sub-skill, every gate, every free-form question. Compound questions split into multiple blockquotes, one question per block, so each lands separately and can be answered separately.

**Structured questions use `AskUserQuestion`.** The tool already provides its own visual treatment (a permission card with options); the orange-question convention does not apply inside structured-question UI. Use `AskUserQuestion` whenever the user is picking from 2–4 mutually exclusive options; use the orange-question blockquote when the answer is open-ended (a sentence, a name, a paragraph, an essay-shaped reply).

The visual contract is non-negotiable. A planner response that asks four questions in flowing prose without orange-question markers is a planner response that loses three of the four answers, because the user reads the response once and only catches the questions that visually called out for an answer. Mark every question.

Context economy matters. The full skill is dense and loading it all for every task is wasteful. The sub-skills load the minimum required files for their workflow. When working freely without a sub-skill, load this `SKILL.md` plus the most relevant depth file or two for the surface — `craft.md` plus `anti-slop.md` for visual review, `components.md` for atomic patterns, `output-format.md` for review formatting, `grids.md` whenever a layout decision is being made, the relevant `library/<category>/README.md` when the surface type has a curated do-and-don't file, the relevant `styles/<style>.md` when the register has a style file. Skim the index, deepen on demand. Carrying every file in working memory dilutes attention; loading the wrong file dilutes craft.

---

## The grid is the deepest layer

Most interfaces that feel sloppy are not sloppy in a single visible way. They are sloppy because no grid was committed to, or a grid was committed to and then quietly abandoned by the third screen. The reader of an interface does not see the grid. They see the consequences of its absence — gutters that drift between sections, type that does not align across columns, paddings that round to slightly different values, hero images that sit one or two pixels off where they should be. None of those failures is loud. All of them, together, are why a product reads as casual.

Pick the grid before placing the first element. Not "we'll use a grid" — pick it: the column count, the gutter token, the canvas margin, the baseline, the breakpoints, and the maximum container width. Write it down somewhere a reviewer can see — in `system.md`, in the design tokens, in the project's PRODUCT.md, in a comment at the top of the page component. Then commit. Every later spacing value, every later component padding, every later vertical rhythm decision derives from the grid you picked. If you find yourself reaching for an inline pixel value instead of a grid token, the grid is being abandoned. Stop and snap back to the system.

The grid behaves differently across registers. **Brand surfaces** (landing pages, campaigns, marketing heroes) take fluid grids — column widths and gutters that scale with viewport via `clamp()`, asymmetric layouts where one element clearly leads. **Product surfaces** (dashboards, settings, admin, authenticated workspaces) take fixed grids — column widths in pixels, gutters in pixels, type that does not drift with viewport because the user lives in this layout for hours and spatial predictability is the property that makes the work navigable. Mixing the registers is the most common error: a marketing-page grid applied to a settings panel, a product-page grid applied to a hero. Pick the register, pick the grid, commit to both.

The depth lives in `grids.md`. The pantheon voices for grids are `design-gods/muller-brockmann.md` (the Swiss codification, the symmetric/mathematical register) and `design-gods/jan-tschichold.md` (the asymmetric register, *Die neue Typographie*, then the Penguin reversal — both halves apply on a screen). Load `grids.md` whenever a layout decision is on the table; load the two designers when the decision is structural enough to need their argument behind it. Reviews must include a grid lens — see `commands/review.md` for the procedure.

---

## Consulting the design-gods

The pantheon is not decoration. Each designer's file in `design-gods/` carries a working principle that survives the medium, and ignoring them is how the work drifts back to defaults. Default to consulting more, not fewer. The cost of over-consulting is a few hundred tokens; the cost of under-consulting is templated work shipped under your name.

The threshold is sized to the work:

- **Trivial — zero gods required.** A single button label, a one-color tweak, a one-line copy edit, a one-icon swap. Consultation here is theater.
- **Small — one god, optional.** A single contained component: a modal, a card, a form field, a status pill, an isolated hover treatment. Consult one designer if their principle is clearly load-bearing; otherwise skip without ceremony.
- **Medium — two gods minimum, three preferred.** A feature surface that holds multiple components or that touches more than one screen — a settings panel, a dashboard section, a marketing hero, a navigation system, a populated empty state, a content-rich card grid. Two consultations are the floor; three are the bar. Building medium-sized work with one or zero gods is allowed only when you can name in writing why no second voice could improve the decision — and that note belongs in your working output.
- **Large — three gods, no exceptions.** A full page, a full flow, a system-level decision (token system, type scale, component library). Anything below three voices is insufficient on a surface that touches this many later decisions.

If you cannot pick two relevant gods, the file index in `design-gods.md` exists for exactly that — scan the capsules, identify which voices speak to the surface, and load those depth files. "I couldn't think of one" is not a defensible answer when a thirteen-designer index sits one file away.

### How to consult

To consult a designer, do four things, in order:

1. **Load** their depth file: `design-gods/<key>.md` (e.g., `design-gods/rams.md`, `design-gods/muriel-cooper.md`).
2. **Read** the "Why they matter" and "Principles they brought" sections at minimum. Skim "Quotes" for a phrase you can apply by reflex.
3. **Apply** — name the specific principle you are taking from them and the specific decision it shapes. Generic invocations ("I consulted Rams") do not count; the consultation must produce a sentence of the form "Per Rams' eighth principle, I removed the third elevation level on the card."
4. **Log** the consultation. See the counter section below.

### Usage counter

Every consultation must append one line to the usage log so we can see which voices are actually being used over time, and which are being neglected. The counter is honest only if you log every consultation. Failing to log is the same as failing to consult — you cannot improve what you cannot measure.

**Log file:** `~/.claude/design-expert/usage-log.jsonl` (create the directory on first write).

**Format:** one JSON object per line, no pretty-printing, UTC timestamp:

```
{"ts":"<ISO 8601 UTC>","god":"<key>","command":"<build|review|plan|write|other>","project":"<basename of cwd>"}
```

**How to write:** append using the Bash tool with `>>` redirection. Always create the directory first; always include the trailing newline:

```bash
mkdir -p ~/.claude/design-expert && \
printf '%s\n' '{"ts":"2026-05-02T15:30:00Z","god":"rams","command":"build","project":"khev-portfolio"}' \
  >> ~/.claude/design-expert/usage-log.jsonl
```

**How to inspect** the counts at any time, ranked by frequency:

```bash
jq -r '.god' ~/.claude/design-expert/usage-log.jsonl | sort | uniq -c | sort -rn
```

Or by command:

```bash
jq -r '.command + " · " + .god' ~/.claude/design-expert/usage-log.jsonl | sort | uniq -c | sort -rn
```

The keys are stable across the skill: `rams`, `vignelli`, `ive`, `kare`, `rand`, `norman`, `nielsen`, `eames`, `victor`, `corum`, `tufte`, `cooper`, `frere-jones`, `muriel-cooper`, `scher`, `muller-brockmann`, `jan-tschichold`. Use the same key as the filename in `design-gods/`.

---

## File index

The full set of files in this skill, with paths, one-line descriptions, and tags. Tags are canonical across the index files so cross-referencing works in one pass.

### Manifesto and foundation files

| File | What it covers | Tags |
|---|---|---|
| `SKILL.md` | This file. The manifesto, the index, and the how-to-use. | `#manifesto` `#index` |
| `foundations.md` | The ten NNg heuristics, the Universal Design 7 principles, and the 10-Lens decision framework. | `#principles` `#heuristics` `#accessibility` |
| `craft.md` | Composition, layering, density, color, the four craft tests, distillation, polish. Editorial layouts moved to `styles/editorial.md`; craft retains a stub pointer. | `#craft` `#visual` `#layering` |
| `grids.md` | The Swiss school, asymmetric grids, types of grids, spacing systems, container/columns/gutters/baselines, brand/product/editorial registers, when to break. | `#grid` `#systems` `#spacing` `#editorial` |
| `layouts.md` | The 32-pattern layout catalog organized by register: 8 editorial + 8 dashboard + 8 interface + 8 landing patterns. Each with name, when-to-use, structure, exemplar, refusal-condition. The lookup loaded at the layout-exploration gate. | `#layouts` `#composition` `#patterns` |
| `anti-slop.md` | Detecting and replacing AI-generated defaults; the six tells; named replacements; grep recipes. | `#anti-defaultism` `#patterns` |
| `typography.md` | Type system, hierarchy levels, 38 pairings, brand-vs-product-vs-editorial type rules. | `#typography` `#fonts` `#editorial` |
| `components.md` | Atomic patterns: cells, status pills, icons, charts, forms, navigation. | `#components` `#patterns` |
| `interaction.md` | The eight states, motion timing, responsive design, onboarding, delight, reduced motion. | `#interaction` `#motion` `#states` |
| `output-format.md` | Review template, confidence framework, five-dimension audit format, citation format. | `#review` `#format` |
| `self-review.md` | End-of-work review discipline. Anti-slop self-scan, four craft tests, register-conditional verdict, voice consistency, image-rhythm honesty, honest cut-list, final polish. Produces a Cuts / Holds / Risks report. Loaded at the close of medium-to-long iterations and builds. | `#review` `#discipline` `#self-audit` |

### Pantheon — historical designers

| File | What it covers | Tags |
|---|---|---|
| `design-gods.md` | The pantheon index — sixteen designers with capsules and tags pointing into per-designer files. | `#history` `#principles` |
| `design-gods/<slug>.md` | One file per designer: Rams, Vignelli, Ive, Kare, Rand, Norman, Nielsen, Eames, Victor, Corum, Tufte, Cooper, Frere-Jones, Muriel Cooper, Müller-Brockmann, Tschichold. Tags vary per designer. | `#history` |

### Curated references — quality exemplars

| File | What it covers | Tags |
|---|---|---|
| `references.md` | The references index — eight working systems and canonical texts with rationale. | `#references` `#exemplars` |
| `references/<slug>.md` | One file per reference: Pentagram, IBM Carbon, Apple HIG, Linear, Stripe, Refactoring UI, Vignelli Canon, Material 3, Grid Systems. | `#reference` |
| `references/nng-articles-index.md` | 270+ NNg articles indexed by topic for fast citation lookup. | `#lookup` `#nng` |

### Curated library — Do / Don't research

| File | What it covers | Tags |
|---|---|---|
| `library.md` | The library index — what good and bad versions of specific surfaces look like. | `#library` `#patterns` |
| `library/dashboards/README.md` | Do / Don't dashboards. | `#dashboards` |
| `library/navbars/README.md` | Do / Don't navbars. | `#navbars` |
| `library/components/tables/README.md` | Do / Don't tables. | `#tables` |
| `library/components/forms/README.md` | Do / Don't forms. | `#forms` |
| `library/components/empty-states/README.md` | Do / Don't empty states. | `#empty-states` |
| `library/components/cards/README.md` | Do / Don't cards. | `#cards` |

### Curated styles — register-specific disciplines

| File | What it covers | Tags |
|---|---|---|
| `styles.md` | The styles index — disciplines that govern surfaces by intent register. | `#styles` `#editorial` `#expressive` |
| `styles/editorial.md` | Editorial register — case studies, long-form, magazine pieces, museum essays, design-agency project pages. Six editorial moves, anti-patterns, when to break the rules. | `#editorial` `#style` `#case-study` |
| `styles/expressive.md` | Expressive register — avant-garde, motion-led, brand-as-product. For agency homepages, manifesto pages, product launches, awards-target work. Six expressive moves, color discipline, anti-patterns. Synthesizes Impeccable's bolder/colorize/delight/layout/craft. | `#expressive` `#style` `#brand` `#avant-garde` |

### Curated voices — writing-context disciplines

| File | What it covers | Tags |
|---|---|---|
| `voices.md` | The voices index — disciplines that govern copy by writing context (UX / long-form / marketing). | `#voices` `#writing` |
| `voices/ux-copy.md` | UX copy voice — buttons, labels, errors, empty states, confirmations, micro-copy. Strunk and White as the floor. | `#voices` `#ux-copy` |
| `voices/long-form.md` | Long-form voice — case studies, blog posts, magazine pieces, journalism. Work&Co tone + canonical exemplars (Talese, Schulz, McPhee, Didion, Coates, Wallace, Orlean, Scientific American) + pattern-formulae. | `#voices` `#long-form` `#editorial` |
| `voices/marketing/george-lois.md` | The Mad-Man voice — bold image-and-line spectacle. Esquire covers, *I Want My MTV*, Tommy Hilfiger. | `#voices` `#marketing` `#ad-lord` |
| `voices/marketing/bill-bernbach.md` | The honest-witty voice — DDB Creative Revolution. *Think Small*, *We Try Harder*, *You Don't Have to Be Jewish*. | `#voices` `#marketing` `#ad-lord` |
| `voices/marketing/howard-gossage.md` | The conversational voice — Socrates of San Francisco, anti-hard-sell. Eagle Shirts, Pink Air, Sistine-Chapel rhetoric. | `#voices` `#marketing` `#ad-lord` |
| `voices/marketing/david-ogilvy.md` | The research-led long-copy voice — *At 60 mph*, Hathaway eyepatch, Schweppes Commander, Dove, Guinness Book of Records. | `#voices` `#marketing` `#ad-lord` |

### Sub-skills — slash commands

| Command | What it does | When to use |
|---|---|---|
| `/design-expert:build` | Build new UI from intent. Gate-driven workflow with Shape, Register, Domain, and Test gates. | Building a new screen, flow, or component. |
| `/design-expert:review` | Review existing UI for craft, accessibility, and anti-slop. Walks the 10 lenses, UD7, heuristic scoring, and hardening. | Reviewing a Figma frame, a deployed surface, or a PR diff. |
| `/design-expert:plan` | Generate `PRODUCT.md` and `DESIGN.md` for a project. Loader check is mandatory — never silent overwrite. | Starting a new project; refreshing a stale brief. |
| `/design-expert:write` | Write or refine UX copy with the WHAT/WHY/HOW error formula and the acknowledge/explain/act empty-state formula. | Writing button labels, error messages, empty states, confirmations, microcopy. |

---

## Hard rules — non-negotiable

These rules never bend. They exist because each one prevents a specific class of failure observed at scale across thousands of AI-generated interfaces. The reasons are mechanical, not aesthetic; the reasons are documented in the depth files cited beside each rule.

- **No emojis as UI.** Emojis render differently across OS, browser, and font; they cannot be tinted to match the type color; their stroke weight is not yours to set; they announce inconsistently to screen readers. They are also the single loudest "AI made that" tell on a product surface. Use a single, consistent icon library. See `components.md`.
- **One icon library, one stroke weight.** Pick Lucide, Heroicons, Phosphor, Tabler, or Material Symbols at the system level and stick to it. Mixed icon families fragment the system. The canonical concept-to-icon mapping lives in `components.md`.
- **IBM Carbon defaults for enterprise and dense-data UIs.** Adapt the patterns; never blind-copy the colors. The Carbon discipline is the floor, not the ceiling. See `references/ibm-carbon.md`.
- **No pie or donut charts.** Cleveland and McGill (1984) — humans read length more accurately than angle. Bar charts win for category comparison every time. See `components.md`.
- **`prefers-reduced-motion: reduce` is mandatory.** Roughly thirty-five percent of adults over forty prefer reduced motion. Animations that ignore the preference are an accessibility failure, not a stylistic choice. See `interaction.md`.
- **44 by 44 pixel minimum touch targets** on any interactive mobile element (WCAG 2.5.5). Smaller targets fail Universal Design 7c.
- **Native `<dialog>` plus `inert` for modals.** Do not ship custom focus-trap JavaScript when the platform already does it correctly. Custom controls that do not expose ARIA roles fail Universal Design 4e.
- **Validate on blur**, never on every keystroke (annoying false errors), never only on submit (forces re-scan). The error formula is WHAT happened / WHY in user terms / HOW to fix. See `interaction.md` and `commands/write.md`.
- **Never use humor for failures, errors, or destructive confirmations.** Save warmth for empty states and celebrations. A joke at the moment of an error is the moment the user loses trust in the system. See `commands/write.md`.
- **No silent overwrite of `PRODUCT.md` or `DESIGN.md`.** The loader check in `/design-expert:plan` is mandatory. Erasing a brief is erasing the project's memory.
- **Two design-gods minimum on medium work, three preferred; three minimum on large work.** Every consultation logs to `~/.claude/design-expert/usage-log.jsonl`. See the "Consulting the design-gods" section above for the sizing definitions, the four-step consultation procedure, and the log format.
- **Pick the grid before placing the first element.** The column count, the gutter token, the canvas margin, the baseline, the breakpoints, and the maximum container width — all chosen, all written down, all committed to. Improvised grids ship templated work. See `grids.md` and the "The grid is the deepest layer" section above.
- **Free-form questions to the user use the orange-circle marker.** When the sub-skill needs a free-form answer (not a discrete choice via `AskUserQuestion`), prefix the question with the 🟠 emoji and treat the question as a Markdown blockquote so it stays visually distinct in long planner responses. Group related questions as `🟠 **Q1.**`, `🟠 **Q2.**`, `🟠 **Q3.**` so the user can answer by reference. The orange marker matches the design-expert plugin's accent color and lets the user scan a long planner response and jump straight to "what does this command actually need from me?" Convention is mandatory across all sub-skills (`/plan`, `/build`, `/review`, `/write`) — never use plain bold or numbered lists for free-form prompts when the orange-circle pattern applies.

---

## Brand vs. product vs. editorial register

Every interface lives in one of three registers, and the same rules apply differently across them. **Brand** surfaces — landing pages, marketing sites, pitch decks, campaigns, launch heroes — exist to be distinctive; they trade familiarity for memorability, and they can deliberately violate consistency (Heuristic 4) and aesthetic-minimalism (Heuristic 8) for the sake of being remembered; the user is here in-and-out under a minute. **Product** surfaces — dashboards, admin panels, settings, in-app flows, authenticated tools — exist to disappear; they trade memorability for earned familiarity and cognitive ease, and consistency is non-negotiable because the user will be in this surface for hours and any inconsistency becomes a tax compounded across every interaction. **Editorial** surfaces — case studies, long-form essays, magazine pieces, museum sites, design-agency project pages, blog posts that aspire — exist to be read; they trade efficiency for attention, density inverts (whitespace becomes the design), color recedes (monochrome chrome with color confined to artwork), and the type does the work of containment that cards do in product. The user is here for ten or twenty minutes; the page earns those minutes through type, grid, and rhythm.

Wrong register equals wrong everything downstream. The Register check is the **second gate** in `/design-expert:build` and the **first gate** in `/design-expert:plan`; sub-skills enforce it via `AskUserQuestion` if confidence on the register sits below 80%. Once the register is confirmed, the relevant style file is loaded — `styles/editorial.md` if editorial, otherwise the foundationals govern alone. See `styles/editorial.md` for the editorial register's discipline; see `commands/build.md` Gate 2 for the register-detection procedure.

---

## Closing

Design is felt, not enforced. The principles in this skill exist not to constrain but to liberate — when the floor is solid, the ceiling lifts. Read the foundations. Apply the craft. Refuse the defaults. Cite the source. Ship work that could only be yours, for this user, in this world, on this surface. That is the bar. Anything less is retrieval dressed as design.
