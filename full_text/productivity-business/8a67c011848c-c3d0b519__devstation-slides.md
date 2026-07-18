---
name: devstation-slides
description: Generate polished 16:9 slide decks in the DevStation visual system — a "Tron meets dev tools" dark aesthetic with absolute-positioned 1280×720 canvases, mono section pills, accent-color highlights, and SVG ambient glows. USE WHEN user asks for a "polished deck", "demo-ready slides", "DevStation style", "presentation quality slides", or wants pitch/launch/product slides with custom visuals rather than templated layouts.
version: 1.0.0
author: MyAIOne Agent
license: MIT
dependencies: []
metadata:
  myai:
    tags: [Slides, Presentations, Decks, DevStation, HTML, Visual-Design, Dark-Mode]
    related_skills: []
---

# DevStation Slides Skill

Generate complete, high-fidelity HTML slide decks in the **DevStation visual
system** — a dark, monospace-accented aesthetic used by the Maya One artifact
editor. Each slide is a fixed 1280×720 canvas with absolute-positioned
content; the host editor handles scaling to any viewport.

This skill is the reusable, portable version of the slide design system
that lives inside the Maya One artifact editor (`artifact-create-slides`).
Use it whenever you need to author polished decks outside that editor —
exporting to PDF, dropping into a static site, sharing as standalone HTML.

## When to use vs. skip

USE this skill when the user asks for:
- "Polished" / "demo-ready" / "investor-quality" slides
- Decks for product launches, pitch reviews, or technical demos
- Custom visuals, diagrams, mock terminals, mock dashboards
- Slides that should feel like real product marketing pages
- Anything described as "DevStation style"

SKIP and use a lighter approach when:
- The user wants a quick utility deck (status update, meeting notes)
- The content is mostly bullet points without visual storytelling
- The deliverable will be edited in Google Slides / PowerPoint (this skill
  emits HTML; for `.pptx` use the `anthropic-skills:pptx` skill)

## The design system

### Canvas
- Every slide is **1280×720** with `position: relative; overflow: hidden`.
- Wrap each slide as:
  ```html
  <section class="slide" data-slide-id="sN" data-layout="custom">
    <div class="slide-container">
      <!-- absolute-positioned objects here -->
    </div>
  </section>
  ```
- Only the first slide gets `class="slide slide--active"`. The host editor
  toggles `slide--active` on others to control visibility. If you're
  rendering standalone HTML (not in the Maya One editor), give every slide
  `slide--active` so they all show, or implement your own switcher.

### Colors

| Token | Hex | Use |
|-------|-----|-----|
| Background — charcoal | `#0a0a0f` | Default slide background |
| Background — black | `#000000` | "Moment" slides (quotes, demos) |
| Surface | `#111118` | Cards, panels, chips |
| Border subtle | `#1f1f2e` | Default stroke |
| Border raised | `#2a2a3a` | When one card should pop |
| Text — white | `#ffffff` | Headlines |
| Text — lead | `#e5e7eb` | Lead paragraphs |
| Text — body | `#9ca3af` | Body copy |
| Text — muted | `#6b7280` | Footers, deemphasized labels |
| Accent amber | `#f59e0b` | Primary brand accent |
| Accent warm amber | `#fbbf24` | Headline emphasis word |
| Accent green | `#22c55e` | Success, live, confirmed |
| Accent red | `#ef4444` | Risk, problem framing |
| Accent blue | `#3b82f6` | Info, focus |
| Accent purple | `#a855f7` | Strategic / abstract |
| Accent cyan | `#06b6d4` | Data / measurement |

**Rule:** never more than 3 accents on a single slide.

### Typography

