---
name: realitybench-caseforge
description: Generates source-grounded, evaluator-fit, first-shot-ready benchmark cases and evaluation suites with explicit claim mapping, source ledgers, oracle sealing, global differentiability, validation tiers, LLM evaluation controls, repeatable harnesses, audit ledgers, and release gates.
version: 1.1.2
last_updated: 2026-06-18
---

# RealityBench CaseForge

## Identity
RealityBench CaseForge creates benchmark cases and evaluation suites that are realistic enough to support a stated decision and exact enough to load, run, score, audit, and recompute in the target evaluator on the first permitted attempt.

A released case must be realistic, source-grounded, evaluator-fit, format-valid, globally differentiable, first-shot-ready, oracle-sealed, objectively or rubric-scoreable, decision-relevant, and honestly tiered. If any required property is unknown, mark the suite `exploratory_only` and cap the claim.

## Activation and Non-Goals
Use this skill when asked to synthesize, repair, validate, benchmark, score, compare, rank, package, or audit benchmark cases for prompts, agents, models, APIs, apps, workflows, retrieval systems, document pipelines, coding systems, judge systems, or other evaluable systems.

Do not use it to create toy examples, marketing demos, schema-invalid samples, answer-leaking prompts, arbitrary synthetic examples, or cases that require trial-and-error against the real evaluator to discover whether they can load.

## Mandatory Operating Order
1. Define the benchmark claim, decision use, forbidden claims, and minimum validation tier.
2. Identify target population, exclusions, representation debt, operational setting, and validity risk budget.
3. Discover the evaluator contract: schema, runner entrypoint, parser constraints, fixture paths, scoring inputs, scoring outputs, aggregation rules, side effects, accepted examples, and rejected examples.
4. Build the source ledger and admissibility map before generating cases.
5. Extract real task anatomy and causal skeleton from admissible sources.
6. Write the sampling plan, calibration anchors, split policy, and synthetic-gap budget.
7. Select coverage axes, differentiability targets, and failure-localization goals.
8. Construct, sanitize, composite, or mutate cases inside the mutation budget.
9. Seal oracle data away from the stimulus, visible metadata, retrieval corpus, and system under test.
10. Audit leakage, shortcuts, memorization risk, trivial-baseline passability, safety risks, and evaluator incompatibility.
11. Preflight without consuming the real attempt.
12. Score performance and validity separately; compute coverage debt, pairwise distance, oracle quality, diagnostic value, and release readiness.
13. Package a ready-to-test bundle with manifest, cases, fixtures, scorer or rubric, adapter if needed, source ledger, oracle metadata, differentiability matrix, raw result rows, checksums, limitations, validation tier, and run status.
14. Run an internal adversarial review before final recommendation or release.

## Precedence
Native evaluator schema, runner code, accepted fixtures, rejected fixtures, CI scripts, scorer outputs, and observed load behavior outrank prose preference. System/developer safety rules outrank user convenience. Oracle sealing outranks readability. Realism, evaluator compatibility, and objective scoring outrank case quantity. Verified evidence outranks plausible explanation. Raw rows outrank summaries. Claim caps outrank aspirational wording.


## Scale Modes
Match deliverables to risk and user need without deleting critical gates:

| Mode | Use when | Minimum handoff |
|---|---|---|
| `micro_probe` | user needs a few diagnostic examples, not a ranking benchmark | claim map, cases, oracle notes, limitations, validation tier |
| `fixture_suite` | user needs reusable scored cases | manifest, cases, fixtures, source ledger, oracles, scorer/rubric, validation log, checksums |
| `ranking_benchmark` | user will compare systems or make release decisions | full bundle, raw rows, differentiability matrix, coverage debt, baselines, sensitivity, recompute script |
| `audit_release` | external or high-stakes review is expected | ranking benchmark plus privacy/license review, correction audit, independent review notes where available |

Do not force a full bundle for a micro-probe, but never omit oracle sealing, source status, evaluator fit, claim cap, or limitations.

## Claim Map and Scope Discipline
Before generation, write `benchmark_claim_map`:

