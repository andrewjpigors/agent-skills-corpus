---
name: surecart-design-to-shop-page
description: Convert a Claude Design export (from design.claude.com) representing a shop / collection / product-listing page into a SureCart `surecart/product-list` block with its full inner template (sort + filter + search + product-template grid + pagination + no-products fallback). ALSO ships an upstream INTAKE MODE (v0.8+): when invoked empty (no attached design), the skill runs a small 2-batch questionnaire and emits a constraint-aware Claude Design prompt the merchant pastes into design.claude.com — closing the merchant-to-markup loop for shop pages. Use when the merchant attaches a Claude Design project (zip / unzipped JSX/CSS / screenshot / URL) of a multi-product page and asks for shop-page markup, OR invokes empty to generate a design prompt. Output is one fenced ```html block of Gutenberg block markup the merchant pastes into the WordPress block editor — no MCP, no API keys, no server calls. Sibling skill to `surecart-design-to-blocks` (which targets single-product detail pages); they share the same emission conventions and validation rubric structure.
version: 0.8.1
---

# Convert Claude Design → SureCart shop / product-list page

> **v0.5.0 — Sibling-skill propagation gap fix (2026-05-27, 8-expert audit synthesis).** Skill was previously pinned to "HC#1–HC#31" from the sibling — out of date as sibling has shipped v7.12/v7.13/v7.14/v7.15 adding HC#32–HC#38 plus P11/P12/P13 primitives. **Bumped sibling reference to HC#1–HC#38.** Specifically critical for shop-page: HC#38 (registered block-style variations) means every per-card `surecart/product-quick-view-button` should emit `className:"is-style-show-on-hover"` so the quick-view UI is hover-revealed (not always-visible cluttering the card). Previously emitted bare blocks producing always-visible yellow "+ Add" buttons on every card. SHC#12 added: `surecart/product-quick-view-button` inside `surecart/product-template` MUST use `is-style-show-on-hover` unless design explicitly shows the always-visible variant. SHC#13 added: per-card surecart blocks (`product-list-price`, `product-scratch-price`, `product-review-average-rating-stars`, `product-sale-badge`) also have server-rendered chrome that may need wrap-and-target (HC#37) when designs have custom borders/backgrounds around them. SHC#14 added: shop-page sidebar position-sticky uses HC#33 (no inline `position:sticky` mirror — `is-position-sticky` class only).
>
> **v0.4.0 — `core/icon` native block support (WP 7.0+, 2026-05-26).** WordPress 7.0 shipped a native `core/icon` block resolving 88 built-in SVG icon slugs (arrow-*, chevron-*, cart, check, plus, star-{filled,empty,half}, info, search, menu, shield, etc.) via `WP_Icons_Registry`. This skill inherits the sibling skill's `reference/wp-core-blocks.md` core block reference where `core/icon` is now documented in full (attribute schema + 88-slug catalog + paste recipes). **Shop-page usage:** per-card chrome decorations (rating stars, sale-badge glyphs that aren't covered by `surecart/product-sale-badge`, quick-view arrows), filter-row chrome (search icon prefix, sort caret), and header/CTA glyphs (cart icon in nav, "view all" arrow). **Precedence:** prefer `core/icon` over inline-SVG `core/html` L1 fallback for any glyph matching a built-in slug. Paste form is always self-closing — `<!-- wp:icon {"icon":"core/cart"} /-->`. SHC#11 added (icon-glyph precedence). Mirrors sibling skill HC#32 / rubric B-28. See `../surecart-design-to-blocks/reference/wp-core-blocks.md § core/icon`. No paste-test required (additive change; all previously emitted markup still validates).
>
> **v0.3.0 — Second paste-test correction (Hearth & Hollow round 2, SUR-5186).** Added SHC#10: NO descriptive HTML comments anywhere inside a block's content area — only block delimiters. Raw section labels (`<!-- Header row -->`, `<!-- Card chrome -->`, `<!-- ONE card -->`) treat as freeform content during parse and silently drop the inner blocks for `apiVersion:3` strict-schema blocks (every `surecart/*` and `core/cover`/`core/group`). Cascades up through 7+ ancestor blocks. Same family as sibling skill's HC#22. Rubric A-10 added; `reference/start-basic-template.md` patched to mark its descriptive labels as `[SECTION-LABEL — STRIP BEFORE EMIT]`.
>
> **v0.2.0 — First paste-test corrections (Hearth & Hollow, SUR-5186).** Added SHC#8 (`is-position-<v>-<h>` class for `core/cover` with `contentPosition`) and SHC#9 (`has-border-color` class for top-level `border.color` literal on `core/cover` / `core/group`). Both surfaced as block-validation cascades that broke the entire shop page from a single inner-block failure. Rubric A-8 / A-9 added.
>
> **v0.1.0 — Initial scaffold (SUR-5186).** This skill mirrors the `surecart-design-to-blocks` architecture but targets multi-product listing pages instead of single-product detail pages. The block vocabulary, paste-safety rules, and rubric pattern are inherited from the sibling skill; what differs is the **emission target**: this skill outputs a `surecart/product-list` block (with full Start-Basic inner template) wrapped at the top level of the page, not a `surecart/product-page` wrapper.
>
> **What this skill does NOT do:** single-product detail pages (use `surecart-design-to-blocks`), cart drawers, checkout, customer dashboard. If the design is a hybrid (e.g., collection landing page with a featured product hero on top), emit two outputs — the shop-page block at the bottom and a separate fenced block for the hero region with a note to the merchant.

## Why this skill exists

SureCart's `surecart/product-list` is a top-level block (not nested inside `surecart/product-page`) with its own 16+ child block family — sort, filter, filter-tags, filter-checkboxes, search, product-template, pagination, sidebar, no-products fallback. Emitting it self-closed (`<!-- wp:surecart/product-list /-->`) renders a "Start Basic" template-picker placeholder in the editor — the same silent-failure mode as `product-review-list` (A-27) and `product-list-related` (A-28) on the product-page side. This skill emits the full Start-Basic template inline so the merchant's design renders on first paste.

The `surecart-design-to-blocks` skill enumerates the `product-list` family as auxiliary vocabulary but never composes a shop page. This skill is the dedicated workflow.

---

## Workflow (6 steps, do not skip any)

### Step 0 — Mode router (run first, no exceptions)

The skill has two operating modes. Decide which one to run before doing anything else. **This step mirrors the sibling skill `surecart-design-to-blocks` Step 0** — same decision tree, same defaults-to-intake policy.

Ask yourself, in order:

1. **Did the merchant attach a file, paste JSX/HTML/CSS, paste a non-Figma URL, or reference the 4 Claude-Design filenames** (`product-page.jsx` + `colors_and_type.css`)?
   → **CONVERT MODE.** Proceed to Step 1.

2. **Did the merchant say "I have a design"** or paste anything that looks like structured design output (JSX, HTML markup, CSS rules, design tokens)?
   → **CONVERT MODE.** Proceed to Step 1.

3. **Otherwise** — empty invocation, vague prose ("I want a shop page", "make me a collection grid", "help me list products"), no attached design.
   → **INTAKE MODE.** Read [`intake/questions.md`](intake/questions.md) and proceed there. Do NOT run Steps 1–5.

When uncertain, choose **INTAKE** — the intake opener tells the merchant *"if you already have a design, paste it now"*, which routes them back to convert mode on their next turn.

**Why this matters.** Convert mode (Steps 1–5) is the canonical conversion pipeline — its behavior is byte-frozen in v0.8 (verified against the shop-page fixture goldens via `intake-99-convert-contract.test.mjs`). Intake mode is new in v0.8 and only activates when the merchant has nothing to convert yet. It asks ~5 questions across 2 batches and emits a Claude Design prompt the merchant pastes into design.claude.com. Once they return with the resulting design, Step 0 routes them back to convert mode automatically.

**Sibling-skill symmetry.** The sibling `surecart-design-to-blocks` runs the same Step 0 decision tree with a product-detail-specific intake. Both skills share `intake/shared/*` assets (anti-patterns, palette presets, tone presets, typography presets) and `intake/constraint-digest.md` (single source of truth, generated from sibling's SKILL.md HC table). See `intake/README.md` for details.

> **Figma URLs.** A bare `figma.com/design/...` URL with no other design content remains a deferred input (per Step 1.0 Figma policy). Step 0 routes it to **INTAKE MODE**, and the intake opener asks the merchant to re-export as PNG or HTML+CSS. The Figma-defer policy is unchanged — only the surface where the merchant hears about it has moved.

---

### Step 1 — Read the design

#### Step 1.0 — Input router

Same 4-mode router as the sibling skill — detect which input the merchant provided and route accordingly:

| Input | Detection signal | Confidence | Path |
|---|---|---|---|
| **A. Claude Design project zip / unzipped / 4 files inline** | `product-page.jsx` + `sections-*.jsx` + `assets/colors_and_type.css` present | High | Step 1.A |
| **B. Single screenshot / image** | merchant attached `.png`/`.jpg`/`.webp` AND no JSX/CSS | Medium-Low | Step 1.B (vision extraction; activates Tier C rubric) |
| **C. HTML + CSS dump** | merchant pasted/attached `.html` + `.css` (or HTML with `<style>` blocks) | Medium-High | Step 1.C |
| **D. Live URL** | merchant pasted a `https://…` URL pointing at a published page | Medium-High (static) / Low (SPAs) | Step 1.D (`WebFetch` → 1.C) |

The extraction paths converge on the same intermediate representation as the sibling skill — see `surecart-design-to-blocks/SKILL.md` Step 1.A–1.D for the canonical extraction algorithms (JSX walk, vision section/typography/color/spacing/layout/asset extraction, HTML+CSS parse, `WebFetch` SPA-detection). Detailed re-emission is omitted here for brevity; reuse those algorithms verbatim.

> **Figma input:** not yet wired — deferred to a later release. If a merchant pastes a `figma.com/design/...` URL, ask them to export the frame as PNG (case B) or paste the rendered HTML+CSS (case C).
>
> **Figma MCP precedence (v0.6, mirrors sibling SKILL.md).** When the input is a `figma.com/design/...` URL AND the merchant has invoked this skill, this skill's deferral WINS over the Figma MCP server's auto-trigger. Do **NOT** call `mcp__claude_ai_Figma__*` tools (e.g. `use_figma`, `get_design_context`, `get_screenshot`). The Figma MCP server is a sibling capability whose tools are deferred until the design-extraction layer supports them natively. Ask the merchant to re-export as PNG or HTML+CSS instead.

**Shop-page-specific extraction additions:**

- **Grid detection.** Identify the product-card grid (the dominant N-up repeated card pattern). Count the columns at desktop width — this becomes `surecart/product-template`'s `layout.columnCount` or `layout.minimumColumnWidth` (responsive auto-fit). Typical values: 3-up (`columnCount:3`), 4-up (`columnCount:4`), or responsive (`minimumColumnWidth:"225px"` lets the grid reflow by card width).
- **Header chrome.** Identify the header row above the grid: sort dropdown, filter dropdown, search input, filter-tags. Map each to its `surecart/product-list-*` child block. Search input typically has a fixed `flexSize:"250px"` and sits on the right.
- **Sidebar detection.** Does the design have a sticky filter column on the left? If yes, this is the **sidebar variant** — emit `surecart/product-list-sidebar` with `position:sticky, top:0px` and `flexSize:"225px"` wrapping the filter blocks, and wrap the grid in a sibling `core/group` with `selfStretch:"fill"`.
- **Filter UI choice.** Designs that show checkbox-style filter groups (Color: ☐ Red ☐ Blue ☐ Green) map to `surecart/product-list-filter-checkboxes` + `-checkbox` template. Designs that show pill/tag-style filters map to `surecart/product-list-filter-tags` + `-filter-tag` template. Designs that show a single "Filter ▾" dropdown map to `surecart/product-list-filter`.
- **Card content scan.** Every card in the grid is inside `surecart/product-template`. Identify per-card elements: cover/featured-image (always `core/cover` with `useFeaturedImage:true`), sale badge, quick-view button, title, rating stars, price, scratch-price, list-price, color/variant chips. These are the inner blocks of the per-card `core/group` wrapper.
- **Pagination shape.** Number pagination (1 2 3 … 10) = full `surecart/product-pagination` triad (previous + numbers + next). "Load more" button-only = just `surecart/product-pagination-next` with a custom label. Infinite scroll = drop+log under `dropped_features`.

### Step 1.5 — Run the Design Extraction Pass

Same 8-category pixel checklist as the sibling skill (`surecart-design-to-blocks/reference/pixel-checklist.md` — lazy-load). Walk every section the design contains (header / filter-row / grid / pagination / footer / any landing-band above the grid). Silent drops are forbidden.

---

### Step 2 — Read these reference files

**EAGER (load on every conversion):**

1. **[reference/shop-page-blocks.md](reference/shop-page-blocks.md)** — curated vocabulary for `surecart/product-list` and its 16+ child blocks. Every `surecart/product-list-*` and `surecart/product-template`, `surecart/product-pagination`, `surecart/product-list-no-products` block in your output must come from this list.
2. **[reference/start-basic-template.md](reference/start-basic-template.md)** — the canonical Start-Basic inner template for `surecart/product-list` and the per-card structure inside `surecart/product-template`. Paste-verified against `packages/blocks-next/src/blocks/product-list/template.js` and `app/src/BlockLibrary/ProductListMigrationService.php:99-115`.

**LAZY (load on demand) — reuse from sibling skill:**

3. `../surecart-design-to-blocks/reference/alias-map.md` — the 6-row ❌/✅ alias rewrite table. Designer-time names (`surecart/variant-picker`, `surecart/quantity`, etc.) DO NOT EXIST in the inventory.
4. `../surecart-design-to-blocks/reference/core-blocks-cheatsheet.md` — paired-block contract with copy-pasteable exemplars. `core/columns`, `core/group`, `core/cover`, `core/buttons`, etc.
5. `../surecart-design-to-blocks/reference/style-conversion.md` — JSX `style={{}}` → Gutenberg attrs table. Rule 0 hierarchy, set-equality rule, hybrid color/spacing policy.
6. `../surecart-design-to-blocks/reference/theme-partial.json` — SureCart preset namespace (color palette slugs, spacing slugs, font-family slugs).
7. `../surecart-design-to-blocks/reference/token-aliases.json` — Claude-Design CSS-var → slug+hex resolver. D7 dual-emit policy.
8. `../surecart-design-to-blocks/reference/design-patterns.md` — Part 1 paste-safe primitives (P1–P10). Most shop-page cards compose from **P3 vertical icon-text card** (when cards have icons), **P4 bordered card chrome** (typical product card), and **P5 multi-card row** (when the grid is implemented as a flex row rather than `product-template` grid for narrow column counts).
9. `../surecart-design-to-blocks/reference/full-inventory.json` — all 153 SureCart blocks. Search this when uncertain about a `surecart/product-list-*` attribute schema.
10. `../surecart-design-to-blocks/reference/pixel-checklist.md` — 8-category Design Extraction Pass.
11. `../surecart-design-to-blocks/reference/custom-html-fallback.md` — 3-tier `core/html` fallback ladder. Applies to shop-page chrome that doesn't map to any SureCart or core block (e.g., decorative collection-banner with custom animation).

The shop-page skill is intentionally a thin layer over the sibling skill's reference base. Most paste-safety rules (Hard Constraints HC#1–HC#38 in `surecart-design-to-blocks/SKILL.md`) apply identically here — same `save()` behavior, same JSON parsing edge cases, same set-equality rules.

---

### Step 3 — Decompose the design, then compose the product-list

#### 3a. Decompose

Walk the design top-to-bottom. For each visually distinct horizontal band, identify:
1. **Its role** — header (logo/nav above the grid), collection-banner (hero band above the grid), filter-row (sort/search/filter chrome), product-grid (the main `product-template`), pagination (below grid), footer.
2. **Its layout** — vertical stack, sidebar+main split (sticky left sidebar + scrolling grid), single-column constrained.
3. **Its chrome** — background color, border, padding.
4. **Its content blocks** — which `surecart/product-list-*` children, which `core/*` blocks.

#### 3b. Pick the outer structure

The output is **one `surecart/product-list` block at the top level** with `align:"wide"` or `align:"full"` to match the design's container width:

```html
<!-- wp:surecart/product-list {"align":"wide","query":{"perPage":N,...}} -->
  <!-- header / filter row groups (children) -->
  <!-- surecart/product-template (with per-card inner) -->
  <!-- surecart/product-pagination triad -->
  <!-- surecart/product-list-no-products fallback -->
<!-- /wp:surecart/product-list -->
```

If the design has **content ABOVE the grid that's not filter/search chrome** (a hero band, a collection title, a landing CTA), emit those as `core/*` blocks **before** the `surecart/product-list` block, NOT inside it. The `product-list` block's children are reserved for filter/sort/search/grid/pagination chrome (per `template.js`).

#### 3c. Compose the Start-Basic template

**Mandatory:** Even when the design has fewer filter controls than the Start-Basic template, emit the FULL canonical Start-Basic template structure with the design's customizations applied. Self-closing or partial template = "Start Basic" picker UI shown in the editor.

The canonical Start-Basic template (paste-verified) lives in `reference/start-basic-template.md`. Customize per-design:
- `query.perPage` → matches the grid's items-per-page (count visible cards on page 1)
- `product-template.layout.columnCount` (or `minimumColumnWidth` for responsive) → matches the grid
- `product-template.style.spacing.blockGap` → matches the design's card gap
- Per-card group's `style` → matches the card chrome (background, border, radius, padding)
- Per-card inner blocks (title, price, rating, sale badge, quick-view button) → emit in source order matching the design

#### 3d. Filter UI fork

Pick **one** filter style per design — the canonical Start-Basic template uses **dropdown filter + tag chips**. Variants:

| Design shows… | Emit |
|---|---|
| Single "Filter ▾" dropdown + clear chips below | `product-list-filter` + `product-list-filter-tags` (default — what Start-Basic ships) |
| Checkbox group ("Color: ☐ Red ☐ Blue") | `product-list-filter-checkboxes` + `-checkbox` template inside `product-list-sidebar` |
| Pill-style multi-select chips | `product-list-filter-tags` + `-filter-tag` template (standalone, no dropdown) |
| Radio-button sort ("Sort: ○ Newest ○ Price ↑") | `product-list-sort-radio-group` + `-radio` template |
| Default dropdown sort | `product-list-sort` (default — what Start-Basic ships) |
| Sticky filter sidebar on the left | wrap filters in `product-list-sidebar` with `position:sticky, top:0px, flexSize:"225px"` |

---

### Step 4 — Emit ONE fenced ```html block (or write to file when large)

Same emission rules as the sibling skill:
- Single ` ```html ` fenced block when total markup is **< 5,120 bytes**
- All paste-safety rules apply — every HC from the primary skill (`surecart-design-to-blocks/SKILL.md`) is inherited unless explicitly overridden by an SHC# below
- For markup **≥ 5,120 bytes**, use the Write tool to save to `~/Desktop/{pattern-slug}.html` (slugify `metadata.patternName` per primary HC#1). When the file branch fires, HC#48 governs the chat response — see primary SKILL.md HC#48 for the exclusivity rule + the 3-platform paste-path (macOS `pbcopy`, Linux `xclip`/`wl-copy`, Windows PowerShell `Set-Clipboard`; NEVER `clip.exe`).
- Comment markers use the **unprefixed core form**: `<!-- wp:group -->`, NOT `<!-- wp:core/group -->`
- Apply the alias map before emit (rewrite designer-time names)
- HC#49 escape-character rule applies — no unescaped `<`, `>`, `&`, `\"`, `--` in any JSON string value

**Shop-page-specific outer-wrapper rule:** the top-level block is `surecart/product-list` (NOT `surecart/product-page`). The `metadata.name` and `metadata.patternName` go on the `surecart/product-list` block. Categories should include `"surecart_shop"` in `metadata.categories` (per the SureCart pattern-library convention).

```html
<!-- wp:surecart/product-list {"limit":null,"query":{...},"metadata":{"categories":["surecart_shop"],"patternName":"<slug>","name":"<title>"},"align":"wide"} -->
  …Start-Basic template body, customized for design…
<!-- /wp:surecart/product-list -->
```

---

### Step 5 — Self-validate (mandatory)

Walk through `rubric/self-validate.md` Tier A/B/C against the candidate output. State the result at the top of the response:

> Self-validation: Tier A 10/10, Tier B 5/5, Tier C skipped (input: zip).

If any item fails, fix and re-validate. Do not emit broken markup.

After the markup, emit a drift report — same JSON shape as the sibling skill (`input_type`, `sections_detected`, `blocks_emitted`, `dropped_features[]`, `color_snap_misses[]`, `classic_theme_readiness`, `b18_compliance`, `assets[]`).

Shop-page-specific drift-report fields:
- `grid_layout` — `{"type":"grid","columnCount":N}` or `{"type":"grid","minimumColumnWidth":"Npx"}`
- `filter_ui_chosen` — one of `"dropdown"`, `"checkboxes"`, `"tags"`, `"radio"` (the variant emitted)
- `sidebar` — `true` (emitted `product-list-sidebar`) or `false`
- `per_card_blocks_emitted` — array of block names emitted inside `product-template` for each card

Then the merchant-instructions block (same as sibling skill — open Code editor, paste, switch back to Visual).

---

## Hard constraints — read `surecart-design-to-blocks/SKILL.md` "Hard constraints" section

**Every hard constraint in the primary skill applies here verbatim unless explicitly overridden below.** Rather than version-pinning a numeric range (which goes stale every time the primary adds an HC), the sibling-skill convention is to reference primary HCs by their topic name where possible (e.g., "the no-comments rule", "the has-border-color always-emit rule"). The SHCs below are EITHER (a) shop-page-only rules the primary doesn't cover, OR (b) one-line pointers to the canonical primary HC where the shop-page emission inherits the rule.

**Quick map of which SHC# is unique vs. inherited:**

| SHC# | Status | Canonical home |
|---|---|---|
| SHC#1 (outer = product-list) | Unique | this file |
| SHC#2 (Start-Basic mandate) | Unique | this file + `reference/start-basic-template.md` |
| SHC#3 (product-template grid) | Unique | this file |
| SHC#4 (per-card content) | Unique | this file |
| SHC#5 (product-pagination triad) | Unique | this file |
| SHC#6 (product-list-no-products fallback) | Unique | this file |
| SHC#7 (filter ancestor constraint) | Unique | this file |
| SHC#8 (cover contentPosition class) | Unique today (PROMOTE to primary in PR2) | this file |
| SHC#9 (has-border-color literal) | Inherited from primary's has-border-color rule (per-side carve-out lifted into primary) | primary SKILL.md HC#21 |
| SHC#10 (no descriptive HTML comments) | Inherited rule + distinct silent-drop failure signature for `apiVersion:3` per-card templates | primary HC#45 + this SHC#10 (both kept) |
| SHC#11 (core/icon) | Inherited from primary's core/icon rule (shop-page slug examples lifted into primary) | primary HC#32 |
| SHC#12 (show-on-hover quick-view) | Unique (shop-page application of HC#38) | this file |
| SHC#13 (per-card wrap-and-target) | Inherited from primary's wrap-and-target rule (per-card nuance lifted into primary) | primary HC#37 |
| SHC#14 (sidebar sticky position) | Inherited from primary's sticky-position rule | primary HC#33 |

### SHC#1. Outer wrapper is `surecart/product-list`, NOT `surecart/product-page`

The top-level block in output is `<!-- wp:surecart/product-list ... -->...<!-- /wp:surecart/product-list -->`. Never wrap a shop page in `surecart/product-page` — that's the single-product context wrapper and will inject `surecart/product_id` context that the children don't expect, causing `apiVersion:3` parse errors.

### SHC#2. `surecart/product-list` MUST be paired with the full Start-Basic inner template (mirrors A-28)

Same failure mode as `surecart/product-list-related` on the product-page side (A-28 in sibling skill). Self-closing `<!-- wp:surecart/product-list /-->` renders a "Start Basic" template-picker placeholder UI in the editor, NOT the products grid. The placeholder is silent — no block-validation error, no recovery prompt — so the merchant doesn't know the paste failed until they look at the page in the editor.

**Always emit the full Start-Basic template.** See `reference/start-basic-template.md` for the canonical form.

### SHC#3. `surecart/product-template` is the grid container, NOT `core/columns` or `core/group` flex

The product grid inside `surecart/product-list` is always rendered by `surecart/product-template`. The `template.js` ships with `layout:{type:"grid",columnCount:4}` and `style.spacing.blockGap:"30px"`. Customize `columnCount` per design (or use `minimumColumnWidth` for responsive auto-fit) — but never substitute a `core/columns` or `core/group` flex for the grid. The product-template handles the WP_Query iteration server-side; substituting a static layout drops the products entirely.

### SHC#4. Per-card block content is the inner template of `surecart/product-template`

Inside `surecart/product-template`, the inner blocks describe the structure of ONE card — the server-side renderer repeats them per product. Do NOT emit N copies of the card block. The canonical per-card inner block tree (paste-verified):

```html
<!-- wp:surecart/product-template {"style":{"spacing":{"blockGap":"30px"}},"layout":{"type":"grid","columnCount":4}} -->
<!-- wp:group {"layout":{"type":"default"}} -->
<div class="wp-block-group">
  <!-- card chrome group (background, border, padding) -->
  <!-- wp:group {"style":{...},"layout":{"type":"constrained"}} -->
  <div class="wp-block-group ...">
    <!-- cover with useFeaturedImage + sale-badge + quick-view -->
    <!-- wp:cover {"useFeaturedImage":true,...} -->...<!-- /wp:cover -->
  </div>
  <!-- /wp:group -->
  <!-- product-title (level:2 for cards, not 1) -->
  <!-- wp:surecart/product-title {"level":2,...} /-->
  <!-- price row (list-price + scratch-price in flex) -->
  <!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap"}} -->
  <div class="wp-block-group">
    <!-- wp:surecart/product-list-price /-->
    <!-- wp:surecart/product-scratch-price /-->
  </div>
  <!-- /wp:group -->
</div>
<!-- /wp:group -->
<!-- /wp:surecart/product-template -->
```

`product-title` MUST be `level:2` on cards (not `level:1` — that's the page-h1 case and a card has many titles, not one).

### SHC#5. `surecart/product-pagination` paired with its 3 children

Same paste-safety rule as the canonical `surecart/product-pagination` in the sibling skill — pair it, don't self-close. The three children are:

```html
<!-- wp:surecart/product-pagination -->
<!-- wp:surecart/product-pagination-previous /-->
<!-- wp:surecart/product-pagination-numbers /-->
<!-- wp:surecart/product-pagination-next /-->
<!-- /wp:surecart/product-pagination -->
```

Omitting any of the 3 children renders a partial control. Self-closing the parent shows the picker.

### SHC#6. `surecart/product-list-no-products` paired with a `core/paragraph` fallback

```html
<!-- wp:surecart/product-list-no-products -->
<!-- wp:paragraph {"align":"center","placeholder":"Add text or blocks that will display when a query returns no products."} -->
<p class="has-text-align-center">No products found.</p>
<!-- /wp:paragraph -->
<!-- /wp:surecart/product-list-no-products -->
```

Self-closing `<!-- wp:surecart/product-list-no-products /-->` shows an empty placeholder when the query returns zero products. Always emit the paragraph fallback.

### SHC#7. Filter / sort block ancestor constraint

`surecart/product-list-sort`, `-filter`, `-filter-tags`, `-filter-checkboxes`, `-search`, and their `*-template` children all have `ancestor: ["surecart/product-list"]` in their `block.json`. Emitting them outside a `surecart/product-list` parent fails block registration at editor load. This is enforced automatically when SHC#1+SHC#2 hold.

### SHC#8. `core/cover` with `contentPosition` requires the matching `is-position-<v>-<h>` class

Discovered: v0.2.0 paste-test (Hearth & Hollow shop). The `core/cover` block's `save()` function emits an `is-position-<vertical>-<horizontal>` CSS class on the `<div class="wp-block-cover ...">` whenever `contentPosition` is set in attrs. The class is derived by replacing the space in the attribute value with a hyphen.

```html
<!-- contentPosition:"center left"  -->  <div class="wp-block-cover ... is-position-center-left ...">
<!-- contentPosition:"top center"   -->  <div class="wp-block-cover ... is-position-top-center ...">
<!-- contentPosition:"bottom right" -->  <div class="wp-block-cover ... is-position-bottom-right ...">
```

**Failure signature:** `Block validation failed for 'core/cover' (Object)`. The diff shows save() expects `is-position-X-Y` and the retrieved HTML is missing it. Cascades to every ancestor block (parent groups, product-template, product-template-container, product-list-content, product-list — they ALL fail validation when an inner block fails).

**Rule:** any time you emit `"contentPosition":"<vertical> <horizontal>"` in cover attrs, also emit `is-position-<vertical>-<horizontal>` in the cover div's class list (alongside `has-custom-content-position`). The companion `has-custom-content-position` class is also required whenever `contentPosition` is anything other than the default `"center center"`.

### SHC#9. Top-level `border.color` requires `has-border-color` class — inherited from primary HC#21 (v0.6 consolidation)

**Inherited rule, canonical home = primary SKILL.md HC#21.** The per-side-border carve-out documented here in v0.2.0–v0.5 has been lifted into HC#21 directly (see the "Per-side carve-out (v7.18.3)" subsection there). Discovered originally during Hearth & Hollow shop paste-test (v0.2.0).

**Reference:** `../surecart-design-to-blocks/SKILL.md` § HC#21 + the per-side carve-out table.

**Companion classes worth re-stating here for shop-page emit-time grep:**
- `has-background` — `style.color.background` literal hex set
- `has-<slug>-background-color` — `backgroundColor:"<slug>"` preset
- `has-text-color` — `style.color.text` literal hex set
- `has-<slug>-color` — `textColor:"<slug>"` preset
- `has-border-color` — top-level `style.border.color` set (per-side `border.top.color` etc. does NOT add this class)
- `has-link-color` — `style.elements.link.color.text` set

### SHC#10. NO descriptive HTML comments anywhere inside a block's content area

Discovered: v0.3.0 paste-test (Hearth & Hollow, second-round). When raw HTML comments (`<!-- Foo bar -->`) that are NOT block delimiters appear inside a block's content area — interleaved between child blocks, between `<div class="wp-block-cover__inner-container">` and its inner blocks, or anywhere in the rendered span — the Gutenberg parser treats them as freeform content. For `apiVersion:3` blocks (every `surecart/*` block and `core/cover`, `core/group` in strict-schema mode), this corrupts inner-block recognition: the children are **silently dropped during parse**, and the editor's `save()` re-emits an empty inner-block area.

**Failure signature:** `Block validation failed for 'core/cover'` (or core/group, or any surecart/*) with the diff showing save() outputs an EMPTY content area (`<div class="wp-block-cover__inner-container"></div>`) while the retrieved HTML contains the comment + the original block tree. Cascades up the ancestor chain — a single descriptive comment inside a per-card cover can brick the entire `surecart/product-list`.

**Allowed:**
- Block delimiters: `<!-- wp:foo -->`, `<!-- /wp:foo -->`, `<!-- wp:foo /-->` (self-closing).
- HTML comments INSIDE the `style="..."` attr of a tag (these are technically not HTML comments — they're attribute content).

**Forbidden (any of these inside a block content area):**
- `<!-- Header row: ... -->`
- `<!-- Card chrome: ... -->`
- `<!-- ONE card (server repeats per product) -->`
- `<!-- TODO: revisit padding -->`
- `<!-- Section: footer -->`
- Any HTML comment that does not match `<!-- wp:.../-->` or `<!-- /wp:... -->` syntax.

**Rule:** the emitted markup file contains ONLY block delimiters and the static HTML they wrap. No editorial or sectioning comments. If you need to mark sections for your own reference during composition, do it in a separate notes file — strip them before emit.

**This rule applies to `reference/start-basic-template.md`'s exemplar too** — the documented Start-Basic template uses descriptive comments for readability ("Header row: sort + filter on the left, search on the right"), but those are LEARNING aids; when you copy that structure into emitted markup, strip the descriptive comments. The block delimiters are the only comments allowed in actual paste output.

**Cross-reference with primary HC#45 (v0.6 consolidation):** the primary skill's HC#45 documents the "Expected token of type EndTag, instead saw Comment" failure path. **SHC#10 stays as a separate sibling rule** because the shop-page per-card template path produces a DISTINCT failure signature — `apiVersion:3` per-card inner blocks are SILENTLY DROPPED during parse (no console error, no recovery prompt) when descriptive comments appear inside the per-card template. The merchant sees an empty card grid; the editor doesn't flag it. SHC#10 keeps the rule statement and the greppable enforcement specifically for this path; HC#45 handles the validateBlock-cascade variant. Both are anchored to the same `block-serialization-default-parser` tokenizer behavior.

### SHC#11. `core/icon` is the canonical block for built-in icon glyphs — inherited from primary HC#32 (v0.6 consolidation)

**Inherited rule, canonical home = primary SKILL.md HC#32.** The shop-page slug examples (search prefix, sort caret, cart icon, rating stars, load-more arrow, filter-clear, filter-checkbox tick, info tooltip, hamburger) have been lifted into HC#32 under "Most-emitted slugs on shop pages."

**Reference:** `../surecart-design-to-blocks/SKILL.md` § HC#32 + `../surecart-design-to-blocks/reference/wp-core-blocks.md § core/icon` (88-slug catalog).

### SHC#12. `surecart/product-quick-view-button` inside cards MUST use `is-style-show-on-hover` (v0.5)

Mirrors sibling HC#38. The block has a registered style variation `show-on-hover` that reveals the quick-view button on card hover (instead of always-visible). For shop-page emissions where the design has a per-card quick-view button (most do), emit with this className:

```html
<!-- wp:surecart/product-quick-view-button {"className":"is-style-show-on-hover"} /-->
```

**NOT** bare `<!-- wp:surecart/product-quick-view-button /-->` (which renders an always-visible button on every card, cluttering the grid).

**When to use bare/default form:** only when the design explicitly shows a persistent (always-visible) quick-view button on every card. Most product-grid designs hide the button by default and reveal on hover.

Other registered variations for shop-page-relevant blocks (per `../surecart-design-to-blocks/reference/surecart-blocks.md § Registered block-style variations`):

- `surecart/product-review-total-rating` — `isDefault:true` is `plus-sign`. OMIT `className` for the no-prefix variant (the common case). Emit `className:"is-style-default"` only for the dot-prefix variant.
- `surecart/product-review-average-rating-value` — `none` (default), `parentheses`, `slash`.

### SHC#13. Per-card surecart blocks with custom chrome → wrap-and-target — inherited from primary HC#37 (v0.6 consolidation)

**Inherited rule, canonical home = primary SKILL.md HC#37.** The per-card block list (`product-list-price`, `product-scratch-price`, `product-review-average-rating-stars`, `product-sale-badge`) has been lifted into HC#37 under "Shop-page per-card blocks." When the design shows custom chrome around any per-card element: FIRST check `reference/surecart-blocks.md § Registered block-style variations` (HC#38 path); if no variation fits, wrap-and-target per HC#37.

**Reference:** `../surecart-design-to-blocks/SKILL.md` § HC#37 + HC#38.

### SHC#14. Sticky sidebar position — inherited from primary HC#33 (v0.6 consolidation)

**Inherited rule, canonical home = primary SKILL.md HC#33.** When emitting `surecart/product-list-sidebar` with sticky positioning: JSON has `style.position.{type:"sticky",top:"0px"}`; wrapper class has `is-position-sticky`; inline `style=""` has NO `position:sticky;top:0px;z-index:N` mirror (save() routes position through class, not inline).

**Reference:** `../surecart-design-to-blocks/SKILL.md` § HC#33.

---

## When the design has elements with no SureCart shop-page block

Same fallback ladder as the sibling skill (`surecart-design-to-blocks/SKILL.md`):
1. Try a WP-core primitive first (`core/group` / `core/columns` / `core/image` / `core/heading`).
2. Try a SureCart block — search `full-inventory.json` for a block that matches the semantics.
3. Open `custom-html-fallback.md` and pick L1 / L2 / L3:
   - L1 static `core/html` for decorative chrome.
   - L2 Interactivity API piggyback ONLY on the 7 allowlist namespaces. `surecart/product-page` is one — but it's the single-product context; on a shop page, `surecart/cart` or `surecart/lightbox` are the relevant ones.
   - L3 drop + recommend `/surecart-new-block` for novel interactivity.

**Never invent a `surecart/product-list-*` child block name.** If the design needs a filter type not in the inventory (e.g., price range slider), drop+log under `dropped_features.type:"unsupported_filter"` with a `merchant_action` recommending `/surecart-new-block`.

---

## Reference structure

```
.claude/skills/surecart-design-to-shop-page/
├── SKILL.md                                ← you are here
├── reference/
│   ├── shop-page-blocks.md                 ← curated product-list family vocabulary
│   └── start-basic-template.md             ← canonical Start-Basic paste-verified template
├── examples/
│   └── patterns/                           ← 6 paste-tested exemplars (moved from sibling skill)
│       ├── INDEX.md
│       ├── list-standard.example.md        ← 9-up responsive grid with header
│       ├── list-sidebar.example.md         ← sticky filter sidebar + main grid
│       ├── list-carousel.example.md        ← 3-col grid with title + pagination
│       ├── list-row.example.md             ← compact 4-col grid
│       ├── list-bento.example.md           ← asymmetric bento grid
│       └── list-staggered.example.md       ← 2-col staggered
├── rubric/
│   ├── self-validate.md                    ← Tier A/B/C pre-emit checklist (shop-page-scoped)
│   └── merchant-recovery.md                ← copy-paste fixes if recovery / placeholder triggers
└── tests/
    └── fixtures/                           ← shop-page paste-test fixtures (empty in v0.1.0; populated through paste-test cycle)
```

The skill leans heavily on the sibling skill's reference base — see Step 2 LAZY section. Most paste-safety knowledge applies identically because the underlying `save()` and `validateBlock()` behavior is shared across all SureCart and WP core blocks.

---

## Quick reference (always-true facts)

- **`surecart/product-list` is the outer wrapper for shop pages.** Every `surecart/product-list-*` and `surecart/product-template` child belongs inside it.
- **`surecart/product-template` is `apiVersion:3` server-rendered and iterates products via WP_Query** — its inner blocks are the per-card template, repeated by the server.
- **The Start-Basic template MUST be emitted** — self-closing `surecart/product-list` shows a template-picker placeholder in the editor (silent failure, same family as A-27 / A-28 on the product-page side).
- **`align:"wide"` or `align:"full"`** at the top level — the shop page typically spans the theme's wide content area, not the default constrained width.
- **`level:2` on per-card `surecart/product-title`** — cards have N titles per page, not one h1.
- **Filter blocks have `ancestor:["surecart/product-list"]`** — they only render correctly inside a product-list parent.
