#!/usr/bin/env bash
# Reproduce the full corpus build. Resumable & idempotent: safe to re-run.
# Requires: python3 + PyYAML, and `gh` authenticated (public-repo read scope).
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/8] GitHub size-sharded enumeration"
ENUM_SEARCH_BUDGET="${ENUM_SEARCH_BUDGET:-900}" python3 01_github_enumerate.py

echo "[2/8] Merge marketplace + sourcegraph GitHub pointers"
python3 04_merge_github_candidates.py

echo "[3/8] Enrich repos (metadata + trees)"
ENRICH_CORE_BUDGET="${ENRICH_CORE_BUDGET:-40000}" MAX_SKILLS_PER_REPO="${MAX_SKILLS_PER_REPO:-300}" python3 02_enrich.py

echo "[4/8] Fetch SKILL.md full text (raw CDN)"
python3 03_fetch_content.py

echo "[5/8] Build corpus (filter + fork-exclude + content-hash dedup)"
python3 05_build_corpus.py

echo "[6/8] File-level last-commit dates for the final set"
DATE_CORE_BUDGET="${DATE_CORE_BUDGET:-5000}" python3 05b_date_final.py

echo "[7/9] Statistics"
python3 06_stats.py

echo "[8/9] Two-axis classification (functional category + agent platform)"
python3 09_classify.py

echo "[9/9] Categorized layout: full_text/<category>/ + by_category + public metadata"
python3 10_reorganize_by_category.py

echo "DONE. See data/metadata.public.jsonl.gz, data/by_category/, full_text/, stats/STATS.md"
