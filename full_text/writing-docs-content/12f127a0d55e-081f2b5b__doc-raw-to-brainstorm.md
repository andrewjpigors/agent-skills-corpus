---
name: doc-raw-to-brainstorm
description: "Transform raw unstructured context (API docs, PO notes, contributor guidelines, reference implementations) into a complete three-layer vault structure: OoB zettels, derived zettels, chunk notes, and a clean brainstorm — all from scratch, without pre-existing zettels."
interaction_model: multi-turn
---

# Doc Raw to Brainstorm

## Mission

Given raw, unstructured context — user requirements (freeform text), API documentation (URLs or pasted), contributor guidelines, reference implementations (file paths), PO feedback (chaotic notes), or any combination thereof — produce a complete three-layer vault structure without requiring any pre-existing zettels:

1. **OoB Gherkin Zettels** — out-of-business patterns generalized with placeholders, reusable across projects.
2. **Derived Gherkin Zettels** — business-specific overrides that link their OoB parent(s) and carry real domain values.
3. **Chunk Notes** — project-scoped work units (PR-sized) embedding derived zettels in Acceptance Criteria, with Goal, Technical Scope, typed Input/Output Contracts, DUSTER table, and Done Checklist.
4. **Clean Brainstorm** — entry-point document embedding all chunks, with overview, pipeline architecture, Mermaid dependency graph, annexes, and post-MVP section.

This skill owns the **creation arc**: raw context in → linked knowledge graph out. It is not a decomposer (`doc-brainstorm-to-zettel`) and not a composer from existing atoms (`doc-zettel-to-brainstorm`). It starts from zero vault state for the project.

**Why this matters:**
Raw context is the real starting point for most feature work: a PO writes chaotic notes, an API exposes endpoints, a contributor guide defines conventions, and a reference implementation demonstrates patterns. This skill extracts all testable behaviors from those surfaces, generalizes them into reusable OoB patterns with dedup, derives business-specific variants, assembles them into PR-shaped chunks with typed contracts, and surfaces the dependency graph — turning ambiguity into an executable planning artifact in one pipeline.

**Cross-project pattern identification** is the primary value of the OoB/derived split. Every behavioral extraction actively searches the vault for existing OoB zettels that cover the same or similar pattern — reusing them as parents for new derived zettels rather than duplicating. When an existing zettel almost-but-not-quite matches, the skill surfaces it as a near-match and offers to extend it. Over time, this builds a shared behavioral pattern corpus where common features (pagination, auth, retry, config validation, etc.) are encoded once and derived many times across projects.

## Usage

- `/doc-raw-to-brainstorm --context {source} --project {project_folder}`
- `/doc-raw-to-brainstorm --context {source} --project {project_folder} --dry-run`
- `/doc-raw-to-brainstorm --context {source} --project {project_folder} --batch-approve`
- `/doc-raw-to-brainstorm --context {source} --project {project_folder} --zettel-zone {zone} --phase "MVP 1 — Core Fetch"`
- `/doc-raw-to-brainstorm --context {source} --project {project_folder} --po-feedback {feedback_path}`
- `/doc-raw-to-brainstorm --context {source} --project {project_folder} --reference-impl {impl_path} --contributing {contrib_path}`

**Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `--context` | Yes | Raw context material. Accepts: inline text, absolute file path, comma-separated list of absolute file paths, or a URL (fetched at runtime). Mixed sources allowed (e.g., a file path + a URL). |
| `--project` | Yes | Absolute path to the target project folder (for chunk notes + brainstorm). Created with user approval if absent. |
| `--zettel-zone` | No | Target zone for new zettels: `global`, `personal`, `workspace`, `otsumi`. Default: `workspace`. |
| `--phase` | No | MVP/phase framing label (e.g., `"MVP 1 — Email Focused"`). Appears as top-level section in brainstorm. |
| `--tags` | No | Additional tags for all generated notes (comma-separated). Merged with inferred project tags. |
| `--dry-run` | No | Produce proposals without writing any files. |
| `--batch-approve` | No | Present all proposals in one batch instead of per-file. |
| `--po-feedback` | No | Absolute path to a PO feedback document. Triggers PO integration pass (Step 10) instead of fresh extraction. |
| `--reference-impl` | No | Absolute path to a reference implementation file or directory. Skill extracts typed contracts and behavioral patterns from code. |
| `--contributing` | No | Absolute path to CONTRIBUTING.md or equivalent contributor guideline document. Extracted conventions feed chunk contracts and Done Checklist items. |

