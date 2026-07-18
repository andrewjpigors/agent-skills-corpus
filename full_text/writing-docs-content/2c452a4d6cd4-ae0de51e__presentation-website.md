---
name: presentation-website
description: "Convert a medical paper (PDF, PPTX, Markdown, or folder with supplements) into a scrollable, slide-based HTML presentation website with embedded figures, screenshot-based PDF/PPTX download (html2canvas + jsPDF/PptxGenJS), designed for journal reading presentations (10-15 min)."
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Journal Presentation

## Overview

When a user provides a medical paper and requests a **journal presentation** (網站報告 / HTML 簡報) for a journal reading or morning meeting (晨會), use this skill to generate a self-contained HTML file. The input can be:

- **A single file** — PDF, PPTX, or Markdown
- **A folder** containing the main paper plus supplementary files (e.g., supplement PDFs, appendix tables, additional figures downloaded from the journal website)

The generated HTML includes:

- Scrollable full-screen slides with keyboard/scroll navigation
- Figures & tables extracted from all source files (main + supplements)
- Professional, clean aesthetic (style is flexible — not locked to any specific theme)
- One-click PDF download with print-optimized CSS
- Mandatory Outline slide (table of contents) and Ending slide (thank you / Q&A)
- When an existing PPTX draft is present, use it as a structural reference and source of supplementary info (presenter name, awards, logos, etc.)

## Prerequisites

1. **PyMuPDF** (`fitz`) for PDF reading and figure extraction:
   ```bash
   pip3 install pymupdf
   ```
2. **python-pptx** for PPTX reading and image extraction:
   ```bash
   pip3 install python-pptx
   ```
3. macOS environment with a modern browser (Chrome/Safari/Edge).

## Workflow

Follow these steps precisely:

### 0a. Ask for Presenter Information

Before starting any processing, **ask the user** for presenter information. This ensures the title slide and ending slide display the correct names. Present the question concisely — the user may skip it:

> **Presenter info:** Who is presenting and who is the supervisor? (e.g., "R2 王大明 / VS 李教授") — press Enter to skip.

- If the user provides names → use them on the title slide and ending slide
- If the user skips (empty reply or says "skip" / "略過") → check memory for saved user profile; if none found, leave presenter info blank or use a generic placeholder ("Presenter / Supervisor")
- If an existing PPTX draft contains presenter/supervisor names → use those as defaults (still ask to confirm)
- Only ask **once** at the beginning — do not re-ask during the workflow

### 0b. Identify Input & Create Output Folder

#### Detect input type

The user may provide:
- **A single file** (PDF, PPTX, or Markdown) → treat it as the main source
- **A folder path** → scan the folder for all relevant files (main paper + supplements)
- **Multiple paths** (e.g., a folder + a PDF) → treat accordingly

**IMPORTANT: Also scan for subfolders.** The user's folder may contain a subfolder with an existing PPTX draft and pre-extracted figures (e.g., `*_journal_reading/`, `*_presentation/`). Always recursively check for PPTX files in subfolders.

```python
import os, re, glob

user_input = "..."  # path provided by user

if os.path.isdir(user_input):
    # Folder input: find all PDFs, PPTX, images, and supplementary files
    input_dir = user_input
    all_pdfs = sorted(glob.glob(os.path.join(input_dir, "*.pdf")))
    # Recursively find PPTX files (may be in subfolders)
    all_pptx = sorted(glob.glob(os.path.join(input_dir, "**/*.pptx"), recursive=True))
    all_images = sorted(
        glob.glob(os.path.join(input_dir, "*.png")) +
        glob.glob(os.path.join(input_dir, "*.jpg")) +
        glob.glob(os.path.join(input_dir, "*.jpeg")) +
        glob.glob(os.path.join(input_dir, "*.tif")) +
        glob.glob(os.path.join(input_dir, "*.tiff"))
    )
    # Also check subfolder figures/ directories for pre-extracted images
    for subfolder in glob.glob(os.path.join(input_dir, "*/figures/")):
        all_images += sorted(glob.glob(os.path.join(subfolder, "*.*")))
    # Identify main paper vs supplements by filename heuristics
    main_pdf = None
    supplement_pdfs = []
    for pdf in all_pdfs:
        basename = os.path.basename(pdf).lower()
        if any(kw in basename for kw in ["suppl", "supplement", "appendix", "table_s", "figure_s", "digital content"]):
            supplement_pdfs.append(pdf)
        elif main_pdf is None:
            main_pdf = pdf
        else:
            if os.path.getsize(pdf) > os.path.getsize(main_pdf):
                supplement_pdfs.append(main_pdf)
                main_pdf = pdf
            else:
                supplement_pdfs.append(pdf)
    # Find existing PPTX draft (prioritize by file size — largest is likely the most complete)
    main_pptx = max(all_pptx, key=os.path.getsize) if all_pptx else None
    print(f"Main paper: {main_pdf}")
    print(f"Existing PPTX draft: {main_pptx}")
    print(f"Supplements: {supplement_pdfs}")
    print(f"Standalone images: {all_images}")
else:
    # Single file input
    main_pdf = user_input if user_input.endswith('.pdf') else None
    main_pptx = user_input if user_input.endswith('.pptx') else None
    input_dir = os.path.dirname(user_input)
    supplement_pdfs = []
    all_images = []
```

#### Create output folder

Create a dedicated output folder **in the same directory as the input**:

```
{ShortTitle}_presentation/
├── presentation_images/    ← extracted figures (from main + supplements)
├── presentation.html       ← development version (external images)
└── presentation_portable.html  ← self-contained portable file
```

**Naming convention:** derive `{ShortTitle}` from the paper title — use 3-5 key English words in snake_case, e.g.:
- "The Effect of Topical Tranexamic Acid on..." → `topical_TXA_rhinoplasty_presentation/`
- "A Randomized Trial of Platelet-Rich Plasma..." → `PRP_randomized_trial_presentation/`

```python
paper_title = "..."  # extracted from the paper
short = "_".join(paper_title.split()[:5]).replace("/","_")
short = re.sub(r'[^a-zA-Z0-9_\-]', '', short)
base_dir = input_dir if os.path.isdir(user_input) else os.path.dirname(user_input)
output_dir = os.path.join(base_dir, f"{short}_presentation")
os.makedirs(os.path.join(output_dir, "presentation_images"), exist_ok=True)
```

All subsequent steps must write output files into this `output_dir`.

### 1. Read All Source Files — Paper-First Strategy

**The PDF original paper is ALWAYS the primary content source.** All academic content (methods, results, statistics, discussion) must be derived from the paper itself. When an existing PPTX draft is found, it serves as a **structural reference** and a source of **supplementary information not found in the paper** (e.g., presenter name, supervisor, presentation occasion, awards, logos, badges).

#### Priority order

| Priority | Source | Role |
|----------|--------|------|
| **1st** | **PDF original paper** | **Primary content source:** all academic content — title, authors, methods, results, statistics, discussion, conclusions. This is the authoritative source for all data and claims. |
| **2nd** | **Existing PPTX draft** (if present) | **Structural reference + supplementary info:** slide organization can be referenced as a guide; extract presenter/supervisor names, presentation occasion, cover page elements (logos, badges, award images), and any user-added context not in the paper. The PPTX may also suggest emphasis choices or content organization preferences. |
| **3rd** | **Supplement PDFs** | Additional figures, tables, extended data, sensitivity analyses |

> **Key distinction:** The PPTX draft is created by the user and may contain information the paper does not have (presenter name, supervisor, which conference it's for, award badges, custom logos). Always extract these. But for academic content (methods, results, p-values, discussion points), the paper is authoritative — the PPTX is only a reference for how the user chose to organize it.

#### Step 1a: Read the PDF original paper

Read the main paper PDF to extract all content — this is the **primary step**:

| Format | How to read | Notes |
|--------|-------------|-------|
| **PDF** (`.pdf`) | Use the `Read` tool with `pages` parameter | Most common for journal papers |
| **Markdown** (`.md`) | Use the `Read` tool directly | Plain text with optional image references |

#### Step 1b: Read the existing PPTX draft (if found)

Use `python-pptx` to extract the **structure and supplementary info** from every slide:

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = Presentation(pptx_path)
for slide_idx, slide in enumerate(prs.slides):
    print(f"\n=== Slide {slide_idx + 1} ===")
    for shape in slide.shapes:
        print(f"Shape: {shape.shape_type}, name={shape.name}")
        if hasattr(shape, 'text') and shape.text:
            print(f"  Text: {repr(shape.text[:300])}")
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            print(f"  IMAGE: {shape.image.content_type}, size={shape.image.size}")
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            for child in shape.shapes:
                if hasattr(child, 'text') and child.text:
                    print(f"    Child text: {repr(child.text[:200])}")
                if child.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    print(f"    Child IMAGE: {child.image.content_type}")
```

From the PPTX draft, extract **supplementary info and structural cues**:
- **Title slide**: presenter name, supervisor name, logos, cover images, journal badges, award images
- **Outline slide**: section names and numbering (can be referenced as a structural guide)
- **Slide organization**: how the user chose to organize content (reference, not authoritative — the paper's own structure takes priority)
- **Embedded images**: cover logos, badges, award images, and any user-added visuals not in the paper
- **Ending slide**: thank you message, Q&A prompt, presenter info

#### Step 1c: Read supplement PDFs

Read each supplement PDF as well — these often contain important supplementary tables, figures, methods, and sensitivity analyses.

#### Step 1d: Copy standalone images

Copy any standalone images (e.g., high-res figures downloaded from the journal website) directly into `presentation_images/`:
```python
import shutil
for img in all_images:
    shutil.copy2(img, os.path.join(output_dir, "presentation_images", os.path.basename(img)))
```

#### What to extract and cross-reference:
- Title, authors, journal, year (from paper)
- Presenter and supervisor names (from PPTX if available — not in PDF)
- Cover images / logos / badges (from PPTX if available)
- Study design, methods, intervention, control (from paper)
- Key results: tables, figures, p-values (from paper)
- Conclusions and clinical implications (from paper)
- Supplementary data (additional tables, figures, sensitivity analyses)

### 2. Extract Figures from All Source Files

Apply the extraction process to **all source files** — main paper AND supplement PDFs. Supplement PDFs often contain high-resolution versions of figures, extended data tables, and flow diagrams.

The extraction method depends on the input format.

#### 2a. From PDF — Three-tier approach

Use a **three-tier approach** for maximum accuracy: (1) caption-aware embedded extraction, (2) automatic block-based detection, (3) visual refinement only when needed.

> ⚠️ **CRITICAL — DO NOT use `page.get_images()` indices to name files.**
> `page.get_images(full=True)` returns images in **xref order** (PDF resource
> dictionary order), NOT spatial / reading order. When a page has multiple
> figures, naming `embedded_p{N}_1`, `embedded_p{N}_2` produces SWAPPED labels.
> Real failure: in the Kappenstein 2026 thyroid paper, page 5 returned FIG 3
> (bottom) before FIG 2 (top), and page 6 returned FIG 5 before FIG 4. Always
> use the caption-aware helper below — it sorts by spatial bbox position and
> matches each image to its "FIG. N" caption text block.

```python
import fitz
import os
import sys

# Use the caption-aware helper from the journal-reading skill
SKILL_SCRIPTS = "<absolute path to>/.claude/skills/journal-reading/scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from extract_figures_by_caption import extract_figures_with_captions

pdf_path = "paper.pdf"
out_dir = os.path.join(output_dir, "presentation_images")  # inside the output folder
os.makedirs(out_dir, exist_ok=True)

# ──────────────────────────────────────────────
# TIER 1: Caption-aware extraction (REQUIRED)
# Maps each embedded image to its FIG N caption by:
#  - sorting images by bbox.y0 (true spatial order)
#  - finding nearest "FIG. N" / "Figure N" text block below the image
#  - naming files as fig1.{ext}, fig2.{ext}, etc.
# Falls back to img_p{N}_pos{M} for images with no caption (logos, etc.)
# ──────────────────────────────────────────────
saved = extract_figures_with_captions(pdf_path, out_dir)
# saved is a list of dicts with {filename, fig_num, label, page, xref, bbox, size, ext}

doc = fitz.open(pdf_path)  # keep doc open for Tier 2 / 3 below

# ──────────────────────────────────────────────
# TIER 2: Block-based detection for precise bounding boxes
# Use get_text("dict") to find image blocks with exact coordinates.
# ──────────────────────────────────────────────
PADDING = 8  # points of padding around detected regions to avoid boundary cuts

for page_idx in range(len(doc)):
    page = doc[page_idx]
    blocks = page.get_text("dict")["blocks"]
    img_blocks = [b for b in blocks if b["type"] == 1]  # type 1 = image blocks
    for i, block in enumerate(img_blocks):
        bbox = block["bbox"]  # (x0, y0, x1, y1) in points — precise!
        print(f"  Page {page_idx+1} image block {i+1}: bbox={bbox}")

# ──────────────────────────────────────────────
# TIER 3: Full-page renders + padded crop (for figures/tables
# that span multiple blocks or need caption inclusion)
# ──────────────────────────────────────────────
scale = 2.5
mat = fitz.Matrix(scale, scale)
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=mat)
    pix.save(os.path.join(out_dir, f"page_{i+1}.png"))

