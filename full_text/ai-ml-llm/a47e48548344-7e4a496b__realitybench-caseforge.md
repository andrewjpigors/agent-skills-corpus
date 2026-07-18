---
name: realitybench-caseforge
description: Generates source-grounded, format-fit, first-shot-ready benchmark test cases, including LLM-specific cases that approximate non-synthesized real-world testing and produce globally differentiated, objectively scoreable evaluation suites with explicit handling for LLM stochasticity, prompt sensitivity, context limits, tool use, safety boundaries, and judge reliability.
version: v1.0.0
last_updated: 2026-06-17
---

# RealityBench CaseForge

## Skill Identity

**Name:** `realitybench-caseforge`  
**Display name:** RealityBench CaseForge  
**Description:** Generates source-grounded, format-fit, first-shot-ready benchmark test cases, including LLM-specific cases that approximate non-synthesized real-world testing and produce globally differentiated, objectively scoreable evaluation suites with explicit handling for LLM stochasticity, prompt sensitivity, context limits, tool use, safety boundaries, and judge reliability.

The name emphasizes two non-negotiable outcomes: benchmark cases must preserve real-world reality, and they must be forged into the exact contract needed by the evaluator before the first real test run.

## Purpose

Generate benchmark test cases that are close enough to non-synthesized real-world testing to support valid decisions, while also fitting the evaluator that will parse, load, run, and score them on the first permitted attempt.

Use this skill for prompts, agents, models, APIs, software, user interfaces, data pipelines, retrieval systems, document workflows, compliance operations, support workflows, business processes, integrations, and other systems that can be evaluated by cases.

A case is valid only when it is all of the following:

```text
realistic + source-grounded + format-valid + globally differentiable + first-shot-ready + objectively scoreable + decision-relevant
```

A case that is realistic but cannot be parsed, loaded, executed, scored, or safely used in the target benchmark is invalid. A case that fits the format but does not preserve realistic task structure is also invalid.

## Core Objective

The goal is not to produce synthetic examples that resemble benchmarks. The goal is to preserve the causal structure of real work:

```text
actor intent + operating context + artifact state + constraints + realistic noise + risk consequence + required evidence + objective oracle + runner contract + decision use
```

A case must force the system to perform the real capability under realistic conditions. Reject cases solvable by labels, keywords, benchmark phrasing, hidden answer leakage, generic behavior, or shortcut heuristics.

## Operating Sequence

Always follow this order:

```text
1. define benchmark claim and decision use
2. identify target population and representation debt
3. discover evaluator format, runner contract, and scoring contract
4. build source ledger and admissibility map
5. model task anatomy and causal skeleton
6. choose source-grounded case construction method
7. generate or transform case within mutation budget
8. seal oracle and remove answer leakage
9. validate format without consuming the real attempt
10. check realism, anti-synthetic risk, and evidence inversion
11. check global variety, pairwise distance, and coverage debt
12. validate oracle, score fit, and diagnostic capture
13. compute validity scores
14. package ready-to-test case bundle
```

Do not generate a full benchmark suite before the evaluator contract and case format are known or safely inferred.

---

## 1. Validity Hierarchy

```text
Tier 0 — Direct real trace: real task, ticket, session, issue, support thread, incident, API trace, CI run, document workflow, query log, UI session, or user interaction.
Tier 1 — Sanitized real trace: sensitive details removed while preserving sequence, artifact relationships, constraints, language shape, failure mechanism, and outcome.
Tier 2 — Mutated real trace: one or two controlled changes while preserving causal mechanism and oracle.
Tier 3 — Composite real-derived case: assembled from multiple real traces from the same task class, with documented provenance and preserved causal structure.
Tier 4 — Expert-modeled synthetic gap case: allowed only for known coverage gaps, capped, disclosed, and excluded from high-confidence claims unless calibrated.
Tier 5 — Toy, keyword, claim, benchmark-shaped, or ungrounded case: invalid.
```

Default rules:

- Prefer Tier 0–2.
- Permit Tier 3 only with a source ledger and causal-skeleton explanation.
- Cap Tier 4 at 10% of a ranking suite unless the benchmark is explicitly exploratory.
- Reject Tier 5.
- Do not make production, global, safety-critical, or compliance claims from suites dominated by low-realism cases.

---

## 2. Benchmark Claim Map

