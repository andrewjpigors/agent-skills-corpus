---
name: nit-pick-supreme
description: "Unified code review: federated analysis engines, parallel fixes, browser testing. Replaces /code-review-workflow and /nit-pick."
argument-hint: "[--static|--code|--arch|--e2e|--explore|--fix|--logs] [--quick|--standard|--deep] [--scope=full|diff] [--diff-base=REF] [--test-cmd=CMD] [--no-fix] [--auto-approve] [--log-days=N]"
---

# nit-pick-supreme

Unified code review system with federated analysis engines, parallel fixes via git worktrees, and browser-level testing. Runs a 9-stage pipeline:

1. **Context Discovery** -- detect tech stack, test runners, build file scope
1.5. **Deterministic Auto-Fix** -- run ruff --fix on mechanical lint issues before LLM dispatch
1.7. **Engine Gating** -- skip engines that cannot contribute to this project
2. **Engine Dispatch** -- run analysis engines in parallel (static sweep, code agents, arch agents, browser E2E, AI explorer)
3. **Synthesis** -- collect findings, deduplicate across engines, link related issues, sort by severity
4. **Fix Planning** -- cluster findings into fix groups, assign to parallel waves (Phase 5)
5. **Fix Execution** -- apply fixes in isolated git worktrees, test, merge (Phase 5)
6. **Report Generation** -- produce REVIEW.md and terminal summary

## Parse Arguments

Parse `$ARGUMENTS` for these flags:

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--static` | boolean | false | Enable static sweep engine |
| `--code` | boolean | false | Enable code-level agents (Haiku) |
| `--arch` | boolean | false | Enable architecture agents (Opus) |
| `--e2e` | boolean | false | Enable browser E2E engine |
| `--explore` | boolean | false | Enable AI explorer (Sonnet) |
| `--fix` | boolean | false | Enable fix pipeline |
| `--logs` | boolean | false | Enable log sweep engine |
| `--log-days` | integer | 7 | Max age in days for log files (used with --logs) |
| `--no-fix` | modifier | - | Remove --fix from any preset |
| `--quick` | preset | - | Expand to: --static |
| `--standard` | preset | - | Expand to: --static --code --e2e --fix |
| `--deep` | preset | - | Expand to: --static --code --arch --e2e --explore --fix --logs |
| `--scope` | string | full | `full` or `diff` |
| `--diff-base` | string | HEAD | Git ref for diff scope |
| `--test-cmd` | string | auto | Override test runner |
| `--auto-approve` | boolean | false | Skip fix approval prompt |

**Validation rules:**

1. If no flags and no preset: load config.yaml for `default_preset`, fall back to `--standard`.
   Load config via: `python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py load-config --project-root=. --output-path=.nit-supreme/config.json`
   Read the config JSON and use the `default_preset` value to expand the preset.

2. If a preset AND individual engine flags are both present: individual flags override the preset entirely. Ignore the preset.

3. If `--no-fix` is present: strip `--fix` after any preset expansion.

4. Track explicit flags: Before preset expansion, check the raw `$ARGUMENTS` string for explicit engine flags:
   - `arch_explicit = true` if `--arch` appears in raw `$ARGUMENTS`
   - `code_explicit = true` if `--code` appears in raw `$ARGUMENTS`
   - `e2e_explicit = true` if `--e2e` appears in raw `$ARGUMENTS`
   - `explore_explicit = true` if `--explore` appears in raw `$ARGUMENTS`
   These flags determine whether engine-specific skip/gate checks can be overridden. Gates ONLY apply when the corresponding `*_explicit` is false (or hard gates, which cannot be overridden even when explicit).

5. If unknown flags are detected: print an error message listing valid flags and STOP. Do not continue the pipeline.

## Checkpoint Resume

Before starting the pipeline, check for an existing checkpoint:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py load-checkpoint \
  --output-dir=.nit-supreme
```

If the output is valid JSON (not "No valid checkpoint found"):
1. Parse the checkpoint JSON
2. Compute the current context hash:
   ```
   python -c "
   import sys; sys.path.insert(0, str(__import__('pathlib').Path.home() / '.claude/skills/nit-pick-supreme'))
   from scripts.orchestrator import compute_context_hash
   from pathlib import Path
   print(compute_context_hash(Path('.nit-supreme/context.json')))
   "
   ```
3. Compare the checkpoint's `context_hash` with the computed hash:
   - If they MATCH: resume from the checkpoint. Use the checkpoint's `flags` and `preset`. Skip stages listed in `completed_stages`. Print "Resuming from stage {current_stage} (stages {completed_stages} already complete)".
   - If they DIFFER: discard the checkpoint. Print "Checkpoint stale (project changed since last run). Starting fresh." Delete checkpoint.json and proceed normally.
4. If resuming: set the flags and preset from the checkpoint values, then jump to the first incomplete stage.

If no checkpoint found, proceed normally from Stage 0.

## Stage 0 -- Memory Consolidation

Before starting the pipeline, run memory consolidation and reset per-run counters:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py consolidate-memory
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py reset-counters
```

This runs at the start of every invocation. Consolidation archives memory entries older than 90 days and merges duplicates. Counter reset zeros the per-run telemetry so the Memory Effectiveness section in REVIEW.md reflects this run only.

## Stage 1 -- Context Discovery

Create the output directory structure:

```
mkdir -p .nit-supreme/engine-output
```

Record the pipeline start time for duration tracking.

Run context discovery:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py discover-context \
  --project-root=. \
  --scope={scope} \
  --output-path=.nit-supreme/context.json \
  {--diff-base=REF if scope=diff} \
  {--test-cmd=CMD if provided} \
  {--auto-approve if set}
```

