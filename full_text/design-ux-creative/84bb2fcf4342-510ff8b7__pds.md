---
name: pds
description: >
  Pencil Design System generator. Invoke with /pds followed by a business domain
  (e.g., "/pds coffee shop that sells coffee online"). Creates a complete design
  system with tokens, foundations, components, patterns, and optional screens
  in a .pen file.
disable-model-invocation: true
version: 1.1.0
license: MIT
metadata:
  author: jsstech
  tags: design-system, pencil, ui-kit, components, tokens, domain-aware
---

# Pencil Design System Generator

Generate a complete, Mews-inspired design system in a Pencil `.pen` file. Research the business domain, create ~89 themed tokens, build visual foundation documentation, ~25 reusable components organized by category, and composition patterns — all from a single command like `/pds coffee shop that sells coffee online`. Domain screens are generated only if the user explicitly requests them.

## ⛔ GOLDEN RULES — Read These First

These rules prevent the #1 visual bug (overlapping elements). **Violating any of these produces a broken design.**

1. **EVERY frame MUST have `layout: "vertical"` or `layout: "horizontal"`.** No exceptions. Without it, children are placed at absolute position (0,0) and overlap each other. This includes: section frames, category rows, component root frames, card bodies, nav containers — ALL frames.
2. **Category display rows MUST use `layout: "horizontal"`.** Components shown side-by-side need a horizontal row frame.
3. **Use `height: "fit_content"` on section frames** — never fixed pixel heights.
4. **After EVERY `batch_design`, take a screenshot and CHECK for overlapping elements.** Missing `layout` → add it immediately.
5. **Copy the exact operation code from the reference files.** Do NOT improvise layout code.
6. **NEVER call `open_document("new")`.** Always check `get_editor_state` first — if a `.pen` file exists, use it.

## Getting Started

When this skill is invoked via `/pds`, begin with:

1. **Parse the user's input** — extract domain, brand name, color preferences, font preferences from their message after `/pds`
2. **Greet and confirm** — show what was understood and what will be built:

```
Pencil Design System Generator

Domain: [extracted domain]
Brand:  [extracted name or "unnamed"]
Colors: [extracted preferences or "will research"]
Fonts:  [extracted preferences or "will research"]

I'll build this step by step:
 1. Research    -> design brief
 2. Tokens      -> ~89 themed variables (light + dark)
 3. Foundations  -> visual documentation
 4. Components  -> ~25 reusable parts
 5. Patterns    -> 4 composition showcases

Each step pauses for your review. Type:
  c  to continue
  r  to redo (tell me what to change)
  s  to skip ahead to final verification

Want screens too? Tell me now or add them later.

Starting with domain research...
```

3. **Proceed to Phase 1** immediately — the first review pause comes after the design brief is ready.

## Input

The user provides a **business domain** (e.g., "bakery", "fitness app", "SaaS dashboard"). Optional extras: brand name, color preferences, font preferences, specific screens wanted, light/dark theme preference, **reference image**. If the user gives only a domain, infer everything else from research.

**If the user specifies colors or fonts:** Use their values as the primary/accent/background tokens in Phase 3 and derive the remaining palette around them (secondary, muted, foregrounds). Research still runs to fill in gaps, but user preferences take priority over both research and fallback tables.

**If the user provides a reference image** (placed on the canvas, pasted in chat, or as a URL): This is the highest-priority design input. In Phase 1, run the 7-pass structured extraction to derive:
- **Colors** — dominant color, accent colors, background color, text color (report as hex values)
- **Typography style** — serif/sans-serif, weight, spacing (match to closest Google Fonts)
- **Tone** — minimal, bold, playful, corporate, organic, etc.
- **Layout density** — spacious vs compact, card-heavy vs list-heavy
- **Visual patterns** — rounded corners vs sharp, shadow depth, border usage

Use these extracted values as the foundation for all tokens. Research supplements the image analysis but does NOT override it — the reference image is the primary source of truth for the design direction.

## Canvas Organization

The canvas is laid out left-to-right in three core sections (always created), plus an optional screens section:

```
[Foundations 1440×fit] → 100px gap → [Components 1440×fit] → 100px gap → [Patterns 1440×fit] → (optional) [Screens →]
```

- **Foundations** — Visual documentation: color palette swatches, typography specimens, spacing scale, elevation examples, border radius showcase.
- **Components** — All ~25 reusable components, organized under category sub-frames (Buttons, Inputs, Typography, Badges, Alerts, Cards, Navigation, Tables, etc.).
- **Patterns** — Composition showcases: form pattern, data display pattern, navigation pattern, card layout pattern. Each uses component refs to demonstrate real usage.
- **Screens** *(only if user requests)* — 3–5 domain-relevant screens placed to the right of Patterns.

No components live at the document root except these section frames and the optional navigation index.

## Workflow

Execute these phases in order. Each phase builds on the previous. Never skip mandatory phases. Reference files in `references/` contain detailed specs — load them as each phase begins.

**⛔ Review gates** are placed after major phases. At each gate you MUST stop, show results, and wait for user input before continuing. The user controls the pace — they type `c` to continue, `r` to redo, or `s` to skip ahead.

### Phase 1 — Research the Domain

