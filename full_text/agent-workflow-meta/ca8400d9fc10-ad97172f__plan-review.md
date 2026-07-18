---
name: plan-review
description: Use after a non-trivial plan is produced and before implementation begins. Runs a second-model audit of the plan against six criteria. Findings only; never edits the plan.
---

# Plan Review

Cheap insurance before expensive implementation. A different model than the
planner audits the plan to surface over-engineering, scope inflation, hidden
coupling, and missing risks.

## When to run

Run when any of these is true:

- Plan touches 3+ packages or 5+ files.
- Plan involves architecture changes, migrations, or contract bumps.
- Plan touches sensitive surfaces (auth, payments, KYC, RG, admin).
- Plan was produced for an ambiguous or risky ticket.

Skip when:

- Single-file fix.
- Copy / translation key change only.
- Dep bump with no API impact.
- Pure formatting.

## Model selection

Pick a model family that is NOT the planner's. Three-way rotation across
Opus, GPT-5.5, and Composer 2.5:

- Planner on Opus 4.7 (xhigh thinking) -> review with GPT-5.5 (preferred)
  or Composer 2.5.
- Planner on GPT-5.5 -> review with Opus 4.7 (xhigh) (preferred) or
  Composer 2.5.
- Planner on Composer 2.5 (cost-saving experiment) -> review with Opus
  4.7 or GPT-5.5.

Cross-model coverage catches blind spots no single model would catch
alone. Composer 2.5 is acceptable as a second opinion on bounded plans
but should NOT review architecturally significant or sensitive-surface
plans alone — pair it with Opus or GPT-5.5 review for those.

## Six criteria

For each, rate Pass / Concern / Fail with one-sentence justification:

1. Success criteria are concrete and verifiable from outside the code.
2. Scope is bounded; non-goals are explicit.
3. At least one alternative approach was considered or explicitly dismissed.
4. Risks and failure modes are named (not deferred as TBD).
5. Test / QA plan covers the affected app/package, not just the happy path.
6. Open questions and blockers are visible (not buried in the body).

## Workflow

1. Read the plan artifact (`.cursor/plans/*.plan.md`) or the in-chat plan.
2. Read the same repo files the plan references; do not trust the plan's
   summary of them.
3. Score the six criteria.
4. Output a verdict:
   - GREEN -> proceed to implementation.
   - YELLOW -> proceed after fixing specific items (list them).
   - RED -> re-plan; the approach has a structural problem (describe it).
5. Append concrete diff suggestions to the plan text for each Concern or Fail.

## Rules

- Findings only. Do NOT rewrite the plan silently.
- Do NOT redesign for taste; flag only items that create likely defects, future
  inconsistency, or scope risk.
- Cite specific repo files / nearby patterns for each finding when possible.
- Keep verdict text short; long-form lives in the per-criterion notes.

Return: verdict, the six criterion scores, the concrete diff suggestions, and
any blocker that should pause implementation.
