---
name: html-schematic
description: Interactive HTML schematic generator for Hubble Engineering. Creates and edits SVG-based electronic circuit schematics with zoom, pan, tooltips, and PNG/SVG export. Use when creating a new schematic from scratch or adding components and wiring to an existing one.
version: 4.0.0
---

# html-schematic

Hubble Engineering interactive HTML schematic generator — Orchestrator + 10 specialized sub-agents with cross-consult protocol.

## When to use
- Creating a **new (Rev 1)** HTML schematic from scratch
- **Revising (Rev ≥ 2)** an existing schematic — adding/removing/replacing parts, bumping revision history
- Validating or fixing an existing schematic's style
- Switching themes (Cyberpunk ↔ Dark Teal)
- Re-tuning export rules (print SVG vs themed PNG)

---

## Agent Architecture

```
                       User Request
                            │
                            ▼
              ┌─────────────────────────────┐
              │        ORCHESTRATOR         │
              │  (routes intent, brokers    │
              │   consults, writes output)  │
              └──────────────┬──────────────┘
                             │
   ┌─────────────────────────┼─────────────────────────┐
   ▼            ▼            ▼            ▼            ▼
 [Layout]  [Datasheet]  [NetColor]  [Assembler]  [Harness]
   ▼            ▲            ▲           ▲            ▲
 [Wire     consults via the Orchestrator     [Validator]
  Router]  (max 2 consults / agent / run)         ▲
                                                  │
                              [Revision Mgr] [Export Spec]
```

Agents share a **Layout Manifest** — a structured record passed from one agent to the next. Each agent reads the manifest, appends its output, and hands off. Any sub-agent may emit a `CONSULT` request back to the Orchestrator to ask another agent a focused question (e.g. Assembler → Datasheet for an unknown pinout). The Orchestrator dispatches the consult and forwards the answer.

**Roster (11 agents total — 1 orchestrator + 10 sub-agents):**

| # | Agent | Owns | Reads | Writes |
|---|---|---|---|---|
| 1 | **Orchestrator** | Intent routing, sub-agent sequencing, **consult broker**, final HTML assembly | manifest | final HTML |
| 2 | **Layout Planner** | Component coordinates, canvas regions, bottom-panel allocation | conventions.md | manifest §components |
| 3 | **Datasheet Researcher** | Resolves pinouts for ICs / dev kits / connectors / headers from name + package | web / local cache | manifest §pinouts |
| 4 | **Net Color Allocator** | Assigns wire class (`.wdata` … `.wdata7`) per net per VR9 + CLAUDE.md table | manifest §nets | manifest §nets[*].wire_class |
| 5 | **Component Assembler** | Snippet substitution for each component `<g>` | snippets/, tokens.md | SVG `<g>` blocks |
| 6 | **Specification Table & Notes Builder** | Emits per-part harness/pinout tables, the wire-gauge table, the fuse-margin table, and the notes panel | manifest §pinouts §nets §components §notes, tables.md | SVG table groups + notes text blocks |
| 7 | **Wire Router** | Orthogonal routing, **arc hops at ALL crossings**, junctions | manifest, conventions.md | SVG wire elements |
| 8 | **Revision Manager** | `EDIT_REVISION` flow — diff prior schematic, bump `<title>` + title-block rev, append revision-history row | prior HTML | revised HTML delta |
| 9 | **Style Validator** | Token contract, VR1 clearance, **VR2 axis alignment**, **VR3 no-overlap topology**, **VR4 tooltip presence**, **VR5 wire/bg contrast**, **VR6 BOM format**, **VR7 wire channel labels**, VR9 net colors, **VR10 missing-arc-hop**, hex literal grep, no-fill-on-containers. **Algorithm details for VR1–VR10 in `reference/validator-spec.md`.** | full HTML | PASS/WARN/FAIL + auto-fix |
| 10 | **Export Specialist** | Owns `getSvgStringPrint()` and `getSvgStringThemed()`; handles `THEME_SWITCH` palette remap | skeleton.html, theme files | updated `:root` / `<script>` |
| 11 | **BOM Specialist** | Auto-populates BOM `<tbody>` rows from manifest §components; groups duplicates; assigns Item#; emits VR6-compliant rows | manifest §components | `<tr>` HTML inside the BOM `<foreignObject>` |

*The roster above is numbered #1 (Orchestrator) through #11. Section headings below cover only the 10 sub-agents, numbered 1–10, and correspond to roster rows #2–#11 respectively (e.g. roster #2 "Layout Planner" = "Sub-Agent 1 — Layout Planner").*

---

## Orchestrator

**Entry point for every `/html-schematic` invocation.**

### Intent routing table

| User says… | Intent | Sub-agents called |
|---|---|---|
| "create", "new schematic", "Rev 1", "draw from scratch" | `CREATE_REV1` | Layout → [Datasheet ∥ NetAllocator] → Assembler → [SpecTables&Notes ∥ BOM] → WireRouter → Validator |
| "revise", "Rev 2", "add to existing", "edit `<path>`", "update component on `<file>`" | `EDIT_REVISION` | RevisionMgr → Layout (delta) → [Datasheet ∥ NetAllocator as needed] → Assembler → [SpecTables&Notes ∥ BOM] → WireRouter → Validator |
| "validate", "check", "fix style" | `VALIDATE` | Validator only |
| "switch theme", "use Dark Teal", "back to Cyberpunk" | `THEME_SWITCH` | Export Specialist |
| "tune export", "change print rules" | `EXPORT_TUNE` | Export Specialist only |

> **🔄 Session persistence.** Once `/html-schematic` is invoked in a session, the Orchestrator's intent-routing table stays active for every subsequent turn — the user does NOT need to re-invoke per edit. Bare directives like `u10px`, `r20`, "smaller font 0.5x", "reverse this step", `RC1 width=80`, "balance the spacing" auto-route to the appropriate sub-agent. An element selection (via `<launch-selected-element>` blocks) in the message body is treated as the target.
>
> **When to re-invoke:** if conversation context is compacted or summarized and the skill rules drop out of the agent's working context, bare directives may stop being recognized. Re-invoke `/html-schematic` once to re-anchor routing for the rest of the session.

### Mode rules

- **`CREATE_REV1`** is the **only** path that reads `skeleton.html`. It MUST NOT read any other `.html` file.
- **`EDIT_REVISION`** reads the **existing project HTML** the user names. It MUST NOT re-read `skeleton.html`. It bumps the `<title>` revision and the title-block `Rev X.Y` text, and appends a row to the revision-history block.

### Orchestrator responsibilities
- Parse intent and pick the route from the table above
- Pass the Layout Manifest between sub-agents in the listed order
- **Dispatch consult requests** between sub-agents (see protocol below)
- After Validator passes, assemble final HTML and write the output file
- **Pre-edit fresh-read protocol** — when issuing a multi-line `Edit` more than ~3 turns after the most recent `Read` of the target file, fresh-`Read` the affected line range first. Stale model-state vs on-disk state has been observed to cause `old_string not found` failures during long revision sessions.
- **Does NOT** calculate coordinates, write snippet SVG, allocate wire colors, or research pinouts itself

---

