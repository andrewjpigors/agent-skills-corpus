---
name: aetherweave-design-system
description: >-
  Applies the Aetherweave design system — Black Bleak Modern Extremism edition —
  (obsidian tokens, dark liquid glass, monochromatic typography, motion, accessibility,
  components) to UI, CSS, content, and design artifacts. Use when the user mentions
  Aetherweave, skills design.md, dark luxury extremism, --aw-* tokens, liquid
  void glass, black mono abstract UI, or asks for branding consistent with this
  repository's spec.
---

# AETHERWEAVE DESIGN SYSTEM
### The Complete, AI-Agent-Ready Specification
**Version 3.0 — 2026 Edition | Black Bleak Modern Extremism Pivot**
**Supersedes v2.0 (warm-earth edition) and Style Guide v1.1**

> This document is the single source of truth for every interface, artifact, website, application, stage visual, print, and spatial experience produced under the Aetherweave identity. It is written to be consumed by AI agents and human designers alike. Every token, rule, component spec, and edge case is defined explicitly — **no "use judgment," no "it depends,"** unless a decision tree is provided.
>
> **This version pivots Aetherweave into its most extreme form: ultra-dark, bleakly opulent, monochromatically hypnotic. The warm-earth + jewel palette is retired. Obsidian dominates. Stark contrast and metallic glints carry dopamine.**

---

## 0. HOW TO USE THIS DOCUMENT (AI Agent Primer)

### 0.1 Order of Precedence
When rules appear to conflict, resolve in this order:
1. **Accessibility** (Section 14) — never compromised
2. **Core Design Tokens** (Section 3) — values are absolute
3. **Component Specifications** (Section 8) — patterns are canonical
4. **Motion & Animation** (Section 9)
5. **Aesthetic Directives** (Sections 2, 4, 5)

### 0.2 AI Agent Decision Rules
- **Never invent a color.** Pull from the defined palette in Section 3.2. All chromatic choices are black, off-black, or achromatic metallic — no hues.
- **Never invent a spacing value.** Use the 4px base scale in Section 3.4.
- **Never invent animation timing.** Use the easing + duration system in Section 9.
- **Never ship without at least 5 Aetherweave visual elements** per meaningful surface (see Section 4.1).
- **Always provide a `prefers-reduced-motion` fallback.**
- **Always provide a `prefers-reduced-transparency` fallback** for the dark liquid glass system.
- **Always verify contrast** against WCAG AA minimum (AAA target for body text). Extreme-contrast is the house style — err high.
- **When uncertain, default to the void.** Aetherweave is maximal *in layering*, not in hue. Depth is sacred, breath is the abyss (Section 4.4).

### 0.3 What This Document Covers
Philosophy → Tokens → Visual Language → Dark Liquid Glass system → Layout → Typography → Components → Motion → Imagery → Responsive → Themes → Accessibility → Edge Cases → Code Patterns → Quality Checklist.

---

## 1. CORE PHILOSOPHY

Aetherweave is a luxury abstract design language synthesizing silk-print craftsmanship, spatial computing fluidity, and culturally expansive storytelling — now channeled through an extreme black monochromatic lens. It retains the masterful layering, narrative depth, and luxurious craftsmanship of the original silk-heritage synthesis (multi-layered storytelling, hand-rendered intricacy, emotional resonance), but delivered as **obsidian depth, high-contrast starkness, and hypnotic intensity** that commands the eye, rewards prolonged gaze, and triggers dopamine through discovery, rhythm, and perceptual tension.

**This is dark luxury extremism**: bleak yet opulent, somber yet addictive. Rick Owens' void silhouettes fused with Reinhardt's near-black monochromes and modern cyber-goth dark-glass interfaces — surfaces that pull you in, layered energy maps that reveal new detail the longer you stare, tactile-digital tension that feels ancient and futuristic at once.

**Mantra:** *Weave the void. Layer the infinite dark. Illuminate with stark intensity.*

**Five non-negotiables:**
1. **Originality** — no replication of existing artists or brands; synthesis only.
2. **Layered void depth** — every surface has 4+ perceptible planes of black.
3. **Tactile-digital hypnosis** — hand-crafted bleak tactility meets refractive dark-glass fluidity.
4. **Cultural expansiveness (dark lens)** — global threads abstracted into voids: Japanese ink in obsidian, African rhythmic geometry in charcoal relief, Islamic tessellation as etched shadow, Indigenous fields as subtle dot voids. Respectful, universal, never literal.
5. **Dopamine through bleak intensity** — extreme contrast edges, rhythmic repetition with variation, hidden strata, metallic glints that reward focus. Bleak immersion, never cold sterility.

**Dopamine stimulation mechanics:**
- Extreme high-contrast edges and optical play (subtle illusions, rhythmic pulses).
- Hidden strata that reward close inspection at 100% zoom.
- Textural hypnosis (impasto ridges on matte black, metallic glints in deep voids).
- Perceptual motion and rhythmic variation that feel impossible to look away from.

---

## 2. DESIGN PRINCIPLES (Operational)

| Principle | Rule of thumb | Anti-pattern |
|---|---|---|
| **Layer before you flatten** | If a surface is one plane of black, add another shade. | Flat single-tone blacks; "dark mode" as inverted light mode. |
| **Breath is the abyss** | Negative space is deep void, not empty whitespace. | Edge-to-edge density; gray filler. |
| **Refract, don't reflect** | Dark surfaces blur what's behind; they don't mirror it. | Hard glass/chrome effects; neon reflections. |
| **Gesture, not geometry alone** | Pair every grid/tessellation with an organic void flow. | Pure geometric grids with no gesture. |
| **Obsidian first, metallic as accent** | Black dominance (≥90% surface area); stark white + metallic threads carry all dopamine. | Any chromatic hue; warmth creeping back in. |
| **Stark contrast is structure** | High-contrast edges are the house voice; low-contrast fog is failure. | Muddy grays; mid-contrast sludge. |
| **Motion with intent** | No animation without narrative purpose. | Decorative motion loops; generic fade-ins. |
| **Detail survives zoom** | Micro-texture visible at 100%, macro-composition reads at 25%. | Smooth gradients only; pure flat blacks. |
| **Bleak, never cold** | Warmth-of-craft lives in texture and gesture, not color. | Sterile cyberpunk; corporate dark-mode. |

---

## 3. DESIGN TOKENS

All tokens are CSS custom properties, prefixed `--aw-`. These are the **only** values permitted in production. The palette is strictly monochromatic.

### 3.1 Token Naming Convention
```
--aw-[category]-[variant]-[state?]-[scale?]
```
Examples: `--aw-color-obsidian-500`, `--aw-space-6`, `--aw-radius-lg`, `--aw-shadow-void-hover`.

### 3.2 Color System

#### 3.2.1 Obsidian Core — The Bleak Foundation (primary use: backgrounds, body, structural elements — ≥90% of any surface)

| Token | Hex | OKLCH | Role |
|---|---|---|---|
| `--aw-color-abyss`          | `#000003` | `1% 0.004 270` | Deepest void. Hero ground. |
| `--aw-color-obsidian-900`   | `#050508` | `5% 0.005 270` | Near-deepest. Primary dark surface. |
| `--aw-color-obsidian-800`   | `#0A0A0E` | `8% 0.006 270` | Canvas default. |
| `--aw-color-obsidian-700`   | `#101016` | `11% 0.008 275` | Sunken surface. |
| `--aw-color-jet-700`        | `#13131A` | `13% 0.008 275` | Raised surface floor. |
| `--aw-color-jet-600`        | `#18181F` | `16% 0.009 275` | Elevated surface. |
| `--aw-color-jet-500`        | `#1D1D25` | `19% 0.009 275` | Standard card fill. |
| `--aw-color-ink-umber-500`  | `#1A1612` | `15% 0.008 45`  | Hint-warm black (≤2% of any comp). |
| `--aw-color-midnight-slate-600` | `#1B1D28` | `18% 0.012 260` | Hint-cool black (≤2% of any comp). |
| `--aw-color-charcoal-500`   | `#252530` | `24% 0.012 275` | Borders, inactive, dividers. |
| `--aw-color-charcoal-400`   | `#2F2F3A` | `28% 0.013 275` | Active dividers. |
| `--aw-color-graphite-400`   | `#3A3A46` | `33% 0.013 275` | Muted foreground. |
| `--aw-color-graphite-300`   | `#4A4A55` | `40% 0.012 275` | Secondary text on deep black. |
| `--aw-color-soot-300`       | `#5F5F6B` | `48% 0.011 275` | Tertiary text on deep black. |
| `--aw-color-ash-400`        | `#7A7A85` | `58% 0.010 275` | Disabled label on dark. |
| `--aw-color-ash-300`        | `#9A9AA3` | `68% 0.008 275` | Muted body on dark. |

**Usage covenant**: at any zoom, ≥90% of pixels in a meaningful surface must come from `abyss` through `charcoal-500`. The two "hint" blacks (ink-umber, midnight-slate) are restricted to subtle warmth/coolness bias **inside a texture or noise layer**, never flat fills.

#### 3.2.2 Stark Contrast Edge (primary use: primary text on dark, gestural marks, stark edges — dopamine anchor)

| Token | Hex | Role |
|---|---|---|
| `--aw-color-bone-50`   | `#FAF8F2` | Purest stark edge (rare, ≤2% surface area) |
| `--aw-color-bone-100`  | `#F0EDE3` | Primary body text on obsidian |
| `--aw-color-bone-200`  | `#E3DFD2` | Secondary text on obsidian |
| `--aw-color-ash-cream` | `#C9C4B5` | Tertiary text, subtitles |
| `--aw-color-pale-fog`  | `#AFA99A` | Muted editorial voice |

Stark edges are the sole carrier of high-contrast dopamine. They replace what jewels did in v2.0. They must **never** wash across more than 8% of a meaningful surface — they are edges, strokes, gestures, type. Not fills.

#### 3.2.3 Metallic Threads (primary use: borders, fine detail, refractive glints — 1–2px hairlines, text accents at ≥14px)

| Token | Hex | Role |
|---|---|---|
| `--aw-color-silver-thread`  | `#B5B2AC` | Default metallic hairline |
| `--aw-color-silver-deep`    | `#6D6B66` | Shadowed silver |
| `--aw-color-chrome-glint`   | `#D6D3CC` | Brightest metallic refraction |
| `--aw-color-platinum-300`   | `#E3E0DA` | Rare luxury glint (≤1% surface area) |
| `--aw-color-gunmetal-500`   | `#4A4A52` | Structural metallic weight |
| `--aw-color-gunmetal-700`   | `#2E2E36` | Gunmetal shadow |

Metallics are the *only* non-black, non-bone chroma allowed. They're what makes the void feel luxurious rather than austere.

#### 3.2.4 Restricted Ember (absolute last-resort chromatic — destructive actions + critical system alerts ONLY)

| Token | Hex | Role |
|---|---|---|
| `--aw-color-ember-danger`  | `#6B1F1F` | Destructive action / critical error fill |
| `--aw-color-ember-edge`    | `#A23535` | Destructive-action edge + icon stroke |

The ember palette exists **only** to meet WCAG status-differentiation requirements for destructive UX. It must never be used decoratively, in marketing, on brand surfaces, or in data visualization. If a designer is tempted to use it outside `role="alert"` or a confirmed-destructive button, the answer is no — use tone, iconography, and typography weight instead.

