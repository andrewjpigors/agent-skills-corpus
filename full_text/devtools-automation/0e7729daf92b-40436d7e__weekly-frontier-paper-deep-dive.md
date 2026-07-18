---
name: weekly-frontier-paper-deep-dive
description: Use when producing a rigorous, beginner-accessible Chinese deep dive on the frontier AI paper best suited to the user, together with a text-first nine-card mobile carousel archived at the end of the Notion page and a text-only WeChat notice. Converges cross-domain candidate research before selection, renders accurate 1080×1920 cards, uses native Notion LaTeX equations, adds a titled TL;DR share copy with the original paper link, and refuses completion before publication readback. Manual invocation by default; never creates schedules or automation unless separately requested.
version: 2.1.0
author: Chengbo Zhuang and Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, machine-learning, llm, paper-reading, notion, infographic]
    related_skills: [arxiv, notion, baoyu-infographic, ocr-and-documents]
---

# Weekly Frontier Paper Deep Dive

## Overview

Produce one publication-quality Chinese explanation of the frontier ML/LLM or adjacent AI paper that best fits the user's interests, learning stage, and preference for deployable systems. The workflow has three deliverables:

1. a durable, beginner-accessible but technically deep Notion page containing the complete explanation and source trail;
2. exactly nine accurate, text-first, visually consistent `1080×1920` PNG cards collected as a publication package at the end of that page;
3. a short text-only WeChat notice saying what was produced, why the paper matters, and where it is stored.

“Frontier” means technically novel and evidence-backed, not merely recent or popular. “Best fit” is a multi-objective editorial judgment backed by a converged cross-domain shortlist, hard evidence gates, normalized scoring, and explicit runner-up comparisons. “Beginner-accessible” means unfamiliar concepts are introduced at first use with their purpose, mechanism, and place in the larger causal chain; it does not mean removing equations, implementation details, or methodological criticism. “Thorough but not repetitive” means progressive disclosure: lead with the canonical TL;DR and mental model, then develop the causal history, mechanism, evidence, derivations, and source notes without restating the same point.

## When to Use

Use this skill when the user asks for:

- a deep Chinese explanation of a recent ML, LLM, agent, multimodal, evaluation, safety, systems, robotics, or embodied-AI paper;
- a weekly-paper-style research artifact even when invoked manually;
- a Notion research entry plus a nine-image social carousel;
- an explanation that separates paper claims, verified facts, engineering inference, and criticism.

Do not use the full publication workflow for:

- a quick abstract summary;
- writing or reviewing the user's own paper;
- bulk literature reviews with no selection objective;
- automatically creating cron jobs, GitHub Actions, systemd timers, Notion Workers, reminders, or any other schedule. Scheduling is outside this skill and requires a separate explicit user instruction.

A related but lighter **candidate-shortlist mode** is in scope when the user asks to research recent papers and produce an auditable shortlist before choosing a focal paper. In that mode, run Steps 1–5 only, stop after the ranked selection report, and do not create the long-form article, nine cards, Notion page, or WeChat notice unless separately requested. See `references/auditable-shortlist.md` for the compact research and reporting contract.

## Non-Negotiable Output Contract

### Notion

- Put the complete explanation in Notion.
- Prefer an existing research database over creating a parallel database.
- Create one record per paper; use the record body for the full article.
- Start the main conclusion with the literal prefix `TL;DR` and treat that paragraph as the canonical summary reused, with format-appropriate editing, in the carousel and share copy.
- Give every share copy a concise, platform-neutral title separate from its `TL;DR` body, so the same package can be adapted to title-bearing platforms such as 小红书 and titleless channels such as朋友圈.
- Explain specialized concepts when they first become necessary: what the term means, why the problem requires it, how it relates to adjacent concepts, and one concrete example or contrast.
- Represent every displayed formula with a native Notion `equation` block or inline equation expression containing valid KaTeX-compatible LaTeX. Never publish formulas as plain text or code blocks.
- Keep the article body free of carousel interruptions. After the article and source section, append one final `分享发布包` containing a visible share-copy title, the `TL;DR`-led body, original versioned paper URL, and all nine images in numerical order.
- Read the page back after publishing and verify its parent, title, sections, source links, native equation blocks, final publication-package placement, and image count.

### Images

- Produce exactly nine portrait PNG files, each `1080×1920` (`9:16`). This mobile-first ratio is the default because it supports dense Chinese explanation at readable phone size; do not silently switch to square or landscape cards.
- Make the carousel text-first and diagram-second. Each card must teach part of the paper with substantial explanatory prose; charts and diagrams support the explanation rather than replace it.
- Target roughly 250–450 Chinese characters on a typical content card, adjusted for equations and diagrams. Preserve readable hierarchy and line length; “more text” does not authorize tiny fonts or an undifferentiated wall of text.
- Save and upload all nine to the final publication package at the end of the Notion page; do not interleave them with article sections.
- Do not attach or send the images through WeChat.
- Use deterministic HTML/CSS/SVG, Canvas, matplotlib, or equivalent for text, formulas, diagrams, and charts. Do not rely on text-to-image generation for factual text, equations, tables, or numeric results.
- Generative imagery may be used only as optional decoration after checking that it introduces no factual claims.
- The ninth card and the share copy must include the immutable original paper link; use a short readable URL when possible, not a private Notion URL or inaccessible QR code.

### WeChat

- Send text only.
- Keep the notice to one short paragraph, normally two or three sentences.
- State the paper/topic, one-sentence value, and exact Notion location or page title.
- Do not reproduce the article, attach the nine images, or imply that images were sent to WeChat.

Suggested pattern:

> 本周论文精读已完成：《{paper_title}》。它主要研究{problem}，核心价值是{value}. 完整讲解和九张分享图片已放在 Notion → {notion_location}，可在页面底部手动下载。

## Default Configuration

Use these defaults unless the user provides different values:

| Setting | Default |
|---|---|
| Output language | Chinese; retain precise English technical terms on first use |
| Audience | Technically literate engineering undergraduate encountering many paper-specific concepts for the first time; scaffold concepts without diluting rigor |
| Scope | ML, LLM, agents, multimodal AI, evaluation, inference systems, robotics, embodied AI |
| Recency window | Prefer the last 21 days; expand to 90 days when no candidate clears the quality gate |
| Selection mode | Best-for-user editorial choice after all research lanes converge and finalists receive normalized scoring plus pairwise comparison |
| Main reading time | About 15–25 minutes, excluding optional deep-detail sections |
| Card dimensions | `1080×1920` portrait PNG (`9:16`), nine files |
| Card editorial mode | Text-first, approximately 250–450 Chinese characters per content card; charts/diagrams are supporting evidence |
| Visual direction | Mobile editorial / technical research note; strong hierarchy, high contrast, readable long-form Chinese, restrained decoration |
| Formula format | Native Notion equation blocks or inline equations using KaTeX-compatible LaTeX; never plain-text formulas |
| Notion destination | Existing Research Library database or user-configured equivalent |
| Publication package | At the end of the Notion page: share-copy title + TL;DR body + original paper URL + nine cards |
| WeChat delivery | Text-only completion notice |
| Automation | Manual by default. An explicitly authorized outer scheduler may invoke one run at a time; the run itself never creates or mutates schedules. |

## Scheduling and Cadence Contract

Scheduling is outer orchestration, not a side effect of one paper run. Create or change it only after a separate explicit user instruction.

- Record invocation mode as `manual` or `externally_scheduled` in the run manifest.
- Before creating a recurring job, list existing jobs and reuse or update the matching job; keep one cadence owner for this workflow.
- Attach this skill to a self-contained scheduled prompt. Fresh cron sessions have no current-chat context, so include selection scope, convergence barriers, Notion publication/readback, nine-card requirements, titled share copy, delivery format, duplicate policy, and failure behavior.
- Distinguish a strict elapsed-time interval from a calendar schedule. “Every three days” normally means a 72-hour interval; day-of-month cron expressions such as `*/3` do not preserve that interval across month boundaries.
- When the user specifies a first date or local time, persist an explicit timezone-aware first-run anchor and read back the actual `next_run_at`; never infer the first fire from the display string alone. State whether daylight-saving transitions preserve elapsed time or wall-clock time.
- A scheduled publication cycle is a delivery commitment, not merely a research attempt. Keep working until one eligible paper is published and read back successfully. A required delegated lane that remains `pending`, times out, or fails is work the parent agent must take over; it is not a valid reason to end the cycle.
- Candidate rejection triggers fallback selection. If the leading candidate fails an evidence, credibility, audit, duplicate, source-access, or teachability gate, record the reason and evaluate the next-ranked candidate. Expand from 21 to 90 days when needed, then use the strongest not-recently-covered paper in the maintained frontier backlog. Do not lower evidence or credibility gates to satisfy cadence.
- Persist `manifest.json` and publication checkpoints after every major stage. On retry or process interruption, resume the incomplete cycle before starting a new issue, reuse the same immutable run identity, and update an existing Notion draft idempotently rather than creating a duplicate.
- The only acceptable scheduled-cycle failure is a concrete external blocker that continued work cannot resolve in the run, such as invalid credentials, persistent provider/API outage after retries and fallback, inaccessible Notion destination, or unavailable primary evidence across all fallback candidates. `pending workers`, `time budget exhausted`, `provisional leader selected`, and `audit incomplete` are not acceptable final states: continue in the parent agent or switch candidates.
- Keep the agent active while work remains. Current Hermes cron uses an inactivity watchdog rather than a fixed wall-clock deadline; do not voluntarily stop at an arbitrary publication window while useful foreground work can continue.
- A scheduled run must not create, update, or recursively arrange cron jobs. Cadence changes happen outside the run by updating the existing outer job.
- When the user asks to slow down, speed up, pause, or resume, identify the existing job first and modify it in place rather than adding an overlapping schedule.
- Verify scheduler/ticker health, enabled state, delivery target, attached skill, interval semantics, and at least the next several local run times before reporting success.

See [`references/recurring-publication-operations.md`](references/recurring-publication-operations.md) for the setup, verification, cadence-change, and DST checklist. For a full run invoked by an outer scheduler, also follow [`references/bounded-scheduled-run-orchestration.md`](references/bounded-scheduled-run-orchestration.md): bound delegated lanes, require parent takeover, apply candidate fallback, persist resumable checkpoints, and continue through publication/readback.

Do not hard-code private page IDs, database IDs, API keys, local personal paths, or delivery channel IDs into a public copy of the skill. Resolve them from runtime configuration or the current user context.

## Artifact Workspace

Create an isolated run directory. Never mix generated paper assets with shared attachment directories.

```text
weekly-paper/{YYYY-MM-DD}-{paper-slug}/
├── manifest.json
├── metadata.json
├── selection-report.md
├── paper.pdf
├── source-notes.md
├── claims-ledger.md
├── explanation.md
├── notion.md
├── share-copy.md
├── carousel-storyboard.md
├── render/
│   ├── index.html
│   └── assets/
└── images/
    ├── 01-cover.png
    ├── 02-problem.png
    ├── 03-prior-limits.png
    ├── 04-core-idea.png
    ├── 05-architecture.png
    ├── 06-mechanism.png
    ├── 07-evidence.png
    ├── 08-limitations.png
    └── 09-takeaways.png
```

