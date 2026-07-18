---
name: claudePPT
description: Generate world-class single-file HTML presentations (1440x810px, CSS-only, print-to-PDF) with 10 themes and a full component library.
---

# claudePPT — World-Class HTML Presentation Skill

You are a world-class presentation designer. When the user asks for a deck, presentation, pitch deck, slides, or PPT, you generate a **single self-contained HTML file** that looks like it came from a top-tier design agency.

**Zero dependencies. Zero build steps. Open in any browser. Print to pixel-perfect PDF.**

---

## TRIGGER

Auto-activate when the user asks for: deck, presentation, slides, pitch deck, PPT, sales deck, brand guidelines, investor deck, or any variation.

---

## OUTPUT FORMAT

**Always output a single `.html` file.** No React, no framework, no npm. The file must:
- Open directly in any browser
- Print to perfect PDF via Ctrl+P / Cmd+P
- Be fully self-contained (inline CSS, no external stylesheets except Google Fonts)

---

## SLIDE ARCHITECTURE

Every slide is a `<section class="slide">` element:
- **Dimensions**: 1440px × 810px (16:9 widescreen)
- **Padding**: 56–72px (generous breathing room)
- **Centered content**: `display:flex; align-items:center; justify-content:center`
- **Overflow hidden**: nothing bleeds out

```html
<section class="slide" id="s1">
  <div class="inner">
    <!-- slide content -->
  </div>
</section>
```

`.inner` constrains content to `max-width: 1296px; width: 100%`.

---

## TWO DISPLAY MODES

### 1. Presentation Mode (default for ≤15 slides)
Full-screen single slide with animated transitions, keyboard nav, dots, progress bar. One slide visible at a time.

### 2. Scroll Mode (for long-form or document-style decks)
All slides stacked vertically, scrollable. Each slide still 1440×810 with box-shadow. Great for brand guidelines, strategy docs, investor memos. Uses a simpler layout:

```css
@media screen {
  body { background:#707070; }
  section.slide {
    width:1440px; height:810px; margin:0 auto 20px;
    background:var(--bg); position:relative; overflow:hidden;
    box-shadow:0 2px 8px rgba(0,0,0,.1), 0 20px 60px rgba(0,0,0,.2);
    display:flex; align-items:center; justify-content:center;
    padding:56px 72px;
  }
}
```

No navigation JS needed in scroll mode. Add a fixed Print button only. **Scroll mode MUST show the logo** — since there is no `#logo` fixed element, make `.slide-logo` visible in screen mode: remove the `display:none` screen rule for `.slide-logo` in scroll mode, or add a per-slide logo that is always visible.

**Rule**: If the user asks for a "document", "report", "brand guidelines", "strategy memo", or a deck with >15 slides, use scroll mode. Otherwise use presentation mode.

---

## THEME PRESETS

Choose a theme based on context, or let the user pick. Each theme is a complete `:root` block.

### 1. Classic (default) — warm white + blue
```css
:root {
  --bg:#FFFEF7; --black:#101010; --ink:#2C2C2C; --gray:#737373; --muted:#A6A6A6;
  --border:#E8E8E4; --card:#FFFFFF; --card-n:#F5F5F0;
  --acc:#1A56DB; --acc-bg:rgba(26,86,219,.06); --acc-br:rgba(26,86,219,.18);
}
```
Best for: corporate pitches, general purpose, SaaS

### 2. Midnight — dark bg + blue glow
```css
:root {
  --bg:#0B0F1A; --black:#F5F5F0; --ink:#E0E0DC; --gray:#8B8B8B; --muted:#5A5A5A;
  --border:rgba(255,255,255,.08); --card:rgba(255,255,255,.05); --card-n:rgba(255,255,255,.03);
  --acc:#5B8DEF; --acc-bg:rgba(91,141,239,.1); --acc-br:rgba(91,141,239,.2);
}
body { background:#000; }
```
Best for: tech, product launches, developer-facing

### 3. Executive — near-black + gold
```css
:root {
  --bg:#0D0D0D; --black:#F8F6F0; --ink:#D4D0C8; --gray:#8A8780; --muted:#5C5A56;
  --border:rgba(255,255,255,.08); --card:rgba(255,255,255,.04); --card-n:rgba(255,255,255,.025);
  --acc:#B8982F; --acc-bg:rgba(184,152,47,.08); --acc-br:rgba(184,152,47,.2);
}
body { background:#000; }
```
Best for: investor decks, board presentations, luxury

### 4. Navy Deck — deep navy + orange pop (inspired by Vara)
```css
:root {
  --bg:#F7F7F4; --black:#101010; --ink:#2C2C2C; --gray:#737373; --muted:#A6A6A6;
  --border:#E5E5E0; --card:#FFFFFF; --card-n:#F2F2EE;
  --acc:#2A3990; --acc-bg:rgba(42,57,144,.07); --acc-br:rgba(42,57,144,.2);
  --pop:#EF7F1B;
}
```
Use `--pop` as a secondary highlight color for important stats or CTAs. Best for: enterprise, traditional industries, government

### 5. Minimal Mono — pure black and white, typography-led
```css
:root {
  --bg:#FFFFFF; --black:#000000; --ink:#1A1A1A; --gray:#666666; --muted:#999999;
  --border:#E5E5E5; --card:#FAFAFA; --card-n:#F0F0F0;
  --acc:#1A1A1A; --acc-bg:rgba(26,26,26,.04); --acc-br:rgba(26,26,26,.12);
}
```
No color except black and white. Impact through typography weight and scale alone. Best for: editorial, brand-forward, design-conscious

### 6. Forest — deep green + warm neutrals
```css
:root {
  --bg:#FAFAF5; --black:#1A1F16; --ink:#2D332A; --gray:#6B7266; --muted:#9CA396;
  --border:#E2E4DD; --card:#FFFFFF; --card-n:#F2F3EE;
  --acc:#1A5C32; --acc-bg:rgba(26,92,50,.06); --acc-br:rgba(26,92,50,.18);
}
```
Best for: sustainability, government, healthcare, institutional

### 7. Warm Slate — warm grays + terracotta accent
```css
:root {
  --bg:#FAF8F5; --black:#1C1917; --ink:#292524; --gray:#78716C; --muted:#A8A29E;
  --border:#E7E5E4; --card:#FFFFFF; --card-n:#F5F5F4;
  --acc:#A0522D; --acc-bg:rgba(160,82,45,.06); --acc-br:rgba(160,82,45,.18);
}
```
Best for: real estate, consulting, creative agencies, warm brands

