---
name: frontcraft
description: "The definitive frontend craft specification. 324 rules across 20 categories with measurable thresholds, covering motion, typography, accessibility, color, performance, layout, forms, and interaction design. Every rule has a name, priority level, and production code. Install with: npx skills add Dragoon0x/frontcraft"
license: MIT
compatibility: "React, Vue, Svelte, vanilla JS/TS, any CSS framework. Framework-agnostic rules."
metadata:
  version: "1.0.0"
  rules: "324"
  categories: "20"
  author: "Dragoon0x"
---

# frontcraft

> The definitive frontend craft specification. 324 rules across 20 categories, each with a measurable threshold, priority level, and production code. Not opinions — standards.

## How to Use This Skill

When implementing or reviewing frontend code, reference these rules by prefix (e.g., `motion-duration-cap`, `a11y-contrast-aa`). Each rule has:

- **Name**: Kebab-case identifier for automated detection
- **Priority**: CRITICAL (breaks UX if violated), HIGH (noticeable degradation), MEDIUM (polish issue), LOW (refinement)
- **Threshold**: A measurable number or condition
- **Implementation**: Production-ready code

Output format for findings: `rule-name | priority | file:line | description`

---

## 1. Motion & Timing

### motion-duration-cap
**Priority**: CRITICAL
**Threshold**: No transition or animation exceeds 500ms. Most should be 150-300ms.
```css
/* PASS */ transition: transform 200ms ease-out;
/* FAIL */ transition: transform 800ms ease;
```

### motion-duration-minimum
**Priority**: HIGH
**Threshold**: No transition below 100ms. Below that, the eye cannot perceive the change and the animation wastes GPU cycles for nothing.
```css
/* PASS */ transition: opacity 120ms ease-out;
/* FAIL */ transition: opacity 50ms ease;
```

### motion-enter-exit-asymmetry
**Priority**: HIGH
**Threshold**: Entry animations should be 1.5-2x longer than exits. Users wait for entrances but want exits instant.
```css
.panel-enter { animation-duration: 250ms; }
.panel-exit { animation-duration: 150ms; }
```

### motion-stagger-increment
**Priority**: MEDIUM
**Threshold**: Stagger delay between list items: 30-80ms. Below 30ms looks simultaneous. Above 80ms feels sluggish.
```css
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
```

### motion-stagger-cap
**Priority**: HIGH
**Threshold**: Total stagger sequence must not exceed 600ms regardless of item count. Cap at 8-10 items, then batch the rest.
```js
const delay = Math.min(index * 50, 400);
```

### motion-spring-stiffness
**Priority**: MEDIUM
**Threshold**: Spring stiffness 100-300 for UI elements. Below 100 feels mushy. Above 300 feels mechanical.
```js
{ type: "spring", stiffness: 200, damping: 20 }
```

### motion-spring-damping-ratio
**Priority**: HIGH
**Threshold**: Damping ratio 0.6-0.9 for UI. Below 0.6 bounces too much. Above 0.9 loses the spring character.
```js
// damping ratio = damping / (2 * sqrt(stiffness * mass))
{ stiffness: 200, damping: 22 } // ratio ~ 0.78
```

### motion-spring-for-gestures
**Priority**: CRITICAL
**Threshold**: Always use spring animations for gesture-driven interactions (drag, swipe, pinch). Easing curves create jarring velocity discontinuities on release.
```js
// PASS: spring continues from gesture velocity
animate(x, target, { type: "spring", velocity: gestureVelocity });
// FAIL: easing ignores release velocity
animate(x, target, { duration: 300, ease: "ease-out" });
```

### motion-ease-out-for-entries
**Priority**: HIGH
**Threshold**: Elements entering the viewport use ease-out (decelerating). Elements leaving use ease-in (accelerating). Never use ease-in for entries.
```css
.entering { animation-timing-function: cubic-bezier(0, 0, 0.2, 1); }
.exiting { animation-timing-function: cubic-bezier(0.4, 0, 1, 1); }
```

### motion-no-linear-transitions
**Priority**: HIGH
**Threshold**: Never use linear for UI state transitions. Linear has no acceleration curve and feels robotic. Reserve linear only for continuous animations like spinners or marquees.
```css
/* PASS */ transition: opacity 200ms ease-out;
/* PASS - continuous rotation */ animation: spin 1s linear infinite;
/* FAIL */ transition: transform 300ms linear;
```

### motion-opacity-with-transform
**Priority**: MEDIUM
**Threshold**: Fade-ins should pair opacity with a subtle transform (translateY 8-16px or scale 0.95-0.98). Opacity alone feels flat.
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### motion-gpu-compositing
**Priority**: CRITICAL
**Threshold**: Only animate transform and opacity. These run on the compositor thread. Animating width, height, top, left, margin, padding triggers layout/paint and drops frames.
```css
/* PASS */ transition: transform 200ms, opacity 200ms;
/* FAIL */ transition: width 200ms, height 200ms;
```

### motion-will-change-sparingly
**Priority**: MEDIUM
**Threshold**: Only apply will-change to elements that will animate within the next 200ms. Never set it permanently. It forces GPU layer creation and eats VRAM.
```css
.card:hover { will-change: transform; }
```

### motion-no-layout-thrash
**Priority**: CRITICAL
**Threshold**: Never read layout properties (offsetHeight, getBoundingClientRect) then write styles in the same synchronous block. Batch reads before writes.
```js
// PASS - batched
const heights = elements.map(el => el.offsetHeight);
elements.forEach((el, i) => { el.style.height = heights[i] + 10 + 'px'; });
```

### motion-cancel-on-interrupt
**Priority**: HIGH
**Threshold**: If a user triggers a new animation on an already-animating element, cancel or blend the current animation. Never queue.
```js
controller.cancel();
element.animate(newKeyframes, options);
```

### motion-scroll-driven-performance
**Priority**: HIGH
**Threshold**: Scroll-linked animations must use animation-timeline: scroll() or Intersection Observer. Never use scroll event listeners with direct style manipulation.
```css
.hero { animation: parallax linear; animation-timeline: scroll(); }
```

### motion-reduced-motion-override
**Priority**: CRITICAL
**Threshold**: All animations must respect prefers-reduced-motion: reduce. Replace motion with instant state changes or subtle opacity fades (max 150ms).
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### motion-exit-before-enter
**Priority**: HIGH
**Threshold**: When swapping content, exit old before entering new. Simultaneous exit/enter creates visual noise.

### motion-transform-origin-intent
**Priority**: MEDIUM
**Threshold**: Set transform-origin to match interaction source. Dropdown from button: origin top. Modal from center: origin center.
```css
.dropdown { transform-origin: top center; }
.modal { transform-origin: center center; }
```

### motion-skeleton-pulse-timing
**Priority**: MEDIUM
**Threshold**: Skeleton pulse: 1.5-2s duration, ease-in-out, infinite. Faster feels anxious. Slower feels broken.
```css
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.skeleton { animation: pulse 1.8s ease-in-out infinite; }
```

