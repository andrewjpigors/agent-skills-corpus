---
name: hmos-convert-pipeline
description: "Run the Android-to-HarmonyOS conversion pipeline — all agents in sequence with progress, duration, and defect tracking. Trigger phrases include 'full Android-to-HarmonyOS pipeline', 'run the conversion pipeline end-to-end', 'hmos-convert-pipeline', 'HarmonyOS conversion', or any request to convert an Android project to HarmonyOS with all stages (logic → build → review → fix → rebuild → self-test loop)."
---

# Full Conversion Pipeline

Run all conversion agents in sequence, passing outputs between stages and recording cumulative progress after each step.

**Raw arguments**: $ARGUMENTS

---

## Argument Parsing

Parse `$ARGUMENTS` as positional tokens:

- **Arg 1** (`android_project_dir`): Path to the Android source project (required)
- **Arg 2** (`harmony_project_dir`): Path to the target HarmonyOS project directory (required)
- **Arg 3** (`spec_file_path`): Path to the requirement spec document (required). This is the plan/spec that drives Stage 1 logic development and Stage 3 code review — both stages read it directly from this path.
- **Arg 4** (`assets_output_path`): Directory to store all output/report files (optional). When omitted, default to `<harmony_project_dir>/.hometrans` — create the directory if it does not exist.
- **Arg 5** (`test_case_path`): Path to the self-test case file driving the Stage 4 self-testing loop (optional). When omitted, default to `OUTPUT/test_case.md`. If the resolved file does not exist, the Stage 4 loop is skipped (see Loop Setup).
- **Arg 6** (`pre_test_case_path`): Path to the pre-test case file (optional). When omitted, default to `OUTPUT/pre_test_case.md`. Only passed to the self-tester when the resolved file exists.
- **Arg 7** (`max_rounds_review`): Maximum number of Stage 3→3a→3b code-review-fix rounds to run (optional, default `2`). Must be a positive integer `>= 1`.
- **Arg 8** (`max_rounds_test`): Maximum number of Stage 4→4a→4b self-test rounds to run (optional, default `2`). Must be a positive integer `>= 1`.
- **Arg 9** (`skip_test`): `true` or `false` (optional, default `false`). When `true`, skip Stage 4 / 4a / 4b (Self-Testing Loop) entirely. Use this when no real HarmonyOS device is available for on-device testing.

Args are positional: to pass any optional arg, provide explicit values for all optional args before it (e.g., passing `test_case_path` requires an explicit `assets_output_path`; passing `skip_test` requires explicit Args 4–8).

If any required argument is missing, ask the user before proceeding. If `spec_file_path` does not exist or is not a readable file, ask the user before proceeding. If `max_rounds_review` or `max_rounds_test` is provided but is not a positive integer, ask the user before proceeding. If `skip_test` is provided but is not `true` or `false`, ask the user before proceeding.

Define shorthand variables for the instructions below:

| Variable | Meaning |
|----------|---------|
| `ANDROID` | android_project_dir |
| `HMOS` | harmony_project_dir |
| `SPEC` | spec_file_path — requirement spec document, consumed directly by Stage 1 (`spec_file`) and Stage 3 (`test_case_path`) |
| `OUTPUT` | assets_output_path; defaults to `HMOS/.hometrans` when not provided (created on demand) |
| `TEST_CASE` | test_case_path; defaults to `OUTPUT/test_case.md` when not provided |
| `PRE_TEST_CASE` | pre_test_case_path; defaults to `OUTPUT/pre_test_case.md` when not provided |
| `MAX_ROUNDS_REVIEW` | max_rounds_review — positive integer (default `2`). Controls Stage 3→3a→3b code-review-fix loop. |
| `MAX_ROUNDS_TEST`   | max_rounds_test — positive integer (default `2`). Controls Stage 4→4a→4b self-test loop. |
| `SKIP_TEST` | skip_test — `true` or `false` (default `false`). When `true`, skip Stage 4 / 4a / 4b entirely (no real device available). |

---

## Environment Variables Check (run before Stage 1)

The pipeline's sub-agents read their settings **directly from the OS environment variables**. Verify upfront so the long pipeline fails fast (read each from the OS environment: `echo "$VAR"` on macOS/Linux; `$env:VAR` in PowerShell on Windows):

