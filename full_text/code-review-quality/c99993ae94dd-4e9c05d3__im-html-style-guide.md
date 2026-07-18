---
name: im-html-style-guide
description: >
  This skill should be used when the user asks to create an HTML document,
  report, presentation, or proposal branded to Integral Media (IM), OR when
  formatting/styling a Google Sheet. Triggers include: "create HTML report",
  "branded document", "IM report", "IM presentation", "Integral Media
  document", "make a branded HTML page", "quarterly review document",
  "client report HTML", "SEO report for [client]", "create a styled HTML
  page", "HTML with IM branding", "format this sheet", "style the
  spreadsheet", "branded Google Sheet", "IM sheet formatting",
  "email signature", "create signature", "new starter signature",
  "Gmail signature", "team signature".
version: 1.5.0
---

# Integral Media — HTML Document Style Guide

To create an Integral Media branded HTML document, follow these rules.

## Getting Started

1. Read the template file: `${CLAUDE_PLUGIN_ROOT}/assets/im-document-template.html`
2. Duplicate it as your starting point
3. Replace the `<!-- TEMPLATE: Replace -->` markers with actual content
4. All documents must be **self-contained** — inline CSS, inline SVG logos, no external stylesheets

---

## SEO & Meta Tags

Any public-facing IM document must include Open Graph and Twitter Card meta tags in `<head>`:

```html
<!-- TEMPLATE: Replace all content="" values -->
<meta name="description" content="Page description for search engines">
<meta property="og:title" content="Page Title — Integral Media">
<meta property="og:description" content="Description for social sharing (1-2 sentences)">
<meta property="og:image" content="https://example.com/og.png">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title — Integral Media">
<meta name="twitter:description" content="Description for Twitter sharing">
<meta name="twitter:image" content="https://example.com/og.png">
<link rel="canonical" href="https://example.com/page">
```

**Rules:**
- `og:image` should be 1200x630px for best rendering across platforms
- `og:description` and `twitter:description` can differ (Twitter has tighter character limits)
- Canonical URL must be the production URL, not a staging/preview URL
- Internal documents (not deployed publicly) can skip this section

---

## Brand Colours

| Name | Hex | CSS Variable | Usage |
|------|-----|-------------|-------|
| **Sky Blue** | `#27C1F4` | `--sky` | Primary accent, links, highlights, timeline dots. Note: logo icon mark uses `#23B2EF` (original brand file shade) |
| **Deep Navy** | `#002F6C` | `--navy` | Hero/footer backgrounds, section titles, headings, step badges |
| **Charcoal** | `#333740` | `--charcoal` | Body text |
| **Cool Grey** | `#DCDDEB` | `--cool-grey` | Borders, dividers, tab bars |
| **White** | `#FFFFFF` | `--white` | Card backgrounds, hero text |

### Extended Palette (derived, not in brand guidelines)

These are utility colours that complement the brand:

| Name | Hex | CSS Variable | Usage |
|------|-----|-------------|-------|
| Navy Light | `#0a3d7a` | `--navy-light` | Hover states on navy |
| Sky Light | `#4fd1ff` | `--sky-light` | Hover states on sky |
| Sky Muted | `#e6f7fe` | `--sky-muted` | Code backgrounds, callout backgrounds |
| Slate | `#64748b` | `--slate` | Secondary text, nav links |
| Light | `#f1f5f9` | `--light` | Table header backgrounds |
| Lighter | `#f8fafc` | `--lighter` | Page background |
| Green | `#22c55e` | `--green` | Success states, checkmarks |
| Green Muted | `#dcfce7` | `--green-muted` | Success badges |
| Amber | `#f59e0b` | `--amber` | Warning/conditional states |
| Amber Muted | `#fef3c7` | `--amber-muted` | Warning badges |
| Red | `#ef4444` | `--red` | Error/danger states |
| Warm Gray | `#94a3b8` | `--warm-gray` | Muted decorative text |
| Red Muted | `#fee2e2` | `--red-muted` | Danger badges |

---

## Typography

### Font Stack

```css
--display: 'Julius Sans One', 'Trebuchet MS', sans-serif;
--sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
```

### Font Loading (recommended)

Use `<link rel="preload">` + `<link rel="stylesheet">` in `<head>`, **outside** the `<style>` block:

```html
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Julius+Sans+One&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Julius+Sans+One&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
```

**Why not `@import`?** `@import` inside `<style>` blocks rendering — the browser must download and parse the imported stylesheet before rendering any content. `<link>` loads fonts in parallel with the page.

**Fallback only** (if you must keep everything inside `<style>`):
```css
@import url('https://fonts.googleapis.com/css2?family=Julius+Sans+One&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
```

### Julius Sans One — Display Font

Used for: hero titles, section titles, section numbers, step number badges.

**Critical styling rules (must match logo usage):**
- **Always uppercase** (`text-transform: uppercase`)
- **Weight 400** (only available weight — do NOT use `font-weight: bold`)
- **Tight letter-spacing** — tighter than the font's natural spacing to match the logo's compact character spacing:
  - Hero h1 (large): `letter-spacing: -0.5px`
  - Section titles (medium): `letter-spacing: 0px`
  - Section numbers (decorative): `letter-spacing: 0px`
- **Never use for body text** — display only, for headings and labels

### Inter — Body Font

Used for: all body text, card headings (h3), paragraphs, lists, status card titles.

| Context | Size | Weight | Line Height |
|---------|------|--------|-------------|
| Body text | 15px | 400 | 1.7 |
| Card headings (h3) | 16px | 600 | default |
| Card/step body | 14.5px | 400 | 1.75 |
| Hero description | 16px | 300 | 1.7 |
| Status card body | 13.5px | 400 | 1.7 |

### JetBrains Mono — Monospace Font

Used for: labels, nav items, inline code, architecture diagrams, status badges, timeline dates.

