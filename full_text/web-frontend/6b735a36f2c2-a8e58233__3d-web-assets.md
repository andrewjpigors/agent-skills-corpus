---
name: 3d-web-assets
description: End-to-end pipeline for turning Blender output into shippable assets for digital online experiences — landing pages, web apps, marketing sites, social posts, email, OG cards, app icons, and optional runtime 3D scenes via React Three Fiber. Owns surface targeting (aspect ratios, retina/responsive variants, transparent backgrounds), output-format selection (AVIF, WebP, MP4/AV1, WebM, Lottie vs video decision, glTF/GLB for runtime), compression pipelines (avifenc, cwebp, ffmpeg, gltf-transform with Meshopt and KTX2), color management to sRGB (with Display-P3 progressive enhancement), and Core Web Vitals / accessibility gates (LCP, INP, prefers-reduced-motion). Use when the user mentions web asset, hero image, landing page, OG image, Open Graph, social card, app icon, favicon, PWA icon, email header, marketing render, product mockup, glTF, GLB, three.js, Three.js, R3F, React Three Fiber, Drei, runtime 3D, interactive 3D, AVIF, WebP, Lottie, microinteraction, 3D icon set, glassmorphism asset, depth in UI, or asks "how do I get this Blender render onto the website / into the app / into the brand kit."
---

# 3D Web Assets — Blender to Shippable Web/Digital Output

End-to-end pipeline that takes a correctly authored Blender scene and turns it into the actual files that ship inside browsers, native apps, marketing pages, social platforms, and email. Three phases, three non-negotiable quality gates. The most common failure mode is producing a beautiful render that is unusable in production — wrong color space, no transparency, no retina variant, no fallback for `prefers-reduced-motion`, no perf budget for mobile, or a runtime glTF that ships uncompressed and tanks LCP.

This skill is the **delivery leg** of the 3D pipeline. It owns *what file type, what size, what compression, what fallback, what surface*. It does NOT own modeling, materials, or lighting — those route to their respective specialist skills.

Source spine: web-delivery research bundle (May 2026). Shared defaults: `~/.claude/skills/3d-blender/foundations.md`.

---

## When to use

- The user wants a Blender render placed on a website, in a web app, in a marketing email, in a social post, or as an app/PWA icon.
- The user asks for an OG image, Twitter card, hero illustration, product mockup for a landing page, sculpted-looking icon set, or branded 3D scene.
- The user wants the user to be able to rotate / interact with a 3D object in the browser (runtime glTF + Three.js / React Three Fiber).
- Output-format decisions: AVIF vs WebP vs PNG, MP4 vs WebM vs Lottie vs animated WebP, glTF/GLB vs pre-rendered video.
- Compression / optimization passes: gltf-transform with Meshopt and KTX2, avifenc tuning, ffmpeg recipes for web video, building `<picture>` srcset cascades.
- Performance budget enforcement: hero LCP, INP under 200ms, page-weight gates.
- Accessibility for visual assets: alt text strategy, `prefers-reduced-motion` fallbacks, keyboard alternatives for interactive 3D.

## When NOT to use

