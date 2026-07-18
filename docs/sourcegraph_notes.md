# Sourcegraph cross-engine coverage check for `SKILL.md`

Snapshot date: **2026-07-18**
Source engine: **Sourcegraph public code search** (`sourcegraph.com`), anonymous access.

## API and query

Streaming search API (Server-Sent Events):

```
GET https://sourcegraph.com/.api/search/stream?q=<url-encoded-query>
Header: Accept: text/event-stream
```

Two queries were run with `curl` + `python3` (no `requests`):

1. **Sample / cap-probe query**
   `file:(^|/)SKILL\.md$ count:5000 type:file`
   Returned 5000 `path`-type matches, then the stream reported
   `skipped: shard-match-limit "result limit hit"` — i.e. the `count:5000`
   cap was hit, so this query only proves there are **>= 5000** matches.

2. **Total-estimate query**
   `file:(^|/)SKILL\.md$ count:all type:file select:file`
   The final `progress` event with `done:true` reported
   **`matchCount = 750266`** (durationMs ~24s, ~334 MB stream).

The SSE stream was parsed by splitting on blank lines into events; `event: matches`
blocks carry a JSON array of match objects (keys: `type`, `path`, `repository`,
`repoStars`, `branches`, `commit`, `language`, ...). `event: progress` /
`event: filters` / `event: done` carry counts.

## Result counts

- **Sourcegraph raw estimate (`count:all`): 750,266 path matches** for the
  regex `(^|/)SKILL\.md$`.
- **IMPORTANT — case sensitivity:** Sourcegraph regex file filters are
  **case-insensitive by default**, so the 750,266 figure includes case variants.
  Basename breakdown of the returned matches:
  - `SKILL.md` (exact): **746,565**
  - `skill.md`: 3,499
  - `Skill.md`: 153
  - `SKILL.MD`: 47
  - other (`SKill.md`, `Skill.MD`): 2
- **Exact-basename `SKILL.md` total: 746,565**, spread across only
  **18,521 distinct repositories**.

### The exact count is heavily inflated by aggregator/registry repos

The 746,565 figure is NOT ~746k independent skills. A handful of "skill registry"
/ mirror / awesome-list repos each vendor tens or hundreds of thousands of
`SKILL.md` files. Top offenders:

| SKILL.md files | repo |
|---:|---|
| 203,634 | github.com/majiayu000/claude-skill-registry |
| 99,152 | github.com/NeverSight/learn-skills.dev |
| 69,600 | github.com/openclaw/skills |
| 26,226 | github.com/Klotzkette/claude-fuer-deutsches-recht |
| 16,755 | github.com/diegosouzapw/awesome-omni-skill |
| 12,424 | github.com/ComeOnOliver/skillshub |
| 10,504 | github.com/lingxling/awesome-skills-cn |

- Repos with **exactly 1** `SKILL.md`: 6,975
- Repos with **>100** `SKILL.md`: 379 (these ~2% of repos produce the vast
  majority of the file count)
- **Median `SKILL.md` files per repo: 3**

So the more meaningful coverage signals are the **distinct-repo count (~18.5k)**
and the median-of-3, not the raw file count.

## Host / code-host breakdown

Of the 746,565 exact `SKILL.md` matches:

- **github.com: 746,560**
- **gitlab.com: 5** (in 3 repos: `gitlab-org/gitlab`, `gitlab-org/gitaly`,
  `gitlab-org/api/client-go` — incidental, not skill-ecosystem repos)
- other hosts: 0 visible.

Sourcegraph's public index is essentially GitHub for this query; GitLab and other
hosts are negligible.

## Sample captured

- File: `sourcegraph_sample.jsonl`
- **8,000 records**, one JSON object per match:
  `{"platform","repo","path","html_url","source":"sourcegraph","snapshot_date":"2026-07-18"}`.
  Only exact basename `SKILL.md` is included.
- To avoid the sample being swallowed by the few mega-registry repos, matches were
  **capped at 3 paths per repository** (stream order preserved). The sample
  therefore spans **4,119 distinct repositories**.
- All 5 gitlab.com matches are force-included; breakdown: github 7,995 / gitlab 5.
- `html_url` is synthesized (`https://<repo>/blob/<branch>/<path>`, GitLab uses
  `/-/blob/`). Branch is often empty in the stream (default branch) and is
  rendered as `HEAD`; these URLs are constructed, not returned verbatim by
  Sourcegraph, and were not fetched/verified.

## Limitations

1. **Partial index.** Sourcegraph's public code search indexes only a subset of
   public repositories (popular / opted-in / crawled), not all of GitHub. Its
   totals are a lower bound on true public prevalence and are biased toward
   higher-star repos.
2. **By default excludes forks and archived repos.** The stream reported
   `280 forked` and `92k archived` repositories skipped. Including them
   (`fork:yes archived:yes`) would raise counts further; they were intentionally
   excluded to match typical "primary public repo" coverage.
3. **Case-insensitive matching** inflates the regex total; exact `SKILL.md` was
   isolated by post-filtering basenames (see above).
4. **Aggregator inflation.** File-level counts are dominated by a few registry
   repos; per-file totals overstate distinct-skill coverage by ~40x relative to
   distinct repos.
5. **Cap behavior.** `count:5000` hits a shard match limit; `count:all` was
   required for a full estimate. The `count:all` run was a single ~334 MB
   response — reproducible but heavy.
6. **Anonymous access worked** (HTTP 200, no auth); no rate-limiting was
   encountered across the 2 requests made. No GitHub API / `gh` was used.

## Cross-engine coverage comparison (qualitative)

Sourcegraph independently confirms that `SKILL.md` is a widespread convention:
**~18.5k distinct public repos** contain at least one exact `SKILL.md`, with a raw
file count of ~746k dominated by a small number of aggregator repos. For a
per-repo (deduplicated-skill) coverage measure, the ~18.5k distinct-repo figure is
the number to compare against the primary GitHub-based corpus. Because Sourcegraph
indexes only a subset of public repos and excludes forks/archived by default, its
repo count is a **lower bound**; agreement at the repo level would indicate good
cross-engine coverage, while the raw 746k file count should be treated as an
upper-bound artifact of registry/vendoring inflation rather than a true skill
population.