### motion-spinner-minimum-display
**Priority**: HIGH
**Threshold**: If a spinner is shown, display for minimum 400ms. Sub-400ms flash looks like a glitch.
```js
await Promise.all([fetchData(), sleep(400)]);
```

### motion-no-bounce-on-data
**Priority**: HIGH
**Threshold**: Never use bouncy/elastic animations on data-carrying elements (numbers, charts, progress bars). Bounce implies imprecision.

### motion-page-transition-direction
**Priority**: MEDIUM
**Threshold**: Forward navigation slides left/up. Back navigation slides right/down. Consistent spatial mapping.

### motion-hover-delay
**Priority**: MEDIUM
**Threshold**: Hover-triggered tooltips: 200-400ms enter delay, 150ms exit delay. Prevents accidental triggers.
```css
.tooltip { transition: opacity 150ms ease-out 300ms; }
.trigger:hover .tooltip { transition-delay: 0ms; }
```

### motion-scroll-snap-deceleration
**Priority**: MEDIUM
**Threshold**: scroll-snap-type: x mandatory for carousels, proximity for content. Mandatory on content pages traps users.

### motion-progress-animation
**Priority**: HIGH
**Threshold**: Progress bars must animate continuously during indeterminate states. Frozen progress bar signals crash.

---

## 2. Typography

### type-body-size-minimum
**Priority**: CRITICAL
**Threshold**: Body text minimum 16px (1rem). Below 16px fails readability on mobile.
```css
body { font-size: 16px; }
```

### type-line-height-ratio
**Priority**: CRITICAL
**Threshold**: Body line-height: 1.5-1.7. Headings: 1.1-1.3. Below 1.4 for body causes line collision on mobile.
```css
p { line-height: 1.6; } h1, h2, h3 { line-height: 1.2; }
```

### type-measure-cap
**Priority**: HIGH
**Threshold**: Maximum line length: 45-75 characters. Optimal: 65ch. Beyond 75ch, eye tracking fails.
```css
.prose { max-width: 65ch; }
```

### type-heading-scale
**Priority**: HIGH
**Threshold**: Consistent type scale. 1.2 (minor third) for compact, 1.25 (major third) for general, 1.333 (perfect fourth) for editorial.
```css
:root { --step-0: 1rem; --step-1: 1.25rem; --step-2: 1.563rem; --step-3: 1.953rem; --step-4: 2.441rem; }
```

### type-paragraph-spacing
**Priority**: MEDIUM
**Threshold**: Space between paragraphs: 0.75em-1.25em. Never margin-top on first paragraph.
```css
p + p { margin-top: 1em; }
```

### type-font-loading-swap
**Priority**: CRITICAL
**Threshold**: Always use font-display: swap or optional. Never block rendering on font load.
```css
@font-face { font-family: 'Custom'; src: url('font.woff2'); font-display: swap; }
```

### type-font-loading-preload
**Priority**: HIGH
**Threshold**: Preload critical fonts in head. Reduces FOUT by 200-500ms.
```html
<link rel="preload" href="/fonts/body.woff2" as="font" type="font/woff2" crossorigin>
```