| Context | Size | Weight | Letter Spacing |
|---------|------|--------|---------------|
| Labels / nav | 11px | 500 | 1.5–2.5px |
| Inline code | 12.5px | 500 | — |
| Architecture diagrams | 12.5px | 400 | — |
| Status badges | 10px | 500 | 0.5px |

---

## Logo

### CRITICAL — Do NOT regenerate the logo SVG

The IM logo SVG is **path-only** (all letters drawn as `<path>` outlines, no `<text>` elements, no font dependency). Earlier renders that produced garbled wordmarks (e.g. "ROVKTKILE IA" instead of "INTEGRAL MEDIA") were caused by the model writing `<text>` elements that depended on Bricolage Grotesque being installed at render time. That dependency does not exist in the canonical SVG.

**Rules — non-negotiable:**

- **Copy the SVG block below verbatim.** Do not regenerate, retype, paraphrase, simplify, or shorten the paths. Treat the path `d` attributes as opaque binary.
- **Never use `<text>` elements** anywhere in the logo SVG. If you find yourself typing `<text>` while building the logo, stop — you are doing it wrong.
- **Never use an external image file** for the logo — always inline this exact SVG block for self-contained documents.
- **Never modify logo colours** outside the two approved variants (colour on dark below; for light backgrounds, swap `fill="white"` on the wordmark paths to `fill="#002F6C"`).
- The SVG `viewBox` is `0 0 1208 142` — always preserve aspect ratio.

### Inline SVG (colour on dark background — for hero/footer)

Two variants exist:

1. **Header logo** — icon mark in Sky Blue (`#23B2EF`), wordmark in white. Height: 28px.
2. **Footer logo** — same SVG but styled with `opacity: 0.7` on the container and wordmark wrapped in `rgba(255,255,255,0.7)` via CSS. Height: 22px.

**Use this exact block (do not edit any path data):**

```html
<svg width="1208" height="142" viewBox="0 0 1208 142" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Integral Media">
<title>Integral Media</title>
<path d="M122.748 94.3069L106.15 139.418L35.686 3.69806L33.6758 0L74.2812 0.106144" fill="#23B2EF"/>
<path d="M165.181 0H134.199V142H165.181V0Z" fill="#23B2EF"/>
<path d="M26.7985 141.723H0.523438V81.779C0.523438 81.779 0.524017 55.1074 0.524017 53.4409H30.9802V141.723" fill="#23B2EF"/>
<path d="M15.4909 32.2727C24.0462 32.2727 30.9817 25.0482 30.9817 16.1364C30.9817 7.2245 24.0462 0 15.4909 0C6.9355 0 0 7.2245 0 16.1364C0 25.0482 6.9355 32.2727 15.4909 32.2727Z" fill="#23B2EF"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M1160.76 23.8361H1168.83L1207.88 116.934H1193.72L1181.42 87.3112H1147.93L1135.63 116.934H1121.84L1160.76 23.8361ZM1164.62 47.001C1164.41 47.511 1164.21 48.0035 1164 48.4785C1164 48.4868 1163.99 48.4952 1163.99 48.5036L1152.9 75.3179H1176.44L1165.37 48.6351C1165.11 48.0689 1164.86 47.5241 1164.62 47.001Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M1103.85 24.4333H1116.68V116.934H1103.85V24.4333Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M1013.34 24.4417C1021.54 23.8786 1029.83 23.5972 1038.19 23.5972C1052.13 23.5972 1064.01 27.9788 1073.57 36.845C1083.25 45.7524 1087.96 57.8334 1087.96 72.6546C1087.96 80.1182 1086.75 86.8835 1084.23 92.8826C1081.81 98.7626 1078.38 103.606 1073.88 107.291L1073.87 107.3L1073.86 107.31C1064.93 114.508 1053.87 118.009 1040.93 118.009C1032.77 118.009 1023.55 117.565 1013.28 116.682L1010.03 116.403V24.6685L1013.34 24.4417ZM1022.86 36.3236V105.05C1027.52 105.451 1033.53 105.658 1040.93 105.658C1051.5 105.658 1059.59 102.825 1065.56 97.4842C1071.43 92.2305 1074.65 84.1439 1074.65 72.5352C1074.65 61.083 1071.08 52.3263 1064.19 45.8581L1064.18 45.8518L1064.17 45.8455C1057.24 39.2724 1048.66 35.9488 1038.19 35.9488C1032.45 35.9488 1027.35 36.0747 1022.86 36.3236Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M949.691 24.4333H996.444V36.546H962.521V60.8648H993.219V72.858H962.521V104.821H997.758V116.934H949.691V24.4333Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M847.451 23.7166H856.167L883.696 89.1437C883.775 89.3174 883.854 89.4907 883.932 89.6635C884.01 89.5017 884.089 89.3376 884.169 89.1711C884.173 89.1637 884.176 89.1562 884.18 89.1487L914.863 23.7166H923.395L937.487 116.934H924.315L915.086 52.6829L887.125 112.515H879.268L854.89 53.494L845.275 116.934H832.195L847.451 23.7166ZM854.778 38.7136L852.913 34.2799L852.144 38.9783L854.778 38.7136Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M741.609 24.4333H754.439V104.583H793.737V116.934H741.609V24.4333Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M689.276 23.8361H697.342L736.391 116.934H722.237L709.934 87.3112H676.447L664.144 116.934H650.355L689.276 23.8361ZM693.134 47.001C692.928 47.5096 692.722 48.0009 692.517 48.4747C692.513 48.4843 692.508 48.494 692.504 48.5036L681.416 75.3179H704.957L693.881 48.6343C693.621 48.0684 693.372 47.5239 693.134 47.001Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M579.242 24.8012C586.857 24.2402 593.281 23.9555 598.495 23.9555C607.248 23.9555 614.766 26.2403 620.771 31.0575C627.001 35.9721 629.994 42.9619 629.994 51.5124C629.994 57.4291 628.25 62.9361 624.843 67.9577C622.377 71.5906 619.65 74.7105 616.648 77.2808C619.161 80.6986 622.088 84.6044 625.431 88.9996C629.784 94.539 632.523 97.9301 633.725 99.288C638.091 103.927 644.5 106.73 647 106L642 117.5C636.867 117.416 637.813 117.049 634.194 115.43L634.159 115.415L634.124 115.398C630.649 113.752 627.406 111.328 624.38 108.215L624.362 108.196L624.344 108.178C621.538 105.207 614.932 96.5546 604.691 82.5289C599.016 82.5018 593.713 82.3458 588.784 82.0596V116.934H575.955V25.0435L579.242 24.8012ZM588.784 36.4574V70.2608C593.838 70.527 598.587 70.6594 603.034 70.6594C604.952 70.6594 607.794 69.349 611.575 64.9628C615.006 60.9829 616.687 56.468 616.687 51.2735C616.687 46.0259 614.971 42.5632 611.895 40.2559L611.864 40.2329L611.834 40.2093C608.568 37.6479 604.002 36.1876 597.778 36.1876C595.136 36.1876 592.139 36.2768 588.784 36.4574Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M492.945 36.9267C501.461 27.6323 512.423 23 525.538 23C535.494 23 545.539 24.6603 555.661 27.9518L559.034 29.0488L555.313 40.4986L551.991 39.502C542.721 36.721 533.908 35.3515 525.538 35.3515C516.072 35.3515 508.538 38.6953 502.636 45.38C496.653 52.155 493.61 60.4929 493.61 70.624C493.61 80.5379 496.997 88.8331 503.812 95.7209C510.623 102.605 518.83 106.016 528.643 106.016C536.455 106.016 542.926 105.071 548.149 103.29V67.0761H560.978V110.343L559.301 111.384C551.587 116.172 541.123 118.367 528.285 118.367C514.955 118.367 503.538 113.757 494.254 104.559L494.242 104.547C484.966 95.2708 480.303 83.8922 480.303 70.624C480.303 57.3902 484.488 46.0776 492.945 36.9267Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M424.98 24.4333H471.733V36.546H437.81V60.8648H468.508V72.858H437.81V104.821H473.047V116.934H424.98V24.4333Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M346.602 24.4333H417.243V36.546H388.337V116.934H375.508V36.546H346.602V24.4333Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M258.809 23.7166H266.604L323.941 89.8193L323.958 89.8391C324.694 90.7129 325.398 91.5541 326.071 92.3627C326.062 91.5421 326.057 90.7062 326.057 89.855V24.4333H338.887V117.651H331.093L272.709 50.3881C272.707 50.3857 272.705 50.3833 272.703 50.3809C272.315 49.9385 271.939 49.5093 271.576 49.0933L271.638 51.7096V116.934H258.809V23.7166Z" fill="white"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M225.182 24.4333H238.011V116.934H225.182V24.4333Z" fill="white"/>
</svg>
```