#### 3.2.5 Refractive Glint Layer (primary use: rare generative/motion highlights, metallic light-bends — max 2% of surface area)

| Token | Hex | Role |
|---|---|---|
| `--aw-color-glint-cold`  | `#C9D1D6` | Cold-spectrum refraction (near-silver) |
| `--aw-color-glint-warm`  | `#D6CFC2` | Warm-spectrum refraction (near-bone) |
| `--aw-color-glint-ghost` | `#E8E5DE` | Ghost refraction highlight |

No saturated hues. All glints sit within the grayscale-to-bone spectrum, distinguished only by micro temperature shifts. Used for prism edges on Tier-3 glass, hero motif shimmers, and focus-state light-through-void effects.

#### 3.2.6 Semantic Tokens (use these in components, not raw palette values)

```css
/* Surfaces */
--aw-bg-canvas: var(--aw-color-obsidian-800);   /* page base */
--aw-bg-surface: var(--aw-color-obsidian-900);  /* recessed surface */
--aw-bg-sunken: var(--aw-color-abyss);          /* deepest sunken */
--aw-bg-raised: var(--aw-color-jet-600);        /* cards at rest */
--aw-bg-elevated: var(--aw-color-jet-500);      /* cards on hover */
--aw-bg-inverse: var(--aw-color-bone-100);      /* extreme-contrast inversion — use sparingly */

/* Foreground */
--aw-fg-primary: var(--aw-color-bone-100);
--aw-fg-secondary: var(--aw-color-bone-200);
--aw-fg-muted: var(--aw-color-ash-cream);
--aw-fg-disabled: var(--aw-color-graphite-400);
--aw-fg-inverse: var(--aw-color-obsidian-900);  /* on inverse bg only */
--aw-fg-accent: var(--aw-color-chrome-glint);   /* the stark dopamine edge */
--aw-fg-link: var(--aw-color-bone-50);          /* underlined silver */

/* Borders */
--aw-border-subtle: rgba(240, 237, 227, 0.06);
--aw-border-default: rgba(240, 237, 227, 0.12);
--aw-border-strong: rgba(240, 237, 227, 0.24);
--aw-border-silver: var(--aw-color-silver-thread);
--aw-border-glint: rgba(214, 211, 204, 0.35);

/* Status (tonal-first, ember reserved for danger only) */
--aw-status-success: var(--aw-color-platinum-300); /* paired with ✓ iconography */
--aw-status-info:    var(--aw-color-chrome-glint); /* paired with ◐ iconography */
--aw-status-warning: var(--aw-color-silver-thread);/* paired with △ iconography */
--aw-status-danger:  var(--aw-color-ember-edge);   /* only chromatic status */
```

**Status design covenant**: Because four of the five status tokens are tonal siblings, every status treatment **must** pair with a unique icon shape + a typography weight shift. Color alone never carries status.

### 3.3 Typography Tokens

**Type families:**
```css
--aw-font-display: "Gotham", "Montserrat", "Work Sans", system-ui, sans-serif;
--aw-font-body: "Neue Haas Grotesk", "Helvetica Neue", Helvetica, Arial, system-ui, sans-serif;
--aw-font-mono: "JetBrains Mono", "SF Mono", "Berkeley Mono", ui-monospace, monospace;
--aw-font-etched: "Gotham", "Montserrat", system-ui, sans-serif; /* rare, for void pull quotes — always italic, always ultralight */
```

**Scale (modular, 1.250 major third on desktop, 1.200 minor third on mobile):**

| Token | Desktop | Mobile | Line-height | Letter-spacing | Weight |
|---|---|---|---|---|---|
| `--aw-text-display-2xl` | 84px / 5.25rem | 52px | 1.00 | -0.04em | 200 |
| `--aw-text-display-xl`  | 64px / 4rem    | 42px | 1.02 | -0.035em | 250 |
| `--aw-text-display-lg`  | 48px / 3rem    | 34px | 1.06 | -0.03em | 300 |
| `--aw-text-display-md`  | 36px / 2.25rem | 28px | 1.12 | -0.02em | 300 |
| `--aw-text-display-sm`  | 28px / 1.75rem | 24px | 1.2  | -0.015em | 400 |
| `--aw-text-body-lg`     | 18px / 1.125rem| 17px | 1.6  | 0.005em | 400 |
| `--aw-text-body-md`     | 16px / 1rem    | 16px | 1.65 | 0.01em | 400 |
| `--aw-text-body-sm`     | 14px / 0.875rem| 14px | 1.55 | 0.02em | 400 |
| `--aw-text-caption`     | 12px / 0.75rem | 12px | 1.45 | 0.08em | 500 |
| `--aw-text-micro`       | 10px / 0.625rem| 10px | 1.4  | 0.14em | 600 |

**Typographic bleak rules:**
- Display weights skew ultralight (200–300) — extreme thin type floating over void is the house voice.
- Body weights stay regular. Never bold body copy; emphasis via italic or all-caps caption.
- Letter-spacing on display is tighter than v2.0; on caption/micro it is looser. Both heighten extremism.
- Display uses the Gotham stack (`--aw-font-display`). Body uses the Neue Haas Grotesk stack (`--aw-font-body`). Mono is for code, data, technical specs only. Etched is reserved for ≤1 use per page, always italic, always ≥ 28px, always ultralight (200).

### 3.4 Spacing Scale (4px base)

```css
--aw-space-0:  0;
--aw-space-px: 1px;
--aw-space-0-5: 2px;
--aw-space-1:  4px;
--aw-space-2:  8px;
--aw-space-3:  12px;
--aw-space-4:  16px;
--aw-space-5:  20px;
--aw-space-6:  24px;
--aw-space-8:  32px;
--aw-space-10: 40px;
--aw-space-12: 48px;
--aw-space-16: 64px;
--aw-space-20: 80px;
--aw-space-24: 96px;
--aw-space-32: 128px;
--aw-space-40: 160px;
--aw-space-48: 192px;
--aw-space-64: 256px;
```

**Rhythm rules (bleak spacing skews wider than v2.0):**
- Paragraph spacing: `--aw-space-4`.
- Section spacing (within a view): `--aw-space-20` minimum desktop, `--aw-space-12` mobile.
- Hero-to-content: `--aw-space-32` desktop / `--aw-space-16` mobile. Void breath is extreme.
- Never use values outside this scale. No `15px`, no `37px`.

### 3.5 Radii

```css
--aw-radius-none: 0;              /* preferred for extremism moments */
--aw-radius-sm: 2px;              /* tighter than v2.0 */
--aw-radius-md: 6px;
--aw-radius-lg: 12px;             /* default component radius */
--aw-radius-xl: 20px;
--aw-radius-2xl: 32px;
--aw-radius-pill: 9999px;
--aw-radius-void-a: 63% 37% 54% 46% / 55% 48% 52% 45%;
--aw-radius-void-b: 38% 62% 41% 59% / 44% 39% 61% 56%;
```

**Default component radius:** `--aw-radius-lg` (12px). Sharp 0-radius corners are encouraged on architectural surfaces (hero panels, modals in extreme mode). Pills reserved for tags, avatars, status dots. Void radii reserved for decorative biomorphic masks, never interactive controls.

### 3.6 Shadow & Elevation System

Aetherweave v3.0 shadows are **deep black, sharp, and high-contrast**. No warm cast. Shadows now also carry a secondary hairline glint on top-edge for luxury definition against the void.

```css
--aw-shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.55);
--aw-shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.60), 0 0 0 1px rgba(240, 237, 227, 0.04);
--aw-shadow-md: 0 10px 28px rgba(0, 0, 0, 0.70), 0 0 0 1px rgba(240, 237, 227, 0.06);
--aw-shadow-lg: 0 22px 52px rgba(0, 0, 0, 0.80), 0 0 0 1px rgba(240, 237, 227, 0.08);
--aw-shadow-xl: 0 40px 96px rgba(0, 0, 0, 0.88), 0 0 0 1px rgba(240, 237, 227, 0.10);

/* Specialty: void inset for sunken surfaces */
--aw-shadow-inset-void: inset 0 2px 8px rgba(0, 0, 0, 0.70);

/* Specialty: silver thread outline for luxury emphasis (use sparingly) */
--aw-shadow-silver-thread: 0 0 0 1px rgba(181, 178, 172, 0.45), 0 12px 32px rgba(0, 0, 0, 0.75);

/* Specialty: chrome-glint top highlight — signature dopamine hairline on raised surfaces */
--aw-shadow-chrome-glint: inset 0 1px 0 rgba(214, 211, 204, 0.14);

/* Focus: metallic halo around focused element */
--aw-shadow-focus: 0 0 0 2px var(--aw-color-chrome-glint), 0 0 0 5px rgba(214, 211, 204, 0.22);
```

**Elevation map:**
| Level | Token | Use |
|---|---|---|
| 0 | none | Inline text, inherent-flow elements |
| 1 | `--aw-shadow-xs` | Subtle borders, resting inputs |
| 2 | `--aw-shadow-sm` + chrome-glint | Cards at rest |
| 3 | `--aw-shadow-md` + chrome-glint | Cards on hover, dropdowns |
| 4 | `--aw-shadow-lg` | Modals, popovers |
| 5 | `--aw-shadow-xl` + silver-thread | Full-screen sheets, hero overlays |

### 3.7 Blur & Refraction Tokens (Dark Liquid Glass foundation)

```css
--aw-blur-xs: 4px;
--aw-blur-sm: 12px;
--aw-blur-md: 24px;
--aw-blur-lg: 44px;
--aw-blur-xl: 72px;

--aw-saturate-glass: 0.6;   /* DESATURATE — v3.0 pulls color OUT of what's behind */
--aw-brightness-glass: 0.58; /* DARKEN what's refracted */
--aw-contrast-glass: 1.18;   /* Boost contrast for dopamine edge */
```

Dark liquid glass inverts v2.0's glass philosophy: rather than brightening and saturating what's beneath, v3.0 **pulls everything toward the void**, then stakes high-contrast edges and hairlines. What sits behind a panel becomes a shadow of itself — the panel's chrome-glint edge is the hero.

### 3.8 Z-index Scale

```css
--aw-z-hide: -1;
--aw-z-base: 0;
--aw-z-raised: 10;
--aw-z-dropdown: 100;
--aw-z-sticky: 200;
--aw-z-overlay: 300;
--aw-z-modal: 400;
--aw-z-popover: 500;
--aw-z-toast: 600;
--aw-z-tooltip: 700;
--aw-z-debug: 9999;
```

### 3.9 Breakpoints

```css
--aw-bp-xs:  480px;
--aw-bp-sm:  640px;
--aw-bp-md:  768px;
--aw-bp-lg:  1024px;
--aw-bp-xl:  1280px;
--aw-bp-2xl: 1536px;
--aw-bp-3xl: 1920px;
```

Mobile-first. Media queries use `min-width` only.

### 3.10 Content Width Tokens

```css
--aw-width-prose: 64ch;        /* tighter than v2.0 for extremism */
--aw-width-narrow: 640px;
--aw-width-content: 960px;
--aw-width-wide: 1200px;
--aw-width-full: 1440px;
--aw-width-cinema: 1760px;
```

