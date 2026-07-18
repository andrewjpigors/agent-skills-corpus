---
name: synth-panel-builder
description: Build interactive SVG panel components for synthesizer instruments. Use when adding a new instrument to the project, creating or modifying panel visualizer components, or when the user references panel layout, control placement, or instrument panel design.
---

# Synth Panel Builder

Build interactive SVG panel components that faithfully reproduce physical synthesizer panel layouts as React components with hand-placed controls, interactive knobs/sliders, cable visualization, and session embedding.

## When to Use

- Adding a new instrument to the project
- Creating or modifying `*-panel.tsx` components
- Adding or fixing control positions in `*-panel-data.ts`
- The user mentions panel layout, control placement, or synth panel design
- Fixing visual issues with panel rendering

## Critical Principle: Reference-First, Never Algorithmic

**Every control must be hand-placed based on the physical panel image.** Do not use algorithmic grid layouts, computed positions, or uniform spacing. Real synth panels have intentional, non-uniform layouts that cannot be derived from control counts.

**HARD GATE: Do not place controls without a reference image.** If the manual PDF is missing, the download failed, or the panel layout pages are unclear — STOP and ask the user for a panel photo before writing any position code. Proceeding without a reference produces layouts that look nothing like the physical instrument and require a full rewrite. A textual description of a panel layout is not a substitute for seeing it.

Before writing any code:
1. Read the instrument manual PDF (in `references/`) for panel layout pages
2. If the manual is unavailable or unclear, **ask the user for a panel photo** — do not proceed without one
3. Study the image carefully: identify the layout archetype (row, columnar, cluster), which controls are adjacent, signal flow direction, and decorative routing lines
4. Map the physical layout structure: which rows/columns, which modules break the grid, which sections contain sub-sections

## Two Approaches — When to Use Which

### Data-Driven (Cascadia pattern) — DEFAULT for new instruments

Positions in a `CONTROL_POSITIONS` map, rendering via a generic loop over `CONTROL_METADATA`. Best when:
- Many repeated control types (knobs, sliders, jacks) across many modules
- Modular or semi-modular instruments with patch jacks and cables
- Frequent position iteration (change one number, not hunt through JSX)
- Cable rendering needed (jack positions in a lookup table)

**Reference implementation**: `src/components/cascadia-panel.tsx` + `src/lib/cascadia-panel-data.ts`

Key patterns:
- `CONTROL_POSITIONS` constant maps every control ID to `{x, y}`
- `SELECTOR_KNOBS` config maps selector knob IDs to their position labels
- `TWO_WAY_SWITCHES` Set distinguishes 2-way from 3-way rendering
- Generic render loop: `CONTROL_METADATA` → lookup position → switch on type → render component
- Cable paths render from `JACK_POSITIONS` lookup
- Sub-section labels and dividers as explicit SVG elements outside the loop

### Inline JSX (Evolver pattern) — for instruments with unique UI elements

Every control placed as explicit JSX with a `K()` helper. Best when:
- Instrument has many one-off visual elements (LCD display, sequencer LED grids, keyboard, mod wheels)
- Each section has a unique layout that doesn't repeat
- Few or no patch jacks / cable connections
- Small total control count

**Reference implementation**: `src/components/evolver-panel.tsx` + `src/lib/evolver-panel-data.ts`

Key patterns:
- `K(id, x, y, large, label)` helper renders interactive knobs inline
- Switches as inline `<g>` elements with hand-coded transforms
- Decorative elements (wood cheeks, LCD, brand text) mixed naturally with controls
- Two knob sizes: `knob-large` (r=14) and `knob-small` (r=10)
- NRPN parameter numbers in metadata (for MIDI-equipped instruments)

### Evolver-specific metadata differences
```typescript
// Evolver uses NRPN numbers and knob size distinction
interface ControlMeta {
  id: string;
  name: string;
  nrpn: number | null;           // MIDI parameter number
  section: string;
  type: 'knob-large' | 'knob-small' | 'switch' | 'led';  // No jacks, no sliders
}
```

## Architecture

Each instrument panel has two files:

### Data File: `src/lib/{instrument}-panel-data.ts`

For data-driven panels (Cascadia pattern):
```typescript
export interface {Instrument}ControlMeta {
  id: string;
  name: string;       // Short label matching the panel silk-screen
  module: string;     // Module/section it belongs to
  type: 'knob' | 'slider' | 'switch' | 'jack-in' | 'jack-out' | 'led';
  signalType?: 'audio' | 'cv' | 'gate' | 'modulation';  // Required for jacks
}

export const CONTROL_METADATA: Record<string, {Instrument}ControlMeta> = { ... };
export const SECTION_BOUNDS: Record<string, { x; y; width; height }> = { ... };
export function midiToRotation(value: number): number;
export function midiToSliderPosition(value: number): number;
```

