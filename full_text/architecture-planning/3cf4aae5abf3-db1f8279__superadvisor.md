---
name: superadvisor
description: "Default-on multi-advisor workflow for substantive workspace-changing work. Use to coordinate GPT Pro as the default Plan planner through SuperGPT, Claude as Plan fallback only, an external Codex tmux reviewer, and GPT Pro review. Plan uses GPT Pro first with rich briefs and optional scoped source bundles, falls back to Claude when GPT Pro is limited/unavailable, then Codex+GPT Pro review it; light Mid uses Codex only; major Mid and Final use Codex+GPT Pro. Claude never participates after planning. Skip only for pure Q&A, file-location answers, status reports, or command-output relay with no workspace artifact changes."
---

# Superadvisor

Use this skill when Codex should remain the executor but needs outside planning or review. Do not call a wrapper script. Codex directly curates briefs and scoped source bundles, calls GPT Pro through SuperGPT for Plan by default, drives Claude through tmux only as Plan fallback, drives a separate Codex reviewer through tmux, and synthesizes the result.

## Workspace

Use a fixed trusted root plus per-task folders:

```bash
if [ -z "${TASK_ID:-}" ]; then
  echo "[superadvisor] Set TASK_ID to a short per-task slug before using superadvisor, e.g. export TASK_ID=20260630-superadvisor-hardening" >&2
  exit 2
fi
task_id="$TASK_ID"
task_id_safe="$(printf '%s' "$task_id" | tr -c 'A-Za-z0-9_.-' '-' | sed 's/--*/-/g; s/^-//; s/-$//')"
if [ -z "$task_id_safe" ] || [ "$task_id_safe" = "default" ]; then
  echo "[superadvisor] TASK_ID must sanitize to a non-default per-task slug" >&2
  exit 2
fi
session_id_safe="$(printf '%s' "$task_id_safe" | tr '.:' '--' | tr -c 'A-Za-z0-9_-' '-' | sed 's/--*/-/g; s/^-//; s/-$//')"
if [ -z "$session_id_safe" ] || [ "$session_id_safe" = "default" ]; then
  echo "[superadvisor] TASK_ID produced an invalid session slug" >&2
  exit 2
fi
superadvisor_home="${SUPERADVISOR_HOME:-$HOME/.superadvisor}"
task_dir="$superadvisor_home/$task_id_safe"
codex_sess="${SUPERADVISOR_CODEX_SESSION:-superadvisor-codex-$session_id_safe}"
claude_sess="${SUPERADVISOR_CLAUDE_SESSION:-superadvisor-claude-$session_id_safe}"
gptpro_sess="${SUPERADVISOR_GPTPRO_SESSION:-superadvisor-gptpro-$session_id_safe}"
max_wait="${SUPERADVISOR_MAX_WAIT:-300}"
gptpro_max_wait="${SUPERADVISOR_GPTPRO_MAX_WAIT:-3600}"
gptpro_send_timeout="${SUPERADVISOR_GPTPRO_SEND_TIMEOUT:-180}"
gptpro_poll_slice="${SUPERADVISOR_GPTPRO_POLL_SLICE:-60}"
case "$max_wait" in ''|*[!0-9]*) max_wait=300 ;; esac
case "$gptpro_max_wait" in ''|*[!0-9]*) gptpro_max_wait=3600 ;; esac
case "$gptpro_send_timeout" in ''|*[!0-9]*) gptpro_send_timeout=180 ;; esac
case "$gptpro_poll_slice" in ''|*[!0-9]*) gptpro_poll_slice=60 ;; esac
```

Create `superadvisor_home` once and `task_dir` for each real task. Ensure `$superadvisor_home/AGENTS.md` contains the Codex reviewer role and `$superadvisor_home/CLAUDE.md` contains the Claude planner role.

## Role File Minimums

If the fixed root role files are missing or stale, patch only the missing clauses and preserve local additions.

`$superadvisor_home/AGENTS.md` must say the nested Codex reviewer:

- Reads `brief-N.md` first, then may inspect only the read-only files, folders, or source bundles explicitly named in the brief.
- Does not edit code or workspace files except the requested `codex-answer-N.md`.
- Must not call `$superadvisor`, Claude, GPT Pro, SuperGPT, subagents, or any advisor/reviewer workflow.
- Judges both the work and evidence sufficiency, and returns `INSUFFICIENT` when a critical claim lacks inline proof or cannot be verified by allowed read-only inspection.
- Ends the answer file with `<<<DONE>>>`.

`$superadvisor_home/CLAUDE.md` must say the Claude planner:

- Runs only as Plan fallback when GPT Pro planning is limited, unavailable, timed out, or degraded.
- Writes only the requested `claude-plan-N.md`.
- Is not a reviewer and never judges Mid/Final or final diffs.
- Uses the rich planning brief to clarify intent, missing requirements, risks, and verification ideas.
- Ends the plan file with `<<<DONE>>>`.

## Advisor Matrix

Use superadvisor by default for substantive work. Skip it only for pure Q&A, file-location answers, status reports, or command-output relay with no workspace artifact changes. If the task changes code, docs, config, or other workspace artifacts, Final is mandatory before completion.

| Tier | When | Advisors |
|---|---|---|
| Plan | Before committing to a meaningful approach | GPT Pro plans first with rich brief/source bundle; if GPT Pro is limited/unavailable, Claude plans as fallback; then Codex + GPT Pro review |
| Light Mid | Useful intermediate check where speed matters and risk is moderate | Codex only |
| Major Mid | Hard-to-reverse, architectural, security, data, public API, or user-visible behavior decision | Codex + GPT Pro |
| Final | Before declaring completion | Codex + GPT Pro only |

GPT Pro is the default planner and a reviewer. Claude is a fallback planner, not a reviewer. Call Claude only during Plan fallback. Do not call Claude for Light Mid, Major Mid, or Final.
Do not optimize Plan, Codex, or GPT Pro briefs for token savings. Prefer complete source context, diffs, evidence, and logs over compact summaries.

## Brief Routing And Token Budget

`brief-N.md` is the primary rich review brief for Codex and GPT Pro. Give Codex and GPT Pro enough context to review the actual work: relevant diffs, risky hunks, command output, reviewer history, and unresolved gaps.

For Plan only, first write `$task_dir/gptpro-plan-brief-N.md` as a rich planning brief for GPT Pro. The brief should frame the task as: current state/design/source is provided, sensitive files and irrelevant generated artifacts are omitted, the user wants a specific change, and the planner should propose a concrete solution plus implementation and verification plan.

GPT Pro must answer directly in the ChatGPT conversation as plain text. Do not ask GPT Pro to create, attach, or return a downloadable file/artifact for the answer. Codex saves GPT Pro's chat text into `gptpro-plan-N.md`, `gptpro-answer-N.md`, or the relevant provider answer file after polling.

When source context matters, create `$task_dir/source-bundle-N.zip` from relevant source files, diffs, logs, and README-like context, and preferably create `$task_dir/plan-context-N.zip` that contains both `gptpro-plan-brief-N.md` and the scoped source context. The GPT Pro Plan command sends `plan-context-N.zip` when it exists; otherwise it sends `gptpro-plan-brief-N.md`. Exclude secrets, env files, credentials, private large data, generated build output, dependency folders, and unrelated personal files. Include a short manifest or brief section naming what was included and why anything material was omitted.

If GPT Pro planning is limited, unavailable, times out, or otherwise degrades, use Claude as the planning fallback with the same rich planning brief copied to `$task_dir/claude-plan-brief-N.md`, and write `$task_dir/claude-plan-N.md`. Then create or update `$task_dir/brief-N.md` for Codex/GPT Pro review, including the executor's plan plus the decisive parts of `gptpro-plan-N.md` or Claude fallback plan.

Because GPT Pro is both default planner and later reviewer, the Plan review brief and synthesis must explicitly state when GPT Pro drafted the plan so the later GPT Pro review is not treated as fully independent.

## Round Number And Budget

Choose `N` from the task log; never hardcode it:

```bash
last_n="$(
  find "$task_dir" -maxdepth 1 -type f -name 'brief-*.md' -printf '%f\n' 2>/dev/null \
  | sed -n 's/^brief-\([0-9][0-9]*\)\.md$/\1/p' \
  | sort -n \
  | tail -1
)"
n=$(( ${last_n:-0} + 1 ))
```

Cap each task at 4 review rounds and reserve one slot for Final. The GPT Pro planning step, or Claude planning fallback, is part of the Plan round, not an extra review round:

- Plan, Light Mid, or Major Mid: skip if `n >= 4`.
- Final: run only if `n <= 4`; if Final cannot run, say final superadvisor review did not run.
- Never reuse existing `brief-N.md` or answer files for a new round, even if earlier rounds were deleted.

## Evidence Contract

Reviewer briefs must make the evidence level of each material claim clear. GPT Pro primarily relies on the brief and attached source bundle. The Codex reviewer may additionally inspect only read-only files, folders, or source bundles explicitly named in the brief.

