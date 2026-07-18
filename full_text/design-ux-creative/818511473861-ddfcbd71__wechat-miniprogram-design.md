---
name: wechat-miniprogram-design
description: Create distinctive, production-grade WeChat mini-program UI/UX design — multi-screen interactive prototypes that live inside a real iOS frame with the WeChat top capsule. Trigger whenever the user touches mini-program visual direction — designing from scratch, mocking an existing app, evolving a single screen into a full clickable flow, redesigning, reskinning, or reviewing a prototype. Fires on 小程序界面 / 小程序设计稿 / 小程序原型 / 微信小程序 UI / 界面设计 / 视觉方向 / 改版 / 重新设计, and on English equivalents (mini-program UI, WeChat screen design, interactive prototype, screen mockup, visual redesign). Fires even when the user doesn't say "design" explicitly — e.g. "帮我做个登录页", "画几个屏", "这个页面再优化下", "make this screen feel less generic". Helps non-designers discover their aesthetic through side-by-side device-frame previews rather than abstract style words. If a request touches a mini-program visual decision, this skill runs.
---

# WeChat Mini-Program Design

Create multi-screen, capsule-aware, finger-ergonomic mini-program UI that looks like a real product running on a real iPhone — not a marketing mock.

## The prototype is NOT the mini-program (read this first)

This is the single most important framing for the skill. The AI burns the most tokens when it forgets it.

You are producing an **HTML React prototype that looks like a running mini-program**, viewed in Chrome. It is for design review, not for shipping to WeChat. Engineering converts the design into wxml/wxss/js later — they are a downstream consumer, not your runtime.

What this means for your decisions while generating:

- **Use modern CSS freely in the prototype.** `clip-path`, `backdrop-filter`, `:has()`, `mask-image`, view transitions, container queries, scroll-driven animations — all work in the Chrome that renders the prototype. Do not refuse a design choice because "WeChat WebView doesn't support it." That is a handoff concern, not a generation concern.
- **Wire AI features through a single `aiComplete(prompt)` async hook.** The prototype's React component declares one such hook at the top; the body just calls it. The hook has two runtimes: in the prototype (Chrome) it mocks with realistic timing or, when available, calls `window.claude.complete`; in the production mini-program it calls `wx.cloud.extend.AI` directly — **no cloud function proxy needed**, the AI extension is the transport. The UI never changes between the two; only the hook implementation swaps. See *Phase 3 → AI features in prototypes* and the companion `ai-model-wechat` skill for the production call shape.
- **The Rendering Recipes table (next section) is the only place portability matters during generation.** It pre-decides the technique for identity-load-bearing graphics (iconic masks, mood faces, glass panels) so production-degradation is graceful. Everywhere else, the prototype is in Chrome and the prototype gets to use Chrome.
- **Portability is `handoff.md`'s job.** When a screen uses a feature that won't survive WXSS (e.g. `backdrop-filter` as the load-bearing identity, complex `clip-path`, `:has()`-driven logic), note the WXSS-safe equivalent in the handoff doc. Do not pre-degrade the prototype to match production capability.
- **This skill runs in any agent shell with filesystem access.** Cursor, Cline, Aider, Claude Code (terminal or claude.ai), Codex CLI, custom MCP agents — all fine. The deliverable is a design (HTML prototype) + a handoff doc; producing those needs no MCP-specific tool. The companion skills named in `handoff.md` (`miniprogram-development`, `cloudbase`, `ai-model-wechat`, `auth-wechat`) are reading material for whoever picks up the handoff — the dev team or a downstream agent shell — **not runtime dependencies of this skill**. See *Runtime Adapter* for per-shell mechanism details.

If you find yourself deliberating in chat about whether some CSS is mini-program-safe, **stop and re-read this section.** The answer is almost always: yes in the prototype, document the fallback in handoff.

## Core Principles

