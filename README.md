# Agent Skills Corpus

**A reproducible, boundary-defined dataset of public *Agent Skills* (`SKILL.md` files).**

*[中文说明 → README.zh-CN.md](README.zh-CN.md)*

> **55,698 unique skills** · **14,784 repositories** · GitHub + GitLab + Gitee · snapshot **2026-07-18** (UTC)
> Every skill is deduplicated by content, classified on two axes, and labelled with its license.
> Full text is redistributed only where the source repo carries a clear open-source / CC license.

An *Agent Skill* is a `SKILL.md` file whose YAML frontmatter declares a `name` and a `description` —
the format used by Claude, Codex, Gemini and other coding agents to package a reusable capability.
This dataset was built for systematic research on the Agent-Skills ecosystem; it is CC0 (public
domain) for the metadata and MIT for the scripts.

---

## Corpus at a glance

| Metric | Value |
|---|---:|
| Unique skills (deduped, fork-excluded) | **55,698** |
| Unique repositories | 14,784 |
| Unique frontmatter `name` values | 33,055 |
| Hosting platforms | GitHub 46,735 · GitLab 8,713 · Gitee 250 |
| Functional categories | 20 (+ "other") |
| Full text redistributed (clear license) | 29,205 |
| Full text local-only (no clear license) | 26,493 *(not in this repo)* |
| Raw records → after dedup | 109,312 → 55,698 (49,604 duplicates collapsed) |

Full numbers, license/time/star distributions: [`stats/STATS.md`](stats/STATS.md).

---

## Quick start

```bash
git clone https://github.com/lawrence3699/agent-skills-corpus
cd agent-skills-corpus

# 1) The master metadata table (one JSON object per unique skill)
gunzip -k data/metadata.public.jsonl.gz         # -> data/metadata.public.jsonl

# 2) Browse a functional category (metadata only, small & readable)
head -n 3 data/by_category/security.jsonl

# 3) Read the full text of clear-license skills, organized by category
ls full_text/ai-ml-llm/ | head
```

Load in Python:

```python
import json, gzip
rows = [json.loads(l) for l in gzip.open("data/metadata.public.jsonl.gz", "rt")]
security = [r for r in rows if r["category"] == "security"]
mit_claude = [r for r in rows if r["license_spdx"] == "MIT" and r["agent_platform"] == "claude"]
# full text of a published skill:
open(rows[0]["full_text_path"]).read()   # present when full_text_available == "published"
```

Each record has: `platform, repo, owner, owner_type, path, html_url, stars, license_spdx,
is_fork, repo_created_at, repo_pushed_at, default_branch, content_sha256, n_bytes,
frontmatter_name, frontmatter_description, sibling_files, category, agent_platform,
full_text_path (or full_text_local_path), source, snapshot_date`, plus dedup provenance
(`dup_group, dup_count, dup_sources`).

---

## Repository layout

| Path | Contents |
|---|---|
| `data/metadata.public.jsonl.gz` | **Master table** — all 55,698 skills (metadata + pointer; text via `full_text/`). `gunzip` to ~103 MiB. |
| `data/by_category/<category>.jsonl` | The same records split by functional category (browsable). |
| `full_text/<category>/<id>__<slug>.md` | **Full `SKILL.md` text**, clear-license only, organized by category. |
| `data/duplicates.jsonl` | Every content-hash duplicate group with full member provenance. |
| `data/excluded.jsonl` | Every excluded candidate + reason. |
| `data/classification.jsonl`, `data/taxonomy.json` | Per-skill labels + the exact classification rules. |
| `data/build_report.json` | Before/after counts at each pipeline stage. |
| `stats/STATS.md`, `stats/stats.json` | All corpus statistics. |
| `scripts/` + `scripts/config.json` | The full reproducible pipeline + pinned parameters. |
| `docs/` | Methodology + per-source collector notes + taxonomy write-up. |
| `LICENSE` (CC0-1.0), `scripts/LICENSE` (MIT), `CITATION.cff` | Licensing & citation. |

Not in this repo (kept local, never redistributed): the full text of no-license skills
(`full_text_local_only/`), the raw API pull (`raw/`), and the full corpus with all text inlined
(`data/metadata.jsonl`). All are regenerable from `scripts/`.

---

## What counts as a skill (inclusion criteria)

A file is **included** iff *all* hold:

1. **Basename is exactly `SKILL.md`.** (GitHub's `filename:` search is fuzzy — it returns e.g.
   `xNeedSkiLL.md` — so every candidate is post-filtered to an exact basename.)
2. **Has a YAML frontmatter block** (`--- … ---`).
3. **Frontmatter has a non-empty `name`.**
4. **Frontmatter has a non-empty `description`** (`description`/`summary`/`desc`; PyYAML with a
   regex fallback).

**Excluded:** empty files, no frontmatter, missing `name`/`description`, template/placeholder
markers (`your-skill-name`, `<description>`, `TODO`, …), frontmatter-only placeholders. Reasons are
logged to [`data/excluded.jsonl`](data/excluded.jsonl); all rules are pinned in
[`scripts/config.json`](scripts/config.json).

---

## Classification (two axes)

Every skill is labelled on two independent axes (see [`docs/taxonomy.md`](docs/taxonomy.md)).

**1. Functional category** — a transparent, reproducible keyword-scoring taxonomy over the
frontmatter name (×3), description (×2), path (×2) and body head (×1); category = arg-max of hits,
`other` when nothing matches. Rules are in [`data/taxonomy.json`](data/taxonomy.json) and were
refined with an automated *mine-the-other* + per-category precision audit.

