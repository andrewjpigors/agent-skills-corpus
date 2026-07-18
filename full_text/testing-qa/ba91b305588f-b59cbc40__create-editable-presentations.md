---
name: create-editable-presentations
description: Create source-grounded editable presentations from documents, URLs, notes, data, transcripts, reports, existing HTML, or ideas. Use when Codex needs to analyze sources, design a storyline, author canonical fixed-size HTML/CSS slides, run fidelity and editability QA, and deliver an editable PowerPoint or directly create native Google Slides.
---

# Editable Presentation Studio

Create an end-to-end presentation deliverable: analyze source material or an idea, design the narrative, author a polished fixed-size HTML/CSS deck, run QA, then export a visually faithful editable PowerPoint or create a native Google Slides deck directly from a connector-ready build plan.

This is a presentation-authoring skill, not merely an HTML converter. The HTML/CSS deck and its Chromium render are the canonical visual design. Existing HTML conversion remains supported, but it is secondary to the source-to-presentation workflow.

This skill is standalone. Do not require, load, install, or patch the Visualize skill. Borrow only the broad front-door idea of turning content into a polished visual artifact; keep every deck export-safe with fixed `1280x720` slides.

## Core Model

Use HTML/CSS as the canonical visual design and Chromium as the layout engine.

1. Analyze source material before writing HTML.
2. Design a slide-by-slide storyline.
3. Author one self-contained, presentation-quality fixed-size HTML deck.
4. Classify slide objects as editability `required`, `preferred`, or `visual` and add stable object IDs.
5. Recreate supported business objects natively by default; rasterize only unsupported or fidelity-sensitive visual regions.
6. Run content, visual, fidelity, editability, and export QA gates.
7. Deliver the requested target: editable PowerPoint, direct native Google Slides, or both as separate outputs.

Apply quality priorities in this order:

1. Source accuracy and storyline quality.
2. Canonical HTML/Chromium design quality.
3. Exported PowerPoint or direct Slides fidelity to the canonical Chromium render as a hard gate.
4. Semantic native coverage maximized among outputs that pass the fidelity gate.

Never simplify or flatten a strong presentation design merely to raise the raw native-object count. If a complex effect cannot be reproduced faithfully, keep the smallest practical visual region rasterized while preserving editable text, data, and simple business geometry around it.

For the primary PowerPoint deliverable, every visible user-facing text string is a hard native requirement. Raster regions may preserve decoration but must contain no readable text. Every semantic chart must emit as a native PowerPoint chart backed by editable chart data; a missing or unsupported chart spec blocks the primary editable export instead of permitting a silent raster chart fallback.

PowerPoint export modes:

- `hybrid`: CSS-rendered visual regions plus editable native objects. Use by default with the `powerpoint-editable` policy.
- `image`: each slide is a full-slide screenshot. Use for fidelity comparison or a separate preview copy.
- `native`: only native PPTX objects. Use as an experiment, not as permission to damage the design.

Never claim a hybrid deck is fully editable. Report which required or preferred objects remain rasterized and why.

For direct Google Slides, do not route through a PPTX. Generate the `google-slides-native` plan, create a blank native Slides file, and use structured Slides `batchUpdate` requests. A transparent full-slide underlay may preserve CSS-only decoration and fidelity exceptions, while required text and supported business geometry remain native above it. Load `references/google-slides-native.md` for the full resolver, connector, chart, and verification contract.

## Mandatory Workflow

### 0. Intake

- Determine audience, purpose, output type, language, slide count, and editability needs.
- If details are missing, infer practical defaults and keep moving.
- Use source material already present in the conversation. Do not invent placeholder data when real content exists.
- Existing HTML decks are valid secondary input; skip source analysis and storyline design only when the user explicitly asks for conversion only.

### 1. Source Analysis

Read all provided source material: URLs, PDFs, documents, reports, articles, pasted notes, meeting transcripts, CSV/JSON/table data, screenshots with text, or vague deck requests.