def crop_save(page_idx, rect_tuple, filename, padding=PADDING):
    """Crop a region from a PDF page with padding to avoid boundary cuts.

    Args:
        page_idx: 0-based page index
        rect_tuple: (x0, y0, x1, y1) in PDF points
        filename: output filename
        padding: extra points around the region (default 8pt)
    """
    page = doc[page_idx]
    page_rect = page.rect
    # Apply padding, clamped to page boundaries
    x0 = max(rect_tuple[0] - padding, page_rect.x0)
    y0 = max(rect_tuple[1] - padding, page_rect.y0)
    x1 = min(rect_tuple[2] + padding, page_rect.x1)
    y1 = min(rect_tuple[3] + padding, page_rect.y1)
    clip = fitz.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(matrix=fitz.Matrix(3.0, 3.0), clip=clip)
    pix.save(os.path.join(out_dir, filename))

doc.close()
```

#### Figure extraction decision guide

| Scenario | Method | Notes |
|----------|--------|-------|
| Standalone photo/chart embedded as raster image | **Tier 1** (`extract_image`) | Best quality — uses the original embedded image at native resolution, no re-rendering artifacts |
| Need precise crop of a figure region | **Tier 2** (`get_text("dict")` bounding boxes) → feed bbox into `crop_save()` | Use the detected bbox coordinates directly instead of guessing |
| Complex figure with caption, or table spanning text | **Tier 3** (visual inspection + `crop_save()`) | Read the full-page PNGs to identify regions, then use `crop_save()` with default 8pt padding |
| Vector graphics (charts drawn with PDF primitives) | **Tier 3** with higher scale (3.5–4.0) | Vector art won't appear in `get_images()`; must be rendered from the page |

**Key principles to avoid cut-off, noise, AND mis-labelled figures:**
- **Always use padding** (default 8pt) when cropping — `crop_save()` handles this automatically
- **Tier 1 must be caption-aware** — use `extract_figures_with_captions()` from the journal-reading skill's `scripts/extract_figures_by_caption.py`; never name files by `get_images()` index
- **Use Tier 2 bounding boxes** instead of manually guessing coordinates — `get_text("dict")` returns pixel-accurate positions
- **For tables**: include 15-20pt padding to capture outer borders and column headers
- **Verify FIG-N mapping AND content**: after Tier 1, read each `figN.{ext}` with the Read tool and confirm the image content matches what FIG N is described as in the paper. The caption-matcher is robust on standard journal layouts but can fail on multi-panel figures with sub-captions only ("a)", "b)" without "FIG N"); always cross-check.
- **Verify Tier-2/3 crops visually**: re-read each cropped image to confirm no clipping or noise before proceeding to HTML generation.

#### 2b. From PPTX — Extract embedded images

Use `python-pptx` to extract all images from the PPTX slides:

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import os

pptx_path = "presentation.pptx"
out_dir = os.path.join(output_dir, "presentation_images")  # inside the output folder
os.makedirs(out_dir, exist_ok=True)

prs = Presentation(pptx_path)
img_count = 0

for slide_idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            img_count += 1
            image = shape.image
            ext = image.content_type.split('/')[-1]  # png, jpeg, etc.
            if ext == 'jpeg':
                ext = 'jpg'
            filename = f"slide{slide_idx+1}_img{img_count}.{ext}"
            with open(os.path.join(out_dir, filename), 'wb') as f:
                f.write(image.blob)
            print(f"  Extracted: {filename} ({image.size[0]}x{image.size[1]})")
        elif shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            # Recursively check grouped shapes for images
            for child in shape.shapes:
                if child.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    img_count += 1
                    image = child.image
                    ext = image.content_type.split('/')[-1]
                    if ext == 'jpeg':
                        ext = 'jpg'
                    filename = f"slide{slide_idx+1}_img{img_count}.{ext}"
                    with open(os.path.join(out_dir, filename), 'wb') as f:
                        f.write(image.blob)
                    print(f"  Extracted: {filename}")
```

