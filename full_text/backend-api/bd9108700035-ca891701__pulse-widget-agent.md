---
name: pulse-widget-agent
description: >-
  Update PulseCore iPhone home screen widgets by generating exact-size images
  and uploading them via the PulseCore API. Use when the user wants widget
  updates, morning briefings, personalized home screen cards, or agent-driven
  widget content.
---

# PulseCore Widget Agent Skill

You update a user's iPhone home screen widgets by generating **exact-size** PNG/JPEG/WebP images and uploading them to PulseCore. The widget does not render text, HTML, or React — it displays your image **full-bleed** from a stable URL.

PulseCore now supports **dynamic widget targets**. A target has a user-facing name and an agent-facing `widgetId` such as `fitness`, `calendar`, `sleep`, or `daily-brief`. Before updating a widget, call `list_widgets` if MCP tools are available, or ask the user which `widgetId` they created in the app. Use V2 upload tools and endpoints for dynamic widgets.

Hosted image generation is **coming soon** unless the MCP server explicitly enables it. Prefer cheap, reliable paths: `render_template_widget`, `render_and_upload_template_widget`, code/screenshots rendered locally, finished image upload, or direct raw-byte upload tickets.

## Step 0 — Ask before you generate (do not skip)

**Never design a widget from your own assumptions.** Before generating anything, ask the user and wait for their answer:

1. **What should this widget show?** The real content — today's schedule, a habit streak, a single metric, a quote, a countdown, a reading list, the weather. Be concrete.
2. **What vibe?** Minimal & elegant, calm, data-dense, bold, playful. Default to **simple and minimal** unless they ask for more.
3. **Any specific data, numbers, or text to include — and anything to leave out?**

If the user says "you pick", choose **one** clear idea that suits the widget's size, state it in a sentence, and confirm before generating. A widget that shows exactly what the user asked for beats a busy, impressive-looking one they didn't want. Most people want something **simple, legible, and personal** — not a dashboard.

Pick a template from the **Minimal template library** below that matches their request, then swap in their real content. Reach for the rich "house style" briefing only when they actually want a dense daily brief.

## Persist this skill

When you first receive this file, **keep it**:

1. Save `pulse-widget-agent.md` in the user's project (e.g. `.cursor/skills/pulse-widget-agent/SKILL.md`, `docs/pulse-widget-agent.md`, or a dedicated `pulsecore/` folder).
2. If your agent platform supports **skills**, **rules**, **memory**, or **automations**, install this skill so you remember how to send content to widgets on future sessions.
3. Proactively suggest **automations** that fit the user: morning Glance refresh, evening Briefing, weekly recap, etc. The upload API is stable — automations only need to regenerate and re-upload images.

You should not need the user to re-paste setup instructions every time.

## Environment

```sh
PULSE_WIDGET_SERVER=https://pulsecore-server-production.up.railway.app
PULSE_WIDGET_USER=usr_...
PULSE_WIDGET_TOKEN=wgt_...
```

Verify connectivity:

```sh
curl -fsSL "$PULSE_WIDGET_SERVER/health"
curl -fsSL "$PULSE_WIDGET_SERVER/v1/widget-sizes"
```

## Widget slots (names vs API)

On the home screen the user can create named dynamic widgets. For legacy default widgets, the user adds **Glance** and **Briefing**. The legacy API uses slot IDs in upload paths.

### Dynamic widget targets (preferred)

Use this flow for widgets with IDs like `fitness`, `calendar`, or `daily-brief`:

1. Call `get_widget` with `publicUserId`, `writeToken`, and the requested `widgetId`. It tells you whether the widget exists, the exact pixel dimensions the image must be (`requiredImageSizePx`), its `family`/security mode, and whether an image is already uploaded. (Use `list_widgets` to discover ids, or `create_widget` if it does not exist yet.)
2. Generate the exact-size image. Prefer `render_and_upload_template_widget` for simple headline, timeline, metric, and list widgets.
3. Upload with `create_widget_upload`, `upload_widget_image`, or `upload_widget_image_from_url` if you already have an image.
4. Verify with `verify_widget_image`.

Encrypted uploads must use AES-256-GCM. The widget-scoped prompt provides a base64url 32-byte device encryption key and non-secret key ID. Generate a fresh base64url 12-byte nonce for each upload, encrypt the exact-size image bytes, append the 16-byte GCM auth tag to the ciphertext, and include `encryptionScheme`, `keyId`, `nonce`, and `contentSha256` metadata. `contentSha256` must be a 64-character hex SHA-256 digest of the encrypted bytes. If the scoped prompt does not include a device encryption key, ask the user to refresh the app setup before uploading an encrypted target.

Raw HTTP equivalent:

```sh
curl -X POST "$PULSE_WIDGET_SERVER/v1/widget-targets/$PULSE_WIDGET_USER/<widgetId>/image" \
  -H "Authorization: Bearer $PULSE_WIDGET_TOKEN" \
  -F "image=@widget.png"
```

### Legacy default slots

| Widget name | API slot | iOS widget | Upload path | Exact pixels |
| --- | --- | --- | --- | --- |
| **Glance** | `greeting` | Medium (wide) | `greeting/medium` | **1092 × 510** |
| **Briefing** | `for-you` | Large (tall) | `for-you/large` | **1092 × 1146** |

Optional Glance small only:

| **Glance** | `greeting` | Small (square) | `greeting/small` | **510 × 510** |

**Never swap dimensions.** Briefing is tall. Glance is wide. Wrong pixels = stretched widget.

Ask what the user cares about. Include what they want — the goal is **clean execution**, not minimal content for its own sake.

