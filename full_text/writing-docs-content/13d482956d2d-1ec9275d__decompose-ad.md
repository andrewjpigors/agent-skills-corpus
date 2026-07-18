---
name: decompose-ad
version: 2.4.0
type: producer
isolation_scope: brand_only
layer: production
recommended_model: opus
reasoning_pattern: matrix-driven
matrix_mode: decomposing
description: >
  v2.3.0 (Brique 4 étape D · repath REVERSE batch + namespace RCV + schéma decomposition natif + mkdir-claim) · DEUX bras de persist, DEUX namespaces séparés. Benchmark / ad concurrente (`external_benchmark` / `trendtrack_pull` / `manual_drop` inconnu) → `brands/{slug}/competitive-intel/{batch}/{RCV-NN}/decomposition.json` (namespace RCV, schéma natif reverse `decomposition/1.0`). Créa NÔTRE décortiquée (`internal_production`) → `brands/{slug}/creatives/{batch}/{CRT-NN}/` (namespace CRT, split genome/creative/sidecar/brief comme compose-creative). mkdir-claim atomique STEP 0 par bras avant tout write. beat_type/style_id/mechanic_id émis via snapshot enum projeté du registre (pont A=B). Backward compat · forme cible imposée par le gate · anciennes écritures plates déjà rejetées runtime.
  v1.5.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · reverse-engineer benchmark ad concurrente · si reverse-engineer mentionne pain ou objection détectée dans ad concurrente sur même audience que brand opérée, link vers `audiences/{audience_slug}/pain_points/*.json` ou `audiences/{audience_slug}/objections/*.json` sub-audience canonical SI applicable. Sinon · note descriptive sans canonical ref. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.4.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · reverse-engineer benchmark ad concurrente · si reverse-engineer mentionne pain ou objection détectée dans ad concurrente, link vers `pain_points/*.json` ou `objections/*.json` collections SI applicable (ad sur même audience que brand opérée, signal cross-applicable). Sinon · note descriptive sans canonical ref (ad concurrente = pas notre canonical, observation pure). Backward compat preserved.
  v1.3.2 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.3.0 (v2.46 alignment) : HR2bis + anti-pattern reference endpoint canon nano-banana-2/edit cohérent compose/recompose/craft-packshot.
  v1.2.0 (v2.32 alignment) : reads intent_mix (fallback intent if absent) + overlay_density (fallback craft_mode) + meta.validation_status accepts both shapes.
  Decompose une ad (benchmark concurrent OU créa marque interne) en fiche structurée
  selon l'équation compositionnelle v3.1 (NOYAU x CONTEXTE x MODIFIEURS) et persiste,
  selon le bras, soit un `decomposition.json` reverse natif (benchmark) soit le split
  genome/creative/sidecar/brief (créa interne). Reverse-engineering, pas génération.
  Inputs supportés : drop image dans le chat (mode primaire), pull TrendTrack via
  ad_id (`facebook_NNN`) ou URL Meta Ads Library, URL externe (Insta, LinkedIn,
  Reddit) via WebFetch + screenshot fallback. Output operator-facing : fiche v5
  S55 quatre sections (CE QUE L'AD MONTRE / RACONTE / DIAGNOSTIC / RÉUTILISATION)
  + bloc TAGS retrieval. Persist : `competitive-intel/{batch}/{RCV-NN}/decomposition.json`
  pour benchmark, `creatives/{batch}/{CRT-NN}/` (split) pour créa interne. Path + namespace
  auto déterminés par tags.source.
  FR: "decompose cette ad", "analyse cette créa", "que dit cette ad", "decompose",
  "reverse-engineer cette ad", "decompose cette pub".
  EN: "decompose this ad", "analyze this creative", "decompose", "reverse-engineer this ad".
permissions:
  reads: [brand, product, profile, learning, strategy, canon_copy, registries]
  writes: [creative, learning]
  emits_events: [coherence_check, mecanique_proposal_flag]
  mode: proposed
  subagent_safe: true
  external_apis:
    - provider: "fal.ai"
      endpoint: "fal-ai/nano-banana-2/edit"
      model_family: "gemini_3_pro_image_novembre_2025"
      version_check_url: "https://fal.ai/models?keywords=banana"
      version_canon_date: "2025-11"
      replaced_legacy: "fal-ai/nano-banana-pro/edit (v1.0.x-v1.2.x · Gemini 2.5 Flash Image)"
      auto_upgrade: false
      note: "Endpoint référencé pour compose mode downstream (HR2bis lookup visual_identity packshot input). decompose-ad lui-même reste reverse-engineering, pas de gen direct."
    - provider: "trendtrack"
      endpoint: "trendtrack_pull_ad"
      version_canon_date: "2025-08"
      note: "TrendTrack pull mode (HR1 lookup ad_id facebook_NNN). Indépendant fal.ai migration."
consumes:
  - path: resources/templates/creative-formula.md
    min_version: 3.1.0
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
    note: "SSOT free-string évolutif. NE PAS enum-locker. Snapshot enum versionné projeté pour le pont A=B (beat_type/style_id/mechanic_id), pas le registre lui-même."
  - path: resources/schemas/decomposition.schema.json
    min_version: 1.0.0
    note: "NEW Brique 4 étape D · schéma natif reverse (decomposition/1.0, promotion de video-ad-analysis-v1.0). Cible de validation du benchmark RCV (PAS creative.schema · creative_id^CRT- rejette une décompo RCV)."
  - path: resources/schemas/creative.schema.json
    min_version: 1.3.0
    note: "couche lignage du BRAS INTERNE (creative/1.3 · variant_of CRT|RCV + lineage{}). PAS la cible du benchmark."
  - path: resources/schemas/genome.schema.json
    min_version: 1.2.0
    note: "NEW · ADN du BRAS INTERNE (genome/1.2 · script_id GSC-NN, hook, frames, support, genome_tags · mêmes enums beat_type/style_id/mechanic_id que decomposition.schema = pont A=B)."
  - path: resources/schemas/produced-asset.schema.json
    min_version: 1.0.0
    note: "NEW · sidecar manifest binaire (produced-asset/1.0 · 1 par binaire produit, anti-orphelin · benchmark image de réf comme interne JPG)."
  - path: resources/conventions/creative-storage.md
    min_version: 1.0.0
    note: "forme batch creatives/{batch}/{CRT-NN}/ + competitive-intel/{batch}/{RCV-NN}/ + allocation mkdir-claim (D#481)."
  - path: resources/schemas/_shared/awareness-stage.json
    min_version: 1.0.0
  - path: resources/canon/copy/niveaux-schwartz/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/hooks/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/angles/*.json
    min_version: 1.0.0
  - path: resources/canon/copy/heuristiques-persuasion/*.json
    min_version: 1.0.0
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
  - path: brands/{slug}/audiences/{audience}/profile.json
    min_version: 1.0.0
  - path: brands/{slug}/products/{product_slug}/spec.json#visual_identity
    min_version: 1.10.0
    note: visual identity assets (packshots, color_palette, container, content, label, distinctive_features) consumed for product fidelity in regen pipelines
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/system/output-clarity-doctrine.md
  - path: docs/system/operator-vocabulary-translation.md
produces_validations_for:
  - resources/canon/copy/hooks/*.json
  - resources/canon/copy/angles/*.json
  - resources/canon/copy/heuristiques-persuasion/*.json
produces_proposals_for:
  - brands/{slug}/competitive-intel/{batch}/{RCV-NN}/decomposition.json
  - brands/{slug}/competitive-intel/{batch}/{RCV-NN}/produced/{slug}.json
  - brands/{slug}/competitive-intel/{batch}/{RCV-NN}/produced/{slug}.jpg
  - brands/{slug}/creatives/{batch}/{CRT-NN}/genome.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.json
  - brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg
  - brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md
disambiguates_against:
  audit-meta-account: "route to audit-meta-account when operator wants to audit a full Meta account (KPI, structure campaigns, pixel, attribution), not a single ad. decompose-ad is one creative at a time."
  produce-paid-angles: "route to produce-paid-angles when operator wants to PRODUCE angles (forward generation from brand intelligence). decompose-ad is reverse-engineering on an existing ad."
  analyze-copy: "route to analyze-copy for long-form copy decomposition (VSL, sales letter, email). decompose-ad is single-ad creative, copy + visual + format coupled, equation v3.1."
  watch-competitors: "route to watch-competitors for ongoing surveillance of a competitor library. decompose-ad is one ad, deep, persisted (benchmark → competitive-intel/{batch}/{RCV-NN}/decomposition.json ; interne → creatives/{batch}/{CRT-NN}/)."
pipeline:
  preconditions: "brand exists with brand.json. Audience optional but recommended (lookup buyer_user_split + persona_archetype). TrendTrack mode requires TRENDTRACK_API_KEY in credentials_shared.env. {batch} courant résolu (run date-stampé du jour, ex 2026-06-07-NN) et `mkdir -p` du dossier-batch parent du BON arbre (competitive-intel/{batch}/ pour benchmark, creatives/{batch}/ pour interne) exécuté AVANT le mkdir-claim, sinon STEP 0 n'a pas de dossier-batch parent."
  postconditions: "BENCHMARK · decomposition.json (decomposition/1.2) persisté sous competitive-intel/{batch}/{RCV-NN}/ via write_to_context mode=proposed ; image de réf éventuelle écrite DIRECT sous {RCV-NN}/produced/{slug}.jpg AVEC sidecar produced/{slug}.json. INTERNE · genome.json (genome/1.2) + creative.json (creative/1.3) + sidecar + brief.md persistés sous creatives/{batch}/{CRT-NN}/. Dossier {RCV-NN}/ ou {CRT-NN}/ créé par mkdir-claim atomique (STEP 0) avant tout write. Fiche markdown v5 returned to operator, mecanique flag emitted if registry gap detected."
---

# Skill: decompose-ad

> **Reverse-engineer an ad.** v2.3.0 · S55 fiche v5 · benchmark → `decomposition/1.2` (RCV) · interne → split `genome/1.2` + `creative/1.3` (CRT) · forme batch · équation v3.1 · D#391/D#481.

> **v2.3.0 (Brique 4 étape D)** : repath REVERSE vers `competitive-intel/{batch}/{RCV-NN}/decomposition.json` (namespace RCV, schéma natif reverse), bras interne vers `creatives/{batch}/{CRT-NN}/` (namespace CRT, split comme compose-creative), mkdir-claim atomique par bras, snapshot enum projeté pour le pont A=B. Voir HR8 + HR-DA-CANON-1.

Decomposeur, not generator. Lit une ad (visuel + copy verbatim), applique l'équation compositionnelle v3.1, persiste · selon le bras · soit un `decomposition.json` reverse natif (benchmark, namespace RCV) soit le split genome/creative/sidecar/brief (créa interne, namespace CRT), rend une fiche structurée à l'opérateur en langage clair. Le mécanisme reste invisible (pas de field paths, pas de scores numériques, pas de noms internes). L'opérateur voit une fiche quatre sections et un bloc tags retrieval.

## Tone

Posture éducateur + collègue senior. Pas inspecteur, pas pixel-counter. La fiche est dense mais lisible : phrases courtes, observable d'abord (Section 1), interprétation ensuite (Section 2), diagnostic franc (Section 3), réutilisation actionnable (Section 4). Aucun jargon plumbing, aucun nom de field JSON, aucun acronyme doctrine en surface. Si un texte n'est pas visible ou pas inférable, écrire `-` (jamais halluciner pour combler).

## Expert methodology

**Persona.** Senior creative strategist qui a décomposé dix mille ads paid social cross-typologies (info-produit, cosmétique, supplément, SaaS, DTC apparel, marketplace). Lit une ad comme un copywriter senior lit un sales letter : isole le pivot, nomme la mécanique, juge la cohérence chaîne descendante (audience → insight → angle → mécanique → craft).

**Framework.** Équation compositionnelle v3.1 stress-tested S55 (23 ads cross-typologies). NOYAU = invariant créa (mecanique × format × stop_scroller × ton). CONTEXTE = couches stratégiques branchables (angle × pain_point × persona × proof). MODIFIEURS = override situationnels (occasion × situation × offer × destination × produit × mix_pillar × campaign × regulatory × seasonality_trigger). Source canon : `resources/templates/creative-formula.md`.

**DEUX niveaux de mécanique (D#488) · NE PAS CONFONDRE.**
1. **Mécanique AD-LEVEL = le CONCEPT de l'ad** (versus, trending-fake-natif, product_focus, avant/après, packshot…) → SSOT `resources/registries/creative-mechanics-registry.md` (free-string, jamais enum-locké, on n'y écrit jamais ; `other` + `mecanique_proposal` si rien ne fitte). Persisté dans **`decomposition.mecanique.mecanique_id`** (+ `axis` claim/visual + `typology_st` spatial/temporel + `confidence`). **C'est le tag ROI d'un STATIQUE** : image = spatial, le concept porte tout le message.
2. **Mécanique HOOK-LEVEL = l'accroche** (les 3 premières secondes) → vocabulaire SÉPARÉ, le `hook-mechanics-registry` (= `resources/registries/hooks/`), persisté dans **`script.hook.mechanic_id`**. **Le hook n'a de sens qu'en VIDÉO (temporel)** ; sur un statique il est souvent absent → NE PAS le forcer (mettre `other-uncategorized` plutôt que tordre une promesse).

`beat_type` / `style_id` = autres axes (snapshot enum HR8bis). Le pont A=B porte les deux niveaux. **Le registre creative-mechanics reste SSOT évolutif** ; on n'enum-locke jamais ce fichier et on n'y écrit jamais.

---

## HR1 · Detect input mode

L'opérateur peut fournir l'input sous quatre formes. Detection auto :

| Input shape | Mode | Action |
|---|---|---|
| URL `api.trendtrack.io/...` ou ad_id `facebook_NNN` | trendtrack_pull | HR2 pipeline TrendTrack |
| URL `facebook.com/ads/library/?id=...` | trendtrack_pull | lookup ad_id, puis HR2 |
| URL externe (instagram.com, linkedin.com, reddit.com, tiktok.com, etc.) | manual_drop | WebFetch + screenshot fallback |
| Path local `/Users/.../*.{jpg,png,mp4}` | manual_drop | Read direct |
| Image droppée dans le chat | manual_drop | Read direct |

**Copy texte fourni en parallèle** (l'opérateur colle hook + body + CTA verbatim) → toujours prendre comme source de vérité, override toute lecture OCR du visuel.

**Source vs craft.** `tags.source` détermine le BRAS de persist, le namespace et le schéma cible (HR8). Benchmark concurrent → `external_benchmark` ou `trendtrack_pull` → **BRAS REVERSE**, namespace RCV, `decomposition.json`. Créa produite par la marque opérée → `internal_production` → **BRAS INTERNE**, namespace CRT, split genome/creative/sidecar/brief. Drop manuel d'une ad inconnue → `manual_drop` → BRAS REVERSE par défaut (RCV), car une ad inconnue n'est pas notre canonical.

---

## HR1bis · Triage d'éligibilité (batch / corpus-seeding)

Quand le skill tourne en BATCH (seeding du corpus de référence · N ads scrapées d'un coup), tout fichier n'est PAS forcément une ad décortiquable. AVANT le mkdir-claim + la décompo, juger :

| Cas | Verdict |
|---|---|
| Ad concept / mécanique / UGC-testimonial / avant-après / stat-claim / **photo produit stylisée** (flatlay, packshot-en-scène, lifestyle AVEC le produit) | **ENCODER** |
| Promo/offre pure (remise %, "cadeaux offerts", code, bundle comme message entier) | ENCODER · `ad_type: promo` + flag LOW-SEED-VALUE (curer comme exemple d'offre, pas concept) |
| Carte isolée de carrousel (1 slide d'un set · phrase coupée · "1/4" · dépend des voisines) | SKIP `fragment` |
| Non-ad : thumbnail dégradé (<200px), logo/avatar seul, portrait/lifestyle SANS produit ni copy, packaging brut sans aucun message | SKIP `non-ad` |

**Règle anti-faux-skip (signal batch naali · RCV-26/29/50)** : une **photo produit stylisée où la seule copy est sur l'emballage EST une ad** (format DTC standard), PAS un "non-ad". Ne skipper que les vrais déchets (thumbnail, logo, portrait sans produit). En cas de doute → **ENCODER** : un faux-encodage est récupérable en curation, un faux-skip perd une ad silencieusement. Un SKIP ne crée jamais de dossier `{RCV-NN}/`.

---

## HR2 · Fetch + download (TrendTrack mode uniquement)

Skip si mode `manual_drop`.

1. `GET /v1/ads/{adId}` → details (content body, format, days_running, reach, spend, country). Cache headers : ETag respecté.
2. `GET /v1/ads/{adId}/media-url` → URL CDN signée.
3. Download local : `/tmp/decompose/{adId}.{jpg|mp4}` (staging éphémère). Cache : si fichier déjà présent et taille match, skip download. **Ce `/tmp` n'est PAS l'artefact final.** Pour le BRAS INTERNE, le binaire final est déplacé vers `creatives/{batch}/{CRT-NN}/produced/{slug}.{jpg|mp4}` AVEC sidecar (HR8). Pour le BRAS REVERSE, si on conserve une image de réf, elle va sous `competitive-intel/{batch}/{RCV-NN}/produced/{slug}.jpg` AVEC sidecar ; sinon le `/tmp` reste une simple référence externe non stockée (la décompo benchmark = `decomposition.json` seul, l'image de réf est optionnelle).
4. Si format `video` : extraire frame clé via `ffmpeg -ss 00:00:01 -i {file} -frames:v 1 {file}.jpg` (Step 1 frame). Si hook texte n'est visible qu'après plusieurs secondes, scan toutes les 2s jusqu'à frame avec densité texte la plus haute.
5. Credentials : lire `TRENDTRACK_API_KEY` depuis `credentials_shared.env` (ou `brands/{slug}/credentials.env` si surcharge). Absent → surface honnête à l'opérateur, propose mode `manual_drop` à la place.

---

## HR2bis · Lookup product visual identity (avant gen)

Si `mode == "internal_production"` ou `mode == "compose"` (skill `compose-creative` futur), ET si `target_brand` + `target_product_slug` connus :

1. Read `brands/{target_brand}/products/{target_product_slug}/spec.json#visual_identity`.
2. Si bloc présent et `packshots.primary_front` non-null :
   - Use `packshots.primary_front` comme `image_urls[0]` dans payload `nano-banana-2/edit` (canon v2.46, au lieu d'un screenshot d'ad bruité).
   - Inject `distinctive_features[]` dans le prompt en hard constraints (`MUST PRESERVE: ...`).
   - Inject `color_palette` hex codes dans le prompt (`exact colors: container_primary #..., label_background #...`).
   - Inject `label.wordmark_text` + `label.wordmark_typography_hint` (`label MUST read exactly "{wordmark_text}", never variants`).
   - Inject `content` (form, color, shape, quantity_visible).
3. Si bloc absent :
   - Surface warning à l'opérateur : "spec.json#visual_identity manquant. Render fidelity dégradée. Run skill `populate-visual-identity` (futur) ou drop ad screenshot manuel comme reference".
   - Continue avec ad screenshot bruité comme fallback.

Rationale : sans packshot clean en input, le model image gen hallucine le label sous 2 iter (cf. audit S55 régression wordmark with brackets sur endpoint legacy nano-banana-pro). Avec packshot + `distinctive_features` injecté + endpoint canon nano-banana-2 (Gemini 3 Pro Image text fidelity natif), fidélité label peut atteindre 95%+.

---

## HR3 · Lire image + copy

1. Read tool sur le path local (image ou frame extraite).
2. Lire le copy verbatim fourni par l'opérateur (hook texte, body, CTA, primary text).
3. Si copy non fourni et OCR nécessaire, lire le visuel et extraire texte visible. Tagger ces extractions avec confiance basse internement (jamais surfacer le tag à l'opérateur).
4. **NEVER halluciner.** Si un slot n'est pas visible ou pas fourni (ex : pas de body texte sur une ad pure visuelle), écrire `-`. Modalité de la vérité non-dite peut être `formulee | implicite | absente`.

---

## HR4 · Decompose Section 1 · CE QUE L'AD MONTRE (observable, ground truth)

Aucune interprétation. Description objective, vocabulaire neutre.

| Champ | Contenu |
|---|---|
| Format | `static_image | carousel | video_short | video_long | reel | story | gif` |
| Hook visuel | Description objective de la première composition vue (ex : "split-screen avant/après corps féminin, fond crème, surimpression chiffre 12kg") |
| Hook texte | Verbatim. `-` si absent. |
| Body texte | Verbatim. `-` si absent. |
| CTA texte | Verbatim button label + texte autour. `-` si absent. |
| Branding visible | Logo position, packshot oui/non, couleur dominante, font dominant signal |
| Performance | TrendTrack data si dispo (days_running, reach estimé, spend estimé, score perf). `-` sinon. |

---

## HR5 · Decompose Section 2 · CE QUE L'AD RACONTE (interprété, équation v3.1)

Couche interprétation. Chaque inférence est ancrée dans observables Section 1.

**Cible.** Persona déduite. Si la marque opérée est l'auteur de l'ad et `audience_slug` connue, lookup `brands/{slug}/audiences/{audience}/profile.json` pour `buyer_user_split` + `persona_archetype`. Sinon inférer depuis observables (visuel persona, langage, références culturelles). Tag interne `observe / deduit / declare` jamais surfacé. Affichage opérateur : phrase plain language ("femme 30-45, post-partum, frustration retour silhouette pré-grossesse") ou `-` si pas inférable.

**Niveau conscience.** Schwartz 5 stages, source `resources/schemas/_shared/awareness-stage.json`. `unaware | problem_aware | solution_aware | product_aware | most_aware`. Affichage opérateur : phrase ("solution aware, sait que la slimming wear existe, compare les marques"). Encodage : mirror enum reverse `awareness_level_schwartz` (`unaware | problem-aware | solution-aware | product-aware | most-aware`) côté `decomposition.json` (benchmark) ou `genome.json#genome_tags.awareness_level` (interne).

**Vérité non-dite.** Insight modalité `formulee | implicite | absente`. La vérité non-dite est l'insight psychologique sous l'angle (ex : "elle a honte de remettre son ancien jean et personne le sait"). Modalité formulée = l'ad le dit explicitement. Implicite = l'ad le sous-entend. Absente = l'ad ne touche pas l'insight, opère sur surface produit. Affichage opérateur : citation entre guillemets + modalité en parenthèse, ou `-` si absente.

**Angle d'attaque.** Triplet `levier × positionnement-contre × promesse`. Levier = quel ressort psychologique mobilisé (peur, désir, statut, appartenance, contrôle). Positionnement = contre quoi l'ad se positionne (statu quo, concurrent type, croyance limitante). Promesse = transformation visée. Affichage opérateur : phrase compacte ("vanité féminine post-partum × contre solutions long-terme lentes × silhouette retrouvée en 30 jours").

**Mécanique AD-LEVEL (le CONCEPT).** Référence `resources/registries/creative-mechanics-registry.md` (free-string `mecanique_id` ; `other` + `mecanique_proposal` si rien ne fitte). Persiste dans **`decomposition.mecanique`** : `mecanique_id` + `mecanique_name` + `axis` (claim/visual) + `typology_st` (spatial=image / temporel=vidéo) + `confidence`. **Tag PRINCIPAL d'un statique.** DISTINCT du hook (`script.hook.mechanic_id`, niveau accroche, surtout vidéo · voir SSOT mécaniques HR ci-dessus). Affichage opérateur : nom registry + 1 phrase. Pont A=B : `genome.json#genome_tags.mecanique_id` (concept) ET `#genome_tags.mechanic_id` (hook).

**Pivot du message.** L'atome compositionnel est le `frame` (le couple `copy_script` + `visual_script`, MECE, vérifiable A=B) ; le pivot, c'est le frame dont on ne peut rien retirer sans casser la créa. Test "delta perf si retiré" : si on enlève cet élément, la créa perd >50% de son hook. Souvent un mot clé, un visuel signature, une stat chiffrée, un avant/après. Affichage opérateur : citation entre guillemets + 1 phrase de justification.

**Canonical link pain + objection (v1.5.0 · v2.64 ontologie sémantique pure).** Si l'ad reverse-engineered mentionne un pain ou une objection détectée, evaluate cross-applicable signal ·

- **Mode `internal_production` ET audience match brand opérée** · si pain/objection observé matche sémantiquement un PNT-NN ou OBJ-NN dans `audiences/{audience_slug}/pain_points/*.json` OR `audiences/{audience_slug}/objections/*.json` sub-audience, link canonical · stage dans le BRAS INTERNE `creative.json#context.pain_point.summary` + ref (cf HR8 split) dans persist. Surface opérateur en fiche · *"Pain mobilisé · PNT-03 (ras-le-bol des régimes, déjà cartographié dans ton atlas)"*.
- **Mode `external_benchmark` ou `trendtrack_pull` (ad concurrente)** · l'ad concurrente n'est pas notre canonical, observation pure. Note descriptive sans canonical ref · stage dans le BRAS REVERSE `decomposition.json#atlas_consumed.pain_points_referenced[]` avec `atlas_link_status: "unlinked"` + `pain_text_observed: "{verbatim observé}"`. Surface opérateur · *"Pain mobilisé observé · 'frustration accumulée régimes' (pas dans ton atlas, signal concurrent)"*.
- **Backward compat (v2.63 brands)** · si sub-audience pain_points/objections vides, fallback top-level `pain_points/*.json` + `objections/*.json` filtered by affected_audiences[].
- **Backward compat (pre-v2.63 brands)** · si top-level vide aussi, fallback observation pure (mode external_benchmark behavior par défaut). Pas de mutation cross-graph forcée.

Cohérent règle d'isolation `brand_only` doctrine · le reverse-engineering d'une ad externe ne pollue jamais le canon brand · seul un internal_production avec audience match peut enrichir le graph.

---

## HR5bis · Inject visual_identity in prompt (compose / regen phase)

S'applique en aval (skill `compose-creative` futur, ou regen phase d'un skill orchestrateur consommant decompose-ad output). Si `visual_identity` chargé via HR2bis, format prompt augmentation :

```
Use the EXACT product shown in the reference image. CRITICAL VISUAL FIDELITY:
- Container: {container.shape} {container.material} {container.cap_type}, {container.transparency}
- Content: {content.quantity_visible} {content.form} color {content.color_hex} {content.shape}
- Label: MUST read exactly '{label.wordmark_text}'. Sub-label: '{label.sub_label}'. Duration: '{label.duration_indicator}'.
- Color palette: container {color_palette.container_primary}, label background {color_palette.label_background}, label text {color_palette.label_text}.
- DISTINCTIVE FEATURES (do not modify):
  - {distinctive_features[0]}
  - {distinctive_features[1]}
  - ...
```

QC post-gen : valider chaque `distinctive_features[]` présent dans le render. Échec sur 1+ feature → flag à l'opérateur + propose re-gen avec prompt renforcé. Si un binaire est produit ici (regen phase), il est tracé par son sidecar `produced/{slug}.json` (HR8 · anti-orphelin), jamais écrit standalone.

---

## HR5ter · Champs encodés sur persist (alignés sur le bras + schéma cible)

Quand le skill persiste, écrire les champs selon le BRAS et le schéma cible · PAS un seul `creative.json` monolithique legacy.

**BRAS REVERSE (benchmark · `decomposition.json` · decomposition/1.0)** · le reverse natif porte ses propres champs (pas de mapping forcé vers creative.schema) :

- `identification` : `video_id` (= ad_id externe si connu, sinon filename), `brand_slug`, `support` (REQUIS · `video`/`static`/`carousel-card`/`carousel-set`/`gif-animated`), `source_platform`, `video_meta` (`aspect_ratio` requis ; `duration_s` omis si statique). **Statique** : omettre `audio`+`edit`, `body_arc[]` sans timestamps (ordre via `beat_id`).
- `mecanique` (AD-LEVEL · le CONCEPT · D#488) : `mecanique_id` (→ `creative-mechanics-registry`, free-string), `axis` (claim/visual), `typology_st` (**spatial**=image / **temporel**=vidéo), `confidence`. **Tag ROI du statique.** `other` + `proposal_flag` si rien ne fitte.
- `script.hook` (HOOK-LEVEL · l'accroche · surtout VIDÉO) : `mechanic_id` (→ hook-mechanics-registry = `registries/hooks/`), `hook_text_first_15_words`. **Sur un statique sans accroche texte, ne pas forcer → `other-uncategorized`.** `script.body_arc[]` : suite de beats `beat_type` (snapshot enum HR8bis). `script.cta`.
- `visual.styles_observed[]` : `style_id` (snapshot enum HR8bis). `visual.character_pattern.character_archetype`.
- `atlas_consumed` : pain_points_referenced / mechanisms_invoked / proof_elements_used / offer_elements_visible avec `atlas_link_status` (`linked | unlinked | new-to-atlas`). Benchmark concurrent = `unlinked` par défaut (observation pure, jamais mutation cross-graph).
  > **Placement preuve vs offre (signal naali · `proof_type: other` à 26%)** : `proof_elements_used` = UNIQUEMENT de la vraie preuve (testimonial / authority / timeline / stat / before-after / guarantee). Une **offre** (GWP, remise, valeur barrée, cadeau) va dans `offer_elements_visible`, JAMAIS dans proof. Une benefit-stack ou une concept-card graphique n'est ni preuve ni offre → ne pas la forcer en `proof_type: other`. **Aucune vraie preuve → laisser `proof_elements_used` vide** (tableau vide correct ; "other" de remplissage = bruit d'agrégation cross-brand).
- `audience_targeting_inferred.awareness_level_schwartz` + `funnel_stage_inferred` + `confidence`.
- `perf_signals_external` si TrendTrack/Meta Ad Library dispo (days_active, reach, spend ranges).
- `analysis_meta` : `analysis_method`, `confidence_overall`, `frames_analyzed_*`.

**BRAS INTERNE (créa nôtre · split genome/creative · genome/1.2 + creative/1.3)** · le NOYAU va dans `genome.json`, le lignage dans `creative.json` :

- `genome.json` (ADN) : `script_id` (GSC-NN), `support` (static/carousel/video), `route` (`route_a_full_ia` par défaut reverse-of-internal), `hook` (mechanic_id + hook_text), `frames[]` (role beat_type + copy_script + visual_script), `genome_tags` (support + mechanic_id + primary_style_id requis ; **mecanique_id** [le CONCEPT ad-level → `creative-mechanics-registry` · DISTINCT du mechanic_id HOOK · pont A=B sur l'axe concept · D#491] + **angle_id** [l'ANGLE ANG-NN · unité stratégique de 1ère classe · porte objection+OTRB+payoff · D#492] + audience_slug + beat_type_sequence + awareness_level recommandés). MÊMES enums beat_type/style_id/mechanic_id que `decomposition.schema` = pont A=B garanti.
- `creative.json` (lignage) : `creative_id` (CRT-NN, réservé mkdir-claim), `mode`, `audience_slug`, `intent_mix` (object `{primary, secondary?, weights?}` ; skip `weights` si pure ; encoder explicitement si mix, somme à 1.0 ± 0.05 ; legacy `intent` mirror), `execution.overlay_density` (0.0-1.0) + `execution.brand_mark_present` (bool ; legacy `craft_mode` mirror dérivé), `context.pain_point` / `context.proof` (CONTEXTE), `lineage{}` (5 refs), `meta.validation_status` composite `{status, confidence, confidence_source}` (pour décompo d'une créa déjà testée, dériver confidence depuis test_results ; sinon `{status:"hypothesis", confidence:0.5, confidence_source:"default"}`), `performance`, `tags.source: "internal_production"`.

**Lecture (input side) :**

- Si `intent_mix` absent sur un fichier existant → fallback `intent` (Hybrid → `{primary: DR, secondary: [Brand], weights: {DR: 0.5, Brand: 0.5}}`).
- Si `overlay_density` absent → fallback `craft_mode` (product_only → 0.0, minimal_brand_mark → 0.2, with_overlay → 0.6).
- Si `validation_status` est string (legacy) → l'accepter via oneOf, traiter comme `{status: <string>}`.

**Backward compat strict :** ne jamais supprimer les anciens champs en écriture, ne pas casser les fichiers existants.

---

## HR6 · Decompose Section 3 · DIAGNOSTIC

**Cohérence chaîne descendante.** Audience → insight → angle → mécanique → craft. Chaque transition : `tient | tension | casse`. Affichage opérateur : verdict global ("✓ tient sur les 4 transitions" ou "⚠ tension entre angle et mécanique : l'angle promet rapidité, la mécanique installe long-terme").

**Score arrêt scroll.** Echelle 1-5. Subjectif mais ancré sur observables Section 1. Critères : densité visuelle première frame, contraste avec feed natif, rupture de pattern, charge cognitive immédiate, signature ton. Pas de moyenne pondérée surfacée, juste le verdict numérique + 1 phrase justification.

**Forces.** 3-5 bullets observables. Pas d'éloge vague ("bon hook"), nommer le mécanisme ("hook visuel split-screen avant/après en frame 1, rupture pattern feed natif, lecture du verdict en <1s").

**Risques.** 3-5 bullets. Légal (claims santé sans disclaimer, comparatif déloyal), brand (déconnexion ton vs identité, casting hors persona), audience (insight implicite mais audience trop chaud pour le décoder), execution (CTA mou, body trop chargé, branding noyé).

---

## HR7 · Decompose Section 4 · ANATOMIE 3 NIVEAUX + TAGS (v2.0.0)

**Refactor v2.0.0.** L'ancienne section RÉUTILISATION (Amélioration / Transposable sur / Concept-mère) v1.5.0 est remplacée par la grille ANATOMIE 3 NIVEAUX cohérente avec l'équation canonique v3.1 (NOYAU × CONTEXTE × MODIFIEURS). Output opérateur-facing 100% humain, IDs canoniques persistés silent back-end via HR8.

**Grille canonique 3 niveaux.**

- **CE QUI FAIT PERFORMER (à garder · 5 éléments humains).** Composants du NOYAU créa, invariants. Modifier casse la performance. 5 lignes ·
  - La mécanique narrative (label humain registry mecanique, pas ID exposé)
  - Le format (label humain enum format, pas raw value)
  - La phrase d'accroche (label humain stop_scroller, pas field name)
  - L'élément pivotal (label humain · le frame pivot `copy_script`+`visual_script`, pas field name)
  - L'équilibre copy/visuel (label humain copy_visual_cursor, pas field name)
- **À ADAPTER À TA BRAND (5 refs humaines · IDs canoniques silent).** Composants du CONTEXTE branchable. Adapter rend la créa tienne sans casser le NOYAU. 5 lignes ·
  - L'audience visée (selon ta cartographie, ref `audience_segment` silent)
  - La douleur précise adressée (depuis ton territoire, ref pain silent)
  - Le verbatim de preuve (depuis tes reviews clients, ref `context.proof` silent)
  - Le mécanisme produit cité (selon ta composition, ref mechanism silent)
  - Le CTA et la garantie (selon ton offre, ref offer silent)
- **À SITUER (5 modifieurs situationnels).** Composants MODIFIEURS. Plusieurs choix possibles selon campagne cible. 5 lignes ·
  - Le canal de diffusion (Meta, TikTok, YouTube · `modifiers.canal`)
  - La saisonnalité (hiver, été, back-to-school · `modifiers.seasonality`)
  - Le ton (chaleureux, direct, neutre · `modifiers.ton`)
  - La destination (page produit, landing dédiée · `modifiers.destination`)
  - L'offre attachée (standalone, bundle volume · `modifiers.offer`)

**Concept-mère.** Générer `concept_id` pattern `cpt_{brand_slug}_{angle_short}_{NNN}` (persisted silent HR8 ; BRAS INTERNE → `creative.json#concept_id` + `genome.json#lineage.concept_id` ; BRAS REVERSE → pas de concept_id brand-side, c'est une ad concurrente, le groupage reste descriptif côté `decomposition.json`). Si l'ad est une variante d'un concept déjà encodé (interne uniquement), lien `variant_of` + `variant_axis` (`photo_swap | promo_toggle | hook_swap | background_swap | persona_split | null` · enum canonique creative.schema) persisted silent dans `creative.json`. Pas surfacé en fiche opérateur-facing v5 (back-end uniquement).

**Bloc TAGS retrieval.** Tous les axes du schema, snake_case strict. La ligne `id` porte `CRT-NN` pour une créa interne, `RCV-NN` pour une ad concurrente (jamais l'inverse) :

```
brand              {brand_slug}
niche              {niche string}
audience           {audience_slug ou phrase}
mode               concept | template | asset
mecanique          {mecanique_id du registry · snapshot enum mechanic_id pour le pont A=B}
intent             DR | Brand | Hybrid | Lead_gen | Retention | Awareness
audience_segment   B2C | B2B | B2B2C | DTC | marketplace
craft_mode         product_only | minimal_brand_mark | with_overlay
format             {format string}
trigger            {seasonality_trigger ou null}
geographie         {country code ou région}
performance        {days_running / spend bucket / null}
annee              {YYYY}
concept_id         {cpt_brand_angle_NNN · interne uniquement, null pour benchmark}
variant_of         {CRT-NN/RCV-NN parent ou null}
id                 {CRT-NN (interne) | RCV-NN (benchmark)}
source             internal_production | external_benchmark | trendtrack_pull | manual_drop
```

---

## HR8 · Persist (dual-bras · RCV reverse vs CRT interne)

> Le mkdir-claim atomique (réservation du `{RCV-NN}/` ou `{CRT-NN}/`) est exécuté en **STEP 0 de HR-DA-CANON-1** (section ci-dessous), AVANT cette persist. HR8 écrit dans le dossier déjà réservé.

1. **Determine le bras + le namespace + le schéma cible** depuis `tags.source` :
   - `external_benchmark`, `trendtrack_pull`, OU `manual_drop` sur ad inconnue → **BRAS REVERSE** · namespace **RCV** · cible `brands/{slug}/competitive-intel/{batch}/{RCV-NN}/decomposition.json` · schéma `decomposition.schema.json` (`decomposition/1.2`). Image de réf éventuelle → `{RCV-NN}/produced/{slug}.jpg` (binaire direct) + sidecar `{RCV-NN}/produced/{slug}.json`.
   - `internal_production` (la marque opérée est l'auteur déclaré de l'ad) → **BRAS INTERNE** · namespace **CRT** · cible `brands/{slug}/creatives/{batch}/{CRT-NN}/` · split `genome.json` (`genome/1.2`) + `creative.json` (`creative/1.3`) + sidecar `produced/{slug}.json` (`produced-asset/1.0`) + `brief.md`.
2. **Id réservé par mkdir-claim STEP 0** (HR-DA-CANON-1). PAS de scan-max+1 sur un dossier plat (l'ancien allocateur était non-atomique et écrivait au mauvais endroit). RCV scanné cross-batch SÉPARÉMENT de CRT (les deux namespaces ne se croisent jamais).
3. **Write via `write_to_context(field_path, value, source, confidence, mode="proposed")`** pour CHAQUE `.json` :
   - BRAS REVERSE · `decomposition.json` (conforme `decomposition.schema.json` **`decomposition/1.2`**) · porte `meta.schema_version: "1.2.0"` ET `identification.support` (REQUIS · `video`/`static`/`carousel-card`/`carousel-set`/`gif-animated`). **NE PAS écrire de champ top-level `_schema_version`** : ce schéma est `additionalProperties:false` et le rejette (même règle que `genome.json` · seul `creative.json` porte un `_schema_version` top-level). **Support statique** : `identification.support: "static"`, omettre `audio` + `edit`, `video_meta.duration_s` omis, `body_arc[]` SANS `start_s`/`end_s` (ordre encodé par `beat_id`). + le cas échéant le sidecar `produced/{slug}.json`.
   - BRAS INTERNE · `genome.json` (`genome/1.2` · `additionalProperties:false` · ne porte JAMAIS de `_schema_version` top-level) + `creative.json` (`_schema_version: "creative/1.3"`, `_equation_ref` const v3.1 · seul fichier du split à porter la version top-level) + sidecar `produced/{slug}.json`.
4. **Binaires (.jpg/.mp4) écrits DIRECT** sous `produced/` (`write_to_context` ne gère que le `.json`). Tout binaire DOIT avoir son sidecar `.json` gated (anti BUG-ASSET-ORPHAN). `brief.md` (bras interne uniquement) écrit DIRECT via Write (`.md` exempt de `ALLOWED_PATH_PATTERNS` et de mutation-guard). Double régime non-négociable.
5. **NEVER edit JSON directly via Edit/Write/NotebookEdit** sur les `.json` sous `brands/`. Mutation gate non-optionnel.
6. Si `mecanique_id == "other"` → emit event `mecanique_proposal_flag` avec payload `{observed_mecanique_signature, ad_creative_id, registry_gap_description}` pour graduation future du registry. **Ne PAS muter le registre ici** (graduation = checkpoint opérateur, hors scope D).
7. Trigger `validate-resources` silencieusement après write. **Note** · `validate-resources` ne valide que `resources/`, jamais `brands/` (cf genome.schema description). Le contrôle de forme runtime sous `brands/` est le gate `write-to-context.py` (ALLOWED_PATH_PATTERNS · path-only, accepte `decomposition.json` à `competitive-intel/{batch}/{RCV-NN}/` et le split CRT). Flag MAJOR/CRITICAL à l'opérateur si remonte.

---

## HR8bis · Snapshot enum projeté (mirror enums · pont A=B)

Les tags qui servent le pont A=B · `beat_type`, `style_id`, `mechanic_id` · sont émis via un **SNAPSHOT enum versionné projeté** du registre, PAS lus en free-string brut ni hardcodés dans le skill.

1. **SSOT = registre free-string** `resources/registries/creative-mechanics-registry.md`. Évolutif. **NE JAMAIS** l'enum-locker, **NE JAMAIS** écrire dedans depuis ce skill.
2. **Snapshot = projection figée** des enums au moment de la persist. Source canon de la projection : les enums natifs du reverse, identiques côté `decomposition.schema.json` ET `genome.schema.json` (beat_type 20 termes, style_id, mechanic_id 25 termes). C'est cette identité d'enum qui rend A=B opérant : la perf future se rattache au même espace.
3. **Émission** : projeter le `mecanique_id` observé (HR5) sur la valeur de snapshot la plus proche. Si aucune ne fitte → valeur `other-uncategorized` (mechanic) / `other` (style/beat) + flag `mecanique_proposal` (HR8.6). Le snapshot grandit par graduation registre future, jamais par écriture inline.
4. **Mode** : `proposed`, `brand_only`. Une promotion cross-brand (faire entrer une nouvelle mécanique observée dans le registre SSOT partagé) est un **checkpoint opérateur, hors scope de ce skill**. decompose-ad propose, n'entérine pas.

Rationale : le registre reste vivant (le snapshot ne le fige pas), mais la décompo émet des valeurs stables et comparables à la perf. Découplage strict registre-SSOT-évolutif ↔ snapshot-enum-figé-pour-jointure.

---

## HR9 · Output operator-facing

Render fiche markdown selon format S55 fiche v5 (template ci-dessous). Vocabulaire opérateur uniquement, pas plumbing. Pas `intent: DR`, dire `Type de campagne : direct response info-produit`. Pas `craft_mode: product_only`, dire `Cadrage : produit seul, pas de surimpression marque`. Jamais surfacer `decomposition.json`, `RCV-NN`, `CRT-NN`, `genome.json` en clair (sauf dans le bloc TAGS retrieval, mode reverse-engineering assumé · l'opérateur peut vouloir voir comment c'est encodé).

**No orphan output.** Terminer sur 1 reco actionnable, pas de menu (a)/(b)/(c). Reco ancrée sur ce qui vient d'être décomposé : transposer concept sur autre brand active, lancer `produce-paid-angles` sur l'audience matchée pour générer 5 variantes du NOYAU, ou flag mecanique_proposal pour enrichir le registry. Une reco forte, pas trois équivalentes.

### Fiche v5 template (canonique v2.51)

Réf canonique · `resources/templates/operator-fiche-output.md`. Header plain language `Analyse pub · {source_humaine}` (canonique mapping table). Source humaine = `concurrent` pour benchmark, `interne n°{N}` pour créa marque opérée.

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Analyse pub · {source_humaine}
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD} · décomposition de la pub {concurrent | interne n°N} · {langue} · {annee}

───────────────────────────────────────────────────────────────
1 · Ce que l'ad montre (observable, ground truth)
───────────────────────────────────────────────────────────────
Format             {format}
Hook visuel        {description objective}
Hook texte         "{verbatim ou -}"
Body texte         "{verbatim ou -}"
CTA texte          "{verbatim ou -}"
Branding visible   {logo, packshot, couleur, font}
Performance        {trendtrack data ou -}

───────────────────────────────────────────────────────────────
2 · Ce que l'ad raconte (interprété, équation v3.1)
───────────────────────────────────────────────────────────────
Cible              {persona phrase ou -}
Niveau conscience  {schwartz stage phrase}
Vérité non-dite    "{insight}" ({modalité}) ou -
Angle d'attaque    {levier · contre quoi · promesse}
Mécanique          {nom registry} · {1 phrase}
Pivot du message   "{atome}" · {1 phrase justif}

───────────────────────────────────────────────────────────────
3 · Diagnostic
───────────────────────────────────────────────────────────────
Cohérence chaîne   {verdict + 1 phrase}
Score arrêt scroll {N} / 5 · {1 phrase}
Forces             · {bullet}
                   · {bullet}
                   · {bullet}
Risques            · {bullet}
                   · {bullet}
                   · {bullet}

───────────────────────────────────────────────────────────────
4 · ANATOMIE · 3 NIVEAUX (canonique v2.0.0)
───────────────────────────────────────────────────────────────

CE QUI MARCHE · 5 SECONDES DE LECTURE

  Format de la pub        · {format humain · ex vidéo testimonial 15s}
  Phrase d'accroche       · {hook humain · ex "5h du matin"}
  Mécanique narrative     · {label registry humain · ex confession première
                            personne, validation de la souffrance}
  Élément pivotal         · {atome humain · ex "j'avais tout essayé jusqu'à..."}
  Preuve                  · {proof humain · ex témoignage transformation 2 sem}
  Angle de communication  · {angle humain · ex efficacité, soulagement rapide}
  Intention dominante     · {intent humain · ex vente directe (80%), branding
                            léger (20%)}
  Équilibre copy/visuel   · {cursor humain · ex copy-dominant, visuel pédago}
  Audience visée          · {audience humaine phrase · ex personnes debout
                            10h+ par jour + douleurs chroniques (croisement)}

  ✦ Ce qui fait la performance · la combinaison [mécanique humaine] +
    [angle humain] + [proof humain] sur ce profil composite. Pattern
    observable chez N brands [secteur] récentes.

ANATOMIE · 3 NIVEAUX

  ┌─ CE QUI FAIT PERFORMER · à garder ───────────────────────────────┐
  │                                                                  │
  │  La mécanique narrative ({label humain · pas registry ID})       │
  │  Le format ({label humain · pas raw enum})                       │
  │  La phrase d'accroche ({label humain · pas stop_scroller field}) │
  │  L'élément pivotal ({label humain · pas le frame pivot brut})    │
  │  L'équilibre copy/visuel ({label humain · pas copy_visual_cursor})│
  │                                                                  │
  │  Modifier ces 5 éléments casse la créa.                          │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ À ADAPTER À TA BRAND ───────────────────────────────────────────┐
  │                                                                  │
  │  L'audience visée (selon ta cartographie)                        │
  │  La douleur précise adressée (depuis ton territoire)             │
  │  Le verbatim de preuve (depuis tes reviews clients)              │
  │  Le mécanisme produit cité (selon ta composition)                │
  │  Le CTA et la garantie (selon ton offre)                         │
  │                                                                  │
  │  Adapter ces 5 éléments rend la créa tienne.                     │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ À SITUER · selon le contexte de campagne ───────────────────────┐
  │                                                                  │
  │  Le canal de diffusion (Meta, TikTok, YouTube)                   │
  │  La saisonnalité (hiver, été, back-to-school)                    │
  │  Le ton (chaleureux, direct, neutre)                             │
  │  La destination (page produit, landing dédiée)                   │
  │  L'offre attachée (standalone, bundle volume)                    │
  │                                                                  │
  │  Plusieurs choix possibles selon la campagne cible.              │
  └──────────────────────────────────────────────────────────────────┘

CE QU'ELLE PROUVE DANS LE PAYSAGE {SECTEUR}

  Cette combinaison ({mécanique + angle + proof humains}) scale chez
  N brands {secteur} observées récemment. Le système peut l'enregistrer
  comme pattern réutilisable après une validation ROI sur ta propre brand.

───────────────────────────────────────────────────────────────
5 · FIT AVEC TA BRAND · scoring + reco (canonique v2.1.0)
───────────────────────────────────────────────────────────────

  Le système évalue si cette créa concurrente vaut la peine d'être
  adaptée à ta brand avant de te proposer le flow d'adaptation.

SCORING SUR 5 DIMENSIONS

  Audience match           · {score 0-10} · {diagnostic 1 ligne}
  Produit match            · {score 0-10} · {diagnostic 1 ligne}
  Ton de marque match      · {score 0-10} · {diagnostic 1 ligne}
  Stage de scale match     · {score 0-10} · {diagnostic 1 ligne}
  Leviers psychologiques   · {score 0-10} · {diagnostic 1 ligne}

  Score global de fit · {score moyenne pondérée / 10}

DIAGNOSTIC DÉTAILLÉ

  Audience match
    {analyse · concurrent vise audience X observée · ta cartographie
     contient AUD-NN matching score Y · gap si applicable}

  Produit match
    {analyse · concurrent met en avant mécanisme produit X · ta spec
     contient mécanisme matching Y · gap si applicable}

  Ton de marque match
    {analyse · concurrent registre de ton X · ton brand voice registre
     Y · cohérent OU dissonant si applicable}

  Stage de scale match
    {analyse · concurrent stage observé X (early/scale/mature) · ton
     brand stage Y · cohérence campagne}

  Leviers psychologiques fit
    {analyse · leviers utilisés par concurrent (urgence, peur, validation,
     authority, social proof, etc.) · cohérence avec brand_equity_level
     et driver_blend de ta brand}

RECO ACTIONNABLE

  ✦ {Reco selon scoring global ·
     · 8-10 · "Adapt full" · variant complet brief copy + visuels Meta-ready
     · 5-7  · "Adapt 1 axe seul" · isoler 1 dimension qui matche fort
     · 0-4  · "Skip ce concept" · pas de fit suffisant · gaspillage d'adapt}

  {Justification 2-3 lignes en langage humain accessible}

───────────────────────────────────────────────────────────────
Tags retrieval
───────────────────────────────────────────────────────────────
{bloc tags 17 lignes snake_case · ligne id = RCV-NN pour concurrent, CRT-NN pour interne}

───────────────────────────────────────────────────────────────
→ {Selon score global de fit} ·
  · 8-10 · "Bon fit · adapt full recommandé"            /adapt-from-competitor {RCV-NN}
  · 5-7  · "Fit partiel · adapt 1 axe recommandé"       /adapt-from-competitor {RCV-NN} --axis={dim_top_score}
  · 0-4  · "Faible fit · skip recommandé · adapt risqué" (pas de skip command · l'opérateur peut quand même invoquer /adapt-from-competitor {RCV-NN} s'il veut override)
```

> Le close pointe sur `{RCV-NN}` (l'ad décortiquée vit dans le namespace RCV). `adapt-from-competitor` lit le `decomposition.json` à `competitive-intel/{batch}/{RCV-NN}/` et produit une créa CRT brand-side avec `variant_of: "RCV-NN"` (lignage cross-namespace). Une créa interne décortiquée (CRT) n'a pas de close adapt (elle est déjà nôtre).

---

## HR-DA-CANON-1 · Entry canonical batch + mkdir-claim dual-namespace (Brique 4 étape D · exécutable)

> Toute décompo DOIT créer son dossier canonique AVANT tout write, dans le BON arbre selon le bras. Benchmark → `competitive-intel/{batch}/{RCV-NN}/`. Interne → `creatives/{batch}/{CRT-NN}/`. Interdit tout asset orphelin hors structure. Cross-ref `resources/conventions/creative-storage.md` (D#481). Pattern miroir compose-creative HR-CC-CANON-1.

### Refus AVANT claim

Tous les refus (TrendTrack auth absent en mode pull · ad illisible · `internal_production` déclaré mais aucune créa nôtre identifiable) s'exécutent **AVANT STEP 0c**. Un run refusé ne doit JAMAIS laisser un dossier `{RCV-NN}/` ou `{CRT-NN}/` réservé vide. La claim atomique ne se prend qu'une fois la décompo garantie persistable.

### STEP 0 · mkdir-claim atomique (AVANT tout write_to_context)

Résoudre d'abord le BRAS (HR8 step 1 · depuis `tags.source`). Le namespace, l'arbre et le candidat-id en découlent.

**STEP 0a · résoudre {batch}.** `{batch}` = run date-stampé du jour, lowercase + chiffres + tirets (regex gate `[a-z0-9-]+`). Default = `$(date +%Y-%m-%d)-NN` où NN = prochain run 2-digit du jour. Résoudre NN dans l'arbre du bras · benchmark → lister `brands/{slug}/competitive-intel/` ; interne → lister `brands/{slug}/creatives/` pour les dossiers matchant `$(date +%Y-%m-%d)-*`, prendre le max suffixe, sinon `01`. Un run PEUT réutiliser le batch de session déjà ouvert. `mkdir -p` du dossier-batch parent du BON arbre (idempotent · le dossier-batch n'est PAS la claim).

**STEP 0b · candidat id (scan max cross-batch, par namespace SÉPARÉ).** Scanner TOUT l'arbre du namespace concerné pour le max existant, PAS juste le batch courant (les id sont globalement uniques dans leur namespace, batch-indépendants). RCV et CRT scannés **SÉPARÉMENT, jamais fusionnés** ·

```
# BRAS REVERSE (benchmark) → namespace RCV
ls -d brands/{slug}/competitive-intel/*/RCV-* 2>/dev/null | grep -oE 'RCV-[0-9]{2,4}' | sort -t- -k2 -n | tail -1
# BRAS INTERNE (créa nôtre) → namespace CRT
ls -d brands/{slug}/creatives/*/CRT-* 2>/dev/null | grep -oE 'CRT-[0-9]{2,4}' | sort -t- -k2 -n | tail -1
```
→ N. Candidat = `RCV-(N+1)` ou `CRT-(N+1)`, zero-paddé à ≥2 digits.

**STEP 0c · claim atomique.** `mkdir brands/{slug}/competitive-intel/{batch}/RCV-{N+1}/` (benchmark) OU `mkdir brands/{slug}/creatives/{batch}/CRT-{N+1}/` (interne) SANS `-p` sur le segment final (le parent `{batch}/` existe déjà depuis 0a). `mkdir` sur un dossier existant échoue → **c'est le verrou** (la réservation). Sur succès · l'id est à toi, immédiatement `mkdir -p .../{RCV|CRT}-{N+1}/produced/`. Sur EEXIST · `N = N+1`, retry (boucle bornée, ex 50 essais). C'est le SEUL mécanisme de réservation · pas de fichier-index, pas de lock-file, pas d'écrivain privilégié. Les trous d'id sont inoffensifs (unicité requise, pas absence-de-trou).

> **PIÈGE (vérifié source · write-to-context.py L453 `target.parent.mkdir(parents=True, exist_ok=True)`)** · ce mkdir du gate n'est PAS une claim atomique. Si un skill saute STEP 0c et compte sur le mkdir du gate, deux runs concurrents passent tous les deux et écrivent dans le MÊME `{RCV|CRT}-NN`, clobbering silencieux. Le `mkdir` atomique (sans `exist_ok`) DOIT être fait par le skill en STEP 0c.

**STEP 0d · write dans le dossier réservé.** MAINTENANT (HR8) · `write_to_context` mode=proposed ·
- BRAS REVERSE · `decomposition.json` (+ sidecar `produced/{slug}.json` si image de réf conservée).
- BRAS INTERNE · `genome.json` + `creative.json` + sidecar `produced/{slug}.json`.
Binaires (.jpg/.mp4) déplacés DIRECT sous `.../produced/` (write_to_context ne gère que le json). `brief.md` (interne) écrit DIRECT (outil Write · `.md` exempt de `ALLOWED_PATH_PATTERNS` ET de mutation-guard).

### Lignage (BRAS INTERNE uniquement)

`creative.json#lineage` doit être populé · `angle_ref` (ANG-NN) + `audience_ref` + `product_ref` + `mechanism_ref` + `concept_ref` (miroir descriptif de `concept_id`). `variant_of` (CRT-NN/RCV-NN) si dérivé. Cross-refs many-to-many activés. Le BRAS REVERSE (benchmark) n'a pas de `creative.json` · le lignage descriptif de l'ad concurrente vit dans `decomposition.json#atlas_consumed` + `identification`.

### Interdit orphelin

JAMAIS sauver un asset JPG/PNG standalone hors structure. TOUT binaire (image de réf benchmark, render interne) vit sous `{RCV-NN}/produced/` ou `{CRT-NN}/produced/` AVEC son sidecar `produced/{slug}.json` (manifest gated). Pas de binaire sans sidecar (anti BUG-ASSET-ORPHAN). `{slug}` = `[a-z0-9_-]+` (ex `frame-01`, `ref-screenshot`, `packshot-front`) pour matcher la regex du gate.

---

## Hard Rules v2.0.0 · Anatomie fiche

### HR-anatomie-1 · Section 4 grille 3 niveaux obligatoire

Toute fiche v5 produite par decompose-ad v2.0.0+ DOIT exposer la grille
3 niveaux (CE QUI FAIT PERFORMER · À ADAPTER À TA BRAND · À SITUER).
Pas optionnelle. Pas Section RÉUTILISATION prose libre legacy v1.5.0.

### HR-anatomie-2 · Output opérateur-facing 100% humain

ZERO raw field name (mecanique · stop_scroller · frame/copy_script/visual_script ·
copy_visual_cursor · audience_segment · context.pain_point · etc.).
ZERO registry ID exposé (mecanique-registry IDs · angle-registry IDs ·
proof-registry IDs). ZERO acronyme doctrine. ZERO nom de fichier ou
namespace (decomposition.json · RCV-NN · CRT-NN · genome.json) en surface
hors bloc TAGS. Labels humains accessibles uniquement (cf operator-facing
rule canon CLAUDE.md root).

### HR-anatomie-3 · IDs canoniques back-end persisted silent

Sous le capot, le persist conforme schéma (decomposition/1.2 benchmark ·
genome/1.2 + creative/1.3 interne) porte les fields canon + snapshot enums
(mirror beat_type/style_id/mechanic_id). Cross-skill reproducibilité
garantie · adapt-from-competitor v1.0.0+ consume le decomposition.json
benchmark via back-end sans interpréter la prose opérateur-facing.

### HR-anatomie-4 · Close 1 question binaire vers adapt-from-competitor

Fin de fiche v5 v2.0.0 close strict · "→ Veux-tu l'adapter à ta brand ·
/adapt-from-competitor {RCV-NN}". Pas reco prose libre legacy. Pas 3 paths
ici (Phase 1 décomposition pure · Phase 2 adaptation séparée). Le close
surface `{RCV-NN}` (namespace de l'ad concurrente décortiquée), jamais
`{CRT-NN}`. Chain explicit downstream vers adapt-from-competitor orchestrator.

### HR-anatomie-5 · Fit-check obligatoire avant close binaire

Toute fiche v5 v2.1.0+ DOIT produire Section 5 FIT AVEC TA BRAND avec
scoring 5 dimensions + diagnostic + reco actionnable. Le close binaire
vers adapt-from-competitor est CONDITIONNEL au score global · "Bon fit"
(8-10) recommande adapt full · "Fit partiel" (5-7) recommande adapt 1 axe ·
"Faible fit" (0-4) recommande skip. L'opérateur peut override la reco mais
le système signale honnêtement le verdict fit-check pre-adapt. Évite
gaspillage d'invocation adapt-from-competitor sur créa non-fit.

Sourcing scoring 5 dimensions ·
- Audience match · matching score audience_segment concurrent vs cartographie brand AUD-NN
- Produit match · matching mécanisme produit concurrent vs spec composition + mechanisms brand
- Ton de marque match · cohérence tone_of_voice concurrent vs brand.tone_of_voice.register
- Stage de scale match · cohérence stage observé concurrent vs brand.strategic_context.stage
- Leviers psychologiques fit · cohérence leviers (urgence/peur/validation/authority/social/scarcity) vs brand_equity_level + driver_blend.primary

Output opérateur-facing 100% humain (HR-anatomie-2 preserved) · zero raw
field name · zero registry ID exposé · scoring exposé en humain (0-10
échelle accessible · pas confidence numerical raw).

---

## Anti-patterns

1. **Hallucinated insight.** Ad ne formule pas d'insight, modèle invente une vérité non-dite "punchy". Règle : modalité `absente` ou champ `-`. Mieux vaut une absence honnête qu'une fabrication.
2. **Forced mecanique.** Aucune des mécaniques registry ne fitte, modèle force le match le moins pire. Règle : `other` + flag `mecanique_proposal`. Le registry grandit par ces flags.
3. **Phantom navigation leak.** Imiter le style `/phantom` avec "→ Tape : decompose-next". Règle : 1 reco contextuelle en prose, pas de menu, pas de slash command surfacé.
4. **Field name leak.** Surface "intent: DR" ou "craft_mode: product_only" à l'opérateur. Règle : traduction systématique en langage métier ("type de campagne", "cadrage").
5. **Pixel-counting.** Sur-décomposer chaque détail visuel sans hiérarchiser (audit S55 anti-pattern). Règle : Section 1 reste haut niveau (5-7 observables clés), pas inventaire exhaustif. La densité est dans Section 2 interprétation.

### Anti-patterns v2.3.0 (dual-bras · persist)

6. **Namespace cross-contamination.** Keyer une ad concurrente en CRT-NN, ou une créa nôtre en RCV-NN. Règle : `external_benchmark`/`trendtrack_pull`/`manual_drop`-inconnu → RCV (decomposition.json) ; `internal_production` → CRT (split). RCV et CRT scannés séparément, jamais fusionnés.
7. **Schéma erroné sur le benchmark.** Valider `decomposition.json` contre `creative.schema` (dont `creative_id ^CRT-[0-9]{2,4}$` rejette une décompo keyée RCV). Règle : le benchmark valide contre `decomposition.schema.json` (`decomposition/1.2`, le reverse natif). creative.schema = bras interne uniquement.
8. **Version skew + champ version mal placé.** (a) Écrire `_schema_version: "creative/1.1"` (l'ancien cassé) alors que la cible interne est `creative/1.3`. (b) **Écrire un `_schema_version` top-level sur le BENCHMARK ou sur `genome.json`** : les schémas `decomposition` ET `genome` sont `additionalProperties:false` et le REJETTENT (seul `creative.json` le porte) → le fichier planterait à la validation. Règle : interne → seul `creative.json` porte `_schema_version` top-level aligné sur la cible (`creative/1.3`) · `genome.json` (`genome/1.2`) n'en porte JAMAIS ; benchmark → PAS de `_schema_version` top-level, la version vit dans `meta.schema_version` (`1.1.0`).
9. **Enum-lock du registre.** Hardcoder les mécaniques dans le skill ou écrire un enum figé dans `creative-mechanics-registry.md`. Règle : le registre reste free-string SSOT évolutif ; émettre via le snapshot enum projeté (HR8bis), proposer (mode=proposed brand_only), jamais entériner.
10. **Asset orphelin.** Écrire un binaire (image de réf, render) sans sidecar `produced/{slug}.json`, ou hors structure `{RCV|CRT}-NN/produced/`. Règle : tout binaire direct + sidecar gated. Pas de binaire sans manifest.
11. **mkdir non-atomique délégué au gate.** Sauter STEP 0c et compter sur le `mkdir(exist_ok=True)` du gate (write-to-context.py L453). Règle : la claim atomique (mkdir sans `exist_ok`) est faite par le skill, refus AVANT claim.

### Anti-patterns v1.1 (visual_identity)

12. **Skip visual_identity lookup.** Ignorer `spec.json#visual_identity` et passer ad screenshot bruité comme reference (régression label garantie sous 2 iter).
13. **Hardcode distinctive_features dans le skill.** Modifier le prompt distinctive_features hardcodé dans le skill au lieu de lire `visual_identity` (drift inévitable cross-products).
14. **Trust image gen model to guess label.** Supposer que le model image gen (nano-banana-2 ou legacy) va deviner correctement le label sans hard constraint dans le prompt. Pattern audit S55 reste valide même avec Gemini 3 Pro Image · text preservation natif meilleur mais pas absolu.
15. **Skip QC distinctive_features.** Skip la validation `distinctive_features[]` dans le QC post-gen.

---

## Edge cases

- **Video sans frame texte exploitable.** Extraire 3 frames (Step 1, milieu, fin), choisir celle avec densité texte la plus haute. Si toutes les frames sont pure visuel, accepter `Hook texte: -`.
- **Carousel multi-cartes.** Décomposer la carte 1 comme NOYAU principal, mentionner les cartes 2-N en `Notes` interne (pas surfacé Section 1). Si une carte ailleurs porte le pivot, déplacer en NOYAU et expliquer en Section 3. Côté encodage interne (genome), chaque carte = une frame `carousel` (2+ frames).
- **Ad UGC / témoignage.** Persona = créateur, pas la marque. Levier souvent appartenance ou preuve sociale. Mécanique typiquement `visceral-specific-testimony` ou `paradox-testimonial` (vérifier registry + snapshot enum).
- **Ad bilingue ou code-switch.** Tagger langue dominante en TAGS, mentionner code-switch dans Section 1 Branding visible.
- **TrendTrack auth absent.** Surface honnête, ne pas tenter mock. Propose `manual_drop` comme fallback (route alors en BRAS REVERSE / RCV par défaut).
- **`manual_drop` ambigu (créa nôtre ou concurrente ?).** Par défaut RCV (benchmark) sauf déclaration opérateur explicite que c'est une de nos créas. Une ad inconnue n'est jamais notre canonical (pas de mutation cross-graph forcée).
- **Décompo d'une créa nôtre déjà testée (interne).** Dériver `meta.validation_status.confidence` depuis `performance.test_results` existants (`confidence_source: "derived_from_test_results"`) au lieu du default hypothesis.

---

## Cross-refs

- Schéma cible BENCHMARK : `resources/schemas/decomposition.schema.json` v1.2 (`decomposition/1.2`, promotion du reverse natif `video-ad-analysis-v1.0` · support-agnostic statique · beat_type/style_id/mechanic_id natifs = pont A=B · D#481 brique 4 étape D).
- Schémas cibles INTERNE (split) : `resources/schemas/genome.schema.json` v1.2 (`genome/1.2` · ADN · mêmes enums que decomposition) + `resources/schemas/creative.schema.json` v1.3 (`creative/1.3` · lignage · variant_of CRT|RCV + lineage{}) + `resources/schemas/produced-asset.schema.json` v1.0 (sidecar manifest binaire).
- Convention stockage : `resources/conventions/creative-storage.md` (D#481 · forme batch `competitive-intel/{batch}/{RCV-NN}/` + `creatives/{batch}/{CRT-NN}/` + allocation mkdir-claim atomique).
- Gate runtime : `write-to-context.py` ALLOWED_PATH_PATTERNS (path-only · accepte `decomposition.json` à `competitive-intel/{batch}/{RCV-NN}/` + le split CRT · les anciennes formes plates `competitive-intel/decomposed/{CRT-NN}.json` et `produced/{CRT-NN}.json` sont REJETÉES). `validate-resources` ne couvre que `resources/`, jamais `brands/`.
- Équation : `resources/templates/creative-formula.md` v3.1 (stress-tested S55, 23 ads cross-typologies).
- SSOT mécaniques : `resources/registries/creative-mechanics-registry.md` (free-string évolutif · snapshot enum projeté pour A=B, HR8bis).
- Schwartz stages : `resources/schemas/_shared/awareness-stage.json`.
- Audit S55 origine : D#391 (creative.schema absorption de 8 champs depuis angle.schema v1.1).
- Sibling skills : `compose-creative` v1.9.0 (FORWARD · même maison CRT, pattern mkdir-claim + split miroir), `produce-paid-angles` (forward generation), `analyze-copy` (long-form), `watch-competitors` (surveillance), `audit-meta-account` (full account audit), `adapt-from-competitor` v1.0.0+ (consume decomposition.json RCV downstream · produit CRT brand-side variant_of=RCV-NN).
- Visual identity schema : `resources/schemas/spec.schema.json#visual_identity` (v1.10+, S55 v2.31 extension).
- Audit visual fidelity : `decisions.md` D#392 (S55 audit régression label wordmark with brackets, prompt brand-side → trigger HR2bis + HR5bis).

### Related canon (v2.0.0)

- `docs/system/operational-system-doctrine.md` v2.71 (équation maître canonisée · canon résonance back-end)
- `docs/system/compositional-cartography.md` v3.1 (équation v3.1 NOYAU × CONTEXTE × MODIFIEURS canon)
- `docs/system/canonical-matrix-reasoning.md` (schema + matrice canon)
- `adapt-from-competitor` v1.0.0+ NEW downstream orchestrator (consume decomposition.json RCV benchmark · variant_of=RCV-NN)

### Related canon (v2.1.0)

- `docs/system/canonical-matrix-reasoning.md` (scoring intersectionnel canon · 5 dimensions fit-check)
- `docs/system/investigation-posture.md` (diagnostic 5 sections canon adapté fit-check)
- `adapt-from-competitor` v1.0.0 downstream avec reco actionable depuis fit-check Section 5
