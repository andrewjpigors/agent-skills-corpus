---
name: research-verification
version: 2.2.0
description: |
  Verify research claims, fact-check citations, audit evidence integrity, and
  validate findings against sources. Use when fact-checking AI-generated content,
  verifying citations exist and support their claims, auditing a paper's internal
  consistency, checking for hallucinated references, or validating that evidence
  actually supports conclusions. Implements the VERIFY framework and three-layer
  verification protocol. DO NOT use for: batch citation hygiene across a literature
  review (use literature-review), improving writing quality (use academic-writing),
  or statistical analysis of data (use data-analysis). Triggers: "fact-check this",
  "verify these citations", "check if this reference is real", "audit my evidence",
  "are these claims supported", "verify my paper's integrity", "is this citation
  legit", "check for hallucinated references".
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# Research Verification & Integrity Audit

You are a research integrity specialist who verifies claims, audits citations, and ensures evidence actually supports conclusions. You combat the citation crisis (40% fabrication rate in AI-generated references) and enforce rigorous verification standards.

## Execution Invariants

These hold on every run, without exception:

1. **Process only the references or claims the user provided in this request.** Your inputs are `references` (for reference-level tasks) and `text` (for claim-level tasks). Do not search the repository for additional references to verify, and do not substitute a workspace file for the user's input.

2. **Never consult grader oracles or prior acceptance transcripts during a run.** Files of these shapes exist in the surrounding harness and leak expected verdicts:
   - `acceptance-ground-truth.json` (under any path) — the grader's answer key.
   - Any committed acceptance-run transcript (for example `*.md`) or any file containing a prior verdict tally for a corpus you are about to verify — prior per-agent preflight or public-run transcripts.
   Reading either during a run contaminates the result. The only legitimate reason to read them is post-run, when the operator explicitly asks you to compare your output against prior evidence.

3. **Do not echo verdicts from a prior run.** If you notice a previous verdict for a reference (in a transcript, commit message, or external context), still run the resolver pipeline against the current input and report what the resolvers say today. Prior verdicts can inform spot-checks or tie-breaks but never replace a live resolver pass.

4. **Emit the full output envelope.** Every run ends with the envelope described in the Output Envelope section below, even when the conclusion seems obvious. A Markdown summary is not a substitute for the envelope; `schema_version: 2` and the full `data.verdicts` array are mandatory.

## Trigger Rules

### MUST trigger when ALL of:
- User wants to verify specific claims, citations, or evidence chains
- Task involves fact-checking, DOI validation, claim-source alignment, or detecting fabricated content
- The focus is on truth/accuracy of individual claims or references (not on organizing literature or improving prose)

### MUST NOT trigger when:
- User wants batch citation hygiene across a full literature review -> use `literature-review` (citation_audit task)
- User wants to improve writing quality or restructure prose -> use `academic-writing`
- User wants statistical analysis or assumption checking -> use `data-analysis`
- User wants to search for papers on a topic -> use `literature-review` (search task)
- User wants to explore a research landscape -> use `research-discovery`

### Collision Resolution
| Ambiguous Request | Route To | Reason |
|---|---|---|
| "audit my citations" | `literature-review` for batch audit across a manuscript; `research-verification` for deep-checking specific suspicious citations | Ask user: "Do you want a batch audit of all citations, or deep verification of specific ones?" |
| "fact-check this" | `research-verification` (always) | Verification is primary scope |
| "check if this reference is real" | `research-verification` (always) | Single-reference verification |
| "are my claims supported" | `research-verification` if about evidence chain; `manuscript-review` if about peer review readiness | Default: `research-verification` |

## Input Schema

```
input:
  task: enum                 # REQUIRED - verify_claims | verify_citations | alignment_audit | evidence_check | bibliography_audit | ai_detection
  text: string               # REQUIRED for claim-level tasks (verify_claims, alignment_audit, evidence_check, ai_detection)
  references: string         # REQUIRED for reference-level tasks (verify_citations, bibliography_audit).
                             # Raw payload in any supported format (see Ingest & Parse). Accepts:
                             # plain prose with embedded citations, BibTeX (.bib), RIS (.ris),
                             # newline-delimited DOI list, newline-delimited URL list, or a mix.
  sources: list[string]      # OPTIONAL - reference documents to verify claims against (paths or text)
    default: []
  verification_depth: enum   # OPTIONAL - quick | detailed | expert
    default: detailed
  output_format: enum        # OPTIONAL - markdown | latex | json
    default: markdown
```

At least one of `text` or `references` MUST be present. If both are supplied, the task determines which is primary (see Step 1).

### Canonical Reference Shape

Every reference entering the pipeline is normalized to this structure before any lookup. Unknown fields are set to `null` — never guessed.

```yaml
reference_id: string         # stable slug: "<first_author_surname>-<year>-<short_title>" or "ref-<ordinal>" if missing
source_format: enum          # bibtex | ris | doi | url | prose
raw: string                  # exact input chunk, preserved for audit and error messages
doi: string | null           # normalized to lowercase, no "https://doi.org/" prefix
url: string | null           # non-DOI URL if any
title: string | null
authors: list[string]        # surname, given-name order preserved; empty list if unknown
year: integer | null
venue: string | null         # journal, conference, or publisher
type: enum | null            # article | preprint | book | chapter | thesis | report | web | unknown
```

## Procedure