Read `.nit-supreme/context.json` to confirm context was discovered. Print a brief summary: language, framework, file count, test runner.

Compute the context hash for checkpoint validation:
```
python -c "
import sys; sys.path.insert(0, str(__import__('pathlib').Path.home() / '.claude/skills/nit-pick-supreme'))
from scripts.orchestrator import compute_context_hash
from pathlib import Path
print(compute_context_hash(Path('.nit-supreme/context.json')))
"
```
Record this hash value. Save checkpoint:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py save-checkpoint \
  --output-dir=.nit-supreme \
  --stage=1 \
  --completed-stages=1 \
  --engine-results='{}' \
  --flags='{"static":{static},"code":{code},"arch":{arch},"e2e":{e2e},"explore":{explore},"fix":{fix}}' \
  --preset={preset} \
  --context-hash={computed_hash}
```

## Stage 1.5 -- Deterministic Auto-Fix

After context discovery, run deterministic auto-fix to eliminate mechanical lint issues before any LLM engine sees the codebase. This stage is always-on for Python projects and skips gracefully for others.

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py autofix \
  --project-root=. \
  --output-path=.nit-supreme/autofix-manifest.json \
  --context-path=.nit-supreme/context.json
```

Read `.nit-supreme/autofix-manifest.json`. The command prints a summary line to stdout:
- If fixes were applied: "Auto-fixed: N issues (F401: X, F841: Y, I001: Z)"
- If skipped: "Auto-fix: skipped (reason)"
- If clean: "Auto-fix: 0 issues (clean codebase)"

Print this line to the user.

**Note (AFIX-04):** Static sweep in Stage 2 runs on the post-autofix working tree, so it naturally reports only issues ruff cannot fix. No coordination needed -- the file system IS the coordination mechanism.

Save checkpoint with stage 0.5 completed:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py save-checkpoint \
  --output-dir=.nit-supreme \
  --stage=1.5 \
  --completed-stages=1,1.5 \
  --engine-results='{}' \
  --flags='{"static":{static},"code":{code},"arch":{arch},"e2e":{e2e},"explore":{explore},"fix":{fix}}' \
  --preset={preset} \
  --context-hash={computed_hash}
```

## Stage 1.7 -- Engine Gating

After context discovery and auto-fix, compute engine gates to determine which engines should be skipped:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py compute-gates \
  --context-path=.nit-supreme/context.json \
  --output-path=.nit-supreme/engine-gates.json \
  --engine-output-dir=.nit-supreme/engine-output
```

This command:
1. Reads context.json (with source_files and tech_stack)
2. Evaluates gate conditions for each engine
3. Writes engine-gates.json with gate decisions
4. Writes gated engine output files (status: "gated") to engine-output/ so synthesis includes them in engine-stats

Read `.nit-supreme/engine-gates.json`. For each gated engine, the command will print:
"Engine {name} gated: {reason}"

Gate types:
- **Soft gates** (code-frontend, ai-explorer, browser-e2e without playwright issue): Can be overridden by explicit flags (--code, --explore, --e2e)
- **Hard gates** (browser-e2e when playwright not in dependencies): Cannot be overridden even with explicit flags

Engine-to-explicit-flag mapping for gate override:
- `code-frontend` -> `code_explicit`
- `code-backend` -> `code_explicit`
- `ai-explorer` -> `explore_explicit`
- `browser-e2e` -> `e2e_explicit`

Save checkpoint after engine gating:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py save-checkpoint \
  --output-dir=.nit-supreme \
  --stage=1.7 \
  --completed-stages=1,1.5,1.7 \
  --engine-results='{}' \
  --flags='{flags_json}' \
  --preset={preset} \
  --context-hash={context_hash}
