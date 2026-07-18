---
name: produce-paid-angles
type: producer
version: "1.15.0"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
reasoning_pattern: matrix-driven
matrix_mode: generating
consumes:
  - path: resources/frameworks/paid-angle-scoring.md
    min_version: 1.0.0
  - path: resources/frameworks/paid-angle-scoring-weights.json
    min_version: 1.0.0
  - path: resources/registries/angle-registry.md
    min_version: 1.0.0
  - path: resources/registries/proof-registry.md
    min_version: 1.0.0
  - path: resources/routing/awareness-angle-matrix.md
    min_version: 1.0.0
  - path: resources/templates/hook-formulas.md
    min_version: 1.0.0
  - path: resources/canon/copy/hooks/*
    min_version: 1.0.0
  - path: resources/canon/copy/angles/*
    min_version: 1.0.0
  - path: resources/canon/copy/frameworks/*
    min_version: 1.0.0
  - path: resources/canon/copy/niveaux-schwartz/*
    min_version: 1.0.0
  - path: resources/canon/copy/archetypes-voix/*
    min_version: 1.0.0
  - path: resources/canon/copy/heuristiques-persuasion/*
    min_version: 1.0.0
  - path: resources/schemas/_shared/awareness-stage.json
    min_version: 1.0.0
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
  - path: resources/registries/hooks/*
    min_version: 1.0.0
  - path: resources/concepts/*
    min_version: 1.0.0
  - path: docs/doctrine/angle-strategy-doctrine.md
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/doctrine/objections-mapping-doctrine.md
  - path: docs/doctrine/audiences-cartography-doctrine.md
description: >
  v1.13.0 (D#523 · coordonnée NÉGATIF câblée au contrat d'écriture) · le squelette d'angle écrit inclut désormais la 5e coordonnée `negative` (l'alternative déplacée · summary + type[competitor|category-belief|status-quo|substitute|diy|do-nothing] + spectrum_cell_ref optionnel vers le négatif concurrentiel du Spectre) · _schema_version write bumpé angle/1.3→angle/1.6. Filets post-hoc dans validate-all (advisory LOW `angle_negative_missing` si reframe sans négatif · intégrité MED `angle_negative_untraced` si spectrum_cell_ref présent ne résout pas) · jamais un gate au write (Master rule). Les 4 autres coordonnées existaient déjà au contrat (origin_axis · awareness_movement · lineage.pain_ref+formula.tension · formula.reframe). consumes angle-strategy-doctrine déjà déclaré. Backward compat strict additif.
  v1.12.0 (v2.90.0 câblage workflow A · bibliothèques cross-brand + régime) · NEW Step 0quater : lecture du cadrage de batch `creatives/{batch}/frame.json` si présent (régime explore/exploit + rayon sectoriel, produit par frame-regime) + chargement des bibliothèques cross-brand (creative-mechanics-registry 34 mécaniques · registries/hooks patterns promote-ready · resources/concepts) avec filtre de distance verticale rayon_max(freedom_cursor) et surfaçage des emprunts (pari conscient, jamais silencieux). Step 3 : NEW dimension candidate `mecanique` (concept ad-level du registre). Step 9 : si batch cadré, chaque angle top-ranked porte 3 perspectives POV (fondateur/client/expert tiers, A5). Close : chaînage workflow A (evaluate-concept → weave-hooks) quand le batch est cadré. Sans frame.json, comportement v1.11 inchangé (backward compat strict additif).
  v1.11.0 (v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés) · Section pré-runtime ajoutée AVANT Step 0 · expose 6 paramètres décomposés au runtime (audience targeted · pains/JTBD source · formula angles OTRB · couches pain-benefit-chain · hypothèses figées · biais à éviter) avec POURQUOI chacun + close binaire OK ou ajuste. Cross-ref doctrines `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ + `docs/system/engagement-disclosure-doctrine.md` v2.79.5+. Backward compat strict additif (Steps 0-12 runtime preserved · seul l'amont disclosure change).
  v1.10.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · Step 1 read encoded data refactor · pain_points lus depuis `audiences/{audience_slug}/pain_points/*.json` (sub-audience NEW v2.64 · owned natif par parent path) · objections lues depuis `audiences/{audience_slug}/objections/*.json` (sub-audience NEW v2.64). Step 11bis back-refs P4/P5 stages canonical refs `audiences/{audience_slug}/objections/{OBJ-NN}.json#response_counter` + `audiences/{audience_slug}/pain_points/{PNT-NN}.json#derived_angle_refs`. angle.schema v1.3 lineage.pain_ref + objection_ref · skill populate désormais PNT-NN + OBJ-NN refs canonical sub-audience. Backward compat strict additif · fallback transparent top-level v2.63 + profile sub-fields legacy v1.7 preserved.
  v1.9.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · Step 1 read encoded data refactor · pain_points lus depuis `pain_points/*.json filtered by affected_audiences contains audience_slug` (collection top-level NEW v2.63) · objections lues depuis `objections/*.json filtered idem` (collection top-level NEW v2.63). Step 11bis back-refs P4/P5 stages canonical refs `objections/{OBJ-NN}.json#response_counter` et `pain_points/{PNT-NN}.json#derived_angle_refs` (au lieu de profile.json#/objections/{idx} sub-fields legacy). angle.schema v1.3 lineage.pain_ref + objection_ref · skill populate désormais PNT-NN + OBJ-NN refs canonical en bonus de pain_extract text legacy. Backward compat lecture profile.pain_points[] + profile.objections[] legacy preserved (pre-v2.63 brands).
  v1.8.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method, breakthrough-advertising-5-stages, objections-mapping, audiences-cartography). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.8.0 (v2.58 coverage extend) · objections.response_counter + derived_angle_refs back-ref auto-persist · angle.compatibility[] cross-audience persist (extension encart v1.7.0). Closes 3 orphans audit v2.57.
  v1.7.0 (v2.56 Notion zone 3→4 filter-by-persona extension) : Step 11 artifact ajoute encart pivot fin de table · `Pour pivoter sur une autre audience, relance avec {audience_slug_other}` avec liste des autres `brands/{slug}/audiences/*/profile.json` cartographiées. Couvre opérationnellement le pattern Notion zone 3→4 filter-by-persona observé dans workspace stride-up. Pas de skill standalone `filter-angles-by-persona` (anti-pattern fork) · ce skill est déjà multi-audience friendly via input `{audience_slug}`. L'encart matérialise la capacité existing.
  v1.6.1 (v2.55 audit consume canon matrices) : frontmatter consumes: enrichi avec resources/canon/copy/{hooks,angles,frameworks,niveaux-schwartz,archetypes-voix,heuristiques-persuasion,_shared/awareness-stage.json}. Aligne déclaration consumes: avec Step 0ter qui lit déjà ces matrices via phantom-canon.py. Master doctrine PhantomOS reasons over a business universe ré-activé · canon dormant = output générique averaged-LLM. Mécanismes inchangés.
  v1.6.0 (v2.54 investigation posture refactor) : angles présentés avec confidence chain inheritée audience+brand en surface opérateur. Chaque angle porte derived_from_audience_confidence + derived_from_brand_confidence + claim_confidence agrégée (min des deux héritages). Ranked table colonne `Confiance` ajoutée. Close ouvre drill-down macro · test ces angles tels quels OU upgrade confidence audience source d'abord. Préserve équation Obs+Tension+Reframe+Bridge, lineage canon copy, scoring framework. Refacto uniquement la posture surface · angles avec confidence chain visible vs recommandations stratégiques posées. Cross-ref docs/system/investigation-posture.md.
  v1.4.0 (v2.36 frictions runtime patch) : HR4.5 verbatim density floor gate strict. AskUserQuestion explicit gate quand voice.key_expressions[] < 5 OR cumulative verbatim_quotes[] < 5 · pas de production sans operator response (a/b/c). Resoud anti-pattern mou v1.3.0 ou angles inferes shippaient avec flag inline sans gate explicite.
  v1.3.0 (v2.32 alignment) : when reading creative.json instances, prefer intent_mix over intent and overlay_density + brand_mark_present over craft_mode. validation_status read via oneOf (legacy string OR composite object).
  Generates a ranked matrice copy of paid creative angles for an audience
  on a brand. Consumes encoded intelligence (verbatims, pains, objections,
  vernacular) from mine-voc / mine-vom Layer B. Internal cartesian product
  of audience × awareness × emotion × objection × placement, scored per
  paid-angle-scoring framework, filtered, clustered. Operator-facing output:
  ranked table 3-5 angles (up to 7 if signal density high), each with hook
  verbatim-anchored + emotion + objection + placement reco + confidence chain inheritée. Synthesis
  paragraph naming why these rank top + close drill-down macro.
  FR: "trouve les meilleurs angles pour {audience} {brand}", "matrice angles {brand}", "angles paid {audience}", "brief créa de N angles", "quels hooks tester sur {audience}".
  EN: "find the best angles for {audience} {brand}", "paid angles {audience}", "creative angles brief".
permissions:
  reads: [brand, product, profile, learning, strategy]
  writes: [learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists with at least one audience profile.json containing pain_points, objections, voice.key_expressions. Ideally mine-voc has run on the audience.
  postconditions: ranked angles artifact in produced/paid-angles/, scoring trace in sources/produced-angles/, learnings appended if pattern detected, finalize-mutation-batch event emitted, recommended next-step persisted as an idempotent In Progress line in brands/{slug}/todos.md (canonical format, auto-ticked when the downstream skill runs).
disambiguates_against:
  produce-copy-brief: "route to produce-copy-brief when operator wants a full copywriter brief on ONE chosen angle (audience + angle + channel structured doc) · produce-paid-angles is the upstream ideation step"
  mine-voc: "route to mine-voc when audience profile is thin (no verbatims encoded yet) · paid-angles needs verbatim density to score, must capture first"
  mine-audience: "route to mine-audience when audience itself is not yet defined or split · paid-angles assumes audience encoded"
  ingest-resource: "route to ingest-resource when operator drops a single brief or doc · that's a one-off ingestion, not angle ideation"
prerequisites:
  - field: audiences/{slug}/profile.json
    level: L1
    auto_pull: read_audience_profile
    freshness_ttl_days: 60
  - field: audiences/{slug}/verbatim_density
    threshold: 5
    level: L2
    options:
      - force_inferred
      - mine_voc_first
      - hybrid_one_anchored
  - field: brand.creative_zone
    level: L3
    fallback: proxy_brand_personality
    confidence_default: 0.6
  - field: resources/canon/copy/hooks
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
  - field: angles/*.json
    level: L1
    auto_pull: read_brand_angles_existing
    freshness_ttl_days: 90
---

# Skill: produce-paid-angles

> **Changelog v1.2.0 (S55 · v2.29.0 alignment).** `awareness_stage` at `lineage.awareness_stage` (renamed from `schwartz_conscience` per `angle.schema.json` v1.2). `origin_axis` at top-level (renamed from `source`). Drop fields migrated to `creative.schema.json` v1.1 (`intent`, `mecanique`, `seasonality_trigger`, `execution.craft_mode`, `execution.longevity_signal`, `execution.cta`). Use `$ref` to `_shared/awareness-stage.json` for the canonical 5 Schwartz stages. Cross-refs: v2.29.0 manifest, D#391.

Synthesizer, not fabricator. Reads encoded brand intelligence, reasons over a cartesian internally, ships a ranked angle table the operator can hand to a copywriter. The mechanism stays invisible. The operator sees ranked angles in plain language, hooks anchored in real customer voice, a synthesis that names why these top, and a reasoned next move grounded in what was just produced.

## Tone

Synthesis-first, prose-first. The output structure IS a ranked table · that's the visible deliverable. The prose around it follows the snapshot-brand Step 7 voice canon strictly: three implicit movements, no bold-section anchors, no enumeration of dimensions analyzed, no exposed scores, no internal labels. The agent never says *"5 dimensions analyzed"*, never says *"Score 73/100"*, never names a JSON field path, never closes on a hardcoded *"(a)/(b)/(c)/(d) Other"* menu. Read snapshot-brand SKILL.md Step 7 before writing the synthesis paragraph if any uncertainty.

## Expert methodology

**Persona:** senior media buyer who has watched ten thousand creatives ship and knows what wins on cold versus warm, on Reels versus Stories, on premium versus mass-market positioning. Reads a brand's encoded intelligence the way a senior strategist reads a research deck · lands on what matters, drops what dilutes, ranks by load-bearing weight, names the trade-off when there is one.

**Framework:** five-lens scoring per `resources/frameworks/paid-angle-scoring.md`. Verbatim density (35% weight, dominant), emotional resonance (20%), objection neutralization (20%), placement viability (binary filter), awareness-acquisition alignment (25%). Cluster-deduplication rule de-dupes near-identical cells. Verbatim anchor selection rule per framework Section 4.

The skill consumes the framework verbatim. No improvisation on weights, thresholds, anchor priority. Read the framework file at first invocation.

---

## Engagement disclosure pré-runtime · NIVEAU 0 paramètres décomposés (canon v2.79.5)

Avant Step 0 (Resolve target audience), expose ce disclosure NIVEAU 0 à l'opérateur. Pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5. Le but · rendre les paramètres décomposés que ce skill va mobiliser visibles AVANT exécution, pour que l'opérateur s'engage en conscience et puisse ajuster un paramètre avant de brûler 5-15 min de runtime.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Audience targeted
     {audience_slug_résolu Step 0} · segment atlas brand sélectionné
     POURQUOI · {raison priority · ex "densité verbatim la plus forte"
     OR "audience mère validée" OR "demande opérateur explicit"}

  2. Pains/JTBD source
     Lus depuis {sub-audience pain_points/* OR top-level OR profile sub-fields legacy}
     Ordre couches activé · functional → emotional → identity → aspirational
     POURQUOI cet ordre · {ex "pain dominant émotionnel-identitaire
     post-grossesse, functional reste backup proof"
     OR "audience problem-aware, functional ouvre puis bascule
     identity en bridge"}

  3. Structure angles · 4 temps
     Observation × Tension × Reframe × Bridge (acronyme interne · jamais exposé opérateur)
     POURQUOI · 4 temps canon paid-angle qui force · ancrage observable
     (Observation) → naming tension client (Tension) → renversement framing
     (Reframe) → connexion offre (Bridge). Pas freestyle prose.

  4. Couches pain-benefit-chain variants
     Functional · Emotional · Identity · Aspirational
     POURQUOI multi-couches · une seule couche = angle plat. Variants
     croisent les 4 couches pour permettre tests A/B sur axes
     orthogonaux (pas répétition cosmétique).

  5. Hypothèses figées
     Niveau sophistication marché · {stage Schwartz · lu brand.json
     OR inféré spec.market_context}
     Niveau conscience audience · {unaware → most-aware · lu profile
     market_position.awareness_dominant}
     Canal · Meta vs autre · {default Meta si stack signals · sinon
     inferred ou opérateur stated}

  6. Biais à éviter
     · Clichés DTC FR (registre "minceur magique", "régime miracle",
       "transformation 30 jours")
     · Répétition pattern angles précédents (lus learnings.json +
       angles/*.json brand existing · cluster-deduplication)
     · Sur-pondération une couche (ex 5 angles tous functional · canon
       exige variance couches pain-benefit-chain)

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?
```

