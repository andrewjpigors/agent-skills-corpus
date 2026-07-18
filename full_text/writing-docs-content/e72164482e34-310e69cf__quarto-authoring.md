---
name: quarto-authoring
description: Comprehensive Quarto + Typst skill covering authoring (QMD syntax, cross-refs, callouts, figures, tables, citations, code cells, divs/spans), websites and blogs (navigation, themes/SCSS, dark mode, listings, categories, RSS, about pages, comments), books in PDF and EPUB (chapters, parts, appendices, multi-format output, cover images, e-reader metadata), PDF output via Typst (page layout, fonts, typst-show.typ templates, pandoc escaping, orange-book, CV/resume/paper templates, brand.yml) and WeasyPrint (standalone HTML+CSS), MS Word/docx (reference-doc templates), presentations (revealjs, pptx, beamer, Typst slides), dashboards (rows/columns/pages, value boxes, cards, tabsets, sidebars), interactive documents (Observable JS, Shiny, Jupyter widgets/htmlwidgets), manuscripts (notebook-first scholarly articles, journal formats, MECA bundles), project configuration (profiles, pre/post-render scripts, virtual environments, Binder), publishing/deployment (quarto publish, GitHub Pages, Netlify, GitHub Actions, freeze CI pattern), and migration from R Markdown/bookdown/blogdown/Jupyter. Use for any question about Quarto, Typst documents or templates, .qmd files, building a blog or personal website, writing a book or ebook, making a CV or resume PDF, building a Quarto dashboard, adding interactivity (OJS/Shiny/widgets) to a document, writing a reproducible-research manuscript, configuring Quarto project profiles/scripts, or rendering/publishing any of these.
metadata:
  author: SisengAI (merged from quarto-authoring, quarto-book-structure, colorful-pdf, quarto-typst-pdf)
  thanks: Posit and the Quarto core team for building and documenting Quarto itself — see also their independently-authored quarto-authoring skill at posit-dev/skills
  version: "3.4"
license: MIT
---
# Quarto Authoring

Comprehensive reference for Quarto — documents, books, PDFs, and presentations.

---

## 1. QMD Essentials

### Basic Document Structure

```yaml
---
title: "Document Title"
author: "Author Name"
date: today
format: html
---
```

### Divs and Spans

Divs use fenced colons, spans use brackets:
```markdown
::: {.class-name}
Content inside the div.
:::

[important text]{.highlight}
```

Details: [references/divs-and-spans.md](references/divs-and-spans.md)

### Code Cells

Options use the language's comment symbol + `|`. Use **dashes, not dots**:
- R, Python, Julia: `#|`
- Mermaid: `%%|`
- Graphviz/DOT: `//|`

````markdown
```{language}
#| label: fig-example
#| echo: false
#| fig-cap: "A scatter plot."
```
````

Set document-level defaults:
```yaml
execute:
  echo: false
  warning: false
```

**Caching:** `#| cache: true` only works for R (knitr). For Python/Jupyter, use `execute: cache: true` in top-level YAML + `pip install jupyter-cache`.

Details: [references/code-cells.md](references/code-cells.md)

### Cross-References

Labels must start with a type prefix. Reference with `@`:
- Figure: `fig-` → `@fig-plot`
- Table: `tbl-` → `@tbl-data`
- Section: `sec-` → `@sec-intro`
- Equation: `eq-` → `@eq-model`

```markdown
# Introduction {#sec-intro}
See @sec-intro for background.
See @fig-plot for the results.
```

Details: [references/cross-references.md](references/cross-references.md)

### Callout Blocks

Five types: `note`, `warning`, `important`, `tip`, `caution`:
```markdown
::: {.callout-note}
This is a note.
:::

::: {.callout-warning}
## Custom Title
Warning with custom title.
:::
```

Details: [references/callouts.md](references/callouts.md)

### Figures

```markdown
![Caption text](image.png){#fig-name fig-alt="Alt text"}
```

Subfigures:
```markdown
::: {#fig-group layout-ncol=2}
![Sub 1](img1.png){#fig-sub1}
![Sub 2](img2.png){#fig-sub2}
Main caption.
:::
```

Details: [references/figures.md](references/figures.md)

### Tables

```markdown
::: {#tbl-example}
| Col 1 | Col 2 |
|-------|-------|
| Data  | Data  |
Table caption.
:::
```

Details: [references/tables.md](references/tables.md)

### Citations

```markdown
According to @smith2020...
Multiple citations [@smith2020; @jones2021].
```

```yaml
bibliography: references.bib
csl: apa.csl
```

Details: [references/citations.md](references/citations.md)

### Conditional Content & Shortcodes

Details: [references/conditional-content.md](references/conditional-content.md), [references/shortcodes.md](references/shortcodes.md)

### Diagrams (Mermaid, Graphviz)

Details: [references/diagrams.md](references/diagrams.md)

### Compute Engines

Details: [references/engines.md](references/engines.md)

### Page Layout

Details: [references/layout.md](references/layout.md)

### Extensions

Details: [references/extensions.md](references/extensions.md)

### YAML Front Matter

