#!/usr/bin/env python3
"""
10_reorganize_by_category.py — produce the category-organized, publish-ready layout.

Joins data/metadata.jsonl (full, with text) + data/classification.jsonl (id -> category,
agent_platform) and writes:
  data/metadata.public.jsonl        metadata + category + agent_platform + full_text pointer
                                    (skill_md_text=null; dup_sources capped at 30)
  data/metadata.public.jsonl.gz     compressed copy
  data/by_category/<category>.jsonl  public metadata split per functional category
  full_text/<category>/<id>__<slug>.md            clear-license full text (publishable)
  full_text_local_only/<category>/<id>__<slug>.md no-license full text (local only, git-ignored)

Streams metadata.jsonl (1.8 GB) line-by-line — low memory. Idempotent: clears the full_text
trees and by_category dir first.
"""
import os, sys, re, json, gzip, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

FT_PUB   = os.path.join(C.ROOT, "full_text")
FT_LOCAL = os.path.join(C.ROOT, "full_text_local_only")
BYCAT    = os.path.join(C.DATA, "by_category")
PUB      = os.path.join(C.DATA, "metadata.public.jsonl")
ALLOW    = set(C.CONFIG["publishability"]["publish_full_text_if_license_in"])
DUP_CAP  = 30

def slug(s):
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", (s or "skill")).strip("-.").lower()
    return s[:48] or "skill"

def main():
    # fresh trees
    for d in (FT_PUB, FT_LOCAL, BYCAT):
        if os.path.isdir(d): shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
    cls = {}
    for o in C.read_jsonl(os.path.join(C.DATA, "classification.jsonl")):
        cls[o["id"]] = (o.get("category", "other"), o.get("agent_platform", "generic"))

    cat_writers = {}
    def cat_writer(cat):
        if cat not in cat_writers:
            cat_writers[cat] = open(os.path.join(BYCAT, f"{cat}.jsonl"), "w", encoding="utf-8", errors="replace")
        return cat_writers[cat]

    npub = nloc = nmiss = n = 0
    made_dirs = set()
    with open(PUB, "w", encoding="utf-8", errors="replace") as pubf:
        for ln in open(os.path.join(C.DATA, "metadata.jsonl"), encoding="utf-8", errors="replace"):
            o = json.loads(ln); n += 1
            cat, plat = cls.get(o.get("id"), ("other", "generic"))
            o["category"] = cat
            o["agent_platform"] = plat
            text = o.get("skill_md_text")
            ds = o.get("dup_sources") or []
            if len(ds) > DUP_CAP:
                o["dup_sources"] = ds[:DUP_CAP]; o["dup_sources_truncated"] = True
            fname = f"{o.get('id')}__{slug(o.get('frontmatter_name') or o.get('skill_dir'))}.md"
            o["skill_md_text"] = None
            if text:
                publishable = (o.get("license_spdx") in ALLOW)
                root = FT_PUB if publishable else FT_LOCAL
                d = os.path.join(root, cat)
                if d not in made_dirs:
                    os.makedirs(d, exist_ok=True); made_dirs.add(d)
                with open(os.path.join(d, fname), "w", encoding="utf-8", errors="replace") as f:
                    f.write(text)
                rel = f"{'full_text' if publishable else 'full_text_local_only'}/{cat}/{fname}"
                if publishable:
                    o["full_text_available"] = "published"; o["full_text_path"] = rel; npub += 1
                else:
                    o["full_text_available"] = "local_only"; o["full_text_local_path"] = rel; nloc += 1
            else:
                o["full_text_available"] = "missing"; nmiss += 1
            line = json.dumps(o, ensure_ascii=False)
            pubf.write(line + "\n")
            cat_writer(cat).write(line + "\n")
    for w in cat_writers.values(): w.close()

    with open(PUB, "rb") as fi, gzip.open(PUB + ".gz", "wb") as fo:
        shutil.copyfileobj(fi, fo)

    print(json.dumps({"records": n, "published_full_text": npub, "local_only_full_text": nloc,
                      "missing_text": nmiss, "categories": len(cat_writers),
                      "public_bytes": os.path.getsize(PUB), "gz_bytes": os.path.getsize(PUB + ".gz")}, indent=2))

if __name__ == "__main__":
    main()
