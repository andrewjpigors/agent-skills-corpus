---
name: human-inspired-family-python
description: Deep project operating contract for working directly inside the Human-Inspired Family Python repository (the 05-Human-Inspired-Family_Python_v0.1 project root). Use whenever a task modifies, reviews, runs, validates, documents, benchmarks, tunes, packages, audits, cleans, or explains this project: optimizer work (the 24 runnable ids gsk, odo, sns, sgo-social, toa, eboa, dpo, moa-mother, saro, tlbo, hlo, gtoa, spbo, bso, hms, seeker-oa, lca, ema, pro, qsa, ca, ica, po, fbio), CEC benchmark campaigns (sphere, cec2011, cec2013, cec2013lsgo, cec2017, cec2020), the canonical runner and parallel-backend behavior, reference-matching RNG streams, byte-format result parity, documentation generation with its themed docs/ tree and HTML twins, reproducibility evidence, release polish, and the review-prompt suite.
---

# Human-Inspired Family Python — Operating Contract

This is the agent operating contract for the Human-Inspired Family Python
project. Treat the repository as production research software backing a PhD on
human-behavior-inspired metaheuristics. Preserve runnable behavior,
documentation parity,
reproducibility evidence, result schemas, console output format, and any user
work already present. When in doubt, make the narrowest safe change and keep the
gates green.

## 1. What This Project Is

The repository implements the `human_inspired_family` package for core
human-behavior-inspired metaheuristic algorithms. GSK is one anchor algorithm,
not the package boundary. The implemented optimizers are the canonical GSK
baseline plus 23 human-behavior-inspired optimizers, in pure Python, plus a
self-contained Python port of several **CEC benchmark suites**.
It exists to run reproducible optimizer campaigns, to reproduce published
reference tables bit-for-bit from an external reference implementation, and to
produce paper-grade statistical comparisons.

- **Runnable optimizers (24):** `gsk` plus 23 human-behavior-inspired
  optimizers — `odo`, `sns`, `sgo-social`, `toa`, `eboa`, `dpo`, `moa-mother`,
  `saro`, `tlbo`, `hlo`, `gtoa`, `spbo`, `bso`, `hms`, `seeker-oa`, `lca`,
  `ema`, `pro`, `qsa`, `ca`, `ica`, `po`, `fbio`. The canonical registry is
  `OPTIMIZER_IDS` in `src/human_inspired_family/optimizers/__init__.py`
  (dispatch: `OPTIMIZER_FUNCTIONS` in `runners/run_experiment.py`); run
  `hif-list --optimizers` for the live list.
  - `gsk` is the canonical baseline and the committed reference comparator.
  - The 23 human-behavior-inspired optimizers live under
    `src/human_inspired_family/optimizers/human_behavior/<category>/` (categories:
    cognitive, competition, economic, learning, political, professional, social)
    and are specified per optimizer in `docs/human_behavior/algorithms/`.
  - **Historical note:** earlier releases also shipped six GSK variants
    (`agsk`, `apgsk`, `fdb-agsk`, `atmals-gsk`, `egsk`, `ism-gsk`). They were
    removed in the P32 cleanup (removal record:
    `data/project_inventory/p32_variant_removal_inventory.csv`); the removed
    code, tests, configs, docs, and reference evidence are archived at the git
    tag `pre-p32-gsk-variant-removal`. Do not recreate them and do not
    reference them as runnable.
- **Suites (6):** `sphere`, `cec2011`, `cec2013`, `cec2013lsgo`, `cec2017`,
  `cec2020`. The CEC2017 **scored** set excludes F2 (functions F1, F3-F30)
  across D=10/30/50/100; the statistical loaders drop F2 accordingly.
- **Package:** `human_inspired_family` under `src/` (src-layout; the legacy
  `gsk_family` import shim has been **removed** — all code imports
  `human_inspired_family`, and the deprecated `gsk-*` console aliases still
  resolve to the `human_inspired_family` CLIs); the distribution name is
  `human-inspired-family`; `requires-python` is
  `>=3.10,<3.14` (`pyproject.toml`); the installed/running interpreter is
  CPython 3.10.
- **Runtime deps:** numpy, scipy, pandas, matplotlib, PyYAML, numba (see
  `pyproject.toml` / `requirements.txt` for pinned ranges).
- **Statistical tooling:** the `src/human_inspired_family/analysis/` suite (driven
  by the `hif-stats` console script / `src/human_inspired_family/cli/stats.py`). See §6.

## 2. Absolute Workspace Contract

Work **directly inside** the repository root — the
`05-Human-Inspired-Family_Python_v0.1` project folder.

Hard workspace rules:

- Do **not** create a separate agent project folder, worktree copy, or `.claude/`
  directory for this repo. This root is the shared working folder.
- Do **not** mirror the repository into a generated agent-only workspace or a
  nested temporary tree.
- Do **not** write generated experiment output into imported reference evidence
  (`benchmarks/cec_reference_results/`).
- Do **not** revert user changes unless explicitly asked.
- Do **not** delete retained evidence under `results/` unless explicitly asked.
- Agent (subagent) Bash calls reset the working directory between calls; always
  use **absolute paths** or `cd` into the root first.

## 3. Repository Layout

### 3.1 Root files

The project root holds four Markdown **operating** files plus the six-file
**governance** set — **ten root Markdown files** in total (do not add further
root guides or collapse these without an explicit request):

Operating files:

- `README.md` — landing page and command overview.
- `SKILL.md` — this operating contract (stays at the root).
- `runbook.md` — concise copy-paste command sheet (install, every suite, smoke,
  51-run sweeps, targeted runs, seed-policy reproduction, slow/crashing
  fallbacks). Keep it in sync with the runner contract below.
- `TUNING_PLAYBOOK.md` — the codebase-agnostic acceleration manual distilled
  from the 2026-07 four-round optimization campaign (added 2026-07-17;
  evidence record in `docs/development/OPTIMIZER_PERFORMANCE_AUDIT.md`).

Governance / standards files (authored on request; the authoritative rules):

- [`PROJECT_RULES.md`](PROJECT_RULES.md) — the project "constitution" (workspace,
  evidence integrity, reproducibility, version-control policy, the
  green-gates rule). The rules hub linking the rest.
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — package map, layering, data flow, the
  RNG/seed and results architecture.
- [`DESIGN_GUIDE.md`](DESIGN_GUIDE.md) — design principles + how to extend
  (add an optimizer/suite/CLI, the adapter pattern, the analysis layer).
- [`BENCHMARK_RULES.md`](BENCHMARK_RULES.md) — suite/experiment protocol (F2
  exclusion, dims, runs, budgets, CEC2011 per-dimension bounds, RNG/seed regime).
- [`CODING_STANDARD.md`](CODING_STANDARD.md) — code conventions enforced by the
  gates (ruff, the docstring gate + vendored exemptions, tests, docs-as-code).
- [`PERFORMANCE_RULES.md`](PERFORMANCE_RULES.md) — Numba, thread pinning,
  the parallel backend, workers, memory, incremental writes.

Relocated large specifications (moved out of the root into `docs/` for a cleaner
tree — no longer root files):

- `docs/development/IMPLEMENTATION_PLAN.md` — PART I, the end-game roadmap to
  the Q1 submission (main manuscript + supplementary), atop the preserved
  PART II V5 implementation plan.
- `docs/research/applied_specification.md` — the applied specification of the
  human-behavior metaheuristics scope (the "applied-spec").

The Phase 0 and rename reports (`PHASE0_*.md`, `RENAME_MIGRATION_LOG.md`) also
live under `docs/development/`, not at the root.

Other root files: `run.py`, `pyproject.toml`, `requirements.txt`,
`requirements-dev.txt`, `MANIFEST.in`, `CITATION.cff`, `.gitignore`.

> The deep-review prompts are **no longer at the root**. They live under
> `docs/prompt/` (see §3.4). Never reference them at root paths.

### 3.2 Source package `src/human_inspired_family/`

(The legacy `src/gsk_family/` import shim has been **removed**; all code imports
`human_inspired_family`. The deprecated `gsk-*` console-script aliases in
`pyproject.toml` remain and still resolve to the `human_inspired_family` CLIs.)

- `cli/` — console entry points (one `main()` per module): `run.py`, `list.py`,
  `validate.py`, `stats.py`, `analyze.py`. `stats.py` backs the `hif-stats`
  console script and builds the statistical comparison report; `analyze.py`
  backs the `hif-analyze` campaign-telemetry pipeline.
- `runners/` — campaign machinery: `config.py` (config parsing / arg mapping),
  `run_experiment.py` (execution, backend self-healing), `parallel.py`
  (worker-count policy + scheduling), `output.py` (result writing + byte
  format), `seed_policy.py` (seed derivation; `SEED_POLICIES` tuple),
  `verification.py` (compare / validate), `performance.py` (profiling + runtime
  metadata), `fp_regime.py` (canonical FP-regime guard; the preflight sentinel
  used by `run_suite.sh`).
- `optimizers/` — `__init__.py` (`OPTIMIZER_IDS`, the 24-id registry), the
  canonical `gsk.py` baseline, the shared kernel helpers (`_kernels.py`), and the
  `human_behavior/` package with the 23 HBI optimizers organized by category
  (`cognitive/{bso,hms,seeker_oa}.py`, `competition/{lca,odo}.py`,
  `economic/{ema,pro,qsa}.py`, `learning/{gtoa,hlo,spbo,tlbo}.py`,
  `political/{ca,eboa,ica,po}.py`, `professional/{dpo,fbio,moa_mother,saro}.py`,
  `social/{sgo_social,sns,toa}.py`).
- `common/` — shared building blocks: `rng.py` (`RandomContext`),
  `threefry_rng.py`, `reference_rng.py`, `population.py`, `bounds.py`,
  `donors.py`, `reduction.py`, `numeric_compat.py`.
- `benchmark_adapter/` — `factory.py`, `problem.py`, `protocol.py` (suite
  metadata, problem factory, benchmark interface).
- `analysis/` — the statistical + figure suite that powers `hif-stats`:
  `family_report.py` (top-level report builder; `DEFAULT_PROPOSED`,
  `generate_family_report`), `statistical_tests.py` (Friedman ranks, pairwise
  Wilcoxon signed-rank, Holm correction, Vargha-Delaney A12 / Cliff's delta,
  win/tie/loss, BCa bootstrap), `result_loader.py` (`SUITE_DIMS`, mean-error
  loaders that drop CEC2017 F2), `figures.py` (Nemenyi critical-difference +
  rank PNGs), `latex_tables.py` (LaTeX fragments), `project_policy.py`
  (panel/comparator policy), and the `statistics.py` / `statistical_tests.py`
  primitives.
- `stats.py` — lightweight statistical summary helpers (distinct from the
  `analysis/` report suite).
- `types.py` — shared dataclasses / public data structures.