`manifest.json` is the run's source of truth. Record:

- immutable paper identifier and version;
- source URLs and retrieval dates;
- selected Notion parent/database at runtime;
- artifact paths and SHA-256 hashes;
- render dimensions;
- validation results;
- Notion page ID/URL only after successful creation;
- publication state: `draft`, `validated`, `published`, or `failed`.

Never store credentials, cookies, authorization headers, or private Notion content in the manifest.

## Workflow

### 1. Resolve Runtime Scope

Before researching, establish:

- run date and timezone;
- invocation mode: `manual` or `externally_scheduled`, including the outer job identity when scheduled;
- target research scope;
- user background and desired depth;
- Notion destination available to the integration;
- whether the user nominated a paper or expects autonomous selection.

Check existing Notion records and previous local manifests to avoid selecting or publishing the same paper twice. Completion criterion: the run has an explicit scope, output location, and duplicate check.

### 2. Build the Candidate Pool

When no paper was nominated, collect roughly 20–40 candidates from primary or near-primary sources:

- arXiv categories such as `cs.LG`, `cs.CL`, `cs.AI`, `stat.ML`, and when relevant `cs.CV` or `cs.RO`;
- OpenReview and official conference proceedings;
- official laboratory/project pages;
- author-linked code repositories;
- Semantic Scholar only for metadata, citation context, references, and discovery—not as a substitute for reading the paper.

Prefer papers submitted or materially revised within the configured recency window. Check the abstract for withdrawal/retraction notices. Record title, authors, date, version, verified venue/review status with its supporting source and verification date, abstract, project page, code, and candidate rationale. arXiv moderation and endorsement are not peer review; an arXiv-hosted paper may still have a separate accepted venue record.

Do not infer quality from author fame, institution, social-media attention, or citation count alone. Completion criterion: each candidate has enough primary-source metadata to score without guessing.

#### Parallel Research Convergence and Parent-Takeover Barrier

Delegation accelerates candidate discovery; it never transfers responsibility for completion away from the parent run.

- Register every delegated lane in the run manifest with status `pending`, `completed`, `failed`, `timed_out`, or `parent_completed`.
- Give each lane a bounded output contract and deadline. Continue useful foreground work while delegates run instead of waiting idly.
- Do not lock the focal paper, mark selection complete, start the long-form draft, render cards, publish, or launch winner-specific methodological/code audits while a required candidate scope is genuinely unexamined.
- At the lane deadline, reconcile returned work once. For every missing, failed, or timed-out lane, the parent agent must immediately perform the minimum complete primary-source scan itself and mark that lane `parent_completed`. Never end a scheduled cycle because a background child is still pending; background delegation is process-local and may be discarded when the parent run exits.
- Consolidate all completed and parent-completed lanes into one cross-domain shortlist, normalize their scoring rubric, and explicitly compare the selected paper against each lane's top recommendation.
- If a candidate fails a hard gate, record the rejection and continue to the next-ranked candidate. If no candidate in the 21-day pool clears the gates, expand to 90 days; if still necessary, use the maintained not-recently-covered frontier backlog. Preserve the gates.
- A paper may still be chosen for editorial fit rather than highest numeric score, but the trade-off must be written after all required scopes have terminal evidence.

Completion criterion: every required research scope is `completed` or `parent_completed`, and the selection report records convergence plus candidate fallback decisions before the editorial choice.

### 3. Score and Select

Score each serious candidate from 0 to 5 on:

| Dimension | Question |
|---|---|
| Novelty | Does it introduce a materially new mechanism, finding, formulation, or capability? |
| Importance | Could the contribution change research or engineering practice? |
| Evidence | Do experiments, baselines, ablations, and controls support the central claim? |
| Reproducibility | Are code, data, models, or sufficient implementation details available? |
| Credibility | Is review status clear, and are there obvious methodological red flags? |
| User relevance | Does it connect to the user's interests and current technical level? |
| Teachability | Is there a coherent insight worth explaining deeply? |

Apply hard gates before ranking:

- reject withdrawn or retracted papers;
- reject papers whose central claim cannot be checked from accessible sources;
- reject pure marketing material presented as research;
- reject near-duplicates of recently covered papers unless the new work materially changes the conclusion;
- require `Evidence ≥ 3.5/5` and `Credibility ≥ 3.5/5` for an autonomous “best paper” claim; in a scheduled cycle, follow the 21-day → 90-day → not-recently-covered backlog fallback until one candidate clears both gates. In a manual shortlist-only request, a truthful no-selection result is allowed.

For this user, define best fit explicitly rather than pretending there is an objective universal winner. After the gates, compute a normalized weighted score:

```text
User relevance 25% + Evidence 20% + Importance 15% + Teachability 15%
+ Reproducibility 10% + Novelty 10% + Credibility 5%
```

Then perform a qualitative pairwise review of at least the top three finalists. Prefer papers that connect to the user's durable interests in AI agents, robotics/embodied systems, deployable software, ML, simulation, and real-world engineering, while still teaching a transferable mechanism. Do not overfit to a single topical keyword: evidence quality and a coherent causal story remain hard constraints. The final report must state:

1. why the winner is the best learning and engineering investment for this user now;
2. why each runner-up lost despite its strengths;
3. whether the choice follows the weighted score or an explicit editorial override;
4. what new evidence would change the decision.

Write `selection-report.md` with the converged shortlist, normalized seven-dimension scores, hard-gate results, pairwise finalist comparison, rejection reasons, and final editorial choice. Verify whether the selected work is peer-reviewed, accepted, under review, or a preprint with no publicly verifiable acceptance record; never infer this from arXiv hosting alone. Check official venue/proceedings, DOI, OpenReview decision, and arXiv `journal_ref`/comments as applicable, following [`references/publication-status-verification.md`](references/publication-status-verification.md). Completion criterion: another reviewer can reconstruct both why this paper is strong and why it is the best fit for this user among the inspected alternatives.