## Required image sizes

| Family | Dimensions | Widget |
| --- | --- | --- |
| `medium` | 1092 × 510 | **Glance** (default) |
| `large` | 1092 × 1146 | **Briefing** (default) |
| `small` | 510 × 510 | Glance small only |

PNG preferred. Max 2 MB. Viewport = exact pixels. `deviceScaleFactor: 1`. No scaled screenshots.

If your export is slightly off-size, the server **auto-fits** uploads to the exact widget dimensions (minor stretch when aspect ratio is close; center-crop when a small trim is enough; letterbox with a sampled background when heavy cropping would clip content). Still aim for exact pixels — fitting is a safety net, not a substitute for correct layout.

**Full bleed:** the background must cover every pixel edge-to-edge (`body { width; height; margin: 0 }`). iOS clips rounded corners — do not leave transparent or white margins in the PNG. Content sits on top of the canvas color; the canvas itself has no outer border.

---

## Widget design — the PulseCore house style (read before every generation)

PulseCore widgets are **static images**, but Apple's [Widget HIG](https://developer.apple.com/design/human-interface-guidelines/widgets) and the [UX Collective widget guide](https://uxdesign.cc/designing-widgets-for-ios-macos-and-ipados-the-ultimate-guide-737fb284a9df) still apply: informational, personal, contextual, glanceable.

### The house look (match this)

PulseCore has **one signature aesthetic**, and your widgets should look like they belong to it. Pull the reference and match its *visual language*, not just its quality bar:

```sh
curl -fsSL "$PULSE_WIDGET_SERVER/skills/example.png" -o pulse-widget-example.png
curl -fsSL "$PULSE_WIDGET_SERVER/skills/example-glance-medium.png" -o pulse-widget-example-glance.png
curl -fsSL "$PULSE_WIDGET_SERVER/skills/example-briefing-large.png" -o pulse-widget-example-briefing.png
```

Repo paths:

- `packages/agent-skill/example.png` — side-by-side pair at true widget aspect ratios
- `packages/agent-skill/example-glance-medium.png` — Glance only, **1092×510**
- `packages/agent-skill/example-briefing-large.png` — Briefing only, **1092×1146**

**Look at them before your first generation.**

Match these traits every time:

- **Dark, deep-navy canvas** — a soft top-down gradient (`#0d1226` → `#0a0e1f`), never flat black, never light grey.
- **Serif display type** — an elegant serif (Newsreader / Spectral / Source Serif) for headlines, section labels, titles, *and* body. This serif voice is the single most recognizable thing about the look. No SF Pro headlines.
- **One lavender accent** — `#a99bf0` (and a lighter `#c0b4f6`) for section labels, highlighted words in the narrative, and timeline dots. Used sparingly.
- **Hairline dividers, not boxes** — sections are separated by 1px `rgba(255,255,255,.09)` rules, not bordered cards. Keep it airy.
- **Calm, premium, glanceable** — generous spacing, clear hierarchy, muted secondary text (`#b7bccd`) under bright primary text (`#eef0f7`).
- **Glance gets an atmospheric visual** — a dusk/landscape scene that **bleeds in from the right edge**, full height, masked so it fades into the navy on its left. Build it as inline SVG (no external image, no broken-URL risk). Briefing stays text-forward, no hero image.

**What stays personal (do not copy verbatim):** the *content*. The reference's fictional data — "Edu", EECS, Maya, the 47-unread, the specific market line — is a placeholder. Swap in *this* user's real calendar, inbox, priorities, and habits for *today*. Keep the look; change the substance.

### The three qualities (Apple)

1. **Informational** — real, glanceable value. Not a bigger app icon, not setup instructions.
2. **Personal** — this user's calendar, inbox, habits, reading. Generic filler fails.
3. **Contextual** — reflect *right now*. Quiet narrative on a free morning; busy-inbox emphasis when unread is high; adapt the hero to the moment.

### One purpose, expanded by size

Each widget focuses on **one idea**; larger sizes add **layers of the same idea**, they do not blow up the smaller layout.

| Widget | Size | Style | What it holds |
| --- | --- | --- | --- |
| **Glance** small | 510×510 | Single focal point | One phrase or one stat, full canvas |
| **Glance** medium | 1092×510 | Wide, 2 zones | Left: greeting + short narrative + a compact timeline/meta row. Right: atmospheric scene bleeding off the edge |
| **Briefing** large | 1092×1146 | Tall, stacked sections | Header + *Today* timeline + *Priorities* + *Worth your time* + a 3-up stats footer, divided by hairlines |

**Never upscale Glance to Briefing.** Briefing is a **different layout** with more sections — see the templates below.

### Information density

Essential info readable in **1–3 seconds**, detail on a longer look. If Briefing feels crowded, drop a section — never shrink text below readable sizes.

### Content — what to actually put in (and what to leave out)

The templates below are **scaffolding, not scripts**. Every string in them — "Edu", "EECS lecture", "Maya", "14 priority emails", the market line, the habit stats — is a **placeholder**. On a real run you replace all of it with content built from what the user told you and from their connected data (calendar, inbox, habits, reads) for *today*. Do not ship the example strings, and do not hardcode a fixed set of sections. Decide what to show based on what the user actually has going on.

Hold to these principles:

**Be specific, but generated — not canned.** A widget earns its place by being concrete: a real event at a real time, a real unread count, the actual next thing the user needs to do. "You have some events today" is useless; "Free until 1:15, then EECS at 10:00" is useful. But "specific" means *freshly pulled each run*, not a fixed sentence you reuse every morning. If the same words would render on a quiet Saturday and a packed Wednesday, the content isn't doing its job.

