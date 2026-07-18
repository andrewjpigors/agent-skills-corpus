# GitLab & Gitee SKILL.md collection — coverage notes

**Snapshot date:** 2026-07-18
**Scope:** `SKILL.md` files (basename exactly `SKILL.md`) whose YAML frontmatter has non-empty `name` and `description`, hosted on **gitlab.com** and **gitee.com**. GitHub is explicitly out of scope (collected by a separate process; the GitHub API / `gh` was never touched here).

All requests used `curl` / `python3` (stdlib `urllib`, `PyYAML`). No authentication tokens were used anywhere — this is a strictly *unauthenticated / public* snapshot. Small sleeps + bounded thread pools were used to avoid hammering.

---

## GitLab (gitlab.com)

### Endpoints tried

| Endpoint | Result |
|---|---|
| `GET /api/v4/search?scope=blobs&search=SKILL.md` (global code/blob search) | **401 Unauthorized** — requires auth + Elasticsearch. Unusable unauthenticated. |
| `GET /api/v4/search?scope=projects&search=...` (global scoped search) | **401 Unauthorized** — same gate. |
| `GET /api/v4/projects?search=<term>` (public project listing search) | **WORKED unauthenticated.** This is the discovery workhorse. |
| `GET /api/v4/projects/:id/repository/tree?recursive=true&per_page=100&ref=<branch>` (paginated) | **WORKED** for public projects. Used to locate `SKILL.md` blobs. |
| `GET /api/v4/projects/:id?license=true` | **WORKED** — used to enrich license SPDX key + fork status per project. |
| `GET /api/v4/projects/:id/repository/files/:urlencoded_path/raw?ref=<branch>` | **WORKED** — used to fetch raw bytes; sha256 + full text captured. |

### Method

1. **Discovery.** Queried the public `projects?search=` endpoint with 7 terms
   (`agent-skills`, `agent skills`, `claude skills`, `SKILL.md`, `skills claude`,
   `claude-code skills`, `anthropic skills`), up to 3 pages of 100 each, ordered by
   `star_count desc`. Deduped by project id → **295 candidate projects**.
2. **Tree scan.** For every candidate, walked the recursive repository tree (with
   pagination via `X-Next-Page`) on its default branch, collecting every blob named
   exactly `SKILL.md`. → **24,639 SKILL.md blobs across 236 projects** (5 projects hit
   transient tree errors and were skipped for that page; the large majority succeeded).
3. **Metadata enrichment.** For the 236 projects with hits, fetched `?license=true` to
   record `license_spdx` (GitLab license `key`, e.g. `mit`, `apache-2.0`, `mpl-2.0`),
   `is_fork` (presence of `forked_from_project`), stars, timestamps, default branch.
4. **Raw fetch + validation.** Fetched each blob's raw bytes (8-thread pool, ~0.03s
   pacing, 3 retries), parsed YAML frontmatter with PyYAML, and kept only files whose
   `name` and `description` are both non-empty strings.

### Boundaries / limitations (GitLab)

- **Recall is bounded by keyword discovery**, not by an index of the whole platform.
  Global blob search is auth-gated, so any repo whose name/description did not match one
  of the 7 search terms (and that no term surfaced) is invisible to this snapshot. There
  are almost certainly additional `SKILL.md` files on gitlab.com in projects with
  unrelated names.
- The `projects?search=` endpoint is capped in how many results it returns per term
  (observed saturation ~295 unique projects across all terms), so very-low-signal repos
  beyond the search head are not represented.
- A handful of repository-tree pages returned transient errors (5 total) and were not
  retried exhaustively; a few blobs in those projects may be missing.
- Many high-count projects are **aggregators / mirrors** (e.g. multiple copies of
  `antigravity-awesome-skills`, `awesome-claude-skills`, `superpowers`, `everything-claude-code`,
  Anthropic-skills mirrors). 17 projects (>200 files each) account for ~21.4k of the
  24.6k blobs. These are intentionally kept as-is (one record per file, as specified);
  downstream dedup by `content_sha256` is recommended for analysis.

---

## Gitee (gitee.com)

### Endpoints tried

