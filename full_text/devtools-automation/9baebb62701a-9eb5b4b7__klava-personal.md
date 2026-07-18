---
name: klava-personal
description: Use Vadim's Klava context stack, Obsidian vault, vadimgest, and autonomy rules.
---

# Klava Personal Context

Use this skill whenever a request depends on Vadim's personal context, active projects, deals, relationships, tasks, Telegram routing, Klava cron migration, or source-backed memory.

Primary map: `/srv/codex-klava/data/hermes/knowledge/vadim-info-map.md`.

## Load Order

1. Run `scripts/klava-recall "query"` for the named person, company, deal, project, prior discussion, email, or message. This must be the first retrieval tool call. Do not use file search, repo grep, session memory, daily memory, the Working Set, or Obsidian first.
2. Open the relevant raw source hit. The command searches the canonical server index across Obsidian, Telegram, Signal, Gmail, Bee, and Hlopya.
3. Read `/srv/codex-klava/data/hermes/knowledge/vadim-info-map.md` only if source routing or a fallback is needed.
4. Read today's and yesterday's daily memory from `/home/codex/.klava/memory/`, then the matching Obsidian note, to reconcile the raw evidence with current State + Log.
5. Read `/srv/codex-klava/data/hermes/SOUL.md` when operating rules or autonomy boundaries are relevant.

## Search Commands

```bash
cd /srv/codex-klava/repos/claude
scripts/klava-recall "query"
scripts/klava-recall "exact phrase" --sources telegram,signal,gmail,bee --full
scripts/klava-recall "query" -s telegram
```

The wrapper uses bakeneko first from the Mac and falls back to the local index only when the server is unavailable. Set `KLAVA_RECALL_LOCAL_ONLY=1` only for explicit offline diagnostics.

When a Mac-side recall result points to `/srv/codex-klava/...#L<N>`, that path is on bakeneko. Open it directly with `ssh bakeneko "sed -n '<N>p' /srv/codex-klava/..."`; do not try the server path on the Mac first.

For heartbeat-style intake:

```bash
SOURCES=$(find -L /srv/codex-klava/data/vadimgest/sources -maxdepth 1 -name '*.jsonl' ! -name 'browser.jsonl' ! -name 'xnews.jsonl' -printf '%f\n' | sed 's/\.jsonl$//' | sort | paste -sd, -)
env -u PYTHONPATH VADIMGEST_CONFIG=/srv/codex-klava/data/vadimgest/config.yaml VADIMGEST_DATA_DIR=/srv/codex-klava/data/vadimgest /srv/codex-klava/venvs/vadimgest/bin/vadimgest read --consumer intake --sources "$SOURCES" -f md --context 3 --limit 200
```

Heartbeat excludes only `browser` and `xnews`. All other vadimgest edge/local sources (`signal`, `whatsapp`, `dayflow`, `imessage`, `hlopya`, etc.) must be triaged. If a source prints `... +N more`, do not commit that source to the end; process it through a source-specific/backfill batch first.

## Source Priority

Use this order unless the task says otherwise:

1. Raw source record for exact facts.
2. Obsidian State + Log for current entity state.
3. Google Tasks / Deck for action state.
4. Daily memory for recent orientation.
5. Klava skills for procedure.
6. Hermes memory for local adaptation.
7. Inference.

Raw-source priority for recall is Telegram, Signal, Gmail, Bee, then other relevant sources. Absence from Obsidian is not evidence of absence. Scoring decides what is promoted into State + Log; all raw records remain in the append-only lake.

## Verification Playbook for "processed correctly?"

When user asks whether a day/session got processed and routed properly, run this 5-point check and only then report:

### 0) Scope and evidence window
- Fix time window explicitly (e.g., last 24h or from last handoff marker).
- Collect evidence from source of truth files first: `vadimgest`, `MyBrain`, `daily memory`, `Hermes cron state`.

### 1) Corpus health (vadimgest)
- **First: run `vadimgest read --consumer intake --limit 5`** and check whether it returns "No new data since last checkpoint" (cursor current = loop has been processing) OR a massive backlog going months back (cursor stale = loop has NOT processed, regardless of cron `last_status`). This is the ground truth.
- `stats`: confirm totals changed and source lines are increasing.
- `checkpoints/<consumer>.json`: confirm intake/consumer cursors moved forward and mtime is recent.
- `state.json`: confirm `total_records` and per-source `last_ts` are coherent.
- `read --consumer intake -f md --raw --limit ...`: confirm sample rows appear for expected chats/sources.
- **Pitfall — do not infer from cron `last_status: ok` alone.** A job can exit 0 without ever advancing the intake cursor. The consumer cursor position is the only reliable signal.
- **Pitfall — checkpoint line slightly ahead of corpus count is normal.** Gap of 1–5 is fine. Only flag if gap >50 or checkpoint is *behind* the corpus.
### Per-source delta audit when headline count is large (>200 new records).** Headline = SUM across all sources; one stale source inflates by hundreds. **WhatsApp: hard-exclude from `$SOURCES` (add `! -name 'whatsapp.jsonl'`). Leave for backfill `0649b859d63d`. 📋 `references/whatsapp-backlog-hard-exclude.md`.** Claude may be Feb 2026 Клавдия backlog — fast-path. Signal/Hlopya accumulate — triage from file end; Hlopya `content` always empty, use `notes`/`transcript`. 📋 `references/per-source-delta-audit-patterns.md`.
- **Sub-case: prior artifact `[SILENT]` does NOT mean cursor is current.** Always re-run `vadimgest read --consumer intake ... --limit 200` in the current session.

📋 `references/vadimgest-embedding-scope.md` — embedded source list (hlopya/granola/signal/bee added Jun 27), hybrid search usage, and the **Klava infra session triage rule** (infra-only sessions = daily memory note, no Obsidian writes).
📋 `references/per-source-delta-audit-patterns.md` — fast delta check script (run FIRST when >200 records); Codex historical backlog pattern; Signal dedup by `period_end`; WhatsApp exclusion. Also: calendar checkpoint lag (59K phantom records), mid-session new records, meeting note `content` field.
📋 `references/vadimgest-checkpoint-boundary-false-positive.md` — "N new records" when `checkpoint.line == file total lines` = boundary artifact, not genuinely new. Verify `total_lines - checkpoint_line == 0`.

- **Pitfall — months-stale cursor = loop failing silently.** Check the cursor, not just `last_status`.

### 2) Knowledge store updates (MyBrain)
- Identify modified `.md` files in key areas (`People`, `Inbox`, `Vox Lab`, `Klava/Ops`, `Life`).
- Confirm person/project notes include source-anchored `src:` or equivalent provenance fields after significant contact/information changes.
- For operational incidents, verify dedicated Ops notes or project notes were updated instead of temporary temp files.
- If `output/<job_id>/` is being checked, always use the *newest* file by mtime; stale/older truncated files can persist and should not be treated as current run state.

### 3) Daily memory placement
- Confirm the target file (`/home/codex/.klava/memory/YYYY-MM-DD.md`) has the day’s summary block(s).
- Ensure important identity/context anchors are in memory if they were surfaced in the same session.

### 4) Execution control plane migration integrity
- Check active scheduler: `/srv/codex-klava/data/hermes/cron/jobs.json` for enabled jobs.
- Check legacy klava job file (or equivalent) for disabled duplicates before claiming migration is complete.
- Read latest cron output artifacts in `/srv/codex-klava/data/hermes/cron/output/<job_id>/` for successful run markers.

### 5) Pending write governance
- Validate `skills.write_approval` / `memory.write_approval` and any pending payloads under `/pending/memory` and `/pending/skills`.
- If `pending/skills` is empty but data exists in backup directories, treat that as a **queue location migration event**, not “nothing to do.”
- For non-empty `/pending/memory`, evaluate every payload in this run and mark each one as **apply**, **reject**, or **retire**. Unresolved payloads must be listed explicitly in the heartbeat report.
- Use `HEARTBEAT_OK` only when both payload queues are empty (or already fully resolved) and there is no new intake work to process.
- Record any explicit decision rationale in the heartbeat run output and keep failed/blocked payloads for the next run. Use `references/heartbeats/pending-governance-runbook.md` for detailed examples.

### Reporting pattern
- Return concise verdict: **PASS / Partial / FAIL** plus: *what is correct*, *what is pending*, *what to do next*.
📋 `references/codex-infra-ops-session-triage.md` — Codex infra/ops sessions ("Back up sessions", "Inspect Hetzner disks", "Grant Codex full access to bakeneko") — recognition, grouping, and note-home rules.
📋 `references/codex-session-triage-patterns.md` — session-specific heartbeat CLI/artifact behavior, consult `references/hermes-heartbeat-cli-quirks.md` before concluding `PASS`/`PARTIAL`. Also covers: parallel audit dispatch, second wave, scheduling loop closure, ops defer-to-next-cycle, **server-side active session triage** (ID format `codex_<uuid>_<thread>_<turn>` vs Mac-local `session_MacBook-Pro-Vadim.local_*`), user prompt extraction from rollout JSONL.
📋 `references/codex-session-blocked-recovery-patterns.md` — stalled/no-output sessions: English-coach gate on pitch drafts, Tailscale SSH auth-link resolution for DF machines, agent_turn field layout, checkpoint semantics, "Чат осуждения" group triage.
- If the latest heartbeat artifact contains `Response truncated`/`output length limit`/`No fresh heartbeat artifact`, treat the cycle as **Partial**, then do a bounded re-run with compact report surface and re-check artifact freshness rather than assuming no-op.
- For production truncation recovery workflows, use `references/heartbeats/heartbeat-production-output-reduction-runbook.md`.

### Production heartbeat execution contract
- In production mode, trigger with:
  - `hermes cron run ff50067ec588 --accept-hooks`
  - then immediately run `hermes cron list --all` to confirm the job is still enabled/scheduled and inspect `Last run` + `Next run`.
- Always cross-check control plane and artifact together:
  - `jobs.json` entry for `ff50067ec588` (enabled, scheduled, state)
  - latest `/srv/codex-klava/data/hermes/cron/output/ff50067ec588/*.md` mtime and status line
- A run is **not** a pass unless all are true:
  - latest artifact exists and is newer than the previous run
  - latest run status is not `FAILED`
  - latest artifact does **not** contain `Response truncated` / `output length limit`
  - intake cursors are advanced or the run explicitly ended as no-op
  - pending governance queues are resolved or explicitly listed
- If artifact is truncated, classify run as **PARTIAL** and do a follow-up rerun with minimal output surface (compact heartbeat summary path), as per `references/hermes-cron-output-truncation-runbook.md`.
- Use the heartbeat-style intake command above first in scope; if it returns `No new data since last checkpoint.` then `HEARTBEAT_OK` is allowed with no side-effect writes.

On codex-klava, direct live vadimgest sync is enabled for Telegram, Obsidian, Codex, and Slack. Other sources may be indexed but should be treated as historical or edge-synced unless a health check proves they are fresh.

## Writing Rules

- Facts go to Obsidian State + Log with source URIs.
- Commitments and follow-ups go to Google Tasks / Deck through Klava helpers.
- Repeating procedures become skills.
- Important session continuity goes to `/home/codex/.klava/memory/YYYY-MM-DD.md`.

### Obsidian notes on codex-klava have embedded line-number prefixes when read via terminal
When you read a MyBrain note using `terminal("cat '/path/to/note.md'")` on codex-klava, the `read_file` tool (or the terminal output format) prepends line numbers to every line in `N|content` format:

```
1|---
2|handle: ""
3|email: "a.a.pokras@gmail.com"
...
78|- **misha_bilokur_visit:** Sasha's high-school friend...
79|
80|## Log
```

This causes `str.replace()` to **silently fail** — your `old_string` targets clean text, but the file on disk starts every line with `N|`. The `## Log` heading appears as `80|## Log`, so `content.find('## Log')` returns `-1`.

**Fix: strip line numbers before any string operations.**

