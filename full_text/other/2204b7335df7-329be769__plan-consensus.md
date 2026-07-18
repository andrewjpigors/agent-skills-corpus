---
name: plan-consensus
description: Use for non-trivial work before implementation. Runs a bounded 3-cycle iteration between an Opus 4.7 (xhigh) planner and a GPT-5.5 (high) reviewer. Surfaces residual disagreement to the user instead of looping forever. Hands the converged plan to Composer 2.5 for implementation.
---

# Plan Consensus

A two-model, three-cycle convergence protocol that catches blind spots no
single model would catch alone. Use this as the **default** plan-review
mode for any non-trivial work. Use `plan-review` (single-pass) only for
plans too small to justify three cycles.

## When to run

Run when any of these is true:

- Plan touches 3+ packages or 5+ files.
- Plan involves architecture changes, migrations, contract bumps,
  cross-service sagas, or feature flags affecting money/identity/RG.
- Plan touches sensitive surfaces (auth, payments, KYC, RG, admin,
  Fireblocks, ledger, key material).
- Plan was produced for an ambiguous, multi-step, or high-risk ticket.
- Manager explicitly asks for plan-consensus.

Skip and use `plan-review` instead when:

- Plan touches 1-2 files and 1 package.
- Plan is a copy / translation key change.
- Plan is a dep bump with no API impact.
- Plan is pure formatting or mechanical rename.

## Hard model assignment

This skill assigns models. Do NOT substitute.

- **Planner**: `claude-opus-4-7-thinking-xhigh` (Tier C).
- **Reviewer**: `gpt-5.5-high` (Tier B).
- **Implementer dispatch after convergence**: `composer-2.5-fast` (Tier A)
  for the bounded, pattern-following work that follows the converged
  plan. The manager may upgrade specific implementer subagents to
  Tier C when the converged plan calls out an architecturally
  significant or sensitive-surface piece (rare; document why).

Cross-family planner/reviewer is the whole point — Opus and GPT-5.5
fail in different directions. Composer 2.5 is NOT used in this skill.

## The 3-cycle protocol

The manager runs exactly **three** plan ↔ review cycles, then stops.
Each cycle has two Task dispatches.

### Cycle 1

1. Dispatch the `planner` subagent with `model: "claude-opus-4-7-thinking-xhigh"`.
   Input: the verified task (from `verify-task`), repo context, success
   criteria, non-goals, affected packages. Expect output: `plan v1`
   in `.cursor/plans/<ticket>.plan.md` (or in-chat if no plans dir).
2. Dispatch a reviewer subagent (use the `plan-review` skill body)
   with `model: "gpt-5.5-high"`. Input: `plan v1` + the same repo
   context. Expect output: verdict (GREEN / YELLOW / RED) + per-criterion
   scores + concrete diff suggestions.

If verdict is **GREEN** after cycle 1, skip cycles 2 and 3 and proceed to
implementation. Early convergence is a feature, not a bug.

### Cycle 2

3. Resume the `planner` subagent (do NOT pass `model:` on resume — the
   Task tool preserves the planner's Opus model). Input: cycle-1
   reviewer findings + `plan v1`. Expect output: `plan v2` that
   either accepts each finding (with the change applied) or rejects
   it (with one-sentence rationale).
4. Resume the `plan-review` reviewer subagent. Input: `plan v2` +
   cycle-1 findings (so the reviewer can see what was accepted vs
   rejected). Expect output: new verdict + new findings.

If verdict is **GREEN** after cycle 2, proceed to implementation.

### Cycle 3

5. Resume the planner with cycle-2 findings. Output: `plan v3`.
6. Resume the reviewer with `plan v3` + history of accepted/rejected
   findings. Output: final verdict.

After cycle 3, **stop iterating regardless of verdict**.

## Convergence outcomes after cycle 3

| Final verdict | Action |
|---|---|
| **GREEN** | Plan converged. Proceed to implementation. |
| **YELLOW** | Plan converged on most points; reviewer flagged residual concerns. Apply the listed YELLOW fixes inline, then proceed. Do NOT run a 4th cycle. |
| **RED** | Persistent structural disagreement. Surface the disagreement to the user as a single bulleted summary: what the planner insists on, what the reviewer rejects, and which decision the user must make. Do NOT proceed to implementation. |

The 3-cycle cap exists because two models that haven't agreed by cycle
3 usually have a real semantic disagreement that no further loop will
resolve. The human in the loop makes the call.

## Disagreement surfacing format (RED after cycle 3)

```
## Plan-consensus did not converge after 3 cycles

**Question to resolve:** <one-sentence framing of the disagreement>

**Planner (Opus 4.7 xhigh) position:**
- <bullet>
- <bullet>

**Reviewer (GPT-5.5 high) position:**
- <bullet>
- <bullet>

**Implications of each choice:** <one paragraph>

**Recommended next step:** <one option, with the reasoning>
```

## Hand-off to implementation

Once GREEN or post-YELLOW-fix, dispatch implementation per the
orchestrate skill's dispatch matrix. Implementer subagents default
to `composer-2.5-fast`. Upgrade a specific implementer to
`claude-opus-4-7-thinking-xhigh` only when the converged plan
explicitly calls out one of:

- Provider topology / context boundary design.
- API contract definition (new endpoint shape, breaking change).
- Money flow, ledger entries, or idempotency contract.
- Auth / session / permission boundary.
- Cross-service saga or distributed transaction.

For everything else — Composer 2.5 owns the implementation.

## Rules

- Hard model pinning. The planner is Opus 4.7 xhigh, the reviewer is
  GPT-5.5 high. No substitution.
- Exactly three cycles maximum. No silent fourth cycle.
- Reviewer's job is findings, not redesign. The reviewer never
  rewrites the plan.
- Planner's job is to accept or reject each finding with explicit
  rationale. Silently dropping a finding is not allowed.
- If the planner runs out of useful revisions before cycle 3 (verdict
  was GREEN earlier), stop early. Three cycles is a cap, not a quota.
- The manager (this session) does NOT participate in the plan / review
  cycles. The manager dispatches, observes, and surfaces the result.
  Manager intervention mid-cycle defeats the cross-model audit.

## Return

The converged plan (file path or in-chat), the final verdict, the
list of accepted vs rejected reviewer findings across all cycles,
and either the implementation dispatch (GREEN/YELLOW) or the
disagreement surfacing (RED).
