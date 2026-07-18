---
name: multi-review
description: >
  Launch and coordinate multi-agent code reviews with optional fix mode.
  Handles scope analysis, multi-agent dispatch via multi-agent-review CLI,
  fix coordination, iterative convergence, and result communication.
  Trigger: user says /multi-review, "review this code", "review these
  changes", or requests a code review of any kind.
# Claude Code skill frontmatter; other agents receive instructions via prompt templates
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Agent
---

# Multi-Agent Code Review

Coordinate multi-agent reviews using `multi-agent-review` CLI. Reviews follow a phased pipeline:

    scope --> partition x lens matrix --> review --> merge --> global merge --> (optional) fix --> (optional) iterate

Small reviews collapse the pipeline: a single-kickoff review skips partitioning and the global merge. Each phase uses a fresh agent context. Effectiveness decays exponentially within a single context (DDI research) -- fresh agents per phase maintain review quality.

The skill has FULL AUTHORITY to deviate from the standard pipeline for unusual situations -- custom prompts, direct agent dispatch, strategy changes. The framework is infrastructure, not a cage.

## Terminology

Three terms describe the three axes of decomposition. Use them precisely; they are not interchangeable.

- **Lane** -- one agent's path within a single review execution: the claude lane, the codex lane, and the merge lane. Lanes are redundant perspectives on the SAME scope, managed by the CLI.
- **Partition** -- one unit of the scope split when a large review (>1000 LOC) is broken into separate, independent reviews (split by logical cohesion -- see Section 2). Partitions run in parallel and do not feed each other. Each partition gets its own scope prefix.
- **Wave** -- one iteration of the review --> fix --> re-review cycle within a partition. Waves run sequentially; wave N+1 is seeded with wave N's findings and fixes. Convergence rules (Section 6) count waves per partition.

Partitioned and multi-lens reviews add these terms:

- **Seam** -- the set of cross-partition dependency edges created by a partitioning cut: caller/callee pairs, shared data structures, schemas, contracts, and imports that span two partitions.
- **Seam manifest** -- the artifact emitted by the partitioning step that records every seam edge. An empty manifest is a meaningful result: evidence that the partitions are independent.
- **Lens** -- a named review discipline: what the reviewers should attend to, rendered mechanically as a review template plus optional rubric references. Examples: general correctness (the default), security, data-engineering pattern conformance. The seam review is a built-in lens applied to a computed scope.
- **Lens directive** -- a lightweight free-text steer within a lens, passed verbatim from the user (the `$lens_directive` template variable; formerly `$review_focus`). A directive tunes one run; a lens is a durable catalog entry.
- **Lens catalog** -- the discoverable set of lenses: packaged defaults plus project-defined entries, with metadata for matching user intent. Enumerate with `multi-agent-review list-lenses`.
- **Global merge** -- the cross-kickoff integration step that consolidates all per-kickoff integrated reports (partitions x lenses + seam) into one canonical findings document. Distinct from the per-kickoff lane merge (Claude + Codex).
- **Canonical findings document** -- the single user-facing deliverable of a review and the input contract for fixing.
- **Backlog** -- the DURABLE record of known, deliberately deferred issues (typically the repo's root `BACKLOG.md`, or an external tracker). Consulted at review time to classify findings as new vs already-known, and the destination where new out-of-scope findings are appended. Distinct from the ephemeral per-review backlog artifact, which survives only for `custom`/`none` backlog kinds (see Section 4).

A full review resolves to one or more partitions; each partition runs a sequence of waves; each wave runs lanes. With lenses, one wave of a partitioned review dispatches one kickoff per (partition x applicable lens) matrix cell, plus a seam kickoff when the manifest is non-empty; the global merge then consolidates the per-kickoff integrated reports. Mechanically, the CLI's `--wave` flag identifies a single `kickoff` invocation -- i.e., one wave of one matrix cell -- named `<partition-scope>-w<N>-<timestamp>` (see "Wave naming convention" in Section 3).

## 0. Help Mode and Onboarding

Two triggers route here instead of launching review infrastructure:

1. **The user asks about the skill** rather than requesting a review:
   `/multi-review help [topic]`, `/multi-review --help`, `/multi-review help lenses`, "what can the
   review skill do", "how does code review work here", or any question about the
   skill itself.
2. **Onboarding fallback**: a bare `/multi-review` with no scope and no arguments in a
   repo that has no `.multi-agent-review/` config. Do not fail cryptically --
   route here and offer `init`.

**Load `references/help.md` and follow it.** It holds the help dispatch logic,
the repo-aware behaviors (missing config, stale `config_version`, `help lenses`,
the backlog explainer), and the rule for reporting the absolute installed path of
the user guide. Help prose lives in `help.md` and the user guide, NOT in this
file -- this `SKILL.md` body loads on every review, so it stays lean.

**Never run execution or mutating commands in help mode:** no `kickoff`,
`launch-lane`, `global-merge`, or `backlog-append`. Read-only CLI (`list-lenses`,
`list-templates`, `backlog-digest`, `status`, `debug`, `doctor`) is allowed to
tailor the answer to the current repo.

## 1. First-Run Setup

This skill is a **generic coordinator**. All per-repo behavior lives in the
target repo's `.multi-agent-review/` directory (config, criteria chunks, prompt
overlay), never in skill files. The skill carries no per-repo state and is never
copied into a consumer repo -- it runs from the installed plugin (or, in
development, from a checkout). All target-repo paths below are relative to the
repo root.

Run the checks below once per repo per session, before the first real review.
Persist resolved values to `.multi-agent-review/config.json`.

### Config Location and Migration

Read wiring config from `.multi-agent-review/config.json` in the target repo.
Ignore any key whose name begins with `_` -- those are inline documentation
written by `init`.

- `.multi-agent-review/config.json` exists: use it.
- Only the legacy `config/review-config.json` exists: honor it for this run, then
  offer to migrate -- move its content to `.multi-agent-review/config.json` and
  add `config_version: 2`. The engine still reads the legacy path but prints a
  deprecation notice on every run, so migrating also silences that.
- Neither exists: this repo is not wired. A bare `/multi-review` routes to help and
  offers `init` (Section 0). For an explicit review request, offer to run
  `multi-agent-review init` (scaffolds `.multi-agent-review/config.json` plus an
  example criteria chunk), then continue.

**Check `config_version` on every invocation.** The version this skill expects is
`2`.

- Missing or lower than `2`: explain what changed and offer a migration -- bring
  the file to the current schema and set `config_version: 2`. Do not silently
  proceed on a stale schema (that is the drift class this redesign exists to
  kill).
- Higher than `2`: the config was written by a newer plugin than this skill.
  Tell the user to update the plugin (`/plugin update`) rather than editing the
  config down.

### Config Schema