Both fonts are loaded from Google Fonts and used inline:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=IBM+Plex+Mono:wght@400;600;700&display=swap">
```

| Font | Weight | Use |
|------|--------|-----|
| `'Inter', sans-serif` | 800 | Headlines (48–120px) |
| `'Inter', sans-serif` | 600 | Card titles (18–24px) |
| `'Inter', sans-serif` | 400 | Body copy (15–18px) |
| `'IBM Plex Mono', monospace` | 700 | Stat numbers, big nums |
| `'IBM Plex Mono', monospace` | 600 | Pills, chips, labels (14px) |
| `'IBM Plex Mono', monospace` | 400 | Footers, captions (11–16px) |

Letter-spacing convention:
- Display headlines: `-0.02em` to `-0.04em` (tight)
- Mono labels & footers: `0.05em` to `0.1em` (open)

### Spacing grid

- Outer margin: **64px** from any edge.
- Top pill row: `top: 64px`.
- Headline starts: `top: 100–180px`.
- Footer caption: `top: 660px`.

## Required chrome (every slide)

Every slide has at minimum:

1. **Top-left section pill** — `EPISODE_01 — OVERVIEW`-style monospace label
2. **Top-right status pill** — page count, version, or "● LIVE" indicator
3. **Bottom footer caption** — muted monospace, often punctuated with `//`
4. **Ambient SVG glow** — three blurred circles for depth (optional but recommended)

## Layout recipes

### 1. Cover hero (slide1 pattern)

Giant 120px wordmark, secondary "From X to Y" tagline, status pill at bottom-left.

```html
<section class="slide slide--active" data-slide-id="s1" data-layout="custom">
  <div class="slide-container">
    <!-- ambient glow -->
    <div style="position:absolute;left:0;top:0;width:1280px;height:720px;z-index:1;">
      <svg width="1280" height="720" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter id="g" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="80"/>
          </filter>
        </defs>
        <circle cx="1000" cy="360" r="200" fill="#f59e0b" filter="url(#g)" opacity="0.06"/>
        <circle cx="200"  cy="600" r="250" fill="#3b82f6" filter="url(#g)" opacity="0.04"/>
        <circle cx="800"  cy="100" r="150" fill="#a855f7" filter="url(#g)" opacity="0.03"/>
      </svg>
    </div>

    <!-- top-left pill -->
    <div style="position:absolute;left:64px;top:64px;z-index:10;">
      <p style="margin:0;font-family:'IBM Plex Mono',monospace;font-size:14px;font-weight:600;color:#9ca3af;background:#111118;border:1px solid #1f1f2e;border-radius:4px;padding:6px 14px;display:inline-block;letter-spacing:0.05em;">
        EPISODE_01 — OVERVIEW
      </p>
    </div>

    <!-- hero wordmark -->
    <div style="position:absolute;left:60px;top:250px;width:1000px;z-index:10;">
      <p style="margin:0;font-family:'Inter',sans-serif;font-size:120px;font-weight:800;color:#ffffff;letter-spacing:-0.04em;line-height:1.1;">
        DevStation
      </p>
    </div>

    <!-- tagline -->
    <div style="position:absolute;left:68px;top:400px;width:1000px;z-index:10;">
      <p style="margin:0;font-family:'Inter',sans-serif;font-size:44px;font-weight:400;color:#e5e7eb;letter-spacing:-0.01em;">
        From Issue to <strong style="font-weight:600;color:#f59e0b;">Merge-Ready</strong> PR
      </p>
    </div>

    <!-- status footer -->
    <div style="position:absolute;left:64px;top:660px;z-index:10;">
      <p style="margin:0;font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:#22c55e;letter-spacing:0.05em;">
        ● v1.0 PIPELINE ONLINE
      </p>
    </div>
  </div>
</section>
```

### 2. Centered quote (slide2 pattern)

Use black `#000000` background. 68px headline with 2–3 accent words.

```html
<p style="margin:0;text-align:center;font-family:'Inter',sans-serif;font-size:68px;font-weight:800;color:#ffffff;letter-spacing:-0.03em;line-height:1.25;">
  "DevStation helps me ship <span style="color:#f59e0b;">faster</span> —<br>
  with <span style="color:#22c55e;">cleaner</span>, more <span style="color:#ef4444;">secure</span> code."
</p>
```