#### 2c. From Markdown — Resolve image references

Markdown files may contain image references in these formats:
- `![alt](path/to/image.png)` — local file path
- `![alt](https://...)` — remote URL (download with `curl` or `urllib`)

```python
import re, os, shutil, urllib.request

md_path = "paper.md"
out_dir = os.path.join(output_dir, "presentation_images")  # inside the output folder
os.makedirs(out_dir, exist_ok=True)

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

md_dir = os.path.dirname(os.path.abspath(md_path))
images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', md_content)

for idx, (alt, src) in enumerate(images):
    ext = os.path.splitext(src)[-1] or '.png'
    filename = f"md_img{idx+1}{ext}"
    dest = os.path.join(out_dir, filename)
    if src.startswith(('http://', 'https://')):
        urllib.request.urlretrieve(src, dest)
    else:
        local = os.path.join(md_dir, src)
        if os.path.exists(local):
            shutil.copy2(local, dest)
    print(f"  Resolved: {alt or 'image'} -> {filename}")
```

If the Markdown has no images, skip figure extraction entirely and generate a text-only presentation.

### 3. Generate the HTML Presentation

Use the template structure in `templates/presentation_template.html` as a **starting reference for HTML/CSS/JS features**, but the visual style is flexible — any professional, clean design is acceptable.

#### 3a. Slide Structure — Paper-First with Optional PPTX Reference

**The paper's own section structure is the primary guide** for organizing slides. When an existing PPTX draft is found, it may be referenced as a structural guide (e.g., how the user chose to split or combine sections), but the paper's content and organization take priority.

**When an existing PPTX draft is found:**
- Reference the PPTX slide organization as a guide for how the user prefers to structure the presentation.
- Preserve all custom elements from the PPTX cover (presenter name, supervisor, logos, journal badges, award images, DOI, trial registration numbers).
- The paper defines the academic content and section structure — the PPTX may suggest how to split or group that content.

**When NO PPTX draft exists (PDF-only mode):**
- Fall back to the default structure below.

#### Mandatory slides (always required regardless of source):

| Position | Slide | Content |
|----------|-------|---------|
| **2nd slide** | **Outline** | Numbered list of all sections in the presentation. This serves as a table of contents and must match the actual slide titles that follow. **IMPORTANT:** Do NOT add empty placeholder items (e.g., empty `.outline-item` divs) to pad a grid layout — only include items that correspond to actual sections. Empty items cause visual artifacts (blank numbered circles) and cannot be edited. |
| **Last slide** | **Ending** | "Thank you — Questions?" slide with presenter info. May also include key references or a brief clinical pearl summary. |

#### Default structure (when no PPTX draft exists):

| Slide | Section | Content |
|-------|---------|---------|
| 1 | **Title** | Paper title, authors, journal, LOE, presenter info |
| 2 | **Outline** | Numbered table of contents |
| 3 | **Background** | Clinical problem, knowledge gap, study rationale |
| 4 | **Study Objective & PICO** | Objective, PICO table, intervention mechanism |
| 5 | **Methods — Design & Intervention** | Study design, surgical technique, intervention vs control |
| 6 | **Methods — Outcome Assessment** | Photography, scoring, grading scales (text) |
| 7 | **Methods — Grading Scales & Statistics** | Grading scale images, statistical methods |
| 8 | **Results — Demographics** | Table 1, baseline characteristics |
| 9 | **Results — Primary Outcome A** | Table + figures + key finding |
| 10 | **Results — Primary Outcome B** | Table + figures + key finding |
| 11 | **Results — Summary Comparison** | Head-to-head comparison table of outcomes |
| 12 | **Results — Clinical Photographs** | Side-by-side clinical photos (if available) |
| 13 | **Discussion — Key Findings** | Main results interpretation |
| 14 | **Discussion — Mechanism** | Why the results differ, pathophysiology |
| 15 | **Discussion — Literature** | Comparison with existing studies |
| 16 | **Discussion — Strengths & Limitations** | Two-column layout |
| 17 | **Discussion — Clinical Implications** | Practical takeaways |
| 18 | **Discussion — Future Research** | Research directions |
| 19 | **Conclusions** | Key findings + clinical pearl |
| 20 | **Ending** | "Thank you — Questions?" |

