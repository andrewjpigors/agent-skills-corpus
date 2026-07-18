---
name: builder-foundation
description: Shared quality framework inherited by ALL builder skills. Defines the Mid-Draft Quality Check, Quality Dimensions scoring, Refine-or-Pivot decision, weakness-weighted review tiers, and optional document evaluator integration. Builder skills reference this instead of duplicating quality logic.
tools-needed: file read/write
---

# Builder Foundation

## Purpose

This is NOT a standalone skill. It is a shared foundation that all builder skills inherit. It defines quality gates, scoring dimensions, and review patterns that apply to every document type.

**All builder skills MUST reference this foundation.** When creating a new builder skill, add this line near the top:

```markdown
> **Foundation:** This skill inherits the quality framework from `skills/builders/builder-foundation/SKILL.md`. All Mid-Draft Quality Checks, Quality Dimensions, and Review Tiers defined there apply here.
```

## When This Foundation Applies

- Every builder skill in `skills/builders/`
- Every presentation skill in `skills/presentations/` that generates content (presentation-builder, presentation-planner)
- Any future skill that generates a document, transcript, or structured output for user consumption

Does NOT apply to:
- Intake skills (idea-refiner, north-star-builder, research, learn-and-improve) - these produce plans, not final documents
- Review skills (cross-agent-review) - these evaluate, not generate
- Utility skills (prose cleanup) - these post-process, not generate

---

## Spec-Becomes-Eval Discipline

The North Star is the spec. Mid-Draft Quality Check + Completion Gate ARE evals against the spec - they're not separate artifacts, they're one continuous loop. Treat the spec as the highest-leverage input: clarity at the North Star step multiplies through everything downstream.

"Skip-the-spec is skip-the-eval is dark code." When a builder skips the North Star or hand-waves a section, it removes the eval that would have caught the gap before draft. Builders that produce surprisingly bad output usually trace back to surprisingly thin North Stars.

### Source-Side Honesty (the substrate complements the spec)

The North Star is the spec; the **Source Inventory** is the substrate. A clean spec drafted over a contradictory, stale, or duplicate source set still hallucinates structurally - and a *plausibly-sourced wrong number can pass the Completion Gate's claim-honesty check* because the citation looks fine. Input-side preparation (the Source Inventory + Phase 1.5 Source Reconciliation in `north-star-builder` - conflict log, missing-context list, duplicates flag) and output-side honesty (the Completion Gate, below) are **complementary, not redundant**: the inventory prevents the dirty source from entering the draft; the gate catches what slips through. When a builder draws on multiple sources of uncertain authority, confirm the upstream reconciliation ran before trusting the substrate.

## Mid-Draft Quality Check (Mandatory)

After completing the first full draft, BEFORE presenting to the user, every builder skill must run this internal quality gate.

### Step 1: Quality Dimensions (Self-Score)

Rate the draft 1-5 on each dimension. Accurate self-assessment is essential - avoiding self-evaluation bias produces the most useful scores.

| Dimension | Score Range | What It Measures |
|-----------|------------|-----------------|
| **Depth** | 1-5 | Does the content teach something specific, or just describe at surface level? Would a domain expert learn something new? |
| **Originality** | 1-5 | Does the content offer non-obvious insights, or is it the first thing anyone would say about this topic? Could this have been the top Google result? **Compression test (external-facing content):** if an AI agent summarized this to three sentences for someone asking "should I trust/use this?", would a provable, differentiated point of view survive - or would it flatten into the category average? (N/A for tutorials/specs/code docs.) |
| **Coherence** | 1-5 | Does the narrative build logically toward the North Star's stated outcome? Could you remove any section without breaking the argument? |
| **Completeness** | 1-5 | Are all North Star must-covers addressed with substance (not just mentioned in passing)? |

**Scoring guide:**

| Score | Meaning |
|-------|---------|
| 5 | Exceptional - a domain expert would be impressed |
| 4 | Strong - solid content with genuine insights |
| 3 | Adequate - meets expectations but nothing surprising |
| 2 | Weak - surface-level, generic, or missing key details |
| 1 | Poor - does not address this dimension |

