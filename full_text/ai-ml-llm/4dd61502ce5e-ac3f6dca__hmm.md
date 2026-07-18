---
name: HMM
description: Multi-mode problem structuring and method orchestration for vague requests, prompt systems, nested state machines, and research workflows. Use when Codex needs not only problem briefs, constraints matrices, branch plans, and evaluation loops, but also advanced system modeling, template chains, variant recomposition, traversal and invention analysis, optimization portfolios, governance and feedback rules, or explicit XML and graph exports.
---

# HMM

## Overview

Use this skill to compress a vague, bloated, or mixed-granularity problem into a stable MVP workflow.

Default output shape:

- `intake-record`
- `problem-brief`
- `constraints-matrix`
- `mode-resolution`
- `branch-plan`
- `evaluation-report`
- `loop-decision`

Prefer this skill when the user is not asking for a final domain solution yet, but first needs the problem itself to become structured, scoped, and executable.

## Execution Profiles

Use one execution-profile keyword to control interaction cadence and proactive expansion without changing the underlying mode system.

Available user-facing keywords:

- `共创深探`
  - interact often
  - probe optional modes aggressively
  - confirm after major phase boundaries and high-signal probe activations
- `共创稳推`
  - interact at milestones rather than every branch
  - keep expansion bounded unless stronger evidence appears
- `自治深探`
  - do not stop for routine confirmation
  - proactively probe optional modes when clear gain is plausible
  - prefer depth before early closure
- `自治稳推`
  - do not stop for routine confirmation
  - stay on the mainline unless explicit need or stronger system signals appear

Internal ids such as `autonomous_deep`, `autonomous_steady`, `co_create`, or `steady_probe` are contract-side labels only.
User-facing prompts should use the Chinese execution-profile keywords above.

Default rule:

- if the user explicitly gives one of these keywords, use it
- if the round is primarily a source-aligned self-review of HMM itself and no keyword is given, default to `自治稳推`
- otherwise default to `自治深探`

## Profile-Driven Mode Probing

Execution profiles do not replace mode names.
They control how aggressively HMM probes optional modes.

Rules:

- deep profiles may start a `probe activation` from one high-signal gain cue when no hard boundary blocks it
- steady profiles should wait for an explicit user request or at least two system-inference cues before activating a non-core mode
- probe activation should begin with the smallest useful artifact slice rather than the whole pipeline
- `evaluation_validation` should decide whether to deepen, keep bounded, or prune that probe
- execution profiles never override authorization boundaries, source authority, or derived runtime blocking rules

## Source Alignment Rule

When the current task is explicitly grounded in the original source files:

- `references/metaPrompt.md`
- `references/agentic-nested-state-machine.opml`

default to the source-aligned method core first.

The maintained `metaPrompt.md` is now a chapter-based source scaffold rather than the old numbered step draft.

That source-aligned core should be read in three layers:

- default core capabilities
  - shared symbol control
  - Six-Box top scaffold
  - semantic clarification
  - true demand / true constraints
  - ANT / EAFC modeling
  - state / constraint / ideal-direction analysis
  - branch planning
  - evaluation and critique
- first-class source layers that may still be conditionally expanded in runtime
  - retrieval and evidence writeback
  - candidate generation
  - implementation shaping
  - pluginization and skill exteriorization
- source-grounded but non-default expansion planes
  - shared-file coordination
  - memory pruning

Do not auto-expand into long-lived runtime operations engineering just because the user mentions orchestration, branching, or governance.

Treat runtime hooks, provider failover, drift monitoring, threshold governance, and external governance source-of-truth as derived extensions. Only activate them when the task explicitly involves real runtime channels, real service hooks, real provider topology, or continuous operations governance.

## Self-Iteration Rule

When the task is to refine this skill itself, or to align this skill back to `references/metaPrompt.md` and `references/agentic-nested-state-machine.opml`:

- treat `SKILL.md` plus `references/` as the current system under analysis
- default to the source-aligned core and keep derived runtime operations blocked unless the user explicitly asks for real runtime behavior
- when the current round is primarily a source-aligned self-review of HMM itself and the user did not pick a profile, prefer `自治稳推`
- prefer repairing contract mismatches, scope drift, and stage-boundary confusion before adding new modes or new artifacts
- use one bounded local `first_search` pass against the current repo and source files before widening scope
- emit the full base artifact chain so the repair is auditable and reusable in the next round
- when the current round is primarily a source-aligned review of the skill itself, `critique-report.json` may be emitted as a standalone review artifact without implying full advanced-mode completion

## Workflow

Follow this order unless the user explicitly asks to skip a stage:

1. `problem_intake`
Collect the raw request, decide whether it is single-step or multi-step, and record only the minimum context needed to proceed.

2. `semantic_clarification`
Rewrite the problem into a lower-ambiguity form. Extract core terms, ambiguities, and open questions.

When the source distinction matters, keep these separate instead of collapsing them too early:

- visible demand versus real demand,
- assumed constraints versus real constraints.

Between `semantic_clarification` and `demand_constraint_modeling`, allow one bounded `first_search` pass:

- gather only enough external or local evidence to reduce ambiguity,
- keep links or source pointers,
- do not turn this into open-ended research.
- if this pass happens, store it as optional `search-notes.json`.

3. `demand_constraint_modeling`
Model the current state, goal state, actors, constraints, resources, and core frictions. Keep the model minimal.

If the goal state is still unstable, do not force a polished target too early. Record:

- anti-goals,
- failure states,
- collapse paths,
- and survival extremes before overcommitting to one idealized goal.

If the task involves automation, delegated action, auto-send, escalation, or any system acting on behalf of a human, explicitly model:

- authorization boundaries,
- data boundaries,
- escalation boundaries.
- system name, system purpose, system structure, working principle, evolution stage, and current runtime environment when the problem is system-oriented.

4. `branch_plan_generation`
Split the work into executable branches only when the branches are independently testable and their dependencies are explicit.

This stage must also produce `mode-resolution.json`. It should not only list active modes, but also expand:

- which execution profile is active,
- which interaction / expansion profile is active,
- which confirmation policy and mode-probe policy apply in the current round,
- which stages each mode attaches to,
- which outputs become required at each stage,
- which outputs were explicitly requested in the current round,
- which optional mode probes are recommended, promoted, or blocked,
- which derived runtime outputs stay blocked in source-alignment rounds,
- what the current scope-alignment status is,
- and which state should be revisited if those stage outputs are missing.

5. `evaluation_validation`
Check completeness, consistency, blocking issues, and whether the current plan is actually ready.

Do not stop at final-output checks. Also verify stage-level mode requirements:

- whether the chosen execution profile was actually followed,
- whether the round was under-expanded or over-expanded for that profile,
- whether any probe activation was justified, excessive, or missing,
- which stage requirements passed,
- which explicitly requested outputs are already satisfied,
- whether scope drift or blocked scope expansions are present,
- which stage outputs are still missing,
- and which state should be revisited by default.

6. `loop_or_finish`
Either finish the round or loop back to the earliest state that can fix the current defect with the lowest repair cost. Record `scope_alignment_decision`, `scope_repair_target`, and `stage_dispatch_target` explicitly whenever the round is source-aligned or has stage-level output gaps.

When execution profiles are active, `loop_or_finish` should also preserve any `profile_adjustment_recommendation` produced by evaluation so the next round can switch from:

- `共创` to `自治`,
- `自治` to `共创`,
- `深探` to `稳推`,
- or `稳推` to `深探`

when the current round clearly under-expanded, over-expanded, or interrupted the user at the wrong cadence.

## Runtime Compression Of `metaPrompt v2`

The maintained `metaPrompt.md` is now a chapter-based source scaffold rather than the old numbered draft.

The current six-state shell remains valid, but it should now be read explicitly as a runtime compression of the maintained source.

Preferred mapping:

1. `problem_intake`
   - pre-entry of chapter `4`
2. `semantic_clarification`
   - the rest of chapter `4`
3. `demand_constraint_modeling`
   - chapter `5`
   - chapter `6`
   - and lightweight chapter `7` awareness when resource notes are needed but no deep expansion is activated
4. `branch_plan_generation`
   - the bridge from chapter `6` into chapter `9`
   - including target selection and candidate-routing setup
5. `evaluation_validation`
   - chapter `10`
   - and the finish-gating side of chapter `11`
6. `loop_or_finish`
   - chapter `12`
   - plus explicit writeback-driven return to earlier states

This means:

- chapter `8` retrieval and evidence writeback
- chapter `9` candidate generation
- chapter `10` evaluation and implementation shaping
- chapter `11` pluginization and self-upgrade

are all first-class source layers, even when they are not represented as separate top-level runtime states.

Do not silently collapse these into “miscellaneous extensions”.

## Default Core Versus Conditional Expansion

Within the runtime shell, keep this distinction explicit:

### Default Core

By default, every normal round should still guarantee:

- task intake and clarification
- `E/A/F/Cond` modeling
- `S0/Sg/IFR/C/TC/PC` analysis
- branch planning
- evaluation and loopback

### First-Class But Conditionally Expanded Layers

The following belong to the maintained source core, but may still be activated conditionally in the shell:

- retrieval and evidence writeback
- deeper resource/system-level work
- candidate generation as a distinct layer
- explicit implementation planning
- pluginization and skill exteriorization

The rule is:

- if the current task is blocked without them, activate them explicitly;
- if the current task does not need them, keep them inactive but still recognized as first-class source layers.

## Capability Boundary Stop Rule

After the repository has already aligned:

- the maintained `metaPrompt v2` source,
- the typed source companions,
- the boundary files,
- the contract shell,
- and the most source-sensitive mode references,

do not keep widening the skill boundary by default.

Treat broad boundary expansion as stopped when all of the following remain true:

1. the maintained source file stays aligned,
2. the six-state shell still explicitly declares itself as a runtime compression,
3. retrieval and pluginization remain recognized as first-class source layers,
4. optional planes do not silently activate into the neutral core,
5. and no real downstream consumer requires a missing distinction.

When those conditions hold, the correct next work is usually:

- consolidation,
- validation,
- commit preparation,
- packaging,
- distribution,
- or concrete task-driven iteration,

not another broad architecture pass.

Reopen broad boundary work only if at least one of these becomes true:

1. a real downstream consumer cannot use the current shell without a missing distinction,
2. a maintained source change invalidates the current compression,
3. retrieval / generation / evaluation / pluginization begin drifting apart again,
4. or runtime/provider/governance behavior is explicitly requested as real operational scope.

Execution profiles may widen probing aggressiveness, but they do not cancel:

- source authority,
- authorization boundaries,
- or derived runtime blocking rules.

## Global Mode Interaction

When more than one extension mode is active in the same round, do not leave their interaction implicit.

`mode-resolution.json` should preferably make these explicit:

- `mode_precedence`
  Which mode's decision boundary wins when two modes touch the same object.
- `cross_mode_handoffs`
  Which artifact becomes upstream input to which later artifact across modes.
- `authority_boundaries`
  Which mode computes, which mode overrides, and which mode only serializes.
- `interaction_notes`
  Short notes for any non-default cross-mode arrangement in the current round.

Prefer these as explicit structured entries rather than free-form prose:

- `mode_precedence`
  Use entries such as `higher_mode`, `lower_mode`, `precedence_basis`, `applies_to`.
- `cross_mode_handoffs`
  Use entries such as `from_mode`, `to_mode`, `via_artifact`, `handoff_purpose`.
- `authority_boundaries`
  Use entries such as `subject`, `computed_by`, `overridden_by`, `serialized_by`, `final_authority`.
- `interaction_notes`
  Use entries such as `related_modes`, `active_when`, `note`.

Typical examples:

- library and weighting mode computes ranking, governance and feedback mode may override it.
- discovery and hypothesis mode defines feedback entry points, governance and feedback mode records actual feedback events.
- portfolio and optimization mode may consume weighting outputs, but it should not silently replace explicit human override policy.
- representation and serialization mode may export an artifact, but it should not invent semantics that upstream modes did not establish.

Reference examples:

- `references/examples-index.md`
- `references/mode-resolution-example.json`
- `references/evaluation-report-example.xml`
- `references/mode-resolution-example-discovery-governance.json`
- `references/evaluation-report-example-discovery-governance.xml`
- `references/mode-resolution-example-advanced-representation.json`
- `references/evaluation-report-example-advanced-representation.xml`
- `references/mode-resolution-example-template-orchestration.json`
- `references/evaluation-report-example-template-orchestration.xml`

## Advanced Mode

If the user wants the maintained `metaPrompt v2` mainline to continue into deeper system modeling beyond the base workflow, enable `advanced mode`.

Use advanced mode when the user explicitly wants:

- resource graphs,
- actor-network graphs,
- function-field and flow modeling,
- SAFC modeling,
- contradiction analysis,
- USIT32-style operator analysis,
- or a structured solution set after deep system modeling.
- Also use it when the user wants multi-screen system analysis or a critique of the method chain itself.

Advanced mode extends the base flow with this artifact chain:

1. `resource-graph.json`
2. `actor-network.json`
3. `function-field-model.json`
4. `flow-analysis.json`
5. `safc-model.json`
6. `contradiction-analysis.json`
7. `solution-set.json`

Advanced mode end-stage review output:

- `critique-report.json` before declaring the advanced round complete

Optional advanced extension:

- `multi-screen-analysis.json`

Read `references/advanced-mode.md` before running this chain.
Read `references/screen-and-critique-mode.md` when the user wants resource-scan depth, multi-screen analysis, or a post-solution critique of the method itself.

## Template Mode

If the user wants to turn the current method into reusable prompts, a template chain, or batch exploration scaffolding, enable `template mode`.

Use template mode when the user explicitly wants:

- a reusable prompt template,
- a template chain,
- explicit variable mapping,
- batch exploration from one method,
- pruning notes for rejected paths.

Template mode extends the current work with:

- `template-chain.json`
- `pruning-notes.json`
- `checklist-migration-pointer.json` when preserved legacy template consumers need an explicit shared-file pointer to discover `checklist-migration-map.json`
- `checklist-migration-pointer-registry.json` when multiple preserved legacy template consumers should share one discovery entry instead of each depending on a separate implicit pointer path

When a template chain already has a lighter restart layer, `template-chain.json` may also expose optional `fast_entry_points` that reference compressed continuation artifacts such as `checklist-summary.json`, `prompt-guidance.json`, or `graph-format-selection.json`.

When that compressed continuation is already itemized as a todo list, each fast entry point may also expose optional `checklist_item_routes` so the checklist can point to template subsets instead of only the whole chain.

When a pointer registry grows beyond one preserved consumer, it may also expose optional grouping metadata such as `grouping_strategy` and `consumer_groups` so discovery remains explicit without forcing consumers to scan one flat undifferentiated list.

When preserved consumers start diverging by both history and type, the grouped registry may also expose optional `group_dimensions` plus entry-level `consumer_generation` and `consumer_class` metadata so grouping can stay additive instead of forcing a schema break.

When more than one grouped entry exists, prefer layered matching by declared dimension priority first, and only use cross-product matching as a fallback when layered matching still leaves ambiguity.

When the fallback path itself needs to be audited, the grouped registry may also expose optional `matching_examples` so concrete query cases, fallback triggers, and final outcomes become machine-readable instead of staying only in prose.

When the same observable hint repeatedly decides successful fallback resolution, prefer promoting it into explicit `fallback_match_fields` inside `matching_strategy` instead of leaving it implicit inside examples.

Interpret `fallback_match_fields` from left to right by priority. Do not append a new field unless current examples show it actually disambiguates a real preserved-consumer case.

Read `references/template-mode.md` before building these artifacts.

## Library And Weighting Mode

If the user wants the method to become reusable as libraries, guidance sets, or weighted decision structures, enable `library and weighting mode`.

Use it when the user explicitly wants:

- a glossary,
- a parameter library,
- an effect library,
- a temporary working library,
- reusable user-guidance prompts,
- graph-format selection rules,
- or weighted branch/solution ranking.

This mode extends the current work with:

- `glossary.json`
- `parameter-library.json`
- `effect-library.json`
- `temporary-library.json`
- `prompt-guidance.json`
- `graph-format-selection.json`
- `checklist-summary.json`
- `checklist-migration-map.json`
- `decision-weighting.json`

Boundary to governance:

- `decision-weighting.json` computes or records ranking logic, criteria, and fallback weighting when human weights are absent,
- `override-policy.json` decides what happens when human instructions override that ranking,
- and when both are active, the weighting artifact should be treated as upstream input rather than the final authority.

Boundary to candidate listing:

- `decision-weighting.json` owns ranking semantics,
- `variant-set.json` owns the comparable candidate list when explicit variants exist,
- and ranking should bind to stable branch or variant ids rather than display order, list position, or example numbering.

When `checklist-summary.json` is expected to be consumed by downstream template routing, its `items` may also be structured entries with stable `item_id` values instead of plain strings only.

When older checklist artifacts must be preserved for history while newer consumers expect stable `item_id` values, emit `checklist-migration-map.json` instead of rewriting old rounds in place.

Read `references/library-and-weighting-mode.md` before building these artifacts.
If explicit human weights or priority overrides exist, prefer them over derived weighting. Use `decision-weighting.json` only as a fallback when no human weight input is available.

When multiple observed fallback-success signals compete for `fallback_match_fields`, reuse `decision-weighting.json` to rank them before changing the registry. If no new positively validated candidate appears, keep the current fallback field set unchanged.
When a fallback-field ranking becomes stable enough, compress it into `prompt-guidance.json` or a short `checklist-summary.json` so later rounds can reuse the decision boundary without rereading the full weighting artifact.
When that checklist is meant for repeated machine consumption across later maintenance rounds, prefer structured `items` with stable `item_id` values instead of plain strings.

## Orchestration And Memory Mode

If the user wants branch strategy, asynchronous coordination, execution supervision, or explicit memory pruning rules, enable `orchestration and memory mode`.

Use it when the user explicitly wants:

- branch type design,
- parallel versus serial planning,
- suspended-path management,
- execution supervision,
- shared-context coordination,
- or memory pruning records.

This mode extends the current work with:

Source-aligned orchestration core:

