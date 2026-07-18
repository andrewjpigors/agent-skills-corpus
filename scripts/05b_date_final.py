#!/usr/bin/env python3
"""
05b_date_final.py — fill file_last_commit_at for the FINAL deduped GitHub records only.

Runs AFTER 05 so the number of commit-API calls is minimized (one per unique kept record).
Uses GET repos/{repo}/commits?path=<path>&per_page=1&sha=<branch> -> latest commit date.
Cache: raw/last_commit_cache.jsonl (resumable). Falls back to repo_pushed_at when budget
is exhausted or the call fails (flagged via file_date_source).

Rewrites data/metadata.jsonl in place with file_last_commit_at + file_date_source.
Env: DATE_CORE_BUDGET (default 4000).
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

META_PATH  = os.path.join(C.DATA, "metadata.jsonl")
CACHE_PATH = os.path.join(C.RAW, "last_commit_cache.jsonl")
LOGFILE    = os.path.join(C.LOGS, "05b_date.log")
BUDGET     = int(os.environ.get("DATE_CORE_BUDGET", "4000"))

def main():
    recs = C.read_jsonl(META_PATH)
    cache = {(c["repo"], c["path"]): c["date"] for c in C.read_jsonl(CACHE_PATH)}
    calls = 0
    filled = 0
    for r in recs:
        if r.get("platform") != "github":
            if not r.get("file_last_commit_at"):
                r["file_last_commit_at"] = r.get("repo_pushed_at", "")
                r["file_date_source"] = "repo_pushed_at"
            continue
        key = (r["repo"], r["path"])
        if key in cache:
            r["file_last_commit_at"] = cache[key]; r["file_date_source"] = "file_commit"
            filled += 1; continue
        if calls >= BUDGET or r.get("unavailable_repo"):
            r["file_last_commit_at"] = r.get("repo_pushed_at", ""); r["file_date_source"] = "repo_pushed_at"
            continue
        branch = r.get("default_branch") or "HEAD"
        data, st = C.gh_get(f"repos/{r['repo']}/commits",
                            {"path": r["path"], "per_page": 1, "sha": branch}); calls += 1
        date = ""
        if st == 200 and isinstance(data, list) and data:
            commit = data[0].get("commit", {})
            date = (commit.get("committer") or {}).get("date") or (commit.get("author") or {}).get("date") or ""
        if date:
            cache[key] = date
            C.append_jsonl(CACHE_PATH, {"repo": r["repo"], "path": r["path"], "date": date})
            r["file_last_commit_at"] = date; r["file_date_source"] = "file_commit"; filled += 1
        else:
            r["file_last_commit_at"] = r.get("repo_pushed_at", ""); r["file_date_source"] = "repo_pushed_at"
        if calls % 100 == 0:
            C.log(f"  dated {calls} via API ({filled} filled)", LOGFILE)
    C.write_jsonl(META_PATH, recs)
    C.log(f"== dating done: {calls} API calls, {filled} file-level dates ==", LOGFILE)
    print(json.dumps({"records": len(recs), "api_calls": calls, "file_level_dates": filled}))

if __name__ == "__main__":
    main()