**If `collectui-mcp` is available:** Use it for visual research before web search.
1. Call `collectui_search({ query: "[domain]", limit: 8 })` — e.g., `"coffee shop"`, `"dashboard"`, `"e-commerce"`
2. Analyze the returned design screenshots — extract dominant colors (hex), typography patterns, layout styles, corner radii, shadow depth
3. Use these as strong design signals alongside web research

**If a reference image exists:** Check if the user placed an image on the canvas or provided one in chat.
- If on canvas: call `get_screenshot` on the image node to analyze it
- If pasted in chat or provided as a URL: analyze the image directly

Run a **7-pass structured extraction** to map visual properties to specific tokens:

| Pass | What to Extract | Token Mapping |
|------|----------------|---------------|
| **1. Colors** | Background color(s), primary brand color, secondary/supporting color, accent color (buttons/links/highlights), text colors (heading, body, muted/caption), border/divider colors, any semantic indicators (green/amber/red for status) | `--background`, `--primary`, `--secondary`, `--accent`, `--foreground`, `--muted-foreground`, `--border`, `--color-success/warning/error/info` |
| **2. Typography** | Heading font (serif/sans? geometric/humanist?), body font, font weights observed (thin, regular, semibold, bold?), letter spacing patterns (tight headings? wide all-caps?), line height density | `--font-primary`, `--font-secondary`, `--weight-*`, `--tracking-*`, `--leading-*` |
| **3. Spacing & Sizing** | Overall density (spacious/moderate/compact), padding scale estimates (small 4-8px, medium 12-16px, large 24-32px), component sizes (button height, input height, icon sizes), gap patterns between cards/fields/sections | `--space-*`, `--size-button-height`, `--size-input-height`, `--size-icon-*`, `--size-sidebar-width` |
| **4. Shape Language** | Corner radius style (sharp 0-2px, subtle 4-6px, medium 8-12px, rounded 16+px, pill), shadow depth (none/subtle/moderate/prominent), border usage pattern | `--radius-*`, `--shadow-*`, `--border-thin/default/thick` |
| **5. Visual Patterns** | Card-heavy or flat/borderless layout, icon style (outlined/solid, thin/regular stroke), opacity usage (transparent overlays, disabled states), border widths (hairline 1px, default 1-2px, thick 2-3px) | `--opacity-*`, `--border-*` |
| **6. Tone** | Professional/corporate, playful/casual, minimal/clean, bold/dramatic, organic/natural — and implied audience (enterprise, consumer, creative, developer) | Informs semantic color derivation and font selection |
| **7. Structured Output** | Compile a mapping table: each extracted value → specific token name and estimated value | Feeds directly into Phase 3 token creation |

**If no reference image exists:** Skip this extraction and rely on CollectUI visual research + web search + fallback tables. The remaining phases work identically — the image extraction is an enhancement that provides higher-fidelity starting values, not a requirement.

Use extracted values as the PRIMARY design direction — research supplements, not overrides

**Web research (always runs):** Use `WebSearch` to study the domain's design conventions. Identify five pillars: color palette, typography, imagery themes, screen inventory, and UI density/tone. Document findings as a design brief.

**Typography is research-driven, not table-driven.** Run specific font research queries (e.g., `"bakery website fonts 2026"`, `"best Google Fonts for bakery"`) and validate against 3–5 real websites in the domain. The font pairing table in `domain-research-guide.md` is a fallback — always prefer research-validated choices. See `references/domain-research-guide.md`.

**Priority order for design decisions:** Reference image > Collect UI visual research > User preferences > Web research > Fallback tables.

**⛔ REVIEW — Design Brief**

Present the research findings as a design brief:

```
Design Brief — [Domain]

Colors:
  Primary:    [hex] ([description])
  Secondary:  [hex] ([description])
  Accent:     [hex] ([description])
  Background: [hex] ([description])

Typography:
  Heading:    [font name]
  Body:       [font name]
  Mono:       [font name]
  Weights:    [list observed: regular, semibold, bold, etc.]
  Tracking:   [tight headings / normal body / wide caps]

Shape & Depth:
  Radius:     [sharp / subtle / medium / rounded / pill]
  Shadows:    [none / subtle / moderate / prominent]
  Borders:    [hairline / default / thick]

Layout:
  Density:    [spacious / moderate / compact]
  Icon style: [outline / solid, thin / regular]

Tone:       [2-3 adjectives]
Source:     [reference image / CollectUI / web research]
Based on:   [list 2-3 reference sites or image description]
```

**[c]** Continue to token creation
**[r]** Redo — tell me what to change (e.g., "use teal instead of brown")
**[s]** Skip to final verification

**WAIT for user input. Do NOT proceed.**

### Phase 2 — Initialize the Pencil Document

**Step 1 — CHECK for an existing document FIRST:**
Call `get_editor_state({ include_schema: true })`. Read the response carefully. Look at the `filePath` field.

**⛔ STOP AND DECIDE — do NOT skip this check:**
- **If `filePath` contains a `.pen` file** (e.g., `design.pen`, `project.pen`, anything ending in `.pen`): **USE THAT FILE. Do NOT call `open_document` at all.** The document is already open. Save the `filePath` for all subsequent calls.
- **ONLY if `filePath` is empty/null/undefined** (meaning NO `.pen` file is open): Create a named file: `open_document("./[domain]-design-system.pen")`. Always prefix with `./`.

