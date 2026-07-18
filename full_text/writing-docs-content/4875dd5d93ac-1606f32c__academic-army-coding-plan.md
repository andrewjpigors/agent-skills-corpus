---
name: academic-army-coding-plan
description: >-
  Create an English coding_plan.md and a Chinese coding_plan.explain.md from a
  paper blueprint and experiment plan. Use when Codex needs to translate paper
  goals, candidate methods, baselines, datasets, metrics, harnesses, tests, and
  result requirements into a detailed logical coding plan for downstream
  implementation, without writing code or deciding physical file layout.
---

# Academic Army Coding Plan

## Purpose

Produce exactly two Markdown files in the requested output directory:

- `coding_plan.md`: English, AI-facing, and only the coding plan.
- `coding_plan.explain.md`: Chinese, human-facing, and only the explanation and decision rationale for the coding plan.

This skill writes planning artifacts only. Code implementation, physical file placement, plotting, paper prose, and final figure/table formatting belong to later skills.

The coding plan is a downstream implementation contract at the logical level. It describes components, interfaces, entrypoint semantics, execution stages, harnesses, tests, and result artifact schemas. It does not prescribe where the downstream coding skill must create files, unless the user-provided inputs already name an existing path that must be cited as a fact.

## Review Feedback Intake

Classify feedback before changing or regenerating artifacts:

- `Artifact-content feedback`: the reviewer quotes file contents or names a concrete defect in `coding_plan.md` or `coding_plan.explain.md`. Convert the defect into stronger generation, readability, validation, or self-audit rules.
- `Artifact-access feedback`: the reviewer could not inspect files because local commands, Node REPL, MCP resources, mounted paths, connectors, local browser or `file://` opens, or sandbox startup failed. Process-spawn errors such as `windows sandbox: spawn setup refresh` are access feedback.

Access feedback changes delivery behavior, not the planning schema. Preserve the plan requirements unless concrete artifact contents show a real content problem. When access feedback occurs, treat handoff mode as sticky for the next artifact generation in the thread: the pasted read-back contents are the primary review artifact, and path-only delivery is incomplete.

When the only feedback is access feedback, do not invent content critiques, redundancy fixes, or prompt changes about plan substance. Tighten delivery, read-back, and self-contained review rules instead. The reviewer can only evaluate language, boundaries, redundancy, harness/test separation, and artifact schemas after the generated files are pasted.

## Artifact Delivery

Write both files to the requested output directory and read them back before responding.

For `workspace/evolve-*` outputs, or whenever artifact-access feedback is active or sticky in the thread, the final response must be directly reviewable without local filesystem access:

1. Start with one concise validation sentence.
2. Add `Review Handoff` immediately after that sentence.
3. Paste the complete read-back contents of both files under exact relative path headings, including the output directory.
4. Put optional status notes only after the handoff.

Use five-backtick fences for full-file handoffs so embedded command fences remain readable:

``````markdown
## workspace/evolve-.../coding_plan.md

```markdown
<full coding_plan.md content>
```
``````

## workspace/evolve-.../coding_plan.explain.md

```markdown
<full coding_plan.explain.md content>
```

````

When files are long, read each file with a complete read method or bounded chunks before composing the handoff. Paste the read-back contents, not a regenerated approximation. If read-back fails after writing, try another local read mechanism. If read-back remains impossible, report the read-back failure clearly and mark delivery blocked rather than presenting unverified contents.

When a reviewer reports repeated sandbox, PowerShell, Node REPL, connector, mounted-path, browser-open, or `file://` failures, keep the final response concise before `Review Handoff`; do not ask the reviewer to retry local access as the main remedy after producing the artifacts.

If the generated artifact is too long for a comfortable final response, still prefer the complete read-back handoff for `workspace/evolve-*` or active access-feedback tasks. If a platform limit prevents pasting both files, paste as much as possible, clearly mark the truncation point, and state that review is blocked until the remaining read-back content can be provided.

## Output Style

Use natural, readable Markdown. Organize both files with clear semantic headings, short paragraphs, bullets, and compact tables when they clarify parallel entities.

Use numbered lists only for real sequence, such as implementation order, experiment stages, priority, or step-by-step entrypoint semantics. Do not use global abstract ID systems such as `C1`, `B2`, `H3`, or `T4`. If an existing repository already uses short registry keys, preserve them only as aliases beside semantic names and use the semantic names for headings and cross-references.

