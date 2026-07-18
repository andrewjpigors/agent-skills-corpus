---
name: hwpx-document-processing
description: Use when inspecting, extracting, creating, editing, repairing, validating, or repackaging Hancom HWPX documents. Provides HWPX-only ZIP/XML workflows and helper scripts for OWPML package structure, text, styles, equations, images, tables, fields, cross-file references, layout validation, and safe output reporting; binary HWP is detection/read-only fallback only.
version: 1.3.4
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [HWPX, HWP, Hancom, OWPML, document-processing, Korean documents, XML, ZIP, equations, images, tables, layout, helper-scripts]
    related_skills: [ocr-and-documents, nano-pdf]
---

# HWPX Document Processing

## Purpose

Use this skill to inspect, extract, create, edit, repair, validate, or repackage Hancom `.hwpx` documents while preserving as much layout and document semantics as possible.

A `.hwpx` file is not plain text, not Markdown, and not DOCX. Treat it as an OPC-like ZIP package containing OWPML XML, style reference graphs, cached layout fragments, field controls, embedded binary assets, previews, and metadata. XML validity is necessary but not sufficient: the final authority for visual layout is Hancom Office rendering or a Hancom-exported PDF.

The goal is not merely to produce a ZIP that parses. The goal is a document that:

- opens in Hancom-compatible software,
- preserves existing styles/layout unless the user asked to change them,
- keeps equations/images/tables/forms/captions/references connected,
- passes structural validation,
- and clearly reports any remaining layout uncertainty.

## Non-negotiable operating rules

1. **Prefer clone-and-mutate.** For edits and generated templates, start from a known-good `.hwpx` seed or from the user's original file. Do not construct a complete OWPML package from zero unless no seed exists and the task is explicitly experimental.
2. **Never edit the user's original as the only copy.** Write to a new path or backup first. Preserve the original ZIP entries and metadata whenever possible.
3. **Never blindly unzip untrusted input.** Inspect with `zipfile` entry reads. If extraction is needed, normalize paths and reject absolute paths or `..` components.
4. **Use namespace/local-name aware XML parsing.** Do not depend on a specific prefix beyond writing known-good output; prefixes may vary, but local names such as `p`, `run`, `t`, `tbl`, `pic`, `equation`, `script` are stable enough for inspection.
5. **Preserve style/reference IDs unless you intentionally add definitions.** A section reference such as `charPrIDRef="7"` is only safe if `Contents/header.xml` defines the corresponding `hh:charPr id="7"`.
6. **Remove stale layout caches after text/object edits.** `hp:linesegarray` is cached layout. If text length, equations, images, or table content changes, remove affected `linesegarray` nodes so Hancom can recalculate.
7. **Validate after every edit.** At minimum check ZIP integrity, required parts, XML parse, section order, text/control extraction, equation lint, image references, table grid sanity, and cross-file ID refs.
8. **Do not claim visual correctness from `rhwp`/SVG.** `rhwp` rendering can distort equations and object geometry, so use it only as a weak smoke check for text/object presence and page dump sanity. Final visual authority is Hancom Office or a Hancom-exported PDF.
9. **Do not under-generate or ignore the requested form.** HWPX generation is not complete merely because the file opens. If the user supplied a format, rubric, section list, sample, or length expectation, treat it as a checklist/schema and verify that the generated document covers it before finalizing.
10. **Prefer readable spacing over raw density.** Generated documents must have intentional paragraph breaks, headings, equation/table separation, and no random empty-line clutter. Fix cramped or overly sparse layouts before returning the file.

## When to use

Load and follow this skill for:

- `.hwpx` package inspection, text extraction, or review,
- `.hwpx` creation from a seed/template,
- surgical edits to text, equations, images, tables, fields, captions, citations, headers, footers, or metadata,
- equation script linting and repair,
- image/BinData reference repair,
- table/form validation,
- converting a report/Markdown/TeX draft into an HWPX workflow,
- diagnosing layout breakage after AI edits,
- checking whether a Korean school/report document is likely submission-safe.

Do not use this as the primary editing method for binary `.hwp` unless you have a dedicated HWP writer. For binary HWP, prefer extraction/review or ask the user to export/convert to `.hwpx` before surgical editing.

## Format decision

When a file arrives, detect by bytes, not just extension:

```python
def detect_hwp_family(path):
    with open(path, "rb") as f:
        head = f.read(64)
    if head.startswith(b"PK\x03\x04"):
        return "zip_maybe_hwpx"
    if head.startswith(bytes.fromhex("D0CF11E0A1B11AE1")):
        return "ole_cfb_probably_hwp5"
    if b"HWP Document File V3.00" in head:
        return "hwp3"
    return "unknown"
```

Decision rules:

- If extension is `.hwpx` and signature is ZIP, use the ZIP/XML workflow below.
- If extension is `.hwp` and signature is OLE/CFB, treat it as binary HWP v5. Prefer read-only extraction or ask for HWPX export before editing.
- If extension is `.pdf`, use it only for visual validation or read-only review. Do not infer editable HWPX object positions from a PDF unless doing a manual reconstruction.
- If the file is ZIP but lacks HWPX required parts, do not assume it is HWPX.

## Mental model of an HWPX package

A typical HWPX ZIP contains:

