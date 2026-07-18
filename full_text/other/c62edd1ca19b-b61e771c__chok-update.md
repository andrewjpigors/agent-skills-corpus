---
name: chok-update
description: Manually pull the latest chok-* skills from https://gitlab.com/public-repo1995722/claude-code_skills and reinstall into ~/.claude/skills/. Use when the user types /chok-update or says things like "chok 업데이트", "chok 스킬 최신화", "update chok skills".
triggers:
  keywords: [chok 업데이트, 스킬 최신화, update chok]
  type: system
  model-hint: sonnet
---

# chok-update

Manual updater for the chok-* skills maintained at
`https://gitlab.com/public-repo1995722/claude-code_skills`.

## When to invoke

- User runs `/chok-update`.
- User explicitly asks to update / sync / refresh chok skills.
- A prior `chok-*` skill invocation surfaced an update-available systemMessage
  and the user wants to apply it.

## What to do

Run the updater script and report back what changed:

```bash
bash ~/.claude/chok-skills-repo/scripts/update.sh
```

The script:

1. `git fetch` + compare local clone HEAD vs remote HEAD.
2. If equal, prints "이미 최신 버전" and exits.
3. Otherwise, `git pull --ff-only` then `bash install.sh --force`
   which overwrites `~/.claude/skills/chok-*` with the new versions.
4. Updates the `.last-check` timestamp so the auto-detection hook
   (`scripts/check-update.sh`, registered as a PreToolUse:Skill hook)
   won't nag again for an hour.

## Auto-update toggle

The PreToolUse:Skill hook detects remote changes before any chok-* skill runs.
Behavior depends on the `auto_update` config:

```bash
# 자동 pull 켜기 (감지 시 백그라운드 자동 업데이트, 다음 호출부터 반영)
bash ~/.claude/chok-skills-repo/scripts/chok-config.sh set auto_update true

# 끄기 (기본값 — 알림만 뜨고 수동 /chok-update 필요)
bash ~/.claude/chok-skills-repo/scripts/chok-config.sh set auto_update false
```

## Output to user

- If already up to date → one line: "이미 최신 버전입니다 (<sha>)".
- If updated → list which skills changed (the install.sh output already
  marks them with `UPDATE` or `INSTALL`). Mention the commit range, e.g.
  "local abc123 → remote def456". Do not dump the full install log unless
  the user asks.

## Do NOT

- Do not edit files under `~/.claude/chok-skills-repo/` directly — it is a
  git clone that will be force-overwritten on next `git pull --ff-only`.
  Edit the development repo instead and `npm run ship`.
- Do not modify the installed skills at `~/.claude/skills/chok-*` manually
  for the same reason.
- Do not run `install.sh` without `--force` inside an agent — the interactive
  prompt will hang.