### 3.11 Opacity Scale

```css
--aw-opacity-0: 0;
--aw-opacity-3: 0.03;
--aw-opacity-6: 0.06;
--aw-opacity-12: 0.12;
--aw-opacity-24: 0.24;
--aw-opacity-48: 0.48;
--aw-opacity-72: 0.72;
--aw-opacity-92: 0.92;
--aw-opacity-100: 1;
```

Micro-opacities (3, 6, 12) are critical to bleak extremism — they're how you layer 10+ near-black strata without mud.

---

## 4. AETHERWEAVE VISUAL LANGUAGE

### 4.1 The Seven-Elements Rule (Bleak Edition)
Every meaningful surface (page, hero, major section, hero product card) must contain **at least 5** of these 7 elements. Minor surfaces (buttons, inputs) may carry fewer, inherited from context.

1. **Layered void translucency** — 4+ overlapping planes of near-black with blur or opacity differentiation.
2. **Organic-geometric extremism** — a sharp grid/tessellation intersecting a biomorphic void flow.
3. **Metallic thread** — a hairline silver/chrome/platinum detail (1–2px).
4. **Rhythmic repetition with variation** — subtle dot fields, etched strokes, radial pulses in charcoal-on-jet that pulse like a heartbeat.
5. **Obsidian dominance + stark edge** — ≥90% obsidian surface area with stark bone/chrome accents ≤8%.
6. **Gestural void mark** — a hand-drawn, brushstroke, or calligraphic element disappearing into darkness.
7. **Refractive glint** — a singular light-through-void micro-highlight (platinum or chrome).

### 4.2 Composition: the 8-to-18 Layer Rule (raised from v2.0)
Hero surfaces carry **8 to 18** distinct strata. Count includes: abyss wash, noise grain, impasto ridge, pattern layer, motif layer(s), dark glass panel, foreground content, metallic thread, gestural overlay, refractive glint, void dot-field, edge-mask.

Fewer than 8: feels flat — add depth.
More than 18: feels chaotic — consolidate.

### 4.3 Texture System (Extreme Tactility)
Every Aetherweave surface carries micro-texture. Use at least **two** of these per meaningful surface:

- **Fractal noise** — `0.06` opacity fractal noise SVG, `mix-blend-mode: overlay` on dark. (Heavier than v2.0's 0.04 — bleak texture is the voice.)
- **Woven thread illusion** — 45°/135° 1px silver-thread lines at `0.04` opacity.
- **Impasto void ridges** — layered radial gradients in near-blacks at low opacity creating matte depth.
- **Sgraffito etch** — sparse 1px bone-100 lines at `0.06` opacity, rotated randomly (scratched into the void).
- **Ink bleed in void** — radial blur spots in `obsidian-700` at `0.12` opacity on `abyss`.
- **Metallic grain** — 1px silver/chrome specks at `0.05` opacity, simulating refractive flecks.

**Reference CSS — fractal noise overlay on dark:**
```css
.aw-texture-void-grain::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('/textures/aw-noise-fractal.svg');
  mix-blend-mode: overlay;
  opacity: 0.06;
  pointer-events: none;
  z-index: 1;
}
```

### 4.4 Negative Space ("The Abyss")
Negative space in v3.0 is not blank — it is the void. It actively carries tension.

- Minimum hero abyss: **45%** of viewport height untouched by primary content.
- Minimum section abyss: **25%** of section width on at least one side.
- Typography abyss: min `--aw-space-8` above any heading `display-md` or larger.

Abyss areas may carry a single sub-5% opacity textural element (noise, lone dot-field, distant gestural mark) — but must never hold secondary content. The void is sacred.

### 4.5 Motif Library (invoke by name — all rendered in obsidian extremism)

| Motif ID | Description | Typical use |
|---|---|---|
| `aw-motif-void-prism` | Near-black light-bending planes with chrome-glint edges, 7–12 rays | Hero focal points |
| `aw-motif-sonic-void` | Rhythmic wave lines carved through blackness, variable amplitude | Audio/music contexts |
| `aw-motif-abyss-migration` | Mehretu-esque layered trajectory lines flowing through dark | Data, journeys, systems |
| `aw-motif-dot-abyss` | Scattered dots in varying black densities, meditative | Background texture |
| `aw-motif-ink-void-flow` | Single continuous gestural line disappearing into dark | Accent, dividers |
| `aw-motif-shadow-tessellation` | Etched geometric repeat with 1–3 variations on jet ground | Borders, patterns |
| `aw-motif-ink-splash-void` | Organic ink bloom in charcoal-on-jet | Accent, backgrounds |
| `aw-motif-biomorph-shadow` | Amoeba/cell/leaf organic shape emerging from void | Containers, masks |
| `aw-motif-bricolage-void` | Collage of fragmented matte/gloss black rectangles | Cultural/archival feel |
| `aw-motif-refract-glint` | Singular platinum light-bend (extreme-rare) | Singular luxury moment |

All motifs are original inventions rendered in extreme black. Motifs are SVG assets stored at `/assets/motifs/{motif-id}.svg`. They accept CSS custom property color overrides via `currentColor` or `var(--aw-motif-color)` — which defaults to `var(--aw-color-charcoal-500)`.

---

## 5. DARK LIQUID GLASS SYSTEM

The refractive dark glass panel is Aetherweave v3.0's signature digital surface. Three tiers — all **frosted black**, desaturating and darkening what sits behind them.

### 5.1 Glass Tier 1 — Veil (subtlest)
Use: sticky headers, tooltips, subtle overlays.

```css
.aw-glass-veil {
  background: rgba(10, 10, 14, 0.62);
  backdrop-filter: blur(var(--aw-blur-sm))
                   saturate(var(--aw-saturate-glass))
                   brightness(var(--aw-brightness-glass))
                   contrast(var(--aw-contrast-glass));
  -webkit-backdrop-filter: blur(var(--aw-blur-sm))
                           saturate(var(--aw-saturate-glass))
                           brightness(var(--aw-brightness-glass))
                           contrast(var(--aw-contrast-glass));
  border: 1px solid rgba(240, 237, 227, 0.06);
  border-top-color: rgba(214, 211, 204, 0.14); /* chrome-glint top hairline */
  box-shadow: var(--aw-shadow-sm);
}
```

### 5.2 Glass Tier 2 — Pane (standard)
Use: cards, modals, dropdown content.

```css
.aw-glass-pane {
  background: linear-gradient(
    135deg,
    rgba(10, 10, 14, 0.78) 0%,
    rgba(5, 5, 8, 0.66) 100%
  );
  backdrop-filter: blur(var(--aw-blur-md))
                   saturate(var(--aw-saturate-glass))
                   brightness(var(--aw-brightness-glass))
                   contrast(var(--aw-contrast-glass));
  -webkit-backdrop-filter: blur(var(--aw-blur-md))
                           saturate(var(--aw-saturate-glass))
                           brightness(var(--aw-brightness-glass))
                           contrast(var(--aw-contrast-glass));
  border: 1px solid rgba(240, 237, 227, 0.10);
  border-top-color: rgba(214, 211, 204, 0.22);
  box-shadow: var(--aw-shadow-md), inset 0 1px 0 rgba(214, 211, 204, 0.12);
  border-radius: var(--aw-radius-lg);
}
```

### 5.3 Glass Tier 3 — Prism-Void (signature)
Use: hero panels, feature showcases, singular extremism moments. **Max 1 per view.**

```css
.aw-glass-prism-void {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(10, 10, 14, 0.82) 0%,
    rgba(29, 29, 37, 0.52) 50%,
    rgba(5, 5, 8, 0.78) 100%
  );
  backdrop-filter: blur(var(--aw-blur-lg)) saturate(0.4) brightness(0.5) contrast(1.25);
  border-radius: var(--aw-radius-xl);
  border: 1px solid transparent;
  background-clip: padding-box;
  box-shadow: var(--aw-shadow-xl), var(--aw-shadow-silver-thread);
}

.aw-glass-prism-void::before { /* monochrome refractive edge */
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  padding: 1px;
  background: conic-gradient(
    from 180deg at 50% 50%,
    var(--aw-color-glint-cold),
    var(--aw-color-silver-thread),
    var(--aw-color-platinum-300),
    var(--aw-color-gunmetal-500),
    var(--aw-color-glint-warm),
    var(--aw-color-glint-cold)
  );
  opacity: 0.35;
  -webkit-mask: linear-gradient(#000, #000) content-box, linear-gradient(#000, #000);
  mask: linear-gradient(#000, #000) content-box, linear-gradient(#000, #000);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

The prism-void ring is the only place where multiple metallic hues co-exist — forming a bleak rainbow across the grayscale-to-platinum spectrum. No chromatic hues enter this gradient.

### 5.4 Light-Inversion Glass (accessibility / extreme-contrast moment)
When `[data-theme="inverse"]` is active (Section 12.3 — a rare bone-dominant inversion), glass inverts to:
- Background `rgba(245, 243, 238, 0.72)` (bone-on-bone)
- Border `rgba(29, 29, 37, 0.24)` (jet hairline)
- Top-highlight `rgba(255, 255, 255, 0.55)`

### 5.5 Glass Fallback (no `backdrop-filter` support)
```css
@supports not (backdrop-filter: blur(1px)) {
  .aw-glass-veil,
  .aw-glass-pane,
  .aw-glass-prism-void {
    background: var(--aw-bg-raised);
    box-shadow: var(--aw-shadow-md);
    border-color: var(--aw-border-default);
  }
}
```

### 5.6 Glass Performance Rules
- **Never stack more than 2 backdrop-filter layers.** Nested blur is expensive and muddy.
- **Never use blur ≥ `--aw-blur-xl`** on scrollable content — kills FPS on mid-range devices.
- **Disable backdrop-filter** when `prefers-reduced-transparency: reduce` is set. Fall back to solid `--aw-bg-raised` with a chrome-glint top border.

---

## 6. LAYOUT SYSTEM

### 6.1 Grid
12-column fluid grid. Gutters scale with breakpoint:

| Breakpoint | Columns | Gutter | Margin |
|---|---|---|---|
| xs / sm | 4 | 16px | 16px |
| md | 8 | 20px | 24px |
| lg | 12 | 24px | 40px |
| xl / 2xl | 12 | 32px | 64px |
| 3xl | 12 | 40px | auto (capped at `--aw-width-cinema`) |

### 6.2 Container Pattern
```css
.aw-container {
  width: 100%;
  max-width: var(--aw-width-full);
  margin-inline: auto;
  padding-inline: var(--aw-space-4);
}
@media (min-width: 768px)  { .aw-container { padding-inline: var(--aw-space-6); } }
@media (min-width: 1024px) { .aw-container { padding-inline: var(--aw-space-10); } }
@media (min-width: 1536px) { .aw-container { padding-inline: var(--aw-space-16); } }
```

### 6.3 Section Rhythm
Every section has inherent vertical padding via tokens. Don't override with margin hacks. Abyss breath is wider than v2.0.

```css
.aw-section { padding-block: var(--aw-space-20); }
.aw-section--hero { padding-block: var(--aw-space-32) var(--aw-space-24); }
.aw-section--compact { padding-block: var(--aw-space-12); }
@media (min-width: 1024px) {
  .aw-section { padding-block: var(--aw-space-32); }
  .aw-section--hero { padding-block: var(--aw-space-48) var(--aw-space-40); }
}
```

### 6.4 Asymmetric Composition Rule
Aetherweave v3.0 layouts are **extremely asymmetrically balanced** — more often than centered. For hero sections, prefer 8/4 or 9/3 splits over 6/6. Center only for singular statement moments where the subject demands axis-dominance.

### 6.5 Architectural Edge Rule
Every full-bleed section carries one architectural edge: a 1px silver-thread hairline, a thin charcoal rule, or a vertical gutter of abyss. This edge defines the rhythm of the composition. Never ship a section without one.

---

## 7. TYPOGRAPHY SYSTEM

### 7.1 Hierarchy Rules
- **One display-2xl per view maximum.**
- Heading levels must descend sequentially in the DOM (h1 → h2 → h3). Skip levels only with `role="heading" aria-level`.
- Body copy default: `--aw-text-body-md`, `--aw-fg-primary`, measure capped at `--aw-width-prose` (64ch).
- Display weights default to ultralight (200–300). Never ship display copy in weight ≥ 400.

### 7.2 Display Treatment
Display text uses `--aw-font-display` (Gotham stack), extremely tight tracking, ultralight weight. It **floats in the void** — never shrink line-height below 1.00 at display-2xl. Display copy should feel almost disembodied.

```css
.aw-display-2xl {
  font: 200 var(--aw-text-display-2xl) / 1.00 var(--aw-font-display);
  letter-spacing: -0.04em;
  color: var(--aw-color-bone-100);
}
```

### 7.3 Pull Quotes (etched void treatment)
```css
.aw-pull-quote {
  font-family: var(--aw-font-etched);
  font-style: italic;
  font-weight: 200;
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  line-height: 1.35;
  color: var(--aw-color-ash-cream);
  border-inline-start: 1px solid var(--aw-color-silver-thread);
  padding-inline-start: var(--aw-space-6);
  max-width: 52ch;
}
```

### 7.4 Drop Caps (editorial void moments)
```css
.aw-dropcap::first-letter {
  font-family: var(--aw-font-display);
  font-weight: 200;
  font-size: 5.5em;
  line-height: 0.82;
  float: inline-start;
  padding-inline-end: var(--aw-space-3);
  padding-block-start: var(--aw-space-2);
  color: var(--aw-color-bone-50);
}
```

### 7.5 Links
```css
.aw-link {
  color: var(--aw-fg-link);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-decoration-color: rgba(181, 178, 172, 0.45); /* silver-thread */
  text-underline-offset: 0.18em;
  transition: text-decoration-color 220ms var(--aw-ease-silk),
              color 220ms var(--aw-ease-silk);
}
.aw-link:hover {
  color: var(--aw-color-chrome-glint);
  text-decoration-color: var(--aw-color-chrome-glint);
}
.aw-link:focus-visible { /* see Section 14.3 */ }
```

### 7.6 Numerals
Use tabular numerals for tables, data, timestamps, prices: `font-variant-numeric: tabular-nums`. Oldstyle numerals are prohibited in v3.0 — they introduce organic warmth that conflicts with extremism. Only lining + tabular numerals.

### 7.7 All-Caps Caption Treatment (signature)
Caption and micro tiers default to all-caps for structural moments (eyebrow labels, section indicators, metadata):
```css
.aw-caption-eyebrow {
  font: 600 var(--aw-text-micro) / 1.4 var(--aw-font-body);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--aw-color-silver-thread);
}
```

---

## 8. COMPONENT LIBRARY

Every component is specified with: **anatomy, default state, all interactive states, variants, sizes, do's, don'ts, edge cases**. All components default to obsidian surfaces, bone text, silver-thread borders, chrome-glint hover.

### 8.1 BUTTON

#### Anatomy
`[optional leading icon] [label] [optional trailing icon]` — padding, radius, border, fill, shadow.

#### Variants
- **Primary (Void)** — filled obsidian-900, bone-100 text, 1px silver-thread border. The hero action.
- **Secondary (Etched)** — transparent fill, 1px silver-thread border, bone-200 text.
- **Tertiary / Ghost** — no border, no fill, label only in `--aw-fg-accent`.
- **Glass** — `.aw-glass-pane` fill, silver-thread border on hover.
- **Destructive** — ember-danger fill, bone-100 text (the ONLY chromatic button).
- **Link button** — renders as inline `.aw-link` semantically a button.

#### Sizes
| Size | Height | Padding-inline | Font | Icon size |
|---|---|---|---|---|
| `xs` | 28px | 10px | body-sm | 14px |
| `sm` | 36px | 14px | body-sm | 16px |
| `md` | 44px | 20px | body-md | 18px |
| `lg` | 52px | 28px | body-md | 20px |
| `xl` | 64px | 36px | body-lg | 24px |

#### States (all variants)
- **Default**
- **Hover** — elevation rise (+1 shadow step), chrome-glint top border intensifies, translateY(-1px), 220ms silk ease
- **Focus-visible** — 2px chrome-glint outline offset 3px + silver halo (see `--aw-shadow-focus`)
- **Active** — translateY(0), shadow drops to elevation-1
- **Disabled** — opacity 0.35, cursor not-allowed, no hover
- **Loading** — spinner replaces leading icon, label visible, aria-busy="true"

#### Primary (Void) button reference CSS
```css
.aw-btn-void {
  display: inline-flex;
  align-items: center;
  gap: var(--aw-space-2);
  height: 44px;
  padding-inline: var(--aw-space-5);
  border-radius: var(--aw-radius-lg);
  border: 1px solid rgba(181, 178, 172, 0.35);
  background: linear-gradient(180deg, var(--aw-color-obsidian-700) 0%, var(--aw-color-obsidian-900) 100%);
  color: var(--aw-color-bone-100);
  font: 500 var(--aw-text-body-md) / 1 var(--aw-font-body);
  letter-spacing: 0.02em;
  box-shadow: var(--aw-shadow-sm), inset 0 1px 0 rgba(214, 211, 204, 0.14);
  cursor: pointer;
  transition:
    transform 220ms var(--aw-ease-silk),
    box-shadow 220ms var(--aw-ease-silk),
    border-color 220ms var(--aw-ease-silk),
    background 220ms var(--aw-ease-silk);
}
.aw-btn-void:hover {
  transform: translateY(-1px);
  border-color: var(--aw-color-chrome-glint);
  box-shadow: var(--aw-shadow-md), inset 0 1px 0 rgba(214, 211, 204, 0.22);
  background: linear-gradient(180deg, var(--aw-color-jet-600) 0%, var(--aw-color-obsidian-800) 100%);
}
.aw-btn-void:active { transform: translateY(0); box-shadow: var(--aw-shadow-xs); }
.aw-btn-void:focus-visible {
  outline: 2px solid var(--aw-color-chrome-glint);
  outline-offset: 3px;
}
.aw-btn-void:disabled { opacity: 0.35; cursor: not-allowed; transform: none; }
```

#### Destructive button reference CSS
```css
.aw-btn-destructive {
  /* same structure as aw-btn-void, with ember fill */
  background: linear-gradient(180deg, var(--aw-color-ember-edge) 0%, var(--aw-color-ember-danger) 100%);
  border: 1px solid rgba(240, 237, 227, 0.24);
  color: var(--aw-color-bone-100);
}
```

#### Edge cases
- **Long label** → don't wrap buttons; if label > 24 chars, shorten or switch to link.
- **Icon-only** → set `aria-label`, add `aspect-ratio: 1`, same height as sized counterpart.
- **In a form** → must have `type="button"` unless it's the submit.
- **Adjacent buttons** → use `--aw-space-3` gap minimum.
- **Full-width** → only in mobile CTAs, single stack, never in rows.

### 8.2 INPUT / TEXT FIELD

#### Anatomy
`[label] [optional description] [leading-icon? input trailing-icon/action?] [helper text / error]`

#### States
Default → Hover → Focus → Filled → Error → Disabled → Read-only.

#### Reference CSS
```css
.aw-field-input {
  width: 100%;
  height: 44px;
  padding: 0 var(--aw-space-4);
  border-radius: var(--aw-radius-md);
  border: 1px solid var(--aw-border-default);
  background: var(--aw-color-obsidian-900);
  color: var(--aw-fg-primary);
  font: 400 var(--aw-text-body-md) / 1.4 var(--aw-font-body);
  box-shadow: var(--aw-shadow-inset-void);
  transition: border-color 180ms var(--aw-ease-silk), box-shadow 180ms var(--aw-ease-silk);
}
.aw-field-input::placeholder { color: var(--aw-fg-muted); }
.aw-field-input:hover { border-color: var(--aw-border-strong); }
.aw-field-input:focus-visible {
  outline: none;
  border-color: var(--aw-color-chrome-glint);
  box-shadow: 0 0 0 3px rgba(214, 211, 204, 0.22), var(--aw-shadow-inset-void);
}
.aw-field-input[aria-invalid="true"] {
  border-color: var(--aw-color-ember-edge);
  box-shadow: 0 0 0 3px rgba(162, 53, 53, 0.20);
}
.aw-field-input:disabled { opacity: 0.4; cursor: not-allowed; background: var(--aw-bg-sunken); }
```

#### Label & Helper Pattern
```html
<div class="aw-field">
  <label class="aw-field__label" for="email">EMAIL ADDRESS</label>
  <p class="aw-field__description">We'll never share this.</p>
  <input id="email" class="aw-field-input" type="email" aria-describedby="email-help" />
  <p id="email-help" class="aw-field__helper">Use the address linked to your account.</p>