```yaml
system_under_test:
evaluation_goal:
decision_use:
deployment_or_usage_claim:
target_population:
excluded_populations:
operational_setting:
representation_debt:
validity_risk_budget:
forbidden_claims:
minimum_validation_tier:
planned_fixture_count:
planned_source_count:
release_status:
claim_cap:
```

If target population, evaluator contract, source basis, oracle, or scoring method is undefined, create only an exploratory suite. Do not claim production readiness, global superiority, compliance sufficiency, safety sufficiency, or domain-general superiority without matching sources, validation tier, and release gates.


## Acceptance Criteria and Stop Gates
Before writing cases, define machine-checkable acceptance criteria where possible:

```yaml
acceptance_criteria:
  schema_validity:
  loader_success:
  oracle_separation:
  minimum_source_tier:
  minimum_coverage_axes:
  required_negative_controls:
  required_calibration_anchors:
  maximum_near_duplicate_rate:
  allowed_synthetic_gap_rate:
  privacy_license_clearance:
  scorer_recompute_command:
  ready_status_blockers:
```

A suite cannot be marked `ready` unless every blocker criterion is either satisfied or explicitly waived by the user with a downgraded release status. Do not let a larger fixture count compensate for a failed critical gate.

## Case Lifecycle and Status Transitions
Track each case through `draft → contract_checked → source_checked → oracle_sealed → shortcut_checked → scorer_checked → package_checked → released`. A case may move backward after any amendment. Do not promote directly from draft to released.

Allowed terminal statuses are `ranking`, `calibration`, `regression`, `exploratory`, `quarantine`, and `reject`. A quarantined case may not be counted toward claim coverage until repaired and rechecked. A rejected case must retain its rejection reason so the same defect is not reintroduced.

## Evaluator Contract Discovery
Treat evaluator compatibility as a validity requirement, not a formatting afterthought. Inspect, in order:

1. Native schema, type definitions, JSON schema, protobuf, database model, or fixture contract.
2. Runner entrypoint, CLI flags, working directory, environment variables, dependency files, and path assumptions.
3. Parser constraints: required fields, optional fields, enums, escaping, encodings, line formats, token limits, attachment handling, timestamps, locale fields, and path rules.
4. Existing accepted fixtures, rejected fixtures, golden rows, logs, and CI examples.
5. Validators, scorer code, rubric files, adapters, aggregation code, and output examples.
6. Scoring inputs, scoring outputs, tie-breaking, weighting, partial credit, abstention handling, and failure classes.
7. Side-effect boundaries: network, credentials, filesystem writes, destructive actions, rate limits, paid APIs, external tools, and privacy constraints.

Record unresolved contract fields as blockers unless a neutral adapter can translate representation without changing semantics. Never silently normalize away fields that the evaluator uses for scoring.

## Validity Hierarchy
Prefer direct real traces, sanitized real traces, and lightly mutated real traces. Composite real-derived cases are allowed only with provenance and causal-skeleton documentation. Expert-modeled synthetic gap cases are allowed only for declared uncovered boundaries and are capped at 10% of ranking suites unless the benchmark is explicitly exploratory. Toy, keyword-shaped, benchmark-shaped, ungrounded, symmetric, no-consequence, answer-leaking, or schema-invalid cases are invalid.

## Source Ledger and Admissibility Map
Every realism claim must be tied to a source-ledger entry:

```yaml
source_id:
validity_tier: direct_real | sanitized_real | lightly_mutated_real | composite_real_derived | expert_modeled_gap | invalid
source_type:
acquisition_mode:
timeframe:
population:
observed_fields:
measured_fields:
inferred_fields:
assumed_fields:
preserved_properties:
transformed_properties:
redactions_or_sanitization:
privacy_or_license_constraints:
inadmissible_claims:
allowed_case_uses:
source_cluster:
final_admissibility:
```

Use claim tags: `observed`, `measured`, `inferred`, `assumed`, `external-cited`, `external-unverified`, and `not-evaluated`. Never upgrade an inferred or assumed field into an observed fact. Redaction must preserve causal validity; otherwise downgrade the source tier or quarantine the case.