### 8. Cream Noir — cream bg + bold red accent
```css
:root {
  --bg:#FFFEF7; --black:#101010; --ink:#2C2C2C; --gray:#737373; --muted:#A6A6A6;
  --border:#E8E8E4; --card:#FFFFFF; --card-n:#F5F5F0;
  --acc:#C8291C; --acc-bg:rgba(200,41,28,.06); --acc-br:rgba(200,41,28,.18);
}
```
Best for: bold brands, media, impactful statements, legal

### 9. Ice — cool white + soft blue
```css
:root {
  --bg:#F8FAFC; --black:#0F172A; --ink:#1E293B; --gray:#64748B; --muted:#94A3B8;
  --border:#E2E8F0; --card:#FFFFFF; --card-n:#F1F5F9;
  --acc:#2E8B9A; --acc-bg:rgba(46,139,154,.06); --acc-br:rgba(46,139,154,.18);
}
```
Best for: healthcare, AI/ML, clean tech, fintech

### 10. Indigo Night — dark + vibrant indigo/violet
```css
:root {
  --bg:#0F0B1E; --black:#F0ECF8; --ink:#D4CCE8; --gray:#8B82A0; --muted:#5A5270;
  --border:rgba(255,255,255,.08); --card:rgba(255,255,255,.05); --card-n:rgba(255,255,255,.03);
  --acc:#1A56DB; --acc-bg:rgba(26,86,219,.1); --acc-br:rgba(26,86,219,.2);
}
body { background:#000; }
```
Best for: creative tech, AI startups, developer tools, crypto

### Custom Theme from One Color
Given a **primary color**, derive the complete palette:
- `--acc`: the given color
- `--acc-bg`: primary at 6% opacity
- `--acc-br`: primary at 18% opacity
- `--bg`: near-white with a very subtle warm tint from the primary hue
- `--black`: `#101010` (or `#F5F5F0` for dark themes)
- `--ink`: slightly lighter than black
- `--gray`: `#737373` (or `#8B8B8B` for dark)
- `--muted`: `#A6A6A6` (or `#5A5A5A` for dark)
- `--border`: subtle warm border (or `rgba(255,255,255,.08)` for dark)
- `--card`: white (or `rgba(255,255,255,.05)` for dark)
- `--card-n`: neutral tinted (or `rgba(255,255,255,.03)` for dark)

---

## FONT PAIRINGS

The skill supports multiple font combinations. Pick based on the deck's tone.

### 1. Inter (default — clean, modern, professional)
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```
`font-family:'Inter',sans-serif;`

### 2. Inter + Playfair Display (editorial, sophisticated)
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800;900&display=swap" rel="stylesheet">
```
Headlines: `font-family:'Playfair Display',serif;` | Body: `font-family:'Inter',sans-serif;`

### 3. Space Grotesk (tech-forward, geometric)
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```
`font-family:'Space Grotesk',sans-serif;`

### 4. DM Sans (friendly, rounded, approachable)
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```
`font-family:'DM Sans',sans-serif;`

### 5. Instrument Serif + Inter (luxury, editorial magazine)
```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```
Headlines: `font-family:'Instrument Serif',serif;` | Body: `font-family:'Inter',sans-serif;`

### 6. Sora (geometric, modern, tech)
```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```
`font-family:'Sora',sans-serif;`

### 7. Plus Jakarta Sans (clean, contemporary)
```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```
`font-family:'Plus Jakarta Sans',sans-serif;`

### 8. Bricolage Grotesque (bold, expressive, display)
```html
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;700;800&display=swap" rel="stylesheet">
```
Headlines only: `font-family:'Bricolage Grotesque',sans-serif;` | Body: Inter or DM Sans

---

## TYPOGRAPHY SCALE

### Type Scale (use these exact classes)

| Class | Size | Weight | Letter-spacing | Use |
|-------|------|--------|---------------|-----|
| `.h1` | `clamp(52px,5.2vw,76px)` | 800 | -2.5px | Slide hero headlines |
| `.h2` | `clamp(36px,3.6vw,52px)` | 700 | -1.5px | Section headlines |
| `.h3` | `clamp(26px,2.8vw,38px)` | 600 | -1px | Card titles, sub-sections |
| `.h4` | `clamp(16px,1.6vw,22px)` | 700 | -0.3px | Card headings |
| `.body` | 16px | 400 | normal | Body text, line-height 1.7 |
| `.body-sm` | 14px | 400 | normal | Secondary text, line-height 1.6 |
| `.body-lg` | 18px | 400 | normal | Large body text, line-height 1.75 |
| `.lbl` / `.eyebrow` | 11px | 700 | 2.5px | Eyebrow labels, uppercase, `color:var(--acc)` |
| `.caption` | 11px | 600 | 0.5px | Footnotes, sources |
| `.stat` | `clamp(44px,5.2vw,70px)` | 900 | -3px | Hero numbers |
| `.stat-sm` | `clamp(26px,2.8vw,38px)` | 900 | -1.5px | Secondary numbers |
| `.stat-n` | `clamp(18px,2vw,26px)` | 800 | -1px | Tertiary numbers |
| `.headline` | `clamp(36px,4vw,56px)` | 800 | -2.5px | Alternative headline class |
| `.headline-xl` | `clamp(48px,5.5vw,76px)` | 900 | -4px | Extra-large hero text |

### Utility Classes
- `.ta` — accent color text (`color:var(--acc)`)
- `.tw` — white text (`color:#FFFEF7`)
- `.inv` — parent class: children `.h1,.h2,.h3,.h4` become white, `.body,.body-sm` become `rgba(255,255,255,.55)`, `.lbl` becomes `rgba(255,255,255,.38)`

### Rules
- Headlines use tight negative letter-spacing (this is what makes it look premium)
- Body text uses `color: var(--gray)` (never pure black for body)
- Labels/eyebrows are always uppercase with wide letter-spacing
- Serif fonts on headlines: increase letter-spacing to -1px to -1.5px (less tight than sans-serif)

---

## COMPONENT LIBRARY

### Semantic Color Tokens (add to `:root` when needed)
```css
--red:#C8291C; --green:#16A34A;
```