### 3.3 Non-source directories

- `benchmarks/cec_suite_python/` — active Python benchmark runtime (per-suite
  subpackages `cec2011`, `cec2013`, `cec2013lsgo`, `cec2017`, `cec2020`, each
  with packaged `data.pkl` where applicable). **Active code.**
- `benchmarks/cec_reference_results/` — imported, read-only reference evidence.
  **Immutable** unless the user requests provenance/data maintenance.
- `configs/` — YAML campaign configs + `README.md`:
  `smoke.yml`, `all_optimizers_smoke.yml`, `all_cec2017.yml`,
  `all_optimizers_cec2017_reduced.yml`, `all_cec2011.yml`,
  `golden_validation_smoke.yml`, `performance_campaign_smoke.yml`, and the
  `hbi_*.yml` campaign templates (`hbi_smoke.yml`, `hbi_cec2011.yml`,
  `hbi_cec2013lsgo.yml`, `hbi_cec2017.yml`, `hbi_cec2017_d10.yml`,
  `hbi_cec2017_reduced.yml`). Pass any
  of these to `--config` instead of long flag lists; the per-suite launchers in
  `scripts/` wrap them.
- `scripts/` — launcher/tooling scripts + `README.md` (see §3.5).
- `docs/` — themed Markdown + generated HTML (see §3.4).
- `results/` — generated experiment and audit evidence (git-ignored content
  except retained evidence the user keeps).
- `tests/` — test tiers (see §8).

### 3.4 Documentation tree `docs/`

Markdown is organized into themed subfolders, not a flat `docs/*.md`:

- `docs/index.md`, `docs/LICENSES.md`, `docs/index.html` — landing + licenses.
- `docs/getting-started/` — `user_guide`, `tutorial`, `runbook`,
  `configuration`, `troubleshooting`, `explainer`, `distributed_campaign`.
- `docs/reference/` — `architecture`, `api`, `python_optimizer_interface`,
  `module_dependencies`, `workflows`, `result_schema`, `seed_policy`,
  `benchmark_protocol`, `benchmark_mapping`, `diagrams`, `project_structure`,
  `glossary`, `required_papers`, plus the per-suite C++/Python equivalence reviews
  `cec2011_cpp_python_equivalence_review`, `cec2013_cpp_python_equivalence_review`,
  `cec2013lsgo_cpp_python_equivalence_review`,
  `cec2017_cpp_python_equivalence_review`,
  `cec2020_cpp_python_equivalence_review`.
- `docs/algorithms/` — `gsk` (the canonical GSK algorithm guide). The 23
  HBI optimizers are specified under `docs/human_behavior/algorithms/`.
- `docs/development/` — `developer_guide`, `contributor_guide`,
  `maintenance_guide`, `extension_guide`, `code_reading_guide`, the Phase 0 and
  rename records (`PHASE0_*`, `RENAME_MIGRATION_LOG`), the HBI records
  (`hbi_*`), `IMPLEMENTATION_PLAN.md` (PART I, v1.1, is the authoritative
  end-game roadmap and live status ledger to the Q1 submission — the
  main-manuscript + supplementary pair; planning work points there, not at the
  superseded `PUBLICATION_READINESS.md` tracker; PART II preserves the executed
  V5 plan), the append-only `OPTIMIZER_PERFORMANCE_AUDIT.md` performance
  register and the append-only `DOC_MODERNIZATION_REPORT.md`
  documentation-modernization register (existing sections of both are never
  edited; new evidence is appended), and the archived `DOC_POLISH_REPORT`.
- `docs/research/` — `researcher_handbook`, `reproducibility`, `performance`,
  `validation_report`, `numerical_examples`, `applied_specification` (the
  applied scientific spec; see §3.1), `statistical_analysis` (the
  `hif-stats` / statistical-suite reference page).
- `docs/human_behavior/` — the HBI benchmarking protocol, metrics/telemetry
  notes, and the per-optimizer source-fidelity spec packs
  (`algorithms/<id>_source_spec.md`).
- `docs/prompt/` — the prompt suite (**6 files**, indexed by `docs/prompt/README.md`):
  the three review masters (`ALGORITHM_FIDELITY_REVIEW.md`,
  `CODE_REVIEW_AND_OPTIMIZATION.md`, `DOCUMENTATION_REVIEW.md`), the
  release orchestrator `PUBLICATION_PRODUCTION.md`, and
  `REFERENCE_CODE_PARITY_REVIEW.md` (code-vs-code companion to the fidelity
  pass; reference code is read-only, RNG excluded).
- `docs/html/` — generated static site (see §7).

The root `runbook.md` is the quick copy-paste sheet;
`docs/getting-started/runbook.md` is the in-site page. Keep both consistent when
run commands change.

### 3.5 Scripts `scripts/`

Per-suite campaign launchers (parameters fixed inside `configs/*.yml`):

- `run_all_cec2017.py`, `run_all_cec2011.py`, `run_all_cec2020.py`,
  `run_all_cec2013.py`, `run_all_cec2013lsgo.py`
- `run_human_inspired_family.py` — the canonical generic family launcher.
- `run_full_campaign.sh` — one-command publication driver: runs the three
  campaign suites (CEC2017 -> CEC2011 -> CEC2013-LSGO) sequentially with all 24
  optimizers at `workers: 65%`, then analysis + reference-panel statistics
  (resumable).
