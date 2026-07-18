---
name: app-launch-page
description: Use when designing or redesigning a landing page with waitlist for an app launch. Auto-detects brand identity from the project, adapts sections by app type (SaaS, mobile, dev tool), and outputs a complete design spec with copy framework. Works with any AI coding tool.
---

# App Launch Page

Generate a complete landing page + waitlist design specification by reading your project's existing brand identity. Outputs a markdown spec document with adaptive sections, draft copy, and visual direction — ready for implementation with TanStack Start + React 19 + TypeScript (SSR/SSG for full crawlability).

## When to Use

- Building a new landing page for an app launch
- Redesigning an existing landing page that looks too generic or basic
- Adding a waitlist / early access signup to a pre-launch page
- Need a design spec before writing any frontend code

## When NOT to Use

- The page is already built and just needs copy tweaks
- You need a full marketing site with multiple pages (this covers the launch page + minimal supporting pages)
- The project has no existing brand identity and no preferences — help them establish one first

---

## Process

You MUST follow these phases in order. Do not skip phases or combine them.

### Phase 1: Ask the User

Before reading ANY project files, ask the user all of these. Do not proceed until you have answers.

#### Required

1. **App screenshots** — "Where are your app screenshots? Provide separate folders for each platform:"
   - **iOS screenshots** → will be rendered inside `mockup.png` (iPhone frame, co-located with this skill)
   - **Android screenshots** → will be rendered inside `android.png` (Android frame, co-located with this skill)
   - Accepted formats: PNG files of actual device captures
   - If the app is iOS-only or Android-only, only that platform's screenshots are needed
   - **NOTE: Use a 6.1 inch simulator to capture iOS screenshots.** This avoids image scaling/adjustment issues when rendering inside the mockup frame. For Android, use a standard phone-sized emulator.

2. **App icon** — "Where is your app icon PNG?"

3. **Feature list** — "List your app's features in priority order. What's the #1 thing your app does?"

4. **Website pages** — "What pages do you want on your website? Here's a recommended minimal set:"

   **For Mobile Apps (recommended):**
   - Home (landing page) — required
   - Privacy Policy — required for app stores
   - Terms of Service — required for app stores
   - Delete Account — required for app stores (GDPR)

   **For SaaS / Desktop (recommended):**
   - Home (landing page) — required
   - Pricing — if not on the landing page itself
   - Privacy Policy — required
   - Terms of Service — required

   **Optional pages (all types):**
   - Changelog / What's New
   - About / Team
   - Blog
   - Contact / Support
   - Documentation / FAQ

   The user picks which pages they want. The landing page spec covers the Home page. Other pages get a brief structural note in the spec's implementation notes.

5. **Waitlist or launched?** — "Is this a pre-launch waitlist, or is the app already live? This determines whether the primary CTA is email capture or store/download links."

6. **Waitlist endpoint** (if pre-launch) — "Do you already have a waitlist API endpoint set up, or do we need to build one? If you have one, provide:"
   - Endpoint URL (e.g., `POST /api/waitlist`)
   - Request body format (e.g., `{ "email": "user@example.com" }`)
   - Response format for success, duplicate, and error cases
   - Any authentication or headers required

   If no endpoint exists, the spec will include a backend-agnostic API shape that the user can implement separately or that gets built as part of the implementation plan. The frontend waitlist component will be wired to whatever endpoint is provided — or to a placeholder path (`/api/waitlist`) with clearly marked TODOs if none exists yet.

7. **Real metrics & social proof** — "Do you have any REAL metrics or reviews you'd like to showcase? Only provide what actually exists:"
   - App store rating + review count (e.g., "4.8 stars, 2.3k reviews")
   - Download / user count (e.g., "10,000+ downloads")
   - Press mentions or awards (e.g., "App of the Day", "Featured in TechCrunch")
   - Real user testimonials (quote + name + role)
   - Any other verifiable metric

   **CRITICAL: If the user has no real metrics, do NOT fabricate them. Do NOT add placeholder stats, fake testimonials, or invented numbers. Skip the social proof section entirely. A landing page without social proof is far more trustworthy than one with fake data. Instead, focus the page on features, product screenshots, and the value proposition — these speak for themselves.**

#### Optional

8. **Style references** — "Share any landing pages you admire. What specifically did you like about each?"
9. **Brand colors override** — "Are you happy with your existing brand colors, or do you want to adjust the palette for the website?"
10. **Font override** — "Do you want to keep your app's fonts, or prefer something different for the web?"
11. **Dark or light** — "Any preference for dark or light theme? (If unsure, we'll derive from your app's existing theme)"
12. **Additional instructions** — "Any specific requirements, constraints, or preferences?"

#### Derived from answers (do NOT ask — decide yourself)

Based on the user's style direction, existing brand, and app type, decide:
- **Background style**: gradients, solid colors, section alternation strategy
- **Decorative elements**: blobs, glows, geometric shapes, or none — match the brand
- **Animation approach**: CSS-only vs Framer Motion (see Phase 3)
- **Typography treatment**: weight, tracking, line height derived from brand personality
- **Color application**: text hierarchy, section backgrounds, component colors
- **Mockup usage**: which platform mockup(s) to use based on screenshots provided