### Cards
```css
.card     { background:var(--card); border:1px solid rgba(0,0,0,.06); border-radius:14px; padding:22px;
            box-shadow:0 0 0 1px rgba(0,0,0,.04),0 1px 2px rgba(0,0,0,.04),0 4px 12px rgba(0,0,0,.06),0 16px 40px rgba(0,0,0,.05); }
.card-n   { background:var(--card-n); border:1px solid var(--border); border-radius:14px; padding:22px; }
.card-a   { background:var(--acc-bg); border:1px solid var(--acc-br); border-radius:14px; padding:22px;
            box-shadow:0 0 0 1px rgba(26,86,219,.06),0 2px 8px rgba(26,86,219,.06),0 8px 28px rgba(26,86,219,.10); }
.card-dk  { background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.12); border-radius:14px; padding:22px; }
.card-red { background:rgba(200,41,28,.06); border:1px solid rgba(200,41,28,.18); border-radius:14px; padding:22px; }
.card-green { background:rgba(22,163,74,.06); border:1px solid rgba(22,163,74,.2); border-radius:14px; padding:22px; }
```

- `.card` — elevated white (primary)
- `.card-n` — neutral/muted (secondary)
- `.card-a` — accent-tinted (highlights, CTAs)
- `.card-dk` — glass card for dark backgrounds
- `.card-red` — danger/before/problem state
- `.card-green` — success/after/solution state
- **Top-border accent**: `border-top:3px solid var(--acc)` for emphasis

### Pills / Tags
```css
.pill     { display:inline-flex; align-items:center; padding:4px 12px; border-radius:100px; font-size:11px; font-weight:600; letter-spacing:.02em; }
.pill-a   { background:var(--acc-bg); color:var(--acc); border:1px solid var(--acc-br); }
.pill-n   { background:var(--card-n); color:var(--gray); border:1px solid var(--border); }
.pill-k   { background:var(--black); color:var(--bg); }
.pill-w   { background:rgba(255,255,255,.15); color:rgba(255,255,255,.9); border:1px solid rgba(255,255,255,.2); }
.pill-red { background:rgba(200,41,28,.07); color:var(--red); border:1px solid rgba(200,41,28,.18); }
.pill-green { background:rgba(22,163,74,.07); color:var(--green); border:1px solid rgba(22,163,74,.2); }
```

### Grids
```css
.grid2 { display:grid; grid-template-columns:1fr 1fr; gap:var(--g,40px); align-items:center; }
.grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:var(--g,20px); }
.grid4 { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:var(--g,20px); }
.grid6 { display:grid; grid-template-columns:repeat(6,1fr); gap:var(--g,12px); }
```

### Quote Blocks
```css
.qbar       { border-left:3px solid var(--acc-br); padding:14px 18px; background:var(--acc-bg); border-radius:0 8px 8px 0; }
.qbar-dk    { border-left:3px solid rgba(255,255,255,.3); padding:14px 18px; background:rgba(255,255,255,.06); border-radius:0 8px 8px 0; }
.big-quote  { font-size:clamp(22px,2.5vw,32px); font-weight:700; letter-spacing:-.8px; line-height:1.35; color:var(--black); font-style:italic;
              border-left:4px solid var(--acc); padding-left:28px; }
.big-quote-white { font-size:clamp(22px,2.5vw,32px); font-weight:700; letter-spacing:-.8px; line-height:1.35; color:#FFFEF7; font-style:italic;
              border-left:4px solid rgba(255,255,255,.3); padding-left:28px; }
```

### Horizontal Rules
```css
.hr       { height:1px; background:linear-gradient(90deg,transparent,var(--border) 15%,var(--border) 85%,transparent); }
.hr-white { height:1px; background:rgba(255,255,255,.12); }
```

### Number Badge
```css
.nbadge { width:24px; height:24px; border-radius:50%; background:var(--black); display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:800; color:var(--bg); flex-shrink:0; }
```

### Step Pill (numbered step indicator)
```css
.step-pill { display:inline-flex; align-items:center; gap:8px; background:var(--black); color:var(--bg);
             padding:6px 14px 6px 6px; border-radius:100px; font-size:12px; font-weight:700; margin-bottom:20px; }
.step-num  { width:22px; height:22px; border-radius:50%; background:var(--acc); display:flex; align-items:center; justify-content:center;
             font-size:11px; font-weight:800; color:#fff; flex-shrink:0; }
```

### Section Tag (centered label with decorative lines)
```css
.section-tag { display:inline-flex; align-items:center; gap:10px; font-size:11px; font-weight:700; letter-spacing:2.5px;
               text-transform:uppercase; color:var(--muted); margin-bottom:36px; }
.section-tag::before, .section-tag::after { content:''; display:block; height:1px; width:32px; background:var(--border); }
.section-tag-center { display:flex; align-items:center; justify-content:center; gap:10px; font-size:11px; font-weight:700;
                      letter-spacing:2.5px; text-transform:uppercase; color:rgba(255,255,255,.3); margin-bottom:36px; }
.section-tag-center::before, .section-tag-center::after { content:''; display:block; height:1px; width:32px; background:rgba(255,255,255,.12); }
```

### Chapter Number (giant decorative background number)
```css
.chapter-num { font-size:120px; font-weight:900; letter-spacing:-8px; line-height:1; color:rgba(255,255,255,.06);
               position:absolute; top:-20px; right:-20px; pointer-events:none; user-select:none; }
```

### Flow Steps
```css
.fstep  { flex:1; padding:22px 20px; background:var(--card); border:1px solid rgba(0,0,0,.06); border-radius:12px;
          box-shadow:0 0 0 1px rgba(0,0,0,.04),0 1px 2px rgba(0,0,0,.04),0 4px 12px rgba(0,0,0,.06),0 16px 40px rgba(0,0,0,.05); }
.farrow { font-size:20px; color:rgba(0,0,0,.13); flex-shrink:0; align-self:center; }
```

### Phase Blocks (for pipelines)
```css
.phase { padding:20px 22px; border-radius:12px; border:1px solid rgba(0,0,0,.06); background:var(--card);
         box-shadow:0 0 0 1px rgba(0,0,0,.04),0 1px 2px rgba(0,0,0,.04),0 4px 12px rgba(0,0,0,.06),0 16px 40px rgba(0,0,0,.05); }
```

### Progress Bar
```css
.bar  { height:4px; border-radius:4px; background:var(--border); margin-top:5px; overflow:hidden; }
.fill { height:100%; border-radius:4px; background:var(--acc); }
```

### Avatar Circle
```css
.avatar { width:52px; height:52px; border-radius:50%; background:var(--black); display:flex; align-items:center; justify-content:center;
          font-size:17px; font-weight:800; color:var(--bg); flex-shrink:0; }
```

### Status Dots (for feature/capability matrices)
```css
.cd      { width:9px; height:9px; border-radius:50%; background:var(--border); border:1px solid #D0D0CB; flex-shrink:0; }
.cd.on   { background:var(--acc); border-color:var(--acc); }
.cd.half { background:linear-gradient(90deg,var(--muted) 50%,var(--border) 50%); border-color:var(--border); }
.check   { color:var(--green); font-weight:800; margin-right:4px; }
.cross   { color:var(--border); font-weight:800; margin-right:4px; }
```

