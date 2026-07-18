---
name: kronos-collect
disable-model-invocation: true
description: "Kronos — generates your daily timesheet by collecting work activity from GitHub commits/PRs, Slack messages, Slack DMs, Slack huddles, Google Calendar, Zoom meetings, and Google Drive, then posts a review summary to your Slack DM. Invoke this skill whenever the user says: generate timesheet, generate timesheet for [date], timesheet for [date], what did I work on today, what did I work on yesterday, collect my work activity, summarize my work day, create timesheet summary, /kronos-collect. Do not use generic Claude behavior for these requests — always load this skill."
---

Collect yesterday's work activity from GitHub, Slack, Google Calendar, Zoom, and Google Drive, then post a summary to the user via Slack DM for review. If today is Monday, collect the previous Friday's (last day of the week) work activity.

---

## Arguments

An optional date string may be passed, e.g. "yesterday", "April 18", "2026-04-18", "last Friday".
Accepted formats: natural language ("yesterday", "last Friday"), month + day ("April 18", "Apr 18"), or ISO date ("2026-04-18").
When only a month and day are given with no year, assume the current year.
If no argument is provided, generate the summary for the most recently completed work day (yesterday, or Friday if today is Monday).

---

## Instructions

### Step 1 — Bootstrap

1. Resolve the **memory path** — check in this order and use the first that exists:
   - `~/.claude/plugins/marketplaces/local-desktop-app-uploads/kronos/memory.md`
   - `./memory.md`
   - If neither exists: run `/kronos-setup` first, then resume here.
     Use this resolved path for all reads and writes throughout this skill run.
2. Read `memory.md` in full from the resolved path. All configuration (GitHub username, ERP URL, mappings, etc.) lives there.
   - If the file is empty, run `/kronos-setup` first, then resume here.
   - If `memory.md` is invalid, try to fix it — if you can't, stop and reply: `Error: memory.md is invalid. Please run /kronos-setup to reconfigure.`
   - Validate that the following fields are non-empty: `Slack User ID`, `ERP URL`, `GitHub Org`. If any are missing, stop and reply: `Setup incomplete — the following fields are missing from memory.md: [list]. Please run /kronos-setup to fill them in.`
3. Verify **connected tools** — check each required connector is available:
   - **GitHub MCP**: if unavailable, stop and reply: `Cannot proceed: GitHub MCP is unavailable. Please configure it in claude_desktop_config.json and re-run.`
   - **Slack MCP**: if unavailable, stop and reply: `Cannot proceed: Slack MCP is unavailable. Please connect the Slack connector in Claude settings and re-run.`
   - **Google Calendar MCP**: if unavailable, skip — no calendar events will be collected
   - **Google Drive MCP**: if unavailable, skip Drive activity collection
   - **Zoom MCP**: if unavailable, skip Zoom enrichment and note it in the summary
4. Resolve the **target date range**:
   - Read `Day Boundary` from `memory.md` (e.g. "11:00 AM") and `Timezone` (e.g. "Asia/Kolkata"). The window is always 24 hours: that time on the target day → that same time the next calendar day, interpreted in the configured timezone (accounting for DST at the target date).
   - Default target day: the **previous working day**
      - If today is Monday, previous working day = Friday (3 calendar days ago)
      - Otherwise, previous working day = yesterday
   - If a date argument was passed, use it as the target day.
   - If `Day Boundary` is missing from `memory.md`, default to 11:00 AM.
5. Derive the **display date** (the day the work counts toward) as the start date of that window.
6. If **no date argument was passed** and today falls on **Saturday or Sunday**, stop and reply: `Skipping: today is a weekend.`

---

### Step 2 — Check if timesheet is already complete