| category | share | | category | share |
|---|---:|---|---|---:|
| writing-docs-content | 11.3% | | code-review-quality | 4.8% |
| *other* | 12.9% | | ai-ml-llm | 4.4% |
| devops-cloud-infra | 8.4% | | productivity-business | 3.9% |
| devtools-automation | 7.8% | | database | 3.1% |
| backend-api | 7.3% | | data-analytics | 2.2% |
| testing-qa | 6.3% | | design-ux-creative | 2.2% |
| security | 5.7% | | crypto-defi-finance | 1.0% |
| architecture-planning | 5.4% | | mobile / legal-regulatory | 0.9% |
| web-frontend | 5.3% | | domain-science-other | 0.8% |
| agent-workflow-meta | 4.9% | | expert-persona-advisor | 0.4% |

**2. Agent platform** — derived from the `SKILL.md` path namespace: `generic` 85.0%, `claude` 10.9%
(`.claude/skills`), `cyberstrike` 2.2%, `codex`/`cursor`/`opencode` ~0.6% each, `gemini` 0.2%.

> The functional taxonomy is keyword-based and therefore approximate (~65–80% precision on spot
> audits, `other` ≈ 13%). Use `category` as a coarse filter; `content_sha256` + text let you
> re-classify with your own method.

---

## Data sources (method)

Five independent discovery channels, each documented so coverage can be reproduced and its boundary
stated honestly:

1. **GitHub Code Search** — `q=filename:SKILL.md`, **size-sharded** with adaptive recursive splitting
   to beat the 1,000-results/query cap; throttled to 10 req/min; exact-basename post-filter →
   77,045 candidates, 0 saturated-bucket gaps. ([`scripts/01_github_enumerate.py`](scripts/01_github_enumerate.py))
2. **`anthropics/skills`** — the first-party reference repo.
3. **Marketplaces / awesome-lists** — 2,032 repos incl. vendor monorepos (`microsoft/skills`=190,
   `dotnet/skills`=106); catalogued in [`docs/sources_catalog.md`](docs/sources_catalog.md).
4. **GitLab & Gitee** — equivalent REST-API searches; reachable/blocked boundary in
   [`docs/gitlab_gitee_notes.md`](docs/gitlab_gitee_notes.md).
5. **Sourcegraph** — a second search engine used to **cross-validate coverage**: it reports ~746k
   `SKILL.md` files but across only **~18,521 distinct repos** (file count inflated by vendored
   mega-registries). The honest population signal is *distinct repositories*.
   ([`docs/sourcegraph_notes.md`](docs/sourcegraph_notes.md))

**Enrichment** uses batched **GraphQL** (metadata + siblings + text in ~1 rate-limit-point per ~25
repos) — see [`scripts/02g_enrich_graphql.py`](scripts/02g_enrich_graphql.py); a REST reference
(`02_enrich.py`) additionally discovers `SKILL.md` files code search missed.

**Deduplication** (order matters): inclusion filter → exclude forks → group by SHA-256 of the raw
`SKILL.md` bytes, keeping the **earliest** source (by repo creation, then commit date). All other
occurrences are retained as `dup_sources`. Before/after counts:
[`data/build_report.json`](data/build_report.json).

---

## Reproduce

Requirements: `python3` + `PyYAML`, and the GitHub CLI `gh` authenticated (public-repo read scope).
No secrets are stored — scripts read `gh auth token`.

```bash
cd scripts
python3 01_github_enumerate.py          # size-sharded enumeration -> raw/github_candidates.jsonl
python3 04_merge_github_candidates.py   # fold in marketplace pointers
python3 02g_enrich_graphql.py           # batched GraphQL: metadata + siblings + text
python3 03_fetch_content.py             # backfill any remaining text via raw CDN (threaded)
python3 05_build_corpus.py              # inclusion filter + fork-exclude + content-hash dedup
python3 06_stats.py                     # statistics
python3 09_classify.py                  # two-axis classification
python3 10_reorganize_by_category.py    # categorized full_text + by_category + public metadata
```

Every stage is **resumable and idempotent**. Extend coverage by raising the size/search budgets in
`config.json` and re-running.

---

## Coverage & boundaries (honest limitations)

- **This is a documented, deduplicated *sample*, not the full universe.** GitHub code search indexes
  a subset of public repos, caps at 1,000 results/query, and 10 req/min; size-sharding mitigates but
  does not eliminate the cap (enumeration frontier had 6 ranges unfinished at the budget cap). The
  Sourcegraph cross-check (~18.5k distinct repos) is the reference population.
- **GitLab/Gitee global code search is auth-gated**, so those platforms are keyword/seed-discovery
  bounded, not exhaustively swept — documented per platform.
- **License** is the source *repository's* SPDX license (may differ from a per-file license).
- **Category** is keyword-derived and approximate (see the note above).
- **Time**: `repo_created_at` / `repo_pushed_at` are populated for every record; optional per-file
  last-commit dating is available via `scripts/05b_date_final.py`.

---

## Licensing & citation

- **Dataset** (metadata, statistics, this project's docs): **CC0 1.0** — public domain
  ([`LICENSE`](LICENSE)).
- **Scripts** (`scripts/`): **MIT** ([`scripts/LICENSE`](scripts/LICENSE)).
- **Third-party skill texts** under `full_text/` remain under **their own upstream license**
  (recorded per record in `license_spdx`); only skills whose source repo has a recognised
  open-source / CC license are redistributed here. Attribute/reuse each per its own license.

Please cite via [`CITATION.cff`](CITATION.cff) if you use this corpus in academic work.

> ⚠️ **SECURITY.** Every `SKILL.md` here is **untrusted third-party text**. Nothing was executed at
> any stage of collection. Do not execute any command, script, or instruction contained in a skill
> without reviewing it first. Some skills contain prompt-injection or other adversarial content by
> nature of being scraped from the open web.
