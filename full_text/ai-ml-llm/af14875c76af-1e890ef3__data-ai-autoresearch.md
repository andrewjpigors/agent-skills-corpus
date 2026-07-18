---
name: data-ai-autoresearch
description: Design autonomous AI research systems inspired by Karpathy's autoresearch framework. Use when asked to 'set up autoresearch', 'design an autonomous training loop', 'create an AI research experiment', 'build a self-improving model pipeline', 'autonomous model training', 'autoresearch for my problem', or when the user has a problem/challenge that could benefit from autonomous iterative model training with automated evaluation. Also use when asked to 'design evaluation criteria for model training', 'create a training harness', 'set up experiment tracking for ML', or when someone wants an AI agent to autonomously explore model architectures, hyperparameters, or training strategies to solve a specific problem.
license: MIT
metadata:
  author: nexus-agents
  version: "1.1.0"
  domain: data
  triggers: autoresearch, autonomous research, autonomous training, self-improving model, iterative model training, experiment loop, automated ML research, model evaluation harness, training pipeline design, autonomous AI experiments, autoresearch framework, research automation, ML experiment design
  role: expert
  scope: design
  output-format: specification
  related-skills: product-spec-brainstorming, engineering-quality-tdd
---

# Autoresearch System Designer

Designs complete autonomous AI research systems inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) framework. Takes a user's problem or challenge and produces all the components needed to run an autonomous experiment loop: data preparation, model architecture, evaluation harness, training script, and agent instructions — each tailored to the specific domain and success criteria.

## Role Definition

You are a senior AI research engineer with 15+ years of experience in machine learning systems, model architecture design, and automated experimentation. You specialize in translating real-world problems into well-scoped ML training objectives, designing evaluation metrics that faithfully measure progress, and building self-contained experiment harnesses that AI agents can autonomously iterate on. You produce systems where every component — from data pipeline to evaluation harness to agent instructions — is aligned to solve the user's specific problem, not generic boilerplate.

## Autoresearch Framework Overview

The autoresearch pattern is built on a simple but powerful loop:

```
┌─────────────────────────────────────────────────┐
│  AUTONOMOUS EXPERIMENT LOOP                     │
│                                                 │
│  1. Modify training code (model, optimizer,     │
│     hyperparams, architecture)                  │
│  2. Run training for fixed time budget          │
│  3. Evaluate against fixed metric               │
│  4. If improved → keep changes (advance)        │
│     If not → discard changes (revert)           │
│  5. Log results                                 │
│  6. Repeat indefinitely                         │
│                                                 │
│  Key invariants:                                │
│  • Fixed time budget per experiment             │
│  • Fixed evaluation metric and harness          │
│  • Single file modified by the agent            │
│  • All other infrastructure is read-only        │
│  • Results tracked in append-only log           │
└─────────────────────────────────────────────────┘
```

**Three files that matter:**
1. **prepare script** — Fixed data prep, tokenizer, dataloader, evaluation function. Read-only to the agent.
2. **train script** — The single file the agent edits. Contains model, optimizer, and training loop. Everything is fair game.
3. **program file** — Agent instructions. Written by the human. Defines scope, constraints, metrics, and the experiment loop protocol.

**For robust real-world use, add a fourth layer:**
4. **runner and enforcement artifacts** — A single blessed experiment entrypoint (for example `src/[slug]/run_experiment.py`) plus workspace instructions and, when available, hooks. This layer exists to keep the agent on the rails: no side probes, no silent metric checks outside the log, and no ambiguity about how an experiment is launched.

## Core Workflow

### Phase 0: Data Readiness (Pre-Flight)

Before the autonomous loop begins, ensure the data is understood, clean, and feature-complete. This phase is human-guided — the agent does not run autonomously here. Skip this phase only when the data is already well-understood and prepared (e.g., a known benchmark dataset).

Load `references/data-readiness.md` for detailed guidance on each step.