Use these labels in every non-trivial brief:

- `Observed`: directly seen in a file, command output, diff, screenshot, or produced artifact.
- `Inferred`: concluded from observed facts, but not directly proven.
- `Omitted`: intentionally not pasted; summarize why it is low-risk or too large.
- `Unknown`: not verified yet and still relevant to risk.

For each material claim, include enough inline evidence for a reviewer to challenge it:

- Paste exact command names, exit codes, and the key stdout/stderr lines. Artifact paths are supporting context, not proof.
- Paste risky code hunks verbatim. If a hunk is omitted, name the file and explain what was omitted.
- Do not mark a critical claim as proven by `Omitted`; either paste inline proof or make the reviewer answer `INSUFFICIENT`.
- Distinguish "path smoke works" from "real behavior was reviewed"; do not let one stand in for the other.
- Mark untested critical paths explicitly. Missing evidence for a critical claim should lead reviewers to answer `INSUFFICIENT`.

## Brief Templates

Write `$task_dir/brief-N.md` for Codex and GPT Pro review. For Plan only, also write `$task_dir/gptpro-plan-brief-N.md` before calling GPT Pro and optionally prepare `$task_dir/source-bundle-N.zip` or `$task_dir/plan-context-N.zip`. Read `$task_dir/gptpro-plan-N.md`, or `$task_dir/claude-plan-N.md` when GPT Pro degrades, before creating the review brief.

### Plan

GPT Pro planning brief. This is rich because GPT Pro's job is to understand the user's desired change against the current source/design state and propose a concrete solution plus implementation plan:

```markdown
## 상황 / 목표
[user request, current state, success criteria]

## 사용자가 중요하게 보는 것
[preferences, constraints, implied priorities, prior decisions]

## 관찰한 사실
- Observed: [facts already inspected, with short inline evidence]
- Unknown: [what is not known yet but could change the approach]

## 첨부 / 소스 번들
[path to source-bundle-N.zip or plan-context-N.zip, included files, omitted sensitive/generated/unrelated files]

## GPT Pro에게 부탁할 것
[ask GPT Pro to propose the solution and execution/verification plan for accomplishing the user's desired change]

## 원하는 산출물
Return plain chat text only: recommended solution, implementation plan, missing requirements, risks, and verification ideas. Do not create or attach a downloadable file. Codex will save your chat response as `gptpro-plan-N.md`. End with <<<DONE>>>.
```

After GPT Pro responds, or after Claude fallback planning completes, write the Plan review brief for Codex + GPT Pro:

```markdown
## 상황 / 목표
[task goal, current state, success criteria]

## Planning source
[GPT Pro plan, Claude fallback plan, or executor-only if both degraded; include degradation reason and note GPT Pro independence limits when GPT Pro planned]

## Planner output 요약
[decisive parts of gptpro-plan-N.md or claude-plan-N.md, including missing requirements and risks]

## Executor 계획
[the plan Codex intends to follow, including where it agrees/disagrees with the planner]

## 영향 범위
[files/components/configs likely to change, or "unknown yet"]

## Evidence Contract
- Observed: [facts already inspected, with short inline evidence]
- Inferred: [assumptions behind the plan]
- Unknown: [what is not known yet but could change the approach]

## 검증 계획
[commands/smoke/manual checks expected to prove the risky claims]

## 결정할 것
[one question about whether this direction is right]

## 원하는 답 형태
GO/ADJUST/INSUFFICIENT + 이유 1-2줄 + 최대 리스크 1개 + 반드시 포함해야 할 증거 3개
```

### Light Mid

Use for fast intermediate checks where quality matters but the decision is not hard to reverse. Codex only.

```markdown
## 상황
2-4 lines, self-contained.

## 결정 + 근거
[decision plus the smallest relevant snippet/output]

## Claim / Evidence Map
- Claim: [material claim]
  Evidence: [Observed/Inferred/Unknown + exact snippet/output]

## Known gaps
[unverified path, or "none"]

## 원하는 답 형태
GO/ADJUST/INSUFFICIENT + 이유 1-2줄 + 필수수정(있으면)
```

### Major Mid

Use when a mid-task decision is expensive to reverse or could affect architecture, security, permissions, migrations, public API, data shape, compatibility, or user-visible state. Codex + GPT Pro.