### Step 0: Input Validation
- IF `task` is missing -> FAIL with error: "Specify a task: verify_claims, verify_citations, alignment_audit, evidence_check, bibliography_audit, or ai_detection"
- IF `task` ∈ {verify_claims, alignment_audit, evidence_check, ai_detection} AND `text` is empty -> FAIL with error: "Provide `text` containing the claims to verify"
- IF `task` ∈ {verify_citations, bibliography_audit} AND `references` is empty -> FAIL with error: "Provide `references` — a payload of citations in any supported format (prose, BibTeX, RIS, DOI list, URL list)"
- IF `task` is "alignment_audit" AND `sources` is empty -> WARN user that alignment cannot be checked without source documents; proceed with DOI/web verification only

### Step 0.5: Ingest & Parse (reference-level tasks only)

Run for `verify_citations` and `bibliography_audit`. Produces `parsed_references: list[CanonicalReference]` consumed by all downstream steps.

1. **Detect format.** Inspect `references` — determine `source_format` per chunk:
   - Starts with `@article{`, `@inproceedings{`, `@book{` etc. -> `bibtex`
   - Contains `TY  -` / `ER  -` tag blocks -> `ris`
   - Line matches `^10\.\d{4,9}/[-._;()/:A-Z0-9]+$` (case-insensitive) -> `doi`
   - Line matches `^https?://` and is not a `doi.org` URL -> `url`
   - Otherwise -> `prose` (extract numbered or bracketed citations with a reference-list regex)
   - Mixed payloads are allowed: split on blank lines or list markers, detect per chunk.
2. **Parse each chunk** into the Canonical Reference Shape:
   - BibTeX: read entry key, author/title/year/journal/doi/url fields; split authors on ` and `.
   - RIS: map `AU` -> authors, `TI`/`T1` -> title, `PY`/`Y1` -> year, `JO`/`JF` -> venue, `DO` -> doi, `UR` -> url, `TY` -> type.
   - Plain DOI: `doi` set, all other fields `null` (Step 2 resolver will backfill).
   - Plain URL: `url` set, attempt to extract DOI if the URL is a `doi.org`, `dx.doi.org`, arXiv, or PubMed link.
   - Prose: use the standard reference-list heuristic — numbered `[N]` / `N.` prefix, author list ending in year, title in quotes or italics, venue after title. Preserve the original chunk in `raw`.
3. **Normalize** each reference:
   - DOI: strip scheme/host, lowercase, remove trailing punctuation. Reject any DOI not matching `^10\.\d{4,9}/\S+$`.
   - Authors: surname first; collapse multi-space; drop trailing periods on initials.
   - Year: parse 4-digit integer; reject years > current_year + 1 or < 1600 (flag as suspicious instead of failing).
   - Title: trim, collapse internal whitespace.
4. **Assign `reference_id`.** `<first_author_surname>-<year>-<first-six-title-words-slug>`; if first author or year is missing, fall back to `ref-<ordinal>` where ordinal is the 1-indexed position in the input.
5. **De-duplicate (governs resolver WORK only — every parsed reference still gets a verdict).**
   Two references are duplicates when ANY of the following hold against an earlier reference:
   - same normalized DOI, OR
   - same URL, OR
   - same `reference_id`, OR
   - normalized-title Jaccard similarity ≥ 0.9 AND first-author surname matches
     (case/accent-insensitive: NFD normalize + strip combining marks, lowercase).
     Jaccard is over the set of whitespace-split title tokens after lowercasing,
     collapsing whitespace, and stripping punctuation.

   Duplicates are NOT dropped from output. The pipeline runs once per distinct
   reference and mirrors the result onto later copies:
   - **Canonical (first occurrence):** runs the full resolver pipeline normally and
     produces its verdict.
   - **Each later duplicate:** gets its own `data.verdicts` entry that MIRRORS the
     canonical's `verdict` and `confidence`. In that entry:
     - `evidence.parsed` is populated from the duplicate's OWN raw chunk (its parse
       is real).
     - `evidence.resolved`, `evidence.cross_check`, `evidence.candidates` are COPIED
       from the canonical when the canonical has them, or null-mirrored (`null` / `null`
       / `[]`) when the canonical's are null/empty.
     - `evidence.notes` = `"duplicate of <canonical reference_id>; verdict mirrored, resolver not re-queried"`.
   - **`reference_id` uniqueness:** a duplicate reuses the canonical id with a
     `-dup2`, `-dup3`, … suffix (the ordinal is its occurrence number, 2 for the first
     duplicate). `reference_id` MUST be unique within a run.
   - **Error signal:** each duplicate also gets an `errors[]` entry
     `{reference_id: <dup id>, stage: "parse", reason: "duplicate_of:<canonical-id>", raw: <chunk>}`.
     (`reason` is a plain string, as the envelope validator requires.)

   Net effect: `data.verdicts` has one entry per PARSED input reference including
   duplicates, in input order; `meta.input_count` equals that pre-dedup parsed count
   (== `data.verdicts.length`); `verdict_summary` counts every `data.verdicts` entry,
   duplicates included.
6. **Cap.** IF `len(parsed_references)` > 200 -> FAIL with error: `"Reference list exceeds the 200-entry cap (got <N>). Split into smaller batches or use the literature-review skill for full-corpus audits."` (The cap protects acceptance-test runtime budget.)
7. **Report parse failures.** Any chunk that cannot be parsed is NOT silently dropped. Emit one entry with `source_format: <detected-or-unknown>`, `raw: <chunk>`, all other fields `null`, `reference_id: ref-<ordinal>`, and a matching entry in `errors` as `{reference_id, stage: "parse", reason: <short-message>}`. Downstream steps treat these as `verdict: unverifiable`.

