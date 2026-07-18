---
name: orchestrate
description: Use for non-trivial tickets, design implementations, migrations, or risky bug fixes. Acts as a manager session that dispatches to specialist subagents by change type, runs a remediation loop after pr-audit, and preserves main-agent architecture judgment.
---

# Orchestrate

Manager mode. The main session is the manager. Subagents do bounded work
(planning, implementation, review, QA) and report back. The manager owns
synthesis, architecture, source-of-truth decisions, domain-risk judgment,
and final commit framing.

## Model tier guidance

Tiers and per-role assignments live in the `agent-routing` and
`model-policy` rules. The manager dispatches every subagent with an
explicit `model:` parameter:

- Manager session: `claude-opus-4-7-thinking-xhigh`.
- Tier A subagents and skills: `composer-2.5-fast`.
- Tier B subagents (terminal-heavy): `gpt-5.5-high`.
- Tier C subagents (architecture, sensitive, perf):
  `claude-opus-4-7-thinking-xhigh`.
- For `plan-review` and `plan-consensus`, pick a model family that is
  NOT the planner's.

Constraints:

- Do NOT pass `model:` when using `resume:` — the Task tool preserves
  the prior subagent's model and rejects the parameter.
- Do NOT let a Tier A subagent own architecture, contract changes, or
  domain-risk calls.

## Recommended manager model

The main chat session IS the manager. Default the session driving
orchestrate to `claude-opus-4-7-thinking-xhigh` — manager work owns
final synthesis and domain-risk judgment, both of which Opus handles
best.

Narrow exception: very-long-running orchestrations dominated by
shell-pipeline subagents (multi-service migration with many ORM CLI
runs, large CI debugging session). For those, `gpt-5.5-high` is
reasonable because the manager spends most of its time orchestrating
tool calls, which is GPT-5.5's Terminal-Bench strength.

Do NOT manage from a Tier A model. The manager owns architecture
decisions and Composer 2.5 is not allowed to own those.

## Ownership rules

- Main session owns: product intent, architecture boundaries, API semantics,
  provider topology, domain-risk judgment, final synthesis, commit framing.
- Subagents own: fact gathering, bounded file-scoped implementation, scoped
  review, scoped QA.
- Subagents may NOT silently redefine requirements or change architecture.

## Workflow

1. Read repo guidance (`AGENTS.md` root + per-package), plus any open Cursor
   plans relevant to this work.
2. **Triage** — if a ticket is in scope (Linear, GitLab, Jira, etc.), run
   `linear-triage` (or the equivalent triage skill).
   - RED -> stop. Surface the draft comment + reassignment.
   - YELLOW -> ask the user 1-3 clarifying questions; resume when answered.
   - GREEN -> continue.
3. `verify-task` for bugs or ambiguous features. For features, state success
   criteria, non-goals, affected app/package, and user/admin boundary.
   - If the task is large or vague, run `decompose` BEFORE `planner` so
     the plan operates on already-divided subproblems.
   - If reproduction or framing gets stuck for >15 minutes, run
     `stuck-loop`.
4. Produce the plan via the `planner` agent for ambiguous scope, or the
   `senior-architect` agent for architecturally significant work.
5. **Plan review** — pick the right depth for the stakes:
   - Trivial single-file edits or copy-only changes: skip.
   - Small bounded plans (1-2 files, 1 package, no contract/architecture
     concerns): run `plan-review` (single-pass cross-family audit).
   - **Default for non-trivial work**: run `plan-consensus` — a 3-cycle
     iteration between the `planner` subagent on
     `claude-opus-4-7-thinking-xhigh` and the `plan-review` reviewer on
     `gpt-5.5-high`. Early convergence (GREEN after cycle 1 or 2)
     stops the loop. Persistent disagreement after cycle 3 is surfaced
     to the user; the manager does NOT silently extend to a 4th cycle.
   - GREEN -> continue.
   - YELLOW after `plan-consensus`: apply the listed fixes inline,
     then continue (do not start a 4th cycle).
   - RED after `plan-consensus`: stop. Surface the disagreement to the
     user using the format in `plan-consensus`'s "Disagreement
     surfacing" section. Wait for the user's call before re-entering
     step 4.
   - RED after `plan-review` (single-pass): back to step 4.
