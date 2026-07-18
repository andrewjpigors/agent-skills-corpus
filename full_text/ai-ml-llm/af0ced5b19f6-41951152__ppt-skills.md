---
name: ppt-skills
description: Create stunning, animation-rich HTML presentations from scratch or convert PowerPoint files (.ppt/.pptx) to beautiful web slides. Use when the user wants to build a pitch deck, presentation, slideshow, or slide deck — or convert an existing PPT to a web presentation. Generates zero-dependency single HTML files with keyboard/touch navigation and scroll-triggered animations. Supports speaker notes, theme toggle, code highlighting, charts, PDF export, Alibaba PuHuiTi font embedding, fullscreen presentation, speaker view, and more. Style options include Neon Cyber, Bold Signal, Swiss Modern, Paper & Ink, and 8 more curated presets.
---

# ppt-skills

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser. Single self-contained HTML files — no npm, no build tools, no frameworks. Works offline, renders in 10 years.

**Style presets:** Bold Signal, Electric Studio, Creative Voltage, Dark Botanical, Notebook Tabs, Pastel Geometry, Split Pastel, Vintage Editorial, Neon Cyber, Terminal Green, Swiss Modern, Paper & Ink

**Font options:** Space Grotesk, Alibaba PuHuiTi 3, JetBrains Mono, Clash Display, and more

For full style details and CSS specs: read `references/STYLE_PRESETS.md` when needed.

---

## Phase 0: Detect Mode

Determine the user's intent:

- **Mode A — New Presentation:** Create slides from scratch → go to Phase 1
- **Mode B — PPT Conversion:** Convert an existing `.ppt`/`.pptx` file → go to Phase 4
- **Mode C — Enhance Existing:** Improve an existing HTML presentation → read the file, then enhance (always maintain viewport fitting)
- **Mode D — Multi-File Merge:** Combine multiple PPT/PPTX files into one deck → go to Phase 4b

---

## ⚠️ CRITICAL: Viewport Fitting (Non-Negotiable)

**Every slide MUST fit exactly within the viewport. No scrolling within slides, ever.**

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4–6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards max (2×3 or 3×2) |
| Code slide | 1 heading + 8–10 lines of code |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |
| Chart slide | 1 heading + 1 chart (full width) |
| Video slide | 1 heading + 1 embedded video |

**Content exceeds limits → Split into multiple slides.**

### Required CSS for Every Presentation

```css
html, body { height: 100%; overflow-x: hidden; }
html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }

:root {
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
}

.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--slide-padding);
}

@media (max-height: 700px) { :root { --slide-padding: clamp(0.75rem, 3vw, 2rem); --title-size: clamp(1.25rem, 4.5vw, 2.5rem); } }
@media (max-height: 600px) { :root { --title-size: clamp(1.1rem, 4vw, 2rem); --body-size: clamp(0.7rem, 1.2vw, 0.95rem); } .nav-dots, .toolbar, .keyboard-hint, .progress-info { display: none; } }
@media (max-height: 500px) { :root { --title-size: clamp(1rem, 3.5vw, 1.5rem); --slide-padding: clamp(0.4rem, 2vw, 1rem); } }
@media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.2s !important; } }
```

**⚠️ Never negate CSS functions directly.** Use `calc(-1 * clamp(...))` not `-clamp(...)`.

---

## Phase 1: Content Discovery (New Presentations)

Ask the user (via normal conversation — ask all at once):

1. **Purpose:** pitch deck / teaching / conference talk / internal presentation?
2. **Length:** ~5–10 / 10–20 / 20+ slides?
3. **Content:** ready content, rough notes, or just a topic?
4. **Images:** any images to include? (provide path like `./assets` or `~/Desktop/screenshots`)
5. **Inline editing:** should text be editable in-browser after generation?
6. **Speaker notes:** does the presentation need speaker notes?
7. **Template:** start from scratch, or use a built-in template?

### Built-in Templates

When user says **"use a template"**, ask which scenario:

| Template | Style | Use Case |
|----------|-------|-----------|
| **Keynote Style** | Minimal, elegant transitions, large imagery | Product demo, premium pitch |
| **Jobs Style** | Black bg, white text, full-bleed images | Classic Steve Jobs presentation |
| **Flat Corporate** | Clean shapes, data-forward, brand colors | Business reports, board decks |
| **Academic** | Serif headings, structured layout, paper-like | Research talks, thesis defense |
| **Creative Portfolio** | Bold typography, asymmetric grid | Design/creative showcase |
| **Startup Pitch** | Bold numbers, milestones, team photos | VC pitch, roadshow |