- `mimetype`: usually the first ZIP entry; should be stored/uncompressed when repacking.
- `version.xml`: Hancom/version metadata.
- `Contents/content.hpf`: OPF-like package manifest and spine. This often defines section order and image `BinData` entries.
- `Contents/header.xml`: fonts, paragraph styles, character styles, border fills, numbering, bullets, tab definitions, page/border styles, and other global reference definitions.
- `Contents/section0.xml`, `Contents/section1.xml`, ...: document body sections, paragraphs, controls, tables, equations, pictures, fields, section properties.
- `settings.xml`: settings.
- `META-INF/container.xml`, `META-INF/manifest.xml`, sometimes `META-INF/container.rdf`.
- `Preview/PrvText.txt`, `Preview/PrvImage.png`: preview/search assets.
- `BinData/...`: embedded images/OLE/binary assets.

Important implication: the section XML contains many references into other package files. Valid XML can still render incorrectly when these cross-file references are broken.

## Reusable validator script

This skill includes a dependency-free structural validator:

```bash
python /home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts/validate_hwpx.py file.hwpx
python /home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts/validate_hwpx.py --json file.hwpx
```

Use it whenever practical after creating or editing an HWPX. It checks:

- ZIP signature and `ZipFile.testzip()` integrity,
- unsafe ZIP paths,
- required package parts,
- XML parse status,
- section order from `content.hpf` spine with filename fallback,
- paragraph/control counts,
- equation object count and script lint,
- image `binaryItemIDRef` → `content.hpf` manifest → `BinData` resolution,
- table direct row/cell/span sanity,
- field counts,
- style/paragraph/character/border/tab/numbering reference consistency,
- object ID and `zOrder` duplicate warnings.

Treat the validator as structural evidence only. It cannot prove baseline, clipping, pagination, font fallback, or final rendered layout.

## HWPX helper script bundle

Use the bundled helper scripts for repeatable HWPX-only work instead of rewriting ad-hoc ZIP/XML code each time. Detailed usage is in `references/HWPX_HELPER_SCRIPTS.md`.

```bash
SK=/home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts
python "$SK/validate_hwpx.py" file.hwpx
python "$SK/extract_hwpx_text.py" file.hwpx --format json -o out.json
python "$SK/create_hwpx_from_seed.py" --out report.hwpx --title "보고서 제목"
python "$SK/fill_placeholders_hwpx.py" form.hwpx --out filled.hwpx --map '{"{{name}}":"홍길동"}'
python "$SK/add_equations_hwpx.py" in.hwpx --out out.hwpx --equation "MSE::MSE = { 1 } over { n } sum _ { i = 1 } ^ { n } e _ { i } ^ { 2 }"
python "$SK/replace_equations_hwpx.py" in.hwpx --out out.hwpx --index 0 --script "RMSE = sqrt { { 1 } over { n } sum _ { i = 1 } ^ { n } e _ { i } ^ { 2 } }"
python "$SK/insert_table_hwpx.py" in.hwpx --out out.hwpx --rows '[["항목","값"],["A","10"]]'
python "$SK/replace_table_cells_hwpx.py" in.hwpx --out out.hwpx --index 0 --rows '[["항목","새 값"],["A","20"]]'
python "$SK/insert_image_hwpx.py" in.hwpx --image figure.png --caption "그림 1. 구조" --out out.hwpx
python "$SK/replace_image_hwpx.py" in.hwpx --image new_figure.png --index 0 --out out.hwpx
python "$SK/render_or_svg_check_hwpx.py" out.hwpx --outdir render_check
```

Available scripts:

Additional workflow notes:

- `references/school-report-from-markdown-workflow.md`: marker-based Markdown → school-report HWPX workflow for dense Korean 수행평가 reports with real equations/tables/figures, equation placement/renumbering guidance, AI-evidence appendix handling, final figure appendix, reference-report density comparison, and overflow mitigation.

- `hwpx_utils.py`: shared safe ZIP/XML, section-order, style-ref, repack, object-id, image, table, equation helpers.
- `validate_hwpx.py`: structural validator for package/XML/reference/object sanity.
- `extract_hwpx_text.py`: text, paragraph, equation, image, table, field extraction to text/Markdown/JSON.
- `create_hwpx_from_seed.py`: create a simple HWPX from a known-good seed while preserving package/header/section properties.
- `fill_placeholders_hwpx.py`: conservative text placeholder replacement; default preserves field/control shapes by replacing only within single text nodes.
- `add_equations_hwpx.py`: append real `hp:equation` objects with HWP equation-script lint.
- `replace_equations_hwpx.py`: replace existing equation scripts by index while preserving each `hp:equation` object's position, size, wrapping, IDs, and geometry.
- `insert_table_hwpx.py`: append simple grid tables using existing style and border-fill IDs.
- `replace_table_cells_hwpx.py`: replace text inside an existing simple table while preserving table/cell geometry, borders, margins, and style IDs.
- `insert_image_hwpx.py`: add image BinData, `content.hpf` manifest item, section `hp:pic`/`hc:img`, geometry, and caption.
- `replace_image_hwpx.py`: replace an existing image asset by `binaryItemIDRef` or occurrence index while preserving section `hp:pic` geometry and captions.
- `render_or_svg_check_hwpx.py`: run validator and, when `rhwp` exists, weak text/object/page-dump smoke checks. Do not use `rhwp` SVG output as visual-layout authority, especially for equations.

Design basis: Hancom's official OWPML model/documentation, `python-hwpx`, `unhwp`, `openhanji`, `hwpx-filler`, and `rhwp`/`rhwp-python` all support the same core lesson: treat HWPX as a package+XML reference graph, extract with local-name traversal, mutate by preserving existing shapes, and validate structurally. `rhwp` can help confirm that text/objects/pages are detected, but its rendered SVG is not visually authoritative; use Hancom/PDF for layout confidence.

## Safe inspection workflow

Use this sequence for review, diagnosis, and pre-edit discovery.

