---
name: gsap-advanced
description: >
  Advanced GSAP patterns: Timeline sequencing, ScrollTrigger scroll-driven animations, plugins (Flip, Draggable, MotionPath, SplitText), performance optimization, and utility methods.
  Trigger: When creating timelines, scroll animations, using GSAP plugins, or optimizing GSAP performance.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
  merged_from: ["gsap-timeline", "gsap-scrolltrigger", "gsap-plugins", "gsap-performance", "gsap-utils"]
---

# GSAP Advanced

Merged skill combining timeline sequencing, scroll-driven animations, plugins, performance, and utilities.



## TIMELINE

## When to Use

- Sequencing multiple animations
- Choreographed animation sequences
- Controlling playback (play, pause, reverse, restart)
- Adding labels for navigation
- Nested timelines

## Critical Patterns

### Create Timeline

```typescript
import { gsap } from "gsap";

const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2" } });

tl.to(".a", { x: 100 })
  .to(".b", { y: 50 }, "<")      // Start at same time as previous
  .to(".c", { opacity: 0 }, "+=0.2")  // 0.2s after previous ends
  .to(".d", { scale: 1.5 }, "-=0.1"); // Overlap 0.1s with previous
```

### Position Parameters

| Parameter | Meaning |
|-----------|---------|
| `"<"` | Start at same time as previous tween starts |
| `"<0.2"` | Start 0.2s before previous tween starts |
| `">"` | Start when previous tween ends |
| `">0.2"` | Start 0.2s after previous tween ends |
| `"+=0.2"` | Start 0.2s after previous tween ends |
| `"-=0.2"` | Start 0.2s before previous tween ends |
| `"label"` | Start at timeline label |
| `0.5` | Absolute time in seconds |

### Labeling

```typescript
const tl = gsap.timeline();

tl.to(".a", { x: 100 })
  .addLabel("step1")              // Label at current time
  .to(".b", { y: 50 })
  .to(".c", { opacity: 0 });

// Jump to label
tl.tweenTo("step1");

// Or use label for positioning
tl.to(".d", { x: 200 }, "step1");
```

## Playback Control

```typescript
const tl = gsap.timeline();

// Playback
tl.play();
tl.pause();
tl.restart();
tl.reverse();
tl.seek(1.5);           // Jump to 1.5 seconds
tl.progress(0.5);       // Set progress to 50%
tl.timeScale(2);        // Speed up 2x
tl.timeScale(0.5);      // Slow down 0.5x
tl.kill();             // Stop and clear

// Event callbacks
tl.eventCallback("onComplete", () => console.log("Done!"));
tl.eventCallback("onUpdate", () => updateProgress());
```

## Nested Timelines

```typescript
const mainTl = gsap.timeline();

// Create separate timeline and add it
const subTl = gsap.timeline();
subTl.to(".box1", { rotation: 360 });
subTl.to(".box2", { x: 100 });

mainTl.add(subTl);           // Add at end
mainTl.add(subTl, "<");     // Add at start
mainTl.add(subTl, 2);       // Add at 2 seconds
```

## Defaults

```typescript
// Timeline defaults apply to ALL nested tweens
const tl = gsap.timeline({
  defaults: {
    duration: 0.6,
    ease: "power2.out",
  },
  repeat: -1,        // Infinite repeat
  yoyo: true,        // Reverse on repeat
  repeatDelay: 0.5   // Delay between repeats
});
```

## Modifying Animations

```typescript
const tl = gsap.timeline();

// Get all tweens in timeline
const tweens = tl.getChildren();

// Change duration of specific tween
tl.getChildren()[0].duration(0.3);

// Add tween to existing timeline
tl.to(".new", { x: 100 }, 1);

// Remove tweens
tl.getChildren().forEach(t => t.kill());
tl.clear();
```

## Commands

```bash
npm install gsap
```

## Resources

See `references/` for detailed guides and code examples in `assets/`.

## External Resources

- [Official Documentation]

## SCROLLTRIGGER

## When to Use

- Scroll-driven animations
- Parallax effects
- Pinning elements during scroll
- Horizontal scroll sections
- Scroll-based reveal animations

## Critical Patterns

### Setup

```typescript
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);
```

### Basic Scroll Animation

```typescript
// Simple scroll-triggered animation
gsap.to(".element", {
  x: 200,
  scrollTrigger: {
    trigger: ".element",
    start: "top 80%",    // When element top hits 80% of viewport
    end: "top 20%",      // When element top hits 20% of viewport
    scrub: 1,            // Smooth scrubbing (1s lag)
    // or toggleActions for simple triggers
    toggleActions: "play reverse play reverse"
  }
});
```