- `orchestration-plan.json`
- `shared-context-map.json` when shared-file coordination structure must be made explicit before execution supervision
- `execution-supervision.json`
- `executor-interface.json`
- `executor-capability-registry.json`
- `memory-pruning.json`
- `writeback-ledger.json` when the flow includes shared-file writebacks, environment observation, checkpoint writebacks, or merge tracking

Derived runtime operations extension, only when the task explicitly involves runtime/service/provider/governance operations:

- `executor-capability-version-policy.json`
- `executor-capability-discovery.json` when capability/availability discovery is in scope
- `executor-runtime-hook.json` when discovery depends on runtime signals or external probe hooks
- `runtime-event-source-contract.json` when runtime hook depends on an event source contract
- `runtime-event-source-registry.json` and `runtime-event-schema-version-policy.json` when event source registration or schema evolution is in scope
- `runtime-event-source-service-hook.json` and `runtime-schema-registry-hook.json` when the event source or schema registry is exposed as a real service
- `capability-update-ledger.json` when discovery results change the registry or fallback routes
- `capability-migration-ledger.json` when registry versioning or compatibility changes are in scope
- `consumer-compatibility-probe.json` when compatibility is decided from observed consumer requests or runtime probe evidence
- `consumer-registry.json` and `consumer-runtime-discovery.json` when compatibility depends on runtime consumer identity or a consumer source-of-truth
- `consumer-registry-version-policy.json` and `consumer-registry-migration-ledger.json` when consumer source-of-truth versioning or migration is in scope
- `runtime-event-schema-migration-ledger.json` when runtime event schema migration is in scope
- `consumer-registry-service-hook.json` when the consumer source-of-truth is exposed as a real service
- `source-of-truth-drift-report.json` and `source-of-truth-reconciliation-ledger.json` when service/source registry/runtime observations may drift
- `source-of-truth-drift-monitor.json`, `drift-monitor-scheduler.json`, `auto-reconcile-policy.json`, `alert-routing-policy.json`, `human-escalation-workflow.json`, and `drift-scan-ledger.json` when drift should be monitored continuously rather than checked once
- `drift-scheduler-service-hook.json`, `alert-delivery-contract.json`, and `human-escalation-channel.json` when continuous drift monitoring needs to connect to real runtime channels
- `delivery-provider-capability-matrix.json`, `channel-failover-policy.json`, and `delivery-failover-ledger.json` when those runtime channels need provider failover or multi-channel routing fallback
- `provider-health-check.json`, `circuit-breaker-policy.json`, and `provider-recovery-switch-ledger.json` when provider health state and recovery switching are in scope
- `provider-health-telemetry.json`, `circuit-breaker-hysteresis-policy.json`, and `recovery-canary-policy.json` when recovery switching needs telemetry, hysteresis, or canary control
- `provider-telemetry-stream-contract.json`, `anomaly-scoring-policy.json`, `adaptive-threshold-policy.json`, and `threshold-adaptation-ledger.json` when stabilization depends on telemetry streams, anomaly scores, or adaptive thresholds
- `telemetry-baseline-evolution.json`, `anomaly-model-recalibration.json`, `threshold-governance-workflow.json`, and `threshold-governance-ledger.json` when adaptive stabilization needs long-term baseline evolution, model recalibration, or human governance
- `baseline-governance-service-hook.json`, `anomaly-model-registry.json`, `threshold-policy-registry.json`, and `governance-sync-ledger.json` when long-term threshold governance needs to connect to external governance systems
- `governance-source-drift-report.json`, `governance-source-reconciliation-ledger.json`, and `governance-approval-channel.json` when those external governance systems may drift or need approval-channel integration
- `governance-review-scheduler.json`, `governance-alert-routing-policy.json`, `governance-review-cadence.json`, and `governance-review-ops-ledger.json` when governance drift should be handled as a continuous operations workflow
- `governance-provider-capability-matrix.json`, `governance-channel-failover-policy.json`, and `governance-delivery-failover-ledger.json` when governance operations need provider failover or multi-channel routing fallback

When this mode is active, do not just say “parallel” or “serial” in prose. Classify each path explicitly as one of:

- `parallel_worker`
- `parallel_branch`
- `suspended_traversal`
- `parallel_fork`
- `serial_branch`

Also make the shared-context and supervision boundaries explicit:

- who can read what,
- who can write what,
- what counts as shared fact,
- what remains local hypothesis,
- and when a suspended or pruned path may be restored.

Prefer structural execution language over agent-identity language:

- `execution_units` for executable identities,
- `worker_scopes` for bounded responsibility,
- and `reference_context_refs` for upstream context bindings.

Prefer structural memory language over tool language:

- `memory-pruning.json` for pruning and reactivation policy,
- `memory_edit_events` for actual replacement writebacks,
- and `replacement_summaries` for what future rounds should retain.

When the orchestration design is execution-oriented, also make these explicit:

- whether workers coordinate by shared files or environment observation,
- whether direct worker-to-worker messaging is disallowed,
- whether upstream context is treated as `reference_context`,
- what visibility class and permission class each worker belongs to,
- and how upstream todo items are distributed to workers.
- Emit `executor-interface.json` so these rules become executable packets instead of prose.

If the flow is moving toward a real executor, extend `executor-interface.json` with:

- executor kind per unit,
- input/output artifact contract per unit,
- failure and resume signals,
- and checkpoint hook bindings.

If executor kinds are heterogeneous, also emit `executor-capability-registry.json` so the skill can decide:

- which executor kind can actually run which unit,
- which capabilities are missing,
- and what fallback or escalation route should be used.

If executor availability or capability can change over time, also emit:

- `executor-capability-discovery.json`
- `capability-update-ledger.json`
- `executor-runtime-hook.json` when runtime signals are part of discovery

If capability registry versions can evolve, also emit:

- `executor-capability-version-policy.json`
- `capability-migration-ledger.json` when a version bump, deprecation, or compatibility break happens
- `consumer-compatibility-probe.json` when compatibility needs to be measured against runtime consumer requests

Read `references/orchestration-and-memory-mode.md` before building these artifacts.

## Variant And Composition Mode

If the user wants multiple comparable variants, step normalization, or recomposition of steps across alternatives, enable `variant and composition mode`.

Use it when the user explicitly wants:

- multiple ranked variants,
- normalized shared steps,
- explicit `step_id` and dependency repair,
- or a new merged variant composed from parts of several alternatives.

When the target direction must stay fixed but the path, order, or local tactic may change under different constraints, treat that as a first-class `variant and composition mode` use case.

This mode extends the current work with:

- `variant-set.json`
- `step-normalization.json`
- `composition-plan.json`

Keep this boundary explicit:

- `variant-set.json` records the candidate set and default pointer,
- `decision-weighting.json` records ranking semantics when explicit sorting is needed,
- and `default_variant` should be justified by ranking or override basis rather than by presentation order.

Read `references/variant-and-composition-mode.md` before building these artifacts.

## Traversal And Invention Mode

If the user wants systematic divergence, heuristic filters, or invention-measure exploration, enable `traversal and invention mode`.

Use it when the user explicitly wants:

- relation / parameter / granularity traversal,
- spacetime or causal filtering,
- IFR-style elimination,
- invention measures,
- or measure combinations that create a system-level change.

Default traversal discipline:

- traverse relation dimensions first, then parameter thresholds, then granularity / containment,
- use the source razor and stay on the narrowest dimension that can actually change the dominant harmful interaction,
- anchor dimensions on function and interaction chains rather than product structure or backend inventories,
- black-box a subsystem as a field or capability when the contradiction is about how it acts, not how it is internally produced,
- and require every measure combination to explain why the combination becomes a new mechanism and what system-level change it causes.

This mode extends the current work with:

- `traversal-plan.json`
- `heuristic-filters.json`
- `invention-measures.json`
- `measure-combinations.json`

Read `references/traversal-and-invention-mode.md` before building these artifacts.

## Discovery And Hypothesis Mode

If the user wants latent-demand discovery, early-adopter signals, explicit clarification-mode control, or open-assumption management, enable `discovery and hypothesis mode`.

Use it when the user explicitly wants:

- strict versus open clarification,
- repeated confirmation loops,
- latent-demand discovery,
- demand-visibility shaping,
- field-created demands,
- cognitive-economy factors,
- blocked demand expression,
- early adopter or extreme-user signals,
- soft pruning,
- low-confidence pruning,
- or real-world feedback hooks.

Boundary to the base chain:

- `semantic_clarification` may record lightweight `visible_demand` and `real_demand_hypothesis`,
- but this mode should own latent demand discovery, field-created demand, cognitive-economy framing, visibility barriers, early-adopter signals, and explicit open-assumption governance,
- and `feedback-hooks.json` should define entry points and triggers, not replace the later `feedback-ledger.json` of governance mode.

This mode extends the current work with:

- `demand-visibility.json`
- `hypothesis-register.json`
- `feedback-hooks.json`

Read `references/discovery-and-hypothesis-mode.md` before building these artifacts.

When these artifacts are present, prefer making the discovery boundary explicit:

- `demand-visibility.json` should show what moved beyond the base-chain lightweight demand split.
- `hypothesis-register.json` should keep assumptions reversible by default and make pruning or suspension explicit.
- `feedback-hooks.json` should define where external evidence can re-enter the workflow and what later ledger should receive it.

## Portfolio And Optimization Mode

If the user wants multi-method branching, approximate-optimal comparison, state-space matrices, or a layered research-versus-execution roadmap, enable `portfolio and optimization mode`.

Use it when the user explicitly wants:

- near-optimal multi-path comparison,
- methodology branches,
- state-space matrices,
- research plans separated from execution plans,
- or a portfolio of methods rather than one method.

Default portfolio discipline:

- do not force a single winner too early when the source problem is genuinely multi-objective,
- preserve a near-optimal set or non-dominated set before compressing to one recommended route,
- treat method family, changed constraints, and changed weights as explicit branch variables,
- separate research plans from execution roadmaps instead of blending unknowns and commitments into one list,
- and if human weights are absent, allow a lightweight pairwise or AHP-style fallback weighting with an explicit consistency check.

This mode extends the current work with:

- `state-space-matrix.json`
- `methodology-portfolio.json`
- `method-branch-map.json`
- `research-plan.json`
- `execution-roadmap.json`
- `optimization-report.json`

Read `references/portfolio-and-optimization-mode.md` before building these artifacts.

## Governance And Feedback Mode

If the user wants human-in-the-loop controls, interaction policy, override priority, or a real-world feedback ledger, enable `governance and feedback mode`.

Use it when the user explicitly wants:

- guided question styles,
- explicit human review points,
- override rules for weights or plans,
- or a ledger of real-world feedback and applied corrections.

Default governance discipline:

- prefer bounded choice-style or heuristic prompts over open-ended questioning,
- keep human-visible and human-modifiable surfaces explicit instead of assuming model outputs are final,
- let human-provided weights and overrides outrank automatic ranking,
- use automatic weighting only as a fallback when human weight input is absent,
- and treat real-world feedback as a writeback channel for correction rather than as a decorative appendix.

This mode extends the current work with:

- `interaction-policy.json`
- `governance-checkpoints.json`
- `override-policy.json`
- `feedback-ledger.json`

Read `references/governance-and-feedback-mode.md` before building these artifacts.
When governance and weighting are both in scope, human-specified weights and overrides take precedence over automatic ranking.

When these artifacts are present, prefer making governance boundaries explicit:

- `interaction-policy.json` should show which question styles are preferred, avoided, and when they trigger.
- `governance-checkpoints.json` should show where humans must review, what they may edit, and what remains non-overridable.
- `override-policy.json` should say how human overrides beat default ranking and what fallback weight method is allowed when humans stay silent.
- `feedback-ledger.json` should distinguish observed real-world feedback, applied corrections, and still-pending checks.

## Representation And Serialization Mode

If the user wants XML, Mermaid, DAG, triple, or logic-oriented exports as first-class outputs, enable `representation and serialization mode`.

Use it when the user explicitly wants:

- XML-wrapped rewritten prompts,
- Mermaid sequence diagrams,
- explicit DAG export,
- explicit triple export,
- or logic-oriented serialized outputs.

Default representation discipline:

- do not export into a representation layer before the underlying semantics are stable enough,
- choose formats by downstream use rather than exporting every format by default,
- use XML for structured wrapping, Mermaid for order or interaction, DAG for dependency structure, triples for compressed relations, and logic notation for necessary or sufficient conditions,
- keep the representation layer aligned with the current source artifact instead of inventing new semantics in the export step,
- and record chosen formats and export targets explicitly so downstream consumers do not need to infer them.

This mode extends the current work with:

- `xml-rewrite.xml`
- `sequence-diagram.mmd`
- `representation-bundle.json`

Read `references/representation-and-serialization-mode.md` before building these artifacts.

## Default Rules

- Keep the workflow on a single main line. Do not expand worker execution into the state machine in MVP.
- Do not reintroduce UI, client interaction design, or multi-agent memory governance into the main skill flow unless the user explicitly asks to widen scope.
- When asking the user for clarification, prefer bounded choice-style or heuristic prompts over open-ended questioning.
- Branch only when the candidate branches have no hidden control dependency and each branch has its own `validation_target`.
- Prefer fixing the earliest broken upstream state over patching downstream artifacts.
- In one round, prefer at most 3 meaningful steps of advancement.
- Do not finish if blocking issues are still open.
- Treat `first_search` as a bounded helper step, not a new main state.
- When discovery mode is active, prefer soft pruning or reversible suspension before irreversible deletion.
- If the goal is still too vague to model directly, switch to `anti-goals` first: define what failure, collapse, or unacceptable outcomes look like, then prune paths that lead there.
- When the task is source alignment against `references/metaPrompt.md` or `references/agentic-nested-state-machine.opml`, do not auto-activate derived runtime/provider/governance operations artifacts. Keep them blocked unless the user explicitly asks for real runtime operations behavior.

## Minimal Problem Frame

When structuring the problem, think with the smallest useful subset of the original state-space frame:

- `S0`: current state
- `Sg`: goal state
- `O`: operators, actions, resources, or forces that can move the system
- `C`: constraints and path boundaries
- `T`: transition logic or causal consequences
- `M`: domain method or imported method family

Do not force every output artifact to expose all six fields, but keep them in mind when a problem remains underdefined.

Use this frame especially when:

- the user mixes present facts with desired outcomes,
- the solution language is ahead of the problem definition,
- or multiple methods are being blended without clear boundaries.

## Core Lens From Source

Do not reduce the original source to a generic workflow only.

The source material has a deeper method core:

- `true demand / true constraints`
- `problem formation chain`
- `E / A / F / C` analysis
- actor-network roles
- anti-goals when `Sg` is still unstable
- evaluation through necessary / sufficient / pivot roles

Read `references/core-method.md` when the user is working from the original source materials or when the task starts looking like a mixed prompt-method-state-machine system rather than a normal planning task.

At minimum, the skill should explicitly ask:

- what is the real demand versus the visible demand,
- what is the real constraint versus the assumed constraint,
- who is paying, deciding, using, bearing externalities, and evaluating,
- which harmful interaction is currently dominant,
- which hidden condition makes that interaction persist,
- and what compensating cost appears if the usual fix path is used.

## Thinking Modes

The original source has a real dual-mode pattern that should not be lost:

- `Dissipation mode`
  Keep assumptions open, allow temporary inconsistency, and explore alternative framings.
- `Crystallization mode`
  Reduce ambiguity, freeze key assumptions, harden outputs, and remove weak paths.

In practice:

- use dissipation mode before the problem is structurally clear,
- use crystallization mode before branching, evaluation, and finish decisions.

Do not crystallize too early.

## Language Policy

Always use neutral analysis language.

- Describe incentives, constraints, risks, side effects, and externalities.
- Do not default to manipulative or extraction-first wording.
- If the source material uses strong or adversarial wording, label it as source phrasing and then rewrite it neutrally.
- Keep theory symbols if useful, but explain them neutrally.

Read `references/terminology-policy.md` before generating user-facing analysis.

## References

Load references progressively, not all at once.

- Read `references/scope-boundary.md` when deciding what belongs in the skill and what must stay out.
- Read `references/node-taxonomy.md` when a node mixes state, rule, artifact, UI, theory, or example roles.
- Read `references/state-contracts.yaml` when producing or checking state outputs.
- Read `references/state-machine.yaml` when deciding transitions, loopbacks, pruning, or finish conditions.
- Read `references/examples-index.md` when more than one extension mode is active, or when you need a concrete cross-mode example before writing `mode-resolution.json` or `evaluation-report.xml`.
- Read `references/opml-functional-architecture-review.md` when the task is to critique or optimize the abstract functional design of the original OPML rather than only refining the skill contracts.
- Read `references/examples-index.json` when example selection itself should be machine-readable rather than only human-readable.
- Read `references/opml-promotion-status-model.md` when the task is to decide whether a source-derived idea should stay an example, become a rule, become a contract, or remain a reference.
- Read `references/opml-promotion-status-model.json` when the promotion model itself should be machine-readable.
- Read `references/source-node-promotion-catalog.json` when you need concrete current promotion-status mappings for high-value OPML nodes.
- Read `references/opml-promotion-backlog.json` when the task is to prioritize which candidate source nodes should be split, renamed, archived, or promoted next.
- Read `references/opml-architecture-optimization-roadmap.md` when the task has moved beyond local promotion fixes and into maintenance-mode abstract architecture alignment of the original OPML.
- Read `references/opml-architecture-optimization-roadmap.json` when that maintenance-mode architecture map should itself be machine-readable.
- Read `references/legacy-artifact-compatibility-policy.md` when the task is to decide whether a historical source artifact should stay active, become compatibility-only, or become archived.
- Read `references/legacy-artifact-compatibility-policy.json` when that archive/compatibility decision should be machine-readable.
- Read `references/branch-topology-decision-table.md` when the task is to normalize topology choice among `parallel_worker`, `parallel_branch`, `serial_branch`, `suspended_traversal`, and `parallel_fork`.
- Read `references/branch-topology-decision-table.json` when that topology decision logic should be machine-readable.
- Read `references/typed-source-node-index.md` when the task should start from a typed companion of the OPML source rather than reconstructing roles directly from the free-form tree.
- Read `references/typed-source-node-index.yaml` when that typed source companion should be machine-readable.
- Read `references/metaPrompt-step-index.md` when the task should start from a typed companion of the maintained chapter-based `metaPrompt.md` scaffold rather than reconstructing chapter order from prose.
- Read `references/metaPrompt-step-index.json` when that maintained source scaffold should be machine-readable.
- Read `references/source-node-type-registry.md` when the task needs the meaning of typed source node roles, scope layers, and source-plane hints.
- Read `references/source-node-type-registry.json` when that role registry should be machine-readable.
- Read `references/product-interaction-boundary.md` when the task is to keep UI/product ideas out of workflow contracts.
- Read `references/ui-pattern-archive.json` when product interaction residue from the OPML should be machine-readable instead of staying only in prose review.
- Read `references/executor-persona-boundary.md` when the task is to keep execution substrate taxonomy out of orchestration contracts.
- Read `references/execution-substrate-taxonomy.json` when execution substrate residue from the OPML should be machine-readable instead of staying only in prose review.
- Read `references/strategy-intervention-boundary.md` when the task is to keep strategy/intervention material out of the neutral default core unless explicitly activated.
- Read `references/optional-strategy-mode.json` when optional strategy/intervention residue from the OPML should be machine-readable instead of staying only in prose review.
- Read `references/boundary-razor-policy.md` when the task is to decide whether an already-defined archive plane should freeze or expand.
- Read `references/boundary-razor-policy.json` when that freeze-versus-expand decision should be machine-readable.
- Read `references/release-consolidation-checklist.md` when the task is about release-ready maintenance, loading priority, or keeping the reference stack consolidated.
- Read `references/release-consolidation-checklist.json` when that maintenance map should be machine-readable.
- Read `references/release-final-review.md` when the task is to check or communicate the current closeout judgment for the maintained reference stack.
- Read `references/release-final-review.json` when that closeout judgment should be machine-readable.