</div>
```

Label is always visible (no placeholder-as-label), rendered as `.aw-caption-eyebrow` all-caps treatment. If space demands, use floating label variant — floating label animates from placeholder position to eyebrow position via 220ms silk ease.

#### Edge cases
- **Autofill** — override browser's yellow with `-webkit-box-shadow: 0 0 0 1000px var(--aw-color-obsidian-900) inset; -webkit-text-fill-color: var(--aw-fg-primary);`
- **Long text overflow** — `text-overflow: ellipsis` only on read-only; editable fields scroll horizontally.
- **Number inputs** — right-align, tabular-nums, disable native steppers with custom +/-.
- **Password visibility toggle** — trailing icon button, `aria-pressed`, switches `type` between `password` and `text`.

### 8.3 TEXTAREA
Same as input, but: `min-height: 120px; padding-block: var(--aw-space-3); resize: vertical;`.
Character counter if `maxLength` set: bottom-right, `--aw-text-caption`, turns ember-edge at 90% full.

### 8.4 SELECT / DROPDOWN
Custom only — never rely on native `<select>` for aesthetic parity. Built on a listbox pattern with full ARIA.

- Closed: styled like input, chevron trailing.
- Open: `.aw-glass-pane` panel, `--aw-shadow-lg`, max-height 280px, scrollable.
- Options: 44px height, hover `rgba(214, 211, 204, 0.06)`, selected `rgba(214, 211, 204, 0.14)` + silver-thread leading line (2px).

### 8.5 CHECKBOX & RADIO
- 20×20 box, `--aw-radius-sm` (checkbox), full pill (radio).
- Unchecked: 1.5px border `--aw-border-strong`, `--aw-color-obsidian-900` fill.
- Checked: filled `--aw-color-bone-100`, obsidian-900 checkmark (hand-drawn SVG, not geometric ✓). The inversion is the dopamine — a tiny bright square in the void.
- Focus: 3px chrome-glint ring, offset 2px.
- Disabled: opacity 0.35.
- Animation: 180ms silk ease for check mark path-length reveal.

### 8.6 SWITCH / TOGGLE
- 44×24px track.
- Off: `--aw-color-obsidian-700` track, graphite-300 thumb.
- On: `--aw-color-bone-100` track, obsidian-900 thumb with silver-thread hairline — extreme inversion.
- Thumb 20×20, 2px inset from track, translate animation 260ms silk ease.

### 8.7 CARD

#### Anatomy
`[optional media] [header: title + optional subtitle] [body] [optional footer]`

#### Variants
- **Flat (Etched)** — `--aw-bg-raised`, 1px `--aw-border-subtle`, no shadow.
- **Raised (Void)** — `--aw-shadow-sm` + chrome-glint inset, no border.
- **Glass** — Tier 2 glass.
- **Feature (Prism-Void)** — Tier 3 glass, silver-thread border, hero context only (max 1 per view).
- **Interactive** (clickable whole card) — hover raises `--aw-shadow-md`, translateY(-2px), chrome-glint border intensifies, 260ms.

#### Reference CSS
```css
.aw-card {
  position: relative;
  padding: var(--aw-space-6);
  border-radius: var(--aw-radius-lg);
  background: var(--aw-bg-raised);
  border: 1px solid var(--aw-border-subtle);
  box-shadow: var(--aw-shadow-sm), var(--aw-shadow-chrome-glint);
  overflow: hidden;
  isolation: isolate; /* prevents motif bleed */
}
.aw-card__title { font: 300 var(--aw-text-display-sm) / 1.2 var(--aw-font-display); color: var(--aw-fg-primary); letter-spacing: -0.015em; }
.aw-card__subtitle { font: 400 var(--aw-text-body-sm) / 1.4 var(--aw-font-body); color: var(--aw-fg-secondary); margin-block-start: var(--aw-space-1); }
.aw-card__body { margin-block-start: var(--aw-space-4); color: var(--aw-fg-primary); }
.aw-card__footer { margin-block-start: var(--aw-space-6); display: flex; gap: var(--aw-space-3); align-items: center; }
```

#### Aetherweave card embellishments (apply to feature cards)
- Silver-thread hairline along top edge (1px `--aw-color-silver-thread`, 40% opacity).
- Corner motif: `aw-motif-dot-abyss` or `aw-motif-ink-void-flow`, 10% opacity, absolute top-right, 80×80px.
- Fractal noise texture overlay (Section 4.3).
- Optional refractive glint: single `--aw-color-platinum-300` 2×2px dot in a non-obvious corner (Easter-egg dopamine).

### 8.8 MODAL / DIALOG

#### Structure
- Overlay: `rgba(0, 0, 0, 0.72)` + `backdrop-filter: blur(12px) saturate(0.5)`.
- Panel: `.aw-glass-pane`, max-width 560px (md), 720px (lg), 960px (xl), 100vw on mobile (bottom sheet).
- Padding: `--aw-space-8` desktop, `--aw-space-6` mobile.
- Header: title (`display-md` ultralight), close button top-right.
- Body: scrollable if overflow, with fade-to-abyss masks top/bottom when scrolled.
- Footer: right-aligned button cluster (LTR); stacked on mobile.

#### Entry animation
```
opacity: 0 → 1  (180ms linear)
scale: 0.96 → 1 (320ms silk-ease)
translateY: 16px → 0 (320ms silk-ease)
blur (backdrop): 0px → 12px (320ms silk-ease)
```
Overlay fades independently (180ms).

#### Exit
Reverse, 180ms for both.

#### Focus trap & a11y
- On open: move focus to first interactive element, or title (`tabindex="-1"`).
- Trap tab cycle within modal.
- Escape closes.
- Return focus to trigger on close.
- `role="dialog" aria-modal="true" aria-labelledby="…"`.

#### Edge cases
- **Nested modals** — allowed up to depth 2; increment z-index by 100. Don't double-blur the backdrop (the void stays singular).
- **Long content** — internal scroll; never scroll the page behind (lock body scroll).
- **Mobile** — bottom sheet with drag-to-dismiss handle (4×32px silver-thread pill at top).

### 8.9 TOAST / NOTIFICATION
- Position: top-right desktop, top-center mobile.
- Stack: newest at top, max 3 visible; older compress with -8px translateY each.
- Auto-dismiss: 5s default, 8s for warnings, indefinite for errors (destructive/ember states).
- Swipe-right to dismiss on touch.

Status variants carry a leading 3px vertical bar in status token color (silver-thread for info, platinum for success, silver-deep for warning, ember-edge for danger) **and** a 16px status icon. Never color-only.

### 8.10 TOOLTIP
- Trigger: hover 600ms delay, focus instant.
- Max-width 260px, `--aw-text-body-sm`, `.aw-glass-veil` bg, silver-thread border.
- Arrow: 6px, matches panel fill.
- Position: auto-flip based on viewport edge.
- Dismiss: mouseleave, Escape, blur.

### 8.11 NAVIGATION

#### Top Nav
- Height 72px desktop, 64px mobile.
- Sticky with `.aw-glass-veil` when scrolled > 20px.
- Logo left, primary links center (or left-adjacent), actions right.
- Active link: silver-thread underline, 2px, offset 6px.
- Hover link: color transitions bone-200 → chrome-glint, 180ms.
- A single 1px silver-thread bottom rule divides nav from content.

#### Mobile Nav
Hamburger → full-screen sheet with `.aw-glass-prism-void`, large display links (`display-md` ultralight on abyss), stagger-in animation 60ms delay between items.

#### Sidebar / Side Nav
- Width 264px.
- Collapsible to 72px (icons only).
- Active item: bone-100 background at 6% opacity, 3px silver-thread left border, text shifts to chrome-glint.

### 8.12 TABS
- Horizontal: label + 2px silver-thread underline for active, 240ms slide transition.
- Vertical: label + 3px chrome-glint left-border for active.
- Overflow: scroll horizontally with fade-to-abyss mask edges.
- Active label weight shifts from 400 → 500; inactive stays 400.

### 8.13 ACCORDION
- 1px `--aw-border-subtle` divider between items.
- Header: 56px min height, chevron trailing (stroke chrome-glint), rotates 180° on expand (260ms silk).
- Content: height auto-animation via `grid-template-rows: 0fr → 1fr` (modern) with `max-height` fallback.

### 8.14 TABLE
- Header: `--aw-bg-sunken`, `.aw-caption-eyebrow` treatment, silver-thread bottom border (1px).
- Rows: alternating `--aw-bg-canvas` and `--aw-bg-raised` (zebra at ~40% opacity differentiation).
- Row hover: chrome-glint at 4% opacity overlay.
- Row selected: 8% opacity + silver-thread left edge (3px).
- Numeric columns: tabular-nums, right-aligned.
- Sortable headers: chevron indicator (chrome-glint), entire cell clickable.
- Sticky first column + sticky header for wide tables.
- Mobile: collapse to card-per-row with label:value pairs.

### 8.15 AVATAR
- Sizes: 24, 32, 40, 48, 64, 96px.
- Circle by default; `--aw-radius-void-a` variant for brand moments.
- Border: 1.5px silver-thread for featured avatars.
- Fallback: initials in `--aw-font-display` ultralight, on an obsidian gradient bg derived from name hash (all gradients stay within `obsidian-900` → `jet-500` range — never chromatic).
- Status dot: bottom-right, 25% of avatar size, 2px abyss outline.

### 8.16 BADGE / TAG
- Pill shape, `--aw-space-1 --aw-space-3` padding, `--aw-text-caption` uppercase (eyebrow treatment).
- Variants: etched (transparent + silver-thread border), void (jet-500 fill), stark (bone-100 fill + obsidian-900 text — extreme inversion, max 2 per view), metallic (silver-thread fill + obsidian-900 text).
- Dismissible variant has trailing × with 20px hit area.

### 8.17 PROGRESS

#### Linear
- 4px height (default), 8px (prominent).
- Track: `--aw-color-obsidian-900`.
- Fill: silver-thread → chrome-glint gradient (left→right), with subtle shimmer animation (`aw-prism-shimmer`).
- Indeterminate: 35%-wide bar translates left→right, 1.8s ease-in-out infinite.

#### Circular
- Strokes 2px (sm, 20px), 3px (md, 40px), 4px (lg, 64px), all in `--aw-color-chrome-glint` over `--aw-color-obsidian-700` track.
- Start at 12 o'clock, clockwise.
- Indeterminate: rotates 1.4s linear + dash-array animates 1.4s ease-in-out.

### 8.18 SKELETON
- Shape matches content.
- Base: `--aw-color-obsidian-700`.
- Shimmer: 120° gradient sweep through `--aw-color-jet-500` → `--aw-color-jet-600`, 1.6s linear infinite.
- Fades in over 180ms when replacing content.

### 8.19 EMPTY STATE
- Centered.
- Illustration: Aetherweave motif (void-prism or biomorph-shadow) at 20% opacity, 160–240px, stroked in silver-thread.
- Title: `display-sm` ultralight bone-100, bleakly confident copy (never "No results"; prefer "Nothing in the void yet — step in.").
- Description: `body-md`, `--aw-fg-secondary`.
- Primary action button below.

### 8.20 ERROR STATE (in-page, not toast)
- Same structure as empty state.
- Motif: `aw-motif-ink-splash-void` with ember-edge stroke at 25% opacity (the single chromatic exception).
- Title uses bone-100 on `--aw-font-display` ultralight.
- Always offers retry + support link.

### 8.21 LOADING / BUSY
- Full-page: Aetherweave `aw-motif-void-prism` SVG, rotating 3s linear, with subtle pulsing scale 0.98→1.02, strokes in chrome-glint at 60% opacity.
- Inline: skeleton or spinner (circular progress).
- Button loading: see 8.1.

---

## 9. MOTION & ANIMATION SYSTEM

### 9.1 Easing Curves (all motion uses these — no defaults, no `ease`, no `linear` except for opacity crossfades)

```css
--aw-ease-silk:    cubic-bezier(0.22, 0.61, 0.36, 1.00);   /* default — everything */
--aw-ease-weave:   cubic-bezier(0.65, 0.00, 0.35, 1.00);   /* entrances */
--aw-ease-thread:  cubic-bezier(0.16, 1.00, 0.30, 1.00);   /* generous overshoot feel */
--aw-ease-prism:   cubic-bezier(0.76, 0.00, 0.24, 1.00);   /* dramatic reveal */
--aw-ease-hush:    cubic-bezier(0.25, 0.10, 0.25, 1.00);   /* exits, dismissals */
--aw-ease-void:    cubic-bezier(0.85, 0.00, 0.15, 1.00);   /* extremism reveal — v3.0 signature */
```

### 9.2 Duration Scale

```css
--aw-dur-instant: 80ms;   /* toggle flashes */
--aw-dur-quick:   180ms;  /* hover, focus, micro */
--aw-dur-base:    260ms;  /* most component motion */
--aw-dur-slow:    420ms;  /* modals, sheets */
--aw-dur-slower:  680ms;  /* page-level transitions */
--aw-dur-epic:    1400ms; /* hero entrances — longer in bleak */
```

### 9.3 Motion Principles
1. **Purpose** — every animation has a narrative reason (reveal, guide, confirm, delight).
2. **Anticipation** — pre-motion (micro pull-back) on large reveals.
3. **Overshoot sparingly** — thread ease only for brand/delight moments.
4. **Stagger** — lists stagger 40–80ms per item, max 8 items staggered.
5. **Crossfade opacity, transform everything else.** Never width/height animate where possible.
6. **Void-reveal** — major entrances emerge *from* obsidian (opacity 0 + scale 0.92 + blur 8px) rather than sliding in. The content condenses out of darkness.
7. **Chrome-glint finishing** — signature moves end with a 140ms chrome-glint hairline sweep across the edge of the revealed surface. This is the dopamine payoff.

### 9.4 Keyframe Library

```css
@keyframes aw-fade-in {
  from { opacity: 0; } to { opacity: 1; }
}