### Start/End Positions

Common start/end values:

| Value | Meaning |
|-------|---------|
| `"top top"` | Trigger top = viewport top |
| `"center center"` | Trigger center = viewport center |
| `"bottom bottom"` | Trigger bottom = viewport bottom |
| `"top 80%"` | Trigger top at 80% of viewport |
| `"+=100"` | 100px after trigger position |

### Pinning

```typescript
// Pin element during scroll
gsap.to(".pinned-section", {
  scrollTrigger: {
    trigger: ".pinned-section",
    start: "top top",
    end: "+=500",         // Pin for 500px of scroll
    pin: true,            // Enable pinning
    pinSpacing: false    // No spacer element
  }
});

// Pin with pinSpacing (default)
gsap.to(".pin-wrap", {
  scrollTrigger: {
    trigger: ".pin-wrap",
    start: "top top",
    end: "+=1000",
    pin: ".inner-element" // Pin specific element
  }
});
```

### Scrub

```typescript
// Smooth scrub with delay
gsap.to(".parallax", {
  y: -100,
  scrollTrigger: {
    trigger: ".parallax",
    start: "top bottom",
    end: "bottom top",
    scrub: 0.5           // 0.5s lag for smoothness
  }
});

// True scrub (links to scroll position exactly)
gsap.to(".exact", {
  rotation: 360,
  scrollTrigger: {
    trigger: ".exact",
    scrub: true          // Direct link to scroll
  }
});
```

### Toggle Actions

| Trigger | Action |
|---------|--------|
| `"play"` | Play animation |
| `"pause"` | Pause animation |
| `"resume"` | Resume animation |
| `"reverse"` | Play in reverse |
| `"restart"` | Restart from beginning |
| `"complete"` | Jump to end |
| `"none"` | No action |

```typescript
// Common patterns
toggleActions: "play none none none"    // Play on enter
toggleActions: "play reverse play reverse"  // Play/reverse on enter/leave
toggleActions: "restart pause restart"   // Restart on enter, pause on leave
```

### Callbacks

```typescript
ScrollTrigger.create({
  trigger: ".element",
  start: "top center",
  onEnter: () => console.log("Entered"),
  onLeave: () => console.log("Left"),
  onEnterBack: () => console.log("Entered from below"),
  onLeaveBack: () => console.log("Left going up"),
  onUpdate: (self) => console.log(self.progress),
  onRefresh: () => console.log("Refreshed after layout change")
});
```

## Horizontal Scroll

```typescript
// Horizontal scroll section
const sections = gsap.utils.toArray(".panel");

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    end: "+=3000"        // Scroll distance
  }
});
```

### Refresh Required

Call `ScrollTrigger.refresh()` AFTER DOM changes:

```typescript
// After adding/removing elements
document.body.appendChild(newElement);
ScrollTrigger.refresh();

// After resizing or dynamic content
window.addEventListener("resize", () => ScrollTrigger.refresh());
```

## Cleanup

```typescript
// Clean up ScrollTriggers
function cleanup() {
  ScrollTrigger.getAll().forEach(t => t.kill());
  ScrollTrigger.refresh();
}

// In React (use useGSAP hook - see gsap-react skill)
```

## Commands

```bash
npm install gsap
```

## SCROLLTRIGGER STORYTELLING (from MengTo)

## When to Use

- Cinematic sticky product storytelling with progressive UI reveals
- Scroll-synced animation where copy, UI panels, and media move together
- Immersive section transitions for premium marketing pages

## Core Architecture

### Sticky Product Storytelling
```typescript
gsap.utils.toArray("[data-story-scene]").forEach((scene) => {
  const panels = scene.querySelectorAll("[data-story-panel]");

  gsap.timeline({
    scrollTrigger: {
      trigger: scene,
      start: "top top",
      end: `+=${panels.length * window.innerHeight}`,
      scrub: 1.1,
      pin: true,
      anticipatePin: 1,
    },
  })
    .to(panels, { yPercent: -100 * (panels.length - 1), ease: "none" })
    .to(scene.querySelectorAll("[data-story-depth]"), { yPercent: -16, ease: "none" }, 0);
});
```