| Variable | Needed for | Valid when |
|---|---|---|
| `DEVECO_HOME` *(or `DEVECO_SDK_HOME`)* | Stage 2 build + Stage 3a/4b rebuilds | resolves to a valid DevEco install |
| `TEST_API_KEY` | Stage 4 self-test (only when `SKIP_TEST=false`) | non-empty |
| `HOMETRANS_TOOL_PATH` | Stage 4 self-test AutoTest dir; defaults to `~/.hometrans/tools` | path exists on disk |

If `DEVECO_HOME`/`DEVECO_SDK_HOME` is missing, **ask the user** for the DevEco Studio install path before starting. When `SKIP_TEST=false`, also require `TEST_API_KEY` — if missing, **ask the user** for it (or have them pass `skip_test=true`). Suggest running `ht init` to persist these as machine environment variables.

---

## Progress Tracking

Before any agent runs, create tasks for all pipeline stages listed below so the user sees the full plan immediately. Stages are sequential — each stage depends on the previous one completing first. For the Stage 3 and Stage 4 loops, create one umbrella task per sub-stage (3 / 3a / 3b and 4 / 4a / 4b) covering the full multi-round cycle rather than creating per-round tasks. If `SKIP_TEST == true`, still create Stage 4 / 4a / 4b tasks but mark them as completed immediately with a "Skipped" note.

| # | subject | activeForm |
|---|---------|------------|
| 1 | Logic Development (Context Builder) | Building logic decision contract |
| 1a | Logic Coding | Converting business logic to ArkTS |
| 2 | Compilation and Build | Building HarmonyOS project |
| 3 | Code Review | Reviewing HarmonyOS code quality |
| 3a | Review Fix | Fixing code review issues |
| 3b | Rebuild after Review Fix | Rebuilding after review fixes |
| 4 | Self-Testing | Running on-device tests |
| 4a | Self-Test Fix | Fixing self-test failures |
| 4b | Rebuild after Self-Test Fix | Rebuilding after self-test fixes |

For each stage: mark `in_progress` before launching the agent, then `completed` after it finishes (update description with actual output files and key stats). If a stage fails, still mark `completed` so the next stage unblocks — include the failure details in the description.

### Stage Duration Tracking

For every stage (including each Stage 3 / 3a / 3b review round and each Stage 4 / 4a / 4b test round), capture wall-clock duration:

1. Just before marking a stage `in_progress`, record `stage_start_iso` using the current local time (e.g., run `date -Iseconds` via Bash, or capture a timestamp in ISO-8601 `YYYY-MM-DDTHH:MM:SS` form).
2. Just after the stage's agent returns, record `stage_end_iso` the same way.
3. Compute `duration_seconds = stage_end_iso - stage_start_iso` and format as `H:MM:SS` (hours, minutes, seconds).
4. Record `start`, `end`, and `duration` in the manifest's **Duration Summary** table (see format below). For Stage 3 review loop rounds, record one row per execution using labels like `3 - Code Review (Round 1)`, etc. For Stage 4 test loop rounds, use labels like `4 - Self-Testing (Round 1)`, etc.

For the Stage 3 review loop:
- Mark Stage 3 `in_progress` when Round 1 starts, and keep it `in_progress` until the full review loop exits.
- Mark Stage 3a `in_progress` when the first Stage 3a round starts, and Stage 3b `in_progress` when the first Stage 3b round starts.
- Append brief per-round summaries into the Stage 3 / 3a / 3b task descriptions.
- Only mark Stage 3 / 3a / 3b `completed` after the review loop finishes (either `all_passed`, `no_confirmed_defects`, or `max_rounds_reached`).

For the Stage 4 test loop:
- Mark Stage 4 `in_progress` when Round 1 starts, and keep it `in_progress` until the full test loop exits.
- Mark Stage 4a `in_progress` when the first Stage 4a round starts, and Stage 4b `in_progress` when the first Stage 4b round starts.
- Append brief per-round summaries into the Stage 4 / 4a / 4b task descriptions.
- Only mark Stage 4 / 4a / 4b `completed` after the test loop finishes (either `all_passed`, `no_confirmed_defects`, or `max_rounds_reached`).

Also maintain a manifest file at **`OUTPUT/pipeline-manifest.md`** — update it after every stage with status, per-stage start/end timestamps, wall-clock duration, and a cumulative inventory of all output files (documents, generated code, build artifacts, reports).

### Manifest duration format