## Data Governance and Redaction Boundaries
For real traces, record the minimum data needed to preserve causal validity and remove everything else. Redaction must not change the decision boundary, available evidence, temporal ordering, legal/business meaning, or locale-specific interpretation. When redaction weakens the causal skeleton, downgrade the source tier and mark the affected claim as unsupported or exploratory.

Never place secrets, credentials, private personal data, paid API keys, proprietary unreleased details, or license-restricted content in generated stimuli unless the user explicitly authorizes a compliant internal benchmark and the bundle remains access-controlled. Public release requires a separate privacy/license pass.

## Real Task Anatomy
Extract the practical structure that makes the task real:

```yaml
actor:
intent:
stakes_or_consequence:
domain_context:
initial_state:
available_information:
hidden_information:
artifact_state:
constraints:
ambiguities:
noise_or_error_profile:
required_decision_or_action:
observable_success_signal:
plausible_failure_modes:
```

A case without actor intent, constraints, state, and consequence is usually not benchmark-grade.

## Causal Skeleton and Mutation Budget
Represent each case as a causal skeleton:

```yaml
trigger:
context_dependencies:
necessary_evidence:
reasoning_or_action_path:
decision_boundary:
expected_behavior:
failure_mechanism:
oracle_basis:
```

Mutations may alter names, dates, quantities, locale, format, order, surface wording, noise level, and non-causal distractors only when expected behavior and oracle remain causally valid. Mutations must not introduce impossible states, remove required evidence, leak answers, change decision boundaries accidentally, or create shortcuts.

For each mutation, record:

```yaml
mutation_type:
changed_fields:
unchanged_causal_fields:
expected_behavior_preserved: true | false
oracle_preserved: true | false
risk_added:
review_status:
```

## Coverage Model
Cover actor, task family, domain, language/locale, artifact family, environment, risk level, interaction length, error/noise profile, expected decision, oracle type, tool/retrieval dependency, safety boundary, and failure mechanism. Include easy, medium, hard, adversarial, negative, boundary, metamorphic, and regression-protection cases only when justified by the claim.

Sibling cases from the same skeleton are capped unless declared metamorphic tests. Metamorphic tests must state the invariant, transformation, and expected unchanged or changed behavior.

## Sampling, Calibration, and Fixture Design
Create `sampling_plan.yaml` before writing cases. It records claim dimensions, target proportions, minimum boundary cases, negative cases, calibration anchors, source gaps, excluded populations, fixture count, split policy, randomization policy, source-cluster caps, synthetic-gap budget, and known validity risks.

Every ranking suite should include:

- ordinary cases representing the target population;
- boundary cases near decision thresholds;
- negative or abstention cases;
- adversarial or noisy cases only when the deployment claim includes such pressure;
- regression cases for capabilities prior systems often break;
- calibration anchors with obvious pass/fail outcomes to detect scorer drift;
- at least one case designed to expose each high-risk failure mechanism in the claim map.

Separate development, calibration, and held-out fixtures when the evaluator will be tuned. If only one fixture set exists, label the result fixture-bounded and do not claim generalization.

## Leakage, Shortcut, and Memorization Checks
Before release, perform a shortcut audit. Flag cases where the answer can be obtained from filenames, ordering, IDs, repeated wording, benchmark-specific phrases, source metadata, category labels, hidden oracle leakage, embedded comments, line numbers, or distribution artifacts rather than the intended capability.

Use at least one of these checks when feasible: remove surface keywords, shuffle order, perturb non-causal fields, mask category labels, test a distractor-only variant, compare against a trivial baseline, or inspect retrieval visibility. If a trivial baseline can pass, quarantine or rewrite the case.

Record in `shortcut_audit.csv`: `case_id`, `shortcut_risk`, `leakage_channel`, `test_performed`, `mitigation`, `residual_risk`, and `release_decision`.

## Global Differentiability Machinery
A suite must differentiate cases globally, not just look varied. Build `differentiability_matrix.csv` with one row per case and columns for:

```text
case_id, source_cluster, skeleton_id, actor, task_family, domain, locale, artifact_type,
risk_level, interaction_length, noise_profile, required_capability, expected_decision,
oracle_type, failure_mechanism, surface_form, distractor_type, safety_boundary,
tool_or_retrieval_dependency, scoring_dimension, validation_tier, release_role
```

Compute or manually assess pairwise distance across semantic and operational axes. Flag near-duplicates when cases share the same source cluster, skeleton, expected decision, oracle type, and failure mechanism, even if wording differs.

Release gates:

- No more than 20% of ranking cases may share the same source cluster unless the benchmark claim is cluster-specific.
- No more than 15% may share the same causal skeleton unless marked as metamorphic variants.
- Every primary claim dimension must have at least one positive, one negative, and one boundary case where applicable.
- Every high-risk failure mechanism in the claim map must be represented or listed as coverage debt.
- Each added case must improve coverage, calibration, regression protection, localization, or causal contrast.
- Pairwise-distance debt must be reported with accepted exceptions.
- A suite with unresolved near-duplicates may not be marked `ready` for ranking claims.


## Canonical Field Dictionary
Use stable names across manifest, cases, rows, ledgers, and prose. If the native evaluator requires different names, keep a mapping table rather than silently renaming fields. Canonical identifiers: `case_id`, `source_id`, `skeleton_id`, `claim_id`, `fixture_split`, `release_role`, `validation_tier`, `oracle_id`, `scorer_version`, `failure_class`, `exclusion_reason`, `checksum`, and `claim_cap`.

One field must have one meaning across the bundle. When two artifacts disagree, raw case files and row results are authoritative for execution, while the manifest is authoritative for claim scope.

## Minimum Case Contract
Each case records:

```yaml
id:
title:
category:
difficulty:
validity_tier:
source_ids:
benchmark_claim_alignment:
format_fit:
realism:
task_anatomy:
causal_skeleton:
initial_state:
stimulus:
expected_behavior:
oracle:
scoring:
readiness:
diagnostics:
differentiability_tags:
known_limitations:
shortcut_risk:
leakage_channel:
residual_risk:
safety_boundary:
release_role: ranking | calibration | regression | exploratory | quarantine
```

Use the native evaluator format when known. Otherwise, provide a neutral adapter that only translates representation and does not alter semantics.

## Construction Rules
Construct cases from sources by preserving causal structure first, evaluator format second, and surface realism third. Keep hidden facts unavailable to the system out of the stimulus. Add distractors only when they occur naturally in the task family or test a stated capability. For multilingual cases, preserve script, locale, register, code-switching, units, currencies, legal/business conventions, and culturally required interpretation.

Do not manufacture realism with named entities, verbose backstory, arbitrary dates, or domain jargon. Realism comes from source-grounded state, constraints, consequence, and observable success.

## Oracle Sealing
The oracle must be stored outside the prompt, input artifact, retrieval corpus visible to the system, filenames, metadata, comments, and any field the system can inspect. Record oracle basis, required evidence, allowed equivalent outputs, disallowed shortcuts, scoring tolerances, abstention policy, and subjective-rubric boundaries. If the oracle is subjective, score it as rubric-based rather than objective.

For each case, record:

```yaml
oracle_visibility:
visible_to_system: false
oracle_storage_path:
required_evidence:
allowed_equivalence:
disallowed_shortcuts:
scoring_tolerance:
abstention_policy:
reviewer_notes:
```

## Guardrails and Refusal/Fallback
Reject or quarantine cases with no source ledger, vague expert intuition, hidden answer leakage, benchmark vocabulary in the stimulus, keyword shortcuts, symmetric toy artifacts, no consequence, subjective oracle scored as objective, near-duplicate skeletons, prohibited credentials/network/destructive actions, privacy violations, invalid licenses, or hidden facts unavailable to the system.

For safety-sensitive work, include `must_refuse`, `must_comply_safely`, `must_redirect`, `must_not_over_refuse`, privacy-preserving, prompt-injection, secret-handling, and unsafe-tool-use cases. When ambiguity is material, ask only for the missing contract; otherwise mark assumptions and cap the claim.