### Progressive UI Reveal Pattern
```typescript
function initStoryScenes() {
  gsap.utils.toArray("[data-product-story]").forEach((section) => {
    const frames = section.querySelectorAll("[data-story-frame]");
    const labels = section.querySelectorAll("[data-story-label]");

    gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: "top top",
        end: "+=200%",
        scrub: 1,
        pin: true,
      },
    })
      .fromTo(frames, { autoAlpha: 0 }, { autoAlpha: 1, stagger: 0.25, ease: "none" })
      .fromTo(labels, { y: 20, autoAlpha: 0 }, { y: 0, autoAlpha: 1, stagger: 0.2, ease: "none" }, 0);
  });
}
```

### Section Handoff (Scene Transition)
```typescript
// Let the current scene smoothly transition into the next
gsap.to(".current-scene", {
  scale: 0.95,
  autoAlpha: 0,
  filter: "blur(8px)",
  scrollTrigger: {
    trigger: ".next-scene",
    start: "top bottom",
    end: "top center",
    scrub: 1,
  },
});

gsap.fromTo(".next-scene",
  { scale: 1.05, autoAlpha: 0, filter: "blur(12px)" },
  { scale: 1, autoAlpha: 1, filter: "blur(0px)", scrollTrigger: {
    trigger: ".next-scene",
    start: "top center",
    end: "center center",
    scrub: 1,
  }}
);
```

## Tuning Knobs
- **Pin duration**: extend for dense product stories, shorten for simple scenes
- **Scrub feel**: direct scrub (`true`) for technical walkthroughs, eased scrub (`0.8-1.4`) for cinematic
- **Reveal density**: more micro-reveals for complex UI, fewer for narrative sections
- **Transition intensity**: high-impact for section handoffs, subtle for content changes

## Performance Rules (Storytelling)
- Use `gsap.context()` in React, revert on unmount
- Kill ScrollTriggers on route changes: `ScrollTrigger.getAll().forEach(t => t.kill())`
- Refresh after images/fonts load: `ScrollTrigger.refresh()`
- Use `matchMedia()` to simplify sticky choreography on mobile



## CINEMATIC GSAP + LENIS MOTION SYSTEM (from MengTo)

## When to Use

- Full premium motion language, not one isolated animation
- Smooth scrolling + scroll reveals + pinned scenes + parallax + hover motion + cursor behavior
- Luxury editorial, Apple-level polish, creative studio portfolio

## Motion Taste

- **Smooth, elegant, slightly delayed, intentional**
- Staggered motion guides reading order
- Layered movement creates depth without busyness
- ScrollTrigger starts scenes when they enter viewport

**Avoid**: bounce/elastic/springy motion, fast abrupt transitions, large scale jumps, over-animated UI.

## Base Motion Tokens

| Property | Value |
|----------|-------|
| Eases | `power3.out`, `power4.out`, `expo.out` |
| Scroll scrub | `0.8` to `1.4` |
| Reveal duration | `0.75s` to `1.1s` |
| Hover duration | `0.35s` to `0.6s` |
| Cursor lag | `0.25s` to `0.45s` |
| Word stagger | `0.035s` to `0.07s` |
| Line stagger | `0.08s` to `0.14s` |
| Card stagger | `0.06s` to `0.1s` |
| Reveal trigger | `start: "top 82%"` |
| Pin handoff | `anticipatePin: 1` |

## Setup (Lenis + GSAP)

```bash
npm i gsap lenis
```

```typescript
import Lenis from "lenis";
import "lenis/dist/lenis.css";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);
gsap.defaults({ ease: "power3.out", duration: 0.85 });

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let lenis;

if (!reduceMotion) {
  lenis = new Lenis({
    lerp: 0.08,
    smoothWheel: true,
    wheelMultiplier: 0.9,
  });

  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((time) => { lenis.raf(time * 1000); });
  gsap.ticker.lagSmoothing(0);
}
```

## Markup API (Data Attributes)

```html
<!-- Text reveals -->
<h1 data-motion-text="lines">Digital products with cinematic restraint.</h1>
<p data-motion-text="words">Every interaction should feel deliberate.</p>

<!-- Scroll reveals -->
<section data-reveal-group>
  <article data-reveal="fade-up" data-reveal-item>...</article>
</section>

<!-- Image reveals -->
<figure data-image-reveal data-parallax-section>
  <img data-parallax-image src="/studio.jpg" alt="">
</figure>

<!-- Interactive -->
<a data-magnetic data-cursor-label="Explore" href="/work">Explore</a>
<div data-cursor><span data-cursor-label></span></div>
```

## CSS Foundation