Templates are NOT separate files — the agent generates the specific slide structure, color palette, and animation timing for each template style using the existing 12 presets.

---

## Phase 2: Style Discovery

### Option A — Direct Selection (user knows what they want)

Pick from presets:

| Preset | Vibe |
|--------|------|
| Bold Signal | Confident, high-impact, dark |
| Electric Studio | Clean, professional, split panel |
| Creative Voltage | Energetic, retro-modern |
| Dark Botanical | Elegant, sophisticated |
| Notebook Tabs | Editorial, organized |
| Pastel Geometry | Friendly, approachable |
| Split Pastel | Playful, modern |
| Vintage Editorial | Witty, personality-driven |
| Neon Cyber | Futuristic, techy |
| Terminal Green | Developer-focused, hacker |
| Swiss Modern | Minimal, precise |
| Paper & Ink | Literary, thoughtful |

### Option B — Visual Discovery (default for undecided users)

Generate **3 mini style preview HTML files** in `.tmp-slide-previews/` — each is a single title slide showing typography, colors, and animation. Tell the user the file paths and ask which they prefer.

### Font Options

| Font | Style | How to use |
|------|-------|-----------|
| **Alibaba PuHuiTi 3** | Modern Chinese font, 9 weights | Use `fonts/` folder (see below) |
| Space Grotesk | Clean geometric sans | Google Fonts CDN |
| JetBrains Mono | Developer-friendly monospace | Google Fonts CDN |
| Clash Display | Bold display, futuristic | Fontshare CDN |
| Satoshi | Clean modern sans | Fontshare CDN |
| Cormorant | Elegant serif | Google Fonts CDN |

**Alibaba PuHuiTi 3 Setup:**
If the user selects PuHuiTi, the skill generates HTML that references `fonts/AlibabaPuHuiTi-3-*.woff2` from a local `fonts/` folder. The skill includes a `fonts/` directory with 9 weights (Thin/Regular/Medium/Bold/.../Black) as WOFF2 files.

**Never use:** purple gradients on white, Inter/Roboto/system fonts as display fonts, generic blue primary colors.

For full preset specs (colors, fonts, signature elements): read `references/STYLE_PRESETS.md`.

---

## Phase 3: Generate Presentation

### Image Processing (skip if no images)

If user provided images, use direct file paths in HTML (not base64), e.g. `src="assets/logo.png"`. Never overwrite originals.

### HTML Architecture (Full-Featured)

