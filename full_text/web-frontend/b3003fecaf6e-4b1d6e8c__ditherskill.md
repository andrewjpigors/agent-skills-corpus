---
name: ditherskill
description: >
  Dither images and generate dithered interactive UI components (charts, buttons, sliders,
  toggles, meters, dashboards). Classic + modern algorithms (Floyd-Steinberg, Atkinson, Bayer,
  blue-noise, hybrid, Riemersma). Use when the user wants 1-bit/print/pixel/retro dither effects;
  multi-color palettes; procedural UI mockups that look dithered; animated component frames;
  CLI/HTTP agent tooling; or the DitherStudio web app. Local-only processing.
metadata:
  tags:
    - dither
    - image-processing
    - ui-generation
    - charts
    - pixel-art
    - floyd-steinberg
    - bayer
    - cli
    - agent-tools
---

# DitherSkill

Dither photos **and** generate procedural UI (charts, buttons, sliders, toggles, meters) that can be animated and dithered live.

**Website / examples:** https://ditherskill.ideatr.dev  
**Studio:** https://ditherstudio.ideatr.dev  
**Install:** `npx skills add arjunkshah/ditherskill -g -y`

## When to use

- Dither any image (1-bit, ordered, error diffusion, multi-color)
- Generate **dithered UI mockups**: bar/line/pie charts, buttons, sliders, switches, progress, knobs, meters, cards, dashboards, waveforms
- Animate component frames for motion dither previews
- Agent CLI/HTTP pipelines for deterministic exports

## Studio tabs

1. **Dither** — algorithm, threshold, pixel size, palette, invert, serpentine, edge, color mode  
2. **Tone** — brightness, saturation, gamma, contrast, noise, strength blend, softness, seed  
3. **Generate** — pick component type, value/speed/size/label/accent, animate on/off  

Open Generate → choose e.g. `slider` or `bar-chart` → enable **Animate** → adjust dither settings live.

URL deep-link example:

```
https://ditherstudio.ideatr.dev/?a=bayer-8&gen=slider&gv=0.7&anim=1
```

## Generators (procedural)

| id | what |
|----|------|
| `bar-chart` | animated columns |
| `line-chart` | moving series |
| `pie-chart` | rotating segments |
| `button` | primary + secondary |
| `slider` | range control |
| `toggle` | on/off switch |
| `progress` | loading bar |
| `knob` | rotary dial |
| `meter` | level meter |
| `card` | metric card + sparkline |
| `dashboard` | multi-widget board |
| `waveform` | oscilloscope |
| `histogram` | distribution |
| `switch-row` | settings list |

In code (browser):

```ts
import { renderGenerator } from './lib/generate'
import { canvasToBuffer } from './lib/browser'
import { processBuffer } from './lib/dither'

const canvas = renderGenerator('bar-chart', { t: 0.35, value: 0.6, width: 640, height: 400 })
const buf = canvasToBuffer(canvas)
const out = processBuffer(buf, { dither: { algorithm: 'floyd-steinberg' }, pixelSize: 2 })
```

## Algorithms

threshold, random, floyd-steinberg, atkinson, jjn, stucki, burkes, sierra, bayer-2/4/8, halftone, blue-noise, riemersma, hybrid

See `references/algorithms.md`.

## Tone controls

| option | range | role |
|--------|-------|------|
| brightness | -100..100 | lift/crush |
| saturation | 0..2 | color amount pre-dither |
| gamma | 0.4..2.4 | midtone curve |
| contrast | 0.5..2 | contrast |
| noise | 0..1 | grain before dither |
| strength | 0..1 | blend dither vs preprocess |
| softness | 0..3 | pre-blur radius |
| seed | int | deterministic RNG |

## CLI (agents)

```bash
npm run cli -- photo.jpg -o out.png -a atkinson -t 140 --seed 7 --json
npm run cli -- batch ./in -o ./out -a bayer-8 --palette 111,eee,0f0
npm run serve
```

Flags: `-a -t -p -c --dark --light --palette --seed --gamma --contrast --edge-aware --color --export-scale --brightness` (via API/body when extended) `--json`

Full HTTP: `references/cli-api.md`.

## Agent workflow

1. Image file → CLI or upload studio.  
2. UI mock / chart / control → Studio **Generate** tab or `renderGenerator`.  
3. Tune **Tone** sliders for mood; **Dither** for algorithm/palette.  
4. Animate only for preview; export still frames for production assets.  
5. Return file path / PNG; never claim cloud upload.

## Constraints

- Local only; server binds 127.0.0.1 by default  
- Animation uses lower max-edge for FPS; export with animate off for full quality  
- `random` / blue-noise respect `seed` when set  

## Related

- Studio: https://ditherstudio.ideatr.dev  
- Examples gallery: https://ditherskill.ideatr.dev#examples  
- Source: GitLab `arjunkshah/ditherstudio` + `arjunkshah/ditherskill`