1. **The capsule is immovable** — every screen is designed around the WeChat top capsule (right side, ~24px from top), the iOS status bar, and the device safe-area bottom inset. Never put content under the capsule. Never propose a layout that ignores it.
2. **Show flows, not screens** — a mini-program is judged on transitions and reactivity, not single hero shots. Always design a flow of 4–6 connected screens (home → write → loading → result → detail → share, etc.). One-screen mocks lie.
3. **Show, don't tell** — generate visual previews in real device frames, not abstract style choices. People discover what they want by seeing it side-by-side.
4. **Distinctive design over "WeChat default"** — Mini-programs all look the same when designers fall back to WeChat's stock vocabulary (white cards, blue links, rounded chips, system fonts). That's the "AI slop" of this medium. Make a deliberate visual thesis.
5. **Finger-first ergonomics** — every tappable target is ≥44px (Apple HIG) / ≥88rpx (WeChat's rpx unit at 750 design width). Hit targets that fail this are not optional polish; they're broken.
6. **Performance is part of the design** — backdrop-blur, big gradients, and complex shadows are real cost in WeChat's WebView (especially on low-end Android). Pick a fidelity level explicitly and design within it.
7. **CJK-first typography** — text in the design is Chinese by default. Don't pick a Latin display font and hope CJK pairs gracefully. Choose the CJK weight first, then pair the Latin counterpart.

## Platform Invariants

Platform truths, not style choices. The rest of this skill assumes them. This section is the **only** place these rules live — feedback patterns and silent-failure CSS catalogs are in the appendices, the canonical rendering technique per case is in *Rendering Recipes*.

### Capsule, launch, navigation

- **Capsule (upper-right) is reserved.** No tap targets under it. Any in-page right-side action must look visually distinct from the capsule — different shape, fill, position. A second pill of similar size next to the capsule is the most common mini-program failure.
- **Launch page is fixed by the platform** — logo-only, no animation, no customization. Don't design one.
- **Tab bar: 2–5 items, ≤4 recommended; one tab bar per page; ≥56px tall excluding safe-area.** Three is the sweet spot for consumer mini-programs.
- **Bottom safe-area** (~34px on iPhone X+; 0 on older devices). Tab bars and bottom-fixed CTAs use `padding-bottom: calc(<value> + env(safe-area-inset-bottom))`. Hard-coded 34px breaks on older devices.

### Stage & canvas

- Every screen is authored at a fixed phone-portrait canvas: **393×852** (iPhone 15 Pro baseline) or **375×812** (iPhone X baseline). Pick one per project and stick to it.
- Every screen sits inside an iOS frame with the WeChat top capsule rendered. The frame is part of the deliverable — naked screens read as mockups, not products.
- The WeChat top capsule sits at the **right side, ~24px below the status bar, ~88×32px**. Titles, back buttons, page actions must clear it.
- Use `clamp()` and viewport units sparingly — you're authoring at 1× pixel scale, not responsive.
- Lay screens out as a flow on a **Design Canvas**. Materialize the `ios-frame.jsx` and `design-canvas.jsx` starters into the deliverable (see *Runtime Adapter* for how your environment fulfills this) — do not hand-draw the bezel or canvas wrapper.

### Tap, type, density

- **Hit targets: ≥44×44px normal, ≥40pt in elderly mode.** Spacing between adjacent tap targets ≥8px. Feedback padding ≥12pt around interactive elements.
- **Floating buttons (FAB) ≥56px circle.**
- **Type ladder reference: 22 / 17 / 15 / 14 / 12 pt** (display / title / subhead / body / caption). In rpx for WXSS handoff: ≥24rpx footnote, ≥28rpx body, ≥36rpx titles. Extend upward for hero typography; never below 12pt for body. This is the system-font floor your custom pairings should beat — if your design at 14pt body reads worse than 苹方 14pt body, your pairing is wrong.

### Accessibility & Care Mode

- **Contrast ≥4.5:1 body text; ≥3:1 for text ≥18pt.** Floor, not guideline. Test against the actual background, not `#FFF`.
- **Honor `fontSizeScaleFactor`.** Care Mode (老年模式 / 关怀模式) scales **content 1.4×**, but **nav-bar and tab-bar heights stay fixed.** Design content blocks that can grow inside fixed chrome.
- **Non-native UI requires `aria-component` annotation** for screen reader support — custom buttons, cards with interactive behavior, tab bars.

### PC adapt

- Unadapted mini-programs render at **414×736** (compact) or **768×1024** (wide) on WeChat PC. Don't rely on swipe-back or pull-down gestures — desktop has neither. PC traffic is real (~10–15% for B2B-leaning products via DingTalk / WeCom integrations). Verify both sizes if the design will ship to PC.

---

## Rendering Recipes (pre-decided — do not deliberate)

When you need to render something, **look it up here and ship.** Do not re-derive the choice from first principles. Every row encodes a decision the skill has already made on your behalf about: identity-portability (will it survive WXSS?), perf cost on Android low-end, asset weight, and engineering handoff complexity.

| If you need to render… | Use this | Don't use this | Notes |
| --- | --- | --- | --- |
| **Iconic mask / cut-out shape** (identity-load-bearing) | Inline SVG with `<mask>` or `<clipPath>` *inside* the SVG; OR pre-rendered PNG with alpha | CSS `clip-path: polygon(...)` on a `<div>` | SVG-internal masking is portable; CSS `clip-path` fails on X5 and ships a square. |
| **"Glass" / blurred translucent panel** | `rgba()` fill + 1px inset highlight + soft shadow as the baseline; `backdrop-filter` layered on top as `@supports` enhancement | `backdrop-filter` as the only thing that creates the glass effect | If the glass is the system identity (Glass Dusk), the opaque-fallback must already look good. Test by toggling backdrop-filter off in DevTools. |
| **Decorative texture** (grain, screentone, noise, halftone) | Pre-rendered tileable PNG (~5–15KB), `background-repeat: repeat` | Live `<feTurbulence>` SVG filter | Filter is 3–5× perf cost on Android and renders inconsistently. |
| **Mood face / small custom icon** (≤48px) | Inline SVG component, ≤2KB each, no filters | Unicode emoji; raster icon | These are *identity*. Keep them as code, hand-tune the curves. |
| **Hero illustration / mascot** (≥120px) | `<img>` pointing at a PNG/WebP asset; user supplies via `image-slot` | Inline SVG > 15KB | Parse cost dominates render past 15KB inline. |
| **Chart / data viz** | Inline SVG for ≤5 series and static; `<canvas>` (production: `<canvas type="2d">` component) for ≥5 series or animated | CSS-only "bar with `width: %`" beyond a single progress bar | Charts have their own perf math. Don't reinvent. |
| **Progress bar / single-value meter** | `<div>` with `transform: scaleX()` or `width: %` + transition on `transform` | `<progress>` element (styling is unreliable cross-browser and on X5) | Animate `transform`, not `width`, for GPU compositing. |
| **Page background gradient** | Linear gradient with ≤3 stops (free on GPU); pre-rendered PNG for radial or ≥4 stops | Multi-stop radial gradients in WXSS at runtime | Linear gradients composite for free. Radial blows the budget on Android. |
| **Animated transition between screens** | CSS `@keyframes` on `transform` + `opacity`, triggered by React state | `view-transition-name` API | View Transitions are not in mini-program WebView. Hand-roll. |
| **Scroll-bound parallax or fade-in-on-scroll** | `IntersectionObserver` + add/remove class | `animation-timeline: scroll(...)` | Scroll-driven animations are unsupported on X5. Restrict to one element per screen on Android. |
| **Press / tap-down feedback** | CSS class toggled by `onTouchStart`/`onTouchEnd` (or `:active` in the prototype); `hover-class` attribute in production WXML | `:hover` for mobile press feedback | Mobile has no hover. The prototype can use `:active`; handoff says `hover-class`. |
| **Shadowed image** | `<view>` wrapping `<image>`, with `box-shadow` on the *wrapper* | `box-shadow` directly on `<image>` | Native `<image>` in WXSS ignores box-shadow. Wrap once, ship everywhere. |
| **Custom CJK font** | Subsetted WOFF2 (≤150KB / weight), `font-display: swap`, system-font fallback declared | Full unsubsetted Noto Sans SC (≥8MB) | Two custom weights total max — see Appendix B for the budget. |
| **Loading state** | Designed full-screen state OR inline skeleton, system-tinted; `weui-toast` spinner only for ≤2s blocking | `weui-toast` for anything > 2s; generic spinner with no design | Loading is its own designed surface, not an afterthought. |
| **Error feedback** | Inline beneath the offending field + summary at top of form | A toast | Toast is success/info only. This is the #1 anti-pattern. |
| **Animated success confirmation** | Brief toast (1.5s, system-tinted, not generic black panel) + immediate UI update | Modal | Modals interrupt; toasts inform. |
| **Bottom-fixed CTA / sheet / tab bar** | `padding-bottom: calc(<value> + env(safe-area-inset-bottom))` | Hard-coded 34px bottom padding | iPhone X+ has 34px; older devices have 0. `env()` handles both. |

**The rule:** if a row exists, use it. If it doesn't and you're tempted to deliberate, ask the user once and add the answer here for next time.

---

## Design Aesthetics

You will tend to converge on "generic mini-program" outputs: white card on light-gray bg, system sans, blue link, pink-purple gradient CTA. Users call this **AI slop**. Avoid it. Make designs that surprise — pick a committed visual thesis that an art-school graduate would defend.

Focus on:

- **Typography** — WeChat's official guidance recommends the **system font stack only** (苹方 / PingFang on iOS, the device-default sans on Android). That is the right floor when nothing else differentiates the product, and it costs zero in T1 latency. Custom CJK fonts (思源黑体 / 思源宋体 / 霞鹜文楷 LXGW WenKai / 阿里巴巴普惠体 / OPPO Sans) paired with a Latin display partner (Anton / DM Serif / Quicksand / Bebas / Instrument Serif) are an **informed override** of that guidance — appropriate in Custom-skinned and Brand-immersive fidelity, where the type pairing IS the personality. Budget the cost (Appendix B), subset CJK aggressively, ship a system-font fallback, and accept the T1 hit consciously. If you don't have a strong typographic thesis, fall back to the system stack and put the differentiation in color, layout, or illustration.
- **Color & Theme** — Commit to a palette. Dominant hue + one sharp accent beats five timid pastels. Borrow from cultural references: 国画 ink-and-color, Y2K candy, 民国 letterpress, 90s 日漫 spot color, golden-hour photography, MUJI muted, 蒸汽波 vaporwave. Don't default to "soft purple + cream."
- **Motion & Reactivity** — Mini-programs feel cheap when they're motionless. Add purposeful transitions: page slide-in (right-to-left), card tap-down (`translate(-1px,-1px)` + shadow collapse), pull-to-refresh, the WeChat-native swipe-back gesture. Animate selection states. CSS transitions ≥150ms. `prefers-reduced-motion` respected.
- **Backgrounds & Texture** — Atmosphere over flat panels. Layer subtle gradients, scattered SVG textures (pixel hearts, screentone, stars, grain), one signature decorative device per system. A flat white background is almost always a missed opportunity in a mini-program — it makes the product look like a v1 internal tool.

Avoid the generic mini-program tropes:

- White rounded-corner card stack on `#F5F5F7` background (the WeChat default)
- 系统 苹方 / Inter at every size — the most boring possible CJK pairing
- Pink-purple gradient CTA with rounded corners and a white inner glow
- Blue link text (`#0080FF`) — that's WeChat's wxss default, not a design choice
- "Three colored stat cards in a row at the top of the home screen" — the universal dashboard cliché
- Emoji used in lieu of designed iconography
- 顶部胶囊 forgotten / overlapped by content

The 微信小程序 medium has more constraints than a landing page; that's the *opportunity*, not the limit. The capsule, the safe-area, the 44px hit target, the WeChat tab bar — these are the system's signature edges, the way a sonnet is constrained. Design with them, not against them.

## Fidelity Modes

Ask the user which fidelity to design at, then design around the answer:

| Fidelity mode | Best for | Design behavior |
| --- | --- | --- |
| **WeChat-native** | Internal tools, B2B, fast handoff to engineering, products where users expect the native WeChat feel | Use WeChat's component vocabulary: blue links, white cards, system 苹方, navigation bar at top. Limited but signal-correct. Avoid for consumer products. |
| **Custom-skinned** | Most consumer products | Custom palette + custom type + custom components, while respecting capsule + tab bar + safe-area. The default. |
| **Brand-immersive** | Hero campaign mini-programs, marketing/anniversary, premium products | Full-bleed atmosphere — gradient/photo backgrounds, custom navigation, hidden tab bar, animated transitions. Highest production cost; highest payoff. Performance budget on Android matters. |

Mention this once in Phase 1. The user picks. The fidelity mode determines everything that follows: type system, color, component vocabulary, performance ceiling.

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Mini-program** — design a flow from scratch. Go to Phase 1.
- **Mode B: Reskin / Mock** — recreate a real mini-program's UI (the user references an existing app — get them to paste code, screenshots, or design system links). Go to Phase 1.2 (Reference acquisition).
- **Mode C: Enhancement** — improve an existing mini-program prototype. Read every screen first, then follow the Modification Rules below. Skip Phase 1 (no questions — the design system is already locked) and Phase 2 (style is already given); modify the existing files directly per the rules, then deliver via Phase 4.

### Mode C: Modification Rules

When enhancing an existing prototype, the biggest risks are: (a) breaking the capsule clearance, (b) breaking the 44px hit-target floor, (c) cluttering the screen with new content that the user didn't ask for.

1. **Before adding content**: count existing elements on the affected screen; check against density limits.
2. **Adding a tab/section**: never add a screen without showing how the user navigates to it and back. New screens must enter the flow.
3. **Adding a new component**: derive it from the existing system's vocabulary (border weight, radius, shadow, color). Never introduce a new visual language for one element.
4. **After ANY modification**: verify the capsule is still clear, every tap target is still ≥44px, the safe-area bottom is respected, and the design canvas still shows the screen.
5. **Proactively reorganize**: if changes will cause the screen to overflow, split into a new screen and tell the user.

---

## Phase 1: Content Discovery (New Mini-Programs)

Ask all the questions at once using the structured-question UI. Don't ask them one at a time.

**Question 1 — Product** (header: "Product"):
What does the mini-program do in one sentence? *(Freeform — short.)*

**Question 2 — User & moment** (header: "User"):
Who is using it and in what moment? Options:
- Quick utility (commute, queue, transaction-shaped)
- Daily ritual (diary, habit, fitness, reading)
- Social / share-first (group, event, content posting)
- Discovery / browse (catalog, content feed, store)
- Heavy entry (form-filling, registration, multi-step task)

**Question 3 — Core flows** (header: "Flows"):
What are the 3–5 screens you need? *(Pick from typical or freeform.)* Examples: Onboarding · Home / list · Create / write · Loading state · Detail / result · Calendar / archive · Profile / settings · Share card · Empty state · Error state

**Question 4 — Fidelity** (header: "Fidelity"):
What level of design polish? Options:
- WeChat-native
- Custom-skinned
- Brand-immersive

*(See the **Fidelity Modes** table earlier in this skill for what each mode means — don't repeat the table to the user.)*

**Question 5 — Design system / brand** (header: "Brand"):
What design assets exist? Options:
- A design system you'll attach
- An existing UI kit (Tencent / WeUI / Vant Weapp / Taro UI)
- A brand kit (logo + palette + fonts) you'll attach
- Nothing — pick the aesthetic for me

> **If the user picks "Nothing"** (the most common case): do not invent the aesthetic from scratch. Consult `design-systems/` — the project's curated library of pre-explored, named systems — and shortlist 2–3 candidates whose axes match the brief. The canonical read order (README → preview.md → design.md) lives in *Supporting Reference → Design-system companion files*; if no `design-systems/` folder exists, offer to draft one or design directly and capture retroactively.

**Question 6 — Tone & references** (header: "Tone"):
Any reference mini-programs, brands, art directions, illustrators, films? *(Freeform — encourage. This is the most valuable question.)*

### Step 1.2: Reference acquisition (Mode B only)

When recreating an existing mini-program, the work splits into **input** (what to ask the user for) and **extraction** (what to do with it). Mode B typically skips Phase 2 — the style is given — jumping from this step straight to Phase 3 once the recreated home screen is confirmed.

**Input — ask for, in order of preference:**

- A GitHub repo link — best for pixel fidelity. Import the repo (mechanism: *Runtime Adapter* — e.g., a managed `github_*` tool, a shelled `git clone`, etc.); read theme files first, then components.
- Screenshots of the target app from multiple angles.
- The UI library the team uses (Vant Weapp, WeUI, Taro UI, ColorUI, iView Weapp) — each has its own vocabulary you can match.
- Brand palette and font specifications.

Importing source > copying screenshots. Hex values lifted from a `theme.ts` will always beat eyeballed values from a screenshot.

**Extraction — when source is available:**

1. **Pull tokens.** Look for `theme.ts`, `colors.css`, `tokens.json`, `variables.scss`, or `app.wxss`. Lift exact hex values, spacing scales, and type ladders verbatim — do not paraphrase.
2. **Identify the component library** in use so you can match its vocabulary — see Appendix A's WeUI / Vant / Taro translation table.
3. **Show a side-by-side first**: extracted source values + a single recreated home screen at the user's canvas. Get confirmation on fidelity before expanding.
4. **Then continue to Phase 3** — generate the remaining screens using the locked-in tokens and components.

### Step 1.3: Asset evaluation (if provided)

If the user attaches images / logos / photographs:
1. **Scan** — list every user-attached asset. (Where attachments live is environment-specific; see *Runtime Adapter*.)
2. **Inspect each** — use image-understanding to extract: subject, dominant colors, usability (sharp / blurry / too-busy), and likely role (logo, hero, content photo, mood reference).
3. **Co-design the screens** — curated photos inform the layout from the start. Don't plan screens then paste photos in.
4. **Logo handling**: if a usable logo is identified, embed it (base64) into every Phase 2 style preview so the user sees their brand styled three different ways.

---

## Phase 2: Style Discovery

**This is the "show, don't tell" phase.** Most users can't articulate aesthetic preferences in words. They can react to side-by-side phones.

### Step 2.0: Generate 3 style previews directly

Based on Product, User moment, Fidelity, and Tone, generate **3 distinct home-screen previews**, each inside an iOS frame with the WeChat top capsule rendered. Each preview must look like a real first screen of the user's product — not a style swatch card.

Do not ask the user whether they want options. The default discovery experience is always side-by-side phones.

**Sourcing the three directions**:

- **If a design system was attached** — use it as one direction; generate 2 distinct alternatives from the project's `design-systems/` library or as custom wildcards.
- **If a brand kit was attached** — generate all 3 around it (different typographic and layout interpretations of the same palette).
- **If the user answered "Nothing" in Q5** (the most common case) — **do not invent from scratch.** Read `design-systems/README.md`, shortlist 2–3 systems whose axes (audience age, time-of-day, shareability, premium signal, build complexity) match the brief, then read those candidates' `preview.md` files (lightweight, ~5KB each — do not read full `design.md` files yet). Use the shortlisted systems as Directions A and B; let Direction C be either a third library system or a custom wildcard if the library's range doesn't cover a useful contrast. This is the canonical Phase 2 path — it costs ~10–15KB of context and produces sharper, more diverse previews than free-form generation.
- **If no `design-systems/` folder exists** — design freely, but capture the resulting system into a new `design-systems/<slug>/` folder retroactively after the user picks (so the next project benefits). Or, before Phase 2, offer to draft one library entry first; this is ~20 minutes upfront and pays off across every future brief.

**Preview mix rules:**

- **Direction A — Safe / committed:** the most likely-correct interpretation of the brief. Restrained, brand-correct, low risk.
- **Direction B — Bold:** a strong typographic or atmospheric thesis. Take a real creative risk.
- **Direction C — Wildcard:** something the user didn't ask for but should consider. Drawn from a cultural reference (Risograph, 国画, Y2K, golden-hour, 民国 letterpress, manga, vaporwave, etc.). Strongest contrast against A and B.

For conservative briefs (B2B / heavy entry / financial), make Direction A especially restrained, Direction B a calm typographic study, Direction C an editorial / book-like direction. Avoid Y2K / neon for these.

For consumer / social / lifestyle briefs, let Direction B be a strong commitment and Direction C an adventurous contrarian.

**Custom-preview rules:**

- Follow the Design Aesthetics section above. No generic AI slop. No purple-gradient-on-white. No system-sans-everywhere.
- Pick deliberately: a distinct CJK type pairing, a committed 4–6 color palette, a recognizable layout system, and one signature decorative device per direction.
- The preview must imply a design system that can expand into write / loading / result / detail / calendar / share — not just look good on the home screen.
- Use the fixed phone canvas (393×852 default) inside the iOS frame with the WeChat top capsule.
- Never render workflow text on screen: no `preview`, `Direction A/B/C`, `style option`, `template`, `wildcard`, `mock`, file names, paths, slug names.
- Use real product chrome only: real product title, real screen title, real date, real user content — never `Lorem` / placeholder.

**Preview authenticity rules:**

A preview that breaks any of these reads as a mockup instead of a real product — and the whole point of Phase 2 is letting the user judge real-product feel side-by-side.

- Every preview must look like a real first screen running on a real phone, not a diagnostic card.
- Capsule visible and uncovered. Status bar correct (signal / WiFi / battery / time).
- If the system has a tab bar, render it; if it has a floating CTA, render it. Don't show partial chrome.
- Real content, not Lorem ipsum. Real Chinese, real product nouns, real dates.
- Frame the previews inside a `design-canvas.jsx` so the user can compare side-by-side, focus one fullscreen, and drag-reorder.

Save the previews to one HTML file. Open it for the user. Tell them which direction is A / B / C **in the chat message** — not on the screens themselves.

### Step 2.1: User picks

Ask (header: "Direction"):
Which direction feels right? Options: Direction A: [name] / Direction B: [name] / Direction C: [name] / Mix elements

If "Mix elements," ask which discrete pieces (e.g., "B's color + A's type + C's texture"). Never mix illustration systems — they're load-bearing and don't blend.

---

## Phase 3: Generate the Full Prototype

Now expand the chosen direction into the full flow.

Read the design system docs (if attached) end-to-end before generating. Treat the design system as the authoritative source of truth — lift hex values, spacing tokens, type scales, and component recipes. Do not paraphrase or "improve" them.

Generate **all the screens the user listed in Question 3**, each as an artboard inside a single `design-canvas.jsx`. The canvas is the deliverable — not loose HTML files for each screen.

Apply the user's fidelity choice throughout:

- **WeChat-native:** use 苹方 / system sans, blue link (`#0080FF`), white cards, official-looking navigation bar at top. Restrained, signal-correct. Borrow from WeUI / Vant Weapp component vocabulary.
- **Custom-skinned:** apply the chosen palette and type pairing to every screen. Keep the WeChat capsule visible but use a custom navigation pattern below it. The default for most consumer products.
- **Brand-immersive:** full-bleed atmosphere. Custom navigation. Animated transitions. Hide the WeChat tab bar; use a floating bottom CTA instead. Highest cost; highest payoff.

### Multi-screen system requirements

A mini-program is a *flow*. The deliverable proves it by having:

- A consistent type ramp across all screens (display / title / body / eyebrow / micro / numeral).
- A consistent component vocabulary across all screens (the same card / button / chip / mood-element across every appearance).
- A consistent navigation pattern (back behavior, tab bar position, capsule clearance).
- At least one **state**: empty state, loading state, error state, or success state, designed in the system's vocabulary.
- A **share card** for any social/consumer product (the screenshot the user will WeChat to friends — designed as a separate artboard, not pasted-in chrome).

### Tweaks panel

Wire 2–4 tasteful tweaks into the prototype using the `tweaks-panel.jsx` starter — switch primary color, switch type pairing, switch density, toggle dark mode, etc. Tweaks let the user re-skin live and make the prototype feel reactive rather than locked. Pick the tweaks that best showcase the chosen design system's flex points; don't expose every variable.

Tweaks read from `localStorage` so refreshing doesn't reset them.

### AI features in prototypes

If the product has an AI feature — interpret-my-dream, generate-a-comic, classify-this-photo, summarize-my-day, suggest-the-next-word, AI chat — wire it through a **single async hook** named `aiComplete(prompt) → Promise<string>` (or `aiImage(prompt) → Promise<url>` for image gen). Declare it once at the top of the prototype's root component; every AI surface calls the same hook. The implementation differs across the prototype runtime and the production mini-program runtime, but the UI never changes.

#### Prototype runtime (Chrome)

The deliverable HTML lives in a browser. There is no `wx.cloud.extend.AI` here. Two implementations of `aiComplete`:

- **Browser exposes `window.claude.complete`** (e.g. claude.ai artifact viewer) — `const aiComplete = (p) => window.claude.complete(p);` Real LLM responses, no setup.
- **Any other browser** (HTML opened from disk, deployed static URL, Chrome on a phone) — mock with realistic timing: `const aiComplete = async (p) => { await new Promise(r => setTimeout(r, 1800)); return CURATED[p] ?? CURATED.default; };` Define a small `CURATED` object with 3–5 realistic responses per feature.

Pick by detecting the runtime once:

```jsx
const aiComplete =
  typeof window !== 'undefined' && window.claude?.complete
    ? (p) => window.claude.complete(p)
    : async (p) => { await new Promise(r => setTimeout(r, 1800)); return CURATED[p] ?? CURATED.default; };
```

For **image / audio / video gen** in the prototype runtime, **always mock** — even when `window.claude.complete` is present: ship a designed loading state (1500–2500ms via `setTimeout`) then a curated static asset. Real-time generation is too slow and unreliable for side-by-side design review. Production handles this differently (see below).

#### Production runtime (mini-program)

In the shipped mini-program, `aiComplete` calls **`wx.cloud.extend.AI` directly** — the AI extension is the transport, no cloud-function proxy needed. Text and image are both real:

```js
// Text — replaces aiComplete in production
const model = wx.cloud.extend.AI.createModel({ provider: 'cloudbase', model: 'deepseek-v3.2' });
const aiComplete = async (prompt) => {
  const res = await model.generateText({ messages: [{ role: 'user', content: prompt }] });
  return res.text;
};

// Image — replaces aiImage in production
const imageModel = wx.cloud.extend.AI.createImageModel({ provider: 'hunyuan-image', model: 'hunyuan-image-v2' });
const aiImage = async (prompt) => (await imageModel.generateImage({ prompt })).url;
```

Exact call shape (`generateText` vs `streamText`, callbacks, data wrappers, error handling) lives in the **`ai-model-wechat` companion skill** — do not invent it inline.

#### Preflight contract (mandatory before production wiring)

The `ai-model-wechat` skill requires a 2-step preflight. The design skill's job is to **document it in `handoff.md` as a checklist** so the dev team can't skip it. Without these, `wx.cloud.extend.AI.createModel(...)` fails opaquely:

1. **Bind the envId** via the `cloudbase` auth tool — the `wx.cloud.init({ env: 'xxx' })` call needs a real env.
2. **Check 成长计划 enrollment** for that envId (`AttendRecords`) — if enrolled, the `hunyuan-exp` group is free; if not, only paid groups (`cloudbase`) work.
3. **Check Token Credits resource pack** balance (e.g. `pkg_token_free_10w`) — non-zero, status active.
4. **Check chosen model group `Status=1`** (active in the env).
5. **Pick group + model** consistent with steps 2–4. Default for this skill's handoff: `cloudbase` + `deepseek-v3.2` (text), `hunyuan-image` + `hunyuan-image-v2` (image).

The handoff template (Phase 5) ships a copy-paste version of this checklist.

#### "AI unavailable" must be a designed state

Production calls fail. Token Credits run out, the env loses 成长计划 status, the network drops, the model returns an error. **Treat "AI unavailable" as a first-class designed state** — designed in the same vocabulary as empty/loading/error, surfaced inline (not as a toast), and delivered as an artboard in the prototype. The mock `CURATED.default` response in the Chrome runtime is one place to preview the copy; the production fallback path uses the same UI.

**Do not deliberate the prototype implementation in chat.** Ship the dual-implementation hook by default. The deliberation is the bug.

### Key requirements

- Single self-contained HTML file (no build step). All CSS/JSX inline or imported as sibling files via `<script type="text/babel" src="…">`.
- Use the React 18 + Babel inline-JSX pattern with the exact pinned versions and integrity hashes from the project's frontend conventions.
- Materialize the starter components — `ios-frame.jsx`, `design-canvas.jsx`, and `tweaks-panel.jsx` — into the deliverable. (Mechanism is environment-specific; see *Runtime Adapter*.) Do not hand-roll device bezels or canvas wrappers.
- Load CJK fonts from Google Fonts (思源宋体 = Noto Serif SC; 思源黑体 = Noto Sans SC; 霞鹜文楷 = LXGW WenKai; etc.). Always preload the weights you actually use.
- Every screen has a clear `/* === SCREEN NAME === */` comment block.
- Component names are specific (e.g., `MangaMood`, `BubbleFace`, `GlassCard`), never generic (`Card`, `Button`, `MoodPicker`).
- `data-screen-label` attributes on each screen root for comment-anchoring during review.
- Each screen sized to its content. Never use `height: 100%` + `overflow: scroll` on a screen artboard — that's slide thinking, not mini-program thinking.

---

## Phase 4: Delivery

1. **Clean up** — delete intermediate / scratch files; keep only the deliverable HTML + sibling `.jsx` modules.
2. **Open the deliverable for the user.** (Environment-specific — a preview/artifact tool, a "done" signal, or writing to a known path and telling the user where; see *Runtime Adapter*.)
3. **Summarize**:
   - File location, direction name, screen count, fidelity mode
   - How to navigate the canvas: drag-pan, scroll-zoom, click an artboard to focus, ←/→/Esc to navigate focus
   - Tweaks panel toggleable from the toolbar
   - How to customize: which CSS variable / component file to edit for which thing
   - Direct-manipulation inline editing: hover any text element to edit copy in place
4. **Offer the natural next steps**: more screens, a different direction, dark-mode pass, share-card design, Figma handoff, engineering handoff.

---

## Phase 5: Share & Export

**Default behavior: produce a small handoff bundle proactively, no question asked.** After delivery, generate:

1. **`export/png/`** — a 2× screenshot pass over every artboard, named `01-home.png`, `02-write.png`, etc. Universal, lightweight (~50KB per screen), readable by anyone (WeChat, Slack, Figma drag-import).
2. **`handoff.md`** — color tokens, type scale, spacing scale, component recipes, rpx conversion note. ~5KB. Engineering can read it without opening the prototype.

This is the **token-efficient default** — no extra skill invocation, no playwright, no user back-and-forth. It costs ~1 screenshot pass and one file write. The user opens the folder and immediately sees what shareable artifacts look like.

Mention the other options as one-liners in the delivery message:
> "I've also saved a PNG set + handoff.md in `export/`. If you want a single PDF, a live shareable URL, or the prototype packaged as a standalone offline HTML, just ask."

Don't ask a multi-choice export question — it costs a round-trip and most users want the default.

### On-request options

These cost more (extra skill loads, extra tooling). Only invoke when the user explicitly asks.

#### PDF (one page per artboard)

Render every artboard to a print-ready PDF (mechanism: *Runtime Adapter* — e.g., a "Save as PDF" sub-skill, headless Chromium `--print-to-pdf`, etc.). Best for printing, email to stakeholders, regulatory review.

#### Live URL

Bundle the prototype as a self-contained offline HTML (mechanism: *Runtime Adapter* — e.g., a "Save as standalone HTML" sub-skill, or inline assets by hand), then deploy. The deployed URL works on phones — the user can WeChat the link to stakeholders for review.

**⚠ Mini-program preview gotcha**: a deployed HTML is NOT a working mini-program. It's a design preview. Tell the user explicitly: this is for review, not for production. To actually ship, engineering converts the design into wxml/wxss/js inside WeChat's IDE — **native WXSS only**, no Tailwind, no `@apply`, no CSS-in-JS, no Sass at runtime. The prototype's CSS is a design contract; the implementation language is fixed by the platform.

#### Figma import

The PNG set IS the Figma import path — users drag PNGs into Figma directly. No separate step needed.

#### WeChat developer tools handoff

The `handoff.md` IS the developer-tools handoff. Engineering opens 微信开发者工具, creates a project, and pastes the CSS variables from `handoff.md` into `app.wxss`. No separate skill needed.

### handoff.md template

The full skeleton (tokens, type scale, component recipes, rpx conversion, **AI features section with preflight checklist + per-feature call shapes + "AI unavailable" state pointers**) lives in **`references/handoff-template.md`**. Read it when writing the handoff doc in Phase 5. Default group/model picks (`cloudbase` + `deepseek-v3.2` for text; `hunyuan-image` + `hunyuan-image-v2` for image) and the 5-step CloudBase preflight checklist are baked in — override only with explicit reason.

Keep it terse. Engineering doesn't want prose; they want token names and recipes.

---

## Supporting Reference

### Design-system companion files

The project's `design-systems/` folder is the canonical companion to this skill. It is structured for progressive disclosure — lightweight selection-index first, full spec only after the user commits to a direction. **Mirror this read order exactly** to avoid burning context on systems the user will reject.

| File / Resource | Purpose | When to Read |
| --- | --- | --- |
| `design-systems/README.md` | Selection index across every system the project ships. Cross-system comparison table, audience axes, build-complexity axes. Tells you which 2–3 systems to shortlist for the brief. | Phase 2 (style discovery, very first) |
| `design-systems/<slug>/preview.md` | Lightweight style card per system (~5KB). Contains slug, tagline, mood, audience, best-for / avoid-for, palette ingredients, signature moves, CJK notes, preview-rendering rules. Read only for shortlisted systems. | Phase 2 (after shortlist, before generating the 3 previews) |
| `design-systems/<slug>/design.md` | Full spec per system (~25KB). YAML frontmatter (tokens, type scale, shadows, spacing, radii, component recipes) + sections on color, typography, layout, depth, illustration prompt scaffold, voice & copy, do/don't, CJK & international, iteration checklist, and known gaps. Read only for the system the user picks. | Phase 3 (after user commits to a direction) |
| `<Product> · Design Systems.html` (e.g. `Diary Comic · Design Systems.html`) | Canonical visual reference doc. Open this when prose isn't enough — it shows every system rendered against itself with real swatches, type samples, and hero compositions. | Phase 2 or 3 (visual sanity check) |

The table's **When to Read** column is the canonical answer. Phase 2 and Phase 3 in-flow guidance restate the key beats; if they conflict with this table, the table wins.

### Starter components & font workhorses

| File / Resource | Purpose | When to Read |
| --- | --- | --- |
| `ios-frame.jsx` (starter) | iOS device bezel with WeChat capsule. Materialize into deliverable per *Runtime Adapter*. | Phase 3 (generation) |
| `design-canvas.jsx` (starter) | Pan/zoom multi-artboard canvas. Required for any multi-screen deliverable. | Phase 3 (generation) |
| `tweaks-panel.jsx` (starter) | Live-toggleable controls panel. Always wired (2–4 default tweaks per prototype). | Phase 3 (always) |
| `image-slot.js` (starter) | User-fillable image placeholders (logo, photo). | Phase 3 (when user assets pending) |
| WeUI / Vant Weapp / Taro UI source | Component vocabulary references. Lift patterns, don't lift code. See `references/component-vocab.md` for the translation table. | Phase 3 (custom-skinned and below) |
| Noto Sans/Serif SC, LXGW WenKai, OPPO Sans, 阿里巴巴普惠体 | The CJK font workhorses. Always preload weights you actually use. | Phase 3 (generation) |

### Companion skills

The design skill ships the prototype + handoff. These siblings are what the dev team (or a downstream agent shell) reads to *implement* the handoff. **They do not need to be installed in the shell running this design skill** — they only need to be reachable by whoever picks up the deliverable. Always name them in `handoff.md` so the path to production is explicit, even when the current shell can't reach them itself.

| Companion skill | Purpose | When to invoke |
| --- | --- | --- |
| `Tweaks Panel.md` | Sub-skill for designing the in-prototype Tweaks panel — control selection, persistence, UI density, conflict handling, ceiling/floor rules. | Phase 3, when wiring the Tweaks panel into the prototype |
| `miniprogram-development` | Project scaffold, `project.config.json`, `appid` setup, WeChat Developer Tools workflow, `miniprogram-ci` preview/upload, real-device debugging, release. | Phase 4 deliverable handoff to engineering. |
| `cloudbase` | EnvId binding, CloudBase resource overview (NoSQL/MySQL, 云函数, 云存储, 云托管), AI extension overview, ops/diagnostics. The umbrella for everything backend-side. | Phase 3 when introducing storage or AI; Phase 5 when writing `handoff.md`. |
| `ai-model-wechat` | The exact `wx.cloud.extend.AI` call shape for `generateText` / `streamText` / `generateImage`, model group selection (`cloudbase` vs `hunyuan-exp` vs `hunyuan-image`), and the mandatory 2-step preflight. Do not invent these inline. | Phase 3 AI features section and Phase 5 `handoff.md` AI section. |
| `auth-wechat` | Mini-program native auth (`wx.login` → OPENID/UNIONID), session handling, `wx.cloud` identity. | Phase 5 `handoff.md` when the design implies user-scoped data (diary entries, saved profiles, social shares). |

### Runtime Adapter

The skill body uses capability-name language ("materialize a starter", "render to PDF", "open the deliverable") and defers the concrete mechanism to the table below. The reason: this skill is meant to run inside more than one coding-agent shell. The body stays portable; the adapter table is where each environment plugs in its specifics.

If you are reading this skill inside a shell not covered below, add a column. If a row's capability is genuinely unavailable in your shell, use the **Generic fallback** column — it is intentionally lowest-common-denominator (file-system + browser + shell) and works almost anywhere. **The Generic fallback column covers Cursor, Cline, Aider, vanilla Claude Code, Codex CLI, and any custom MCP-based agent.** Same call shape; no MCP-specific tool required.

| Capability | Used in | Claude.ai shell (artifact viewer) | Claude Code (terminal / IDE) | Generic fallback |
| --- | --- | --- | --- | --- |
| **Materialize a starter component** | Phase 3 (`ios-frame.jsx`, `design-canvas.jsx`, `tweaks-panel.jsx`) | `copy_starter_component(kind=...)` tool | Read `starters/<file>` → Write to deliverable path | Same as Claude Code — Read + Write |
| **In-prototype LLM call** | Phase 3 AI features (`aiComplete` hook) | `window.claude.complete(prompt)` available in the rendered HTML | Browser opens local file — `window.claude.complete` is absent → use the `setTimeout` + curated-text mock | Same — mock unless a localhost proxy is wired |
| **Open the deliverable for the user** | Phase 4 step 2 | `done` signal / artifact preview | Write HTML to `./prototype.html`; print the absolute path so the user opens it | Same — write + tell user where |
| **Import a Git repo** | Phase 1.2 (Mode B) | `github_*` tools | `git clone` via shell | `git clone` via shell |
| **Extract content from a user-attached image** | Phase 1.3 (asset eval) | Vision-capable model reads attachment directly | Read image via Read tool into vision-capable model | Same |
| **Locate user-attached uploads** | Phase 1.3 | Attachments surface in conversation context | Project root or `./uploads/` as agreed convention | Ask the user where they put them |
| **Render every artboard to PDF** | Phase 5 (PDF option) | "Save as PDF" sub-skill | Headless Chromium: `chromium --headless --print-to-pdf=out.pdf file://prototype.html` | Same Chromium command, or screenshot loop + merge |
| **Bundle prototype as standalone offline HTML** | Phase 5 (Live URL option) | "Save as standalone HTML" sub-skill | Inline `<script>`/`<style>`/base64 images by hand, write `bundle.html` | Same |

**This block is the dependency contract.** Adding a new environment-specific assumption to the body means adding a row here. Removing a capability from the body means removing its row. If a deployment of this skill silently fails, the first place to audit is whether a body section quietly relies on a capability not in this table.

---

## Appendix A · Component Vocabulary

Atomic-component translation table for **WeUI / Vant Weapp / Taro UI** (page background, list row, card, primary/secondary/warn buttons, tag, mood, tab bar, nav bar, input, modal, action sheet, toast, loading, stepper, uploader, empty state), each library's default color palette, the WXSS-vs-browser gotchas that change how design specs must be written (`<image>` ignores `box-shadow`, `placeholder-class` instead of `::placeholder`, `hover-class` instead of `:hover`, `env(safe-area-inset-bottom)` for bottom-fixed chrome), and the cultural pattern law around toasts / form errors / modals / action sheets.

**Lives in `references/component-vocab.md`.** Read it in Phase 3 when picking the component vocabulary for the chosen fidelity mode, and again in Phase 5 when writing `handoff.md`. Not needed for Phase 1 / Phase 2 — keep it out of context until it's actually load-bearing.

---

## Appendix B · Performance Budget

Silent-failure CSS reference (the catalog of features that render as if they weren't there on X5 / older Android WebViews — `backdrop-filter`, `filter`, DOM-level `clip-path`, scroll-driven animations, View Transitions, container queries, `:has()`), the package and asset-weight ceilings (2 MB main package, 500 KB first-screen JS, 200 KB hero image, 150 KB per custom font weight, 2 weights max), the per-frame render-cost budget on Android low-end with concrete multipliers per effect, and the `@supports`-based fallback pattern for `backdrop-filter`.

**Lives in `references/performance-budget.md`.** Read it before generating in Phase 3. **Mandatory for Brand-immersive fidelity** — the budget bites hardest there. Optional for WeChat-native and Custom-skinned unless the brief leans heavily on glass, blur, or long lists. The Rendering Recipes table upstream has already pre-decided the technique for most cases; consult this reference when you're writing `handoff.md` or when Recipes doesn't cover your case.

---

## What "Outstanding" Looks Like

A junior designer thinks the goal is a screen that looks pretty. A master designer knows the goal is a **flow that feels alive** when a finger moves across it. The differences are concrete:

- **Capsule clearance is perfect on every screen.** Not a single title bumps the capsule. This alone signals "designer who has shipped before."
- **The type pairing is the personality.** A user can describe the product by describing the type pairing: "the one with the heavy Anton + Noto 900 + serif body" vs "the one with the dusk gradient + DM Serif italic."
- **The mood system is hand-built, not emoji.** Mini-programs that use Unicode emoji for moods look like prototypes; ones with a hand-built mood-face SVG kit look like products.
- **Every screen earns its place.** No filler. No "About" tab unless the product needs an About tab. No three stat cards at the top of the home screen unless the user actually wants three stats.
- **One signature move per system.** A red drop shadow on exactly one element per screen. A rainbow ribbon at the top of every screen. A sun orb top-right. A drop cap on every body paragraph. One repeated signature — not five.
- **States, not just screens.** Empty state is designed. Loading state is designed. The share card is designed. These are the screens users actually see most.
- **Performance has been thought about.** No 30 stacked backdrop-blur layers on a write screen. No 200KB hero image. No animation at 60fps that drops to 20fps on a Redmi Note.
- **The Chinese reads like a human wrote it.** No `点击查看更多`. No `提示：请输入...`. Real product voice — playful, formal, terse, expansive, whatever the brand requires — but always *intentional*.

The mini-program medium punishes default thinking. Every screen the user opens, they're comparing it (unconsciously) to WeChat itself and to the dozens of mini-programs they've used this week. Designing into that crowded mental field requires *commitment* — to a thesis, a palette, a type pairing, a single decorative device — and the discipline to apply it across every screen.

Make the commitment in Phase 2. Honor it in Phase 3. Defend it in Phase 4.