Prefer names that stand alone:

- `Candidate Method Selection Harness`
- `Reference Lifecycle Deadline Harness`
- `Full-System Deadline-Hit QoE Harness`
- `Data Loading Tests`
- `Metric Computation Tests`
- `Result Export Tests`
- `CLI Smoke Tests`
- `Result Export Layer`
- `Method Adapter Layer`

Use positive, task-facing language. State what the coding plan includes, which logical component owns each concern, what each harness evaluates, and how artifacts flow to later skills. Keep runtime, sandbox, tool-call, fallback-path, and local execution troubleshooting details out of both generated artifacts.

### Chinese Explanation Style

`coding_plan.explain.md` must be Chinese-first natural prose. Preserve English method names, repository names, dataset names, benchmark names, metric names, command semantics, and code identifiers when exact spelling matters. Preserve existing paths only when the user input or project context explicitly gave them and the explanation needs that fact.

When explaining a design choice, first summarize the corresponding plan content, then explain why it supports the paper blueprint and experiment plan. Use natural references such as “method替换模块”, “candidate筛选harness”, “result export layer”, and “CLI smoke tests”, not abstract IDs or “见H2”.

## Workflow

### Gather Minimal Local Context

Locate the two required local inputs from explicit user paths, conventional names, or the closest semantic match:

- paper blueprint
- experiment plan

After locating them, read only those two files. Do not inspect old plans, logs, README files, source trees, notebooks, package metadata, previous outputs, or nearby drafts merely because they are nearby.

Read nearby local files only when the blueprint or experiment plan explicitly references them as required implementation context. If a required local dependency is missing, record it as an open coding question. Supply general engineering patterns through DeepResearch, not unrelated local files.

Before drafting, perform an input-hygiene check: the planned artifacts should depend only on the blueprint, experiment plan, user-provided task constraints, and necessary DeepResearch evidence. Remove unrelated local context if it slipped in.

### Run Pre-Planning DeepResearch

Before drafting `coding_plan.md`, run `academic_army_mcp_tools.deepresearch` unless the provided context already contains a fresh lookup artifact covering the current paper domain, method family, experiment style, and repository-design questions.

Use DeepResearch to inspect high-quality related codebases, official benchmark artifacts, evaluation harnesses, experiment frameworks, paper artifacts, configuration systems, and result-logging conventions relevant to the current domain. Let the lookup choose sources; do not hardcode a fixed source list into the skill output.

Prompt shape:

```text
You are supporting a coding-plan generator for a research paper.

Research brief:
[paper goal, system, candidate methods, baselines, datasets, metrics,
experiment-plan requirements, and any explicit local context]

Return concise implementation-planning evidence:

- Highly engineered related repositories or official artifacts and how they structure logical modules, configs, registries, evaluation harnesses, tests, and result exports.
- Canonical implementation shape for the candidate methods and baselines.
- Current benchmark or dataset protocol details that affect loaders, evaluators, metrics, or comparators.
- Harness implications from traditional test harnesses and modern evaluation harnesses: controlled inputs, drivers, fixtures, evaluator separation, metrics, raw result records, smoke/full protocols, frozen variables, and decision rules.
- Raw result fields needed for later tables, figures, and paper claims.
- Source table with title, link, date, version, or commit when visible; role; whether the takeaway is a confirmed source fact or inferred design pattern; and the planning decision it affects.
```

Put planning consequences in `coding_plan.md`. Put lookup topic, sources, dates or versions when visible, takeaways, evidence type, affected design choices, confidence, and remaining uncertainty in `coding_plan.explain.md`.

## Planning Object: Logical Design Over File Layout

Plan logical components, not physical files. The coding plan may name:

- logical modules
- components
- interfaces
- adapter layers
- registries as concepts
- entrypoint semantics
- configuration concepts
- artifact types and schemas
- test capabilities

The coding plan must not invent concrete file paths, directory trees, or filenames for implementation code, configs, scripts, tests, or outputs. Existing input paths explicitly provided by the user may be cited as input facts. The requested output directory and required artifact filenames may be used for delivery.

Describe code organization with phrases such as:

- “Implement a Method Adapter Layer that exposes a common scheduling interface.”
- “Provide a harness runner entrypoint that accepts harness name, method, dataset split, seed, and configuration identifier.”
- “Emit raw lifecycle records with object ID, event type, timestamp, deadline, useful flag, and drop reason.”