Extract an internal evidence map before authoring slides:

- core thesis
- key facts
- numbers and metrics
- named entities
- chronology
- stakeholders
- tensions and risks
- recommended actions
- source-backed claims
- missing or uncertain data

Load `references/source-analysis.md` for source-specific extraction rules.

### 2. Storyline Design

Choose an audience-appropriate narrative arc before writing HTML; use `references/storyline-design.md` for the supported briefing, recommendation, dashboard, comparison, roadmap, and process patterns.

Create a slide plan with:

- slide title
- single takeaway
- supporting evidence
- visual pattern
- editability-required elements
- editability-preferred elements
- visual-only elements
- fidelity-locked elements whose appearance must not be approximated
- speaker/source notes when useful

Load the same reference for the full slide planning contract.

### 3. HTML Deck Authoring

Create one self-contained HTML file. Every slide must be a fixed slide container:

```html
<section class="slide" data-pptx-slide aria-label="Executive Summary">
  <!-- slide content -->
</section>
```

Use this 16:9 default unless the user requests another size:

```css
.slide {
  width: 1280px;
  height: 720px;
  position: relative;
  overflow: hidden;
}

@page {
  size: 13.333333in 7.5in;
  margin: 0;
}
```

Authoring rules:

- Use fixed `1280x720` layout; do not depend on responsive viewport behavior.
- Treat the Chromium render of the HTML/CSS as the canonical visual reference for PDF, PPTX, and direct Google Slides QA.
- Give each meaningful export object a stable `data-deck-id`.
- Use `data-deck-native` for the intended native object type and `data-deck-editability="required|preferred|visual"` for its priority. Legacy `data-pptx-*` attributes remain accepted aliases.
- Make supported business objects native by default: titles, body text, labels, metrics, callouts, solid cards, simple shapes, dividers, connectors, process blocks, tables, and images. Charts with explicit data are native PowerPoint charts; direct Slides charts require an explicitly authorized linked-Google-Sheets workflow or a target-specific primitive renderer that passes fidelity QA.
- Keep complex gradients, glows, blur, masks, dense SVG/canvas visuals, and exact image crops in the smallest practical raster region.
- Do not redesign a slide into simpler geometry solely to increase native coverage.
- Use Korean-safe typography when Korean content is present: `Pretendard`, `"Noto Sans KR"`, `"Malgun Gothic"`, Arial, sans-serif.
- Preserve citations and source notes in a consistent footer or source slide.

Load `references/deck-skeleton.md` when starting a new HTML deck. Load `references/slide-patterns.md` when choosing slide layouts.

### 4. Pre-export QA

The HTML deck must pass these gates before export:

Content QA:

- every slide has one clear takeaway
- no placeholder text, lorem ipsum, or fake numbers
- important claims are source-backed or marked as assumptions
- storyline order is coherent
- uncertainty and missing data are visible where material

Slide QA:

- no text overflow or clipped content
- no visible text escaping outside chips, cards, buttons, badges, or other bounded boxes
- no visible text collisions between titles, takeaways, cards, footers, or labels
- repeated card or row groups have comfortable parent-panel edge insets
- chart marks, labels, and callouts stay inside the visible chart panel; do not mix SVG/viewBox coordinates with slide-level coordinates
- nested KPI cards or repeated components have dimensions tuned for their parent panel, not inherited from a larger hero/card pattern
- readable font sizes
- consistent footer/source-note system
- each slide fits `1280x720`
- deck-wide typography, palette, and spacing are consistent

Target editability QA:

- every `required` object has a stable `data-deck-id`, a supported target-native representation, and a target-specific emitted or planned native object
- titles, key business text, metric values, labels, callouts, and recommendations are editable
- simple solid cards, dividers, connectors, and process blocks are native when their Chromium appearance can be matched
- simple tables are native or editable boxy cells; PowerPoint-editable charts include explicit chart JSON, while required direct-Slides charts need an explicitly authorized linked Sheets workflow
- `preferred` objects fall back to raster only for a recorded fidelity or capability reason
- `visual` and fidelity-locked regions are intentionally rasterized at the smallest practical scope