**Thresholds:**
- All dimensions 4+ → proceed to present
- Any dimension = 3 → recommended refinement. A score of 3 means "adequate but not surprising" - acceptable for quick drafts, but for high-stakes documents (whitepapers targeting investors, tech-arch for production systems), refine the weakest section before presenting
- Any dimension <= 2 → mandatory Refine-or-Pivot (Step 2)
- Average < 3.5 → strongly consider a structural pivot

**Eval Gold Standard:** A scoring criterion is well-written when two independent reviewers reading the same criterion would reach the same pass/fail (or same numerical score) on the same draft. If two reviewers might disagree, the criterion is too vague - sharpen it.

### Step 2: Refine-or-Pivot Decision

When any quality dimension scores <= 2, or when a dimension scores 3 on a high-stakes document:

1. **Identify** the weakest section - which single section would you rewrite if you could only improve one?
2. **Diagnose** the root cause:
   - **Surface problem** (missing details, vague language, generic examples) → **REFINE**
   - **Structural problem** (wrong angle, wrong decomposition, wrong framework) → **PIVOT**
3. **Execute** the decision:
   - **REFINE** = keep the structure, add depth, evidence, specificity, or concrete examples
   - **PIVOT** = restructure the section with a different angle, framework, or narrative approach. This means deleting and rewriting, not just editing.
4. **Re-score** the affected dimension. If still <= 2, pivot again or escalate to the user.
5. Present the improved draft as v1.

This check is internal - do not show the user the intermediate scores or state.

### Per-Skill Quality Prompts

Each builder skill should define skill-specific prompts for each dimension. The foundation provides the framework; the skill provides the specifics.

**Example for whitepaper-builder:**
```
Depth: Do deep-dive sections teach specific mechanics, or just describe feature existence?
Originality: Does competitive analysis reveal non-obvious gaps?
```

**Example for blog-builder:**
```
Depth: Do examples use specific details (names, numbers, dates) or generic placeholders?
Originality: Does the hook avoid cliched openings? Does the post offer a unique perspective?
```

---

## Weakness-Weighted Review Tiers

All review checklists in builder skills must be split into two tiers:

### Tier 1: Critical Items (Claude Weak Spots) - 70% of Review Effort

These are dimensions where Claude naturally underperforms. Spend most of your review time here.

**Universal Critical Items (apply to ALL builder skills):**

- [ ] Analysis goes beyond surface-level observations - every claim has supporting evidence or reasoning
- [ ] At least 2 insights that are non-obvious (not the first thing anyone would say about this topic)
- [ ] Honest Assessment / Risk sections genuinely acknowledge limitations (not token risks)
- [ ] No AI writing patterns (run a mental prose-cleanup check): no significance inflation ("serves as a testament to"), no promotional language ("groundbreaking"), no generic positive conclusions, no rule-of-three forcing
- [ ] Depth test: would a domain expert find new information here?
- [ ] **Negative constraints stated explicitly.** Every builder template names what the document should NOT include (e.g., no vendor marketing language, no emojis, no rule-of-three forcing, no "serves as a testament to" significance inflation). Opus 4.7 follows instructions literally; absent negative constraints, common AI patterns leak in. A prose-cleanup pass encodes such negative patterns - apply it from the relevant builder rather than restating.

**Skill-specific Critical Items** are defined in each builder skill and address weaknesses particular to that document type.

### Tier 2: Standard Items (Claude Strong Spots) - 30% of Review Effort

These are dimensions where Claude naturally excels. Quick verification is sufficient.

**Universal Standard Items (apply to ALL builder skills):**

- [ ] All template sections present and correctly ordered
- [ ] Formatting consistent throughout
- [ ] North Star alignment maintained (must-covers addressed, must-not-covers absent)
- [ ] Version naming correct
- [ ] No placeholder text remains
- [ ] Tone matches North Star specification

**Skill-specific Standard Items** are defined in each builder skill.

---

## Task Risk Gradient (Weight Review by Consequence)

The Weakness-Weighted Review Tiers (above) weight review by *Claude's skill at the task*. This gradient weights by a second, **orthogonal** axis: *the consequence of the claim being wrong*. Both apply at once - a claim can be a Claude strong-spot **and** high-consequence (a cleanly-formatted board number), and it still earns the full gate.

Review burden is not flat. Before the Completion Gate, tag each claim or element:

| Consequence | Examples | Review burden |
|-------------|----------|---------------|
| **Low** | Layout, formatting, chart drafting, summary wording, consistency checks | Trust the model; spot-check only |
| **Medium** | Source attribution, data extraction, paraphrase of a source | Verify the link, not the whole chain |
| **High** | Numerical synthesis, financial calculations, regulatory/compliance language, **any number that travels to a decision-maker** (investor, board, senior leadership) | Mandatory human-verifiable trace; never ship un-spot-checked |

One undefendable high-consequence number in an otherwise finished-looking file survives quick review precisely because everything else looks finished - concentrate scarce verification attention where being wrong is expensive.

**Calibration guard:** the gradient only helps if Low and Medium genuinely mean "lighter touch." If everything gets tagged High, the signal is lost - re-read the Low/Medium examples and demote anything that does not actually drive a decision.

---

## Completion Gate (Mandatory Before Presenting)

Mid-Draft Quality Check evaluates *content quality*. The Completion Gate evaluates *completion honesty*. Both run before presenting to the user.

The premise: Claude's most common document-generation failure is declaring a draft complete while obvious gaps remain - placeholder text, unverified numerical claims, broken cross-references, missing must-cover topics, fabricated facts. These are not quality issues (covered by Mid-Draft Quality Check); they are honesty issues. The cost of catching them after the user reviews is high - it erodes trust in every claim the document makes.

### The Gate

Before declaring v1 complete, every builder must answer each of these. Empty checkmarks are not allowed - every item gets a real disposition (`VERIFIED`, `SKIPPED: <why>`, or `BLOCKED: <reason>`).

#### Section 1: Claim Honesty

1. **Every numerical claim is traceable.** Each number in the document either points to a Fact Bank entry marked VERIFIED, or carries an inline source citation. No naked numbers, no remembered numbers from prior sessions. Tag each number's consequence (per the Task Risk Gradient); **High-consequence numbers need an explicit human-verifiable trace, not just a citation that looks fine** - a plausible citation on a wrong number passes this check otherwise.
2. **Every named entity is real.** Every cited person, project, paper, contract address, HIP, RFC, or standard exists and was checked (not assumed from training data). Fabricated citations are the highest-severity failure - if any citation cannot be verified, mark it UNVERIFIED in the Fact Bank rather than presenting it as fact.
3. **Every named feature behaves as described.** When the document describes how something works (a protocol, an API, a tool), the description matches reality, not a plausible-sounding fabrication. If you are not certain about behavior, hedge ("based on the v3.0 docs, X is expected to...") or omit.

#### Section 2: Structural Honesty

4. **No placeholder text remains.** Grep the draft for `TODO`, `TBD`, `<...>`, `Lorem ipsum`, `[INSERT`, `XXX`, and `FIXME`. Every hit must be resolved or removed.
5. **All North Star must-covers are addressed with substance.** "Mentioned in passing" does not count - each must-cover gets its own section or substantial subsection. Cross-reference the North Star and confirm.
6. **Cross-references resolve.** Every "see Section X" or "as discussed in [name]" points to content that actually exists in the document. After Rule 2 (Descriptive References), grep the draft for `Section \d`, `Step \d`, `Figure \d`, `Table \d` and confirm each has a descriptive name and the referenced content is present.
7. **Canonical Glossary applied.** If the document has 3+ sections, the Canonical Glossary exists at the top of the working file and every key noun matches it exactly. Grep each glossary term and check for drift.

#### Section 3: Scope Honesty

8. **Match the version filename to actual scope.** A "v2" implies meaningful changes from v1. If the v2 is mostly v1 with cosmetic edits, name it v1.1 or note "minor revision" in the changelog. Do not inflate version numbers.
9. **Match the summary to actual content.** If the executive summary or abstract claims "this whitepaper covers X, Y, Z," the document must actually cover X, Y, and Z with substance. No aspirational summaries.
10. **List what was NOT addressed.** Explicitly note in the document (or in the message presenting it) which North Star items were deferred, simplified, or not addressed - and why. Honesty about gaps prevents false confidence.

#### Section 4: Visual Honesty (Binary Outputs Only)

This section applies only when the deliverable is a binary file the agent cannot directly read (PPTX, DOCX, PDF, MP4, PNG-from-render). Skip if the output is text/Markdown/HTML.