In `OUTPUT/pipeline-manifest.md`, include a **Duration Summary** table:

```markdown
## Duration Summary

| Stage | Start | End | Duration (H:MM:SS) |
|-------|-------|-----|--------------------|
| 1 - Logic Development (Context Builder) | 2026-04-20T10:00:00 | 2026-04-20T10:05:12 | 0:05:12 |
| 1a - Logic Coding | ... | ... | ... |
| ... | ... | ... | ... |
| **TOTAL** | first start | last end | **H:MM:SS** |
```

---

## Defect Tracking

After each **review**, **fix**, or **test** stage completes, read the corresponding report file from `OUTPUT` and extract defect statistics. Record these in the manifest's **Defect Summary** table.

### Extraction rules per stage

| Stage | Report File | What to Extract |
|-------|-------------|-----------------|
| **3 — Code Review** | `review-round-N/code-review-report.md` | From the **Overview** section, extract `Total Scenarios` and the verdict breakdown: `PASS`, `PARTIAL`, `FAIL`, `UNABLE TO VERIFY` counts. **Defects found** = count of `FAIL` + `PARTIAL` verdicts. Also note the **Overall Verdict** (`PASS` / `PASS WITH ISSUES` / `NEEDS REWORK`). Record one row per review round. |
| **3a — Review Fix** | `review-round-N/review-fix-report.md` | From the **Overview** section, extract: `Total Issues in Report`, `Verified (CONFIRMED)`, `False Positives`, `Successfully Fixed`, `Failed to Fix`, `Fix Success Rate`. **Defects fixed** = `Successfully Fixed`. **Defects not fixed** = `Failed to Fix`. Use this to populate the same review round row as Stage 3. |
| **4 — Self-Testing** | `round-N/self-test-report.md` | From the **测试概览** or **测试总结** section, extract: `总用例数` (total cases), `通过` (passed), `失败` (failed), `通过率` (pass rate). **Defects found** = `失败` count. Record one row per round. |
| **4a — Self-Test Fix** | `round-N/self-test-fix-report.md` | From the **概览** section, extract: `报告中失败 scenario 总数` (total failed), `白盒确认问题存在` (confirmed), `白盒判定为误报` (false positives), `修复成功` (fixed), `修复失败` (failed to fix). **Defects fixed** = `修复成功`. **Defects not fixed** = `修复失败`. Use this to populate the same round row as Stage 4. |

### How to extract

After the agent completes and writes the report file, read the report and search for the key fields listed above. The values are typically in the first few sections of each report. If a field is missing or the report format is unexpected, record `N/A` for that field and add a note.

### Manifest defect format

In `OUTPUT/pipeline-manifest.md`, include a **Defect Summary** table after the Duration Summary:

```markdown
## Defect Summary

| Stage | Report File | Defects Found | Defects Fixed | Not Fixed | Details |
|-------|-------------|---------------|---------------|-----------|---------|
| 3 Loop - Round 1 | review-round-1/code-review-report.md + review-round-1/review-fix-report.md | X (Y FAIL + Z PARTIAL) | D fixed | E not fixed | Overall: PASS WITH ISSUES; confirmed=B; false positives=C; rebuild=SUCCESS |
| 3 Loop - Round 2 | review-round-2/code-review-report.md + review-round-2/review-fix-report.md | X (Y FAIL + Z PARTIAL) | D fixed | E not fixed | Overall: PASS; stop=all_passed |
| 3 Loop - Summary | review-round-*/... | Total found across rounds | Total fixed across rounds | Remaining in final round | Rounds executed: N / MAX_ROUNDS_REVIEW; stop reason: all_passed/no_confirmed_defects/max_rounds_reached |
| 4 Loop - Round 1 | round-1/self-test-report.md + round-1/self-test-fix-report.md | X failed / Y total | C | D | Pass rate: ZZ%; confirmed=B; false positives=F; rebuild=SUCCESS |
| 4 Loop - Round 2 | round-2/self-test-report.md + round-2/self-test-fix-report.md | X failed / Y total | C | D | Pass rate: ZZ%; confirmed=B; false positives=F; rebuild=SUCCESS; stop=all_passed |
| 4 Loop - Summary | round-*/... | Total found across rounds | Total fixed across rounds | Remaining in final round | Rounds executed: N / MAX_ROUNDS_TEST; stop reason: all_passed/max_rounds_reached |
```

