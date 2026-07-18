#!/usr/bin/env python3
"""
04_merge_github_candidates.py — fold GitHub pointers discovered by the marketplace/awesome-list
and Sourcegraph agents into raw/github_candidates.jsonl so they get enriched uniformly.

Sources merged (if present):
  raw/other_sources/marketplace_github_candidates.jsonl  (source: marketplace:* / awesome:* / official:*)

Sourcegraph (source #5) is used ONLY for coverage cross-validation (see 06_stats.py), NOT
ingested as corpus records — per the study design it is a second-engine sample check, and
folding its ~4k repos into enrichment would roughly double the GitHub core-API load. To
additionally ingest Sourcegraph-only repos, add "sourcegraph_sample.jsonl" to MERGE_FILES.

Dedup by (repo, path). Records with an unknown path (path == "") are kept as repo-only seeds:
02_enrich will scan the repo tree to find the real SKILL.md paths. Idempotent.
"""
MERGE_FILES = ["marketplace_github_candidates.jsonl"]
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

CAND_PATH = os.path.join(C.RAW, "github_candidates.jsonl")
OTHER = os.path.join(C.RAW, "other_sources")

def norm_repo(x):
    x = (x or "").strip()
    for pre in ("https://github.com/", "http://github.com/", "github.com/"):
        if x.startswith(pre): x = x[len(pre):]
    x = x.strip("/")
    parts = x.split("/")
    return "/".join(parts[:2]) if len(parts) >= 2 else ""

def main():
    existing = C.read_jsonl(CAND_PATH)
    seen = {(c["repo"], c.get("path", "")) for c in existing}
    added = 0
    for fname in MERGE_FILES:
        fp = os.path.join(OTHER, fname)
        for o in C.read_jsonl(fp):
            if fname.startswith("sourcegraph"):
                # only github.com matches feed the GitHub pipeline
                if "github.com" not in (o.get("repo", "") + o.get("html_url", "")) and o.get("platform") != "github":
                    continue
            repo = norm_repo(o.get("repo", "")) or norm_repo(o.get("html_url", ""))
            if not repo:
                continue
            path = o.get("path", "") or ""
            if path and path.rsplit("/", 1)[-1] != "SKILL.md":
                path = ""  # keep as repo-only seed rather than a bogus path
            key = (repo, path)
            if key in seen:
                continue
            seen.add(key)
            C.append_jsonl(CAND_PATH, {
                "platform": "github", "repo": repo, "owner": repo.split("/")[0],
                "owner_type": "", "path": path, "html_url": o.get("html_url", ""),
                "sha": "", "found_size_range": None,
                "source": o.get("source", fname.split(".")[0]),
                "snapshot_date": C.SNAPSHOT_DATE,
            })
            added += 1
    print(json.dumps({"added": added, "total_candidates": len(existing) + added}))

if __name__ == "__main__":
    main()