```

## Stage 2 -- Engine Dispatch

Build the list of enabled engines from parsed flags. Dispatch engines in two groups:

### Group A -- Parallel (no dependencies between these)

Issue ALL Group A tool calls in a SINGLE message for maximum parallel execution:

- **If --static is enabled:** Use Bash tool:
  ```
  python ~/.claude/skills/nit-pick-supreme/scripts/static_sweep.py \
    --project-root=. \
    --scope={scope} \
    --output-path=.nit-supreme/engine-output/static-sweep.json \
    {--diff-base=REF if scope=diff}
  ```

- **If --code is enabled:** Use Agent tool for code-level agents, checking gates first:

  **code-frontend:** Check engine-gates.json for "code-frontend" entry.
    - If gated AND gate is hard: skip (print "code-frontend gated (hard): {reason}")
    - If gated AND gate is soft AND `code_explicit` is false: skip (already handled by compute-gates output file)
    - If gated AND gate is soft AND `code_explicit` is true: dispatch normally (override gate, print "code-frontend: overriding soft gate (--code explicit)")
    - If not gated: dispatch normally
  `Agent(subagent_type="nps-code-frontend", prompt="Analyze the project at {project_root}. Read .nit-supreme/context.json for project context. Use the source_files list for your analysis scope. Write findings to .nit-supreme/engine-output/code-frontend.json using the unified findings schema.")`

  **code-backend:** Always dispatch when --code is enabled (no gate condition for code-backend).
  `Agent(subagent_type="nps-code-backend", prompt="Analyze the project at {project_root}. Read .nit-supreme/context.json for project context. Use the source_files list for your analysis scope. Write findings to .nit-supreme/engine-output/code-backend.json using the unified findings schema.")`

  **code-safety:** Always dispatch when --code is enabled (per SCOPE-03, uses full files list).
  `Agent(subagent_type="nps-code-safety", prompt="Analyze the project at {project_root}. Read .nit-supreme/context.json for project context. Use the full files list (not source_files) for security analysis. Write findings to .nit-supreme/engine-output/code-safety.json using the unified findings schema.")`

- **If --e2e is enabled:** Check engine-gates.json for "browser-e2e" entry.
    - If gated AND gate is hard: skip, print "browser-e2e gated (hard): {reason} -- cannot override with --e2e"
    - If gated AND gate is soft AND `e2e_explicit` is false: skip (gated output file already written)
    - If gated AND gate is soft AND `e2e_explicit` is true: dispatch normally (override gate)
    - If not gated: dispatch normally
  ```
  python ~/.claude/skills/nit-pick-supreme/scripts/browser_e2e.py \
    --project-root=. \
    --output-path=.nit-supreme/engine-output/browser-e2e.json
  ```

- **If --logs is enabled:** Use Bash tool:
  ```
  python ~/.claude/skills/nit-pick-supreme/scripts/log_sweep.py \
    --project-root=. \
    --output-path=.nit-supreme/engine-output/log-sweep.json \
    {--log-days=N if --log-days provided} \
    {--config-log-paths=paths if config.yaml has log_paths key}
  ```

**Before dispatching each agent or script:** Check if the agent definition file or script file exists. If not found, skip that engine with a warning message (e.g., "Skipping nps-code-frontend: agent definition not found"). This allows additive development -- the orchestrator works with whatever engines are available.

### Arch Agent Skip Gates

After Group A engines complete, evaluate whether to dispatch architecture agents.

**If `arch_explicit` is true (user explicitly passed `--arch`):**
Skip gate evaluation entirely. Dispatch all arch agents as Group A2.

**If `arch_explicit` is false (--arch came from preset expansion or is not set):**

**If --arch is not enabled at all:** Skip this section (no arch agents to dispatch).

**Gate 1 -- File count (PERF-01):**
Read `.nit-supreme/context.json` and extract the `file_count` value.
If `file_count` < 20:
  Print: "arch agents skipped: <20 files in scope"
  Skip arch agent dispatch. Proceed to Group B.

**Gate 2 -- Finding count (PERF-02):**
Count total code-level findings from Group A outputs:
- Read `.nit-supreme/engine-output/code-frontend.json` (if exists)
- Read `.nit-supreme/engine-output/code-backend.json` (if exists)
- Read `.nit-supreme/engine-output/code-safety.json` (if exists)
- Read `.nit-supreme/engine-output/static-sweep.json` (if exists)
- For each file, parse JSON and count the length of the `findings` array
- Sum all finding counts

If total findings > 80:
  Print: "arch agents skipped: >80 code-level findings"
  Skip arch agent dispatch. Proceed to Group B.

**If neither gate triggers:** Dispatch arch agents as Group A2.

### Group A2 -- Architecture Agents (conditional)

If arch agents passed the skip gates above, dispatch all three arch agents in a SINGLE message:
- `Agent(subagent_type="nps-arch-structure", prompt="Analyze architecture at {project_root}. Read .nit-supreme/context.json. Use the source_files list for your analysis scope. Write findings to .nit-supreme/engine-output/arch-structure.json.")`
- `Agent(subagent_type="nps-arch-contracts", prompt="Analyze architecture at {project_root}. Read .nit-supreme/context.json. Use the source_files list for your analysis scope. Write findings to .nit-supreme/engine-output/arch-contracts.json.")`
- `Agent(subagent_type="nps-arch-patterns", prompt="Analyze architecture at {project_root}. Read .nit-supreme/context.json. Use the source_files list for your analysis scope. Write findings to .nit-supreme/engine-output/arch-patterns.json.")`

### Group B -- Sequential (depends on Group A and Group A2 results)

After ALL Group A and Group A2 (if dispatched) engines complete:

- **If --explore is enabled:** Check engine-gates.json for "ai-explorer" entry.
    - If gated AND gate is hard: skip (print warning)
    - If gated AND gate is soft AND `explore_explicit` is false: skip (gated output file already written)
    - If gated AND gate is soft AND `explore_explicit` is true: dispatch normally (override gate)
    - If not gated: dispatch normally
  `Agent(subagent_type="nps-ai-explorer", prompt="Explore the application at {project_root}. Read .nit-supreme/context.json for context. If .nit-supreme/engine-output/browser-e2e.json exists, read it for E2E results to inform exploration. Write findings to .nit-supreme/engine-output/ai-explorer.json.")`

After the explorer agent completes, if it produced output:
1. Read `.nit-supreme/engine-output/ai-explorer.json`
2. Extract the `_meta` block from the JSON
3. If `_meta` exists and is not null, accumulate telemetry:
   ```
   python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py accumulate-telemetry \
     --output-dir=.nit-supreme \
     --meta-json='{_meta JSON string}'
   ```
4. Write the `_meta` block to `.nit-supreme/explorer-meta.json` for the report generator:
   ```
   python -c "
   import json, pathlib
   data = json.loads(pathlib.Path('.nit-supreme/engine-output/ai-explorer.json').read_text())
   meta = data.get('_meta')
   if meta:
       pathlib.Path('.nit-supreme/explorer-meta.json').write_text(json.dumps(meta, indent=2))
   "
   ```

### Engine Result Collection

After all dispatched engines complete, collect the list of engine names that were dispatched (e.g., `static-sweep,code-frontend,code-backend`). If --logs was enabled, include `log-sweep` in the list. This list is needed for Stage 3 synthesis.

**Gated engines:** Gated engines already have output files written by the compute-gates command (status: "gated"). Include their names in the engine list for synthesis so they appear in engine-stats. The comma-separated list should include all engines that were either dispatched OR gated (but NOT engines whose flag was simply disabled).

The `--engine-names` list for Stage 3 synthesis must include:
- All engines that were dispatched (regardless of success/failure)
- All engines that were gated (their output files have status: "gated")
- Do NOT include engines whose flags were not enabled at all

For engines that failed (Agent returned error, Bash command failed): if the engine is an LLM agent, it will be retried per the Agent Output Verification and Retry section below. For subprocess engines, log the failure and continue.

### Agent Output Verification and Retry

After all Group A engines complete (and Group A2 and Group B if dispatched), verify each LLM agent's output before proceeding to synthesis. This does NOT apply to subprocess engines (static-sweep, browser-e2e, log-sweep) -- those are deterministic and will not benefit from retry.

LLM agents to verify: code-frontend, code-backend, code-safety, ai-explorer, fix-planner. Additionally, if Group A2 was dispatched: arch-structure, arch-contracts, arch-patterns.

For each dispatched LLM agent, check its output file:

1. Check if `.nit-supreme/engine-output/{engine_name}.json` exists
2. If exists, verify it contains valid JSON by reading the file
3. If the file is missing, empty (0 bytes), or contains invalid JSON:
   a. Delete the partial output file if it exists: `rm -f .nit-supreme/engine-output/{engine_name}.json`
   b. Log: "Engine {engine_name} produced no valid output. Retrying in 10s..."
   c. Wait 10 seconds
   d. Re-dispatch the same Agent tool call with the original prompt
   e. After retry completes, check output file again
   f. If still missing/empty/invalid: mark engine as failed, log "Engine {engine_name} failed after retry -- marking as error", continue pipeline

**Important:** A valid JSON file with `"status": "success"` and an empty findings array `[]` is a LEGITIMATE result (engine found nothing wrong). Do NOT retry in that case.

**Important:** Delete the partial output file BEFORE retrying to prevent the retry from appending to or conflicting with the failed attempt's output.

Collect the final list of successful/failed engines for Stage 3 synthesis.

Save checkpoint after engine dispatch:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py save-checkpoint \
  --output-dir=.nit-supreme \
  --stage=2 \
  --completed-stages=1,1.5,1.7,2 \
  --engine-results='{engine_results_json}' \
  --flags='{flags_json}' \
  --preset={preset} \
  --context-hash={context_hash}
```

