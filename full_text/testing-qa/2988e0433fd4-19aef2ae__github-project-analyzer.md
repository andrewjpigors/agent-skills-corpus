---
name: github-project-analyzer
description: >
  Performs a structured analysis of any GitHub repository with user-selectable report depth
  and output formats. Users choose between Full (comprehensive, all sections, editorial depth)
  or Short (essentials-focused, condensed) reports, then select output format: HTML (Full only,
  interactive), Markdown (Full & Short, copyable), or PDF (Full & Short, printable). Covers
  project purpose, state, features, test coverage, architecture, incomplete work, and frank
  editorial assessment. Use whenever the user provides a GitHub URL and wants project summary,
  code review, status report, or "what does this repo do" analysis. Trigger on any github.com
  link alongside evaluation, summary, or analysis intent.
---

# GitHub Project Analyzer — Tiered Reporting Edition

Produces structured, opinionated project reports from GitHub repositories with flexible
report types (Full/Short) and output formats (HTML/Markdown/PDF).

---

## Workflow Overview

0. **Ask report type preference** — Full or Short report?
1. **Ask output format preference** — Format choice based on type selected
2. **Resolve the repository** — Parse URL, fetch top-level metadata via GitHub API
3. **Inventory the codebase** — Walk directory tree, identify languages, frameworks, config files
4. **Deep-read key artifacts** — README, source files, test files, CI configs, dependency manifests
5. **Assess test coverage** — Detect test frameworks, count test files, check for coverage reports
6. **Identify incomplete work** — Scan for TODOs, FIXMEs, stubs, NotImplementedException, placeholders
7. **Synthesize the report** — Generate sections based on selected report type (Full or Short)
8. **Generate output** — Render in chosen format (HTML/Markdown/PDF)

---

## Step 0A — Ask Report Type Preference

**Before making any fetch calls**, use `ask_user_input_v0` to present the first decision point.

```javascript
ask_user_input_v0({
  questions: [
    {
      question: "What level of detail would you like in your analysis?",
      type: "single_select",
      options: [
        "Full Report (comprehensive, all sections, editorial depth)",
        "Short Report (essentials only, condensed)"
      ]
    }
  ]
})
```

Store the user's selection. **Do not proceed to Step 0B until this response is recorded.**

---

## Step 0B — Ask Output Format Preference

Based on the report type selected in Step 0A, present the appropriate format options.

### If User Selected "Full Report":

```javascript
ask_user_input_v0({
  questions: [
    {
      question: "How would you like the full report delivered?",
      type: "single_select",
      options: [
        "Interactive HTML (navigable, best for screen reading)",
        "Comprehensive Markdown (copyable, best for documentation)",
        "PDF (portable, best for sharing/printing)"
      ]
    }
  ]
})
```

### If User Selected "Short Report":

```javascript
ask_user_input_v0({
  questions: [
    {
      question: "How would you like the short report delivered?",
      type: "single_select",
      options: [
        "Markdown (copyable, best for documentation)",
        "PDF (portable, best for sharing/printing)"
      ]
    }
  ]
})
```

Wait for the user's response, then store both preferences (report type + format) and **proceed
to Step 1. Do not begin any web fetches until both preferences are recorded.**

---

## Steps 1–6: Analysis Workflow (Unchanged)

The core analysis workflow (Steps 1–6 from original skill) remains identical. Refer to the
original SKILL.md documentation for:
- Step 1: Resolve & Fetch Repository Metadata
- Step 2: Inventory Key Files
- Step 3: Identify Incomplete Implementations
- Step 4: Assess Test Coverage
- Step 5: Synthesize the Report (see Step 7 below for report-type-specific guidance)
- Step 6: Deliver (now driven by preferences from Steps 0A–0B)

---

## Step 7 — Synthesize Report (Type-Specific)

Report content adapts based on the report type selected in Step 0A. Follow the appropriate
section guidance below.

---

## FULL REPORT STRUCTURE

Comprehensive, opinionated project evaluation for architects, decision-makers, and deep due
diligence. Target length: **1200–2500 words** depending on project size.

All **seven sections** are included with full depth. Editorial section includes multi-dimensional
quality scoring with detailed strengths, concerns, and tiered improvement suggestions.