Use Claude in Chrome to open the ERP URL from `memory.md`.
If the ERP page fails to load (not logged in, unreachable, etc.), stop and reply:
`Cannot reach ERP. Please open Chrome, log in to [ERP URL], and re-run.`
Verify the logged-in employee matches `ERP Employee Name` from `memory.md` (check the name shown in the ERP UI). If it does not match, stop and reply: `⚠️ ERP employee name mismatch — logged in as "[actual]" but memory.md has "[expected]". Please log in as the correct user, then re-run /kronos-collect [date].`
Navigate to the week containing the display date.
Sum all logged hours for that day.
Read `Daily Hours Target` from `memory.md` (default: 8:00 if missing).
If the total **exceeds the target by more than 30 minutes**, stop and reply:
`Timesheet already complete for [display date] (X:XX hrs logged). Nothing to do.`

---

### Step 3 — Fetch Calendar events

If Google Calendar MCP is unavailable (as noted in Step 1), skip to Step 3b with an empty calendar event list.

Use the Google Calendar MCP to list events for the display date.

If multiple events on this day share the same title, append their start time in parentheses to each — 12-hour format, no leading zero, uppercase AM/PM (e.g. "Weekly Sync (10:00 AM)", "Weekly Sync (3:00 PM)"). Convert each event's start time to the user's configured `Timezone` for this suffix; if `Timezone` is empty, read the timezone directly from the Calendar event's own timezone field in the API response. This deduplication applies regardless of whether the Zoom MCP is available.

Then proceed to Step 3b to cross-reference these calendar events with Zoom.

---

### Step 3b — Cross-reference Zoom meetings