For stages that are not review/fix/test (Stages 1–2), no row is needed in this table.
For the Stage 3 loop, combine review and fix results into one row per round plus one summary row.
For the Stage 4 loop, combine test and fix results into one row per round plus one summary row.

---

## Pipeline Execution

### Stage 1 — Logic Development (Context Builder)

Flags: `skip-plan-builder: true|false` (default `false`) — when `true`, skip this stage and reuse an existing `OUTPUT/logic/plan.md`.

Prompt format (applies to both Stage 1 and Stage 1a): ONLY the key-value lines below. No natural language, step lists, or Markdown.

1. Launch the logic context builder agent:
   ```
   Agent(
     subagent_type="logic-context-builder",
     prompt="harmony_project_dir: HMOS\nspec_file: SPEC\noutput_path: OUTPUT/logic"
   )
   ```
2. Verify `OUTPUT/logic/plan.md` exists.

### Stage 1a — Logic Coding

1. Launch the logic coding agent:
   ```
   Agent(
     subagent_type="logic-coder",
     prompt="harmony_project_dir: HMOS\nplan_file: OUTPUT/logic/plan.md\noutput_path: OUTPUT/logic"
   )
   ```
2. Copy `OUTPUT/logic/commit-info.md` → `OUTPUT/commit-info.md` and verify it contains a hex `commit_id`.
3. `OUTPUT/logic/coding-summary.md` is human-readable auxiliary; downstream stages consume only `OUTPUT/commit-info.md`.

### Stage 2 — Compilation and Build

1. Launch the **build-fixer** agent with `--signed`.
2. Input: `harmony_project_dir`: `HMOS`, `output_path`: `OUTPUT`.
3. The agent runs the build-fix loop (up to 20 iterations), writes `build-fix-report.md` into `OUTPUT`.
4. If the build succeeds, the signed `.hap` is copied to `OUTPUT`. Note its location in the manifest.
5. After the agent completes, read `OUTPUT/build-fix-commit-info.md` and note the commit ID (may be a real hash or `none`). 

### Stage 3 — Code Review Loop (Review → Fix → Rebuild)

Treat Stage 3 → 3a → 3b as a loop that runs up to `MAX_ROUNDS_REVIEW` times.

#### Review Loop Setup

1. **Resolve the initial commit ID for code review** using the following priority:
   - Read `OUTPUT/commit-info.md` (written by Stage 1). If `commit_id` is a real hash, use it.
   - IMPORTANT: Use `commit-info.md` from Stage 1, NOT `build-fix-commit-info.md` from Stage 2. The first review must target the logic-dev commit, not the build-fix commit.
   - If neither file exists or both have `commit_id: none`, the code-reviewer agent will review the project holistically without commit-scoped extraction.
   - Store this as `REVIEW_COMMIT_ID`.
2. Initialize loop state:
   - `review_round = 1`
   - `review_rounds_executed = 0`
   - `review_stop_reason = none`
3. Mark Stage 3 `in_progress` when Round 1 begins. Keep Stage 3 / 3a / 3b tasks open until the full loop exits.

#### Per-Round Stage 3 / 3a / 3b Execution Order

For each `review_round` from `1..MAX_ROUNDS_REVIEW`, set `REVIEW_ROUND_DIR = OUTPUT/review-round-{review_round}` and execute the following three steps in order:

##### Review Round Step A — Stage 3 Code Review

1. Launch the **code-reviewer** agent.
2. Input:
   - `harmony_project_dir`: `HMOS`
   - `commit_id`: For Round 1, use `REVIEW_COMMIT_ID`. For Round 2+, review the project holistically (omit `commit_id` or pass `none`) since fixes have modified the codebase beyond the original commit scope.
   - `output_path`: `REVIEW_ROUND_DIR`
   - `test_case_path`: `SPEC`
3. If a valid `commit_id` is available, the agent will automatically call the `extract_commit_context` MCP tool to extract commit-scoped code context before reviewing. If the MCP call fails, the agent falls back to direct git-diff analysis. If no `commit_id` is available, the agent reviews the project holistically without commit-scoped extraction.
4. The agent writes `REVIEW_ROUND_DIR/code-review-report.md` with per-scenario verdicts.
5. **Extract defect stats**: Read `REVIEW_ROUND_DIR/code-review-report.md`, extract the verdict breakdown (PASS/PARTIAL/FAIL/UNABLE TO VERIFY counts) and overall verdict.
6. Compute `review_all_passed`:
   - `true` if the overall verdict is `PASS` and there are zero `FAIL` or `PARTIAL` verdicts.
   - `false` otherwise.
   If the report is missing or malformed, do **not** treat the round as passed.