```python
import re

raw = open('/srv/codex-klava/data/MyBrain/People/Person.md', 'r').read()
lines = raw.split('\n')
clean_lines = []
for line in lines:
    m = re.match(r'^\d+\|(.*)$', line)
    clean_lines.append(m.group(1) if m else line)
content = '\n'.join(clean_lines)

# Now str.replace() works correctly on `content`
content = content.replace(old_text, new_text, 1)

from hermes_tools import write_file
write_file('/srv/codex-klava/data/MyBrain/People/Person.md', content)
```

**Why this happens:** `read_file` adds line numbers to its output format. When you use `terminal("cat ...")` the raw terminal output passes through the same display layer. `open()` on the actual file path gives you the raw content — use `open()` for mutation work, not `terminal("cat ...")`.

**Verification:** after stripping, run `content.find('## Log')` and `content.find('## State')` — both should return non-negative positions. If either returns `-1` on a note that has those sections, the stripping step failed.

Session example (2026-06-21): Sasha Pokras note — `content.find('## Log')` returned `-1` because `terminal("cat ...")` output had `80|## Log`. Stripping line numbers resolved it.

### patch tool escape-drift on quoted strings in Obsidian notes
The `patch` tool rejects `old_string` / `new_string` that contain `\"` (backslash-escaped double quotes) with error:
```
Escape-drift detected: old_string and new_string contain the literal sequence '\\\"' but the matched region of the file does not.
```
This fires when the file has plain `"` (unescaped) but the tool call serializes them as `\"`. **Fix:** use `execute_code` with `str.replace()` on the raw file content instead. Additional Unicode/em-dash and scope pitfalls: `references/obsidian-str-replace-pitfalls.md`. Duplicate `facts-touched` from multiple replace() calls on same anchor: `references/str-replace-pitfalls-addendum.md`.

```python
from hermes_tools import terminal, write_file
r = terminal("cat '/path/to/note.md'")
content = r['output']
new_content = content.replace(old_string_exact, new_string_exact, 1)
write_file('/path/to/note.md', new_content)
```