If the maintenance-consolidation gates are already satisfied, do not keep creating new architecture layers by default.
Prefer release review, commit preparation, packaging, or distribution unless a real downstream consumer or source drift explicitly reopens architecture work.
- Treat `references/examples-index.json`, `references/opml-promotion-status-model.json`, `references/source-node-promotion-catalog.json`, and `references/opml-promotion-backlog.json` as lightweight source-review reference contracts rather than per-round required outputs.
- Read `references/terminology-policy.md` when rewriting source material into neutral analysis language.
- Read `references/source-alignment-policy.md` when the task is to align the skill back to the original source, or when you suspect orchestration has drifted into runtime/provider/governance operations beyond the source.
- Read `references/core-method.md` when you need the distilled core ideas from the original two source files without loading all of their raw text.
- Read `references/advanced-mode.md` when the user wants the maintained `metaPrompt v2` mainline to expand into deeper graph / flow / SAFC / contradiction / solution-set modeling.
- Read `references/output-and-evaluation.md` when the user needs template variable mapping, graph formats, triple formats, DAG formats, logic formats, or stronger evaluation methods.
- Read `references/template-mode.md` when the user wants template chains, batch exploration, or pruning notes.
- Read `references/screen-and-critique-mode.md` when the user wants multi-screen analysis, ordered resource scanning, IFR-style resource reconstruction, or critique reports.
- Read `references/library-and-weighting-mode.md` when the user wants libraries, guidance prompts, graph-format choices, or weighted decision outputs.
- Read `references/orchestration-and-memory-mode.md` when the user wants branch strategies, asynchronous coordination, execution supervision, or memory pruning.
- Read `references/variant-and-composition-mode.md` when the user wants multiple variants, step normalization, or merged plans composed from multiple alternatives.
- Read `references/traversal-and-invention-mode.md` when the user wants systematic traversal, heuristic filters, IFR-style elimination, or invention-measure exploration.
- Read `references/discovery-and-hypothesis-mode.md` when the user wants latent-demand discovery, early adopter signals, clarification-mode control, or explicit hypothesis management.
- Read `references/portfolio-and-optimization-mode.md` when the user wants methodology portfolios, state-space matrices, multi-path optimization, or layered research/execution plans.
- Read `references/governance-and-feedback-mode.md` when the user wants human review points, guided question styles, override rules, or real-world feedback tracking.
- Read `references/representation-and-serialization-mode.md` when the user wants explicit XML, Mermaid, DAG, triple, or logic exports.
- Read `references/metaPrompt.md` and `references/agentic-nested-state-machine.opml` only when you need the original source language or source structure.

Read them in particular when you need:

- the maintained chapter-based method scaffold from `references/metaPrompt.md`,
- the larger mother-structure from `references/agentic-nested-state-machine.opml`,
- the original `P = {S0, Sg, O, C, T, M}` style thinking,
- the dissipation/crystallization loop,
- or the source definitions of search, evaluation, and branch orchestration.

## Output Contract

When the user wants files, prefer this artifact set:

- `intake-record.json`
- `search-notes.json` when bounded first-search evidence is needed
- `problem-brief.json`
- `constraints-matrix.json`
- `branch-plan.json`
- `mode-resolution.json`
- `evaluation-report.xml`
- `loop-decision.json`

If advanced mode is active, extend the artifact set with:

- `resource-graph.json`
- `actor-network.json`
- `function-field-model.json`
- `flow-analysis.json`
- `safc-model.json`
- `contradiction-analysis.json`
- `solution-set.json`
- `critique-report.json` before declaring the advanced round complete
- `multi-screen-analysis.json` when the user wants super/current/sub-system evolution analysis

If source-aligned candidate generation and implementation shaping is active, extend the artifact set with:

- `selected-targets.json`
- `operator-calls.json`
- `candidate-pool.json`
- `combination-hints.json`
- `solution-comparison.json`
- `solution-paths.json`
- `validation-plan.json`
- `implementation-steps.json`
- `fallback-rules.json`

When these artifacts are present, prefer making the generation and evaluation boundary explicit:

- `selected-targets.json` should say which targets were chosen for generation and which were deferred.
- `operator-calls.json` should show which operator families were applied to which targets instead of hiding generation provenance.
- `candidate-pool.json` should keep each candidate's expected gain, new cost, and evidence-needed fields explicit.
- `combination-hints.json` should stay advisory until evaluation promotes a path.
- `solution-comparison.json` should compare expected gain, new cost, risk, validation need, and constraint fit before a route is treated as ready.
- `solution-paths.json` should separate main and fallback paths.
- `validation-plan.json`, `implementation-steps.json`, and `fallback-rules.json` should carry the evaluation result forward into executable next-step logic.