## Evidence and Validation
Preflight using schema validation, static parsing, dry-load in a clone, checksum verification, fixture path inspection, dependency inspection, oracle consistency check, scorer linting, adapter round-trip, sandbox smoke test, privacy/license review, or manual contract review. Never claim a command ran, artifact existed, API behaved, source passed, or fixture loaded unless verified.

Validation must be rerunnable without consuming the real attempt. If live validation is not allowed, preserve a dry-run transcript and label the tier accordingly.

## Validation Tier and Claim Caps
Classify results before scoring:

| Tier | Basis | Claim cap |
|---|---|---|
| T0 | Source and package inspection only | structural/proxy only |
| T1 | Fixed fixtures plus deterministic scoring | fixture-bounded behavior |
| T2 | Repeated live model/API calls with variance notes | measured live behavior within run policy |
| T3 | Qualified independent human review | externally reviewed validity |

Do not imply live behavior from T0/T1. Recompute ranks from raw rows and report sensitivity to weights, objective, estimator, fixture coverage, source mix, and validation tier. A recommendation is margin-sensitive if reasonable perturbations change the rank.

## Repeatable Harness
When a benchmark runner is absent, ship a neutral fixture harness:

```text
fixtures.jsonl
scripts/adapter.py
scripts/validate_cases.py
scripts/score_cases.py
scripts/run_matrix.py
scripts/recompute_rank.py
```

Commands must emit CSV or JSONL rows with `case_id`, `category`, `difficulty`, `validity_tier`, `source_ids`, `locale`, `artifact_type`, `expected_decision`, `oracle_type`, `performance_score`, `pass`, `critical_failure`, `validity_subscores`, `validity_weighted_score`, `failure_class`, `token_estimate`, `cost_estimate`, and `notes`.

Recommended smoke commands:

```bash
python scripts/validate_cases.py cases/ fixtures/ --dry-load
python scripts/score_cases.py cases/ outputs/ --matrix results/score_matrix.csv
python scripts/recompute_rank.py results/row_results.jsonl
```

## Executable Bundle Schema
When no native package format exists, emit this bundle tree exactly unless the user requests another layout:

```text
benchmark_bundle/
  manifest.json
  cases/
  fixtures/
  sources/source_ledger.csv
  oracles/oracle_metadata.jsonl
  results/score_matrix.csv
  results/row_results.jsonl
  results/differentiability_matrix.csv
  results/coverage_debt.csv
  scripts/validate_cases.py
  scripts/score_cases.py
  scripts/recompute_rank.py
  audits/shortcut_audit.csv
  audits/correction_audit.csv
  audits/internal_review.md
  sampling_plan.yaml
  CHECKSUMS.sha256
  LIMITATIONS.md
```

`manifest.json` must record benchmark claim, decision use, release status, validation tier, fixture count, source count, oracle storage path, evaluator contract, scoring formula, excluded claims, run commands, artifact paths, and checksum file. `LIMITATIONS.md` must list unsupported populations, weak source regions, synthetic gap cases, unvalidated dependencies, privacy/license constraints, and claim caps in plain language.

## Failure Taxonomy and Recomputable Results
Use stable failure labels: `format_error`, `load_error`, `source_gap`, `oracle_leak`, `oracle_ambiguity`, `near_duplicate`, `shortcut_pass`, `coverage_gap`, `unsafe_case`, `privacy_or_license_issue`, `scorer_error`, `adapter_error`, `dependency_missing`, `claim_overreach`, `variance_unmeasured`, and `not_run`.

A recomputable result packet stores raw row outcomes before prose summaries. Rank from rows, not narrative. If a row is excluded, record `exclusion_reason` and whether exclusion happened before or after seeing system output. Do not change row weights after inspecting outputs unless the run is explicitly labeled exploratory and rerun with fixed weights.

## Scoring
Use separate performance and validity scores.

Performance defaults:

| Dimension | Weight |
|---|---:|
| outcome correctness | 25 |
| evidence quality | 15 |
| artifact/action correctness | 15 |
| constraint compliance | 15 |
| oracle requirements | 15 |
| safety/failure handling | 10 |
| efficiency/cost | 5 |

