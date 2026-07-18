---
name: map-audiences
type: producer
version: 1.6.0
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
description: |
  v1.2.0 (v2.64 ontologie sémantique pure) · BREAKING refactor read pattern · lit pain_points + objections depuis SUB-AUDIENCE au lieu de top-level collections v2.63. Detection chevauchements Q4 (Step 1) compare pain similarity cross-audiences sémantique (le pain appartient à une audience, similarity = pattern recurrent entre audiences distinctes). Backward compat fallback top-level v2.63 + profile sub-fields v1.7.
  v1.1.0 (v2.63 ontologie pure) · BREAKING refactor read pattern · lit pain_points + objections depuis COLLECTIONS TOP-LEVEL séparées au lieu de sub-fields profile.pain_points[] / profile.objections[] legacy. Cartography 3 niveaux référence cross-audience pain_points + objections shared (un pain peut affecter mère ET sous-poche via affected_audiences[]).
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (audiences-cartography, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.0.0 (S55 · v2.58 · D#386 canon) · Atomique cartography extraction.
  Cartographie le PORTFOLIO audiences brand-wide en appliquant le framework 4 questions canon (porte d'entrée · niveau granularité · stade Schwartz · chevauchements). Scaffold N audiences mères + sous-poches via mutation gate avec validation_status hypothesis par défaut. Invocable séparément pour refresh cartographie audiences sans relancer le full snapshot. Distinct profile-audience qui drill UNE audience en deep 8 dimensions · map-audiences pose la carte brand-wide light pass.
  FR: "map-audiences {brand}", "cartographie les audiences", "split snapshot audience", "extrait les audiences mères".
  EN: "map audiences", "cartograph audiences brand", "split mother audiences".
disambiguates_against:
  - profile-audience: "profile-audience drill UNE audience en deep 8 dimensions canon V3 avec verbatims mining. map-audiences SCAFFOLD le portfolio brand-wide (N audiences mères + sous-poches) en light pass cartography (4 questions framework canon · validation_status hypothesis)."
  - snapshot-brand: "snapshot-brand est l'orchestrateur cartographie complète depuis URL (brand + products + audiences + close). map-audiences est l'atomique audiences-only invocable séparément pour refresh cartographie sans relancer le full snapshot. D#386."
  - mine-audience: "mine-audience découvre des sub-clusters candidats depuis VoC mining (signal-driven discovery). map-audiences applique le framework 4 questions canon (structure-driven scaffolding) sans verbatim density requise."
  - cartograph: "cartograph est READ-ONLY synthèse strategique cross-brand. map-audiences WRITE brand-side (scaffold audience folders + profile.json light pass)."
consumes:
  - brands/{slug}/brand.json (sector, market context, hero product)
  - brands/{slug}/audiences/*/profile.json (existing audiences pour merge/duplicate avoid)
  - brands/{slug}/audiences/*/pain_points/*.json (v2.64 ontologie sémantique pure · sub-audience canonical, owned natif par parent path)
  - brands/{slug}/audiences/*/objections/*.json (v2.64 ontologie sémantique pure · sub-audience canonical, owned natif par parent path)
  - brands/{slug}/pain_points/*.json (legacy v2.63 backward compat read fallback · top-level collection avec affected_audiences[])
  - brands/{slug}/objections/*.json (legacy v2.63 backward compat read fallback · top-level collection avec affected_audiences[])
  - brands/{slug}/products/*/spec.json (cross-ref applies_to_products binding)
  - brands/{slug}/products/*/spec.json#/mechanisms[] (mode spectre · MEC-NN, pont génératif Mc→U→A)
  - brands/{slug}/brand.json#/meta/stage (mode spectre · curseur explore/exploit stage-aware)
  - resources/schemas/profile.schema.json (target v1.7 read backward compat · v2.0 BREAKING write skip)
  - resources/canon/copy/niveaux-schwartz/* (awareness stages canon · Schwartz double-stage)
  - resources/canon/copy/archetypes-voix/* (archetypes canon · informe persona_archetype hypothesis)
  - docs/system/audience-cartography-doctrine.md (canon 3 niveaux · invariants enforcement)
  - docs/doctrine/audience-cartography-framework.md (4 questions canon)
  - path: docs/doctrine/audiences-cartography-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/system/output-clarity-doctrine.md
  - path: docs/system/operator-vocabulary-translation.md
produces_proposals_for:
  - brands/{slug}/audiences/{audience_slug}/profile.json (light pass scaffold · meta + identity light)
  - brands/{slug}/products/{slug}/spec.json#/use_cases[] (mode spectre · énumération usages génératifs, append-only)
permissions:
  reads: [brands/, resources/, docs/]
  writes: [brands/{slug}/audiences/{slug}/profile.json via write_to_context, brands/{slug}/products/{slug}/spec.json#/use_cases via write_to_context (mode spectre)]
  emits_events: [audience_cartography_proposal_created, audience_cartography_validated]
pipeline:
  preconditions:
    - "brand.json existe (sector identifié)"
    - "operator a déclenché map-audiences explicitement OR snapshot-brand orchestrateur appelle ce sub-skill"
  postconditions:
    - "N audience folders scaffold conformes profile.schema v1.7"
    - "Hierarchy 3 niveaux respect (broad → segment → micro)"
    - "validation_status hypothesis par défaut sur chaque audience"
    - "operator validation gate passed"
prerequisites:
  - field: brand.sector
    level: L1
    auto_pull: read_brand_json
    freshness_ttl_days: 90
  - field: audiences/*/profile.json
    level: L1
    auto_pull: read_existing_audiences_brownfield
    freshness_ttl_days: 90
  - field: products/*/spec.json
    level: L2
    auto_pull: read_products_for_cross_ref
    freshness_ttl_days: 90
    fallback: skip_cross_product_binding
  - field: resources/canon/copy/niveaux-schwartz
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: resources/canon/copy/archetypes-voix
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
---

# map-audiences

Atomique cartography. Cartographie le PORTFOLIO audiences brand-wide en appliquant le framework 4 questions canon. Scaffold N audiences mères + sous-poches via mutation gate, validation_status hypothesis par défaut. Permet refresh cartographie audiences sans relancer le full snapshot-brand.

Distinct profile-audience (qui drill UNE audience deep 8 dimensions avec verbatims mining). map-audiences pose la carte brand-wide light pass · framework canon respecté, pas de mine-voc requis.

## Hard Rules

### Step 0 · DRGFP prerequisite check (v2.38 canon · v1.2.0 v2.64 ontologie sémantique pure read)

Avant Step 1, scanner prerequisites :

1. **L1 silent** · `brand.json` (sector identifié) · `audiences/*/profile.json` existing brownfield · `brands/{slug}/audiences/*/pain_points/*.json` (v2.64 sub-audience) · `brands/{slug}/audiences/*/objections/*.json` (v2.64 sub-audience) · canon `niveaux-schwartz` + `archetypes-voix` · doctrine `audience-cartography-doctrine.md` + `audience-cartography-framework.md`
2. **L2 cross-ref** · `products/*/spec.json` pour binding `applies_to_products[]` · fallback skip si absent (audience brand-wide acceptable)
3. **L3 gate operator** · si brand.json absent OR sector vide → refuse + reco `snapshot-brand` d'abord pour poser la base brand

**Read pattern pain_points + objections v1.2.0 (v2.64 ontologie sémantique pure)** ·

Pour identifier overlap pain_points + objections cousins inter-audiences candidates (Q4 cartography Step 1), scan désormais sub-audience direct par audience candidate ·

- Scan `brands/{slug}/audiences/*/pain_points/*.json` → audience parent_slug implicite via path → mapping audience_slug → [pain_ids owned]
- Scan `brands/{slug}/audiences/*/objections/*.json` → idem → mapping audience_slug → [objection_ids owned]
- Backward compat fallback v2.63 · si sub-audience vides OR absent, fallback top-level `brands/{slug}/pain_points/*.json` + `brands/{slug}/objections/*.json` filtré par `affected_audiences[]` contains slug
- Backward compat fallback v1.7 · si top-level vide aussi, fallback `audiences/{slug}/profile.json#/pain_points[]` + `profile.json#/objections[]` legacy brownfield

Owned natif sub-audience · un pain `PNT-12` dans `brands/{slug}/audiences/audience_A/pain_points/` appartient à audience_A. Si pattern similaire détecté dans audience_B (pain `PNT-NN` distinct mais semantically close), c'est un signal chevauchement (Q4) à surface · audiences cousines via pain shape, pas via reference partagée.

Output state map + confidence_chain[] init.

Cross-ref doctrine · `docs/system/dependency-resolution-protocol.md`.

### Step 0bis · Détection du mode (normal vs spectre)

map-audiences a deux modes. **Mode normal** (défaut, comportement v1.3.x strictement inchangé) · cartographie le portfolio d'audiences via les 4 questions. **Mode spectre** · s'active si le skill est invoqué avec le flag mode spectre (par `build-atlas-complete` palier spectre, par `/phantom {brand} spectre`, ou sur demande opérateur explicite « cartographie le terrain / le spectre des usages »). En mode spectre, le skill exécute d'abord **F1** (énumération des usages depuis le mécanisme) puis applique le framework **par usage** (**F2**), avec les deltas ci-dessous.

**Précondition mode spectre · `spec.mechanisms[]` non vide** (le pont génératif Mc→U a besoin du mécanisme). Si vide → **invoquer `map-mechanisms` d'abord** (inline OU déjà fait par l'orchestrateur build-atlas Step 2.5 sous-bloc A), PAS seulement « recommander » · sans mécanisme, F1 n'a pas d'amont et la chaîne meurt. JAMAIS inventer d'usages.

**Précondition d'écriture (gate `confirmed_products`)** · le write sur `products/{slug}/spec.json` est gaté par le checkpoint `confirmed_products` (write-to-context). Dans le flux build-atlas, c'est résolu (le produit est confirmé au Gate Intermédiaire 1). En invocation STANDALONE (`/phantom {brand} spectre` sur une marque brownfield), si le produit n'est pas dans `confirmed_products` → le write `die()`. Dans ce cas, lancer `stage-proposal confirmed_products --product-slug {slug}` d'abord, ne pas retry à l'identique.

### Mode spectre · F1 énumération des usages, F2 audiences par usage

(s'exécute uniquement en mode spectre, en amont et autour de Step 1)

**F1 · Énumérer les usages depuis le mécanisme (Mc → U).** Lire `spec.mechanisms[].mechanism_id` + `spec.problems_solved[]` + seed optionnel `specs.target_suitability.use_cases[]` (qui SEED, ne remplace pas le nœud stratégique). Énumérer génétiquement TOUS les jobs que le mécanisme peut servir, y compris adjacents et non-évidents (c'est là que naissent les marchés non vus). Trois statuts :
- **evident** · déjà servi/communiqué par la marque
- **adjacent** · même mécanisme, autre situation ou audience
- **speculative** · marché non vu, hypothèse à qualifier · reste hypothèse tant que rien ne la confirme, JAMAIS asserté comme fait (D#503)

**Garde-fou anti-sous-exploration (D#514).** F1 ne s'arrête PAS aux usages évidents. Un F1 qui ne sort que des `evident` (1:1 avec les audiences déjà visibles sur le site) n'a PAS exploré · générer au moins 2-3 usages `adjacent`/`speculative`, les non-évidents qu'un scan des avis ne contiendrait jamais (un moment d'usage daté · le segment que la marque ne sert pas encore · périménopause, axe intestin-cerveau, le moment précis de la journée). Le tier `speculative` EST le livrable de valeur · sans lui, la dérivation d'audiences (F2) retombe sur les tiers évidents du même acheteur in-market. Observé au run onday · 4 use_cases tous evident/adjacent, zéro speculative → les audiences non servies jamais sorties, retour au quasi-miroir. Un `spec.use_cases[]` sans aucun `speculative` est un signal d'exploration avortée · garde-fou mécanique correspondant (D#518) · la postcondition orchestrateur `build-atlas-complete` inspecte l'artefact écrit (use_cases avec ≥1 speculative + `spectrum.json` existe) quelle que soit la porte qui l'a produit, et `resources/scripts/validate-all.py` flague post-hoc (`use_cases_no_speculative`) un array sans speculative.

Écrire chaque usage dans `spec.use_cases[]`. **Clés EXACTES** (`use_case_id` est `required`, ne pas le deviner) ·
```json
{"use_case_id":"UC-NN","label":"{le job côté client}","mechanism_refs":["MEC-NN"],"mechanism_hint":"{texte libre SI le mécanisme n'est pas encore en MEC-NN · jamais inventer un MEC-NN}","status":"evident|adjacent|speculative","_source":"observed|inferred|declared"}
```
**Mécanique d'écriture** · `use_cases[]` est un array, donc `write_to_context` refuse `--mode proposed` sur un array · écrire élément par élément en `--mode direct` avec `--path "brands/{slug}/products/{p}/spec.json#/use_cases/-"` (le `/-` append en fin d'array). Le `_source` de l'usage (dans la valeur) est distinct de l'arg `--source` du writer.

**F2 · Dériver les audiences PAR usage (U → A).** Pour chaque usage de F1, appliquer le framework 4 questions de Step 1 scopé à CET usage, avec ces deltas vs le mode normal :
- `meta.audience_type: probe` (sonde, pas audience opérable · promue à 5 verbatims, cf C1) · `validation_status: hypothesis`
- **motivation OBLIGATOIRE** (situation déclenchante, tension, alternative rejetée) · démographie dérivée optionnelle
- `meta.primary_splitting_axis = use_case` forcé par construction (le Q5 est tranché d'office)
- Q1 `entry_door` reste requis (Invariant 5)
- **stage-aware** (lit `brand.json#/meta/stage`) · `launch` → quota d'usages adjacent/speculative relevé (exploration dominante, carte au crayon assumée) · `scale`/`mature` → evident d'abord

Le plafond de 5 audiences est relâché **en mode spectre uniquement** (la carte est exhaustive et gratuite, D#502) · il reste intact en mode normal et pour la production aval.

### Step 1 · Application framework 4 questions canon

Le skill applique strictement les 4 questions canon (`docs/doctrine/audience-cartography-framework.md`) en mode batch (toutes les audiences cartographiées en une passe, pas une par une comme `profile-audience`).

#### Q1 · Porte d'entrée par audience identifiée

Pour chaque audience mère candidate, déterminer la porte d'entrée dominante via enum strict :

- **`pain_driven`** · entre par un problème ressenti (ex chute capillaire, ballonnement, fatigue)
- **`goal_driven`** · entre par une ambition projet (ex longueur cheveux pour mariage, perte 5kg avant été, summer body)
- **`identity_driven`** · entre par qui elle est ou veut être (ex hijabi qui préserve les edges, sportive endurance, jeune maman naturelle)

Hard rule canon · **1 porte dominante par audience**. Si 3 portes égales détectées sur une candidate → flag piège 2 (audience-redondante mal séparée), proposer re-découpage.

Persister dans `meta.entry_door` enum.

#### Q2 · Niveau granularité (3 niveaux MECE max)

Hiérarchie cap à `broad → segment → micro`. Cardinalité canon :

| Niveau | Volume estimé | Cardinalité par brand |
|---|---|---|
| broad | 500k+ actives | 1-3 max |
| segment | 100-500k actives | 5-15 par broad |
| micro | 20-100k actives | 0-3 par segment, optionnel |

Inférer scope depuis sector brand + description candidate. Persister `meta.scope` + `meta.parent_slug`.

Hard rule canon · **descendre d'un niveau requiert 3/3** (volume restant suffisant + pitch divergent + offer divergent). Si 0/3 ou 1/3 sur une candidate micro → refuse + reclasse en variation copy (pas sous-audience).

#### Q3 · Stade Schwartz (light pass · pas de mining)

map-audiences est **light pass** · ne mine pas, ne pose pas le stade Schwartz par audience comme `profile-audience` (qui requiert verbatim density). Mention canon awareness stages disponibles pour orientation downstream :

```
product-awareness · unaware → problem → solution → product → most-aware
emotional-maturity · niant → résigné → en recherche → combatif → acceptant
```

Note pour Layer A trace · la DISTRIBUTION chiffrée de conscience par audience (mesurée) est assignée en deep pass par `profile-audience` quand le mining verbatim a tourné. MAIS le stade DOMINANT se POSE en hypothèse dès le scaffold (D#519) depuis la maturité catégorie (`market_position.awareness_dominant`) · ça se dérive du marché sans verbatim. Seule la distribution chiffrée `psychology.awareness_stage_*` reste null en light pass.

#### Q4 · Chevauchements cousins (v1.2.0 v2.64 ontologie sémantique pure · cross-audience semantic similarity)

Scan pairwise des audiences cartographiées pour détecter chevauchements.

**v2.64 ontologie sémantique pure · detection chevauchements via semantic similarity sub-audience** ·

1. Pour chaque pair (audience_A, audience_B), scan `brands/{slug}/audiences/audience_A/pain_points/*.json` + `audiences/audience_B/pain_points/*.json` → semantic similarity comparison sur `formulation` + `chain[]` text + `pain_category` enum
2. Idem `audiences/audience_A/objections/*.json` + `audiences/audience_B/objections/*.json` → semantic similarity comparison sur `formulation` + `type` enum
3. Si similarity threshold ≥ 0.6 sur 1+ pain pair OR 1+ objection pair → flag chevauchement entre audience_A et audience_B (semantic pattern cousiné, pas reference partagée)
4. Backup fallback v2.63 · scan top-level `pain_points/*.json` + `objections/*.json` filter par `affected_audiences[]` contains BOTH audiences → flag shared (legacy behavior)
5. Backup fallback v1.7 · heuristic semantic similarity sur pain dominant inféré + identity signals (legacy brownfield)

Ontologie sémantique pure · le pain owned par audience_A est DISTINCT du pain owned par audience_B même si semantically similar. La similarité reveal le pattern cousiné cross-audiences, pas une réutilisation d'entité (chaque audience a sa propre encoded matière).

Surface 1-3 paires cousines détectées par audience candidate, avec liste des pain semantic matches comme indicateurs explicites.

Persister `meta.overlap_with[]` array slugs sur chaque audience scaffold.

Note pédagogique canon · les chevauchements ne disqualifient pas l'audience · ils révèlent les angles porteurs cousinés (cross-pollinisation copy). Pattern v2.64 · chaque audience encode son matériel propre, le chevauchement est observé via similarity, pas via partage d'entité. Operator-facing · dire "audiences cousines", jamais "overlap_with" brut.

#### Q5 · Axes primaires de découpage MECE explicit (v2.87.6 NEW gate)

**Gate canon obligatoire si Q2 niveau granularité = 2 ou 3 (sub-audiences scaffold détecté · 2+ sous-poches mère même produit).** Skip si Q2 = 1 (audience plate sans sub-poches).

**Pourquoi cette gate.** Audit Fincut session v2.87.3 finding · Q1-Q4 scaffolde des sub-audiences sans avoir clarifié AVEC l'opérateur l'axe primaire de splitting. Résultat · 3 sous-poches `audience_mère_A` peuvent être splittées implicitement par démographie alors que la vraie variable dominante en paid est use_case OR canal OR trigger temporel. La sub-audience structurée sur le mauvais axe primaire produit des angles plats même si le scaffold passe les tests semantic Q1-Q4.

**Question pivotale opérateur (rendre via `AskUserQuestion` 6 options canon MECE)** ·

| Axe primaire | Définition opérateur-facing |
|---|---|
| `use_case` | Quelle situation déclenche l'achat ? (e.g. workers shift 8h vs grand-parents marche jardin pour Stepprs) |
| `demographie` | Quel segment socio-démographique ? (e.g. femmes 45-60 vs hommes 25-35 · âge dominant · CSP · genre) |
| `canal` | Sur quelle plateforme se trouvent-ils ? (e.g. Meta vs TikTok vs Search · pas pareil intent) |
| `awareness_stage` | Quel niveau de conscience du problème ? (unaware · problem_aware · solution_aware · product_aware · most_aware · Schwartz 5 stades) |
| `sophistication` | Quel niveau de saturation du marché vu par l'audience ? (Stage 1-5 Schwartz · de "première offre" à "tous les angles éculés") |
| `trigger_temporel` | Quel moment déclenche le besoin ? (matin · fin de shift · post-grossesse · saison · cycle de vie) |

**Pattern de raisonnement agent** · proposer en priorité l'axe primaire qui maximise la variance copy entre sub-audiences (cf brand cas pédagogique Stepprs · `use_case` est l'axe primaire dominant cf `workers-shifts` vs `chronic-pain-45` · variance copy énorme entre "tiens ton shift sans douleur" et "garde tes petits-enfants au parc"). Les autres axes restent valid mais comme horizontales partagées (e.g. `chronic-pain-45` peut avoir sub-poches par `awareness_stage` plantar_fasciitis_diagnosed vs heel_pain_general · axe secondaire).

**Test runtime cas concret obligatoire AVANT scaffold sub-audiences** · l'agent doit articuler pour 2 sub-audiences pressenties · "si je split sur axe X, voici les 2 hooks copy distincts qui en sortent · si je split sur axe Y, voici les 2 hooks distincts qui en sortent." Comparer side-by-side. L'axe qui produit la plus grande divergence copy = l'axe primaire canonique pour cette brand × produit.

**Persister `meta.primary_splitting_axis = "use_case" | "demographie" | "canal" | "awareness_stage" | "sophistication" | "trigger_temporel"`** sur la mère audience scaffold (Step 2) · permet aux skills aval (compose-creative · produce-paid-matrix) de respecter l'axe primaire pour la composition many-to-many.

**Anti-pattern banned** · scaffolder 2+ sub-poches sans Q5 explicit · canon v2.87.6 refuse write_to_context si `primary_splitting_axis` absent dans `meta` sub-audience (enforcement runtime backlog v2.88.0+ · v2.87.6 patch_notes déclaratif).

### Step 2 · Scaffold audience folders + profile.json light pass

Pour chaque audience mère identifiée Step 1, scaffold via mutation gate :

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/profile.json#/meta/name" --value "{audience_name}" --source agent --confidence 0.6 --mode proposed --reason "map-audiences scaffold light pass"
```

Champs scaffold light pass (rest stay null jusqu'à `profile-audience` deep drill OR `mine-voc` enrich) :

```
meta.name              → human-readable label (e.g. "Femmes 30-45 chute post-grossesse")
meta.slug              → kebab-case slug
meta.scope             → broad | segment | micro
meta.parent_slug       → null pour broad mère, slug-of-mother pour sub
meta.entry_door        → pain_driven | goal_driven | identity_driven (Q1 canon)
meta.overlap_with      → array slugs cousines (Q4 canon)
meta.validation_status → "hypothesis" par défaut
meta.audience_type     → "primary" | "secondary" | "discovered" | "assumed"
meta.applies_to_products → array product slugs si cross-product check Step 3 trigger
meta.tags              → namespace-prefixed tags depuis sector brand (e.g. "problem:hair-loss", "context:post-pregnancy")
identity.description   → 1-line description audience (inférée depuis sector + market context brand.json)
identity.gender        → male | female | all (only si explicit brand.json target · démo DÉRIVÉE, jamais le nœud primaire)
identity.age_range     → {min, max} (only si explicit brand.json target audience · idem, optionnel)
```

**Plancher expert par nœud (D#519 · motivation-first, dérivable du mécanisme SANS verbatim).** Le scaffold light pass NE se limite PAS à `meta` + `identity` (un nœud démographique plat = la régression onday). Il POSE EN HYPOTHÈSE (confiance faible, `validation_status: hypothesis`, flaggé) les champs experts que le mécanisme + la catégorie suffisent à dériver, AVANT tout mining ·

```
psychology.jtbd.primary            → le JOB (motivation d'abord) dérivé du use_case servi · jamais une démo
psychology.jtbd.context            → la situation déclenchante + l'alternative rejetée (le contexte du job)
decision_process.awareness_trigger → le moment/déclencheur qui ouvre le besoin
market_position.awareness_dominant → le stade de conscience DOMINANT posé en hypothèse depuis la maturité catégorie (la distribution chiffrée reste null)
```

Un nœud sans `jtbd.primary` + `entry_door` + `awareness_trigger` + `awareness_dominant` est SOUS le plancher doctrine (`docs/doctrine/audiences-cartography-doctrine.md` principes 1-2) · ce sont des hypothèses DÉRIVÉES, pas du VoC, donc « pas encore la voix client » ne les excuse pas.

**Restent déférés** (ceux-là exigent vraiment du VoC) · `pain_points[]`, `voice.key_expressions[]`, `objections[]`, `benefits[]` appartiennent à `profile-audience` + `mine-voc`. Jamais null EN BLOC pour autant · poser les hypothèses experts ci-dessus.

**Règle dure (D#519 · le profil porte le raisonnement, pas le template).** NE JAMAIS écrire un `profile.json` dont `meta.slug` reste `example-audience` / `meta.name` reste `Example Audience` dans un dossier non-`_example`. Sur un write gated/pausé, FLUSHER `.workflow.json#pending.summary` (le raisonnement validé, gelé dans le buffer du gate) dans le light pass AVANT de rendre la main · sinon le raisonnement narré reste piégé dans le pending et l'artefact reste un template vide (observé run onday · `actifs-fatigue` octet-pour-octet le template). Filet post-hoc · `audience_profile_template_clone` dans `resources/scripts/validate-all.py`.

### Step 3 · Cross-link audiences ↔ products

Si `brands/{slug}/products/` contient des spec.json, scan pairwise audiences ↔ products via :

- `spec.problems_solved[]` pain match contre Q1 entry_door inféré
- `spec.applies_to_audiences[]` reverse-ref si déjà encodé
- Sector brand cross-ref hero product

Pour chaque audience candidate :
- Single product match → `meta.applies_to_products: ["product_slug"]`
- Multi-product match (cross-product) → `meta.applies_to_products: ["p1", "p2"]`
- No clear match OR brand-wide audience → `meta.applies_to_products: []` (brand-wide)

Hard rule canon · `meta.applies_to_products: []` (vide) est valide (brand-wide audience). Jamais default `[hero_product_slug]` silencieusement · respecter le binding explicite décidé Step 1.

Stage chaque `applies_to_products` via mutation gate :

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/profile.json#/meta/applies_to_products" --value '["product_slug"]' --source agent --confidence 0.7 --mode proposed --reason "map-audiences cross-product binding from spec.problems_solved match"
```

### Step 4 · Hierarchy enforcement canon doctrine

Avant write final, validate hierarchy canon (`docs/system/audience-cartography-doctrine.md`) :

1. **Invariant 1** · 3 niveaux max (broad → segment → micro). Refuse niveau 4+.
2. **Invariant 2** · Pas d'orphelin segment. Segment sans `parent_slug` → flag MAJOR.
3. **Invariant 3** · Pas de cycle overlap. A↔B valide (symétrie), A→B→C→A interdit (flag MAJOR).
4. **Invariant 4** · Test 3/3 sur micro (volume + pitch divergent + offer divergent). Si 0/3 ou 1/3 → reclasse en variation copy.
5. **Invariant 5** · Porte d'entrée explicite. `meta.entry_door` requis sur chaque audience scaffold.

Si invariant violé → revise cartographie Step 1 avant Step 2 write. Pas de scaffold sur cartography incohérente.

### Step 5 · Output operator-facing 5 sections investigation-posture

**Doctrinal contract canon.** map-audiences produit une synthèse strategique cartographie · structure obligatoire en 5 sections explicites (`docs/system/investigation-posture.md`).

#### Section 1 · Observé (faits sourcés)

Ce qui a été lu de brand.json + products spec + audiences existing :

```
Observé · cartographie depuis matière brand encodée (run {date}, {duration})

- Sector brand : {sector_slug} ({source brand.json#sector})
- Hero product : {hero_slug} ({source brand.json#hero_product OR products/*/spec.json#identity.primary})
- Audiences existing : {N existing} ({slugs · status validation_status})
- Products bindings : {N products} ({slugs avec applies_to scope inféré})
- Sector market context : {market.maturity OR market.sophistication si encodé brand.json}
```

Hard rule · faits sourcés uniquement avec ref. Pas d'hypothèse en Section 1.

#### Section 2 · Déduit (hypothèses cartographie avec confidence)

Cartographie N audiences mères + sous-poches identifiées en hypothèse :

```
Déduit · N audiences cartographiées en hypothèses

{Audience_1_label} (broad · pain_driven)
  Confidence : {forte | moyenne | faible · si verbatim_density existing OR uniquement inféré depuis sector}
  Indicateurs sources : {ce qui justifie · sector match + market context + competitor reference OR brand.target explicit}
  Sous-poches identifiées : {2-3 segments si Schwartz sub-cluster pertinent}
  Cross-product : {applies_to inférée OR brand-wide}

{Audience_2_label} (broad · goal_driven)
  ...

{Sous-poche_1A_label} (segment · sous {Audience_1})
  ...
```

Hard rule · audiences présentées comme HYPOTHÈSES (validation_status hypothesis par défaut). Anti-pattern AP-2 doctrine BANNI · personas inventés présentés comme analytiques sans data verbatim.

#### Section 3 · Inconnu (variables à mining-confirm)

Variables non observables sans mining verbatim :

```
Inconnu · variables à creuser pour passer hypothèse → validée

- Vrais pain_points par audience (mining verbatim Trustpilot + forums niche requis)
- Vraies expressions clientes par audience (vocabulary natif client vs ce que la brand projette)
- Schwartz stage dominant par audience (product-awareness + emotional-maturity)
- Objections récurrentes par audience (severity + frequency réelle)
- Vraies overlap cousines vs hypothèses overlap (sample verbatim cross-audience match)
- Volume estimate restant par segment (data analytics audience requise)
```

#### Section 4 · Leviers (drill-down options)

Skills + actions pour lever les inconnues :

```
Leviers · 4 axes prioritaires post-cartographie

Axe A · Drill UNE audience deep 8 dimensions (mining verbatim + synthesis canon V3)
  → écoute clients structurée sur Trustpilot + forums niche sur {audience_X}
  → ~8-12 min mining + synthesis 8 dimensions canon
  
Axe B · Sortir un set d'angles ranked sur UNE audience cartographiée
  → ideation angles paid avec confidence chain hérité audience source
  → requiert Axe A d'abord pour confidence forte
  
Axe C · Ingest matière founder/brand existante (PDF brief, deck, sources VoC exportées)
  → upgrade confidence cartographie sans nouvelle mining ronde
  → 1-2 phrases denses opérateur OR drop fichier upload
  
Axe D · Refresh cartographie audiences sur changement scope brand
  → re-run map-audiences si nouveau produit ajouté, nouveau marché, pivot positioning
```

#### Section 5 · Close ouvert (UNE question macro)

Anti-pattern AP-5 doctrine BANNI · close affirmatif qui ferme la conversation. Toujours close ouvert drill-down macro · UNE question · opérateur arbitre.

Format close canonique :

> Pour passer ces {N} audiences de hypothèse à validée terrain et débloquer la suite (angles paid, brief créa) avec une fondation sourcée ·
>
> A · Drill UNE audience deep (~8-12 min écoute clients + synthesis 8 dimensions). Recommandé sur l'audience prioritaire identifiée · {audience_top_label}.
> B · Garde toutes les audiences en hypothèse et lance les angles directement · downstream porte la confidence `hypothèse` héritée (à tester budget calibré, pas all-in).
> C · Tu m'injectes données existantes (reviews exportées, analytics audience, retours SAV, brief founder) en 1-2 phrases denses ou drop fichier · je re-évalue cartographie avec matière fraîche.
>
> Mon avis · {reco macro adaptive · si N audiences > 5 et zéro verbatim existing → A critique sur l'audience hero · si audiences existing déjà mining-sourced partiel → B valide direct}.

L'opérateur arbitre · l'agent enchaîne le drill-down sur l'axe choisi (silencieusement vers `profile-audience` OR `produce-paid-angles` OR `ingest-resource` selon choix).

### Step 6 · Persist via mutation gate

Une fois validation operator passée, `write_to_context` chaque champ scaffold (Steps 2-3) sur `brands/{slug}/audiences/{a_slug}/profile.json` :

```bash
python3 .skills/write-to-context.py --path "audiences/{a_slug}/profile.json#/meta" --value '{...}' --source agent --confidence 0.6 --mode proposed --reason "map-audiences light pass scaffold"
```

Conformité `profile.schema v1.7` obligatoire. `validation_status: hypothesis` par défaut sur chaque audience.

### Step 7 · Finalize mutation batch

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mécanique. Inspecte mutations Step 6, runs structural checks, emit `audience_cartography_validated` event pour turn-end-audit.

Exit code 2 = blocking issue → revise avant ship. Exit code 0 warnings = log, ship.

### Step 8 · Déposer le beat de restitution des audiences (D#520)

L'arbre est POSÉ (audiences mères + sous-poches écrites, `entry_door` + `jtbd.primary` + `awareness_trigger` + `awareness_dominant` remplis au plancher D#519, batch finalisé). Avant de rendre la main, dépose le registre de CE QUE TU VIENS DE TRANCHER pendant que ton contexte est frais. Doctrine SSOT · `docs/system/restitution-beat-doctrine.md` (contrat payload, règles décision-d'abord, richesse second-ordre, temporalité + mode, table phase→vue + phase→forward-look). NE résume PAS l'arbre en une phrase · tu déposes le beat, le code le rend (anti double-compression · le raisonnement meurt quand on le compresse ici puis qu'on demande au fil de le re-broder).

Écris (`Write` · c'est sous `.phantom/`, hors `brands/`, donc hors gate mutation · ne passe PAS par `write-to-context`) le fichier `.phantom/beats/{slug}/audiences.json` :

```bash
Write → .phantom/beats/{slug}/audiences.json
```

**Params de cette phase** (le reste du contrat vit dans la doctrine, ne le re-duplique pas) ·
- `phase` · `"audiences"`
- vue rendue par le code · `/phantom {slug} audiences` (le renderer l'appose paste-ready · ne mets PAS de chemin dans `tease`)
- forward-look apposé par le code · « je croise mécanisme et audiences en carte de marché (le spectre) »

**Le contenu, calibré audiences** (richesse = le second ordre, cf doctrine règle 2) ·
- `verdict` · la lecture tranchée de l'arbre, une ligne · QUELLE mère est le vrai wedge (celle qui porte l'éco), laquelle reste hypothèse. Pas « N audiences posées ».
- `read` · le second ordre · POURQUOI cette mère porte (la porte d'entrée × le job × la maturité catégorie qui la rend activable maintenant), et ce que la poche spéculative OUVRE (le segment non servi que le mécanisme atteint mais que les avis ne nomment jamais · le lane que personne n'occupe encore).
- `analyzed` / `found` · les déductions saillantes par mère (entry_door dominante, axe de découpage retenu et pourquoi il maximise la variance copy, chevauchements cousins révélés) · amorce grasse possible.
- `rejected` · les découpages écartés avec leur raison (axe démographie écarté au profit de l'usage, micro reclassé en variation copy faute de 3/3) · le rejet est le travail le plus défendable.
- `encoded` · les artefacts posés · N mères + M sous-poches, plancher expert hypothèse par nœud.
- `confidence` · la confiance AVEC sa cause · les audiences à confiance faible nomment leur cause ET l'étape qui les lèvera (« hypothèse dérivée du mécanisme, pas encore de voix client · la voix-client la tranchera »). La confiance forte vit dans le verdict, on ne la liste pas seule.
- `basis` · la largeur · combien d'audiences, sourcées comment (sector + market context brand.json + usages du mécanisme · zéro verbatim à ce stade, c'est assumé).
- `tease` · la valeur DANS la vue audiences · ce que l'opérateur va voir de tranché ou d'inattendu (l'arbre mère/poches, le wedge éco lisible d'un coup d'œil) · une invitation, pas un chemin.

Champ vide = omis, jamais inventé. Le renderer réorganise en décision-d'abord (verdict + read, le raisonnement qui flue, puis « Ce sur quoi je reste prudent » avec la cause, puis « Lu · », puis le CTA `/phantom`), tu déposes les champs.

### Step 9 · Émettre le beat (standalone uniquement · réutilise le signal de mode)

Même signal orchestré-vs-standalone que Step 0bis (mode spectre) · invoqué par `build-atlas-complete` (palier Phase 3) = ORCHESTRÉ · invoqué par l'opérateur seul ou via `/phantom {slug}` = STANDALONE.

- **Orchestré** · NE rends rien · tu as déposé le payload, c'est l'orchestrateur qui émet le beat (il exécute `render-beat.py --phase audiences` quand map-audiences lui rend la main, présente la sortie telle quelle, et relie vers le Gate 2). Tu rends juste la main.
- **Standalone** · émets toi-même le beat · `python3 .skills/render-beat.py --brand {slug} --phase audiences --mode standalone` et présente sa sortie TELLE QUELLE (NE re-narre pas, NE re-résume pas). En standalone le renderer propose la suite (« Prochaine étape · je croise mécanisme et audiences en carte de marché. Je lance ? ») · la proactivité vient de là.

**Filet** · si `render-beat` rend du vide (payload absent), retombe sur la synthèse Step 5 (5 sections investigation-posture) en prose · ne laisse JAMAIS un trou à la place de la phase. Le hook `beat-emit` rappelle mécaniquement un payload frais non-émis.

## Hard rules globales

- **Doctrine audience-cartography 3 niveaux respect** · jamais niveau 4+. Invariant 1 canon enforce.
- **validation_status hypothesis par défaut** · sur chaque audience scaffold light pass. Upgrade à `validated` uniquement post-mining verbatim (responsabilité `profile-audience` OR `mine-voc`).
- **Backward compat strict** · existing audiences brownfield (read en Step 0 prerequisite) jamais écrasées. Merge strategy · skip si entry existing + validation_status >= validated. Append si entry nouvelle. Flag conflict si entry existing + validation_status hypothesis (operator arbitre).
- **JAMAIS halluciner une audience sans justification sector + market context** · Section 1 Observé sourced obligatoire avant Section 2 Déduit hypothèse.
- **JAMAIS exposer `validation_status: hypothesis`, `meta.parent_slug`, `meta.entry_door` bruts** en surface operator. Reformuler en langage métier (porte d'entrée, audience mère, hypothèse à valider).
- **JAMAIS nommer skill** (`mine-voc`, `profile-audience`, `produce-paid-angles`) en surface operator. Routing silencieux post-arbitrage opérateur.
- **JAMAIS scaffold audience folder si Section 1 Observé vide AND operator skip Q1** · refuse write, surface gap, suggest `snapshot-brand` d'abord OR ingest brief operator.
- **Cap 5 audiences max scaffold par run** · au-delà, dilue cartographie et viole Pareto canon (80% revenue brand = 2-3 audiences activées). Surface flag si >5 candidates détectées, suggest priorisation operator. **SAUF mode spectre** · la carte est exhaustive et gratuite (D#502), le cap est relâché · il reste intact en mode normal ET pour les artefacts opérables (la production aval garde le Pareto).
- **DRGFP L3 gate strict** · brand.json absent OR sector vide → refuse + reco `snapshot-brand`. Pas de freestyle cartography sans base brand encodée.

## Anti-patterns

- **AP-1** · scaffold audience folder sans `meta.entry_door` (viole Invariant 5 canon).
- **AP-2** · présenter audiences comme analytiques sans flag hypothèse (anti-pattern doctrine investigation-posture).
- **AP-3** · cartography flat sans hiérarchie broad → segment → micro (viole Movement 3 audience-cartography canon).
- **AP-4** · niveau 4+ subdivisé (sous-micro) · viole Invariant 1 canon doctrine.
- **AP-5** · close affirmatif post-cartographie (*"audiences saved, what next?"*) · banni canon investigation-posture.
- **AP-6** · default `applies_to_products: [hero_slug]` silencieusement · audience brand-wide doit rester `[]` explicite.
- **AP-7** · scaffold sur cartographie incohérente (Invariants 1-5 violés) sans revise Step 1.
- **AP-8** · drill 8 dimensions par audience en map-audiences (overlap profile-audience scope) · light pass uniquement, deep dimensions delegated.

## Operator output template canonique

```
{BRAND} · CARTOGRAPHIE AUDIENCES ({N} hypothèses)

─────────────────────────────────────────────

Observé · matière brand lue (run {date}, {duration})

  Sector             {sector_slug}
  Hero product       {hero_slug}
  Audiences existing {N existing · statuts}
  Products bindings  {N products · cross-ref scope}
  Market context     {maturity OR sophistication encodée}

─────────────────────────────────────────────

Déduit · {N audiences} hypothèses cartographiées

  [1] {Audience_1_label} (audience mère · porte pain_driven)
    Confidence       {forte | moyenne | faible}
    Indicateurs      {ce qui justifie · sector + market context + brand.target}
    Sous-poches      {N segments · labels}
    Cross-product    {applies_to inféré OR brand-wide}
    Audiences cousines {N overlap_with détectées}

  [2] {Audience_2_label} (audience mère · porte goal_driven)
    ...

  [1A] {Sous-poche_1A_label} (segment · sous {Audience_1})
    Confidence       {moyenne}
    Justification    {pitch + offer divergents OR pas)
    Indicateurs      {ce qui justifie split}

─────────────────────────────────────────────

Inconnu · variables à creuser pour passer hypothèse → validée

  - Vrais pain_points par audience (mining requise)
  - Vraies expressions clientes par audience
  - Schwartz stage dominant par audience
  - Objections récurrentes par audience
  - Vraies overlap cousines vs hypothèses overlap
  - Volume estimate restant par segment

─────────────────────────────────────────────

Leviers · 4 axes drill-down post-cartographie

  Axe A · Drill UNE audience deep 8 dimensions
  Axe B · Sortir set angles ranked sur UNE audience cartographiée
  Axe C · Ingest matière founder/brand existante
  Axe D · Refresh cartographie sur changement scope brand

─────────────────────────────────────────────

Close · UNE question macro drill-down

Pour passer ces {N} audiences de hypothèse à validée terrain et débloquer la suite ·

A · Drill UNE audience deep (~8-12 min écoute clients + synthesis 8 dimensions). Reco sur audience prioritaire · {audience_top_label}.
B · Garde toutes en hypothèse et lance les angles directement · downstream porte confidence héritée.
C · Tu m'injectes données existantes (reviews, analytics, brief founder) · je re-évalue avec matière fraîche.

Mon avis · {reco macro adaptive selon état corpus existing}.
```

## Cross-references

- `docs/system/investigation-posture.md` · doctrine canon 5 sections obligatoires (Observé · Déduit · Inconnu · Leviers · Close ouvert)
- `docs/system/audience-cartography.md` · doctrinal contract Movement 3 cartography (mère / sous-audiences)
- `docs/system/audience-cartography-doctrine.md` · spec rigoureuse système-side · 5 invariants enforcement
- `docs/doctrine/audience-cartography-framework.md` · 4 questions canon framework operator-facing
- `resources/schemas/profile.schema.json` (v1.7) · target schema scaffold
- `resources/canon/copy/niveaux-schwartz/*` · awareness stages canon (Schwartz double-stage référence note)
- `resources/canon/copy/archetypes-voix/*` · archetypes canon (informe persona_archetype hypothesis)
- `.skills/skills/profile-audience/SKILL.md` · drill UNE audience deep 8 dimensions (downstream consumer)
- `.skills/skills/mine-voc/SKILL.md` · enrich audience verbatim post-cartographie
- `.skills/skills/produce-paid-angles/SKILL.md` · consume audiences cartographiées (downstream consumer)
- `.skills/skills/snapshot-brand/SKILL.md` · orchestrateur cartographie complète (parent caller D#386)
- D#386 · décision canon · architecture cartographie marketing (snapshot-brand orchestrateur + sub-skills map-X invocables séparément)