### Section 1: Project Summary (Full Report)

Include all of the following:

| Field | Content |
|-------|---------|
| **Name** | Repo name + any product/marketing name from README |
| **Repository** | Full GitHub URL |
| **Primary Language(s)** | Sorted by prevalence (e.g., "TypeScript 70%, Python 20%, Shell 10%") |
| **Framework(s)** | All major detected frameworks (e.g., Express.js, React, Typeorm) |
| **License** | From repo metadata (or "Not specified") |
| **Last Active** | `updated_at` from API; also note creation date and total repository age |
| **Commit Activity** | Frequency assessment (e.g., "5–10 per week", "multiple per day", "1–2 per month") |
| **Community Signals** | Star count, fork count, contributor count if available |
| **Current State** | 2–3 paragraph narrative covering:<br/>• What the project is and the problem it solves<br/>• Current maturity level (prototype / alpha / beta / stable / maintenance / archived)<br/>• Development pace and health signals<br/>• Intended audience or use case<br/>• Notable dependencies or relationships to other projects |

---

### Section 2: Features & Capabilities (Full Report)

A **detailed, bulleted list** of **confirmed, implemented** features organized into logical
subsystems or domains. For each feature, include:
- Feature name
- 1–2 sentence description of what it does
- Key technologies or patterns used (if notable)

**Recommended subsystem groupings** (adapt to project):
- Core Functionality
- API / Integration Layer
- Data Access & Storage
- Authentication & Authorization
- Configuration & Deployment
- Observability & Diagnostics
- Developer Experience & Tooling
- Security & Compliance Features

For libraries/frameworks, also include:
- Public API Surface (major classes, interfaces, entry points)
- Extension Points (middleware, plugins, hooks, interceptors, custom handlers)

Aim for **20–40+ features** depending on project scope.

---

### Section 3: Incomplete Implementations (Full Report)

A **detailed table** of confirmed incomplete work, sourced from TODOs, FIXMEs,
`NotImplementedException`, stub/placeholder methods, declared ROADMAP items, and architectural
gaps identified through code review.

**Table format:**

| Area | File/Location | Description | Severity | Impact |
|------|--------------|-------------|----------|--------|
| Auth | `src/Auth/TokenService.cs:42` | Refresh token rotation not implemented | High | Cannot safely extend session lifetimes beyond 1 hour |
| Caching | `src/Services/CacheService.cs:18` | Cache invalidation strategy marked TODO | Medium | Risk of stale data in high-traffic scenarios |

**Severity definitions**:
- **High** — Blocks a core use case, critical path, or security concern
- **Medium** — Degrades functionality, required for production readiness, architectural limitation
- **Low** — Nice-to-have, cosmetic, edge case, or technical debt

**Additional guidance**:
- Link issues/PRs if available from README or code comments
- Compare declared ROADMAP items against actual code state
- Flag any stubbed-out modules that are imported but not implemented
- If no incomplete implementations found, state this explicitly

---

### Section 4: Test Coverage Assessment (Full Report)

A comprehensive 6-part evaluation:

**1. Test Infrastructure**
- Presence/absence of test projects or test directories
- Frameworks detected (xUnit, NUnit, Jest, pytest, etc.) with versions
- Test language vs. main language (if different)
- CI integration status (do tests run automatically on push/PR?)

**2. Test Scope**
- Estimated test count (e.g., "127 test methods across 18 test classes")
- Test categories if discernible: unit, integration, end-to-end, performance
- Key areas with visible test coverage vs. unverified areas

**3. Coverage Metrics**
- Is coverage actively measured and reported? (badges, CI artifacts, etc.)
- If available, cite percentage or metrics from recent runs
- Note if coverage thresholds are enforced

**4. Maturity Assessment**
- Rate using one of: **None** / **Unconfirmed** / **Minimal** / **Partial** / **Good** / **Comprehensive**
- Provide 2–3 sentence justification

**5. Notable Gaps**
- Any obvious untested areas visible from code review
- If critical paths have no test coverage, flag explicitly
- Configuration, middleware, integration layers often undertested

**6. Traversal Transparency**
- If directory tree was not fully retrieved (permissions, robots.txt), explicitly state
  which fallback evidence sources were checked (CLAUDE.md, README test sections, dependency
  manifests for test packages, CI workflows)