@keyframes aw-rise-in {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes aw-void-condense {
  from { opacity: 0; transform: scale(0.92); filter: blur(8px); }
  to   { opacity: 1; transform: scale(1);    filter: blur(0); }
}

@keyframes aw-prism-shimmer {
  0%   { background-position: -200% 50%; }
  100% { background-position: 200% 50%; }
}

@keyframes aw-void-pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50%      { opacity: 1;   transform: scale(1.02); }
}

@keyframes aw-gestural-draw {
  from { stroke-dashoffset: var(--aw-path-length); }
  to   { stroke-dashoffset: 0; }
}

@keyframes aw-refract-drift {
  0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg); }
  33%      { transform: translate3d(10px, -14px, 0) rotate(1.5deg); }
  66%      { transform: translate3d(-8px, 10px, 0) rotate(-1deg); }
}

@keyframes aw-spinner-sweep {
  0%   { stroke-dasharray: 1 150; stroke-dashoffset: 0; }
  50%  { stroke-dasharray: 90 150; stroke-dashoffset: -35; }
  100% { stroke-dasharray: 90 150; stroke-dashoffset: -125; }
}

@keyframes aw-chrome-glint-sweep {
  from { background-position: -120% 0; opacity: 0.0; }
  20%  { opacity: 0.8; }
  to   { background-position: 120% 0; opacity: 0.0; }
}
```

### 9.5 Signature Motion — "Void Condense"
The v3.0 page-load hero pattern, replacing v2.0's "Silk Settle":

1. Scene starts at full `--aw-color-abyss`.
2. Background obsidian layers fade in linearly over 680ms.
3. Noise + texture overlays fade to target opacity over 420ms (staggered 120ms after bg).
4. Gestural marks draw-in (`aw-gestural-draw`), staggered 80ms, 1400ms total.
5. Display type condenses out of void (`aw-void-condense`) with 260ms delay after marks complete, 680ms duration, `--aw-ease-void`.
6. Body + CTA condense 180ms after display, staggered 80ms.
7. Single chrome-glint sweep animates across primary CTA edge at 2100ms (`aw-chrome-glint-sweep`, 1200ms, runs once).
8. Motif refract-drift loop starts at 2400ms, 16s duration infinite.

Total orchestration: content **condenses out of the void** rather than settling onto a surface. The chrome-glint at the end is the dopamine.

### 9.6 Scroll-Triggered Reveals
Use IntersectionObserver at `threshold: 0.15`. Element receives `.aw-reveal--in-view` which triggers `aw-void-condense` with `--aw-ease-weave`, 680ms.

```css
.aw-reveal { opacity: 0; transform: scale(0.96) translateY(16px); filter: blur(4px); }
.aw-reveal--in-view {
  animation: aw-void-condense var(--aw-dur-slower) var(--aw-ease-weave) forwards;
}
```

Never animate every child — pick anchors. Too much scroll motion fatigues the extremism.

### 9.7 Hover Principles
- Shadow + translateY(-1px or -2px) + chrome-glint border intensify — never scale() on actionable elements (looks gimmicky).
- 220ms with silk ease.
- Feature cards may use `aw-chrome-glint-sweep` on gradient border hover (once per hover).

### 9.8 Reduced Motion Fallback (MANDATORY)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .aw-reveal { opacity: 1; transform: none; filter: none; }
  .aw-refract-drift { animation: none; }
}
```

Preserve opacity crossfades (≤ 120ms) for essential state changes.

### 9.9 Parallax
Use only on hero motifs. Max 20% translate on scroll. Always `will-change: transform` only during scroll. Disabled under reduced-motion.

---

## 10. IMAGERY & ICONOGRAPHY

### 10.1 Photography Direction
- Cool-void-biased white balance (slight blue-black skew, never warm).
- Dramatic single-source lighting — Rembrandt / chiaroscuro tradition.
- Subjects emerge from shadow; 60%+ of frame is near-black.
- Textural surfaces: black silk, matte leather, obsidian, basalt, volcanic stone, charcoal, carbon fiber, skin with sculptural shadow.
- Subjects framed asymmetrically (rule of thirds min).
- Shallow DOF acceptable; never heavy bokeh-blur effects.
- Color grade: crush blacks to true `#0A0A0E`, lift highlights only on edges (silver rim-light), desaturate globally by ~40%, add subtle film grain at 4% opacity.

### 10.2 Image Treatments
- **Default** — unadorned, `--aw-radius-lg` corners, 1px silver-thread border.
- **Etched** — 1px silver-thread outline, 4px abyss offset frame (double-void feel).
- **Woven** — image + subtle woven-thread overlay at 6% opacity, mix-blend-mode overlay.
- **Refracted** — image + radial prism-void mask at 10% opacity, chrome-glint edge sweep on hover.
- **Void-fade** — image fades to `--aw-color-abyss` on bottom 30% via linear-gradient mask.

### 10.3 Icons
- Line icons, 1.75px stroke (not 1px, not 2px — the half-px gives humanity even in extremism).
- Default stroke: `--aw-color-bone-200`. Muted: `--aw-color-ash-cream`. Active/hover: `--aw-color-chrome-glint`.
- 24×24 default, 20 and 16 variants allowed.
- Rounded corners (`stroke-linejoin: round`), rounded caps (`stroke-linecap: round`).
- Icon set: Phosphor (Regular or Duotone weights) as base, with Aetherweave custom icons overriding brand-specific needs.
- Never mix line and filled icons in the same context.
- Duotone variant: stroke `currentColor`, fill `currentColor` at 0.18 opacity.

### 10.4 Illustration Style
- Abstract, never literal.
- Invoke motif library (Section 4.5).
- Palette: strictly monochromatic — all illustrations render in the obsidian → bone → metallic spectrum.
- Vector (SVG) preferred for scalability; raster for photographic moments only.

---

## 11. RESPONSIVE & ADAPTIVE BEHAVIOR

### 11.1 Universal Rules
- Mobile-first CSS; enhance upward.
- All interactive targets ≥ 44×44px on touch devices.
- Hover states must never be required for functionality.
- Viewport-relative units (`vh`, `dvh`, `svh`) for full-height surfaces; prefer `dvh` where supported.

### 11.2 Breakpoint Behavior Matrix

| Component | xs/sm (mobile) | md (tablet) | lg+ (desktop) |
|---|---|---|---|
| Nav | Hamburger prism-void sheet | Condensed horizontal | Full horizontal |
| Grid | 1–2 col | 2–3 col | 3–4+ col |
| Hero type | display-xl (200wt) | display-xl (200wt) | display-2xl (200wt) |
| Modal | Bottom sheet | Centered dialog | Centered dialog |
| Card grid gap | `space-4` | `space-5` | `space-6` |
| Side nav | Hidden / overlay | Collapsed | Expanded |
| Table | Card-per-row | Horizontal scroll | Full grid |
| Abyss breath | 30% viewport min | 40% viewport min | 45% viewport min |

### 11.3 Fluid Typography
Display sizes use `clamp()`:
```css
--aw-text-display-2xl-fluid: clamp(2.75rem, 1.5rem + 4.5vw, 5.25rem);
```

### 11.4 Container Queries
Prefer container queries for components reused across layouts:
```css
.aw-card-container { container-type: inline-size; }
@container (min-width: 480px) { .aw-card { padding: var(--aw-space-8); } }
```

### 11.5 Touch / Pointer Adaptation
```css
@media (hover: hover) and (pointer: fine) { /* cursor-device styles */ }
@media (hover: none) and (pointer: coarse) {
  .aw-btn-void:hover { transform: none; } /* avoid phantom hover */
}
```

---

## 12. THEMING: DARK IS DEFAULT

### 12.1 Dark (default, canonical Aetherweave)
The obsidian palette from Section 3.2 IS the default theme. There is no "dark mode toggle" in v3.0 — the void is the baseline. Defined above as `:root`.

### 12.2 Inverse Theme ("Bleached Void" — accessibility / contrast-mode only)
A rare inversion used **only** for printable surfaces, accessibility preference (`prefers-contrast: more` + user opt-in), or regulated contexts. This is not a marketing theme.

```css
[data-theme="inverse"] {
  --aw-bg-canvas: var(--aw-color-bone-100);
  --aw-bg-surface: var(--aw-color-bone-50);
  --aw-bg-sunken: #E8E5DE;
  --aw-bg-raised: #FFFFFF;
  --aw-bg-elevated: #FFFFFF;
  --aw-bg-inverse: var(--aw-color-obsidian-900);

  --aw-fg-primary: var(--aw-color-obsidian-900);
  --aw-fg-secondary: var(--aw-color-graphite-400);
  --aw-fg-muted: var(--aw-color-graphite-300);
  --aw-fg-inverse: var(--aw-color-bone-100);
  --aw-fg-accent: var(--aw-color-obsidian-900);
  --aw-fg-link: var(--aw-color-obsidian-900);

  --aw-border-subtle: rgba(29, 29, 37, 0.06);
  --aw-border-default: rgba(29, 29, 37, 0.14);
  --aw-border-strong: rgba(29, 29, 37, 0.30);

  --aw-shadow-sm: 0 2px 6px rgba(29, 29, 37, 0.10), 0 1px 2px rgba(29, 29, 37, 0.06);
  --aw-shadow-md: 0 10px 26px rgba(29, 29, 37, 0.14), 0 2px 6px rgba(29, 29, 37, 0.08);
  --aw-shadow-lg: 0 22px 50px rgba(29, 29, 37, 0.18), 0 4px 12px rgba(29, 29, 37, 0.10);
}
```

Metallic threads remain identical — silver reads luxurious against both void and bleached ground. Ember-danger darkens to `#4A1313` in inverse for contrast.

### 12.3 High-Contrast Mode

```css
@media (prefers-contrast: more) {
  :root {
    --aw-border-subtle: rgba(240, 237, 227, 0.24);
    --aw-border-default: rgba(240, 237, 227, 0.45);
    --aw-fg-secondary: var(--aw-color-bone-50);
    --aw-fg-muted: var(--aw-color-ash-cream);
  }
  .aw-glass-veil, .aw-glass-pane, .aw-glass-prism-void {
    background: var(--aw-bg-raised);
    backdrop-filter: none;
    border: 2px solid var(--aw-border-strong);
  }
}
```