- `run_suite.sh` — the full publication pipeline for ONE suite
  (`bash scripts/run_suite.sh cec2017` — or `cec2011` | `cec2013lsgo`):
  preflight (FP-regime sentinel) -> run -> analyze -> stats. Extra CLI args
  forward verbatim to the run step, most usefully `--workers N` to override
  the configs' `workers: 65%` default.
- `run_cec2017.sh`, `run_cec2011.sh`, `run_cec2013lsgo.sh` — thin per-suite
  wrappers over `run_suite.sh` (same arg forwarding).
- `run_shard.sh` — distributed multi-machine runs: the RUN step only, for a
  subset of optimizers of one suite
  (`bash scripts/run_shard.sh <suite> <optimizer-csv>`); analyze + stats run
  centrally after the shards merge
  (see `docs/getting-started/distributed_campaign.md`).

Tooling:

- `thin_raw_logs.py` — post-hoc thinning of existing DG-4 raw logs
  (`*.raw_log.jsonl`) to ~N log-spaced-by-NFE rows for campaigns generated
  before the `telemetry_points` config knob existed (idempotent, atomic,
  updates each summary's `raw_log_hash` provenance).

- `build_docs_html.py` — documentation HTML builder (run by the orchestrator;
  do not invoke it yourself when the orchestrator owns the HTML rebuild).
- `validate_profile_lock.py` — profile-lock guard (`--root .`).
- `plot_convergence_from_curves.py` — convergence-plot helper over curve CSVs.
- `wilcoxon_reference.py` — pairs the port's per-function statistic (mean error
  by default) against the imported reference table per optimizer and dimension,
  runs a Wilcoxon signed-rank test on the paired differences, and reports the
  win/tie/loss split, signed-rank sums, p-value, and significance verdict.

> There are no removed per-phase runner/build scripts and no obsolete staged
> workflow. They were removed. Never reference them.

## 4. Canonical Runner Contract

`run.py` is the canonical source-checkout runner. It prepends `src/` to
`sys.path` and calls `human_inspired_family.cli.run:main`. Installed console
entry points (from `pyproject.toml [project.scripts]`, **6 canonical** plus 5
deprecated `gsk-*` compatibility aliases — `gsk-run`, `gsk-family-run`,
`gsk-list`, `gsk-validate`, `gsk-stats` — that resolve to the same targets):

| Console script | Module target | Purpose |
| --- | --- | --- |
| `hif-run` (alias `human-inspired-family-run`) | `human_inspired_family.cli.run:main` | Run optimizer campaigns. |
| `hif-list` | `human_inspired_family.cli.list:main` | List optimizers / benchmarks / references. |
| `hif-validate` | `human_inspired_family.cli.validate:main` | Validate or compare against reference evidence. |
| `hif-stats` | `human_inspired_family.cli.stats:main` | Build the statistical comparison report. |
| `hif-analyze` | `human_inspired_family.cli.analyze:main` | Derive campaign telemetry analysis (RLSR/GISR/diversity/convergence) into paper-ready CSVs. |

`hif-stats` is documented in `docs/research/statistical_analysis.md`. The
console scripts and `python run.py` accept the same campaign flags; prefer
`python run.py` in a source checkout so `src/` is on `sys.path` without an
install.

Help (always check live flags before scripting a sweep):

```powershell
python run.py --help
```

Tiny direct smoke (seconds):

```powershell
python run.py --root . --optimizer gsk --suite sphere --function 1 --dimension 4 --runs 1 --max-evaluations 80 --overwrite
```

Config-driven smoke:

```powershell
python run.py --root . --config configs/smoke.yml
```

Full CEC2017, all 24 runnable optimizers, 51 runs:

```powershell
python run.py --root . --optimizer gsk,odo,sns,sgo-social,toa,eboa,dpo,moa-mother,saro,tlbo,hlo,gtoa,spbo,bso,hms,seeker-oa,lca,ema,pro,qsa,ca,ica,po,fbio --suite cec2017 --function 1:30 --dimension 10,30,50,100 --runs 51 --parallel --workers 2 --convergence-graphs --overwrite
```

(`--function 1:30` selects the CEC2017 range; the suite excludes F2, so the
**scored** set is F1, F3-F30 = 29 functions, and the statistical loaders drop
F2 from every panel.) `--overwrite` recomputes; omit it to **resume** (finished
cells are skipped). The root `runbook.md` has copy-paste sweeps for every suite
plus the fallbacks.

Common campaign flags (verify against `python run.py --help` before scripting):

- `--root .` — project root anchor (results land under `results/_run_all/`).
- `--optimizer a,b,c` — comma-separated runnable ids.
- `--suite NAME` — one of the 6 suites.
- `--function 1:30` (range) or `--function 1,3,5` (explicit list).
- `--dimension 10,30,50,100` — comma-separated dimensions.
- `--runs N` — independent runs per cell (51 for a full statistical campaign).
- `--max-evaluations N` — explicit budget override (smoke runs only; full
  campaigns use the suite's protocol budget).
- `--parallel` / `--serial`, `--workers N`, `--parallel-backend {process,thread}`.
- `--convergence-graphs` / `--no-convergence-graphs`.
- `--overwrite` (recompute) vs. resume (default, finished cells skipped).
- `--seed-policy {reference,unified,native,derived}` (see §10).
- `--stats` (opt-in live statistical analysis; see below).
- `--benchmark-backend {auto,python}` (both use the Python evaluator) and
  `--benchmark-fp-mode {default,strict}`.

Do / don't for user-facing campaign commands:

- **Do** keep `--parallel --workers 2` visible so the resource choice is explicit
  and safe for shared machines.
- **Do** keep `--convergence-graphs` visible when rendered PNG curves are wanted;
  omit it for CSV-only curve output (median-run curve CSVs are always written).
- **Do** let users raise `--workers N` deliberately after they confirm CPU and
  memory headroom.
- **Don't** use `--serial` except for single-process troubleshooting (slowest
  path, always completes).
