---
name: sync-notion-atlas
type: orchestrator
version: "2.0.1"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: false
mode: proposed
operator_facing: true
reasoning_pattern: null
description: >
  v2.0.1 (v2.67) · territoire-only alignment doctrine territory-doctrine.md NEW. Phase B push refactor · 10 databases territoire strict (Produits, Specs, Mécanismes, Bénéfices, Personae, Pain Points, Angles, Objections, Frictions usage, Roadmap). Full funnel Meta (creatives = production layer) RETIRÉE du push v2.0.1 · creatives push via NEW skill dédié sync-creatives-to-notion v2.68+ futur (production layer séparée · cards/Kanban Notion pour briefs + créas par angle). Phase A pull (Steps 0-6) preserved unchanged backward compat strict additif (pull peut ingérer 11 collections si présent Notion-side legacy). --mode=diff reste deferred Phase C v2.59+.
  v2.0.0 (v2.66) · Phase B push runtime exec-ready · Steps B1-B7 detailed (canvas + 11 DBs creation + rows population + relations 2-pass + idempotency lookup par phantom_entity_id). Phase A pull (Steps 0-6) preserved unchanged backward compat strict additif. Dual-direction sync operational. --mode=diff reste deferred v2.59+.
  v1.1.0 (v2.58 coverage extend) · friction.{current_workarounds, resolution_state, cross_refs.*} mapping enrichi · roadmap.{mix[], relations} mapping + denormalized view auto-computed. Closes 4 orphans audit v2.57.
  v1.0.0 baseline Phase A pull-only MVP. Synchronise un workspace Notion (canvas
  stride-up avec 11 collections canon · Produits, Specs, Mécanismes, Bénéfices,
  Personae, Pain Points, Angles, Objections, Frictions usage, Roadmap, Full funnel
  Meta) vers les entités canon PhantomOS d'une brand existante. Modes
  --mode=pull {notion_url} (Phase A v2.57), --mode=push {notion_parent_url} (Phase B
  v2.0.1 · scaffold canvas + 10 DBs territoire + populate rows + bind relations · creatives push via NEW skill dédié sync-creatives-to-notion v2.68+ futur · production layer séparée), --mode=scaffold
  (canvas + 10 DBs territoire vides sans populate, Phase B variant). --mode=diff (Phase C deferred v2.59).
  Mutation gate strict (write-to-context.py mode=proposed) côté pull, MCP Notion direct
  côté push, isolation_scope brand_only, stateless idempotent par phantom_entity_id.
  Source of truth canon = PhantomOS, Notion = UI optionnelle mirror.
  FR: "sync notion atlas {brand_slug}" "pull notion vers phantom" "import notion vers {brand_slug}" "synchronise mon notion avec phantom" "tire mon atlas notion dans phantom" "push phantom vers notion" "scaffold notion workspace {brand_slug}" "expose phantom dans notion".
  EN: "sync notion atlas" "pull notion to phantom" "import from notion" "sync workspace from notion" "push phantom to notion" "scaffold notion workspace" "export phantom to notion".
permissions:
  reads: [brand, product, offer, profile, angle, friction, roadmap, creative]
  writes: [product, offer, profile, angle, friction, roadmap, creative]
  mode: proposed
  subagent_safe: false
pipeline:
  preconditions: |
    brands/{slug}/brand.json non-empty · MCP Notion connecté côté Claude Code
    opérateur (verify via claude mcp list) · schemas canon présents
    (brand/spec/offer/profile/angle/friction/roadmap/creative).
  postconditions: |
    validate-resources triggered silently post toutes stages · pending-validations.md
    enrichi · opérateur arbitre accept/reject/correct par collection ou batch.
consumes:
  - brand.schema
  - spec.schema
  - offer.schema
  - profile.schema
  - angle.schema
  - roadmap.schema
  - friction.schema
  - creative.schema
  - docs/system/territory-doctrine.md
produces_proposals_for:
  - brands/{slug}/products/{p}/spec.json
  - brands/{slug}/products/{p}/offers.json
  - brands/{slug}/audiences/{a}/profile.json
  - brands/{slug}/angles/{ANG-NN}.json
  - brands/{slug}/frictions/{FRC-NN}.json
  - brands/{slug}/roadmap.json
  - brands/{slug}/creatives/{CRT-NN}.json
  - brands/{slug}/funnel.json
disambiguates_against:
  snapshot-brand: "route to snapshot-brand quand l'opérateur fournit une URL e-commerce brand (scrape direct PDP / homepage / collection). sync-notion-atlas est UPSTREAM différent · pull depuis workspace Notion structuré opérateur, pas scrape brand publique. Pas la même source, pas la même richesse data."
  import-asset: "route to import-asset pour assets visuels individuels (logo, badges, mascotte) ou par auto_multi sur une brand URL. sync-notion-atlas couvre la data structurée canon des 11 collections, pas les assets binaires."
  ingest-resource: "route to ingest-resource pour docs ponctuels (brief PDF, transcript interview, copy doc, reviews export). sync-notion-atlas couvre le workspace Notion systémique 11 collections inter-reliées, pas l'enrichissement par document isolé."
---

## Tone

Présenter le sync comme un acte d'ingestion structuré, jamais comme un data dump. *"J'ai cartographié ton workspace Notion · 9 collections sur 11 attendues détectées, X rows pulled, Y propositions stagées"*, JAMAIS *"sync-notion-atlas pull executed at 0.73 confidence on 47 rows"*. Le bridge est un mécanisme, pas un héros. L'opérateur voit l'effet (proposals stagées en cours de validation), jamais la plomberie.

---

# Skill: Sync Notion Atlas

Bridge Notion → PhantomOS Phase A pull-only MVP. Synchronise les 11 collections canon stride-up d'un workspace Notion vers les entités canon PhantomOS d'une brand existante via le mutation gate strict (`write-to-context.py --mode=proposed`).

PhantomOS = source of truth canonique. Notion = UI optionnelle mirror. Le bridge est asymétrique par design (cf. `docs/system/notion-bridge-doctrine.md § Le principe canon`).

Phase A (v1.0.0 baseline) `--mode=pull` Steps 0-6 unchanged. Phase B (v2.0.0 NEW v2.66) `--mode=push` + `--mode=scaffold` Steps B1-B7 runtime exec-ready ci-dessous. Phase C `--mode=diff` reste deferred v2.59+.

---

## Step 0 · DRGFP prerequisite check (L1 silent · L2 gate · L3 degraded)

Avant toute opération, run le canon DRGFP `docs/system/dependency-resolution-protocol.md` ·

**L1 silent** (input prerequisites) ·
- `brand_slug` fourni en argument ?
- `notion_workspace_url` fourni en argument ?
- `brands/{brand_slug}/brand.json` existe ET `identity.name` non-empty ?

Si NON sur l'un de ces 3 · refuse to ship · surface en clair · *"Il me manque {ce_qui_manque} pour démarrer. Brand existante requise (lance setup-brand si besoin), URL workspace Notion requise."*. Stop.

**L2 gate** (Layer 1 MCP infrastructure check, cf. `docs/system/connectivity-layering.md`) ·
- MCP Notion connecté côté opérateur ? Verify via `claude mcp list` OR test ping silencieux avec `mcp__claude_ai_Notion__notion-search` (query trivial).
- Si refus / non-réponse / MCP absent · AskUserQuestion explicit ·

```
Le bridge Notion a besoin du serveur MCP Notion configuré côté ton Claude Code.
Je ne le vois pas actif sur ta session.

(a) Setup MCP Notion d'abord · je te guide via connect-mcp-server
(b) Abort · on reprend quand tu auras le MCP en place
(c) Use cached snapshot si dispo · si un sync Notion antérieur a déjà tourné, on lit le snapshot local
```

Pas de fallback silencieux. Le bridge requiert MCP actif.

**Si MCP Notion absent** · AskUserQuestion 2 options ·
- (a) "Je te guide pour connecter Notion maintenant (2 min via connect-mcp-server target=notion)"
- (b) "Je bascule en mode export markdown standalone (j'écris les fichiers JSON, tu push manuellement vers Notion plus tard)"
Default proactif proactif · (a) si l'opérateur a le temps.

**L3 degraded** (schemas canon v2.56+ requis) ·
- Verify presence de `resources/schemas/friction.schema.json` + `resources/schemas/roadmap.schema.json` + `resources/schemas/brief.schema.json`. Ces schemas sont v2.56+ pré-requis pour Phase A.
- Si absents · workspace-template stale détecté · flag explicite à l'opérateur · *"Le template workspace est antérieur à v2.56. Les schemas friction.schema + roadmap.schema sont requis pour le sync Phase A. Mets à jour le workspace via update-workspace avant de relancer."*. Refuse to ship. DRGFP gate strict.

Si Step 0 passe (3 checks L1 silent + L2 MCP actif + L3 schemas présents) · continue.

---

## Step 1 · Notion canvas discovery

**Goal** · cartographier la structure Notion (canvas root + 11 collections candidates) avant tout query massif.

**Sub-step 1.1 · Canvas root fetch** ·

```
mcp__claude_ai_Notion__notion-fetch
  url: {notion_workspace_url}
```

Retrieve canvas root + structure descendante (databases, pages enfants).

**Sub-step 1.2 · Collections matching** ·

```
mcp__claude_ai_Notion__notion-search
  query_filter: {parent canvas root id}
```

Pour chacune des 11 collections canon attendues, match par titre (case-insensitive, fuzzy léger acceptable) ·

| Collection canon attendue | Variantes acceptées (FR + EN) |
|---|---|
| Produits | Produits, Products, Product Catalogue |
| Specs | Specs, Specifications, Caractéristiques |
| Mécanismes | Mécanismes, Mechanisms, Mecaniques |
| Bénéfices | Bénéfices, Benefits, Avantages |
| Personae | Personae, Audiences, Personas, Audience Segments |
| Pain Points | Pain Points, Douleurs, Pains |
| Angles | Angles, Angles produits, Strategic Angles |
| Objections | Objections, Freins |
| Frictions usage | Frictions usage, Frictions, Usage Frictions |
| Roadmap | Roadmap, Roadmap angles/audiences, Planning |
| Full funnel Meta | Full funnel Meta, Funnel Meta, Meta Funnel, Full Funnel |

**Sub-step 1.3 · Surface cartography à l'opérateur** ·

Format opérateur-facing (5 sections investigation-posture, mini-cycle Step 1) ·

> *Observé · canvas Notion `{nom_canvas}` cartographié ({date}, {durée_scan}).*
>
> *{N} collections sur 11 attendues détectées ·*
> *{liste matched · pour chaque · nom Notion détecté ↔ collection canon}*
>
> *Non-détectées ({M}) · {liste unmatched · collections canon manquantes dans Notion}*
>
> *On continue le pull sur les {N} collections détectées, ou tu valides la cartographie d'abord (genre · ajuster un nom Notion pour matcher, ou confirmer que la collection manquante n'existe pas vraiment) ?*

**Sub-step 1.4 · AskUserQuestion si corpus thin** ·