### type-system-font-stack
**Priority**: MEDIUM
**Threshold**: Full system font stack, not just sans-serif.
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
```

### type-tabular-nums-for-data
**Priority**: CRITICAL
**Threshold**: tabular-nums for changing numbers. Proportional figures cause layout shift.
```css
.price, .timer, .stat, td { font-variant-numeric: tabular-nums; }
```

### type-no-orphans
**Priority**: MEDIUM
**Threshold**: Prevent single-word orphans on headings.
```css
h1, h2, h3 { text-wrap: balance; }
```

### type-truncation-with-title
**Priority**: HIGH
**Threshold**: Truncated text must have full text via title attribute or tooltip.
```html
<span class="truncate" title="Full text here">Full text h...</span>
```

### type-responsive-sizing
**Priority**: HIGH
**Threshold**: clamp() for fluid typography. Never viewport units alone.
```css
h1 { font-size: clamp(1.75rem, 1.2rem + 2vw, 3rem); }
```

### type-weight-hierarchy
**Priority**: HIGH
**Threshold**: Maximum 3 font weights per page. More muddles hierarchy.

### type-letter-spacing-uppercase
**Priority**: HIGH
**Threshold**: Uppercase text needs 0.02em-0.08em letter-spacing.
```css
.label { text-transform: uppercase; letter-spacing: 0.05em; }
```

### type-no-justify
**Priority**: HIGH
**Threshold**: Never text-align: justify without hyphens: auto. Creates rivers of whitespace.

### type-code-font-size
**Priority**: MEDIUM
**Threshold**: Inline code: 0.875em of surrounding text. Monospace renders optically larger.

### type-subpixel-antialiasing
**Priority**: MEDIUM
**Threshold**: -webkit-font-smoothing: antialiased for light text on dark backgrounds.
```css
.dark-bg { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
```

### type-vertical-rhythm
**Priority**: MEDIUM
**Threshold**: All spacing multiples of base line-height unit. Body 16px/1.5 = 24px unit.

### type-heading-proximity
**Priority**: HIGH
**Threshold**: Space above heading 1.5-2x space below. Headings connect to content they introduce.
```css
h2 { margin-top: 2.5em; margin-bottom: 0.75em; }
```

### type-small-text-minimum
**Priority**: CRITICAL
**Threshold**: No text below 12px anywhere. Captions, footnotes, labels, all minimum 12px.

### type-link-distinction
**Priority**: CRITICAL
**Threshold**: Links distinguishable by more than color. Use underline or weight. Color-only fails for colorblind users.
```css
a { text-decoration: underline; text-underline-offset: 2px; }
```

### type-em-for-emphasis
**Priority**: LOW
**Threshold**: Use em for stress emphasis, strong for importance. Never b or i for semantic emphasis.

### type-font-subsetting
**Priority**: HIGH
**Threshold**: Subset fonts to needed character sets. Latin-only can reduce 200KB to 20KB.
```css
@font-face { unicode-range: U+0000-00FF, U+0131, U+0152-0153; }
```

### type-variable-font-optimization
**Priority**: MEDIUM
**Threshold**: 3+ weights of same family: switch to variable font. 40-70% payload reduction.

### type-list-spacing
**Priority**: MEDIUM
**Threshold**: Multi-line list items: 0.5em-0.75em spacing. Single-line: 0.25em-0.5em.

---

## 3. Accessibility

### a11y-contrast-aa
**Priority**: CRITICAL
**Threshold**: Normal text: 4.5:1 contrast ratio (WCAG AA). Large text (18px bold / 24px): 3:1.

### a11y-contrast-aaa
**Priority**: HIGH
**Threshold**: Target 7:1 for body text (WCAG AAA). Critical for long-form reading.

### a11y-contrast-non-text
**Priority**: HIGH
**Threshold**: UI components and graphical objects: 3:1 against adjacent colors.

### a11y-focus-visible
**Priority**: CRITICAL
**Threshold**: Every interactive element: visible focus indicator. Minimum 2px solid outline, 2px offset.
```css
:focus-visible { outline: 2px solid var(--focus-color); outline-offset: 2px; }
:focus:not(:focus-visible) { outline: none; }
```

### a11y-focus-order
**Priority**: CRITICAL
**Threshold**: Focus order matches visual order. Never tabindex > 0.

### a11y-skip-link
**Priority**: CRITICAL
**Threshold**: First focusable element: skip-to-content link. Visible on focus.
```html
<a href="#main-content" class="skip-link">Skip to content</a>
```

### a11y-heading-hierarchy
**Priority**: CRITICAL
**Threshold**: Heading levels never skip. H1 > H2 > H3. One H1 per page.

### a11y-alt-text
**Priority**: CRITICAL
**Threshold**: Every img has alt. Decorative: alt="". Informative: descriptive text.
```html
<img alt="Bar chart showing Q3 revenue up 12%" src="chart.png">
<img alt="" src="divider.svg" role="presentation">
```

### a11y-aria-labels
**Priority**: CRITICAL
**Threshold**: Interactive elements without visible text: aria-label or aria-labelledby.
```html
<button aria-label="Close dialog"><svg>...</svg></button>
```

### a11y-form-labels
**Priority**: CRITICAL
**Threshold**: Every input has a visible label with matching for/id. Placeholder is not a label.
```html
<label for="email">Email</label>
<input id="email" type="email">
```

### a11y-error-identification
**Priority**: CRITICAL
**Threshold**: Form errors via text (not just color), linked via aria-describedby, announced via role="alert".
```html
<input aria-describedby="email-err" aria-invalid="true">
<span id="email-err" role="alert">Enter a valid email</span>
```

### a11y-color-not-sole-indicator
**Priority**: CRITICAL
**Threshold**: Color never the only way to convey information. Add icons, text, or patterns.

### a11y-touch-target-size
**Priority**: CRITICAL
**Threshold**: Minimum 44x44px (WCAG 2.1). Recommended 48x48px. Includes padding.

### a11y-touch-target-spacing
**Priority**: HIGH
**Threshold**: Minimum 8px between adjacent touch targets.

### a11y-keyboard-trap
**Priority**: CRITICAL
**Threshold**: Users can navigate to AND away from every component via keyboard. Focus traps only in modals.

### a11y-modal-focus-trap
**Priority**: CRITICAL
**Threshold**: Open modals trap focus. Tab wraps. Escape closes. Focus returns to trigger.

### a11y-live-regions
**Priority**: HIGH
**Threshold**: Dynamic content uses aria-live. Polite for non-urgent, assertive for critical.
```html
<div aria-live="polite">3 items added to cart</div>
```

### a11y-landmark-roles
**Priority**: HIGH
**Threshold**: Every page: header, nav, main, footer. Multiple navs need aria-label.

### a11y-language-attribute
**Priority**: HIGH
**Threshold**: html lang="en" set. Screen readers use this for pronunciation.

### a11y-page-title
**Priority**: HIGH
**Threshold**: Unique descriptive title per page. "Page Name - Site Name".

### a11y-motion-reduced
**Priority**: CRITICAL
**Threshold**: Respect prefers-reduced-motion. See motion-reduced-motion-override.

### a11y-zoom-200
**Priority**: CRITICAL
**Threshold**: Usable at 200% zoom. No clipping, no horizontal scroll, no overlap.

### a11y-text-resize
**Priority**: HIGH
**Threshold**: Text resizable to 200% without loss. Use rem/em, not fixed px.

### a11y-autocomplete-attribute
**Priority**: HIGH
**Threshold**: Personal data fields have autocomplete attribute.
```html
<input type="email" autocomplete="email">
```

### a11y-table-headers
**Priority**: HIGH
**Threshold**: Data tables use th with scope="col" or scope="row".

### a11y-svg-accessible
**Priority**: HIGH
**Threshold**: Meaningful SVGs: role="img" aria-label. Decorative: aria-hidden="true".

### a11y-no-autoplay
**Priority**: HIGH
**Threshold**: No auto-playing media. If unavoidable: visible pause within 3 seconds.

### a11y-animation-pause
**Priority**: HIGH
**Threshold**: Animations > 5 seconds must have pause mechanism. WCAG 2.2.2.

### a11y-timeout-warning
**Priority**: HIGH
**Threshold**: Session timeouts: warn 60 seconds before. Provide extend option.

### a11y-visible-state
**Priority**: HIGH
**Threshold**: All states visually distinct: default, hover, focus, active, disabled, selected, error. Minimum 2 distinguishing properties.

### a11y-disabled-semantics
**Priority**: HIGH
**Threshold**: Disabled elements: disabled attribute, opacity 0.4-0.5, removed from tab order.
```css
[disabled] { opacity: 0.45; cursor: not-allowed; pointer-events: none; }
```

### a11y-screen-reader-only
**Priority**: MEDIUM
**Threshold**: sr-only class for screen-reader-only content. Never display:none for this.
```css
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
```

### a11y-dialog-semantics
**Priority**: CRITICAL
**Threshold**: Use dialog element or role="dialog" with aria-modal="true" and aria-labelledby.

### a11y-link-vs-button
**Priority**: HIGH
**Threshold**: Links navigate. Buttons act. Never div onClick or a href="#" for actions.

### a11y-no-tabindex-positive
**Priority**: CRITICAL
**Threshold**: Never tabindex > 0. Use 0 or -1 only.

---

## 4. Color & Contrast

### color-palette-limit
**Priority**: HIGH
**Threshold**: Maximum 5-7 distinct hues.

### color-semantic-mapping
**Priority**: CRITICAL
**Threshold**: Red/destructive, green/success, yellow/warning, blue/info. Never red for positive.

### color-neutral-range
**Priority**: HIGH
**Threshold**: Minimum 9 neutral steps (50-900). Each visually distinguishable.

### color-dark-mode-not-inverted
**Priority**: CRITICAL
**Threshold**: Dark mode is NOT inverted light mode. Max white: #E0E0E0. Desaturate 10-20%.
```css
--text-dark: #E0E0E0; --bg-dark: #121212;
```

### color-dark-mode-elevation
**Priority**: HIGH
**Threshold**: Higher elevation = lighter surface in dark mode. Each step: +3-5% white overlay.
```css
--surface-0: #121212; --surface-1: #1E1E1E; --surface-2: #232323;
```

### color-opacity-over-gray
**Priority**: MEDIUM
**Threshold**: Text hierarchy: use opacity/alpha, not fixed grays. Adapts to any background.
```css
--text-primary: rgba(0,0,0,0.87); --text-secondary: rgba(0,0,0,0.60);
```

### color-state-tokens
**Priority**: HIGH
**Threshold**: Define color tokens for states. Components reference tokens, never hex directly.

### color-interactive-feedback
**Priority**: HIGH
**Threshold**: Hover: darken 5-10%. Active: darken 10-15%. Focus: distinct outline.
```css
.btn:hover { background: color-mix(in srgb, var(--primary) 90%, black); }
```

### color-consistent-saturation
**Priority**: MEDIUM
**Threshold**: Same-palette colors share similar saturation. Mixing vibrant/muted confuses hierarchy.

### color-perceptual-uniformity
**Priority**: MEDIUM
**Threshold**: Use OKLCH/OKLAB for palette generation. HSL produces uneven brightness across hues.
```css
--primary: oklch(65% 0.15 240);
```

### color-background-text-separation
**Priority**: CRITICAL
**Threshold**: Never text directly on images/gradients without overlay or shadow to guarantee contrast.

### color-brand-accent-ratio
**Priority**: MEDIUM
**Threshold**: Brand color: 5-15% of visual area. More than 15% loses signal.

### color-transparency-layering
**Priority**: MEDIUM
**Threshold**: Never stack more than 2 semi-transparent layers.

### color-forced-colors
**Priority**: HIGH
**Threshold**: Support forced-colors: active (Windows High Contrast Mode).
```css
@media (forced-colors: active) { .button { border: 2px solid ButtonText; } }
```

### color-data-viz-palette
**Priority**: HIGH
**Threshold**: Data viz: max 6-8 colors. Beyond 8, discrimination drops below 80%.

### color-data-viz-colorblind
**Priority**: CRITICAL
**Threshold**: Data palettes must pass deuteranopia, protanopia, tritanopia simulation.

### color-gradient-direction
**Priority**: LOW
**Threshold**: Gradients: top-to-bottom or left-to-right following reading direction.

### color-shadow-hue
**Priority**: MEDIUM
**Threshold**: Shadows tinted with surface hue at 5-10% opacity. Pure black shadows look flat.
```css
box-shadow: 0 4px 12px oklch(25% 0.02 250 / 0.15);
```

### color-sufficient-distinction
**Priority**: HIGH
**Threshold**: Adjacent UI elements must have minimum 15% lightness difference in OKLCH to be perceived as separate.

### color-status-redundancy
**Priority**: HIGH
**Threshold**: Status colors always paired with icon or text. Green dot + "Online". Red badge + number.

---

## 5. Touch & Interaction

### touch-target-48
**Priority**: CRITICAL
**Threshold**: All tappable elements: minimum 48x48px touch area including padding.

### touch-feedback-immediate
**Priority**: CRITICAL
**Threshold**: Touch feedback within 100ms. Active state, ripple, or press animation.
```css
button:active { transform: scale(0.97); }
```

### touch-no-hover-dependency
**Priority**: CRITICAL
**Threshold**: No critical functionality behind :hover. Touch devices have no hover.

### touch-gesture-hint
**Priority**: HIGH
**Threshold**: Custom gestures need visual hints on first encounter.

### touch-swipe-threshold
**Priority**: HIGH
**Threshold**: Swipe: 10-30px movement + velocity > 0.3px/ms.
```js
const SWIPE_THRESHOLD = 20; const VELOCITY_THRESHOLD = 0.3;
```

### touch-pull-to-refresh-distance
**Priority**: MEDIUM
**Threshold**: Pull-to-refresh trigger: 60-80px.

### touch-scroll-lock-on-gesture
**Priority**: HIGH
**Threshold**: Lock page scroll during recognized gestures. touch-action: none on gesture target.

### touch-momentum-scroll
**Priority**: HIGH
**Threshold**: Custom scroll containers: -webkit-overflow-scrolling: touch or overscroll-behavior: contain.

### touch-no-double-tap-zoom
**Priority**: MEDIUM
**Threshold**: touch-action: manipulation on interactive areas eliminates 300ms delay.

### touch-drag-cancel
**Priority**: HIGH
**Threshold**: All drags support cancel. Escape or drag back to origin reverts.

### touch-haptic-on-commit
**Priority**: MEDIUM
**Threshold**: Haptic on commit actions only. Never on hover or scroll.
```js
if ('vibrate' in navigator) navigator.vibrate(10);
```

### touch-hold-delay
**Priority**: HIGH
**Threshold**: Long-press: 400-600ms. Visual progress indicator during hold.

### touch-rubber-band-feedback
**Priority**: MEDIUM
**Threshold**: 30-50px elastic overscroll at container bounds.

### touch-pinch-zoom-images
**Priority**: HIGH
**Threshold**: Full-width images support pinch-to-zoom. No maximum-scale=1.

### touch-edge-swipe-safety
**Priority**: HIGH
**Threshold**: Reserve 20px from screen edges for system gestures.

### touch-button-debounce
**Priority**: CRITICAL
**Threshold**: Debounce taps: disable for 300ms or until action completes.
```js
if (processing) return; setProcessing(true);
```

### touch-input-font-size
**Priority**: CRITICAL
**Threshold**: Input fields minimum 16px on iOS. Below 16px triggers auto-zoom.

### touch-dismissible-overlays
**Priority**: HIGH
**Threshold**: All overlays dismissible by tapping outside.

### touch-scroll-direction-lock
**Priority**: MEDIUM
**Threshold**: Lock to axis once scroll direction established.

### touch-safe-area-respect
**Priority**: CRITICAL
**Threshold**: Interactive elements never overlap with device safe areas (notch, home indicator).

---

## 6. Layout & Spacing

### layout-spacing-scale
**Priority**: HIGH
**Threshold**: Consistent spacing scale from base unit (4px or 8px). All values multiples.
```css
:root { --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-6: 24px; --space-8: 32px; }
```

### layout-content-width
**Priority**: HIGH
**Threshold**: Max content: 1200-1440px for apps, 720-960px for reading.
```css
.container { max-width: 1200px; margin-inline: auto; }
```

### layout-padding-mobile
**Priority**: CRITICAL
**Threshold**: Minimum horizontal padding on mobile: 16px.

### layout-z-index-scale
**Priority**: HIGH
**Threshold**: Named z-index tiers: base(0), dropdown(100), sticky(200), overlay(300), modal(400), toast(500), tooltip(600).

### layout-gap-over-margin
**Priority**: HIGH
**Threshold**: Use gap in flex/grid instead of margin on children.
```css
.row { display: flex; gap: 16px; }
```

### layout-logical-properties
**Priority**: MEDIUM
**Threshold**: Use margin-inline, padding-block instead of margin-left. Required for RTL.

### layout-border-box
**Priority**: CRITICAL
**Threshold**: box-sizing: border-box globally.
```css
*, *::before, *::after { box-sizing: border-box; }
```

### layout-sticky-offset
**Priority**: MEDIUM
**Threshold**: Sticky headers: top: 0 + z-index above content. Account for stacking.

### layout-container-queries
**Priority**: MEDIUM
**Threshold**: Component-level responsiveness: container queries over media queries.
```css
.card-container { container-type: inline-size; }
```

### layout-grid-auto-fill
**Priority**: HIGH
**Threshold**: Auto-flowing grids: auto-fill with minmax().
```css
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px; }
```

### layout-aspect-ratio
**Priority**: HIGH
**Threshold**: Media containers: aspect-ratio to prevent layout shift.
```css
.video { aspect-ratio: 16 / 9; } .thumb { aspect-ratio: 1; }
```

### layout-scroll-margin
**Priority**: MEDIUM
**Threshold**: Anchor targets: scroll-margin-top equals fixed header height.
```css
[id] { scroll-margin-top: 80px; }
```

### layout-overflow-clip
**Priority**: MEDIUM
**Threshold**: Use overflow: clip over overflow: hidden when no scroll container needed.

### layout-min-height-dvh
**Priority**: HIGH
**Threshold**: Full-height: min-height: 100dvh not 100vh. Accounts for mobile browser chrome.

### layout-safe-area-inset
**Priority**: CRITICAL
**Threshold**: Devices with notches: env(safe-area-inset-*) padding.
```css
body { padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); }
```

### layout-no-horizontal-scroll
**Priority**: CRITICAL
**Threshold**: No unintentional horizontal scroll. Test at 320px width.

### layout-whitespace-proportion
**Priority**: HIGH
**Threshold**: Larger components need proportionally larger surrounding whitespace.

### layout-grid-gutter-responsive
**Priority**: MEDIUM
**Threshold**: Grid gutters scale: 16px mobile, 24px tablet, 32px desktop.

### layout-centering-method
**Priority**: MEDIUM
**Threshold**: Use place-items: center for single-element centering. Flexbox for multi-element.

---

## 7. Responsive Design

### responsive-breakpoints
**Priority**: HIGH
**Threshold**: Standard: 320, 375, 768, 1024, 1280, 1536. Mobile-first.

### responsive-mobile-first
**Priority**: HIGH
**Threshold**: Base styles for mobile, add with min-width. Never max-width as primary.

### responsive-fluid-over-fixed
**Priority**: HIGH
**Threshold**: Fluid values (%, vw, clamp()) over fixed where possible.

### responsive-image-srcset
**Priority**: HIGH
**Threshold**: Every image: srcset with 2-3 variants and sizes attribute.
```html
<img srcset="photo-400.jpg 400w, photo-800.jpg 800w" sizes="(max-width: 768px) 100vw, 50vw">
```

### responsive-picture-art-direction
**Priority**: MEDIUM
**Threshold**: picture with source for different crops at breakpoints.

### responsive-viewport-meta
**Priority**: CRITICAL
**Threshold**: viewport meta tag. Never maximum-scale=1 or user-scalable=no.
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### responsive-font-scaling
**Priority**: HIGH
**Threshold**: clamp() for headings. No fixed sizes.

### responsive-hide-with-purpose
**Priority**: HIGH
**Threshold**: Hidden elements still accessible or alternative path exists.

### responsive-table-overflow
**Priority**: HIGH
**Threshold**: Tables on mobile: overflow-x: auto or convert to stacked cards below 768px.

### responsive-modal-fullscreen-mobile
**Priority**: HIGH
**Threshold**: Modals below 480px go full-screen or bottom sheet.

### responsive-nav-hamburger-threshold
**Priority**: MEDIUM
**Threshold**: Collapse nav when items dont fit at touch target size. Never collapse 3-item nav.

### responsive-input-sizing
**Priority**: HIGH
**Threshold**: Mobile inputs: full-width. Side-by-side only above 768px.

### responsive-sticky-bottom-mobile
**Priority**: MEDIUM
**Threshold**: Primary mobile CTAs in sticky bottom bar within thumb reach.

### responsive-landscape-consideration
**Priority**: MEDIUM
**Threshold**: Test landscape. Fixed headers + footers can consume >50% in landscape.

### responsive-test-320
**Priority**: CRITICAL
**Threshold**: Test at 320px minimum. iPhone SE is 320px.

### responsive-container-query-components
**Priority**: MEDIUM
**Threshold**: Reusable components: container queries over media queries.

---

## 8. Performance

### perf-lcp-under-2500
**Priority**: CRITICAL
**Threshold**: LCP under 2.5s. Core Web Vital.

### perf-inp-under-200
**Priority**: CRITICAL
**Threshold**: INP under 200ms. Under 100ms is good.

### perf-cls-under-01
**Priority**: CRITICAL
**Threshold**: CLS under 0.1. Set dimensions on images/videos.

### perf-ttfb-under-800
**Priority**: HIGH
**Threshold**: TTFB under 800ms. Use CDN, edge caching, SSG.

### perf-js-bundle-budget
**Priority**: CRITICAL
**Threshold**: Initial JS: <100KB gzipped. Each 100KB costs 350ms parse on mid-tier phone.

### perf-critical-css-inline
**Priority**: HIGH
**Threshold**: Inline critical CSS in head. Max 14KB (TCP congestion window).

### perf-lazy-load-images
**Priority**: HIGH
**Threshold**: Below-fold images: loading="lazy". LCP image: eager + fetchpriority="high".

### perf-preconnect-origins
**Priority**: HIGH
**Threshold**: Preconnect to critical third-party origins. Saves 100-300ms.
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
```

