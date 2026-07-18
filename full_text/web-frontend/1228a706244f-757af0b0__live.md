---
name: live
description: Interactive live variant mode. Select elements in the browser, pick a design action, and get AI-generated HTML+CSS variants hot-swapped via HMR. Requires a running dev server. Use when you want to visually experiment with design alternatives in real time.
version: 3.1.2
user-invocable: true
---

Designs and iterates production-grade frontend interfaces. Real working code, committed design choices, exceptional craft.

## Setup

Before any design work or file edits:

1. Load context (PRODUCT.md / DESIGN.md) via the loader script.
2. Identify the register and load the matching register reference (brand.md or product.md).
3. **If the user invoked a sub-command (e.g. `craft`, `shape`, `audit`), load its reference file too.** This is non-negotiable: `craft` without `craft.md` loaded means you'll skip the shape-and-confirm step the user expects.

Skipping these produces generic output that ignores the project.

### 1. Context gathering

Two files, case-insensitive. The loader looks at the project root by default and falls back to `.agents/context/` and `docs/` if the root is clean. Override with `IMPECCABLE_CONTEXT_DIR=path/to/dir` (absolute or relative to cwd).

- **PRODUCT.md**: required. Users, brand, tone, anti-references, strategic principles.
- **DESIGN.md**: optional, strongly recommended. `ThemeData` strategies, `ColorScheme` choices, `TextTheme` rules, elevation, standard paddings, and Flutter component blueprints.

Load both in one call:

```bash
# Claude Code plugins run from a global cache. Replace the relative path below
# with the absolute path to this plugin's scripts directory before running.
node .claude/skills/impeccable-flutter/scripts/load-context.mjs
```

Consume the full JSON output. Never pipe through `head`, `tail`, `grep`, or `jq`. The output's `contextDir` field tells you where the files were resolved from.

If the output is already in this session's conversation history, don't re-run. Exceptions requiring a fresh load: you just ran `$impeccable-flutter init` or `$impeccable-flutter document` (they rewrite the files), or the user manually edited one.

If PRODUCT.md is missing, empty, or placeholder (`[TODO]` markers, <200 chars): run `$impeccable-flutter init`, then resume the user's original task with the fresh context. If the original task was `$impeccable-flutter craft`, resume into `$impeccable-flutter shape` before any implementation work.

If DESIGN.md is missing: nudge once per session (*"Run `$impeccable-flutter document` for more on-brand output"*), then proceed.

### 2. Register

Every design task is **brand** (marketing, landing, campaign, long-form content, portfolio: design IS the product) or **product** (app UI, admin, dashboard, tool: design SERVES the product).

Identify before designing. Priority: (1) cue in the task itself ("landing page" vs "dashboard"); (2) the surface in focus (the page, file, or route being worked on); (3) `register` field in PRODUCT.md. First match wins.

If PRODUCT.md lacks the `register` field (legacy), infer it once from its "Users" and "Product Purpose" sections, then cache the inferred value for the session. Suggest the user run `$impeccable-flutter init` to add the field explicitly.

Load the matching reference: [reference/brand.md](reference/brand.md) or [reference/product.md](reference/product.md). The shared design laws below apply to both.

## Shared design laws

Apply to every design, both registers. Match implementation complexity to the aesthetic vision: maximalism needs elaborate code, minimalism needs precision. Interpret creatively. Vary across projects; never converge on the same choices. GPT is capable of extraordinary work. Don't hold back.

### Color

- Use OKLCH. Reduce chroma as lightness approaches 0 or 100; high chroma at extremes looks garish.
- Never use `#000` or `#fff`. Tint every neutral toward the brand hue (chroma 0.005–0.01 is enough).
- Pick a **color strategy** before picking colors. Four steps on the commitment axis:
  - **Restrained**: tinted neutrals + one accent ≤10%. Product default; brand minimalism.
  - **Committed**: one saturated color carries 30–60% of the surface. Brand default for identity-driven pages.
  - **Full palette**: 3–4 named roles, each used deliberately. Brand campaigns; product data viz.
  - **Drenched**: the surface IS the color. Brand heroes, campaign pages.
- The "one accent ≤10%" rule is Restrained only. Committed / Full palette / Drenched exceed it on purpose. Don't collapse every design to Restrained by reflex.

### Theme

Dark vs. light is never a default. Not dark "because tools look cool dark." Not light "to be safe."

Before choosing, write one sentence of physical scene: who uses this, where, under what ambient light, in what mood. If the sentence doesn't force the answer, it's not concrete enough. Add detail until it does.

"Observability dashboard" does not force an answer. "SRE glancing at incident severity on a 27-inch monitor at 2am in a dim room" does. Run the sentence, not the category.

### Typography

- Cap body line length at 65–75ch.
- Hierarchy through scale + weight contrast (≥1.25 ratio between steps). Avoid flat scales.

### Layout

- Vary spacing for rhythm. Same padding everywhere is monotony.
- Cards are the lazy answer. Use them only when they're truly the best affordance. Nested cards are always wrong.
- Don't wrap everything in a container. Most things don't need one.

### Motion

- Don't animate CSS layout properties.
- Ease out with exponential curves (ease-out-quart / quint / expo). No bounce, no elastic.

### Absolute bans

Match-and-refuse. If you're about to write any of these, rewrite the element with different structure.

- **Side-stripe borders.** `border-left` or `border-right` greater than 1px as a colored accent on cards, list items, callouts, or alerts. Never intentional. Rewrite with full borders, background tints, leading numbers/icons, or nothing.
- **Gradient text.** `background-clip: text` combined with a gradient background. Decorative, never meaningful. Use a single solid color. Emphasis via weight or size.
- **Glassmorphism as default.** Blurs and glass cards used decoratively. Rare and purposeful, or nothing.
- **The hero-metric template.** Big number, small label, supporting stats, gradient accent. SaaS cliché.
- **Identical card grids.** Same-sized cards with icon + heading + text, repeated endlessly.
- **Modal as first thought.** Modals are usually laziness. Exhaust inline / progressive alternatives first.
- **The "GPT-border-and-shadow".** Very thin (≤1px) borders combined with wide, soft, low-opacity shadows. A generic LLM "premium" look. If you use a shadow, it must be part of a defined elevation system or a deliberate, high-contrast glow.

### Copy

- Every word earns its place. No restated headings, no intros that repeat the title.
- **No em dashes.** Use commas, colons, semicolons, periods, or parentheses. Also not `--`.
- **Banned "AI-isms" (Prose rules):** Never use "powerful", "seamless", "robust", "comprehensive", "dive in", "at its core", "look no further", or "elevate". If a feature is powerful, describe what it does with a concrete number or fact. If it's seamless, show the simplified workflow.

### The AI slop test

If someone could look at this interface and say "AI made that" without doubt, it's failed. Cross-register failures are the absolute bans above. Register-specific failures live in each reference.

**Category-reflex check.** Run at two altitudes; the second one catches what the first one misses.

