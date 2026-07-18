---
name: dev-session
description: Unified session lifecycle — start, resume, monitor, and end Copilot CLI sessions. Covers context management, twin sync, issue state, and branch cleanup.
tier: standard
---

# Session Lifecycle

## Model

- **Preferred:** `claude-sonnet-4.6`
- **Cost-tier fallback:** `/model auto` → `claude-sonnet-4.5` — see `/fallback-mode`
- **Source of truth:** Model Routing Matrix in `.github/skills/dev-session/SKILL.md`

This skill owns the full session lifecycle referenced by `.github/copilot-instructions.md`. Use `/dev-session` at the start and end of cold-start sessions. Savepoint-resume sessions may follow the resume path below without re-invoking `/dev-session`, but must still honor the same lifecycle rules.

## Session Start

### Cold-start vs Savepoint-resume path

**Check first:** Does `.session-state/RESUME.md` exist?

```bash
ls .session-state/RESUME.md 2>/dev/null && echo "SAVEPOINT EXISTS" || echo "COLD START"
```

| Path | Condition | Steps |
|---|---|---|
| **Savepoint-resume** | `.session-state/RESUME.md` exists | `view .session-state/RESUME.md` → targeted issue lookup (active issue only) → begin work. **Skip** `skill("dev-session")` and `skill("fallback-mode")` — their operative rules are already in system instructions. **Hygiene scan (steps 3b/4c) is intentionally omitted on savepoint-resume.** The prior session's scope coverage carries forward. The 2h cache is inherited if still fresh. |
| **Cold-start** | No RESUME.md | Follow the full Session Start protocol (steps 1–7 below) |

**Skills safe to skip on resume** (operative rules already in system instructions):
- `dev-session` — session lifecycle; rules in custom instructions
- `fallback-mode` — model routing; rules in custom instructions

**Skills that must always be invoked when the task requires them** (procedural detail NOT in system instructions):
- `qa-capture-ios` — exact xcrun/simctl commands
- `brand-asset-pipeline` — exact export pipeline steps
- `qa-validate`, `kids-safety`, `risk-review`, `ship-issue` — when task scope requires them

**Context savings:** Skipping `dev-session` + `fallback-mode` skill invocations saves ~523 lines / ~6–8k tokens per session start.

---

1. **Check repository_memories** — review stored facts in the system prompt. Do NOT re-research topics already covered.

2. **Check if a relevant skill exists** for the current task.
   - Prefer the repo skill catalog in `.github/skills/`
   - Use `/skills list` if you need the runtime list

