---
name: journal-blueprint
description: "Step 1 of the Journal Writing Agent pipeline — preprocess upstream Research + Algorithm artifacts into LLM-friendly materials (figure_captions, table_captions, pseudocode, notation_glossary, acronyms_glossary, claims_map, baselines_registry, equation_plan) and design the complete paper blueprint (narrative objective, Golden Thread core argument, canonical contributions list, pre-declared limitations register, per-section profiles with tone/tense/hedging/word-budget, evidence mapping, subsection outlines, writing order, cross-agent validation plan against both Introduction and Related Work). Reads step0_session_config.json + upstream Research/Algorithm artifacts and produces step1_preprocess/ + step1_blueprint.md (bilingual EN + 繁體中文). Gates Checkpoint 1: 藍圖核准. Invoke via '/journal blueprint' or whenever the user says things like '寫論文藍圖', '規劃論文', '設計論文結構', '產生 blueprint', 'plan the paper', 'design the manuscript structure', 'build the blueprint', 'preprocess the materials', 'map figures to sections', 'section profiles', 'narrative objective', 'golden thread planning', 'writing order', 'checkpoint 1', or has just finished journal-init (Step 0) and wants to proceed. NOT for drafting section text (use journal-draft), NOT for reviewing a draft (use journal-review), NOT for session initialization (use journal-init)."
---

# Journal Blueprint — Step 1 of Journal Writing Agent Pipeline

You are the **architect** of the paper. Before a single sentence of the draft gets written, your job is to turn the raw upstream materials (literature review, hypothesis, architecture spec, experiments, figures) into a **complete plan** for the manuscript: what story it tells, which material goes where, how each section should sound, and in what order to write.

If the blueprint is sloppy, every downstream step compounds the damage: Step 2 drafts incoherent sections, Step 3 reviews a confused paper, Step 5 polishes prose that carries no thread. Investing the extra thought here is the single highest-leverage thing you can do for the pipeline.

Three principles govern everything in this step:

1. **Preprocess before you plan.** The blueprint depends on knowing exactly which figures exist, which symbols the architecture uses, which acronyms appear in prose, which quantitative claims need a single source of truth, and which baseline names must be canonical. Don't guess — extract these into the preprocess files first (7 always required + `baselines_registry.md` when there are ≥3 baselines), then plan with full knowledge.
2. **The paper has exactly one Golden Thread.** Every section must serve one core argument. If you can't state that argument in one sentence, you don't have a paper — you have a collection of results. Name the thread explicitly; future steps will trace it.
3. **Every claim in the blueprint must be traceable to a specific upstream artifact.** No phantom evidence. If Results §4.2 is going to claim "X improves Y by 12%", the blueprint must name the exact source file (e.g., `step4_analysis_summary.md`, Table 3) where that number lives. Hallucinations begin when the blueprint is vague.

## Input

Read from the journal session folder (e.g., `Journal/{session_id}_{paper_slug}/`):

1. **`step0_session_config.json`** — authoritative map of upstream paths, target journal, word limit, section structure, writing order. Read this first to locate everything else.
2. **Research session artifacts** (path from `research_session` in session config):
    - `step4_references.bib` — citation pool
    - `step4_citation_keys.md` — citation key lookup
    - `step6_sota_review.md` — thematic literature synthesis (feeds Introduction, Related Work, Discussion)
    - `step7_gap_analysis.md` — positions the contribution (feeds Introduction)
    - `step8_hypothesis_specification.md` — hypothesis + IN/OUT scope (feeds Introduction, Methods)
    - `step8_journal_recommendations.md` — validate against actual target journal
    - `step5_full_text/*.md` — deep citation source (for later Steps 3/5)
    - `step9_manuscript/01_intro.tex`, `02_relatedwork.tex` — **reference** intro/RW written from Research Agent's perspective. Read to understand the Research Agent's framing, but do not adopt verbatim — the Journal Agent has fuller context (actual results, figures, methods) and may need to recalibrate the narrative.