> **Note:** Not every paper needs all 20 slides. Adjust based on content — the key principle is that **each slide must fit comfortably within the viewport** without overflow. Split dense content into multiple slides rather than cramming.

#### 3b. Slide Density & Font Sizing (Critical for PDF/PPTX Export)

**Every slide must respect the 16:9 viewport ratio.** Content that overflows the visible area will be cut off in PDF export and produce broken PPTX output. Design each slide as if it were a fixed-size PowerPoint slide — no scrolling.

**Content density rules:**
- **Max 5–6 bullet points** per card; max 2 cards per slide
- **Max 1 table + 2 figures** per slide (table on top, figures below)
- If a slide has both a table AND a highlight box AND figures, it is too dense — split it
- **Two-column layouts:** max 5 items per column
- If content exceeds these limits, **split into multiple slides** rather than shrinking fonts

**Font sizing for projection readability** (assuming `html { font-size: 18px; }`):

| Element | Minimum Size | Notes |
|---------|-------------|-------|
| `.section-header` | 1.5rem (27px) | Slide title — must be readable from back of room |
| `.card li`, `.card p` | 1.05rem (19px) | Body text — primary reading content |
| `.data-table` | 1rem (18px) | Table cells — avoid going below this |
| `.highlight-box`, `.key-point` | 1.05rem (19px) | Emphasis boxes |
| `.figure-caption` | 0.8rem (14px) | Captions can be smaller |
| `.slide-counter` | 14px | Page numbers |
| `.outline-text` | 0.95rem (17px) | TOC items |

**Base font size:** Use `html { font-size: 18px; }` (not 16px) as the base. This ensures all `rem`-based sizes scale up for projection. PDF/PPTX export uses html2canvas screenshot (not print CSS), so the screen font size is what appears in the exported files.

**When splitting slides, update:**
1. The Outline slide to reflect the new section list
2. All `.slide-counter` values (X / N) — the total N must be correct
3. The nav dots will auto-generate from the slide count

#### 3c. Required HTML Features

The visual style does not need to follow a fixed theme. Any **professional, clean** design is acceptable as long as it includes the following functional requirements:

1. **CSS Variables** for easy theming (colors are flexible):
   ```css
   :root {
     --primary: #1a5276;      /* or any professional color */
     --primary-light: #2980b9;
     --accent: #e74c3c;
     --success: #27ae60;
   }
   ```

2. **Navigation system:**
   - Right-side dot navigation with hover tooltips
   - Top progress bar
   - Keyboard support: Arrow Up/Down/Left/Right, Space, PageUp/PageDown — must also work with presentation clickers (投影筆), which typically send ArrowRight/ArrowLeft or PageDown/PageUp
   - **IMPORTANT:** `e.preventDefault()` must be called **before** calculating the current slide index — this prevents the browser's native scroll-snap from firing and conflicting with `scrollIntoView`
   - `scroll-snap-type: y mandatory` for smooth slide snapping

3. **Content layout** (card-based or any clean layout):
   - Clear visual hierarchy for sections
   - Grid layouts for side-by-side content
   - Highlighted boxes for important findings
   - Key-point summary boxes

4. **Figure display:**
   - `<img src="presentation_images/fig1.png">` with caption
   - Side-by-side figure grids
   - Max-height constraints for consistent sizing

5. **Data tables:**
   - Clean headers with contrast
   - `.sig` class for significant p-values (red, bold)
   - Highlight rows for inter-group comparisons

6. **Colored slides:**
   - Title slide: gradient background
   - Conclusion / ending slide: distinct background
   - Content slides: light neutral background

7. **Slide numbers (mandatory):**
   - Every slide must display a page number in the format `"X / N"` (e.g., "3 / 11") at the bottom-right corner
   - Use the `.slide-counter` class: `<div class="slide-counter">3 / 11</div>` inside each `<section class="slide">`
   - Styled as small, muted text (opacity 0.6); on dark slides use light text

8. **Fade-in animations:**
   - IntersectionObserver on `.fade-in` elements
   - Translate Y + opacity transition