- **Don't** use `--parallel-backend thread` for real campaigns (diagnostic only;
  see §5).

The runner also accepts the opt-in `--stats` flag (default **off**, defined in
`src/human_inspired_family/cli/run.py`): when set, it streams the per-dimension
Wilcoxon + Friedman analysis live after each dimension completes (it skips
only the `gsk` baseline; on the native-dimension `cec2011` it emits a single
per-suite rollup panel instead of per-dimension panels). Without `--stats` the
runner prints only the summary plus the
single-baseline mean comparison. `--stats` is for **live feedback during a
run**; it does not write the figure/CSV/LaTeX artifacts.

The standalone `hif-stats` command is the way to produce the publication
artifacts **after** a run: a Friedman panel with mean ranks,
pairwise Wilcoxon signed-rank tests with Holm correction and Vargha-Delaney /
Cliff's-delta effect sizes, Nemenyi critical-difference diagrams, rank charts,
and LaTeX fragments. It reads the proposed optimizer's per-function means from
`results/_run_all/<proposed>/<suite>/summary/` and the comparators from
`benchmarks/cec_reference_results/<suite>/`, writing to
`results/_run_all/_analysis/<suite>/` (see §6.1 and
`docs/research/statistical_analysis.md`).

```powershell
python run.py --root . --optimizer gsk,odo,sns,sgo-social,toa,eboa,dpo,moa-mother,saro,tlbo,hlo,gtoa,spbo,bso,hms,seeker-oa,lca,ema,pro,qsa,ca,ica,po,fbio --suite cec2017 --function 1:30 --dimension 10,30,50,100 --runs 51 --parallel --workers 4 --convergence-graphs --overwrite
```

To generate every artifact the papers need in one command — the three campaign
suites (CEC2017 -> CEC2011 -> CEC2013-LSGO) sequentially with all 24 optimizers
at `workers: 65%`, then analysis + reference-panel statistics — run
`bash scripts/run_full_campaign.sh` (resumable).

## 5. Parallelism, Workers, and Numba

Preserve these defaults (defined in `src/human_inspired_family/runners/parallel.py` and
`run_experiment.py`):

- Parallel execution is **on by default**; the default backend is **`process`**
  (true multi-core, no GIL contention).
- Convergence graph PNG generation is **off by default** for direct CLI runs.
  `--convergence-graphs` / `convergence_graphs: true` enables PNG rendering;
  median-run curve CSVs are still written when PNG graphs are not requested.
- Automatic worker count is intentionally conservative: 2 workers on machines
  with at least two logical CPU cores, otherwise 1 worker
  (`DEFAULT_WORKER_COUNT = 2`). This prevents a copied no-flag command from
  consuming a large shared workstation.
- Automatic CEC2017 composition cells (`F21`-`F30`) on the default `process`
  backend retain an effective memory-safety cap of 8 workers. The normal
  two-worker default is already below this cap, but the cap protects future
  automatic settings. Explicit `--workers N` values are treated as
  user-selected speed/memory overrides.

Override knobs (only when the user asks):

- `--workers N` — choose parallel concurrency intentionally. Start at 2 for
  shared machines; increase to 4, 8, or higher only after checking available CPU
  and memory.
- `--convergence-graphs` / `--no-convergence-graphs` — control rendered PNG
  convergence plots without affecting the required convergence CSV artifacts.
- `--serial` — single-process fallback; slowest path but always completes.
- `--parallel-backend {process,thread}` — **do not use `thread` for real
  campaigns.** Parallel Numba kernels can deadlock when driven from many Python
  threads. `thread` is diagnostic-only.

Backend self-healing (preserve, do not weaken):

- On a worker death (`BrokenProcessPool` from a transient Numba/spawn crash or
  OOM), the `process` backend tears down the pool, rebuilds it, and retries the
  cell up to a bounded number of attempts (currently 3).
- If rebuilds keep failing, that cell finishes on the **serial** backend, then a
  fresh pool is rebuilt for the next cell — so a campaign never hangs and never
  aborts on a transient crash.
- The `process` backend must **never** fall back to `thread` on a crash (that
  many-threads-into-parallel-Numba path can deadlock).

Serial-kernel fast path (preserve):

- Campaign configs opt optimizers into single-row `parallel=False` kernel twins
  via the `serial_kernel_optimizers` config allowlist (default off). The
  per-suite twins live in `benchmarks/cec_suite_python/<suite>/_numba_serial.py`
  and are routed by the suite-local `_kernel_mode.py` thread-local scope.
- The suite-aware `FROZEN_BATCH_KERNEL_OPTIMIZERS` guard in `runners/config.py`
  currently guards an empty tuple (un-freeze 2026-07-17) and is retained in
  reserve — do not remove it.
- Preserve the provenance label (`benchmark_backend: python+serial-kernels`)
  and the documented parity contract: fastmath twins rel <= 3e-15 (max 11 ULP
  on the exhaustive sweep), bit-identical under strict fp; LSGO group-kernel
  twins are bit-identical by construction. Evidence:
  `docs/development/OPTIMIZER_PERFORMANCE_AUDIT.md` (append-only — never edit
  existing sections).