```html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>
    <meta name="description" content="Presentation description">
    <meta property="og:title" content="Presentation Title">
    <meta property="og:description" content="Presentation description">

    <!-- Highlight.js — code highlighting with offline fallback -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>window.hljs || document.write('<script src="data:text/javascript,hljs=%7BhighlightElement:%7B%7D%7D"><\/script>')</script>

    <!-- Chart.js — charts with offline fallback -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
    <script>window.Chart || document.write('<script>window.Chart={}"><\/script>')</script>

    <style>
        /* ─── BASE ─────────────────────────────── */
        :root {
            --title-size: clamp(1.5rem, 5vw, 4rem);
            --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
            --h3-size: clamp(1rem, 2.5vw, 1.5rem);
            --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
            --small-size: clamp(0.65rem, 1vw, 0.875rem);
            --slide-padding: clamp(1rem, 4vw, 4rem);
            --content-gap: clamp(0.5rem, 2vw, 2rem);
        }

        /* ─── ALIBABA PUHUITI FONT ───────────── */
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 100; font-style: normal; font-display: swap; src: url(fonts/AlibabaPuHuiTi-3-35-Thin.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 300; src: url(fonts/AlibabaPuHuiTi-3-45-Light.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 400; src: url(fonts/AlibabaPuHuiTi-3-55-Regular.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 500; src: url(fonts/AlibabaPuHuiTi-3-65-Medium.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 600; src: url(fonts/AlibabaPuHuiTi-3-75-SemiBold.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 700; src: url(fonts/AlibabaPuHuiTi-3-85-Bold.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 800; src: url(fonts/AlibabaPuHuiTi-3-95-ExtraBold.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 900; src: url(fonts/AlibabaPuHuiTi-3-105-Heavy.woff2) format('woff2'); }
        @font-face { font-family: "Alibaba PuHuiTi 3"; font-weight: 950; src: url(fonts/AlibabaPuHuiTi-3-115-Black.woff2) format('woff2'); }

        /* ─── VIEWPORT (MANDATORY) ───────────── */
        html, body { height: 100%; overflow-x: hidden; }
        html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }
        body { font-family: 'Space Grotesk', sans-serif; }
        .slide {
            width: 100vw; height: 100vh; height: 100dvh;
            overflow: hidden; scroll-snap-align: start;
            display: flex; flex-direction: column; position: relative;
        }
        .slide-content {
            flex: 1; display: flex; flex-direction: column;
            justify-content: center; max-height: 100%;
            overflow: hidden; padding: var(--slide-padding);
        }

        /* ─── THEME TOGGLE ──────────────────── */
        :root { --bg: #0a0a0f; --text: #ffffff; --accent: #00ffcc; --card-bg: #1a1a24; }
        :root[data-theme="light"] { --bg: #faf9f7; --text: #1a1a1a; --accent: #0055ff; --card-bg: #f0f0f0; }
        body { background: var(--bg); color: var(--text); transition: background 0.3s, color 0.3s; }

        /* ─── NAVIGATION ────────────────────── */
        .progress-bar { position: fixed; top: 0; left: 0; height: 3px; background: var(--accent); width: 0%; z-index: 1000; transition: width 0.3s; }
        .progress-info { position: fixed; top: 0.75rem; left: 1rem; font-size: var(--small-size); color: var(--text); opacity: 0.6; z-index: 1000; font-family: 'JetBrains Mono', monospace; }
        .nav-dots { position: fixed; right: 1.5rem; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 8px; z-index: 1000; }
        .nav-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--text); opacity: 0.3; cursor: pointer; transition: all 0.3s; }
        .nav-dot.active { opacity: 1; background: var(--accent); box-shadow: 0 0 8px var(--accent); transform: scale(1.3); }
        .toolbar { position: fixed; top: 0.75rem; right: 1rem; display: flex; gap: 0.4rem; z-index: 1000; }
        .toolbar button {
            background: rgba(128,128,128,0.2); border: 1px solid rgba(128,128,128,0.3);
            border-radius: 6px; color: var(--text); cursor: pointer; padding: 0.4rem 0.75rem;
            font-size: 0.8rem; backdrop-filter: blur(8px); transition: all 0.2s; line-height: 1;
        }
        .toolbar button:hover { background: rgba(128,128,128,0.4); transform: scale(1.05); }
        .toolbar button:active { transform: scale(0.95); }

        /* ─── FULLSCREEN ────────────────────── */
        .fullscreen-toast { position: fixed; top: 50%; left: 50%; transform: translate(-50%,-50%); background: rgba(0,0,0,0.8); color: white; padding: 1rem 2rem; border-radius: 8px; font-size: 1.2rem; z-index: 9999; pointer-events: none; opacity: 0; transition: opacity 0.3s; }
        .fullscreen-toast.show { opacity: 1; }

        /* ─── SPEAKER NOTES ─────────────────── */
        .notes-panel {
            position: fixed; bottom: 0; left: 0; right: 0;
            background: rgba(0,0,0,0.92); backdrop-filter: blur(12px);
            padding: 1.25rem 2rem; transform: translateY(100%);
            transition: transform 0.3s ease; z-index: 2000;
            max-height: 45vh; overflow-y: auto;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        .notes-panel.open { transform: translateY(0); }
        .notes-panel h4 { color: var(--accent); margin: 0 0 0.5rem 0; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; }
        .notes-panel p { color: rgba(255,255,255,0.85); margin: 0; line-height: 1.7; font-size: var(--body-size); }
        .notes-panel .next-slide { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.5); font-size: var(--small-size); }
        .notes-toggle {
            position: fixed; bottom: 1rem; right: 1rem;
            background: rgba(128,128,128,0.2); border: 1px solid rgba(128,128,128,0.3);
            border-radius: 50%; width: 2.5rem; height: 2.5rem;
            color: var(--text); cursor: pointer; font-size: 1.2rem;
            backdrop-filter: blur(8px); z-index: 2001; display: flex; align-items: center; justify-content: center;
        }

        /* ─── SPEAKER VIEW ──────────────────── */
        .speaker-view {
            position: fixed; inset: 0; background: #000;
            z-index: 3000; display: none; padding: 1rem;
            grid-template-columns: 1fr 1fr; grid-template-rows: 1fr auto;
            gap: 0.5rem;
        }
        .speaker-view.active { display: grid; }
        .speaker-slide-current { background: var(--card-bg); border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; }
        .speaker-slide-next { background: #111; border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; font-size: 0.6rem; opacity: 0.7; }
        .speaker-controls { grid-column: 1 / -1; display: flex; align-items: center; justify-content: center; gap: 1rem; }
        .speaker-timer { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; color: white; }
        .speaker-close { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; color: white; padding: 0.5rem 1rem; cursor: pointer; font-size: 0.9rem; }
        .speaker-close:hover { background: rgba(255,255,255,0.2); }

        /* ─── CODE HIGHLIGHTING ────────────── */
        pre code.hljs { border-radius: 8px; padding: clamp(0.75rem, 2vw, 1.5rem) !important; font-size: var(--small-size); max-height: 60vh; overflow: auto; }

        /* ─── CHART ────────────────────────── */
        .chart-container { width: 100%; max-width: 900px; margin: 0 auto; }

        /* ─── VIDEO EMBED ─────────────────── */
        .video-container { position: relative; width: 100%; max-width: 900px; margin: 0 auto; aspect-ratio: 16/9; }
        .video-container iframe, .video-container video { width: 100%; height: 100%; border: none; border-radius: 8px; }

        /* ─── GESTURE LAYER ───────────────── */
        .gesture-hint { position: fixed; bottom: 4rem; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.7); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.75rem; opacity: 0; transition: opacity 0.3s; z-index: 500; pointer-events: none; }
        .gesture-hint.show { opacity: 1; }

        /* ─── LONG-PRESS MENU ─────────────── */
        .context-menu {
            position: fixed; background: rgba(20,20,20,0.95); border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px; padding: 0.5rem 0; min-width: 180px;
            z-index: 4000; display: none; backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        }
        .context-menu.open { display: block; }
        .context-menu-item { padding: 0.6rem 1rem; color: rgba(255,255,255,0.85); cursor: pointer; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem; }
        .context-menu-item:hover { background: rgba(255,255,255,0.1); }
        .context-menu-item.danger { color: #ff6b6b; }
        .context-menu-divider { height: 1px; background: rgba(255,255,255,0.1); margin: 0.25rem 0; }

        /* ─── ANIMATIONS (with data-delay) ─── */
        .reveal {
            opacity: 0; transform: translateY(20px);
            transition: opacity 0.6s ease, transform 0.6s ease;
            transition-delay: var(--reveal-delay, 0s);
        }
        .visible .reveal { opacity: 1; transform: translateY(0); }
        .visible .reveal:nth-child(1) { --reveal-delay: 0.1s; }
        .visible .reveal:nth-child(2) { --reveal-delay: 0.2s; }
        .visible .reveal:nth-child(3) { --reveal-delay: 0.3s; }
        .visible .reveal:nth-child(4) { --reveal-delay: 0.4s; }
        .visible .reveal:nth-child(5) { --reveal-delay: 0.5s; }
        .visible .reveal:nth-child(6) { --reveal-delay: 0.6s; }

        /* Custom delay per element: data-delay="0.8s" */
        .reveal[data-delay] { transition-delay: var(--reveal-delay); }

        /* ─── RESPONSIVE ────────────────────── */
        @media (max-height: 600px) { .nav-dots, .toolbar, .keyboard-hint, .progress-info, .notes-toggle { display: none; } }
        @media (prefers-reduced-motion: reduce) { .reveal { opacity: 1; transform: none; transition: none; } }

        /* ─── PRINT / PDF ─────────────────── */
        @media print {
            .slide { height: 100vh; page-break-after: always; }
            .toolbar, .nav-dots, .keyboard-hint, .progress-info, .notes-toggle, .notes-panel, .speaker-view, .context-menu, .gesture-hint { display: none !important; }
        }
    </style>
</head>
<body>
    <!-- Progress: slide X of Y + time estimate -->
    <div class="progress-info" id="progressInfo">1 / 12 · ~5 min left</div>

    <!-- Toolbar -->
    <div class="toolbar">
        <button onclick="toggleTheme()" title="Toggle Theme (T)">🌓</button>
        <button onclick="toggleSpeakerView()" title="Speaker View (S)">🖥️</button>
        <button onclick="enterFullscreen()" title="Fullscreen (F)">⛶</button>
        <button onclick="window.print()" title="Export PDF (P)">📄</button>
    </div>

    <div class="progress-bar" id="progressBar"></div>
    <nav class="nav-dots" id="navDots"></nav>
    <div class="keyboard-hint">← → Scroll · N Notes · T Theme · S Speaker · F Fullscreen</div>

    <!-- ── Slide 1: Title ── -->
    <section class="slide" data-notes="Welcome. Introduce yourself and set context." data-duration="2min">
        <div class="slide-content">
            <h1 class="reveal" data-delay="0.3s">Presentation Title</h1>
            <p class="reveal" data-delay="0.6s">Subtitle</p>
        </div>
    </section>

    <!-- ── Slide 2: Code ── -->
    <section class="slide" data-notes="This code shows the key API. Walk through each line carefully." data-duration="3min">
        <div class="slide-content">
            <h2 class="reveal">Code Example</h2>
            <pre class="reveal" data-delay="0.3s"><code class="language-javascript">const handler = async (req, res) => {
  const result = await process(req.body);
  return res.json({ ok: true, data: result });
};</code></pre>
        </div>
    </section>

    <!-- ── Slide 3: Chart ── -->
    <section class="slide" data-notes="Chart shows growth over 3 quarters. Key insight: Q4 spike driven by new product launch." data-duration="2min">
        <div class="slide-content">
            <h2 class="reveal">Performance Metrics</h2>
            <div class="chart-container reveal" data-delay="0.3s">
                <canvas id="myChart"></canvas>
            </div>
        </div>
    </section>

    <!-- ── Slide 4: Video ── -->
    <section class="slide" data-notes="Demo video — 90 second walkthrough. Pause after for Q&A." data-duration="2min">
        <div class="slide-content">
            <h2 class="reveal">Product Demo</h2>
            <div class="video-container reveal" data-delay="0.3s">
                <!-- YouTube embed -->
                <!-- <iframe src="https://www.youtube.com/embed/VIDEO_ID" allowfullscreen></iframe> -->
                <!-- Or local video: -->
                <!-- <video src="demo.mp4" controls></video> -->
                <div style="background:#222;width:100%;height:100%;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#666;">Video placeholder</div>
            </div>
        </div>
    </section>

    <!-- More slides... -->

    <!-- Speaker Notes Panel -->
    <div class="notes-panel" id="notesPanel">
        <h4>Speaker Notes</h4>
        <p id="notesContent">Press N to toggle notes for current slide.</p>
        <div class="next-slide" id="nextSlidePreview">Next: Slide Title</div>
    </div>
    <button class="notes-toggle" onclick="toggleNotes()" title="Speaker Notes (N)">📝</button>

    <!-- Speaker View -->
    <div class="speaker-view" id="speakerView">
        <div class="speaker-slide-current" id="speakerCurrent">
            <span style="color:#666;">Current slide</span>
        </div>
        <div class="speaker-slide-next" id="speakerNext">
            <span style="color:#666;">Next slide</span>
        </div>
        <div class="speaker-controls">
            <span class="speaker-timer" id="speakerTimer">00:00</span>
            <button class="speaker-close" onclick="toggleSpeakerView()">Exit Speaker View (Esc)</button>
        </div>
    </div>

    <!-- Context Menu (right-click) -->
    <div class="context-menu" id="contextMenu">
        <div class="context-menu-item" onclick="prevSlide(); closeContextMenu()">← Previous</div>
        <div class="context-menu-item" onclick="nextSlide(); closeContextMenu()">Next →</div>
        <div class="context-menu-divider"></div>
        <div class="context-menu-item" onclick="toggleTheme(); closeContextMenu()">🌓 Toggle Theme</div>
        <div class="context-menu-item" onclick="toggleSpeakerView(); closeContextMenu()">🖥️ Speaker View</div>
        <div class="context-menu-item" onclick="enterFullscreen(); closeContextMenu()">⛶ Fullscreen</div>
        <div class="context-menu-divider"></div>
        <div class="context-menu-item" onclick="toggleNotes(); closeContextMenu()">📝 Toggle Notes</div>
        <div class="context-menu-item danger" onclick="closeContextMenu()">Cancel</div>
    </div>

    <!-- Gesture hint -->
    <div class="gesture-hint" id="gestureHint">Swipe to navigate</div>

    <!-- Fullscreen toast -->
    <div class="fullscreen-toast" id="fullscreenToast">Press Esc to exit</div>

    <script>
        /* ─── SLIDE ENGINE ──────────────────────────────── */
        class SlideEngine {
            constructor() {
                this.slides = document.querySelectorAll('.slide');
                this.total = this.slides.length;
                this.current = 0;
                this.startTime = null;
                this.timerInterval = null;
                this.longPressTimer = null;
                this.init();
            }

            init() {
                this.buildDots();
                this.bindKeys();
                this.bindTouch();
                this.bindContextMenu();
                this.observeSlides();
                this.highlightCode();
                this.initCharts();
                this.updateNotes();
                this.updateProgress();
                this.startTimer();
            }

            buildDots() {
                const nav = document.getElementById('navDots');
                this.slides.forEach((_, i) => {
                    const d = document.createElement('div');
                    d.className = 'nav-dot' + (i === 0 ? ' active' : '');
                    d.onclick = () => this.go(i);
                    nav.appendChild(d);
                });
            }

            observeSlides() {
                const io = new IntersectionObserver(e => {
                    e.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            const idx = [...this.slides].indexOf(entry.target);
                            if (idx !== this.current) {
                                this.current = idx;
                                this.update();
                            }
                        }
                    });
                }, { threshold: 0.5 });
                this.slides.forEach(s => io.observe(s));
            }

            bindKeys() {
                document.addEventListener('keydown', e => {
                    if (e.target.getAttribute('contenteditable')) return;
                    switch(e.key) {
                        case 'ArrowDown': case ' ': case 'ArrowRight':
                            e.preventDefault(); this.next(); break;
                        case 'ArrowUp': case 'ArrowLeft':
                            e.preventDefault(); this.prev(); break;
                        case 'n': case 'N': toggleNotes(); break;
                        case 't': case 'T': toggleTheme(); break;
                        case 's': case 'S': toggleSpeakerView(); break;
                        case 'f': case 'F': enterFullscreen(); break;
                        case 'p': case 'P': window.print(); break;
                        case 'Escape': this.closeAllPanels(); break;
                    }
                });
            }

            bindTouch() {
                let startY = 0, startX = 0, startTime = 0;
                const hint = document.getElementById('gestureHint');

                // Show gesture hint on first touch
                const showHint = () => { hint.classList.add('show'); setTimeout(() => hint.classList.remove('show'), 2000); };
                document.addEventListener('touchstart', e => {
                    startY = e.touches[0].clientY;
                    startX = e.touches[0].clientX;
                    startTime = Date.now();
                    // Long press for context menu (700ms)
                    this.longPressTimer = setTimeout(() => {
                        if (Math.abs(startY - e.touches[0].clientY) < 10 && Math.abs(startX - e.touches[0].clientX) < 10) {
                            this.showContextMenu(e.touches[0].clientX, e.touches[0].clientY);
                        }
                    }, 700);
                }, { passive: true });

                document.addEventListener('touchend', e => {
                    clearTimeout(this.longPressTimer);
                    const dy = startY - e.changedTouches[0].clientY;
                    const dx = startX - e.changedTouches[0].clientX;
                    const dt = Date.now() - startTime;

                    if (dt > 500) return; // long press, don't navigate

                    // Pinch zoom (scale < 0.9 or > 1.1)
                    // Simple vertical swipe for now
                    if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 50) {
                        dy > 0 ? this.next() : this.prev();
                    } else if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {
                        // Horizontal swipe — theme toggle
                        toggleTheme();
                    }
                }, { passive: true });
            }

            bindContextMenu() {
                document.addEventListener('contextmenu', e => {
                    e.preventDefault();
                    this.showContextMenu(e.clientX, e.clientY);
                });
            }

            showContextMenu(x, y) {
                const menu = document.getElementById('contextMenu');
                menu.style.left = Math.min(x, window.innerWidth - 200) + 'px';
                menu.style.top = Math.min(y, window.innerHeight - 300) + 'px';
                menu.classList.add('open');
            }

            go(i) { this.slides[Math.max(0, Math.min(i, this.total - 1))].scrollIntoView({ behavior: 'smooth' }); }
            next() { if (this.current < this.total - 1) this.go(this.current + 1); }
            prev() { if (this.current > 0) this.go(this.current - 1); }

            update() {
                document.querySelectorAll('.nav-dot').forEach((d, i) => d.classList.toggle('active', i === this.current));
                document.getElementById('progressBar').style.width = ((this.current + 1) / this.total * 100) + '%';
                this.updateNotes();
                this.updateProgress();
                this.updateSpeakerView();
            }

            updateNotes() {
                const slide = this.slides[this.current];
                const notes = slide?.dataset?.notes || 'No notes for this slide.';
                document.getElementById('notesContent').textContent = notes;
                const nextSlide = this.slides[this.current + 1];
                document.getElementById('nextSlidePreview').textContent = nextSlide
                    ? 'Next: ' + (nextSlide.querySelector('h1,h2')?.textContent || 'Untitled')
                    : 'End of presentation';
            }

            updateProgress() {
                const remaining = this.total - this.current - 1;
                // Estimate ~1.5min per slide
                const minsLeft = Math.round(remaining * 1.5);
                document.getElementById('progressInfo').textContent =
                    `${this.current + 1} / ${this.total} · ~${minsLeft} min left`;
            }

            updateSpeakerView() {
                // Mirror current slide to speaker view
                const current = this.slides[this.current];
                const next = this.slides[this.current + 1];
                if (current) {
                    const clone = current.cloneNode(true);
                    clone.style.cssText = 'width:100%;height:100%;overflow:hidden;position:relative;';
                    clone.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
                    const container = document.getElementById('speakerCurrent');
                    container.innerHTML = '';
                    container.appendChild(clone);
                }
                if (next) {
                    const clone = next.cloneNode(true);
                    clone.style.cssText = 'width:100%;height:100%;overflow:hidden;position:relative;opacity:0.6;';
                    clone.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
                    const container = document.getElementById('speakerNext');
                    container.innerHTML = '';
                    container.appendChild(clone);
                }
            }

            startTimer() {
                this.startTime = Date.now();
                this.timerInterval = setInterval(() => {
                    const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
                    const m = String(Math.floor(elapsed / 60)).padStart(2,'0');
                    const s = String(elapsed % 60).padStart(2,'0');
                    document.getElementById('speakerTimer').textContent = `${m}:${s}`;
                }, 1000);
            }

            closeAllPanels() {
                document.getElementById('notesPanel').classList.remove('open');
                document.getElementById('speakerView').classList.remove('active');
                document.getElementById('contextMenu').classList.remove('open');
            }

            highlightCode() { document.querySelectorAll('pre code').forEach(b => { if (window.hljs) hljs.highlightElement(b); }); }
            initCharts() {
                document.querySelectorAll('canvas[id]').forEach(canvas => {
                    if (!window.Chart) return;
                    // User provides chart config via data attributes or script
                });
            }
        }

        /* ─── GLOBAL HELPERS ───────────────────────────── */
        window.toggleTheme = () => {
            const html = document.documentElement;
            html.dataset.theme = html.dataset.theme === 'light' ? 'dark' : 'light';
        };

        window.toggleNotes = () => document.getElementById('notesPanel').classList.toggle('open');

        window.toggleSpeakerView = () => {
            const sv = document.getElementById('speakerView');
            sv.classList.toggle('active');
            if (sv.classList.contains('active')) {
                const engine = window.slideEngine;
                if (engine) engine.updateSpeakerView();
            }
        };

        window.enterFullscreen = () => {
            const el = document.documentElement;
            if (!document.fullscreenElement) {
                (el.requestFullscreen || el.webkitRequestFullscreen).call(el);
            } else {
                document.exitFullscreen();
            }
            const toast = document.getElementById('fullscreenToast');
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        };

        window.closeContextMenu = () => document.getElementById('contextMenu').classList.remove('open');
        window.prevSlide = () => window.slideEngine?.prev();
        window.nextSlide = () => window.slideEngine?.next();

        document.addEventListener('DOMContentLoaded', () => {
            window.slideEngine = new SlideEngine();
        });

        // Close context menu on click outside
        document.addEventListener('click', e => {
            if (!e.target.closest('.context-menu')) closeContextMenu();
        });
    </script>
</body>
</html>
```

