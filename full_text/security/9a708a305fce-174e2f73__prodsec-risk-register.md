---
name: prodsec-risk-register
description: >-
  Reviews and maintains James's representation in the Product Security Risk
  Register (per the Security Platforms Architecture handbook page). Pulls the
  live register, cross-references against James's open work in GitLab, runs
  gap analysis to find risks James is materially mitigating but isn't
  attributed to, surfaces risks where his initiatives need to be added, and
  drafts low-context register entries or updates ready for handbook MR.
  Used by prodsec-health-dashboard. Triggers: risk register, prodsec risk
  register, product security risk register, risk gap analysis, register
  representation, risk update, draft risk entry, risk coverage,
  risk-register entry.
license: MIT
metadata:
  version: 1.0.0
  author: jhebden
allowed-tools: Read Write Edit Bash Agent AskUserQuestion mcp__gitlab__glab_issue_list mcp__gitlab__glab_work-items_list mcp__gitlab__glab_mr_list mcp__gitlab__glab_api mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__read_document mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__chat mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__search_files mcp__cbc5b5bb-5bcc-44aa-ac18-15ea28b546f3__read_file_content mcp__workspace__web_fetch
---

# Product Security Risk Register

Make sure the Product Security Risk Register accurately reflects what James
is working on and what's actually at risk. Two things matter: (1) every risk
James is mitigating shows him as DRI or contributor, and (2) every
James-led initiative that warrants a register entry has one.

This skill reads the register, runs gap analysis, and drafts updates.
It does not commit to the handbook directly — output is always a proposed
MR that James reviews and lands.

## Quick Start

1. Pull the live register from the handbook
2. Pull James's open issues, epics, MRs across the gl-security group
3. Map issues/epics → existing register entries (matching rules below)
4. Surface gaps in three categories: Missing Attribution, Missing Entry, Stale Mitigation
5. Draft low-context updates / new entries for each gap, ready to MR

## Identity & Anchor URLs

- **GitLab username:** `jhebden`
- **Risk register handbook page:** https://handbook.gitlab.com/handbook/security/product-security/security-platforms-architecture/risk-register/
- **Handbook source repo:** `gitlab-com/content-sites/handbook` (the markdown files are in `content/handbook/security/product-security/security-platforms-architecture/risk-register/`)
- **Primary GitLab group:** `gitlab-com/gl-security/product-security`
- **VM internal group:** `gitlab-com/gl-security/product-security/vulnerability-management/vulnerability-management-internal`

## Step 1: Fetch the live register

Try sources in order — first that succeeds wins:

### 1a. Web fetch the public handbook page

```
mcp__workspace__web_fetch
  → url: https://handbook.gitlab.com/handbook/security/product-security/security-platforms-architecture/risk-register/
```

### 1b. Read the source markdown via GitLab API

```
mcp__gitlab__glab_api
  → method: GET
    path: /projects/gitlab-com%2Fcontent-sites%2Fhandbook/repository/files/content%2Fhandbook%2Fsecurity%2Fproduct-security%2Fsecurity-platforms-architecture%2Frisk-register%2F_index.md/raw?ref=main
```

If the path differs, fall back to a tree search:

```
mcp__gitlab__glab_api
  → method: GET
    path: /projects/gitlab-com%2Fcontent-sites%2Fhandbook/repository/tree?path=content/handbook/security/product-security/security-platforms-architecture/risk-register&recursive=true
```

### 1c. Glean search

```
mcp__2e8f6674-508f-424d-b798-ee73f8e35cea__search
  → query: "Product Security Risk Register"
    app: "gdrive,confluence,handbook"
    sort_by_recency: true
```

### 1d. Ask James

If all three fail, use `AskUserQuestion` to ask James for the canonical
source (handbook MR, Google Doc, etc.) and cache the response in
`~/.claude/state/risk-register-source.txt` for next run.

## Step 2: Parse the register into entries

The register is typically a Markdown table or a series of headed sections.
Parse into a list of entries with these fields:

| Field | Notes |
|---|---|
| `id` | `R-YYYY-NNN` style identifier; if absent, generate stable hash from title |
| `title` | The risk's headline |
| `description` | The body / threat description |
| `severity` | High / Medium / Low (use the team's scale) |
| `likelihood` | High / Medium / Low |
| `impact` | High / Medium / Low |
| `dri` | Named owner (or `unset`) |
| `contributors` | Anyone listed as supporting |
| `mitigation_status` | Open / Mitigating / Mitigated / Accepted / Closed |
| `mitigation_summary` | What's being done about it |
| `linked_epics` | GitLab epic / issue URLs in the entry |
| `last_reviewed` | Date of last update (parse from log or `last-updated` metadata) |
| `raw` | Original source text (for diff-quality MR drafting) |

If parsing is ambiguous, flag the entry with `parse_quality: low` rather
than dropping it.

## Step 3: Pull James's work

Fire in parallel:

```
mcp__gitlab__glab_issue_list
  → flags: { assignee: "jhebden", output: "json", per_page: 100,
             group: "gitlab-com/gl-security", state: "opened" }

mcp__gitlab__glab_work-items_list
  → flags: { mine: true, type: ["epic"], output: "json", per_page: 100,
             group: "gitlab-com/gl-security/product-security" }

mcp__gitlab__glab_mr_list
  → flags: { author: "jhebden", output: "json", per_page: 50, state: "opened" }

mcp__gitlab__glab_api
  → method: GET
    path: /users/jhebden/events?action=closed&target_type=Issue&per_page=50
```

The events endpoint catches recently-closed work that should still be
attributed to mitigations even if the issue itself is closed.

## Step 4: Match work to register entries

For each open issue / epic / MR, score against each register entry:

| Match signal | Score |
|---|---|
| URL of the issue/epic appears in the entry's `linked_epics` | 100 (definite match) |
| Title keyword overlap (≥3 distinct content words after stop-word strip) | 60 |
| One of James's epic codenames (EUREKA, SLSA, VulnMapper, SSCS) appears in the entry | 40 |
| Same labels (`category::*`, `area::*`) overlap | 20 |
| Description text similarity (cosine on shingles) > 0.5 | 30 |

Threshold = 50 for a match. Items above threshold attach to that entry;
items below threshold are unattached.

## Step 5: Gap analysis — three categories

### Missing Attribution

The work clearly mitigates an existing register entry, but the entry
doesn't list James as DRI/contributor and doesn't link the issue/epic.

Output: a list of register entries where James should be added, with the
specific item that proves mitigation activity.

### Missing Entry

James has substantial work (open epic with health, multiple linked issues,
or a closed MR with security impact) that has no matching register entry.
Could legitimately be a new risk.

Heuristics for "warrants a register entry":
- Open epic in `gl-security/product-security` with health `needsAttention`
  or `atRisk`
- Issue labelled `security-triage::*` or `psirt-slo::*`
- MR title or description references CVE / CWE / SLSA level / SBOM /
  vulnerability disclosure
- Cross-team dependency listed in the issue (other group is blocked on
  this work)

Output: candidate new register entries with draft text.

### Stale Mitigation

A register entry lists James (or one of his epics) but the linked epic /
issue has been closed, completed, or its mitigation status is no longer
current.

Output: entries needing a mitigation status flip, plus suggested new
language reflecting current state.

## Step 6: Draft updates

For each gap, draft the proposed change in handbook-MR-ready Markdown.
Always run the draft through `low-context-comms` before finalizing.

### Drafting Missing Attribution

Produce a unified-diff-style snippet:

```diff
| R-2026-014 | Stale CI runners expose dependency cache to non-cleared builds |
- | DRI: unset | Mitigation: investigation in flight |
+ | DRI: jhebden | Mitigation: investigation in flight ([&12345](url), [#7890](url)) |
```

### Drafting Missing Entry

Use the channel-fit template from `low-context-comms/references/channel-fit.md`
under "Risk register entry":

```markdown
### R-2026-NNN — <verb-led headline>

**Description:**
<3 short paragraphs — what the risk is, the threat scenario / exploit
path, why it matters now>

**Severity:** <High|Medium|Low>  ·  **Likelihood:** <H|M|L>  ·  **Impact:** <H|M|L>

**Mitigation:**
- <concrete step> — DRI: <name> — ETA: <date>
- ...

**Status:** Mitigating
**Last reviewed:** <YYYY-MM-DD>
**Linked work:** [&NNNN](epic-url), [#MMMM](issue-url)
```

Generate a tentative ID (`R-YYYY-NNN` where `NNN` = max existing + 1). Note
in the output that James should confirm the ID at MR time.

### Drafting Stale Mitigation

Provide a clear before/after of the mitigation block, and a one-line
comment for the handbook MR explaining the why:

```
Mitigation status: Mitigating → Mitigated. Linked epic &12345 closed
2026-04-22; rollout completed across all in-scope repos.
```

## Step 7: Output

```markdown
## (◔◡◔) Risk Register Review — <Date>

### TL;DR
- <count> entries reviewed
- <count> Missing Attribution gaps
- <count> Missing Entry candidates
- <count> Stale Mitigation issues

### Missing Attribution
1. **R-NNNN — <title>**
   *Why:* <evidence>
   *Suggested change:* <diff snippet>
   *Source:* <register link> · <linked issue/epic>

### Missing Entry candidates
1. **<draft title>** — <severity> / <likelihood> / <impact>
   *Why it warrants an entry:* <one paragraph>
   *Draft entry:* <full draft>
   *Linked work:* <links>

### Stale Mitigation
1. **R-NNNN — <title>**
   *Why stale:* <evidence>
   *Suggested update:* <before/after>

### Suggested handbook MR
- Title: `prodsec/risk-register: backfill James's mitigations + 2 new entries`
- Branch: `prodsec-risk-register-update-<YYYY-MM-DD>`
- Files: `content/handbook/security/product-security/security-platforms-architecture/risk-register/_index.md`
- Body: <ready-to-paste MR description>
```

The MR body uses the `mr-descriptions.md` reference from
`natural-writing-style` — Problem / Solution / Impact / Testing / Rollback.

## Cache

Write the parsed register and gap analysis to:

```
/sessions/<session-id>/mnt/.cache/risk-register-<YYYY-MM-DD>.md
```

Same format as `operating-model-updates` — YAML front-matter for the
dashboard, Markdown body for human reading.

## Style & low-context discipline

- Every "Missing Entry" draft must satisfy the Risk register entry
  channel-fit rules from `low-context-comms`.
- Severity / likelihood / impact must use the team's standard scale and
  link to the rubric. Never invent a custom scale.
- Every mitigation step must have a DRI and an ETA, or explicitly state
  "DRI not yet identified — proposed: <name>".
- No em-dashes in register entries — they obscure scanning.

## Guard Rails

- **Read-only on the handbook.** Never push directly. Output is a draft
  MR.
- **No issue creation.** If the gap analysis suggests a new GitLab issue
  should exist, surface that as a recommendation — don't create it.
- **Confidential entries.** If the register has private/internal-only
  sections, do not include their contents in any cache file or
  dashboard. Reference them by ID only.
- **Don't invent IDs that conflict.** If you can't reliably read all
  existing IDs, generate the new one as `R-YYYY-DRAFT-NN` and flag
  it as needing renumbering at MR time.
- **Keep severity calibrated.** A Missing Entry candidate scoring
  Severity: High triggers an `AskUserQuestion` confirmation before it
  hits the output — no surprises in the dashboard.

## When called by other skills

`prodsec-health-dashboard` calls with default mode and reads the cache
file for the dashboard's Risk Register section.

`prodsec-reporting-updates` calls to find the top 3 risks James should
mention in the next reporting update.

## References

- `references/severity-rubric.md` — recap of the team's scoring scale and
  links to the canonical rubric
- `references/parsing-fallbacks.md` — strategies when the register format
  changes