Details: [references/yaml-front-matter.md](references/yaml-front-matter.md)

### Markdown Linting

Details: [references/markdown-linting.md](references/markdown-linting.md)

---

## 2. Websites & Blogs

### Website Project

```bash
quarto create project website mysite && cd mysite && quarto preview
```

```yaml
# _quarto.yml
project:
  type: website

website:
  title: "My Site"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: about.qmd
        text: About

format:
  html:
    theme: cosmo          # or {light: flatly, dark: darkly} for a dark-mode toggle
```

Navigation (navbar/sidebar/hybrid), 25+ themes + custom SCSS, dark mode, search, drafts, redirects, social cards, announcement bars, multi-format pages: [references/websites.md](references/websites.md)

### Blog Project

```bash
quarto create project blog myblog
```

A blog = website + listing homepage + `posts/` directory (one folder per post) + categories + RSS:

```yaml
# index.qmd front matter
listing:
  contents: posts
  sort: "date desc"
  categories: true
  feed: true              # RSS at index.xml (needs site-url in _quarto.yml)
```

Key pattern — `posts/_metadata.yml` with `freeze: true` so old posts never re-execute.

Post front matter, listing types, about-page templates (jolla/trestles/solana/marquee/broadside), comments (giscus/utterances), drafts, RSS options: [references/blogging.md](references/blogging.md)

### Publishing (websites, blogs, books)

```bash
quarto publish gh-pages       # also: quarto-pub, netlify, connect, confluence, huggingface
```

CI pattern: `execute: freeze: auto` → render locally → commit `_freeze/` → GitHub Actions renders without R/Python. Full workflows: [references/publishing.md](references/publishing.md)

---

## 3. Books

### Basic Book Structure

```yaml
# _quarto.yml
project:
  type: book

book:
  title: "mybook"
  author: "Jane Doe"
  chapters:
    - index.qmd       # Required — homepage in HTML output
    - intro.qmd
    - summary.qmd
    - references.qmd  # Auto-generated bibliography
```

**Key rules:**
- `index.qmd` is required
- `references.qmd` holds the generated bibliography
- Top-level rendering options go at root of `_quarto.yml`
- Format-specific options under `format:`

### Titles and Chapter Numbers

```markdown
# Preface {.unnumbered}
```

Numbering depth (format option):
```yaml
number-depth: 1
```

`toc-depth` is independent of `number-depth`.

### References / Bibliography

Place a `#refs` div where the bibliography should appear:
```markdown
# References {.unnumbered}
::: {#refs}
:::
```

### Parts & Appendices

**Parts with content files:**
```yaml
book:
  chapters:
    - index.qmd
    - part: dice.qmd       # part intro file
      chapters:
        - basics.qmd
        - packages.qmd
    - part: "Dice"          # title-only (no intro file)
      chapters:
        - objects.qmd
```

**Appendices:**
```yaml
book:
  chapters:
    - index.qmd
  appendices:
    - tools.qmd
    - resources.qmd
```

Appendices are uppercase alpha. Customize:
```yaml
crossref:
  appendix-title: "App."
  appendix-delim: ":"
```

### Cross-References (Books)

Cross-references work across chapters:
```markdown
See @fig-penguins for details.
See @sec-introduction for background.
```

Label must start with `sec-` for chapter/section refs. Suppress prefix: `[-@sec-intro]`. Custom prefix: `[Chapter @sec-vis]`.

Chapter-level figure numbering is automatic.

### Hyperlinks Within a Book

Use source `.qmd` filename as link target:
```markdown
[about](about.qmd)
[section](about.qmd#section)
```

For print output, use cross-references instead of hyperlinks.

### Managing Execution

**Incremental render:** `quarto render intro.qmd` or `quarto render subdir/`

**Freeze** (prevent re-execution on global renders):
```yaml
execute:
  freeze: true    # never re-render
  freeze: auto    # re-render only when source changes
```

Freeze results stored in `_freeze/` — check into version control.

**Cache:**
```yaml
execute:
  cache: true
```
Refresh: `quarto render --cache-refresh`

**Notebooks (.ipynb):** cells not executed by default. To execute: `quarto render notebook.ipynb --execute` or `execute: enabled: true`.

**Working directory:**
```yaml
project:
  execute-dir: project   # use project root
```

### Page Navigation & Footer

```yaml
book:
  page-navigation: true
  page-footer: "Copyright 2021"
```

Targeted footer:
```yaml
book:
  page-footer:
    left: "Copyright 2021"
    right:
      - icon: github
        href: https://github.com/
```

### Typst Books (orange-book)

Quarto 1.9.17+ bundles `orange-book` as the default for book projects:
```yaml
project:
  type: book
book:
  title: "My Book"
  chapters: [index.qmd, intro.qmd, summary.qmd]
format: typst
```

Features: chapter numbering, decorative headers, parts/appendices, styled TOC, `_brand.yml` integration.

**Bibliography gotcha:** in Typst books with citations + a `references.qmd` chapter, Typst's native bibliography leaves the References chapter empty and appends its own duplicate "Bibliography" chapter. Fix with:
```yaml
format:
  typst:
    citeproc: true
```

