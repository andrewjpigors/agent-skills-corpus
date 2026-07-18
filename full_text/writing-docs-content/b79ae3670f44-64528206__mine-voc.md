---
name: mine-voc
type: producer
version: "1.5.0"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
reasoning_pattern: matrix-driven
matrix_mode: coding
consumes:
  - path: resources/frameworks/voc-coding.md
    min_version: 1.0.0
  - path: resources/schemas/voc-verbatim.schema.json
    min_version: 1.0.0
    note: "C1 · SSOT du record Layer A (verbatim_id ^VOC-NN séquence par brand + extraction inline). La prose Step 3 est un rappel, le schéma fait foi."
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
  - path: docs/doctrine/objections-mapping-doctrine.md
description: >
  v1.4.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution (entre Engagement disclosure pré-runtime NIVEAU 0 v2.79.5 et Tone). Action LOURDE (crawl multi-sources + 4-lens coding + 7 Steps + Layer A archive + Layer B mutations). NIVEAU LIVE narratif étendu 2 niveaux abstraction (macro contexte corpus verbatims cross-canaux + micro signaux par cluster phrasé en prose). Pose pair senior expert · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  v1.4.0 (v2.79.5 decomposition visibility NIVEAU 0) · NEW section "Engagement disclosure pré-runtime v2.79.5+" enrichie avec NIVEAU 0 paramètres décomposés (Audience cible · Pains prioritaires · Canaux · Queries opératoires · Hypothèses figées · Biais à éviter · POURQUOI chaque). L'agent expose 6 paramètres contextualisés brand + raisonnement métier expert visible AVANT scrape. Exemple canonisé Liv Happyfood (box konjac · femmes 30-45 actives urbaines · pains JTBD konjac · canaux ranked densité × signal · queries fonctionnel + émotionnel · hypothèses figées · biais à éviter). ATTENDS confirmation explicite paramètres AVANT scrape. Cross-ref `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ NIVEAU 0 + `docs/system/engagement-disclosure-doctrine.md` v2.79.5 Paramètres décomposés. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` OR `--no-disclosure` explicit. Backward compat strict additif (cycle runtime préservé · seul l'amont disclosure change).
  v1.3.0 (v2.64 ontologie sémantique pure) · pain_points + objections passent en SUB-AUDIENCE · stage `brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json` + `brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json` entités complètes (owned natif par l'audience). Generation IDs PNT-NN/OBJ-NN scan désormais `brands/{slug}/audiences/*/pain_points/*.json` filesystem (incrémental cross-audiences). Pattern · pain et objection appartiennent sémantiquement à une audience · sub-parent path canonical (au lieu de top-level v2.63 avec affected_audiences[] array). Backward compat strict additif · lecture fallback `brands/{slug}/pain_points/*.json` + `brands/{slug}/objections/*.json` top-level v2.63 si sub-parent vide OR absent. Profile sub-fields legacy v1.7 read fallback aussi preserved.
  v1.2.0 (v2.63 ontologie pure) · pain_points + objections passent en COLLECTIONS top-level séparées · stage `brands/{slug}/pain_points/{PNT-NN}.json` + `brands/{slug}/objections/{OBJ-NN}.json` entités complètes avec `affected_audiences: [a_slug]`. BREAKING profile.json schema v2.0 (sub-fields legacy `profile.pain_points[]` / `profile.objections[]` DEPRECATED en write · read backward compat preserved). Pattern miroir friction.schema (top-level collection). Cross-audience reference natif via affected_audiences[].
  v1.1.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (pain-benefit-chain, objections-mapping). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.1.0 (v2.58 coverage extend) · benefits emotional_signal + latency_min/max + evidence_verbatim staging (v1.10 NEW fields activated) · pain_id PNT-NN + objection_id OBJ-NN stable generation (v1.7 NEW canonical IDs · fixe faille cross-ref friction). Closes 3 orphans audit v2.57.
  Voice of Customer mining. Captures what real customers say about THIS brand
  from native review widgets, Trustpilot, Reddit threads, app stores, forums.
  Codes verbatim through 4 lenses (JTBD, Schwartz awareness, theme typology,
  pain category). Produces a synthesis paragraph naming what the customers
  reveal that the brand likely does not see, plus structured mutations into
  spec.json verbatim_quotes[], profile.json voice.key_expressions[],
  pain_points/{PNT-NN}.json collection et objections/{OBJ-NN}.json collection.
  FR: "voc {brand}", "scrape les avis", "mine les reviews", "extrais ce que disent les clients", "voice of customer".
  EN: "voc {brand}", "mine reviews", "voice of customer", "scrape customer reviews".
permissions:
  reads: [brand, product, profile]
  writes: [brand, product, profile, learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
produces_proposals_for:
  - brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json
  - brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json
  - brands/{slug}/products/{p_slug}/spec.json#/problems_solved
  - brands/{slug}/products/{p_slug}/spec.json#/benefits
  - brands/{slug}/audiences/{a_slug}/profile.json#/voice/key_expressions
  - brands/{slug}/pain_points/{PNT-NN}.json (legacy v2.63 backward compat read · DEPRECATED write)
  - brands/{slug}/objections/{OBJ-NN}.json (legacy v2.63 backward compat read · DEPRECATED write)
  - brands/{slug}/audiences/{a_slug}/profile.json#/pain_points (legacy v1.7 backward compat read · DEPRECATED write)
  - brands/{slug}/audiences/{a_slug}/profile.json#/objections (legacy v1.7 backward compat read · DEPRECATED write)
pipeline:
  preconditions: brand exists with at least brand.json filled (run setup-brand + snapshot-brand first)
  postconditions: synthesis delivered, Layer A corpus archived in sources/voc/, Layer B mutations proposed, finalize-mutation-batch event emitted
disambiguates_against:
  mine-vom: "route to mine-vom when operator wants market-level voice (competitors, niche communities), not brand-bound customer voice"
  mine-audience: "route to mine-audience when operator wants product-level audience discovery from scraping, not review verbatim mining"
  ingest-resource: "route to ingest-resource when operator drops a single document/CSV · that's a one-off ingest, not a multi-source mining session"
  watch-competitors: "route to watch-competitors when operator wants recurring monitoring of competitors' paid creatives, not one-shot customer voice"
---

# mine-voc

Mine Voice of Customer for an existing brand. Read what the brand's actual customers say across the surfaces where they leave traces, code each verbatim through four established lenses, deliver a synthesis paragraph that names what the brand likely does not see, route the structured findings into existing entities. One brand per invocation. One snapshot in time. The corpus stays as audit substrate; the synthesis is what the operator uses.

---

## Engagement disclosure pré-runtime · canon v2.79.5+ (NIVEAU 0 paramètres décomposés)

Avant de lancer le mining VoC, expose ce disclosure ENRICHI à l'opérateur (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.5 Paramètres décomposés + `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ NIVEAU 0 pré-exec). Le disclosure v2.79.5 ajoute NIVEAU 0 paramètres décomposés AVANT le plan · l'agent contextualise sur la brand cible · 6 paramètres opérationnels + raisonnement métier expert visible (POURQUOI chaque choix). L'opérateur valide ou ajuste les paramètres AVANT le scrape.

### Format canonique disclosure v2.79.5+ enrichi

```
Mining voix client · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Paramètres posés · ce sur quoi je pars
  ─────────────────────────────────────────────────────────────────────
  Audience cible        {segment atlas} · POURQUOI ce choix
  Pains prioritaires    {liste ordonnée} · POURQUOI cet ordre
  Canaux                {ranking sources} · POURQUOI ce ranking
  Queries opératoires   {mots-clés + variants} · POURQUOI dimensions
  Hypothèses figées     {ce que je présume sans valider}
  Biais à éviter        {risk flags du corpus/source}

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Check données first-party (export Shopify · Klaviyo · transcripts)
  2. Détection sources publiques + crawl plan
  3. Scrape verbatims (Trustpilot · widgets natifs · Reddit · marketplaces)
  4. Coding 4 lentilles (theme · JTBD · Schwartz · pain category)
  5. Détection patterns + gap analysis brand-stated vs customer-said
  6. Synthèse 3 mouvements opérateur-facing
  7. Routing structuré dans entités (pain_points · objections · vocabulary)

  ETA           ~10-20 min (selon densité corpus disponible)
  Implication   tu valides paramètres d'abord · tu dis si first-party · puis tu valides la synthèse
  Livrable      synthèse 3 mouvements + corpus Layer A archivé + mutations entités proposées

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

### Pattern obligatoire NIVEAU 0

L'agent expose **6 paramètres décomposés contextualisés** sur la brand cible (lecture `brand.json` + `audiences/*/profile.json` + `products/*/spec.json` upstream). Pour chaque paramètre, **POURQUOI explicit** (raisonnement métier expert visible · pas implicite). L'opérateur voit le raisonnement avant le run · il peut ajuster avant la consommation de tokens scrape.

1. **Audience cible** · segment atlas (depuis `audiences/*/profile.json` encoded). POURQUOI ce focus · cohérence avec positioning brand encoded + densité corpus attendue.
2. **Pains prioritaires** · liste ordonnée 2-4 pains JTBD (depuis brand context + niche category). POURQUOI cet ordre · dominance marché + intensité signal expected.
3. **Canaux** · ranking sources scrape ordonnées (Trustpilot > forums > Reddit > TikTok comments etc.). POURQUOI ce ranking · densité × pertinence × signal direct vs indirect.
4. **Queries opératoires** · mots-clés primaires + variants vernaculaires (incluant fonctionnel + émotionnel). POURQUOI ces dimensions · capturer la chaîne pain → solution → produit-aware sur les deux axes.
5. **Hypothèses figées** · ce que l'agent présume SANS valider (e.g. langue · pas de différentiation H/F · Schwartz stage dominant). L'opérateur sait ce qui n'est pas vérifié.
6. **Biais à éviter** · risk flags du corpus / source (sur-pondération Trustpilot biais positif marque · under-rep Reddit biais critique platform · imported widgets non-vérifiables). L'agent flagge ce qui pourrait fausser le read avant le scrape.

### Exemple concret canonisé · mine-voc sur Liv Happyfood (box konjac minceur)

```
Mining voix client · Liv Happyfood · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Paramètres posés · ce sur quoi je pars
  ─────────────────────────────────────────────────────────────────────
  Audience cible        Femmes 30-45 actives urbaines (60% atlas brand hero)
                        POURQUOI · pas le sportif intensif · positionnement
                        minceur clean encodé brand.json#positioning

  Pains prioritaires    1. Faim entre repas / snacking compulsif
                        2. Coupe-faim sans frustration
                        3. Transit / digestion lourde
                        POURQUOI · 3 JTBD konjac dominants marché FR
                        (densité signal expected category)

  Canaux                1. Avis Trustpilot Liv (densité × signal direct)
                        2. Forums minceur FR (Doctissimo · AuFéminin)
                        3. Reddit r/loseit (cross-cultural sanity check)
                        4. TikTok comments #konjac (vernaculaire récent)
                        POURQUOI · ordre = densité × pertinence + signal
                        brand-direct avant marché-indirect

  Queries opératoires   Fonctionnel · "konjac avis" · "coupe faim"
                        "ventre plat naturel" · "minceur sans frustration"
                        Émotionnel · "j'en peux plus régime" · "marre faim"
                        "envie sucre soir" · variants vernaculaires
                        POURQUOI · fonctionnel pour pain explicit
                        émotionnel pour chaîne deep / identitaire

  Hypothèses figées     H1 · audience FR (pas de scrape EN)
                        H2 · pas de différentiation H/F dans coding
                        H3 · Schwartz dominant solution-aware (cherchent
                             coupe-faim · pas unaware du problème)

  Biais à éviter        Sur-pondération Trustpilot · biais positif marque
                        (clients satisfaits sur-représentés)
                        Under-rep Reddit · biais critique platform
                        (non-buyers vocaux sur-représentés)
                        Imported widgets non-vérifiables · downweight

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Check données first-party (export Shopify · Klaviyo Liv · NPS)
  2. Détection sources publiques + crawl plan triage
  3. Scrape verbatims (Trustpilot · widgets natifs · forums · Reddit)
  4. Coding 4 lentilles (theme · JTBD · Schwartz · pain category)
  5. Détection patterns + gap brand-stated vs customer-said
  6. Synthèse 3 mouvements opérateur-facing
  7. Routing structuré dans entités sub-audience canonical v2.64

  ETA           ~15 min (selon densité corpus disponible)
  Implication   tu valides paramètres d'abord · first-party si dispo · synthèse
  Livrable      synthèse 3 mouvements + corpus Layer A + mutations proposées

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite paramètres AVANT lancement scrape. L'opérateur peut · (a) valider tout · (b) ajuster un paramètre spécifique (e.g. "ajoute Sephora dans canaux", "Schwartz product-aware pas solution-aware", "biais TikTok à intégrer"), (c) abandonner / différer. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set OR si opérateur a flag `--no-disclosure` explicit. Sinon · disclosure obligatoire canon v2.79.5+.

Cross-ref doctrines · `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ (NIVEAU 0 pré-exec) + `docs/system/engagement-disclosure-doctrine.md` v2.79.5 (Paramètres décomposés section).

---

## Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ · crawl multi-sources rate-limited + 4-lens coding par verbatim + 7 Steps cycle complet + Layer A corpus archive + Layer B mutations cross-entities). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement disclosure NIVEAU 0 en amont et synthèse Step 5 + mutations Step 6 en aval.

Pattern obligatoire · l'agent verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique le corpus verbatims et code 4 lentilles par signal, en prose narrative sobre (zéro matrice ASCII en LIVE · les synthèses canon viennent en Step 5 post-coding).

**2 niveaux d'abstraction obligatoires** ·

1. **Macro contexte corpus verbatims cross-canaux** · verbaliser la compréhension du périmètre VoC AVANT de rentrer dans le détail signal par signal.
   Exemple mine-voc · "On part d'une brand {nom · positionnement macro} dont la VoC va surfacer sur {canaux ranked détectés × densité signal estimée}. Mon hypothèse pattern dominant · {majoritairement reviews natifs PDP réguliers · OU verbatims polarisés Trustpilot · OU densité forums spécialisés}. Stade Schwartz audience-side probable · {1-5 inféré canon × signaux brand}. Mon hypothèse de pains prioritaires candidats à confirmer par 4-lens coding · {3-5 pains visibles depuis brand.json + spec.json + JTBD framework} parce que {pattern catégorie + signaux audience-side encoded}. Les vrais axes intéressants ne sont probablement pas les bénéfices revendiqués site mais {ce que les clients soulèvent en mode unprompted}, je vais creuser cette asymétrie en priorité."

2. **Micro signaux par cluster phrasé** · verbaliser les signaux 4-lens en prose narrative pendant le coding par verbatim.
   Exemple mine-voc · "Ce verbatim {citation courte phrasée} touche · lentille JTBD {job-to-be-done dominant phrasé · what they hired the product for} → lentille Schwartz awareness {stage 1-5 phrasé · unaware / problem-aware / solution-aware / product-aware / most-aware} → lentille theme typology {cluster thématique canon · functional / emotional / identity / social} → lentille pain category {surface / consequence / deep canon pain-benefit-chain phrasé}. Cluster auquel ça appartient · {pattern croisé verbatims précédents observé phrasé}. Asymétrie remarquable · {ce que le verbatim révèle que la brand ne voit pas · phrasé canon Step 5 synthesis-first}."

**Calibration narrative** · prose sobre · registre pair senior expert · zéro jargon plumbing (jamais `spec.json#problems_solved[].verbatim_quotes[]`, `_field_types`, `confidence_chain[]`, `PNT-NN` ID brut en LIVE) · zéro tableau ASCII en LIVE (synthèse canon Step 5 prose-first 3 mouvements). Adapter le tonal au registre opérateur détecté (grounded · standard · dense). Cohérent strict avec voice canon Step 5 (no form-fill recap · prose-first · synthesis IS the analysis).

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger si l'agent part dans une mauvaise direction de coding (mauvais JTBD inféré · mauvais stade Schwartz audience-side · mauvaise classification theme typology) AVANT que les downstream pain_points + objections cascadent sur cette base, (b) pédagogie · il apprend la posture experte sur Voice of Customer mining en regardant la manière de penser un cluster verbatim canon 4-lens × pain-benefit-chain.

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

---

## Tone

Strict synthesis-first. Prose-first. Voice canon strict · three movements of plain prose at Step 5, blank line between each, no titles, no bold-section anchors, no field enumeration, no numbers exposed unless load-bearing, no internal vocabulary leaked. The synthesis IS the analysis; it is not a recap of what was scraped.

The Step 5 output follows the snapshot-brand Step 7 canon exactly. Read `.skills/skills/snapshot-brand/SKILL.md § Step 7` and apply its decisive test verbatim before sending: if the output carries bold section labels, numbered headings, "X themes detected" enumerations, or `Field. content.` templated openers, the skill reverted to form-fill and must rewrite.

The corpus volume, the source split, the coding distribution · none of these are operator-facing. They live in Layer A. The operator sees the read, not the inventory.

Anti-pattern bans, non-negotiable.

- No form-fill recap of the form *"I scraped 247 verbatims, identified 12 themes, 5 pain points, 8 objections, 6 audience signals"*.
- No bold-section anchors marking movements.
- No exposed scores, confidence numbers, or coding distribution percentages.
- No internal field paths (`spec.json#problems_solved[].verbatim_quotes[]`) named in the operator surface.
- No platform names listed as a tally (*"Trustpilot: 89, Judge.me: 234, Reddit: 12"*) · provenance shows up only when an asymmetry is the finding.
- No marketing language. Banned vocabulary: supercharge, unlock, empower, leverage, optimize, transform, journey, deep-dive.

---

## Expert methodology

Persona for this skill: senior consumer insights consultant who has read every Trustpilot review on the brand, cross-referenced the Judge.me hero against the Reddit threads naming the brand by name, checked Sephora cross-listings if relevant, and is now sitting across from the operator with one read, two corrections to the brand's stated audience, and one channel opportunity the operator has not surfaced. Not a researcher dumping data. The synthesis is what the operator pays for; the corpus is the substrate that backs every line.

Framework: four lenses applied sequentially per verbatim. Theme typology first (filters the corpus and decides which other lenses run), JTBD second (frames what the customer hired the product for), Schwartz awareness third (depends on vocabulary surfaced in the previous two), pain category fourth and only conditionally on theme = pain. The coding canon is `resources/frameworks/voc-coding.md`. The skill consumes that file; it does not improvise the lenses, does not invent themes outside the closed typology, does not promote singletons to claims.

The triangulation rule from snapshot-brand carries through unchanged. A pattern earns Layer B status when at least three distinct verbatims across or within sources name a close variant of the same thing. Singletons stay in Layer A as evidence; they do not become claims. A four-source convergence on a single signal is a stronger finding than fifty verbatims on one platform · provenance is named when the asymmetry is the read.

Sample before exhausting. When the available corpus exceeds 200 verbatims, code 50 randomly sampled entries first, check whether the coding distribution matches the brand's stated profile, and only run the full pass if the sample shows divergence. This is the validation-cascade-avoidance rule from `docs/system/contextual-intelligence.md` applied to coding: do not run all four lenses on every verbatim before talking to the operator if a sample answers the synthesis question.

---

## Step 0 · First-party data ask (mandatory)

Before scraping anything public, ask the operator. Verbatim:

> *"Avant que je scrape les avis publics, est-ce que tu as :
> - Un export de tes reviews Shopify (CSV) ?
> - Un dump Klaviyo de tes campagnes feedback / NPS ?
> - Des transcripts de support client ?
> - Des résultats de sondage ou enquête client récente ?
> - N'importe quoi de first-party, format libre.
>
> Si oui, drop ici, je le digère en priorité.
> Si non, je pars sur les sources publiques (Trustpilot, Reddit, app stores)."*

Two branches.

**First-party material provided.** Route through `ingest-resource` first to digest the file. The first-party corpus becomes the primary evidence; the third-party scrape that follows runs as cross-validation, not as primary signal. First-party data is denser, less biased, and reflects the buyers the brand actually sells to · not the angry-Trustpilot-leaver minority.

**No first-party.** Proceed to Step 1 with public sources only. Flag the limitation in Step 5 prose, woven into the synthesis: *"Synthèse basée sur sources publiques uniquement. Si tu as des données first-party, on peut affiner."* · never as a separate disclaimer block.

This step is non-negotiable. A skill that scrapes Trustpilot before checking whether the operator has a Klaviyo export with 5000 NPS responses is incompetent. First-party data, when available, is the strongest signal the brand owns.

---

## Step 1 · Source detection and crawl plan

Read `brand.json`. Extract the brand domain, Shopify handle, social handles, marketplaces in `external_ids`, Google Business name. Build the surface inventory.

Available review surfaces, in order of typical density:

- Native review widgets on the brand site · Shopify Product Reviews, Judge.me, Loox, Okendo, Yotpo, Stamped. JS-rendered, requires Chrome MCP capture; static WebFetch returns empty review blocks. Highest density on most Shopify DTC brands.
- Trustpilot if the brand has a profile (`trustpilot.com/review/{domain}`).
- Sephora, Mecca, Marionnaud, Amazon, retail-marketplace cross-listings if the brand sells through them.
- Reddit threads naming the brand or a product by name (search via `site:reddit.com {brand}` plus the niche subreddits the brand's audience inhabits).
- App Store / Play Store reviews if a companion app exists.
- YouTube comments under brand-channel videos and under reviewer videos that name the brand.
- Brand support forum or Discord if accessible.

Output the crawl plan to the operator, one declarative sentence per source. Format: *"Je vais lire ton Judge.me, Trustpilot, et trois threads Reddit qui nomment la marque. Démarre dans 30 secondes."* · no menu, no enumeration of platforms operator has not heard of, no mention of file paths or field names. The plan is binary: surfaces named, run.

Triage probe before deep crawl. For each surface, run a cheap WebFetch or API call to count visible reviews. Three buckets. Dense (>50 verbatims accessible) · sample with quotas per theme. Thin (5-50) · exhaust. Absent (0 or paywalled) · note silently and move on. The triage prevents spending a 30-minute budget on a surface that returns 3 reviews.

---

## Step 2 · Crawl with rate-limit and provenance

Each verbatim captured with full provenance · non-negotiable. The corpus is audit material; an unsourced quote is unusable downstream.

Required fields per verbatim, captured at extraction time:

- Source platform (enum: trustpilot, judge_me, loox, okendo, yotpo, shopify_native, sephora, amazon, reddit, twitter, youtube_comments, tiktok, instagram, app_store, play_store, support_export).
- Source URL or platform-specific reference ID.
- Captured timestamp (ISO 8601).
- Rating if surfaced (1-5 scale; null if the platform does not expose rating).
- Verified-buyer flag if surfaced (true / false / null).
- Raw verbatim text · no paraphrase, no cleanup beyond whitespace normalization.
- Anchor product slug · which SKU the verbatim concerns (null if brand-level).
- Language detected.
- Username retained for first-party data (operator's own export); anonymized for third-party (replaced with `anon_{nano_id}`).

Rate-limit handling: exponential backoff per source, max 3 retries, then skip the surface and continue. 403 / captcha → log surface as `inaccessible` in the run report, do not block. Empty surface → note silently in the run report, do not fabricate. Imported-but-unverifiable widget content (Judge.me / Loox import features) → tag `verified_buyer: false` with `provenance_note: "displayed on-site, source unverifiable"` and downweight in frequency counts.

Caps. 200 verbatims per source maximum at default depth; 1000 verbatims total maximum across all surfaces. Larger corpora require operator-explicit `--depth=deep` flag. The cap exists because a 5000-verbatim corpus does not produce a 25× better synthesis than a 200-verbatim sample · diminishing returns hit hard around the third source.

Cache by `domain × week` to avoid re-scraping the same surface within seven days of a prior run. Documented per platform in `resources/conventions/{platform}.json`.

---

## Step 3 · 4-lens coding per verbatim (+ canon tagging v2.26.0+)

> **Atlas refs** dans cette skill = atlas canon copy (sense 1, référentiel cross-brand doctrine copywriting). Brand-side enrichment via `validations[]` (sense 2 atlas vivant). Distinct de l'atlas brand (sense 4, cartographie holistique data brand) qui désigne la matière brand structurée navigable via `/phantom`. Pour la distinction lexicale complète : `lexicon.md § Atlas, 4 senses MECE`.

<!-- v2.29.0 alignment verify : awareness_stage rename in angle.lineage. Canon tagging field names unchanged (point vers fiches canon copy). Layer A `awareness_stage` field already aligned with `_shared/awareness-stage.json` $ref (5 valeurs canoniques `unaware | problem_aware | solution_aware | product_aware | most_aware`). -->


Apply `resources/frameworks/voc-coding.md` strictly. The order is the order; do not reshuffle.

**Canon tagging additif.** Depuis v2.26.0, chaque verbatim qui passe le coding (i.e. propage à Layer B) est aussi tagué selon les outils canon copy pertinents. Cela enrichit la map et débloquera plus tard les vues `copy-matrix audience × stade-conscience`. Les tags canon ajoutés au verbatim Layer B :

- `canon_schwartz_conscience_id` : un parmi `unaware | problem_aware | solution_aware | product_aware | most_aware` (cohérent avec le coding lens 3 ci-dessous, nommé par référence à `canon copy niveaux-schwartz conscience`).
- `canon_emotion_id` : un terme issu du vocabulaire émotion canonique (espoir, peur, frustration, culpabilite, soulagement, fierte, envie, indignation, surprise, mefiance-eveillee, complicite, regret-anticipe, reconnaissance, appartenance, volonte). Si le verbatim ne porte pas d'émotion claire, laisser null.
- `canon_objection_pattern_id` (uniquement si theme=objection) : un parmi les 4 patterns canon `feel-felt-found | reframe-positif | pre-emption | comparaison-cout-inaction` selon ce que la résolution implicite du verbatim suggère. Souvent null en mining (l'objection est posée, pas encore résolue).

Ces tags sont écrits sur le verbatim dans le Layer A jsonl (`brands/{slug}/sources/voc/{run-date}/{platform}.jsonl`) et utilisés en Step 6 pour informer les routes Layer B.

1. **Theme typology first.** Assign one or many themes from the closed list of seven (pain, benefit, objection, comparison, surprise, vocabulary, social-proof-signal). A verbatim that matches none stays in Layer A as raw evidence and does not propagate to Layer B. Multi-theme is normal · *"le produit est top mais la livraison est catastrophique"* carries benefit (product) plus pain (operational).

2. **JTBD second.** If the verbatim names a job the customer hired the product for, code along three independent dimensions: functional (mechanical change in physical state, time, output, behavior), emotional (internal state the purchase resolves), social (position relative to others the purchase secures). Each dimension is coded only if the language supports it; absence of mention is absence of evidence. Stay in customer voice · if the verbatim only restates a brand claim, JTBD is null.

3. **Schwartz awareness third.** Single value from the five-stage ladder, picking the highest stage the verbatim demonstrates. Most-aware (names the brand or a specific SKU and discusses repurchase, format, or offer terms) → product-aware (names two or more competing branded products) → solution-aware (names the solution category without naming brands) → problem-aware (names the problem state without a solution category) → unaware (downstream symptom, problem unframed). Promotion of a verbatim above the stage its vocabulary supports is back-projection · refused.

4. **Pain category fourth, conditional.** Run only if a theme codes as pain. Tag each category the verbatim explicitly names; multi-category is normal. Functional (product does not deliver the mechanical outcome), emotional (internal state persists or worsens), social (perceived position vs others), financial (absolute cost or value-for-money), temporal (time-to-result, timing-of-purchase, duration-of-use), relational (frictions with another person triggered by purchase or use). The financial-versus-value-perception split is the most consequential miscode · *"c'est trop cher"* alone is financial, *"pour ce que c'est, c'est trop cher"* is value-perception. Code both when ambiguous; the synthesis flags the ambiguity rather than collapse it.

Coding model: Sonnet for v1.0 · JTBD and Schwartz coding quality is the load-bearing factor and Haiku has not been validated yet. A/B test Haiku 4.5 on a 50-verbatim corpus in v1.1 before downgrading.

Layer A entry shape, written to `brands/{slug}/sources/voc/{YYYY-MM-DD}/{platform}-{anchor}.jsonl`, one entry per line. **SSOT du record = `resources/schemas/voc-verbatim.schema.json` (voc-verbatim/1.0 · C1)** · la forme ci-dessous est un rappel, le schéma fait foi.

**Allocation `verbatim_id` (C1)** : séquence numérique PAR BRAND `^VOC-[0-9]{2,5}$` (VOC-01, VOC-02, …), allouée à l'écriture du record · scanner le max existant cross-runs sous `sources/voc/**`, incrémenter · stable, jamais réassigné. C'est LA clé que les Layer B pointent (`verbatim_ref` dans pain_points/objections verbatim_quotes, `voice_ref` dans profile key_expressions, `source_verbatim_ref` dans fears). **Provenance mécanique** : remplir le bloc `extraction` inline ($ref `_shared/extraction-provenance.json` · method/confidence/extracted_at · `absent` exige `lever`). Les jsonl pre-schema (ancien format `id: VOC-{platform}-{nano_id}`) restent valides en l'état, pas de validation rétroactive (audit substrate).

```json
{
  "verbatim_id": "VOC-23",
  "platform": "trustpilot",
  "source_ref": "https://www.trustpilot.com/review/example-brand.com/123456",
  "captured_at": "2026-04-24T14:32:00Z",
  "rating": 2,
  "verified_buyer": true,
  "text": "<exact text, no edits>",
  "product_slug": "respire-sticks-deo",
  "language": "fr",
  "coding": {
    "theme": "pain.functional",
    "jtbd": "regained morning routine",
    "awareness_stage": "product_aware",
    "pain_category": "functional"
  },
  "extraction": { "extraction_method": "headless", "extraction_confidence": 0.8, "extracted_at": "2026-04-24T14:32:00Z" }
}
```

Batch coding in groups of 30-80 verbatims per pass to keep token usage bounded. Sample first when corpus exceeds 200 (see § Expert methodology).

---

## Step 4 · Pattern detection and gap analysis

After coding, four reads run on the corpus.

**Recurring themes.** A theme reaches Layer B status when at least three distinct verbatims (across or within sources) carry close variants of it. Cluster on JTBD, pain category, and theme + sub-axis. Singletons stay in Layer A as audit material; they do not become claims.

**Brand-stated vs customer-said gaps.** Compare `brand.json#positioning`, `brand.json#tone_of_voice`, and `brand.json#identity` claims against the dominant verbatim themes. The brand says X · do customers actually mention X, or do they talk about Y? Compare each `audiences/{slug}/profile.json#identity` against the demographic clues and registers surfaced in coding. Every contradiction is a load-bearing finding · the operator paid for snapshot's hypothesis, the customers either ratified it or invalidated it. Synthesis surfaces the contradiction explicitly, never silently overwrites.

**Audience signals.** Demographic clues, life-stage references, professional context, language register. When a coherent cluster shows up that is distinct from the existing audience folders (a B2B sub-segment in a B2C brand's reviews, a 22-32 sub-cohort in a brand targeting 35-50, a male buyer pattern in a female-positioned brand), propose a new audience candidate with `validation_status: "hypothesis"` and `_source_meta.origin: "voc-mining"`.

**Vocabulary patterns.** Recurring expressions, vernacular phrasings, customer-voice anchors. These feed `profile.json#voice.key_expressions[]`. Two filters apply. First, distinguish vernacular from brand-jargon-echoed-back · *"actifs naturels"* repeated in customer reviews is the brand's positioning vocabulary returned, not customer voice. Tag it as benefit-claimed, not vocabulary. Second, frequency without sample_size is meaningless; the schema enforces the denominator (e.g. `frequency: 47, sample_size: 89, platform: trustpilot`).

**Channel signals.** Sources that surfaced the brand organically (Reddit threads, niche-forum mentions, YouTube reviewer pieces) are channel hypotheses. A 47-upvote thread on r/Skincareaddiction naming the brand as *"ce que j'aurais voulu trouver plus tôt"* is an untapped acquisition signal · the brand has organic resonance in a community it has not activated in paid. These route to `learnings.json` as channel-opportunity entries when the operator validates them at Step 5 close.

---

## Step 5 · Operator-facing synthesis (mandatory format)

Apply the snapshot-brand Step 7 canon strictly. Pure prose, three movements, blank line between each, no titles, no bold-section anchors, no enumeration, no scores, no "X themes detected", no platform tally.

**Movement 1.** What the customers reveal about who they are and why they buy. Often diverges from the brand-stated audience. Name the divergence in the first or second sentence · that is the headline. Use the JTBD and Schwartz coding as raw material; do not name the framework. A reader should leave Movement 1 knowing who actually buys and what they hired the product for, in customer voice, not in brand voice. 1-3 sentences.

**Movement 2.** What customers say about the product and the offer that the brand does not claim, or claims differently. The brand-stated-vs-customer-said gap from Step 4 lands here. If the brand communicates performance and customers buy softness, this is where it surfaces. If the offer architecture suggests one thing and the verbatims reveal another, this is where it surfaces. Use comparison-vs-competitor and benefit-perceived-vs-claimed coding as raw material. 1-3 sentences.

**Movement 3.** The one or two things the operator likely did not see. Channel opportunity (organic resonance in an unactivated community), dissonant signal (a pattern that contradicts brand identity in a way the brand can lean into), ops gap (a recurring delivery / packaging / support flag distinct from the product itself), regulatory or trust signal (a third-party-named concern the brand should know about). The skill is paid for these. 1-3 sentences.

End with a closing line, prose-form, conditional on what was surfaced:

> *"Want to validate and route these signals into the brand context, or keep digging?"*

Hard rule, restated: never list "themes detected", "verbatims captured", "platforms scraped", "patterns identified", "audiences found" as numbers. The synthesis IS the analysis. The corpus volume lives in Layer A · the operator can audit it on demand, never as default surface.

If sources were thin or inaccessible, weave the limitation into the synthesis prose: *"Trustpilot returned 0 reviews · ta marque n'est pas encore indexée là-bas, ce qui colore le read"*. Never as a separate "data quality" block.

Decisive test before sending. Read the synthesis as a stranger. If it carries bold section labels, numbered headings, *Field. content. Field. content.* templated openers, or any enumeration of internal structure (`coded 247 verbatims`, `12 themes detected`, `4 audience signals`), the skill reverted to form-fill. Rewrite as flowing prose where each paragraph names what it carries via its first sentence, not via a label above it.

---

## Step 6 · Routing into entity files (Layer B)

Based on patterns confirmed at Step 4, propose mutations through the canonical channel. All writes are `mode=proposed`; nothing direct.

`python3 .skills/write-to-context.py --mode proposed --field-path {path} --value {value} --source {voc} --confidence {0.55-0.85}` for each routed signal.

Route map.

- `products/{slug}/spec.json#problems_solved[].verbatim_quotes[]` · top 3-5 representative quotes per problem, each carrying `_source_meta.origin: "voc"` and pointing by `verbatim_ids` into Layer A. Frequency and urgency derived from corpus counts (1-10 scale per schema).
- `products/{slug}/spec.json#benefits[].verbatim_quotes[]` · same shape, surfacing perceived-benefit angles the brand under-exploits.
- **`products/{slug}/spec.json#benefits[].emotional_signal` + `.latency_min` / `.latency_max` + `.evidence_verbatim[]` (v1.10 NEW fields, v2.58 write-side)** · lors du coding lens 2 (JTBD emotional dimension) et lens 1 (theme=benefit), identifier verbatims qui portent un ressenti spécifique exprimé (`emotional_signal`), une fenêtre temporelle ressenti effet (`latency_min` / `latency_max`, ex *"après 3 semaines je sentais"*, *"il faut 2 mois pour voir"*) et des quotes anchored (`evidence_verbatim[]`). Stage par benefit indexé :

  ```bash
  python3 .skills/write-to-context.py --path "products/{p_slug}/spec.json#/benefits/{idx}/emotional_signal" --value "{quote}" --source agent --confidence 0.7 --mode proposed --reason "VoC mining anchored"
  python3 .skills/write-to-context.py --path "products/{p_slug}/spec.json#/benefits/{idx}/latency_min" --value {N} --source agent --confidence 0.6 --mode proposed --reason "VoC mining time-to-effect"
  python3 .skills/write-to-context.py --path "products/{p_slug}/spec.json#/benefits/{idx}/latency_max" --value {N} --source agent --confidence 0.6 --mode proposed --reason "VoC mining time-to-effect"
  python3 .skills/write-to-context.py --path "products/{p_slug}/spec.json#/benefits/{idx}/evidence_verbatim" --value '["{quote_1}","{quote_2}"]' --source agent --confidence 0.7 --mode proposed --reason "VoC anchored evidence"
  ```

  Absence de signal temporel ou émotionnel = absence d'evidence, ne pas inventer. Stage uniquement les benefits où la verbatim corpus porte le signal.

- **`brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json` (v1.3.0 v2.64 ontologie sémantique pure · SUB-AUDIENCE)** · pain_points appartiennent sémantiquement à une audience · sub-parent path canonical. Chaque pain point staged = entité complète fichier dédié `brands/{slug}/audiences/{a_slug}/pain_points/{PNT-NN}.json` (owned natif). Plus de array `affected_audiences[]` nécessaire (la parent path déclare l'audience owner).

  Generation incrémentale PNT-NN · scan `brands/{slug}/audiences/*/pain_points/*.json` existing pour next id cross-audiences (PNT-01, PNT-02, ... PNT-NN max + 1). Pattern stable PNT-NN, jamais réassigné. Si un pain similaire détecté cross-audiences (même phenomenon dans 2 audiences), stage UNE entité dans chaque audience parente (pas de dedup cross-audience · sémantique d'appartenance owned).

  Entité shape (full file) ·

  ```json
  {
    "pain_id": "PNT-{NN}",
    "formulation": "{verbatim customer-voice}",
    "pain_category": "physical | emotional | friction_ux | logistical | cognitive | social_status",
    "chain": [
      {"level": "surface", "formulation": "{ce qu'elle dit}"},
      {"level": "consequence", "formulation": "{impact quotidien}"},
      {"level": "deep", "formulation": "{sens identitaire}"}
    ],
    "emotion": "{dominant emotion}",
    "trigger": "{contextual trigger}",
    "awareness_stage": "{Schwartz stage}",
    "affected_products": ["{p_slug}"],
    "_source_meta": {
      "origin": "voc",
      "platform": "{platform}",
      "sample_size": {N},
      "date_captured": "{ISO date}",
      "verbatim_ids": ["VOC-{platform}-{nano_id}", ...]
    },
    "meta": {
      "validation_status": "hypothesis",
      "_source": "observed",
      "created_by_skill": "mine-voc",
      "created": "{date}"
    }
  }
  ```

  Mutation gate (stage entité complète) ·

  ```bash
  python3 .skills/write-to-context.py --path "audiences/{a_slug}/pain_points/{PNT-NN}.json" --value '{<full pain_point entity JSON>}' --source agent --confidence 0.7 --mode proposed --reason "v2.64 ontologie sémantique pure · sub-audience canonical"
  ```

  Backward compat strict additif · si la brand cible est en migration partielle, fallback lecture transparent `brands/{slug}/pain_points/{PNT-NN}.json` top-level v2.63 si sub-audience vide. Write-side v1.3.0 stage toujours sub-audience canonical.

  Cross-ref canonical friction · `friction.cross_refs.pain_point_ids[]` référence désormais les PNT-NN sub-audience canonical (lookup via parent audience path).

- **`brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json` (v1.3.0 v2.64 ontologie sémantique pure · SUB-AUDIENCE)** · objections appartiennent sémantiquement à une audience · sub-parent path canonical. Chaque objection staged = entité complète fichier dédié `brands/{slug}/audiences/{a_slug}/objections/{OBJ-NN}.json` (owned natif). Plus de array `affected_audiences[]` nécessaire.

  Generation incrémentale OBJ-NN · scan `brands/{slug}/audiences/*/objections/*.json` existing pour next id cross-audiences (OBJ-01, OBJ-02, ... OBJ-NN max + 1).

  Entité shape (full file) ·

  ```json
  {
    "objection_id": "OBJ-{NN}",
    "type": "prix | scepticisme | temps | confiance | urgence | efficacité | comparaison",
    "formulation": "{verbatim customer-voice}",
    "frequency": {1-10},
    "severity": "low | medium | high",
    "severity_score": {1-10},
    "response_counter": "{counter-réponse opérateur}",
    "derived_angle_refs": ["ANG-{NN}", ...],
    "lifecycle_stage": "awareness | consideration | decision | post_purchase",
    "affected_products": ["{p_slug}"],
    "_source_meta": {
      "origin": "voc",
      "platform": "{platform}",
      "sample_size": {N},
      "date_captured": "{ISO date}",
      "verbatim_ids": ["VOC-{platform}-{nano_id}", ...]
    },
    "meta": {
      "validation_status": "hypothesis",
      "_source": "observed",
      "created_by_skill": "mine-voc",
      "created": "{date}"
    }
  }
  ```

  Mutation gate (stage entité complète) ·

  ```bash
  python3 .skills/write-to-context.py --path "audiences/{a_slug}/objections/{OBJ-NN}.json" --value '{<full objection entity JSON>}' --source agent --confidence 0.7 --mode proposed --reason "v2.64 ontologie sémantique pure · sub-audience canonical"
  ```

  Backward compat strict additif · fallback lecture `brands/{slug}/objections/{OBJ-NN}.json` top-level v2.63 si sub-audience vide. Write-side v1.3.0 stage toujours sub-audience canonical.

  Cross-ref canonical friction · `friction.cross_refs.objection_ids[]` référence désormais les OBJ-NN sub-audience canonical.

- **Legacy write `profile.json#/pain_points` + `profile.json#/objections` DEPRECATED v1.2.0** · Profile v2.0 BREAKING post-v2.63 · sub-fields `profile.pain_points[]` et `profile.objections[]` ne sont PLUS écrits par mine-voc v1.2.0+. Read backward compat preserved · les profile.json brownfield v1.7 contenant sub-fields legacy restent lisibles (skills downstream lisent les deux paths · top-level collections en priorité, profile sub-fields fallback legacy). Migration progressive · scripts upstream peuvent migrer profile.pain_points[] → pain_points/{PNT-NN}.json files sans casser lecture.

- `audiences/{slug}/profile.json#voice.key_expressions[]` · 5-10 highest-frequency real-customer phrases. Mandatory triplet: `frequency`, `sample_size`, `platform`. Frequency without denominator is refused at the schema level. (Préservé v1.2.0 · vocabulary reste audience-bound sub-field profile.json, pas collection séparée.)
- `audiences/{slug}/profile.json#psychology.beliefs_limiting` · only if a belief recurs in three or more verbatims and contradicts a brand claim. (Préservé v1.2.0 · psychology reste audience-bound sub-field.)
- New `audiences/{new-slug}/profile.json` scaffolded if a coherent sub-segment surfaces that is distinct from existing audience folders. Status `hypothesis`, source `voc-mining`. Operator can reject in next turn; the proposal lives until accepted.
- `brand.json#tone_of_voice` flags · if customers describe the brand in language wildly different from the brand's stated tone, flag for operator review. Never auto-overwrite operator-validated tone.
- `learnings.json` append · only when a cross-session-stable pattern earns it (a recurring ops flag the operator confirmed actionable, a regulatory signal that warrants compliance review, a channel opportunity the operator wants tracked across sessions). Routine theme detection does not append learnings.

Layer A corpus written to `brands/{slug}/sources/voc/{YYYY-MM-DD}/{platform}-{anchor}.jsonl`. Never auto-loaded into context. Audit substrate, queryable on demand, copy-gold reservoir for downstream skills (`generate-hook-brief`, ad copy generation, email sequencing) · those skills pull verbatims from here, never invent.

Every Layer B field carrying VoC content must reference at least one Layer A `id` via `_source_meta.verbatim_ids`. The link is mechanical · operator clicks a synthesized claim, lands on the raw verbatim that justifies it. No claim without backing evidence.

Never overwrite operator-validated data. If a `profile.json` field carries `_source: operator`, propose update via `mode=proposed`; the operator accepts or rejects in the next turn. Direct overwrite of operator-stated fields is refused at the mutation gate.

---

## Step 7 · Finalize (mandatory)

Run, after all Step 6 mutations complete:

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mechanical Python primitive. No LLM negotiation. No skip path.

Exit code 0 → ship; the synthesis from Step 5 is delivered to the operator. Exit code 2 → blocking issue (schema violation, broken Layer A reference, missing denominator on a key_expressions entry, validate-resources MAJOR/CRITICAL). Revise the offending mutation, re-run finalize, do not deliver Step 5 until exit 0.

Skipping Step 7 is the kind of failure that produces a coherence_check warning at turn-end-audit. The hook reads finalize events; if the skill claims "VoC mining done" without a finalize event for the run window, the hook flags an unchecked-entity-claim warning to the operator. Non-negotiable.

After finalize exit 0, trigger the brand snapshot rebuild silently:

```bash
python3 .skills/build-brand-snapshot.py {slug}
```

Per the master mutation rule, any write to a brand's core files refreshes `_snapshot.md`. ~50ms per brand.

---

## --focus parameter modes

The skill ships four narrow modes that adjust Step 5 synthesis emphasis without changing the Step 1-4 mining. Layer A is always full; only the operator-facing surface narrows.

- **default** (no flag) · full three-movement synthesis as specified at Step 5.
- **--focus=objections** · Movement 1 names the audience-as-revealed; Movements 2 and 3 surface only objections, blockers, post-purchase regret. Benefits and vocabulary skipped from the prose. Useful when the operator is briefing a sales-page rebuild and needs the friction inventory in customer voice.
- **--focus=vocabulary** · Movement 1 names the audience; Movements 2 and 3 surface only customer-vocabulary patterns (vernacular expressions, recurring terms, register markers). Theme synthesis skipped. Useful when the operator is writing copy and needs the words their customers actually use.
- **--focus=audience-refinement** · All three movements reorient around audience: who the customers are vs who the brand thought they were, what sub-segments surfaced, where the demographic clues land. Useful after snapshot when the operator suspects the inferred audience is off.
- **--focus=channel-signals** · All three movements reorient around acquisition: where the brand has organic resonance it has not activated, what communities surface the brand by name, what third-party validations show up unprompted. Useful when the operator is planning paid channels and wants the unactivated-organic read first.

Layer A corpus is full regardless of focus mode; the focus only narrows what the operator sees in the synthesis. A subsequent invocation with a different focus reads the same Layer A and re-renders Movement-prose without re-scraping.

---

## Triggers and chaining contexts

Three contexts surface this skill.

**Standalone invocation.** Operator pastes *"voc on respire"*, *"voc {brand}"*, *"scrape les avis pour {brand}"*, *"extrais ce que disent les clients de {brand}"*, *"mine reviews for {brand}"*. Direct trigger. Skill checks brand exists with `brand.json` filled, runs Step 0 ask, proceeds.

**Post-snapshot escape hatch.** At Step 7 close of `snapshot-brand`, the synthesis paragraph proposes (in prose, not menu): *"Want me to go pull what your actual customers say (Trustpilot, native reviews, Reddit) and validate the audience I just inferred? ~10 min."* Operator says yes → mine-voc launches in subagent (Sonnet, `subagent_safe: true`). Snapshot's inferred audience and tone become the testable hypothesis; mine-voc validates or contradicts.

**Orchestrator chaining.** `deepen-brand-context` orchestrator chains mine-voc → mine-vom → final synthesis. mine-voc first (this brand's customers), mine-vom second (the market and competitors), final synthesis cross-references the two. The orchestrator passes `--depth=standard` by default; operator can override at trigger.

---

## Hard Rules

- **Step 0 first-party ask is non-negotiable.** Never start scraping without asking. A skill that misses a 5000-row Klaviyo NPS export because it skipped to Trustpilot is incompetent.
- **Triangulation mandatory.** Minimum three sources before naming a pattern. Singletons stay in Layer A; they do not become Layer B claims.
- **Source provenance always tagged.** Trustpilot ≠ Judge.me ≠ Reddit ≠ Sephora ≠ Amazon. Never aggregate cross-platform without naming the split when the asymmetry matters. A 4.7 average on Loox plus a 2.1 on Trustpilot is not a 3.4; it is a story about who shows up where.
- **Synthesis follows snapshot Step 7 canon strictly.** Three movements of prose, blank line between, no titles, no bold-section anchors, no exposed numbers, no field paths leaked. The decisive stranger-test runs before send.
- **Schema field semantics as analytical vocabulary, never as JSON path mentions.** The skill reasons over `voice.key_expressions` and `pain_points`; it never says those words to the operator.
- **Inferred attributes flagged inline** with *"(à valider)"* / *"(I deduced this)"* · never as a separate "missing fields" or "low confidence" block.
- **finalize-mutation-batch mandatory at Step 7.** Skipping = unchecked-entity-claim warning at turn-end-audit. No skip path. Exit code 2 blocks Step 5 delivery until revised.
- **Verbatim citation policy.** Third-party reviews retain URL and timestamp, anonymize username (replace with `anon_{nano_id}`). First-party data retains author identifier when the operator's export carries one. GDPR consideration: redact email fragments and full names at extraction time.
- **Never overwrite operator-validated data.** Fields carrying `_source: operator` route through `mode=proposed`; the operator accepts or rejects in the next turn. Direct overwrite is refused at the mutation gate.
- **Cap per session.** 200 verbatims per source maximum at default depth, 1000 verbatims total maximum across all surfaces. Larger corpora require operator-explicit `--depth=deep`. Diminishing returns hit hard around the third source.
- **Coding canon non-negotiable.** Read `resources/frameworks/voc-coding.md` at first invocation per session. The four lenses, their order, their binary tests, and their anti-patterns are consumed verbatim. The skill does not improvise the coding.
- **Imported-but-unverifiable widget content downweighted.** Judge.me / Loox / Yotpo allow brands to import or fabricate reviews. Tag `verified_buyer: false` with `provenance_note` when the platform does not expose verification, and downweight in frequency counts.
- **Public-only by default.** Private support tickets require explicit operator authorization before ingestion.
- **Recency weighting.** Reviews older than 12 months carry less weight in synthesis unless the operator asks otherwise. A 2019 review of a discontinued formulation is noise.
- **No fabrication.** Never invent verbatims, never composite quotes from multiple reviewers, never paraphrase into the corpus. The corpus is audit substrate; the synthesis can paraphrase, the corpus never does.

---

## Cross-references

- `resources/frameworks/voc-coding.md` · analytical canon for the four lenses. Mandatory read at first invocation per session. The skill consumes; it does not improvise.
- `.skills/skills/snapshot-brand/SKILL.md § Step 7` · voice canon source for Step 5 synthesis. Three-movement prose, blank-line separation, no-title rule, decisive stranger-test.
- `.skills/skills/ingest-resource/SKILL.md` · first-party data digestion path. Routed at Step 0 when operator drops a CSV / Klaviyo export / support transcript.
- `.skills/skills/mine-vom/SKILL.md` · sister skill for market-level voice (competitors, niche communities). Disambiguation: mine-voc reads this brand's customers; mine-vom reads the market.
- `.skills/skills/mine-audience/SKILL.md` · sister skill for product-level audience discovery. Disambiguation: mine-audience clusters audiences from market scraping; mine-voc mines verbatim from existing customers.
- `.skills/finalize-mutation-batch.py` · mandatory Step 7 primitive. Mechanical, exit 2 = block.
- `.skills/write-to-context.py` · canonical mutation channel. All Layer B writes route through this; never `Edit` on JSON.
- `.skills/build-brand-snapshot.py` · silent rebuild after Step 7 finalize. Per master mutation rule.
- `.claude/hooks/turn-end-audit.py` · reads coherence_check events. Flags unchecked-entity-claim if Step 7 finalize did not run.
- `docs/system/contextual-intelligence.md` · master doctrine. Validation-cascade-avoidance and trust-the-model rules govern the workflow.
- `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ NIVEAU 0 + v2.81.1+ NIVEAU LIVE · doctrine racine 3 phases temporelles · AVANT exec NIVEAU 0 paramètres décomposés (Engagement disclosure pré-runtime) · PENDANT exec NIVEAU LIVE thinking aloud expert action LOURDE 2 niveaux abstraction macro contexte corpus + micro signaux par cluster 4-lens phrasé · APRÈS exec synthèse Step 5 prose-first 3 mouvements + Step 6 mutations sub-audience canonical · HR-DVD-11 + AP-DVD-11 enforcement.
- `docs/system/voice.md` · voice canon. Operator-facing synthesis follows it strictly.
- `resources/schemas/spec.schema.json`, `resources/schemas/profile.schema.json` · exit points for Layer B mutations. Field definitions live there.

---