**IMPORTANT:** If the user gives additional instructions at any point, follow them. User instructions always override skill defaults.

### Phase 2: Brand Discovery

Auto-detect the project's design DNA. Read files in this priority order — stop once you have enough signal:

1. **Theme / design token files** — CSS custom properties, Tailwind config/theme, design token files (`colors`, `typography`, `spacing`)
2. **Existing pages or components** — extract color usage, font stacks, border radius, shadow patterns from current UI code
3. **App icon / logo files** — search `assets/`, `static/`, `public/`, `web/static/` for PNG/SVG icons and logos. The website header and footer MUST use the app's actual icon — never just a text wordmark without the icon.
4. **Package/config files** — app name, description, tagline from `package.json`, `pubspec.yaml`, `Cargo.toml`, `pyproject.toml`, `setup.py`, etc.
5. **README or docs** — project description, target audience, key features
6. **App store metadata** — if present, app descriptions and category

Assemble a **Brand Profile**:

```
App Name:        [detected]
Tagline:         [detected or "needs input"]
App Icon:        [path to highest quality PNG/SVG — will be used in header + footer]
Primary Color:   [hex + human-readable name, e.g. #9B1B30 "wine"]
Color Palette:   [full palette with shade scale if available]
Typography:      [heading font + body font, e.g. "Lora (headings) + Open Sans (body)"]
Design Tokens:   [radius, shadows, spacing scale — whatever exists]
App Type:        [SaaS | Mobile App | Desktop App | Dev Tool | API/Platform]
Target Audience: [detected or "needs input"]
Key Features:    [top 3-5 from docs/code]
Tone:            [derived from existing copy — professional, playful, technical, warm, minimal]
Platforms:       [iOS | Android | Both | Web | Desktop]
```

**Brand identity rules:**
- The website MUST use the same heading + body font as the app. Detect these from the theme file (e.g., `theme.dart`, `tailwind.config`, CSS variables). Load via Google Fonts with `preconnect` + `display=swap`.
- The app icon MUST appear in the header (next to the wordmark) and footer. This creates instant brand recognition and coherence between the product and its marketing site.
- Never invent a "marketing font" or "website logo" — the website is the product's face on the web.

**Present the Brand Profile to the user for confirmation.** Ask them to correct anything wrong and fill in any "needs input" fields. Do NOT proceed until confirmed.

### Phase 3: App Type Template Selection

Based on the confirmed **App Type**, load the matching template from `design-patterns.md`. Each template defines:

- **Layout blueprint** — exact section order and spatial relationships
- **Visual characteristics** — color strategy, typography rules, component styles specific to this app type
- **Copy tone** — how headlines and body text should sound for this category
- **Device mockup strategy** — which mockup frame(s) to use

**App Type Detection Heuristics:**

| Signal | App Type |
|--------|----------|
| `pubspec.yaml` with Flutter, iOS/Android folders | Mobile App |
| `package.json` with Next.js/Nuxt/SvelteKit + API routes, dashboard UI | SaaS |
| `Cargo.toml`, CLI binary structure, `.exe`/`.dmg` builders | Dev Tool / Desktop |
| `openapi.yaml`, `/api/` route structure, SDK folders | API/Platform |
| Electron, Tauri, SwiftUI `.app`, `.dmg` config | Desktop App |
| Multiple signals present | Ask user to clarify primary |

**Device Mockup Selection:**

| User provided | Mockup used |
|--------------|-------------|
| iOS screenshots only | `mockup.png` (iPhone frame) |
| Android screenshots only | `android.png` (Android frame) |
| Both iOS + Android | Both frames — hero uses primary platform, features alternate |

Present the selected template's section list to the user. They can add, remove, or reorder sections.

**Animation Decision:**

**Default to CSS-only.** A landing page does not need an animation library. CSS transitions + `IntersectionObserver` cover 90% of landing page animation needs with zero bundle cost. Only add a library when the user explicitly asks for complex animations (parallax, scrub, orchestrated timelines, text splitting).

| Need | Use |
|------|-----|
| Scroll reveals (fade-in, slide-up), hover effects, transitions | **CSS transitions + IntersectionObserver** — zero dependencies, best Lighthouse score |
| Complex orchestration the user explicitly requests (parallax, scrub, staggered timelines, text splitting) | **GSAP + ScrollTrigger** — `pnpm add gsap`, works with any framework. Only add when CSS alone can't achieve what the user wants. |
| Spring physics, layout animations (React only) | **Framer Motion** — only if the user asks for it |

**Why CSS-first matters:**
- Every animation library adds bundle size (GSAP ~25KB, Framer Motion ~30KB). Landing pages must score 90+ on Lighthouse Performance.
- CSS `transition` and `@keyframes` run on the compositor thread — they don't block the main thread.
- `IntersectionObserver` is native, efficient, and sufficient for scroll-triggered reveals.
- An animation library that slightly improves easing curves is not worth the Lighthouse penalty unless the user specifically wants those interactions.