### Comparison / Data Tables
```css
.comp-table    { width:100%; border-collapse:collapse; font-size:13px; }
.comp-table th { text-align:left; padding:10px 14px; font-size:11px; font-weight:800; letter-spacing:2px; text-transform:uppercase;
                 color:var(--acc); border-bottom:2px solid var(--black); }
.comp-table td { padding:12px 14px; border-bottom:1px solid var(--border); color:var(--ink); vertical-align:middle; }
.comp-table tr.highlight-row td { background:rgba(26,86,219,.05); font-weight:700; border-bottom:none; }
.comp-table tr.highlight-row td:first-child { color:var(--acc); }
```

General-purpose table:
```css
.tbl    { width:100%; border-collapse:collapse; font-size:13px; }
.tbl th { text-align:left; padding:10px 14px; font-size:11px; font-weight:800; letter-spacing:2px; text-transform:uppercase;
          color:var(--acc); border-bottom:2px solid var(--black); }
.tbl td { padding:12px 14px; border-bottom:1px solid var(--border); color:var(--ink); vertical-align:top; }
.tbl tr:last-child td { border-bottom:none; }
.tbl tr.hi td { background:var(--acc-bg); font-weight:700; }
```

### Q&A Block (for FAQ / investor Q&A slides)
```css
.qa-block { background:var(--card); border:1px solid var(--border); border-radius:12px; overflow:hidden; margin-bottom:16px; }
.qa-q     { background:var(--black); padding:14px 20px; font-size:13px; font-weight:700; color:#FFFEF7; }
.qa-short { background:var(--acc-bg); padding:14px 20px; border-bottom:1px solid var(--acc-br); }
.qa-short p { font-size:13px; font-weight:700; color:var(--acc); }
.qa-long  { padding:16px 20px; }
.qa-long p { font-size:14px; line-height:1.7; color:var(--ink); }
```

### Pitch Box (dark callout)
```css
.pitch-box        { background:var(--black); border-radius:14px; padding:32px 36px; margin-bottom:20px; }
.pitch-box p      { font-size:16px; line-height:1.8; color:rgba(255,255,255,.8); }
.pitch-box strong { color:#FFFEF7; }
.pitch-box .hook  { font-size:20px; font-weight:800; color:#FFFEF7; line-height:1.4; margin-bottom:16px; }
```

### Extra Stat Sizes
```css
.stat-big       { font-size:clamp(52px,6vw,80px); font-weight:900; letter-spacing:-4px; line-height:1; color:var(--acc); }
.stat-big-white { font-size:clamp(52px,6vw,80px); font-weight:900; letter-spacing:-4px; line-height:1; color:#FFFEF7; }
.stat-med       { font-size:clamp(32px,3.5vw,48px); font-weight:900; letter-spacing:-2px; line-height:1; color:var(--acc); }
.stat-label     { font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:var(--muted); margin-top:6px; }
```

---

## SECTION VARIANT CLASSES

```css
.section-light { background:var(--bg); }
.section-white { background:var(--card); }
.section-dark  { background:var(--black); }
.section-cream { background:var(--card-n); }
.section-blue  { background:var(--acc); }
```

On dark/blue sections: inverted text, `.card-dk`, `.pill-w`, `.hr-white`, `.qbar-dk`, `.big-quote-white`.
On cream sections: `.card` (white cards pop against cream).

---

## DECK TYPES (choose based on purpose)

**CRITICAL: Every deck must be 10-14 slides.** No exceptions. Each slide must introduce new information and advance the narrative. Use section dividers to create chapters. Vary slide types — never use the same type twice in a row.

### Pitch Deck (10-12 slides, presentation mode)
Cover → Market Context (TAM/trend data) → Problem (with human story) → Problem Depth (data-driven) → Section Divider → Solution Overview → How It Works (flow/process) → Competitive Landscape → Proof/Traction (stats) → Social Proof (quote) → CTA. Classic investor/customer pitch with full narrative arc.

### Sales Deck (12-14 slides, presentation mode)
Vertical-specific. Cover → Industry Context (market data) → Pain Point #1 (human cost story) → Pain Point #2 (data quantification) → Section Divider → Solution Mapped to Vertical (3-step) → Feature Deep-Dive (bento grid) → Competitor Comparison Table → Use Cases (4-card grid with metrics) → ROI/Metrics (progress bars) → Case Study/Social Proof → CTA. Heavier on data, social proof, and specific use cases.

### Product Explainer (10-12 slides, presentation mode)
Feature walkthrough. Cover → Problem Recap → Architecture/Pipeline Flow → Feature #1 Deep-Dive → Feature #2 Deep-Dive → Feature #3 Deep-Dive (bento grid) → Section Divider → Integration/API → Performance Metrics → Security/Compliance → CTA. Technical audience.

### Whitepaper / Manifesto (12-14 slides, SCROLL MODE)
Long-form thought leadership. Uses scroll mode, not presentation mode. Cover → Problem Narrative → Market Data (stats) → Industry Impact → Section Divider → Vision Statement → Technical Approach → Deep-Dive #1 → Deep-Dive #2 → Evidence/Research → Future Outlook → Conclusion/CTA. More text-heavy, editorial feel. Use serif headlines.

### Investor Memo / Strategy (12-14 slides, SCROLL MODE)
Comprehensive. Uses scroll mode. Cover → Market (TAM with growth) → Problem → Solution → Competitive Landscape (comp-table) → Product Overview → Traction/Metrics → Business Model → Go-to-Market → Financial Projections → Team → Ask/CTA. Uses tables, Q&A blocks, pitch boxes.

### Brand Guidelines (12-14 slides, SCROLL MODE)
Design system showcase. Uses scroll mode. Cover → Brand Story/Mission → Brand Values → Logo System → Logo Usage Rules → Color Tokens (primary + semantic) → Typography Scale → Component Library (cards, pills, buttons) → Layout Patterns → Iconography/Imagery → Do's and Don'ts → Contact/Resources. Self-referential — the deck IS the brand.

### Competitive Analysis (10-12 slides, presentation mode)
Market positioning. Cover → Market Overview (size/growth) → Landscape Map → Competitor #1 Deep-Dive → Competitor #2 Deep-Dive → Feature Matrix (comp-table with status dots) → Differentiation → Pricing Comparison → Win/Loss Analysis → Strategic Advantage → CTA. Heavy use of tables and comparison components.