**NEVER call `open_document("new")`.** This creates a generic `pencil-new.pen` that ignores the existing file.
**NEVER call `open_document` if a `.pen` file is already open.** This creates a SECOND document.

**Step 2** — Call `get_guidelines({ topic: "design-system" })`.
**Step 3** — Call `get_style_guide_tags()` then `get_style_guide({ tags: [...] })` with 5–10 domain-matching tags.
**Step 4** — Call `get_variables({ filePath })` to check for existing tokens.

Merge the style guide with Phase 1 research to form the final design direction.

### Phase 3 — Create Design Tokens

Call `set_variables` to create the full token system (~89 tokens). Every color, font, radius, spacing, shadow, font size, line height, font weight, letter spacing, sizing, opacity, and border width is a variable.

**Handling user-specified colors:** If the user provided color preferences (e.g., "terracotta and cream"), map them to the appropriate tokens (`--primary`, `--background`, `--accent`) and derive the rest of the palette (secondary, muted, foregrounds, borders) to complement. The industry palette tables are starting points, not mandates.

**Post-creation color changes:** Since all components use `$--` token references (not hardcoded hex), calling `set_variables` again with new color values updates the entire design system instantly — every component, pattern, and screen inherits the change. No per-node updates needed.

**Token categories:**

| Category | Count | Examples |
|----------|-------|---------|
| Core colors | 19 | `--background`, `--foreground`, `--primary`, `--secondary`, `--muted`, `--accent`, `--destructive`, `--border`, `--input`, `--ring` |
| Semantic colors | 8 | `--color-success`, `--color-warning`, `--color-error`, `--color-info` + foregrounds |
| Typography | 3 | `--font-primary`, `--font-secondary`, `--font-mono` |
| Border radius | 6 | `--radius-none` (0) through `--radius-pill` (9999) |
| Spacing | 12 | `--space-1` (4) through `--space-24` (96) |
| Shadows | 4 | `--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--shadow-xl` |
| Font sizes | 9 | `--text-xs` (12) through `--text-5xl` (48) |
| Line heights | 3 | `--leading-tight` (1.25), `--leading-normal` (1.5), `--leading-relaxed` (1.75) |
| Font weights | 6 | `--weight-thin` ("200") through `--weight-bold` ("700") |
| Letter spacing | 4 | `--tracking-tight` (-0.5) through `--tracking-wide` (1.5) |
| Sizing | 9 | `--size-icon-sm` (16), `--size-avatar-md` (40), `--size-button-height` (40), `--size-sidebar-width` (240) |
| Opacity | 3 | `--opacity-disabled` (0.5), `--opacity-hover` (0.8), `--opacity-overlay` (0.6) |
| Border widths | 3 | `--border-thin` (1), `--border-default` (1.5), `--border-thick` (2) |

**Semantic colors MUST be derived from the primary palette.** Match the temperature (warm/cool), saturation, and lightness of your primary/accent colors. Do NOT use default Tailwind green/amber/red/blue (`#22C55E`, `#F59E0B`, `#EF4444`, `#3B82F6`). A warm muted palette needs warm muted semantics (sage green, golden amber, terracotta red, dusty blue). A cool vivid palette needs cool vivid semantics (teal-green, gold, crimson, blue). See `references/design-tokens-reference.md` for the derivation algorithm and per-industry examples.

**CRITICAL — Exact `set_variables` format.** Copy this structure exactly. Do NOT deviate.

CORRECT format for **color tokens** (themed — light + dark):
```json
{
  "--primary": {
    "type": "color",
    "value": [
      { "value": "#3E2723", "theme": { "mode": "light" } },
      { "value": "#D7CCC8", "theme": { "mode": "dark" } }
    ]
  }
}
```

CORRECT format for **non-color tokens** (no theme needed):
```json
{
  "--font-primary": { "type": "string", "value": [{ "value": "Fraunces, serif" }] },
  "--radius-md":    { "type": "number", "value": [{ "value": 6 }] },
  "--text-base":    { "type": "number", "value": [{ "value": 16 }] },
  "--space-4":      { "type": "number", "value": [{ "value": 16 }] }
}
```

WRONG — these will break theming:
```json
// WRONG: empty theme object — light/dark switching will NOT work
{ "value": "#3E2723", "theme": {} }

// WRONG: missing theme entirely on colors — both values collapse to same
{ "value": [{ "value": "#3E2723" }, { "value": "#D7CCC8" }] }

// WRONG: "themes" key in variables object — causes error
{ "themes": { "mode": ["light", "dark"] }, "--primary": { ... } }

// WRONG: "values" (plural) instead of "value"
{ "--primary": { "type": "color", "values": [...] } }
```

**Post-creation verification (MANDATORY):** After calling `set_variables`, immediately call `get_variables` and check EVERY color token. Each must show:
- `"theme": {"mode": "light"}` on the first value
- `"theme": {"mode": "dark"}` on the second value

If ANY color shows `"theme": {}` (empty object) or missing theme keys, the format was WRONG. Delete all variables and redo with the correct format above. Do NOT proceed to Phase 4 with broken themes.

See `references/design-tokens-reference.md` for full JSON payloads.

**⛔ REVIEW — Tokens**

Call `get_variables` and present results:

```
Tokens Created — [count] total

| Category        | Count | Status      |
|-----------------|-------|-------------|
| Core colors     | 19    | light+dark  |
| Semantic colors | 8     | light+dark  |
| Typography      | 3     |             |
| Border radius   | 6     |             |
| Spacing         | 12    |             |
| Shadows         | 4     |             |
| Font sizes      | 9     |             |
| Line heights    | 3     |             |

[any warnings: missing themes, wrong format, etc.]
```

**[c]** Continue to Foundations
**[r]** Redo — tell me what to change
**[s]** Skip to final verification

**WAIT for user input. Do NOT proceed.**

### Phase 4 — Build Foundations (Visual Documentation)

Create the Foundations section frame at the left of the canvas with `width: 1440, height: "fit_content", layout: "vertical"`. **Do NOT use fixed heights** — use `height: "fit_content"` so the frame grows to fit all content. Inside it, build 11 visual documentation frames:

1. **Color Palette** — Labeled swatches for all 27 color tokens. **Split into rows of max 5-6 swatches each** to prevent horizontal overflow. Use multiple horizontal rows inside a vertical container (e.g., Row 1: Primary, Secondary, Accent, Background, Card. Row 2: Success, Warning, Destructive, Muted, Input, Border. Row 3: Foregrounds + remaining). Each swatch is ~140-160px wide — 6 swatches + gaps fit within 1280px content width.
2. **Typography Scale** — 6 specimens (H1 → Caption) rendered at real sizes with metadata labels.
3. **Spacing Scale** — 12 visual blocks showing each spacing value with labels. Use 2 rows of 6 blocks each.
4. **Elevation** — 4 cards demonstrating shadow levels in a single horizontal row.
5. **Border Radius** — 6 rectangles showcasing each radius token in a single horizontal row.
6. **Font Sizes** — 9 text samples rendered at actual `--text-xs` through `--text-5xl` sizes with token name + pixel value labels.
7. **Font Weights** — Same sample text rendered in each of the 6 weight tokens (`--weight-thin` through `--weight-bold`).
8. **Semantic Colors** — 4 large card-like swatches for success/warning/error/info, each showing the color paired with its foreground.
9. **Sizing** — Visual rectangles showing icon sizes (sm/md/lg), avatar sizes (sm/md/lg), button height, and input height.
10. **Shadows & Borders** — Expanded elevation section showing 4 shadow levels + 3 border width examples + 3 opacity examples.
11. **Letter Spacing** — Same text rendered at each `--tracking-*` value with labels.

**Critical: Use a neutral white backdrop (`fill: "#FFFFFF"`), NOT the design system's own `$--background` token.** The Foundations section is documentation chrome — using the themed background (e.g., cream for a bakery, blue-gray for SaaS) makes light swatches like `--card`, `--secondary`, and `--muted` nearly invisible. A neutral white surface lets every color be evaluated accurately against a known reference. Swatches use `$--` tokens for their fills; only the documentation frame itself is neutral.

These are documentation frames, NOT reusable components. They use `$--` tokens for swatch fills everywhere. See `references/foundations-specs.md` for exact `batch_design` code (spread across Batches A–J within 25-op limits).

After each batch, call `get_screenshot` to verify rendering.

**⛔ REVIEW — Foundations**

Call `get_screenshot` on the Foundations frame and present:

```
Foundations Complete

Sections built:
 - Color Palette (27 swatches)
 - Typography Scale (6 specimens)
 - Spacing Scale (12 blocks)
 - Elevation (4 shadow levels)
 - Border Radius (6 shapes)
 - Font Sizes (9 samples)
 - Font Weights (6 weight samples)
 - Semantic Colors (4 status cards)
 - Sizing (icons, avatars, buttons, inputs)
 - Shadows & Borders (shadows + border widths + opacity)
 - Letter Spacing (4 tracking samples)

[screenshot]
[any visual issues: blank swatches, overlap, clipping]
```

**[c]** Continue to Components
**[r]** Redo — tell me what to fix
**[s]** Skip to final verification

**WAIT for user input. Do NOT proceed.**

### Phase 4b — Build Icon Library

Build a documentation frame inside Foundations (after the Letter Spacing section) containing a curated set of **42 Lucide icons** organized into 6 categories. This makes the design system self-documenting — users can see all available icons at a glance.

**Structure:**

| Category | Icons (7 each) |
|----------|---------------|
| Navigation | `house`, `arrow-left`, `arrow-right`, `chevron-down`, `menu`, `search`, `x` |
| Action | `plus`, `minus`, `edit`, `trash-2`, `download`, `upload`, `copy` |
| Status | `check`, `circle-check`, `circle-x`, `triangle-alert`, `info`, `loader`, `clock` |
| Social | `share`, `heart`, `star`, `bookmark`, `message-circle`, `bell`, `user` |
| Media | `image`, `camera`, `play`, `pause`, `volume-2`, `mic`, `film` |
| Misc | `settings`, `filter`, `eye`, `eye-off`, `lock`, `unlock`, `globe` |