3. **If resuming prior work**, follow the [Resuming Prior Work](#resuming-prior-work) section below.

4. **Check session store** for recent work:
   ```sql
   SELECT s.id, s.summary, s.updated_at
   FROM sessions s
   WHERE s.repository LIKE '%{YOUR_REPOSITORY_PATTERN}%'
   ORDER BY s.updated_at DESC LIMIT 5;
   ```

4b. **Check recent mistake patterns (last 7 days)**:
   ```sql
   SELECT si.content, si.session_id, si.source_type
   FROM search_index si
   JOIN sessions s ON s.id = si.session_id
   WHERE si.search_index MATCH 'FIVE_WHYS_POSTMORTEM OR "severity gate" OR postmortem'
     AND datetime(s.updated_at) >= datetime('now', '-7 days')
   ORDER BY rank
   LIMIT 5;
   ```
   - If results exist, surface one line per hit before work:
     `⚠️ Known mistake patterns (last 7 days): <root cause> [session: <id>]`
   - If no results, skip silently.

4c. **Issue hygiene scan (cold-start, cache-aware):** This step must run on every cold-start — never skipped entirely. A cache hit is a valid outcome (silent skip); a cache miss triggers a full scan. Derive `TOUCHED_REPOS` from session context; if undefined, default to CWD repo only.

   Check cache freshness (2h TTL) — a cache hit from a recent resume's step 3b is valid:
   ```bash
   find .session-state/.issue-scan-cache -mmin -120 2>/dev/null | grep -q .
   ```
   - **Cache hit (exit 0):** skip silently — scan already ran within 2h.
   - **Cache miss (exit non-zero):** for each repo in `TOUCHED_REPOS`, run:
   ```bash
   gh issue list --repo <REPO> --state open --limit 200 --json number,title,labels \
     | jq -r '.[] | "<REPO> #\(.number) \(.title)"'
   ```
   - Open issues: must surface `⚠️` lines to founder.
   - Zero open issues: must emit `✅ Issue hygiene scan: no open issues found (<REPO>)`.
   - `gh` unauthenticated or fails: skip silently — do not block.

5. **dtwin rule surfacing (session-start, cold-start recommended):** Run `python3 -m dtwin list-rules --status pending`. BUILDER adds this to the session-start block; whether to gate on cold-start vs every-resume is BUILDER's discretion (document the choice inline if changing defaults). Apply threshold:
   - Pending count ≥ 10: surface top-5 titles + rule-ids to founder for approve/reject before proceeding.
   - Pending count 5–9: add a one-line note to the session digest ("N dtwin rules pending — review via `list-rules` when convenient") without blocking.
   - Pending count < 5: no action needed.

   Use `python3 -m dtwin get-candidate-rules` for the legacy view if needed. (Note: `list-memories` is **not** a dtwin subcommand — verified 2026-05-18 against CLI surface.)

   **Advisory drift check:** Run `python3 -m dtwin list-rules --status approved | wc -l` and compare roughly to the count of Automatable rows in `automation-registry/SKILL.md`. If the registry is materially longer, remind founder: recent automations may need a paired `python3 -m dtwin add-rule --approve --rule-type workflow "title" "body"`.

6. **Usage check (mandatory, at cold-start):** Run on cold-start — not optional. Savepoint-resume paths (which skip steps 1–7) also skip this check; the cost guard state from the prior session's cold-start persists.

   - **If `COPILOT_PLAN_LIMIT` is NOT set:** Surface this WARNING and keep it visible for the full session (not just at cold-start):
     ```
     ⚠️ COPILOT_PLAN_LIMIT not set — cost guard is disabled. Configure before dispatching premium-tier agents.
     ```
     Drop PLANNER and REVIEWER to `claude-sonnet-4.6 --effort xhigh` — premium-tier (Opus) dispatch is blocked until the variable is configured. Standard-tier (Sonnet) work may continue.

   - **If `COPILOT_PLAN_LIMIT` IS set:** First run **Step A (auto-fallback check)** below, then — unless Step A already entered fallback or blocked — run the existing CONDUCTOR cost-guard checks.

     **Step A — Auto-fallback check (cold-start only):**

     > **Why cold-start only:** This check sets the session posture at session open, so the entire session operates under a consistent model-routing policy from the first subagent dispatch. Mid-session threshold crossings are normally caught by the CONDUCTOR cost-guard (the `--threshold 70` check in the Subagent spawning rules section), which fires before each individual REVIEWER/PLANNER dispatch. **Note:** when fallback-mode is active, CONDUCTOR skips further usage checks by design (`conductor.agent.md`: "fallback-mode is active — hard override — skip usage check"). If the budget exhausts (exit 3) after cold-start during a fallback-mode session, mid-session detection is not available — standard-tier (Sonnet) dispatches will continue. This is an accepted limitation; monitor usage manually when operating near quota.

     1. Read `COPILOT_FALLBACK_THRESHOLD` env var (default: `50`).
     2. **Validate the value** (valid range: 1–50 inclusive):
       - If `> 50` or non-integer or `< 1`: emit the following error and use `50` instead:
         - For `> 50`:
           ```
           ❌ COPILOT_FALLBACK_THRESHOLD must be ≤50 — values above 50% risk failing the Domain 41 threshold policy. Defaulting to 50.
           ```
         - For non-integer or `< 1`:
           ```
           ❌ COPILOT_FALLBACK_THRESHOLD must be a positive integer between 1 and 50. Defaulting to 50.
           ```
     3. Run `scripts/check-copilot-usage.sh --threshold $COPILOT_FALLBACK_THRESHOLD --format json`.
     4. Apply exit-code routing:
        - **Exit 0**: proceed; continue to the CONDUCTOR cost-guard (`--threshold 70`) check below.
          ```bash
          rm -f .session-state/.fallback-state
          ```
          (clears any stale sentinel from a prior crashed session)
        - **Exit 1** (any non-zero exit other than 2 or 3 — script error, API failure, or invalid response): treat as **fail-closed** — enter fallback-mode, same model restrictions as Exit 2, but surface a distinct message attributing fallback to check failure, not budget level. Any JSON status value outside `{ok, warning, over_quota}` should also be treated as fail-closed:
          ```
          ⚠️ Usage check failed or returned an unexpected status — entering fallback-mode as a precaution (fail-closed). Check scripts/check-copilot-usage.sh and COPILOT_PLAN_LIMIT configuration.
          ```
          PLANNER (Opus 15×), REVIEWER (Opus 15×), market-scan (GPT-5.5 7.5×), and any two-pass skill escalating to Opus (reviewer-qa-gate, qa-validate, brand-compliance) will use claude-sonnet-4.6 for this session. Skip the `--threshold 70` check below.
          ```bash
          mkdir -p .session-state/ && echo '{"reason":"check-failed","timestamp":"'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}' > .session-state/.fallback-state
          ```
          > **Note:** Manual `/fallback-mode` must also write this sentinel so savepoint/resume restores fallback posture consistently. `/fallback-mode-off` clears the same file.

          `.session-state/` is relative to the session repo root — the same cwd used for `.session-state/RESUME.md`.
        - **Exit 2** (≥ `$COPILOT_FALLBACK_THRESHOLD`% burn): surface the following message, mark the session as in fallback-mode, and **skip** the `--threshold 70` check below (it is moot — fallback is already active):
          ```
          ⚠️ Budget ≥{THRESHOLD}% used — entering fallback-mode automatically. PLANNER (Opus 15×), REVIEWER (Opus 15×), market-scan (GPT-5.5 7.5×), and any two-pass skill escalating to Opus (reviewer-qa-gate, qa-validate, brand-compliance) will use claude-sonnet-4.6. CONDUCTOR applies fallback-mode rules for this session.
          ```
          ```bash
          mkdir -p .session-state/ && echo '{"reason":"budget>='"$COPILOT_FALLBACK_THRESHOLD"'%","threshold":'"$COPILOT_FALLBACK_THRESHOLD"',"timestamp":"'"$(date -u +"%Y-%m-%dT%H:%M:%SZ")"'"}' > .session-state/.fallback-state
          ```
          > **Note:** Manual `/fallback-mode` must also write this sentinel so savepoint/resume restores fallback posture consistently. `/fallback-mode-off` clears the same file.

          `.session-state/` is relative to the session repo root — the same cwd used for `.session-state/RESUME.md`.
        - **Exit 3** (over quota): surface the following message and block all premium/extra-premium dispatch for the session. Skip the `--threshold 70` check below — budget is exhausted.
          ```
          🛑 Budget exhausted — premium tier (PLANNER, REVIEWER at Opus 15×), extra-premium tier (market-scan at GPT-5.5 7.5×), and Opus escalation in two-pass skills (reviewer-qa-gate, qa-validate, brand-compliance) are blocked for this session.
          ```
          ```bash
          mkdir -p .session-state/ && echo '{"reason":"over-quota","timestamp":"'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}' > .session-state/.fallback-state
          ```
          > **Note:** Manual `/fallback-mode` must also write this sentinel so savepoint/resume restores fallback posture consistently. `/fallback-mode-off` clears the same file.

          `.session-state/` is relative to the session repo root — the same cwd used for `.session-state/RESUME.md`.

     **CONDUCTOR cost-guard (run only if Step A did not enter fallback or block):** Run `scripts/check-copilot-usage.sh --model opus --threshold 70` unconditionally before dispatching REVIEWER/PLANNER subagents. For extra-premium (gpt-5.5) sessions, also run `scripts/check-copilot-usage.sh --tier extra-premium --threshold 70`. Apply exit-code routing:
     - Exit 0 = proceed normally; no restriction applied.
     - Exit 1 (script or API error): Surface this WARNING and block premium-tier dispatch:
       ```
       ⚠️ Usage check failed or unavailable — cost guard inactive. Premium-tier agents (PLANNER, REVIEWER at Opus) are blocked until the check succeeds or COPILOT_PLAN_LIMIT is configured correctly.
       ```
       Standard-tier (Sonnet) work may continue.
     - Exit 2 = apply the fallback for the checked tier (premium → drop REVIEWER/PLANNER to standard; extra-premium → drop the market-scan route to `claude-sonnet-4.6 --effort xhigh` + rubber-duck).
     - Exit 3 = block the checked tier (see `/fallback-mode`).

   See `.github/skills/usage/SKILL.md`.

7. **TickTick Inbox nudge (cold-start only):** Check whether the TickTick Inbox has unrouted items.

   ```bash
   source ~/.config/foculoom/ticktick.env 2>/dev/null
   curl -s "https://api.ticktick.com/open/v1/project/${TICKTICK_INBOX_ID}/data" \
     -H "Authorization: Bearer $TICKTICK_ACCESS_TOKEN" 2>/dev/null \
     | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('tasks',[])))" 2>/dev/null
   ```

   - If the count is **≥ 1**: surface `📥 N item(s) in TickTick Inbox — run /triage to route them.`
   - If the count is **0** or the call fails: skip silently. Do not surface errors.
   - This is a nudge only — do not invoke `/triage` automatically.

8. **Do NOT re-run setup** that was completed in prior sessions:
   - Do not re-clone repos
   - Do not re-install dependencies unless there's evidence they changed
   - Do not re-validate repo structure

## Resuming Prior Work

Follow these steps in order to resume work efficiently.

### Step 1: Load prior context from digital twin

Call `tom-continuationPrompt` with the topic or issue number. This returns a context pack from all prior sessions.

If no topic is provided, call `tom-continuationPrompt` without a topic to get the most recent work context.

### Step 2: Query session store for recent sessions

```sql
SELECT s.id, s.branch, s.summary, s.updated_at
FROM sessions s
WHERE s.repository LIKE '%{YOUR_REPOSITORY_PATTERN}%'
ORDER BY s.updated_at DESC
LIMIT 5;
```

### Step 3: Check GitHub Issue state

If an issue number is known:

```bash
gh issue view <N> --repo {YOUR_REPO} --json state,title,body,labels
```

If no issue is specified, check for open issues:

```bash
gh issue list --repo {YOUR_REPO} --state open --limit 10
```

3b. **Issue hygiene scan (resume, cache-aware, 2h TTL):**

Check cache freshness first:

```bash
find .session-state/.issue-scan-cache -mmin -120 2>/dev/null | grep -q .
```

- **Cache hit (exit 0):** skip silently. *(2h cache — re-run with --refresh to force)*
- **Cache miss (exit non-zero):** proceed with scan below.

If `.issue-scan-cache` exists but JSON parse fails, treat as cache miss — malformed cache is re-scanned silently (no parse error emitted to user).

Derive `TOUCHED_REPOS` from session context (repos touched or referenced in this session). If `TOUCHED_REPOS` is undefined, default to the CWD repo only.

For each repo in `TOUCHED_REPOS`:

```bash
mkdir -p .session-state/
gh issue list --repo <REPO> --state open --limit 200 --json number,title,labels \
  | jq -r '.[] | "<REPO> #\(.number) \(.title)"' \
  > .session-state/.issue-scan-cache.tmp 2>/dev/null \
  && mv .session-state/.issue-scan-cache.tmp .session-state/.issue-scan-cache
```

- Open issues: must surface `⚠️` lines to founder.
- Zero open issues: must emit `✅ Issue hygiene scan: no open issues found (<REPO>)` (never silent on zero).
- `gh` unauthenticated or fails: skip silently — do not block (same pattern as step 7 TickTick nudge, not the blocking pattern of step 6 usage check).
- Must NOT write `.issue-scan-cache` if `gh` or `jq` fails — atomic write (`.issue-scan-cache.tmp` → `mv`) ensures partial writes are never read as valid.

### Step 4: Determine what's done and what remains

Compare the digital twin context, session store, and issue state. Identify:
- What was completed in prior sessions
- What remains to be done
- Any blockers or dependencies

### Step 5: Begin work from the current state

Do NOT redo completed steps. Start from where the prior session left off.

## During Session

### Context budget: context-health checkpoints

Context % used (from `/context`) is the **primary** lifecycle signal. Turn count is a safety cap only — not the primary estimate. A heavy REVIEWER pass loads ~8 KB; a lightweight status check loads ~0.5 KB. Evaluate context health at fixed checkpoints instead of auto-stopping at a fixed turn count.

> **Cloud-agent scope note:** `/context` is unavailable in cloud-agent sessions (`copilot-instructions.md:263`). Cloud-agent sessions retain turn-based checkpoints as primary signal; %-context rules apply to local-CLI sessions only.

**When to run `/context` (by turn — safety-cap triggers):**

| Turn | Trigger |
|---|---|
| **Turn 5** | Always — compact if context > 50% used (> 40% in fallback) |
| **Turn 10** | Always — apply context threshold table below |
| **Turn 15** | Hard ceiling (unconditional safety cap) — wind down regardless of context % |

**Context threshold table (apply at Turn 10 reading):**

| Context used | Action |
|---|---|
| **< 60%** | Extend wind-down to turn 14; continue dispatching |
| **60–75%** | Compact + extend to turn 12; flag quality risk |
| **> 75%** | Wind-down mandatory regardless of turns remaining |

**Pre-compaction reading is authoritative.** If you compact at turn 10 and context drops from 65% to 30%, the extension decision is still "compact + extend to turn 12" (based on the 65% pre-compaction reading). Post-compaction reading informs quality risk only.

**Missed checkpoints:** if turn 10 passed without a `/context` check, run it immediately at the current turn and apply the strictest applicable rule. If the current turn is ≥ 15, wind down unconditionally.

**Fallback mode** tightens all thresholds by 10 percentage points:

| Context threshold | Normal | Fallback |
|---|---|---|
| Turn 5 compact threshold | > 50% | > 40% |
| Turn 10: extend to turn 14 | < 60% | < 50% |
| Turn 10: compact + extend to turn 12 | 60–75% | 50–65% |
| Turn 10: mandatory wind-down | > 75% | > 65% |
| Turn 15 hard ceiling (safety cap) | always | always |

**Multi-signal stop predicates** — wind-down or fan-out triggers on any of:

| Signal | Threshold | Action |
|---|---|---|
| (a) Token budget hard ceiling | > 75% used (> 65% fallback) | Halt — wind-down mandatory |
| (b) Token budget soft threshold | > 60% used | Compact (per checkpoint table); if no progress after compact → wind-down. Low-progress signal (≤ 1 atomic task remaining or no AC delta since last compact) escalates to wind-down sooner. |
| (c) Wall-clock warning | Approaching session time limit | Wind-down and checkpoint |
| (d) Cost cap | `/usage` exits 2 (≥70% burn on checked tier) or exit 3 (over quota on checked tier) | Exit 2: drop one cost tier for the affected route (premium → REVIEWER/PLANNER to standard; extra-premium → market-scan/gpt-5.5 route; see `/fallback-mode`); exit 3: block the checked tier |
| (e) Repetition | ≥ 3 identical tool calls | Wind-down or fan-out to fresh subagent |
| (f) Error rate | > 5% of tool calls failing | Wind-down or fan-out |

See `fallback-mode` skill and `.github/agents/conductor.agent.md` § Subagent spawning rules → Wind-down buffer for CONDUCTOR enforcement of these checkpoints.

### Proactive compaction

Do NOT wait for auto-compaction at 95%. In normal mode, compact proactively around 50–60%. In fallback mode, compact at 40–50%. The checkpoint table above defines when compaction is mandatory.

### Savepoint pattern (preferred over /compact)

A savepoint fully resets context by writing a structured handoff file, running `/clear`, and reloading. This is **4–8× more context-efficient than `/compact`** because `/compact` leaves 20–40k tokens of residual summary whereas a savepoint starts from a clean slate with only the explicitly reloaded content.

#### RESUME.md format

Keep RESUME.md **≤ 1 500 words / ≤ 8 000 tokens**. Use exactly these four named fields (additional fields are allowed but these four are required):

```markdown
# RESUME.md — <issue or task title>

## Completed items
- <bullet per completed atomic task, past-tense, one line each>

## Next items
- <bullet per remaining atomic task in priority order>

## Open blockers
- <bullet per unresolved dependency or blocker; "None" if clear>

## Context-critical facts
- <bullet per non-obvious fact that a fresh context would not know: file paths,
  decisions made, rejected approaches, environment quirks, branch name, PR URL>
```

#### Command sequence

> **Scratch state:** RESUME.md is ephemeral session state — do not stage or commit it. Preferred path is `.session-state/RESUME.md` (already gitignored). A root-level `RESUME.md` is also gitignored as a belt-and-braces guard.

1. **Before `/clear`:** complete any required session-end obligations for this repo (e.g., `tom-syncTwin` if applicable). If obligations cannot be completed before the reset, capture them as bullets in **Context-critical facts** so the fresh context knows to run them.
2. Write `.session-state/RESUME.md`: use `edit` or `create` at path `.session-state/RESUME.md`.
3. Run `/clear` — this resets the context window completely.
4. At the top of the new session, reload: `view .session-state/RESUME.md`.
5. Re-read every file listed under **Context-critical facts** before resuming work.
6. Continue work from **Next items**.

#### Prefer savepoint vs. /compact decision rule

| Condition | Action |
|---|---|
| Remaining work > 2 atomic tasks **or** fresh-context benefit outweighs compaction residual (e.g., complex multi-file change, premium model swap) | **Use savepoint** — write RESUME.md → `/clear` → reload |
| One small remaining task (≤ 1 atomic step) **or** savepoint setup cost > benefit (e.g., mid-turn emergency compaction, context spike from a single large read) | **Use `/compact`** — faster, lower overhead for short remaining work |
| Approaching Turn 15 hard ceiling with multiple tasks left | **Use savepoint** — do not compress into a lossy summary when significant work remains |
| Fallback mode active (cost-tier step-down) | **Prefer savepoint** — standard-tier models degrade more on residual summaries; clean context recovers more quality |

> **Rule of thumb:** if you would need to compact more than once to finish, use savepoint instead.

### Parallel-execution worktree guard

When running parallel BUILDER work in the same repo, each BUILDER MUST run in its own linked worktree. Single-checkout parallel dispatch is FORBIDDEN.

Pre-dispatch checklist:

1. Run `git worktree list`.
2. If the target issue branch already has a linked worktree, reuse it.
3. Otherwise create one:
   `git worktree add ../<repo>-issue-<N> -b feature/issue-<N>-<slug>`
4. Pin the absolute `WORKTREE_PATH` in the spawn prompt.
5. If an absolute `WORKTREE_PATH` cannot be determined, stop and do not dispatch.

Anchor-validation clause: before inserting this guard, verify `### Proactive compaction` and `### Wind-down protocol` anchors exist. If future restructuring changes those headings, place this guard in the equivalent `## During Session` lifecycle section and do not duplicate it.

### Wind-down protocol (context-health triggers)

Wind-down begins when any of these conditions is met (using pre-compaction context reading):
- Turn 10 check: context > 75% used (> 65% in fallback mode)
- Turn 15: hard ceiling (safety cap) — wind down unconditionally regardless of context %

When wind-down triggers, **stop accepting new work** and begin the wind-down sequence:

1. **Stop dispatching** — do not spawn new subagents or start new tasks.
2. **Let in-flight work finish** — wait for any background subagents to reach a safe checkpoint.
3. **Store memories** — call `store_memory` for every significant discovery this session.
4. **Update plan.md / issue state** — capture remaining work and blockers in the GitHub issue.
5. **Return to default branch** — follow the § Session End checklist below.
6. **Checkpoint** — call `tom-syncTwin` to persist context for the next session.

**CONDUCTOR ownership:** when CONDUCTOR is driving, it owns this sequence. CONDUCTOR must surface `⚠️ WIND-DOWN: context-health checkpoint triggered — beginning end-of-session sequence` (appending the reason, e.g., `turn 10 >75%` or `turn 15 hard ceiling`) before wind-down starts, so the founder can redirect if needed. Do NOT start a new issue during wind-down.

### Model selection

Use the Model Routing Matrix below as the single source of truth for picking a model per skill or agent. It supersedes the prior bullet list.

<!-- Last verified against Copilot CLI v1.0.61 on 2026-06-11 -->
**Last verified:** Copilot CLI **v1.0.61** on 2026-06-11 (foculoom/foculoom-project#1760; refreshed audit metadata, re-checked Auto pool and GPT-5.5 multiplier, logged current task-model enum mismatch for founder routing decision). Previous: v1.0.59 on 2026-06-03 (foculoom/foculoom-project#1630; no model roster changes, no tier drift detected). Refresh via the `model-audit` skill (#464) every 7 days (or after any `copilot update` bump, or on any GitHub Copilot changelog entry mentioning model/auto/deprecat/pricing) — see #928 for rationale.

#### Tier Taxonomy (canonical)

Every agent profile and skill SKILL.md declares its tier as follows: skill `SKILL.md` files use a `tier:` YAML front-matter field; agent `.agent.md` files use an HTML-comment marker `<!-- tier: <value> -->` immediately after the front-matter close (the Copilot CLI custom-agent loader rejects unknown front-matter fields, so `tier:` cannot live in `.agent.md` front-matter; a prior loader regression established this split declaration form). The Matrix's "Preferred Model" column is the authoritative routing; the tier label is a declarative summary for cost-guard gating, allowlisting, and audit. Two-pass skills (`reviewer-qa-gate`, `qa-validate`, `brand-compliance`) declare `tier: two-pass` and use multiple models per the Matrix row.

| Tier | Label | Default model | Multiplier (PRU-era¹) | Used by |
|---|---|---|---|---|
| 1 | **basic** | `claude-haiku-4.5` | 0.33× | usage, model-audit, automation-registry, llc-ops, qa-capture-ios, 5-whys, release-asset-fanout, a11y-godot (OUTLINE), status (Quick mode default) |
| 2 | **standard** | `claude-sonnet-4.6` | 1× | BUILDER, CONDUCTOR, dev-session, ship-issue, brand-asset-pipeline, release-post, fallback-mode, kids-safety, new-blog-posts, status (Full mode) |
| 3 | **premium** | `claude-opus-4.8` | 15× | PLANNER, REVIEWER, new-feature, risk-review |
| 4 | **extra-premium** | `gpt-5.5` | 7.5× | market-scan |
| — | **two-pass** | per Matrix row | mixed | reviewer-qa-gate (Sonnet+Opus), qa-validate (Sonnet+Opus), brand-compliance (Sonnet+Opus) |

> ¹ Multiplier values are PRU-era figures. GitHub switched to AI Credits billing effective 2026-06-01. Re-verify rates at https://github.com/pricing/calculator before making cost decisions.

> **Cost-guard mapping** (`scripts/check-copilot-usage.sh --tier <label>`): basic → `*haiku*`, standard → `*sonnet*`, premium → `*opus*`, extra-premium → `gpt-5.5`. Backward-compatible with `--model <glob>`.

#### Model Routing Matrix

| Skill / Agent | Preferred Model | Reason | Cost-Tier Fallback |
|---|---|---|---|
| **agent: planner** | `claude-opus-4.8` | Strategy, spec writing, content judgment | premium → standard: `claude-sonnet-4.6` + `--effort xhigh` + mandatory rubber-duck |
| **agent: builder** | `claude-sonnet-4.6` | Implementation and build/test at standard tier | standard → basic: `/model claude-haiku-4.5` (no effort flag); or `/model auto` → `claude-sonnet-4.5` |
| **agent: reviewer** | `claude-opus-4.8` | Visual/business judgment, deep audits | premium → standard: `claude-sonnet-4.6` + `--effort xhigh` + rubber-duck before every quality verdict |
| **agent: conductor** | `claude-sonnet-4.6` | Orchestration, gate reasoning, subagent dispatch — deliberately pinned to standard tier by founder 2026-05-24 (prev: gpt-5.5) | standard → basic: `claude-haiku-4.5` (no effort flag); REVIEWER/PLANNER subagents: premium → standard per fallback-mode SKILL |
| `a11y-godot` | `claude-haiku-4.5` (while OUTLINE per #947); upgrade to `claude-sonnet-4.6` post-spike | Placeholder checklist; minimal judgment required pending SPIKE-A11Y closure | `claude-haiku-4.5` (while OUTLINE); `/model auto` → `claude-sonnet-4.5` post-#947 |
| `automation-registry` | `claude-haiku-4.5` | Reference lookup, mechanical | `claude-haiku-4.5` (already cheap) |
| `brand-asset-pipeline` | `claude-sonnet-4.6` | Visual judgment + tool orchestration | `/model auto` → `claude-sonnet-4.5` |
| `brand-compliance` | `claude-sonnet-4.6` (checklists); `claude-opus-4.8` for Social Media Art-Director Review (§8) | Visual/brand review; qualitative Art-Director judgment for social | `/model auto` → `claude-sonnet-4.5`; `claude-sonnet-4.6 --effort xhigh` + rubber-duck for Opus-escalation |
| `dev-session` | `claude-sonnet-4.6` | Session orchestration | `/model auto` → `claude-sonnet-4.5` |
| `fallback-mode` | `claude-sonnet-4.6` | Self-referential: the skill IS the fallback | n/a (already at fallback tier) |
| `kids-safety` | `claude-haiku-4.5` (trivial features only — no data/AI/IAP/UGC); `claude-sonnet-4.6 --effort xhigh` default for non-trivial features | COPPA/KOSA per-feature checklist; $50k/violation risk warrants Sonnet default when feature touches any trigger surface | `claude-sonnet-4.6` + `--effort xhigh` + rubber-duck |
| `llc-ops` | `claude-haiku-4.5` | Checklist / date lookup | `claude-haiku-4.5` (already cheap) |
| `market-scan` | `gpt-5.5` | Research + competitive analysis | extra-premium → standard: `claude-sonnet-4.6` + `--effort xhigh` + rubber-duck |
| `model-audit` | `claude-haiku-4.5` | Version diff + template generation | `claude-haiku-4.5` (already cheap) |
| `new-blog-posts` | `claude-sonnet-4.6` | Web search + HTML content gen + PR orchestration | `/model auto` → `claude-sonnet-4.5` |
| `new-feature` | `claude-opus-4.8` | PLANNER intake decisioning | premium → standard: `claude-sonnet-4.6` + `--effort xhigh` |
| `qa-capture-ios` | `claude-haiku-4.5` | Mechanical `xcrun` commands | `claude-haiku-4.5` (already cheap) |
| `qa-validate` | `claude-sonnet-4.6` (CLI/platform steps); `claude-opus-4.8` for Sprite Art Gate (§2.5), Walk-Cycle Receipt Subgate (§2.5.1), Art Director Visual Review (§3.5) | Platform detection + test runs; ADA-class visual judgment for art gates | `/model auto` → `claude-sonnet-4.5`; `claude-sonnet-4.6 --effort xhigh` + rubber-duck for Opus-escalation steps |
| `risk-review` | `claude-opus-4.8` | Sensitive judgment (health/legal/kids) | premium → standard: `claude-sonnet-4.6` + `--effort xhigh` + rubber-duck |
| `5-whys` | `claude-haiku-4.5` | Mechanical root-cause template; escalate when root cause is disputed | `claude-sonnet-4.6` for severity gates (i)-(iii) or disputed root cause |
| `release-asset-fanout` | `claude-haiku-4.5` | Pure script runner (Pillow resize + manifest JSON write); zero judgment | `claude-haiku-4.5` (already cheap) |
| `release-post` | `claude-sonnet-4.6` | Content gen + tool orchestration | `/model auto` |
| `reviewer-qa-gate` | Two-pass: `claude-sonnet-4.6` (items 1–12, 17–20) + `claude-opus-4.8` (items 13–16 HARD-FAIL legal/IP) | Cost-optimized: Sonnet for layout/a11y/polish/kids-product gates; Opus only for mascot visual/voice + legal/IP gate | `claude-sonnet-4.6` + `--effort xhigh` (all items); founder MAY opt into single-Opus pass for operational simplicity |
| `ship-issue` | `claude-sonnet-4.6` | BUILDER workflow | `/model auto` → `claude-sonnet-4.5` |
| `status` | `claude-haiku-4.5` (Quick mode); `claude-sonnet-4.6` (Full mode) | Quick = JSON scan + label classification (mechanical); Full = cross-repo daily brief synthesis | `claude-haiku-4.5` for both modes |
| `usage` | `claude-haiku-4.5` | Mechanical API call — billing usage check | `claude-haiku-4.5` (already cheap) |

> ⚠️ **Deprecation tracking:** `gpt-5.2`, `gpt-5.2-codex`, and `gpt-4.1` remain intentionally unlisted in routing rows. Verify current task-tool enum presence during each `/model-audit` and remove stale notes once retired.

#### MCP Tool Inventory (audio/image/TTS)

Registered in `~/.copilot/mcp-config.json`. All output paths are under `~/{YOUR_ORG}/infra/{YOUR_BRAND_ASSET_PATH}`.

| MCP Server | Tool(s) | Use for | Output path |
|---|---|---|---|
| `openai-image` | `openai-image-create-image`, `openai-image-edit-image` | Brand marks, OG images, concept art | `assets/generated/` |
| `fal-ai` | `fal-ai-flux-pro-kontext-max-*` | Multi-frame sprites, reference-consistent characters | `assets/generated/` |
| `suno` | `suno-*` | Music, jingles, game audio suites | `assets/audio/generated/` |
| `elevenlabs` | `elevenlabs-text-to-speech`, `elevenlabs-list-presets` | TTS voice assets (onboarding, readback, narration) | `assets/audio/generated/elevenlabs/{preset}/` |

**ElevenLabs presets → products:** map your preset names to your own product lines in your MCP README or ops docs. Soft monthly cap $5/mo; every generated file must pass REVIEWER before entering a product repo. Voice cloning is out of scope — requires `/risk-review`. See your ElevenLabs MCP README for the full registry.

**How to use:**
- Switch with `/model <id>` or pass `model: "<id>"` when invoking a sub-agent via the `task` tool.
- "Cost-Tier Fallback" applies when spend on the current model tier needs to be reduced; full recipe lives in the `fallback-mode` skill (#463).
- Per-skill `## Model` blocks (#462) repeat the same values inline; on conflict, this matrix wins.
- **Audit note (2026-06-11 / foculoom-project#1760):** In this runtime on CLI v1.0.61, the `task` tool schema exposed three pin-able IDs: `gpt-5.3-codex`, `gpt-5.4-mini`, and `gpt-5-mini`. This runtime observation can diverge from docs tables (`auto-model-selection.yml` and changelog notes), so Matrix rows were left unchanged and escalated for founder routing decision. `auto-model-selection.yml` still reports the 6-model CLI Auto pool (Sonnet 4.6, Haiku 4.5, GPT-5.4, GPT-5.3-Codex, GPT-5.4 mini, GPT-5 mini). `model-multipliers.yml` still reports GPT-5.5 at 7.5×. Copilot CLI 1.0.61 changelog includes "Add support for Claude Fable 5 model"; no stable task-enum ID was confirmed in this runtime.
- **Audit note (2026-05-20 / #1231):** All explicit task-tool model IDs referenced in the matrix are still present in the current `task` tool roster (v1.0.51 enum: 14 IDs — unchanged from v1.0.48; of which 3 — `gpt-5.2`, `gpt-5.2-codex`, `gpt-4.1` — are deprecated effective June 1, 2026; post-June-1 audit will confirm their removal and reduce the count to 11). Additional exposed IDs — `gpt-5.4`, `gpt-5.4-mini`, `gpt-5-mini` (plus the 3 deprecated above) — remain intentionally unlisted here because no skill currently recommends them as the preferred or fallback route. Auto pool unchanged at 6 models. Raptor mini appeared in Auto-pool YAML with cli:false — no task enum entry, no Matrix action needed. Claude Opus 4.6 (fast mode) (preview) appears in `model-supported-clients.yml` as cli:true but is not exposed as a pin-able task enum ID; no Matrix row will be added until a stable ID is exposed in the task tool enum. GPT-5.5 multiplier confirmed at 7.5× via `model-multipliers.yml` (fetched 2026-05-18); must be re-verified post-June-1 because GitHub docs state multipliers/costs are subject to change.
- **Audit note (2026-05-30 / foculoom-project#1528):** `claude-opus-4.8` is now the premium-tier model as of CLI v1.0.56. All Matrix rows and agent front-matter pins updated from `claude-opus-4.7`. Task tool enum counts **14 IDs** (unchanged from v1.0.54). Auto pool still **6 models** — does not include Opus tier. `gpt-5.2`, `gpt-5.2-codex`, and `gpt-4.1` scheduled for removal effective June 1, 2026 — confirm removal via `/model-audit` post-June-1. **2026-06-01 audit:** gpt-5.2, gpt-5.2-codex, gpt-4.1 still present in task tool enum as of CLI v1.0.56 on 2026-06-01. Removal not yet confirmed. Re-check at next 7-day audit.
- **Audit note (2026-05-31 / foculoom-project#1550):** On `/model-audit` verification (CLI v1.0.56), the live `task` tool enum was observed at **14 IDs** with `claude-opus-4.7` absent from the enum. The 2026-05-30 note has been corrected: count updated 15 → 14 and the assertion that `claude-opus-4.7` remained a valid task enum ID has been removed. Remediation: doc-accuracy only. No causal story asserted (whether the CLI removed the ID within-patch or the note was inaccurate when written is not established here).
- **Audit note (2026-05-24 / #1382):** `claude-opus-4.6` and `claude-opus-4.5` are now pin-able task enum IDs as of CLI v1.0.54 (no longer preview/unexposed). Both are intentionally unlisted in this Matrix — no skill currently recommends them as a preferred or fallback route; all Opus-tier routing uses `claude-opus-4.8`.
- **Auto model selection (GA 2026-04-17; server-side routing since v1.0.43):** `/model auto` is a viable alternative for most Standard-tier and Mechanical-tier skills. It routes dynamically among models with ≤1× multipliers, chosen in real time by GitHub server-side logic — pool composition can change without a CLI version bump. As of 2026-05-06 (`github/docs` commit [`98afef20`](https://github.com/github/docs/blob/main/data/tables/copilot/auto-model-selection.yml)) the CLI Auto pool contains 6 models: Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4, GPT-5.3-Codex, **GPT-5.4 mini**, **GPT-5 mini**. Authoritative live list: [`auto-model-selection.yml`](https://github.com/github/docs/blob/main/data/tables/copilot/auto-model-selection.yml). Paid plans receive a 10% multiplier discount on Auto responses. Auto **cannot reach Opus 4.8** — all Opus-tier skills must stay on explicit model IDs. Keep explicit `claude-haiku-4.5` for any task where zero-premium spend is required.
- **Guardrail:** do not pair sticky `--effort xhigh` with `/model auto` (notably inside `/fallback-mode`). Auto may route to `claude-haiku-4.5`, which rejects reasoning effort and can fail the request.

## Session End

Run these steps before ending any session. Each step takes < 1 minute.

### 1. Store new learnings

For each significant discovery this session, call `store_memory`:

- **Error resolutions** — what broke, what fixed it, why
- **Build/QA commands** — exact commands that worked (or didn't)
- **Procedures refined** — capture steps, deployment gotchas
- **Brand/design decisions** — confirmed choices, rejected alternatives
- **MCP/tool configuration** — env vars, paths, flags that matter

Skip if the session was purely research with no new actionable facts.

### 2. Sync digital twin

> ⚠️ **Availability check required before skipping:** call `tool_search_tool_regex` with pattern `tom.*sync|syncTwin` **before** declaring this step unavailable. Never skip based on memory alone — the tool is an MCP tool, not a CLI command, and is available whenever the MCP server is running. Only skip with an explicit "tool not found" result in hand.

Use the `tom-syncTwin` MCP tool with `mode: "incremental"`.

This ensures the next session can retrieve context from this one via `tom-continuationPrompt`.

### 3. Return to default branch

Before branch cleanup, the repo must be back on its real default branch or fail
with an explicit blocker:

- `origin/HEAD` must resolve to a stable default branch, not a feature or WIP branch
- detached HEAD state is non-compliant
- a dirty non-default branch is non-compliant because session-end cannot switch safely
- if the default branch is checked out in another linked worktree, stop and surface it
- in your tracking repo, session-end is also non-compliant when the default branch is ahead of, behind, or diverged from upstream
- in your tracking repo, local-only spec/workflow commits that reference already-closed issues must land through a reviewable path or remain attached to an explicit open landing step before issue closeout

### 4. Clean merged local branches

If you merged a feature branch during this session, clean it up locally before
stopping:

```bash
scripts/cleanup-redundant-local-branches.sh feature/issue-N-short-description
scripts/cleanup-redundant-local-branches.sh --apply feature/issue-N-short-description
```

- Run the dry-run first.
- Only apply once the branch is confirmed redundant and any linked worktree is
  clean.
- If the current repo does not have this helper, use the repo-native equivalent
  cleanup flow before ending the session.

### 5. Update issue state

If working on a GitHub Issue, add a progress comment:

```bash
gh issue comment <N> --repo {YOUR_REPO} --body "Progress: <what was done, what remains>"
```

### 6. Note incomplete work

If work is unfinished, ensure:
- The session summary captures what remains
- Any blocking issues are documented
- The GitHub Issue reflects current state
- Any tracking-repo issue with local-only spec/workflow commits is either still attached to an explicit open landing step or not closed yet
- Any hook warning about a dirty worktree is addressed by either committing the intended changes, handing the work off to BUILDER or `/delegate`, or explicitly calling out why the files remain uncommitted

### 6b. Run severity-gate completion check

Scan current session turns for correction markers: `wrong`, `mistake`, `I should have`, `apologies`, `bad premise`, `fixed`, `root cause`, `severity gate`.

- If candidates are found, surface:
  `⚠️ Candidate severity-gate events detected this session — please confirm 5-whys is filed on the related issue, or mark as excluded (typo / retried tool call / pre-founder-visible self-correction).`
- If none are found, state:
  `No severity-gate events detected this session.`

**Untracked-file disposition protocol:**
For each untracked file shown by `git status --short`:
1. Identify the linked issue (from file content, filename, or session context).
2. If the linked issue is **OPEN** and the approach is still live → label "needs commit or issue + PR".
3. If the linked issue is **CLOSED** or the approach was abandoned → default to **delete-confirm**: surface to founder, then delete if approved. Do NOT create a new tracking issue.
4. If no linked issue can be found → surface to founder for disposition. Do not assume it should be committed.

### 7. Clear fallback-mode sentinel

Delete the fallback-mode sentinel file if present — this ensures the next session starts without a stale fallback posture:

```bash
rm -f .session-state/.fallback-state
```

### `.dtwin/` protected artifact protocol

Treat `.dtwin/` as protected AI-infra state, not generic scratch/residue.

Before any cleanup/disposition claim about `.dtwin/`, verify from the repo root:
1. **dtwin CLI behavior** (both forms are valid):  
   `python3 -m dtwin list-rules --status pending`  
   `python3 -m dtwin --repo-root "$PWD" list-rules --status pending`
2. **Local `.dtwin/dtwin.db` state** — confirm schema/tables and row counts are readable.
3. **Canonical dtwin DB comparison** — check your canonical shared dtwin database path (for example, `{YOUR_DTWIN_DB_PATH}`) and compare state.
4. **Git visibility/ignore state** — run `git status --untracked-files=all .dtwin` and `git check-ignore` for `.dtwin` artifacts.

Do not delete `.dtwin/`, `dtwin.db`, `dtwin.db-shm`, or `dtwin.db-wal` without explicit founder approval and a replacement ignore/state policy.

## Choosing CONDUCTOR vs individual agents

For multi-role work, prefer CONDUCTOR (`.github/agents/conductor.agent.md`). It spawns PLANNER/BUILDER/REVIEWER as subagents and stops only at named founder gates. Use individual agents only for single-role asks.

CONDUCTOR runs the mandatory plan-critique checkpoint (REVIEWER critiques plans) and pre-PR diff review automatically — these are blind-spot catchers, not nice-to-haves.

## Anti-patterns

- Sessions longer than 15 turns (quality drops sharply)
- Waiting for auto-compaction at 95% (loses critical early context)
- Not syncing twin at end of session (next session starts blind)
- Using Opus 4.8 for routine work (15× vs 1× Sonnet 4.6; Opus 4.5/4.6 are 3×; Opus 4.6 fast mode preview is 30× and is not task-enum pin-able as of v1.0.51). Re-verify regularly because model multipliers and costs are subject to change.
- Re-discovering facts already in repository_memories
- Re-cloning repos that already exist locally
- Re-running setup completed in prior sessions
- Re-discovering procedures encoded in skills (QA capture, brand pipeline, etc.)
- Investigating from scratch without checking `repository_memories` first