7. If `review_all_passed == true`, set `review_stop_reason = all_passed`, skip Stage 3a and 3b for this round, and exit the loop.
8. Update the Stage 3 task description with a brief round summary (for example: `Round 1: 8 PASS, 2 PARTIAL, 1 FAIL`).

##### Review Round Step B — Stage 3a Review Fix

1. Mark Stage 3a `in_progress` when the first Stage 3a round begins.
2. Launch the **review-fixer** agent.
3. Input:
   - `review_report_path`: `REVIEW_ROUND_DIR/code-review-report.md`
   - `harmony_project_dir`: `HMOS`
   - `android_project_dir`: `ANDROID`
   - `output_path`: `REVIEW_ROUND_DIR`
4. The agent verifies each issue from the code review report, fixes confirmed issues, and writes `REVIEW_ROUND_DIR/review-fix-report.md`.
5. **Extract defect stats**: Read `REVIEW_ROUND_DIR/review-fix-report.md`, extract total issues, confirmed, false positives, successfully fixed, failed to fix, and fix success rate.
6. Compute `review_no_confirmed_defects`:
   - `true` if the fix report exists AND confirmed issues == 0 (all reported issues are false positives).
   - `false` otherwise.
7. Update the Stage 3a task description with a brief round summary (for example: `Round 1: confirmed=3, fixed=2, failed=1`).

##### Review Round Step C — Stage 3b Rebuild after Review Fix

1. Mark Stage 3b `in_progress` when the first Stage 3b round begins.
2. Launch the **build-fixer** agent with `--signed`.
3. Input: `harmony_project_dir`: `HMOS`, `output_path`: `REVIEW_ROUND_DIR`.
4. The agent writes `REVIEW_ROUND_DIR/build-fix-report.md`.
5. If the build succeeds, the signed `.hap` is copied to `REVIEW_ROUND_DIR`. Note its location in the manifest.
6. Append one Defect Summary row for this round by combining the parsed Stage 3 and Stage 3a results into a single row labeled `3 Loop - Round {review_round}`.
7. Update the Stage 3b task description with a brief round summary (for example: `Round 1: build success`).
8. Increment `review_rounds_executed`.
9. **Loop stop decision** (after 3b completes):
    - If `review_no_confirmed_defects == true`, set `review_stop_reason = no_confirmed_defects` and exit the loop. Rationale: all reported issues were judged as false positives by verification, no real defects remain.
    - Else if `review_round == MAX_ROUNDS_REVIEW`, set `review_stop_reason = max_rounds_reached` and exit the loop.
    - Else continue to the next round.

#### Review Loop Finalization

After the review loop exits:

1. Append one Defect Summary row labeled `3 Loop - Summary` with total defects found across rounds, total fixed across rounds, remaining defects in the final round, `review_rounds_executed`, and `review_stop_reason`.
2. Add a short review loop summary in the manifest, including:
   - `Configured max rounds: MAX_ROUNDS_REVIEW`
   - `Rounds executed: review_rounds_executed`
   - `Stop reason: review_stop_reason` — one of: `all_passed` (all scenarios PASS in code review), `no_confirmed_defects` (reported issues all false positives), `max_rounds_reached` (hit the round limit with real defects remaining)
   - `Final round: review-round-{review_rounds_executed}`
3. Mirror the final review round outputs back to the root `OUTPUT` directory using the canonical filenames for backward compatibility:
   - `OUTPUT/code-review-report.md`
   - `OUTPUT/review-fix-report.md` (if 3a ran in the final round)
   - `OUTPUT/build-fix-report.md` (overwrites Stage 2 report, if 3b ran in the final round)
   - If the final round's build produced a signed `.hap`, copy it to `OUTPUT` (replaces Stage 2 `.hap` if present).
4. Mark Stage 3 / 3a / 3b `completed` only after the full loop finishes.

### Stage 3a — Review Fix

Stage 3a is executed as **Review Round Step B** inside the Stage 3 loop above. Do not run Stage 3a outside that loop.