ATTENDS confirmation explicite avant de lancer Step 0. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set OR si l'opérateur a flag `--no-disclosure` explicit OR si N usages successifs >= seuil expert (`auto_skip_after_n_calls` true). Sinon · disclosure obligatoire canon v2.79.5.

Cross-ref doctrines racine `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5.

---

## Step 0 · Resolve target audience

The operator references the audience in natural language. Examples: *"femme minceur okr"*, *"audience anti-âge"*, *"hommes sport perf"*, *"women 30-55 weight loss"*. Match the reference against `brands/{slug}/audiences/*/profile.json` using `meta.tags`, `identity.label`, `identity.description`, `pain_points[].formulation` as match surfaces.

Three branches:
- **One match** → continue to Step 1.
- **Multiple matches** → ask one disambiguation question via AskUserQuestion. *"On part sur la femme post-grossesse ou la femme 40+ pré-ménopause ?"* Plain language, no field names, no slugs surfaced.
- **Zero matches** → audience does not exist yet. Surface clearly: *"Pas trouvé d'audience qui matche sur cette marque. Le move utile c'est de la créer d'abord · `mine-audience` ~10 min, ou tu m'envoies les éléments en clair et je la code."* Stop. Do not invent an audience to satisfy the request.

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant détection scope (Step 1), scanner prerequisites canon DRGFP :

1. L1 silent · `audiences/{slug}/profile.json` (required input) · `resources/canon/copy/{hooks,frameworks,archetypes-voix}` · `angles/*.json` brand existing
2. L2 gate (HR4.5 v2.36 formalisé) · si `audiences/{slug}/verbatim_density < 5` → AskUserQuestion 3 options (force_inferred · mine_voc_first · hybrid_one_anchored)
3. L3 degraded · si `brand.creative_zone` absent → fallback `brand_personality` · confidence 0.6 · flag _gaps

Output state map + confidence_chain[] init avec valeur dépendante de density réelle.

Note · HR4.5 v2.36 reste opérante, le frontmatter prerequisites L2 est sa formalisation déclarative (cross-doc DRGFP cohérent).

---

## Step 0ter · Load canon copy (v2.26.0+, refacto v2.29.0)

> **Atlas refs** dans cette skill = atlas canon copy (sense 1, référentiel cross-brand doctrine copywriting). Brand-side enrichment via `validations[]` (sense 2 atlas vivant). Distinct de l'atlas brand (sense 4, cartographie holistique data brand) qui désigne la matière brand structurée navigable via `/phantom`. Pour la distinction lexicale complète : `lexicon.md § Atlas, 4 senses MECE`.

**Avant Step 1**, charger l'atlas canon copy comme bibliothèque de référence pour la production. Les angles ne sont plus générés depuis le néant, ils sont composés en piochant dans des outils canon référencés.

Read-only access aux fichiers `resources/canon/copy/{layer}/{tool}.json`. Couches utilisées par ce skill :
- `frameworks` (AIDA, PAS, BAB, QUEST, FAB, 4Ps) : squelette structurel
- `hooks` (curiosity-gap, contrarian, stat-choc, avant-apres, question-callout, confession) : ouverture
- `angles` (mecanisme-unique, identite, retour-en-arriere, ennemi-commun, status-shift, contre-intuitif) : axe narratif
- `niveaux-schwartz` (conscience, sophistication) : grille de pertinence · les 5 stages conscience canoniques sont définis dans `resources/schemas/_shared/awareness-stage.json` ($ref partagé v2.29.0), consommés via le field name `awareness_stage` (le terme Schwartz reste valide en surface opérateur, mais le field canonique est `awareness_stage`)
- `archetypes-voix` (caregiver, sage, rebelle, amante, heros, homme-ordinaire) : registre

Pour chaque outil canon lu, garder en mémoire : `id, when_works[], when_avoid[], combines_with{}`. Ces contraintes filtrent quels outils sont compatibles avec le contexte audience résolu en Step 0/1.

**Lecture batch.** `python3 .skills/phantom-canon.py copy {layer}` retourne la liste des outils d'une couche. Itérer pour charger les couches utilisées. Cache en mémoire pour la durée du run.

---

## Step 0quater · Régime + bibliothèques cross-brand (v1.12.0 · workflow A)

**Cadrage de batch.** Chercher le `frame.json` le plus récent sous `brands/{slug}/creatives/{batch}/frame.json` (ou celui passé en input par l'orchestrateur). S'il existe et date de moins de 7 jours :

- Lire `regime` (mode + freedom_cursor) et `rayon_max`. Le régime gouverne la PROVENANCE des angles : exploit = coller à la matière prouvée (atlas + patterns promus), explore = autoriser la re-dérivation depuis la banque de concepts.
- Le run devient un run cadré : l'output le mentionne en une ligne ("batch cadré en {mode}, curseur {x}") et le close chaîne vers le workflow A (voir Step 9).

S'il n'existe pas : run autonome, comportement identique aux versions antérieures. Ne JAMAIS exiger un cadrage pour produire des angles (la skill reste utilisable seule), mais si l'opérateur enchaîne visiblement vers de la production (demande un batch, des créas), proposer frame-regime en next-step.

**Bibliothèques cross-brand (lues dans tous les cas, filtrées par le rayon si cadré) :**

- `resources/registries/creative-mechanics-registry.md` · les 34 mécaniques ad-level (le CONCEPT, roi de l'image). Chaque angle candidat est mappé à sa mécanique dominante (`mecanique_id`), ce qui rend l'angle joignable au génome et à la perf en aval.
- `resources/registries/hooks/*.json` · patterns hook promote-ready (library-pattern, multi-source). En exploit : prioriser les patterns à `promotion.status: promote-ready` qui matchent la mécanique. En explore : ouvrir aux patterns watch avec flag.
- `resources/concepts/*.json` · banque de concepts (principes abstraits). Plancher de l'explore : on ne part JAMAIS d'une page blanche.

**Distance sectorielle (rayon, D#480).** Fonction de distance unique, définie dans `resources/sops/creative-production/cross-brand-curation.md` (source canonique de la fonction) : distance(item, marque) = 0 si la verticale de la marque ∈ `item.vertical_scope.origins` OU (`item.vertical_scope.breadth == "universal"` ET `item.promote_status == "promote-ready"`) · 1 si une origin est une verticale VOISINE de la marque · 2 sinon. Filtrer : distance <= rayon_max, lu depuis `frame.json#rayon_max` (persisté, jamais re-dérivé · 0 exploit, 1 balanced, 2 explore · rayon 2 par défaut si run non cadré, MAIS tout emprunt distance > 0 est alors surfacé). Chaque emprunt retenu est taggé `vertical_distance` + `distance_note` et SURFACÉ dans l'output opérateur comme pari conscient, jamais silencieux.

---

## Step 1 · Read encoded data (v1.10.0 ontologie sémantique pure)

Load the encoded substrate for this brand and this audience. Read silently · never narrate the loading.

**Sub-audience v2.64 (NEW · ontologie sémantique pure)** ·

- `brands/{slug}/audiences/{audience_slug}/pain_points/*.json` · pain canon entity owned natif par parent path (PNT-NN id, formulation, emotion, trigger, awareness_stage, verbatim_quotes[], severity, confidence_chain). Source de vérité pour `formula.tension.state_actual` + `formula.observation.phenomenon`. L'audience parente est implicite via path (pas de filter affected_audiences[] nécessaire).
- `brands/{slug}/audiences/{audience_slug}/objections/*.json` · objection canon entity owned natif (OBJ-NN id, formulation, type, response_counter, derived_angle_refs[], lifecycle_stage). Source de vérité pour `formula.tension.reason_blocked` + cells objection axis.

**Backward compat lecture (v2.63 brands)** · si `brands/{slug}/audiences/{audience_slug}/pain_points/` ET `brands/{slug}/audiences/{audience_slug}/objections/` n'existent pas, fallback top-level `brands/{slug}/pain_points/*.json` + `brands/{slug}/objections/*.json` filtered by `affected_audiences[]` contains `{audience_slug}`. Skill ne refuse jamais sur ce point, route transparent.

**Backward compat lecture (pre-v2.63 brands)** · si top-level v2.63 absent aussi, fallback `audiences/{audience-slug}/profile.json#pain_points[]` + `profile.json#objections[]` (legacy sub-fields v1.7).

**Audience profile (toujours lu)** ·

- `brands/{slug}/audiences/{audience-slug}/profile.json` · voice.key_expressions[] (with frequency / sample_size), psychology.jtbd (functional / emotional / social), market_position.awareness_dominant (RENAME C1 profile/2.3), demographics. **Note v2.64** · `pain_points[]` + `objections[]` sub-fields legacy preserved en lecture pour backward compat, mais sub-audience collections prennent priorité si présentes.
- `brands/{slug}/products/{product-slug}/spec.json` · problems_solved[].verbatim_quotes[], benefits[].chain (functional → emotional → identity), proofs.{social|authority|performance|scientific}, market_context.sophistication, identity.
- `brands/{slug}/products/{product-slug}/offers.json` · active offers, urgency flags, bundle structure, subscription presence (informs offer-led angle activation).
- `brands/{slug}/brand.json` · tone_of_voice, market.* if VoM has run (vernacular, sophistication_stage, awareness_distribution, white_spaces, external_intelligence).
- `brands/{slug}/strategy.json#current_focus` · acquisition_focus when encoded (awareness lens weight signal).
- Optional: `brands/{slug}/learnings.json` · past angle patterns (winners, killed, recurring objection-proof pairings).

**Verbatim density floor check.** Count `voice.key_expressions[]` entries with sample_size populated AND total `verbatim_quotes[]` across `pain_points` and `problems_solved`. If `voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5 → flag thin corpus. Surface to the operator before producing: *"La voix client est trop fine pour ranker proprement · j'ai 2 verbatims sur la pain principale, je sortirais des angles inférés à 80%. Le move qui paie c'est de runner mine-voc d'abord, ~20 min, et on revient avec des angles ancrés. Sinon je peux quand même produire en flaguant chaque hook inféré."* Default behavior: pause unless operator forces.

---

## Step 2 · Resolve placement context

Read `operator/profile.json#context.stack[]` (captured pre-snapshot per cascade C v2.8). Derive active placements from the stack:

- **Meta in stack** → Reels, Stories, Feed UGC eligible.
- **TikTok in stack** → TikTok organic / paid eligible.
- **Google in stack** → Search, Display eligible (filter applies · Search only for solution-aware+, Display for problem-aware).
- **Pinterest in stack** → Pinterest eligible (lifestyle / aspiration verticals).

If operator stack signals only Shopify + Klaviyo (no paid platform), warn explicitly: *"Ton stack capté ne flag aucune plateforme paid active. Une matrice paid perd sa relevance là · le move utile c'est sûrement un brief copy email ou landing à la place. Tu veux que je pivote sur `produce-copy-brief` pour ton flow Klaviyo, ou tu confirmes que tu actives Meta/TikTok bientôt et je reste sur paid ?"*

Default placement scope when stack is silent: Reels / Stories / Feed UGC / TikTok · the four DTC paid placements with highest current leverage.

---

## Step 3 · Select active dimensions

Not a fixed list. The selection adapts to what is encoded densely on this brand. Pick 4-5 dimensions max from the candidate set below, applying the activation rule per dimension and the cap rule overall.

**Always active when encoded:**
- `pain.formulation` (from `pain_points[]`)
- `objection.formulation` or `objection.type` (from `objections[]`)

**Often active:**
- `pain.emotion` or `JTBD.emotional` (emotional dominant)
- `audience.awareness_stage` (if encoded with cross-source consistency)

**Sometimes active:**
- `placement` (when multi-platform stack · single-platform stack drops this dimension since placement is fixed)
- `product.proof.type` (when `proofs.*` carries 2+ varied types · single-proof brand locks this dimension to dominant proof, no axis variation)
- `offer.urgency` or `offer.type` (when operator query is offer-led · *"angles pour la promo BFCM"* boosts these into active set)
- `brand.market.vernacular` (when VoM has run, raises hook quality)
- `mecanique` (v1.12.0 · concept ad-level du creative-mechanics-registry · active quand le run est cadré par un frame.json OU quand l'opérateur vise explicitement de la production créa · chaque cellule porte alors un `mecanique_id` candidat, joignable au génome et à la perf en aval)

**Hard cap: 5 dimensions max.** Beyond 5, cartesian explodes (5×4×3×3×2 = 360 cells) and signal dilutes per scoring framework anti-pattern. The agent picks the 4-5 highest-density dimensions for THIS brand and THIS query, never defaults to a fixed list.

The selection rationale lives in the Layer A trace, never in operator output.

---

## Step 4 · Generate cartesian product (INTERNAL)

Iterate over the active dimensions, build all combinations. Internal data structure only. Never mentioned in operator output. Never logged in a way the operator can stumble on (Layer A trace only).

Typical sizes:
- Well-encoded brand, 4 dimensions active: 4 pains × 3 objections × 3 emotions × 2 placements = 72 cells.
- Thin brand, 2 dimensions active: 3 pains × 2 placements = 6 cells.

Cell shape (internal):
```
{ pain_id, objection_id, emotion, placement, awareness_stage, ... }
```

---

## Step 5 · Score each cell per framework

Apply `resources/frameworks/paid-angle-scoring.md` lens by lens:

- **Verbatim density (35%, dominant).** Exact match in `voice.key_expressions[]` with `sample_size ≥ 5` → maximum. Semantic match in `verbatim_quotes[]` with high emotional weight → strong. No anchor, formula-derived only → low (cell survives only if no grounded alternative in cluster).
- **Emotional resonance (20%).** Cell emotion alignment with `audience.psychology.jtbd.emotional_driver` and `psychology.emotions[]` dominant.
- **Objection neutralization (20%).** Cell objection × `product.proofs.*` strength match per `proof-registry.md` mapping. Clinical trial neutralizes scepticism, risk-reversal neutralizes price hesitation, press quote neutralizes trust gap. Unmapped objection → flag un-neutralizable, drop cell.
- **Placement viability (binary filter, not weight).** Cell hook length and format constraint per placement. Reels = 3s pattern interrupt. Stories = swipe-up curiosity. Feed UGC = identification. TikTok = native vernacular. Fail = drop cell. Pass = neutral (no point bonus).
- **Awareness alignment (25%).** Cell awareness stage × `brand.json#market.awareness_distribution` (or audience-level fallback) × `strategy.json#current_focus.acquisition_focus`. Cross-reference `routing/awareness-angle-matrix.md` to filter angles in the "avoid" column for the dominant awareness stage.

Composite score 0-100. **Never exposed to the operator.** Never written to the operator-facing artifact. Lives in Layer A trace only.

---

## Step 6 · Cluster filter de-dupe

Two cells are "similar" when they share: same dominant pain (theme + emotion) AND same dominant objection AND same placement. Keep the highest-scored cell per cluster, drop the rest.

The output table never contains two rows saying the same thing differently. If the operator sees five rows, the angles cover five distinct positions in the audience-objection-emotion space, not five paraphrases of the same insight.

When two cells differ only on placement (same pain + same objection + same emotion, Reels vs Stories), surface as ONE angle with two placement variants in the artifact footnote, NOT two separate rows.

---

## Step 7 · Rank and cap

Rank surviving cells by composite score descending.

Cap rules:
- **5 angles by default.** This is the scannable ceiling for an operator briefing a copywriter.
- **Up to 7 angles** when the top 3 cells score above the high-density threshold defined in `paid-angle-scoring.md` AND the operator stated a wide-test objective (*"je lance un test large"*, *"vague d'ouverture"*, *"sortir 7 angles à tester"*).
- **Below 5 angles** only when the corpus is genuinely thin and the synthesis explains why in prose. Never silently ship 3 angles when 5 were expected · name the corpus thinness.

---

## Step 8 · Verbatim anchor selection per ranked cell

Per scoring framework Section 4, for each ranked cell, select the hook anchor in this priority:

1. **Exact verbatim match** from `voice.key_expressions[]` with `sample_size ≥ 5` and high emotional weight. Highest priority. The hook IS the verbatim or a 2-4 word adaptation of it.
2. **Semantic verbatim match** from `pain_points[].verbatim_quotes[]` or `problems_solved[].verbatim_quotes[]` with strong emotional anchor. The hook adapts the verbatim while preserving the customer voice signature.
3. **Hook formula** from `resources/templates/hook-formulas.md` matched to the cell's awareness stage, when no verbatim is available. The Layer A trace flags this cell with `(formulation type, no direct customer voice)`. In operator output, the hook ships with no anchor mention · internal sourcing stays internal.
4. **Never invent a quote attributed to customers.** Never paraphrase a verbatim and present it as if it were a real customer quote. Either real or formula-flagged. The trust contract is non-negotiable.

Each shipped hook passes the `resources/quality-specs/hook-quality-spec.md` 5-criterion test (Pattern Interrupt, Identification, Open Loop, Spécificité, Awareness Match) at threshold ≥ 4/5. Hook below 4/5 → either retry once with a different anchor or drop the cell entirely. The skill does not negotiate on hook quality.

---

## Step 9 · Operator-facing output (synthesis + table + close drill-down, v2.54)

Apply snapshot-brand Step 7 v2.54 doctrine investigation-posture STRICTLY. Angles dérivent d'hypothèses (audience source, brand source) · leur confidence chain est héritée, doit être visible en surface, jamais cachée.

### Confidence chain inheritée (v2.54 NEW)

Pour chaque angle, le skill calcule la confidence agrégée selon · 

**`derived_from_audience_confidence`** · héritée du `profile.json#meta.validation_status` de l'audience source · si audience portée comme hypothèse `TRÈS faible` (zéro mining) → propagation `TRÈS faible`. Si audience portée `moyenne` ou `forte` (mine-voc tourné, verbatim_density >= 5) → propagation niveau correspondant.

**`derived_from_brand_confidence`** · héritée du `brand.json` état Observé/Déduit selon doctrine investigation-posture · sourcing direct du scrape (positioning revendiqué site, tone of voice direct) = `forte` · inférence agent (sophistication estimée, market position déduit) = `moyenne` ou `faible`.

**`claim_confidence`** · agrégat = MIN des deux héritages (algèbre conservative cross-skill, per `docs/system/confidence-propagation.md`). Un angle ne peut pas être plus fiable que l'audience ou la brand sur laquelle il est dérivé.

Persister dans Layer A trace + dans `angles/{ANG-N}.json#lineage` (nouveaux fields v1.3 schema).

### Synthesis paragraph (3-5 sentences, prose-first, posture analyste)

Ce qui rend les top angles load-bearing pour cette audience et cette brand. Ce qui sépare les top 2 du reste du ranked set. **La confidence chain en signal explicite** · si l'audience source est hypothèse `TRÈS faible` (pas de mine-voc), le synthesis le dit clairement · *"Ces 5 angles dérivent d'une audience portée en hypothèse intuition (zéro verbatim client mining-sourced), ils sont à tester avec budget calibré, pas à scaler avant validation terrain."* Si audience est `forte` (mine-voc dense + analytics convergents), le synthesis le dit aussi · *"Audience source validée terrain (mine-voc sur 28 verbatims), angles 1-3 ancrés direct sur expressions clientes."*

**Hard rules synthesis** ·
- Posture analyste, pas marketer. Pas de copywriting narratif déguisé en analyse (anti-pattern AP-3 doctrine).
- Mentionne EXPLICITEMENT la confidence chain inheritée dans la prose (1 phrase au minimum).
- Si claim_confidence `TRÈS faible` ou `faible` agrégé → signal explicit "à tester sur budget calibré, pas à scaler".
- JAMAIS exposer scores numériques, JAMAIS lister "5 dimensions analyzed", JAMAIS mention cartesian / clustering / framework names.
- Inférés flag inline (*"à valider, pas de verbatim direct"*) selon HR4.5 v2.36 gate.

### Ranked table (markdown, 6 ou 7 colonnes v2.54)

Headers · `# / Angle / Hook / Émotion mobilisée / Objection neutralisée / Placement reco / Confiance`

Each row ·
- `#` · rank position (1, 2, 3...).
- `Angle` · operator-language, evocative, 2-3 words. *"Miroir post-grossesse"*, *"Ras-le-bol des régimes"*, *"Verdict balance"*. Anchored in the dominant verbatim cluster of the cell. Maps to `angle-registry.md` taxonomy when a registry entry fits, brand-specific naming when it does not.
- `Hook` · verbatim-anchored where possible (in quotes), or formula-derived (no quotes, no anchor mention).
- `Émotion mobilisée` · 1-2 plain words. *"Identitaire"*, *"Délivrance"*, *"Soulagement"*, *"Frustration accumulée"*. Never `emotional_driver:identity`.
- `Objection neutralisée` · 1-line, verbatim-anchored when possible (in quotes from `objections[].formulation`).
- `Placement reco` · 1 word. *"Reels"*, *"Stories"*, *"Feed UGC"*, *"TikTok"*. Never `awareness_stage:problem-aware|placement:reels` jargon.
- **`Confiance` (v2.54 NEW)** · `claim_confidence` agrégée en qualitatif (`forte / moyenne / faible / TRÈS faible`) + 1-mot motif source si pertinent. Exemples · *"forte"*, *"moyenne"*, *"faible (hérite audience hypothèse)"*, *"TRÈS faible (audience non-validée)"*.

**Cap** · 5 rows by default, 7 when signal density justifies. Below 5 only when corpus thin and synthesis explains why.

**Banned** · column headers in jargon, cells with internal labels, scores numériques in any column, field paths anywhere.

**Format ligne enrichi v2.54 (operator-facing)** ·

```
| # | Angle | Hook | Émotion | Objection | Placement | Confiance |
| 1 | Miroir post-grossesse | "Je ne pouvais plus voir mon reflet" | Identitaire | "J'ai déjà tout essayé" | Reels | moyenne (audience mine-voc partiel) |
| 2 | Ballonnement permanent | "Toujours ballonnée, le ventre gonflé même à jeun" | Inconfort | "Trop cher pour 1-3 kg" | Stories | forte (verbatim direct) |
| 3 | Ras-le-bol des régimes | "Frustration, échec, culpabilité, la boucle" | Délivrance | "C'est juste du marketing" | Feed UGC | moyenne |
| 4 | Verdict balance | "Le moment où tu montes et tu sais déjà" | Anticipation négative | "Ça marche pour les autres" | Reels | faible (formula-derived) |
| 5 | Confiance retrouvée | "Remettre la robe rangée il y a 2 ans" | Aspiration | "Je vais reprendre après" | TikTok | TRÈS faible (audience non-validée) |
```

### Encart pivot audiences (v1.7.0 NEW)

Après le ranked table, avant le close drill-down, insérer un encart court qui matérialise la capacité de pivoter sur d'autres audiences cartographiées de la brand. Scan `brands/{slug}/audiences/*/profile.json` (exclusif audience source actuelle), surface les 3-5 autres audiences candidates avec leur `identity.label` operator-language.

Format encart ·

```
Pour pivoter sur une autre audience cette brand · relance avec ·
- {audience_label_2} ({audience_slug_2}) · {dominant_pain_extract_short}
- {audience_label_3} ({audience_slug_3}) · {dominant_pain_extract_short}
- {audience_label_4} ({audience_slug_4}) · {dominant_pain_extract_short}