Before producing cases, define what real workload the benchmark claims to represent and what decision the benchmark will support.

```yaml
benchmark_claim_map:
  system_under_test: prompt | agent | model | api | app | library | workflow | ui | pipeline | policy | integration | process | other
  evaluation_goal: what the benchmark will decide
  decision_use: rank_versions | qualify_release | regression_guard | compare_architectures | monitor_drift | diagnose_capability | exploratory_mapping | other
  deployment_or_usage_claim: real workload represented by the suite
  target_population:
    actors: []
    task_families: []
    domains: []
    languages_locales: []
    artifact_families: []
    environments: []
    risk_levels: []
    interaction_lengths: []
    error_or_noise_profiles: []
  excluded_populations:
    - population: ...
      reason: out_of_scope | unavailable_sources | unsupported_by_runner | safety_or_privacy | separate_benchmark_needed
  representation_debt:
    known_missing_segments: []
    likely_missing_segments: []
    risk_to_claim: low | medium | high
  validity_risk_budget:
    acceptable_synthetic_gap_fill_percent: 0-10
    minimum_case_validity_for_ranking: 80
    minimum_suite_validity_for_ranking: 85
    minimum_format_validity: 95
    minimum_first_shot_readiness: 95
  claims_forbidden_without_real_anchors:
    - production readiness
    - global superiority
    - safety-critical reliability
    - compliance sufficiency
    - domain-general superiority
```

If the target population is undefined, generate only an exploratory suite and label the result low-confidence.

---

## 3. Evaluator Contract Discovery

A case must fit the test that will run it. Discover or infer the evaluator contract before case generation.

Use available evidence in this order:

```text
1. explicit schema files, validators, test harness code, parser code, CLI help, config files
2. existing accepted cases, fixtures, snapshots, score files, report outputs
3. CI scripts, package scripts, Makefiles, workflow files, runner docs
4. adjacent conventions such as directory layout, naming, metadata, artifact patterns
5. minimal neutral adapter format only when the native format cannot be discovered
```

When no example or sample exists, infer the smallest safe contract from schemas, runner entrypoints, parser requirements, CLI arguments, file naming, and scoring outputs. Do not invent unsupported native fields. Unknown fields must be placed in an adapter or metadata envelope that the runner can ignore safely.

```yaml
evaluator_contract:
  runner_name: known_or_unknown
  runner_entrypoint: command_or_api_or_manual_protocol
  accepted_file_types: []
  required_fields: []
  optional_fields: []
  forbidden_fields: []
  naming_rules: []
  directory_layout: []
  parser_constraints: []
  scoring_inputs: []
  scoring_outputs: []
  environment_requirements: []
  isolation_requirements: []
  side_effect_limits: []
  validation_method: schema | parser | dry_load | static_check | manual_inspection | other
  confidence: high | medium | low
```

Critical blockers:

- Unknown required fields.
- Ambiguous scoring output.
- Unloadable file format.
- Path layout incompatible with runner.
- Required external dependency unavailable.
- Case requires side effects prohibited by the benchmark.
- Oracle cannot be evaluated by the declared scoring system.

---

## 4. Source Ledger and Claim Discipline

Every realism claim must be traceable.

```yaml
source_ledger_entry:
  source_id: stable sanitized identifier
  validity_tier: 0 | 1 | 2 | 3 | 4 | 5
  source_type: user_request | issue | ticket | support_thread | incident | ci_log | production_log | api_trace | ui_session | query_log | analytics_sample | dataset_snapshot | document_workflow | audit_record | expert_model | other
  acquisition_mode: direct | summarized | sampled | redacted | generated_from_expert_model
  source_timeframe: exact_or_range_if_safe
  source_population: workload, domain, product area, deployment, cohort, or environment
  observed_fields: []
  measured_fields: []
  inferred_fields: []
  assumed_fields: []
  redacted_fields: []
  preserved_properties: []
  transformed_properties: []
  inadmissible_claims: []
  admissibility: final_ranking | calibration_only | exploratory | reject
  admissibility_reason: why this source can or cannot support benchmark cases
```

Use claim tags:

```text
observed | measured | inferred | assumed | external-cited | external-unverified | not-evaluated
```

Do not claim tests passed, commands ran, artifacts existed, APIs behaved, or external facts are current unless verified. If a case relies on an assumption, record the assumption and reduce validity confidence.

