---
name: operating-model-updates
description: >-
  Fetches and distills updates across GitLab's company operating model
  initiatives — Software Factories, Non-Linear Gains, Mythos-readiness — and
  any GitLab epics labelled with operating-model / software-factory /
  non-linear-gains / mythos. Pulls the linked Google Docs Jamie referenced in
  the April 2026 ProdSec note plus any newer doc updates, and produces a
  concise digest of what changed, what's being asked of ProdSec, and how
  James's work connects. Used by prodsec-health-dashboard. Triggers:
  operating model updates, company operating model, software factories,
  non-linear gains, mythos readiness, mythos-ready, transformation epics,
  what's happening across r&d, opmodel digest, operating model digest.
license: MIT
metadata:
  version: 1.0.0
  author: jhebden
allowed-tools: Read Write Edit Bash Agent AskUserQuestion mcp__gitlab__glab_work-items_list mcp__gitlab__glab_work-items_view mcp__gitlab__glab_issue_list mcp__gitlab__glab_api mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__read_document mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__chat mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__read_file_content mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__list_recent_files mcp__workspace__web_fetch
---

# Operating Model Updates

Pull together what's happening across the company operating model so James
can plug into the right initiatives, contribute where it counts, and make
sure ProdSec work is represented in the broader transformation conversation.

This skill produces a digest. It does not push changes anywhere. The
digest is consumed by `prodsec-health-dashboard` and is also useful as a
standalone briefing.

## Quick Start

1. Decide scope — `daily` (last 24h), `weekly` (last 7d), or `full` (everything in flight)
2. Fetch all three of Jamie's named initiatives in parallel: Software Factories, Non-Linear Gains, Mythos
3. Fetch labelled GitLab epics across `gitlab-com` (operating-model / software-factory / non-linear-gains / mythos)
4. Pull the canonical Google Docs and any newer linked docs
5. Cross-reference to find what's being asked of ProdSec and where James's work plugs in
6. Synthesize into a digest grouped by initiative

## Identity & Anchor URLs

- **GitLab username:** `jhebden`
- **Primary GitLab group:** `gitlab-com`
- **Search scope for transformation epics:** `gitlab-com` and all subgroups
- **Anchor docs from Jamie's April 2026 note (refresh-on-open):**
  - Software Factories: https://docs.google.com/document/d/15oZ8nHZ7r2ABYQ5j4xUburWgA-KnryO8tcxaTr3WTVk/edit
  - Non-Linear Gains (human-less code reviews partnership): https://docs.google.com/document/d/1Hve19F5_NDh4gbM5mrb-U4yqXctiM9J90OdoRy2XzpA/edit
  - April 2026 ProdSec note (the trigger document): https://docs.google.com/document/d/16SYAjofflZhk9EUQ66kM21q20KrTGZY6eHR9kUfQRJo/edit
- **Mythos-readiness:** No single canonical doc in Jamie's note — discover via labelled epics and recent doc mentions (search query: `Mythos-ready` or `Mythos readiness`).

## Scope modes

| Mode | Window | Use when |
|---|---|---|
| `daily` | Last 24h of changes | Inside the daily dashboard regen |
| `weekly` | Last 7 days | Inside weekly-planning, retro prep |
| `full` | All open work + last 30d of activity | First run, monthly review, onboarding the dashboard |

Default to `daily` if not specified.

## Step 1: Fetch in parallel

Fire all of these in a single message:

### Anchor docs (Jamie's three references)

```
mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__read_file_content
  → fileId: 15oZ8nHZ7r2ABYQ5j4xUburWgA-KnryO8tcxaTr3WTVk      # Software Factories

mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__read_file_content
  → fileId: 1Hve19F5_NDh4gbM5mrb-U4yqXctiM9J90OdoRy2XzpA      # Non-Linear Gains

mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__read_file_content
  → fileId: 16SYAjofflZhk9EUQ66kM21q20KrTGZY6eHR9kUfQRJo      # Jamie's April 2026 note
```

If a Drive read fails (permission, expired ID), fall back to
`mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__read_document` with the URL,
and if that also fails, log it as a `(?)` source in the digest output —
don't block the run.

