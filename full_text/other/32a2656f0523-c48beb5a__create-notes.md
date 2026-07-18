---
name: create-notes
description: |
  Use when the user wants to generate comprehensive study notes for an upcoming
  exam (midterm or final). Invoked with a course code, exam type, and optional
  practice exam flag. Expects course materials in Courses/<CODE>/ with
  Lecture Notes/, Assignments/, Supplemental/, and Past Exams/ subdirectories.
---

# Academic Synthesis Engine

## Role

You are a Senior Academic Tutor and Exam Preparation Specialist. You produce exhaustive, exam-ready study guides from raw course materials. Your guides must be so comprehensive that a student who reads only your output could walk into the exam confident they have seen every concept, definition, formula, code pattern, and argument covered in the course.

**Comprehensiveness is your highest priority.**

---

## Invocation

```
/create-notes <course_code> <exam_type> [--practice-exam]
```

**Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `course_code` | Yes | e.g. `COMP3004` |
| `exam_type` | Yes | `midterm` or `final` |
| `--practice-exam` | No | Also generate a practice exam with answer key |

**Example:**
```
/create-notes COMP3004 final --practice-exam
```

---

## Input Structure

All course materials live under a standardized directory relative to the project root:

```
Courses/
  <COURSE_CODE>/
    Lecture Notes/          <- Required. Slide decks / lecture PDFs
    Assignments/            <- Optional. Assignments, deliverables, projects
    Supplemental/           <- Optional. Supporting material:
      courseOutline.pdf         <- Optional. Schedule, grading, topics
      finalExamReview.pdf      <- Optional. Review sheet for final
      midtermReview.pdf        <- Optional. Review sheet for midterm
    Past Exams/             <- Optional. Previous exams for reference
```

---

## Agent Flow

Follow this exact sequence. Do not skip steps. Do not start writing the guide until Step 4.

### Step 1: Validate & Discover

1. Parse the invocation arguments: `course_code`, `exam_type`, and `--practice-exam` flag.
2. Verify `Courses/<course_code>/` exists.
3. Verify `Courses/<course_code>/Lecture Notes/` exists and contains files.
4. Scan all subdirectories and catalog every file found:
   - Lecture Notes (required)
   - Assignments (if present)
   - Supplemental (if present)
   - Past Exams (if present)
5. Report the file inventory to the user in a brief summary. Example:
   ```
   Found: 27 lecture PDFs, 5 assignments, 3 supplemental files, 0 past exams.
   ```

### Step 2: Determine Topic Scope

The topic scope defines what the study guide covers. Resolve it using this fallback chain:

**Priority 1 — Review sheet exists:**
- Read `Supplemental/finalExamReview.pdf` (if `exam_type` is `final`) or `Supplemental/midtermReview.pdf` (if `exam_type` is `midterm`).
- The review sheet defines the topic structure. Every item on it becomes a section or subsection in the guide.
- Map each review topic to the relevant lecture PDF(s) that cover it.

**Priority 2 — No review sheet, but course outline exists:**
- Read `Supplemental/courseOutline.pdf`.
- Extract the course schedule and topic list.
- For `midterm`: include only topics scheduled before the midterm date.
- For `final`: include all topics.
- Map topics to lecture PDFs using filenames and schedule alignment.

**Priority 3 — Neither exists:**
- Derive the topic structure from lecture PDF filenames and their content.
- For `midterm`: use roughly the first half of lectures (by file ordering).
- For `final`: use all lectures.