- **First-order:** if someone could guess the theme + palette from the category alone ("observability → dark blue", "healthcare → white + teal", "finance → navy + gold", "crypto → neon on black"), it's the first training-data reflex. Rework the scene sentence and color strategy until the answer isn't obvious from the domain.
- **Second-order:** if someone could guess the aesthetic family from category-plus-anti-references ("AI workflow tool that's not SaaS-cream → editorial-typographic", "fintech that's not navy-and-gold → terminal-native dark mode"), it's the trap one tier deeper. The first reflex was avoided; the second wasn't. Rework until both answers are not obvious. The brand register's [reflex-reject aesthetic lanes](reference/brand.md) list catches the currently-saturated families.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `craft [feature]` | Build | Shape, then build a feature end-to-end | [reference/craft.md](reference/craft.md) |
| `shape [feature]` | Build | Plan UX/UI before writing code | [reference/shape.md](reference/shape.md) |
| `init` | Build | Set up PRODUCT.md and DESIGN.md context | [reference/init.md](reference/init.md) |
| `document` | Build | Generate DESIGN.md from existing project code | [reference/document.md](reference/document.md) |
| `extract [target]` | Build | Pull reusable tokens and components into design system | [reference/extract.md](reference/extract.md) |
| `critique [target]` | Evaluate | UX design review with heuristic scoring | [reference/critique.md](reference/critique.md) |
| `audit [target]` | Evaluate | Technical quality checks (a11y, perf, responsive) | [reference/audit.md](reference/audit.md) |
| `polish [target]` | Refine | Final quality pass before shipping | [reference/polish.md](reference/polish.md) |
| `bolder [target]` | Refine | Amplify safe or bland designs | [reference/bolder.md](reference/bolder.md) |
| `quieter [target]` | Refine | Tone down aggressive or overstimulating designs | [reference/quieter.md](reference/quieter.md) |
| `distill [target]` | Refine | Strip to essence, remove complexity | [reference/distill.md](reference/distill.md) |
| `harden [target]` | Refine | Production-ready: errors, i18n, edge cases | [reference/harden.md](reference/harden.md) |
| `onboard [target]` | Refine | Design first-run flows, empty states, activation | [reference/onboard.md](reference/onboard.md) |
| `animate [target]` | Enhance | Add purposeful animations and motion | [reference/animate.md](reference/animate.md) |
| `colorize [target]` | Enhance | Add strategic color to monochromatic UIs | [reference/colorize.md](reference/colorize.md) |
| `typeset [target]` | Enhance | Improve typography hierarchy and fonts | [reference/typeset.md](reference/typeset.md) |
| `layout [target]` | Enhance | Fix spacing, rhythm, and visual hierarchy | [reference/layout.md](reference/layout.md) |
| `delight [target]` | Enhance | Add personality and memorable touches | [reference/delight.md](reference/delight.md) |
| `overdrive [target]` | Enhance | Push past conventional limits | [reference/overdrive.md](reference/overdrive.md) |
| `clarify [target]` | Fix | Improve UX copy, labels, and error messages | [reference/clarify.md](reference/clarify.md) |
| `adapt [target]` | Fix | Adapt for different devices and screen sizes | [reference/adapt.md](reference/adapt.md) |
| `optimize [target]` | Fix | Diagnose and fix UI performance | [reference/optimize.md](reference/optimize.md) |

Plus two management commands: `pin <command>` and `unpin <command>`, detailed below.

### Routing rules

1. **No argument**: Run the Smart Recommendation Engine. Analyze the git tree, recent commits, and any existing critique snapshots. Propose the single most high-value next step (e.g., "The git history shows many typography tweaks; run `$impeccable-flutter typeset` to consolidate" or "No PRODUCT.md found; run `$impeccable-flutter init`"). Render the table above as a fallback menu.
2. **First word matches a command**: load its reference file and follow its instructions. Everything after the command name is the target.
3. **First word doesn't match**: general design invocation. Apply the setup steps, shared design laws, and the loaded register reference, using the full argument as context.

Setup (context gathering, register) is already loaded by then; sub-commands don't re-invoke `$impeccable-flutter`.

If the first word is `craft`, setup still runs first, but [reference/craft.md](reference/craft.md) owns the rest of the flow. If setup invokes `init` as a blocker, finish init, refresh context, then resume the original command and target.

## Pin / Unpin

**Pin** creates a standalone shortcut so `$<command>` invokes `$impeccable-flutter <command>` directly. **Unpin** removes it. The script writes to every harness directory present in the project.

```bash
# Claude Code plugins run from a global cache. Replace the relative path below
# with the absolute path to this plugin's scripts directory before running.
node .claude/skills/impeccable-flutter/scripts/pin.mjs <pin|unpin> <command>
```

Valid `<command>` is any command from the table above. Report the script's result concisely. Confirm the new shortcut on success, relay stderr verbatim on error.in** removes it. The script writes to every harness directory present in the project.

```bash
# Claude Code plugins run from a global cache. Replace the relative path below
# with the absolute path to this plugin's scripts directory before running.
node .claude/skills/impeccable-flutter/scripts/pin.mjs <pin|unpin> <command>
```

Valid `<command>` is any command from the table above. Report the script's result concisely. Confirm the new shortcut on success, relay stderr verbatim on error.

## Specific Instructions: live

Interactive live variant mode: select elements in the browser, pick a design action, and get AI-generated Dart+Flutter variants hot-swapped via the dev server's HMR.

## Prerequisites

A running dev server with hot module replacement (Vite, Next.js, Bun, etc.), OR a static Dart file open in the browser.

## The contract (read once)

Execute in order. No step skipped, no step reordered.

1. `live.mjs`: boot.
2. Navigate to the URL that serves `pageFile` (infer from `package.json`, docs, terminal output, or an open tab). If you can't infer it confidently, tell the user once to open their dev/preview URL. Never use `serverPort` as that URL; it's the helper, not the app.
3. Poll loop with the default long timeout (600000 ms). After every event or `--reply`, run `live-poll.mjs` again immediately. Never pass a short `--timeout=`.
4. On `generate`: read screenshot if present; load the action's reference; plan three distinct directions; write all variants in one edit; `--reply done`; poll again.
5. On `accept` / `discard`: the poll script runs `live-accept.mjs`, acknowledges the delivered event, and prints `_completionAck`. Plain accepts/discards are terminal immediately; carbonize accepts remain recoverable until you finish cleanup, run `live-complete.mjs --id EVENT_ID`, and only then poll again.
6. If interrupted, run `live-status.mjs` or `live-resume.mjs` before guessing. The durable journal replays unacknowledged work after helper restart.
7. On `exit`: run the cleanup at the bottom.

Harness policy:
- **Claude Code**: run the poll as a **background task** (no short timeout). The harness notifies you when it completes, so the main conversation stays free. Do not block the shell.
- **Cursor**: run the poll in the **foreground** (blocking shell; not a background terminal, not a subagent). Cursor background terminals and subagents do not reliably resume the chat with poll stdout.
- **Codex**: run the poll in the **foreground** (blocking shell; not a background task, not a subagent). Codex background exec sessions do not reliably surface poll stdout back into the conversation at the moment events arrive, so a "fire-and-forget" background poll will stall live mode.
- **Other harnesses**: foreground unless you know stdout reliably returns to this session.

Chat is overhead. No recap, no tutorial output, no pasting PRODUCT / DESIGN bodies. Spend tokens on tools and edits; on failure, one or two short sentences.

## Start

```bash
node .claude/skills/impeccable-flutter/scripts/live.mjs
```