### perf-image-format
**Priority**: HIGH
**Threshold**: WebP or AVIF for raster images. WebP: 25-35% smaller. AVIF: 50% smaller.

### perf-font-subset
**Priority**: HIGH
**Threshold**: Subset fonts. Latin-only: 200KB to 20KB.

### perf-third-party-async
**Priority**: HIGH
**Threshold**: All third-party scripts: async or defer.

### perf-no-render-blocking-css
**Priority**: HIGH
**Threshold**: Non-critical CSS: media attribute or async load.

### perf-code-splitting
**Priority**: HIGH
**Threshold**: Route-based splitting minimum. Dynamic import() for heavy components.

### perf-prefetch-likely-routes
**Priority**: MEDIUM
**Threshold**: Prefetch likely next pages on hover/visibility.

### perf-debounce-scroll-resize
**Priority**: HIGH
**Threshold**: Throttle scroll/resize to 100ms or use rAF.

### perf-virtual-list
**Priority**: HIGH
**Threshold**: Lists >50 items: virtualize.

### perf-image-dimensions
**Priority**: CRITICAL
**Threshold**: All img/video: explicit width and height or aspect-ratio.

### perf-service-worker-cache
**Priority**: MEDIUM
**Threshold**: Cache static assets with service worker.

### perf-dns-prefetch
**Priority**: LOW
**Threshold**: DNS-prefetch for third-party domains.