---

## 5. Real Task Anatomy

A realistic test case must describe the task it is trying to synthesize, not only its expected answer.

```yaml
task_anatomy:
  actor_intent:
    actor: end_user | developer | operator | analyst | customer | auditor | scheduler | system_event | integration | learner | manager | other
    user_goal: real-world goal, not benchmark goal
    success_condition: what success means outside the benchmark
    failure_consequence: annoyance | wasted_time | bad_decision | data_loss | outage | security_risk | compliance_risk | financial_cost | safety_risk | reputational_risk
    pressure: urgency | ambiguity | incomplete_context | stale_state | conflicting_goals | cost_limit | privacy_limit | fatigue | none
  capability_profile:
    primary_capability: answer | classify | retrieve | transform | code | plan | repair | decide | refuse | escalate | execute | compare | summarize | validate | route | monitor | recover | release | localize | negotiate_constraints | other
    secondary_capabilities: []
    unacceptable_shortcuts: []
  language_model:
    language: ISO code or mixed
    locale: region, calendar, unit, currency, date, number, or legal convention if relevant
    register: terse | formal | casual | frustrated | operational | legal | support | developer | executive | academic | multilingual | noisy
    information_density: underspecified | normal | verbose | pasted_artifacts | noisy | contradictory
    error_style: typo | shorthand | jargon | copy_paste | incomplete_records | speechlike | none
  context_model:
    artifacts: []
    metadata_to_preserve: [timestamps, versions, IDs, paths, status fields, error codes, environment, locale]
    hidden_dependencies: []
    stale_or_conflicting_state: []
    realistic_noise: []
  interaction_model:
    turn_count: single | multi_turn | batch | asynchronous_trace | event_driven
    allowed_tools_or_actions: []
    forbidden_tools_or_actions: []
    side_effects: none | simulated | sandboxed | irreversible
```

Reject cases that lack a real user or system goal, realistic state, a measurable outcome, or a meaningful failure consequence.

---

## 6. Causal Skeleton Preservation

Before writing a case, extract the causal skeleton from the source.

```yaml
causal_skeleton:
  trigger: what starts the task
  prior_state: files, records, data, environment, permissions, history, or constraints already present
  actor_gap: what the actor does not know or cannot do alone
  required_capability: what the system must actually perform
  decision_point: what must be decided, transformed, fixed, refused, routed, or verified
  evidence_needed: what objective evidence proves success or failure
  failure_mechanism: how weak systems are expected to fail
  consequence: why the failure matters
  oracle_basis: source, rule, invariant, calculation, test, diff, log, human rubric, or external authority
```

Mutation is allowed only when it preserves the causal skeleton. Do not mutate so heavily that the case becomes a toy, puzzle, or benchmark-shaped prompt.

### Mutation Budget

```yaml
mutation_budget:
  preserved:
    - actor goal
    - failure mechanism
    - artifact relationship
    - oracle basis
    - consequence class
  may_change:
    - names and identifiers
    - domain labels
    - nonessential quantities
    - benign wording
    - redacted details
  must_not_change:
    - required capability
    - scoring oracle
    - dependency direction
    - safety or compliance implication
    - runner format
  mutation_count: 0-2 preferred
  mutation_risk: low | medium | high
```

---

## 7. Case Contract Grammar

Use the native evaluator format when known. When no native format is known, use this neutral grammar and provide an adapter.

```yaml
id: globally_unique_case_id
title: short descriptive name
category: primary capability or workflow class
difficulty: easy | medium | hard | adversarial
validity_tier: 0 | 1 | 2 | 3 | 4
source_ids: []

benchmark_claim_alignment:
  task_family: ...
  target_population_segment: ...
  decision_use: ...
  represented_risk: ...

format_fit:
  native_format: known | inferred | adapter
  runner_entrypoint: ...
  required_fields_present: true
  parser_safe: true
  scoring_safe: true
  first_shot_ready: true

realism:
  causal_skeleton_summary: ...
  preserved_real_properties: []
  transformed_properties: []
  realism_risks: []
  evidence_inversion: what would show this case is unrealistic, misleading, or invalid

initial_state:
  files: []
  records: []
  data: []
  environment: []
  permissions: []
  prior_interactions: []
  constraints: []

stimulus:
  user_or_system_input: ...
  changed_artifacts: []
  event: ...

expected_behavior:
  expected_decision: pass | fail | block | repair | escalate | refuse | transform | route | answer | no_action | other
  required_actions: []
  forbidden_actions: []
  required_evidence: []
  expected_artifacts: []
  allowed_variance: []

oracle:
  oracle_type: exact | semantic | rubric | invariant | executable_test | diff | metric | human_review | hybrid
  pass_conditions: []
  fail_conditions: []
  critical_failures: []
  hidden_from_stimulus: true

scoring:
  total_points: 100
  criteria: []
  validity_weighting: enabled | disabled

readiness:
  files_complete: true
  paths_valid: true
  dependencies_declared: true
  side_effects_controlled: true
  checksums_recorded: true
  dry_load_status: pass | not_run | not_applicable
```

