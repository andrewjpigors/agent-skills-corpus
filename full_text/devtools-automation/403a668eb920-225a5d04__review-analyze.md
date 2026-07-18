---
name: review-analyze
description: How to analyze a diff — checklist execution, finding patterns, classifying changes, trigger counting
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: analyze-phase
---

## Diff Analysis Protocol

Run the checklist from `framework/review/checklists/diff-checklist.yml` in priority order.

### Getting the Diff

- **Branch diff**: Use THREE-DOT merge-base syntax to get only the
  branch's own changes:
  `git diff <base>...<head> --stat` for overview first,
  `git diff <base>...<head>` for the full diff,
  `git log --oneline <base>...<head>` for the commit list.
  **NEVER use two-dot syntax** (`<base>..<head>`) for branch reviews.
  Two-dot includes upstream changes on stale branches.
- **MR**: Use GitLab MCP tools (`gitlab_get_merge_request_diffs`) to fetch the diff
- **File**: Read the file directly, check against conventions
- **Staged**: `git diff --cached`

Always get the `--stat` overview first to understand scope before reading full diffs.

### Checklist Execution

For each check in `diff-checklist.yml`:

1. **CHK-SEC (Security)**: Scan diff for patterns matching secrets, tokens, API keys, passwords, private keys. Regex patterns: `(?i)(password|secret|token|api.?key|private.?key)\s*[:=]`, base64-encoded strings in config files, `.env` file additions.

2. **CHK-STABILITY (Stability)**: For each modified file, compute stability level using git log. Flag stable files (change_share < 0.05) and pinned files (from `project/review/stability.yml` if present).

3. **CHK-CONSTRAINTS (Constraints)**: Check each commit in the diff for file count (max 8), message format (imperative summary + body).

4. **CHK-CONVENTIONS (Conventions)**: Load matched scope conventions. For each convention, check if the diff violates it. Also check universal code conventions from `framework/review/rules/code-conventions.yml`. **After checking, update trigger counts** (see below).

5. **CHK-QUALITY (Code quality)**: DRY violations, hardcoded config, architectural boundaries. Delegate to `review-code` agent for large diffs.

6. **CHK-COMMENTS (Comment accuracy)**: If comments changed, verify accuracy, flag rot, flag restated-obvious comments. Delegate to `review-comments` agent.

7. **CHK-TYPES (Type design)**: If types changed, evaluate invariants, encapsulation, enforcement on 4 dimensions (1-10). Delegate to `review-types` agent.

8. **CHK-TESTS (Test coverage)**: Behavioral coverage, critical path gaps, test quality. Rate gaps by criticality (1-10). Delegate to `review-tests` agent.

9. **CHK-ERRORS (Error handling)**: Empty catches (R-008, blocking), broad catches, silent failures, missing error context. Delegate to `review-errors` agent.

10. **CHK-DEPS (Dependencies)**: Unused imports, circular dependency introduction.

11. **CHK-SPECS (Spec compliance)**: If `project/specs/` exists, check contracts, invariants, permissions. Run `--validate` if spec files modified.

12. **CHK-HISTORY (Historical patterns)**: Check history for similar past flags.

13. **CHK-INTENT (Intent clarity)**: Identify remaining ambiguity. Triggers clarify phase.

14. **CHK-SIMPLIFY (Simplification)**: After all checks pass, delegate to `review-simplify` agent. Advisory only, not blocking.

15. **CHK-MR-CONTEXT (MR & Issue alignment)**: If MR/issue context
    was loaded during orientation:
    - Check that unresolved reviewer comments are addressed in
      the current diff. If a reviewer requested a specific change
      and the code hasn't changed in that area, flag as WARN.
    - Check that the MR description matches the actual changes
      (e.g., "What does this MR do" section reflects the diff).
    - Check that issue requirements/acceptance criteria are
      covered by the diff.
    - Summarize any key decisions from issue comments that affect
      the review (e.g., "agreed to skip feature flag per comment").
    - Classification: WARN for unresolved concerns, PASS otherwise.
    - SKIP if no MR or issue context was loaded.

