---
name: craft-packshot
type: orchestrator
recommended_model: sonnet
subagent_safe: true
operator_facing: true
isolation_scope: brand_only
layer: production
version: 1.3.0
mode: proposed
permissions:
  reads: [brand, product, visual_identity]
  writes: [visual_identity_sidecar, asset]
  mode: proposed
  subagent_safe: true
  bash_allowlist:
    - "curl"
    - "python3"
  emits_events: [packshot_source_acquired, packshot_generated, packshot_validated_canonical]
  external_apis:
    - provider: "fal.ai"
      endpoint: "fal-ai/nano-banana-2/edit"
      model_family: "gemini_3_pro_image_novembre_2025"
      version_check_url: "https://fal.ai/models?keywords=banana"
      version_canon_date: "2025-11"
      replaced_legacy: "fal-ai/nano-banana-pro/edit (v1.0.0 · Gemini 2.5 Flash Image)"
      auto_upgrade: false
prerequisites:
  - field: brands/{slug}/brand.json
    level: L1
    auto_pull: read_brand_canonical
    freshness_ttl_days: 90
  - field: brands/{slug}/products/{slug}/spec.json
    level: L1
    auto_pull: read_product_spec
    freshness_ttl_days: 90
  - field: brands/{slug}/products/{slug}/visual_identity.json
    level: L1
    auto_pull: read_visual_identity_v11
    freshness_ttl_days: 90
  - field: source_packshot_input
    level: L2
    options:
      - scrape_from_official_site
      - upload_local_file
      - use_existing_canonical
description: >
  Orchestrator skill schema-driven · génère packshot canonique source of truth pour un produit physique.
  Lit brand.json + spec.json + visual_identity.json + scrape carousel site officiel. Compose prompt fal.ai
  nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025) dynamiquement depuis les schémas (pas d'enum
  produit hardcoded). Prompt naturel français court (langue maternelle opérateur · 50-300 chars max), pas
  redécrire ce que le model voit dans l'image attachée. Operator gate validation Step 5 obligatoire avant
  flag _canonical: true. Save asset packshot canonical réutilisable par compose-creative downstream.
  Pattern stress-testé S55 v2.44 sur {product_slug} gen v10 (silhouette préservée + text verbatim + 8/8 pass
  · 1 attempt vs 9 échouées sur endpoint legacy nano-banana-pro/edit).
  FR: "crée packshot canon", "génère photo produit propre", "prépare packshot source canon", "canonalise packshot", "nettoie packshot officiel".
  EN: "craft canonical packshot", "generate clean product shot", "prepare canonical product photo", "produce canonical packshot source".
disambiguates_against:
  compose-creative: "compose-creative consume canonical packshot pour générer pub paid social. craft-packshot CRÉE le canonical packshot upstream (asset source of truth)."
  compose-overlay-text: "compose-overlay-text fix logo + sub-text PIL post-gen sur creative pub. craft-packshot crée le packshot SOURCE upstream brand-level."
  define-specs: "define-specs encode visual_identity.json (label, container, content). craft-packshot consume visual_identity puis produit l'asset packshot canonique."
consumes:
  - path: brands/{slug}/brand.json
    min_version: 2.0.0
    note: identity.language pour anti-hallucination accents, meta.sector pour applicability detect
  - path: brands/{slug}/products/{slug}/spec.json
    min_version: 1.5.0
    note: identity.product_category physical required, identity.name pour prompt
  - path: brands/{slug}/products/{slug}/visual_identity.json
    min_version: 1.1.0
    note: container/content/label/distinctive_features/wordmark_pattern → prompt composition
  - path: resources/schemas/skill-prerequisites.schema.json
    min_version: 1.0.0
  - path: docs/system/output-clarity-doctrine.md
  - path: docs/system/operator-vocabulary-translation.md
produces_proposals_for:
  - brands/{slug}/products/{slug}/assets/packshot-canonical-{angle}-{date}-gen-v{N}.png
  - brands/{slug}/products/{slug}/visual_identity.json#assets_canonical
---

# Skill: craft-packshot

> **Craft canonical packshot from schemas.** v1.1.0 · v2.44 · orchestrator schema-driven · scrape → pick → compose prompt naturel court → gen IA via nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025) → operator gate → persist canonical. Asset source of truth réutilisable par compose-creative.