The `str.replace()` approach bypasses the serialization layer entirely. Use it any time the target text contains double-quoted strings (common in State bullets with Vadim's direct quotes).

**Companion pitfall:** the `patch` tool also warns `"file was modified by sibling subagent"` when you write a file you never called `read_file` on.

📋 `references/venv-python-break-recovery.md` — when `execute_code` fails with `No such file or directory: venv/bin/python`, Hermes venv symlinks are broken. Switch to `terminal()` immediately and fix symlinks.

### ⚠️ execute_code variable scope — SINGLE BLOCK for read→transform→write (fires every session)
Each `execute_code` block is a **fresh Python interpreter**. Variables, imports, and computed values from block N are completely gone in block N+1. **Always do read + transform + write in ONE block.** Splitting them guarantees `NameError`. Sessions that got this wrong: 2026-06-20, 2026-06-29 (Natuska note — split write_file to second block → crash → wasted one full retry).


### terminal() truncates at ~50K bytes — NEVER use to read large files for mutation
`terminal("cat large_file.md")` silently truncates its output at the tool's ~50K byte cap. If you do `content = result['output']` and then `write_file(path, content)`, you write a truncated file with **no error**.

**Failure pattern:**
```python
# WRONG — truncates silently if file > 50KB:
result = terminal("cat '/path/to/large_file.md'")
content = result['output']  # may be only 47K chars of a 97K file
write_file('/path/to/large_file.md', content)  # DESTROYS ~50K chars
```

**Fix:** use Python's `open()` directly inside `execute_code`:
```python
from hermes_tools import write_file
content = open('/path/to/large_file.md', 'r').read()  # always reads full file
new_content = content.replace(old, new, 1)
write_file('/path/to/large_file.md', new_content)
```

**Why it's dangerous:** files with Cyrillic text output ~50K bytes ≈ 47K chars, which looks complete. The tool returns no error or truncation marker. Files >50KB that contain mostly ASCII will truncate at a clean-looking word boundary.

**Incident:** klava-personal SKILL.md (97K chars) was truncated to 47K chars on 2026-06-27. Skill lost 29 sections covering critical heartbeat triage rules. Had to restore from session context.

### execute_code tool return-key conventions on codex-klava
Inside `execute_code`, the hermes_tools return different keys depending on the tool:

```python
# read_file → result['content'] (NOT result['output'])
result = read_file("/path/to/file.md")
text = result['content']          # correct
# text = result['output']         # KeyError — wrong key

# terminal → result['output']
result = terminal("some command")
text = result['output']           # correct
```

Additionally, `read_file` returns a dedup response when the file was already read earlier in the same session. When deduped, the dict has `status: 'unchanged'` and **no `content` key at all** — accessing `result['content']` raises `KeyError`. Recovery: fall back to `terminal('cat /path/to/file')` and use `result['output']`.

```python
result = read_file("/home/codex/.klava/memory/2026-06-20.md")
if result.get('status') == 'unchanged':
    # read_file deduped — fall back to terminal
    result = terminal('cat /home/codex/.klava/memory/2026-06-20.md')
    content = result['output']
else:
    content = result['content']
```

This bites during daily memory appends mid-session: first `read_file` call caches the file, the append call finds `status: unchanged`, then `result['content']` raises `KeyError`.

### Appending to daily memory on codex-klava
Do NOT use heredoc or `echo >> file` in `terminal()` for multi-line appends — the shell expansion and quoting reliably break on this server. Use `execute_code` with `read_file` + `write_file` instead:

```python
from hermes_tools import read_file, write_file
existing = read_file("/home/codex/.klava/memory/2026-06-20.md")
new_content = existing['content'] + "\n## New Block\n...\n"
write_file("/home/codex/.klava/memory/2026-06-20.md", new_content)
```

This is the only reliable pattern for daily memory appends on codex-klava.

**Alternative: `open()` directly in execute_code.** Within `execute_code`, Python's built-in `open()` also works safely and avoids the `read_file` dedup issue entirely:

```python
from hermes_tools import write_file
existing = open('/home/codex/.klava/memory/2026-06-20.md', 'r').read()
write_file('/home/codex/.klava/memory/2026-06-20.md', existing + "\n## New Block\n...\n")
```

Use `open()` when you're mid-session and `read_file` is likely to return `status: unchanged` (i.e., you already read the file earlier this session). `open()` always reads from disk — no caching.

**Creating a new day's file (first heartbeat of the day).** When the heartbeat runs early and the target date file doesn't exist yet, `open()` will raise `FileNotFoundError`. Use `try/except` to seed the file:

```python
from hermes_tools import write_file
today = "2026-06-22"
mem_path = f"/home/codex/.klava/memory/{today}.md"
try:
    existing = open(mem_path, 'r').read()
except FileNotFoundError:
    existing = f"# {today}\n"
write_file(mem_path, existing + "\n## Heartbeat ...\n")
```

This handles both the "appending to existing file" and "creating a new day's file" cases in one block.

## Intake Triage Pitfalls

### Session antipatterns reference
Full catalog of recurring session failure modes (self-improvement detour, planning-only Codex session, interrupted multi-task session) with detection scripts and triage rules: `references/session-antipatterns.md`.

### Клава/Hermes session logs dominate large batches
When `vadimgest read` returns hundreds of new Telegram records, many will be from the `Клава` chat. Filter early: `[09:xx] Клава: ⏳ Working` / `💻 terminal` / `📚 skill_view` = noise; `[09:xx] Vadims Casecnikovs:` = signal. See `references/intake-noise-patterns.md` for WeightLossBot/Fit Mentor bot reminders, Клава system pings, English quiz notifications.

**Sub-case: automated system status pings.** Клава sends periodic pings: `System Status OK Daemons: + TG Gateway + Hermes Dashboard ...`. Always noise — skip, no tasks. Escalate only if a daemon status *changes* (new failure or recovery). Recurring same-daemon-down for 2-3 cycles = known ongoing, skip silently. **"Vadimgest (300601 new)"** in these pings = cumulative index total since last reset, NOT 300K new records this cycle. The `(+N)` delta per source is the actual new count. Do not treat large running totals as a triage backlog.

**Sub-case: interrupted multi-task session — only the completed task is in git.** When Клава handles a session with 2+ tasks and the second task ends with a clarifying question ("What do you want to replace it with?") but the session then closes, the picture is:
- Task A (e.g., "remove Astrum.trade") → **done, pushed to git**
- Task B (e.g., "fix the tagline") → **open, no Obsidian trace, no git trace**

Detection pattern: scan the session log lines for `Клава:` messages that contain a question directed at Vadim followed by no Vadim reply. If the last agent message ends with "?" or "which one?" or "what do you want to replace it with?" — the session ended before Vadim answered.

**Triage rule for this sub-case:**
1. Surface task B as **🔔 PENDING** in the heartbeat report, not just "done."
2. Do NOT create a Google Task — it just needs Vadim's one-line answer to unblock.
3. Specify exactly what's still live on disk/in the repo (e.g. "phrase X is still at line N of file Y, not yet removed").
4. Note in daily memory: "[task B] — Клава asked for replacement text, session ended before answer."

Session example (2026-06-21): Клава removed Astrum.trade (done, pushed). Then asked "What do you want to replace it with?" for the tagline "Building at the intersection of AI and fintech." — session ended. Phrase still live at line 39 of `app/page.tsx`. Surfaced as PENDING in heartbeat.

### Respecting third-party privacy requests
When a contact explicitly asks Клава/Hermes not to reveal information to Vadim, honor it:
- Log the contact in Obsidian (update `last_contact` only).
- Do NOT surface the content in the heartbeat report.
- Do NOT create a task or proposal that would reveal the withheld content.
- The appropriate note: "Gleb reached out personally — Vadim needs to read it himself."
This is rare but binding when it occurs.

**NDA on a specific sentence:** Contacts sometimes flag individual facts within a message as NDA — e.g. "The last sentence is NDA" or "don't share this part." In that case: log everything else normally in the Log entry; for the flagged fact, include it in the note body with an explicit `[NDA: do not share externally]` marker rather than omitting it. The person note is private Obsidian — capturing the fact with NDA marking is correct. What you must NOT do: include the NDA-marked detail in a heartbeat report, a Deck card, a task title, or any surface Vadim might forward.

**Follow-up cycle handling:** If in a later cycle the same contact reveals "that was a joke / по приколу написал," do NOT retroactively reconstruct the original withheld content (you still don't know it). Instead: log the meta-event ("privacy request was a joke, contact was surprised Klava honored it") and update `last_contact`. The original non-disclosure decision was correct — don't second-guess it just because the requester revealed it was a test. The content remains unlogged unless the contact themselves shares it openly in a new message.

### Game-chat mixed with Vox/tech discussion: disambiguation rule
Vadim often plays mobile games (Clash of Clans, etc.) with the same contacts he discusses Vox/data work with. Within a single chat thread, messages may pivot between:
- Data/tech: "Да всё есть, продажи нужны" (we have the data, we need sales)
- Game: "Варвары лучницы есть?" (do you have barbarian archers?) / "Я чисто на миньонах вывожу" (I play pure minions)

**Disambiguation rule:** when a contact asks about "юзеры" (users), "сливаются" (leaking), or "подозрительных личностей" (suspicious people) after a game-chat exchange, check which context it belongs to:
- If the sentence immediately follows game talk and the phrasing is casual ("Ебать мне начало писать подозрительных личностей" = WTF, suspicious accounts are DMing me), it is about the *contact's own experience* (e.g. their game account or personal TG getting spam), NOT a Vox security event.
- Vadim's "Нет" reply to "у вас юзеры никуда не сливаются?" = Vox/Astrum users are not leaking. This is Vadim confirming product security to a curious contact — not a new security finding.
- Only escalate as `[SECURITY signal]` if: (a) Vadim himself says there's a leak, (b) the contact says they received suspicious contact *from* a known Vox product, or (c) the OSINT bot returns a red flag (see Vox Compliance Bot section).

Session example (2026-06-20): Igor Blink — game chat → "Ебать мне начало писать подозрительных личностей" + Vadim "Нет" = Igor getting spam on his own TG/game account. Not a Vox incident. Logged as casual data brainstorm + game chat extension.

### Клава bot reply = primary source intel (exception to noise rule)
`Vadims Casecnikovs:` lines inside `### Клава` that answer a Клава clarifying question contain durable facts (fund names, check sizes, deal context). Write them to the relevant entity note. Full pattern + post-fumble fundraising debrief shape: `references/klava-bot-reply-intel-pattern.md`.

### All-noise batch: immediate HEARTBEAT_OK path
When `vadimgest read` returns a batch where **every** new record is a Клава/bot system status ping, skip triage: commit cursor, run cron health, append daily memory, report `HEARTBEAT_OK`. **Exception:** `Vadims Casecnikovs:` reply lines inside Клава disqualify this — unless Клава already picked it up (delegate_task/⏳ Working same minute). See `references/concurrent-session-triage.md`.

### Codex session output surfaces in TG chat: cross-source triage
When a Codex session's output (e.g. code stats, analysis results) is then pasted or paraphrased by Vadim into a Telegram chat in the same heartbeat window, you will see both a Codex record AND a TG record with the same underlying data. Triage rule:
- The **Codex record** is a no-write fast path (Mac-local, no Obsidian needed unless genuinely new outcome).
- The **TG record** carries the social/business context and is the one to log — write the Log entry to the relevant person note, referencing the content as "shared from Codex session" if helpful.
- Do NOT create two separate entries for the same underlying event. The TG exchange is where the facts matter.

Session example (2026-06-27): session `019f080d` ("Посчитай строки кода", vox-harbor) generated code stats Vadim then shared with Sasha Pokras at 07:56-08:13 UTC. Codex record = no-write fast path. Sasha TG exchange = single Log entry on Sasha's note.

### Multi-record same-session Codex fast path
When `vadimgest read` returns **2–N records** and they are ALL turns of the same Codex session (identical `session_id`), treat this as a single no-write fast path:

**Scale note:** sessions can generate 10–20+ continuation turns between heartbeat cycles (e.g., session `019ed978` generated 19 new records across a single heartbeat window). The presence of many records does NOT mean more triage work — if all share a `session_id`, it's the same fast-path regardless of count.

**Sub-case: same session_id, different phase names across cycles.** A long-running session can change its `title` across phases while retaining the same `session_id`. Example: session `019ee16c` appeared across many cycles as "OB/GYN P4 readiness counts" (readiness phase) and later as "Beamforming" (supervision phase). Both are the same session. The title change does NOT trigger a new Obsidian write — check `session_id` identity first, not the title. Only write if the new phase produced a genuinely new outcome not yet in the existing Log entry.

1. **Confirm session_id identity.** Read the JSONL directly — all N records should share `session_id`. If `created_at` spread is within 30 minutes, treat as one session.
2. **Check session_id against Obsidian.** If already logged in a Study Log / project note from a prior cycle, this is a continuation — no new write needed.
3. **Commit and note.** Append one daily memory line: "Codex <session title> — N turns of session <id>, already tracked." Commit cursor and confirm no-op.

**Sub-case: multi-day session with turns on both sides of the checkpoint.**
A Codex session can start on day N, be logged in daily memory, and then generate new turns on day N+1 that appear fresh in the intake. The checkpoint line (`positions.codex.line`) may land mid-session. Pattern to handle:
1. Check `_line` of the new records vs `checkpoints/intake.json positions.codex.line`. Lines above the checkpoint are genuinely new.
2. If `session_id` was already logged in daily memory (yesterday or today), check those turns' `created_at` — if they're still on the same topic with no new facts (e.g. continuing the same analysis loop), treat as continuation and skip Obsidian write.
3. If the new turns' titles reveal a *new task* or a *new result* not in the existing log, write a note to daily memory + Obsidian as if it were a fresh session.
4. The ground truth is: same session_id + same topic loop = continuation no-write. Same session_id + task/outcome change = write.

Session example (2026-06-21): `019ee16c` (OB/GYN P4 readiness counts) started Jun 19, 8 turns logged in Jun 20 memory. Checkpoint at line 8174. Two new turns at lines 8184-8185 (Jun 20 23:02-23:03 UTC) arrived in the Jun 21 intake. Same title/topic as prior turns — no new facts. Treated as continuation, no Obsidian write, noted in daily memory only.

Session example (2026-06-20 ~15:56 UTC): 4 records all from session `019ed978` (W&B SoTA analysis, 12:00-12:23 UTC). Same session logged in Caterpillar Study Log 2026-06-18, referenced in 10+ prior heartbeat daily memory entries. No write needed.

**Key check for the multi-record case:** verify `len(set(r['session_id'] for r in records)) == 1` — if there are 2+ distinct session IDs in a small Codex-only batch, fall through to the standard small-batch triage instead. For sub-step outcome turns (e.g. "val is now fast enough"), daily memory only is correct — no Obsidian write needed. Full decision table: `references/codex-continuation-turn-outcome-triage.md`.

### Single-record batch: 1 Codex turn = almost always a no-write fast path
When `vadimgest read` returns exactly **1 record** and it is a Codex session turn, execute this fast path:

1. **Read the JSONL record directly** — get `session_id`, `thread_id`, `cwd`, and the full `title` (the intake view truncates at ~80 chars).
2. **Check `session_id` against Obsidian.** If the same `session_id` already appears in a Study Log / project note entry from a prior cycle, this is a continuation turn — no new write needed.
3. **Verify with checkpoint line** — confirm `_line > checkpoints/intake.json positions.codex.line` (see pitfall below). If equal or lower, something is wrong with the cursor; investigate before committing.
4. **Commit and report no-op.** Append a brief daily memory block noting "Codex W&B/X session — continuation, already tracked," commit the cursor, confirm no remaining data.

Session example: session `019ed978` (W&B SoTA analysis) — already in Study Log, 6 prior daily memory entries. No write — commit + HEARTBEAT_OK. 📋 `references/codex-single-record-sub-patterns.md` — result-confirmation Q&A turns, ops failure noise, strftime pitfall for daily memory.

### Small-batch triage (< 15 records): fast-path decision rules
When `vadimgest read` returns a small batch (say, 2–15 records), use this fast path instead of a full triage sweep:

1. **Identify the one novel event.** Most small batches = 1 new conversation thread + N continuation Codex turns. Find the thread with new facts.
2. **Codex dedup first.** Check if repeated Codex prompts are turns of the same session (same prompt prefix + created_at within 10 min). If yes, treat as one session. Check Obsidian for whether it's already logged — if it is, skip.
3. **Write only for the novel event.** A small batch typically warrants one Obsidian update (State + Log), one daily memory append, and one commit. Do not manufacture additional writes.
4. **Report the novel event prominently.** If there's a time-sensitive signal (call happening now, person moving fast), surface it first in the heartbeat report — even before the standard intake count line.

Session example (2026-06-20 07:36 UTC): 8 records = 5 Gleb TG (Toms proposed call <24h after intro, URGENT) + 3 Codex W&B continuation (already tracked). Fast path: one Gleb State+Log update, daily memory append, commit. Done.

### Intake sections to expect and triage order
1. `## Telegram` — scan all `###` chats; skip `Клава` body; prioritize: active deals > personal with action > new contacts > passive personal
2. `## Signal` — often contains Vox Lab / Sasha Pokras / defense contacts; high priority
3. `## Codex` — agent session IDs; extract only completed sessions with meaningful outcomes
4. `## Obsidian` — new/modified notes; check if they need cross-linking or triage
5. `## Gmail` / `## LinkedIn` — check for deal responses or cold intro replies

### Premature "Resolved" markers: verify before trusting
When a prior Log entry contains a "**Resolved X:XX UTC:**" marker (or "Closed." / "Loop closed." etc.), do NOT treat it as ground truth. Vadim often says "Сейчас сделаю" / "А это вроде бы приглашение / Сейчас сделаю" / "OK буду" — intent-to-act phrases that a prior heartbeat marked as resolution. The actual action may never have happened.

**Verification rule:** if a new intake message from the same contact appears to re-ask the same thing (follow-up, reminder, "скинешь?", "ну как?", "напомни"), the prior "Resolved" was premature. Immediately:
1. Re-open the Log entry: replace "Resolved...Closed." with "Vadim said he would X. **Still open:** [new message]. Reply pending."
2. Update `last_contact` frontmatter + State bullet to the new message date.
3. Surface in the heartbeat report under 🔔 ACTION NEEDED — Vadim still has to send/do this.

**Intent-to-act phrases that do NOT mean "done":**
- "Сейчас сделаю" (I'll do it now)
- "А это вроде бы X / Сейчас сделаю" (I think this is X / I'll send it now)
- "Ок, буду" / "Окей" without a follow-up confirmation
- "Разберусь" (I'll figure it out)

Only mark Resolved when: (a) the follow-through message is explicit ("Отправил" / "Done" / "Sent"), or (b) the other party confirms receipt ("спасибо, получил" / "got it").

**Third–Sixth resolution states:** see `references/resolution-states.md` for full specs, Log entry shapes, and session examples. Quick summary:
- **State 3 — mechanism unavailable:** Vadim tried, system said no ("Не даёт больше"). Promise closed, underlying need open. Surface alternative route.
- **State 4 — pivoted to alternative:** Access via different means (shared credentials). Log "access path: shared credentials" — NEVER the credentials themselves. Follow up next cycle.
- **State 5 — 2FA blocking:** Credentials provided but phone verification blocking completion. NOT closed. Log as Continuation.
- **State 6 — conversational thread closed, operational loops still open:** Contact sends a social closure ("спокойной ночи", "да, спал", "ок понял") that closes the exchange but not the underlying task. Extend the same Log entry; do NOT mark open loops closed. (Session example: Artyom goodnight Jun 22 — exchange closed, Latvia + 2FA loops still open.)

Session example (2026-06-21): Artyom's Jun 20 Claude link request — prior heartbeat marked "Resolved 20:04 UTC: Closed." → Artyom sent "скинешь?" at 21:43 Jun 21 → loop not closed, Obsidian entry corrected to "Still open."

### Additive messages: extend existing Log entry vs. create new one
When new intake messages continue the same conversation thread as an already-written Log entry (same day, same topic, same `src` chat), decide:

- **Create new Log entry** if: new fact changes State, new event occurred, or enough new content (~3+ messages) to stand alone.
- **Extend existing summary** if: 1-2 messages add a detail/quote to a thread already logged, no new State fields change.

**Sub-case: "pending reply" annotation gets resolved.** When a prior Log entry ends with a note like "A reply from Vadim would be kind / loop still open / reply pending" and the next cycle delivers Vadim's actual reply, extend that existing entry rather than creating a new one. Add the reply text + its `src:` URI inline in the summary and mark it closed. Do NOT duplicate the `src:` line — just extend the summary prose with "Vadim replied at HH:MM UTC: '...' · src: `<uri>` · YYYY-MM-DD." This keeps the full exchange in one Log entry without a noise entry for a single-message response.

**Sub-case: earlier-in-the-day request gets resolved later the same day.** When a morning message asked Vadim to do something ("можешь такую ссылку еще раз скинуть?" = please resend the link) and a later-in-the-day message shows Vadim resolving it ("А это вроде бы приглашение / Сейчас сделаю"), extend the earlier Log entry's summary with "**Resolved HH:MM UTC:** <what Vadim said>. Closed." Update `last_contact` src to the later message. Same rule applies whether same cycle or different cycles. Session example (2026-06-20): Artyom's 09:08 Claude link request resolved by Vadim's 20:04 reply.

Extension pattern: `content.replace(old_summary, old_summary + ". Follow-up: <new detail>", 1)`.

Session example: 2 Sasha messages added "digital twins of mouse/macaque brains" + "Wow, we need him" to an existing entry. Extended, not new entry — recruit signal also triggered creating Misha Bilokur note.

**Sub-case: reply received but loop still open (reply is a question).** When a prior entry said "X hasn't replied, loop open" and X replies with "кто?" / "когда?" / any question — do NOT close. Extend: "Follow-up HH:MM: X replied '[question].' Ball in Vadim's court — [what's needed]." See `references/additive-log-patterns.md`. Example (2026-06-22): Van0SS replied "кто?" to Vadim's RL env intro — loop still open, Vadim needs to name the person.

### Stale tentative State fields
When a new message *confirms* or *supersedes* a State bullet that was written as tentative/pending (e.g., `office_visit: tentatively Tuesday — not yet confirmed`), the Log entry must also update the State bullet to remove the tentative qualifier and replace the old src/date. Two-step pattern:
1. Append the Log entry as normal.
2. Rewrite the State bullet: new value + new src + new date. Don't leave the old tentative phrasing in State even if it's older — State is current truth, not history.

If the State bullet was entirely superseded (e.g., `office_visit` moved from "tentatively Jun-17" to "confirmed Jun-20"), also update frontmatter `last_contact` to match.

### Clock skew in heartbeat_state.json and jobs.json
Both `heartbeat_state.json last_run` and `jobs.json last_run_at` can carry future timestamps due to timezone offset or clock drift. Do NOT use either to infer recency. Use artifact file mtime (`ls -la cron/output/ff50067ec588/`) as ground truth, and `vadimgest read --consumer intake` to confirm cursor state. Also: daily memory files may be dated one day ahead of UTC — always use `date -u` and write to whichever file is already active. Full details: `references/clock-skew-pitfalls.md`.

### State key duplication on update/reschedule
A single State key must appear **exactly once** in `## State` with **exactly one** `· src:` field. Two failure modes:
- **Duplicate bullets** — prior heartbeat left both "tentative" and "confirmed" bullet for the same key. Collapse to most recent; add a Log entry.
- **Double-src in one bullet** — prior heartbeat chained `· src: X · date: note · src: Y · date` in a single bullet. Collapse to most recent src in the same write pass.

📋 `references/state-bullet-single-src-rule.md` — full patterns, fix code, session example (Ramazan Jun-25).

### jobs.json structure — use defensive parse
`/srv/codex-klava/data/hermes/cron/jobs.json` has been observed in **two formats** across deployments:
- `{"jobs": [...]}` — object with a `jobs` key (confirmed 2026-06-20, 19 jobs)
- A flat JSON array `[...]` at the top level (older deployments)

Do NOT hardcode either assumption. Use the safe parse pattern that handles both:

```python
import json, sys
data = json.load(sys.stdin)
jobs = data if isinstance(data, list) else data.get('jobs', data.get('cron_jobs', []))
for j in jobs:
    if isinstance(j, dict) and j.get('enabled'):
        print(j.get('id','?')[:12], '|', j.get('name','')[:40], '|', j.get('last_status','?'))
```

The `isinstance(j, dict)` guard catches accidental string iteration if structure changes. The `data.get('jobs', data.get('cron_jobs', []))` chain handles both known wrapper key names.

**Never-run jobs show `None` on all time/status fields — this is normal, not an error.** A freshly-added job that has never triggered will have `last_run_at: None`, `last_status: None`, `next_run_at: <first scheduled time>`. Do NOT classify a `None` status as a failure. Example: `e67d66896ba9` (English Coach Weekly Report, scheduled Monday 10:00) shows `last_status: None` until its first Monday run — correct state, not an alert.

**Pitfall — any job field can be `None` for never-run or partially-initialized jobs.** This includes `last_run_at`, `last_status`, `next_run_at`, and similar fields. Two failure modes:

1. **Slicing `None`** raises `TypeError: 'NoneType' object is not subscriptable` — wrap with `str()`:
```python
# WRONG — crashes if last_run_at is None:
j.get('last_run_at','?')[:16]

# CORRECT:
str(j.get('last_run_at','?'))[:16]
```

2. **Format strings on `None`** raise `TypeError: unsupported format string passed to NoneType.__format__` — use explicit `str()` or avoid f-string format specs on fields that could be None:
```python
# WRONG — crashes if last_status is None:
f"{j.get('last_status','?'):8}"

# CORRECT:
str(j.get('last_status', '?')).ljust(8)
# or just:
str(j.get('last_status', '?'))
```

**Safe pattern for printing job summaries:**
```python
for j in jobs:
    if isinstance(j, dict) and j.get('enabled'):
        jid = str(j.get('id', '?'))[:12]
        name = str(j.get('name', ''))[:40]
        status = str(j.get('last_status', '?'))
        last_run = str(j.get('last_run_at', '?'))[:16]
        print(f"  {jid} | {status} | {last_run} | {name}")
```

This applies to any field on a freshly-added job that has never run, or any optional field the scheduler may not yet have populated.

### Extended Codex triage patterns
📋 `references/codex-session-triage-patterns.md` — partial-findings sessions, "pending reply annotation gets resolved", investor-list no-action pattern, rollout JSONL extraction, commentary-only sessions.

📋 `references/codex-ops-supervision-pattern.md` — Ops-supervision sessions; triage as `[OPS supervision]`.
📋 `references/loop-closure-patterns.md` — artifact-as-loop-closure (PDF proves a promise), Klava self-improvement session noise sub-case.

📋 `references/backfill-cursor-gap-pattern.md` — backfill writes Inbox triage note but does NOT commit cursor; main heartbeat must do entity writes + commit. Detection: compare Inbox note mtime vs checkpoint mtime.

### vadimgest commit is a separate step — `read` has no `--commit` flag
`vadimgest read` does **not** accept a `--commit` flag. Passing it is silently ignored — the cursor does not advance. The correct two-step:

```bash
# Step 1: read and process the records
SOURCES=$(find -L /srv/codex-klava/data/vadimgest/sources -maxdepth 1 -name '*.jsonl' ! -name 'browser.jsonl' ! -name 'xnews.jsonl' -printf '%f\n' | sed 's/\.jsonl$//' | sort | paste -sd, -)
env -u PYTHONPATH VADIMGEST_CONFIG=/srv/codex-klava/data/vadimgest/config.yaml VADIMGEST_DATA_DIR=/srv/codex-klava/data/vadimgest /srv/codex-klava/venvs/vadimgest/bin/vadimgest read --consumer intake --sources "$SOURCES" -f md --context 3 --limit 200

# Step 2: after processing, commit only sources that were fully visible
env -u PYTHONPATH VADIMGEST_CONFIG=/srv/codex-klava/data/vadimgest/config.yaml VADIMGEST_DATA_DIR=/srv/codex-klava/data/vadimgest /srv/codex-klava/venvs/vadimgest/bin/vadimgest commit --consumer intake --sources "$SOURCES"
```

Verify the commit worked by re-running the read command. If any source printed `... +N more`, remove that source from `$SOURCES`; process it through the heartbeat edge backfill script or a source-specific batch and commit the exact processed line instead.

**Pitfall:** calling `read ... --commit 2>&1` looks like it might work but the flag is dropped. Always separate read from commit.

### Silence detector JSON has control characters — use file+regex fallback
📋 `references/silence-detector-control-chars.md` — full pattern. Also: `references/silence-detector-execute-code-pattern.md` — always use /tmp script from execute_code (inline -c + f-strings breaks every session); covers find|xargs grep space-path failure (use grep -rl).

### tasks.queue full API surface and common pitfalls
📋 `references/tasks-queue-api-pitfalls.md` — full verified export list, `update_task` does not exist (use `update_task_notes` instead), `complete_task` has no `note=` kwarg, `create_proposal` uses `plan=` not `body=`, topic-dedup behavior, and the proposal scope-drift update pattern.

### complete_task() has no 'note' kwarg — inspect before batch ops
📋 `references/tasks-queue-api-pitfalls.md` — `complete_task(task_id: str, list_id: str = None)` only. No `note=` kwarg. Also covers full API surface, `update_task_notes` vs `update_task`, and batch completion safe pattern.

### Org stub creation during reflection: when to create
During cross-link sweep (Phase 3), if a person note references a company/org as **plain text** (e.g. `company: "Sazabi (YC)"` in frontmatter, or `merged with YC company Sazabi` in body) but no `Organizations/Sazabi.md` exists, create a minimal stub. Signals:
- New person note created this cycle with a non-trivial `company:` field
- Body text references a company with `[[...]]` wikilink that has no backing file
- The company is relevant to Vadim's network or deals (not a random employer)

Stub format — minimal but State+Log compliant:
```markdown
---
tags: [organization, <domain>, <other-tags>]
status: active
last_contact: YYYY-MM-DD
---

# Company Name

One-sentence description from the context that surfaced it.

## State

- **category:** <what they do> · src: `<source-uri>` · YYYY-MM-DD
- **contact_via:** [[Person]] → [[Introducer]] · src: `<source-uri>` · YYYY-MM-DD

## Log

### YYYY-MM-DD — Org stub created from [person] intro context
- **src:** `<source-uri>`
- **mentions:** [[Person]], [[Introducer]]
- **summary:** [ORG new stub] One-sentence origin story.
- **facts-touched:** category, contact_via
```

After creating the stub, update the person note to replace plain text with `[[OrgName]]` wikilinks (both in body and State bullet).

### Codex session triage: detect "discussed but wrote nothing durable"
Short Codex sessions (2-3 turns, < 5 min): check `has_writes = any(k in content for k in ('write_file','patch','str_replace','create_file','apply_patch'))`. If False + turns ≤ 2: conceptual — pending task, not done. See `references/codex-session-triage-patterns.md`.

### Image/screenshot records: two-sub-case triage
Full patterns, decision tree, and session examples: `references/image-ocr-triage-patterns.md`.

**Sub-case A — readable financial/document screenshots (e.g. crypto deposits, receipts):**
Extract key facts from OCR, write a `[FINANCIAL signal]` Log entry, add a `crypto_screenshot` (or equivalent) State bullet, leave exchange open if Vadim asked "Это что?" and sender hasn't replied. Do not create a task. Session example (2026-06-22): Dad's 500 USDC BEP20 deposit screenshots.

**Sub-case B — garbled OCR (rotated/photocopied Cyrillic → Latin):**
OCR content is not the signal — surrounding message context is. Write Log entry describing intent, note garbled OCR explicitly, leave open if no resolution. Session example (2026-06-20): Sasha NDA screenshot rendered as `"Kak Tbl AYM@eLb..."`.

**Quick rule:** OCR legible → doc (A); OCR garbled → context-driven (B); complaint+image → complaint is signal, OCR is context (C); sender==Vadim → outgoing (D). Full specs: 📋 `references/image-ocr-triage-patterns.md`.

### JSONL intake edge cases (truncation, line collisions, checkpoint semantics)
See `references/jsonl-intake-pitfalls.md` for: `conversation` type records (dominant DM format — top-level `text`/`sender` empty, messages in `r['messages']` list; 2026-06-22), display truncation vs source-side truncation, `_line` collision (use `_ingested_at >= checkpoint updated_at`), and reading by `source_uri`.

📋 `references/ambiguous-message-disambiguation.md` — short bursts with no referent: trace JSONL, "?" = clarification incoming.

### JSONL direct read (vadimgest search fallback)
📋 `references/source-uri-lookup-patterns.md` — full patterns: `source_uri` construction, chat_id discovery, multi-message burst URI extraction.
📋 `references/vadimgest-read-plus-n-more-pattern.md` — `... +N more` in vadimgest read is usually view truncation; JSONL-verify the latest record before leaving a source for backfill.
📋 `references/catallax-buyer-lane-identity-resolution.md` — resolve short company names ("Кrea написала") as Catallax buyer lanes; cross-write pattern (Pufit note + deal note + org stub).

When search returns empty, read raw JSONL — write multi-line lookups to `/tmp` scripts (inline `-c` fails on `for` loops):

```python
script = """
import json
records = [json.loads(l) for l in open('/srv/codex-klava/data/vadimgest/sources/telegram.jsonl') if l.strip()]
chat = [r for r in records if r.get('chat','') == 'Chat Name Here']
recent = chat[-15:] if len(chat)>=15 else chat
for r in recent:
    print(r.get('timestamp',''), '|', r.get('sender',''), '|', r.get('text','')[:150])
"""
with open('/tmp/jsonl_read.py', 'w') as f: f.write(script)
# terminal("python3 /tmp/jsonl_read.py")
```

**Key fields:** `chat`, `sender`, `timestamp`, `text`, `meta.chat_id`, `meta.message_id`, `source_uri`. **Empty `source_uri`** is common on incoming messages — construct it as `vadimgest://telegram/<chat_id>_<message_id>`.

Session example (2026-06-20): Igor Blink — vadimgest search empty, JSONL showed full conversation.

### Commercial/marketing Telegram senders = always noise
Brand/service marketing channels (luxury concierge, bank promos, premium card services like CinCin Exchange) are pure noise. Recognition: pitch language ("Личный консьерж", "24/7", "безграничные возможности"), sender is a brand not a person, no Vadim replies. **Triage rule:** skip, no write, just commit cursor.

**Site deploy verify:** after vadi.ms push, grep repo source — not live curl. CDN: 1-3 min. Full pattern: `references/site-deployment-verification.md`. Gmail/Codex triage patterns (empty-body Gmail, Mac-local commentary sessions, training-pipeline ops, Signal "+N more"): 📋 `references/gmail-codex-triage-patterns.md`.

The `vadimgest read` intake output for `## Codex` entries only shows titles (truncated at ~80 chars). Look up the full title from JSONL directly — it is usually the Codex task prompt. Cross-reference with Obsidian notes to determine if the session outcome is already captured. If the Codex session was a continuation of work already logged in the current Obsidian note, no new write is needed — note it in daily memory instead.

📋 `references/codex-single-record-sub-patterns.md` — Q&A turns, ops noise, strftime pitfall. `references/codex-session-id-lookup-pitfalls.md` — **daily memory grep (not Obsidian) for same-day session-ID checks** — Obsidian times out 15s+; dedup; fast-path decision tree.

📋 `references/codex-session-type-session-triage.md` — `type: session` Mac-local records (prefix `session_MacBook-Pro-Vadim.local_...`). Read final assistant message; note in daily memory only; no Obsidian write unless significant.

### Large Obsidian notes (>100K chars): read_file rejects, use targeted terminal reads
Some project notes (e.g. Caterpillar Study Log, Vox deals with long history) exceed `read_file`'s 100K char safety limit. When `read_file` returns `"Read produced N characters which exceeds the safety limit"`:

```bash
# Find section line numbers
grep -n "## Study Log\|## State\|## Log\|### 2026" "/path/to/note.md" | tail -20

# Read specific section by offset
read_file(path, offset=61, limit=60)   # offset = line number from grep

# Read tail for most recent entries
terminal('tail -80 "/path/to/note.md"')
```

Pattern: use `grep -n` to find the line number of the section you need, then `read_file` with `offset=<line>` and a small `limit`. For Study Log / recent entries, `tail -80` is usually enough.

### MyBrain on codex-klava is NOT a git repo — do not git commit
`/srv/codex-klava/data/MyBrain` syncs via `obsidian-headless-sync` from Vadim's Mac. There is no `.git` directory. Never attempt `git -C /srv/codex-klava/data/MyBrain commit` or `git add` — it will always fail with `fatal: not a git repository`. Writes via `patch` or `write_file` go directly to disk and sync outward automatically. No commit step needed or possible.

### Log summary extension: exact-text pitfalls and hiring pipeline two-cycle escalation
See `references/log-extension-pitfalls.md` for: em-dash/quote mismatch handling, safe `repr()`-then-replace pattern, multi-field update order, and the yap-complaint → engineering-disqualification two-cycle shape.

### patch uniqueness on notes with multiple `## Log` sections
Some person notes (e.g. Vladislav Dombrovsky) contain multiple `## Log` headers — one per chat source. A `patch` call using `old_string: "## Log\n\n### YYYY-MM-DD..."` will fail with "Found N matches." Fix: include enough of the first list item after the target `## Log` heading so the match is unique. Typically 2-3 lines into the first entry is sufficient:

```python
# Too short — matches all ## Log sections:
old_string = "## Log\n\n### 2026-06-18 — Title\n"

# Sufficient — include the src line to make it unique:
old_string = "## Log\n\n### 2026-06-18 — Title\n- **src:** `tg://...`\n"
```

Alternatively, use `grep -n "## Log"` first to find which line number contains the target section, then prepend the preceding non-Log line as context anchor.

### str.replace() uniqueness when inserting after a Log entry's facts-touched line
When appending a new Log entry after an existing entry's `facts-touched:` line, the anchor string must be unique across the whole file. Using only `"- **facts-touched:** key1, key2"` may work if there's one match, but it is fragile. The safe pattern anchors on both the `facts-touched` line AND the header of the **next** Log entry immediately below:

```python
# Fragile — only works if there's exactly one matching facts-touched line:
old = "- **facts-touched:** last_contact, meeting_scheduled"

# Robust — includes the next section header to make match unambiguous:
old = "- **facts-touched:** last_contact, meeting_scheduled\n\n### 2026-06-07 — fUS for brain write"
new = "- **facts-touched:** last_contact, meeting_scheduled\n\n### 2026-06-20 — New entry\n...\n\n### 2026-06-07 — fUS for brain write"
```

Rule: when inserting between two Log entries, always include at least the first line of the *following* entry in `old_string` so the insertion point is pinned. This is especially important in long notes with many entries sharing similar key names.

### Obsidian edge-sync records: check server before creating
The `## Obsidian` section in `vadimgest read` output shows records synced from Mac (paths like `/Users/vadimchashechnikov/Documents/MyBrain/...`). These notes are mirrored to the server at `/srv/codex-klava/data/MyBrain/...` via obsidian-headless-sync.

**Before creating a new note that appears in the Obsidian intake section**, check whether it already exists on the server:
```bash
ls "/srv/codex-klava/data/MyBrain/People/Person Name.md"
# or
find "/srv/codex-klava/data/MyBrain/People" -name "*Keyword*"
```

If the file exists with the same content the prior heartbeat wrote, it is already current — no write needed. The Obsidian intake record is just the edge-sync event arriving in vadimgest after the file was written on Mac.

**Pitfall:** Always `stat` or `cat` the server path first — do not create duplicate notes.

**Sub-case: file not yet on server (sync lag).** `find` returns empty — obsidian-headless-sync hasn't delivered the file yet. Do NOT write based on filename inference — note expected resolutions in daily memory and defer all writes to next cycle. Report as "🔔 Meeting note pending sync." Full pattern: `references/obsidian-sync-lag-triage.md`.

**Sub-case: Hlopya meeting notes as Obsidian intake events.** Synced from Mac via obsidian-headless-sync. Triage: confirm file exists on server, read it (Action Items + Decisions are the signal), cross-write key facts to participant People notes, do NOT rewrite the meeting note itself. Participants listed in frontmatter `participants:` field.

**Sub-case: `[[People/X]]` wikilink in meeting note has no backing file** → search for a partial-identity note first (`grep -r "identity_unresolved" People/`), confirm match via Calendly URL / company / project context, update the existing note in place (do NOT create a new file, do NOT rename), resolve `identity_unresolved` State bullet, add meeting Log entry, also update any project Study Log with confirmed dates/milestones from the same meeting.

📋 `references/hlopya-meeting-cross-write-patterns.md` — full pattern with session examples (2026-06-21 equity extraction, 2026-06-23 Kevin J = Kevin Joo identity resolution).

### Recruit-candidate people notes
When a new contact is flagged as a potential technical recruit (Vadim says "we need him", "can I invite them", "would be useful for Alegria/SSI work"), the person note should include these State bullets:

```markdown
- **recruit_signal:** <exact Vadim quote + context> · src: `<uri>` · YYYY-MM-DD
- **applied_work_signal:** <Sasha/referrer's assessment of willingness to do applied work> · src: `<uri>` · YYYY-MM-DD
- **vadim_condition:** <any constraints Vadim set, e.g. "Lev shouldn't poach him"> · src: `<uri>` · YYYY-MM-DD
- **research_group:** <what group/lab/project they're in, and who else is there> · src: `<uri>` · YYYY-MM-DD
- **first_meeting:** <date, time, location> · src: `<uri>` · YYYY-MM-DD
```

Key signal phrases:
- "Wow, we need him/her" → `recruit_signal` State bullet immediately
- "would be useful to either you or Lev" → cross-reference with Caterpillar/SSI project note
- "he/she would do applied work if interesting enough" → `applied_work_signal`

### Single-word follow-up from a contact with a pending PROPOSAL = urgent action item
📋 `references/single-word-followup-pending-proposal.md` — when "hey"/"привет"/"?" arrives after 7d+ gap from a contact with an open PROPOSAL, treat as follow-up, surface as action needed. Session example: Ilya HighTower "hey" Jun 29.

### Stable Telegram contact identities
Some recurring contacts appear under non-obvious display names or handles. Known identities (do not re-derive).

📋 `references/intake-noise-patterns.md` — WeightLossBot/Fit Mentor bot reminders, Клава system pings, large Клава completed-session fast-path, **active Klava mid-session detection** (mid-task at heartbeat time: detect via `⏳ Working —` tail, report INCOMPLETE, don't re-do in-progress work). 📋 `references/bee-intake-triage-patterns.md` — `bee_fact`/`bee_conversation`/`bee_daily_summary` triage, "Unknown source: bee" PYTHONPATH false alarm fix, sync gap detection.

**Fast resolution path — frontmatter `handle:` field.** Before doing any deduction, search the People notes for a `handle:` frontmatter key matching the Telegram display name. Many personal contacts are pre-resolved this way:

```bash
grep -rl 'handle: "Natuska"\|handle: Natuska' /srv/codex-klava/data/MyBrain/People/
```

Or search across all:
```bash
grep -r "^handle:" /srv/codex-klava/data/MyBrain/People/ | grep -i "DISPLAY_NAME"
```

This resolves immediately for family and close contacts (e.g., `handle: "Natuska"` → Наташа Чашечникова.md). Only fall through to alias deduction if `grep` finds nothing.

Core entries (also in the index):

- **Toms 👾** — Toms Cernavskis (roam.lol), founder. TG display name includes the game controller emoji. File: `People/Toms Cernavskis (roam.lol).md`. Matched via phone `+1 (628) 240-4507` in frontmatter.
- **Artinleather** — Vadim's dad. Casual personal chat: short check-ins, YouTube links, occasional equity/business updates. `tg://artinleather/...`. Any message from him is personal, low urgency unless he mentions equity, Roko, or Vox structure.
- **Pufitus II** — Artem Pufit (CTO Vox Lab). TG account name differs from note name. If Vladik says "ответь пуфиту" / "ПУФИТ" — that's a ping to reply to Pufitus II = Pufit.
- **Natuska** — Наташа Чашечникова, Vadim's mother. Family contact in Riga. Warmly personal (calls him "котенок", "солнц"). Messages are typically: check-ins, tech help requests, family logistics. Handle stored in frontmatter as `handle: "Natuska"`.

### Short-alias contacts: cross-cycle identity resolution
Telegram sometimes surfaces contacts under a single letter or short alias (e.g. "D", "M", "R") when the phone number isn't in Vadim's contacts under a full name. These require active identity resolution before writing to Obsidian:

1. **Check prior daily memory first.** Search `/home/codex/.klava/memory/YYYY-MM-DD.md` for the alias — a prior heartbeat may have already identified the person.
2. **Check context clues in the intake.** What did they ask about? What topic? Who else mentioned them?
3. **Check existing Obsidian People notes** for anyone who fits (location, topic, mutual connection).
4. **Don't create a new note under the alias.** Write to the identified person's note. If identity is uncertain, note it as "likely X" in the State bullet's summary with a `?` qualifier.
5. **Don't block the cycle on unresolved identity.** Create a stub under `People/<alias> (identity unresolved).md`. Set `follow_up:` to tomorrow so it surfaces again next cycle. Full stub pattern: `references/identity-stub-patterns.md`.

Session example: "D" appeared in two consecutive heartbeat cycles. First cycle: identified as "likely Danielle Strachman (1517 Fund)" from context (SF, investor, asked for calendar slots). Second cycle: confirmed by behavior (meeting arranged for next day) → wrote to Danielle Strachman note.

### Vox Compliance Bot output in intake = Vadim ran OSINT on a contact
When `### Vox | Compliance Bot` appears in the intake with messages like "Previous names: ...", "Language: ru Sex: male Age range: ..." — Vadim queried the bot with `@handle`. This is NOT noise. Triage as:

1. **Who is the target?** The bot message immediately follows a Vadim message like `[04:01] Vadims Casecnikovs: @IgorBlink`.
2. **Does the person have an Obsidian note?** If yes, add an `osint_run` State bullet with the key profile fields (age range, location, role, interests). If no, create a minimal people note with those fields.
3. **osint_run State bullet format:**
   ```
   - **osint_run:** <key fields: gender, age range, location, role, interests> · src: `tg://vox-compliance-bot/YYYY-MM-DD` · YYYY-MM-DD
   ```
4. **Red flags to surface:** bot outputs "Is bot: True", known scam/spam groups in the Groups section, unusual name-change history. If present, flag in the heartbeat report as `[SECURITY signal]`.
5. If the target is a Vox team member or known contact with a full note, the osint_run bullet is still worth adding — it shows Vadim is actively vetting someone in the context of a deal or hire.

**Sub-case: bot returns null result ("can't gather enough information")**
When the bot outputs `"Unfortunately I can't gather enough information about user #XXXXXXX. Try another one."` — this is still actionable:
- The OSINT attempt happened; log it. Create or update the person note with an `osint_run` State bullet marked `null — insufficient public data`.
- `osint_run` null format: `- **osint_run:** null (bot: insufficient data on #XXXXXXX) · src: \`tg://vox-compliance-bot/YYYY-MM-DD\` · YYYY-MM-DD`
- A null result often means: private account, no Telegram username, or brand-new account. Worth noting — it tells Vadim the contact is unlookable by this method.
- Do NOT skip the write just because the bot found nothing. The attempt itself is signal (Vadim is actively vetting this person).

**Sub-case: contact forwarded by a trusted friend (not directly queried by Vadim)**
Sometimes a trusted contact (Vladik, Sasha, etc.) sends someone's TG ID + phone number to Vadim first, and then Vadim queries the bot with that ID. Recognition pattern:
- Friend sends: `5821420253` / `telegram id 5821420253` / `phone number +XX X XXXX XXXX` — labeled, structured
- Then: `[08:11] Vadims Casecnikovs: 5821420253` to the bot
This is different from Vadim independently looking someone up. The friend is the referral source; the phone number provides a cross-platform identifier (country code often tells you something). Log as:
- `osint_run` State bullet on the unknown contact (create a stub note if none exists, title = "Unknown contact #5821420253" until identified)
- Note the forwarding context: "forwarded by [[Vladislav Dombrovsky]]" in the summary
- Australian number (+61 4 prefix) = mobile number, not landline. Country context worth noting if geographically unexpected.

### Vadim brokering intros for his network (not for himself)
Vadim sometimes asks a contact to connect him to a third party *on behalf of his own friends/colleagues*, not for personal business reasons. Recognition pattern:

- Phrase: "можешь пожалуйста сконектить с ребятами этими, я думаю, как минимум могу их с друзьями соединить, которые делают X" — "can you connect me with these guys, I can connect them with friends who do X"
- The ask is symmetric: Vadim is offering his network as *value* in exchange for the intro.
- This is **not** a Vox sales lead and **not** a personal deal. It is network brokering.

**Triage rule:**
1. Classify as `[NETWORK brokering]` in the Log entry (not `[DEAL new]` or `[OPPORTUNITY]`).
2. Add a `<topic>_connection_request` State bullet (e.g. `rl_connection_request`) pointing to the contact Vadim asked.
3. No Google Task needed — this is conversational, not a tracked deliverable. Surface it in heartbeat report as "awaiting Nur intro to RL environment builders" but don't create a task unless Vadim explicitly marks it as important/time-sensitive.
4. If the contact makes the intro in a later cycle, update the State bullet to `<topic>_connection: made` and add a Log entry.

Session example (2026-06-20): Vadim asked Nur to connect him with "exclusive RL environments" builders — Vadim's pitch is he can connect them with his own friends in that space. `rl_connection_request` State bullet added. No task created.

### Late-sync media artifacts: stale-timestamp records in current intake
Vadimgest occasionally delivers a record whose `timestamp` is days or weeks in the past — typically a media file (video, audio, image) that was written to disk late or whose sync event was delayed. Recognition signals:
- Record appears in the current intake batch but its timestamp is significantly older than today's date (e.g., Jun 15 record appearing in a Jun 21 intake run)
- The record is a `[Document: ...]` or media attachment, not a text message
- The surrounding context messages in that chat (via JSONL direct read) all belong to the old date

**Triage rule:** treat stale-timestamp media records as **no-action** unless the media's content is independently significant (e.g., Vadim sent a video that was requested by someone in a later message). Steps:
1. Check the record's `timestamp` field against today's date — if it's >24h stale, it's a late-sync artifact.
2. Check whether there is a conversation thread around that timestamp that already got processed in a prior cycle (confirm via daily memory or Obsidian Log entries).
3. If already processed or pure media with no surrounding unprocessed context: skip. Commit cursor and note "Dan Klishch — old media artifact (Jun 15), no action" in daily memory.
4. Do NOT update `last_contact` for the person based on a late-sync timestamp. Their `last_contact` reflects when they actually interacted, not when the media synced.

Session example (2026-06-21): Dan Klishch record appeared with timestamp `2026-06-15T03:07Z` in a Jun 21 intake. It was a `video.mp4` Vadim sent after confirming "Arriving in 5 min." Context from Jun 15 was a restaurant meetup — already a closed event. Skipped cleanly.

📋 `references/vladik-judgment-patterns.md` — Vladik covert check-ins revealed to target, over-communication toward founders.
📋 `references/office-access-request-triage.md`
📋 `references/credential-sharing-triage.md` — WiFi hotspot / device passcode / API token shared in TG: never log values, note exchange only, no task.
📋 `references/meeting-prep-pattern.md` — meeting prep, Nextcloud credential gap, unknown-contact stub.
📋 `references/additive-log-patterns.md` — reply-received-but-loop-still-open, pending-reply resolved, stale-thread short-closure (Ну да, бывает).
📋 `references/team-corrects-vadim-number-pattern.md` — teammates correct a Vadim-stated figure mid-thread: extend existing entry, add accuracy qualifier fact-key, no State update unless authoritative correction agreed.
📋 `references/cold-contact-triage.md` — unknown cold contacts (1 message, no history). Stub + identity_unresolved.
📋 `references/low-signal-personal-tg-patterns.md` — cold contact vs personal passive share. Sub-case 5: time-critical expiry → ⚠️ ACTION NEEDED; add `<doc>_expiry` State bullet; no Google Task for same-day expiry.
📋 `references/scheduling-loop-edge-cases.md` — wrong-timezone calendly, interview slot proposed→confirmed, social invite, counter-proposal loop.
📋 `references/same-day-multi-entry-insertion.md` — insertion point when note has multiple same-date Log entries; anchor ranking; new-entry vs extend.

### Broadcast-channel contacts: image/media-only posts = last_contact update only
📋 `references/broadcast-style-vs-broadcast-channel.md` — two-way contacts who also send broadcast-style intel shares; disambiguation rule before applying the fast path.

Some Telegram contacts (e.g. Vlad Zharoff) operate as broadcast channels — they post photos, film reviews, art projects, creative content, or news digests (`#новости`) to followers with no direct conversation thread. Recognition signals:
- Single image or media post with no text, or short thematic text with no ask
- Chat name includes descriptors like "фотограф", "artist", "проект", "канал"
- Prior log shows a pattern of one-way posts (photo batches, project updates)
- No `Vadims Casecnikovs:` reply lines in the recent history

**Triage rule:** broadcast posts are **always no-action**. The only write is updating `last_contact` in frontmatter + State bullet. Do NOT create tasks, proposals, or surface in heartbeat report unless the contact switches to direct message mode (i.e., a `Vadims Casecnikovs:` reply appears in context).

**Log entry shape for broadcast posts:**
```markdown
### YYYY-MM-DD — Broadcast <media type> post
- **src:** `vadimgest://telegram/<chat_id>_<msg_id>`
- **mentions:** [[Person]]
- **summary:** Posted N image(s)/video(s) at HH:MM UTC. No text / <brief text if present>. Continuation of <project name> content stream (prior: <last notable post>).
- **facts-touched:** last_contact
```

**Same-day double-burst:** When a broadcast contact posts twice in the same day and the first burst was already logged, **extend the existing Log entry** — update src to latest message ID, update summary to cover both bursts. Do NOT create two Log entries with the same date for broadcast-only contacts.

📋 `references/broadcast-checkinquestion-media-pattern.md` — "Спишь?" + immediate media = social framing for the share, not an open loop. Extend existing entry, no task.

### Personal contact tech/safety questions: no-action unless Vadim's reply is needed
Family and close personal contacts occasionally ask about AI tool safety, security, or tech decisions (e.g. "можно ли загружать зараженные файлы в Codex?"). Triage pattern:

1. **Check if the contact self-resolved.** If their second message says "не рискую" / "передумала" / "разберусь сама" — the question is closed. No task needed.
2. **Check the stakes.** A virus analysis curiosity question ≠ active incident. If they have a plan already (reinstall Monday, etc.) the situation is handled.
3. **Surface as optional reply suggestion only.** Vadim might want to briefly acknowledge the smart call. Do NOT create a Google Task — this is a 5-second WhatsApp/TG reply, not a deliverable.
4. **Log it in Obsidian** with `[PERSONAL stable]` marker — good to know mom is thinking about security, even if no action is required.

The answer to "can I upload virus-infected files to an AI assistant?": yes, text/code from an infected backup is generally safe to paste (the AI can't execute it), but uploading binary executables or running infected scripts on the same machine is not. The virus lives in the executable, not in static text you paste.

### Investor meeting debrief: personal contact "Как прошло?" open loop
When Vadim tells a personal contact he's heading to investor meetings ("Еду общаться с инвесторами") and then returns, the contact will often ask "Как прошло?" (how did it go?). This creates a soft open loop even when the prior heartbeat entry said "no action needed."

**Triage rule:** When the prior entry logged "heading to investors" as no-action, and a new intake message contains "Как прошло?" with no Vadim reply:
1. Extend the existing Log entry (do NOT create a new one) with the follow-up question and "Vadim has not replied yet."
2. Update `last_contact` src to the new message ID.
3. Do NOT create a Google Task — this is a personal conversation, not a deliverable.
4. Report in heartbeat summary as a soft open loop: "Signum/[contact] is waiting on investor meeting debrief."

**Signal phrases:** "Как прошло?" / "Ну как?" / "Расскажи" after an investor/business event mention.

Session example (2026-06-21 cycle 7): Signum asked "Как прошло?" at 17:51 UTC after Vadim had said "Еду общаться с инвесторами" at 15:13. Prior entry written as no-action; new message extended same entry with "Vadim has not replied yet."

### Meeting-time coordination signals
When a contact sends a time like "я где-то в 2-30 освобожусь" ("I'll be free around 2:30") in a chat where a meeting was previously arranged (e.g., Saturday lunch in daily memory, coffee confirmed in prior cycle) — this is an imminent meetup time signal, not casual chat.

**Triage rule:**
1. Cross-reference with daily memory for the prior arrangement (often from yesterday's heartbeat entry).
2. Parse the time in local context: if the contact is in SF and says "2:30", that's 2:30pm PDT = 21:30 UTC.
3. Add a `meeting_scheduled` State bullet to the person note: `<day date>, ~<time> local / <UTC> — <context> · src: <uri> · YYYY-MM-DD`
4. Extend the existing Log entry for the day (do not create a new entry just for this).
5. Update `last_contact` src to the latest message ID.

**Signal phrases:** "я буду в X", "освобожусь в X", "буду свободен/свободна в X", "встретимся в X?" when there's a prior meeting arrangement in context.

**Arrival/en-route phrases:** "Я через час буду" / "еду уже" / "буду через N минут" — these are not time proposals but arrival confirmations when a meeting was already scheduled. Update `office_visit` State bullet to note "en route" + update `last_contact`. No new task needed — meeting is already set. Extend the existing Log entry rather than creating a new one.

### Travel document forwarding = Vadim's own itinerary signal
When Vadim forwards I-94 printouts or flight change screenshots to a contact, it encodes his own travel plans. Parse `Admit Until Date` (hard visa deadline), update `vadim_departure_date` State bullet, supersede tentative stay-plan bullets. Full pattern: `references/travel-document-triage.md`.

### Location-share links signal an imminent in-person meeting
When a contact sends a `share.google/...` or `maps.app.goo.gl/...` link in Telegram with no other text, it almost always means: "here's where to meet me / come here." Context clue for triage:

- If prior messages in the same thread had "can we meet?" / "coffee?" / "see you?" → location link = "I'm here / meet here."
- Update the person's State with `meeting_scheduled` or extend the last Log summary.
- No new Log entry needed if it's clearly additive to an already-written thread.

Session example: Nur sent `https://share.google/hubiCpGKDjzjjnMbf` after confirming "Np! Sure" to Vadim's coffee offer → treated as meeting location → Log extended with "in-person meeting materializing."

### Vox deal research: non-Mercor/non-Catallax route cross-reference
When Vadim asks "which of these companies do we have a connection to *not through Mercor/Max/Mahir/Catallax*", the pattern is:

1. **Get the exclusion boundary first.** Check `Vox Lab/Deals/max + Mahir Bansal/max + Mahir Bansal — Data Brokerage.md` → `## State` for Catallax carve-outs. Check `schedule-c-vox-direct-carveouts-v1.md` for the formal exclusion list. Companies in those carve-outs are Vox-direct by definition.
2. **For each company, search Obsidian + vadimgest** for: named contacts, deal notes, meeting records, Signal/TG threads. A "plain mention" (e.g., product review, market map entry) does NOT count as a connection.
3. **Route categories:**
   - **Direct:** named contact + conversation record (e.g., Cohere via Josh Netto-Rosen, xAI via Harsh Gupta, Google DeepMind via Nikita Silakovs, OpenAI Sora via Alex Zhao)
   - **Via intermediary (non-Mercor):** Dima/Grably as channel (Luma, HeyGen, Moonvalley, ElevenLabs, Mistral, Microsoft, Amazon)
   - **Catallax/Mercor only:** explicitly tagged in Max+Mahir deal note or only appears in prospect lists
   - **No connection yet:** cold outbound sent but no reply, or only product mentions
4. **No Obsidian write needed** for pure research output — capture in daily memory and leave the Codex session artifact as the source.

Quant names (Bridgewater, Jane St, AQR, Renaissance, Two Sigma, Squarepoint, D.E. Shaw) historically have **no direct buyer contact** — only market map entries. Citadel is the exception.

### Frontmatter cache drift: update when State bullet contradicts it
When a new intake fact changes a field that is also in frontmatter (`company`, `role`, `location`, `last_contact`, `stage`, `next_action`, etc.), update **both** the State bullet and the frontmatter cache in the same write. Downstream tooling (status_collector, silence-detector, vox-crm) reads frontmatter, not State directly.

Common trigger: a contact's company or URL surfaces in a message that differs from what's in frontmatter (e.g., `company: "roam.lol"` in frontmatter but intake reveals `areality.co` as the actual current domain). Pattern:

```python
# Read the file
result = terminal("cat '/path/to/People/Person.md'")
content = result['output']

# Update frontmatter field (top of file, between --- delimiters)
content = content.replace('company: "roam.lol"', 'company: "areality.co"', 1)

# Also update the State bullet (if it exists) or add one
content = content.replace(
    '- **company_url:** roam.lol',
    '- **company_url:** areality.co (also roam.lol) · src: `tg://...` · YYYY-MM-DD',
    1
)
write_file('/path/to/People/Person.md', content)
```

**Pitfall from 2026-06-20:** added `company_url` State bullet for Toms (areality.co) but did not update `company: "roam.lol"` in frontmatter. The silence-detector will still read the old value. Fix: always update frontmatter in the same pass.

### Cross-writing: business events surfaced in personal chats
When a personal chat (Sasha, Vladik, Julia) contains a business development event (demo outcome, investor meeting, partnership signal), write to BOTH:
- The person's note (Log entry under the contact)
- The relevant project/research note (e.g. Caterpillar Study Log, deal note, Vox Lab/Deals/X)

Example: Sasha told Vadim that Alegria demoed to Butterfly Network and they liked it → Sasha Pokras note gets the conversation context; Caterpillar (Alegria) Study Log gets the business fact with BFLY stock context.

### Vadim-as-recruiter: friend-to-startup-job intros
Vadim actively introduces close friends into SF startup jobs (known instances: Vladislav Dombrovsky → roam.lol, Gleb Maksimov → areality.co). When this pattern fires, specific State bullets and a follow-up task type are needed.

**Sub-pattern: live CV/pitch coaching in Telegram**
Vadim sometimes coaches a candidate's pitch *in real-time over TG* — sending bullet-by-bullet CV content, framing advice, and strategy notes before or during the company call. Recognition signals:
- Vadim sends formatted bullet lists to the candidate (e.g. "Shelter 3.5M downloads...", "Three.js (!!) …", "Applied AI: …")
- Rapid short messages each adding a new CV section, sent within minutes of each other
- Candidate asks "Успеваем подготовиться?" / "what do I say about X?"

**Triage rule for these sessions:** all of Vadim's coaching bullets belong in a single Log entry (extended summary, not new entry per message). The candidate note's `job_opportunity` State bullet gets updated to `preparing` or `interview imminent`. Key pitch bullets should be captured in the Log summary so future sessions know what was said.

**cv_status State bullet update:** once Vadim drafts the full pitch, update `cv_status` to `pitch drafted by Vadim (TG coaching session YYYY-MM-DD)` — this distinguishes it from "AI-generated CV" (red flag) vs "Vadim-coached narrative" (strong signal).

**Signal phrases:**
- "Разрекламировал тебя" / "I hyped you up" → intro already made, the person is live in the hiring pipeline
- "Создал чат" → new TG group exists for the three-way coordination
- "Он готов купить билет и работать прямо сейчас" (or Vadim saying this on behalf of the friend) → commitment signal to the hiring company
- Vadim offering to do an "interview planning session" → he's personally coaching the friend

**State bullets to add on the friend's note:**
```markdown
- **job_opportunity:** <company> — Vadim intro'd, <status: CV rewrite / interview planning / offer pending> · src: `tg://<chat>/YYYY-MM-DD` · YYYY-MM-DD
- **cv_status:** <AI-generated (red flag) / rewriting manually / sent> · src: `tg://<chat>/YYYY-MM-DD` · YYYY-MM-DD  ← only if CV was discussed
```

**State bullet to add on the company contact's note (Toms, etc.):**
```markdown
- **hiring_candidate:** [[Friend Name]] — intro from Vadim, awaiting CV + availability confirmation · src: `tg://<chat>/YYYY-MM-DD` · YYYY-MM-DD
```

**Follow-up task to surface in heartbeat report:**
> "Interview planning session needed with [Friend] before CV is sent to [Company Contact]."

This is time-sensitive — Vadim promised the session; it should happen before the friend sends the CV to avoid a bad first impression.

**Hiring pipeline velocity tracking:** After the intro is made, watch for how fast the company responds. Signals:
- Company proposes a call within 24h of intro → `job_opportunity` State updated to "Toms proposed call <24h after intro" — strong positive velocity signal, surface in heartbeat report.
- Company goes silent for 48h+ → extend existing Log summary with silence note, do NOT create a new task (Vadim is the connector, not the applicant).
- State bullet format for fast-moving hires: `job_opportunity: <company> — Vadim intro'd, <company> proposed call <24h (<date/time>), <friend> preparing · src: ... · YYYY-MM-DD`.

**Founder-to-referrer complaint = candidate over-messaging signal.** When a founder (Toms, etc.) sends Vadim a short frustrated reaction about the candidate (e.g. "holy fucking yap / gleb") — this is the founder complaining to the referrer that the candidate is over-communicating or being too intense. Triage as:
1. **Surface immediately in heartbeat report** as ⚠️ signal (not buried in body).
2. **Extend the existing Log entry** on both the candidate note and the founder note — do NOT create a new Log entry for a 2-message reaction.
3. **Frame the action clearly:** Vadim needs to coach the candidate to dial back. Founders at fast-moving companies (Toms especially) respect action over words; candidate should let the founder move next rather than pushing.
4. **Do not create a Google Task** — this is a quick Vadim-to-friend coaching message, not a tracked deliverable.
5. **Do not update `job_opportunity` State bullet** unless the pipeline stage actually changed (e.g., call cancelled, offer withdrawn). A yapping complaint is friction, not a stage change.

**Sub-case: referrer defends the candidate back to the founder.**
When a subsequent message shows Vadim pushing back on the complaint ("He is good at game dev / three.js / did GTM for shelter") + asking what specifically triggered it ("What he said?") — this is active damage control. Extend the same Log entry (do NOT create a new one) on both the candidate note and the founder note. Key signals for this sub-case:
- Vadim lists the candidate's concrete skills to the founder (implies defending, not agreeing)
- Vadim asks "What did he say?" or equivalent — trying to learn the trigger
The `job_opportunity` State bullet still does not change until the stage actually changes. Note in the extended summary: "coaching conversation not yet visible in messages as of HH:MM UTC."

**Sub-case: founder escalates from yapping complaint to engineering disqualification.**
When the founder's reply shifts to a substantive engineering verdict ("0 indication he's a good eng somehow") — this is a category change. Update `job_opportunity` State to "disqualified; Vadim defending." Surface as a decision point: (a) accept the loss, or (b) push back with concrete portfolio evidence. Pattern: Cycle N = yap complaint, Cycle N+1 = engineering verdict, Cycle N+2 = root cause confirmed (candidate confesses to mutual contact). Do not collapse cycles — they have different action implications. Full arc details, Sasha post-meeting intel request pattern, and olympian talent pipeline context: `references/hiring-pipeline-arc-patterns.md`.

### Reading indirect speech for major facts
Vadim often communicates significant developments indirectly, especially in personal chats. Don't skim past first-person present-tense statements as casual chat — they may contain major deal/role changes.

Pattern to watch: **"I asked X to prepare Y"** or **"He's preparing a proposal for me to be Z"** — these are active deal signals, not hypotheticals. Log them as `[DEAL escalating]` or `[OPPORTUNITY new]` in State, not buried in summary prose.

Example: "I asked him to prepare terms next week and a proposal for me being COO next week. He believes in me, I don't know why. I believe brain writing is the coolest opportunity." → This is a COO offer being scoped, terms pending next week. Surfaces as a new `coo_proposal` State bullet immediately.

Other patterns: "they liked it" after a demo = positive outcome; "but she was convinced" = initial resistance overcome; "he/she believes in me" = equity/role discussion underway.

### Sasha Pokras as recurring talent pipeline: track "Getting X for tmrw" signals
Sasha regularly introduces high-quality recruits to Vadim's lab/gathering sessions. When Sasha says "Getting [X/him/her] for tmrw" or "I'll bring X" — this is a concrete recruit pipeline event, not casual conversation. Triage pattern:

1. **Identify the person.** If named: check/create Obsidian note. If unnamed ("insane hardware guy"): add a `sasha_recruit_pending` State bullet on Sasha's note with a description ("hardware engineer, attending Jun 22 gathering") until identity is revealed in a later cycle.
2. **Cross-reference with prior meeting context.** Sasha sometimes lines up people discussed in earlier meetings (e.g. Jun 20 Hlopya meeting surfaced a 16yo hardware engineer). Check recent daily memory before treating the unnamed person as brand new.
3. **Update the gathering note or create a named person note** when identity resolves. Use the `recruit_signal` State bullet pattern (see Recruit-candidate people notes section above).
4. **Track in daily memory** as "Sasha bringing [X] to [date/location] — identity [known/TBD]."

Recurring Sasha recruit signals (session log):
- Misha Bilokur: Stanford neuroscience PhD — Jun 20 intro, Sunday Jun 22 visit confirmed
- Andrii Holovach: observability founder, YC Sazabi — same Jun 22 Sunday
- Hardware engineer (16yo?): "Getting him for tmrw as well / Insane hardware guy imo" — Jun 21, same Jun 22 gathering

📋 `references/sasha-live-deal-coaching-pattern.md` — Sasha rapid-burst live coaching (⚠️ DEAL CRITICAL; no task; State bullet format; Jun 27 AWS credits example).

### Sasha post-meeting intel request pattern
Sasha regularly asks Vadim for debriefs after significant meetings. Recognition: "сообщи потом, как с [X] прошло" / "мб можно что-то соушл инженерить" / timing check. Triage: add `[[Sasha Pokras]]` to mentions in meeting-subject's Log entry. No Google Task — surface as reminder in report. Full examples: `references/hiring-pipeline-arc-patterns.md`.

### Fundraising strategy / raise narrative as a distinct State key
When Sasha (or another advisor) explicitly formulates a **raise timing and narrative** — not just "you should raise" but a specific sequence with investor framing — it warrants its own `fundraising_strategy` State bullet on the relevant person note, not just a Log summary.

Recognition signals:
- Advisor gives a multi-step sequenced plan: "First X happens, then you do Y, then on the wave of Z you raise"
- Investor framing is articulated: "they want to pre-empt / FOMO / best terms for friends"
- Vadim confirms: "Ты очень прав" / "exactly right" / "this is the plan"

**State bullet format:**
```markdown
- **fundraising_strategy:** <sequence in 1-2 lines>. <investor framing if given>. Strategy formulated by <advisor> <date> · src: `<uri>` · YYYY-MM-DD
```

This is distinct from:
- `coo_proposal` — a role offer being scoped
- `butterfly_demo` — a demo outcome
- `incorporation_advice` — legal/structural advice

The `fundraising_strategy` key captures the *narrative and timing* the team will use with investors. It belongs in State because future sessions need to know what story is being told, not just that "someone suggested raising."

**facts-touched:** update `fundraising_strategy` in the Log entry's `facts-touched:` line when this fires.

Session example (2026-06-21): Sasha formulated Allegria-announcement-anchored raise timing + Ilya pre-emption framing after NDA sender was confirmed. Added to Sasha Pokras State as `fundraising_strategy`.

**Sub-case: fundraising strategy advancing to active deal mechanics.** When the raise narrative transitions from "advisor advice" to "investor action" (e.g. the named investor calls and says they want in), write to BOTH the advisor's note (update `fundraising_strategy` bullet to reflect the real-time evolution) AND the investor's note (add `investor_interest` State bullet). Pattern:

1. **Advisor note:** update `fundraising_strategy` to reflect the new development — e.g. "strategy → fund investment confirmed, term sheet needed."
2. **Investor note:** add `investor_interest` State bullet: `wants to invest via fund / angel terms not yet offered — advisor recommends: get term sheet (even discounted) for optionality before raise starts · src: ... · YYYY-MM-DD`.
3. **Surface in heartbeat report** as actionable: "Get a term sheet from [Investor] before the raise opens — gives optionality."

This cross-write pattern fires whenever advice about an investor shifts from "here's what to do with Ilya" (on Sasha's note) to "Ilya called and is moving" (on Ilia's note). The event has two actors; both notes need the update.

### Self-evolve on codex-klava: server path overrides
📋 `references/self-evolve-server-paths.md` — Mac→server path override table, approved-tasks check pattern, python3 -c multiline restriction (use /tmp script files instead).

### Cron artifact cleanup / file retention: find -mtime pitfall
📋 `references/find-mtime-off-by-one.md` — `find -mtime +N` off-by-one: use `+(N-1)` to prune files older than N days. `-mtime +7` = ">8 full days", not ">7 days". Incident: backup cleanup silently skipped Jun 18 files for 8 days. Job `601e16617d4b` (evidence auto-close dry-run timeout) — known ongoing, skip in heartbeat reports.

### Cron health check: three-tier error classification
When reviewing cron job statuses in the health check, classify each `error` or anomaly into one of three tiers:

**Tier 1 — Known ongoing (silent skip):**
- Job `601e16617d4b` (Evidence auto-close, dry-run timeout) — always skip
- Any job where the same error has appeared in the last 2–3 daily memory entries with no change
- Do NOT surface in heartbeat report, do NOT create a task

**Tier 2 — Watch next run:**
- A job that shows `error` for the first time (or after a gap of successful runs)
- Note it in the heartbeat report as "watch next run" — no task yet
- If the same job shows `error` in two consecutive heartbeat cycles, promote to Tier 3
- Example: `856ab3e31a19` (Sales Mentor) — errored Jun 19, first sighting → "watch next run"

**Tier 3 — Escalate:**
- Same job `error` across 2+ consecutive heartbeat cycles
- Job that was previously `ok` and is now `error` AND directly affects Vadim's daily workflow (heartbeat, reflection, mentor, task consumer)
- Create a Google Task or surface prominently in report

**Never-run jobs (`last_status: None`, `last_run_at: None`):**
- Do NOT classify as errors. These are freshly-added jobs waiting for their first scheduled tick.
- Only note them if `next_run_at` is also `None` (scheduling gap — investigate) or if they should have already run by now based on schedule.
- Example: `e67d66896ba9` (English Coach Weekly Report, Monday 10:00) — `None` status is correct until first Monday fires.

**Klava system ping WARN vs jobs.json:** The Telegram ping reflects state at ping time; `jobs.json` is always more current. If `jobs.json` shows `ok` but the ping showed `WARN`, the job recovered after the ping — Tier 1, silent. See `references/cron-health-triage-patterns.md` for: transient script error investigation steps, ModuleNotFoundError dotenv diagnosis/fix, and the full Tier 1 always-skip list.

### 429 rate limit on anthropic jobs: scheduler gap behavior

When an LLM cron job fails with `HTTP 429: The usage limit has been reached`, the Hermes scheduler does NOT retry on the next scheduled tick. Instead it advances `next_run_at` by a full cycle. Example: self-evolve runs daily at 10:45; failed Jun 19; `next_run_at` was set to Jun **21** (skipped Jun 20 entirely). This is NOT a bug — it's the scheduler's retry-delay behavior after consecutive failures.

**What to do:**
- If the 429 was transient (single day, other jobs on same provider succeeded later), let it run on next scheduled tick. Do not force-trigger unless Vadim asks.
- If jobs are failing for multiple days, investigate: `hermes auth list` to see if `usage_limit_reached (429)` still shows with a reset time.
- For the openai-codex provider: the rate limit shows `(4d 23h left)` — this is the reset window, not fixable by retrying.
- For anthropic: a 429 on a paid API key means per-minute/per-hour rate limit was exceeded. Usually self-resolves. If persistent, check `ANTHROPIC_API_KEY` is valid via `hermes auth list`.

## Safety

📋 `references/org-note-cross-write-patterns.md` — org cross-write, HighTower escalation, inbox pre-check.
📋 `references/state-bullet-replacement-pitfalls.md` — silent no-op, artifact cleanup, long-description canonicalization.
- Do not send personal messages from Vadim's accounts. Draft only.
- Do not duplicate mutating cron actions during Hermes migration.
- Default operating mode after migration: **Hermes-first / Klava-dead-legacy cleanup on user request**.
  - Keep non-essential legacy Klava loops disabled or removed from Hermes scheduling when equivalent Hermes-native jobs exist.
  - Preserve failed runs as evidence in `/srv/codex-klava/data/hermes/cron/output/<job_id>/*` until superseded by a successful rerun.
- Do not kill or restart training, eval, or long-running compute processes.
- Do not disable or restart Klava system services without explicit direction and verification.

## Style

Be direct, specific, and English-first. Give Vadim concrete next actions, not generic reassurance.

### Heartbeat runbook behavior (klava-personal + Hermes)
- In scheduled runs, prefer direct single-run execution:
  - `hermes cron run ff50067ec588 --accept-hooks` for the Hermes heartbeat job.
  - Avoid `hermes cron tick --accept-hooks` as a one-shot fallback for this class of job; it may exceed CLI time limits in long-running or blocked environments and return timeout noise before the heartbeat job itself finishes.
  - In production, treat `hermes cron run ff50067ec588 --accept-hooks` as a scheduler nudge unless an artifact appears immediately.
  - Verify completion through `cron/jobs.json` (`last_status`, `last_run_at`, `next_run_at`) plus a fresh non-truncated artifact in `cron/output/ff50067ec588`.
  - If `cron tick` blocks, stop it and fall back to bounded polling of scheduler state/artifacts instead of waiting indefinitely.
- Intake gating:
  - If the heartbeat-style intake command returns `No new data since last checkpoint.`, treat it as an explicit no-op and finish as `HEARTBEAT_OK`.
  - When there are no new durable facts, do not force extra writes, commits, or side effects.
- Operational artifacts check before reporting:
  - confirm checkpoint/state progression (`/srv/codex-klava/data/vadimgest/state.json` + `checkpoints/*`),
  - confirm heartbeat state file has moved/contains result,
  - confirm queue/pending governance (empty queues vs backup migration event).
- **Output truncation guardrail (Hermes cron):**
  - If the latest `ff50067ec588` artifact contains `Response truncated` or `output length limit`, mark that run as **PARTIAL** and keep it as evidence.
  - Re-run once with a shorter report surface (smallest possible `---DELTAS---` payload and concise `HEARTBEAT_OK`).
  - Do not infer success from the old artifact if it ended in truncation.
  - For implementation details, see `references/heartbeats/hermes-heartbeat-runtime-notes.md` and `references/heartbeats/heartbeat-scheduler-execution-guardrails.md`.
  - After any re-run, confirm `cron/jobs.json` `last_status` is `ok` and the latest artifact is no longer truncated before reporting PASS.

### Conversation posture for this user
- If Vadim says "be more proactive" or "research my needs," switch to **proactive + action-first** mode: do the most likely next 1–3 steps from live state in one pass, then report.
- Avoid over-formatting with abstract prose when an immediate next action is available; prefer direct operational output.
- Keep responses crisp by default; if deeper analysis is needed, separate it explicitly as:
  - `Quick answer` (2–4 lines)
  - `Why this now` (short rationale)
- If a workflow requires multiple tools, execute them now and report results; only ask for clarity when ambiguity changes which tool/plan to use.
- In automation/cron tasks, prefer **validate → fix → rerun → verify** cycle and report state, not narratives.

When Vadim explicitly asks for proactive context research, return:
1) top 3 active priorities from working set / daily memory,
2) what is blocking them right now,
3) a single recommended next action.

Reference for recent automation hardening patterns:
- `references/heartbeats/hermes-heartbeat-runtime-notes.md`
- `references/heartbeats/hermes-cron-output-truncation-runbook.md`
- `references/hermes-provider-auth-state.md` — provider credential inventory, 429 diagnosis, OAuth wiring status