**CSS-only patterns (default):**

```css
/* Scroll reveal base */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease-out, transform 0.7s ease-out;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
}
```

```javascript
// IntersectionObserver for scroll triggers
const observer = new IntersectionObserver(
  (entries) => entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  }),
  { threshold: 0.15 }
);
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

**Animation timing guidelines (applies to all approaches):**
- Section reveals: 0.6-0.8s duration, ease-out, 20-28px translateY
- Hero entrance: orchestrate with staggered delays (0.1-0.15s between elements), not simultaneous
- Overline text: use `letter-spacing` expansion (0.05em → 0.15em) + subtle x-shift for editorial feel — avoid plain fade-up on small uppercase text
- Card grids: stagger 0.08-0.12s between cards
- Hover effects: 0.2-0.3s, subtle (scale 1.02, shadow increase)
- Always `once: true` — don't re-trigger animations when scrolling back
- Always check `prefers-reduced-motion` and provide instant-visible fallback

**When the user requests GSAP (complex animations only):**
- Always use `gsap.context(callback, scope)` and return `ctx.revert()` for cleanup
- Register plugins once: `gsap.registerPlugin(ScrollTrigger)`
- Animate only `transform` and `opacity` — never `width`, `height`, `top`, `left`
- Use `will-change: transform, opacity` only on elements that actually animate
- Use `once: true` on ScrollTrigger to avoid re-triggering

Note the decision in the spec.

### Phase 4: Visual Direction

Read `design-patterns.md` for the selected app type's visual characteristics. Then derive the specific visual direction from the Brand Profile.

Do NOT ask mood/style questions — infer everything from the brand's existing design language.

Generate a **Visual Direction** covering:

**Layout & Spacing**
- Content max-width (typically 680-800px for text, 1100-1200px for full layouts)
- Section vertical padding: 150-200px between major sections (desktop), 96-120px (mobile). This aggressive spacing is what separates premium from generic — it signals confidence.
- Feature section internal spacing: 128-160px between alternating text/mockup pairs
- Grid columns and gaps: 80-96px between text and mockup columns
- The "breathing room" principle: generous whitespace is a design element, not wasted space. When in doubt, add more space.

**Color Application**
Map the detected palette to specific page roles:
- Primary → CTAs, accents, active states, links
- Background strategy → section alternation (white/light gray, or dark theme if brand supports it)
- Text hierarchy → headings (near-black), body (dark gray), muted (medium gray)
- Contrast breaks → placement of ONE dark/colored section for visual rhythm
- Decorative elements → brand color at low opacity for glows, backgrounds

**Typography Scale**
- h1: 48-72px, bold/black weight, tight line-height (1.1-1.2), tight letter-spacing (-0.02em)
- h2: 32-40px section headings
- h3: 24-28px subsection/feature titles
- Body: 16-18px, line-height 1.5-1.6, max-width 540-640px for readability
- Use the detected heading + body font pairing

**Component Style**
- Buttons: primary color fill, matching border-radius from design tokens, 48-52px height, bold text
- Cards: subtle border (1px, low opacity) OR soft shadow, consistent internal padding (24-32px), radius from tokens. **Cards in a grid row MUST be equal height** — use `h-full` on the card container so varying content length doesn't produce uneven rows.
- Card icons: use inline SVG inside a fixed-size container (e.g., 40x40px rounded box with a subtle background tint — `bg-gray-100` on light sections, `bg-white/5` on dark). Use Heroicons, Lucide, or custom SVGs with `aria-hidden="true"`. **Never use emoji characters as icons** — they render inconsistently across platforms and look unprofessional.
- Input fields: generous padding (14-16px), visible border, brand-color focus ring
- Badges/pills: small, rounded, primary color at low opacity with primary text

**Device Mockups**

Both mockups use the same technique: a device frame PNG with a screenshot overlaid inside the screen area using absolute positioning with percentage offsets. The screen coordinates are pre-measured from the frame image.

**iOS — `mockup.png` (iPhone frame, gold):**
```
Frame: 1022 × 2082 px
Screen area: left 52px, top 46px, width 918px, height 1990px
Border radius: 126px on both axes

MK_W  = 1022;   MK_H  = 2082;
SC_L  = (52  / MK_W)  * 100;   // screen left %
SC_T  = (46  / MK_H)  * 100;   // screen top %
SC_W  = (918 / MK_W)  * 100;   // screen width %
SC_H  = (1990/ MK_H)  * 100;   // screen height %
SC_RX = (126 / 918)   * 100;   // border-radius x %
SC_RY = (126 / 1990)  * 100;   // border-radius y %
```
Use a **6.1 inch simulator** for iOS screenshots to avoid scaling issues.

**Android — `android-mockup.png` (Pixel 8 frame, dark):**
```
Frame: 978 × 2100 px
Screen area: left 33px, top 49px, width 902px, height 2002px
Border radius: 40px on both axes

