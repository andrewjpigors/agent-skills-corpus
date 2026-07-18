---
name: paper-review
description: "Comprehensive multi-agent research paper review — reference verification, vision analysis, independent domain survey, datapoint-level claim validation. The thorough review most papers never get."
argument-hint: "[path] — PDF or DOCX file path"
version: "1.0"
user-invocable: true
context: fork
model: opus
---

# Comprehensive Paper Review

Orchestrate a multi-phase, multi-agent review of a research paper. Produces dimension-specific analysis files and a unified review report as markdown in a per-paper review workspace.

**Design principles:**
- Every claim verified against data, not taken at face value
- Vision model checks every figure and table independently
- References verified against their actual content, not just existence
- Independent literature survey — find what the paper *should* cite, not just what it does cite
- Datapoint-level granularity — numbers in text must match figures

## Input Handling

The user provides a **file path** to a PDF (`.pdf`) or DOCX (`.docx`).

Detection logic:
```
if argument ends with .pdf → Route: PDF
if argument ends with .docx → Route: DOCX
else → ask user for a valid file path
```

## Phase 0: Ingestion & Setup

### Route 1: PDF File

```bash
REVIEW_DIR="reviews/{paper_slug}_{timestamp}"
mkdir -p "$REVIEW_DIR/00_source"
cp "{input_path}" "$REVIEW_DIR/00_source/"
.venv/bin/python .claude/skills/paper-review/scripts/ingest.py \
    --pdf "{input_path}" \
    --output "$REVIEW_DIR/00_source/"
```

This produces:
- `parsed_text.md` — normalized text with section structure
- `figures/` — extracted embedded images
- `pages/` — full-page renders at 200 DPI (for vision analysis)
- `metadata.json` — title, authors, page count, figure/table counts

### Route 2: DOCX File