```markdown
## 상황
2-4 lines, self-contained. GPT Pro relies on the brief/source bundle; Codex may inspect only read-only paths explicitly named here.

## 중대한 결정 + 근거
[decision plus relevant snippets, partial diff, or command output]

## Claim / Evidence Map
- Claim: [material claim]
  Evidence: [Observed/Inferred/Unknown + exact snippet/output]
- Claim: [material claim]
  Evidence: [Observed/Inferred/Unknown + exact snippet/output]

## 위험 불변식
[what must stay true: compatibility, permissions, routing, data shape, cleanup, idempotence]

## 검증 기록 / 예정
[commands with exit codes and key output, or planned checks if not run yet]

## 이미 정함
[what reviewers should not re-litigate]

## Known gaps
[unverified paths, omitted hunks, unavailable logs, or "none"]

## 원하는 답 형태
GO/ADJUST/INSUFFICIENT + 이유 2-3 + 핵심 리스크 + 필수수정(있으면) + 추가로 필요한 증거
```

### Final

Do not keep Final briefs artificially short. Include the complete evidence needed for Codex and GPT Pro to validate the result, even if the brief is long. Prefer full diffs, full risky hunks, command outputs, reviewer answers, and synthesis notes over compressed summaries.

Include `git diff --stat` or an equivalent changed-file list with line counts. Paste the actual diff whenever practical. Omit only generated files, binary files, huge lockfiles, or clearly low-risk repetitive output; for each omission, name the file and explain why it is safe to omit.

```markdown
## 상황 / 완료 기준
[what must be true for this task to be complete]

## 변경 파일 / diff stat
[git diff --stat or changed-file list]

## 변경 전체 / diff
[actual git diff; if omitted, list each omitted file with reason]

For prompt, workflow, or template changes, include at least one inline hunk per changed brief template, reviewer prompt, role file, or provider path.

## Claim / Evidence Map
- Claim: [completion claim]
  Evidence: [Observed/Inferred/Unknown + exact inline proof]
- Claim: [safety/regression claim]
  Evidence: [Observed/Inferred/Unknown + exact inline proof]

## 이미 검증/처리함
[commands run with exit codes and key stdout/stderr lines; include enough output to make pass/fail independently reviewable]

## Reviewer history / prior rounds
[relevant prior advisor answers, required fixes, and synthesis decisions; paste decisive lines, not only file paths]

## Known gaps / 미검증 경로
[anything not tested, degraded reviewers, omitted logs/hunks, or "none"]

## 특히 봐줬으면
[most uncertain or risky point]

## 원하는 답 형태
GO/ADJUST/INSUFFICIENT + 모든 임계결함(개수 제한 없음) + 비임계 리스크 + 필수수정 + 부족한 증거
```

## Codex Review

Codex reviews Plan, Light Mid, Major Mid, and Final through a separate one-shot tmux session. The executor Codex must not write `codex-answer-N.md` directly.

Run the Codex reviewer with `codex exec` inside tmux, not by driving the interactive TUI input field. The interactive TUI can require extra Enter/focus handling and is less reliable for automation.
Do not use `--output-last-message` as the reviewer answer path: that captures the nested agent's final chat message, not necessarily the review file content. The reviewer must write `codex-answer-N.md` itself; stdout/stderr are logs only.

```bash
codex_round_sess="$codex_sess-r$n"
rm -f "$task_dir/codex-answer-$n.md" "$task_dir/codex-prompt-$n.txt" "$task_dir/codex-log-$n.stdout" "$task_dir/codex-log-$n.stderr"
cat > "$task_dir/codex-prompt-$n.txt" <<EOF
Read the full rich brief $task_id_safe/brief-$n.md and write your review to $task_id_safe/codex-answer-$n.md.
Inspect the relevant inline evidence, diffs, logs, gaps, and any read-only source paths or source bundles explicitly named in the brief. For Light Mid, stay focused and fast; for Plan, Major Mid, and Final, do not optimize for token savings. Judge both the proposed work and whether the brief plus allowed read-only inspection contains enough evidence. Use INSUFFICIENT when a critical claim lacks inline proof and cannot be verified from allowed paths.
Do not call superadvisor, Claude, GPT Pro, SuperGPT, subagents, or any advisor/reviewer workflow. Do not edit code or workspace files. Write only $task_id_safe/codex-answer-$n.md.
End the answer file with <<<DONE>>> on its own line.
EOF
tmux kill-session -t "$codex_round_sess" 2>/dev/null || true
tmux new-session -d -s "$codex_round_sess" -x 220 -y 50 -c "$superadvisor_home" \
  "codex exec -C . --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check - < '$task_id_safe/codex-prompt-$n.txt' > '$task_id_safe/codex-log-$n.stdout' 2> '$task_id_safe/codex-log-$n.stderr'"
```