Orchestrator, pas générateur naïf. Lit (brand × product × visual_identity), scrape carousel produit, score sources brutes, compose prompt fal.ai DYNAMIQUEMENT depuis les schémas (jamais d'enum produit hardcoded dans le code), génère packshot IA, valide 8 critères, propose à l'opérateur le gate canonical. L'opérateur voit "votre packshot canon est prêt avec X% des critères passés", jamais "schema field consumed" ou "prompt composed from variables".

## Tone

Posture art director senior + ingénieur qualité invisible. Pas générateur aveugle, pas inspecteur bavard. Output opérateur 6-10 lignes max : source pickée (1 ligne justif), prompt composé (résumé non-jargon), gen IA latence + path, 8 critères table compacte, gate validation explicite. Aucun terme schema/prompt_template/variable_binding/L3_degraded en surface. Si schéma champ manque, surface honnête en langage opérateur ("votre fiche produit n'a pas X · est-ce que je continue avec valeur par défaut ou tu remplis d'abord ?").

## Expert methodology

**Persona.** Senior creative director e-commerce + retoucheur post-prod studio + ingénieur prompt IA. Sait qu'un packshot canon est l'atome reusable de toute la pipeline créa. Sait que parasites visuels (badges marketing, decor, props éparpillés) brûlent les retries fal.ai en downstream. Sait que verbatim label preservation + accents = critère bloquant régression brand.

**Framework.** Workflow déterministe 7 steps · scrape carousel → score qualité 6 critères source → pick best 1-3 → compose prompt schema-driven minimal (une variable container.shape · reste constant · langue opérateur) → fal.ai nano-banana-2/edit retry adaptatif → quality assessment 8 critères output → operator gate → persist sidecar.

**Pattern position pipeline.** craft-packshot CRÉE l'asset canon (upstream brand-level). compose-creative CONSUME l'asset canon (pour générer pub paid). compose-overlay-text RAFFINE post-gen creative (logo + text crisp si régression fal.ai). Source canon : `docs/system/compositional-cartography.md` v2.42 (cartographie + composer).

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant scrape (Step 1), scanner prerequisites :

1. **L1 silent** · `brands/{slug}/brand.json` → extract `meta.sector`, `identity.language`, `identity.brand_personality`, `meta.brand_equity_level`, `meta.creative_zone` (last 3 optional, L3 fallback `brand_personality` ou défaut neutre).
2. **L1 silent** · `brands/{slug}/products/{slug}/spec.json` → extract `identity.name`, `identity.product_category`, `unique_mechanism.name`, `specs.target_suitability`, `sensory_profile.scent_family` (last 2 optional selon product_category).
3. **L1 silent** · `brands/{slug}/products/{slug}/visual_identity.json` v1.1+ → extract `container.*`, `content.*`, `color_palette.*`, `label.wordmark_text`, `label.sub_label`, `label.duration_indicator`, `label.elements[]` si présent, `distinctive_features[]`, `wordmark_pattern`.
4. **Detect skill applicability** · si `spec.identity.product_category` ∈ {service, digital} OU `brand.meta.sector` ∈ {services, SaaS, B2B-only} OU `visual_identity.container` null → skill skip avec message opérateur-facing : *"Ce skill cible les produits physiques avec packshot photo. {brand} n'a pas de produit physique cartographié sous {product_slug}. Tu veux setup d'abord la fiche visuelle via `define-specs` ?"*. Refuse de continuer.
5. **L3 degraded** · si `visual_identity.label.elements[]` absent (label éléments non énumérés mais wordmark + sub_label présents) → continue avec prompt L3 (label minimal), flag `_label_completeness: partial` dans output gen metadata.
6. **L2 gate** · operator choice `source_packshot_input` (1 question AskUserQuestion si pas explicite dans la requête initiale) :
   - `scrape_from_official_site` (default si `brand.identity.website` présent et carousel détectable)
   - `upload_local_file` (operator drop dans assets/, skill évalue qualité)
   - `use_existing_canonical` (si `visual_identity.assets_canonical.{slot}._validated_by_operator: true` déjà flag)

Output state map + confidence_chain[] init.

---

## HR1 · Schema-driven obligatoire (canon SED v2.X)

**JAMAIS hardcoded enum produit/brand dans le prompt.** TOUJOURS consume schemas (`brand.json` + `spec.json` + `visual_identity.json`) pour composer prompt dynamiquement. Si un champ schéma manque, deux options :
- Optionnel (ex `sensory_profile.scent_family` pour produit functional) → skip dans prompt sans flag.
- Required pour ce produit (ex `visual_identity.container.material`) → L3 degraded mode, flag opérateur gate (*"je n'ai pas X dans ta fiche, je continue avec valeur par défaut Y ou tu remplis d'abord ?"*).

**Anti-pattern.** Skill avec branche `if brand == "brand_a" then prompt_a else if brand == "brand_b" then prompt_b`. Drift cross-produit inévitable, scaling cassé. Pattern schema-driven valide aux tests Phase 1 v2.44 stress-test.

---

## HR2 · Operator gate systématique

**Aucun packshot flag `_canonical: true` sans validation opérateur explicite.** `_validated_by_operator: false` par défaut à la persistence Step 6. Gate Step 5 obligatoire (surface path local + 8 critères + 3 options · validate / retry / re-pick source). L'opérateur seul flag `_canonical: true`, jamais le skill auto.

**Anti-pattern.** Auto-flag canonical après quality assessment 8/8 pass. Quality assessment est un signal, pas une décision finale. Critères machine ne couvrent pas brand intuition opérateur.

---

## HR3 · fal.ai endpoint canon

Endpoint `fal-ai/nano-banana-2/edit` (Gemini 3 Pro Image · canon novembre 2025 · supérieur vs `nano-banana-pro/edit` legacy Gemini 2.5 Flash Image qui régressait silhouette contenant OR text fidelity, et `nano-banana/edit` v1.0 qui ignore aspect_ratio + qualité moindre). Aspect ratio `1:1` standard packshot. Resolution `2K` minimum (2048×2048 cible). Format `png` (transparent OR fond blanc pur `#FFFFFF`).

**Model versioning canon · check latest dispo pre-call.** Doctrine sœur · `docs/system/model-versioning-canon.md` v2.44 NEW. Avant tout call API externe, vérifier latest version disponible (URL fournie en frontmatter `permissions.external_apis[].version_check_url`). Si version récente dispo · flag operator OR auto-switch selon `auto_upgrade` config. Log version utilisée dans output metadata pour audit trail.

Auth header `Authorization: Key ${FAL_API_KEY}` (lookup `credentials_shared.env` racine workspace OR `brands/{slug}/credentials.env` fallback).

---

## HR3.4 · Retry policy adaptative (cohérent compose-creative)

- **Scène simple** (label minimal, wordmark + sub_label uniquement, pas de cert badge ni duration_indicator complexe) → `max_retry = 2`.
- **Scène complexe** (multi-label texts ≥ 5 éléments + cert badges + duration_indicator + composition list) → `max_retry = 3`.

Si retry exhausted et label régression persistante :
1. NE PAS continuer à retry (gain marginal, brûle budget API).
2. Persist creative avec note `gen_needed_manual_cleanup: true` dans sidecar metadata.
3. Surface alternative à l'opérateur : *(a) Photoshop manuel cleanup résiduel, (b) re-pick source carousel autre asset, (c) compose-overlay-text PIL post-gen pour fix wordmark/sub-text crisp.*

---

## HR-ANTI-VERBOSE · Prompt minimum viable (NEW v1.1)

**Prompt minimum viable · langue maternelle opérateur · pas redécrire ce que le model voit dans image attachée · 50-300 chars max.** Style `photoshoot professionnel · uniquement le produit · belle lumière` suffit.

**Pattern canon novembre 2025.** Gemini 3 Pro Image (`nano-banana-2/edit`) répond mieux à un brief court naturel qu'à un prompt verbeux corporate. Le model voit l'image source attachée donc redécrire le produit (couleur, matériaux, text label, ingrédients) = bruit qui dégrade la fidélité. Une seule variable composée depuis schéma · `visual_identity.container.shape` (bocal · flacon · tube · sachet · pot · boîte). Le reste = constant.

**Anti-pattern.** Prompt 4000+ chars 16 variables avec sections LABEL ELEMENTS · DISTINCTIVE FEATURES · REMOVE PARASITES · ANTI-HALLUCINATION RULES · NEGATIVE INSTRUCTIONS · BRAND REGISTER · OUTPUT SPECS (= v1.0 pattern). v1.1 retire l'orchestre verbose · le model voit l'image et corrige avec moins de directives.

**Validation pre-call** · `final_prompt` length 50-300 chars (zone validée S55 v2.44 gen v10 · ~250 chars). Si > 300 = trop verbose, simplifier. Si < 50 = trop vague, vérifier `container.shape` rempli.

---

## HR-MODEL-VERSIONING · Verify latest endpoint pre-call (NEW v1.1)

**Verify latest endpoint version dispo avant call API externe.** `nano-banana-2/edit` > `nano-banana-pro/edit` > `nano-banana/edit`. Vérifier `https://fal.ai/models?keywords=banana` pour newest avant lancer gen IA.

**Frontmatter contract.** Chaque skill qui call API externe DOIT declarer `permissions.external_apis[]` avec `provider · endpoint · model_family · version_check_url · version_canon_date · replaced_legacy · auto_upgrade`. Audit trail dans output metadata · log endpoint utilisé + version date pour traçabilité.

**Anti-pattern.** Hardcoder endpoint legacy sans check version récente. v2.43 cycle USAGE a montré que `compose-creative` et `craft-packshot` continuaient à utiliser `nano-banana-pro/edit` (Gemini 2.5 Flash Image legacy) en novembre 2025 alors que Google avait release Gemini 3 Pro Image (`nano-banana-2/edit`) supérieur en text fidelity + material preservation native.

**Application v2.44.** craft-packshot v1.1 swap fait. Skills consumers TODO v2.45+ · `compose-creative`, `recompose-creative`, `decompose-ad` (check si decompose-ad utilise endpoint trendtrack spécifique).

Doctrine canon · `docs/system/model-versioning-canon.md` v2.44 NEW.

---

## HR4 · Anti-hallucination text (BLOCKER canon)

Prompt MUST inclure explicitement :
- `"COPY LABEL TEXT VERBATIM FROM REFERENCE · DO NOT INVENT OR PARAPHRASE · DO NOT ADD TEXT WHERE NONE EXISTS · DO NOT HALLUCINATE CHARACTERS"`
- Liste numérotée des éléments label à préserver (1-N, top-to-bottom du packshot) avec spelling explicite pour mots à fort risque hallucination (ex `Goût myrtille & framboise` épelé letter-by-letter dans label_elements_iteration).
- Section `NEGATIVE INSTRUCTIONS` avec mots à NE PAS render (anti-faux-français : NO marble, NO frumboise, NO inventés diacritics).
- `"All {brand_language} diacritics preserved character-by-character (é è ê à â ù û ç î ï ô œ æ)"`.

**Sans ces 4 blocs anti-hallucination, le pattern régresse.** Audit S55 v2.44 test brand workspace gen v1 → flavor text rendu en quasi-anglicismes (hallucination textuelle sur diacritics français). Gen v2 avec ces 4 blocs ajoutés → 8/8 pass.

---

## HR5 · Quality assessment 8 critères (canon)

Pour chaque gen output, table critère par critère :

| # | Critère | Source |
|---|---|---|
| 1 | Wordmark verbatim selon `wordmark_pattern` regex | visual_identity.label.wordmark_text |
| 2 | Sub-label verbatim (CELL BOOST, GLOW BOOST, etc.) | visual_identity.label.sub_label |
| 3 | Composition list verbatim avec separators · | visual_identity.label.ingredients_listed |
| 4 | Duration indicator verbatim ("1 MOIS DE CURE · 60 gummies") | visual_identity.label.duration_indicator |
| 5 | Cert badge sans hallucination text (round shape OK, text legible OR clean blank) | visual_identity.distinctive_features |
| 6 | Subtitle/descriptive line accents préservés character-by-character | visual_identity.label.elements OU distinctive_features |
| 7 | Container preservé (shape, material, transparency, cap) | visual_identity.container |
| 8 | Background pure white (#FFFFFF) OR transparent, zero parasite (no decor, no badge marketing, no props scattered) | visual_identity-derived requirement |

Statuts : `pass` / `pass_partial` / `fail`. Critère 5 (cert badge) tolère `pass_partial` si round shape OK + text fragments légitimes lisibles (pas hallucination), c'est le seul critère où partial = pass (cert badges sont souvent partiellement illisibles sur sources brutes aussi). Critères 1-4, 6-8 binaires (pass/fail).

Verdict global · `8/8` ou `7/8 (avec pass_partial cert badge)` = ready for operator gate. `≤6/8 pass` = retry.

---

## HR6 · Operator-facing translation (canon)

Vocabulaire interne → operator-facing (cf `docs/system/operator-vocabulary-translation.md`) :

| Interne | Operator-facing |
|---|---|
| consume schemas | lit votre fiche produit |
| L1 auto_pull | récupération automatique |
| L3 degraded | champ manquant, je flag |
| image_urls payload | image source |
| prompt composé dynamiquement | brief automatique généré depuis ta fiche |
| nano-banana-pro/edit endpoint | génération IA haute fidélité |
| label_compositing_required: true | wordmark à raffiner manuellement |
| _canonical: true flag | marqué comme version officielle |
| wordmark_pattern regex validation | vérification du wordmark exact |
| 8 critères quality assessment | check 8 points qualité |
| _validated_by_operator gate | ta validation avant marque officielle |

JAMAIS exposer `field_path`, `source`, `confidence` (numbers), `mode` à l'opérateur. Operator verbs : valide / refuse / corrige / flag.

---

## Steps

### Step 0 · Detect input + L1/L2 prerequisite scan (cf Step 0bis above)

Detect input mode :
- `(brand_slug, product_slug)` explicite → prerequisite scan direct.
- `(product_slug)` sans brand → lookup brand parent depuis path produit.
- Phrase libre opérateur → extract brand + product (1 question si ambigu).

Run Step 0bis prerequisite check. Si applicability fail, refuse et surface honnête.

### Step 1 · Source acquisition

#### Mode A · scrape_from_official_site

1. Read `brand.identity.website`. Si absent, ask opérateur URL produit.
2. Construct URL produit `{website}/products/{product_slug}` ou variant ask opérateur si pattern différent.
3. `curl -sL {url} -H "User-Agent: Mozilla/5.0" -o /tmp/{product_slug}-page.html`.
4. Parse carousel images via `grep -oE '"src":"[^"]+\.(png|webp|jpg)[^"]*"'` pour extract URLs Shopify CDN OR équivalent WooCommerce/custom.
5. Score chaque asset selon 6 critères :
   - **resolution** (target ≥ 2000×2000, accept ≥ 1500×1500 fallback)
   - **format** (PNG > WebP > JPG)
   - **fond** (transparent > white > decor parasites)
   - **angle** (front isolé > 3/4 > top > carousel multi-jars)
   - **lisibilité label** (wordmark + sub-label readable)
   - **parasites** (count badges marketing + decor + props éparpillés, lower = better)
6. Pick top 1-3 sources (best front, best 3/4 si dispo, best autre angle si dispo).
7. Download via `curl` vers `brands/{slug}/products/{product_slug}/assets/packshot-source-{angle}-{date}.png`.

#### Mode B · upload_local_file

1. Opérateur drop fichier(s) dans `brands/{slug}/products/{product_slug}/assets/`.
2. Évaluer qualité (resolution, format, fond, parasites) via PIL ou file metadata.
3. Si qualité suffisante (resolution ≥ 2000, fond clean, parasites = 0) → skip Step 2 gen IA, propose Step 5 gate direct (asset utilisable as-is). Si qualité insuffisante → proceed Step 2.

#### Mode C · use_existing_canonical

1. Read `visual_identity.assets_canonical.{slot}.path` + `_validated_by_operator`.
2. Verify file exists at path + `_validated_by_operator: true` flag.
3. Si validé → skill skip Steps 2-6, surface "asset canon déjà validé pour ce slot. Path : X. Tu veux re-gen ou utilise tel quel ?".

### Step 2 · Prompt composition schema-driven minimal (CANON SED v1.1)

C'est le step canon. v1.1 swap pattern v1.0 verbose (4000+ chars 16 variables) vers minimum viable naturel français court (50-300 chars · 1 variable).

**Template canon novembre 2025** (Gemini 3 Pro Image · `nano-banana-2/edit`) ·

```python
prompt_template = (
    "Mets-moi ce produit sur un photoshoot professionnel bien au centre "
    "avec une belle lumière, uniquement le produit, rien d'autre, "
    "le {container_shape} et tous les détails sur le produit sur le packaging."
)

# Une seule variable composée depuis schéma
variables = {
    "container_shape": visual_identity["container"]["shape"]
    # bocal · flacon · tube · sachet · pot · boîte
}

final_prompt = prompt_template.format(**variables)
```

**Le reste = constant.** Le model voit l'image attachée donc pas besoin de redécrire produit · couleur · matériaux · text label · ingrédients · cert badges · etc. Pattern v1.0 verbose dégradait la fidélité avec du bruit instructionnel. v1.1 confie au model la lecture de l'image source + applique brief minimum viable.

**Validation pre-call** · `final_prompt` length 50-300 chars (zone validée gen v10 · ~250 chars). Si > 300 = trop verbose, simplifier. Si < 50 = trop vague, vérifier `container.shape` rempli dans `visual_identity.json`.

**Locale switch.** Si `brand.identity.language ≠ FR`, traduire template dans langue opérateur. Default · FR (template style direct). EN equivalent · *"Put this product in a professional photoshoot, well-centered with beautiful lighting, only the product, nothing else, the {container_shape} and all the product details on the packaging."*

### Step 3 · fal.ai call

```bash
# 3a. Upload source reference image
SOURCE_URL=$(curl -s -X POST "https://rest.alpha.fal.ai/storage/upload/initiate" \
  -H "Authorization: Key ${FAL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"content_type":"image/png","file_name":"packshot-source.png"}' \
  | jq -r '.upload_url')

curl -X PUT "${SOURCE_URL}" --data-binary @packshot-source-front-{date}.png

# 3b. Get signed source URL from upload response, then call edit endpoint
SOURCE_SIGNED_URL=$(... extract from upload response ...)

curl -s -X POST "https://queue.fal.run/fal-ai/nano-banana-2/edit" \
  -H "Authorization: Key ${FAL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": \"${FINAL_PROMPT}\",
    \"image_urls\": [\"${SOURCE_SIGNED_URL}\"],
    \"aspect_ratio\": \"1:1\",
    \"output_format\": \"png\",
    \"resolution\": \"2K\"
  }"

# 3c. Poll request status, then download result PNG
# 3d. Save to brands/{slug}/products/{product_slug}/assets/packshot-canonical-{angle}-{date}-gen-v{N}.png
```

Retry budget HR3.4. Si label régression detected post-Step 4, retry max selon scène simple/complexe.

### Step 4 · Quality assessment 8 critères

Pour chaque label_element + 4 critères meta · visual inspection via Read tool (image multimodal) OR pseudo-OCR via PIL → text region extraction → string match avec `visual_identity.label.*`.

Output table dense (cf HR5 above).

### Step 5 · Operator validation gate (CRITIQUE · BLOCKER canon)

Surface à l'opérateur selon template canonique `resources/templates/operator-fiche-output.md`. Plain language, zéro jargon plumbing ·

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Photo officielle · {product_humain}
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD} · version {N}, prête pour ta validation

Source utilisée ·
  {source_filename} · {resolution} · {1 ligne plain language · ex "meilleure version
  du carrousel produit, vue de face, fond propre"}

Brief utilisé ·
  {1-2 lignes plain language · ex "photoshoot studio fond blanc pur, label conservé
  caractère par caractère, accents français préservés, aucune invention textuelle"}

Photo générée · ouvre dans Preview · open {output_path}

Check qualité 8 points ·
  1. Logo principal             {ok | à revoir}
  2. Sous-titre du logo         {ok | à revoir}
  3. Liste composition          {ok | à revoir}
  4. Mention durée              {ok | à revoir}
  5. Badge certification        {ok | acceptable | à revoir}
  6. Accents français           {ok | à revoir}
  7. Forme du produit           {ok | à revoir}
  8. Fond blanc propre          {ok | à revoir}

  Verdict · {N}/8

  Note · {1-2 lignes si applicable · ex "tout bon · juste un léger reflet dans le verre
  du contenant, pas bloquant"}

───────────────────────────────────────────────────────────────
À toi de valider
───────────────────────────────────────────────────────────────
(a) Validé · je marque comme version officielle de ta photo produit
(b) Re-essayer · ajustements (précise quoi)
(c) Autre source · je re-pick une photo différente du carrousel
```

JAMAIS auto-flag `_canonical: true` sans réponse opérateur explicite (cf HR2). JAMAIS exposer `{endpoint}`, `latency`, `_validated_by_operator: true + _canonical: true`, scores numériques verbatim style `score 4/5`, sidecar field paths à l'opérateur. Tous les flags techniques persistent en backstage dans `visual_identity.json` (cf Step 6 update fields).

### Step 6 · Update visual_identity.json sidecar + README

Si Step 5 validé option (a) :

**Mutation gate decision (CRITIQUE).** `visual_identity.json` est sidecar (pas core entity dans la liste des 6 core entities `brand/product spec/offers/audience profile/learnings/strategy` du mutation rule canon). Donc edit direct via Write/Edit accepté pour ce sidecar (clarifié explicitement dans contraintes mission v2.44). Si la convention évolue vers `write_to_context` pour sidecars sous `brands/{slug}/`, ce skill devra basculer en mode `write_to_context` (point à surveiller).

**Update fields** :
- `assets_canonical.{slot}.path` → new gen path (`packshot-canonical-{angle}-{date}-gen-v{N}.png`).
- `assets_canonical.{slot}.resolution` → output resolution (typically 2048×2048).
- `assets_canonical.{slot}.background` → `"pure_white_ffffff"` ou `"transparent"`.
- `assets_canonical.{slot}._canonical: true`.
- `assets_canonical.{slot}._validated_by_operator: true`.
- `assets_canonical.{slot}._validated_at: "{date}"`.
- `assets_canonical.{slot}._generated_via_craft_packshot: true`.
- `assets_canonical.{slot}._generation_version: "v1.1.0"`.
- `assets_canonical.{slot}._generated_via_endpoint: "fal-ai/nano-banana-2/edit"`.
- `assets_canonical.{slot}._generation_endpoint_model_family: "gemini_3_pro_image_novembre_2025"`.
- `assets_canonical.{slot}._generation_latency_seconds: N`.
- `assets_canonical.{slot}._source_reference_path` (relative path source brute Step 1).
- `assets_canonical.{slot}._source_reference_uploaded_url` (fal.ai signed URL Step 3).
- `assets_canonical.{slot}._output_signed_url` (fal.ai output signed URL Step 3).
- `assets_canonical.{slot}._parasites_removed_attempted: [...]` (liste depuis HR4 prompt block REMOVE).
- `assets_canonical.{slot}._preserve_attempted: [...]` (liste depuis distinctive_features + label.elements).
- `assets_canonical.{slot}._quality_checks_8_criteria: {...}` (table Step 4 résultats).
- `assets_canonical.{slot}._gen_attempts: ["v1", "v2", ...]` (array versions itérations).
- `_fallback_to_cdn: false` (asset local désormais source of truth).

**README.md update** section `## generated_canonical_assets_{date}` avec table gen v{N} | path | status | endpoint | latency | prompt_resume.

### Step 7 · No orphan output (langage métier · zéro jargon · soft offer 1 ligne)

Operator-facing summary final ·

- Photo officielle du produit prête · ouvre la dans Preview macOS (`open {path}`).
- 1 reco douce contextuelle, soft offer · jamais menu, jamais nommer le skill ·
  - Si seul angle front généré → *"Si tu veux, on peut aussi préparer la vue 3/4 et la vue arrière pour avoir une photothèque complète."*
  - Si tous angles validés → *"Si tu veux, on peut tester une pub avec cette photo officielle."*
  - Si autre produit même brand pas encore préparé → *"Si pertinent, on peut faire pareil pour {autre_product_humain} (1 fois et c'est réutilisable sur toutes ses pubs)."*

**No orphan close.** Pas de "Done. Want anything else?". Pas de menu hardcoded. Soft offer 1 ligne max.

### Step 8 · Trigger validate-resources silently post-write (v2.51 NEW)

Après Step 6 persist visual_identity.json sidecar update, trigger `validate-resources` silencieusement sur la brand · même pattern que compose-creative + snapshot-brand post-mutation.

```bash
# Silent validation pass
python3 .skills/build-brand-snapshot.py {brand_slug}
# validate-resources via Task tool (subagent_safe: true permet inline)
```

Flag MAJOR/CRITICAL à l'opérateur si remonte. Sinon silent. Cohérent doctrine root CLAUDE.md ligne 168 *"ALWAYS after any write under brands/{slug}/custom/ or {entity}.extensions.json : trigger validate-resources on that brand silently."* Évite drift schema sidecar silencieux post-mutation.

---

## Hard Rules récap (numéro canonical)

| HR | Règle | Type |
|---|---|---|
| HR1 | Schema-driven obligatoire (jamais hardcoded enum produit) | BLOCKER |
| HR2 | Operator gate systématique avant flag _canonical (Step 5) | BLOCKER |
| HR3 | fal.ai endpoint nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025) + aspect_ratio 1:1 + resolution 2K + format png | CANON |
| HR3.4 | Retry policy adaptative (simple 2 / complexe 3) | CANON |
| HR-ANTI-VERBOSE | Prompt minimum viable 50-300 chars langue opérateur (NEW v1.1) | CANON |
| HR-MODEL-VERSIONING | Verify latest endpoint version dispo pre-call (NEW v1.1) | CANON |
| HR4 | Anti-hallucination text legacy (v1.0 reference · v1.1 délègue au model via image attachée) | LEGACY |
| HR5 | Quality assessment 8 critères avec verdict pass/fail/pass_partial | CANON |
| HR6 | Operator-facing translation strict (no plumbing leak) | BLOCKER |

---

## Edge cases

- **Brand sans website.** `brand.identity.website` null → Mode A impossible. Bascule Mode B (upload local) ou ask opérateur URL produit explicite.
- **Carousel masquée derrière JS rendering.** Si `grep` sur HTML statique trouve 0 image, propose Mode B upload OR utilise Puppeteer/Playwright si dispo via MCP (à clarifier opérateur).
- **Visual_identity.label.elements[] absent.** L3 degraded · helper `_build_label_elements_from_schema(vi)` reconstruit depuis `label.wordmark_text`, `label.sub_label`, `label.ingredients_listed`, `label.duration_indicator`. Si tous absents = refuse, surface "fiche visuelle trop vide, run `define-specs` d'abord".
- **Cert badge zone très complexe.** Si visual_identity flag cert_badge particulier avec arc text détaillé, ajouter precision element dans label_elements_iteration avec spelling literal de l'arc text (ex `Minéraux · Plantes · Vitamines`).
- **FAL_API_KEY manquant.** Surface honnête : *"je n'ai pas accès à fal.ai sur ton workspace. Drop le token dans credentials.env racine, ou utilise Mode B upload manuel"*. Refuse de continuer.
- **Source carousel max 1500×1500 only.** Continue avec source < 2000×2000 (acceptable pour gen IA upscale via nano-banana-pro/edit qui scale to 2K output anyway), flag note dans sidecar `_source_resolution_under_target`.

---

## Cross-refs

- Schema cible visual_identity : `resources/schemas/visual_identity.schema.json` v1.1.0 (S55 v2.43+ extension).
- Schema spec : `resources/schemas/spec.schema.json` v1.5.0+ (identity.product_category, sensory_profile, target_suitability).
- Schema brand : `resources/schemas/brand.schema.json` v2.0.0+ (identity.brand_personality, identity.language, meta.creative_zone).
- Schema prerequisites : `resources/schemas/skill-prerequisites.schema.json` v1.0.0+.
- Equation cartographie : `resources/templates/creative-formula.md` v3.1 (NOYAU × CONTEXTE × MODIFIEURS · craft-packshot opère sur NOYAU brand-level upstream).
- Vocabulary translation : `docs/system/operator-vocabulary-translation.md` v2.X.
- DRGFP : `docs/system/dependency-resolution-protocol.md` v2.38+ (L1/L2/L3 gap-filling Step 0bis canon).
- Sibling skills : `compose-creative` (consume canonical packshot downstream), `compose-overlay-text` (PIL post-gen raffine MODIFIEURS), `define-specs` (encode visual_identity prerequisite), `import-product-visuals` (futur skill v2.4X upload bulk multi-angles).
- Doctrines : `docs/system/contextual-intelligence.md` (operator-facing rule absolue), `docs/system/schema-encoding-doctrine.md` (substrate canon SED v2.X · schema-driven obligatoire HR1), `docs/system/canonical-matrix-reasoning.md` (production discipline · craft-packshot = NOYAU producer asset canon réutilisable), `docs/system/model-versioning-canon.md` v2.44 NEW (HR-MODEL-VERSIONING canon · vérifier latest endpoint version dispo pre-call API externe).
- Audit ref · S55 v2.44 stress test {product_slug} gen v10 nano-banana-2/edit (Gemini 3 Pro Image canon novembre 2025) · silhouette préservée + text verbatim + 8/8 pass · 1 attempt vs 9 attempts échouées sur endpoint legacy `nano-banana-pro/edit` (Gemini 2.5 Flash Image · silhouette bouteille réinventée OR text gibberish). Pattern v1.1 swap endpoint + prompt naturel français court résout cycle complet · operator validé canon 2026-05-12.