- Material authoring (Principled BSDF, texture maps, baking) → `3d-material`.
- Lighting / render engine configuration / fireflies / passes → `3d-lighting-render`.
- Geometry / topology / UVs → relevant modeling skill (`3d-character`, `3d-hard-surface`, `3d-environment`).
- Pure design intent before any modeling exists → `3d-design-brief`.
- Programmatic batch rendering or headless farm work → `3d-automation` (which wraps this skill's output-side bpy and the CLI tooling below).
- Native app icon production for iOS App Store / Play Store submission — Blender produces the master, but Xcode/Android Studio own the actual asset catalog format. This skill produces the 1024×1024 master PNG; platform-tool handoff is out of scope.

## Prerequisites

- `foundations.md` (universal rules, color-space table, render defaults) is in force.
- Scene is **already correctly lit and shaded** under AgX — render settings cannot fix delivery problems, and delivery settings cannot fix render problems. If output looks wrong before encoding, audit upstream (`3d-material`, `3d-lighting-render`) first.
- Real-world scale + applied transforms (Universal Rule 2). Crops and aspect-ratio composition rely on physical units.
- Multilayer EXR master archived before any web-format encoding. **Never encode a deliverable from an 8-bit PNG that came directly out of Blender's image output** — encode from the EXR through AgX to a 16-bit intermediate, then to AVIF/WebP. Encoding from clipped 8-bit loses highlights and banding becomes permanent.

---

## Pipeline overview

```
Phase 1: Asset Spec               →  QG1: surface + dimensions + format + budget + a11y locked
Phase 2: Author for Delivery      →  QG2: render output correct at target size; alpha right; color space right
Phase 3: Optimize & Deliver       →  QG3: budget met; LCP/INP gates clear; reduced-motion fallback exists
```

Three phases, three quality gates. Do not advance past a failed gate. The cost of re-rendering after discovering a wrong aspect ratio is one full Cycles render. The cost of discovering missing alpha after encoding to AVIF is one full re-render plus re-encode.

---

## Phase 1 — Asset Spec

Goal: lock the deliverable specification before any modeling or render decisions are touched. Specs answer six questions.

### The six questions (must all be answered before Phase 2)

| # | Question | Why it matters |
|---|---|---|
| 1 | **Where will this live?** | Landing hero, pricing card, OG/social card, app icon, favicon, email header, blog inline, social feed post, runtime canvas. Each has standard sizes and platform constraints. |
| 2 | **What is the surface dimension and aspect?** | 1920×1080 (16:9) hero, 1200×630 (1.91:1) OG, 1080×1080 (1:1) social, 1024×1024 PNG app icon master, 600px-wide email header. See `surface-targets.md`. |
| 3 | **Static, animated, or interactive?** | Static → AVIF + WebP fallback. Looping animation → WebM/AV1 + MP4/H.264 fallback. Interactive → glTF/GLB via Three.js/R3F. Lottie only if the motion is vector-authorable (no true 3D camera moves, no shaders). |
| 4 | **Transparent background?** | If yes, the render must use a film/transparent setting (`bpy.context.scene.render.film_transparent = True`) and the output format must support alpha (PNG, WebP, AVIF, WebM/VP9, animated WebP — NOT MP4/H.264 / Lottie alpha is limited / JPEG never). |
| 5 | **Performance budget?** | Default budgets in `surface-targets.md`. Hero AVIF target 80–180 KB; initial GLB <2 MB; total page weight <1.5 MB; hero LCP <2.5 s on a Moto G Power profile. |
| 6 | **Accessibility?** | Alt text for static. `prefers-reduced-motion` fallback (poster image, paused first frame, or static AVIF) for animated. `aria-label` + keyboard alternative for interactive 3D. WCAG 2.2 Level A applies. |

### Surface-target standards (May 2026)

| Surface | Native dim | @2x | Format | Notes |
|---|---|---|---|---|
| Landing hero | 1920×1080 | 3840×2160 | AVIF + WebP fallback | Author at 4K, downscale. Critical content in 1080×500 safe zone for hero-with-text overlays. |
| OG / social preview | 1200×630 | n/a | PNG → AVIF cascade | 1.91:1. Safe zone 1080×565. Strip ICC profile for social uploads. |
| Social feed (square) | 1080×1080 | n/a | AVIF/WebP/PNG | 1:1. Instagram/LinkedIn/X feed. |
| Social feed (portrait) | 1080×1350 | n/a | AVIF/WebP/PNG | 4:5. Instagram feed (preferred). |
| Stories / Reels / Shorts | 1080×1920 | n/a | MP4 or AVIF | 9:16 vertical. |
| App icon (iOS master) | 1024×1024 | n/a | PNG (8-bit, no alpha) | Master. Platform tooling generates derivatives. |
| App icon (Android adaptive) | 432×432 foreground / 512×512 PNG | n/a | PNG (with alpha for foreground) | Foreground in 264×264 safe zone (88px padding each side). |
| Favicon | SVG + 32 / 180 / 192 / 512 PNG | n/a | SVG primary, PNG fallback | PWA `maskable` 512×512 needs 80% safe zone. |
| Email header | 1200×400 source | n/a | PNG / JPEG | Render at 2× (1200px), display at 600px. Inline-able size <200 KB. Avoid AVIF/WebP (Outlook). |
| Blog inline / card | 1600×900 | 3200×1800 | AVIF + WebP fallback | 16:9. |
| Runtime 3D canvas | n/a | n/a | GLB | <2 MB initial, KTX2 textures, Meshopt geometry. |

Detailed per-surface sheets with safe zones, font-size implications, and platform recompression quirks: `surface-targets.md`.

### Quality Gate 1

- Surface chosen and verified against the table.
- Dimension + aspect locked in `bpy.context.scene.render.resolution_{x,y}`.
- Static/animated/interactive decision made and the output format(s) listed.
- Alpha requirement marked (Yes/No) and `render.film_transparent` set accordingly.
- Performance budget written down (target KB for static, target initial GLB for interactive).
- Accessibility plan written: alt text drafted, reduced-motion fallback identified, interactive 3D has keyboard alt.

If any of these is missing or vague, the spec is incomplete. Do not start authoring.

---

## Phase 2 — Author for Delivery

Goal: produce a render whose composition, color, and transparency are correct *at the target output size*. This is not the same as a render that looks good in the Blender viewport.

### Composition for crop tolerance

Web layouts reshape containers across breakpoints. A hero that's a tight 16:9 in Figma will be a 21:9 letterbox on ultrawide and a 4:3 squash on tablet portrait. Three rules:

1. **Author wider than you need; crop down in CSS.** Render at 16:9, but compose the subject inside the **inner 4:3** of the frame. Outer wings become breathing room for crop variation.
2. **Keep the subject off-center on the "anchor side."** For OG cards with overlaid text on the left, render the subject on the right 60% of the frame. Most landing-hero text overlays go top-left; counter-position the subject bottom-right.
3. **Avoid critical detail near edges.** Platform recompression chews edge pixels first; safe zones are tighter than they look.

### Camera, lens, and DoF for web

- **Lens choice:** 50–85 mm equivalent for product/hero shots — flatter perspective reads as "premium product photography." Wide angles (24–35 mm) read as "real estate" or "automotive marketing"; use intentionally.
- **DoF:** Subtle is better. Web compression flattens bokeh anyway; aggressive shallow DoF turns into smear. Cycles f/4–f/8 typically translates well after AVIF encode.
- **Orthographic** for icon-style assets (3D icon sets, isometric illustrations). Removes perspective drift across the icon family so all icons read at the same visual weight.

### Transparency and the alpha channel

For UI compositing onto arbitrary backgrounds, the asset must have a clean alpha matte:

```python
scn = bpy.context.scene
scn.render.film_transparent = True                    # transparent film
scn.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
scn.render.image_settings.color_mode = 'RGBA'
scn.render.image_settings.color_depth = '32'
```

For the export pass that becomes the deliverable:

```python
# 16-bit PNG intermediate (preserves AgX → sRGB tone-map, no banding)
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_mode = 'RGBA'
scn.render.image_settings.color_depth = '16'
```

Alpha gotcha: glossy reflections and emissive materials need transparent-film-aware setup. If reflections show the world environment, the alpha matte will be inconsistent. Either bake a clean matte via Cryptomatte and re-composite, or render with the environment muted and accept that the asset must sit on a similar backdrop.

### Color management → sRGB delivery

The pipeline:

1. **Render in linear / scene-referred.** AgX as the View Transform (foundations §6).
2. **Output a multilayer EXR master.** This is the archival source.
3. **Tone-map to 16-bit PNG through AgX.** Blender's image-save writes the View Transform; verify Render Properties → Color Management → View Transform = AgX before saving the PNG.
4. **Encode AVIF/WebP from the 16-bit PNG**, not from Blender's direct 8-bit PNG output. The 16-bit intermediate preserves the AgX rolloff so encoder quantization doesn't introduce banding in skies, gradients, and shadow ramps.

For Display-P3 wide-gamut delivery (recommended for hero assets, optional elsewhere):

- Render and tone-map as above.
- Pass `--cicp 1/13/6` to `avifenc` for Display-P3 (BT.709 primaries with sRGB transfer is the safe default; full P3 needs `--cicp 12/13/6`).
- Non-P3 browsers gamut-map to sRGB automatically when an ICC/CICP tag is present.
- **Strip the profile** when uploading to social platforms (X, Instagram, LinkedIn recompress and routinely break embedded profiles).

Full color-space recipe: `format-cascade.md` §Color.

### Lighting and material decisions sized for web

Two adjustments to a "perfect render" for web-sized output:

- **Slightly raise the key light separation.** Browser compression flattens midtones. A 2 EV key/shadow separation that looks great at full resolution often reads muddy at 480 px wide. Push to ~2.5 EV for hero assets that will be viewed at thumbnail size somewhere in the funnel.
- **Boost roughness contrast in materials.** Subtle micro-roughness variation gets killed by lossy encoding. A material that reads as "weathered brass" in 4K may read as "uniform plastic" after AVIF encode at thumbnail size. Push the contrast on roughness/metallic masks.

These are tuning notes — the authoritative material work happens in `3d-material`. This skill flags the deltas; the specialist skill applies them.

### Quality Gate 2

- Render at exact target resolution (no "I'll downscale later" — encode artifacts compound).
- Color Management View Transform = AgX, output through the 16-bit PNG intermediate.
- Alpha matte clean (if transparent background was specified). Spot-check edge pixels for halos.
- Composition holds at the planned breakpoint crops — pull the render into a Figma frame at hero / tablet / mobile dimensions and visually verify the subject is not amputated.
- Lookdev pass at 50%, 100%, and 25% display size. If it reads at 25% (typical thumbnail / card use), it will read at all sizes. If it falls apart at 25%, the composition or lighting is too subtle.

---

## Phase 3 — Optimize & Deliver

Goal: produce the final files that ship, in the right formats, within budget, with fallbacks and accessibility wired up.

### Format cascade — pick winners (May 2026)

**Static images:**

| Use case | Primary | Fallback | Master |
|---|---|---|---|
| Landing hero, product card, blog inline | AVIF (q 60–75) | WebP (q 80) | 16-bit PNG |
| Photoreal with subtle gradient | AVIF (q 70–80) | WebP (q 85) | 16-bit PNG |
| UI screenshot, icon, asset needing pixel-perfect text/edges | PNG lossless | — | PNG |
| App icon (iOS master) | PNG 8-bit, no alpha | — | PNG |
| Email header (Outlook-safe) | JPEG q 85 or PNG | — | PNG |
| Social platform upload (X, IG, LinkedIn) | JPEG q 90 or PNG, **profile stripped** | — | PNG |

Skip JPEG XL — Chrome removed the decoder in 2022 and it has not returned in mainline. JPEG remains the universal lowest common denominator; AVIF is now ~95% supported and is the default modern choice. WebP at ~96% is the safe fallback.

**Looping animation / video:**

| Use case | Primary | Fallback |
|---|---|---|
| 3-second hero loop (no alpha) | WebM/AV1 (`libsvtav1 -crf 30`) | MP4/H.264 (`libx264 -crf 22`) |
| 3-second hero loop with alpha | WebM/VP9 + alpha | HEVC alpha (Safari) or animated WebP |
| 10-second product reveal | WebM/AV1 + MP4/H.264, plus AVIF poster | — |
| UI microinteraction (vector-authorable) | Lottie / dotLottie | — |
| UI microinteraction (true 3D, raster, <500 KB) | APNG or animated WebP | — |

**Lottie ceiling:** Lottie cannot render perspective-correct 3D, shader effects, true lights, or volumetrics. If the motion involves any of those, pre-render to video. Rive 2 covers 2.5D rigged interactivity in between.

**Runtime interactive 3D:**

| Use case | Format | Compression |
|---|---|---|
| Hero canvas, product configurator, interactive scene | glTF 2.0 GLB | Meshopt geometry + KTX2/Basis textures |
| Cold-cache one-shot load (single page visit) | glTF 2.0 GLB | Draco geometry (slightly smaller, slower decode) |

Encoder/recipe details in `format-cascade.md` and `optimization-recipes.md`.

### The retina conversation

`@1x / @2x / @3x` is **dead for web** in 2026. Ship intrinsic sizing via `srcset` + `sizes` + AVIF and let the browser pick.

```html
<picture>
  <source
    type="image/avif"
    srcset="hero-800.avif 800w, hero-1600.avif 1600w, hero-2400.avif 2400w, hero-3840.avif 3840w"
    sizes="(min-width: 1280px) 1280px, 100vw">
  <source
    type="image/webp"
    srcset="hero-800.webp 800w, hero-1600.webp 1600w, hero-2400.webp 2400w"
    sizes="(min-width: 1280px) 1280px, 100vw">
  <img
    src="hero-1600.jpg"
    alt="Sculpted brass coin on a matte black surface, lit by a single overhead area light"
    width="1600" height="900"
    loading="eager" fetchpriority="high">
</picture>
```

Three-variant `srcset` (e.g., 800 / 1600 / 2400) covers ~95% of viewports without bloating the manifest. Add a 3840w only when ultrawide users are a meaningful audience.

**Where @2x/@3x is still required:** native iOS/Android asset catalogs (Xcode, Android Studio) and HTML email (Outlook and most clients lack reliable `srcset` support — ship a 2× PNG at half its native display size and let the client downscale).

### Compression recipes (canonical commands)

**AVIF encoding from 16-bit PNG:**

```sh
# Hero quality (q ≈ 70, ~120 KB for 1920×1080)
avifenc --speed 4 --min 20 --max 30 --depth 10 hero-1920.png hero-1920.avif

# Aggressive (smaller, for thumbnails / cards)
avifenc --speed 4 --min 30 --max 45 --depth 8 card-512.png card-512.avif

# Display-P3 wide gamut (hero)
avifenc --cicp 12/13/6 --speed 4 --min 20 --max 30 --depth 10 hero-p3.png hero-p3.avif
```

**WebP fallback:**

```sh
cwebp -q 80 -m 6 hero-1920.png -o hero-1920.webp
cwebp -q 85 -m 6 card-512.png -o card-512.webp
```

**Looping animation from a Blender PNG sequence:**

```sh
# AV1 (modern, smaller; Safari needs M3+/A17+ for hardware decode but falls back)
ffmpeg -framerate 60 -i frame_%04d.png \
  -c:v libsvtav1 -preset 6 -crf 30 -pix_fmt yuv420p \
  hero-loop.webm

# H.264 fallback (universal)
ffmpeg -framerate 60 -i frame_%04d.png \
  -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p \
  -movflags +faststart hero-loop.mp4

# Constrain height to 1080 if rendering came in larger
ffmpeg -framerate 60 -i frame_%04d.png -vf "scale=-2:1080" \
  -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p \
  -movflags +faststart hero-loop-1080.mp4
```

**glTF/GLB optimization:**

```sh
# Single command — Meshopt + KTX2 + simplify + weld + prune + instance
gltf-transform optimize input.glb output.glb \
  --texture-compress ktx2 \
  --compress meshopt \
  --simplify \
  --weld \
  --prune \
  --instance

# Inspect before/after
gltf-transform inspect output.glb
```

Full per-format recipe library: `optimization-recipes.md`.

### Runtime 3D handoff (when interactive is required)

If the spec says "the user must rotate / scrub / interact with the 3D object," the deliverable is a GLB, not a video. The integration target is almost always React Three Fiber (R3F) for React-based codebases.

Two non-negotiables for R3F integration:

1. **Explicit color space on every texture.** R3F v9+ removed the automatic sRGB conversion that older code relied on. Albedo textures must be tagged `THREE.SRGBColorSpace`; normal / roughness / metallic / data textures must be `THREE.NoColorSpace`. A wrong tag here is the runtime-3D equivalent of the static-image "Normal map color space wrong" failure.
2. **`renderer.toneMapping = THREE.AgXToneMapping`** + `renderer.outputColorSpace = THREE.SRGBColorSpace`. This mirrors the Blender authoring view transform; without it the runtime render diverges from the Blender lookdev.

Full handoff patterns (R3F + Drei boilerplate, GLB loading with Meshopt decoder worker, perf-budget gates, prefers-reduced-motion handling, accessibility wrapper): `runtime-3d-handoff.md`.

### Accessibility — non-negotiable for every deliverable

- **Static images:** meaningful `alt` text (describes the subject and intent, not "image of"). Decorative-only assets get `alt=""`.
- **Animated assets:** every `<video autoplay loop>` must have a `prefers-reduced-motion: reduce` fallback that pauses at the poster frame or swaps to the AVIF poster. Hard requirement.
- **Lottie:** check `matchMedia('(prefers-reduced-motion: reduce)').matches` and pause at frame 0 or load the static SVG.
- **Interactive 3D:** `aria-label` describing the scene, keyboard alternatives for any drag/orbit interaction, and a static AVIF poster as the `<noscript>` and reduced-motion fallback. WCAG 2.2 treats inaccessible interactive 3D as a Level A failure.

### Performance budgets — defaults and how to enforce

| Asset class | Budget |
|---|---|
| Hero AVIF (1920×1080) | <200 KB |
| Card / inline AVIF (512×512) | <40 KB |
| Looping video (3 s, AV1) | <800 KB |
| Initial GLB (runtime 3D hero) | <2 MB |
| Total page weight | <1.5 MB |
| LCP (Moto G Power profile) | <2.5 s |
| INP | <200 ms |

Wire a Lighthouse CI step into the deployment pipeline that fails the build when any of these thresholds is breached. Performance budgets without an automated gate are aspirational.

### Quality Gate 3

- All target formats produced (AVIF + WebP + JPEG fallback for static; AV1 + H.264 for video; optimized GLB for interactive).
- File sizes within the per-class budget table.
- `<picture>` srcset cascade or `<video>` dual-source written.
- `prefers-reduced-motion` fallback exists for any animated/interactive asset.
- Alt text / `aria-label` written.
- Lighthouse CI gate passes locally (LCP, INP, page weight).
- For runtime 3D: explicit color-space tagging on every texture verified; AgX tone mapping enabled in the renderer.

---

## Common failures (symptom → fix)

| Symptom | Root cause | Fix |
|---|---|---|
| Hero AVIF has visible banding in skies / gradients | Encoded from 8-bit PNG; quantization compounded | Re-encode from 16-bit PNG intermediate; raise `--depth 10` in `avifenc` |
| Transparent PNG has white halo / dark fringe on edges | Render lacked `film_transparent`, or env reflections baked into alpha | Set `bpy.context.scene.render.film_transparent = True`; if reflections are in alpha, re-render with environment muted or composite via Cryptomatte |
| Subject is cut off at mobile / tablet breakpoint | Composed for full hero aspect; ignored crop tolerance | Re-frame: subject inside inner 4:3 of the 16:9 canvas, off-center on the anchor side |
| Render reads as muddy / flat at thumbnail size | Lighting separation too soft for downstream compression | Push key/shadow separation ~2.5 EV; boost roughness mask contrast |
| OG card looks wrong on LinkedIn / X but fine on the site | Embedded ICC profile mishandled by platform recompression | Strip color profile from social uploads; keep profile on self-hosted delivery |
| Runtime glTF appears washed-out / desaturated in browser vs Blender | Renderer using LinearToneMapping or NoToneMapping; albedo textures tagged NoColorSpace | `renderer.toneMapping = THREE.AgXToneMapping`; albedo textures `colorSpace = SRGBColorSpace`; data textures `NoColorSpace` |
| GLB >5 MB despite simple scene | No KTX2 texture compression; no Meshopt; embedded duplicate materials | `gltf-transform optimize --texture-compress ktx2 --compress meshopt --prune --instance` |
| Animated hero plays jankily on mobile | 60 fps video on a device that can't keep up; or autoplay with no `playsinline` / `muted` | Cap to 30 fps for mobile-first; ensure `<video muted playsinline autoplay loop>`; provide `prefers-reduced-motion` poster |
| Lottie animation looks wrong / missing 3D depth | Asked Lottie to render true 3D; it can't | Pre-render to video (WebM/AV1 + MP4 fallback); use Lottie only for vector-authorable motion |
| Email header doesn't render in Outlook | Used AVIF or WebP; Outlook lacks support | Ship PNG/JPEG for email regardless of how good AVIF is on the website |
| Page LCP regressed after adding hero | Hero not preloaded; lazy-loaded above the fold; or WebGL canvas became the LCP element | `<link rel="preload" as="image" fetchpriority="high" imagesrcset="...">`; for 3D hero, AVIF poster is the LCP element, canvas hydrates after |
| Site fails accessibility audit on the new hero | No alt text, or animated hero has no reduced-motion fallback | Add meaningful `alt`; gate animation behind `prefers-reduced-motion: no-preference` |
| App icon shows white square corners in some contexts | Padding inside the 1024×1024 master not respecting platform safe zones | iOS: full bleed, system rounds corners. Android adaptive: foreground inside 264×264 safe zone of 432×432 canvas. PWA maskable: content inside 80% safe zone of 512×512. |
| R3F canvas hangs in Suspense; never resolves on slow / offline network | `<Environment preset="...">` is a CDN fetch; stalls behind proxies and in local dev | Use procedural `<Environment>` + `<Lightformer>` children -- see `runtime-3d-handoff.md` "Offline / fast-load environment" |
| Blender card/panel model loads lying flat instead of upright in R3F | Blender Z-up to glTF Y-up swap; flat objects standing in Blender end up face-up in the GLB | `rotation={[Math.PI/2 - tilt, 0, skew]}` on the outer R3F group -- see `runtime-3d-handoff.md` "Y-up rotation correction" |
| Child parts of model ignore parent rotation; pose only partially applied | Blender exporter flattens hierarchy for identity-transform children; parent rotation bakes into sibling nodes | `scene.traverse` to zero all node rotations on load; one outer group controls the pose -- see `runtime-3d-handoff.md` "Hierarchy flatten fix" |
| Metallic surfaces render as black or near-black under procedural lighting | Metals have no diffuse; sparse procedural env provides too few reflection surfaces | Lift material roughness to 0.18-0.25; set `envMapIntensity` 1.5-1.8x at runtime -- see `runtime-3d-handoff.md` "Metallic material tuning" |
| Floating 3D model is clipped at the container edge despite `alpha: true` | Container element has a background that overrides canvas transparency | Set canvas container to `background: transparent`; span full layout area -- see `runtime-3d-handoff.md` "Canvas alpha + container transparency" |

---

## Execution modes

### Playbook mode (default)

Produce step-by-step instructions a human follows in Blender + a separate shell session for encoding. Three blocks:

1. Blender output settings (resolution, film_transparent, view transform, file format, color depth).
2. Render and save the EXR + 16-bit PNG intermediate.
3. Shell commands for AVIF / WebP / video / glTF optimization (the recipes above).

Default to Playbook mode when no live Blender instance is detected.

### MCP mode (live Blender via MCP server)

Detection: try `mcp__blender__get_scene_info`. If it returns a scene, MCP mode is available.

**Tools used by this skill:**

- `mcp__blender__get_scene_info` — detect MCP availability; inspect current resolution / output settings.
- `mcp__blender__execute_blender_code` — set output configuration; run the render; save the EXR + 16-bit PNG.
- `mcp__blender__get_viewport_screenshot` — sanity-check the composition at the target aspect before committing to a full render.

**Canonical output-side bpy snippet:**

```python
import bpy
scn = bpy.context.scene

# 1. Resolution + aspect
scn.render.resolution_x = 1920
scn.render.resolution_y = 1080
scn.render.resolution_percentage = 100

# 2. Color management
scn.view_settings.view_transform = 'AgX'      # foundations §6

# 3. Transparent film (set Yes only if the spec requires alpha)
scn.render.film_transparent = True

# 4. Master output — multilayer EXR (archive)
scn.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
scn.render.image_settings.color_mode = 'RGBA'
scn.render.image_settings.color_depth = '32'
scn.render.image_settings.exr_codec = 'ZIP'
scn.render.filepath = '//renders/hero_master_####'
bpy.ops.render.render(write_still=True)

# 5. Deliverable intermediate — 16-bit PNG, AgX baked in
scn.render.image_settings.file_format = 'PNG'
scn.render.image_settings.color_mode = 'RGBA'
scn.render.image_settings.color_depth = '16'
scn.render.image_settings.compression = 15
scn.render.filepath = '//deliverables/hero_1920x1080_####'
bpy.ops.render.render(write_still=True)
```

**Encoding step lives outside Blender.** The MCP execute_blender_code path does NOT run shell commands or call `subprocess` (blocked by the safety hook). After Blender writes the PNG intermediate, switch to Claude Code's Bash tool to invoke `avifenc`, `cwebp`, `ffmpeg`, `gltf-transform`. See `foundations.md` §11.1 for the full list of patterns blocked inside MCP execute calls.

For scripted batch (a hundred OG variants, a brand kit, a per-product mockup library) defer to `3d-automation` — it wraps these patterns in robust drivers.

---

## Cross-discipline boundaries

- **Lighting and materials must be right first.** A wrong View Transform or normal-map color space is not solvable in AVIF compression. If output looks wrong before encoding, audit upstream.
- **Geometry / UVs do not change here.** This skill's "Phase 2 adjustments" (key separation, roughness contrast) are tuning notes for the lighting and material specialists, not edits to mesh topology.
- **Animation curves / timing** are out of scope. This skill renders and packages animation; it does not author it.
- **Scripted batch generation** → `3d-automation`. Pattern: this skill's bpy + this skill's CLI recipes, wrapped in a Python driver with error recovery and a manifest writer.
- **Brand styling decisions** (palette, type, voice) are upstream of this skill — usually handled by a brand or design skill or a design brief. This skill receives the brand intent as a constraint.

---

## Source pointers

- Web-delivery research (May 2026): formats, browser support, encoders, R3F state, perf budgets.
- Khronos glTF 2.0 Asset Creation Guidelines 2.0 (SIGGRAPH 2025).
- Shared defaults: `~/.claude/skills/3d-blender/foundations.md` §4 (color spaces), §6 (lighting/render defaults), §11.1 (MCP safety hook).
- Theory cross-cuts: `~/.claude/3d-modeling/3d_foundational_theory.agent.final.md` §8 (lighting/render — this skill's upstream), §12.3 (rendering rules), §13.4 (rendering failures).

Supporting files in this skill directory:

- `surface-targets.md` — per-surface spec sheets with safe zones, platform recompression quirks, font-size implications.
- `format-cascade.md` — full format decision matrix, encoder recipes with all parameters, color-management deep dive.
- `optimization-recipes.md` — canonical `avifenc`, `cwebp`, `ffmpeg`, `gltf-transform` invocations with parameter notes and benchmark targets.
- `runtime-3d-handoff.md` — R3F + Drei integration patterns, color-space tagging, Meshopt worker decoder, perf budgets, prefers-reduced-motion handling, accessibility wrappers.
