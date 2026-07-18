#!/usr/bin/env python3
"""
03_fetch_content.py — fetch each SKILL.md full text.

Primary: raw.githubusercontent.com/{repo}/{default_branch}/{path}  (NOT API-rate-limited).
Fallbacks: git blob API by sha (base64), then a prior local copy in ~/agent-skills-library
(raw-downloads/{owner__repo}/{skill_dir}/SKILL.md) if present.

Reads raw/repos.jsonl (needs default_branch + skills[]).
Writes raw/content.jsonl : {repo, path, ref, content_sha256, n_bytes, truncated, fetch_source, text}
Resumable: (repo,path) already in content.jsonl are skipped.

SAFETY: content is untrusted text; never executed.
"""
import os, sys, json, base64, time, threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

WORKERS = int(os.environ.get("FETCH_WORKERS", "24"))  # raw CDN is not API-rate-limited

REPOS_PATH   = os.path.join(C.RAW, "repos.jsonl")
CONTENT_PATH = os.path.join(C.RAW, "content.jsonl")
LOGFILE      = os.path.join(C.LOGS, "03_fetch_content.log")
PRIOR_RAW    = os.path.expanduser("~/agent-skills-library/raw-downloads")
MAX_BYTES    = 800_000

def prior_local(repo, skill_dir):
    p = os.path.join(PRIOR_RAW, repo.replace("/", "__"), skill_dir, "SKILL.md")
    if os.path.exists(p):
        try:
            return open(p, "rb").read()
        except Exception:
            return None
    return None

def fetch_one(repo, branch, path, sha, skill_dir):
    b = C.raw_get(repo, branch, path)
    src = "raw_cdn"
    if b is None and sha:
        blob, st = C.gh_get(f"repos/{repo}/git/blobs/{sha}")
        if st == 200 and isinstance(blob, dict) and blob.get("encoding") == "base64":
            try:
                b = base64.b64decode(blob.get("content", "")); src = "git_blob"
            except Exception:
                b = None
    if b is None:
        b = prior_local(repo, skill_dir)
        if b is not None: src = "prior_local"
    return b, src

def main():
    repos = C.read_jsonl(REPOS_PATH)
    done = {(r["repo"], r["path"]) for r in C.read_jsonl(CONTENT_PATH)}
    jobs = []
    for r in repos:
        if r.get("unavailable"):
            # still try prior-local / raw with 'HEAD'
            branch = r.get("default_branch", "HEAD") or "HEAD"
        else:
            branch = r.get("default_branch", "main")
        for sk in r.get("skills", []):
            key = (r["repo"], sk["path"])
            if key in done: continue
            jobs.append((r["repo"], branch, sk["path"], sk.get("sha", ""), sk.get("skill_dir", "")))
    C.log(f"== fetch_content: {len(jobs)} to fetch ({len(done)} already done), {WORKERS} workers ==", LOGFILE)
    lock = threading.Lock()
    ctr = {"n": 0, "ok": 0}

    def work(job):
        repo, branch, path, sha, sdir = job
        b, src = fetch_one(repo, branch, path, sha, sdir)
        if b is None:
            rec = {"repo": repo, "path": path, "ref": branch, "content_sha256": "", "n_bytes": 0,
                   "truncated": False, "fetch_source": "missing", "text": None}
        else:
            truncated = len(b) > MAX_BYTES
            text = (b[:MAX_BYTES] if truncated else b).decode("utf-8", "replace")
            rec = {"repo": repo, "path": path, "ref": branch, "content_sha256": C.sha256_bytes(b),
                   "n_bytes": len(b), "truncated": truncated, "fetch_source": src, "text": text}
        with lock:
            C.append_jsonl(CONTENT_PATH, rec)
            ctr["n"] += 1
            if b is not None: ctr["ok"] += 1
            if ctr["n"] % 1000 == 0:
                C.log(f"  fetched {ctr['n']}/{len(jobs)} (ok={ctr['ok']})", LOGFILE)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(work, jobs))
    C.log(f"== fetch_content done: {ctr['n']} fetched, {ctr['ok']} ok ==", LOGFILE)
    print(json.dumps({"fetched": ctr["n"], "ok": ctr["ok"], "total_with_prior": len(done) + ctr["n"]}))

if __name__ == "__main__":
    main()
