---
name: triage-org-flaky-tests
description: Batch-triage every open flaky-test failure issue owned by the Organizations group — all `group::organizations` issues in quality/test-failure-issues not already triaged by the agent. Classifies, labels, posts a recommendation, and marks each triaged so re-runs skip it. Use to sweep the group's flaky-test queue. Delegates each issue to triage-flaky-test.
allowed-tools: Bash, Read, Grep
---

# Triage Organizations' Flaky-Test Queue

Sweep every open flaky-test failure issue owned by the Organizations group and triage the untriaged ones. Use the `glab` CLI.

`triage-flaky-test` applies directly (labels + note) and self-skips any issue already triaged, so this sweep just enumerates and delegates — triage and post for each issue, then give the user the Step 3 summary.

## Step 1 — find untriaged issues

Read `references/queue.md` for the commands. It lists open `group::organizations` issues and drops three kinds: issues whose title does **not** start with `[Flaky Test File]` (other failure types — e.g. `[Test]` E2E/QA — are out of scope); issues already carrying the agent's marker (the recommendation note's attribution footer); and issues with a linked fix MR (work in progress). A **quarantine** MR does not count as work in progress — the flake itself is still untriaged — so those issues are still triaged.

## Step 2 — triage each issue

For each issue, apply the **`triage-flaky-test`** skill (`/organizations:triage-flaky-test`) with that issue ID: gather evidence, classify, apply labels, post the `## Organizations Agent Triage Recommendation` note. The note closes with the agent-skill attribution footer, which doubles as the marker that keeps this sweep idempotent — so posting the recommendation *is* what marks the issue triaged; there is no separate marker comment. The queue is already scoped to `[Flaky Test File]` issues (Step 1), so triage each one with the same process.

Some issues have **no live flake** — a one-off or already-cleared transient. For those, `triage-flaky-test` posts the close note and closes the issue (a closed issue drops out of the open-issues query, so the sweep stays idempotent). Report these in the summary as closed, not triaged.

## Step 3 — summarize

```
Triaged X issues:

1. #43489 sharding_key_spec.rb — ~"flaky-test::state leak", kept ~Category:Organization
2. #43468 groups_spec.rb — ~flaky-test::too-many-sql-queries, kept ~"Category:Groups & Projects"

Closed Z one-off issues:

1. #43457 user_inherited_access_spec.rb — single OpenTimeout, infra blip, no recurrence

Skipped Y already-triaged issues.
```