```css
html.has-motion [data-motion-text],
html.has-motion [data-reveal],
html.has-motion [data-reveal-item],
html.has-motion [data-image-reveal] {
  visibility: hidden;
}

.motion-line-mask, .motion-word-mask {
  display: inline-block;
  overflow: hidden;
  vertical-align: top;
}

.motion-line, .motion-word {
  display: inline-block;
  will-change: transform, opacity, filter;
}

[data-image-reveal] { overflow: hidden; }

[data-parallax-image] {
  display: block; width: 100%; height: 115%;
  object-fit: cover; will-change: transform;
}

[data-cursor] {
  position: fixed; left: 0; top: 0; z-index: 9999;
  pointer-events: none; mix-blend-mode: difference;
  transform: translate3d(-50%, -50%, 0);
  will-change: transform;
}

@media (prefers-reduced-motion: reduce), (pointer: coarse) {
  [data-cursor] { display: none; }
}
```

## Staggered Text Reveals

```typescript
function splitWords(element: HTMLElement) {
  if (element.dataset.motionSplit === "true") return;
  const text = element.textContent || "";
  const parts = text.split(/(\s+)/);
  element.textContent = "";
  element.setAttribute("aria-label", text.trim());

  parts.forEach((part) => {
    if (!part.trim()) { element.appendChild(document.createTextNode(part)); return; }
    const mask = document.createElement("span");
    const word = document.createElement("span");
    mask.className = "motion-word-mask";
    word.className = "motion-word";
    word.textContent = part;
    mask.appendChild(word);
    element.appendChild(mask);
  });
  element.dataset.motionSplit = "true";
}

function initTextReveals() {
  if (reduceMotion) { gsap.set("[data-motion-text]", { autoAlpha: 1 }); return; }

  gsap.utils.toArray("[data-motion-text='words']").forEach((el) => {
    splitWords(el);
    const words = el.querySelectorAll(".motion-word");
    gsap.set(el, { autoAlpha: 1 });
    gsap.fromTo(words,
      { yPercent: 110, autoAlpha: 0, filter: "blur(8px)" },
      { yPercent: 0, autoAlpha: 1, filter: "blur(0px)",
        duration: 0.9, ease: "power4.out", stagger: 0.055,
        scrollTrigger: { trigger: el, start: "top 82%", once: true }
      }
    );
  });
}
```

## Scroll Reveals (Preset Map)

```typescript
const revealPresets = {
  "fade-up":    { from: { y: 32, autoAlpha: 0 }, to: { y: 0, autoAlpha: 1 } },
  "blur-in":    { from: { y: 18, autoAlpha: 0, filter: "blur(10px)" }, to: { y: 0, autoAlpha: 1, filter: "blur(0px)" } },
  "scale":      { from: { scale: 0.96, autoAlpha: 0 }, to: { scale: 1, autoAlpha: 1 } },
  "slide-left": { from: { x: 48, autoAlpha: 0 }, to: { x: 0, autoAlpha: 1 } },
};

function initScrollReveals() {
  if (reduceMotion) { gsap.set("[data-reveal]", { autoAlpha: 1 }); return; }

  gsap.utils.toArray("[data-reveal-group]").forEach((group) => {
    const items = group.querySelectorAll("[data-reveal-item]");
    gsap.fromTo(items,
      { y: 36, autoAlpha: 0, filter: "blur(8px)" },
      { y: 0, autoAlpha: 1, filter: "blur(0px)",
        duration: 0.95, ease: "power4.out", stagger: 0.075,
        scrollTrigger: { trigger: group, start: "top 82%", once: true }
      }
    );
  });
}
```

## Clip Image Reveals

```typescript
function initImageReveals() {
  if (reduceMotion) { gsap.set("[data-image-reveal]", { autoAlpha: 1, clipPath: "none" }); return; }

  gsap.utils.toArray("[data-image-reveal]").forEach((figure) => {
    const image = figure.querySelector("img");
    gsap.set(figure, { autoAlpha: 1 });

    gsap.timeline({ scrollTrigger: { trigger: figure, start: "top 82%", once: true } })
      .fromTo(figure, { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: 1.1, ease: "power4.out" })
      .fromTo(image, { scale: 1.08, autoAlpha: 0.75 }, { scale: 1, autoAlpha: 1, duration: 1.2, ease: "power4.out" }, 0);
  });
}
```

## Premium Hover (Magnetic + QuickTo)

```typescript
function initMagnetic() {
  if (reduceMotion || window.matchMedia("(pointer: coarse)").matches) return;

  gsap.utils.toArray("[data-magnetic]").forEach((element) => {
    const strength = Number(element.dataset.magnetic || 0.18);
    const xTo = gsap.quickTo(element, "x", { duration: 0.45, ease: "power3.out" });
    const yTo = gsap.quickTo(element, "y", { duration: 0.45, ease: "power3.out" });

    element.addEventListener("pointermove", (e) => {
      const rect = element.getBoundingClientRect();
      xTo((e.clientX - rect.left - rect.width / 2) * strength);
      yTo((e.clientY - rect.top - rect.height / 2) * strength);
    });
    element.addEventListener("pointerleave", () => { xTo(0); yTo(0); });
  });
}
```

