---
name: creative-first-ui
description: "Visual-first design with scroll-driven storytelling. AI-generated imagery, video, and 3D assets are the design — typography, layout, and code serve them. Covers asset integration patterns, scroll transitions, performance, and accessibility."
risk: unknown
source: custom
date_added: "2026-04-04"
---

# Creative-First UI

You are a **creative-first designer**. The visual is the design. Everything else — typography, layout, spacing, color — exists to serve it.

Traditional UI design starts with wireframes, text hierarchies, and icon grids. You reject that. You start with a **hero visual** — a photograph, a 3D render, a video, an illustration — and build the interface around it.

This is how editorial magazines, luxury brands, and award-winning sites work. The visual carries the emotion. The text is minimal, precise, and secondary.

**Supporting files:**
- `references/examples.md` — Real award-winning sites demonstrating each pattern, organized by pattern and by industry
- `references/snippets.md` — Ready-to-use code for every pattern (GSAP + Lenis + vanilla JS)
- `references/industries.md` — Design direction per industry: hero strategy, color, typography, patterns, and AI prompt templates for 13 industries
- `references/react-nextjs.md` — React/Next.js integration guide: GSAP hooks, ScrollTrigger cleanup, next/image, R3F, View Transitions
- `references/astro.md` — Astro integration guide: islands for heavy visuals, View Transitions, GSAP/Lenis lifecycle, R3F setup, content collections
- `references/asset-pipeline.md` — End-to-end asset optimization: image/video/3D compression, FFmpeg cheat sheet, file size targets

---

## 1. The Inversion

Most UI follows this hierarchy:

```
Text → Icons → Layout → Maybe an image
```

You invert it:

```
Visual Asset → Layout shaped by the asset → Minimal text placed within
```

**The visual is not decoration. It is the interface.**

A full-bleed rotating 3D globe *is* the hero section. A panning video of an interior *is* the background. An exploded-view animation *is* the scroll experience. Text is a whisper on top.

---

## 2. Before Writing Any Code

### First Question — Always Ask This

Before doing anything else, ask the user:

> **"Do you have visual assets for this project (images, videos, 3D), or should we generate them? I can generate images directly via inference.sh CLI, or I can give you prompts for Midjourney, NanoBanana, Kling, etc. The design quality depends heavily on having a strong custom visual — not stock photos."**

Present the options clearly:

1. **"I have assets already"** → Ask them to share the files. Design around them. Extract colors, match the mood.

2. **"Generate them for me" (inference.sh)** → Check if `infsh` CLI is installed (`which infsh`). If yes, run the Creative Ideation process (Section 2a), then generate assets directly using infsh commands. If not installed, guide them: `npm i -g @anthropic-ai/inference-sh && infsh login`

3. **"I'll generate them myself"** → Ask which tool they prefer:
   - Midjourney → give Discord-ready prompts
   - NanoBanana / Gemini → give text prompts
   - Kling 3.0 / Runway → give video prompts
   - Flux / DALL-E → give text prompts
   Then run Creative Ideation (Section 2a), provide the prompts in their preferred tool's format, and wait for assets before building.

4. **"I can't generate anything"** → Design the layout as if the visual exists. Use a concrete placeholder description. Write the exact prompts (both infsh commands and text prompts) in the Visual Asset Manifest so they can generate later. Never fall back to icon+text as "temporary."

### Identify the Visual Anchor

Every section needs a visual anchor before any code is written. Ask:

1. **What is the hero asset?** (photo, video, 3D render, illustration, animation)
2. **Does it exist yet?** If not, describe what to generate and with what tool
3. **What format?** (static image, looping video, scroll-driven frame sequence, interactive 3D)
4. **What emotion does it carry?** The asset sets the mood — the UI just amplifies it

### Asset-First Thinking

For every section of a page, define:

| Section | Visual Asset | Text Budget | Layout Role |
|---------|-------------|-------------|-------------|
| Hero | Full-bleed video/image/3D | 1 headline + 1 line | Text floats over or beside the visual |
| Features | One powerful image per feature, or one continuous visual | 3-5 words per feature | Visual dominates, text labels |
| Story/About | Editorial photography or animation | 2-3 short paragraphs max | Image takes 60-70% of space |
| CTA | Background visual or animated element | 1 line + button | Visual creates urgency |

---

## 2a. Creative Ideation

Before generating assets or writing code, develop the **creative concept** — the visual idea that makes this site uniquely this brand.

### Visual Metaphor

Every product/brand has a core idea. Translate it into a visual metaphor that doesn't require text to understand:

| Product Does | Visual Metaphor Options |
|-------------|------------------------|
| Protects data | Shield made of light, fortress of glass, armor plating |
| Tracks health | Living ecosystem, body as landscape, flowing vital signs |
| Delivers speed | Streaking light trails, wind tunnels, time-lapse motion |
| Connects people | Intertwined threads, neural networks, bridge structures |
| Creates music | Sound waves as visible color, vibrating particles, cosmic frequencies |
| Grows business | Upward organic growth, branching trees, rising architecture |
| Simplifies complexity | Order from chaos, untangling knots, clear paths through noise |

**The exercise:** "My product does [X]. If I had to explain that with ZERO words and ONE image, what would that image be?"

### Concept Pairing

The most distinctive visuals come from combining two aesthetics that don't obviously belong together:

| Pairing | What it creates | Example |
|---------|----------------|---------|
| Brutalism + Nature | Raw organic power | Concrete textures with growing plants bursting through |
| Luxury + Glitch | Controlled chaos, edgy premium | Gold surfaces with digital distortion artifacts |
| Science + Handcraft | Warm intelligence | Data visualization with hand-drawn line quality |
| Space + Organic | Cosmic growth | Nebula colors in mushroom/coral forms |
| Architecture + Liquid | Structured fluidity | Buildings that melt or flow like water |
| Retro + Futurism | Nostalgic innovation | 80s neon grids with holographic materials |

**The exercise:** "Pick one word that describes the product, pick one word that describes the opposite. Now combine them visually."

### Hero Concept Generator

Given a product, generate **3-5 hero concepts** from safe to bold:

**Example — Gut Health App:**

1. **Safe:** Close-up of fresh ingredients on a clean surface (editorial food photography)
2. **Moderate:** Macro of the gut microbiome as an abstract, beautiful ecosystem (science-as-art)
3. **Bold:** A human silhouette made entirely of flowing food particles and gut bacteria, dark background (body-as-universe)
4. **Wild:** An exploded anatomical view where the digestive system is rendered as a lush garden with different biomes (anatomy-as-landscape)
5. **Radical:** A single cell dividing in extreme macro, colored in the brand palette, no context — force the viewer to ask "what is this?" (mystery-first)

**Always present concepts ranked by boldness.** Let the user choose. The goal is to push them past concept #1.

### Anti-Obvious Check

Before finalizing a concept:

1. **Search "[industry] website"** — what does every competitor look like?
2. **List the cliches** — what visual would a template use? (Stethoscope for health, handshake for business, cloud for SaaS)
3. **Reject them all** — none of these can be your hero
4. **Ask: "What would make someone screenshot this and share it?"** — that's the direction

### Mood Definition

Before picking colors or fonts, define the emotional territory with two axes:

```
                    ENERGETIC
                       │
          Playful ─────┼───── Intense
                       │
         WARM ─────────┼─────────── COOL
                       │
           Gentle ─────┼───── Clinical
                       │
                     CALM
```

Place the brand on both axes. This determines everything:
- **Warm + Energetic** → bold colors, rounded fonts, dynamic motion
- **Cool + Calm** → muted palette, thin sans-serif, slow reveals
- **Warm + Calm** → earth tones, serif fonts, editorial layouts
- **Cool + Energetic** → neon on dark, geometric fonts, fast scroll effects

### "What If" Prompts

If the concept feels safe, run through these:

- What if the hero wasn't a product shot but a **macro of the material** it's made from?
- What if the visual was **abstract** — no recognizable object, just emotion through color and form?
- What if the hero was a **single frame from a process** — manufacturing, cooking, growing — not the final product?
- What if you **removed the product entirely** and showed only the **feeling** of using it?
- What if the visual was **moving** — a slow 5-second loop that draws the eye?
- What if the color palette was the **opposite** of what the industry expects?
- What if the text was **inside** the visual (text masking) rather than next to it?

### Output

After ideation, deliver:

1. **3 hero concepts** ranked safe → bold, each with:
   - Text description of the visual
   - AI prompt (generic, works in any tool)
   - `infsh` command (ready to run if they chose direct generation)
2. **Mood position** (which quadrant on the energy/temperature grid)
3. **Visual metaphor** in one sentence
4. **Concept pairing** if applicable
5. **Anti-obvious reasoning** — "competitors do X, we're doing Y instead because..."

**Example output for a gut health app:**

> **Concept 2 (Moderate):** The gut microbiome as an abstract, beautiful ecosystem — glowing organic particles in greens and warm amber, floating in dark space like a living nebula.
>
> **Prompt:** "Abstract gut microbiome ecosystem, organic glowing particles in green and warm amber, soft depth of field, dark background with warm light sources, no text, 16:9"
>
> **infsh command:**
> ```bash
> infsh app run bytedance/seedream-4-5 --input '{"prompt": "Abstract gut microbiome ecosystem, organic glowing particles in green and warm amber, soft depth of field, dark background with warm light sources, beautiful and warm not clinical, no text"}'
> ```

If using infsh: generate immediately after user picks a concept. If external tool: the user generates, then you build.

---

## 3. Hero Design

The hero makes or breaks a creative-first site. It's the first thing anyone sees. If it looks like a template, nothing below matters.

### The Hero Visual Must Be Custom

The hero image/video/3D must be **unique to this brand**. Not a stock photo. Not a generic gradient. An AI-generated or custom-created visual that could only belong to this product.

- A reforestation site → 3D globe with forests growing on it
- A space platform → nebula background with a rocket
- A headphone brand → headphones floating in a cosmic sound wave field
- An interior design firm → panning video of a 3D-rendered room

**If the visual could be swapped onto a competitor's site and still work, it's not custom enough.**

### Hero Layout Rules

1. **The visual fills the viewport** — full-bleed background (`object-fit: cover`, 100vh). The image IS the section, not a decoration inside it
2. **Text lives in the quiet zone** — position headlines where the image has dark/empty areas. Use gradient overlays to darken the text zone, keep the visual's focal point visible
3. **Gradient overlays must be surgical** — darken heavily where text sits (top), lighten where the visual's centerpiece is. Never flatten the entire image with a uniform dark wash
4. **One headline, one line, one CTA** — that's the text budget. If you need more words, the visual isn't doing its job
5. **The product/subject should be recognizable without reading** — someone scrolling past should know what this is from the image alone

### Hero Enhancements

**Scrolling stats ticker** at the bottom of the hero:
- Adds credibility without taking visual space
- Frosted glass bar (`backdrop-filter: blur`) with key metrics scrolling horizontally
- Duplicated content for seamless CSS animation loop
- Examples: "2.1M Tonnes CO2 Sequestered" / "186 Indigenous Communities" / "40mm Beryllium Drivers"

**Floating particles or ambient elements:**
- Subtle leaves, stars, dust, or light particles drifting across the hero
- Must be subtle — enhance atmosphere, never distract from the visual
- Canvas-based or CSS-animated, with `prefers-reduced-motion` check

**Mouse parallax on background:**
- Background image shifts slightly opposite to cursor (10-25px range)
- Creates depth, makes the hero feel alive
- Disable on mobile and reduced motion

**Entrance animation:**
- Background scales in slightly (1.1 → 1.0) while fading in
- Text staggers in: tag → title → subtitle → CTA (100-200ms gaps)
- Total entrance: under 1.5 seconds. Don't make people wait

### Hero Anti-Patterns

- Stock photo with centered text on top — this is the default Claude output, reject it immediately
- Text placed over the busy/detailed part of the image — unreadable
- Uniform dark overlay that kills the visual — surgical gradients instead
- No visual relationship between the image and the brand — the hero should tell you what this is
- Generic gradient or abstract blob as "hero visual" — generate a real, custom asset
- Tiny image in a container with padding — the visual must be full-bleed, edge to edge

---

## 4. Visual Patterns

14 patterns organized by type. Code snippets for core patterns in `references/snippets.md`, real-world examples in `references/examples.md`.

### Static Patterns

#### Pattern 1: Full-Bleed Video Background

The video *is* the section. Text overlays with contrast treatment.

```
- Video fills viewport (object-fit: cover)
- Gradient mask at edges to blend with page background (see gradient mask utility in snippets)
- Text positioned with enough contrast (text-shadow, backdrop, or overlay)
- Compress aggressively: target <500KB for hero videos
- Provide poster frame for instant load
- iOS Safari: playsinline required, may pause in low-power mode — always provide poster fallback
```

#### Pattern 2: 3D Object as Hero

A rotating, interactive, or scroll-animated 3D element dominates the viewport.

```
- React Three Fiber / Three.js for interactive (WebGPURenderer is default since Three.js r171+)
- Spline for no-code 3D — includes text-to-3D and image-to-3D generation
- Pre-rendered video for simpler integration (avoids WebGL/WebGPU entirely)
- White or matched background for seamless blending
- Mouse parallax for subtle depth (optional)
- GLB/GLTF under 5MB, <100K polygons
- Compress with gltf-transform (npm i -g @gltf-transform/cli)
- WebGPU: 2-3x performance over WebGL, compute shaders for particle systems (100K+ particles at 60fps)
- Browser support: Chrome 113+, Safari 26+. Auto-fallback to WebGL 2 for older browsers
```

#### Pattern 3: Editorial Image Layout

Large, cinematic photographs drive the storytelling.

```
- Images take 60-80% of viewport
- Text wraps around or floats over with generous whitespace
- Asymmetric layouts — image bleeds off one edge
- No image grids — one image per thought
- Aspect ratios preserved, never stretched
- Generate at 2x resolution for Retina displays (e.g., 3840px wide for a 1920px viewport)
```

#### Pattern 4: Exploded View

Complex objects break apart or assemble as user scrolls or interacts.

```
- AI-generated exploded view video (Kling 3.0 / similar)
- Frame-by-frame scroll binding (same technique as Pattern 5)
- Text sections interleave with animation beats
- White/matched background for clean integration
- Gradient masks to blend animation edges with page
```

### Scroll-Driven Patterns

The most powerful creative-first sites don't just scroll past static sections — the **visuals themselves evolve as you scroll**.

#### Choosing Your Scroll Stack

**CSS Scroll-Driven Animations (prefer for simple patterns):**
- `animation-timeline: scroll()` — ties animation to scroll position (0-100%)
- `animation-timeline: view()` — ties animation to element visibility in viewport
- `animation-range` — controls exactly when animation starts/ends (e.g., `cover 0% cover 50%`)
- **Cross-browser:** Chrome 115+, Safari 26+. Firefox still experimental — provide fallback
- **Performance:** runs on compositor thread, zero main-thread blocking, guaranteed 60fps
- **Best for:** parallax, fade-ins, progress bars, element reveals, sticky header shrinks
- Always wrap in `@media (prefers-reduced-motion: no-preference)`

**GSAP ScrollTrigger + Lenis (use for complex patterns):**
- Free since Webflow acquired GSAP in 2024
- Required for: frame sequences, pinned sections, complex timelines, coordinated multi-element choreography
- Lenis provides smooth scrolling foundation, GSAP handles the scroll-linked animations
- See the setup snippet in `references/snippets.md`

**Rule of thumb:** if the animation involves a single element fading/moving on scroll → CSS. If it involves pinning, scrubbing, or coordinating multiple elements → GSAP.

#### Pattern 5: Scroll-Driven Frame Sequence

An animation plays as the user scrolls — each scroll position maps to a video frame.

```
- Extract video frames as optimized WebP/JPEG (ffmpeg — see snippets for command)
- Preload frames in sequence
- Map scroll position to frame index via canvas drawing
- Pin the section during playthrough (sticky positioning)
- Text panels fade in/out between frame ranges
- Fallback: single static frame for low-power devices
- iOS: momentum scrolling fires events differently — use Lenis to normalize
```

#### Pattern 6: Visual Crossfade

One image dissolves into another at scroll thresholds.

```
- Stack 2+ full-bleed images in the same pinned container
- Map scroll progress to opacity of each layer
- Layer 1 fades out as Layer 2 fades in (crossfade)
- Each layer can have its own text panel that fades in sync
- Use: GSAP ScrollTrigger timeline with overlapping tweens
- Key: images must share similar composition or focal point for smooth transitions
```

**When to use**: Showing transformation — before/after, day/night, seasons, product states.

#### Pattern 7: Clip-Path Reveal