## Hard Rules

### Path + Template Authority

- MUST resolve `zettel_root`, `gherkin_template`, `chunk_template`, and all funnel zettel roots from system context (`## Knowledge Bases`). NEVER hardcode paths.
- MUST read `gherkin_template` (003.007) and `chunk_template` (003.024) before generating any note. Frontmatter keys, casing, and structure come from the template. NEVER guess.
- `--zettel-zone` resolves to: `global` → `funnel_zettels_global`, `personal` → `funnel_zettels_personal`, `workspace` → `funnel_zettels_workspace`, `otsumi` → `zettel_root`.
- **Brainstorm notes** have no dedicated template. They derive frontmatter from `zettel_template` with `Template: Brainstorm` and surface the missing-template gap to the user.
- **Date format**: Substitute `Creation Date` and `Modification Date` with current timestamp in `YYYY/MM/DD HH:mm:ss` format. NEVER ISO 8601.
- **Tags field**: When multiple tags are needed, use YAML list syntax (`tags:\n  - Gherkin\n  - pattern/http-client`). Obsidian and Dataview handle both forms equivalently.
- **Gherkin zettels in any zone**: Valid in all zettel zones. Convention: OoB pattern zettels in `funnel_zettels_global`; derived zettels in project-appropriate zone (typically `workspace`).

### Submodule Awareness

- At parameter resolution time (Step 1), check if `--zettel-zone` or `--project` resolves under a known submodule root (`100-Personal/`, `600-Workspace/`, `4242-Otsumi/`).
- If so, warn the user IMMEDIATELY and require confirmation before proceeding.
- Do NOT defer this disclosure to write time.

### Project Tags

- **Project tags** are determined from `--tags` (if explicitly provided) PLUS inferred from `--context` content (look for consistent domain names, API product names, project identifiers, or folder path).
- Convention: `{domain}/{project-name}` (e.g., `oaev/my-collector`, `infra/monitoring-agent`).
- If ambiguous after inference, ask the user to confirm the project tag set before generating notes.

### Source Fidelity

- MUST NEVER fabricate behavioral specs not present or implied in the source material.
- MUST preserve the semantic intent of every behavioral signal in the source — they may be restructured but not dropped silently.
- If a source section contains no extractable behavioral spec (pure prose, configuration reference), note it in the report as "non-behavioral content" and include it verbatim in the chunk note or brainstorm annexe directly.
- If a URL is provided as context, fetch it at Step 2 and treat the response body as source material. Report fetch failures immediately — do NOT silently skip.

### OoB Generalization Rules

- An OoB zettel uses **generic placeholders** (`<SERVICE_CLASS>`, `<CONFIG_CLASS>`, `<ENDPOINT>`, `<BASE_CLASS>`, `<OUTPUT_MODEL>`, `<AUTH_PROVIDER>`, etc.) to remove project-specific references.
- The test is: "Could another project in a different domain reuse this exact zettel unchanged?" If yes → OoB. If no → stays derived or needs further generalization.
- Patterns that are inherently domain-locked (e.g., OAuth2 against a specific provider, a specific API endpoint schema) are NOT forced into OoB — they become derived zettels directly.
- Tag OoB zettels with `pattern/{category}` (e.g., `pattern/http-client`, `pattern/data-mapping`, `pattern/orchestration`).

### Derived Zettel Rules

- A derived zettel MUST link its OoB parent(s) via `[[parent-zettel]]` in the body under a "Derives from:" line.
- A derived zettel MUST link its OoB parent(s) in frontmatter `Links:`.
- A derived zettel carries the full business-specific gherkin with real field names, real API endpoints, real model names.
- Tag derived zettels with both the pattern tag AND the business/project tag (e.g., `pattern/http-client` + `oaev/my-collector`).

### Chunk Note Rules