Each icon rendered as:
```javascript
iconFrame=I(categoryRow, { type: "frame", layout: "vertical", gap: 6, alignItems: "center", width: 80, padding: [12, 8, 12, 8] })
icon=I(iconFrame, { type: "icon_font", iconFontFamily: "lucide", iconFontName: "[name]", width: 24, height: 24, fill: "$--foreground" })
iconLabel=I(iconFrame, { type: "text", content: "[name]", fontFamily: "$--font-mono", fontSize: 10, fill: "$--muted-foreground", textAlignHorizontal: "center" })
```

Each category row = ~23 ops (1 title + 1 row frame + 7 icons × 3 ops). Total: 6 `batch_design` calls.

**Domain adaptation:** Supplement the base 42 icons with domain-specific icons:
- **Food/Bakery:** `utensils`, `cake`, `coffee`, `wine`, `shopping-bag`
- **SaaS/Dashboard:** `layout-dashboard`, `bar-chart-2`, `database`, `cloud`, `webhook`
- **Fitness:** `dumbbell`, `timer`, `activity`, `trophy`, `flame`
- **E-commerce:** `shopping-cart`, `package`, `truck`, `credit-card`, `tag`

**IMPORTANT:** Use explicit pixel values (24) for `icon_font` width/height — variable references like `$--size-icon-lg` may resolve to 0 for `icon_font` nodes.

No review gate here — continue directly to Phase 5.

### Phase 5 — Build Base Components (~15 Primitives)

Create the Components section frame to the right of Foundations with `width: 1440, height: "fit_content", layout: "vertical", fill: "#FFFFFF"` (same neutral backdrop rationale as Foundations — light-fill variants like Ghost buttons and muted badges need a known white reference). **Do NOT use fixed heights** — use `height: "fit_content"`.

**⚠ CRITICAL STRUCTURE FOR EACH BATCH:**
1. Create a **category frame** (`layout: "vertical"`, `width: "fill_container"`) inside Components section
2. Add a category title text
3. Create a **display row** (`layout: "horizontal"`, `gap: 16`, `width: "fill_container"`) inside the category
4. Insert components into the display row — NOT directly into the Components section
5. **If elements overlap after batch_design, the parent frame is missing `layout` — fix immediately**

| Batch | Category | Components | Count |
|-------|----------|-----------|-------|
| 1 | Buttons | Category (vertical) → Row (horizontal) → Primary, Secondary, Outline, Ghost, Destructive | 5 |
| 2 | Inputs | Category (vertical) → Row (horizontal) → TextField, Textarea, Select, InputGroup | 4 |
| 3 | Typography | Category (vertical) → H1, H2, H3, Body, Caption, Label stacked | 6 |
| 4 | Badges | Category (vertical) → Row (horizontal) → Default, Success, Warning, Error | 4 |
| 5 | Alerts | Category (vertical) → Info, Success, Warning, Error stacked | 4 |

Every component has `reusable: true`, uses only `$--` tokens, and follows `"Category/Variant"` naming. See `references/component-specs.md`.

**MANDATORY — Post-Batch Validation (after EVERY batch_design call):**
1. Check the batch response for "unknown properties were ignored" warnings — fix immediately.
2. Call `get_screenshot` on the affected section — visually confirm no overlapping elements, no invisible shadows, no broken layouts.
3. **If ANY elements overlap or stack on top of each other, the parent frame is missing `layout: "horizontal"` or `layout: "vertical"`.** Fix it before proceeding to the next batch.

### Phase 6 — Build Composite Components (~10 Composites)

Continue inside the Components section frame, adding category sub-frames for each composite group.

| Batch | Category | Components | Count |
|-------|----------|-----------|-------|
| 6 | Card | Header + Content + Actions slots | 1 |
| 7 | Navigation | Sidebar container, ActiveItem, DefaultItem, SectionTitle | 4 |
| 8 | Table | Wrapper, HeaderRow, DataRow | 3 |
| 9 | Tabs | Container, ActiveTab, InactiveTab | 3 |
| 10 | Breadcrumbs | Item, Separator, ActiveItem | 3 |
| 11 | Pagination | Container, PageItem, ActiveItem, PrevNext | 4 |
| 12 | Modal | Dialog with Header/Body/Footer | 1 |
| 13 | Dropdown | Container, Item, Divider, SectionTitle | 4 |
| 14 | Misc | Avatar, Divider, Switch, Checkbox, Radio | 5 |

After batches 8, 11, and 14: run `get_screenshot` and `snapshot_layout({ problemsOnly: true })`. Fix issues immediately. See `references/component-specs.md`.

**⛔ REVIEW — Components**

Call `batch_get({ patterns: [{ reusable: true }] })`, `get_screenshot`, and `snapshot_layout({ problemsOnly: true })`. Present:

```
Components Created — [count] reusable

| Category    | Components                              | Count |
|-------------|----------------------------------------|-------|
| Buttons     | Primary, Secondary, Outline, Ghost, Destructive | 5 |
| Inputs      | TextField, Textarea, Select, InputGroup | 4 |
| Typography  | H1, H2, H3, Body, Caption, Label      | 6 |
| Badges      | Default, Success, Warning, Error       | 4 |
| Alerts      | Info, Success, Warning, Error          | 4 |
| Card        | Header + Content + Actions             | 1 |
| Navigation  | Sidebar, Active, Default, SectionTitle | 4 |
| Table       | Wrapper, HeaderRow, DataRow            | 3 |
| ...         | [remaining composites]                 | ... |

[screenshot]
[layout issues from snapshot_layout, if any]
```