PowerPoint export QA, only when PowerPoint/PDF is requested:

- PDF exists
- PDF pages have been visually inspected after export, not only HTML screenshots
- hybrid PPTX exists
- final PPTX has been visually rendered or opened after export, not only the `*-hybrid-slides-png/` debug backgrounds
- manifest exists
- manifest reports `authored`, `resolved`, and `emitted` states for identified objects
- manifest warnings and fallback reasons are inspected
- repair and re-export if warnings indicate drift, missing native objects, unsafe tables, unsafe charts, unexpected raster fallback, or PPTX render clipping/duplication

Direct Google Slides plan QA, only when Google Slides is requested:

- plan and referenced PNG assets exist; no PPTX was emitted or imported as an intermediate
- every request uses one supported official Slides request key, valid IDs, PT units, create-before-use ordering, and bounded geometry
- summary and native coverage are recomputed from the object ledger rather than trusted from a prefilled total
- each slide has one RGB/RGBA visual-underlay PNG with native candidates hidden; low transparency requires an explicit recorded visual-region or auto-text compatibility exception, and isolated chart/image raster assets are referenced exactly once
- each slide records a DOM capture audit whose hidden, paint-hidden, and explicitly kept counts account for every native candidate with zero violations
- `createSheetsChart` appears only when valid canonical chart JSON, explicit source attributes, and `--allow-linked-sheets-charts=true` are all present; record Google Sheets plus the spreadsheet/chart IDs as the structured chart-data edit surface
- required objects remain native; every preferred raster fallback has a reason
- local `qa.remoteStatus` remains `unverified` until connector execution, structure readback, and fresh LARGE thumbnail QA all succeed
- after execution, connector readback confirms page size, slide order, object IDs, and bootstrap-slide deletion, and fresh LARGE thumbnails pass visual comparison

Run the bundled HTML QA script before export when available:

```bash
node scripts/qa-html-deck.mjs path/to/deck.html
```

For real deliverables, generate and inspect full-render screenshots:

```bash
node scripts/qa-html-deck.mjs path/to/deck.html --screenshots=dist/full-render
```

Also generate PDF-export-style screenshots when the deck will be delivered as PDF or when the HTML uses slide-framework or animation classes:

```bash
node scripts/qa-html-deck.mjs path/to/deck.html --pdf-screenshots=dist/pdf-render-check
```

Do not use `*-hybrid-slides-png/` as the only visual QA surface. Those PNGs are background debug layers with native overlays hidden, so they can miss text collisions and final composition problems.

For PPTX deliverables, render or open the exported `.pptx` itself and inspect every slide. Hybrid decks are composed from a raster background plus native overlays; a background debug PNG can look blank by design, while the final PPTX may still have overlay drift, duplicate text, clipped tables, or off-slide content. Treat slide-level clipping, doubled text, missing right-side panels, or objects pushed below the footer as blockers.

Do not treat HTML full-render screenshots as a substitute for exported PDF review. The exporter injects print/PDF CSS, and existing HTML decks can contain generic classes such as `.reveal` on ordinary cards as well as on framework containers. Always inspect the exported PDF pages when a real deliverable is requested, especially for two-column layouts, comparison cards, timeline panels, dashboards, and slides with many `data-deck-native` or legacy `data-pptx-native` overlays.

After export, run manifest QA so authored intent is reconciled with resolution decisions and actual emitted PPTX objects:

```bash
node scripts/qa-export-manifest.mjs path/to/deck.hybrid.manifest.json
```

Then validate the PPTX package itself. This catches duplicate PowerPoint object IDs, missing content-type parts, broken internal relationships, and native charts that lack a slide reference, `externalData` link, or valid embedded XLSX workbook:

```bash
node scripts/qa-pptx-package.mjs path/to/deck.hybrid.pptx
```

Treat a missing emitted object for any `required` ID, native text-character coverage below 100%, a semantic chart that was not emitted as a native chart, an unexplained preferred fallback, a claimed native object that was not emitted, or any package-integrity error as a blocker. These text and chart gates are enabled by default in `qa-export-manifest.mjs`.

The QA script also warns on repeated card groups that sit too close to a parent panel edge (`layout.group-spacing`). Fix by reducing row height/gap, moving the group, enlarging the parent panel, or marking intentional exceptions with `data-qa-spacing-ok="true"`.

It also warns when text extends outside a visible bounded box even if CSS `overflow` is still `visible` (`layout.visible-overflow`). Fix by shortening copy, widening the box, increasing height, reducing font size, or marking intentional exceptions with `data-qa-visible-overflow-ok="true"`.

It also warns when a `data-deck-native="text"` element has visible box styling such as background, border, or radius (`pptx.native-visual-loss`). Fix chips, badges, heatmap cells, and number pills with `data-deck-native="shape text"` plus explicit `data-pptx-margin-pt`/`data-pptx-valign` when needed, or split the visual box and native text into separate elements.

It also warns when a native container such as `shape` or `shape text` contains CSS-only child visuals (`pptx.native-container-visual-loss`). In hybrid export the whole native container is hidden from the raster background, so nested progress bars, styled spans, mini charts, SVGs, or rich metric layouts can disappear or flatten in the final PPTX. Fix by making the container `data-deck-native="raster"` with `data-deck-editability="visual"` and marking every user-visible child string as native text.

It also warns when native table headers and body cells are likely to drift in PPTX (`table.header-alignment`, `pptx.table-text-margin`). For `boxy` tables, keep `th`/`td` padding and alignment consistent or set `data-pptx-cell-margin-pt` on the table.

It also warns when an actual HTML `<table>` is raster/background-only (`pptx.table-rasterized`). Use `data-deck-native="table"` for tables the user must edit, or mark intentional image-only tables with `data-qa-table-raster-ok="true"`.

Load `references/qa-gates.md` for the full checklist and repair loop.

### 5. Export

Choose the branch requested by the user. Both branches start from the same canonical HTML but resolve native capability separately.

For PowerPoint, create the primary editable deliverable with the `powerpoint-editable` profile. This profile uses hybrid output, preserves eligible native tables and charts, and sets `preview-safe=false`:

```bash
node scripts/export-html-editable-deck.mjs path/to/deck.html dist --profile=powerpoint-editable --theme=light
```

From the skill folder itself:

```bash
node scripts/export-html-editable-deck.mjs ../../path/to/deck.html ../../dist --profile=powerpoint-editable --theme=light
```

For direct Google Slides, do not emit a PPTX. Generate and validate the connector-ready native plan:

```bash
node scripts/export-html-google-slides-plan.mjs path/to/deck.html dist-slides --profile=google-slides-native --theme=light
node scripts/qa-google-slides-plan.mjs dist-slides/deck.google-slides.plan.json
```

The default plan is materialized for `720x405pt`. For another live page size with the same aspect ratio as the canonical HTML, pass both `--page-width-pt=<width>` and `--page-height-pt=<height>`. The options are required together; omitting both keeps the default.

Then follow `references/google-slides-native.md`: create the native Slides file, execute the ordered batches, re-read the presentation and slides, and inspect fresh LARGE thumbnails for every slide.

When browser or web-viewer compatibility is required, create a separate preview-fidelity copy. Do not substitute it for the primary editable deck:

```bash
node scripts/export-html-editable-deck.mjs path/to/deck.html dist-preview --profile=preview-fidelity --theme=light
```

Outputs:

```text
dist/deck.pdf
dist/deck.hybrid.pptx
dist/deck.hybrid.manifest.json
dist/deck-hybrid-slides-png/
```

Direct Slides local outputs:

```text
dist-slides/deck.google-slides.plan.json
dist-slides/deck-google-slides-assets/
```

### 6. Final Response

Return only the artifacts for the requested branch:

- generated HTML
- PDF, when requested or produced for the PowerPoint branch
- primary editable PPTX and its manifest, when PowerPoint is requested
- separate preview-fidelity PPTX and manifest, when requested
- direct Slides plan and assets when Google Slides is requested
- verified Google Slides URL only after connector creation, readback, and thumbnail QA

State that the HTML/Chromium render is the canonical design, summarize target-specific native coverage and intentional raster fallbacks, and disclose any required or preferred object that was not emitted or remotely verified natively. Do not call the deck fully editable unless every intended object is confirmed in the actual target and the claim is accurate.

## Reference Router

Read only the references needed for the current task:

| Need | Reference |
|---|---|
| Extract claims, evidence, metrics, risks, chronology, stakeholders | `references/source-analysis.md` |
| Choose narrative arc and create slide plan | `references/storyline-design.md` |
| Start a PPTX-safe single-file HTML deck | `references/deck-skeleton.md` |
| Choose slide layout patterns | `references/slide-patterns.md` |
| Run content, visual, editability, and export checks | `references/qa-gates.md` |
| Compare high/low models, subagents, or model-output variants | `references/model-benchmark-decks.md` |
| Preserve citations, assumptions, and source notes | `references/source-notes.md` |
| Understand native overlay attributes | `references/native-contract.md` |
| Add export-safe CSS | `references/export-css.md` |
| Debug exporter issues | `references/troubleshooting.md` |
| Create Google Slides directly without PPTX import | `references/google-slides-native.md` |

## Style Profile Router

When the user asks for a deck style, choose one profile before authoring HTML. Read only the matching reference file, then adapt the pattern to fixed-size canonical HTML and the selected target's fidelity-safe native output.

| User intent | Profile reference |
|---|---|
| earnings, IR, financial results, board metric review | `references/style-earnings-release.md` |
| executive summary, leadership briefing, one-slide decision summary | `references/style-executive-summary.md` |
| KPI dashboard, operating metrics, product or business health | `references/style-dashboard.md` |
| report summary, research digest, article or document summary | `references/style-report-summary.md` |
| timeline, roadmap, milestones, release plan | `references/style-timeline-roadmap.md` |
| process, workflow, system flow, operating model | `references/style-process-flow.md` |
| comparison, matrix, pricing/options, before-after table | `references/style-comparison-table.md` |
| infographic, one-pager, concept explainer | `references/style-infographic-onepager.md` |

Profile rules are constraints, not templates. Keep the user's brand, content density, and audience first. If no profile fits, use the closest profile for structure. Preserve complex decoration visually, but keep simple business geometry native when fidelity holds.

## Native Overlay Hints

Use the target-neutral deck contract when authoring new presentations:

| Canonical attribute | Purpose | Legacy alias |
|---|---|---|
| `data-deck-id` | stable ID across authored, resolved, and emitted manifest states | `data-pptx-id` |
| `data-deck-native` | requested native object type | `data-pptx-native` |
| `data-deck-editability` | `required`, `preferred`, or `visual` priority | `data-pptx-priority` with the same priority value |

Use `required` for objects that must be editable, `preferred` for objects that should be native when the canonical appearance survives, and `visual` for fidelity-locked or decorative regions. Existing `data-pptx-*` markup remains supported; `data-pptx-editability` is a renderer decision hint, not a priority alias. See `references/native-contract.md` for the mapping.

Add stable IDs and native intent to meaningful objects:

```html
<h1 data-deck-id="s1-title" data-deck-native="text" data-deck-editability="required">
  Quarterly Growth Strategy
</h1>

<div class="metric-card" data-deck-id="s1-metric-card" data-deck-native="shape" data-deck-editability="preferred">
  <strong data-deck-id="s1-metric-value" data-deck-native="text" data-deck-editability="required">+42%</strong>
  <span data-deck-id="s1-metric-label" data-deck-native="text" data-deck-editability="required">Conversion lift</span>
</div>

<table data-deck-id="s1-table" data-deck-native="table" data-deck-editability="required" data-pptx-table-mode="native">...</table>
```

Supported values:

| Value | PPTX result | Use for |
|---|---|---|
| `text` | editable text box | titles, labels, bullets, metrics |
| `shape` | editable shape | cards, panels, badges, simple dividers |
| `image` | editable image object | local, file URL, or data URI images |
| `chart` | editable chart | canvas or div with explicit chart JSON |
| `table` | editable table or editable cell boxes | actual HTML tables |
| `shape text` | shape plus text from one element | small badges and chips |
| `ignore` or `raster` | no native object | keep as raster background only |

Use `data-deck-native="raster"` with `data-deck-editability="visual"` for complex panels and decorative visuals, then make every user-visible text child native.

Do not mark a chip, badge, pill, heatmap cell, or numbered marker as `data-deck-native="text"` when the same element carries the visible background/border/radius. The exporter hides text-native elements from the raster background, so the box can disappear in PPTX previews; use `shape text` or split box/text instead.

## Chart Contract

Do not reverse-engineer canvas pixels. Add chart data explicitly:

```html
<div
  data-deck-id="s2-chart"
  data-deck-native="chart"
  data-deck-editability="required"
  class="chart-panel"
  data-pptx-chart='{
    "type": "bar",
    "labels": ["Q1", "Q2", "Q3", "Q4"],
    "series": [
      { "name": "Revenue", "values": [12, 18, 24, 31] }
    ],
    "title": "Quarterly Revenue",
    "showLegend": false,
    "showValue": true
  }'>
</div>
```

Use the HTML chart for PDF/visual fidelity and the JSON spec for editable PPTX charts.

In the primary `powerpoint-editable` output, chart editability is mandatory regardless of `preferred` versus `required` priority. The manifest gate requires a real native chart part and the exporter supplies the embedded workbook used by PowerPoint's Edit Data workflow. If the chart JSON is missing or unsupported, stop and repair the spec; do not accept a raster chart.

## Table Fidelity

For tables where position matters, make browser layout deterministic:

```css
table.report-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}
```

Use `<colgroup>` or explicit first-row widths when column proportions matter. Choose table mode per table:

```html
<table data-deck-id="s3-table-native" data-deck-native="table" data-deck-editability="required" data-pptx-table-mode="native">...</table>
<table data-deck-id="s3-table-boxy" data-deck-native="table" data-deck-editability="preferred" data-pptx-table-mode="boxy">...</table>
<table data-deck-id="s3-table-visual" data-deck-native="table" data-deck-editability="visual" data-pptx-table-mode="raster" data-qa-table-raster-ok="true">...</table>
```

Use `native` for data tables users will edit as tables. Use `boxy` for dense dashboards or layouts where rendered geometry matters. Use `raster` for nested tables, complex cell visuals, images, SVGs, or decorative mini-layouts.

For `boxy` tables with styled headers, use consistent `th`/`td` padding and add `data-pptx-cell-margin-pt="6"` when PPTX text anchors must line up across header and body cells.

When exporting a PPTX compatibility copy with `--preview-safe=true`, native tables are normally kept in the raster background unless they use `boxy`. For simple tables that must stay editable in that PowerPoint/web-preview copy, use:

```html
<table data-deck-id="s3-preview-table" data-deck-native="table" data-deck-editability="required" data-pptx-table-mode="native" data-pptx-preview-native="true">
  ...
</table>
```

## Text Fidelity

