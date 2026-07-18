---
name: prodsec-reporting-updates
description: >-
  Drafts and reviews entries for the Product Security Reporting Updates page
  per Jamie's April 2026 ProdSec note. Pulls James's recent shipped work
  (closed issues, merged MRs, completed epic milestones), recent risk
  register changes, and active operating-model asks, and synthesizes them
  into the Informing format (Problem / Current state / Next steps / More
  detail). Used by prodsec-health-dashboard. Triggers: reporting update,
  prodsec reporting update, product security reporting update,
  status report, weekly report, exec update, broadcast my work,
  represent my work, share what I've done, prodsec broadcast.
license: MIT
metadata:
  version: 1.0.0
  author: jhebden
allowed-tools: Read Write Edit Bash Agent AskUserQuestion mcp__gitlab__glab_issue_list mcp__gitlab__glab_work-items_list mcp__gitlab__glab_mr_list mcp__gitlab__glab_api mcp__gitlab__glab_user_events mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__read_document mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__chat mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__search_files mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__read_file_content mcp__workspace__web_fetch
---

# Product Security Reporting Updates

Draft entries for the Product Security Reporting Updates page so James's
work is broadcast in the format Jamie called out as the canonical
exemplar — Problem / Current state / Next steps / More detail.

This skill reads James's recent activity, identifies items worth
broadcasting, and produces ready-to-paste entries. It does not publish
anywhere — output is a draft that James reviews, copies, and lands.

## Quick Start

1. Determine reporting cadence — `weekly` (default), `bi-weekly`, or `ad-hoc topic`
2. Fetch James's recent shipped work + active high-impact items
3. Cluster items into 3–6 reportable entries (one per topic — never combine unrelated topics)
4. Pull adjacent context: matching risk register entries, operating-model asks, customer escalations
5. Draft each entry in the canonical format and run through `low-context-comms`
6. Suggest where each entry should land — Reporting Updates page, Slack broadcast, exec digest

## Identity & Anchor URLs

