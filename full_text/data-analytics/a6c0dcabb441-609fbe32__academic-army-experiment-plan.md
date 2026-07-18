---
name: academic-army-experiment-plan
description: >-
  Create a strategic, evidence-driven academic experiment plan from a research
  idea, paper_blueprint.md, paper claims, storytelling blueprint, target venue,
  existing results, prior plans, or revision feedback. Produces exactly two
  Markdown files: an English AI-facing experiment_plan.md and a Chinese
  human-facing experiment_plan.explain.md. Uses
  academic_army_mcp_tools.deepresearch for live target-venue, influential-paper,
  baseline, dataset/workload, metric, artifact, autoresearch, and reviewer
  expectation research before making claim-to-evidence planning choices.
---

# Academic Army Experiment Plan

## Purpose

Create a strategic experiment plan for an academic paper. The plan turns paper
claims into an evidence strategy that later AI skills can inherit when they
write code, run experiments, plan figures, and draft paper sections.

Own the experiment-strategy layer:

- paper thesis and claim-to-evidence mapping
- experiment objectives and their paper-story roles
- workload/dataset, metric, and baseline strategy
- reader interpretation and reviewer-concern coverage
- ablation, robustness, boundary, and artifact-readiness objectives
- Chinese rationale that lets the user judge whether the strategy is reasonable

Do not execute experiments, write code, prescribe shell commands, create exact
run matrices, fabricate results, or produce final figures.

## Output Contract

Create exactly two Markdown files in the requested output directory:

1. `experiment_plan.md`
   - English.
   - AI-facing.
   - Contains only the strategic experiment plan.
   - Uses stable experiment names, registries, and fields that downstream skills
     can inherit.

2. `experiment_plan.explain.md`
   - Chinese.
   - Human-facing.
   - Starts with the concrete user-provided and locally available planning
     inputs used in this invocation.
   - Explains why the experiment portfolio is reasonable for the paper.
   - Explains choices from the paper thesis, blueprint, target venue, live
     research, existing evidence, and storytelling needs.

Do not create extra output files. Do not put provenance, source summaries,
user-facing review notes, or skill-internal process comments inside
`experiment_plan.md`.

## Inputs To Use

Use supplied or available project context before planning. Prefer
`paper_blueprint.md` when present. Also use prior experiment plans,
preliminary results, revision feedback, target-venue notes, metaskill design
goals, or artifact summaries when they are part of the current task.

Extract or infer:

- paper goal, title, field, subfield, target venue, year, and track
- central research bet and novelty boundary
- main claims and expected reviewer concerns
- storytelling posture: motivation, method insight, main evidence, claim
  boundary, and reader journey
- required or preferred datasets, workloads, baselines, metrics, hardware,
  traces, artifacts, or deployment setting
- known constraints: compute, privacy, data access, unavailable baselines,
  human-subject constraints, deadline, target track, or reproducibility needs
- existing evidence: preliminary numbers, pilot studies, prior figures, logs,
  notes, old experiment plans, reviews, rebuttal feedback, or artifact feedback

Use live research and paper goals to infer nonblocking missing details. Ask for
additional user input only when a missing fact would materially change claim
coverage, workload scale, baseline fairness, ethics, or story placement and no
defensible default can be inferred.

## Required Deepresearch

Use `academic_army_mcp_tools.deepresearch` for every nontrivial plan or
substantive revision after project-specific context is understood.

- Server: `academic_army_mcp_tools`
- Tool: `deepresearch`
- Canonical MCP name when exposed:
  `mcp__academic_army_mcp_tools__deepresearch`

Ask for concise planning lessons, not a literature review. The prompt should
cover multiple perspectives:

- current or recent target-venue experiment expectations
- high-impact or high-citation papers from the target venue and adjacent top
  venues such as SIGGRAPH, CVPR, SIGCOMM, NSDI, INFOCOM, MMSys, CHI, NeurIPS,
  ICML, ICLR, ACL, or domain-specific venues when relevant
- why those papers' experiments are persuasive: methods, datasets, baselines,
  metrics, result presentation, artifacts, and claim boundaries
- recent methods, datasets, workloads, baselines, metrics, benchmarks,
  artifacts, and result-presentation patterns in the paper's subfield
- motivation or design-insight experiment patterns that make the core intuition
  visible before full-system evaluation
- autoresearch, scientific-discovery, paper-writing-agent, benchmark, prompt
  template, and experiment-automation workflow lessons when they improve
  planning or downstream handoff

The skill defines what to research, not the answer. Do not hardcode mutable
venue norms, current SOTA baselines, or dataset preferences into the skill body;
derive them at invocation time through deepresearch.

For each live-research anchor that changes the plan, record this in
`experiment_plan.explain.md`:

- `source`: title and link
- `date`: visible publication, submission, event, metadata, or page date
- `venue_status`: one of `official_proceedings`, `arxiv_only`,
  `project_page_claim`, `secondary_metadata`, or `classic_background`
- `影响到的规划决定`: the baseline, metric, workload, experiment placement,
  evidence style, artifact expectation, or claim boundary it changed

Use `official_proceedings` only when the venue is confirmed by conference,
proceedings, publisher, DOI metadata, or official venue pages. Use
`arxiv_only` for arXiv records. Use `project_page_claim` for author, lab, or
project claims not confirmed elsewhere. Use `secondary_metadata` for
aggregators or institutional pages. Use `classic_background` for older
foundational precedents.

## Decision Sufficiency Policy

Make goal-oriented choices. Do not transfer obvious decisions to the user.

When user input, the blueprint, existing evidence, and deepresearch make one
choice clearly better for the paper, write that choice into `experiment_plan.md`
and explain the reasoning in Chinese in `experiment_plan.explain.md`.

Keep open variables only when all are true:

- the information cannot be inferred reliably from current inputs or live
  research
- the choice materially changes experiment objectives, claim coverage, workload
  scale, baseline fairness, ethics, or story placement
- downstream skills cannot proceed sensibly without inheriting the uncertainty

Do not create broad lists of questions. Represent nonblocking unknowns as
assumptions, dependencies, optional claim-expansion modules, or handoff notes.
As user-confirmed content and research accumulate, open variables should shrink.

## Planning Method

Build the plan around the paper story, not around a generic evaluation
checklist. The plan must be claim-derived, not template-derived: treat the
template as scaffolding for consistency, and include content only when it
advances a specific paper claim, reader doubt, storytelling need, or downstream
handoff.

1. Normalize the paper into an experimental thesis, primary comparison,
   operating conditions, venue/story evidence posture, and paper-specific claim
   verbs such as demonstrate, isolate, quantify, rule out, stress-test,
   calibrate, validate, attribute, generalize, diagnose, contextualize, or
   explain.
2. Build a claim-to-evidence map before writing individual objectives.
3. Define workload/dataset, metric, and baseline registries once.
4. Organize experiment objectives by evidence role: motivation, method insight,
   main evaluation, mechanism/ablation, robustness, generalization, contribution
   boundary, human/perceptual evidence, deployment realism,
   cost/scalability, or reproducibility.
5. For each objective, specify the claim supported, reviewer concern answered,
   story placement, evidence scope, workloads, metrics, comparators,
   presentation intent, expected result pattern, reader takeaway,
   claim-calibration output, downstream handoff, dependencies, and priority.
6. Merge objectives that do not have a distinct claim, story role, reader
   takeaway, or primary evidence output. Represent secondary needs as metric
   slices, reporting views, or shared protocols.
7. Put optional broader-scope ideas into claim-expansion modules with activation
   conditions.
8. Explain the rationale in Chinese as a causal argument for the user, not as a
   field-by-field translation.

Motivation and design-insight experiments should make the core intuition visible
early. Use them to show an existing-system defect or a core-mechanism feasibility
signal before full-system evaluation. Their planned result should be immediately
readable: a curve separation, small table, heatmap, qualitative grid, timeline,
breakdown, representative case, or before/after panel.

Use deepresearch-derived venue and paper patterns as experiment-design choices,
not as citations or literature review. Convert them into concrete baseline
families, metric choices, ablation styles, robustness checks, artifact
expectations, and result-presentation intent for the current paper.

Before writing, ask of each experiment: What paper sentence or claim will this
evidence support? What doubt does it remove? Why are these metrics, baselines,
workloads, and ablations the right ones for this claim? What should the reader
conclude? Where will the result appear in the paper? What downstream
writing/figure/table handoff does it enable?

## Strategic Plan Boundary

`experiment_plan.md` should include:

- experimental thesis, primary comparison, and operating conditions
- venue/storytelling evidence posture
- claim-to-evidence map
- workload or dataset registry
- metric registry
- baseline registry
- resource, cost, statistical, and reproducibility principles when relevant
- experiment objectives organized by evidence role
- ablation, sensitivity, robustness, and claim-boundary objectives when needed
- optional claim-expansion modules for broader scope
- main-paper versus supplemental presentation intent at a strategic level
- objective dependency graph

`experiment_plan.md` should not include:

- source summaries or literature review prose
- confirmed-input ledger or user-facing explanation
- implementation owners
- shell commands, scripts, exact run matrices, hyperparameter grids, or code
- concrete output paths, logging schemas, manifest fields, or final figure files
- fabricated numeric results or claims that experiments have succeeded
- user reminders, disclaimers, or sections such as `Assumptions to validate`,
  `Artifact cautions`, or `Do not assume reviewers will run code`

