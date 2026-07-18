#!/usr/bin/env python3
"""
05_build_corpus.py — join + inclusion-filter + fork-exclude + content-hash dedup (OFFLINE).

Inputs:
  raw/repos.jsonl            (GitHub repo meta + skills[] with siblings)
  raw/content.jsonl          (GitHub SKILL.md text + content_sha256)
  raw/other_sources/*.jsonl  (gitlab.jsonl, gitee.jsonl, sourcegraph_sample.jsonl,
                              marketplace_github_candidates.jsonl — the last two are
                              GitHub pointers already folded into repos.jsonl/content.jsonl
                              upstream; only records carrying their own skill_md_text are
                              treated as standalone non-GitHub rows.)

Pipeline (order matters, per config.dedup):
  1. Assemble raw records from all platforms.
  2. Inclusion filter (frontmatter has name+description, non-empty, non-template, non-placeholder).
  3. Exclude forks.
  4. Content-hash (sha256 of raw SKILL.md) dedup, keep EARLIEST source.
  5. Report before/after counts; write outputs.

Outputs (data/):
  metadata.jsonl                 unique, included, fork-excluded, deduped  (THE corpus)
  metadata_included_predupe.jsonl included + fork-excluded, before dedup
  duplicates.jsonl               one row per dup group (>1 raw occurrence)
  excluded.jsonl                 every excluded raw record + reason
  build_report.json              counts at each stage
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

REPOS_PATH   = os.path.join(C.RAW, "repos.jsonl")
CONTENT_PATH = os.path.join(C.RAW, "content.jsonl")
OTHER_DIR    = os.path.join(C.RAW, "other_sources")

def dirname(p): return p.rsplit("/", 1)[0] if "/" in p else ""

def load_github():
    repos = {r["repo"]: r for r in C.read_jsonl(REPOS_PATH)}
    content = {(c["repo"], c["path"]): c for c in C.read_jsonl(CONTENT_PATH)}
    rows = []
    for repo, r in repos.items():
        for sk in r.get("skills", []):
            c = content.get((repo, sk["path"]))
            text = C.clean_text(c.get("text")) if c else None
            rows.append({
                "platform": "github",
                "repo": repo,
                "owner": r.get("owner", ""),
                "owner_type": r.get("owner_type", ""),
                "path": sk["path"],
                "skill_dir": sk.get("skill_dir", dirname(sk["path"])),
                "html_url": f"https://github.com/{repo}/blob/{r.get('default_branch','HEAD')}/{sk['path']}",
                "stars": r.get("stars", 0),
                "license_spdx": C.canon_spdx(r.get("license_spdx", "")),
                "license_name": r.get("license_name", ""),
                "is_fork": bool(r.get("is_fork", False)),
                "repo_created_at": r.get("created_at", ""),
                "repo_pushed_at": r.get("pushed_at", ""),
                "file_last_commit_at": "",
                "default_branch": r.get("default_branch", ""),
                # recompute hash uniformly from text so cross-platform dedup is exact
                "content_sha256": C.sha256_bytes(text.encode("utf-8")) if text else "",
                "n_bytes": (c or {}).get("n_bytes", 0),
                "sibling_files": sk.get("siblings", []),
                "source": "github_code_search" if not sk.get("from_tree_only") else "github_repo_tree",
                "snapshot_date": C.SNAPSHOT_DATE,
                "skill_md_text": text,
                "_from_tree_only": sk.get("from_tree_only", False),
                "unavailable_repo": bool(r.get("unavailable", False)),
            })
    return rows

def load_other_platform(fname, platform):
    path = os.path.join(OTHER_DIR, fname)
    rows = []
    for o in C.read_jsonl(path):
        text = C.clean_text(o.get("skill_md_text"))
        if not text:      # pointer-only rows without their own text are not standalone records
            continue
        b = text.encode("utf-8", "replace")
        rows.append({
            "platform": platform,
            "repo": o.get("repo", ""),
            "owner": o.get("owner", ""),
            "owner_type": o.get("owner_type", ""),
            "path": o.get("path", ""),
            "skill_dir": dirname(o.get("path", "")),
            "html_url": o.get("html_url", ""),
            "stars": o.get("stars", 0),
            "license_spdx": C.canon_spdx(o.get("license_spdx", "")),
            "license_name": o.get("license_name", ""),
            "is_fork": bool(o.get("is_fork", False)),
            "repo_created_at": o.get("created_at", ""),
            "repo_pushed_at": o.get("updated_at", ""),
            "file_last_commit_at": "",
            "default_branch": o.get("default_branch", ""),
            "content_sha256": C.sha256_bytes(b),   # uniform text-derived hash (cross-platform dedup)
            "n_bytes": len(b),
            "sibling_files": o.get("sibling_files", []),
            "source": o.get("source", platform),
            "snapshot_date": C.SNAPSHOT_DATE,
            "skill_md_text": text,
            "_from_tree_only": False,
            "unavailable_repo": False,
        })
    return rows

def earliest_key(rec):
    # earliest source: repo_created_at, then file/pushed date, then repo name
    return (rec.get("repo_created_at") or "9999",
            rec.get("file_last_commit_at") or rec.get("repo_pushed_at") or "9999",
            rec.get("repo", "~"), rec.get("path", "~"))

def main():
    rows = load_github()
    for fn, plat in [("gitlab.jsonl", "gitlab"), ("gitee.jsonl", "gitee")]:
        rows += load_other_platform(fn, plat)
    report = {"snapshot_date": C.SNAPSHOT_DATE, "raw_records": len(rows)}

    # 2. inclusion filter
    included, excluded = [], []
    excl_reasons = {}
    for r in rows:
        cl = C.classify_skill(r.get("skill_md_text"))
        if cl["included"]:
            r["frontmatter_name"] = cl["name"]
            r["frontmatter_description"] = cl["description"]
            included.append(r)
        else:
            excl_reasons[cl["reason"]] = excl_reasons.get(cl["reason"], 0) + 1
            excluded.append({"repo": r["repo"], "path": r["path"], "platform": r["platform"],
                             "reason": cl["reason"], "source": r.get("source", "")})
    report["included_raw"] = len(included)
    report["excluded_raw"] = len(excluded)
    report["exclude_reason_breakdown"] = dict(sorted(excl_reasons.items(), key=lambda x: -x[1]))

    # 3. exclude forks (before dedup)
    forks = [r for r in included if r.get("is_fork")]
    included_nofork = [r for r in included if not r.get("is_fork")]
    report["forks_excluded"] = len(forks)
    report["included_nonfork_predupe"] = len(included_nofork)

    # 4. content-hash dedup, keep earliest
    groups = {}
    for r in included_nofork:
        h = r.get("content_sha256") or ("NOHASH::" + r["repo"] + "::" + r["path"])
        groups.setdefault(h, []).append(r)
    unique = []
    dup_rows = []
    for h, members in groups.items():
        members_sorted = sorted(members, key=earliest_key)
        rep = dict(members_sorted[0])
        rep["dup_group"] = h[:16]
        rep["dup_count"] = len(members)
        rep["dup_sources"] = [{"platform": m["platform"], "repo": m["repo"], "path": m["path"],
                               "source": m.get("source", "")} for m in members_sorted]
        # id: stable, content-derived
        rep["id"] = (h[:12] if not h.startswith("NOHASH") else "nohash") + "-" + \
                    C.sha256_bytes((rep["repo"] + "/" + rep["path"]).encode())[:8]
        # drop internal fields
        for k in ("_from_tree_only",):
            rep.pop(k, None)
        unique.append(rep)
        if len(members) > 1:
            dup_rows.append({"content_sha256": h, "count": len(members),
                             "representative": {"platform": rep["platform"], "repo": rep["repo"], "path": rep["path"]},
                             "members": rep["dup_sources"]})
    report["unique_after_dedup"] = len(unique)
    report["duplicate_groups"] = len(dup_rows)
    report["duplicate_raw_records_collapsed"] = report["included_nonfork_predupe"] - report["unique_after_dedup"]

    # write outputs
    unique_sorted = sorted(unique, key=lambda r: (-int(r.get("stars") or 0), r.get("repo", "")))
    C.write_jsonl(os.path.join(C.DATA, "metadata.jsonl"), unique_sorted)
    C.write_jsonl(os.path.join(C.DATA, "metadata_included_predupe.jsonl"), included_nofork)
    C.write_jsonl(os.path.join(C.DATA, "duplicates.jsonl"), dup_rows)
    C.write_jsonl(os.path.join(C.DATA, "excluded.jsonl"), excluded)
    json.dump(report, open(os.path.join(C.DATA, "build_report.json"), "w"), indent=2)

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
