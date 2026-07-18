---
name: echomill
description: Create a reproduction package from a technical paper, paper URL, DOI, arXiv link, GitHub repo, or uploaded PDF. Use when the user asks to review, audit, score, reproduce, verify, rerun, or generate target outputs from a technical paper. Default to audit/readiness mode unless the user explicitly requests or approves execution.
---

# EchoMill

Create a **reproduction package** for a technical paper.

The package should explain what was checked, what was run, what reproduction
targets were generated, what matched, what failed, and what is still unknown.

Use the term **reproduction package**. Do not use "capsule" in user-facing
project files unless referring to old notes or migration history.

## Read This Skill In This Order

1. Decide whether this skill applies from the YAML `name` and `description`.
2. Read the core honesty rule.
3. Inspect the user input and available files.
4. Select audit mode or execution mode from the user's request.
5. Use the helper scripts for deterministic file creation, validation, setup,
   content extraction, execution, comparison, and scoring.
6. Write or update the required reproduction package files.
7. Summarize the result without overstating what happened.

## Core Honesty Rule

Do not claim that a paper was reproduced unless the relevant reproduction targets were
actually generated and checked.

If execution or comparison is blocked, call the result an **incomplete
reproduction attempt**, not a completed reproduction.

A failed reproduction attempt is useful when the blockers, logs, assumptions,
and missing materials are clearly documented.

## Expected Inputs

The user may provide one or more of these:

- paper URL
- DOI
- arXiv link
- uploaded PDF
- local PDF path
- GitHub repository
- local source directory
- supplementary material link
- dataset link
- model checkpoint link
- partial reproduction instructions

## Mode Selection

Default to **audit mode** unless the user explicitly asks for execution.

Audit mode means readiness review only. It may create a reproduction package,
record sources, download or copy paper/code/data materials, extract paper text,
render paper pages, identify targets, detect dependencies, write a draft
`REPRODUCTION_RECIPE.json`, validate the recipe, and write readiness scores.
Audit mode must not create a runtime environment, install dependencies, run
third-party code, generate target outputs, or compare generated outputs.

Use audit mode for requests such as:

- "review paper"
- "audit this paper"
- "score reproducibility"
- "readiness score"
- "assess whether this is reproducible"
- "make a reproduction package" when the user does not also ask to run code

Execution mode is allowed only when the user explicitly asks for it in the
prompt or explicitly approves it in a follow-up. Examples include:

- "run it"
- "execute the code"
- "attempt reproduction"
- "reproduce the results"
- "generate the target outputs"
- "rerun the benchmark"
- "yes, run the commands"

Do not infer execution permission from a source URL, an uploaded paper, a
GitHub repository, the word "review", or the existence of runnable code. Do not
set `review_status` to `"approved"` merely because Codex has inspected the
recipe. Recipe approval is an execution gate and requires explicit user
permission.

If the user asks for audit/readiness only, complete every non-execution step
that can run honestly, record any blockers, leave execution-related scores as
`null` or clearly "not attempted", and state that execution was not attempted.

Do not quietly narrow the reproduction scope. If the paper has multiple
important claims, figures, tables, benchmarks, datasets, model checkpoints, or
pipelines, identify them as targets even when the full run is expensive or
partially blocked. A smaller dataset-only, figure-only, or metric-only run is
allowed only in execution mode, and only when it is explicitly labeled as a
subset or smoke test and the unattempted full-paper targets remain visible as
incomplete, blocked, or failed.

Built-in sample papers and remote papers use the same mode gate. Codex reads
the prepared evidence, writes `REPRODUCTION_TARGETS.json`,
`TARGET_CONTENT.json` when paper-side content is needed, and
`REPRODUCTION_RECIPE.json`, then calls only the generic helper scripts allowed
by the selected mode. Do not use a hardcoded fixture workflow to prove agent
behavior.

The old trusted-local wrapper has been moved to
`scripts/archive/run_trusted_local_workflow.py` for migration history only. It
is not the active reproduction path and should not be used for current workflow
tests.