AMK_W = 978;    AMK_H = 2100;
ASC_L = (33  / AMK_W) * 100;   // screen left %
ASC_T = (49  / AMK_H) * 100;   // screen top %
ASC_W = (902 / AMK_W) * 100;   // screen width %
ASC_H = (2002/ AMK_H) * 100;   // screen height %
ASC_RX= (40  / 902)   * 100;   // border-radius x %
ASC_RY= (40  / 2002)  * 100;   // border-radius y %
```
Use a standard phone-sized emulator for Android screenshots.

**Component pattern (framework-agnostic):**
```html
<div style="position: relative; aspect-ratio: {FRAME_W}/{FRAME_H};">
  <!-- Device frame -->
  <img src="/mockup.png" alt="" style="display: block; width: 100%; height: 100%;" />
  <!-- Screenshot overlay -->
  <div style="
    position: absolute; z-index: 10; overflow: hidden;
    left: {SC_L}%; top: {SC_T}%; width: {SC_W}%; height: {SC_H}%;
    border-radius: {SC_RX}% / {SC_RY}%;
  ">
    <img src="{screenshot}" alt="{description}" style="display: block; width: 100%; height: 100%; object-fit: fill;" />
  </div>
</div>
```

- Show real app screenshots — NEVER placeholder screens
- Use `object-fit: fill` (not `cover`) to avoid cropping
- Placement: centered or offset per layout blueprint, slight shadow for depth
- On feature sections: alternate between platforms if both available

**Motion**
- Default: CSS transitions + `IntersectionObserver` for scroll reveals (0.6-0.8s, ease-out). No animation library needed.
- Hero entrance: orchestrate a staggered sequence — overline → headline → body → CTA → mockup, with 0.1-0.15s delays between elements. Use `letter-spacing` expansion on overlines for editorial feel.
- Section reveals: fade-up (opacity 0→1, translateY 24-28px→0), triggered once when element enters viewport.
- Only add GSAP/Framer Motion if the user explicitly requests complex animations (parallax, scrub, text splitting, spring physics).
- Always respect `prefers-reduced-motion` — disable all motion, show content immediately.
- Lighthouse target: animations must not impact TBT (Total Blocking Time) or CLS. Use `will-change` sparingly, only on elements that actually animate.

**Responsive**
- Mobile-first
- Breakpoints: mobile (<640px), tablet (640-1024px), desktop (>1024px)
- Navigation: minimal on desktop, hamburger or hidden on mobile
- Cards/grids: 1 col mobile → 2 col tablet → 3 col desktop
- Device mockups: scale down proportionally, never crop

### Phase 5: Copy Framework

Generate draft copy for every selected section. Read the copy tone guidelines from `design-patterns.md` for the selected app type.

**Universal Copy Rules:**

Headlines:
- Lead with the outcome, not the feature
- Max 8-10 words for hero headline
- Use the app's detected tone
- Formula: [Outcome] + [Without Pain Point] or [Outcome] + [For Audience]
- Add personality: inline SVG icons, animated text (Tailwind `animate-*` or Framer Motion), deliberate line breaks, or bold/colored key words. Never use emoji — use SVGs or animated components instead.

Subheadlines:
- Expand the headline with specifics, 15-25 words
- Address "how" or "why believe us"

Body copy:
- 2-3 sentences max per paragraph
- Active voice, present tense, "you" not "users"
- Conversational > corporate

CTAs:
- Primary: action-oriented ("Get Early Access", "Join the Waitlist", "Download Free")
- Secondary: lower commitment ("See How It Works", "View Pricing")
- Microcopy below: anxiety reducer ("No spam ever", "Free during beta", "Cancel anytime")
- Repeat primary CTA 2-3 times across the page in different contexts

Feature descriptions:
- Benefit headline (not feature name): "Never miss a deadline" > "Smart Notifications"
- 1-2 sentences: what it does + why it matters
- Consistent format across all features

Social proof (ONLY if real data was provided in Phase 1):
- Stats: [Number] + [What] — only verified numbers ("2,000+ downloads", "4.8 star rating")
- Testimonials: quote + name + role — only real user quotes, never fabricated
- Awards/badges: only actual awards ("App of the Day", press mentions)
- **If no real metrics exist: SKIP this section entirely.** Do not add placeholders, do not add "500+ users" if there aren't 500 users, do not invent testimonials. A clean page with no social proof is more credible than one with fake data. Focus on features and product screenshots instead.

**Output format for each section:**

```
## [Section Name]

### Overline (optional)
[category label, e.g. "PRODUCTIVITY" or "HOW IT WORKS"]

### Headline
[draft headline]

### Subheadline
[draft subheadline — if applicable]

### Body
[draft body copy — if applicable]

### CTA
Primary: [button text]
Secondary: [link text — if applicable]
Microcopy: [text below button — if applicable]