For inline panels (Evolver pattern):
```typescript
export interface ControlMeta {
  id: string;
  name: string;
  nrpn: number | null;
  section: string;
  type: 'knob-large' | 'knob-small' | 'switch' | 'led';
}
```

### Component File: `src/components/{instrument}-panel.tsx`
- `'use client'` React component
- Data-driven: `CONTROL_POSITIONS` constant + type-switching render loop
- Inline: `K()` helper + explicit JSX per section
- Shared: `useKnobDrag` hook, glow filter defs, `PanelTooltip`, event delegation for hover
- Memo'd main component

## Control Types and How to Render Them

### Regular Knobs
Rotary knobs with indicator line. Supports drag interaction via `useKnobDrag`.
- Circle with indicator line rotated by `midiToRotation(value)`
- Label below
- Evolver distinguishes large (r=14) and small (r=10); Cascadia uses uniform r=12

### Selector Knobs (click-position rotary selectors)
Rotary selectors that click into labeled positions (e.g., VCF Mode: LP1-PHZ, Octave: 0-7).
- Larger circle with position labels arranged in an arc around it
- NOT a switch, NOT a regular knob — distinct visual treatment
- Data type is `'knob'` but listed in `SELECTOR_KNOBS` config: `{ 'knob-id': ['POS1', 'POS2', ...] }`
- Render with `SelectorKnobComponent`

### Sliders (modular instruments only)
Vertical faders with draggable thumb via `useSliderDrag`.
- Track height ~90px to match physical fader proportions
- Thumb slides vertically based on MIDI value
- Label below

### 2-Way Switches (on/off toggles)
Two circles stacked vertically. Selected position filled orange (`#cc4422`), other open.
- Listed in `TWO_WAY_SWITCHES` Set
- Examples: Soft Clip, TZFM, AC/DC, VCO/LFO, Env Follow, Slew Shape

### 3-Way Switches (three-position selectors)
Three circles stacked vertically (traffic light style). Selected position filled orange.
- Default for any switch NOT in `TWO_WAY_SWITCHES`
- Examples: Sub Type, Noise Type, Slew Direction, Pitch Source
- Labels go ABOVE the switch, not below (prevents visual association with wrong control)

### Rectangular Button Switches (Evolver style)
Small labeled rectangles. Used for mode/program selection, sequencer controls.
- `<rect>` with `switchRect` style + centered `<text>` label
- Optional LED indicator circle adjacent
- Used when the physical panel has labeled pushbuttons rather than toggle switches

### Input Jacks (modular only)
Dark circles (`fill: #1a1a1a`, `stroke: #555`).
- Label below with name (e.g., "PITCH IN", "FM 1 IN")

### Output Jacks (modular only)
**White-filled circles** (`fill: #e8e8e8`, `stroke: #fff`).
- Immediately distinguishable from input jacks
- Labels should NOT include "OUT" — just the signal name (e.g., "SINE", "LP4", "VCF")

### LEDs
Small indicator dots (r=3-4). Near switches or controls they indicate.
- Evolver: colored styles (`ledBlue`, `ledRed`, `ledOff`) for sequencer/mode indication
- Cascadia: simple off state, used sparingly

### Alt-Function Controls (Intellijel, Elektron, etc.)

Many modules have controls that serve **two labeled purposes** — a primary function and a secondary (ALT/shift) function accessed by holding a modifier button. Both labels are printed on the panel, typically with the primary above and alt below (or primary in bold, alt in smaller text).

**Data model:** Add an `altName` field to the control metadata:
```typescript
interface ControlMeta {
  id: string;
  name: string;        // Primary function label (e.g., "Rise")
  altName?: string;    // Secondary function label (e.g., "EF Gain")
  // ...
}
```

**Rendering:** Show both labels on the panel SVG — primary label in normal weight, alt label below in smaller/lighter text. This matches the physical panel silk-screen. Do NOT create separate metadata entries for primary and alt functions of the same physical control.

**Examples from Intellijel Swells:**
- Rise / EF Gain (one knob, two functions)
- Fall / →EF (one knob)
- Input / Trim (one knob)
- Mix / →Verb (one knob)
- Freeze / Trig (one button)
- Reverse / Drive (one button)
- Burst / Type (one button)

**The ALT button itself** is a real physical control and must be in the metadata. It's the modifier that activates the secondary functions.