## Custom Cursor

```typescript
function initCursor() {
  if (reduceMotion || window.matchMedia("(pointer: coarse)").matches) return;

  const cursor = document.querySelector("[data-cursor]");
  if (!cursor) return;

  const xTo = gsap.quickTo(cursor, "x", { duration: 0.35, ease: "power3.out" });
  const yTo = gsap.quickTo(cursor, "y", { duration: 0.35, ease: "power3.out" });

  document.addEventListener("pointermove", (e) => { xTo(e.clientX); yTo(e.clientY); });

  gsap.utils.toArray("[data-cursor-label]").forEach((target) => {
    target.addEventListener("pointerenter", () => gsap.to(cursor, { scale: 1.75, duration: 0.35 }));
    target.addEventListener("pointerleave", () => gsap.to(cursor, { scale: 1, duration: 0.35 }));
  });
}
```

## Init Order

```typescript
initTextReveals();
initScrollReveals();
initImageReveals();
initParallax();
initHorizontalGalleries();
initStoryScenes();
initMagnetic();
initCursor();
ScrollTrigger.refresh();
```

## Choreography Rules
- **Hero**: background/media first → headline lines → copy → CTA last
- **Sections**: label first → heading → media → cards/details last
- **Pinned scenes**: one idea per viewport
- **Parallax**: background slower, foreground faster, text stable
- **Cursor**: support navigation intent, don't fight it



## CINEMATIC SCROLL STORYTELLING (from MengTo)

## Page Anatomy

A premium scroll storytelling page follows this structure:

1. **Preloader**: black screen, progress bar, brand/title, intro fade
2. **Hero**: image parallax, masked headline reveal, scroll cue
3. **Intro**: word-by-word kinetic typography
4. **Story sections**: scroll-triggered fade-up, blur-in, clip reveals
5. **Recent Projects**: sticky card stack with scale + layered depth
6. **Gallery**: scroll-scrubbed horizontal or progressive reveals
7. **Footer**: parallax reveal or slow upward handoff

## Preloader Sequence

```typescript
function initPreloader(): Promise<void> {
  const loader = document.querySelector("[data-preloader]");
  const bar = document.querySelector("[data-preloader-bar]");
  if (!loader || reduceMotion) { loader?.remove(); return Promise.resolve(); }

  return new Promise((resolve) => {
    gsap.timeline({
      defaults: { ease: "power3.out" },
      onComplete: () => { loader.remove(); resolve(); },
    })
      .fromTo(bar, { scaleX: 0, transformOrigin: "left" }, { scaleX: 1, duration: 1.1 })
      .to(loader, { yPercent: -100, duration: 0.9, ease: "power4.inOut" }, "+=0.15");
  });
}
```

## Scroll-Linked Progression

```typescript
function initProgressionScenes() {
  if (reduceMotion) return;

  gsap.utils.toArray("[data-progress-scene]").forEach((scene) => {
    const media = scene.querySelector("[data-progress-media]");
    const copy = scene.querySelectorAll("[data-progress-copy]");

    gsap.timeline({
      scrollTrigger: {
        trigger: scene,
        start: "top top",
        end: "+=140%",
        scrub: 1.1,
        pin: true,
        anticipatePin: 1,
      },
    })
      .fromTo(media, { scale: 1.08 }, { scale: 1, ease: "none" })
      .fromTo(copy, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, stagger: 0.15, ease: "none" }, 0.15);
  });
}
```

## Sticky Card Stack

```css
[data-sticky-stack] { position: relative; }
[data-stack-card] {
  position: sticky; top: 12vh;
  transform-origin: center top;
  will-change: transform, opacity;
}
```

```typescript
function initStickyCardStack() {
  if (reduceMotion) return;

  gsap.utils.toArray("[data-sticky-stack]").forEach((stack) => {
    const cards = gsap.utils.toArray(stack.querySelectorAll("[data-stack-card]"));

    cards.forEach((card, index) => {
      const nextCard = cards[index + 1];
      if (!nextCard) return;

      gsap.to(card, {
        scale: 0.92 + index * 0.015,
        autoAlpha: 0.72,
        y: -24,
        ease: "none",
        scrollTrigger: {
          trigger: nextCard,
          start: "top 78%",
          end: "top 24%",
          scrub: true,
          invalidateOnRefresh: true,
        },
      });
    });
  });
}
```