10.5. **Render and read.** Before declaring v1 complete, convert the binary to a readable form and visually verify at least 3 representative samples (e.g., title slide, mid-document slide, conclusion slide for a deck; first/middle/last page for a doc). Read the rendered images via Claude Code's image-reading capability. Verify: diagrams render fully (no `\n` line breaks, no truncation); text fits its container (no overflow, no autofit collapse); colors match plan (no hex format mismatch).

The premise: when the agent writes code that emits a binary, the agent never sees the rendered output during the build. The user becomes the renderer-of-last-resort, and visible bugs (Mermaid `\n`, autofit, color formats) only surface after presentation. Rendering one sample mid-build catches these before they ship.

If your skill produces binary output, document the rendering pipeline in the skill's "Visual Self-QA" subsection (e.g., presentation-builder uses `python scripts/office/soffice.py --headless --convert-to pdf` + `pdftoppm -jpeg`).

#### Section 5: Entity Linking and Plain-English (When the Document References External Entities)

This section applies when the deliverable references external entities readers may want to follow up on - GitHub repos/PRs/issues/releases, Notion pages, web URLs, papers, standards, products. Skip if the deliverable has no external references.

11. **Every external entity reference is a markdown link on first mention.** The bar is not "link if significant" - it is "link every time you name a specific repo/PR/issue/page/standard/paper." Bare entity names are the #1 cause of follow-up friction; the cost of one extra `[name](url)` is trivial compared to a reader manually searching for the thing you just named. Subsequent in-section mentions may be plain text if context is unambiguous.
12. **First-mention expansion for jargon.** The first time you name a project, internal component, or acronym in a section, follow it with a 3-7 word plain-English expansion (e.g., "`solo`, the local Hiero/Hedera dev network deployment tool"). The expansion source is, in priority order: (a) a Project Glossary in the source profile/spec if one exists, (b) your verified knowledge written at that level of detail. If you cannot confidently expand a term, hedge ("an internal SDK abstraction") or skip the term - parroting jargon you don't understand is worse than verbose plain English. This rule originated in the team-digest sa-digest skill (May 2026 friction: digest entries like "PR #1328 deprecating local-node in favor of solo" forced readers to ask "what's solo?").

#### Section 6: The "5 More Minutes" Question

13. **What would I check if I had 5 more minutes?** Answer in one specific sentence. If the answer is non-trivial, do it before presenting.

### Output

Surface the gate result as a brief inline summary when presenting v1: "Completion Gate: 11/11 verified" or "Completion Gate: 9/11 verified (2 skipped: <why>)". Do not paste the full checklist - the act of running it is the value, not a wall of paperwork.

### Failure Patterns This Catches

Provenance: the 2026-04-06 through 2026-04-29 Lessons Log rows map one-to-one to the gate items above.

---

## Optional: Document Evaluator Agent

For complex or high-stakes documents, builder skills can invoke the `[DOC_EVAL]` agent (`.claude/agents/document-evaluator.md`) as an independent quality check. This provides a separate evaluation context, partially mitigating self-evaluation bias.

### When to Use

- **Recommended:** whitepapers, tech-arch docs, product specs (complex, multi-section)
- **Optional:** blog posts, one-pagers (simpler, lower stakes)
- **Not needed:** quick drafts or iterative revisions where the user is providing live feedback

### How to Invoke

After the Mid-Draft Quality Check, if the skill wants an independent evaluation:

1. Spawn the `[DOC_EVAL]` agent with:
   - The North Star file path
   - The draft document file path
   - The document type (whitepaper, spec, blog, etc.)
2. The agent returns: dimension scores, top 3 weaknesses, and a PASS/REVISE/REWRITE verdict
3. If REVISE or REWRITE, feed the agent's feedback into a Refine-or-Pivot cycle before presenting to the user

### Anti-Leniency Notes

The document evaluator agent is tuned to be skeptical. It has explicit anti-leniency rules. However, it is still Claude evaluating Claude - this mitigates but does not eliminate self-evaluation bias. For truly independent evaluation, use the cross-agent review skill with external models.

### Autonomous Refine Loop (Opt-In)

When the user wants the quality cycle to run hands-off (or pairs the build with `/goal`), wire the evaluator as an iterate-until-pass loop instead of a one-shot check. The grader runs in an independent context window, which outperforms self-critique:

1. Draft per the builder skill (Mid-Draft Quality Check still applies mid-stream).
2. Spawn `[DOC_EVAL]` on the full draft (North Star + draft path + document type).
3. PASS -> stop, report iterations + final scores. REVISE/REWRITE -> apply ONLY the evaluator's top 3 weaknesses (no opportunistic rewrites - scope creep here erodes the North Star), then re-evaluate.
4. Hard cap: 3 evaluation rounds. Still failing at the cap -> stop IMMEDIATELY: no further edits, present the document WITH the round-3 weaknesses listed as unresolved (per Refine-or-Pivot, any persistent failing verdict - REVISE or REWRITE - signals a problem the user must weigh in on, not a polish problem).

Each round reports: verdict, dimension scores, what changed. The loop's stop condition is the evaluator's verdict - never the drafting context's own judgment. Goal-ready pairing: `/goal "the document evaluator sub-agent returns PASS, or 3 evaluation rounds have completed"`.

---

## Sprint Contract Pattern (Complex Documents Only)

For documents expected to exceed 500 lines (whitepapers, tech-arch docs), builder skills should optionally use the sprint contract pattern before drafting:

### What is a Sprint Contract?

A brief agreement (written as a comment in the output file or held in working memory) that specifies:
1. **What "done" looks like for each major section** - not just "write the section" but "this section must include X, Y, Z with at least N examples/diagrams"
2. **How quality will be verified** - which quality dimensions matter most for this section
3. **Acceptance criteria** - what would make this section score 4+ on each relevant dimension

### When to Use

- Documents with 5+ major sections
- Documents where section quality varies significantly (common in whitepapers where deep-dives are the substance but executive summaries are boilerplate)
- When the user has indicated high expectations for a specific section

### When to Skip

- Blog posts, one-pagers, or documents under 500 lines
- When the user wants a quick draft and will iterate
- Revision cycles (v2, v3) where the structure is already established

---

## Harness Assumption Awareness

Every builder skill encodes assumptions about what Claude must be told explicitly; they go stale as models improve. Recurring suspects: output chunking caps, explicit Mermaid formatting rules, detailed template section ordering, review-checklist items that always pass. The test-and-remove procedure (ablate one constraint, build, compare) lives in the Skill Health Audit (`docs/skill-health-audit.md`). Default to the simplest rule set that demonstrably holds.

---

## Periodic Simplification Pass

Quarterly or after a model upgrade, review each builder skill per the Skill Health Audit (rules that never trigger, boilerplate template sections, always-pass checklist items, merge candidates). Document findings in `workspace/idea-forge-meta/` using the learn-and-improve skill format.

---

## Token Economy Rules

When processing long content (500+ lines) during any phase of document generation:

1. **Summarize first, then work from the summary.** Never analyze a long document by re-reading it end-to-end multiple times.
2. **Use Grep for specific quotes** instead of re-reading the full source. If you need a specific passage, search for it.
3. **Never re-read a full document you've already summarized in the same session.** Work from your summary and Grep for details.
4. **For research inputs (articles, papers):** read once, extract patterns, then work from extracted patterns. Do not re-fetch or re-read the source.

These rules apply to all builder skills when processing North Star docs, plans, research briefs, or reference material during document generation.

### MCP Tool Results

When using MCP tools that return lists (e.g., `search_thoughts`, `list_thoughts`):
- Process the **top 3-5 most relevant results**, not all returned results
- If more than 5 results return, scan titles/summaries first, then read only the relevant ones in full
- For batch captures (5+ items to `capture_thought`), collect all items first, then dedup in a single pass using `search_thoughts` with the most distinctive term from each item

---

## Document Consistency Rules (Mandatory)

Two rules apply to every document produced by any builder skill. Both exist because real Catalyst v3 review surfaced violations that confused readers and caused downstream AI tools to produce wrong answers when queried about the document.

### Rule 1: Naming Consistency (Canonical Glossary)

**Problem (Catalyst v3):** the same base pool was named "USDC/catUSD", "USDC/USDT", and "USDC/USDT0" across three sections - and survived into v2 because no single source of truth existed.

**Rule:** Before drafting any document with 3+ sections, create a **Canonical Glossary** at the top of the working file (can be removed before final version, OR kept as an appendix). The glossary locks every key noun to one canonical form:

- **Protocol components** (base pool composition, token names, engine names, module names)
- **Numerical claims that appear multiple times** (TVL figures, market share, launch dates)
- **Defined terms** introduced in the document (acronyms, project-specific concepts)