Same as PDF but with `--docx` flag. No page renders (DOCX doesn't have fixed pages).

### After Ingestion

1. Read `metadata.json` and `parsed_text.md`
2. Create remaining workspace directories:
   ```
   mkdir -p "$REVIEW_DIR"/{01_extraction,02_dimensions,03_references/deep_verification,04_synthesis}
   ```
3. Derive `paper_slug` from title (lowercase, hyphens, max 50 chars)
4. Report to user: "Ingested: {title} — {pages} pages, {figures} figures, {tables} tables. Starting extraction."

---

## Phase 1: Deep Extraction

**Executor:** You (orchestrator), single focused pass. This is the foundation — everything downstream depends on it.

Read `00_source/parsed_text.md` in full. Then produce three artifacts:

### 1.1 Claim Extraction — `01_extraction/claim_map.md`

Extract **every** claim the paper makes, classified by type:

**For each claim, record:**
```markdown
### CLAIM-{NNN}: {one-sentence claim}

- **Type:** novel | background | methodological | interpretive
- **Location:** Section {X}, paragraph {Y}
- **Verbatim:** "{exact quote making the claim}"
- **Strength language:** demonstrates | shows | suggests | is consistent with | indicates | proves | implies
- **Evidence pointers:**
  - Figure {N}: {what the figure supposedly shows}
  - Table {N}: {what data point is cited}
  - Data: {inline numbers or statistics}
  - Reference: [{ref_number}] — {what the reference supposedly supports}
- **Flags:** [if any issues detected during extraction]
```

**Extraction depth:**
- Do NOT just extract section-level claims. Go to the **datapoint level**.
- "The particle size increased from 50 nm to 120 nm (Figure 3a)" → extract the specific numbers, the figure reference, and what the figure should show.
- Implicit claims count. If the Discussion says "consistent with Smith et al." without hedging, that implies agreement — extract it.
- Count strength language carefully. "Demonstrates" is much stronger than "suggests."

### 1.2 Vision Analysis — Figures & Tables

For **every** figure and table in the paper:

1. Read the page render (`pages/page_NNN.png`) or extracted figure (`figures/figure_NNN.png`)
2. Independently describe what the figure/table shows — BEFORE reading what the text claims about it
3. Then compare your independent reading against the text's claims about this figure
4. Record in `01_extraction/claim_map.md` under each relevant claim:

```markdown
#### Vision Check: Figure {N}
- **Independent reading:** {what I see in the figure}
- **Text claims:** {what the paper says about this figure}
- **Alignment:** match | partial_mismatch | mismatch
- **Details:** {specific discrepancies if any — axis labels, trends, magnitudes, error bars}
```

**Critical checks:**
- Do axis labels match what the text describes?
- Do trends go in the direction claimed?
- Are error bars present and do they support statistical claims?
- Do the numbers in the text match what's visible in the figure?
- Are there features in the figure the text doesn't mention (cherry-picking)?

### 1.3 Reference Catalog — `01_extraction/reference_catalog.md`

For **every** citation in the paper:

```markdown
### REF-{NNN}: [{ref_number}] {author}, {year} — {title if available}

- **Citation contexts:** (every place this reference is cited)
  1. Section {X}: "{sentence where cited}" — Usage: {background | method_justification | claim_support | comparison | contradicts}
  2. ...
- **Importance:** key_claim_support | method_basis | background | peripheral
- **Bibliographic details as stated:** {full reference string from the reference list}
```

### 1.4 Checkpoint 1

Present to user:

```
## Extraction Summary

**Paper:** {title}
**Claims extracted:** {N} ({K} novel, {M} background, {J} methodological, {L} interpretive)
**Figures analyzed:** {N} — {X} aligned, {Y} partial mismatch, {Z} mismatch
**References cataloged:** {N} — {K} supporting key claims, {M} method basis, {J} background

### Claim Hierarchy (top-level)
1. {Main novel claim 1} [strength: {language}]
   - Supported by: Figure {X}, Table {Y}, Refs [{a}, {b}]
2. {Main novel claim 2} ...
...

### Vision Flags (if any mismatches found)
- Figure {N}: {brief description of mismatch}
...

Confirm scope before I proceed to dimension analysis?
```

Wait for user confirmation. User may:
- Adjust scope (e.g., "focus on claims 1-5, skip background claims")
- Add context (e.g., "I know the authors, ref [7] is actually my paper")
- Flag known issues (e.g., "the methods section is thin, dig into that")

---

## Phase 2: Dimension Analysis (Agent Team)

### 2.1 Team Setup

Create a persistent agent team:

```
TeamCreate: paper-review-{paper_slug}
```

**Team structure:**
- **You (orchestrator):** Dispatch agents, collect results, manage checkpoints
- **6 dimension agents** (see below): Each analyzes one dimension, writes one MD file

### 2.2 Shared Context Package

Every agent receives:
1. **The full `01_extraction/claim_map.md`** — the foundation
2. **The full `01_extraction/reference_catalog.md`** — reference context
3. **Paper metadata** — title, authors, journal, year
4. **The original `00_source/parsed_text.md`** — full paper text
5. **User context from Checkpoint 1** — any adjustments or focus areas

### 2.3 Agent Roles & Dispatch

Dispatch all 6 agents in parallel using `SendMessage` with `run_in_background: true`.

Each agent follows the same output protocol:
1. Analyze their dimension
2. Write their findings to `02_dimensions/{dimension_name}.md`
3. Append flagged items to `flags.md` in the review workspace root
4. Send a summary back to the orchestrator (max 500 words)

---

#### Agent 1: Reasoning Chain

**File:** `02_dimensions/reasoning_chain.md`

**Prompt template:**
```
You are the REASONING CHAIN analyst in a comprehensive paper review team.

Paper: {title}
Your task: Map and evaluate the paper's argument architecture.

Read the claim map and full paper text provided. Then analyze:

1. **Argument Map** — Draw the logical flow: premises → intermediate conclusions → final claims.
   For each step, identify the argument type (deductive, inductive, abductive, analogical).

2. **Logical Gaps** — Where does the argument skip steps? Where are implicit assumptions
   not stated? Where does a conclusion not follow from its premises?

3. **Alternative Explanations** — For each novel claim, list at least 2 alternative
   explanations the authors did NOT consider. Are they addressed anywhere? Dismissed fairly?

4. **Overreach Detection** — Compare the strength of claims in Results vs. Discussion vs.
   Abstract vs. Conclusion. Does the language escalate? (e.g., "suggests" in Results
   becomes "demonstrates" in the Abstract)

5. **Circular Reasoning Check** — Does any claim rest on itself? Does the paper cite its
   own prior work as independent evidence?

Output format: Write to 02_dimensions/reasoning_chain.md using the template from
references/templates.md. Flag items as [CRITICAL], [CONCERN], [NOTE], or [USER].
```

---

#### Agent 2: Data Quality

**File:** `02_dimensions/data_quality.md`

**Prompt template:**
```
You are the DATA QUALITY analyst in a comprehensive paper review team.

Paper: {title}
Your task: Evaluate the quality, rigor, and transparency of the data and methods.

Read the claim map (especially vision checks) and full paper text. Then analyze:

1. **Methods Reproducibility** — Could an independent researcher reproduce this work
   from the methods section alone? List what's missing: reagent concentrations,
   instrument settings, software versions, sample preparation details.

2. **Statistical Rigor** — Are statistical tests appropriate? Sample sizes adequate?
   Error bars/confidence intervals reported? P-values used correctly?
   Watch for: unreported multiple comparisons, inappropriate parametric tests on
   non-normal data, missing effect sizes.

3. **Controls Assessment** — Are positive and negative controls present? Are they
   appropriate? What controls are missing?

4. **Figure Integrity** — Review the vision analysis from the claim map. For any
   partial_mismatch or mismatch flags, investigate further:
   - Read the page renders to independently verify
   - Check if axis scales are appropriate or misleading
   - Check if image processing/contrast adjustments are documented

5. **Data Transparency** — Is raw data available? Code available? Are there
   supplementary materials referenced? Is the data sufficient to verify the claims?

6. **Internal Consistency** — Do numbers in the text match numbers in tables/figures?
   Cross-check ALL quantitative claims against their source data.

Output format: Write to 02_dimensions/data_quality.md using the template.
Flag items as [CRITICAL], [CONCERN], [NOTE], or [USER].
```

---

#### Agent 3: Claim–Evidence Alignment

**File:** `02_dimensions/claim_evidence.md`

**Prompt template:**
```
You are the CLAIM-EVIDENCE analyst in a comprehensive paper review team.

Paper: {title}
Your task: For every claim, evaluate whether the evidence actually supports it.

Read the claim map carefully. For EACH claim (especially novel and interpretive claims):

1. **Evidence Sufficiency** — Is there enough evidence? One data point is not sufficient
   for a general claim. A single experiment does not "demonstrate" — it "suggests."

2. **Evidence Type Match** — Is it the right KIND of evidence?
   - Correlation claimed as causation?
   - In vitro results extrapolated to in vivo?
   - Computational prediction presented as experimental finding?
   - Model system results generalized to the real system?

3. **Floating Claims** — Claims with NO evidence in the paper. These are assertions
   presented as findings. List them all.

4. **Strength Calibration** — For each novel claim, rate:
   - Language strength: 1 (hedged) to 5 (definitive)
   - Evidence strength: 1 (weak/absent) to 5 (strong/replicated)
   - MISMATCH if language > evidence by 2+ points

5. **Negative Results** — Are there results that don't support the narrative?
   Are they acknowledged or buried? Is there selective reporting?

Output as a per-claim verdict table:
| Claim ID | Claim (short) | Language (1-5) | Evidence (1-5) | Gap | Verdict |

Flag items as [CRITICAL], [CONCERN], [NOTE], or [USER].
Write to 02_dimensions/claim_evidence.md.
```

---

#### Agent 4: Domain Research

**File:** `02_dimensions/domain_context.md`

**Prompt template:**
```
You are the DOMAIN RESEARCH agent in a comprehensive paper review team.

Paper: {title}
Your task: Independent literature survey of the paper's domain. Do NOT rely on
training data — actively search.

Tools available (in order of preference):
- A paper-retrieval MCP if installed (e.g. `mcp__papers__search_papers`,
  `mcp__papers__get_paper_metadata`, `mcp__papers__get_citation_graph`,
  `mcp__papers__get_full_text`) — best signal, structured metadata.
- `WebSearch` and `WebFetch` — always-available fallback. Use these if no
  paper-retrieval MCP is configured, or to confirm/expand MCP results.

Execute the following research program:

1. **Domain Mapping** — Search for the paper's core topic using the paper-retrieval
   MCP if available, otherwise web search. Identify:
   - The 5-10 most important prior works in this specific sub-area
   - The current state of the art
   - Key open questions in the field
   - Recent developments (last 2 years)

2. **Coverage Analysis** — Compare your independently found literature against the
   paper's reference list:
   - Which key papers did the authors cite? (good coverage)
   - Which key papers did they MISS? (gaps)
   - Is the literature review biased toward certain groups or perspectives?

3. **Novelty Assessment Input** — Based on your survey:
   - Has this specific contribution been made before (even partially)?
   - Are there prior works that make similar claims with different evidence?
   - How does this work position itself relative to the actual state of the art?

4. **Context Brief** — Write a 500-word domain context brief that a reviewer
   would need to evaluate this paper properly.

5. **Local index check (optional)** — If the user maintains a local literature
   index or citation database (e.g. via a search MCP over their notes folder,
   or ripgrep over a structured library), query it for any of the cited papers
   or domain topics and report connections. Skip this step if no local index
   is configured.

Write to 02_dimensions/domain_context.md.
Flag missing key references as [CONCERN]. Flag potential prior art as [CRITICAL].
```

---

#### Agent 5: Structural Review

**File:** `02_dimensions/structural.md`

**Prompt template:**
```
You are the STRUCTURAL REVIEW agent in a comprehensive paper review team.

Paper: {title}
Your task: Evaluate the paper's structure, writing, and formal integrity.

Analyze:

1. **Abstract Accuracy** — Does the abstract faithfully represent the paper?
   Compare each claim in the abstract against the actual findings.
   Flag any overclaiming or omission of important caveats.

2. **Structure & Flow** — Does the paper follow logical structure for its type?
   Are sections proportionate? Is the narrative coherent?
   Does the introduction properly motivate the research question?

3. **Writing Quality** — Clarity, precision, ambiguity.
   Flag: vague language, undefined terms, inconsistent terminology,
   passive voice obscuring who did what.

4. **Figure/Table Integration** — Are all figures/tables referenced in text?
   Are they necessary? Are captions self-sufficient?
   Could any data be better presented (table → figure or vice versa)?

5. **Reporting Standards** — Check against applicable standards:
   - Chemistry: IUPAC nomenclature, experimental detail norms
   - Biology: ARRIVE, CONSORT, PRISMA as applicable
   - General: data availability statement, conflict of interest, funding

6. **Self-Consistency** — Terminology, notation, abbreviation consistency.
   Numbers matching across text, figures, tables, abstract.

Write to 02_dimensions/structural.md.
Flag items as [CRITICAL], [CONCERN], [NOTE], or [USER].
```

---

#### Agent 6: Novelty Assessment

**File:** `02_dimensions/novelty.md`

**Prompt template:**
```
You are the NOVELTY ASSESSMENT agent in a comprehensive paper review team.

Paper: {title}
Your task: Evaluate whether the claimed contributions are genuinely novel and significant.

You will receive the domain researcher's findings (02_dimensions/domain_context.md)
once available. If it's not ready yet, proceed with your own analysis and update later.

Analyze:

1. **Claimed Contributions** — List each contribution the authors explicitly claim.
   Where in the paper is each claim of novelty made?

2. **Novelty Evaluation** — For each claimed contribution:
   - Is it genuinely new? Or incremental extension of prior work?
   - Does it represent a new method, new finding, new interpretation, or new application?
   - Is the novelty in the result, the method, or the question?

3. **Significance Assessment** — Even if novel:
   - Does it advance understanding meaningfully?
   - Is the advance incremental or substantial?
   - Who benefits from this work? How broad is the impact?

4. **Overclaiming Check** — Compare:
   - What the abstract/conclusion claims as contribution
   - What the data actually shows
   - What prior work already established
   - Flag any inflation of significance

5. **Publishability Assessment** (relative to venue if known):
   - Is this level of contribution appropriate for the apparent target journal?
   - Are there fundamental issues that would prevent publication?

Write to 02_dimensions/novelty.md.
Flag items as [CRITICAL], [CONCERN], [NOTE], or [USER].
```

### 2.4 Flag Collection

After all agents complete, collect flags from:
1. Each `02_dimensions/*.md` file — grep for `[CRITICAL]`, `[CONCERN]`, `[NOTE]`, `[USER]`
2. Compile into `flags.md` at the review workspace root

```markdown
# Review Flags — {paper_title}

## [CRITICAL] — High-confidence issues
- {dimension}: {description} (from: {file}:{line})
...

## [USER] — Needs user input
- {dimension}: {description} (from: {file}:{line})
...

## [CONCERN] — Potential issues needing judgment
- {dimension}: {description} (from: {file}:{line})
...

## [NOTE] — Minor observations
...
```

### 2.5 Checkpoint 2

Present to user:

```
## Dimension Analysis Complete

### Critical Findings ({N} items)
{List each [CRITICAL] flag with one-line summary}

### Items Needing Your Input ({N} items)
{List each [USER] flag with the specific question}

### Concerns ({N} items)
{List each [CONCERN] flag with one-line summary}

### Dimension Summaries
- **Reasoning Chain:** {2-sentence summary from agent}
- **Data Quality:** {2-sentence summary from agent}
- **Claim–Evidence:** {2-sentence summary from agent}
- **Domain Context:** {2-sentence summary from agent}
- **Structural:** {2-sentence summary from agent}
- **Novelty:** {2-sentence summary from agent}

Proceed to reference verification? {N} references to scan, estimated {K} will need deep verification.
```

Resolve [USER] flags through dialogue. Then proceed.

---

## Phase 3: Reference Verification

### 3.1 Pass A — Metadata Scan

For **every** reference in `01_extraction/reference_catalog.md`:

**Step 1: Check reference cache**
```
Read reviews/reference_cache/index.md
If DOI or title matches a cached entry → load cached findings
```

**Step 2: Paper-retrieval MCP lookup** (for uncached refs, if a papers MCP is configured)
```
mcp__papers__search_papers(query="{author} {title} {year}")
mcp__papers__get_paper_metadata(paperId="{id}")
```
If no paper-retrieval MCP is available, skip directly to Step 3.

**Step 3: Web search** (always available; primary route if no MCP, fallback if MCP miss)
```
WebSearch("{author} {year} {title fragment}")
WebFetch("{doi_url}")  # for DOI resolution / abstract scraping
```

**Step 4: Abstract-level verification**
For each reference, compare:
- What the citing paper claims this reference says
- What the reference's abstract/metadata actually says
- Flag mismatches

Write results to `03_references/metadata_scan.md`:

```markdown
### REF-{NNN}: {author}, {year}

- **Status:** verified | not_found | metadata_only | cached
- **DOI verified:** yes | no | mismatch
- **Paper-retrieval MCP ID:** {id or "not used"}
- **Abstract available:** yes | no
- **Citation context match (abstract-level):**
  - Context 1: "{how the paper cites it}" → match | suspicious | mismatch
  - Context 2: ...
- **Cache hit:** yes (from review: {slug}) | no
- **Deep verification priority:** high | medium | low | skip
- **Priority reason:** {why}
```

### 3.2 Triage Protocol

Score each reference for deep verification priority:

**HIGH priority** (always verify):
- Supports a novel claim (from claim_map: type=novel + has this ref)
- Abstract-level check flagged suspicious or mismatch
- Used to justify a key methodological choice
- Domain researcher flagged as potentially miscited
- Is the user's own paper (if indicated at Checkpoint 1)

**MEDIUM priority** (verify if budget allows):
- Supports an interpretive claim
- Used in quantitative comparison ("our results are X% better than [ref]")
- Sole reference supporting any claim

**LOW priority** (skip unless flagged):
- Pure background/context citation
- Cited alongside 2+ other refs for the same point
- Well-known foundational reference (e.g., seminal methods papers)

**SKIP:**
- Cache hit with matching citation context and verdict=accurate
- Reference to standards or databases (not verifiable via paper-retrieval tooling)

### 3.3 Checkpoint 3

Present to user:

```
## Reference Verification Triage

**Total references:** {N}
**Cache hits (reused):** {K}
**Metadata scan results:**
- Verified & no issues: {N}
- Suspicious (abstract-level): {N}
- Not found: {N}

### High Priority — Deep Verification Recommended ({N} refs)
| # | Reference | Reason | Supporting Claim |
|---|-----------|--------|-----------------|
| 1 | Smith et al. 2024 | Supports CLAIM-003 (novel) | "Pore size is tunable across the 5–50 nm range" |
| 2 | Zhang et al. 2023 | Abstract mismatch | Methods justification |
...

### Medium Priority ({N} refs)
...

Estimated time for deep verification: ~{2-3 min per ref × N refs}.
Confirm which references to verify? (Default: all HIGH + flagged MEDIUM)
```

User may adjust scope. Proceed with confirmed list.

### 3.4 Pass B — Deep Verification

For each reference in the confirmed verification list, spawn a standalone agent (Agent tool, NOT the Phase 2 team — these are independent, focused tasks):

**Agent prompt:**
```
You are verifying whether reference [{ref_number}] in a paper review is cited accurately.

**The citing paper claims:**
{citation_context — the sentence(s) where this ref is cited, and what it's used to support}

**Reference to verify:**
Title: {title}
Authors: {authors}
Year: {year}
DOI: {doi}

**Your task:**
1. Get the full text. In order of preference:
   - If a paper-retrieval MCP is configured: `mcp__papers__get_full_text(paperId="{id}")`
   - `WebFetch("{doi_url}")` to resolve the DOI and read the publisher page
   - `WebSearch` for an open-access version (preprint server, author homepage, PMC)

2. Find the specific passages/findings that the citing paper references.
   Quote them directly.

3. Compare: Does the referenced paper ACTUALLY say what the citing paper claims?

4. Verdict — choose ONE:
   - **ACCURATE** — The citation fairly represents the referenced work
   - **DISTORTED** — The citation misrepresents, oversimplifies, or takes out of context
   - **UNSUPPORTED** — The referenced paper doesn't contain the claimed finding
   - **CONTRADICTED** — The referenced paper actually says the opposite

5. Write your findings to: 03_references/deep_verification/ref_{NNN}_{author_slug}.md

Use this format:
---
ref_number: {N}
title: "{title}"
authors: "{authors}"
year: {year}
doi: "{doi}"
verdict: accurate | distorted | unsupported | contradicted
confidence: high | medium | low
---

## Citation Context
{The exact sentence(s) in the citing paper where this ref appears}

## What the Citing Paper Claims This Reference Shows
{Extracted claim}

## What the Reference Actually Says
{Direct quotes from the reference, with section/page if available}

## Verdict Analysis
{Detailed comparison — what matches, what doesn't, and why}

## Impact on Review
{How this finding affects the paper's claims — which specific claims are weakened/invalidated}
```

Dispatch these agents in parallel (up to 5 concurrent).

### 3.5 Reference Cache Protocol

After deep verification completes, update the reference cache for future reuse:

For each newly verified reference:

1. Check if `reviews/reference_cache/{doi_slug}.md` exists
2. If new: create the cache entry
3. If exists: append to `verification_history`

**Cache entry format:**
```markdown
---
title: "{title}"
authors: "{first_author} et al."
year: {year}
doi: "{doi}"
journal: "{journal}"
papers_mcp_id: "{id}"
key_findings:
  - "{finding 1}"
  - "{finding 2}"
verification_history:
  - review: "{review_slug}"
    date: {YYYY-MM-DD}
    cited_as: "{how the citing paper used this ref}"
    verdict: accurate | distorted | unsupported | contradicted
    notes: "{specifics}"
last_verified: {YYYY-MM-DD}
---

## Abstract
{abstract text}

## Key Passages (verified content)
{Direct quotes that have been checked during verification}
```

Update `reviews/reference_cache/index.md`:
```markdown
- [{doi}] {author}, {year} — {short title} — last verified: {date}
```

---

## Phase 4: Synthesis & Output

**Executor:** You (orchestrator), single focused pass.

### 4.1 Cross-Dimensional Analysis

Read ALL artifacts:
- `01_extraction/claim_map.md`
- `02_dimensions/*.md` (all 6 dimension reports)
- `03_references/metadata_scan.md`
- `03_references/deep_verification/*.md` (all verification reports)
- `flags.md`

**Look for compound patterns** — individual findings that combine into larger issues:

| Pattern | Components | Severity |
|---------|-----------|----------|
| **Overclaiming cascade** | Strong language + weak evidence + miscited ref | CRITICAL |
| **Methodological gap** | Missing control + unsupported method claim + no replication | CRITICAL |
| **Selective narrative** | Cherry-picked data + ignored alternative explanations + biased lit review | CRITICAL |
| **Minor inflation** | Slightly strong language + adequate evidence | CONCERN |
| **Honest uncertainty** | Hedged language + acknowledged limitations | POSITIVE |

Write cross-dimensional findings to `04_synthesis/cross_findings.md`.

### 4.2 Final Report — `04_synthesis/REVIEW_REPORT.md`

Structure:

```markdown
# Review Report: {Paper Title}

**Authors:** {authors}
**Reviewed:** {date}
**Review scope:** {what was reviewed — full/partial, which refs verified}

---

## Executive Summary

{One paragraph: overall assessment, major strengths, major weaknesses, recommendation}

**Overall verdict:** {accept | minor_revision | major_revision | reject}
**Confidence in verdict:** {high | medium | low}

---

## Strengths
{Bulleted list of genuine strengths found during the review}

## Critical Issues
{Numbered list of [CRITICAL] findings with evidence}

## Major Concerns
{Numbered list of [CONCERN] findings with evidence}

---

## Detailed Findings by Dimension

### 1. Argument Architecture
{Summary from reasoning_chain.md — key findings, logic map reference}

### 2. Data Quality & Methods
{Summary from data_quality.md — reproducibility, stats, controls}

### 3. Claim–Evidence Alignment
{Include the verdict table from claim_evidence.md}
{Highlight the worst mismatches}

### 4. Domain Context & Literature
{Summary from domain_context.md — coverage gaps, missing refs}

### 5. Structural & Writing Quality
{Summary from structural.md — key issues only}

### 6. Novelty & Significance
{Summary from novelty.md — is the contribution what they claim?}

---

## Reference Integrity Report

**Total references checked:** {N}
**Deep-verified:** {K}

| Ref | Citation | Verdict | Impact |
|-----|----------|---------|--------|
| [1] | {context} | ACCURATE | — |
| [3] | {context} | DISTORTED | Weakens CLAIM-005 |
| [7] | {context} | UNSUPPORTED | Invalidates CLAIM-012 |
...

### Miscitation Details
{For each non-accurate verdict: what was claimed vs. what the ref actually says}

### Missing References
{Key papers the authors should have cited, from domain research}

---

## Cross-Dimensional Patterns
{Compound issues identified in 4.1}

---

## Recommendations for Authors
{Specific, actionable items — not vague "improve methods"}

1. {specific recommendation}
2. {specific recommendation}
...

---

## Review Metadata
- Review workspace: {path}
- Dimension reports: {list of files}
- Reference verifications: {list of files}
- Flags: {total by severity}
- Time elapsed: {approximate}
```

---

## Flag Taxonomy

Use these severity tags consistently across all phases:

| Tag | Meaning | Action |
|-----|---------|--------|
| `[CRITICAL]` | High-confidence error: unsupported claim, logical fallacy, data inconsistency, miscited reference | Must be in final report |
| `[CONCERN]` | Potential issue needing expert judgment — could be an error or a valid choice | Include in report with context |
| `[NOTE]` | Minor observation: style, clarity, formatting | Include only if pattern emerges |
| `[USER]` | Cannot resolve without domain expert input — blocks or qualifies a finding | Present at checkpoint, resolve before synthesis |
| `[POSITIVE]` | Genuine strength worth noting — good methodology, honest uncertainty, thorough controls | Include in Strengths section |

**Flagging format in dimension reports:**
```
[CRITICAL] Claim-007 states "demonstrates" but evidence is a single unreplicated experiment
with n=3 and no error bars. Strength-evidence gap: 4 vs 1.
```

---

## Workspace Directory Layout

```
reviews/{paper_slug}_{timestamp}/
├── 00_source/
│   ├── {original_file}          # PDF or DOCX copy
│   ├── parsed_text.md           # Normalized text
│   ├── metadata.json            # Extraction metadata
│   ├── figures/                 # Extracted embedded images
│   │   ├── figure_001.png
│   │   └── ...
│   ├── pages/                   # Full-page renders (PDF only)
│   │   ├── page_001.png
│   │   └── ...
│   └── tables/                  # Extracted tables as markdown (DOCX)
├── 01_extraction/
│   ├── claim_map.md             # All claims with evidence pointers + vision checks
│   └── reference_catalog.md     # All references with citation contexts
├── 02_dimensions/
│   ├── reasoning_chain.md       # Argument architecture analysis
│   ├── data_quality.md          # Methods, stats, controls, figures
│   ├── claim_evidence.md        # Per-claim evidence verdict table
│   ├── domain_context.md        # Independent lit survey + coverage analysis
│   ├── structural.md            # Format, writing, reporting standards
│   └── novelty.md               # Contribution evaluation
├── 03_references/
│   ├── metadata_scan.md         # Pass A results for all refs
│   ├── triage.md                # Prioritized list for deep verification
│   └── deep_verification/       # Pass B results
│       ├── ref_001_smith2024.md
│       └── ...
├── 04_synthesis/
│   ├── cross_findings.md        # Cross-dimensional patterns
│   └── REVIEW_REPORT.md         # Final aggregated review
└── flags.md                     # All flags across all phases

reviews/reference_cache/
├── index.md                     # DOI → file lookup
└── {doi_slug}.md                # Cached verification data per reference
```

---

## Error Handling

- **Ingestion failure:** If PDF/DOCX parsing fails, report the error and ask the user for an alternative format.
- **Paper-retrieval MCP unavailable:** Fall back to `WebSearch` + `WebFetch` for reference metadata. Note reduced verification confidence in the report.
- **Full text unavailable:** For Pass B, if no full text can be obtained, report this honestly. Do not guess. Mark verification as `confidence: low` and note the limitation.
- **Agent failure:** If a dimension agent fails, report which dimension was not analyzed. Offer to retry or skip.