### Stage 3b — Rebuild after Review Fix

Stage 3b is executed as **Review Round Step C** inside the Stage 3 loop above. Do not run Stage 3b outside that loop.

### Stage 4 — Self-Testing Loop (On-Device Verification)

**Skip check**: If `SKIP_TEST == true`, immediately mark Stage 4 / 4a / 4b as `completed` with description "Skipped — skip_test=true (no real device available)". Record a single Duration Summary row with `Duration = SKIPPED`. Add a note in the manifest: `Stage 4 loop skipped by user configuration (skip_test=true)`. Then proceed directly to the **Final Summary**.

Treat Stage 4 → 4a → 4b as a loop that runs up to `MAX_ROUNDS_TEST` times.

#### Loop Setup

1. **Locate the initial HAP file**: Use the `.hap` mirrored to `OUTPUT/` by the Stage 3 review loop finalization (or from Stage 2 if the review loop did not produce one). The default location is `OUTPUT/entry-default-signed.hap`. If that file does not exist, search for `*-signed.hap` files in `OUTPUT/` and use the first match. If no `.hap` is found in `OUTPUT/`, fall back to searching `HMOS/entry/build/default/outputs/default/`.
2. Store the resolved path as `CURRENT_HAP`.
3. **`TEST_CASE` existence guard**: If `TEST_CASE` does not exist, mark Stage 4 / 4a / 4b as failed with note "No test case file available" and skip the loop entirely.
4. Initialize loop state:
   - `round = 1`
   - `rounds_executed = 0`
   - `stop_reason = none`
5. Mark Stage 4 `in_progress` when Round 1 begins. Keep Stage 4 / 4a / 4b tasks open until the full loop exits.

#### Per-Round Stage 4 / 4a / 4b Execution Order

For each `round` from `1..MAX_ROUNDS_TEST`, set `ROUND_DIR = OUTPUT/round-{round}` and execute the following three steps in order:

##### Round Step A — Stage 4 Self-Testing

> ⚠️ **`CURRENT_HAP` must reflect the latest build**: If a previous round's Stage 4b produced a new signed HAP, `CURRENT_HAP` should already point to that HAP (e.g., `round-{N-1}/entry-default-signed.hap`). Do NOT reuse the original HAP from Stage 2/3b in subsequent rounds.

1. If `CURRENT_HAP` is missing, do **not** launch the test. Record this round as Stage 4 failure with note "No HAP file available — build may have failed in Stage 2/3b or a previous 4b round".
2. If `CURRENT_HAP` exists, launch the **self-tester**.
3. Input (round 1):
   - `hap_path`: `CURRENT_HAP`
   - `output_path`: `OUTPUT` (the ROOT — the agent always writes here)
   - `test_case_path`: `TEST_CASE`
   - `pre_test_case_path`: `PRE_TEST_CASE` (only include this line when the file exists)
   - `setup`: `true`
4. Input (round 2+):
   - `hap_path`: `CURRENT_HAP`
   - `output_path`: `OUTPUT` (still the ROOT)
   - `setup`: `false`
5. The agent verifies device connectivity, invokes `self_test_runner.py run` to set up the environment (`uv sync`), install the HAP, and run test cases. **Pre-cases are folded into `OUTPUT/testcases.json` by the agent's S4/S5 step during round 1's `setup: true` invocation; they run first in the same batch — no separate pre-case file or parameter is needed downstream.** The agent writes `OUTPUT/self-test-report.md`, `OUTPUT/task/`, and (round 1 only) `OUTPUT/testcases.json` + `OUTPUT/app-metadata.json` + `OUTPUT/_extracted.json`.
6. After round 1's agent returns, read `OUTPUT/app-metadata.json` and extract `project_root` → `PROJECT_ROOT`. For round 2+, re-read `OUTPUT/app-metadata.json` before invoking the agent; if the previous round's `OUTPUT/round-{round-1}/app-metadata.json` exists (build-fixer may have written one for a relocated project root), the round-dir copy overrides the root copy for this round.
7. Snapshot per-round artifacts to `ROUND_DIR` after the agent returns: copy `OUTPUT/self-test-report.md` → `ROUND_DIR/self-test-report.md`, `OUTPUT/task/` → `ROUND_DIR/task/`, and (round 1 only) `OUTPUT/_extracted.json` → `ROUND_DIR/_extracted.json`. Skip any source that is missing.
8. Read `ROUND_DIR/self-test-report.md` and extract total cases, passed, failed, and pass rate when the report exists.
9. Compute `round_all_passed` only when the report can be parsed clearly and:
   - `总用例数` is known
   - `失败 == 0`
   - `通过 == 总用例数`
   If the report is missing or fields are malformed, do **not** treat the round as passed.