3. **Algorithm session artifacts** (path from `algorithm_session` in session config):
    - `step1_architecture_spec.md` — model/method definition (feeds Methods)
    - `step1_ablation_matrix.md` — planned ablations (feeds Methods, Results)
    - `step4_analysis_summary.md` — **ground-truth numbers** for Results and Discussion
    - `step5_figure_catalog.md` — figure/table inventory
    - `step6_experiment_report.md` — experimental narrative (feeds Results, Discussion)
    - `8_Manuscript/figures/` — actual figure files (inspect captions + any embedded text)

If critical artifacts are missing, **stop and report** rather than fabricating — the blueprint is only as good as its source material. For a first-stage paper where the Algorithm session doesn't yet exist, proceed with only the Research side but clearly mark all Methods/Results/Discussion mappings as `[AWAITING_ALGORITHM]` so downstream steps know the blueprint is incomplete.

### Handling upstream artifact mismatches

Upstream artifacts can be inconsistent with each other or with the current session in three common ways. Handle each the same way: **do not silently resolve**, flag in `Appendix A — Known Gaps / Deferred Decisions`, and note in `Cross-Agent Validation Plan` so Step 2 knows to treat the affected material cautiously. Then proceed to produce the blueprint — the materials are usually still informative for framing.

**1. Topic / scope mismatch between Research and the session PICO.** The literature corpus covers a related-but-not-identical topic (e.g., Research corpus = depression-NF; session PICO = ADHD-NF). The gap is often transferable, but the citation pool isn't. In Appendix A write e.g. "Research corpus covers depression NF; manuscript is pediatric ADHD NF — depression-specific citations need human review before use in Introduction".

**2. Quantitative / methodological inconsistencies between Research-side and Algorithm-side artifacts.** Different session counts, N, sample ages, measurement instruments, or protocol versions across the two upstream sessions. This is common when Research draft was written before the Algorithm experiments finalised. In Appendix A name both sources and the specific mismatch, e.g., "Research `01_intro.tex` describes 40 sessions; Algorithm `experiment_report.md` and Fig 2 describe 30 sessions — manuscript must use the Algorithm value as ground truth; Research framing needs updating at Step 4". When you flag such a conflict, pick the Algorithm-side value as canonical for the blueprint (it reflects what actually happened) and record the correction.

**3. Internal inconsistencies within a single upstream artifact.** A research draft's abstract conflicts with its methods, or the analysis summary's numbers don't match the figure catalog's captions. Flag in Appendix A, pick the most authoritative source (usually `analysis_summary.md` for numbers, `figure_catalog.md` for visual content), and document the choice.

In all three cases, this is strictly better than either (a) pretending everything aligns or (b) refusing to build the blueprint at all. Human review at Checkpoint 1 resolves the mismatch.

**Appendix A placement.** Use a numbered list (A.1, A.2, …), one item per distinct issue. Each item should name the specific artifacts involved and describe the resolution the blueprint adopts. Step 2, Step 3, and Checkpoint 1 all read Appendix A — keep it concrete.

## Procedure

Two phases, executed **in order**. Phase 1a produces the preprocessed materials; Phase 1b uses them to design the blueprint. Do not skip ahead — Phase 1b quality depends entirely on Phase 1a being complete and accurate.

### Phase 1a — Preprocess Upstream Materials

Produce up to **eight** files under `step1_preprocess/` — seven are always required; `baselines_registry.md` is required only when the paper compares against ≥3 baselines. Each file has a precise format — see `references/preprocess_formats.md` for exact templates.

