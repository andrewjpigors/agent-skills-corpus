---
name: lecture-review
description: >-
  Use when the user invokes /lecture-review to review lecture material and create cheat sheets.
  Supports three modes: review (default), condense <pages>, and status.
  Reads PDF lectures from the course Lectures/ folder, explains concepts via teach-back,
  and generates LaTeX/PDF cheat sheets.
---

# Lecture Review & Cheat Sheet Generator

## Overview

Help the user review lecture material and generate exam-ready cheat sheets.
Three modes: **review** (teach-back + per-lecture cheat sheet), **condense** (combine into N pages),
and **status** (show progress).

## Setup

This skill expects the following directory structure in the user's working directory:

```
<course-dir>/                  # The directory where the user runs Claude Code
├── Lectures/                  # PDF lecture files go here
│   ├── lecture01.pdf
│   ├── lecture02.pdf
│   └── ...
├── cheatsheets/               # Generated cheat sheets (auto-created)
│   ├── per-lecture/
│   └── final/
├── teach-back/                # Generated HTML teach-backs (auto-created)
└── .lecture-review-state.json # Progress tracking (auto-created)
```

**COURSE_DIR** is the current working directory (use `.` or the absolute path from the environment).

## Mode Detection

Parse the argument passed to the skill:
- No argument or a lecture filename → **Review Mode**
- Starts with `condense` followed by a number → **Condense Mode** (extract the page count)
- `status` → **Status Mode**

If the argument is ambiguous, ask the user what they meant.

---

## Status Mode

1. Read the state file at `COURSE_DIR/.lecture-review-state.json`
   - If it doesn't exist or is malformed, treat all lectures as unreviewed
2. List all PDFs in `COURSE_DIR/Lectures/` using the Glob tool with pattern `*.pdf`
3. Present a table:

| Lecture | Reviewed | Cheat Sheet |
|---------|----------|-------------|
| lecture01.pdf | Yes | cheatsheets/per-lecture/lecture01-cheatsheet.pdf |
| lecture02.pdf | No | — |

4. If a final condensed sheet exists in `cheatsheets/final/`, mention it at the bottom.

---

## Review Mode

### Step 1: Lecture Selection

1. Read the state file at `COURSE_DIR/.lecture-review-state.json`
   - If missing or malformed JSON, start fresh: `{"reviewed": [], "cheatsheets": {}, "preferences": {}}`
2. List all PDFs in `COURSE_DIR/Lectures/` using Glob with `*.pdf`
3. If a specific lecture was passed as argument, use that one
4. Otherwise, present the list of **unreviewed** lectures (those whose filenames are NOT in the `reviewed` array) and ask:
   > "Which lecture would you like to review?"
5. If all lectures are already reviewed, say so and ask if the user wants to re-review one.

### Step 2: Teach-Back (HTML-First)

#### 2a: Read the PDF