For critical headings and long text, use explicit line wrappers so PowerPoint does not rewrap differently:

```html
<h1 data-deck-id="s4-critical-heading" data-deck-native="text" data-deck-editability="required" data-pptx-text-mode="lines">
  <span data-pptx-line>CSS design stays intact</span>
  <span data-pptx-line>PowerPoint text stays editable</span>
</h1>
```

```css
[data-pptx-line] {
  display: block;
}
```

Useful fine-tuning attributes:

| Attribute | Meaning |
|---|---|
| `data-pptx-dx-px` | add/subtract CSS px from x before conversion |
| `data-pptx-dy-px` | add/subtract CSS px from y before conversion |
| `data-pptx-dw-px` | add/subtract CSS px from width before conversion |
| `data-pptx-dh-px` | add/subtract CSS px from height before conversion |
| `data-pptx-font-scale` | multiply CSS font size before converting px to pt |
| `data-pptx-margin-pt` | PowerPoint text box internal margin; default is `0` |
| `data-pptx-z` | additional z-index for native layering |
| `data-pptx-bg-keep="true"` | do not hide this native element in the raster background |

## Export Options

Choose the output branch from the requested deliverable. PowerPoint and Google Slides share the canonical HTML but have separate target resolvers and QA. Do not use one format as an unrequested intermediate for the other.

### PowerPoint

Use the editable PowerPoint profile for the primary deliverable:

```bash
node scripts/export-html-editable-deck.mjs path/to/deck.html dist --profile=powerpoint-editable --theme=light
```

`powerpoint-editable` resolves to hybrid export with `preview-safe=false`. It keeps supported business objects native. Decorative fidelity exceptions may remain raster, but readable text and semantic charts may not: text must reach 100% native character coverage and charts must remain native with editable data.

Create a separate compatibility copy only when a browser previewer or an explicitly accepted import path needs it. Do not silently substitute this for direct Google Slides creation:

```bash
node scripts/export-html-editable-deck.mjs path/to/deck.html dist-preview --profile=preview-fidelity --theme=light
```

`preview-fidelity` uses `preview-safe=true`; it may intentionally keep chart/table visuals in the raster background. Never present this compatibility copy as the most editable deliverable.

Use `--fallback=balanced|strict|editable` to control how aggressively the exporter keeps objects native when PowerPoint cannot match the CSS exactly:

- `balanced`: default policy; rasterize CSS effects PowerPoint commonly mismatches.
- `strict`: maximize visual fidelity; more objects remain in the raster background.
- `editable`: aggressive diagnostic policy; keep more native shapes, but never use it for the primary deliverable unless a render of the exported PPTX still passes the canonical fidelity gate.

Use `--bg-native=keep` only when a PPTX viewer does not show native overlays reliably. The default `--bg-native=hide` avoids duplicated text in PowerPoint.

Use explicit low-level flags only when debugging or overriding a profile. `--preview-safe=false` is the primary editable policy. `--preview-safe=true` belongs to the separate preview-fidelity copy because it can skip native chart/table overlay objects and keep those visuals in the raster background.

Use `--table-mode=auto|native|boxy|raster` to control editable table output:

- `auto`: default; simple tables become native PowerPoint tables, while risky CSS/table layout can become editable cell-by-cell boxes or raster fallback.
- `native`: force a real PowerPoint table object.
- `boxy`: draw each rendered HTML cell as editable shapes/text boxes using DOMRect positions.
- `raster`: keep the table only in the CSS background.

Never manually compute CSS layout from `left`, `top`, `grid`, `flex`, `padding`, or `clamp()`. The exporter reads `getBoundingClientRect()`, subtracts the current slide rect, and normalizes to the PPTX slide size.

### Direct Google Slides

When the deliverable is Google Slides, bypass PPTX creation and import:

```bash
node scripts/export-html-google-slides-plan.mjs path/to/deck.html dist-slides --profile=google-slides-native --theme=light
node scripts/qa-google-slides-plan.mjs dist-slides/deck.google-slides.plan.json
```