---

## 8. First-Shot Readiness

Some benchmarks can be run only once because the attempt is expensive, live, rate-limited, irreversible, externally observed, or reserved for final comparison. A case must be ready before that attempt.

Do not rely on trial-and-error against the real target. Preflight only through methods that do not consume the benchmark attempt.

Allowed preflight methods:

```text
schema validation, static parsing, dry-load in a clone, checksum verification, fixture path inspection, dependency inspection, oracle consistency check, scoring-rubric linting, adapter round-trip, sandbox-only smoke test, manual contract review
```

Readiness blockers:

- Missing required file or field.
- Fixture path mismatch.
- Unresolved dependency.
- Ambiguous expected output.
- Oracle visible in the stimulus.
- Score cannot be computed from captured outputs.
- Case requires prohibited network, credentials, destructive actions, or private data.
- Adapter modifies semantics instead of only translating format.
- The case needs a real run to discover whether it is loadable.

---

## 9. Oracle Sealing and Tamper Resistance

The oracle must be objective enough to score but not leaked into the stimulus.

Rules:

- Do not put expected labels, answer keys, hidden bug names, exact rubric phrases, or pass/fail hints in user-visible input unless they naturally exist in the real source.
- Keep expected behavior, scoring, and critical failures in evaluator-only metadata.
- When using semantic rubrics, define acceptable and unacceptable answer classes.
- When using executable oracles, include commands, expected exit codes, output files, and environmental assumptions.
- When using human rubrics, include examples of acceptable evidence and critical failure overrides.
- Record evidence inversion: what evidence would make the oracle wrong.

---

## 10. Anti-Synthetic Rejection Gate

Reject or quarantine cases with these signs:

```text
- No source ledger or only vague expert intuition.
- User asks directly for the tested feature by name.
- Stimulus contains benchmark vocabulary rather than real task language.
- Case is solvable by keyword matching or label copying.
- All artifacts are clean, minimal, symmetric, and context-free.
- No realistic noise, stale state, constraints, or trade-off.
- Expected answer is obvious from the title or category.
- Failure has no consequence outside the benchmark.
- Oracle is subjective but scored as objective.
- Multiple cases share the same skeleton with only names changed.
- Case cannot be loaded or scored by the runner.
- Case requires the model to know hidden facts not present in state, source, or allowed tools.
```

A case may still be simple. It must not be toy-like.

---

## 11. Sampling Rules

A benchmark suite must represent the claimed workload, not the generator's convenience.

### Sampling Frame

```yaml
sampling_frame:
  target_population: ...
  source_pool_size: ...
  included_segments: []
  excluded_segments: []
  stratification_dimensions:
    - task_family
    - difficulty
    - language_locale
    - artifact_type
    - risk_level
    - interaction_length
    - noise_profile
    - environment
    - expected_decision
  sampling_method: proportional | stratified | risk_weighted | balanced | adversarial_supplement | exploratory
  sibling_case_cap: max 2-3 per source skeleton unless explicitly testing metamorphic behavior
  synthetic_gap_fill_percent: 0-10
```

### Recommended Distribution

Adjust to the target population when real data exists. Otherwise start with:

```text
common happy-path or routine tasks:      20-30%
normal complex workflow tasks:           25-35%
edge/recovery/error tasks:               15-25%
risk-sensitive or adversarial tasks:     10-20%
long-tail locale/artifact/noise tasks:    5-15%
token/latency/cost pressure tasks:        5-10%
```

Do not let rare adversarial cases dominate a benchmark that claims routine production performance. Do not omit long-tail cases when the benchmark claims global or robust performance.

