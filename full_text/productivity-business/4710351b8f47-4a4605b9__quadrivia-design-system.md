---
name: quadrivia-design-system
description: >
  Quadrivia's design system and brand reference for its product "Q". Use for ANY
  product-facing UI or frontend work on a Quadrivia or Q surface — even when the
  user never says "design system", "brand", or "tokens". Trigger when someone
  builds, styles, reviews, or refactors product UI (buttons, cards, modals,
  forms, inputs, selects, toggles, tables, filters, nav, dashboards, charts,
  badges, toasts, empty states, landing sections, product emails); decides color
  (the Primary Four: purple/teal/yellow/pink), Poppins type, spacing, rounded
  radii, gradients, shadows, motion, Phosphor icons, or Q logo usage; or writes
  CSS, React, Tailwind, or shadcn/ui for a Q screen. Also for product copy and UI
  microcopy in Q's voice. Do NOT trigger for non-UI work that only mentions
  Quadrivia (backend/API, SQL or DB migrations, data analysis, CI/deploy), nor
  for business/investor comms, the historical "quadrivium", or another product's
  system like Cercle. If the work is visual or brand-facing for Q, this skill
  must be active.
metadata:
  author: David Vegas Garcia
  version: "2.11"
---

# Quadrivia Design System

> Authored and maintained by **David Vegas Garcia** · v2.11 · 2026

The design system for **Q**, the product, by **Quadrivia**, the company. The aesthetic is **bold, bright, and generous**: four co-equal brand colors carrying equal weight, fully rounded geometry with no hard right angles, a single confident typeface (Poppins), gradients as a signature device, and a lot of breathing room.

**Single source of truth:** `tokens/quadrivia.tokens.json`. It generates two consumable artifacts:

- `tokens/tokens.css` — CSS custom properties + `.t-*` typography utilities
- `tokens/tailwind.preset.js` — a Tailwind preset (`presets: [require('./tokens/tailwind.preset.js')]`)