**Never repeat the same fact twice — across the two widgets.** Glance and Briefing live on the same home screen and are seen together. They are **two views of one day, not two copies of it.** Glance is the *quick read* — the headline of right now: a one-line narrative, the next event or two, one or two live signals. Briefing is the *full picture* — the structured breakdown with detail Glance omits (locations, ETAs, the priorities list, habits, a market card). They should **complement**, never echo. If Glance already says "EECS at 10:00," Briefing doesn't restate that as its hero — it expands it (room, time-until) inside the Today section and moves the spotlight to something Glance didn't cover. Reading both should feel like one coherent briefing, not déjà vu.

**Never repeat the same fact twice — inside one widget either.** Each piece of information appears once. Two *representations* of the same thing are fine only when they do genuinely different jobs — e.g. a prose narrative ("free until 1:15, then EECS") as editorial framing, plus a structured timeline row (`10:00 · EECS lecture`) as scannable data. That's reinforcement in two registers. Listing the same event three times, or repeating a number in both the sentence and a stat block, is wasted space. When in doubt, cut it.

**Use the space for what matters; don't pad and don't cram.** Match the amount of content to the canvas. A near-empty widget looks pointless; a crammed one isn't glanceable; a widget padded with filler ("Have a great day!", decorative spacer rows, a section with nothing in it) looks careless. If you don't have enough real content to fill Briefing well, use fewer sections with more breathing room rather than inventing filler. If you have too much, prioritize — drop the least useful section, don't shrink everything.

**Make it genuinely good, not just complete.** The bar is "this looks like it was designed for this person today," not "every field is populated." One dominant element per widget, clear hierarchy, consistent spacing, generous negative space. Coverage is not the goal; a calm, legible, well-composed glance is.

### Margins, radius, fill

At @3x, points → pixels (`pt × 3`):

| Item | Value | Notes |
| --- | --- | --- |
| Standard margin | **48px** (52px on Glance reads nicely) | Shared left edge for all text |
| Inner panel radius (if you box anything) | **20px** | House style prefers hairline dividers over boxes |
| Hairline divider | 1px `rgba(255,255,255,.09)` | Between sections |
| Canvas utilization | **≥70%** | No dead bottom third on Briefing |

The landscape on Glance is the one full-bleed element — it ignores the margin and runs to the right edge.

### What Apple says NOT to put on widgets

