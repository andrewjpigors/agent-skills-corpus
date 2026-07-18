#!/usr/bin/env python3
"""
common.py — self-contained helpers for the Claude Agent Skills corpus pipeline.

Reproducible: no third-party deps except PyYAML (optional; regex fallback provided).
Auth: uses `gh auth token` (GitHub CLI) so no secret is stored in the repo.
SAFETY: nothing is ever executed. All fetched files are treated as untrusted text.

Rate limits handled by sleeping (resumable). See config.json for all parameters.
"""
import os, re, sys, json, time, hashlib, subprocess, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW  = os.path.join(ROOT, "raw")
DATA = os.path.join(ROOT, "data")
LOGS = os.path.join(ROOT, "logs")
for d in (RAW, DATA, LOGS): os.makedirs(d, exist_ok=True)

with open(os.path.join(HERE, "config.json")) as f:
    CONFIG = json.load(f)

SNAPSHOT_DATE = CONFIG["snapshot_date"]
API = "https://api.github.com"
UA  = "agent-skills-corpus/1.0 (research; contact via repo)"

# ------------------------------------------------------------------ logging
def log(msg, logfile=None):
    from datetime import datetime, timezone
    line = f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z] {msg}"
    print(line, flush=True)
    if logfile:
        with open(logfile, "a") as fh:
            fh.write(line + "\n")

# ------------------------------------------------------------------ auth
def gh_token():
    try:
        t = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    except Exception:
        t = ""
    return t or os.environ.get("GITHUB_TOKEN", "")

TOKEN = gh_token()
HEADERS = {"Accept": "application/vnd.github+json",
           "X-GitHub-Api-Version": "2022-11-28", "User-Agent": UA}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

# ------------------------------------------------------------------ GitHub REST
SEARCH_MIN_INTERVAL = float(CONFIG["sources"]["github_code_search"]["search_min_interval_seconds"])
SECONDARY_SLEEP = 60
_last_search = [0.0]
_core_stats = {"search_calls": 0, "core_calls": 0}

def gh_get(path, params=None, is_search=False, max_retries=5):
    """Authenticated GET with rate-limit/408/secondary-limit handling. Returns (json, status)."""
    url = path if path.startswith("http") else API + "/" + path.lstrip("/")
    if params:
        url += "?" + urllib.parse.urlencode(params)
    for attempt in range(max_retries):
        if is_search:
            wait = SEARCH_MIN_INTERVAL - (time.time() - _last_search[0])
            if wait > 0: time.sleep(wait)
            _last_search[0] = time.time()
            _core_stats["search_calls"] += 1
        else:
            _core_stats["core_calls"] += 1
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8")), 200
        except urllib.error.HTTPError as e:
            code = e.code
            body = e.read().decode("utf-8", "replace")
            rem = e.headers.get("x-ratelimit-remaining")
            reset = e.headers.get("x-ratelimit-reset")
            retry_after = e.headers.get("retry-after")
            if code == 422:                       # beyond 1000 results / invalid range
                return {"_stop": True, "body": body}, 422
            if code in (403, 429):
                if retry_after:
                    time.sleep(min(120, int(retry_after) + 1)); continue
                if rem == "0" and reset:
                    slp = max(2, int(reset) - int(time.time()) + 2)
                    log(f"  rate limit hit; sleeping {min(slp,300)}s"); time.sleep(min(slp, 300)); continue
                if "secondary rate limit" in body.lower():
                    log(f"  secondary rate limit; sleeping {SECONDARY_SLEEP}s"); time.sleep(SECONDARY_SLEEP); continue
                time.sleep(12); continue
            if code == 408:
                time.sleep(4 * (attempt + 1)); continue
            if code == 404:
                return {"_404": True}, 404
            time.sleep(3 * (attempt + 1))
        except Exception:
            time.sleep(3 * (attempt + 1))
    return {"_fail": True}, 0

def raw_get(repo, ref, path, timeout=45):
    """Fetch file bytes from the raw CDN (NOT API-rate-limited). Returns bytes or None."""
    url = f"https://raw.githubusercontent.com/{repo}/{ref}/" + urllib.parse.quote(path)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None

# ------------------------------------------------------------------ frontmatter
try:
    import yaml
    _HAVE_YAML = True
except Exception:
    _HAVE_YAML = False

_FM_RE = re.compile(r"^﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(\r?\n|$)", re.DOTALL)

