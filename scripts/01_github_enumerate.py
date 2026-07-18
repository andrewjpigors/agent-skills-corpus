#!/usr/bin/env python3
"""
01_github_enumerate.py — broad GitHub enumeration of SKILL.md via size-sharded code search.

Method (see config.json -> sources.github_code_search):
  q = "filename:SKILL.md", sharded by byte-size range to break the 1000-results/query cap.
  Adaptive: when a range returns total_count>1000 (or HTTP 422), split it in half.
  GitHub's filename: qualifier is a fuzzy/substring match, so every item is post-filtered
  to exact basename == "SKILL.md".

Resumable: the pending-range frontier, seen keys, gaps, and stats persist to raw/_enum_state.json;
candidates stream to raw/github_candidates.jsonl. Re-run to continue where it stopped.

Env:
  ENUM_SEARCH_BUDGET  (default from config budgets.github_search_calls)
  ENUM_MAX_RUNTIME    seconds (default 999999)
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

STATE_PATH = os.path.join(C.RAW, "_enum_state.json")
CAND_PATH  = os.path.join(C.RAW, "github_candidates.jsonl")
LOGFILE    = os.path.join(C.LOGS, "01_github_enumerate.log")

BUDGET      = int(os.environ.get("ENUM_SEARCH_BUDGET", C.CONFIG["budgets"]["github_search_calls"]))
MAX_RUNTIME = int(os.environ.get("ENUM_MAX_RUNTIME", 999999))
SEED_LO, SEED_HI = C.CONFIG["sources"]["github_code_search"]["size_seed_range"]
QUERY = C.CONFIG["sources"]["github_code_search"]["query"]
T0 = time.time()

def load_state():
    if os.path.exists(STATE_PATH):
        s = json.load(open(STATE_PATH))
        s["seen"] = set(tuple(k) for k in s.get("seen", []))
        s["stack"] = [tuple(r) for r in s.get("stack", [])]
        return s
    return {"stack": [[SEED_LO, SEED_HI]], "seen": set(), "gaps": [],
            "done_ranges": 0, "search_calls_used": 0, "candidates": 0}

def save_state(s):
    out = dict(s)
    out["seen"] = [list(k) for k in s["seen"]]
    out["stack"] = [list(r) for r in s["stack"]]
    tmp = STATE_PATH + ".tmp"
    json.dump(out, open(tmp, "w"))
    os.replace(tmp, STATE_PATH)

def basename(path):
    return path.rsplit("/", 1)[-1]

def add_items(items, s, size_range):
    """Add exact-basename SKILL.md items; return count of NEW candidates."""
    new = 0
    for it in items or []:
        path = it.get("path", "")
        if basename(path) != "SKILL.md":   # exact-basename filter (fuzzy search noise removed)
            continue
        repo = it.get("repository", {}).get("full_name", "")
        key = (repo, path)
        if not repo or key in s["seen"]:
            continue
        s["seen"].add(key)
        owner = it.get("repository", {}).get("owner", {})
        cand = {
            "platform": "github",
            "repo": repo,
            "owner": owner.get("login", ""),
            "owner_type": owner.get("type", ""),
            "path": path,
            "html_url": it.get("html_url", ""),
            "sha": it.get("sha", ""),
            "found_size_range": list(size_range),
            "source": "github_code_search",
            "snapshot_date": C.SNAPSHOT_DATE,
        }
        C.append_jsonl(CAND_PATH, cand)
        new += 1
    return new

def query_range(lo, hi, page):
    q = f"{QUERY} size:{lo}..{hi}"
    return C.gh_get("search/code", {"q": q, "per_page": 100, "page": page}, is_search=True)

def main():
    s = load_state()
    C.log(f"== enumerate start: budget={BUDGET} stack={len(s['stack'])} seen={len(s['seen'])} "
          f"calls_used={s['search_calls_used']} ==", LOGFILE)
    calls = 0
    since_ckpt = 0
    while s["stack"]:
        if calls >= BUDGET:
            C.log(f"  search budget reached ({BUDGET}); pausing (resumable).", LOGFILE); break
        if time.time() - T0 > MAX_RUNTIME:
            C.log("  runtime cap reached; pausing (resumable).", LOGFILE); break
        lo, hi = s["stack"].pop()
        data, st = query_range(lo, hi, 1); calls += 1; since_ckpt += 1
        if st == 422:                                   # range invalid / >1000 window; split
            if hi > lo:
                mid = (lo + hi) // 2
                s["stack"].append((lo, mid)); s["stack"].append((mid + 1, hi))
            else:
                s["gaps"].append({"size": lo, "reason": "http_422_single_size"})
            continue
        if not isinstance(data, dict) or "items" not in data:
            # transient failure already retried inside gh_get; record and move on
            if data.get("_fail"):
                s["gaps"].append({"range": [lo, hi], "reason": "fetch_fail"})
            continue
        total = data.get("total_count", 0)
        new = add_items(data.get("items"), s, (lo, hi))
        if total > 1000 and hi > lo:                    # saturated -> split, don't page parent
            mid = (lo + hi) // 2
            s["stack"].append((lo, mid)); s["stack"].append((mid + 1, hi))
            s["done_ranges"] += 1
        else:
            if total > 1000 and lo == hi:               # unsplittable saturated single size
                s["gaps"].append({"size": lo, "total": total, "captured_cap": 1000,
                                  "reason": "single_size_over_1000"})
            pages = min(10, (min(total, 1000) + 99) // 100)
            for p in range(2, pages + 1):
                if calls >= BUDGET: break
                d2, st2 = query_range(lo, hi, p); calls += 1; since_ckpt += 1
                if st2 != 200 or not isinstance(d2, dict): break
                new += add_items(d2.get("items"), s, (lo, hi))
            s["done_ranges"] += 1
        s["search_calls_used"] += 0  # (kept for compat; real count below)
        if new:
            C.log(f"  size {lo}..{hi}: total~{total}, +{new} new (cands={len(s['seen'])}, "
                  f"calls={calls}/{BUDGET}, stack={len(s['stack'])})", LOGFILE)
        if since_ckpt >= 15:
            s["candidates"] = len(s["seen"]); s["search_calls_used"] = s.get("search_calls_used", 0)
            save_state(s); since_ckpt = 0
    s["candidates"] = len(s["seen"])
    save_state(s)
    done = not s["stack"]
    C.log(f"== enumerate {'COMPLETE' if done else 'PAUSED'}: candidates={len(s['seen'])} "
          f"gaps={len(s['gaps'])} calls_this_run={calls} stack_remaining={len(s['stack'])} ==", LOGFILE)
    print(json.dumps({"candidates": len(s["seen"]), "gaps": len(s["gaps"]),
                      "stack_remaining": len(s["stack"]), "complete": done}))

if __name__ == "__main__":
    main()
