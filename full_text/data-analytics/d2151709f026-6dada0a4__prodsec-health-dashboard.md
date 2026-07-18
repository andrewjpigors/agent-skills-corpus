---
name: prodsec-health-dashboard
description: >-
  Orchestrates James's Product Security health dashboard. Runs
  operating-model-updates, prodsec-risk-register, and prodsec-reporting-updates
  in parallel; synthesizes their caches into a single live HTML artifact
  showing alignment with operating-model and ProdSec epics, freshness of
  representation, and gaps where shipped or in-flight work hasn't been
  broadcast. The dashboard is regenerated daily via the prodsec-health-dashboard
  scheduled task and complements the daily-priorities briefing. Triggers:
  prodsec health dashboard, prodsec dashboard, health dashboard, build
  dashboard, refresh dashboard, regenerate dashboard, prodsec health,
  representation health, alignment health, gap dashboard, daily prodsec view.
license: MIT
metadata:
  version: 1.0.0
  author: jhebden
allowed-tools: Read Write Edit Bash Agent AskUserQuestion mcp__cowork__create_artifact mcp__cowork__update_artifact mcp__cowork__list_artifacts mcp__gitlab__glab_issue_list mcp__gitlab__glab_work-items_list mcp__gitlab__glab_mr_list mcp__gitlab__glab_todo_list mcp__gitlab__glab_api mcp__9b8600af-4161-42cd-847f-420f0b7df2f4__list_events mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__read_document mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__chat mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__read_file_content mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__list_recent_files mcp__workspace__web_fetch
---

# ProdSec Health Dashboard

The dashboard is one screen. James opens it once a day and learns:

- Where his work stands in the company operating model conversation
- Whether the Risk Register accurately reflects what he's mitigating
- Whether his shipped work has been broadcast through Reporting Updates
- Where representation gaps exist and what to do next

It complements `daily-priorities` (which is "what should I do today?") with
"how is my work being represented?" — a different question, asked at the
same daily cadence.

## Quick Start