Then execute the validated plan through the connected Drive/Slides tools. Create a blank native Google Slides file, read its live page size and bootstrap slide ID, and require the plan's expected page before content writes. Plans default to `720x405pt`; for another live page with the canonical HTML aspect ratio, regenerate with both `--page-width-pt=<width>` and `--page-height-pt=<height>`. The options are required together, and existing materialized requests must never be treated as implicitly rescaled. Create the planned blank slides, delete only the bootstrap slide, and apply each slide's ordered batches. Pass a batch's local image path through connector-level `image_uris`.

The plan contains a transparent visual underlay plus native text, shapes, lines, tables, and images. Its `qa.remoteStatus` must remain `unverified` until the presentation is created and verified through connector readback and fresh LARGE thumbnails.

Default direct-Slides chart policy is fidelity-first:

- a preferred chart may use an isolated canonical chart PNG with a recorded capability reason
- a required data-editable chart blocks the default plan unless the user explicitly authorizes a linked Google Sheets chart workflow
- never invent a generic chart or import a PPTX chart merely to claim native coverage

Use `--table-mode=boxy` when exact cell geometry matters more than row/column operations. Use `--table-mode=native` for a real Slides table, then verify cell padding, row growth, and Korean text wrapping in thumbnails.

Read `references/google-slides-native.md` before executing this branch. Local plan QA proves only request structure and planned coverage; remote completion requires structure readback and visual verification.

## Validation

Match validation to the change:

Deck-only creation or edits:

```bash
node scripts/qa-html-deck.mjs path/to/deck.html
node scripts/qa-html-deck.mjs path/to/deck.html --screenshots=dist/full-render
node scripts/export-html-editable-deck.mjs path/to/deck.html dist --profile=powerpoint-editable --theme=light
node scripts/qa-export-manifest.mjs dist/deck.hybrid.manifest.json
node scripts/qa-pptx-package.mjs dist/deck.hybrid.pptx
```

Direct Google Slides deliverable:

```bash
node scripts/qa-html-deck.mjs path/to/deck.html --screenshots=dist-slides/full-render
node scripts/export-html-google-slides-plan.mjs path/to/deck.html dist-slides --profile=google-slides-native --theme=light
node scripts/qa-google-slides-plan.mjs dist-slides/deck.google-slides.plan.json
```

After connector execution, re-read the presentation and every edited slide, then inspect fresh LARGE thumbnails for all slides. Do not claim remote creation from local plan QA alone.

Skill, reference, README, or example changes:

```bash
node --check skills/create-editable-presentations/scripts/export-html-editable-deck.mjs
node --check skills/create-editable-presentations/scripts/qa-html-deck.mjs
node --check skills/create-editable-presentations/scripts/qa-pptx-package.mjs
node --check skills/create-editable-presentations/scripts/export-html-google-slides-plan.mjs
node --check skills/create-editable-presentations/scripts/qa-google-slides-plan.mjs
npm run qa:demo
```

Exporter, QA script, table/chart conversion, or package script changes:

```bash
node --check skills/create-editable-presentations/scripts/export-html-editable-deck.mjs
node --check skills/create-editable-presentations/scripts/qa-html-deck.mjs
node --check skills/create-editable-presentations/scripts/export-html-google-slides-plan.mjs
node --check skills/create-editable-presentations/scripts/qa-google-slides-plan.mjs
npm run qa:demo
npm run qa:matrix-extended
npm run qa:google-slides-matrix
node scripts/qa-html-deck.mjs examples/source-to-board-brief.html --screenshots=dist/full-render
npm run export:hybrid
node scripts/qa-pptx-package.mjs dist/korean-hybrid-demo.hybrid.pptx
npm run export:image
npm run export:native
```

Agent compatibility changes:

```bash
npm run check:agents
```
