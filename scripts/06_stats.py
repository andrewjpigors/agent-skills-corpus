#!/usr/bin/env python3
"""
06_stats.py — corpus statistics + coverage report. OFFLINE.

Reads data/metadata.jsonl, data/build_report.json, raw/_enum_state.json,
and any raw/other_sources/*notes*.md / *.jsonl for cross-engine signals.
Writes stats/stats.json and stats/STATS.md.
"""
import os, sys, json, re
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

STATS_DIR = os.path.join(C.ROOT, "stats")
os.makedirs(STATS_DIR, exist_ok=True)

def ym(iso):
    m = re.match(r"(\d{4})-(\d{2})", iso or "")
    return f"{m.group(1)}-{m.group(2)}" if m else "unknown"
def year(iso):
    m = re.match(r"(\d{4})", iso or "")
    return m.group(1) if m else "unknown"

def main():
    recs = C.read_jsonl(os.path.join(C.DATA, "metadata.jsonl"))
    build = {}
    bp = os.path.join(C.DATA, "build_report.json")
    if os.path.exists(bp): build = json.load(open(bp))
    enum = {}
    ep = os.path.join(C.RAW, "_enum_state.json")
    if os.path.exists(ep):
        e = json.load(open(ep))
        enum = {"candidates_enumerated": e.get("candidates", 0),
                "coverage_gaps": len(e.get("gaps", [])),
                "gaps_detail_sample": e.get("gaps", [])[:20],
                "frontier_remaining": len(e.get("stack", []))}

    n = len(recs)
    # two-axis classification (from 09_classify.py output)
    cat_c, aplat_c = Counter(), Counter()
    for c in C.read_jsonl(os.path.join(C.DATA, "classification.jsonl")):
        cat_c[c.get("category", "other")] += 1
        aplat_c[c.get("agent_platform", "generic")] += 1
    platform = Counter(r.get("platform", "") for r in recs)
    source = Counter((r.get("source", "") or "").split(":")[0] for r in recs)
    lic = Counter((r.get("license_spdx") or "NONE") for r in recs)
    owner_type = Counter(r.get("owner_type", "") or "unknown" for r in recs)
    created_by_month = Counter(ym(r.get("repo_created_at")) for r in recs)
    updated_by_year = Counter(year(r.get("file_last_commit_at") or r.get("repo_pushed_at")) for r in recs)
    stars = sorted((int(r.get("stars") or 0) for r in recs), reverse=True)
    def star_bucket(s):
        return ("0" if s == 0 else "1-9" if s < 10 else "10-99" if s < 100 else
                "100-999" if s < 1000 else "1000+")
    star_dist = Counter(star_bucket(int(r.get("stars") or 0)) for r in recs)
    n_siblings = Counter(min(len(r.get("sibling_files") or []), 20) for r in recs)
    have_text = sum(1 for r in recs if r.get("skill_md_text"))
    unique_repos = len({r.get("repo") for r in recs})
    unique_names = len({(r.get("frontmatter_name") or "").strip().lower() for r in recs})

    # publishable split preview
    allow = set(C.CONFIG["publishability"]["publish_full_text_if_license_in"])
    publishable = sum(1 for r in recs if (r.get("license_spdx") in allow))

    stats = {
        "snapshot_date": C.SNAPSHOT_DATE,
        "total_unique_skills": n,
        "unique_repositories": unique_repos,
        "unique_frontmatter_names": unique_names,
        "records_with_full_text": have_text,
        "publishable_full_text (clear OSS/CC license)": publishable,
        "local_only_full_text (no clear license)": n - publishable,
        "dedup": {
            "raw_records": build.get("raw_records"),
            "included_raw": build.get("included_raw"),
            "excluded_raw": build.get("excluded_raw"),
            "forks_excluded": build.get("forks_excluded"),
            "included_nonfork_predupe": build.get("included_nonfork_predupe"),
            "unique_after_dedup": build.get("unique_after_dedup"),
            "duplicate_groups": build.get("duplicate_groups"),
            "duplicate_records_collapsed": build.get("duplicate_raw_records_collapsed"),
        },
        "exclude_reason_breakdown": build.get("exclude_reason_breakdown", {}),
        "functional_category_distribution": dict(cat_c.most_common()),
        "agent_platform_distribution": dict(aplat_c.most_common()),
        "platform_distribution": dict(platform.most_common()),
        "source_distribution": dict(source.most_common()),
        "license_distribution": dict(lic.most_common()),
        "owner_type_distribution": dict(owner_type.most_common()),
        "stars_distribution": dict(sorted(star_dist.items())),
        "top_stars": stars[:10],
        "sibling_file_count_distribution": dict(sorted(n_siblings.items())),
        "repo_created_by_month": dict(sorted(created_by_month.items())),
        "last_updated_by_year": dict(sorted(updated_by_year.items())),
        "github_enumeration": enum,
    }
    # cross-engine signal
    sg = os.path.join(C.RAW, "other_sources", "sourcegraph_sample.jsonl")
    if os.path.exists(sg):
        stats["sourcegraph_sampled_matches"] = len(C.read_jsonl(sg))

    json.dump(stats, open(os.path.join(STATS_DIR, "stats.json"), "w"), indent=2)

    # markdown
    def table(d, k="key", v="count"):
        lines = [f"| {k} | {v} |", "|---|---:|"]
        for kk, vv in d.items():
            lines.append(f"| {kk} | {vv} |")
        return "\n".join(lines)
    md = []
    md.append(f"# Corpus Statistics — Claude Agent Skills\n")
    md.append(f"**Snapshot date:** {C.SNAPSHOT_DATE}  \n")
    md.append(f"**Total unique skills (included, fork-excluded, content-deduped):** {n}  ")
    md.append(f"**Unique repositories:** {unique_repos}  ")
    md.append(f"**Unique frontmatter `name` values:** {unique_names}  ")
    md.append(f"**Records with full SKILL.md text:** {have_text}\n")
    md.append("## Deduplication (before → after)\n")
    d = stats["dedup"]
    md.append(f"- Raw records collected: **{d['raw_records']}**")
    md.append(f"- Passed inclusion filter: **{d['included_raw']}** (excluded {d['excluded_raw']})")
    md.append(f"- After excluding forks: **{d['included_nonfork_predupe']}** (forks removed: {d['forks_excluded']})")
    md.append(f"- **Unique after content-hash dedup: {d['unique_after_dedup']}** "
              f"({d['duplicate_groups']} dup groups, {d['duplicate_records_collapsed']} duplicate records collapsed)\n")
    md.append("## Exclusion reasons\n"); md.append(table(stats["exclude_reason_breakdown"], "reason", "count") + "\n")
    md.append("## Functional category distribution\n"); md.append(table(stats["functional_category_distribution"], "category", "skills") + "\n")
    md.append("## Agent-platform distribution (from SKILL.md path namespace)\n"); md.append(table(stats["agent_platform_distribution"], "agent_platform", "skills") + "\n")
    md.append("## Hosting-platform distribution\n"); md.append(table(stats["platform_distribution"], "platform", "skills") + "\n")
    md.append("## Source distribution\n"); md.append(table(stats["source_distribution"], "source", "skills") + "\n")
    md.append("## License distribution (repo SPDX)\n"); md.append(table(stats["license_distribution"], "license", "skills") + "\n")
    md.append("## Owner type\n"); md.append(table(stats["owner_type_distribution"], "owner_type", "skills") + "\n")
    md.append("## Stars distribution\n"); md.append(table(stats["stars_distribution"], "stars_bucket", "skills") + "\n")
    md.append("## Repo creation by month\n"); md.append(table(stats["repo_created_by_month"], "month", "skills") + "\n")
    md.append("## Last update by year\n"); md.append(table(stats["last_updated_by_year"], "year", "skills") + "\n")
    md.append("## GitHub enumeration coverage\n")
    md.append(f"- Candidates enumerated (unique repo/path, exact basename): **{enum.get('candidates_enumerated')}**")
    md.append(f"- Documented coverage gaps (saturated unsplittable size buckets): **{enum.get('coverage_gaps')}**")
    md.append(f"- Enumeration frontier remaining (0 = complete): **{enum.get('frontier_remaining')}**")
    if "sourcegraph_sampled_matches" in stats:
        md.append(f"- Sourcegraph cross-engine sampled matches: **{stats['sourcegraph_sampled_matches']}**")
    md.append("")
    md.append("## Publishability\n")
    md.append(f"- Full text publishable under a clear OSS/CC license: **{publishable}**")
    md.append(f"- Full text local-only (no clear license): **{n - publishable}**\n")
    open(os.path.join(STATS_DIR, "STATS.md"), "w").write("\n".join(md))
    print(json.dumps({"total_unique": n, "unique_repos": unique_repos, "publishable": publishable}, indent=2))

if __name__ == "__main__":
    main()