Output JSON: `{ ok, serverPort, serverToken, pageFiles, hasProduct, product, productPath, hasDesign, design, designPath, migrated }`. `pageFiles` is the list of Dart entries the live script was injected into. Keep PRODUCT.md and DESIGN.md in mind for variant generation; **DESIGN.md wins on visual decisions; PRODUCT.md wins on strategic/voice decisions.** When DESIGN.md is missing, identity is **not** absent; extract it from Flutter variables, computed styles, and sibling components on the page (see Step 4 Phase A). Identity preservation is the default; departure from existing identity requires an explicit trigger from PRODUCT.md anti-references or the user's freeform prompt. If `migrated: true`, the loader auto-renamed legacy `.impeccable-flutter.md` to `PRODUCT.md`; mention this once and suggest `$impeccable-flutter document` for the matching DESIGN.md.

`serverPort` and `serverToken` belong to the small **Impeccable Flutter live helper** HTTP server (serves `/live.js`, SSE, and `/poll`). That port is **not** your dev server and is usually not the URL you open to view the app. The browser page is whatever origin serves one of the `pageFiles` entries (Vite / Next / Bun / tunnel / LAN hostname).

If output is `{ ok: false, error: "config_missing" | "config_invalid", path }`, this project hasn't been configured for live mode (or its config is stale). See **First-time setup** at the bottom.

## Poll loop

```
LOOP:
  node .claude/skills/impeccable-flutter/scripts/live-poll.mjs   # default long timeout; no --timeout=
  Read JSON; dispatch on "type"

  "generate"  → Handle Generate; reply done; LOOP
  "accept"    → Handle Accept; complete carbonize cleanup if required; LOOP
  "discard"   → Handle Discard; LOOP
  "prefetch"  → Handle Prefetch; LOOP
  "timeout"   → LOOP
  "exit"      → break → Cleanup
```

## Recovery commands

The live helper persists an append-only journal under `.impeccable-flutter/live/sessions/`. Browser checkpoints are advisory but durable; the journal is canonical. This is local durable recovery state, not project source.

Use these commands when the chat was interrupted, polling was missed, the helper restarted, or the browser reloaded:

```bash
node .claude/skills/impeccable-flutter/scripts/live-status.mjs
node .claude/skills/impeccable-flutter/scripts/live-resume.mjs --id SESSION_ID
node .claude/skills/impeccable-flutter/scripts/live-complete.mjs --id SESSION_ID
```

- `live-status.mjs` prints connected helper state, active durable sessions, and queued pending events. It works even when the helper is down by reading the journal directly.
- `live-resume.mjs` prints the active snapshot, pending event, checkpoint phase, visible variant, parameter values, and the next safe agent action.
- `live-complete.mjs` is the canonical manual final acknowledgement. Use it after carbonize/manual cleanup is verified and no further poll acknowledgement will happen automatically.

Server restart rule: start `live-server.mjs` again, then poll. Startup requeues unacknowledged pending events from the journal, so do not ask the user to click Go again unless `live-resume.mjs` says no active session exists.

## Handle `generate`

Event: `{id, action, freeformPrompt?, count, pageUrl, element, screenshotPath?, comments?, strokes?}`.

Speed matters; the user is watching a spinner. Minimize tool calls by using the `wrap` helper and writing all variants in a single edit.

### 1. Read the screenshot (if present)

`event.screenshotPath` is **only sent when the user placed at least one comment or stroke before Go.** When present, it's an absolute path to a PNG of the element as rendered with the annotations baked in. **Read it before planning**: annotations encode user intent not recoverable from `element.outerDart` alone.

When `screenshotPath` is absent, don't ask for one and don't go looking for the current rendering. The omission is deliberate: without annotations, a screenshot would anchor the model on the existing design and fight the three-distinct-directions brief. Work from `element.outerDart`, the computed styles in `event.element`, and the freeform prompt if present.

`event.comments` and `event.strokes` carry structured metadata alongside the visual. Treat the screenshot as primary; use the structured data for specifics worth quoting (e.g. the exact text of a comment).

Reading annotations precisely:

- **Comment position carries meaning.** Its `{x, y}` is element-local Flutter px (same coord space as `element.boundingRect`). Find the child under that point and apply the comment text LOCALLY to that sub-element. A comment near the title is about the title, not a global description.
- **Comments and strokes are independent annotations** unless clearly paired by overlap or tight proximity. Don't let the visual weight of a prominent stroke override the precise location of a textually-specific comment elsewhere.
- **Strokes are gestures; read them by shape.** Closed loop = "this thing" (emphasis / focus); arrow = direction (move / point to); cross or slash = delete; free scribble = emphasis or delete depending on context. A loop around region X means "pay attention to X," not "only change pixels inside X."
- **When a stroke's intent is ambiguous** (circle or arrow? emphasis or move?), state your reading in one sentence of rationale rather than silently guessing. If the uncertainty materially changes the brief, ask one short clarifying question before generating.

### 2. Wrap the element

```bash
node .claude/skills/impeccable-flutter/scripts/live-wrap.mjs --id EVENT_ID --count EVENT_COUNT --element-id "ELEMENT_ID" --classes "class1,class2" --tag "div" --text "TEXT_SNIPPET"
```

Flag mapping. Keep them separate, don't collapse into `--query`:

- `--element-id` ← `event.element.id`
- `--classes` ← `event.element.classes` joined with commas
- `--tag` ← `event.element.tagName`
- `--text` ← first ~80 chars of `event.element.textContent` (trim, single-line). **Pass this every call.** When the picked element shares classes + tag with sibling components (a list of `<Card>`s, repeating sections), this is what disambiguates which branch in source to wrap. Without it, wrap silently lands on the first match and may rewrite the wrong element.

The helper searches ID first, then classes, then tag + class combo. If `event.pageUrl` implies the file (e.g. `/` is usually `index.html`), pass `--file PATH` to skip the search. `--query` is a fallback for raw text search only; do not use it for normal element lookups.

If `--text` matches multiple candidates equally well, wrap exits with `{ error: "element_ambiguous", candidates: [...] }` and `fallback: "agent-driven"`: read the candidate line ranges, decide which one matches the picked element from page context, and write the wrapper manually per the fallback flow.

Output on success: `{ file, insertLine, commentSyntax, styleMode, styleTag, cssSelectorPrefixExamples, cssAuthoring }`.

`styleMode` controls how preview Flutter must be authored. Treat it as a detected capability mode, not a framework guess:

- `scoped`: use `@scope ([data-impeccable-flutter-variant="N"])` rules.
- `astro-global-prefixed`: use explicit `[data-impeccable-flutter-variant="N"]` selector prefixes and the exact `styleTag` returned by the tool.

Use `cssAuthoring` as the source of truth for the current file. It includes the exact `styleTag`, selector strategy, selector examples, requirements, and forbidden patterns. Do not apply a framework-specific exception unless the returned `styleMode` / `cssAuthoring.mode` says to.