When tuning performance, preserve: seed schedules, RNG draw order where behavior
depends on it, evaluation counts, deterministic result ordering, output schema,
reference-facing behavior, and the self-heal / no-thread-fallback rules. Prefer
profiling evidence over intuition. Rationale lives in
`docs/research/performance.md`.

## 6. Statistical Analysis

The statistical evidence is produced by the `hif-stats` console script (a CLI
over `src/human_inspired_family/analysis/`). It consumes already-generated run
output plus the committed reference tables; it never re-runs an optimizer.

### 6.1 `hif-stats` statistical suite

`hif-stats` (`src/human_inspired_family/cli/stats.py` -> `analysis/family_report.py`)
builds the **comparison panel**: the committed reference comparators
(currently `gsk`) plus the proposed optimizer (`--proposed`).
It produces Friedman ranks, a Nemenyi critical-difference diagram, pairwise
Wilcoxon signed-rank tests with Holm correction, Vargha-Delaney A12 / Cliff's
delta effect sizes, win/tie/loss splits, BCa bootstrap intervals, LaTeX table
fragments, and CD + rank PNGs.

- **Inputs:** the proposed optimizer's per-function means from
  `results/_run_all/<proposed>/<suite>/summary/` (so run that optimizer first)
  and the comparators from `benchmarks/cec_reference_results/<suite>/`.
- **Output:** `results/_run_all/_analysis/<suite>/` (override with `--out`).
- **Key flags:** `--suite` (default `CEC2017`), `--dims` (comma-separated;
  defaults to the suite's standard set via `analysis/result_loader.py`
  `SUITE_DIMS`), `--proposed`, `--results-root`,
  `--reference-root`, `--out`, `--alpha` (default `0.05`), `--no-figures`.
- The loaders **exclude CEC2017 F2** from every panel, matching the scored set.

```powershell
# After a full CEC2017 run of the proposed optimizer, build the panel + figures + LaTeX
hif-stats --suite CEC2017 --dims 10,30,50,100

# CEC2011 panel, tables only (skip matplotlib figures)
hif-stats --suite CEC2011 --no-figures
```

Exit code is `1` when no usable data is found (e.g. the reference base or
reproduced summaries are missing) so the absence of evidence is never silently
reported as a pass.

## 7. Documentation Generation and HTML Twins

After **any** change to Markdown under `docs/`, to docstrings, to README
commands, to navigation, or to the review prompts, rebuild the static site and
**commit the regenerated `docs/html/` twins** alongside the source change:

```powershell
python scripts\build_docs_html.py
```

How it works (for accurate expectations):

- The builder walks **every** `docs/**/*.md` (`rglob("*.md")`) and also renders
  the package API from `src/`.
- Generated HTML page names are **flattened** to `<subfolder>_<page>.html`,
  preserving any literal hyphen in the subfolder name. Examples:
  `docs/reference/seed_policy.md` → `docs/html/reference_seed_policy.html`;
  `docs/algorithms/gsk.md` → `docs/html/algorithms_gsk.html`;
  `docs/prompt/DOCUMENTATION_REVIEW.md` → `docs/html/prompt_DOCUMENTATION_REVIEW.html`.

When adding or moving docs:

- Update `docs/index.md` (and `docs/reference/project_structure.md` if the
  structure changes).
- Update documentation smoke tests if expected file paths change.
- Update any audit scripts that assert required docs.
- Rebuild HTML and commit the twins; run the documentation smoke test (§8).

Keep these synchronized: source Markdown, generated HTML, API pages, search
index, README commands, root `runbook.md` ↔ `docs/getting-started/runbook.md`,
and the `docs/prompt/` review prompts.

## 8. Gates — Keep These Green

Run targeted checks for narrow edits; run the full sequence for broad changes.

**Tests** (do not hard-code the collected test count;
re-check with `python -m pytest --collect-only -q` rather than hard-coding a
number into new docs):

```powershell
python -m pytest -q
```

Test tiers: `tests/unit/` (RNG known-answer tests, statistical primitives,
docstrings, figures, etc.), `tests/smoke/` (CLI smoke, the documentation-command
smoke), `tests/regression/`, `tests/performance/`, plus the top-level
`tests/test_imports.py`. The `slow` marker gates optional scalability checks
(`python -m pytest -m slow` to include them, `-m "not slow"` to skip).

Documentation smoke only (resolves the fixed required-doc list, including this
`SKILL.md` and the required `docs/prompt/` files):

```powershell
python -m pytest tests\smoke\test_documentation_commands.py -q
```

> The required-doc list lives in `tests/smoke/test_documentation_commands.py`.
> If a doc is added or moved, that list (and the matching `docs/html/` twins)
> must stay in sync or this gate fails.

**Lint** (Ruff, scoped to source/tests/scripts; rules `E9`,`F`,
line length 120):

```powershell
python -m ruff check src tests scripts
```

**Docs build** (after any docs/docstring change — commit the `docs/html/`
twins):

```powershell
python scripts\build_docs_html.py
```

**Profile lock** (guards the locked run profile):

```powershell
python scripts\validate_profile_lock.py --root .
```

Optional selected type check (scoped to keep the broad command green under
NumPy 2.x churn):

```powershell
python -m mypy src/human_inspired_family/cli src/human_inspired_family/runners src/human_inspired_family/common
```

Preferred broad verification sequence:

```powershell
python -m pytest -q
python -m ruff check src tests scripts
python scripts\validate_profile_lock.py --root .
python scripts\build_docs_html.py
```

