# Corpus Statistics — Claude Agent Skills

**Snapshot date:** 2026-07-18  

**Total unique skills (included, fork-excluded, content-deduped):** 55698  
**Unique repositories:** 14784  
**Unique frontmatter `name` values:** 33055  
**Records with full SKILL.md text:** 55698

## Deduplication (before → after)

- Raw records collected: **109312**
- Passed inclusion filter: **105392** (excluded 3920)
- After excluding forks: **105302** (forks removed: 90)
- **Unique after content-hash dedup: 55698** (12716 dup groups, 49604 duplicate records collapsed)

## Exclusion reasons

| reason | count |
|---|---:|
| no_frontmatter | 2478 |
| missing_name | 601 |
| template_marker:todo | 591 |
| missing_description | 121 |
| template_marker:<name> | 86 |
| no_content | 14 |
| template_marker:<description> | 12 |
| template_marker:fixme | 8 |
| template_marker:example-skill | 5 |
| placeholder_no_body | 1 |
| template_marker:your-skill-name | 1 |
| template_marker:replace this | 1 |
| template_marker:brief description of | 1 |

## Functional category distribution

| category | skills |
|---|---:|
| other | 7165 |
| writing-docs-content | 6311 |
| devops-cloud-infra | 4696 |
| devtools-automation | 4319 |
| backend-api | 4050 |
| testing-qa | 3534 |
| security | 3197 |
| architecture-planning | 3019 |
| web-frontend | 2973 |
| agent-workflow-meta | 2720 |
| code-review-quality | 2658 |
| ai-ml-llm | 2462 |
| productivity-business | 2179 |
| database | 1708 |
| data-analytics | 1244 |
| design-ux-creative | 1200 |
| crypto-defi-finance | 562 |
| mobile | 516 |
| legal-regulatory | 487 |
| domain-science-other | 472 |
| expert-persona-advisor | 226 |

## Agent-platform distribution (from SKILL.md path namespace)

| agent_platform | skills |
|---|---:|
| generic | 47323 |
| claude | 6045 |
| cyberstrike | 1223 |
| codex | 336 |
| cursor | 321 |
| opencode | 311 |
| gemini | 134 |
| windsurf | 2 |
| aider | 1 |
| amazon-q | 1 |
| continue | 1 |

## Hosting-platform distribution

| platform | skills |
|---|---:|
| github | 46735 |
| gitlab | 8713 |
| gitee | 250 |

## Source distribution

| source | skills |
|---|---:|
| github_code_search | 31280 |
| github_repo_tree | 15455 |
| gitlab_api_v4 projects?search -> repository/tree(recursive) -> files/raw (blob code-search is auth-gated) | 8713 |
| gitee_api_v5_tree+raw (repos discovered via web search; anon repo/code search returns empty) | 250 |

## License distribution (repo SPDX)

| license | skills |
|---|---:|
| NONE | 22143 |
| MIT | 21488 |
| Apache-2.0 | 4747 |
| NOASSERTION | 4255 |
| AGPL-3.0 | 2112 |
| GPL-3.0 | 357 |
| CC-BY-4.0 | 126 |
| CC0-1.0 | 85 |
| BSD-3-Clause | 82 |
| MPL-2.0 | 61 |
| MIT-0 | 45 |
| Unlicense | 39 |
| GPL-2.0 | 37 |
| CC-BY-SA-4.0 | 16 |
| BSD-3-Clause-Clear | 14 |
| UPL-1.0 | 13 |
| LGPL-3.0 | 11 |
| ISC | 11 |
| EPL-2.0 | 9 |
| BSD-2-Clause | 8 |
| EUPL-1.2 | 7 |
| Zlib | 6 |
| other | 6 |
| 0BSD | 5 |
| LGPL-2.1 | 5 |
| OFL-1.1 | 3 |
| BlueOak-1.0.0 | 2 |
| WTFPL | 2 |
| Artistic-2.0 | 1 |
| LPPL-1.3c | 1 |
| MulanPSL-2.0 | 1 |

## Owner type

| owner_type | skills |
|---|---:|
| User | 37063 |
| Organization | 9672 |
| unknown | 8963 |

## Stars distribution

| stars_bucket | skills |
|---|---:|
| 0 | 25675 |
| 1-9 | 17065 |
| 10-99 | 8213 |
| 100-999 | 2713 |
| 1000+ | 2032 |

## Repo creation by month