---

## 12. Global Differentiability

Cases must be different enough that passing one does not imply passing the rest by pattern memorization.

Compute or estimate pairwise distance across:

```text
capability, source skeleton, actor, artifact type, input shape, language/locale, risk consequence, expected decision, oracle type, failure mechanism, environment, interaction length, constraint type, noise profile
```

Quarantine near-duplicates unless they are part of a declared metamorphic set.

```yaml
case_distance:
  min_pairwise_distance: 0.35 for local suites, 0.50 for global suites
  max_same_skeleton_cluster_size: 3
  max_same_source_family_percent: 20
  required_unique_failure_mechanisms: at least 6 for suites of 30+
  required_oracle_mix: at least 3 oracle types for broad suites
```

### Metamorphic Sibling Rules

Metamorphic siblings are allowed when they test whether the same capability survives realistic variation.

Each sibling must change at least one meaningful dimension:

```text
locale, artifact format, noise profile, dependency state, risk level, interaction length, or constraint conflict
```

Each sibling must preserve the same core oracle or intentionally document why the oracle changes.

---

## 13. Calibration Against Real Anchors

Use held-out real traces when available.

```yaml
calibration:
  anchor_sources: []
  anchor_validity_tiers: []
  compared_dimensions:
    - task_family_distribution
    - artifact_distribution
    - language_distribution
    - error_distribution
    - risk_distribution
    - model_failure_distribution
    - score_ranking_correlation
  calibration_methods:
    - distribution_distance
    - expert_blind_rating
    - case_to_trace_matching
    - failure_mode_overlap
    - ranking_correlation
  acceptance_thresholds:
    minimum_realism_rating: 80
    maximum_distribution_drift: 20_percent_relative_unless_justified
    minimum_failure_mode_overlap: 70
```

If calibration is unavailable, report the suite as uncalibrated and reduce confidence.

---

## 14. Diagnostic Capture

A benchmark should reveal why a system failed, not only that it failed.

Each case should capture enough output to classify failures into:

```text
capability_failure, format_failure, oracle_ambiguity, missing_context, tool_or_environment_failure, safety_or_policy_failure, hallucinated_evidence, premature_completion, over-refusal, under-refusal, shortcut_solution, excessive_cost
```

Add diagnostic fields:

```yaml
diagnostics:
  required_logs: []
  required_outputs: []
  required_artifacts_after_run: []
  failure_classification_rules: []
  evaluator_notes_allowed: true | false
  reproducibility_materials: []
```

---

## 15. Scoring and Validity

Use two scores: performance score and validity score.

```yaml
performance_scoring:
  total_points: 100
  recommended_weights:
    task_outcome_correctness: 25
    evidence_or_reasoning_quality: 15
    artifact_or_action_correctness: 15
    constraint_compliance: 15
    oracle_specific_requirements: 15
    safety_and_failure_handling: 10
    efficiency_or_cost_discipline: 5
```

Validity scores determine whether the performance score can be trusted.

```yaml
validity_scoring:
  non_synthesized_closeness_score: 0-100
  source_grounding_score: 0-100
  format_validity_score: 0-100
  first_shot_readiness_score: 0-100
  oracle_quality_score: 0-100
  global_differentiability_score: 0-100
  calibration_score: 0-100
  decision_relevance_score: 0-100
  overall_case_validity: min(all above scores that apply)
```

Interpretation:

```text
95-100: production-grade case for the stated claim
85-94: strong case with minor limitations
75-84: usable for exploratory or internal ranking, not strong claims
60-74: weak; quarantine unless needed for gap analysis
<60: invalid for benchmark decisions
```

Critical validity failures override numeric scores:

- No objective oracle.
- No source ledger for a realism claim.
- Format not loadable.
- Runner cannot capture required output.
- Oracle leaked into stimulus.
- Expected behavior contradicts initial state.
- Case cannot be isolated.
- Case requires unapproved external state, credentials, or destructive side effects.
- Near-duplicate used as independent evidence.

---

## 16. Ready-to-Test Bundle

Each released case or suite must include:

```text
case file or native case directory
fixture files
source ledger or sanitized provenance summary
oracle metadata hidden from the system under test
scoring rubric or executable scorer
runner instructions
adapter if needed
checksums
preflight validation result
known limitations
```

Recommended manifest:

```yaml
case_bundle_manifest:
  bundle_id: ...
  cases: []
  files:
    - path: ...
      sha256: ...
      purpose: case | fixture | oracle | scorer | adapter | documentation
  runner_contract_ref: ...
  scoring_contract_ref: ...
  environment_assumptions: []
  prohibited_side_effects: []
  preflight_checks:
    schema_valid: true
    paths_exist: true
    checksums_recorded: true
    oracle_hidden: true
    scorer_available: true
    dry_load_passed: true | false | not_applicable
  release_status: ready | quarantine | exploratory_only | reject
```

---

## 17. Suite-Level Report

A benchmark report must include:

```text
1. benchmark objective and decision use
2. system versions or configurations tested
3. target population and representation debt
4. source ledger summary and validity tier distribution
5. evaluator contract and format validation method
6. case taxonomy and sampling method
7. realism and anti-synthetic methodology
8. oracle types and scoring rubric
9. preflight and first-shot readiness results
10. full score matrix
11. validity-weighted score matrix
12. per-version summary
13. category-level strengths and weaknesses
14. critical failures and failure classes
15. calibration against real anchors, or explicit uncalibrated limitation
16. global differentiability analysis
17. token, latency, or cost analysis when relevant
18. recommendation and claim boundaries
```

Required score matrix columns:

```csv
case_id,category,difficulty,validity_tier,source_ids,language_locale,artifact_type,expected_decision,oracle_type,performance_score,case_passed,critical_failure,non_synthesized_closeness_score,source_grounding_score,format_validity_score,first_shot_readiness_score,oracle_quality_score,global_differentiability_score,calibration_score,decision_relevance_score,overall_case_validity,validity_weighted_score,failure_class,notes
```

---

## 18. Release Gates

Do not release a benchmark suite for ranking unless all gates pass:

```text
[ ] Benchmark claim and decision use are explicit.
[ ] Evaluator format and runner contract are known or safely adapted.
[ ] Every ranking case has source ledger coverage or is clearly marked exploratory.
[ ] Every ranking case has an objective oracle.
[ ] Every ranking case passes format validation without consuming the real attempt.
[ ] Every ranking case is first-shot-ready.
[ ] Oracle content is sealed away from the stimulus.
[ ] Suite meets minimum differentiability and sampling requirements.
[ ] Synthetic gap-fill remains within the stated budget.
[ ] Critical validity failures are zero.
[ ] Known limitations and representation debt are reported.
```

If any gate fails, mark the suite `quarantine`, `exploratory_only`, or `reject`.

---

## 19. Minimal Workflow

For small tasks, use this compact flow:

```text
1. What decision will this benchmark support?
2. What real workload does it claim to represent?
3. What format will the evaluator accept?
4. What real or real-derived source anchors the case?
5. What capability must the case force?
6. What objective oracle scores it?
7. What would make the case invalid?
8. Can it load and score on the first attempt?
9. Is it meaningfully different from existing cases?
10. What validity score limits the claim?
```

---



---

## LLM Evaluation Extension

Use this extension whenever the system under test is an LLM, LLM-powered agent, prompt, chatbot, tool-using model, retrieval-augmented system, coding model, evaluator model, planner, assistant workflow, or model-mediated automation.

LLM benchmarks have special failure modes. A case may be realistic, format-valid, and first-shot-ready, yet still invalid for LLM evaluation if it ignores stochastic outputs, prompt sensitivity, context-window effects, safety/refusal behavior, judge bias, or tool-call uncertainty.

### LLM Characteristic Map

Before generating LLM cases, define the evaluation target:

```yaml
llm_characteristic_map:
  model_or_system_type: base_model | chat_model | agent | rag_system | coding_assistant | tool_using_assistant | evaluator_judge | workflow | other
  interaction_mode: single_turn | multi_turn | long_context | batch | streaming | tool_augmented | retrieval_augmented | code_execution | human_in_loop
  model_controls:
    temperature: known | unknown | variable
    seed: fixed | unavailable | unknown
    max_tokens: known | unknown
    system_prompt_visible: true | false | partial | unknown
    tool_access: none | declared | dynamic | unknown
    memory_or_state: none | session | persistent | retrieved | unknown
  output_contract:
    required_format: free_text | json | yaml | code | patch | table | citations | tool_calls | artifacts | mixed
    allowed_variance: exact | semantically_equivalent | rubric_bounded | multi_solution | probabilistic
    forbidden_outputs: []
  scorer_or_judge:
    scorer_type: deterministic | executable | rubric | llm_judge | human | hybrid
    judge_bias_risks: []
    calibration_required: true | false
  deployment_risks:
    hallucination | unsafe_refusal | over_refusal | tool_misuse | privacy_leakage | instruction_conflict | stale_fact | context_loss | excessive_cost | other
```

