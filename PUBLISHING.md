# Publishing & licensing policy

This corpus separates **redistributable** artifacts from **local-only** ones by each skill's source
repository license.

## Published in this repository

| Artifact | Notes |
|---|---|
| `data/metadata.public.jsonl.gz` | Master metadata table — all 55,698 unique skills (metadata + category + agent_platform + full-text pointer; `skill_md_text` is null). `gunzip` → ~103 MiB. |
| `data/by_category/<category>.jsonl` | The same records split per functional category (browsable). |
| `full_text/<category>/…md` | Full `SKILL.md` text of the **29,205** skills whose source repo carries a clear open-source / Creative-Commons license, organized by category. |
| `data/duplicates.jsonl`, `data/excluded.jsonl`, `data/build_report.json` | Duplicate provenance, exclusions, pipeline counts. |
| `data/classification.jsonl`, `data/taxonomy.json` | Per-skill labels + exact rules. |
| `scripts/`, `docs/`, `stats/` | Reproducible pipeline, methodology, statistics. |
| `LICENSE` (CC0-1.0), `scripts/LICENSE` (MIT), `CITATION.cff` | Licensing & citation. |

## Never redistributed (git-ignored, local-only)

- `full_text_local_only/<category>/…md` — full text of the **26,493** skills whose source repo has
  **no clear license**. Retained locally for analysis only; **not** redistributed. The published
  metadata still lists these skills (with `full_text_available: "local_only"`), so their provenance
  and `content_sha256` are public and anyone can re-fetch the text from the source themselves.
- `data/metadata.jsonl` — the full local corpus, which inlines **all** text (incl. no-license).
- `raw/` — intermediate API pull (regenerable from `scripts/`).
- `data/metadata.public.jsonl` (uncompressed, ~103 MiB > GitHub's 100 MiB file limit) — the tracked
  form is the `.gz`.

## Licensing summary

CC0 1.0 covers this project's **compilation and metadata**. It does **not** override the upstream
copyright of the third-party `SKILL.md` texts under `full_text/` — each remains under its source
repository's license (`license_spdx` per record). Reuse each skill per its own license.

## Reproducibility

The entire corpus (including local-only parts) is regenerable from `scripts/` + `scripts/config.json`
at the fixed `2026-07-18` snapshot. Each published record's `content_sha256` lets a third party
re-fetch and verify any skill's text independently.