Audience absente du listing ? `mine-audience` pour la cartographier d'abord, ou `profile-audience` pour la coder à la main.
```

**Hard rules encart** ·
- Surface uniquement si 2+ autres audiences existent dans `brands/{slug}/audiences/`. Si solo audience brand, encart skipped (pas de pivot disponible).
- Cap 5 audiences max pour scannabilité. Au-delà, "et N autres audiences cartographiées" hint.
- Operator-language labels (`identity.label`), jamais slugs purs ou JSON paths.
- Couvre le pattern Notion zone 3→4 filter-by-persona observé workspace stride-up (Décision v2.56 routing systémique).

### Close · verdict de move (affirme / ouvre / gate)

Le verdict de move n'est pas PRESCRIT par la forme · il est PRODUIT en raisonnant sur le substrat encodé. Fais tourner la chaîne diagnostique experte sur le set ranked + la confidence chain héritée · position → négatif → audience-du-mécanisme → priorité-éco → verdict (`docs/doctrine/strategic-diagnostic-doctrine.md`) · le move sort de cette lecture croisée, pas d'une checklist. Posture du close, ordre de priorité affirme/ouvre/gate · SSOT `docs/system/investigation-posture.md` + master `docs/system/contextual-intelligence.md` (ne pas re-coller le contrat ici). Le move s'appuie sur un déduit qui porte sa confidence, il ne l'invente jamais.

**L'out honnête** · si la data ne porte pas encore de move (ex deux lectures opposées également plausibles sur la source), ne fabrique pas un verdict pour faire décisif · nomme LA seule inconnue qui bloque et le chemin exact pour la lever (ex ~8-12 min d'écoute clients pour ancrer les angles formula-derived et re-ranker). « Je ne tranche pas sans X, voilà comment on a X » est un move, pas un cop-out.

**Self-critique avant de rendre le close** · relis-le contre affirme/ouvre/gate · tranche-t-il un move défendu, ou décrit-et-rend-il une question ? Bulletin météo (état + menu d'axes · *"lequel veux-tu creuser ?"*) → réécris en verdict de move.

**Exemplar** · `resources/canon/exemplars/close.md` avant de rendre · le noticing (ce que l'expert a vu de non-évident), l'out honnête, et la paire sharp vs mushy.

Le drill-down macro reste une AFFORDANCE de redirection trailing (tester direct vs upgrader la source d'abord), jamais le défaut · le close tranche. L'agent enchaîne ensuite sur le move affirmé (silencieusement vers produce-copy-brief par défaut, ou mine-voc si la route upgrade est prise) · si l'opérateur redirige, il bascule, mais le close part affirmé.

**Run cadré (v1.12.0 · frame.json présent)** · trois ajouts au rendu, rien d'autre ne change ·

1. **Perspectives POV (A5)** · chaque angle top-ranked porte 3 incarnations narratives : fondateur (parole de marque), client (témoignage première personne), expert tiers (autorité neutre). Même angle, trois voix · jamais présentées comme trois angles distincts. Une ligne par POV sous l'angle dans la table.
2. **Dérivation des concepts candidats (réceptacle gate concepts)** · regrouper les angles top-ranked par principe abstrait : un concept = un principe détaché de la formulation. Chaque concept candidat porte `{concept_id: "CPT-NN", principle, angle_refs[], applicable_mechanics (mecanique_id du creative-mechanics-registry), vertical_scope hérité des emprunts, status: "candidate"}` · 2 à 4 concepts par batch typique. Allocation `CPT-NN` = scan du max existant dans `brands/{slug}/creatives/{batch}/concepts/` + 1. Écrire chaque concept via `python3 .skills/write-to-context.py --path "brands/{slug}/creatives/{batch}/concepts/CPT-NN.json" --value '{concept JSON}' --mode direct --source agent --reason "Concept candidate derived from top-ranked angles (run cadré)"`. Ces fichiers sont le réceptacle unique que le gate concepts (evaluate-concept) évalue ensuite · les verdicts sont retournés au flux appelant qui les persiste dans chaque fichier CPT (champ `evaluation`).
3. **Close chaîné workflow A** · le close drill-down propose en option A' la suite du flux cadré : *"le batch est cadré en {mode} · la suite naturelle, c'est le gate concepts puis le tissage des scripts"* (verbalisé métier, l'agent route vers evaluate-concept, qui juge les `concepts/CPT-NN.json` écrits au point 2, puis weave-hooks). Les emprunts cross-verticale retenus (distance > 0) sont rappelés dans le close comme paris à arbitrer au gate.

---

## Step 10 · Layer A scoring trace

Write to `brands/{slug}/sources/produced-angles/{YYYY-MM-DD}/scoring-trace.jsonl`. One line per cell scored. Audit substrate, never auto-loaded into context, never surfaced unless the operator asks *"pourquoi cet angle ranke premier"*.

Trace inclut (v2.54) la confidence chain inheritée par angle ·

```json
{
  "id": "PA-001",
  "run_id": "pa-2026-04-24-001",
  "produced_at": "2026-04-24T14:32:00Z",
  "audience_anchor": "femmes-30-55-minceur",
  "audience_source_confidence": "forte",
  "brand_source_confidence": "forte",
  "dimensions_active": ["pain.emotion", "objection.type", "placement"],
  "cartesian_size": 72,
  "filtered_to": 8,
  "clustered_to": 5,
  "ranked_top": [
    {
      "rank": 1,
      "angle_name": "Miroir post-grossesse",
      "score": 87,
      "verbatim_anchor_id": "VOC-trustpilot-7a2x",
      "anchor_type": "exact_match",
      "derived_from_audience_confidence": "forte",
      "derived_from_brand_confidence": "forte",
      "claim_confidence": "forte"
    }
  ],
  "scoring_breakdown_per_cell": [...]
}
```

**Calcul `claim_confidence` (v2.54 algèbre conservative cross-skill)** ·

```python
def aggregate_claim_confidence(audience_conf, brand_conf, anchor_type):
    levels = ["TRÈS faible", "faible", "moyenne", "forte"]
    aud_idx = levels.index(audience_conf)
    brand_idx = levels.index(brand_conf)
    base = levels[min(aud_idx, brand_idx)]
    
    # Anchor type modulator (formula-derived downgrade 1 level if claim > faible)
    if anchor_type == "formula_derived" and levels.index(base) > 1:
        base = levels[levels.index(base) - 1]
    
    return base