**[c]** Continue to Patterns
**[r]** Redo — tell me what to fix
**[s]** Skip to final verification

**WAIT for user input. Do NOT proceed.**

### Phase 7 — Build Patterns (Composition Showcases)

Create the Patterns section frame to the right of Components with `width: 1440, height: "fit_content", layout: "vertical"`. Build 4 composition showcases that demonstrate real usage of the components:

1. **Form Pattern** — Vertical stack (`layout: "vertical"`) of InputGroup refs + Submit button.
2. **Data Display Pattern** — Table ref with populated rows + Pagination ref, stacked vertically.
3. **Navigation Pattern** — Horizontal layout with sidebar (left, `layout: "vertical"`, width: 240px) + content area (right, `layout: "vertical"`, `width: "fill_container"`). **The sidebar frame MUST have `layout: "vertical"`** so nav items stack. Each nav item is a separate text/ref element inside the sidebar.
4. **Card Layout Pattern** — Horizontal row of populated Card refs (`layout: "horizontal"`, `gap: 24`). Use `width: "fill_container"` on cards to distribute evenly. **Add domain-relevant stock images** to each card using `G(imageFrame, "stock", "[domain] keyword")` — e.g., for a coffee shop: `"latte art"`, `"coffee beans"`, `"barista"`.

**Using images (`G()` operation):**
- Card images: Insert a frame (e.g., `width: "fill_container", height: 200`) inside the card, then `G(frame, "stock", "[domain keyword]")`
- Avatar components: `G(avatarFrame, "stock", "professional portrait")`
- Hero sections in screens: `G(heroFrame, "stock", "[domain] hero")`
- Use `"stock"` for realistic photos, `"ai"` for custom/branded visuals
- Always insert the frame FIRST, then apply `G()` — images are fills on frames, not separate nodes

**Layout rules for patterns:**
- Every frame that arranges children horizontally MUST have `layout: "horizontal"`
- Every frame that stacks children vertically MUST have `layout: "vertical"`
- Sidebar/nav containers are ALWAYS `layout: "vertical"`
- Content areas with mixed content are ALWAYS `layout: "vertical"`

Each pattern uses only `ref` instances + `$--` tokens. **After each pattern, run the Post-Batch Validation** (screenshot + check for overlapping/broken layouts). See `references/screen-patterns.md`.

**⛔ REVIEW — Patterns**

Call `get_screenshot` on the Patterns frame and present:

```
Patterns Complete — 4 composition showcases

 1. Form Pattern       — InputGroup refs + Submit button
 2. Data Display       — Table ref + Pagination ref
 3. Navigation Pattern — Sidebar + Breadcrumbs + Tabs refs
 4. Card Layout        — Grid of populated Card refs

[screenshot]
[any layout or ref issues]
```

**[c]** Continue to Screens (or skip to verification if no screens requested)
**[r]** Redo — tell me what to fix
**[s]** Skip to final verification

**WAIT for user input. Do NOT proceed.**

### Phase 8 — Create Domain Screens *(only if user requests)*

**Skip this phase unless the user explicitly asks for screens** (e.g., "build screens for a bakery", "I need a landing page and menu screen", "create example screens"). The core deliverable is Foundations + Components + Patterns — screens are an optional add-on.

If the user requests screens, build 3–5 placed to the right of the Patterns section. Each screen uses only component `ref` instances and `$--` variable tokens.

**Per-screen workflow:**
1. Call `find_empty_space_on_canvas({ direction: "right", width: 1440, height: 900, padding: 100 })`.
2. Insert screen frame at returned position.
3. Build layout with component refs. Customize via `U(instanceId+"/descendantId", {...})`.
4. Add domain imagery via `G()`.
5. Call `get_screenshot` to verify.

See `references/screen-patterns.md` for domain-specific screen templates.

**⛔ REVIEW — Domain Screens** *(only if Phase 8 was executed)*

Call `get_screenshot` on each screen and present:

```
Domain Screens — [count] created

 1. [Screen Name] — [brief description]
 2. [Screen Name] — [brief description]
 ...

[screenshots]
[any issues: missing refs, hardcoded values, layout problems]
```

**[c]** Continue to Business Logic Screens (or verification)
**[r]** Redo — tell me what to fix
**[s]** Skip to final verification

**WAIT for user input. Do NOT proceed.**

### Phase 8b — Business Logic Screens *(only if user provides requirements)*

**Skip this phase unless the user provides specific product requirements, user flows, or feature specs.** This differs from Phase 8 (generic domain screens) — here the user supplies their actual business logic and the AI designs screens tailored to it.

The user might provide:
- User flows: "checkout: cart → address → payment → confirmation"
- Feature specs: "CRM with contact list, deal pipeline kanban, activity timeline"
- A PRD or user story document
- Wireframe descriptions: "onboarding wizard with 4 steps"

**Workflow:**
1. Read existing components: `batch_get({ patterns: [{ reusable: true }], readDepth: 2 })`.
2. Read existing tokens: `get_variables({ filePath })`.
3. Plan screens based on user requirements — map each user flow or feature to a screen.
4. For each screen:
   a. Call `find_empty_space_on_canvas({ direction: "right", width: 1440, height: 900, padding: 100 })`.
   b. Insert screen frame at returned position.
   c. Build layout using existing component `ref` instances.
   d. Customize content via `U(instanceId+"/descendantId", {...})` with realistic business data.
   e. Add imagery via `G()` where appropriate.
   f. Call `get_screenshot` to verify.