If template mode is active, extend the artifact set with:

- `template-chain.json`
- `pruning-notes.json`

If library and weighting mode is active, extend the artifact set with:

- `glossary.json`
- `parameter-library.json`
- `effect-library.json`
- `temporary-library.json`
- `prompt-guidance.json`
- `graph-format-selection.json`
- `checklist-summary.json`
- `decision-weighting.json`

If orchestration and memory mode is active, extend the artifact set with:

- `orchestration-plan.json`
- `execution-supervision.json`
- `executor-interface.json`
- `executor-capability-registry.json`
- `memory-pruning.json`
- `writeback-ledger.json` when execution-side writebacks or merge tracking are in scope

If variant and composition mode is active, extend the artifact set with:

- `variant-set.json`
- `step-normalization.json`
- `composition-plan.json`

If traversal and invention mode is active, extend the artifact set with:

- `traversal-plan.json`
- `heuristic-filters.json`
- `invention-measures.json`
- `measure-combinations.json`

When these artifacts are present, prefer making the narrowing logic explicit:

- `traversal-plan.json` should expose the active focus, deferred dimensions, and any scope guard that keeps the traversal bounded.
- `heuristic-filters.json` should distinguish direct operators from background states and should record what was pruned or black-boxed.
- `invention-measures.json` should separate single, paired, and complex measures instead of flattening them into one undifferentiated list.
- `measure-combinations.json` should explain the new mechanism, not just the component list.

If discovery and hypothesis mode is active, extend the artifact set with:

- `demand-visibility.json`
- `hypothesis-register.json`
- `feedback-hooks.json`

If portfolio and optimization mode is active, extend the artifact set with:

- `state-space-matrix.json`
- `methodology-portfolio.json`
- `method-branch-map.json`
- `research-plan.json`
- `execution-roadmap.json`
- `optimization-report.json`

When these artifacts are present, prefer making the portfolio logic explicit:

- `state-space-matrix.json` should say what decomposition basis produced the matrices and how priority is being viewed.
- `methodology-portfolio.json` should show method families, target objectives, and tradeoff styles instead of only naming candidate methods.
- `method-branch-map.json` should expose which constraints or weights changed per branch.
- `research-plan.json` should answer what still needs to be learned before commitment.
- `execution-roadmap.json` should answer what to do first, next, and in parallel once the uncertainty boundary is acceptable.
- `optimization-report.json` should explain why the result is approximate-best and why a single-best collapse would be misleading if that is the case.

If governance and feedback mode is active, extend the artifact set with:

- `interaction-policy.json`
- `governance-checkpoints.json`
- `override-policy.json`
- `feedback-ledger.json`

If representation and serialization mode is active, extend the artifact set with:

- `xml-rewrite.xml`
- `sequence-diagram.mmd`
- `representation-bundle.json`

When these artifacts are present, prefer making the export logic explicit:

- `xml-rewrite.xml` should identify which rewritten object is being wrapped and what XML target it serves.
- `sequence-diagram.mmd` should be tied to a real interaction or execution order rather than generated decoratively.
- `representation-bundle.json` should say which formats were selected, what each target points to, and why some other formats were not emitted.

If source-aligned pluginization and self-upgrade is active, extend the artifact set with:

- `plugin-decisions.json`
- `plugin-drafts.json`
- `plugin-interfaces.json`
- `plugin-feedbacks.json`
- `plugin-upgrade-rules.json`

When these artifacts are present, prefer making the plugin boundary explicit:

- `plugin-decisions.json` should say what is being promoted, what stays deferred, and why.
- `plugin-drafts.json` should preserve reusable domain structure, evidence sources, operator mappings, and failure modes without pretending to be an executable MCP skill.
- `plugin-interfaces.json` should expose future skill shells only after the plugin draft is stable enough to externalize.
- `plugin-feedbacks.json` should keep vocabulary, analysis, solution, and failure writebacks separate so later rounds can reuse them intentionally.
- `plugin-upgrade-rules.json` should make `P0 -> P1 -> P2` promotion explicit instead of silently upgrading maturity.

If the user only wants discussion, still think in this artifact shape internally and summarize from it.

If the problem is still unstable after `problem-brief`, explicitly summarize:

- what is known in `S0`,
- what is still uncertain about `Sg`,
- which `O` are only hypotheses,
- which `C` are hard constraints versus temporary assumptions.

In `constraints-matrix.json`, prefer to make these source-derived structures explicit:

- actor-network roles,
- actor thresholds,
- harmful functions,
- hidden conditions,
- compensating costs,
- system profile,
- objective function,
- survival extremes,
- authorization boundaries when automation is involved.

## Evaluation Lens

Do not score outputs only by whether they sound reasonable.

At evaluation time, explicitly test whether the current path is acting as:

- a `necessary condition`,
- a `sufficient condition`,
- or a `pivot variable` inside a larger combination.

If the user asks for depth, explain which of the three roles each key step is playing.

If a self-score is present, treat it only as a weak auxiliary check:

- it may help expose obvious weakness,
- it must include a concrete deduction reason,
- and it must never replace source consistency, cross-format consistency, or fact validation.

If the user asks for stronger verification, also separate:

- same-source consistency,
- cross-format consistency,
- fact-level validation chain,
- and unverifiable assumptions.

If two or more extension modes are active in the same round, also check:

- whether their handoffs are explicit,
- whether their authority boundaries conflict,
- and whether any mode is silently redefining an upstream artifact it should only consume.

## When To Stop

Stop the current round only when:

- the scoped problem is explicit,
- constraints and actors are explicit,
- the branch plan is explicit,
- the evaluation report has no unresolved blocking issue,
- and the loop decision is explicit.

If any one of those is missing, do not pretend the workflow is complete.

Also do not stop when:

- the goal state is still only a slogan,
- the branch plan is just a list without validation targets,
- or the evaluation phase has not distinguished between blockers and non-blocking risks.