### Visual Notes
[what visual/screenshot/mockup appears alongside this copy]
[specify: mockup.png (iOS) or android.png (Android) with which screenshot]
```

### Phase 6: Waitlist Component Spec

Design a simple, high-converting email capture. Read the waitlist patterns from `design-patterns.md`.

Skip this phase if the app is already launched — replace with store badge / download CTA spec instead.

**Structure:**
- Single field: email only (no name, no phone — minimize friction)
- Input + submit button on same row (desktop), stacked (mobile)
- Social proof line below or above ("Join X others on the waitlist")
- Anxiety reducer below button ("No spam. Unsubscribe anytime.")

**States:**
- Default: empty input with placeholder "you@email.com"
- Focus: brand-color outline ring
- Loading: spinner in button or subtle pulse
- Success: form replaced with "You're in! You're #[position] on the list."
- Error: red border + inline message, form remains editable
- Already registered: friendly message, no error styling

**Placement:**
- Primary: embedded in Hero section (above fold)
- Secondary: standalone Final CTA section (before footer)
- Both instances submit to the same endpoint

**API Integration:**

If the user provided an existing endpoint in Phase 1 (question 6):
- Wire the form to their endpoint URL, request format, and response handling
- Match their error codes and response body structure in the form state logic
- Document any required headers or auth in the spec

If no endpoint exists:
- Use the default API shape below as the spec
- Mark the endpoint as a TODO in implementation notes — the frontend form will POST to `/api/waitlist` but the backend handler needs to be built
- Include the API shape in the spec so the user (or a backend subagent) can implement it

**Default API shape (used when no endpoint exists):**
```
POST /api/waitlist
Body: { "email": "user@example.com" }

200: { "position": 42, "message": "You're on the list!" }
409: { "message": "You're already on the list!" }
400: { "message": "Please enter a valid email" }
```

### Phase 7: Assemble Spec Document

Combine all phases into a single markdown spec. Save to:

```
docs/specs/landing-page-spec.md
```

Or the project's existing spec/docs directory if one exists.

**Spec document structure:**

```markdown
# [App Name] — Landing Page Design Specification

> Auto-generated from project brand identity on [date].
> Review and adjust before implementation.

## 1. Brand Profile
[from Phase 2 — the confirmed brand profile]

## 2. Pages
[list of pages from Phase 1 question 4, with brief purpose]
- Home (landing page) — this spec
- Privacy Policy — legal requirement
- Terms of Service — legal requirement
- [other pages selected by user]

## 3. Page Structure
[ordered section list from Phase 3, with brief purpose for each]

## 4. Visual Direction

### Layout
[spacing, grid, content width]

### Color Map
[primary, backgrounds, text hierarchy, contrast sections]

### Typography
[heading/body specs with exact sizes, weights, line-heights]

### Components
[buttons, cards, inputs, badges — with exact specs]

### Device Mockups
[which mockup frames, how screenshots map to them]
- iOS: mockup.png frame + [list of screenshots and where they appear]
- Android: android.png frame + [list of screenshots and where they appear]

### Motion
[CSS-only or Framer Motion — with specific animation specs]

### Responsive
[breakpoints, reflow behavior]

## 5. Section-by-Section Content

### 5.1 Hero
[copy + visual notes + mockup assignment]

### 5.2 [Next Section]
[copy + visual notes]

... [one subsection per selected section]

## 6. Waitlist Component (or Download CTA)
[full spec from Phase 6]

## 7. Implementation Notes

### Stack
- **Framework:** TanStack Start + React 19 + TypeScript
- **Rendering:** SSR with static prerendering (SSG) for landing pages — full HTML in initial response for crawlers
- **Routing:** TanStack Router (file-based, type-safe)
- **Styling:** [Tailwind CSS | CSS Modules — match project convention]
- **Animations:** CSS transitions + IntersectionObserver (default) | GSAP + ScrollTrigger (if user requested) | Framer Motion (if user requested, React only)
- **Device mockups:** mockup.png (iOS) + android.png (Android) from skill assets

### Additional Pages
[brief structural note for each non-landing page selected in Phase 1]

### Assets Required
- mockup.png — iPhone device frame (included with skill)
- android.png — Android device frame (included with skill)
- App icon PNG
- iOS screenshots: [list with filenames]
- Android screenshots: [list with filenames]
- OG image (1200x630) — to be generated

## 8. SEO, Accessibility & Web Crawlers

### SEO (Search Engine Optimization)

**Critical: Canonical URL consistency.** Choose ONE primary domain (e.g., `https://thedeadliner.app`) and use it everywhere — canonical tags, sitemap, robots.txt, OG URLs, JSON-LD. Mixed domains (`deadliner.app` vs `thedeadliner.app`) confuse search engines about which domain is authoritative. Audit every file before shipping.

**SEO component pattern — create a reusable component with these defaults:**
- Accept per-page props: `title`, `description`, `canonical`, `image`, `noindex`, `jsonLd`
- Set sensible defaults (app name, default description, primary domain, OG image path)
- Render ALL meta tags from one component so nothing is missed

