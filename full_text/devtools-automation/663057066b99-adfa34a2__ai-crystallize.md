---
name: ai-crystallize
description: Autonomous AI crystallization - synthesizes converged thinking topics into ai-inferred notes in a dedicated folder. Never touches the human-curated permanent knowledge base and never changes a topic's status, so manual crystallization stays available to the user.
automation: autonomous
schedule: "0 8 * * 1"
allowed-tools: Read, Write, Grep, Glob, Bash
user-invocable: true
argument-hint: "[topic-slug] (optional - processes all un-crystallized converged topics if omitted)"
---

# AI Crystallize

Autonomous companion to the human crystallization path. Each run synthesizes **converged** thinking topics into standalone notes written to a **dedicated, segregated folder** - never `Brain/02-Permanent/`.

**Why this exists:** Converged topics pile up faster than a human can crystallize them. This playbook captures the AI's synthesis of each converged topic so the conclusion is not lost - while preserving the one boundary the second brain must never cross autonomously: **nothing enters the endorsed permanent knowledge base without an explicit endorsement act by the user.**

**The boundary, stated plainly:**
- This playbook writes ONLY to `Brain/05-Meta/AI Crystallizations/`, tagged `provenance: ai-inferred`, excluded from semantic indexing.
- It NEVER writes to `Brain/02-Permanent/`, `Brain/AI Extracted Notes/`, or `Brain/05-Meta/Reports/`.
- It NEVER changes a topic's `status` in the Thinking Registry (the topic stays `converged`), so `/manage-thinking-topics crystallize` remains fully available to the user for the real, endorsed crystallization.
- Its output is a **candidate for human review**, not a permanent note.

## Design principle

Automate the synthesis, segregate the artifact, gate the endorsement. The AI may draft what it concluded; only the human may promote a conclusion into the knowledge they will reason FROM.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Thinking Registry | `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` | ✓ | | Find converged topics (read-only - never mutated here) |
| Thinking Files | `Brain/05-Meta/Thinking/[topic-slug].md` | ✓ | | Source of the converged conclusion (read-only) |
| AI Crystallizations | `Brain/05-Meta/AI Crystallizations/[topic-slug].md` | ✓ | ✓ | Output notes (the only write target for content) |
| Crystallization Index | `Brain/05-Meta/AI Crystallizations/INDEX.md` | ✓ | ✓ | Manifest of what has been AI-crystallized |
| Session Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Run log |

## Prerequisites

- Thinking Registry exists at `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`
- Output folder `Brain/05-Meta/AI Crystallizations/` exists (create if missing)
- At least one topic with `status: converged` (otherwise clean exit)

## Configuration

- **Per-run cap:** process at most **5** un-crystallized converged topics per run (reliability + 45-minute budget). Remaining topics are picked up on the next run. The cap is a soft limit; if fewer than 5 remain, process all.

---

## Process

### Step 1: Get Date and Load Converged Topics

```bash
date '+%Y-%m-%d'
```

Read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`. Collect every topic listed in the **Converged (Ready for Crystallization)** table (or any topic whose thinking-file frontmatter is `status: converged`).

If a specific `[topic-slug]` was passed as argument, restrict to that single topic (verify it is converged; if not, log and exit).

If there are no converged topics, write a brief changelog entry and exit cleanly.

### Step 2: Deduplicate (Idempotency)

For each converged topic, check whether `Brain/05-Meta/AI Crystallizations/[topic-slug].md` already exists.

- **Exists** -> already AI-crystallized; skip.
- **Does not exist** -> eligible for this run.

This file-existence check is the dedup mechanism. The playbook never mutates the Thinking Registry or thinking files, so it is fully idempotent and safe to retry.

### Step 3: Select the Batch

From the eligible (un-crystallized) converged topics, take up to the per-run cap (5), oldest-converged first where the converged date is available; otherwise registry order. **Convergence-date proxy:** thinking files carry no `converged_on` frontmatter field, so use the frontmatter `updated:` date (the converging run stamps it) as the oldest-first sort key - cheap to extract in one pass with `grep -m1 '^updated:'` across the Thinking folder. Note in the run log any eligible topics deferred to a later run.

### Step 4: Extract the Converged Conclusion

For each selected topic, read `Brain/05-Meta/Thinking/[topic-slug].md` and extract the conclusion. Prefer the canonical block, fall back gracefully:

1. **Look for `## Final Synthesis`** - the canonical block appended by the incubation loop at convergence. If present, this is authoritative. Extract: Conclusion, Confidence + leading hypothesis, Key evidence, Convergence path, Remaining uncertainty, Related topics. **Note:** legacy topics instead carry an inline `**Final Synthesis:**` / `**Final converged position:**` line (not a `##` header) near the end - a `grep '## Final Synthesis'` will miss these. Match the lowercase inline form too, or just go straight to the tail per step 2.
2. **If absent** (legacy topics), read only the **last ~120 lines** of the file (some are 5,000+ lines). Extract: central question (frontmatter `topic`), the trailing "Final Synthesis" / "Final converged position" / "Current Best Answer", the last "Updated Hypotheses" table, and any "Open Questions". The convergence-assessment block (run count, leading-hypothesis streak, confidence delta) sits just above and gives the Convergence Path.
3. Read the full file only if the last 200 lines contain no conclusion.