def split_frontmatter(text):
    """Return (frontmatter_dict_or_None, raw_frontmatter_str_or_None, body).
    frontmatter_dict is None when there is no leading --- ... --- block."""
    m = _FM_RE.match(text)
    if not m:
        return None, None, text
    block = m.group(1)
    body = text[m.end():]
    fm = None
    if _HAVE_YAML:
        try:
            loaded = yaml.safe_load(block)
            if isinstance(loaded, dict):
                fm = {str(k).lower(): v for k, v in loaded.items()}
        except Exception:
            fm = None
    if fm is None:  # regex fallback (line-based; handles simple key: value)
        fm = {}
        key = None
        for ln in block.split("\n"):
            if re.match(r"^\s*-\s+", ln) and key:
                fm.setdefault(key + "__list", []).append(ln.strip()[1:].strip().strip("'\""))
                continue
            km = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", ln)
            if km:
                key = km.group(1).lower().strip()
                val = km.group(2).strip().strip("'\"")
                fm[key] = val if val else fm.get(key, "")
    return fm, block, body

def _as_text(v):
    if v is None: return ""
    if isinstance(v, str): return v.strip()
    if isinstance(v, (int, float, bool)): return str(v).strip()
    if isinstance(v, (list, dict)): return json.dumps(v, ensure_ascii=False).strip()
    return str(v).strip()

TEMPLATE_MARKERS = [m.lower() for m in CONFIG["exclusions"]["template_markers"]]

def classify_skill(text):
    """Apply inclusion criteria. Returns dict with keys:
       included(bool), reason(str), name(str), description(str), has_frontmatter(bool)."""
    out = {"included": False, "reason": "", "has_frontmatter": False,
           "name": "", "description": ""}
    if text is None:
        out["reason"] = "no_content"; return out
    stripped = text.strip()
    if not stripped:
        out["reason"] = "empty_file"; return out
    fm, _, body = split_frontmatter(text)
    if fm is None:
        out["reason"] = "no_frontmatter"; return out
    out["has_frontmatter"] = True
    name = _as_text(fm.get("name"))
    desc = _as_text(fm.get("description") or fm.get("summary") or fm.get("desc"))
    out["name"], out["description"] = name, desc
    if not name:
        out["reason"] = "missing_name"; return out
    if not desc:
        out["reason"] = "missing_description"; return out
    # template / placeholder detection
    hay = (name + " || " + desc).lower()
    body_stripped = body.strip()
    for marker in TEMPLATE_MARKERS:
        if marker in hay:
            out["reason"] = f"template_marker:{marker}"; return out
    # pure placeholder: frontmatter present but body has essentially no real instruction content
    body_wordcount = len(re.findall(r"\w+", body_stripped))
    if body_wordcount < 5 and len(body_stripped) < 40:
        # allow if description itself is substantive; otherwise treat as placeholder
        if len(desc) < 15:
            out["reason"] = "placeholder_no_body"; return out
    out["included"] = True
    out["reason"] = "ok"
    return out

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

_SURROGATE_RE = re.compile(r"[\ud800-\udfff]")
def clean_text(s):
    """Replace lone/unpaired surrogate code points (invalid UTF-8, from malformed source files
    round-tripped through JSON \\uD8xx escapes) with U+FFFD so text can be hashed and serialized."""
    if not isinstance(s, str):
        return s
    return _SURROGATE_RE.sub("�", s)

# ------------------------------------------------------------------ SPDX canonicalization
# GitHub returns canonical SPDX ids (MIT, Apache-2.0); GitLab returns lowercase (mit, apache-2.0).
# Canonicalize so license distribution + publishability matching are consistent across platforms.
_SPDX_KNOWN = [
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "BSD-3-Clause-Clear", "MPL-2.0",
    "ISC", "Unlicense", "CC0-1.0", "0BSD", "CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-4.0",
    "CC-BY-NC-SA-4.0", "GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0", "AGPL-3.0", "BSL-1.0",
    "Zlib", "EPL-2.0", "MPL-2.0", "WTFPL", "NOASSERTION", "OSL-3.0", "MS-PL", "Artistic-2.0",
]
_SPDX_MAP = {s.lower(): s for s in _SPDX_KNOWN}

def canon_spdx(s):
    if not s:
        return ""
    return _SPDX_MAP.get(str(s).strip().lower(), str(s).strip())

# ------------------------------------------------------------------ jsonl helpers
def append_jsonl(path, obj):
    with open(path, "a", encoding="utf-8", errors="replace") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def read_jsonl(path):
    if not os.path.exists(path): return []
    out = []
    with open(path) as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                try: out.append(json.loads(ln))
                except Exception: pass
    return out

def write_jsonl(path, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", errors="replace") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)