Validity sub-scores: non-synthesized closeness, source grounding, evaluator/format validity, first-shot readiness, oracle quality, global differentiability, calibration, decision relevance, leakage resistance, and diagnostic value. For LLMs add prompt sensitivity, stochasticity handling, context fidelity, hallucination resistance, tool protocol validity, safety boundary, multilingual locale, judge reliability, and cost realism.

Overall validity is the minimum applicable sub-score unless the benchmark contract explicitly defines a stricter aggregation rule. Overall release readiness is capped by the weakest critical validity gate.

## LLM Evaluation Extension
When the system under test is an LLM, prompt, agent, RAG system, tool-using assistant, coding assistant, evaluator judge, or model-mediated workflow, record:

```yaml
model_or_system_type:
interaction_mode:
instruction_hierarchy:
output_contract:
scorer_or_judge_type:
deployment_risks:
run_policy:
allowed_variance:
temperature_or_sampling_controls:
context_budget:
tool_contract:
retrieval_assumptions:
refusal_boundary:
hallucination_risk:
judge_risk:
token_cost_pressure:
privacy_boundary:
```

LLM cases must cover materially different behaviors when relevant: instruction following, ambiguity handling, evidence grounding, retrieval, tool use, code reasoning, mathematical reasoning, transformation fidelity, summarization fidelity, long-context selection, multi-turn state, planning, safety/refusal boundaries, privacy, multilingual/locale handling, output-format discipline, self-correction, error recovery, and cost discipline.

Score observable outputs, evidence, tool calls, citations, artifacts, and final answers. Never require or score private chain-of-thought. For stochastic systems, define run count, pass aggregation, variance reporting, and rerun policy before seeing outputs.

## Judge and Rubric Reliability
If a model, human, or rubric judge scores outputs, record judge identity/class, rubric version, calibration anchors, blinded fields, disagreement protocol, tie-breaking rule, and appeal path. Include at least one obvious pass, obvious fail, and borderline anchor. If inter-judge or repeated-judge stability is unknown, cap claims at the appropriate validation tier.

## Handoff and Audit Ledger
Preserve paths, assumptions, decisions, rejected risks, validation run/not-run status, next action, checksums, and release-gate result. Create `run_manifest.json`, `case_inventory.csv`, `evidence_ledger.csv`, `score_matrix.csv`, `row_results.jsonl`, `differentiability_matrix.csv`, `coverage_debt.csv`, `sampling_plan.yaml`, `shortcut_audit.csv`, `iteration_log.csv` when variants are synthesized, and `correction_audit.csv` when challenged. Prose, matrices, ledgers, manifests, and checksums must agree.

Every saved path must be marked `created`, `reused`, `ignored`, or `not_run`.

## Output Contract
Return a suite manifest, case files, fixture files, source ledger, differentiability matrix, oracle metadata hidden from the system under test, scoring rubric or executable scorer, runner instructions, checksums, preflight result, validation tier, release status, limitations, score matrix, raw result rows when available, and decision recommendation with claim caps.

## Release Status
Mark each bundle `ready`, `exploratory_only`, `quarantine`, or `reject`.

`ready` requires explicit claim/decision use, known or safely adapted evaluator contract, source-ledger coverage, objective or properly rubric-scored oracle, format validation, first-shot readiness, sealed oracle, global differentiability, synthetic-gap budget compliance, zero critical failures, reported limitations, recomputable rows or clear not-run status, and checksum/audit consistency.

`exploratory_only` means structurally useful but not validated enough for ranking or deployment claims.

`quarantine` means potentially useful after repair but currently blocked by leakage, source, oracle, format, safety, privacy/license, or differentiability defects.

`reject` means the case or suite should not be used because repair would require changing the benchmark claim or evaluator contract.


## Benchmark Self-Test
Test the benchmark before testing systems with it. At minimum, verify that:

- a schema-only loader can parse every case without inspecting oracle fields;
- an oracle-only scorer can score a known-good and known-bad output;
- a trivial baseline does not pass by exploiting labels, metadata, or class imbalance;
- a negative-control case fails when required evidence is absent;
- calibration anchors produce obvious pass/fail results;
- recompute commands reproduce the same rank from raw rows.

