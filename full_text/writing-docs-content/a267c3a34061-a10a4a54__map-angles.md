---
name: map-angles
type: producer
version: 1.1.0
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
subagent_safe: true
mode: proposed
operator_facing: true
archetype_canon_id_enum:
  - innocent
  - sage
  - explorer
  - rebelle
  - magician
  - heros
  - amante
  - jester
  - homme-ordinaire
  - caregiver
  - ruler
  - creator
description: |
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, breakthrough-advertising-5-stages, audiences-cartography). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.0.0 (S55 · v2.58 · D#386 canon) · Atomique cartography extraction.
  Cartographie le PORTFOLIO angles brand-wide depuis audiences cartographiées · scaffold N angles ANG-NN.json light pass (formula 4 components + lineage canon obligatoire) sans deep production matrix scoring. Invocable séparément pour refresh cartographie angles sans relancer le full pipeline produce-paid-angles. Distinct produce-paid-angles qui scoring + ranks + close drill-down matrix · map-angles scaffold le PORTFOLIO depuis cross-product audience × axis origin (audience-derived · product-derived · category-derived · brand-derived · temporal-cultural).
  FR: "map-angles {brand}", "cartographie les angles", "extrait les angles brand-wide", "refresh angles brand".
  EN: "map angles", "cartograph angles brand-wide", "refresh angles".
disambiguates_against:
  - produce-paid-angles: "produce-paid-angles scoring + ranks 5-7 angles top sur UNE audience avec matrice 5-lens framework + close drill-down deep production. map-angles SCAFFOLD le portfolio angles brand-wide light pass (cross-product audience × origin_axis) sans scoring numérique exposé. Refresh cartographie sans relancer le full pipeline scoring."
  - decompose-angle: "decompose-angle deep pass UNE angle existante (formula 4 components → atoms recursive · verbatim sources · sample sizes). map-angles scaffold N angles light pass (formula text-level only)."
  - cartograph: "cartograph est READ-ONLY synthèse strategique cross-brand. map-angles WRITE brand-side (scaffold angles ANG-NN.json light pass avec lineage canon)."
  - snapshot-brand: "snapshot-brand orchestrateur cartographie brand + products + audiences. map-angles atomique angles-only · invocable post-cartographie audiences pour scaffold portfolio angles."
consumes:
  - brands/{slug}/audiences/*/profile.json (cross-product audience cartographiées · target source)
  - brands/{slug}/products/*/spec.json (mechanism + benefits pour formula.bridge)
  - brands/{slug}/brand.json (origin_axis brand-derived · tone of voice · positioning)
  - brands/{slug}/angles/*.json (existing angles brand pour merge/duplicate avoid)
  - brands/{slug}/products/*/spec.json#/use_cases[] (mode spectre · UC-NN, axe externe du croisement 3D)
  - brands/{slug}/brand.json#/meta/stage (mode spectre · stage_at_build du spectrum)
  - brands/{slug}/spectrum.json (mode spectre · brownfield merge, ne pas écraser cellules validated)
  - resources/schemas/spectrum.schema.json (mode spectre · contrat de la carte)
  - resources/schemas/angle.schema.json (target v1.2)
  - resources/canon/copy/hooks/* (hook_canon_id lineage obligatoire)
  - resources/canon/copy/angles/* (angle_canon_id lineage obligatoire)
  - resources/canon/copy/frameworks/* (framework_canon_id lineage obligatoire)
  - resources/canon/copy/archetypes-voix/* (archetype_canon_id lineage obligatoire)
  - resources/canon/copy/niveaux-schwartz/* (awareness_stage canon Schwartz)
  - resources/schemas/_shared/awareness-stage.json (5 stages canon $ref shared)
  - docs/system/compositional-cartography.md (canon doctrine formula 4 components)
  - docs/system/canonical-matrix-reasoning.md (canon CMR · canon × audience cross-product)
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/doctrine/audiences-cartography-doctrine.md
produces_proposals_for:
  - brands/{slug}/angles/{ANG-NN}.json (light pass scaffold · formula text + lineage canon + meta hypothesis)
  - brands/{slug}/spectrum.json (mode spectre · la carte · cells use_case × audience × origin_axis)
permissions:
  reads: [brands/, resources/, docs/]
  writes: [brands/{slug}/angles/{ANG-NN}.json via write_to_context, brands/{slug}/spectrum.json via write_to_context (mode spectre)]
  emits_events: [angle_cartography_proposal_created, angle_cartography_validated]
pipeline:
  preconditions:
    - "brand.json existe"
    - "Au moins 1 audience cartographiée dans brands/{slug}/audiences/"
    - "Canon copy loaded (hooks + angles + frameworks + archetypes-voix + niveaux-schwartz)"
  postconditions:
    - "N angle ANG-NN.json scaffold conformes angle.schema v1.2"
    - "lineage canon obligatoire (hook_canon_id + framework_canon_id + angle_canon_id + archetype_canon_id) sur chaque angle"
    - "validation_status hypothesis par défaut"
    - "operator validation gate passed"
prerequisites:
  - field: audiences/*/profile.json
    level: L1
    auto_pull: read_audiences_cartographiees
    freshness_ttl_days: 90
  - field: products/*/spec.json
    level: L1
    auto_pull: read_products_for_formula_bridge
    freshness_ttl_days: 90
  - field: brand.json
    level: L1
    auto_pull: read_brand_for_origin_axis
    freshness_ttl_days: 90
  - field: angles/*.json
    level: L2
    auto_pull: read_existing_angles_brownfield
    freshness_ttl_days: 90
    fallback: greenfield_no_existing
  - field: resources/canon/copy/hooks
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: resources/canon/copy/angles
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: resources/canon/copy/frameworks
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: resources/canon/copy/archetypes-voix
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: resources/canon/copy/niveaux-schwartz
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
---

# map-angles

Atomique cartography. Cartographie le PORTFOLIO angles brand-wide depuis audiences cartographiées · cross-product audience × origin_axis · scaffold N angles ANG-NN.json light pass (formula 4 components text-level + lineage canon obligatoire) sans deep production matrix scoring. Invocable séparément pour refresh cartographie angles sans relancer le full pipeline `produce-paid-angles`.

Distinct `produce-paid-angles` (qui scoring + ranks 5-7 angles top sur UNE audience avec matrice 5-lens framework). map-angles scaffold le portfolio brand-wide depuis cross-product audience × axis origin canon · light pass formula text-level only, lineage canon obligatoire, validation_status hypothesis par défaut.

## Hard Rules

### Step 0 · DRGFP prerequisite check (v2.38 canon)

Avant Step 1, scanner prerequisites :

1. **L1 silent** · `brand.json` (origin_axis brand-derived) · `audiences/*/profile.json` cartographiées · `products/*/spec.json` (formula.bridge) · canon copy 5 couches (hooks + angles + frameworks + archetypes-voix + niveaux-schwartz)
2. **L2 brownfield** · `angles/*.json` existing brand · si présents, merge/duplicate avoid · si absents, greenfield scaffold
3. **L3 gate operator** · si audiences/ vide → refuse + reco `map-audiences` d'abord (besoin audiences cartographiées pour cross-product) · si canon copy dormant → fail-safe (master doctrine `PhantomOS reasons over a business universe` exige canon obligatoire)

Output state map + confidence_chain[] init.

Cross-ref doctrine · `docs/system/dependency-resolution-protocol.md`.

### Step 0bis · Load canon copy matrices (force batch read · master doctrine)

Skill ne fonctionne pas en mode prose libre déduit de connaissance LLM · il consume canon. Si canon dormant → output générique averaged-LLM, contourne master doctrine `PhantomOS reasons over a business universe`.

Lecture batch obligatoire via `python3 .skills/phantom-canon.py copy {layer}` pour chaque couche :

1. **`hooks`** · 6 ouvertures canon (curiosity-gap, contrarian, stat-choc, avant-apres, question-callout, confession). Hook ID lineage `hook_canon_id` obligatoire sur chaque angle scaffold.
2. **`angles`** · 6 axes narratifs canon (mecanisme-unique, identite, retour-en-arriere, ennemi-commun, status-shift, contre-intuitif). Angle ID lineage `angle_canon_id` obligatoire.
3. **`frameworks`** · 6 squelettes structurels canon (AIDA, PAS, BAB, QUEST, FAB, 4Ps). Framework ID lineage `framework_canon_id` obligatoire.
4. **`archetypes-voix`** · 12 registres canon Mark+Pearson (innocent, sage, explorer, rebelle, magician, heros, amante, jester, homme-ordinaire, caregiver, ruler, creator). Archetype ID lineage `archetype_canon_id` obligatoire. Enum complet `archetype_canon_id_enum` frontmatter ci-dessus.
5. **`niveaux-schwartz`** · 5 stages product-awareness canon (`_shared/awareness-stage.json` $ref) · awareness_stage + sophistication (v1-v5) lineage obligatoire.

Pour chaque outil canon lu, garder en mémoire · `id, when_works[], when_avoid[], combines_with{}`. Ces contraintes filtrent quels outils sont compatibles avec audience résolue Step 1 + product résolu Step 2.

Cache mémoire pour durée du run.

### Step 1 · Read audiences cartographiées (cross-product source)

Load chaque `audiences/*/profile.json` cartographiée brand. Extract :

- `meta.slug` (audience slug · target audience_slug angle)
- `meta.entry_door` (pain_driven | goal_driven | identity_driven · informe origin_axis audience-derived)
- `meta.scope` (broad | segment | micro)
- `meta.applies_to_products[]` (cross-product binding · informe formula.bridge.spec_activated)
- `meta.validation_status` (hypothesis | tested | validated · propagation confidence_chain downstream)
- `pain_points[]` (si encodés · informe formula.observation + formula.tension · sinon null light pass)
- `psychology.jtbd.emotional_driver` (si encodé · informe archetype_canon_id mapping)

Si audience `validation_status: hypothesis` (light pass map-audiences sans mining) → propagation confidence `TRÈS faible` ou `faible` sur angles dérivés. Confidence chain hérité doctrine `confidence-propagation.md`.

### Détection du mode (portfolio vs spectre)

map-angles a deux modes. **Mode portfolio** (défaut, comportement v1.0.2 strictement inchangé) · scaffold N angles ANG-NN depuis le cross-product audience × origin_axis. **Mode spectre** · s'active si invoqué avec le flag mode spectre (par `build-atlas-complete` palier spectre, par `/phantom {brand} spectre`, ou demande opérateur « cartographie le terrain / le spectre »). En mode spectre, le skill ne scaffold PAS d'angles · il croise en 3D, écrit la carte `spectrum.json`, et rend la carte. **Précondition mode spectre** · `spec.use_cases[]` non vide → sinon refuse + reco `map-audiences` mode spectre d'abord (le pont Mc→U doit avoir tourné).

### Mode spectre · la carte du terrain (overlay de Step 2 et 3)

(s'exécute uniquement en mode spectre · remplace le scaffold d'angles par l'écriture de la carte)

**Croisement 3D.** Le cross-product de Step 2 passe de 2 axes (audience × origin_axis) à 3 axes · `use_case × audience × origin_axis`. `use_case` (UC-NN de `spec.use_cases[]`) est l'axe externe, on itère par usage. Le mode portfolio garde son 2-axes intact.

**Cellules faibles → zones blanches (pas skip).** Là où le portfolio fait skip+log d'une cellule faible, le mode spectre ÉMET la cellule en `coverage_self: blank` + `lever` nommé + `blank_qualification: unqualified`. Une zone vide n'est pas jetée, elle est cartographiée comme terrain libre à qualifier (D#502). Le skip+log reste pour le portfolio.

**Évidence typée + saturation par cellule.** Chaque cellule porte `evidence[]` typée (behavioral/voc/vom/structural/cultural + force + `_source`, D#503 · le verbatim n'a pas le monopole) et `saturation` (seed depuis map-mechanisms market_sophistication).

**Écriture · le singleton `spectrum.json` (PAS N angles).** Le mode spectre écrit `brands/{slug}/spectrum.json` (spectrum.schema v1.0), pas N fichiers ANG-NN.

Champs par cellule (clés EXACTES, `use_case_ref` lit `spec.use_cases[].use_case_id`) ·
```json
{"cell_id":"SPC-NN","use_case_ref":"UC-NN","audience_ref":"{slug ou null si grain usage}","origin_axis":"{enum}","coverage_self":"covered|partial|blank","coverage_market":"unknown","strategic_position":null,"saturation":"{fresh|warming|saturated|unknown ou null}","status":"hypothesis","is_core":false,"blank_qualification":"opportunity|cemetery|desert|unqualified","lever":"{nommé si unknown/blank/hypothesis}","evidence":[{"evidence_type":"behavioral|voc|vom|structural|cultural","force":"strong|moderate|weak","_source":"observed|inferred|declared","ref":"...","note":"..."}]}
```
Règles · `coverage_market: "unknown"` en dur (pont watch-competitors différé · NE PAS fabriquer) · `strategic_position: null` tant que coverage_market unknown (règle schema, garantie skill) · `status: "hypothesis"` si pas d'evidence · `lever` obligatoire sur toute cellule unknown/blank/hypothesis (jamais inventer, D#503) · `blank_qualification` posé sur les cellules blank. Top-level · `brand_slug`, `refreshed_at` (timestamp du run, RÉ-estampillé à chaque écriture), `stage_at_build` (← `brand.json#/meta/stage`, null si absent), `regime`, `core_cell_ref` (le `cell_id` du cœur · le snapshot lit ce champ, pas la boucle is_core).

**Écriture mécanique (read → merge → write, JAMAIS un write naïf qui écrase).**
1. Lire le `spectrum.json` existant s'il existe (`load_json`).
2. Fusionner par `cell_id` · pour chaque cellule entrante, si une cellule de même `cell_id` existe avec `status: validated` (ou scaled), PRÉSERVER l'existante telle quelle (ne pas la régresser à hypothesis). Sinon, la nouvelle remplace.
3. Écrire le document fusionné en **`--mode direct`** (un singleton complet, PAS un champ stampable · le whole-file `proposed` est refusé par le writer) · `write_to_context --path "brands/{slug}/spectrum.json" --mode direct --source agent --confidence 0.6`. Ré-estampiller `refreshed_at`.

**Déposer le beat de restitution du spectre (D#520).** Doctrine SSOT · `docs/system/restitution-beat-doctrine.md` (contrat payload, règles décision-d'abord, richesse second-ordre, temporalité, mode, table phase→vue). Une fois `spectrum.json` écrit et fusionné, pendant que ton contexte est frais, écris (`Write` · c'est sous `.phantom/`, hors `brands/`, donc **hors gate mutation** · ne passe PAS par `write-to-context`) le fichier `.phantom/beats/{slug}/spectrum.json` (le payload du beat, PAS le `spectrum.json` métier · noter le chemin `.phantom/beats/`). C'est la matière que `build-atlas-complete` RENDRA à l'opérateur · tu ne compresses pas la carte en une phrase météo, tu déposes la lecture du terrain (anti double-compression · le raisonnement meurt quand on l'écrase ici puis qu'on demande au fil de le re-broder). Le contenu vise le **second ordre** (l'implication, la tension, le négatif concurrentiel · cf doctrine règle 2), pas le constat plat. `phase: "spectrum"`. Forme ·

   ```json
   {
     "phase": "spectrum",
     "verdict": "<la lecture de la carte, une ligne tranchée · où on tient (cœur de cible · cellules covered), où c'est libre face aux concurrents (zones blanches qualifiées opportunity)>",
     "read":     "<2-3 phrases · le second ordre · QUELLE zone blanche est la plus rentable et POURQUOI (croisement saturation faible × usage à fort pull × audience non servie), et le négatif concurrentiel (le lane que personne ne tient, ce qu'il coûte d'y aller, sa fragilité)>",
     "analyzed": ["<recoupements use_case × audience × origin_axis · ex « l'usage UC-NN concentre N cellules covered mais l'usage adjacent reste vierge → terrain de croissance, pas le cœur historique »>"],
     "found":    ["<faits saillants de la carte · cellules covered, le cœur de cible marqué (core_cell_ref), les zones blanches opportunity comptées>"],
     "rejected": [{"what": "<territoire cimetière · cellule qualifiée cemetery>", "why": "<la raison · saturé v5, usage sans pull réel, audience absente · défendable>"}],
     "confidence": [{"claim": "<assertion sur une cellule ou une zone>", "level": "forte|moyenne|faible", "reason": "<la VRAIE cause · une evidence structural/inferred n'est pas une cellule à confiance forte>"}],
     "blocked":  [{"source": "<ex · couverture concurrente>", "reason": "<coverage_market unknown en dur · le pont watch-competitors n'a pas tourné · à lever par watch-competitors>"}],
     "encoded":  ["<artefacts posés · spectrum.json · N cellules · M zones blanches qualifiées · cœur marqué>"],
     "basis":    "<une ligne sobre · les usages croisés, les audiences cartographiées, l'évidence typée lue · rendue « Lu · ... »>",
     "tease": "<une ligne qui tease la valeur DANS la carte · l'étendue du jouable, la zone blanche qui saute aux yeux · NE mets pas de chemin, le code ajoute la commande paste-ready et choisit la vue (spectre) selon la phase>"
   }
   ```

   **Décision-d'abord, le code décide la forme.** Tu déposes les champs, `render-beat.py` réorganise en · ouverture `verdict` + `read`, puis le raisonnement qui flue (`analyzed` + `found` + `rejected`), puis **Ce sur quoi je reste prudent** (`blocked` + confiance non-forte, avec leur cause · la couverture concurrente non vérifiée va ici, avec son levier `watch-competitors`), puis `basis`, puis le CTA `tease`. La confiance **forte** n'est pas affichée seule, elle vit dans le verdict (on flague l'incertain, on ne caveat pas ce dont on est sûr). Les items `prudent` pointent l'étape qui les lèvera (la couverture marché reste `unknown` en dur tant que `watch-competitors` n'a pas tourné · le dire, ne pas fabriquer).

   **Richesse · le négatif concurrentiel et le nerf.** `read` et `analyzed` ne s'arrêtent pas à « telle cellule est blanche » · ils déroulent la **conséquence** · quelle zone blanche est la plus rentable et pourquoi (le croisement usage à fort pull × audience non servie × saturation faible), le lane que personne ne tient et ce qu'il coûte d'y aller, sa fragilité. Chaque territoire cimetière (`rejected`) porte sa raison (le rejet est le travail le plus défendable et le plus invisible). C'est la densité d'insight qui fait l'expert 360, pas la longueur. Registre **sharp, pair-expert, jamais météo**.

   **CTA + temporalité (le code décide la vue, pas le modèle).** Le `tease` est l'accroche (la valeur dans la carte) · `render-beat.py` y appose la commande `/phantom {slug} spectre` paste-ready (table `PHASE_VIEW` · phase `spectrum` → vue `spectre`) et signale le cap forward-look « j'écris les angles d'attaque, un par territoire » (table `PHASE_NEXT`). Champ vide = omis, jamais inventé. C'est un état système (restitution), pas de la donnée de marque · il ne transite pas par `write-to-context`, et le hook `beat-emit` garantit qu'il sera montré si l'orchestrateur l'oublie.

   **Émission selon le mode (réutilise le signal orchestré-vs-standalone déjà détecté).** Le skill connaît déjà sa porte d'entrée (cf « Détection du mode » · invoqué par `build-atlas-complete` palier spectre = **orchestré** · invoqué par `/phantom {brand} spectre` ou demande opérateur = **standalone**).
   - **Orchestré** · NE rends PAS le beat toi-même · contente-toi d'écrire le payload, `build-atlas-complete` l'émet (`render-beat.py --mode orchestrated`) et présente sa sortie telle quelle. Tu peux t'arrêter là (le rendu opérateur ci-dessous est porté par l'orchestrateur).
   - **Standalone** · le skill est arrivé seul, il émet AUSSI son beat · `python3 .skills/render-beat.py --brand {slug} --phase spectrum --mode standalone`, et présente sa sortie **telle quelle** (NE re-narre pas, NE re-résume pas). En standalone le renderer PROPOSE la suite (« Prochaine étape · j'écris les angles d'attaque, un par territoire. Je lance ? »).
   - **Filet** · si `render-beat` rend du vide (pas de payload trouvé), retomber sur le rendu opérateur en prose ci-dessous · ne JAMAIS laisser un trou à la place de la phase.

**Rendu opérateur · la carte (pas le top-3 angles).** L'output est la carte (table lisible des cellules par couverture + zones blanches qualifiées + cœur de cible marqué), en posture d'investigation (Observé / Déduit / Inconnu / Leviers / Close ouvert). La priorisation (top-3) reste un objet séparé (score-matrix) · la carte montre l'étendue du jouable, elle ne décide pas le spend (D#502).

### Step 2 · Cross-product audience × origin_axis canon

Pour chaque audience cartographiée, cross-product contre 5 origin axes canon (`angle.schema v1.2`) :

| Origin axis | Definition | Trigger contexte |
|---|---|---|
| **`audience-derived`** | Built from audience pain/desire/identity | Si audience pain_points encodés OR psychology.jtbd dense |
| **`product-derived`** | Built from spec/mechanism | Si product spec.active_principle OR spec.mechanism dense |
| **`category-derived`** | Built from market context vs alternatives | Si brand.market.competitors OR sector market context encodé |
| **`brand-derived`** | Built from brand identity/tone | Si brand.tone_of_voice OR brand.positioning explicit |
| **`temporal-cultural`** | Built from moment, trend, cultural pivot | Si seasonal OR trend signal encodé brand.json#market.seasonality |

Pour chaque cell `(audience_X, origin_axis_Y)`, évaluer opportunity angle :

- Cell viable → scaffold ANG-NN.json
- Cell weak (origin axis silent OR audience pain absent) → skip + log
- Cell duplicate (existing angle même audience + origin_axis détecté) → merge avoid + log

Cap canon · **N audiences × 5 origin_axes = N×5 candidates max** · filter à 8-15 angles scaffold par run (au-delà, dilue cartographie et viole Pareto canon).

### Step 3 · Scaffold formula 4 components light pass

Pour chaque opportunity cell Step 2, scaffold formula 4 components text-level only (deep atoms delegated `decompose-angle`) :

```json
{
  "formula": {
    "observation": {
      "summary": "{1-line phrasing observation depuis audience pain OR product spec}"
    },
    "tension": {
      "summary": "{1-line phrasing tension gap depuis audience jtbd OR product benefit}"
    },
    "reframe": {
      "summary": "{1-line phrasing perceptual pivot · contre-narrative canon}"
    },
    "bridge": {
      "summary": "{1-line phrasing how product fits reframed worldview}"
    }
  }
}
```

Hard rule canon · `docs/system/compositional-cartography.md` équation v3.1 formula `Observation + Tension + Reframe + Bridge` respect obligatoire. Validated empirically sur 23 ads cross-typologies S55.

Light pass · `summary` text-level only par component. Deep atoms (phenomenon · source · sample_size · state_actual · state_desired · pivot_mechanism · spec_activated · benefit_served · promise_formulated) restent `null` jusqu'à `decompose-angle` deep drill.

### Step 4 · Lineage canon assignation (obligatoire)

Pour chaque angle scaffold Step 3, assigner lineage canon depuis matrices Step 0bis :

```json
{
  "lineage": {
    "awareness_stage": "{unaware | problem_aware | solution_aware | product_aware | most_aware}",
    "schwartz_sophistication": "{v1 | v2 | v3 | v4 | v5}",
    "hook_canon_id": "{hook_id depuis canon/copy/hooks/}",
    "framework_canon_id": "{framework_id depuis canon/copy/frameworks/}",
    "angle_canon_id": "{angle_id depuis canon/copy/angles/}",
    "archetype_canon_id": "{archetype_id depuis canon/copy/archetypes-voix/}",
    "pain_extract": "{pain extract from audience profile OR product spec}",
    "proof_primary": "{proof primary type depuis spec.proofs OR null}",
    "cta": "{cta suggéré OR 'à créer'}"
  }
}
```

Hard rule canon · 4 IDs lineage canon obligatoires sur chaque angle (`hook_canon_id`, `framework_canon_id`, `angle_canon_id`, `archetype_canon_id`). Anti-pattern v2.55 BANNI · halluciner archetype ou hook sans le mapper au canon (`PhantomOS reasons over a business universe`, canon dormant = output générique averaged-LLM).

Cross-product canon × audience cartographié obligatoire :
- Si audience entry_door pain_driven → angle archetype likely `caregiver` OR `sage` OR `innocent` (cross-ref canon `when_works`)
- Si audience entry_door identity_driven → angle archetype likely `rebelle` OR `amante` OR `explorer` OR `ruler` (cross-ref canon `when_works`)
- Si audience entry_door goal_driven → angle archetype likely `heros` OR `magician` OR `creator` (cross-ref canon `when_works`)
- Si audience registre fun ou hédoniste → angle archetype likely `jester` OR `amante` (cross-ref canon `when_works`)
- Si audience scope broad → angle awareness_stage likely `problem_aware` OR `solution_aware` (top funnel)
- Si audience scope micro → angle awareness_stage likely `product_aware` OR `most_aware` (bottom funnel)

Combination matrix canon (`combines_with{}` field de chaque outil) filtre les compatibilités. Ex hook `confession` combines well with framework `PAS` + archetype `homme-ordinaire`. Ex angle `mecanisme-unique` combines well with hook `curiosity-gap` + framework `FAB`.

### Step 5 · Origin axis attribution + awareness movement

Pour chaque angle scaffold :

```json
{
  "origin_axis": "{audience-derived | product-derived | category-derived | brand-derived | temporal-cultural}",
  "awareness_movement": {
    "in": "{awareness stage assumé start}",
    "out": "{awareness stage produit end}"
  }
}
```

Hard rule canon · `awareness_movement.in` ≤ audience.awareness_dominant pour que l'angle soit playable sur audience. Si `in > out` → flag MAJOR (angle régresse · deliberate re-funnel OR erreur).

Awareness movement light pass · `in == out` acceptable (angle valide perception existante) OR `in < out` (angle éduque, plus coûteux mais plus différenciant). Deep scoring movement delegated `produce-paid-angles`.

### Step 6 · Cross-audience compatibility detection

Pour chaque angle scaffold, scan pairwise audiences cartographiées (autres que primary `audience_slug`) pour détection compatibility cross-audience :

```json
{
  "compatibility": [
    {
      "audience_slug": "{other_audience_slug}",
      "fit": "{strong | moderate | weak}",
      "notes": "{1 phrase · pourquoi fit X · pain match + objection convergence OR divergence}"
    }
  ]
}
```

Hard rule canon · default safe `fit: moderate` si signal mixte, `fit: weak` si pain ou objection divergent, `fit: strong` uniquement si pain match + objection match + verbatim convergence (verbatim density requise · sinon stay `moderate`).

### Step 7 · Stage chaque angle via mutation gate

Pour chaque angle scaffold Steps 3-6, write_to_context :

```bash
python3 .skills/write-to-context.py --path "angles/{ANG-NN}.json" --value '{...full angle object schema v1.2 conforme...}' --source agent --confidence 0.6 --mode proposed --reason "map-angles light pass scaffold · D#386 atomique cartography"
```

ANG-NN ID stable · pattern `^ANG-[0-9]{2,3}$` canon. Incrément depuis existing angles brand (read Step 0bis brownfield).

Conformité `angle.schema v1.2` obligatoire. Validation_status `hypothesis` par défaut. `created_by_skill: "map-angles"`.

### Step 8 · Output operator-facing 5 sections investigation-posture

**Doctrinal contract canon.** map-angles produit synthèse strategique cartographie · structure obligatoire 5 sections explicites (`docs/system/investigation-posture.md`).

#### Section 1 · Observé (faits sourcés)

```
Observé · cartographie depuis matière brand encodée (run {date}, {duration})

- Audiences cartographiées : {N audiences · slugs + scope + entry_door}
- Products encodés : {N products · slugs + active_principle si dense}
- Brand origin signals : {tone_of_voice + positioning + market.competitors si dense}
- Angles existing brand : {N existing · slugs}
- Canon copy chargé : {5 couches · {hook_count} hooks + {angle_count} angles + {framework_count} frameworks + {archetype_count} archetypes}
```

#### Section 2 · Déduit (cartographie N angles + top-3 opportunities qualitatif)

```
Déduit · {N angles} hypothèses cartographiées + top-3 opportunities qualitatif

[ANG-01] {angle_name} (audience-derived · {audience_X_slug})
  Formula light · obs + tension + reframe + bridge texte
  Lineage canon · hook={hook_id} + framework={framework_id} + angle={angle_id} + archetype={archetype_id}
  Awareness movement · {in} → {out}
  Confidence · {forte | moyenne | faible · hérité audience_source}
  Compatibility · {N audiences cousines · fit {strong|moderate|weak}}

[ANG-02] {angle_name} (product-derived · {product_X_slug})
  ...

[ANG-03] {angle_name} (category-derived · vs alternatives)
  ...

─────

Top-3 opportunities qualitatif (pas scoring numérique · délégué produce-paid-matrix)

  1. {ANG-XX} · ranking qualitatif raison · {pain density + canon compatibility forte + audience confidence}
  2. {ANG-YY} · ranking qualitatif raison · {differentiation vs competitors + brand tone alignment}
  3. {ANG-ZZ} · ranking qualitatif raison · {audience confidence forte + lineage canon optimal}
```

Hard rule canon · angles présentés comme HYPOTHÈSES (validation_status hypothesis par défaut). Qualitatif ranking only · jamais scoring numérique exposé (delegated `produce-paid-matrix` OR `produce-paid-angles` deep).

#### Section 3 · Inconnu (variables à mining-confirm)

```
Inconnu · variables à creuser pour passer hypothèse → testé/validé

- Verbatim density réelle audience source par angle (mining requise pour confidence forte)
- Performance réelle paid (CTR + CPA + ROAS) par angle (test launch requis)
- Vrai stade Schwartz audience cible (mining + analytics pour valider awareness_movement)
- Vraies objections audience cible (severity + frequency · confidence_chain dépend)
- Proof primary réel par angle (spec_activated + benefit_served · audit-meta-account learnings)
- Compatibility cross-audience réelle (test learnings cross-pivot fit strong vs moderate)
```

#### Section 4 · Leviers (drill-down options)

```
Leviers · 4 axes prioritaires post-cartographie angles

Axe A · Deep scoring matrice paid sur UNE audience top (5-lens scoring framework + ranked table 5-7 angles)
  → ideation paid deep production avec verbatim density check + cluster filter + cap rank
  → requiert verbatim density audience source >= 5 (sinon mine-voc d'abord)
  
Axe B · Decompose UNE angle deep (formula atoms · verbatim sources · sample sizes)
  → audit angle hypothèse → confidence upgrade par sourcing atomes (phenomenon, source, sample_size)
  → ~5-10 min sur angle prioritaire
  
Axe C · Produire brief créa direct sur UNE angle scaffold
  → brief copywriter hook + body + CTA depuis angle light pass
  → propage confidence chain TRÈS faible si audience source hypothesis · test budget calibré
  
Axe D · Pivot sur autre audience cartographiée brand (refresh angles cross-audience)
  → re-run map-angles avec audience_slug différent pour scaffold portfolio autre audience
```

#### Section 5 · Close ouvert (UNE question macro)

Anti-pattern AP-5 BANNI · close affirmatif fermé. Toujours close ouvert drill-down macro · UNE question · opérateur arbitre.

Format close canonique :

> Pour passer ces {N} angles de hypothèse à testé/validé et débloquer la suite (brief créa, launch paid) ·
>
> A · Deep scoring matrice paid sur audience top {audience_top_label} (~10-15 min · 5-lens framework + ranked 5-7 angles + verbatim density check). Recommandé si confidence audience source forte.
> B · Decompose UNE angle deep pour upgrade confidence (~5-10 min · formula atoms verbatim-sourced sur {ANG-XX top}). Recommandé si tu veux trace canon complète avant brief créa.
> C · Brief créa direct sur UNE angle scaffold (test budget calibré · confidence héritée hypothèse). Recommandé si deadline serrée et tu testes en aveugle accepté.
> D · Pivot sur autre audience cartographiée brand (refresh cartographie angles cross-audience).
>
> Mon avis · {reco macro adaptive · si audience source hypothesis TRÈS faible → A après upgrade audience OR C avec budget calibré · si audience source validée mine-voc → A direct scoring matrice}.

L'opérateur arbitre · l'agent enchaîne le drill-down sur l'axe choisi (silencieusement vers `produce-paid-angles` OR `decompose-angle` OR `produce-copy-brief` OR re-run `map-angles` selon choix).

### Step 9 · Finalize mutation batch

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mécanique. Inspecte mutations Step 7, runs structural checks (schema v1.2 compliance + lineage canon presence + validation_status hypothesis), emit `angle_cartography_validated` event pour turn-end-audit.

Exit code 2 = blocking issue → revise avant ship. Exit code 0 warnings = log, ship.

## Hard rules globales

- **Canon copy obligatoire lineage** · 4 IDs canon (`hook_canon_id`, `framework_canon_id`, `angle_canon_id`, `archetype_canon_id`) sur chaque angle scaffold. Anti-pattern v2.55 BANNI · halluciner sans canon mapping.
- **Doctrine compositional-cartography formula 4 components** · `Observation + Tension + Reframe + Bridge` respect obligatoire (canon `docs/system/compositional-cartography.md` v3.1). Light pass text-level only, deep atoms delegated `decompose-angle`.
- **JAMAIS scoring numérique exposé** en surface operator · délégué `produce-paid-matrix` OR `produce-paid-angles` deep. Top-3 ranking qualitatif uniquement (raison + canon compatibility + audience confidence).
- **Backward compat strict** · existing angles brownfield (read Step 0bis) jamais écrasés. Merge strategy · skip si entry existing + validation_status >= validated. Append nouveau ANG-NN incrémenté. Flag conflict si collision même audience + origin_axis (operator arbitre).
- **validation_status hypothesis par défaut** · sur chaque angle scaffold light pass. Upgrade `tested` post-launch paid · `validated` post-CPA/ROAS confirmation viable.
- **Confidence chain hérité audience source** · si audience source hypothesis → angle confidence `TRÈS faible` ou `faible` (algèbre conservative cross-skill MIN, doctrine `confidence-propagation.md`). Anti-pattern AP-1 doctrine évité.
- **JAMAIS exposer field path interne** · `lineage.hook_canon_id`, `formula.observation.summary`, `meta.validation_status`, `origin_axis` brut en surface operator. Reformuler en langage métier (axe narratif, observation, archetype voix, hypothèse à valider, depuis audience/produit/catégorie/brand/moment).
- **JAMAIS nommer skill** (`mine-voc`, `produce-paid-angles`, `decompose-angle`, `produce-copy-brief`) en surface operator. Routing silencieux post-arbitrage opérateur.
- **DRGFP L3 gate strict** · audiences/ vide → refuse + reco `map-audiences` d'abord (cross-product requiert audiences cartographiées). Canon copy dormant → fail-safe (master doctrine).
- **Cap 8-15 angles scaffold par run** · cross-product N audiences × 5 origin_axes peut exploser. Filter selon viability cell + canon compatibility + Pareto canon (top opportunities qualitatives). Au-delà 15 dilue cartographie. **SAUF mode spectre** · la carte est exhaustive (D#502), le cap est relâché · il reste intact en mode portfolio.
- **Awareness movement playability** · `awareness_movement.in` ≤ `audience.awareness_dominant`. Si `in > out` flag MAJOR (régresse · erreur ou re-funnel deliberate).

## Anti-patterns

- **AP-1** · scaffold angle sans 4 IDs lineage canon (viole doctrine routing canon copy obligatoire).
- **AP-2** · scoring numérique exposé en surface (overlap produce-paid-matrix scope · délégué).
- **AP-3** · formula skip · `observation` ou `tension` ou `reframe` ou `bridge` `summary` null (viole compositional-cartography canon v3.1).
- **AP-4** · halluciner archetype ou hook sans canon mapping (viole master doctrine PhantomOS reasons over a business universe).
- **AP-5** · close affirmatif post-cartographie (*"angles saved, what next?"*) · banni canon investigation-posture.
- **AP-6** · audience source confidence chain ignoré · angle confidence default `forte` alors qu'audience `hypothesis` (viole algèbre conservative).
- **AP-7** · cap >15 angles · viole Pareto canon (top opportunities should be 3-5 priority). **Mode portfolio uniquement** · ne s'applique pas au mode spectre (carte exhaustive par design).
- **AP-8** · deep atoms scaffold (phenomenon, source, sample_size) en map-angles · scope creep `decompose-angle`.
- **AP-9** · scoring 5-lens framework appliqué · scope creep `produce-paid-angles` (cluster filter + cap rank + verbatim density check). map-angles est cartography light, pas production deep.
- **AP-10** · default origin_axis `audience-derived` silencieusement · attribution doit être contextuelle (5 axes canon).

## Operator output template canonique

```
{BRAND} · CARTOGRAPHIE ANGLES ({N} hypothèses cross-product)

─────────────────────────────────────────────

Observé · matière brand lue (run {date}, {duration})

  Audiences cartographiées  {N · slugs + scope + entry_door}
  Products encodés          {N · slugs + active_principle si dense}
  Brand origin signals      {tone + positioning + competitors si dense}
  Angles existing brand     {N existing}
  Canon copy chargé         {5 couches · {totals}}

─────────────────────────────────────────────

Déduit · {N angles} hypothèses cartographiées

  [ANG-01] {angle_name} (depuis audience · {audience_X})
    Formule light       observation + tension + reframe + bridge texte
    Référence canon     hook + framework + axe narratif + archetype voix
    Mouvement awareness {stade_in} → {stade_out}
    Confidence          {forte | moyenne | faible · hérité audience source}
    Audiences cousines  {N · fit qualitatif}

  [ANG-02] {angle_name} (depuis produit · {product_X})
    ...

  [ANG-03] {angle_name} (depuis catégorie · vs alternatives)
    ...

  ─────

  Top-3 opportunités qualitatif

  1. {ANG-XX} · raison ranking · {pain density + canon compatibility + audience confidence}
  2. {ANG-YY} · raison ranking · {differentiation vs competitors + brand tone alignment}
  3. {ANG-ZZ} · raison ranking · {audience confidence forte + lineage canon optimal}

─────────────────────────────────────────────

Inconnu · variables à creuser pour passer hypothèse → testé/validé

  - Verbatim density réelle audience source par angle
  - Performance réelle paid (CTR + CPA + ROAS) par angle
  - Vrai stade Schwartz audience cible
  - Vraies objections audience cible (severity + frequency)
  - Proof primary réel par angle
  - Compatibility cross-audience réelle vs hypothèse

─────────────────────────────────────────────

Leviers · 4 axes drill-down post-cartographie

  Axe A · Deep scoring matrice paid sur UNE audience top
  Axe B · Decompose UNE angle deep (atoms verbatim-sourced)
  Axe C · Brief créa direct sur UNE angle scaffold
  Axe D · Pivot sur autre audience cartographiée brand

─────────────────────────────────────────────

Close · UNE question macro drill-down

Pour passer ces {N} angles de hypothèse à testé/validé ·

A · Deep scoring matrice paid sur audience top {audience_top_label} (~10-15 min · 5-lens framework + ranked + verbatim density check).
B · Decompose UNE angle deep pour upgrade confidence (~5-10 min · atoms verbatim-sourced).
C · Brief créa direct sur UNE angle scaffold (test budget calibré · confidence héritée).
D · Pivot sur autre audience cartographiée brand.

Mon avis · {reco macro adaptive selon état audience source + deadline}.
```

## Cross-references

- `docs/system/investigation-posture.md` · doctrine canon 5 sections obligatoires (Observé · Déduit · Inconnu · Leviers · Close ouvert)
- `docs/system/compositional-cartography.md` · canon doctrine formula 4 components (équation v3.1)
- `docs/system/canonical-matrix-reasoning.md` · canon CMR · canon × audience cross-product
- `docs/system/confidence-propagation.md` · algèbre cascade confidence cross-skill (audience → angle MIN conservative)
- `docs/system/audience-cartography-doctrine.md` · canon audiences source (3 niveaux MECE)
- `resources/schemas/angle.schema.json` (v1.2) · target schema scaffold
- `resources/schemas/profile.schema.json` (v1.7) · audience source schema
- `resources/canon/copy/hooks/*` · lineage hook_canon_id obligatoire
- `resources/canon/copy/angles/*` · lineage angle_canon_id obligatoire
- `resources/canon/copy/frameworks/*` · lineage framework_canon_id obligatoire
- `resources/canon/copy/archetypes-voix/*` · lineage archetype_canon_id obligatoire
- `resources/canon/copy/niveaux-schwartz/*` · awareness_stage canon Schwartz
- `resources/schemas/_shared/awareness-stage.json` · $ref shared 5 stages canon
- `.skills/skills/map-audiences/SKILL.md` · upstream cartography audience source (D#386 sister atomique)
- `.skills/skills/produce-paid-angles/SKILL.md` · deep scoring matrice paid (downstream consumer · scoring + ranks)
- `.skills/skills/decompose-angle/SKILL.md` · deep atoms verbatim-sourced (downstream consumer · formula atoms)
- `.skills/skills/produce-copy-brief/SKILL.md` · brief créa direct sur angle scaffold (downstream consumer)
- `.skills/skills/produce-paid-matrix/SKILL.md` · scoring matrice paid DTC complete (overlap produce-paid-angles + portfolio)
- `.skills/skills/snapshot-brand/SKILL.md` · orchestrateur cartographie complète (parent caller D#386)
- D#386 · décision canon · architecture cartographie marketing (snapshot-brand orchestrateur + sub-skills map-X invocables séparément)