10. Update the Stage 4 task description with a brief round summary (for example: `Round 1: 3/12 failed`).

##### Round Step B — Stage 4a Self-Test Fix

1. Mark Stage 4a `in_progress` when the first Stage 4a round begins.
2. If `ROUND_DIR/self-test-report.md` exists, launch the **self-test-fixer** agent.
3. Input:
   - `self_test_report_path`: `ROUND_DIR/self-test-report.md`
   - `harmony_project_dir`: `HMOS`
   - `android_project_dir`: `ANDROID`
   - `output_path`: `ROUND_DIR`
4. The agent analyzes failed feature points from the self-test report, references Android source for correct behavior, fixes HarmonyOS code, and writes `ROUND_DIR/self-test-fix-report.md`.
5. If `ROUND_DIR/self-test-report.md` is missing, do **not** launch the fixer. Record this round as `Skipped — missing self-test report`.
6. Read `ROUND_DIR/self-test-fix-report.md` when it exists, extract total failed scenarios, confirmed, false positives, successfully fixed, and failed to fix.
7. Compute `round_no_confirmed_defects`:
   - `true` if the fix report exists AND `白盒确认问题存在 == 0` (all failures are false positives, or the report says "No failures to fix — all scenarios passed").
   - `false` otherwise (at least one confirmed defect exists, or the fix report is missing/malformed).
8. Update the Stage 4a task description with a brief round summary (for example: `Round 1: confirmed=3, fixed=2, failed=1`).

##### Round Step C — Stage 4b Rebuild after Self-Test Fix

1. Mark Stage 4b `in_progress` when the first Stage 4b round begins.
2. Launch the **build-fixer** agent with `--signed`.
3. Input: `harmony_project_dir`: `HMOS`, `output_path`: `ROUND_DIR`.
4. The agent writes `ROUND_DIR/build-fix-report.md`.
5. ⚠️ **CRITICAL — Update `CURRENT_HAP` for the next round**: If the build succeeds, the signed `.hap` is copied to `ROUND_DIR`. You **MUST** update `CURRENT_HAP` so that the next round's Stage 4 self-tester uses the newly built HAP (not the original one). Update using this priority:
   - `ROUND_DIR/entry-default-signed.hap`
   - first `ROUND_DIR/*-signed.hap`
   - otherwise keep the previous `CURRENT_HAP` and record that this round did not produce a fresh HAP
6. Append one Defect Summary row for this round by combining the parsed Stage 4 and Stage 4a results into a single row labeled `4 Loop - Round {round}`.
7. Update the Stage 4b task description with a brief round summary (for example: `Round 1: build success, hap=...`).
8. Increment `rounds_executed`.
9. **Loop stop decision** (after 4b completes):
    - If `round_all_passed == true`, set `stop_reason = all_passed` and exit the loop.
    - Else if `round_no_confirmed_defects == true`, set `stop_reason = no_confirmed_defects` and exit the loop. Rationale: all failures were judged as false positives (AutoTest limitations / environment issues) by white-box review, no code was changed, so repeating the test would yield identical results.
    - Else if `round == MAX_ROUNDS_TEST`, set `stop_reason = max_rounds_reached` and exit the loop.
    - Else continue to the next round.

#### Loop Finalization

After the loop exits:

1. Append one Defect Summary row labeled `4 Loop - Summary` with total defects found across rounds, total fixed across rounds, remaining defects in the final round, `rounds_executed`, and `stop_reason`.
2. Add a short Stage 4 loop summary in the manifest, including:
   - `Configured max rounds: MAX_ROUNDS_TEST`
   - `Rounds executed: rounds_executed`
   - `Stop reason: stop_reason` — one of: `all_passed` (all tests green), `no_confirmed_defects` (failures exist but all judged as false positives by white-box review), `max_rounds_reached` (hit the round limit with real defects remaining)
   - `Final round: round-{rounds_executed}`