## Agent And Script Responsibilities

Codex is responsible for judgment and sequencing:

- classify the input
- read the paper text and identify reproduction targets
- write or update `REPRODUCTION_TARGETS.json`, including target-level
  `paper_content_extraction` instructions when needed
- run paper-side target content extraction for figures, tables, plots, and
  other visual/numeric claims before claiming target matches
- locate code, data, checkpoints, and environment information
- write or update `REPRODUCTION_RECIPE.json`
- decide which helper script should run next
- interpret failures honestly
- write the final user-facing summary

Helper scripts are responsible for repeatable actions:

- create package files and folders
- record paper, code, environment, execution, and comparison evidence
- extract text
- copy or clone code
- validate recipes
- extract paper-side target content
- in execution mode, create isolated environments
- in execution mode, run approved commands
- in execution mode, compare generated outputs mechanically
- regenerate scorecards and readmes from recorded evidence

Scripts do not replace Codex reasoning. Codex calls scripts in the correct order.

## Execution Scope And Safety

Run local execution only when both conditions are true:

1. The user explicitly requested or approved execution.
2. `REPRODUCTION_RECIPE.json` is validated, has `review_status: "approved"`,
   and the helper script is called with its explicit execution flag.

Use the execution backend supported by the current helper scripts. The current
local helper path creates `runtime/conda-env`; a conda environment isolates
dependencies but is not a security sandbox. Treat third-party code execution as
trusted-code execution.

In audit mode, do not call `setup_reproduction_environment.py
--allow-execution` or `generate_target_outputs.py --allow-execution`. Do not run
equivalent setup, install, training, evaluation, benchmark, or generation
commands by hand.

If execution requires a backend or resource the helper scripts cannot provide,
record the blocker in the reproduction package. Do not silently skip the rest of
the workflow.

## Long-Run And Smoke-Test Policy

Always identify all reproduction targets in both audit mode and execution mode.
In audit mode, record long-running targets as planned, blocked, or not
attempted. In execution mode, when a target is too slow for the current helper
limits, too expensive for the local machine, or likely to run for hours or days,
add an explicit smoke-test path instead of dropping the target.

For long-running benchmark/training/evaluation targets:

- Classify every target with `evidence_scope`: `full_claim`, `smoke_test`,
  `readiness`, or `supporting`. Only `full_claim` targets contribute to target
  match. Smoke and readiness checks are reported separately.
- Keep the full target in `REPRODUCTION_TARGETS.json` with the paper's expected
  output and status `not_attempted`, `blocked`, `failed`, or `partial` after
  comparison. Do not mark the full target as passed unless all required outputs
  were generated and compared.
- Decide full-vs-smoke at the smallest practical target group, such as one
  classifier family, table row group, seed group, checkpoint, figure, or
  training run. Do not downgrade an entire benchmark to smoke mode when some
  target groups can reasonably run at paper scale.
- Run a short pilot when practical. Record `runtime_estimate.seconds`, its
  `method`, and the pilot duration and scale factor. Do not classify a target
  as too long without a recorded estimate or a concrete resource blocker.
- In execution mode, add one or more smoke-test targets that exercise the same workflow on a
  smaller, bounded run. Examples: one row per benchmark family, a tiny training
  split, one epoch, one seed, one fold, one representative checkpoint, or a
  short runtime-limited command.
- Make the smoke-test label explicit in target IDs, descriptions, report text,
  score notes, and dashboard output.
- Prefer smoke tests that touch every major component or model family over
  smoke tests that only run the first easy target.
- Record the exact reduction: sample size, epochs, seeds, rows, model families,
  timeout, hardware, and any skipped outputs.
- Score the full target and the smoke target separately. A passed smoke test
  means the workflow path was exercised; it does not mean the paper result was
  fully reproduced.
- When a smoke test produces reduced evidence for a full target, show the full
  target as `partial` in user-facing dashboards/reports. Also show both values:
  the full paper-scale output produced and the reduced smoke-test output
  produced.