```

Un angle ne peut pas être plus fiable que l'audience ou la brand sur laquelle il est dérivé (algèbre conservative, anti-pattern AP-1 doctrine évité).

The trace is queryable post-hoc. It is the proof that no verbatim was fabricated, the substrate for the next pass to learn from this run, and the audit trail when angle quality is challenged downstream.

---

## Step 11 · Layer B operator artifact

Write the synthesis + ranked table as markdown to:

`brands/{slug}/produced/paid-angles/{YYYY-MM-DD}-{audience-slug}.md`

Pure deliverable. Copy-pasteable into Notion, Slack, a Google Doc, a brief sent to a copywriter. Header carries: brand name / audience label / date / angle count. Body carries the synthesis paragraph and the ranked table. Footer carries the citations row when verbatims were used (verbatim IDs referencing the original `voc/` corpus when relevant) · never inline scores, never field paths.

**Canon lineage block (v2.26.0+, refacto v2.29.0).** Chaque angle dans le ranked table porte son lignage canon explicite. Format ligne par angle :

```
ANG-{N} · {angle name}
  audience          {audience_slug}
  awareness_stage   {awareness_stage}       ← _shared/awareness-stage.json (5 stages canon)
  sophistication    {schwartz_sophistication wave v1-v5}
  hook              {hook_canon_id}         ← canon copy hooks
  framework         {framework_canon_id}    ← canon copy frameworks
  angle narratif    {angle_canon_id}        ← canon copy angles
  archetype voix    {archetype_canon_id}    ← canon copy archetypes-voix
  pain cible        {pain_extract from VoC}
  proof primary     {proof_primary from spec}
  CTA               {cta or "à créer"}