## Stage 3 -- Synthesis

Run synthesis on all dispatched engine outputs:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py synthesize \
  --engine-output-dir=.nit-supreme/engine-output \
  --engine-names={comma-separated list of dispatched engines} \
  --output-path=.nit-supreme/findings.json \
  --project-root=.
```

The `--project-root` parameter enables memory-based suppression checking and confidence adjustment during synthesis.

Read `.nit-supreme/findings.json` briefly to confirm synthesis completed and note the finding count.

**Post-synthesis enrichment (Phase 20):** The synthesis command now automatically consolidates same-category same-file findings (reducing finding count while preserving traceability via `consolidated_from` fields) and assigns deterministic `fix_tier` values ("auto", "mechanical", "substantive", "architectural") to every finding. No additional command needed -- these steps are integrated into the `synthesize` command pipeline.

Save checkpoint:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py save-checkpoint \
  --output-dir=.nit-supreme \
  --stage=3 \
  --completed-stages=1,1.5,1.7,2,3 \
  --engine-results='{engine_results_json}' \
  --flags='{flags_json}' \
  --preset={preset} \
  --context-hash={context_hash}
```

## Stage 3.5 -- Preliminary Report and Baseline Capture

After synthesis completes, dispatch TWO operations in parallel (issue both in a SINGLE message):

**Task A: Generate preliminary REVIEW.md**

Generate a preliminary REVIEW.md so the user can see findings before any fixes run.

Extract engine stats from findings.json:
```
python -c "
import json, pathlib
data = json.loads(pathlib.Path('.nit-supreme/findings.json').read_text())
pathlib.Path('.nit-supreme/engine-stats.json').write_text(json.dumps(data.get('engine_stats', {}), indent=2))
"
```

Generate the preliminary report (no Fixed section, no Explorer Budget):

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py generate-preliminary-review \
  --findings-path=.nit-supreme/findings.json \
  --engine-stats-path=.nit-supreme/engine-stats.json \
  --output-path=.nit-supreme/REVIEW.md \
  --config-path=.nit-supreme/config.json \
  --preset={preset_name} \
  --duration={duration_seconds} \
  --autofix-manifest-path=.nit-supreme/autofix-manifest.json