- If the smoke test passes and the full target remains incomplete, report the
  reproduction status as `partial`, not `success`.

## Full Reproduction Workflow

Run these steps in order for every reproduction request. The first twelve steps
are audit-safe. Steps 13-16 are execution-gated and require explicit user
permission. If a step cannot run, record the blocker and continue with later
steps that remain meaningful for the selected mode.

1. Create the reproduction package with `create_reproduction_package.py`.
2. Record the paper source with `write_paper_source.py`.
3. Download or copy available paper, code, data, and supplementary materials.
4. Extract paper text into `PAPER_TEXT.txt` with `extract_paper_text.py`.
5. Render PDF pages into `PAPER_ASSETS/` with `render_paper_pages.py` when a PDF is available.
6. Inspect `PAPER_TEXT.txt` and rendered pages to identify figures, tables,
   plots, metrics, datasets, checkpoints, scripts, notebooks, and pipelines.
7. Write or update `REPRODUCTION_TARGETS.json`.
   Include full-paper targets first. If a full target is too long-running,
   also include explicit smoke-test targets that exercise the same workflow
   without replacing the full target.
8. For every figure, table, plot, or visual/numeric claim that needs paper-side
   values, add `paper_content_extraction` to the target and run
   `extract_target_content.py` to create `TARGET_CONTENT.json`.
9. Acquire executable code into `code/` with `get_code_source.py` or the
   source-specific downloader already used for the package.
10. Detect dependencies and environment facts with `write_code_dependencies.py`.
11. Write `REPRODUCTION_RECIPE.json` with setup commands, run commands,
    expected outputs, and target-output mappings.
    For long-running work, include bounded smoke-test commands in addition to
    the full command. Give paired commands the same `selection_group`, set
    `mode` to `full` or `smoke`, and list the target IDs each command covers.
12. Validate the recipe with `validate_reproduction_recipe.py`.
13. Stop here in audit mode. Leave the recipe unapproved, finalize a readiness
    report, and state that execution was not attempted.
14. In execution mode only, set `review_status` to `approved` after the user has
    explicitly approved the exact commands.
15. In execution mode only, acquire declared HTTPS data with
    `acquire_reproduction_data.py --allow-network`, when the recipe has URL
    sources. Preserve checksums in `DATA_ACQUISITION.json`.
16. In execution mode only, create the environment and run setup with
    `setup_reproduction_environment.py --allow-execution`.
17. In execution mode only, generate target outputs with
    `generate_target_outputs.py --allow-execution --mode auto`. Use a recorded
    per-target runtime budget and `--resume` for interrupted long runs.
18. In execution mode only, compare generated outputs with `compare_targets.py`. Use
    `target_content_csv` when a generated CSV should match paper-side
    `TARGET_CONTENT.json` values.
19. Write the final report and score. Use readiness-only scoring when execution
    was not attempted; use execution evidence when execution was explicitly run.
20. Write `DASHBOARD_RECORD.json` with `write_dashboard_record.py`, then render
    the scorecard-style `DASHBOARD.html` with
    `render_reproduction_dashboard.py` when a dashboard view is useful. The
    renderer should read user-facing prose, target explanations, and score
    explanations from `DASHBOARD_RECORD.json`, not invent them while rendering
    HTML.
21. Update `REPRO_PLAN.md`, `REPRODUCTION_REPORT.txt`, and
    `REPRODUCTION_SCORE.json` so they reflect what actually happened.

Do not claim a figure, table, plot, or reported metric matched unless
paper-side expected values were extracted, recorded, and compared. File
existence checks are useful evidence, but they are `generated_unverified`, not
reproduced result matches.

For long runs, do not present an early stop as a full reproduction. Present it
as a smoke test or partial reproduction, with completed rows and uncompleted
rows both recorded.

## Failure And Retry Procedure

If validation, setup, execution, or comparison fails:

1. Stop the current step.
2. Read the command output, `logs/`, and the relevant record file.
3. Classify the issue as a blocker, missing material, environment problem,
   recipe problem, or target mismatch.