6. **Dispatch matrix** — pick the implementer subagent by the dominant change
   type. **Default implementer model is `composer-2.5-fast`** unless the
   converged plan explicitly calls out an architecturally significant or
   sensitive-surface piece (then upgrade that specific subagent to
   `claude-opus-4-7-thinking-xhigh`; document why in the dispatch note).
   If two implementers apply, pick the dominant one and hand off explicitly:
   - UI design from Figma / new screen / new modal / layout change
     -> `ui-implementer` (Composer 2.5) + `design-implementation` skill +
     `figma-read` when designs exist.
   - Data / API / cache / endpoint / mutation / mapper / generated-client
     consumer -> `data-implementer` (Composer 2.5) + `api-sync` or
     `wire-mock-to-api` or `generated-artifact-sync` as relevant.
     Upgrade to Opus xhigh if the work defines a new API contract or
     touches money/identity flows.
   - React architecture (providers, hooks composition, Suspense, state
     machines, perf, dynamic imports) -> `senior-implementer` (Opus
     xhigh — architecture is Tier C) + optionally `module-scaffold`
     for new feature shells.
   - CSS / design tokens / responsive-only -> `styling` (Composer 2.5).
   - Cross-package or contract-bump migration -> `migration-engineer`
     (GPT-5.5 high — Tier B, terminal-heavy).
   - Behavior-preserving cleanup -> `refactorer` (Composer 2.5).
   - User-facing text -> `i18n-workflow` skill (Composer 2.5).
   - Test gap surfaced -> `testing-guide` -> `test-writer` (Composer 2.5)
     or `e2e-engineer` (Composer 2.5; upgrade to GPT-5.5 if the test
     setup is shell-heavy).
7. `quality-gates` — scoped to changed packages/apps; never invent commands.
8. `pr-audit` (manager mode — fans out to specialist reviewers; see that
   skill).
9. **Remediation loop** — if `pr-audit` returns findings ordered SEVERE or
   BLOCKING:
   - Route each finding to its owner subagent: `refactorer` for cleanup,
     the relevant implementer specialist for behavior fixes, `data-layer`
     reviewer + `data-implementer` for cache/contract issues,
     `migration-engineer` for migration-reviewer findings, etc.
   - Re-run `quality-gates`.
   - Re-run `pr-audit`.
   - If the same finding survives a second cycle, run `cognitive-heuristics`
     or `stuck-loop` to break the pattern before a third try.
   - Stop after TWO cycles. If findings persist, surface them as blockers
     to the user; do NOT keep looping silently.
10. `project-qa` for spot-checked browser QA, or `deep-qa` for high-risk
    flows. `real-browser-qa` only when policy + need both call for it.
11. `commit-prep` — drafts a conventional commit (`type(scope): TICKET msg`).
    The user taps the signing hardware (if required) and runs `git commit`
    manually.
12. `create-mr` — drafts MR title + body + test plan + risk notes. Opens
    via `glab mr create` (GitLab), `gh pr create` (GitHub), or the
    forge's CLI of choice.
13. `done` to capture residual risk. `improve` if recurring friction surfaced.

## Hand-off discipline

- Each subagent invocation must include: scope, files in/out of scope,
  expected return shape, and which sibling subagent owns adjacent work.
- After each subagent returns, the manager summarizes in one line what
  changed and what comes next. No silent state.
- If a subagent's output contradicts the plan, the manager pauses and
  either updates the plan (loop back to step 5) or rejects the output.

## When to bypass orchestrate

Skip orchestrate and go straight to implementation when:

- Single-file fix with obvious cause.
- Copy / translation key change only.
- Pure formatting / mechanical rename.

For everything else, run orchestrate.

## Return

- Changed files, checks run (with exact commands), pr-audit verdict, residual
  risk, and explicit next steps for the user.