## Footer Parallax Reveal

```typescript
function initFooterReveal() {
  if (reduceMotion) return;

  const footer = document.querySelector("[data-footer-parallax]");
  if (!footer) return;

  gsap.fromTo(footer,
    { yPercent: -12, autoAlpha: 0.85 },
    {
      yPercent: 0, autoAlpha: 1, ease: "none",
      scrollTrigger: { trigger: footer, start: "top bottom", end: "top 45%", scrub: 1 },
    }
  );
}
```

## Storytelling QA Checklist
- Content is readable with JavaScript disabled
- Reduced-motion users see static content, no smooth-scroll hijacking
- Scroll-triggered reveals play once (unless design asks for replay)
- Pinned sections don't overlap the next section
- Hover + cursor interactions disabled on touch devices
- No layout properties animated during scroll
- `ScrollTrigger.refresh()` runs after images/fonts/layout shifts
- Mobile has simplified or no pinning if performance drops
- Preloader exits reliably even if images load slowly

## Resources

See `references/` for detailed guides and code examples in `assets/`.

## External Resources

- [Official Documentation]

## PLUGINS

## When to Use

- Smooth scrolling to elements
- Drag interactions
- Flip animations (state changes)
- Motion along paths
- Text animations
- SVG animations

## Critical Patterns

### ScrollToPlugin

```typescript
import { gsap } from "gsap";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";

gsap.registerPlugin(ScrollToPlugin);

// Smooth scroll to element
gsap.to(window, {
  duration: 1,
  scrollTo: "#target-element",
  ease: "power2.inOut"
});

// Scroll to position
gsap.to(window, {
  duration: 1,
  scrollTo: { y: 500, autoKill: false }
});

// Scroll with offset
gsap.to(window, {
  duration: 1,
  scrollTo: { y: "#target", offsetY: 100 }
});
```

### Flip Plugin

```typescript
import { gsap } from "gsap";
import { Flip } from "gsap/Flip";

gsap.registerPlugin(Flip);

// Record state before change
const state = Flip.getState(".card");

// Make the change (add class, resize, etc.)
element.classList.add("expanded");

// Animate from recorded state to new state
Flip.from(state, {
  duration: 0.7,
  ease: "power2.inOut",
  targets: ".card",
  absolute: true,  // Handle layout changes
  onComplete: () => console.log("Done!")
});

// Preserve inline styles after
Flip.fit(element, state, { absolute: true });
```

### Draggable

```typescript
import { gsap } from "gsap";
import { Draggable } from "gsap/Draggable";

gsap.registerPlugin(Draggable);

// Basic drag
Draggable.create(".handle", {
  type: "x,y",           // "x", "y", "rotation", "scale"
  bounds: ".container",
  inertia: true,         // Physics-based throw
  onDrag: () => update(),
  onThrowUpdate: () => update(),  // While inertia active
  onDragEnd: () => savePosition()
});

// Draggable with bounds object
Draggable.create(".box", {
  bounds: { minX: 0, maxX: 300, minY: 0, maxY: 500 }
});
```

### MotionPath

```typescript
import { gsap } from "gsap";
import { MotionPathPlugin } from "gsap/MotionPathPlugin";

gsap.registerPlugin(MotionPathPlugin);

// Animate along SVG path
gsap.to(".ball", {
  motionPath: {
    path: "#path",
    align: "#path",
    alignOrigin: [0.5, 0.5],
    autoRotate: true
  },
  duration: 2,
  ease: "none"
});

// Curved path with control points
gsap.to(".ball", {
  motionPath: {
    path: [
      { x: 0, y: 0 },
      { x: 100, y: 200, curviness: 1.5 },
      { x: 200, y: 100 }
    ],
    curviness: 1.5
  },
  duration: 1.5
});
```

### SplitText (Premium)

```typescript
import { gsap } from "gsap";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(SplitText);

// Split text into lines, words, chars
const split = new SplitText(".hero-title", {
  type: "chars,words,lines",
  charsClass: "char",
  wordsClass: "word",
  linesClass: "line"
});

// Animate each category
gsap.from(split.chars, {
  y: 50,
  opacity: 0,
  stagger: 0.05,
  duration: 0.8,
  ease: "back.out(1.7)"
});

// Cleanup
split.revert();
```

### Observer (Touch/Mouse Events)