### 12.4 Theme Switching
- Only two themes exist: `default` (void) and `inverse` (bleached). There is no "light mode" in the traditional sense.
- Transition `background-color` and `color` for 260ms silk ease globally when theme changes.
- Persist choice in `localStorage`. `prefers-color-scheme` is **ignored** for Aetherweave brand surfaces — the void is intentional, not system-driven. For utility/admin/documentation contexts, respecting system preference is permissible.
- `prefers-contrast: more` → automatic high-contrast adjustment on top of whichever theme is active.

---

## 13. DENSITY & DATA CONTEXTS

Aetherweave v3.0 is extreme by default but must also serve **dense data** contexts (dashboards, admin, analytics) without losing the void aesthetic.

### 13.1 Density Modes

```css
[data-density="comfortable"] { /* default */ }
[data-density="compact"] {
  --aw-row-height: 36px;
  --aw-form-height: 36px;
  --aw-padding-scale: 0.75;
}
[data-density="spacious"] {
  --aw-row-height: 56px;
  --aw-form-height: 52px;
  --aw-padding-scale: 1.25;
}
```

### 13.2 Data Visualization Palette
Data viz in v3.0 is **strictly monochromatic with pattern differentiation**.

- **Sequential**: `obsidian-900` → `bone-100` (8 steps), light-through-void. Darkest to brightest.
- **Diverging**: `obsidian-900` → `charcoal-500` → `bone-100` (neutral midpoint is charcoal, not white).
- **Categorical (up to 8)**: achieved via combination of (1) monochrome step + (2) hatch/dot pattern. Eight patterns: solid, horizontal line, vertical line, 45° line, 135° line, dot, cross-hatch, diagonal weave. Each assigned to a fixed grayscale step.
- **Status in charts**: ember-edge used only for exceeded-threshold marks or critical alerts. All other status signaling is pattern + iconography.
- Never use pure red/green for success/failure in charts — pattern alone + monochrome signals.

### 13.3 Chart Style
- Gridlines: `--aw-border-subtle`, dashed 2/3.
- Axis labels: `--aw-text-caption`, `--aw-fg-muted`.
- Tooltips: `.aw-glass-pane`.
- Annotations: hand-drawn style via SVG filter (`<feTurbulence>` distortion on stroke), chrome-glint.
- Chart title: `display-sm` ultralight, `--aw-font-display`.
- Data-point focus: chrome-glint 2px ring with silver halo.

---

## 14. ACCESSIBILITY (NON-NEGOTIABLE)

### 14.1 Contrast
- Body text: **7:1** target (AAA), minimum 4.5:1.
- Large text (≥ 18.66px bold or 24px regular): 3:1 minimum.
- Non-text UI (focus rings, borders of form elements): 3:1.
- Test every Aetherweave color combination. `bone-100` on `obsidian-800` = 17:1 ✓. `ash-cream` on `obsidian-800` = 8.9:1 ✓. `soot-300` on `obsidian-800` = 3.2:1 ✗ (reserve for non-text decorative only).
- **Stark contrast is the house voice** — never pair near-black on near-black as functional text. Low-contrast moments are decorative motifs, not copy.

### 14.2 Focus
- Every interactive element has a visible focus state.
- Default focus: 2px chrome-glint outline, 3px offset, with `--aw-shadow-focus` silver halo.
- Never `outline: none` without replacement.
- Focus must not rely on color alone — outline width/offset + halo together guarantee visibility.

```css
.aw-focus-ring:focus-visible {
  outline: 2px solid var(--aw-color-chrome-glint);
  outline-offset: 3px;
  box-shadow: var(--aw-shadow-focus);
  border-radius: inherit;
}
```

### 14.3 Keyboard
- All interactive elements reachable via Tab.
- Tab order matches visual order.
- Escape dismisses overlays.
- Arrow keys navigate within composite widgets (menus, listboxes, tabs, carousels).
- Enter/Space activate buttons; Enter submits forms; Space toggles checkboxes.

