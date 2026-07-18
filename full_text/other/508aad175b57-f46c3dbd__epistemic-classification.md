---
name: epistemic-classification
description: Framework for distinguishing research findings from hypotheses and speculative synthesis. Use when extracting insights from research, creating notes from external sources, or classifying the epistemic status of claims.
user-invocable: false
---

# Epistemic Classification Framework

**CRITICAL: When extracting insights from research or synthesizing across domains, you MUST clearly distinguish between:**

## Classification Levels

### 1. Confirmed Research Findings
Empirically validated, peer-reviewed, replicated

- **Tag:** `#research-finding` or `#empirical-evidence`
- **Language:** "Research shows...", "Studies confirm...", "Evidence demonstrates..."
- **Requirement:** Source citation with publication year and journal

### 2. Theoretical Frameworks
Established models with strong theoretical backing

- **Tag:** `#theoretical-framework` or `#established-theory`
- **Language:** "The framework proposes...", "Theory suggests...", "Model predicts..."
- **Note:** Level of acceptance in field

### 3. Working Hypotheses
Testable propositions not yet validated

- **Tag:** `#hypothesis` or `#testable-hypothesis`
- **Language:** "A possible mechanism...", "This suggests...", "One hypothesis..."
- **Mark as:** "HYPOTHESIS:" in note title or frontmatter
- **Include:** What would validate/falsify this hypothesis

### 4. Speculative Synthesis
Original connections or interpretations

- **Tag:** `#speculative-synthesis` or `#original-synthesis`
- **Language:** "This might explain...", "A potential connection...", "Speculatively..."
- **State clearly:** "This is synthesis/interpretation, not established fact"
- **Confidence level:** Low (20-40%), Medium (40-70%), High (70-90%)

### 5. Research Gaps
Identified missing connections in literature

- **Tag:** `#research-gap` or `#unexplored-connection`
- **Language:** "Research has not yet explored...", "Gap identified..."
- **Note:** Why this gap matters

---

## Mandatory Labeling for Hypotheses

When creating notes containing hypotheses or speculative synthesis:

```markdown
---
title: [Title] (HYPOTHESIS) or [Title]
type: hypothesis / speculative-synthesis / working-theory
status: untested / under-investigation / partially-supported
confidence: low / medium / high
tags: #hypothesis #topic
---

**STATUS: HYPOTHESIS - NOT CONFIRMED BY RESEARCH**

[Content of hypothesis]

## Testable Predictions
[What would validate this]

## Current Evidence
[Supporting indirect evidence]

## Research Needed
[What studies would test this]
```

---

## Examples

### ✅ GOOD
- "Dopamine May Modulate Interoceptive Precision Weighting (HYPOTHESIS)"
- Type: speculative-synthesis
- Status: untested
- Confidence: medium
- Clear statement: "This is an original synthesis filling a research gap"

### ❌ BAD
- "Dopamine Modulates Interoceptive Precision" (stated as fact)
- No hypothesis tag
- No confidence level
- Presented as established finding

---

## Intellectual Honesty Principle

Your role is to help build a knowledge base with MAXIMUM EPISTEMIC CLARITY. Users must be able to trust the distinction between:
- What science has proven
- What theory predicts
- What remains speculative
- What is original synthesis

**Never present hypotheses as facts. Never obscure the difference between research and speculation. Intellectual rigor requires epistemic humility.**

---

## Authorship Provenance (a second, orthogonal axis)

The classification levels above tag a claim's **truth status** (how proven it is). Provenance is a **separate, independent axis** that tags **who authored the thinking**. Both must be carried - a claim can be high-confidence-empirical *and* merely `encountered` (a peer-reviewed finding read but not endorsed); it can be low-confidence-speculative *and* `originated` (the user's uncorroborated gem).

Set the `provenance:` frontmatter field on every knowledge note:

| Value | Meaning |
|-------|---------|
| `originated` | the user's own original thinking - the cognitive fingerprint. **The asset.** |
| `endorsed` | External idea the user explicitly adopted as his own view. |
| `encountered` | Read and recorded, not yet endorsed. **Default for external-document extractions.** |
| `ai-inferred` | An agent's own synthesis/inference. Must stay tagged so it never wears the user's voice. |

**Two guardrails (non-negotiable):**

1. **Never demote an `originated` insight toward consensus.** Uncorroborated + originated = the gem, not a defect. A second brain that regresses its owner's thinking to the consensus mean has destroyed its reason to exist. (This is the inversion that makes this knowledge base *not* an oracle.)
2. **Measure provenance; never adjudicate originality.** Tiering and tagging are human-reviewable signals. Do not silently decide what is "true" or rewrite who authored a thought.

**The guarded boundary:** nothing crosses `encountered` -> `endorsed` without an explicit endorsement act by the user. When new external input contradicts an existing note, create a tension/contrast link - do **not** overwrite. Contradictions are synthesis fuel for `detect-tensions`, not errors to correct.

---

## Gate 1: Source Tiering at Ingestion

Before extracting from any external source, tier it and reject slop **at the door**. Stamp the tier on the note's frontmatter (`source-tier:`) so trust is recorded, not buried.

**The per-domain source diet - which sources to trust, demote, or reject - is the canonical `resources/SOURCE-AUTHORITY.md`.** Consult it when tiering. Keep that file as the single source of truth; do not maintain a competing list here.

**Tier values for `source-tier:`** `primary` (the paper/text/lab itself) | `credible-interpreter` (a trusted secondary reading it faithfully) | `rejected` (content-farm / AI-generated / regurgitation - do not extract).

**Cross-domain rule (applies to any domain):** prefer the primary over anyone summarizing it; reject machine-generated and content-farm material before extraction; record the tier on ingestion.