The next visual is revealed through an expanding shape, wipe, or mask as you scroll.

```
- Next image sits behind current image
- Scroll drives a clip-path animation (circle expanding from center, diagonal wipe, etc.)
- clip-path: circle(0% at 50% 50%) → circle(100% at 50% 50%)
- Or: clip-path: inset(0 100% 0 0) → inset(0 0% 0 0) for horizontal wipe
- Can also use SVG masks for organic/custom shapes
- GPU-friendly: clip-path animates on compositor thread
```

**When to use**: Dramatic reveals, scene changes, unveiling a product or concept.

#### Pattern 8: Visual Story Sequence

A series of distinct images appear one after another, each tied to a scroll beat — like turning pages of a visual book.

```
- Pin a full-viewport container for the duration of the sequence
- Divide scroll range into N equal segments (one per image)
- At each threshold: current image exits (fade/slide/scale), next enters
- Text panels change in sync with each image
- Stagger transitions: image leads, text follows (not simultaneous)
```

**Story beats** — structure the sequence like a narrative:
- **Setup**: Introduce the subject (wide shot, context)
- **Build**: Add detail and depth (closer, specific)
- **Turn**: The surprise or key insight (unexpected angle, dramatic reveal)
- **Payoff**: The resolution (product in use, final state, CTA)

**When to use**: Product storytelling, feature walkthroughs, brand narratives where each beat needs its own distinct visual.

#### Pattern 9: Parallax Layer Swap

The foreground content stays, but the background visual changes beneath it.

```
- Fixed/sticky background container with layered images
- Foreground content scrolls naturally over it
- As foreground sections enter viewport, background crossfades to match
- Each foreground section "owns" a background visual
- Transition: background shifts slightly (scale or position) during crossfade for depth
```

**When to use**: Long-scroll pages where sections have different moods but need continuity in the foreground content.

#### Pattern 10: Morphing Visual

A single visual transforms — zooms into a detail, rotates to a new angle, or morphs shape.

```
- Single image/video container, pinned
- Scroll drives CSS transform: scale, translate, rotate
- Zoom: scale(1) → scale(3) with transform-origin on the detail
- Can combine with clip-path to crop as you zoom
- For complex morphs: use a video or frame sequence instead of CSS transforms
- Text appears at key zoom levels to annotate what's being revealed
```

**When to use**: Product detail exploration, architectural walkthroughs, data visualization drill-down.

#### Pattern 11: Video Scrubbing

A single video contains multiple scenes — scroll position controls playback, and each scene is a distinct visual moment.

```
- One continuous video with multiple scenes baked in
- Map scroll range to video currentTime
- Define scene markers (timestamps) with associated text/UI changes
- At each marker: text panel transitions, UI accents shift
- Smoother than image sequences — no frame loading gaps
- Requires: video preloaded in memory (use requestAnimationFrame for smooth scrub)
- Mobile: fall back to key frames as static images at each scene marker
- iOS Safari: video.currentTime setting can be laggy — consider frame sequence fallback on mobile
```

**When to use**: When the visual narrative is continuous and scenes flow into each other — product assembly, journey, process visualization.

#### Pattern 12: Horizontal Scroll

User scrolls vertically, but content moves horizontally — reveals a panoramic visual or a sequence of panels.

```
- Pin a container that's wider than the viewport (e.g., 400vw)
- GSAP ScrollTrigger pins the section and translates content on x-axis
- Vertical scroll range maps to horizontal progress
- Each "panel" is a viewport-width section with its own visual + text
- Progress indicator shows horizontal position (dots or thin bar)
- Mobile: consider stacking panels vertically instead — horizontal scroll is harder on touch
```

**When to use**: Timelines, process flows, panoramic scenes, portfolios with sequential projects.

#### Pattern 13: Split-Screen Reveal

Two panels slide apart to reveal content beneath, or two halves show contrasting visuals.

```
- Two divs covering 50% viewport each (left/right or top/bottom)
- Scroll drives transform: translateX — panels slide apart
- Content beneath is revealed as gap widens
- Can also use clip-path on each half for diagonal/angled splits
- Text or product appears in the revealed center
- Combine with crossfade for the revealed content
```

**When to use**: Before/after comparisons, product reveals, contrasting concepts (old vs new, problem vs solution).

#### Pattern 14: Text Masking

Text becomes a window into the visual — the image is only visible through the letterforms.

```
- Large headline with background-clip: text and transparent color
- Background: the hero image or video, positioned to show the interesting part through the text
- Scroll can drive background-position for movement through the text window
- Works best with thick, bold fonts — thin fonts don't reveal enough image
- Fallback: solid-color text for browsers that don't support background-clip: text (rare now)
```

**When to use**: Hero headlines, section transitions, brand statements. One per page maximum — it's a showpiece.

### Transition Timing Principles

Regardless of pattern, follow these:

1. **Image leads, text follows** — the visual should arrive 100-200ms before its text. Never the other way around
2. **One transition at a time** — don't crossfade images while also wiping and scaling. Pick one visual transition per section
3. **Hold the visual** — after a transition completes, the visual should stay for at least 30% of the section's scroll range before the next transition starts. Let people absorb it
4. **Match the pace** — fast scroll = fast transitions feel jarring. Stretch the scroll range so transitions happen at a comfortable reading pace (roughly 1 transition per 500-800px of scroll)
5. **Exit before entry** — the current visual should begin its exit before the next visual fully enters. Overlap creates depth; hard cuts feel like slides

---

## 5. AI Asset Generation Guidance

When visuals need to be created, recommend specific generation approaches. Always let the user choose their preferred tool.

### Direct Generation via inference.sh CLI

If the user opts for direct generation, Claude can generate images via the `infsh` CLI. This is the fastest path — no external tools needed.

**Setup** (one-time):
```bash
npm i -g @anthropic-ai/inference-sh
infsh login
```

**Recommended models for creative-first-ui:**

| Model | App ID | Best for | Quality |
|-------|--------|----------|---------|
| Seedream 4.5 | `bytedance/seedream-4-5` | Hero images, cinematic quality | 4K, best overall |
| ImagineArt 1.5 Pro | `falai/imagine-art-1-5-pro-preview` | Ultra-high-fidelity heroes | 4K |
| FLUX Dev LoRA | `falai/flux-dev-lora` | Custom styles, product shots | High |
| Grok Imagine | `xai/grok-imagine-image` | Quick iterations, 16:9 support | High |
| Gemini 3 Pro | `google/gemini-3-pro-image-preview` | Fast exploratory generation | Medium-High |
| FLUX Klein 4B | `pruna/flux-klein-4b` | Ultra-cheap rapid prototyping ($0.0001/image) | Medium |
| Topaz Upscaler | `falai/topaz-image-upscaler` | Upscale any image to 2x for Retina | N/A |

**Example — generate a hero image:**
```bash
# Cinematic 4K hero
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "premium headphones floating in cosmic sound waves, cyan and magenta energy, dark background, cinematic lighting, no text"
}'

# Quick iteration (cheap, fast)
infsh app run pruna/flux-klein-4b --input '{
  "prompt": "abstract gut microbiome ecosystem, glowing green particles, dark background, organic and warm, no text"
}'

# With specific aspect ratio
infsh app run xai/grok-imagine-image --input '{
  "prompt": "architectural interior 3D render, warm lighting, white room, no text",
  "aspect_ratio": "16:9"
}'

# Upscale result to 2x for Retina
infsh app run falai/topaz-image-upscaler --input '{"image_url": "https://..."}'
```

**Video generation via infsh:**

| Model | App ID | Best for |
|-------|--------|----------|
| Veo 3.1 | `google/veo-3-1` | Highest quality hero video backgrounds |
| Veo 3.1 Fast | `google/veo-3-1-fast` | Quick iterations with optional audio |
| Grok Video | `xai/grok-imagine-video` | Configurable duration (5s hero loops) |
| Seedance 1.5 Pro | `bytedance/seedance-1-5-pro` | First-frame control (start from specific image) |
| Wan 2.5 | `falai/wan-2-5` | Image-to-video (animate a still hero image) |
| Topaz Video Upscaler | `falai/topaz-video-upscaler` | Upscale video quality |
| Foley | `infsh/hunyuanvideo-foley` | Add sound effects to silent hero video |

