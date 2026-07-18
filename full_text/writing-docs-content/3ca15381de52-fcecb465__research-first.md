---
name: research-first
description: Gather sources before implementing
inputs:
  - topic: string
  - max_sources: number
---

# When to use

Before writing code on a topic the agent doesn't already know well — save round-trips on bad assumptions.

# Steps

1. Search for high-signal sources on **{{topic}}**.
2. Read up to **{{max_sources}}** of them; prefer primary docs, RFCs, source code, and recent (≤12 months) writeups.
3. Summarize key findings, contradictions, and open questions in a short brief.
4. Only then proceed to implementation.

# Output

A markdown brief with:

- **Sources**: titled, dated, linked.
- **Findings**: 3–5 bullets, one fact each.
- **Contradictions**: anywhere two sources disagree.
- **Open questions**: things to verify in code before writing.