| month | skills |
|---|---:|
| 2008-01 | 1 |
| 2009-04 | 1 |
| 2009-05 | 2 |
| 2009-09 | 1 |
| 2009-11 | 1 |
| 2009-12 | 1 |
| 2010-05 | 1 |
| 2010-08 | 1 |
| 2010-09 | 2 |
| 2011-03 | 1 |
| 2011-04 | 1 |
| 2011-06 | 4 |
| 2011-07 | 2 |
| 2011-08 | 27 |
| 2011-09 | 1 |
| 2011-10 | 5 |
| 2011-11 | 2 |
| 2011-12 | 2 |
| 2012-02 | 3 |
| 2012-03 | 2 |
| 2012-04 | 3 |
| 2012-05 | 3 |
| 2012-07 | 1 |
| 2012-08 | 2 |
| 2012-09 | 1 |
| 2012-10 | 2 |
| 2012-12 | 1 |
| 2013-01 | 3 |
| 2013-02 | 2 |
| 2013-03 | 1 |
| 2013-05 | 4 |
| 2013-06 | 3 |
| 2013-07 | 3 |
| 2013-08 | 8 |
| 2013-10 | 3 |
| 2013-11 | 1 |
| 2013-12 | 1 |
| 2014-01 | 1 |
| 2014-03 | 3 |
| 2014-04 | 5 |
| 2014-05 | 3 |
| 2014-08 | 2 |
| 2014-10 | 3 |
| 2014-11 | 1 |
| 2014-12 | 4 |
| 2015-01 | 8 |
| 2015-02 | 5 |
| 2015-03 | 4 |
| 2015-04 | 5 |
| 2015-05 | 5 |
| 2015-06 | 2 |
| 2015-07 | 5 |
| 2015-08 | 15 |
| 2015-09 | 4 |
| 2015-10 | 1 |
| 2015-11 | 8 |
| 2015-12 | 6 |
| 2016-01 | 6 |
| 2016-02 | 7 |
| 2016-03 | 9 |
| 2016-04 | 6 |
| 2016-06 | 4 |
| 2016-07 | 5 |
| 2016-08 | 6 |
| 2016-09 | 4 |
| 2016-10 | 3 |
| 2016-11 | 6 |
| 2016-12 | 12 |
| 2017-01 | 5 |
| 2017-02 | 2 |
| 2017-03 | 11 |
| 2017-04 | 2 |
| 2017-05 | 5 |
| 2017-06 | 3 |
| 2017-07 | 3 |
| 2017-08 | 8 |
| 2017-09 | 1 |
| 2017-10 | 4 |
| 2017-11 | 7 |
| 2018-01 | 9 |
| 2018-02 | 7 |
| 2018-03 | 6 |
| 2018-04 | 12 |
| 2018-05 | 7 |
| 2018-06 | 6 |
| 2018-07 | 5 |
| 2018-08 | 5 |
| 2018-09 | 4 |
| 2018-10 | 3 |
| 2018-11 | 10 |
| 2018-12 | 10 |
| 2019-01 | 7 |
| 2019-02 | 7 |
| 2019-03 | 13 |
| 2019-04 | 6 |
| 2019-05 | 9 |
| 2019-06 | 10 |
| 2019-07 | 8 |
| 2019-08 | 45 |
| 2019-10 | 6 |
| 2019-11 | 14 |
| 2019-12 | 59 |
| 2020-01 | 8 |
| 2020-02 | 14 |
| 2020-03 | 14 |
| 2020-04 | 8 |
| 2020-05 | 18 |
| 2020-06 | 18 |
| 2020-07 | 138 |
| 2020-08 | 8 |
| 2020-09 | 9 |
| 2020-10 | 8 |
| 2020-11 | 7 |
| 2020-12 | 7 |
| 2021-01 | 6 |
| 2021-02 | 8 |
| 2021-03 | 4 |
| 2021-04 | 9 |
| 2021-05 | 11 |
| 2021-06 | 311 |
| 2021-07 | 14 |
| 2021-08 | 13 |
| 2021-09 | 33 |
| 2021-10 | 19 |
| 2021-11 | 14 |
| 2021-12 | 24 |
| 2022-01 | 55 |
| 2022-02 | 20 |
| 2022-03 | 27 |
| 2022-04 | 34 |
| 2022-05 | 12 |
| 2022-06 | 31 |
| 2022-07 | 15 |
| 2022-08 | 19 |
| 2022-09 | 8 |
| 2022-10 | 13 |
| 2022-11 | 15 |
| 2022-12 | 14 |
| 2023-01 | 22 |
| 2023-02 | 19 |
| 2023-03 | 20 |
| 2023-04 | 24 |
| 2023-05 | 33 |
| 2023-06 | 15 |
| 2023-07 | 27 |
| 2023-08 | 27 |
| 2023-09 | 57 |
| 2023-10 | 22 |
| 2023-11 | 22 |
| 2023-12 | 34 |
| 2024-01 | 41 |
| 2024-02 | 161 |
| 2024-03 | 37 |
| 2024-04 | 26 |
| 2024-05 | 73 |
| 2024-06 | 48 |
| 2024-07 | 26 |
| 2024-08 | 38 |
| 2024-09 | 44 |
| 2024-10 | 47 |
| 2024-11 | 59 |
| 2024-12 | 81 |
| 2025-01 | 56 |
| 2025-02 | 46 |
| 2025-03 | 87 |
| 2025-04 | 101 |
| 2025-05 | 230 |
| 2025-06 | 249 |
| 2025-07 | 1020 |
| 2025-08 | 275 |
| 2025-09 | 532 |
| 2025-10 | 878 |
| 2025-11 | 1239 |
| 2025-12 | 1335 |
| 2026-01 | 2974 |
| 2026-02 | 4359 |
| 2026-03 | 9114 |
| 2026-04 | 9660 |
| 2026-05 | 9218 |
| 2026-06 | 7133 |
| 2026-07 | 4623 |

## Last update by year

| year | skills |
|---|---:|
| 2025 | 581 |
| 2026 | 55117 |

## GitHub enumeration coverage

- Candidates enumerated (unique repo/path, exact basename): **77045**
- Documented coverage gaps (saturated unsplittable size buckets): **0**
- Enumeration frontier remaining (0 = complete): **6**
- Sourcegraph cross-engine sampled matches: **8000**

## Publishability

- Full text publishable under a clear OSS/CC license: **29205**
- Full text local-only (no clear license): **26493**