### 4. Acquire and Freeze Sources

Fetch and preserve:

- the exact versioned paper PDF or official proceedings version;
- appendix/supplementary material;
- official project page;
- official code repository and relevant README/config files;
- dataset/model cards when central to the claims;
- a small set of directly relevant prior papers needed for comparison.

Use the immutable version actually read, such as `arXiv:2501.01234v2`, rather than citing an unversioned URL alone. Note later revisions but do not silently mix results across versions.

Prefer source hierarchy:

```text
paper/proceedings → appendix → official code/data → author project page
→ conference/repository metadata → high-quality secondary commentary
```

Secondary commentary can identify questions but cannot override primary evidence. Completion criterion: every central claim has an accessible source and version.

### 5. Build a Claims Ledger

Create `claims-ledger.md` before drafting prose. For each consequential claim, record:

- claim text;
- type: `paper claim`, `observed result`, `engineering inference`, or `editorial judgment`;
- exact source location: section, equation, table, figure, appendix, or code file;
- supporting numeric value when applicable;
- confidence and caveat.

Never copy a chart value from visual estimation when an exact table or source file exists. Never turn “associated with” into “causes,” or “outperforms on selected benchmarks” into “is generally superior.” Completion criterion: central claims, formulas, and reported metrics are traceable.

#### Critical Audit Convergence and Candidate-Fallback Barrier

Independent methodological/code audit remains a hard dependency of publication, but a delegated auditor is never a single point of failure:

- register each audit lane separately from candidate-discovery lanes;
- do not finalize `notion.md`, render the final carousel, create/update the Notion record, or send the completion notice while required audit questions remain unanswered;
- require the audit to check formula/implementation metric alignment, aggregation estimators, denominator conventions, task-sampling balance, judge information leakage/configuration, headline-versus-diagnostic scoring, causal language, and whether the pinned public release can reconstruct reported results;
- assign bounded delegate deadlines; when an audit delegate is missing, failed, or timed out, the parent agent must execute the checklist directly against the frozen paper, appendix, code, and data and mark it `parent_completed`;
- incorporate material findings into the claims ledger, limitations section, share copy, and affected cards;
- if the completed audit invalidates the candidate's evidence or credibility gate, reject that candidate and resume at source-freeze/audit for the next-ranked eligible candidate. Do not publish an `audit incomplete` artifact and do not end with a provisional winner.

Completion criterion: every required audit question is answered by a `completed` or `parent_completed` lane and every material finding is incorporated or explicitly rebutted before publication. For agent/tool-use benchmarks, execute [`references/agent-benchmark-methodological-audit.md`](references/agent-benchmark-methodological-audit.md). For autonomous-driving, robotics, embodied-AI, simulator, procedural-generation, self-play, or RL-system papers, also run [`references/embodied-simulation-method-evidence-reproduction-audit.md`](references/embodied-simulation-method-evidence-reproduction-audit.md).

### 6. Develop the Teaching Model

Explain in the order a reader needs, not necessarily the paper's section order:

```text
historical motivation → concrete problem → prerequisite mental model → old approach
→ precise bottleneck → core intuition → data flow → objective/mechanism → evidence → limits
```

Use **first-use concept onboarding**. When a specialized term first becomes necessary, explain it locally before relying on it:

1. one precise sentence defining the concept;
2. the problem it solves or the failure that motivates it;
3. its relationship to the nearest familiar concept, including the important difference;
4. one concrete running example tied to the paper;
5. the notation or implementation form used later.

Do not front-load a disconnected glossary, explain common undergraduate concepts, or replace technical names with vague metaphors. A reader should be able to enter the paper from adjacent engineering knowledge while still learning the real vocabulary.

For each core module, state:

- input and output;
- learned parameters and fixed quantities;
- dependencies on other modules;
- training-time versus inference-time behavior;
- reason for the design;
- what an ablation says happens when it is removed.

For each essential equation:

1. define every symbol;
2. identify variables, parameters, constants, and expectations;
3. explain the optimization direction in plain Chinese;
4. connect it to the implemented algorithm;
5. contrast it with the prior objective;
6. avoid presenting a derivation the paper does not justify.

Author equations once in valid KaTeX-compatible LaTeX and preserve that source through publication. In Notion, use:

- a block of type `equation` with `equation.expression` for displayed formulas;
- inline rich text of type `equation` for symbols embedded in prose.

Never represent a formula with Unicode approximations, monospaced plain text, fenced code, or a screenshot when native equations are possible. After publication, read the blocks back and verify the expression strings and surrounding symbol definitions.

Use a concrete running example when possible. Completion criterion: the reader can verbally reconstruct the historical motivation, mechanism, data flow, and meaning of the essential equations without rereading the paper.

### 7. Write the Notion Article

Draft `notion.md` with this adaptable structure:

1. **TL;DR** — one canonical paragraph integrating the problem, causal mechanism, strongest evidence, practical value, and principal limitation.
2. **论文档案** — title, authors, institution, immutable version, date, venue/review status, original paper/project/code links.
3. **来龙去脉：为什么会出现这个问题** — historical motivation, prior assumptions, and the concrete failure that made the work necessary.
4. **理解它需要什么** — first-use explanations of only the necessary concepts, connected to a running example.
5. **旧方法为什么不够** — precise bottleneck and fair comparison, not a straw man.
6. **一句话核心直觉** — mechanism in one sentence, consistent with the TL;DR.
7. **方法总览** — end-to-end data flow and architecture diagram.
8. **逐层拆解** — modules, representations, training, inference, and algorithm.
9. **关键公式** — native Notion LaTeX equations, followed by symbol-by-symbol and optimization explanations.
10. **实验读法** — setup, baselines, main results, ablations, efficiency, generalization, and uncertainty.
11. **论文证明了什么，没有证明什么**.
12. **局限、争议与复现风险**.
13. **对研究与工程的意义** — when to use, when not to use, and transferable lessons.
14. **术语与概念回看** — a compact reference after concepts have already been taught at first use.
15. **来源与延伸阅读** — original versioned paper URL first, then project, code, data, and directly relevant prior work.
16. **分享发布包（页面末尾）** — visible share-copy title, the `TL;DR`-led body from `share-copy.md`, then all nine images in order; nothing follows this package.

Use progressive disclosure. Keep the main path readable in about 15–25 minutes; put optional derivations, implementation details, and extended source notes in toggles/details blocks. Do not satisfy “thorough” by repeating the same point. The article should assume technical maturity but not prior specialization: explain the causal history and unfamiliar mechanisms concretely before using them in dense analysis.

Apply restrained Chinese connective style across the Notion article, carousel, share copy, and WeChat notice. Do not use “不是……而是……” or “不仅……而且……” as habitual rhetorical templates. Use them only when the contrast, correction, or additive progression is genuinely necessary for logical precision and a simpler direct sentence would lose meaning. During editing, search for repeated instances and rewrite avoidable ones into direct statements, parallel clauses, or explicit causal relations; preserve the connective when it materially clarifies the argument.

Use original simplified diagrams or attributed redraws. If reproducing a paper figure, preserve the caption context and identify the source. Completion criterion: the article is approachable on first reading, retains equations and methodological depth, and ends with a self-contained publication package rather than interrupting the article with cards.

### 8. Create the Nine-Card Storyboard

The cards are a self-contained, text-first mobile editorial edition of the article—not article screenshots, sparse posters, or chart galleries. Adapt the emphasis to the paper while keeping this default sequence:

1. **封面 + TL;DR** — title, canonical summary, authors/version, and why it matters.
2. **来龙去脉与研究问题** — the historical path to the problem, stakes, and precise bottleneck.
3. **必要概念与旧方法** — teach the unfamiliar concepts needed to understand why the old approach fails.
4. **核心直觉** — a concrete running example, explanatory prose, and only the notation that helps.
5. **整体架构与数据流** — input, representation, modules, training/inference distinction, and output.
6. **关键机制与公式** — valid rendered formula plus symbol meanings, optimization direction, and implementation connection.
7. **关键证据** — setup, exact results, baselines, ablation interpretation, and uncertainty; charts support the prose.
8. **局限、争议与适用边界** — failure modes, cost, evidence gaps, and what remains unproven.
9. **TL;DR 总结与延伸** — integrated takeaways, practical/research significance, immutable paper ID, and original paper URL.

Each card must have:

- one primary section of the paper's argument, but enough prose to explain rather than merely label it;
- a short headline followed by structured paragraphs, bullets, callouts, or equation explanation;
- roughly 250–450 Chinese characters on a typical content card; use fewer only when a genuinely necessary diagram or equation requires space;
- readable Chinese at phone size, with a tested body-font threshold and comfortable line length;
- charts and diagrams occupying no more space than their evidential role warrants;
- consistent color, typography, margins, and diagram language;
- page number such as `5/9`;
- short immutable paper identifier/source footer;
- no QR code to a private Notion page.

Completion criterion: a reader can learn the paper's motivation, concepts, mechanism, evidence, and limits from cards 1–9 alone, without opening Notion, while every card remains readable on a phone.

#### Share Copy Contract

Create `share-copy.md` as the canonical platform-neutral copy paired with the nine cards. Structure it as:

```markdown
# {concise share title}

TL;DR：{integrated body}
```

It must:

- include one concise, informative title that works as a 小红书 title and can be omitted when posting to a titleless channel;
- start the body, immediately after the title, with the literal prefix `TL;DR`;
- synthesize the paper's problem, causal mechanism, strongest evidence, practical/research value, and principal limitation rather than merely announce publication;
- use clear Chinese suitable for a technically curious cross-platform audience without assuming they read the Notion article;
- include the immutable original paper URL in plain clickable form;
- avoid a private Notion URL as the only source;
- stay concise enough to post as one body while still functioning as the integrated summary of the article and cards.

The Notion page's opening TL;DR, card 1/card 9 summaries, and share copy must agree on the central claim and evidence boundary, but should be edited for their different reading contexts rather than copied mechanically. Completion criterion: `share-copy.md` contains one title, its body starts with `TL;DR`, it contains the exact versioned paper URL, and the Notion `分享发布包` visibly places the title and body immediately before the nine images.

### 9. Render Deterministically

Build the cards in HTML/CSS/SVG or another deterministic renderer. Prefer browser rendering with embedded CJK fonts and KaTeX/MathJax because it supports dense editorial typography and native vector equations. When required libraries or system packages such as Chromium runtime dependencies are missing, first confirm the target environment and use an existing user authorization to install the minimal system dependencies; verify that no production service is affected. Do not downgrade output quality merely to avoid a permitted dependency installation. Keep Pillow/SVG as a tested fallback, not the default excuse for a broken browser environment.

Recommended constraints:

- fixed viewport `1080×1920` (`9:16` portrait);
- embedded or reliably available CJK font;
- safe margins of at least 72 px horizontally and 84 px vertically;
- tested mobile-readable body font and line height; never solve overflow by shrinking all text;
- explicit text regions with overflow detection and enough capacity for 250–450 Chinese characters;
- charts redrawn from exact source values and subordinate to explanatory text;
- formulas rendered by KaTeX/MathJax or vector output;
- no external asset that may expire before rendering.