Use logical handles for outputs, such as `substitution_surface`,
`main_qoe_table`, or `stress_regime_matrix`. Later skills choose concrete file
names, logging formats, implementation details, and plotting layouts.

Avoid generic plan content. If a section, heading, experiment name, metric
rationale, baseline choice, or ablation could apply unchanged to another paper,
make it more specific to the current paper's thesis or remove it.

## Registries

Define shared registries once and reference IDs in objectives.

### Workload or Dataset Registry

Separate:

- `Required workloads/datasets`: committed by user input, blueprint, existing
  evidence, or live-research-selected venue protocol.
- `Scope-extension candidates`: broaden scene, data, benchmark, substrate,
  device, deployment, user-study, or contention claims.

Name workload classes or dataset families unless exact datasets are confirmed or
venue norms make a dataset clearly required.

### Metric Registry

Group metrics by evidence role, for example:

- primary claim quality/effectiveness
- latency/deadline/responsiveness
- cost/resource/efficiency
- robustness/stress/generalization
- mechanism/control/action behavior
- statistical reporting
- human/perceptual signal, when relevant

Objectives reference metric IDs only. Do not repeat metric definitions inside
every objective.

### Baseline Registry

Use compact entries:

```markdown
- `baseline_id`:
  - Burden: minimum | diagnostic | optional_expensive
  - Baseline role: canonical | recent_strong | simple | ablated_self | status_quo | oracle | deployment
  - Comparison purpose:
  - Fairness principle:
```

Use baseline ladders:

- canonical baselines expected by reviewers
- recent strong baselines from live research
- simple baselines that test whether complexity is justified
- ablated self-baselines that isolate mechanism
- status-quo or deployment baselines for systems papers
- oracle or upper-bound baselines only when they clarify headroom

Objectives own baseline usage through their `Comparators` field. The registry
defines each baseline once.

## Positive Evidence Language

Write the main plan as a positive evidence specification. Use fields such as:

- `Evidence goal`
- `Evidence scope`
- `Evidence role`
- `Story placement`
- `Reviewer concern answered`
- `Presentation intent`
- `Reader takeaway`
- `Claim calibration output`
- `Expected evidence outputs`
- `Handled by later skills`

Use positive limitation language: `limitation regime`, `unsupported regime`,
`claim boundary`, `stress sensitivity`, and `adaptation attribution`. Use
`failure` only for explicit diagnostic objectives where a failure-analysis
artifact is part of the evidence.

For engineering papers, do not organize the plan around weak-result
contingencies. Plan how the core intuition should be shown and verified. Express
risks as dependencies, open variables, stress regimes, or claim-boundary
objectives.

## `experiment_plan.md` Template

```markdown
# Experiment Plan: <Paper/System Name>

## 1. Experimental Thesis

- Experimental thesis:
- Primary comparison:
- Operating conditions:
- Venue/story evidence posture:

## 2. Claim-to-Evidence Map

| Claim | Reviewer Concern | Evidence Objective | Story Placement | Expected Evidence Output |
| ----- | ---------------- | ------------------ | --------------- | ------------------------ |

## 3. Workload and Dataset Registry

- Required workloads/datasets:
- Scope-extension candidates:

## 4. Metric Registry

- `<metric_id>`:

## 5. Baseline Registry

- `<baseline_id>`:
  - Burden:
  - Baseline role:
  - Comparison purpose:
  - Fairness principle:

## 6. Resource, Cost, and Reproducibility Principles

- Resource/cost reporting:
- Statistical reporting:
- Artifact/reproducibility principle:

## 7. Core Experiment Objectives

### <Experiment Name>

- Story placement:
- Evidence goal:
- Claims supported:
- Reviewer concern answered:
- Evidence scope:
- Evidence role:
- Workloads/datasets:
- Controlled factors:
- Comparators:
- Metrics:
- Presentation intent:
- Expected evidence outputs:
- Expected result pattern:
- Reader takeaway:
- Claim calibration output:
- Handled by later skills:
- Dependencies:
- Priority:

## 8. Optional Claim-Expansion Modules

### <Module Name>

- Module type: claim_expansion_module
- Scope expanded:
- Activation condition:
- Use objective fields only when the module is activated.

## 9. Objective Dependency Graph

- <experiment/output> -> <experiment/output>:
```

Omit empty sections. Keep identifiers natural and readable; avoid abstract ID
systems such as `c1`, `c2`, `b1`, or `m1` unless the source paper already uses
them.

## `experiment_plan.explain.md` Template

Write this file in natural Chinese. English paper titles, venue names, method
names, datasets, benchmarks, and technical terms may remain in English when that
is clearer.