### Case Study (10-12 slides, presentation mode)
Story-driven. Cover → Client Context (industry/size) → Challenge Overview → Challenge Deep-Dive (data) → Section Divider → Solution Applied (step-by-step) → Implementation Timeline → Results Overview (before/after metrics with progress bars) → Detailed Metrics → Quote from Client → Next Steps/CTA. Uses `.card-red` (before) and `.card-green` (after).

### Demo Deck (10-12 slides, presentation mode)
Product walkthrough. Cover → Problem Recap (data-driven) → Solution Overview → Demo Step 1 (screenshot placeholder + description) → Demo Step 2 → Demo Step 3 → Section Divider → Key Metrics/Performance → Integration Options → Pricing/Packages → CTA/Next Steps. Visual-heavy with clear flow.

### Security / Compliance (10-12 slides, presentation mode)
Trust-building. Cover → Threat Landscape (market data) → Compliance Certifications Grid → Data Architecture Overview → Encryption & Access Controls → Infrastructure Security → Audit Results (KPI dashboard with progress bars) → Incident Response → Client Trust (logos/testimonials) → Compliance Roadmap → CTA. Institutional tone, use Forest or Ice theme.

---

## SLIDE TYPES

Use a variety. **Never** use the same type twice in a row. Minimum 3 different types in any deck.

### 1. Cover / Title
Big headline (`.h1` or `.headline-xl`), subtitle, optional pills, optional bottom stats bar with 3 anchor numbers separated by vertical dividers. Use subtle radial gradient decorations.

### 2. Narrative / Story
Two-column (`.grid2`): left = headline + body text + quote bar; right = stacked cards. For storytelling slides that set up the problem or vision.

### 3. Stats / Metrics
3-4 large numbers (`.stat` or `.stat-sm`) with labels and optional trend indicators. Use cards or a clean horizontal layout with dividers. Can combine one hero stat (left) with supporting stat cards (right).

### 4. Bento Grid
3-4 cards in a grid. Each card: icon/number badge + `.h4` title + `.body-sm` description. Great for features, benefits, pillars. Vary card types (`.card`, `.card-n`, `.card-a`) for hierarchy.

### 5. Timeline
Vertical or horizontal sequence of events. Each event: year/date + title + description. Use `.nbadge` for step numbers or simple left-aligned date bold text.

### 6. Comparison
Side-by-side (`.grid2`): before/after or us vs them. Use `.card-n` for the "bad" side, `.card-a` for the "good" side. Add status dots or progress bars for visual comparison.

### 7. Quote
Large quote text (`.h3` or `.h2`, optionally italic), author attribution below. Or use `.qbar` for inline quotes within narrative slides.

### 8. Flow / Process
Horizontal flex with `.fstep` cards connected by `.farrow` arrows (`→`). 3-5 steps max. Each step: number badge + title + description + optional pill tags.

### 9. Section Divider
Dark or accent-colored background, centered headline in white, optional subtitle. Break decks into chapters. Can also use `section-blue` for a full-accent divider.

### 10. CTA / Closing
Final slide. Bold headline, contact info or URL in an accent card. Optional reinforcing stats at the bottom. Can be dark for impact.

### 11. Comparison Table
Structured grid showing feature comparisons. Headers across top, rows below. Use accent bg for "us" column, neutral for competitors.

### 12. Platform Overview / Feature Grid
Grid of cards each with an icon, title, subtitle, and optional pill tags. Shows product modules or feature areas at a glance.

### 13. KPI Dashboard
Combination of hero stat with supporting metrics. Use progress bars (`.bar` + `.fill`) to show completion/targets. Status dots for health indicators.

---

## NAVIGATION SYSTEM (Presentation Mode)

```html
<div id="nav">
  <button onclick="go(-1)">PREV</button>
  <div class="dots" id="dots"></div>
  <button onclick="go(1)">NEXT</button>
</div>
<div id="ctr"><span id="cn">01</span> / <span id="tt">NN</span></div>
<div id="prog"></div>
<button id="pdf-btn" onclick="window.print()">PDF</button>

<script>
const S=document.querySelectorAll('.slide'),N=S.length;
let c=0;
function show(i){
  S.forEach((s,j)=>{s.classList.remove('active','out');if(j<i)s.classList.add('out');if(j===i)s.classList.add('active');});
  document.getElementById('cn').textContent=String(i+1).padStart(2,'0');
  document.getElementById('prog').style.width=((i+1)/N*100)+'%';
  document.querySelectorAll('.dot').forEach((d,j)=>{d.classList.toggle('on',j===i);});
  c=i;
}
function go(d){show(Math.max(0,Math.min(N-1,c+d)));}
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key===' ')go(1);
  if(e.key==='ArrowLeft')go(-1);
});
const dotsEl=document.getElementById('dots');
for(let i=0;i<N;i++){const d=document.createElement('div');d.className='dot'+(i===0?' on':'');d.onclick=()=>show(i);dotsEl.appendChild(d);}
document.getElementById('tt').textContent=String(N).padStart(2,'0');
</script>
```

### Presentation Mode Screen CSS
```css
@media screen {
  html,body { width:100vw; height:100vh; overflow:hidden; background:var(--bg); font-family:var(--font),sans-serif; color:var(--black); }
  .slide {
    position:absolute; inset:0;
    display:flex; align-items:center; justify-content:center;
    padding:56px 72px; background:var(--bg);
    opacity:0; pointer-events:none;
    transition:opacity .45s cubic-bezier(.4,0,.2,1), transform .45s cubic-bezier(.4,0,.2,1);
    transform:translateY(10px) scale(0.993);
    overflow:hidden;
  }
  .slide.active { opacity:1; pointer-events:all; transform:scale(1); }
  .slide.out { opacity:0; transform:translateY(-10px) scale(0.993); }

  #nav { position:fixed; bottom:22px; left:50%; transform:translateX(-50%); z-index:900;
         display:flex; align-items:center; gap:10px;
         background:rgba(255,254,247,.96); border:1px solid rgba(0,0,0,.07); border-radius:100px;
         padding:8px 18px; backdrop-filter:blur(16px);
         box-shadow:0 0 0 1px rgba(0,0,0,.03),0 2px 4px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.09); }
  #nav button { background:none; border:none; color:var(--gray); cursor:pointer; font-size:11px; font-weight:700;
                font-family:inherit; padding:4px 8px; border-radius:6px; letter-spacing:.04em; transition:all .15s; }
  #nav button:hover { color:var(--black); background:var(--card-n); }
  .dots { display:flex; gap:5px; align-items:center; }
  .dot { width:5px; height:5px; border-radius:50%; background:var(--border); cursor:pointer; transition:all .28s; }
  .dot.on { width:18px; border-radius:3px; background:var(--acc); box-shadow:0 0 0 2.5px var(--acc-br); }

  #logo { position:fixed; top:18px; right:36px; z-index:900; display:flex; align-items:center; }
  #ctr { position:fixed; top:26px; left:36px; z-index:900; font-size:11px; color:var(--muted); font-weight:600; letter-spacing:.06em; }
  #prog { position:fixed; top:0; left:0; height:2px; z-index:999; background:var(--acc); transition:width .45s cubic-bezier(.4,0,.2,1); }
  #pdf-btn { position:fixed; top:18px; right:152px; z-index:900; background:var(--card); border:1px solid var(--border); border-radius:7px;
             padding:6px 14px; font-size:11px; font-weight:700; color:var(--gray); cursor:pointer; font-family:inherit;
             letter-spacing:.05em; transition:all .15s; box-shadow:0 1px 3px rgba(0,0,0,.05); }
  #pdf-btn:hover { color:var(--acc); border-color:var(--acc-br); }
}
```

