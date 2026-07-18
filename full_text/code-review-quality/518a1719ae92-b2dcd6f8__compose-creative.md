---
name: compose-creative
version: 1.9.1
type: producer
isolation_scope: brand_only
layer: production
recommended_model: opus
subagent_safe: true
mode: proposed
operator_facing: true
reasoning_pattern: matrix-driven
matrix_mode: composing
description: >
  v1.7.0 (v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés) · Section pré-runtime ajoutée AVANT HR1 detect input mode · expose 6 paramètres décomposés au runtime (brief source · mécanique creative · variants visuels · hook variants OTRB · packshot/asset · hypothèses figées · biais à éviter) avec POURQUOI chacun + close binaire OK ou ajuste. Cross-ref doctrines decomposition-visibility-discipline + engagement-disclosure-discipline v2.79.5+. Backward compat strict additif.
  v1.6.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · context.pain_point reference refactor · lookup `audiences/{audience_slug}/pain_points/{PNT-NN}.json` canonical sub-audience (owned natif par parent path). creative.json stage maintenant ref `context.pain_point_ref: "PNT-NN"` canonical depuis sub-audience. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.5.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · context.pain_point reference refactor · lookup `pain_points/{PNT-NN}.json` canonical (au lieu de profile.pain_points[idx] sub-field legacy). creative.json stage maintenant ref `context.pain_point_ref: "PNT-NN"` canonical. Backward compat lecture profile.pain_points[] legacy preserved (pre-v2.63 brands).
  v1.4.3 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method, pain-benefit-chain, breakthrough-advertising-5-stages). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.4.0 (v2.48) : multi-layer paste extension HR3b Step 3b.5 · composite_layers[] ordered packshot + logo + badge en couches pour ads complets branded pixel-exact.
  v1.3.0 (v2.47) : composite_mode input option · full_regen (default) OR layered (pattern studio photographer · packshot canon collé pixel-exact via PIL paste post-gen scene-only).
  v1.2.0 (v2.46) : endpoint nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025) cohérent craft-packshot v1.1.
  v1.0.1 (v2.35 alignment) : visual_identity path fallback (spec.json#visual_identity OR sibling visual_identity.json).
  v1.0.0 (v2.34 ship production loop). Pendant FORWARD de decompose-ad (qui est REVERSE).
  Génère une créa (visuel via fal.ai nano-banana-2/edit + brief copy markdown S55 fiche v5)
  depuis un brief structuré ancré dans canon × profil audience × angle × brand visual_identity.
  Assemblage compositionnel selon équation v3.1 (NOYAU x CONTEXTE x MODIFIEURS).
  Persiste (Brique 4 étape B · split) sous brands/{slug}/creatives/{batch}/{CRT-NN}/ ·
  genome.json (ADN · genome/1.2) + creative.json (lignage · creative/1.4) + produced/{slug}.json
  (sidecar manifest binaire · produced-asset/1.0) + produced/{slug}.jpg (binaire direct) + brief.md.
  Dossier {CRT-NN}/ réservé par mkdir-claim atomique (STEP 0) avant tout write.
  Inputs supportés : (audience_slug, angle_id, product_slug optional), ou hypothèse from
  scratch ("produit angle pour {brand_slug} post-grossesse" sans angle_id, le skill propose 2-3
  angles depuis profile.json + canon copy).
  FR: "compose une créa", "produis un visuel", "génère une créa pour", "creative pour cette audience", "matérialise l'angle".
  EN: "compose a creative", "generate a visual", "produce creative for", "materialize the angle".
disambiguates_against:
  decompose-ad: "decompose-ad fait du REVERSE (analyse ad existante). compose-creative fait du FORWARD (génère depuis brief)."
  produce-paid-angles: "produce-paid-angles produit des ANGLES (stratégie textuelle). compose-creative produit la CRÉA finale (visuel + brief copy)."
  produce-copy-brief: "produce-copy-brief écrit un BRIEF copy. compose-creative orchestre brief + visuel ensemble."
  recompose-creative: "recompose-creative ADAPTE une créa existante (variant). compose-creative produit ex nihilo."
  weave-hooks: "weave-hooks prépare le paquet multi-scripts du batch (contrat A→B) en amont · compose-creative produit le binaire d'UN CRT."
consumes:
  - path: brands/{slug}/angles/{angle_id}.json
    min_version: 1.2.0
    note: angle source (formula Obs+Tension+Reframe+Bridge + lineage canon)
  - path: brands/{slug}/audiences/{audience_slug}/profile.json
    min_version: 1.0.0
    note: 8 dimensions + Schwartz + persona
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
    note: brand_equity_level + creative_zone (curseur copy/visual)
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: "primary path. packshots clean + color_palette + distinctive_features (S55 v2.31 extension)"
  - path: brands/{slug}/products/{product_slug}/visual_identity.json
    min_version: 1.0.0
    note: "fallback path (sibling). Convention legacy or import-product-visuals output. Verifier _belongs_to pointer = product_slug."
  - path: resources/canon/copy/hooks/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/mecaniques/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/archetypes-voix/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/formules-titres/*.json
    min_version: 1.0.0
  - path: resources/templates/creative-formula.md
    min_version: 3.1.0
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
  - path: resources/registries/styles/*.json
    min_version: 1.0.0
    note: "NEW style-library (backing primary_style_id) · la fiche du style choisi pilote le prompt (render_recipe), fournit les anti_ai_guardrails au gate qc-creative, et le da_compat vérifié vs brand.json#brand_da"
  - path: resources/registries/style-registry.md
    min_version: 1.0.0
  - path: resources/concepts/*.json
    min_version: 1.0.0
    note: "NEW history-aware · patterns concept promus (library-pattern). Sur freedom_cursor=exploit, piocher un pattern promote-ready matchant le mecanique_id choisi, via l'espace d'ids déclaré par related_mechanic_ids (hook-level enum ET mecanique_id ad-level · cf description élargie library-pattern.schema), au lieu de composer à froid."
  - path: resources/registries/hooks/*.json
    min_version: 1.0.0
    note: "NEW history-aware · patterns hook promus cross-brand (surtout vidéo). EN PLUS de canon/copy/hooks (archétypes de copy), distinct."
  - path: resources/schemas/creative.schema.json
    min_version: 1.3.0
    note: "couche lignage (Brique 4 étape B · creative/1.4 · variant_of CRT|RCV + lineage{})"
  - path: resources/schemas/genome.schema.json
    min_version: 1.0.0
    note: "NEW Brique 4 étape B · ADN par-créa (genome/1.2 · script_id GSC-NN, hook, frames, support, genome_tags)"
  - path: resources/schemas/produced-asset.schema.json
    min_version: 1.0.0
    note: "NEW Brique 4 étape B · sidecar manifest binaire (produced-asset/1.0 · 1 par .jpg produit, anti-orphelin)"
  - path: resources/conventions/creative-storage.md
    min_version: 1.0.0
    note: "forme batch creatives/{batch}/{CRT-NN}/ + allocation mkdir-claim (D#481)"
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/system/output-clarity-doctrine.md
  - path: docs/system/operator-vocabulary-translation.md
produces_validations_for:
  # Brique 4 étape B · les tags mécanique/concept vivent désormais dans genome.json (ADN),
  # les validations vers le canon copy se sourcent de la couche genome (genome_tags.mechanic_id /
  # hook.mechanic_id), pas de creative.json.
  - resources/canon/copy/hooks/*.json
  - resources/canon/copy/mecaniques/*.json
  - resources/canon/copy/archetypes-voix/*.json
produces_proposals_for:
  - brands/{slug}/creatives/{batch}/{CRT-NN}/genome.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg
  - brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md
prerequisites:
  - field: angles/{angle_id}.json
    level: L1
    auto_pull: read_angle_target
    freshness_ttl_days: 30
  - field: products/{slug}/brief-{angle_id}.md
    level: L1
    auto_pull: read_brief_markdown
    freshness_ttl_days: 30
  - field: products/{slug}/visual_identity
    level: L1
    auto_pull: dual_path_inline_or_sibling
    freshness_ttl_days: 90
  - field: products/{slug}/visual_identity.assets_canonical.{slot}
    level: L2
    note: "v1.3 layered mode prerequisite · lookup canonical packshot path validated_by_operator + _canonical true · si absent, layered impossible et fallback full_regen"
    freshness_ttl_days: 90
  - field: brand.creative_zone
    level: L3
    fallback: proxy_brand_personality
    confidence_default: 0.6
  - field: resources/canon/copy/formats-livrables
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
permissions:
  reads: [brand, product, profile, angle, learning, strategy, canon_copy, registries]
  writes: [creative]
  emits_events: [creative_composed, visual_generated, brief_written, mecanique_proposal_flag]
  external_apis:
    - provider: "fal.ai"
      endpoint: "fal-ai/nano-banana-2/edit"
      model_family: "gemini_3_pro_image_novembre_2025"
      version_check_url: "https://fal.ai/models?keywords=banana"
      version_canon_date: "2025-11"
      replaced_legacy: "fal-ai/nano-banana-pro/edit (v1.0.x · Gemini 2.5 Flash Image)"
      auto_upgrade: false
  preconditions: "angle.json existe avec lineage canon. profile.json 8 dimensions populated. spec.json#visual_identity populated avec primary_front packshot. credentials FAL_API_KEY présent dans credentials_shared.env. {batch} courant résolu (run date-stampé du jour, ex 2026-06-07-NN) et `mkdir -p brands/{slug}/creatives/{batch}/` exécuté AVANT le mkdir-claim, sinon STEP 0 n'a pas de dossier-batch parent."
  postconditions: "genome.json (genome/1.2) + creative.json (creative/1.4) persistés sous brands/{slug}/creatives/{batch}/{CRT-NN}/ via write_to_context mode=proposed. JPG écrit DIRECT sous {CRT-NN}/produced/{slug}.jpg AVEC sidecar produced/{slug}.json (produced-asset/1.0) le traçant (anti-orphelin). brief.md écrit DIRECT sous {CRT-NN}/. Dossier {CRT-NN}/ + produced/ créés par mkdir-claim atomique (STEP 0) avant tout write. brief markdown S55 fiche v5 forward rendu à l'opérateur. Validation silencieuse via validate-resources."
---

# Skill: compose-creative

> **Compose a creative forward.** v1.9.0 · S55 fiche v5 forward · split genome/1.2 + creative/1.4 + produced-asset/1.0 · forme batch `creatives/{batch}/{CRT-NN}/` · équation v3.1 · pendant FORWARD de decompose-ad.

Producer, not decomposer. Lit (angle × audience × brand × product visual_identity × canon copy), applique l'équation compositionnelle v3.1 en mode forward, génère un visuel via fal.ai nano-banana-2/edit (v2.46 canon, Gemini 3 Pro Image), écrit un brief copy markdown S55 fiche v5. Persiste (Brique 4 étape B · split) sous `brands/{slug}/creatives/{batch}/{CRT-NN}/` · genome.json (ADN · mécanique/format/concept/stop_scroller/hook/frames/genome_tags typed/script_id GSC-NN) + creative.json (lignage · refs + variant_of + variant_axis + meta.validation_status + performance + tags) + sidecar produced/{slug}.json (manifest binaire) + brief.md. Le dossier {CRT-NN}/ est réservé par mkdir-claim atomique AVANT tout write. Le mécanisme reste invisible (pas de field paths, pas de scores numériques, pas de noms internes). L'opérateur voit une fiche quatre sections forward, un JPG local, et un bloc tags retrieval.

## Tone

Posture créateur senior + collègue stratège. Pas inspecteur, pas générateur aveugle. La fiche est dense mais lisible : phrases courtes, projection visuelle d'abord (Section 1), pourquoi ça raconte ça (Section 2), diagnostic prédictif honnête (Section 3), tags retrieval. Aucun jargon plumbing, aucun nom de field JSON, aucun acronyme doctrine en surface. Si un slot manque (visual_identity absent, profile incomplet), surface honnête et propose le skill prérequis à run d'abord.

## Expert methodology

**Persona.** Senior creative director qui a composé dix mille créas paid social cross-typologies. Lit un brief comme un copywriter senior lit un canon : isole le NOYAU (mécanique × format × stop_scroller × ton), branche le CONTEXTE (angle × pain_point × persona × proof), applique les MODIFIEURS (intent_mix × audience_segment × craft_mode × overlay_density × brand_mark_present × cta).

**Framework.** Équation compositionnelle v3.1 stress-tested S55. Source canon : `resources/templates/creative-formula.md`. SSOT mécaniques : `resources/registries/creative-mechanics-registry.md`. Free-string `mecanique_id` autorisé.

**Pattern partagé avec decompose-ad.** Mode forward (input = brief stratégique, output = creative). Mode reverse = decompose-ad (input = ad existante, output = fiche). Cohérence cross-skill obligatoire sur fiche v5 layout.

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant assemblage compositionnel (Step 1), scanner prerequisites :

1. L1 silent · `angles/{angle_id}.json` (required) · `products/{slug}/visual_identity` (dual path inline OR sibling, HR1.4 v2.35 formalisé) · `resources/canon/copy/formats-livrables`
2. L1 silent optionnel · `products/{slug}/brief-{angle_id}.md` (si présent, source de truth pour copy)
3. L3 degraded · si `brand.creative_zone` absent → fallback `brand_personality` · confidence 0.6 · flag _gaps

Output state map + confidence_chain[] init.

---

## Engagement disclosure pré-runtime · NIVEAU 0 paramètres décomposés (canon v2.79.5)

Avant HR1 (detect input mode + load pre-requisites), expose ce disclosure NIVEAU 0 à l'opérateur. Pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5. Le but · rendre les paramètres décomposés que ce skill va mobiliser visibles AVANT exécution. Coût compose-creative = appel fal.ai nano-banana-2/edit facturé (token + crédit image gen). Disclosure protège l'opérateur d'un run qui part sur mauvais asset / mauvaise mécanique.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Brief source
     {brief markdown atlas brand `products/{slug}/brief-{angle_id}.md`
     OR angle.json seul (mode hypothèse from scratch)}
     POURQUOI ce brief · {ex "brief copy déjà produit produce-copy-brief
     <24h, source de vérité pour copy"
     OR "pas de brief existant, je compose depuis angle + profile +
     canon copy"}

  2. Mécanique creative
     Sélection depuis `resources/registries/creative-mechanics-registry.md`
     {ex avant-après · démonstration · témoignage UGC · stat-choc ·
     question-callout · contrarian · before-after · split-screen · autre}
     POURQUOI cette mécanique · {ex "audience problem-aware →
     avant-après ancrage somatique" OR "objection 'just marketing'
     → démonstration mécanisme + proof scientifique" OR "stage
     conscience unaware → stat-choc pour briser pattern"}

  3. Variants visuels
     {N variants · default 1 single OR 2-3 si A/B test demandé}
     POURQUOI cette variance · {ex "single ship rapide pour test
     baseline" OR "3 variants croisent hook × mécanique × asset
     pour ladder A/B" OR "operator explicit demand N"}

  4. Hook variants
     OTRB · Observation × Tension × Reframe × Bridge
     {N hooks générés · default 3 hooks variants quality spec ≥4/5}
     POURQUOI ces variants · {ex "hook 1 verbatim exact, hook 2
     verbatim sémantique, hook 3 formula contre-intuitive"}. Structure
     canon angle-anatomy doctrine, pas freestyle.

  5. Packshot/asset
     Source · {visual_identity.assets_canonical.{slot}
     _validated_by_operator: true OR primary_front packshot OR
     fallback full_regen (no canonical asset)}
     POURQUOI cet asset · {ex "packshot canon validé pixel-exact
     mode layered" OR "pas de canonical, full_regen scène complète
     avec produit hallucination accepted" OR "layered + logo + badge
     multi-layer composite pour ad branded complet"}

  6. Hypothèses figées
     Format paid · {Meta vs organic (TikTok / Reels / Stories) ·
     default Meta si stack signals}
     Ratio aspect · {1:1 default Meta feed · 4:5 feed mobile
     optimized · 9:16 Stories/Reels · adapté placement}
     Placement · {feed / story / reel / carousel · inféré stack +
     brand focus + format demandé}

  7. Biais à éviter
     · Over-design (visuel surchargé qui dilue le hook · canon
       v2.51 craft_mode density modérée default)
     · Template visuel répétitif (cluster-deduplication contre
       formats identiques cross-runs)
     · Cliché créa DTC FR (registre "transformation 30 jours",
       "avant-après photoshop évident", "fond blanc isolé sans
       contexte" si audience demande scène-de-vie)

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?
```

ATTENDS confirmation explicite avant de lancer HR1. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set OR si l'opérateur a flag `--no-disclosure` explicit OR si N usages successifs >= seuil expert (`auto_skip_after_n_calls` true). Sinon · disclosure obligatoire canon v2.79.5.

Cross-ref doctrines racine `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5.

---

## HR1 · Detect input mode + load pre-requisites

L'opérateur peut fournir l'input sous trois formes. Detection auto :

| Input shape | Mode | Action |
|---|---|---|
| `(audience_slug, angle_id, product_slug)` explicite | forward_direct | Load tous les pre-requis, pipeline complet |
| `(audience_slug, angle_id)` sans product_slug | forward_direct | Lookup product principal de la marque, pipeline complet |
| `(audience_slug, product_slug)` sans angle_id | hypothesis_from_scratch | Skill propose 2-3 angles depuis profile.json + canon copy avant de composer |

**Composite mode (NEW v1.3) · option orthogonale aux inputs ci-dessus.**

Operator peut ajouter `composite_mode` au input · `full_regen` (default · pipeline HR3 standard) OR `layered` (pipeline HR3b · scène séparée + packshot canon collé PIL). Decision rule détaillée HR-COMPOSITE. Detection signaux ·
- Phrase explicite "studio photographer", "packshot canon", "fidélité critique", "preserve packshot", "mode layered", "composite mode" → `layered`
- Spec.identity.product_category ∈ {supplement, cosmetic, food, pharma} ET visual_identity.assets_canonical.{slot}._validated_by_operator: true → suggest `layered` avec AskUserQuestion gate
- Sinon · `full_regen` default

**Read pre-requisites obligatoires :**

1. `brands/{slug}/angles/{angle_id}.json` (formula + lineage canon).
2. `brands/{slug}/audiences/{audience_slug}/profile.json` (8 dimensions + Schwartz + persona).
3. `brands/{slug}/brand.json` (creative_zone + brand_equity_level + tone_of_voice).
4. `visual_identity` (packshots clean + color_palette + distinctive_features + label.wordmark_text). **Path lookup avec fallback :**
   1. Tenter `brands/{slug}/products/{product_slug}/spec.json#visual_identity` (path canonique inline).
   2. Si absent ou champ manquant, fallback `brands/{slug}/products/{product_slug}/visual_identity.json` (sibling). Verifier `_belongs_to` pointer = `product_slug` avant consume.
   3. Si toujours absent ou les 2 paths donnent des champs vides, surface gracefully + suggest `define-specs` (canon path) ou `import-product-visuals` (futur skill, sibling path).
   4. JAMAIS refuser bloquant si l'un des 2 paths donne quelque chose d'exploitable. Merge logique : sibling override inline si les 2 existent et divergent (sibling = source plus recente par convention import).
5. `resources/canon/copy/*` (hooks, mecaniques, archetypes-voix, formules-titres).
6. `resources/registries/creative-mechanics-registry.md` (SSOT mécaniques).

**Pre-requis manquants gate :**

- `visual_identity` absent ou `packshots.primary_front` null → surface warning, suggest `define-specs` à run d'abord. Refuse de composer (régression label garantie).
- `profile.json` incomplet (moins de 6 dimensions sur 8) → surface warning, suggest `profile-audience` à run d'abord. Continue si l'opérateur insiste mais flag confidence basse.
- `angle.json` absent et mode `hypothesis_from_scratch` → propose 2-3 angles candidats depuis profile.json problem_map + canon copy formules-titres, demande validation avant de composer.
- `FAL_API_KEY` absent → surface honnête, refuse de composer, suggest connect-source pour configurer la credential.

---

## HR2 · Apply équation v3.1 compositionnelle

Assembler l'ADN (genome.schema · genome/1.2 · genome.json) + le lignage (creative.schema · creative/1.4 · creative.json) selon NOYAU × CONTEXTE × MODIFIEURS. Le NOYAU (mécanique × format × stop_scroller × ton) projette dans `genome.json` ; le CONTEXTE/MODIFIEURS (refs, intent_mix, execution, performance) dans `creative.json`. La persist split est détaillée HR5.

**History-aware (NEW · pioche vs froid) :** lire `regime.freedom_cursor` (explore↔exploit). Ordre de résolution v2.90.0 : (1) `creatives/{batch}/genome-package.json#regime` si le script en provient (produit par weave-hooks, contrat A→B) · (2) sinon `creatives/{batch}/frame.json#regime` si le batch est cadré (produit par frame-regime) · (3) sinon composer à froid avec `freedom_cursor_note: "uncadré"`.
- **exploit** (cursor bas) · pour le `mecanique_id` AD-level choisi, chercher un pattern PROMU (`resources/concepts/*.json` = `library-pattern` avec `promotion.status: promote-ready`) qui le matche via l'espace d'ids déclaré par `related_mechanic_ids` (hook-level enum ET mecanique_id ad-level · cf description élargie library-pattern.schema · le pattern déclare lui-même les ids des deux espaces qu'il couvre, jamais de match mécanique d'un free-string ad-level contre l'enum hook). Si trouvé, injecter son `skeleton`/`slots` comme base · composer SUR l'historique qui a marché cross-brand, pas à froid. Idem côté hook si vidéo (`registries/hooks/*.json`). NB : `primary_style_id` se joint via le style-registry, pas via `related_mechanic_ids`.
- **explore** (cursor haut) · autoriser un reslot novateur (pattern d'une autre verticale, ou mécanique moins évidente), et le SURFACER à l'opérateur comme pari assumé.
- Aucun pattern promu disponible · composer à froid (comportement actuel), `freedom_cursor_note` consigné.

**NOYAU (invariant créa) :**

- `mecanique` : choisir parmi `creative-mechanics-registry` SSOT en cohérence avec `angle.formula` + `profile.market_context`. Free-string `mecanique_id` autorisé. Si aucune mécanique ne fitte → `other` + flag `mecanique_proposal` (HR7).
- `format` : default `static_image` ratio 4:5 (Meta feed) sauf override opérateur (`carousel`, `video_short`, `reel`, `story`).
- `stop_scroller` :
  - `hook_layer` (verbal) pulled depuis `angle.formula.observation` summary, formulé en 1 phrase courte.
  - `visual_layer` (description scène) depuis `angle.formula.tension` + `audience.problem_map`, descriptif visuel objectif.
- `ton` : depuis `brand.tone_of_voice` + `audience.identity_signals`, croisé.

**CONTEXTE (couches stratégiques branchables) :**

- `angle_ref` : `angle_id` source (lineage canon préservé).
- `pain_point` (v1.6.0 ontologie sémantique pure) : lookup `audiences/{audience_slug}/pain_points/{PNT-NN}.json` canonical sub-audience (owned natif par parent path · NEW v2.64). Stage `context.pain_point_ref: "PNT-NN"` canonical dans creative.json downstream HR5. Si angle.lineage.pain_ref déjà populé (produce-paid-angles v1.10+), priorité absolue à ce ref canonique. Sinon, pick top pain entity par severity desc sur l'audience. Backward compat (v2.63 brands) · si sub-audience vide, fallback top-level `pain_points/{PNT-NN}.json` v2.63 filtered by `affected_audiences[]` contains `{audience_slug}`. Fallback v1.7 · si top-level vide aussi, fallback `profile.json#problem_map` ou `profile.json#pain_points[]` sub-field legacy · stage `context.pain_point_ref: null` + `context.pain_point_text: "{verbatim from legacy}"` inline.
- `persona` : depuis `profile` (type + buyer_user_split snapshot cache).
- `proof` : depuis `spec.problems_solved` + `audience.benefit_stack`.

**MODIFIEURS (override situationnels) :**

- `intent_mix` (multi-weighted) : depuis `brand.creative_zone` + `angle.intent` fallback. Si pure (`primary` 100%), skip `weights`. Si mélange (ex 60% DR + 40% Brand), encoder explicitement (`weights: {DR: 0.6, Brand: 0.4}`, somme à 1.0 ± 0.05).
- `audience_segment` : depuis `profile` (B2C default).
- `craft_mode + overlay_density + brand_mark_present` : depuis `brand.creative_zone` curseur.
  - `overlay_density` (0.0-1.0) : 0.0 photo produit pure, 0.1-0.3 minimal mark, 0.4-0.7 hook + claim layered, 0.8-1.0 verbal-dominated.
  - `brand_mark_present` (bool) : logo/wordmark visible, orthogonal à overlay_density.
  - `craft_mode` legacy mirror : `product_only` si density=0 et brand_mark_present=false ; `minimal_brand_mark` si density<0.3 et brand_mark_present=true ; `with_overlay` si density>=0.4.
- `cta` : modalité explicite depuis `angle.formula.bridge.promise` + `offer.json` si applicable.

---

## HR3 · Génération visuelle via fal.ai nano-banana-2/edit

Endpoint canon · `fal-ai/nano-banana-2/edit` (Gemini 3 Pro Image · canon novembre 2025 · supérieur vs `nano-banana-pro/edit` legacy Gemini 2.5 Flash Image qui régressait silhouette OR text fidelity). Cohérent craft-packshot v1.1 upstream qui valide ce pattern (S55 v2.44 stress test · 1 attempt vs 9 échouées endpoint legacy). Doctrine sœur · `docs/system/model-versioning-canon.md`.

Pipeline image gen :

1. Récupère packshot clean URL depuis `visual_identity.packshots.primary_front`. **Path lookup avec fallback :**
   1. Tenter `brands/{slug}/products/{product_slug}/spec.json#visual_identity.packshots.primary_front`.
   2. Si absent, fallback `brands/{slug}/products/{product_slug}/visual_identity.json#packshots.primary_front` (sibling, verifier `_belongs_to` pointer).
   3. Si les 2 paths absents ou null, refuse de composer (regression label garantie cf HR1.4).
2. Construis prompt structuré :
   - **Style (style-library · NEW)** : lire la fiche `resources/registries/styles/{genome_tags.primary_style_id}.json`. Son `render_recipe.prompt_skeleton` (+ `slots`, `lighting`, `camera_lens`, `palette_mood`, `texture_grain`, `composition_notes`) PILOTE le squelette du rendu au lieu de l'improviser. Vérifier `primary_style_id ∈ brand.json#brand_da.allowed_style_ids` (sinon warn opérateur). Transmettre les `anti_ai_guardrails` de la fiche au gate `qc-creative` (Axe 5). Index lisible · `resources/registries/style-registry.md`.
   - Référence DNA visuel angle (mécanique narrative + scène depuis HR2 NOYAU).
   - Hard constraints `visual_identity` (non-négo) :
     - Container : `{container.shape} {container.material} {container.cap_type}, {container.transparency}`.
     - Content : `{content.quantity_visible} {content.form} color {content.color_hex} {content.shape}`.
     - Label : `MUST read exactly '{label.wordmark_text}'. Sub-label: '{label.sub_label}'. Duration: '{label.duration_indicator}'.`.
     - Color palette : `container {color_palette.container_primary}, label background {color_palette.label_background}, label text {color_palette.label_text}.`.
     - Distinctive features : `MUST PRESERVE: {distinctive_features[0]}. {distinctive_features[1]}. ...`.
   - Atmosphère depuis `brand.creative_zone` + `audience.identity_signals`.
   - Format `4:5 vertical Meta feed` default.
3. POST `https://fal.run/fal-ai/nano-banana-2/edit` (endpoint canon v2.46, **PAS** `nano-banana-pro/edit` legacy v1.0.x ni `nano-banana/edit` v0 qui ignore aspect_ratio) avec payload :
   - `image_urls=[packshot_url]`
   - `prompt=<above>`
   - `aspect_ratio="4:5"` (default Meta feed, override possible via input opérateur). Enum supportée par endpoint : `auto, 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16`.
   - `output_format="jpeg"`, `resolution="1K"` (default Meta feed, override `2K` si haute fidélité requise).
   - Auth header `Authorization: Key ${FAL_API_KEY}`.
4. Download résultat dans `/tmp/compose-creative/{brand}-{crt_id}.jpg` (staging éphémère).
5. Move final vers `brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg` (binaire écrit DIRECT · le dossier `{CRT-NN}/produced/` existe déjà, réservé par le mkdir-claim HR-CC-CANON-1 STEP 0). PUIS écrire le sidecar manifest `produced/{slug}.json` (produced-asset/1.0 · `asset_role`, `file`, `tool: "fal"`, `endpoint`, `params`, `status: "generated"`, `created_at`, `genome_ref: <script_id GSC-NN>`) via `write_to_context` mode=proposed (anti BUG-ASSET-ORPHAN · tout binaire sous produced/ a son sidecar json gated). Double régime explicite · binaire .jpg direct, sidecar .json par le gate. Détail HR5 + HR-CC-CANON-1.

**Retry logic label preservation :**

- Si gen retourne visuel avec label régressé (wordmark différent du `label.wordmark_text`), retry max 2 fois avec prompt renforcé `"PRESERVE EXACTLY label artwork from reference image. Wordmark text MUST be '{label.wordmark_text}' character-for-character. NO variants, NO substitutions."`.
- Si toujours régressé après 3 iter total, flag warning à l'opérateur en langage métier (cf HR3.4 soft offer) + persiste avec note technique backstage `meta.label_compositing_required: true`.

**QC post-gen :**

- Valider chaque `distinctive_features[]` présent dans le render (lecture image + cross-check description).
- Valider color_palette dominantes match (hex tolérance ±15%).
- Échec sur 1+ feature → flag à l'opérateur + propose re-gen avec prompt renforcé.

### HR-QC-GATE · Gate QC de sortie (qc-creative) · pas de spend sans vert

Après le QC soft ci-dessus et AVANT de présenter la créa comme prête (avant persist final), invoquer le gate `qc-creative` sur le binaire produit. On met du budget média derrière, rien ne passe sans gate vert.

1. **Invoquer** `qc-creative` avec `creative_dir = brands/{slug}/creatives/{batch}/{CRT-NN}/` (Task tool · curator · sonnet · subagent_safe). Il REGARDE le binaire (vision) et rend `{shippable, decision, per_binary[], blocking_issues[], fix_list[]}`.
2. **Écrire le verdict** dans `produced/{slug}.json#qc` (`passed`, `checks[]`, `regen_count`) via `write_to_context` mode=proposed (réceptacle produced-asset/1.0 existant). C'est le caller qui écrit, jamais le gate.
3. **Brancher la décision** :
   - `PASS` (`shippable: true`) → persist normal, créa éligible au spend.
   - `FIX` avec un `block` fidélité (logo/produit re-généré) ET `assets_canonical.{slot}._validated_by_operator: true` présent → **auto-retry en `composite_mode: layered`** (HR3b · coller le vrai asset canon) puis re-gate. Généralise l'auto-trigger HR3.4 step 2 à la fidélité produit · c'est la boucle qui ferme le défaut logo.
   - `FIX` sans asset canon → persister avec `produced/{slug}.json#qc.passed: false` (non-shippable) + surfacer le `fix_list` à l'opérateur en langage métier (soft offer · canoniser le packshot / déposer le logo).
   - `KILL` → ne pas présenter comme prête ; proposer de recomposer (concept troué / produit faux).
4. **Jalon `shippable`** = dérivé (tous binaires fidélité-critique `qc.passed` + zéro blocking), DISTINCT de `validation_status` (cycle perf). Ne jamais marquer une créa spend-ready sans `qc-creative` PASS.

---

## HR3.4 · Adaptive retry policy (v1.0.2)

Calibrer `max_retry` selon complexité scène détectée à partir du prompt assemblé en HR3 :

- **Scène simple** (packshot studio uniquement, pas de model, pas de scene context, pas de props multiples) → `max_retry = 2` (default historique).
- **Scène complexe** (model + props multiples OU scene context narratif OU 2+ couches sub-label/duration_indicator/distinctive_features à préserver) → `max_retry = 3`.

**Sub-label / duration_indicator regression handling :**

Après les retries autorisés, si le wordmark principal (`label.wordmark_text`) est préservé MAIS le sub-label (`label.sub_label`) ou duration indicator (`label.duration_indicator`) reste flou ou illisible :
1. NE PAS continuer à retry (gain marginal, brûle budget API).
2. **v1.3+ auto-trigger layered mode si canonical asset disponible** · check `visual_identity.assets_canonical.{slot}._validated_by_operator: true` · si oui, redéclencher pipeline en `composite_mode: layered` (HR3b) plutôt que persister régression. Solution canonique au problème historique.
3. Si pas de canonical asset · persister la créa avec wordmark préservé + set `meta.label_compositing_required: true` dans `creative.json` (sous `brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json` · ce flag est de la traçabilité/lignage, il vit dans creative.json, PAS dans genome.json).
4. Note dans brief markdown S55 fiche v5 (Section 1, ligne Branding), langage métier · *"Petit texte sous le logo flou sur le packshot. Si on canonise une fois la photo produit officielle, ça sera net sur toutes les pubs suivantes."*
5. Flag explicite opérateur reco no-orphan, langage métier, soft offer · *"Logo principal préservé, mais le petit texte sous le logo est flou. Si tu veux, on peut canoniser le packshot une fois et le réutiliser sur toutes tes pubs (net garanti)."*

**Anti-pattern UX prose** · JAMAIS nommer `craft-packshot`, `compose-overlay-text`, `mode layered`, `HR3b`, `compositing` en surface operator. Soft offer + langage métier · "canoniser la photo produit", "réutiliser sur toutes tes pubs", "net garanti".

**Note v2.43+ scope shipped :** `compose-overlay-text` v2.43 fait le compositing PIL text overlay post-gen (sub-label, duration indicator, optional CTA badge). v2.47 ajoute layered mode HR3b in-skill · packshot collage pixel-exact upstream du text overlay (canonical asset + scène séparée). Deux outils complémentaires · layered = packshot, overlay-text = text crisp.

---

## HR3.5 · Post-gen aspect ratio normalize (v1.0.2)

Defensive primitive : même si HR3 step 3 passe `aspect_ratio` explicite, certains endpoints fal.ai (cas où l'opérateur override sur `nano-banana/edit` v0 sans suffixe, ou fallback API-side) peuvent retourner un ratio différent de la target.

**Procédure post-download :**

1. Lire dimensions image téléchargée (`/tmp/compose-creative/{brand}-{crt_id}.jpg`) via PIL.
2. Calculer ratio actuel `current_ratio = width / height`.
3. Calculer ratio target depuis param `aspect_ratio` envoyé en HR3 step 3 (ex `4:5` → `0.8`).
4. Si écart `|current_ratio - target_ratio| > 0.02` :
   - Crop centré via `PIL.Image.crop()` pour atteindre exactement le ratio target.
   - Préserver hauteur ou largeur selon laquelle dimension contraint (crop la plus large).
   - Sauvegarder over le fichier d'origine.
   - Note dans brief markdown S55 fiche v5 (Section 1, ligne Visuel généré) : *"auto-cropped {current_ratio} → {target_ratio} post-gen"*.
5. Si écart ≤ 0.02 → no-op, ratio déjà correct.

**Pas de retry fal.ai sur mismatch ratio.** Crop PIL est déterministe et instantané, retry fal.ai = gain marginal + coût API.

**Dépendance :** Python PIL (Pillow). Si absent dans l'env runtime, surface honnête à l'opérateur + persiste sans crop avec note `aspect_ratio_mismatch_unresolved` dans `meta`.

---

## HR-COMPOSITE · Mode selection full_regen vs layered (NEW v1.3)

Deux modes pour le pipeline visuel · `full_regen` (default historique HR3) régénère scène ET produit dans un seul call nano-banana-2. `layered` (NEW v1.3 · pattern studio photographer) sépare en 2 phases · scène générée sans produit + packshot canon collé pixel-exact via PIL paste.

**Decision rule.** Choisir `layered` si :

1. **Operator request explicite** · input contient `composite_mode: layered` OR phrase "studio photographer", "packshot canon", "fidélité critique", "preserve packshot".
2. **Canonical asset disponible** · `visual_identity.assets_canonical.{slot}._validated_by_operator: true` AND `_canonical: true` AND path file exists. Sans canonical asset → soft offer pull-not-push pattern (v2.50 NEW) · *"Pour faire ça en mode photo studio (packshot pixel-exact), j'aurais besoin d'une photo officielle du produit. Si tu en as une, drop-la. Si tu veux que je la prépare depuis ton site, dis-moi. Sinon je génère en mode classique (le produit peut bouger légèrement)."*. Operator décide · drop fichier OR fetch from URL OR fallback full_regen. Pas de "run craft-packshot d'abord" en surface (jargon skill name).
3. **Fidélité critique flag** · spec.identity.product_category ∈ {supplement, cosmetic, food, pharma} avec sub-label fin / badge plantes / claim certification / composition list visible. Ces produits = text fidelity blocker.
4. **Auto-trigger retry exhausted** · HR3.4 retry policy a flag `label_compositing_required: true` après 3 iter sur full_regen. Au lieu de surfacer opérateur "compositing externe recommandé" comme v1.2, v1.3 auto-trigger `layered` sur retry si canonical asset disponible (transparent fallback).

Choisir `full_regen` si :

1. Pas de canonical asset (craft-packshot pas encore run sur ce produit).
2. Scène narrative complexe avec produit en main de model OR en interaction physique (layered casse l'illusion · packshot collé ne tient pas dans une main convaincante).
3. Operator preference declared `composite_mode: full_regen`.

**Trade-off.** `layered` garantit packshot pixel-exact (substrat canonisé craft-packshot) MAIS scène autour générée sans produit peut sembler artificielle si la composition exigerait interaction (main qui tient, table contact réaliste, etc.). `full_regen` garantit cohérence visuelle scène-produit MAIS risque drift label (notre problème historique). Choisir selon priorité brand · text fidelity blocker → layered, narrative cohérence → full_regen.

**No false binary.** `layered` n'est pas "meilleur que" `full_regen` · c'est une alternative selon contexte produit. Pour packshot studio simple (90% des paid social Meta feed e-com), `layered` gagne. Pour lifestyle UGC narratif, `full_regen` gagne.

---

## HR3b · Pipeline layered compositing (NEW v1.3)

Activer si HR-COMPOSITE décide `composite_mode: layered`. Sinon skip et utiliser HR3 standard.

### Step 3b.1 · Génération scène-only via nano-banana-2

Prompt explicit "no product" pour générer background scène sans le produit ·

```
Empty professional photoshoot studio scene, soft lighting from the left,
{brand.atmosphere or audience.identity_signals depuis HR2 NOYAU},
clean composition with negative space center-bottom for product placement,
{angle.formula.tension surface en background context},
NO product, NO bottle, NO container, NO label, NO text overlay.
Format 4:5 vertical Meta feed.
```

Override aspect_ratio + resolution depuis input opérateur ou défauts HR3 step 3.

POST `https://fal.run/fal-ai/nano-banana-2/edit` MAIS sans `image_urls[]` (pure generation, pas edit) OR avec `image_urls=[]` ET prompt no-product explicite. Si endpoint refuse empty image_urls, fallback `nano-banana-2/text-to-image` (non-edit variant) si dispo, ELSE pass un mood reference scène vide pertinent.

Download résultat dans `/tmp/compose-creative/{brand}-{crt_id}-scene.jpg`.

### Step 3b.2 · Lookup canonical packshot path

1. Read `brands/{slug}/products/{product_slug}/visual_identity.json#assets_canonical.{slot}` (slot default `front`).
2. Verify `_validated_by_operator: true` AND `_canonical: true` AND `path` exists on filesystem.
3. Si absent ou flag false → **soft offer pull-not-push (v2.50)** au lieu de refuser. Langage métier, jamais nommer le skill ·

   > *"Pour faire la pub en photo studio (produit pixel-exact), il me faut une photo officielle du {product_name}. Trois options ·*
   > *(a) Tu as un fichier en local ? Drop-le.*
   > *(b) Je peux la récupérer depuis ton site et la préparer (1-2 min).*
   > *(c) Je génère en mode classique (le produit peut bouger légèrement vs photo officielle)."*

   Operator décide. Skill chain l'option choisie. Jamais bloquant.

   **Bridge code (v2.51 NEW · câblage explicite Task tool params)** ·

   Selon la réponse operator, l'agent invoke concrètement ·

   - **Option (a) drop fichier local** · operator drop path absolu d'un fichier image. Skill consume direct ·
     ```
     Lecture du fichier path operator + verify format (png/webp/jpg) + verify resolution (min 2048x2048 recommandé).
     Persist via Edit/Write dans visual_identity.json#assets_canonical.packshot_front avec _validated_by_operator: true uniquement APRÈS gate explicit operator validation Step 5 craft-packshot symétrique.
     Si quality assessment 8 critères < 6/8 pass · surface warning operator + propose re-upload.
     ```

   - **Option (b) récupère depuis ton site** · invoke `craft-packshot` skill via Task tool · params concrets ·
     ```
     Task tool invocation ·
     - description · "Génère packshot canonique {product_humain}"
     - subagent_type · "general-purpose" (le skill craft-packshot recommended_model: sonnet, subagent_safe: true)
     - prompt · "Run craft-packshot pour {brand_slug}/{product_slug}. Mode scrape_from_official_site. Brand URL · {brand.identity.website}. Aspect ratio · 1:1. Resolution · 2K. Output path canonique · brands/{brand_slug}/products/{product_slug}/assets/packshot-canonical-front-{date}-gen-v1.png. Skill flow standard 7 steps · scrape carousel → score → pick source → compose prompt → fal.ai nano-banana-2/edit → quality 8 critères → operator gate Step 5 → persist visual_identity.json. Return absolute path canonical asset post-validation."
     ```
     Wait completion. Re-read `visual_identity.json#assets_canonical.packshot_front` post-completion. Si `_validated_by_operator: true` AND path file exists · continue pipeline Step 3b.3 layered composite. Si operator a rejected dans craft-packshot Step 5 gate · fallback option (c).

   - **Option (c) génère en mode classique** · fallback `composite_mode: full_regen` · skip HR3b layered, route vers HR3 standard pipeline.

5. Path absolu canonical asset · `brands/{slug}/products/{product_slug}/{path}` (relative dans visual_identity.json).

### Step 3b.3 · PIL composite paste + soft drop shadow

```python
from PIL import Image, ImageFilter
import os

def layered_composite(
    scene_path,
    packshot_path,
    output_path,
    scale_factor=0.65,
    position=("center", 0.62),
    shadow_offset=(0, 20),
    shadow_blur=35,
    shadow_opacity=0.35
):
    """
    scene_path · jpg scene-only (Step 3b.1 output)
    packshot_path · png canonical packshot (Step 3b.2 lookup)
    scale_factor · packshot height / scene height (0.0-1.0, default 0.65)
    position · (horizontal, vertical_pct) · horizontal ∈ {center, left, right} ou int px, vertical_pct ∈ 0.0-1.0
    shadow_offset · (dx, dy) px shadow displacement
    shadow_blur · gaussian blur radius shadow
    shadow_opacity · 0.0-1.0 shadow alpha
    """
    scene = Image.open(scene_path).convert("RGBA")
    packshot = Image.open(packshot_path).convert("RGBA")

    # Threshold white background to alpha if packshot has white bg (canonical asset convention)
    if packshot.mode == "RGBA":
        data = packshot.getdata()
        new_data = []
        for px in data:
            r, g, b, a = px
            if r > 245 and g > 245 and b > 245:
                new_data.append((r, g, b, 0))
            else:
                new_data.append((r, g, b, a))
        packshot.putdata(new_data)

    # Resize packshot to target height
    target_height = int(scene.size[1] * scale_factor)
    aspect = packshot.size[0] / packshot.size[1]
    target_width = int(target_height * aspect)
    packshot_resized = packshot.resize((target_width, target_height), Image.LANCZOS)

    # Position
    horizontal, vertical_pct = position
    if horizontal == "center":
        x = (scene.size[0] - target_width) // 2
    elif horizontal == "left":
        x = int(scene.size[0] * 0.15)
    elif horizontal == "right":
        x = int(scene.size[0] * 0.85) - target_width
    else:
        x = int(horizontal)
    y = int(scene.size[1] * vertical_pct) - target_height // 2

    # Generate soft drop shadow
    shadow = Image.new("RGBA", scene.size, (0, 0, 0, 0))
    shadow_mask = packshot_resized.split()[3] if packshot_resized.mode == "RGBA" else None
    if shadow_mask:
        shadow_layer = Image.new("RGBA", packshot_resized.size, (0, 0, 0, int(255 * shadow_opacity)))
        shadow.paste(shadow_layer, (x + shadow_offset[0], y + shadow_offset[1]), shadow_mask)
        shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))

    # Composite · scene + shadow + packshot
    composite = Image.alpha_composite(scene, shadow)
    composite.paste(packshot_resized, (x, y), packshot_resized)

    # Convert RGBA → RGB for jpeg save
    composite_rgb = Image.new("RGB", composite.size, (255, 255, 255))
    composite_rgb.paste(composite, mask=composite.split()[3] if composite.mode == "RGBA" else None)
    composite_rgb.save(output_path, "JPEG", quality=92)

    return output_path
```

Defaults tuning ·
- `scale_factor: 0.65` · packshot occupe 65% hauteur scène, laisse air respiration top
- `position: ("center", 0.62)` · centré horizontalement, légèrement bas (règle des tiers)
- `shadow_offset: (0, 20)` · ombre légère décalée bas
- `shadow_blur: 35` · doux, pas hard edge
- `shadow_opacity: 0.35` · subtle, pas dramatique

Override possibles via operator input ou angle.formula.observation context (ex angle "produit en main" → layered probablement pas optimal, fallback HR3 full_regen).

### Step 3b.4 · Output composite

Save final composite dans `/tmp/compose-creative/{brand}-{crt_id}.jpg` (replace scene-only temp file · staging éphémère). Path final downstream HR3 step 5 standard · move vers `brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg` (binaire écrit DIRECT) + émettre le sidecar `produced/{slug}.json` via `write_to_context` mode=proposed (mode layered produit aussi un binaire qui DOIT être manifest-tracé · même régime que HR3 step 5). Le production-how (endpoint, params, canonical asset path) vit dans le sidecar (= le manifest = COMMENT le binaire a été fabriqué), PAS dans creative.json.

Note dans le sidecar `produced/{slug}.json` (produced-asset/1.0) · le COMMENT-le-binaire-a-été-fait ·
- `tool: "fal"` + `endpoint: "fal-ai/nano-banana-2/edit"`
- `params: {composite_mode: "layered", scale_factor, position, shadow_offset, shadow_blur, shadow_opacity}`
- `source_asset_ref: {kind: "scraped_packshot", path: <canonical asset path relative>}` (+ `composite_canonical_asset_validated_at: <date depuis visual_identity.json>` en additif)
- `status: "generated"`, `created_at`, `genome_ref: <script_id GSC-NN>`

(Stratégie-pourquoi reste dans creative.json ; production-comment dans le sidecar. Si laissé dans creative.json, le sidecar serait vide et la valeur anti-orphelin perdue.)

**Avantage layered.** Text fidelity 100% (packshot canonisé craft-packshot · 8/8 quality check pass déjà validé opérateur). Pas de retry budget burned sur label preservation. Pipeline déterministe sur produit · stochastique uniquement sur scène.

**Limite layered.** Composition narrative limitée · packshot ne peut pas tenir convaincante dans main de model OU être en interaction physique réaliste avec props scène. Pour ces cas, fallback HR3 full_regen.

### Step 3b.5 · Multi-layer paste optional (NEW v1.4 · packshot + logo + badge)

Si `visual_identity.assets_canonical` contient aussi `logo_canonical._validated_by_operator: true` AND/OR `badge_canonical.{slug}._validated_by_operator: true`, layered mode supporte multi-layer paste pour ad complet branded pixel-exact.

**Input opérateur** · `composite_layers[]` array ordered, default `["packshot"]` (Step 3b.3 standard single-layer). Extensions ·
- `["packshot", "logo"]` · packshot center-bottom + logo bottom-right
- `["packshot", "badge:cert_plantes_naturelles"]` · packshot + badge top-left
- `["packshot", "logo", "badge:cert_plantes_naturelles"]` · les 3 ensembles
- Order = z-index render (premier paste = derrière, dernier = devant)

**Layer config defaults** ·

| Layer | Slot lookup | Default position | Default scale | Shadow |
|---|---|---|---|---|
| `packshot` | assets_canonical.packshot_front | (center, 0.62) | 0.65 (% scene height) | enabled (offset 0,20 · blur 35 · opacity 0.35) |
| `logo` | assets_canonical.logo_canonical | (right, 0.92) bottom-right | 0.12 | disabled (logos = no shadow typiquement) |
| `badge:{slug}` | assets_canonical.badge_canonical.{slug} | (left, 0.10) top-left | 0.10 | disabled |

Operator peut override chaque param via input dict ·
```
composite_layers: [
  {"type": "packshot", "scale": 0.7},
  {"type": "logo", "variant": "monochrome_white", "position": ["right", 0.95]},
  {"type": "badge", "slug": "cert_plantes_naturelles", "position": ["left", 0.08], "scale": 0.12}
]
```

**Extension PIL code** ·

```python
def multi_layer_composite(
    scene_path,
    layers_config,
    output_path,
    visual_identity_assets_canonical
):
    """
    scene_path · jpg scene-only output Step 3b.1
    layers_config · array ordered de {type, slug, variant, position, scale, shadow}
    visual_identity_assets_canonical · dict des assets canonical lus depuis visual_identity.json
    """
    scene = Image.open(scene_path).convert("RGBA")
    composite = scene.copy()

    for layer in layers_config:
        layer_type = layer["type"]

        # Resolve slot path
        if layer_type == "packshot":
            slot = visual_identity_assets_canonical.get("packshot_front", {})
            asset_path = slot.get("path")
        elif layer_type == "logo":
            slot = visual_identity_assets_canonical.get("logo_canonical", {})
            variant_name = layer.get("variant", "primary")
            asset_path = next(
                (v["path"] for v in slot.get("variants", []) if v["name"] == variant_name),
                slot.get("path")
            )
        elif layer_type == "badge":
            badges = visual_identity_assets_canonical.get("badge_canonical", {})
            slug = layer["slug"]
            slot = badges.get(slug, {})
            asset_path = slot.get("path")
        else:
            continue  # unknown layer type skipped

        if not asset_path:
            # Slot empty · soft offer pull-not-push pattern v2.50
            # Avant skip silencieux v1.4, maintenant v1.4.1+ surface gap à operator
            # avec offer fetch from URL OR drop OR skip
            missing_layers.append({
                "type": layer_type,
                "slug": layer.get("slug"),
                "variant": layer.get("variant"),
                "humain_label": _humain_label_from_layer(layer_type, layer)
            })
            continue  # skip ce layer pour l'instant, on surface après tous les layers

        # Load + apply white→alpha threshold (canonical asset convention)
        asset = Image.open(asset_path).convert("RGBA")
        if slot.get("background") == "white":
            data = asset.getdata()
            new_data = [(r, g, b, 0) if (r > 245 and g > 245 and b > 245) else (r, g, b, a) for r, g, b, a in data]
            asset.putdata(new_data)

        # Resolve params (operator override > defaults per layer type)
        defaults = {
            "packshot": {"scale": 0.65, "position": ["center", 0.62], "shadow": True},
            "logo": {"scale": 0.12, "position": ["right", 0.92], "shadow": False},
            "badge": {"scale": 0.10, "position": ["left", 0.10], "shadow": False}
        }
        cfg = {**defaults[layer_type], **layer}

        # Resize
        target_height = int(scene.size[1] * cfg["scale"])
        aspect = asset.size[0] / asset.size[1]
        target_width = int(target_height * aspect)
        asset_resized = asset.resize((target_width, target_height), Image.LANCZOS)

        # Position
        horizontal, vertical_pct = cfg["position"]
        if horizontal == "center":
            x = (scene.size[0] - target_width) // 2
        elif horizontal == "left":
            x = int(scene.size[0] * 0.05)
        elif horizontal == "right":
            x = int(scene.size[0] * 0.95) - target_width
        else:
            x = int(horizontal)
        y = int(scene.size[1] * vertical_pct) - target_height // 2

        # Shadow if enabled
        if cfg["shadow"]:
            shadow_layer = Image.new("RGBA", asset_resized.size, (0, 0, 0, int(255 * 0.35)))
            shadow_canvas = Image.new("RGBA", scene.size, (0, 0, 0, 0))
            shadow_canvas.paste(shadow_layer, (x, y + 20), asset_resized.split()[3])
            shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(35))
            composite = Image.alpha_composite(composite, shadow_canvas)

        # Paste layer
        composite.paste(asset_resized, (x, y), asset_resized)

    # Convert RGBA → RGB for jpeg save
    composite_rgb = Image.new("RGB", composite.size, (255, 255, 255))
    composite_rgb.paste(composite, mask=composite.split()[3] if composite.mode == "RGBA" else None)
    composite_rgb.save(output_path, "JPEG", quality=92)

    return output_path
```

**Missing layers handling (v2.50 NEW · soft offer pull-not-push)** ·

Si `multi_layer_composite()` rencontre un layer dont le slot canonique est vide (ex operator demande `composite_layers: ['packshot', 'logo', 'badge:cert_plantes_naturelles']` mais `logo_canonical` empty), v1.4.1+ pattern · build la créa avec les layers disponibles, puis surface gap à operator avec soft offer en fin de pipeline ·

> *"Pub générée avec ton packshot. J'ai pas trouvé ton logo brand ni le badge "cert plantes naturelles" en version officielle. Si tu veux, je peux les récupérer depuis ton site (1-2 min) pour les ajouter cette pub et toutes les suivantes."*

Operator décide ·
- (a) **Récupère depuis le site** · skill chain l'import des assets manquants puis re-compose
- (b) **Drop fichier(s) local** · skill consume immédiatement et re-compose
- (c) **Skip pour cette pub** · la créa actuelle est OK comme ça
- (d) **Skip pour toujours** · ces layers ne sont pas pertinents pour cette brand (flag opérateur preference, plus de relance)

Pas blocking. Pas refuser. Pas push. Soft offer 1 fois, operator passe à autre chose si pas pertinent. Jamais nommer les skills (import-asset / extract_from_url) en surface.

**Bridge code (v2.51 NEW · câblage explicite Task tool params)** ·

Selon réponse operator, l'agent invoke concrètement ·

- **Option (a) Récupère depuis le site** · pour chaque layer manquant dans `composite_layers_missing[]`, invoke `import-asset` skill via Task tool · params concrets ·
  ```
  Task tool invocation par layer manquant ·
  - description · "Récupère {label_humain_layer} depuis site brand"
  - subagent_type · "general-purpose" (import-asset recommended_model: sonnet, subagent_safe: true)
  - prompt · "Run import-asset Mode C extract_from_url pour {brand_slug}. Brand URL · {brand.identity.website}. Asset type · {layer.type} (logo OU badge selon layer demandé). Pour badge · slug {layer.slug} (ex cert_plantes_naturelles). Mode C workflow standard 4 sub-steps (C.1 scrape HTML, C.2 extract candidats heuristics par type, C.3 download + rasterize SVG fallback chain, C.4 operator gate validation). Return path canonical asset post-validation."
  ```
  Wait completion par layer. Re-read `visual_identity.json#assets_canonical.{slot}` post-completion. Si peuplé + validé · re-trigger `multi_layer_composite()` pour re-compose la pub avec les layers maintenant disponibles. Si operator rejected dans import-asset HR4 gate · skip ce layer pour cette pub (l'overlay sera incomplet pour cette créa, OK).

- **Option (b) Drop fichier(s) local** · pour chaque layer manquant, AskUserQuestion path absolu fichier. Pour chaque fichier dropé, invoke `import-asset` Mode A direct · ·
  ```
  Task tool ·
  - prompt · "Run import-asset Mode A operator_drop_local_path pour {brand_slug}. Asset type · {layer.type}. Slug si applicable · {layer.slug}. File path · {operator_drop_path}. Quality assessment 5 critères + operator gate HR4."
  ```
  Wait completion. Re-trigger multi_layer_composite() avec layers maintenant peuplés.

- **Option (c) Skip pour cette pub** · finalize la créa actuelle telle quelle (build sans layers manquants). Meta `composite_layers_missing[]` log pour audit. No re-compose.

- **Option (d) Skip pour toujours** · flag dans `brands/{slug}/brand.json#preferences.composite_layers_skip` array avec entries `{type, slug}`. Future invocations compose-creative layered ne re-proposent plus ces layers pour cette brand. Finalize créa actuelle. Cohérent operator decision · pas tous les brands ont logo/badge pertinents.

Pas de "run import-asset Mode C" en surface operator. Le bridge code ci-dessus est instruction agent-facing pour câblage runtime, jamais leak operator.

**Meta logged additif** · le binaire composite final multi-layer est tracé par SON sidecar `produced/{slug}.json` (produced-asset/1.0). Chaque champ de prod va dans le manifest, pas dans creative.json ·
- `params.composite_layers: [...]` (array ordered des layers appliqués avec params résolus) → sidecar
- `params.composite_layers_assets_paths: [...]` (paths absolus pour audit) → sidecar ; les assets sources (packshot/logo/badge) sont référencés depuis visual_identity, pas re-tracés ici
- `params.composite_layers_missing: [...]` (array layers demandés mais slot vide, surface à operator v2.50+) → sidecar
- `status: "generated"`, `created_at`, `genome_ref: <script_id GSC-NN>` → sidecar (chaque binaire composite final obtient son sidecar)

**Workflow recommandé v2.48** ·
1. `craft-packshot` upstream → canonical packshot validé
2. `import-asset` pour logo + badge cert plantes
3. `compose-creative composite_mode: layered composite_layers: [packshot, logo, badge:cert_plantes_naturelles]` → ad complet pixel-exact branded

Avantage multi-layer · pubs avec branding complet (packshot + logo + badge cert) tous pixel-exact, réutilisation cross-pubs sans regen. Limite · si scene a composition complexe (model holding produit), packshot collé tient pas. Fallback `composite_mode: full_regen` pour ces cas (mais perd fidélité branding).

---

## HR4 · Génération brief markdown S55 fiche v5 forward

Format opérateur-facing structuré (équivalent decompose-ad output, mode forward).

**Section 1 · CE QUE LA CRÉA VA MONTRER** (projection visuelle objective)

| Champ | Contenu |
|---|---|
| Format | `static_image | carousel | video_short | reel | story` + ratio + langue |
| Hook visuel | Description scène depuis HR2 NOYAU stop_scroller.visual_layer |
| Hook texte | Verbatim généré, max 8 mots, formule depuis canon hooks |
| Body | Description body description (si présent) |
| CTA texte | Verbatim button label + texte autour |
| Branding | Logo position, packshot oui/non, couleur dominante (hex), font signal |
| Visuel généré | Staging `/tmp/compose-creative/{...}.jpg` → `creatives/{batch}/{CRT-NN}/produced/{slug}.jpg` (binaire + sidecar `produced/{slug}.json`) |

**Section 2 · CE QUE LA CRÉA RACONTE** (intention stratégique)

| Champ | Contenu |
|---|---|
| Cible | Phrase plain language depuis profile (persona type + buyer_user_split) |
| Niveau conscience | Schwartz double-stage (entrée + sortie visée) |
| Vérité non-dite | Insight depuis angle.formula.observation+tension, modalité formulee/implicite/absente |
| Angle d'attaque | Levier × positionnement-contre × promesse depuis angle.formula synthèse |
| Mécanique | Nom registry + 1 phrase explicative |
| Pivot du concept | Atome irréductible entre guillemets + 1 phrase justification |

**Section 3 · DIAGNOSTIC PRÉDICTIF**

- Cohérence chaîne : audience → insight → angle → mécanique → craft. Chaque transition `tient | tension | casse`. Verdict global + 1 phrase.
- Score arrêt-scroll prédit : 1-5, ancré sur observables Section 1 (densité visuelle, contraste feed, rupture pattern, charge cognitive, signature ton).
- Forces : 3-5 bullets observables (pas d'éloge vague, nommer le mécanisme).
- Risques : 3-5 bullets (légal, brand, audience, execution).

**Section TAGS RETRIEVAL** : tous les axes du schema, snake_case strict.

---

## HR5 · Persist split genome.json + creative.json + sidecar + brief.md (Brique 4 étape B)

> Le mkdir-claim atomique (réservation du `{CRT-NN}/`) est exécuté en **STEP 0 de HR-CC-CANON-1** (section ci-dessous), AVANT cette persist. HR5 écrit dans le dossier déjà réservé.

L'unique `creative.json` historique se SPLIT en trois fichiers `.json` (+ le brief `.md`), chacun conforme à son schéma. Mapping champ→fichier = celui des schémas (`genome.schema.json` ADN, `creative.schema.json` lignage, `produced-asset.schema.json` sidecar).

**genome.json** (ADN · conforme `genome.schema.json` `_schema_version: "genome/1.2"`, strictement nu, aucun costume `_field_types`) ·
- `script_id` : `GSC-NN` (Genome SCript · clé de join perf future · PAS CRT-NN · pattern `^GSC-[0-9]{2,4}$`).
- `support` : `static | carousel | video` (depuis HR2 `format`).
- `route` : `route_a_full_ia` (default forward) ou `route_b_export_brief`.
- `hook` : `{mechanic_id (enum), hook_text}` depuis HR2 NOYAU stop_scroller + canon hooks. `hook.visual` optionnel (first-frame stop-scroll).
- `frames` : tableau ordonné copy+visuel (static = 1 frame, carousel/video = 2+). Chaque frame `{role (beat_type), copy_script, visual_script}`.
- `genome_tags` : `{support, mechanic_id, primary_style_id}` requis + `beat_type_sequence` (projection plate des `frames[].role`) + **`mecanique_id`** (le CONCEPT ad-level choisi en HR2 · → `creative-mechanics-registry` SSOT · DISTINCT du `mechanic_id` HOOK · pont A=B sur l'axe concept · D#491) + **`angle_id`** (l'ANGLE ANG-NN choisi en HR2 = unité STRATÉGIQUE de 1ère classe · porte l'objection [via `angle.lineage.objection_ref`] + l'OTRB + le payoff [via l'audience] · joignable à la perf · D#492) + **`audience_slug`** (porte le dream_scenario) + `awareness_level` recommandés.
- `lineage` (optionnel ADN abstrait) : `{concept_id, angle_id (ANG-NN), persona_label}`.

**creative.json** (lignage · conforme `creative.schema.json` `_schema_version: "creative/1.4"`) ·
- `creative_id` : `CRT-NN` (réservé par mkdir-claim STEP 0 · pattern `^CRT-[0-9]{2,3}$`).
- `mode` : `concept | template | asset`. `audience_slug`. `_equation_ref` const v3.1.
- `concept_id` : nouveau `cpt_{brand_slug}_{angle_short}_{NNN}` (SSOT du groupage de variantes).
- `variant_of` : `null` (source canonique) ou `CRT-NN`/`RCV-NN` du parent si dérivé. `variant_axis` : enum canonique `[photo_swap, promo_toggle, hook_swap, background_swap, persona_split, null]`.
- `lineage{}` : `{angle_ref (ANG-NN), audience_ref, product_ref, mechanism_ref, concept_ref, variant_of, brief_ref (BRF-NN), ad_id}`.
- `intent_mix` (multi-weighted depuis HR2). Champ legacy `intent` mirror backward-compat.
- `execution.overlay_density` (0.0-1.0) + `execution.brand_mark_present` (bool). Champ legacy `craft_mode` mirror dérivé.
- `meta.validation_status` (object composite) : `{status: "hypothesis", confidence: 0.5, confidence_source: "default"}` (créa pas encore testée). `meta.created`. `meta.created_by_skill: "compose-creative"`. `meta.test_results[]` empty.
- `performance.longevity_signal` vide (pas encore en prod). `tags.source: "internal_production"`.

**produced/{slug}.json** (sidecar manifest binaire · conforme `produced-asset.schema.json` `_schema_version: "produced-asset/1.0"`) · UN sidecar par binaire `.jpg` produit (anti-orphelin) ·
- `asset_role` (ex `"composite-final"`, `"first-frame-hook"`), `file` (ex `"{slug}.jpg"`), `status: "generated"`, `created_at` requis.
- `tool: "fal"`, `endpoint: "fal-ai/nano-banana-2/edit"`, `params` (prompt/aspect_ratio/resolution + composite params si layered), `source_asset_ref`, `hash` optionnel, `qc` optionnel.
- `genome_ref` : `<script_id GSC-NN>` (relie le binaire à l'ADN sans le dupliquer).

**Mutation gate (séquence) :**

1. **Dossier déjà réservé** par le mkdir-claim atomique STEP 0 (HR-CC-CANON-1) · `creatives/{batch}/{CRT-NN}/` + `produced/` existent. NE PAS s'appuyer sur le `mkdir(exist_ok=True)` du gate (non-atomique · 2 runs concurrents écraseraient le même `CRT-NN`).
2. Write `genome.json` + `creative.json` + sidecar `produced/{slug}.json` via `write_to_context(field_path, value, source, confidence, mode="proposed")` (les trois `.json`). **NEVER edit JSON directly via Edit/Write/NotebookEdit.**
3. Persist JPG : move `/tmp/compose-creative/{brand}-{crt_id}.jpg` → `brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg`. **Le binaire `.jpg`/`.mp4` est écrit DIRECT** (`write_to_context` ne gère que le `.json`), MAIS son sidecar `.json` (step 2) passe par le gate. Double régime non-négociable.
4. Write brief markdown : `brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md` (nom fixe `brief.md`, format S55 fiche v5 forward). **Écrit DIRECT via l'outil Write** (`.md` n'est NI dans `ALLOWED_PATH_PATTERNS` du gate write-to-context, NI dans mutation-guard qui ne garde que `.json`) · ne PAS router le `.md` via `write_to_context` (échouerait).
5. Si `mecanique_id == "other"` → emit event `mecanique_proposal_flag` avec payload `{observed_mecanique_signature, ad_creative_id, registry_gap_description}`.
6. Trigger `validate-resources` silencieusement post-write (valide genome + creative + sidecar contre `genome.schema.json` / `creative.schema.json` / `produced-asset.schema.json`, et la forme de path contre `ALLOWED_PATH_PATTERNS`). Flag MAJOR/CRITICAL à l'opérateur si remonte.

---

## HR-CC-CANON-1 · Entry canonical batch + mkdir-claim (Brique 4 étape B · exécutable)

> Cette règle était déclarée en frontmatter (`patch_notes_v2_87_4`) mais JAMAIS exécutée. Elle est ici MATÉRIALISÉE en section réelle. Toute génération créa DOIT créer son dossier canonique `brands/{slug}/creatives/{batch}/{CRT-NN}/` AVANT tout write, persister le split (genome + creative + sidecar + brief), et interdire tout asset orphelin hors structure. Cross-ref `resources/conventions/creative-storage.md` (D#481).

### Refus AVANT claim (ordre HR7)

Tous les refus HR7-style (HR7 anti-pattern 1 · `packshots.primary_front` absent dans les 2 paths · HR7 anti-pattern 3 · `angle.json` absent / `formula` vide · `FAL_API_KEY` absent) s'exécutent **AVANT STEP 0c**. Un run refusé ne doit JAMAIS laisser un dossier `CRT-NN/` réservé vide. La claim atomique ne se prend qu'une fois la génération garantie possible.

### STEP 0 · mkdir-claim atomique (AVANT tout write_to_context)

Le mkdir-claim s'exécute en **STEP 0**, juste avant la génération visuelle persistée (HR3/HR3b produisent le binaire en `/tmp` ; HR5 persiste dans le dossier réservé ici).

**STEP 0a · résoudre {batch}.** `{batch}` = run date-stampé du jour, lowercase + chiffres + tirets (regex gate `[a-z0-9-]+`). Default = `$(date +%Y-%m-%d)-NN` où NN = prochain run 2-digit du jour. Résoudre NN · lister `brands/{slug}/creatives/` pour les dossiers matchant `$(date +%Y-%m-%d)-*`, prendre le max suffixe, sinon `01`. Un run PEUT réutiliser le batch de session déjà ouvert. `mkdir -p brands/{slug}/creatives/{batch}/` (idempotent · le dossier-batch n'est PAS la claim).

**STEP 0b · candidat CRT-NN (scan max cross-batch).** Scanner TOUT l'arbre du namespace CRT pour le max existant, PAS juste le batch courant (les id sont globalement uniques dans le namespace CRT, batch-indépendants) ·
```
ls -d brands/{slug}/creatives/*/CRT-* 2>/dev/null | grep -oE 'CRT-[0-9]{2,4}' | sort -t- -k2 -n | tail -1
```
→ N. Candidat = `CRT-(N+1)`, zero-paddé à ≥2 digits. CRT scanné SÉPARÉMENT de RCV (jamais fusionnés · RCV = namespace concurrent decompose-ad).

**STEP 0c · claim atomique.** `mkdir brands/{slug}/creatives/{batch}/CRT-{N+1}/` SANS `-p` sur le segment final (le parent `{batch}/` existe déjà depuis 0a). `mkdir` sur un dossier existant échoue → **c'est le verrou** (la réservation). Sur succès · l'id est à toi, immédiatement `mkdir -p brands/{slug}/creatives/{batch}/CRT-{N+1}/produced/`. Sur EEXIST · `N = N+1`, retry (boucle bornée, ex 50 essais). C'est le SEUL mécanisme de réservation · pas de fichier-index, pas de lock-file, pas d'écrivain privilégié. Les trous d'id sont inoffensifs (unicité requise, pas absence-de-trou).

> **PIÈGE (vérifié source · write-to-context.py L453 `target.parent.mkdir(parents=True, exist_ok=True)`)** · ce mkdir du gate n'est PAS une claim atomique. Si un skill saute STEP 0c et compte sur le mkdir du gate, deux runs concurrents passent tous les deux et écrivent dans le MÊME `CRT-NN`, clobbering silencieux. Le `mkdir` atomique (sans `exist_ok`) DOIT être fait par le skill en STEP 0c.

**STEP 0d · write dans le dossier réservé.** MAINTENANT (HR5) · `write_to_context` les trois `.json` (`genome.json`, `creative.json`, sidecar `produced/{slug}.json`) en mode=proposed. Binaires (.jpg/.mp4) déplacés DIRECT sous `.../produced/` (write_to_context ne gère que le json). `brief.md` écrit DIRECT (outil Write · `.md` exempt de `ALLOWED_PATH_PATTERNS` ET de mutation-guard).

### Lignage 5-refs obligatoire

`creative.json#lineage` doit être populé · `angle_ref` (ANG-NN) + `audience_ref` + `product_ref` + `mechanism_ref` + `concept_ref` (miroir descriptif de `concept_id`, SSOT groupage = `creative.concept_id` top-level). `variant_of` (CRT-NN/RCV-NN) si dérivé. Cross-refs many-to-many activés.

### Interdit orphelin

JAMAIS sauver un asset JPG/PNG standalone hors structure (e.g. `visual-identity/creative_ANG-01_*.jpg` orphelin). TOUT binaire vit sous `creatives/{batch}/{CRT-NN}/produced/` AVEC son sidecar `produced/{slug}.json` (manifest gated). Pas de binaire sans sidecar (anti BUG-ASSET-ORPHAN). Pas d'entry créa sans genome.json + creative.json.

---

## HR5bis · Persist next-step + tick upstream (v1.9.2, additif strict)

Ce skill est aval de `produce-copy-brief` et `produce-paid-angles` · son artifact ferme une boucle ouverte en amont, et il ouvre lui-même la boucle suivante. Deux gestes légers idempotents, exécutés après HR5 (persist split OK) et avant HR6 (output). Aucun ne bloque la livraison de la créa · le binaire + la fiche restent la sortie primaire.

Pattern déjà prouvé par `register-and-flag` Step 6 (write idempotent d'une ligne de tracking dans `brands/{slug}/todos.md`).

**Geste A · tick la ligne amont (fermeture de boucle).** Scanner `brands/{slug}/todos.md → ## In Progress`. Si une ligne y désigne `compose-creative` comme skill aval avec la même cible (même brief BRF-NN / même angle ANG-NN / même audience que ce run · ex `- [ ] compose-creative sur le brief BRF-04 | P: 1 | E: med | T: quelques heures`), basculer la case `[ ]` → `[x]` (puis archivage selon la doctrine todos racine). C'est l'auto-tick que `produce-copy-brief` Step 8bis et `produce-paid-angles` Step 12ter attendent de l'aval. Aucune ligne ne matche → ne rien faire, continuer (silencieux). Jamais de tick manuel.

**Geste B · persister son propre next-step.** Le close (HR6) recommande un move (tester sur Meta · décliner la créa en variants · passer le gate qc-creative avant spend). Cette reco vit dans le chat et meurt au prochain tour si rien ne la fixe. Lui donner une trace · une ligne dans `## In Progress` au **format de ligne canonique** ·

```
- [ ] {Name} | P: {0-3} | E: {low|med|high} | T: {durée}
```

- `Name` · le soft offer du close verbalisé court, sans nommer de skill interne en surface opérateur MAIS nom de skill aval recevable dans la ligne todo (réceptacle backstage, pas surface). Ex `tester la créa CRT-12 sur Meta audience principale`, `décliner CRT-12 en 2 variants hook`, `qc-creative gate avant spend sur CRT-12`.
- `P` · priorité dérivée · créa qc-PASS prête au spend → `P: 1` · déclinaison optionnelle → `P: 2`.
- `E` · effort du move aval (low pour un lancement test, med pour une déclinaison, high pour un batch complet).
- `T` · ETA aligné `feedback_client_effort_scale` si client-facing (ex `quelques heures`, `demi-journée`).

**Idempotence (dure, comme register-and-flag).** Avant d'écrire, scanner `## In Progress` · si une ligne porte déjà le même `Name`, ne pas dupliquer. Re-run de la même créa = zéro nouvelle ligne. Les deux gestes passent par le mutation gate ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/todos.md#in-progress" --value "- [ ] {Name} | P: {n} | E: {level} | T: {eta}" --source agent --mode direct --reason "Persist recommended next-step from compose-creative close (idempotent)"
```

Si `write-to-context.py` ne route pas le markdown todos, fallback `register-and-flag` (sous-skill curator) · même réceptacle, même idempotence. Ne JAMAIS hand-editer le markdown todos hors gate (cohérent HR7 anti-pattern 4 · `.json` par le gate · ici le `.md` todos passe aussi par le canal canonique, pas Edit/Write direct).

**Léger, jamais bloquant.** Échec d'un write (gate refuse, fichier absent) → flag interne silencieux, ne casse pas le ship de la créa. La trace todo est un bonus de persistance, pas une précondition.

**Doctrine.** Report des étapes différées et matérialisation des next-steps comme tâches reprenables avec leur levier · `docs/system/onboarding-setup-flow.md` (sections « Exhaustivité offerte, jamais forcée, reportable » et « La persistance est native »). Référencée ici, pas redupliquée.

---

## HR6 · Output operator-facing

Render fiche markdown selon format S55 fiche v5 forward (template ci-dessous). Vocabulaire opérateur uniquement, pas plumbing. Pas `intent_mix: {primary: DR}`, dire `Type de campagne : direct response`. Pas `overlay_density: 0.6`, dire `Cadrage : hook + claim layered sur packshot`.

**No orphan output.** Terminer sur 1 reco douce (soft offer) ancrée sur ce qui vient d'être composé. Langage métier zéro jargon technique, jamais nommer de skill ni concept interne.

- Chaîne cohérente · *"Cette créa est cohérente. Si tu veux, on peut la tester sur Meta avec ton audience principale."*
- Hypothèse non-validée · *"Pas encore certain que cet angle va marcher. Si tu veux, on peut tester 2 angles en parallèle pour voir lequel performe."*
- Variantes possibles · *"Si tu veux, on peut décliner cette créa (autre hook, autre persona, autre plateforme) sans tout refaire."*
- Photo produit manque · *"Il manque une photo officielle du produit pour vraiment bien faire. Si tu en as une, drop-la, sinon on peut la générer."*

**Anti-pattern UX prose** · JAMAIS nommer `compose-creative`, `recompose-creative`, `define-specs`, `photo_swap`, `hook_swap`, `persona_split`, `Visual_identity` en surface operator. Soft offer langue métier · "tester", "décliner", "drop-la", "photo officielle".

Une reco forte, pas trois équivalentes.

---

## HR7 · Anti-patterns

1. **Compose sans visual_identity.** Régression label garantie sous 2 iter (audit S55 wordmark with brackets dégradé en variant sans brackets sur brand test workspace). Refuse de composer si `packshots.primary_front` absent dans les 2 paths (spec.json#visual_identity ET sibling visual_identity.json).
2. **Hardcoded mécanique.** Modifier le prompt mécanique hardcodé dans le skill au lieu de lookup canon registry SSOT. Drift inévitable cross-products.
3. **Skip angle.formula validation.** NOYAU sans angle = creative null. Refuse de composer si `angle.json` absent ou `formula` vide.
4. **Confusion régime d'écriture sous `creatives/{batch}/{CRT-NN}/produced/`.** INTERDIT · écrire un `.json` (genome.json / creative.json / sidecar produced/{slug}.json) en direct (Edit/Write) · toujours `write_to_context` mode=proposed (mode `proposed` non-optionnel). ATTENDU · écrire les binaires `.jpg`/`.mp4` DIRECT sous `produced/` (write_to_context ne gère que le json), MAIS chaque binaire DOIT avoir son sidecar `produced/{slug}.json` gated (anti BUG-ASSET-ORPHAN). Double régime · json par le gate, binaire direct + sidecar gated. Ne JAMAIS écrire un binaire sans sidecar, ni un `.json` hors gate.
5. **Regen >3 iter pour label preservation.** Basculer en mode layered (HR-COMPOSITE) si canonical asset dispo, sinon flag opérateur en langage métier (HR3.4). Ne pas brûler API budget en boucle.
6. **JSON brut leak.** Surface `intent_mix: {primary: DR, weights: {DR: 0.6}}` à l'opérateur. Règle : traduction systématique en langage métier.
7. **Plumbing leak.** Surface `field_path`, `source`, `confidence`, `mode` à l'opérateur. Règle : opérateur voit `observé / déduit / déclaré / incertain`, jamais numbers.
8. **Doctrine name leak.** Surface `canonical-matrix-reasoning`, `Contextual Intelligence`, `Schema Encoding Discipline` à l'opérateur. Règle : opérateur sent les effets, pas les noms.
9. **Hypothesis from scratch sans validation.** Mode `hypothesis_from_scratch` propose 2-3 angles candidats AVANT de composer, jamais compose direct sur angle inventé.
10. **Phantom navigation leak.** Imiter `/phantom` avec "→ Tape : compose-next". Règle : 1 reco contextuelle en prose, pas de menu, pas de slash command surfacé.

---

## Operator output template

### Fiche canonique v2.51 forward template

Réf canonique · `resources/templates/operator-fiche-output.md`. Header plain language, body en vocabulaire métier, footer soft offer 1 ligne max. Bloc retrieval `concept_id`/`variant_of`/`intent_mix` persiste en backstage (creative.json) mais n'apparaît PAS dans le rendu operator.

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Pub n°{N}
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD} · {1 phrase plain language qui décrit la pub · ex "pub direct response Meta carrousel pour audience post-grossesse"}

───────────────────────────────────────────────────────────────
1 · CE QUE LA PUB MONTRE
───────────────────────────────────────────────────────────────
Format             {plain · ex "carrousel · 4:5 · français" ou "image statique · 1:1 · anglais"}
Accroche visuelle  {description scène en prose · 1-2 lignes}
Accroche texte     "{verbatim hook · max 8 mots}"
Corps              {description body · 1 ligne · ou vide si pas de body}
Bouton             "{verbatim CTA}"
Branding           {plain · ex "Logo en bas à droite · photo officielle du produit centrée"}
Photo générée      ouvre dans Preview · open {path} (= creatives/{batch}/{CRT-NN}/produced/{slug}.jpg)

───────────────────────────────────────────────────────────────
2 · CE QUE LA PUB RACONTE
───────────────────────────────────────────────────────────────
Cible              {1 phrase plain · ex "femmes 35-45 post-grossesse, chute de cheveux + sentiment perte d'identité"}
Niveau conscience  {plain · ex "consciente du problème, pas encore du produit"}
Vérité non-dite    "{verbatim insight}" · {formulée | implicite | absente}
Angle              {1 phrase plain · ex "frustration des soins de surface"}
Type de campagne   {plain · "direct response" ou "branding" ou "direct response avec touche brand (priorité direct response)"}
Mécanique          {nom métier · ex "before-after-bridge"} · {1 phrase explicative}
Pivot du concept   "{atome irréductible}" · {1 phrase justif}

───────────────────────────────────────────────────────────────
3 · DIAGNOSTIC
───────────────────────────────────────────────────────────────
Cohérence          {plain · ex "tient · la mécanique reflète l'insight, l'angle est cohérent avec la cible"}
Score arrêt-scroll {★★★★☆ · 1-5 stars · 1 phrase courte}
Forces             · {observable concret · ex "rupture pattern Meta feed via cadrage carré sur visage"}
                   · {observable}
                   · {observable}
Risques            · {observable · ex "claim 'cliniquement testé' nécessite preuve attachée"}
                   · {observable}
                   · {observable}

───────────────────────────────────────────────────────────────
{1 reco soft offer 1 ligne max · ex "Si tu veux, on peut la tester en live sur Meta avec ton audience principale."}
```

**Backstage (creative.json, NON rendu operator)** · `concept_id`, `variant_of`, `variant_axis`, `intent_mix`, `execution.overlay_density`, `execution.brand_mark_present`, `tags.source`, `meta.validation_status`, etc. Vivent dans le JSON persisté pour retrieval programmatique et audit · operator ne les voit pas.

**Validation pre-ship fiche** ·
1. Header ne contient pas `COMPOSE CREATIVE`, `CRT-N`, `variant_axis`, `concept_id`
2. Body ne contient pas `intent_mix: {...}`, `overlay_density: 0.6`, `craft_mode`, field paths JSON
3. Footer · 1 phrase soft offer max, jamais menu (a)/(b)/(c), jamais "Tape commande X"
4. Vocabulaire cohérent avec `resources/templates/operator-fiche-output.md § Mappings vocabulaire`

---

## Edge cases

- **Hypothesis from scratch (pas d'angle_id).** Skill propose 2-3 angles candidats depuis `profile.problem_map` + `canon/copy/formules-titres`. Demande validation opérateur AVANT pipeline gen. Ne compose jamais sur angle inventé sans gate.
- **Multi-products brand.** Si `product_slug` absent et marque a 2+ produits, demande choix opérateur (1 question AskUserQuestion). Ne devine pas.
- **Visual_identity partiel.** `primary_front` présent mais `distinctive_features[]` vide → continue, flag confidence dégradée. `primary_front` absent → refuse.
- **fal.ai API down ou rate limit.** Surface honnête, propose retry ETA + langage métier soft offer. Ne tente pas mock.
- **Label régressé après 3 iter.** Persiste le split (genome.json + creative.json + sidecar + brief.md) sous `creatives/{batch}/{CRT-NN}/`, JPG direct sous `produced/{slug}.jpg`, note `meta.label_compositing_required: true` dans `creative.json` (backstage, lignage). Flag à l'opérateur en langage métier HR3.4 (soft offer · canoniser la photo produit pour text fidelity garantie).
- **Concept variant.** Si opérateur déclare "comme CRT-12 mais hook différent", set `variant_of: "CRT-12"` + `variant_axis: hook_swap` dans `creative.json` (lignage · le namespace reste CRT-NN, jamais RCV · valeur depuis l'enum canonique creative.schema). Lineage préservé.

---

## Cross-refs

- Schemas cibles (Brique 4 étape B · split) : `resources/schemas/creative.schema.json` v1.3 (lignage · D#391 + variant_of CRT|RCV + lineage{}), `resources/schemas/genome.schema.json` v1.0 (ADN par-créa · script_id GSC-NN, hook, frames, support, genome_tags), `resources/schemas/produced-asset.schema.json` v1.0 (sidecar manifest binaire · 1 par .jpg, anti-orphelin).
- Convention stockage : `resources/conventions/creative-storage.md` (D#481 · forme batch `creatives/{batch}/{CRT-NN}/` + allocation mkdir-claim atomique).
- Équation : `resources/templates/creative-formula.md` v3.1 (stress-tested S55, 23 ads cross-typologies).
- SSOT mécaniques : `resources/registries/creative-mechanics-registry.md`.
- Schwartz stages : `resources/schemas/_shared/awareness-stage.json`.
- Visual identity schema : `resources/schemas/spec.schema.json#visual_identity` (v1.10+, S55 v2.31 extension).
- Audit visual fidelity : `decisions.md` D#392 (S55 audit régression label wordmark with brackets).
- Sibling skills : `decompose-ad` (REVERSE pattern, fiche v5 layout source), `produce-paid-angles` (forward angles textuels), `produce-copy-brief` (brief copy seul), `recompose-creative` (variant existant), `define-specs` (visual_identity prerequisite), `profile-audience` (profile prerequisite), `craft-packshot` v1.1+ (canonical asset upstream pour mode `layered` HR3b · v2.47), `compose-overlay-text` v2.43+ (text overlay PIL post-gen · complémentaire à layered packshot).
- Doctrines : `docs/system/canonical-matrix-reasoning.md` (production discipline), `docs/system/skill-authoring-doctrine.md` (frontmatter triad), `docs/system/contextual-intelligence.md` (operator-facing rule absolue), `docs/system/model-versioning-canon.md` v2.44+ (endpoint canon nano-banana-2/edit, frontmatter permissions.external_apis[] obligatoire), `docs/system/visual-identity-doctrine.md` v2.43+ (canonical assets + wordmark_pattern).
- Audit v2.46 endpoint migration : craft-packshot v1.1 upstream (S55 v2.44 stress test produit canon gen v10 · 1 attempt vs 9 échouées nano-banana-pro legacy) · pattern stress-testé puis propagé downstream consumers.
- Pattern v2.47 layered compositing · packshot canon (craft-packshot) + scène séparée nano-banana-2 + PIL composite paste · résout problème historique label regression sans burn budget API retry · text fidelity garantie 100% via substrat canonisé.