Every mention of a key noun in the document must match the glossary exactly. No variation, no synonyms, no "USDT0" in one paragraph and "USDT" in the next unless they are genuinely different things.

**Self-check before declaring the draft complete:**
1. List every key noun in the Canonical Glossary
2. Grep the document for each one and its common variations
3. Fix any drift

**Why beyond aesthetics:** inconsistent nouns also break AI-assisted querying of the doc - the tool cannot tell which form is authoritative.

### Rule 2: Descriptive References (No Naked Numbers)

**Problem (Catalyst v3):** "Catalyst solves for steps 2-4", "Engine 2", "Section 5 and Section 6 explain this" - forces flip-back lookups and goes stale on reorder.

**Rule:** Never reference another part of the document by number alone. Always use a descriptive name:

| Wrong | Right |
|-------|-------|
| "Section 5 and 6 explain this" | "the Liquidity Bootstrapping and Revenue Model sections explain this" |
| "Engine 2 handles CDP issuance" | "the CDP Issuance Engine handles this" |
| "Catalyst solves for steps 2-4" | "Catalyst solves for liquidity bootstrapping, market-making, and credit market access" |
| "See Figure 3" | "See the Metapool Architecture diagram" |

If a section or concept is important enough to reference, it's important enough to have a name the reader will remember. Numbers force lookups; names teach.

**Exception:** Formal numbered references (e.g., "HIP-991", "GENIUS Act Section 3(a)") are fine because those numbers are external canonical identifiers, not internal document structure.

**Self-check:** Grep the draft for `Section \d`, `Step \d`, `Engine \d`, `Figure \d`, `Table \d`. Every hit must have a descriptive name alongside or replacing the number.

---

## Lessons Log

Every builder skill should maintain a dated lessons log. When a skill execution surfaces a problem, add a row. This makes skills smarter over time from real usage.

### Format

```markdown
## Lessons Log

| Date | What Happened | What Changed |
|------|--------------|-------------|
| YYYY-MM-DD | <specific failure description> | <rule or process that was updated> |
```

### Rules

1. **Add entries after real failures**, not hypothetical ones. The date proves it happened.
2. **Be specific.** "Output was bad" is useless. "Whitepaper deep-dive section scored 2/5 on depth because it described features without explaining mechanics" is actionable.
3. **Reference the fix.** Every entry should point to what was changed (a new rule, an updated quality prompt, a threshold adjustment).
4. **Graduate stable lessons.** After 3+ months, if a lesson has been encoded as a permanent rule, remove the log entry. The rule is the lesson; the log entry is the provenance.
5. **Log entries are not complaints.** Each entry must have a "What Changed" column that shows the skill actually improved.

### Builder Foundation Lessons Log