1. Detect file type by signature.
2. Open ZIP with `zipfile.ZipFile`; run `testzip()`.
3. Reject or report unsafe entry names: absolute paths or `..` components.
4. Check required parts:
   - `mimetype`
   - `Contents/content.hpf`
   - `Contents/header.xml`
   - at least one `Contents/section*.xml`
   - `META-INF/container.xml` for strict validation.
5. Parse all XML-like entries (`.xml`, `.hpf`, `.rdf`) and collect parse errors.
6. Resolve section order from `Contents/content.hpf` spine. Fallback to sorted `Contents/section*.xml` only if spine resolution fails.
7. Extract paragraphs by local names: `p` → descendant `t`.
8. Extract controls and objects by local names: `tbl`, `tr`, `tc`, `pic`, `img`, `equation`, `script`, `caption`, `fieldBegin`, `fieldEnd`, `footNote`, `endNote`, `header`, `footer`.
9. Build cross-file reference sets from section attributes and compare them to `Contents/header.xml` definitions.
10. Resolve image references through `Contents/content.hpf` manifest and ZIP `BinData/` entries.
11. Lint equation scripts.
12. Validate table grids using only direct `tr`/`tc` children per table; validate nested tables separately.
13. Check captions, citations, and field pairs if relevant.
14. If layout matters, render or ask for a Hancom-exported PDF.

Minimal local-name helpers:

```python
def lname(tag):
    return tag.rsplit('}', 1)[-1] if '}' in tag else tag

def paragraph_text(p):
    return ''.join(t.text or '' for t in p.iter() if lname(t.tag) == 't')
```

Section order helper:

```python
def resolve_sections(zip_names, content_hpf_root):
    id_to_href = {}
    spine_ids = []
    for e in content_hpf_root.iter():
        local = lname(e.tag)
        if local == 'item' and e.attrib.get('id') and e.attrib.get('href'):
            id_to_href[e.attrib['id']] = e.attrib['href']
        elif local == 'itemref' and e.attrib.get('idref'):
            spine_ids.append(e.attrib['idref'])
    ordered = [id_to_href[i] for i in spine_ids
               if id_to_href.get(i, '').startswith('Contents/section')]
    return ordered or sorted(n for n in zip_names if re.match(r'Contents/section\d+\.xml$', n))
```

## Cross-file reference validation

Check these graphs explicitly:

- section `charPrIDRef` → `Contents/header.xml` `hh:charPr id`
- section `paraPrIDRef` → `hh:paraPr id`
- section `styleIDRef` → `hh:style id`
- table/cell/page `borderFillIDRef` → `hh:borderFill id`
- paragraph `tabPrIDRef` → `hh:tabPr id`
- numbering/bullet refs → header numbering/bullet definitions
- section `<hc:img binaryItemIDRef="imageN">` → `Contents/content.hpf` `opf:item id="imageN"` → ZIP `BinData/...`
- newly inserted object `id` and `zOrder` uniqueness within the edited scope.

Do not assume image references live in `header.xml`. Real HWPX samples often use `Contents/content.hpf` as the primary manifest, while section XML stores `binaryItemIDRef="imageN"`.

Broken reference IDs are high severity because Hancom may silently substitute defaults or render layout incorrectly.

## Editing strategy for existing HWPX files

Use clone-and-mutate:

1. Copy the original file to a new output path.
2. **Preserving visual intent in templates.** AI edits often target an existing school/report/public-form template. When an object already exists in the right place, prefer replacement helpers over insertion helpers:
   - existing image slot → `replace_image_hwpx.py`, preserving `hp:pic` geometry/caption,
   - existing equation slot → `replace_equations_hwpx.py`, preserving equation object hitbox and placement,
   - existing simple table → `replace_table_cells_hwpx.py`, preserving table/cell geometry and styles.
3. Locate the smallest affected subtree.
4. Preserve existing `paraPrIDRef`, `styleIDRef`, `charPrIDRef`, `borderFillIDRef`, object geometry, and metadata unless changing them is the actual task.
5. Modify only the necessary text/script/reference/asset nodes.
6. Remove stale `hp:linesegarray` from affected paragraphs.
7. If adding new styles/assets, update every required package part and validate references.
8. Repack with `mimetype` first and stored/uncompressed when practical; preserve remaining entry order and original entries.
9. Run structural validation and text/control extraction after repacking.

### Text edits

Prefer editing existing `hp:t` text nodes within the same `hp:run`. Preserve `charPrIDRef` and surrounding controls.

Cautions:

- Multiple `hp:t` nodes may form one visual paragraph.
- Empty runs and control-only runs are meaningful; do not delete them casually.
- Preserve `xml:space="preserve"` where it exists.
- If replacing text changes line breaks or length materially, remove the paragraph's `hp:linesegarray`.
- Do not flatten `fieldBegin`/`fieldEnd` controls unless the user explicitly wants static text.

### Style edits

Avoid editing `Contents/header.xml` unless required. If you must add style definitions:

- Add `hh:charPr`, `hh:paraPr`, `hh:style`, `hh:borderFill`, or related definitions consistently.
- Use unique IDs that do not collide with existing IDs.
- Update any item counts if the source uses count attributes.
- Validate all section references against header definitions.

For most AI edits, reuse existing style IDs from nearby paragraphs.

### Layout cache

`hp:linesegarray` is cached layout. It can cause overlap, stale line heights, or clipping after text/object edits. Remove it from affected paragraphs and let Hancom recalculate.

Do not remove layout caches globally unless the user accepts layout recalculation across the document.

## Creating new HWPX templates