### perf-long-task-break
**Priority**: HIGH
**Threshold**: No JS task >50ms on main thread. Break with rIC or setTimeout(0).

### perf-react-memo-threshold
**Priority**: MEDIUM
**Threshold**: Memoize components rendering >16ms with stable props. Profile first.

### perf-reflow-batch
**Priority**: HIGH
**Threshold**: Batch DOM reads before writes.

### perf-css-containment
**Priority**: MEDIUM
**Threshold**: contain: layout on independent components.

### perf-resource-hints-order
**Priority**: MEDIUM
**Threshold**: Resource hint priority: preload > preconnect > prefetch > dns-prefetch.

---

## 9. Loading States

### loading-skeleton-shape
**Priority**: HIGH
**Threshold**: Skeletons match shape/layout of replaced content. No generic rectangles.

### loading-skeleton-animation
**Priority**: MEDIUM
**Threshold**: Shimmer gradient (left-to-right wave) implies progress.
```css
.skeleton { background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%); background-size: 200% 100%; animation: shimmer 1.5s ease-in-out infinite; }
```

### loading-instant-feedback
**Priority**: CRITICAL
**Threshold**: Visual feedback within 100ms of user action.

### loading-spinner-delay
**Priority**: HIGH
**Threshold**: Show spinner after 300-500ms delay. Most operations complete before it appears.