```markdown
# 实验计划说明：<论文/系统名>

## 用户已经明确的内容

记录本轮实际使用的用户指令、论文蓝图、旧计划、反馈、已有结果、目标 venue、约束和实时调研入口。

## 论文核心出发点

解释这篇论文想让审稿人相信什么，以及为什么实验必须围绕这些论点组织。

## 实时调研如何影响实验取舍

| 来源 | 日期 | venue_status | 影响到的规划决定 |
| ---- | ---: | ------------ | ---------------- |

## 实验故事线

用自然语言说明 motivation、method insight、main evaluation、ablation、
robustness、boundary、artifact evidence 如何串起来。

## 为什么选择这些实验

逐个实验解释：它支撑哪个 claim、解决哪个 reviewer concern、放在论文哪个叙事位置、预期结果如何帮助读者理解核心思想。

## 为什么选择这些基线

说明 canonical、recent strong、simple、self-ablation、status quo、oracle 等基线各自排除哪个疑虑。

## 为什么选择这些指标和工作负载

解释指标和 workload 如何服务论文论点，不要只解释字段含义。

## 结果展示策略

说明哪些结果适合主文，哪些适合补充材料；只做战略层面的图表/表格/案例意图，不设计最终图。

## 仍需继承的开放变量

只列真正影响实验规模、claim 覆盖、伦理/数据访问、baseline 公平性或 story placement 的未知项，并说明为什么当前信息不足以决定。
```

The explanation is for user confirmation, not for downstream execution. It
should let the user identify whether a questionable experiment comes from the
core thesis, target-venue prior, live-research pattern, or an inference step.
It should not describe the Markdown template, generation process, or section
mechanics.

## Revision Behavior

When revising an existing experiment plan, revise from concrete artifact content
and concrete feedback. Classify feedback as substantive, file-contract,
over-defensive/open-question, generic/template-driven, language/filename,
evidence-linkage, or non-controlling.

- Substantive feedback may change experiments, baselines, workloads, metrics,
  story placement, or claim boundaries.
- File-contract and language feedback should change filenames, language split,
  section boundaries, or lint compliance without inventing new experiment
  content.
- Over-defensive/open-question feedback should reduce unnecessary open variables
  and turn inferable choices into committed plan decisions with Chinese
  rationale.
- Generic/template-driven feedback should replace checklist-like sections with
  paper-specific experiment objectives, claim verbs, reader doubts, expected
  result patterns, and downstream handoffs.
- Evidence-linkage feedback should strengthen the claim-to-evidence map,
  objective fields, reader takeaways, and explanation logic.
- Feedback that provides no artifact-content defect should not trigger changes
  to experiment objectives, baselines, workloads, metrics, or output schema.
- Non-inspective evaluator feedback that only says artifacts were not examined
  or asks for artifact availability is outside this skill's academic-planning
  scope. Unless it cites a content-specific defect, preserve the academic design
  and output contract.

Make the smallest change that addresses the feedback while preserving the
two-file contract.

## Quality Checks

Before finalizing, check:

- Exactly two Markdown files are produced: `experiment_plan.md` and
  `experiment_plan.explain.md`.
- `experiment_plan.md` is English-only and contains only the strategic plan.
- `experiment_plan.explain.md` is Chinese-first and begins with actual planning
  inputs used.
- The main plan defines workload/dataset, metric, and baseline registries once.
- Objectives reference registry IDs rather than redefining baselines or metrics.
- Every baseline has `Burden: minimum | diagnostic | optional_expensive`.
- Every objective has claim support, story placement, reviewer concern,
  presentation intent, expected evidence output, expected result pattern, reader
  takeaway, and priority.
- Motivation/design-insight experiments make the core intuition visible before
  full evaluation when the paper needs them.
- Main-paper versus supplemental presentation intent is strategic, not a final
  figure design.
- Open variables appear only in the explanation and only when they materially
  affect plan quality.
- Facts resolved by user input, blueprint, existing evidence, live research, or
  clear inference are not restated as user questions.
- Every live-research anchor in the explanation has source, date,
  `venue_status`, and the planning decision it changed.
- Deepresearch-derived venue and paper patterns are converted into design
  choices, not generic citations or literature-review summaries.
- No section, heading, experiment name, metric rationale, baseline choice, or
  ablation could apply unchanged to an unrelated paper.
- The plan contains no source prose, literature review, user-facing warnings,
  shell commands, code, fabricated results, concrete output paths, logging
  schemas, manifest fields, implementation owners, exact run scripts, or
  runtime environment mechanics.
- The explanation explains design reasoning and paper-story fit, not template
  mechanics or generation process.
- Objectives with overlapping claims, workloads, metrics, comparators, and
  outputs are merged or represented as reporting views.