```

En surface opérateur (rendu human-readable), le terme *Schwartz* reste recevable comme référence auteur (*"Schwartz conscience: solution-aware"*). Le field name canonique côté schema/JSON est `awareness_stage`. Le lignage rend l'angle **traçable** : `/phantom {brand_slug} angles ANG-03` pourra rendre la chaîne compositionnelle lue à travers l'atlas. C'est aussi ce qui débloquera les vues `copy-matrix` et `copy-map`.

**Persistence brand-side (angle.schema v1.3+).** Le lignage canon est ALSO écrit dans `brands/{slug}/angles/{ANG-N}.json` aligné sur `angle.schema.json` v1.3 (NEW v2.63 · pain_ref + objection_ref canonical refs), enrichi v2.54 avec confidence chain inheritée ·

```json
{
  "_schema_version": "angle/1.6",
  "angle_id": "ANG-NN",
  "name": "...",
  "audience_slug": "...",
  "origin_axis": "audience-derived | product-derived | category-derived | brand-derived | temporal-cultural",
  "awareness_movement": { "in": "...", "out": "..." },
  "lineage": {
    "awareness_stage": "...",
    "schwartz_sophistication": "v1-v5",
    "hook_canon_id": "...",
    "framework_canon_id": "...",
    "angle_canon_id": "...",
    "archetype_canon_id": "...",
    "pain_extract": "...",
    "pain_ref": "PNT-NN | null (NEW v1.3 v2.63 · canonical ref si pain sourcé pain_points/PNT-NN.json)",
    "objection_ref": "OBJ-NN | null (NEW v1.3 v2.63 · canonical ref si objection sourcée objections/OBJ-NN.json)",
    "proof_primary": "...",
    "cta": "...",
    "derived_from_audience_confidence": "forte | moyenne | faible | TRÈS faible",
    "derived_from_brand_confidence": "forte | moyenne | faible | TRÈS faible",
    "claim_confidence": "forte | moyenne | faible | TRÈS faible"
  },
  "formula": { "observation": {}, "tension": {}, "reframe": {}, "bridge": {} },
  "negative": { "summary": "l'alternative déplacée (1 ligne)", "type": "competitor | category-belief | status-quo | substitute | diy | do-nothing", "spectrum_cell_ref": "SPC-NN | null (le négatif concurrentiel sourcé du Spectre)" },
  "insight": { "modalite": "formulé | implicite | absent", "status": "déduit | validé | incertain", "formulation": "..." },
  "meta": { "validation_status": "hypothesis", "created": "YYYY-MM-DD" }
}
```

Les 3 fields `derived_from_audience_confidence`, `derived_from_brand_confidence`, `claim_confidence` (v2.54 doctrine investigation-posture) permettent au downstream `/phantom {brand_slug} angles ANG-NN` de rendre l'angle avec sa fiabilité héritée explicite, et à `produce-copy-brief` d'hériter à son tour la confidence chain dans le brief créa downstream.

**NEW v1.13.0 · coordonnée NÉGATIF (D#523).** Un angle est un pari sur le chemin de croyance le plus court, défini par 5 coordonnées dans l'ordre canon · (1) l'entrée (`awareness_movement`), (2) le moteur désir-douleur (`lineage.pain_ref` + `formula.tension`), (3) la source de croyance (`lineage.proof_primary` + `origin_axis`), (4) le NÉGATIF (`negative` · l'alternative que l'angle déplace), (5) le RECADRAGE (`formula.reframe`). Le négatif nomme la CIBLE du recadrage · sans lui, l'angle affirme une promesse sans déloger l'option en place (le concurrent, la croyance de catégorie, le statu quo, le renoncement). Le peupler dès le light pass (`summary` + `type`) · le négatif concurrentiel vient souvent d'une cellule du Spectre, traçable via `negative.spectrum_cell_ref` (le pont carte→négatif · cf `docs/doctrine/angle-strategy-doctrine.md`). Filet · `validate-all` advise en LOW un angle qui a un reframe SANS négatif (`angle_negative_missing`) et vérifie post-hoc en MED qu'un `spectrum_cell_ref` présent résout (`angle_negative_untraced`) · JAMAIS un gate au write (le choix de quoi déplacer = jugement stratégique, trust the model · Master rule).

**NEW v1.9.0 · pain_ref + objection_ref canonical population.** Lors de l'écriture `angles/{ANG-NN}.json` v1.3, si la cellule top a un `pain_id` (PNT-NN) ou `objection_id` (OBJ-NN) mappable depuis Step 1 collections top-level read · populer `lineage.pain_ref` + `lineage.objection_ref` avec les canonical IDs. Sinon (cellule formula-derived, ou pre-v2.63 brand avec lecture fallback profile sub-fields), laisser null + garder `pain_extract` text legacy comme fallback. Cohérent triangulation cross-canon avec downstream (`decompose-angle` v1.1+ peut désormais re-triangulate atom-level depuis canonical refs).

Renommages v2.29.0 : `source` (top-level) devient `origin_axis` · `lineage.schwartz_conscience` devient `lineage.awareness_stage`. Le field `awareness_stage` consomme l'enum canonique de `_shared/awareness-stage.json` (5 stages).

**Fields migrés vers creative.schema.json v1.1 (drop ici).** Les fields `intent`, `mecanique`, `seasonality_trigger`, `execution.craft_mode`, `execution.longevity_signal`, `execution.cta` ont été migrés de `angle.schema` vers `creative.schema` (7ème entité brand) en v2.29.0. **NE PAS les écrire dans `angles/{ANG-N}.json`.** Si le skill veut produire une créa instance complète (concept × execution), invoquer le skill `compose-creative` (futur v2.31+) ou écrire directement `brands/{slug}/creatives/{CREA-N}.json` aligné sur `creative.schema.json` v1.1, qui absorbe execution + classification + variant_of et référence l'angle parent via `variant_of.angle_id`.

Permet aux outils downstream (`/phantom {brand_slug} angles ANG-03`, `produce-copy-brief ANG-03`) de relire la composition.

The next-step proposal lives in the conversational reply, NOT in the artifact file. The artifact is the pure deliverable; the conversational reply carries the reasoned next move.

---

## Step 11bis · Back-refs auto-persist (v1.8.0, v2.58 coverage extend)

**Append-only additive coverage.** Trois orphans audit v2.57 fermés par back-refs auto-persistées **post-Step 11 artifact write, pre-Step 12 finalize**. Patches NE remplacent PAS la production angles ranked, ils ENRICHISSENT le graph audience↔angle pour rendre la fiche audience drillable downstream (`/phantom {brand_slug} audiences {a_slug}` rendra les objections avec leur response_counter + derived_angle_refs[]).

**Backward compat strict** · si l'objection traitée n'existe pas dans `profile.json#/objections` (cas où l'angle a été généré sur un objection_id absent du profile, ex pivot audience), skip silencieusement le back-ref P4/P5. Si pas de pivot audience triggered (encart v1.7.0 non utilisé), skip P6. Aucun blocking, aucun refus de ship.