- **GitLab username:** `jhebden`
- **Reporting Updates page (canonical exemplar):** https://internal.gitlab.com/handbook/security/product_security/security-platforms-architecture/product-security-reporting/
- **Style guide reference (Jamie's note):** https://docs.google.com/document/d/16SYAjofflZhk9EUQ66kM21q20KrTGZY6eHR9kUfQRJo/edit
- **Primary GitLab group:** `gitlab-com/gl-security`
- **VM internal group:** `gitlab-com/gl-security/product-security/vulnerability-management/vulnerability-management-internal`

## Cadence modes

| Mode | Window | Output |
|---|---|---|
| `weekly` | Last 7 days | 3–6 entries grouped by initiative |
| `bi-weekly` | Last 14 days | 4–8 entries grouped by initiative |
| `ad-hoc topic` | The topic itself, no time window | A single entry, deep |
| `monthly` | Last 30 days | 6–10 entries with themes |

Default `weekly` if not specified.

## Step 1: Fetch the live reporting page

The page lives on `internal.gitlab.com` and may need authentication. Try:

```
mcp__workspace__web_fetch
  → url: https://internal.gitlab.com/handbook/security/product_security/security-platforms-architecture/product-security-reporting/
```

If that 401s or returns empty, fall back to Glean:

```
mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search
  → query: "Product Security Reporting Updates"
    app: "confluence,gdrive,handbook"
    sort_by_recency: true

mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__read_document
  → url: <top result>
```

Worst case, prompt James for the latest entry as an `AskUserQuestion`
preview so the skill can match the live format.

The goal of fetching the page is two-fold: confirm the format hasn't
changed, and identify what's already been reported so we don't repeat.

## Step 2: Pull James's recent activity

Fire in parallel for the chosen window:

```
mcp__gitlab__glab_user_events
  → flags: { username: "jhebden", per_page: 100, after: "<window-start>" }

mcp__gitlab__glab_issue_list
  → flags: { assignee: "jhebden", output: "json", per_page: 100,
             state: "all", group: "gitlab-com/gl-security",
             updated_after: "<window-start>" }

mcp__gitlab__glab_mr_list
  → flags: { author: "jhebden", output: "json", per_page: 50,
             state: "all", updated_after: "<window-start>" }

mcp__gitlab__glab_work-items_list
  → flags: { mine: true, type: ["epic"], output: "json", per_page: 100,
             group: "gitlab-com/gl-security/product-security",
             updated_after: "<window-start>" }
```

Plus context from the dashboard cache (read if present, don't re-run):

```bash
ls -t /sessions/*/mnt/.cache/operating-model-*.md 2>/dev/null | head -1
ls -t /sessions/*/mnt/.cache/risk-register-*.md 2>/dev/null | head -1
```

## Step 3: Score each item for reportability

A high score means it deserves a broadcast entry. Scoring:

| Signal | Points |
|---|---|
| Closed issue / merged MR with `psirt-slo::*` or `security-triage::*` label | 30 |
| Closed issue resolving a customer escalation (ZD ticket linked) | 30 |
| Epic milestone completed | 25 |
| MR merged that's referenced in an open risk register entry | 25 |
| Closed issue that's a child of a Mythos / NLG / SF epic | 20 |
| Any work referenced by a teammate's Slack mention this week | 15 |
| Newly opened high-priority epic (`needsAttention` / `atRisk`) | 15 |
| Repeated topic from prior reporting (bump or status change) | 10 |
| Any closed issue/MR not flagged elsewhere | 5 |

Take the top N by score (where N = entry count for the cadence mode).
Anything below 10 only gets included as a sentence in the digest summary,
not as its own entry.

## Step 4: Cluster

Group reportable items by topic. One topic = one entry. Common clusters:

- **Mythos-readiness** — SAST, DAST, SBOM, dependency-scanning rollout
- **Software Factories** — pipeline gates, factory tooling, CI/CD security
- **Non-Linear Gains** — AI-assisted triage, scanner adoption
- **Vulnerability Management ops** — PSIRT, triage queue, SLO compliance
- **Strategic projects** — EUREKA, SLSA, VulnMapper, SSCS
- **Risk register movement** — new entries, status flips
- **Customer-driven work** — anything tied to a ZD ticket

If a topic has only one item, but the item is significant (severity High,
customer impact), it still gets its own entry. Don't pad with low-value
items just to bulk up.

## Step 5: Draft each entry

Use the canonical format (channel-fit `Reporting Updates entry` from
`low-context-comms`):

```markdown
### <Topic — verb-led headline>

**Problem:** <state of the world that needed addressing — 1–3 sentences>
**Current state:** <what's been done, what's in flight — 1–3 sentences with explicit links>
**Next steps:** <upcoming actions with DRI and timing — 1–2 sentences, or "No action needed — informational" if applicable>
**More detail:** <SSoT link, prior reports, related epic / risk entry>
```

Run every draft through `low-context-comms` checklist:
- First-line test passes
- Why-not-just-what filled in
- All required slots populated
- Acronyms expanded on first use
- DRI named for any action
- Timing concrete (no "soon", "ASAP")

And through `natural-writing-style`:
- Active voice, contractions, varied sentences
- No banned patterns
- No em-dash overload
- Read-aloud test

## Step 6: Suggest landing surfaces

For each entry, suggest where it should land:

| Entry type | Primary | Secondary |
|---|---|---|
| Mythos-readiness milestone | Reporting Updates page | `#prodsec-leads` Slack |
| Customer-driven resolution | Reporting Updates page + customer-success-prodsec channel | — |
| New risk register entry | Reporting Updates page + a handbook MR for the register itself | — |
| Strategic project status | Reporting Updates page | Weekly exec digest if invited |
| Quiet ops work | Reporting Updates page only | — |

Output the suggestion for each entry. James decides whether the secondary
broadcast happens.

## Step 7: Final output

```markdown
## (¬‿¬) Reporting Update Draft — <Date> — <Cadence>

### TL;DR
- <one line per entry>

### Suggested headline for the digest broadcast
*<Slack-shaped opener line — bolded, one sentence>*

### Entries

#### 1. <Topic>
**Suggested landing:** Reporting Updates page · <secondary if any>

```
[full canonical-format entry, ready to paste]
```

#### 2. <Topic>
...

### What I left out
- <topic + reason — "no shipped work this week" / "still in flight, not yet reportable">

### Items below the threshold (mention only if asked)
- <bullet — for completeness>
```

## Cache

Write to:

```
/sessions/<session-id>/mnt/.cache/reporting-updates-<YYYY-MM-DD>.md
```

Same YAML-front-matter convention as the other skills. The dashboard
reads the latest by mtime.

## Gap detection

If James's recent work doesn't include any reportable items in a given
initiative bucket (Mythos / NLG / SF), flag it as a **representation
gap** in the digest:

```
### Representation gaps
- **Mythos-readiness:** No shipped or in-flight work this week. If this
  is intentional (deprioritised), say so in the next reporting update;
  otherwise consider drafting a status entry to keep visibility.
- **Operating-model — other:** Last reported activity was 2026-04-15. The
  next reporting update should mention this if work has resumed, or
  acknowledge the pause.
```

These gap notes are critical — they're what the dashboard's "alignment
score" depends on.

## Style & low-context discipline

Same rules as `low-context-comms` apply, with these reporting-specific
additions:

- **No marketing language.** "We delivered..." is fine; "We're proud to
  announce..." is not. Reporting is informational, not promotional.
- **No buried wins.** If something material shipped, lead the relevant
  entry with it.
- **Acknowledge what's not done.** "Targeted Tue 6 May; slipped to Wed 14
  May because the schema review surfaced a backwards-compat risk" is
  better than omission.
- **Quote, don't paraphrase, customer asks.** When citing an ask, use the
  exact phrasing from the source if possible.
- **Consistent ID format.** GitLab IDs as `&12345` (epic) or `#7890`
  (issue) or `!1234` (MR). Use the same form everywhere.

## Guard Rails

- **Read-only on the live page.** This skill drafts; it does not push.
- **No tagging in drafts.** `@<name>` mentions land in the eventual
  Slack post, not in the markdown draft (otherwise the dashboard could
  trigger phantom notifications).
- **No confidential entries unredacted.** If an item references a
  customer name, ZD ticket number, or unannounced vendor partnership,
  surface it in the draft but flag with `[CONFIDENTIAL — review before
  posting]` and require manual confirmation.
- **No fabricated metrics.** "We resolved 7 PSIRT tickets" only when
  the data actually supports it. If unknown, say "We resolved several
  PSIRT tickets — exact count tracked in &12345".
- **Never report work you didn't do.** This skill should never include
  items where James isn't author/assignee/DRI/contributor.

## When called by other skills

`prodsec-health-dashboard` calls with `cadence=weekly` and reads the cache
for the dashboard's "Recent Reporting" section. The dashboard's
representation-gap score is partly derived from this skill's output.

## References

- `references/entry-templates.md` — concrete templates per entry type
- `references/example-entries.md` — full worked examples in canonical format