Use `--dangerously-bypass-approvals-and-sandbox` for this nested reviewer because Codex's normal Linux sandbox can fail inside the current execution environment before it can read advisor files, allowed source paths, or write the answer file. The `$superadvisor_home/AGENTS.md` role and fixed CWD keep the reviewer behavior bounded: it must read the brief first, inspect only explicitly allowed read-only paths, avoid advisor workflows, and write only the requested answer file.

Wait for `<<<DONE>>>` on the last non-empty line:

```bash
codex_degraded=0
waited=0
until awk 'NF { last=$0 } END { exit !(last=="<<<DONE>>>") }' "$task_dir/codex-answer-$n.md" 2>/dev/null; do
  sleep 2
  waited=$((waited + 2))
  if [ "$waited" -ge "$gptpro_max_wait" ]; then
    echo "[superadvisor] Codex timeout after ${gptpro_max_wait}s; degrade" >&2
    codex_degraded=1
    break
  fi
done
```

If Codex degrades, inspect `codex-log-N.stdout` and `codex-log-N.stderr`, then record the degradation in synthesis.

## GPT Pro Plan

Use GPT Pro as the default Plan planner. GPT Pro receives a rich `gptpro-plan-brief-N.md` and, when useful, an attached scoped source bundle such as `source-bundle-N.zip` or `plan-context-N.zip`. The planning question should be framed as: "this is the current design/source state, sensitive or irrelevant files are omitted, the user wants this change, what solution and execution plan should accomplish it?"

Run GPT Pro planning with Plan-specific artifacts and the same detached send/poll/status shape as GPT Pro review:

```bash
gptpro_plan_sess="$gptpro_sess-plan-r$n"
rm -f "$task_dir/gptpro-plan-$n.md" "$task_dir/gptpro-plan-log-$n.stderr" "$task_dir/gptpro-plan-exit-$n.status" "$task_dir/gptpro-plan-send-$n.json" "$task_dir/gptpro-plan-poll-$n.json" "$task_dir/gptpro-plan-session-$n.id"
plan_input="$task_dir/gptpro-plan-brief-$n.md"
if [ -s "$task_dir/plan-context-$n.zip" ]; then
  plan_input="$task_dir/plan-context-$n.zip"
fi
plan_input_q="$(printf '%q' "$plan_input")"
answer_q="$(printf '%q' "$task_dir/gptpro-plan-$n.md")"
log_q="$(printf '%q' "$task_dir/gptpro-plan-log-$n.stderr")"
status_q="$(printf '%q' "$task_dir/gptpro-plan-exit-$n.status")"
send_json_q="$(printf '%q' "$task_dir/gptpro-plan-send-$n.json")"
poll_json_q="$(printf '%q' "$task_dir/gptpro-plan-poll-$n.json")"
session_q="$(printf '%q' "$task_dir/gptpro-plan-session-$n.id")"
node_q="$(printf '%q' "$HOME/supergpt/bin/supergpt.mjs")"
gptpro_plan_cmd="$(cat <<EOF
set -u
if command -v supergpt >/dev/null 2>&1; then
  timeout '${gptpro_send_timeout}s' supergpt send -p 'Read the attached rich planning brief/source context bundle. The user is asking how to accomplish the requested change from the current source/design state, not for an abstract plan. Create a concrete solution, implementation plan, risks, and verification plan. This is planning, not final review. Do not optimize for token savings. Return the answer directly in this chat as plain text only; do not create, attach, or offer a downloadable file/artifact. Codex will save your chat response into the plan file.' --file $plan_input_q --json > $send_json_q 2>> $log_q
else
  timeout '${gptpro_send_timeout}s' node $node_q send -p 'Read the attached rich planning brief/source context bundle. The user is asking how to accomplish the requested change from the current source/design state, not for an abstract plan. Create a concrete solution, implementation plan, risks, and verification plan. This is planning, not final review. Do not optimize for token savings. Return the answer directly in this chat as plain text only; do not create, attach, or offer a downloadable file/artifact. Codex will save your chat response into the plan file.' --file $plan_input_q --json > $send_json_q 2>> $log_q
fi
rc=\$?
if [ "\$rc" != "0" ]; then printf 'send-failed:%s\n' "\$rc" > $status_q; exit 0; fi
session_id=\$(node -e 'const fs=require("fs"); const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); if (!o.sessionId) process.exit(2); process.stdout.write(o.sessionId);' $send_json_q 2>> $log_q) || { printf 'send-json-missing-session\n' > $status_q; exit 0; }
printf '%s\n' "\$session_id" > $session_q
deadline=\$(( \$(date +%s) + ${gptpro_max_wait} ))
while :; do
  now=\$(date +%s)
  remaining=\$(( deadline - now ))
  if [ "\$remaining" -le 0 ]; then printf 'poll-timeout\n' > $status_q; exit 0; fi
  slice='${gptpro_poll_slice}'
  if [ "\$remaining" -lt "\$slice" ]; then slice="\$remaining"; fi
  if command -v supergpt >/dev/null 2>&1; then
    timeout "\$((slice + 30))s" supergpt poll "\$session_id" --timeout "\$slice" --json > $poll_json_q 2>> $log_q
  else
    timeout "\$((slice + 30))s" node $node_q poll "\$session_id" --timeout "\$slice" --json > $poll_json_q 2>> $log_q
  fi
  rc=\$?
  if [ "\$rc" != "0" ]; then printf 'poll-failed:%s\n' "\$rc" > $status_q; exit 0; fi
  poll_status=\$(node -e 'const fs=require("fs"); const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); process.stdout.write(String(o.status || ""));' $poll_json_q 2>> $log_q) || { printf 'poll-json-invalid\n' > $status_q; exit 0; }
  if [ "\$poll_status" = "complete" ]; then
    node -e 'const fs=require("fs"); const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); if (!o.answerText) process.exit(2); process.stdout.write(o.answerText);' $poll_json_q > $answer_q 2>> $log_q || { printf 'poll-complete-empty\n' > $status_q; exit 0; }
    if [ -s $answer_q ]; then printf '0\n' > $status_q; else printf 'poll-complete-empty\n' > $status_q; fi
    exit 0
  fi
  if [ "\$poll_status" = "timeout" ]; then continue; fi
  printf 'poll-status:%s\n' "\$poll_status" > $status_q
  exit 0
done
EOF
)"
tmux kill-session -t "$gptpro_plan_sess" 2>/dev/null || true
if ! tmux new-session -d -s "$gptpro_plan_sess" -x 220 -y 50 -c "$superadvisor_home" "$gptpro_plan_cmd"; then
  printf '%s\n' "tmux new-session failed" > "$task_dir/gptpro-plan-log-$n.stderr"
  printf '%s\n' "tmux-new-session-failed" > "$task_dir/gptpro-plan-exit-$n.status"
fi
```