```json
{
  "config_version": 2,
  "cli_path": "./bin/multi-agent-review",
  "worktree_root": ".review-worktrees",
  "review_standard_path": null,
  "default_lens": null,
  "backlog": null
}
```

- `config_version`: schema version. This skill expects `2`; see migration above.
- `cli_path`: path to the `multi-agent-review` binary (resolved by CLI Discovery below).
- `worktree_root`: directory under which both the engine's isolated review worktrees AND the skill's fix worktrees are created, plus the cleanup that manages them (default: `.review-worktrees`, relative to repo root).
- `review_standard_path`: path to a project-level review standard document (coding standards, review checklists). Default: `null`. See "Review Standard Discovery" below.
- `default_lens`: name of the lens applied to every partition when the user does not name one. Default: `null` -- fall through to the template catalog's `default_lens`, then the packaged default template (which is NOT a named lens; `--lens` is omitted at dispatch). See "Lens Resolution" in Section 2.
- `backlog`: how this project tracks its durable backlog. Default: `null` (not yet resolved -- triggers detection/ask; see "Backlog Discovery" below). One of:
  - `{"kind": "file", "path": "BACKLOG.md"}` -- a backlog file, path relative to the repo root. Fully supported: digest injection via `--backlog-path`, auto-append via `backlog-append`.
  - `{"kind": "custom", "instructions": "<free-form>"}` -- an external tracker (Jira, Notion, ...). The instructions tell YOU (the skill) how to query it and how to push new entries; you compose the digest yourself and inject it via `--template-vars-json '{"known_backlog_md": ...}'`, and push new entries per the instructions. No dedicated backend code exists -- follow the instructions best-effort, creating tools as needed.
  - `{"kind": "none"}` -- the user was asked and answered "none". Legacy behavior: ephemeral backlog extraction only. Never re-ask.

All fields except `config_version` are optional with sensible defaults. The skill writes this file incrementally as each check completes.

### CLI Discovery

The skill needs a working `multi-agent-review` CLI. Resolve it in this order;
first hit wins. Validate the chosen binary with
`multi-agent-review list-templates --output json` (confirms it runs and the
template catalog loads), then persist the resolved value to `cli_path`.

1. `cli_path` in `.multi-agent-review/config.json`, when set and runnable.
2. **The plugin's own bundled shim**: when this skill runs from an installed
   plugin, resolve its plugin root and use `<plugin-root>/bin/multi-agent-review`.
   Prefer `${CLAUDE_PLUGIN_ROOT}` when that env var is set. Otherwise derive the
   root from this skill's own location: this `SKILL.md` sits at
   `<plugin-root>/skills/multi-review/SKILL.md`, so the bundled shim is two directories
   up from it, then `bin/` -- `<plugin-root>/bin/multi-agent-review`.
3. `multi-agent-review` on `PATH` (a `uv tool install` of the package exposes it).
4. A consumer `./bin/multi-agent-review` shim in the target repo.
5. **None found: ask the user.** Mention the two install routes --
   `uv tool install git+<repo-url>` (or `uv tool install /path/to/checkout`), and
   the `MULTI_AGENT_REVIEW_HOME` dev override every shim honors first.

All example commands below spell the binary `multi-agent-review`; substitute the
resolved path (`cli_path`).

### Prerequisite Preflight (doctor)

The first time the skill does real work in a repo this session (not help mode),
preflight prerequisites before dispatch:

```bash
multi-agent-review doctor --output json
```

It returns `{"ok": <bool>, "checks": [{"name", "status", "detail", "fix"}]}` with
each `status` in `ok | warn | fail`.

- **Any `fail`**: stop before kickoff and surface each failing check's `detail`
  and `fix` (missing `claude`/`codex`/`uv`, absent Codex MCP config in
  `~/.codex/config.toml`, unusable `git worktree`). These are prerequisites no
  marketplace can install -- report them with fix instructions instead of failing
  mid-kickoff.
- **`warn` entries** (the CLAUDECODE sandbox advisory; a Codex config naming no
  MCP server; codex unable to load its MCP config or rejecting the
  `enabled=false` overrides kickoff emits -- these last two predict a
  claude-only codex lane, so surface them and their printed fix before
  dispatch): mention if relevant, but do NOT block on them.
- **All `ok`/`warn`**: proceed.

Run this once per repo per session; a later review after a clean preflight need
not re-run it.

### Commit Capability Preflight

Required every time fix mode is requested. Run this test in the actual fix worktree using the fixer agent's launch parameters -- not in a separate throwaway worktree.

```bash
# In the fix worktree, before dispatching real fixes:
cd "$FIX_WORKTREE"
touch .preflight-test
git add .preflight-test
git commit -m "preflight: test commit capability"
# Verify commit exists
git log --oneline -1  # should show the preflight commit
# Revert the test commit (keep the worktree clean for real fixes)
git reset --hard HEAD~1
```

If the commit blocks on interactive prompts or permission errors, offer three options:
1. **Proceed review-only** -- run the review without fix mode.
2. **Abort** -- stop so the user can fix permissions or agent configuration.
3. **Diagnose** -- inspect the blocker (git config, hooks, GPG signing, etc.) and report specifics.

### Review Standard Discovery

On first run, ask the user: "Does this project have a review standard document (coding standards, review criteria)?" Handle responses:

- **Yes + path provided**: persist to `review_standard_path` in `.multi-agent-review/config.json`.
- **No**: persist `null` and move on. No further prompting on subsequent runs.

On subsequent runs:
- If `review_standard_path` is set and the file exists, pass it via `$review_framework_refs` template variable.
- If `review_standard_path` is set but the file no longer exists, warn the user and clear the config entry.

The user can update this at any time by saying "set the review standard to X" -- update the config accordingly.

### Backlog Discovery

Resolve how the project tracks its durable backlog before dispatching a review. Resolution order (first hit wins):

1. **Explicit config**: the `backlog` key in `.multi-agent-review/config.json` is set (not `null`). Use it as-is; `{"kind": "none"}` means the user already answered -- never re-ask.
2. **Default detection**: run `multi-agent-review backlog-digest --root . --output json` -- it performs the case-insensitive root `backlog.md` lookup (`BACKLOG.md` preferred) and reports the resolved path, or exits 2 when nothing is found. When found, persist `{"kind": "file", "path": "<found name>"}` to the config and proceed without asking.
3. **Ask the user**: "How does this project track its backlog? A file (give me the path)? An external tracker -- give me instructions for querying it and adding entries? Or none?" Persist the answer as the `backlog` key (`file` / `custom` / `none`).

The user can update this at any time by saying "set the backlog to X" -- update the config accordingly. If a configured `file` path no longer exists, warn the user and re-run discovery.

## 2. Scope Resolution

Parse user input to determine what to review. Map the request to a CLI `--scope` argument.

### Input Patterns