- One chunk per logical work unit (PR-sized scope).
- Chunk notes embed derived zettels (not OoB) in the Acceptance Criteria section via `![[derived-zettel]]`.
- Chunk frontmatter `Links:` contains wikilinks to ALL referenced zettels (both OoB and derived).
- **Typed Input/Output Contracts**: MUST be expressed as Python code blocks with modern syntax (`str | None`, `list[X]`, `dict[str, Any]`). No pseudocode.
- **Output Contract annotation**: Every output contract block MUST be followed immediately by a `Consumed by: CHK.N — {purpose}` line naming which downstream chunk consumes the output and why.
- **Chunk note body sections (required)**: Goal, PR Target, Technical Scope (Included / Excluded / Enablers / Blockers), Contracts (Input / Output), DUSTER table (empty for team), Done Checklist.
- If a source field is absent (e.g., DUSTER scores), leave it empty but keep the structure.
- Contributing guideline conventions (if `--contributing` is provided) feed the Done Checklist as verification items.

### Brainstorm Rules

- The clean brainstorm embeds ALL chunk notes via `![[chunk-note]]`.
- Each chunk embed MUST be preceded by a `#### CHK.N — {title}` heading, then the `![[chunk-note]]` embed, then a `---` separator.
- Brainstorm frontmatter `Links:` contains wikilinks to all chunks AND all derived zettels.
- **Diagrams**: MUST use Mermaid fenced blocks. NEVER ASCII art.
  - Pipeline/Architecture diagram: `flowchart LR` or `flowchart TD` showing data flow between components.
  - Dependency graph: `graph TD` with `classDef` color-coding by chunk status (e.g., `classDef foundation fill:#1a1a2e` for foundational chunks, `classDef feature fill:#16213e` for feature chunks, `classDef gate fill:#0f3460` for gate/integration chunks).
- Brainstorm includes: Overview, MVP/Phase framing (if applicable), Pipeline Architecture (Mermaid), Dependency Graph (Mermaid with classDef), External Dependencies, Chunk Embeds (with `#### CHK.N — Title` headings), Post-MVP Follow-ups, Annexes (config reference, operator reference, API tiers/rate limits, risk register, open questions).
- Annexe sections are populated from non-behavioral source content, reference implementation excerpts (if `--reference-impl`), and contributing guideline conventions (if `--contributing`).

### Dedup and Cross-Project Pattern Surfacing

The primary purpose of this flow is to **identify common features, use cases, scenarios, and behaviors across projects**. Dedup is not a defensive check — it is the core knowledge-graph mechanism.

- Before creating **any** zettel (OoB or derived), search `all_zettel_roots` for existing notes by title fuzzy match, tag intersection, and body semantic overlap.
- **OoB dedup**: If an existing OoB zettel covers the same pattern, SKIP creation and use the existing one as the parent for the derived zettel.
- **Near-match detection**: If an existing OoB zettel covers ~70-90% of the extracted behavior (similar structure, partially overlapping scenarios, same pattern category), surface it as a **near-match candidate** with:
  - The existing zettel path and title.
  - A diff showing what the existing zettel covers vs. what the new behavior adds.
  - Options: `extend existing` (propose additions to the existing OoB zettel) / `create new` (genuinely distinct pattern) / `derive from existing as-is` (existing is close enough).
  - If the user chooses `extend existing`, the skill proposes specific amendments to the existing zettel (new scenarios, additional placeholders) as a per-file diff requiring approval. This strengthens the OoB corpus rather than fragmenting it.
- **Derived zettel dedup**: Before creating a derived zettel, search for existing derived zettels with the same project tags, overlapping behavioral content, AND matching OoB parent link. Two derived zettels that share the same OoB parent and have significant title/tag/content overlap are likely duplicates. Present the overlap diff to the user and offer: `reuse existing` / `update existing` / `create new` / `skip`.
- **Cross-project overlap report**: After all dedup passes complete, produce a summary report showing:
  - OoB zettels reused from other projects (indicating shared patterns).
  - Near-matches found (indicating evolving shared patterns).
  - Net-new OoB zettels created (indicating novel patterns unique to this project so far).
  - This report is included in the brainstorm's Annexe section as a "Pattern Reuse Report".
- Present all dedup findings to the user before any write.

### Approval + Safety

- MUST present proposals before writing (per-file or batch).
- MUST NOT `git add`, `git commit`, or `git push`.
- MUST disclose submodule writes if the target path is under a submodule.
- If target filename already exists on disk and was NOT matched by dedup (different content, same name), surface the conflict — NEVER silently overwrite.