Si `N < 8` (moins de 8 collections sur 11 matched) · AskUserQuestion explicit ·

```
Cartographie Notion thin · {N}/11 collections détectées seulement.
Les non-détectées · {liste}.

Risque · pull partiel, certaines entités PhantomOS resteront vides
(frictions / roadmap / angles selon manquantes).

(a) Continue quand même · pull les {N} détectées, accept que {M} entités PhantomOS restent à null
(b) Pause · tu mets à jour Notion (rename + create) puis on relance
(c) Schema map override · si tes collections ont des noms custom non-canon, donne-moi le mapping manuel
```

Pas de pull silent sur corpus thin. L'opérateur arbitre.

Si `N >= 8` · continue silent vers Step 2 (cartographie suffisante).

---

## Step 2 · Collections query

**Goal** · pour chaque collection matched Step 1, pull les rows.

**Sub-step 2.1 · Per-collection query** ·

Pour chaque collection matched (dict `{collection_name → notion_db_id}`) ·

```
mcp__claude_ai_Notion__notion-query-database-view
  database_id: {notion_db_id}
```

Stocker en mémoire dict ·

```
collections_data = {
  "Produits": [row1, row2, ...],
  "Personae": [row1, row2, ...],
  ...
}
```

**Sub-step 2.2 · Cap corpus large** ·

Cap 200 rows par collection pour Phase A MVP. Si une collection retourne > 200 rows ·

