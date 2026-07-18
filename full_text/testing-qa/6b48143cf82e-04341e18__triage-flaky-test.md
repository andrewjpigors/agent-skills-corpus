---
name: triage-flaky-test
description: Triage (classify and label) a single flaky-test failure issue from the quality/test-failure-issues tracker — set the feature category, owning group, and flaky-test::* type, then post an Organizations Agent Triage Recommendation. Use when asked to triage/classify/categorize a flaky test failure issue (URL or ID). Does NOT fix the test.
argument-hint: "<failure issue URL/ID — required>"
allowed-tools: Bash, Read, Grep
---

# Triage Flaky Test File

Classify a flaky-test-file failure issue and leave a recommendation. Given a failure issue, produce:

1. The correct **feature category** label (e.g. `Category:Groups & Projects` vs `Category:Organization`).
2. The correct **owning group** (`group::*`).
3. The correct **`flaky-test::*` type** label.
4. A recommendation posted under a `## Organizations Agent Triage Recommendation` heading, closing with the agent-skill attribution footer.

This is triage, **not** a fix — it categorizes and labels; it does not change the test.

**Idempotency guard:** if the issue already carries a triage note — a note whose body contains the attribution footer `Triaged by the organizations agent skill` (posted under the `## Organizations Agent Triage Recommendation` heading by a prior run) — it has **already been triaged**. Stop and report that; do **not** re-triage or post a second note. Otherwise you are cleared to classify and apply (labels + note) directly — no separate go signal is needed.

## 1. Get the target

A target is **required** (a failure issue URL or ID). If none was given, stop and ask — do not pick an issue from the tracker yourself. These are GitLab **work items**; the numeric ID is the issue IID.

Before triaging, check the issue's notes for the attribution footer above (`glab api "projects/gitlab-org%2Fquality%2Ftest-failure-issues/issues/<iid>/notes?per_page=100"`). If it's already triaged, stop and report — skip the rest.

## 2. Gather the evidence

Read `references/gather-evidence.md` to fetch the issue, its diagnostic comment, and the CI job logs, then **classify every job in the timeline and tally by signature** — the live flake is the signature spread across the most days (incl. recent ones), not the aggregated "dominant error %", the pattern table's headline, or a single-day spike.

Then **reconcile the tally against fixes already merged on `master` or in flight** (`git log` on the spec file, the issue's linked MRs, a branch named `<iid>-*`). The tally ranks the snapshot window, which is history — if its top signature is already fixed, exclude it and re-rank to the top remaining live signature. Never label the issue after a flake that's already resolved.

## 3. Classify

Read `references/classify.md`. First decide the **verdict**: is there a live flake, a one-off / already-cleared transient that should be **closed**, or is the issue **still reported flaky but the only data available to you is stale**? If it's a live flake, decide the feature category + owning group and pick the `flaky-test::*` type label. If it's closeable, recommend closing instead of labeling. If it's still reported flaky but the evidence is weeks old, recommend the DRI look into the most recent logs and **refuse to modify the labels**.

## 4. Apply the recommendation

Read `references/classify.md` (final section) for the recommendation-note template and the label/comment API calls, then apply directly. For a live flake, post the note and update labels. For a closeable verdict, post the close note and close the issue. For a stale-data verdict, post the note only — leave the labels untouched and don't close.

Then report what you did — the same concise, scannable recommendation (live flake, root cause, type, label add/remove/keep), the format in `references/classify.md`, labels as `~` references. Keep it tight; don't over-explain.