### Animation Delay Control

Use `data-delay="0.8s"` on any `.reveal` element to set custom animation delay:

```html
<h1 class="reveal" data-delay="0.2s">Fast entrance</h1>
<p class="reveal" data-delay="1.2s">Delayed, appears after 1.2s</p>
<p class="reveal">Uses default stagger (0.3s)</p>
```

### Speaker Notes Feature

Add `data-notes="Your speaker notes here"` and `data-duration="2min"` to each `<section class="slide">`:

```html
<section class="slide" data-notes="Key talking points..." data-duration="3min">
```

- `data-duration` estimates time for this slide (shown in progress info)
- Notes panel toggled via **N key** or **📝 button**
- Speaker view (dual screen) shows current + next slide via **S key** or **🖥️ button**

### Code Highlighting

Use `<pre><code class="language-xxx">...</code></pre>`. Highlight.js handles 40+ languages. CDN has offline fallback (graceful degradation).

### Chart.js Charts

```javascript
new Chart(canvas.getContext('2d'), {
    type: 'bar', // bar, line, pie, doughnut, radar, bubble
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{ label: 'Revenue', data: [12, 19, 8, 15], backgroundColor: '#00ffcc' }]
    },
    options: { responsive: true }
});
```

CDN has offline fallback — if Chart.js fails to load, chart containers render as empty boxes (no crash).

