---
name: manuscript-audit
description: Full-spectrum audit of a scientific manuscript for journal-submission readiness. Covers content accuracy (numbers, claims, data), narrative flow (paragraph-to-paragraph content sequencing), academic register, structural integrity, figure audit, citation hygiene, layout/presentation, submission hygiene, and reproducibility. Use when the user asks to "audit the manuscript", "review the paper", "fix up / polish / improve" a manuscript at the level of journal-submission quality, or asks "is this submission-ready / does this read like a [target venue] paper". Project-agnostic: works for any scientific manuscript in LaTeX, Markdown, or Word.
allowed-tools: [Read, Glob, Grep, Bash, Edit, Write, Agent]
---

# Manuscript Audit

A reusable, project-agnostic methodology for auditing scientific manuscripts at journal-submission quality. Produces a structured, line-numbered findings report covering correctness, structure, prose, and submission readiness — and applies auto-fixable findings under the user's direction.

This skill is the canonical entry point for any manuscript audit work in this repository. It supersedes ad-hoc checks; if you find yourself doing two or more of the audit dimensions below by hand, invoke this skill instead.

---

## Table of contents

1. [When to invoke](#when-to-invoke)
2. [Core principles](#core-principles)
3. [Inputs](#inputs)
4. [Audit dimensions — what is checked and why](#audit-dimensions)
5. [Workflow — phased execution](#workflow)
6. [Subagent strategy](#subagent-strategy)
7. [Output format](#output-format)
8. [Heuristics — academic register vs storytelling](#heuristics)
9. [Common pitfalls](#common-pitfalls)
10. [Validation after edits](#validation-after-edits)

---

## When to invoke

**Trigger phrases:**
- "audit the manuscript", "full audit", "review the paper"
- "polish / fix up / improve / clean up the narrative or flow"
- "make sure it flows / makes sense / reads professionally / follows conventions"
- "is this submission-ready", "does this read like a [Nature / JACS / ACS Catal. / etc.] paper"
- "go through the manuscript and check everything"

**Do NOT invoke for:**
- Pure copyediting (typos only) — use a focused pass; this skill overshoots
- New-manuscript drafting — this skill audits, does not generate
- Single-figure caption rewrites — too narrow; do inline
- Pure code-comment review — wrong target

**Distinguishing this skill from related ones:**
- `hydrog-rebuild-manuscript` — builds the PDF/DOCX. Run after this skill, not instead of.
- `hydrog-audit-structure` — repo-level hygiene (stale dirs, broken symlinks). Different scope.
- `manuscript-audit` (this one) — content of the manuscript itself.

---

## Core principles

1. **Comprehensive but surgical.** The audit checks every dimension below. The fixes it produces are line-by-line, traceable to specific findings, never bulk rewrites. If a section needs a wholesale rewrite, flag as P0 and stop — get user input.

2. **Content is sacred.** Scientific claims, numbers, and citations are preserved unless the audit identifies a contradiction with canonical sources. When in doubt, keep. Never delete a claim "to improve flow."

3. **Calibrate to target venue.** Different venues have different conventions for length, Discussion depth, Methods placement, hedging norms, citation density. Always identify the target venue (or ask) before running the audit.

4. **Distinguish auto-fixable from user-input-required.** Some findings (factual errors, redundant paragraphs, stale references, register-flag substitutions, broken cross-refs) the agent fixes. Others (citation posture for in-prep collaborators, funding text, target-venue choice, scope decisions on figures) require the user. The output must separate these clearly.

5. **Content flow > transition phrases.** The narrative test is "does paragraph N's content set up paragraph N+1's premise, in a sequence that follows the natural prerequisite chain a reader needs?" — not "is there a connector word." Flag paragraphs that pivot without setup, paragraphs that restate without advancing, sequences where idea (b) is presented before its prerequisite (a).

6. **Academic register, not narrative storytelling.** Scientific manuscripts in target venues read as assertive-but-bounded technical prose anchored to quantitative claims. They do not read as discovery narratives. See [Heuristics](#heuristics) for specific lexical signals.

7. **Honesty about scope.** Always include a "what this audit did NOT check" section. The audit cannot assess novelty against current literature, run statistical reanalysis, evaluate experimental design, or replace peer review.

---

## Inputs

| Input | Required? | Purpose |
|---|---|---|
| Manuscript file path | Required | The thing being audited. `.tex`, `.md`, `.docx`. |
| Target venue | Required (ask if missing) | Calibrates register, length, Discussion depth, hedging norms. |
| Canonical-data source(s) | Strongly recommended | STATUS.md, output JSON, validated tables. Used in content-accuracy phase. |
| Style notes / voice guide | Optional | Author or PI's preferred phrasings (e.g., "Heinz-style"). Treat as override for register heuristics when provided. |
| Prior audit report(s) | Optional | Avoids re-flagging issues already known. Reference, do not regress. |
| Submission checklist | Optional | Venue-specific (data availability format, COI declaration, ethics statement, etc.). |
| Repository state | Optional | `git status`, `git log` to identify recent edits and uncommitted changes that may need separate review. |

---

## Audit dimensions

Each dimension below is a separate phase of the audit. The "why" explains what failure mode it catches; the "how" describes the procedure.

### A. Content accuracy
**Why:** A manuscript that misstates its own data fails peer review on first read. Headline numbers must match the canonical pipeline output; internal numbers must be consistent across Abstract, Results, Conclusions; stale references to deprecated pipelines/versions/dates must be eliminated.

**How:**
1. Load canonical data source(s) — STATUS.md, output JSON, validated tables.
2. Cross-reference every quantitative claim in the manuscript:
   - Headline numbers in Abstract, Results paragraphs, Conclusions, figure captions.
   - Derived ratios (e.g., 2.92× = 0.13 / 0.0445; verify if claimed).
   - Statistical quantities (p-values, χ², SE, confidence intervals).
   - Sample counts, run lengths, time scales, temperatures, dimensions.
3. Internal triangle check: Abstract claim ↔ Results claim ↔ Conclusions claim — all three must agree.
4. Stale-reference sweep: deprecated pipeline names (e.g., "5-gate", "15-sample"), old versions, superseded dates.
5. Spelling consistency for proper nouns (system names, software names: CHARMM36, INTERFACE, NAMD, GROMACS, etc.).

**Flag:**
- Numeric mismatch between manuscript and canonical
- Internal triangle disagreement
- Stale pipeline / version / date references
- Inconsistent spelling/capitalization of proper nouns

### B. Narrative flow (paragraph-to-paragraph content sequencing)
**Why:** A paper that has correct facts but disjoint paragraphs forces the reader to do the work the author should have done. Editor and reviewer first impressions are shaped almost entirely by whether the argument unfolds in the natural prerequisite chain. The test is content sequencing, not connector words.

**How:**
For each paragraph, determine and record:
1. **Topic claim** — what is this paragraph asserting? Is the claim sentence first, or buried? Is the claim premature (stated before evidence appears)?
2. **Evidence** — what does the paragraph offer? Quantitative, figure ref, prior-work citation, mechanism argument? Or just assertion?
3. **Setup for next** — does the last sentence/clause establish the premise the next paragraph needs?
4. **Pickup from previous** — does the first sentence pick up the thread the previous paragraph laid down, or pivot abruptly?

For each section, list the paragraph claims in order and ask: is this the natural order in which a domain reader needs the ideas? If the science requires (a) → (b) → (c), is the manuscript ordering them so?

**Flag:**
- Orphan paragraph (does not connect to neighbors)
- Sequence break (idea ordering violates prerequisite chain)
- Premature claim (stated before supporting evidence)
- Buried claim (paragraph offers evidence but never states the claim)
- Restatement-only (paragraph repeats without advancing)
- Pivot without setup (abrupt topic shift between paragraphs)
- Filler (paragraph that could be deleted with no loss)
- Out-of-order subsections (Discussion subsection that depends on a later one's setup)

Apply the same content-flow test at section boundaries (does the end of Background actually set up the opening of Results?).

### C. Academic register vs storytelling
**Why:** Scientific manuscripts are not stories. Register slip — dramatic adverbs, narrative first-person, mystery framing — undermines credibility and signals the author treated the venue as a popular-science outlet. Editors of technical journals (J. Catal., ACS Catal., JACS, J. Phys. Chem. C, etc.) flag this on first read.

**How:**
1. Pattern-scan the prose for storytelling lexical signals (see [Heuristics](#heuristics) for full list).
2. For each flagged instance, propose an academic substitute that preserves the technical content.
3. Check active/passive voice ratio — academic writing uses active voice with subject = data/system/result, plus "we" for actions taken; avoid passive evasion ("it was found that").
4. Check tense conventions — past for actions taken in this work, present for general truths and reading the figures, future avoided in claims.
5. Check hedging calibration — claims must match evidence strength ("consistent with" for correlative findings, "shows" only when mechanism is established, "proves" almost never).

**Flag:**
- Dramatic adverbs without quantitative justification ("strikingly", "remarkably", "surprisingly", "elegantly")
- Discovery narrative ("we set out to", "our journey", "we uncovered")
- Mystery framing ("what could explain X? the answer lay in...")
- Personification ("the data wants to tell us")
- Editorialization ("nicely", "beautifully")
- Overclaim ("proves", "demonstrates conclusively") with correlative evidence
- Filler ("actually", "basically", "essentially", "simply", "just")
- Passive evasion ("it was found that", "it was observed that")
- Tense drift (mixing past and present in claims about the same finding)

### D. Structural integrity
**Why:** A manuscript that does not match the expected scientific-paper template confuses editors who triage by section. Most chemistry/materials journals expect Abstract → Intro/Background → Methods → Results → Discussion → Conclusions → (Outlook) → Acknowledgments → References. Some allow Methods at the end (Nature style); some require it after Intro. Section completeness, hierarchy depth, and order matter.

**How:**
1. Enumerate sections and subsections; build a tree.
2. Compare against the target venue's expected template:
   - Are all expected sections present?
   - Is the order venue-appropriate?
   - Is subsection depth reasonable (target ≤ 3 levels for most journals)?
3. Check section-length balance — is one section absurdly long or short?
4. Check that each section has a topic-setting opening sentence and a "so what" closing sentence.
5. For combined "Results and Discussion" sections, verify that interpretation is integrated, not deferred.

**Flag:**
- Missing expected section (e.g., no §Limitations in a methods-heavy paper)
- Section out of expected order for target venue
- Subsection nesting too deep (>3 levels)
- Section with no topic-setting opener or "so what" closer
- Length imbalance suggesting one section is underdeveloped

### E. Discussion depth
**Why:** Description without interpretation is a Results section, not a Discussion. Reviewers explicitly look for: (1) interpretation of each finding; (2) engagement with prior work that is argumentative, not perfunctory; (3) limitations integrated where claims are made; (4) "so what" landing per subsection.

**How:**
For each Results+Discussion subsection, score:
1. **Description vs interpretation ratio.** Count sentences that describe what a figure shows vs. sentences that interpret what it means. Target ≥ 1:1.
2. **Engagement with prior work.** Are citations argumentative ("our finding refines / contradicts / extends Smith 2020 in that ...") or perfunctory ("see Smith 2020")? Count argumentative vs perfunctory.
3. **Hedging calibration.** Are claims qualified to evidence strength?
4. **"So what" landing.** Does the subsection close with a sentence articulating what this finding means for the larger argument?
5. **Limitation integration.** Are caveats placed near the claims they bound, or only deferred to a §Limitations section?

**Flag:**
- Description-only subsection (no interpretation sentences)
- Perfunctory citation chain (no argumentative engagement)
- Over- or under-hedged claim
- Missing "so what" closing
- Caveats only in §Limitations, none integrated near claims

### F. Figure audit
**Why:** Each figure must do argument work, not decoration. Figures are how readers triage: most reviewers look at the figures before reading the prose carefully. Caption discipline is critical (bold lead claim + interpretation, not bare description). Figure ordering should follow the prerequisite chain.

**How:**
For each figure:
1. **Argument role** — what does this figure assert? Is it advancing the argument, or showing the same data twice?
2. **Caption discipline** — does it open with a bold claim sentence, then provide interpretation? Or just describe panels?
3. **Placement** — does the prose set up the figure before it appears? Is it referred back to after?
4. **Ordering** — does each figure set up the next, or do they sit in parallel without sequence?
5. **SI candidacy** — is any figure showing data that supports a secondary claim and would better serve the argument as SI?
6. **Subpanel labels** — consistent (a/b/c vs A/B/C), referenced in caption and prose?
7. **Color/legibility** — are colors distinguishable (color-blind safety), are labels readable at print scale, are units shown?

**Flag:**
- Figure with no clear argument role (decoration)
- Caption with no claim sentence (bare panel description)
- Figure shown before prose setup (forward orphan)
- Figure not referenced in prose (orphan)
- Figure ordering not following prerequisite chain
- Redundant figures (could be merged or one moved to SI)
- Inconsistent subpanel labeling
- Color-blind unsafe palette in a venue that flags it

### G. Layout & presentation
**Why:** Editors notice layout artifacts before content. Overfull boxes, awkward float placement, half-empty pages, broken tables, and orphan headings signal a draft that has not been proofread by anyone.

**How:**
1. Build the manuscript clean (`make pdf` for LaTeX) and capture the build log.
2. Scan log for warnings:
   - "Float too large for page" — figure or table dimensioned wrong
   - "Overfull \hbox" — line overruns margin
   - "Underfull \vbox" — page-height stretching artifact
   - "Citation undefined", "Reference undefined" — broken cross-refs
3. Render key pages (first page, every section opening, last page); spot-check:
   - Page breaks not landing inside a paragraph mid-sentence
   - Section headings not orphaned at page bottom
   - Figure-caption pairs not split across pages
   - White-space gaps not absurd (>30% blank suggests float placement issue)
4. Verify Table of Contents (if present) matches actual section headings.

**Flag:**
- Each LaTeX build warning except trivial font notes
- Page with >30% white space (likely float-placement artifact)
- Section heading at bottom of page (orphan)
- Figure-caption split across pages
- Broken cross-reference

### H. Citation hygiene
**Why:** Broken citations are an instant rejection signal. Citation rhetoric (placement, specificity, argumentative use) reflects the author's command of the literature.

**How:**
1. Verify every `\cite{key}` (or equivalent) resolves to a valid `.bib` entry.
2. Verify every `.bib` entry is cited (no orphan entries).
3. Check citation placement — at end of supported claim sentence, not floating.
4. Check citation density — too many in one sentence ("[1,2,3,4,5]") is a smell; too few in Background suggests under-engagement.
5. Check argumentative use — see Discussion-depth phase.
6. Check `.bib` fields — title, journal, year, DOI, page, volume present.
7. Check for "in preparation" / "submitted" / "in press" placeholders that need decision before submission.

**Flag:**
- Undefined `\cite` key
- Orphan `.bib` entry
- Citation floating in middle of sentence with no attached claim
- "Citation chain" of 5+ refs in one sentence (decorating)
- "in preparation" placeholder needing posture decision
- Missing DOI / volume / page in `.bib` entry

### I. Convention compliance (venue-calibrated)
**Why:** Each venue has style preferences. Compliance signals professionalism and reduces editorial friction. Non-compliance can trigger desk-reject or back-to-author for formatting.

**How:**
1. Identify target venue → look up its style guide (if available locally) or apply general scientific-writing conventions.
2. Check:
   - **Cross-reference style** — `\ref{sec:X}` vs §X vs Section X vs Sec. X — pick one, apply consistently
   - **Abbreviation discipline** — defined at first use *in each section a reader might skip to* (Abstract, Intro, Methods, Results, Conclusions). Common offenders: COM, KDE, FF, CN, MD.
   - **Number/unit formatting** — `\SI{}` consistency for SI units; one decimal-precision policy throughout
   - **Heading style** — capitalization (sentence case vs title case), numbering depth
   - **Tense conventions** — past for done, present for true, future avoided
   - **Person conventions** — "we" for actions ("we resolve"), avoid narrative use ("we noticed")
   - **Equation/table usage** — appropriate, numbered, referenced
   - **List-vs-prose decisions** — enumerate environments only when ordering matters
   - **British vs American spelling** — pick one, apply consistently
3. Check title and Abstract optimization for the venue:
   - Title: does it carry the story or just describe the system? Editor-facing strings should signal contribution.
   - Abstract first 1–2 sentences: editors triage on these. Do they state the problem and the contribution?

**Flag:**
- Inconsistent cross-reference style
- Abbreviation undefined in a skip-to section
- Mixed `\SI{}` and inline unit formatting
- Title that doesn't signal contribution
- Abstract opening that buries the contribution

### J. Submission hygiene
**Why:** A manuscript with `\todo{}` placeholders, empty Acknowledgments, missing data-availability URLs, or unresolved Outlook-section banners cannot be submitted. These are blocking items.

**How:**
1. Grep for `\todo{`, `[TBD]`, `TODO`, `FIXME`, `XXX`, `\sectioninprogress`, `(In progress)`.
2. Verify Acknowledgments has funding text and grant numbers.
3. Verify Data Availability has actual URL/DOI, not placeholder.
4. Verify Code Availability has actual URL, not placeholder.
5. Verify all collaborator citations have a posture decision (in-prep vs submitted vs DOI).
6. Verify ORCID, affiliations, contributor statements (CRediT) present if venue requires.
7. Verify ethics / COI / funding declarations present if venue requires.

**Flag:**
- Each `\todo{}` or placeholder
- Empty Acknowledgments / funding section
- Placeholder data/code URL
- Unresolved collaborator citation posture
- Missing venue-required declaration

### K. Reproducibility
**Why:** High-quality venues increasingly require reproducibility — code availability, parameter provenance, version stamping, deposit DOI for raw data. A manuscript that cannot be reproduced from its own description is a reproducibility failure regardless of content quality.

**How:**
1. Methods section: are all parameters specified (force fields, cutoffs, time steps, ensembles, seeds)?
2. Code availability: is the code released, with a version tag matching the manuscript's analysis?
3. Data availability: are raw trajectories, output JSONs, parameter files deposited?
4. Parameter provenance: is the source library / version / commit documented? (For this project: `lib_version`, `lib_git_sha`, `gate_fingerprint` per project memory.)
5. Figure provenance: can each figure be regenerated from the deposited code + data?

**Flag:**
- Underspecified Methods parameter
- Unreleased code with no embargo justification
- Undeposited data
- Missing version/commit stamping
- Figure with no regeneration path

### L. Document hygiene
**Why:** Typos, broken LaTeX, orphan commands, and stale comments are noise that distracts reviewers from the science.

**How:**
1. Grep for common LaTeX typos: `\\\\` (double backslash in odd places), unmatched braces (Bash: `awk '{n+=gsub(/{/,""); m+=gsub(/}/,"")} END{print n,m}'` — should be equal), stray `%` in math mode.
2. Check for stale or misleading comments (`% Figure 3:` when figure is now Figure 4).
3. Check for embedded TODOs in code blocks if Methods includes pseudocode.
4. Spell-check via `aspell` or equivalent, with a project dictionary for technical terms.
5. Check for accidental duplicated paragraphs (search for repeated 10+ word sequences).

**Flag:**
- Unbalanced braces or orphan LaTeX commands
- Stale comments
- Repeated paragraphs
- Spell-check hits not in technical-term dictionary

### M. Title & Abstract optimization
**Why:** The title and abstract are the only parts of the manuscript that editors and most reviewers read with full attention. They are the manuscript's interface to the world. Optimizing them is the single highest-leverage activity in submission prep.

**How:**
1. **Title** — short test: read the title without context. Does it convey (a) the system, (b) the contribution, (c) the venue's interest? Examples:
   - Weak: "A Molecular Dynamics Study of Pt Nanoparticles"
   - Strong: "Hollow-Site Dominance and Curvature-Concentrated Reactivity in NEC Dehydrogenation on Pt Cuboctahedra"
2. **Abstract first 2 sentences** — these are the editor-triage zone. Do they state (a) the problem, (b) the contribution? Avoid burying the contribution past sentence 3.
3. **Abstract structure** — most venues expect: motivation → approach → key findings (2–3) → implications. Check coverage.
4. **Abstract length** — venue-specific (often 150–250 words). Check.
5. **Keywords** — if required by venue, present and venue-appropriate?

**Flag:**
- Title that describes the system without signaling contribution
- Abstract opening that buries the contribution
- Abstract missing one of motivation/approach/findings/implications
- Abstract length out of venue range
- Missing keywords if required

### N. Supplementary material coverage
**Why:** SI is where deferred content lives — sensitivity analyses, parameter tables, additional figures, methodological detail. The main text refers to SI; the SI must actually contain what is referred. Mismatches are common when SI is built late.

**How:**
1. Grep main text for "see Supporting Information" / "SI Table SX" / "Figure SY" / "Section SZ" — list all references.
2. Open the SI document; verify each referenced item exists.
3. Check SI table/figure numbering matches main-text references.
4. Check SI content does not duplicate main-text content unnecessarily.
5. If SI references main-text figures, verify those references resolve.

**Flag:**
- Main text references SI item that does not exist
- SI numbering mismatch
- SI duplicates main-text content
- SI orphan content (not referenced from main text)

---

## Workflow

Run phases in this order. Use TaskCreate to track progress.

### Phase 0 — Setup
1. Locate manuscript file. Confirm it builds (e.g., `cd <manuscript_dir> && make pdf` for LaTeX). Capture build log.
2. Identify target venue. If not provided, ask. Default for catalysis/structure-sensitivity work: ACS Catalysis or J. Catal.
3. Identify canonical-data source(s). For this project: STATUS.md + `analysis/ensemble/results/.../outputs/*.json`.
4. Read voice/style notes if provided.
5. Read prior audit report(s) if present, to avoid re-flagging.
6. Record line counts, section structure for reference in the report.

### Phase 1 — Context pass
Read the manuscript top-to-bottom once. Build a model of the argument. At end of pass, produce a 2-paragraph summary of the manuscript's central claim and how it is argued. This is the proof-of-comprehension checkpoint.

### Phase 2 — Audit dimensions
Run dimensions A–N from the [Audit dimensions](#audit-dimensions) section. Each produces line-numbered findings. For long manuscripts (>500 lines), parallelize via subagents (see [Subagent strategy](#subagent-strategy)).

The recommended order is:
1. **Correctness first** (A, H, L) — facts, citations, document hygiene
2. **Structure next** (D, F, G) — sections, figures, layout
3. **Prose** (B, C, E) — narrative flow, register, discussion depth
4. **Readiness** (I, J, K) — convention, submission, reproducibility
5. **Optimization** (M, N) — title/abstract, SI

### Phase 3 — Synthesis & triage
Group all findings:
- **P0 — auto-fixable** (factual errors, redundant content, register substitutions, broken refs, stale comments)
- **P0 — user-input required** (citation posture, funding text, scope decisions, venue-specific format choices)
- **P1 — auto-fixable** (consistency issues, polish)
- **P1 — user-input required** (style judgment calls)
- **P2 — polish** (optional)

Estimate effort. Recommend execution sequence.

### Phase 4 — Apply auto-fixes
Surgical edits, traceable to specific findings. No bulk rewrites. Preserve scientific content.

When a fix would substantively change a claim, qualify the change in the report and flag for user review even if technically auto-fixable.

### Phase 5 — Validate
1. Rebuild manuscript clean (`make clean && make pdf && make word`).
2. Confirm no new undefined references.
3. Spot-render Abstract, opening of each major section, Conclusions, and any heavily-edited section.
4. Diff against pre-edit baseline (`git diff` if tracked); confirm no scientific content was inadvertently removed.
5. Re-read Abstract; confirm it still previews the story Results delivers.
6. Update the audit report with "after-edit" status per finding.

### Phase 6 — Report
Hand back the structured findings report (see [Output format](#output-format)). Include:
- What was checked
- What was fixed
- What remains for user input
- What this audit did NOT check (scope honesty)

---

## Subagent strategy

For long manuscripts (>500 lines) or comprehensive audits across all 14 dimensions, use Explore subagents.

**Single-agent strategy** (short manuscript, <500 lines):
- One Explore subagent runs all phases in sequence with a single self-contained brief.

**Multi-agent strategy** (long manuscript, comprehensive audit):
- One agent per dimension cluster:
  - Agent 1: Correctness (A, H, L)
  - Agent 2: Structure (D, F, G)
  - Agent 3: Prose (B, C, E)
  - Agent 4: Readiness (I, J, K)
  - Agent 5: Optimization (M, N)
- Run in parallel where possible
- Synthesize findings in main thread

**When dispatching subagents, always provide:**
- The relevant section of this skill (or the full skill if uncertain)
- The manuscript file path
- The target venue
- The canonical-data source path
- Style notes if any
- Prior audit reports if relevant

Do NOT assume the subagent has read this skill. Brief explicitly.

---

## Output format

```markdown
# Manuscript Audit — <ISO date>

## Setup
- File: <path>
- Build status: <clean / N warnings / M errors>
- Target venue: <venue>
- Canonical source(s): <path or "none">
- Style notes: <name or "default">
- Length: <N pages, M lines>
- Prior audits: <list or "none">

## Executive summary
3–6 sentences:
- Overall health
- Biggest correctness concern
- Biggest structural concern
- Biggest prose concern
- Biggest submission-readiness concern
- Count of findings per priority

## Phase 1 — Context summary
Two paragraphs summarizing the manuscript's central claim and how it is argued. Demonstrates the agent understood the science before auditing it.

## Findings by dimension

### A. Content accuracy
- **L<n>:** <issue> | **canonical:** <value> | **fix:** <suggested edit> | **severity:** P0/P1/P2
- ...

### B. Narrative flow
- **L<n>:** <issue, e.g. "paragraph claim premature, evidence appears in next paragraph"> | **fix:** <suggested reorder or rewrite> | **severity:**
- ...

### C. Register
- **L<n>:** <flagged phrase> | **substitute:** <academic alternative> | **severity:**
- ...

### D. Structure
- ...

### E. Discussion depth
- ...

### F. Figure audit
- **Fig N:** <issue> | **fix:** <suggested change> | **severity:**
- ...

### G. Layout & presentation
- ...

### H. Citation hygiene
- ...

### I. Convention compliance
- ...

### J. Submission hygiene
- ...

### K. Reproducibility
- ...

### L. Document hygiene
- ...

### M. Title & Abstract optimization
- ...

### N. Supplementary material coverage
- ...

## Triage
- **P0 — auto-fixable:** [finding IDs]
- **P0 — user-input required:** [finding IDs]
- **P1 — auto-fixable:** [finding IDs]
- **P1 — user-input required:** [finding IDs]
- **P2 — polish:** [finding IDs]

## Recommended execution sequence
Numbered list with estimated effort. Group items that can be done in one editing pass.

## What this audit did NOT check
Be explicit:
- Did not assess novelty against current literature
- Did not run statistical reanalysis or independent verification
- Did not evaluate experimental design
- Did not check English for native-speaker fluency (recommend separate pass)
- Did not replace peer review
- (Other scope limits as relevant)

## After-edit status (Phase 4 onward)
For each finding: APPLIED / DEFERRED (reason) / FLAGGED FOR USER

## Files modified
List of file paths with one-line description per file.
```

---

## Heuristics

### Academic register signals (KEEP) — examples

- "Catalytic dehydrogenation of N-ethylcarbazole on platinum proceeds through three stoichiometric two-H₂ eliminations."
- "Twenty independent 12.50 ns trajectories at 453 K resolve 397 reactive configurations."
- "Per-face χ² tests fail to reject Oh-equivalence (p₁₀₀ = 0.43, p₁₁₁ = 0.26)."
- "The activity difference cannot be explained by surface-atom count alone."
- "These findings locate catalytic privilege at sites where surface geometry breaks symmetry."
- "INTERFACE reproduces the Pt lattice constant to within 0.3% of experiment."
- "Across multiple length and time scales, the picture is robust."

### Storytelling signals (FLAG) — examples to remove

- "We set out to understand why cuboctahedra are so much more active." — replace: "We characterize the atomistic basis for cuboctahedron activity."
- "Strikingly, the data revealed a clear pattern." — replace: "The data show <quantitative claim> (p < 0.01)." (Quantify, don't dramatize.)
- "Our journey began with a simple question." — delete entirely.
- "The system, as it turned out, had a story to tell." — delete entirely.
- "We were amazed to find that..." — replace: "We find that <quantitative claim>."
- "It was found that the contact density was higher at vertices." — replace: "Contact density at vertices was 2.92× the {111}-interior value."

### Specific lexical flags (regex-friendly)

- `\b(strikingly|remarkably|surprisingly|notably|elegantly|beautifully|nicely|interestingly)\b` — flag, judge each on quantitative justification, usually delete or replace
- `\b(set out to|journey|discovered|uncovered|amazed)\b` — flag, propose academic substitute
- `\b(proves?|demonstrates conclusively|definitively|clearly shows)\b` — flag, replace with calibrated hedge unless evidence is conclusive
- `\b(actually|basically|essentially|simply|just|really)\b` — usually filler, delete
- `\b(in order to)\b` — replace with "to" unless rhythm-justified
- `\b(it (is|was) found that|it was observed that|it was noted that)\b` — passive evasion, rewrite active
- `\b(very|quite|rather|somewhat)\b\s+\w+` — flag intensifier+adjective; usually replace with quantitative
- `\b(plays a role|plays an important role)\b` — vague, replace with mechanism statement
- `\b(novel|new|first)\b` — claim of novelty; verify against literature, hedge if uncertain

### Voice-guide override

If a project-specific style note is provided (e.g., "Heinz-style"), use it as the calibration baseline. Heinz-style example (per project README):
- Lead with structure-sensitivity / agreement-window claim
- Frame FF choice via experimental anchoring, not DFT
- Long list-laden sentences, assertive-but-bounded tone
- Detailed figure captions (claim sentence + interpretation, not bare description)
- Signature phrasings: "in quantitative agreement with", "thermodynamically consistent", "within Z% of calorimetric experiment", "across multiple length and time scales"

When a style note conflicts with default register heuristics, the project style note wins.

---

## Common pitfalls

- **Conflating fact-check with narrative audit.** Phase A covers facts; Phases B–C–E cover prose. Don't substitute one for the other. The first audit on this project (2026-04-24, pre-skill) made this mistake — it verified numbers but reported "narrative is coherent ✓" without engaging with paragraph-level content flow.
- **Bulk rewrites.** This skill produces line-numbered surgical edits. If a section needs a wholesale rewrite, flag as P0 and stop.
- **Removing technical content "to improve flow."** Scientific content is sacred. Edits should preserve every claim and every number unless the audit shows internal contradiction.
- **Calibrating hedge language without checking evidence strength.** Don't soften "shows" to "is consistent with" without verifying that the evidence is correlative; don't strengthen "consistent with" to "shows" without verifying causation/mechanism is established.
- **Treating the manuscript as a story.** "Make it flow" does not mean "make it narrative." It means "make the content sequence be the natural prerequisite chain a reader needs."
- **Ignoring venue conventions.** A perfectly polished manuscript for *Nature Catalysis* (heavy Discussion, broad-impact framing) can be over-pitched for *J. Phys. Chem. C* (system-characterization, methods-forward). Calibrate.
- **Skipping Phase 1.** Without the context pass, the audit cannot evaluate whether a paragraph fits the argument — it can only check local consistency. Always summarize the manuscript before flagging.
- **Trusting the audit report uncritically.** Subagent reports describe what the agent intended to check, not necessarily what it actually checked. Spot-verify a few findings by re-reading the cited lines yourself before applying edits.
- **Not declaring scope limits.** Always include "what this audit did NOT check" — keeps the user calibrated.

---

## Validation after edits

1. Build clean: `make clean && make pdf && make word` (or equivalent for non-LaTeX manuscripts). Capture build log; verify no new warnings/errors.
2. Render and visually spot-check:
   - Title page (first impression)
   - Abstract
   - Opening of each major section
   - Each figure caption
   - Conclusions
   - Any heavily-edited section
3. Diff against pre-edit baseline (`git diff <file>`); for each diff hunk, confirm:
   - It corresponds to a finding in the audit report
   - It preserves all scientific claims and numbers
   - It does not introduce contradictions with other parts of the manuscript
4. Re-run a focused content-accuracy spot-check on edited paragraphs (numbers still match canonical).
5. Update the audit report's after-edit status section.
6. If the build broke or content was inadvertently removed, revert and re-plan; do not patch over.
