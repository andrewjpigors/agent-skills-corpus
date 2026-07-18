---
name: cmux-agents
description: Coordinate multiple AI agents inside cmux — spawn parallel Claude Code teammates (cmux claude-teams), drive sibling Claude/Codex (cmux send/read-screen), macOS notifications.
---

<!-- archived-description (auto-shortened 2026-05-06):
Coordinate multiple AI agent sessions inside cmux — spawn parallel Claude Code teammates via `cmux claude-teams`, drive sibling Claude/Codex/OpenCode terminals via `cmux send` + `cmux read-screen`, and post native macOS attention notifications via `cmux notify` + `cmux trigger-flash`. Use when the task fans out to multiple agents (parallel feature branches, parallel reviewers, parallel investigators), when monitoring or feeding input to a sibling agent's session, when the user wants to launch a teammate to work in parallel, or when a long-running operation needs to alert the user when it finishes. Distinct from spawning subagents inside this session because each cmux teammate is its own full Claude Code process with its own conversation, model, and worktree.
-->

# Multi-agent orchestration via cmux

cmux is built around the assumption that you'll be running many AI agents in parallel. It exposes that as: spawn-as-native-split, drive-by-stdin, observe-by-screen-read, alert-by-notification. This skill is the playbook for using those primitives.

## When to fan out across cmux teammates vs. spawn subagents

| Need | Tool |
|------|------|
| Quick research / single-question delegation | **Agent tool subagent** (lives inside this session) |
| Long-running parallel implementation across separate worktrees | **`cmux claude-teams`** (full Claude Code per pane) |
| User wants to watch and intervene in the parallel work | **`cmux claude-teams`** (visible UI panes) |
| Need to drive a session the user already started manually | **`cmux send`** to that surface |
| Want to monitor a long build/test run elsewhere | **`cmux read-screen --surface`** + `notify` when done |

Rule of thumb: **if the user benefits from seeing the parallel agent's pane, use cmux. If the parallelism is just to save my own time, use the Agent tool.**

## Spawn parallel Claude Code teammates

`cmux claude-teams` accepts the full Claude Code argument set and opens each teammate as a native split with sidebar metadata:

```bash
# Simplest: launch one teammate in a new split
cmux claude-teams

# Pre-seed a prompt and a worktree
cmux claude-teams -w feature/auth -p "implement OAuth login per design/auth.md"

# Hand it a model + permission policy
cmux claude-teams --model opus --permission-mode acceptEdits "refactor server/api/routes.py"

# Bare mode (no hooks, no auto-memory) — useful for clean repro runs
cmux claude-teams --bare -p "run the failing test and report only the failure"
```

`cmux claude-teams` is a thin wrapper around `claude` itself — every flag from `claude --help` works (--worktree, --resume, --session-id, --model, --effort, --agents, --plugin-dir, --mcp-config, etc.).

After spawning, surface IDs may renumber — re-run `cmux tree --all` to find the new teammate's `surface:N`.

## Drive a sibling agent's session

Once you have a teammate's surface (or any other terminal surface in cmux), you can feed it input:

```bash
# Find the teammate
cmux tree --all | grep -i claude

# Send a prompt (\n submits)
cmux send --surface surface:18 "Why did test X fail?\n"

# Send a control key (interrupt, etc.)
cmux send-key --surface surface:18 "C-c"

# Read what the teammate has produced
cmux read-screen --surface surface:18 --scrollback --lines 200
```

This is how you build agent-to-agent loops: the orchestrator (this session) writes prompts to a teammate, reads back its screen, decides next steps, repeats.

## Other agent CLIs cmux integrates

| Command | Spawns |
|---------|--------|
| `cmux claude-teams [args]` | Claude Code |
| `cmux omc [args]`          | OpenCode (`omc` flavor) |
| `cmux omo [args]`          | OpenCode (`omo` flavor) |
| `cmux omx [args]`          | OpenCode (`omx` flavor) |
| `cmux codex install-hooks` | Wires Codex CLI lifecycle into cmux UI |

Same pattern: each appears as a native split with sidebar metadata and notification hooks.

## Lifecycle hooks (claude-hook)