### Incremental Operation

- This skill is designed to be invoked multiple times on the same project folder (e.g., once per PO feedback round).
- If `brainstorm.md` already exists in `--project`: offer `append new chunks` / `rebuild from scratch` / `abort`.
- If chunk notes already exist: dedup by title and offer `update existing` / `create new (renumber)` / `skip`.
- If derived zettels already exist for the same OoB parent + project tags: reuse them.
- `--po-feedback` specifically triggers Step 10 (PO Feedback Integration Pass), which targets ONLY the delta — it does not re-process already-covered context.

## Steps

### 1. Resolve vault and templates

1. Resolve target vault from system context (`## Knowledge Bases`).
2. Read `gherkin_template` and `chunk_template` at their absolute paths. Store their frontmatter schema.
3. Resolve `--zettel-zone` to an absolute path.
4. Verify `--project` folder exists. If not, propose creation and require user approval before proceeding.
5. Check if `--project` or `--zettel-zone` is under a submodule root. If so, warn immediately and require confirmation.
6. If `brainstorm.md` or any `CHK.*` files exist in `--project`, report them and ask: `append new chunks` / `rebuild from scratch` / `abort`.

### 2. Ingest and normalize raw context

For each source in `--context` (file paths, inline text, URLs):

1. **File paths**: Read content end-to-end. Detect format: Markdown, plaintext, YAML/JSON (API spec), Python/code.
2. **URLs**: Fetch at runtime. On HTTP failure, report error and ask user: `skip` / `retry` / `provide alternative`. Store fetched body.
3. **Inline text**: Treat as freeform Markdown.
4. **`--reference-impl`** (if provided): Read the implementation file(s). Extract:
   - Public class and method signatures (typed).
   - Docstrings and inline comments that describe behavioral intent.
   - Any existing test fixtures visible in the implementation folder.
5. **`--contributing`** (if provided): Read the document. Extract:
   - Naming conventions, code style rules, commit discipline, PR checklist items.
   - These feed the Done Checklist of every chunk note and the brainstorm's Annexe.
6. Normalize all collected material into a unified **Source Map**: `{source_id, origin_type (file|url|inline|impl|contributing), raw_content, format}`.
7. Present the source map summary to the user for validation before behavioral extraction.

### 3. Extract behavioral signals

From the normalized Source Map:

1. **Scan for behavioral signals**: Look for explicit Gherkin blocks, acceptance criteria bullets, decision tables, state descriptions, endpoint descriptions (request/response), error conditions, edge cases, and rate/quota behaviors.
2. **Classify each signal**:
   - `gherkin` — already in Gherkin format.
   - `ac_bullet` — plain-English acceptance criterion (bullet or numbered).
   - `api_behavior` — endpoint description implying a testable behavior (e.g., "returns 429 when rate limit exceeded").
   - `constraint` — hard rule from contributing guide or PO note (becomes a Done Checklist item, not necessarily a zettel).
   - `non_behavioral` — pure prose, config reference, investigation notes.
3. For each `gherkin`, `ac_bullet`, or `api_behavior` signal:
   - Draft a normalized Gherkin scenario candidate: `Feature`, `Scenario`, `Given/When/Then` structure.
   - Annotate the source ID and source line/section.
4. Build **Behavior Candidate List**: `{candidate_id, signal_type, raw_signal, gherkin_draft, source_id, section_label}`.
5. For `non_behavioral` content: annotate as "annexe candidate" — goes to brainstorm Annexe or chunk Technical Scope verbatim.
6. Present the Behavior Candidate List to the user for review. User may: approve / edit individual scenarios / drop / mark as annexe.

### 4. Classify behaviors → OoB vs Derived

For each approved behavior candidate:

1. **Generalizability test**: Can the scenario be expressed with generic placeholders without losing testable meaning?
   - Yes → mark as OoB candidate. Draft the generalized version with placeholders.
   - No (inherently domain-locked) → mark as Derived-only. Keep full domain values.