4. Do not delete or hide the failed logs or evidence.
5. If an adjustment is justified, edit `REPRODUCTION_RECIPE.json` and document the
   adaptation.
6. Validate the updated recipe before running anything else.
7. Rerun from the earliest affected step:
   - dependency or setup changes: rerun setup, execution, comparison, finalize
   - reproduction command changes: rerun execution, comparison, finalize
   - comparison-only changes: rerun comparison and finalize
8. If no justified adjustment exists, finalize the package with the blocker
   documented.

Do not loop indefinitely or guess commands just to make a run succeed.

## Helper Script Map

Detailed script usage examples live in `references/helper_scripts.md`.

Use this table to choose the next helper:

| Area | Helper | Purpose |
| --- | --- | --- |
| Start | `create_reproduction_package.py` | Create the package folder and starter files. |
| Source | `write_paper_source.py` | Record the paper source in `PAPER_SOURCE.json`. |
| Source | `download_paper_and_code.py` | Download an arXiv PDF and source/code archive into the package. |
| Paper | `extract_paper_text.py` | Create `PAPER_TEXT.txt` from the recorded source. |
| Paper | `render_paper_pages.py` | Render every available PDF page into `PAPER_ASSETS/` for agent visual inspection. |
| Targets | `write_reproduction_targets.py` | Add figures, tables, metrics, datasets, checkpoints, or scripts to `REPRODUCTION_TARGETS.json`. |
| Targets | `extract_target_content.py` | Read paper-side target content, including digitized plots and tables, into `TARGET_CONTENT.json`. |
| Targets | `compare_target_content.py` | Compare extracted paper-side target content against a reproduction CSV. |
| Code | `get_code_source.py` | Copy or clone code into `code/` and record `code_source`. |
| Code | `write_code_dependencies.py` | Inspect dependency files and record environment evidence. |
| Recipe | `validate_reproduction_recipe.py` | Validate `REPRODUCTION_RECIPE.json` before setup or execution. |
| Data | `acquire_reproduction_data.py` | Execution mode only. Download declared HTTPS data and verify optional SHA-256 checksums. |
| Run | `setup_reproduction_environment.py` | Execution mode only. Build `runtime/conda-env` and run approved setup commands. |
| Run | `generate_target_outputs.py` | Execution mode only. Select full/smoke commands per target group, resume completed outputs, and write `TARGET_OUTPUTS.json`. |
| Compare | `compare_targets.py` | Execution mode only. Compare declared outputs and copy generated files into `artifacts/generated/`. |
| Finalize | `write_reproduction_report.py` | Regenerate `REPRODUCTION_SCORE.json` and `REPRODUCTION_REPORT.txt` from evidence. |
| Finalize | `write_reproduction_score.py` | Create or update scores when execution was blocked. |
| Finalize | `render_reproduction_report.py` | Create the plain-language report when execution was blocked. |
| Finalize | `write_dashboard_record.py` | Write `DASHBOARD_RECORD.json` with user-facing dashboard text derived from package records. |
| Finalize | `render_reproduction_dashboard.py` | Create the scorecard-style `DASHBOARD.html` from `DASHBOARD_RECORD.json` and `REPRODUCTION_SCORE.json` status flags. |

### Figure And Table Content

Beyond checking that a figure file exists, the skill can read the actual numbers
behind a paper's figures and tables and compare them to the reproduction. Run
these in the `reproduce-it` conda environment. This is a required part of the
workflow whenever a figure, table, plot, or visual metric is used as a match
target. In audit mode, extract and record paper-side target content when useful,
but do not compare it against generated reproduction outputs unless execution
was explicitly approved and run.

Two steps:

1. `extract_target_content.py` -> `TARGET_CONTENT.json` (reads each target's
   `paper_content_extraction`, digitizes plots/panels, and reads tables
   from the PDF text layer).
2. `compare_target_content.py` -> compares that against the reproduction's numbers.

Target-driven extraction command shape:

```bash
python .agents/skills/echomill/scripts/extract_target_content.py \
  --pdf path/to/paper.pdf \
  --targets path/to/REPRODUCTION_TARGETS.json \
  --out path/to/TARGET_CONTENT.json
```

Extracted numbers are recorded with their extraction confidence. Do not report a
numerical match unless the generated output was compared against these extracted
paper-side values. See
`references/helper_scripts.md` for exact commands.

## Required Package Structure

Create or update a folder called a **reproduction package**.

Recommended structure:

Reader-facing files stay at the package root; every evidence record (text and
JSON derived from the paper, code, and runs) lives in the `paper-derived/`
subfolder.

```text
reproduction-packages/<safe-paper-name>/
  REPRO_PLAN.md
  REPRODUCTION_REPORT.txt
  REPRODUCTION_SCORE.json
  REPRODUCTION_RECIPE.json
  DASHBOARD_RECORD.json
  DASHBOARD.html
  paper-derived/
    PAPER_SOURCE.json
    PAPER_ASSETS.json
    PAPER_TEXT.txt
    REPRODUCTION_TARGETS.json
    TARGET_CONTENT.json
    CODE_SOURCE.json
    CODE_DEPENDENCIES.json
    REPRODUCTION_ENVIRONMENT.json
    TARGET_OUTPUTS.json
    TARGET_COMPARISON.json
  artifacts/
    expected/
    generated/
    comparisons/
  code/
    adapters/
  logs/
  runtime/
    conda-env/
```

## Required Files

### `REPRO_PLAN.md`

The reproduction plan. Include paper source, code source, data source, expected
reproduction targets, required environment, expected commands, blockers, assumptions, and
next steps.

### `REPRODUCTION_REPORT.txt`

The plain-language report. Explain what was attempted, what worked, what failed,
what was missing, what was adapted, what assumptions were made, how to rerun the
attempt, and the final score summary.

### `REPRODUCTION_SCORE.json`

The machine-readable score. Keep readiness scoring separate from actual
reproduction scoring.

It should include:

- `overall_score`
- `readiness_score`
- `execution_score`
- `target_match_score`
- `data_availability_score`
- `code_availability_score`
- `environment_completeness_score`
- `documentation_score`
- `adaptation_burden_score`
- `blockers`
- `successful_targets`
- `failed_targets`
- `unknown_targets`
- `notes`

### `REPRODUCTION_TARGETS.json`

The structured inventory of reproduction targets: figures, tables, plots, metrics,
datasets, trained models, checkpoints, scripts, notebooks, preprocessing
pipelines, and evaluation pipelines.

A **claim** is an assertion recorded in `paper_elements`. A **target** is a
concrete output or check used to test that assertion. Add each applicable
`paper_elements[].id` to the target's `claim_ids` list. A target may support
more than one claim. Dashboards roll up claim status from required
`full_claim` targets and show smoke, readiness, and supporting links separately.
Record `dashboard_summary.main_claim` and `dashboard_summary.main_blocker` in
the target inventory when the default first-claim and scorecard-blocker text
would not give a clear one-glance summary. The rendered Paper Summary contains
only those two facts; the Overall Reproduction card carries the paper-claim
pass count.

Each target should have a stable ID such as:

```text
figure_1
table_2
metric_main_accuracy
dataset_training
checkpoint_main_model
```

#### Standard target types

Every target must be one concrete thing from this rubric (the `type` field,
enforced by `write_reproduction_targets.py`):

| Type | Use for |
| --- | --- |
| `plot` | A chart, graph, or curve whose data points can be digitized and compared. |
| `table` | A table of reported values. |
| `metric` | A single reported number (accuracy, loss, runtime, count). |
| `image` | A qualitative image or sample grid. |
| `structure` | A reported structure such as a network architecture or file layout. |
| `dataset_output` | A dataset property: split sizes, shapes, class balance, checksums. |
| `model_checkpoint` | A trained model artifact. |
| `generated_file` | Any other file the paper's pipeline should produce. |
| `script_output` | The output of running a specific script or command. |
| `pipeline_output` | The end result of a multi-step pipeline. |
| `other` | Only when nothing above fits. |