> *La collection {nom} a {X} rows. Je cap à 200 pour ce sync v1.0.0 (Phase A MVP). Tu veux que je pull les 200 premières ({ordre Notion natif), ou tu préfères filtrer (par date, par status, autre) ?*

L'opérateur arbitre. Cap respecté.

**Sub-step 2.3 · No-op si collection vide** ·

Si une collection matched retourne 0 rows · note `{collection_name: []}` silent, continue. Pas de stage de proposal vide. L'opérateur le verra dans la synthèse Step 6.

---

## Step 3 · Mapping Notion vers PhantomOS canon

**Goal** · pour chaque row Notion pullée, appliquer le mapping canon documenté dans `docs/system/notion-bridge-doctrine.md § Mappings cross-platform`.

### Table de mapping résumée (canon)

| Collection Notion | Schema PhantomOS | Storage Path |
|---|---|---|
| Produits | `spec` + `offer` | `brands/{slug}/products/{p}/spec.json` + `offers.json` |
| Specs | `spec.composition` + `spec.specs.*` | subfields spec.json (group by product cross-ref) |
| Mécanismes | `spec.mechanisms[]` | subfield spec.json |
| Bénéfices | `spec.benefits[]` (emotional_signal + latency v2.56) | subfield spec.json |
| Personae | `profile` (audience-level entity) | `brands/{slug}/audiences/{a}/profile.json` |
| Pain Points | `profile.pain_benefit_chain[]` + `pain_category` v2.56 | subfield profile.json |
| Angles produits | `angle` | `brands/{slug}/angles/{ANG-NN}.json` |
| Objections | `profile.objections[]` enrichi v2.56 + xref `angle.tension` | subfields profile.json + angle.json |
| Frictions usage | `friction` NEW v2.56 (v1.1.0 · enrichi `current_workarounds`, `resolution_state`, `cross_refs.{objection_ids, pain_point_ids}`) | `brands/{slug}/frictions/{FRC-NN}.json` |
| Roadmap | `roadmap` NEW v2.56 (v1.1.0 · enrichi `mix[]`, `relations.{angle_ids, audience_slugs, product_slugs, creative_ids}` denormalized view) | `brands/{slug}/roadmap.json` (singleton) |
| Full funnel Meta | `creative` + `funnel` | `brands/{slug}/creatives/{CRT-NN}.json` + `funnel.json` |

Full doctrine canon + cohérence cross-collections (relations Notion devenant cross_refs PhantomOS) · `docs/system/notion-bridge-doctrine.md`.

### Mappings enrichis v1.1.0 (Phase A coverage extend)

#### Frictions usage · enrichments v1.1.0

Quand collection Notion `Frictions usage` est query, mapper additionnellement vers ·

| Notion property | PhantomOS field | Type |
|---|---|---|
| `Workarounds` ou `Solutions actuelles client` (multi-text) | `friction.current_workarounds[]` | array text |
| `Statut résolution` (select) | `friction.resolution_state` | enum [unresolved · in_progress · resolved · accepted] |
| `Cross-ref objections` (relation → Objections, multi) | `friction.cross_refs.objection_ids[]` | array (OBJ-NN canonical IDs) |
| `Cross-ref pain points` (relation → Pain Points, multi) | `friction.cross_refs.pain_point_ids[]` | array (PNT-NN canonical IDs v1.7 NEW) |

Stage chaque field via write-to-context.py mode=proposed (cf. Step 4 patterns). Pour `cross_refs.*`, résoudre les relations Notion vers PhantomOS IDs canonical (OBJ-NN + PNT-NN) avant stage.

#### Roadmap · enrichments v1.1.0

Quand collection Notion `Roadmap [angles/audiences]` porte property `Mix axis` (select · audience · angle · product · funnel · creative) + property `Weight` (number 0-1), mapper vers `roadmap.mix[]` array.

Post-mapping rows roadmap, computer aggregat denormalized auto-computed · collecter tous les `phase.priorities[].angle_ids` + tous les `production_status[].entity_id` → group by entity_type → populate `roadmap.relations.{angle_ids, audience_slugs, product_slugs, creative_ids}`. Vue denormalized auto-générée post Step 4, pas operator-fournie.

### Tags universels mapping (épistemic)

Les 3 tags universels stride-up Notion mappent sur l'encodage épistemic PhantomOS (cf. `docs/system/schema-encoding-doctrine.md`) ·

| Notion (select/text property) | PhantomOS field |
|---|---|
| `source` = `observed` | `_field_types: "observed"` per-field concerné |
| `source` = `inferred` | `_field_types: "derived"` per-field |
| `source` = `declared` | `_field_types: "stated"` per-field |
| `source` empty / null | `_field_types: "stated"` (default défensif) |
| `confidence` qualitatif `forte` | `meta.confidence: 0.9` (numeric, jamais surface opérateur) |
| `confidence` qualitatif `moyenne` | `meta.confidence: 0.7` |
| `confidence` qualitatif `faible` | `meta.confidence: 0.5` |
| `confidence` qualitatif `TRÈS faible` | `meta.confidence: 0.3` |
| `confidence` empty / null | `meta.confidence: 0.7` (default défensif pull Notion, à valider) |
| `validation_status` = `hypothesis` | `meta.validation_status: "hypothesis"` (via `_shared/validation-status.json` enum) |
| `validation_status` = `tested` | `meta.validation_status: "tested"` |
| `validation_status` = `validated` | `meta.validation_status: "validated"` |
| `validation_status` = `scaled` | `meta.validation_status: "scaled"` |
| `validation_status` = `fatigued` | `meta.validation_status: "fatigued"` |
| `validation_status` empty / null | `meta.validation_status: "hypothesis"` (default défensif) |

### Per-row mapping execution

Pour chaque row d'une collection ·

1. Lire row Notion → extract properties (title, fields custom, relations).
2. Map vers le schema PhantomOS cible (table ci-dessus).
3. Build l'objet JSON cible respectant le schema canon (validate-resources friendly).
4. Si row Notion a un champ vide (property null / empty) → laisser le champ PhantomOS vide / null. **JAMAIS** inférer pour combler. Notion = source of truth en mode pull. Hard rule absolue.
5. Compute confidence + _field_types selon tags universels (table ci-dessus).
6. Capture lineage · ajouter `_source: "sync-notion-atlas"` + `_notion_row_id: "{notion_row_id}"` + `_synced_at: "{ISO timestamp}"` pour traçabilité.

### Edge cases canonisés (cf. notion-bridge-doctrine.md § Edge cases)

- **Property type mismatch** (Notion `select` vs schema attend `multi_select`) · flag explicitement Section 4 synthesis, ne mute pas silencieusement. Opérateur arbitre.
- **Row Notion avec field schema-extension custom** (field qui n'existe pas dans canon PhantomOS) · flag, propose `scaffold-extension` post-sync. Pas d'invention.
- **Notion workspace structure non-canonique** (collection avec nom custom) · check si `~/notion-mappings/{brand_slug}.json` override existe (v2.60+ deferred). Sinon fallback détection heuristique Step 1. Si toujours non-matched · AskUserQuestion mapping manuel.

---

## Step 4 · Stage proposals via mutation gate

**Goal** · pour chaque entité PhantomOS construite Step 3, stage la mutation via le mutation gate canonique `write-to-context.py --mode=proposed`.

**Anti-pattern absolu** · JAMAIS hand-edit JSON sous `brands/{brand_slug}/`. JAMAIS bypass write-to-context. JAMAIS d'`Edit/Write/NotebookEdit` sur les `.json` brand-side (refusé runtime par mutation-guard PreToolUse hook). Toute mutation via write-to-context (`docs/system/schema-encoding-doctrine.md § Mutation rule`).

### Stage execution pattern

Pour chaque entité buildée Step 3 ·

**Pattern A · Scaffold file (si entité brand-new, fichier inexistant)** ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/{entity_path}#" \
  --value '{full canonical JSON respecting schema, with null placeholders for missing fields}' \
  --source agent \
  --confidence 0.7 \
  --mode direct
```

Mode `direct` requis pour scaffold initial (le mode `proposed` est rejected sur les writes-whole-file car corrompt les consumers ; cf. snapshot-brand Hard Rules § Write modes). Le scaffold pose la structure complète avec null placeholders.

**Pattern B · Stamp inferred fields (post-scaffold)** ·

Pour chaque field dont la valeur provient d'un row Notion ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/{entity_path}#/{field_pointer}" \
  --value '{scalar or dict value}' \
  --source import \
  --confidence {0.9 | 0.7 | 0.5 | 0.3 selon Notion confidence qualitatif} \
  --mode proposed
```

Mode `proposed` stamp les `_proposed: true` + `_source: "import"` + `_confidence: N` au niveau du field, permet à l'opérateur d'accept/reject par mutation via `pending-validations.md` workflow.

`--source import` valeur enum (cf. write-to-context.py `VALID_SOURCES`), réservée aux ingestions externes structurées comme Notion.

### Pattern C · Stage enrichments v1.1.0 (Phase A coverage extend)

**C.1 · friction.current_workarounds[] + resolution_state** ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/current_workarounds" \
  --value '["{workaround_1}","{workaround_2}"]' \
  --source import \
  --confidence 0.8 \
  --mode proposed

python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/resolution_state" \
  --value '"unresolved"' \
  --source import \
  --confidence 0.8 \
  --mode proposed
```

**C.2 · friction.cross_refs.{objection_ids, pain_point_ids} cross-DB resolution** ·

Quand collection Notion porte cross-relations (e.g. friction page mentionne objections OR pain_points via relation Notion), résoudre vers PhantomOS IDs canonical (OBJ-NN + PNT-NN v1.7 NEW). Stage ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/cross_refs/objection_ids" \
  --value '["OBJ-01","OBJ-03"]' \
  --source agent \
  --confidence 0.8 \
  --mode proposed

python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/frictions/{FRC-NN}.json#/cross_refs/pain_point_ids" \
  --value '["PNT-02","PNT-05"]' \
  --source agent \
  --confidence 0.8 \
  --mode proposed
```

**C.3 · roadmap.mix[] mapping (axis + weight)** ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/roadmap.json#/mix" \
  --value '[{"mix_id":"MIX-01","weight":0.4,"axis":"audience","target_id":"...","rationale":"..."}]' \
  --source agent \
  --confidence 0.8 \
  --mode proposed
```

**C.4 · roadmap.relations denormalized view auto-computed** ·

Post-mapping rows roadmap (Step 3 + Step 4 Patterns A-B-C.3 staged), computer aggregat denormalized · collecter tous les `phase.priorities[].angle_ids` + tous les `production_status[].entity_id` → group by entity_type → populate `roadmap.relations`. Stage ·

```bash
python3 .skills/write-to-context.py \
  --path "brands/{brand_slug}/roadmap.json#/relations" \
  --value '{"angle_ids":["ANG-01","ANG-03"],"audience_slugs":["..."],"product_slugs":["..."],"creative_ids":["CRT-12"]}' \
  --source agent \
  --confidence 0.9 \
  --mode proposed \
  --reason "Denormalized view auto-computed"
```

Vue denormalized auto-générée, pas operator-fournie. Permet drill-down rapide cross-entités sans re-parser phase.priorities[] runtime.

### Delegation à encode-batch (Haiku) pour batches > 5 mutations

Pour les collections volumineuses (typiquement Personae 5-20 rows × 10 fields = 50-200 mutations, ou Angles 10-30 rows × 5 fields), la délégation à `encode-batch` est canonique (cf. ingest-resource SKILL.md pattern) ·

```
Task tool invocation ·
- subagent_type: shared
- skill: encode-batch
- model: haiku
- prompt: |
    {
      "brand_slug": "{brand_slug}",
      "target_entities": [
        {"file_path": "brands/{brand_slug}/audiences/{a}/profile.json", "schema": "resources/schemas/profile.schema.json"},
        ... une entrée par audience à scaffolder ...
      ],
      "observations": [
        {"semantic_kind": "audience_name", "raw_value": "{notion_row.title}", "evidence": "notion row {row_id} title", "source": "import", "confidence_signal": "literal"},
        ... une observation par row Notion par field non-null ...
      ],
      "default_mode": "proposed"
    }
```

Le sub-agent Haiku map chaque `semantic_kind` → `field_path`, run `write-to-context.py` par mutation, rebuild snapshot, run `finalize-mutation-batch.py`. Retourne summary structuré (`mutations_count`, `files_touched`, `unmapped`, `finalize_exit_code`).

Pour batches ≤ 5 mutations (typiquement Roadmap singleton), inline `write-to-context.py` direct acceptable.

### Stage all or none discipline (partial)

Si une mutation individuelle échoue (validate fail intermédiaire, refus sécurité write-to-context, schema mismatch détecté in-flight) · log l'erreur, flag dans Section 4 synthesis, **continue le batch** sur les autres mutations. Pas de rollback automatique des mutations déjà stagées (anti-pattern destructive · l'opérateur arbitre via pending-validations.md ce qu'il retient).

---

## Step 5 · Trigger validate-resources silently

Post toutes les stages Step 4 · invoke `validate-resources` skill (haiku subagent_safe true) pour integrity check structural cross-brand.

```
Task tool invocation ·
- subagent_type: shared
- skill: validate-resources
- model: haiku
- prompt: "Run validate-resources on brand={brand_slug}. Silent unless MAJOR/CRITICAL findings."
```

Si MAJOR / CRITICAL errors remontés · flag explicitement dans Section 3 (Inconnu) ou Section 4 (Leviers) synthesis · l'opérateur sait que certaines entités stagées ont des problèmes structurels à traiter avant accept.

Si zero finding ou seulement MINOR · continue silent vers Step 6 (la synthèse Step 6 mentionnera la validation passée OK).

---

## Step 6 · Synthesis 5-section investigation-posture operator-facing

Output final canonique respectant `docs/system/investigation-posture.md` (5 sections explicites, jamais fusionnées en prose).

### Section 1 · Observé (faits sourcés)

Format structuré, faits avec ancrage source. Pas de prose narrative.

Exemple cible ·

> *Observé · pull Notion `{nom_canvas}` ({date}, {durée_total_sync})*
>
> *{N_collections} collections cartographiées sur 11 attendues ·*
> *  • Produits · {X1} rows pulled → {Y1} spec.json + {Z1} offers.json stagés*
> *  • Personae · {X2} rows pulled → {Y2} profile.json stagés (audiences)*
> *  • Pain Points · {X3} rows pulled → {Y3} pain_benefit_chain entries stagés (subfield profile.json)*
> *  • Angles · {X4} rows pulled → {Y4} angle.json stagés (ANG-NN)*
> *  • Objections · {X5} rows pulled → {Y5} objections entries stagés (subfield profile.json + xref angle.tension)*
> *  • Frictions usage · {X6} rows pulled → {Y6} friction.json stagés (FRC-NN)*
> *  • Roadmap · {X7} rows pulled → 1 roadmap.json singleton stagé (RDM-{brand_slug})*
> *  • Full funnel Meta · {X8} rows pulled → {Y8} creative.json stagés (CRT-NN) + funnel.json maj*
> *  • Specs · {X9} rows pulled → fields {Y9} composition + specs subfields stagés cross-product*
> *  • Mécanismes · {X10} rows pulled → fields mechanisms[] stagés cross-product*
> *  • Bénéfices · {X11} rows pulled → fields benefits[] stagés cross-product*
>
> *Total · {N_proposals} mutations stagées via le mutation gate (write-to-context mode=proposed) sous brands/{brand_slug}/*
>
> *Tags universels Notion détectés cross-rows ·*
> *  • Tag `source` renseigné sur {pct_source}% des rows*
> *  • Tag `confidence` renseigné sur {pct_confidence}% des rows*
> *  • Tag `validation_status` renseigné sur {pct_status}% des rows*
>
> *Pas observé directement (ne pas affirmer) · contenu réel des reviews clients sourçant les pain points encodés Notion · qualité du verbatim {sourced/inferred/declared} par row · perfs paid des creatives Full funnel Meta encodés Notion · réalité terrain des frictions usage vs hypothèses ops.*

### Section 2 · Déduit (hypothèses avec confidence chain)

Hypothèses sur la qualité du corpus Notion pullé. JAMAIS affirmation. Confidence chain qualitatif (`forte / moyenne / faible / TRÈS faible`).

Exemple cible (adapter selon corpus réel) ·

> *Déduit · {N} hypothèses qualité corpus Notion*
>
> *H1 · Qualité épistemic du corpus Notion*
> *  Confidence · {forte si pct_tags > 70%, moyenne si 40-70%, faible si < 40%}*
> *  Indicateurs · tags universels renseignés sur {pct_global}% rows cross-collections · {N_rows_observed} rows tag source=observed (sourced verbatim), {N_rows_inferred} inferred, {N_rows_declared} declared*
> *  À valider · Tu confirmes que le tagging Notion reflète la réalité (sourced = vraiment verbatim Trustpilot/reviews, pas posé par défaut) ?*
>
> *H2 · Audiences encodées Notion = data-driven vs hypothèses*
> *  Confidence · {selon pct audiences avec validation_status >= "tested"}*
> *  Indicateurs · {N_audiences_tested} audiences sur {N_total} avec validation_status >= tested · {N_audiences_hypothesis} encore en hypothesis*
> *  À valider · Les audiences en hypothesis ont-elles déjà du verbatim mining client réel derrière, ou ce sont des cartographies ops sans data terrain ?*
>
> *H3 · Cohérence cross-collections relations Notion ↔ cross_refs PhantomOS*
> *  Confidence · {selon validate-resources output}*
> *  Indicateurs · {N_cross_refs_resolved} relations Notion mappées sur cross_refs PhantomOS, {N_cross_refs_unresolved} non-résolues (target id absent ou mal nommé)*
> *  À valider · {liste cross_refs unresolved si applicable}*
>
> *(... adapter selon corpus pullé · skipper H2/H3 si data non significative ...)*

### Section 3 · Inconnu (variables non observables)

Liste explicite des variables que le sync Notion ne peut pas lever.

Exemple cible ·

> *Inconnu · {N} variables à creuser*
>
> *1. Collections non-matched ({M}/11) · {liste collections canon manquantes dans Notion} → soit pas peuplées Notion-side (l'opérateur arbitre s'il les crée), soit nom Notion non-canon (schema map override)*
> *2. Qualité verbatim sourcing pain points encodés · sans audit des sources Notion (Trustpilot exports, reviews capture, interview transcripts), impossible de savoir si `source: observed` Notion = vrai verbatim ou tag posé par défaut → audit via mine-voc cross-référence*
> *3. Audiences réelles paid Meta vs cartographiées Notion → audit via audit-meta-account si compte Meta dispo*
> *4. Frictions réelles client vs hypothèses ops encodées Frictions usage → cross-référence support tickets + reviews verbatim*
> *5. Viability roadmap (capacité atelier, capacité paid, calendrier réel) → operator capture*
> *6. {liste validate-resources MAJOR/CRITICAL findings si applicable}*

### Section 4 · Leviers (options drill-down · opérateur arbitre)

Pour chaque inconnue importante, quel skill / action permet de la lever.

Exemple cible ·

> *Leviers · {N} axes d'investigation prioritaires*
>
> *Axe A · Validation workflow pending-validations (lève Inconnu 6 + cohérence générale)*
> *  → Workflow opérateur classique · review batch des {N_proposals} mutations stagées via pending-validations.md, accept/reject/correct par collection ou batch (10-15 min par collection si tu reviews finement, 5 min si tu accept tout en bulk)*
> *  → Si certaines mutations ont validate-resources MAJOR flag, traiter d'abord ces ones (corriger Notion + re-pull, ou correct PhantomOS-side via stage-proposal correction)*
>
> *Axe B · Upgrade confidence corpus Notion thin (lève H1)*
> *  → Si tags universels Notion peu renseignés (<40%), recommander mining client réel pour upgrade · écoute Trustpilot + reviews onsite + threads sectoriels (~30 min) puis re-tag Notion-side avant re-sync*
> *  → Audit compte paid Meta si dispo, cross-référence audiences réelles vs hypothèses Notion*
>
> *Axe C · Re-sync si Notion mis à jour (lève {variables temporelles})*
> *  → Sync stateless idempotent · re-run `/sync-notion-atlas {brand_slug} --mode=pull {notion_url}` à tout moment quand Notion update. Les mutations re-stagées remplacent les pending non-accept.*
>
> *Axe D · Phase B push (PhantomOS → Notion) post-MVP*
> *  → Disponible v2.58 prévue · expose state PhantomOS encodé en UI Notion navigable pour client review ou collab agency. Pas v1.0.0 actuel.*

### Section 5 · Close ouvert (UNE question macro)

UNE question macro priorité drill-down. Reco macro explicite. JAMAIS menu plat.

Exemple cible ·

> *On a {N_proposals} mutations stagées sous brands/{brand_slug}/, prêtes à valider. Pour la suite, tu préfères ·*
>
> *A · Accept all en batch maintenant ({~5 min} bulk validation via pending-validations.md, puis tu reviens si correction nécessaire post-coup)*
> *B · Review par collection ({~10-15 min par collection × {N_collections}} pour audit fin avant accept)*
> *C · Drill-down sur une collection problématique d'abord (genre · {nom collection avec validate-resources MAJOR si applicable}, ~10 min)*
>
> *Mon avis · {recommandation macro contextualisée}. Si le tagging Notion est solide (Section 1 montre pct_tags > 60%), A en bulk économise du temps. Si la cartographie est récente / pas validée terrain, B par collection donne le contrôle. Si validate-resources a flagué du MAJOR, C en priorité sur la collection concernée.*

L'opérateur dit `A` / `B` / `C` ou autre, l'agent enchaîne le drill-down sur l'axe choisi (cycle itératif respect 5 sections).

### Hard rules cross-section synthèse (cf. investigation-posture.md)

- **5 sections explicites, jamais fusionnées en prose continue.** Anti-pattern AP-6 doctrine.
- **JAMAIS exposer confidence numeric à l'opérateur.** Confidence chain qualitatif uniquement (`forte / moyenne / faible / TRÈS faible`).
- **JAMAIS nommer le skill interne en surface opérateur** (`mine-voc`, `audit-meta-account`, `pending-validations.md` interne = OK si présenté comme workflow, pas comme path technique).
- **JAMAIS clôturer avec affirmation** (*"Voilà, sync terminé. Autre chose ?"*) · close ouvert toujours UNE question macro drill-down.
- **JAMAIS inventer data Notion pour combler les vides.** Si la collection Frictions est vide Notion-side, la Section 1 dit *"Frictions · 0 rows, pas peuplé Notion-side"*. JAMAIS générer des frictions de placeholder.

---

## Workflow opérateur

### Invocation Phase A (v1.0.0)

```
/sync-notion-atlas {brand_slug} --mode=pull {notion_workspace_url}
```

Exemple ·

```
/sync-notion-atlas stepprs --mode=pull https://notion.so/workspace/abc123def456
```

### Modes deferred (v2.0.0 status)

Si l'opérateur invoque `--mode=diff` v2.0.0 ·

> *Sync-notion-atlas v2.0.0 = dual-direction sync shipped v2.66. Modes `--mode=pull` (Phase A) et `--mode=push` / `--mode=scaffold` (Phase B) opérationnels. Mode `--mode=diff` (compare sans muter, audit pré-sync) reste deferred Phase C v2.59+.*
>
> *Pour pull · `/sync-notion-atlas {brand_slug} --mode=pull {notion_url}`*
> *Pour push · `/sync-notion-atlas {brand_slug} --mode=push {notion_parent_url}`*
> *Pour scaffold blank · `/sync-notion-atlas {brand_slug} --mode=scaffold {notion_parent_url}`*

Pas de fallback silencieux. Refuse cleanly avec roadmap d'évolution.

---

## Phase B runtime v2.0.1 (v2.67) · push PhantomOS → Notion territoire-only exec-ready

> **Status** · v2.0.1 territoire-only refactor v2.67 · 7 steps B1-B7 runtime-executable. Le skill génère le système Notion canon (canvas wrapper + 10 DBs territoire + rows + relations + tags universels) miroir stride-up Onday template, from blank OR from populated PhantomOS state, sur n'importe quel parent Notion. Idempotent par `phantom_entity_id`. Phase B = `--mode=push` from PhantomOS state populé (territoire only), OR `--mode=scaffold` from blank brand (10 DBs territoire vides, skip Step B3).
>
> **Production layer split (doctrine `territory-doctrine.md`)** · Full funnel Meta (creatives) = production layer, NOT pushed par sync-notion-atlas v2.0.1+. Push creatives via NEW skill dédié `sync-creatives-to-notion` v2.68+ futur (cards/Kanban Notion pour briefs + créas par angle). Pattern canon · 1 skill par layer. Évite mixed orchestrator anti-pattern.

### Invocation Phase B

```
/sync-notion-atlas {brand_slug} --mode=push {notion_parent_url}
/sync-notion-atlas {brand_slug} --mode=scaffold {notion_parent_url}
```

- `push` · brand `brands/{brand_slug}/` existe avec state populé → exec Steps B1 + B2 + B4 + B3 + B5 + B6 + B7 (DBs + rows + relations + idempotency).
- `scaffold` · brand vierge OR pre-onboarding → exec Steps B1 + B2 + B5a (relations DB-side) + B7 uniquement, skip Step B3 (no rows populate). Refuse `--mode=scaffold` si brand a state populé (anti-pattern, propose `--mode=push` à la place).

### Working memory dict (cross-steps)

L'agent maintient en working memory tout au long de Phase B ·

```
{
  "canvas_root_id": "<notion_page_id from Step B1>",
  "data_client_page_id": "<notion_page_id from Step B1>",
  "db_ids": {
    "Produits": "<db_id>", "Specs": "<db_id>", "Mécanismes": "<db_id>",
    "Bénéfices": "<db_id>", "Personae": "<db_id>", "Pain Points": "<db_id>",
    "Angles produits": "<db_id>", "Objections": "<db_id>", "Frictions usage": "<db_id>",
    "Roadmap": "<db_id>"
  },
  "row_ids": {
    "<phantom_entity_id>": "<notion_row_id>",
    ...
  },
  "created_count": {"<collection>": N, ...},
  "updated_count": {"<collection>": N, ...},
  "conflicts": [{"phantom_entity_id": "...", "reason": "notion_edited_after_sync"}, ...]
}
```

---

### Step B0 · Pre-checks Phase B spécifiques

Avant Step B1 ·

1. **Brand state check (mode-dependent)** ·
   - Si `--mode=push` · verify `brands/{brand_slug}/brand.json` existe ET `identity.name` non-empty. Si vide · refuse · *"Brand state empty. Pour push, brand doit avoir au moins identity.name. Lance setup-brand + ingest avant push, OU passe `--mode=scaffold` si tu veux juste un workspace Notion blank."*
   - Si `--mode=scaffold` · verify brand state est vide / pre-onboarding (only `brand.json` minimal + `status.json`). Si state populé (audiences/products/angles présents) · refuse · *"Brand a déjà du state populé ({N} audiences · {N} products · {N} angles). Mode scaffold blank serait destructif Notion-side. Use `--mode=push` à la place pour exposer ton state existant."*

2. **Notion parent URL parse** · `notion_parent_url` → extract `parent_page_id`. Verify URL Notion valide · si fail · AskUserQuestion mapping correct.

3. **MCP Notion gate** · même check que Phase A Step 0 L2 (déjà fait Step 0 standard avant ramification mode).

Si Step B0 passe · continue vers Step B1.

---

### Step B1 · Canvas root + Données Atlas wrapper creation

**Goal** · poser le wrapper canvas Onday-style (canvas root + sub-page Données Atlas) avant tout DB creation.

**Sub-step B1.1 · Canvas root page** ·

```
mcp__claude_ai_Notion__notion-create-pages
  parent: {parent_page_id from B0}
  title: "Phantom OS · {brand_name}"
  icon: "🧠"
  content: |
    {Canvas root content blocks ·
    
    Block 1 · 3-column callout layout ·
      Column 1 · Callout "📊 Base de données" + mention link sub-page "Data Client · {brand_name}"
      Column 2 · Callout "🔗 Liens utiles" + placeholders bullets (Drive assets · Drive créas · Slack channel)
      Column 3 · Callout "👤 Espace Client" + placeholder sub-page "Suivi des créas"
    
    Block 2 · Heading 2 "Opérations / lancements"
    Block 3 · Table 5 columns months (rolling 5 prochains mois from date push) · rows · Events (empty) · Budget (empty)
    
    Block 4 · Heading 2 "Roadmap angles/audiences"
    Block 5 · Inline database placeholder (sera replacé Step B2 avec Roadmap DB_id)
    
    Note v2.0.1 territoire-only · canvas root n'inclut PLUS de section "Full funnel Meta" (production layer · push via NEW skill dédié sync-creatives-to-notion v2.68+ futur per doctrine territory-doctrine.md). Si le skill production layer v2.68+ ship, il ajoutera sa propre sub-page cards/Kanban sous canvas root.
    }
```

Store · `canvas_root_id` ← notion_page_id retourné.

**Sub-step B1.2 · Données Atlas wrapper sub-page** ·

```
mcp__claude_ai_Notion__notion-create-pages
  parent: {canvas_root_id}
  title: "Data Client · {brand_name}"
  icon: "#️⃣"
  content: |
    {Documentation header content ·
    
    Heading 1 "Data Client · {brand_name}"
    
    Heading 2 "Comment lire l'ensemble"
    Paragraph · "3 zones reliées · Produit (specs · mécanismes · bénéfices) · Audiences (personae · pain points · objections · frictions usage) · Angles (formula obs+tension+reframe+bridge)."
    
    Heading 2 "Les 9 DBs Data Client en un coup d'œil"
    Table 2 columns (DB ↔ Réponse) ·
      Produits ↔ "Qu'est-ce qu'on vend ?"
      Specs ↔ "De quoi c'est fait ?"
      Mécanismes ↔ "Comment ça marche ?"
      Bénéfices ↔ "Qu'est-ce que le client gagne ?"
      Personae ↔ "Qui achète ?"
      Pain Points ↔ "Pourquoi ils achètent ?"
      Angles produits ↔ "Comment on leur parle ?"
      Objections ↔ "Pourquoi ils n'achètent pas ?"
      Frictions usage ↔ "Pourquoi ils arrêtent ?"
    
    Heading 2 "Comment naviguer"
    Numbered list · 1. Persona → 2. Pain Points → 3. Angles → 4. Formula (obs+tension+reframe+bridge)
    
    Heading 2 "Tags universels (sur les 10 DBs territoire)"
    Bullets · "Source · observed / inferred / declared" · "Confidence · 0-1" · "Validation status · hypothesis / tested / validated / scaled / fatigued"
    }
```

Store · `data_client_page_id` ← notion_page_id retourné.

---

### Step B2 · 10 databases creation pass 1 structure no-relations

**Goal** · créer les 10 DBs Notion territoire (1 sous canvas_root · Roadmap · 9 sous data_client_page · les autres) avec leurs properties non-relation. Les properties `relation` sont DEFERRED à Step B5 (pass 2) pour éviter race condition (relation ne peut pointer vers DB qui n'existe pas encore).

**Note** · Full funnel Meta (creatives = production layer) NOT included in territoire-only push v2.0.1+. Productions sync via NEW skill dédié `sync-creatives-to-notion` v2.68+ futur (cf doctrine `territory-doctrine.md` Section 10 Notion bridge implication).

**Pattern par DB** · `mcp__claude_ai_Notion__notion-create-database` avec parent + properties spec.

**Rate limit** · max 3 requests/seconde à Notion API. Throttle si cascade · `time.sleep(0.4)` entre creates si besoin.

**Hidden property universelle** · chaque DB inclut `phantom_entity_id` (text, hidden default mais queryable) pour idempotency lookup Step B4.

**Tags universels** (3 properties sur chaque DB) ·
- `Source` (select · observed [green] · inferred [yellow] · declared [blue])
- `Confidence` (number · 0-1)
- `Validation status` (select · hypothesis [gray] · tested [yellow] · validated [green] · scaled [purple] · fatigued [red])

**DB 1 · Produits** (parent = data_client_page_id) ·
- `Nom produit` (title)
- `Slug` (text, url-safe)
- `Niche` (select)
- `Positioning` (text)
- `Active offer summary` (text · price + urgency)
- `phantom_entity_id` (text, hidden)
- Tags universels (3 properties)

**DB 2 · Specs** (parent = data_client_page_id) ·
- `Spec name` (title)
- `Type` (select · composition / dosage / certification / packaging / origin / regulatory)
- `Value` (text)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Produit` (relation → Produits)

**DB 3 · Mécanismes** (parent = data_client_page_id) ·
- `Mécanisme name` (title)
- `Description physiologique` (text rich)
- `Duration / délai d'effet` (text · ex "4-6 semaines")
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Produit` (relation → Produits, multi)

**DB 4 · Bénéfices** (parent = data_client_page_id) ·
- `Bénéfice name` (title)
- `Chain level` (select · functional / emotional / identity)
- `Emotional signal` (text)
- `Latency min (jours)` (number)
- `Latency max (jours)` (number)
- `Evidence verbatim` (text rich · multi-line VoC quotes)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Produit` (relation → Produits) + `Mécanisme` (relation → Mécanismes)

**DB 5 · Personae** (parent = data_client_page_id) ·
- `Persona label` (title)
- `Slug` (text, url-safe)
- `Awareness stage` (select · unaware / problem-aware / solution-aware / product-aware / most-aware)
- `Demographics` (text rich)
- `JTBD primary` (text)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Produit principal` (relation → Produits)

**DB 6 · Pain Points** (parent = data_client_page_id) ·
- `Pain formulation` (title · customer language)
- `Category` (select · physical / emotional / friction_ux / logistical / cognitive / social_status)
- `Emotion` (text)
- `Trigger` (text · moment déclencheur)
- `Verbatim quotes` (text rich · VoC + sample_size en parenthèses)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Persona` (relation → Personae) + `Bénéfice servi` (relation → Bénéfices)

**DB 7 · Angles produits** (parent = data_client_page_id) ·
- `Angle name` (title)
- `Angle ID` (text · pattern ANG-NN)
- `Origin axis` (select · audience-derived / product-derived / category-derived / brand-derived / temporal-cultural)
- `Awareness stage in` (select · 5 stages canon)
- `Awareness stage out` (select · 5 stages canon)
- `Formula Observation` (text)
- `Formula Tension` (text)
- `Formula Reframe` (text)
- `Formula Bridge produit` (text)
- `Hook canon ID` (text)
- `Framework canon ID` (text)
- `Archetype voix canon ID` (text)
- `Pain extract` (text)
- `Proof primary` (text)
- `CTA` (text)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Persona cible` (relation → Personae)

**DB 8 · Objections** (parent = data_client_page_id) ·
- `Objection formulation` (title)
- `Type` (select · price / scepticism / fit / urgency / trust / status / risk)
- `Lifecycle` (select · awareness / consideration / decision / post-purchase)
- `Severity score` (number 1-10)
- `Response counter` (text)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Persona` (relation → Personae, multi) + `Angle dérivé` (relation → Angles produits, multi)

**DB 9 · Frictions usage** (parent = data_client_page_id) ·
- `Friction name` (title)
- `Friction ID` (text · pattern FRC-NN)
- `Category` (select · physical / emotional / friction_ux / logistical / cognitive)
- `Severity score` (number 1-10)
- `Customer evidence` (text rich)
- `Current workarounds` (text)
- `Resolution state` (select · unresolved / in_progress / resolved / accepted)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Affected products` (relation → Produits, multi) + `Affected audiences` (relation → Personae, multi) + `Cross-ref objections` (relation → Objections, multi) + `Cross-ref pain points` (relation → Pain Points, multi)

**DB 10 · Roadmap** (parent = **canvas_root_id**, pas data_client_page) ·
- `Phase name` (title)
- `Phase ID` (text)
- `Dates start` (date)
- `Dates end` (date)
- `Status` (select · draft / in-progress / shipped / paused / killed)
- `Mix axis` (select · audience / angle / product / funnel / creative)
- `Weight` (number 0-1)
- `Production status` (select · spec'd / in-production / shipped / iterating)
- `Priorities (top 3)` (text rich · bullets)
- `phantom_entity_id` (text, hidden)
- Tags universels
- **DEFERRED Step B5** · `Angles refs` (relation → Angles, multi) + `Audiences refs` (relation → Personae, multi) + `Products refs` (relation → Produits, multi) + `Creatives refs` (relation field shape conservé pour future bind via skill production layer v2.68+ · resolution empty Step B5b v2.0.1+ · creatives non sync par ce skill)

**Production layer NOT pushed (territoire-only doctrine)** · Full funnel Meta (creatives) RETIRÉE de la loop Step B2 v2.0.1+. La DB creatives sera créée par NEW skill dédié `sync-creatives-to-notion` v2.68+ futur (production layer · cards/Kanban Notion pour briefs + créas par angle · skill séparé per doctrine `territory-doctrine.md` Section 10 Notion bridge implication · Section 12 Anti-patterns mixed orchestrator). Pattern canon · 1 skill par layer.

Store dans working memory · `db_ids = {collection_name: notion_db_id}` mapping (10 entries territoire).

**Sub-step B2.bis · scaffold mode shortcut** · si `--mode=scaffold`, jump direct to Step B5a (add relation properties pass 2a only, skip Step B3 + Step B5b row-relation-binding). Workspace ship blank canon.

---

### Step B3 · Rows population per PhantomOS entity (mode=push only)

**Goal** · pour chaque entité PhantomOS sous `brands/{brand_slug}/`, créer rows correspondants dans les DBs Notion. Toutes relations sont DEFERRED à Step B5b (set après Step B5a a ajouté les relation properties aux DBs).

**Mode=scaffold** · skip entièrement Step B3.

**Convention `phantom_entity_id` (idempotency key)** ·
- Produits · `prod-{product_slug}`
- Specs · `spec-{product_slug}-{spec_type}-{index}` (ex `spec-multivit-composition-0`)
- Mécanismes · `mech-{product_slug}-{index}` (ex `mech-multivit-0`)
- Bénéfices · `bnf-{product_slug}-{index}`
- Personae · `pers-{audience_slug}`
- Pain Points · `pain-{audience_slug}-{index}`
- Angles · `{angle_id}` (ex `ANG-01`)
- Objections · `obj-{audience_slug}-{index}` (ou `OBJ-NN` canonical si dispo)
- Frictions · `{friction_id}` (ex `FRC-01`)
- Roadmap phases · `roadmap-phase-{phase_id}` (ex `roadmap-phase-P1`)
- Creatives · `{creative_id}` (ex `CRT-12`)

**Property mapping PhantomOS → Notion (inverse Phase A Step 3)** ·

#### B3.1 · Produits (depuis `brands/{slug}/products/{p}/spec.json` + `offers.json`)
Pour chaque product folder ·
```
Map ·
  Nom produit ← spec.identity.product_name
  Slug ← {product_slug}
  Niche ← spec.market_context.niche
  Positioning ← spec.identity.positioning
  Active offer summary ← compute from offers.offer_groups[0] (price + urgency_window résumé 1 ligne)
  phantom_entity_id ← "prod-{product_slug}"
  
mcp__claude_ai_Notion__notion-create-pages
  parent: {db_ids["Produits"]}
  properties: {Map above}
```
Store · `row_ids["prod-{product_slug}"]` ← notion_row_id.

#### B3.2 · Specs (depuis `spec.composition` + `spec.specs.*`)
Pour chaque composition entry et chaque spec entry · 1 row Specs ·
```
Map ·
  Spec name ← composition[i].name OR specs[type].label
  Type ← composition / dosage / certification / packaging / origin / regulatory
  Value ← composition[i].value OR specs[type].value
  phantom_entity_id ← "spec-{product_slug}-{type}-{i}"
  
mcp__claude_ai_Notion__notion-create-pages parent={db_ids["Specs"]} properties=Map
```

#### B3.3 · Mécanismes (depuis `spec.mechanisms[]`)
```
Map per mechanism ·
  Mécanisme name ← mechanisms[i].name
  Description physiologique ← mechanisms[i].description
  Duration / délai d'effet ← mechanisms[i].duration
  phantom_entity_id ← "mech-{product_slug}-{i}"
```

#### B3.4 · Bénéfices (depuis `spec.benefits[]`)
```
Map per benefit ·
  Bénéfice name ← benefits[i].name
  Chain level ← benefits[i].chain_level (functional / emotional / identity)
  Emotional signal ← benefits[i].emotional_signal
  Latency min (jours) ← benefits[i].latency_min_days
  Latency max (jours) ← benefits[i].latency_max_days
  Evidence verbatim ← benefits[i].evidence_verbatim (join multi-line)
  phantom_entity_id ← "bnf-{product_slug}-{i}"
```

#### B3.5 · Personae (depuis `brands/{slug}/audiences/{a}/profile.json`)
```
Map per audience ·
  Persona label ← profile.identity.label
  Slug ← {audience_slug}
  Awareness stage ← profile.psychology.awareness_stage
  Demographics ← profile.identity.demographics (compact JSON → markdown)
  JTBD primary ← profile.psychology.jtbd_primary
  phantom_entity_id ← "pers-{audience_slug}"
```

#### B3.6 · Pain Points (depuis `profile.pain_benefit_chain[]`)
Pour chaque audience, pour chaque pain entry ·
```
Map ·
  Pain formulation ← pain_benefit_chain[i].pain_formulation
  Category ← pain_benefit_chain[i].pain_category
  Emotion ← pain_benefit_chain[i].emotion
  Trigger ← pain_benefit_chain[i].trigger
  Verbatim quotes ← pain_benefit_chain[i].verbatim_quotes (join + sample_size)
  phantom_entity_id ← "pain-{audience_slug}-{i}"
```

#### B3.7 · Angles produits (depuis `brands/{slug}/angles/{ANG-NN}.json`)
```
Map per angle ·
  Angle name ← angle.name
  Angle ID ← angle.angle_id
  Origin axis ← angle.origin_axis
  Awareness stage in ← angle.awareness_movement.stage_in
  Awareness stage out ← angle.awareness_movement.stage_out
  Formula Observation ← angle.formula.observation
  Formula Tension ← angle.formula.tension
  Formula Reframe ← angle.formula.reframe
  Formula Bridge produit ← angle.formula.bridge_product
  Hook canon ID ← angle.lineage.hook_canon_id
  Framework canon ID ← angle.lineage.framework_canon_id
  Archetype voix canon ID ← angle.lineage.archetype_voix_canon_id
  Pain extract ← angle.insight.pain_extract
  Proof primary ← angle.insight.proof_primary
  CTA ← angle.insight.cta
  phantom_entity_id ← angle.angle_id
```

#### B3.8 · Objections (depuis `profile.objections[]`)
Pour chaque audience, pour chaque objection ·
```
Map ·
  Objection formulation ← objections[i].formulation
  Type ← objections[i].type
  Lifecycle ← objections[i].lifecycle
  Severity score ← objections[i].severity_score
  Response counter ← objections[i].response_counter
  phantom_entity_id ← objections[i].objection_id OR "obj-{audience_slug}-{i}"
```

#### B3.9 · Frictions usage (depuis `brands/{slug}/frictions/{FRC-NN}.json`)
```
Map per friction ·
  Friction name ← friction.name
  Friction ID ← friction.friction_id
  Category ← friction.category
  Severity score ← friction.severity_score
  Customer evidence ← friction.customer_evidence (join multi-line)
  Current workarounds ← friction.current_workarounds (join, "; ")
  Resolution state ← friction.resolution_state
  phantom_entity_id ← friction.friction_id
```

#### B3.10 · Roadmap (depuis `brands/{slug}/roadmap.json#/phases[]` + `mix[]`)
1 row par phase ·
```
Map per phase ·
  Phase name ← phases[i].name
  Phase ID ← phases[i].phase_id
  Dates start ← phases[i].dates.start
  Dates end ← phases[i].dates.end
  Status ← phases[i].status
  Mix axis ← phases[i].mix_axis_primary (or null si phase-level pas mix-level)
  Weight ← phases[i].weight_primary (or null)
  Production status ← phases[i].production_status
  Priorities (top 3) ← phases[i].priorities (join bullets)
  phantom_entity_id ← "roadmap-phase-{phase_id}"
```
Note · `mix[]` est aggregat singleton, expose via `Mix axis` + `Weight` rolled-up dans phase rows pour Phase B v2.0.0+. Si besoin separate per-mix rows émerge use-case futur, ajouter colonne dédiée.

#### B3.11 · Full funnel Meta · SKIP v2.0.1+ (production layer)

**Creatives skip** · production layer NON couvert par sync-notion-atlas v2.0.1+. La mapping `creatives/{CRT-NN}.json → 1 row Full funnel Meta` est RETIRÉE de la table mappings Step B3 v2.0.1+. Push creatives via NEW skill dédié `sync-creatives-to-notion` v2.68+ futur (production layer · cards/Kanban Notion pour briefs + créas par angle · per doctrine `territory-doctrine.md`). Skill dédié futur · 1 skill par layer canon.

**Mappings table Step B3 v2.0.1+ · 10 entités territoire seulement** · B3.1 Produits · B3.2 Specs · B3.3 Mécanismes · B3.4 Bénéfices · B3.5 Personae · B3.6 Pain Points · B3.7 Angles · B3.8 Objections · B3.9 Frictions usage · B3.10 Roadmap. B3.11 Full funnel Meta retirée (production layer · futur skill dédié).

**Tags universels per row (toutes les 10 DBs territoire)** ·
- `Source` ← reverse `_field_types` per entity (observed→observed · derived→inferred · stated→declared · default declared)
- `Confidence` ← `meta.confidence` numeric direct (0-1)
- `Validation status` ← `meta.validation_status` enum direct (hypothesis/tested/validated/scaled/fatigued)

**No invented data rule** · si un PhantomOS field est null/missing, SKIP la property Notion (do NOT default a value). Le row ship avec property vide Notion-side.

**Stage all or none discipline** · si un row creation fail (Notion API error, property invalide) · log error, flag dans Step B7 Section 4 Leviers, continue le batch. Pas de rollback automatique.

**MCP call pattern par row** ·
```
mcp__claude_ai_Notion__notion-create-pages
  parent: {db_ids[target_collection]}
  properties: {Map à partir entity PhantomOS}
```

Store · `row_ids[phantom_entity_id]` ← notion_row_id retourné. Critical pour Step B5b resolution.

**Compteurs** · `created_count[collection] += 1` (ou `updated_count[collection] += 1` si Step B4 a flagué update).

---

### Step B4 · Idempotency lookup (interleaved pre Step B2 + Step B3)

**Goal** · re-run de push update existing rows par `phantom_entity_id` plutôt que dupliquer. Hard rule canon · NEVER create duplicate.

**Sub-step B4.1 · DB-level lookup (avant chaque create Step B2)** ·

Pour chaque DB à créer Step B2, AVANT le `notion-create-database` ·
```
mcp__claude_ai_Notion__notion-search
  query: "{db_title}"
  parent_id: {canvas_root_id OR data_client_page_id selon target}
```

Si match retourné (DB déjà existe sous parent avec ce titre) · skip create, store existing `db_id` dans `db_ids[collection]`, log "DB {name} pre-existing, reused".

Si zéro match · proceed avec create normal Step B2.

**Sub-step B4.2 · Row-level lookup (avant chaque create Step B3)** ·

Pour chaque entity à push Step B3, AVANT le `notion-create-pages` ·
```
mcp__claude_ai_Notion__notion-query-database-view
  database_id: {db_ids[target_collection]}
  filter: {property: "phantom_entity_id", text: {equals: "{target_id}"}}
```

Si match retourné (1 row existant avec ce phantom_entity_id) ·
- Extract `notion_row_id` + `last_edited_time` du match.
- **Conflict check** · si `last_edited_time` (Notion-side) > `_synced_at` PhantomOS-side timestamp · FLAG conflict ·
  ```
  conflicts.append({
    "phantom_entity_id": target_id,
    "notion_row_id": notion_row_id,
    "reason": "notion_edited_after_sync",
    "notion_last_edited": last_edited_time,
    "phantom_synced_at": phantom_synced_at
  })
  ```
  → do NOT overwrite. Skip update for this row. Surface dans Section 4 Step B7 Leviers (Phase C diff candidate v2.59+).
- Si pas de conflict · UPDATE via `mcp__claude_ai_Notion__notion-update-page` (pas create) ·
  ```
  mcp__claude_ai_Notion__notion-update-page
    page_id: {notion_row_id}
    properties: {Map}
  ```
  Increment `updated_count[collection] += 1`. Store `row_ids[phantom_entity_id]` ← existing notion_row_id.

Si zéro match · proceed avec create normal Step B3, increment `created_count[collection] += 1`.

**Hard rule** · re-run push = update existing par `phantom_entity_id`, NEVER duplicate. Soft rule · Notion-side edits post-sync = flag conflict, no silent overwrite.

---

### Step B5 · Relations cross-link binding (pass 2 · 2 sub-passes)

**Goal** · après Steps B2 (DBs created) + B3 (rows populated), résoudre les relations cross-DB en 2 sub-passes ·

**Sub-pass B5a · Add relation properties to DBs** ·

Pour chaque DB ayant des relations DEFERRED Step B2, run ·
```
mcp__claude_ai_Notion__notion-update-data-source
  data_source_id: {db_ids[collection]}
  add_properties: [
    {name: "Produit", type: "relation", relation: {database_id: {db_ids["Produits"]}}},
    ... per DB's deferred relations ...
  ]
```

Mapping deferred relations à ajouter ·
- **Specs** · `Produit` → Produits
- **Mécanismes** · `Produit` → Produits (multi)
- **Bénéfices** · `Produit` → Produits + `Mécanisme` → Mécanismes
- **Personae** · `Produit principal` → Produits
- **Pain Points** · `Persona` → Personae + `Bénéfice servi` → Bénéfices
- **Angles produits** · `Persona cible` → Personae
- **Objections** · `Persona` → Personae (multi) + `Angle dérivé` → Angles produits (multi)
- **Frictions usage** · `Affected products` → Produits (multi) + `Affected audiences` → Personae (multi) + `Cross-ref objections` → Objections (multi) + `Cross-ref pain points` → Pain Points (multi)
- **Roadmap** · `Angles refs` → Angles (multi) + `Audiences refs` → Personae (multi) + `Products refs` → Produits (multi). Le `Creatives refs` field shape conservé Notion-side pour future bind via skill production layer v2.68+, mais relation property cible (Full funnel Meta DB) PAS créée par sync-notion-atlas v2.0.1+ (creatives = production layer · skill séparé futur).
- **Full funnel Meta · NOT pushed v2.0.1+.** Production layer routée via NEW skill dédié `sync-creatives-to-notion` v2.68+ futur. Relations `CONTEXTE angle` + `CONTEXTE persona` seront gérées par le skill production layer dédié (cf doctrine `territory-doctrine.md`).

**Sub-pass B5b · Set relation values on rows** (skip si mode=scaffold) ·

Pour chaque row créé/updaté Step B3, résoudre ses cross_refs PhantomOS-side vers notion_row_ids via `row_ids` mapping working memory ·

Pattern resolution per entity type ·

- **Specs row** · resolve `spec.cross_refs.product_slug` → `row_ids["prod-{product_slug}"]`. Set property `Produit` = [resolved_notion_row_id].
- **Mécanismes row** · resolve product_slugs (multi) → list of `row_ids["prod-{slug}"]`. Set `Produit` (multi).
- **Bénéfices row** · resolve product + mécanisme refs.
- **Personae row** · resolve product principal ref.
- **Pain Points row** · resolve audience_slug → `row_ids["pers-{slug}"]` + benefit_served_id → `row_ids[bnf-id]`.
- **Angles row** · resolve `angle.audience_slug` → `row_ids["pers-{audience_slug}"]`. Set `Persona cible`.
- **Objections row** · resolve audience_slugs (multi) + `objections.derived_angle_refs[]` (multi · resolve each `ANG-NN` to `row_ids[ANG-NN]`).
- **Frictions usage row** · resolve `friction.affected_products[]` + `friction.affected_audiences[]` + `friction.cross_refs.objection_ids[]` + `friction.cross_refs.pain_point_ids[]` (each multi).
- **Roadmap row** · resolve `phases[i].priorities[].angle_ids[]` + `phases[i].priorities[].audience_slugs[]` + `phases[i].priorities[].product_slugs[]` (collect per phase, set on phase row, all multi). Le `Creatives refs` field shape conservé Notion-side mais resolution = empty Step B5b v2.0.1+ (creatives pas sync · skip silently · binding fait par skill production layer v2.68+ futur).
- **Full funnel Meta row** · NOT pushed v2.0.1+ (production layer). Resolution `creative.context.angle_id` + `creative.audience_slug` sera gérée par NEW skill dédié `sync-creatives-to-notion` v2.68+ futur.

**MCP call pattern** ·
```
mcp__claude_ai_Notion__notion-update-page
  page_id: {row_ids[phantom_entity_id]}
  properties: {<relation_name>: <list of resolved notion_row_ids>, ...}
```

**Resolution failure handling** · si une cross_ref pointe vers un PhantomOS ID absent du `row_ids` mapping (target entity pas pushé, ou nom mal référencé) · log warning, skip cette relation pour cette row, increment `relations_unresolved_count`. Surface % `pct_relations_linked` dans Step B7 Section 1.

---

### Step B6 · Tags universels + epistemic sync stamp (verify pass)

**Goal** · pass de vérification que chaque row créé/updaté Step B3 a bien ses 3 tags universels (Source · Confidence · Validation status) set explicitement. Cas typique · row updaté Step B4 (idempotent) pré-existait Notion-side, vérifier qu'il a hérité des nouveaux tags PhantomOS-side.

Pour chaque row dans `row_ids` ·
- Si row a été créé Step B3 · tags déjà set inline via property mapping (rien à faire).
- Si row a été updaté Step B4 idempotent · re-verify Source / Confidence / Validation status présents et alignés sur PhantomOS state actuel. Si missing · `mcp__claude_ai_Notion__notion-update-page` avec defaults défensifs ·
  ```
  Source = "declared" (default défensif si _field_types absent)
  Confidence = 0.7 (default défensif si meta.confidence absent)
  Validation status = "hypothesis" (default défensif si meta.validation_status absent)
  ```
  Aligné canon Phase A Step 3 tags universels mapping lignes 287-298.

**Stamp pass · agnostic** · permet aux 3 tags d'être source of truth bidirectionnelle (Notion-side opérateur peut corriger Source=observed après audit verbatim, et Phase A pull v2.66+ rapatriera la correction si --mode=pull relance).

---

### Step B7 · Synthesis output 5 sections investigation-posture

**Goal** · output final canonique respectant `docs/system/investigation-posture.md` (5 sections explicites, jamais fusionnées en prose).

#### Section 1 · Observé (faits sourcés)

> *Observé · workspace Notion créé sous {notion_parent_url} ({date}, {durée_total_push})*
>
> *Canvas root · {canvas_url} (page "Phantom OS · {brand_name}")*
> *Data Client wrapper · {data_client_url} (sub-page "Data Client · {brand_name}")*
>
> *10 db_ids territoire créés/réutilisés ·*
> *  • Produits · {created_count.Produits} créées · {updated_count.Produits} mises à jour*
> *  • Specs · {created_count.Specs} / {updated_count.Specs}*
> *  • Mécanismes · {created_count.Mécanismes} / {updated_count.Mécanismes}*
> *  • Bénéfices · {created_count.Bénéfices} / {updated_count.Bénéfices}*
> *  • Personae · {created_count.Personae} / {updated_count.Personae}*
> *  • Pain Points · {created_count.PainPoints} / {updated_count.PainPoints}*
> *  • Angles produits · {created_count.Angles} / {updated_count.Angles}*
> *  • Objections · {created_count.Objections} / {updated_count.Objections}*
> *  • Frictions usage · {created_count.Frictions} / {updated_count.Frictions}*
> *  • Roadmap · {created_count.Roadmap} phases*
>
> *Note v2.0.1 · creatives (Full funnel Meta) NOT pushed (production layer · NEW skill dédié `sync-creatives-to-notion` v2.68+ futur).*
>
> *Total · {sum(created)} rows créés · {sum(updated)} rows updatés idempotent (par phantom_entity_id) sur 10 collections territoire*
>
> *Relations cross-DB · {pct_relations_linked}% des cross_refs PhantomOS résolues vers Notion page IDs ({N_resolved} / {N_total} cross_refs)*
>
> *Tags universels stampés cross-rows ·*
> *  • Source set sur {pct_source}% des rows*
> *  • Confidence set sur {pct_confidence}% des rows*
> *  • Validation status set sur {pct_status}% des rows*

#### Section 2 · Déduit (hypothèses)

> *Déduit · qualité du scaffold reflète la densité du state PhantomOS source*
>
> *H1 · Densité cross_refs PhantomOS-side*
> *  Confidence · {forte si pct_relations_linked > 80% · moyenne si 50-80% · faible si < 50%}*
> *  Indicateurs · {N_cross_refs_resolved} relations résolues sur {N_cross_refs_total} cross_refs présentes PhantomOS state*
> *  À valider · Si pct < 50%, le state PhantomOS est sparse (peu de cross-refs entre entités). Workspace Notion sera navigable mais relations vides. Tu veux qu'on enrichisse les cross_refs PhantomOS d'abord, ou ship as-is ?*
>
> *H2 · Conflicts détectés (Notion-side edits post dernier sync)*
> *  Confidence · {forte si {len(conflicts)} > 0, sinon zéro}*
> *  Indicateurs · {len(conflicts)} rows pré-existaient Notion-side avec last_edited_time > _synced_at PhantomOS. Skip overwrite, candidats Phase C diff v2.59+.*

#### Section 3 · Inconnu (variables non observables)

> *Inconnu · {N} variables à creuser*
>
> *1. Adoption Notion-side · le client / collab à qui tu shares l'URL va-t-il vraiment utiliser cette UI vs PhantomOS canon ? Inconnu jusqu'à feedback.*
> *2. Drift PhantomOS ↔ Notion futur · les edits Notion-side post-push créeront du drift cumulatif. Audit via Phase C diff v2.59+.*
> *3. Cohérence relations resolved · les {pct_relations_linked}% résolues sont-elles sémantiquement correctes ou juste structurellement liées ? Audit manuel.*
> *4. Conflicts non-résolus · {len(conflicts)} rows Notion-side modifiés depuis sync → divergence entre Notion truth opérateur et PhantomOS canon · arbitrage manuel ou Phase C v2.59+.*

#### Section 4 · Leviers (options drill-down)

> *Leviers · {N} axes d'investigation prioritaires*
>
> *Axe A · Share URL au client / collab pour review*
> *  → Workspace prêt à partager · canvas root URL ci-dessus · client peut naviguer 10 DBs territoire + canvas Onday-style*
> *  → Reco · accompagner share par doc "Comment lire l'ensemble" (Data Client page déjà documenté Sub-step B1.2)*
>
> *Axe B · Re-run push idempotent quand PhantomOS évolue*
> *  → Re-invoke `--mode=push` à tout moment · les rows existants updatent par phantom_entity_id · nouveaux entities créés · aucune duplication*
> *  → Si Notion édité side opérateur entre 2 push · conflicts surfacés Section 4 Leviers post-run*
>
> *Axe C · Resolve conflicts détectés (si {len(conflicts)} > 0)*
> *  → Phase C diff v2.59+ permettra audit explicite delta Notion ↔ PhantomOS avant overwrite*
> *  → En attendant v2.59+ · review manuelle des {len(conflicts)} rows, decide source-of-truth, sync manuel*
>
> *Axe D · Populate Opérations table manuelle (canvas root)*
> *  → Table 5 colonnes mois shipped vide Step B1.1 · à populer manuellement Notion-side (events + budget) hors scope skill*
>
> *Axe E · Phase A pull pour rapatrier edits Notion → PhantomOS plus tard*
> *  → Cycle bidirectionnel opérationnel · `--mode=pull` après que client a édité Notion = rapatrie corrections vers PhantomOS canon*
>
> *Axe F · Creatives push deferred via NEW skill dédié `sync-creatives-to-notion` v2.68+ futur*
> *  → Production layer (briefs + créas par angle) routée via skill séparé · cards/Kanban Notion (pas tabular DB territoire) per doctrine `territory-doctrine.md`*
> *  → En attendant v2.68+ ship · creatives restent canon PhantomOS-side (`brands/{slug}/creatives/{CRT-NN}.json`) · push Notion manuel temporairement si besoin urgent*

#### Section 5 · Close ouvert (UNE question macro)

> *Workspace Notion canon créé sous {canvas_url}, {sum(created)} rows shipped, {pct_relations_linked}% relations linked, {len(conflicts)} conflicts détectés.*
>
> *Tu veux que je share l'URL à ton client / collab pour review, OU on enchaîne sur la table Opérations / lancements à populer manuellement Notion-side, OU on stop ici et tu inspectes le workspace ?*

#### Hard rules cross-section synthèse (cf. investigation-posture.md)

- **5 sections explicites, jamais fusionnées en prose continue.** Anti-pattern AP-6 doctrine.
- **JAMAIS exposer confidence numeric à l'opérateur.** Confidence chain qualitatif uniquement.
- **JAMAIS nommer le skill interne en surface opérateur** (`mcp__claude_ai_Notion__*` interne = OK si présenté comme workflow, pas comme path technique).
- **JAMAIS clôturer avec affirmation** · close ouvert toujours UNE question macro drill-down.
- **JAMAIS inventer data Notion pour combler les vides PhantomOS-side.** Si une cross_ref pointe vers entity absente, skip silent (log warn dans `relations_unresolved_count`).

---

### Hard rules Phase B spécifiques

- **Idempotent par `phantom_entity_id`.** Re-run push update les pages Notion existantes par phantom_entity_id (hidden text property sur chaque DB). JAMAIS création duplicate. Pattern · query Notion par phantom_entity_id → si match update, sinon create (Step B4).
- **No silent overwrite Notion-side edits.** Si page Notion `last_edited_time` > PhantomOS `_synced_at` · flag conflict Section 4 Leviers, do NOT overwrite. Phase C diff v2.59+ candidat resolve.
- **2-pass create pattern · DBs first (B2), relations second (B5).** Eviter race condition relation → DB inexistante. Sub-pass B5a ajoute relation properties aux DBs, sub-pass B5b set values sur rows.
- **Rate limit Notion API 3 req/sec.** Throttle si cascade requests (Steps B2 + B3 + B5 ont beaucoup de calls). `time.sleep(0.4)` entre creates si besoin.
- **Mode scaffold blank-only.** Si brand a state populé · refuse `--mode=scaffold` (anti-pattern · scaffold blank effacerait Notion existant). Propose `--mode=push` à la place (Step B0 pre-check).
- **Canvas wrapper template fidèle Onday-style.** Step B1 reproduit le canvas Onday (3 colonnes callouts + Opérations table + Données Atlas sub-page) miroir stride-up. Reproductible cross-clients Abyss collectif.
- **No invented data Notion-side.** Si PhantomOS field null/missing · skip property Notion-side (Step B3). Do NOT default a value. Parité doctrinale `snapshot-brand § Never invent`.
- **Stage all or none discipline (partial).** Si row creation/update fail · log, flag Section 4, continue batch. Pas de rollback automatique (anti-pattern destructive).
- **`brand.json` not pushed.** Brand identity reste canon PhantomOS-side, jamais exposée Notion-side (anti-pattern leak identity data multi-clients agency).
- **Production layer NOT pushed.** Creatives (Full funnel Meta collection canon stride-up) sont production layer per doctrine `territory-doctrine.md` · NOT pushed par sync-notion-atlas v2.0.1+. Push creatives via NEW skill dédié `sync-creatives-to-notion` v2.68+ futur (production layer Notion · cards/Kanban briefs+créas par angle). Pattern canon · 1 skill par layer. Évite mixed orchestrator anti-pattern (cf doctrine `territory-doctrine.md` Section 12 Anti-patterns).

### Workflow post-Phase B (cycle bidirectionnel)

1. Largo run `--mode=push {brand_slug} {notion_parent_url}` · workspace Notion populé from PhantomOS state · 10 collections territoire · partage URL au client/collab.
2. Client/collab édite Notion-side · territoire (corrections, enrichissements, validation_status updates sur 10 collections).
3. Largo run `--mode=pull {brand_slug} {notion_url}` plus tard pour rapatrier les edits Notion → PhantomOS via mutation gate.
4. Cycle bidirectionnel opérationnel. Conflicts détectés Step B4 idempotency check candidate Phase C diff v2.59+.

**Note v2.0.1+** · Productions (briefs + creatives) éditées via outils séparés · Notion canvas brand-side = territoire only · production tooling via `creative-brief-composer` (canon PhantomOS-side) + futur `sync-creatives-to-notion` v2.68+ (cards/Kanban Notion production layer). Layer split strict per doctrine `territory-doctrine.md`.

### Évolutions futures Phase B+

- **v2.0.2 · canvas template extended** · Liens utiles populé (drive URLs depuis brand config) · Opérations table avec dates auto-générées (12 prochains mois rolling).
- **v2.0.3 · separate per-mix rows Roadmap** · si `roadmap.mix[]` granularity émerge use-case, ajouter colonne dédiée vs rolled-up dans phase rows.
- **v2.59 · `--mode=diff`** · compare state PhantomOS vs Notion, surface deltas operator-facing en 5 sections, resolve conflicts détectés Step B4.
- **v2.60 · multi-Notion sources aggregation** · 1 PhantomOS brand pulled from N Notion workspaces (Abyss collectif scaling).
- **v2.68+ · NEW skill `sync-creatives-to-notion` production layer** · canvas cards/Kanban Notion pour briefs + creatives par angle · skill dédié séparé · 1 skill par layer canon (cf doctrine `territory-doctrine.md`).

---

### Workflow post-sync (opérateur arbitre)

1. Synthesis Section 5 propose le drill-down macro (A / B / C).
2. Si A · opérateur va dans `brands/{slug}/pending-validations.md`, bulk accept (workflow standard PhantomOS).
3. Si B · opérateur review collection par collection, accept/reject/correct par mutation, agent peut driller sur une collection si besoin.
4. Si C · agent drille sur la collection problématique (re-cycle 5 sections sur le focus).

Le sync ne ferme pas la conversation. Il ouvre le workflow validation classique PhantomOS.

### Re-sync

Stateless idempotent. Re-run `/sync-notion-atlas {brand_slug} --mode=pull {notion_url}` à tout moment quand Notion mis à jour. Les mutations re-stagées remplacent les pending non-accept (write-to-context mode=proposed gère le merge / overwrite per-field). Idempotent par design.

---

## Hard rules

- **Mutation gate strict.** TOUT write via `python3 .skills/write-to-context.py`. JAMAIS `Edit/Write/NotebookEdit` sur les `.json` sous `brands/{brand_slug}/`. Bypass = refusé runtime par mutation-guard PreToolUse hook + corrupt proposal/acceptance workflow. Doctrine canon · `docs/system/schema-encoding-doctrine.md § Mutation rule`.
- **isolation_scope brand_only.** Le sync n'affecte QUE `brands/{brand_slug}/`. JAMAIS workspace-global, JAMAIS cross-brand. 1 brand par invocation. Pour sync brand A + brand B · 2 invocations distinctes. Doctrine canon · `docs/system/brand-isolation-doctrine.md`.
- **Stateless idempotent.** Re-run identique = même résultat. Notion = source of truth en mode pull, PhantomOS canonical write via gate. Idempotent par design (les mutations re-stagées remplacent les pending non-accept).
- **No scoring leak.** JAMAIS expose confidence numeric à l'opérateur. Use qualitatif `forte / moyenne / faible / TRÈS faible` per investigation-posture canon. Confidence numeric reste agent-side / encoded JSON / consumers internes.
- **No em-dash.** Canon style strict (cf. CLAUDE.md root · *no em-dash global*). Substitute par middle dot ·, parenthèses, virgule, point, deux-points. Zero em-dash en operator surface, code comments, prose interne, output schema description, partout.
- **Stage all or none (partial).** Si validate-resources MAJOR sur une entité stagée · flag dans Section 3 / Section 4 synthesis, **continue le batch** sur les autres. Pas de rollback automatique (anti-pattern destructive). L'opérateur arbitre via pending-validations.md.
- **No invented data.** Si row Notion a champ vide (property null / empty) · le champ PhantomOS reste vide / null. JAMAIS d'inférence pour combler. Notion = source of truth en mode pull. Hard rule absolue, parité doctrinale `snapshot-brand § Never invent`.
- **No-orphan output.** Close drill-down macro UNE question, JAMAIS menu plat (a/b/c/d equal-weight), JAMAIS *"voilà fait, autre chose ?"*. Reco macro explicite avec rationale 1 ligne. Doctrine canon · `contextual-intelligence.md § No orphan output`.
- **Backward compat strict additif.** Skill NEW v2.57, n'override aucun existant. Phases B (push) + diff stubbées mais inactives v1.0.0. Invocation `--mode=push` ou `--mode=diff` refuse cleanly avec roadmap d'évolution.
- **Operator-facing rule absolue.** JAMAIS nommer doctrine names (Compositional Cartography, Schema Encoding Discipline, Investigation Posture, DRGFP), acronymes, paths internes (`brands/{slug}/.workflow.json`, `write-to-context.py`, `validate-resources` interne), enum brut (`isolation_scope`, `_field_types`, `_source`) en surface opérateur. L'opérateur voit l'effet (proposals stagées prêtes à valider), JAMAIS la plomberie.
- **MCP Notion gate strict.** Pas de fallback silencieux si MCP absent · refuse cleanly Step 0 L2 gate avec 3 options AskUserQuestion (setup MCP / abort / cached snapshot). Pas de pseudo-pull depuis fake source.
- **No bidirectionnel auto-sync.** Phase A pull-only · jamais de push silencieux post-pull. L'opérateur invoque explicitement chaque sync. Anti-pattern · auto-loop Notion ↔ PhantomOS sans gate operator.
- **JAMAIS de bridge mutation cross-brand.** Un sync = un brand. JAMAIS de pull data depuis Notion brand A vers brand B (anti-pattern AP-4 notion-bridge-doctrine.md).

---

## Cross-references

### Doctrine canon
- `docs/system/notion-bridge-doctrine.md` · source canon doctrine bridge bidirectionnel (mappings, edge cases, anti-patterns, layer 1 positioning)
- `docs/system/compositional-cartography.md` · 4 arbres compositionnels + matrice canon + modulateurs que les 11 collections Notion stride-up implémentent (§4 mappings table)
- `docs/system/brand-isolation-doctrine.md` · isolation_scope brand_only enforcement (default obligatoire, privacy multi-clients agency)
- `docs/system/investigation-posture.md` · 5 sections close synthesis canon (Observé / Déduit / Inconnu / Leviers / Close ouvert)
- `docs/system/schema-encoding-doctrine.md` · mutation rule canon (write-to-context.py only) + `_field_types` enum + sourcing tags
- `docs/system/connectivity-layering.md` · Layer 1 MCP servers (Notion MCP positioning)
- `docs/system/dependency-resolution-protocol.md` · DRGFP L1/L2/L3 prerequisite checks Step 0

### Schemas canon consumés
- `resources/schemas/brand.schema.json` · brand identity (read-only, sync n'affecte pas brand.json)
- `resources/schemas/spec.schema.json` · produits + specs + mechanisms + benefits
- `resources/schemas/offer.schema.json` · offers v2 (offer_groups[])
- `resources/schemas/profile.schema.json` · personae + pain_benefit_chain + objections
- `resources/schemas/angle.schema.json` · angles produits (ANG-NN)
- `resources/schemas/friction.schema.json` · NEW v2.56 frictions usage (FRC-NN)
- `resources/schemas/roadmap.schema.json` · NEW v2.56 roadmap singleton (RDM-{slug})
- `resources/schemas/creative.schema.json` · creatives Full funnel Meta (CRT-NN)
- `resources/schemas/funnel.schema.json` · funnel global brand
- `resources/schemas/_shared/validation-status.json` · enum validation_status canon

### Skills pattern miroir + downstream
- `.skills/skills/snapshot-brand/SKILL.md` · pattern miroir scrape + map + stage (URL e-commerce brand vs URL workspace Notion · UPSTREAM différent)
- `.skills/skills/ingest-resource/SKILL.md` · pattern délégation encode-batch Haiku pour batches > 5 mutations
- `.skills/skills/encode-batch/SKILL.md` · sub-agent Haiku canonical pour scaler les mutations
- `.skills/skills/validate-resources/SKILL.md` · integrity check post-stage (Step 5)
- `.skills/skills/connect-mcp-server/SKILL.md` · setup MCP Notion (route Step 0 L2 gate option a)
- `.skills/skills/scaffold-extension/SKILL.md` · route post-sync pour fields Notion custom non-canon

### Infrastructure scripts
- `.skills/write-to-context.py` · mutation gate canonical (mode direct pour scaffold, mode proposed pour stamp inferred fields)
- `.skills/stage-proposal.py` · checkpoint gate workflow (non utilisé Phase A · réservé checkpoints `audience_q1q4_answered` + `confirmed_products` snapshot-brand)
- `.skills/build-brand-snapshot.py` · rebuild snapshot post-mutations (silent ~50ms)
- `.skills/finalize-mutation-batch.py` · coherence check post-batch (mechanical Python primitive)

### Layer 1 MCP config
- `.mcp.json.example` · entry `notion` server Layer 1 documenté (credentials ref `NOTION_API_KEY`)

---

## Verdict

Skill `sync-notion-atlas` v2.0.1 ship le bridge Notion ↔ PhantomOS territoire-only · 10 collections territoire stride-up bidirectionnel (Phase A pull v1.0.0+ unchanged · Phase B push v2.0.0+ adjusted v2.0.1 territoire-only strict) · canvas Onday-style wrapper + 10 DBs creation pass 1 + rows population pass 2 + relations binding pass 3 (2 sub-passes B5a property add / B5b value set) + idempotency lookup par phantom_entity_id (no duplicate, no silent overwrite conflicts surfaced) · mutation gate strict pull-side · MCP Notion direct push-side · 5 sections close investigation-posture · isolation_scope brand_only · 13 hard rules canon. Phase C diff (`--mode=diff`) reste deferred v2.59+ pour resolve conflicts détectés Step B4. Production layer (creatives Full funnel Meta) routée via NEW skill dédié `sync-creatives-to-notion` v2.68+ futur. Pattern canon · 1 skill par layer.