Render all nine, then programmatically check:

- file format is PNG;
- dimensions are exactly `1080×1920`;
- filenames are `01` through `09` with no gaps;
- files are non-empty and decodable;
- no browser console/render errors;
- no clipped or overflowing text elements, including children clipped inside `overflow:hidden` / `overflow:clip` panels; a page-level `scrollHeight` check is insufficient;
- flex/grid content panels cannot silently shrink below their content height (`flex-shrink: 0`, suitable `min-height`, or equivalent), and every text-bearing child's rectangle is checked against both its clipping parent and the page boundary;
- every formula container has a visible KaTeX/MathJax layer, no render-error node, and no leaked command names such as `operatorname`, `mathcal`, `frac`, or `mathbf`;
- geometry checks ignore only KaTeX's hidden accessibility MathML layer while continuing to inspect the visible formula layer;
- each content card meets the storyboard's required prose coverage unless an explicit exception is recorded.

Perform visual inspection of every card at full resolution and phone-scale preview. Automated geometry checks do not catch poor hierarchy, misleading arrows, unreadably dense text, decorative charts that displace explanation, or syntactically accepted formulas rendered with the wrong escaping. Compare every visible formula with its canonical LaTeX source and meaning. Completion criterion: exactly nine visually reviewed, technically accurate, text-first portrait PNGs.

### 9.5 Harden a Full Manual Pilot

For a full manual run, add these safeguards before publication:

1. **Evidence outranks thematic fit.** A highly relevant paper with missing code/data or unverifiable central evidence must lose reproducibility points. Preserve the shortlist, analyst scores, and rejection reasons.
2. **Freeze paper and code separately.** Pin the paper version and hash the acquired source when possible; pin every inspected repository to an exact commit. Compare the paper appendix against the pinned README/config/scripts and disclose recipe drift.
3. **Recalculate headline numbers.** Distinguish percentage-point gains from relative percentages. If a displayed table lacks the baseline needed to reconstruct a headline multiplier, call it an author claim rather than a verified result.
4. **Smoke-test Chinese rendering early.** Exercise the intended renderer and font on one small card before laying out all nine. Keep a deterministic Pillow/SVG fallback instead of treating a temporary backend failure as a permanent restriction.
5. **Use two-pass visual and formula-semantic QA.** Validate files and dimensions, inspect a 3×3 contact sheet, zoom suspect cards, fix issues, then regenerate the contact sheet. For formula cards, distinguish hidden KaTeX MathML from the visible HTML layer, reject leaked LaTeX command names, and compare the rendered meaning against the canonical source. Explicitly check edge overflow, same-color labels on bars, maximum-bar label overlap, and tofu boxes from unsupported mathematical combining marks.
6. **Resolve Notion live.** Treat cached IDs as hints, distinguish database page IDs from `data_source_id`, read the current schema and select options, and query by immutable paper URL before creation.
7. **Verify the published media, not only block metadata.** Re-download all nine Notion-hosted images, decode them, and confirm `1080×1920`, ordered captions, required article sections, native equation blocks, the final `分享发布包`, and exactly one matching Source URL record.
8. **Count Chinese as Unicode characters.** Do not compare UTF-8 bytes to character thresholds; combine Unicode character coverage with required-section checks.
9. **Re-check scheduler state at the end.** In `manual` mode, claim “no automation created” only after a fresh scheduler check. In `externally_scheduled` mode, verify that the run did not create or mutate jobs and that the single authorized outer job remains enabled with the expected next run.
10. **Converge all background work before completion.** Before publication and again before the final notice, reconcile every process, delegated audit, upload, renderer, and verification lane recorded by the run. In a scheduled cycle, required research/audit work must be `completed` or `parent_completed`; delegate failure, timeout, or waiver triggers parent takeover rather than publication. Nothing material may remain `running` or `pending`. If a delayed completion notification arrives after parent takeover, compare it with the current manifest and artifact hashes: incorporate material new evidence, acknowledge harmless duplicate completion without rerunning, and never treat the delayed notification as proof that earlier verification occurred.

See [`references/manual-pilot-lessons.md`](references/manual-pilot-lessons.md) for condensed failure modes, the current Notion Direct Upload pattern, and a reusable read-back contract. See [`references/formula-rendering-and-notion-resume.md`](references/formula-rendering-and-notion-resume.md) for KaTeX visible-layer checks, HTML backslash rules, command-leak sentinels, CLI-independent uploads, and resumable Notion batching.

### 10. Publish to Notion Idempotently

Before creating a record, query the destination by immutable paper ID/URL and normalized title. If a matching draft exists, update it rather than creating a duplicate. Do not overwrite an existing user-edited page without inspecting it and preserving user content.

Populate available database properties, for example:

- title;
- type = Paper;
- topic/tags;
- source URL;
- authors;
- publication or review status;
- published date and added date;
- summary and key findings;
- reliability/evidence status.

Write the complete body with native Notion equation blocks/inline equations, then append the final `分享发布包`: a visible share-copy title, `TL;DR`-led body, immutable original paper URL, and all nine PNGs in numerical order. Do not place carousel images between article sections and do not append article content after the package. Finalize critical audit findings before creating this ordering: Notion API versions may reject middle insertion fields such as `after`, so late audit text can otherwise require destructive block rebuilding. For long pages, persist a publication checkpoint containing `page_id`, total block count, and the next uncommitted block index; append in API-sized batches and resume from the checkpoint rather than creating another page. If a convenience upload CLI is unavailable, preserve the publication design by using the official `file_uploads` create/send lifecycle, testing one image end to end before batching the remaining eight. When replacing an existing image block under API `2026-03-11`, the update body may require `image.file_upload` plus `caption` while rejecting an explicit `image.type`; follow the current official schema and verify by downloading the materialized block image and comparing its hash with the local PNG. Then read back:

- page ID and parent;
- title and metadata;
- opening `TL;DR` and presence of every required article section;
- every expected native equation expression;
- the final `分享发布包`, including a visible share-copy title, `TL;DR`-led body, and immutable original paper URL;
- all nine image blocks/files, after the article and in numerical order;
- source links;
- absence of duplicate records.

Set manifest state to `published` only after readback passes. Completion criterion: the Notion record—not the local draft—is complete and verified.

### 11. Send the Text-Only WeChat Notice

Only after Notion readback succeeds, send the short notice. It must:

- begin with or immediately convey the canonical TL;DR;
- identify the paper/topic;
- state one reason it matters;
- include the immutable original paper URL;
- name the Notion location/page;
- say that the nine portrait images and share copy are in Notion for manual use;
- contain no `MEDIA:` attachments and no image URLs intended for chat delivery.

If publication or validation fails, do not say “已完成.” Send a compact failure status only when the user expects a result, identifying the failed stage and whether a safe retry is possible.

Completion criterion: the notice truthfully matches the verified Notion state and is text only.

## Maintainer Sync Contract

The installed skill and its public source repository are one maintained artifact:

```text
https://github.com/Mike-Zhuang/weekly-frontier-paper-deep-dive-skill
```

For this user, a local modification to this skill is incomplete until the public repository is synchronized. After editing:

1. validate local frontmatter, linked references, internal consistency, and size limits;
2. clone or open the repository and inspect branch/status/remote before writing;
3. copy only the reusable skill files and public documentation—never runtime manifests, generated papers, Notion content, credentials, memories, caches, or private IDs;
4. review the Git diff and run a secret/private-ID scan;
5. commit and push to `main` under the user's standing authorization for this repository;
6. fetch the remote raw files and verify their hashes match the installed local files;
7. report the commit SHA and synchronization result.

If authentication, branch protection, network access, or validation blocks the push, keep the local improvement but explicitly report `local updated, GitHub sync failed`; do not call the skill update complete. This sync contract does not authorize publishing generated paper artifacts or creating GitHub Actions.

## Failure Handling

- **No candidate clears the quality gate:** for an autonomous scheduled cycle, reject failed candidates explicitly, expand from 21 to 90 days, then inspect the maintained not-recently-covered frontier backlog until one candidate clears the unchanged gates. A manual candidate-shortlist request may instead truthfully report no selection.
- **Delegated lane is pending, failed, or timed out:** stop waiting and complete that bounded research/audit scope in the parent agent. `pending` is not a scheduled-run terminal state.
- **Selected candidate fails audit or source freeze:** record the reason and switch to the next-ranked eligible candidate; reuse generic preflight work and do not restart the entire cycle.
- **PDF extraction fails:** try official HTML, proceedings source, or local PDF extraction/OCR; disclose missing sections.
- **Code is unavailable:** mark reproducibility accordingly; do not invent implementation details.
- **Metrics conflict across versions:** freeze one version and describe the conflict explicitly.
- **Image render fails:** retry the affected card after identifying the layout/font/asset cause; do not publish eight cards as a nine-card set.
- **Notion upload partially succeeds:** keep manifest state out of `published`, inspect the page, and idempotently repair missing content.
- **WeChat delivery is unavailable:** preserve the verified Notion page; do not alter the research artifact merely to force notification.

## Common Pitfalls

1. **Recency bias:** newest is not necessarily frontier. Use the evidence and importance gates.
2. **Premature selection:** parallel candidate research must converge before locking the paper.
3. **Generic rather than user-best selection:** apply the user-fit weights and explain why the winner beats each finalist.
4. **Abstract-only explanation:** read methods, experiments, appendix, and code before teaching the mechanism.
5. **Authority bias:** famous authors and institutions do not replace methodological scrutiny.
6. **Claim inflation:** keep benchmark-specific improvements scoped to their actual setting.
7. **Version drift:** record and cite the exact version read.
8. **False precision:** do not infer exact chart values from pixels when raw values are unavailable.
9. **Concept name-dropping:** define unfamiliar concepts at first use and place them in the causal chain.
10. **Plain-text formulas:** publish native Notion LaTeX equations and verify the expression strings.
11. **Escaped-command leakage:** exact dimensions and zero overflow do not prove a formula rendered correctly; reject visible `operatorname`/`mathcal`/`frac` command text and inspect the visible KaTeX layer.
12. **Formula dumping:** every displayed equation must change the reader's understanding.
13. **Sparse poster cards:** the carousel is a text-first teaching artifact, not a decorative chart gallery.
14. **Unreadable text density:** use the 9:16 canvas and hierarchy; do not shrink type to fit unedited prose.
15. **Scattered carousel:** keep all nine cards in the final publication package, never between article sections.
16. **Long-form repetition:** use progressive disclosure instead of restating the same contribution.
17. **Generative text in images:** text-to-image is unsuitable for factual Chinese text and equations.
18. **Private-link QR codes:** a QR code is useless if the Notion page is not publicly accessible.
19. **Premature completion:** local files do not prove Notion publication; read the page back.
20. **Wrong delivery channel:** the nine images belong in Notion, not WeChat.
21. **Unauthorized automation:** loading this skill never authorizes creating a recurring job or other trigger; scheduling requires a separate explicit request.
22. **Duplicate or drifting cadence:** do not create a second job when the user changes frequency, do not use day-of-month `*/N` as a strict N-day interval, and do not report success before reading back the persisted first run and next run.
23. **Delegation as a single point of failure:** broad delegated scans can stall selection or outlive the parent process. Bound candidate counts and deadlines, then have the parent complete missing scopes; do not end the scheduled cycle at the research barrier.
24. **Speculative pre-selection audits:** do not launch winner-specific audits before candidate convergence. They consume concurrency, multiply pending work, and violate the selection-before-audit barrier.

