---
name: sync-prep
description: Generate a sync prep briefing by analyzing a Jira board for anti-patterns. Works with Scrum sprints and Kanban boards. Use this skill whenever the user mentions sync prep, sprint health, sprint analysis, kanban review, board health, flow metrics, daily sync briefing, iteration review, team sync, or wants to review their Jira board before a team meeting — even if they don't say "sync prep" explicitly.
---

# Sync Prep Generator

Your job is to analyze a team's Jira board (Scrum or Kanban), detect anti-patterns, and generate a concise sync prep briefing that helps the team run an effective daily sync.

## Step 0: Verify Jira Connection

Before asking the user anything, check whether you have access to Jira tools. This skill requires a Jira integration — either a **Jira MCP server** (in Claude Code) or a **Jira connector/integration** (on Claude.ai).

**How to check:**
1. Look at your available tools for anything Jira-related (e.g., `jira_list_boards`, `jira_search`, `jira_get_sprint`, `list_boards`, or similar)
2. If you find Jira tools: proceed to Step 1
3. If you do NOT find Jira tools: **stop here** and tell the user:
   - In **Claude Code**: "I don't have a Jira MCP server connected. You'll need to add one (e.g., Atlassian MCP) to your MCP configuration before I can analyze your board."
   - On **Claude.ai**: "I don't see a Jira integration connected. You can add one from Settings → Integrations → Jira."
   - Provide a brief setup pointer and ask them to reconnect once it's configured. Do NOT ask for a board or project — there's nothing you can do without the connection.

Optionally, also check for **GitHub access**. The agent can use GitHub in three ways (check in this order):
1. **GitHub MCP tools** — look for tools with "github", "pull_request", "pr", or "commit" in the name
2. **`gh` CLI** — in Claude Code, run `gh auth status` to check if the GitHub CLI is authenticated. If it is, you can use `gh pr list`, `gh api`, etc. for all GitHub rules.
3. **Claude.ai GitHub connector** — this only provides file access, NOT API tools. It cannot search PRs or commits.

If either option 1 or 2 is available, 3 additional rules (PR checks, done-not-merged, unlinked commits) will run. If neither is available, those rules are skipped gracefully — mention this to the user so they know what they're getting.

## Jira API Safety: Pagination and Search

Jira instances in real companies can be massive — 1000+ projects, hundreds of boards, sprints with 200+ issues (especially with subtasks). Every Jira list operation in this skill must follow these rules:

1. **Never assume a list fits in one page.** Always check if the response has more results (`total > startAt + maxResults`, or a `nextPage` token) and keep fetching until complete.
2. **Prefer search/filter over list-all.** When looking for a board or project, use name or key filters rather than listing everything. For example, filter boards by project key or name substring instead of fetching all 500 boards and scanning locally.
3. **Cap `maxResults` appropriately.** Use 50 for sprint issues, 20 for backlog queries, 10 for board/project discovery. Only increase if you need all results (like sprint issues).
4. **Paginate in parallel when possible.** If the first page tells you `total = 180` and your page size is 50, you can fetch pages 2, 3, 4 in parallel (`startAt=50`, `startAt=100`, `startAt=150`).

These patterns apply to every Jira MCP call in this skill — board listing, sprint fetching, issue queries, and backlog scans.

## Step 1: Find the Board and Determine Mode

Only proceed here after confirming Jira tools are available in Step 0.

Ask the user which Jira board or project to analyze. They might give you:
- A **project key** (e.g., "AUTH", "PLAT-") — search boards filtered by that project
- A **board name** (e.g., "Platform Team Board") — search boards by name
- A **board ID** (e.g., "42") — use it directly
- Something vague (e.g., "my board", "the backend project") — ask them for a project key or board name to narrow the search. Do NOT list all boards — large orgs can have hundreds.

### Board Discovery

Before detecting the board type, **resolve to a specific board first**. A single project can have multiple boards (e.g., one Scrum, one Kanban).