If these fields are unknown, mark them unknown and reduce validity confidence. Do not invent model controls or hidden prompts.

### LLM Capability Coverage

A globally valid LLM suite should cover materially different model behaviors, not just topic categories.

Recommended dimensions:

```text
instruction following, task decomposition, ambiguity handling, uncertainty calibration, abstention, evidence grounding, retrieval use, tool use, code reasoning, mathematical reasoning, transformation fidelity, summarization fidelity, long-context selection, multi-turn state tracking, planning, constraint negotiation, safety/refusal boundaries, privacy preservation, multilingual handling, locale conventions, tone/register control, output-format discipline, self-correction, error recovery, cost/token discipline
```

Avoid suites where every case is merely a different subject for the same instruction pattern.

### Prompt Sensitivity and Instruction Conflict

LLM cases should detect whether the model solves the real task rather than overfitting to prompt wording.

Include realistic variants such as:

```text
underspecified request, conflicting user constraints, stale conversation state, irrelevant pasted context, misleading but non-authoritative text, role confusion, tool instruction conflicts, required refusal with safe alternative, exact-format requirement under pressure, and user request that asks for a shortcut the benchmark forbids
```

Forbidden case design:

```text
- The stimulus names the exact capability being scored.
- The answer is recoverable from the title, category, or hidden metadata.
- The prompt says “be grounded” while providing no source-grounding requirement in the oracle.
- The case rewards verbosity rather than correctness.
- The case relies on private chain-of-thought disclosure.
```

### Stochasticity and One-Shot Policy

LLM outputs may vary. A benchmark must declare whether it is one-shot or multi-run.

```yaml
llm_run_policy:
  run_mode: one_shot | repeated_samples | fixed_seed | human_final | production_replay
  sample_count: 1 | 3 | 5 | other
  aggregation: first_run | mean | median | best_of_n | worst_of_n | pass_if_any | pass_if_all
  acceptable_variance:
    content_variance: none | low | medium | high
    format_variance: none | low
    reasoning_path_variance: allowed_if_final_correct | not_scored
    tool_call_variance: allowed_if_equivalent | not_allowed
  confidence_reporting: required | optional | not_applicable
```

Rules:

- For release qualification, prefer one-shot or fixed-seed runs unless production will use repeated sampling.
- Do not use best-of-n unless the deployed system actually uses best-of-n.
- Use semantic or rubric-bounded oracles only when exact matching is unrealistic.
- Score the final answer and observable evidence, not hidden reasoning.
- Record variance as a benchmark property, not an evaluator failure.

### Long-Context and State Behavior

When evaluating long-context or multi-turn systems, include checks for:

```text
relevant detail retrieval, irrelevant-context resistance, primacy/recency bias, stale-state correction, conflict resolution between old and new instructions, citation to the right source span, preservation of IDs/paths/numbers, and graceful handling of context overflow or missing context
```

A long-context case is invalid if the oracle requires information not present in the supplied context, allowed retrieval source, or declared tool output.

### Evidence Grounding and Hallucination Controls

For LLM cases involving facts, documents, code, logs, or tool outputs, require observable evidence.

Critical failures:

```text
fabricated citation, fabricated tool result, invented file/path/API response, unsupported current fact, unsupported quote, false claim that a command or test was run, failure to abstain when evidence is missing, using low-authority text over higher-authority source, and silently filling missing data
```

When current or niche external facts are required, either provide the source inside the case, require an allowed lookup tool, or mark the case invalid for closed-book evaluation.

### Tool-Use and Agentic Behavior

For tool-using LLMs, separate task success from tool protocol success.

```yaml
tool_use_contract:
  allowed_tools: []
  forbidden_tools: []
  required_tool_calls: []
  optional_tool_calls: []
  tool_failure_simulation: unavailable | timeout | malformed_output | contradictory_output | stale_output | permission_denied | none
  side_effect_policy: none | sandbox_only | reversible | irreversible_prohibited
  evidence_required_from_tools: []
```