**Step 1 — Exploratory Data Analysis (EDA):**
- Profile the dataset: row count, column types, cardinalities, null rates, basic statistics
- Visualize distributions of key features and the target variable
- Check class balance (for classification) or target distribution (for regression)
- Compute correlation matrix between features and target — flag highly correlated feature pairs
- Identify potential data leakage: features that are proxies for the target or derived from future information
- Examine outliers and decide whether to clip, winsorize, or leave them
- Check that train/validation splits have similar distributions

**Step 2 — Data Cleansing:**
- Document null handling decisions per feature (drop, impute with median/mode/zero, flag-and-impute)
- Handle duplicates: exact duplicates (drop), near-duplicates (investigate)
- Fix data type issues: strings that should be numeric, dates that need encoding, inconsistent categorical labels
- Apply outlier treatment decided in EDA (clip bounds become fixed constants in `src/[slug]/prepare.py`)
- Validate referential integrity across related features (e.g., payments_made ≤ expected_payments)

**Step 2.5 — Synthetic Data Assessment (if needed):**
- Evaluate whether synthetic data generation is needed (class imbalance, insufficient volume, privacy restrictions, missing edge cases)
- Choose appropriate technique: SMOTE/ADASYN for imbalance, CTGAN/SDV for privacy-preserving generation, domain simulation for edge cases, augmentation for robustness
- Validate synthetic data quality: statistical fidelity, privacy preservation, downstream utility
- See `references/data-pipeline.md` Stage 1 for detailed synthetic data guidance

**Step 3 — Domain Feature Engineering (Round 1):**
- Create features that require business/domain knowledge and lock them into `src/[slug]/prepare.py`
- These are features the autonomous agent should NOT experiment with — they represent ground-truth domain logic
- See the Feature Engineering Split section below for what belongs here vs. in `src/[slug]/train.py`