1. If the **Zoom MCP is unavailable**, skip this step entirely and note "⚠️ Zoom connector unavailable — meeting attendees and Zoom AI summaries not available" in the summary.
2. Read `Timezone` from `memory.md` (required by the Zoom MCP — e.g. `"Asia/Kolkata"`). If `Timezone` is empty, skip this step entirely and note `⚠️ Zoom enrichment skipped — Timezone is not configured in memory.md. Add it by running /kronos-setup.` in the summary.
3. Call `search_meetings` with the target date window (converted to UTC) to retrieve all Zoom meetings for the day.
4. **Match Calendar events → Zoom meetings:**
   - For each Google Calendar event from Step 3, use the event title as already stored (with any start-time suffix already applied by Step 3's dedup rule).
   - Inspect the event description/body for a Zoom meeting URL (e.g. `zoom.us/j/NNNNNNNNNN` or `zoom.us/w/NNNNNNNNNN`). If multiple Zoom URLs are present in the description, use the first one found.
   - Extract the numeric meeting ID from the URL: take the digit sequence immediately after `/j/` or `/w/`, stopping at `?`, `&`, `/`, or end of string (ignore any conftoken or password suffix)
   - Find the matching Zoom search result by comparing the extracted number against `meeting_number`
   - If no Zoom URL is found in the description, or if no `meeting_number` match is found in the Zoom results, or if the matched Zoom result is missing a `meeting_uuid` field, treat the Calendar event as a Calendar-only meeting (no Zoom enrichment) and continue
   - If a match is found: use the `meeting_uuid` field from that Zoom search result to call `get_meeting_assets(meeting_uuid)` and retrieve `participants` and `meeting_summary`. If the call fails (network error, deleted meeting, permissions issue, etc.), log a warning and continue with participants and meeting_summary as unavailable — do not stop the run.
   - Store: `{ calendar_event_title, zoom_uuid, participants: [...], zoom_ai_summary: "..." }`
5. **Handle Zoom-only meetings** (Zoom results with no matching Calendar event):
   - Treat each as a new time block. Use the meeting `topic` as the task name; if multiple Zoom meetings share the same topic on the same day, append the start time in parentheses to make each entry uniquely addressable. Convert `schedule_start_time` from UTC to the user's configured `Timezone` for this suffix; if `Timezone` is empty, `schedule_start_time` is already in UTC so display the suffix in UTC (e.g. "Daily Standup (9:00 AM UTC)"). Format the time in 12-hour format with no leading zero on the hour and uppercase AM/PM (e.g. `9:00 AM` not `09:00 AM`; `12:30 PM` not `12:30 pm`) → "Daily Standup (9:00 AM)"
   - Use the `meeting_uuid` field from the Zoom search result to call `get_meeting_assets(meeting_uuid)` for participants + AI summary. If `meeting_uuid` is missing from a result, skip the `get_meeting_assets` call and note participants as unavailable
   - Use `schedule_start_time` + `duration` from the Zoom search result as the time block window
6. Store all enriched meeting data for use in Steps 7, 8, and 9.

---

### Step 4 — Collect GitHub activity

Use the GitHub MCP. Fetch all of the following for the configured GitHub username within the target time window:

- **Commits** authored (across all repos in the configured org)
- **Pull request** reviews, approvals, and comments
- **Issue comments** posted
- **Issues** opened or updated

Group results by **repository**, then by **issue** (link commits to issues via `#number` references in commit messages or branch names like `issue-123-description`).

For each issue worked on, note:
- Issue title, number, URL
- List of commits with timestamps
- PR/review activity with timestamps

If an issue cannot be determined from a commit, keep the commit grouped under the repo with title "Unlinked commits".

If the GitHub MCP is connected but returns **zero activity** for the configured username and org, add a warning to the summary: `⚠️ No GitHub activity found — verify your GitHub Username and Org in memory.md.`

If a GitHub rate limit error is returned at any point during collection, wait 60 seconds and retry that request once. If still rate-limited, continue with whatever data has been collected so far and note "⚠️ GitHub data may be incomplete — rate limited during collection" in the summary.

---

### Step 5 — Collect Slack activity

Use the Slack MCP `slack_search_public_and_private` tool to collect all messages sent by the user during the target time window.

**Search parameters:**
- `query`: `from:<@{Slack User ID}>` — substitute the actual User ID from `memory.md` (e.g. `from:<@U0123ABCDEF>`)
- `after`: window start as Unix timestamp
- `before`: window end as Unix timestamp
- `channel_types`: `public_channel,private_channel,mpim,im`
- `sort`: `timestamp`, `sort_dir`: `asc`
- `limit`: `20` (maximum per page)
- `include_bots`: `false`

**Pagination:** after each response, check for a returned `cursor` value. If present, repeat the same call with `cursor` set to that value to fetch the next page. Continue until no `cursor` is returned. This fully exhausts all messages sent by the user regardless of workspace size.

**Thread replies:** for each result whose `thread_ts` differs from its own `ts` (i.e. it is a reply inside a thread), use `slack_read_thread` with `channel_id` and `message_ts` = `thread_ts` to fetch the full thread context. Bound the thread read with `oldest` and `latest` matching the target window. Paginate `slack_read_thread` with `cursor` if a next cursor is returned (limit 100 per page).

**Rate-limit handling:** if any call returns a rate-limit error, wait 60 seconds and retry. After 3 retries on the same call, continue with results collected so far and note `⚠️ Slack data may be incomplete — rate limited after [N] messages` in the summary.

**Channel messages:** group by **thread** (parent message URL). Standalone messages not part of any thread are each their own single-message group. For each thread, note:
- Channel name
- Thread URL (link to first message)
- Summary of what was discussed (1–2 sentences)
- Timestamps of user's messages in that thread

**DM messages** (results from `im` and `mpim` channel types): group by **DM conversation + thread** the same way channel messages are grouped. For each DM thread, note:
- Participant(s) (e.g. "DM with @teammate")
- Thread URL (link to first message)
- Summary of what was discussed (1–2 sentences)
- Timestamps of user's messages in that thread
- Mark each DM thread with `source: "slack_dm"` for use in Steps 7 and 10

**Record active channel/DM IDs** from all Step 5 results — these are needed by Step 5b for huddle detection.

---

### Step 5b — Collect Slack Huddles

For each active channel/DM ID recorded in Step 5, use `slack_read_channel` with `oldest` and `latest` set to the target window's Unix timestamps and `limit` 100 per call. Paginate with `cursor` until exhausted. Scan the returned messages for entries with `subtype: "call_started"` or `subtype: "call_ended"`. Apply the same rate-limit handling as Step 5 (wait 60 s, up to 3 retries per call). This scopes huddle detection to channels where the user was already active, avoiding blind enumeration of the full workspace.

For each matched huddle:
1. **Duration**: compute `call_ended.timestamp − call_started.timestamp`. If a `call_ended` event is missing (huddle still active or event lost), **default the duration to 30 minutes** and note `⚠️ Huddle duration estimated at 0:30 — call_ended event not found` in the summary. Do not skip the huddle entry.
2. **Context**: read the 10 messages immediately before and after the `call_started` event in the same channel or DM. Use these as context for summary generation in Step 9.
3. **Location**: determine whether the huddle occurred in a **channel** or a **DM**:
   - Channel huddle: record the channel name
   - DM huddle: record the participant(s) (e.g. "DM with @teammate")
4. **Mark** each huddle with `source: "slack_huddle"`, its location type (`channel` or `dm`), duration, and the collected context messages.
5. Store all huddle data for use in Steps 7, 8, and 9.

---

### Step 6 — Collect Google Drive activity

Use the Google Drive MCP `search_files` tool with the following query to find files **you personally opened or edited** during the target time window (convert the window boundaries to UTC ISO 8601 before substituting):

```
viewedByMeTime >= '[window_start_utc]' and viewedByMeTime <= '[window_end_utc]'
```

Do **not** use `list_recent_files` — its default `recency` sort returns files modified by anyone (teammates, automations, etc.), not only by you.

For each file returned, note: name, file type (Doc/Sheet/Slide), and the `viewedByMeTime` value (use this as the activity timestamp, not `modifiedTime`).
Group by project if the file name or parent folder matches a known project from `memory.md`.

After completing Steps 3, 3b, 4, 5, 5b, and 6: if **zero activity** was found across all sources (no Calendar events, no Zoom meetings, no GitHub events, no Slack messages, no Slack DMs, no Slack huddles, no Drive files), send a Slack DM to the user: `No activity detected for [display date]. If this is correct, no timesheet is needed. If you worked offline or did work not tracked in these tools, skip this and file manually using /kronos-file [date]. Otherwise, check that your GitHub Username, GitHub Org, and Slack Workspace are set correctly in memory.md, then re-run.` Then stop.

---

### Step 7 — Map activity to ERP projects and tasks

For each item of activity collected, determine:

**ERP Project:**
- Look up the GitHub repo in the `GitHub Repo → ERP Project Mappings` table in `memory.md`
- For Slack **channel** threads with no GitHub issue, look up the Slack channel in the `Slack Channel → GitHub Repo Mappings` table, then resolve to ERP project. If the channel is found in the table but the resolved repo has no entry in `GitHub Repo → ERP Project Mappings`, do **not** silently fall through to `📁 Other` — add an inline warning to the summary: `⚠️ #[channel] maps to [repo] but [repo] has no ERP project mapping — entry placed under 📁 Other. Fix with: /kronos-remember [repo] → ERP Project Name`
- For Slack **DM** threads (`source: "slack_dm"`): infer the ERP project from the thread content using AI (look for repo names, project names, issue references, or task descriptions in the messages). If a project can be confidently inferred, map it to the corresponding ERP project via `GitHub Repo → ERP Project Mappings`. If no project can be inferred, place under `📁 Other`.
- For Slack **channel huddles** (`source: "slack_huddle"`, location: `channel`): look up the huddle's channel in `Slack Channel → GitHub Repo Mappings`, then resolve to ERP project. Same warning rule as channel messages if the chain is broken.
- For Slack **DM huddles** (`source: "slack_huddle"`, location: `dm`): infer the ERP project from the context messages around the huddle using AI. If no project can be inferred, place under `📁 Other`.
- For Google Drive files: check if the **file name or its immediate parent folder name** contains any known ERP project name or repo name from `memory.md` (case-insensitive substring match). For repo names, match against the **repo portion only** (the part after the `/` — e.g. match `acme` from `your-org/acme`, not the full `your-org/acme` string, since filenames cannot contain slashes). If multiple projects match, use the one whose matched text (the repo name portion or ERP project name that was found in the filename) is longest. If no match, add to the unknown-mappings list (Step 10)
- For all meeting entries (Calendar or Zoom-only): extract a project hint from the meeting title (e.g. "Alpha Sprint Planning" → "Alpha", "Acme Weekly Sync" → "Acme"). Search the configured `GitHub Org` for a repository whose name closely matches the extracted hint. Look up the found repo in `GitHub Repo → ERP Project Mappings` to get the ERP project name. If no matching repo is found, or if the found repo has no ERP project mapping, add to the unknown-mappings list: ask the user which repo in the `GitHub Org` this meeting belongs to, and to provide the answer using `Map: org/repo → ERP Project Name`

**ERP Task:**
- The ERP task name is the **GitHub issue title** (exact match)
- For all meeting entries (Calendar or Zoom-only): search GitHub issues in the resolved repo for titles containing "standup", "sync-up", or "miscellaneous" (in that order of preference). **Use the found GitHub issue title as the task name in the summary** — this is what Phase 2 will type into the ERP Tasks field directly. If multiple meeting entries of any type resolve to the same GitHub issue title, append their start time suffix to each (e.g. "Standup and Sync-ups (9:00 AM)"). If no matching GitHub issue is found, fall back to the meeting title as the task name.

**Learned Facts correction pass (applies to all entry types):**
After resolving the initial ERP task name for every entry — GitHub tasks, meeting entries, Slack threads, Drive files, huddles — scan the `Learned Facts & Notes` section of `memory.md` for any entry that references the resolved task name (case-insensitive) and contains a recognisable correction pattern (e.g. `correct ERP task for "X" is "Y"`, `ERP task for "X" under [Project] is "Y"`). If a match is found, replace the task name with the value stated in the fact before building the Slack summary. This pass runs once over all entries after Step 7 is otherwise complete, ensuring that any user-saved correction is applied uniformly regardless of the entry's data source.

**Unknown mappings:**
- Collect all unmapped items (repos, channels, files with no project match)
- Do NOT ask the user mid-run. Accumulate them and ask in the Slack DM summary at the end (Step 10)

---

### Step 8 — Estimate time per task

All tasks are calculated **independently and additively** — overlapping entries each receive their full time estimate. The user may work on multiple things simultaneously, so the total can legitimately exceed the daily target; no proportional splitting is applied between tasks.

1. **Normalize all timestamps** to the user's configured `Timezone` from `memory.md` before any further processing. GitHub, Slack, Drive, and Zoom all return UTC or Unix timestamps — convert each to the user's local timezone so that all further calculations are in the user's wall-clock time.

2. **Anchor the first task to Day Boundary:**
   - From all activity-based tasks (GitHub/Slack/Drive) — excluding meetings — find the task(s) whose first event timestamp is the earliest across the day.
   - For each such task (all ties included), set its effective segment start to the `Day Boundary` time from `memory.md`, regardless of how far the first event falls after Day Boundary.
   - Meetings (Calendar, Zoom-only, Slack Huddles) are excluded from this pool entirely — they keep their exact durations.

3. **Mechanical pass (floor):** For each activity-based task independently:
   - Build the task's own activity timeline from its events (commits, Slack messages, Drive edits), using the Day Boundary-adjusted start for any first-task anchored in step 2.
   - Group consecutive events within 30 minutes of each other into work segments. A segment may span calendar midnight — two events at 11:55 PM and 12:10 AM are 15 minutes apart and form one segment.
   - Task time = sum of all segment durations for that task.
   - This mechanical result is the **floor** — the AI pass in the next step can only increase it, never decrease it.

4. **AI holistic pass:** Lay out a complete chronological timeline of all events across all tasks and meetings for the day. Using this full-day context, reason about how long the user likely spent on each activity-based task:
   - Consider the gaps between tasks, surrounding meeting blocks, and the overall shape of the day.
   - For the last task of the day, factor in any trailing time after its last event that was not consumed by a subsequent task or meeting.
   - For each task, if the holistic estimate exceeds the mechanical floor, use the holistic estimate. If it is equal to or below the floor, keep the floor.

5. **Round** each activity-based task's final estimated time **up to the next 30-minute boundary** (ceiling rounding). Examples: 0:01 → 0:30, 0:30 → 0:30, 0:31 → 1:00, 1:01 → 1:30, 1:30 → 1:30, 1:31 → 2:00. This means every activity-based task with at least one event is a minimum of 0:30.

6. For each **meeting entry** (Calendar, Zoom-only, or Slack Huddle): use the known duration directly — Calendar event end minus start, Zoom `schedule_start_time` + `duration`, or huddle `call_ended − call_started`. Meeting entries are not rounded. The user can adjust times in their Slack reply before filing.

7. Read `Daily Hours Target` from `memory.md` (default: 8:00 if missing). If the total estimated time is more than 30 minutes **below** the target, note the discrepancy in the summary but do not force-adjust — let the user correct it. Totals exceeding the target are normal on parallel-work days and should not be flagged. (Note: Phase 1 uses a 30-minute below-target threshold as an early heads-up during review. Phase 2 uses a 1-hour threshold in either direction as a final warning before committing to ERP — this difference is intentional.)

---

### Step 9 — Generate AI summary per task

For each task, write a 2–4 sentence progress summary using:
- Commit messages for that issue
- Slack thread content related to that issue
- PR descriptions or review comments

For **meeting entries** (Calendar events matched to Zoom, or Zoom-only meetings):
- Use the Zoom `meeting_summary` (AI-generated) as the primary context if available
- Weave attendee names naturally into the summary sentence (e.g. "Attended sprint planning with Alice, Bob, and 3 others — discussed unblock strategy for the CAD Downloads block...")
- If no Zoom summary is available, generate from the Calendar event title and any Slack messages around the same time

For **Slack Huddle entries**:
- Use the context messages collected in Step 5b (the 10 messages before and after `call_started`) to infer what the huddle was about and generate a 2–4 sentence summary
- Weave participant names naturally if identifiable from the DM or channel members
- If the context messages are insufficient to generate a meaningful summary (e.g. no messages around the huddle, or only unrelated messages), flag this huddle in the Slack DM summary with: `⚠️ Could not infer huddle summary for [channel/DM with @user] ([duration]) — please reply with a brief description of what was discussed`

Write in first person past tense (e.g. "Implemented the CAD Downloads block and fixed a rendering bug in the editor...").

---

### Step 10 — Build and send Slack DM

Format the summary as a Slack message using mrkdwn. Group entries by **ERP project name**. The header for each group is the ERP project name in bold, with the GitHub repo linked in parentheses. Tasks with no resolved ERP project go under `📁 Other`.

**Slack mrkdwn formatting rules:**
- Do **not** use `---` as a section divider — Slack does not render it as a horizontal rule; it appears as literal dashes. Use a blank line between sections instead.

**Grouping rules:**
- GitHub entries: look up the repo in `GitHub Repo → ERP Project Mappings` → use that ERP project as the group header
- Meeting entries (Calendar or Zoom-only) with a resolved ERP project: group under that ERP project header
- Any entry whose project cannot be resolved: goes under `📁 Other`

**GitHub link rules per task:**
- PR that links to an issue → use the issue URL as the task link; list PR URL(s) in the summary line
- Multiple PRs linking to the same issue → merge into one entry, combine time, list all PR URLs in summary
- PR with no linked issue → use the PR URL as the task link
- Commits not tied to any PR or issue → one entry titled "Unlinked commits" linked to the repo URL

Always use full hyperlinks — never bare numbers like `#222` or `PR #1303`. For **task links** (issues, PRs used as the main entry link), use standard markdown format `[text](url)`. For **PR references in the "PRs:" sub-bullet line**, always use the full URL without any markdown link text (e.g. `https://github.com/org/repo/pull/1296`), so that Phase 2 can extract the URL from plain Slack text without ambiguity.

**Meeting link rules per task:**
- Calendar meeting (with or without a Zoom match): no hyperlink — display the task name followed by `_(Google Calendar)_`
- Zoom-only meeting: search Slack for a message containing the Zoom meeting URL and use it as the task link. If no Slack message is found, display the title with no link
- Slack Huddle: no hyperlink — display the task name followed by `_(Slack Huddle)_`
- Slack DM thread: use the thread URL as the task link if available; display the participant(s) as context (e.g. `_(DM with @teammate)_`)

```
📋 **Kronos Summary — [Display Date]**
Total estimated: X:XX hrs

**Alpha Project** ([your-org/alpha](https://github.com/your-org/alpha))
  • [CAD Downloads block in Accordion](https://github.com/your-org/alpha/issues/222) (1:30)
    • Developed and raised PR to support CAD Downloads inside Accordion block.
    • PRs: https://github.com/your-org/alpha/pull/1296, https://github.com/your-org/alpha/pull/1308
  • [PR code review — Products Block](https://github.com/your-org/alpha/pull/1303) (0:30)
    • Reviewed and approved with a minor comment. Coordinated merge with teammate.

**Acme Corp** ([your-org/acme](https://github.com/your-org/acme))
  • [GH-2107: BlogPosting schema + PR reviews](https://github.com/your-org/acme/issues/2107) (1:00)
    • Coordinated PRs for BlogPosting schema.
    • PRs: https://github.com/your-org/acme/pull/2383, https://github.com/your-org/acme/pull/2389
  • Standup and Sync-ups _(Google Calendar)_ (1:00)
    • Attended the monthly engineering meetup with Alice, Bob, and 8 others.

**📁 Other**
  • [Some unmapped task](https://github.com/...) (0:30)
    • Short description.

⚠️ **Unknown mappings (please reply with the correct project/task):**
- `your-org/some-repo` — which ERP project does this belong to?
- `#some-channel` — which GitHub repo does this channel map to?
- Meeting "Ad-hoc Sync" — which repo in [GitHub Org] does this belong to?
Reply using the format (you can include multiple lines in a single reply):
  `Map: your-org/some-repo → ERP Project Name`
  `Map: #channel → your-org/repo-name`


To correct entries, reply using the task name:
  • `CAD Downloads block in Accordion: change time to 2:00`
  • `CAD Downloads block in Accordion: task is #223`
  • `Add: Task name :: ERP Project :: 0:30 :: Summary`  _(fields separated by ` :: `; do not use `::` inside any field)_

If two entries share the same task name, disambiguate with the ERP project in parentheses:
  • `Code Review (Alpha Project): change time to 1:00`

For meeting entries with the same topic (disambiguated by start time), use the full task name including the suffix:
  • `Standup and Sync-ups (9:00 AM): change time to 0:30`

Then run `/kronos-file [Display Date]` in Claude Code to file.

_You cannot trigger Phase 2 from Slack — it must be started from your Claude client._
```

Use the Slack MCP to send this as a **direct message to the user** using the `Slack User ID` from `memory.md`.

**Message length:** if the full summary exceeds ~3,500 characters, split it across multiple messages in the same DM thread: send the header + first ERP project group as the initial message, then post each remaining ERP project group (including `📁 Other` and the unknown-mappings block) as sequential thread replies. Phase 2 reads all messages in the thread, so splitting does not affect filing.

---

### Step 11 — Mapping answers are handled by Phase 2

If the user replies to this DM thread with mapping answers, Phase 2 will read them, save them to `memory.md`, and apply them during filing. No action needed here. Multiple `Map:` lines in a single reply are all processed. Supported formats:
- `Map: your-org/some-repo → ERP Project Name` → saved to `GitHub Repo → ERP Project Mappings`
- `Map: #channel → your-org/repo-name` → saved to `Slack Channel → GitHub Repo Mappings`

---

## Error handling

- If GitHub MCP is unavailable, stop — it is required (see Step 1)
- If Google Calendar, Google Drive, or Zoom MCP is unavailable, skip that data source, note it in the summary, and continue
- If Slack MCP is unavailable, stop — it is required (see Step 1)
- If GitHub rate limit is hit, collect what is available and note "GitHub data may be incomplete"
- If no activity is found at all, see Step 6 for the handling and stop message
- Always read `memory.md` before asking the user anything — the answer may already be stored there