### 3. 3-up icon grid (slide3, slide4 pattern)

Pill label + headline + three vertical cards. Each card: 220×340, surface
fill, 1px border (often colored), 8px radius, accent left bar (3px).

```html
<!-- card body -->
<div style="position:absolute;left:100px;top:260px;width:220px;height:340px;z-index:1;">
  <div style="width:100%;height:100%;background:#111118;border:1px solid #1f1f2e;border-radius:8px;box-sizing:border-box;"></div>
</div>
<!-- accent left bar -->
<div style="position:absolute;left:100px;top:260px;width:3px;height:340px;background:#22c55e;border-radius:8px 0 0 8px;z-index:2;"></div>
<!-- card content -->
<div style="position:absolute;left:120px;top:280px;width:180px;z-index:10;">
  <p style="margin:0;font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:700;color:#22c55e;letter-spacing:0.1em;">01</p>
  <p style="margin:12px 0 10px 0;font-family:'Inter',sans-serif;font-size:18px;font-weight:600;color:#ffffff;line-height:1.2;">Project Index</p>
  <p style="margin:0;font-family:'IBM Plex Mono',monospace;font-size:11px;color:#9ca3af;line-height:1.5;">
    Secure context for agents.
  </p>
</div>
```

### 4. Demo / split screen (slide5, slide7 pattern)

Left half: oversized monospace tag ("DEMO_01"), amber accent headline,
body paragraph. Right half: mock product UI (issue list, terminal,
code diff). Build the mock with stacked rows of `position: absolute` divs.

### 5. Roadmap matrix (slide10 pattern)

Centered headline + grid of 5–6 phase cards drawn entirely in SVG (so
connector lines work). Each card has an accent left bar in a different
color to denote phase ownership.

### 6. Process flow (slide11 pattern)

Numbered cards with horizontal arrows between them and status badges
("✅ DONE", "🔄 IN PROGRESS", "⏳ NEXT") in the bottom-right of each card.

### 7. Closing CTA / series teaser (slide9 pattern)

Short centered headline ("The deep-dive series."), 3+ smaller cards
teasing future episodes, footer with brand mark.

## Workflow

1. **Confirm intent.** Ask if not specified: how many slides? Audience?
   Tone (technical / sales / hype)? Brand color override?
2. **Outline first.** Draft a one-line description per slide before
   writing HTML. Match each line to a recipe above.
3. **Open with cover, close with CTA.** Always.
4. **Build slide by slide.** For each slide:
   - Pick a recipe.
   - Drop in the chrome (pill, status, footer, glow).
   - Place the headline.
   - Place the body content.
5. **Save** as one `.html` file with all slides under `<body>`. Include the
   Google Fonts link in `<head>` if rendering standalone.
6. **Validate.** No `<script>`, `<iframe>`, `<form>`, or inline event
   handlers — Maya One's validator will reject them.

## Boilerplate (standalone HTML)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{deck title}</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=IBM+Plex+Mono:wght@400;600;700&display=swap">
  <style>
    body { margin: 0; padding: 0; background: #0a0a0f; font-family: 'Inter', sans-serif; overflow: hidden; }
    .slide { position: relative; width: 1280px; height: 720px; margin: 0 auto; background: #0a0a0f; overflow: hidden; }
    .slide-container { position: absolute; inset: 0; width: 1280px; height: 720px; }
  </style>
</head>
<body>
  <!-- slides go here -->
</body>
</html>
```

When emitting inside the Maya One editor, use `data-artifact-type="slides"`
and link to `/static/artifact-themes/default.css` instead — the editor
handles scaling, navigation, and theming.

## See also

- `references/sample-deck.html` — full 11-slide reference deck demonstrating
  every recipe (cover, quote, 3-up grid, demo split, roadmap, process flow,
  CTA).
- The Maya One artifact editor at `/static/artifact-themes/default.css`
  includes the `data-layout="custom"` CSS that scales `.slide-container` to
  any viewport without distortion.