1. Search boards filtered by the user's project key or board name.
2. **If exactly 1 board is found:** use it and proceed to Board Type Detection.
3. **If multiple boards are found:** list them with their names and types (if available) and ask the user to pick one. Example: "I found 2 boards for OPS: 'OPS Sprint Board' and 'OPS Kanban Board'. Which one should I analyze?"
4. **If no boards are found** (or board listing tools aren't available): fall back to JQL-based detection — try the sprint search and infer from the results.

### Board Type Detection

Once you have a specific board (or if the user told you the type directly):

- If the user said **"Kanban board"** or **"Kanban"**: go directly to Kanban mode.
- If the user said **"Scrum"** or **"sprint"**: go directly to Scrum mode.
- Otherwise, try the **Scrum path first**: query for an active sprint on the board. If found → Scrum mode. If no active sprint → offer Kanban mode:

> "I didn't find an active sprint on this board. Would you like me to analyze it as a Kanban board?"

**Scrum mode** → proceed to "Resolve Sprint" below, then Step 2 (Scrum).
**Kanban mode** → proceed to "Collect Kanban Config" below, then Step 2K (Kanban).

### Resolve Sprint (Scrum Mode)

Different MCP servers expose different tools. Adapt your approach based on what's available:

**If you have board/sprint tools** (e.g., `jira_list_boards`, `jira_get_active_sprint`):
1. Search boards by project key or name filter
2. Fetch the active sprint directly — this gives you sprint name, goal, dates, and state

**If you only have JQL search and general search** (e.g., Atlassian MCP with `searchJiraIssuesUsingJql` and `searchAtlassian`):
1. Use JQL to find issues in the active sprint: `project = {key} AND sprint IN openSprints() ORDER BY priority DESC`
2. The sprint name and dates are usually embedded in the `sprint` field on each issue
3. **Sprint goal is NOT on individual issues** — it lives on the sprint object. To retrieve it:
   - Try a general search (e.g., `searchAtlassian`) for the sprint name to find sprint details
   - Try `fetchAtlassian` with a sprint ARI if one appears in search results (format: `ari:cloud:jira:cloudId:sprint/sprintId`)
   - If the sprint goal cannot be retrieved through any tool, note "Sprint goal: Could not be retrieved (MCP limitation)" in the output — do NOT say "Not defined" unless you've confirmed the goal field is actually empty
4. If `openSprints()` JQL function isn't supported, ask the user for the sprint name and use: `project = {key} AND sprint = "{sprint_name}"`

If the user gives a project key, search filtered by that project. If multiple boards/sprints match, show them and ask which one.

Extract sprint metadata:
- `sprint_name`, `sprint_goal` (may be empty or unretrievable — see above), `start_date`, `end_date`, `state`
- The sprint goal is important for Rule 1 — if the goal field is empty or couldn't be retrieved, that rule is skipped

**Edge cases:**
- **Multiple active sprints:** Unusual but possible. List them and ask the user to pick.
- **Sprint has no start/end date:** Cannot analyze. Tell the user.
- **Sprint state is "closed" or "future":** Only analyze sprints with state "active". If the only sprint returned is closed/future, let the user know.
- **Too many boards returned:** If the board search returns 50+ results, ask the user for a more specific project key or board name rather than listing everything.
- **Company-managed vs team-managed projects:** Jira Cloud has two project types with slightly different APIs. Board/sprint APIs work the same, but field names on issues may differ (e.g., next-gen projects use `issuelinks` instead of `subtasks` for parent-child relationships). The script handles both.

### Collect Kanban Config (Kanban Mode)

For Kanban analysis, collect the following from the user or use defaults:

1. **Project key** — required (you already have this from the board discovery step)
2. **Analysis window** — default: 14 days. Ask the user if they want a different window (e.g., "last 7 days", "last 30 days"). Calculate `analysis_window_start` and `analysis_window_end` dates.
3. **WIP limits** (optional) — ask: "Does your board have WIP limits? If so, what are they? (e.g., 'In Progress: 4, In Review: 3')" If not provided, WIP violation detection is skipped.

Build the `kanban_config` object:
```json
{
  "project_key": "OPS",
  "analysis_window_days": 14,
  "analysis_window_start": "2026-03-16T00:00:00.000Z",
  "analysis_window_end": "2026-03-30T00:00:00.000Z",
  "wip_limits": { "In Progress": 4, "In Review": 3 }
}
```

## Step 2: Fetch Sprint Issues (Scrum Mode)

Retrieve all issues in the active sprint. Use JQL like: `sprint = {sprint_id} ORDER BY priority DESC`

**Pagination is required here.** Sprints with subtasks can easily exceed 100-200 issues. Use `maxResults=50` and paginate until you have everything:
1. Fetch page 1 (`startAt=0, maxResults=50`). Check the `total` field in the response.
2. If `total > 50`, fetch remaining pages. You can parallelize: if `total=180`, fetch `startAt=50`, `startAt=100`, `startAt=150` concurrently.
3. Do not proceed to Step 3 until you have all issues — partial data will produce wrong rule results (especially burndown, workload, and bottleneck calculations).

For each issue, you need these fields:
- `key`, `summary`, `status`, `statusCategory`, `assignee`, `priority`
- `created`, `updated`, `issuetype`, `parent`
- `comment` or `comments` (comments list — Jira APIs return either name), `subtasks`, `issuelinks`
- **Estimation field** — this varies across orgs. The script auto-detects from these candidates: `story_points`, `storyPoints`, `story_point_estimate`, `customfield_10016` (Jira Cloud default), `customfield_10028`, `customfield_10002`, `estimation`, `estimate`, `points`. If none found, the script falls back to ticket count.
- `statuscategorychangedate` (or `statusCategoryChangeDate`) — when the issue last changed status category. Critical for Rule 8.

**Important field notes:**
- `statusCategory` is essential for most rules. If missing on some issues, the script warns but continues. If the MCP returns `fields.statusCategory.name` instead of a flat string, flatten it before passing to the script.
- `assignee` can be an object (`{ displayName, accountId }`) or a string — the script handles both. Prefer `displayName` for readable output.
- `issuetype` varies: classic projects use "Sub-task", next-gen may use "Subtask" or "Child Issue". The script normalizes case.

If a field isn't available, the rules that need it will be skipped gracefully. The script outputs a `warnings` array if critical fields are missing.

## Step 2K: Fetch Kanban Board Items (Kanban Mode)

Run these JQL queries in parallel. Paginate each (`maxResults=50`) until you have all results.

**Query 1 — Active items** (all non-Done issues on the board):
```
project = {key} AND statusCategory != Done ORDER BY status ASC, updated DESC
```

**Query 2 — Recently resolved** (for cycle time and throughput analysis):
```
project = {key} AND resolved >= -{lookback_days}d ORDER BY resolved DESC
```
Use `lookback_days = 28` (4 weeks) to give enough data for throughput trend and cycle time median.

**Query 3 — Backlog blockers** (same as Scrum Rule 5, but without the sprint clause):
```
project = {key} AND priority = Blocker AND status NOT IN (Done, Closed) ORDER BY updated DESC
```

For each issue, you need the same fields as Step 2 (Scrum), except:
- **No estimation field needed** — Kanban analysis uses item count, not story points.
- **`resolved` date** is needed on Query 2 results for cycle time calculations.
- `statuscategorychangedate` is critical for aging work items (Rule K1) and cycle time outliers (Rule K2).

Save the data for the script:
- `issues.json` — all items from Query 1
- `resolved.json` — all items from Query 2
- `config.json` — the `kanban_config` object from Step 1

## Step 3: Run Anti-Pattern Detection

### Rule Applicability Matrix

| Rule | ID | Scrum | Kanban |
|------|----|-------|--------|
| 1 Goal Tickets | goal_tickets_unfinished | YES | -- |
| 2 New Scope | new_scope_added | YES | -- |
| 3 In Review No PR | in_review_no_pr | YES | YES |
| 4 Unassigned Active | unassigned_active | YES | YES |
| 5 Blockers in Backlog | blocker_in_backlog | YES | YES (no sprint clause) |
| 6 Burndown | sprint_burndown | YES | -- |
| 7 Workload Imbalance | workload_imbalance | YES | YES |
| 8 Stale In Progress | stale_in_progress | YES | -- (replaced by K1) |
| 9 Bottleneck Columns | bottleneck_columns | YES | YES |
| 10 Done Not Merged | done_not_merged | YES | YES (window-based) |
| 11 Unlinked Commits | unlinked_commits | YES | YES (window-based) |
| 12 Comment Volume | high_comment_volume | YES | YES (window-based) |
| K1 Aging Work | aging_work_items | -- | YES |
| K2 Cycle Time Outliers | cycle_time_outliers | -- | YES |
| K3 Throughput Trend | throughput_trend | -- | YES |
| K4 WIP Violations | wip_violations | -- | YES |

### Scrum Mode

The 12 Scrum rules split into two groups that can run **in parallel**:

**Group A — Script rules (Rules 1, 2, 4, 6, 7, 8, 9, 12):**
These only need the sprint metadata and issues you already fetched. Use the helper script for accuracy:
```bash
node scripts/analyze-sprint.mjs --sprint sprint.json --issues issues.json
```
Or follow each rule's detection steps below if you can't run the script.

**Group B — External query rules (Rules 3, 5, 10, 11):**
These require additional Jira or GitHub API calls. Run them in parallel with Group A and with each other:
- **Rule 3** (in_review_no_pr) — GitHub PR search
- **Rule 5** (blocker_in_backlog) — Jira backlog query (see pagination notes below)
- **Rule 10** (done_not_merged) — GitHub PR + commit search
- **Rule 11** (unlinked_commits) — GitHub commit list

If you have access to subagents, spawn them in parallel for each Group B rule. Otherwise, run them sequentially after Group A.

### Kanban Mode

The Kanban rules also split into two groups:

**Group A — Script rules (Rules 4, 7, 9, K1, K2, K3, K4, 12):**
```bash
node scripts/analyze-sprint.mjs --mode kanban --config config.json --issues issues.json --resolved resolved.json
```

**Group B — External query rules (Rules 3, 5, 10, 11):**
Same as Scrum, but adapt:
- **Rule 5** (blocker_in_backlog): remove `sprint NOT IN openSprints()` from JQL — just query `status NOT IN (Done, Closed)` for the project
- **Rules 10, 11** (done_not_merged, unlinked_commits): use `analysis_window_start` instead of `sprint.startDate` for the time range
- **Rule 12** (high_comment_volume): uses the analysis window dates instead of sprint dates

---

### Rule 1: Goal Tickets Unfinished
- **ID:** `goal_tickets_unfinished`
- **Priority:** HIGH
- **When to check:** Only when ALL of these are true:
  - Sprint has a goal defined (non-empty `sprint_goal`)
  - Sprint has not yet ended (`now < end_date`)
  - Sprint is >= 75% elapsed by business days (Mon-Fri only)
- **Detection:**
  1. Identify tickets linked to the sprint goal. Check for "sprint-goal" label first. If none found, read the sprint goal text and match it against ticket summaries to infer which tickets contribute to the goal.
  2. Filter to those where `statusCategory` is NOT one of: "Done", "Closed", "Resolved", "Complete"
  3. If any remain, this rule triggers
- **If sprint has no goal:** Skip entirely — do not trigger, do not report. Just note "Sprint goal: Not defined" in the header.
- **Output:** List the unfinished goal tickets with keys + summaries
- **Coaching nudge:** "Review blockers daily and reassign or slice scope to restore flow on goal items."

### Rule 2: New Scope Added
- **ID:** `new_scope_added`
- **Priority:** HIGH
- **Detection:**
  1. Find tickets created after `sprint_start_date` — exclude sub-tasks
  2. Calculate ratio: `new_tickets / total_non_subtask_tickets`
  3. Triggers if ratio > **15%**
  4. Even if ratio <= 15%, still mention new tickets added (as informational, not an alert)
- **Output:** List the new tickets with keys + summaries, show the percentage
- **Coaching nudge:** "Route new work through Product Lead; defer to backlog unless it unblocks the sprint goal."

### Rule 3: In Review Without PR
- **ID:** `in_review_no_pr`
- **Priority:** HIGH
- **Requires:** GitHub MCP (skip gracefully if unavailable — just note "GitHub integration not available, skipping PR checks")
- **Detection:**
  1. Find tickets where `status` matches a review state. Jira boards use different names — check for: "In Review", "Code Review", "Ready for Review", "Review in Progress", "Peer Review", "Review" (case-insensitive). Use the actual status names from the board's issues rather than hardcoding one variant.
  2. For each, search recent PRs (last 20) for the ticket key in PR title or branch name
  3. Categorize results:
     - **No PR at all** — highest concern
     - **Only closed/merged PRs, no open PR** — ticket might need status update
  4. Use judgment: non-code tickets (documentation, design, process) may not need a PR — exclude those from the alert
- **Output:** List tickets in review with no linked PR, separately list those with only closed PRs
- **Coaching nudge:** "Require a linked PR for review state; add a board validator or automation."

### Rule 4: Unassigned Active Tickets
- **ID:** `unassigned_non_todo_tickets`
- **Priority:** HIGH
- **Detection:**
  1. Find tickets where `statusCategory` is NOT "To Do" AND `assignee` is null/empty
  2. Include tickets in any active state — In Progress, In Review, Blocked, etc.
  3. Any match triggers the rule
- **Output:** List unassigned active tickets with their current status
- **Coaching nudge:** "Assign ownership on pull; do not move work forward without an assignee."

### Rule 5: Blockers in Backlog
- **ID:** `blocker_in_backlog`
- **Priority:** HIGH
- **Detection:**
  1. Run **targeted JQL queries** against the backlog. Backlogs can contain thousands of issues — never fetch the full backlog. Use narrow filters with `maxResults` capped at 20 per query.
  2. Run these queries (in parallel if possible, sequentially if not):

     **Query A — Blocker priority items not in sprint:**
     ```
     project = {project_key} AND priority = Blocker AND sprint NOT IN openSprints() AND status NOT IN (Done, Closed) ORDER BY updated DESC
     ```
     `maxResults = 20`

     **Query B — Blocked/waiting status items:**
     ```
     project = {project_key} AND status IN ("Blocked", "Waiting", "On Hold") AND sprint NOT IN openSprints() AND updated >= -{sprint_duration}d ORDER BY priority DESC
     ```
     `maxResults = 20`

     **Query C — Flagged or impediment-labeled items:**
     ```
     project = {project_key} AND (labels IN ("blocked", "impediment") OR flagged = true) AND sprint NOT IN openSprints() AND status NOT IN (Done, Closed) ORDER BY updated DESC
     ```
     `maxResults = 10`

  3. Deduplicate results across the 3 queries by issue key
  4. If any results remain, this rule triggers
- **JQL compatibility notes:** Some Jira instances may not support all JQL functions. If a query fails:
  - `openSprints()` not available → replace with `sprint NOT IN ({current_sprint_id})`
  - `flagged = true` not supported → drop that clause from Query C
  - Status names like "Blocked", "Waiting" may differ → check the project's actual workflow statuses first
  - If all 3 queries fail, skip this rule and note "Blocker backlog check unavailable due to JQL limitations"
- **Why tight filters matter:** Backlog queries without filters can return thousands of results and slow down or fail. The JQL above scopes to: same project, not in active sprint, not done, recently updated, and matching a specific blocker signal. This keeps each query fast and under 20 results.
- **Output:** List the blocker keys and summaries
- **Coaching nudge:** "Ensure blockers are addressed immediately; assign to current sprint or document why they are deferred."

### Rule 6: Sprint Burndown
- **ID:** `sprint_burndown`
- **Priority:** MEDIUM
- **Detection:**
  1. Calculate `elapsed_ratio` = calendar time elapsed / total sprint duration (using timestamps, not business days — this gives a continuous progress signal including weekends)
  2. Determine completion metric:
     - If any tickets have story points > 0: use points. `completed_ratio = done_points / total_points`
     - Otherwise: use ticket count. `completed_ratio = done_tickets / total_tickets`
     - "Done" means `statusCategory` in ["Done", "Completed", "Closed"]
  3. Pace assessment:
     - **Behind:** `completed_ratio < elapsed_ratio * 0.8`
     - **Ahead:** `completed_ratio > elapsed_ratio / 0.8`
     - **On track:** everything else
  4. Only triggers (as a warning) when the team is **behind**
- **Output:** "X% done at Y% elapsed (expected ~Z%)" with pace assessment
- **Coaching nudge:** "Re-plan with the team; drop lower-priority scope or swarm to finish committed work."

### Rule 7: Workload Imbalance
- **ID:** `workload_imbalance`
- **Priority:** MEDIUM
- **Detection:**
  1. Group all "In Progress" (`statusCategory` = "In Progress") tickets by assignee
  2. Calculate:
     - `max_issues` = most tickets assigned to one person
     - `avg_issues` = mean across all assignees in the in-progress group
     - `load_ratio` = max_issues / avg_issues
  3. Determine `total_team_members` = count of unique assignees across ALL sprint issues (not just in-progress)
  4. `active_ratio` = members_with_in_progress_work / total_team_members
  5. Triggers if `load_ratio > 2.0` OR `active_ratio < 0.5`
- **Edge case:** If no issues are in progress, skip this rule. If `total_team_members` is 0, default `active_ratio` to 1.0.
- **Output:** Show per-person counts, highlight overloaded and idle members
- **Coaching nudge:** "Rebalance assignments; pair or mob to unblock overloaded teammates."

### Rule 8: Stale In Progress
- **ID:** `stale_in_progress`
- **Priority:** MEDIUM
- **Detection:**
  1. Find tickets where `statusCategory` = "In Progress" (skip sub-tasks at top level)
  2. Check `statuscategorychangedate` — this is when the ticket entered its current status category. This is more reliable than `updated` (which fires on comments/edits)
  3. If `statuscategorychangedate` is older than **3 business days** (Mon-Fri), the ticket is a stale candidate
  4. **Parent-child exception:** If the ticket has subtasks and any child subtask moved to "Done" within the last 3 business days (check child's `statuscategorychangedate`), the parent is NOT stale — work is progressing through children
  5. If `statuscategorychangedate` is missing from the data, skip this ticket (don't guess)
- **Output:** List stale ticket keys with days idle and assignee
- **Coaching nudge:** "Escalate blockers; slice smaller; time-box spikes and decide on next steps."

### Rule 9: Bottleneck Columns
- **ID:** `bottleneck_columns`
- **Priority:** MEDIUM
- **Detection:**
  1. Collect all tickets in active statuses — exclude `statusCategory` "To Do" and "Done" (also exclude "Completed", "Closed")
  2. Need at least **4 active tickets** and **2 distinct statuses** to evaluate. With fewer tickets, the ratios aren't meaningful — skip the rule.
  3. Count tickets per `status` (the specific status, not the category)
  4. If the most common status holds > **50%** of active tickets, it's a bottleneck
- **Output:** Name the bottleneck status, its percentage, and the full status distribution
- **Coaching nudge:** "Swarm on the bottleneck column; reduce upstream pull until flow recovers."

### Rule 10: Done but Not Merged
- **ID:** `done_not_merged`
- **Priority:** MEDIUM
- **Requires:** GitHub MCP (skip gracefully if unavailable)
- **Detection:**
  1. Find tickets where `statusCategory` = "Done" / "Completed" / "Closed"
  2. For recently transitioned tickets (check `statuscategorychangedate` is within this sprint), search recent closed PRs for matching ticket keys in:
     - PR title
     - Commit messages within the PR
  3. If a "Done" ticket has no corresponding merged PR, flag it
  4. Use judgment: non-code tickets (design, documentation, process tasks) don't need merged PRs — exclude those from the alert
- **Output:** List done tickets that appear to need a PR but don't have one merged
- **Coaching nudge:** "Keep PRs and tickets in sync; only mark Done when merged and verified."

### Rule 11: Unlinked Commits
- **ID:** `unlinked_commits`
- **Priority:** MEDIUM
- **Requires:** GitHub MCP (skip gracefully if unavailable)
- **Detection:**
  1. Fetch recent commits on the main/default branch since sprint start
  2. For each commit message, look for a Jira ticket key pattern: `[A-Z]{2,}-\d+` (2+ uppercase letters, dash, digits)
  3. Calculate: `unlinked_ratio` = commits_without_key / total_commits
  4. Triggers if `unlinked_ratio > 20%`
  5. If there are no commits at all, skip this rule
- **Output:** Show the percentage and list a few unlinked commits with authors
- **Coaching nudge:** "Enforce commit message patterns or use PR templates that require ticket keys."

### Rule 12: High Comment Volume
- **ID:** `unresolved_comment_threads`
- **Priority:** MEDIUM
- **Detection:**
  1. For each sprint issue, count comments created within the sprint date range (`start_date` to `end_date`)
  2. If any issue has > **10 comments** within the sprint window, flag it
  3. These tickets likely have unresolved debates that need a synchronous discussion to settle
- **Output:** List tickets with high comment volume and their comment counts
- **Coaching nudge:** "Schedule a 15-30 min huddle to decide and capture a single source of truth."

---

### Kanban-Only Rules

These rules replace the sprint-dependent rules (1, 2, 6, 8) when analyzing Kanban boards.

### Rule K1: Aging Work Items
- **ID:** `aging_work_items`
- **Priority:** HIGH
- **Detection:**
  1. Find tickets where `statusCategory` = "In Progress" (skip sub-tasks)
  2. Check `statuscategorychangedate` — calculate business days since the issue entered its current status
  3. Tier thresholds:
     - **Warning:** > 5 business days
     - **Critical:** > 10 business days
  4. Sort results by age descending
- **Why different from Rule 8 (Stale In Progress):** Rule 8 uses a 3-day threshold designed for sprints. Kanban items naturally live longer in active states, so higher thresholds avoid false positives. The framing also shifts from "stale" (implying inaction) to "aging" (measuring flow time).
- **Output:** List aging tickets with days, severity, and assignee. Show critical items first.
- **Coaching nudge:** "Escalate blockers; break items into smaller deliverables; enforce WIP limits to finish before starting."

### Rule K2: Cycle Time Outliers
- **ID:** `cycle_time_outliers`
- **Priority:** MEDIUM
- **Detection:**
  1. From the recently resolved issues (last 28 days), calculate cycle time for each: `resolved - created` in business days. Exclude sub-tasks.
  2. Need at least 3 resolved items for a meaningful baseline. If fewer, skip this rule.
  3. Compute the **median** cycle time (more robust than mean for skewed distributions).
  4. For each active in-progress issue, calculate its current age (business days since `statuscategorychangedate`).
  5. Flag active items whose age exceeds **2x the median** cycle time.
- **Output:** Show the median, threshold, and list outliers with their age and ratio to median.
- **Coaching nudge:** "Investigate root cause; is this blocked, too large, or unclear? Slice or escalate."

### Rule K3: Throughput Trend
- **ID:** `throughput_trend`
- **Priority:** MEDIUM
- **Detection:**
  1. From the recently resolved issues (last 28 days), group by ISO week. Exclude sub-tasks.
  2. Need at least 2 weeks of data. If fewer, skip this rule.
  3. Calculate rolling average from all weeks except the latest.
  4. Compare the latest week's count to the rolling average.
  5. Trend assessment:
     - **Declining:** latest < 60% of rolling average
     - **Improving:** latest > 140% of rolling average
     - **Stable:** everything else
  6. Triggers only when the trend is **declining**.
- **Output:** Show weekly counts, rolling average, latest week count, and trend.
- **Coaching nudge:** "Declining throughput may signal blockers, overloaded WIP, or capacity issues. Investigate before adding more work."

### Rule K4: WIP Limit Violations
- **ID:** `wip_violations`
- **Priority:** HIGH
- **Detection:**
  1. If no WIP limits were provided by the user, skip this rule — note "No WIP limits configured" in output.
  2. Count active issues (exclude Done and sub-tasks) per `status` column.
  3. Compare each status count to the user-provided limit (case-insensitive matching).
  4. Any column exceeding its limit triggers this rule.
- **Output:** List violations with status name, current count, limit, and how many items over.
- **Coaching nudge:** "Stop starting, start finishing. Enforce WIP limits to restore flow."

---

## Step 4: Generate the Sync Prep

Using the triggered rules, generate the sync prep briefing. Use the **Scrum template** or **Kanban template** depending on the board mode. Keep the total output under **250 words**. (Healthy boards will be much shorter; unhealthy boards with many findings need the headroom.)

### Prioritization
- List sections and items in descending order of severity (HIGH before MEDIUM)
- Within the same priority, lead with the most impactful finding (e.g., burndown slippage of 30% is more urgent than a single unassigned ticket)
- Only include sections that have triggered rules — skip empty sections entirely

### Formatting Rules
- **One line per triggered rule.** Every rule that triggers gets its own bullet under the appropriate section. Do not merge findings from different rules into a single bullet — even if they overlap (e.g., aging work and workload imbalance may mention the same person, but they are separate signals and should be reported separately).
- Include ticket key + short summary for every ticket mentioned (e.g., "ABC-123 Auth Service")
- Mention assignees by name where relevant (e.g., "@sarah" for workload imbalance)
- If a rule found more than 3 items, show the top 3 and summarize the rest as "+N more"
- If no anti-patterns triggered: output "Board is healthy. No anti-patterns detected." (or "Sprint is healthy." for Scrum)

### Scrum Output Template

```
# Sync Prep: Sprint {sprint_name}
### Date: {today}
### Sprint Progress: {elapsed}% elapsed | {completed}% complete
### Sprint Goal: {goal or "Not defined"}

## Sprint Goals & Commitments
- **Burndown Pace:** {pace assessment}
- **Scope Change:** {new tickets summary}
- **Goal Tickets At Risk:** {unfinished goal tickets}

## Execution & Flow Health
- **Workload Imbalance:** {imbalance details}
- **Stale Work:** {stale tickets}
- **Bottleneck:** {bottleneck status}

## Board & Repo Alignment
- **Unassigned Work:** {unassigned tickets}
- **Review Gaps:** {in review without PR / done not merged}

--------
## Recommended Focus
1. {highest priority action item}
2. {second priority action item}
3. {third priority action item}
```

**Scrum Section Mapping:**
- **Sprint Goals & Commitments:** Rules 1 (goal_tickets_unfinished), 2 (new_scope_added), 6 (sprint_burndown)
- **Execution & Flow Health:** Rules 7 (workload_imbalance), 8 (stale_in_progress), 9 (bottleneck_columns)
- **Board & Repo Alignment:** Rules 3 (in_review_no_pr), 4 (unassigned_non_todo_tickets), 5 (blocker_in_backlog), 10 (done_not_merged), 11 (unlinked_commits), 12 (unresolved_comment_threads)

### Kanban Output Template

```
# Sync Prep: {project_key} Kanban Board
### Date: {today}
### Analysis Window: {start} -- {end} ({N} days)
### Active Items: {count} | Resolved This Period: {count}

## Flow Health
- **Throughput Trend:** {weekly counts, trend assessment}
- **Aging Work:** {aging items with severity}
- **Cycle Time:** Median {N} days | {count} outliers exceeding 2x median
- **Bottleneck:** {bottleneck status}

## WIP & Workload
- **WIP Violations:** {status: count/limit}
- **Workload Imbalance:** {imbalance details}

## Board & Repo Alignment
- **Unassigned Work:** {unassigned tickets}
- **Review Gaps:** {in review without PR / done not merged}
- **Comment Volume:** {high-comment tickets}

--------
## Recommended Focus
1. {highest priority action item}
2. {second priority action item}
3. {third priority action item}
```

**Kanban Section Mapping:**
- **Flow Health:** Rules K1 (aging_work_items), K2 (cycle_time_outliers), K3 (throughput_trend), 9 (bottleneck_columns)
- **WIP & Workload:** Rules K4 (wip_violations), 7 (workload_imbalance)
- **Board & Repo Alignment:** Rules 3 (in_review_no_pr), 4 (unassigned_non_todo_tickets), 5 (blocker_in_backlog), 10 (done_not_merged), 11 (unlinked_commits), 12 (high_comment_volume)

### Recommended Focus
Pick the top 3 most actionable findings. Each should:
- Name the anti-pattern clearly
- Reference specific tickets or people
- Suggest a concrete next step (drawn from the coaching nudges above)