### loading-progress-determinate
**Priority**: HIGH
**Threshold**: Known progress: use determinate bar. Indeterminate spinner for unknown.

### loading-optimistic-update
**Priority**: HIGH
**Threshold**: Binary actions (toggle, like): update UI immediately, reconcile async.
```js
setLiked(!liked); // optimistic
try { await api.toggleLike(id); } catch { setLiked(liked); }
```

### loading-content-priority
**Priority**: HIGH
**Threshold**: Load order: text > above-fold images > below-fold > non-critical.

### loading-error-recovery
**Priority**: HIGH
**Threshold**: Every loading state has error state with retry. Timeout after 10-15s.

### loading-empty-state-helpful
**Priority**: HIGH
**Threshold**: Empty states explain WHY and provide primary action. Not just "No results."

### loading-pagination-infinite
**Priority**: MEDIUM
**Threshold**: Infinite scroll: loading indicator, scroll-to-top after 3 pages, virtualize after 100 items.

### loading-skeleton-reduced-motion
**Priority**: MEDIUM
**Threshold**: prefers-reduced-motion: static gray blocks instead of animated skeletons.

### loading-placeholder-image
**Priority**: MEDIUM
**Threshold**: Images show BlurHash, LQIP, or dominant color during load.

### loading-stream-long-content
**Priority**: MEDIUM
**Threshold**: Stream long content as it arrives. Users read while loading.

---

## 10. Error States

### error-message-human
**Priority**: CRITICAL
**Threshold**: Human language, not technical codes.

### error-message-specific
**Priority**: HIGH
**Threshold**: Explain what went wrong AND what to do.

### error-message-no-blame
**Priority**: HIGH
**Threshold**: Never blame the user. "We could not find" not "You entered invalid."

### error-inline-not-modal
**Priority**: HIGH
**Threshold**: Validation errors inline next to field, not in modal/alert.

### error-real-time-validation
**Priority**: MEDIUM
**Threshold**: Validate on blur for text, immediately for toggles/selects.

### error-persistent-until-fixed
**Priority**: HIGH
**Threshold**: Errors visible until corrected. Never auto-dismiss.

### error-404-helpful
**Priority**: HIGH
**Threshold**: 404 includes search, home link, suggested pages.

### error-network-offline
**Priority**: HIGH
**Threshold**: Detect offline, show persistent banner, cache last content.
```js
window.addEventListener('offline', () => showBanner('You are offline'));
```

### error-retry-exponential
**Priority**: MEDIUM
**Threshold**: Auto-retry: 1s, 2s, 4s, 8s, max 30s. Stop after 5 attempts.

### error-boundary-react
**Priority**: CRITICAL
**Threshold**: Error boundaries at route level and around risky components.

### error-form-preserve-input
**Priority**: CRITICAL
**Threshold**: Failed submission: preserve all input. Never clear on failure.

### error-rate-limit-messaging
**Priority**: MEDIUM
**Threshold**: Rate limit errors: tell when to retry with countdown.

### error-destructive-confirmation
**Priority**: CRITICAL
**Threshold**: Destructive actions: confirm with specific item name.

### error-undo-over-confirm
**Priority**: HIGH
**Threshold**: Prefer undo over confirmation dialogs. Undo is a real safety net.

---

## 11. Dark Mode

### dark-surface-elevation
**Priority**: HIGH
**Threshold**: Lighter surfaces = higher elevation. 4-5 steps.

### dark-no-pure-black
**Priority**: HIGH
**Threshold**: No #000000. Use #121212-#1A1A1A. Pure black causes OLED smearing.

### dark-no-pure-white-text
**Priority**: HIGH
**Threshold**: No #FFFFFF text. Use #E0E0E0-#EBEBEB. Pure white causes halation.

### dark-desaturate-colors
**Priority**: HIGH
**Threshold**: Reduce accent saturation 10-20% in dark mode.

### dark-increase-lightness
**Priority**: HIGH
**Threshold**: Accent L value +15-25% in OKLCH for dark mode.

### dark-shadow-alternative
**Priority**: MEDIUM
**Threshold**: Replace shadows with subtle borders (1px, 5-10% white opacity).
```css
/* Dark */ border: 1px solid rgba(255,255,255,0.08);
```

### dark-image-brightness
**Priority**: MEDIUM
**Threshold**: Reduce image brightness 10-15% in dark mode. Not user content.
```css
@media (prefers-color-scheme: dark) { img:not(.user-content) { filter: brightness(0.88); } }
```

### dark-system-preference
**Priority**: HIGH
**Threshold**: Default to prefers-color-scheme. Manual toggle persists.

### dark-transition-smooth
**Priority**: MEDIUM
**Threshold**: Theme switch: 200-300ms transition on background/color.

### dark-code-block-theme
**Priority**: MEDIUM
**Threshold**: Dark syntax theme in dark mode. Light in light mode.

### dark-favicon-variant
**Priority**: LOW
**Threshold**: Dark-mode favicon if logo disappears on dark chrome.

### dark-meta-theme-color
**Priority**: MEDIUM
**Threshold**: meta theme-color matches dark mode background on mobile.
```html
<meta name="theme-color" content="#121212" media="(prefers-color-scheme: dark)">
```

---

## 12. Keyboard Navigation

### keyboard-all-interactive-reachable
**Priority**: CRITICAL
**Threshold**: Every interactive element reachable by Tab.

### keyboard-escape-closes
**Priority**: CRITICAL
**Threshold**: Escape closes topmost overlay. Focus returns to trigger.

### keyboard-enter-activates
**Priority**: HIGH
**Threshold**: Enter activates buttons/links. Space toggles checkboxes/buttons.

### keyboard-arrow-keys
**Priority**: HIGH
**Threshold**: Arrows navigate within composite widgets. Tab exits widget.

### keyboard-visible-focus
**Priority**: CRITICAL
**Threshold**: 2px outline, 3:1 contrast against adjacent backgrounds.

### keyboard-roving-tabindex
**Priority**: HIGH
**Threshold**: Composite widgets: one child in tab order. Arrows move between children.

### keyboard-shortcut-discoverable
**Priority**: MEDIUM
**Threshold**: Shortcuts shown in tooltips or ? dialog. Undocumented shortcuts do not exist.

### keyboard-no-override-browser
**Priority**: HIGH
**Threshold**: Custom shortcuts must not override browser defaults (Ctrl+F, Ctrl+S).