**Meta tags (server-rendered in `<head>`):**
- `<title>` — "[App Name] — [Tagline]" (max 60 chars)
- `<meta name="description">` — value proposition summary (max 155 chars)
- `<link rel="canonical">` — canonical URL (MUST match primary domain exactly)
- `<meta name="robots" content="index, follow">` for public pages
- `<meta name="robots" content="noindex, follow">` for private pages (payment success/cancel, reset, delete-account, verify-email)
- `<meta name="author">` — app name or company
- `<meta name="theme-color">` — brand primary color

**Open Graph (social sharing):**
- `og:title`, `og:description`, `og:image` (1200x630 PNG), `og:image:alt`, `og:image:width` (1200), `og:image:height` (630)
- `og:type` = "website"
- `og:url` = canonical URL
- `og:site_name` = app name
- `og:locale` = "en_US"

**Twitter Card:**
- `twitter:card` = "summary_large_image"
- `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt`

**Structured Data (JSON-LD in `<head>`):**

Default (every page):
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "[App Name]",
  "url": "[canonical URL]",
  "publisher": { "@type": "Organization", "name": "[App Name]", "logo": { "@type": "ImageObject", "url": "[logo URL]" } }
}
```

Homepage (additional):
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[App Name]",
  "description": "[tagline]",
  "applicationCategory": "[category]",
  "operatingSystem": "[iOS, Android, etc.]",
  "offers": { "@type": "AggregateOffer", "lowPrice": "0", "highPrice": "[price]", "priceCurrency": "USD" }
}
```
- Add `aggregateRating` ONLY if real ratings exist
- Add `review` ONLY if real reviews exist

**Favicons & App Icons:**
- `favicon-16x16.png`, `favicon-32x32.png` — browser tab
- `apple-touch-icon.png` (180x180) — iOS home screen
- `site.webmanifest` with 192px and 512px icons (include maskable)
- Theme color in manifest matching brand primary

**Sitemap (`sitemap.xml`):**
- List ONLY public, indexable pages (home, pricing, privacy, terms)
- Do NOT include noindexed pages (payment, reset, delete-account, verify)
- Set realistic priorities: home (1.0), pricing (0.9), legal pages (0.5)
- Set realistic changefreq: home (weekly), pricing (monthly), legal (yearly)
- Auto-generate `lastmod` from build date
- Prerender the sitemap at build time for static sites

**robots.txt:**
- Block private/transactional pages: `/reset`, `/payment-success`, `/payment-cancel`, `/delete-account`, `/verify-email`
- Allow everything else
- Reference sitemap: `Sitemap: https://[domain]/sitemap.xml`
- Domain in sitemap URL MUST match canonical domain

**Performance SEO (Lighthouse targets):**
- LCP < 2.5s — hero content server-rendered, no layout shift
- CLS < 0.1 — explicit dimensions on all images/mockups, no content shift from animations
- FCP < 1.8s — minimal JS bundle, critical CSS inlined
- TBT < 200ms — animations must not block main thread
- Lighthouse Performance score target: 90+

### Web Crawler Optimization

**Why TanStack Start (SSR/SSG):**
Landing pages MUST serve complete HTML content on first response. Search engine crawlers (Googlebot, Bingbot) and social media scrapers (Twitter, Facebook, Slack, iMessage link previews) do not reliably execute JavaScript. CSR pages appear blank to crawlers, killing SEO and social sharing.

**Requirements:**
- All text content (headlines, descriptions, feature copy) rendered as real HTML elements in the server response — NOT injected via JavaScript after hydration
- All `<meta>`, `<title>`, Open Graph, and JSON-LD tags present in the initial HTML `<head>`
- Images use `<img>` tags with `alt`, `width`, `height` attributes (not CSS background-image for content images)
- Internal links use `<a href>` tags (not JavaScript click handlers for navigation)
- No content hidden behind JavaScript-only interactions for primary page content
- `robots.txt` allows crawling of all public pages
- `sitemap.xml` generated and referenced

**Static prerendering (SSG):**
- Landing page and legal pages (privacy, terms) should be statically prerendered at build time
- This produces plain `.html` files that serve instantly — zero server-side computation at request time
- TanStack Start supports this via prerender configuration

**Testing crawlability:**
- View page with JavaScript disabled — all content should be visible
- Use `curl -s [URL]` and verify HTML contains actual content, not empty `<div id="root">`
- Check Google Search Console after deployment for indexing issues

### Accessibility (WCAG 2.1 AA)