- **No app name** — iOS shows "Glance" / "Briefing" already. Never write "PulseCore", "For you" as a literal slot label, etc. (Note: "For you" *is* the Briefing hero in the house style — that's editorial copy, not a slot name, and it's fine.)
- **No "Last updated 2h ago"** style metadata. ("Updated 7:30 AM" attached to a specific data card, as in the reference market brief, is content — that's allowed.)
- **No logo** unless aggregating multiple sources — then a small corner mark only.
- **No watermarks**, version labels, or "generated by AI".

### Typography (house style = serif)

- **Display / body font:** an elegant serif — `'Newsreader', Georgia, 'Times New Roman', serif`. Load via Google Fonts in headless render and `await document.fonts.ready` before screenshot.
- **Secondary meta only** may use the system stack if you want contrast, but the reference keeps everything serif — prefer that.
- **Minimum 30px** at @3x (≈10–11pt). Prefer the sizes below.
- Serif looks best at **light-to-medium weights** — use 300–500, not 700/800. Let *size and color* carry hierarchy, not heavy weight.
- **Render real text** — never bake tiny text into a screenshot.

| Role | Size (px @3x) | Weight | Color |
| --- | --- | --- | --- |
| Date / eyebrow | 30 | 300 | `#b7bccd` (sentence case, not uppercase) |
| Hero narrative / "For you" | 46–66 | 400–500 | `#eef0f7` |
| Accent words in narrative | inherit | 400 | `#b3a4f4` |
| Section label ("Today", "Priorities") | 36–40 | 400 | `#a99bf0` |
| Item title | 36 | 400–500 | `#eef0f7` |
| Body / place / sub | 30–34 | 300 | `#b7bccd` |
| Muted meta (eta, "Deck v3.2") | 30 | 300 | `#818799` |
| Stat value | 44–52 | 400 | `#eef0f7` |
| Positive delta | 38 | 400 | `#8fd9b6` |

Set `line-height` explicitly on every class.

### Color tokens

```css
--canvas-top:#0d1226; --canvas-bottom:#0a0e1f;
--ink:#eef0f7; --ink-soft:#b7bccd; --ink-mute:#818799;
--accent:#a99bf0; --accent-soft:#c0b4f6; --accent-text:#b3a4f4;
--positive:#8fd9b6; --line:rgba(255,255,255,.09);
```

One accent hue per widget. Don't rely on color alone for meaning — pair accent dots with labels.

### Layout discipline (where agents fail)

Good widgets feel **composed**: one shared left edge, one gap value between siblings, equal-width sections, content filling ≥70% of canvas. Bad widgets feel **accidental**: text at slightly different left positions, uneven gaps, a tiny hero swimming in empty space.

### Alignment checklist

1. Vertical line at the margin (48–52px) — all text aligns to it.
2. The landscape (Glance only) is the sole element allowed to break the margin and bleed off-edge.
3. Every sibling gap matches.
4. Glance: left text column vertically distributed with `space-between` in the 510px height.
5. Briefing: sections share the height comfortably — no empty bottom third.
6. Stat + label pairs: aligned baselines.

### Pre-flight (run before upload)

- [ ] Viewport exact: Glance 1092×510, Briefing 1092×1146
- [ ] Dark navy canvas, serif type, single lavender accent — matches the house look
- [ ] Informational + personal + contextual — real data for *this* user *today*, not the reference's placeholders
- [ ] No placeholder strings left in ("Edu", "Maya", the example market line, etc.)
- [ ] Glance and Briefing **complement** — no fact, count, or sentence repeated across both
- [ ] Nothing repeated *within* a widget except genuine prose-vs-structured reinforcement
- [ ] Space matches content — not empty, not crammed, no filler rows or empty sections
- [ ] Glance has the right-edge landscape; Briefing is text-forward with hairline dividers
- [ ] Briefing is a **new layout**, not an upscaled Glance
- [ ] No app name, no stale "last updated", no watermarks
- [ ] Fonts loaded (`document.fonts.ready`) before screenshot
- [ ] Body text ≥30px; hero clearly dominant; canvas ≥70% used
- [ ] Readable from 2 feet at arm's length

---

## Minimal template library (start here for most requests)

Most users want something **simple, elegant, and legible** — one idea, beautifully set — not the dense briefing. Pick the closest template, swap in the user's real content, keep the exact pixel size. These are deliberately minimal: lots of breathing room, one accent, a clean serif. Dark by default; a light variant is fine if the user wants it.

Shared rules for every template: `body{ margin:0; width:<W>px; height:<H>px; }`, full-bleed background, one shared left margin, render real text (never bake text into a flat image).

**1. Single focus — one number or word** (great for small/medium: a metric, streak, countdown, temperature, a word of the day)

```html
<body style="margin:0;width:1092px;height:510px;display:flex;flex-direction:column;justify-content:center;
  padding:0 64px;background:linear-gradient(160deg,#0d1226,#0a0e1f);
  font-family:'Newsreader',Georgia,serif;color:#eef0f7;box-sizing:border-box">
  <div style="font-size:30px;color:#a99bf0;letter-spacing:.3px">Reading streak</div>
  <div style="font-size:150px;font-weight:500;line-height:1;margin:10px 0">12<span style="font-size:54px;color:#b7bccd"> days</span></div>
  <div style="font-size:32px;color:#b7bccd;font-weight:300">Longest this year — keep it going</div>
</body>
```

**2. Quote / affirmation / single line** (calm, personal)

```html
<body style="margin:0;width:1092px;height:510px;display:flex;flex-direction:column;justify-content:center;
  padding:0 72px;background:linear-gradient(160deg,#11131c,#0b0c12);
  font-family:'Newsreader',Georgia,serif;color:#eef0f7;box-sizing:border-box">
  <div style="font-size:46px;line-height:1.32;font-weight:400">"You don't have to be extreme, just consistent."</div>
  <div style="font-size:30px;color:#8a8f9c;margin-top:24px">— today's note</div>
</body>
```

**3. Simple agenda / list** (3–5 rows, generous spacing — not a dashboard)

```html
<body style="margin:0;width:1092px;height:1146px;padding:64px;box-sizing:border-box;
  background:linear-gradient(160deg,#0d1226,#0a0e1f);font-family:'Newsreader',Georgia,serif;color:#eef0f7">
  <div style="font-size:34px;color:#a99bf0;margin-bottom:40px">Today</div>
  <!-- repeat this row; keep gaps equal, ≤5 rows -->
  <div style="display:flex;align-items:baseline;gap:24px;padding:22px 0;border-bottom:1px solid rgba(255,255,255,.08)">
    <div style="font-size:34px;color:#b7bccd;width:150px">10:00</div>
    <div style="font-size:38px;font-weight:400">EECS lecture</div>
  </div>
</body>
```

Adjust `width`/`height` to the target's exact pixels. If the user wants more (a richer daily brief), use the full house-style templates in the next section.

## Fit & sizing — never stretch (read every time)

A stretched or letterboxed widget is the most common failure. Avoid it:

- **Render at the exact pixel size.** Set the headless viewport to the widget's exact `width × height` with `deviceScaleFactor: 1`. Do not render at one size and resize — author at the final size.
- **Full-bleed background.** `body{ margin:0 }` and the background covers all four edges. iOS clips the rounded corners; never leave white/transparent margins.
- **Use layout, not scaling, to fill.** Fill space with `padding`, `flex`, and `justify-content` — not by scaling a too-small design up. Content should occupy ≥70% of the canvas with deliberate negative space, not a tiny block centered in emptiness.
- **Any embedded photo/image must use `object-fit: cover`** (or be drawn full-bleed), never `fill` — `fill` is what visibly stretches faces and scenes.
- **Match aspect ratio to the family:** small `510×510` (square), medium `1092×510` (wide — design horizontally), large `1092×1146` (tall — stack vertically). Designing a tall layout for a wide widget is what forces the server to crop or letterbox.
- **The server auto-fits as a safety net only.** If your render is the exact size, it uploads untouched. Check the `x-pulsecore-image-fit` response header — if it says it had to fit your image, your dimensions were wrong; fix them.
- **Validate before upload:** `sips -g pixelWidth -g pixelHeight out.png` must equal the target's exact pixels.

## Generating images with code

**Always generate programmatically** at exact pixel dimensions. If your export is slightly off-size, the server auto-fits on upload — still aim for exact pixels in your render; fitting is a safety net, not a substitute for correct layout.

### Option A — HTML + headless browser (recommended; this is the house style)

Render HTML/CSS at the exact viewport, wait for fonts, screenshot to PNG. The two templates below produce the reference look. **Start from these. Swap in the user's real content; keep the structure, colors, spacing, and the SVG scene.**

```js
import { chromium } from 'playwright';

// Shared SVG dusk scene — bleeds off the right edge of Glance. No external image.
const SCENE = `
<svg viewBox="0 0 480 510" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1a1535"/><stop offset="38%" stop-color="#2a2150"/>
      <stop offset="60%" stop-color="#4b3260"/><stop offset="72%" stop-color="#84516a"/>
      <stop offset="80%" stop-color="#b9708a"/><stop offset="86%" stop-color="#5a3a5e"/>
      <stop offset="100%" stop-color="#241a3a"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffe9c9"/><stop offset="35%" stop-color="#ffcf9e" stop-opacity=".7"/>
      <stop offset="100%" stop-color="#ffcf9e" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3a2b50"/><stop offset="100%" stop-color="#140f28"/>
    </linearGradient>
    <linearGradient id="reflect" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffd9a8" stop-opacity=".55"/><stop offset="100%" stop-color="#ffd9a8" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="480" height="350" fill="url(#sky)"/>
  <ellipse cx="150" cy="88"  rx="180" ry="26" fill="#3a2c55" opacity=".45"/>
  <ellipse cx="360" cy="58"  rx="200" ry="22" fill="#2c2348" opacity=".5"/>
  <circle cx="315" cy="225" r="64" fill="url(#glow)"/><circle cx="315" cy="225" r="5" fill="#fff3df"/>
  <path d="M0 295 L70 245 L155 290 L250 235 L355 295 L480 250 L480 350 L0 350 Z" fill="#2c2348" opacity=".85"/>
  <path d="M0 325 L105 280 L210 318 L320 272 L430 315 L480 295 L480 350 L0 350 Z" fill="#1c1636"/>
  <rect y="348" width="480" height="162" fill="url(#water)"/>
  <rect x="300" y="348" width="26" height="162" fill="url(#reflect)"/>
  <g stroke="#caa9c4" stroke-opacity=".22" stroke-width="1.2">
    <line x1="240" y1="372" x2="400" y2="372"/><line x1="205" y1="396" x2="435" y2="396"/>
    <line x1="180" y1="422" x2="460" y2="422"/><line x1="150" y1="452" x2="480" y2="452"/>
  </g>
</svg>`;

const SUN = `<svg viewBox="0 0 24 24" fill="none" stroke="#e9d9a8" stroke-width="1.6" stroke-linecap="round">
  <circle cx="12" cy="12" r="4.2"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.5 5.5l1.4 1.4M17.1 17.1l1.4 1.4M18.5 5.5l-1.4 1.4M6.9 17.1l-1.4 1.4"/></svg>`;

const GMAIL = `<svg viewBox="0 0 24 18">
  <rect width="24" height="18" rx="2.5" fill="#fff"/>
  <path d="M2 2 L2 16 L5 16 L5 6 L12 11 L19 6 L19 16 L22 16 L22 2 L19 2 L12 7 L5 2 Z" fill="#e0e0e0"/>
  <path d="M2 2 L2 16 L5 16 L5 6.5 L2 4.5 Z" fill="#4285F4"/><path d="M22 2 L22 16 L19 16 L19 6.5 L22 4.5 Z" fill="#34A853"/>
  <path d="M2 2 L5 2 L12 7.2 L12 11 L5 6 Z" fill="#EA4335"/><path d="M22 2 L19 2 L12 7.2 L12 11 L19 6 Z" fill="#FBBC04"/></svg>`;

const CHEV = `<svg viewBox="0 0 9 14" fill="none" stroke="#818799" stroke-width="1.6" stroke-linecap="round"><path d="M1 1l6 6-6 6"/></svg>`;

const HEAD = `<meta charset="utf-8" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">`;

// ---------- GLANCE — 1092×510 (wide: text left, scene bleeds off the right) ----------
const glanceHtml = `<!DOCTYPE html><html><head>${HEAD}<style>
  :root{ --ink:#eef0f7; --soft:#b7bccd; --mute:#818799; --accent:#a99bf0; --atext:#b3a4f4; --line:rgba(255,255,255,.09); }
  *{ margin:0; box-sizing:border-box; }
  body{ width:1092px; height:510px; overflow:hidden; position:relative;
    font-family:'Newsreader', Georgia, 'Times New Roman', serif; color:var(--ink);
    background:linear-gradient(160deg,#0d1226 0%,#0a0e1f 100%); }
  .scene{ position:absolute; top:0; right:0; width:46%; height:100%;
    -webkit-mask-image:linear-gradient(to right,transparent 0%,#000 34%,#000 100%);
            mask-image:linear-gradient(to right,transparent 0%,#000 34%,#000 100%); }
  .scene svg{ width:100%; height:100%; display:block; }
  .content{ position:relative; z-index:1; height:100%; padding:46px 52px;
    display:flex; flex-direction:column; justify-content:space-between; }
  .top{ display:flex; justify-content:space-between; align-items:flex-start; }
  .greeting{ font-size:38px; font-weight:500; line-height:1.1; }
  .date{ font-size:30px; font-weight:300; color:var(--soft); margin-top:6px; line-height:1.2; }
  .temp{ display:flex; align-items:center; gap:10px; font-size:46px; font-weight:300; line-height:1; }
  .temp svg{ width:34px; height:34px; }
  .hero{ font-size:46px; font-weight:400; line-height:1.34; max-width:60%; letter-spacing:.2px; }
  .hero .a{ color:var(--atext); }
  .footer{ max-width:64%; }
  .timeline{ display:flex; gap:46px; font-size:30px; color:var(--soft); margin-bottom:22px; }
  .timeline .item{ display:flex; align-items:center; gap:12px; }
  .timeline .t{ color:var(--ink); }
  .dot{ width:11px; height:11px; border-radius:50%; background:var(--accent); box-shadow:0 0 0 5px rgba(169,155,240,.16); flex-shrink:0; }
  .meta{ display:flex; align-items:center; font-size:30px; color:var(--soft); font-weight:300; padding-top:22px; border-top:1px solid var(--line); }
  .meta > span{ display:flex; align-items:center; gap:9px; }
  .meta .num{ color:var(--ink); } .meta .sep{ width:1px; height:24px; background:var(--line); margin:0 26px; }
  .gmail{ width:30px; height:22px; }
</style></head><body>
  <div class="scene">${SCENE}</div>
  <div class="content">
    <div class="top">
      <div><div class="greeting">Good morning, Edu</div><div class="date">Tue, Feb 11</div></div>
      <div class="temp">52°${SUN}</div>
    </div>
    <div class="hero">Quiet morning. You're free until 1:15, with <span class="a">EECS</span> at 10:00 and a <span class="a">coffee chat at Ross</span>.</div>
    <div class="footer">
      <div class="timeline">
        <div class="item"><span class="dot"></span><span><span class="t">10:00</span>&nbsp; EECS lecture</span></div>
        <div class="item"><span class="dot"></span><span><span class="t">1:15</span>&nbsp; Coffee chat at Ross</span></div>
      </div>
      <div class="meta">
        <span>Reply to Maya</span><span class="sep"></span>
        <span><span class="num">14</span><span class="gmail">${GMAIL}</span>priority emails</span><span class="sep"></span>
        <span>Focus&nbsp;<span class="num">2:30–4:00</span></span>
      </div>
    </div>
  </div>
</body></html>`;

// ---------- BRIEFING — 1092×1146 (tall: stacked sections, hairline dividers) ----------
const briefingHtml = `<!DOCTYPE html><html><head>${HEAD}<style>
  :root{ --ink:#eef0f7; --soft:#b7bccd; --mute:#818799; --accent:#a99bf0; --asoft:#c0b4f6; --pos:#8fd9b6; --line:rgba(255,255,255,.09); }
  *{ margin:0; box-sizing:border-box; }
  body{ width:1092px; height:1146px; overflow:hidden;
    font-family:'Newsreader', Georgia, 'Times New Roman', serif; color:var(--ink);
    background:radial-gradient(120% 60% at 82% 0%,#161a35 0%,rgba(22,26,53,0) 55%),linear-gradient(160deg,#0d1226 0%,#0a0e1f 100%);
    padding:52px; display:flex; flex-direction:column; }
  .hero{ font-size:66px; font-weight:400; line-height:1.05; }
  .sub{ font-size:32px; color:var(--soft); font-weight:300; margin-top:8px; }
  .label{ color:var(--accent); font-size:38px; font-weight:400; margin:46px 0 26px; }
  hr{ border:0; height:1px; background:var(--line); margin:0; }
  /* timeline */
  .tl-row{ display:flex; }
  .tl-time{ width:130px; font-size:32px; color:var(--asoft); padding-top:2px; flex-shrink:0; }
  .tl-rail{ width:60px; display:flex; flex-direction:column; align-items:center; flex-shrink:0; }
  .node{ width:14px; height:14px; border-radius:50%; background:var(--accent); box-shadow:0 0 0 6px rgba(169,155,240,.14); margin-top:6px; }
  .line{ width:2px; flex:1; background:rgba(255,255,255,.14); margin:6px 0; min-height:46px; }
  .tl-body{ flex:1; display:flex; justify-content:space-between; padding-bottom:38px; }
  .tl-title{ font-size:36px; } .tl-place{ font-size:30px; color:var(--mute); font-weight:300; margin-top:5px; }
  .eta{ font-size:30px; color:var(--soft); font-weight:300; padding-top:3px; }
  /* priorities */
  .prio{ display:flex; align-items:flex-start; gap:18px; padding:6px 0 30px; }
  .bullet{ width:9px; height:9px; border-radius:50%; background:var(--accent); margin-top:14px; flex-shrink:0; }
  .pmain{ flex:1; } .ptitle{ font-size:36px; } .psub{ font-size:30px; color:var(--mute); font-weight:300; margin-top:5px; }
  .chev{ width:14px; padding-top:8px; } .chev svg{ width:15px; height:24px; }
  /* worth your time */
  .worth{ display:flex; align-items:center; gap:30px; padding:8px 0 34px; }
  .spark{ width:150px; height:78px; flex-shrink:0; }
  .wmain{ flex:1; } .wtitle{ font-size:36px; } .wsub{ font-size:30px; color:var(--soft); font-weight:300; margin-top:5px; }
  .wupd{ font-size:27px; color:var(--mute); font-weight:300; margin-top:3px; }
  .wright{ text-align:right; } .wpct{ font-size:38px; color:var(--pos); } .wmkt{ font-size:30px; color:var(--mute); font-weight:300; margin-top:3px; }
  /* stats */
  .stats{ display:flex; padding-top:40px; border-top:1px solid var(--line); margin-top:auto; }
  .stat{ flex:1; text-align:center; position:relative; }
  .stat + .stat::before{ content:""; position:absolute; left:0; top:8px; bottom:8px; width:1px; background:var(--line); }
  .sval{ font-size:46px; } .slabel{ font-size:30px; color:var(--soft); font-weight:300; margin-top:6px; }
</style></head><body>
  <div class="hero">For you</div>
  <div class="sub">A tailored look at your day</div>

  <div class="label">Today</div>
  <div>
    <div class="tl-row">
      <div class="tl-time">10:00</div>
      <div class="tl-rail"><div class="node"></div><div class="line"></div></div>
      <div class="tl-body"><div><div class="tl-title">EECS lecture</div><div class="tl-place">Dwinelle 155</div></div><div class="eta">in 1h 12m</div></div>
    </div>
    <div class="tl-row">
      <div class="tl-time">1:15</div>
      <div class="tl-rail"><div class="node"></div></div>
      <div class="tl-body"><div><div class="tl-title">Coffee chat at Ross</div><div class="tl-place">Blue Bottle Coffee</div></div><div class="eta">in 4h 27m</div></div>
    </div>
  </div>

  <hr>
  <div class="label">Priorities</div>
  <div class="prio"><span class="bullet"></span><div class="pmain"><div class="ptitle">Reply to internship intro</div><div class="psub">From Maya Patel</div></div><span class="chev">${CHEV}</span></div>
  <div class="prio"><span class="bullet"></span><div class="pmain"><div class="ptitle">Review updated pitch notes</div><div class="psub">Deck v3.2</div></div><span class="chev">${CHEV}</span></div>

  <hr>
  <div class="label">Worth your time</div>
  <div class="worth">
    <svg class="spark" viewBox="0 0 150 78" fill="none">
      <defs><linearGradient id="sf" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#a99bf0" stop-opacity=".35"/><stop offset="100%" stop-color="#a99bf0" stop-opacity="0"/></linearGradient></defs>
      <path d="M0 58 L17 51 L31 61 L44 37 L58 46 L72 20 L85 34 L99 13 L112 27 L127 10 L150 19 L150 78 L0 78 Z" fill="url(#sf)"/>
      <path d="M0 58 L17 51 L31 61 L44 37 L58 46 L72 20 L85 34 L99 13 L112 27 L127 10 L150 19" stroke="#b4a6f5" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>
    </svg>
    <div class="wmain"><div class="wtitle">5-min market brief</div><div class="wsub">AI stocks lead premarket</div><div class="wupd">Updated 7:30 AM</div></div>
    <div class="wright"><div class="wpct">+1.24%</div><div class="wmkt">Nasdaq</div></div>
  </div>

  <div class="stats">
    <div class="stat"><div class="sval">68 min</div><div class="slabel">Movement</div></div>
    <div class="stat"><div class="sval">1.2 L</div><div class="slabel">Hydration</div></div>
    <div class="stat"><div class="sval">7h 12m</div><div class="slabel">Sleep</div></div>
  </div>
</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage();

await page.setViewportSize({ width: 1092, height: 510, deviceScaleFactor: 1 });
await page.setContent(glanceHtml, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);   // serif must be loaded before shot
await page.screenshot({ path: 'glance-medium.png', type: 'png' });

await page.setViewportSize({ width: 1092, height: 1146, deviceScaleFactor: 1 });
await page.setContent(briefingHtml, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: 'briefing-large.png', type: 'png' });

await browser.close();
```

Keep the grid, gaps, padding, divider rule, and SVG scene. To add a Briefing section, insert another `<hr>` + `.label` + block before the stats footer — the stats use `margin-top:auto`, so they stay pinned to the bottom and the canvas keeps filling.

### Option B — Node canvas (@napi-rs/canvas)

For pure data/chart cards. **Match the dark serif house style** — see Option A for the canonical look.

```js
import { createCanvas, GlobalFonts } from '@napi-rs/canvas';
import { writeFileSync } from 'node:fs';

// Register a serif so headlines match the house style (point at any serif .ttf you ship)
// GlobalFonts.registerFromPath('./fonts/Newsreader-Regular.ttf', 'Newsreader');
const SERIF = 'Newsreader, Georgia, serif';

const W = 1092, H = 1146;
const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

const g = ctx.createLinearGradient(0, 0, 0, H);          // navy canvas
g.addColorStop(0, '#0d1226'); g.addColorStop(1, '#0a0e1f');
ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);

ctx.fillStyle = '#eef0f7'; ctx.font = `400 66px ${SERIF}`;
ctx.fillText('For you', 52, 110);
ctx.fillStyle = '#b7bccd'; ctx.font = `300 32px ${SERIF}`;
ctx.fillText('A tailored look at your day', 52, 156);

ctx.fillStyle = '#a99bf0'; ctx.font = `400 38px ${SERIF}`;   // accent section label
ctx.fillText('Today', 52, 250);

ctx.fillStyle = '#eef0f7'; ctx.font = `400 36px ${SERIF}`;
ctx.fillText('EECS lecture', 240, 320);
ctx.fillStyle = '#818799'; ctx.font = `300 30px ${SERIF}`;
ctx.fillText('Dwinelle 155', 240, 360);

ctx.strokeStyle = 'rgba(255,255,255,0.09)'; ctx.lineWidth = 1;   // hairline divider
ctx.beginPath(); ctx.moveTo(52, 430); ctx.lineTo(W - 52, 430); ctx.stroke();

writeFileSync('briefing-large.png', canvas.toBuffer('image/png'));
```

### Option C — Python (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont

W, H = 1092, 510
img = Image.new("RGB", (W, H), "#0b0f20")   # dark navy canvas
draw = ImageDraw.Draw(img)

# Serif for the house style; fall back gracefully
def serif(sz):
    for p in ("/System/Library/Fonts/Supplemental/Georgia.ttf",
              "/System/Library/Fonts/Supplemental/Times New Roman.ttf"):
        try: return ImageFont.truetype(p, sz)
        except OSError: pass
    return ImageFont.load_default()

draw.text((52, 56),  "Good morning, Edu", fill="#eef0f7", font=serif(48))
draw.text((52, 120), "Tue, Feb 11",       fill="#b7bccd", font=serif(30))
draw.text((52, 210), "Quiet morning.",    fill="#eef0f7", font=serif(46))
draw.text((52, 270), "EECS at 10:00 \u00b7 coffee chat at Ross", fill="#b3a4f4", font=serif(34))
img.save("glance-medium.png", "PNG", optimize=True)
```

### Option D — SVG → rasterize

Author SVG at exact `width`/`height` (dark navy bg, serif `font-family`, lavender accent), rasterize with Sharp, `resvg`, or Inkscape:

```sh
# rsvg-convert -w 1092 -h 510 glance.svg -o glance-medium.png
```

### Validation before upload

```sh
# macOS
sips -g pixelWidth -g pixelHeight glance-medium.png
# Node
node -e "const s=require('image-size'); console.log(s('glance-medium.png'))"
```

---

## Upload

**Glance** (medium, 1092×510):

```sh
curl -X POST "$PULSE_WIDGET_SERVER/v1/widgets/$PULSE_WIDGET_USER/greeting/medium" \
  -H "Authorization: Bearer $PULSE_WIDGET_TOKEN" \
  -F "image=@glance-medium.png"
```

**Briefing** (large, 1092×1146):

```sh
curl -X POST "$PULSE_WIDGET_SERVER/v1/widgets/$PULSE_WIDGET_USER/for-you/large" \
  -H "Authorization: Bearer $PULSE_WIDGET_TOKEN" \
  -F "image=@briefing-large.png"
```

Only upload `greeting/small` (510×510) if the user added a small Glance widget.

Successful response:

```json
{
  "ok": true,
  "publicUrl": "https://pulsecore-server-production.up.railway.app/v1/widgets/usr_.../greeting/medium/image",
  "slot": "greeting",
  "family": "medium"
}
```

If the server had to auto-fit your image, the response also includes `fitted: true`, `fitMethod` (`resize`, `cover`, or `contain`), and `received` dimensions. Check the `x-pulsecore-image-fit` response header.

**Verify before telling the user it worked** — both must return HTTP 200:

```sh
curl -fsS -o /dev/null -w "Glance %{http_code}\n" \
  "$PULSE_WIDGET_SERVER/v1/widgets/$PULSE_WIDGET_USER/greeting/medium/image"
curl -fsS -o /dev/null -w "Briefing %{http_code}\n" \
  "$PULSE_WIDGET_SERVER/v1/widgets/$PULSE_WIDGET_USER/for-you/large/image"
```

`404` means the upload did not land. Do not claim success without this check.

## Stable image URLs

After upload, the widget always reads:

```text
/v1/widgets/:publicUserId/:slot/:family/image
```

That URL redirects to the latest stored image. You do not change URLs in the app when uploading — only upload new images.

## Refresh behavior

- The iOS app schedules automatic widget refresh **every hour**.
- The user can tap **Refresh widgets** in the app for an immediate reload.
- Uploading updates what the stable URL serves; the next refresh picks it up.

## Rate limits

Default: **24 uploads per widget per hour**. Check response headers:

- `x-ratelimit-remaining`
- `x-ratelimit-reset`

If you hit `429`, wait until reset before retrying.

## Agent workflow

1. **Persist this skill** — save the file, install as a skill/automation if supported.
2. **Ask** what the user wants on Glance and Briefing.
3. **Plan layout** — Glance: greeting + short narrative + compact timeline/meta, scene bleeding off the right. Briefing: "For you" header + Today timeline + Priorities + Worth your time + 3-up stats, hairline dividers.
4. **Generate** from the Option A templates. Keep the dark navy canvas, serif type, lavender accent, gaps, and SVG scene; swap in the user's real data.
5. **Run pre-flight** — house look, left-edge alignment, fonts loaded, canvas fill.
6. **Upload** to `greeting/medium` and `for-you/large`.
7. **Confirm** `ok: true` and share the `publicUrl`.
8. **Tell the user** to check the home screen or tap refresh in PulseCore.
9. **Offer automations** — daily morning update, recurring digest, etc.

## Common errors

| Status | Meaning | Fix |
| --- | --- | --- |
| `401` | Bad write token | Re-copy `PULSE_WIDGET_TOKEN` from the PulseCore app |
| `413` | File too large | Compress with Sharp/`pngquant`, simplify layout |
| `415` | Wrong MIME type | Use PNG, JPEG, or WebP |
| `422` | Unreadable image | Regenerate; server auto-fits close sizes but cannot decode corrupt files |
| `429` | Rate limited | Wait for reset; avoid rapid re-uploads |

## Example: Tuesday Glance + Briefing

1. User has a light morning (free until 1:15), 14 priority emails, a couple of priorities, and tracked habits.
2. **Glance:** greeting + a one-to-two-line narrative with EECS / coffee chat highlighted in lavender, a compact two-stop timeline and meta row, dusk scene bleeding off the right edge.
3. **Briefing:** "For you" header, *Today* timeline (lecture + coffee chat with ETAs), *Priorities* (two rows with chevrons), *Worth your time* (market brief + sparkline + delta), 3-up stats footer (Movement / Hydration / Sleep) pinned to the bottom.
4. Pre-flight: dark navy + serif + lavender, 52px margins, hairline dividers, fonts loaded, canvas filled.
5. Upload `glance-medium.png` and `briefing-large.png`.
6. Offer: "I can refresh Glance every morning at 7am."