**⛔ REVIEW — Business Logic Screens**

Call `get_screenshot` on each screen and present:

```
Business Logic Screens — [count] created

 1. [Screen Name] — maps to: [which user requirement/flow]
 2. [Screen Name] — maps to: [which user requirement/flow]
 ...

[screenshots]
[any issues or gaps vs requirements]
```

**[c]** Continue to Layout Enforcement
**[r]** Redo — tell me what to fix
**[s]** Skip to final verification

**WAIT for user input. Do NOT proceed.**

### Phase 9 — Layout Enforcement Pass (MANDATORY)

**Why this exists:** The AI consistently drops `layout: "horizontal"` from frames during generation, even when specs include it. This pass programmatically catches and fixes every missing layout. **This phase is NOT optional — skip it and the design will have broken layouts.**

**Step 1 — Collect all frames with flex properties.**
```
batch_get({ filePath, patterns: [{ type: "frame" }], searchDepth: 10, readDepth: 0 })
```
Search within EACH top-level section (Foundations, Components, Patterns, and any screens).

**Step 2 — Identify frames needing layout enforcement.**
From the results, find every frame that has ANY of: `gap`, `alignItems`, `justifyContent` — regardless of whether `layout` already appears (since `batch_get` doesn't display `layout: "horizontal"` in its output — it's considered the default).

**Step 3 — Bulk-apply `layout: "horizontal"` to ALL identified frames.**
```javascript
U("frameId1", { layout: "horizontal" })
U("frameId2", { layout: "horizontal" })
// ... for every frame with gap/alignItems/justifyContent
```
Exclude frames that should be vertical (identifiable by name: category sections, form containers, vertical stacks). Apply `layout: "vertical"` to those instead.

**Step 4 — Verify shadows use hex colors.**
Check any frame with `effect` property. If `color` uses `rgba()` format, replace with 8-digit hex `#RRGGBBAA`.

**Step 5 — Screenshot every section** to confirm no overlapping elements.

This is safe to run multiple times — setting `layout: "horizontal"` on a frame that already has it is a no-op.

### Phase 10 — Final Verification

Run comprehensive QA. Fix every issue before presenting to the user.

1. **Visual** — `get_screenshot` on Foundations, Components, Patterns (and screens if created). Check alignment, spacing, typography, color, overflow.
2. **Layout** — `snapshot_layout({ problemsOnly: true })` to detect clipping/overflow. Fix all.
3. **Token audit** — `search_all_unique_properties` for `fillColor`, `textColor`, `fontFamily`, `fontSize`. Replace leaked hex values and raw font sizes with `$--` tokens.
4. **Component audit** — `batch_get({ patterns: [{ reusable: true }] })`. Verify ~25 components.
5. **Organization audit** — Verify no orphan components at document root. All should be under Components section.
6. **Fix and re-verify** — Re-screenshot affected areas after fixes.
7. **Present** — Summarize tokens, components, patterns (and screens if created). Show key screenshots.

See `references/verification-checklist.md`.

### Phase 11 — Canvas Navigation Index

Create a small navigation index frame at the canvas origin (x: 0, y: 0) showing a map of all sections with their positions:

```
Design System Index
├── Foundations (x, y)
├── Components (x, y)
├── Patterns (x, y)
└── Screens (x, y) — only if screens were created
```

This helps users navigate the canvas. Only include the Screens entry if Phase 8 was executed.

### Phase 12 — Code Export *(optional, user-triggered)*

**Skip this phase unless the user explicitly requests code export** (e.g., "export to Tailwind", "convert to code", "generate React components", "export as CSS"). This phase converts the design system into production-ready Tailwind CSS + React components.

**Step 1 — Collect preferences.** Ask the user for:
- **Tailwind version:** v3 or v4
- **Framework:** Next.js or Vite+React

**Step 2 — Extract tokens.** Call `get_variables({ filePath })` to read all ~89 tokens. Categorize by type (color, number, string, shadow). Separate themed (light/dark) from static tokens.

**Step 3 — Read components.** Call `batch_get({ patterns: [{ reusable: true }], readDepth: 3, searchDepth: 3 })` to get every reusable component with its full node tree.

**Step 4 — Load Pencil's code generation guidelines.** Call `get_guidelines("code")` and `get_guidelines("tailwind")`. These are the **primary authority** for translating Pencil nodes to code — they cover component instance mapping, property-to-Tailwind-class translation, font wiring, and visual verification. Follow them for all translation work in Steps 8-9.

**Step 5 — Generate `globals.css`.** Build the CSS file with all tokens as CSS custom properties:
- **v3:** `:root` with HSL values (space-separated, no `hsl()` wrapper), `.dark` overrides, `@layer base` font utilities
- **v4:** `@import "tailwindcss"`, `@custom-variant dark`, `:root` with hex values, `.dark` overrides, `@layer base` font utilities

**Step 6 — Generate `tailwind.config.js` (v3 only).** Map all tokens to Tailwind utility names: colors via `hsl(var(--name))`, radii, shadows, font sizes, spacing, line heights.