Do **not** run KB search or web search - this playbook synthesizes from the already-converged reasoning, not new evidence. Keep it fast and self-contained.

### Step 5: Draft the AI Crystallization Note

Write to `Brain/05-Meta/AI Crystallizations/[topic-slug].md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: [model-name]
updated_by: [model-name]
agent_version: 01.25
provenance: ai-inferred
source_topic: "[[topic-slug]]"
status: ai-crystallized
---

> 🤖 **AI Crystallization - not endorsed knowledge.** Synthesized autonomously from a converged thinking topic. Carries `provenance: ai-inferred` and lives outside `Brain/02-Permanent/`. This is a **candidate for human review**, not a permanent note. To promote it, the user runs `/manage-thinking-topics crystallize [topic-slug]`.

# [Topic Title]

**Central Question:** [exact question from the thinking file]

## Conclusion
[1-2 paragraphs - the substantive answer, in neutral third-person AI-synthesis voice. NOT first-person your voice - this is ai-inferred, not his endorsed thinking.]

## Confidence
[X% on H[N] (and any co-leading hypotheses)]

## Key Evidence
- [[Note A]] - [why it mattered]
- [[Note B]] - [why it mattered]
- [[Note C]] - [why it mattered]

## Convergence Path
[Standard | Framework exhaustion] after [N] runs

## Remaining Uncertainty
[1 paragraph - what is known to be unknown; what could change this]

## Source
Crystallized from [[topic-slug]] (`Brain/05-Meta/Thinking/[topic-slug].md`), converged [date].
[Related topics, if any: [[other-slug]]]
```

**Voice discipline:** write the Conclusion in neutral analytical voice, never first-person as the user. This artifact is `ai-inferred`; it must never read as if the user authored or endorsed it. Per CLAUDE.md's guarded boundary, only an explicit endorsement act by the user (via manual crystallization) may set `provenance` to `endorsed` or `originated`.

### Step 6: Update the Crystallization Index

Append a row to `Brain/05-Meta/AI Crystallizations/INDEX.md` (create the file with a header if missing):

```
| [topic-slug] | [one-line conclusion summary] | [confidence] | YYYY-MM-DD |
```

### Step 7: Write Session Changelog

Write to `Brain/05-Meta/Changelogs/CHANGELOG - AI Crystallize YYYY-MM-DD.md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: [model-name]
updated_by: [model-name]
agent_version: 01.25
---

# AI Crystallize Session: YYYY-MM-DD

## Crystallized This Run
| Topic | Conclusion Summary | Confidence | Status |
|-------|-------------------|------------|--------|
| [slug] | [summary] | X% | ai-crystallized (awaiting human review) |

## Deferred (over per-run cap)
[List of eligible converged topics not processed this run, or "None"]

## Note
These are AI-inferred candidates in `Brain/05-Meta/AI Crystallizations/`. The source topics remain `status: converged` and available for the user's manual crystallization via `/manage-thinking-topics crystallize [slug]`.
```

---

## What This Playbook Must Never Do

- ❌ Write to `Brain/02-Permanent/`, `Brain/AI Extracted Notes/`, or `Brain/05-Meta/Reports/`
- ❌ Set `status: crystallized` on a topic (that marks human, endorsed crystallization)
- ❌ Set `provenance` to `endorsed` or `originated`
- ❌ Write any note in the user's first-person voice
- ❌ Mutate the Thinking Registry or thinking files

If any of these would be required, stop and log - the topic belongs to the human path.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Registry missing | Log to changelog, exit cleanly |
| No converged topics | Log to changelog, exit cleanly |
| Output folder missing | Create `Brain/05-Meta/AI Crystallizations/`, proceed |
| Thinking file missing for converged topic | Log warning, skip topic |
| No Final Synthesis and no conclusion in last 200 lines | Read full file once; if still none, skip topic and log |
| Run approaches 45 minutes | Stop after current topic, log remaining as deferred |

---

## Completion Checklist

- [ ] Registry read - converged topics identified
- [ ] Each converged topic deduped against the AI Crystallizations folder
- [ ] Batch selected within per-run cap; deferred topics logged
- [ ] Each processed topic: conclusion extracted (Final Synthesis preferred)
- [ ] Each processed topic: note written to `Brain/05-Meta/AI Crystallizations/` with `provenance: ai-inferred`
- [ ] No write touched `02-Permanent/`, `AI Extracted Notes/`, or `Reports/`
- [ ] No topic status changed in the registry
- [ ] Index updated
- [ ] Session changelog written

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `incubation-loop` | Produces the converged topics this playbook reads |
| `manage-thinking-topics crystallize` | The **human, endorsed** path - writes to `02-Permanent/` / `Reports/`, gated by approval. This playbook never overlaps with it; it is the AI-only, segregated companion |
| `synthesize-insights` | the user's manual synthesis tool - unaffected |

---

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could extraction, the note template, or the cap be sharper?
- [ ] **Scope check**: Only execution changes - NEVER relax the segregation boundary (the never-touch-permanent rule is load-bearing, not tactical)
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control**:
  - [ ] `git add .claude/skills/ai-crystallize/SKILL.md`
  - [ ] `git commit -m "refactor(ai-crystallize): <brief improvement>"`