### Discover newer linked docs

```
mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search
  → query: "Software Factories"
    app: "gdrive"
    updated: "past_month"
    sort_by_recency: true

mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search
  → query: "Non-Linear Gains"
    app: "gdrive"
    updated: "past_month"
    sort_by_recency: true

mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search
  → query: "Mythos-ready OR Mythos readiness"
    app: "gdrive"
    updated: "past_month"
    sort_by_recency: true
```

### Slack mentions of the same initiatives

```
mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search
  → query: "Software Factories OR Non-Linear Gains OR Mythos"
    app: "slack"
    updated: "past_week"
    sort_by_recency: true
```

### Labelled GitLab epics

The label set varies by group; try the obvious labels first, fall back to
title search if no label matches.

```
mcp__gitlab__glab_work-items_list
  → flags: { type: ["epic"], output: "json", per_page: 50,
             group: "gitlab-com",
             label: "operating-model" }

mcp__gitlab__glab_work-items_list
  → flags: { type: ["epic"], output: "json", per_page: 50,
             group: "gitlab-com",
             label: "software-factories" }

mcp__gitlab__glab_work-items_list
  → flags: { type: ["epic"], output: "json", per_page: 50,
             group: "gitlab-com",
             label: "non-linear-gains" }

mcp__gitlab__glab_work-items_list
  → flags: { type: ["epic"], output: "json", per_page: 50,
             group: "gitlab-com",
             label: "mythos" }
```

Then a fallback search across the same group by title keyword:

```
mcp__gitlab__glab_api
  → method: GET
    path: /groups/gitlab-com/epics?search=Software+Factories&state=opened&per_page=20

mcp__gitlab__glab_api
  → method: GET
    path: /groups/gitlab-com/epics?search=Non-Linear+Gains&state=opened&per_page=20

mcp__gitlab__glab_api
  → method: GET
    path: /groups/gitlab-com/epics?search=Mythos&state=opened&per_page=20
```

Deduplicate by epic ID before processing — labels and title search can
overlap.

### James's plug-in points

```
mcp__gitlab__glab_issue_list
  → flags: { assignee: "jhebden", output: "json", per_page: 50,
             group: "gitlab-com", state: "opened" }

mcp__gitlab__glab_work-items_list
  → flags: { mine: true, type: ["epic"], output: "json", per_page: 50,
             group: "gitlab-com" }
```

## Step 2: Process oversized results

If any single JSON blob exceeds the inline token budget, dispatch a subagent
to extract just the fields we need: `iid`, `title`, `web_url`, `state`,
`labels`, `health_status`, `due_date`, `updated_at`, the first paragraph of
the description. Don't read oversized files directly with `Read`.

## Step 3: Categorize each epic

For each epic, assign one (and only one) of these initiative buckets based
on the order of precedence:

1. **Software Factories** — explicit `software-factories` label, or the
   word "Software Factory" in the title, or a description that links to
   the canonical Software Factories doc.
2. **Non-Linear Gains** — explicit `non-linear-gains` label, "NLG" or
   "Non-Linear" in the title, or links to the NLG doc.
3. **Mythos-readiness** — explicit `mythos` label, "Mythos" in the title,
   or description references SAST/DAST/SBOM/dependency-scanning adoption
   under the Mythos banner.
4. **Operating-model — other** — `operating-model` label without one of
   the above. These are the broader transformation epics (process,
   tooling, CI/CD, observability) outside the three named tracks.
5. **Adjacent — ProdSec impact** — not labelled but the description or
   recent activity asks for ProdSec input (SAST/DAST/Sec-Section/Risk
   Register/PSIRT keywords). Surface these as suggested adjacencies, not
   as authoritative operating-model entries.

## Step 4: Find James's connection points

Cross-reference James's open issues and epics against each bucketed epic.
A connection exists when:

- An issue James owns is referenced (`#nnn` or full URL) in the epic body or recent comments
- One of James's epics is linked as a child or related epic
- James is mentioned (`@jhebden`) in the epic or its recent comments
- A keyword from James's epic titles (EUREKA, SLSA, VulnMapper, SSCS, dependency-scanning, SBOM, vulnerability-management) appears in the operating-model epic

Each connection becomes a row in the digest with the epic, James's
matching item, and the connection type.

If no connection exists for a bucket, flag the bucket as a **representation
gap** — an area where ProdSec work isn't visible in the operating-model
narrative.

## Step 5: Surface what's being asked of ProdSec

For each epic, scan the description and recent comments for ask-shaped
phrases:

- "ProdSec to..." / "Product Security to..."
- "Need a security review for..."
- "Asking @jhebden / @<other-prodsec-name>..."
- "SAST / DAST / SBOM / SLSA gap..."
- "Mythos-ready scanner adoption..."
- "Risk register entry..."

Pull the surrounding sentence as context and tag it as an `Ask`, an
`Open question`, or a `Required dependency`.

## Step 6: Synthesize the digest

Group output by initiative (Jamie's three first, then operating-model
other, then adjacent). For each initiative:

```markdown
### <Initiative name>

**Anchor:** <doc URL> · <last updated>

**What changed since last digest:**
- <bullet — concrete change with date and source>

**Open epics in scope:** <count>
| Epic | Status | Due | James plug-in? |
|---|---|---|---|
| [Title](url) | onTrack / needsAttention / atRisk | YYYY-MM-DD | ✓ via <issue#> / — gap |

**Asks landing on ProdSec:**
1. <quoted ask> — source: <link> — DRI on our side: <name or unset>

**Representation gaps:**
- <bullet — what James is doing that isn't visible in this initiative's narrative>
- <bullet — initiative work where ProdSec input is implied but not formally requested>
```

End with a top-level summary section:

```markdown
## (｡♥‿♥｡) Operating Model Digest — <Date> — <Mode>

### TL;DR
- <one line per initiative — biggest signal>

### Highest-priority asks
1. <verb-led one-liner> — <link>

### Representation gaps for James
1. <gap> — <suggested action>

### Stale / atRisk to watch
- <epic> — <reason it needs attention>
```

## Output destinations

- **Default**: print the digest inline (Markdown).
- **When called by `prodsec-health-dashboard`**: also write the digest to
  `/sessions/<session-id>/mnt/.cache/operating-model-<YYYY-MM-DD>.md` so
  the orchestrator can read it without re-running the whole pipeline.
- **On user request "save digest"**: write to
  `~/Documents/Claude/digests/operating-model-<YYYY-MM-DD>.md` (create
  the directory if missing).

## Style & low-context discipline

- Apply the `low-context-comms` skill — every "Asks landing on ProdSec"
  bullet must include a DRI and a deadline (or explicitly say "no DRI named
  yet").
- Apply `natural-writing-style` — no hedging, no AI tells, varied sentence
  length.
- Always cite: every claim in the digest links back to its source (epic,
  doc, Slack message). No source-less assertions.
- Acronyms get expanded on first use per `low-context-comms` rules.

## Guard Rails

- **No new GitLab issues / no comments posted.** This skill is read-only.
  If it identifies an action, it surfaces it; James decides whether to
  comment.
- **No doc edits.** Even on the anchor docs.
- **Skip labels that don't exist.** A 404 on a label query isn't an error;
  it just means the label isn't in use yet — note it in output.
- **Cap epic processing at 25 per bucket.** If more, sample the most
  recently updated and note "+<N> more not shown — re-run with `mode=full`".
- **Treat health status as advisory.** `onTrack` doesn't override a stale
  description; if an epic hasn't been touched in 30 days, flag it
  regardless of health.

## When called by other skills

`prodsec-health-dashboard` calls this with `mode=daily` and expects:
- The cache file at the path above
- A two-line TL;DR for embedding in the dashboard summary

`prodsec-risk-register` calls this with `mode=weekly` to find which risks
are tied to which operating-model initiatives.

## References

- `references/initiative-keywords.md` — keyword expansion lists for matching
- `references/digest-cache.md` — cache format and conventions