- **Do NOT declare coverage as "None" based solely on unverifiable tree data**

---

### Section 5: Architectural Overview (Full Report)

A detailed section covering the design and structure of the system. Only include if enough
source is readable to say something meaningful. If project is small or mostly config, abbreviate
or skip.

**Topics to cover:**
- **Design Pattern(s)**: Layered, clean architecture, hexagonal, event-driven, CQRS, serverless, etc.
- **Dependency Structure**: Major internal modules and relationships; external dependencies and roles
- **Data Flow**: How data enters, flows through, and exits the system (conceptual level)
- **Scalability Characteristics**: Visible limitations or design decisions affecting scale
- **Key Design Decisions**: Notable architectural choices visible in code with rationale
- **Integration Points**: How does this system connect to external systems (APIs, databases, queues)?

**Format suggestions:**
- 1–2 paragraph prose narrative + ASCII diagram or bullet hierarchy if complex
- Reference actual files/classes to ground the explanation
- Be honest about gaps in understandability (e.g., "event orchestration layer is not
  immediately clear from available documentation")

---

### Section 6: Editorial Assessment (Full Report)

**Opinionated, candid section written in first person.** Purpose: give the author real,
useful feedback, not diplomatic hedging.

#### A. Overall Quality Rating

Rate on a **1–10 scale** across four dimensions, with 2–3 sentence justification per:

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Code Quality | X/10 | Readability, naming conventions, structure, consistency, adherence to language idioms. Is code maintainable? Obvious anti-patterns? |
| Architecture | X/10 | Design soundness, separation of concerns, extensibility, testability. Does structure support goals? Easy to add features? |
| Project Value | X/10 | Usefulness to intended audience, originality, problem-solution fit. Does it solve a real problem well? |
| Production Readiness | X/10 | Error handling, logging, configuration, security, deployment story, monitoring hooks. Is it production-ready or prototype-stage? |

**Calculate overall score** as average of four ratings.

#### B. Strengths

List 3–5 concrete, specific strengths. **Generic praise is not useful.** Instead, cite
specific examples:
- "Exception handling is comprehensive and provides context-specific error messages"
- "CI pipeline enforces code quality gates (linting, tests, coverage thresholds)"
- "Module is loosely coupled and easy to test in isolation"

#### C. Concerns

What would give pause before using or contributing to this project? **Be frank and specific:**
- Missing error handling in critical paths
- Weak test coverage in core features
- Heavy reliance on undocumented conventions
- Security vulnerabilities or dangerous patterns
- Undocumented dependencies or assumptions

#### D. Suggested Improvements

Organize into three tiers:

**Quick Wins** (low effort, high impact — hours to days):
- Specific, actionable items with concrete first steps
- Examples: "Add type annotations to cache layer", "Document token refresh flow in README",
  "Extract constant magic numbers to named constants"

**Medium-Term Improvements** (days to weeks):
- Specific, actionable items requiring some design work
- Examples: "Refactor authentication middleware into strategy pattern for multiple auth providers",
  "Add integration tests for HTTP client retry logic"

**Strategic Enhancements** (architectural or feature-level — weeks to months):
- Major structural or capability additions
- Examples: "Implement plugin architecture for extensibility", "Add async/await support to
  synchronous code paths"

#### E. New Feature Recommendations

3–5 features not currently present that would meaningfully increase project value. For each:
- **What**: Concise feature name and description
- **Why**: User benefit and alignment with project scope
- **How**: 1–2 sentence architectural approach (not implementation detail)

---

### Section 7: Quick Reference (Full Report)

A compact summary card:

```
Project:             [name]
Repository:          [github URL]
Language(s):         [primary languages, ranked]
Framework(s):        [frameworks if applicable]
License:             [license type]
Maturity:            [Prototype / Alpha / Beta / Stable / Maintenance / Archived]
Test Coverage:       [None / Minimal / Partial / Good / Comprehensive]
Incomplete Items:    [count of TODOs, FIXMEs, NotImplementedExceptions]

Code Quality:        [X]/10
Architecture:        [X]/10
Project Value:       [X]/10
Production Ready:    [X]/10
Overall Score:       [average]/10

Status:              [1–2 sentence summary of overall health and readiness]
Recommendation:      [one sentence: "Recommended for [use case]" or "Not recommended because..."]
Next Steps:          [3–5 bullet-pointed suggested first actions if adopting/contributing]
```

---

## SHORT REPORT STRUCTURE

Focused, decision-oriented evaluation for rapid assessment and quick screening. Target length:
**500–1000 words**.

Includes Sections 1, 2, combined Test Coverage & Concerns, and condensed Editorial Summary.
Omits detailed Sections 3, 5, and 7.

### Section 1: Project Summary (Short Report)

Essentials only:

| Field | Content |
|-------|---------|
| **Name** | Repo name + product name (if any) |
| **Repository** | Full GitHub URL |
| **Primary Language(s)** | Top 1–2 languages only |
| **Framework(s)** | Major frameworks only |
| **License** | From repo metadata |
| **Last Active** | `updated_at`; note if dormant |
| **Current State** | 1 paragraph: What is it? What problem does it solve? Is it stable? |

---

### Section 2: Features & Capabilities (Short Report)

A **bulleted list** of **10–15 core features only.** No subsystem grouping. For each:
- Feature name
- 1-sentence description

Keep it scannable. Omit minor features, developer tooling, and secondary capabilities.

---

### Section 3: Test Coverage & Concerns (Short Report, Combined)

A **single concise paragraph** covering:
- Test infrastructure present? (Yes / No / Unconfirmed) + brief framework note if applicable
- Coverage maturity (None / Minimal / Partial / Good / Comprehensive) with 1-sentence justification
- 1–2 sentence callout of any **critical gaps or concerns** (if applicable)

**Example:**
```
Tests are present and integrated with CI (Jest framework, ~310 test methods across 47 files,
GitHub Actions on push/PR). Coverage is Partial because unit tests are strong for business
logic but React components lack visible test coverage, and integration scenarios (exchange
failure handling, tournament state persistence) are not fully exercised. Critical gap: no
reported coverage metrics visible in CI output.
```

---

### Section 4: Editorial Summary (Short Report, Condensed)

A **frank, single paragraph** covering:
- Overall quality rating (X/10, averaged across all dimensions)
- Top 1–2 **specific** strengths and 1–2 **specific** concerns (not generic praise)
- Single biggest improvement that would increase value

**Example:**
```
Overall: 7/10. Well-organized, novel MARL + sentiment approach with solid core logic
and good testing discipline on business logic. Strengths: clear layering, 310 test cases,
novel generational tournament mechanic. Concerns: production-unready (no structured logging,
no graceful shutdown, no health checks), React dashboard untested, exchange integration
only mocked. Biggest improvement: add structured logging, health checks, and graceful
shutdown for minimal effort + max impact on reliability.
```

---

### Section 5: Quick Reference (Short Report, Minimal)

A compact summary:

```
Project:             [name]
Language:            [primary language only]
Maturity:            [Prototype / Alpha / Beta / Stable / Maintenance]
Test Coverage:       [rating]
Overall Score:       [X]/10
Recommendation:      [one sentence]
```

---

## Step 8 — Output Generation (Format-Specific)

Render the synthesized report in the format chosen in Step 0B. Follow the specifications below.

---

## HTML Format (Full Reports Only)

**File location:** `/mnt/user-data/outputs/{repo-name}-analysis.html`

Generate an **interactive, navigable HTML report** with the following structure and features:

### HTML Structure

Use semantic HTML5 with embedded CSS (no external dependencies):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{Repo Name} - Project Analysis</title>
  <style>
    /* All CSS embedded here for portability */
  </style>
</head>
<body>
  <!-- Header with project name and generation date -->
  <header class="analysis-header">
    <h1>{Repo Name} — Project Analysis</h1>
    <p>Generated {date} from <a href="{github-url}">{github-url}</a></p>
  </header>

  <!-- Sidebar navigation with section anchors -->
  <nav class="sidebar">
    <ul>
      <li><a href="#summary">Project Summary</a></li>
      <li><a href="#features">Features & Capabilities</a></li>
      <li><a href="#incomplete">Incomplete Implementations</a></li>
      <li><a href="#testing">Test Coverage</a></li>
      <li><a href="#architecture">Architectural Overview</a></li>
      <li><a href="#editorial">Editorial Assessment</a></li>
      <li><a href="#reference">Quick Reference</a></li>
    </ul>
    <!-- Dark mode toggle -->
    <button id="theme-toggle" aria-label="Toggle dark mode">🌙</button>
  </nav>

  <!-- Main content -->
  <main class="report-content">
    <section id="summary">
      <h2>Project Summary</h2>
      <!-- Content rendered here -->
    </section>

    <section id="features">
      <h2>Features & Capabilities</h2>
      <!-- Collapsible subsystems for long lists -->
      <details>
        <summary>Core Functionality</summary>
        <!-- Content -->
      </details>
    </section>

    <!-- Additional sections ... -->

    <!-- Quick Reference card in styled box -->
    <section id="reference" class="quick-reference-card">
      <h2>Quick Reference</h2>
      <!-- Key metrics in grid or table -->
    </section>
  </main>

  <footer>
    <p>Generated by GitHub Project Analyzer</p>
  </footer>

  <script>
    // Dark mode toggle with localStorage
    // Smooth scroll navigation handlers
    // Copy-to-clipboard button functionality
    // Collapsible section handlers
  </script>
</body>
</html>
```

### HTML Features

- **Fixed sidebar navigation** with anchor links to all sections, smooth scroll
- **Dark/light mode toggle** with localStorage persistence for user preference
- **Responsive design** optimized for desktop and mobile viewports
- **Collapsible sections** (using `<details>`/`<summary>`) for Incomplete Implementations and Improvements if lengthy
- **Copy-to-clipboard buttons** for code blocks, metadata cards, and quick reference
- **Professional styling** with semantic HTML5, clean typography, color scheme
- **Print-friendly CSS** that hides navigation, adjusts spacing for paper output
- **Self-contained file** (all CSS and JavaScript embedded, no external dependencies)

### HTML Styling Guidelines

- **Color scheme**: Professional (blues, grays, subtle accent colors)
- **Typography**: Sans-serif headings (14–16pt), serif body text (11pt), 1.5 line-height
- **Tables**: Light shading on alternating rows for readability
- **Code blocks**: Monospace font (10pt), light gray background
- **Spacing**: 1-inch margins, logical section separation
- **Dark mode**: Invert colors appropriately (light background → dark, dark text → light)

---

## Markdown Format (Full & Short)

**File location:** `/mnt/user-data/outputs/{repo-name}-analysis.md` or `{repo-name}-analysis-short.md`

Generate a **well-formatted Markdown document** with:

### Markdown Structure

```markdown
# {Repo Name} — Project Analysis

*Generated {date} | [View on GitHub]({github-url})*

---

## Project Summary

**Name:** ...
**Repository:** ...
**Primary Language(s):** ...
[... other fields ...]

{Narrative content...}

---

## Features & Capabilities

### Core Functionality
- **Feature A**: Description.
- **Feature B**: Description.

[... other subsystems ...]

---

## [Additional Sections as per report type]

---

## Quick Reference

```
Project:             ...
Overall Score:       .../10
Recommendation:      ...
```

---

*Report generated by GitHub Project Analyzer*
```

### Markdown Conventions

- Use `##` for major sections, `###` for subsections
- Use `| --- |` markdown tables for structured data
- Fenced code blocks with language hints (```csharp, ```javascript, ```python)
- Inline `code` formatting for file names, identifiers, method names
- Horizontal rules (`---`) to visually separate major sections
- Links as `[text](url)` Markdown syntax
- Bold for emphasis: **important terms**
- Blockquotes for callouts or important notes: `> Note: ...`

### Markdown Advantages

- Plain text, version-control friendly
- Renders cleanly on GitHub, VS Code, GitLab, and markdown preview tools
- Easy to copy/paste into documentation or knowledge bases
- Diffs are human-readable
- No dependencies or rendering issues

---

## PDF Format (Full & Short)

**File location:** `/mnt/user-data/outputs/{repo-name}-analysis.pdf` or `{repo-name}-analysis-short.pdf`

Generate a **professional, printable PDF report** with:

### PDF Structure

1. **Title Page**
   - Project name and repository URL
   - Generation date and analyst/tool attribution
   - Executive summary (1–2 paragraph high-level overview)

2. **Table of Contents**
   - Auto-generated with page numbers
   - Hyperlinked for navigation in PDF viewers

3. **Main Report Content**
   - Sections in logical page breaks
   - Headers and footers with project name and page numbers
   - Professional pagination avoiding orphaned content

4. **Appendices** (if Full report with substantial data)
   - Detailed improvement roadmaps
   - Additional metrics or technical details

### PDF Styling

- **Page size**: Letter (8.5" × 11")
- **Margins**: 1 inch on all sides
- **Body font**: Serif, 11pt (e.g., Georgia, Garamond, Cambria)
- **Heading font**: Sans-serif, 14–16pt (e.g., Helvetica, Arial)
- **Line height**: 1.5 for readability
- **Tables**: Light shading on alternating rows, centered cells
- **Code blocks**: Monospace font (10pt), light gray background
- **Page headers/footers**: "{Repo Name} — Project Analysis | Page {X}"
- **Hyperlinks**: Underlined, colored (blue or accent color)

### PDF Generation Approaches

**Option A: Python `reportlab` library** (recommended if available)
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate(
    filename,
    pagesize=letter,
    rightMargin=72, leftMargin=72,
    topMargin=72, bottomMargin=18
)

story = [
    # Title page
    Paragraph(f"<b>{repo_name} — Project Analysis</b>", styles['Title']),
    # Table of contents
    # Main sections
    # Each section built as Platypus elements
]

doc.build(story, onFirstPage=add_page_header, onLaterPages=add_page_header)
```

**Option B: Markdown → Pandoc conversion** (bridge solution)
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=weasyprint \
  --css=styles.css \
  --variable=geometry:margin=1in \
  --variable=title="{repo-name} Analysis"
```

**Option C: HTML → Browser automation** (as fallback)
- Generate clean HTML, use Puppeteer/Playwright to export PDF with print CSS

---

## Delivery Rules (Steps 0A–0B → Output Generation)

| User Selection | Chat Output | File Output | Notes |
|---|---|---|---|
| Full + HTML | 1-paragraph executive summary | `{repo-name}-analysis.html` (interactive HTML) | Most immersive; best for screen reading |
| Full + Markdown | 1-paragraph executive summary | `{repo-name}-analysis.md` (comprehensive Markdown) | Most versatile; version-control friendly |
| Full + PDF | 1-paragraph executive summary | `{repo-name}-analysis.pdf` (printable PDF) | Professional delivery; print-optimized |
| Short + Markdown | Display short report inline (no summary needed) | `{repo-name}-analysis-short.md` (short Markdown) | Quick reference; ~600 words |
| Short + PDF | Display short report inline (no summary needed) | `{repo-name}-analysis-short.pdf` (short PDF) | Portable quick assessment |

**One-paragraph executive summary** (used when Full report is generated as file-only):
- Include: project name, primary language, maturity level, overall score, top 1–2 specific
  strengths, and single most important recommendation
- Then present the file download link
- Do not repeat section content; this is a teaser/summary only

**File naming convention**:
- Full reports: `{repo-name}-analysis.{ext}` (where ext is html, md, or pdf)
- Short reports: `{repo-name}-analysis-short.{ext}`
- Example: `sentiment-analyzer-analysis.html`, `sentiment-analyzer-analysis-short.md`
- Use lowercased repository name; replace hyphens/underscores consistently

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Repo is private / 404 | Inform user, ask for public URL or GitHub PAT |
| README is empty/missing | Note in Section 1; flag in editorial as a concern |
| Very small repo (< 5 files) | Complete the report but keep it proportionally brief; note in editorial |
| Monorepo | Focus on primary/most active module; note monorepo structure in Section 1 |
| No source code (docs-only) | Adjust report structure; skip code quality ratings; focus on documentation value |
| Rate limit hit | Use unauthenticated requests where possible; if blocked, report to user and retry later |
| Tree traversal blocked (robots.txt/permissions) | **Do NOT infer absence of tests from missing tree data.** Run fallback checks: CLAUDE.md, README test sections, dependency manifests for test packages, CI workflows |
| PDF generation fails | Fall back to Markdown output; note in chat that PDF generation encountered an issue and provide Markdown file instead |
| HTML generation fails | Fall back to Markdown output; note in chat |

---

## Implementation Notes

### For HTML Generation

- Use `visualize:show_widget` with clean HTML/CSS for preview in chat (optional)
- Programmatically generate the full HTML file using string templating or lightweight library
- Ensure CSS is **embedded** (not external) so the file is self-contained and portable
- Test on multiple viewport sizes (desktop, tablet, mobile)
- Use localStorage for dark mode toggle persistence
- Provide copy-to-clipboard functionality for code blocks and metadata

### For Markdown Generation

- Build report as a string with careful attention to Markdown syntax
- Use consistent code fence markers (```), always include language hints
- Ensure all URLs are properly formatted as Markdown links: `[text](url)`
- Test rendering in GitHub markdown preview, VS Code markdown preview
- Validate table formatting (all cells aligned, pipes properly escaped)

### For PDF Generation

- **Recommended approach**: Python `reportlab` if available in environment
- Alternative: Generate clean Markdown, pipe to `pandoc` with `weasyprint` backend
- Ensure all fonts are embedded or system-available
- Test on multiple PDF readers (Adobe, browser native PDF viewer, etc.)
- Verify page breaks occur at logical section boundaries (avoid orphaned headers)

### Calling `present_files`

After generating any output file(s), always call `present_files` with the appropriate file path:

```javascript
present_files({
  filepaths: [
    "/mnt/user-data/outputs/{repo-name}-analysis.html"
  ]
})
```

Only call for files that exist and are ready for download. Multiple files can be passed:

```javascript
present_files({
  filepaths: [
    "/mnt/user-data/outputs/{repo-name}-analysis.md",
    "/mnt/user-data/outputs/{repo-name}-analysis.pdf"
  ]
})
```

---

## Notes for Kurt's Projects

When analyzing repositories belonging to Kurt Mitchell (`github.com/kmitch2300` or organization
`github.com/infinyte`), apply additional context:

- **Primary stack**: .NET/C#, TypeScript/Node.js, Azure cloud services, Semantic Kernel
- **Architectural patterns**: Weight feedback toward Zero Trust, Clean Architecture, layered
  patterns, DDD, and canonical data models
- **Code conventions**: Flag deviations from Microsoft naming and coding guidelines
- **Integration patterns**: Note alignment or divergence from established patterns
  (DocFlow, CDM, previous FLIFO work)
- **Development maturity**: Consider project context (side project vs. flagship); adjust editorial
  expectations accordingly
- **Feynman technique preference**: Lead with hole-checking for negative assessments before
  encouraging elements; provide evidence for positive ratings; avoid generic praise

---

## Original Reference: Steps 1–6 Analysis

For complete details on data collection and analysis (Steps 1–6), refer to the original
github-project-analyzer SKILL.md documentation, which remains unchanged. The workflow for:

- Resolving repository metadata
- Inventorying the codebase
- Deep-reading key artifacts
- Assessing test coverage
- Identifying incomplete implementations

...is **identical to the original skill** and should be followed as previously documented.

The enhancements in this version apply only to:
1. **Preference elicitation** (Steps 0A–0B: new two-step flow)
2. **Report synthesis** (Step 7: type-specific section depth)
3. **Output generation** (Step 8: format-specific rendering)

---

## Summary of Enhancements

### What's New

✓ **Two-step preference flow**: Report type (Full/Short) → Format (HTML/Markdown/PDF)  
✓ **Full Report**: Comprehensive 7-section evaluation (1200–2500 words)  
✓ **Short Report**: Essentials-focused 4-section assessment (500–1000 words)  
✓ **Three output formats**: Interactive HTML (Full only), copyable Markdown (both), professional PDF (both)  
✓ **Enhanced editorial**: Multi-dimensional scoring with specific strengths/concerns and tiered improvements  
✓ **Flexible delivery**: Users choose depth and format matching their needs  

### What's Unchanged

✓ **Analysis workflow** (Steps 1–6) — identical to original  
✓ **Data collection methods** — all the same  
✓ **Error handling patterns** — consistent approach  
✓ **Trigger patterns** — "analyze my repo", "review this project", etc.  
✓ **Architectural patterns** — no changes to how analysis is performed  