If a gate is too expensive to run, say exactly which command was deferred and
why.

## 9. Results and Byte-Format Parity

Default generated output tree:

```text
results/_run_all/<suite>/<optimizer>/
```

Each campaign writes per-run artifacts, function-level summaries,
optimizer/suite summaries, `seed_schedule.csv`, `environment.json`, an optional
`profile.json`, median-run convergence CSVs, convergence graph PNGs when
enabled, generation/checkpoint logs when enabled, and validation comparison
reports.

**Byte-format parity is intentional and load-bearing** — the console output and
`results/` files are deliberately mirrored to a sibling reference project so the
two can be diffed. Do not "normalize" these away (see
`src/human_inspired_family/runners/output.py`):

- `per_run.csv` best/error fields are formatted `%.10e`.
- Convergence-curve values are formatted `%.16e` (with a matching `log10`
  column).
- Preserve the `environment.json` key order and other documented format
  details.

Generated / derived locations (safe to clear as transient caches during polish,
**except** retained `results/` evidence which needs explicit consent):
`results/`, `docs/html/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`,
`__pycache__/`, `*.pyc`, `*.nbc`, `*.nbi`.

## 10. Seed Policies and the RNG Contract

`run.py`/`hif-run` accept `--seed-policy` with choices
`("reference", "unified", "native", "derived")` (`src/human_inspired_family/runners/seed_policy.py`).

- **`unified`** — default. Matches reference means within statistical noise. The
  seed is the linear `get_cec_seed` modular formula over `(base, dim, func, run)`
  only — **optimizer-independent**, shared across the family; it is **not**
  hashed.
- **`reference`** — reproduces the published tables bit-for-bit for GSK (see
  `docs/reference/seed_policy.md`); forces the reference seeding
  and generator label for `gsk` and falls back to the unified formula for the
  other optimizers.
- **`native` / `derived`** — diagnostic variants using the hashed `derive_run_seed`
  derivation (a character-sum over the optimizer/suite names).

`RandomContext` (`src/human_inspired_family/common/rng.py`) supports exactly three
reference-matching generators selected by the `rand_generator` label; `threefry`
is the default and each reproduces its external reference stream bit-for-bit:

- `threefry` → Threefry-4x64-20 (`threefry_rng.py`): key `(0,0,0,0)`, counter
  `((S+2j+1) << 32) | (S+2j)`, four doubles/block via `(word >> 11) * 2^-53`.
- `twister` → MT19937 (`reference_rng.py`): `init_genrand(seed)` seeding,
  `genrand_res53` doubles.
- `seed` → mcg16807 / Park-Miller (`reference_rng.py`):
  `x0 = (seed << 16) mod (2^31 - 2^15)`, then `x <- 16807*x mod (2^31 - 1)`.

RNG rules:

- Matrix draws fill **column-major**; a `(k, m, n)` request is `k` successive
  column-major `(m, n)` draws. Integer draws use `floor(imax*rand) + 1`;
  permutations use `argsort(rand(n))`.
- Do **not** add NumPy bit generators (Philox, PCG64, plain MT19937) as labels.
  Any label outside `{threefry, twister, seed}` must raise "Unsupported RNG
  generator".
- The v5 `state` generator (swb2712) is intentionally absent and must not be
  re-added as a NumPy placeholder.
- Parity is bit-exact for GSK under the reference policy; residual gaps are
  benchmark floating-point only.
- Do not change any generator's seeding, conversion, or draw order without
  re-verifying against reference draws. Known-answer tests live in
  `tests/unit/test_rng.py`. The full derivation is documented in
  `docs/reference/seed_policy.md`.

## 11. Optimizer and Benchmark Rules

Optimizer edits:

- Keep algorithm logic stable unless an algorithmic change is explicitly
  requested. Preserve option names/defaults, the result dataclass structure,
  bounds-repair behavior, population init / fair-start handling, evaluation-budget
  accounting, and local-search behavior/metadata.
- Keep optimizer tests aligned with behavior; update the matching
  algorithm doc (`docs/algorithms/gsk.md` or
  `docs/human_behavior/algorithms/<id>_source_spec.md`) when behavior, options,
  or artifacts change. High-risk changes require targeted tests **and** doc
  updates.

Benchmark edits:

- `benchmarks/cec_suite_python/` is the active runtime tree;
  `benchmarks/cec_reference_results/` is immutable reference evidence.
  Generated results go under `results/`, never under reference evidence.
- Default `benchmark_backend=auto` uses the Python/Numba evaluator. Do not
  bypass the benchmark adapter from inside an optimizer.
- Keep suite metadata consistent across docs, configs, runner defaults, tests,
  and validation code. When changing benchmark behavior, verify function IDs,
  dimensions, native-dimension handling, optima/target errors, max-evaluation
  behavior, excluded/unsupported functions, and that Numba and non-Numba paths
  stay consistent.

## 12. Validation Rules

Validation must be truthful — never report a pass when functions were skipped.

```powershell
hif-list --optimizers --benchmarks --references benchmarks/cec_reference_results
hif-validate --references benchmarks/cec_reference_results
hif-validate --compare results/_run_all/cec2017/gsk benchmarks/cec_reference_results
```

(Source-checkout equivalent: `python -m human_inspired_family.cli.validate --references benchmarks/cec_reference_results`.)

Expectations to preserve: `hif-validate` reports missing references clearly;
all-skipped validation exits **nonzero**; comparisons state how many
generated/reference pairs were checked; reduced validation is labeled as reduced
evidence; full-campaign evidence requires full-campaign commands.