**Semantic HTML:**
- Use proper heading hierarchy: one `<h1>` per page, `<h2>` for sections, `<h3>` for subsections
- Use landmark elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`
- Each `<section>` should have an `aria-label` or `aria-labelledby`
- Use `<button>` for actions, `<a>` for navigation — never `<div onClick>`
- Forms: every `<input>` has a visible `<label>` (or `aria-label`)

**Color & Contrast:**
- Text on background: minimum 4.5:1 contrast ratio (AA)
- Large text (18px+ bold or 24px+): minimum 3:1
- UI components and graphical objects: minimum 3:1 against adjacent colors
- Never convey information through color alone

**Keyboard Navigation:**
- All interactive elements reachable via Tab key
- Visible focus indicators (`:focus-visible`) on all interactive elements — use brand color outline
- Skip-to-content link as first focusable element
- No keyboard traps — users can always Tab away from any element
- Escape key closes modals/menus

**Motion & Animation:**
- Wrap all animations in `@media (prefers-reduced-motion: no-preference)`
- Provide `prefers-reduced-motion: reduce` alternative that disables motion
- No auto-playing animations that cannot be paused
- No flashing content (3 flashes per second max)

**Images:**
- All content images have descriptive `alt` text
- Decorative images use `alt=""` and `aria-hidden="true"`
- Device mockup images: `alt` describes the app screen shown, not the device frame

**Screen Reader:**
- Dynamic content updates (waitlist form states) announced via `aria-live` regions
- Error messages linked to inputs via `aria-describedby`
- Loading states communicated via `aria-busy` or live region

### Analytics
- Event tracking on CTA clicks, waitlist submissions, scroll depth
- Track without blocking render — load analytics scripts with `defer` or `async`
```

### Phase 8: User Review

Present a summary of the assembled spec — section list, key visual decisions, and sample copy — directly in the conversation.

Ask the user to review the full spec document. Iterate on any feedback.

The spec is the deliverable of the design phase.

### Phase 9: Implementation Planning

After the spec is approved, transition to implementation using subagent-driven development:

1. **Create implementation plan** — Break the spec into discrete, parallelizable tasks:
   - Project scaffolding (TanStack Start + React 19 + TypeScript)
   - SSR/SSG configuration (prerender landing + legal pages)
   - Component hierarchy (layout, sections, shared components)
   - Each section as an independent task
   - Waitlist integration
   - SEO setup (meta tags, OG, JSON-LD, sitemap, robots.txt)
   - Accessibility pass
   - Responsive polish
   - Animation pass

2. **Dispatch subagents** — Use parallel subagents for independent sections:
   - Each subagent gets: the full spec, its assigned section(s), brand profile, and asset paths
   - Subagents work in isolated worktrees to avoid conflicts
   - Shared components (Header, Footer, Button, device mockup components) are built first in the main branch

3. **Integration** — Merge subagent work, resolve any conflicts, verify the full page

### Phase 10: Review & QA

After implementation is complete, run a structured review:

1. **Code review** — Use the code-reviewer agent to verify:
   - React 19 + TanStack Start best practices
   - TypeScript strictness (no `any`, proper typing)
   - Accessibility compliance (WCAG 2.1 AA)
   - Performance (no unnecessary re-renders, optimized images)
   - Responsive behavior across breakpoints

2. **SEO & crawler review** — Verify:
   - `curl` the page and confirm HTML contains all text content (not empty shell)
   - All meta tags, OG tags, and JSON-LD present in `<head>` of server response
   - **Canonical URL audit**: grep all `.svelte` and `.ts` files for the domain — every occurrence must use the same primary domain. Mixed domains is a critical SEO bug.
   - `robots.txt` blocks private pages, references sitemap with correct domain
   - `sitemap.xml` lists only public pages, uses correct domain, has realistic priorities
   - Private pages have `noindex={true}` prop on SEO component
   - OG image loads at the URL specified in meta tags (test with `curl -I [og:image URL]`)
   - Disable JavaScript in browser — all content still visible
   - No social proof, ratings, or testimonials unless real data was provided

3. **Visual review** — Compare implementation against spec:
   - Colors match brand profile
   - Typography matches scale
   - Spacing matches rhythm
   - Device mockups render correctly with screenshots
   - Animations are smooth and respect reduced motion

4. **Accessibility review** — Verify:
   - Keyboard navigation works end-to-end (Tab through entire page)
   - Focus indicators visible on all interactive elements
   - Screen reader announces content in logical order
   - Color contrast passes WCAG AA on all text
   - `prefers-reduced-motion` disables animations

5. **Functional review** — Verify:
   - Waitlist form submits correctly (all states work)
   - All links and CTAs work
   - Navigation works on all breakpoints
   - No console errors

6. **Bug squash** — Fix any issues found in review before marking complete

---

## Quality Checklist

Before marking the spec or implementation as complete, every item must pass:

### Spec Quality
- [ ] Brand profile confirmed by user — no assumed values
- [ ] Every section has a clear purpose tied to conversion
- [ ] All copy passes the "one second test" — readable at a glance
- [ ] No two adjacent sections share the same layout pattern
- [ ] Device mockups show real app screenshots, never placeholders
- [ ] Social proof uses ONLY real metrics — or is absent entirely
- [ ] Waitlist/CTA appears 2-3 times (hero, mid-page, final) without feeling repetitive