16. **CHK-LABELS-TRAILERS (Labels & commit metadata)**: Check MR
    labels and commit trailers against GitLab conventions.
    All findings in this check are WARN (not FAIL), since Danger
    auto-adds some labels and the MR may be in-progress.

    Labels:
    - Must have a `type::` scoped label (type::feature, type::bug,
      type::maintenance)
    - Must have section/devops/group labels matching the team
    - Specialization labels (frontend, backend, database,
      documentation) should match the files changed
    - If database migrations present: `database` label required
    - If feature flag YAML touched: `feature flag` label expected
    - If EE-only files changed: verify EE-relevant labeling

    Commit trailers:
    - `Changelog:` trailer: required unless docs-only, refactor,
      or pipeline-only change. Valid categories: added, fixed,
      changed, deprecated, removed, security, performance, other.
      Skip check if labels include maintenance::refactor,
      maintenance::pipelines, maintenance::workflow, ci-build, meta.
    - `EE: true` trailer: required when only ee/ files changed
    - `MR:` trailer: optional, must be full URL if present
    - No short references (#123, !123) in commit messages —
      must use full URLs

    Commit message format:
    - Subject: capital letter, ≤72 chars, no trailing period,
      ≥3 words, no emoji (Markdown or Unicode)
    - Subject and body separated by blank line
    - Body: lines ≤72 chars (excluding URLs)
    - Changes 30+ lines across 3+ files should have a body

    SKIP if no MR context was loaded (labels can't be checked
    without an MR).

### Specialized Agents

Some checks have an associated `agent` field in the checklist. When present,
you may delegate deep analysis to that agent via the Task tool:

- **CHK-QUALITY** → `review-code` agent
- **CHK-COMMENTS** → `review-comments` agent (if comments changed)
- **CHK-TYPES** → `review-types` agent (if types changed)
- **CHK-TESTS** → `review-tests` agent
- **CHK-ERRORS** → `review-errors` agent
- **CHK-SIMPLIFY** → `review-simplify` agent (after all checks pass)

Delegation is optional. For small diffs, run checks inline. For large diffs
or when deep analysis is needed, delegate to the specialized agent.

### Confidence Scoring

Rate each finding 0-100:
- **0-25**: Likely false positive or pre-existing issue
- **26-50**: Minor nitpick not explicitly in rules
- **51-75**: Valid but low-impact
- **76-90**: Important, requires attention
- **91-100**: Critical bug or rule violation

**Only report findings with confidence >= 80.** This filters aggressively
for quality over quantity, matching the approach used by specialized agents.

Include the confidence score in the report:
```
CHK-CONVENTIONS  FAIL  CC-008: Hardcoded state name "opened" (confidence: 92)
```

### Finding Verification (mandatory before FAIL classification)

Before classifying any finding as FAIL (confidence >= 80), you MUST
verify the underlying assumption against the actual source code.
Do NOT classify based on heuristics or pattern matching alone.

**Verification steps:**

1. **Behavioral claims** — If the finding claims "this code should
   do X" or "this test is wrong because the component does Y",
   read the relevant production source file to confirm. Use
   `git show origin/master:<path>` for the latest version.
   Example: before saying "this assertion should be positive",
   check what the component actually redirects to and why.

2. **Inconsistency findings** — If the finding is based on a
   pattern inconsistency (e.g., "two of three tests use pattern A,
   one uses pattern B"), check whether the inconsistency has a
   semantic reason. Read the surrounding code to understand WHY
   the pattern differs before flagging it.

3. **Missing test findings** — If claiming a code path is untested,
   verify the code path actually exists by reading the source.
   Check that the branch condition you're referencing is real.

**If verification changes your assessment**, adjust the confidence
score or reclassify. If the finding was based on an incorrect
assumption, drop it entirely — do not report it at a lower
confidence.

**If you cannot verify** (e.g., the file doesn't exist or the
code is too complex to trace), cap the confidence at 75 (WARN
threshold) and note "unverified" in the finding description.

### Result Classification

Each check produces one of:
- **PASS**: No issues found (or all findings below confidence threshold)
- **FAIL**: Issue found with confidence >= 80, verified against source code
- **WARN**: Issue found with confidence 60-79 that should be discussed
- **SKIP**: Check not applicable (e.g., no specs present for CHK-SPECS)

### Convention Trigger Counting (during CHK-CONVENTIONS)

For every convention checked during CHK-CONVENTIONS, determine if it is
**applicable** to the current diff. A convention is applicable when:
- Its scope matches files in the diff (e.g., an `api` convention applies when API files are in the diff)
- The convention's subject matter is relevant to the changes (e.g., an error handling convention applies when error handling code is modified)

For each applicable convention, regardless of whether the diff passes or violates it:
1. Increment `triggered_count` by 1 in the scoped convention file
2. Set `last_triggered` to today's ISO8601 date
3. Track which conventions were triggered for the review history

This tracking drives the promotion system. Do NOT increment for conventions
that are not applicable to the current diff.

### Promotion Candidate Detection

After CHK-CONVENTIONS completes and trigger counts are updated, scan all
conventions for promotion candidates:

- `triggered_count >= 3` AND `promoted == false`

If any candidates exist, add a **Promotion** section to the review report:

```
=== Promotion Candidates ===

  API-001 (triggered 5 times): "All endpoints must validate input"
  GEN-003 (triggered 3 times): "Background jobs must be idempotent"

These conventions have been consistently relevant. Propose promotion? (y/n)
```

The agent asks the human for confirmation before promoting each candidate.
See the review-learn skill for the promotion execution protocol.