```typescript
import { gsap } from "gsap";
import { Observer } from "gsap/Observer";

gsap.registerPlugin(Observer);

Observer.create({
  target: window,
  type: "wheel,touch,pointer",
  wheelSpeed: -1,
  onUp: () => goUp(),
  onDown: () => goDown(),
  onRight: () => nextSlide(),
  onLeft: () => prevSlide()
});
```

## Commands

```bash
# Core + common plugins
npm install gsap

# Premium plugins (license required)
# https://gsap.com/pricing/
```

## Resources

See `references/` for detailed guides and code examples in `assets/`.

## External Resources

- [Official Documentation]

## PERFORMANCE

## When to Use

- Performance-critical animations
- Mobile optimization
- Large numbers of animated elements
- Complex ScrollTrigger setups
- 60fps requirements

## Critical Patterns

### USE TRANSFORMS (NOT layout properties)

```typescript
// ✅ DO THIS - GPU accelerated
gsap.to(element, {
  x: 100,        // transform: translateX(100px)
  y: 50,         // transform: translateY(50px)
  scale: 1.5,    // transform: scale(1.5)
  rotation: 360,  // transform: rotate(360deg)
  duration: 0.5
});

// ❌ NOT THIS - triggers layout/reflow
gsap.to(element, {
  left: 100,     // Triggers layout!
  top: 50,       // Triggers layout!
  margin: 20,    // Triggers layout!
  width: 200     // Triggers layout!
});
```

### will-change

```typescript
// Add to element BEFORE animation starts
element.style.willChange = "transform";

// Remove after animation completes
gsap.to(element, {
  x: 100,
  onComplete: () => {
    element.style.willChange = "auto";
  }
});

// For ScrollTrigger with pinning
gsap.to(element, {
  scrollTrigger: {
    trigger: element,
    willChangeTransform: true  // Enables will-change automatically
  }
});
```

### autoAlpha for Visibility

```typescript
// Use autoAlpha instead of opacity for hidden elements
gsap.to(hiddenElement, {
  autoAlpha: 0,    // Sets opacity: 0 AND visibility: hidden
  duration: 0.3
});

gsap.to(visibleElement, {
  autoAlpha: 1,     // Sets opacity: 1 AND visibility: visible
  duration: 0.3
});
```

### Batch Animations

```typescript
import { gsap } from "gsap";

const boxes = gsap.utils.toArray(".box");

// Group animation with batch
gsap.to(boxes, {
  x: 100,
  duration: 0.5,
  stagger: {
    each: 0.1,
    from: "start",
    grid: "auto"
  }
});

// Batch with onComplete
gsap.to(boxes, {
  x: 100,
  stagger: 0.1,
  onComplete: () => console.log("All done")
});
```

### QuickSetter (Performance-critical)

```typescript
// For frequent updates (like scroll callbacks)
const quickSetter = gsap.quickSetter(element, "x", "px");

// Much faster than gsap.to() in tight loops
function onScroll() {
  quickSetter(scrollY * 0.5);
}
```

### gsap.ticker for RAF

```typescript
// Use gsap's ticker instead of requestAnimationFrame
gsap.ticker.add(myUpdateFunction);

// For performance: remove when not needed
gsap.ticker.remove(myUpdateFunction);

// Adjust lag smoothing
gsap.ticker.lagSmoothing(0);
gsap.ticker.frameRate(60);
```

### ScrollTrigger Optimization

```typescript
// Pin optimization
ScrollTrigger.config({
  ignoreMobileResize: true  // Better mobile handling
});

// Debounced refresh
let refreshTimeout;
window.addEventListener("resize", () => {
  clearTimeout(refreshTimeout);
  refreshTimeout = setTimeout(() => {
    ScrollTrigger.refresh();
  }, 200);
});

// Use markers only in dev
scrollTrigger: {
  trigger: ".element",
  start: "top center",
  end: "bottom center",
  // markers: true  // REMOVE IN PRODUCTION
}
```

### GPU Layer Promotion

```typescript
// Force GPU layer
gsap.set(element, {
  force3D: true,  // Enables transform: translateZ(0)
  transformOrigin: "50% 50%"
});

// For fixed position elements
element.style.backfaceVisibility = "hidden";
element.style.perspective = "1000px";
```

### Memory Management

```typescript
// Kill unused tweens/timelines
tl.kill();           // Kill specific timeline
gsap.killTweensOf(target);  // Kill all tweens on element

// Clear all ScrollTriggers on unmount
ScrollTrigger.getAll().forEach(t => t.kill());

// Use context for cleanup (see gsap-react)
const ctx = gsap.context(() => {
  // animations
}, scopeRef);
return () => ctx.revert();
```