When the user asks to create a new `.hwpx` document and no strict visual design is required, do not build the full OWPML package from zero. Use a validated blank/minimal HWPX seed.

Practical clone-and-fill pattern:

1. Find a known-good blank/minimal `.hwpx` seed.
2. Validate the seed first.
3. Preserve ZIP package entries, namespaces, `Contents/header.xml`, `version.xml`, `settings.xml`, and `META-INF` files.
4. Preserve the section root namespace declarations and the first paragraph's section property run containing `hp:secPr` and `hp:colPr`.
5. Replace body paragraph blocks with generated `hp:p` elements.
6. Use existing style references only after inspecting `Contents/header.xml`:
   - body often uses `paraPrIDRef="1" styleIDRef="1" charPrIDRef="0"`, but confirm in the seed.
   - headings can reuse outline styles such as `styleIDRef="2"` when present.
   - title-like text can reuse title/TOC-sized styles only after confirming the style IDs.
7. Generate unique paragraph IDs. Avoid reusing object IDs when inserting controls.
8. Do not include stale `hp:linesegarray` in generated paragraphs.
9. Update `Contents/content.hpf` metadata when safe: title, creator, created/modified date.
10. Update `Preview/PrvText.txt` so file managers/search show meaningful content.
11. Repack with `mimetype` first and stored/uncompressed when practical.
12. Validate by reopening the new file and extracting text back out.

For generated school/report templates, include clear placeholder text such as `○○`, `홍길동`, `[표 1]`, `[그림 1]`, and tell the user what to replace.

## Generated-document quality guardrails

When creating an HWPX document from a prompt, especially 논문/보고서/수행평가/공문/양식 templates, structural validity is necessary but not enough. Many failures come from content that is too short, missing requested sections, broken equations, or poor whitespace. Apply these guardrails before packaging and again before the final response.

### 1. Requested format = checklist/schema

Before writing the section XML, derive a compact checklist from the user's request or source template:

- required title/subtitle/meta fields,
- heading hierarchy and section order,
- required tables, figures, equations, captions, references, appendix items,
- required paragraph count, page/length expectation, rubric items, or placeholder slots,
- formatting constraints such as 논문체, 보고서체, school-report style, numbered sections, or specific labels.

After generating the HWPX, extract text and object metadata back out and compare against this checklist. If a requested section/table/equation/label is missing or renamed unexpectedly, fix the document rather than merely warning.

### 2. Minimum content density

Do not satisfy a report/template request with title plus one-line sections unless the user explicitly asked for a skeleton. Reasonable defaults:

- A 논문/보고서 sample should include an abstract/요약, introduction, method/body, results/discussion, conclusion, and references or placeholders when appropriate.
- Each major body section should contain at least one developed paragraph, not only a heading.
- If the user requests an "임의의 서식" or sample, include realistic placeholder-rich sample content, not empty decorative sections.
- If the intended document is a fillable template, make placeholders explicit and sufficiently descriptive, e.g. `[연구 목적 3~5문장 입력]`, not just `내용`.

When the requested scope is ambiguous, choose a useful medium-density artifact: complete enough to demonstrate the form, but not bloated.

### 3. Equation fidelity

For every substantive formula planned in the document:

- convert it to HWP equation script, not raw LaTeX or plain Unicode text,
- insert or replace it as an actual `hp:equation` object unless it is truly a tiny inline symbol,
- keep a source list of intended equation labels/scripts,
- validate extracted equation count and script text against that source list,
- lint for raw LaTeX commands, missing spaces around operators such as `cdot`, malformed braces/subscripts/superscripts, and too-small hitboxes.

If equation object rendering cannot be visually confirmed, say so. Do not claim equations "look correct" from XML validation alone. If an equation cannot be safely represented, include a readable fallback plus a warning.

### 4. Readability and whitespace

Whitespace is part of document quality. Prefer predictable spacing rules:

- one title block, then one intentional gap before the body,
- one blank paragraph or equivalent spacing between major sections only,
- no repeated accidental blank paragraphs,
- explanatory text before/after equations, tables, and figures so objects are not jammed together,
- separate long equations into their own paragraphs with generous hitbox height,
- keep table cell text concise and avoid overfilling narrow cells,
- update `Preview/PrvText.txt` so extracted preview text is readable too.

After generation, inspect extracted paragraph sequence for empty-paragraph runs, missing headings, and cramped object adjacency. Remove stale `hp:linesegarray` in affected paragraphs so Hancom can recalculate spacing.

### 5. Final self-check for AI-generated HWPX

Before returning a generated or heavily rewritten HWPX, confirm:

- requested format checklist coverage,
- enough content density for the user's requested artifact type,
- all intended equations became `hp:equation` objects or are explicitly justified as inline text,
- extracted text is readable in order,
- major sections are separated consistently,
- there are no obvious placeholder omissions, duplicated headings, or accidental blank-line clusters.

## Equations

HWP equation objects are renderer-specific and script-sensitive. **Default policy: insert most mathematical formulas as real HWP equation objects (`hp:equation`) whenever practical.** When generating or converting HWPX documents, do not leave formulas as plain text merely because Unicode inline notation is easier. Convert equations, metric definitions, transformations, sums, fractions, square roots, vector/matrix expressions, and named formulas into HWP equation script and insert them with `add_equations_hwpx.py` or an equivalent cloned `hp:equation` object.

### Inline math policy

Use Unicode inline notation only for isolated symbols or very short non-central mentions where a separate equation object would make the layout worse:

```text
rᵢ, θₜ, φ, Δ, j−i, e², mθₜ, β₀, β₁, ŷᵢ
```