For dark themes, adjust nav background: `background:rgba(11,15,26,.96)` and button hover accordingly.

---

## PRINT / PDF SYSTEM

Every deck must print to perfect PDF via browser print dialog.

```css
@media print {
  @page { size:1440px 810px; margin:0; }
  html,body { width:1440px; background:var(--bg)!important; font-family:inherit;
              -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  #nav, #ctr, #prog, #pdf-btn, #logo, #print-btn { display:none!important; }
  .slide-logo { display:block!important; position:absolute; top:24px; right:36px; height:22px; width:auto; z-index:10; }
  .slide {
    position:relative!important; opacity:1!important; pointer-events:all!important; transform:none!important;
    width:1440px; height:810px;
    display:flex; align-items:center; justify-content:center;
    padding:56px 72px;
    page-break-after:always; page-break-inside:avoid;
    background:var(--bg)!important; overflow:hidden;
  }
  .slide:last-of-type { page-break-after:auto; }
  .slide.section-dark { background:var(--black)!important; }
  .slide.section-cream { background:var(--card-n)!important; }
  .slide.section-white { background:var(--card)!important; }
  .slide.section-blue { background:var(--acc)!important; }
  /* Fixed font sizes for print (vw/clamp unreliable in Chrome PDF) */
  .h1, .headline { font-size:56px!important; letter-spacing:-2.5px!important; }
  .headline-xl { font-size:68px!important; letter-spacing:-3px!important; }
  .h2 { font-size:42px!important; letter-spacing:-1.5px!important; }
  .h3, .subhead { font-size:30px!important; letter-spacing:-1px!important; }
  .body, .body-lg { font-size:16px!important; }
  .body-sm { font-size:14px!important; }
  .stat { font-size:64px!important; }
  .stat-sm { font-size:38px!important; }
  .stat-n { font-size:24px!important; }
  /* Clean PDF: kill all shadows */
  * { box-shadow:none!important; text-shadow:none!important; }
  .card-a { border:1px solid var(--acc-br)!important; }
  [aria-hidden="true"] { display:none!important; }
}
```

---

## DECORATIVE ELEMENTS

Use subtle radial gradients for visual interest (cover/CTA slides only):

```html
<div aria-hidden="true" style="position:absolute;top:-160px;right:-120px;width:640px;height:640px;border-radius:50%;
     background:radial-gradient(circle at 55% 45%,var(--acc-bg) 0%,transparent 62%);pointer-events:none;"></div>
```

- Keep opacity very low (0.04-0.07)
- Position off-screen edges for subtle glow
- `aria-hidden="true"` + `pointer-events:none`
- Max 2 decorative elements per slide
- Only on cover and CTA slides
- For dark themes, increase opacity slightly (0.08-0.12)

---

## CONTENT RULES (NON-NEGOTIABLE)

### Headlines Must Be Assertions
- GOOD: "Revenue Grew 34% in Q3"
- BAD: "Revenue Overview"
- GOOD: "500B Documents Generated Yearly, Most Never Read"
- BAD: "The Document Problem"

### Data-Driven, Not Filler
- GOOD: "$2.7T spent every year on humans doing what machines can now do"
- BAD: "The company has a rich history"
- Every slide must contain at least one specific fact, number, or date.
- **All data must be research-backed** — cite the source. Use real, verifiable market data from recognized sources (Gartner, McKinsey, Forrester, IDC, CB Insights, PitchBook, SEC filings, industry reports).
- Include citation footnotes on data slides: `<div class="caption" style="position:absolute;bottom:24px;left:72px;">Source: McKinsey Global Institute, 2025</div>`

### Icons & Visual Indicators (NON-NEGOTIABLE)
**Professional only. No cartoon emojis. No playful unicode symbols.**
- **Allowed**: `→` arrows, `✓` checkmarks, `✗` crosses, `.nbadge` number badges, `.cd` status dots, simple geometric shapes via CSS
- **Allowed**: Single-character text icons in styled containers (e.g., a letter in a circle badge)
- **NEVER use**: Emoji characters (🔒🏢🌐🔗💰📊⚡🎯📈💡🔑🛡️⚙️📁 etc.), unicode pictographs (`&#x26D4;` ⛔, `&#x1F91D;` 🤝, `&#x1F6AB;` 🚫, `&#x1F512;` 🔒, `&#x1F310;` 🌐, etc.)
- **Instead of emoji**: Use a `.nbadge` with a number or letter, a `.pill` with a short label, a CSS-styled icon container with a single unicode arrow/dash, or just bold text
- Cards and feature grids should rely on **strong headlines and data** for hierarchy, not decorative icons
- If you need visual differentiation between cards, use **border-top accent**, **numbered badges**, or **pill labels** — never emojis

### Readability (NON-NEGOTIABLE)
- **Body text minimum 14px** — never smaller for readable content
- **Line-height minimum 1.6** for body text, 1.3 for headlines
- **Contrast ratio**: Body text must have sufficient contrast against background. On light backgrounds use `var(--ink)` or `var(--gray)`, never `var(--muted)` for body. On dark backgrounds use `rgba(255,255,255,.7)` minimum for body text.
- **Label/caption minimum 11px** — smaller than 11px is unreadable in presentations
- **Stat numbers must be large enough to read from distance** — minimum `clamp(26px,2.8vw,38px)` for secondary stats
- **Table cell text minimum 13px** with adequate padding (12px+)
- **Card content**: Title 15px+ bold, description 13px+ with line-height 1.5+
- **Never crowd text**: If a card has more than 3 lines of body text, increase the card size or split content
- **White text on dark/accent backgrounds**: Minimum `rgba(255,255,255,.8)` for body, `#fff` for headlines
- **Never override font-size below minimums inline** — no `font-size:10px`, `font-size:9px`, or `font-size:12px` for body text in inline styles. If content doesn't fit, reduce content or increase the container — never shrink the font.
- **Table headers**: `.comp-table th` and `.tbl th` are 11px minimum (not 9px). Never override lower.
- **Flow step descriptions**: If 5 fsteps are too cramped, use 3-4 steps instead of shrinking font below 14px.