**For light backgrounds:** use the same SVG but replace every `fill="white"` (on the wordmark paths only — paths 5 onward) with `fill="#002F6C"`. The first 4 paths (the icon mark) stay `#23B2EF`.

**Canonical source files** (if you need to verify the paths haven't drifted):

- Colour on dark: `assets/integralmedia_colour_dark_bg.svg`
- All-white: `assets/integralmedia_white.svg`
- Colour on light: `assets/integralmedia_colour.svg`
- All-black: `assets/integralmedia_black.svg`

### Favicon

Use this inline data URI in the `<head>`:

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 166 142'><path d='M122.748 94.3069L106.15 139.418L35.686 3.69806L33.6758 0L74.2812 0.106144' fill='%2323B2EF'/><path d='M165.181 0H134.199V142H165.181V0Z' fill='%2323B2EF'/><path d='M26.7985 141.723H0.523438V81.779C0.523438 81.779 0.524017 55.1074 0.524017 53.4409H30.9802V141.723' fill='%2323B2EF'/><path d='M15.4909 32.2727C24.0462 32.2727 30.9817 25.0482 30.9817 16.1364C30.9817 7.2245 24.0462 0 15.4909 0C6.9355 0 0 7.2245 0 16.1364C0 25.0482 6.9355 32.2727 15.4909 32.2727Z' fill='%2323B2EF'/></svg>">
```

---

## Page Structure

### Layout

- Max content width: `960px`, centred with `margin: 0 auto`
- Side padding: `40px` (desktop), `20px` (mobile)
- Page background: `--lighter` (`#f8fafc`)

### Hero (Header)

- Background: `--navy`
- Decorative glow: `radial-gradient` circle in top-right (Sky Blue at 15% opacity)
- Bottom accent: 3px gradient line (`sky → navy → sky`)
- Contains: logo, label (monospace, uppercase, sky colour with left dash), h1 (Julius Sans One), description paragraph

### Sticky Navigation

- White background, bottom border in cool grey
- Links: monospace, 11px, uppercase, 1.5px letter-spacing
- Hover: navy text + sky bottom border

### Sections

- Padding: `70px 0 20px`
- Section header: number (Julius Sans One, 56px, sky at 35% opacity) + title (Julius Sans One, 28px, navy, uppercase)
- Bottom border on header: 1px cool grey

### Cards

- White background, cool grey border, 10px border-radius
- Padding: 32px
- Subtle hover shadow: `0 4px 24px rgba(0,47,108,0.06)`
- Card headings: Inter 16px 600 with optional 28px icon square (navy background, 6px radius)

### Footer

- Background: `--navy`
- Logo at reduced opacity (0.7)
- "Last updated" text: monospace, 11px, white at 40% opacity

---

## Accessibility Baseline

Every IM document must include these accessibility features:

### Language

```html
<html lang="en-AU">
```

Use `en-AU` for Australian documents, not just `en`.

### Skip Link

Add before the hero, hidden until focused:

```html
<a href="#section-1" class="skip-link">Skip to content</a>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 16px;
  background: var(--navy);
  color: var(--white);
  padding: 8px 16px;
  border-radius: 0 0 6px 6px;
  font-family: var(--mono);
  font-size: 12px;
  text-decoration: none;
  z-index: 1000;
  transition: top 0.2s;
}
.skip-link:focus { top: 0; }
```

### Decorative Elements

Add `aria-hidden="true"` to purely visual elements so screen readers skip them:

```html
<span class="section-number" aria-hidden="true">01</span>
<span class="icon" aria-hidden="true"><svg>...</svg></span>
```

### SVG Logos

Add `role="img"` and a `<title>` to logo SVGs:

```html
<svg role="img" viewBox="0 0 1208 142" ...>
  <title>Integral Media</title>
  <!-- paths -->
</svg>
```

### Focus-Visible States

Add visible focus outlines on all interactive elements (nav links, buttons, CTAs):

```css
.nav-inner a:focus-visible {
  outline: 2px solid var(--sky);
  outline-offset: 2px;
  border-radius: 2px;
}
```

Use `focus-visible` (not `focus`) so outlines only appear on keyboard navigation, not mouse clicks.

---

## Component Reference

### Icons (Lucide — inline SVG only)

**NEVER use emoji HTML entities** (e.g. `&#9889;`, `&#128203;`) or Unicode emoji in documents. Use [Lucide](https://lucide.dev) icons as inline SVGs instead.

**How to use:** Place the SVG directly inside the `.icon` span. The CSS handles sizing and colour:

```html
<span class="icon">
  <svg viewBox="0 0 24 24"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>
</span>
```

**Rules:**
- Always use `viewBox="0 0 24 24"` (Lucide's standard viewBox)
- Do NOT set `width`, `height`, `stroke`, or `fill` on the `<svg>` — the CSS handles it (white stroke on navy background)
- Pick icons that clearly communicate the card's purpose — browse [lucide.dev/icons](https://lucide.dev/icons) for the full library
- Copy ONLY the inner `<path>`, `<rect>`, `<circle>`, `<line>`, `<polyline>` elements from Lucide — strip any wrapper markup

**Icon reference (1,703 available at [lucide.dev/icons](https://lucide.dev/icons) — most common below):**

| Purpose | Lucide name | SVG inner elements |
|---------|------------|----------|
| Check / done | `check` | `<path d="M20 6 9 17l-5-5"/>` |
| Check circle | `circle-check` | `<path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/>` |
| Close / dismiss | `x` | `<path d="M18 6 6 18"/><path d="m6 6 12 12"/>` |
| Info / overview | `info` | `<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>` |
| Warning | `triangle-alert` | `<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>` |
| Error / alert | `circle-alert` | `<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>` |
| Lightning / action | `zap` | `<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>` |
| Arrow right | `arrow-right` | `<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>` |
| External link | `external-link` | `<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>` |
| Search | `search` | `<path d="m21 21-4.34-4.34"/><circle cx="11" cy="11" r="8"/>` |
| Eye / visibility | `eye` | `<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>` |
| Settings / config | `settings` | `<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>` |
| Checklist / tasks | `clipboard-list` | `<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>` |
| Document / file | `file-text` | `<path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>` |
| Chart / data | `bar-chart-3` | `<path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>` |
| Trending up | `trending-up` | `<path d="M16 7h6v6"/><path d="m22 7-8.5 8.5-5-5L2 17"/>` |
| Star / rating | `star` | `<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>` |
| Calendar / schedule | `calendar` | `<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>` |
| Clock / time | `clock` | `<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>` |
| Mail / email | `mail` | `<path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/><rect x="2" y="4" width="20" height="16" rx="2"/>` |
| Phone | `phone` | `<path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/>` |
| Globe / web | `globe` | `<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>` |
| Download | `download` | `<path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/>` |
| Upload | `upload` | `<path d="M12 3v12"/><path d="m17 8-5-5-5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>` |
| Security / lock | `shield-check` | `<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>` |
| Link / connection | `link` | `<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>` |
| Users / team | `users` | `<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>` |

### Callout Box

```html
<div class="callout">
  <strong>Note:</strong> Important information here.
</div>
```

Sky muted background, 3px sky left border, rounded right corners.

### Step Cards (numbered)

```html
<div class="step">
  <div class="step-num">1</div>
  <h3>Step Title</h3>
  <p>Description text.</p>
</div>
```

White card with 88px left padding, navy number badge (40x40, 10px radius, Julius Sans One).

### Auto-list (inside steps)

```html
<div class="auto-list">
  <p>Section Label</p>
  <ul>
    <li>Item with green checkmark</li>
  </ul>
</div>
```

Lighter background, monospace label, green check marks.

### Timeline

Vertical timeline with sky-to-grey gradient line, dot markers, date labels in monospace.

### Status Cards (3-column grid)

Cards with coloured top borders (amber for warning, green for success, red for danger). Status badges use matching muted backgrounds.

### Registry Tables

Clean minimal tables with monospace uppercase headers, light background header row, subtle bottom borders.

### Tab Bar (spreadsheet visualisation)

Horizontal tabs mimicking a spreadsheet tab bar. Active tab in navy, hidden tabs dashed border.

### Architecture Diagram

Navy background code block with syntax highlighting via span classes: `.comment` (30% white), `.highlight` (sky), `.accent` (green #86efac), `.warm` (yellow #fcd34d).

### Inline Code

```css
code {
  font-family: var(--mono);
  font-size: 12.5px;
  background: var(--sky-muted);
  padding: 2px 7px;
  border-radius: 4px;
  color: var(--navy);
  font-weight: 500;
}
```

### Status Badges

```html
<span class="status-badge paused">paused</span>
<span class="status-badge active">active</span>
<span class="status-badge archived">archived</span>
```

### Conditional Labels

```html
<span class="cond">If condition</span>
```

Amber muted background, monospace uppercase, 10.5px.

### Pullquote

Large-format quote with optional attribution, for editorial/press content:

```html
<div class="pullquote">
  <blockquote>"Quote text here."</blockquote>
  <p class="attribution">— Speaker Name, Title</p>
</div>
```

Sky-muted background, 3px navy left border, rounded right corners. Attribution in monospace uppercase.

### Stats Bar

Horizontal grid of key numbers with labels:

```html
<div class="stats-bar">
  <div class="stat"><span class="stat-value">358</span><span class="stat-label">Occupations</span></div>
  <div class="stat"><span class="stat-value">13.9M</span><span class="stat-label">Workers</span></div>
</div>
```

4-column grid (2-column on mobile). Values in Julius Sans One, labels in monospace uppercase.

### Release Banner

Announcement bar for press releases:

```html
<div class="release-banner">For Immediate Release — 23 March 2026</div>
```

Navy background, sky text, monospace uppercase, centred.

### CTA Bar

Call-to-action strip with left text and right button:

```html
<div class="cta-bar">
  <p>Want to explore the data?</p>
  <a href="https://example.com">Visit the interactive map</a>
</div>
```

Navy background, flex row (stacks on mobile). Button in sky with navy text.

### Media Contact Card

Structured contact block for press materials:

```html
<div class="media-contact">
  <div>
    <h3>Media Contact</h3>
    <div class="contact-item">
      <span class="contact-label">Name</span>
      <span>Contact Person</span>
    </div>
  </div>
  <div>
    <div class="contact-item">
      <span class="contact-label">Email</span>
      <a href="mailto:contact@example.com">contact@example.com</a>
    </div>
  </div>
</div>
```

Navy background, 2-column grid (1 column on mobile). Sky labels, white text, underline links.

---

## Mobile Optimisation (MANDATORY)

**Every HTML document MUST render correctly on mobile devices.** This is non-negotiable — clients view these on phones and tablets.

### Required Meta Tag

Always include in `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### Primary Breakpoint: 768px

All components must adapt at `@media (max-width: 768px)`. The template includes these rules — preserve and extend them for any custom components you add.

### Core Mobile Rules

**Layout:**
- Container padding: `40px` → `20px`
- Cards padding: `32px` → `20px`
- Section padding-top: `70px` → `48px`

**Typography:**
- Hero h1: `42px` → `28px`
- Section number: `56px` → `40px`
- Section title: `28px` → `22px`

**Navigation:**
- Nav strip: `overflow-x: auto` with `-webkit-overflow-scrolling: touch`
- `flex-wrap: nowrap` so links scroll horizontally rather than stacking awkwardly
- Hide scrollbar visually: `.nav-inner::-webkit-scrollbar { display: none; }`

**Grids:**
- Status grid: `3 columns` → `1 column`
- Any multi-column grid: collapse to single column at 768px

**Steps:**
- Left padding: `88px` → `20px`
- Step number: reposition to `static` flow above the title (not absolute-left on small screens)

**Tables:**
- Wrap in a `div` with `overflow-x: auto` so wide tables scroll horizontally
- On mobile: reduce cell padding to `8px 10px`, header font to `9.5px`, body font to `12.5px`
- Cards containing tables: `padding: 20px 0` with `h3, p` getting `padding: 0 16px`
- Minimum touch target: `44px` height for any interactive table rows

**Images & SVGs:**
- `max-width: 100%; height: auto;` on all images
- Hero logo SVG: reduce height to `22px`

**Touch Targets:**
- All interactive elements (links, buttons): minimum `44px x 44px` hit area
- Nav links: `padding: 14px 12px` minimum

**Architecture Diagrams:**
- `overflow-x: auto` already set — also add `font-size: 11px` on mobile
- Consider `white-space: pre-wrap` for very long lines if content allows

### Secondary Breakpoint: 480px (optional)

For extra-small screens, consider:
- Hero h1: `28px` → `24px`
- Section header: stack number above title (`flex-direction: column; align-items: flex-start`)
- Card padding: `20px` → `16px`
- Tab bar tabs: `font-size: 10px; padding: 5px 10px`

### Testing Checklist

Before finalising any HTML document, mentally verify:
- [ ] No horizontal scroll on mobile (except intentional: tables, code blocks, tab bars)
- [ ] All text is readable without pinch-zooming (minimum 14px body text)
- [ ] Touch targets are large enough (44px minimum)
- [ ] Grids collapse to single column
- [ ] Navigation is usable (scrollable or wraps cleanly)
- [ ] Images/SVGs don't overflow their containers

---

## Print Styles

Add a `@media print` block at the end of the CSS:

```css
@media print {
  .nav-strip, .release-banner { display: none; }
  .hero { padding: 30px 0; }
  section { break-inside: avoid; }
  .card { break-inside: avoid; box-shadow: none; border: 1px solid var(--cool-grey); }
}
```

Hide navigation and banners, prevent page breaks inside cards, remove box shadows.

---

## Do's and Don'ts

### Do

- Use the template as a starting point
- Keep the hero + nav + sections + footer structure
- Use inline SVG for the logo (self-contained documents)
- Apply `text-transform: uppercase` and tight letter-spacing on Julius Sans One
- Use the extended colour palette for status/semantic colours
- Include the favicon data URI
- Use `lang="en-AU"` for Australian documents
- Add `aria-hidden="true"` on decorative section numbers and icon spans
- Include OG meta tags for any public-facing page
- Use font preload (`<link>`) instead of `@import` for fonts

### Don't

- **Use emoji or HTML entities for icons** — always use Lucide inline SVGs
- Use Julius Sans One for body text
- Bold Julius Sans One (`font-weight: 400` only)
- Add wide letter-spacing to Julius Sans One (tighten it to match the logo)
- Use colours outside the palette without good reason
- Link to external stylesheets (documents must be self-contained)
- Include any client-specific branding if the document is for a white-label partner (Higher Ranking, Purpose Digital). In that case, remove all IM logos and references — use navy + sky colours only.
- Reference Integral Media in documents intended for Higher Ranking or Purpose Digital clients

---

## White-Label Considerations

If creating a document for a **white-label partner** (Higher Ranking, Purpose Digital):
- Remove all IM logos and "Integral Media" text
- The navy/sky colour palette is safe to use (it's generic enough)
- Replace the hero label and footer with partner-appropriate text
- Do NOT include any IM email addresses, names, or references

---

# Integral Media — Email Signature Style Guide

Standard HTML email signature for all Integral Media team members. Gmail-compatible table-based layout — no external stylesheets, no JavaScript.

---

## Signature Layout

Two-column table layout with a vertical accent divider:

```
┌──────────────┬───────────────────────────┐
│              │  Full Name                │
│  Brandmark   │  Job Title                │
│  (80px)      │                           │
│              │  M  0400 000 000          │
│  INTEGRAL    │  E  name@integralmedia... │
│  MEDIA       │  W  integralmedia.com.au  │
│              │                           │
│              │  605/10 Yarra Street...   │
└──────────────┴───────────────────────────┘
        ↑ 2px Sky Blue (#27C1F4) border
```

- **Max width:** 520px
- **Left column:** Brandmark image (80px wide, centred) + "INTEGRAL MEDIA" wordmark text below
- **Divider:** 2px solid `#27C1F4` (right border on left cell)
- **Right column:** Name, title, contact details, address
- **Cell padding:** 24px either side of divider

---

## Typography

| Element | Font | Size | Weight | Colour |
|---------|------|------|--------|--------|
| Full name | Inter / system fallback | 17px | Bold (700) | Navy `#002F6C` |
| Job title | Inter / system fallback | 13px | 400 | `#6B7280` |
| Contact labels (M, E, W) | Inter / system fallback | 13px | 400 | `#6B7280` |
| Contact values | Inter / system fallback | 13px | 400 | Sky `#27C1F4` (linked) |
| Address | Inter / system fallback | 11px | 400 | `#9CA3AF` |
| "INTEGRAL MEDIA" wordmark | Julius Sans One / Arial Black fallback | 16px | Bold | Navy `#002F6C` |

### Font Stack

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
```

### Wordmark Text Styling

The "INTEGRAL" and "MEDIA" text below the brandmark uses special rendering to match the logo weight:

```css
font-family: 'Julius Sans One', 'Arial Black', sans-serif;
font-size: 16px;
font-weight: bold;
color: #002F6C;
letter-spacing: 0.05px;
-webkit-text-stroke: 0.5px #002F6C;
text-shadow: 0 0 1px #002F6C, 0 0 1px #002F6C;
```

---

## Colours

| Element | Value |
|---------|-------|
| Name | `#002F6C` (navy) |
| Title | `#6B7280` (grey) |
| Contact labels | `#6B7280` (grey) |
| Links (phone, email, website) | `#27C1F4` (sky) — `text-decoration: none` |
| Address | `#9CA3AF` (light grey) |
| Vertical divider | `#27C1F4` (sky), 2px solid |
| Body text | `#333740` (charcoal) — line-height: 1.7 |

---

## Logo / Brandmark

- **Image:** `https://reports.integralmedia.com.au/logos/current/png/brandmark/im_brandmark_colour.png`
- **Width:** 80px
- **Display:** Block, centred in left cell with 8px bottom margin
- **Alt text:** "IM"

> **Note:** Unlike HTML documents (which use inline SVG), email signatures use an externally hosted PNG because Gmail strips SVG from signatures.

---

## Contact Detail Format

Each contact line uses a single-letter label with fixed 18px width for alignment:

```html
<div style="margin-bottom: 3px;">
  <span style="color: #6B7280; display: inline-block; width: 18px;">M</span>
  <a href="tel:0400000000" style="color: #27C1F4; text-decoration: none;">0400 000 000</a>
</div>
<div style="margin-bottom: 3px;">
  <span style="color: #6B7280; display: inline-block; width: 18px;">E</span>
  <a href="mailto:name@integralmedia.com.au" style="color: #27C1F4; text-decoration: none;">name@integralmedia.com.au</a>
</div>
<div style="margin-bottom: 3px;">
  <span style="color: #6B7280; display: inline-block; width: 18px;">W</span>
  <a href="https://integralmedia.com.au" style="color: #27C1F4; text-decoration: none;">integralmedia.com.au</a>
</div>
```

### Address

Separated from contact links by 8px top margin, indented 18px (matching label width), smaller text (11px), lighter colour (`#9CA3AF`):

```
605/10 Yarra Street, South Yarra, VIC 3141
```

---

## Full HTML Template

When generating a new team member signature, use this template. Replace the placeholder values.

```html
<table cellpadding="0" cellspacing="0" border="0" style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; max-width: 520px;">
  <tr>
    <td style="padding-right: 24px; vertical-align: middle; border-right: 2px solid #27C1F4; text-align: center;">
      <img src="https://reports.integralmedia.com.au/logos/current/png/brandmark/im_brandmark_colour.png" alt="IM" width="80" style="display: block; margin: 0 auto 8px; border: 0;">
      <div style="text-align: center; line-height: 1.1;">
        <div style="font-family: 'Julius Sans One', 'Arial Black', sans-serif; font-size: 16px; font-weight: bold; color: #002F6C; letter-spacing: 0.05px; -webkit-text-stroke: 0.5px #002F6C; text-shadow: 0 0 1px #002F6C, 0 0 1px #002F6C;">INTEGRAL</div>
        <div style="font-family: 'Julius Sans One', 'Arial Black', sans-serif; font-size: 16px; font-weight: bold; color: #002F6C; letter-spacing: 0.05px; -webkit-text-stroke: 0.5px #002F6C; text-shadow: 0 0 1px #002F6C, 0 0 1px #002F6C;">MEDIA</div>
      </div>
    </td>
    <td style="padding-left: 24px; vertical-align: middle;">
      <div style="margin-bottom: 8px;">
        <strong style="font-size: 17px; color: #002F6C; display: block; margin-bottom: 2px;"><!-- FULL NAME --></strong>
        <span style="font-size: 13px; color: #6B7280;"><!-- JOB TITLE --></span>
      </div>
      <div style="font-size: 13px; line-height: 1.7; color: #333740; margin-top: 10px;">
        <div style="margin-bottom: 3px;">
          <span style="color: #6B7280; display: inline-block; width: 18px;">M</span>
          <a href="tel:<!-- PHONE_RAW -->" style="color: #27C1F4; text-decoration: none;"><!-- PHONE_FORMATTED --></a>
        </div>
        <div style="margin-bottom: 3px;">
          <span style="color: #6B7280; display: inline-block; width: 18px;">E</span>
          <a href="mailto:<!-- EMAIL -->" style="color: #27C1F4; text-decoration: none;"><!-- EMAIL --></a>
        </div>
        <div style="margin-bottom: 3px;">
          <span style="color: #6B7280; display: inline-block; width: 18px;">W</span>
          <a href="https://integralmedia.com.au" style="color: #27C1F4; text-decoration: none;">integralmedia.com.au</a>
        </div>
        <div style="margin-top: 8px; font-size: 11px; color: #9CA3AF; padding-left: 18px;">
          605/10 Yarra Street, South Yarra, VIC 3141
        </div>
      </div>
    </td>
  </tr>
</table>
```

---

## Generating Signature Pages

When asked to create a signature for a team member, generate a standalone HTML page that wraps the signature table in a copy-paste helper:

1. **Info panel** at top — name, title, instructions ("Select and copy the signature below, then paste into Gmail Settings > Signature")
2. **Dashed border box** (`3px dashed #27C1F4`) containing the signature table
3. **"SELECT AND COPY BELOW/ABOVE" hints** in Sky Blue above and below the signature
4. Include the Google Fonts import for Julius Sans One and Inter in the page `<head>`

### Deployment

Individual signature files are deployed to the VPS at:
```
reports.integralmedia.com.au/Claude_Code_Projects/email-signatures/signature-{firstname}-{lastname}.html
```

The master preview of all signatures lives at:
```
reports.integralmedia.com.au/Claude_Code_Projects/email-signatures/ALL-SIGNATURES-PREVIEW.html
```

---

## Email Signature Do's and Don'ts

### Do
- Use the exact template above — all signatures must be visually identical in structure
- Use the hosted brandmark PNG (Gmail strips inline SVG)
- Include `border: 0` on the image to prevent blue link borders in some email clients
- Use inline styles on every element (email clients strip `<style>` blocks)
- Link phone numbers with `tel:` and emails with `mailto:`
- Keep `text-decoration: none` on all links

### Don't
- Add social media icons or links (not part of the IM signature standard)
- Use different colours, fonts, or sizes per team member
- Include marketing taglines, quotes, or legal disclaimers
- Use an `<img>` tag for the wordmark text — it's rendered as styled text for crispness
- Modify the vertical divider colour or width
- Add the signature to white-label partner communications — use a plain text sign-off instead

---

# Integral Media — Google Sheets Style Guide

Brand-faithful formatting for Google Sheets, derived from the IM HTML style guide. Adapted for Sheets constraints: limited fonts, no border-radius/shadows/text-transform. All colour combinations pass WCAG AA (4.5:1+ for normal text).

---

## Sheets Colour Palette

| Token | Hex | RGB (0-1) | WCAG Notes | Usage |
|-------|-----|-----------|------------|-------|
| `navy` | `#002F6C` | `0.0, 0.184, 0.424` | 17.5:1 vs white | Document title row bg, summary tab colour |
| `navy-light` | `#0A3D7A` | `0.039, 0.239, 0.478` | 14.4:1 vs white | Section divider row bg |
| `sky` | `#27C1F4` | `0.153, 0.757, 0.957` | Accent only | Tab colours (data tabs), accent borders |
| `sky-muted` | `#E6F7FE` | `0.902, 0.969, 0.996` | 6.3:1 vs slate-dark | Notes/data source bg, LOW priority bg |
| `charcoal` | `#333740` | `0.200, 0.216, 0.251` | 14.8:1 vs white | All body text |
| `cool-grey` | `#DCDDEB` | `0.863, 0.867, 0.922` | — | All borders, horizontal rules |
| `light` | `#F1F5F9` | `0.945, 0.961, 0.976` | 14.0:1 vs charcoal | Column header bg, alternating row band |
| `lighter` | `#F8FAFC` | `0.973, 0.980, 0.988` | 16.7:1 vs navy | Sub-header bg |
| `slate-dark` | `#475569` | `0.278, 0.333, 0.412` | 6.3:1 vs sky-muted | Secondary text (notes, footnotes) |
| `white` | `#FFFFFF` | `1.0, 1.0, 1.0` | — | Primary row bg, text on dark bg |
| `subtitle-grey` | `#CCCCCC` | `0.8, 0.8, 0.8` | 10.8:1 vs navy | Subtitle text on navy bg |
| `red-muted` | `#FEE2E2` | `0.996, 0.886, 0.886` | 12.4:1 vs charcoal | HIGH priority bg |
| `amber-muted` | `#FEF3C7` | `0.996, 0.953, 0.780` | 13.8:1 vs charcoal | MEDIUM priority bg |
| `amber` | `#F59E0B` | `0.961, 0.620, 0.043` | — | Warning row left border accent |
| `green-muted` | `#DCFCE7` | `0.863, 0.988, 0.906` | 14.2:1 vs charcoal | VERIFIED / complete bg |

### Accessibility Notes
- `slate` (#64748B) replaced with `slate-dark` (#475569) for all secondary text — original was borderline 4.5:1 on sky-muted, new value gives 6.3:1 headroom
- Minimum font size: 10pt everywhere (no 9pt)
- Separator rows: 20px minimum (invisible rows break keyboard nav + screen readers)
- Priority/warning rows use colour + text label + left border accent (not colour-only)

---

## Element Specifications

| Element | Background | Text Colour | Font | Size | Bold | Height | Merge | Borders |
|---------|-----------|-------------|------|------|------|--------|-------|---------|
| Document title | `navy` | `white` | Roboto | 14pt | Yes | 40px | Full width | Bottom: 3px `sky` accent |
| Subtitle rows | `navy` | `subtitle-grey` | Roboto | 10pt | No | 22px | Full width | None |
| Section divider | `navy-light` | `white` | Roboto | 11pt | Yes | 30px | Full width | None |
| Column header | `light` | `charcoal` | Roboto | 10pt | Yes | 28px | No | Bottom: 1px `cool-grey` |
| Sub-header | `lighter` | `navy` | Roboto | 10pt | Yes | 26px | Full width | Bottom: 1px `cool-grey` |
| Data cell (single-line) | `white` | `charcoal` | Roboto | 10pt | No | 24px | No | Bottom: 1px `cool-grey` |
| Data cell (wrapped) | `white` | `charcoal` | Roboto | 10pt | No | 42px | No | Bottom: 1px `cool-grey` |
| Alt data cell (single-line) | `light` | `charcoal` | Roboto | 10pt | No | 24px | No | Bottom: 1px `cool-grey` |
| Alt data cell (wrapped) | `light` | `charcoal` | Roboto | 10pt | No | 42px | No | Bottom: 1px `cool-grey` |
| Data source note | `sky-muted` | `slate-dark` | Roboto | 10pt | Italic | 24px | Full width | None |
| Separator row | `white` | — | — | — | — | **20px** | — | None |
| HIGH priority | `red-muted` | `charcoal` | Roboto | 10pt | Yes | 24px | No | Left: 3px `red` |
| MEDIUM priority | `amber-muted` | `charcoal` | Roboto | 10pt | Yes | 24px | No | Left: 3px `amber` |
| LOW priority | `sky-muted` | `charcoal` | Roboto | 10pt | Yes | 24px | No | Left: 3px `sky` |
| Warning row | `amber-muted` | `charcoal` | Roboto | 10pt | **Yes** | 24px | No | Left: 3px `amber` |

---

## Sheets Design Decisions

- **Font:** Roboto everywhere (closest to Inter in Sheets). Roboto Mono for email addresses and IDs.
- **Hierarchy:** Navy title → navy-light sections → light headers → white/light data rows (4 levels)
- **Borders:** Horizontal rules only — 1px cool-grey bottom border on every data row. No full grid.
- **Sky accent:** Used sparingly — tab colours + title bottom accent border only. Never as cell bg.
- **Separator rows:** 20px empty rows for breathing space, accessible for keyboard nav.
- **Text wrapping:** Default to **WRAP on all content columns**. Only use CLIP/OVERFLOW on explicitly short-value columns (single status words, yes/no, single IDs under 15 chars). When in doubt, WRAP.
- **Frozen rows:** Row 1 on data tabs, none on Summary/report tabs.
- **Alignment:** Left-align all text columns. Never centre-align text columns.
- **Tab colours:** Summary = navy (#002F6C), data tabs = sky (#27C1F4).

### Column Width Guidelines

| Content Type | Width (px) |
|-------------|-----------|
| Dates | 140 |
| Email addresses | 250 |
| IDs / short codes | 110-140 |
| Names / labels | 220-280 |
| Status / role | 120-140 |
| Notes / descriptions | 300-400 |
| URLs | 320-400 |

---

## Sheets Anti-Patterns (Do Not)

- Full grid borders (overwhelming)
- Bright saturated cell backgrounds (unprofessional, accessibility issues)
- Multiple font families (visual noise)
- Centre-aligned text columns (harder to scan)
- Font sizes below 10pt (readability on laptop screens)
- Invisible separator rows (<20px)
- Colour-only status indicators (accessibility failure)
- Relying on sheet default for white backgrounds (residual formatting bleeds through from previous sessions)
- Formatting only the data range without clearing surrounding columns/rows (old banding/formatting artifacts remain visible)

---

## Sheets API Reference

When building batchUpdate requests, use the RGB (0-1) values from the colour palette. Google Sheets API expects `{ red: 0.0, green: 0.184, blue: 0.424 }` format.

### Implementation Rules

- **Explicit white backgrounds:** Always set explicit white backgrounds on ALL data rows. Never rely on the sheet default — previous formatting sessions may have left residual cell-level backgrounds that override the sheet default.
- **Clear beyond data range:** After formatting the data range, clear all backgrounds from `endColumn` to column Z and from `endRow` to row 100+. Old banded ranges and formatting often extend beyond the visible data area.
- **Default wrap strategy:** Set `wrapStrategy: "WRAP"` on all content columns. Only use CLIP/OVERFLOW on columns with short single-value content (yes/no, single IDs under 15 chars).

### API Gotchas

- **Unmerge before merge:** Always send `unmergeCells` on the full sheet range before applying any new `mergeCells` requests. Otherwise you'll get "You must select all cells in a merged range to merge or unmerge them" errors from cells merged in previous sessions.
- **Banding conflicts:** `addBanding` fails if any banded range already overlaps the target range. The correct delete method is `deleteBanding` (not `deleteBandedRange`). Query existing banded ranges first and delete ALL of them, not just known IDs.
- **Merged cells silently block writes:** Writing to column B of a merged A:B cell returns success but the value is NOT written. Always `unmergeCells` on the target range before writing data.

### Typical Request Order per Tab

0. `unmergeCells` — clear all existing merges on the full sheet range
1. `deleteBanding` — query and remove ALL existing banded ranges
2. `updateSheetProperties` — tab colour, frozen rows
3. `mergeCells` — section dividers, title rows, note rows
4. `updateDimensionProperties` — column widths + row heights
5. `repeatCell` — backgrounds, text formatting, fonts, alignment, wrap
6. `updateBorders` — horizontal rules, accent borders
7. `addBanding` — alternating rows on data sections with 8+ rows
8. Clear formatting beyond data range — explicit white bg on surrounding empty cells

---

## Sheets White-Label

Same formatting rules apply for Higher Ranking and Purpose Digital clients — just remove all IM references from content. No brand modifications needed to the formatting itself.