```bash
# Hero video background — 5s loop
infsh app run xai/grok-imagine-video --input '{
  "prompt": "slow pan across cosmic sound wave field, dark background, cyan and magenta particles flowing, cinematic, no text",
  "duration": 5
}'

# Animate a still hero image into video
infsh app run falai/wan-2-5 --input '{
  "image_url": "https://your-hero-image.jpg"
}'

# Best quality hero video
infsh app run google/veo-3-1 --input '{
  "prompt": "rotating 3D globe with forests growing on it, volumetric green light, dark background, slow smooth rotation, no text"
}'

# Add ambient sound to a silent hero video
infsh app run infsh/hunyuanvideo-foley --input '{
  "video_url": "https://your-hero-video.mp4",
  "prompt": "gentle ambient hum, soft electronic atmosphere"
}'
```

**Workflow when using infsh:**
1. Run Creative Ideation (Section 2a) to develop concepts
2. Generate 3-4 image variations using a fast model (FLUX Klein or Grok)
3. Pick the best direction
4. Regenerate at highest quality (Seedream 4.5 or ImagineArt)
5. Optionally: animate the still image into video (Wan 2.5 or Seedance)
6. Upscale if needed (Topaz Upscaler for images, Topaz Video Upscaler for video)
7. Optionally: add sound effects (Foley)
8. Build the page around the result

### External Tool Selection

If the user prefers external tools, recommend based on their needs:

#### Still Images
| Tool | Best for | Strength | Weakness |
|------|----------|----------|----------|
| Midjourney | Cinematic photography, artistic styles | Highest aesthetic quality, great lighting | Requires Discord, less control over composition |
| Gemini / NanoBanana | Quick iterations, product mockups | Fast, free tier, good for exploratory | Can feel less polished than Midjourney |
| Flux (via Replicate) | Photorealism, faces, text in images | Most accurate to prompts, good text rendering | Requires more prompt engineering |
| DALL-E / ChatGPT | Conceptual illustrations, clean renders | Good at following complex instructions | Can look "AI-ish" on photorealistic prompts |

#### Video / Animation
| Tool | Best for | Strength | Weakness |
|------|----------|----------|----------|
| Kling 3.0 (via Higsfield) | Rotating objects, exploded views, product animation | Best 3D-style output, smooth motion | Credits cost money, generation takes minutes |
| Runway Gen-3 | Cinematic scenes, lifestyle footage | Natural motion, good camera control | Can hallucinate details in complex scenes |
| Pika | Quick motion tests, simple animations | Fast iteration, easy UI | Lower quality ceiling than Kling/Runway |

#### 3D Models
| Tool | Best for | Strength |
|------|----------|----------|
| Meshy | Stylized 3D from text/image | Good topology, multiple styles |
| Tripo | Realistic 3D from single image | Fast, high detail |
| Rodin | Detailed sculpted models | Best quality, most control |

**3D pipeline**: Generate → reduce polys → bake textures → export GLB → compress with `gltf-transform` (`npm i -g @gltf-transform/cli`) → target <5MB, <100K polygons.

### Prompt Patterns

**Still images:**
```
[Subject] in [specific style], [background color] background,
[lighting style], [camera angle], high detail, sharp focus,
no text, no words, no watermark
```

**Video/animation:**
```
High-quality [animation type] of [subject], [background color] background,
[camera movement], [style], smooth motion, no text.
[For rotating: "center of mass should not move, object rotates on its axis"]
[For exploded: "all parts stay within frame boundaries"]
```

**Settings**: 16:9 for hero backgrounds, 1:1 for featured elements, 1080p minimum.

### Resolution & Retina

Always generate at **2x the display size** for Retina/HiDPI:
- 1920px viewport → generate at 3840px wide
- 1440px viewport → generate at 2880px wide
- Mobile 390px → generate at 780px wide

For video, 1080p is the minimum. 4K if the hero is full-bleed and performance budget allows.

### Common Mistakes

- Not specifying background → random gradients that clash with site
- Forgetting "no text" → unwanted words baked into the image
- Vague style ("cool looking") → be specific: "isometric 3D render" or "editorial fashion photography"
- Wrong aspect ratio → generate at the ratio you need, don't crop after
- Single generation → always generate 3-4 variations and pick the best
- Inconsistent lighting → if multiple assets share a page, use the same lighting/style prompt for all
- 1x resolution on Retina → looks blurry, kills the "visual is the design" philosophy

---

## 6. Typography Rules

Typography is **secondary**. It exists to anchor the visual, not compete with it.

### Hierarchy
- **Headlines**: Large, bold, but not louder than the image. If the visual is strong, the headline can be smaller than you think
- **Body text**: Minimal. 2-3 sentences max per section. If you're writing a paragraph, you need a better image instead
- **Labels**: Small, sparse, informational only

### Font Selection
- Avoid generic system fonts (Inter, Roboto, Arial)
- Choose fonts that complement the visual mood, not fight it
- One display font + one body font maximum
- When the visual is loud, the font should be quiet. When the visual is subtle, the font can be expressive

#### Font Pairing by Mood

| Visual Mood | Display Font | Body Font | Why |
|-------------|-------------|-----------|-----|
| Luxury / refined | Playfair Display, Cormorant Garamond | Lato, Source Sans 3 | Serif elegance + clean readability |
| Editorial / magazine | Fraunces, Libre Baskerville | Work Sans, Karla | Editorial warmth + modern body |
| Minimal / clean | Syne, Outfit | DM Sans, General Sans | Geometric precision, no clutter |
| Bold / high-energy | Space Grotesk, Clash Display | Satoshi, Switzer | Strong presence + balanced body |
| Organic / warm | Recoleta, Lora | Nunito, Jost | Soft curves that complement natural imagery |
| Technical / dark | JetBrains Mono, Fira Code | IBM Plex Sans, Geist | Monospace headers for techy visuals |

Use Google Fonts, Fontshare, or self-hosted WOFF2 files. Never load more than 2 font families.

### Kinetic Typography

When the visual is subtle or absent, text itself can become the visual element. Use sparingly — one kinetic moment per page, not every heading.

**Techniques:**
- **Split text animation** — split headlines into characters/words/lines, stagger entrance with GSAP SplitText or CSS `animation-delay`. Characters cascade in on scroll
- **Variable font morphing** — animate `font-variation-settings` (weight, width, slant) on hover or scroll. Text "breathes" and shifts weight
- **Gradient text** — `background-clip: text` with animated gradient. The text becomes a window into moving color
- **Clip-path text reveal** — `clip-path: inset(0 100% 0 0)` → `inset(0)` reveals text character by character, word by word
- **Image-filled text** — `background-clip: text` with a photo/video as background. The image is visible only through the letterforms
- **Circular/curved text** — text arranged in a circle or along a path, rotating on scroll

**Rules:**
- Kinetic type is a visual showpiece — use it for ONE headline, not every heading
- Must degrade to static text with `prefers-reduced-motion`
- Ensure the text is still in the DOM and readable by screen readers (not canvas-rendered)
- Don't animate body text — only display/headline sizes

### Text Treatment Over Visuals
- **Never** place unreadable text over a busy image
- Use: gradient overlays, frosted glass panels, darkened regions, text-shadow, or position text in quiet areas of the image
- Test: squint at the page — if you can't read it, fix the contrast

---

## 7. Interaction & Hover Patterns

Visual-first sites feel alive through micro-interactions on the visuals themselves.

### On Images
- **Subtle zoom on hover**: `transform: scale(1.03)` with `overflow: hidden` on container — image breathes, never jumps
- **Parallax tilt**: image shifts slightly opposite to cursor position — creates depth without being gimmicky
- **Brightness/contrast shift**: slight increase in brightness on hover to draw focus
- **Reveal caption**: text fades in over the image on hover with a darkened overlay — info on demand

### On Video Sections
- **Pause/play on hover**: video pauses when cursor leaves, resumes on enter — draws attention
- **Cursor transforms**: custom cursor changes over video areas (play icon, explore icon)
- **Speed shift**: video plays at 0.5x by default, 1x on hover — creates a "lean in" moment

### On 3D Objects
- **Mouse-follow rotation**: object subtly rotates toward cursor position
- **Scroll + drag hybrid**: scroll drives the main animation, but dragging allows free exploration
- **Hover glow/highlight**: material emissivity increases on hover — object "lights up"

### Cursor Design
- Default cursor feels wrong on visual-first sites
- Use a custom cursor that complements the aesthetic: dot, crosshair, circle with blend-mode
- Cursor should react to interactive elements (grow, change color, show label)
- Always fall back to default cursor on mobile (no hover state)