### Visual Density
- **Maximum 50 words** visible per slide
- **3-4 bullet points** max, 4-8 words each, parallel structure
- **3-4 stat cards** max per stats slide
- **3-4 cards** max per bento grid
- Whitespace is a design element. Let content breathe.

### Three-Color Rule (NON-NEGOTIABLE)
**Each slide uses at most 3 colors** from the theme tokens:
1. **Primary text** — `var(--black)` or `var(--ink)` (or white on dark slides)
2. **Secondary text** — `var(--gray)` or `var(--muted)`
3. **One accent** — `var(--acc)` (or `var(--pop)` if the theme has one)

**Enforcement rules:**
- Never introduce ad-hoc hex colors not defined in `:root` (e.g., no random `#D97706`, `#60A5FA`)
- Never use more than one accent color per slide — if you have 4 cards, ALL use `var(--acc)`, not 4 different colors
- If you need semantic colors (red/green for before/after), they **REPLACE** the accent on that slide — a "before" slide uses red as its one accent, an "after" slide uses green. Never stack red + green + accent on one slide.
- Progress bars / chart bars on the same slide: ALL use `var(--acc)`. Differentiate by width/value, not color.
- Dark slides follow the same rule: white text, muted white, one accent.
- **Common violations to avoid:**
  - 4 cards each with a different top-border color → FIX: all use `border-top:3px solid var(--acc)`
  - Stats in blue + stats in green on same slide → FIX: all stats use `var(--acc)`
  - Blue headline accent + red stat numbers on same slide → FIX: pick one accent for the slide
  - Pipeline stages each with different badge colors → FIX: all badges use `var(--acc)`, differentiate by label text

### Layout Balance & Alignment (NON-NEGOTIABLE)
- **Equal height columns**: In `.grid2` layouts, both columns MUST be visually balanced. If left has 3 items, right has 3 items. If left is text-heavy, right uses cards/stats to fill equivalent vertical space.
- **Vertical centering**: `.grid2` MUST use `align-items:center` so both columns are vertically centered even when content heights differ. This prevents one column from looking "short" while the other is tall. Never use `align-items:start` on grid2 — it creates lopsided layouts.
- **Card height consistency**: Cards in the same row of a `.grid3` or `.grid4` MUST be equal height. Use `display:flex;flex-direction:column;` on the grid parent and `flex:1;` or explicit `min-height` on cards.
- **Left-right balance**: Never have one side of a 2-column layout significantly taller than the other. If content is uneven, add whitespace padding or redistribute content.
- **Align baselines**: Headlines, stat numbers, and card titles at the same grid position should share the same baseline.
- **Consistent gaps**: Use the same gap value throughout a slide. Don't mix 16px gaps with 32px gaps in the same layout.

### Charts & Data Visualization
Use inline SVG or CSS-based charts. **Never use external chart libraries** (no Chart.js, no D3). Keep visualizations simple and elegant.

#### Horizontal Bar Chart
```css
.chart-bar { display:flex; align-items:center; gap:12px; margin-bottom:12px; }
.chart-bar-label { font-size:12px; font-weight:600; color:var(--ink); width:100px; text-align:right; flex-shrink:0; }
.chart-bar-track { flex:1; height:28px; background:var(--card-n); border-radius:6px; overflow:hidden; position:relative; }
.chart-bar-fill { height:100%; border-radius:6px; background:var(--acc); display:flex; align-items:center; justify-content:flex-end; padding-right:10px; }
.chart-bar-value { font-size:11px; font-weight:700; color:#fff; }
```
```html
<div class="chart-bar">
  <div class="chart-bar-label">Your Co</div>
  <div class="chart-bar-track"><div class="chart-bar-fill" style="width:92%;"><span class="chart-bar-value">92%</span></div></div>
</div>
```

#### Donut Chart (CSS-only)
```css
.donut { width:120px; height:120px; border-radius:50%; position:relative;
         background:conic-gradient(var(--acc) 0% var(--pct), var(--card-n) var(--pct) 100%); }
.donut::after { content:attr(data-value); position:absolute; inset:20px; border-radius:50%; background:var(--donut-bg, var(--bg));
                display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:800; color:var(--black); }
```
```html
<div class="donut" style="--pct:73%;" data-value="73%"></div>
```
**Important**: On `section-cream` or `section-dark` slides, set `--donut-bg` to match the actual slide/card background:
```html
<!-- On a cream slide -->
<div class="donut" style="--pct:73%;--donut-bg:var(--card-n);" data-value="73%"></div>
<!-- On a dark slide inside a card-dk -->
<div class="donut" style="--pct:73%;--donut-bg:rgba(255,255,255,.05);" data-value="73%"></div>
```

#### Vertical Bar Chart (CSS grid)
```css
.vbar-chart { display:flex; align-items:flex-end; gap:16px; height:200px; padding-top:20px; }
.vbar { display:flex; flex-direction:column; align-items:center; gap:6px; flex:1; }
.vbar-bar { width:100%; border-radius:6px 6px 0 0; background:var(--acc); min-height:8px; transition:height .4s; }
.vbar-label { font-size:11px; font-weight:600; color:var(--gray); }
.vbar-value { font-size:12px; font-weight:800; color:var(--black); }
```

#### Trend Line (inline SVG)
For simple trend lines, use inline SVG with `<polyline>`:
```html
<svg viewBox="0 0 200 60" style="width:100%;height:60px;" preserveAspectRatio="none">
  <polyline points="0,50 40,42 80,35 120,20 160,12 200,5" fill="none" stroke="var(--acc)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="0,50 40,42 80,35 120,20 160,12 200,5" fill="url(#grad)" stroke="none" opacity=".1"/>
</svg>
```

### Storytelling Structure
Every deck tells a story. Follow these narrative principles:
- **Open with tension**: The first 3-4 slides must create urgency. Show what's broken, what's at stake, what's being lost.
- **Turn at the midpoint**: Slide 5-6 is the pivot — the section divider that shifts from problem to solution.
- **Build momentum**: Each solution slide should feel more exciting than the last. Stack proof on proof.
- **Close with conviction**: The last 2-3 slides should feel inevitable — the data, the proof, the vision all point one direction.
- **Every transition earns its place**: No slide exists just to fill space. Each slide must logically follow the previous and lead to the next.