2. For OoB candidates: draft both the generalized version AND the business-specific derived version.
3. For Derived-only candidates: draft only the business-specific version. It will be created without an OoB parent.
4. Infer natural chunk groupings from the behavior candidate set: cluster by pipeline stage, feature boundary, or resource type (e.g., config → auth → fetch → transform → match → output).
5. Present the full classification to the user: OoB candidates, Derived-only candidates, and proposed chunk groupings. Require confirmation before proceeding to dedup.

### 5. Dedup and near-match analysis for OoB candidates

For each OoB candidate:

1. Search `all_zettel_roots` by title fuzzy match, `pattern/*` tags, and body semantic overlap (scenario structure comparison).
2. **Exact match** (similarity >= 0.9): present to user → `reuse existing` (skip OoB creation, link existing as parent) / `skip`.
3. **Near-match** (similarity 0.7-0.9): present the existing zettel with a diff showing coverage gap. Options: `extend existing` (propose amendments to existing OoB) / `create new` (genuinely distinct) / `derive from existing as-is` (close enough without modification).
4. **No match** (similarity < 0.7): proceed to creation.
5. If `extend existing` chosen: draft per-file diff for the existing OoB zettel (add new scenarios/placeholders). Require user approval. This is a **zettel update, not a creation**.
6. Record mapping: `{oob_zettel_path (existing or planned), derived_zettel_path (planned), match_type (exact/near/new)}`.
7. After processing all candidates: generate the Cross-Project Pattern Report (see Dedup rules).

### 6. Generate OoB Zettels

For each approved OoB candidate (create new):

1. Build from `gherkin_template` frontmatter.
2. Title: lowercase-kebab descriptive of the pattern (e.g., `http-paginated-fetch-follows-next-link-until-exhausted`).
3. Tags: `pattern/{category}` + any cross-cutting tags. YAML list syntax when multiple.
4. Body: `# Gherkin : {title}` → `## Feature` → gherkin block with placeholders.
5. Filename: `{title}.md` in `funnel_zettels_global` (OoB patterns are global by convention).

### 7. Generate Derived Zettels

For each behavior candidate in the approved set:

1. **Dedup check**: Search `all_zettel_roots` for existing derived zettels by: title fuzzy match (planned derived title), tag intersection (project tags + pattern tag), body semantic overlap, OoB parent link match. Present overlap diff if found. User chooses: `reuse existing` / `update existing` / `create new` / `skip`. Proceed only for `create new`.
2. Build from `gherkin_template` frontmatter.
3. Title: `{project-prefix}-{behavior-description}` (e.g., `my-collector-fetcher-paginates-api-alerts`).
4. Tags: `pattern/{category}` + project tags. YAML list syntax.
5. Links: wikilinks to OoB parent(s) (if any).
6. Body:
   - "Derives from:" line with `[[oob-parent]]` embed(s). Omit if Derived-only (no OoB parent).
   - `## Feature` → full business-specific gherkin with real names, real endpoints, real field values.
   - `## Output Contract` — typed Python code block (modern syntax: `str | None`, `list[X]`) if the behavior implies a data output. Add `Consumed by: CHK.N — {purpose}` line immediately after.
   - Optional: `## Design Notes`, `## Mapping Table`, `## Investigation Notes` — if source material provides design intent or field mapping.
7. Filename: `{title}.md` in the resolved `--zettel-zone`.

### 8. Build Dependency Graph

Before generating chunk notes, analyze the typed Output Contracts across all derived zettels to build a dependency graph:

1. Map `Consumed by: CHK.N` annotations to chunk-to-chunk dependencies.
2. Determine chunk ordering: which chunks must complete before others can begin.
3. Identify foundational chunks (no dependencies), feature chunks (depends on ≥1), and gate/integration chunks (depends on all prior).
4. Generate a Mermaid `graph TD` diagram:
   - Each chunk is a node: `CHK_N[CHK.N — Title]`.
   - Edges show consumption: `CHK_N --> CHK_M`.
   - `classDef` color-coding:
     - `classDef foundation fill:#1a1a2e,color:#e94560,stroke:#e94560`
     - `classDef feature fill:#16213e,color:#0f3460,stroke:#0f3460`
     - `classDef gate fill:#0f3460,color:#e94560,stroke:#e94560`
   - Apply class to each node: `class CHK_N foundation`.
5. Present the dependency graph to the user for validation before generating chunk notes.

### 9. Generate Chunk Notes