```

Print the terminal summary pointing to the preliminary report:

```
python -c "
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path.home() / '.claude/skills/nit-pick-supreme'))
from scripts.orchestrator import generate_terminal_summary
from scripts.nps_schema import Finding
data = json.loads(pathlib.Path('.nit-supreme/findings.json').read_text())
findings = [Finding.model_validate(f) for f in data.get('findings', [])]
manifest_path = pathlib.Path('.nit-supreme/autofix-manifest.json')
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else None
print(generate_terminal_summary(findings, '.nit-supreme/REVIEW.md', autofix_manifest=manifest))
"
```

Print: "Preliminary report written to .nit-supreme/REVIEW.md"
Print: "Review the findings above. Fix planning begins next."

**Task B: Capture pre-fix test baseline**

Read `.nit-supreme/context.json` to get the `test_cmd` value. Capture the current test state before any fixes are applied.

If `test_cmd` is null or empty in context.json (no test runner detected), call capture-baseline WITHOUT the `--test-cmd` flag. This produces a no-op baseline with `status: "no_test_runner"` so Stage 5 can skip test verification gracefully:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py capture-baseline \
  --project-root=. \
  --output-path=.nit-supreme/baseline.json
```

If `test_cmd` is not null, include `--test-cmd` as before:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py capture-baseline \
  --project-root=. \
  --test-cmd={test_cmd from context.json} \
  --output-path=.nit-supreme/baseline.json
```

After BOTH Task A and Task B complete, continue to Stage 4.

## Stage 4 -- Fix Planning

If `--fix` is NOT enabled, skip directly to Stage 6.

### 4.1 Stash Uncommitted Changes

Protect the user's working tree by stashing uncommitted changes before the fix pipeline modifies anything:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py stash-push \
  --project-root=.
```

Record the output. If it prints "Stashed: true" (either "true (stash)" or "true (temp_commit)"), the user had uncommitted changes and they are now safely preserved. If "Stashed: false", the working tree was already clean. The key decision point: if the output does NOT contain "false", Stage 5 Cleanup must pop/reset.

**Save this value** -- it determines whether Stage 5 Cleanup needs to pop the stash.

### 4.2 Clean Up Stale Worktrees

Remove any leftover worktrees from a previous aborted run:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py cleanup-worktrees \
  --project-root=.
```

### 4.3 Generate Fix Plan

Cluster findings into fix groups, assign waves, and evaluate blast radius:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py cluster-and-plan \
  --findings-path=.nit-supreme/findings.json \
  --output-path=.nit-supreme/fix-plan.json \
  --project-root=.
```

The cluster-and-plan command now uses module-level grouping with tiered model selection:
- **Auto-tier** findings (already fixed by ruff): excluded from plan
- **Mechanical-tier** findings: bundled into a single group with `model: "haiku"`
- **Substantive-tier** findings: grouped per-module with `model: "sonnet"`
- **Architectural-tier** findings: excluded from plan (report-only, per TIER-03)

Read `.nit-supreme/fix-plan.json` and note: the number of groups, total waves, and the model field on each group.

Apply auto-escalation from memory -- categories with historically high failure rates get requires_decision set automatically:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py apply-escalations \
  --fix-plan-path=.nit-supreme/fix-plan.json \
  --findings-path=.nit-supreme/findings.json \
  --context-path=.nit-supreme/context.json
```

### 4.4 Dispatch Fix-Planner Agent for Validation

**Skip gate (PERF-03):** Before dispatching the fix-planner agent, check if the deterministic plan is simple enough to use directly:

Read `.nit-supreme/fix-plan.json`:
- Count the number of groups in the `groups` array
- For each group, count the number of files in its `files` array

If groups <= 10 AND every group has files <= 3:
  Print: "fix-planner skipped: <=10 groups, all <=3 files"
  Skip fix-planner dispatch. Use the orchestrator-generated plan as-is.
  Proceed to Stage 4.5 (Fix Selection Menu).

Otherwise, check if the fix-planner agent definition exists:

```
ls ~/.claude/agents/nps-fix-planner.md
```

If the file exists, dispatch the fix-planner agent to validate the plan, assess "introduces new patterns" for each group, and update fix-plan.json:

- `Agent(subagent_type="nps-fix-planner", prompt="Validate and refine the fix plan at .nit-supreme/fix-plan.json. Read .nit-supreme/context.json for project context and .nit-supreme/findings.json for the findings. Assess each group for 'introduces new patterns' and update requires_decision accordingly. Write the validated plan back to .nit-supreme/fix-plan.json.")`

If the agent definition is not found, skip this step with a warning: "Skipping nps-fix-planner: agent definition not found. Using orchestrator-generated plan as-is."

### 4.5 Fix Selection Menu

If `--auto-approve` IS set: skip the menu entirely. Fix all groups where `requires_decision: false`. Skip all `requires_decision: true` groups -- set their `user_decision` to `"skip"` in fix-plan.json so Stage 6 can distinguish the reason (they will appear as "skipped" in the report with reason "auto-approve bypassed decision group"). Jump to Stage 5.

If `--auto-approve` is NOT set:

Generate the fix selection menu text:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py format-fix-interaction \
  --fix-plan-path=.nit-supreme/fix-plan.json \
  --findings-path=.nit-supreme/findings.json \
  --mode=menu
```