### keyboard-search-focus
**Priority**: MEDIUM
**Threshold**: Search focusable with / or Cmd+K.

### keyboard-type-ahead
**Priority**: MEDIUM
**Threshold**: Lists/selects support type-ahead character jump.

---

## 13. Sound Design

### sound-action-feedback
**Priority**: MEDIUM
**Threshold**: Success/error/warning sounds: distinct, under 200ms. Reserve for important state changes.

### sound-volume-control
**Priority**: CRITICAL
**Threshold**: Mute toggle that persists. Default 30-50% system volume.

### sound-no-autoplay-audio
**Priority**: CRITICAL
**Threshold**: Never autoplay audio. User must initiate.

### sound-system-sounds
**Priority**: LOW
**Threshold**: Native platforms: prefer system sounds for common actions.

### sound-haptic-pairing
**Priority**: MEDIUM
**Threshold**: Mobile: pair sounds with haptic for important actions.

### sound-spatial-audio
**Priority**: LOW
**Threshold**: Spatial interfaces: subtle spatial audio reinforces position.

### sound-frequency-meaning
**Priority**: MEDIUM
**Threshold**: Higher pitch = success. Lower = error. Ascending = progress. Descending = regression.

### sound-click-debounce
**Priority**: HIGH
**Threshold**: Debounce sound triggers within 50ms.

---

## 14. Micro-interactions

### micro-toggle-state
**Priority**: HIGH
**Threshold**: Toggles show state via position, color, and optionally icon.

### micro-button-press
**Priority**: MEDIUM
**Threshold**: Buttons: scale(0.97) or translateY(1px) on :active. 100ms.

### micro-input-focus
**Priority**: HIGH
**Threshold**: Focus: border color + ring/glow. 150ms transition.
```css
input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-alpha-20); }
```

### micro-count-animate
**Priority**: MEDIUM
**Threshold**: Changing numbers: animate roll or fade. 200-400ms.

### micro-checkbox-animation
**Priority**: MEDIUM
**Threshold**: Checkmark draw animation (stroke-dasharray). 200ms.

### micro-switch-inertia
**Priority**: MEDIUM
**Threshold**: Toggle switch: spring curve, slight overshoot. 300ms total.

### micro-copy-confirmation
**Priority**: HIGH
**Threshold**: Copy: icon changes to checkmark for 2s, tooltip "Copied!"

### micro-like-burst
**Priority**: LOW
**Threshold**: Like/favorite: particle burst or scale pop. 400ms.

### micro-link-hover
**Priority**: MEDIUM
**Threshold**: Links on hover: underline slide-in or color shift. 150ms.

### micro-card-hover-lift
**Priority**: MEDIUM
**Threshold**: Card hover: translateY(-2px) + shadow increase. 200ms.
```css
.card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
```

### micro-drag-shadow
**Priority**: MEDIUM
**Threshold**: Dragged elements: larger shadow, scale(1.02-1.05), reduced opacity at origin.

### micro-notification-dot
**Priority**: HIGH
**Threshold**: Notification badge: scale-in with bounce (300ms). New: pulse once (400ms).

### micro-tab-underline
**Priority**: MEDIUM
**Threshold**: Active tab indicator slides (translateX). 250ms ease-out.

### micro-accordion-icon
**Priority**: MEDIUM
**Threshold**: Accordion icon rotates 180deg or morphs. 200ms. Synced with content.

### micro-scroll-indicator
**Priority**: LOW
**Threshold**: Scroll progress bar at top. Width scales with scroll percentage.

---

## 15. Forms & Input

### form-label-always-visible
**Priority**: CRITICAL
**Threshold**: Labels visible with content. Floating labels OK. Placeholder-only: never.

### form-required-indicator
**Priority**: HIGH
**Threshold**: Required: asterisk + aria-required. If most required, mark optional instead.

### form-input-types
**Priority**: HIGH
**Threshold**: Correct HTML types: email, tel, url, number, search.

### form-autofill-style
**Priority**: MEDIUM
**Threshold**: Style autofilled fields to match design.
```css
input:-webkit-autofill { -webkit-box-shadow: 0 0 0 1000px var(--bg) inset; }
```

### form-password-visibility
**Priority**: HIGH
**Threshold**: Show/hide toggle on password fields.

### form-submit-loading
**Priority**: CRITICAL
**Threshold**: Submit button shows loading, prevents double-submission.

### form-success-feedback
**Priority**: HIGH
**Threshold**: Clear success: checkmark, message, what happens next.

### form-field-width-meaning
**Priority**: MEDIUM
**Threshold**: Width hints at input length. Zip: narrow. Name: wide.

### form-date-format-hint
**Priority**: HIGH
**Threshold**: Date format in placeholder/helper. Better: date picker.

### form-multiline-auto-resize
**Priority**: MEDIUM
**Threshold**: Textarea auto-grows with content.
```js
textarea.style.height = 'auto'; textarea.style.height = textarea.scrollHeight + 'px';
```

### form-inline-help
**Priority**: MEDIUM
**Threshold**: Complex fields: helper text always visible, not just on error.

### form-step-indicator
**Priority**: HIGH
**Threshold**: Multi-step: progress indicator with current/total.

### form-field-grouping
**Priority**: MEDIUM
**Threshold**: Related fields: fieldset + legend.

### form-enter-to-submit
**Priority**: HIGH
**Threshold**: Single-field forms submit on Enter.

### form-clear-affordance
**Priority**: MEDIUM
**Threshold**: Search/filter: clear (x) button when populated.

---

## 16. Navigation

### nav-current-indicator
**Priority**: CRITICAL
**Threshold**: Active nav item visually distinct + aria-current="page".

### nav-breadcrumb-structure
**Priority**: HIGH
**Threshold**: 3+ levels deep: breadcrumbs with nav aria-label="Breadcrumb".

### nav-back-predictable
**Priority**: HIGH
**Threshold**: Browser back works predictably. SPA pushes history states.

### nav-depth-limit
**Priority**: HIGH
**Threshold**: Max 3 levels deep. Flatten architecture beyond.

### nav-mobile-bottom-bar
**Priority**: HIGH
**Threshold**: 3-5 primary destinations: bottom bar with icons AND labels.

### nav-search-global
**Priority**: HIGH
**Threshold**: 10+ pages or 100+ content: global search with Cmd+K.

### nav-sidebar-collapse
**Priority**: MEDIUM
**Threshold**: Collapsible to icons-only. 48-64px collapsed width.

### nav-link-underline
**Priority**: HIGH
**Threshold**: In-content links: underlined. Nav links: distinct styling without underline.

### nav-external-link-indicator
**Priority**: MEDIUM
**Threshold**: New-tab links: external icon + target="_blank" rel="noopener noreferrer".

### nav-scroll-position-restore
**Priority**: HIGH
**Threshold**: Restore scroll position on back navigation.

### nav-pagination-context
**Priority**: MEDIUM
**Threshold**: Pagination: current page, total, first/last, ellipsis for gaps.