Wait for `$task_dir/gptpro-plan-exit-$n.status` with `gptpro_max_wait + 30` slack. Treat any non-zero status, missing status, or empty `$task_dir/gptpro-plan-$n.md` as degraded.

## Claude Plan Fallback

Use Claude only when GPT Pro planning degrades because of timeout, missing output, unavailable SuperGPT, upload/send failure, limit, or any other provider failure. Claude is not a reviewer and must not be called for Light Mid, Major Mid, or Final. Before calling Claude, copy or adapt the GPT Pro planning brief to `$task_dir/claude-plan-brief-N.md` and include the GPT Pro degradation reason.

Start or reuse Claude in the fixed root:

```bash
tmux new-session -d -s "$claude_sess" -x 220 -y 50 -c "$superadvisor_home" \
  'claude --permission-mode dontAsk --tools Read,Write,Glob,Grep --allowedTools Read,Write,Glob,Grep --effort xhigh --strict-mcp-config --name superadvisor-claude'
```

Wait until the visible pane shows `don't ask on`; accept a first-run trust prompt for the fixed root once if it appears. Use visible pane capture only:

```bash
tmux capture-pane -pt "$claude_sess"
```

Send Claude a relative-path prompt:

```bash
claude_degraded=0
rm -f "$task_dir/claude-plan-$n.md"
if [ ! -s "$task_dir/claude-plan-brief-$n.md" ]; then
  echo "[superadvisor] missing Claude fallback planning brief; degrade Claude planning" >&2
  claude_degraded=1
else
  tmux send-keys -t "$claude_sess" -l "Read the rich fallback planning brief $task_id_safe/claude-plan-brief-$n.md and write your plan to $task_id_safe/claude-plan-$n.md. GPT Pro planning was attempted first and degraded; you are the Plan fallback. Your job is to understand the user's intent, fill missing requirements, identify risks, and propose a concrete execution and verification plan. Do not review code or final diffs. End the plan file with <<<DONE>>> on its own line."
  tmux send-keys -t "$claude_sess" Enter
fi
```

Wait for `<<<DONE>>>` on the last non-empty line:

```bash
waited=0
if [ "$claude_degraded" -eq 0 ]; then
  until awk 'NF { last=$0 } END { exit !(last=="<<<DONE>>>") }' "$task_dir/claude-plan-$n.md" 2>/dev/null; do
    sleep 2
    waited=$((waited + 2))
    if [ "$waited" -ge "$max_wait" ]; then
      echo "[superadvisor] Claude fallback planning timeout after ${max_wait}s; degrade" >&2
      claude_degraded=1
      break
    fi
  done
fi
```

If both GPT Pro planning and Claude fallback planning degrade, continue with the executor's plan and record both degradations in synthesis. If GPT Pro planning succeeds, include `gptpro-plan-N.md` in the Plan review brief and explicitly mark that the later GPT Pro reviewer is reviewing a plan that GPT Pro helped draft. If Claude fallback succeeds, include `claude-plan-N.md` and the GPT Pro degradation reason.

## GPT Pro Review

Use GPT Pro through the local SuperGPT CLI for Plan, Major Mid, and Final. Do not call GPT Pro for Light Mid unless the user explicitly asks.
GPT Pro can take much longer than Claude/Codex; use `SUPERADVISOR_GPTPRO_MAX_WAIT`, defaulting to 3600 seconds, instead of the general `max_wait`.
Run GPT Pro in a one-shot tmux session too. Long foreground SuperGPT calls can be killed by the outer execution session before `gptpro_max_wait` expires.
Use `supergpt send --json` plus repeated `supergpt poll --json` instead of one long `supergpt ask`; this preserves a session id and makes timeout recovery explicit.

Call GPT Pro with the brief file and write an exit status file:

```bash
gptpro_round_sess="$gptpro_sess-r$n"
rm -f "$task_dir/gptpro-answer-$n.md" "$task_dir/gptpro-log-$n.stderr" "$task_dir/gptpro-exit-$n.status" "$task_dir/gptpro-send-$n.json" "$task_dir/gptpro-poll-$n.json" "$task_dir/gptpro-session-$n.id"
brief_q="$(printf '%q' "$task_dir/brief-$n.md")"
answer_q="$(printf '%q' "$task_dir/gptpro-answer-$n.md")"
log_q="$(printf '%q' "$task_dir/gptpro-log-$n.stderr")"
status_q="$(printf '%q' "$task_dir/gptpro-exit-$n.status")"
send_json_q="$(printf '%q' "$task_dir/gptpro-send-$n.json")"
poll_json_q="$(printf '%q' "$task_dir/gptpro-poll-$n.json")"
session_q="$(printf '%q' "$task_dir/gptpro-session-$n.id")"
node_q="$(printf '%q' "$HOME/supergpt/bin/supergpt.mjs")"
gptpro_cmd="$(cat <<EOF
set -u
if command -v supergpt >/dev/null 2>&1; then
  timeout '${gptpro_send_timeout}s' supergpt send -p 'Review the attached rich superadvisor brief. Do not optimize for token savings; inspect the relevant inline evidence, diffs, logs, and gaps. Judge both the work and whether the brief contains enough evidence. Use INSUFFICIENT when a critical claim lacks inline proof. Answer in the requested format. Return the answer directly in this chat as plain text only; do not create, attach, or offer a downloadable file/artifact. Codex will save your chat response into the review answer file.' --file $brief_q --json > $send_json_q 2>> $log_q
else
  timeout '${gptpro_send_timeout}s' node $node_q send -p 'Review the attached rich superadvisor brief. Do not optimize for token savings; inspect the relevant inline evidence, diffs, logs, and gaps. Judge both the work and whether the brief contains enough evidence. Use INSUFFICIENT when a critical claim lacks inline proof. Answer in the requested format. Return the answer directly in this chat as plain text only; do not create, attach, or offer a downloadable file/artifact. Codex will save your chat response into the review answer file.' --file $brief_q --json > $send_json_q 2>> $log_q
fi
rc=\$?
if [ "\$rc" != "0" ]; then printf 'send-failed:%s\n' "\$rc" > $status_q; exit 0; fi
session_id=\$(node -e 'const fs=require("fs"); const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); if (!o.sessionId) process.exit(2); process.stdout.write(o.sessionId);' $send_json_q 2>> $log_q) || { printf 'send-json-missing-session\n' > $status_q; exit 0; }
printf '%s\n' "\$session_id" > $session_q
deadline=\$(( \$(date +%s) + ${gptpro_max_wait} ))
while :; do
  now=\$(date +%s)
  remaining=\$(( deadline - now ))
  if [ "\$remaining" -le 0 ]; then printf 'poll-timeout\n' > $status_q; exit 0; fi
  slice='${gptpro_poll_slice}'
  if [ "\$remaining" -lt "\$slice" ]; then slice="\$remaining"; fi
  if command -v supergpt >/dev/null 2>&1; then
    timeout "\$((slice + 30))s" supergpt poll "\$session_id" --timeout "\$slice" --json > $poll_json_q 2>> $log_q
  else
    timeout "\$((slice + 30))s" node $node_q poll "\$session_id" --timeout "\$slice" --json > $poll_json_q 2>> $log_q
  fi
  rc=\$?
  if [ "\$rc" != "0" ]; then printf 'poll-failed:%s\n' "\$rc" > $status_q; exit 0; fi
  poll_status=\$(node -e 'const fs=require("fs"); const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); process.stdout.write(String(o.status || ""));' $poll_json_q 2>> $log_q) || { printf 'poll-json-invalid\n' > $status_q; exit 0; }
  if [ "\$poll_status" = "complete" ]; then
    node -e 'const fs=require("fs"); const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8")); if (!o.answerText) process.exit(2); process.stdout.write(o.answerText);' $poll_json_q > $answer_q 2>> $log_q || { printf 'poll-complete-empty\n' > $status_q; exit 0; }
    if [ -s $answer_q ]; then printf '0\n' > $status_q; else printf 'poll-complete-empty\n' > $status_q; fi
    exit 0
  fi
  if [ "\$poll_status" = "timeout" ]; then continue; fi
  printf 'poll-status:%s\n' "\$poll_status" > $status_q
  exit 0
done
EOF
)"
tmux kill-session -t "$gptpro_round_sess" 2>/dev/null || true
if ! tmux new-session -d -s "$gptpro_round_sess" -x 220 -y 50 -c "$superadvisor_home" "$gptpro_cmd"; then
  printf '%s\n' "tmux new-session failed" > "$task_dir/gptpro-log-$n.stderr"
  printf '%s\n' "tmux-new-session-failed" > "$task_dir/gptpro-exit-$n.status"
fi
```