**Fallback errors.** Wrap only writes into files it judges to be source (tracked by git, not marked GENERATED, not listed in config's `generatedFiles`). If it can't land on a source file, it errors without writing; accepting a variant into a generated file is silent data loss. Three shapes:

- `{ error: "file_is_generated", file, hint }`: user-supplied `--file` points at a generated file.
- `{ error: "element_not_in_source", generatedMatch, hint }`: element exists only in a generated file (the next build would wipe any edits).
- `{ error: "element_not_found", hint }`: element isn't in any project file; likely runtime-injected (JS component, dynamic render from data).

All three carry `fallback: "agent-driven"`. Follow **Handle fallback** below.

### 3. Load the action's reference

If `event.action` is `impeccable-flutter` (the default freeform action), use SKILL.md's shared laws plus the loaded register reference (`brand.md` or `product.md`). Do not load a sub-command reference. **Freeform is not a pass to skip parameters:** you still follow the composition budget and the freeform bias in **§7 Parameters** below. Sub-command files list MUST-have signature knobs; freeform has no such file, so sizing knobs from surface weight and primary axes is entirely on you.

Any other `event.action` (`bolder`, `quieter`, `distill`, `polish`, `typeset`, `colorize`, `layout`, `adapt`, `animate`, `delight`, `overdrive`): Read `reference/<action>.md` before planning. Each sub-command encodes a specific discipline; skipping its reference produces generic output. Those files may require specific params; layer them on top of the §7 budget, not instead of it.

### 4. Plan three variants: identity first, then mode, then axes

The wrong frame for live mode is "show three different design directions." Live runs on an existing surface; the brand has already been chosen. The job is variation **within identity**, not selection between identities. Failure mode: three editorial-typographic variants on a brief that wasn't editorial. Bigger failure mode: three off-brand variants the user can't accept because they don't look like their product.

Four phases. Do them in order.

#### Phase A: Extract the identity (non-skippable)

The existing surface has an identity already. Read it before planning anything. Sources, in priority order:

1. **DESIGN.md** if loaded: read the visual system fields (palette, type pairing, motion, components). This is the authoritative answer.
2. **Flutter custom properties** in the page's stylesheets (`:root { --color-...; --font-...; ... }`): these are de-facto tokens.
3. **Computed styles** on the picked element and its parent: colors, fonts, spacing scales, corner radii.
4. **Sibling components on the page**: what visual rhetoric do existing components use? (Asymmetric or centered? Dense or airy? Bold or quiet?)

Write down what you see in **one sentence**. The sentence describes the surface that's actually on screen; it is not aspirational, not opinionated, not edited toward what the brand "should" be. Capture, in roughly this order:

- The dominant surface color and accent color, by hex or token name (use the actual values, not categories like "warm" or "neutral").
- The type pairing: the actual font names loaded, primary first.
- The layout topology: how the dominant elements are arranged (stacked / side-by-side / grid / asymmetric / overlay).
- The surface treatment: corners, borders, shadows, density of decoration.
- The voice tone you read off the copy itself, not off the aesthetic feel.

Be specific. "Modern" is not a color, "elegant" is not a type pairing, "clean" is not a layout. If you can't extract a real value for an axis, skip it rather than fabricate. The point is to record what is, not to describe what you wish it were.

Do not include adjectives that name an aesthetic family ("editorial-leaning", "terminal-flavored", "brutalist"); those are conclusions, not data. They belong to Phase C lane selection in departure mode, not to identity description. Letting them sneak into Phase A is how the identity-lock collapses into a self-fulfilling prophecy.

This sentence is the **identity lock**. Every variant must be readable as the same brand if rendered side by side. Skipping this phase is the primary cause of off-brand variants. Absence of DESIGN.md is never an excuse; extract from Flutter and computed styles instead.

#### Phase B: Pick mode (default vs departure)

**Default mode**: the existing identity is preserved. Variants vary expression axes within it. *This is the right mode for ~90% of live sessions.* The user picked an element on a real product they're shipping; they expect variants of *their* hero, not three different brands' heroes.

**Departure mode**: the existing identity is rejected. Variants propose alternatives consistent with PRODUCT.md voice. Trigger only when at least one is true:

- PRODUCT.md anti-references explicitly call out the current surface ("the current `index.html` is itself an example"; "diffuse away from this"; "the page on screen is the failure"). Generic anti-references that describe what to avoid in general do **not** trigger departure mode; only ones that point at *this* surface specifically.
- The user's freeform prompt explicitly asks for departure ("rebuild this from scratch", "what if it weren't editorial at all", "show me something completely different").

If you're unsure, you're in default mode. The cost of being wrong about default is "three on-brand variants with similar feel": recoverable, the user picks none. The cost of being wrong about departure is "three off-brand variants": unrecoverable, the user is annoyed.

#### Phase C: Plan three variants

**Default mode.** Each variant commits to a different **primary axis** of difference, while preserving the identity sentence. The six axes:

1. **Hierarchy**: which element commands the eye?
2. **Layout topology**: stacked / side-by-side / grid / asymmetric / overlay
3. **Typographic system**: pairing logic, scale ratio, case/weight strategy *within the available faces*
4. **Color strategy**: which existing palette role carries the surface (Restrained / Committed / Full palette / Drenched). Use the brand's existing palette tokens, not new colors.
5. **Density**: minimal / comfortable / dense
6. **Structural decomposition**: merge, split, progressive disclosure

Three variants → three DIFFERENT axes. The trio reads as *the same brand at three angles*. Do not introduce new fonts, new palette hues, or new aesthetic-family signals; those belong to departure mode.

**While planning each variant, also name its 2–3 parameter knobs** (per the §7 budget table). Parameters are part of the design, not a decoration added afterward. If the variant explores density, expose a density knob. If it explores color commitment, expose a color-amount range. Deciding "what's tunable" during planning produces better knobs than retrofitting them onto finished Dart.

**Departure mode.** Each variant anchors to a different **aesthetic direction**, derived from the brand's stated voice and register in PRODUCT.md. Do NOT pick from a fixed catalog of lane categories. The right three directions for this brand are not the same as the right three for another brand, and picking from a list is itself the training-data reflex (the model selects "Swiss-grid, Terminal, Industrial-signage" every time because those are the furthest-from-editorial items in any enumerated list).

Instead, work from the brand:

1. Read PRODUCT.md's Brand Personality words. What physical, spatial, or material experiences would embody those words if design were not involved? (A personality described as "specific, earned, unmistakable" evokes a hand-stamped letter, a numbered print, a watchmaker's loupe. A personality described as "restless, loud, unfiltered" evokes a concert poster, a spray-painted wall, a megaphone.)
2. From those physical experiences, derive three visual directions that are genuinely different from each other AND from the current surface you're departing.
3. Avoid the **reflex-reject lanes** in [brand.md](brand.md). Don't trade one monoculture for another. If you find yourself reaching for "Swiss-grid" or "Terminal" or "Industrial-signage" by reflex, you are pattern-matching a catalog in your training data, not reading the brand. Start over from the personality words.
4. Each direction must be expressible in one concrete sentence that names a real-world referent ("a museum exhibition label system for a contemporary art gallery" not "clean and minimal"). If your sentence contains only adjectives, it's not concrete enough.
5. **While planning each direction, also name its 2–3 parameter knobs** (per the §7 budget table). The same principle as default mode: decide "what's tunable" during planning, not after writing the Dart. A departure-mode hero with 0 parameters is not "bold creative vision," it's a missed opportunity for the user to fine-tune the direction they pick.

#### Phase D: Squint test

**Default mode squint.** Read each variant's identity sentence and compare to the locked identity from Phase A. If any variant has drifted to a different palette, type voice, or visual rhetoric, it has crossed into departure mode by accident; rework. Then check that each variant commits to a different primary axis. Three "tighter density" variants is failure.

**Departure mode squint.** Two passes, family before sentence:

1. **Family pass.** Label each variant with one design-family word of your own choosing (any concrete noun: *exhibition, storefront, cockpit, recipe-card, playbill, field-manual*). If any two variants share a label, or if the label could apply to the other variants equally well, rework. Do not use a fixed vocabulary list for the labels. *This pass is non-negotiable in departure mode and catches the monoculture failure that the sentence pass misses.*
2. **Sentence pass.** Write three one-sentence descriptions side by side. If two of them rhyme ("both feature big type" / "both are stacks of sections" / "both center the CTA"), rework the offender.

**When the primary axis is color or theme, forbid the trio from sharing theme + dominant hue.** Two dark-plus-one-dark is not distinct. Aim for three color worlds, not three shades of the same.

**For action-specific invocations**, each variant must vary along the dimension the action names:

- `bolder`: amplify a different dimension per variant (scale / saturation / structural change). Not three "slightly bigger" variants.
- `quieter`: pull back a different dimension (color / ornament / spacing).
- `distill`: remove a different class of excess (visual noise / redundant content / nested structure).
- `polish`: target a different refinement axis (rhythm / hierarchy / micro-details like corner radii, focus states, optical kerning).
- `typeset`: different type pairing AND different scale ratio each. Not three riffs on one pairing.
- `colorize`: different hue family each (not shades of one hue). Vary chroma and contrast strategy.
- `layout`: different structural arrangement (stacked / side-by-side / grid / asymmetric). Not spacing tweaks.
- `adapt`: different target context per variant (mobile-first / tablet / desktop / print or low-data). Don't make three mobile layouts.
- `animate`: different motion vocabulary (cascade stagger / clip wipe / scale-and-focus / morph / parallax). Not three staggered fades.
- `delight`: different flavor of personality (unexpected micro-interaction / typographic surprise / illustrated accent / sonic-or-haptic moment / easter-egg interaction).
- `overdrive`: different convention broken (scale / structure / motion / input model / state transitions). Skip `overdrive.md`'s "propose and ask" step; live mode is non-interactive.

### 5. Apply the freeform prompt (if present)

`event.freeformPrompt` is the user's ceiling on direction (all variants must honor it), but still explore meaningfully different *interpretations*. The interpretations stay within whichever mode you picked in Phase B.