Explicit format:
```bash
quarto add quarto-ext/orange-book
```
```yaml
format: orange-book-typst
```

### Typst Books (bookly)

Third-party extension with 6 visual themes, LOF/LOT, and Tufte layout:
```bash
quarto add maucejo/quarto-bookly
```
```yaml
project:
  type: book
book:
  title: "My Book"
  chapters: [index.qmd, chapters/intro.qmd]
  appendices: [appendices/appendixA.qmd]
format:
  bookly-typst:
    theme: modern           # classic, modern, fancy, obook, orly, pretty
    toc: true
    lof: true               # list of figures
    lot: true               # list of tables
    tufte: false            # Tufte-style margin notes
    part-numbering: "1"     # "A", "I", etc.
    colors:
      primary: rgb("#2563EB")
    fonts:
      body: "Lato"
```
Maps callouts to bookly info boxes. Requires Quarto >= 1.9.17.

### Multi-Chapter Typst ({{< include >}})

Without a book project, use a master `.qmd`:
```markdown
---
title: "My Document"
format:
  typst:
    template-partials:
      - typst-show.typ
---

# Chapter One
{{< include 01-chapter.qmd >}}

# Chapter Two
{{< include 02-chapter.qmd >}}
```

Real-world example: [christopherkenny/harvard-diss](https://github.com/christopherkenny/harvard-diss) — open-source Harvard dissertation using Typst + Quarto.

### Navbar Options

```yaml
book:
  navbar:
    title: "Title"
    logo: logo.png
    background: "#fff"
    pinned: true
    search: true
    left: [{text: "Home", href: index.qmd}]
    right: [{icon: github, href: "https://github.com/"}]
```

### Sidebar Options

```yaml
book:
  sidebar:
    style: docked         # or floating
    background: light
    search: true
    collapse-level: 2
    logo: false           # disable brand logo
```

### Search

```yaml
book:
  search:
    location: navbar      # or sidebar
    type: overlay         # or textbox
```

Algolia:
```yaml
search:
  algolia:
    index-name: <index>
    application-id: <id>
    search-only-api-key: <key>
```

### Social Metadata

**Twitter card:**
```yaml
book:
  twitter-card:
    site: "@handle"
    title: "..."
    description: "..."
    image: path/to/image.png
    card-style: summary_large_image
```

**Open Graph:**
```yaml
book:
  open-graph:
    title: "OG Title"
    description: "..."
    image: path/to/image.png
    locale: en_US
```

### Comments

Hypothesis, Utterances, or Giscus:
```yaml
book:
  comments:
    hypothesis: true
    # or:
    giscus:
      repo: owner/repo
      mapping: pathname
```

### Listings

Auto-generate content:
```yaml
---
title: "Listing"
listing:
  contents: posts
  type: grid
  grid-columns: 2
---
```

Types: `default`, `table`, `grid`, `custom`. Options: `sort`, `max-items`, `page-size`, `categories`, `feed` (RSS).

### Book Options Reference

| Option | Description |
|--------|-------------|
| `title`, `subtitle`, `author`, `date` | Book metadata |
| `cover-image` | Cover image (HTML + ePub) |
| `sharing` | `twitter`, `facebook`, `linkedin` |
| `downloads` | `pdf`, `epub`, `docx` |
| `doi` | Digital Object Identifier |
| `favicon`, `site-url` | Site identity |
| `repo-url`, `repo-actions` | Source repository links (`edit`, `source`, `issue`) |
| `output-file` | Output filename (no extension) |

### EPUB & Multi-Format Books

One book source → website + PDF + ebook, with download buttons:

```yaml
book:
  cover-image: cover.png
  downloads: [pdf, epub]

format:
  html:
    theme: cosmo
  typst: default
  epub:
    identifier: "urn:isbn:9780123456789"   # stable ID for store submission
```

```bash
quarto render                # all formats → _book/
quarto render --to epub      # just the .epub
```

EPUB metadata, cover sizing, CSS constraints, font embedding, chapter splitting, epubcheck validation, Kindle/KDP notes: [references/epub.md](references/epub.md)

---

## 4. PDF Output — WeasyPrint (HTML+CSS)

For visually rich, colorful PDFs. Zero LaTeX.

### Prerequisites

```bash
uv tool install weasyprint
```

### Critical: Quarto's Bootstrap overrides dark themes

Quarto HTML always sets `body { background-color: #fff }` even with `theme: none` or `minimal: true`. For dark/styled PDFs use a **standalone HTML file** with embedded CSS — bypass Quarto's HTML output entirely.

### Workflow

```bash
weasyprint standalone.html output.pdf
```

### CSS tips

- `@page { size: A4; margin: 2cm; }` for page control
- `@page { @bottom-center { content: counter(page); } }` for page numbers
- Gradients, `border-radius`, `box-shadow`, `background-image` all work
- `page-break-after/before: always` for page control
- `min-height: 297mm` (A4 height) for full-page sections
- `-webkit-print-color-adjust: exact; print-color-adjust: exact;` for reliable color

### Quarto + WeasyPrint hack (keeps .qmd)

```bash
quarto render doc.qmd --to html
sed -i 's/background-color:#fff/background-color:#050D1A/g' doc.html
weasyprint doc.html output.pdf
```

---

## 5. PDF Output — Typst

Zero LaTeX. Blazing fast. Quarto >=1.5 includes the Typst CLI.

### Quick start

```yaml
---
title: "My Document"
format: typst
---
```

```bash
quarto render doc.qmd --to typst
```

### Page layout

```yaml
format:
  typst:
    papersize: a4
    margin:
      x: 2.5cm
      y: 2cm
    columns: 1
    page-numbering: false
```

Article layout (Tufte-style): `grid: { margin-width: 2in, body-width: 4in, gutter-width: 0.25in }`

### Table of contents

```yaml
format:
  typst:
    toc: true
    toc-depth: 3
    toc-title: "Contents"
    toc-indent: 1.5em
```

Exclude: `### Heading {.unnumbered .unlisted}`

### Section numbering

```yaml
number-sections: true       # OFF by default
number-depth: 3
section-numbering: 1.A.a
```

Exclude: `### Heading {.unnumbered}`

### Fonts

```yaml
format:
  typst:
    mainfont: "Inter"
    fontsize: "11pt"
    font-paths: ["fonts/"]
```

### Syntax highlighting

```yaml
format:
  typst:
    syntax-highlighting: arrow   # default
    # 20+ themes: pygments, tango, monokai, nord, github, dracula...
    # Special: none, idiomatic (Typst native)
```

### Typst CSS — inline styles

Quarto 1.5+ translates CSS → Typst:
```markdown
[amber text]{style="color: #D4720A"}
[blue bg]{style="background-color: #2563EB; color: white; padding: 4pt"}
```

### Typst blocks

```markdown
::: {.block fill="luma(230)" inset="8pt" radius="4pt"}
Gray rounded box.
:::
```

Any `#block()` arg: `fill`, `stroke`, `inset`, `radius`, `width`, `height`.

### Theorems

```yaml
format:
  typst:
    theorem-appearance: fancy   # colored boxes, brand colors
    # Options: simple, fancy, clouds, rainbow
```

### Raw Typst

````markdown
```{=typst}
#set par(justify: true)
#block(fill: rgb("#050D1A"), inset: 10pt)[Dark block]
```
````

### PDF accessibility

```yaml
format:
  typst:
    pdf-standard: ua-1
    pdf-standard: [a-2b, ua-1]
```

Validate: `quarto install verapdf`

### Includes & keep-typ

```yaml
format:
  typst:
    keep-typ: true
    include-before-body:
      text: |
        #show heading: set text(fill: rgb("#E8B949"))
```

---

## 6. Custom Typst Templates

### Quick: template-partials (one file)

Create `typst-show.typ` alongside `.qmd`:

```typst
#let navy = rgb("#050D1A")
#let gold = rgb("#E8B949")

#show: doc => {
  set page(fill: navy, margin: (top: 2cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    footer: [Your footer],
  )
  set text(font: "Inter", size: 10pt, fill: rgb("#9DB0CF"))

  show heading.where(level: 1): it => {
    pagebreak()
    v(0.8cm)
    set text(size: 28pt, weight: "black", fill: gold)
    it
  }
  show strong: it => text(weight: "semibold", fill: rgb("#EDF2FA"), it)
  show table: it => {
    show table.cell.where(y: 0): cell => {
      set text(fill: gold, weight: "semibold")
      cell
    }
    it
  }
  doc
}
```

```yaml
format:
  typst:
    template-partials:
      - typst-show.typ
```

### Pandoc escaping gotchas

**`$` signs:** Pandoc strips `\$` in `typst-show.typ`. Use `#let d = sym.dollar` then `["He turned #d 5,000"]`.

**Variable escaping:** Use `[$variable$]` (content blocks) instead of `"$variable$"` (strings).

**Injected page number:** Quarto's built-in Typst template emits `#set page(numbering: "1")` even for custom templates. For one-pagers (CVs, letters), suppress it: `page-numbering: false` in YAML, or `set page(numbering: none)` inside your template's show rule.

**Dashes in strings:** Typst only shapes `--` → en dash and `---` → em dash in *markup*, not inside string literals (`"2019--2023"` renders literally). Use real dash characters (– —) or content blocks (`[2019--2023]`).

**`to-string()` helper:**
```typst
#let to-string(content) = {
  if content.has("text") { content.text }
  else if content.has("children") { content.children.map(to-string).join("") }
  else if content.has("body") { to-string(content.body) }
  else if content == [ ] { " " }
}
```

### Full: custom format extension

```bash
quarto create extension format   # pick typst, name it
```

Generates: `_extension.yml`, `typst-template.typ`, `typst-show.typ`, `template.qmd`.

### Template patterns & tips

**Parameterized reports:** Pass Quarto `params` to Typst via the show file:
```yaml
# QMD frontmatter:
params:
  species: "Penguin"
```
```typst
// typst-show.typ:
#show: article.with(
  species: "$params.species$",
)
```
```typst
// typst-template.typ uses `species` as a variable throughout.
```
Useful for batch-rendering per-state/product/category reports.

**Colored sidebar:** Add a persistent colored strip to every page via `set page(background: place(top, rect(width: 2cm, height: 100%, fill: ...)))`.

**Heading level shift:** Quarto shifts Typst headings up one level on render. A QMD `# Heading` becomes Typst level 2. Design show rules accordingly (target `where(level: 2)` for QMD-level-1 headings).

**Custom functions** (callable from both template and `{=typst}` chunks):
```typst
#let blueline() = { line(length: 100%, stroke: 2pt + rgb("#68ACE5")) }
#let source_text(src) = { align(right, text(src, font: "Bitter", size: 9pt, style: "italic")) }
#let status-box(top-box-text: "", bottom-box-text: "") = {
  let top_box = box(width: 2in, height: 0.7in, fill: rgb("#002D72"), inset: 6pt,
    align(center + horizon)[#text(fill: white, weight: "bold", size: 9pt)[#top-box-text]])
  let bottom_box = box(width: 2in, height: 0.7in, fill: white, inset: 6pt,
    align(center + horizon)[#text(fill: black, size: 14pt)[#bottom-box-text]])
  stack(top_box, bottom_box, spacing: 0pt)
}
```
`status-box()` is the go-to for a KPI-style callout (e.g. "Q3 Revenue: $1.2M") in an executive-summary report.

**Per-level heading show rule** (different size/case/alignment per level, in one function):
```typst
show heading: it => {
  let sizes = ("1": 16pt, "2": 10pt)
  let level = str(it.level)
  let size = sizes.at(level)
  let formatted_heading = if level == "1" { upper(it) } else { it }
  let alignment = if level == "2" { center } else { left }

  set text(font: "Bitter", fill: rgb("#002D72"), size: size, weight: "bold")
  align(alignment)[#formatted_heading]
}
```
Remember the heading-level-shift rule above when picking which level to key off of.

**Footer built with `grid()`** (two-column: title left, date right, on a colored bar):
```typst
footer: {
  rect(width: 100%, height: 0.75in, outset: (x: 15%), fill: rgb("#68ACE5"),
    pad(top: 16pt, block([
      #grid(columns: (75%, 25%),
        align(left)[#text(upper(title), font: "Bitter", fill: white, weight: "bold")],
        align(right)[#text(upper(date), font: "Bitter", fill: white, weight: "bold")],
      )
    ])),
  )
}
```

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Title/date disappear | Custom template overrides defaults | Pass them through explicitly in `typst-show.typ` |
| Footer date shows raw ISO (`2025-09-01`) | Missing date format | Add `date-format: "MMMM YYYY"` |
| Heading styles apply to the wrong level | Quarto's heading level shift | Style Typst level 1 for Quarto `##` (see above) |
| Function prints as literal text | Missing `#` | Add `#` inside `[ ]` content brackets |
| Template not applied at all | Partials not declared | Add `template-partials` to YAML `format.typst` |

### Scaffolding a Branded Report Project

For repeatable "PDF report from a brief" work — as opposed to one-off documents — `scripts/` has a small uv-run scaffolder:

```bash
uv run python scripts/scaffold.py my-report --title "My Report" --date "July 2026"
uv run python scripts/validate.py my-report
quarto render my-report/report.qmd
```

`scaffold.py` writes `report.qmd`, `typst-show.typ`, `typst-template.typ`, `_brand.yml`, `pyproject.toml`, and an `images/` folder, with `blueline()`/`source_text()`/`status-box()` already wired into the template. `validate.py` checks the YAML actually declares `template-partials` (and catches a stray `format: pdf`) before you waste a render on a template that silently won't apply. `snippets.py [name]` prints any one helper on its own — run with no argument to list what's available.

**Date formatting:**
```yaml
date: September 2025
date-format: "MMMM YYYY"   # "September 2025" instead of "2025-09-01"
```

**Columns via layout-ncol** (works in Typst output):
```markdown
:::{layout-ncol=2}
![Image 1](img1.svg)
![Image 2](img2.svg)
:::
```
Quarto has no native Typst multi-column construct — `layout-ncol` is a Quarto-level shortcut good for side-by-side images only. For anything more custom (mixed content, uneven widths, a footer split into columns), drop into a `{=typst}` chunk or template and use Typst's own `grid()` directly, e.g. `grid(columns: (75%, 25%), [left], [right])`.

**HTML divs for backgrounds** (Quarto translates CSS → Typst):
```html
<div style="background-color: #F8F8F8;">
Content with gray background.
</div>
```

**`#` hash rule:** Inside brackets `[...]`, use `#` before function calls. In `{=typst}` chunks, also use `#`. Example: `#blueline()`, `#text(fill: white)[Title]`.

**Tools:** [Typst LSP](https://open-vsx.org/extension/nvarner/typst-lsp) (tooltips/autocomplete), [Tinymist](https://open-vsx.org/extension/myriad-dreamin/tinymist) (formatter), [vscode-pdf](https://open-vsx.org/extension/tomoki1207/pdf) (inline PDF preview), all for Positron/VS Code.

### Premade Typst templates

| Typst template | Quarto wrapper | Use |
|---|---|---|
| `charged-ieee` | `quarto-ext/typst-templates/ieee` | IEEE papers |
| `unequivocal-ams` | `quarto-ext/typst-templates/ams` | AMS math papers |
| `Typst-Paper-Template` | *no wrapper* | General working paper |
| `LaPreprint` | *no wrapper* | Beautiful preprints |
| `appreciated-letter` | `quarto-ext/typst-templates/letter` | Formal letters |
| `dashing-dept-news` | `quarto-ext/typst-templates/dept-news` | Newsletters |
| `wonderous-book` | `quarto-ext/typst-templates/fiction` | Fiction books |
| `typst-poster` | `quarto-ext/typst-templates/poster` | Academic posters |
| `orange-book` | Bundled (book projects) | Technical books |
| `cereal-words` | *no wrapper* | Resume/CV |
| `bare-bones-cv` | *no wrapper* | Minimal single-page CV |
| `imprecv` | *no wrapper* | YAML-driven CV (version control) |
| `billryan-typst` | *no wrapper* | Simple minimalist resume |
| `modern-typst-resume` | *no wrapper* | Modern resume + cover letter |
| `typst-blue-header-cv` | *no wrapper* | Two-column with blue header |
| `typst-cv-miku` | *no wrapper* | Academic CV (EN/ZH) |
| `typst-cv-template1` | *no wrapper* | Graduate CV style |
| `icicle`, `badformer` | *no wrapper* | Presentation slides |
| `typst-invoice` | *no wrapper* | Invoice generator (TOML→PDF) |
| `typst-palettes` | *no wrapper* | Color palette library |
| `typst-timetable` | *no wrapper* | Class/timetable schedules |
| `showybox` | *no wrapper* | Colorful customizable boxes |

Install: `quarto use template quarto-ext/typst-templates/<name>`. Full list: [github.com/typst/templates](https://github.com/typst/templates).

Usage examples — IEEE:
```yaml
---
title: "Paper Title"
authors:
  - name: Author Name
    email: "email@example.com"
    affiliations:
      - name: University
        city: City
        country: Country
abstract: |
  Abstract content...
format:
  ieee-typst: default
bibliography: refs.bib
---
```

AMS:
```yaml
---
title: "Mathematical Theorems"
authors:
  - name: Author
    affiliations:
      - name: University
        department: Mathematics
format: ams-typst: default
bibliography: refs.bib
---
```

Letter:
```yaml
---
subject: "Subject"
name: "Sender Name"
sender: "Sender Address"
recipient: |
  Recipient Name \\
  Address
sent: "City, Date"
format: letter-typst: default
---
```

Fiction:
```yaml
---
title: "Book Title"
author: Author Name
dedication: "for Someone"
publishing-info: "Publisher Info"
format: fiction-typst: default
---
```

Poster:
```yaml
---
title: "Academic Poster"
format:
  poster-typst:
    size: "36x24"
    poster-authors: "A. Smith, B. Jones"
    departments: "Department Name"
    institution-logo: "./images/logo.png"
    footer-text: "Conference 2026"
    keywords: ["Typst", "Quarto"]
---
```

### Bundling Typst packages

```bash
quarto call typst-gather          # auto-detect from _extension.yml
quarto call typst-gather --init-config
```

Downloads `@preview` packages into `typst/packages/` for offline use.

---

## 7. _brand.yml Integration

```yaml
color:
  primary: "#D4720A"
  secondary: "#321208"
logo:
  images:
    site-logo:
      path: logo.svg
  medium: site-logo
```

Typst templates read via `brand-color.primary`, `brand-color.secondary`. `fancy` theorem appearance and `orange-book` respect brand colors automatically.

---

## 8. Presentations

Formats: `revealjs` (HTML), `pptx` (PowerPoint), `beamer` (LaTeX/PDF), plus standalone Typst decks (touying/polylux).

```yaml
---
title: "Habits"
author: "John Doe"
format: revealjs
---
```

```markdown
## Getting up
- Turn off alarm
- Get out of bed

## Going to sleep
- Get in bed
- Count sheep
```

Level-1 headings create section title slides. Horizontal rules (`---`) create slides without titles.

Incremental lists, columns, code line stepping, speaker notes, slide backgrounds, fragments/auto-animate, custom SCSS themes, PDF export, pptx reference-doc templates, beamer, Typst slides: [references/presentations.md](references/presentations.md)

---

## 9. Dashboards

```yaml
---
title: "Sales Dashboard"
format: dashboard
---
```

Level-2 headings become rows (or columns with `orientation: columns`); size with `{height=}`/`{width=}`. Each code cell is a **card**:

```markdown
## Row {height=60%}

```{python}
#| title: Revenue by Region
# chart code
```

## Row {height=40%}
```

Level-1 headings create **pages** in a multi-page dashboard. `{.tabset}` on a row/column turns its cards into a tabset. `{.sidebar}`/`{.toolbar}` on a column/row holds input controls.

**Value box** for a KPI metric:
```markdown
```{python}
#| content: valuebox
#| title: "Total Revenue"
dict(value = "$1.2M", icon = "currency-dollar", color = "success")
```
```

Dashboards are HTML under the hood — same `theme:`/SCSS/`_brand.yml` mechanism as websites applies. Interactivity is either static (OJS/widgets, deployable anywhere) or Shiny-backed (`server: shiny` in YAML, needs a Shiny server/Posit Connect — won't run on GitHub Pages/Netlify).

Multi-page nav, parameterized dashboard variants, expandable cards, responsive behavior: [references/dashboards.md](references/dashboards.md)

---

## 10. Interactivity

Three approaches, increasing infrastructure required:

**Widgets** (Jupyter Widgets / htmlwidgets) — render to self-contained HTML+JS at build time, zero server, works in a static site or dashboard card as-is.

**Observable JS (OJS)** — reactive, client-side, no server:
```{ojs}
viewof minimum = Inputs.range([-2, 2], {value: 1, step: 0.01, label: "minimum"})
```
Any cell referencing `minimum` re-runs automatically when the input moves. Deploys as pure static HTML.

**Shiny** — reactive, server-backed (R or Python):
```r
selectInput("type", "Trend index", choices = unique(trend_data$type))
output$lineplot <- renderPlot({ plot(x = selected_trends()$date, y = selected_trends()$close) })
```
Requires the knitr engine plus a running Shiny process (`server: shiny` in YAML) — needs a Shiny server/Posit Connect in production, not compatible with static-only hosting.

**Choosing:** static HTML deployment → OJS or a widget; computation must genuinely re-run server-side (model refit, DB query) → Shiny; just embedding an existing interactive plot → Jupyter Widgets/htmlwidgets.

OJS data sources (`FileAttachment`, `ojs_define()`), cross-file OJS imports, Shiny reactive expressions and execution contexts, input panel layout: [references/interactivity.md](references/interactivity.md)

---

## 11. MS Word (docx)

```yaml
---
title: "Report"
format: docx
---
```

**Match a corporate template** without touching XML — create a `.docx` in Word with the styles (Heading 1, Body Text, table style, ...) set the way you want, then point Quarto at it:

```yaml
format:
  docx:
    reference-doc: custom-reference-doc.docx
```

Generate a starter reference doc to edit rather than starting from a blank Word file:

```bash
quarto pandoc -o custom-reference-doc.docx --print-default-data-file reference.docx
```

Track changes and comments round-trip normally through Word after rendering — useful when final sign-off happens in Word rather than in a PDF or the terminal.

---

## 12. WeasyPrint vs Typst

|                | WeasyPrint              | Typst                  |
| -------------- | ----------------------- | ---------------------- |
| Color power    | Full CSS                | Good (fills, borders)  |
| Page layout    | CSS @page               | `papersize`, `margin`  |
| Page numbers   | CSS counters             | `page-numbering`       |
| TOC            | Manual CSS              | `toc: true`            |
| Cross-refs     | Manual                  | Native `@sec-/@fig-`   |
| Templates      | HTML+CSS                | `typst-show.typ`       |
| Bootstrap issue| Must use standalone HTML| None                   |
| Accessibility  | Manual                  | `pdf-standard: ua-1`   |

**Rule:** Typst for structure (TOC, cross-refs). WeasyPrint for visual design (gradients, dark themes).

---

## 13. LaTeX Parity — Typst Workarounds

| Feature       | Typst equivalent                                 |
| ------------- | ------------------------------------------------ |
| `linestretch` | `set par(leading: linestretch * 0.65em)`         |
| `mathfont`    | `#show math.equation: set text(font: mathfont)`  |
| `codefont`    | `#show raw: set text(font: codefont)`            |
| `linkcolor`   | `#show link: set text(fill: rgb(linkcolor))`     |
| `citecolor`   | `#show ref: set text(fill: rgb(citecolor))`      |
| `thanks`      | `footnote(thanks, numbering: "*")` on title      |

---

## 14. Migration

Only when converting existing projects. Do NOT read for new Quarto documents:
- R Markdown → [references/conversion-rmarkdown.md](references/conversion-rmarkdown.md)
- bookdown → [references/conversion-bookdown.md](references/conversion-bookdown.md)
- xaringan → [references/conversion-xaringan.md](references/conversion-xaringan.md)
- distill → [references/conversion-distill.md](references/conversion-distill.md)
- blogdown → [references/conversion-blogdown.md](references/conversion-blogdown.md)
- Jupyter → [references/conversion-jupyter.md](references/conversion-jupyter.md)

---

## 15. Manuscripts

Notebook-first scholarly articles: write in Jupyter/VS Code/RStudio, get the article (PDF/Word/journal format) *and* a manuscript website exposing the source notebooks alongside it.

```bash
quarto create project manuscript mymanuscript
```

```yaml
# _quarto.yml
project:
  type: manuscript

manuscript:
  article: index.qmd
  notebooks:
    - notebook-data-cleaning.ipynb
    - notebook-figures.qmd
```

Journal-required formats sit alongside HTML:
```yaml
format:
  html: default
  docx: default    # journal submission
  jats: default     # publisher-ingestion XML
```

Community journal templates install like any extension: `quarto add quarto-journals/agu`. Publishes as a manuscript website (`quarto publish`) plus, for journal submission, a MECA bundle. Use a plain `.qmd` with `format: pdf`/`typst` instead when there are no notebooks to expose to readers — the manuscript project type is for reproducible-research papers, not every PDF-producing document.

Authoring per-IDE, notebook-embedding mechanics, when to prefer a book project instead: [references/manuscripts.md](references/manuscripts.md)

---

## 16. Projects

The operational layer under website/book/dashboard/manuscript projects.

**Types:** `quarto create project <type> <name>` — `default | website | blog | book | manuscript | confluence`.

**Render control:**
```yaml
project:
  render:
    - "*.qmd"
    - "!ignored.qmd"
```
`_metadata.yml` in a subdirectory applies settings (e.g. `freeze: true`) to just that folder, merged over the project-level config.

**Profiles** — multiple variants from one source (dev vs. production, per-region reports):
```bash
quarto render --profile production
```
```yaml
# _quarto-production.yml
execute:
  freeze: false
```
Conditional content: `::: {.content-visible when-profile="production"}`.

**Pre/post-render scripts:**
```yaml
project:
  pre-render: prepare.py
  post-render: [compress.ts, fix-links.py]
```
`QUARTO_PROJECT_RENDER_ALL` distinguishes a full-project render from an incremental one inside these scripts.

**Virtual environments:** `venv`/`conda` (Python) or `renv` (R) — auto-detected by RStudio/Positron, and the same dependency files (`requirements.txt`/`environment.yml`/`renv.lock`) are what Quarto uses to configure a Binder-launchable environment automatically.

Full profile-merging rules, all script environment variables, Binder specifics: [references/projects.md](references/projects.md)

---

## 17. Reference Links

**Quarto docs:**
- [Quarto Documentation](https://quarto.org/docs/)
- [Websites](https://quarto.org/docs/websites/) · [Blogs](https://quarto.org/docs/websites/website-blog.html) · [Listings](https://quarto.org/docs/websites/website-listings.html)
- [Books](https://quarto.org/docs/books/) · [EPUB format](https://quarto.org/docs/reference/formats/epub.html)
- [Publishing](https://quarto.org/docs/publishing/) · [GitHub Actions](https://github.com/quarto-dev/quarto-actions)
- [Presentations](https://quarto.org/docs/presentations/) · [Reveal.js options](https://quarto.org/docs/reference/formats/presentations/revealjs.html)
- [Dashboards](https://quarto.org/docs/dashboards/) · [Interactive documents](https://quarto.org/docs/interactive/)
- [MS Word format reference](https://quarto.org/docs/output-formats/ms-word.html)
- [Manuscripts](https://quarto.org/docs/manuscripts/) · [Projects](https://quarto.org/docs/projects/quarto-projects.html) · [Profiles](https://quarto.org/docs/projects/profiles.html)
- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Community Extensions](https://m.canouil.dev/quarto-extensions/)
- [Typst Basics](https://quarto.org/docs/output-formats/typst.html)
- [Custom Typst Formats](https://quarto.org/docs/output-formats/typst-custom.html)
- [Book Output (Typst)](https://quarto.org/docs/books/book-output.html#typst-output)
- [Article Layout](https://quarto.org/docs/authoring/article-layout.html)
- [Typst format reference](https://quarto.org/docs/reference/formats/typst.html)
- [Typst Gather](https://quarto.org/docs/advanced/typst/typst-gather.html)

**Typst resources:**
- [Typst Reference](https://typst.app/docs/reference/)
- [Making a Template](https://typst.app/docs/tutorial/making-a-template/)
- [Typst Universe (packages)](https://typst.app/universe/)
- [Typst Forum](https://forum.typst.app/)
- [Official Typst templates](https://github.com/typst/templates)
- [Awesome Typst](https://github.com/qjcg/awesome-typst) — curated directory of 300+ tools, templates, and libraries
- Python bindings: [typst-py](https://github.com/messense/typst-py) (compile .typ from Python), [pypst](https://github.com/tilman151/pypst) (declarative Typst in Python), [mpl-typst](https://github.com/daskol/mpl-typst) (Matplotlib→Typst backend)
- Formatter: [typstyle](https://github.com/typstyle-rs/typstyle) — opinionated Typst code formatter

**Discussions & examples:**
- [Typst template parity #10223](https://github.com/orgs/quarto-dev/discussions/10223)
- [Typst book support #6979](https://github.com/orgs/quarto-dev/discussions/6979)
- [Harvard dissertation (Typst+Quarto)](https://github.com/christopherkenny/harvard-diss)
- [State immunization reports](https://github.com/claritydatastudio/state-immunization-reports) — production Typst template with custom functions (`#source()`, `#blueline()`, `#status-boxes()`), R-based but Typst patterns are language-agnostic
- [Quarto + Typst PDF reports walkthrough](https://rfortherestofus.com/2025/11/quarto-typst-pdf) — source tutorial behind the `status-box()` pattern and the scaffold/validate script workflow above
