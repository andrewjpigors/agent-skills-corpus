#!/usr/bin/env python3
"""
02_enrich.py — per-repo metadata + recursive git tree enrichment.

For each unique repo among the candidates:
  * GET repos/{repo}         -> stars, SPDX license, fork flag, created_at, pushed_at,
                                default_branch, owner login/type.
  * GET git/trees/{branch}?recursive=1
        -> every SKILL.md path in the repo (augments code-search; catches missed files),
           blob sha, and same-directory sibling file list for each SKILL.md dir.
        -> on truncation, fall back to contents API for known skill dirs.

Output raw/repos.jsonl : one JSON object per repo:
  {repo, owner, owner_type, stars, license_spdx, is_fork, default_branch,
   created_at, pushed_at, tree_truncated, skills:[{path, skill_dir, sha, siblings:[{name,type}]}]}

Resumable: repos already present in raw/repos.jsonl are skipped.
Env: ENRICH_CORE_BUDGET (default from config), ENRICH_MAX_RUNTIME.
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

CAND_PATH  = os.path.join(C.RAW, "github_candidates.jsonl")
REPOS_PATH = os.path.join(C.RAW, "repos.jsonl")
LOGFILE    = os.path.join(C.LOGS, "02_enrich.log")
BUDGET      = int(os.environ.get("ENRICH_CORE_BUDGET", C.CONFIG["budgets"]["github_core_calls_soft"]))
MAX_RUNTIME = int(os.environ.get("ENRICH_MAX_RUNTIME", 999999))
# Vendored mega-registries (e.g. majiayu000/claude-skill-registry ~203k SKILL.md) would
# otherwise dominate fetch time. Cap SKILL.md paths recorded per repo; flag capped repos.
# Content-hash dedup attributes each unique skill to its earliest source regardless.
MAX_SKILLS_PER_REPO = int(os.environ.get("MAX_SKILLS_PER_REPO", "300"))
T0 = time.time()

def dirname(p): return p.rsplit("/", 1)[0] if "/" in p else ""

def siblings_from_tree(tree, skill_dir):
    """Immediate children (files + subdirs) of skill_dir."""
    prefix = (skill_dir + "/") if skill_dir else ""
    out = []
    for e in tree:
        p = e.get("path", "")
        if not p.startswith(prefix): continue
        rest = p[len(prefix):]
        if "/" in rest:  # not an immediate child
            continue
        if not rest:
            continue
        out.append({"name": rest, "type": "dir" if e.get("type") == "tree" else "file"})
    return out

def siblings_via_contents(repo, branch, skill_dir):
    data, st = C.gh_get(f"repos/{repo}/contents/{skill_dir}", {"ref": branch})
    if st != 200 or not isinstance(data, list):
        return []
    return [{"name": d.get("name", ""), "type": "dir" if d.get("type") == "dir" else "file"} for d in data]

def main():
    cands = C.read_jsonl(CAND_PATH)
    # group candidate SKILL.md paths by repo. Repo-only seeds (path empty / non-SKILL.md,
    # e.g. from a marketplace that only knew the repo) still create a repo entry so the repo
    # gets enriched and its tree is scanned for the real SKILL.md paths.
    by_repo = {}
    for c in cands:
        repo = c.get("repo", "")
        if not repo:
            continue
        s = by_repo.setdefault(repo, set())
        p = c.get("path", "")
        if p and p.rsplit("/", 1)[-1] == "SKILL.md":
            s.add(p)
    done = {r["repo"] for r in C.read_jsonl(REPOS_PATH)}
    todo = [r for r in by_repo if r not in done]
    C.log(f"== enrich start: {len(by_repo)} repos total, {len(done)} done, {len(todo)} todo, budget={BUDGET} ==", LOGFILE)
    calls0 = C._core_stats["core_calls"]
    processed = 0
    for repo in todo:
        if C._core_stats["core_calls"] - calls0 >= BUDGET:
            C.log(f"  core budget reached; pausing (resumable) at {processed} repos.", LOGFILE); break
        if time.time() - T0 > MAX_RUNTIME:
            C.log("  runtime cap; pausing.", LOGFILE); break
        meta, st = C.gh_get(f"repos/{repo}")
        if st != 200 or not isinstance(meta, dict) or meta.get("_404") or meta.get("_fail"):
            # record a stub so we don't retry forever; mark unavailable
            C.append_jsonl(REPOS_PATH, {"repo": repo, "unavailable": True, "http": st,
                                        "skills": [{"path": p, "skill_dir": dirname(p), "sha": "", "siblings": []}
                                                   for p in sorted(by_repo[repo])]})
            processed += 1; continue
        lic = (meta.get("license") or {})
        branch = meta.get("default_branch", "main")
        tree, st2 = C.gh_get(f"repos/{repo}/git/trees/{branch}", {"recursive": "1"})
        truncated = False
        tree_entries = []
        if st2 == 200 and isinstance(tree, dict) and "tree" in tree:
            tree_entries = tree["tree"]; truncated = tree.get("truncated", False)
        # all exact-basename SKILL.md paths from the tree (augments code search)
        tree_skillmd = {e["path"]: e.get("sha", "") for e in tree_entries
                        if e.get("type") == "blob" and e.get("path", "").rsplit("/", 1)[-1] == "SKILL.md"}
        all_paths_full = sorted(set(by_repo[repo]) | set(tree_skillmd.keys()))
        skills_capped = len(all_paths_full) > MAX_SKILLS_PER_REPO
        # keep code-search-confirmed paths first, then tree-only, up to the cap
        confirmed = [p for p in all_paths_full if p in by_repo[repo]]
        tree_only = [p for p in all_paths_full if p not in by_repo[repo]]
        all_paths = (confirmed + tree_only)[:MAX_SKILLS_PER_REPO]
        skills = []
        for p in sorted(all_paths):
            sd = dirname(p)
            sha = tree_skillmd.get(p, "")
            if tree_entries and not truncated:
                sib = siblings_from_tree(tree_entries, sd)
            elif truncated and (C._core_stats["core_calls"] - calls0) < BUDGET:
                sib = siblings_via_contents(repo, branch, sd)
            else:
                sib = []
            skills.append({"path": p, "skill_dir": sd, "sha": sha, "siblings": sib,
                           "from_tree_only": p not in by_repo[repo]})
        rec = {
            "repo": repo,
            "owner": meta.get("owner", {}).get("login", ""),
            "owner_type": meta.get("owner", {}).get("type", ""),
            "stars": meta.get("stargazers_count", 0),
            "license_spdx": lic.get("spdx_id") or "",
            "license_name": lic.get("name") or "",
            "is_fork": bool(meta.get("fork", False)),
            "default_branch": branch,
            "created_at": meta.get("created_at", ""),
            "pushed_at": meta.get("pushed_at", ""),
            "updated_at": meta.get("updated_at", ""),
            "tree_truncated": truncated,
            "skills_capped": skills_capped,
            "total_skillmd_in_repo": len(all_paths_full),
            "skills": skills,
        }
        C.append_jsonl(REPOS_PATH, rec)
        processed += 1
        if processed % 25 == 0:
            C.log(f"  enriched {processed}/{len(todo)} (core_calls={C._core_stats['core_calls']-calls0}, "
                  f"last={repo}, skills={len(skills)})", LOGFILE)
    C.log(f"== enrich pause/done: processed {processed}, core_calls={C._core_stats['core_calls']-calls0} ==", LOGFILE)
    print(json.dumps({"processed": processed, "core_calls": C._core_stats['core_calls'] - calls0,
                      "repos_done_total": len(done) + processed, "repos_total": len(by_repo)}))

if __name__ == "__main__":
    main()