For each approved chunk group:

1. Build from `chunk_template` frontmatter.
2. Title: `Chunk : CHK.{N} {group_title}`.
3. Tags: `Chunk` + project tags. YAML list syntax.
4. Links: wikilinks to ALL zettels (OoB + derived) in this chunk.
5. Body sections:
   - **Goal**: one-sentence description of what this chunk delivers.
   - **PR Target**: branch/PR naming convention (from `--contributing` if provided, else placeholder).
   - **Technical Scope**:
     - Included: specific classes, modules, endpoints, transformations in scope.
     - Excluded: explicit out-of-scope items (prevents scope creep).
     - Enablers: external prerequisites the chunk depends on (other chunks, external services).
     - Blockers: known unknowns that must be resolved before this chunk can start.
   - **Contracts**:
     - Input: typed Python code block (`class ChunkNInput`, fields, types). MUST use modern syntax.
     - Output: typed Python code block (`class ChunkNOutput`, fields, types). MUST be followed by `Consumed by: CHK.M — {purpose}` (one line per consumer).
   - **Acceptance Criteria**: `![[derived-zettel]]` embed for each zettel in this chunk's group.
   - **DUSTER table**: empty structure for team to fill (`D`, `U`, `S`, `T`, `E`, `R` columns).
   - **Done Checklist**: derived from behavioral scenarios (each scenario → checklist item) PLUS contributing guideline items (if `--contributing` provided) PLUS any `--reference-impl` verification items.
6. Filename: `CHK.{N}-{kebab-title}.md` in `--project`.

### 10. PO Feedback Integration Pass (when `--po-feedback` is provided)

This step executes INSTEAD of (or after) Steps 2–9 when `--po-feedback` is given:

1. Read the PO feedback document end-to-end.
2. Extract behavioral signals from the feedback (same classification logic as Step 3).
3. **Overlap analysis**: For each extracted signal, check against existing chunk notes and derived zettels in `--project` and `all_zettel_roots`:
   - **Covered**: signal already addressed by an existing zettel or chunk — report as "already covered" with the matching note path.
   - **Partial**: signal extends an existing behavior — propose updating the existing derived zettel and/or chunk note.
   - **New**: signal introduces a net-new behavior — run the full OoB/derived/chunk pipeline (Steps 4–9) for this signal only.
4. For partial/new signals: number new chunks starting from `CHK.{N+1}` where N is the current highest chunk number in `--project`.
5. Update `brainstorm.md` by appending new chunk embeds (with `#### CHK.N — Title` headings) and updating the Mermaid dependency graph to include new nodes and edges.
6. Present the full delta (covered / partial / new) to the user before any write.

### 11. Generate Clean Brainstorm

1. If `brainstorm.md` exists and user chose `append`: read existing file, insert new chunk embeds and update dependency graph in place. Skip to Step 12.
2. If fresh or `rebuild`:
   - **Frontmatter**: derive from `zettel_template` with `Template: Brainstorm`. Tags: `brainstorm` + project tags. Links: all chunks + all derived zettels.
   - **Title**: `Brainstorm : {project_display_name}`.
   - **Phase framing** (if `--phase` provided): insert as the first heading above Overview.
   - **Overview**: synthesize from context + behavior candidate set (3–5 sentences describing what the project does, what problem it solves, what the planned output is).
   - **Pipeline Architecture** (Mermaid `flowchart LR` or `flowchart TD`): show data flow between components inferred from Input/Output contract chain. Label edges with the data type flowing between nodes.
   - **Dependency Graph** (Mermaid `graph TD` with `classDef`): the graph produced in Step 8.
   - **External Dependencies**: external services, APIs, auth providers, or platform requirements that the project depends on but does not own. Sourced from chunk Enablers/Blockers and `--context` material.
   - **Chunk Embeds**: for each chunk in dependency order:
     ```
     #### CHK.N — {title}

     ![[CHK.N-{kebab-title}]]

     ---
     ```
   - **Post-MVP Follow-ups**: behaviors and enhancements identified in context but explicitly deferred. Bullet list with source attribution.
   - **Annexes** (one subsection per concern):
     - Configuration Reference (from contributing guide or reference impl config classes).
     - Operator Reference (CLI flags, environment variables, runtime options).
     - API Tiers and Rate Limits (from API doc context, if present).
     - Risk Register (known risks from Blockers and open questions).
     - Open Questions (unresolved decisions surfaced during extraction).
     - Reference Implementation Excerpts (if `--reference-impl` provided): code blocks with attribution.