Present the menu to the user via AskUserQuestion with the output from format-fix-interaction.

Handle the user's response:

**Option 1 ("Fix all auto-fixable" or "1"):**
- Fix all groups where requires_decision is false
- Skip all requires_decision groups (mark user_decision="skip" in fix-plan.json)
- Proceed to Stage 5

**Option 2 ("Fix all" or "2"):**
- If there are requires_decision groups: proceed to Stage 4.6 (Decision Walkthrough)
- If no requires_decision groups: fix all groups, proceed to Stage 5

**Option 3 ("Select by category" or "3"):**
- Generate category selection text:
  ```
  python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py format-fix-interaction \
    --fix-plan-path=.nit-supreme/fix-plan.json \
    --findings-path=.nit-supreme/findings.json \
    --mode=category
  ```
- Present category list via AskUserQuestion
- Parse user's comma-separated numbers or "all"
- Map selected categories to finding IDs, then to fix groups containing those findings
- Fix only groups that contain at least one finding in a selected category
- Mark unselected groups with user_decision="skip" in fix-plan.json
- Proceed to Stage 5

**Option 4 ("Skip fixes" or "4"):**
- Skip the entire fix pipeline (Stage 5)
- Mark all groups as user_decision="skip" in fix-plan.json
- Jump to Stage 6 (Report Update)

### 4.6 Decision Walkthrough

Only reached when the user selected Option 2 ("Fix all") and there are requires_decision groups.

Generate the walkthrough text:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py format-fix-interaction \
  --fix-plan-path=.nit-supreme/fix-plan.json \
  --findings-path=.nit-supreme/findings.json \
  --mode=walkthrough
```

For each decision group in the walkthrough output (up to 10 groups):

Present the group's context via AskUserQuestion with the group text block.

Handle the user's response:
- **"1" or "Approve":** Set user_decision="approve" for this group. Continue to next group.
- **"2" or "Skip":** Set user_decision="skip" for this group. Continue to next group.
- **"3" or "Stop":** Set user_decision="skip" for this and ALL remaining decision groups. Exit walkthrough.

After the walkthrough completes, update fix-plan.json with user_decision values for all groups.

Groups with user_decision="approve" will be fixed in Stage 5.
Groups with user_decision="skip" will be skipped in Stage 5 and listed in the Skipped section of the final report.

### 4.7 Record Dismissals to Memory

If any groups were skipped or dismissed, record to false positive registry:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py record-dismissals \
  --fix-plan-path=.nit-supreme/fix-plan.json \
  --findings-path=.nit-supreme/findings.json \
  --context-path=.nit-supreme/context.json
```

This records each dismissed finding to the memory system's false-positives layer, enabling future confidence adjustment for repeatedly-dismissed categories.

Save checkpoint:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py save-checkpoint \
  --output-dir=.nit-supreme \
  --stage=4 \
  --completed-stages=1,1.5,1.7,2,3,4 \
  --engine-results='{engine_results_json}' \
  --flags='{flags_json}' \
  --preset={preset} \
  --context-hash={context_hash}
```

## Stage 5 -- Fix Execution

If `--fix` is NOT enabled, skip directly to Stage 6.

**CRITICAL SAFETY RULE:** If ANY step in Stage 5 fails or errors, STILL execute the "Stage 5 Cleanup (Always Runs)" section below before reporting the error. The stash-pop is unconditional cleanup -- user's uncommitted work must be restored regardless of pipeline outcome.

### 5.1 Read the Fix Plan

Read `.nit-supreme/fix-plan.json` and parse the groups and total_waves.

Initialize tracking variables:
- `all_merged_groups`: list of group IDs successfully merged (across all waves)
- `all_group_results`: list of result dicts for each group
- `merge_shas`: dict mapping group_id to merge commit SHA

### 5.2 Execute Waves

For each wave (1 through total_waves):

#### 5.2.1 Filter Groups for This Wave

Select all groups where `wave == current_wave`.

#### 5.2.2 Create Worktrees

For each group in this wave, create an isolated worktree:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py create-worktree \
  --project-root=. \
  --group-id={group_id}
```

The command prints the worktree path. Record it for the fix-engine dispatch.

#### 5.2.3 Dispatch Fix-Engine Agents in Parallel

Check if the fix-engine agent definition exists:

```
ls ~/.claude/agents/nps-fix-engine.md
```

If found, read `.nit-supreme/baseline.json` and check the `status` field before dispatching.

**Model-aware dispatch (Phase 20):** For each group in this wave, check the `model` field in fix-plan.json:

- If `model == "haiku"`: Use `Agent(subagent_type="nps-fix-engine-haiku", prompt="...")`
- If `model == "sonnet"` (or absent): Use `Agent(subagent_type="nps-fix-engine", prompt="...")` (existing behavior)

This ensures mechanical-tier fixes use the cheaper Haiku model while substantive fixes use Sonnet.