Use `hp:equation` objects for nearly all substantive formulas that should survive as editable/rendered math in Hancom:

- definitions and metric formulas,
- display equations,
- equalities/inequalities and derivation steps,
- fractions, sums, products, square roots, exponents, limits, integrals,
- vectors, matrices, dot products, transformations, rotations,
- formulas with Greek symbols or multi-level subscripts/superscripts,
- formulas the user may edit in Hancom's equation editor.

If a document contains multiple formulas, batch them through `add_equations_hwpx.py` from JSON instead of scattering them as text. Only fall back to Unicode inline math when an expression is truly trivial or when a renderer check shows the equation object harms readability.

### Equation script mapping

HWP equation script is not raw LaTeX. Common safe mappings:

```text
\theta                 -> theta
\phi                   -> phi
\Delta                 -> Delta
\alpha                 -> alpha
\beta                  -> beta
\pi                    -> pi
\cdot                  -> cdot
\times                 -> times
\approx                -> approx
\oplus                 -> oplus
\sqrt{x}               -> sqrt { x }
\frac{a}{b}            -> { a } over { b }
\sum_j                 -> sum _ { j }
\operatorname{score}   -> score
\operatorname{softmax} -> softmax
\mathbf{q}             -> q
```

Examples of safe scripts:

```text
score ( i , j ) = q _ { i } cdot k _ { j }
theta _ { j } ^ { K } - theta _ { i } ^ { K }
e _ { i } = y _ { i } - yhat _ { i }
MAE = { 1 } over { n } sum _ { i = 1 } ^ { n } | e _ { i } |
RMSE = sqrt { { 1 } over { n } sum _ { i = 1 } ^ { n } e _ { i } ^ { 2 } }
```

Lint equation scripts for:

- empty script,
- raw LaTeX commands such as `\theta`, `\frac`, `\sum`,
- `cdotk` or `cdotq` missing spaces,
- malformed superscripts such as `^ { K - }`,
- malformed indices such as `_ { i } , t`,
- accidental renderer keywords that the current Hancom version may not support.

### Equation insertion workflow

Preferred method:

1. Find a known-good `hp:equation` object in the same document or a validated same-version sample.
2. Deep-clone it.
3. Replace only:
   - `hp:script` text,
   - object `id`,
   - `zOrder`,
   - hitbox size `hp:sz width/height`, if needed.
4. Keep `numberingType`, `version`, `baseLine`, `baseUnit`, `lineMode`, `font`, `pos`, `outMargin`, and `shapeComment` unless there is a specific reason to change them.
5. Insert into the intended `hp:run` or paragraph.
6. Remove affected `linesegarray`.
7. Validate actual equation count by XML local-name `equation`, not by broad text regex.
8. Inspect rendering when possible; structural validation cannot prove baseline or clipping.

For simple generated templates, a minimal inline equation object can work if a same-version sample confirms the shape:

```xml
<hp:equation id="1200000000" zOrder="1" numberingType="EQUATION"
  textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None"
  version="Equation Version 60" baseLine="86" textColor="#000000"
  baseUnit="1000" lineMode="CHAR" font="HancomEQN">
  <hp:sz width="6000" widthRelTo="ABSOLUTE" height="1800" heightRelTo="ABSOLUTE" protect="0"/>
  <hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0"
    holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA"
    vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/>
  <hp:outMargin left="0" right="0" top="0" bottom="0"/>
  <hp:shapeComment>수식입니다.</hp:shapeComment>
  <hp:script>y = beta _ { 0 } + beta _ { 1 } x + epsilon</hp:script>
</hp:equation>
```

Hitbox heuristics:

- plain variable or short inline expression: small width, height around `975` to `1200`,
- formulas with `over`, `sqrt`, or `sum`: larger width and height around `1600` to `2400`,
- long formulas: prefer a separate paragraph, not a crowded inline run,
- if clipping occurs in rendering, increase `hp:sz` height/width and remove `linesegarray` again.

Common pitfall: counting equations with a regex for the word `equation` may match attributes such as `equation="0"` in section numbering. Count actual XML elements whose local-name is `equation`.

## Images and BinData

Image handling is a three-way graph:

```text
section*.xml <hc:img binaryItemIDRef="imageN">
→ Contents/content.hpf <opf:item id="imageN" href="BinData/imageN.png" ...>
→ ZIP entry BinData/imageN.png
```

Do not assume `Contents/header.xml` contains image mappings. In real HWPX samples, image references may be entirely manifest-based.

### Reviewing images

For each `hc:img`:

1. Read `binaryItemIDRef`.
2. Find an `opf:item` with matching `id` in `Contents/content.hpf`.
3. Confirm its `href` exists in the ZIP.
4. Confirm `media-type` is plausible for the extension. Allow Hancom variants such as `image/jpg` for `.JPG`.
5. Report unused `BinData/` entries as warnings, not automatic errors; Hancom files may contain leftovers or preview-related assets.
6. Check figure captions and ordering if the document uses figures.

Preserve manifest details when cloning:

- extension case (`.JPG`, `.BMP`, `.PNG`),
- `media-type`, including Hancom variants,
- `isEmbeded="1"` spelling,
- optional `hashkey`,
- existing entry order if practical.

### Inserting images

Preferred method:

1. Convert unsupported or uncertain source images to PNG. Avoid SVG unless the target Hancom version is known to support it reliably.
2. Add a new ZIP entry under `BinData/`, e.g. `BinData/image7.png`.
3. Add a matching `opf:item` to `Contents/content.hpf` manifest, e.g. `id="image7" href="BinData/image7.png" media-type="image/png" isEmbeded="1"`.
4. Clone an existing `hp:pic` from the same document if possible.
5. Replace `hc:img binaryItemIDRef` with the new manifest ID.
6. Update geometry consistently:
   - `hp:orgSz`,
   - `hp:curSz`,
   - `hp:imgRect`,
   - `hp:imgClip`,
   - `hp:imgDim`,
   - `hp:sz`,
   - `hp:pos`,
   - `hp:renderingInfo` if the sample uses non-identity transforms.
7. Give the picture a unique object `id` and `zOrder`.
8. Add or update caption only when intended; keep caption sequence consistent.
9. Validate image graph and render if possible.

Do not insert figures by alphabetical order. Use explicit mapping from requested figure/caption to asset path.

## Tables

Tables are high-risk because they combine layout, border styles, nested paragraph lists, merged cells, and sometimes nested tables or form fields. Prefer cloning a similar table from the same document.

A typical table structure:

```xml
<hp:tbl rowCnt="..." colCnt="..." borderFillIDRef="..." ...>
  <hp:sz .../>
  <hp:pos .../>
  <hp:outMargin .../>
  <hp:inMargin .../>
  <hp:tr>
    <hp:tc borderFillIDRef="...">
      <hp:subList ...>
        <hp:p ...>...</hp:p>
      </hp:subList>
      <hp:cellAddr colAddr="0" rowAddr="0"/>
      <hp:cellSpan colSpan="1" rowSpan="1"/>
      <hp:cellSz width="..." height="..."/>
      <hp:cellMargin .../>
    </hp:tc>
  </hp:tr>
</hp:tbl>
```

Validation rules:

- Respect child order used by the source document.
- Compare `rowCnt` with direct `hp:tr` children.
- Compare cell occupancy using only direct `hp:tc` children under direct `hp:tr` children of that table.
- Do not count nested tables inside a cell's `hp:subList` as parent cells.
- Validate `cellAddr`, `cellSpan`, `cellSz`, `cellMargin` exist for each direct cell.
- Merged cells must not exceed declared `rowCnt`/`colCnt`.
- Preserve `repeatHeader`, `pageBreak`, `noAdjust`, `cellSpacing`, `treatAsChar`, `vertRelTo`, `horzRelTo`, table `borderFillIDRef`, and cell `borderFillIDRef` unless intentionally changing layout.
- For cell text edits, preserve cell paragraph styles and remove stale `linesegarray` in edited cell paragraphs.

Generation strategy:

- For simple result tables, clone an existing table with the desired border style and adjust text/row count carefully.
- If no table seed exists, generate a minimal table only for simple grids and validate aggressively.
- Avoid complex merged-cell tables from scratch unless required; they are easy to make structurally valid but visually wrong.

## Fields, forms, hyperlinks, formulas

Field controls are semantic objects, not plain text. Common field types in samples include:

- `CLICK_HERE`: form-like placeholder/input field,
- `HYPERLINK`: URL or internal link,
- `FORMULA`: table/formula field.

They appear as `hp:fieldBegin` with attributes and parameter children, followed later by matching `hp:fieldEnd`.

Rules:

- Preserve `fieldBegin`/`fieldEnd` pairs.
- Preserve `parameters` children unless intentionally changing field behavior.
- Do not flatten field content into plain text unless the user explicitly asks for a static document.
- When editing visible text near a field, avoid deleting the field markers.
- Validate counts and pair balance if the document contains fields.

## Captions, citations, footnotes, endnotes, headers, and footers

These objects affect submission quality and document meaning.

Captions:

- Detect figure/table captions by style name, caption controls, or text patterns such as `[그림 1]`, `그림 1.`, `[표 1]`, `표 1.`.
- Check numbering sequence.
- Ensure each referenced figure/table exists.
- Ensure image/caption mapping is explicit, not filename-sorted.

Citations:

- For numbered citations, check inline `[n]` references against bibliography `[n]` entries.
- Report missing or unused citation numbers.
- Do not invent bibliographic details.

Footnotes/endnotes:

- Preserve note controls and numbering settings.
- Check note references and note bodies remain paired.
- Avoid moving footnote/endnote controls across sections unless explicitly required.

Headers/footers/master pages:

- Multi-section documents may have different header/footer visibility and page settings.
- Preserve section `hp:secPr` unless the user asks for page layout changes.
- If editing headers/footers, validate all sections, not just `section0.xml`.

## Multi-section documents

Always resolve section order from `Contents/content.hpf` spine first. Multi-section files may have:

- independent page size/margins,
- landscape/portrait changes,
- columns,
- headers/footers/master pages,
- page border/fill changes,
- numbering restarts,
- footnote/endnote settings.

When editing multi-section documents:

- Determine which section contains the target text/object.
- Do not assume `section0.xml` is the whole document.
- Preserve `hp:secPr` in each section.
- Report section count and section order source.

## Repacking rules

When writing the output `.hwpx`:

1. Preserve original ZIP entry order when practical.
2. Write `mimetype` first and stored/uncompressed when practical.
3. Preserve original entries not intentionally modified.
4. Preserve `ZipInfo` metadata where practical, but do not let metadata preservation block correctness.
5. Use UTF-8 XML output.
6. Run `ZipFile.testzip()` after writing.
7. Reopen the output file and parse XML again.
8. Extract the edited/generated text back out to confirm the intended content is actually present.

Minimal repack pattern:

```python
with zipfile.ZipFile(out, 'w') as zout:
    for name in original_order:
        zi = zipfile.ZipInfo(filename=name, date_time=original_infos[name].date_time)
        zi.compress_type = zipfile.ZIP_STORED if name == 'mimetype' else zipfile.ZIP_DEFLATED
        zout.writestr(zi, entries[name])
```