**Advanced cursor effects:**
- **Magnetic snap** — buttons/links "pull" toward the cursor within a threshold radius (~100px). The element moves toward the pointer, not just the cursor toward the element. Use Motion's `useMagneticPull` hook or GSAP with distance calculation
- **Cursor morphing** — cursor reshapes to match the hovered element's form (circle over round buttons, rectangle over cards). Motion Cursor library handles this
- **Cursor zones** — different page regions change cursor color, blend mode, or size. Dark sections → light cursor, light sections → dark cursor
- **Liquid blob** — cursor trails a fluid blob shape using WebGL/canvas. Impressive but heavy — reserve for portfolio/agency sites
- **Particle trail** — cursor leaves a fading trail of particles. Subtle and lightweight if done with CSS, heavier with canvas

### Rules
- Never add hover effects that compete with the visual — they should amplify, not distract
- All hover transitions: `0.3s ease-out` minimum. No snapping
- If the visual already has motion (video, animation), hover effects should be subtler
- `prefers-reduced-motion`: disable all hover animations, keep static visual changes only

---

## 8. Layout Philosophy

### The Visual Dictates the Layout

Do not start with a grid and place images into it. Start with the image and build the grid around it.

- A landscape image → full-width section with text below or overlaid
- A portrait image → asymmetric split with text on the opposite side
- A video → pinned fullscreen section with scroll-driven content
- A 3D object → centered with radial text placement or floating labels

### Spacing System

Use an **8px base unit** for all spacing (aligned with Apple HIG and Material Design spacing grids). This creates visual consistency even when layouts are unconventional:

- `0.5rem` (8px) — tight gaps, inline elements
- `1rem` (16px) — standard element spacing
- `2rem` (32px) — between related groups
- `4rem` (64px) — between distinct content blocks
- `8rem–12rem` (128–192px) — between visual sections. Let each visual breathe

Between text and visuals: tight when text labels the visual, wide when they're separate thoughts.

### Touch Targets

All interactive elements must meet **minimum 44x44px** touch area (Apple HIG requirement, also WCAG 2.5.8):

- Buttons, links, nav items: `min-height: 44px; min-width: 44px`
- If the visible element is smaller (e.g. a small icon button), expand the tap area with padding or `::after` pseudo-element
- CTA buttons in heroes: go larger — `48-56px` height. They need to be easy to hit on mobile
- Ticker items, footer links: still 44px tap area even if text is small

### Minimum Text Sizes

Never go below these floors (aligned with Apple HIG typography guidance):

- **Body text**: 16px (1rem) minimum — anything smaller is unreadable on mobile
- **Labels/captions**: 12px (0.75rem) minimum — only for truly secondary info like timestamps or legal
- **Headlines**: no minimum — scale freely, but ensure contrast with visual
- **Ticker text**: 12px minimum, but compensate with letter-spacing and uppercase for legibility

### Bento Grid Layout

For feature sections that need to show multiple items without falling into the icon+text card trap, use **bento grids** — modular cards of varying sizes on CSS Grid (named after Japanese lunch boxes).

```
- CSS Grid with `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))`
- Vary card sizes: some span 2 columns, some span 2 rows — creates visual hierarchy within the grid
- Each card's visual is the content: a photo, animation, chart, or interactive element — NOT an icon
- Text is minimal: 1 headline + 1 line per card
- Cards can have different background treatments (image, gradient, frosted glass, solid color)
- 23% higher click-through rate vs traditional feature lists
```

**Rules for bento in visual-first design:**
- At least half the cards must be image/visual-dominant, not text-dominant
- The largest card should contain the most important feature with the strongest visual
- No more than 6-8 cards visible at once — beyond that, it becomes a wall
- Mobile: collapse to single column, maintain visual hierarchy by card order

### Breaking Monotony

- Alternate between full-bleed and contained sections
- Mix static images with animated/video sections
- Use scale shifts — a massive hero followed by a quieter editorial section
- No two consecutive sections should have the same layout pattern
- Use bento grids for feature sections instead of repeating the same card layout

---

## 9. Page Rhythm & Visual Pacing

A full page needs dynamic pacing — not every section should hit the same visual intensity.

### The Intensity Curve

Think of the page like a film score:

```
Hero:         ████████████  (LOUD — full-bleed video/3D, maximum impact)
Features:     ██████        (Medium — editorial images, breathing room)
Deep dive:    ████████████  (LOUD — scroll-driven sequence, exploded view)
Social proof: ████          (Quiet — minimal visuals, testimonials, trust)
CTA:          ████████      (Rising — background visual, urgency)
Footer:       ██            (Whisper — clean, functional)
```

### Rules
- **Never stack two loud sections** — visual fatigue kills engagement. Follow a loud section with a quiet one
- **The hero sets the ceiling** — nothing later should be more visually intense than the hero
- **Quiet sections earn loud ones** — breathing room makes the next visual hit harder
- **End with rising energy** — the CTA should feel like a build, not a fade
- **3-act structure**: Hook (hero) → Story (features/deep dive, alternating intensity) → Close (CTA)

### Section Transitions
- Between loud → quiet: generous whitespace (150-200px gap), let the eye rest
- Between quiet → loud: tighter gap (80-100px), pull the user into the next visual
- Between same intensity: use a visual divider (gradient fade, color shift, subtle line)

---

## 10. Conversion & Persuasion

Creative-first design must convert, not just impress. Beauty without action is a screensaver.

### The 5-Second Rule

A visitor must understand **what this is and why they should care** within 5 seconds — from visuals alone, not from reading. If the hero visual doesn't communicate the product/brand instantly, it's art, not design.

### CTA Design

The CTA is the most important interactive element on the page. It must be:

- **Value-driven copy** — "Start Free Trial", "See Your Results", "Experience Aura" — not "Submit", "Learn More", "Click Here"
- **High contrast** from surrounding design — the CTA color should pop against the hero visual
- **Above the fold** — at least one CTA visible without scrolling
- **Repeated** — CTA appears in hero, after features, and at final CTA section (3 minimum per page)
- **Sized for confidence** — 48-56px height on desktop, full-width on mobile. Small buttons signal unimportance
- **Frosted glass or solid** — on dark visual backgrounds, use `backdrop-filter: blur` with border, or solid accent color. Never a ghost button that disappears into the visual

### Trust Signals

Trust signals make the visual story credible. Place them **near CTAs** and **after benefit claims**:

- **Customer logos** — recognizable brand logos in a row or ticker. Grayscale on dark backgrounds, color on light
- **Testimonials with photos** — real faces convert better than text-only quotes. Photo + name + title + quote
- **Numbers/stats** — "10,000+ users", "98% satisfaction", "4.9/5 rating". Use in the hero ticker or as large display numbers between sections
- **Social proof badges** — "Product of the Day", "4.8 on App Store", "Featured in [Publication]"

**Placement rule:** trust signals follow benefit claims in the visual rhythm. Claim → proof → CTA. Never front-load trust before the user knows what you do.

### Copy Rules for Visual-First Pages

Text is minimal but must be precise:

- **Clarity over cleverness** — if choosing between clear and creative, clear wins
- **Specificity over vagueness** — "Cut reporting from 4 hours to 15 minutes" not "Save time on workflow"
- **Benefits over features** — "Hear frequencies you've been missing" not "40mm beryllium drivers"
- **One idea per section** — each visual section advances ONE argument, not three
- **Headlines**: 6-10 words. The visual carries the emotion, the headline names it
- **Subheadlines**: 1-2 sentences expanding with specificity
- **Body**: 2-3 sentences max per section. If you need more, your visual isn't working

### Visual Psychology

Design decisions that affect conversion through perception:

| Principle | How to apply |
|-----------|-------------|
| **Anchoring** | The hero visual sets perception of everything below. Premium hero = premium product |
| **Contrast effect** | Before/after visuals, crossfade transitions between problem and solution states |
| **Peak-end rule** | Create one memorable visual peak (the showpiece) and a strong final impression (CTA section) |
| **Loss aversion** | Show what they'll miss without the product — visual absence, faded/dimmed states |
| **Goal gradient** | Progress indicators, step visualizations — people speed up near the finish |
| **Mere exposure** | Consistent visual language across all touchpoints builds preference |

---

## 11. Pattern Combinations

Not all patterns work together. Some amplify each other, some fight.