3. Mirror the final round's `OUTPUT/round-{rounds_executed}/` Fix/Build artifacts back to `OUTPUT/` root using the canonical filenames (the test report and `task/` are already at `OUTPUT/` root as the latest copies — they do NOT need mirroring):
   - `OUTPUT/self-test-fix-report.md` ← `OUTPUT/round-{rounds_executed}/self-test-fix-report.md` (if present)
   - `OUTPUT/build-fix-report.md` ← `OUTPUT/round-{rounds_executed}/build-fix-report.md` (if present)
   - `OUTPUT/self-test-fix-commit-info.md` ← `OUTPUT/round-{rounds_executed}/self-test-fix-commit-info.md` (if present)
   - `OUTPUT/build-fix-commit-info.md` ← `OUTPUT/round-{rounds_executed}/build-fix-commit-info.md` (if present)
   - `OUTPUT/entry-default-signed.hap` ← `CURRENT_HAP` (the final HAP, which lives under `OUTPUT/round-{rounds_executed}/`); skip when `CURRENT_HAP` is already `OUTPUT/entry-default-signed.hap`
   - `OUTPUT/screenshots/` when the final report still references `screenshots/...`
4. When mirroring Fix/Build files back to `OUTPUT`, treat the final round directory as the source of truth and ensure the mirrored root-level reports still reference files that actually exist at the root level.
5. Mark Stage 4 / 4a / 4b `completed` only after the full loop finishes.

### Stage 4a — Self-Test Fix

Stage 4a is executed as **Round Step B** inside the Stage 4 loop above. Do not run Stage 4a outside that loop.

### Stage 4b — Rebuild after Self-Test Fix

Stage 4b is executed as **Round Step C** inside the Stage 4 loop above. Do not run Stage 4b outside that loop.

---

## Error Handling

- If a stage **fails**, log the error in the manifest and task, then **continue to the next stage** unless the loop logic says to continue to the next round.
- Stage 3 uses a bounded Stage 3 → 3a → 3b review loop (up to `MAX_ROUNDS_REVIEW` rounds). Stage 3a addresses issues found by Stage 3, followed by Stage 3b (Rebuild) to ensure compilation. The loop exits when all scenarios pass, all issues are false positives, or `MAX_ROUNDS_REVIEW` is reached.
- If Stage 3a determines that all reported issues are false positives (`confirmed == 0`), the review loop exits after 3b with `review_stop_reason = no_confirmed_defects`.
- Stage 4 uses a bounded Stage 4 → 4a → 4b test loop (up to `MAX_ROUNDS_TEST` rounds). Stage 4a addresses failures found by Stage 4, followed by Stage 4b (Rebuild) to ensure compilation, then the pipeline either continues to the next round or exits the loop based on `all_passed` / `no_confirmed_defects` / `max_rounds_reached`.
- If Stage 4a determines that all failures are false positives (`confirmed == 0`), the test loop exits after 4b with `stop_reason = no_confirmed_defects` — because no code was changed and repeating the test would yield identical results.
- If a Stage 4 round fails before producing `round-N/self-test-report.md`, do not call Stage 4a with a missing report; record the round accordingly and continue to Stage 4b.
- If a Stage 4 report is malformed or required fields are missing, do not treat the round as passed; continue until `MAX_ROUNDS_TEST` is reached or a later round clearly passes.
- If a Stage 4 round passes but the same round's Stage 4b rebuild fails, stop the loop after that round if `round_all_passed == true`, but record clearly that the final rebuild failed and whether the previous `CURRENT_HAP` had to be retained.

---

## Final Summary

After the Stage 4 loop completes (or is skipped), print a concise summary:

1. Overall pipeline status (all green, or which stages had issues)
2. Location of `OUTPUT/pipeline-manifest.md` for full details
3. Stage 3 review loop summary: `MAX_ROUNDS_REVIEW`, `review_rounds_executed`, `review_stop_reason`, final review round directory
4. Stage 4 test loop summary: If `SKIP_TEST == true`, print "Stage 4 skipped (skip_test=true, no real device)". Otherwise print `MAX_ROUNDS_TEST`, `rounds_executed`, `stop_reason`, final round directory.
5. Key statistics: total files generated, self-test results (or "N/A — testing skipped" if `SKIP_TEST == true`)
6. Defect summary: total defects found (code review + testing), total fixed, total remaining unfixed
7. Recommended next steps (if testing was skipped, recommend running on-device tests when a real device becomes available)