### P4 · objections.response_counter back-ref (v1.10.0 sub-audience canonical)

Quand `produce-paid-angles` génère un angle qui exploite une objection (via `formula.tension` mappée à OBJ-NN canonical depuis `audiences/{a_slug}/objections/*.json` sub-audience), persist back-ref · l'objection traitée reçoit `response_counter` = la formulation neutralization de l'angle généré (extraite de `formula.reframe.text`).

Pour chaque angle ranked dans le top output (5 par défaut, jusqu'à 7), si la cellule a un `objection_id` (OBJ-NN) mappable à `audiences/{a_slug}/objections/*.json` ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json#/response_counter" --value "{angle.formula.reframe.text}" --source agent --confidence 0.8 --mode proposed --reason "Back-ref auto from produce-paid-angles run"
```

Le `response_counter` rend la fiche objection opérable downstream · l'opérateur qui drill `audiences/{a_slug}/objections/{OBJ-NN}` voit non seulement la formulation mais aussi la neutralization formula que les angles ont déjà cristallisée. Évite re-générer un counter from scratch pour `produce-copy-brief` ou objection-handling email flows.

**Backward compat (v2.63 brands)** · si `audiences/{a_slug}/objections/{OBJ-NN}.json` n'existe pas (sub-audience non-shipped), fallback top-level `objections/{OBJ-NN}.json` v2.63. Si top-level absent aussi, fallback path legacy `audiences/{a_slug}/profile.json#/objections/{idx}/response_counter` (sub-field profile v1.7). Lookup `{idx}` via match `objections[].formulation` from profile sub-array. Skip silencieusement si zéro match.

**Anti-pattern banni** · écraser un `response_counter` existant si l'objection a déjà été traitée par un angle antérieur (validation_status >= validated). Le mutation gate `write-to-context.py` mode proposed surface conflict si collision · operator arbitre.

### P5 · objections.derived_angle_refs[] + pain_points.derived_angle_refs[] back-refs (v1.10.0 sub-audience canonical)

Pour la même objection traitée par un angle, append `derived_angle_refs[]` avec l'`ANG-NN` id (append-only, jamais overwrite). Permet à la fiche objection canonique de remonter tous les angles dérivés (1-N relation).

**Stage append-only objections sub-audience** ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json#/derived_angle_refs" --value '["ANG-{NN}"]' --source agent --confidence 1.0 --mode proposed --reason "Back-ref ANG-NN derivation"
```

**v1.10.0 · pain_points.derived_angle_refs[] back-ref sub-audience** · si l'angle a `lineage.pain_ref` populé avec un PNT-NN canonical (Step 11 angle.json v1.3 write), append symétrique sur la fiche pain sub-audience ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json#/derived_angle_refs" --value '["ANG-{NN}"]' --source agent --confidence 1.0 --mode proposed --reason "Back-ref ANG-NN pain source"
```

Si pain est observation source de l'angle (formula.observation.phenomenon ancré sur un PNT-NN canonical), le back-ref permet à la fiche pain de remonter tous les angles construits sur ce pain. Symétrie complète audience↔pain↔objection↔angle graph navigable.

Le mutation gate handle l'append (si `derived_angle_refs[]` existe → append le nouveau ANG-NN ; sinon initialize l'array avec [ANG-NN]).

**Backward compat (v2.63 brands)** · si `audiences/{a_slug}/objections/{OBJ-NN}.json` ou `audiences/{a_slug}/pain_points/{PNT-NN}.json` n'existent pas sub-audience, fallback top-level `objections/{OBJ-NN}.json` + `pain_points/{PNT-NN}.json` v2.63. Si top-level absent aussi, fallback path legacy `audiences/{a_slug}/profile.json#/objections/{idx}/derived_angle_refs` (sub-field profile v1.7). Si zéro pain canonical PNT-NN ref dans angle.lineage, skip pain back-ref entirely.

Couvre le pattern Notion zone 3→4 reverse (depuis pain ou objection canonique, voir tous les angles que la matrice paid a produits sur cette pain-objection pair). Dual-direction du encart pivot v1.7.0 (depuis angles, voir autres audiences).

### P6 · angle.compatibility[] cross-audience persist

Quand l'opérateur trigger pivot audience via l'encart v1.7.0 (Step 11 artifact mentionne *"Pour pivoter sur une autre audience cette brand · relance avec {audience_slug_other}"*) et que le pivot run produit des angles compatibles avec multiple audiences, persist `angle.compatibility[]` entry sur chaque ANG-NN cross-applicable ·

Pour chaque angle dans le ranked output qui matche aussi une audience autre que la source (semantic match sur pain dominant + verbatim convergence), stage ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/angles/{ANG-NN}.json#/compatibility" --value '[{"audience_slug":"{other_aud}","fit":"yes","notes":"..."}]' --source agent --confidence 0.7 --mode proposed --reason "Cross-audience pivot persist"
```

Schema entry `compatibility[]` ·

```json
{
  "audience_slug": "string (slug audience cousine)",
  "fit": "yes | no | partial",
  "notes": "string (1 phrase · pourquoi fit yes/no/partial · ex 'pain identique mais objection prix moins saliente sur cette audience')"
}
```

- `fit: yes` · angle directement réutilisable sur l'audience cousine sans modif (verbatim density + objection match)
- `fit: partial` · angle réutilisable avec adaptation hook (pain match mais verbatim audience-specific à swap)
- `fit: no` · angle non-applicable (pain ou objection divergent)

L'opérateur qui drill `/phantom {brand_slug} angles ANG-NN` voit la matrice de compatibility cross-audience, déclenche re-test sur audience cousine sans re-mining si `fit: yes`. Économise le cartesian re-run.

**Anti-pattern banni** · auto-tagger `fit: yes` sur toute audience cousine sans cross-product check (pain match ET objection match ET verbatim convergence). Default safe = `fit: partial` si signal mixte, `fit: no` si divergent.

**Surface operator** · cette persistence reste INTERNE (jamais exposée brute en Step 9 output table). Le ranked table garde `Confiance` colonne v2.54. Les `compatibility[]` enrichissent le graph brand-side, lus par `/phantom` rendering downstream.

---

## Step 12 · Finalize

Mandatory before shipping the operator-facing summary:

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mechanical Python primitive. Inspects every mutation written in this run (Layer A trace, Layer B artifact, optional learnings append), runs structural checks, emits a `coherence_check` event so `turn-end-audit` sees the loop closed.

Exit code 2 = blocking issue → revise before shipping. Exit code 0 with warnings = log them, ship. **Non-negotiable, mechanical, not skippable.**

---

## Step 12ter · Persist the recommended next-step (v1.12.1, additif strict)

Le close drill-down (Step 9) propose un next-step en clair · il vit dans la réponse conversationnelle. Mais une reco qui ne vit que dans le chat meurt au prochain tour. Ce step lui donne une **trace persistante** · une ligne dans la todo de la brand, sans rien retirer du close in-line, qui reste tel quel.

Pattern déjà prouvé par `register-and-flag` Step 6 (write idempotent d'une ligne de tracking dans `brands/{slug}/todos.md`). On le réapplique au next-step produit.

**Geste** · après Step 12 (finalize OK), écrire une ligne unique dans `brands/{slug}/todos.md → ## In Progress` au **format de ligne canonique** ·

```
- [ ] {Name} | P: {0-3} | E: {low|med|high} | T: {durée}
```

- `Name` · le next-step recommandé verbalisé court, dérivé du move A du close (ex `produce-copy-brief sur l'angle #2 Ballonnement`, `mine-voc pour upgrade audience source avant scale`). Operator-language, pas de slug pur sauf nom de skill aval.
- `P` · priorité dérivée de la confiance · claim_confidence majoritairement `forte` et reco = production downstream → `P: 1` · reco = upgrade substrat (mine-voc) parce que corpus thin → `P: 1` aussi (bloquant qualité) · reco secondaire / variant → `P: 2`.
- `E` · effort du skill aval (low pour un brief ciblé, med pour un mine-voc, high pour un re-mining large).
- `T` · ETA verbalisé du skill aval (ex `15 min`, `demi-journée`), aligné `feedback_client_effort_scale` si client-facing.

**Idempotence (dure, comme register-and-flag).** Avant d'écrire, scanner `## In Progress` · si une ligne porte déjà le même `Name` (même skill aval + même cible), **ne pas dupliquer**. Re-run du même skill sur la même brand/audience = zéro nouvelle ligne. Le write passe par le mutation gate ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/todos.md#in-progress" --value "- [ ] {Name} | P: {n} | E: {level} | T: {eta}" --source agent --mode direct --reason "Persist recommended next-step from produce-paid-angles close (idempotent)"
```

Si `write-to-context.py` ne route pas le markdown todos, fallback `register-and-flag` (sous-skill curator) en lui passant l'entry · même réceptacle, même idempotence. Ne JAMAIS hand-editer le markdown hors gate.

**Auto-tick aval.** La ligne est cochée `[x]` automatiquement quand le skill aval nommé tourne et produit son artifact · `produce-copy-brief` (et tout producer aval) lit `## In Progress` à son finalize, matche une ligne dont le `Name` le désigne comme skill aval avec la même cible (angle/audience), et la bascule `[x]` (archivée selon la doctrine todos racine). Pas de tick manuel · le downstream ferme la boucle. Si aucune ligne ne matche, le downstream ne crée rien et continue (silencieux).