### Video Embed

YouTube/Bilibili:
```html
<div class="video-container">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID" allowfullscreen></iframe>
</div>
```

Local video:
```html
<video src="demo.mp4" controls></video>
```

### Theme Toggle

Dark/light via `data-theme` on `<html>`:

```css
:root { --bg: #0a0a0f; --text: #ffffff; --accent: #00ffcc; }
:root[data-theme="light"] { --bg: #faf9f7; --text: #1a1a1a; --accent: #0055ff; }
```

### Gesture Controls

| Gesture | Action |
|---------|--------|
| Swipe up/down | Navigate slides |
| Swipe left/right | Toggle theme |
| Long press (700ms) | Open context menu |
| Pinch | Reserved (future) |

---

## Phase 4: PPT Conversion (Single File)

**Note:** PPT conversion requires `python-pptx`. If not installed, guide user to convert PPT to text/images manually.

```python
# pip install python-pptx
from pptx import Presentation

def extract_pptx(file_path):
    prs = Presentation(file_path)
    slides = []
    for i, slide in enumerate(prs.slides):
        data = {'title': '', 'content': [], 'notes': '', 'images': []}
        for shape in slide.shapes:
            if shape.has_text_frame:
                if shape == slide.shapes.title:
                    data['title'] = shape.text.strip()
                else:
                    data['content'].append(shape.text.strip())
            if hasattr(shape, 'image'):
                data['images'].append(shape.name)
        if slide.has_notes_slide:
            data['notes'] = slide.notes_slide.notes_text_frame.text.strip()
        slides.append(data)
    return slides
```