Regenerate after any token change: `node scripts/build-tokens.mjs` (or `python3 scripts/build_tokens.py` if you don't have Node). **Never hand-edit the generated files.**

A live visual reference is `showcase.html`. Open it in a browser to see every token and component rendered.

> **About this document's own formatting:** it is a developer reference, so it uses ordinary Markdown lists and emphasis for legibility. Those are documentation conventions. The brand rules below (no bullets, no em dashes, never italics, etc.) govern **product and brand surfaces**, not this developer reference.

---

## What Q is (so the UI matches the story)

Q is a **Clinical Process Outsourcing partner** — a managed service combining AI execution with human clinician oversight to run entire patient journeys end to end. Q is **not** a chatbot, an EHR bolt-on, a point solution, or a task handler. The UI should feel like an owned, end-to-end **partner**: confident, calm, structured, never busy or gimmicky. Full voice and naming rules live in [references/voice-and-content.md](references/voice-and-content.md) — read it before writing any product copy or microcopy.

---

## Common mistakes (read first)

The shortcuts that most often break the Quadrivia look. Avoid these before reaching for any token.

1. **Don't let one brand color dominate by default.** Purple, Teal, Yellow, and Pink carry **equal** weight in data and expressive use. When a single dominant is unavoidable, default to **Teal `#22C7C6`** (the brand default-dominant). This is separate from the **primary action button**, which is **Purple** (see Interactive) — purple is reserved for that one role so CTAs stand out.
2. **Don't ship hard right angles.** Cards, containers, and image frames use **30px** radius (`--radius-card`); labels, pills, badges, and buttons are **fully rounded** (`--radius-pill`). Sharp 0px corners are off-brand.
3. **Don't use italics. Ever.** Emphasize with **weight** (SemiBold/Bold), never slant. This is a hard brand rule.
4. **Don't introduce a second typeface.** Poppins at every level. (Mono `JetBrains Mono` is a sanctioned UI extension for code and tabular numerals only — never for prose.)
5. **Don't use bullets, dashes, or numbered lists in product/marketing UI.** Separate list items with a 2px gradient rule (`.q-separator`) that cycles the Primary Four. See [Signature layout devices](#signature-layout-devices).
6. **Don't recolor, gray out, or add effects to the Q logo.** The Q mark is **full-color only** — color *is* the logo. See [Brand & logo](#brand--logo).
7. **Don't introduce colors outside the documented system.** The Primary Four + extended brand + the sanctioned UI extensions (neutrals, semantics, charts) are the whole palette. No stray `#eee`, no random hexes.
8. **Don't invent off-grid values.** Snap to the 4px spacing grid, the radius scale, and the type scale. No 13px padding, no 7px radius, no 17px gaps.
9. **Don't write "the Q".** Q is always capitalized and standalone. **Quadrivia** is the company; **Q** is the product.
10. **Match density to the surface.** **Brand / marketing surfaces stay generous** — breathing room is deliberate; when unsure, choose the larger step. **Data-heavy product surfaces** (queues, tables, dashboards, dense forms) switch on **compact density** (`data-density="compact"`) so information isn't crowded out. Don't make a dashboard as airy as a landing page — or a landing page as tight as a table. See [Density](#density--ui-extension).

---

## Brand & logo

The brand mark is the **Q icon**, always shown with **"Powered by Quadrivia"** locked beneath it.

### Hard rules (from the brand guide)

- The Q mark is **always displayed in full color.** No black, white, grayscale, or single-color versions exist or are approved. **Color is not a stylistic choice — it is the logo.** Design *around* it; never adapt it to the background.
- **"Powered by Quadrivia" always appears small, directly beneath the full-color icon.** This is the only approved text pairing. The lockup is a fixed asset — never retype, reposition, or rescale the icon-to-line relationship independently.
- **Never** recolor the icon, place it on a background that would require a color adaptation, separate the "Powered by Quadrivia" line from the icon, recreate the lockup in any other typeface or weight, or stretch / rotate / apply effects of any kind.

### Putting it on colored or busy surfaces

Because the mark must stay full-color on every background, **do not recolor it to fit** — instead place it on a clean containment surface: a white (or `--color-surface-page`) tile with **`--radius-card` (30px)** corners and padding equal to the mark's clear space. This keeps the mark untouched while it sits on color or imagery.

### Sizing & clear space

- **Minimum height:** the full lockup is a **square, stacked mark-over-wordmark**, so it needs roughly **56px** of height for "Powered by Quadrivia" to stay legible. For smaller spots, use an icon-only export (the mark without the wordmark) down to `--logo-min-height` (32px). Never shrink the combined lockup until the text is unreadable.
- **Clear space** on all four sides equals the height of the wordmark line. Nothing intrudes into that frame.
- The asset is square (200×200, transparent). Set one dimension and let the other match — never distort it.

### Assets

The official full-color mark lives in `assets/logo/` and **doubles as both the icon and the lockup** — the gradient circle with the human figure, over "Powered by Quadrivia". See [assets/logo/README.md](assets/logo/README.md).

```
assets/logo/
  q-lockup.webp         full-color mark + wordmark · 200×200, transparent  ← default
  q-lockup.png          raster fallback (email, legacy contexts)
```

```html
<!-- Default in product UI -->
<img src="/assets/logo/q-lockup.webp" alt="Q — Powered by Quadrivia"
     width="120" height="120" />
```

Always include descriptive `alt` text. The wordmark is the only black element, so on dark or busy surfaces place the lockup on a white `--radius-card` tile rather than recoloring it. An SVG and an icon-only (no-wordmark) export are still worth adding for crisp scaling and tiny placements — request them if needed.

---

## Colors

Reach for colors through the token names. CSS: `var(--color-brand-teal)`. Tailwind: `bg-brand-teal`, `text-ink`, `border-line`, `bg-success-subtle`, etc.

### Brand — the Primary Four (co-equal)

| Token | Hex | CSS var | Tailwind |
|-------|-----|---------|----------|
| Purple | `#5349FF` | `--color-brand-purple` | `brand-purple` |
| Teal | `#22C7C6` | `--color-brand-teal` | `brand-teal` |
| Yellow | `#FFCB00` | `--color-brand-yellow` | `brand-yellow` |
| Pink | `#F72485` | `--color-brand-pink` | `brand-pink` |

These four are **equal in rank** and used interchangeably. **Default dominant** when balance is impossible: **Teal**, which reads cleanest on both light and dark backgrounds. Never give a single color consistent dominance across a product.

### Brand — extended

Use **only** when a genuine fifth or sixth color is required. Never a substitute for the Primary Four.

| Token | Hex | Tailwind |
|-------|-----|----------|
| Soft Coral | `#F2636C` | `soft-coral` |
| Light Blue | `#3ED6FE` | `light-blue` |
| Black | `#000000` | `black` |
| White | `#FFFFFF` | `white` |

**Black** is for body text and structural anchoring only. **White** is always the primary background.

### Neutrals · *UI extension*

A cool-cast gray ramp for borders, surfaces, and text hierarchy — necessary for real product depth, kept tinted toward the brand's cool side so it never reads "default gray". `--color-neutral-0` (`#FFFFFF`) → `50 #F7F8FA` → `100 #EFF1F5` → `200 #E2E5EB` → `300 #CBD0D9` → `400 #A7AEBC` → `500 #7E8696` → `600 #5A6172` → `700 #3E4453` → `800 #262B36` → `900 #11151C` → `1000 #000000`.

### Semantic status · *UI extension*

The brand has no success green and no readable error/info hues, so these are sanctioned additions. **`success` is tuned teal-adjacent** to harmonize; **`warning` is a deeper amber kept distinct from brand Yellow** so a status is never mistaken for a brand color; `danger` sits near Soft Coral; `info` derives from Light Blue. Each has `subtle` (bg), default (icon/fill), `strong` (text).

| Purpose | Default | Subtle | Strong |
|---------|---------|--------|--------|
| Success | `#12B886` | `#E2F7EF` | `#0C7A5A` |
| Warning | `#E8A200` | `#FFF4D1` | `#A66F00` |
| Danger | `#E5484D` | `#FCE7E8` | `#B4262B` |
| Info | `#2BA6E8` | `#E3F1FC` | `#176C9E` |

### Semantic aliases

| Role | Value | CSS var | Tailwind |
|------|-------|---------|----------|
| Body text | `#000000` | `--color-text-primary` | `text-ink` |
| Secondary text | `#5A6172` | `--color-text-secondary` | `text-ink-secondary` |
| Tertiary / muted | `#7E8696` | `--color-text-tertiary` | `text-ink-tertiary` |
| Disabled text | `#A7AEBC` | `--color-text-disabled` | `text-ink-disabled` |
| Link | `#22C7C6` | `--color-text-link` | `text-ink-link` |
| Page background | `#FFFFFF` | `--color-surface-page` | `bg-surface` |
| Raised surface | `#F7F8FA` | `--color-surface-raised` | `bg-surface-raised` |
| Sunken surface | `#EFF1F5` | `--color-surface-sunken` | `bg-surface-sunken` |
| Dark surface | `#11151C` | `--color-surface-inverse` | `bg-surface-inverse` |
| Border subtle / default / strong | `#E2E5EB` / `#CBD0D9` / `#5A6172` | `--color-border-*` | `border-line-*` |
| Focus ring color | `#22C7C6` | `--color-border-focus` | `border-line-focus` |

### Interactive (buttons)

The **primary action is Purple** with white text — it reads as "the primary action," and because purple is reserved for that one role, CTAs stand out. **Teal stays the accent** (focus ring, links, selection, active states) and the brand default-dominant for data and expressive use. The other brand colors are for categorization and expressive surfaces, not for signalling the primary action.

| Variant | Background | Hover | Active | Foreground |
|---------|-----------|-------|--------|------------|
| Primary | `#5349FF` | `#4339E6` | `#3A33B8` | `#FFFFFF` |
| Secondary | `#000000` | `#11151C` | `#262B36` | `#FFFFFF` |
| Tertiary | `transparent` | `#EFF1F5` | `#E2E5EB` | `#000000` |
| Destructive | `#E5484D` | `#B4262B` | `#B4262B` | `#FFFFFF` |

### Charts · *UI extension*

Lead with **`chart-1` (Teal)** — the brand default-dominant — so the brand carries the dashboard. Naming is positional (`chart-1`…`chart-8`) so series can swap colors without renaming code. Each has `subtle` (area fills), default (line/bar), `strong` (emphasis). Order: 1 Teal, 2 Purple, 3 Yellow, 4 Pink, 5 Light Blue, 6 Soft Coral, 7 Green, 8 Orange. **Don't exceed 8** — aggregate or switch to a sequential ramp (`--color-seq-teal-1..5`, `-purple-`, `-neutral-`) or diverging ramp (`--color-div-teal-pink-1..5` direction-only, `--color-div-bad-good-1..5` valenced).

**Anti-patterns:** don't use a brand color for chart grid lines (use `--color-chart-grid`, which themes light/dark); don't mix categorical and semantic colors in one chart; axis labels use `--color-text-secondary` at `bodyS`/`caption`.

---

## Dark mode · *UI extension*

Q ships a dark theme. It **remaps the semantic layer only** — `surface`, `text`, `border`, the `fill` interaction tokens, semantic status, interactive, chart fills + grid, and shadows. The **Primary Four hues, the neutral ramp, and gradients do not change.** Anything that reads a semantic token (`var(--color-surface-page)`, `text-ink`, `border-line`, `bg-success-subtle`, …) themes automatically — **never hardcode a neutral step** (e.g. `--color-neutral-100`) for a surface or fill, or it won't flip.

**Activation** — OS by default, overridable per-document with a `[data-theme]` on `<html>`:

| state | behavior |
|-------|----------|
| *(no attribute)* | follows the OS via `prefers-color-scheme` |
| `data-theme="dark"` | force dark |
| `data-theme="light"` | force light (overrides a dark OS) |

```html
<!-- set before paint to avoid a flash -->
<script>var t=localStorage.getItem('q-theme');if(t)document.documentElement.setAttribute('data-theme',t);</script>
```

Tailwind: the preset sets `darkMode: ['selector', '[data-theme="dark"]']` and the semantic color utilities resolve to CSS vars, so `bg-surface` / `text-ink` / `bg-success-subtle` follow the theme with **no `dark:` prefix**. (Trade-off: Tailwind opacity modifiers like `bg-primary/50` don't apply to the var-backed semantic tokens — the raw `brand-*` / `neutral-*` palette keeps them.)

**Surfaces — elevation by tint, not shadow.** Shadows barely read on dark; depth comes from a *lighter* surface plus a border.

| token | light | dark |
|-------|-------|------|
| `surface-sunken` | `#EFF1F5` | `#0C1014` |
| `surface-page` | `#FFFFFF` | `#11151C` |
| `surface-raised` | `#F7F8FA` | `#262B36` |

**Text:** primary `#000`→`#EFF1F5`, secondary →`#A7AEBC`; the Teal **link** lightens to `#4FD6D4` for AA. **Borders** climb the ramp (`subtle #262B36`, `default #3E4453`). **Status** pairs invert — `subtle` → a dark tint, `strong` → a light tint (e.g. success `#10271E` / `#7CE7C7`). **Buttons:** primary stays Purple; the black secondary becomes a light surface with dark text. **Focus ring** stays Teal. **Logo** stays full-color on a white tile.

**Interaction fills:** use `--color-fill-hover` / `--color-fill-active` (`#F7F8FA` / `#EFF1F5` → `#1C222C` / `#262B36`) for hover/active backgrounds — not raw neutrals.

---

## Typography

**Poppins. One typeface, every level. Never italics.**

```css
--font-primary: "Poppins", system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
--font-mono:    "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace; /* code & tabular numerals only */
```

Load Poppins (e.g. Google Fonts) at weights **300, 400, 500, 600, 700** — no italics axis.

**Weights:** Light 300 (labels only) · Regular 400 (body) · Medium 500 (callouts/labels) · SemiBold 600 (section headers) · Bold 700 (display/hero). Weights outside this set are off-brand.

### Type scale

Use the `.t-*` utility classes from `tokens.css`, or Tailwind `text-displayXL` … `text-code`.

| Token | Weight | Size / line | Use |
|-------|--------|-------------|-----|
| `displayXL` | 700 | 72 / 76 | Hero |
| `displayL` | 700 | 56 / 60 | Hero |
| `displayM` | 700 | 48 / 52 | Page hero |
| `displayS` | 700 | 36 / 42 | Big numbers, hero subhead |
| `headingXL` | 600 | 32 / 40 | Page title |
| `headingL` | 600 | 28 / 36 | Section |
| `headingM` | 600 | 24 / 32 | Subsection / card group |
| `headingS` | 600 | 20 / 28 | Card title |
| `headingXS` | 600 | 16 / 24 | Dense headings |
| `bodyL` | 400 | 18 / 30 | Lede |
| `bodyM` *(default)* | 400 | 16 / 26 | Body |
| `bodyS` | 400 | 14 / 22 | Secondary body |
| `label` | 500 | 14 / 20 | Form labels, buttons |
| `caption` | 500 | 13 / 18 | Captions, meta |
| `overline` | 600 | 12 / 16 · UPPERCASE · +0.08em | Eyebrows, table headers |
| `quote` | 600 | 24 / 34 | Pull-quotes (larger than body) |
| `quoteAttribution` | 400 | 14 / 20 | Quote attribution beneath |
| `statValue` | 700 | 48 / 52 | Standalone data callout numbers |
| `statLabel` | 400 | 14 / 20 | Stat label beneath the number |
| `code` | 400 mono | 14 / 20 | Code, IDs |

The composite scale is the **default** for real type — it bakes in the correct weight, line-height, and tracking, and themes nothing you have to remember.

### Raw size scale (t-shirt) · *UI extension*

A primitive **size-only** scale for one-off sizing — a single glyph, a number, a tweak that doesn't warrant a semantic role. Every step lands on an existing Q type size, so it never introduces an off-grid value. Tailwind `text-xs` … `text-8xl`; CSS `var(--text-md)`. It carries **size only** — no weight, line-height, or tracking — so compose `font-*` / `leading-*` / `tracking-*` yourself. **Reach for the composite scale first;** use the t-shirt scale only when no semantic token fits.

| Utility | Size | ≈ Composite |
|---------|------|-------------|
| `text-xs` | 12 | overline |
| `text-sm` | 14 | bodyS / label |
| `text-md` | 16 | bodyM |
| `text-lg` | 18 | bodyL |
| `text-xl` | 20 | headingS |
| `text-2xl` | 24 | headingM |
| `text-3xl` | 28 | headingL |
| `text-4xl` | 32 | headingXL |
| `text-5xl` | 36 | displayS |
| `text-6xl` | 48 | displayM / statValue |
| `text-7xl` | 56 | displayL |
| `text-8xl` | 72 | displayXL |

**`text-xs` (12px) is the floor for text** — there is no sub-12 step, per the brand minimum. For sizing **icons**, don't reach here — use the dedicated `text-icon-*` utilities (see [Iconography](#iconography--phosphor)).

### Brand typography rules

- **Titles are left-aligned, always.** Two-line stacks preferred. **No accent lines or decorative elements beneath titles.**
- **Quotes:** SemiBold 600, larger than body; attribution in Regular 400 beneath. No decorative quote graphics.
- **Stats / data callouts:** numbers large and standalone (`statValue`), label small beneath (`statLabel`), no decoration.
- Never: italics (anywhere), all-caps beyond `overline`, centered or flush-right headlines/body, or gradients/effects applied to type. **One sanctioned exception:** the `.t-grad` utility may clip an AA-tuned gradient onto a single keyword in a title (see [Gradients](#gradients)). Never on body, never across a whole headline.

---

## Spacing

Base unit **4px**; always snap to the grid. **On brand / marketing surfaces, Quadrivia favors generous spacing** — breathing room is a design choice; when unsure, take the larger step. **On data-heavy product surfaces, switch on [compact density](#density--ui-extension)** so the same components tighten up without going off-grid.

`--space-1 4` · `2 8` · `3 12` · `4 16` · `5 20` · `6 24` · `8 32` · `10 40` · `12 48` · `16 64` · `20 80` · `24 96` · `32 128` · `40 160` · `48 192` · `64 256` (plus `0`, `px`=1, `0.5`=2).

**Semantic spacing:** component padding XS 8 / S 12 / M 16 / L 24 / XL 32 · stacks XS 8 → XL 40 · **section gaps S 64 / M 96 / L 128** · page gutters mobile 20 / tablet 32 / desktop 48.

These are the **comfortable** (default) values; data-heavy surfaces tighten them via compact density — see next.

---

## Density · *UI extension*

Two densities. **Comfortable is the brand default** (the generous spacing above). **Compact** opts data-heavy surfaces — queues, tables, dashboards, dense forms — into a tighter layer so they fit more without feeling cramped. It works exactly like dark mode: a `[data-density]` attribute remaps a small set of **var-backed tokens**; everything else (the Primary Four, radius, the raw 4px scale, type scale) is unchanged.

**Activation** — set `data-density` on `<html>` (whole app) or on any container (just that panel):

| state | behavior |
|-------|----------|
| *(no attribute)* | comfortable — the brand default |
| `data-density="compact"` | compact — for data-dense surfaces |
| `data-density="comfortable"` | force comfortable inside a compact ancestor |

**What flips** (comfortable → compact). Each is a CSS var exposed as a Tailwind utility, so it re-densifies with no `dark:`-style variants:

| token | utility | comfortable → compact |
|-------|---------|-----------------------|
| `--density-control` | `h-control` (control/row height) | 44 → 36 |
| `--density-pad` | `p-pad` (card / panel padding) | 24 → 16 |
| `--density-tight` | `p-tight` (table cell / dense) | 12 → 8 |
| `--density-stack` | `gap-stack` (stack gap) | 16 → 12 |
| `--density-section` | `gap-section` / `mb-section` | 96 → 64 |
| `--density-gutter` | `gap-gutter` (grid gutter) | 24 → 16 |
| `--density-text` (+ leading) | `text-data` (data body) | 16/26 → 14/20 |

Build a data surface with these instead of fixed steps and it tightens automatically:

```html
<section data-density="compact">                          <!-- opt this panel into compact -->
  <button class="h-control px-5 rounded-pill …">Run</button>  <!-- 44 → 36 -->
  <div class="p-pad rounded-card …">…</div>                  <!-- card padding 24 → 16 -->
  <td class="p-tight text-data …">…</td>                     <!-- cell 12 → 8, text 16 → 14 -->
</section>
```

**Use compact for:** queues, data tables, dashboards, list-heavy views, dense forms, side panels. **Keep comfortable for:** landing / marketing, hero, onboarding, empty states — anything brand-facing. Touch-first surfaces stay at 44px; compact's 36px control is for pointer / desktop density.

---

## Shape — radius & borders

**Quadrivia is round. No hard right angles.**

| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | 8px | Inner elements, small chips |
| `--radius-md` | 12px | **Inputs**, small controls |
| `--radius-lg` | 16px | Dropdowns, popovers, toasts, **data tables** |
| `--radius-xl` | 20px | Panels |
| `--radius-card` | **30px** | **Cards, containers, modals, image frames** (brand value) |
| `--radius-hero` | 40px | Hero sections, large feature surfaces |
| `--radius-pill` | 9999px | **Buttons, labels, badges, pills, status dots** |
| `--radius-circle` | 50% | Avatars, icon buttons |

Default container radius is **30px**; default control radius is **pill**. `--radius-none` (0) is reserved only for the inner cells of a clipped container (e.g. table cells inside a 30px-rounded, `overflow:hidden` frame).

**Borders:** `--border-width-thin` 1px (default) · `thick` 2px (the gradient separator rule) · `heavy` 4px (structural accents). Default border color `--color-border-subtle`/`-default`.

---

## Elevation · *UI extension*

Soft, diffuse, **cool-tinted** shadows (`rgba(17,21,28,…)`) — never pure black. Quadrivia leans on color and space over heavy shadow, so keep elevation light.

| Token | z-index | Use |
|-------|---------|-----|
| `--shadow-0` | 0 | Page surface |
| `--shadow-1` | 10 | Cards, list rows |
| `--shadow-2` | 100 | Sticky headers |
| `--shadow-3` | 1000 | Dropdowns, tooltips |
| `--shadow-4` | 1100 | Popovers, menus |
| `--shadow-5` | 1200 | Modals |
| `--shadow-6` | 1300 | Toasts |

Focus ring: `--shadow-focus-ring` (`0 0 0 3px rgba(34,199,198,.40)`, teal) on light; `--shadow-focus-ring-inverse` (white) on dark. **Every interactive element needs a visible focus ring.**

---

## Motion

Default to `--duration-base` (200ms) with `--ease-standard`. Durations: instant 0 · fast 120 · base 200 · slow 320 · slower 480. Easings: `--ease-standard` (most), `--ease-entrance`, `--ease-exit`, `--ease-emphasis`. Never `transition: all` — name the properties. The generated CSS includes a `prefers-reduced-motion` guard; honor it.

---

## Layout

**Z-index:** `--z-dropdown 1000` · `popover 1100` · `modal 1200` · `toast 1300` · `tooltip 1400`. Always use the named tokens.

**Breakpoints (Tailwind `screens`):** sm 640 · md 768 · lg 1024 · xl 1280 · 2xl 1536. **Max-widths:** 2xl 1440 (default app shell — dashboards, tables, data-dense product surfaces) · xl 1200 (compact / centered content) · prose 680 (reading / form columns).

**Sizes:** icons `--size-icon-*` (xs 12 → 2xl 48, default m 20) · controls `--size-control-*` (s 36 / **m 44** / l 52 / xl 60 · Tailwind `h-control-s/m/l/xl`) · avatars `--size-avatar-*` (s 24 / m 32 / l 48 / xl 64).

---

## Grid

A **12-column grid** for dashboards and side-by-side panels — reach for it instead of hand-rolling `grid-cols-*` per layout. Use the `.q-grid` container (12 columns; gutter = the density-aware `--density-gutter`) with `col-span-*` on children; the gutter tightens under compact density.

```html
<div class="q-grid">
  <section class="col-span-8">Primary panel</section>
  <aside class="col-span-4">Side panel</aside>
</div>
```

Inline in Tailwind it's `grid grid-cols-12 gap-gutter`, with `col-span-{1..12}` (add `md:col-span-12` to stack on small screens). Common splits: **8 / 4** (content + rail) · **6 / 6** (compare) · **9 / 3** (main + filters) · **3 × 4** (card wall).

**Containers** — center with `mx-auto` + page-gutter padding, capped at a max-width: **`max-w-2xl` 1440** (app shell — dashboards, tables) · **`max-w-xl` 1200** (compact / centered) · **`max-w-prose` 680** (reading / forms). Wrap a `.q-grid` in one of these.

---

## Iconography — Phosphor

Quadrivia standardizes on **[Phosphor Icons](https://phosphoricons.com)** — its rounded, friendly forms match the brand's "no hard right angles" geometry. **Phosphor only; never mix in another library** (Material, Heroicons, Lucide, FontAwesome, Feather). Mixing breaks stroke weight and corner consistency.

**Install (quickstart):** per-weight CSS via CDN for static pages; `@phosphor-icons/react` for the product app. Load only the weights you use (regular always; add bold and fill if used).

```html
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2/src/regular/style.css" />
<i class="ph ph-heartbeat" aria-hidden="true"></i>
```

The **full install matrix** (all-weights JS, npm web/React/Vue, `IconContext` design-system defaults, self-hosting) and **deep worked examples at every size** (buttons, inputs, menus, nav, list rows, empty states) are in **[references/iconography.md](references/iconography.md)**.

**Use sparingly** — one icon per control max, always left of the label, never decoratively, never an icon next to a label that says the same thing (mark decorative icons `aria-hidden="true"`; icon-only buttons need `aria-label`). Set size to match the control (default `--size-icon-m` 20px); full sizing table in [references/iconography.md](references/iconography.md#sizing-in-context). Icons inherit `currentColor` — set `color`, not `fill`/`stroke`. Use `regular` by default; `bold` for emphasis (mirrors "bold, never italics"); `fill` for active/selected states. Avoid `thin`, `light`, and `duotone`.

**Sizing — use the `text-icon-*` utilities, never an arbitrary `text-[Npx]`.** Phosphor glyphs are font-sized, so the icon scale rides the same `font-size` channel as text. The `--size-icon-*` tokens are exposed as atomic Tailwind utilities so icons stay on-grid:

| Utility | Size | Use |
|---------|------|-----|
| `text-icon-xs` | 12 | Status dots, micro-glyphs, chip close (`ph-x`) |
| `text-icon-s` | 16 | Inline glyphs, dense list rows, pagination carets |
| `text-icon-m` *(default)* | 20 | Buttons, nav, toolbars, menu items |
| `text-icon-l` | 24 | Prominent actions, section headers |
| `text-icon-xl` | 32 | Empty-state and feature glyphs |
| `text-icon-2xl` | 48 | Large empty states, marketing |

CSS users size from the same source: `font-size: var(--size-icon-m)`. **Snap to a step — no `text-[18px]`, no off-grid icon sizes.**

**Healthcare concepts (Q is healthcare):** vitals → `ph-pulse` / `ph-heartbeat`; cardiology → `ph-heart`; mental health → `ph-brain`; care/first-aid → `ph-first-aid` / `ph-first-aid-kit`; clinician → `ph-stethoscope`; medication → `ph-pill`; injection → `ph-syringe`; infection → `ph-virus`; records → `ph-clipboard-text`; hospital → `ph-hospital`.

**General UI:** add `ph-plus`, search `ph-magnifying-glass`, filter `ph-funnel`, edit `ph-pencil-simple`, delete `ph-trash`, settings `ph-gear`, user `ph-user`, calendar `ph-calendar-blank`, time `ph-clock`, notify `ph-bell`, message `ph-chat-circle`, email `ph-envelope`, more `ph-dots-three`, nav `ph-caret-right/left/down/up`, success `ph-check-circle`, warning `ph-warning`, info `ph-info`, error/close `ph-x`, download `ph-download-simple`.

**Don't:** use emojis as icons; recolor health icons with semantic colors (inherit `text-secondary`/`text-primary`); put more than one icon in a button; draw bespoke icons for things Phosphor already has.

---

## Signature layout devices

These are what make a screen read as **Quadrivia**, not generic. Use them.

### Gradient separators (no bullets)

**No bullets, dashes, or numbered lists** in product/marketing UI. Separate list items with a 2px horizontal rule that cycles the Primary Four (`--gradient-separator`). The build ships a `.q-separator` helper:

```html
<div class="list-item">Nurses define the standards.</div>
<hr class="q-separator" />
<div class="list-item">Nurses do the testing.</div>
<hr class="q-separator" />
<div class="list-item">Nurses determine what works.</div>
```

### "With Q / Without Q" contrast framing

The brand's recurring layout device: two **equal-weight** side-by-side columns comparing the world with and without Q. **Neither side dominates through color** — don't paint "Without Q" red and "With Q" teal. Keep the columns equal; let the content carry the contrast. Use a subtle neutral surface for one side at most.

### Repetition as rhythm

Short declarative statements repeat **in threes**, with white space for the rhythm to land. Never collapse them into one sentence. (e.g. "Nurses define the standards. Nurses do the testing. Nurses determine what works.") Apply this in hero sections, feature triads, and value props.

### Gradients

Gradients are signature, used deliberately — not as random decoration. **`--gradient-brand`** cycles the Primary Four in the order **teal→purple→pink→yellow** (teal and yellow never touch, so there's no green blend) and is reserved for **small accents/details** — thin strips, tiny marks, the separator rule. **`--gradient-teal-pink`** is the **secondary** gradient: reach for it on **large expressive shapes/surfaces**, since the busy four-color brand reads as noise at scale. **`--gradient-teal-purple`** for progress bars, timelines, and data spans (the product roadmap look). Never run a gradient under type (a gradient background behind text hurts legibility).

**Gradient on a title keyword (one sanctioned exception, v2.10).** Applying a gradient to type is otherwise off-limits, but the `.t-grad` (and `.t-grad-pink`) utility may clip an **AA-tuned** gradient onto a **single keyword in a title**. It uses `--gradient-ink-teal-purple` / `--gradient-ink-teal-pink`, whose stops are deepened (deep teal `#15807F` into purple `#5349FF` or strong pink `#B01060`) so every point holds at least **4.5:1 on white**, with a solid-color fallback for browsers that cannot clip text and a `forced-colors` guard. Keep it to one gradient keyword per title, never on body, never across a whole headline, and keep the weight Bold. On dark surfaces these two ink gradients swap to lighter stops (the only gradients that theme, for the same legibility reason text color does).

---

## Component recipes

Starting points that combine tokens correctly. Don't re-derive these. Each also lists a **Tailwind** class string; the full atomic vocabulary + more recipes live in [references/tailwind.md](references/tailwind.md).

### Button (primary, medium)

```
height: 44px (control-m)        radius: pill
padding: 0 20px                 font: Poppins 600 14/20 (.t-label, weight 600)
background: #5349FF → hover #4339E6 → active #3A33B8
color: #FFFFFF                  (white on purple — AA 5.8:1)
focus: box-shadow var(--shadow-focus-ring)
disabled: opacity .48
transition: background-color 120ms var(--ease-standard)
```
Secondary = black bg / white text. Tertiary = transparent / black text / hover `#EFF1F5`. Destructive = `#E5484D` / white. All pill-shaped.

**Tailwind** · `inline-flex items-center justify-center h-11 px-5 rounded-pill text-label font-semibold bg-primary text-primary-fg hover:bg-primary-hover active:bg-primary-active focus-visible:shadow-focus disabled:opacity-50` — swap `primary` → `secondary` / `tertiary` / `destructive` (all theme in dark).

### Input (text field)

```
height: 44px (control-m)        radius: 12px (--radius-md)
padding: 0 14px                 font: bodyM (16/26)
background: #FFFFFF              border: 1px solid #CBD0D9
placeholder: #7E8696
hover border: #A7AEBC
focus: border #22C7C6 + box-shadow var(--shadow-focus-ring)
error: border #E5484D + helper text in danger
```

**Tailwind** · `h-11 w-full px-3.5 rounded-md text-bodyM bg-surface text-ink border border-line placeholder:text-ink-tertiary hover:border-neutral-400 focus:border-line-focus focus:shadow-focus focus:outline-none`

### Card

```
background: #FFFFFF (or surface-raised)   border: 1px solid #E2E5EB
radius: 30px (--radius-card)              padding: 24px (component L)
shadow: --shadow-1
hover (interactive): --shadow-3, translateY(-2px), 200ms var(--ease-standard)
```

**Tailwind** · `bg-surface border border-line-subtle rounded-card shadow-1 p-6` — interactive: add `hover:shadow-3 hover:-translate-y-0.5 transition-shadow`.

### Badge / pill

```
radius: pill            font: overline (12/16, UPPERCASE, +0.08em)  — or caption for sentence case
height: 24px            padding: 0 10px
neutral: bg #EFF1F5 / text #000000
status: bg <semantic>-subtle / text <semantic>-strong
environment: Sandbox = warning (amber) · Production = success (teal-green) — small, uppercase; never brand-purple
```

**Tailwind** · `inline-flex items-center h-6 px-2.5 rounded-pill text-overline uppercase bg-success-subtle text-success-strong` — swap the semantic group (warning / danger / info).

**Environment badge** (deploy env in a workspace/tenant switcher): a status badge, not a brand-color chip. **Sandbox** → `warning` (`#FFF4D1` / `#A66F00`); **Production** → `success` (`#E2F7EF` / `#0C7A5A`). Small, uppercase, pill — so prod is unmistakable at a glance. Never use `--color-brand-purple` (reserved for the primary action) or a low-contrast tinted fill.

### Stat callout

```
number: .t-statValue (Poppins 700, 48/52), color #000000 or a brand color
label:  .t-statLabel (Poppins 400, 14/20), color #5A6172, beneath the number
no decoration, no icon competing with the number
```

### Modal

```
overlay: var(--color-surface-overlay)  (rgba(17,21,28,.56)) full viewport
panel: #FFFFFF, radius 30px (--radius-card), padding 24–32px
shadow: --shadow-5     z-index: --z-modal (1200)
entrance: opacity + translateY(8px), 200ms var(--ease-entrance)
```

### Dropdown / popover / toast

```
dropdown/popover: #FFFFFF, border 1px #E2E5EB, radius 16px (--radius-lg),
  shadow --shadow-3/4, z 1000/1100, item padding 8px 12px, item hover #EFF1F5
toast: surface-inverse (#11151C) or <semantic>-subtle, radius 16px,
  shadow --shadow-6, z 1300, auto-dismiss 4–6s
```

### Forms, tables & filtering

These have dedicated deep references — reach for them for any form, data table, or filter UI:

- **[references/forms.md](references/forms.md)** — every control (text, select, textarea, checkbox, radio, toggle, addons), states, validation, and sectioned form cards.
- **[references/tables-and-filtering.md](references/tables-and-filtering.md)** — data tables (sort, row-select, row actions, density, pagination, empty/loading) and filtering (the `LABEL value ⌄` filter-pill bar, search, segmented control, faceted popover, removable chips, filtered-empty state).

Quick hits: text controls are `--radius-md` (12px), 44px tall, Teal focus; **selects** use a Phosphor caret, never the native arrow; checkbox/radio/toggle selected = Teal; **filter pills** are `--radius-pill` with an uppercase label + bold value + caret, border turning Teal when a non-default value is set; selected table rows take a Teal-subtle wash, and status always rides in a **badge**, never a color-filled row.

### Section heading + body

```
overline (optional): .t-overline, color #5A6172
title:   .t-headingXL, color #000000, LEFT-ALIGNED, two-line stack ok, NO underline beneath
body:    .t-bodyM, color #5A6172
stack: 12px overline→title, 16px title→body
```

---

## Composing screens & flows

The tokens are the language and the [component gallery](components/index.html) the vocabulary; **[references/screens-and-flows.md](references/screens-and-flows.md)** is how to assemble them into a screen or flow — read it before recreating any Q screen or user flow. The method:

1. **Name the archetype** — list/queue · detail · dashboard · form · empty/onboarding.
2. **Shell & density** — product screens sit in the [app shell](components/index.html#app-shell) @ 1440; **data-heavy → `data-density="compact"`**, brand/onboarding → comfortable.
3. **Compose the stack** the archetype prescribes — e.g. **list/queue** = app shell → page header → filter bar → data table → pagination → empty state; **dashboard** = page header + segmented range → stat tiles → chart cards in a `.q-grid`. Keep one primary action per view, status in badges (never a colored row), `.q-grid` for any side-by-side.
4. **Worked screens** live in `examples/` (campaigns, journeys, reports). The full "which component for the job" table, every archetype, and the flow patterns are in **[references/screens-and-flows.md](references/screens-and-flows.md)**.

---

## Voice & content (summary)

Full rules in [references/voice-and-content.md](references/voice-and-content.md). The essentials:

- **Voice:** direct, specific, grounded in clinical reality. It doesn't explain itself, hedge, or celebrate its own tech. Test: if a line could run in any healthcare-AI company's marketing, it isn't Q copy.
- **Empathy principle:** never imply AI outperforms clinicians. Q absorbs volume so clinicians focus where human judgment matters most.
- **Hard copy rules** (UI, microcopy, tooltips, errors too): **no em dashes anywhere** (use a period + new sentence, parentheses, or a restructure) · **no italics** (bold for emphasis) · **no first-person** ("we" / "our") · **no centered body text**.
- **Rhythm:** short declarative over descriptive; lists repeat in threes with white space; never collapse the three.
- **People are patients, not "users"** in patient-facing / clinical copy.
- **CTAs & links:** natural, low-pressure, no performative asks; link text describes its destination.
- **Naming:** Quadrivia = company, Q = product. Never interchangeable (except the About page). **Never "the Q".** Always capitalize Q standalone.
- **Taglines:** "Q. Helping Healthcare Help Humans." (hero) · "You direct. Q delivers." (differentiator).
- **Word swaps:** journeys not tasks · full journey / care continuum not single-task · orchestrate / run / own not automate · partner / managed service not tool / solution · patients not users.

---

## Quick-reference cheat sheet

| Decision | Reach for |
|----------|-----------|
| Primary CTA | bg `#5349FF` (purple), **white** text, pill, hover `#4339E6` |
| Page background | `#FFFFFF` (`bg-surface`) |
| Card | bg white, border `line-subtle`, **radius 30px**, `shadow-1` |
| Body text | `#000000` (`text-ink`) at `bodyM` 16/26 Poppins 400 |
| Secondary text | `#5A6172` (`text-ink-secondary`) |
| Section title | `headingXL` Poppins 600, left-aligned, no underline |
| Semantic type (default) | `text-bodyM` / `text-headingXL` … (or `.t-*`) — bakes in weight + leading + tracking |
| Raw size (one-off) | t-shirt `text-xs`…`text-8xl` (size only; `text-xs` 12 is the floor) |
| Icon size | `text-icon-m` 20 (default) · xs 12 / s 16 / l 24 / xl 32 — **never `text-[Npx]`** |
| Input | radius **12px**, border `#CBD0D9`, focus teal + ring |
| Button / badge / pill radius | **pill** (`--radius-pill`) |
| Container / modal radius | **30px** (`--radius-card`) |
| Data table radius | **16px** (`--radius-lg`) — tighter than cards |
| List items | `.q-separator` gradient rule — **no bullets** |
| Emphasis | **weight** (SemiBold/Bold) — **never italics** |
| Copy voice | direct, specific, clinical · **no em dashes** anywhere · no first-person · patients not "users" |
| Chart series 1 (lead) | `chart-1` Teal `#22C7C6` |
| Below/above baseline | `--color-div-teal-pink-*` |
| On-target vs miss | `--color-div-bad-good-*` |
| Success / Warning / Danger / Info | `#12B886` / `#E8A200` / `#E5484D` / `#2BA6E8` |
| Icon library | **Phosphor only** (`ph ph-*`) |
| Vitals / clinician / medication icon | `ph-pulse` / `ph-stethoscope` / `ph-pill` |
| Logo in product | `assets/logo/q-lockup.webp`, height ≥ 32px, full-color, never recolored |
| Text input / select | `--radius-md` 12px, 44px tall, Teal focus; select uses a Phosphor caret |
| Filter control | `.filter-pill` — pill, uppercase label + bold value + caret |
| Selected table row | Teal-subtle wash; status in a badge, never a filled row |
| Dark mode | OS via `prefers-color-scheme`; force with `[data-theme="dark"\|"light"]` on `<html>` |
| Hover / active fill | `--color-fill-hover` / `--color-fill-active` — never raw `neutral-*` |
| Dark surfaces | `page #11151C`, `raised #262B36`; elevation = lighter tint, not shadow |
| Density | comfortable by default; `data-density="compact"` on data screens (tables, queues, dashboards) |
| Compact utilities | `h-control` 44→36 · `p-pad` 24→16 · `p-tight` 12→8 · `gap-stack` 16→12 · `text-data` 16→14 |
| Grid | `.q-grid` (12-col, `gap-gutter`) + `col-span-*`; splits 8/4, 6/6, 9/3, card wall |

---

## Consuming the tokens

**Plain CSS / HTML:** link `tokens/tokens.css`, then use `var(--color-…)` and the `.t-*` type utilities.

**Tailwind / atomic CSS:** a ready-to-use config ships at the repo root —
```js
// tailwind.config.js
module.exports = { presets: [require('./tokens/tailwind.preset.js')], content: ['./src/**/*.{html,js,jsx,ts,tsx,vue}'] };
```
Then build with utilities: `bg-primary`, `text-ink`, `bg-surface`, `border-line`, `rounded-card`, `rounded-pill`, `shadow-1`, `text-headingXL`, `bg-gradient-teal-pink`, etc. Also load `tokens.css` — the semantic utilities resolve to its CSS vars, which is how they flip light/dark. **Full setup, the token→utility cheat-sheet, and every component recipe as a class string: [references/tailwind.md](references/tailwind.md).** A build-free live demo is `examples/tailwind-demo.html`; the full **browsable component gallery** — 45 components (atoms → molecules → organisms) as copy-paste atomic recipes, light/dark — is `components/index.html`.

**React / shadcn:** drive shadcn's CSS variables from `tokens.css` (map `--background`→`--color-surface-page`, `--primary`→`--color-primary-bg`, `--radius`→`--radius-card`, etc.) and use the Tailwind preset for utilities. Keep Poppins + Phosphor as the only font and icon set.

**Dark mode:** ships in `tokens.css` (`prefers-color-scheme` + a `[data-theme]` override) and in the Tailwind preset (`darkMode: ['selector', '[data-theme="dark"]']`). Components that use the semantic tokens theme automatically — set `data-theme` on `<html>` for a manual toggle (persist to `localStorage`, apply before paint). See **[Dark mode](#dark-mode--ui-extension)**.

**Changing a token:** edit `tokens/quadrivia.tokens.json`, run `node scripts/build-tokens.mjs`, commit the regenerated `tokens.css` + `tailwind.preset.js` together. Provenance (what comes from the brand guide vs. what's a sanctioned UI extension) is recorded in the JSON's `$meta`.

---

## Authoring

Authored and maintained by **David Vegas Garcia** (`david.vegas@quadrivia.ai`). Source: the Q Brand Guidelines 2026, extended with the UI tokens this product system needs. Propose changes by editing the token JSON (never the generated files) and documenting the rationale, traceable back to the brand guide or marked as a UI extension.