3. Filename: `brainstorm.md` in `--project`.

### 12. Approval Gate

- Default: present each file proposal with path + content preview (truncated to first 20 lines). User approves per file.
- `--batch-approve`: present summary table (filename, type, line count) + full content on demand. Single approval for all.
- `--dry-run`: emit the full proposal set as skill output. No file is written.

### 13. Write

For each approved file:
1. Write atomically.
2. Verify YAML frontmatter parses correctly (no unclosed strings, correct date format, valid list syntax).
3. Verify Mermaid fenced blocks are well-formed (no unclosed brackets, valid node IDs, valid classDef syntax).

### 14. Report

Return:

- **Sources ingested**: file paths, URLs fetched, inline sections processed.
- **Behaviors extracted**: total count, OoB count, derived count, domain-locked (no OoB) count.
- **Created files by layer**: OoB zettels, derived zettels, chunk notes, brainstorm.
- **Dedup hits**: reused existing zettels (OoB and derived), with path references.
- **Skipped content**: with reasons (dropped by user / no behavioral signal / dedup-skipped).
- **Non-behavioral content**: what was placed in annexes or chunk scope sections directly.
- **PO feedback delta** (if `--po-feedback`): covered / partial / new signal counts.
- **Submodule write disclosures** (if any).
- Reminder: no git operation was performed.

## Drift Guardrails

- If the raw context is empty or all URLs fail to fetch → REFUSE. Raw context is required. Ask the user to supply at least one non-empty source.
- If the user provides an existing brainstorm document as `--context` → REFUSE. Route to `doc-brainstorm-to-zettel` for decomposition of an existing brainstorm.
- If the user provides existing zettels as the primary input (not context) and wants them composed → REFUSE. Route to `doc-zettel-to-brainstorm`.
- If asked to implement code → REFUSE. Route to `dev-*` skills.
- If asked to run tests → REFUSE. Route to `dev-run-tests`.
- If the user wants a SINGLE resource note embedding zettels without chunk structure or project context → route to `kb-obsidian-assemble`.
- If the extracted context has no behavioral signals at all (pure config reference or prose only) → report and suggest `kb-obsidian-zettelize` for direct zettelization or `kb-obsidian-remember` for raw capture.

## Validation

Before claiming success:

- [ ] All provided context sources were ingested (no silent skips; fetch failures were reported).
- [ ] Every approved behavioral signal has a corresponding zettel (OoB, derived, or both) OR a documented reason for exclusion.
- [ ] Every derived zettel embeds its OoB parent(s) in body AND links them in frontmatter (`Links:`). Derived-only (no OoB parent) zettels are explicitly annotated as domain-locked.
- [ ] Every Output Contract code block is followed by `Consumed by: CHK.N — {purpose}`.
- [ ] Every chunk note embeds its derived zettels in Acceptance Criteria (`![[derived-zettel]]`).
- [ ] Every chunk embed in the brainstorm is preceded by a `#### CHK.N — {title}` heading.
- [ ] All diagrams use Mermaid fenced blocks — no ASCII art.
- [ ] Mermaid dependency graph includes `classDef` color-coding and `class` assignments for all nodes.
- [ ] Typed Python contracts use modern syntax (`str | None`, `list[X]`) — no `Optional`, no `List`, no `Dict`.
- [ ] The brainstorm embeds all chunk notes.
- [ ] Frontmatter follows the template exactly (casing, fields, date format `YYYY/MM/DD HH:mm:ss`).
- [ ] Dedup was performed against `all_zettel_roots` before any zettel creation.
- [ ] Incremental runs (PO feedback pass) did not duplicate existing notes.
- [ ] No git operation was performed.
- [ ] Near-match detection was performed for every OoB candidate (not just exact-match dedup).
- [ ] Cross-Project Pattern Report is included in brainstorm Annexe section.
- [ ] Every reused OoB zettel is attributed with the project(s) that originally created it.
- [ ] Submodule writes (if any) were explicitly disclosed and confirmed.