## Layout validation ladder

Use the strongest practical validation available.

1. **Structural validation**: ZIP integrity, required parts, XML parse, section order, references, equation lint, image graph, table grid.
2. **Semantic extraction**: extract text, equation scripts, image refs, captions, citations, and field counts; confirm the intended edit is present.
3. **`rhwp` text/object smoke check**: if `rhwp` is available, use SVG/debug/page-dump tools only to confirm that paragraphs, equations, tables, images, and rough page flow are detected.
   - `rhwp export-svg file.hwpx --debug-overlay`
   - `rhwp dump-pages file.hwpx -p 0`
   - `rhwp dump file.hwpx -s 0 -p N`
   - Do not trust `rhwp` SVG as final visual rendering; equations may appear stretched/distorted and object geometry may differ from Hancom.
4. **Final visual validation**: open in Hancom Office and export/inspect PDF.

If level 3 is unavailable, state that only structural/semantic validation was performed. If level 3 was performed, report it as a weak text/object smoke check, not as proof of visual correctness. If level 4 is unavailable, say final Hancom/PDF visual layout is unverified.

## One-shot recipes

### Quick review of an HWPX

1. Run the validator script:
   ```bash
   SK=/home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts
   python "$SK/validate_hwpx.py" file.hwpx
   ```
2. Extract paragraph text and object counts:
   ```bash
   python "$SK/extract_hwpx_text.py" file.hwpx --format json -o file.extract.json
   ```
3. Inspect equations/images/tables/fields if present.
4. Report:
   - submission/opening risk,
   - critical structural issues,
   - recommended fixes,
   - evidence from package validation,
   - visual-layout limitation.

### Create a simple report/template HWPX

1. Prefer the helper script when a standard seed-based template is enough:
   ```bash
   SK=/home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts
   python "$SK/create_hwpx_from_seed.py" --out report.hwpx --title "보고서 제목" --paragraph "본문"
   ```
2. For structured input, pass JSON with `title`, `subtitle`, `meta`, and `sections`.
3. Before writing, convert the user's requested format/rubric/sample into a checklist: required headings, labels, paragraph density, tables, figures, equations, captions, references, and placeholders.
4. Generate medium-density content by default. Do not return a barely filled skeleton unless the user explicitly asked for an empty template.
5. Use clear paragraph spacing: no accidental blank-line clusters, no object-to-object crowding, and separate long equations/tables/figures with explanatory text.
6. The helper preserves package/header/section properties, updates `content.hpf` metadata and `Preview/PrvText.txt`, then validates.
7. Add equations/images/tables with the dedicated helper scripts only after the base document validates.
8. Extract text/object metadata after packaging and compare it against the checklist. Fix missing sections, too-short bodies, missing equation objects, and unreadable spacing before finalizing.
9. Return file path and validation summary.

### Add or replace real HWP equation objects

1. To append a new formula, prefer:
   ```bash
   SK=/home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts
   python "$SK/add_equations_hwpx.py" in.hwpx --out out.hwpx --equation "MSE::MSE = { 1 } over { n } sum _ { i = 1 } ^ { n } e _ { i } ^ { 2 }"
   ```
2. To replace an existing formula in a template while preserving placement/hitbox, prefer:
   ```bash
   python "$SK/replace_equations_hwpx.py" in.hwpx --out out.hwpx --index 0 --script "RMSE = sqrt { { 1 } over { n } sum _ { i = 1 } ^ { n } e _ { i } ^ { 2 } }"
   ```
3. Convert LaTeX-like input to HWP equation script first.
4. `add_equations_hwpx.py` assigns unique `id`/`zOrder`, sets a generous hitbox, appends the equation paragraph, updates preview text, and validates.
5. `replace_equations_hwpx.py` changes only `hp:script` text by equation occurrence index; it preserves `hp:equation` object attributes, IDs, hitbox, wrapping, and position.
6. If hand-editing instead, inspect sample equation shape, clone or generate minimal `hp:equation`, remove affected `linesegarray`, and validate.

### Insert or replace an image

1. To insert a new image, prefer:
   ```bash
   SK=/home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts
   python "$SK/insert_image_hwpx.py" in.hwpx --image figure.png --caption "그림 1. 구조" --out out.hwpx
   ```
2. To replace an existing image slot while preserving its position/size/caption, prefer:
   ```bash
   python "$SK/replace_image_hwpx.py" in.hwpx --image new_figure.png --index 0 --out out.hwpx
   python "$SK/replace_image_hwpx.py" in.hwpx --image new_figure.png --ref image3 --out out.hwpx
   ```
3. `insert_image_hwpx.py` updates the full graph: ZIP `BinData/...`, `Contents/content.hpf` manifest item, and section `hp:pic`/`hc:img binaryItemIDRef`.
4. `replace_image_hwpx.py` updates the `content.hpf` manifest and `BinData` bytes but does not modify the section `hp:pic`; geometry, wrapping, zOrder, caption location, and object IDs are preserved.
5. Use replacement when a template already has the correct figure slot. Use insertion when adding a new figure.

### Insert or replace a simple table

1. To insert a new simple grid, prefer:
   ```bash
   SK=/home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts
   python "$SK/insert_table_hwpx.py" in.hwpx --out out.hwpx --rows '[["항목","값"],["A","10"]]'
   ```