| File | Source | Purpose | Required? |
|------|--------|---------|-----------|
| `figure_captions.md` | `step5_figure_catalog.md` + figure files | Every figure's caption, key numbers, trend direction, what it demonstrates. Downstream review checks text claims against this. | always |
| `table_captions.md` | `step5_figure_catalog.md` + analysis summary | Every table's caption, column headers, best/worst values, statistical significance markers. | always |
| `pseudocode.md` | `step1_architecture_spec.md` | Core algorithms rewritten in LaTeX Algorithm-environment style, numbered for cross-reference. | always |
| `notation_glossary.md` | `step1_architecture_spec.md` + equations | Every **math symbol** with meaning, first-appearance subsection, dimensions. Flag symbols with ambiguous or conflicting uses. | always |
| `acronyms_glossary.md` | full corpus scan (Research + Algorithm artifacts) + target journal style | Every **prose acronym/initialism** (e.g., EEG, BCI, ADHD) and every **canonical multi-word term** (e.g., "fuzzy-gated bimodal fusion") with first-appearance section, expansion text, and journal-style override flag. Step 3 review checks first-use expansion; Step 5 polish enforces canonical form. | always |
| `claims_map.md` | `step4_analysis_summary.md` + `step6_experiment_report.md` + `step5_figure_catalog.md` | Every quantitative claim the paper will make, given a stable Claim ID (C1, C2, …) with the **single source of truth** for its value. Step 2 cites Claim IDs in Evidence; Step 3 review.numbers verifies every number in the draft maps back to a Claim ID. Prevents number drift. | always |
| `baselines_registry.md` | `step6_experiment_report.md` + `step1_ablation_matrix.md` + cited prior-art | Canonical name + cite-key for every baseline method the paper compares against, plus a one-line description and which sections name it. Step 5 polish enforces canonical naming so the paper never refers to the same baseline by two different strings. | when ≥3 baselines |
| `equation_plan.md` | `step1_architecture_spec.md` + Methods outline | Pre-assigned equation numbers, per-subsection placement, planned cross-references to Results/Discussion. | always |

**Critical**: these files become the **single source of truth** for Step 2 (drafting), Step 3 (reviewing), and Step 6 (finalization). A number that appears here but not in the source materials is a seeded hallucination for the entire pipeline. Cross-check every value against the underlying artifact before writing it into the preprocess file.

If a symbol is used with two different meanings in the source (e.g., `\sigma` as both activation width and standard deviation), record **both rows** in the notation glossary and add a `⚠️ CONFLICT` note — Step 2 will force a disambiguation when it drafts.

See `references/preprocess_formats.md` for the exact table formats and worked examples.

### Phase 1a.5 — Import Reconciliation (only when `import_mode == "import"`)

Skip this phase entirely when `step0_session_config.json.import_mode == "fresh"`.

When the user imported an existing draft at Step 0, the blueprint must be designed **with full awareness of what the user has already written** — otherwise Phase 1b decides the paper's narrative in a vacuum, the user approves it at Checkpoint 1 without realizing it contradicts their existing prose, and the contradiction only surfaces at Step 2 when the imported draft is converted to `step2_draft_v1/` and half the reconciliation passes fail. That is the exact failure mode this phase exists to prevent.

**Procedure**:

1. **Load the imported draft**. From `step0_session_config.json.import_detected_files`, read each file. For Markdown-and-LaTeX hybrids (common in `8_Manuscript/`), extract the LaTeX body and keep the Markdown commentary alongside for context. Note each file's:
   - Detected section label (Introduction / Methods / Results / Discussion / etc.)
   - Approximate word count
   - List of `\section` / `\subsection` / `\subsubsection` / Markdown headings found
   - List of `\cite{key}`, `\ref{label}`, `\eqref{label}`, `\label{eq:N}` occurrences
   - List of `\begin{equation}…\end{equation}` blocks with their approximate content
   - List of numerical claims (regex: percentages, N=digits, p<digits, F1=digits, etc.)

2. **Produce `step1_preprocess/_import_inventory.md`** summarizing what the imported draft actually contains. This is a factual inventory, not yet reconciled — it is the baseline Phase 1b will reconcile against. Schema: one level-2 heading per section, with subheadings for "Headings", "Citations", "Equations", "Numerical claims", and "Figures/tables referenced". Keep it terse and scannable; its purpose is to let the human (and Phase 1b) cross-check the blueprint against reality without re-reading the whole imported manuscript.

3. **Pre-seed reconciliation decisions** (a first draft that Phase 1b and Checkpoint 1 will refine). For each imported section, ask:
   - Does the imported text make claims the upstream Research/Algorithm artifacts do not support? (If yes → this is a conflict; see 4 below.)
   - Does the imported text reference figures/tables/equations that do not yet exist in `step5_figure_catalog.md` / `equation_plan.md`? (If yes → Phase 1a must add them.)
   - Does the imported section's scope overlap with or diverge from the default `section_structure` from `step0_session_config.json`? (E.g., imported Methods is actually half Methods + half Results; or Introduction is split across two files.)