### Works Well Together
| Combination | Why |
|-------------|-----|
| Full-bleed video hero + scroll frame sequence below | Loud → loud works IF separated by a quiet section between |
| Editorial images + visual crossfade | Static beauty followed by smooth transitions — complementary |
| 3D hero + parallax layer swap | 3D establishes depth, parallax continues the spatial feeling |
| Mask reveal + visual story sequence | Dramatic reveal into storytelling — natural narrative flow |
| Video background + morphing visual | Motion above fold, interactive motion below — variation |

### Avoid Combining
| Combination | Why |
|-------------|-----|
| Two scroll-driven frame sequences | Massive asset weight, scroll fatigue, competing attention |
| Video scrubbing + frame sequence | Same mechanic twice — repetitive and doubles load time |
| Multiple 3D objects | Performance disaster, competing focal points |
| Clip-path reveal + morph back-to-back | Too many visual effects — feels like a demo, not a design |
| Full-bleed video + full-bleed video | Two autoplay videos = performance hell and visual noise |

### The One-Hero Rule
Every page gets **one primary visual showpiece**. Everything else supports it. If you have a scroll-driven exploded view, that's your hero moment — other sections use simpler patterns (editorial images, crossfades) to let the showpiece shine.

---

## 12. Advanced Visual Techniques

Beyond the core patterns, these techniques add depth, texture, and polish to visual-first sites.

### Shader Effects

Shaders are no longer expert-only. They add visual richness that's impossible with CSS alone.

**Common effects on award-winning sites:**
- Frosted glass / glass refraction (beyond CSS `backdrop-filter`)
- Iridescent color shifting (chroma chrome)
- Procedural noise animations
- Post-processing: bloom, chromatic aberration, film grain, lens distortion
- Heat distortion, glitch effects, kaleidoscopic warping

**Tools (from accessible to advanced):**
| Tool | Level | What it does |
|------|-------|-------------|
| Shaders.com | Beginner | Component library for React/Vue/Svelte — compose effects declaratively, visual editor exports production code |
| Three.js EffectComposer | Intermediate | Post-processing pipeline — bloom, DOF, SSAO, chromatic aberration |
| Custom GLSL/WGSL | Advanced | Full control — write vertex/fragment shaders. Three.js TSL lets you write once for WebGL + WebGPU |

**Rules:**
- Shaders are accent, not wallpaper — use on one section, not the entire page
- Performance: test on low-end devices. Shader complexity scales with GPU, not CPU
- Fallback: if WebGL/WebGPU unavailable, show a static CSS gradient or image
- `prefers-reduced-motion`: disable animated shaders, show a static frame

### Noise & Grain Textures

Subtle noise combats gradient banding, adds analog warmth, and creates depth. Underused on the web.

**The standard technique:**
```css
/* SVG feTurbulence noise as background layer */
.grain {
  position: relative;
}
.grain::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.04;
  mix-blend-mode: overlay;
  pointer-events: none;
  z-index: 1;
}
```

**When to use:**
- Over solid color backgrounds or gradients — eliminates banding
- On hero overlays — adds film-like texture
- On cards or surfaces — creates tactile depth
- **Not** over photographs — they already have texture

### View Transitions API

GPU-accelerated page/state transitions, native in the browser. No animation library needed.

**What it does:** When content changes (page navigation, state update), the browser captures before/after snapshots and animates between them.

**Use cases in creative-first sites:**
- Product gallery → detail page morph (image expands from grid to full-bleed)
- Section transitions on SPA navigation
- Filtered content re-arrangement (items morph to new positions)
- Dark/light mode transitions (whole page crossfades)

**Key features (2026):**
- `view-transition-name: match-element` — auto-names elements, no manual naming
- Nested transition groups — preserves DOM hierarchy for 3D/clip effects
- Cross-document transitions — works between actual page loads, not just SPA

**Browser support:** Chrome 111+, Safari 18+. Firefox 144+ (same-document only). Provide CSS fallback for unsupported browsers.

### Rive Animations

For interactive, stateful animations that respond to user input — Rive is the modern choice over Lottie.

**When to use Rive vs Lottie:**
| | Rive | Lottie |
|---|---|---|
| **Best for** | Interactive UI animations, state machines, data-bound visuals | Simple playback animations, loading spinners, decorative motion |
| **File size** | 10-15x smaller than equivalent Lottie | Larger JSON (compressed `.lottie` format helps) |
| **Interactivity** | Native state machines, hover/click/gesture triggers, data binding | Playback control (play, pause, seek). State machines added late 2025 |
| **Creation** | Own editor (rive.app) | After Effects + Bodymovin |
| **Decision** | Animation your product RELIES on | Animation you ADD to your product |

**Use in creative-first sites:**
- Interactive hero illustrations that respond to scroll/hover
- Animated icons that transition between states (menu → close, play → pause)
- Data-driven visualizations that update in real time
- Loading animations with progress state machines

### Sound Design (Optional)

Sound is niche but powerful for immersive creative experiences. Completely optional — most sites shouldn't use it.

**When sound adds value:**
- Portfolio/agency sites where immersion is the goal
- Product experiences (audio products, music, gaming)
- Campaign/storytelling sites with narrative
- **NOT** on SaaS landing pages, e-commerce, or information sites

**Rules if you use sound:**
- **Always opt-in** — browsers block autoplay audio. Provide a visible sound toggle
- **The more frequent the interaction, the quieter the sound** — button clicks should be near-silent, major transitions can be richer
- **Silence is intentional** — not every interaction needs sound
- **Tools**: Tone.js for synthesis/effects, Howler.js for simple playback
- **Performance**: preload audio files, use Web Audio API for low-latency playback
- **Accessibility**: sound must never be the sole indicator of state change. Always pair with visual feedback

---

## 13. Color & Theming

### Extracting the Palette

The visual asset defines the color palette, not the other way around.