2. To replace cell text in an existing simple table while preserving geometry/styles, prefer:
   ```bash
   python "$SK/replace_table_cells_hwpx.py" in.hwpx --out out.hwpx --index 0 --rows '[["항목","새 값"],["A","20"]]'
   python "$SK/replace_table_cells_hwpx.py" in.hwpx --out out.hwpx --index 1 --csv data.csv
   ```
3. `insert_table_hwpx.py` uses existing style refs and a visible `borderFillIDRef`; it is intended for simple grids.
4. `replace_table_cells_hwpx.py` keeps `hp:tbl`/`hp:tc` geometry, borders, margins, zOrder, wrapping, and paragraph style IDs, and replaces only cell text nodes.
5. For merged/nested/public-form tables, clone a same-document table manually or use replacement only after validation; simple regex-based cell replacement is intentionally conservative.

### Fill a form-like HWPX

1. Prefer conservative placeholder filling:
   ```bash
   SK=/home/mattc/.hermes/skills/productivity/hwpx-document-processing/scripts
   python "$SK/fill_placeholders_hwpx.py" form.hwpx --out filled.hwpx --map '{"{{name}}":"홍길동"}'
   ```
2. Default mode only replaces placeholders inside single `<hp:t>` nodes, preserving `fieldBegin`/`fieldEnd` and other controls.
3. Use `--paragraph-mode` only for simple templates with split placeholders; it may collapse styling within that paragraph.
4. Validate field counts and text extraction.
5. Render or open in Hancom if the form layout matters.

## Common pitfalls

1. **Treating HWPX like DOCX or Markdown.** HWPX is OWPML inside ZIP; use XML/package validation.
2. **Assuming XML parse means success.** Broken style/image references may still parse but render incorrectly.
3. **Counting equations by regex.** Count XML elements with local-name `equation`; regex can match attributes like `equation="0"`.
4. **Forgetting `content.hpf` for images.** Real files often map `imageN` through `content.hpf`, not `header.xml`.
5. **Breaking `isEmbeded`/extension/media details.** Preserve Hancom quirks when cloning image manifest entries.
6. **Counting nested table cells as parent cells.** Only direct `tr`/`tc` children belong to a table's own grid.
7. **Flattening fields.** `CLICK_HERE`, `HYPERLINK`, and `FORMULA` controls are semantic; preserve pairs and parameters.
8. **Leaving stale `linesegarray`.** Edited text/equations may overlap or clip if stale layout caches remain.
9. **Inventing style IDs.** Every `styleIDRef`, `paraPrIDRef`, and `charPrIDRef` must exist in `header.xml`.
10. **Compressing or reordering `mimetype` carelessly.** Keep it first and stored/uncompressed when practical.
11. **Changing `section0.xml` only in multi-section docs.** Resolve and inspect all sections.
12. **Inserting figures by filename order.** Use explicit figure-to-caption mapping.
13. **Overclaiming visual layout.** `rhwp` SVG/page rendering is a weak smoke check only and can distort equations; final visual claims require Hancom Office or Hancom-exported PDF.
14. **Overusing plain Unicode math.** In HWPX generation, most substantive formulas should be real `hp:equation` objects; reserve Unicode inline math for isolated symbols and tiny mentions.
15. **Returning a structurally valid but underwritten document.** A generated 논문/보고서 with only headings and one-line filler is a failed artifact unless the user asked for a blank skeleton. Add realistic sample content or descriptive placeholders.
16. **Ignoring the user's supplied format.** Do not silently change heading names, section order, required labels, table columns, equation labels, or rubric items. Treat them as a schema and verify extracted output against it.
17. **Letting equations degrade into text.** Raw LaTeX, Unicode approximation, or missing `hp:equation` objects often looks acceptable in extracted text but fails the HWPX requirement. Validate actual equation elements and scripts.
18. **Bad whitespace from AI generation.** Repeated empty paragraphs, cramped equation/table placement, and missing section gaps reduce readability even when XML is valid. Inspect paragraph sequence and object adjacency.

## Validation checklist before final response

For every edited or generated HWPX, report as many of these as apply:

- Output file path.
- ZIP signature and `testzip()` result.
- Required package parts present/missing.
- XML parse status.
- Section count and section order source.
- Paragraph count and extracted-text sanity check.
- Requested-format checklist coverage: required headings, labels, tables, figures, equations, references, and placeholders present.
- Content density check: no unintended one-line sections, missing bodies, or overly empty sample/template areas.
- Readability/spacing check from extracted paragraph order: no accidental blank-line clusters, no cramped object adjacency, consistent section separation.
- Cross-file reference status for style/paragraph/character/border/tab/numbering refs.
- Equation object count, scripts, lint warnings, and coverage against the intended formula list.
- Image `binaryItemIDRef` → manifest → BinData resolution.
- Table count and grid/span warnings.
- Field counts and field pair warnings.
- Caption and citation consistency if relevant.
- Whether stale `linesegarray` was removed from edited paragraphs.
- Whether `rhwp` weak text/object smoke check was performed, if used.
- Whether Hancom/PDF visual validation was performed.
- Remaining limitations.

## Output style

For reviews, answer result-first in Korean:

1. 제출 가능 여부 or structural safety verdict.
2. Critical issues, if any.
3. Recommended fixes.
4. Verified evidence from ZIP/XML/text/equation/image/table/field checks.
5. Limitations, especially final visual rendering if no Hancom/PDF check was done. Do not present `rhwp` output as visual proof.

For edits/generation, include:

- created/edited file path,
- concise validation summary,
- what changed,
- any warnings,
- whether visual layout still needs Hancom/PDF confirmation.

Keep the final user response concise, but never omit a material blocker or validation limitation.
