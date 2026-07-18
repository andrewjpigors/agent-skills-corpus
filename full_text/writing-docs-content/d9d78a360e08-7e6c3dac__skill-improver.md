---
name: skill-improver
description: Continuously experiments with Claude Code skills to improve them over time. Each skill invocation acts as an experimental observation; iterations apply real mutations to the skill bundle, measure the impact, and keep or revert based on a composite quality metric. Trigger automatically (passive) on every Skill use, or run a focused experiment burst via /improve-skill. Friction detected during normal skill use kicks off a remediation experiment. USE FOR — improving skill quality, experimenting on skills, optimizing skill prompts, measuring skill effectiveness, /improve-skill, /improve, addressing friction in a skill, refining skill behavior over time. DO NOT USE FOR — creating new skills (use skill-creator), one-shot bug fixes in skill code (regular dev workflow), changes to a skill's YAML name field (immutable identifier).
license: MIT
compatibility: Requires git, Claude Code, gitlab-mcp MCP server. Each managed skill must live in a git repo (skill-improver itself or under the claude-code-skills GitLab group). Hooks added globally during install.
---

# Skill-Improver: Continuous Skill Experimentation (v2)

> **v2 design.** v1 (current) is friction-spawn-driven; v2 is metric-driven continuous experimentation. v1 stays running until v2 is implemented and the cutover is performed via an MR.

An experimentation loop for Claude Code skills. Real user invocations are the iterations; the system mutates each skill, measures the impact via per-use telemetry, and keeps or reverts each change. Inspired by Karpathy-style autoresearch, generalized to long-running skill quality optimization.

## Three modes

| Mode | Trigger | Cadence | Iterations come from |
|---|---|---|---|
| **Passive observation** | Default state. Auto-triggered by PostToolUse hook on Skill invocations. | Every 5 user-driven Skill uses observe → at use 10 commit verdict + propose next mutation. | Real users running the skill in real sessions. |
| **Active synthetic burst** | `/improve-skill <name>` slash command. | Continuous; agent runs eval batteries via subagents, no user gating. | Synthetic eval test cases run by subagents. |
| **Friction-watch remediation** | `.friction-log.json` written during normal skill use, after the initial budget is exhausted. | 5-iteration burst targeted at the specific friction point. | Mix of synthetic and real, depending on friction context. |

Active mode resumes from where passive left off: if passive is mid-iteration N, active discards passive's in-progress partial and begins synthetic iteration N from scratch. After active drains the budget → friction-watch.

## Agent Behavior Rules

1. **DO** run the Setup phase interactively the first time `/improve-skill` is invoked on a skill that has no metric definition.
2. **DO** establish a baseline measurement before mutating anything.
3. **DO** commit every mutation to `experiment/<skill>` branch before measuring (so revert is a clean `git reset`).
4. **DO** apply mutations directly — no "proposed but not applied" deferrals.
5. **DO** revert iterations that regress the composite metric (`git reset --hard HEAD~1`).
6. **DO** capture per-skill-invocation telemetry in real-time and persist it to `.telemetry.jsonl`.
7. **DO NOT** mutate the YAML `name` field — it's the skill's identity.
8. **DO NOT** mutate the YAML `description` field via this loop — that's a separate optimization sub-loop (use `scripts/run_loop.py` instead).
9. **DO NOT** keep iterations that regress the metric, unless the user pre-approved that trade-off.
10. **DO NOT** install new dependencies, change environment, or touch test/eval harness files unless explicitly approved.

---

## Setup phase (first invocation per skill)

**Mechanism — two paths, same outcome.** Setup needs interactive Q&A with the user, which requires a direct user-input channel. Two ways to provide it:

- **Preferred (when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)**: spawn a `setup-coordinator-<skill>` as a **team member**. Each team member has its own Claude Code session and direct user input — the user uses **Shift+Down to cycle to the coordinator and types answers directly** (or clicks into the coordinator's pane in split-pane mode). The main session is uninvolved during Q&A. This is cleaner UX and isolates setup-thinking from whatever the user was doing in the main session.
- **Fallback (when teams aren't enabled)**: spawn `setup-coordinator-<skill>` as an addressable sub-agent. The main session relays each Q from the coordinator (via `SendMessage`) and the user's A back. Functionally identical; just routes everything through the main session.

The coordinator's prompt is the same in both paths. Only the input plumbing differs. Both paths produce the same `.skill-meta.json` and the same handoff to the iteration loop.

**Completion signal — belt-and-suspenders.** When setup completes, the coordinator (a) writes `<skill-bundle>/.setup-complete` sentinel file *and* (b) sends a "DONE" message to the main session. The sentinel is the authoritative completion marker because in team mode, messages addressed to team-lead don't always surface as turn-deliveries — the main session can `[[ -f ... ]]` check the sentinel reliably even if the message is buffered in the inbox.

When `/improve-skill <name>` is invoked on a skill with no metric definition in `.skill-meta.json`, the coordinator (in either mode) asks the eight questions below. Auto-derive defaults where possible. Echo a confirmation table; require explicit "go" before writing `.skill-meta.json`.

### 1. What does this skill need to do well?

Elicit one or more **success criteria** — these become *proposed metrics*. For each criterion, capture:

- **Description** — one sentence (e.g., "extracted CSV matches the expected schema")
- **Measurement** — how to evaluate it. Could be:
  - A regex/jq match against tool output
  - A grader subagent prompt (LLM-as-judge)
  - A scripted check (e.g., `jq '.errors | length == 0'`)
- **Direction** — `lower-is-better` or `higher-is-better`
- **Weight** (optional, defaults to 1.0)

A skill can have multiple criteria. They're combined into the **proposed-metric bucket** in the composite score. If 3 criteria are defined with default weight 1.0, each contributes 1/3 of the bucket weight.

### 2. Implicit telemetry — automatic

These are captured for every Skill invocation regardless of skill type:

- **Tokens** — input + output tokens consumed during the skill's session window
- **Tool-call count** — number of tool calls between the Skill invocation and window close
- **Re-prompt rate** — whether the user re-prompted (signal of incomplete output)
- **Completion** — boolean (did the agent emit a Stop marker before window closed)

Direction: `lower-is-better` for tokens and tool-count and re-prompt rate; `higher-is-better` for completion.

### 3. Friction signal — automatic

The existing `.friction-log.json` mechanism (Claude self-review during deliberate review). One number per friction-log write: count of `friction_points` entries. Direction: `lower-is-better`.

### 4. Composite score formula

```
composite = (proposed_weight × Σ proposed_terms)
          + (implicit_weight × Σ implicit_terms)
          + (friction_weight × friction_term)
```

Default weights: **proposed=3.0, implicit=1.0, friction=0.5**. All terms normalized to [0, 1] before weighting; direction inversion handled per term.

The composite is the keep/discard signal. Lower-is-better on composite by default.

### 5. Mutable scope

Defaults to **the entire skill bundle except the YAML `name` and `description` fields**. That includes SKILL.md body, `references/`, `scripts/`, `assets/`. Per-skill override allows narrowing (e.g., "only SKILL.md body" for skills with sensitive scripts).

### 6. Constraints

Project defaults applied to every skill:

- Resulting SKILL.md must be valid YAML+markdown (parse-checked after every iteration)
- Total SKILL.md must not exceed 500 lines (autoresearch-style line budget)
- The YAML `name` field must remain unchanged (parsed and verified)
- File paths/imports referenced in SKILL.md must still exist after the mutation

Per-skill add-ons allowed (e.g., "always preserve the section titled `## Examples`").

### 7. Iteration budget

`MAX_ITERATIONS` — default **100**. Per-skill override stored in `.skill-meta.json`. When budget is exhausted, mode shifts to friction-watch.

If `/improve-skill <name>` is invoked on a skill with budget already exhausted: refill to N and start a fresh experiment cycle. (Simplest predictable behavior.)

### 8. Simplicity policy

Prefer ablations over additions. When generating an iteration's mutation, follow this priority:

1. **Remove** — does friction stem from a misleading or redundant section? Delete it.
2. **Tighten** — same outcome, fewer words?
3. **Restructure** — same content, clearer hierarchy?
4. **Add** — only if 1–3 don't address the issue.

Net-zero or net-negative line count is a great outcome.

---

## Iteration loop (passive mode)

Each iteration spans **10 user-driven Skill invocations**: 5 observation uses on the current variation, then 5 verdict uses on the candidate mutation.

```
Per iteration N (passive):

1. PROPOSE — agent generates one candidate mutation (per simplicity policy).
             Commit to experiment/<skill> as "iter N: <description>".

2. OBSERVE  — uses 1..5 of iteration N run on the candidate.
             Telemetry collected per use; running averages computed.

3. DECIDE  — at use 5 of iteration N, compare aggregate metrics:
             IMPROVED  → Keep. Update "best" baseline. Status = "keep".
             NEUTRAL/  → Revert: `git reset --hard HEAD~1`. Status = "discard".
             WORSE       Variation existed for 5 uses, then reverted.
             CRASH    → If parse-check or constraint check failed:
                         attempt a quick fix (typo, malformed yaml).
                         Amend the iteration commit, retry parse.
                         If unfixable in 2 attempts → revert.
                         Status = "crash".

4. LOG     — Append row to experiments.tsv:
             N  commit  metric_pre  metric_post  delta  status  description

5. ADVANCE — Increment iteration counter. If N == MAX_ITERATIONS → end passive,
             emit final report, transition to friction-watch.
```

Cycle math: 100 iterations × 10 uses each = 1,000 user-driven invocations. For a skill used 20×/day, that's ~50 days of passive observation.

## Iteration loop (active mode)

Same logic, synthetic execution. When `/improve-skill <name>` fires:

1. **Resume point**: discard passive's in-progress iteration N (if partial). Start synthetic iteration N from scratch.
2. **Eval surface**: requires `evals/evals.json` in the skill bundle. **If absent, the setup phase prompts the user to draft 3–5 evals interactively** (skill-creator-style, but synchronously in the foreground). Active mode will not run without user-reviewed evals; auto-generation without review reliably optimizes for the wrong thing. v2.1 may add auto-gen with mandatory user-review step before iteration begins.
3. **Per iteration**: agent runs the eval battery via subagents on the candidate mutation; aggregates metrics; decides keep/discard.
4. **Cadence**: continuous. No user-invocation gating. Drains remaining iterations until budget reached.
5. **Completion**: same as passive (final report → friction-watch).

### Low-traffic fallback

Skills with fewer than `low_traffic_threshold` invocations in the last 30 days (default **10**) skip passive mode entirely. `/improve-skill <name>` is the only path to iteration for these skills. Threshold is configurable per-skill in `.skill-meta.json`. Without this fallback, a skill used 1×/week would need 19 years to drain a 100-iteration passive budget.

## Friction-watch mode (post-budget)

After budget is exhausted, the system idles. When `.friction-log.json` is written during a normal skill session:

1. Trigger a **5-iteration remediation burst** scoped to the specific friction point(s).
2. Iterations run in active mode (synthetic eval).
3. After 5 iterations → back to friction-watch idle.

Each remediation burst extends the `experiment/<skill>` branch; deltas tracked in the same TSV.

---

## Branch + storage layout

| Path | Purpose |
|---|---|
| `experiment/<skill>` git branch | Where iterations live. Install location is a worktree on this branch. |
| `<skill-bundle>/.skill-meta.json` | Per-skill state: budget, iteration counter, current best metric, criteria definitions. |
| `<skill-bundle>/.telemetry.jsonl` | Per-skill-invocation telemetry. One JSON object per line. Untracked via `.git/info/exclude`. |
| `<skill-bundle>/experiments.tsv` | The iteration ledger. 7 columns: iteration, commit, metric_pre, metric_post, delta, status, description. Untracked. |
| `<skill-bundle>/docs/experiments/<date>.tsv` | TSV archive on `experiment/<skill> → master` merge. Tracked. Branch deleted after archive. |

### Multi-install coordination

A skill can be installed at both user-level (`~/.claude/skills/<skill>/`) and project-level (`<project>/.claude/skills/<skill>/`). **Both worktrees track the same `experiment/<skill>` branch**, share `.skill-meta.json`, and write to the same `.telemetry.jsonl` (since both are git worktrees of the same repo).

- Iteration state is **shared** — a use at user-level and a use at project-level both count toward the same iteration's observation window.
- Telemetry is **merged** in the same file (file-locked appends; conflicts unlikely given JSONL append-only semantics).
- Worktrees can drift if `git pull` runs in one but not the other. The stale one observes/logs against an older variation until pulled. **This is acceptable** — the stale variation's telemetry is still attached to its actual commit, so the data remains coherent.

If a user wants independent experiment streams per install location, that's an explicit per-skill configuration (`independent_branches: true` in `.skill-meta.json`), out of scope for v2.0.

---

## /improve-skill <name> behavior

Single slash command, single behavior:

1. **Setup check** — if `.skill-meta.json` lacks metric definitions, run setup phase first.
2. **Resume from passive** — discard any partial iteration; preserve completed iterations.
3. **Active burst** — drain remaining budget via synthetic evals.
4. **Final report** — print top-3 most impactful iterations, kept-only commit log, recommended next steps for human review.
5. **Open MR** — propose `experiment/<skill> → master` merge.
6. **Transition to friction-watch** — passive scheduling ends for this budget cycle.

If invoked on a skill whose budget is already exhausted: refill to N, start a fresh cycle from iteration 1.

---

## Key invariants

- Every iteration is a real `git commit`. Reverts are real `git reset --hard HEAD~1`.
- The installed skill at `~/.claude/skills/<skill>/` (or `<project>/.claude/skills/<skill>/`) **is** a worktree on `experiment/<skill>`. Real users execute the candidate.
- `master` only advances when an `experiment/<skill> → master` MR is approved by a human.
- Telemetry is captured per Skill PostToolUse and accumulates over a window that closes on: next Skill use / next UserPromptSubmit / Stop. Real-time-with-settled-flag.