Wait for the status file, then require a zero exit status and non-empty answer:

```bash
gptpro_degraded=0
waited=0
until [ -f "$task_dir/gptpro-exit-$n.status" ]; do
  sleep 5
  waited=$((waited + 5))
  if [ "$waited" -ge $((gptpro_max_wait + 30)) ]; then
    echo "[superadvisor] GPT Pro no status after $((gptpro_max_wait + 30))s; degrade" >&2
    gptpro_degraded=1
    break
  fi
done

if [ "$gptpro_degraded" -eq 0 ]; then
  gptpro_rc="$(cat "$task_dir/gptpro-exit-$n.status" 2>/dev/null || printf 'missing')"
  if [ "$gptpro_rc" != "0" ] || [ ! -s "$task_dir/gptpro-answer-$n.md" ]; then
    echo "[superadvisor] GPT Pro failed or returned empty answer; degrade" >&2
    gptpro_degraded=1
  fi
fi
```

If GPT Pro is unavailable, returns a non-zero status, returns empty output, or times out, inspect `gptpro-log-N.stderr` and record the degradation. Treat a non-zero status as degraded even if an answer file exists. For Final, mention in the final response that GPT Pro final review did not complete.

## Synthesis

After the tier's reviewers finish or degrade, Codex reads the available answer files and writes `$task_dir/synthesis-N.md`:

- State which reviewers completed and which degraded.
- Resolve disagreements with concrete verification evidence first.
- Apply required fixes before continuing or declaring completion.
- Carry forward any `INSUFFICIENT` result as either a required evidence fix or an explicit unresolved gap.
- For Final, do not claim completion if critical findings remain unresolved.

## Skill Edit Verification

When editing this skill, verify the orchestration contract before Final review:

- Run the local skill validator, for example `python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" "$HOME/.codex/skills/superadvisor"`, and include the exit code plus key output.
- Grep the active workspace setup assignments and confirm task identity fails closed instead of falling back to a shared default folder.
- List files under the skill folder and confirm the change did not add wrapper/helper scripts unless the user explicitly changed the no-wrapper policy.
- Grep for `gptpro-plan`, `codex-answer`, `INSUFFICIENT`, and `<<<DONE>>>` to confirm the Plan fallback, reviewer ownership, evidence gating, and completion markers remain represented.

## Cleanup

Use one tmux session per long-lived provider per task/topic. Codex one-shot sessions normally exit by themselves; clear any leftover reviewer sessions when switching topics:

```bash
tmux kill-session -t "$codex_sess-r$n"
tmux kill-session -t "$claude_sess"
tmux kill-session -t "$gptpro_sess-r$n"
```