## Cross-agent consult protocol

Any sub-agent may emit:

```
CONSULT {
  to:       <agent name>          # e.g. "Datasheet Researcher"
  question: <focused, one-shot>   # e.g. "Pin map for LM358N DIP-8"
  context:  <relevant manifest excerpt>
}
```

The Orchestrator:
1. Receives the CONSULT block.
2. Invokes the named agent with the question + relevant manifest slice.
3. Returns the answer to the requesting agent.
4. Resumes the original pipeline.

**Budget:** max **2 consults per agent per run**. If an agent would exceed that, it escalates back to the Orchestrator with a `BLOCKED: need user input` message and the run pauses.

**Common consult patterns:**
- Component Assembler → Datasheet Researcher (unknown pinout / package)
- Wire Router → Net Color Allocator (a new net appears mid-routing)
- Harness-Table Builder → Datasheet Researcher (full pin-name list)
- Validator → Wire Router (auto-fix a missing arc hop — single retry)
- Revision Manager → Layout Planner (place a newly added part respecting existing layout)
- Any agent → Export Specialist (export-rule question, e.g. "what color does print mode use?")

---

## Sub-Agent 1 — Layout Planner

**Input:** Component list from user (or from Revision Manager's diff)
**Output:** Layout Manifest §components, §canvas, §bottom-panel-allocation

### Canvas constants (must match `skeleton.html`)

- SVG dimensions: `width=2400 height=1800`, `viewBox="-180 -15 2420 1815"`
- Inner work region (after `<g transform="translate(80,0)">`):
  - Main diagram: `x ∈ [0, 2040]`, `y ∈ [110, 1010]`
  - Common ground bus: `y = 1020`
  - Bottom panels: `y ∈ [1080, 1700]`
- **20 px margin inside the inner work region** (not against the outer viewBox).

### Layout rules

- Minimum 40 px gap between any two component bodies
- Power buses: horizontal, placed inside the main-diagram band (`y ∈ [110, 1010]`)
- Data buses: vertical, placed at the left/right edges of the inner region
- Pin markers flush to the component body edge they belong to
- Stack components left-to-right, grouped by function (power → control → IO)
- **Reserve a column in the bottom-panel area for harness tables** (default `x ∈ [1000, 1340]`, beside the wire-gauge table which occupies `x ∈ [690, 990]`)
- **Local vs schematic coordinates inside transformed sub-groups** — when a component `<g>` carries a `transform="translate(... ) scale(...)"`, every child element's `x`/`y`/`cx`/`cy`/`d` is in the *parent-group's* local coordinate frame, not the schematic frame. Revision Manager nudges applied to such children must use local deltas (multiply schematic delta by the inverse scale if necessary).

### Layout Manifest format

```
LAYOUT_MANIFEST:
  canvas: {w: 2400, h: 1800, viewBox: "-180 -15 2420 1815"}
  legend_entries:
    # Drives the title-block legend strip (M4). Sub-Agent 4 rule 10 emits one
    # <rect> swatch + one <text> label per entry. If absent, the strip is
    # auto-derived from the set of wire classes appearing in §nets.
    - {wire_class: "w12v",   label: "12V"}
    - {wire_class: "w5v",    label: "5V"}
    - {wire_class: "wgnd",   label: "GND"}
    - {wire_class: "wdata",  label: "CH1 (GPIO1)"}
    - {wire_class: "wdata2", label: "CH2 (GPIO2)"}
  components:
    - id: "U1"
      type: "component-box"
      part: "ESP32-S3-WROOM-1"
      package: "WROOM-38"
      value: "ESP32-S3-WROOM-1-N16R8"   # optional; defaults to `part` if absent
      tolerance: ""                       # optional; e.g. "1%", "X7R"
      rating: ""                          # optional; e.g. "50 V", "1/4 W"
      channel_group: ""                   # optional; e.g. "RC" for RC1..RC4 — tags symmetric iteration
      channel_index: 0                    # optional; 1-based index within the channel_group
      x: 300  y: 200  w: 260  h: 380
      label: "ESP32-S3"
      # ── Optional transform fields (for type=dev-board-visual or any scaled <g>) ──
      transform_translate: [696.07, 174]  # optional; null/absent = no translate
      transform_scale: [0.8539, 0.8]      # optional; null/absent = no scale
      # When set, every child element's x/y/cx/cy/d is in the LOCAL coord frame.
      # Sub-Agent 7 nudge math: local_delta = schematic_delta / scale_factor per axis.
      pins:
        - {id: "U1.1",  name: "GND",  net: "GND",      edge: "left",  offset: 40}
        - {id: "U1.2",  name: "3V3",  net: "BUS_3V3",  edge: "left",  offset: 60}
        - {id: "U1.18", name: "GPIO15", net: "DATA_RGB", edge: "right", offset: 60}
        - {id: "U1.38", name: "EN",   net: "EN",       edge: "top",   offset: 30}
        # edge ∈ {"left", "right", "top", "bottom"}; offset is measured from the
        # component's top-left along that edge (LOCAL frame if transform_scale set)
      # ── Schematic-frame pins (outside the scaled inner group) ──
      schematic_pins:                       # optional; only for scaled components
        - {id: "U1.PSU+_CH1_COM", cx: 1221, cy: 250}
        - {id: "U1.ATZ1+_CH1_NO", cx: 1221, cy: 280}
        # cx/cy in SCHEMATIC coords (i.e. after transform_translate + transform_scale).
        # Use these for net annotations and outer wire endpoints; the Wire Router
        # connects to schematic_pins, never to local-frame pins, when the component
        # carries transform_scale.
      is_critical: false                    # M5: drives BOM warn-color highlighting.
                                            # Auto-true for fuses where margin_ratio < 1.5×.
      # ── Fuse-specific fields (only for type=fuse-vertical or fuse-horizontal) ──
      # fuse_rating: 2.0                    # amperes (the fuse value, T2A = 2.0)
      # steady_load: 1.4                    # amperes (the actual steady-state load)
      # margin_ratio: 1.43                  # = fuse_rating / steady_load. < 1.5 → critical.
  pinouts:
    - id: "U1"      # filled in by Datasheet Researcher if part is recognized
      rows: [{pin: "1", name: "GND", net: "GND"}, ...]
  nets:
    - id: "BUS_5V"     wire_class: "w5v"
      # ── M1 wire-gauge fields (optional; drive Sub-Agent 5 wire-gauge table) ──
      awg: 18                            # AWG, integer
      load_current: 8.2                  # amperes (steady)
      ampacity_pct: 65                   # ampacity used by this run, percent
      run_description: "PSU+ trunk"       # short prose; flagged in --warn when ampacity_pct ≥ 70
    - id: "DATA_RGB"   wire_class: "wdata"
      awg: 22
      load_current: 0.05
      ampacity_pct: 5
      run_description: "GPIO15 → driver"
  bottom_panels:
    # ── L5: optional data_info on each panel for the hover tooltip ──
    - {kind: "BOM",          x:  40,  y: 1080, w: 620, h: 620, data_info: "Bill of Materials|Component list"}
    - {kind: "wire-gauge",   x: 690,  y: 1080, w: 300, h: 200, data_info: "Wire gauge|AWG and current rating per run"}
    - {kind: "fuse-margin",  x: 690,  y: 1290, w: 300, h: 180, data_info: "Fuse margin summary|Steady load vs fuse rating"}
    - {kind: "harness",      x: 1000, y: 1080, w: 340, h: auto, data_info: "Wire-harness map|Per-part pinout tables"}  # stacks vertically
    - {kind: "notes-rev",    x: 1350, y: 1080, w: 650, h: 620, data_info: "Notes and revision history"}
  notes:
    # ── M2: top-level notes panel drives Sub-Agent 5 notes builder ──
    - {number: 1, lines: ["Fuse topology: F_MAIN protects all downstream; F1 only ESP sub-branch."], is_warning: false}
    - {number: 3, lines: ["Buck pre-calibration: with F2 installed and buck output DISCONNECTED,",
                          "power up PSU and adjust the trim pot until DMM reads 5.00 V ± 0.05 V.",
                          "Power down. Only then connect the COM bus."], is_warning: true}
```

**Channel-group auto-detection.** If Layout Planner sees `≥ 3` components in the manifest whose `id` matches `<prefix><integer>` (e.g. `RC1, RC2, RC3, RC4` or `F3, F4, F5, F6` or `LED1..LEDn`), it auto-stamps each with `channel_group=<prefix>` and `channel_index=<integer>`. Explicit values in the manifest override auto-detection. The tag enables Revision Manager's channel-group propagation (see Sub-Agent 7) so a single nudge or resize cascades across all members.

**Tools to read:** `reference/conventions.md`

---

## Sub-Agent 2 — Datasheet Researcher

**Called by:** Orchestrator, or consulted by Assembler / Harness-Table Builder
**Input:** part name + package (e.g. `LM358N` + `DIP-8`, `ESP32-S3-WROOM-1`, `JST-XH-4P`)
**Output:** manifest §pinouts entry — `[{pin, name, default_net?}]`

### Coverage
- ICs with public datasheets (op-amps, MCUs, regulators, transceivers)
- Dev kits with standard pinouts (Arduino Uno/Nano/Mega, RPi 40-pin, ESP32 dev boards)
- Connectors (JST PH/XH, Molex, Dupont, terminal blocks)
- Headers (2.54 mm pin, IDC ribbon, board-to-board)

### Behavior
- If pinout is well-known, return it deterministically.
- If unsure, return `{confidence: "low", suggestion: "<best guess>"}` and let the Orchestrator surface a clarifying question.
- Never invent pin numbers/names — better to flag low confidence than hallucinate.

---

## Sub-Agent 3 — Net Color Allocator

**Called by:** Orchestrator (always, after Layout) and consulted by Wire Router
**Input:** manifest §nets (net IDs only) + working-dir `CLAUDE.md` Wire Assignment Table if present
**Output:** manifest §nets[*].wire_class

### Rules
- `GND` → `wgnd`
- `12V` family → `w12v`
- `5V` family → `w5v`
- `3V3` family → `w3v3`
- All other nets get assigned a `wdata` … `wdata7` class **once** and that class follows the entire net (VR9).
- If working-dir `CLAUDE.md` has a "Wire Assignment Table", it is **binding** — read it first.

---

## Sub-Agent 4 — Component Assembler

**Called by:** Orchestrator after Layout + NetAllocator (and after Datasheet Researcher if pinouts were needed)
**Input:** Layout Manifest
**Output:** Assembled `<g>` SVG blocks for all components, ready to insert into skeleton

### Snippet selection logic

| Manifest `type` | Snippet file |
|---|---|
| `component-box` | `snippets/component-box.html` |
| `dev-board-visual` | `snippets/dev-board-visual.html` |
| `fuse-vertical` | `snippets/fuse-vertical.html` |
| `fuse-horizontal` | `snippets/fuse-horizontal.html` |
| `gpio-marker` | `snippets/gpio-marker.html` |
| `power-junction` | `snippets/power-junction.html` |
| `wire-rounded` | `snippets/wire-rounded.html` |
| `bus-endcap` | `snippets/bus-endcap.html` |
| `warning-banner` | `snippets/warning-banner.html` |
| `note-numbered` | `snippets/note-numbered.html` |
| `revision-single` | `snippets/revision-single.html` |
| `revision-multi` | `snippets/revision-multi.html` |
| `section-border-dash` | `snippets/section-border-dash.html` |
| `harness-table` | `snippets/harness-table.html` |

`dev-board-visual` is for physical-board replicas (relay boards, dev kits with rich silk) where the board image itself is the schematic representation. It uses a scaled inner `<g>` — see C3 (manifest `transform_scale` / `schematic_pins`) and Sub-Agent 7's scaled-nudge math. `fuse-vertical` / `fuse-horizontal` are orientation-specific in-line fuse blocks with a rotated or centered label and a slow-blow sub-caption.

### Assembly rules
1. Read each required snippet file
2. Substitute manifest values into the snippet (x, y, w, h, label, pin offsets)
3. Assign `data-info` tooltip with 3 or 4 pipe-separated fields: `"ComponentID|brief|spec"` or `"ComponentID|brief|spec|note"`. Example: `data-info="F1|Inline fuse 1 A slow-blow (T1A)|5×20 mm · 22 AWG RED|ESP sub-branch protection"`. The 4th field is optional and used for failure-mode hints, upgrade notes, or safety callouts.
4. Wrap each component in `<g id="COMPONENT_ID">…</g>`
5. **No hardcoded hex** — use only CSS token variables (e.g. `stroke="var(--comp-stroke)"`)
6. **Container shapes are outline-only** — `fill="none"` on rects/polygons that wrap text. Indicator dots (junction, pin) stay filled. **`class="comp"` and `data-info` go on the `<rect>`, NOT on the wrapping `<g>`.** The `<g>` carries only `id`. Reason: `.comp { fill: none }` on a `<g>` cascades via CSS inheritance to child `<text>` and makes labels invisible — putting the class on the `<rect>` isolates `fill: none` to the box outline. Validator selectors (`rect[class~="comp"]`) resolve the component id by walking up to `rect.closest('g[id]')`.
7. If a component's pinout is missing from the manifest, emit `CONSULT → Datasheet Researcher`.
8. **Single-text containers fit their content** — when a `<rect>` (e.g. warning banner, callout) wraps exactly one `<text>` node, set `rect.width = text.getBBox().width + 16` and `rect.x = text.x − (rect.width / 2)` (assuming `text-anchor="middle"`). Banners that span the canvas because "it looks wide enough" are a VR3 risk and a visual rough-edge.
   **Exception (L4): full-width status banners.** When the banner intentionally spans most of the canvas (intent: "this warning applies to the whole schematic, not a localized callout"), auto-fit does NOT apply — the width is hand-tuned to the schematic's inner-region width. Heuristic: any banner whose target width ≥ `canvas_inner_width × 0.4` is treated as a full-width banner and skips auto-fit. Canonical example: Scent Controller §9 PRE-SET BUCK warning at `width="921"` (about 45% of the 2040-px inner region) — intentionally wide so the warning is read as global. Localized callouts (RC snubber tooltips, F2 sub-captions, etc.) still auto-fit per the rule above.
9. **Multi-text containers fit their stacked content** — when a component `<rect>` wraps `N ≥ 2` stacked `<text>` nodes (title + value, label + spec, ID + tolerance), size the box so the text breathes:
   - `rect.width  = max(text_widths) + 2 × hpad` with `hpad ≥ 8 px`
   - `rect.height = (N − 1) × line_gap + Σ font_size_i + 2 × vpad` with `vpad ≥ 6 px`
   - `line_gap ≥ font_size × 1.3` baseline-to-baseline (use the larger of the two adjacent font sizes when they differ)
   - **Inter-text bbox-edge-to-bbox-edge gap ≥ 3 px** — Validator VR8b (`reference/validator-spec.md`) warns below this
   - All texts share `text-anchor="middle"` and sit at `rect.cx`; baselines distributed evenly between `rect.y + vpad + font_size_1` and `rect.y + h − vpad`
   - Worked example: title font-size 11 + value font-size 10, vpad=6, hpad=8, line_gap=15 → box 70×70 px is the minimum for the RC-snubber pattern (RC1–RC4 in the Scent Controller Rev 1.0 schematic).
10. **Title-block legend strip (M4)** — generate paired color-swatch `<rect>` + label `<text>` entries inside `<g id="title-block">` from `manifest.legend_entries` (or auto-derive from `manifest.nets[*].wire_class` if `legend_entries` is absent). Pattern:
    ```svg
    <rect x="{ENTRY_X}" y="46" width="24" height="3" rx="1.5" fill="var(--wire-{TOKEN})"/>
    <text x="{ENTRY_X + 32}" y="52" font-size="12" fill="var(--text-secondary)"
          class="bold-text" letter-spacing="1">{LABEL}</text>
    ```
    Stride between entries: 60-80 px along x, chosen so each label fits without overlap. Power rails first (12V → 5V → GND → 3V3), then data channels in `wdataN` order. Bus variants share the rail entry — emit only one swatch per rail color. VR7 enforces presence of every used wire class as a legend entry.

**Tools to read:** all required `snippets/*.html`, `reference/tokens.md`

---

## Sub-Agent 5 — Specification Table & Notes Builder

**Called by:** Orchestrator after Component Assembler
**Input:** manifest §pinouts, §nets, §components (for fuses), §notes
**Output:** SVG `<g>` table groups + notes-panel `<text>` blocks, placed in their allocated `bottom_panels` slots

This agent owns four bottom-panel artifacts:

1. **Per-part harness tables** — one per IC / dev kit / connector / header with ≥ 4 used pins
2. **Wire-gauge table** (M1) — one row per net, showing AWG / ampacity / run description
3. **Fuse-margin table** (M1) — one row per fuse component, showing rating / load / margin
4. **Notes panel** (M2) — numbered notes shared with the revision-history container

### Harness tables

- Emit a table for every part with **≥ 4 used pins**: ICs, dev kits, connectors, headers.
- Skip parts with < 4 pins (Rs, Cs, LEDs, transistors, 2-pin headers).
- Stack tables vertically in the allocated column from §bottom_panels.
- Use `snippets/harness-table.html` — see its header comment for substitution tokens.
- The "CH" column shows a wire-color swatch using the same wire class as the routed net, so the table tracks any future theme switch.
- If a pinout is incomplete in the manifest, emit `CONSULT → Datasheet Researcher` before drawing.

### Wire-gauge table (M1)

Drives from `manifest.nets[*]` entries that carry the optional gauge fields (`awg`, `load_current`, `ampacity_pct`, `run_description`). Skip nets without gauge data — the wire-gauge panel only documents power and bus runs that warrant a gauge spec.

Per-row template (use the same `j*` class as the wire so the swatch follows theme switches):

```svg
<rect x="20"  y="{ROW_Y - 4}" width="20" height="4" rx="1" class="j{WIRE_CLASS_SUFFIX}"/>
<text x="120" y="{ROW_Y}" font-size="11" fill="var(--text-primary)"   text-anchor="middle" class="bold-text">{AWG}</text>
<text x="200" y="{ROW_Y}" font-size="11" fill="var(--text-secondary)" text-anchor="middle">{LOAD_A} A · {AMPACITY_PCT}%</text>
<text x="265" y="{ROW_Y}" font-size="11" fill="{ROW_FILL}"            text-anchor="middle">{RUN_DESCRIPTION}</text>
```

`{ROW_FILL}` is `var(--text-secondary)` for ampacity_pct < 70%, `var(--warn)` (with `class="bold-text"`) when ≥ 70% — flag upsized runs that may need a larger gauge.

### Fuse-margin table (M1)

Drives from `manifest.components` where `type == "fuse-vertical"` or `type == "fuse-horizontal"`. Required fields per fuse: `fuse_rating` (A), `steady_load` (A), `margin_ratio` (= `fuse_rating / steady_load`).

Per-row template:

```svg
<text x="{X_ID}"     y="{ROW_Y}" font-size="11" fill="var(--accent)"       text-anchor="middle" class="bold-text">{FUSE_ID}</text>
<text x="{X_RATING}" y="{ROW_Y}" font-size="11" fill="var(--text-primary)" text-anchor="middle">{FUSE_RATING} A</text>
<text x="{X_LOAD}"   y="{ROW_Y}" font-size="11" fill="var(--text-secondary)" text-anchor="middle">{STEADY_LOAD} A</text>
<text x="{X_MARGIN}" y="{ROW_Y}" font-size="11" fill="{MARGIN_FILL}"        text-anchor="middle" class="bold-text">{MARGIN_RATIO}×</text>
```

`{MARGIN_FILL}` is `var(--text-primary)` when `margin_ratio ≥ 1.5`, `var(--warn)` when `< 1.5`. Fuses with `margin_ratio < 1.5` also get `is_critical = true` auto-stamped on their manifest component entry (drives BOM critical-row highlighting via Sub-Agent 10).

### Notes panel (M2)

Drives from `manifest.notes` (top-level). Container shared with revision history at the `notes-rev` panel slot (default `x=1350 y=1080 w=650 h=600`). Title `NOTES` at y=1102. Per-note vertical pitch: 40 px for 2-line notes, 55 px for 3-line notes (see Scent Controller §16 layout).

Per-note pattern uses `snippets/note-numbered.html`:

```svg
<text x="1365" y="{NOTE_Y}" font-size="12" fill="{NOTE_FILL}" class="bold-text">
  <tspan fill="var(--text-primary)">{N}.</tspan> {LINE_1}
  <tspan x="1380" dy="14">{LINE_2}</tspan>
  <tspan x="1380" dy="14">{LINE_3}</tspan>
</text>
```

`{NOTE_FILL}` is `var(--text-secondary)` for standard notes, `var(--warn)` when `manifest.notes[i].is_warning == true`. The number prefix (`<tspan>`) stays at `var(--text-primary)` regardless.

### Common rules

- All bottom-panel containers inherit `data-info` from `manifest.bottom_panels[*].data_info` if present (L5).
- If a pinout / gauge / fuse field is incomplete, emit `CONSULT → Datasheet Researcher` before drawing.

**Tools to read:** `snippets/harness-table.html`, `snippets/note-numbered.html`, `reference/tables.md`

---

## Sub-Agent 6 — Wire Router

**Called by:** Orchestrator after Harness-Table Builder
**Input:** Layout Manifest (nets section) + assembled component coordinates
**Output:** `<line>`, `<polyline>`, and `<path>` wire SVG elements

### Routing rules
1. **Orthogonal only** — all wire segments must be horizontal or vertical.
2. **Arc hop at every cross-over across ALL net types** (GND, 12V, 5V, 3V3, every data channel). Unconnected crossings require a 5 px-radius arc `<path>` over the crossing wire. Bare crossings ≡ electrical connection — only allowed when an electrical junction is intended (and then a junction dot is also added). Arc syntax: `a 5,5 0 0,0 10,0` for a left-to-right horizontal that bumps upward (the standard convention); `a 5,5 0 0,1 0,10` for a top-to-bottom vertical that bumps right. The bump direction should be AWAY from the wire being crossed when net hierarchy differs (bus on top, branch on bottom → branch hops up over bus).
3. **Parallel spacing** — wires on different nets sharing a channel must offset by ≥ 8 px; shared segment = joined nets.
4. **No body overlap** — no wire segment may pass through a component body `<rect>`.
5. **Stroke width** by wire type:
   - Bus trunk: `stroke-width="4"`
   - Primary power branch: `stroke-width="2.5"`
   - Data / secondary: `stroke-width="2"`
6. **Color** from manifest `wire_class` (e.g. `class="w5v"` or `stroke="var(--wire-5v)"`).
7. **Junctions** — add a `<circle>` (r = 4.5 major power, r = 3.5 secondary power, r = 3 pin/data, r = 2.5 minor signal) at every T-junction or pin landing. See `reference/conventions.md` §Dot radius hierarchy.
8. **Ground connections** — GND pins must connect to the common ground bus with a wire. Exception: when routing would cross a congested area, place a GND symbol (`⏚` text label, `fill="var(--wire-gnd)"`) directly adjacent to or below the component pin instead.
9. **Universal clearance (VR1)** — every drawable object must be ≥ 10 SVG units apart from every other object, edge-to-edge. Violations are FAIL, not WARN.
10. **Net color follows signal, not voltage (VR9)** — once a net is assigned a wire class, that class applies to ALL segments of that net. Exception: the always-hot supply wire upstream of a MOSFET (PSU/fuse → drain, before the switch) keeps `.w12v`; only the switched drain side takes the GPIO color. CLAUDE.md Wire Assignment Table, if present, is binding.
11. **Series component through-wires** — for every two-terminal in-line component (fuse, resistor in-line, jumper) whose `<rect class="comp">` has `fill:none`, a `<line>` of the routed net's wire class MUST connect the two terminal coordinates through the component body. Without it, the wire visually breaks at the box edges. Apply to: fuses (F_MAIN, F1–F6 family), in-line resistors, dummy jumpers.
12. **Shunt component bypass** — for every two-terminal component placed ACROSS a net (RC snubbers, decoupling caps, pull-ups landing on a bus), the routed net's wire MUST pass alongside the component, not through it. Tap stubs branch from the wire to each terminal. No through-wire inside the body.

If Wire Router encounters an unallocated net, emit `CONSULT → Net Color Allocator`.

**Tools to read:** `reference/conventions.md`

---

## Sub-Agent 7 — Revision Manager

**Called by:** Orchestrator for `EDIT_REVISION` only.
**Input:** path to the existing project HTML + the requested delta (e.g. "add a MAX485 between U1 and J3")
**Output:** revised HTML with revision metadata bumped

### Steps
1. Read the existing project HTML (NOT `skeleton.html`).
2. Parse current `<title>` and the title-block `Rev X.Y` text.
3. Bump:
   - Patch revision for fixes/swaps (`Rev 1.0` → `Rev 1.1`)
   - Minor revision for added or removed parts (`Rev 1.x` → `Rev 1.(x+1)` or `Rev 2.0` if user requests major)
4. Append a new row to the revision-history block in the bottom panel (date, rev, change summary).
5. **Legend-strip refresh (M4)** — if the delta adds or removes a channel (any `wdataN` class enters or leaves use), update `manifest.legend_entries` to match the new set of wire classes and re-invoke Sub-Agent 4 rule 10 to rewrite the title-block legend strip. Pure pixel-nudges and resizes do NOT trigger this — only changes that affect `manifest.nets[*].wire_class` membership.
6. Hand the parsed component map + pending delta to Layout Planner so downstream agents work on the existing layout, not a fresh canvas.

### Pixel-nudge edits (sub-intent of EDIT_REVISION)

> **📐 Pixel-nudge grammar — first letter = direction**
>
> | Input              | Direction | Effect  |
> |--------------------|-----------|---------|
> | `l10px` · `l10` · `L10` · `left 10px`   | left  | x −= 10 |
> | `r20px` · `r20` · `R20` · `right 20px`  | right | x += 20 |
> | `u5px`  · `u5`  · `U5`  · `up 5px`      | up    | y −= 5  |
> | `d8px`  · `d8`  · `D8`  · `down 8px`    | down  | y += 8  |
>
> Case-insensitive. `px` suffix optional. Verbose forms ("left 10px", "down 8") parse identically to short forms. Coordinate frame = the SELECTED element's local frame.
>
> **Scaled-parent math (C3):** when the selected element lives inside a `<g>` whose component manifest entry has `transform_scale: [sx, sy]`, the user's pixel value is interpreted in SCHEMATIC units and converted to local units before being applied: `local_delta_x = schematic_delta_x / sx`, `local_delta_y = schematic_delta_y / sy`. Example: `d10px` inside U1's `scale(0.8539, 0.8)` group applies a vertical delta of `10 / 0.8 = 12.5` local units to the element's `y`/`cy`/path. If the selection is outside any scaled `<g>`, sx=sy=1 (no conversion). Always also update any `schematic_pins` entry that references the moved local pin — the schematic-frame pin coords stay in schematic units.

When the user issues such a directive against a selected element, Revision Manager handles it as a single-element coordinate translation without bumping the revision number (it's a visual polish edit, not a part change).

**Direction parsing reference:** `u`/`up` = −y, `d`/`down`/`D` = +y, `l`/`left` = −x, `r`/`right` = +x. Numeric suffix = pixel delta in the selected element's coordinate frame.

**Dependent-element tracking — REQUIRED before applying:**

Build the coupling set for the selected element. For each coordinate that changes, find every other element that references the same coordinate:

| Selected element type | Find and update together |
|---|---|
| Wire `<line>` endpoint at (x,y) | Every other `<line>`/`<path>` starting/ending at (x,y); junction `<circle>` at (cx=x, cy=y); pin `<circle>` at (cx=x, cy=y); text label whose baseline is within 8 px |
| Component `<g>` (whole-component move) | All children with absolute coordinates; ALL wires terminating on any pin of the component; nearby labels referencing the component |
| Junction `<circle>` | The wires whose endpoints land on it; sibling junctions on the same bus |
| Text label near a wire | Just the label (clearance check via VR8 — see Validator) |
| Pin `<circle>` | The wire(s) that terminate at it; the pin-name `<text>` placed alongside |

**Verification after every nudge:** the same preview server stays running; reload via `window.location.reload(true)`, then `preview_eval` a DOM query to confirm the new attribute values BEFORE taking a screenshot (screenshots are expensive; attribute checks are cheap).

**`data-info` on new wire fragments** — when a nudge spawns a new `<line>` or `<path>` (arc hop, jog stub, through-wire bridging two endpoints, RC bypass tap), the fragment MUST inherit `data-info` from the parent net's existing wires, formatted as 3 pipe-separated fields:

```
data-info="NET_ID|segment role|gauge or voltage"
```

- `NET_ID` — the same net identifier used by upstream segments (e.g. `12V_ESP`, `SW_A1`, `GND`).
- `segment role` — a short noun phrase describing this fragment's purpose (`through F2`, `U2.VOUT stub`, `RC1 NO tap`, `→ F3 in`).
- `gauge or voltage` — the wire-gauge or rail tag (`22 AWG RED`, `18 AWG BLACK`, `signal`, `switched 5V to A1`). If the parent's existing segments use a longer descriptor in this slot, copy it verbatim.

Never emit `data-info="NET|role|"` with an empty third field — the hover tooltip renders as a blank line. If unsure of the gauge/voltage, look up the closest upstream `<line>` on the same net and copy its third field.

### Container-resize edits (sub-intent of EDIT_REVISION)

When a directive changes the `width` / `height` of a component `<rect>` (e.g. `RC1 width=80`, or a multi-text auto-fit re-run after a font-scale), re-anchor every child element that references the box:

| Child element | Re-anchor rule |
|---|---|
| `<text>` middle-anchored near the box center | `x → new rect.cx`; multi-text baselines redistribute per Sub-Agent 4 rule 9 |
| `<text>` end-anchored on the left edge | `x = new rect.x − pad` (preserve original padding) |
| `<text>` start-anchored on the right edge | `x = new rect.x + new rect.width + pad` |
| Pin `<circle>` on a box edge | Stays on the same edge; only the axis that grew shifts |
| `<line>` / `<path>` terminating on a pin | Endpoint follows the pin |

**Cumulative-shift rule:** if `rect.y` is unchanged but `height` grows by Δh, only bottom-anchored children shift by +Δh; top-anchored children stay. Same for `width` growth on the right edge.

If the resized component carries a `channel_group` tag (see Channel-group propagation below), the same resize auto-applies to all sibling channels with the inter-row Δy preserved — unless the directive ends with the `--solo` flag.

### Channel-group propagation (sub-intent of EDIT_REVISION)

Many schematics contain symmetric channel iterations — `RC1, RC2, RC3, RC4` snubbers, `F3, F4, F5, F6` per-channel fuses, `A1..An` driver boards, `LED1..LEDn` indicator banks. When the Layout Planner stamps a `channel_group` on these (either via explicit manifest field or via auto-detection — see Sub-Agent 1), Revision Manager treats any nudge, resize, or font-scale on one member as an edit to the entire group.

**Behavior:**
- A directive like `RC1 width=80` resizes RC1 AND propagates the same `width=80` to RC2, RC3, RC4. Inter-row Δy (vertical spacing between channel rows) is preserved.
- A pixel-nudge on the group's first member (e.g. RC1 `r10`) shifts every group member by the same Δx; Δy nudges similarly propagate.
- A font-scale on one text in one channel propagates to the same-role text in every other channel of the same group (matched by relative position inside the parent `<g>`).

**Override:** append `--solo` to the directive to touch only the selected member (e.g. `RC1 width=80 --solo`).

**Empty-group safety:** if `channel_group` is set but `channel_index` differs across members in a way that breaks the symmetric-iteration assumption (gaps, duplicates), Revision Manager emits `BLOCKED: channel_group "RC" has non-contiguous indices` and refuses to propagate.

### REVERT_LAST sub-intent

**Triggers:** "reverse this step", "undo last edit", "revert that", "undo", "undo last".

**Behavior:** pop the most recent `(file, old_string, new_string)` triple from the session edit-log and apply `Edit(old_string=new_string, new_string=old_string)`. No revision-number bump (it's an undo, not a change).

If the edit-log for the current session is empty, return `BLOCKED: nothing to revert`. Revert does not chain — to undo multiple steps, the user must issue "reverse this step" once per step (or "undo last 3" if a multi-step grammar is added later).

### Font-scale sub-intent

**Triggers:** "smaller font (0.5x)", "bigger 1.5x", "0.75x font", "2x larger", etc., issued against one or more selected `<text>` elements.

**Behavior:** `new_font_size = round(old_font_size × factor)`. Clamp to `6 ≤ new ≤ 24`. If the computation falls below 6, clamp to 6 and emit `WARN: clamped to floor 6 px (was N px)`. Integer only — no fractional `font-size`. No revision-number bump.

When applied to a text inside a component whose container follows the multi-text auto-fit rule (Sub-Agent 4 rule 9), trigger the resize rule above to re-fit the container.

---

## Sub-Agent 8 — Style Validator

**Called by:** Orchestrator after Wire Router (always runs before final output)
**Input:** Assembled schematic HTML string
**Output:** Validation report (PASS / WARN / FAIL per rule) + auto-corrected HTML

### Validation checklist

**Token contract (23 required CSS vars in `:root`):**
```
--bg-dark  --bg-panel
--wire-12v  --wire-5v  --wire-3v3  --wire-gnd
--wire-data  --wire-data2  --wire-data3  --wire-data4
--wire-data5  --wire-data6  --wire-data7
--text-primary  --text-secondary  --accent
--comp-fill  --comp-fill-hover  --comp-stroke  --border  --pin-dot
--warn  --warn-bg
```
→ FAIL if any token is missing from `:root`. `--comp-fill` / `--comp-fill-hover` may be `none` but the names must still exist.

**Stroke width hierarchy:** 4 / 2.5 / 2 / 1.5 / 1 / 0.5 / 0.3 — WARN on any other value
**Dot radius hierarchy:** 4.5 / 3.5 / 3 / 2.5 — WARN on any other value
**No hardcoded hex** — grep `#[0-9a-fA-F]{3,6}` in SVG attributes → FAIL if found
**Token name consistency (skeleton.html only)** — applies to the final exported `skeleton.html`. No source-namespace tokens (`--cp-*`, `--mb-*`, `--np-*`, `--cb-*`, `--pl-*`, `--en-*`, `--mp-*`, plus any future `--xx-*`) may appear in skeleton.html's `:root`; only contract-namespace tokens (`--bg-*`, `--wire-*`, `--text-*`, `--comp-*`, `--accent`, `--border`, `--pin-*`, `--warn*`) are allowed. Theme source files under `reference/themes/` are exempt. → FAIL.
**Container fill rule** — `<rect>`/`<polygon>` that wraps component text/labels, or carries `class="comp"` / `class="sec-border-dash"`, must have `fill="none"` or a CSS class whose `fill` is `none`. Header/footer panel backgrounds (legend, BOM card, revision-history card) may use `fill="var(--bg-panel)"`. Junctions and pin dots exempt. → FAIL.
**VR1 universal clearance** — non-intersecting pairs must be ≥ 10 SVG units apart edge-to-edge. Elements inside a transformed `<g>` (translate/scale) have their bbox composed into the schematic frame before clearance math (see validator-spec § VR1). → FAIL.
**VR2 axis alignment + grid** — wire segments horizontal/vertical only; component `<rect>` no rotate transform; `<polyline>` vertices on a 10-unit grid. Arc-hop paths exempt. → FAIL.
**VR3 no-overlap (topology)** — wire segment vs `<text>` / `<rect class~="comp">` bbox intersection. Same transformed-group bbox composition rule as VR1. → FAIL.
**VR4 tooltip presence and content** — `[data-info]` on every `<line>`, `<polyline>`, `<path>`, component `<g>`, junction `<circle>`. Field count and content depend on element type:

| Element type | Required fields | Format |
|---|---|---|
| Wire `<line>` / `<polyline>` / `<path>` | exactly 3 | `NET_ID\|segment role\|gauge or voltage` (e.g. `GND\|PSU return trunk\|18 AWG BLACK`) |
| Component `<rect class~="comp">` (id resolved via parent `<g id="...">`) | 3 or 4 | `ComponentID\|brief\|spec` and optional `\|note` (e.g. `PSU1\|DC industrial PSU\|12 V · 8.2 A · DIN rail\|Oversized — 2–3 A would suffice`) |
| Junction `<circle>` (j*) | 2 or 3 | `NET_ID\|junction role` and optional `\|note` |

→ FAIL on missing `data-info` attribute. → FAIL when field count is outside the allowed range for the element type. → FAIL on any field that is empty or whitespace-only (catches `"NET\|role\|"`).

**Auto-fix during EDIT_REVISION nudges:** when Wire Router adds a new wire fragment (arc hop, jog stub, through-wire bypass tap), it inherits the parent net's `NET_ID` and the parent net's most-common gauge/voltage tag for the third field. Field 2 (role) must be authored — defaults to the segment's geometric description (`through {COMPONENT_ID}`, `{COMPONENT_ID} stub`, `arc-hop over {OTHER_NET}`). The validator does not auto-generate field 2 if it's missing — that's a FAIL with `BLOCKED: need user input`.
**VR5 wire/bg contrast** — every `--wire-*` vs `--bg-dark`, WCAG ratio ≥ 3:1. → FAIL.
**VR6 BOM format** — pure-SVG `<g class="bom-panel">` container; column header `<text>` cells in order `# / QTY / REF / DESCRIPTION`; every `<rect class~="comp">` designator present in exactly one REF-column cell; Item# contiguous 1-based; row baselines aligned across the 4 cells. → FAIL.
**VR7 channel identification** — (a) every wire class used in the body has a swatch+label entry in the title-block legend strip; (b) every named non-rail data net surfaces as ≥1 `<text>` annotation somewhere in the schematic body. Power rails (`w12v`/`w5v`/`w3v3`/`wgnd` + `-bus` variants) need only the legend swatch. `<text class="channel-label">` is optional/decorative as of v4.0. → FAIL.
**VR8 text clear-space** — for every `<text>` element, its rendered bbox (use `getBBox()` post-render, or estimate as `length × font-size × 0.55 + 2` px wide and `font-size + 2` px tall around the baseline) must be ≥ 5 px from:
  (a) every `<line>` / `<path>` centerline not labeling that wire's own net (use `data-info` or shared parent `<g>` as the same-group test), and
  (b) every `<circle class="pin">` / `<circle class="j*">` not anchored to the labeled net.
→ FAIL. Common fix: nudge the text baseline 5–8 px away from the nearest wire centerline along the orthogonal axis.
**VR8b intra-container text spacing** — stacked `<text>` nodes sharing a parent `<g>` (same `text-anchor`, `x` within ±4 px) must keep a ≥ 3 px bbox-edge-to-bbox-edge vertical gap. → **WARN** (not FAIL) — runtime safety net for Sub-Agent 4 rule 9's build-time multi-text auto-fit. **Algorithm in `reference/validator-spec.md`.**
**VR9 net color consistency** — cross-check every wire class against working-dir CLAUDE.md "Wire Assignment Table" if present. → FAIL on mismatch.
**VR10 arc-hop coverage** — arc-hop `<path>` within ±6 px of every wire-vs-wire crossing of different nets without a junction. → FAIL. Validator may emit `CONSULT → Wire Router` for a single auto-fix retry per failure.

**Algorithm details for VR1–VR10:** see [`reference/validator-spec.md`](reference/validator-spec.md). Sub-Agent 8 reads both this checklist (high-level contract) and the spec (algorithmic procedure with inputs, pseudocode, edge cases, and failure messages).

---

## Sub-Agent 9 — Export Specialist

**Called by:** Orchestrator for `THEME_SWITCH` and `EXPORT_TUNE`; consulted on demand by other agents about color/export rules.
**Input:** target theme name OR export-rule change
**Output:** updated `:root` block and/or updated `getSvgStringPrint()` / `getSvgStringThemed()` functions

### Export contract (must be preserved)

- **Export SVG button** → calls `getSvgStringPrint()` → black strokes, black text, transparent background, no `<rect>` background, `!important` overrides on every themed class. For print/embed.
- **Export PNG button** → calls `getSvgStringThemed()` → themed visual matching the on-screen schematic.

**Print-mode selector strategy (M6).** `getSvgStringPrint()` uses attribute selectors (`[class*="wdata"]`, `[class^="j"]`, `[class*=" j"]`) rather than enumerated class lists, so new wire classes (e.g. adding `--wire-data8` + `.wdata8` to extend beyond the 7-channel default) are picked up automatically with no edit to the print CSS. Do NOT add new hard-coded `.wdata8, .wdata9, …` lines to the print block — the attribute-prefix selector covers them.

### Theme remap (THEME_SWITCH mode)

Each theme defines its own remap table from its source namespace (e.g. `--cp-*`, `--mb-*`) to the schematic contract names. The Export Specialist reads the target theme file's table, then writes the contract `:root` block into `skeleton.html` between the `/* === THEME START === */` markers. Source-namespace tokens MUST NOT appear in the exported skeleton.html (enforced by the token-name-consistency rule in the validator checklist above).

**Available themes** (canvas type in parens):

| Theme | Canvas | Source namespace | File |
|---|---|---|---|
| Cyberpunk *(default)* | dark | `--cp-*` | `reference/themes/Color-Palette_Cyberpunk-theme.md` |
| Dark Teal | dark | *(none — contract-only)* | `reference/themes/Color-Palette_Dark-Teal-theme.md` |
| Midnight Blue | dark | `--mb-*` | `reference/themes/Color-Palette_Midnight-Blue-theme.md` |
| Nebula Pop | dark | `--np-*` | `reference/themes/Color-Palette_Nebula-Pop-theme.md` |
| Cobalt Pop | dark | `--cb-*` | `reference/themes/Color-Palette_Cobalt-Pop-theme.md` |
| Editorial Navy | dark | `--en-*` | `reference/themes/Color-Palette_Editorial-Navy-theme.md` |
| Prism Light | **light** | `--pl-*` | `reference/themes/Color-Palette_Prism-Light-theme.md` |
| Mosaic Pastel | **light** | `--mp-*` | `reference/themes/Color-Palette_Mosaic-Pastel-theme.md` |

Light-canvas themes invert every `--wire-*` default that would be white (Prism Light → `#212121`, Mosaic Pastel → `#4A5258`). The Export Specialist must preserve this inversion; VR5 catches any regression. Dark Teal has no source namespace — its `:root` already uses contract names.

**Tools to read:** `reference/tokens.md`, `reference/themes/Color-Palette_<Theme>-theme.md`.

---

## Sub-Agent 10 — BOM Specialist

**Called by:** Orchestrator after Component Assembler (in parallel with Harness-Table Builder); consulted on demand by Revision Manager when components are added/removed.
**Input:** Layout Manifest §components (and §parts if a separate parts catalog exists)
**Output:** populated **pure-SVG** row blocks inside the `<g id="bom-panel" class="bom-panel">` container in skeleton.html. Each row = 4 `<text>` cells at a shared y-baseline + 1 `<line>` separator. **No `<foreignObject>`, no HTML `<table>`.**

### Procedure

1. Read every entry in manifest §components.
2. Group by `(part, package, value, tolerance, rating)` — components matching on all five collapse into one BOM row.
3. Within each group, sort designators by letter then number (`R1, R2, R3` not `R1, R10, R2`). Contiguous numeric ranges may collapse to `A1–A4` form (use the en-dash `U+2013`).
4. Sort groups by designator letter prefix, then by first numeric designator within letter — passive parts first (C, D, J, L, R), then active (Q, U), then misc.
5. Assign Item# as a contiguous 1-based sequence in the sorted group order.
6. Build Description: `{value} {package}` + (` {tolerance}` if set) + (` {rating}` if set). Use Unicode units (`kΩ`, `µF`, `°C`). Fall back to `part` if `value` is absent.
7. Compute row y-baselines: first row `y = 1143`, pitch `16 px`. Total panel height grows with row count — update the outer `<rect>` height and the column-divider `y2` to `1108 + 20 + ROW_COUNT × 16 + 20`.
8. Emit one row block per group. Standard row:
   ```svg
   <text x="60"  y="{ROW_Y}" font-size="10" fill="var(--text-primary)" text-anchor="middle">{N}</text>
   <text x="105" y="{ROW_Y}" font-size="10" fill="var(--text-primary)" text-anchor="middle">{QTY}</text>
   <text x="195" y="{ROW_Y}" font-size="10" fill="var(--accent)"       text-anchor="middle" class="bold-text">{REF}</text>
   <text x="268" y="{ROW_Y}" font-size="10" fill="var(--text-primary)">{DESCRIPTION}</text>
   <line x1="80" y1="{ROW_Y+5}" x2="655" y2="{ROW_Y+5}" stroke="var(--comp-stroke)" stroke-width="0.3" opacity="0.4"/>
   ```
9. **Critical-row highlighting (M5):** when the manifest component has `is_critical=true` (auto-true for fuses where `margin_ratio < 1.5`), every cell in that row uses `fill="var(--warn)"` and adds `class="bold-text"` (replacing the default fills above). The REF cell already has `class="bold-text"` — leave that. The row separator stays at `var(--comp-stroke)`.
10. Insert all emitted row blocks inside the existing `<g id="bom-panel">` placeholder, after the column-divider lines. **Do NOT regenerate the container `<g>`, outer `<rect>`, title, header band, or column dividers** — those are skeleton-owned and VR6 enforces their presence.
11. If a component's `value` is missing AND `part` looks generic (e.g., "Resistor", "Capacitor" with no value), emit `CONSULT → Datasheet Researcher` with the component id + part name.

### Rules

- Item# stability across revisions: a BOM row that already exists in a prior revision keeps its Item#. New groups append at the end with the next free Item#. Removed groups leave a gap — the Revision Manager re-sequences only if explicitly requested via `RENUMBER_BOM` intent.
- No row may have Qty < 1.
- A single designator may appear in only one row (VR6 enforces uniqueness; ranges expand for the uniqueness check).
- Decorative-only components (`class="deco"`) are exempt from the BOM.
- Row baselines must align across the 4 cells (±1 px) so VR6's row-grouping pass works unambiguously.

### Tools to read

- `reference/tables.md` § BOM section (the structural contract — geometry, columns, critical-row pattern)
- `reference/validator-spec.md` § VR6 (the validation algorithm — for self-check before handoff)

### Common consult patterns

- BOM Specialist → Datasheet Researcher (missing value/rating for an unidentified part)
- Revision Manager → BOM Specialist (a component was added/removed/swapped; emit updated rows)

---

## Reference files

| File | Load when… |
|---|---|
| `reference/tokens.md` | Color token names, font weights, letter-spacing values |
| `reference/conventions.md` | Units, primitive selection, stroke widths, dot radii, glyphs, fill-vs-outline rule, arc-hop variants, VR-number index |
| `reference/tables.md` | GPIO map, BOM list, revision history, wire-gauge, harness-table patterns, wire channel labels |
| `reference/validator-spec.md` | Algorithmic specs for VR1–VR10 (Inputs / Procedure / Edge cases / Failure messages). Read alongside SKILL.md validator checklist, which states the high-level contract for each rule. |
| `reference/themes/Color-Palette_*-theme.md` | One file per theme. See the Export Specialist § Available themes table for the full list (8 themes, dark & light). Load only the file matching the requested `THEME_SWITCH` target. |

Default theme is **Cyberpunk** (`reference/themes/Color-Palette_Cyberpunk-theme.md`). All other themes are opt-in via `THEME_SWITCH`. VR8 enforces text clear-space (added in v3.1).

---

## Source of truth

The skill is the source of truth for the **VR\* validator rules** (VR1–VR10) — the machine-enforceable checks that Sub-Agent 8 runs on the assembled HTML.

The master at `Claude Working Folder\Hubble Engineering - Document Style Guide\HTML_Schematic_Style_Guide\HTML_Schematic_Style_Guide.md` is the source of truth for **DR\* drawing rules** (DR1–DR8) — the human-readable conventions for laying out a schematic (box clearance, pin exits, polarity, label-obstruction, etc.).

The two rule sets are intentionally disjoint:
- **DR\*** = human design intent (how a person should draw a schematic)
- **VR\*** = machine validation (how the validator catches issues a person missed)

Sync direction:
- Changes to **DR\*** rules live in the master. `reference/conventions.md` may reference them but does not own them.
- Changes to **VR\*** rules live in the skill (`SKILL.md` validator checklist + `reference/validator-spec.md`). The master need not mention VR\* rules; they're machine-side.

The skill exists in two synchronized copies:
- Authoring: `Claude Working Folder\Claude Skills\HTML-schematic\`
- Installed (runtime): `~/.claude/skills/html-schematic\`

After any edit, mirror authoring → installed and `fc /b` (or `cmp -s`) to confirm parity.