### Special Elements (inline approach only)
- **LCD Display**: `<rect>` background + monospace `<text>` for program/parameter display
- **Sequencer LEDs**: Grid of circles with `ledBlue`/`ledOff` states
- **Keyboard**: White and black key `<rect>` elements
- **Mod/Pitch Wheels**: Rounded rectangles with track + position indicator
- **Wood Side Cheeks**: Decorative side panels (`<rect>` with wood-tone fill)

## Cable Rendering (Modular Instruments)

Modular and semi-modular instruments visualize patch cable connections between jacks as colored bezier curves on the panel SVG. This is a key capability for teaching patching — learners see exactly which jacks to connect.

### How it works

1. Session markdown includes `data-cables` attribute on panel markers:
   ```html
   <div data-cascadia-panel
     data-cables="jack-lfo-xyz-x-out>jack-vcf-fm-3-in:audio,jack-env-a-out>jack-vca-a-in:mod"
   ></div>
   ```

2. `session-detail.tsx` parses cable entries into `{ sourceId, destId, signalType }` props

3. `CablePath` component looks up both jack positions from `JACK_POSITIONS` (derived from `CONTROL_POSITIONS`) and draws a quadratic bezier curve between them

### Cable path geometry
- Control point: `midX = (src.x + dst.x) / 2`, `midY = max(src.y, dst.y) + droop`
- Droop scales with distance: `min(80, 30 + abs(dx) * 0.15)` — short cables hang less, long cables droop more
- SVG path: `M src.x,src.y Q midX,midY dst.x,dst.y`

### Cable colors by signal type
| Signal Type | Color | Hex |
|------------|-------|-----|
| audio | Orange-red | `#ff6644` |
| cv | Blue | `#3388ff` |
| modulation | Amber | `#ffaa33` |
| default | Gray | `#888888` |

### Cables render last
Cable `<path>` elements render after all controls in the SVG, giving them highest z-order so they visually sit on top of the panel.

### JACK_POSITIONS lookup
Built automatically from `CONTROL_POSITIONS` by filtering for `jack-in` and `jack-out` types:
```typescript
const JACK_POSITIONS: Record<string, { x: number; y: number }> = {};
for (const [id, meta] of Object.entries(CONTROL_METADATA)) {
  if (meta.type === 'jack-in' || meta.type === 'jack-out') {
    const pos = CONTROL_POSITIONS[id];
    if (pos) JACK_POSITIONS[id] = pos;
  }
}
```

### Critical regex note
The `>` character in cable syntax (`jack-source>jack-dest`) breaks naive HTML attribute regexes like `[^>]*`. The panel marker regex MUST allow `>` inside quoted attribute values:
```typescript
// WRONG: [^>]* stops at > inside data-cables="jack-a>jack-b:audio"
/<div data-cascadia-panel([^>]*)>\s*<\/div>/g

// CORRECT: allows > inside quoted values
/<div data-cascadia-panel((?:[^>"]|"[^"]*")*)>\s*<\/div>/g
```

## Physical Format Dimensions

ViewBox dimensions must match the real physical aspect ratio. Getting this wrong makes the panel unrecognizable regardless of control placement.

### Eurorack 3U modules
Standard eurorack is 128.5mm tall. Width = HP * 5.08mm. Aspect ratio is roughly 4:5 for typical modules.

| HP | Physical (mm) | ViewBox | Aspect |
|----|--------------|---------|--------|
| 4  | 20.3 x 128.5 | 60 x 380 | ~1:6.3 |
| 8  | 40.6 x 128.5 | 120 x 380 | ~1:3.2 |
| 12 | 60.9 x 128.5 | 180 x 380 | ~1:2.1 |
| 16 | 81.3 x 128.5 | 240 x 380 | ~1:1.6 |
| 20 | 101.6 x 128.5 | 300 x 380 | ~1:1.3 |
| 28 | 142.2 x 128.5 | 420 x 380 | ~1.1:1 |

Use the closest width that's a clean multiple. Height should always be ~380 for a 300-wide base scale.

### Desktop synthesizers
Landscape orientation, wider than tall. No standard dimensions — derive from the physical panel photo.
- Evolver: `0 0 1000 340`
- Cascadia: `0 0 1000 580`

### Elektron devices
Landscape, roughly 16:9 to 3:2 depending on model.
- Octatrack MKII: `0 0 1200 420`

## Layout Rules

### Row Structure (synthesizers / desktop instruments)
Panels are organized in horizontal rows separated by thin bars:
```
Top strip:   FX/Output controls, or logo/display area
Row 1:       Main audio path modules
Row 2:       Modulation/utility modules
Row 3:       Oscillators, envelopes
```