9. **Double-click source text popup (MANDATORY — 100% coverage):**
   - **CRITICAL REQUIREMENT: EVERY single content block** — every `.card`, `.key-point`, `.highlight-box`, and `.figure-container` — **MUST** include a hidden `<div class="source-text">` element containing the corresponding original paper excerpt. This is a **non-negotiable** requirement. No content block should be left without a source text popup. The user relies on this for Q&A fact-checking during the live presentation — every point must be traceable to the paper.
   - **Coverage rule:** When generating the HTML, go through each slide systematically and ensure every card/key-point/highlight-box has a `<div class="source-text">` with a relevant excerpt. Only purely structural elements (outline items, recommendation summary table headers, ending slide decorative elements) are exempt.
   - **Prefer direct quotes** from the PDF whenever possible. Use paraphrased summaries only when the content synthesizes multiple sections or when no single passage covers the point.
   - **Double-clicking** any block opens a centered modal popup showing the source text
   - The JS parent selector must include all block types: `.closest('.card, .key-point, .highlight-box, .figure-container, .slide-inner')`
   - **Two source types** distinguished by `data-type` attribute:
     - **Direct quotes** (from the PDF): `<div class="source-text"><blockquote>"Exact quote..."</blockquote></div>` — modal shows "Original Text"
     - **Paraphrased** (when PDF is not available or content is summarized): `<div class="source-text" data-type="paraphrase"><blockquote>Paraphrased content...</blockquote></div>` — modal shows "Source Text (Paraphrased)"
   - The modal label element needs `id="sourceModalLabel"` so JS can update it dynamically
   - Blocks with source text show a faint "double-click to view original text" hint on hover
   - **Figure containers** need special CSS to avoid layout shift: `.figure-container.has-source { position: relative; }` with `::after { position: absolute; bottom: 4px; }`
   - The `.source-text` element is hidden via CSS (`display: none`) — it only serves as a data container
   - HTML patterns:
     ```html
     <!-- Direct quote from paper -->
     <div class="card">
       <ul><li>Key finding summarized...</li></ul>
       <div class="source-text">
         <blockquote>"Exact quote from the paper..."</blockquote>
       </div>
     </div>
     <!-- Paraphrased content -->
     <div class="key-point">
       <strong>Key point text...</strong>
       <div class="source-text" data-type="paraphrase">
         <blockquote>Paraphrased summary of the relevant paper section.</blockquote>
       </div>
     </div>
     <!-- Highlight box with source text -->
     <div class="highlight-box">
       <strong>Note:</strong> Important note text...
       <div class="source-text">
         <blockquote>"Relevant quote from the paper..."</blockquote>
       </div>
     </div>
     <!-- Figure with source text -->
     <div class="figure-container">
       <img src="presentation_images/fig1.png" alt="Figure 1">
       <div class="figure-caption">Figure 1: Description</div>
       <div class="source-text" data-type="paraphrase">
         <blockquote>Description of what this figure shows from the paper.</blockquote>
       </div>
     </div>
     ```
   - **IMPORTANT (double-click reliability):** Do NOT use `window.getSelection()` as a guard — double-clicking text auto-selects a word, which would prevent the modal from ever opening. Instead, use `window.getSelection().removeAllRanges()` to clear the selection before showing the modal.
   - The modal is dismissed by clicking the × button, clicking the overlay backdrop, or pressing Escape
   - Hidden automatically in print/PDF export and presenter mode
   - Does not trigger when in edit mode

10. **Presentation mode (presenter-friendly UI toggle):**
   - A keyboard shortcut (`P` key or `F5`) toggles `body.presenter-mode` class
   - When active, **interactive UI controls are hidden**: download buttons, edit toolbar, keyboard hints — while **dot navigation and progress bar remain visible** for orientation during presentation
   - Also hide the mouse cursor after 2 seconds of inactivity (`cursor: none`) for a clean projector look
   - Press the same key again (or `Escape`) to exit presenter mode
   - CSS:
     ```css
     body.presenter-mode .download-btn,
     body.presenter-mode .download-pptx-btn,
     body.presenter-mode .edit-toolbar,
     body.presenter-mode .kbd-hint {
       display: none !important;
     }
     body.presenter-mode { cursor: none; }
     body.presenter-mode:active { cursor: default; }
     ```
   - JS:
     ```javascript
     let cursorTimer;
     document.addEventListener('keydown', e => {
       if (e.key === 'p' || e.key === 'P' || e.key === 'F5') {
         if (document.activeElement.isContentEditable) return; // skip in edit mode
         e.preventDefault();
         document.body.classList.toggle('presenter-mode');
       }
       if (e.key === 'Escape' && document.body.classList.contains('presenter-mode')) {
         document.body.classList.remove('presenter-mode');
       }
     });
     document.addEventListener('mousemove', () => {
       document.body.style.cursor = 'default';
       clearTimeout(cursorTimer);
       if (document.body.classList.contains('presenter-mode')) {
         cursorTimer = setTimeout(() => { document.body.style.cursor = 'none'; }, 2000);
       }
     });
     ```
   - Show a brief toast notification when toggling: "Presenter Mode ON — press P or Esc to exit"

#### 3d. PDF & PPTX Download — Screenshot-Based Approach (Critical)

**Both PDF and PPTX downloads use the same html2canvas screenshot approach** to guarantee pixel-perfect visual fidelity with the web presentation. Do NOT use `window.print()` or per-slide-type PptxGenJS reconstruction — these approaches produce layout mismatches (broken two-column layouts, misaligned images, wrong proportions).

**Required CDN scripts** (load before the main `<script>` block):

```html
<script src="https://cdn.jsdelivr.net/gh/gitbrent/PptxGenJS@3.12.0/dist/pptxgen.bundle.js"></script>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js"></script>
```

**Shared capture logic:** Both functions follow this pattern for each slide:
1. Hide UI elements (nav dots, buttons, toolbar, slide counters, source-text)
2. Force slide to fixed dimensions: `width:1280px; height:720px; overflow:hidden`
3. Capture with `html2canvas` at `scale: 2` for high resolution (2560×1440px output)
4. Place the captured image as a full-page background in the output format
5. Restore original styles after capture

**PDF Download (jsPDF):**