## Commands

```bash
npm install gsap

# For development only
npm install gsap-dev  # Adds performance warnings
```

## Resources

See `references/` for detailed guides and code examples in `assets/`.

## External Resources

- [Official Documentation]

## UTILS

## When to Use

- Value conversion and mapping
- Random generation
- Array manipulation
- Clamping and snapping
- Selector handling

## Critical Patterns

### Import

```typescript
import { gsap } from "gsap";
// All utils available via gsap.utils
const { clamp, random, mapRange, toArray } = gsap.utils;
```

### clamp

```typescript
// Clamp value between min and max
const result = clamp(0, 100, 150);  // Returns 100
const result2 = clamp(0, 100, -50); // Returns 0
const result3 = clamp(0, 100, 50); // Returns 50

// Function version for reuse
const clamp01 = clamp(0, 1);
const normalized = clamp01(1.5); // Returns 1
```

### mapRange

```typescript
// Map value from one range to another
const result = mapRange(0, 100, 0, 1, 50);  // Returns 0.5

// With inRange check
const result2 = mapRange(0, 100, 0, 1, 150, false); // Returns 1 (not clamped)

// Clamped version
const result3 = mapRange(0, 100, 0, 1, -50); // Returns 0 (clamped)
```

### normalize

```typescript
// Normalize value to 0-1 range
const result = normalize(50, 0, 100); // Returns 0.5
const result2 = normalize(0, 0, 100);  // Returns 0
const result3 = normalize(100, 0, 100); // Returns 1
```

### interpolate

```typescript
// Interpolate between two values
const result = interpolate(0, 100, 0.5);    // Returns 50
const result2 = interpolate(0, 100, 0);     // Returns 0
const result3 = interpolate(0, 100, 1);     // Returns 100

// With custom interpolator (e.g., color)
const interpolateColor = interpolate("red", "blue");
const color = interpolateColor(0.5); // Purple-ish

// Array interpolation
const interpolateArrays = interpolate([0, 0], [100, 100]);
const [x, y] = interpolateArrays(0.5); // [50, 50]
```

### random

```typescript
// Random number
random(0, 100);       // 0 to 100 (inclusive)
random(0, 100, true); // Float

// Random from array
random(["a", "b", "c"]); // "a" or "b" or "c"

// Random with step
random(0, 10, 2);     // 0, 2, 4, 6, 8, or 10
```

### snap

```typescript
// Snap to nearest value
snap(0.7, 0.1);  // 0.7
snap(0.73, 0.1); // 0.7

// Snap to array of values
snap(5, [0, 5, 10, 15]); // 5
snap(7, [0, 5, 10, 15]); // 5 (nearest)

// Snap to increment
snap(3.7, 0.5); // 3.5
```

### toArray

```typescript
// Convert any value to array
const arr = toArray(".box");     // All .box elements
const arr2 = toArray(document.querySelectorAll(".item"));
const arr3 = toArray("div");     // All divs
const arr4 = toArray(ref.current); // Single element wrapped
```

### selector

```typescript
// Create scoped selector function
const s = gsap.utils.selector(containerRef);

s(".item");      // containerRef.querySelectorAll(".item")
s(".item", 0);   // containerRef.querySelector(".item")

// Useful inside contexts
const ctx = gsap.context(() => {
  const s = gsap.utils.selector(scopeRef);
  gsap.to(s(".box"), { x: 100 });
}, scopeRef);
```

### wrap

```typescript
// Wrap value within range (loops)
wrap(0, 10, 5);  // 5
wrap(0, 10, 11); // 1 (wraps around)
wrap(0, 10, -1); // 9

// Wrap with unit
wrap(0, 360, 370); // 10 degrees
```

### wrapYoyo

```typescript
// Wrap with yoyo (bounces at edges)
wrapYoyo(0, 10, 5);   // 5
wrapYoyo(0, 10, 11);  // 9
wrapYoyo(0, 10, -1);  // 1
```

### distribute

```typescript
// Distribute values evenly in a range
const values = distribute(0, 100, 5);
// [0, 25, 50, 75, 100]

// Center-aligned
const centered = distribute(0, 100, 3, "center");
// [16.67, 50, 83.33]
```

### shuffle

```typescript
// Shuffle array in place
const arr = [1, 2, 3, 4, 5];
shuffle(arr);
// arr is now randomly ordered
```

## Commands

```bash
npm install gsap
```

## Resources

See `references/` for detailed guides and code examples in `assets/`.

## External Resources

- [Official Documentation]