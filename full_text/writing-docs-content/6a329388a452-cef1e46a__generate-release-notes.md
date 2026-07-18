---
name: generate-release-notes
description: This skill should be used when the user asks to "generate release notes", "draft release notes", "write release notes for issue", "create a release post entry", "draft monthly release notes", "release post YAML", or provides a GitLab issue/MR URL and asks to summarize the change for release. Produces either GitLab monthly release-notes Markdown (Hugo shortcode format with tier/offering/links inside a `{{< details >}}` block, ≤125-word description in "In previous versions you couldn't… Now you can…" voice) or release-post YAML items.
version: 0.3.0
license: MIT
---

# generate-release-notes

## Purpose

Draft a release-notes entry for a GitLab feature from one issue (and optionally one or more MRs). Produces one of two artifacts at the user's choice: GitLab monthly release-notes Markdown (Hugo shortcode format), or a release-post YAML item. Built for GitLab PMs drafting their own features into the monthly release docs and the release post.

## Required inputs

- A GitLab issue URL (mandatory).
- Zero or more MR URLs (optional — useful when the issue body is sparse or the change shipped across multiple MRs).
- A format choice (one of two — see Workflow step 1).

If the user provides only a feature description with no issue URL, ask for the issue URL before proceeding. Release notes need a canonical `[Related issue]` link.

## Workflow

### 1. Confirm format

If the user hasn't specified, ask:

> Which format? **(1)** Monthly release-notes Markdown (the `{{< details >}}` block that goes into `doc/releases/<major>/gitlab-<major>-<minor>-released.md` in `gitlab-org/gitlab`), or **(2)** release-post YAML item (for the www-gitlab-com release post).

Wait for the answer before fetching anything. The two formats need different fields, so fetching first wastes work.

### 2. Detect data source

Check whether the GitLab MCP tool `mcp__gitlab__get_issue` is available in the current tool list.

**MCP available** (typical Claude Code setup):
- Call `mcp__gitlab__get_issue` for the issue URL.
- For each MR URL, call `mcp__gitlab__get_merge_request`.
- Only call `mcp__gitlab__get_merge_request_diffs` if the issue + MR descriptions don't make the user-visible change clear. Diffs are expensive and rarely needed for release-notes voice (which is about user impact, not implementation).

**MCP unavailable** (claude.ai web, or Code without GitLab MCP configured):
- Don't error. Drop to paste mode silently.
- Ask the user to paste, in this shape:

  ```
  ISSUE
  Title: ...
  URL: ...
  Labels: GitLab Tier::Premium, group::pipeline execution, devops::verify, Category::Continuous Integration
  Description:
  <paste body>

  MR 1 (optional)
  Title: ...
  URL: ...
  Merged: yes
  Description:
  <paste body>
  ```

### 3. Extract release fields

From the fetched or pasted content, extract:

- **Feature name** — from issue title (cleaned up: remove `[Feature]`, milestone prefixes, etc.).
- **Tier** — from `GitLab Tier::Free|Premium|Ultimate` labels, or the older `GitLab Premium` / `GitLab Ultimate` label form. If absent or ambiguous, **ask**. Never silently default to Free.
- **Offering** — `GitLab.com`, `GitLab Self-Managed`, `GitLab Dedicated`. Default all three; confirm with the user if the issue suggests otherwise. `GitLab Dedicated for Government` is a fourth value used when applicable.
- **Documentation link** — for Markdown format, use a **relative path** from the release-notes file's directory (`doc/releases/<major>/`) to the docs page. Most paths look like `../../ci/...`, `../../user/...`, `../../administration/...`. For YAML format, use the full `https://docs.gitlab.com/...` URL. If the docs MR isn't merged yet, accept `TBD` and flag in assumptions.
- **Section** (Markdown only) — one of `Primary features`, `Agentic Core`, `Scale and Deployments`, `Unified DevOps and Security`. Pick based on feature theme; ask if unclear.
- **Category** — from `Category::*` label (e.g. `Category:Merge Trains` → `Merge Trains`). Used in Markdown as the `<!-- categories: ... -->` comment and in YAML's `categories:` list.
- **Stage / group** — from `devops::*` and `group::*` labels.
- **Reporter** — defaults to `@rutshah`. On first use per session, ask "Drafting on behalf of yourself (@rutshah) or someone else?" and remember the answer for subsequent invocations in this session.
- **Community contribution** — check for the `Community contribution` label on the issue or any of the MRs. If present, capture the contributor's name and GitLab handle (from MR author).

### 4. Draft

Apply the chosen template (verbatim blocks below). Voice rules:

- Present tense, second person ("you").
- Open with past-state framing: "In previous versions you couldn't…" or "Previously, you had to…".
- Then "Now you can…".
- ≤125 words for the description body.
- No marketing adjectives: avoid "powerful", "seamless", "robust", "blazing", "cutting-edge", "revolutionary".
- Concrete user benefit, not internal mechanics. The reader is a customer, not an engineer.

### 5. Present and confirm

Output the draft inside a fenced code block so it's copy-pastable.

After the draft, list assumptions in a short bullet list:

> Assumptions:
> - Tier: Premium, Ultimate (from `GitLab Premium` and `GitLab Ultimate` labels)
> - Offering: GitLab.com, Self-Managed, Dedicated (default — no constraint found)
> - Section: Unified DevOps and Security
> - Documentation: `../../ci/pipelines/merge_trains.md` (from docs MR)
> - Reporter: @rutshah

Ask if any need correction. Do not iterate silently — surface every inference.

### 6. Surface submission deadlines

After confirming the draft, remind the user of the deadlines that apply to the target release (see "Submission process and deadlines" below). Tailor the reminder to the user's situation:

- If the milestone is in a future release week: call out the **week-before deadline** for inclusion in the Self-Managed (SM) package.
- If the user mentioned this is a top/primary item: emphasize the **week-before "What's new" deadline** and ask whether they have an image yet.
- If they're already in release week: call out the **Wednesday content cutoff** for the initial release-notes page.

Don't surface deadlines that aren't relevant — keep it short and specific to the entry being drafted.

## Output template 1: Monthly release-notes Markdown (Hugo shortcode)

The 19.0+ release-notes file uses Hugo shortcodes. The entry sits under one of four section headings: `## Primary features`, `## Agentic Core`, `## Scale and Deployments`, `## Unified DevOps and Security`. The entry itself is a level-3 heading.

```markdown
### {Feature name}

<!-- categories: {Category from issue label} -->

{{< details >}}

- Tier: {Free|Premium|Ultimate}
- Offering: {GitLab.com, GitLab Self-Managed, GitLab Dedicated}
- Links: [Documentation]({relative_doc_path}), [Related issue]({issue_url})

{{< /details >}}

In previous versions you couldn't {prior limitation}. Now you can {new capability},
which {concrete user benefit}. {Optional: how to access — UI path or API}.
```

Format notes (these matter — getting any of them wrong fails the docs lint):

- Heading is `###` (level 3), not `####`.
- `{{< details >}}` is a Hugo shortcode, **not** the HTML `<details>` element. Do not include a `<summary>` line.
- Tier, Offering, and Links live as bullets **inside** the shortcode, not outside.
- The `<!-- categories: ... -->` comment sits between the heading and the details block.
- Documentation link is a **relative path** from `doc/releases/<major>/`. Most paths start with `../../`.
- Description prose follows the closing `{{< /details >}}`. No leading bullet, no list.
- For community contributions, append a "Thanks to [Name (@handle)](URL) for this community contribution." sentence as the final line of the description.

## Output template 2: Release-post YAML

```yaml
- name: "{Feature name}"
  available_in: [{free|premium|ultimate}]   # tiers, lowercase, list
  documentation_link: '{doc_url}'             # full https:// URL
  image_url: '/images/release/placeholder.png'   # PM replaces post-draft
  reporter: {gitlab_handle_without_at}
  stage: {stage}
  categories:
    - "{Category from issue label}"
  issue_url: '{issue_url}'
  description: |
    In previous versions you couldn't {prior limitation}. Now you can
    {new capability}, which {concrete user benefit}.
```

## Voice and style — quick rules

- **Audience:** the customer, not internal teams.
- **Tense:** present.
- **Person:** second ("you can…"), not third ("users can…").
- **Length:** description body ≤125 words.
- **Banned adjectives:** powerful, seamless, robust, blazing, cutting-edge, revolutionary, intuitive, easy-to-use.
- **No internal jargon:** avoid epic numbers, milestone codenames, group names ("Pipeline Execution"), stage names ("verify") in user-facing copy. They're fine in YAML metadata fields, not in description prose.
- **Concrete > abstract:** "configure caching for 50% faster pipelines" beats "improved performance".

Full guide: see `references/voice-and-style.md`.

## Submission process and deadlines

(Applies to monthly release-notes Markdown. Release-post YAML follows separate deadlines in `gitlab-com/www-gitlab-com`.)

Release notes are submitted as MRs to `gitlab-org/gitlab`, editing the release-notes file for the target milestone (e.g. `doc/releases/19/gitlab-19-0-released.md`). The file itself contains a copy-this template near the top — match its format exactly.

**Deadlines:**

- **Week before release** — submit your entry by this point so it's included in the Self-Managed (SM) release package. Now that release notes live in `gitlab-org/gitlab`, hitting this window matters for SM customers.
- **Wednesday of release week** — content cut off for the initial version of the release-notes page (exact time TBD per release).
- **Top/primary "What's new" items** — must be ready the week before release. The in-app "What's new" trial merges before code cutoff, so primary items can't slip into release week.

**Images:**

- Optional for standard entries.
- For a **top/primary item** that will appear in the in-app "What's new" panel, upload a screenshot or short GIF to the existing release images folder and reference it. The item still ships without an image, but visuals help for primary items.

## Edge cases

- **Multiple MRs across milestones.** If MRs span milestones but ship one user-facing capability, draft one entry. If they ship distinct capabilities, ask which to feature, or draft one entry per capability.
- **Internal-only changes** (refactors, dependency upgrades, infra changes with no user-visible behavior). Refuse to draft a release note. Explain that release notes are for user-visible changes and suggest a changelog entry instead.
- **Missing tier label.** Ask explicitly. Wrong tier on a public release note is embarrassing.
- **Doc URL TBD.** The docs MR is often still open at drafting time. Accept `TBD` and flag it in the assumptions list. Suggest the user fill it in before merging the release-notes MR.
- **Beta / Experiment features.** Note explicitly in the description ("This feature is in beta…") and confirm tier rules for beta features with the user — beta tier semantics differ from GA.
- **Community contributions.** When the issue or any MR has the `Community contribution` label, the MR author is the contributor. Append a "Thanks to [Name (@handle)](URL) for this community contribution." sentence at the end of the description prose.

## Additional resources

- `references/monthly-notes-format.md` — canonical GitLab monthly release-notes format spec.
- `references/release-post-yaml.md` — canonical release-post YAML schema, field rules, and linter constraints.
- `references/voice-and-style.md` — full voice and style guide with examples.
- `examples/monthly-notes-example.md` — a worked example of monthly Markdown output.
- `examples/release-post-yaml-example.yml` — a worked example of YAML output.