```javascript
async function downloadPDF() {
  if (typeof html2canvas === 'undefined' || typeof window.jspdf === 'undefined') { showToast('Libraries not loaded'); return; }
  showToast('Generating PDF...', 15000);

  document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
  const hideEls = document.querySelectorAll('.nav, .progress-bar, .kbd-hint, .download-btn, .download-pptx-btn, .edit-toolbar, .toast, .slide-counter, .source-text');
  hideEls.forEach(el => { el.dataset.od = el.style.display; el.style.display = 'none'; });

  const { jsPDF } = window.jspdf;
  const pageW = 338, pageH = 190; // 16:9 in mm
  const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: [pageW, pageH] });
  const allSlides = document.querySelectorAll('.slide');

  for (let i = 0; i < allSlides.length; i++) {
    if (i > 0) pdf.addPage([pageW, pageH], 'landscape');
    const hs = allSlides[i];
    const orig = hs.getAttribute('style') || '';
    hs.style.cssText = 'width:1280px;height:720px;min-height:720px;max-height:720px;overflow:hidden;scroll-snap-align:none;';
    try {
      const canvas = await html2canvas(hs, {
        scale: 2, useCORS: true, allowTaint: true,
        width: 1280, height: 720, windowWidth: 1280, windowHeight: 720, logging: false
      });
      pdf.addImage(canvas.toDataURL('image/jpeg', 0.92), 'JPEG', 0, 0, pageW, pageH);
    } catch(e) { console.warn('Capture failed slide '+(i+1), e); }
    hs.setAttribute('style', orig);
  }

  hideEls.forEach(el => { el.style.display = el.dataset.od || ''; delete el.dataset.od; });
  pdf.save('presentation.pdf');
  showToast('PDF downloaded!');
}
```

**PPTX Download (html2canvas + PptxGenJS):**

```javascript
async function downloadPPTX() {
  if (typeof PptxGenJS === 'undefined' || typeof html2canvas === 'undefined') { showToast('Libraries not loaded'); return; }
  showToast('Generating PPTX...', 15000);

  document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
  const hideEls = document.querySelectorAll('.nav, .progress-bar, .kbd-hint, .download-btn, .download-pptx-btn, .edit-toolbar, .toast, .slide-counter');
  hideEls.forEach(el => { el.dataset.od = el.style.display; el.style.display = 'none'; });

  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'WIDE', width: 13.333, height: 7.5 });
  pptx.layout = 'WIDE';
  const allSlides = document.querySelectorAll('.slide');
  const total = allSlides.length;

  for (let i = 0; i < total; i++) {
    const hs = allSlides[i];
    const orig = hs.getAttribute('style') || '';
    hs.style.cssText = 'width:1280px;height:720px;min-height:720px;max-height:720px;overflow:hidden;scroll-snap-align:none;';
    try {
      const canvas = await html2canvas(hs, {
        scale: 2, useCORS: true, allowTaint: true,
        width: 1280, height: 720, windowWidth: 1280, windowHeight: 720, logging: false
      });
      const ps = pptx.addSlide();
      ps.addImage({ data: canvas.toDataURL('image/png'), x: 0, y: 0, w: 13.333, h: 7.5 });
      const isDark = hs.classList.contains('title-slide') || hs.classList.contains('ending-slide');
      ps.addText((i+1)+' / '+total, { x:11.8, y:7.0, w:1.2, h:0.35, fontSize:10, color: isDark?'70A0CC':'999999', align:'right', fontFace:'Helvetica' });
    } catch(e) { console.warn('Capture failed slide '+(i+1), e); }
    hs.setAttribute('style', orig);
  }

  hideEls.forEach(el => { el.style.display = el.dataset.od || ''; delete el.dataset.od; });
  await pptx.writeFile({ fileName: 'presentation.pptx' });
  showToast('PPTX downloaded!');
}
```

**Button placement:**
```html
<button class="download-btn" onclick="downloadPDF()" title="Download PDF">
  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M5 20h14v-2H5v2zm7-18v12.17l3.59-3.58L17 12l-5 5-5-5 1.41-1.41L12 14.17V2z"/></svg>
  PDF
</button>
<button class="download-btn download-pptx-btn" onclick="downloadPPTX()" title="Download PPTX">⬇ PPTX</button>
```

**Why screenshot-based:**
- `window.print()` + `@media print` CSS produces layout mismatches — two-column grids collapse, images change proportions, fonts resize differently
- PptxGenJS per-slide-type reconstruction can never perfectly match CSS flexbox/grid layouts with rounded cards, shadows, and gradients
- html2canvas captures the exact rendered pixels, guaranteeing 100% visual fidelity
- Trade-off: PPTX slides are image-based (not editable text) — if editable PPTX is needed, use the `/journal-reading` skill which generates a fully editable python-pptx presentation

**`@media print` CSS is still included** as a fallback for users who manually do Cmd+P, but it is NOT the primary PDF export method. Keep the print CSS from the template for graceful degradation.

#### 3e. Inline Editing Feature

The HTML **must** include a built-in inline editing mode so users can modify the presentation directly in the browser without touching HTML source code. Every generated presentation must contain:

1. **Edit toolbar** — fixed bottom-right with Edit/Save buttons and editing status indicator, styled consistently with the existing Download PDF button
2. **CSS for edit mode** — `body.edit-mode` class that shows dashed outlines on editable elements, solid outline + background on focus, and "Click to replace image" overlay on figure containers
3. **JS editing logic** (~120 lines):
   - `toggleEditMode()` — **must be `async`**. When exiting edit mode ("Stop Editing"), it **auto-saves** by calling `await savePresentation()` before disabling editing. This ensures edits persist when reopening the file — the user does not need to manually click Save before stopping.
   - `enableEditing()` / `disableEditing()` — sets/removes `contenteditable="true"` on: `h1, h2, h3, .card li, .card p, .key-point, .figure-caption, .section-header, .outline-num, .outline-text, .split-header, .subtitle, .journal-badge, .presenter-info, .title-authors, .title-journal, .title-date, .loe-badge, .ending-title, .ending-subtitle, .ending-info, .ending-ref, .highlight-box, .data-table td/th, .slide-counter`
   - **Image replacement** — click on `.figure-container` opens file picker, or drag-and-drop; uses `FileReader` to convert to base64 and replace `img.src`
   - `savePresentation()` — uses File System Access API (`showSaveFilePicker`) when available (Chrome/Edge on http://); falls back to Blob download for Safari or `file://` protocol. Clones the document, strips edit toolbar/contenteditable attributes, resets edit state in the clone.
   - **Keyboard passthrough** — when a `contenteditable` element is focused, arrow keys and Space must NOT trigger slide navigation
4. **Print/PDF** — `.edit-toolbar` hidden in `@media print`
5. **Hidden file input** — `<input type="file" id="imageUploadInput" accept="image/*" style="display:none;">` for image replacement

Refer to `templates/presentation_template.html` for the reference implementation.

### 4. Generate Portable Version

After the main HTML is complete, generate a **self-contained portable HTML** by embedding all images as Base64 data URIs. This produces a single file that works on any computer without needing the `presentation_images/` folder.

```python
import base64, os, re

html_path = os.path.join(output_dir, "presentation.html")
img_dir = os.path.join(output_dir, "presentation_images")

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

for filename in set(re.findall(r'src="presentation_images/([^"]+)"', html)):
    filepath = os.path.join(img_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as img_f:
            b64 = base64.b64encode(img_f.read()).decode('utf-8')
        mime = 'image/png' if filename.endswith('.png') else 'image/jpeg'
        html = html.replace(
            f'src="presentation_images/{filename}"',
            f'src="data:{mime};base64,{b64}"'
        )

portable_path = os.path.join(output_dir, "presentation_portable.html")
with open(portable_path, 'w', encoding='utf-8') as f:
    f.write(html)
```

### 5. Deliver

1. All output files are saved inside the dedicated output folder (created in Step 0b):
   ```
   {ShortTitle}_presentation/
   ├── presentation_images/          ← extracted figures (intermediate)
   ├── presentation.html             ← development version (external images)
   └── presentation_portable.html    ← portable single-file (~1 MB)
   ```
2. Open in browser: `open "{output_dir}/presentation_portable.html"`
3. Instruct the user:
   - **Browse:** scroll or use keyboard arrows/presentation clicker (Arrow keys, Space, PageUp/PageDown all supported)
   - **Edit:** click "Edit" (bottom-right) to enter edit mode — click any text to modify, click figures to replace images, drag-and-drop images. Click "Stop Editing" to **auto-save and exit** edit mode. Edits persist when reopening the file (Chrome/Edge on http://; on Safari or file:// protocol, a download is triggered).
   - **Source text:** double-click any card to view the original paper excerpt in a popup — useful for Q&A fact-checking
   - **Download PDF:** click the PDF button — outputs 16:9 slide-ratio pages via html2canvas screenshot
   - **Download PPTX:** click the PPTX button to generate and download a PowerPoint file directly from the browser (uses PptxGenJS)
   - **Presenter mode:** press `P` or `F5` to hide UI controls for clean projection; press again or `Esc` to exit
   - **Share:** copy the single `presentation_portable.html` file to USB drive or upload to Google Drive — works on any computer with a browser

## Content Guidelines

- **Default language: English** — all slide content must be written in English using standard medical terminology
- If the user explicitly requests Chinese or bilingual content, switch accordingly
- Keep bullet points concise (1 line each, max 5 per card)
- Always show **p-values** and **effect sizes** for results
- Use `.sig` (red) styling for statistically significant values
- Include original paper figures — do NOT recreate charts
- Provide mechanism-based explanations for why results differ
- End with actionable clinical pearl (what to do tomorrow in the OR)
- UI elements (buttons, hints) should also be in English: "Download PDF", "Use Arrow Keys or Space to navigate slides"

### Citation and Attribution in Discussion Slides

When the Discussion section references other studies or makes interpretive claims, **always properly attribute** the source:

- **Cited studies:** Use format `**Author et al. (Year):** key finding (sample size, route, outcome)` — e.g., `**Ghavimi et al. (2017):** IV TA in rhinoplasty (n=60) — reduced edema & ecchymosis at 24 hrs. *BUT systemic route*`
- **The current paper's own interpretations:** Present as the authors' analysis — e.g., "The authors suggest that..." or frame it clearly as this study's discussion point
- **Do NOT** present cited literature findings without attribution — always make it clear whose finding it is
- **Distinguish clearly** between: (1) the current study's own results, (2) findings from cited studies, and (3) the authors' interpretive claims
- Bad example: `IV TA reduces edema and ecchymosis at 24 hours` (who found this? this study or a cited one?)
- Good example: `**Ghavimi et al. (2017):** IV TA (n=60) reduced edema & ecchymosis at postop hr 24; 10 mg/kg dose → BUT systemic route`

## When to Use

This skill applies when a user:
- Provides a medical paper in **PDF, PPTX, or Markdown** format, or a **folder** containing the main paper plus supplements
- Requests a "presentation website" / "網站報告" / "HTML 簡報"
- Mentions "晨會" (morning meeting) or journal reading/club
- Wants embedded figures from the original source (including supplementary materials)
- Needs downloadable PDF output from the presentation
