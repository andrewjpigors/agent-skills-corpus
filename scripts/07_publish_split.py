#!/usr/bin/env python3
"""
07_publish_split.py — split full text into publishable vs local-only by license, and emit
the publish-safe metadata file. OFFLINE.

Publishable = repo license SPDX in config.publishability.publish_full_text_if_license_in.
  -> full text written to full_text/<id>.md AND included in data/metadata.public.jsonl.
Otherwise (no/unclear license) = local-only:
  -> full text written to full_text_local_only/<id>.md (git-ignored),
     data/metadata.public.jsonl carries metadata only (skill_md_text=null, flag set).

data/metadata.jsonl (the full local corpus, with all text) is left untouched.
"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

FT_PUB   = os.path.join(C.ROOT, "full_text")
FT_LOCAL = os.path.join(C.ROOT, "full_text_local_only")
os.makedirs(FT_PUB, exist_ok=True); os.makedirs(FT_LOCAL, exist_ok=True)
ALLOW = set(C.CONFIG["publishability"]["publish_full_text_if_license_in"])

def slug(s):
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", (s or "skill")).strip("-.").lower()
    return s[:50] or "skill"

def main():
    recs = C.read_jsonl(os.path.join(C.DATA, "metadata.jsonl"))
    public = []
    npub = nloc = 0
    for r in recs:
        text = r.get("skill_md_text")
        rid = r.get("id", C.sha256_bytes((r["repo"] + "/" + r["path"]).encode())[:12])
        fname = f"{rid}__{slug(r.get('frontmatter_name') or r.get('skill_dir'))}.md"
        publishable = (r.get("license_spdx") in ALLOW)
        pub = {k: v for k, v in r.items() if k != "skill_md_text"}
        # metadata.public.jsonl stays lean (metadata + pointer); full text lives in the
        # full_text/ files (publishable) so no single file blows past host size limits.
        pub["skill_md_text"] = None
        if text:
            if publishable:
                with open(os.path.join(FT_PUB, fname), "w", encoding="utf-8", errors="replace") as f:
                    f.write(text)
                pub["full_text_available"] = "published"
                pub["full_text_path"] = f"full_text/{fname}"
                npub += 1
            else:
                with open(os.path.join(FT_LOCAL, fname), "w", encoding="utf-8", errors="replace") as f:
                    f.write(text)
                pub["full_text_available"] = "local_only"
                pub["full_text_local_path"] = f"full_text_local_only/{fname}"
                nloc += 1
        else:
            pub["full_text_available"] = "missing"
        public.append(pub)
    C.write_jsonl(os.path.join(C.DATA, "metadata.public.jsonl"), public)
    print(json.dumps({"total": len(recs), "published_full_text": npub,
                      "local_only_full_text": nloc}, indent=2))

if __name__ == "__main__":
    main()
