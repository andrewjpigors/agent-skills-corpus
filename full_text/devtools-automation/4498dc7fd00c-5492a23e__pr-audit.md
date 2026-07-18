---
name: pr-audit
description: Use for reviewing a branch, diff, or merge request. Manager-mode skill that fans out to specialist reviewer subagents by diff domain, prioritizes correctness over style, and hands findings back to the remediation loop in orchestrate.
---

# PR Audit

Manager mode. Take a code-review stance. Findings come first. The manager
inspects the diff once, dispatches reviewers in parallel by domain, then
synthesizes a single ordered finding list with named owner agents per
finding.

## Workflow

1. Inspect the diff (`git diff`, `git diff <base>..HEAD`, or the MR diff).
2. Map changed paths to their domains: UI, data, sensitive surface, generated,
   tests, docs, migrations, distributed systems.
3. Understand the intended behavior versus the previous behavior. Read the
   plan or ticket if available.
4. **Reviewer dispatch matrix** — fire the always-run reviewer plus the
   domain-conditional ones in parallel:
   - Always: `code-reviewer` — intent match, contract changes, async/concurrency
     bugs, nullability, missed consumers, regressions.
   - If UI files changed (`*.tsx`, `*.style.ts`, Storybook stories, theme,
     i18n keys reaching UI): `frontend-reviewer`. Add
     `design-fidelity-reviewer` when a design source is available. Add
     `react-perf-reviewer` if the diff is heavy in renders, context, hooks,
     memo, large lists, or effect/state interplay.
   - If data files changed (network / services, listeners, mappers, query /
     mutation endpoints, generated-client consumers): `data-layer`.
   - If sensitive-surface files changed (auth, MFA, JWT, payments, signing,
     KYC, RG, admin actions, permission middleware): `security-reviewer`
     AND trigger `sensitive-surface-review` skill.
   - If the fork ships a domain-safety reviewer (e.g. `casino-safety-reviewer`,
     `payments-reviewer`, `vault-reviewer`, `medical-data-reviewer`) AND
     the diff touches that domain: invoke it. See `templates/` for examples.
   - If migration files changed (`*/migrations/**`, `*/db/migrations/**`):
     `migration-reviewer`.
   - If distributed-systems surface changed (Kafka producer/consumer, Redis
     Cluster usage, replication-lag-sensitive reads, cross-service saga,
     idempotency contract, distributed lock, clock-based decision):
     `distributed-systems-reviewer`.
   - If runtime boundaries crossed (web <-> worker, client <-> shared lib,
     SSR <-> CSR): trigger `runtime-boundary-review` skill.
5. Run `quality-gates` if it has not been run on the current diff.
6. Synthesize: merge all reviewer findings into one list, ordered by severity
   (BLOCKING > SEVERE > MAJOR > MINOR > NIT). For each finding, include:
   - File:line reference.
   - One-sentence description of the defect.
   - Concrete fix suggestion.
   - Owner agent for the fix (`refactorer`, `ui-implementer`,
     `data-implementer`, `senior-implementer`, etc.).
7. Verdict at the top:
   - GREEN -> green-light; proceed to commit-prep / create-mr.
   - YELLOW -> fix-and-proceed; remediation loop applies but is bounded.
   - RED -> block; remediation loop required before MR.
8. Hand the verdict and findings back to the `orchestrate` remediation loop
   (step 9 of that skill).

## Out of scope for pr-audit

- Style, formatting, lint — covered by `quality-gates`.
- Speculative refactors that don't address a real defect.
- Cosmetic naming preferences unless they cause a correctness risk.
- Documentation polish (use a separate pass if needed).

## Rules

- Findings only on this run. Do NOT apply fixes — that's the remediation loop.
- Cite file and line for every finding when possible.
- If no issues meet the bar, say that explicitly and name residual test gaps
  or unverified scenarios.
- AI-review labels (CodeRabbit, etc.) are claims, not facts; verify before
  treating them as findings.
- Respect `local/disabled.txt`: do not invoke disabled reviewer agents.

## Return

- Verdict (GREEN / YELLOW / RED).
- Ordered findings list with file:line, fix, and owner agent.
- Residual risk and unverified scenarios.
- Hand-off note to the orchestrate remediation loop.