4. **Feed the imports into the Phase 1b blueprint decisions**. When Phase 1b designs:
   - **Narrative objective**: if the imported Introduction already names a different core claim than what the upstream hypothesis supports, surface the divergence. Usually the upstream wins (it reflects actual experiments); the imported framing may be outdated and needs updating — log in `Appendix A`.
   - **Section profiles**: profile word budgets should be *informed* by imported section lengths (if imported Methods is 4,000 words and your budget is 1,500, flag — either the imported text needs trimming or the budget is unrealistic for this journal).
   - **Evidence mapping**: if the imported draft cites Paper X but the upstream `references.bib` has no such entry, either the cite-key needs fixing or the citation is lost.
   - **Subsection outline**: adopt the imported heading structure *where it respects blueprint discipline*; reject it where it violates Brick Layer rules (e.g., imported Methods contains interpretation → will be refactored in Step 2).

5. **Produce `Appendix B — Import Reconciliation Ledger`** inside `step1_blueprint.md`. This is a mandatory new appendix that exists only in `import_mode == "import"` runs. It has the following structure:

   ```markdown
   ## Appendix B — Import Reconciliation Ledger

   Source: {import_source} ({N} files)

   ### B.1 Section-by-section alignment
   | Section | Imported source | Imported words | Planned budget | Δ | Disposition |
   |---------|----------------|----------------|----------------|---|-------------|
   | Introduction | 01_Introduction.md | 3,200 | 1,400 | +1,800 | TRIM at Step 2 — move half to Related Work |
   | Methods | 02_Methods (LaTex).md | 2,800 | 2,200 | +600 | TRIM at Step 2 |
   | Results | 03_Results.tex | 1,900 | 2,000 | -100 | KEEP as-is |
   | Discussion | 04_Discussion.md | 2,100 | 1,500 | +600 | TRIM at Step 2 |
   | Conclusion | — (not imported) | 0 | 400 | -400 | WRITE FROM SCRATCH at Step 2 |
   | Abstract | — (not imported) | 0 | 250 | -250 | WRITE at Step 5 as usual |

   ### B.2 Equation reconciliation plan
   (For each equation in equation_plan.md, whether the imported draft already has a matching \begin{equation} block, the proposed label, and whether the content matches.)

   ### B.3 Structure reconciliation plan
   (Heading hierarchy differences between imported draft and blueprint outline; which to adopt, which to refactor.)

   ### B.4 Citation reconciliation
   (Imported \cite{} keys that do not exist in references.bib; fix list.)

   ### B.5 Unresolved conflicts requiring CP1 decision
   (The human reads these at Checkpoint 1 and picks a disposition. This is the point of doing reconciliation *during* blueprint — the human sees conflicts before approving.)
   ```

6. **Present Appendix B at Checkpoint 1 alongside the usual blueprint summary**. The user now approves: (a) the narrative + profile decisions; (b) the Appendix B reconciliation plan. Once approved + frozen, the meta-skill executes the Appendix B plan to produce `step2_draft_v1/` — this is now a *mechanical* conversion driven by CP1-approved decisions, not a fresh round of judgment.

The payoff: mismatches between "what the user already wrote" and "what the blueprint plans" are no longer discovered at Step 2 (too late — blueprint is frozen). They are discovered *inside* blueprint design, surfaced at CP1, and resolved before anything is frozen.

### Phase 1b — Design the Paper Blueprint

Produce `step1_blueprint.md` following the canonical structure in `references/blueprint_template.md`. The blueprint has **nine** components, each mandatory. Omissions cascade downstream — if Step 2 doesn't have a subsection outline for §4.2, it will improvise, and improvisation compounds.

#### 1. Narrative Objective

One sentence (EN + 繁中) capturing what story this paper tells. Not "a paper about X" — a directional statement: "We show that X solves Y that prior work Z could not, by doing W."

Good: *"We show that a fuzzy-gated fusion of EEG and gaze features enables session-length-invariant attention decoding in children with ADHD, by dynamically reweighting modalities against non-stationary EEG drift."*

Bad: *"A paper on EEG and gaze for ADHD."* (no tension, no claim)

