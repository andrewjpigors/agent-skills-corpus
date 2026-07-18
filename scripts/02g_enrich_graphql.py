#!/usr/bin/env python3
"""
02g_enrich_graphql.py — FAST GitHub enrichment via the GraphQL API.

At ~20k repos, REST (repos/{repo} + recursive tree, and a contents call per skill dir when a
tree is truncated) costs ~2-15 core calls/repo -> many hours. GraphQL fetches, in ONE batched
query per ~25 repos: repo metadata (stars, SPDX license, fork/archived flags, created/pushed/
updated, default branch, owner type) + for each SKILL.md: its full text (Blob.text) AND its
same-directory sibling listing (Tree.entries). Cost is ~1 point/query -> the whole set in minutes.

Trade-off vs REST: GraphQL Tree is not recursive, so this does NOT discover SKILL.md files that
code search missed (the REST path in 02_enrich does). We rely on the 70k code-search candidate
paths instead; this is documented as a coverage choice.

Writes (compatible with the REST stage 02/03 schemas so 05_build_corpus works unchanged):
  raw/repos.jsonl    (repo metadata + skills[] with siblings)
  raw/content.jsonl  (SKILL.md text + content_sha256)
Resumable: repos already in raw/repos.jsonl are skipped.

Env: GQL_SKILLS_CAP (per-repo skill lookups, default 100), GQL_REPOS_PER_BATCH (default 25),
     GQL_MAX_RUNTIME (seconds).
"""
import os, sys, json, time, zlib, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

# Sharding for safe parallelism: run N instances with SHARD_N=N and SHARD_I=0..N-1, each with a
# distinct OUT_SUFFIX. Repos are partitioned by crc32(repo)%N (disjoint). Concatenate shard files
# into raw/repos.jsonl / raw/content.jsonl afterwards.
SHARD_N = int(os.environ.get("SHARD_N", "1"))
SHARD_I = int(os.environ.get("SHARD_I", "0"))
SUFFIX  = os.environ.get("OUT_SUFFIX", "")

CAND_PATH    = os.path.join(C.RAW, "github_candidates.jsonl")
REPOS_MAIN   = os.path.join(C.RAW, "repos.jsonl")          # REST-enriched repos already here
REPOS_PATH   = os.path.join(C.RAW, "repos.jsonl" + SUFFIX)
CONTENT_PATH = os.path.join(C.RAW, "content.jsonl" + SUFFIX)
LOGFILE      = os.path.join(C.LOGS, "02g_enrich_graphql.log")
GQL_URL      = "https://api.github.com/graphql"
SKILLS_CAP       = int(os.environ.get("GQL_SKILLS_CAP", "100"))
REPOS_PER_BATCH  = int(os.environ.get("GQL_REPOS_PER_BATCH", "25"))
MAX_RUNTIME      = int(os.environ.get("GQL_MAX_RUNTIME", "999999"))
MAX_BYTES        = 800_000
T0 = time.time()

def dirname(p): return p.rsplit("/", 1)[0] if "/" in p else ""