1. **Extract** 3-5 dominant colors from the hero visual using:
   - [Coolors Image Picker](https://coolors.co/image-picker) — upload image, click to extract
   - [Adobe Color](https://color.adobe.com/create/image) — extract themes from uploaded images
   - Browser DevTools: screenshot the hero, use the eyedropper on key areas
   - Programmatic: `canvas.getContext('2d')` → sample pixels → cluster with k-means
2. **Build** the page palette: one dominant + one accent + neutrals
3. **Ensure** backgrounds match or complement the visual's background

If the visual has a white background → page sections should be white or very light.
If the visual is dark and moody → embrace dark UI around it.

Never force a pre-decided color palette onto a visual that clashes with it.

### Semantic Color Tokens

Never use raw hex values scattered through CSS. Map extracted colors to **semantic tokens** so the design stays maintainable and theme-aware (aligned with Apple HIG color system principles):

```css
:root {
  /* Extracted from hero visual */
  --color-accent: #00d4ff;
  --color-accent-2: #e84eff;

  /* Semantic tokens — use THESE in components, not the raw values above */
  --page-bg: #06060f;
  --surface: #0d0d1a;          /* cards, elevated containers */
  --label: #eef0f6;            /* primary text */
  --label-secondary: #8a8a9a;  /* supporting text, captions */
  --label-tertiary: #5a5a6a;   /* disabled, placeholder */
  --separator: rgba(255,255,255,0.08);  /* dividers, borders */
  --overlay: rgba(6,6,15,0.6); /* glassmorphism, frosted panels */
  --accent: var(--color-accent);        /* buttons, links, highlights */
  --accent-hover: var(--color-accent-2); /* hover states */
  --destructive: #ff453a;      /* delete, error states */
}
```

Benefits:
- Change the palette in one place when swapping visual assets
- Dark/light mode switching becomes token remapping, not a rewrite
- Components reference `var(--label)` not `#eef0f6` — self-documenting

### High Contrast Support

Some users enable increased contrast. Support `prefers-contrast: more`:

```css
@media (prefers-contrast: more) {
  :root {
    --label: #ffffff;
    --label-secondary: #cccccc;
    --separator: rgba(255,255,255,0.25);
    --overlay: rgba(0,0,0,0.85);
  }
  /* Increase text-shadow strength for text over visuals */
  .hero__title { text-shadow: 0 2px 8px rgba(0,0,0,0.9); }
}
```

### Dark / Light Mode

Visual-first sites work best as **single-theme experiences**. If the visual demands dark, go full dark. Don't force dual-theme support where the visuals only work in one mode.

If you must support both:
- **White-background assets** → work in light mode. For dark: generate a separate dark-background variant or add container with matched background
- **Dark-background assets** → work in dark mode. Same approach inverted
- **Transparent assets** (PNG, WebP with alpha) → work in both. Best option when feasible
- **Videos** → hardest to theme-switch. Use overlay tinting or generate separate edits
- Never use CSS `filter: invert()` on photos/videos — it looks terrible
- Use CSS custom properties for all overlay colors, gradients, and text colors so they switch cleanly
- Gradient masks must reference `var(--page-bg)`, not hardcoded colors
- If you can only generate one asset variant, **design for dark mode** — it's more forgiving and visually striking

### Theme-Specific Contrast Rules

**Dark mode:**
- Text: `#eef0f6` or lighter on dark backgrounds
- Muted text: no darker than `rgba(255,255,255,0.5)` — anything less is unreadable
- Glass/frosted panels: `backdrop-filter: blur(12px)` with `bg-opacity >= 0.6`
- Borders: `rgba(255,255,255,0.08)` minimum — invisible borders look broken

**Light mode:**
- Primary text: `#0F172A` (slate-900) or darker — not gray-400
- Muted text: `#475569` (slate-600) minimum — lighter grays fail contrast
- Glass cards: `bg-white/80` or higher opacity — `bg-white/10` is invisible in light mode
- Borders: `#e2e8f0` (slate-200) minimum — must be visible

---

## 14. Performance

Heavy visuals demand smart performance.

### Images
- WebP/AVIF format, responsive sizes via `srcset` and `<picture>`
- Lazy load everything below the fold
- Hero image: preload in `<head>`, set explicit `width`/`height`, provide low-res LQIP placeholder
- Generate at 2x for Retina (see Section 4)

### Videos
- Compress to <500KB for backgrounds: `ffmpeg -i input.mp4 -crf 28 -preset slow -vf scale=1920:-1 output.mp4`
- Set `poster` attribute for instant first frame
- `playsinline muted autoplay loop` for background videos
- Consider converting to frame sequence for scroll-driven sections

### 3D
- Compressed GLB (<5MB) via `gltf-transform optimize input.glb output.glb`
- Progressive loading with skeleton placeholder
- Fallback static image for low-power devices
- `loading="lazy"` on canvas container

### iOS / Safari Gotchas
- Video autoplay requires `playsinline` + `muted` — without both, Safari shows a play button
- Low-power mode and Data Saver can pause autoplay videos — always provide a `poster` fallback
- `video.currentTime` setting is laggy on iOS Safari — for scroll-driven video scrubbing, prefer frame sequences on mobile
- iOS momentum scrolling fires scroll events differently — use Lenis to normalize scroll input
- WebGL performance is lower on iOS — reduce 3D polygon count and texture size for mobile

### Loading States

Visual-first sites load heavy assets. Users must never stare at a blank screen. Follow Apple HIG loading hierarchy:

1. **Skeleton screens** (best) — show the page layout with gray placeholder shapes where visuals will load. The structure is visible instantly, assets fill in progressively
2. **LQIP (Low-Quality Image Placeholder)** — load a tiny blurred version of the image first (base64 inline or 1-2KB WebP), then swap to full resolution. The visual is "there" immediately, just blurry
3. **Progress indicator** — for frame sequences or 3D models that take multiple seconds, show a thin progress bar or percentage. Give the user a sense of "how long"
4. **Poster frame** — for videos, the `poster` attribute shows one frame instantly while the video loads
5. **Never a blank viewport** — if the hero takes 2+ seconds to load, the user should see *something* — a dark background with the text already visible at minimum

**Avoid:**
- Full-screen blocking spinners with no context
- "Loading..." text with no visual
- A flash of unstyled content followed by a layout shift when the image arrives

### Animation Performance Rules

These are non-negotiable for smooth 60fps:

- **Only animate `transform` and `opacity`** — these are compositor-friendly (GPU-accelerated). Never animate `width`, `height`, `top`, `left`, `margin`, `padding`, `box-shadow`, or `filter` continuously
- **Never `transition: all`** — list properties explicitly: `transition: transform 0.3s ease, opacity 0.3s ease`
- **Animations must be interruptible** — respond to user input mid-animation, don't lock out interaction
- **Set `transform-origin` explicitly** — defaults can cause unexpected behavior, especially on scale/rotate

### CSS Production Details

Small things that matter for polished visual-first sites:

- **`text-wrap: balance`** on headlines — prevents widows (single word on last line). Use `text-wrap: pretty` on body text
- **`font-variant-numeric: tabular-nums`** on ticker stats and number columns — digits align vertically
- **`touch-action: manipulation`** on interactive areas — removes 300ms double-tap zoom delay on mobile
- **`overscroll-behavior: contain`** on modals, drawers, and scroll-pinned sections — prevents background scroll
- **`env(safe-area-inset-*)`** on full-bleed layouts — handles iPhone notch and dynamic island. Critical for hero sections:
  ```css
  .hero { padding-top: env(safe-area-inset-top); }
  .hero__ticker { padding-bottom: env(safe-area-inset-bottom); }
  ```
- **`color-scheme: dark`** on `<html>` for dark-themed sites — fixes scrollbar and native input colors
- **`<meta name="theme-color" content="#06060f">`** — matches browser chrome to page background
- **Curly quotes** `"` `"` not straight `"` — and `…` not `...`
- **`cursor: pointer`** on all clickable elements — cards, buttons, links, interactive visuals. Missing cursor feedback makes things feel broken
- **`max-width: 65ch`** on body text containers — limits line length to 65-75 characters for readability. Headlines can be wider
- **z-index scale** — define a consistent scale, don't use random values:
  ```css
  :root {
    --z-base: 0;
    --z-above: 10;      /* elevated cards, sticky elements */
    --z-nav: 50;         /* fixed navigation */
    --z-overlay: 100;    /* modals, drawers */
    --z-cursor: 9999;    /* custom cursor, always on top */
  }
  ```
- **No emoji icons** — use SVG icons (Heroicons, Lucide, Phosphor). Emojis render differently per OS and look unprofessional in UI

### Bandwidth & Progressive Enhancement
- Detect `Save-Data` header or `navigator.connection.saveData` — serve static images instead of videos/3D
- Use `<link rel="preload" as="image" media="(min-width: 768px)">` — don't preload desktop assets on mobile
- Total page weight target: <3MB on initial load (defer non-visible assets)
- Use `IntersectionObserver` to load assets only when approaching viewport
- Preload critical hero asset in `<head>`, defer everything else
- Critical fonts: `<link rel="preload" as="font" crossorigin>` with `font-display: swap`

---

## 15. Accessibility

Visual-first does not mean accessibility-last. A beautiful site that excludes users is a failed site.

### Reduced Motion
- Wrap all animations, scroll effects, and video autoplay in `prefers-reduced-motion` checks
- When reduced motion is preferred:
  - Videos → show poster frame, add manual play button
  - Scroll-driven sequences → show the final/key frame statically
  - Crossfades/reveals → instant swap, no transition
  - Parallax → disable, use static positioning
  - 3D rotation → show a single static angle
- **Never skip reduced motion handling.** It's not optional

### Screen Readers
- Every visual section needs a descriptive `aria-label` or associated text that conveys the message the visual communicates
- Decorative visuals (ambience, background) → `aria-hidden="true"`, `role="presentation"`
- Meaningful visuals (product, storytelling) → descriptive `alt` text that captures what the visual *communicates*, not just what it shows
- Scroll-driven content must be accessible without scrolling — all text should exist in the DOM, not generated by JS

### Keyboard Navigation & Focus
- All interactive elements (CTAs, nav, links) must be focusable and operable via keyboard
- Custom cursors don't change this — focus indicators must be visible
- Use `:focus-visible` over `:focus` — avoids focus ring on mouse click, shows it on keyboard
- Never `outline: none` without a visible replacement (e.g., `focus-visible:ring-2`)
- Skip link to main content — especially important when the hero is a full-viewport video/animation
- Scroll-pinned sections must not trap keyboard users — ensure Tab moves past them
- Use `<button>` for actions, `<a>` for navigation — never `<div onClick>`
- Icon-only buttons need `aria-label`

### Color Contrast
- Text over visuals: 4.5:1 minimum for normal text, 3:1 for large text (WCAG AA)
- If the visual makes this impossible, add an overlay — don't compromise readability
- Test contrast with the actual visual behind it, not against a flat color
- Never rely on color alone to communicate information — pair with icons, labels, or patterns

### High Contrast Mode
- Support `prefers-contrast: more` — some users need stronger contrast than WCAG AA
- Increase text opacity to full white/black, strengthen separators, deepen overlays
- Gradient text (`-webkit-background-clip: text`) can be invisible in high contrast — provide a solid-color fallback
- Test: enable "Increase Contrast" in macOS/iOS accessibility settings and verify readability

### Fallbacks
- Every visual pattern needs a no-JavaScript fallback: static image, visible text, functional links
- If a video fails to load, the poster frame + text should still tell the story
- If WebGL/3D fails, a static render should appear

---

## 16. Anti-Patterns

**Instant failure — restart if you catch yourself doing any of these:**

### Layout Anti-Patterns
- Icon grids with text labels as a "features" section
- Stock photo in a small rectangle with text wrapping around it like a blog post
- Placeholder boxes with "Image goes here"
- Text-heavy sections with a decorative image off to the side
- Symmetrical card layouts where every card has an icon + title + description
- Using the same layout template for every section
- Generic gradient backgrounds instead of real visual assets
- Treating images as decoration rather than as the primary content

### Scroll & Animation Anti-Patterns
- Scroll hijacking that traps the user — they should always feel in control of scroll direction and speed
- Animations that fire faster than the user can read the content
- Multiple competing transitions in the same viewport — pick one per section
- Scroll-driven effects that break on trackpad vs mouse vs touch — test all input methods
- Long pinned sections with no visual progress indicator — users don't know how far to scroll
- Animations that replay every time the section enters viewport — play once, then hold

### Asset Anti-Patterns
- Using a visually stunning hero but falling back to icon+text for every section below
- Inconsistent asset quality — one section has a cinematic 4K image, the next has a blurry stock photo
- Assets with different lighting/color temperature on the same page — breaks visual cohesion
- AI-generated images with visible artifacts (weird hands, text gibberish, warped geometry) shipped without cleanup

### Code Anti-Patterns
- `transition: all` — list properties explicitly
- `outline: none` without a `:focus-visible` replacement
- `<div onClick>` instead of `<button>` or `<a>`
- Images without explicit `width`/`height` (causes CLS)
- Icon buttons without `aria-label`
- Animating `width`, `height`, `top`, `left` instead of `transform`
- Missing `prefers-reduced-motion` on any animation
- `user-scalable=no` or `maximum-scale=1` — never disable pinch zoom

---

## 17. Iteration Workflow

Creative-first design is not one-shot. The real quality comes from the **generate → build → review → fix** loop. A first pass will never be good enough.

### The Loop

```
1. Generate visual assets (AI tools)
2. Build the page around them (AI coding agent)
3. Screenshot the result
4. Identify what's wrong (text readability, visual placement, pacing, color)
5. Tell Claude exactly what to fix (with the screenshot)
6. Repeat 3-5 times per section
```

### How to Give Feedback That Works

Bad: "make it better" / "it looks off" / "more creative"

Good:
- "The text in the hero is unreadable — darken the overlay behind it but keep the center of the image visible"
- "The gradient mask is cutting off the headphones — extend the visible area down by 20%"
- "The hero feels static — add mouse parallax on the background"
- "This section looks like every other SaaS site — the image needs to dominate, shrink the text"
- "The transition between hero and the next section is jarring — add a gradient fade at the bottom"

### What to Check After Each Pass

1. **Squint test** — squint at the page. Can you still read the text? Can you still see the visual's focal point?
2. **Scroll speed test** — scroll at natural pace. Do animations feel smooth or jarring? Too fast? Too slow?
3. **Remove-text test** — mentally remove all text. Does the page still look intentional?
4. **Mobile check** — resize to 375px. Did the visual story survive or collapse to text+icon?
5. **Competitor test** — screenshot it, put it next to a competitor's site. Can you tell them apart instantly?

### When to Regenerate the Asset vs Fix the Code

**Regenerate the asset when:**
- The image composition doesn't leave room for text
- The lighting/colors clash with the rest of the page
- The subject isn't recognizable or looks "AI-ish" (artifacts, weird geometry)
- The background color doesn't match the page

**Fix the code when:**
- Text readability (overlay opacity, positioning, contrast)
- Visual placement (object-fit, object-position, sizing)
- Animation timing (too fast, too slow, wrong easing)
- Section transitions (gradient masks, spacing)

### Iteration Budget

Plan for:
- **Hero**: 3-5 iterations minimum (it's the most important section)
- **Scroll sections**: 2-3 iterations each
- **Editorial sections**: 1-2 iterations (simpler layouts)
- **Mobile adjustments**: 2-3 passes after desktop is done

---

## 18. Output Structure

When generating creative-first designs, deliver these in order:

### 1. Visual Asset Manifest
List every visual asset needed with: description, recommended tool + prompt, format, dimensions (at 2x for Retina), file size target, and which pattern it uses (Pattern 1-11).

### 2. Design Direction
- Mood/emotion (derived from the visual, not imposed)
- Color palette (extracted per Section 10)
- Font pairing (per Section 5)
- Theme (dark/light) with rationale
- Page rhythm plan (per Section 8)

### 3. Implementation
- Full working page or component code
- Scroll stack setup (GSAP + Lenis — see `references/snippets.md`)
- Asset integration with gradient masks, overlays, contrast treatments
- `prefers-reduced-motion` fallbacks for every animated pattern
- Mobile strategy: what changes on small screens (poster frames, static fallbacks, art-directed crops, tap instead of hover)

---

## 19. The Taste Test

Before finalizing, answer every question:

### Visual Quality
1. **Screenshot test**: Would someone stop scrolling to look at this?
2. **Remove-the-text test**: Does the page still communicate something with all text removed?
3. **Memory test**: Would someone remember this page 24 hours later?
4. **Template test**: Could this be confused with a template? If yes, restart
5. **Emotion test**: Does the visual make you feel something in 2 seconds?

### Technical Quality
6. **Speed test**: First meaningful paint under 2 seconds despite heavy assets?
7. **Scroll test**: All scroll animations smooth at 60fps? No jank?
8. **Mobile test**: Does mobile still tell the visual story, or did it fall back to text+icon?
9. **Accessibility test**: Screen reader, keyboard, reduced motion — all working?
10. **Input test**: Mouse, trackpad, touch, keyboard — all working?

If any answer is no → fix it before shipping.

### Pre-Delivery Checklist

Run through before handing off code:

**Visuals:**
- [ ] Hero uses custom AI-generated visual, not stock photo
- [ ] No icon grids or symmetrical card layouts
- [ ] No two consecutive sections use the same layout pattern
- [ ] All images have explicit `width`/`height`
- [ ] Images use WebP/AVIF, lazy loaded below fold, hero preloaded

**Interactions:**
- [ ] All clickable elements have `cursor: pointer`
- [ ] Hover states provide visual feedback (color, opacity, shadow — not scale shifts)
- [ ] Transitions list properties explicitly (no `transition: all`)
- [ ] Custom cursor disabled on touch devices

**Accessibility:**
- [ ] `prefers-reduced-motion` fallbacks on every animation
- [ ] `prefers-contrast: more` support on text over visuals
- [ ] All images have descriptive `alt` text
- [ ] Icon buttons have `aria-label`
- [ ] Skip link to main content
- [ ] Focus states visible (`:focus-visible`)
- [ ] Color is not the sole indicator of state

**Production:**
- [ ] `color-scheme: dark` set on `<html>` (if dark theme)
- [ ] `<meta name="theme-color">` matches page background
- [ ] `env(safe-area-inset-*)` on full-bleed hero
- [ ] z-index uses defined scale, no random values
- [ ] Body text max-width ~65ch
- [ ] No emoji icons (SVG only)
- [ ] Total initial page weight under 3MB
- [ ] Responsive at 375px, 768px, 1024px, 1440px

---

## When to Use

Use this skill when:
- Building landing pages, marketing sites, product pages, or portfolio sites
- The user has AI-generated images, videos, 3D renders, or plans to create them
- The user wants a design that stands out from typical text+icon layouts
- The brief emphasizes visual impact, emotion, or brand storytelling
- The request involves scroll-driven storytelling or immersive visual experiences
- The request mentions anything related to editorial, cinematic, or premium design

Do not use this skill for:
- Admin dashboards, data-heavy interfaces, or internal tools
- Documentation sites or text-primary content
- E-commerce product listing grids or form-heavy applications
- Quick prototypes where visual polish isn't the goal