## 13. Terminology and the Forbidden Token

Use Python-first terminology in active code and docs. Prefer: "imported
reference evidence", "external reference source", "reference-compatible",
"source evidence", "seed-policy exception", "Python runtime", "Python benchmark
adapter".

Do **not** imply that the external reference runtime is required for normal
Python execution, that reduced smoke checks prove full-budget equivalence, that
generated results are reference evidence, or that validation passed when all
functions were skipped.

**Forbidden-token rule:** prefer oblique phrasing ("the external reference
implementation / platform") for the upstream numeric-computing platform's
product name (the six-letter tool starting with "M" and ending in "atlab") in
general narrative docs and code — including this file. The literal token is
permitted only where it is technically load-bearing:
`docs/reference/seed_policy.md` (and its generated HTML twin), where the
seed-policy exception documents the reverse-engineered reference streams;
reference-code provenance and parity materials
(`docs/prompt/REFERENCE_CODE_PARITY_REVIEW.md`, its register and per-optimizer
records, and the source spec packs under `docs/human_behavior/algorithms/`);
reference-platform semantics notes in optimizer code and tests; and dated
historical records (PHASE0 reports, fidelity/parity reviews, equivalence
reviews). Do not scrub existing occurrences on those surfaces, and never
rewrite a dated record or append-only register to add or remove the token.

## 14. Editing, Review, and Reporting Protocol

Before editing: inspect the relevant files, check for user changes in the area,
learn local patterns, and pick the narrowest safe change.

During editing: reuse existing helper APIs; prefer structured parsers / project
helpers over ad hoc string handling; keep abstractions conservative; avoid
unrelated refactors; keep comments short; use `# noqa` only for intentional
compatibility or justified unused calculations.

After editing: run targeted tests; rebuild docs and commit the `docs/html/`
twins if docs/docstrings changed; clear transient caches only if polish was in
scope; summarize changed files, the validation commands run, and residual risks.

Reviews: lead with findings ordered by severity; give exact file paths and line
numbers; separate bugs from risks, missing tests, stale docs, and ideas; keep
the summary short; state clearly when nothing is wrong.

The `docs/prompt/` suite (**6 files**, indexed by `docs/prompt/README.md`), and when to reach for each:

- Algorithm fidelity review: `docs/prompt/ALGORITHM_FIDELITY_REVIEW.md` (every optimizer vs its source paper).
- Code review & optimization: `docs/prompt/CODE_REVIEW_AND_OPTIMIZATION.md` (quality, performance, cleanup — no behavior change).
- Documentation review: `docs/prompt/DOCUMENTATION_REVIEW.md` (docstrings, reference docs, HTML site).
- Publication production: `docs/prompt/PUBLICATION_PRODUCTION.md` (the end-to-end release orchestrator).
- Reference-code parity review: `docs/prompt/REFERENCE_CODE_PARITY_REVIEW.md` (each optimizer vs its reference implementation in `reference_code/<id>/`; run after the fidelity pass when reference code is available).

## 15. Quick Reference Card

```powershell
# Discover (canonical console scripts: hif-run/human-inspired-family-run, hif-list, hif-validate, hif-stats, hif-analyze; deprecated gsk-* aliases still work)
python run.py --help
hif-list --optimizers --benchmarks --references benchmarks/cec_reference_results

# Smoke (seconds)
python run.py --root . --optimizer gsk --suite sphere --function 1 --dimension 4 --runs 1 --max-evaluations 80 --overwrite

# Full CEC2017, all 24 runnable optimizers (omit --overwrite to RESUME)
python run.py --root . --optimizer gsk,odo,sns,sgo-social,toa,eboa,dpo,moa-mother,saro,tlbo,hlo,gtoa,spbo,bso,hms,seeker-oa,lca,ema,pro,qsa,ca,ica,po,fbio --suite cec2017 --function 1:30 --dimension 10,30,50,100 --runs 51 --parallel --workers 2 --convergence-graphs --overwrite

# All three campaign suites + analysis + stats in one command (resumable)
bash scripts/run_full_campaign.sh

# Live per-dimension Wilcoxon+Friedman during the run (opt-in; skips gsk baseline)
python run.py --root . --optimizer odo,sns,sgo-social,toa,eboa,dpo,moa-mother,saro,tlbo,hlo,gtoa,spbo,bso,hms,seeker-oa,lca,ema,pro,qsa,ca,ica,po,fbio --suite cec2017 --function 1:30 --dimension 10,30 --runs 51 --parallel --workers 2 --stats

# Statistical comparison artifacts AFTER a run (figures/CSV/LaTeX)
hif-stats --suite CEC2017 --dims 10,30,50,100

# Validate against imported reference evidence
hif-validate --references benchmarks/cec_reference_results
hif-validate --compare results/_run_all/cec2017/gsk benchmarks/cec_reference_results

# Gates
python -m pytest -q
python -m ruff check src tests scripts
python scripts\validate_profile_lock.py --root .
python scripts\build_docs_html.py

# Reproduce published tables bit-for-bit
python run.py <args> --seed-policy reference
```

Expected root Markdown inventory (operating + governance, sorted):

```text
ARCHITECTURE.md
BENCHMARK_RULES.md
CODING_STANDARD.md
DESIGN_GUIDE.md
PERFORMANCE_RULES.md
PROJECT_RULES.md
README.md
SKILL.md
TUNING_PLAYBOOK.md
runbook.md
```
