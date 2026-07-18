---
name: validate-resources
type: curator
version: "1.4.0"
isolation_scope: workspace_global
layer: meta
recommended_model: haiku
reasoning_pattern: null
description: >
  Audits workspace integrity: shared resources + brand context files.
  Detects orphaned files, broken references, schema violations, stale entries,
  duplicate IDs, index drift, and brand status inconsistencies.
  FR: "validate" "audit ressources" "check KB" "health check" "vérifie la cohérence" "audit workspace" "intégrité".
  EN: "validate" "audit resources" "check KB" "health check" "audit workspace" "integrity check".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: []
  mode: none
  subagent_safe: true
pipeline:
  preconditions: ingest-resource should have run at least once
  postconditions: none · agents can query after validate
disambiguates_against:
  audit-meta-account: "route to audit-meta-account when operator says 'audit' + platform context (Meta Ads), that's a platform-specific audit, not a workspace integrity check"
---

## v2.32 alignment (creative.schema v1.2)

- `meta.validation_status` accepts `oneOf [legacy ref | composite ref]`. Both shapes valid, no blocking on either. String form (legacy `validation-status.json`) and object form (`validation-state.json` with `status` + `confidence` + `confidence_source`) both pass.
- Pas de blocking validation sur la présence de `intent` vs `intent_mix` : les deux acceptables. Idem `craft_mode` vs (`overlay_density` + `brand_mark_present`). Backward compat additif strict.
- Flag MINOR (non-blocking) si un fichier `creative.json` v1.2 schema-version ne porte ni `intent_mix` ni `intent` (gap réel d'encoding). Idem si ni `overlay_density` ni `craft_mode`.

## Tone

Résultats en langage courant. Pas de codes de check, pas de noms de fichiers. "Ta fiche produit est complète" · pas "spec.json passes check 11b." Gaps = opportunités, jamais des erreurs.

# Skill: Validate Resources

Garbage collection + integrity checks for the full workspace.
Covers both `resources/` (shared KB) and `brands/` (context DB + OS).

---

## Checks · Shared Resources (run all)

### 1. Index ↔ Filesystem Sync

- Scan all `.json` files in `resources/{type}/` folders
- Compare against `index.json.resources[]`
- Flag: **orphan files** (on disk, not in index)
- Flag: **ghost entries** (in index, file missing)
- **Auto-fix**: Add orphans with `[UNVALIDATED]` tag. Remove ghosts.

### 2. Schema Validation

- For each resource JSON, validate against `resources/schemas/{type}.schema.json`
- Per-brand entity files map to their schema by filename : `brand.json`→brand, `spec.json`→spec, `offers.json`→offer, `profile.json`→profile, `strategy.json`→strategy, `learnings.json`→learnings, `status.json`→status, **`spectrum.json`→spectrum (Spectre, D#502)**, `sources/voc/**/*.jsonl` records→voc-verbatim (par ligne, post-schema only).
- Flag: **schema violations** (missing required, wrong types, pattern mismatches)
- **Report only**

### 3. ID Uniqueness

- Collect all catalogue entry IDs across all catalogues
- Flag: **duplicate IDs**, **prefix collisions**
- Check `index.json.id_prefixes` matches actual prefixes
- **Report only**

### 4. Broken References

- Read `refs` fields in every resource
- Check every referenced ID/path exists
- Flag: **broken outbound refs**, **missing inbound refs**
- **Auto-fix**: Add missing inbound refs

### 5. Staleness Detection

- Check `meta.updated` on all resources
- Flag: not updated in >90 days as **potentially stale**
- Flag: 0 inbound refs → **possibly obsolete**
- **Report only**

### 6. Ramification Check

- Catalogues with `entries.length > 12` → flag
- SOPs with `steps.length > 20` → flag
- **Report only**

### 7. Stats Integrity

- Recount `stats.by_type` and `stats.total_resources`
- **Auto-fix** if drifted

---

## Checks · Brand Context (per brand)

### 8. Wedge Completeness

- Check existence and non-empty status of wedge docs:
  - `brand.json` · meta.name filled? market.competitors has at least 1 entry?
  - At least 1 `products/{slug}/spec.json` with meta.name filled
  - At least 1 `audiences/{slug}/profile.json` with meta.name filled
- Extended checks (not blocking for wedge, but flagged):
  - `offers.json` exists for at least 1 product? If missing → flag `offers_missing` (degrades acquisition/piloting)
  - `strategy.json` has annual_goals? If empty → flag `strategy_empty` (degrades piloting)
  - `credentials.env` exists? If missing → flag `credentials_missing` (degrades platform access)
- **Update `status.json`**: Set `wedge_complete` true/false (core 3 only). Extended flags in `status.json.flags[]`.

### 9. Entity Completeness

- For each context file, check % of required fields filled vs empty
- Classify: `empty` (0%) | `draft` (<30%) | `partial` (30-80%) | `complete` (>80%)
- `learnings.json`: `empty` if 0 entries, `active` if ≥1 entry (no partial · it's append-only)
- `strategy.json`: `empty` if no goals, `draft` if goals only, `complete` if goals + monthly_targets + current_focus
- **Update `status.json.completeness`**

### 10. Freshness

- Check `meta.updated` or `updated` on every brand file
- Flag files not updated in >90 days
- `learnings.json`: check `entries[-1].date` (latest entry). No entries in >90 days → flag `learnings_stale`
- `strategy.json`: check `monthly_targets[-1].month`. If latest month is >2 months behind current → flag `strategy_stale`
- **Update `status.json.freshness`**

### 11. Cross-Reference Validation

- `profile.pain_points[].ref` → must exist in `spec.problems_solved[].problem_id` (iterate array)
- `profile.benefits[].ref` → must exist in `spec.benefits[].benefit_id` (iterate array)
- `offers.offer_groups[].offers[].product_refs[].slug` → must exist in `brand.products_index[].slug` (v2 schema · offers are NESTED under `offer_groups[]`, each offer has `product_refs[]`; legacy `offers.meta.product_slug` is v1.x only)
- `profile.meta.product_id` (if set) → must match a product slug in `products/`
- **Spectre (D#502/D#503)** · `spectrum.cells[].use_case_ref` → must exist in `spec.use_cases[].use_case_id` · `spectrum.cells[].audience_ref` (if set) → must match a slug under `audiences/` · `spectrum.core_cell_ref` (if set) → must match a `cells[].cell_id` in the same file · `spec.use_cases[].mechanism_refs[]` → must exist in `spec.mechanisms[].mechanism_id` (le pont Mc → U → A vérifiable).
- **Spectre trace angle→carte (D#518)** · `angle.lineage.use_case_ref` (si présent) → must exist in `spec.use_cases[].use_case_id` (et donc, transitivement, tracer à un `mechanism_refs[]` · un angle dont l'usage n'est porté par aucun mécanisme est une projection, pas un angle) · `angle.lineage.spectrum_cell_ref` (si présent) → must match a `cells[].cell_id` dans le `spectrum.json` de la même marque. Intégrité QUAND le ref est présent, jamais forcé (cf garde-fou mécanique correspondant dans `resources/scripts/validate-all.py` · `angle_spectrum_untraced` MED).
- **Spectre integrity post-hoc (D#503, intégrité pas pré-validation)** · `spectrum.cells[]` avec `status: validated` ET `evidence: []` vide → flag **MAJOR : cellule validée sans aucune preuve** (la validation par procuration exige au moins un signal · attrape l'erreur persistante, ne pré-valide pas le raisonnement). Idem `coverage_self: blank` non qualifié et sans `lever` → flag MINOR (zone blanche orpheline).
- **Pont watch-competitors → coverage_market (D#518)** · `spectrum.cells[]` avec `coverage_market != "unknown"` MAIS aucun `evidence[]` de nature `behavioral` taguée `_source: observed|inferred` → flag **MINOR : couverture concurrente affirmée sans signal** (la cellule prétend lire le terrain adverse sans preuve · garde le pont honnête sans pré-valider le matching de cellule). Rappel : `strategic_position` reste `null` tant que `coverage_market == "unknown"`.
- Flag: **broken cross-refs**
- **Report only** (data loss risk)

**Offer counting · always iterate `offer_groups[].offers[]`** (v2 schema). Example:
```python
count = sum(len(g.get("offers", [])) for g in offers_doc.get("offer_groups", []))
```
Never count via flat `offers_doc.get("offers", [])` · that's the legacy v1.x path and returns 0 on v2 files, producing the false "offers missing" flag. If a brand still has a v1.x flat-offers file, the count legitimately is 0 under v2 expectation; flag it as schema-migration-pending, not as missing data.

### 11b. _field_types Consistency

- Every top-level section in JSON must have at least one entry in `_field_types`
- No `_field_types` key should reference a field path that doesn't exist in the file
- Derived fields (`_field_types` = "derived") should not be empty when raw source fields are filled
- Flag: **unmapped fields**, **orphaned type entries**, **empty derived fields**
- **Report only**

### 11b-bis. _extraction Consistency (C1 · sibling de 11b)

- Sur les porteurs canon (brand, spec, offer, profile, pain_points, objections · liste fermée C1) : chaque entrée de la root map `_extraction` valide contre `_shared/extraction-provenance.json` (extraction_method dans l'enum, extraction_confidence 0-1, extracted_at date-time)
- Les clés de `_extraction` = globs ou chemins valides (mêmes règles que `_field_types` : pas de clé orpheline vers un champ inexistant)
- **`extraction_method: "absent"` SANS `lever` = FAIL** (politique d'échec C1 : une brique introuvable porte son levier, jamais inventée)
- **Horloge de fraîcheur (C1.1 · D#518)** · si `reliability_tier` présent → dans l'enum [revealed, behavioral-soft, verbatim, structural, declared] · si `velocity_tier` présent → dans l'enum [static, slow, drift, weekly, live] · sur `spectrum.cells[].evidence[].extracted_at` (si présent) → date-time valide. Ces champs sont optionnels (additif strict), validés seulement quand présents · ils ne déclenchent jamais un FAIL par absence (la fraîcheur est un curseur, pas un gate).
- HR field-types C1 : tout champ de `offer.economics_proxy` et `angle.test_readiness.eligibility.overall` doit être tagué `derived` dans `_field_types` · sinon flag **MAJOR : derived non tagué**
- Sans ce check, `_extraction` existe mais n'est jamais validé (échec silencieux)
- **Report only**

### 12b. Learnings Lifecycle

- Scan `learnings.json.entries[]` dans chaque brand
- Détecter contradictions : si deux entries ont >60% tag overlap + dates différentes + facts sémantiquement opposés → marquer l'ancienne comme `status: "superseded"`, `superseded_by: "{newer_id}"`
- Cross-brand : si mode all-brands, détecter learnings similaires (même platform + >60% tag overlap) dans 2+ brands → ajouter au `promote-backlog.json` (créer le fichier s’il n’existe pas encore)
  - Candidat structure :
    ```json
    {
      "learning_id": "LRN-001",
      "brand_slug": "glowco",
      "fact": "...",
      "tags": [...],
      "genericity": "sector",
      "tag_overlap_pct": 78,
      "matching_brands": ["glowco", "nestra"],
      "suggested_resource_type": "convention",
      "suggested_target": "conventions/meta-ads.json",
      "priority": "high",
      "flagged_date": "2026-04-04"
    }
    ```
- Flag learnings avec `status: "active"` + `date` > 180 jours → flag `[REVIEW]` (potentiellement obsolète)
- **Entrées actives > 200** → ajouter dans `todos.md → ## Flags` :
  ```
  [STORAGE] learnings.json {brand} : {N} entrées actives · recommandé de passer les plus vieilles à status:"archived".
  Tri suggéré : garder toutes les entries < 180 jours + les entries avec tags platform/compliance quel que soit l'âge.
  ```
  Ne jamais archiver automatiquement · décision opérateur uniquement.
- **Auto-fix** : marquer les contradictions. Écrire `promote-backlog.json` (créer le fichier s’il n’existe pas encore).

### 11c. Learnings Index Rebuild

- Lire `brands/{slug}/learnings.json`
- Pour chaque entry avec `status: "active"` → écrire dans `learnings-index.json` :
  ```json
  { "id": "LRN-001", "scope": "platform", "platform": "meta", "type": "workaround", "tags": ["ads", "creation"], "summary": "première phrase du fact tronquée à 80 chars" }
  ```
- Exclure les entries `status: "superseded"` ou `status: "archived"`
- **Auto-fix** : réécrire `learnings-index.json` entier à chaque validate (source of truth = learnings.json)

### 12. Update Todos Flags

- Collect all flags from checks 8-11 and 15-18
- Write to `brands/{slug}/todos.md` → `## Flags` section
- Remove resolved flags (issue no longer present)
- **Auto-maintained**: operator doesn't edit Flags section

### 13b. Skill Typology Enforcement

**CRITICAL:** scan every `.skills/skills/{name}/SKILL.md` frontmatter. **YOU MUST** validate:

- `type:` field present and non-null
- value is exactly one of: `producer | curator | capturer | orchestrator | navigator | builder`

**If missing, null, or invalid** → raise **blocking error**, not warning:
```
[SKILL-TYPE-INVALID] .skills/skills/{name}/SKILL.md → `type:` missing or invalid. Required: one of {producer, curator, capturer, orchestrator, navigator, builder}. See docs/system/patterns.md § Skill Taxonomy for binary tests.
```

**If present but contract suspicious** (e.g. `type: curator` with `recommended_model: opus` without a justification YAML comment next to the overridden field) → warning:
```
[SKILL-TYPE-OVERRIDE-UNJUSTIFIED] .skills/skills/{name}/SKILL.md → overrides default contract without justification. Expected: `# override: <reason>` YAML comment next to the overridden field.
```

**Rationale**: with skill count growing over time, unenforced taxonomy drifts to irrelevance. Blocking validation keeps the typology load-bearing. See `docs/system/patterns.md § Skill Taxonomy § Enforcement`.

### 13c. Skill isolation_scope frontmatter enforcement (v2.37+, runtime v2.42)

**HR · Brand isolation scope enforcement runtime**

Pour chaque `SKILL.md` sous `.skills/skills/{name}/`, parser frontmatter YAML et appliquer algorithme :

```
for skill_md in glob(".skills/skills/*/SKILL.md"):
    fm = parse_yaml_frontmatter(skill_md)
    iso = fm.get("isolation_scope")

    # Step 1 · presence check
    if iso is None:
        iso = "brand_only"  # auto-applied default
        emit(SKILL-ISOLATION-DEFAULT, severity=warning, skill=skill_md.parent.name)
    elif iso not in {"brand_only", "cross_brand_with_gate", "workspace_global"}:
        emit(SKILL-ISOLATION-ENUM-INVALID, severity=major, skill=skill_md.parent.name, value=iso)
        continue

    # Step 2 · workspace_global justification
    if iso == "workspace_global":
        desc = fm.get("description", "") + " " + fm.get("patch_notes", "")
        justified = any(token in desc.lower() for token in [
            "infrastructure", "workspace_global justifié", "cross-brand", "atlas vivant",
            "validates all", "validate tous", "promote", "promotion canon"
        ])
        if not justified:
            emit(SKILL-ISOLATION-UNJUSTIFIED, severity=major, skill=skill_md.parent.name)

    # Step 3 · cross_brand_with_gate gate prose check
    if iso == "cross_brand_with_gate":
        body = read_body_after_frontmatter(skill_md)
        if "AskUserQuestion" not in body or "cross-brand" not in body.lower():
            emit(SKILL-ISOLATION-GATE-MISSING, severity=major, skill=skill_md.parent.name)
```

Error codes :
```
[SKILL-ISOLATION-DEFAULT] .skills/skills/{name}/SKILL.md → `isolation_scope:` absent. Default `brand_only` auto-appliqué. Déclarer explicitement pour silence le warning.

[SKILL-ISOLATION-ENUM-INVALID] .skills/skills/{name}/SKILL.md → `isolation_scope: {value}` invalide. Valeurs autorisées : {brand_only, cross_brand_with_gate, workspace_global}.

[SKILL-ISOLATION-UNJUSTIFIED] .skills/skills/{name}/SKILL.md → `isolation_scope: workspace_global` sans justification. Réservé infrastructure skills. Documenter raison dans description ou patch_notes, ou rétrograder à brand_only.

[SKILL-ISOLATION-GATE-MISSING] .skills/skills/{name}/SKILL.md → `isolation_scope: cross_brand_with_gate` sans AskUserQuestion gate explicit dans Step prose avant cross-brand read.
```

**Rationale** : empêche cross-contamination silencieuse multi-brand (red team finding A7). Critique en context agency multi-clients · NDAs interdisent cross-pollination data. Default `brand_only` est le filet de sécurité par défaut. Full doctrine `docs/system/brand-isolation-doctrine.md`.

---

### 13d. Skill layer frontmatter enforcement (v2.42+)

**HR · Connectivity layer enforcement runtime**

Pour chaque `SKILL.md` sous `.skills/skills/{name}/`, parser frontmatter et appliquer algorithme :

```
for skill_md in glob(".skills/skills/*/SKILL.md"):
    fm = parse_yaml_frontmatter(skill_md)
    layer = fm.get("layer")

    # Step 1 · presence check
    if layer is None:
        emit(SKILL-LAYER-MISSING, severity=major, skill=skill_md.parent.name)
        continue

    # Step 2 · enum check
    if layer not in {1, 2, 3}:
        emit(SKILL-LAYER-ENUM-INVALID, severity=major, skill=skill_md.parent.name, value=layer)
        continue

    # Step 3 · layer coherence check
    body = read_body_after_frontmatter(skill_md)
    perms = fm.get("permissions", {})
    if layer == 1:
        # MCP servers requis → frontmatter ou body mentionne MCP
        if "mcp" not in (str(fm) + body).lower():
            emit(SKILL-LAYER-1-MCP-NOT-FOUND, severity=minor, skill=skill_md.parent.name)
    elif layer == 2:
        # APIs callable requis → mention credentials.env ou env var
        signals = ["credentials.env", "credentials_shared", "fal.ai", "trendtrack", "shopify", "meta api", "graph api", "WebFetch", "scrape"]
        if not any(s in (str(fm) + body).lower() for s in [s.lower() for s in signals]):
            emit(SKILL-LAYER-2-API-NOT-FOUND, severity=minor, skill=skill_md.parent.name)
    elif layer == 3:
        # Shipped infra → no external deps mention requis (best-effort)
        pass  # tolerant · layer 3 default catégorie
```

Error codes :
```
[SKILL-LAYER-MISSING] .skills/skills/{name}/SKILL.md → `layer:` absent. Required enum {1, 2, 3}. Layer 1 = MCP server requis, layer 2 = API callable via credentials, layer 3 = shipped infra (no external deps).

[SKILL-LAYER-ENUM-INVALID] .skills/skills/{name}/SKILL.md → `layer: {value}` invalide. Valeurs autorisées : {1, 2, 3}.

[SKILL-LAYER-1-MCP-NOT-FOUND] .skills/skills/{name}/SKILL.md → `layer: 1` déclaré mais aucune mention MCP server dans frontmatter ou body. Documenter MCP requirement.

[SKILL-LAYER-2-API-NOT-FOUND] .skills/skills/{name}/SKILL.md → `layer: 2` déclaré mais aucune mention API/credentials/scrape dans frontmatter ou body. Documenter source ou rétrograder à layer 3.
```

**Rationale** : trois layers (MCP / API callable / shipped infra) sont déclaratives doctrine `docs/system/connectivity-layering.md` (Patch 4A canon). Sans enforcement frontmatter, operator setup et template ship surface divergent silencieusement. Layer frontmatter rend la cartographie auditable et machine-checkable. Backward compat additif strict · skills v2.41- continuent à passer avec warning auto-default.

Cross-ref · canon `docs/system/connectivity-layering.md`.

---

### 13. CLAUDE.md Size Audit

- Scan all `CLAUDE.md` files: root + all `brands/{slug}/`
- Flag: root CLAUDE.md > 150 lines → `[SPLIT-CANDIDATE]`
- Flag: brand CLAUDE.md > 80 lines → `[SPLIT-CANDIDATE]`
- **Report only** · suggest which sections to extract to docs/system/architecture.md or brand-specific docs
- Recommend target sections for extraction: verbose sections (Tiers, Session Relay, Communication Rules, Rules)

### 14. Update Status Timestamps

- Update `status.json.last_activity` to current ISO timestamp (since validate produces output impact)
- No session-state.md activity log entry needed (validate is read-heavy, not write-heavy on brand content)

### 15. Custom Entities · Filesystem Walk (V1.5)

Extends check 1 to the extension layer.

- Walk every `brands/*/custom/*/` folder. For each entity type directory:
  - Verify presence of `schema.json`. Missing → `MAJOR: custom entity {type} has no schema.json`.
  - Verify presence of `README.md`. Missing → `MINOR: custom entity {type} has no README.md`.
  - Verify the type has an entry in `index.json → extensions[]`. Missing → `MAJOR: custom entity {type} not registered in index`.
- Walk `index.json → extensions[]`. For each registered entry:
  - Verify the referenced folder and schema file exist on disk. Missing → `MAJOR: orphan extension entry {type} in index`.

### 16. Custom Schema Canon Validation (V1.5)

Extends check 2 to custom entity schemas.

- For every `brands/*/custom/*/schema.json`:
  - Verify it declares `_version`, `_schema`, `_field_types`. Missing → `MAJOR: custom schema violates canon`.
  - Validate every instance file in the same folder against this schema. Instance violation → `MAJOR: instance {file} violates schema {type}`.
- For every sidecar `brands/*/*.extensions.json` and `brands/*/{products,audiences}/*/*.extensions.json`:
  - Verify `_extends` field points to a valid core entity name.
  - Verify sidecar does not redefine fields already present in the core schema (append-only discipline). Override → `MAJOR: sidecar redefines core field {name}`.

### 17. Reserved Names Collision (V1.5)

Blocks custom entity names that would collide with core.

- Reserved names (case-insensitive): `brand`, `product`, `offer`, `profile`, `learnings`, `strategy`.
- Scan every `brands/*/custom/{type}/` folder name. Match against reserved list → `CRITICAL: reserved name collision on custom entity {type}`.
- Also scan `index.json → extensions[].type` for the same check.

### 18. Sidecar Coherence (V1.5 · flag only)

Flags potential sidecar semantic divergence with the core entity.

- For every sidecar, list field names that could be semantic neighbors to core fields (heuristic match on substring or lexical similarity · `currency`, `locale`, `timezone`, `unit`, `language`, etc.).
- Output as `INFO: sidecar field {x} may overlap with core field {y}, review manually`.
- This check flags, does not block. Automated resolution of semantic divergence is pending V1.x.

### 19. Frontmatter prerequisites schema validation (v2.37+)

**HR-19** Si SKILL.md frontmatter contient un field `prerequisites:` :

1. Charger `resources/schemas/skill-prerequisites.schema.json`
2. Valider `frontmatter.prerequisites` contre le schema (JSON Draft-07, jsonschema lib)
3. Si validation fail → MAJOR finding, skill REJECTED jusqu'à fix
4. Vérifications additionnelles cross-doc :
   - Chaque entry `prerequisites[i].field` doit être référencée dans le Step 0bis prose du même SKILL.md
   - Si dérive frontmatter ↔ Step 0bis → MAJOR finding (multi-source of truth interdit)

Backward compat : SKILL.md sans field `prerequisites:` passe silently (additif, pas requis). Bloque drift garanti à l'échelle (red team finding A3 v2.36).

### 20. Operator vocabulary jargon lint (v2.37+)

**HR-20** Scan tout SKILL.md prose example operator-facing (`output_format:`, vue ASCII templates, no_orphan_output, AskUserQuestion text, exemples opérateur quotés) pour tokens jargon listés dans `docs/system/operator-vocabulary-translation.md`.

Patterns à flag (regex case-insensitive) sur prose hors backticks code :

- `\batlas\s+(brand|vivant|canon)`
- `\bcanon\s+(copy|tool)`
- `\bvalidations\[\]`
- `\bfiches\b` (sauf si dans backticks code)
- `\bcouches\b` (sauf si dans backticks code)
- `\barchetype\b` (sauf operator-facing context explicit)
- `\bL[123]\s+(fallback|gate|degraded)`
- `\bprerequisites\b` (sauf backticks code)
- `\bconfidence_(chain|propagation)`

Si match dans context operator-facing (no inline code/backticks) → MAJOR finding + suggested replacement from translation table (`docs/system/operator-vocabulary-translation.md § Mapping canonique`).

Empêche jargon leak operator-facing (CRITICAL bug v2.36 red team Friction 5).

Backward compat : skills v2.36 sans translation appliquée continuent à fonctionner mais sont flaggés warning par lint (additif strict).

### 21. Audience cartography hierarchy enforcement (v2.42+)

**HR-21** matérialise les 5 invariants doctrine `docs/system/audience-cartography-doctrine.md` (v2.39) en checks runtime sur chaque `brands/{slug}/audiences/{audience_slug}/profile.json`.

Pour chaque profile.json :

1. **scope_enum_strict** · parse `meta.scope` · MUST be in enum `{broad, segment, micro}` · refuse legacy values `{mother, sub}` (migré v2.42). Match legacy → MAJOR finding "Legacy scope value (mother/sub) detected, migrate to broad/segment/micro per doctrine v2.42".

2. **parent_slug_required** · if scope ∈ `{segment, micro}` · verify `meta.parent_slug` is non-null AND points to existing audience slug under same `brands/{slug}/audiences/` (filesystem walk). If null or unresolved → MAJOR finding "Audience-orpheline: scope={scope} without resolvable parent_slug".

3. **overlap_with_acyclic** · scan `meta.overlap_with[]` array across all audiences of the brand · build directed graph (node = audience_slug, edge = each entry in `overlap_with[]`) · run DFS cycle detection · if cycle present → MAJOR finding "Audience-redondante: cycle in overlap_with: {A} → {B} → ... → {A}".

4. **micro_3_of_3_justification** · if scope=micro · verify frontmatter OR meta declares all three fields per doctrine framework Q2 (3/3 test):
   - `volume_remaining_estimate` (numeric, k actives, minimum 20)
   - `pitch_divergent` (bool, MUST be true)
   - `offer_divergent` (bool, MUST be true)
   If 0/3, 1/3, or 2/3 → MAJOR finding "Audience-fantôme suspect: micro scope without 3/3 justification (volume + pitch_divergent + offer_divergent per Invariant 2 doctrine v2.39)".

5. **entry_door_enum_strict** · parse `meta.entry_door` · MUST be in enum `{pain_driven, goal_driven, identity_driven}` · if null, missing, or unknown value → MAJOR finding "Audience without entry door (Invariant 3 doctrine v2.39 Q1 framework)".

6. **isolation_boundary_brand_const** · verify `meta._isolation_boundary` present AND equals literal `"brand"` (string const) per Invariant 5 isolation discipline v2.37 · if missing → auto-fix (write `"brand"`) + log INFO · if present with different value → MAJOR finding "Isolation boundary violated: expected const 'brand', got {value}".

**Algorithms pseudo-code:**

```python
# Check 21 main loop
for brand_slug in brands_iter():
    audiences = walk(f"brands/{brand_slug}/audiences/*/profile.json")
    audience_index = {a.slug: a for a in audiences}
    overlap_graph = build_directed_graph(audiences)  # node=slug, edge=overlap_with[]

    for audience in audiences:
        meta = audience.get("meta", {})

        # 1. scope enum
        scope = meta.get("scope")
        if scope in {"mother", "sub"}:
            findings.append(major(audience, "Legacy scope value (mother/sub)"))
        elif scope not in {"broad", "segment", "micro"}:
            findings.append(major(audience, f"Invalid scope: {scope}"))

        # 2. parent_slug for segment/micro
        if scope in {"segment", "micro"}:
            parent = meta.get("parent_slug")
            if not parent or parent not in audience_index:
                findings.append(major(audience, "Audience-orpheline: unresolved parent_slug"))

        # 4. micro 3/3 justification
        if scope == "micro":
            score = sum([
                isinstance(meta.get("volume_remaining_estimate"), (int, float)) and meta["volume_remaining_estimate"] >= 20,
                meta.get("pitch_divergent") is True,
                meta.get("offer_divergent") is True,
            ])
            if score < 3:
                findings.append(major(audience, f"Audience-fantôme suspect: micro {score}/3 justification"))

        # 5. entry_door enum
        entry = meta.get("entry_door")
        if entry not in {"pain_driven", "goal_driven", "identity_driven"}:
            findings.append(major(audience, "Audience without entry door (Q1 framework v2.39)"))

        # 6. _isolation_boundary const "brand"
        boundary = meta.get("_isolation_boundary")
        if boundary is None:
            auto_fix(audience, "meta._isolation_boundary", "brand")
        elif boundary != "brand":
            findings.append(major(audience, f"Isolation boundary violated: expected 'brand', got {boundary}"))

    # 3. cycle detection on overlap_with graph
    cycles = detect_cycles_dfs(overlap_graph)
    for cycle in cycles:
        findings.append(major(brand_slug, f"Audience-redondante: cycle {' → '.join(cycle)} → {cycle[0]}"))
```

All findings reference doctrine doc `docs/system/audience-cartography-doctrine.md` Invariants 1-5 with `suggested_fix` pointing to the matching invariant section.

**Audit JSON output enriched** · per-brand object adds:

```json
{
  "audience_cartography": {
    "n_audiences_validated": 7,
    "n_violations_by_invariant": {
      "invariant_1_scope_enum": 0,
      "invariant_2_parent_required": 1,
      "invariant_3_overlap_acyclic": 0,
      "invariant_4_micro_3_of_3": 2,
      "invariant_5_entry_door": 1,
      "invariant_6_isolation_boundary": 0
    },
    "suggested_fixes_count": 4,
    "auto_fixed_count": 1
  }
}
```

Empêche les 3 pièges canon doctrine v2.39 · audience-fantôme (micro sans justification 3/3), audience-redondante (cycle overlap_with), audience-orpheline (segment/micro sans parent résolvable).

---

## Output Format

```
## Validation Report · {date}

### Verdict
{Une ligne. Toujours en premier. En langage opérateur, jamais de jargon technique.}

Prêt. Tu peux bosser sur {brand}.
Utilisable mais incomplet. Il manque {X} avant de lancer {action}.
Pas utilisable tel quel. {raison en une phrase + action immédiate}.

Exemples :
Prêt. Tu peux bosser sur Glowco.
Utilisable mais incomplet. Il manque le problème principal du client avant de lancer une campagne Meta.
Pas utilisable tel quel. Ta fiche marque est vide. Lance setup-brand pour configurer la marque.
```

Tout ce qui suit (Summary, Auto-Fixed, Manual Action Required...) est affiché après le verdict. L'opérateur voit la réponse à "est-ce que je peux bosser ?" en premier, le détail technique en second.

---

```

### Résumé
- Ressources partagées analysées : {N}
- Fichiers brand analysés : {N}
- Problèmes trouvés : {N} ({N} corrigés automatiquement, {N} à faire)
- Niveau 1 complet : {oui/non par brand}

### Auto-Fixed
- [fix] {description}

### Points à corriger manuellement
- [données manquantes] {description opérateur · ex: "un champ n'est pas catalogué dans la fiche produit {produit}"} · {action exacte}
- [référence cassée] {description · ex: "le profil audience référence un problème qui n'existe pas dans la fiche produit"} · vérifier que {ID} est bien présent dans {entité concernée en français}
- [données vieilles] {entité concernée en français · ex: "stratégie Glowco"} pas mise à jour depuis {date} · ingest des mises à jour si disponibles
- [à décomposer] {ressource concernée en français} : {N} entrées, dépasse la limite recommandée · à découper en sous-listes si tu veux améliorer les performances
- [fichier trop long] {fichier concerné en français} : {N} lignes · certaines sections peuvent être externalisées

→ **Règle absolue** : aucun path fichier, aucun code technique (`schema_11b`, `wedge_incomplete`, `_field_types`…). Toujours décrire le problème en termes métier + l'action concrète pour le régler.

### Statut par brand
- {brand}: Niveau 1 {complet/incomplet} | {N} points à corriger

### Learnings Health
- {brand}: {N} active | {N} superseded | {N} archived | {N} candidates for promotion
- Contradictions detected: {list}
- Review needed: {learnings > 180 days}

### Context Level (tier-aware)

Niveau de contexte : {brand}
  Niveau 1 (MVP)    : {complet | X/3 éléments manquants}
  Niveau 2 (Enrichi): {complet | X éléments optionnels à ajouter}
  Niveau 3 (Opérationnel): {complet | disponible quand tu auras des ventes}

Tier 1 checks (= wedge):
- brand.json: meta.name + positioning.value_proposition + tone_of_voice.style filled
- ≥1 spec.json: meta.name + pricing.price + benefits (≥1) + problems_solved (≥1) filled
- ≥1 profile.json: meta.name + demographics (≥1 field) + pain_points (≥1) filled

Tier 2 checks (non-blocking, suggestions):
- benefits[].chain or pain_points[].chain filled on any entity
- brand.market.competitors has ≥1 entry
- ≥1 offers.json exists with ≥1 entry in `offer_groups[].offers[]` (v2 schema · see § 11 counting rule)
- tone_of_voice has banned_words or frequent_words

Tier 3 checks (non-blocking, contextual):
- financials has ≥2 non-null fields
- strategy.json has ≥1 annual_goal
- seasonality has peak_periods

### Next Actions
For each missing element, include the exact phrase the operator should say:
- "{brand}: brand incomplete" → Dis "Ingest ces infos sur {brand}" et ajoute : {liste des champs manquants}
- "{brand}: offers empty" → Dis "Ingest cette offre pour {product}" et décris : prix, type d'offre, dates
- "{brand}: audience missing" → Dis "Ingest ce profil client pour {brand}" et décris : qui ils sont, leurs problèmes, leurs objections
- "{brand}: stale" → Dis "Ingest ces mises à jour pour {brand}" et ajoute les infos récentes
- "broken-ref" → Vérifier que les IDs référencés existent (ex: PROB-01 dans spec.json si profile.json le référence)

Use plain language. No technical jargon. Each action = one sentence starting with "Dis" + the exact words to type.

**Tier framing rule**: Present Tier 2/3 gaps as opportunities ("pour améliorer la qualité"), never as errors. Only Tier 1 gaps are flagged as blocking.
```

Append report to CHANGELOG.md.

**CHANGELOG.md rotation** : après append, compter le nombre d'entrées `## v` dans CHANGELOG.md.
- Si ≤ 50 → rien à faire.
- Si > 50 → déplacer les entrées les plus anciennes (au-delà de 50) dans `CHANGELOG_archive.md` (append en bas, jamais supprimer). Conserver les 50 plus récentes dans CHANGELOG.md. Signaler : "CHANGELOG archivé · {N} entrées déplacées vers CHANGELOG_archive.md."

---

## Post-Validate Usage Guide

After reporting, if `wedge_complete = true` for at least one brand, append a **usage bridge** to the output. This is the single most important UX moment · the user just invested 15-30 min and needs to know what to do next.

### When wedge_complete = true:

```
Contexte prêt. Tes agents peuvent travailler.

Essaie maintenant :
→ "Écris une description produit pour {product_name}"
→ "Génère 5 hooks publicitaires pour {audience_name}"
→ "Rédige un email de lancement pour {brand_name}"
→ "Analyse mes concurrents et propose un angle de différenciation"
→ "Prépare un brief créa pour une campagne Meta"

Tes agents puisent automatiquement dans le contexte que tu viens de configurer.
Pas besoin de re-expliquer ta marque · c'est déjà fait.

Pour enrichir plus tard : "Ingest [nouvelles infos] pour {brand_name}"
Pour vérifier la santé : "Validate {brand_name}"
```

Replace `{product_name}`, `{audience_name}`, `{brand_name}` with actual values from the brand data.

### When wedge_complete = false:

```
Contexte incomplet. Tes agents peuvent travailler, mais la qualité sera limitée.

Ce qui manque :
{list from Next Actions section}

Une fois complété, tes agents pourront :
→ Générer du contenu ciblé (hooks, descriptions, emails)
→ Analyser tes concurrents avec le bon contexte
→ Piloter tes campagnes avec les bons KPIs
```

### Hard rule: ALWAYS display the usage bridge. Never end validation without showing what comes next.

---

## Modes

### Default: Single brand

Operator says "validate {brand}" or "health check {brand}" → run checks 1-14 on that brand + checks 15-18 on its extensions + shared resources.

### All brands mode

Operator says "validate all", "validate everything", "health check global", or "workspace status" → run checks on ALL brands:

1. List all brand slugs: scan `brands/*/brand.json` (skip `_TEMPLATE/`, `_EXAMPLE/`)
2. Run checks 1-7 (shared resources) · once
3. Run checks 8-14 per brand, plus checks 15-18 on each brand's extensions
4. Aggregate results into `workspace-status.json` (root level):

```json
{
  "generated": "2026-04-04T12:00:00Z",
  "template_version": "1.1.0",
  "brands_count": 3,
  "brands": {
    "{slug}": {
      "wedge_complete": true,
      "completeness_summary": "brand:complete, products:2/3 complete, audiences:1/2 partial",
      "flags_count": 2,
      "stale_files": 0
    }
  },
  "shared_resources": {
    "total": 12,
    "orphans": 0,
    "ghosts": 0,
    "schema_violations": 1
  },
  "health": "healthy | degraded | critical"
}
```

**Health rules:**
- `healthy` = all brands wedge_complete + 0 critical flags
- `degraded` = at least 1 brand incomplete OR >0 schema violations
- `critical` = >50% brands incomplete OR broken cross-refs in multiple brands

5. Print summary table in report output:

```
### Workspace Overview
| Brand | Wedge | Flags | Stale |
|-------|-------|-------|-------|
| acme  | ok    | 0     | 0     |
| xyz   | ko    | 3     | 1     |

Health: degraded
```

**workspace-status.json is auto-maintained by validate only.** Same authority rule as brand status.json.

---

## Hard Rules

- **Never delete files** · only flag
- **Auto-fix only safe ops**: index sync, inbound refs, stats, status.json, workspace-status.json, todos flags
- **Schema violations and duplicates** = report only
- **Run ALL checks every time** · no partial validation (mode incrémental = V2)
- **Validate = autorité unique** sur status.json, workspace-status.json, cross-refs, et stats. Aucun autre skill n'écrit dans ces fichiers.
- **Brand status.json is the only file validate writes in brands/** (+ todos.md flags)
- **workspace-status.json is the only cross-brand aggregation file** · lives at workspace root
- **HR-19 frontmatter prerequisites schema validation** · voir check 19. Tout SKILL.md avec un field `prerequisites:` MUST passer la validation contre `resources/schemas/skill-prerequisites.schema.json` ET maintenir la cohérence avec son Step 0bis prose. Frontmatter ↔ Step 0bis drift = MAJOR finding (multi-source of truth interdit, red team v2.36 A3).
- **HR-20 operator vocabulary jargon lint** · voir check 20. Scan SKILL.md prose operator-facing pour tokens jargon (atlas brand/vivant/canon, validations[], fiches, couches, archetype, L1/L2/L3 fallback, etc.). Match hors backticks code → MAJOR finding + suggested replacement via `docs/system/operator-vocabulary-translation.md`. Empêche jargon leak operator (red team v2.36 Friction 5).

### HR-21 · Audience cartography hierarchy validation (v2.42+)

Pour chaque profile.json sous `brands/{slug}/audiences/` ·

1. **meta.scope enum strict** · valeurs autorisées `broad | segment | micro` · refuse legacy `mother | sub` (migré v2.42)
2. **Segment + micro require parent_slug** · si scope ∈ {segment, micro} alors meta.parent_slug doit pointer vers une audience existante
3. **overlap_with non-cyclique** · scanner meta.overlap_with[] · si A → B → A (cycle) détecté → MAJOR finding
4. **Micro require justification 3/3** · si scope=micro, frontmatter doit déclarer `volume_remaining_estimate` + `pitch_divergent: bool` + `offer_divergent: bool` (test 3/3 doctrine framework Q2)
5. **meta.entry_door requis + enum strict** · valeurs `pain_driven | goal_driven | identity_driven` · si absent ou null → MAJOR finding
6. **_isolation_boundary const "brand"** · forcer présence + valeur `brand` sur tous profile.json (isolation discipline v2.37)

Violations → MAJOR finding + suggested fix pointing vers `docs/system/audience-cartography-doctrine.md` Invariants 1-5.

Empêche audience-fantôme / audience-redondante / audience-orpheline (3 pièges canon doctrine v2.39).

---

## v1.8 Validation Rules (2026-04)

Le schéma v1.8 est backward-compatible. Les contraintes additionnelles à vérifier :

**spec.json v1.8 :**
- `specs.composition[]` accepte string OR objet structuré (anyOf). Si objet, `ingredient` requis.
- `specs.posology.recommended_daily_servings` · number si présent
- `specs.contraindications.age_min/max` · integer ≥ 0 si présent
- `nutrition_facts.nutri_score_grade` · enum ["A","B","C","D","E"] ou null
- `nutrition_facts.allergens[]` · enum EU14 + "oats" (nouvelle valeur)
- `dietary_tags[]` · enum étendue (caffeine_free, bio, raw, chicory_based, clean_beauty, cruelty_free en plus)
- `perishability.period_after_opening_months` · number si cosmétique

**offers.json v1.8 :**
- `contents.duration_type` · enum ["calendar","usage_days","servings"] si présent
- `pricing.price_per_unit.unit` · enum-locked à 22 valeurs (gram, kg, ml, l, serving, dose, day, month, piece, meter, m2, load, wash, application, capsule, tablet, sachet, bottle, pack, count, portion, unit)
- `incentives.duration_tiers[].duration_months` · integer > 0
- `incentives.loyalty.tiers[]` · structure libre si présent

**Règle :** Un instance en v1.7 doit aussi valider sous v1.8 (backward compat). Si échec → flagger comme régression.

**Stamping:** read expected `_version` values from `brands/_TEMPLATE` (living source of truth) and verify each file in a fresh instance matches the corresponding entity. Current values (2026-04-23): `brand.json _version=2.2`, `products/{slug}/spec.json _version=1.8`, `products/{slug}/offers.json _version=2.0`, `audiences/{slug}/profile.json _version=1.2`. Never hardcode "1.8" as a universal version · each entity has its own schema line. The field is `_version`, not `_template_version` (legacy terminology drift).