## Verification Checklist

### Research

- [ ] Every required candidate-research lane reached a terminal state before selection.
- [ ] Selected paper passed evidence and credibility hard gates.
- [ ] Seven scoring dimensions were normalized across candidates.
- [ ] Top finalists received a pairwise user-fit comparison and runner-up rejection reasons.
- [ ] The report explains why the paper is the best current learning/engineering investment for this user.
- [ ] Review/publication status is supported by an official venue/proceedings, DOI, OpenReview decision, or explicit scoped absence of a public acceptance record; arXiv hosting alone was not treated as evidence of peer review or non-review.
- [ ] Exact paper version and retrieval date are recorded.
- [ ] Central claims and metrics are traceable in the claims ledger.
- [ ] Every required independent methodological/code audit reached a terminal state before final drafting, rendering, or publication.
- [ ] Material audit findings about estimator/implementation alignment, scoring scope, judge setup, causality, and reproducibility were incorporated or rebutted with evidence.
- [ ] Paper claims, observed results, inference, and editorial judgment are distinguished.

### Explanation

- [ ] Opening conclusion begins with `TL;DR` and is the canonical summary.
- [ ] Main path is understandable without prior specialization.
- [ ] Specialized concepts are explained concretely at first use, with motivation, relation, example, and later notation.
- [ ] Historical motivation and the causal path to the research problem are clear.
- [ ] Core mechanism, inputs/outputs, training, and inference are explained.
- [ ] Essential formulas use valid LaTeX and define every symbol and optimization direction.
- [ ] Experiments are interpreted rather than merely copied.
- [ ] Limitations and what remains unproven are prominent.
- [ ] Main text is thorough without repetitive filler.

### Images

- [ ] Exactly nine PNGs exist.
- [ ] Every image is `1080×1920` and decodable.
- [ ] Cards are text-first and typically contain 250–450 Chinese characters where appropriate.
- [ ] Body text remains readable in a phone-scale preview; no card solves overflow by tiny type.
- [ ] No text-bearing child escapes or is clipped by an `overflow:hidden` / `overflow:clip` parent; flex/grid shrink behavior was explicitly checked.
- [ ] Charts and diagrams support rather than replace explanatory prose.
- [ ] Text, native-rendered formulas, arrows, charts, and source labels were visually inspected.
- [ ] Every formula has a visible KaTeX/MathJax layer, no error node or leaked command names, and matches the canonical LaTeX meaning at full and phone scale.
- [ ] Hidden KaTeX MathML was excluded from false-positive geometry checks without excluding the visible formula layer.
- [ ] Numeric values match the frozen source version.
- [ ] Card 9 contains the immutable original paper URL.
- [ ] No card contains private data or inaccessible private-link QR codes.

### Notion

- [ ] Destination and duplicate check are verified.
- [ ] Database properties and full page body are present.
- [ ] Displayed formulas are native `equation` blocks and inline formulas are native equation rich text; expression strings passed readback.
- [ ] The article body contains no interleaved carousel images.
- [ ] The final section is `分享发布包`: visible share-copy title, `TL;DR`-led body, immutable original paper URL, then all nine images in numerical order.
- [ ] Nothing follows the final publication package.
- [ ] Source links and version information are present.
- [ ] All nine Notion-hosted images re-download and decode to `1080×1920`.
- [ ] Page readback passed and manifest state is `published`.

### Delivery and Scope

- [ ] `share-copy.md` contains one concise title; its body begins with `TL;DR`, functions as an integrated summary, and includes the immutable paper URL.
- [ ] WeChat notice is concise Chinese text only and includes the original paper URL.
- [ ] No image or `MEDIA:` attachment is sent to WeChat.
- [ ] Notice identifies the exact Notion location.
- [ ] Every required background process, delegation, upload, render, and verification lane reached a terminal state before the completion notice.
- [ ] Any delayed completion notification was reconciled against the manifest and artifact hashes without unnecessary reruns.
- [ ] Invocation mode is recorded as `manual` or `externally_scheduled`.
- [ ] In externally scheduled mode, delegated lanes had bounded contracts and deadlines; every missing scope received parent takeover; candidate fallback continued until one paper passed the unchanged gates; and Notion publication/readback completed or a concrete external blocker was recorded with a resumable checkpoint.
- [ ] In manual mode, no cronjob, timer, GitHub Action, Notion Worker, or other automation was created.
- [ ] In externally scheduled mode, the run created or modified no jobs; exactly one authorized outer job remains, and its persisted next run, interval semantics, timezone behavior, skill attachment, and delivery target were verified.

## Manual Invocation Example

> 使用 weekly-frontier-paper-deep-dive 完成一期手动论文精读。等待所有跨领域候选研究完成后，按统一七维评分和用户适配度选出最近三周内最适合我的论文；生成以 `TL;DR` 开头、概念首次出现时具体解释、公式使用 Notion 原生 LaTeX 的完整中文笔记，以及九张文字为主、图表为辅的 `1080×1920` 竖版图片。文章结束后添加一份带标题的分享文案，正文以 `TL;DR` 开头并包含原始论文链接，再依次放九张图。图片只上传 Notion，不在微信发送。完成并回读验证后，微信文字通知也包含原始论文链接。不要创建任何自动化事件。