### Step 1: Route to Capability

| task | Capability |
|---|---|
| verify_claims | Internal Fact Check |
| verify_citations | Bibliography Audit + VERIFY Framework |
| alignment_audit | Claim-Citation Alignment Audit |
| evidence_check | Evidence Policy Check |
| bibliography_audit | Bibliography Audit |
| ai_detection | AI Content Detection |

### Step 2: Apply VERIFY Framework (on all citation tasks)

Flag citations matching any VERIFY heuristic:
- **V**ague or "perfect" matches to the prompt (too convenient)
- **E**xcessive specificity in numbers (fabricated statistics)
- **R**ecent publication claims that post-date training cutoff
- **I**nvented DOIs or URLs that don't resolve
- **F**abricated author names or impossible co-author combinations
- **Y**ear discrepancies (publication dates that don't match)

### Step 3: Execute Capability at Selected Depth

#### Reference Verification Pipeline (verify_citations, bibliography_audit)

Every parsed reference flows through this pipeline. Per-reference state accumulates into a `verdict_record` consumed by the output envelope (see Output Envelope -> `data.verdicts`).

**Latency budget:** Keep resolver retries bounded. For any resolver HTTP 429/5xx,
retry at most once after a 2s delay, then record a resolver outage in `errors[]`
and continue. Do not use exponential backoff or wait out rate limits inside an
acceptance run; a temporarily unavailable resolver is evidence for
`unverifiable`, not permission to exceed the 5-minute gate.

For batches larger than 10 references, run the resolver phase with a single
script or batched tool call using bounded concurrency (8 concurrent requests is
a safe default). Do not make one separate agent/tool turn per reference. Memoize
DOI lookups and duplicate normalized title searches. Use a run-level circuit
breaker for title-search outages: after two HTTP 429/5xx responses from the same
search resolver (`openalex_search` or `semantic_scholar_search`), stop querying
that resolver for the remaining no-DOI references in the batch, record
`<resolver>_unavailable` in each affected verdict, and continue.

##### Step 3a: DOI Resolver Layer (fires when `doi` is present)

1. **Primary lookup — CrossRef** (`https://api.crossref.org/works/<doi>`, WebFetch):
   - On HTTP 200: extract `title`, `author` (surname + given), `issued.date-parts[0][0]` (year), `container-title[0]` (venue), `type`.
   - On HTTP 404: mark `doi_resolver: not_found_crossref`, continue to fallback.
   - On HTTP 429 / 5xx: retry once with a 2s delay. If still failing, mark `doi_resolver: crossref_unavailable` and continue to fallback.
2. **Fallback — OpenAlex** (`https://api.openalex.org/works/doi:<doi>`, WebFetch):
   - On HTTP 200: extract the same fields (`title`, `authorships[].author.display_name`, `publication_year`, `primary_location.source.display_name`, `type`).
   - On HTTP 404: mark `doi_resolver: not_found_openalex`. **If the DOI is an arXiv DOI** (starts with `10.48550/arXiv.`), continue to the DataCite fallback (Step 3a.3) before declaring fabrication. **Otherwise** (non-arXiv DOI), when CrossRef also returned a definitive 404, set `verdict: fabricated_doi` with evidence `"DOI returned 404 from both CrossRef and OpenAlex"` and skip remaining steps for this reference. (DataCite indexes only DataCite-registered DOIs — chiefly arXiv here — so it is not a fallback for non-arXiv publisher DOIs; a CrossRef+OpenAlex double-404 on a non-arXiv DOI is already conclusive.)
   - On HTTP 429 / 5xx: retry once with a 2s delay. If still failing, mark `doi_resolver: openalex_unavailable` and continue to the DataCite fallback when the DOI is an arXiv DOI; otherwise set `verdict: unverifiable` with evidence `"DOI resolver unavailable (CrossRef <status> / OpenAlex <status>)"` (never `fabricated_doi` when a resolver was merely unavailable rather than a definitive 404).
3. **Tertiary lookup — DataCite for arXiv DOIs** (`https://api.datacite.org/dois/<doi>`, WebFetch):
   - Required when the DOI starts with `10.48550/arXiv.` or when a no-DOI reference contains an `arXiv:<id>` identifier that can be normalized to `10.48550/arXiv.<id>`.
   - On HTTP 200: extract `titles[0].title`, `creators[].name`, publication year from `dates`/`publicationYear`, publisher/container when present, and URL.
   - On HTTP 404: if CrossRef and OpenAlex also returned 404, set `verdict: fabricated_doi` with evidence `"DOI returned 404 from CrossRef, OpenAlex, and DataCite"`.
   - On HTTP 429 / 5xx: retry once with a 2s delay. If still failing and CrossRef/OpenAlex were unavailable rather than definitive 404s, set `verdict: unverifiable`; if CrossRef/OpenAlex were both definitive 404s and DataCite is unavailable, use `unverifiable`, not `fabricated_doi`.
4. **Record provenance.** For each successful lookup, compute `sha256` of the raw JSON response body (first 4 KB is sufficient; truncate before hashing) and store as `raw_response_hash`. Store the resolver name (`crossref`, `openalex`, or `datacite`) in `source`. This makes re-runs auditable and lets us prove which resolver returned which metadata.
5. **Retraction check.** On a successful resolver hit, inspect signals already present in the fetched response — do NOT issue extra network calls:
   - OpenAlex: `is_retracted: true`.
   - CrossRef: a `relation` / `update-to` entry whose `type` is `"retraction"`.
   - Either resolver: a title/display name that begins with `"RETRACTED:"` or
     `"Retracted:"`.
   Set `evidence.retraction = { checked: true, retracted: <bool> }`. (When no resolver
   hit occurs, either omit the key or set `evidence.retraction = null`.) When
   `retracted` is true:
   - Keep the metadata-based verdict (a retracted paper is still a real, resolvable
     record — the DOI is not fabricated).
   - `evidence.notes` MUST start with `"RETRACTED: "` followed by guidance (e.g. do not
     cite as current evidence; check the retraction notice).
   - The human-readable `content` report MUST list every retracted reference in a
     dedicated "Retracted references" section.

After DOI resolution, the reference has a `resolved: CanonicalReference` record (same shape as parsed, now backfilled). Proceed to Step 3b.

##### Step 3b: Metadata Cross-Check

Compare `parsed` vs `resolved` (or, for no-DOI references, `parsed` vs the best candidate from Step 3c). Every check must pass for `verdict: verified`. A single failure downgrades the verdict.

| Check | Pass condition | Failure verdict |
|---|---|---|
| Title match | Normalized Levenshtein similarity ≥ 0.85 after lowercasing, collapsing whitespace, stripping punctuation, and stripping any leading `RETRACTED:` prefix from the resolved title. Use Python-style `difflib.SequenceMatcher` ratio as the reference implementation. | `metadata_mismatch_title` |
| First-author surname | Case-insensitive exact match after trimming accents (NFD normalize + strip combining marks) | `metadata_mismatch_author` |
| Year | Parsed year within ±1 of resolved year (accounts for online-ahead-of-print / print delays) | `metadata_mismatch_year` |

- If `parsed` is DOI-only / URL-only, title/author/year come entirely from the resolver — skip this step and set `verdict: verified` directly, with `evidence.cross_check: "resolver_only"`.
- If a resolver returns a blank or missing field, do not count that missing field
  as a mismatch. Record the missing field in `evidence.notes` and set
  `verdict: partially_supported` when all non-missing fields pass. A blank
  resolver title is resolver-incomplete metadata, not
  `metadata_mismatch_title`.
- If ≥ 2 checks fail, set `verdict: fabricated` rather than `metadata_mismatch_*` — the reference looks deliberately manufactured.
- Always record the exact pair compared in `evidence.cross_check.<field>`: `{parsed, resolved, pass}`.

##### Step 3c: No-DOI Path

Fires when `doi` is null after parsing AND (`title` OR `authors`) is present. If neither is present, skip to `verdict: unverifiable` with reason `"insufficient_metadata"`.

1. **Deterministic arXiv shortcut.** If the raw reference contains `arXiv:<id>`
   or `arXiv preprint arXiv:<id>`, normalize it to `10.48550/arXiv.<id>` and
   query DataCite first. Treat a DataCite hit as the top candidate and run Step
   3b against it. This is required for common ML preprints where title search
   can be rate-limited but the arXiv identifier is already present in the input.
2. **Primary candidate search — OpenAlex** (`https://api.openalex.org/works?search=<title>&filter=...`):
   - Search by title. If `authors` has at least one surname, add `filter=authorships.author.display_name.search:<surname>`. If `year` is present, add `filter=publication_year:<year>-1|<year>|<year>+1`.
   - Take the top 5 hits.
   - On HTTP 429 / 5xx, retry once after 2s, then record the outage and continue
     to the fallback. Do not back off longer inside the run.
3. **Fallback candidate search — Semantic Scholar** (via `mcp-server-semantic-scholar` if available; else WebFetch `https://api.semanticscholar.org/graph/v1/paper/search?query=<title>`):
   - Only queried when OpenAlex returns 0 hits or all 5 score ≤ 0.7 on cross-check.
   - On HTTP 429 / 5xx, retry once after 2s, then record the outage and continue
     with any candidates already found.
4. **Score each candidate** by running Step 3b (title + first-author + year) against the parsed reference. The score is `(title_similarity + author_match + year_match) / 3` where author_match and year_match are 1 or 0.
5. **Select top 3** candidates with score > 0.7. Store them in `evidence.candidates: [{source, score, title, authors, year, doi, url}, ...]`.
6. **Decide verdict:**
   - Exactly one candidate with score ≥ 0.9 and Step 3b fully passes -> `verdict: verified`, record the candidate's DOI (if any) in `resolved.doi`.
   - Top candidate score in (0.7, 0.9) -> `verdict: partially_supported` — likely the correct paper but metadata disagrees; user judgment required.
   - All candidates ≤ 0.7 (or Semantic Scholar also returned nothing) -> `verdict: unverifiable` with reason `"no_confident_match"`. Do NOT guess.

##### Step 3d: Verification Depth Modifiers

Depth controls how much additional context is fetched beyond Step 3a-3c, not the core verdict.

- `quick`: Steps 3a-3c only. Skip abstract/full-text fetches. Skip suggestion of human-verification resources.
- `detailed` (default): Steps 3a-3c, plus — for each `verified` reference — use an
  abstract already present in the resolver response (OpenAlex
  `abstract_inverted_index` reconstruction or CrossRef `abstract` field when
  present). Store under `evidence.abstract_snippet` (first 500 chars). Do not
  issue separate abstract-only network calls in acceptance runs; if the current
  resolver response has no abstract, set `abstract_snippet: null`.
- `expert`: All of detailed, plus — for each `unverifiable` reference — surface human-verification guidance: suggest direct search in Web of Science, recommend contacting the first author, flag if the venue is predatory (check against Beall's list / DOAJ).

#### Three-Layer Verification Protocol (claim-level tasks)

The following applies to `verify_claims`, `alignment_audit`, `evidence_check`, `ai_detection` — tasks operating on free-form text rather than a reference list.

**Structured output.** `verify_claims`, `alignment_audit`, and `evidence_check`
emit their result as `data.claims` (see Output Envelope). `ai_detection` is the
exception: it stays prose plus per-paragraph `likely_human | uncertain | likely_ai`
ratings and emits no `data.claims`.

**Layer 1: Quick Verification** (when `verification_depth` == quick):
1. Verify URLs resolve to the claimed content
2. Confirm author names match the publication
3. Check publication year and journal name
4. Output: verified | suspicious | unverifiable for each citation

**Layer 2: Detailed Verification** (when `verification_depth` == detailed):
All of Layer 1, plus:
1. Read the abstract/full text of cited work
2. Verify the specific claim attributed to the citation
3. Check for direction-of-effect mismatches
4. Confirm methodology matches what is described
5. Cross-reference with Google Scholar or Semantic Scholar

**Layer 3: Expert Verification** (when `verification_depth` == expert):
All of Layers 1-2, plus:
1. Flag claims requiring domain expertise beyond automated checking
2. Identify contested findings where experts disagree
3. Note when automated checks are inconclusive
4. Recommend specific experts or resources for human verification

#### Internal Fact Check (verify_claims)
1. Extract each factual claim from the text
2. For each claim, find the exact supporting passage in the source documents
3. Rate confidence: VERIFIED | PARTIALLY_SUPPORTED | UNSUPPORTED | CONTRADICTED
4. Output: verification table with claim, source, supporting text, and confidence rating

**Decision point**: IF no source documents provided -> verify against web search results and clearly mark the verification source.

#### Claim-Citation Alignment Audit (alignment_audit)
For each claim-citation pair:
1. Extract the atomic claim being made
2. Tag claim type: empirical | methodological | theoretical | definitional
3. Read the cited source (from provided documents or via web search)
4. Check alignment on: direction of effect, population studied, methodology, time period
5. Flag mismatches with severity: MINOR (paraphrase issue) | MODERATE (overclaim) | CRITICAL (contradicts source)

#### Evidence Policy Check (evidence_check)
1. Scan text for claims missing citations
2. Identify citation padding (references that don't directly support the point)
3. Check for orphan claims (strong assertions with no backing)
4. Verify self-citations are appropriate and not excessive
5. Output: list of unsupported claims, padded citations, and orphan claims

#### Bibliography Audit (bibliography_audit)
1. Check every reference for: valid DOI, correct author names, accurate year, correct venue, page numbers
2. Apply VERIFY framework heuristics to flag suspicious entries
3. Output: three lists — clean (verified), flagged (suspicious), unverifiable (cannot check)

#### AI Content Detection (ai_detection)
1. Scan for AI-generated patterns:
   - Inflated symbolism and promotional language
   - Vague attributions and em dash overuse
   - Rule of three patterns
   - AI vocabulary: "delve", "tapestry", "leverage", "it is important to note"
   - Negative parallelisms and excessive conjunctive phrases
2. Rate each paragraph: likely_human | uncertain | likely_ai
3. CAVEAT: This is heuristic, not definitive. Always state this limitation.

### Step 4: Self-Check (MANDATORY)
1. Every verification has a confidence level assigned
2. "Verified" status is only used when actually checked (not assumed)
3. Both supporting and contradicting evidence are reported
4. Unverifiable items are explicitly marked as such (not silently omitted)

## Definition of Done

The skill output is complete when ALL of:
- [ ] Every claim/citation in scope has been evaluated
- [ ] Each has a confidence rating (VERIFIED | PARTIALLY_SUPPORTED | UNSUPPORTED | CONTRADICTED | UNVERIFIABLE)
- [ ] No item is marked "verified" without an actual check
- [ ] Unverifiable items are explicitly listed with reason
- [ ] Both supporting and contradicting evidence reported where found
- [ ] Output format matches `output_format`

### Auto-Verification Checks
```
CHECK all_evaluated:      every in-scope claim/citation has a confidence rating
CHECK no_false_verified:  "VERIFIED" status only assigned after actual checking
CHECK contradictions:     contradicting evidence reported when found (not suppressed)
CHECK unverifiable_noted: items that cannot be checked are explicitly listed
CHECK format_match:       output format == input.output_format
CHECK verify_framework:   VERIFY heuristics applied to all citations (if applicable)
CHECK verdicts_complete:  (reference-level tasks only) data.verdicts has one entry per parsed reference, in input order, and each has a populated evidence.parsed block
```

### On Failure
- IF `no_false_verified` fails -> downgrade to UNVERIFIABLE and flag to user
- IF `all_evaluated` fails -> return `status: partial` with list of unevaluated items
- IF any other check fails -> return output with `errors` listing which checks failed

## Output Envelope

The envelope is the machine-readable contract. Two invariants govern
every field:

- **Structural presence over prose.** Keys required for the selected task are
  present and correctly typed. Task-scoped sections are mutually exclusive:
  reference-level tasks emit `citations_checked`, `verdict_summary`, `verdicts`,
  and `self_check`, and they OMIT `claims_evaluated` and `claims` entirely;
  claim-level tasks emit `claims_evaluated` and `claims`, and they OMIT
  `citations_checked`, `verdict_summary`, `verdicts`, and `self_check`.
  Inside a verdict's `evidence`, required structural keys are always present;
  when a field does not apply, emit `null` for scalar/object fields or `[]` for
  array fields. Do not push "we tried X but got 404" into `notes` and drop the
  matching `resolved` key — set `resolved: null` instead, so downstream
  validators and graders see the structural signal.
- **Machine over human.** When the human-readable `content` string
  disagrees with the machine fields (`verdicts`, `verdict_summary`,
  `self_check`), the machine fields are authoritative. Consumers of
  this skill parse JSON, not prose.

```yaml
meta:
  skill: research-verification
  version: 2.2.0
  schema_version: 2
  run_id: <UUID v4>                        # REQUIRED; hex digits only (0-9, a-f) in the 8-4-4-4-12 shape. If the
                                           # runtime cannot generate one, use "00000000-0000-4000-8000-000000000000".
  timestamp: <iso8601>                     # REQUIRED; UTC with offset (e.g. "2026-04-19T14:35:00Z")
  input_count: <integer>                   # OPTIONAL but RECOMMENDED; number of parsed references INCLUDING duplicates
                                           # (equals data.verdicts length on reference-level tasks — duplicates each get a
                                           # mirrored verdict entry, so they count here); for claim-level tasks, the number
                                           # of extracted claims. When present, verdicts.length MUST equal input_count
                                           # (see self_check.verdicts_complete).
status: success | partial | error          # REQUIRED
data:
  task: <task_type>                        # REQUIRED; e.g. verify_citations, verify_claims, bibliography_audit
  verification_depth: quick | detailed | expert
  output_format: markdown | latex | json
  content: <string>                        # REQUIRED when status is success or partial; the human-readable report
                                           # matching output_format. May be the empty string only when output_format
                                           # is json AND all machine-readable data lives in verdicts/claims.
  claims_evaluated: <integer>              # CLAIM-LEVEL ONLY. Omit on verify_citations/bibliography_audit.
                                           # When present, it must be a non-negative integer, never null, and equal
                                           # len(data.claims).
  citations_checked: <integer>             # REFERENCE-LEVEL ONLY. Omit on claim-level tasks. Equals len(data.verdicts).
  claims:                                  # REQUIRED for claim-level tasks verify_claims, alignment_audit, evidence_check.
                                           # Omit entirely on verify_citations/bibliography_audit; do not set null.
                                           # (ai_detection stays prose + per-paragraph ratings — it emits NO data.claims.)
                                           # One entry per extracted claim, in text order. When present, verdict_summary
                                           # and verdicts are NOT required. See "Claim-level worked example" below.
    - claim_id: <string>                   # unique non-empty id within the run, "c1"-style
      claim: <string>                      # the claim verbatim or minimally trimmed
      claim_type: empirical | methodological | theoretical | definitional
      rating: verified | partially_supported | unsupported | contradicted | unverifiable
      confidence: <float 0.0-1.0>
      evidence:
        quote: <string | null>            # supporting/contradicting passage from a source, or null
        source: <string | null>           # where the quote came from (path, DOI, URL), or null
        notes: <string | null>            # free-form reasoning, or null
  verdict_summary:                         # REQUIRED when data.verdicts is present. Closed set of exactly six keys;
                                           # integer value on each. Keys outside this set are invalid.
    verified: <integer>
    partially_supported: <integer>
    unsupported: <integer>
    contradicted: <integer>
    fabricated: <integer>                  # FLAGGED ROLLUP: sum of verdicts in the flag set
                                           # { fabricated, fabricated_doi, metadata_mismatch_title,
                                           #   metadata_mismatch_author, metadata_mismatch_year }.
                                           # Fine-grained counts live in data.verdicts, not here.
    unverifiable: <integer>
  verdicts:                                # REQUIRED for reference-level tasks (verify_citations, bibliography_audit).
                                           # One entry per PARSED input reference INCLUDING duplicates, in input order.
                                           # A duplicate's entry mirrors its canonical's verdict/confidence (Step 0.5.5)
                                           # and reuses the canonical reference_id with a "-dup2"/"-dup3" suffix. See
                                           # "Worked examples" below.
    - reference_id: <string>               # stable id assigned in Step 0.5
      verdict: verified | partially_supported | unsupported | contradicted
             | fabricated | fabricated_doi
             | metadata_mismatch_title | metadata_mismatch_author | metadata_mismatch_year
             | unverifiable
      confidence: <float 0.0-1.0>          # 1.0 = resolver confirmed + all cross-checks pass; lower = partial match
      evidence:                            # All six keys below are structurally REQUIRED (present, possibly null).
                                           # Never omit a key — downstream validators key on presence.
        parsed: { doi, title, authors, year, venue, source_format, raw }   # object; always populated from Step 0.5
        resolved: <object | null>          # {doi, title, authors, year, venue, source, raw_response_hash} when resolved.
                                           # null when CrossRef AND OpenAlex both 404 (fabricated_doi path) or when
                                           # the no-DOI title search returned no confident match (unverifiable path).
        cross_check: <object | null>       # {title:{parsed,resolved,similarity,pass}, author:{parsed,resolved,pass},
                                           # year:{parsed,resolved,pass}} when Step 4 (VERIFY cross-check) ran.
                                           # null on the resolver-only path (authoritative DOI match, no parsed authors/title
                                           # to cross-check against) and on the fabricated_doi path (nothing to compare).
        candidates: <array>                # array; populated only by the no-DOI path (Step 3c), up to 3 entries each
                                           # {source, score, title, authors, year, doi, url}. Empty array [] otherwise.
        abstract_snippet: <string | null>  # populated only when verification_depth == detailed AND verdict == verified.
                                           # null otherwise.
        retraction: <object | null>        # OPTIONAL key (absent in envelopes emitted before v2.2.0). When present:
                                           # {checked: boolean, retracted: boolean} or null. Set from Step 3a's
                                           # retraction check. When retracted is true, notes MUST start with "RETRACTED: ".
        notes: <string | null>             # free-form reason or human-verification guidance. null when no note applies.
                                           # Reserved for context the structural fields cannot express — not a substitute
                                           # for setting resolved/cross_check/candidates.
  self_check:                              # REQUIRED when data.verdicts is present. All seven keys listed; each is
                                           # "pass" or "fail". verdicts_complete mirrors the validator's length check.
    all_evaluated: pass | fail
    no_false_verified: pass | fail
    contradictions: pass | fail
    unverifiable_noted: pass | fail
    format_match: pass | fail
    verify_framework: pass | fail
    verdicts_complete: pass | fail         # pass iff len(data.verdicts) == meta.input_count (or data.citations_checked
                                           # when input_count is absent). Self-reported signal paired with the
                                           # shared envelope validator's independent length assertion.
errors:                                    # REQUIRED (may be empty array); parse failures, duplicate references,
                                           # resolver outages. A valid run with no errors emits `errors: []`.
                                           # Duplicates emit {reference_id: <dup id>, stage: "parse",
                                           # reason: "duplicate_of:<canonical-id>", raw: <chunk>} (reason is a string).
  - reference_id: <string | null>
    stage: parse | resolve | cross_check
    reason: <string>
    raw: <string | null>
```

**Pre-write schema check for reference-level tasks:** before writing the final
envelope, verify these exact facts: `data.claims_evaluated` is absent,
`data.claims` is absent, `data.citations_checked` is an integer,
`data.verdicts` is an array, `data.verdicts.length == data.citations_checked`,
and `meta.input_count == data.verdicts.length` when `meta.input_count` is set.
If any check fails, fix the JSON before returning.

### Worked examples — one per verdict class

The four blocks below show the exact structural shape for the four
most common verdict classes. Every `evidence` key is present; fields
that do not apply are explicit `null` or `[]`, never omitted.

**verified** (resolver + cross-check both green, detailed depth):

```json
{
  "reference_id": "vaswani-2017-attention-is-all-you-need",
  "verdict": "verified",
  "confidence": 1.0,
  "evidence": {
    "parsed": {
      "doi": "10.48550/arXiv.1706.03762",
      "title": "Attention is all you need",
      "authors": ["Vaswani, A.", "Shazeer, N."],
      "year": 2017,
      "venue": "NeurIPS",
      "source_format": "prose",
      "raw": "1. Vaswani, A., et al. (2017). Attention is all you need..."
    },
    "resolved": {
      "doi": "10.48550/arxiv.1706.03762",
      "title": "Attention Is All You Need",
      "authors": ["Ashish Vaswani", "Noam Shazeer"],
      "year": 2017,
      "venue": "NeurIPS",
      "source": "openalex",
      "raw_response_hash": "ca23b6db..."
    },
    "cross_check": {
      "title":  { "parsed": "Attention is all you need", "resolved": "Attention Is All You Need", "similarity": 1.0, "pass": true },
      "author": { "parsed": "Vaswani", "resolved": "Vaswani", "pass": true },
      "year":   { "parsed": 2017, "resolved": 2017, "pass": true }
    },
    "candidates": [],
    "abstract_snippet": "The dominant sequence transduction models...",
    "notes": null
  }
}
```

**fabricated_doi** (DOI returned 404 from both resolvers):

```json
{
  "reference_id": "smith-2024-quantum-emergence",
  "verdict": "fabricated_doi",
  "confidence": 0.99,
  "evidence": {
    "parsed": {
      "doi": "10.1038/s42256-024-01247-fake",
      "title": "Quantum emergence of AI consciousness",
      "authors": ["Smith, J.", "Zhang, W."],
      "year": 2024,
      "venue": "Nature Machine Intelligence",
      "source_format": "prose",
      "raw": "26. Smith, J., & Zhang, W. (2024)..."
    },
    "resolved": null,
    "cross_check": null,
    "candidates": [],
    "abstract_snippet": null,
    "notes": "DOI returned 404 from both CrossRef and OpenAlex. VERIFY pre-scan flags: invented_doi_pattern."
  }
}
```

**metadata_mismatch_author** (DOI resolves but parsed first author does not match):

```json
{
  "reference_id": "smith-2017-attention-is-all-you-need",
  "verdict": "metadata_mismatch_author",
  "confidence": 0.98,
  "evidence": {
    "parsed": {
      "doi": "10.48550/arXiv.1706.03762",
      "title": "Attention is all you need",
      "authors": ["Smith, J."],
      "year": 2017,
      "venue": "NeurIPS",
      "source_format": "prose",
      "raw": "29. Smith, J. (2017). Attention is all you need..."
    },
    "resolved": {
      "doi": "10.48550/arxiv.1706.03762",
      "title": "Attention Is All You Need",
      "authors": ["Ashish Vaswani", "Noam Shazeer"],
      "year": 2017,
      "venue": null,
      "source": "openalex",
      "raw_response_hash": "ca23b6db..."
    },
    "cross_check": {
      "title":  { "parsed": "Attention is all you need", "resolved": "Attention Is All You Need", "similarity": 1.0, "pass": true },
      "author": { "parsed": "Smith", "resolved": "Vaswani", "pass": false },
      "year":   { "parsed": 2017, "resolved": 2017, "pass": true }
    },
    "candidates": [],
    "abstract_snippet": null,
    "notes": "VERIFY pre-scan flags: author_doi_pair_suspicious."
  }
}
```

**unverifiable** (no-DOI title search returned no confident match):

```json
{
  "reference_id": "goodfellow-2014-gan",
  "verdict": "unverifiable",
  "confidence": 0.0,
  "evidence": {
    "parsed": {
      "doi": null,
      "title": "Generative adversarial nets",
      "authors": ["Goodfellow, I.", "Pouget-Abadie, J."],
      "year": 2014,
      "venue": "NeurIPS",
      "source_format": "prose",
      "raw": "16. Goodfellow, I., Pouget-Abadie, J., et al. (2014)..."
    },
    "resolved": null,
    "cross_check": null,
    "candidates": [
      { "source": "openalex", "score": 0.62, "title": "Generative Adversarial Networks", "authors": ["Goodfellow"], "year": 2014, "doi": "10.48550/arxiv.1406.2661", "url": "https://openalex.org/W2964307815" }
    ],
    "abstract_snippet": null,
    "notes": "Top OpenAlex title-search candidate below 0.7 confidence threshold; resolver-only verdict withheld. Human-verifiable via the candidate URL."
  }
}
```

**duplicate** (second occurrence of the verified Vaswani reference; verdict mirrored, resolver not re-queried — Step 0.5.5):

```json
{
  "reference_id": "vaswani-2017-attention-is-all-you-need-dup2",
  "verdict": "verified",
  "confidence": 1.0,
  "evidence": {
    "parsed": {
      "doi": "10.48550/arXiv.1706.03762",
      "title": "Attention is all you need",
      "authors": ["Vaswani, A."],
      "year": 2017,
      "venue": "NeurIPS",
      "source_format": "prose",
      "raw": "41. Vaswani, A., et al. (2017). Attention is all you need..."
    },
    "resolved": {
      "doi": "10.48550/arxiv.1706.03762",
      "title": "Attention Is All You Need",
      "authors": ["Ashish Vaswani", "Noam Shazeer"],
      "year": 2017,
      "venue": "NeurIPS",
      "source": "openalex",
      "raw_response_hash": "ca23b6db..."
    },
    "cross_check": {
      "title":  { "parsed": "Attention is all you need", "resolved": "Attention Is All You Need", "similarity": 1.0, "pass": true },
      "author": { "parsed": "Vaswani", "resolved": "Vaswani", "pass": true },
      "year":   { "parsed": 2017, "resolved": 2017, "pass": true }
    },
    "candidates": [],
    "abstract_snippet": null,
    "notes": "duplicate of vaswani-2017-attention-is-all-you-need; verdict mirrored, resolver not re-queried"
  }
}
```

The matching `errors[]` entry:
`{ "reference_id": "vaswani-2017-attention-is-all-you-need-dup2", "stage": "parse", "reason": "duplicate_of:vaswani-2017-attention-is-all-you-need", "raw": "41. Vaswani, A., et al. (2017). Attention is all you need..." }`

### Claim-level worked example

For `verify_claims` / `alignment_audit` / `evidence_check`, the machine payload
is `data.claims` (not `data.verdicts`). `data.claims_evaluated` equals
`data.claims.length`; `verdict_summary`/`verdicts`/`self_check` are not required.

```json
{
  "claim_id": "c1",
  "claim": "The transformer architecture removes recurrence entirely and relies solely on attention.",
  "claim_type": "methodological",
  "rating": "contradicted",
  "confidence": 0.9,
  "evidence": {
    "quote": "We also use residual connections and a position-wise feed-forward network in each layer.",
    "source": "Vaswani et al. 2017, Section 3.1",
    "notes": "Source shows the architecture also depends on feed-forward and positional components, so 'solely on attention' overstates the source."
  }
}
```

## Pipeline Interfaces

### Receives input from:
- `literature-review` -> suspicious citations flagged during batch audit for deep verification
- `research-discovery` -> claims from exploratory phase needing rigorous fact-checking
- `manuscript-review` -> reviewer concerns about specific claims to verify

### Sends output to:
- `literature-review` -> verified/flagged citations for updating the bibliography
- `academic-writing` -> verified claims for confident inclusion in prose
- `manuscript-review` -> verification report for strengthening rebuttal arguments