### Visual Quality
- [ ] Color usage matches the brand profile — no invented palette
- [ ] Typography hierarchy is clear: h1 > h2 > h3 > body > muted
- [ ] Generous whitespace between sections (120-200px)
- [ ] At least one contrast section for visual rhythm
- [ ] Decorative elements (if any) support the message, don't block content
- [ ] Responsive behavior defined for all three breakpoints
- [ ] Card grids have equal-height cards across each row
- [ ] No emoji characters anywhere — all icons are inline SVGs in fixed-size containers

### Technical Quality
- [ ] `curl` returns full HTML with all content (not empty shell)
- [ ] All meta tags, OG, and JSON-LD present in server-rendered `<head>`
- [ ] **Canonical URL consistency** — every canonical, sitemap URL, robots.txt sitemap reference, OG url, and JSON-LD url uses the SAME domain. No mixed `app.com` vs `theapp.com`.
- [ ] `robots.txt` blocks private pages and references sitemap with correct domain
- [ ] `sitemap.xml` lists only public indexable pages with realistic priorities
- [ ] Private pages (payment, reset, delete-account) have `noindex` meta tag
- [ ] OG image exists at 1200x630, referenced correctly in meta tags
- [ ] Favicons (16px, 32px), apple-touch-icon (180px), and web manifest with 192/512px icons
- [ ] WCAG 2.1 AA: contrast ratios, keyboard nav, focus indicators, semantic HTML
- [ ] `prefers-reduced-motion` disables all animations and shows content immediately
- [ ] All images have `alt`, `width`, `height` attributes
- [ ] No console errors, no layout shift on load
- [ ] Lighthouse Performance score 90+ — animations use only `transform`/`opacity`, no layout-triggering properties
- [ ] No animation library in bundle unless user explicitly requested complex animations
- [ ] Animations don't increase TBT (Total Blocking Time) or cause CLS > 0.1

### Copy Quality
- [ ] Hero headline: 8-10 words max, benefit-first
- [ ] Each feature headline sells an outcome, not a feature name
- [ ] CTAs are action-oriented and specific
- [ ] Microcopy reduces anxiety (no spam, free tier, cancel anytime)
- [ ] No marketing buzzwords unless they're genuinely accurate
- [ ] No two headlines use the same formula

---

## Key Principles

- **Never assume — detect.** Read the project first. Fill gaps with questions, don't start from scratch.
- **Ask first, then detect.** Get user requirements (pages, screenshots, preferences) before diving into code.
- **Brand coherence.** The landing page must feel like it belongs to the same product. Same fonts, same icon, same color palette. The header must show the app's actual icon next to the wordmark — never a text-only logo.
- **No generic AI aesthetics.** No gratuitous gradients on white backgrounds, no stock-photo heroes, no "revolutionize your workflow" copy. Every choice derives from the actual brand and app type.
- **Product is the hero.** Show the real product in real device frames — `mockup.png` for iOS, `android.png` for Android. Never illustrations of what the product "might look like."
- **Fewer sections, more space.** Pre-launch pages need 3-4 sections max (Hero, Features, Secondary Features, CTA). Every additional section dilutes the conversion funnel. Generous whitespace (150-200px between sections) signals premium quality. Don't fill space with "How It Works" or "Problem/Solution" unless they add information the features don't already cover.
- **Conversion-focused.** Every section exists to move the visitor toward the waitlist/download. If a section doesn't serve that goal, remove it. Pricing, FAQ, and testimonials belong on post-launch pages — not pre-launch waitlist pages.
- **Spec is the design deliverable.** Detailed enough that any developer or AI tool can implement faithfully. No ambiguity in spacing, colors, or typography.
- **TanStack Start + React 19 + TypeScript for implementation.** SSR/SSG for full crawlability. Landing pages must serve complete HTML — no empty shells. CSS transitions + IntersectionObserver for animations by default — zero bundle cost, Lighthouse-friendly. Only add GSAP or Framer Motion when the user explicitly requests complex animations.
- **Crawlable by default.** Every piece of content must be in the server-rendered HTML. If `curl` returns an empty `<div>`, the implementation is wrong. Search engines, social media scrapers, and link previews depend on real HTML content.
- **Subagent-driven development.** Parallelize independent sections for faster implementation.
- **Review before shipping.** Code review, visual review, and functional review are mandatory before marking complete.
- **Real metrics or none.** Never fabricate social proof, reviews, testimonials, user counts, or awards. Fake data destroys trust faster than no data at all. If the user has no metrics, focus on features, product screenshots, and the value proposition instead. A minimalist page with real content always beats a busy page with invented credibility.
- **Accessible by default.** WCAG 2.1 AA is the floor, not the ceiling.
- **No emoji, ever.** Emoji characters render inconsistently across platforms, look unprofessional, and can't be styled. Use inline SVGs (Heroicons, Lucide, or custom) inside fixed-size containers with a subtle background tint. SVGs scale cleanly, match the brand palette via `currentColor`, and support `aria-hidden` for accessibility.