1. Read the selected PDF using **parallel dual-reader subagents** for speed and accuracy.
   - First, determine the total page count of the PDF using Bash: `pdfinfo <file> | grep Pages`. If `pdfinfo` is not available, fall back to `python3 -c "import fitz; print(fitz.open('<file>').page_count)"` or simply try reading the first 20 pages and check if more exist.
   - If the PDF is **20 pages or fewer**, read it directly with the Read tool (no subagent needed).
   - If the PDF is **over 20 pages**, split it into 20-page chunks. For **each chunk**, launch **two independent subagents** in parallel (all subagents for all chunks in a single message):
     - Each subagent should use `subagent_type: "general-purpose"` with `model: "haiku"`.
     - Each subagent's prompt should instruct it to: read the specific page range of the PDF using the Read tool's `pages` parameter, then return a **detailed, structured extraction** of the content. The prompt must emphasize:
       - List **every** key concept, definition, theorem, and formula — do not summarize or skip anything
       - Reproduce formulas and equations **exactly** as they appear (variable names, subscripts, etc.)
       - Note any diagrams/figures and describe what they show
       - Include page numbers for each item so discrepancies can be traced back
     - Label them clearly: e.g., "Reader A pages 1-20", "Reader B pages 1-20", "Reader A pages 21-40", etc.
     - Example: for a 55-page PDF, launch **6** subagents: Reader A pages 1-20, Reader B pages 1-20, Reader A pages 21-40, Reader B pages 21-40, Reader A pages 41-55, Reader B pages 41-55.
   - **Consensus & conflict resolution:** After all subagents return, for each chunk:
     - **Agreements:** Where both readers report the same concept/formula/detail, accept it as reliable.
     - **Unique items:** If one reader extracted something the other missed, include it (it's likely real content that one reader overlooked, not a hallucination).
     - **Conflicts:** If the two readers disagree on a formula, definition, or claim (e.g., different variable names, contradictory statements), **re-read those specific pages yourself** using the Read tool to resolve the discrepancy. Do not guess — go back to the source.
   - Combine the verified, de-duplicated content in page order to form your complete understanding of the lecture.

#### 2b: Generate the HTML Teach-Back (Parallel Section Generation)

**Do NOT output the teach-back as text to the console.** Generate the full teach-back directly as an HTML file.

**Why parallel generation:** For large lectures, the combined extracted content + full HTML output can exceed context limits. To solve this, generate each HTML section independently via parallel subagents, then assemble the final file.

##### Phase 1: Create a Learning Plan

This is a two-step process: first create the plan, then review it as a learner.

**Step 1 — Draft the learning plan.** Review the extracted content from step 2a and create a **learning plan** — a list of 4-8 major sections that will become `<section>` blocks in the HTML. For each section, include:
   - **Section title** (the `<h2>` text) — use narrative, question-based titles that tell a story (e.g., "The Problem — Why Do We Need All This?" rather than "Introduction")
   - **Topics covered** — bullet list of concepts, formulas, and ideas that belong in this section
   - **Content summary** — the key extracted content relevant to this section (include exact formulas, definitions, and specifics — enough that a subagent can write thorough HTML without needing the original PDF)
   - **Section type hints** — note if this section should include diagrams, comparison tables, connection blocks, etc. Only request SVG diagrams when the concept is spatial, architectural, or flow-based and would be significantly harder to grasp from text alone. When requesting a diagram, describe exactly what it should show.

Also plan a **final section** for "Connections & Practical Takeaways" that ties the lecture to prior material and highlights implementation tips.

**CRITICAL — SCOPE DISCIPLINE:** The learning plan must ONLY include topics that appear in the extracted lecture content. Do NOT add topics, models, comparisons, or concepts that the lecture does not cover. The teach-back is a faithful companion to THIS lecture — not a general textbook on the subject.

**Step 2 — Review the plan as a first-time learner.** Now go back through the plan and adopt the mindset of someone encountering this material for the very first time. For each section and each concept within it, reason through:

1. **"What would confuse me here?"** — Identify the specific points where a learner would get stuck. These are the spots that need deep dives, worked examples, or analogies.
2. **"What kind of help would actually work?"** — For each hard concept, decide which tool is best:
   - A **worked numerical example** (best when the math itself is the hard part — plug in real numbers and walk through step by step)
   - A **deep dive** (best for non-intuitive concepts, common misconceptions, or "why does this work?" questions)
   - An **analogy** (best only when it maps cleanly to the concept — a forced analogy is worse than none)
   - **Nothing extra** (the concept is straightforward enough that a clear explanation suffices)
3. **"What would I skip or skim?"** — Identify parts that are over-explained or padded. Mark these for concise treatment.

Add the results as an **intuition guidance** field to each section in the plan:
   - For hard concepts: specify exactly what kind of help to include and what it should cover (e.g., "deep dive on why f_t and i_t are independent — the key insight is the four combinations; include a worked example with f_t=0.1, i_t=0.9 vs f_t=0.9, i_t=0.9")
   - For straightforward concepts: mark as "no extra intuition needed"

**Important:** The learning plan is your handoff document. Each subagent will ONLY see its own section's plan entry — not the full extracted content. So be specific and thorough in the content summary. Include exact formulas with variable names, key definitions verbatim, and enough context for the subagent to write a complete section. The intuition guidance tells the subagent exactly where to invest depth and where to keep things concise.

##### Phase 2: Launch Parallel Section Subagents

Launch **one subagent per section** in parallel (all in a single message), each using `subagent_type: "general-purpose"` with `model: "sonnet"`.

Each subagent's prompt should include:
- **Its section title and content summary** from the plan (only its own section, not the full plan)
- **The HTML building blocks reference** (copy this into each prompt):
  ```
  Use these HTML building blocks:
  - <section><h2>Section Title</h2>...</section> — wrap your entire output in ONE section tag
  - <div class="equation-block">$$...$$<span class="label">Name</span></div> — for important equations (KaTeX $$ for display, $ for inline)
  - <div class="key-insight">...</div> — for critical concepts to remember
  - <div class="deep-dive"><span class="deep-dive-label">Deep Dive — Topic Name</span><p>Extended explanation...</p></div> — for hard-to-understand, non-intuitive, or exam-critical concepts that need extra depth: analogies, concrete numerical examples, alternative formula forms, common misconceptions, or intuition-building content. Aim for 2-4 per section on the hardest material.
  - <div class="connection">...</div> — for connections to previous lectures
  - <table class="comparison-table"><thead><tr><th>...</th></tr></thead><tbody>...</tbody></table> — for comparisons
  - <div class="diagram"><svg>...</svg><div class="caption">...</div></div> — for visual diagrams (use colors: #e94560 accent, #4ecca3 green, #f0c040 yellow, #eee text, #0f3460 card bg)
  - Use <h3> with class for subsections within the section
  - Use <p>, <ul>, <ol>, <li>, <strong>, <code> for body content
  ```
- **Instructions:** "Generate a single complete `<section>...</section>` HTML block for this topic.

  **CRITICAL — STAY IN SCOPE:** Only explain concepts, formulas, and examples that are explicitly covered in the lecture content summary provided to you. Do NOT introduce topics, theorems, models, or comparisons that are not in the lecture notes. If the lecture doesn't mention GANs, don't discuss GANs. If the lecture doesn't derive a formula, don't derive it. The teach-back should be a faithful, intuitive explanation of WHAT THE LECTURE ACTUALLY COVERS — not a broader textbook treatment. Analogies and examples are encouraged to build intuition, but they must serve concepts that are IN the lecture.

  **CRITICAL — INTUITION-FIRST APPROACH:** Write as if explaining to a smart person who has never seen this material before. The student finds dense mathematical presentations hard to follow. Build up concepts with intuition before formulas:

  1. **For genuinely hard or non-intuitive concepts, start with a real-world analogy or concrete example** before showing any math. But do NOT force analogies onto straightforward concepts — if a concept is self-explanatory or the analogy would be a stretch, just explain it directly. Quality over quantity.
  2. **Walk through formulas step by step.** For every equation, explain WHAT each symbol means, WHY each term is there, and WHAT WOULD HAPPEN if you removed it. Don't just show a formula — unpack it.
  3. **Include concrete numerical examples where they clarify.** After showing a formula, plug in actual numbers and walk through the computation when it helps understanding. e.g., 'If μ=2.3, σ=0.5, and we sample ε=0.7, then z = 2.3 + 0.5×0.7 = 2.65.'
  4. **Use analogies selectively, not liberally.** Only use an analogy when it genuinely illuminates the concept. A forced or imprecise analogy can confuse more than it helps. Ask: "Does this analogy make the concept clearer, or am I just adding words?" If the latter, skip it.
  5. **Build a narrative arc.** Each section should tell a STORY — start with a problem or question, develop the solution step by step, and end with a payoff or insight.
  6. **Include inline SVG diagrams** wherever a visual would genuinely aid understanding — especially for architectures (e.g., RNN unrolled, encoder-decoder, FFNN layers), data flow (e.g., how hidden state passes through time), and comparisons (e.g., AE vs VAE bottleneck). Use the diagram block: `<div class=\"diagram\"><svg>...</svg><div class=\"caption\">...</div></div>` with colors #e94560 (accent), #4ecca3 (green), #f0c040 (yellow), #eee (text), #0f3460 (card bg). Don't force diagrams where text suffices, but DO add them for spatial/architectural concepts that are hard to grasp from text alone.
  7. **After writing, review each analogy and example.** Remove or adjust any that feel forced, redundant, or don't actually make the concept clearer. If the concept is already well-explained without the analogy, cut it.

  **For concepts that are particularly important for exams, non-intuitive, or commonly misunderstood, add Deep Dive blocks** using this HTML pattern:
  ```html
  <div class=\"deep-dive\">
    <span class=\"deep-dive-label\">Deep Dive — [Topic]</span>
    <p>Extended explanation with analogies, concrete examples, alternative formulations, or intuition-building content...</p>
  </div>
  ```
  Deep Dives should go beyond the surface explanation and include things like: rewriting a formula in a more intuitive form, concrete numerical examples with actual numbers plugged in, physical/real-world analogies, common misconceptions and why they're wrong, or connections to other concepts. Aim for 2-4 Deep Dives per section, focusing on the hardest and most exam-relevant material.

  **CRITICAL — DIAGRAM QUALITY:** Only include SVG diagrams when the concept genuinely requires visual representation (architectures, data flow, spatial relationships). Do NOT create diagrams just to fill space. Every diagram must be logically correct — labels must match the formulas, arrows must point in the right direction, and the visual must accurately represent the concept. If you are not confident a diagram will be correct and helpful, omit it.

  Output ONLY the raw HTML — no markdown fences, no explanation, just the `<section>` block."

##### Phase 3: Assemble the Final HTML

1. **Read the template** from `${CLAUDE_PLUGIN_ROOT}/skills/lecture-review/references/teach-back-template.html`
2. **Replace placeholders:**
   - `LECTURE_TITLE` with the human-readable lecture name
   - `<!-- CONTENT_PLACEHOLDER -->` and the comment block below it with all the section HTML blocks concatenated in order (as returned by the subagents)
3. **Review the assembled content as a first-time learner.** Before writing the file, read through the concatenated sections and adopt the mindset of someone encountering this material for the first time. For each section, ask yourself:
   - "If I had never seen this concept before, would this explanation actually make it click?"
   - "Where would I get confused or lost? Is there a gap in the reasoning?"
   - "Does this deep dive actually deepen my understanding, or is it just more words?"
   - "Does this analogy genuinely help me grasp the idea, or is it a stretch that adds confusion?"
   - "Is this numerical example illuminating, or is it just plugging in numbers mechanically?"
   - "Does this diagram help me see something I couldn't understand from text alone?"

   Based on this review:
   - **Add** deep dives, worked examples, or analogies where a first-time learner would genuinely struggle without them
   - **Remove** analogies that don't clarify, numerical examples that don't illuminate, and deep dives that just restate what's already said
   - **Verify SVG diagrams are necessary** — remove any that don't add understanding beyond the text
   - **Check diagram correctness** — verify labels match formulas, arrows point correctly, and visuals accurately represent concepts. Fix or remove misleading diagrams.
4. **Write the file** to `COURSE_DIR/teach-back/<lecture-name>.html`
   - Create the `teach-back/` directory if it doesn't exist
   - `<lecture-name>` is the PDF filename without `.pdf`
4. **Serve via local HTTP server** and give the user a clickable link:
   - Check if a server is already running on port **8109**: use `lsof -ti:8109` on macOS/Linux, or `ss -tlnp | grep 8109` as a fallback if `lsof` is not available
   - If not running, start one in the background:
     ```bash
     cd COURSE_DIR/teach-back && python3 -m http.server 8109 &
     ```
   - Provide the link: `http://localhost:8109/<lecture-name>.html`
   - The server stays running for the session so subsequent lectures are served instantly
5. **Console output:** Only print a brief message, e.g.:
   > "Teach-back ready! Open http://localhost:8109/<lecture-name>.html to review the material.
   > Take a look, then let me know when you're ready to continue."

   Do **not** repeat the teach-back content as text in the console.

##### Small Lectures (≤ 20 pages): Simplified Flow

If the PDF was 20 pages or fewer (read directly without subagents in step 2a), the extracted content is small enough to generate HTML in one shot. In this case, **skip the parallel subagent approach** — generate all sections directly and write the file. Use the same building blocks and template assembly process described above, just do it inline instead of via subagents.

### Step 3: Q&A

After completing the teach-back, ask:
> "Any questions about this material, or are you ready to move on?"

Continue answering questions until the user says to move on. After each answer, ask again:
> "Any more questions, or ready to move on?"

### Step 4: Quiz

After the Q&A is complete, ask:
> "Would you like to take a quiz on this lecture before we generate the cheat sheet?"

If the user declines, skip to Step 5 (Cheat Sheet Generation).

If the user accepts:

1. **Generate questions:** Create **10 multiple-choice questions** (A-D) that progress from easy to challenging. **Every question MUST be grounded in specific material covered in this lecture's notes** — do not ask general knowledge questions or questions unrelated to what the lecture actually teaches.

   **Key principle: Comprehension over recall.** The student is allowed to use cheat sheets during quizzes, so there is no value in testing memorization of formulas, definitions, or specific values. Instead, test whether the student truly **understands** the concepts — can they explain *why* something works, *when* to use it, and *what happens* when conditions change? A student who understands the material but needs to glance at a formula sheet should ace the quiz; a student who memorized formulas without understanding should struggle.

   **Difficulty progression (easy → hard, superficial → deep):**
   - **Questions 1-3 (Conceptual understanding):** Test comprehension of core ideas — "Why does method X work this way?", "What is the intuition behind Y?", "In your own words, what does Z accomplish?" These confirm the student grasps the *meaning* behind the material, not just the surface-level facts they could look up on a cheat sheet.
   - **Questions 4-6 (Application & reasoning):** Apply concepts to scenarios — "If you changed parameter X, what would happen to Y and why?", "Given this scenario, which technique from the lecture would you use and what's the reasoning?" Requires understanding cause-and-effect and being able to reason through problems.
   - **Questions 7-9 (Analysis & connections):** Deeper reasoning — "Why does method A outperform method B in situation Z?", "What is the relationship between concept X and concept Y?", "What would break if assumption Z were violated and why?" Tests whether the student can reason *about* the material and connect ideas.
   - **Question 10 (Synthesis):** Connects ideas across the lecture or requires novel application — "Design a scenario where...", "Which combination of techniques would you use for... and explain the tradeoffs", "What's the flaw in this argument about...?" The student must think beyond what was explicitly stated.

   **Question design rules:**
   - **Focus on comprehension, not recall.** Never test whether someone can remember a formula, definition, or specific value — they have a cheat sheet for that. Test whether they *understand* what the formula means, when it applies, and why it works.
   - Questions should reference specific concepts, algorithms, and ideas **from this lecture's material**
   - Wrong answers should be plausible misconceptions that reveal shallow understanding — the kind of mistakes someone makes when they memorized but didn't truly comprehend
   - At least 3 questions must test "why" or "when" reasoning (not "what is" recall)
   - At least 2 questions must present a scenario and ask the student to reason through it
   - **ALL 10 questions must be conceptual / intuition-based.** Every question should test whether the student can reason about the *idea* itself — no questions that rely on memorizing numbers, formulas, specific values, or algorithmic steps. Examples: "What is the core problem that technique X solves?", "If you had to explain concept Y to a non-technical person, which analogy captures the key insight?", "What fundamental assumption does method Z rely on, and what happens conceptually when it's violated?", "Why is approach A fundamentally better suited than approach B for this class of problems?" The quiz should feel like a conversation about understanding, not a lookup exercise. If a question could be answered by scanning a cheat sheet, rewrite it.
   - **Never** ask a question that could be answered by simply looking at a cheat sheet (e.g., "What is the formula for X?" is bad; "Why does the formula for X include term Z?" is good)
   - **CRITICAL — Uniform answer length and detail.** All four answer choices (A-D) MUST be similar in length, specificity, and level of explanation. The correct answer must NOT stand out by being longer, more detailed, or more "textbook-sounding" than the distractors. This is the most common flaw in generated quizzes — the correct answer gets a thorough explanation while wrong answers are short and vague, letting a test-savvy student pick the right answer without understanding the material. To fix this:
     - Write ALL four options with the same level of detail and reasoning
     - If the correct answer includes a "because..." clause, the wrong answers must also include "because..." clauses (with plausible but incorrect reasoning)
     - If the correct answer is one sentence, all options should be roughly one sentence
     - Distractors should sound equally confident and well-reasoned — they should be *wrong* in substance, not in polish
     - After drafting each question, mentally check: "Could a student who doesn't know the answer eliminate options just by length or detail?" If yes, rewrite the options

2. **Present questions one at a time.** For each question:
   - Show the question number and difficulty tier (e.g., "**Q3/10** (Warm-up)")
   - Show the question and all four options
   - Wait for the user's answer
   - After they answer, reveal whether they were correct
   - If **correct**: briefly reinforce why that's right, referencing the specific lecture content
   - If **incorrect**: explain why their choice was wrong and why the correct answer is right. Reference the specific slide/section where this was covered. Be thorough — this is a learning opportunity.

3. **Score summary & state tracking.** After all 10 questions:
   - Calculate and display: `Quiz results: X/10 correct`
   - Show a per-tier breakdown: `Warm-up: a/3 | Application: b/3 | Analysis: c/3 | Synthesis: d/1`
   - Feedback:
     - If 9-10/10: "Excellent! You have a deep understanding of this material."
     - If 7-8/10: "Strong grasp! Review the concepts you missed — especially the harder ones."
     - If 4-6/10: "Decent foundation, but the deeper concepts need work. Want me to re-explain the topics you missed?"
     - If 0-3/10: "Let's go back over this material. Want me to re-do the teach-back focusing on your weak areas?"
   - **Save the score to state.** Read the current state file, then update (or create) a `quiz_scores` object:
     ```json
     "quiz_scores": {
       "lecture-filename.pdf": {
         "attempts": [
           {"date": "2026-03-11", "score": 7, "total": 10, "breakdown": {"warmup": 3, "application": 2, "analysis": 1, "synthesis": 1}}
         ]
       }
     }
     ```
     Append the new attempt to the `attempts` array for that lecture. Preserve all existing scores.
   - If the lecture has previous attempts, show the trend: "Previous scores: 5/10 → 7/10 → 9/10 (improving!)"

4. **Post-quiz: Update teach-back with quiz and deep dives for weak areas.** After the quiz is complete:
   - **Add the quiz to the HTML teach-back file** as an interactive section at the bottom (before the footer). Use click-to-reveal answer blocks with the question, all four options, and the correct answer with explanation. Style with CSS classes for tier badges (warm-up, application, analysis, synthesis).
   - **Add Deep Dive blocks to the main teach-back sections** for any topics where the user:
     - Got the question **wrong**
     - Expressed **hesitation** or uncertainty (e.g., "not sure", "I think", "don't know")
     - Took noticeably longer or asked for clarification
   - Each Deep Dive should go into the relevant main section (not the quiz section) and include: alternative explanations, analogies, concrete numerical examples, or rewritten formulas in more intuitive form. Use the `<div class="deep-dive">` block.
   - This ensures the teach-back becomes a **personalized study document** that reinforces exactly the concepts the user found challenging.

5. **Offer more questions:** Ask:
   > "Want another round of 10 questions, or ready to move on to the cheat sheet?"
   If the user wants more, generate 10 **new** questions (don't repeat any from previous rounds). Focus the new round more heavily on topics the user got wrong. Otherwise proceed.

### Step 5: Cheat Sheet Generation

1. **Propose content:** Present the key topics and formulas you'd include on the cheat sheet.
   Ask: "Here's what I'd put on the cheat sheet — anything to add or remove?"

2. **Layout preferences (first time only):**
   Check the state file for stored `preferences`. If `preferences` is empty or missing, ask:
   > "Quick layout preferences for the cheat sheet:
   > - Columns: 2 (default) or 3?
   > - Font size: 9pt (default), 8pt, or 7pt?
   > - Margins: 0.75in (default) or 0.5in?"

   Store the answers in the state file under `preferences`.

3. **Page limit:** Ask: "How many pages for this lecture's cheat sheet? (default: 1)"

4. **Generate LaTeX:**
   - Read the template from `${CLAUDE_PLUGIN_ROOT}/skills/lecture-review/references/per-lecture-template.tex`
   - Replace `CHEATSHEET_TITLE` with the lecture name (human-readable, derived from filename)
   - Replace `% CONTENT_PLACEHOLDER` and the comment lines below it with the actual cheat sheet content
   - Apply user's layout preferences if they differ from template defaults:
     - Columns: change `\begin{multicols}{2}` to the chosen number
     - Font size: change `[9pt]` in `\documentclass` to the chosen size
     - Margins: change `[margin=0.75in]` in `\usepackage[margin=...]{geometry}`
   - Write the file to `COURSE_DIR/cheatsheets/per-lecture/<name>-cheatsheet.tex`
     where `<name>` is the PDF filename without the `.pdf` extension

6. **Compile:**
   ```bash
   cd COURSE_DIR/cheatsheets/per-lecture && pdflatex -interaction=nonstopmode <name>-cheatsheet.tex
   ```
   - First check if `pdflatex` is available: `which pdflatex`
   - If not installed, warn the user: "pdflatex is not installed. The .tex file has been saved — you can compile it manually or upload it to Overleaf. To install locally:
     - **Ubuntu/Debian:** `sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-science`
     - **macOS:** `brew install --cask mactex-no-gui`
     - **Windows (WSL):** `sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-science`"
   - If compilation fails, show the error and ask: "LaTeX compilation had errors. Want me to try to fix them?"
   - Clean up auxiliary files: `rm -f <name>-cheatsheet.aux <name>-cheatsheet.log`

7. **Update state:**
   - Read current state file
   - Add the lecture filename to `reviewed` array (if not already there)
   - Add/update the cheat sheet path in `cheatsheets` object: `"<filename>": "cheatsheets/per-lecture/<name>-cheatsheet.tex"`
   - Preserve existing `preferences`
   - Write the full updated JSON to `COURSE_DIR/.lecture-review-state.json`

8. **Confirm:** Tell the user where the `.tex` and `.pdf` files were saved.

---

## Condense Mode (Exam Cheat Sheet)

Invoked with `/lecture-review condense` or `/lecture-review condense <pages>`. Also triggered when the user asks to generate an "exam cheat sheet" or "final cheat sheet".

The goal is to **fit all the content from every per-lecture cheat sheet into the fewest pages possible**, maximizing density. This is an exam reference sheet — every square millimeter counts.

### Step 1: Ask Page Count

If a page count was not provided as an argument, ask:
> "How many pages for the exam cheat sheet?"

### Step 2: Gather

1. Read the state file
2. List all `.tex` files in `COURSE_DIR/cheatsheets/per-lecture/` using Glob
3. If no per-lecture cheat sheets exist, tell the user:
   > "No per-lecture cheat sheets found. Review some lectures first with `/lecture-review`."
   Then stop.
4. Read all per-lecture `.tex` files **in parallel** using multiple Read tool calls in a single message (one per file)

### Step 3: Prioritize & Plan

1. Present the topics from all lectures and the target page count
2. The default approach is to include **everything** from all per-lecture cheat sheets. Only if the content clearly cannot fit even with maximum density settings, ask:
   > "Even at maximum density, all this material won't fit in [N] pages. Here's what I'd prioritize — should I weight certain lectures or topics more heavily?"
3. Let the user adjust priorities before proceeding

### Step 4: Generate

1. Read the condensed template from `${CLAUDE_PLUGIN_ROOT}/skills/lecture-review/references/condensed-template.tex`
2. **Maximize density with these hard rules:**
   - **Font size: 8pt** — use `\documentclass[8pt]{extarticle}`
   - **No margins:** use `\usepackage[margin=0.15in, top=0.15in, bottom=0.15in]{geometry}` — absolute minimum margins
   - **No headers or footers:** use `\pagestyle{empty}` — remove all headers, footers, and page numbers. Every millimeter is for content.
   - **Column count:** Use as many columns as needed to fit the content. Start with 3 columns. If content is still overflowing, try 4. The goal is to fit everything in the target page count.
   - **Ultra-compact spacing:** minimize all vertical spacing between sections, items, and paragraphs
3. Combine and distill all per-lecture cheat sheet content into the template
4. Replace `% CONTENT_PLACEHOLDER` with the condensed content
5. Write to `COURSE_DIR/cheatsheets/final/final-cheatsheet.tex`

### Step 5: Compile

```bash
cd COURSE_DIR/cheatsheets/final && pdflatex -interaction=nonstopmode final-cheatsheet.tex
```
- Same error handling as review mode (check for pdflatex, handle errors, offer to fix)
- Clean up: `rm -f final-cheatsheet.aux final-cheatsheet.log`

### Step 6: Verify Page Count

After compilation, check the page count:
```bash
pdfinfo COURSE_DIR/cheatsheets/final/final-cheatsheet.pdf | grep Pages
```
If `pdfinfo` is not available, skip this check.

If page count exceeds the target:
1. First try increasing columns (e.g., 3 → 4)
2. If still overflowing, tighten spacing further and reduce less critical content
3. Recompile and check again
4. If it still won't fit after two attempts, inform the user:
   > "The sheet came out as X pages instead of [target]. Want me to trim more content, or is X pages OK?"

---

## State File Format

Location: `COURSE_DIR/.lecture-review-state.json`

```json
{
  "reviewed": ["lecture01.pdf"],
  "cheatsheets": {
    "lecture01.pdf": "cheatsheets/per-lecture/lecture01-cheatsheet.tex"
  },
  "preferences": {
    "columns": 2,
    "font_size": "9pt",
    "margins": "0.75in"
  },
  "quiz_scores": {
    "lecture01.pdf": {
      "attempts": [
        {"date": "2026-03-10", "score": 7, "total": 10, "breakdown": {"warmup": 3, "application": 2, "analysis": 1, "synthesis": 1}}
      ]
    }
  }
}
```

When reading: if file is missing or JSON is invalid, start with empty state:
`{"reviewed": [], "cheatsheets": {}, "preferences": {}, "quiz_scores": {}}`

When writing: use the Write tool to overwrite the entire file with the full updated JSON.

---

## Important Behaviors

- **Ask when in doubt.** At every decision point where there's ambiguity, ask the user rather than assuming.
- **Chunk large PDFs.** Use the Read tool's `pages` parameter. Max 20 pages per read call.
- **Handle missing pdflatex gracefully.** Output the `.tex` file and inform the user how to install or compile manually.
- **Preserve state.** Always read state before modifying, and write back the full updated state.
- **Be thorough in teach-back.** This is a study tool — the user wants to deeply understand the material, not just skim it.
- **Keep cheat sheets dense but readable.** Maximize information per page while keeping it scannable during an exam.