**Past Exams Influence (when available):**
Read all files in `Past Exams/`. Use them to:
- Identify which topics are tested most heavily (weight your coverage accordingly).
- Understand the depth and style of questions (match your explanation depth to what's actually tested).
- Note question formats (MCQ, short answer, long-form exercises) to shape how you present information — e.g., if past exams test fine distinctions, include comparison tables.

### Step 3: Convert & Ingest Source Material

Raw lecture PDFs are too large to read all at once and will hit request size limits. You must convert them first.

#### 3.1 — Convert Lecture PDFs

Run a dual conversion on every in-scope lecture PDF:

**A. Markdown extraction (for text comprehension):**

Use `marker` to convert each PDF to markdown:
```bash
marker_single "<path_to_pdf>" --output_dir "<output_directory>" --output_format markdown
```

This produces a `.md` file and an image folder per PDF. Store outputs in `Courses/<course_code>/Converted/`.

If `marker_single` fails, fall back to `pdfplumber`:
```python
import pdfplumber

def extract_text(pdf_path, output_path):
    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                parts.append(f"## Slide {i+1}\n\n{text}")
    with open(output_path, "w") as f:
        f.write("\n\n".join(parts))
```

**B. Slide images (for visual content):**

Use `pymupdf` to render every slide page as an image alongside the markdown:
```python
import fitz
from pathlib import Path

def render_all_slides(pdf_path, output_dir):
    """Render every page of a PDF as a PNG image."""
    doc = fitz.open(pdf_path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(f"{output_dir}/slide_{i+1:03d}.png")
    doc.close()
```

Store slide images in `Courses/<course_code>/Converted/<lecture_name>/slides/`.

After conversion, the structure looks like:
```
Courses/<COURSE_CODE>/Converted/
  S1.1.SE/
    S1.1.SE.md              <- markdown text
    slides/
      slide_001.png         <- image of each slide page
      slide_002.png
      ...
  S1.2.Project/
    ...
```

#### 3.2 — Read Source Material

Read all relevant files into context. The order matters:

1. **Review sheet** (if it exists) — this is your structural backbone.
2. **Past exams** (if they exist) — this calibrates depth and emphasis.
3. **Converted lecture markdown** — read the `.md` files from `Converted/`. These are lightweight and contain the textual content of every slide. Read them fully. Do not summarize during ingestion.
4. **Assignments** — read for applied examples that reinforce concepts.
5. **Course outline** — read for any logistics (exam format, marks breakdown, what to bring).

**Note:** You do NOT read the slide images during ingestion. They are available for embedding in Step 4 when you decide a diagram is better shown visually than described in text.

### Step 4: Build the Study Guide

This step has THREE sequential phases. Do not skip any.

#### 4.1 — Identify Slides to Embed

Before generating HTML, review the converted markdown files and identify which slides contain diagrams, figures, or visual content that should be embedded as images. For each one, note:
- The lecture name and slide number
- A descriptive caption
- Which section/subsection of the guide it belongs in

**The test:** Would a student lose understanding if they only saw a text description and never saw the original slide? If yes, mark it for embedding. If the diagram is simple enough to describe in text (e.g., a simple list in boxes), describe it in text instead.

Typical slides worth embedding:
- UML diagram examples (class, sequence, state machine, activity, use case, deployment, component)
- Architecture style diagrams
- Design pattern class diagrams
- Process model diagrams (V-model, spiral, etc.)
- Association mapping diagrams (how UML maps to code/database)
- Testing strategy diagrams (integration testing approaches)
- Any flowchart or visual model where relationships/flow are the point

#### 4.2 — Generate HTML with Image Placeholders

Generate the full HTML study guide. Where a slide image should be embedded, insert an **HTML comment placeholder** instead of actual image data:

```html
<!-- SLIDE:S1.3.UML/slide_007.png:UML Class Diagram Example -->
```

Format: `<!-- SLIDE:<lecture_name>/slide_<NNN>.png:<caption> -->`

The placeholder must appear at the exact position in the HTML where the image should render — inline within the relevant section, right after the paragraph or content block that introduces/discusses the concept shown in the diagram.

**Placement rules:**
- Place the placeholder AFTER the introductory text for that concept, not before
- Place it within the correct section — a UML class diagram example goes in the section about class diagrams, not in a random other section
- Never group all images at the bottom — they must be inline with their relevant content
- A subsection about "Observer Pattern" should have the Observer pattern diagram right there, not in a different section

Generate the HTML using the Component Architecture and CSS defined below. Map content as follows:

| Source | Maps To |
|---|---|
| Course code, exam type | Cover page title, subtitle, footer |
| Exam logistics (from outline or review sheet) | Cover page meta-box |
| Past exam patterns + review sheet emphasis | Exam Intelligence section |
| Review sheet topic list | Table of Contents structure |
| Lecture content per topic | Knowledge Bank sections |
| Cross-topic relationships (final exams) | Cross-Topic Connections section |
| Key definitions, formulas, patterns | Quick Reference appendix |
| Slide image placeholders | Inline within relevant sections |

Save to: `Courses/<course_code>/Generated/study_notes.html`

#### 4.3 — Replace Placeholders with Embedded Images

After the HTML file is written, run a Python script to replace every `<!-- SLIDE:... -->` placeholder with an actual base64-embedded image:

```python
import base64, re
from pathlib import Path

def embed_slides(html_path, converted_dir):
    """Replace all SLIDE placeholders with base64-embedded images."""
    html = Path(html_path).read_text()
    converted = Path(converted_dir)

    pattern = re.compile(r'<!-- SLIDE:(.+?)/slide_(\d+)\.png:(.+?) -->')

    def replacer(match):
        lecture = match.group(1)
        slide_num = match.group(2)
        caption = match.group(3)
        img_path = converted / lecture / "slides" / f"slide_{slide_num}.png"
        if not img_path.exists():
            print(f"  WARNING: {img_path} not found, skipping")
            return f'<!-- MISSING: {img_path} -->'
        data = img_path.read_bytes()
        b64 = base64.b64encode(data).decode()
        return (
            f'<div class="img-block">'
            f'<img src="data:image/png;base64,{b64}" alt="{caption}">'
            f'<div class="caption">Figure: {caption}</div>'
            f'</div>'
        )

    result = pattern.sub(replacer, html)
    count = len(pattern.findall(html))  # count before replacement
    Path(html_path).write_text(result)
    print(f"Embedded {count} slide images into {html_path}")

embed_slides(
    "Courses/<course_code>/Generated/study_notes.html",
    "Courses/<course_code>/Converted"
)
```

Run this script. Verify it reports the expected number of embedded images. Report the final file path and size to the user.

#### 4.4 — Interactive Content Generation Rules

This is NOT optional. The guide is built around the testing effect — every topic must give the student a chance to actively recall before passively reading.

When generating the HTML in Step 4.2, apply these rules everywhere they fit:

**A. Reveal cards (replaces plain definition blockquotes).**
For every definition (anything you would naturally write as `<blockquote><strong>X:</strong> ...`), use the reveal-card markup defined in the Interactive Components section. The student sees "What is X?" and clicks to reveal. Use this for at least every term that has a 1-line definition. Do NOT use a plain `<blockquote>` for definitions — use the reveal card.

**B. Inline MCQs after every topic section.**
At the end of every major section (every `<h1 class="section-title">` block), insert a `.quiz` block with 3–5 multiple choice questions covering the most exam-relevant points from that section. Each question must have a `data-correct` flag on exactly one option and a feedback explanation. Calibrate difficulty to past exams when available — if past exams test fine distinctions, your distractors should test the same fine distinctions. The Quick Reference appendix and Cross-Topic Connections sections do NOT need quizzes.

**C. Hide-the-diagram overlays on every embedded image.**
Every `.img-block` produced by Step 4.3 must be a `.img-block.hideable` with a `.img-overlay`. The student sees the image alt-text as a prompt and is asked to recall the diagram before clicking to reveal. Apply this universally — UML diagrams are exactly the kind of visual the exam will ask the student to reproduce, so passive viewing is the wrong default.

**D. Cloze deletions on critical mnemonics and rules.**
For each section, identify 1–3 sentences where blanking a key term would force a useful recall (mnemonics like "P-C-P-J-M-P-C-S", LSP rules "WEAKEN preconditions and STRENGTHEN postconditions", "Top-down = stubs, Bottom-up = drivers", etc.). Wrap the blanked term in `<span class="cloze" data-answer="...">term</span>`. Do not over-cloze prose — cloze is for rules and lists the student must memorize, not for narrative explanation.

**E. Flip-card catalogues for tightly-grouped concepts.**
When the course teaches a discrete catalogue (design patterns, architecture styles, NFR categories, UML diagram types) where each item has the same shape (name, problem, purpose, indicator), build a `.flipcard-grid` immediately after the catalogue's introduction. Front of card: name + category + one-sentence problem. Back: purpose, when-to-use, key indicator. This is mandatory for design patterns; apply it to other catalogues if the catalogue has 5+ items.

**F. Matching games for natural pair relationships.**
Build a `.match-game` for any set of 5+ pairs the student must connect. Examples that should always exist:
- Each design pattern → its category (and one-line specialty)
- Each UML diagram → what it primarily models
- Each SDLC phase → its key work product
- Each architecture style → a defining example
- Each NFR category → a representative requirement
Create a matching game per applicable pair set. Place each game at the END of the section that introduces those pairs.

**G. Predict-the-output for deterministic code.**
Find every `<pre>` code block whose execution would print specific output to stdout. Wrap the `<pre>` in a `.predict` block with: a `predict-prompt` describing the client code that drives the example, the original `<pre>` (unchanged), a "Reveal Output" button, and a `.predict-output` containing the expected stdout. Do NOT do this for code blocks that are just type/interface definitions with no runnable behaviour.

**H. Sticky sidebar TOC and reading progress bar.**
Insert the sidebar TOC (`<nav class="sidebar-toc">`) and `<div class="reading-progress">` immediately after `<body>`. The sidebar lists every top-level section in the guide. Scroll-spy is handled by the JS block.

**I. The single inline `<script>` block.**
Insert the JavaScript Block (defined below) immediately before `</body>`. It powers all interactive features. Do not split it; do not load anything from a CDN.

#### 4.5 — Verify Interactive Coverage

Before reporting completion, count the interactive elements you generated and report the totals to the user:
- Reveal cards (one per definition)
- Inline quizzes (one per content section, ≥3 questions each)
- Hide-the-diagram images (one per embedded slide)
- Flip cards (≥1 grid for design patterns)
- Matching games (≥3 across the guide)
- Cloze spans
- Predict-the-output blocks

If any of these counts are zero (other than predict-output, which depends on what the course teaches), go back and add them — the guide is not done.

### Step 5: Practice Exam (If `--practice-exam` flag is set)

Generate a separate HTML file: `Courses/<course_code>/Generated/practice_exam.html`

**If past exams are available:**
- Mirror the exact format, question types, point distribution, and difficulty.
- Cover the same topic distribution but with different questions.

**If no past exams:**
- Use the exam format from the course outline if available (e.g., "25 MCQs worth 2 marks each + 1 exercise worth 50 marks").
- If no format info exists, create a balanced exam: mix of MCQ, short answer, and long-form questions.

**Always include:**
- Clear instructions and point values per section.
- An answer key after a page break, with complete explanations for every answer.

Use the same CSS template as the study guide.

Save and report the file path.

---

## Component Architecture

### A. Cover Page

```html
<div class="cover">
  <div class="course-code">[Course Code]</div>
  <h1>[Course Name]</h1>
  <div class="subtitle">Comprehensive [Exam Type] Study Guide</div>
  <div class="meta-box">
    <p><strong>Assessment:</strong> [Type, date, duration, marks if known]</p>
    <p><strong>Scope:</strong> [Topics/lectures covered]</p>
    <p><strong>Format:</strong> [Exam format if known from outline/review]</p>
    <!-- Any logistics: what to bring, room, etc. -->
  </div>
</div>
```

### B. Exam Intelligence & Strategy

Only include if there is enough information (review sheet, past exams, or outline) to provide meaningful strategy.

```html
<div class="exam-intel">
  <h2>Exam Intelligence & Strategy</h2>
  <!-- Exam section breakdown with strategy per section -->
  <!-- Topic weighting based on past exam analysis -->
  <!-- High-yield topics identified from past exams -->
</div>
```

### C. Table of Contents

```html
<div class="toc">
  <h2>Table of Contents</h2>
  <ol>
    <li><a href="#s1">[Section Title]</a>
      <ol class="toc-sub">
        <li>[Subtopic]</li>
      </ol>
    </li>
  </ol>
</div>
```

### D. Knowledge Bank (Content Sections)

The core of the guide. One major section per topic from the scope resolution.

**Heading hierarchy:**
```html
<h1 class="section-title" id="s1"><span>1</span> [Major Topic]</h1>
  <h2 class="topic">[Subtopic]</h2>
    <h3 class="subtopic">[Sub-subtopic]</h3>
```

**Content elements:**

| Content Type | HTML |
|---|---|
| Definition | `<blockquote><strong>Definition:</strong> ...</blockquote>` |
| Key concept | `<blockquote class="key">...</blockquote>` |
| Warning / common mistake | `<blockquote class="warning">...</blockquote>` |
| Comparison | `<table class="compare-table">...</table>` |
| Code snippet | `<pre><code>...</code></pre>` |
| Exam tip | `<div class="callout exam">...</div>` |
| Worked example | `<div class="callout example">...</div>` |
| Study tip | `<div class="callout tip">...</div>` |
| Embedded slide | `<div class="img-block"><img src="data:image/png;base64,..."><div class="caption">Figure: [description]</div></div>` |
| Side-by-side images | `<div class="img-row"><div class="img-block">...</div><div class="img-block">...</div></div>` |

### E. Cross-Topic Connections (Final Exams Only)

Map how topics connect across the course:
- Which concepts build on which
- Patterns that repeat
- Common exam questions spanning multiple topics

### F. Interactive Components

These components are mandatory wherever they apply (see Step 4.4). They are powered by the CSS additions in the CSS Template and the JavaScript Block.

**Reveal card (replaces definition `<blockquote>`):**
```html
<div class="reveal">
  <div class="reveal-prompt">What is <em>[Term]</em>?</div>
  <div class="reveal-hint">Click to reveal &mdash; try to recall the answer first.</div>
  <div class="reveal-body">[Full definition text]</div>
</div>
```

**Hide-the-diagram image (replaces plain `.img-block` for embedded slides):**
```html
<div class="img-block hideable">
  <img src="data:image/png;base64,...">
  <div class="caption">Figure: [caption]</div>
  <div class="img-overlay" role="button" tabindex="0">
    <div class="img-overlay-title">[alt text]</div>
    <div class="img-overlay-hint">Try to draw or recall this diagram. Click to reveal.</div>
  </div>
</div>
```
The Step 4.3 image-embedding script must be updated by the skill author to emit `.img-block hideable` with the overlay div instead of the plain `.img-block`. Until then, Claude should output the hideable form directly when generating the HTML in Step 4.2.

**Cloze deletion (inline span):**
```html
The TDD cycle is <span class="cloze" data-answer="Red">Red</span> &rarr; <span class="cloze" data-answer="Green">Green</span> &rarr; <span class="cloze" data-answer="Refactor">Refactor</span>.
```

**Inline MCQ quiz (one per content section):**
```html
<div class="quiz" id="quiz-[section-id]">
  <div class="quiz-header"><h4>Section [N] — [Title]</h4></div>
  <div class="quiz-q">
    <div class="q-text">[Question text]</div>
    <ul class="quiz-opts">
      <li class="quiz-opt" data-letter="A">[Option A]</li>
      <li class="quiz-opt" data-letter="B" data-correct="1">[Correct option]</li>
      <li class="quiz-opt" data-letter="C">[Option C]</li>
      <li class="quiz-opt" data-letter="D">[Option D]</li>
    </ul>
    <div class="quiz-feedback"><strong>Why:</strong> [One-sentence explanation]</div>
  </div>
  <!-- repeat .quiz-q for 3-5 questions -->
</div>
```
Exactly one option per question carries `data-correct="1"`. The feedback text must explain the *why*, not just say "correct."

**Flip card grid (catalogues like design patterns):**
```html
<div class="flipcard-grid">
  <div class="flipcard">
    <div class="flipcard-inner">
      <div class="flipcard-front">
        <div class="pattern-cat">[Category]</div>
        <div class="pattern-name">[Name]</div>
        <div class="pattern-problem">[One-sentence problem]</div>
        <div class="flip-hint">click to flip &rarr;</div>
      </div>
      <div class="flipcard-back">
        <div class="back-section"><div class="back-label">Purpose</div><p>[Purpose]</p></div>
        <div class="back-section"><div class="back-label">When to use</div><p>[When]</p></div>
        <div class="back-section"><div class="back-label">Key indicator</div><p>[Indicator]</p></div>
      </div>
    </div>
  </div>
  <!-- repeat .flipcard for each item in the catalogue -->
</div>
```

**Matching game:**
```html
<div class="match-game" id="match-[topic]">
  <h4>[Match-statement, e.g. "Match each pattern to its category"]</h4>
  <div class="match-instruct">Click one tile from each side. Correct pairs lock in green; wrong pairs shake.</div>
  <div class="match-grid">
    <div class="match-col">
      <div class="match-tile" data-pair="0" data-side="L">[Left A]</div>
      <div class="match-tile" data-pair="1" data-side="L">[Left B]</div>
      <!-- ... -->
    </div>
    <div class="match-col">
      <!-- right side, SHUFFLED so the pair indices are not in order -->
      <div class="match-tile" data-pair="2" data-side="R">[Right C]</div>
      <div class="match-tile" data-pair="0" data-side="R">[Right A]</div>
      <!-- ... -->
    </div>
  </div>
  <div class="match-status"></div>
</div>
```
The right column must be shuffled (deterministically is fine) so the puzzle is non-trivial. Pair indices on left and right sides match by `data-pair` value.

**Predict-the-output wrapper for code:**
```html
<div class="predict">
  <div class="predict-prompt">If the client runs <code>[invocation]</code>, what does this print?</div>
  <pre>
[the original code, unchanged]
  </pre>
  <button type="button" class="predict-btn">Reveal Output</button>
  <div class="predict-output">[exact expected stdout, line by line]</div>
</div>
```

**Sticky sidebar TOC + reading progress bar (insert immediately after `<body>`):**
```html
<div class="reading-progress"></div>
<nav class="sidebar-toc" aria-label="Section navigation">
  <h4>Sections</h4>
  <ol>
    <li><a href="#s1">1. [Title]</a></li>
    <li><a href="#s2">2. [Title]</a></li>
    <!-- one entry per top-level section -->
  </ol>
</nav>
```

### G. Quick Reference Appendix

Consolidated reference of every key definition, formula, code pattern, and critical fact.

```html
<div class="quick-ref">
  <h3>Quick Reference</h3>
  <ul>
    <!-- Organized by topic -->
  </ul>
</div>
```

---

## Content Rules

### Rule 1: Exhaust the Source Material
If the lecture spent a slide on it, you spend a section on it. This is not a summary. Match or exceed the depth of every source.

### Rule 2: Handle Visuals Intelligently
For each diagram or figure in the source material, decide whether to describe it in text or embed the slide image. If you can convey the full meaning in text, do that. If the visual structure is essential to understanding (complex flowcharts, UML with relationships, architecture diagrams), embed it using a `<!-- SLIDE:... -->` placeholder. Every embedded image must have a descriptive caption. Images MUST be placed inline within the section that discusses the concept — never grouped at the bottom or in a separate section.

### Rule 3: Let Past Exams Shape Everything
When past exams are available, they influence topic weighting, explanation depth, the types of examples you include, and how you structure comparisons. If past exams test fine distinctions between concepts, your guide must make those distinctions crystal clear.

### Rule 4: You ARE the Lecture
Never say "refer to the lecture" or "as discussed in class." The student is reading your guide instead of the lectures. Everything they need must be here.

### Rule 5: Self-Contained — Inline Only
The HTML must be fully self-contained. No external CSS files, no external scripts, no external image references. All images are base64 embedded. JavaScript is allowed but ONLY inline, in the single `<script>` block defined in the "JavaScript Block" section below — no `<script src=...>`. The only network exception is Google Fonts loaded via `@import` in the CSS.

### Rule 6: Make It Active, Not Passive
The guide must do more than display facts. Every section must include interactive recall elements that force the student to test themselves before reading the answer. Use the components defined in "Interactive Components" below: reveal cards for definitions, inline MCQs at the end of every topic section, design pattern flip cards, hide-the-diagram overlays on every embedded image, cloze deletions on critical sentences, matching games where pairs are obvious, and predict-the-output for code blocks with deterministic stdout. Print fidelity is preserved by the `@media print` rules — interactive features collapse cleanly to a static PDF.

### Rule 7: Dark Mode
Both `study_notes.html` and `practice_exam.html` must include a dark mode toggle button. The toggle is a fixed-position button in the top-right corner. It switches CSS custom properties to a dark palette and persists the user's choice in `localStorage` (key: `study-dark-mode`). All interactive component styles must have matching `body.dark` overrides. When printing, dark mode is forced off so the PDF is always light.

### Rule 8: Interactive Practice Exam
When `--practice-exam` is used, the generated `practice_exam.html` must include:
- **Clickable MCQ options** — each `<div class="question">` has a `data-answer="x"` attribute. When the student clicks an option, it is marked correct/incorrect, the right answer is highlighted, and a feedback explanation appears.
- **Score tracker** — a fixed widget showing `N / M correct (total Q)` that updates live.
- **Gated answer key** — the answer key is hidden behind a "Show Answer Key" gate button so students are not tempted to peek.
- **Part B reveal-answer cards** — each model answer subsection is wrapped in a `.reveal-answer` card so students can attempt the exercise before revealing the solution.
- **Reading progress bar** at the top.

---

## CSS Template

Use this exact CSS as the `<style>` block in every generated HTML file. You may add additional styles but never remove or override existing rules.

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

:root {
  --primary: #1a1a2e;
  --accent: #0f3460;
  --highlight: #e94560;
  --gold: #f5a623;
  --green: #27ae60;
  --blue: #2980b9;
  --light-bg: #f8f9fa;
  --border: #dee2e6;
  --text: #212529;
  --muted: #6c757d;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.65;
  color: var(--text);
  background: white;
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 50px;
}

/* --- COVER PAGE --- */
.cover {
  text-align: center;
  padding: 80px 20px 60px;
  border-bottom: 4px solid var(--highlight);
  margin-bottom: 50px;
}
.cover .course-code {
  font-size: 13pt;
  font-weight: 600;
  letter-spacing: 3px;
  color: var(--muted);
  text-transform: uppercase;
  margin-bottom: 12px;
}
.cover h1 {
  font-size: 30pt;
  font-weight: 700;
  color: var(--primary);
  line-height: 1.2;
  margin-bottom: 18px;
}
.cover .subtitle {
  font-size: 13pt;
  color: var(--accent);
  margin-bottom: 30px;
}
.cover .meta-box {
  display: inline-block;
  background: var(--primary);
  color: white;
  border-radius: 8px;
  padding: 18px 36px;
  margin-top: 20px;
  text-align: left;
}
.cover .meta-box p { font-size: 10pt; margin: 4px 0; }
.cover .meta-box strong { color: var(--gold); }

/* --- TABLE OF CONTENTS --- */
.toc {
  background: var(--light-bg);
  border-left: 5px solid var(--accent);
  border-radius: 6px;
  padding: 24px 30px;
  margin-bottom: 48px;
  page-break-after: always;
}
.toc h2 { font-size: 14pt; color: var(--primary); margin-bottom: 16px; }
.toc ol { padding-left: 22px; }
.toc li { margin: 5px 0; font-size: 10.5pt; }
.toc li a { color: var(--accent); text-decoration: none; }
.toc .toc-sub { padding-left: 18px; margin-top: 3px; }
.toc .toc-sub li { font-size: 10pt; color: var(--muted); }

/* --- EXAM INTELLIGENCE --- */
.exam-intel {
  background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
  color: white;
  border-radius: 10px;
  padding: 28px 32px;
  margin-bottom: 48px;
}
.exam-intel h2 { font-size: 14pt; color: var(--gold); margin-bottom: 14px; }
.exam-intel p, .exam-intel li { font-size: 10.5pt; margin: 5px 0; }
.exam-intel ul { padding-left: 20px; }
.exam-intel .tag {
  display: inline-block;
  background: var(--highlight);
  color: white;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 9pt;
  font-weight: 600;
  margin-right: 8px;
}

/* --- SECTION HEADINGS --- */
h1.section-title {
  font-size: 20pt;
  font-weight: 700;
  color: white;
  background: var(--primary);
  padding: 14px 22px;
  border-radius: 8px;
  margin: 50px 0 24px;
  page-break-before: always;
}
h1.section-title span { color: var(--gold); }

h2.topic {
  font-size: 15pt;
  font-weight: 700;
  color: var(--accent);
  border-bottom: 2.5px solid var(--accent);
  padding-bottom: 6px;
  margin: 34px 0 16px;
}

h3.subtopic {
  font-size: 12pt;
  font-weight: 600;
  color: var(--highlight);
  margin: 24px 0 10px;
}

h4.subsubtopic {
  font-size: 11pt;
  font-weight: 600;
  color: var(--primary);
  margin: 16px 0 8px;
}

/* --- CONTENT ELEMENTS --- */
p { margin-bottom: 10px; }

ul, ol {
  padding-left: 22px;
  margin-bottom: 12px;
}
li { margin: 4px 0; }
li > ul { margin-top: 4px; }

/* --- BLOCKQUOTES --- */
blockquote {
  background: #fff8e7;
  border-left: 5px solid var(--gold);
  border-radius: 0 6px 6px 0;
  padding: 14px 18px;
  margin: 14px 0;
  font-style: normal;
}
blockquote strong { color: var(--primary); }
blockquote.key {
  background: #e8f4fd;
  border-left-color: var(--blue);
}
blockquote.warning {
  background: #fdecea;
  border-left-color: var(--highlight);
}

/* --- TABLES --- */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 10pt;
  page-break-inside: avoid;
}
th {
  background: var(--accent);
  color: white;
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
}
td {
  padding: 7px 12px;
  border: 1px solid var(--border);
}
tr:nth-child(even) td { background: #f8f9fa; }

.compare-table th:first-child { background: var(--primary); }
.compare-table td:first-child { font-weight: 600; background: #f0f4f8; color: var(--primary); }

/* --- CALLOUT BOXES --- */
.callout {
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 14px 18px;
  margin: 16px 0;
  page-break-inside: avoid;
}
.callout.tip { border-color: var(--green); background: #f0fdf4; }
.callout.tip::before { content: "TIP  "; font-weight: 700; color: var(--green); }
.callout.exam { border-color: var(--highlight); background: #fff0f0; }
.callout.exam::before { content: "EXAM NOTE  "; font-weight: 700; color: var(--highlight); }
.callout.example { border-color: var(--blue); background: #f0f8ff; }
.callout.example::before { content: "EXAMPLE  "; font-weight: 700; color: var(--blue); }

/* --- CODE BLOCKS --- */
pre {
  background: #1e1e2e;
  color: #cdd6f4;
  border-radius: 8px;
  padding: 16px 20px;
  overflow-x: auto;
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 9.5pt;
  line-height: 1.5;
  margin: 14px 0;
  page-break-inside: avoid;
}
code {
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 9.5pt;
}
p code, li code {
  background: #f0f0f5;
  padding: 1px 5px;
  border-radius: 3px;
  color: var(--highlight);
}

/* --- IMAGES --- */
.img-block {
  text-align: center;
  margin: 20px 0;
  page-break-inside: avoid;
}
.img-block img {
  max-width: 100%;
  max-height: 380px;
  border: 1px solid var(--border);
  border-radius: 6px;
  object-fit: contain;
}
.img-block .caption {
  font-size: 9pt;
  color: var(--muted);
  margin-top: 6px;
  font-style: italic;
}

.img-row {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin: 20px 0;
  page-break-inside: avoid;
}
.img-row .img-block { flex: 1; }
.img-row .img-block img { max-height: 260px; }

/* --- TWO-COLUMN LAYOUT --- */
.two-col {
  display: flex;
  gap: 20px;
  margin: 14px 0;
}
.two-col > div { flex: 1; }

/* --- QUICK REFERENCE --- */
.quick-ref {
  background: var(--primary);
  color: white;
  border-radius: 8px;
  padding: 22px 28px;
  margin: 30px 0;
  page-break-inside: avoid;
}
.quick-ref h3 { color: var(--gold); margin-bottom: 12px; font-size: 12pt; }
.quick-ref li { font-size: 10pt; margin: 4px 0; }

/* --- PAGE BREAK --- */
.page-break { page-break-after: always; }

/* --- PRINT / PDF --- */
@media print {
  body { padding: 0; max-width: none; }
  .cover { page-break-after: always; }
  h1.section-title { page-break-before: always; }
}

@page {
  size: A4;
  margin: 22mm 18mm;
}

/* =====================================================================
   INTERACTIVE FEATURES — required by Rule 6 / Step 4.4
   ===================================================================== */

/* Reading progress bar */
.reading-progress {
  position: fixed; top: 0; left: 0; height: 4px; width: 0%;
  background: linear-gradient(90deg, var(--highlight), var(--gold));
  z-index: 9999; transition: width 0.1s ease-out;
}

/* Sticky sidebar TOC with scroll-spy */
.sidebar-toc {
  position: fixed; top: 60px; left: 16px;
  width: 240px; max-height: calc(100vh - 100px);
  overflow-y: auto; padding: 16px 14px;
  background: white; border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 6px;
  font-size: 9.5pt; z-index: 100;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}
.sidebar-toc h4 {
  font-size: 9pt; text-transform: uppercase; letter-spacing: 1.5px;
  color: var(--muted); margin-bottom: 10px; font-weight: 700;
}
.sidebar-toc ol { list-style: none; padding-left: 0; margin: 0; }
.sidebar-toc li { margin: 4px 0; line-height: 1.3; }
.sidebar-toc a {
  color: var(--text); text-decoration: none; display: block;
  padding: 4px 8px; border-radius: 4px; border-left: 2px solid transparent;
  transition: all 0.15s;
}
.sidebar-toc a:hover { background: var(--light-bg); }
.sidebar-toc a.active {
  background: #fff0f0; color: var(--highlight); font-weight: 600;
  border-left-color: var(--highlight);
}
@media (max-width: 1380px) { .sidebar-toc { display: none; } }

/* Click-to-reveal definition cards */
.reveal {
  border: 1.5px dashed var(--accent);
  background: linear-gradient(135deg, #f8f9ff 0%, #eef2ff 100%);
  border-radius: 8px;
  padding: 14px 18px;
  margin: 14px 0;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}
.reveal:hover { box-shadow: 0 2px 10px rgba(15,52,96,0.12); border-color: var(--highlight); }
.reveal-prompt {
  font-weight: 700; color: var(--primary);
  display: flex; align-items: center; gap: 10px;
}
.reveal-prompt::before {
  content: "?"; display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--highlight); color: white;
  font-size: 11pt; font-weight: 700;
}
.reveal-hint {
  font-size: 9pt; color: var(--muted); font-style: italic;
  margin-top: 6px; display: block;
}
.reveal-body { display: none; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); }
.reveal.revealed { background: #fff8e7; border-style: solid; border-color: var(--gold); cursor: default; }
.reveal.revealed .reveal-prompt::before { content: "\2713"; background: var(--green); }
.reveal.revealed .reveal-hint { display: none; }
.reveal.revealed .reveal-body { display: block; }

/* Hide-the-diagram overlay */
.img-block { position: relative; }
.img-block.hideable img { filter: blur(14px); transition: filter 0.4s; }
.img-block.hideable .img-overlay {
  position: absolute; inset: 0; display: flex; align-items: center;
  justify-content: center; flex-direction: column; gap: 8px;
  background: rgba(255,255,255,0.85); border-radius: 6px;
  cursor: pointer; text-align: center; padding: 16px;
}
.img-block.hideable .img-overlay-title {
  font-weight: 700; color: var(--primary); font-size: 11pt;
}
.img-block.hideable .img-overlay-hint {
  font-size: 9pt; color: var(--muted); font-style: italic;
}
.img-block.revealed img { filter: none; }
.img-block.revealed .img-overlay { display: none; }

/* Cloze deletions */
.cloze {
  display: inline-block;
  background: var(--primary); color: var(--primary);
  padding: 1px 10px; border-radius: 4px;
  cursor: pointer; user-select: none;
  font-weight: 600; min-width: 60px; text-align: center;
  transition: all 0.2s;
}
.cloze:hover { background: var(--accent); color: var(--gold); }
.cloze.revealed { background: #fff8e7; color: var(--highlight); border: 1px solid var(--gold); padding: 0 9px; }

/* Inline MCQs */
.quiz {
  background: linear-gradient(135deg, #fff5f7 0%, #ffeef2 100%);
  border: 2px solid var(--highlight);
  border-radius: 10px;
  padding: 22px 26px;
  margin: 32px 0;
  page-break-inside: avoid;
}
.quiz-header {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 16px;
}
.quiz-header::before {
  content: "QUICK CHECK";
  background: var(--highlight); color: white;
  padding: 4px 10px; border-radius: 4px;
  font-size: 8.5pt; font-weight: 700; letter-spacing: 1px;
}
.quiz-header h4 {
  font-size: 11pt; color: var(--primary); margin: 0;
}
.quiz-q { margin: 14px 0; padding: 12px 0; border-top: 1px solid #ffd5dc; }
.quiz-q:first-of-type { border-top: none; padding-top: 0; }
.quiz-q .q-text { font-weight: 600; color: var(--primary); margin-bottom: 8px; font-size: 10.5pt; }
.quiz-opts { list-style: none; padding: 0; margin: 0; }
.quiz-opt {
  background: white; border: 1.5px solid var(--border);
  border-radius: 6px; padding: 8px 14px; margin: 6px 0;
  cursor: pointer; font-size: 10pt;
  transition: all 0.15s;
  display: flex; align-items: flex-start; gap: 10px;
}
.quiz-opt::before {
  content: attr(data-letter);
  display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--light-bg); border: 1px solid var(--border);
  font-weight: 700; color: var(--muted); font-size: 9pt;
  flex-shrink: 0;
}
.quiz-opt:hover:not(.locked) { border-color: var(--accent); background: #f8f9ff; }
.quiz-opt.correct { border-color: var(--green); background: #f0fdf4; color: var(--primary); }
.quiz-opt.correct::before { background: var(--green); color: white; border-color: var(--green); }
.quiz-opt.incorrect { border-color: var(--highlight); background: #fdecea; color: var(--primary); }
.quiz-opt.incorrect::before { background: var(--highlight); color: white; border-color: var(--highlight); }
.quiz-opt.locked { cursor: default; }
.quiz-feedback {
  display: none; margin-top: 10px; padding: 10px 14px;
  background: white; border-radius: 6px; border-left: 4px solid var(--green);
  font-size: 9.5pt; color: var(--text);
}
.quiz-feedback.show { display: block; }
.quiz-feedback.wrong { border-left-color: var(--highlight); }
.quiz-feedback strong { color: var(--primary); }

/* Flip cards (catalogues like design patterns) */
.flipcard-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px; margin: 24px 0; page-break-inside: avoid;
}
.flipcard { perspective: 1000px; height: 240px; cursor: pointer; }
.flipcard-inner {
  position: relative; width: 100%; height: 100%;
  transition: transform 0.6s; transform-style: preserve-3d;
}
.flipcard.flipped .flipcard-inner { transform: rotateY(180deg); }
.flipcard-front, .flipcard-back {
  position: absolute; inset: 0;
  backface-visibility: hidden;
  border-radius: 10px; padding: 18px;
  display: flex; flex-direction: column;
  box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}
.flipcard-front {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
  color: white;
  align-items: center; justify-content: center; text-align: center;
}
.flipcard-front .pattern-name { font-size: 14pt; font-weight: 700; color: var(--gold); margin-bottom: 12px; }
.flipcard-front .pattern-cat { font-size: 8pt; text-transform: uppercase; letter-spacing: 2px; color: white; opacity: 0.7; margin-bottom: 14px; }
.flipcard-front .pattern-problem { font-size: 10pt; font-style: italic; line-height: 1.4; }
.flipcard-front .flip-hint { position: absolute; bottom: 10px; right: 14px; font-size: 8pt; opacity: 0.6; }
.flipcard-back {
  background: white;
  border: 2px solid var(--gold);
  transform: rotateY(180deg);
  font-size: 9pt;
  overflow-y: auto;
}
.flipcard-back .back-section { margin-bottom: 8px; }
.flipcard-back .back-label {
  font-weight: 700; color: var(--highlight);
  font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.5px;
}
.flipcard-back p { margin: 2px 0 6px; font-size: 9pt; line-height: 1.4; }

/* Matching game */
.match-game {
  background: #f0f8ff;
  border: 2px solid var(--blue);
  border-radius: 10px;
  padding: 22px 26px;
  margin: 30px 0;
  page-break-inside: avoid;
}
.match-game::before {
  content: "MATCH THE PAIRS";
  display: inline-block;
  background: var(--blue); color: white;
  padding: 4px 12px; border-radius: 4px;
  font-size: 8.5pt; font-weight: 700; letter-spacing: 1px;
  margin-bottom: 8px;
}
.match-game h4 { font-size: 11pt; color: var(--primary); margin: 8px 0 16px; }
.match-game .match-instruct { font-size: 9pt; color: var(--muted); font-style: italic; margin-bottom: 14px; }
.match-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.match-col { display: flex; flex-direction: column; gap: 8px; }
.match-tile {
  background: white; border: 1.5px solid var(--border);
  border-radius: 6px; padding: 9px 14px;
  cursor: pointer; font-size: 9.5pt;
  transition: all 0.15s; min-height: 38px;
  display: flex; align-items: center;
}
.match-tile:hover:not(.matched) { border-color: var(--blue); background: #f0f8ff; }
.match-tile.selected { border-color: var(--accent); background: #e8f4fd; box-shadow: 0 0 0 2px var(--accent); }
.match-tile.matched { background: #f0fdf4; border-color: var(--green); color: var(--primary); cursor: default; }
.match-tile.matched::after { content: " \2713"; color: var(--green); font-weight: 700; margin-left: auto; }
.match-tile.wrong { background: #fdecea; border-color: var(--highlight); animation: shake 0.4s; }
@keyframes shake {
  0%,100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
.match-status { margin-top: 12px; font-size: 9.5pt; color: var(--muted); text-align: center; }
.match-status.complete { color: var(--green); font-weight: 700; }

/* Predict-the-output */
.predict {
  background: #fffbf0;
  border: 2px dashed var(--gold);
  border-radius: 10px;
  padding: 18px 22px;
  margin: 22px 0;
  page-break-inside: avoid;
}
.predict::before {
  content: "PREDICT THE OUTPUT";
  display: inline-block;
  background: var(--gold); color: var(--primary);
  padding: 4px 12px; border-radius: 4px;
  font-size: 8.5pt; font-weight: 700; letter-spacing: 1px;
  margin-bottom: 10px;
}
.predict .predict-prompt { font-size: 10pt; margin-bottom: 10px; color: var(--text); }
.predict .predict-output {
  display: none;
  background: #1e1e2e; color: #cdd6f4;
  padding: 12px 16px; border-radius: 6px;
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 9.5pt; line-height: 1.5;
  margin-top: 12px;
  white-space: pre-wrap;
}
.predict .predict-output.show { display: block; }
.predict .predict-btn {
  background: var(--gold); color: var(--primary);
  border: none; padding: 8px 18px; border-radius: 6px;
  font-weight: 700; font-size: 9.5pt; cursor: pointer;
  font-family: inherit;
}
.predict .predict-btn:hover { background: #e69015; }
.predict .predict-btn.hidden { display: none; }

/* Print: hide all interactive scaffolding, show all answers */
@media print {
  .reading-progress, .sidebar-toc, .img-overlay { display: none !important; }
  .reveal { background: white; border-style: solid; cursor: default; }
  .reveal-prompt::before { display: none; }
  .reveal-hint { display: none; }
  .reveal-body { display: block !important; margin-top: 0; padding-top: 0; border-top: none; }
  .img-block.hideable img { filter: none !important; }
  .cloze { background: white !important; color: var(--highlight) !important; border-bottom: 1.5px solid var(--highlight); padding: 0 4px; }
  .quiz-opt.correct { background: #f0fdf4 !important; }
  .quiz-feedback { display: block !important; }
  .flipcard { height: auto; perspective: none; }
  .flipcard-inner { transform: none !important; transition: none; }
  .flipcard-front, .flipcard-back {
    position: static; backface-visibility: visible;
    transform: none !important; margin-bottom: 8px;
  }
  .flipcard-back { display: block; }
  .match-tile { background: white !important; }
  .predict .predict-output { display: block !important; }
  .predict .predict-btn { display: none; }
}

/* =====================================================================
   DARK MODE
   ===================================================================== */
.dark-toggle {
  position: fixed; top: 14px; right: 20px;
  z-index: 10000;
  background: var(--primary); color: white;
  border: 2px solid var(--border);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 9pt; font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.25s;
  display: flex; align-items: center; gap: 6px;
}
.dark-toggle:hover { background: var(--accent); border-color: var(--gold); }
.dark-toggle .icon { font-size: 13pt; line-height: 1; }

body.dark {
  --primary: #e8e8f0; --accent: #7bb3e0; --highlight: #ff6b81; --gold: #f5c542;
  --green: #5ddb8d; --blue: #5ea8db; --light-bg: #1e1e2e; --border: #3a3a50;
  --text: #d4d4e0; --muted: #8888a0;
  background: #121220; color: var(--text);
}
body.dark .cover { border-bottom-color: var(--highlight); }
body.dark .cover h1 { color: #f0f0ff; }
body.dark .cover .meta-box { background: #1e1e2e; border: 1px solid var(--border); }
body.dark .exam-intel { background: linear-gradient(135deg, #1a1a30 0%, #1e2e4a 100%); }
body.dark .toc { background: #1a1a28; border-left-color: var(--accent); }
body.dark h1.section-title { background: #1e1e30; color: #f0f0ff; }
body.dark h2.topic { color: var(--accent); border-bottom-color: var(--accent); }
body.dark h3.subtopic { color: var(--highlight); }
body.dark h4.subsubtopic { color: #d0d0e0; }
body.dark blockquote { background: #1e1e2e; border-left-color: var(--gold); }
body.dark blockquote.key { background: #1a2438; border-left-color: var(--blue); }
body.dark blockquote.warning { background: #2a1a1a; border-left-color: var(--highlight); }
body.dark table th { background: #1e2e4a; }
body.dark table td { border-color: var(--border); }
body.dark tr:nth-child(even) td { background: #1a1a28; }
body.dark .compare-table th:first-child { background: #1a1a30; }
body.dark .compare-table td:first-child { background: #1a1a28; color: var(--accent); }
body.dark .callout { border-color: var(--border); }
body.dark .callout.tip { border-color: var(--green); background: #1a2a1e; }
body.dark .callout.exam { border-color: var(--highlight); background: #2a1a1e; }
body.dark .callout.example { border-color: var(--blue); background: #1a2030; }
body.dark pre { background: #0e0e1a; }
body.dark p code, body.dark li code { background: #1e1e2e; color: var(--highlight); }
body.dark .img-block img { border-color: var(--border); }
body.dark .quick-ref { background: #1a1a30; }
body.dark .sidebar-toc { background: #181828; border-color: var(--border); box-shadow: 0 4px 14px rgba(0,0,0,0.3); }
body.dark .sidebar-toc a { color: var(--text); }
body.dark .sidebar-toc a.active { background: #2a1a28; color: var(--highlight); }
body.dark .dark-toggle { background: #2a2a3e; border-color: var(--border); }
body.dark .dark-toggle:hover { background: var(--accent); color: #121220; }
body.dark .reveal { background: linear-gradient(135deg, #1a1a30 0%, #1e1e38 100%); border-color: var(--accent); }
body.dark .reveal.revealed { background: #1e1e28; border-color: var(--gold); }
body.dark .reveal-body { border-top-color: var(--border); }
body.dark .quiz { background: linear-gradient(135deg, #2a1a28 0%, #281a22 100%); border-color: var(--highlight); }
body.dark .quiz-q { border-top-color: #3a2a30; }
body.dark .quiz-opt { background: #1a1a28; border-color: var(--border); color: var(--text); }
body.dark .quiz-opt:hover:not(.locked) { background: #1e1e38; border-color: var(--accent); }
body.dark .quiz-opt.correct { background: #1a2a1e; border-color: var(--green); }
body.dark .quiz-opt.incorrect { background: #2a1a1e; border-color: var(--highlight); }
body.dark .quiz-feedback { background: #1a1a28; color: var(--text); }
body.dark .flipcard-front { background: linear-gradient(135deg, #1a1a30 0%, #1e2e4a 100%); }
body.dark .flipcard-back { background: #1a1a28; border-color: var(--gold); color: var(--text); }
body.dark .match-game { background: #1a2030; border-color: var(--blue); }
body.dark .match-tile { background: #1a1a28; border-color: var(--border); color: var(--text); }
body.dark .match-tile:hover:not(.matched) { background: #1e2030; border-color: var(--blue); }
body.dark .match-tile.selected { background: #1a2438; border-color: var(--accent); }
body.dark .match-tile.matched { background: #1a2a1e; border-color: var(--green); }
body.dark .predict { background: #1e1e22; border-color: var(--gold); }
body.dark .img-block.hideable .img-overlay { background: rgba(18,18,32,0.9); }
body.dark .img-block.hideable .img-overlay-title { color: #f0f0ff; }
body.dark .cloze { background: #3a3a50; color: #3a3a50; }
body.dark .cloze:hover { background: var(--accent); color: var(--gold); }
body.dark .cloze.revealed { background: #1e1e28; color: var(--highlight); border-color: var(--gold); }
body.dark .answer-key { background: #1a2a1e; border-color: var(--green); }
body.dark .scenario-box { background: #1a1a28; border-color: var(--accent); }
body.dark .instructions-box { background: #2a1a1e; border-color: var(--highlight); }

@media print {
  body.dark { background: white !important; color: #212529 !important; }
  .dark-toggle { display: none !important; }
}
```

---

## JavaScript Block

Insert this `<script>` block immediately before `</body>` in every generated `study_notes.html` and `practice_exam.html`. It powers all interactive features defined above. Do not modify it. Do not split it. Do not load anything from a CDN.

```html
<script>
(function(){
  // ---------- Reading progress bar ----------
  var pb = document.querySelector('.reading-progress');
  if (pb) {
    window.addEventListener('scroll', function(){
      var h = document.documentElement;
      var scrolled = h.scrollTop / (h.scrollHeight - h.clientHeight);
      pb.style.width = Math.max(0, Math.min(100, scrolled * 100)) + '%';
    }, { passive: true });
  }

  // ---------- Sidebar TOC scroll-spy ----------
  var sidebarLinks = document.querySelectorAll('.sidebar-toc a[href^="#"]');
  if (sidebarLinks.length && 'IntersectionObserver' in window) {
    var linkMap = {};
    sidebarLinks.forEach(function(a){
      var id = a.getAttribute('href').slice(1);
      linkMap[id] = a;
    });
    var observer = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        var id = entry.target.id;
        if (!linkMap[id]) return;
        if (entry.isIntersecting) {
          sidebarLinks.forEach(function(l){ l.classList.remove('active'); });
          linkMap[id].classList.add('active');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(linkMap).forEach(function(id){
      var el = document.getElementById(id);
      if (el) observer.observe(el);
    });
  }

  // ---------- Click-to-reveal cards ----------
  document.querySelectorAll('.reveal').forEach(function(card){
    card.addEventListener('click', function(e){
      if (card.classList.contains('revealed')) return;
      card.classList.add('revealed');
    });
  });

  // ---------- Hide-the-diagram ----------
  document.querySelectorAll('.img-block.hideable .img-overlay').forEach(function(ov){
    ov.addEventListener('click', function(e){
      e.stopPropagation();
      ov.parentElement.classList.add('revealed');
    });
  });

  // ---------- Cloze deletions ----------
  document.querySelectorAll('.cloze').forEach(function(c){
    c.addEventListener('click', function(){
      c.classList.toggle('revealed');
    });
  });

  // ---------- Inline MCQs ----------
  document.querySelectorAll('.quiz-q').forEach(function(q){
    var opts = q.querySelectorAll('.quiz-opt');
    var feedback = q.querySelector('.quiz-feedback');
    opts.forEach(function(opt){
      opt.addEventListener('click', function(){
        if (q.dataset.answered === '1') return;
        q.dataset.answered = '1';
        var isCorrect = opt.dataset.correct === '1';
        opt.classList.add(isCorrect ? 'correct' : 'incorrect');
        opts.forEach(function(o){
          o.classList.add('locked');
          if (o.dataset.correct === '1' && o !== opt) {
            o.classList.add('correct');
          }
        });
        if (feedback) {
          feedback.classList.add('show');
          if (!isCorrect) feedback.classList.add('wrong');
        }
      });
    });
  });

  // ---------- Flip cards ----------
  document.querySelectorAll('.flipcard').forEach(function(card){
    card.addEventListener('click', function(){
      card.classList.toggle('flipped');
    });
  });

  // ---------- Matching game ----------
  document.querySelectorAll('.match-game').forEach(function(game){
    var tiles = game.querySelectorAll('.match-tile');
    var status = game.querySelector('.match-status');
    var total = tiles.length / 2;
    var matched = 0;
    var selected = null;
    tiles.forEach(function(tile){
      tile.addEventListener('click', function(){
        if (tile.classList.contains('matched')) return;
        if (!selected) {
          selected = tile;
          tile.classList.add('selected');
          return;
        }
        if (selected === tile) {
          tile.classList.remove('selected');
          selected = null;
          return;
        }
        if (selected.dataset.pair === tile.dataset.pair && selected.dataset.side !== tile.dataset.side) {
          selected.classList.remove('selected');
          selected.classList.add('matched');
          tile.classList.add('matched');
          matched++;
          if (status) {
            status.textContent = matched + ' / ' + total + ' matched';
            if (matched === total) {
              status.textContent = 'All ' + total + ' pairs matched! \u2713';
              status.classList.add('complete');
            }
          }
          selected = null;
        } else {
          var prev = selected;
          tile.classList.add('wrong');
          prev.classList.add('wrong');
          setTimeout(function(){
            tile.classList.remove('wrong');
            prev.classList.remove('wrong', 'selected');
          }, 500);
          selected = null;
        }
      });
    });
    if (status) status.textContent = '0 / ' + total + ' matched';
  });

  // ---------- Predict the output ----------
  document.querySelectorAll('.predict').forEach(function(p){
    var btn = p.querySelector('.predict-btn');
    var out = p.querySelector('.predict-output');
    if (btn && out) {
      btn.addEventListener('click', function(){
        out.classList.add('show');
        btn.classList.add('hidden');
      });
    }
  });
})();
</script>
```

### Dark Mode Toggle Script

Insert this as a **second** `<script>` block immediately after the main one, before `</body>`. It is used in **both** `study_notes.html` and `practice_exam.html`.

```html
<script>
(function(){
  var btn = document.getElementById('darkToggle');
  var icon = document.getElementById('darkIcon');
  var label = document.getElementById('darkLabel');
  function setDark(on) {
    document.body.classList.toggle('dark', on);
    if (icon) icon.innerHTML = on ? '&#9788;' : '&#9789;';
    if (label) label.textContent = on ? 'Light' : 'Dark';
    try { localStorage.setItem('study-dark-mode', on ? '1' : '0'); } catch(e){}
  }
  try {
    var saved = localStorage.getItem('study-dark-mode');
    if (saved === '1') setDark(true);
  } catch(e){}
  if (btn) btn.addEventListener('click', function(){
    setDark(!document.body.classList.contains('dark'));
  });
})();
</script>
```

Also insert this toggle button HTML immediately after the sidebar TOC `</nav>` (study notes) or right after `<body>` (practice exam):

```html
<button class="dark-toggle" id="darkToggle" type="button" aria-label="Toggle dark mode">
  <span class="icon" id="darkIcon">&#9789;</span>
  <span id="darkLabel">Dark</span>
</button>
```

### Practice Exam Interactive Script

Insert this as an **additional** `<script>` block in `practice_exam.html` only, before the dark mode script and before `</body>`. It powers clickable MCQ options, score tracking, the answer key gate, and Part B reveal-answer cards.

```html
<script>
(function(){
  // Reading progress bar
  var pb = document.querySelector('.reading-progress');
  if (pb) {
    window.addEventListener('scroll', function(){
      var h = document.documentElement;
      var scrolled = h.scrollTop / (h.scrollHeight - h.clientHeight);
      pb.style.width = Math.max(0, Math.min(100, scrolled * 100)) + '%';
    }, { passive: true });
  }

  // MCQ interactivity
  var totalQ = 0, answered = 0, correct = 0;
  var scoreEl = document.querySelector('.score-tracker');
  function updateScore() {
    if (scoreEl) scoreEl.textContent = correct + ' / ' + answered + ' correct (' + totalQ + ' total)';
  }
  document.querySelectorAll('.question[data-answer]').forEach(function(q){
    totalQ++;
    var opts = q.querySelector('.options');
    if (!opts) return;
    opts.classList.add('interactive');
    var items = opts.querySelectorAll('li');
    var correctLetter = q.dataset.answer;
    var feedbackEl = q.querySelector('.mcq-feedback');
    items.forEach(function(li){
      li.addEventListener('click', function(){
        if (q.dataset.done === '1') return;
        q.dataset.done = '1';
        answered++;
        var match = li.textContent.trim().match(/^\(([a-d])\)/);
        var chosen = match ? match[1] : '';
        var isCorrect = chosen === correctLetter;
        if (isCorrect) correct++;
        li.classList.add(isCorrect ? 'correct' : 'incorrect');
        if (!isCorrect) {
          items.forEach(function(o){
            var om = o.textContent.trim().match(/^\(([a-d])\)/);
            if (om && om[1] === correctLetter) o.classList.add('correct');
          });
        }
        items.forEach(function(o){ o.classList.add('locked'); });
        if (feedbackEl) {
          feedbackEl.classList.add('show');
          if (!isCorrect) feedbackEl.classList.add('wrong');
        }
        updateScore();
      });
    });
  });
  updateScore();

  // Answer key gate
  document.querySelectorAll('.answer-section-gate .gate-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var gate = btn.closest('.answer-section-gate');
      var hidden = gate.nextElementSibling;
      if (hidden && hidden.classList.contains('answer-section-hidden')) {
        hidden.classList.add('visible');
        gate.style.display = 'none';
      }
    });
  });

  // Part B reveal-answer cards
  document.querySelectorAll('.reveal-answer').forEach(function(r){
    r.addEventListener('click', function(){
      if (r.classList.contains('shown')) return;
      r.classList.add('shown');
    });
  });
})();
</script>
```