### nav-404-recovery
**Priority**: HIGH
**Threshold**: Dead links are trust killers. See error-404-helpful.

---

## 17. Icons & Imagery

### icon-consistency
**Priority**: HIGH
**Threshold**: Same stroke width, corner radius, visual weight, style across all icons.

### icon-size-minimum
**Priority**: HIGH
**Threshold**: 16px inline, 20px standalone, 24px primary actions.

### icon-label-pairing
**Priority**: HIGH
**Threshold**: Icon-only: aria-label. Icon+text: icon gets aria-hidden="true".

### icon-filled-active
**Priority**: MEDIUM
**Threshold**: Outlined = inactive. Filled = active.

### icon-no-ambiguity
**Priority**: HIGH
**Threshold**: Ambiguous icon? Add text label. When in doubt, add text.

### icon-svg-over-font
**Priority**: HIGH
**Threshold**: Inline SVG, not icon fonts. Better scaling, accessibility, multicolor.

### icon-optical-alignment
**Priority**: MEDIUM
**Threshold**: Play/triangle: 1-2px right offset for optical center.

### image-lazy-loading
**Priority**: HIGH
**Threshold**: Below-fold images: loading="lazy".

### image-alt-descriptive
**Priority**: CRITICAL
**Threshold**: Alt describes what image SHOWS. Not filename.

### image-fallback-on-error
**Priority**: HIGH
**Threshold**: Error fallback: placeholder or user initial. Never broken image icon.
```html
<img onerror="this.src='/placeholder.svg'" alt="Profile">
```

### image-decorative-performance
**Priority**: MEDIUM
**Threshold**: Decorative images: CSS backgrounds or loading="lazy" + alt="".

---

## 18. Scroll Behavior

### scroll-smooth-native
**Priority**: MEDIUM
**Threshold**: scroll-behavior: smooth for anchor navigation.

### scroll-to-top
**Priority**: HIGH
**Threshold**: Pages >3 viewports: scroll-to-top button. Appears after 1 viewport scroll.

### scroll-indicator-long-content
**Priority**: LOW
**Threshold**: Content >5 viewports: scroll progress indicator.

### scroll-snap-alignment
**Priority**: MEDIUM
**Threshold**: Carousels: CSS scroll-snap for native pagination.
```css
.gallery { scroll-snap-type: x mandatory; } .gallery-item { scroll-snap-align: center; }
```

### scroll-overscroll-contain
**Priority**: MEDIUM
**Threshold**: Modal/drawer: overscroll-behavior: contain. Prevents background scroll chaining.

### scroll-infinite-sentinel
**Priority**: MEDIUM
**Threshold**: Infinite scroll: Intersection Observer on sentinel 200-300px from bottom.

### scroll-parallax-performance
**Priority**: HIGH
**Threshold**: Parallax: CSS transform in 3D context or animation-timeline: scroll(). Never JS listeners.

### scroll-anchor-offset
**Priority**: HIGH
**Threshold**: Account for fixed headers on anchor jumps. See layout-scroll-margin.

### scroll-restoration-spa
**Priority**: HIGH
**Threshold**: SPA scroll restoration per route.

---

## 19. Content & Copy

### copy-action-verbs
**Priority**: HIGH
**Threshold**: Button labels: action verbs. Save, Send, Create. Never Submit or OK.

### copy-error-actionable
**Priority**: HIGH
**Threshold**: Errors: what happened + what to do.

### copy-confirmation-specific
**Priority**: HIGH
**Threshold**: Name specific item: "Delete 'Project Alpha'?" Include consequences.

### copy-placeholder-example
**Priority**: MEDIUM
**Threshold**: Placeholder shows example, not label: "jane@example.com".

### copy-microcopy-reassurance
**Priority**: MEDIUM
**Threshold**: Sensitive fields: add reassurance. "We never share your email."

### copy-loading-context
**Priority**: MEDIUM
**Threshold**: Loading messages explain what is happening: "Uploading 3 photos..."

### copy-empty-state-encouraging
**Priority**: HIGH
**Threshold**: Empty states guide, not dead-end.

### copy-cta-single-focus
**Priority**: HIGH
**Threshold**: One primary CTA per section. Multiple competing CTAs cause paralysis.

### copy-tooltip-concise
**Priority**: MEDIUM
**Threshold**: Tooltips: 1-2 sentences max.

### copy-notification-format
**Priority**: MEDIUM
**Threshold**: Format: "[Who] [did what] [when]." Lead with subject.

---

## 20. Performance Perception

### perception-optimistic-render
**Priority**: HIGH
**Threshold**: Show UI structure immediately. Skeleton > real content feels faster than spinner > complete page.

### perception-above-fold-priority
**Priority**: CRITICAL
**Threshold**: Above the fold renders in under 1 second.

### perception-progress-over-spinner
**Priority**: HIGH
**Threshold**: Determinate progress > indeterminate > spinner > nothing. Each step up: -20% perceived wait.

### perception-instant-navigation
**Priority**: HIGH
**Threshold**: Page navigation feels instant (<200ms). Preload on hover.

### perception-content-shift-zero
**Priority**: CRITICAL
**Threshold**: No visible content shift after initial render. Reserve space for everything.

### perception-time-display
**Priority**: MEDIUM
**Threshold**: Relative times for <7 days. Absolute times after.

### perception-operation-feedback
**Priority**: HIGH
**Threshold**: Every action gets feedback within 100ms. Silence = broken.

### perception-preload-prediction
**Priority**: MEDIUM
**Threshold**: Predict next action and preload. Mouse near link: prefetch.

### perception-skeleton-timing
**Priority**: MEDIUM
**Threshold**: Skeletons for content >300ms load time only.

### perception-chunked-rendering
**Priority**: HIGH
**Threshold**: Large datasets: first 20 items immediately, batch-render rest.

---

## Rule Index

Total rules: 324

| Category | Count |
|---|---|
| Motion & Timing | 26 |
| Typography | 25 |
| Accessibility | 35 |
| Color & Contrast | 20 |
| Touch & Interaction | 20 |
| Layout & Spacing | 19 |
| Responsive Design | 16 |
| Performance | 24 |
| Loading States | 13 |
| Error States | 14 |
| Dark Mode | 12 |
| Keyboard Navigation | 10 |
| Sound Design | 8 |
| Micro-interactions | 15 |
| Forms & Input | 15 |
| Navigation | 12 |
| Icons & Imagery | 11 |
| Scroll Behavior | 9 |
| Content & Copy | 10 |
| Performance Perception | 10 |

## Priority Distribution

| Priority | Count | Action |
|---|---|---|
| CRITICAL | 65 | Must fix. Breaks UX, accessibility, or performance. |
| HIGH | 152 | Should fix. Noticeable degradation. |
| MEDIUM | 98 | Polish. Difference between good and great. |
| LOW | 9 | Refinement. The last 5% of craft. |

## License

MIT License - Dragoon0x (https://github.com/Dragoon0x)