| Date | What Happened | What Changed |
|------|--------------|-------------|
| 2026-04-04 | Skills had static "Lessons Learned" sections with no dates or failure context. Impossible to assess recency or whether lessons were from real failures. | Added this dated Lessons Log format to builder-foundation. All builder skills now inherit it. |
| 2026-04-04 | Self-evaluation bias: builder skills checked their own review checklists and always "passed." No quality scoring or thresholds. | Added Mid-Draft Quality Check with 4-dimension scoring (Depth/Originality/Coherence/Completeness) and Refine-or-Pivot decision. Source: Anthropic harness design article. |
| 2026-04-04 | Review checklists treated all items equally. Claude spent equal time on structure (strong) and depth (weak). | Added weakness-weighted review tiers: 70% effort on Critical (Claude weak spots), 30% on Standard (Claude strong spots). Source: Anthropic harness design article. |
| 2026-04-06 | Catalyst v3 whitepaper: research agents hallucinated dates and inflated numbers. SaucerSwap TVL reported as $140M (actual: $78M), USDT0 launch reported as 2025 (actual: March 2026), AUDD TVL reported as $5.2M (actual: ~$180K), staking yield reported as 6.5% (actual: 2.5%). | Added "Numerical Claim Verification" section to research skill requiring primary source verification for all numbers. Added numerical verification as top Critical Item in whitepaper-builder review checklist. |
| 2026-04-06 | Catalyst v3 Mid-Draft Quality Check: Originality scored 3/5 (borderline) but didn't trigger refinement because threshold was <= 2. A score of 3 means "adequate but not surprising" which is insufficient for investor-facing whitepapers. Also found: HIP-1215 repeated 4-6 times across sections (redundancy), no quantitative financial model despite describing revenue sources. | Added borderline threshold (dimension = 3 recommends refinement for high-stakes docs). Added no-redundancy rule and financial model requirement to whitepaper-builder. Added both to Critical Items checklist. |
| 2026-04-08 | Catalyst v3 whitepaper v2 user review: base pool composition described inconsistently across sections (USDC/catUSD in one section, USDC/USDT in another, USDC/USDT0 in a third). Caused reader confusion and made AI-assisted summaries unreliable because the tool could not identify the canonical form. | Added Rule 1 (Naming Consistency / Canonical Glossary) to builder-foundation. Every builder must lock key nouns before drafting and self-check via grep before declaring complete. |
| 2026-04-08 | Catalyst v3 whitepaper v2 user review: vague cross-references throughout ("Section 5 and 6 explain this", "Engine 2 handles CDP", "Catalyst solves for steps 2-4"). Forced readers to flip between sections and became stale when sections were reordered. | Added Rule 2 (Descriptive References / No Naked Numbers) to builder-foundation. Every builder must use descriptive names for internal references, not section/step/engine numbers. |
| 2026-04-29 | Claude Code usage report (1,020 messages, 39 sessions) showed 38 friction events (20 wrong_approach + 18 buggy_code) tracing to premature completion claims - shipping work that looks done but isn't (stderr leakage missed, percentages exceeding bounds, surface-level tests missing real bugs, commit messages overstating scope, fabricated technical claims like fictional HIP-904 indefinite rent). Mid-Draft Quality Check evaluates content quality but did not catch completion-honesty issues. | Added Completion Gate (mandatory before presenting v1) covering Claim Honesty, Structural Honesty, Scope Honesty, and the "5 more minutes" reflection. Counters the premature-completion failure mode at the document level. |
| 2026-04-29 | The Smart Ape "Opus 4.7 punishes bad prompting" article (Apr 17 2026) flagged that 4.7 follows instructions literally - vague templates that produced acceptable output on 4.6 leak common AI patterns on 4.7 because the model no longer fills in unstated intent. Universal Critical Items listed positives only. | Added "Negative constraints stated explicitly" as a Universal Critical Item. Builder templates must name what the document should NOT include, not just what it should. References a prose-cleanup pass rather than restating the patterns. |
| 2026-06-07 | learn-and-improve audit of the Nate Jones data-room video surfaced that idea-forge's hallucination defenses were entirely output-side (Completion Gate, Fact Bank, numerical verification). A plausibly-sourced wrong number drafted from a contradictory or duplicate source set passes claim-honesty and ships. No input-side source-prep existed. | Added "Source-Side Honesty" to the Spec-Becomes-Eval Discipline, pointing builders at the upstream Source Inventory + Phase 1.5 Source Reconciliation in north-star-builder as the input-side complement to this gate. |
| 2026-06-08 | learn-and-improve audit of the Nate Jones agentic-office-pipeline video: review effort was weighted only by Claude's skill at the task (Weakness-Weighted Tiers), never by the consequence of a claim being wrong. A board-bound valuation number and a layout tweak got the same (flat) scrutiny - "a financial model in a costume" ships when a high-consequence number looks finished. | Added the Task Risk Gradient (Low/Medium/High consequence, orthogonal to the skill-based tiers) and tied it into Completion Gate Section 1: High-consequence numbers need a human-verifiable trace, not just a plausible citation. |

---

## Integration with New Builder Skills

When creating a new builder skill:

1. Add the foundation reference line (see Purpose section)
2. Define skill-specific quality prompts for each of the 4 dimensions
3. Define skill-specific Critical and Standard review items
4. Decide whether the sprint contract pattern applies (based on expected document length)
5. Decide whether the document evaluator is recommended or optional for this type

The foundation handles the framework; the skill handles the specifics.

---

**Version:** 2.7.0 - leanness trim after the model-upgrade ablation review: provenance prose compressed (rules unchanged), Failure-Patterns table folded into a provenance line, Harness-Assumption/Simplification bodies now point at the Skill Health Audit. No behavioral rule added or removed.

2.6.0 - Autonomous Refine Loop (prior baseline).