After extraction: show user the structure, then proceed to Phase 2 (style), then Phase 3 (generate).

---

## Phase 4b: Multi-File PPT Merge

Ask the user to provide multiple PPT/PPTX files. Merge all into one presentation:

```python
def merge_pptx(file_paths, output_path):
    """Merge multiple PPTX files into one deck."""
    from pptx import Presentation
    merged = Presentation()
    for path in file_paths:
        prs = Presentation(path)
        for slide in prs.slides:
            # Copy each slide layout
            slide_layout = merged.slide_masters[0].slide_layouts[6]  # blank
            new_slide = merged.slides.add_slide(slide_layout)
            for shape in slide.shapes:
                if shape.has_text_frame:
                    tf = new_slide.shapes.text_frame
                    tf.text = shape.text_frame.text
                if hasattr(shape, 'image'):
                    # Copy image
                    pass
    merged.save(output_path)
    return output_path
```

After merge: show user the combined slide count, then proceed to Phase 2 (style), then Phase 3 (generate).

---

## Phase 5: Delivery

1. Delete `.tmp-slide-previews/` if created
2. If using Alibaba PuHuiTi 3: tell user to keep the `fonts/` folder alongside the HTML
3. Tell user the output file path
4. Navigation: `← →` / `Space` · `N` Notes · `T` Theme · `S` Speaker View · `F` Fullscreen · `P` PDF
5. Ask if any adjustments needed

---

## Keyboard Shortcuts Reference

| Key | Action |
|-----|--------|
| `←` `→` `Space` | Navigate slides |
| `N` | Toggle speaker notes |
| `T` | Toggle dark / light theme |
| `S` | Toggle speaker view |
| `F` | Enter / exit fullscreen |
| `P` | Export PDF (print) |
| `E` | Toggle inline editing (if enabled) |
| `Esc` | Close all panels |

---

## Style → Feeling Quick Reference

| Feeling | Use |
|---------|-----|
| Dramatic/Cinematic | Slow fades (1–1.5s), dark + spotlight, parallax |
| Techy/Futuristic | Neon glow, particles, grid pattern, monospace accents |
| Playful/Friendly | Bouncy easing, rounded corners, pastels, floating anim |
| Professional/Corporate | Fast subtle anim (200–300ms), navy/slate, data-focused |
| Calm/Minimal | Very slow motion, high whitespace, serif type, muted palette |
| Editorial/Magazine | Strong type hierarchy, pull quotes, grid-breaking layouts |