**Léger, jamais bloquant.** Échec du write (gate refuse, fichier absent) → flag interne silencieux, ne casse pas le ship des angles. Le livrable Layer B (Step 11) et le close restent la sortie primaire · la trace todo est un bonus de persistance, pas une précondition.

**Doctrine.** Report des étapes différées et matérialisation des next-steps comme tâches reprenables avec leur levier · `docs/system/onboarding-setup-flow.md` (sections « Exhaustivité offerte, jamais forcée, reportable » et « La persistance est native »). Référencée ici, pas redupliquée.

---

## Step 12quater · Déposer le beat de restitution des angles (D#520)

Le set d'angles vient d'être posé (`angles/{ANG-NN}.json` lignés, back-refs tissés, todo persistée). Avant de rendre la main, **dépose le registre de ce run pendant que ton contexte est frais** · la lecture experte du set (lequel gagne, sur quel mécanisme, lequel est fragile et pourquoi) meurt si on la compresse en une phrase ici puis qu'on demande au fil de la re-broder. C'est de la matière de restitution, pas de la donnée de marque.

**Doctrine SSOT (contrat payload, règles décision-d'abord, richesse second-ordre, temporalité, mode) ·** `docs/system/restitution-beat-doctrine.md`. NE redéplie PAS le contrat JSON ici · lis la doctrine pour la forme, ce step ne porte que les params de la phase `angles`.

**Écris** (`Write` direct · c'est sous `.phantom/`, hors `brands/`, donc hors gate mutation · ne transite PAS par `write-to-context`) le fichier `.phantom/beats/{slug}/angles.json`. Params de cette phase ·

- `"phase": "angles"`. Le renderer mappe seul · vue `/phantom {slug} matrix`, forward-look « je score la matrice et je sors les axes prioritaires » (table doctrine). Tu ne mets ni chemin ni commande dans le payload, le code les appose.
- **`verdict`** · la lecture top-line du SET, tranchée, une ligne · lequel angle gagne et pourquoi en une frappe (le plus ancré sur de vrais verbatims, ou le plus différenciant si le corpus est mince). Pas « 5 angles produits » (météo), mais le verdict de matrice.
- **`read`** · 2-3 phrases de second ordre · POURQUOI cet angle gagne · sur quel mécanisme/insight il mord, ce que ça implique pour le test (budget calibré vs scale direct), et **le nerf** · la tension qui sépare le top 2 du reste. Densité d'insight, pas longueur.
- **`found` / `analyzed`** · les faits saillants du run (clusters de verbatims dominants, awareness stage joué, objection neutralisée la plus saillante) et leur conséquence (ce que la convergence des avis dit du vrai levier d'achat). Amorce grasse possible (`**la thèse.** le pourquoi`).
- **`rejected`** · les angles ou cellules écartés AVEC leur raison défendable (cellule formula-derived sans ancrage écartée du top, awareness stage en colonne « avoid » filtré, doublon clusterisé). Le travail de rejet est le plus invisible et le plus défendable · ne le jette pas.
- **`confidence`** · les angles à confiance faible AVEC leur cause RÉELLE · héritée de l'audience source (« audience portée en hypothèse, zéro mining → angles `TRÈS faible`, à tester pas à scaler ») ou de la brand. Un angle formula-derived n'est pas faible pour la même raison qu'un angle dérivé d'une audience non-validée · nomme laquelle. Les items prudents pointent l'étape qui les lèvera (« la voix-client lève cette confiance audience avant scale »).
- **`encoded`** · les artefacts posés (N angles lignés brand-side, back-refs objection/pain tissés, todo next-step) · pour le record.
- **`basis`** · une ligne sobre · le substrat lu (verbatims/objections/pains consommés, awareness distribution, canon copy) · rendue « Lu · ... ». Si le corpus était mince, dis-le ici (c'est la cause de la confiance, pas un caveat).
- **`tease`** · l'accroche · la valeur DANS la matrice (la lecture croisée angle × confiance × placement, ou l'angle surprise qui ressort). PAS de chemin · le renderer appose `/phantom {slug} matrix` et choisit la vue selon la phase.

Champ vide = omis, jamais inventé. Le renderer réorganise en **décision-d'abord** (verdict + read d'abord, puis le raisonnement qui flue, puis « Ce sur quoi je reste prudent », puis basis, puis le CTA) · tu déposes les champs, le code décide la forme. La confiance **forte** ne s'affiche pas seule, elle vit dans le verdict.

**Émission selon le mode (réutilise le signal orchestré-vs-standalone du skill).** Même signal que pour le `frame.json` passé en input par l'orchestrateur (Step 0quater) et le close chaîné ·

- **Orchestré** (produce-paid-angles invoqué par `build-atlas-complete` Phase 6 · audience/batch passés par le chairman) · tu te contentes d'écrire le payload, tu **n'émets pas**. L'orchestrateur rend le beat (`render-beat.py`) à sa frontière de phase. Tu rends la main.
- **Standalone** (l'opérateur a tapé « trouve les angles pour {audience} {brand} » directement) · après le Write, **émets toi-même** ·

  ```bash
  python3 .skills/render-beat.py --brand {slug} --phase angles --mode standalone
  ```

  Présente sa sortie **telle quelle** (NE re-narre pas, NE re-résume pas). En standalone le renderer PROPOSE la suite (« je score la matrice et je sors les axes prioritaires · je lance ? ») · la proactivité vient de là, elle remplace le close drill-down générique par le forward-look de la phase. Le hook `beat-emit` est le filet · si un payload frais reste non-émis, il le pousse.

**Léger, jamais bloquant.** Échec du Write ou du render (pas de payload, render vide) → retombe sur le close drill-down en prose (Step 9), ne laisse JAMAIS un trou à la place de la phase. Le livrable Layer B (Step 11) reste la sortie primaire · le beat est la restitution experte par-dessus, pas une précondition du ship.

---

## Cache strategy

24h TTL on the `(brand, audience, query-hash)` tuple. Re-running the same query on the same brand within 24h returns the cached output unless invalidated.

**Invalidation triggers (automatic):**
- Any mutation to `brands/{slug}/audiences/{audience-slug}/profile.json`.
- Any mutation to `brands/{slug}/products/{product-slug}/spec.json` for any product in the audience's primary scope.
- Any mutation to `brands/{slug}/brand.json#market.*` (VoM output landed since last run).

**Manual override:** `--fresh` flag bypasses cache, forces re-run.

Cache file location: `brands/{slug}/sources/produced-angles/_cache/{audience-slug}-{query-hash}.json`. Cleared automatically on file watcher trigger (mutation event).

The cache prevents LLM-variance noise on repeated identical queries (same operator question on Tuesday and Wednesday should not produce a slightly different ranking each time). The invalidation rule prevents stale results when fresh data lands between calls.

---

## --focus parameter

The skill accepts a focus modifier for narrower runs:

- **default** (no flag) · full ranked table 5 angles + synthesis + next-step proposal.
- **`--focus=cold`** · only angles for problem-aware / solution-aware audience cohorts (cold acquisition). Filters out product-aware and most-aware cells from cartesian.
- **`--focus=retargeting`** · only angles for product-aware / most-aware cohorts (warm retargeting). Filters out problem-aware and solution-aware cells.
- **`--focus=objection`** · table emphasizes objection neutralization, sorts by that lens, surfaces angles where the objection-proof match is strongest.
- **`--fresh`** · bypasses cache, forces re-run with current encoded data.

Focus modifiers are operator-facing additions (the operator can say *"angles paid pour la femme minceur okr en cold uniquement"* and the agent maps to `--focus=cold`). Internal flag, never surfaced as `--focus=` syntax to the operator.

---

## Hard Rules

- **Never invent a verbatim attributed to customers.** Never paraphrase a verbatim and present it as a customer quote. Either real (sourced from `voice.key_expressions[]` or `verbatim_quotes[]`) or formula-flagged. The trust contract breaks irrecoverably on this rule.
- **Verbatim density floor.** If `voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5 → recommend `mine-voc` first, do not produce angles on inferred-only basis without explicit operator override.
- **HR4.5 · Verbatim density floor gate (v1.4.0, append-only).** Si verbatim density floor déclenché en Step 1 (`voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5), le skill **doit** émettre un AskUserQuestion explicit AVANT toute production. Pas de fallback silencieux sur "je flag inline et ship quand même". Format gate strict :
  ```
  Corpus thin · {N_verbatims} verbatim(s) seul(s) disponible(s) sur {audience_label}.
  Trois moves possibles :
  (a) Produire 3 angles inférés à 60% confidence (flag visible inline + lineage formula-derived).
  (b) Refuser et router vers mine-voc d'abord (~20 min, on revient avec verbatims denses).
  (c) Produire 1 angle ancré sur le seul verbatim disponible, autres en backup formula-derived flagués.
  Tu choisis ?
  ```
  **Pas de production sans operator response explicit (a/b/c).** Override possible uniquement si l'opérateur a déclaré explicitement *"force, je sais que c'est inféré"* dans le tour précédent. Anti-pattern v1.3.0 résolu : auparavant, le skill shippait 3 angles inférés avec flag inline `(à valider, pas de verbatim direct)` sans gate, l'opérateur pouvait shipper sans réaliser que la matière n'était pas ancrée.
- **Cap dimensions at 5 max.** Cartesian beyond 5 dilutes signal per scoring framework anti-pattern.
- **Cluster filter mandatory.** Output never contains 2+ cells saying the same thing with different wording. Same pain + same objection + same placement = one angle, drop the rest.
- **Score never exposed.** Operator sees ranked angles, not numbers. No `Score 73/100`, no percentage, no rating bar.
- **Synthesis follows snapshot Step 7 canon strictly.** Pure prose, three implicit movements, no bold-section anchors, no enumeration of dimensions, no jargon leak. Read snapshot-brand SKILL.md Step 7 if uncertain.
- **Verbatim anchor flagged when formula-derived.** In the Layer A trace, every formula-derived cell carries `(formulation type, no direct customer voice)`. In operator output, formula-derived hooks ship with no anchor mention · internal sourcing stays internal, but inferred angles are flagged inline (*"à valider, pas de verbatim direct"*) so the operator knows what to test cautiously.
- **No orphan output mandatory.** Always close on a reasoned next-step proposal per doctrine v2.10.0. Never *"voilà tes angles, autre chose ?"*. Never a hardcoded `(a)/(b)/(c)/(d) Other` menu. The proposal is a function of operator goal × what was produced × what is runnable, not a template.
- **Cache invalidation on entity mutation.** No stale results when fresh data lands. Cache invalidates automatically on any mutation to in-scope `profile.json`, `spec.json`, or `brand.json#market.*`.
- **Schema field semantics as analytical vocabulary, never JSON path mentions.** *"the emotional driver is identity"* · yes. *"emotional_driver: identity"* · banned.
- **Banned jargon in operator surface.** No `awareness_stage:problem-aware`, no `cartesian_size: 72`, no `cluster filter applied`, no `dimensions_active`, no `score 87`, no `verbatim_anchor_id`, no `voice.key_expressions[]`, no `verbatim_quotes[]`, no `pain_points[].verbatim_quotes[]`, no `formula.tension.reason_blocked`, no JSON field paths whatsoever in operator-facing surface. The gate logic (Step 1 verbatim density check, HR4.5) reads these paths internally · the operator-facing surface uses plain language only (*"ta voix client est trop fine"*, *"verbatims sur la pain principale"*, *"j'ai 2 verbatims"*). No skill names mentioned in synthesis.
- **Auto-trigger after mine-voc OFF.** Even when `mine-voc` proposes `produce-paid-angles` as next step per no-orphan-output, the skill never auto-runs. Operator confirmation explicit, every time.
- **DTC-bounded in v1.** SaaS lead-gen, agency services, B2B information products carry different dimensions and proof emphasis. v1 ships DTC-only. SaaS adaptation belongs to a v2 mode or sibling skill, not a default branch.
- **Paid-only by name and scope in v1.** If operators ask for non-paid (content / email / organic) angles 2+ times, extend this skill via a new mode · do not fork into `produce-creative-angles` (per `extend_before_create`).
- **Hook quality spec mandatory.** Every shipped hook passes the 5-criterion test at ≥ 4/5. Below threshold → retry once with a different anchor or drop the cell. Non-negotiable.
- **`finalize-mutation-batch` mandatory.** Step 12 runs the Python primitive before any operator-facing summary. Exit code 2 = revise before shipping.
- **Weights are externalized canon.** All scoring weights (35/25/20/20 + binary placement filter) live in `resources/frameworks/paid-angle-scoring-weights.json` versioned. **NEVER override inline.** To propose new weights, bump `_version` in the JSON file and add a migration entry in `_change_log`. Improvised inline weights = refused, doctrine violation.
- **Voice consistency cross-block on multi-hook outputs.** When the output ships >1 hook (e.g. wide-test brief with 5-7 hooks for one campaign), persona and lexical_register must stay stable ±1 step across all hooks. Drift = MAJOR, refuse to ship without operator override.
- **Emotional diversity check post-rank.** If the top N ranked angles all collapse to the same emotional driver category (5 angles all loss-aversion-driven), the cluster filter has failed at the emotional-driver layer. Flag MAJOR, regenerate with explicit driver diversity constraint (anti-pattern: ranked angles paraphrasing the same fear).
- **Risk_bet slot opt-in via `--mode=breakthrough`.** Operator can request 5 safe + 1 risk_bet (max). The bet cell carries `bet=true`, `anchor=null` (verbatim-anchor suspended), `hypothesis_to_test` declared in plain language. Cell tagged in Layer A trace, surfaced in output with explicit *"Pari : [angle]. Hypothèse : [...]. À valider en test."* marker. Post-test routing: validated → promote to learnings, falsified → [SUPERSEDED]. Default OFF · never auto-trigger. See internal quality spec for the breakthrough mode protocol.

---

## Cross-references

- `docs/system/investigation-posture.md` (v2.54 doctrine canon) · cartographier avant affirmer · confidence chain explicit · angles portent confidence inheritée audience+brand en surface · close drill-down macro · opérateur arbitre (test direct vs upgrade audience source).
- `docs/system/confidence-propagation.md` · algèbre cascade confidence cross-skill (audience → angle → brief créa · MIN conservative).
- `resources/frameworks/paid-angle-scoring.md` · analytical canon. Mandatory read at first invocation. Codifies the five-lens scoring and the cluster-deduplication rule.
- `resources/registries/angle-registry.md` · angle taxonomy reference (14 angle types). Cell labels map to registry entries when possible.
- `resources/registries/proof-registry.md` · objection-neutralization mapping (which proof type defuses which objection).
- `resources/templates/hook-formulas.md` · fallback hook library (15 patterns) when verbatim is thin.
- `resources/quality-specs/hook-quality-spec.md` · 5-criterion hook quality test. Mandatory threshold ≥ 4/5 before shipping any hook.
- `resources/routing/awareness-angle-matrix.md` · awareness-angle pairing, used to filter cells in the "avoid" column for the dominant awareness stage.
- `.skills/skills/snapshot-brand/SKILL.md` · voice canon source for Step 9 synthesis. Read before writing the synthesis paragraph if any uncertainty.
- `.skills/skills/mine-voc/SKILL.md` · upstream Layer B source. Provides the verbatim density that ranking depends on.
- `.skills/skills/mine-vom/SKILL.md` · optional upstream. Vernacular and white-space signals raise hook quality and unlock the market dimension.
- `.skills/skills/produce-copy-brief/SKILL.md` · downstream production skill. Operator picks an angle from the ranked table → `produce-copy-brief` turns it into a hook variant set + body opening + CTA family.
- `.skills/finalize-mutation-batch.py` · mandatory Step 12 primitive.
- `.skills/write-to-context.py` · canonical mutation channel for any write to `learnings.json` if a pattern is detected during the run.
- `docs/system/contextual-intelligence.md` · master doctrine. No orphan output rule, contextual reasoning, anti-patterns.
- `docs/system/voice.md` · voice canon, register, banned phrases.
- `resources/schemas/_shared/awareness-stage.json` · `$ref` partagé v2.29.0, 5 stages Schwartz canoniques. Source unique consommée par `lineage.awareness_stage` dans `angle.schema.json` v1.2.
- `resources/schemas/angle.schema.json` (v1.2) · schema cible persistance brand-side. Renommages : `source` devient `origin_axis`, `lineage.schwartz_conscience` devient `lineage.awareness_stage`. 8 fields migrés vers creative.
- `resources/schemas/creative.schema.json` (v1.1, NEW) · 7ème entité brand. Absorbe `intent`, `mecanique`, `seasonality_trigger`, `execution.*`, classification, `variant_of`. Si production créa instance complète, écrire ici (skill `compose-creative` v2.31+ ou direct).
- v2.29.0 manifest + D#391 · refacto angle/creative split, gouvernance schemas.

---

## Example output · okr probiotique minceur

What the operator sees in the terminal after triggering *"trouve les meilleurs angles paid pour la femme minceur okr"*:

---

Sur la femme minceur okr, audience source mine-voc tourné (28 verbatims, validation `forte` côté pain principal "ras-le-bol des régimes" et "miroir post-grossesse"). Brand source positioning Observé direct (revendiqué site, tone confirmé), `forte` aussi. Les angles 1-3 héritent claim_confidence `forte`, ancrés sur verbatims VoC denses. Les angles 4-5 sont formula-derived (pas de verbatim direct dans le corpus), héritent `moyenne` agrégée · à valider sur premiers tests.

Le move premier sur ton lancement c'est l'angle miroir en Reels · verbatim dense, objection scepticisme neutralisée par tes avis Trustpilot, format Reels qui matche ton stack. L'angle ballonnement en Stories est le backup à promouvoir si le miroir fatigue après une semaine. Garde le ras-le-bol des régimes pour une vague 2, il convertit moins haut mais retient plus longtemps.

| # | Angle | Hook | Émotion mobilisée | Objection neutralisée | Placement reco | Confiance |
|---|---|---|---|---|---|---|
| 1 | Miroir post-grossesse | "Je ne pouvais plus voir mon reflet" | Identitaire | "J'ai déjà tout essayé" | Reels | forte (verbatim direct) |
| 2 | Ballonnement permanent | "Toujours ballonnée, le ventre gonflé même à jeun" | Inconfort quotidien | "Trop cher pour 1-3 kg" | Stories | forte |
| 3 | Ras-le-bol des régimes | "Frustration, échec, culpabilité, la boucle de tous les régimes" | Délivrance | "C'est juste du marketing" | Feed UGC | forte |
| 4 | Verdict balance | "Le moment où tu montes sur la balance et tu sais déjà" | Anticipation négative | "Ça marche pour les autres, pas pour moi" | Reels | moyenne (formula-derived) |
| 5 | Confiance retrouvée | "Remettre la robe que tu as rangée il y a 2 ans" | Aspiration projetée | "Je vais reprendre dès que j'arrête" | TikTok | moyenne (formula-derived) |

Le move · on part direct sur les 3 premiers angles (`forte`, calibrés sur verbatims) pour ton lancement jeudi · brief créa, budget test ~50-100€ par angle, 5-7 jours de data minimum avant verdict. Les angles 4-5 (`moyenne`, formula-derived) partent en variants secondaires sur le même test · tu auras la data réelle après 7 jours pour les killer ou les pousser, sans re-mining préalable.

Les angles 4-5 ne sont pas ancrés sur verbatim direct · je regarde en parallèle s'il existe une formulation cliente dans le corpus pour les solidifier, je te ramène ça sans que tu aies à creuser.

Tu peux aussi prendre l'autre route si tu veux 5 angles tous ancrés avant de scaler · pousser l'écoute clients sur les pains "verdict balance" et "confiance retrouvée" (~10 min) avant de lancer. Mais vu ta deadline jeudi, le move au-dessus tient.

---

The same skill on a vitamin-C serum brand for women 28-42 with hyperpigmentation surfaces different dimensions: `pain.trigger` becomes load-bearing (post-pill, post-pregnancy, post-summer triggers), `objection.type` foregrounds *scepticisme actifs* over *prix*, the white-space dimension from VoM (post-rétinol routines, layering anxiety) becomes a primary axis. Output shape stays identical (five rows, plain language, hooks anchored in customer voice, synthesis above, next-step below) but no row repeats from the okr output. That non-repetition is the proof the skill reasons over the brand and does not template.

On a fashion brand the skill degrades gracefully: `pain.emotion` thins (fashion is more desire-driven than pain-driven), so active dimensions shift to `audience.JTBD.social`, `product.benefit.identity`, `brand.market.sophistication_stage`, and `placement`. The synthesis names the shift in prose (*"sur cette poche fashion la matière sort moins sur les pains que sur l'identité projetée, donc les angles ranked travaillent plus sur le statut et la projection que sur la résolution d'un problème"*) and the table holds.