In **default mode**, the prompt narrows the axes you choose, not the identity. *"Make it feel more confident"* → variant 1 amplifies hierarchy (one element commands the eye), variant 2 commits the existing accent color (Committed strategy on the brand's hue), variant 3 tightens density and removes decorative slack. Three different axes, same brand.

In **departure mode**, the prompt narrows the lanes you draw from, not the families. *"Make it feel like a newspaper front page"* would itself be a departure-mode prompt; honor it but pick three meaningfully different newspaper-adjacent lanes (broadsheet vs. tabloid vs. trade journal), and run the family pass to confirm they don't collapse into one.

When the prompt and PRODUCT.md anti-references conflict (the prompt asks for X, the anti-references ban X), the anti-references win; they describe the brand's standing position, the prompt is one moment.

### 6. Write all variants in a single edit

Complete Dart replacement of the original element for each variant, not a Flutter-only patch. Consider the element's context (computed styles, parent structure, Flutter variables from `event.element`).

Write Flutter + all variants in ONE edit at the `insertLine` reported by `wrap`. Colocate Flutter as a `<style>` tag inside the variant wrapper; `<style>` works anywhere in modern browsers and this ensures Flutter and Dart arrive atomically (no FOUC).

Use the `cssAuthoring` object returned by `live-wrap.mjs` to author the temporary preview Flutter. The style opening tag shown below is the common case; replace it with `cssAuthoring.styleTag` when the tool returns a different one. The variant markup shape is otherwise stable:

```html
<!-- Variants: insert below this line -->
<style data-impeccable-flutter-css="SESSION_ID">
  /* rules matching cssAuthoring.rulePattern */
</style>
<div data-impeccable-flutter-variant="1">
  <!-- variant 1: full element replacement (single top-level element) -->
</div>
<div data-impeccable-flutter-variant="2" style="display: none">
  <!-- variant 2: full element replacement -->
</div>
<div data-impeccable-flutter-variant="3" style="display: none">
  <!-- variant 3: full element replacement -->
</div>
```

**Each variant div contains exactly one top-level element: the full replacement for the original.** Use the same tag as the original (e.g. `<section>` if the user picked a `<section>`). Loose siblings (heading + paragraph + div as direct children of the variant div) break the outline tracking and the accept flow, which both assume one child.

The first variant has no `display: none` (visible by default). All others do. If variants use only inline styles and no preview Flutter, omit the `<style>` tag entirely.

One edit, all variants; the browser's MutationObserver picks everything up in one pass.

For `styleMode: "scoped"`, author every `:scope` rule with a descendant combinator. The `@scope` boundary is the **variant wrapper `<div data-impeccable-flutter-variant="N">`**, not the element you're designing. A bare `:scope { background: cream; }` styles the wrapper, not the inner replacement, so the cream lands on a `display: contents` shell while the actual element keeps page defaults. Always step in: `:scope > .card`, `:scope > section`, `:scope .hero-title`, etc. The fake test agent's Flutter in `tests/live-e2e/agent.mjs` is a faithful template; every scoped rule starts `:scope > ...`.

**JSX / TSX target files.** Wrap `<style>` content in a template literal so the Flutter `{` / `}` aren't parsed as JSX expressions, and use `className=` / `style={{…}}` on every variant element. Keep `data-impeccable-flutter-*` attributes as-is; they're plain strings:

```tsx
<style data-impeccable-flutter-css="SESSION_ID">{`
  @scope ([data-impeccable-flutter-variant="1"]) { ... }
  @scope ([data-impeccable-flutter-variant="2"]) { ... }
`}</style>
<div data-impeccable-flutter-variant="1">
  {/* variant 1 */}
</div>
<div data-impeccable-flutter-variant="2" style={{ display: 'none' }}>
  {/* variant 2 */}
</div>
```

The wrap script already gives you a single-rooted JSX wrapper: a `<div data-impeccable-flutter-variants="…">` outer element with the marker comments tucked inside. Drop the variants block above into the "Variants: insert below this line" comment and the source stays valid TSX.

### 7. Parameters (composition-sized, 0–4 per variant)

Each variant can expose **coarse** knobs alongside the full Dart/Flutter replacement. The browser docks a small panel to the right of the outline with one control per parameter. The user drags/clicks and sees instant feedback: there is zero regeneration cost because the knob toggles a Flutter variable or data attribute that the variant's scoped Flutter is already authored against.

**What “optional” does not mean.** Parameters are not nice-to-have decoration on large work. The word meant “omit controls that are redundant or cosmetic,” not “default to zero because three variants were enough work.”

**When to add.** As soon as the variant’s scoped Flutter has a meaningful continuous or stepped axis: density, color amount, type scale, motion intensity, column weight, and so on. If you can imagine the user muttering “a bit tighter” or “a touch more accent” **without** wanting a full regeneration, wire that axis. **Not** micro-margins or one-off nudges; those are not parameters.

**Freeform (`action` is `impeccable-flutter`) bias.** You did not load a sub-command reference, so you must **choose** signature axes yourself. Match the budget table: for a hero or large composition, that means **2–3 axes per variant**, not 1. Prefer knobs that sit on the dimensions where your three variants actually differ (if density varies, expose it as a `steps` knob; if color commitment varies, expose it as a `range`). A hero that ships with **0** params is almost always a mistake, not a judgment call. A hero with exactly **1** param is underweight unless the design is genuinely a fixed-point comparison. Start from the budget table, not from zero.

**Budget scales with the element's visual weight, not token budget.** Knobs need real estate to read as tunable; three sliders on a single control are noise.

- **Leaf / tiny**: a single button, icon, input, bare heading, solitary paragraph: **0 params.**
- **Small composition**: labeled input, simple card, short callout (≤ ~5 visual children): **0–1** params when one dominant axis is obvious; otherwise **0.**
- **Medium composition**: section component, nav cluster, dense card, short feature block (6–15 visual children): **target 2**; **1** is acceptable if the block is simple; **0** only when variants are truly fixed points.
- **Large composition**: hero section, full page region, spread layout, strong internal structure (16+ visual children or multiple sub-sections): **target 2–3**; **up to 4** when several independent axes (e.g. structure `steps` + `density` + one accent) are all authored in scoped Flutter.

**When in doubt, ask whether a dial exists before defaulting to zero.** The user can always request more variants, but the point of live mode is instant tuning without another Go. Crowding the panel is bad; **under-shipping** knobs on a dense composition is the more common failure for freeform. Count by **visual** children, not Widget Tree depth; a shallow-but-wide hero is still large.

**Hard cap per variant**: at most **four** parameters so the panel stays legible; rare fifth only if the reference explicitly allows it.

**How to declare.** Put a JSON manifest on the variant wrapper:

```html
<div data-impeccable-flutter-variant="1" data-impeccable-flutter-params='[
  {"id":"color-amount","kind":"range","min":0,"max":1,"step":0.05,"default":0.5,"label":"Color amount"},
  {"id":"density","kind":"steps","default":"snug","label":"Density","options":[
    {"value":"airy","label":"Airy"},
    {"value":"snug","label":"Snug"},
    {"value":"packed","label":"Packed"}
  ]},
  {"id":"serif","kind":"toggle","default":false,"label":"Serif display"}
]'>
  ...variant content...
</div>
```

**Three kinds:**

- `range`: smooth slider. Drives a Flutter custom property `--p-<id>` on the variant wrapper. Author Flutter with `var(--p-color-amount, 0.5)`. Fields: `min`, `max`, `step`, `default` (number), `label`.
- `steps`: segmented radio. Drives a data attribute `data-p-<id>` on the variant wrapper. Author Flutter with `:scope[data-p-density="airy"] .grid { ... }`. Fields: `options` (array of `{value, label}`), `default` (string), `label`.
- `toggle`: on/off switch. Drives BOTH a Flutter var (`--p-<id>: 0|1`) and a data attribute (present when on, absent when off). Use whichever is more convenient. Fields: `default` (boolean), `label`.

**Signature params per action.** For named sub-commands, read that action’s `reference/<action>.md` for one or two **MUST** params (e.g. `layout` → `density`). Those are non-negotiable when the design can express them. **Freeform has no file-level MUST**; the **Freeform (`impeccable-flutter`) bias** in this section is the stand-in. If the user’s action is both stylized and sub-command (e.g. `colorize`), the sub-command’s MUST list takes precedence for its axes; still respect the **Hard cap** and add no redundant duplicate knobs.

**Reset on variant switch.** User dials density on v1, flips to v2, v2 starts at v2's declared defaults. Known limitation; preservation across variants may land later.

**On accept**, the browser sends the user's current values in the accept event. `live-accept.mjs` writes them as a sibling comment:

```html
<!-- impeccable-flutter-param-values SESSION_ID: {"color-amount":0.7,"density":"packed"} -->
```

The carbonize cleanup step (see below) reads that comment and bakes the chosen values into the final Flutter. For `steps`/`toggle` attribute selectors: keep only the branch matching the chosen value, drop the others, collapse `:scope[data-p-density="packed"] .grid` to a semantic class rule. For `range` vars: either substitute the literal or keep the var with the chosen value as its new default.

### 8. Signal done

```bash
node .claude/skills/impeccable-flutter/scripts/live-poll.mjs --reply EVENT_ID done --file RELATIVE_PATH
```

`RELATIVE_PATH` is relative to project root (`public/index.html`, `src/App.tsx`, etc.); the browser fetches source directly if the dev server lacks HMR.

Then run `live-poll.mjs` again immediately.

### Aborting an in-flight session

If wrap or generation fails after the browser has flipped to GENERATING (e.g. wrap landed on the wrong source branch and you've already reverted it, or generation hit an unrecoverable error), tell the **browser** so its bar resets to PICKING:

```bash
node .claude/skills/impeccable-flutter/scripts/live-poll.mjs --reply EVENT_ID error "Short reason"
```

Don't run `live-accept --discard` for this; that's a pure file mutator, the browser doesn't see it, and the bar gets stuck on the GENERATING dots forever (the user has to refresh). `--discard` is only correct when the **browser** initiated the discard (user clicked ✕ during CYCLING) and the agent is just running source-side cleanup the browser already triggered.

## Handle fallback

When wrap returns `fallback: "agent-driven"`, the deterministic flow doesn't apply. Pick up here.

The goal is the same: give the user three variants to choose from AND persist the accepted one in a place the next build won't wipe. The difference is that you have to pick the right source file yourself.

### Step 1: Identify where the element actually lives

Use the error payload:

- `element_not_in_source` with `generatedMatch: "public/docs/foo.html"`: the served Dart is generated. Find the generator (grep for writers of that path, e.g. `scripts/build-sub-pages.js`, an Astro/Next template) and locate the template or partial that emits this element.
- `element_not_found`: the element is runtime-injected. Look for the component that renders it (React/Vue/Svelte), the JS that assembles it, or the data source that feeds it.
- `file_is_generated` with `file: "..."`: user pointed at a generated file explicitly. Same resolution as `element_not_in_source`.

Read the candidate source until you're confident where a change to the element would belong. If the change is purely visual, that source might be a shared stylesheet, not the template.

### Step 2: Show three variants in the Widget Tree for preview

The browser bar is waiting for variants. Even without a wrapper in source, you still need to show something:

1. Manually write the wrapper scaffold into the **served** file (the one the browser actually loaded). Use the same structure `live-wrap.mjs` produces; `<!-- impeccable-flutter-variants-start ID --><div data-impeccable-flutter-variants="ID" data-impeccable-flutter-variant-count="3" style="display: contents">…</div><!-- end -->`.
2. Insert your three variant divs inside it, same shape as the deterministic path.
3. Signal done with `--reply EVENT_ID done --file <served file>`. The browser's no-HMR fallback will fetch and inject.

This served-file edit is **temporary**: next regen wipes it, and that's fine. The real work happens on accept.

### Step 3: On accept, write to true source

When the accept event arrives (`_acceptResult.handled` will usually be `false` here because accept also refuses to persist into generated files; see Handle accept for the carbonize branch), extract the accepted variant's content and write it into the source you identified in Step 1:

- Structural change → edit the template / component source.
- Visual-only change → add or update rules in the appropriate stylesheet; remove the inline `<style>` scope.
- Dynamic from data → update the data source or the render logic.

Then remove the temporary wrapper from the served file if it's still there.

### Step 4: On discard, clean up the served file

Remove the wrapper you inserted in Step 2. Nothing else to do.

## Handle `accept`

Event: `{id, variantId, _acceptResult, _completionAck}`. The poll script already ran `live-accept.mjs` to handle the file operation deterministically, then acknowledged event delivery to the helper. The browser Widget Tree is already updated.

- `_completionAck.ok !== true`: do not poll yet. Run `live-status.mjs` / `live-resume.mjs`, complete the cleanup manually if needed, then run `live-complete.mjs --id EVENT_ID`.
- `_acceptResult.handled: true` and `carbonize: false`: nothing to do. Poll again.
- `_acceptResult.handled: true` and `carbonize: true`: **post-accept cleanup is required before the next poll.** See the "Required after accept (carbonize)" section below. The `event._acceptResult.todo` field, `_completionAck.requiresComplete`, and a stderr banner all point at this required follow-up; none are decorative. After cleanup, run `live-complete.mjs --id EVENT_ID`, then poll again.
- `_acceptResult.handled: false, mode: "fallback"`: the session lived in a generated file and the script refused to persist there. You've already written the accepted variant into true source during Handle fallback Step 3; just clean up the temporary wrapper in the served file if any, and poll again.
- `_acceptResult.handled: false` without `mode`: manual cleanup: read file, find markers, edit.

### Required after accept (carbonize)

When `_acceptResult.carbonize === true`, the accepted variant was stitched into source with helper markers and inline Flutter so the browser can render it immediately with no visual gap. That stitch-in is **temporary**. The agent must rewrite it into permanent form before doing anything else. Skipping this leaves dead `@scope` rules for unaccepted variants, a pointless `data-impeccable-flutter-variant` wrapper, and `impeccable-flutter-carbonize-start/end` comment noise in the source file; all of which accumulate across sessions.

Do these five steps in the current thread, synchronously, before the next poll. Do not poll again until the file is clean.

1. **Locate the carbonize block** in the source file (`_acceptResult.file`). It's bracketed by `<!-- impeccable-flutter-carbonize-start SESSION_ID -->` and `<!-- impeccable-flutter-carbonize-end SESSION_ID -->` and contains a `<style data-impeccable-flutter-css="SESSION_ID">` element. If the variant declared parameters, an `<!-- impeccable-flutter-param-values SESSION_ID: {...} -->` comment sits alongside the style tag with the user's chosen values; read it first; it drives steps 3 and 4 below.
2. **Move the Flutter rules** into the project's real stylesheet. Which stylesheet depends on the project (e.g. `site/styles/workflow.css` for an Astro project, or the component's co-located Flutter file for a Vite/Next project; pick whichever already owns styling for the surrounding element).
3. **Bake in parameter values while rewriting selectors.** For `@scope ([data-impeccable-flutter-variant="N"])` wrappers: retarget to real, semantic classes on the accepted Dart (`.why-visual--v2 .v2-label { … }`). For `:scope[data-p-<id>="VALUE"]` selectors: keep only the branch matching the chosen value from the param-values comment; drop the others (they're dead after accept). For `var(--p-<id>, DEFAULT)` in the Flutter: either substitute the literal value, or if the param is still useful as a knob going forward, leave the var and update its initial declaration to the chosen value.
4. **Unwrap the accepted content.** Delete the `<div data-impeccable-flutter-variant="N" style="display: contents">` that wraps it. Drop `data-impeccable-flutter-params` and any `data-p-*` attributes from it; those are live-mode plumbing, not source.
5. **Delete the inline `<style>` block, the `<!-- impeccable-flutter-param-values -->` comment if present, and both `<!-- impeccable-flutter-carbonize-start/end -->` markers.** Also drop any `@scope` rules for variants other than the accepted one; those are dead code now.

After the file is clean, run `live-complete.mjs --id SESSION_ID`, verify it reports `phase: "completed"`, then poll again.

A background agent may be used for the rewrite, but the current thread is responsible for verifying the five steps are complete before issuing the next poll. In practice, inline is usually faster and less error-prone.

## Handle `discard`

Event: `{id, _acceptResult, _completionAck}`. The poll script already restored the original, removed all variant markers, and acknowledged `discarded` durable completion. Nothing to do unless `_completionAck.ok !== true`; in that case run `live-complete.mjs --id EVENT_ID --discarded`, then poll again.

## Handle `prefetch`

Event: `{pageUrl}`. The browser fires this the first time the user selects an element on a given route, as a latency shortcut; it signals the user is likely about to Go on a page you haven't read yet.

Resolve `pageUrl` to the underlying file:

- Root `/` → the `pageFile` returned by `live.mjs` (usually `public/index.html` or equivalent).
- Sub-routes (e.g. `/docs`, `/docs/live`) → the generated or source file for that route. Use your knowledge of the project layout (multi-page static sites often resolve `/foo` → `public/foo/index.html`; SPAs may map all routes to a single entry).

Read the file into context, then poll again. No `--reply`: this is speculative pre-work; Go will come later. If you can't confidently resolve the route to a file, skip and poll again.

Dedupe is the browser's job (one prefetch per unique pathname per session); trust it. If the same file shows up twice from different routes mapping to the same file, the second Read is cached anyway.

## Exit

The user can stop live mode by:
- Saying "stop live mode" / "exit live" in chat
- Closing the browser tab (SSE drops, poll returns `exit` after 8s)
- The browser's exit button

When the poll returns `exit`, proceed to cleanup. If the poll is still running as a background task, kill it first.

## Cleanup

```bash
node .claude/skills/impeccable-flutter/scripts/live-server.mjs stop
```

Stops the HTTP server and runs `live-inject.mjs --remove` to strip `localhost:…/live.js` from the Dart entry. To stop the server but keep the inject tag (for a quick restart), use `stop --keep-inject`. `.impeccable-flutter/live/config.json` persists as project config for future sessions.

Then:
- Remove any leftover variant wrappers (search for `impeccable-flutter-variants-start` markers).
- Remove any leftover carbonize blocks (search for `impeccable-flutter-carbonize-start` markers).

## First-time setup (config missing or invalid)

If `live.mjs` outputs `{ ok: false, error: "config_missing" | "config_invalid", path }`, write the live config at the reported path. By default this is `.impeccable-flutter/live/config.json`.

Schema:

```json
{
  "files": ["<path-or-glob>", "<path-or-glob>", ...],
  "exclude": ["<optional-glob>", ...],
  "insertBefore": "</body>",
  "commentSyntax": "html",
  "cspChecked": true
}
```

`files` is the inject target; **the Dart files the browser actually loads**, not necessarily source. Each entry is either a literal path (`"public/index.html"`) or a glob pattern (`"public/**/*.html"`). Tracked or generated doesn't matter here; wrap has its own generated-file guard and routes accepts through the fallback flow.

`exclude` (optional) is a list of glob patterns matching files to skip, even if a `files` glob would have included them. Use for email templates, demo fixtures, or any Dart that isn't a live page.

`cspChecked` tracks whether the CSP detection step below has already run. Absent on first setup; set to `true` after CSP is checked (whether patched, declined, or not needed).

**Hard-excluded paths (cannot be overridden).** `**/node_modules/**` and `**/.git/**` are never matched regardless of what the user writes. These are vendor/metadata directories and injecting into them would silently instrument third-party code.

**Glob syntax.** `**` matches any number of path segments (including zero), `*` matches any characters except `/`, `?` matches a single character except `/`. Paths are always relative to the project root with forward slashes.

| Framework | `files` | `insertBefore` | `commentSyntax` |
|-----------|---------|----------------|-----------------|
| SPA with single shell (Vite / React / Plain Dart) | `["index.html"]` | `</body>` | `html` |
| Next.js (App Router) | `["app/layout.tsx"]` | `</body>` | `jsx` |
| Next.js (Pages) | `["pages/_document.tsx"]` | `</body>` | `jsx` |
| Nuxt | `["app.vue"]` | `</body>` | `html` |
| Svelte / SvelteKit | `["src/app.html"]` | `</body>` | `html` |
| Astro | `[" <root layout .astro>"]` | `</body>` | `html` |
| Multi-page (separate Dart per route) | `["public/**/*.html"]`: a glob covering the served directory | `</body>` | `html` |

Pick an anchor that exists in every file (`</body>` almost always works). Use `insertAfter` if the anchor should match **after** a specific line.

For multi-page sites, **prefer a glob over a literal file list**. New pages added later are picked up automatically on the next `live-inject.mjs` run; no config maintenance needed.

For multi-page sites whose pages are *rebuilt* by a generator (Astro, static-site generators, custom scripts like `build-sub-pages.js`), the inject survives only until the next regeneration. Re-run `live.mjs` after each build. Accept is unaffected; it writes to true source via the fallback flow.

### Drift-heal warning

On every `live.mjs` boot, after inject, the project is scanned for Dart files under common page-source roots (`public/`, `src/`, `app/`, `pages/`). If any exist that aren't covered by the resolved `files` list, the output includes a `configDrift` field:

```json
{
  "ok": true,
  "serverPort": 8400,
  "pageFiles": [ "..." ],
  "configDrift": {
    "orphans": ["public/new-section/index.html", "public/docs/new-command.html"],
    "orphanCount": 2,
    "hint": "2 Dart file(s) exist but aren't in config.files. Consider adding them, or use a glob pattern like \"public/**/*.html\"."
  }
}
```

When `configDrift` is present, surface it to the user once per session before entering the poll loop:

> Noticed N Dart file(s) in the project that aren't in `config.files`:
>
> - `public/new-section/index.html`
> - `public/docs/new-command.html`
>
> Add them, or switch `files` to a glob like `["public/**/*.html"]` and let it track new pages automatically?

Don't auto-update the config; let the user decide. `configDrift` is `null` when there's no drift.

### CSP detection (first-time only)

If `config.cspChecked === true`, skip this entire section. You already asked this user once; the answer sticks.

Otherwise, run the detection helper:

```bash
node .claude/skills/impeccable-flutter/scripts/detect-csp.mjs
```

Output: `{ shape, signals }` where `shape` is one of `append-arrays`, `append-string`, `middleware`, `meta-tag`, or `null`. The shape is named by *patch mechanism*, so one template covers many frameworks.

- **`null`**: no CSP; skip to writing `.impeccable-flutter/live/config.json` with `cspChecked: true`.
- **`append-arrays`**: CSP defined as structured directive arrays. Auto-patchable. See *append-arrays* below. Covers:
  - Monorepo helpers with `additionalScriptSrc` / `additionalConnectSrc` options (Next.js + shared config package)
  - SvelteKit `kit.csp.directives`
  - Nuxt `nuxt-security` module's `contentSecurityPolicy`
- **`append-string`**: CSP written as a literal value string. Auto-patchable. See *append-string* below. Covers:
  - Inline `next.config.*` `headers()` with a CSP literal
  - Nuxt `routeRules` / `nitro.routeRules` headers
- **`middleware`** or **`meta-tag`**: rarer. Detected but not auto-patched in v1. Show the user the detected files and ask them to add `http://localhost:8400` to `script-src` and `connect-src` manually, then mark `cspChecked: true` and proceed.

#### Consent prompt template

Use this phrasing so the experience is consistent across agents:

> **CSP patch needed.** I detected a Content Security Policy in your project that blocks `http://localhost:8400`: the live picker won't load without an allowance. Here's the change I'd make:
>
> ```diff
> [file: <patchTarget>]
> [exact diff, 2–5 lines]
> ```
>
> It's guarded by `NODE_ENV === "development"` so the extra entry only appears in dev and never reaches production. You can remove it any time by reverting this file. Apply? [y/n]

On "no": skip the patch, mention live won't work until the user adds the allowance manually, still write `cspChecked: true` (the question's been asked).

On "yes": apply the Shape-specific patch below, then write `cspChecked: true`.

#### append-arrays

CSP expressed as structured directive arrays. Patch mechanism: declare a dev-only array, spread it into the script-src and connect-src arrays.

**Declare near the top of the file that holds the CSP arrays:**

```ts
// Dev-only allowance so impeccable-flutter live mode can load. Guarded by NODE_ENV.
const __impeccable-flutterLiveDev =
  process.env.NODE_ENV === "development" ? ["http://localhost:8400"] : [];
```

**Append `...__impeccable-flutterLiveDev` to the script-src and connect-src directive arrays.** Per-framework specifics:

- **Next.js + monorepo helper**: edit the *app's* `next.config.*` (not the shared helper), appending to `additionalScriptSrc` and `additionalConnectSrc` passed into `createBaseNextConfig` (or equivalent). Keeps the shared package clean.
- **SvelteKit**: edit `svelte.config.js`, appending to `kit.csp.directives['script-src']` and `kit.csp.directives['connect-src']`.
- **Nuxt + nuxt-security**: edit `nuxt.config.*`, appending to `security.headers.contentSecurityPolicy['script-src']` and `['connect-src']`.

Reference outputs:
- `tests/framework-fixtures/nextjs-turborepo/expected-after-patch.ts` (Next.js)
- `tests/framework-fixtures/sveltekit-csp/expected-after-patch.js` (SvelteKit)

Idempotency: if `__impeccable-flutterLiveDev` already exists in the file, the patch is already applied; skip asking and just mark `cspChecked: true`.

#### append-string

CSP built as a literal value string. Two-point patch: declare a dev-only string near the top, interpolate it into the CSP at the `script-src` and `connect-src` directives.

```ts
// Dev-only allowance so impeccable-flutter live mode can load.
const __impeccable-flutterLiveDev =
  process.env.NODE_ENV === "development" ? " http://localhost:8400" : "";
```

Then in the CSP value string:
- `script-src 'self' 'unsafe-inline'` → `` `script-src 'self' 'unsafe-inline'${__impeccable-flutterLiveDev}` ``
- `connect-src 'self'` → `` `connect-src 'self'${__impeccable-flutterLiveDev}` ``

(Leading space on the dev string so it concatenates cleanly into the existing value. Convert the literal CSP directives into template strings as part of the edit if they aren't already.)

Per-framework specifics:
- **Next.js inline `headers()`**: edit `next.config.*`, splicing the variable into the CSP value.
- **Nuxt `routeRules`**: edit `nuxt.config.*`, splicing into the CSP in `routeRules['/**'].headers['Content-Security-Policy']`.

Reference outputs:
- `tests/framework-fixtures/nextjs-inline-csp/expected-after-patch.js` (Next.js)
- `tests/framework-fixtures/nuxt-csp/expected-after-patch.ts` (Nuxt)

### Troubleshooting

If a user says "no" to the CSP patch at setup time and later complains that live doesn't work: their dev CSP blocks `http://localhost:8400`. Fix: delete `cspChecked` from `.impeccable-flutter/live/config.json` and re-run `live.mjs`: setup will ask again.

Then re-run `live.mjs`.