**If `status` is `"no_test_runner"`:** Dispatch fix-engine agents with a modified prompt that skips test verification. For each group in the wave, select the agent type based on the group's model field:
- Haiku groups: `Agent(subagent_type="nps-fix-engine-haiku", prompt="Fix group {group_id}. Worktree path: {worktree_path}. Findings: {JSON of findings for this group from findings.json, filtered by finding_ids}. No test framework detected in this project. Apply the fixes and verify the code compiles/parses correctly, but skip test execution. Write results to .nit-supreme/engine-output/fix-{group_id}.json")`
- Sonnet groups: `Agent(subagent_type="nps-fix-engine", prompt="Fix group {group_id}. Worktree path: {worktree_path}. Findings: {JSON of findings for this group from findings.json, filtered by finding_ids}. No test framework detected in this project. Apply the fixes and verify the code compiles/parses correctly, but skip test execution. Write results to .nit-supreme/engine-output/fix-{group_id}.json")`

**If `status` is `"ok"`:** Dispatch ALL fix-engine agents for this wave in a SINGLE message for parallel execution with the full prompt including test verification. For each group in the wave, select the agent type based on the group's model field:
- Haiku groups: `Agent(subagent_type="nps-fix-engine-haiku", prompt="Fix group {group_id}. Worktree path: {worktree_path}. Findings: {JSON of findings for this group from findings.json, filtered by finding_ids}. Test command: {test_cmd from context.json}. Write results to .nit-supreme/engine-output/fix-{group_id}.json")`
- Sonnet groups: `Agent(subagent_type="nps-fix-engine", prompt="Fix group {group_id}. Worktree path: {worktree_path}. Findings: {JSON of findings for this group from findings.json, filtered by finding_ids}. Test command: {test_cmd from context.json}. Write results to .nit-supreme/engine-output/fix-{group_id}.json")`

Issue all Agent calls in ONE message so they execute in parallel.

If the agent definition is not found, skip fix execution with a warning.

#### 5.2.4 Collect Results and Merge

After all agents complete for this wave, process results in group-ID sorted order:

For each group in sorted order by group_id:
1. Read `.nit-supreme/engine-output/fix-{group_id}.json`
2. Record the result in all_group_results
3. If status is "pass":
   ```
   python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py merge-branch \
     --project-root=. \
     --group-id={group_id}
   ```
   - If merge result status is "merged": add group_id to all_merged_groups. Parse the JSON output from merge-branch -- if it contains `"merge_sha"`, record `merge_shas[group_id] = merge_sha`.
   - If merge result status is "conflict": record as conflict, continue with next group
4. If status is "fail", "skipped", or "manual": log and continue (do NOT merge)

#### 5.2.5 Clean Up Wave Worktrees

After merging, remove worktrees for this wave:

For each group in this wave:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py remove-worktree \
  --project-root=. \
  --group-id={group_id}
```

### 5.3 Final Regression Check

After all waves complete, read `.nit-supreme/baseline.json` and check the `status` field.

**If `status` is `"no_test_runner"`:** Skip the regression check entirely. Print: "Skipping regression check: no test runner configured". Jump to Stage 5.5.

**Otherwise**, run the test suite again to check for regressions:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py capture-baseline \
  --project-root=. \
  --test-cmd={test_cmd} \
  --output-path=.nit-supreme/final-test-state.json
```

Compare the final test state against the pre-fix baseline. Use inline Python to detect regressions:

```
python -c "
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path.home() / '.claude/skills/nit-pick-supreme'))
from scripts.orchestrator import detect_regressions
baseline = json.loads(pathlib.Path('.nit-supreme/baseline.json').read_text())
current = json.loads(pathlib.Path('.nit-supreme/final-test-state.json').read_text())
regressions = detect_regressions(baseline, current)
if regressions:
    print(f'REGRESSIONS DETECTED: {len(regressions)} new failures')
    for r in regressions:
        print(f'  - {r}')
else:
    print('No regressions detected')
print(json.dumps(regressions))
"
```

### 5.4 Isolation Loop (If Regressions)

Read `.nit-supreme/baseline.json` and check the `status` field.

**If `status` is `"no_test_runner"`:** Skip the isolation loop entirely. Print: "Skipping isolation loop: no test runner configured". Jump to Stage 5.5.

**Otherwise**, if regressions were detected:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py run-isolation \
  --project-root=. \
  --merged-groups={comma-separated all_merged_groups} \
  --test-cmd={test_cmd} \
  --baseline-path=.nit-supreme/baseline.json \
  --merge-shas='{JSON string of merge_shas dict}'
```

Record the causal groups identified.

### 5.5 Write Fix Results

Collect all results into fix-results.json:

```
python -c "
import json, pathlib
results = {
    'groups': [],
    'baseline': json.loads(pathlib.Path('.nit-supreme/baseline.json').read_text()),
    'regressions': [],
    'stash_applied': False
}
# Read results from all group output files
import glob
for f in sorted(glob.glob('.nit-supreme/engine-output/fix-*.json')):
    results['groups'].append(json.loads(pathlib.Path(f).read_text()))
pathlib.Path('.nit-supreme/fix-results.json').write_text(
    json.dumps(results, indent=2)
)
print(f'Fix results: {len(results[\"groups\"])} groups')
"
```

### 5.6 Record Fix Outcomes to Memory

After fix results are written, record outcomes to memory:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py record-fix-outcomes \
  --project-root=. \
  --fix-results-path=.nit-supreme/fix-results.json \
  --findings-path=.nit-supreme/findings.json \
  --context-path=.nit-supreme/context.json
```

This records successful fix patterns and failures to the memory system, enabling future confidence adjustment and fix strategy recommendations.

## Stage 5 Cleanup (Always Runs)

**This section MUST execute even if Stage 5 encounters errors. It restores the user's stashed uncommitted changes.**