cmux can light up the sidebar / pane ring based on Claude Code state. The hooks read JSON from stdin:

```bash
# When a Claude session starts (called from a SessionStart hook)
echo '{"session_id":"abc"}' | cmux claude-hook session-start

# When Claude is idle / done
echo '{}' | cmux claude-hook stop

# Forward a Claude notification ("waiting for input")
echo '{"message":"Need approval for git push"}' | cmux claude-hook notification

# Clear the notification when user submits a new prompt
echo '{}' | cmux claude-hook prompt-submit
```

Hook into your Claude Code settings.json under `hooks.SessionStart` / `Stop` / `Notification` / `UserPromptSubmit` to wire these automatically. Result: the cmux pane ring goes blue when this session is waiting on the user.

## Attention: notify + trigger-flash

When something the user cares about finishes, alert them:

```bash
# Native macOS notification (banner + sound)
cmux notify --title "Build done" --body "All 412 tests passed in 2m18s"

# Tied to a specific surface (so the notification panel deep-links there)
cmux notify --surface surface:8 --title "Deploy complete" --subtitle "prod-api"

# Visual flash on a surface (blue ring + sidebar light, no banner)
cmux trigger-flash --surface surface:8

# List/clear pending notifications
cmux list-notifications
cmux clear-notifications
```

Use `notify` for things the user should see if they're alt-tabbed away. Use `trigger-flash` for "your attention is helpful but not urgent."

## Recipes

### Two-agent code-review loop

```bash
# 1. Reviewer teammate, hand it the diff
cmux claude-teams -w review/foo --model opus -p "Review the diff at /tmp/foo.diff. Only respond with structured findings JSON."

# 2. Find its surface
REVIEWER=$(cmux tree --all | grep "Review the diff" | awk '{print $2}')

# 3. Wait for output, capture
cmux read-screen --surface "$REVIEWER" --scrollback --lines 500 > /tmp/review.txt

# 4. Notify the user
cmux notify --title "Review complete" --body "Findings written to /tmp/review.txt"
```

### Watch a long-running build elsewhere

```bash
# User has a build running in surface:8. I'm in surface:13.
# Poll the screen periodically (or use ScheduleWakeup) and notify on completion.

LAST=$(cmux read-screen --surface surface:8 --scrollback --lines 50 | tail -1)
if [[ "$LAST" == *"BUILD SUCCESS"* ]]; then
  cmux notify --title "Build done" --body "Apple Silicon release ready"
elif [[ "$LAST" == *"FAILED"* ]]; then
  cmux notify --title "Build failed" --body "Check surface:8" --surface surface:8
fi
```

### Fan out to N teammates, gather results

```bash
TASKS=("auth" "logging" "metrics")
for t in "${TASKS[@]}"; do
  cmux claude-teams -w "feature/$t" --bare -p "Implement $t per design/$t.md, then write summary to /tmp/$t-summary.md"
done

# Then poll for completion files and aggregate
```

## Gotchas

1. **Surface IDs renumber after teammate close.** Always re-run `cmux tree --all` before sending text to a sibling.
2. **`claude-teams` arguments pass through to `claude`.** Anything you can do with `claude` (resume, session-id, agents JSON, mcp-config) works here too.
3. **`cmux send` does not wait for output.** Pair it with `read-screen` polling, or use `cmux wait-for` for tmux-style signal coordination.
4. **Notifications need the cmux app focus model to be set sensibly.** If macOS Do-Not-Disturb is on, banners are suppressed but the sidebar ring still works.
5. **A teammate spawned via `claude-teams` runs in its own conversation** — it does not see this session's history. Hand it a self-contained prompt or a file path with full context.

## Companions

- `cmux` — topology & cross-surface I/O (the foundation)
- `cmux-browser` — drive browser surfaces in cmux
- `cmux-markdown` — surface a live plan/progress doc beside agent work
- The built-in `Agent` tool — for in-session subagents that share my context

## Reference

- Project: https://github.com/manaflow-ai/cmux
- Hooks reference: `cmux claude-hook --help`, `cmux codex install-hooks --help`
- Full RPC surface: `cmux capabilities`