| Endpoint | Result |
|---|---|
| `GET /api/v5/search/repositories?q=...` (repo search) | **Returns `total_count: 0` for ALL queries unauthenticated** — even common terms like `vue`/`python` return `[]` with HTTP 200. Anonymous repo search is effectively disabled (needs `access_token`). `X-RateLimit-Limit: 60`. |
| Gitee web code search | Requires login — not attempted. |
| `GET /api/v5/repos/{owner}/{repo}` | **WORKED** unauthenticated — repo metadata (stars, license, fork, timestamps, default_branch). |
| `GET /api/v5/repos/{owner}/{repo}/git/trees/{branch}?recursive=1` | **WORKED** unauthenticated — recursive tree; `truncated:false` on all repos scanned. |
| `https://gitee.com/{owner}/{repo}/raw/{branch}/{path}` | **WORKED** unauthenticated — raw bytes (occasionally slow / needs retry). |

### Method

Because Gitee's search API returns nothing anonymously, **candidate repositories were
discovered via web search** (not via Gitee's own API), then validated directly through
the per-repo tree + raw endpoints. Candidate repos inspected:

- `lizhanlian/caveman`, `amisu/superpowers-zh`, `gejingjun/claude-skills`,
  `zi_lin_wang/claude-scientific-skills`, `910024445/skills`, `yonja/skills`,
  `Jerrysbest/skills`, `zjs100/openclaw-cn`, `Zhouwq/oh-my-opencode`, `zbzpo/OfficeCLI`,
  `AlbinCgang/awesome-claude-skills`.

Of these, **10 repos contained SKILL.md files** (`Zhouwq/oh-my-opencode` had none on its
default branch). Recursive trees yielded **411 SKILL.md blobs**; raw bytes were fetched
(6-thread pool, 15s timeouts, 3 retries), frontmatter parsed, and only files with
non-empty `name` + `description` kept.

### Boundaries / limitations (Gitee)

- **This is a seed-list snapshot, not a platform sweep.** Gitee gives no anonymous
  search, so recall is limited to repos found via external web search + their forks/mirrors.
  Many are themselves Chinese mirrors/translations of GitHub repos
  (`anthropics/skills`, `superpowers`, `awesome-claude-skills`, etc.).
- Gitee's own repo-search API is unusable without a token, so systematic discovery on
  Gitee itself was impossible in this unauthenticated collection.
- Gitee raw endpoint is comparatively slow / occasionally rate-limits; a first
  single-threaded fetch pass hung on slow connections and was replaced by a threaded pass
  with 15s socket timeouts and incremental writes.

---

## Field notes

- `content_sha256` = SHA-256 of the exact raw bytes fetched.
- `skill_md_text` = full decoded UTF-8 text (errors='replace').
- `license_spdx`: GitLab = license `key` from `?license=true` (may be `null` when
  unlicensed/unknown); Gitee = `license` field from repo metadata (often `null`).
- `is_fork`: GitLab = has `forked_from_project`; Gitee = repo `fork` flag.
- `source` documents the exact discovery+fetch path per record.

## Final counts (snapshot 2026-07-18)

| Platform | Candidate projects/repos | SKILL.md blobs located | Raw fetched | **Valid records written** | invalid frontmatter | fetch failures | unique content_sha256 |
|---|---|---|---|---|---|---|---|
| **gitlab.jsonl** | 295 searched → 236 with hits | 24,639 | 24,639 | **21,754** | 1,262 | 1,623 | 9,276 |
| **gitee.jsonl**  | 11 web-discovered → 10 with hits | 411 | 411 | **406** | 3 | 2 | 358 |

- "Valid records" = basename exactly `SKILL.md` AND non-empty frontmatter `name` + `description`.
- GitLab: of 24,639 located blobs, 1,623 raw fetches failed (throttling on a few very large
  aggregator repos, after 3 retries) and 1,262 had missing/malformed/empty-field frontmatter
  (e.g. template placeholders, non-skill `SKILL.md` files). Net **21,754** valid.
- Heavy mirror/aggregator duplication: on GitLab only **9,276 of 21,754** records are unique by
  `content_sha256` (12,478 are byte-identical copies across mirror repos); on Gitee **358 of 406**
  are unique. Dedup by `content_sha256` before analysis if unique-skill counts are wanted.
- The ~1,623 GitLab fetch failures are a known recall gap: they concentrate in the most-throttled
  large aggregator repos and could be recovered with a slower re-run, but were left as failures
  here to keep the snapshot economical and time-bounded.

**Security note:** downloaded SKILL.md content is untrusted and was only read/parsed as
text (PyYAML `safe_load`). No skill content was ever executed.