def gql(query, max_retries=6):
    body = json.dumps({"query": query}).encode()
    for attempt in range(max_retries):
        req = urllib.request.Request(GQL_URL, data=body, method="POST",
                                     headers={**C.HEADERS, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            code = e.code
            txt = e.read().decode("utf-8", "replace")
            reset = e.headers.get("x-ratelimit-reset")
            if code in (403, 429):
                if reset:
                    slp = max(2, int(reset) - int(time.time()) + 2)
                    C.log(f"  gql rate limit; sleeping {min(slp,300)}s", LOGFILE); time.sleep(min(slp, 300)); continue
                time.sleep(20); continue
            if code == 502 or code == 500:  # server hiccup on big query
                time.sleep(3 * (attempt + 1)); continue
            C.log(f"  gql HTTP {code}: {txt[:180]}", LOGFILE)
            time.sleep(3 * (attempt + 1))
        except Exception as ex:
            time.sleep(3 * (attempt + 1))
    return None

def build_query(batch):
    """batch: list of (repo, [skill_paths]). Returns (query_str, index_map)."""
    parts = []
    for i, (repo, paths) in enumerate(batch):
        owner, name = repo.split("/", 1)
        blk = [f'r{i}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) {{',
               '  stargazerCount isFork isArchived createdAt pushedAt updatedAt',
               '  owner { login __typename } licenseInfo { spdxId name } defaultBranchRef { name }']
        for j, p in enumerate(paths):
            d = dirname(p)
            blk.append(f'  b{j}: object(expression: {json.dumps("HEAD:" + p)}) '
                       f'{{ ... on Blob {{ text byteSize isBinary oid }} }}')
            blk.append(f'  t{j}: object(expression: {json.dumps("HEAD:" + d)}) '
                       f'{{ ... on Tree {{ entries {{ name type }} }} }}')
        blk.append('}')
        parts.append("\n".join(blk))
    q = "{\n" + "\n".join(parts) + "\n  rateLimit { cost remaining resetAt }\n}"
    return q

def process_batch(batch, capped_map):
    q = build_query(batch)
    resp = gql(q)
    if resp is None:
        return 0, 0, None
    data = (resp or {}).get("data") or {}
    rl = data.get("rateLimit") or {}
    nrepos = ncontent = 0
    for i, (repo, paths) in enumerate(batch):
        node = data.get(f"r{i}")
        if not node:
            C.append_jsonl(REPOS_PATH, {"repo": repo, "unavailable": True, "http": "gql_null",
                                        "skills": [{"path": p, "skill_dir": dirname(p), "sha": "", "siblings": []}
                                                   for p in paths]})
            nrepos += 1
            continue
        lic = node.get("licenseInfo") or {}
        branch = ((node.get("defaultBranchRef") or {}) or {}).get("name") or "HEAD"
        owner = node.get("owner") or {}
        skills = []
        for j, p in enumerate(paths):
            d = dirname(p)
            blob = node.get(f"b{j}") or {}
            tree = node.get(f"t{j}") or {}
            entries = tree.get("entries") if isinstance(tree, dict) else None
            siblings = [{"name": e.get("name", ""), "type": "dir" if e.get("type") == "tree" else "file"}
                        for e in (entries or [])]
            skills.append({"path": p, "skill_dir": d, "sha": blob.get("oid", ""),
                           "siblings": siblings, "from_tree_only": False})
            # content
            text = blob.get("text")
            if text is not None and not blob.get("isBinary"):
                b = text.encode("utf-8", "replace")
                truncated = len(b) > MAX_BYTES
                if truncated:
                    text = b[:MAX_BYTES].decode("utf-8", "replace")
                C.append_jsonl(CONTENT_PATH, {"repo": repo, "path": p, "ref": branch,
                                              "content_sha256": C.sha256_bytes(b),
                                              "n_bytes": blob.get("byteSize", len(b)),
                                              "truncated": truncated, "fetch_source": "graphql", "text": text})
                ncontent += 1
            else:
                C.append_jsonl(CONTENT_PATH, {"repo": repo, "path": p, "ref": branch,
                                              "content_sha256": "", "n_bytes": blob.get("byteSize", 0),
                                              "truncated": False, "fetch_source": "graphql_binary_or_missing",
                                              "text": None})
        rec = {"repo": repo, "owner": owner.get("login", ""), "owner_type": owner.get("__typename", ""),
               "stars": node.get("stargazerCount", 0),
               "license_spdx": (lic.get("spdxId") or "") if lic.get("spdxId") not in ("NOASSERTION",) else "NOASSERTION",
               "license_name": lic.get("name") or "",
               "is_fork": bool(node.get("isFork", False)), "is_archived": bool(node.get("isArchived", False)),
               "default_branch": branch, "created_at": node.get("createdAt", ""),
               "pushed_at": node.get("pushedAt", ""), "updated_at": node.get("updatedAt", ""),
               "tree_truncated": False, "skills_capped": capped_map.get(repo, False),
               "total_skillmd_in_repo": capped_map.get(repo + "::total", len(paths)),
               "enrich_source": "graphql", "skills": skills}
        C.append_jsonl(REPOS_PATH, rec)
        nrepos += 1
    return nrepos, ncontent, rl

def main():
    cands = C.read_jsonl(CAND_PATH)
    by_repo = {}
    for c in cands:
        repo = c.get("repo", "")
        if not repo: continue
        p = c.get("path", "")
        s = by_repo.setdefault(repo, set())
        if p and p.rsplit("/", 1)[-1] == "SKILL.md":
            s.add(p)
    done = {r["repo"] for r in C.read_jsonl(REPOS_MAIN)}
    if SUFFIX:
        done |= {r["repo"] for r in C.read_jsonl(REPOS_PATH)}
    todo = [r for r in by_repo if r not in done]
    if SHARD_N > 1:
        todo = [r for r in todo if zlib.crc32(r.encode()) % SHARD_N == SHARD_I]
    C.log(f"== gql enrich [shard {SHARD_I}/{SHARD_N}]: {len(by_repo)} repos total, "
          f"{len(done)} done, {len(todo)} todo ==", LOGFILE)

    # build capped work items
    capped_map = {}
    work = []
    for repo in todo:
        paths = sorted(by_repo[repo])
        if len(paths) > SKILLS_CAP:
            capped_map[repo] = True
            capped_map[repo + "::total"] = len(paths)
            paths = paths[:SKILLS_CAP]
        work.append((repo, paths))

    batch, alias_budget = [], 0
    total_repos = total_content = 0
    processed = 0
    for item in work:
        batch.append(item); alias_budget += 2 * len(item[1]) + 1
        if len(batch) >= REPOS_PER_BATCH or alias_budget >= 180:
            nr, nc, rl = process_batch(batch, capped_map)
            total_repos += nr; total_content += nc; processed += len(batch)
            if rl and rl.get("remaining", 1) is not None and rl.get("remaining", 9999) < 50:
                slp = max(2, int(time.mktime(time.strptime(rl["resetAt"], "%Y-%m-%dT%H:%M:%SZ")) - time.time()) + 2) if rl.get("resetAt") else 60
                C.log(f"  gql points low ({rl.get('remaining')}); sleeping {min(slp,300)}s", LOGFILE); time.sleep(min(slp, 300))
            if processed % 500 < REPOS_PER_BATCH:
                C.log(f"  gql enriched ~{processed}/{len(work)} (repos+={total_repos}, content+={total_content}, "
                      f"pts_left={rl.get('remaining') if rl else '?'})", LOGFILE)
            batch, alias_budget = [], 0
        if time.time() - T0 > MAX_RUNTIME:
            C.log("  runtime cap; pausing (resumable)", LOGFILE); break
    if batch:
        nr, nc, rl = process_batch(batch, capped_map); total_repos += nr; total_content += nc
    C.log(f"== gql enrich done: repos={total_repos}, content={total_content} ==", LOGFILE)
    print(json.dumps({"repos_enriched": total_repos, "content_written": total_content,
                      "repos_done_total": len(done) + total_repos, "repos_total": len(by_repo)}))

if __name__ == "__main__":
    main()