Score:

```text
correct tool choice, safe argument construction, correct interpretation of tool output, recovery from tool failure, no fabricated tool result, no unapproved side effect, and correct final answer after tool use
```

### Multilingual, Locale, and Register Controls

LLM language ability is not only translation. Include realistic locale differences:

```text
date formats, names, honorifics, currencies, units, legal or business conventions, scripts, romanization, code-switching, informal phrasing, domain jargon, politeness level, and culturally specific ambiguity
```

A multilingual case should state whether success requires same-language response, translation, localization, cross-lingual retrieval, or culturally correct interpretation.

### Safety and Refusal Boundary Cases

Include both sides of the safety boundary:

```text
must_refuse, must_comply_safely, must_redirect, must_ask_for_missing_high-stakes_context, must_not_over_refuse, must_preserve_privacy, must_not_expose_secrets, must_not_follow_prompt_injection
```

For high-stakes domains, distinguish helpful general information from professional advice, and require uncertainty boundaries when evidence is incomplete.

### Judge and Scorer Reliability

If scoring uses an LLM judge, add judge validation:

```yaml
judge_reliability:
  rubric_anchored: true
  blind_to_version_identity: true
  answer_key_hidden_from_system_under_test: true
  calibration_examples: []
  inter_judge_agreement_required: true | false
  deterministic_checks_preferred: true
  bias_checks:
    - verbosity_bias
    - style_bias
    - position_bias
    - brand_or_version_bias
    - language_bias
    - refusal_bias
  adjudication_rule: deterministic_override | second_judge | human_review | rubric_priority
```

Do not allow an LLM judge to reward fluent unsupported answers over concise grounded answers.

### LLM Case Schema Additions

Add these fields to each applicable case:

```yaml
llm_specific:
  target_behavior: instruction_following | grounding | retrieval | tool_use | reasoning | coding | safety | multilingual | long_context | multi_turn | format_control | cost_control | other
  prompt_sensitivity_risk: low | medium | high
  stochasticity_policy: one_shot | repeated | fixed_seed | not_applicable
  context_pressure: none | moderate | high | overflow_risk
  hallucination_risk: low | medium | high
  refusal_boundary: must_comply | must_refuse | must_redirect | must_not_over_refuse | not_applicable
  tool_dependency: none | optional | required | simulated_failure
  output_format_strictness: exact | schema | loose | semantic
  judge_risk: none | low | medium | high
  token_cost_pressure: none | moderate | high
```

### LLM Validity Scores

Extend validity scoring:

```yaml
llm_validity_scoring:
  prompt_sensitivity_coverage_score: 0-100
  stochasticity_handling_score: 0-100
  context_fidelity_score: 0-100
  hallucination_resistance_score: 0-100
  tool_protocol_validity_score: 0-100
  safety_boundary_score: 0-100
  multilingual_locale_score: 0-100
  judge_reliability_score: 0-100
  cost_realism_score: 0-100
  llm_case_validity: min(all applicable LLM scores)
```

For LLM benchmarks:

```text
overall_case_validity = min(base_case_validity, llm_case_validity)
```

### LLM Release Gates

Do not release an LLM benchmark for ranking unless these gates pass:

```text
[ ] Model controls and run policy are recorded or explicitly unknown.
[ ] Allowed tools, retrieval sources, and external knowledge assumptions are declared.
[ ] Output variance is compatible with the oracle.
[ ] Hidden answer keys are not present in the stimulus.
[ ] Scoring does not require private chain-of-thought.
[ ] Current-fact cases provide sources or allowed lookup tools.
[ ] Safety cases include both under-refusal and over-refusal checks when relevant.
[ ] Multilingual claims are supported by actual multilingual or locale-sensitive cases.
[ ] LLM judge, if used, is calibrated, blinded, and checked for bias.
[ ] Token, latency, or cost pressure is represented when it affects deployment.
```

## Final Rule

A benchmark test case is proper only when an evaluator can answer:

```text
Given this initial state and stimulus, did the system perform the required real-world capability, and can that result be trusted for the benchmark's stated decision?
```

If the answer cannot be determined objectively, if the case cannot run in the target format, or if the case would not plausibly occur in the claimed workload, the test case is not benchmark-grade.
