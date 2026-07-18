#!/usr/bin/env python3
"""
08_merge_shards.py — concatenate parallel GraphQL shard outputs into the main raw files.

Merges raw/repos.jsonl.s* into raw/repos.jsonl (dedup by repo, existing main records win)
and raw/content.jsonl.s* into raw/content.jsonl (dedup by (repo,path)). Idempotent: after a
successful merge the shard files are renamed to *.merged so re-running is safe.
"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

def merge(main_path, shard_glob, key_fn):
    seen = set()
    rows = []
    # main first (wins on conflict)
    for r in C.read_jsonl(main_path):
        k = key_fn(r)
        if k in seen: continue
        seen.add(k); rows.append(r)
    n_main = len(rows)
    shard_files = sorted(glob.glob(shard_glob))
    n_shard_added = 0
    for sf in shard_files:
        for r in C.read_jsonl(sf):
            k = key_fn(r)
            if k in seen: continue
            seen.add(k); rows.append(r); n_shard_added += 1
    C.write_jsonl(main_path, rows)
    return n_main, n_shard_added, shard_files

def main():
    rm, ra, rf = merge(os.path.join(C.RAW, "repos.jsonl"),
                       os.path.join(C.RAW, "repos.jsonl.s*"),
                       lambda r: r.get("repo", ""))
    cm, ca, cf = merge(os.path.join(C.RAW, "content.jsonl"),
                       os.path.join(C.RAW, "content.jsonl.s*"),
                       lambda r: (r.get("repo", ""), r.get("path", "")))
    for sf in set(rf) | set(cf):
        try: os.rename(sf, sf + ".merged")
        except Exception: pass
    print(json.dumps({"repos_main_before": rm, "repos_added_from_shards": ra, "repos_total": rm + ra,
                      "content_main_before": cm, "content_added_from_shards": ca, "content_total": cm + ca,
                      "shard_files_merged": len(set(rf) | set(cf))}, indent=2))

if __name__ == "__main__":
    main()