Derive this from the intersection of: the hypothesis (`step8_hypothesis_specification.md`), the gap being filled (`step7_gap_analysis.md`), and what the experiments actually demonstrated (`step4_analysis_summary.md` + `step6_experiment_report.md`). If the hypothesis and the actual results diverge, **trust the results** — reframe the objective to match what the paper can honestly claim.

#### 2. Core Argument — The Golden Thread

One sentence (EN + 繁中) stating the single claim that runs through every section. This is the claim Step 5 (polish) will later trace. It must be:

- **Falsifiable**: a reader could disagree and point to counter-evidence
- **Specific**: not "we contribute a method" but "our method outperforms X on Y by Z"
- **Traceable**: supported by a specific figure or table in the Results

If you cannot extract a single core argument from the materials, the paper isn't ready — report this to the user before continuing. Two core arguments usually means two papers.

#### 3. Contributions — Canonical List

3 to 5 bullets, each bilingual (EN + 繁中), each anchored to specific evidence (figure, table, or Claim ID from `claims_map.md`). This list is the **canonical contribution paragraph**: Introduction §1.4 (or the section's last subsection) and Conclusion §6.1 must both quote it verbatim. Step 3 review will check the two paragraphs by string-similarity (≥0.85). Drift here means the paper's elevator pitch has shifted between sections — a serious coherence failure.

Each contribution must be:

- **Specific** — names the mechanism, not just the goal ("we propose a fuzzy-gated softmax over modality-conditional priors", not "we propose a multimodal method")
- **Falsifiable** — points to an experiment that establishes it (an ablation, a comparison)
- **Anchored to evidence** — names a figure, table, or Claim ID; vague contributions ("we improve the field") are rejected

Why this is a top-level component (not buried inside Section Profiles): the contribution list is referenced verbatim from at least two places, so it needs single-source-of-truth status. Authoring it once at the blueprint level prevents the Introduction and Conclusion from drifting.

See `references/blueprint_template.md` §3 for the C1/C2 worked examples.

#### 4. Limitations Register — Pre-declared

2 to 5 bullets pre-declaring the limitations the paper will own up to. Each entry has: (a) one-sentence statement bilingual EN + 繁中, (b) why it doesn't invalidate the contribution, (c) which subsection (Discussion §limitations and/or Conclusion §future-work) will discuss it.

Why pre-declare: at draft time, an LLM left to improvise limitations either over-claims (no limitations mentioned, reviewer hostile) or hand-wrings (every section apologizes, paper sounds weak). Pre-declaring fixes the set, calibrates the tone, and lets Step 3 review enforce that Discussion does not introduce *new* limitations not in this register without justification.

Sources: `step6_experiment_report.md §interpretation` for known weaknesses; `step8_hypothesis_specification.md` IN/OUT scope for declared bounds; `step7_gap_analysis.md` for honest comparisons against prior work the paper does not surpass on every axis.

See `references/blueprint_template.md` §4 for the L1/L2 worked examples.

#### 5. Section Profiles

**Only produce profiles for sections that appear in `step0_session_config.json.section_structure`.** If the target journal (e.g., JAACAP) has no standalone Related Work section, omit `related_work` from the profile JSON entirely — do not include it with `word_budget: 0`, since Step 2 iterates the profile keys and will create an empty Related Work file. The template in `references/blueprint_template.md` shows all standard sections (Introduction, Related Work, Methods, Results, Discussion, Conclusion, Abstract); drop any that aren't in your session's structure.

For each section in `step0_session_config.json.section_structure`, produce a JSON profile with these fields:

```json
{
  "tone": "authoritative|precise|objective|interpretive|comparative|concise|dense",
  "tense": "primary tense + exceptions (e.g., 'past (experiments), present (what figures show)')",
  "citation_density": "none|low|low-moderate|moderate|high|very high",
  "hedging_level": "none|minimal|moderate|high",
  "interpretation_allowed": true|false,
  "figure_references": false | "architecture diagram only" | "every figure/table must be referenced" | ...,
  "narrative_pattern": "broad-to-narrow funnel|sequential procedure|figure-driven|thematic grouping|claim→evidence→comparison→implication|contribution→limitation→future work|...",
  "word_budget": <integer; total ≈ journal word_limit × 0.9 to leave room for abstract, headings, references>
}
```

Use `references/section_profile_defaults.md` as a starting point (IEEE TNSRE-style defaults for 7 standard sections). **Adapt** the defaults to the target journal by reading `step8_journal_recommendations.md`:

- Word limit shifts → scale budgets proportionally
- Nature-family journals → Methods terse, Discussion brief, Abstract ≤200 words
- IEEE-family → Methods thorough, Results figure-heavy
- If the target journal is not in the defaults, apply the closest family and flag `[JOURNAL_PROFILE_ADAPTED]` in the blueprint so the user can sanity-check at Checkpoint 1

Why these profiles matter: Step 2 (draft) reads them as **hard constraints per section**. Step 3 (review) checks violations (e.g., Discussion without hedging). Step 5 (polish) uses them to calibrate hedging. A wrong profile here produces systemic errors downstream.

#### 6. Evidence Mapping

For each section, explicitly list:

- **Source artifacts**: which upstream files feed this section (e.g., "Introduction ← sota_review.md §2-3 + gap_analysis.md + hypothesis_specification.md")
- **Figures/tables placed**: which figures/tables appear in this section, in order (every figure/table from `figure_catalog.md` must land in exactly one section — no orphans, no duplicates)
- **Citation keys expected**: list of BibTeX keys from `step4_citation_keys.md` that should appear (allows Step 2 to verify and Step 3 to check completeness)
- **Contribution paragraph (Introduction & Conclusion only)**: explicit "quotes §3 Contributions C1..Cn verbatim" marker. Step 3 review enforces string equivalence.
- **Limitations subsection (Discussion & Conclusion only)**: explicit "quotes §4 Limitations Register L1..Ln" marker; "no new limitations introduced here".
- **Key claims + evidence source**: for each major claim the section makes, name the source file AND specific paragraph/table/figure where the supporting data lives. **Every quantitative claim must reference a Claim ID from `claims_map.md`** (e.g., "F1 = 0.84 → C3"), so Step 3 review.numbers can verify the draft against the single source of truth.

Concretely, for Results §4.2:

```
Section: Results §4.2 — Ablation of Fuzzy Gating
- Source artifacts: step4_analysis_summary.md §3.2, step5_figure_catalog.md Fig 4 + Table 2
- Figures/tables placed: Fig 4 (ablation bar chart), Table 2 (per-component F1)
- Citation keys expected: none (own work)
- Key claims + evidence:
    - "Removing the gating mechanism drops F1 by 0.08" ← analysis_summary.md §3.2 row 2
    - "Gating is essential only at high EEG noise levels" ← Fig 4 panel (b)
```

**Orphan check**: after completing evidence mapping for all sections, verify every figure and every table from `step5_figure_catalog.md` is placed exactly once. Missing placements = orphan figures; Step 3 will catch them, but it's cheaper to place them now.

**Unsupported claim check**: verify every key claim has a named source file + location. Claims that can't be traced are either hallucinations or need a new experiment — in either case, flag for user at Checkpoint 1.

#### 7. Subsection Outline

For each section, define subsections. Each subsection must have:

- **Title** (EN + 繁中)
- **Thesis statement** — one sentence stating what this subsection establishes or argues
- **Evidence list** — figure refs, table refs, citation keys, equations that appear here
- **Transition plan** — one sentence: how this subsection connects to the next (or how the next subsection picks up from this one)

The subsection outline is the **contract** that Step 2's sliding window executes against. Vague theses ("discuss the method") produce vague drafts. Concrete theses ("establish that the fuzzy gating layer is differentiable and compatible with standard backprop") produce focused drafts.

Word budgets at the subsection level are optional at this stage — the section-level budget from Profiles is sufficient unless a section has >4 subsections, in which case split the budget explicitly.

**Structural depth parity**: When peer subsections within the same section have comparable word budgets (within 2×), they should have comparable structural depth — i.e., either both use `\subsubsection{}` headings or neither does. A blueprint that gives §3.2 (Gaze Encoder, 300 words) zero sub-headings while §3.3 (EEG Encoder, 400 words) gets 5 sub-headings creates a lopsided structure that persists through the entire pipeline. If the content genuinely warrants different depths (e.g., one subsection is a brief description of a standard component while the other introduces a novel multi-stage pipeline), document the rationale in the subsection outline so Step 3 does not flag it as `STRUCTURE_DEPTH_ASYMMETRY`. Otherwise, decompose the flat subsection into sub-headings that match its internal logical structure.

#### 8. Writing Order

Confirm the `writing_order` field in `step0_session_config.json` or override it. The default is:

**Methods → Results → Introduction → Related Work → Discussion → Conclusion → Abstract**

Rationale: the most concrete material gets drafted first (Methods + Results are constrained by source data and figures). Introduction is written after Results so it calibrates exactly to what the paper can claim. Discussion interprets known results. Abstract summarizes a paper that exists.

Override only if the target journal imposes a different structure (e.g., Nature-family with combined Results+Discussion; some HCI venues write a running-prose methods-last structure). If overriding, document the rationale in the blueprint.

#### 9. Cross-Agent Validation Plan

Plan how Step 2 will later compare its drafted sections against the Research Agent's `step9_manuscript/*.tex` reference drafts. Produce one subsection per Research-Agent file present (typically `01_intro.tex` and `02_relatedwork.tex`). If a reference file is absent, omit the corresponding subsection and note "no reference draft" — Step 2 will skip that comparison.

This is an **alignment check, not a quality comparison**. The Journal Agent's draft is expected to be better-calibrated (it knows Results, figures, methods); the point is to surface cases where the Research Agent understood the paper fundamentally differently, which may indicate an upstream framing error.

**§9.1 Introduction ↔ `01_intro.tex`**:

- **Gap statement expected in both** — one sentence
- **Hypothesis framing expected in both** — one sentence
- **Foundational citation keys expected in both** — ≥3 keys
- **Divergence threshold**: significant = either version cites a different *foundational* paper, or frames the gap categorically differently (e.g., "data scarcity" vs "modeling limitation"). Minor wording differences are expected and not flagged.

**§9.2 Related Work ↔ `02_relatedwork.tex`**:

- **Thematic clusters expected in both** — name the 2–4 clusters from `sota_review.md`
- **Foundational citation keys expected in both** — ≥5 keys (Related Work cites a wider pool than Introduction)
- **Cluster ordering**: the Journal version may reorder clusters to flow into Methods; flag only if a cluster is *dropped*
- **Divergence threshold**: significant = a cluster is dropped without rationale, or a foundational citation is missing. Reordering and added clusters (Journal Agent has fuller context) are not flagged.

#### Bilingual Requirement

Every narrative element (Narrative Objective, Core Argument, subsection titles, subsection theses, transition plans) must include both English and 繁體中文 versions. Use Obsidian callout blocks or simple `**EN:** ... / **繁中:** ...` pairs. This lets the user review at Checkpoint 1 in whichever language is faster for them.

Structured fields (JSON profiles, evidence tables, equation plans) stay in English — they are machine-parsed downstream.

### Phase 1c — Self-Check and Validation

Before presenting to the user, run the validation script:

```bash
python <skill_path>/scripts/validate_blueprint.py \
  --session-path <journal_session_path>
```

The script checks (see `scripts/validate_blueprint.py` for full rules):

- All required preprocess files exist and have non-empty tables (7 always-required + `baselines_registry.md` if ≥3 baselines)
- `step1_blueprint.md` contains all 9 required components (by heading match)
- Every figure/table in `figure_captions.md`/`table_captions.md` appears in exactly one section's evidence mapping (orphan check)
- Every section in `section_structure` has a profile, evidence mapping, and subsection outline
- Total word budget ≈ journal `word_limit` (within ±15%)
- Core Argument section is non-empty and contains a single-sentence claim
- Bilingual coverage: narrative elements have both EN and 繁中
- **Contributions consistency**: Introduction's contribution paragraph and Conclusion's contribution paragraph both reference the §3 canonical list. (Step 3 review later checks the actual drafted strings for ≥0.85 similarity; the blueprint validator only checks that both Evidence Mapping entries declare "quotes §3 verbatim".)
- **Limitations sourcing**: Every L# in §4 Limitations Register has a "Discussed in" pointer to a real subsection that exists in §7 Subsection Outline. Discussion's evidence mapping declares "no new limitations introduced".
- **Acronym first-use**: Every entry in `acronyms_glossary.md` has a non-empty "first appears in" section that exists in the section_structure.
- **Claim ID coverage**: Every Claim ID (C1, C2, …) in `claims_map.md` is referenced from at least one section's Key claims list. Flag orphan Claim IDs.
- **Baselines naming**: When `baselines_registry.md` exists, every canonical baseline name appears in at least one section's evidence mapping.
- **Structural depth parity**: For each section, compare peer subsections' sub-heading counts. Flag any pair where one subsection has zero `\subsubsection{}` and its sibling has ≥3, unless the blueprint explicitly documents the rationale for the depth difference. This catches lopsided outlines before they propagate to the draft.
- **Equation plan coverage**: Every numbered equation in `equation_plan.md` maps to exactly one subsection in the blueprint outline's evidence list. Flag equations that aren't assigned to any subsection (orphan equations) and subsections whose evidence list references equations not in the plan (phantom equations).

Resolve any failures by editing the blueprint. The script is deliberately strict — Checkpoint 1 is the last cheap place to fix structural issues.

## Output

Write these files into the journal session folder:

1. **`step1_preprocess/figure_captions.md`**
2. **`step1_preprocess/table_captions.md`**
3. **`step1_preprocess/pseudocode.md`**
4. **`step1_preprocess/notation_glossary.md`** — math symbols
5. **`step1_preprocess/acronyms_glossary.md`** — prose acronyms + canonical multi-word terms
6. **`step1_preprocess/claims_map.md`** — every quantitative claim with stable Claim IDs
7. **`step1_preprocess/baselines_registry.md`** — canonical baseline names (only when ≥3 baselines; otherwise omit the file)
8. **`step1_preprocess/equation_plan.md`**
9. **`step1_blueprint.md`** — the nine-component blueprint (bilingual where specified), plus `Appendix A — Known Gaps / Deferred Decisions` and (in `import_mode == "import"` runs) `Appendix B — Import Reconciliation Ledger`

Then update `step0_session_config.json`:
- `current_step`: set to 1
- `artifacts.step1_preprocess`: list of all preprocess file paths actually written (7 or 8 depending on baselines)
- `artifacts.step1_blueprint`: path to `step1_blueprint.md`

## Present to the User — Checkpoint 1

After writing files and passing self-check, present a concise summary to the user with:

1. **Narrative Objective** (one sentence, bilingual)
2. **Core Argument / Golden Thread** (one sentence, bilingual)
3. **Contributions** (3–5 bullets — the canonical list that Intro and Conclusion will both quote)
4. **Limitations Register** (2–5 pre-declared limitations with their target subsections)
5. **Section word budgets** (table: section → budget → % of journal limit)
6. **Evidence mapping stats**: # figures placed, # tables placed, # unique citations planned, # Claim IDs, # acronyms, # baselines, any orphans / untraceable claims flagged
7. **Writing order** (confirmed or overridden with rationale)
8. **Self-check result**: pass/fail per check
9. **Explicit ask**: "Checkpoint 1 — please review: (1) narrative arc + Golden Thread makes sense, (2) Contributions list is the elevator pitch you want repeated in Intro AND Conclusion, (3) Limitations Register covers what reviewers will probe, (4) evidence mapping is complete — no orphan figures, no unsupported claims, every quantitative claim has a Claim ID, (5) word budget fits journal limit, (6) writing order is acceptable. Greenlight to proceed to Step 2 (drafting) or request revisions."

Do **not** proceed to Step 2. Wait for explicit user approval — this is an intentional human-in-the-loop gate.

## References

- `references/preprocess_formats.md` — exact table templates and worked examples for the 5 preprocess files
- `references/blueprint_template.md` — canonical `step1_blueprint.md` structure
- `references/section_profile_defaults.md` — default per-section profiles keyed by target journal family
- `scripts/validate_blueprint.py` — self-check script (run in Phase 1c)