### 14.4 Semantic HTML
- Use native elements first. `<button>` for buttons, `<a>` for links, `<input>` for inputs.
- ARIA is a supplement, never a replacement.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`.
- Headings form an outline — no skipped levels.

### 14.5 Screen Reader Considerations
- Decorative elements (motifs, textures, refractive glints): `aria-hidden="true"`.
- Icon buttons: `aria-label`.
- Live regions for toasts: `role="status"` (polite) or `role="alert"` (assertive).
- Loading states: `aria-busy="true"`.
- Form errors: `aria-describedby` links input to error message, `aria-invalid="true"`.

### 14.6 Motion & Transparency
- Honor `prefers-reduced-motion` — fall back to crossfades under 120ms.
- Honor `prefers-reduced-transparency` — disable backdrop-filter, use solid `--aw-bg-raised` + silver-thread border.

### 14.7 Status & Color-Independence
Because v3.0's palette is monochromatic, status signaling **never** relies on color alone:
- Success: platinum-300 tone + ✓ checkmark icon + weight shift.
- Info: chrome-glint tone + ◐ circle icon.
- Warning: silver-thread tone + △ triangle icon + weight shift.
- Danger: ember-edge (the sole chromatic) + ✕ cross icon + weight shift.

All four carry redundant signals. Color-blind users receive full information from tone + shape + weight.

### 14.8 Localization & Directionality
- Use logical properties: `padding-inline-start`, not `padding-left`. `margin-block-end`, not `margin-bottom`.
- All layout works in RTL. Mirror iconography where semantic (chevrons, back arrows, progress flows).
- Text allows growth — German/Finnish translations can be +40% character count. Don't hard-code widths.
- Dates, numbers, currency via `Intl` APIs.

---

## 15. EDGE CASES & DEFENSIVE DESIGN

### 15.1 Content Overflow
- **Long names** — truncate with ellipsis, tooltip shows full on hover/focus.
- **Long URLs** — break-all with `overflow-wrap: anywhere`.
- **Multi-line truncation** — `-webkit-line-clamp`, always paired with fade-to-abyss mask.
- **Zero content** — empty state.
- **One item in grid meant for many** — center or left-align gracefully, don't full-stretch.

### 15.2 Loading Sequences
- First paint under 100ms — critical CSS inline. First paint is `--aw-color-abyss` — the void is instant.
- Skeleton visible by 200ms.
- Real content by 1.5s (target); beyond 3s, show informational message with retry.
- Never flash of unstyled content (FOUC) — preload `--aw-font-display` and `--aw-font-body`.
- **Never flash a light-themed frame before dark loads.** If the dark theme must be injected by JS, block first paint with an inline `<style>` setting `html { background: #0A0A0E; }`.

### 15.3 Error Recovery
- Every async action offers retry.
- Destructive actions require confirmation (modal with `.aw-btn-destructive` + secondary-etched cancel, not instant undo only).
- Form errors inline, not summarized at top (unless > 5 errors, then summarize + inline).
- 404 / 500 pages are full Aetherweave void experiences, not apologetic disclaimers. Motif-led, bleak copy ("The path dissolved. Try another.").

### 15.4 Permission & Empty Data
- Never blame the user. Copy is confident, bleak but inviting, solution-oriented.
- Always show a path forward.

### 15.5 Extreme Viewports
- Test 320px width (smallest realistic mobile) — content must not horizontally scroll.
- Test 2560px+ (ultrawide) — content caps at `--aw-width-cinema` with decorative motifs + abyss filling margins.
- Test 200% zoom — text must remain readable, layouts don't break.

### 15.6 Slow Networks / Offline
- Critical content renders without JS.
- Service worker caches shell.
- Offline indicator in nav when connection lost (etched badge with silver-thread border).
- Graceful font fallback matches metrics — no layout shift.

### 15.7 Input Errors
- Validate on blur, not on each keystroke (except password strength).
- Helper text and error text share location; error supersedes.
- Never clear a form on error.

### 15.8 Print Styles
Print inverts to bleached void — void-on-paper is not printable.
```css
@media print {
  *, *::before, *::after { background: transparent !important; color: #000 !important; box-shadow: none !important; backdrop-filter: none !important; }
  html, body { background: #FFFFFF !important; color: #000000 !important; }
  .aw-nav, .aw-footer, .aw-toast, .aw-modal { display: none !important; }
  body { font-family: "Neue Haas Grotesk", Helvetica, Arial, sans-serif; }
  a::after { content: " (" attr(href) ")"; font-size: 0.85em; color: #555; }
  .aw-glass-veil, .aw-glass-pane, .aw-glass-prism-void { background: transparent !important; border: 1px solid #999 !important; }
}
```

---

## 16. CODE PATTERNS

### 16.1 Root Setup
```css
:root {
  color-scheme: dark;  /* browser chrome stays dark by default */
  /* All --aw-* tokens from Section 3 injected here */
}
html {
  font-family: var(--aw-font-body);
  background: var(--aw-bg-canvas);
  color: var(--aw-fg-primary);
  scroll-behavior: smooth;
}
body { min-height: 100dvh; line-height: var(--aw-text-body-md); }
*, *::before, *::after { box-sizing: border-box; }

/* Guarantee the void appears before any JS runs — prevents light-flash */
html { background: #0A0A0E; }
```

### 16.2 Utility Naming (if utility-first / Tailwind-like)
- Prefix all custom utilities `aw-`.
- Extend Tailwind theme with `aw-*` tokens; do not use Tailwind's default palette (which is too chromatic) in production components.

### 16.3 Tailwind config snippet
```js
// tailwind.config.js (conceptual)
theme: {
  colors: {
    obsidian: { 700:'#101016', 800:'#0A0A0E', 900:'#050508' },
    jet: { 500:'#1D1D25', 600:'#18181F', 700:'#13131A' },
    charcoal: { 400:'#2F2F3A', 500:'#252530' },
    graphite: { 300:'#4A4A55', 400:'#3A3A46' },
    soot: { 300:'#5F5F6B' },
    ash: { 300:'#9A9AA3', 400:'#7A7A85' },
    bone: { 50:'#FAF8F2', 100:'#F0EDE3', 200:'#E3DFD2' },
    silver: { thread:'#B5B2AC', deep:'#6D6B66' },
    chrome: { glint:'#D6D3CC' },
    platinum: { 300:'#E3E0DA' },
    gunmetal: { 500:'#4A4A52', 700:'#2E2E36' },
    ember: { danger:'#6B1F1F', edge:'#A23535' },
    // abyss is the default bg, not a utility color
  },
  fontFamily: {
    display: ['Gotham', 'Montserrat', 'Work Sans', 'system-ui', 'sans-serif'],
    body: ['Neue Haas Grotesk', 'Helvetica Neue', 'Helvetica', 'Arial', 'system-ui', 'sans-serif'],
  },
  fontWeight: {
    ultralight: 200, light: 300, regular: 400, medium: 500,
  },
  borderRadius: { sm:'2px', md:'6px', lg:'12px', xl:'20px', '2xl':'32px' },
  spacing: { /* 4px scale */ },
  boxShadow: { /* void shadows */ },
}
```

### 16.4 Component Authoring Checklist (for every new component)
- [ ] Uses only `--aw-*` tokens (no hex, no magic numbers).
- [ ] Has all states: default, hover, focus-visible, active, disabled, loading (where applicable).
- [ ] Keyboard operable.
- [ ] Screen-reader labeled.
- [ ] Works at 320px viewport.
- [ ] Works at 200% zoom.
- [ ] Works in `inverse` theme.
- [ ] Works with `prefers-reduced-motion`.
- [ ] Works with `prefers-reduced-transparency`.
- [ ] Works with `prefers-contrast: more`.
- [ ] Contrast tested (AAA for body, AA for everything else).
- [ ] Contains at least 1 Aetherweave embellishment (texture, silver thread, motif, chrome glint, or layered void translucency).
- [ ] No chromatic hue introduced outside the sanctioned ember (destructive only).
- [ ] Documented with usage example.

### 16.5 Motion code snippet (JS orchestration for Void Condense)
```js
function voidCondense(root) {
  const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) { root.classList.add('aw-settled'); return; }

  const layers = root.querySelectorAll('[data-aw-layer]');
  layers.forEach((el, i) => {
    el.style.animationDelay = `${i * 80}ms`;
    el.classList.add('aw-void-condense');
  });

  const paths = root.querySelectorAll('[data-aw-gesture]');
  paths.forEach((p, i) => {
    const len = p.getTotalLength();
    p.style.setProperty('--aw-path-length', len);
    p.style.strokeDasharray = len;
    p.style.animationDelay = `${300 + i * 80}ms`;
    p.classList.add('aw-gestural-draw');
  });

  const glintTarget = root.querySelector('[data-aw-chrome-sweep]');
  if (glintTarget) {
    glintTarget.style.animationDelay = '2100ms';
    glintTarget.classList.add('aw-chrome-glint-sweep');
  }
}
```

### 16.6 Flash-of-light prevention
```html
<!-- In <head>, BEFORE any CSS link -->
<style>html{background:#0A0A0E;color:#F0EDE3;}</style>
```

The void must render instantly. A flash of light is a brand failure.

---

## 17. PROJECT SCAFFOLDING

### 17.1 Recommended File Structure
```
/src
  /styles
    /tokens
      colors.css
      typography.css
      spacing.css
      motion.css
      shadows.css
    /base
      reset.css
      globals.css
      typography.css
    /components
      button.css
      card.css
      input.css
      modal.css
      …
    /patterns
      glass-void.css
      motifs.css
      textures-void.css
    /themes
      default-void.css
      inverse-bleached.css
      high-contrast.css
    aetherweave.css  (entry point, imports above)
  /assets
    /motifs    (svg motif library — rendered in charcoal/silver by default)
    /textures  (fractal noise, woven thread, impasto void)
    /fonts
    /icons
  /components
    [framework components, consume tokens]
```

### 17.2 Design Token Source of Truth
Tokens live in `tokens.json` (Design Tokens Community Group format) and are transformed via Style Dictionary to:
- CSS custom properties
- Tailwind theme config
- iOS (Swift)
- Android (XML)
- Figma variables

One source → many outputs. Never duplicate token values across platforms.

---

## 18. QUALITY & GOVERNANCE

### 18.1 Review Checklist (every PR / ticket / artifact)

**Aesthetic (Bleak Extremism)**
- [ ] 5+ Aetherweave elements on meaningful surfaces (Section 4.1).
- [ ] Palette: obsidian-dominant (≥90% surface area), stark edges ≤8%, metallics ≤2%.
- [ ] No chromatic hue outside sanctioned ember (destructive only).
- [ ] Silver/chrome/platinum thread present where appropriate.
- [ ] Layered void depth visible (4+ planes of black).
- [ ] Abyss breath respected (Section 4.4).
- [ ] At least one dopamine hook (chrome-glint sweep, refractive glint, hidden stratum).

**Technical**
- [ ] Only `--aw-*` tokens.
- [ ] Valid HTML, semantic landmarks.
- [ ] Accessibility checks pass (Axe, Lighthouse).
- [ ] Contrast audit clean (AAA for body).
- [ ] Motion honors reduced-motion.
- [ ] Transparency honors reduced-transparency.
- [ ] Works in default (void) + inverse (bleached).
- [ ] No flash-of-light before dark loads.
- [ ] Lighthouse performance ≥ 90 mobile.

**Narrative**
- [ ] Can I describe the invisible void this piece reveals?
- [ ] Does the motion earn its presence? Is there a chrome-glint payoff?
- [ ] Does this feel luxurious on black silk *and* immersive in dark-mode VR/AR?
- [ ] Does the piece provoke "can't look away" — or does it feel cold, sterile, or empty?

### 18.2 Don'ts (common regressions)
- **Don't use pure black `#000`** as a background — always `--aw-color-abyss` (`#000003`) or `--aw-color-obsidian-800`. Pure `#000` has no texture affordance.
- **Don't use pure white `#FFF`** anywhere. Always `--aw-color-bone-50` at absolute purest.
- **Don't introduce any chromatic hue** outside the sanctioned ember tokens.
- **Don't revert to warm earth tones** (terracotta, moss, ochre, umber, sand, cream-veil) — these are retired in v3.0.
- **Don't revert to jewel accents** (sapphire, emerald, ruby, amethyst) — these are retired.
- **Don't animate `height` / `width`** where `transform` or `grid-template-rows` suffices.
- **Don't nest 3+ glass panels.**
- **Don't use `ease` or `linear`** as default transition timing.
- **Don't use emoji** as functional icons.
- **Don't introduce a new font** without spec updates.
- **Don't use heavy display weights** (500+) — the ultralight void voice is sacred.
- **Don't ship cold sterility** — every void surface must have texture, gesture, or glint.
- **Don't use `!important`** except in reduced-motion/reduced-transparency/print overrides.

### 18.3 When to Deviate (governance)
Any deviation requires written justification in the PR, named approver, and a proposal to either codify (update this doc) or revert within the next sprint. Deviations never become informal norms. Introducing any chromatic hue outside ember-danger requires **two** approvers and an explicit opt-in at the artifact level.

### 18.4 Versioning
This spec is semver. Major = breaking token rename or removal, or aesthetic pivot (like v2→v3). Minor = additive tokens or components. Patch = fixes, clarifications. Each release has a migration guide.

### 18.5 v2.0 → v3.0 Migration Notes
- **Palette**: All warm-earth tokens (terracotta, moss, ochre, umber, sand, teal, cream-veil, ink-charcoal, midnight-loom) are **removed**. All jewel tokens (sapphire, emerald, ruby, amethyst) are **removed**. Prism-refraction tokens (aurora, fuchsia, saffron, indigo) are **removed**. Replace per the mapping:
  - `terracotta-500` brand → `obsidian-800` + chrome-glint accent
  - `cream-veil` canvas → `obsidian-800` canvas
  - `ink-charcoal` text → `bone-100` text (contrast inverts)
  - `gold-thread` → `silver-thread`
  - `ruby-500` danger → `ember-edge` danger
  - `sapphire-500` link → `bone-50` link (underline in silver-thread)
- **Shadows**: warm umber casts removed; all shadows rebuilt in deep black with chrome-glint inset.
- **Glass**: saturation/brightness philosophy **inverts** — v3.0 desaturates and darkens behind the panel.
- **Motion**: "Silk Settle" retired; "Void Condense" is the signature.
- **Typography**: display weights drop from 300–400 to 200–300 (ultralight). Script family replaced with "etched" (same stack, always ultralight italic).
- **Motifs**: "prism-burst" → "void-prism"; "sonic-wave" → "sonic-void"; "migration-map" → "abyss-migration"; "dot-field" → "dot-abyss"; "calligraphic-flow" → "ink-void-flow"; "tessellation" → "shadow-tessellation"; "ink-splash" → "ink-splash-void"; "biomorph" → "biomorph-shadow"; "bricolage" → "bricolage-void". A new "refract-glint" motif is added.

---

## 19. AI AGENT IMPLEMENTATION DIRECTIVES

When an AI agent is generating code, designs, or content for an Aetherweave v3.0 project:

1. **Load this document in full as context** before any generation.
2. **Never substitute values.** If a color isn't listed, ask — don't invent. The palette is strictly monochromatic + sanctioned metallics + ember-for-danger-only.
3. **Prefer composition over novelty.** Use existing components before proposing new ones.
4. **Justify new components** with: (a) what existing component fails, (b) which tokens it will use, (c) where it will live in the file structure.
5. **Output includes the Quality Checklist (18.1) filled in.**
6. **When ambiguity exists**, prefer: restraint > expansion; abyss > density; obsidian > bone; metallic-thread > flat-edge; layered > flat; bleak-with-texture > cold-and-empty.
7. **When copy is required** (labels, empty states, errors): confident, bleakly inviting, second-person, never apologetic unless genuinely warranted, never cute. The voice is modern, extreme, mysterious, commanding.
8. **When asked to match a reference not in this doc**, translate it into Aetherweave v3.0 tokens — don't import the reference's palette, typography, or motion as-is. If the reference is chromatic, strip it to monochrome.
9. **Assume reduced-motion, reduced-transparency, inverse theme, and RTL** are live in every output. Plan for them, don't retrofit.
10. **If the user requests "a pop of color,"** push back. The house style is monochrome. If the need is genuine (e.g., a user-uploaded image, a chart marker), confine it to the most restrained tonal treatment and document the deviation.
11. **If in doubt about originality** (does this echo an existing artist/brand too closely?), abstract further — Aetherweave synthesizes influences; it doesn't quote them. Black mono is extremely crowded territory; originality comes from layering + gesture + cultural abstraction, not from referencing a known look.
12. **Every output must trigger the dopamine test**: would a viewer want to stare longer? If it feels cold or empty, add texture, gesture, or a chrome-glint payoff. If it feels chaotic, consolidate layers.

---

## 20. APPENDIX: QUICK REFERENCE CARD

**Palette Stars** — Abyss `#000003` · Obsidian-800 `#0A0A0E` · Jet-500 `#1D1D25` · Charcoal-500 `#252530` · Bone-100 `#F0EDE3` · Silver-Thread `#B5B2AC` · Chrome-Glint `#D6D3CC` · Platinum-300 `#E3E0DA` · Ember-Edge `#A23535` (danger only)

**Default Motion** — 260ms `cubic-bezier(0.22, 0.61, 0.36, 1.00)`

**Default Radius** — 12px (tighter than v2.0; 0-radius encouraged for architectural surfaces)

**Default Shadow** — deep black cast with chrome-glint inset highlight

**Default Breath** — `--aw-space-20` between sections; ≥45% hero viewport as abyss

**Default Glass** — Tier 2 Pane (dark, desaturating, darkening, high-contrast edge)

**Signature Motion** — Void Condense on hero load, chrome-glint sweep as payoff

**Signature Detail** — 1px silver-thread hairline + chrome-glint top-inset on feature surfaces

**Signature Texture** — 6% fractal noise, overlay blend on obsidian

**Signature Type** — Ultralight (200) display, floating in the void

**Non-Negotiable** — Obsidian ≥90% · Stark edge ≤8% · Metallic ≤2% · Chromatic hue = 0% (except sanctioned ember)

---

*Aetherweave Design System — Living Document*
*Black Bleak Modern Extremism Pivot, 2026*
*Update proposals via the governance process (Section 18.3).*