If the stash-push output from Stage 4.1 indicated "Stashed: true" (either stash or temp_commit), pop/reset to restore the user's uncommitted changes:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py stash-pop \
  --project-root=.
```

If stash-pop fails (e.g., conflicts between fixes and user's uncommitted changes), warn the user: "Fix pipeline completed but your uncommitted changes conflict with applied fixes. Run `git stash show` to inspect and resolve manually."

Regardless of stash-pop success or failure, the fix pipeline is complete. Proceed to Stage 6.

Save checkpoint:
```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py save-checkpoint \
  --output-dir=.nit-supreme \
  --stage=5 \
  --completed-stages=1,1.5,1.7,2,3,4,5 \
  --engine-results='{engine_results_json}' \
  --flags='{flags_json}' \
  --preset={preset} \
  --context-hash={context_hash}
```

## Stage 6 -- Report Update

Calculate the pipeline duration in seconds from the start time recorded in Stage 1.

Collect skipped groups for the report. Build a JSON array of skipped group info:
```
python -c "
import json, pathlib
plan = json.loads(pathlib.Path('.nit-supreme/fix-plan.json').read_text())
skipped = []
for g in plan.get('groups', []):
    if g.get('user_decision') == 'skip':
        # Determine reason: requires_decision groups skipped under --auto-approve
        # have no explicit user interaction; all others were user-skipped
        if g.get('requires_decision', False):
            reason = 'auto-approve bypassed decision group'
        else:
            reason = 'user skipped'
        skipped.append({
            'group_id': g['group_id'],
            'files': g['files'],
            'file_count': len(g['files']),
            'reason': reason,
        })
print(json.dumps(skipped))
"
```

Update the existing preliminary REVIEW.md with fix results:

```
python ~/.claude/skills/nit-pick-supreme/scripts/orchestrator.py update-review \
  --review-path=.nit-supreme/REVIEW.md \
  --findings-path=.nit-supreme/findings.json \
  {--fix-results-path=.nit-supreme/fix-results.json if --fix was enabled and file exists} \
  {--explorer-meta-path=.nit-supreme/explorer-meta.json if explorer was enabled and file exists} \
  {--skipped-groups-json='{skipped_json}' if skipped groups exist}
```

If --fix was NOT enabled (report-only mode), the update call still works -- it just won't have fix-results or skipped groups, and the preliminary report is the final report.

### Terminal Summary

After writing REVIEW.md, generate and print the terminal summary. Use the orchestrator to produce a compact severity count line:

```
python -c "
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path.home() / '.claude/skills/nit-pick-supreme'))
from scripts.orchestrator import generate_terminal_summary
from scripts.nps_schema import Finding
data = json.loads(pathlib.Path('.nit-supreme/findings.json').read_text())
findings = [Finding.model_validate(f) for f in data.get('findings', [])]
manifest_path = pathlib.Path('.nit-supreme/autofix-manifest.json')
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else None
print(generate_terminal_summary(findings, '.nit-supreme/REVIEW.md', autofix_manifest=manifest))
"
```

Print the terminal summary output to the user. This is the final user-facing output of the pipeline.

### Pipeline Complete

Delete the checkpoint file since the pipeline completed successfully:
```
rm -f .nit-supreme/checkpoint.json
```

## Error Handling

Throughout the pipeline:

- **If any Bash command fails:** Log the error message, continue the pipeline with partial results. Do not abort.
- **If any Agent call fails or times out:** Record the engine as status `error` or `timeout` in the engine output directory. Continue with other engines.
- **If context discovery fails:** Log error and stop -- context is required for all subsequent stages.
- **If synthesis fails:** Log error, attempt to generate a minimal report noting the failure.
- **The final report is ALWAYS generated**, even with partial results. A report with 0 findings from 1 engine is still valuable -- it proves the engine ran and found nothing.

## Cleanup

The `.nit-supreme/` directory persists between runs for debugging. To clean up:
```
rm -rf .nit-supreme/
```

## GSD Integration Hooks

nit-pick-supreme integrates with GSD workflow hooks. When configured in a target project's CLAUDE.md, GSD commands automatically trigger code reviews at key workflow points:

### Post-Phase Execution (zero LLM cost)
- **When:** After each GSD phase execution completes
- **Trigger:** `/nit-pick-supreme --quick`
- **Effect:** Static sweep only -- catches dead imports, secrets, truncation instantly with zero LLM cost
- **GSD hook:** `gsd:post-phase-execution`

### Pre-Verification
- **When:** Before the GSD verification step
- **Trigger:** `/nit-pick-supreme --standard`
- **Effect:** Static + code agents + E2E + fix pipeline -- comprehensive review before verifying
- **GSD hook:** `gsd:pre-verification`

### Pre-Ship (full review)
- **When:** Before shipping or deploying
- **Trigger:** `/nit-pick-supreme --deep`
- **Effect:** All engines including architecture agents and AI explorer -- maximum coverage before ship
- **GSD hook:** `gsd:ship`

### Setup for Target Projects

To enable GSD integration, add this to the target project's CLAUDE.md:

```markdown
## Code Review Integration

After completing phase work, run a quick static check:
/nit-pick-supreme --quick

Before verification, run a standard review:
/nit-pick-supreme --standard

Before shipping, run a deep review:
/nit-pick-supreme --deep
```
