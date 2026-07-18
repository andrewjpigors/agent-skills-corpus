---
name: scheduled-run
description: Wrapper for scheduled playbooks - handles git sync before and after execution
argument-hint: <playbook-name>
automation: autonomous
allowed-tools: Bash, Skill
user-invocable: true
---

# Scheduled Run

Wrapper that runs any playbook with git sync. Use this for all scheduled executions to ensure:
- Latest changes pulled before running
- All changes committed and pushed after running

## Purpose

Ensures scheduled playbooks on Trinity stay in sync with the GitHub repository.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Git repo | `.git/` | ✓ | ✓ | Pull before, commit+push after |
| Playbook output | varies | | ✓ | Whatever the playbook produces |

## Arguments

`$ARGUMENTS` = The playbook name to run (e.g., `refresh-index`, `coherence-sweep`)

## Process

### Step 1: Pull Latest Changes

```bash
git pull --rebase
```

If conflicts, abort and log error. Do NOT run the playbook on a dirty tree.

### Step 2: Run the Playbook

Scheduled playbooks run at the **core** read-scope by default. `BRAIN_READ_SCOPE`
is unset here, so every `run_search.sh` / `run_connections.sh` call inside the
playbook fails closed to `core` (the fingerprint) - which is the intended scope
for incubation-loop, refresh-index, coherence-sweep, gjopen-refresh, and
ai-crystallize. Perception/cross-domain playbooks that legitimately need non-core
content (e.g. **domain-watch**) set a wider `BRAIN_READ_SCOPE=...` inline on their
own search commands; do not widen it here. (Setting `export BRAIN_READ_SCOPE=core`
here would be a redundant fail-safe - the default is already core - and would not
propagate across the separate Bash invocations a playbook makes anyway.)

Invoke the specified playbook using the Skill tool:

```
Skill: $ARGUMENTS
```

Wait for completion.

### Step 3: Check for Changes

```bash
git status --porcelain
```

If no changes, skip to completion.

### Step 4: Commit Changes

```bash
git add -A && git commit -m "$(cat <<'EOF'
Scheduled: $ARGUMENTS $(date '+%Y-%m-%d %H:%M')

Automated execution via /scheduled-run

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 5: Push to Remote

```bash
git push
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Pull fails (conflicts) | Abort, log error, do not run playbook |
| Playbook fails | Still attempt commit/push of partial changes |
| Push fails | Log error, changes remain local |

## Autonomy Guide

**What should be scheduled (mechanical, no creative decisions):**

| Schedule | Command | Cron (UTC) | Timeout | Purpose |
|----------|---------|------------|---------|---------|
| Incubation Loop | `/scheduled-run incubation-loop` | `0 * * * *` | 45m | Hourly thinking on active topics (self-seeds via starvation floor when empty) — the :00 anchor |
| Domain Watch | `/scheduled-run domain-watch` | `30 */2 * * *` | 30m | Every 2h at :30 — perception layer; auto-activates topics (incl. starvation floor) |
| GJ Open Refresh | `/scheduled-run gjopen-refresh` | `30 1 * * *` | 30m | 01:30 daily — external forecasting data **[disabled]** |
| Refresh Index | `/scheduled-run refresh-index` | `30 3 * * *` | 40m | 03:30 daily — FAISS + BDG bootstrap |
| Coherence Sweep | `/scheduled-run coherence-sweep` | `30 5 * * 1` | 30m | Mon 05:30 — staleness/health briefing **[disabled]** |
| AI Crystallize | `/scheduled-run ai-crystallize` | `30 7 * * 1` | 30m | Mon 07:30 — AI synthesis of converged topics → `AI Crystallizations/` (ai-inferred) |
| Git Sync | (raw git) | `45 */6 * * *` | 10m | :45 every 6h — redundant with scheduled-run git hygiene **[disabled]** |

**Spacing rule:** incubation holds the hourly `:00` slot; every other job runs at `:30` of an **odd** hour (domain-watch only runs even hours), so no two jobs start in the same minute and their git commits never collide. Timeouts match each skill's work budget (the 15-min platform default is too short for FAISS rebuilds and multi-domain scans).

**What should NOT be scheduled (requires human judgment):**

| Skill | Why manual |
|-------|-----------|
| `/auto-discovery` | Generates new connections - that's intellectual work |
| `/deep-research` | Creates new content from external sources |
| `/detect-tensions` | Productive contradictions need human interpretation |
| `/compute-lifecycle` | Promotions to framework status need human decision |
| `/integrate-recent-notes` | Integration choices are creative decisions |
| `/analyze-kb` | Useful on-demand, not worth weekly automation |

**The principle:** Automate measurement and maintenance. Never automate creation or judgment *into the endorsed knowledge base*. The refinement (2026-06): autonomous synthesis is permitted when its output is **segregated and tagged `ai-inferred`** - the starvation floor self-seeds topics, and `ai-crystallize` writes AI conclusions to `Brain/05-Meta/AI Crystallizations/` (never `02-Permanent/`). The gate that stays human is the **endorsement act**: only the user promotes an ai-inferred conclusion into permanent, endorsed knowledge via `/manage-thinking-topics crystallize`.

The coherence sweep is the one weekly artifact that earns automation - it's a Monday briefing that says "here's what changed, here's what might be stale, here's what's evolving." You glance at it, act on what matters, ignore the rest.

## Completion Checklist

- [ ] Git pull completed successfully
- [ ] Playbook executed
- [ ] Changes detected and committed (if any)
- [ ] Changes pushed to remote