| User says | Scope |
|-----------|-------|
| "review staged changes" | `staged` |
| "review my changes" / "review dirty" | `dirty` |
| "review last commit" / "review HEAD" | commit range -- resolve via `git diff --name-only HEAD~1..HEAD`, pass file list with `--changed-files-path`, use `--scope dirty` |
| "review these files: ..." | explicit file list |
| "review commit abc..def" | commit range |
| "review last 3 commits" / "review HEAD~3..HEAD" | commit range (resolve to SHAs) |
| "review everything" / "review the whole repo" / "full codebase review" | `all` |
| (no qualifier) | default to `staged`, fall back to `dirty` if staging area is clean |

`--scope` accepts three values: `staged` (files with staged changes only), `dirty` (staged changes, unstaged modifications, and untracked files -- the CLI flag's built-in default; note the skill's own no-qualifier mapping is staged-first per the table above, so an omitted `--scope` in a skill-driven review resolves to `staged`, not `dirty`), and `all` (every tracked file in the repo plus untracked files, regardless of change state -- a full-repo review, not a diff against any base). Use `all` sparingly: it bypasses the size heuristics below in spirit, since it is not bounded by what changed, so partition aggressively when scope resolves to `all`.

**Deletion caveat.** Automatic `staged`/`dirty` discovery runs `git diff --diff-filter=ACMR`, which EXCLUDES deleted paths -- a delete-only change is silently dropped from discovery and never reviewed. (`all` lists tracked files via `git ls-files`, which likewise cannot surface a path the change removed.) To include deleted paths, drive the review off an explicit file list (`--changed-files` / `--changed-files-path`); pair it with `--materialize-files-path` when a deleted path must also be materialized into the review worktree so a reviewer following a cross-partition edge sees its removal.

### Size Heuristics (SmartBear Research)

- **200-400 LOC**: optimal detection rate (~90% defect detection).
- **400-1000 LOC**: acceptable but detection declines.
- **1000+ LOC**: detection drops ~70%. Partition into multiple kickoffs.

These numbers are targets, not rules. Cohesion beats the number: never split a tightly coupled cluster merely to hit a LOC figure.

Check scope size before dispatch:

1. Run `git diff --stat` (or equivalent for the resolved scope).
2. Count total changed lines.
3. If >1000 LOC, warn the user and propose logical partitioning.
4. If the user confirms a large unpartitioned scope, proceed but note reduced effectiveness in the report.

### Logical Partitioning (when >1000 LOC)

Partition by logical cohesion, not directory layout. Full procedure, seam manifest schema, and artifact formats live in `references/partitioning-strategy.md`; the summary:

1. Build a lightweight dependency picture among the changed files: imports and symbol references via grep and targeted reads, with git co-change history as a tiebreaker for ambiguous groupings. No heavyweight tooling.
2. Cluster so tightly coupled files land together; cut the fewest, weakest edges. Directory grouping is a fallback signal when dependency evidence is thin.
3. Size each partition toward the 200-400 changed-LOC target. A 450-LOC cohesive partition beats two 225-LOC fragments that cut a hot edge.
4. **Emit the seam manifest -- mandatory whenever partitioning.** Record every cross-partition edge (file pair with partition membership, symbols/contracts on the edge, direction) to `<output-root>/reviews/<review-slug>-seam-manifest.md` (the output root is `tmp/` by default, or the kickoff's `--output-root`). Partitioning and seam identification are the same computation; the manifest is the cut, written down. An empty manifest is evidence of independence: retain it and skip the seam kickoff.

Each partition gets its own scope prefix and runs as its own independent kickoff (e.g., `authcore-w1`, `api-w1` -- two partitions, each at wave 1).

### Lens Resolution

Resolve which lenses apply before dispatch.

**Effective default lens** (first hit wins):

1. `default_lens` in `.multi-agent-review/config.json` (per-repo choice). YOU (the
   skill) read this key at startup and apply it at dispatch time by selecting
   the matching lens template via the per-kickoff `--review-template-name` /
   `--merge-template-name` flags, and by passing `--lens <name>` so repo criteria
   chunks scoped to that lens apply (see Section 3). The `multi-agent-review` CLI
   does not read this key.
2. `default_lens` in the effective template catalog. This is what `list-lenses`
   reports as `default_lens`; use it when the config key above is absent.
3. The packaged default (`review.default` via the `default` profile), also
   reflected by `list-lenses` when the catalog sets no `default_lens`. This is a
   template, NOT a named lens -- the packaged catalog defines no default lens
   name -- so at dispatch you OMIT `--lens` for this case (only unscoped repo
   criteria chunks apply). Pass `--lens` only when steps 1 or 2 yielded a name.

**Discovery and intent matching.** Enumerate lenses with `multi-agent-review list-lenses --output json`: name, description, keywords, review template, optional merge template, source layer (`packaged` | `project`), and the effective catalog `default_lens`. Match the user's requested discipline against names, descriptions, and keywords.

**Sparse matrix planning.** A review runs one kickoff per (partition x applicable lens) cell:

- The effective default lens applies to every partition.
- Additional lenses apply only to partitions whose content they match (e.g., a security lens applies to partitions touching auth/input/network surfaces -- the changed files are already in hand at partition time, so this mapping is nearly free).
- The seam lens (`review.seam`) applies to the computed seam scope whenever the seam manifest is non-empty.

Report the planned matrix and its cost BEFORE dispatch, e.g.: "3 partitions x default + security on partitions 1 and 3 + seam = 6 kickoffs."

**Missing lens.** When the user names a lens that matches no catalog entry: never silently fuzzy-match to a near miss, never hard-stop. Offer both:

1. **One-off**: inject the request verbatim as a lens directive (`lens_directive` template variable) into the default lens -- immediate, zero setup.
2. **Durable**: draft a new lens (review template + catalog entry with description and keywords) into the project's `.multi-agent-review/prompt-templates.yaml` for user review. It becomes a version-controlled team artifact that spreads by git pull.

### Edge Case: No Changes Found

If the resolved scope yields zero changed files:
1. Report to the user: "No changes found for scope `<scope>`. Nothing to review."
2. Do not launch the CLI. Do not create a wave.
3. Suggest alternatives: "Did you mean `dirty` instead of `staged`?" or "Check that the commit range contains changes."

### Commit Range Resolution

For ranges like `HEAD~3..HEAD` or `abc123..def456`:
1. Resolve to concrete SHAs: `git rev-parse HEAD~3` and `git rev-parse HEAD`.
2. Extract changed files: `git diff --name-only <from>..<to>`.
3. Pass the file list via `--changed-files-path` and use `--scope dirty` (the scope flag controls diff base for the review prompt; the file list is the actual boundary).

### File List Assembly

Build the file list for `--changed-files` or `--changed-files-path`:

1. Resolve the changed files from the scope.
2. Filter out binary files, lock files, and generated artifacts.
3. For `--changed-files-path`, write the list to a temp file and pass the path.
4. Prefer `--changed-files-path` over `--changed-files` when the file list exceeds 10 files (avoids shell argument length limits).

## 3. Review Dispatch

### Environment Note

The CLI's runner automatically strips sandbox-related env vars (`SANDBOX_RUNTIME`, `no_proxy`, `CLAUDECODE`, etc.) when launching Claude subprocesses. This allows review lanes to run from inside Claude Code sessions. No special handling is needed by the skill -- just invoke the CLI normally.

### Standard Dual-Lane

```bash
multi-agent-review kickoff --wave auth-w1-0304T1422 --scope staged \
  --review-worktree auto \
  [--lens <effective-lens>] \
  --backlog-path BACKLOG.md \
  --template-vars-json '{"context_seed": "Auth module was recently split from monolith; watch for stale imports."}'
```

**Pass `--lens <name>` when a named lens resolved** -- an explicitly requested lens, `config.json`'s `default_lens`, or the catalog's `default_lens` (Section 2's Lens Resolution). When resolution falls through to the packaged default template because no lens was requested AND no `default_lens` is configured (neither config nor catalog), OMIT `--lens`: there is no named default lens to pass, and the packaged catalog defines none. `--lens` is criteria-only: it scopes which repo criteria chunks under `.multi-agent-review/criteria/` are appended to the lane prompts (chunks whose frontmatter names that lens, plus unscoped chunks). Without a named lens, only unscoped chunks apply -- there is nothing lens-scoped to select. It does NOT select templates -- template selection is still `--review-template-name` / `--merge-template-name` (see the Dispatch Matrix).

Pass `--backlog-path <path>` on every kickoff when the resolved backlog kind is `file` (see "Backlog Discovery"). The CLI digests the durable backlog and injects it into review and merge prompts, enabling the three-way scope classification. For `custom` backlogs, compose the digest yourself and inject it via `--template-vars-json '{"known_backlog_md": "..."}'` -- and when the external tracker has ZERO open items, inject the exact placeholder `(backlog provided; no unresolved entries)` instead of an empty string: an empty value reads downstream as "no backlog provided" and would falsify the report's `Not checked` sentinel. For `none`, omit both.

**Wave naming convention** (ref: `fix-worktree-pattern.md` section "Wave Naming Convention"): use `<scope>-w<N>-<suffix>` format, where suffix is a compact timestamp (`MMDDTHHmm`) to prevent collisions. The scope prefix identifies the partition (what is being reviewed); N is the wave number -- the fix-cycle iteration within that partition. Examples: `auth-w1-0304T1422`, `templates-w2-0304T1500`, `w1-0304T0900` (single-partition reviews where a scope prefix adds no value). For matrix cells, encode a non-default lens in the scope prefix (`auth-security-w1-0304T1422`); the seam kickoff uses a `seam` prefix (`seam-w1-0304T1422`). The CLI validates wave names against `^[A-Za-z0-9][A-Za-z0-9._-]*$`.

**Review worktree semantics.** With `--review-worktree`, the CLI resolves the
changed files against the ORIGIN worktree (the review worktree is detached at
HEAD and has no staged/dirty changes of its own) and materializes their
uncommitted content in the review worktree before dispatching lanes. The
materialized files reflect the combined staged+unstaged state of each listed
file -- staged-only content is not distinguished, which is acceptable for
review purposes. On success the auto worktree is removed after artifacts are
copied back; on failure it is preserved for diagnosis and the CLI prints
`[kickoff] review_worktree_preserved=<path>`. Copy-back covers the job
directory (`tmp/collaborations/jobs/<wave>/`), the flat reports
(`tmp/reviews/<wave>-*.md`), and the per-wave directory (`tmp/reviews/<wave>/`).

**Leaked-worktree recovery.** A kickoff killed mid-run cannot clean up its auto
worktree, leaving `<review_root>/review-<wave>` behind. This is self-healing: a
later auto kickoff for the same wave detects the leftover and removes it before
creating a fresh one (`[kickoff] stale_review_worktree_removed=<path>`). To
sweep leaked worktrees across all waves, run
`multi-agent-review cleanup-review-worktrees` (dry-run list by default; add
`--remove` to delete). It only ever touches detached `review-*` worktrees under
the review root, so branch-based fix worktrees are never disturbed.

**Parallel dispatch is safe.** Kickoffs dispatched simultaneously from one
origin repository serialize their origin-git phase (stash-create, worktree
add/remove) behind a repo-scoped lock, so they queue briefly instead of failing
with `index.lock: File exists`. Parallel partition/lens/seam kickoffs need no
staggering.

### Dispatch Matrix (partitioned and multi-lens reviews)

Dispatch one kickoff per (partition x applicable lens) matrix cell:

- **Lens selection**: pass `--lens <lens.name>` for every NAMED-lens cell (so that lens's criteria chunks apply), and select its templates with `--review-template-name <lens.review_template>` (and `--merge-template-name <lens.merge_template>` when the lens defines one). A named default lens (config or catalog `default_lens`) still passes its own `--lens <name>`; only its templates need no override -- the profile default applies there. When the default falls through to the packaged default template (no named lens; the packaged catalog defines none), OMIT `--lens` for that cell.
- **Union materialization**: every partitioned kickoff passes `--materialize-files-path <path>` (only valid with `--review-worktree`), pointing at a file that lists the UNION of the full changeset across all partitions. This widens what is VISIBLE to reviewers -- cross-partition files read at their true post-change state when a reviewer follows an edge -- without widening the attention scope: the kickoff's `--changed-files-path` still carries only the partition's own files, and `changed-files.txt` stays partition-scoped.
- **Seam digest**: each partition kickoff receives a digest of its own seam edges via the `context_seed` template variable (format in `references/partitioning-strategy.md`), so reviewers know what the other side changed, in post-change terms.
- **Seam kickoff**: whenever the seam manifest is non-empty, dispatch one additional kickoff with `--review-template-name review.seam`, scope = the manifest's edge files, and the full seam-manifest digest via `context_seed`. It runs in parallel with the partition kickoffs and has its own dual lanes and lane merge. If a detectable seam issue exists, this is the agent whose success criteria is detecting it.
- **Backlog digest**: every matrix cell (partitions, lenses, and the seam kickoff alike) gets the same backlog treatment as a standard kickoff: `--backlog-path` for `file` backlogs, skill-injected `known_backlog_md` for `custom`. Lanes annotate candidate matches (`Known backlog match: <slug>`); the merge makes the authoritative three-way call.

Example cell dispatch (partition `auth` under the `security` lens):

```bash
multi-agent-review kickoff --wave auth-security-w1-0304T1422 --scope dirty \
  --changed-files-path tmp/reviews/auth-0304T1422/partition-auth.txt \
  --materialize-files-path tmp/reviews/auth-0304T1422/union.txt \
  --review-worktree auto \
  --lens security \
  --backlog-path BACKLOG.md \
  --review-template-name review.security
```

### Single-Lane Fallback

When only one provider is available, the CLI automatically falls back to single-lane. No special handling needed -- just note it in the status report to the user.

A degraded single-lane integrated report is **structurally canonical but unclassified**: the CLI rewrites its headings to match the merge template (`## Out-of-Scope Findings (Backlog)` emitted with the exact `None` sentinel; `## Known Backlog Issues` emitted with a `Not checked ...` sentinel, since no backlog matching ran) so downstream global merge, backlog handling, and fix workflows can consume it, but the merge/classification pass never ran. It therefore carries no cross-lane deduplication and no per-finding `Scope:` annotations, and both backlog sections reflect construction, not verification. The report includes a `## Single-Lane Degradation Notice` section recording this; surface the degradation to the user when a review falls back to single-lane, and do not backlog-append from such a report.

### Profile Selection

| Profile | Use when |
|---------|----------|
| `default` | All reviews |

Only the `default` profile is available. Always use `--template-profile default` (or omit, since it's the default). Findings budgets are judgment-based: templates report everything that clears the severity/confidence bar, most severe first, with no fixed caps.

Pass via `--template-profile <name>`. Override individual templates with `--review-template-name` or `--merge-template-name` (ref: `template-extension-spec.md` section "Template Selection Logic") -- this is also how lens templates are selected (see "Dispatch Matrix" above).

### Template Variable Injection

Pass via `--template-vars-json '<json>'`:

| Variable | Source | Purpose |
|----------|--------|---------|
| `context_seed` | Project memory, known fragile areas, recent refactors, seam digest | Give reviewers domain context |
| `lens_directive` | User's free-text focus directive | Pass through verbatim. Injecting either `lens_directive` or the deprecated alias `review_focus` now suffices: the renderer cross-populates the pair, so a directive given under one name also reaches project templates that still reference the other. Injecting both is still valid, but they must hold the same value (a mismatch is rejected) |
| `review_framework_refs` | Project review standard path | Point reviewers to project standards |
| `fix_instructions` | Fix discipline rules (only when `--fix` active) | Injected into merge and fix prompts |
| `additional_instructions` | Catch-all for extra directives | Anything that doesn't fit above |
| `known_backlog_md` | Durable backlog digest | Auto-injected AND reserved when `--backlog-path` is used (do not also pass it in template vars -- the CLI rejects the collision); skill-injected here for `custom` backlogs, where you compose the digest yourself (one `- <slug> [P2] -- <summary>` line per entry) |

Concrete example with realistic values:

```bash
multi-agent-review kickoff --wave auth-w1-0304T1422 --scope staged \
  --review-worktree auto \
  --template-vars-json '{
    "context_seed": "SessionStore was recently split into SessionManager and TokenCache. Old callers in api/ may still reference SessionStore directly.",
    "lens_directive": "session lifecycle and token expiry edge cases",
    "review_focus": "session lifecycle and token expiry edge cases",
    "review_framework_refs": "See docs/review-standard.md for project-specific criteria.",
    "additional_instructions": "Flag any error message that could leak PII or internal paths."
  }'
```

Reserved variables (`worktree`, `wave`, `scope`, `changed_files_md`, `provider_name`) are auto-injected by the CLI and cannot be overridden -- the CLI exits with an error on collision. The `global-merge` subcommand additionally reserves `input_reports_md` and `output_report_path`. `known_backlog_md` is conditionally reserved: locked in every render when `--backlog-path` computed it (on both `kickoff` and `global-merge`), caller-overridable otherwise. Optional variables default to `""` via safe-substitute (ref: `template-extension-spec.md` section "How to Inject Variables").

### Status & Debug

- Status: `multi-agent-review status --wave <name>` -- poll at reasonable intervals, report transitions.
- Debug: `multi-agent-review debug --wave <name>` -- run on lane failure, read output before deciding next steps.

## 4. Result Collection & Merge

### Artifact Directory Structure

The CLI writes artifacts under `tmp/` in the worktree (or `--output-root` if specified):

```
tmp/
├── collaborations/jobs/<wave>/   # per-lane logs, prompts, exit codes, stream data
└── reviews/
    ├── <wave>-codex.md                  # lane report (Codex)
    ├── <wave>-claude.md                 # lane report (Claude)
    ├── <wave>-integrated.md             # per-kickoff merged report
    ├── <review-slug>-seam-manifest.md   # seam manifest (partitioned reviews; skill-written)
    ├── <review-slug>-canonical.md       # canonical findings document (global merge output)
    └── <review-slug>-backlog.md         # ephemeral backlog artifact -- custom/none backlog kinds only (see below)
```

The `<review-slug>` is the shared prefix that ties one logical review's kickoffs together (see `references/partitioning-strategy.md` "Review Slug"). For single-kickoff reviews the integrated report at `tmp/reviews/<wave>-integrated.md` is the canonical findings document; for multi-kickoff reviews the global merge output is.

Every file above except `<review-slug>-seam-manifest.md` and `<review-slug>-backlog.md` is written by the CLI; those two are skill-managed artifacts (the skill writes the seam manifest during partitioning, and the backlog artifact per the backlog kind below). Do not wait on the CLI to emit the seam manifest. What happens to new out-of-scope findings after the canonical document exists depends on the resolved backlog kind (see "Backlog Discovery" in Section 1):

- **`kind: file`**: the ephemeral extraction step is RETIRED -- new out-of-scope findings are appended directly to the durable backlog file via `backlog-append` (see "Backlog Append" below); no `<review-slug>-backlog.md` is written.
- **`kind: custom`**: write `<review-slug>-backlog.md` as a local staging record (format in `references/partitioning-strategy.md` "Ephemeral Backlog Artifact"), then follow the stored instructions to push the entries to the external tracker.
- **`kind: none`**: legacy behavior -- extract the `## Out-of-Scope Findings (Backlog)` section of the canonical document into `<review-slug>-backlog.md`; that ephemeral file is the only record.

### Dual-Lane Merge

The CLI handles the per-kickoff merge automatically. After both lanes complete:

1. Check merge status via `multi-agent-review status --wave <wave>`.
2. Read the integrated report at `tmp/reviews/<wave>-integrated.md`.
3. If merge fails, run `multi-agent-review debug --wave <wave> --lane merge` and attempt manual reconciliation or re-dispatch.

### Global Merge

Whenever a review comprises more than one kickoff (any partitioned or multi-lens review), run the global merge after all kickoffs complete:

```bash
multi-agent-review global-merge --wave auth-global-w1-0304T1422 --worktree . \
  --reports tmp/reviews/authcore-w1-0304T1422-integrated.md \
            tmp/reviews/api-w1-0304T1422-integrated.md \
            tmp/reviews/seam-w1-0304T1422-integrated.md \
  --output-report tmp/reviews/auth-0304T1422-canonical.md \
  --backlog-path BACKLOG.md
```

- **Inputs**: every per-kickoff integrated report -- all (partition x lens) cells plus the seam kickoff. The CLI requires at least 2 existing report paths.
- **Mechanism**: the CLI renders `merge.global` (override via `--merge-template-name`), injecting the report list as the reserved `input_reports_md` variable, writes the prompt to `tmp/collaborations/jobs/<wave>/prompt-global-merge.txt`, and dispatches through the same lane machinery as the per-kickoff merge -- logging, watchdog, mutation guard, and report-contract validation included. Default provider is `codex`, matching the per-kickoff merge lane; `--provider claude` is available.
- **Backlog digest**: pass `--backlog-path` (or skill-inject `known_backlog_md` for `custom` backlogs) exactly as at kickoff, so the global merge can make the authoritative three-way classification.
- **The output IS the canonical findings document** -- the single user-facing deliverable of the review and the input contract for fixing.
- **Backlog disposition**: after the canonical document exists, handle its new out-of-scope findings per the resolved backlog kind -- `backlog-append` for `file` (see "Backlog Append" below), staging file + external push for `custom`, ephemeral extraction for `none` (see Section 4 "Artifact Directory Structure").
- **P0s are surfaced immediately**: a live pre-existing security hole is a headline in your user-facing summary, not a quietly filed backlog row -- and a known-backlog P0 is flagged `tracked as <slug>` at the top, not silently re-filed.
- **Single-kickoff reviews skip the global merge**: the per-kickoff integrated report is the canonical findings document (`merge.default` already classifies findings three-way and emits both backlog headings).

### Backlog Append (`kind: file` only)

After the canonical findings document exists and BEFORE presenting results:

1. Compose an entries JSON array from the `## Out-of-Scope Findings (Backlog)` section of the canonical document -- one object per NEW out-of-scope finding with `title`, `severity`, `problem`, `risk`, `fix_direction`, and `origin` set to `review <review-slug> (<date>)`. Do not include findings from `## Known Backlog Issues` (they are already tracked).
2. Write it to a temp file and run:

   ```bash
   multi-agent-review backlog-append --path <durable-backlog> \
     --entries-json <tmp-entries.json> --output json
   ```

3. The CLI appends append-only with slug dedup (duplicates are skipped and reported; re-running is a no-op). The write is serialized by an exclusive lock kept in the system temp directory, keyed by the resolved backlog path, so concurrent appends from two reviews finishing together do not lose entries. Report the appended slugs -- and any skipped duplicates -- in the user-facing summary.

### Report Format Expectations

The per-kickoff integrated report uses these exact level-2 headings (enforced by the merge template):

- `## Integrated Findings` -- deduplicated findings, P0 to P3.
- `## Explicit Disagreements` -- where lanes disagreed (or "None").
- `## Cross-lane confidence notes` -- agreement/divergence analysis.
- `## Recommended fix order` -- prioritized sequence for fixing.
- `## Out-of-Scope Findings (Backlog)` -- NEW out-of-scope findings: pre-existing issues discovered incidentally that match no known backlog entry (exactly `None` when empty). This section is the auto-append source for `file` backlogs.
- `## Known Backlog Issues` -- findings matching a known backlog entry, cited by slug. Exactly `None` when a backlog digest was provided and nothing matched; exactly `Not checked (no backlog provided)` when no digest was provided.
- `## Intent vs Behavior vs Documentation` -- alignment assessment.
- `## Residual Risks / Test Gaps` -- coverage gaps.

The canonical findings document produced by the global merge (`merge.global`) uses these exact level-2 headings:

- `## Integrated Findings`
- `## Cross-Kickoff Notes`
- `## Recommended Fix Order`
- `## Out-of-Scope Findings (Backlog)`
- `## Known Backlog Issues`
- `## Residual Risks / Test Gaps`

In both documents, every finding carries a scope annotation on its own line -- exactly one of:

- `Scope: in-scope` (introduced or exposed by the change under review)
- `Scope: out-of-scope (pre-existing)` (a pre-existing issue found incidentally, matching no known backlog entry)
- `Scope: known (backlog: <slug>)` (the same defect as a known backlog entry)

Exception -- degraded single-lane fallback: when only one lane succeeds, the integrated report is the sole lane report with its headings rewritten to match this set (it also carries `## Out-of-Scope Findings (Backlog)` set to `None`, `## Known Backlog Issues` set to a `Not checked ...` sentinel, and an extra `## Single-Lane Degradation Notice` section). No merge/classification pass ran, so its findings have no `Scope:` annotations and both backlog sections reflect construction, not verification. Treat such a report as structurally canonical but unclassified -- see Section 3 "Single-Lane Fallback"; do not backlog-append from it.

When fix mode was active, also:
- `## Fixed` -- applied fixes with commit refs.
- `## Unfixed` -- skipped findings with reasons.
- `## Test Results` -- test command and pass/fail counts.

Parse these headings to extract severity counts and finding details for the user-facing summary.

### Presenting Results

Use the deterministic `review-summarize` formatter for all result output. Never hand-format the tree. `review-summarize` is the sibling shim to `multi-agent-review`; it resolves the same way (CLI Discovery in Section 1 -- plugin `bin/`, PATH, or the `cli_path` sibling). Substitute the resolved path for `review-summarize` below.

**Steps:**

1. Read `result.json` from the job directory (`tmp/collaborations/jobs/<wave>/result.json`) to get paths and statuses.
   - Most kickoff failures still write a structured `result.json` (with a `blocker` such as `changed_files_unsafe`) before exiting. But *pre-dispatch* errors are rejected with a stderr message before the job directory exists, so no `result.json` is written -- and they do not all share one exit code. A config/usage error (an unsafe inline `--changed-files` entry, or a stale/future `config_version`) exits **2** (`ChangedFilesInputError` / `ReviewConfigError`). A bad `--review-worktree` handoff -- e.g. the provided path is not a git worktree -- is a runtime setup failure and exits **1** (`RuntimeError`). Treat **any** non-zero kickoff with no `result.json` as a pre-dispatch error to surface from stderr, not a lane failure to classify; do not assume exit 2 specifically.
2. Read the integrated report to extract severity counts (P0/P1/P2/P3) and file counts for the summary line.
3. Compose a one-line `--summary` (e.g., "Found 4 findings across 3 files (0 P0, 1 P1, 2 P2, 1 P3).") and a `--details` line (e.g., "Dual-agent review (Claude + Codex) of staged changes on main.").
4. Call the formatter:
   ```bash
   review-summarize \
     tmp/collaborations/jobs/<wave>/result.json \
     --branch <branch> \
     --worktree <review-worktree-path> \
     --consolidated tmp/reviews/<wave>-consolidated.md \
     --summary "<summary>" \
     --details "<details>"
   ```
   Add `--fix` flag when fix mode was active.
5. Print the formatter's stdout verbatim. The formatter also writes the consolidated Markdown report.

For reviews spanning multiple kickoffs -- several partitions, several lenses, several waves, or any combination -- pass all result.json files as positional args (one per kickoff, in order). When a global merge ran, the canonical findings document (the `global-merge --output-report` path) is the findings artifact to present; extract severity counts from it, not from the per-kickoff reports it supersedes.

**Output hierarchy** (absolute paths everywhere, Cmd+Click navigable):
- Summary + details on top
- `Findings:` pointing to consolidated report
- `Branch:` and `Worktree:` (review worktree, always shown)
- `Wave N:` per wave, with nested Review/Changes/Agents
- Failed agents show `FAILED -- <reason>` instead of a path

Communication contract: always tell the user how many findings, severity distribution, and what was reviewed. Never present findings without this framing.

## 5. Fix Coordination

Fix mode runs ONLY on explicit user request -- `--fix`, "review and fix", "fix the findings", "fix these findings". Never fix by default.

### Input Contract

Fixing consumes a canonical findings document: the one produced by the review just completed, a prior review's, the durable backlog itself (or a slug subset of it -- "fix materialization-path-sanitization and review-worktree-leak-on-abnormal-exit"), or -- for `custom`/`none` backlog kinds -- an ephemeral `<review-slug>-backlog.md` artifact. "Fix a series of issues relative to a scope of work" is therefore a general entry point of this skill -- the artifact contract, not a separate skill, creates the capability. Never fix from unmerged lane reports.

### Prerequisites

1. Run the commit capability preflight in the fix worktree (see Section 1). If it fails, follow the three-option flow (review-only / abort / diagnose).
2. Ensure the findings artifact exists and is a merged document (per-kickoff integrated report, canonical findings document, or backlog).

### Serial Fix Pipeline (default)

Run ONE fix pipeline over the merged, priority-ordered finding list, applied serially on a single integration worktree:

```bash
# 1. Create integration branch off HEAD
git -C "$MAIN_WT" branch review-fix-auth-w1-0304T1422 HEAD
# 2. Create the integration worktree -- the one worktree all serial fixes land on
git -C "$MAIN_WT" worktree add "$WORKTREE_DIR/review-fix-auth-w1-0304T1422" review-fix-auth-w1-0304T1422
# 3. Dispatch fixer agents against it, one finding (or small batch) at a time
```

- **Serial does not mean one decaying context.** Dispatch a SEQUENCE of fresh fixer agents -- one per finding or small batch -- each handed the cumulative what-has-changed state: findings addressed so far, files touched, commits made.
- **Every fixer re-validates its finding first.** Findings were produced against the pre-fix snapshot; fixes 1..k-1 may have mooted, moved, or aggravated finding k. The fixer checks the finding against the CURRENT worktree state before changing anything, and reports a mooted finding as such rather than "fixing" stale code.
- **Core invariant (unchanged):** the invoking session never moves to a fix worktree. Fix worktrees are created and used exclusively by delegated agents.

Rationale for accepting serial cost: fixes are cheap relative to reviews, the finding count is bounded, and serial-on-one-worktree removes fixer-branch integration, the cross-lane coordinator file, and merge-conflict resolution from the default path.

### Parallel Fixing (provably decoupled groups only)

Parallel fixing is permitted only for finding groups that are provably decoupled: **disjoint file sets AND no seam-manifest edge between the groups**. The seam manifest, already in hand from partitioning, is the decision input (rule details in `references/partitioning-strategy.md`). Disjoint files alone do not prove safety -- fixer A can change a contract fixer B's fix silently relies on; semantic fix conflicts are the seam phenomenon again. When fixing from an artifact with no accompanying seam manifest, default to serial.

### Escalation Valve: Multi-Fixer Branches

For genuinely huge fix volumes, the multi-fixer branch topology survives as a documented escalation valve -- not the default path. Each fixer gets its own branch and worktree off the integration branch, with lane-scope suffixes (`typing`, `tests`, `perf`; this fixer split is not a "partition" in the Terminology sense -- partitions split review scope, fixer lane scopes split findings within one wave), cross-lane issues routed to a coordinator file via `$cross_lane_issues_path`, and an integration agent merging fixer branches afterward. Full topology, naming, and integration flows: `references/fix-worktree-pattern.md`.

### Commit Discipline

- One fix per commit.
- Commit message format: `fix(<scope>): <what> [review-<wave>]`.
- Shared resources (lock files, CI config, generated files) get separate commits.
- Never batch unrelated fixes into a single commit.

### Fix Constraints

Inject fix boundaries via `$fix_instructions`. Construct from `fix-discipline.md` core rules (see section "Template Variable"): lane isolation, scope limits, commit format, shared resource handling, test policy. When fix mode is inactive, set to `""` or omit.

### Completion

In the serial default, there is no integration step: fixes already sit on the integration branch, one commit each. The integration worktree survives for user inspection; report the fix branch name to the user.

When the multi-fixer escalation valve was used, merge each fixer branch into the integration branch sequentially (ref: `fix-worktree-pattern.md` section "Flow 1" / "Flow 2"). On conflict, the integration agent resolves by understanding fix intent; if fixes are semantically incompatible, revert the conflicting commit and report it as unfixed. After a successful merge, remove fixer worktrees and branches (always from the main worktree, never from inside them).

### Unfixed Items

Unfixed items are first-class output, not failures (ref: `fix-discipline.md` section "Unfixed Items"). For each skipped finding, document:

- Finding ID and severity.
- Reason skipped: one of `out of lane scope` | `too architectural` | `low confidence` | `security-sensitive` | `risky blast radius` | `would break tests`.
- Recommended follow-up: `another wave` | `manual fix` | `dedicated cleanup session` | `punt to user`.

The fixer agent's output includes structured `## Unfixed` and `## Fixed` sections. Collect these into the wave report at `tmp/reviews/<wave>/`. Do not silently drop findings that could not be fixed -- a finding that goes unfixed without a documented reason is a gap, not a resolution.

## 6. Iterative Convergence

For multi-wave reviews where findings persist after fixes.

### Wave Mechanics

Each wave is a complete fresh `kickoff` invocation:

- Fresh context, fresh agents (no accumulated context decay). DDI research: 60-80% of debugging capability lost within 2-3 iterations in the same context (ref: `convergence-evidence.md` "Debugging Decay").
- Wave-seed template feeds previous state: prior findings, applied fixes, unfixed items, regression watch list.
- Scope narrows: wave N reviews only files changed by wave N-1 fixes plus unfixed items.

### Convergence Decision Rules

Read the reviewer's convergence recommendation from the merged report, then apply the quantitative rules below. Reference: `references/convergence-evidence.md` "Convergence Decision Rules" table.

| Condition | Action |
|-----------|--------|
| No P0/P1 remaining | **Stop** (default goal) |
| No new findings at target severity | **Stop** (diminishing returns) |
| Fix success rate declining wave-over-wave | **Stop** (DDI intervention point) |
| Wave 3 completed | **Stop** (hard cap -- effectiveness exhausted) |
| User overrides target severity | Continue to user-specified level |

Target severity adapts to user intent: default is P0/P1, but if user says "fix everything including P2", iterate until that level is clear or the hard cap is reached.

### Scope Narrowing

Compute the narrowed file set for wave N+1:

1. Run `git diff --name-only <integration-branch>..HEAD` to find files changed by wave N fixes.
2. Add files with unfixed findings from the wave N report.
3. Remove files with no remaining findings and no recent changes.
4. Pass the narrowed file list via `--changed-files-path` to the next wave.

Example: wave 1 reviewed 15 files, fixes touched 4 files. Wave 2 scope = those 4 + any files with unfixed P1 items = 6 files total.

### Wave Seed Assembly

Build the context seed document at `tmp/reviews/<wave>/context-seed.md`. The schema is defined in `references/fix-worktree-pattern.md` "Context Seed Schema". Steps:

1. Read the merged report from wave N. Extract all findings with severity and fix status.
2. Read the fix manifest for applied fixes and unfixed items with reasons.
3. Populate the four required sections (all must be present; use `(none)` for empty):
   - **Previous Findings Summary**: `- **[P<n>]** <desc> -- <file> -- Status: Fixed | Unfixed | Partial`
   - **Fixes Applied**: one H3 per fix with file, branch, commits, summary fields
   - **Unfixed Items**: one H3 per item with file, reason, context fields
   - **Regression Watch**: bulleted list of behaviors to verify, with file/test paths
4. Template variables map 1:1 to sections: `$previous_findings_summary`, `$fixes_applied`, `$unfixed_items`, `$regression_watch` each contain the body text of the corresponding section.

## 7. Failure Handling

The CLI handles mechanical retries (timeouts, transient errors). The skill handles judgment calls AFTER CLI retry exhaustion.

Reference: `references/failure-classification.md` for the full 20 reason-code decision tree.

### Failure Categories

**Transient** (timeout, stall, stream limit):
- CLI retries automatically.
- If CLI exhausts retries: adjust parameters (reduce scope, increase timeout) and retry once.

**Structural** (missing binary, config error, auth failure):
- Report to user with specific error details.
- Do not retry -- these require user intervention.

**Judgment** (contract failure, worktree mutation, partial output):
- Assess whether partial output is salvageable.
- If salvageable: extract usable findings, note gaps in report.
- If not salvageable: retry once with adjusted parameters.
- If retry also fails: escalate to user with full diagnostic.

Key judgment reason codes -- see `failure-classification.md` "Judgment calls" for full details:
- **`report_contract_failed`** (exit 11): extract raw content if structurally close; retry once if malformed. Never silently discard.
- **`worktree_modified`** (exit 127): never retry same prompt. Check for "fingerprint unavailable" false positive.
- **`no_result_event`** (exit 10): check output stream for partial content before retrying.

### Debug Output

Run `multi-agent-review debug --wave <name>` after any failure. Key signals: reason code (determines decision branch), log tail error patterns, stream byte count > 0 (agent produced output before failing).

### MCP Fallback

When a failure involves MCP (reason codes `mcp_failure` or `mcp_discovery_failed`), retry with `--mcp-mode disable-all`. The CLI's `mcp_mode=auto` preflight handles this automatically for most cases, but if that fallback also failed, an explicit override is needed. Do not retry with the same MCP config.

### Graceful Degradation

Degrade in steps, not all-at-once:

1. **Both lanes** (normal operation).
2. **Single lane** (one lane failed, proceed with the other).
3. **Manual prompt** (both lanes failed -- render the review prompt for the user to run manually).

### Status Transparency

Never silently retry. Report status using these levels:

| Status | Meaning |
|--------|---------|
| `RUNNING` | Normal operation |
| `RETRYING` | A retry is in progress (state what failed and why) |
| `DEGRADED` | Operating at reduced capability (state what's missing) |
| `BLOCKED` | Cannot proceed without user action (state what's needed) |

## 8. Communication Contract

### Startup

The first 30 seconds should tell the user enough to walk away or stay. Deliver immediately after scope resolution: what is being reviewed (scope, file count, LOC estimate), lane configuration (dual/single, providers), and estimated complexity.

Example: "Reviewing staged changes: 7 files, ~340 LOC. Dual-lane (Claude + Codex), default profile." Adapt for degraded (single-lane with reason) or blocked (both failed with exit codes and next steps).

### During Review

Status updates at milestones: lanes launched, first/both lanes complete, merge done, fix started/complete. Do not poll excessively or go silent.

### Results

Present results using the hierarchical format from Section 4 "Presenting Results". Always call the resolved `review-summarize` formatter -- do not hand-format the tree. The formatter reads `result.json` and produces deterministic, Cmd+Click navigable output.

### Errors

Always include:
- What failed (specific phase, lane, step).
- What was tried (retries, fallbacks).
- What the user can do (specific next steps or commands).

## 9. References

Detailed specifications live in the `references/` subdirectory. Load on demand, not upfront.

| Reference | Contents | When to load |
|-----------|----------|--------------|
| `help.md` | Help-mode dispatch: topic routing, repo-aware branches (missing config, stale `config_version`, `help lenses`, backlog explainer), user-guide path resolution | In help mode / onboarding (Section 0) |
| `partitioning-strategy.md` | Logical clustering procedure, seam manifest schema, seam digest format, canonical findings document contract, backlog format, fix-partitioning decision rule | When partitioning a large review, building the seam kickoff, running the global merge, or deciding fix topology |
| `template-extension-spec.md` | Template variable interface, injection patterns, safe-substitute behavior, lens catalog schema and overlay semantics | When constructing template variables, authoring lenses, or debugging variable injection |
| `failure-classification.md` | 20 reason codes, retry/report/adapt decision tree | On any lane failure after CLI retry exhaustion |
| `convergence-evidence.md` | DDI research data, empirical convergence thresholds | When deciding whether to launch another wave |
| `fix-discipline.md` | Lane isolation rules, shared resource handling, commit patterns | When fix mode is active |
| `fix-worktree-pattern.md` | Multi-fixer branch topology, naming conventions, manifest format, integration flows -- the ESCALATION VALVE for huge fix volumes, not the serial default (Section 5) | When the multi-fixer escalation valve is invoked, or building a wave seed |
| `fix-worktree-walkthrough.md` | Step-by-step two-wave scenario for the multi-fixer ESCALATION VALVE (concrete commands, manifests, artifact snapshots); not the serial default | When debugging multi-fixer escalation-valve flow or onboarding to the fix lifecycle |
| `agent-adapters.md` | Agent capabilities, limitations, dispatch patterns per provider | When selecting agents, tuning watchdog parameters, or debugging agent-specific failures |