Avoid physical-layout statements such as “put this class in `src/...`”, “create `tests/...`”, or “write metrics to `output/...`” unless the user-provided inputs already require those paths.

## Draft `coding_plan.md`

Write `coding_plan.md` as an engineering contract for the downstream coding skill. Include the sections that apply to the project:

- scope and planning assumptions
- inputs read and input-hygiene summary
- execution assumptions and reusable entrypoint semantics
- logical architecture overview
- core domain model and shared interfaces
- semantic logical modules and ownership boundaries
- replaceable candidate method and baseline interfaces
- workload, dataset, trace, and configuration concepts
- metric definitions and executable decision rules
- staged experiment pipeline
- harness structure for paper goals
- testing structure for functional correctness
- method selection and freeze protocol when needed
- run matrix or staged comparison matrix
- raw-first result export contract
- derivation path from raw artifacts to paper tables, figures, and claims
- implementation order for the downstream coding skill
- acceptance criteria
- assumptions and open coding questions

Keep the plan specific enough to implement: define interfaces, inputs, outputs, dependencies, artifact schemas, and entrypoint parameters. Keep file placement and directory layout for the downstream coding skill.

## Draft `coding_plan.explain.md`

Write `coding_plan.explain.md` as a Chinese explanation of the coding plan and its decision rationale. It should be understandable without repeatedly checking `coding_plan.md`.

Explain:

- which user-provided inputs were read and what requirements were extracted
- what DeepResearch found and how it affected the design
- why the logical modules are separated this way
- why candidate methods and baselines use replaceable interfaces
- why the staged experiment flow matches the experiment plan
- why each harness exists and what paper claim, method-selection question, or optimization question it supports
- why testing is separate from harness execution
- why raw-first exports support later plotting, tables, and writing
- why physical file layout is left to the downstream coding skill
- which assumptions remain and what they block
- how a downstream coding skill should use the plan

Recommended shape:

```markdown
# 编码计划说明：<Paper/System Name>

## 已读取输入与需求提取
## 预规划研究（DeepResearch）
## 主要逻辑模块设计
## 方法与基线替换结构
## 实验阶段设计理由
## Harness Structure 设计理由
## Testing Structure 设计理由
## 原始结果导出理由
## 文件布局边界说明
## 假设与不确定性
## 下游 Coding Skill 使用方式
```

This outline is a guide. Add, merge, or rename sections when semantic headings would be clearer.

## Core Domain Model And Shared Interfaces

When the system has interacting loaders, replay, controllers, methods, baselines, evaluators, harnesses, and exporters, include a shared-domain-model section before module details.

For each shared type, specify:

- type name
- owning logical component
- purpose
- key fields
- producers
- consumers
- raw export mapping when applicable

Use shared domain types to keep schemas consistent across loaders, methods, evaluators, harnesses, and export writers.

## Logical Modules

Map the system into logical modules. For each module, specify:

- semantic module name
- responsibility
- inputs
- outputs
- dependencies on other logical modules
- implementation requirements for the downstream coding skill
- relevant interfaces or artifact schemas

Typical module families include:

- data preparation and workload manifest module
- substrate or external-system adapter module
- method interface and candidate method adapter module
- baseline adapter module
- replay or execution environment module
- metric computation module
- harness execution module
- testing support module
- result export layer
- paper-output derivation interface

Use the project’s paper and experiment requirements to choose the actual modules.

## Methods And Baselines As Replaceable Components

Map every candidate method, modified variant, baseline, ablation, and oracle to a replaceable logical boundary.

For each method or baseline, specify:

- semantic method name
- role, such as proposed candidate, candidate route, headline baseline, diagnostic baseline, ablation, support estimator, or oracle
- shared interface it implements
- configuration concepts it needs
- observations it may access
- actions it may select
- raw outputs needed for comparison
- harnesses or experiment stages that use it

When two baselines overlap, explain the behavioral difference and why both are included. Candidate selection harnesses should be able to compare naive methods, modified methods, baseline methods, and oracles under the same input protocol and metrics.

## Metrics And Decision Rules

For every metric used by a harness, method-selection rule, acceptance criterion, or paper-output derivation, define:

- metric name
- definition
- unit
- direction: `higher_is_better` or `lower_is_better`
- computation procedure or formula
- numerator and denominator for ratio metrics
- raw required fields
- upstream metric dependencies when any
- derived outputs
- aggregation rule
- missing-data behavior
- harnesses and paper outputs that use it

Decision rules should be executable. If a threshold is unknown, record a high-blocking open question that states which harness can compute metrics but cannot automatically select or promote a method yet.

## Harness Structure

Create a dedicated `Harness Structure` section. A harness is a controlled experiment execution environment for paper goals, method selection, module optimization, ablation, stress, robustness, scalability, latency, quality, cost, or other metrics named by the blueprint and experiment plan.

Each harness should have a semantic name and a clear research purpose. For each harness, specify:

- purpose and associated paper claim, experiment question, method-selection question, or optimization question
- role, such as development, candidate selection, final validation, diagnostic analysis, regression, or claim calibration
- target logical module or replaceable method area
- allowed modification scope
- stable interfaces and frozen variables
- entrypoint semantics and parameter meanings
- input dataset, workload, trace, split, seed, and configuration protocol
- methods, modified methods, naive methods, baselines, ablations, and oracles compared
- metrics and decision rule
- raw result artifact types and minimum fields
- derived metric artifact types
- comparison procedure
- smoke, pilot, and full modes when useful
- relationship to other harnesses
- failure modes that should be visible in artifacts

Harnesses should support the development loop:

```text
modify logical module -> run harness -> inspect parseable results -> refine module
```

Harness outputs should include the least processed records needed to audit the run: per-example predictions or decisions, raw scores, timing traces, resource usage, intermediate decisions, error cases, method/config identifiers, dataset, split, seed, run ID, timestamp, source metadata, metric values, and raw artifact references.

## Testing Structure

Create a dedicated `Testing Structure` section separate from harnesses. Testing answers whether code behaves according to its interfaces. Harnesses answer whether a method or module change helps paper metrics.

Plan test capabilities by function, using semantic names such as:

- `Data Loading Tests`
- `Configuration Parsing Tests`
- `Method Interface Tests`
- `Metric Computation Tests`
- `Result Export Tests`
- `CLI Smoke Tests`

For each test capability, specify:

- functional behavior under test
- logical module, interface, or entrypoint semantics under test
- fixture, toy input, mock data, or minimum example used
- expected behavior, output schema, or exception
- pass/fail criterion
- temporary artifact, terminal output, test report, or minimal debug-log behavior
- harness dependency protected by the test

Tests should use small fixtures or mock data and keep debug outputs separate from paper experiment results. They should make it clear whether a harness failure comes from a bad method result or broken code behavior.

## Experiment Stages And Entrypoint Semantics

For complex experiments, plan staged execution. Typical stages include:

- data or asset preparation
- workload or task-instance construction
- candidate method run
- module-level optimization run
- full-system evaluation
- ablation run
- robustness or stress run
- metric computation
- method freeze
- paper-output derivation interface

For each stage, describe:

- stage purpose
- entrypoint semantics
- required parameters such as method, dataset, split, seed, configuration identifier, resource budget, and run mode
- input artifact types
- output artifact types
- validation checks

The same stage should be reusable across methods, datasets, splits, seeds, and configurations through parameter semantics or configuration concepts.

## Method Selection And Freeze Protocol

When candidate methods, learned variants, modified variants, or stress-tuned variants exist, include a method-selection and freeze protocol:

- which harnesses may influence method design
- which harness selects the final method
- what information the frozen method manifest records
- which final-validation runs use the frozen method
- how diagnostic or stress-tuned variants are labeled separately
- how final split contamination is prevented

Paper-facing final evaluation should use a frozen method. Development, calibration, and candidate-selection harnesses can inform the method, while final validation results stay separated from unrestricted tuning runs.

## Raw-First Result Export

Plan export artifacts so later analysis, plotting, and writing skills can work without rerunning experiments. Describe artifact types and schemas, not output paths.

Use these classifications:

- `raw_observation`: observed events, identifiers, timestamps, states, labels supplied by data, component outputs, directly measured values, and per-example decisions or predictions
- `metadata`: run manifests, resolved configs, environment details, dependency versions, source commits, command or entrypoint text, and orchestration records
- `metric`: derived scores, rates, deltas, deadline statistics, quality scores, aggregate summaries, statistical summaries, and decision-rule results
- `analysis`: counterfactuals, attributions, simulated alternatives, oracle analyses, and generated analytical records
- `summary`: human-readable reports and validation summaries