**Step 4 — Data Quality Gates:**
- Minimum completeness: no feature used in training has > 5% nulls after cleansing (or document why)
- Class balance assessment: if imbalance ratio > 10:1, document the strategy (metric choice, class weighting, oversampling)
- Train/val distribution check: KS test or visual comparison on key features — flag drift > 0.1
- Feature-target leakage scan: no feature has > 0.95 AUC with the target on its own (unless it's a known strong signal)

**Produce:** A data readiness report summarizing EDA findings, cleansing decisions, engineered features, and quality gate results. This report informs the design of `src/[slug]/prepare.py`.

### Phase 1: Problem Decomposition

Interview the user to understand their problem deeply before designing any component.

**Gather:**
- What problem are you trying to solve? (classification, generation, regression, ranking, etc.)
- What data do you have or can obtain? (format, size, quality, labels)
- What does "success" look like? (the real-world outcome, not the ML metric — we derive the metric)
- What compute is available? (GPU type, count, memory, time budget)
- Are there existing baselines or known approaches?
- What constraints exist? (latency, model size, inference cost, regulatory)

**Produce:** A problem brief — one page covering domain, objective, data profile, compute envelope, and success criteria.

**Note:** Phase 0 and Phase 1 can run in either order or in parallel. If you already have the data, start with Phase 0 while scoping the problem. If you're starting from scratch, define the problem first, then acquire and assess the data.

### Phase 2: Evaluation Design

The evaluation metric and harness are the most critical components. A bad metric means autonomous exploration optimizes for the wrong thing. Load `references/evaluation-design.md` for detailed guidance.

**Design decisions:**
- **Primary metric**: A single scalar that the agent optimizes (lower or higher is better). Must be vocab-size-independent and architecture-independent so changes are fairly compared.
- **Secondary metrics**: Tracked but not optimized (e.g., peak VRAM, inference latency, parameter count).
- **Evaluation data**: Held-out validation set, fixed across all experiments.
- **Evaluation function**: Deterministic, fast, and included in the prepare script (read-only to the agent).

**Validation:** The metric must correlate with the user's real-world success criteria. Walk through concrete scenarios: "If the agent achieves metric X, does that mean the real problem is better solved?"

### Phase 3: Data Pipeline & Infrastructure

Design the complete data pipeline — from acquisition and understanding through preparation and EDA to the fixed `src/[slug]/prepare.py` implementation. Incorporate the cleansing decisions and domain features from Phase 0.

Load `references/data-pipeline.md` for comprehensive pipeline guidance covering all four stages.

**Pipeline Stages:**
- **Stage 1 — Data Acquisition & Understanding**: Source identification, collection scripts, synthetic data generation (when needed), schema review, data dictionary, volume assessment
- **Stage 2 — Data Preparation**: Data wrangling (reshape, merge, pivot), cleaning (nulls, outliers, types, duplicates), feature engineering (domain + derived), data integration (multi-source reconciliation)
- **Stage 3 — Exploratory Data Analysis**: Statistical profiling, visualization generation (distributions, relationships, temporal, anomalies), pattern and correlation discovery, hypothesis testing to validate assumptions
- **Stage 4 — Pipeline Implementation**: Translate all decisions from Stages 1–3 into the fixed `src/[slug]/prepare.py` script — constants, acquisition caching, preprocessing transforms, dataloader, evaluation harness

**Design principle:** Everything that must remain constant across experiments lives here. The agent cannot modify this file. If something should be experimentable, it belongs in the train script instead.

#### Feature Engineering Split

Feature engineering spans two files. The split is deliberate — it keeps domain knowledge fixed while letting the agent explore learned representations.

**`src/[slug]/prepare.py` (fixed, read-only) — Domain features:**
- Features requiring business logic or domain expertise (e.g., "policy in surrender period" flag, affordability quartile, tenure bucket)
- Explicit interaction terms with known actuarial/domain meaning (e.g., premium_to_income_ratio)
- Cleaning transforms: null imputation strategy, outlier clip bounds, categorical encoding scheme
- Calendar/time-derived features (day of week, month, seasonality flags)
- Aggregation features from transaction history (rolling averages, cumulative counts)

These are locked because changing them between experiments breaks comparability — you can't tell if a metric improvement came from the model or the data.

**`src/[slug]/train.py` (agent-modifiable) — Learned features:**
- Learned embeddings for categorical features (instead of label encoding)
- Cross-feature attention or interaction layers (letting the model discover non-obvious combinations)
- Polynomial or higher-order feature layers within the network
- Feature selection via learned gating or attention weights
- Input normalization variants (layer norm, batch norm on input, learned scaling)

These are safe for the agent to experiment with because they don't change the raw input data — they change how the model interprets it.

**Rule of thumb:** If creating the feature requires knowing something about the business domain that isn't in the data itself, it belongs in `src/[slug]/prepare.py`. If it's a mathematical transform the model could theoretically learn, it belongs in `src/[slug]/train.py`.

### Phase 4: Training Script Design

Design the modifiable train script — the single file the agent iterates on. Start by choosing the model type (machine learning, deep learning, or hybrid) based on data characteristics, then select a specific architecture.

Load `references/model-selection.md` for the model type decision framework, traditional ML models, deep learning architecture families, and guidance on connecting preparation decisions to the training baseline.

**Model type decision:**
- **Machine learning** (XGBoost, LightGBM, Random Forest, etc.): Best for tabular data, small datasets, interpretability requirements, fast iteration
- **Deep learning** (Transformers, Mamba, CNNs, etc.): Best for unstructured data, large datasets, representation learning, SOTA performance
- **Hybrid/ensemble**: Best for mixed data types, stacking ML+DL outputs, phased approach (ML baseline → DL improvement)

**Starting point (baseline):**
- A model type and architecture justified by data characteristics and EDA findings
- Standard optimizer configuration
- Default hyperparameters that produce a working (not optimal) baseline
- Training loop with proper logging

**What must be in scope for agent modification:**
- Model architecture (layers, dimensions, attention patterns, activation functions)
- Optimizer choice and configuration
- Learning rate schedule
- Batch size and gradient accumulation
- Regularization (dropout, weight decay, etc.)
- Any problem-specific knobs

**What must be fixed (lives in prepare script):**
- Time budget
- Evaluation function
- Data loading
- Validation split

### Phase 5: Agent Program Design

Design the program file — the instructions that guide the autonomous agent.

Load `references/program-design.md` for agent instruction patterns.

**Structure:**
1. **Setup protocol**: How the agent initializes a new experiment run (branching, reading context, establishing baseline)
2. **Scope definition**: What the agent CAN and CANNOT modify
3. **Experiment loop**: The step-by-step protocol for each iteration (modify → train → evaluate → keep/discard → log)
4. **Logging format**: Results tracking schema (structured, append-only)
5. **Decision criteria**: When to keep vs. discard, how to weigh improvement against complexity
6. **Autonomy rules**: The agent runs indefinitely without asking permission to continue

**Key design considerations:**
- The simplicity criterion: improvements that add ugly complexity are not worth it; simplifications that maintain performance are valuable
- Crash handling: fix trivial bugs, skip fundamentally broken ideas
- Never-stop directive: the agent continues autonomously until interrupted
- Circuit breakers: automated detection of pathological states (consecutive crashes, plateau, resource exhaustion)
- Convergence detection: statistical plateau detection with escalation strategies

### Phase 5.5: Process Consistency Enforcement

Design the enforcement layer that makes the program file operational instead of merely aspirational.

**Required outputs:**
- **Blessed runner**: a single experiment command such as `python -m [slug].run_experiment --description "..."` that becomes the only supported path for logged runs
- **Direct-run guard**: `train.py` should require an explicit override flag or environment variable for manual debugging so autonomous work does not casually bypass the runner
- **Workspace instructions**: a `copilot-instructions.md` or `AGENTS.md` file that says the process itself is part of the project and prohibits side probes during autoresearch
- **File-specific instructions**: an `.instructions.md` file scoped to `src/[slug]/train.py` that reinforces one-change-per-experiment and runner-only execution
- **Optional hooks**: if the environment supports hooks, provide a blocking rule for known bad patterns such as direct `train.py` runs or inline Python probes during autoresearch

**What the runner must do:**
- Launch exactly one logged experiment
- Write or overwrite `output/[slug]/run.log`
- Append one row to `output/[slug]/results.jsonl` on success and on crash
- Stamp provenance fields such as runner name, git commit, branch, timestamp, and train-script hash when practical
- Refresh monitoring artifacts after each run

**Design principle:** skill text and markdown instructions are advisory. If you want a process that stays consistent, you must create artifacts that make the correct path the default and the incorrect path inconvenient or blocked.

### Phase 6: Observability & Monitoring Setup

Design the monitoring infrastructure that makes the autonomous loop transparent and manageable. Without observability, you cannot tell if the loop is making progress, wasting compute, or failing silently.

Load `references/observability.md` for detailed guidance on all monitoring, documentation, and tracking systems.

**Components:**
- **Experiment visualization**: Script to generate metric progression charts, keep/crash rates, and resource trends from `results.jsonl`
- **Circuit breakers**: Automated thresholds for consecutive crashes, metric plateau, and resource exhaustion — built into the experiment loop
- **Convergence detection**: Statistical plateau detection with escalation stages (widen search → architecture pivot → simplification → back to basics)
- **Checkpoint management**: Strategy for saving best model, current model, and periodic snapshots with disk budget
- **Resource monitoring**: GPU utilization, throughput, disk usage tracked per experiment
- **Cost tracking**: Estimated compute cost per experiment and cumulative spend with budget guardrails

**Documentation artifacts created during preparation:**
- **Assumptions register** (`output/[slug]/assumptions-register.md`) — Assumptions from every phase, with risk-if-wrong and validation status
- **Decision log** (`output/[slug]/decision-log.md`) — Why each major decision was made, not just what was decided
- **Data manifest** (`output/[slug]/data-manifest.md`) — Data sources, checksums, pull dates, transform lineage
- **Environment manifest** (`output/[slug]/environment-manifest.json`) — Python version, CUDA version, GPU model, package versions, seeds

**Documentation artifacts maintained during the loop:**
- **Experiment journal** (`output/[slug]/experiment-journal.md`) — Qualitative observations, pattern recognition, strategy shifts at natural breakpoints

**Fairness (when applicable):**
- If the model affects people, identify protected attributes, check proxy features, measure baseline fairness, and track fairness metrics as secondary metrics throughout the loop

### Phase 7: Integration & Validation

Assemble all components and verify the system works end-to-end before handing it to an autonomous agent.

**Validation checklist:**
- [ ] prepare script runs without errors and produces training data + tokenizer
- [ ] train script runs within the time budget and produces the primary metric
- [ ] blessed runner executes one complete logged experiment end-to-end
- [ ] direct invocation of `train.py` is blocked or clearly marked as manual-debug-only
- [ ] Evaluation function is deterministic (same model → same score every time)
- [ ] Baseline result is recorded
- [ ] Program file has clear scope boundaries (what's modifiable vs. read-only)
- [ ] Workspace instructions or equivalent customization file exists and points to the blessed runner
- [ ] Results logging format is defined and the first row (baseline) is recorded
- [ ] Git branching strategy is documented
- [ ] The agent can run one complete loop: modify → train → evaluate → log
- [ ] Circuit breakers are configured with appropriate thresholds
- [ ] Checkpoint strategy is in place and disk budget is estimated
- [ ] Environment manifest is generated
- [ ] Data manifest with checksums is recorded
- [ ] Assumptions register has entries from all preparation phases
- [ ] Decision log has entries for all major design choices
- [ ] Visualization script runs and produces charts from results.jsonl
- [ ] Fairness metrics are configured (if applicable)

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|| Data Readiness | `references/data-readiness.md` | Running Phase 0 — EDA, cleansing, domain feature engineering, quality gates || Evaluation Metrics | `references/evaluation-design.md` | Designing the primary metric and evaluation harness |
| Model Selection | `references/model-selection.md` | Choosing model type (ML, DL, hybrid) and specific architecture for the user's problem |
| Data Pipeline | `references/data-pipeline.md` | Full pipeline design: acquisition, preparation, EDA, and prepare script implementation |
| Agent Program | `references/program-design.md` | Writing the program.md agent instructions |
| Observability & Monitoring | `references/observability.md` | Experiment visualization, circuit breakers, convergence detection, checkpoint management, documentation artifacts |
| File System Layout | `references/file-system-layout.md` | Understanding the three-directory structure (src/, data/, output/) or confirming where any file belongs |

## Constraints

### MUST DO
- Run Phase 0 (Data Readiness) when working with real-world or unfamiliar data — skip only for well-known benchmarks
- Document all data cleansing decisions before locking them into the prepare script — undocumented transforms are invisible tech debt
- Explicitly split feature engineering between `src/[slug]/prepare.py` (domain features) and `src/[slug]/train.py` (learned features) — never leave the boundary ambiguous
- Interview the user about their problem before designing any component — never assume the problem type or data format
- Design the evaluation metric first, before the model or training script — the metric defines what "progress" means
- Validate that the primary metric correlates with the user's real-world success criteria through concrete scenarios
- Make the evaluation function deterministic — same model state must always produce the same metric value
- Keep `src/[slug]/prepare.py` strictly read-only to the agent — it is the fixed ground truth
- Confine all agent-modifiable code to `src/[slug]/train.py`
- Generate a single blessed experiment command and make the program file refer only to that command
- Create an execution wrapper that logs run metadata, captures crashes, and refreshes monitoring artifacts
- Emit workspace-level instructions or equivalent customization that explicitly forbids side probes and points the agent to the blessed runner
- Include a simplicity criterion in the program file — complexity costs must be weighed against metric gains
- Set a fixed time budget per experiment so results are comparable regardless of what the agent changes
- Design the baseline to be functional but not optimized — it should leave room for the agent to improve
- Include crash handling guidance in the program file — fix trivial bugs, log and skip fundamental failures
- Configure circuit breakers with explicit thresholds for consecutive crashes, metric plateau, and resource exhaustion — the loop must be able to self-diagnose pathological states
- Generate an environment manifest before the first experiment — reproducibility requires exact environment specifications
- Record data provenance with checksums for every data source — if the data changes, all prior experiments may be invalid
- Maintain an assumptions register starting from Phase 0 — undocumented assumptions are invisible risks
- Maintain a decision log capturing rationale (not just outcomes) for every major design choice
- Include a checkpoint management strategy — save best model, current model, and periodic snapshots with disk budgets
- Design a visualization script for results.jsonl — data that is logged but never visualized is data that is ignored
- Stamp each logged result with enough provenance to audit how the run was launched and which code produced it, when practical
- Evaluate fairness metrics for models that affect people — identify protected attributes, measure demographic parity or equalized odds as secondary metrics

### MUST NOT DO
- Let the user skip evaluation design — a missing or poorly-designed metric makes the entire system useless
- Allow the agent to modify the evaluation function or data pipeline — this breaks experiment comparability
- Design metrics that depend on model vocabulary size or architecture details — metrics must be architecture-independent
- Create a program file without explicit scope boundaries — ambiguity about what's modifiable leads to the agent breaking infrastructure
- Omit the never-stop directive — the agent must run autonomously without asking for human confirmation
- Use subjective or human-judged metrics as the primary optimization target — the metric must be automatically computable
- Skip the baseline run — every experiment run must be compared against an established baseline
- Design experiments without a results logging schema — untracked experiments are wasted compute
- Tell the agent to use ad hoc shell probes, inline Python snippets, or off-log metric checks to choose ideas during autoresearch
- Bundle multiple problems into one autoresearch system — each system optimizes for exactly one metric
- Hardcode hyperparameters in `src/[slug]/prepare.py` that should be experimentable — anything the agent should tune belongs in `src/[slug]/train.py`
- Let the agent modify data cleansing logic or domain feature definitions — these are fixed decisions from Phase 0
- Skip EDA and data quality gates when working with real-world data — garbage in, garbage out applies double in an autonomous loop
- Launch the autonomous loop without circuit breakers configured — an unmonitored loop can waste unlimited compute or silently fail
- Omit the assumptions register — assumptions that are not documented cannot be validated or challenged
- Let documentation artifacts go stale — the decision log and assumptions register must be updated as new decisions are made
- Skip the environment manifest — without exact environment specs, results cannot be reproduced
- Rely on the skill text alone to enforce discipline when workspace customizations, wrappers, or hooks can make the correct behavior explicit

## Output Deliverables

When the design is complete, produce:

1. **Problem Brief** — Domain, objective, data profile, compute envelope, success criteria
2. **Data Readiness Report** — EDA findings, cleansing decisions, domain features engineered, quality gate results (skip for benchmark datasets)
3. **Evaluation Specification** — Primary metric definition, secondary metrics, evaluation function pseudocode, validation data strategy
4. **Prepare Script** (`src/[slug]/prepare.py`) — Complete data pipeline, cleansing transforms, domain features, dataloader, evaluation harness, and fixed constants
5. **Training Script** (`src/[slug]/train.py`) — Baseline model architecture, optimizer, training loop with all experimentable knobs clearly marked
6. **Experiment Runner** (`src/[slug]/run_experiment.py`) — The blessed entrypoint that executes exactly one experiment, writes `run.log`, logs results, records provenance, and handles crashes
7. **Agent Program** (`src/[slug]/program.md`) — Full agent instructions: setup protocol, scope, experiment loop, logging format, decision criteria, autonomy rules
8. **Workspace Instructions** (`.github/copilot-instructions.md` or `AGENTS.md`) — Always-on repository guidance that states the process, the blessed runner, and the no-side-probe rule
9. **File-Specific Process Instructions** (`.github/instructions/autoresearch-process.instructions.md`) — Targeted guidance for `train.py` work so the agent follows one-change-per-run discipline
10. **Results Schema** — Column definitions for experiment tracking (commit, metric, resource usage, status, description, provenance)
11. **Quick Start Guide** — Step-by-step instructions to initialize and launch the autonomous research loop
12. **Assumptions Register** (`output/[slug]/assumptions-register.md`) — Documented assumptions, risk-if-wrong, validation status
13. **Decision Log** (`output/[slug]/decision-log.md`) — Rationale for every major design decision across all phases
14. **Data Manifest** (`output/[slug]/data-manifest.md`) — Data sources, checksums, provenance, transform lineage
15. **Environment Manifest** (`output/[slug]/environment-manifest.json`) — Full reproducibility specification
16. **Visualization Script** (`src/[slug]/visualize_results.py`) — Generates monitoring charts from results.jsonl

### Output File Structure

See `references/file-system-layout.md` for the full directory structure and rationale.

## Knowledge Reference

autoresearch, nanochat, autonomous ML research, experiment tracking, evaluation harness, bits per byte, validation loss, model architecture search, hyperparameter optimization, neural architecture search, PyTorch, training loop, gradient accumulation, learning rate scheduling, Muon optimizer, AdamW, Lion optimizer, mixed precision training, Flash Attention, BPE tokenization, experiment reproducibility, ablation studies, git-based experiment branching, wall-clock time budget, self-improving systems, Transformer, Mamba, Mamba-2, state space models, S4, Hyena, RWKV, xLSTM, RetNet, Jamba, Griffin, Mixture of Experts, MoE, Diffusion Transformer, DiT, latent diffusion, flow matching, VAE, GAN, ConvNeXt, EfficientNet, Vision Transformer, ViT, PatchTST, temporal CNN, WaveNet, Graph Neural Networks, GCN, GAT, GraphSAGE, equivariant GNN, KAN, Kolmogorov-Arnold Networks, FT-Transformer, TabNet, linear attention, sparse attention, sliding window attention, RoPE, ALiBi, exploratory data analysis, EDA, data profiling, data cleansing, data quality, feature engineering, domain features, learned features, data readiness, class imbalance, outlier treatment, null imputation, data leakage detection, train-validation distribution check, feature-target correlation, data acquisition, synthetic data generation, SMOTE, ADASYN, CTGAN, SDV, data wrangling, data integration, entity resolution, data preparation, hypothesis testing, statistical testing, Mann-Whitney U, Kolmogorov-Smirnov, chi-squared test, mutual information, visualization, correlation heatmap, distribution analysis, anomaly detection, isolation forest, DBSCAN, machine learning, XGBoost, LightGBM, CatBoost, Random Forest, logistic regression, ridge regression, support vector machine, SVM, KNN, naive Bayes, ensemble methods, stacking, bagging, boosting, gradient boosted trees, decision tree, hybrid models, model type selection, training foundation, baseline design, observability, monitoring, circuit breakers, convergence detection, plateau detection, checkpoint management, experiment journal, decision log, assumptions register, data lineage, data provenance, data manifest, environment manifest, reproducibility, cost tracking, compute budget, fairness metrics, demographic parity, equalized odds, disparate impact, bias detection, experiment visualization, metric progression, TensorBoard, Weights and Biases, MLflow, resource monitoring, GPU utilization, ARIMA, SARIMA, Prophet, exponential smoothing, ETS, VAR, N-BEATS, N-HiTS, TFT, Temporal Fusion Transformer, TimesNet, TSMixer, Informer, Autoformer, iTransformer, DeepAR, time series forecasting
