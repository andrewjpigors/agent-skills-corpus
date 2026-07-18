---
name: surecart-design-to-blocks
description: Convert a Claude Design export (zip, unzipped JSX+CSS, screenshot, HTML+CSS dump, or live URL) into SureCart product-page Gutenberg markup the merchant pastes into the WP block editor. ALSO ships an upstream INTAKE MODE (v7.22+): when invoked empty (no attached design), the skill runs a small 2-batch questionnaire and emits a constraint-aware Claude Design prompt the merchant pastes into design.claude.com — closing the merchant-to-markup loop. Use when the merchant attaches a Claude Design project AND asks for product-page markup, OR invokes empty to generate a design prompt. Output is ONE fenced ```html block (or a `~/Desktop/{slug}.html` file for markup >5KB). No MCP, API keys, or server calls — pure clipboard flow. The skill ships 69 hard constraints derived from production paste-tests (incl. T1-T5 multi-template campaign 2026-06-04 — HC#59-#66 covering product-template columns + axis labels + buy-buttons wrapper + button width attr + cover min-height path + mono slug + button aria-label + HC#45 grep enforcement, AND HC#67-#69 covering pixel-perfect typography: literal font-family dual-emit for ALL design typefaces + single-quote CSS escaping in inline style + cover min-height for hero/showcase), a paste-safe primitives library (P1–P13), a curated 25-block product-page vocabulary with alias enforcement, a registered-block-style-variations catalog (HC#38 — `is-style-orbit`/`is-style-show-on-hover`/etc.), 19 production-derived pattern exemplars + 5 pixel-perfect golds (T1 Aurora Pro Electronics, T2 Meridian Overcoat Fashion, T3 Hartwell Linen Sofa, T4 Daily Vitality Wellness, T5 Aurore Timepiece Luxury — all paste-tested 2026-06-04 with literal fonts + correct cover min-heights), and a ~52-item Tier A/B/C self-validation rubric. Use sibling skill `surecart-design-to-shop-page` for collection/shop-page designs (multi-product grids). Skip for: theme work, custom block scaffolding (`/surecart-new-block`), checkout/account templates.
version: 7.24.0
---

# Convert Claude Design → SureCart product page

Pure clipboard flow: design export → block markup the merchant pastes into the WP block editor. Past attempts (deterministic emitter, MCP server, server-side LLM) all failed in production. This skill works via curated vocabulary + literal anti-pattern tables + few-shot examples + mandatory self-validation.

## Doctrine reversals — recognized wrong forms

A handful of HCs REVERSE prior doctrine. If you see a paste-test report citing the wrong-form, the actual rule is the right-form in this table. Check the corresponding HC body for the full explanation.

| Topic | Wrong form (don't emit) | Right form (canonical) | HC |
|---|---|---|---|
| `has-border-color` on literal-hex border | OMIT class when border is literal-hex (v7.3) | ALWAYS emit `has-border-color` when `style.border.color` is set, regardless of slug-or-hex (v7.6) | HC#21 |
| `product-review-total-rating` className | Emit `className:"is-style-plus-sign"` (pre-v7.15) | OMIT className — `plus-sign` is `isDefault:true` (v7.15) | HC#19 |
| `core/group` sticky position | Inline `style="position:sticky;top:Npx;z-index:N"` mirror (v7.0 Exemplar 9) | `is-position-sticky` class only, NO inline mirror (v7.13) | HC#25 (unified) |
| `core/group` `style.dimensions.aspectRatio` | Inline `aspect-ratio:1` mirror | NEVER emit — drop+log, use `core/cover` or `padding-top` proxy (v7.7) | HC#25 (unified) |
| `core/cover` `isDark` rationale | "save() emits both is-light AND is-dark" (v7.17 prose) | save() emits `is-light` only; edit-time `setAttributes` overwrites JSON (v7.19 PR2). Rule unchanged: OMIT `isDark` from JSON when bg is set. | HC#42 |
| `core/cover` aspect-ratio inline mirror | Inline `aspect-ratio:X` for ALL cover variants (v7.0 Exemplar 8) | Inline-mirror ONLY when JSON uses top-level `aspectRatio`; `style.dimensions.aspectRatio` does NOT inline-mirror (v7.11) | HC#25 (unified) |
| `core/icon` slug catalog count | 90 slugs | 88 slugs (verified vs `wp-includes/assets/icon-library-manifest.php`) | HC#32 |
| Class order in `<a class="wp-block-button__link">` | "Trailing positions order-sensitive" (pre-v7.19) | Pure set-equality — order is convention only, NEVER validator-enforced (v7.19 PR2 — `validation/index.js:348-356`) | HC#34 / B-22 |
| HC#22 / HC#23 / HC#25 / HC#29 / HC#30 / HC#33 / HC#37 standalone | Each as its own rule (pre-v7.19) | HC#22 → merged into HC#45. HC#29 → absorbed by HC#23. HC#30 + HC#33 → unified into HC#25. HC#37 → fallback under HC#38. (v7.19 PR2) | various |
| `surecart/product-template` columns attribute | `"columns":N` (silently ignored) | `"layout":{"type":"grid","columnCount":N}` — emits `sc-product-template-columns-N` (v7.23.0) | HC#59 |
| `core/cover` `style.dimensions.minHeight` inline mirror | `"style":{"dimensions":{"minHeight":"Npx"}}` + inline `min-height:Npx` | `"minHeight":N,"minHeightUnit":"px"` top-level attrs (DO inline-mirror) — same family as HC#25 (v7.23.0) | HC#63 |
| `core/button` `width:N` inline mirror | Inline `style="width:N%"` on wrapper `<div>` | Wrapper class `has-custom-width wp-block-button__width-N` — no inline style (v7.23.0) | HC#64 |
| `aria-label` HTML attr on `core/button` `<a>` | `<a class="..." aria-label="...">` (no JSON backing) | Drop the attr OR use `core/icon` block (which DOES back ariaLabel) (v7.23.0) | HC#62 |
| Body-text font-family slug (any design typeface) | `fontFamily:"surecart-body"` slug-only — renders as theme `-apple-system` sans, not the design face | Literal `fontFamily:"'DM Sans', sans-serif"` (or `'Lora', serif`, `'Instrument Serif', serif`, etc.) on EVERY text-bearing block; mirror in inline `style` (v7.24.0) | HC#67 |
| Multi-word font-family in inline style | Double-quoted `font-family:"DM Sans", sans-serif` inside HTML `style="..."` — HTML parser truncates style at inner `"` | Single-quoted `font-family:'DM Sans', sans-serif` (HTML-safe, CSS-valid per W3C Fonts L4 §2.3) (v7.24.0) | HC#68 |
| Hero / showcase cover height for visual design | Cover with no `minHeight` attr — collapses to inner-content height (60-70% of design intent) | Top-level `minHeight:N, minHeightUnit:"px"` (per HC#63) when design specifies any `min-height` >400px (v7.24.0) | HC#69 |

Full per-release history was previously in CHANGELOG.md — deleted in PR3 since it had zero readers (no CI, no docs pipeline, no skill-runtime reference). Git log carries the narrative; the table above carries the load-bearing reversals.

---

## Workflow (6 steps, do not skip any)

### Step 0 — Mode router (run first, no exceptions)

The skill has two operating modes. Decide which one to run before doing anything else.

Ask yourself, in order:

1. **Did the merchant attach a file, paste JSX/HTML/CSS, paste a non-Figma URL, or reference the 4 Claude-Design filenames** (`product-page.jsx` + `colors_and_type.css`)?
   → **CONVERT MODE.** Proceed to Step 1.

2. **Did the merchant say "I have a design"** or paste anything that looks like structured design output (JSX, HTML markup, CSS rules, design tokens)?
   → **CONVERT MODE.** Proceed to Step 1.

3. **Otherwise** — empty invocation, vague prose ("I want a product page", "help me start", "make me something"), no attached design.
   → **INTAKE MODE.** Read [`intake/questions.md`](intake/questions.md) and proceed there. Do NOT run Steps 1–5.

When uncertain, choose **INTAKE** — the intake opener tells the merchant *"if you already have a design, paste it now"*, which routes them back to convert mode on their next turn.

**Why this matters.** Convert mode (Steps 1–5) is the canonical conversion pipeline merchants have used since v6 — its behavior is byte-frozen in v7.22 (CI-gated against the 14 fixture goldens). Intake mode is new in v7.22 and only activates when the merchant has nothing to convert yet. It asks ~6 questions across 2 batches and emits a Claude Design prompt the merchant pastes into design.claude.com. Once they return with the resulting design, Step 0 routes them back to convert mode automatically.

**Defense-in-depth.** Misrouting a clear convert input to intake costs the merchant one polite turn ("paste your design"). Misrouting empty intent to convert produces garbage HTML and erodes trust. The decision tree defaults to intake on ambiguity for that reason.

> **Figma URLs.** A bare `figma.com/design/...` URL with no other design content remains a deferred input (per Step 1.0 Figma policy). Step 0 routes it to **INTAKE MODE**, and the intake opener asks the merchant to re-export as PNG or HTML+CSS. The Figma-defer policy is unchanged — only the surface where the merchant hears about it has moved.

---

### Step 1 — Read the design

#### Step 1.0 — Input router (v7.0)

The skill accepts four input modes. Detect which one the merchant provided and follow the corresponding extraction path. **All paths converge on the same intermediate representation** that downstream steps consume: a list of sections, each with text content, image refs (with width/height/alt), inline-style → resolved-token map, layout structure, and `.map()` data arrays expanded.

| Input | Detection signal | Confidence | Path |
|---|---|---|---|
| **A. Claude Design project zip / unzipped / 4 files inline** | `product-page.jsx` + `sections-*.jsx` + `assets/colors_and_type.css` present | High | Step 1.A (canonical, no change from v6) |
| **B. Single screenshot / image** | merchant attached `.png`/`.jpg`/`.webp` AND no JSX/CSS | Medium-Low | Step 1.B (vision extraction; activates Tier C rubric) |
| **C. HTML + CSS dump** | merchant pasted/attached `.html` + `.css` (or HTML with `<style>` blocks) | Medium-High | Step 1.C (parse to intermediate) |
| **D. Live URL** | merchant pasted a `https://…` URL pointing at a published page | Medium-High (static pages) / Low (SPAs) | Step 1.D (`WebFetch` → 1.C) |

If the merchant attached the **single bundled HTML file from Claude Design** (~1.5 MB, React SPA), this is NOT case C — reject it: *"Please re-export from Claude Design as Share → Export as project (zip). The single bundled HTML file is a React SPA we can't parse from."* Case C is for static authored HTML, not bundled SPAs.

If two modes are simultaneously present (e.g., zip + screenshot), prefer A. The screenshot becomes a fidelity reference, not the source of truth.

> **Figma input:** not yet wired in v7.0 — deferred to a later release. If a merchant pastes a `figma.com/design/...` URL, ask them to export the frame as PNG (case B) or paste the rendered HTML+CSS (case C).
>
> **Figma MCP precedence (v7.18.3).** When the input is a `figma.com/design/...` URL AND the merchant has invoked this skill, this skill's deferral WINS over the Figma MCP server's auto-trigger. Do **NOT** call `mcp__claude_ai_Figma__*` tools (e.g. `use_figma`, `get_design_context`, `get_screenshot`). The Figma MCP server is a sibling capability whose tools are deferred until the design-extraction layer supports them natively. Ask the merchant to re-export as PNG or HTML+CSS instead.

---

#### Step 1.A — Claude Design zip / unzipped / 4 files inline (canonical)

The merchant attaches a Claude Design project zip (canonical), an unzipped directory, or pastes the 4 key files inline.

The 4 files you need:
- `product-page.jsx` — page composition (which sections appear in what order)
- `sections-1.jsx` — first half of section components
- `sections-2.jsx` — second half
- `assets/colors_and_type.css` — `:root { --token: value }` design tokens

For each section component (`Hero`, `Highlights`, `Specs`, `FAQ`, `Related`, `FinalCTA`, etc.):
- Look for the `<BlockTag blocks={["surecart/..."]} />` annotation — it names the target block(s)
- Walk the JSX subtree to extract: text, image refs, button labels, inline `style={{...}}`, layout structure (`display: grid`, `gap`, etc.), and `.map()` repetitions over data arrays
- Note which section uses which Claude Design tokens (`var(--brand)`, `var(--bg-dark)`, etc.)

**No-`<BlockTag>` fallback.** `<BlockTag>` is a developer-authored opt-in convention used by the iPhone fixture and similar curated examples — most real Claude Design exports do NOT include it. When absent, infer the target SureCart block from semantic content using `reference/product-page-blocks.md` as the vocabulary:

| Source signal | Target block |
|---|---|
| Page-dominant heading near a price | `surecart/product-title` |
| Currency-formatted price text | `surecart/product-price-chooser` |
| "Add to Cart" / "Add to bag" CTA | `surecart/product-buy-button` (`add_to_cart:true`) inside `surecart/product-buy-buttons` |
| "Buy Now" / "Buy" CTA | `surecart/product-buy-button` (`add_to_cart:false`) inside `surecart/product-buy-buttons` |
| Star/review rating row | `surecart/product-review-summary` (with required inner template — see `reference/style-conversion.md` Rule 3) |
| Quantity stepper (- 1 +) | `surecart/product-quantity` |
| Variant pills / chips ("Black • Blue • Natural Titanium") | `surecart/product-variant-pills` |
| "Related products" / "You may also like" grid | `surecart/product-list-related` |
| Body paragraphs, FAQs, generic layout | `core/*` blocks (heading, paragraph, group, columns, details) |

When semantic inference is ambiguous, prefer `core/*` and log under `dropped_features` in the drift report.

**JS-const tokenization layer.** Real exports declare JS constants for repeated CSS-var refs and consume them via template literals. Example pattern:

```jsx
// product-page.jsx
const ppBorder = "var(--border-1)";

// sections-1.jsx
<div style={{ borderBottom: `1px solid ${ppBorder}` }}>
```

When you see a template literal `${name}` inside an inline style, resolve through the JS const declarations at the top of `product-page.jsx` (and any imported helpers) BEFORE walking the CSS var chain. The full resolution is **JSX template literal → JS const → CSS var → CSS var → hex**. Three-hop chains are routine.

For `assets/colors_and_type.css`:
- Parse the `:root { … }` block
- Build a token map (e.g., `--brand → #01824C`, recursively resolving `var()` chains)
- Match against `reference/theme-partial.json` — slugs found there should be emitted as preset references; values not found are literals
- See `reference/style-conversion.md` Table A for the canonical CSS-var → slug + hex map

---

#### Step 1.B — Screenshot / image input (vision)

Activate Tier C of the self-validation rubric (`rubric/self-validate.md`). Vision-based extraction has lower confidence than parsed JSX/HTML; the rubric gates emission.

**Resolution gate.** The image must be at least 1200px on the long edge. Smaller images yield unreliable color/typography extraction. If below the gate, ask the merchant for a higher-resolution export before proceeding.

**Extraction order:**

1. **Section detection.** Identify visually distinct horizontal bands (header, hero, feature grid, …). Map each band to a section archetype using `reference/design-patterns.md`. If no archetype fits, treat the band as a generic `core/group` + nested children.
2. **Typography extraction.** For every text element, infer family (sans-serif vs serif vs mono — at family granularity, not exact face), size (px), weight (100/300/400/500/600/700/800/900 buckets), line-height (relative to size), letter-spacing (em), text-transform, text-align. Do NOT attempt to identify exact fonts unless the merchant tells you which font is used; default to the SureCart slugs (`surecart-display`/`-body`/`-mono`).
3. **Color extraction.** Sample dominant text/background/border hex values. **Snap to the nearest SureCart palette slug within ΔE 6.** If no slug matches, emit literal hex AND log under `color_snap_misses` in the drift report. **Do NOT trust pixel-precise hex values from screenshots** — JPEG/WebP compression, monitor color profile, and image scaling all distort color; ΔE 6 is the trust boundary.
4. **Spacing inference.** Estimate padding/margin/gap from visual spacing between elements. Round to the nearest 4px (the SureCart spacing unit). Mark all inferred spacing values as `confidence: "low"` in the per-section ledger; merchant should verify in the WP editor.
5. **Layout inference.** Decide between `core/columns` (visible vertical column boundaries), `core/group` flex (horizontal flow with gaps), `core/group` constrained (vertical stack). Card chrome (border + background) → use Exemplar 3.5 literal-bg variant.
6. **Asset extraction.** Each image in the screenshot becomes a `core/image` block with placeholder URL `https://cdn.example.com/inferred-{section}-{idx}.jpg`. Width/height inferred from on-screen pixel dimensions; alt text inferred from surrounding context (or empty + log `{type:"missing-alt"}` in `dropped_features`).

**Confidence dimension.** The drift report includes a `confidence` object: `typography`, `color`, `spacing`, `layout`, `assets` each scored `high`/`medium`/`low`. `color_snap_misses` count contributes directly to color confidence. Merchant uses these scores to know what to verify post-paste.

**Multi-page detection (v7.11 — Mode B pre-emit step).** Before emitting, perform a quick footer-presence check on the screenshot:

- If the screenshot has aspect-ratio ≥ 3:1 (tall page) AND **no footer-archetype band is detected** (forest/dark band with brand mark + link columns OR copyright line at the very bottom), the source likely spans multiple pages. Real product-page designs almost always include a footer — its absence is a strong signal of truncation.
- **Action:** scan for sibling files in the same input directory (`*.source.pdf`, `*.psd`, `*.ai`, `*.fig`) and read them for additional pages. If found, extract additional sections (footer, related products, secondary content) and emit them in source order.
- **No sibling source files:** ask the merchant explicitly: *"This screenshot appears to be page 1 of a multi-page design — I don't see a footer band. Are there additional pages I should know about? If yes, please attach them as additional screenshots or a single multi-page PDF."*
- **Common omitted-on-page-1 sections:** footer, related products / "Pairs well with", newsletter signup, secondary CTA. The Northwind fixture (14) demonstrates the pattern: page 1 ends mid-FAQ; page 2 carries related products + footer.

**Tier C blocking checks (rubric/self-validate.md):**
- C-17. Resolution gate: long edge ≥ 1200px.
- C-18. Confidence dimension: every dimension scored; `low` confidences listed in drift report's `merchant_verify[]` array.
- C-19. No literal hex without snap attempt: every literal hex has a `color_snap_misses` entry explaining why no slug matched.
- C-20. Section-count plausibility: detected sections ≥ 2 (a single-band screenshot rarely represents a full page; ask merchant for a full-page screenshot).
- C-22. Multi-page completeness (v7.11): tall screenshot (aspect ≥ 3:1) WITHOUT a footer-archetype band → scan sibling source files OR ask merchant about additional pages before emitting.

---

#### Step 1.C — HTML + CSS dump

The merchant pastes/attaches a static `.html` file (with `<style>` blocks or linked `.css`) representing the design. Common when the design was built in a static site generator, copied from a CodePen, or hand-coded.

**Extraction order:**

1. **Parse the HTML.** Walk the DOM tree top-to-bottom. Each top-level `<section>` / `<header>` / `<footer>` / `<main>`-child `<div>` becomes a section in the intermediate. Identify section role from class names (`.hero`, `.features`, `.pricing`, `.faq`, `.testimonials`, `.cta`, `.footer`) — these match the design-patterns archetypes.
2. **Resolve CSS.** Combine all `<style>` blocks + linked `.css` into one cascade. For each element, compute the **effective inline styles** (cascade resolution: inline > id > class > tag, !important wins). Resolve `var()` chains via `:root` and any nested custom-property definitions.
3. **Map to intermediate.** Each DOM element with effective styles becomes an entry in the intermediate with: text content, computed `style` map, image refs (from `<img>` `src`/`alt`/`width`/`height`), button hrefs.
4. **`.map()`-equivalent.** HTML doesn't have `.map()`, but repeated children (e.g., 4 `<article class="card">` children of a `.features` section) are the equivalent — emit them all as concrete siblings.
5. **Tokens.** If `:root { --token: value }` is present, treat exactly like Claude Design's `colors_and_type.css` (Table A resolution). Without `:root` tokens, assume literal hex/px throughout — emit literals + log `color_snap_misses` for every color that doesn't match a SureCart slug.

**Confidence:** medium-high. Static HTML+CSS is fully parseable; the only loss is whether class names map cleanly to archetypes (when they don't, fall back to `core/group` with semantic role inference from content).

**Drift report:** `input_type:"html_css"`. `dropped_features` should include any `<script>` tags (always dropped — Gutenberg markup is static), `<iframe>` content (drop unless it's a known embed provider → `core/embed`), and any pseudo-element styles (`::before`, `::after`) which Gutenberg can't express.

---

#### Step 1.D — Live URL

The merchant pastes a `https://…` URL pointing at a published page. Use `WebFetch` to retrieve the rendered HTML, then route to Step 1.C.

**Extraction order:**

1. **Fetch.** Call `WebFetch(url)` with a prompt asking for the full rendered HTML and inline/linked CSS. Note: `WebFetch` returns LLM-summarized content by default — for design extraction, request the raw HTML+CSS explicitly.
2. **Detect SPA.** If the HTML body is mostly empty (e.g., `<div id="root"></div>` and a bundled JS), the page is client-rendered and `WebFetch` won't see the actual content. Reject: *"This URL points to a client-rendered SPA. Please open the page in a browser, save the rendered HTML (right-click → Save As → Webpage Complete), and re-attach as case C (HTML+CSS)."*
3. **Route to Step 1.C** with the fetched HTML+CSS.

**Confidence:** medium-high for static / SSR pages; low for SPAs (rejected). Same drift-report fields as 1.C, plus `input_type:"live_url"` and `source_url`.

**Caveat:** never fetch internal/intranet URLs or URLs that require authentication — they'll either fail or expose credentials in the request log. If the URL requires auth, ask the merchant to export the rendered HTML manually instead.

---

### Step 1.5 — Run the Design Extraction Pass (v7.0)

Before loading exemplars or emitting markup, walk the **[reference/pixel-checklist.md](reference/pixel-checklist.md)** for every section the design contains. The checklist has 8 categories:

1. **Typography** (per-element: family/size/weight/line-height/letter-spacing/text-transform/text-align/decoration/style)
2. **Color** (text/background/border/gradients — slug match within ΔE 6, else literal hex)
3. **Spacing** (padding/margin/gap — literal px only, never preset slug)
4. **Layout** (flex/grid/columns/sticky — map to `core/columns` or `core/group` `layout.*`)
5. **Box** (border/radius/shadow/outline — emit AND set `border-style:"solid"` per v7.3 reversal of v5.6 Rule 4; shadows drop+log)
6. **Sizing** (width/max-width/min-height/aspect-ratio — explicit per block; `core/cover` for aspect-ratio + bg)
7. **Responsive** (breakpoints — drop+log with per-breakpoint patches; stack-on-mobile is automatic on `core/columns`)
8. **Assets** (images/video/fonts — extract filenames+dims+alt from zip; emit placeholder URLs; surface `assets[]` array in drift report)

For each section, every category must be either captured into block attrs OR added to `dropped_features` with a `merchant_action` CSS-snippet escape hatch where restoration via theme CSS is feasible. **Silent drops are forbidden.**

This pass is mandatory and replaces ad-hoc per-property reasoning. Output a small per-section mental ledger (you don't need to print it to the merchant; just walk it before emit).

---

### Step 2 — Read these reference files

The skill loads files in two tiers:

**EAGER — load on every conversion (1–7):**

1. **[reference/alias-map.md](reference/alias-map.md)** — the 6-row ❌/✅ table. Designer-time names like `surecart/variant-picker` DO NOT EXIST in the inventory. **Apply the rewrites BEFORE emitting.** This is the single most important content in the skill.

2. **[reference/product-page-blocks.md](reference/product-page-blocks.md)** — the ~25 curated SureCart blocks for product pages, with attribute cheatsheets per block. Every `surecart/*` block in your output must come from this list (or be looked up in `reference/full-inventory.json` / `reference/surecart-blocks.md`). **Do not invent block names.**

3. **[reference/core-blocks-cheatsheet.md](reference/core-blocks-cheatsheet.md)** — paired-block contract with copy-pasteable exemplars. Self-closing `<!-- wp:core/columns /-->` is the #1 production failure. The cheatsheet shows the right paired form for `core/columns`, `core/group`, `core/media-text`, `core/details`, `core/buttons`, etc.

4. **[reference/style-conversion.md](reference/style-conversion.md)** — JSX `style={{}}` → Gutenberg attrs table. Color/spacing/typography/border conversion + the `__experimentalSkipSerialization` carve-out for `surecart/product-buy-button` etc. + Rule 11 stable JSON key ordering. Also contains the v7.4 SET-equality rule (every wrapper inline `style="..."` rule has a 1:1 JSON `style.*` correlate; orphan rules trigger "Attempt block recovery").

5. **[reference/theme-partial.json](reference/theme-partial.json)** — the SureCart preset namespace (color palette slugs, spacing slugs, font-family slugs). When a CSS token matches a slug here, emit slug attrs (`textColor:"surecart-brand"`) instead of literal hex.

6. **[reference/token-aliases.json](reference/token-aliases.json)** — skill-only authority for resolving Claude-Design CSS-vars (`--brand`, `--bg-1`, `--font-display`, `--space-N`) into BOTH preset slug AND literal hex. The slug feeds standard slug-attr emission; the hex feeds **D7 dual-emit on leaf elements** (heading/paragraph/button/surecart text blocks) so the page renders correctly on classic WordPress themes that don't enqueue global styles. Paired wrappers (`core/group`, `core/columns`, etc.) stay slug-only — `$pairedWrapperBlocksSlugOnly` in the file lists them.

7. **[reference/design-patterns.md](reference/design-patterns.md) — Part 1 PASTE-SAFE PRIMITIVES** (v7.5, eager). The compositional library: P1 body-bg shim, P2 hero flex split, P3 vertical icon-text card, P4 bordered card chrome, P5 multi-card row, P6 CTA band, P7 detail-row, P8 inline review summary, P9 FAQ details list, P10 hero info column. Each primitive is a paste-validated block-tree fragment with a fixed wrapper-class set, fixed inline-style set, and 1:1 JSON `style.*` correlate (set-equality verified). **The skill composes designs from these primitives — it does NOT copy production patterns wholesale.** Production patterns (Part 2 + `examples/patterns/`) are HOW examples (paste-safe conventions), not WHAT templates.

**LAZY — load on demand (8–13):**

8. **[reference/full-inventory.json](reference/full-inventory.json)** — all 153 SureCart blocks with attribute schemas, supports trees, `ancestor`/`parent` constraints. Search this for any `surecart/*` block name when uncertain. Loaded on demand because the file is 8000+ lines.

9. **[reference/pixel-checklist.md](reference/pixel-checklist.md)** — the 8-category Design Extraction Pass from Step 1.5. Re-consult while emitting if any property feels ambiguous (gradients, shadows, sticky, aspect-ratio, asset extraction).

10. **[reference/design-patterns.md](reference/design-patterns.md) — Part 2 SECTION ARCHETYPES** — legacy archetype reference (hero, feature grid, pricing table, testimonial, FAQ, product card, CTA band, footer). Use only when a primitive in Part 1 needs additional context on archetype-level composition (e.g., what surrounds a hero). The archetypes are descriptive, not prescriptive — primitives drive composition.

11. **[reference/surecart-blocks.md](reference/surecart-blocks.md)** — human-readable index of every SureCart block (~153 next-gen + ~84 legacy), grouped by use case. Open when looking up a block outside the curated `product-page-blocks.md` set, including legacy form/checkout/donation blocks where next-gen has no equivalent.

12. **[reference/wp-core-blocks.md](reference/wp-core-blocks.md)** — attribute index for the WP core blocks the skill emits (layout primitives, typography, media, interactive, structural). Open when looking up a core block's attribute schema or wrapper-class shape.

13. **[reference/custom-html-fallback.md](reference/custom-html-fallback.md)** (v7.1) — the 3-tier `core/html` fallback ladder (L1 static, L2 piggyback on existing SureCart Interactivity stores, L3 drop + recommend `/surecart-new-block`). Open when steps 1–12 above came up empty for a design element and you need to decide between static raw HTML, Interactivity-API-piggybacked HTML, or escalating to a custom block.

---

### Step 3 — Decompose the design, then compose primitives

> **v7.5 — paradigm shift.** Earlier versions told the skill to "find the closest matching production pattern and pattern-match against it". That works for designs that happen to mirror a production pattern (e.g., Aether Field Notebook → product-physical) but fails the moment the merchant's design composes differently (e.g., 2-col hero with media on RIGHT + 6 highlight cards in 3×2 + testimonial carousel + embedded video + sticky add-to-cart + footer with newsletter). **The skill must compose paste-safe primitives that match the design — not copy templates.**

#### 3a. Decompose

Walk the design top-to-bottom. For each visually distinct horizontal band, identify:
1. **Its role** — body-bg shim, hero, feature grid, specs row, reviews, FAQ, CTA band, footer, etc.
2. **Its layout** — vertical stack, 2-col flex split, N-up card row, full-width band with constrained content, etc.
3. **Its chrome** — background color, border, padding, radius, shadow, sticky behavior.
4. **Its content blocks** — which SureCart blocks (`surecart/product-title`, `product-buy-buttons`, `product-review-*`, etc.) and which core blocks (`core/heading`, `core/paragraph`, `core/image`, `core/details`).

Record the per-section ledger mentally: `{role, layout, chrome, content_blocks[]}`. Every section is in the ledger; nothing is silently dropped (Hard Constraint #9).

#### 3b. Map sections to primitives

For each ledger entry, pick the matching primitive from **`reference/design-patterns.md` Part 1 (P1–P10)**:

| Section role | Primitive |
|---|---|
| `body { background: ... }` page-bg host | **P1 body-bg shim** — first child of `surecart/product-page` |
| Hero with media on one side + info on other | **P2 hero flex split** — outer flex `core/group` + 2 child groups with `selfStretch:fixed,flexSize:Npx` |
| Highlight card with icon + heading + body | **P3 vertical icon-text card** — `core/group` vertical flex + child SVG `core/html` + heading + paragraph |
| Bordered card chrome (border + background + radius) | **P4 bordered card chrome** — literal-bg + literal-border + 1:1 inline-mirror |
| Row of 3+ cards | **P5 multi-card row** — outer `core/group` flex `flexWrap:"wrap"` + N child cards with `selfStretch:fixed,flexSize:"NN%"` |
| Full-width band with brand-color bg + constrained inner content | **P6 CTA band** — literal-bg `core/group` `align:"full"` + inner constrained content |
| Bordered split row (label + value + label + value) | **P7 detail-row** — flex `core/group` with border-bottom split |
| Stars + numeric rating + review count, single-line | **P8 inline review summary** — `core/group` flex `flexWrap:"nowrap"` + `surecart/product-review-average-rating-stars` + `surecart/product-review-total-rating` (className OMITTED per HC#19 v7.15 — `plus-sign` is `isDefault:true`) |
| FAQ accordion | **P9 FAQ details list** — N `core/details` paired blocks with mandatory `summary` attr |
| Hero info column (title, price, variants, quantity, buy buttons) | **P10 hero info column** — vertical flow inside hero's info side |

If a section doesn't map to any primitive, it usually means:
- **The section is novel** — compose it from finer-grained primitives (e.g., a "testimonial carousel" decomposes into a P6 CTA-band-like wrapper + multiple P3 vertical cards) and log a `dropped_features` entry for the carousel-specific behavior (auto-rotate, swipe) with a `merchant_action` recommending `/surecart-new-block`.
- **The section is a SureCart block** — use the block directly (e.g., `surecart/product-reviews` for reviews list, `surecart/product-list-related` for related products). No primitive needed for block-rendered sections.

#### 3c. Compose

Emit the primitives in source order, with one compositional rule: **set-equality on every wrapper**. For every `core/group` or `core/cover` wrapper that carries an inline `style="..."`, every `prop:value` rule in the inline string MUST have a matching JSON `style.*` path. Drop orphan inline rules (rule with no JSON correlate) and fill missing inline rules (JSON path with no inline correlate) before emit. Set mismatches are the dominant cause of "Attempt block recovery" prompts (verified at `gutenberg/packages/blocks/src/api/validation/index.js:622-697`).

#### 3d. Production patterns are HOW references, not WHAT templates

When a primitive's wrapper-class set or JSON shape feels ambiguous, look up the corresponding production-pattern reference cited in P1–P10:

- **[examples/patterns/product-physical.example.md](examples/patterns/product-physical.example.md)** — warm-palette physical product page (used for P1, P2, P3, P4, P5, P10 references)
- **[examples/patterns/product-standard.example.md](examples/patterns/product-standard.example.md)** — neutral product page (used for P8, P10 hero info-column composition)
- **[examples/patterns/product-course-dark.example.md](examples/patterns/product-course-dark.example.md)** — dark-bg course page (used for P5 wider-grid variant, P6 CTA band on dark)

These confirm a primitive's set-equality without locking the merchant's design into the production pattern's overall composition. Read them when stuck on a primitive's exact wrapper-class set or JSON shape — never as a "use this whole pattern" template.

#### 3e. Typography presets remain authoritative

For text blocks (`core/heading`, `core/paragraph`, `surecart/product-title`, `core/buttons` button labels), keep using **[examples/typography-presets.example.md](examples/typography-presets.example.md)** for the per-class slug + dual-emit recipes. Typography is orthogonal to layout primitives — the same `display-1` heading lives inside P2, P6, or freestanding.

---

### Step 4 — Emit ONE fenced ```html block (or write to file when large)

Output exactly **one** ` ```html ` fenced code block containing the full Gutenberg markup. The block:

- Starts with `<!-- wp:surecart/product-page {"metadata":{"name":"<merchant title>","patternName":"<slug>"}} -->`
- Ends with `<!-- /wp:surecart/product-page -->`
- Has **NO inner `<div>` wrapper** — `surecart/product-page` is `apiVersion: 3` server-rendered, with no `save()`. Children sit between the comment markers as siblings. Hand-writing `<div class="wp-block-surecart-product-page">` becomes freeform HTML and breaks every child block
- Inside, faithfully reconstructs the design's layout using `core/columns` / `core/group` / `core/media-text` / `core/details` etc. with **proper paired-block markup** (see `reference/core-blocks-cheatsheet.md`)
- Every `surecart/product-buy-button` is wrapped in `surecart/product-buy-buttons`
- All inline JSX styles converted via `reference/style-conversion.md`
- Token references resolve via `reference/theme-partial.json` first, literal otherwise

#### Write-to-file threshold + paste-path (v7.18.3 — PR2)

**Why:** chat-render and terminal copy-paste soft-wrap long lines, occasionally inserting literal newlines (U+000A) inside JSON string values. `JSON.parse` rejects literal newlines in strings per ECMA-404 §9 → `parseJSON` returns null → block opens with `attrs=null` → save() regenerates default-only markup → validateBlock mismatch → "Attempt block recovery" cascade. The 80-char per-string-value cap (HC#16) eliminates the most common trigger, but full-page markup can still spread across enough chat-render columns that a long `summary` or URL line-wraps. **The robust fix is to bypass chat-render entirely.**

**Threshold (HC#48-gate):** use the **Write tool** to save the markup to `~/Desktop/{pattern-slug}.html` (where `{pattern-slug}` is the slugified `metadata.patternName` per HC#1's slug-derivation rule) **if total markup ≥ 5,120 bytes (5 KB)**. Otherwise emit one fenced ```html block in chat. The file branch, once entered for this response, is **non-reversible** — DO NOT fall back to chat-emit even if the file is small post-minification. If the Write tool errors, state "file write failed" and ABORT — do not paste markup inline as a fallback.

When the file branch fires, the chat response carries EXACTLY:

1. A short summary of what was written (1-2 sentences).
2. The drift report JSON (Step 5 below). **NO field value may contain `<!-- wp:` literal markup.**
3. A copy-paste instruction block that points the merchant at the file (template below).

> **To use this in WordPress** (LLM detects merchant's OS from conversation context and leads with the matching command):
>
> **macOS** — open Terminal (Cmd+Space → "Terminal"), run:
> ```
> pbcopy < ~/Desktop/{pattern-slug}.html
> ```
>
> **Linux X11/Wayland** — open a terminal, run:
> ```
> xclip -selection clipboard < ~/Desktop/{pattern-slug}.html      # X11
> wl-copy < ~/Desktop/{pattern-slug}.html                          # Wayland (when xclip absent)
> ```
>
> **Windows PowerShell:**
> ```
> Get-Content "$HOME\Desktop\{pattern-slug}.html" -Raw | Set-Clipboard
> ```
>
> **Windows / WSL terminal:** open the file in VS Code, Sublime, or Notepad++ → verify the status bar shows **LF** (not CRLF) → `Cmd/Ctrl+A` → `Cmd/Ctrl+C`. **DO NOT use `clip.exe < file`** — it injects CRLF that corrupts the markup on save round-trip.
>
> **Any OS without clipboard tooling** (remote SSH without clipboard forwarding, minimal Linux box): open the file in VS Code, Sublime, or BBEdit (verify LF line endings). **NOT TextEdit** unless you first disable smart-quote substitution via *Edit → Substitutions → uncheck Smart Quotes*, OR `defaults write -g NSAutomaticQuoteSubstitutionEnabled -bool false` from Terminal.
>
> Then continue: WP page editor → ⋮ menu → **Code editor** (or `Cmd+Shift+Alt+M`) → paste → switch back to **Visual editor** → Save.

**Below 5,120 bytes:** emit one fenced ```html block in chat. Short markup is unlikely to soft-wrap at problematic boundaries.

**Post-write LF verification (v7.20 PR4):** the Write tool writes the bytes the LLM emits. On macOS that is LF by default. After writing, verify with `file -b ~/Desktop/{pattern-slug}.html` — output should be `ASCII text` or `HTML document text, ASCII text` or similar. If the output contains `CRLF line terminators`, the file is corrupted (some Windows-y editor or piping path injected `\r`). Re-emit. The Write tool's content parameter must contain only `\n` line breaks — never `\r\n`, never `\r` alone.

**Empirical anchors:** Aether Field Notebook (31 KB) and all six v7.18.3 paste-test goldens (atlas-greens / aurora-lamp / halcyon-field-jacket / loom-ash-throw / lumen-saas / hearth-hollow-shop, 21–164 KB, 72–376 blocks) → zero recovery prompts via the file-write + `pbcopy` path (verified live in WP 6.7+ block editor, 2026-05-27).

---

### Step 5 — Self-validate (mandatory)

**Before responding to the merchant**, walk through the Tier A/B/C rubric (`rubric/self-validate.md`). State the result at the top of your response. The state line shape varies by input mode:

> Self-validation: Tier A 14/14, Tier B 7/7, Tier C skipped (input: zip).
>
> Self-validation: Tier A 14/14, Tier B 7/7, Tier C 5/5 (input: screenshot, confidence: typography:medium, color:low, spacing:low, layout:high, assets:medium).
>
> Self-validation: Tier A 14/14, Tier B 7/7, Tier C skipped (input: html_css).
>
> Self-validation: Tier A 14/14, Tier B 7/7, Tier C skipped (input: live_url, source: https://example.com/page).

If anything fails, fix and re-validate. Do not emit broken markup.

#### 5a. Re-read pass (v7.0 — mandatory before emit)

After the rubric passes but **before** writing the final response, re-read your own draft markup top-to-bottom and confirm:

1. **Block-comment integrity.** Every `<!-- wp:NAMESPACE/BLOCK ... -->` opener has a matching `<!-- /wp:NAMESPACE/BLOCK -->` closer at the same nesting depth. Self-closing form `<!-- wp:BLOCK ... /-->` is allowed only for the blocks listed under "Self-closing core blocks" in `reference/core-blocks-cheatsheet.md`.
2. **Block name validity.** Every `surecart/*` block name appears in `reference/full-inventory.json` (or the curated list in `reference/product-page-blocks.md`); every `core/*` block name is a real Gutenberg core block. Run the alias-map rewrites one final time — designer-time names should already be gone but it's free to verify.
3. **Attribute schema.** Every JSON attribute key on every block is one the block actually supports. Cross-check `full-inventory.json` `attributes.{name}` and `supports.*` for SureCart blocks; for core blocks rely on the cheatsheet exemplars + `style-conversion.md` Table B. **No invented attrs.** If you can't find an attr in either source, drop it and log under `dropped_features`.
4. **JSON well-formedness.** Every block-comment JSON parses: balanced `{}` and `[]`, double-quoted keys, no trailing commas, no unescaped quotes inside string values. A single broken JSON token cascades recovery across every following block.
5. **JSON key ordering.** Per Rule 11 in `reference/style-conversion.md`, attributes appear in stable order: `metadata` → `align` → `width`/`height`/`aspectRatio` → `backgroundColor`/`textColor`/`borderColor`/`gradient`/`fontFamily`/`fontSize` (slug attrs first) → `style.{color,spacing,typography,border,position,dimensions,shadow}` → `layout` → block-specific tail attrs (e.g., `level`, `summary`, `url`, `placeholder`, `add_to_cart`).
6. **Wrapper-class match.** For every slug attr emitted, the wrapper element's `class=""` includes the matching `has-{slug}-{kind}` class (rubric A-9). For every `style.color/background/spacing` literal, the wrapper has the inline-style mirror per Table B Rule 0 hierarchy.

If any check fails, fix the markup and re-run from 5a. Do not respond to the merchant with broken markup.

After the markup, emit a drift report:

```json
{
  "input_type": "zip",
  "sections_detected": ["StoreHeader","Hero","Highlights","Specs","FAQ","Related","FinalCTA","StoreFooter"],
  "blocks_emitted": 47,
  "annotations_resolved": {"exact": 6, "alias_rewritten": 4, "core": 30, "fallback": 7},
  "tokens_resolved": {"preset": 23, "literal": 14, "type_scale_classes": 8},
  "color_snap_misses": [
    {"source": "#1a1a2e", "reason": "no surecart-* slug within ΔE 6 — emitted literal hex"}
  ],
  "classic_theme_readiness": {
    "leaf_blocks_with_d7_dual_emit": 38,
    "leaf_blocks_total": 41,
    "compliance_percent": 92,
    "note": "wrapper backgrounds remain slug-only per Rule 0; classic themes without SureCart theme partial loaded will see those wrapper bgs render transparent — D7 doesn't apply to paired wrappers"
  },
  "b18_compliance": {
    "blocks_with_full_visual_contract": 47,
    "blocks_total": 47,
    "container_blocks_typography_clean": true,
    "note": "every leaf has explicit typography + color + fontFamily; container blocks (price-chooser, quantity, buy-buttons, product-review-summary) own LAYOUT only"
  },
  "stencil_components_used": ["sc-button", "sc-input", "sc-cart"],
  "stencil_preload_note": "Verify these are listed in app/config.php under 'preload' key; missing entries cause layout shift on first render",
  "assets": [
    {"type": "image", "filename": "hero-iphone.jpg", "width": 1600, "height": 1200, "alt": "iPhone 17 Pro in titanium finish", "placeholder_url": "https://cdn.example.com/hero-iphone.jpg"},
    {"type": "image", "filename": "feature-camera.png", "width": 800, "height": 600, "alt": "Camera close-up", "placeholder_url": "https://cdn.example.com/feature-camera.png"}
  ],
  "dropped_features": [
    {"type": "animation", "section": "Hero", "detail": "transition: transform 0.3s", "merchant_action": "Add `transition: transform 0.3s` to the relevant class via theme stylesheet"},
    {"type": "backdrop-filter", "section": "StoreHeader", "detail": "saturate(180%) blur(8px)", "merchant_action": "Add `backdrop-filter: saturate(180%) blur(8px)` to the header wrapper class"},
    {"type": "shadow", "section": "Highlights cards", "detail": "0 4px 16px rgba(0,0,0,0.1)", "merchant_action": "Add `box-shadow: 0 4px 16px rgba(0,0,0,0.1)` to the card class"},
    {"type": "gradient", "mode": "linear", "section": "FinalCTA", "detail": "linear-gradient(135deg, #01824C 0%, #042F2E 100%)", "fallback_emitted": "surecart-brand (first stop)", "merchant_action": "Use core/cover with customGradient OR add `background: linear-gradient(...)` to the section class"},
    {"type": "responsive", "breakpoint": "sm", "section": "Hero", "detail": "mobile-only padding override", "merchant_action": "In WP block editor switch device preview to Mobile and adjust padding"},
    {"type": "raw_html_static", "section": "Promo ribbon", "detail": "decorative chrome with no Gutenberg block equivalent", "merchant_action": "merchant edits via the Code editor; not visible in Visual mode"},
    {"type": "raw_html_interactive", "level": "L2", "section": "Hero cart pill", "namespace": "surecart/cart", "dependency_block": "surecart/cart-icon", "detail": "custom banner that toggles the cart drawer using surecart/cart::actions.toggle", "merchant_action": "merchant must keep the surecart/cart-icon block on the page for the toggle to work; pasted content survives only with unfiltered_html capability (admin/editor role)"},
    {"type": "raw_html_interactive", "level": "L3", "section": "Animated stats counter", "detail": "count-up animation requires custom state machine; emitted static fallback with final values", "merchant_action": "to restore the count-up animation, invoke /surecart-new-block to scaffold a next-gen interactive block"}
  ]
}
```

**New fields explained:**

- `color_snap_misses[]` — colors that didn't match a SureCart slug within ΔE 6. Lists the literal hex emitted as fallback. High count → merchant should consider adding custom palette entries.
- `classic_theme_readiness` — count and % of leaf blocks with D7 dual-emit. Wrapper bgs are excluded (slug-only per Rule 0). Below 90% on a classic theme means visible color drift.
- `b18_compliance` — % of blocks emitting all 8 visual property categories explicitly. `container_blocks_typography_clean: true` confirms no chooser/quantity/buy-buttons/group has typography attrs (per B-18 + container-vs-leaf rule).
- `stencil_components_used[]` — `sc-*` Stencil tags emitted into the markup (typically through `surecart/*` blocks that internally render Stencil components). Each must have a preload entry in `app/config.php` `'preload'` key on the merchant's site or layout shifts on first render.
- `assets[]` (v7.0) — every image/video extracted from the input. Each entry has `filename`, `width`, `height`, `alt`, and a `placeholder_url` (e.g., `https://cdn.example.com/hero.jpg`) that the merchant searches for and replaces after uploading the file to WP Media Library. Empty array is valid; missing field is not.
- `dropped_features[].merchant_action` (v7.0 mandatory) — every dropped feature must include a `merchant_action` string with a CSS-snippet escape hatch when restoration via theme CSS is feasible. Silent drops are forbidden by the v7.0 Design Extraction Pass.
- `raw_html_static` / `raw_html_interactive` (v7.1) — the 3-tier `core/html` fallback ladder. **L1 (static)** entries log only the section + merchant_action. **L2 (Interactivity API piggyback)** MUST also include `namespace` (one of the 7 documented `surecart/*` namespaces) AND `dependency_block` (the sibling SureCart block on this same emit that triggers the namespace's module load). **L3 (custom)** logs the design's section + merchant_action recommending `/surecart-new-block` (or `/surecart-new-integration` for third-party APIs); the skill emits a best-effort static visual fallback so the page isn't empty pending the developer follow-up. See `reference/custom-html-fallback.md` for the full contract + namespace allowlist.

Finally, give the merchant copy-paste instructions:

> **To use this in WordPress:**
>
> 1. Open the page where you want the design (or create a new page).
> 2. In the block editor, click the ⋮ menu (top right) → **Code editor** (or press `Cmd+Shift+Alt+M`).
> 3. Paste the markup above into the editor.
> 4. Switch back to **Visual editor** (same menu).
> 5. Save / Publish.
>
> If any block shows an "Attempt Block Recovery" notice on first paste, the most likely cause is a long literal string value (>30 chars) inside the block-comment JSON — typically a `fontFamily` stack — that line-wrapped during paste, inserting a literal newline mid-value and breaking `JSON.parse` strictness (ECMA-404 §9). The fix is to register a custom font slug in `theme.json` and re-paste with the slug. **There is no SureCart save filter that normalizes paired-block markup; recovery is purely WP's standard `convert.toRecoveredBlock` re-serialization, which captures the outer `<p>`/`<h{level}>` as `content` and wraps it again — producing the `<p><p>...</p></p>` artifact.** See [rubric/merchant-recovery.md](rubric/merchant-recovery.md).

When the output contains any `core/html` block at L2 (Interactivity API piggyback — drift report shows `raw_html_interactive` with `level:"L2"`), append this single-line warning to the merchant's instructions:

> **Note:** This page uses custom HTML with WordPress Interactivity directives. You must save the page as an Administrator or Editor — Author / Contributor / lower roles will have the `data-wp-*` attributes stripped on save (`unfiltered_html` capability gate).

---

## Hard constraints (committing any of these is a guaranteed bug)

1. **Outer wrapper:** entire output is wrapped in `<!-- wp:surecart/product-page -->…<!-- /wp:surecart/product-page -->`. Without it, every child `surecart/product-*` block renders empty.

    **`metadata.name` + `metadata.patternName` are ALWAYS emitted (v7.18.3 — clarification).** The outer block carries `{"metadata":{"name":"<merchant title>","patternName":"<slug>"}}`. Even though `metadata.patternName` is COSMETIC inside the editor (it appears in the sidebar; it does NOT register the markup as a pattern), it is **load-bearing for the file-write step**: Step 4 derives the `~/Desktop/{pattern-slug}.html` filename from `metadata.patternName`. Dropping the attr makes the slug undefined → write target becomes `~/Desktop/.html`. Always emit both fields.

    **Slug derivation rule (v7.18.3):** the `{pattern-slug}` used for the file path is `metadata.patternName` after slugification: lowercase; replace any non-`[a-z0-9-]` character with `-`; collapse multiple consecutive `-` into one; truncate to 50 chars. Fallback when the slugified result is empty (entire `patternName` was non-ASCII / CJK / punctuation) OR `-`-only: use `surecart-product-page-{YYYY-MM-DD-HHMMSS}` as the filename. On collisions where two patterns slugify to the same name, append the SHA1 hex prefix (8 chars) of the original `patternName` for uniqueness.

2. **Apply the alias map:** rewrite the 6 designer-time names BEFORE emit. See `reference/alias-map.md`.

3. **Never self-close paired core blocks:** `core/columns`, `core/column`, `core/group`, `core/cover`, `core/media-text`, `core/buttons`, `core/list`, `core/list-item`, `core/quote`, `core/details` — each MUST have its `<div class="wp-block-{name}">…</div>` wrapper in `innerHTML`.

4. **Buy buttons coalesce:** Add-to-Cart and Buy-Now go in ONE shared `surecart/product-buy-buttons` wrapper. Never two wrappers.

5. **`metadata` only on the outer block.** Strip from inner blocks.

6. **`__experimentalSkipSerialization` carve-out:** for `surecart/product-buy-button` (skips spacing + color + **border**) and similar blocks, write the attrs but DO NOT inject `class=""` or `style=""` on the wrapper for the skipped support tree. If styling is needed, put it on a parent `core/group`.

7. **Token-first:** prefer `textColor:"surecart-brand"` (slug) over `style.color.text:"#01824C"` (literal) when the slug exists in `theme-partial.json`. Cleaner output, theme-overridable.

8. **`.map()` over a literal array → expand to N siblings.** No template-language artifacts in output (no `{{name}}`, `${var}`, `<%= … %>`).

9. **Every named section in JSX MUST appear in the output OR be logged in `dropped_features`.** If `product-page.jsx` renders Header → Breadcrumbs → Hero → Highlights → DescriptionBlocks → Specs → FAQ → Related → FinalCTA → Footer → StickyBuyBar, the markup must contain all 11 in source order, OR each omission gets a `dropped_features` entry with reason. Silent dropping is the dominant cause of "design doesn't match" reports.

10. **`fontFamily` is mandatory for every text-bearing block** when the source CSS class declares `font-family`. Display headings (`.sc-h1`, `.sc-h2`, `.sc-h3`, `.sc-display-*`) → `fontFamily:"surecart-display"`. Body copy (`.sc-lead`, `.sc-body`, `.sc-eyebrow`, `.sc-small`) → `fontFamily:"surecart-body"`. Mono (`.sc-eyebrow-mono`, `.sc-code`) → `fontFamily:"surecart-mono"`. Always pair with class `has-{slug}-font-family` on the wrapper. Without this, headings render in the active theme's default font, not Geist — the #1 visual-fidelity gap.

11. **`<!-- wp:details -->` MUST carry `{"summary":"<question text>"}`** matching the inner `<summary>` HTML. Gutenberg's deserializer parses summary from HTML and re-serializes with the attr filled in — mismatched empty attr → recovery prompt on every FAQ item.

12. **Comment markers use the unprefixed core form.** `<!-- wp:group -->`, NOT `<!-- wp:core/group -->`. WordPress's `serializeBlock()` writes core blocks without the namespace prefix; mismatched prefixes cause round-trip recovery prompts.

13. **Slug validation.** Before emitting any preset slug (`textColor`, `backgroundColor`, `fontFamily`, `fontSize`, `borderColor`), MUST verify the slug exists in `reference/theme-partial.json`. Never invent slugs by pattern (e.g., `surecart-bg-1` doesn't exist; use `surecart-white` for `#FFFFFF`).

14. **Hybrid spacing/color policy (v5.9).** Use slug attrs for **color and font-family** (theme-overrideable, short class strings, paste-safe). Use **literal pixel values** for **spacing and border** — `padding:"24px"`, `margin:"48px"`, `border.radius:"24px"`. **NEVER emit `"var:preset|spacing|*"` in `style.spacing.*` attrs** — the resulting `var(--wp--preset--spacing--N)` strings inside inline `style=""` are ~250 chars long and get line-wrapped during paste, corrupting the markup with embedded whitespace inside the `var()` parens. Literal px values are byte-perfect every time. See `reference/style-conversion.md` v5.9 hybrid policy table.

15. **Explicit-per-block visual contract (v6.0).** Every block declares EVERY visual property the design exhibits — **including 0 values**. No inheritance assumptions. No "the parent set it / the theme will handle it." The 8 categories: typography (size/weight/lh/ls/transform/decoration/style), font-family slug, spacing (padding/margin/blockGap, including `"0px"`), dimensions (width/height/aspectRatio/contentSize), text color (D7 dual-emit on leaves), background (D7 dual-emit on leaves; slug-only on paired wrappers per Rule 0), border (radius/width/color/**style:"solid"** per the v7.3 reversal of v5.6 Rule 4), layout (type/orientation/flexWrap/justifyContent/verticalAlignment). **Container blocks own LAYOUT only** — `surecart/product-price-chooser`, `surecart/product-quantity`, `surecart/product-buy-buttons`, `surecart/product-review-summary`, `core/group`, `core/columns` — typography/color/font-family belongs on each text-leaf child, NEVER cascaded from the parent. Inheritance is fragile across themes; explicit per-block emission is the contract. See `reference/style-conversion.md` "Explicit-per-block visual contract" section + `rubric/self-validate.md` B-18.

16. **JSON string-value cap (v7.3 + v7.18.3 PR2 mechanism correction).** Never emit a JSON string value longer than **80 characters**. The dominant paste-recovery trigger is chat-render or terminal soft-wrap inserting literal newlines (U+000A) inside long JSON string values. Per ECMA-404 §9, U+000A inside a JSON string is invalid.

    **Actual cascade (v7.18.3 corrected):** `JSON.parse` fails → WP's `parseJSON` wrapper at `@wordpress/block-serialization-default-parser/src/index.js:371-377` returns `null` (NOT throws — it catches the exception) → block opens with `attrs=null` → block falls back to `block.json` `attributes.{name}.default` values → `save()` regenerates default-only markup → `validateBlock` sees the merchant-styled stored content vs default-styled generated content → mismatch → "Attempt Block Recovery". The cascade is wide because the block's full attr set is lost, not just the over-long field.

    **Applies to:** `fontFamily` literal stacks, `summary` (on `core/details`), `metadata.name`, `metadata.patternName`, gradient strings, URLs.

    **Workaround for long font stacks:** keep literal stacks short (one face + one generic fallback, ≤30 chars — e.g., `"Cormorant Garamond, serif"`, `"Inter, sans-serif"`, `"JetBrains Mono, monospace"`). Use the registered `surecart-display` / `surecart-body` / `surecart-mono` slugs for theme-overridable emission. Do NOT register custom font slugs (`cormorant-display`, `inter`, `jetbrains-mono` etc.) in `reference/theme-partial.json` — that file is auto-mirrored from production `app/data/surecart-theme-partial.json` and custom additions will be wiped on next `yarn build:theme-partial-mirror`.

    **Multibyte / non-ASCII note:** the 80-character cap is measured in characters (`.length`), not bytes. A Korean product name at 79 chars is fine for JSON.parse but may exceed effective MySQL row-size limits on installs with `utf8mb4` collation when stored in `wp_posts.post_content` alongside many other long-string attrs. Not a paste-recovery trigger; only a row-size concern. For non-ASCII patterns with many long-string attrs (gradient stacks + long titles + long descriptions), favor preset slugs over literals to keep the per-block JSON compact.

17. **Body-bg shim (v7.3).** When the design CSS declares `body { background-color: #hex }` or has a body-level CSS var (e.g., `--bg-page`), emit it on the FIRST inner `core/group` of `surecart/product-page` — NOT on the SureCart product-page block (apiVersion 3, no save()), AND NOT under `dropped_features`. Pattern reference: `examples/patterns/product-physical.example.md:25-26`.

18. **Buy-button text attr mandatory (v7.3).** Every `surecart/product-buy-button` MUST carry a non-empty `text` attr. Self-closed `<!-- wp:surecart/product-buy-button /-->` (no attrs) is a Tier-A failure. When pairing Add-to-Cart + Buy-Now: primary uses `{"add_to_cart":true,"text":"Add To Cart"}`, secondary uses `{"text":"Buy Now","className":"is-style-outline"}` — NO inline border/radius/color on the secondary. Reference: `product-standard.example.md:102-108`.

19. **Hero review summary fork (v7.3, CORRECTED v7.15).** When the design renders inline single-line review chrome (stars + numeric rating + count, NOT an expanded summary card with breakdown bars), emit a `core/group` flex with `flexWrap:"nowrap"` + `blockGap:"10px"` containing `surecart/product-review-average-rating-stars` + `surecart/product-review-total-rating`. **Default to inline; OMIT `className` on `product-review-total-rating` — `plus-sign` is `isDefault:true` per `block.json#styles`** (this was previously misdocumented as `className:"is-style-plus-sign"` being needed, but `plus-sign` is the registered default so emitting the className triggers a round-trip rewrite). When the design DOES want the dot-prefix variant ("· 1,284 reviews"), emit `className:"is-style-default"` explicitly. The bare self-closed `<!-- wp:surecart/product-review-summary /-->` is reserved for designs that show the expanded summary card. Reference: `product-standard.example.md:35-41`.

20. **Card grids use `core/group` flex (v7.3).** Card grids (3+ sibling cards) ALWAYS use `core/group` flex with each child card a `core/group` carrying `style.layout:{selfStretch:"fixed",flexSize:"NN%"}`. NEVER `core/columns` for card grids — theme-conflict on borders, no per-card width control via inline style, harder to tighten gaps. 4-up: `flexSize:"23%"`; 3-up: `"31%"`; 2-up: `"48%"`. Reference: `product-physical.example.md:26-31`.

21. **`has-border-color` class always-emit policy (v7.6 — REVERSES v7.3).** Emit `has-border-color` **WHENEVER** top-level `style.border.color` is set, regardless of whether the value is a slug or literal-hex. Gutenberg's `save()` function always emits the class when the JSON has top-level `style.border.color` — the earlier v7.3 "OMIT for literal-hex" was empirically wrong (Aurora Lamp paste-test 2026-05-11). When `style.border.color` is a slug, emit `has-{slug}-border-color` IN ADDITION to `has-border-color`. The earlier concern about `--wp--custom--color--border` being theme-undefined is moot: the inline `style="border-color:#hex"` mirror has higher CSS specificity than any class-based theme rule, so the literal hex always wins. Set-equality check: any wrapper with top-level `style.border.color` in JSON MUST emit `has-border-color` in the HTML `class=""`; mismatch triggers "Expected attribute `class` of value `has-border-color`, saw …" recovery on every card.

    **Per-side carve-out (v7.18.3, lifted from shop-page SHC#9).** When the design specifies PER-SIDE border colors via `style.border.top.color` / `style.border.right.color` / `style.border.bottom.color` / `style.border.left.color` instead of the top-level `style.border.color`, save() emits ONLY the inline `border-<side>-color:hex;` style — **NO `has-border-color` class**. Do NOT emit the class in that case.

    | Border JSON | Class emitted | Inline style |
    |---|---|---|
    | `"border":{"color":"#E6DFD2","width":"1px"}` (top-level) | `has-border-color` | `border-color:#E6DFD2;border-width:1px;` |
    | `"border":{"top":{"color":"#E6DFD2","width":"1px"}}` (per-side) | (none) | `border-top-color:#E6DFD2;border-top-width:1px;` |
    | `"border":{"radius":"10px"}` only | (none) | `border-radius:10px;` |
    | `"border":{"color":"#E6DFD2"},"borderColor":"surecart-gray-200"` (slug) | `has-border-color has-surecart-gray-200-border-color` | (no inline border-color — slug class drives it) |

    Same family failure as `core/cover` / `core/group` validation cascades — single-block mismatch propagates up the ancestor chain.

22. **[MERGED v7.18.3 PR2 — canonical home = HC#45]** No HTML comments inside block content areas. The original HC#22 rule was the apiVersion-3-wrapper-specific failure; HC#45 is the broader (greppable) rule covering all block validation comment-mismatch paths. Both failure signatures preserved in HC#45's body. **See HC#45 for the full rule + greppable check + sibling SHC#10 silent-drop variant.**

23. **`core/image` is strict-schema (v7.6 + v7.10 + v7.18.3 PR2 merge — ABSORBS prior HC#29).** The image block's `save()` emits a tightly-controlled set of inline styles on `<img>`. The complete schema:

    | Source attr | Emitted inline style | Notes |
    |---|---|---|
    | `style.border.radius:"Npx"` | `border-radius:Npx` | Class set adds `has-custom-border` |
    | top-level `width:"Npx"` block attr | `width:Npx` | Top-level block attr, NOT `style.dimensions.*` |
    | top-level `height:"Npx"` block attr | `height:Npx` | Top-level block attr |

    **Combined inline-key order** (when multiple set): `border-radius;width;height` — border-radius first, then size. Class set: `wp-block-image size-{slug} is-resized` (always when width OR height is set), plus `has-custom-border` when `style.border.*` is present.

    **Nothing else** is allowed inline on `<figure>` or `<img>`. Adding freehand `style="flex-basis:48%;aspect-ratio:4/3;object-fit:cover;width:100%"` triggers set-equality drift (`Expected attributes [Array(3)], instead saw (2) [Array(3), Array(3)]`). Hand-writing `<img ... width="32" height="32"/>` (as HTML attrs, not inline-style) is also drift: save() emits via inline-style, not HTML attrs.

    For flex-width control inside a flex-row parent (P5 multi-card row, P3 gallery grid), wrap each `core/image` in a `core/group` with `style.layout:{selfStretch:"fixed",flexSize:"NN%"}` — the group carries the width, the image stays schema-clean. To restore lost `aspect-ratio` or `object-fit`, drop+log under `dropped_features` with a CSS-snippet `merchant_action`.

    **Canonical exemplars (v7.10/v7.18.3):**

    Flex-row card image (v7.6 form, no size attrs):
    ```html
    <!-- wp:group {"style":{"layout":{"selfStretch":"fixed","flexSize":"48%"}},"layout":{"type":"default"}} -->
    <div class="wp-block-group">
    <!-- wp:image {"sizeSlug":"large","style":{"border":{"radius":"16px"}}} -->
    <figure class="wp-block-image size-large has-custom-border"><img src="..." alt="..." style="border-radius:16px"/></figure>
    <!-- /wp:image -->
    </div>
    <!-- /wp:group -->
    ```

    Sized thumbnail / icon (v7.10 form, width+height inline):
    ```html
    <!-- wp:image {"sizeSlug":"thumbnail","width":"32px","height":"32px"} -->
    <figure class="wp-block-image size-thumbnail is-resized"><img src="https://cdn.example.com/icon.svg" alt="" style="width:32px;height:32px"/></figure>
    <!-- /wp:image -->
    ```

    Circular avatar (v7.10 form, all three: border + width + height):
    ```html
    <!-- wp:image {"sizeSlug":"thumbnail","width":"36px","height":"36px","style":{"border":{"radius":"36px"}}} -->
    <figure class="wp-block-image size-thumbnail is-resized has-custom-border"><img src="https://cdn.example.com/avatar.jpg" alt="" style="border-radius:36px;width:36px;height:36px"/></figure>
    <!-- /wp:image -->
    ```

24. **`core/list` requires `wp-block-list` class; no inline-styled inline children inside `<li>` (v7.6).** Two regressions discovered together:

    **24a — `<ul>` wrapper class.** `core/list`'s `save()` emits `<ul class="wp-block-list …">`. Omitting `wp-block-list` triggers `"Expected attribute class of value `wp-block-list is-style-none has-…`, saw `is-style-none has-…`"` recovery. Always include `wp-block-list` as the first class on the `<ul>` (or `<ol>` for ordered).

    **24b — list-item content.** `core/list-item` content is rich-text, but inline-styled `<strong>` or `<span>` siblings inside the `<li>` trigger the deprecated `wp.blocks.children.matcher` path (deprecated since WP 6.1, slated for 6.3 removal). The deprecated matcher mis-serializes the content and set-equality fails. **For 2-column key:value tabular data (specs tables, comparison tables), DO NOT use a single `core/list` with inline-styled children.** Instead emit a parent `core/group` (`layout.orientation:"vertical"`) wrapping N detail-row `core/group` (`layout.type:"flex",flexWrap:"nowrap",justifyContent:"space-between"`), each containing 2 `core/paragraph` siblings (label + value). This is P7 (detail-row primitive). Schema-clean, paste-safe, and matches design intent exactly. Plain bulleted lists (no inline styling, plain `<li>` text) are fine with `core/list` + `wp-block-list` class.

25. **Structural-CSS class-only routing on `core/group` + `core/cover` (v7.18.3 PR2 — ABSORBS prior HC#30 + HC#33).** `core/group` and `core/cover` route some structural properties (aspect-ratio, position) through CSS classes / CSS-vars rather than inline-style mirrors. Hand-writing the property in the inline `style=""` triggers set-equality drift and recovery cascades.

    **Decision table — 4 distinct outcomes:**

    | Block | JSON path | Inline `style=""` mirror? | Class emitted | Use case |
    |---|---|---|---|---|
    | `core/group` | `style.dimensions.aspectRatio` | **FORBIDDEN — never emit** | (none — drop+log) | Square placeholder; use `padding-top` proxy or `core/cover` instead |
    | `core/cover` | top-level `aspectRatio:"4/3"` | ✅ YES — emits `aspect-ratio:4/3` | (none class-side) | Hero with `url` (background-image cover) |
    | `core/cover` | `style.dimensions.aspectRatio:"1"` | ❌ NO — applied via CSS class/var | (class-routed via global-styles) | `useFeaturedImage:true` per-card variant (canonical `surecart/product-list-related` Start-Basic template) |
    | `core/group` | `style.position.{type,top}` | ❌ NO — applied via class | `is-position-sticky` | Sticky header / sidebar |

    **Rules:**
    - `core/group` aspect-ratio: never emit `style.dimensions.aspectRatio`. Drop+log under `dropped_features.type:"aspect_ratio_on_group"` with CSS-snippet `merchant_action`. For square / fixed-ratio boxes, use `padding-top`/`padding-bottom` proxy (e.g., 60px vertical inside `flexSize:"32%"` ≈ square at 1240px container) OR substitute with `core/cover` / `core/image`.
    - `core/cover` aspect-ratio: pick the JSON path that matches the use case. Top-level `aspectRatio` inline-mirrors; `style.dimensions.aspectRatio` does NOT. Inline `style="aspect-ratio:X"` is allowed ONLY when JSON uses the top-level attr.
    - `core/group` sticky-position: keep `style.position.{type,top}` in JSON; emit `is-position-sticky` class on wrapper; do NOT emit `position:sticky;top:Npx;z-index:N` in inline `style=""`. The behavior routes via class.
    - When the design requires a specific z-index on a sticky `core/group`, drop under `dropped_features.type:"z_index"` with a `merchant_action` recommending theme CSS targeting `.is-position-sticky`.

    **Failure signatures:**
    - Group aspect-ratio: `Expected style "<short>", saw "<short>;aspect-ratio:1"` → `Block validation failed for core/group` (Morning Glow Serum 2026-05-11).
    - Cover style.dimensions.aspectRatio: `Generated: style="border-radius:4px;margin-bottom:0", retrieved: style="border-radius:4px;aspect-ratio:1"` (Northwind round 2, 2026-05-13).
    - Group position: `Generated: style="border-bottom-color:#E8E1D8;...;padding-left:32px", retrieved: style="...padding-left:32px;position:sticky;top:0px;z-index:50"` (Morning Glow v2, 2026-05-26).

    **Canonical exemplar — sticky header (v7.13 form):**

    ```html
    <!-- wp:group {"align":"full","style":{"position":{"type":"sticky","top":"0px"},"color":{"background":"#FBF7F2"},"spacing":{"padding":{"top":"0","right":"32px","bottom":"0","left":"32px"}},"border":{"bottom":{"color":"#E8E1D8","width":"1px"}}},"layout":{"type":"constrained","contentSize":"1240px"}} -->
    <div class="wp-block-group alignfull is-position-sticky has-background" style="border-bottom-color:#E8E1D8;border-bottom-width:1px;background-color:#FBF7F2;padding-top:0;padding-right:32px;padding-bottom:0;padding-left:32px">
    …header content…
    </div>
    <!-- /wp:group -->
    ```

    Note: NO `position:sticky`, NO `top:0px`, NO `z-index` in inline `style=""`. JSON retains the position attrs; save() applies them via class.

    **Canonical exemplar — featured-image card cover (v7.11 form, `style.dimensions.aspectRatio` path):**

    ```html
    <!-- wp:cover {"useFeaturedImage":true,"dimRatio":0,"isUserOverlayColor":true,"focalPoint":{"x":0.5,"y":0.5},"contentPosition":"top center","isDark":false,"style":{"dimensions":{"aspectRatio":"3/4"},"spacing":{"margin":{"bottom":"15px"}},"border":{"radius":"10px"}},"layout":{"type":"default"}} -->
    <div class="wp-block-cover is-light has-custom-content-position is-position-top-center" style="border-radius:10px;margin-bottom:15px"><span aria-hidden="true" class="wp-block-cover__background has-background-dim-0 has-background-dim"></span><div class="wp-block-cover__inner-container">
      …content…
    </div></div>
    <!-- /wp:cover -->
    ```

    Inline-style key order: `border-radius;margin-{side}` (border before spacing). The `style.dimensions.aspectRatio:"3/4"` lives in JSON only — NOT in the inline mirror.

26. **Zero-value spacing properties REQUIRE JSON↔inline parity (v7.7).** The v7.4 set-equality rule applies to ALL `style.spacing.*` values — including zeros. A JSON path like `style.spacing.margin:{top:"0",bottom:"0"}` MUST emit `style="margin-top:0;margin-bottom:0"` on the wrapper. Omitting the inline mirror (treating `0` as no-op) triggers `Expected style="margin-top:0;margin-bottom:0", saw style=""` recovery.

    **Rule:** when adding zero-value spacing for explicit-per-block visual contract (HC15) reasons, ALWAYS emit BOTH the JSON path AND the inline mirror. If you don't need the explicit zero override (e.g., the default theme spacing is already 0 or acceptable), DROP the property from JSON entirely rather than emit JSON-only.

    The dominant failure mode in practice: leaving a stale `"margin":{"top":"0","bottom":"0"}` in JSON after refactoring the inline `style=""` to remove the mirror. Re-run rubric B-27 (set-equality) after any wrapper-style refactor.

    Applies to **all** spacing properties: `margin.{top|right|bottom|left}`, `padding.{top|right|bottom|left}`, `blockGap`. Verified: morning-glow-serum (v7.7).

27. **`core/cover` gradient-only emission class set canonical form (v7.7 — corrects v7.0 Exemplar 8).** When `core/cover` is emitted with `customGradient` (or `gradient` slug) and NO `url`, save() applies a default `dimRatio:100` and the inner `<span>` overlay class set is:

    ```
    wp-block-cover__background has-background-dim-100 has-background-dim has-background-gradient
    ```

    NOT `wp-block-cover__gradient-background has-background-gradient` as previously documented. The v7.0 cheatsheet Exemplar 8 Variant B was wrong on this point. The corrected canonical exemplar:

    ```html
    <!-- wp:cover {"customGradient":"linear-gradient(135deg,#A 0%,#B 100%)","minHeight":380,"minHeightUnit":"px"} -->
    <div class="wp-block-cover" style="min-height:380px"><span aria-hidden="true" class="wp-block-cover__background has-background-dim-100 has-background-dim has-background-gradient" style="background:linear-gradient(135deg,#A 0%,#B 100%)"></span><div class="wp-block-cover__inner-container">
      …content…
    </div></div>
    <!-- /wp:cover -->
    ```

    **Recommended fallback for non-image gradient backgrounds:** prefer `core/group` with `style.color.background:"#hex"` (one of the gradient end-stops, typically the second/darker stop) over `core/cover` gradient. The `core/group` solid-bg emit is simpler, has fewer class-set drift risks, and the visual difference vs. a subtle gradient is minor. Drop+log the gradient under `dropped_features.type:"gradient", mode:"linear"` with `merchant_action:"add 'background: linear-gradient(…)' to the wrapper class via theme stylesheet"`.

    Verified: morning-glow-serum (v7.7).

28. **`surecart/product-buy-buttons` margin inline-mirror parity (v7.10).** Despite being `apiVersion:3` server-rendered, the buy-buttons wrapper IS subject to set-equality validation against its hand-written wrapper `<div>`. When the block JSON has `style.spacing.margin:{top:X,bottom:Y}`, the wrapper `<div>` MUST carry matching inline `style="margin-top:X;margin-bottom:Y"`. Omission triggers `Block validation failed for surecart/product-buy-buttons. Generated: <div ... style="margin-top:0;margin-bottom:20px"></div>, retrieved: <div ...></div>`.

    **Inline-mirror SCOPE for this wrapper:**

    | JSON path | Emit inline? | Notes |
    |---|---|---|
    | `style.spacing.margin.{top|right|bottom|left}` | YES | `margin-top:X;margin-right:X;...` |
    | `style.spacing.padding.{top|right|bottom|left}` | YES | mirror standard pattern |
    | `style.spacing.blockGap` | NO | flows to gap via CSS var, never inline |
    | `style.color.background` | NO (skipSerialization) | parent group carries chrome |
    | `style.color.text` | NO (skipSerialization) | per buy-button only |
    | `style.border.*` | NO (skipSerialization) | per buy-button only |

    Canonical exemplar (v7.10 — corrects v7.3 / v7.9 exemplars that only had `blockGap`):

    ```html
    <!-- wp:surecart/product-buy-buttons {"style":{"spacing":{"blockGap":"10px","margin":{"top":"0","bottom":"20px"}}}} -->
    <div class="wp-block-surecart-product-buy-buttons wp-block-buttons sc-block-buttons is-layout-flex" style="margin-top:0;margin-bottom:20px">
        <!-- wp:surecart/product-buy-button {"add_to_cart":true,"text":"Add to Cart"} /-->
        <!-- wp:surecart/product-buy-button {"text":"Buy Now","className":"is-style-outline"} /-->
    </div>
    <!-- /wp:surecart/product-buy-buttons -->
    ```

    The wrapper class set (`wp-block-surecart-product-buy-buttons wp-block-buttons sc-block-buttons is-layout-flex`) remains constant — it's server-determined. Only the inline `style=""` changes with `style.spacing.margin/padding` JSON. Verified: northwind-pour-over-kettle (v7.10).

29. **[MERGED v7.18.3 PR2 — canonical home = HC#23]** `core/image` strict-schema (incl. v7.10 width/height-as-inline-style). HC#23 absorbs the v7.10 width/height + combined-order table. **See HC#23 for the unified schema + 3 canonical exemplars.**

30. **[MERGED v7.18.3 PR2 — canonical home = HC#25]** `core/cover` aspect-ratio JSON path fork (top-level vs `style.dimensions.*`). The 4-row decision table + canonical featured-image exemplar live in HC#25. **See HC#25.**

31. **No hand-written `font-style:normal` in inline mirror without `fontStyle:"normal"` in JSON (v7.10).** `font-style:normal` is the CSS default. Style-engine does NOT emit `font-style:normal` to inline unless the JSON path `style.typography.fontStyle:"normal"` is explicitly set. Hand-adding `font-style:normal` to the inline string (defensive habit copied from production exemplars where it IS in JSON) triggers set-drift on every text-bearing block: `Generated has "font-size:22px;font-weight:400;line-height:1.2", retrieved has "font-size:22px;font-style:normal;font-weight:400;line-height:1.2"`.

    **Rule:** JSON↔inline parity on `font-style`. Either path:
    - **Drop from inline**: don't write `font-style:normal` in the inline `style=""`. JSON has no `fontStyle`. Default-CSS handles the `normal` case (which is the same as omitting). Recommended for compactness.
    - **Add to JSON**: emit `style.typography.fontStyle:"normal"` AND `font-style:normal` in inline. Use when matching a production exemplar that explicitly includes it (e.g., reviewer-name styles with `fontStyle:"normal"` for safety against italic-cascading parents).

    Applies symmetrically to `italic`: `style.typography.fontStyle:"italic"` MUST emit `font-style:italic` in inline. Verified: northwind-pour-over-kettle (v7.10).

32. **`core/icon` is the canonical block for built-in icon glyphs (v7.12 — WP 7.0+).** WordPress 7.0 shipped a native `core/icon` block resolving 88 built-in SVG icon slugs via `WP_Icons_Registry`. This is the FIRST CHOICE for any decorative icon glyph in the design — it replaces the L1 `core/html` inline-SVG fallback for the 88 built-in slugs.

    **Precedence ladder for icon glyphs:**

    1. **`core/icon`** — for any glyph matching a built-in slug (arrow-*, chevron-*, cart, check, plus, star-{filled,empty,half}, info, search, menu, shield, share, etc. — full 88-slug catalog in `reference/wp-core-blocks.md § core/icon`).
    2. **`core/image`** — for custom brand glyphs (logo marks, illustrative SVGs / PNGs) that don't match any built-in slug AND exist as a file URL.
    3. **`core/html` L1 inline SVG** — last resort only, when neither of the above applies. Requires `unfiltered_html` capability to survive save; not theme-overridable for color.

    **Paste form (always self-closing — `apiVersion:3` server-rendered, no `save()`):**

    ```html
    <!-- wp:icon {"icon":"core/check"} /-->                                          — minimal
    <!-- wp:icon {"icon":"core/cart","textColor":"surecart-brand","ariaLabel":"Open cart"} /-->   — slug color + a11y label
    <!-- wp:icon {"icon":"core/star-filled","style":{"dimensions":{"width":"20px"},"color":{"text":"#F59E0B"}}} /-->   — literal hex + size
    ```

    **Rules:**
    - Comment marker is unprefixed `wp:icon`, NOT `wp:core/icon` (HC#12 — same as every core block).
    - Icon attribute MUST include the `core/` namespace prefix (`"core/check"`, not `"check"`). Omission → registry lookup fails → block renders empty.
    - ALWAYS self-close. Paired form is wrong.
    - Color / border / padding / width all `__experimentalSkipSerialization` → apply to the inner `<svg>`, NOT the wrapper. Do NOT emit `has-{slug}-color` / `has-text-color` / `has-background` / `has-border-color` classes on the wrapper (which is server-emitted via `get_block_wrapper_attributes()`).
    - **`margin` DOES serialize on the wrapper** — emit `style.spacing.margin` JSON ↔ inline mirror parity (per HC#28's pattern for `surecart/product-buy-buttons`).
    - `align` is `"left"` / `"center"` / `"right"` only — NOT `"wide"` / `"full"`. For wide layouts, wrap the icon in a `core/group` with `align:"full"`.

    **When the design has icon-text cards (P3 vertical icon-text card primitive):** use `core/icon` as the icon child, NOT `core/html` inline SVG.

    **Most-emitted slugs on shop pages (v7.18.3, lifted from sibling SHC#11):**

    | Shop-page need | Slug |
    |---|---|
    | Search input prefix | `core/search` |
    | Sort dropdown caret | `core/chevron-down` |
    | Cart icon in nav | `core/cart` |
    | Rating star on cards | `core/star-filled` / `core/star-empty` / `core/star-half` |
    | "Load more" / "Continue" arrow | `core/arrow-right` |
    | Filter-clear close | `core/plus` (rotated via CSS for X) |
    | Filter-checkbox tick | `core/check` |
    | Info tooltip trigger | `core/info` |
    | Menu / hamburger | `core/menu` |

    Reference: `reference/wp-core-blocks.md § core/icon` (full attribute schema + 88-slug catalog); `reference/core-blocks-cheatsheet.md` Exemplar 10 (paste-form recipes); `reference/custom-html-fallback.md` (updated L1 precedence note); `reference/alias-map.md` (precedence ladder + most-emitted slugs).

33. **[MERGED v7.18.3 PR2 — canonical home = HC#25]** `core/group` `style.position` does NOT inline-mirror. The 4-row decision table + canonical sticky-header exemplar + z-index drop-and-log live in HC#25. **See HC#25.**

34. **`core/button` `has-custom-font-size` class emitted for literal-px `fontSize` + canonical class order with `wp-element-button` TRAILING (v7.13).** When `core/button` JSON has `style.typography.fontSize:"16px"` (a literal px value), save() emits `has-custom-font-size` on the inner `<a class="wp-block-button__link...">` element. The class is the same one already documented for `core/heading` per Rule 5 in `reference/wp-core-blocks.md` — it applies symmetrically to `core/button`.

    **Canonical class set on `<a class="wp-block-button__link">` (v7.13):**

    ```
    wp-block-button__link has-text-color has-background has-{slug}-font-family has-custom-font-size wp-element-button
    ```

    **`wp-element-button` is the FINAL class — trailing indicator.** This mirrors B-22's principle that `has-text-color` / `has-background` are trailing per-property indicators. `wp-element-button` trails the slug + custom-font-size classes.

    **Failure signature:** `Expected class "wp-block-button__link has-text-color has-background has-{slug}-font-family has-custom-font-size wp-element-button", saw "wp-block-button__link has-text-color has-background wp-element-button has-{slug}-font-family"` (missing `has-custom-font-size`, `wp-element-button` mid-order).

    **Rules:**
    - When `core/button` JSON has `style.typography.fontSize` as a literal px value → emit `has-custom-font-size` class.
    - When `core/button` JSON has `fontSize:"<slug>"` (slug attr, not literal) → emit `has-{slug}-font-size` class instead; NO `has-custom-font-size`.
    - Class order (set-comparison, not strict sequence per B-22, but emit in this canonical order for consistency): `wp-block-button__link` → `has-text-color` → `has-background` → `has-{slug}-font-family` (when slug fontFamily set) → `has-custom-font-size` (when literal px fontSize set) → `wp-element-button` (always last).

    **Canonical exemplar** (v7.13):

    ```html
    <!-- wp:button {"style":{"color":{"background":"#2A2620","text":"#FBF7F2"},"spacing":{"padding":{"top":"16px","right":"32px","bottom":"16px","left":"32px"}},"border":{"radius":"9999px"},"typography":{"fontSize":"16px","fontWeight":"500"}},"fontFamily":"surecart-body"} -->
    <div class="wp-block-button"><a class="wp-block-button__link has-text-color has-background has-surecart-body-font-family has-custom-font-size wp-element-button" href="#subscribe" style="border-radius:9999px;color:#FBF7F2;background-color:#2A2620;padding-top:16px;padding-right:32px;padding-bottom:16px;padding-left:32px;font-size:16px;font-weight:500">Start subscription — $42 / month</a></div>
    <!-- /wp:button -->
    ```

    **The same class applies to `core/heading` / `core/paragraph`** per Rule 5 (already documented in `reference/wp-core-blocks.md`) — HC#34 extends the doctrine to `core/button` where it was previously implicit.

    Verified: morning-glow-serum-v2 (v7.13).

35. **Font-family literal fallback alongside slug (v7.14).** Merchant theme.json often doesn't register the design's intended font face (Fraunces / Cormorant / Inter / Geist Mono). Slug-only emission like `fontFamily:"surecart-display"` falls back to whatever `surecart-display` is mapped to in the active theme — frequently Manrope, the system sans, or the theme's default H1 family. To make the design's typography visible without requiring pre-emit theme.json setup, emit **BOTH** the slug AND a literal short-stack:

    ```html
    <!-- wp:heading {"level":1,"fontFamily":"surecart-display","style":{"typography":{"fontSize":"52px","fontWeight":"500","fontFamily":"Fraunces, serif"},"color":{"text":"#2B2520"}}} -->
    <h1 class="wp-block-heading has-text-color has-surecart-display-font-family" style="color:#2B2520;font-family:Fraunces, serif;font-size:52px;font-weight:500">Hand-thrown ceramic ramen bowl</h1>
    <!-- /wp:heading -->
    ```

    **Key rules:**
    - The slug class (`has-surecart-display-font-family`) provides theme-overridable semantic intent.
    - The literal `style.typography.fontFamily:"Fraunces, serif"` (≤30 chars per HC#16 — primary face + ONE generic fallback) provides the visual fallback when the slug isn't registered.
    - The literal value MUST appear in both JSON `style.typography.fontFamily` AND in the inline `style="...;font-family:...;..."` mirror (per B-27 set-equality).
    - **Per HC#16's 80-char cap on JSON string values, keep the font-stack short.** `"Fraunces, serif"` = 16 chars ✓. `"Fraunces, Cormorant Garamond, Times New Roman, serif"` = 49 chars (also OK but verbose). NEVER emit the full design's font-stack list — pick the primary face + one generic fallback.

    **Apply to ALL text-bearing blocks** where the design specifies a non-default font: `core/heading`, `core/paragraph`, `core/details` summary (via internal styling — see HC#11), `core/button` link, `surecart/product-title`, `surecart/product-buy-button`, all `surecart/price-*` leaves.

    **Detection:** if the design's `styles.css` declares `--font-display: 'Fraunces', serif;` (or similar), the literal-fallback short-stack should match the primary face name. Emit `Fraunces, serif`, NOT `'Fraunces', serif` — drop the inner quotes for JSON cleanliness (no need to escape them).

    Verified: kobachi-ramen-bowl (v7.14).

36. **Featured-image cover placeholder fallback (v7.14).** `core/cover {useFeaturedImage:true}` renders as the product's featured image when one is set, but falls back to the cover's background color (`style.color.background` literal) when no featured image exists. This leaves the design's intended hero illustration INVISIBLE pre-image-upload.

    When the design has a CUSTOM SVG illustration in the hero gallery (bowl illustration, product mockup, illustrative shape that won't be replaced by a product photo until merchant uploads one), the skill MUST emit the SVG (as `core/html` L1) INSIDE the cover's `<div class="wp-block-cover__inner-container">` so something visible shows pre-image-upload:

    ```html
    <!-- wp:cover {"useFeaturedImage":true,"dimRatio":0,"isUserOverlayColor":true,"focalPoint":{"x":0.5,"y":0.5},"isDark":false,"style":{"dimensions":{"aspectRatio":"1"},"border":{"radius":"16px"},"color":{"background":"#C8694A"}},"layout":{"type":"default"}} -->
    <div class="wp-block-cover is-light has-background" style="border-radius:16px;background-color:#C8694A"><span aria-hidden="true" class="wp-block-cover__background has-background-dim-0 has-background-dim"></span><div class="wp-block-cover__inner-container">
    <!-- wp:html -->
    <div style="width:60%;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 600 600" aria-hidden="true">…design's bowl illustration paths…</svg></div>
    <!-- /wp:html -->
    </div></div>
    <!-- /wp:cover -->
    ```

    **Rules:**
    - Emit ONE `core/html` block inside the cover's inner-container containing the design's illustration SVG (verbatim from `app.jsx`/sections).
    - The cover's `useFeaturedImage:true` still applies — when merchant uploads a real product image, it replaces the SVG visually (the SVG sits behind the image).
    - The SVG `<div>` wrapper centers the illustration via flex (matching the design's intent).
    - Drop+log under `dropped_features.type:"hero_illustration_placeholder"` with `merchant_action:"upload a real product photo to surecart/product → featured image to replace the placeholder bowl illustration"`.

    **When NOT to do this:** if the cover is purely decorative (e.g., a colored band background in a CTA section with content overlaid), the bg color is fine on its own. The SVG-inside rule applies only when the design's gallery/hero/card image area has a custom illustration that won't show without one.

    Same pattern applies to related-products `surecart/product-template` inner `core/cover` blocks — when the design has card illustrations.

    Verified: kobachi-ramen-bowl (v7.14).

37. **[MERGED v7.18.3 PR2 — canonical home = HC#38]** Server-rendered chrome wrap-and-target. The v7.14 wrap-and-target pattern is now Step 2 (fallback) of the unified rule in HC#38. **See HC#38 for the 2-step decision (block-style variation FIRST, wrap-and-target SECOND), affected blocks, catalog, and canonical exemplars.**

38. **Server-rendered chrome — registered block-style variations FIRST, wrap-and-target FALLBACK (v7.18.3 PR2 — ABSORBS prior HC#37).** When a `surecart/*` server-rendered block needs custom chrome (border, background, padding, radius) that the design specifies, follow this 2-step decision:

    **Step 1 (FIRST CHOICE): Check `reference/surecart-blocks.md § Registered block-style variations`** (the static catalog — do NOT simulate `getBlockStyles()` at runtime; the LLM cannot call it. Consult the catalog.) If the block has a registered variation matching the design's intended chrome, apply it via `className:"is-style-{variant}"` in the JSON.

    **Step 2 (FALLBACK only when no variation fits): Wrap-and-target.** Wrap the affected block in a styled `core/group` that carries the chrome (background, border, padding) AND a stable `className`. The merchant then adds a small CSS rule targeting the inner Stencil component via the wrapper's className.

    **Why server-rendered chrome bypasses skill style attrs:** several SureCart blocks are `apiVersion:3` server-rendered with their own internal Stencil components. Style attrs (typography/border/color) on the block JSON do NOT reliably reach the rendered HTML — the merchant theme's CSS often overrides the inline styles emitted by the server template. The block-style variations (Step 1) solve this at the source via registered CSS; wrap-and-target (Step 2) routes the chrome to a separate wrapper outside the affected block.

    **Affected blocks (incomplete list — verify per emission):**
    - `surecart/product-quantity` — renders a Stencil stepper. Bare emission produces a SQUARE white box; use Step 1 with `className:"is-style-orbit"` (pill) / `"is-style-pebble"` (rounded) / `"is-style-borderless"` for the design's intended chrome.
    - `surecart/product-review-average-rating-value` — numeric "4.9" via Stencil. Use Step 1 with `className:"is-style-parentheses"` / `"is-style-slash"` for display format.
    - `surecart/product-buy-button` — typography respected (per B-16), but `style.color.{text,background}` + `style.border.*` are `__experimentalSkipSerialization` (HC#6). Use Step 1 with `className:"is-style-outline"` for secondary buttons (HC#18).
    - `surecart/product-quick-view-button` (per-card) — bare emission renders always-visible. Use Step 1 with `className:"is-style-show-on-hover"`.
    - `surecart/cart-button` family + `surecart/sticky-purchase` — server template owns the chrome.
    - **Shop-page per-card blocks** (lifted from sibling SHC#13) — `surecart/product-list-price` (typography respected; bg/border via skipSerialization), `surecart/product-scratch-price` (same), `surecart/product-review-average-rating-stars` (icon size via Stencil), `surecart/product-sale-badge` (chrome via Stencil). FIRST check the catalog; if no variation fits, wrap-and-target.

    **Known registered block-style variations (v7.18.3 catalog — full reference at `reference/surecart-blocks.md § Registered block-style variations`):**

    | Block | Variations | Notes |
    |---|---|---|
    | `surecart/product-quantity` | `default`, `borderless`, `orbit`, `pebble` | `orbit` = round pill chrome; `pebble` = rounded but less circular; `borderless` = no chrome at all |
    | `surecart/product-buy-button` | `fill`, `outline` | `outline` per HC#18 secondary buttons |
    | `surecart/product-review-average-rating-value` | `none`, `parentheses`, `slash` | Display format for the numeric rating value |
    | `surecart/product-review-total-rating` | `default`, `plus-sign` | `plus-sign` is `isDefault:true` — omit className for default (HC#19 v7.15 correction) |
    | `surecart/product-quick-view-button` | `default`, `show-on-hover` | `show-on-hover` matches most product-card designs that reveal quick-view on hover |

    **Canonical exemplars:**

    **Step 1 — block-style variation applied (preferred):**
    ```html
    <!-- wp:surecart/product-quantity {"label":"Quantity","hidden_label":true,"className":"is-style-orbit","style":{"spacing":{"padding":{"top":"0","bottom":"0"}}}} /-->
    ```
    ```html
    <!-- wp:surecart/product-quick-view-button {"className":"is-style-show-on-hover"} /-->
    ```
    ```html
    <!-- wp:surecart/product-buy-button {"text":"Buy Now","className":"is-style-outline"} /-->
    ```

    **Step 2 — wrap-and-target (fallback ONLY when no variation matches):**
    ```html
    <!-- wp:group {"className":"qty-pill-chrome","style":{"color":{"background":"#FCFAF6"},"border":{"radius":"9999px","width":"1px","color":"#E5DDD0","style":"solid"},"spacing":{"padding":{"top":"4px","right":"4px","bottom":"4px","left":"4px"}}},"layout":{"type":"flex","flexWrap":"nowrap","verticalAlignment":"center"}} -->
    <div class="wp-block-group qty-pill-chrome has-border-color has-background" style="border-color:#E5DDD0;border-style:solid;border-width:1px;border-radius:9999px;background-color:#FCFAF6;padding-top:4px;padding-right:4px;padding-bottom:4px;padding-left:4px">
    <!-- wp:surecart/product-quantity /-->
    </div>
    <!-- /wp:group -->
    ```

    The outer `core/group` carries the visible pill chrome; the inner block renders inside.

    **`hidden_label` attr — `surecart/product-quantity` only:** boolean attr (default `false`) that hides the visible "Quantity" label above the stepper WITHOUT removing the a11y `label` string. Emit `hidden_label:true` for designs without a visible label.

    **Drift report addition (Step 2 only):** every emit that wraps a server-rendered block logs a `server_rendered_style_attrs_bypassed[]` entry naming the wrapped block + the chrome attrs the outer wrapper carries + the className the merchant targets in custom CSS.

    Verified: kobachi-ramen-bowl + atlas-greens (v7.14 + v7.15).

39. **`surecart/sticky-purchase` content can overflow without explicit positioning constraints (v7.16, surfaced R2 Atlas Greens).** The block ships `position:fixed` on the frontend wrapper, but the **inner content** must fit horizontally. When the skill emits a `surecart/product-media` (without explicit max-width), a `surecart/product-title`, a price block, AND a `surecart/product-buy-buttons` inside the sticky wrapper, the inner flex column can wrap to multiple rows, blowing up the bar's height from the expected ~70–90px to 400+px, and pushing the bar off-screen via `top: <large>px`.

    **Symptom:** the sticky bar exists in DOM (`position:fixed` confirmed) but doesn't appear at the visible bottom-of-viewport on scroll. Inspection shows `getBoundingClientRect().top` is well below the viewport.

    **Fix at emit time:**
    - Cap the `surecart/product-media` width via `style.dimensions.width:"44px"` (block.json supports this) AND set a small `aspect-ratio` like `"1"`.
    - Set the sticky-purchase wrapper's `style.layout.contentSize` to the page's max container width (e.g. `"1280px"`) so the inner row doesn't stretch arbitrarily.
    - Inside the wrapper, use a SINGLE `core/group` with `layout.type:"flex",flexWrap:"nowrap",justifyContent:"space-between"` as the only direct child. Don't nest 3 sibling groups directly.
    - Keep the buy-button's `add_to_cart:true` + a short `text:"Add to cart"` (avoid long labels like "Subscribe & Save — $49/month" that force wrap).

    Surfaced: atlas-greens (v7.16) — content overflow displaced sticky anchor.

40. **`useFeaturedImage:true` on cover thumbnails overrides per-thumb `background-color` (v7.16, surfaced R2 Atlas Greens).** When the design has a horizontal thumb-strip of placeholder squares below a hero gallery (typical "select swatch" UI), the natural emit is 4× `core/cover` with `useFeaturedImage:true` + per-thumb `color.background` for the swatch color. **The featured image ALWAYS wins** — all 4 thumbs render the same product image, not the 4 distinct swatch colors the design shows.

    **Anti-pattern (drift):**
    ```html
    <!-- wp:cover {"useFeaturedImage":true,"style":{"color":{"background":"#E3EDDE"},...}} -->
    <!-- wp:cover {"useFeaturedImage":true,"style":{"color":{"background":"#F7F5F0"},...}} -->
    <!-- wp:cover {"useFeaturedImage":true,"style":{"color":{"background":"#F0E4D2"},...}} -->
    <!-- wp:cover {"useFeaturedImage":true,"style":{"color":{"background":"#2A332E"},...}} -->
    ```
    All 4 render the same featured image, ignoring the 4 distinct colors.

    **Fix:**
    ```html
    <!-- wp:cover {"useFeaturedImage":false,"style":{"color":{"background":"#E3EDDE"},...}} -->
    ...
    ```
    Drop `useFeaturedImage:true` from thumbnails — only the MAIN gallery cover gets the featured image. Thumbnails are pure decorative placeholders awaiting merchant upload of variant photos.

    **Alternative:** use `core/group` with `color.background:"<hex>"` and a CSS `aspect-ratio` style for the thumbs — even cleaner since there's no semantic image inside.

    Surfaced: atlas-greens (v7.16) — all 4 thumb squares rendered featured image instead of design swatches.

41. **`fontFamily:"surecart-display"` attr + literal `font-family` inline style CONFLICT (v7.16, surfaced R2 Atlas Greens). Pick ONE path.** When emitting `<h1>` / `<h2>` / `<h3>` with both `fontFamily:"surecart-display"` AND `style.typography.fontFamily:"EB Garamond, serif"` (the literal-fallback chain from HC#27), the **class wins** and falls through to whatever the theme's `--wp--preset--font-family--surecart-display` CSS variable resolves to. If the theme doesn't define that var (or it resolves to a sans-serif default), the heading renders in the WRONG typeface — the inline `font-family:EB Garamond, serif` does NOT override the theme-named class.

    **Symptom:** hero h1 renders in theme default sans-serif on the frontend despite emitting `font-family:EB Garamond, serif` in the inline style.

    **Why:** the `.has-surecart-display-font-family { font-family: var(--wp--preset--font-family--surecart-display); }` class is loaded LAST in the cascade. CSS specificity treats class + inline as equal at this level, but the class's `var(...)` reference resolves AT runtime, potentially overriding the inline literal.

    **Two valid paths — never mix:**

    **Path A (theme-aware):** emit `fontFamily:"surecart-display"` ONLY, no `style.typography.fontFamily`. Trust the theme's font preset.
    ```html
    <!-- wp:heading {"fontFamily":"surecart-display","style":{"typography":{"fontSize":"48px","fontWeight":"500"}}} -->
    ```

    **Path B (literal fallback, when theme doesn't define the preset):** emit `style.typography.fontFamily:"EB Garamond, serif"` ONLY, NO `fontFamily:"..."` attr.
    ```html
    <!-- wp:heading {"style":{"typography":{"fontSize":"48px","fontWeight":"500","fontFamily":"EB Garamond, serif"}}} -->
    ```

    **Heuristic:** when the design specifies a SPECIFIC literal typeface name that's unlikely to be a theme preset (custom Google Font like "EB Garamond", "Tiempos", "Söhne"), use Path B. When the design references a known SureCart preset family (system fonts, theme defaults), use Path A.

    Surfaced: atlas-greens (v7.16) — frontend rendered theme sans-serif for h1 while h3 stat numerals rendered in EB Garamond. Inconsistency is the tell.

42. **`core/cover` `isDark` MUST match `color.background` luminance — OMIT `isDark` from JSON when bg is set (v7.17 rule + v7.18.3 PR2 mechanism correction).**

    **Actual mechanism (v7.18.3 corrected):** save() (`node_modules/@wordpress/block-library/build/cover/save.js:65-70`) emits `is-light` ONLY when `!isDark`. It does **NOT** emit `is-dark` (that class appears at edit-time via `useBlockProps` injection, not save()). The real failure path: edit-time `setAttributes({isDark})` in `cover/edit/index.js:283-296` calls `getMediaColor` / `compositeIsDark` and OVERWRITES any explicit JSON `isDark:false` with the computed luminance value. Then save() re-renders and drops `is-light`. The stored attrs (with merchant's original `isDark:false`) now disagree with what save() generates → `validateBlock` class-set mismatch → Block Recovery.

    The prior v7.17 prose "save() emits BOTH is-light AND is-dark" was fabricated — verified against WP source. The empirical rule (OMIT `isDark` from JSON) is still correct as a black-box recipe; only the diagnosis prose changes.

    **Symptom:** console logs `Block validation: Expected attribute 'class' of value 'wp-block-cover ...', saw 'wp-block-cover is-dark ...'` (specific class strings vary by other attrs present).

    **Fix at emit time:**
    - For ANY `core/cover` with `color.background` set: OMIT `isDark` from JSON entirely. Let edit-time compute.
    - Never set `isDark:false` on a dark-bg cover.
    - `useFeaturedImage:true` on a cover WITHOUT a featured image AND with `color.background` can also trigger the same edit-time-vs-stored conflict — drop `useFeaturedImage` for decorative-only thumbnails (HC#40).

    Surfaced: atlas-greens (v7.17) — charcoal `#2A332E` thumbnail with `isDark:false` triggered recovery.

43. **`surecart/product-review-average-rating-breakdown` is a HALLUCINATION — the real block is `surecart/product-review-breakdown` (v7.17, surfaced R2 Atlas Greens "site does not support this block" error).** The long-form name does NOT exist in the inventory.

    **Anti-pattern (drift):** `<!-- wp:surecart/product-review-average-rating-breakdown /-->` — editor shows "Your site does not support this block."

    **Fix:** `<!-- wp:surecart/product-review-breakdown /-->` (short-form). Ancestor: `[surecart/product-page, surecart/product-quick-view, surecart/product-review-list, surecart/product-review-template, surecart/sticky-purchase, surecart/product-review-summary]`.

    **Sibling review-summary blocks — only the breakdown drops the `average-rating` prefix:**
    - `surecart/product-review-breakdown` ✅ (histogram of star ratings)
    - `surecart/product-review-average-rating-stars` ✅ (5-star row)
    - `surecart/product-review-average-rating-value` ✅ (numeric "4.8")
    - `surecart/product-review-total-rating` ✅ (count "1,234 reviews")

    Why this trips up emission: Claude assumes "if `-average-rating-stars` and `-average-rating-value` exist, then `-average-rating-breakdown` must exist too." It does NOT. Pre-emit grep sweep: `grep -E "surecart/product-review-average-rating-breakdown"` — any match = hallucination, rewrite.

44. **`surecart/sticky-purchase` MUST use `surecart/product-selected-variant-image`, NOT `surecart/product-media` (v7.17 + v7.18.3 rationale correction).** Real reason: `surecart/product-media`'s `block.json` declares `ancestor: ["surecart/product-page", "surecart/product-template", "surecart/upsell"]` — `surecart/sticky-purchase` is NOT in that list. Placing `surecart/product-media` inside `surecart/sticky-purchase` violates the ancestor constraint and **blocks block-registration at editor load** (the block silently does not render — not a "wrong-looking" failure, a "missing-block" failure). Use `surecart/product-selected-variant-image` which has the correct ancestor allowlist for sticky-purchase. (The earlier rationale "gallery slider inappropriate for 44px thumb" was a visual-fidelity argument but the actual mechanism is the ancestor block-registration gate.)

    **Canonical inner blocks for `surecart/sticky-purchase`** (per production `sticky-purchase.example.md`):
    - `surecart/product-selected-variant-image` ✅ (NOT `product-media`)
    - `surecart/product-title` `level:4` (smaller than hero h2)
    - `surecart/product-selected-variant` (e.g. "Strength: 15% serum")
    - `surecart/product-selected-price-scratch-amount` (line-through original)
    - `surecart/product-selected-price-amount` (current price)
    - `surecart/product-selected-price-interval` (e.g. "/month")
    - `surecart/product-buy-buttons` → SINGLE `surecart/product-buy-button` (text "Add" or "Add to cart" — no Buy Now pair)

    **Structural rules:**
    - `surecart/sticky-purchase` itself carries `layout.type:"flex",orientation:"horizontal",flexWrap:"nowrap",wideSize:"full",justifyContent:"space-between"` directly. No inner constrained wrapper.
    - Two-zone layout: LEFT info group (`selfStretch:"fit"`, `justifyContent:"left"`) + RIGHT buy-button group (`selfStretch:"fill"`, `justifyContent:"right"`). Both carry `className:"is-vertically-aligned-center"`.
    - The inner info-group has a vertical `core/group` child for stacked title + selected-variant + price-row.

    See `examples/patterns/sticky-purchase.example.md` for the byte-perfect canonical. The R2 Atlas Greens gold was retro-corrected post user-flag (2026-05-27) — previously emitted with the anti-pattern.

45. **NO descriptive HTML comments inside block content areas — only block delimiters (v7.18, surfaced R3 Lumen SaaS; ABSORBS prior HC#22 with greppable enforcement).** Bare HTML comments like `<!-- Section 1: Sticky header -->` or `<!-- Starter tier -->` placed between sibling blocks (NOT inside a `core/html` block) cause validation failures.

    **Actual mechanism (v7.18.3 correction):** the **VALIDATOR** rejects, not the parser. WP's `block-serialization-default-parser` tokenizer is lenient and treats unknown comments as freeform content. The failure occurs at `@wordpress/blocks/build/api/validation/index.js:510-545`, specifically the `isEquivalentHTML` token-type comparator at `:534-536` (`actualToken.type !== expectedToken.type`) — generated `EndTag` vs retrieved `Comment` token causes the mismatch.

    **Both failure signatures observed** (preserved from former HC#22):
    - `Block validation: Expected end of content, instead saw {type: 'Comment', chars: ' 1. HERO === '}` (apiVersion:3 wrapper variant)
    - `Block validation: Expected token of type 'EndTag' (Object), instead saw 'Comment' (Object)` (general block-validation variant)

    **Sibling-skill silent-drop variant (SHC#10):** in `surecart/product-template`'s per-card inner template (server iterates per product), descriptive comments inside the per-card cover's `<div class="wp-block-cover__inner-container">` cause inner blocks to be **silently dropped** during parse — no error, no recovery prompt, just an empty card grid. Same root-cause (parser-vs-validator mismatch) but presents as data-loss rather than recovery dialog. Always strip comments from per-card templates too.

    **Anti-pattern:**
    ```html
    <!-- wp:group {...} -->
    <div class="wp-block-group">

    <!-- Starter tier -->            ← FORBIDDEN

    <!-- wp:group {...} -->
    <div class="wp-block-group">...</div>
    <!-- /wp:group -->

    <!-- Pro tier (highlighted) -->  ← FORBIDDEN

    <!-- wp:group {...} -->
    ...
    ```

    **Allowed forms of HTML comments:**
    - **`<!-- wp:* -->` / `<!-- /wp:* -->` block delimiters.** These ARE comments syntactically but are recognized as block tokens.
    - **Comments inside `core/html` content area.** The HTML block's inner content is opaque — comments there don't get parsed by Gutenberg's block tree.
    - **Comments inside `core/code` or `core/preformatted` content** for similar reasons (code/preformatted text is opaque).

    **Forbidden:**
    - Section labels (`<!-- Section 1: Sticky header -->`)
    - Card-row labels (`<!-- Starter tier -->`, `<!-- Pro tier (highlighted) -->`)
    - Any "what this block does" annotation inside markup
    - Even single-line block-comments between sibling `<!-- wp:* -->` openers

    **Pre-emit grep sweep (Tier A blocking):**
    ```
    grep -nE '^<!-- [^/w]' <output.html>   # find comment lines NOT starting with </ or /w
    grep -nE '^<!-- [^/]?[^w]?[^p]' <output.html>  # finds "<!-- " not followed by "/wp:" or "wp:"
    ```
    Any match = anti-pattern. Strip via `sed -i.bak -E '/^<!-- (Section|Starter|Pro|Team|Card|Step|Tier|Row|Col)/d' <output.html>` or equivalent — but **best practice is to NEVER emit them in the first place**. Use code comments in your composition planning notes, NOT in the emitted markup.

    **Why the doctrine exists at all:** Gutenberg's block-parser walks tokens sequentially. A `<div>` open expects a matching `</div>` close on the next "structural" token. Comments in the content area appear as `Comment` tokens between them, and the validator can't reconcile the unexpected comment with the awaited end-tag → validation failure cascades.

    **Why this was previously underweighted:** the existing A-21 rubric item ("no comments inside the wrapper") was documented in 2026-05 (v7.6) but the enforcement was prose-only — not a grep-checkable Tier A blocker. R3 Lumen SaaS (2026-05-27) violated it across 17 section labels because the skill didn't grep-check before emitting. Promoting to HC#45 with explicit greppable rule.

    Surfaced: lumen-saas (v7.18) — 20 descriptive comments triggered recovery; strip-then-paste cleared all.

46. **`surecart/product-variant-pills` emits ONCE — server iterates ALL variant axes (v7.18.2, surfaced R4 Halcyon Field Jacket user-flagged double-render).** When the design has MULTIPLE variant axes (e.g., color + size), emit ONE `surecart/product-variant-pills` block. The server iterates over EVERY axis configured on the SureCart product (color, size, material, etc.) and renders them all as separate pill groups stacked vertically — automatically.

    **Symptom:** emitting two `<!-- wp:surecart/product-variant-pills -->` blocks (one labeled "Color", one labeled "Size") produces DOUBLE rendering — each block renders ALL variant axes, so the variants appear twice on the frontend.

    **Anti-pattern (drift):**
    ```html
    <!-- wp:group {"className":"color-row"} -->
      <!-- wp:paragraph -->Color<!-- /wp:paragraph -->
      <!-- wp:surecart/product-variant-pills -->
        <!-- wp:surecart/product-variant-pill {color-styled} /-->
      <!-- /wp:surecart/product-variant-pills -->
    <!-- /wp:group -->
    <!-- wp:group {"className":"size-row"} -->
      <!-- wp:paragraph -->Size<!-- /wp:paragraph -->
      <!-- wp:surecart/product-variant-pills -->          ← SECOND BLOCK
        <!-- wp:surecart/product-variant-pill {size-styled} /-->
      <!-- /wp:surecart/product-variant-pills -->
    <!-- /wp:group -->
    ```

    Each `product-variant-pills` block iterates over ALL the product's variant axes, so this emits color × 2 AND size × 2.

    **Canonical fix:**
    ```html
    <!-- wp:surecart/product-variant-pills {"style":{"color":{"text":"#EFE9DC"},...}} -->
    <!-- wp:surecart/product-variant-pill {"highlight_text":"#EFE9DC","highlight_background":"#C8694A","highlight_border":"#C8694A","style":{"border":{"radius":"9999px"},"color":{"text":"#EFE9DC"},...}} /-->
    <!-- /wp:surecart/product-variant-pills -->
    ```

    ONE block. The server adds an "Color" / "Size" / "Material" axis label automatically based on the product's configured variant options. The skill emits ONE pill child template, the server expands it per-option per-axis.

    Surfaced: halcyon-field-jacket (v7.18.2) — user-flagged double-render.

47. **`surecart/product-variant-pill` border attrs cause apparent "wrapper border" — emit only `border.radius`, NOT `border.{width,color,style}` (v7.18.2, surfaced R4 Halcyon Field Jacket user flag).** When emitting per-chip border (`border.{width:"1px",color:"#hex",style:"solid"}`) on `surecart/product-variant-pill`, each chip pill gets a visible 1px outline. When pills are tightly packed (small gap, side-by-side), the per-chip borders LOOK like a continuous wrapper border around the entire group — which is rarely the design intent.

    **Symptom:** user reports "the variants pills combined has a border to it. It should not be there" — referring to what appears to be a wrapper outline around the pills group, but is actually 1px borders on each individual chip.

    **Anti-pattern (drift):**
    ```html
    <!-- wp:surecart/product-variant-pill {"style":{"border":{"radius":"9999px","width":"1px","color":"#353330","style":"solid"},...}} /-->
    ```

    **Canonical fix — keep ONLY border.radius (for pill shape):**
    ```html
    <!-- wp:surecart/product-variant-pill {"style":{"border":{"radius":"9999px"},"color":{"text":"#EFE9DC"},"elements":{"link":{"color":{"text":"#EFE9DC"}}}}} /-->
    ```

    Drop `width`/`color`/`style` from the border subobject. Pills get pill-shape from `radius:9999px` alone. If the design explicitly shows per-chip outlines, keep `width:1px,color:"#hex",style:"solid"` — but verify by visual inspection of the design preview, not by reflex.

    The `highlight_*` attrs (`highlight_text`/`highlight_background`/`highlight_border`) handle the SELECTED-pill chrome regardless of base border — they're a separate axis. So you can have unbordered base pills + a visible border on the selected one via `highlight_border`.

    Surfaced: halcyon-field-jacket (v7.18.2) — user-flagged apparent wrapper border (was N per-chip 1px borders merging visually).

48. **File-output exclusivity — chat-leak hard gate (v7.18.3 — PR2).** When the file-write branch fires (per the Step 4 threshold `markup ≥ 5,120 bytes`), in the SAME response AND in every subsequent response within the conversation until the merchant pastes:

    - The chat response MUST NOT contain ANY of: a fenced code block of ANY language (```html, ```text, ```xml, ```markdown, ```bash, ``` bare), an indented code block, OR any line beginning with `<!-- wp:` OR any text containing `wp:surecart/` or `wp:core/`.
    - The chat carries EXACTLY these sections in order: (1) self-validation line, (2) 1–2 sentence summary, (3) drift report JSON (NO field value may contain `<!-- wp:`), (4) the paste-instructions block per Step 4 paste-path.
    - If the merchant requests an excerpt, partial, "show me line N", or "show me just the hero" — REFUSE and point at the file path. The file is the authoritative source.
    - **Pre-respond greppable check (run mentally; record result as part of self-validation):** `grep -nE '^[[:space:]]*<!-- wp:|^[[:space:]]*` + ASCII backtick × 3 + `|wp:surecart/|wp:core/' <draft-response>` MUST return zero matches. If non-zero, strip and re-check before responding.
    - **Cross-turn binding:** once a response in this conversation thread invoked file-write, every subsequent response IN THE SAME THREAD must also obey this rule until the merchant reports successful paste.

49. **JSON string values: unescaped `<`, `>`, `&`, `\"`, `--` are forbidden in any block-comment JSON (v7.18.3 — PR2).** WP's `serializeAttributes` (`node_modules/@wordpress/blocks/build/api/serializer.js:244-257`) Unicode-escapes 5 character classes on save() round-trip:

    1. `--` → `--`
    2. `<` → `<`
    3. `>` → `>`
    4. `&` → `&`
    5. `\"` → `"` (the stripslashes-bypass escape — easy to miss)

    First-paste works because the parser is lenient. But the editor save re-emits with the escapes, validateBlock then sees a stored↔generated mismatch on the next edit → recovery cascade.

    **Pre-emit greppable check** (refined to distinguish raw chars from already-escaped HTML entities — `&amp;` / `&lt;` / `&#xNN;` are correct in rendered-text attrs like `content` / `summary` / `text` / `label` / `placeholder` / `ariaLabel`):

    ```
    grep -oE '"[^"\\]*(\\.[^"\\]*)*"' <output> | \
      grep -E '(<(?!!--|/)|>(?<!--)|&(?!(amp|lt|gt|quot|apos|#[0-9]+|#x[0-9a-fA-F]+);)|--(?![->]))'
    ```

    Zero matches expected.

    **Scope by attr type:**
    - `style.*` JSON values (pure-data attrs) — no raw `<>&"--` allowed.
    - Rendered-text attrs (`content`, `summary`, `text`, `label`, `placeholder`, `ariaLabel`, `metadata.name`) — emit already-escaped entity forms when the source design has `&` / `<` / `>` / `"` / em-dash characters in displayed text (e.g., `&amp;`, `&lt;3`, `AT&amp;T`).

    Also flag: U+2028 / U+2029 / U+0085 / U+FEFF are valid JSON but unsafe (some merchant editors silently strip them). Em-dash / en-dash / smart quotes are SAFE for `serializeAttributes` but separately risky per HC#16 (chat-render quote-substitution → use the file-write path).

50. **Review-template inner-block hallucinations — `-author-info` / `-rating` / `-author` / `-stars` / `-card` are NOT real (v7.22.1, surfaced 2026-05-28 Hearth & Hollow paste-test).** When emitting the per-review card inner blocks inside `surecart/product-review-template`, the natural English-derived names DO NOT EXIST in the inventory. The editor reports "Your site doesn't include support for this block" on first paste; the per-review card renders empty.

    **Anti-patterns (drift) — all 5 hallucinated:**
    - `surecart/product-review-author-info` ❌
    - `surecart/product-review-rating` ❌
    - `surecart/product-review-author` ❌
    - `surecart/product-review-stars` ❌
    - `surecart/product-review-card` ❌

    **Canonical 6-block per-review card inner template** (verified against `packages/blocks-next/src/blocks/product-review-list/template.js:531-755`):

    | Hallucinated name | Canonical replacement |
    |---|---|
    | `-author-info` / `-author` | `surecart/product-review-reviewer-name` (+ optional sibling `surecart/product-review-date` + `surecart/product-review-verified-badge`) |
    | `-rating` / `-stars` | `surecart/product-review-rating-stars` (the per-card 5-star row — NOT the summary block's `-average-rating-stars`) |
    | `-card` | (compose from the 6 inner blocks below; no atomic card block exists) |

    **Canonical inner-block set for `surecart/product-review-template`:**

    - `surecart/product-review-reviewer-name` — reviewer's display name
    - `surecart/product-review-verified-badge` — "Verified purchase" pill
    - `surecart/product-review-date` — submission date
    - `surecart/product-review-rating-stars` — per-card 5-star row
    - `surecart/product-review-title` — review headline
    - `surecart/product-review-content` — review body text

    Minimal paste-safe template (all 6 self-closing apiVersion:3 blocks):

    ```html
    <!-- wp:surecart/product-review-template -->
    <!-- wp:surecart/product-review-reviewer-name /-->
    <!-- wp:surecart/product-review-verified-badge /-->
    <!-- wp:surecart/product-review-date /-->
    <!-- wp:surecart/product-review-rating-stars /-->
    <!-- wp:surecart/product-review-title /-->
    <!-- wp:surecart/product-review-content /-->
    <!-- /wp:surecart/product-review-template -->
    ```

    **Pattern recognition (same root cause as HC#43):** review-domain blocks follow specific suffix families. Per-card rating uses `-rating-stars`. Reviewer attribution uses `-reviewer-name` / `-verified-badge` / `-date`. The shorter `-author` / `-author-info` / `-rating` / `-stars` / `-card` forms are linguistically natural but were never registered.

    **Pre-emit greppable sweep (Tier A blocking):**

    ```
    grep -nE "surecart/product-review-(author|author-info|rating[^-]|stars[^-]|card)([[:space:]]|/?-->|$)" <output.html>
    ```

    Any match = hallucination, rewrite via the table above. The `-rating[^-]` and `-stars[^-]` lookaheads distinguish the canonical `-rating-stars` and `-average-rating-stars` suffixes from the bare hallucinated forms.

    **Two-skill propagation:** the same hallucinations apply to the `surecart-design-to-shop-page` sibling skill when emitting per-card review chrome inside `surecart/product-template` cards. Inherited via shared `reference/alias-map.md`.

51. **Intake-emitted Claude Design prompt §4 palette discipline — name ONE accent slug, FORBID companion-slug invention (v7.22.1, surfaced 2026-05-28 Hearth & Hollow paste-test).** When intake mode emits a Claude Design prompt with `surecart-orange-500` named as the accent slug (per `palette-presets.md`), Claude Design extrapolates and invents a full earth-tone palette of adjacent slug names — `surecart-orange-100`, `surecart-orange-700`, `surecart-oak-900`, `surecart-olive-700`, `surecart-olive-200`, `surecart-ochre-500`, `surecart-cream-50`, etc. None of these exist in `reference/theme-partial.json`. Per HC#13, the skill must NEVER invent slugs, so the converter falls back to literal-hex with D7 dual-emit (works on any theme but bypasses the merchant's theme-overridable preset system).

    **Failure signature:** the Hearth & Hollow design's `colors_and_type.css` declared 14 `--sc-*` CSS-vars referencing `var(--wp--preset--color--surecart-{color}-{shade})` slugs that don't exist. 11 of 14 were Claude-Design-invented companion slugs adjacent to the one named accent.

    **Why this happens:** Claude Design's training prior includes Tailwind-style palette systems (e.g. `slate-50` through `slate-950`). When given one slug like `surecart-orange-500`, it extrapolates the full scale (`100`, `200`, ..., `900`) plus invents thematically-adjacent palettes (oak, olive, ochre, cream for an earthy mood). The intake prompt's §4 needs to actively SUPPRESS this extrapolation.

    **Fix at intake prompt emission time** — append explicit palette-discipline language to §4 (style tokens):

    > **Palette discipline.** Use ONLY the named accent slug above (`{{ACCENT_PRESET_SLUG}}`) and the SureCart neutral palette: `surecart-text`, `surecart-text-muted`, `surecart-bg`, `surecart-surface`, `surecart-border`. Do NOT extrapolate companion slugs (no `-100` / `-200` / `-700` / `-900` shades; no thematically-adjacent named slugs like `-oak` / `-olive` / `-ochre` / `-cream`). When the design needs additional shades or earth tones for visual depth, write raw `#RRGGBB` literals — the converter handles them via D7 dual-emit. Inventing slug names that aren't in the merchant's `theme.json` produces silently-failing references at server-render time.

    **Tier I rubric update (I-10 — new):** before emitting the Claude Design prompt, verify §4 contains the palette-discipline paragraph above. Greppable: prompt must contain the literal string `Palette discipline.` exactly once.

    **Sibling skill propagation:** same fix lands in `surecart-design-to-shop-page/intake/prompt-template.md` §4.

    **Recovery path (when palette inflation has already happened):** the converter logs all invented-slug references under `color_snap_misses[]` and emits literal-hex throughout. The page renders correctly on any theme. To restore theme-overridability post-paste, the merchant either (a) registers the missing slugs in their site's `theme.json`, or (b) accepts the literal-hex baseline.

    Surfaced: Hearth & Hollow Almanac paste-test (2026-05-28) — Claude Design invented 11 adjacent slugs from the one named `surecart-orange-500` accent. All resolved to literal-hex by HC#13's slug-validation gate.

52. **`core/separator` with literal-hex `style.color.background` REQUIRES `opacity:"alpha-channel"` attr AND `has-alpha-channel-opacity` class (v7.22.2, surfaced 2026-05-28 Hearth & Hollow paste-test).** When emitting `core/separator` with a literal-hex `style.color.background:"#hex"` and OMITTING the `opacity` attr, the editor logs:

    > Block validation failed for `core/separator`. Expected class `wp-block-separator has-text-color has-alpha-channel-opacity has-background is-style-default`, saw `wp-block-separator has-text-color has-background is-style-default`.

    **Actual mechanism** (verified against `node_modules/@wordpress/block-library/build/separator/save.js:32-42`): `save()` calls `clsx({'has-alpha-channel-opacity': opacity === 'alpha-channel'})`. The block.json sets `opacity:"alpha-channel"` as the default for new separator inserts, but Gutenberg's parser stores it as a real attr when blocks are saved. Hand-written paste-form without the attr stores `opacity:undefined`, but save() regenerates with the default-injected attr → class-set mismatch → recovery.

    **Fix at emit time:**

    | When | JSON attr | Class emitted |
    |---|---|---|
    | Literal-hex `style.color.background:"#hex"` | `"opacity":"alpha-channel"` (mandatory) | `has-text-color has-alpha-channel-opacity has-background` |
    | Slug `backgroundColor:"surecart-brand"` | `"opacity":"alpha-channel"` (still mandatory — defaults same) | `has-text-color has-alpha-channel-opacity has-{slug}-background-color has-background` |
    | NO color set | (omit `opacity` AND `color`) | `wp-block-separator` (bare) |

    **Canonical exemplar:**

    ```html
    <!-- wp:separator {"opacity":"alpha-channel","style":{"color":{"background":"#E5DDD0"},"spacing":{"margin":{"top":"28px","bottom":"28px"}}},"className":"is-style-default"} -->
    <hr class="wp-block-separator has-text-color has-alpha-channel-opacity has-background is-style-default" style="margin-top:28px;margin-bottom:28px;background-color:#E5DDD0;color:#E5DDD0"/>
    <!-- /wp:separator -->
    ```

    **Class set order** (per save.js):
    1. `wp-block-separator` (always — via useBlockProps)
    2. `has-text-color` (when `backgroundColor` OR `style.color.background`)
    3. `has-{slug}-color` (when `backgroundColor` slug — note: `color`, not `background-color`, because separator uses text-color for the `<hr>` rule)
    4. `has-alpha-channel-opacity` (when `opacity === 'alpha-channel'` — the default)
    5. `has-background` (when literal `style.color.background`)
    6. `is-style-{variant}` (when `className` set — `is-style-default` / `is-style-dots` / `is-style-wide`)

    **Other opacity values:** `opacity:"css"` emits `has-css-opacity` instead (legacy 0.4-opacity-via-CSS-rule path). New code should always use `"alpha-channel"`.

    **Greppable sweep:**

    ```
    grep -nE "wp-block-separator[^\"]*has-background[^\"]*\"[^o]" <output.html>
    ```

    Any match WITHOUT `has-alpha-channel-opacity` between `has-text-color` and `has-background` is broken.

    Surfaced: Hearth & Hollow Almanac paste-test (2026-05-28) — hero divider with `style.color.background:"#E5DDD0"` and `className:"is-style-default"` triggered class-set mismatch + Block Recovery prompt.

53. **`surecart/product-review-list` canonical inner structure — summary + template are SIBLINGS inside `surecart/product-reviews` wrapper, NOT direct children of `product-review-list` (v7.22.2, surfaced 2026-05-28 Hearth & Hollow paste-test).** Emitting `surecart/product-review-summary` and `surecart/product-review-template` as direct children of `surecart/product-review-list` produces wrong-shape rendering (top/bottom stack with no chrome). The canonical structure (verified against `packages/blocks-next/src/blocks/product-review-list/template.js:24-755`) wraps both in `surecart/product-reviews`.

    **Anti-pattern (drift) — direct children of product-review-list:**
    ```html
    <!-- wp:surecart/product-review-list -->
      <!-- wp:surecart/product-review-summary -->...<!-- /wp:surecart/product-review-summary -->
      <!-- wp:surecart/product-review-template -->...<!-- /wp:surecart/product-review-template -->
    <!-- /wp:surecart/product-review-list -->
    ```

    Renders as a vertical T/B stack with no internal layout — visually unstyled.

    **Canonical structure — wrapped in `surecart/product-reviews`:**
    ```html
    <!-- wp:surecart/product-review-list -->
    <!-- wp:surecart/product-reviews -->
      [layout structure here — typically core/columns 2-col]
      <!-- wp:surecart/product-review-summary -->...<!-- /wp:surecart/product-review-summary -->
      <!-- wp:surecart/product-review-template -->...<!-- /wp:surecart/product-review-template -->
    <!-- /wp:surecart/product-reviews -->
    <!-- /wp:surecart/product-review-list -->
    ```

    **Layout patterns by design intent:**

    | Design shape | Inside `surecart/product-reviews` |
    |---|---|
    | Summary LEFT + template RIGHT (most common — typical e-commerce reviews block) | `core/columns` 2-col → summary in `core/column [38-40%]` LEFT, template in `core/column [60-62%]` RIGHT |
    | Summary TOP + template BELOW | direct siblings, no `core/columns` wrapper (just `surecart/product-reviews` + the two children) |
    | Compact: summary INSIDE template card (inline) | not supported — they are separate blocks; use the L/R or T/B pattern |

    **Canonical L/R exemplar (paste-tested 2026-05-28 Hearth & Hollow fix):**

    ```html
    <!-- wp:surecart/product-review-list -->
    <!-- wp:surecart/product-reviews -->
    <!-- wp:columns {"verticalAlignment":"top","style":{"spacing":{"blockGap":{"left":"48px","top":"32px"}}}} -->
    <div class="wp-block-columns are-vertically-aligned-top">

    <!-- wp:column {"verticalAlignment":"top","width":"38%"} -->
    <div class="wp-block-column is-vertically-aligned-top" style="flex-basis:38%">
    <!-- wp:surecart/product-review-summary -->
    <!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap","verticalAlignment":"center"},"style":{"spacing":{"blockGap":"14px","margin":{"bottom":"16px"}}}} -->
    <div class="wp-block-group" style="margin-bottom:16px">
    <!-- wp:surecart/product-review-average-rating-stars /-->
    <!-- wp:surecart/product-review-average-rating-value /-->
    <!-- wp:surecart/product-review-total-rating /-->
    </div>
    <!-- /wp:group -->
    <!-- wp:surecart/product-review-breakdown /-->
    <!-- /wp:surecart/product-review-summary -->
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"verticalAlignment":"top","width":"62%"} -->
    <div class="wp-block-column is-vertically-aligned-top" style="flex-basis:62%">
    <!-- wp:surecart/product-review-template -->
    <!-- wp:surecart/product-review-reviewer-name /-->
    <!-- wp:surecart/product-review-verified-badge /-->
    <!-- wp:surecart/product-review-date /-->
    <!-- wp:surecart/product-review-rating-stars /-->
    <!-- wp:surecart/product-review-title /-->
    <!-- wp:surecart/product-review-content /-->
    <!-- /wp:surecart/product-review-template -->
    </div>
    <!-- /wp:column -->

    </div>
    <!-- /wp:columns -->
    <!-- /wp:surecart/product-reviews -->
    <!-- /wp:surecart/product-review-list -->
    ```

    **Ancestor constraint note:** `surecart/product-review-template`'s block.json declares `"ancestor": ["surecart/product-review-list-content"]`. Empirically the ancestor check is lenient (walks up the chain or accepts `surecart/product-reviews` as an alias) — the canonical SureCart template itself uses `product-reviews` as the wrapper. Both pass paste validation. If a future Gutenberg version tightens the check, swap `surecart/product-reviews` → `surecart/product-review-list-content` (both blocks exist; the latter has `ancestor: ["surecart/product-review-list"]` so the wrap still nests correctly).

    **Detection signal at emit time:** if the design's Claude Design `<ReviewSection/>` placeholder shows the summary visually side-by-side with reviewer cards (rather than as a band above the cards), prefer the L/R variant. If the design shows summary as a wide horizontal band above the review cards, use the T/B variant.

    **Paste-test verified:** 2026-05-28 Hearth & Hollow paste-test #2 — user-flagged top/bottom stack; L/R inside `product-reviews` cleared the layout drift.

54. **`surecart/product-list-title` / `-image` / `-name` are HALLUCINATIONS — only `-price` and `-related` carry the `list-` prefix (v7.22.3, surfaced 2026-06-02 Aurora Pro paste-test).** When emitting per-card inner blocks inside `surecart/product-list-related > surecart/product-template`, the LLM extrapolates `surecart/product-list-*` as the canonical per-card prefix and invents names. Same family as HC#43 (`-average-rating-breakdown` hallucination) and HC#50 (review-template inner-block hallucinations).

    **Anti-patterns and canonical replacements** (verified against `packages/blocks-next/src/blocks/*/block.json`):

    | ❌ DOES NOT EXIST | ✅ CANONICAL |
    |---|---|
    | `surecart/product-list-title` | `surecart/product-title` (level:2 for cards; ancestor allowlist already includes `surecart/product-template`) |
    | `surecart/product-list-image` | `core/cover {useFeaturedImage:true}` (verified Start-Basic uses cover, NOT a SureCart image block) — alternate: `surecart/product-image` (registered, ancestor `surecart/product-list`) |
    | `surecart/product-list-name` | `surecart/product-title` |
    | `surecart/product-list-card` | (compose: `core/group` wrapping cover + title + price) |

    **Why this trips the LLM:** the directory `packages/blocks-next/src/blocks/product-price/` registers as `surecart/product-list-price` (counterintuitive directory/name mismatch). Combined with `surecart/product-list-related` being a real block, the natural extrapolation is `product-list-{title,image,name}` — but the per-card title/image use the SAME blocks as the hero (`product-title` and `core/cover {useFeaturedImage:true}`). Their `ancestor` allowlists already include `surecart/product-template`, so no separate `list-` prefixed block is needed.

    **Failure signature:** editor displays "Your site doesn't include support for this block" on each affected card after first paste.

    **Pre-emit grep sweep (Tier A blocking):**

    ```
    grep -nE "surecart/product-list-(title|image|name|card)([[:space:]]|/?-->|$)" <output.html>
    ```

    Any match = hallucination, rewrite via the table above.

    **Canonical Start-Basic per-card template** (byte-perfect, verified at `packages/blocks-next/src/blocks/product-list/block.json:140-300`):

    ```html
    <!-- wp:surecart/product-template -->
    <!-- wp:group -->
    <div class="wp-block-group">
    <!-- wp:cover {"useFeaturedImage":true,"dimRatio":0,"isUserOverlayColor":true,"focalPoint":{"x":0.5,"y":0.5},"isDark":false,"style":{"dimensions":{"aspectRatio":"3/4"},"spacing":{"margin":{"bottom":"15px"}},"border":{"radius":"10px"}}} -->
    <div class="wp-block-cover" style="border-radius:10px;margin-bottom:15px"><span aria-hidden="true" class="wp-block-cover__background has-background-dim-0 has-background-dim"></span><div class="wp-block-cover__inner-container"></div></div>
    <!-- /wp:cover -->

    <!-- wp:surecart/product-title {"level":2,"style":{"typography":{"fontSize":"15px","fontWeight":"400"},"spacing":{"margin":{"top":"0px","bottom":"5px"}}}} /-->

    <!-- wp:group {"style":{"spacing":{"blockGap":"0.5em"}},"layout":{"type":"flex","flexWrap":"nowrap"}} -->
    <div class="wp-block-group">
    <!-- wp:surecart/product-list-price {"style":{"typography":{"fontSize":"18px","fontWeight":"600"}}} /-->
    <!-- wp:surecart/product-scratch-price {"style":{"typography":{"fontSize":"18px","fontWeight":"600"}}} /-->
    </div>
    <!-- /wp:group -->
    </div>
    <!-- /wp:group -->
    <!-- /wp:surecart/product-template -->
    ```

    See `reference/alias-map.md § Per-card inner-block hallucinations` for the full per-card hallucination table + canonical template.

55. **`surecart/product-media` overflows the editor unless `desktop_gallery:true` is set (v7.22.3, surfaced 2026-06-02 Aurora Pro paste-test).** The block ships TWO registered variations (verified at `packages/blocks-next/src/blocks/product-media/block.json`):

    - `slider` (default, `desktop_gallery:false`) — single image with thumbnail-strip nav, fixed `height:"310px"`, IGNORES parent container width semantics.
    - `gallery` (`desktop_gallery:true`) — desktop full-gallery layout (Apple-style image grid) that RESPECTS parent container width.

    **Symptom:** the default slider variation renders at a fixed 310px height and overflows / under-fills the parent flex column in the editor. Looks especially broken inside a 2-col hero where the gallery side is constrained to ~55% width — the slider's internal layout doesn't reflow.

    **Fix at emit time:** ALWAYS pass `desktop_gallery:true` when emitting `surecart/product-media` inside a constrained-width flex column (i.e. anywhere except a full-width product-page hero where the slider's 310px works). This switches to the gallery variation which respects container width.

    ```html
    <!-- wp:surecart/product-media {"desktop_gallery":true} /-->
    ```

    **Auxiliary attrs to consider:**
    - `auto_height: true` (default) — keeps image aspect; good for gallery variation.
    - `show_thumbnails: true` (default) — gallery variation shows them as a separate strip below.
    - `lightbox: true` (default) — click-to-zoom on the gallery images.
    - `thumbnails_per_page: 5` (default) — number of thumb-strip slots visible at once.

    **Ancestor constraint** (unchanged per HC#44): `surecart/product-media` allowed inside `surecart/product-page`, `surecart/product-template`, `surecart/upsell` ONLY. NOT inside `surecart/sticky-purchase` — use `surecart/product-selected-variant-image` there.

    **Detection signal at emit time:** if the design places the gallery inside a narrower-than-full-width parent (hero 2-col split, sidebar layout, modal), emit `desktop_gallery:true`. If the design places the gallery as a full-width band (rare), the default slider works.

56. **Per-review template inner blocks emit BARE — drop all `style` attrs to avoid recovery cascades (v7.22.3, surfaced 2026-06-02 Aurora Pro paste-test).** When emitting the 6 canonical per-review inner blocks inside `surecart/product-review-template` (`surecart/product-review-rating-stars`, `-title`, `-content`, `-reviewer-name`, `-date`, `-verified-badge`), do NOT pass `style` attrs.

    **Why:** all 6 inner blocks are `apiVersion:3` server-rendered with internal Stencil/Web Component chrome. While they DECLARE typography/color/spacing supports in block.json, the server-rendered HTML doesn't reliably reflect inline `style` attrs — and the editor's reconciliation can produce class-set drift mismatching the stored attrs, triggering "Attempt Block Recovery" cascades on first save round-trip.

    **Symptom:** "Attempt Block Recovery" prompts on every review card in the editor after paste; clicking Recover strips the style attrs.

    **Fix at emit time:** all 6 inner blocks emit SELF-CLOSING with NO `style` attr:

    ```html
    <!-- wp:surecart/product-review-template -->
    <!-- wp:surecart/product-review-rating-stars /-->
    <!-- wp:surecart/product-review-title /-->
    <!-- wp:surecart/product-review-content /-->
    <!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap","justifyContent":"space-between"},"style":{"spacing":{"padding":{"top":"14px","bottom":"0"}},"border":{"top":{"color":"#E8E8E8","width":"1px"}}}} -->
    <div class="wp-block-group" style="border-top-color:#E8E8E8;border-top-width:1px;padding-top:14px;padding-bottom:0">
    <!-- wp:surecart/product-review-reviewer-name /-->
    <!-- wp:surecart/product-review-date /-->
    </div>
    <!-- /wp:group -->
    <!-- /wp:surecart/product-review-template -->
    ```

    **Style customization routing:** wrap the entire `surecart/product-review-template` in a `core/group` with the card chrome (background, border, padding, margin), and style sibling-row layouts via intermediate `core/group` flex wrappers. **Typography on the per-review blocks themselves comes from the theme + the block's registered styles** — not from inline `style` attrs.

    **Same family as HC#38** (server-rendered chrome via wrap-and-target) — but specifically targeted at the review-template inner blocks because their per-card iteration multiplies any recovery failure across N cards.

    **Pre-emit greppable check:**

    ```
    grep -nE "wp:surecart/product-review-(rating-stars|title|content|reviewer-name|date|verified-badge)[^/]*\"style\"" <output.html>
    ```

    Any match = bare-emit violation; strip the `style` attr.

57. **`surecart/product-variant-pill` border-color/width/style ALWAYS produces visible per-chip borders (v7.18.2 HC#47 ENFORCEMENT REINFORCEMENT — repeated violation 2026-06-02 Aurora Pro paste-test).**

    HC#47 already documents the rule: drop `border.{width,color,style}` from `surecart/product-variant-pill` JSON; keep ONLY `border.radius`. But the rule was VIOLATED in the Aurora Pro emit (2026-06-02) despite being in the canon. Promoting from "documented but not enforced" to "Tier A blocking grep check".

    **Pre-emit greppable check (Tier A blocking — fails the rubric):**

    ```
    grep -nE "wp:surecart/product-variant-pill[^/]*\"border\":\{[^}]*(\"width\"|\"color\"|\"style\")" <output.html>
    ```

    Any match (anything in the pill's `border` subobject OTHER than `radius`) = violation. Strip the non-radius border attrs before emit.

    **Allowed:**
    ```
    "style":{"border":{"radius":"9999px"}}
    ```

    **Forbidden:**
    ```
    "style":{"border":{"radius":"9999px","width":"1px","color":"#E8E8E8","style":"solid"}}
    "style":{"border":{"radius":"9999px","width":"1px"}}
    "style":{"border":{"color":"#hex"}}
    ```

    The `highlight_border` attr remains the ONLY way to render a visible border on the SELECTED pill (and only on the selected one — the rest stay borderless via `border.radius` alone).

58. **`core/cover` `useFeaturedImage:true` + `color.background` literal hex is INCOMPATIBLE — the bg-color triggers `is-light/is-dark` class set save() ALWAYS emits but hand-written wrappers miss (v7.22.4, surfaced 2026-06-02 Aurora Pro paste-test — extends HC#42 with greppable enforcement).**

    HC#42 already documents "OMIT `isDark` from JSON when bg is set." This HC extends it: when a `core/cover` block carries BOTH `useFeaturedImage:true` AND `style.color.background:"#hex"`, the combination is an ANTI-PATTERN. Three things go wrong simultaneously:

    1. **The literal bg-color is redundant** — `useFeaturedImage:true` makes the featured image the background. Once the merchant uploads the product's featured image, the literal `#efeeea` (or whatever) is HIDDEN behind the image. The literal hex is only visible in the editor pre-upload — and even then it's the same surface a plain `core/group` would provide.

    2. **save() ALWAYS emits the `is-light` OR `is-dark` class** based on edit-time luminance computation of the bg-color (cover/edit/index.js:283-296 calls `getMediaColor` / `compositeIsDark`). A hand-written wrapper class set that says only `wp-block-cover has-background` (without `is-light` or `is-dark`) WILL drift on first save round-trip — `validateBlock` sees stored `wp-block-cover has-background` vs generated `wp-block-cover is-light has-background` → Block Recovery cascade through every card.

    3. **JSON `style.spacing.margin.bottom:"14px"` requires inline mirror parity (HC#26)** — hand-written wrapper missing the corresponding `margin-bottom:14px` in inline `style=""` adds a SECOND drift on top of the class-set drift.

    **Failure signature (verified 2026-06-02):**
    > `Block validation: Expected attribute 'class' of value 'wp-block-cover is-light has-background', saw 'wp-block-cover has-background'.`
    > Content generated by save: `<div class="wp-block-cover is-light has-background" style="border-radius:0;background-color:#efeeea;margin-bottom:14px">`
    > Content retrieved from post body: `<div class="wp-block-cover has-background" style="border-radius:0;background-color:#efeeea">`

    **Fix at emit time — three valid paths, pick ONE:**

    **Path A (canonical — preferred for related-product cards):** DROP both `color.background` AND `isDark` from JSON. Cover renders as transparent until featured image loads. Wrapper class: `wp-block-cover` (bare).

    ```html
    <!-- wp:cover {"useFeaturedImage":true,"dimRatio":0,"isUserOverlayColor":true,"focalPoint":{"x":0.5,"y":0.5},"style":{"dimensions":{"aspectRatio":"1"},"spacing":{"margin":{"bottom":"14px"}},"border":{"radius":"0"}},"layout":{"type":"default"}} -->
    <div class="wp-block-cover" style="border-radius:0;margin-bottom:14px"><span aria-hidden="true" class="wp-block-cover__background has-background-dim-0 has-background-dim"></span><div class="wp-block-cover__inner-container"></div></div>
    <!-- /wp:cover -->
    ```

    **Path B (byte-perfect canonical Start-Basic — when `isDark:false` is required for editor preview):** keep `isDark:false`, ADD `is-light` to the wrapper class. Still drop `color.background`.

    ```html
    <!-- wp:cover {"useFeaturedImage":true,"isDark":false,"style":{"dimensions":{"aspectRatio":"3/4"},"border":{"radius":"10px"}}} -->
    <div class="wp-block-cover is-light" style="border-radius:10px"><span aria-hidden="true" class="wp-block-cover__background has-background-dim-0 has-background-dim"></span><div class="wp-block-cover__inner-container"></div></div>
    <!-- /wp:cover -->
    ```

    **Path C (placeholder surface only — no featured image semantic):** use `core/group` with `color.background` literal + `aspect-ratio` proxy via padding-top. Drop `core/cover` entirely. Reserved for purely decorative thumbnail squares (HC#40).

    **Pre-emit greppable check (Tier A blocking):**

    ```
    grep -nE "wp:cover[^/]*\"useFeaturedImage\":true[^/]*\"color\":\{[^}]*\"background\"" <output.html>
    ```

    Any match = anti-pattern. Strip `color.background` from the JSON AND remove `has-background;background-color:#hex` from the wrapper class + inline style.

    **Margin parity reminder (HC#26 cross-reference):** for ANY core/cover with `style.spacing.margin.{top|right|bottom|left}` in JSON, the wrapper inline `style=""` MUST include matching `margin-{side}:Xpx` rules. set-equality is set-equality.

    Surfaced: Aurora Pro Wireless Headphones paste-test (2026-06-02) — related-products card cover cascade triggered block recovery across all 4 cards. Fixed by removing `color.background` from the cover JSON.

59. **`surecart/product-template` columns attr is `layout.columnCount`, NOT `columns` (v7.23.0, surfaced 2026-06-04 T1 Aurora Pro Headphones paste-test).** When emitting the per-card grid for `surecart/product-list-related` or shop-page `surecart/product-list`, the columns count attribute is `layout.columnCount` — not `columns`, not `cols`, not `column_count`. The server's `controller.php` (`packages/blocks-next/src/blocks/product-template/controller.php:4`) reads `$attributes['layout']['columnCount']` and emits the wrapper class `sc-product-template-columns-N`.

    **Anti-pattern (drift):**
    ```html
    <!-- wp:surecart/product-template {"columns":4} -->
    ```
    → Renders default 3-col grid; `columns:4` is silently ignored.

    **Canonical:**
    ```html
    <!-- wp:surecart/product-template {"layout":{"type":"grid","columnCount":4}} -->
    ```
    → Renders `<ul class="wp-block-surecart-product-template ... sc-product-template-columns-4">`, 4-col on desktop.

    **Mobile auto-collapse** (from `style.scss`):
    - At `480-768px` viewport, columns 4+ auto-collapse to 3-col.
    - At `<480px`, all collapse to 1-col.
    - You can emit `columnCount:4/5/6` safely; mobile rendering is handled.

    **Greppable check:**
    ```
    grep -nE "wp:surecart/product-template[^/]*\"columns\":" <output.html>
    ```
    Any match = wrong attr name; rewrite to `"layout":{"type":"grid","columnCount":N}`.

    Surfaced: T1 Aurora Pro Headphones (2026-06-04) — emitted `columns:4` initially, rendered as 3-col; fixed via `layout.columnCount:4`.

60. **`surecart/product-variant-pills` server-iterates ALL configured variant axes and emits its OWN axis labels — do NOT hand-emit a label paragraph above the block (v7.23.0, surfaced 2026-06-04 T1 Aurora Pro Headphones paste-test).** Per HC#46 the block is emitted ONCE; this HC adds: the server-rendered output ALSO includes an automatic axis label per axis ("Color", "Size", "Bundle", etc.) derived from the product's variant configuration.

    **Anti-pattern (duplicate + mis-positioned):**
    ```html
    <!-- wp:paragraph {"style":{...}} -->
    <p class="...">Color</p>
    <!-- /wp:paragraph -->
    <!-- wp:surecart/product-variant-pills -->
    <!-- wp:surecart/product-variant-pill {...} /-->
    <!-- /wp:surecart/product-variant-pills -->
    ```
    Server iterates and emits TWO pill groups (color + size), each with its OWN auto-label. The hand-emitted "Color" paragraph sits above the FIRST pill group — which may be "Size" (or whichever axis the server enumerates first) → label/value mismatch.

    **Canonical:**
    ```html
    <!-- wp:surecart/product-variant-pills -->
    <!-- wp:surecart/product-variant-pill {...} /-->
    <!-- /wp:surecart/product-variant-pills -->
    ```
    Server emits both axes with their own per-axis labels. No hand-emitted paragraph above.

    **When the design has visible axis labels like "Color · Midnight":** trust the server. The design's hand-painted label is what the server ALSO renders. Do not duplicate.

    **Greppable check:**
    ```
    grep -nE -B 1 "wp:surecart/product-variant-pills" <output.html> | grep "wp:paragraph"
    ```
    Any sibling paragraph immediately preceding `wp:surecart/product-variant-pills` is a probable duplicate-label violation. Verify against design intent — keep only if it's a meta-label (e.g., "Choose your size:") not the axis name itself.

61. **`surecart/product-buy-buttons` wrapper `<div>` is mandatory ALWAYS — HC#28 expansion (v7.23.0, surfaced 2026-06-04 T1 Aurora Pro Headphones paste-test).** HC#28 documents margin-parity for `surecart/product-buy-buttons` (when margin attrs set, inline mirror required). This HC extends: the wrapper `<div class="wp-block-surecart-product-buy-buttons wp-block-buttons sc-block-buttons is-layout-flex">` is required **even when NO margin/spacing attrs are set**. Self-closing form `<!-- wp:surecart/product-buy-buttons -->\n<!-- wp:surecart/product-buy-button .../-->\n<!-- /wp:surecart/product-buy-buttons -->` (no wrapper div) triggers `Block validation failed for surecart/product-buy-buttons`.

    **Canonical (always — no attrs):**
    ```html
    <!-- wp:surecart/product-buy-buttons -->
    <div class="wp-block-surecart-product-buy-buttons wp-block-buttons sc-block-buttons is-layout-flex">
    <!-- wp:surecart/product-buy-button {"text":"Add to Cart","add_to_cart":true} /-->
    </div>
    <!-- /wp:surecart/product-buy-buttons -->
    ```

    **Canonical (with margin per HC#28):**
    ```html
    <!-- wp:surecart/product-buy-buttons {"style":{"spacing":{"margin":{"top":"8px","bottom":"20px"}}}} -->
    <div class="wp-block-surecart-product-buy-buttons wp-block-buttons sc-block-buttons is-layout-flex" style="margin-top:8px;margin-bottom:20px">
    <!-- wp:surecart/product-buy-button {...} /-->
    </div>
    <!-- /wp:surecart/product-buy-buttons -->
    ```

    The wrapper class set (`wp-block-surecart-product-buy-buttons wp-block-buttons sc-block-buttons is-layout-flex`) is server-determined and constant. The wrapper div is ALWAYS required.

    **Greppable check:**
    ```
    grep -nzE "wp:surecart/product-buy-buttons[^>]*-->\s*\n\s*<!-- wp:surecart/product-buy-button" <output.html>
    ```
    Any match = self-closing-style violation; the wrapper div is missing.

    Surfaced: T1 Aurora Pro Headphones (2026-06-04) — first paste failed with the self-closing form on the qty+addtocart inline group; fixed by always including the wrapper div.

62. **`aria-label` HTML attribute on `core/button` `<a>` triggers validation failure when there's no backing JSON attr (v7.23.0, surfaced 2026-06-04 T2 Meridian Overcoat paste-test).** When hand-writing icon-only buttons (e.g., a wishlist heart "♡"), the natural-looking pattern is:
    ```html
    <a class="..." aria-label="Save to wishlist">♡</a>
    ```
    But `core/button` save() does NOT emit `aria-label` — the block.json doesn't declare an `ariaLabel` attribute. Hand-writing the attribute creates a stored/generated mismatch on every save round-trip.

    **Two valid alternatives:**
    1. **Drop the `aria-label`** entirely (lose decorative semantics — accept that the heart "♡" is the only screen-reader cue, which is poor accessibility but valid markup).
    2. **Use `core/icon` instead** (the right pattern for icon-only buttons). Example:
       ```html
       <!-- wp:icon {"icon":"core/heart","style":{"dimensions":{"width":"24px"}}} /-->
       ```
       Icons have their own ariaLabel attr that DOES backing-emit.

    **Use case routing:**
    - Decorative icon WITH affordance (clickable wishlist toggle, search trigger) → `core/icon` block (preferred — accessible + emits proper aria).
    - Decorative inline glyph (icon as text decoration) → emit as Unicode character inside `core/paragraph`, accept no aria-label.
    - NEVER hand-write `aria-label` / `role` / `aria-*` / `data-*` HTML attrs on `core/button` `<a>` — none of them are backed by save().

    **Greppable check:**
    ```
    grep -nE 'wp-block-button__link[^>]*\s(aria-|role=|data-)' <output.html>
    ```
    Any match = unsupported HTML attr violation.

    Surfaced: T2 Meridian Overcoat (2026-06-04) — wishlist heart with `aria-label="Save to wishlist"` triggered Block Recovery; fix was to drop the attr (or per-HC option, switch to `core/icon`).

63. **`core/cover` `style.dimensions.minHeight` does NOT inline-mirror — use top-level `minHeight`/`minHeightUnit` attrs instead (v7.23.0, surfaced 2026-06-04 T3 Hartwell Linen Sofa paste-test). HC#25 EXTENSION.** Same family as `style.dimensions.aspectRatio` (HC#25). When you want a `core/cover` with a literal pixel min-height (e.g., 640px lifestyle hero), `style.dimensions.minHeight:"640px"` does NOT inline-mirror to `min-height:640px`. Save() generates the inline style WITHOUT min-height; a hand-written wrapper with the inline mirror creates drift.

    **Wrong:**
    ```html
    <!-- wp:cover {"style":{"dimensions":{"minHeight":"640px"},...}} -->
    <div class="wp-block-cover" style="...;min-height:640px"><span ...></span><div ...></div></div>
    ```
    → Validation: "Expected style without min-height, saw style with min-height:640px"

    **Right (top-level attrs DO inline-mirror):**
    ```html
    <!-- wp:cover {"minHeight":640,"minHeightUnit":"px",...} -->
    <div class="wp-block-cover" style="...;min-height:640px"><span ...></span><div ...></div></div>
    ```

    **JSON path summary table for `core/cover` dimension attrs (unified with HC#25):**

    | JSON path | Inline-mirrors? | Notes |
    |---|---|---|
    | top-level `minHeight:N` + `minHeightUnit:"px"` | ✅ YES — `min-height:Npx` | Recommended for literal-px cover heights |
    | `style.dimensions.minHeight:"640px"` | ❌ NO | Drift trigger — never use |
    | top-level `aspectRatio:"4/3"` | ✅ YES — `aspect-ratio:4/3` | For aspect-ratio'd hero covers (HC#25) |
    | `style.dimensions.aspectRatio:"4/3"` | ❌ NO | Routed via CSS class for featured-image variants (HC#25) |

    **Greppable check:**
    ```
    grep -nE 'wp:cover[^/]*"style":\{[^}]*"dimensions":\{[^}]*"minHeight"' <output.html>
    ```
    Any match = wrong path; rewrite to top-level `minHeight`.

    Surfaced: T3 Hartwell Linen Sofa (2026-06-04) — room-hero cover with `style.dimensions.minHeight:"640px"` triggered Block Recovery; fix was to switch to top-level `minHeight:640,minHeightUnit:"px"`.

64. **`core/button` with `"width":N` attribute requires wrapper class `has-custom-width wp-block-button__width-N`, NOT inline `style="width:N%"` (v7.23.0, surfaced 2026-06-04 T5 Aurore Timepiece paste-test).** The `core/button` block declares a `width` attribute (valid values: `25`, `50`, `75`, `100`) for fractional-width buttons. Save() emits the class set `wp-block-button has-custom-width wp-block-button__width-{N}` on the wrapper `<div>` — and does NOT emit any inline `style="width:..."` mirror. Hand-writing `style="width:100%"` triggers validation failure.

    **Anti-pattern (drift):**
    ```html
    <!-- wp:button {"width":100,...} -->
    <div class="wp-block-button" style="width:100%">
    <a class="wp-block-button__link ..." style="...">Book a Private Salon Viewing</a>
    </div>
    <!-- /wp:button -->
    ```
    → Validation: "Expected class `has-custom-width wp-block-button__width-100`, saw `wp-block-button` only"

    **Canonical:**
    ```html
    <!-- wp:button {"width":100,...} -->
    <div class="wp-block-button has-custom-width wp-block-button__width-100">
    <a class="wp-block-button__link ..." style="...">Book a Private Salon Viewing</a>
    </div>
    <!-- /wp:button -->
    ```
    The wrapper `<div>` class adds `has-custom-width wp-block-button__width-100`; NO inline `style="width:..."` on the wrapper. CSS associated with `wp-block-button__width-100` handles the actual width:100% sizing.

    **Width value table:**
    | `width:N` attr | Wrapper class added | CSS effect |
    |---|---|---|
    | 25 | `has-custom-width wp-block-button__width-25` | 25% width |
    | 50 | `has-custom-width wp-block-button__width-50` | 50% width |
    | 75 | `has-custom-width wp-block-button__width-75` | 75% width |
    | 100 | `has-custom-width wp-block-button__width-100` | 100% (full-width) |

    Any other value (33, 60, etc.) is NOT supported — the block.json enum restricts to those 4. To achieve other fractional widths, wrap the button group in a flex `core/group` with `style.layout.flexSize:"Npx"`.

    **Greppable check:**
    ```
    grep -nE '<div class="wp-block-button"[^>]+style="[^"]*width' <output.html>
    ```
    Any match = wrong path; rewrite to use the class.

    Surfaced: T5 Aurore Timepiece (2026-06-04) — full-width "Book a Private Salon Viewing" button emitted with `style="width:100%"` triggered Block Recovery; fix was to use `has-custom-width wp-block-button__width-100` class.

65. **`surecart-mono` slug does NOT resolve to a monospace font in the default theme.json — emit literal mono stack alongside per HC#35 dual-emit (v7.23.0, surfaced 2026-06-04 T1 Aurora Pro Headphones paste-test).** The `theme-partial.json` registers `surecart-mono` as a font-family slug, but the underlying value falls back to the body sans-serif stack (`-apple-system, system-ui, ...`) — NOT a real mono face. Slug-only emission for mono UI text (eyebrow / breadcrumbs / spec labels / mono captions) renders as sans-serif on the frontend, defeating the design intent.

    **Anti-pattern (renders as sans):**
    ```html
    <!-- wp:paragraph {"fontFamily":"surecart-mono",...} -->
    <p class="has-surecart-mono-font-family">Breadcrumbs · text · here</p>
    <!-- /wp:paragraph -->
    ```
    → Theme's `surecart-mono` slug resolves to `-apple-system, system-ui...` → renders as sans-serif.

    **Canonical (per HC#35 dual-emit OR literal-only per HC#41):**

    **Option A — Literal-only (recommended for monospace UI text):**
    ```html
    <!-- wp:paragraph {"style":{"typography":{"fontFamily":"ui-monospace, monospace",...},...}} -->
    <p style="...;font-family:ui-monospace, monospace;...">Breadcrumbs · text · here</p>
    <!-- /wp:paragraph -->
    ```
    Drop the slug; emit a short literal stack (`ui-monospace, monospace` = 23 chars, fits HC#16 30-char target).

    **Option B — HC#35 slug + literal dual-emit:**
    ```html
    <!-- wp:paragraph {"fontFamily":"surecart-mono","style":{"typography":{"fontFamily":"ui-monospace, monospace",...},...}} -->
    <p class="has-surecart-mono-font-family" style="...;font-family:ui-monospace, monospace;...">Breadcrumbs · text · here</p>
    <!-- /wp:paragraph -->
    ```
    Per HC#41, do NOT mix paths for mono UI text — pick ONE. For mono, Option A is cleaner (the slug provides no upside since the theme resolves it to sans anyway).

    **When this rule applies:**
    - Breadcrumbs (mono "/" separators with letter-spacing)
    - Eyebrow labels (uppercase mono e.g. "REFERENCE SL-127.AU")
    - Spec table labels (uppercase mono "POWER RESERVE")
    - Reference numbers / SKU lines

    **When `surecart-display` and `surecart-body` slugs DO work:**
    - `surecart-body` resolves to the active theme's body face (typically sans like DM Sans / Inter) — fine for body copy
    - `surecart-display` MAY resolve to a serif if the theme is editorial — but at the time of this HC (2026-06-04), the default theme's `surecart-display` resolves to body sans too. **For SPECIFIC named typefaces** (Instrument Serif, Lora, Fraunces, etc.) — always use literal `style.typography.fontFamily` per HC#41 + HC#35 Option A.

    **Greppable check:**
    Look for slug-only mono emissions:
    ```
    grep -nE '"fontFamily":"surecart-mono"' <output.html> | grep -v 'font-family:'
    ```
    Any match where the JSON has the slug but the wrapper inline-style is missing a literal `font-family:` mirror = mono renders as sans on frontend.

    Surfaced: T1 Aurora Pro Headphones (2026-06-04) — eyebrow + breadcrumbs + spec labels used `fontFamily:"surecart-mono"` slug-only; on frontend they rendered in the body sans-serif (`-apple-system`), losing the mono design intent. Resolution: T2-T5 emitted with literal `ui-monospace, monospace` only and got correct mono rendering.

66. **Pre-emit grep sweep for descriptive HTML comments is MANDATORY (v7.23.0 enforcement reinforcement — HC#45 was massively violated despite documentation).** HC#45 documents the rule: "NO descriptive HTML comments inside block content areas — only block delimiters." But during the T1-T5 paste-test campaign (2026-06-04), every single template was emitted with 5-35 stray descriptive comments (`<!-- Store Nav -->`, `<!-- Feature 1 -->`, `<!-- Benefits 4-col -->`, etc.) — 70+ total across all 5. Each triggered cascading block-validation failures (12 cascading invalid blocks on T1 alone).

    **The rule isn't violated because LLMs ignore HC#45 — it's violated because the rule lives in PROSE-only enforcement.** The LLM "knows" the rule but applies it inconsistently because the natural composition workflow uses comments as scaffolding ("let me put a comment to mark Section Boundary"). Promoting from documented-only → MANDATORY pre-emit grep step.

    **Pre-emit grep step (required before paste-test OR file-write):**

    ```bash
    python3 -c "
    import re, sys
    src = open(sys.argv[1]).read()
    matches = re.findall(r'<!--(?!\s*/?wp:)[^>]*?-->', src, re.DOTALL)
    print(f'Non-block comments: {len(matches)}')
    if matches:
        for m in matches[:5]:
            print('  ', repr(m[:80]))
        # Strip and rewrite
        src2 = re.sub(r'<!--(?!\s*/?wp:)[^>]*?-->', '', src, flags=re.DOTALL)
        src2 = re.sub(r'\n\s*\n\s*\n+', '\n\n', src2)
        open(sys.argv[1], 'w').write(src2)
        print(f'Stripped → size: {len(src2)}')
    " <output.html>
    ```

    If `Non-block comments: 0` — good, proceed to paste-test.
    If `> 0` — strip them (the script does it inline). Verify the strip didn't break anything by re-running the grep — should report 0 now.

    **Why this MUST run before paste:** the difference between catching 35 comments in `O(1)` grep vs cascading 12 invalid blocks in the editor (each requiring round-tripping diagnostic JS) is ~30 minutes per template. The grep is 100ms.

    **Composition tip:** if you find yourself wanting to write `<!-- Section X -->` as a section boundary while composing, instead use a CODE COMMENT in your scratch notes (not in the emitted markup), OR rely on the block-tree indentation to communicate structure. Each `<!-- wp:group ... -->` opener already names its section semantically via the JSON attrs; descriptive labels above them are redundant.

    Surfaced: T1-T5 paste-test campaign (2026-06-04) — 70+ stray comments across 5 templates. Grep sweep added to workflow; T2-T5 ran the grep before paste and either had 0 matches OR caught + stripped 5-7 stray comments each before failure. T1 (first template) didn't run the grep and suffered 12 cascading recovery prompts.

67. **PIXEL-PERFECT: Body-text font-family slug WITHOUT dual-emit literal renders as theme default sans (extends HC#65 to ALL design typefaces, not just mono) (v7.24.0, surfaced 2026-06-04 T1-T5 pixel-perfect campaign).** HC#65 documented this for `surecart-mono` specifically. T1-T5 pixel-perfect comparison revealed the rule applies to **every** design typeface — `DM Sans`, `Lora`, `Instrument Serif`, `Fraunces`, `JetBrains Mono`, etc. Slug-only emission (`fontFamily:"surecart-body"`) falls through to the theme's body font (typically `-apple-system, system-ui, ...` sans).

    **Universal rule for pixel-perfect typography:** EVERY block whose visual design specifies a non-default typeface MUST emit a LITERAL `style.typography.fontFamily` value (CSS-quoted multi-word names) AND mirror it in the wrapper inline `style`.

    **Canonical emission pattern (matched 5-template paste-test, 2026-06-04):**

    ```html
    <!-- wp:heading {"level":2,"style":{"typography":{"fontSize":"56px","fontWeight":"600","lineHeight":"1.0","letterSpacing":"-0.03em","fontFamily":"'DM Sans', sans-serif"},"color":{"text":"#0a0a0a"}}} -->
    <h2 class="wp-block-heading has-text-color" style="color:#0a0a0a;font-size:56px;font-weight:600;letter-spacing:-0.03em;line-height:1.0;font-family:'DM Sans', sans-serif">Built for the music you actually listen to.</h2>
    <!-- /wp:heading -->
    ```

    Note the **single-quoting** around multi-word names (HC#68 — see below).

    **The 5-template font-family map verified working:**

    | Template | Headings | Body | Mono accents |
    |---|---|---|---|
    | T1 Electronics (Aurora Pro) | `'DM Sans', sans-serif` 600wt | `'DM Sans', sans-serif` 400wt | `ui-monospace, monospace` |
    | T2 Fashion (Meridian Overcoat) | `'Instrument Serif', serif` 400wt italic | `'DM Sans', sans-serif` | `ui-monospace, monospace` |
    | T3 Home (Hartwell Linen Sofa) | `'Lora', serif` 500wt | `'DM Sans', sans-serif` | `ui-monospace, monospace` |
    | T4 Wellness (Daily Vitality) | `'DM Sans', sans-serif` 700wt | `'DM Sans', sans-serif` 400wt | `ui-monospace, monospace` |
    | T5 Luxury (Aurore Timepiece) | `'Instrument Serif', serif` 400wt | `'DM Sans', sans-serif` | `ui-monospace, monospace` |

    **Detection signal:** when the design's CSS declares `:root { --sans: "DM Sans", ...; --serif: "Instrument Serif", ...; --mono: ui-monospace, ... }` or similar, extract those exact stacks and use them as literals on every text-bearing block.

    **Per HC#41 — do NOT mix slug + literal.** Pick literal-only for pixel-perfect work (skips theme resolution entirely; design renders correctly even on themes that don't register the slug).

    **Greppable check:**
    ```
    grep -nE "fontFamily\":\"surecart-(body|display|mono)\"" <output.html> | grep -v "font-family:"
    ```
    Any match where slug is set without inline literal mirror = pixel-perfect violation; rewrite to literal-only path.

    Surfaced: T1-T5 pixel-perfect campaign (2026-06-04) — all 5 templates' body text initially rendered as `-apple-system` despite slugs being emitted. Switching to literal `'DM Sans', sans-serif` (and other faces) fixed rendering on first paste.

68. **PIXEL-PERFECT: Multi-word font-family names in inline `style` MUST use SINGLE quotes (not double) — HTML attribute conflict (v7.24.0, surfaced 2026-06-04 T1 pixel-perfect first attempt).** The natural CSS quoting for multi-word font names is `font-family:"DM Sans", sans-serif`. Embedded in an HTML `style="..."` attribute, the inner `"` breaks parsing: `<h2 style="...;font-family:"DM Sans", sans-serif">` → HTML parser sees `style="...;font-family:"` and `DM Sans"` as a stray attribute → save() generates `font-family:` (EMPTY value) → mismatch.

    **Wrong:**
    ```html
    style="font-size:56px;font-family:"DM Sans", sans-serif"
    ```
    HTML parser truncates style at the first inner `"`.

    **Right (single-quoted CSS string):**
    ```html
    style="font-size:56px;font-family:'DM Sans', sans-serif"
    ```
    CSS accepts both `"` and `'` for font-family string literals (W3C CSS Fonts level 4 §2.3). Use `'` inside HTML `"`-delimited style attrs.

    **JSON form (Gutenberg block attr):** the JSON value itself can use either quote form. For consistency with the inline mirror, use single-quoted multi-word:

    ```json
    "fontFamily":"'DM Sans', sans-serif"
    ```

    The JSON string value is then `'DM Sans', sans-serif` (with literal single-quotes). save() emits this verbatim into the inline `style="...;font-family:'DM Sans', sans-serif"`.

    **Generic alternative (no quotes needed):** if you use a single-word font name OR a generic family only, quotes aren't required. Example: `font-family:system-ui, sans-serif` works as-is. But for design-specified faces (DM Sans, Instrument Serif, etc.), single-quote always.

    **Greppable check (pre-emit Tier A):**
    ```
    grep -nE 'style="[^"]*"[A-Z][a-z]+ [A-Z][a-z]+"' <output.html>
    ```
    Any match = unescaped double-quotes broke the style attr. Rewrite to single-quotes.

    Surfaced: T1 pixel-perfect first attempt (2026-06-04) — naive `font-family:"DM Sans", sans-serif` broke 12 headings because HTML parser truncated the inline-style at the inner `"`. Switching to `font-family:'DM Sans', sans-serif` (single quotes) restored set-equality.

69. **PIXEL-PERFECT: Visual-design `min-height` for hero / showcase covers MUST emit as top-level `minHeight`+`minHeightUnit` attrs (HC#63 cross-ref) (v7.24.0, surfaced 2026-06-04 T1 + T5 pixel-perfect comparison).** Multiple T1-T5 templates have full-bleed dark hero or split showcase covers with design `min-height: 560px` (T1 showcase), `min-height: 640px` (T3 room hero), `min-height: 720px` (T2 hero + T5 hero). Without `minHeight` attr, the cover collapses to inner-content height (typically 60-70% of intended height) — visually cramped vs design.

    **Required emission for ANY `core/cover` with visual min-height in the design:**

    ```html
    <!-- wp:cover {"customOverlayColor":"#0a0a0a","dimRatio":100,"isUserOverlayColor":true,"minHeight":560,"minHeightUnit":"px",...} -->
    <div class="wp-block-cover" style="...;min-height:560px">...
    ```

    Both `minHeight:560` (integer) and `minHeightUnit:"px"` MUST be set (per HC#63 — `style.dimensions.minHeight` does NOT inline-mirror).

    **Cover min-heights observed in T1-T5 (use as reference for your inputs):**

    | Use case | minHeight | minHeightUnit |
    |---|---|---|
    | Showcase split (dark-bg side image + copy) | 560 | px |
    | Room lifestyle hero (large background scene) | 640 | px |
    | Editorial / fashion hero (large image) | 720 | px |
    | Luxury full-bleed hero (dramatic typography) | 720 | px |

    **Detection signal:** when the design's section CSS has `min-height: <N>px` OR the section visually occupies >50% of the 800px viewport (large-band sections), emit the corresponding `minHeight` on the cover.

    Surfaced: T1 + T5 pixel-perfect comparison (2026-06-04) — T1 showcase collapsed from 560px design intent to 480px on FE; T5 hero rendered without 720px design intent. Added `minHeight:N, minHeightUnit:"px"` to fix both.

---

## Iteration (when the merchant comes back with feedback)

If the merchant says "the highlights grid is wrong" or "fix the FAQ section":

- **Surgical, not regenerative.** Emit a fresh fenced block containing JUST the broken section (e.g., one `core/columns` for the highlights), not the entire page.
- Tell the merchant: *"Find the `core/columns` containing the highlights and paste this in its place."*
- If they attached a screenshot, use it to guide the fix — but don't re-emit the whole pattern unless they explicitly ask.
- Re-run self-validation on the section.

---

## When the design has elements with no SureCart block (v7.1 fallback ladder)

Some designs include things SureCart doesn't have a block for (e.g., trust-badge rows, custom video players, animated counters, decorative ribbons, custom toggles). The decision precedence:

1. **Try a WP-core primitive first** — `core/image` for a trust badge, `core/video` / `core/embed` for video, `core/details` for a collapsible toggle, `core/group`+`core/columns` for any flex/grid layout.
2. **Try a SureCart block** — search `reference/surecart-blocks.md` and `reference/full-inventory.json` for a block that matches the semantics (e.g., `surecart/icon` for SureCart-library icons, `surecart/sticky-purchase` for sticky bottom bars).
3. **Open `reference/custom-html-fallback.md`** and decide between the 3 tiers:
   - **L1 — static `core/html`** — decorative content, no behavior. Log `dropped_features.type:"raw_html_static"`.
   - **L2 — `core/html` piggyback on a SureCart Interactivity store** — interactive content where the behavior maps to an action SureCart already exposes (cart toggle, lightbox open, gallery navigation, quantity increment, variant select). Use ONLY the 7 namespaces in the allowlist; verify a sibling SureCart block on this same emit triggers the namespace's module load. Log `dropped_features.type:"raw_html_interactive", level:"L2"` with `namespace` + `dependency_block` fields.
   - **L3 — drop + recommend custom block** — interactive content that doesn't map to any allowlist namespace. Emit best-effort static visual fallback (so the page isn't empty), log `dropped_features.type:"raw_html_interactive", level:"L3"` with `merchant_action` recommending `/surecart-new-block` (or `/surecart-new-integration` for a third-party API).

**Never invent a SureCart block name. Never invent a `data-wp-interactive` namespace.** Both fail silently — invented block names trigger paste recovery; invented namespaces produce inert directives the runtime never hydrates.

---

## Quick reference (always-true facts)

- **`surecart/product-page` is the only block that provides product context.** Every `surecart/product-*` block must be inside it.
- **SureCart blocks are `apiVersion: 3` server-rendered** — they MAY self-close. Core blocks are NOT — paired ones MUST be paired with a wrapper div.
- **`fontWeight` and `lineHeight` are stored as strings** in Gutenberg attrs (`"fontWeight":"700"`, not `700`).
- **`gap` on a flex/grid container** becomes the parent block's `style.spacing.blockGap`, not on each child.
- **Token slugs** in `theme-partial.json`: colors are `surecart-brand`, `surecart-bg-dark`, etc. Spacing is `surecart-1` through `surecart-24`. Fonts are `surecart-display`, `surecart-body`, `surecart-mono`.