Pick from this list first. If no entry fits, pass `--allow-new-type` and
document the new type in a target note so the addition is deliberate and
auditable.

Record the paper page number(s) on every target and paper element (`page`,
e.g. `"4"` or `"3-6"`, via `--page`) so dashboard readers can find the element
in the paper. Verify pages against `PAPER_ASSETS/` page images, not memory.

#### Standard comparison classes

Every comparison must use one class from this rubric (the recipe's
`comparison.method` and the target's `comparison_method`):

| Class | What is compared |
| --- | --- |
| `numeric_tolerance` | One number against the expected value within a margin. |
| `table_tolerance` | Every cell of a small table within a margin. |
| `exact_text` | Output text must match the expected text exactly. |
| `checksum` | The file's SHA-256 hash must match. |
| `figure_presence` | The figure file exists and is non-empty; always recorded as `generated_unverified`, never a full match. |
| `target_content_csv` | Extracted paper-side plot/table content against a generated CSV. |

Pick from this list first. A new class is a code change, not just a label:
implement it in `compare_targets.py`, add it to
`REPRODUCTION_RECIPE.schema.json`, and add it to `COMPARISON_CLASSES` in
`target_records.py` before using it in a recipe.

If a figure, figure panel, or table needs paper-side content extraction, put the
simple extraction instruction directly on that target as
`paper_content_extraction`. Do not create a separate extraction-plan file.
Use rendered page images from `PAPER_ASSETS/` when available to identify visible
figures and panels before writing these target records.

Example:

```json
{
  "id": "figure_2_panel_a",
  "type": "plot",
  "paper_reference": "Figure 2A",
  "comparison_method": "target_content_csv",
  "paper_content_extraction": {
    "method": "raster_panel_crop",
    "page": 2,
    "paper_element_id": "paper_figure_2",
    "parent_figure_id": "figure_2",
    "panel_label": "A",
    "bbox_fraction": [0.0, 0.0, 0.5, 1.0],
    "x_label": "Step",
    "y_label": "Response"
  }
}
```

### Evidence Record Files

Machine-readable source and execution records. All of them live in the
package's `paper-derived/` subfolder; the helper scripts read and write them
there automatically.

Use these records when available:

- `PAPER_SOURCE.json`: paper input, source type, extraction status, and links.
- `PAPER_ASSETS.json`: rendered PDF page images for agent visual inspection.
- `CODE_SOURCE.json`: copied or cloned code source and destination.
- `CODE_DEPENDENCIES.json`: dependency files and setup-command suggestions.
- `DATA_ACQUISITION.json`: URL acquisition results, checksums, and failures.
- `REPRODUCTION_ENVIRONMENT.json`: actual conda setup result and installed packages.
- `TARGET_OUTPUTS.json`: commands run from the recipe and files produced.
- `TARGET_COMPARISON.json`: comparison results for generated outputs.

Use evidence record files for facts that should not be mixed into the scorecard,
recipe, or target inventory.

### `REPRODUCTION_RECIPE.json`

The agent-written runbook for execution. It lists command working directories,
setup commands, reproduction steps, expected generated outputs, comparison
methods, data sources, and review status.

Full/smoke alternatives must use structured `mode`, `selection_group`, and
`target_ids` fields. Do not encode execution scope only in a command ID or an
adapter argument. Record pilot-based runtime estimates when available.

Validate it with `validate_reproduction_recipe.py` before any setup or execution.

## Scoring Rules

Use cautious, evidence-based scoring.

Separate:

1. **Readiness score**: how well the paper and available materials support
   reproduction.
2. **Actual reproduction score**: what happened when code was run, reproduction targets
   were generated, and outputs were checked.

The 100-point breakdown is outcome-weighted: target match dominates because
the overall score is presented as predicted reproducibility of the paper's
results.

```text
40 points - target match quality
15 points - execution success
15 points - data availability
10 points - code availability
10 points - environment completeness
10 points - claim mapping (fraction of recorded paper claims that map
            to at least one reproduction target; scorecard key
            documentation_score)
```

A failed, blocked, or incomplete full-claim target caps the dashboard verdict
at "Moderately reproducible" regardless of the arithmetic score. A
readiness-only score (execution or comparison not attempted) shows the
verdict "Readiness only" instead of a reproducibility claim. Full-claim targets
with no recorded comparison count as unearned weight. Smoke, readiness, and
supporting targets are displayed separately and do not affect target match.

For **data availability**, do not subtract points merely because there is no
independent checksum/evidence audit for every data artifact. Checksums are
useful when the paper, repository, or dataset source provides them, but they are
not a universal scoring requirement. Subtract data points only when evidence
shows that required data is missing, incomplete, wrong, inaccessible,
compromised/corrupted, or unusable for the reported reproduction target.

For **code provenance**, a recorded immutable release-archive SHA-256 provides
the same provenance credit as a pinned Git commit. Do not penalize journal or
repository archives merely because their immutable reference is a checksum
rather than a commit object.

If execution was blocked, leave execution-related fields `null` or clearly
state that execution was not attempted and why.

Do not give a high actual reproduction score unless code was run and reproduction targets
were checked.

Use `references/scoring_rubric.md` when making scoring judgments.

## Reproduction Target Handling

Identify reproduction targets such as:

- figures
- tables
- reported metrics
- plots
- datasets
- trained models
- checkpoints
- scripts
- notebooks
- configuration files
- preprocessing pipelines
- evaluation pipelines

For each target, record:

- stable ID
- concrete type from the standard target-type rubric
- paper reference and page number(s)
- one or more `claim_ids` linking the target to recorded paper claims
- expected output
- generated output if reproduction was attempted
- comparison method from the standard comparison classes if possible
- status
- notes and blockers

## Adaptation Handling

Every adaptation must be documented.

Examples:

- changing Python versions
- replacing deprecated dependencies
- changing file paths
- using substitute data
- reducing training time
- changing hardware
- skipping unavailable checkpoints
- rewriting notebooks as scripts
- guessing undocumented preprocessing
- changing random seeds
- using smaller models

Adaptations are not automatically failures, but they must be visible.

## Reference Documents

Load these only when needed:

- `references/scoring_rubric.md`: scoring rubric for readiness and actual
  reproduction scoring.
- `references/helper_scripts.md`: detailed helper script commands and usage
  notes.
- `assets/REPRODUCTION_RECIPE.schema.json`: schema for validating
  `REPRODUCTION_RECIPE.json`.

## Final Response To User

At the end, provide a short, honest summary.

Include:

- reproduction package location
- overall score
- readiness score, as one score dimension
- execution score if available
- generated target outputs if any
- main blockers
- next best step
- whether the package was audit-only or execution mode

Prefer:

```text
Audit completed. Execution was not attempted because the user did not approve running code.
```

or:

```text
Execution workflow completed with execution blocked because the original dataset was unavailable.
```

or:

```text
Partially reproduced: code ran and generated two target outputs, but plot comparison remains unverified.
```

Do not say:

```text
Fully reproduced.
```

unless reproduction targets were generated and checked.

## Implementation Boundaries

Keep the workflow simple and complete.

Prioritize:

1. creating the reproduction package folder
2. recording paper, code, data, and environment evidence
3. extracting paper text and rendered page images
4. identifying reproduction targets
5. extracting paper-side target content for figures, tables, plots, and visual metrics
6. writing and validating `REPRODUCTION_RECIPE.json`
7. in execution mode only, executing the approved recipe-driven path
8. in execution mode only, comparing generated outputs against extracted or recorded expected values
9. writing `REPRO_PLAN.md`, `REPRODUCTION_REPORT.txt`, and `REPRODUCTION_SCORE.json`

Do not start with a web app, database, queue system, Docker runner, GPU runner,
or multi-agent system.