Evolver uses two rows (top: modulators/sequencer/display, bottom: oscillators/filters/output).
Cascadia uses four zones (top strip + 3 rows) with a grid-breaking left column.

### Cluster Structure (Elektron instruments — MD / MM / OT / Digi series)

Elektron devices do **not** lay out in horizontal rows like modular synths. They use **clusters** — self-contained groups of buttons/knobs with internal alignment but irregular spacing between clusters.

A cluster:
- Is internally grid-aligned (buttons within a cluster share a y-coordinate and even x-spacing)
- Sits at a position that's **independent of other clusters** (not "row 2 of a global grid")
- Often has its own mini-separator or label bracket (e.g., Octatrack's "Track Trigs" / "Sample/MIDI Trigs" brackets beneath the trig row)

Example — Octatrack MKII upper-left has four distinct clusters vertically stacked:
```
Cluster 1 (y=70):   REC1 REC2 REC3             (3 buttons, 60px spacing)
Cluster 2 (y=130):  MIDI                       (1 button, own row)
Cluster 3 (y=185):  PROJ PART AED MIX ARR      (5 buttons, 65px spacing, wider than cluster 1)
Cluster 4 (y=290):  FUNC CUE                   (2 buttons)
                    PTN  BANK                  (2 buttons, y=325)
```

These four clusters are NOT a 4-row grid. Do not try to align their widths, button sizes, or horizontal offsets. Hand-place each cluster's origin based on the photo; only use loops for repeating patterns WITHIN a single cluster (e.g., the 16 trig row).

Horizontal dividers (`<rect fill="#1a1a1a">`) should appear **only** between genuinely separate cluster groups, not between every row of buttons within a cluster.

### Columnar Structure (eurorack modules — Make Noise, Mutable, Intellijel, etc.)

Most eurorack modules do **not** use horizontal rows like a desktop synth. They use a **columnar** layout with top-to-bottom signal flow:

```
Top:      Logo / title
Row A:    Input jacks across the width (signal, trigger, CV)
Middle:   Vertical columns of knobs/controls
          ┌─────────────────────────────────────┐
          │ Outer │ Knobs │ Center │ Knobs │ Outer │
          │ stack │ col   │ column │ col   │ stack │
          │ (CV)  │ (Ch1) │ (atten)│ (Ch4) │ (CV)  │
          └─────────────────────────────────────┘
Row B:    Output jacks across the width
Bottom:   Bus outputs, brand text
```

Key characteristics:
- **Inputs at top, outputs at bottom** — signal flows top-to-bottom, not left-to-right
- **Vertical knob columns** — knobs stack vertically (Rise → Fall → Response), not in horizontal rows
- **Outer-edge input stacks** — secondary CV/gate inputs on the far left and right edges, vertically stacked alongside the knob columns they modulate
- **Symmetrical layouts are common** — left channel mirrors right channel (e.g., Maths Ch1/Ch4, Echophon wet/dry)
- **Signal flow routing lines** — printed lines on the panel connecting jacks to knobs (see Signal Flow Graphics below)
- **Compact spacing** — eurorack panels are narrow; controls are tightly packed

Example — Make Noise Maths (20HP):
```
Top:        MATHS title
Input row:  Ch1, Trig, Ch2, Ch3, Trig, Ch4 (6 jacks across)
Left outer: Cycle btn, Rise CV, Both CV, Fall CV, Cycle In (vertical stack)
Left knobs: Rise, Fall, Vari-Response (vertical column)
Center:     Attenuverters 1, 2, 3, 4 (vertical column)
Right knobs: Rise, Fall, Vari-Response (mirror of left)
Right outer: Cycle btn, Rise CV, Both CV, Fall CV, Cycle In (mirror)
Output row: Variable outs (centered), Unity/EOR/EOC + OR/SUM/INV (across bottom)
```

Do NOT default to horizontal row layouts for eurorack modules. Study the reference image to determine whether the module uses columnar, row, or hybrid structure.

### Signal Flow Graphics (eurorack panels)

Many eurorack panels have printed routing lines showing which jacks feed which controls. These are important visual cues — include them as decorative SVG elements.

**Types of routing lines:**
- **Straight horizontal** — jack and knob at the same y-coordinate, connected by a horizontal line
- **Angled** — jack and knob at different y-coordinates, connected by a diagonal line
- **90-degree elbow** (`<polyline>`) — jack drops straight down, then turns horizontally into the knob. Common when a jack at the panel edge routes to a center-column control (e.g., Ch2 signal jack → Ch2 attenuverter on Maths)
- **Arrow indicators** — envelope shape graphics showing rise/fall curves

**Implementation:**
```tsx
{/* Straight horizontal: Rise CV → Rise knob */}
<line x1={23} y1={150} x2={53} y2={128} stroke="#555" strokeWidth={0.8} />

{/* 90-degree elbow: Ch2 Signal → Ch2 Attenuverter */}
<polyline points="122,82 122,157 138,157" fill="none" stroke="#555" strokeWidth={0.7} />
```

Place routing lines BEFORE the control rendering loop so controls render on top.

### Grid-Breaking Sections
Some modules span multiple rows on one side. Handle with:
- Partial-width separator bars (don't span full width where the column breaks through)
- Separate divider bars within the breaking column
- Section bounds that reflect the actual span

### Sub-Sections
Complex modules may contain distinct sub-sections needing their own labels and dividers:
- **Utilities** → S&H, Slew/Env Follow, Mixuverter
- **Patchbay** → Mults, Sum, Invert, Bi+Uni, Expr Src, Ring Mod
- Set the parent module's display name to `''` and add explicit `<text>` sub-labels

### Section Labels
- Position in the **separator bar above** each row, not inside the module area
- Use `??` (nullish coalescing) not `||` when checking display names, so `''` doesn't fall through to the module key

## Spacing Guidelines

1. **Jacks near their controls** — patch points close to associated sliders/knobs, not far below
2. **Align across sections** — jacks in the same row across modules share the same y-coordinate
3. **Sliders under jacks** — each slider aligns vertically with its corresponding input jack
4. **Switches stacked vertically** — never in horizontal rows. Stacked on the side of the module
5. **Eliminate whitespace** — tighten vertically and horizontally between rows and controls
6. **ViewBox sizing** — use the Physical Format Dimensions table above. Height must match the real aspect ratio, not "fit the content"
7. **CV inputs align with their knobs** — Rise CV jack at the same y as the Rise knob, Fall CV at Fall knob y, etc. Don't cluster CV jacks together at arbitrary positions
8. **Check render size before placing** — Every control has a rendered size (knobs: r=12 → 24px, small knobs: r=6-8, jacks: r=6 → 12px, sliders: trackHeight px tall, buttons: r=6-8). When placing controls in adjacent rows, ensure `row_gap >= (size_of_row_above / 2) + (size_of_row_below / 2) + 4px margin`. Controls that overlap visually are worse than controls that are too spread out. Calculate minimum y-offset between rows before writing positions

## Visual Alignment

When placing controls, look for two levels of alignment in the reference image:

### 1. Sections (visual rows/groups)
Identify which controls form a **visual section** — a horizontal band of related controls at roughly the same y-coordinate. Each section is a conceptual row on the panel. Map sections top-to-bottom before placing any individual controls.

Example from Ikarie (8HP):
```
Section 1: CUTOFF (large knob, centered)
Section 2: STEREO knob (left) + VCA CV jack (right)
Section 3: PAN/SPREAD switch + STEREO CV jack (45° offset)
Section 4: RESONANCE diagonal slider (spanning width)
Section 5: RES CV jack (left) + MOD knob (right)
Section 6: INPUT knob (left) + FOLLOW SPEED switch (right)
Section 7: Input jacks row (4 across)
Section 8: Output jacks row (4 across)
```

### 2. Entity alignment (cross-section vertical/horizontal relationships)
After placing sections, check which controls **align vertically or horizontally across different sections**. These alignments are intentional in physical panel design — they create visual columns and make the panel feel organized.

Common alignment patterns:
- **Vertical columns**: Controls that share the same x-coordinate across multiple sections (e.g., STEREO at x=42 and INPUT at x=42 form a left column; MOD at x=130 and FOLLOW SPEED at x=130 form a right column)
- **Horizontal rows**: Controls at the same y-coordinate across a section (e.g., INPUT and FOLLOW SPEED share y=242)
- **Diagonal offsets**: CV jacks placed at ~45° from their associated main control (e.g., STEREO CV at 45° upper-left of PAN/SPREAD, RES CV at 45° below-left of RESONANCE slider)

**How to apply**: After writing initial positions, explicitly verify alignment by checking:
- Do left-column controls share the same x-value?
- Do right-column controls share the same x-value?
- Do same-row controls share the same y-value?
- Are diagonal-offset jacks at consistent angles from their parent controls?

If two controls should be aligned but have drifted by a few pixels during positioning, snap them to the same coordinate. Misaligned columns look worse than slightly imperfect spacing.

## Label Conventions

Use the **exact text printed on the panel silk-screen**, not verbose descriptions:
- "Trig" not "Trigger"
- "Ch 1" not "Channel 1 Signal"
- "VR" or "Vari-Response" — match what's printed
- Channel numbers: "1", "2", "3", "4" — not "Channel 1 Attenuverter"
- Output jacks: signal name only, no "OUT" suffix (existing rule, restated for emphasis)
- **Do NOT invent section headers** — if the physical panel doesn't have "REVERB PARAMETERS" or "PERFORMANCE" printed on it, don't add them as `<text>` labels in the SVG. Only render text that exists on the real panel silk-screen. Invented labels clutter the layout and inevitably overlap with controls

Eurorack panels have very limited space. Labels must be short. When in doubt, look at the panel photo.

## Coordinate Sanity Checks

After writing `CONTROL_POSITIONS`, verify these invariants before committing:

- [ ] **All x-coordinates within viewBox width** — no control at x > viewBox width - margin
- [ ] **All y-coordinates within viewBox height** — no control at y > viewBox height - margin
- [ ] **Divider/separator lines respect panel bounds** — `x2` must not exceed viewBox width. A line to x=410 on a 300px panel is a rendering bug
- [ ] **Text elements centered correctly** — title and brand text should use `x = viewBox_width / 2` when `textAnchor: 'middle'`, not an arbitrary offset
- [ ] **No label overlaps** — slider labels (y + trackHeight + 12) must not collide with controls in the next row. Calculate the actual bottom edge of each row before placing the next

These are mechanical checks that catch bugs which are obvious in isolation but get preserved across many rounds of incremental position tweaking.

## Data Model Accuracy Checklist

Before creating control metadata, verify against the physical panel:

- [ ] **Reference image is available** — do not proceed without one
- [ ] **ViewBox matches physical format** — use the dimensions table, not arbitrary values
- [ ] **Layout archetype identified** — row (desktop), columnar (eurorack), or cluster (Elektron)
- [ ] Every jack is typed correctly as `jack-in` or `jack-out`
- [ ] External inputs (EXT IN) are `jack-in`, not switches/buttons
- [ ] Rotary selectors with click positions are `knob` type, listed in `SELECTOR_KNOBS`
- [ ] Toggle switches classified as 2-way or 3-way correctly
- [ ] No phantom controls that don't exist on the physical panel
- [ ] Output jack names don't include "OUT"
- [ ] Labels match panel silk-screen text (short abbreviations, not verbose)
- [ ] Control count per module matches the physical panel
- [ ] Signal flow routing lines identified from the panel image
- [ ] NRPN numbers verified against manual parameter list (if applicable)

## Integration Points

### Session Detail Embedding
`src/components/session-detail.tsx` detects panel markers per instrument:
- Regex: `/<div data-{instrument}-panel([^>]*)>\s*<\/div>/g`
- Parser function: `parse{Instrument}PanelProps(attrString)`
- Renders the correct panel component based on `instrumentSlug`
- When adding a new instrument, add a new regex + parser + conditional render branch

### Standalone Route
`src/app/instruments/[slug]/panel/page.tsx` renders the panel at `/instruments/{slug}/panel`.
- Add the instrument to `PANEL_CONFIG` with title, description, and maxWidth
- Update `standalone-panel-client.tsx` to conditionally render the new panel component

### Quick Reference Panel
`src/components/quick-ref-panel.tsx` shows a Panel tab in the session sidebar.
- Add conditional `{instrumentSlug === '{slug}' && <{Instrument}Panel />}` block

### Patch Detail
`src/components/patch-detail.tsx` shows the panel inline for patch pages.
- Add conditional render for the new instrument with cable_routing mapping

## Content Pipeline

When adding panel markers to session files, **update all three locations**:
1. `sessions/{instrument}/*.md` — source of truth in the repo
2. `src/content/sessions/{instrument}/*.md` — bundled content for Vercel deploys
3. `~/song/sessions/{instrument}/*.md` — Obsidian vault (app reads from here locally)

The app reads from `~/song` when `vaultPath` is configured in `evolver.config.json`. If the vault doesn't exist (Vercel), it falls back to `src/content/`. Missing the vault sync means panels won't render locally even though the code is correct.

### Marker Format
```html
<!-- Basic: zoom to sections, highlight controls -->
<div data-{instrument}-panel
  data-sections="module-a,module-b"
  data-knobs="knob-id:64,slider-id:100"
  data-highlights="control-id:blue,jack-id:amber"
></div>

<!-- With cables (modular instruments) -->
<div data-{instrument}-panel
  data-sections="vco-a,mixer"
  data-cables="jack-source>jack-dest:audio,jack-b>jack-c:cv"
></div>
```

## Iterative Workflow

Panel building is inherently visual and iterative:

1. **Study the reference** — read the manual, identify every control type and its physical position
2. **Structure first** — get the row layout and module positions roughly right
3. **Module by module** — work through each section comparing to the reference image
4. **User screenshots** — the user will share screenshots showing issues. Compare to the manual
5. **Small adjustments** — position tweaks of 10-20px are normal. Make the change, reload, check
6. **Test after changes** — run `npx vitest run` on the data and component test files
7. **Tighten last** — eliminate whitespace only after positions are structurally correct

### Context degradation warning

After ~5+ rounds of incremental tweaking in a single conversation, accumulated context works against you. You start anchoring to prior position values instead of the reference image. Bugs introduced early (wrong x2 on divider lines, invented section labels, off-center text) survive because attention shifts to whatever was discussed most recently.

**If a panel still doesn't look right after several rounds**: it's more productive to clear context and re-evaluate the code fresh against the reference image than to continue nudging coordinates. A fresh read catches mechanical bugs (coordinates outside viewBox, labels overlapping controls) that are invisible after 20 rounds of "move this 5px down."

Run the **Coordinate Sanity Checks** (below) before and after any multi-round positioning session.

## Testing

### Data tests (`src/lib/__tests__/{instrument}-panel-data.test.ts`)
- Total control count matches expected
- Every entry has required fields (id, name, module, type)
- Every jack has signalType
- Module names are all valid
- Section bounds have positive dimensions
- Per-module control counts match the physical panel
- Utility functions (midiToRotation, midiToSliderPosition) boundary values

### Component tests (`src/components/__tests__/{instrument}-panel.test.tsx`)
- Renders without crashing
- SVG has correct viewBox
- Cable paths appear with correct bezier commands (modular only)
- Cable colors match signal type
- Glow filter applied for highlighted controls
- Zoom changes viewBox when zoomSections provided

## File Naming Convention

- Data: `src/lib/{instrument}-panel-data.ts`
- Component: `src/components/{instrument}-panel.tsx`
- Tests: `src/lib/__tests__/{instrument}-panel-data.test.ts`, `src/components/__tests__/{instrument}-panel.test.tsx`
- Tooltip: `src/components/evolver-panel-tooltip.tsx` (shared across instruments)
- ID convention: `{type}-{module}-{name-kebab}` (e.g., `knob-vco-a-pitch`, `jack-mixer-out`, `switch-vcf-mode`)

## Changelog

### 2026-04-18 — Maths panel exposed eurorack-specific gaps

The Maths panel (Make Noise, 20HP eurorack) was initially generated with a
completely wrong layout. The agent proceeded without a reference image
(manual PDF download had failed) and defaulted to Cascadia-style horizontal
rows — producing a 300x700 viewBox with controls in stacked rows instead of
the real columnar layout with inputs-at-top / knobs-in-middle / outputs-at-bottom.

Every aspect of the initial generation was wrong: aspect ratio (2:1 instead
of 4:5), layout archetype (rows instead of columns), signal flow direction,
CV input placement (horizontal instead of vertical edge stacks), and labels
("Signal" instead of "Ch 1"). The user provided a panel photo and walked
through corrections over ~6 rounds of feedback.

**Additions to the skill from this round:**
- **Physical Format Dimensions table** — eurorack HP-to-viewBox mapping so
  agents never guess at aspect ratios
- **Columnar Structure archetype** — eurorack modules use vertical columns
  with top-to-bottom signal flow, not horizontal rows
- **Signal Flow Graphics** — routing lines (`<line>`, `<polyline>` with
  90-degree elbows) connecting jacks to knobs
- **Hard gate on reference images** — STOP and ask for a photo if the manual
  is unavailable, do not proceed with textual descriptions
- **Label Conventions** — use exact panel silk-screen text, not verbose names
- **CV input alignment rule** — CV jacks should align vertically with the
  knobs they modulate

**Takeaway**: the skill's existing guidance was desktop-synth-centric. The
Row Structure and Cluster Structure archetypes didn't cover the most common
eurorack layout pattern. Future eurorack module builds should now start from
the right archetype and the right aspect ratio, avoiding the full-rewrite
cycle that Maths required.

### 2026-04-16 — Octatrack MKII validated the skill
Adding the Octatrack MKII panel took only **a handful of prompts** to reach a
usable layout — a massive improvement over the Evolver and Cascadia builds,
both of which required many iterative rounds of visual comparison and position
tweaking (Cascadia alone went through ~20 rounds).

What made the difference:
- The **reference-first, never algorithmic** principle was enforced from the
  start — the initial plan explicitly named the manual as the source of truth
  and flagged positions for later manual verification
- The **data-driven vs inline-JSX** decision was made up front based on the
  control inventory (Octatrack's 67 controls with repeating trig/track rows
  pointed clearly at the data-driven approach)
- The **ID convention** and **SECTION_BOUNDS** structure were already codified,
  so the only work left was positioning — not architecture
- User feedback about the real physical layout (LCD central, T1-T4/T5-T8
  flanking, SRC/AMP below LCD, crossfader above trig row) was applied as
  targeted coordinate edits rather than rewrites

This round also added the **Cluster Structure** section (above) covering
Elektron instruments — a pattern that Row Structure didn't capture. Future
Elektron panel work (Digitakt, Digitone, Analog Rytm, etc.) should benefit
from the same cluster-first framing.

**Takeaway**: the skill is now mature enough that adding a new instrument
panel is mostly a positioning exercise, not an architectural one. Keep the
skill up to date with lessons learned from each new instrument so the next
build stays fast.

### 2026-04-18 — Swells panel: context degradation during iterative positioning

The Swells panel (Intellijel, 20HP eurorack) was built over a long session
with many rounds of incremental position tweaks. After clearing context and
re-evaluating fresh, several bugs were immediately obvious:

- **Divider lines extended to x=410** on a 300px-wide panel (rendering garbage
  past the right edge)
- **Invented section labels** ("REVERB PARAMETERS", "LEVEL", "PERFORMANCE",
  "SWELL GENERATOR", "I/O") that don't exist on the physical panel silk-screen,
  positioned at y-coordinates that overlapped with controls
- **Title and brand text off-center** (x=210 instead of x=150 for a 300px panel)
- **Vertical spacing too tight** in top section — CV jacks, attenuverters, and
  LEDs crammed into 26px of vertical space

All of these were fixable in a single pass with fresh context. The prior
session had been tweaking positions for many rounds but never stepped back to
check whether divider lines respected the viewBox or whether section labels
actually existed on the physical panel.

**Additions to the skill from this round:**
- **Coordinate Sanity Checks** — mechanical checklist to catch coordinates
  outside viewBox, divider lines past panel edges, off-center text
- **Label convention update** — explicit rule against inventing section headers
  not printed on the physical panel
- **Context degradation warning** — after ~5+ rounds of tweaking, clear context
  and re-evaluate rather than continuing to nudge

**Takeaway**: the skill's iterative workflow guidance assumed indefinite
productive iteration within one context window. In practice, accumulated
context causes anchoring to prior values and blindness to mechanical bugs.
The new guidance prescribes fresh-context checkpoints for long positioning
sessions.

### 2026-04-18 — Ikarie panel: visual alignment and diagonal sliders

The Ikarie panel (Bastl/Casper, 8HP) exposed two gaps:

1. **Diagonal slider rendering**: Ikarie's RESONANCE fader is physically
   mounted at a ~55° angle (low-left to high-right). The initial
   implementation used the wrong rotation direction (-35° instead of +55°),
   placing high values on the LEFT instead of the RIGHT. A centered track
   (`y = -halfTrack to +halfTrack` instead of `0 to trackHeight`) was needed
   so rotation pivots around the slider's visual center, not one end.

2. **Visual alignment was missing from the skill**: The agent placed controls
   at plausible-looking coordinates without checking whether controls that
   should share an x or y coordinate actually did. The physical panel has
   clear vertical columns (STEREO and INPUT at the same x on the left; MOD
   and FOLLOW SPEED at the same x on the right) and horizontal rows (INPUT
   and FOLLOW SPEED at the same y). Without explicit alignment checking,
   these relationships drifted by 5-10px during initial placement.

**Additions to the skill from this round:**
- **Visual Alignment section** — two-level framework: (1) identify sections
  (horizontal bands of related controls), (2) check entity alignment across
  sections (shared x for vertical columns, shared y for horizontal rows,
  consistent diagonal offsets for CV jacks). Verify alignment explicitly
  after placing positions
- **Diagonal slider support** — new `DiagonalSliderComponent` with centered
  track and configurable rotation angle. `DIAGONAL_SLIDER_ANGLE` constant
  for easy adjustment. Positive angle = clockwise = high-right/low-left
- **Horizontal switch support** — `HORIZONTAL_SWITCHES` Set for switches
  that render circles horizontally (e.g., Ikarie's FOLLOW SPEED: SLOW/MID/FAST)

**Takeaway**: the skill had good rules for spacing and label accuracy but
lacked explicit guidance on checking alignment relationships between controls
across different sections. "Place controls based on the reference" is
necessary but not sufficient — you must also verify that the mathematical
relationships (shared coordinates) match the visual relationships in the
reference image.