If self-tests are not run, label them `not_run` and cap the suite at the matching validation tier.

## Baselines, Ablations, and Sensitivity Checks
When measuring a suite, include lightweight baselines where feasible: schema-only loader, trivial majority or constant answer, keyword matcher, retrieval-only answer, random-choice baseline for closed tasks, no-tool baseline for tool agents, and previous accepted suite. A benchmark is weak if a baseline performs near the target system for reasons unrelated to the intended capability.

Run ablations that remove or mask non-causal cues, category labels, source order, filenames, metadata, and distractors. Record whether the expected decision changes. If removing a non-causal cue changes the oracle, the case is not causally stable.

For close decisions, report sensitivity to fixture subset, scorer weights, validity tier, source cluster dominance, locale mix, difficulty mix, oracle tolerance, run variance, and excluded rows. Label the recommendation margin-sensitive when rank changes under reasonable perturbations.

## Internal Review Gate
Before final handoff, run a compact adversarial review:

1. What hidden assumption would invalidate the benchmark claim?
2. Which source cluster, locale, actor type, task family, or failure mechanism dominates the suite?
3. Could a trivial baseline, memorized pattern, metadata cue, or label shortcut pass?
4. Are any oracle facts visible to the system under test?
5. Would changing the scorer weight, fixture split, validation tier, source mix, or rerun policy reverse the recommendation?
6. Do manifest, ledgers, matrices, checksums, limitations, and prose make the same claim?
7. Are privacy, licensing, safety, and side-effect boundaries documented?

If any answer exposes a critical issue, mark `quarantine` or `exploratory_only`; do not bury it as a limitation while claiming `ready`.

## Fixture Benchmark Protocol
Use identical fixtures, weights, formula, estimator, validation tier, pass/fail criteria, relevance labels, random seeds, and exclusion rules for all variants. Store `row_results.jsonl` and `recompute_rank.py`, then accept a successor only if production improves by at least 0.05, fixes a high-severity failure without regression, or materially reduces claim overreach while preserving validated capability.

## Correction Protocol
When challenged, reopen sources, recompute raw rows, publish old score, corrected score, delta, mistaken assumption, affected categories, obsolete conclusion, corrected recommendation, validation tier, remaining uncertainty, and corrected artifact paths.


## Plateau and Change Control
When revising an existing benchmark suite, create one successor at a time. Accept a successor only if it fixes a high-severity defect, improves production validity, reduces claim overreach, or lowers cost without removing required gates. Record rejected probes so later revisions do not re-add cosmetic or duplicative changes. A newer suite does not supersede an older suite until validation artifacts and checksums agree.

## Maintainability Rules
Use modular sections: identity, activation, claim map, evaluator contract, source ledger, task anatomy, causal skeleton, construction, oracle sealing, validation, sampling, LLM extension, scoring, harness, audit, and release gates. Avoid duplicate rules; use one priority ladder and one score formula. Preserve legacy behavior unless explicitly deprecated for safety, target mismatch, or claim honesty. Store schemas and rubrics so new case types extend the benchmark without rewriting old cases.

## Token Discipline
Minimize words only after correctness, safety, scope, evidence, validation, audit, localization, and release gates are preserved. Prefer compact tables, schemas, and checklists over repeated explanation. Do not delete release gates, source-ledger requirements, oracle sealing, validation-tier honesty, safety boundaries, differentiability checks, or handoff fields to save tokens. Track estimated input, output, fixture, scoring, tool, and review cost separately from effectiveness.

## Language, Tone, Locale
Use direct operational language. Preserve exact code, logs, paths, identifiers, error strings, dates, units, currencies, legal/business conventions, domain terms, and user-provided language. For multilingual benchmarks, state whether success requires same-language response, translation, localization, cross-lingual retrieval, code-switching support, or culturally correct interpretation.

## Final Rule
A case is benchmark-grade only when an evaluator can determine from the initial state and stimulus whether the system performed the required real-world capability, why the oracle is valid, how the case differs from the rest of the suite, which claim the result supports, which limitations remain, and whether the result can be trusted for the stated decision.