1. Run the three sub-skills in parallel and write their caches
2. Pull additional dashboard-only signals (today's calendar, todos, fresh epic health)
3. Compute the three health scores: Alignment / Representation / Freshness
4. Identify gaps + suggested next actions
5. Render the HTML artifact `prodsec-health-dashboard`
6. Print a one-screen summary in chat

## Identity & Anchors

- **GitLab username:** `jhebden`
- **Artifact id:** `prodsec-health-dashboard`
- **Cache directory:** `/sessions/<session-id>/mnt/.cache/`
- **Sub-skills called:**
  - `operating-model-updates` (mode=`daily`)
  - `prodsec-risk-register`
  - `prodsec-reporting-updates` (cadence=`weekly`)
- **Pairs with:** `daily-priorities` (read-only — does not duplicate)

## Step 1: Run sub-skills (parallel where possible)

The orchestrator runs each sub-skill in its own Agent so caches stay out
of the main context window. Fire all three in a single message:

```
Agent({
  description: "Operating model digest",
  prompt: "Invoke the operating-model-updates skill in mode=daily.
           Write the cache file. Reply with the YAML front-matter only —
           no full markdown body."
})

Agent({
  description: "Risk register review",
  prompt: "Invoke the prodsec-risk-register skill in default mode.
           Write the cache file. Reply with the YAML front-matter only."
})

Agent({
  description: "Reporting updates draft",
  prompt: "Invoke the prodsec-reporting-updates skill in cadence=weekly.
           Write the cache file. Reply with the YAML front-matter only."
})
```

Each sub-skill writes its cache to disk; the orchestrator reads the caches
to populate the dashboard. The Agent return values give us only the YAML
front-matter for the score calculations.

If a sub-skill fails (e.g. handbook page unreachable), the orchestrator
proceeds with what's available and renders that section as `(￣ヘ￣)
Source unavailable — last-known data shown` plus the timestamp from the
last successful cache.

## Step 2: Pull dashboard-only signals

Run in parallel during the same message as Step 1:

```
mcp__gitlab__glab_todo_list
  → flags: { output: "json", per_page: 50 }

mcp__gitlab__glab_work-items_list
  → flags: { mine: true, type: ["epic"], output: "json", per_page: 50,
             group: "gitlab-com/gl-security/product-security",
             state: "opened" }

mcp__gitlab__glab_mr_list
  → flags: { author: "jhebden", output: "json", per_page: 20,
             state: "opened" }

mcp__9b8600af-4161-42cd-847f-420f0b7df2f4__list_events
  → startTime: <today 00:00 AEST>
    endTime:   <today 23:59 AEST>
```

These power the dashboard's "today at a glance" header.

## Step 3: Score health (three axes)

| Axis | What it measures |
|---|---|
| **Alignment** | How well James's open work maps to operating-model initiatives |
| **Representation** | Whether the Risk Register correctly attributes James's mitigations |
| **Freshness** | How recently James's work has been broadcast in Reporting Updates |

Each axis returns a numeric 0–100 score and a kaomoji band.

### Alignment score

- Start at 100
- Subtract 5 for each of James's open epics with no operating-model link
- Subtract 10 for each operating-model "Ask landing on ProdSec" with no DRI named
- Subtract 15 for each initiative bucket where James has zero plug-in points
- Cap subtraction at 70 (floor of 30)

### Representation score

- Start at 100
- Subtract 8 for each Missing Attribution gap from `prodsec-risk-register`
- Subtract 12 for each Stale Mitigation
- Subtract 6 for each Missing Entry candidate (these are softer — not all
  candidates need entries, but they need triage)
- Cap subtraction at 60 (floor of 40)

### Freshness score

- Start at 100
- Subtract 5 for each Reporting Updates representation gap (initiative not reported on)
- Subtract 10 if the latest Reporting Updates entry mentioning James's work is >14 days old
- Subtract 15 if no reporting update has been drafted by `prodsec-reporting-updates` in the cache
- Cap subtraction at 60 (floor of 40)

### Bands

| Score | Band | Visual |
|---|---|---|
| 80–100 | Healthy | (˶•ᵕ•˶) calm |
| 60–79 | Watch | (っ˘ω˘ς) warning |
| 0–59 | Action needed | (ﾉ>ω<)ﾉ urgent |

## Step 4: Identify the day's nudges

The dashboard surfaces a small ranked list of "do this today / this week"
nudges. Sources of nudges:

1. Highest-priority "Ask landing on ProdSec" with no DRI assigned
2. Risk register Missing Attribution where James's epic is the obvious owner
3. Reporting update entry that's drafted but not posted (cache says draft exists)
4. Operating-model epic with `needsAttention` health and no James plug-in
5. Stale Reporting Updates entry that needs a status flip

Cap at 5 nudges. Each nudge has an action verb, a target, and a link.

## Step 5: Render the artifact

Always render to the same artifact id (`prodsec-health-dashboard`) so the
sidebar entry is stable. First run: `create_artifact`. Subsequent runs:
`update_artifact`.

The HTML structure (see `references/artifact-template.html` for the full
template):

```
<header>
  Title: ProdSec Health
  Subtitle: as of <ISO timestamp>
  Three score chips (Alignment / Representation / Freshness)
</header>

<section "Today's nudges">
  Up to 5 ranked items, each with verb-led headline, one-line context, link
</section>

<section "Operating model alignment">
  Per-initiative panel (SF / NLG / Mythos / OpModel-other / Adjacent)
  Each panel shows: epic count, asks count, gaps count, james-plug-ins,
  health band, and a top-3 list of recently active items
</section>

<section "Risk register representation">
  Three columns: Missing Attribution / Missing Entry / Stale Mitigation
  Each column lists up to 5 items
</section>

<section "Reporting updates freshness">
  Latest reporting cadence date, count of representation gaps,
  draft state (drafted / not yet drafted), top 3 reportable items
</section>

<section "Linked docs">
  All the canonical docs from operating-model-updates and recent doc
  mentions surfaced via Glean — clickable list grouped by initiative
</section>

<footer>
  Generated: <timestamp>  ·  Sub-skill versions and last-cache mtimes
  Refresh: scheduled daily at 06:08 AEST
</footer>
```

The artifact uses CSS variables and the kaomoji visual band on each score
chip. No live MCP calls inside the HTML — everything is pre-rendered from
the caches (per James's `daily regeneration via scheduled task` choice).

## Step 6: Print one-screen chat summary

```markdown
## (｡♥‿♥｡) ProdSec Health — <Date>

**Scores:** Alignment <N>/100 (<band>) · Representation <N>/100 (<band>) · Freshness <N>/100 (<band>)

**Today's nudges:**
1. <verb> <thing> — <link>
2. ...

[Open full dashboard](computer:///sessions/<session-id>/mnt/.artifacts/prodsec-health-dashboard/index.html)
```

If a sub-skill failed, list it with the failure reason at the end so James
knows what's missing.

## Step 7: Hand off to daily-priorities

The daily-priorities scheduled task is updated to read this dashboard's
chat summary as its closing line ("Review ProdSec health dashboard"). The
two are independent — neither blocks the other — but they should be timed
so this dashboard regenerates *before* daily-priorities runs each morning.

Recommended schedule:
- `prodsec-health-dashboard`: 06:00 AEST daily
- `daily-priorities`: 06:09 AEST daily (already scheduled)

## Output destinations

- **Artifact:** Cowork sidebar, id `prodsec-health-dashboard`
- **Cache file (machine-readable):** `/sessions/<session-id>/mnt/.cache/health-dashboard-<YYYY-MM-DD>.json`
- **Chat:** One-screen summary, including link to the artifact

## Style & low-context discipline

The dashboard itself is the most low-context surface James produces — it's
a single screen that anyone could pick up. Apply `low-context-comms`
strictly:

- Every nudge has a verb, a thing, a link, and (where applicable) a DRI
- All initiative names expanded on hover (HTML title attr)
- Acronyms expanded on first occurrence per section
- Numbers, not adjectives, in score chips
- Kaomoji bands replace traffic-light colour-only encoding (accessibility)

## Guard Rails

- **Never auto-post.** The dashboard is a read-only view. It does not
  post drafts to Slack, the handbook, or GitLab issues.
- **Cache-only on regen.** If sub-skill caches exist and are <24h old,
  reuse them rather than re-running. The orchestrator only re-runs a
  sub-skill if its cache is missing or stale.
- **No PII / customer data in the artifact.** Sub-skills mark sensitive
  items with `[CONFIDENTIAL]`; the orchestrator strips them and replaces
  with a placeholder linking to the SSoT.
- **Missing source ≠ failure.** If a sub-skill cannot reach the handbook
  or Drive, render its section with `(￣ヘ￣) Source unavailable — last
  known: <date>` and the dashboard still loads.
- **One artifact per day.** Don't create dated copies (e.g.
  `prodsec-health-dashboard-2026-05-06`); always update the canonical id.

## Manual run vs. scheduled run

- **Manual:** James runs the skill ad-hoc to refresh during the day. Output
  to chat + artifact update.
- **Scheduled:** Run by the `prodsec-health-dashboard` scheduled task
  (created via `mcp__scheduled-tasks__create_scheduled_task`). On
  scheduled runs, suppress chat output beyond a one-line summary; the
  artifact update is the primary output.

## References

- `references/artifact-template.html` — base HTML / CSS for the dashboard
- `references/scoring-rules.md` — full scoring tables with worked examples