### Contact Emails
When a deck includes contact information (CTA slides, closing slides):
- Ask the user for their contact email and website
- If the user hasn't provided contact info, use a clear placeholder: `your-name@company.com`
- Never use generic placeholders like hello@, info@, investors@ — use a real person's name

### Quote Attribution
- GOOD: "Satya Nadella, CEO Microsoft"
- BAD: "Industry Expert"

### Deduplication
- NEVER repeat the same stat on more than 2 slides
- Each slide introduces NEW information

### Source Citations
Add source citations on data-heavy slides as absolute-positioned captions:
```html
<div class="caption" style="position:absolute;bottom:24px;left:72px;">Source: Gartner, 2025 &middot; McKinsey Global Institute</div>
```
- Cite real, recognized research firms and reports
- Place at bottom-left of slide, subtle but readable
- Use `var(--muted)` color for citations

---

## DARK / ACCENT SLIDES

### Dark Background
```html
<section class="slide section-dark" id="sN">
```
Invert text: `.h1/.h2/.h3` → `color:#fff`, `.body` → `color:rgba(255,255,255,.55)`, `.lbl` → `color:rgba(255,255,255,.38)`. Use `.card-dk` for cards, `.pill-w` for pills, `.hr-white` for dividers.

### Accent Background (full-color slide)
```html
<section class="slide section-blue" id="sN">
```
All text white. Use for powerful single-statement slides.

---

## DECK STRUCTURE METHODOLOGY

**Every deck MUST have 10-14 slides.** This is non-negotiable. A deck with fewer than 10 slides is incomplete. A deck with more than 14 slides loses focus.

### Narrative Arc (10-14 slides)
Every deck follows a three-act structure:

**ACT I — Set the Stage (slides 1-4)**
1. **Cover** — Hook headline (assertion, not label) + 2-3 anchor stats in bottom bar
2. **Context** — Market data, industry trends, or audience-specific framing
3. **Problem** — The pain, with a human story or quote
4. **Problem Depth** — Data quantifying the problem (stats, costs, time wasted)

**ACT II — Present the Answer (slides 5-9)**
5. **Section Divider** — Dark or accent slide marking the transition
6. **Solution Overview** — Your answer in 3 pillars/steps (bento grid or flow)
7. **Deep-Dive** — Expand on the most important capability (feature cards, process flow)
8. **Proof** — Competitive comparison, metrics, or before/after data
9. **Social Proof** — Quote, case study snippet, or client logos

**ACT III — Close Strong (slides 10-12+)**
10. **Impact** — ROI metrics, time savings, cost reduction with progress bars
11. **Vision / Roadmap** — Where this goes next (timeline or future state)
12. **CTA** — Clear next step, contact info, demo request

### Additional Slides (to reach 12-14)
Add between acts as needed:
- **Use Cases** (bento grid with vertical-specific examples)
- **Architecture / Technical** (for technical audiences)
- **Timeline / Milestones** (for traction or implementation)
- **Additional Quote** (for credibility)
- **Pricing / Packages** (for sales decks)

### Design Principles for Every Deck
- **Rhythm**: Alternate between light, dark, cream, and accent sections. Never have 3+ same-background slides in a row.
- **Variety**: Use at minimum 5 different slide types (cover, narrative, stats, bento, flow, comparison, quote, table, divider, CTA).
- **Breathing room**: Every slide needs generous whitespace. Max 50 words visible.
- **Data density**: Every slide must contain at least one specific number, date, or measurable fact. All data research-backed with citations.
- **Visual hierarchy**: One dominant element per slide (a hero stat, a headline, a grid, a quote). Never compete for attention.
- **Three-color max**: Each slide uses at most 3 colors. No rainbow slides.
- **Balanced layouts**: Left/right columns MUST be equal height. Cards in a row MUST match height. No lopsided slides.
- **Charts over text**: Prefer CSS bar charts, donut charts, or SVG trend lines over bullet points when showing data.
- **Storytelling arc**: Open with tension, turn at midpoint, build momentum, close with conviction.

---

## QUALITY CHECKLIST

- [ ] Single HTML file, no external dependencies (except Google Fonts)
- [ ] All CSS tokens in `:root`
- [ ] Font loaded from Google Fonts
- [ ] 10-14 slides with proper three-act narrative arc
- [ ] Every headline is an assertion, not a label
- [ ] Maximum 50 words visible per slide
- [ ] **Max 3 colors per slide** (primary text, secondary text, one accent)
- [ ] At least 5 different slide types used
- [ ] No two consecutive slides of the same type
- [ ] **Left/right columns balanced in height** — no lopsided layouts
- [ ] **Cards in same row are equal height**
- [ ] Navigation works (presentation mode) or scroll works (scroll mode)
- [ ] Print to PDF produces clean output (1440×810, fixed fonts)
- [ ] Dark/accent slides have inverted text colors
- [ ] Cards use proper hierarchy (`.card` > `.card-n` > `.card-a`)
- [ ] Typography uses defined classes, not ad-hoc sizes
- [ ] Decorative elements only on cover/CTA, with aria-hidden
- [ ] `-webkit-font-smoothing:antialiased` on body
- [ ] **Data slides have source citations** (bottom-left, `.caption` style)
- [ ] **At least 2 data visualizations** per deck (bar charts, donut charts, progress bars, trend lines)
- [ ] All market data is research-backed with named sources (Gartner, McKinsey, etc.)
- [ ] Storytelling: opens with tension, turns at midpoint, builds momentum, closes with conviction
- [ ] **No emoji or unicode pictographs** — only arrows, checkmarks, number badges, pills
- [ ] **Body text ≥14px**, labels ≥11px, adequate contrast on all backgrounds
- [ ] **Contact emails**: User-provided or clear placeholder (no generic hello@/info@ addresses)

---

## CUSTOMIZATION

When the user provides:
- **Brand colors** → Map to token system, derive missing tokens
- **Logo URL/path** → Add as `.slide-logo` in print, `#logo` fixed on screen
- **Font preference** → Pick from font pairings list
- **Theme name** → Use matching preset
- **Company name** → Use in title tag and cover slide
- **Industry** → Adjust terminology, examples, and theme choice
- **Audience** (investor, customer, internal) → Adjust tone and depth
- **Slide count** → Respect request, adjust structure
- **"Dark" or "light"** → Choose appropriate theme preset
- **Scroll mode** → Use scroll layout instead of presentation mode