**Step 7 — Generate font loading code.**
- **Next.js:** `layout.tsx` with `next/font/google` loader setting `--font-primary`, `--font-secondary`, `--font-mono` CSS variables
- **Vite+React:** `<link>` tags in `index.html` loading all three fonts from Google Fonts

**Step 8 — Generate component TSX files.** One file per component category (button.tsx, input.tsx, card.tsx, badge.tsx, alert.tsx, etc.). Each component:
- Uses only token-referencing Tailwind classes (no hardcoded hex)
- Has TypeScript interfaces with variant props where applicable
- Accepts and spreads an optional `className` prop
- Uses v3 mapped classes (`bg-primary`) or v4 arbitrary values (`bg-[var(--primary)]`) based on the chosen version

**Step 9 — Generate screen/page TSX files.** For each screen design in the .pen file:
1. Deep-read the screen frame: `batch_get({ nodeIds: [screenId], readDepth: 10, resolveInstances: true })`
2. Take a reference screenshot: `get_screenshot({ nodeId: screenId })`
3. Follow **Pencil's Component Implementation Workflow** (from Step 4's `get_guidelines("code")`):
   - Steps 1A-1C: Extract components, map ALL instances with ALL overrides and descendants
   - Step 2: Create React components using `get_guidelines("tailwind")` for property-to-class mapping
   - Step 3: Validate each component with `get_screenshot` — pixel-perfect match required
   - Step 4: Integrate into frame, verify instance count and prop completeness
4. Handle screen-level elements: semantic HTML for headings/labels/links, page wrapper, form behavior, icon name conversion, image fills
5. Assemble into a complete page file with all imports
6. Visually verify the rendered page against the Pencil screenshot — fix any discrepancies

See `references/code-export-guide.md` (Section 7) for the complete screen export workflow and common pitfalls.

## Critical Rules

**Rule 1 — Always reuse components.** Search with `batch_get({ patterns: [{ reusable: true }] })` before creating. On screens, every element must be a `ref` instance.

**Rule 2 — Never hardcode values.** All colors use `$--` tokens. All fonts use `$--font-*`. All radii use `$--radius-*`. All font sizes use `$--text-*`. Raw values only appear in `set_variables`.

**Rule 3 — Prevent overflow.** Constrain text with `width: "fill_container"`. Use layout frames. Validate with `snapshot_layout({ problemsOnly: true })`.

**Rule 4 — Verify visually.** Call `get_screenshot` after every major batch. Fix problems immediately.

**Rule 5 — Reuse assets.** Copy images with `C()` instead of regenerating with `G()`.

**Rule 6 — Domain coherence.** Every choice connects back to Phase 1 research.

**Rule 7 — Canvas organization.** All components go inside the Components section frame under categorized sub-frames. No components at document root. Foundations, Components, Patterns, and Screens flow left-to-right on the canvas.

## Component Inventory

| # | Component | Type | Variants |
|---|-----------|------|----------|
| 1–5 | Button | Primitive | Primary, Secondary, Outline, Ghost, Destructive |
| 6–9 | Input | Primitive | TextField, Textarea, Select, InputGroup |
| 10–15 | Typography | Primitive | H1, H2, H3, Body, Caption, Label |
| 16–19 | Badge | Primitive | Default, Success, Warning, Error |
| 20–23 | Alert | Primitive | Info, Success, Warning, Error |
| 24 | Card | Composite | Header + Content + Actions slots |
| 25–28 | Sidebar Nav | Composite | Container, ActiveItem, DefaultItem, SectionTitle |
| 29–31 | Table | Composite | Wrapper, HeaderRow, DataRow |
| 32–34 | Tabs | Composite | Container, ActiveTab, InactiveTab |
| 35–37 | Breadcrumbs | Composite | Item, Separator, ActiveItem |
| 38–41 | Pagination | Composite | Container, PageItem, ActiveItem, PrevNext |
| 42 | Modal/Dialog | Composite | Overlay + Content with slots |
| 43–46 | Dropdown | Composite | Container, MenuItem, Divider, SectionTitle |
| 47–51 | Miscellaneous | Composite | Avatar, Divider, Switch, Checkbox, Radio |

## References

Load the relevant file before starting each phase:

- **`references/pencil-mcp-guide.md`** — Complete Pencil MCP tool reference with examples and operation syntax.
- **`references/domain-research-guide.md`** — Domain research strategies, color psychology, font pairings, screen inventories.
- **`references/design-tokens-reference.md`** — Token architecture, `set_variables` JSON payloads, ~89 token definitions, industry palettes.
- **`references/foundations-specs.md`** — Visual foundation documentation: color palette, typography scale, spacing, elevation, radius `batch_design` code.
- **`references/component-specs.md`** — All ~25 component `batch_design` operation code with section frame organization.
- **`references/screen-patterns.md`** — Layout patterns, composition showcases, and domain-specific screen templates.
- **`references/verification-checklist.md`** — Visual QA, layout checks, token audits, canvas organization verification.
- **`references/code-export-guide.md`** — Tailwind CSS export: token extraction, v3/v4 templates, Pencil-to-Tailwind class cheatsheet, component translation, framework setup (Next.js / Vite+React).