For each important artifact type, specify:

- artifact name
- classification
- purpose
- producing stage
- required fields
- granularity
- format tendency, such as JSONL for raw per-event records or JSON/CSV for aggregates
- source raw artifacts for metrics, summaries, and analyses
- downstream consumer, such as plotting, paper writing, or coding validation
- validation checks

Raw observations should be exported before aggregation. Paper-specific plotting and table formatting consume exported artifacts later.

## Paper Result Derivations

Map each required paper table, figure, or claim to exported artifacts:

- paper output name
- claim or evidence role
- raw artifact types
- metric artifact types
- grouping or filtering
- derived quantities
- statistical summary
- expected downstream artifact type
- notes for plotting or writing skills

Keep paper-specific plotting and final table formatting outside the core experiment system.

## Readability And Path Hygiene Pass

Before writing files, revise for readability and logical-design hygiene:

- Use semantic names as primary anchors for methods, modules, harnesses, tests, exports, and stages.
- Replace alias-only or abstract-ID cross-references with natural references.
- Use numbered lists only for real sequence or priority.
- Make `coding_plan.explain.md` understandable without repeatedly checking `coding_plan.md`.
- Confirm the plan describes logical modules and interfaces rather than invented file paths, directory trees, or filenames.
- Preserve only user-provided existing input paths or project facts that must be cited.
- Express boundaries as ownership rules, such as `Code implementation belongs to the downstream coding skill` and `Paper plotting consumes exported artifacts later`.

## Artifact Quality Self-Audit

Before writing files and again after read-back, check:

- `coding_plan.md` contains only the English coding plan.
- `coding_plan.explain.md` is Chinese-first explanation in natural sentences.
- Neither file relies on global abstract IDs such as `C1`, `B2`, `H3`, or `T4`.
- Neither file invents implementation file paths, directory layout, script paths, test file paths, or output paths beyond the requested artifact delivery location and explicitly provided input paths.
- Harnesses are research-facing evaluation loops with explicit goals, controlled inputs, modification scope, entrypoint semantics, metrics, raw artifacts, and comparison logic.
- Testing remains separate from harness structure and focuses on functional correctness of loaders, interfaces, configs, metrics, exports, and entrypoint wiring.
- Candidate methods and baselines map to replaceable logical interfaces.
- Result exports are raw and parseable first; paper-figure/table derivations are downstream analysis artifacts.
- The files are project-specific and avoid repeating skill rules as defensive boilerplate.

## Validation

Before the final response, confirm:

- `coding_plan.md` exists and is English-only coding plan content.
- `coding_plan.explain.md` exists and is Chinese-first explanation content.
- The output directory contains exactly these two files unless the user explicitly requested additional artifacts.
- DeepResearch was run or a fresh lookup artifact was reused.
- The plan includes logical modules, shared interfaces, replaceable methods and baselines, metrics and decision rules, harness structure, testing structure, staged entrypoint semantics, method freeze protocol when needed, raw-first exports, paper-output derivations, implementation order, acceptance criteria, and open coding questions.
- Every harness has a semantic name, paper-goal mapping, modification scope, stable inputs, entrypoint semantics, parseable raw artifact schema, metric rule, and relationship to other harnesses.
- Every test capability has a semantic name, small fixture or mock input, expected behavior, pass/fail criteria, and debug-output behavior separated from paper results.
- Paper outputs can be derived from raw and metric artifacts without rerunning experiments.
- The readability and path hygiene pass succeeds.
- For `workspace/evolve-*` outputs or artifact-access feedback, the final response includes a `Review Handoff` section with both complete read-back files under relative path headings.
- For repeated artifact-access feedback, the handoff is self-contained enough for a reviewer to evaluate language, content boundaries, path hygiene, harness/testing separation, result artifact schema quality, redundancy, and defensive wording without opening local files.

## Final Response

After writing and validating the files, summarize:

- paths written
- major plan components
- high-blocking open questions
- validation performed, including read-back result

For `workspace/evolve-*` outputs or when artifact-access feedback requests pasted contents, add a `Review Handoff` heading immediately after the concise validation sentence and paste the complete read-back contents of both files using the five-backtick handoff format. A path-only response is incomplete for access-limited review.
````
