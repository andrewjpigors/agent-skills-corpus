---
name: adapt-from-competitor
type: orchestrator
version: "2.0.0"
recommended_model: sonnet
subagent_safe: true
isolation_scope: brand_only
layer: production
reasoning_pattern: matrix-driven
matrix_mode: composing
description: >
  v2.0.0 (Brique 4 étape E · repath LECTURE source RCV + ÉCRITURE variante CRT batch-du-jour + split + mkdir-claim + variant_of cross-namespace) · Orchestrator pour adapter une créa concurrente décomposée à la brand opérée. DERNIER maillon de la chaîne créa (3e écrivain de la maison après compose + recompose). LIT la décompo SOURCE concurrente sous `brands/{slug}/competitive-intel/{batch}/{RCV-NN}/decomposition.json` (namespace RCV, schéma natif reverse `decomposition/1.0` depuis decompose-ad v2.3.0 bras REVERSE · NOYAU preserved + CONTEXTE adaptable + MODIFIEURS situationnels), id RCV-NN GLOBAL scanné cross-batch. PRODUIT une variante = un NOUVEAU `CRT-NN` dans le batch DU JOUR sous `brands/{slug}/creatives/{batch}/{CRT-NN}/` (namespace CRT, split genome.json + creative.json + produced/{slug}.json sidecar + brief.md, dossier réservé par mkdir-claim atomique STEP 0). variant_of = le RCV-NN source (lignage cross-namespace concurrent→nous, pattern `^(CRT|RCV)-[0-9]{2,4}$`). variant_axis SINGLE (axe dominant ou null) conforme enum canonique creative.schema ; le multi-axe (audience+pain+proof+mécanisme+offre) vit dans `lineage.adaptation_axes[]` séparé. _schema_version creative/1.4 + genome/1.2 écrits, decomposition/1.0 lu en source.
  Pré-remplit le contexte brand opérateur (audience cartographiée matching + pain_point canonical
  matching + verbatim Trustpilot auto-pick + spec composition matching + offer.canon), propose 3 paths flow opérateur (variant complet · 1 axe seul ·
  enregistre pattern registry).
  Pipeline 5 phases · load competitor decomposition + brand context, match canonical refs,
  operator gate isolation variables, chain produce-copy-brief brand-side,
  optionnel compose-creative variant.
  Output operator-facing 100% humain · canon résonne back-end · zero raw field
  name · zero registry ID exposé · zero acronyme doctrine.
  FR · "adapte cette créa concurrente", "adapt-from-competitor", "adapter cette
  ad à ma brand", "reprendre cette pub".
  EN · "adapt from competitor", "adapt this ad to my brand", "rework this ad".
  FR: "adapte cette créa concurrente", "fais une variante de cette ad", "adapte cette pub à ma marque", "décline cette créa pour nous".
  EN: "adapt this competitor ad", "make a variant of this creative", "adapt this ad to my brand".
permissions:
  reads: [resource, brand, competitive-intel]
  writes: [brand]
  mode: proposed
  subagent_safe: true
  external_apis: []
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Task
isolation_scope: brand_only
matrix_mode: composing
disambiguates_against:
  decompose-ad: "decompose-ad reverse-engineer 1 ad concurrente en décompo native (benchmark → competitive-intel/{batch}/{RCV-NN}/decomposition.json, schéma decomposition/1.0) + fiche v5 ANATOMIE 3 niveaux. adapt-from-competitor consume cette décompo RCV + adapte à la brand opérée via chain orchestrator (écrit une variante CRT-NN brand-side)."
  recompose-creative: "recompose-creative adapte UNE créa interne brand-side (source creatives/{batch}/{CRT-NN}/creative.json, namespace CRT) sur 1 axis variant explicite, variant_of=CRT. adapt-from-competitor adapte depuis UNE créa CONCURRENTE décomposée (source competitive-intel/{batch}/{RCV-NN}/decomposition.json, namespace RCV) avec multi-axes (audience + pain + proof + mécanisme + offer simultanément, NOYAU preserved strict), variant_of=RCV cross-namespace. recompose ne consomme JAMAIS un RCV-NN directement."
  creative-brief-composer: "creative-brief-composer orchestrator produit brief copy + variants visuels depuis angle interne brand (ANG-NN). adapt-from-competitor orchestrator chain produit brief copy + variants depuis créa concurrente décomposée (RCV-NN) + adaptation contexte brand. adapt-from-competitor upstream invoke creative-brief-composer downstream après isolation variables."
pipeline:
  preconditions:
    - decompose-ad v2.3.0+ bras REVERSE output disponible · decomposition.json (decomposition/1.0) persisted dans brands/{slug}/competitive-intel/{batch}/{RCV-NN}/ (namespace RCV, scan cross-batch pour localiser le RCV-NN)
    - brand canonical cartographié (audiences + pain_points + objections + proofs + offers + spec composition)
    - "{batch} du jour résolu (run date-stampé, ex 2026-06-07-NN) et `mkdir -p brands/{slug}/creatives/{batch}/` exécuté AVANT le mkdir-claim (STEP 0), sinon STEP 0 n'a pas de dossier-batch parent pour la variante CRT"
  postconditions:
    - operator decision logged · path A variant complet OR path B 1 axe seul OR path C registry promotion
    - downstream skill invoked (produce-copy-brief OR compose-creative OR promote-mecanique)
    - "Path A · variante brand-side persistée dans le batch DU JOUR sous brands/{slug}/creatives/{batch}/{CRT-NN}/ via le split · genome.json (genome/1.2 · ADN adapté) + creative.json (creative/1.4 · variant_of=RCV-source, variant_axis single canonique ou null, lineage{} avec adaptation_axes[] si multi-axe) + sidecar produced/{slug}.json (produced-asset/1.0) + brief.md. Dossier {CRT-NN}/ réservé par mkdir-claim atomique STEP 0. JPG direct sous produced/{slug}.jpg AVEC sidecar. tags.source = internal_production."
---

# Skill · Adapt From Competitor

Orchestrator pour adapter une créa concurrente décomposée à la brand opérée. Phase 2 du flow décompose créa concurrente · Phase 1 (decompose-ad v2.3.0 bras REVERSE) a produit la décompo native `decomposition.json` (namespace RCV) + la fiche v5 ANATOMIE 3 niveaux. L'opérateur a dit "oui je veux l'adapter". Ce skill prend le relais.

> **v2.0.0 (Brique 4 étape E)** : adapt LIT la décompo source sous `competitive-intel/{batch}/{RCV-NN}/decomposition.json` (namespace RCV, schéma `decomposition/1.0`, scan cross-batch) et ÉCRIT une variante brand-side = un NOUVEAU `CRT-NN` dans le batch DU JOUR sous `creatives/{batch}/{CRT-NN}/` (split genome/creative/sidecar/brief comme compose + recompose). mkdir-claim atomique STEP 0. `variant_of` = le `RCV-NN` source (lignage cross-namespace concurrent→nous). `variant_axis` SINGLE (axe dominant ou null), le multi-axe vit dans `lineage.adaptation_axes[]`. Voir HR7 + HR-AC-CANON-1.

## Tone

Posture stratège marketing senior · "voici comment on rend cette créa tienne". Pas inspecteur, pas pixel-counter. L'opérateur a déjà vu la décomposition · ici on entre dans la décision d'adaptation. Sections directes, options claires, 3 paths flow opérateur. Aucun jargon plumbing, aucun nom de field JSON, aucun acronyme doctrine en surface.

## Expert methodology

**Persona** · senior media buyer + creative strategist qui a adapté des centaines de créas concurrentes top performer sur ses propres brands. Sait isoler ce qui doit rester stable (NOYAU · ce qui fait performer) vs ce qui doit être adapté (CONTEXTE · ce qui rend la créa "tienne") vs ce qui se situe selon la campagne (MODIFIEURS).

## Pipeline

### Phase 1 · Load competitor decomposition + brand context

Read inputs ·

- `brands/{slug}/competitive-intel/{batch}/{RCV-NN}/decomposition.json` (décompo native reverse depuis decompose-ad v2.3.0 bras REVERSE · schéma `decomposition/1.0` · namespace RCV) · NOYAU + CONTEXTE + MODIFIEURS encodés dans les champs natifs du reverse (script.hook.mechanic_id, script.body_arc[].beat_type, visual.styles_observed[].style_id, atlas_consumed.pain_points_referenced / proof_elements_used / offer_elements_visible, audience_targeting_inferred). L'id source `RCV-NN` est GLOBAL au namespace RCV (batch-indépendant) → localiser par **scan cross-batch** (cf HR1).
- `brands/{slug}/brand.json` (identity · positioning · driver_blend · brand_equity · creative_zone)
- `brands/{slug}/audiences/*/profile.json` (cartographie audience hiérarchique)
- `brands/{slug}/audiences/*/pain_points/*.json` (PNT-NN canonical)
- `brands/{slug}/audiences/*/objections/*.json` (OBJ-NN canonical)
- `brands/{slug}/products/*/spec.json` (composition + mechanisms)
- `brands/{slug}/products/*/offers.json` (offers + guarantees · offer.canon)

Halt si decompose-ad output absent (décompo `decomposition.json` introuvable au scan cross-batch) OR brand not cartographié (cf DRGFP canon).

### Phase 2 · Match canonical refs (silent back-end)

Match competitor CONTEXTE refs (lus depuis la décompo native RCV) sur brand canonical · scoring algorithm ·

- `audience_targeting_inferred.audience_persona_visual_label` competitor vers matching AUD-NN brand cartographié (similarity score 0-1 sur profile.pain_points + profile.triggers + profile.demographics)
- `atlas_consumed.pain_points_referenced[].pain_text_observed` competitor vers matching PNT-NN brand canonical (similarity sur surface + consequence + deep)
- `atlas_consumed.proof_elements_used[].proof_type` competitor vers matching proof-registry ID brand (e.g. competitor "testimonial-personal-first-person" vers brand verbatim Trustpilot canonical OR best-seller-badge selon proof available)
- `atlas_consumed.mechanisms_invoked[].mechanism_text_observed` competitor vers matching spec.composition + spec.mechanisms brand
- `atlas_consumed.offer_elements_visible[].offer_type` competitor vers matching offers.canon brand (e.g. competitor "guarantee-mbg" vers brand offer.guarantees.refund_window)

Output canonical refs matched · pré-rempli pour Phase 3 operator gate.

### Phase 3 · Operator gate isolation variables (AskUserQuestion · 3 paths)

Surface canonical output opérateur-facing ·

```
══════════════════════════════════════════════════════════════════════
ADAPTER · cette pub concurrente à ta brand {ton_slug}
══════════════════════════════════════════════════════════════════════

  Mécanique source · [label humain mécanique narrative]
  Ce qu'on garde · 5 éléments du noyau (la mécanique narrative · le format ·
  la phrase d'accroche · l'élément pivotal · l'équilibre copy/visuel)

CE QUI EST PRÉ-REMPLI DEPUIS TON TERRITOIRE

  Audience visée         · [label humain audience matching · ex "infirmières
                           12h shifts · workers-shifts cartographié"]
  Douleur adressée       · [label humain pain_point matching · ex "fatigue
                           plantaire 10h+ debout"]
  Verbatim de preuve     · [label humain · ex "3 candidats depuis ton
                           Trustpilot · auto-pick top"]
  Mécanisme produit      · [label humain · ex "compression arche TPU +
                           amortissement gel multi-couche"]
  CTA et garantie        · [label humain · ex "ta garantie 60 jours canon"]

CHOISIS TON FLOW

  → Variant complet · brief copy + variants visuels Meta-ready
    NOYAU preserved + CONTEXTE adapté · produit brief copy en 5-10 min

  → Tester 1 axe spécifique avant brief complet
    isole 1 dimension · audience seule OR pain seule OR proof seule
    OR mécanisme seul · 3-5 min

  → Garder l'analyse · enregistrer le pattern dans le registry pour plus tard
    pas de brief variant maintenant · pattern observée stockée
    creative-mechanics-registry pour réutilisation future
```

Operator choice · A · B · C (via AskUserQuestion tool).

### Phase 4 · Chain downstream selon path

> Le mkdir-claim atomique (réservation du `{CRT-NN}/` dans le batch DU JOUR) est exécuté en **STEP 0 de HR-AC-CANON-1** (section ci-dessous), AVANT toute persist Path A. Les refus (décompo source introuvable · brand not cartographié · matching impossible) passent AVANT la claim · jamais de dossier vide réservé.

**Path A · Variant complet** ·

- **STEP 0 · mkdir-claim** le `{CRT-NN}/` dans le batch DU JOUR (HR-AC-CANON-1 · résoudre {batch}, scan max CRT cross-batch, `mkdir` atomique, retry +1 sur EEXIST) AVANT tout write.
- Task tool invoke `produce-copy-brief` avec context · NOYAU preserved (lu depuis `decomposition.json` source) + CONTEXTE adapté brand-side (refs canonical matched Phase 2) + MODIFIEURS opérateur-choice (Phase 3).
- Sub-skill produit brief copy + variants visuels Meta-ready.
- **Persist split** sous `brands/{slug}/creatives/{batch}/{CRT-NN}/` (le dossier réservé STEP 0) · `genome.json` (ADN adapté · genome/1.2) + `creative.json` (lignage · creative/1.4) + sidecar `produced/{slug}.json` (produced-asset/1.0) + `brief.md`. Détail HR7 + HR-AC-CANON-1.
- `variant_of` = le `RCV-NN` source (lignage cross-namespace concurrent→nous · vit dans `creative.json#lineage.variant_of`, pattern `^(CRT|RCV)-[0-9]{2,4}$`). `variant_axis` = l'axe dominant (single, enum canonique) OU null si pas réductible à un axe unique. Le lignage multi-axe (audience+pain+proof+mécanisme+offre) vit dans `creative.json#lineage.adaptation_axes[]` séparé (cf HR8 · jamais dans variant_axis qui reste single).

**Path B · 1 axe spécifique** ·

- AskUserQuestion second-level · "quel axe isoler ?" (audience · pain · proof · mécanisme produit · CTA)
- adapt isole 1 dimension et produit un variant 1 axe seul via le pipeline Path A simplifié (mkdir-claim + split sous `creatives/{batch}/{CRT-NN}/`, `variant_axis` = l'axe canonique isolé · ex `persona_split` pour audience, `hook_swap` pour accroche · valeur single de l'enum creative.schema).
- **Note · recompose-creative ne consomme JAMAIS un RCV-NN directement** (recompose lit une source INTERNE `creatives/{batch}/{CRT-NN}/creative.json`, namespace CRT). Le source d'adapt est RCV (concurrent). Donc on n'invoque PAS recompose-creative sur la source concurrente · adapt produit lui-même le variant 1 axe brand-side (un CRT-NN dont `variant_of`=RCV-NN), exactement comme Path A mais sur une seule dimension. Si l'opérateur veut ensuite décliner cette variante interne sur d'autres axes, ALORS recompose-creative opère sur le CRT-NN désormais interne (jamais sur le RCV).

**Path C · Registry promotion** ·

- Pas de brief variant maintenant · pas de mkdir-claim (aucune créa produite).
- Log mécanique observée dans `learnings.json` brand · candidate promotion vers `creative-mechanics-registry.md` après N validations cross-brand
- Halt skill · opérateur peut re-invoque adapt-from-competitor plus tard

### Phase 5 · Synthesis 5 sections investigation-posture

Toute output stratégique adapt-from-competitor termine par synthese 5 sections IP (cf doctrine investigation-posture · canon CLAUDE.md root) ·

- Observé · {ce qui était dans la décompo concurrente · champs natifs `decomposition.json` résonance}
- Déduit · {match canonical refs brand · scoring + confidence chain}
- Inconnu · {variables non-matchable · gaps refs brand · à creuser}
- Leviers · {sub-skills disponibles · produce-copy-brief · compose-creative · promote-mecanique}
- Close ouvert · {opérateur arbitre · path final OR adjust}

## Hard Rules

### HR1 · Input mandatory decomposition.json (namespace RCV · scan cross-batch)

adapt-from-competitor v2.0.0 REQUIRES decompose-ad v2.3.0+ bras REVERSE output preserved · `brands/{slug}/competitive-intel/{batch}/{RCV-NN}/decomposition.json` (schéma `decomposition/1.0`, namespace RCV). PAS la forme flat-legacy `competitive-intel/decomposed/{CRT-NN}.json` (mauvais namespace CRT pour une ad concurrente, mauvais nom de fichier).

L'id source `RCV-NN` est GLOBAL au namespace RCV (batch-indépendant) → localiser par **scan cross-batch** de tous les dossiers `competitive-intel/*/{RCV-NN}/` ·

```
ls -d brands/{slug}/competitive-intel/*/{RCV_source} 2>/dev/null | head -1
```

Halt si absent (décompo introuvable au scan). Re-prompt decompose-ad sur source ad concurrente (produit la décompo RCV en amont). RCV est scanné SÉPARÉMENT de CRT (les deux namespaces ne se croisent jamais · RCV = concurrents reverse, CRT = nos créas forward).

### HR2 · Brand context required

Brand cartographié (audiences + pain_points + objections + proofs + offers + spec composition) REQUIRED. Halt si brand not setup (cf snapshot-brand + setup-brand + build-atlas-complete upstream).

### HR3 · NOYAU preserved strict

5 éléments NOYAU (mécanique · format · phrase d'accroche · élément pivotal · équilibre copy/visuel · lus depuis la décompo source `decomposition.json` · `script.hook` / `visual.styles_observed` / `script.body_arc`) INCHANGÉS dans variant brand-side. Modifier le NOYAU casse la créa · violation canon · refus orchestrator.

### HR4 · CONTEXTE adapté brand-side canonical

5 refs CONTEXTE (audience · pain · proof · mécanisme · CTA) adaptées via matching canonical refs brand (Phase 2). Pas freelance · matching score required >0.6 sinon AskUserQuestion alternative.

### HR5 · MODIFIEURS opérateur-choice

5 modifieurs (canal · saisonnalité · ton · destination · offer attachée) opérateur-choice via AskUserQuestion (Phase 3 path A). Plusieurs valeurs possibles selon campagne cible.

### HR6 · Output opérateur-facing 100% humain

ZERO raw field name (`audience_targeting_inferred`, `atlas_consumed.pain_points_referenced`, etc.). ZERO registry ID exposé (mecanique-registry IDs · proof-registry IDs · angle-registry IDs). ZERO acronyme doctrine. ZERO `RCV-NN` / `CRT-NN` / `genome.json` / `decomposition.json` en clair. Labels humains accessibles uniquement. Canon résonne back-end via le split (genome.json ADN + creative.json lignage) · cross-skill reproducibilité.

### HR7 · Persist split genome.json + creative.json + sidecar + brief.md (Brique 4 étape E)

> Le mkdir-claim atomique (réservation du `{CRT-NN}/` dans le batch DU JOUR) est exécuté en **STEP 0 de HR-AC-CANON-1** (section ci-dessous), AVANT cette persist. HR7 écrit dans le dossier déjà réservé. La variante adapte l'ADN lu depuis la décompo source RCV. **NEVER** Edit/Write direct sur un `.json`, **ALWAYS** via `write_to_context` mode=proposed.

La variante brand-side se persiste en trois fichiers `.json` (+ le brief `.md`), chacun conforme à son schéma · split miroir compose-creative v1.9.0 + recompose-creative v1.4.0.

**genome.json** (ADN adapté brand-side · conforme `genome.schema.json` `_schema_version: "genome/1.2"`, strictement nu) ·
- `script_id` : nouveau `GSC-NN` (Genome SCript · clé de join perf future · PAS CRT-NN · pattern `^GSC-[0-9]{2,4}$`).
- `support`, `route`, `hook`, `frames`, `genome_tags` : le NOYAU est PRÉSERVÉ depuis la décompo source (`decomposition.json#script.hook.mechanic_id` → `genome.hook.mechanic_id` · même enum reverse↔forward = pont A=B · `script.body_arc[].beat_type` → `frames[].role` · `visual.styles_observed[].style_id` → `frames[].visual_script.style_id` · **`decomposition.mecanique.mecanique_id` → `genome_tags.mecanique_id`** (le CONCEPT ad-level de la créa concurrente · pont A=B sur l'axe concept · NE PAS le perdre · D#491) · **l'ANGLE brand choisi pour l'adaptation → `genome_tags.angle_id`** (unité STRATÉGIQUE de 1ère classe · porte l'objection à neutraliser, l'OTRB, le payoff · c'est l'angle Stepprs sur lequel on re-coule le ressort, PAS celui du concurrent · D#492) · **`audience_slug`** ciblée). Le CONTEXTE est adapté brand-side (copy/visual des frames recalibrés sur les refs matched Phase 2).
- `lineage` (optionnel ADN abstrait) : `{concept_id, angle_id (ANG-NN si applicable), persona_label, ref_ad_id (= le video_id/ad_id de la source concurrente, pont apprenable)}`.

**creative.json** (lignage · conforme `creative.schema.json` `_schema_version: "creative/1.4"`) ·
- `creative_id` : nouveau `CRT-NN` (réservé par mkdir-claim STEP 0 · pattern `^CRT-[0-9]{2,4}$`).
- `mode` : `concept | template | asset`. `audience_slug` (l'AUD-NN brand matched Phase 2). `_equation_ref` const v3.1.
- `concept_id` : nouveau `cpt_{brand_slug}_{angle_short}_{NNN}` (SSOT du groupage de variantes brand-side · l'ad concurrente n'a pas de concept_id brand · on en crée un côté nous).
- `variant_of` = le `RCV-NN` source (le lignage cross-namespace concurrent→nous · pattern `^(CRT|RCV)-[0-9]{2,4}$` · pour adapt c'est TOUJOURS un RCV, JAMAIS un CRT). Vit dans `lineage.variant_of` (+ top-level `variant_of` miroir backward-compat). PAS de suffixe `-competitor` (le namespace RCV porte déjà la sémantique concurrent).
- `variant_axis` ∈ enum canonique creative.schema `[photo_swap, promo_toggle, hook_swap, background_swap, persona_split, null]` (SINGLE string · l'axe DOMINANT de l'adaptation, OU `null` si l'adaptation multi-axe ne se réduit pas à un axe unique). JAMAIS un array · casserait le contrat single-enum partagé avec recompose ET le schéma.
- `lineage{}` : `{angle_ref (ANG-NN), audience_ref, product_ref, mechanism_ref, concept_ref (miroir descriptif de concept_id), variant_of (RCV-source), brief_ref (BRF-NN), ad_id (= ref_ad_id source concurrente), adaptation_axes[]}`. **`lineage.adaptation_axes[]`** capture le lignage MULTI-AXE d'adapt (la liste des dimensions adaptées simultanément · ex `["persona_split", "promo_toggle", "background_swap"]` quand audience+offre+décor changent ensemble) · c'est le champ séparé qui porte le multi-axe pour NE PAS promouvoir `variant_axis` en array.
- `intent_mix` (depuis matching brand + décompo source). Champ legacy `intent` mirror backward-compat.
- `execution.overlay_density` + `execution.brand_mark_present`. Champ legacy `craft_mode` mirror dérivé.
- `meta.validation_status` (object composite) : `{status: "hypothesis", confidence: 0.5, confidence_source: "derived_from_competitor_benchmark"}` (variante adaptée pas encore testée brand-side · la source était une ad concurrente performante, pas notre test). `meta.created`. `meta.created_by_skill: "adapt-from-competitor"`. `meta.decomposed_from` = le ref_ad_id concurrent source.
- `performance.longevity_signal` vide (variante pas encore en prod brand-side). `tags.source: "internal_production"` (c'est désormais NOTRE créa, produite par notre workspace · même si dérivée d'un benchmark concurrent).

**produced/{slug}.json** (sidecar manifest binaire · conforme `produced-asset.schema.json` `_schema_version: "produced-asset/1.0"`) · UN sidecar par binaire `.jpg` produit (anti-orphelin) ·
- `asset_role` (ex `"variant-front"`, `"composite-final"`), `file` (ex `"{slug}.jpg"`), `status: "generated"`, `created_at` requis.
- `tool: "fal"`, `endpoint: "fal-ai/nano-banana-2/edit"` (si Path A invoque compose-creative downstream pour le visuel), `params` (prompt/aspect_ratio/resolution), `source_asset_ref: {kind: "ref_ad_image", path: <image de réf concurrente si stockée sous le RCV-NN source>, ref_ad_id: <video_id concurrent>}`, `hash` optionnel, `qc` optionnel.
- `genome_ref` : `<script_id GSC-NN>` (relie le binaire à l'ADN sans le dupliquer). `created_by_skill: "adapt-from-competitor"`.

**brief.md** · format brief copy + section "ADAPTÉ DEPUIS LA CONCURRENCE". Écrit DIRECT (nom fixe `brief.md`) sous `brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md` (outil Write · `.md` exempt de `ALLOWED_PATH_PATTERNS` ET de mutation-guard, ne PAS router via `write_to_context`).

**Mutation gate (séquence) :**

1. **Dossier déjà réservé** par le mkdir-claim atomique STEP 0 (HR-AC-CANON-1) · `creatives/{batch}/{CRT-NN}/` + `produced/` existent dans le batch DU JOUR. NE PAS s'appuyer sur le `mkdir(exist_ok=True)` du gate (non-atomique · 2 runs concurrents écraseraient le même `CRT-NN`).
2. Write `genome.json` + `creative.json` + sidecar `produced/{slug}.json` via `write_to_context(field_path, value, source, confidence, mode="proposed")` (les trois `.json`). **NEVER edit JSON directly via Edit/Write/NotebookEdit.**
3. Persist JPG : si Path A produit un visuel (via compose-creative downstream), move `/tmp/.../{...}.jpg` → `brands/{slug}/creatives/{batch}/{CRT-NN}/produced/{slug}.jpg`. **Le binaire `.jpg`/`.mp4` est écrit DIRECT** (`write_to_context` ne gère que le `.json`), MAIS son sidecar `.json` (step 2) passe par le gate. Double régime non-négociable.
4. Write brief markdown : `brands/{slug}/creatives/{batch}/{CRT-NN}/brief.md` (nom fixe `brief.md`). **Écrit DIRECT via l'outil Write** (`.md` n'est NI dans `ALLOWED_PATH_PATTERNS` du gate write-to-context, NI dans mutation-guard qui ne garde que `.json`) · ne PAS router le `.md` via `write_to_context` (échouerait).
5. Rebuild snapshot via `python3 .skills/build-brand-snapshot.py {slug}` si un core file est touché (mutation rule · la variante est un nouvel artefact créa du brand).
6. Trigger `validate-resources` silencieusement post-write (valide genome + creative + sidecar contre `genome.schema.json` / `creative.schema.json` / `produced-asset.schema.json`, et la forme de path contre `ALLOWED_PATH_PATTERNS`). Flag MAJOR/CRITICAL à l'opérateur si remonte.
7. **Gate QC de sortie** · si le visuel n'a pas déjà été gaté par compose-creative downstream (Path A délégué), invoquer `qc-creative` (`creative_dir` = le `{CRT-NN}/` produit · Task tool · sonnet · subagent_safe) sur le binaire, écrire son verdict dans `produced/{slug}.json#qc` via `write_to_context`, et NE PAS présenter la variante comme spend-ready sans `decision: PASS`. Même règle anti-défaut (logo/produit fidélité-critique = compositing `layered`, jamais re-généré). Voir `qc-creative/SKILL.md`.

### HR8 · variant_axis SINGLE · multi-axe dans lineage.adaptation_axes[]

adapt-from-competitor est **multi-axe CONCEPTUELLEMENT** (il adapte audience + pain + proof + mécanisme + offre SIMULTANÉMENT, c'est sa nature vs recompose qui change 1 seul axe). MAIS `variant_axis` reste **SINGLE** (un seul string de l'enum canonique creative.schema `[photo_swap, promo_toggle, hook_swap, background_swap, persona_split, null]`, OU null), JAMAIS un array.

- `variant_axis` = l'**axe DOMINANT** de l'adaptation (celui qui porte le plus de signal · ex `persona_split` si le changement le plus marquant est l'audience) OU `null` si l'adaptation multi-axe ne se réduit pas à un axe unique dominant.
- Le **lignage multi-axe** (la liste des dimensions adaptées ensemble) vit dans `creative.json#lineage.adaptation_axes[]` (champ séparé · array de valeurs de l'enum canonique). C'est CE champ qui capture le caractère multi-axe d'adapt, PAS `variant_axis`.
- **NEVER** promouvoir `variant_axis` en array · casserait (a) le contrat single-axis de recompose-creative et (b) le schéma single-enum creative.schema (validate-resources rejette).
- **NEVER** persister une valeur `variant_axis` hors enum canonique creative.schema. Tout vocab variant_axis hors-enum (legacy `new_*`, `platform_swap`, `format_swap`, `visual_treatment_swap`, `audience_swap`, ou suffixes bricolés) est SUPPRIMÉ · seul l'enum canonique single est valide.

### HR9 · Lineage cross-namespace variant_of = RCV

Variant brand-side `brands/{slug}/creatives/{batch}/{CRT-NN}/creative.json` PERSISTED avec `variant_of: "RCV-NN"` (le `RCV-NN` source · pattern `^(CRT|RCV)-[0-9]{2,4}$`). C'est LE cas d'usage qui justifie que `variant_of` accepte un RCV · le lignage CROSS-NAMESPACE concurrent→nous (decompose-ad bras interne et recompose écrivent variant_of=CRT ; adapt écrit variant_of=RCV). Lineage canon · traçabilité full du concurrent vers notre créa · cycle apprentissage couches op-system v2.71. Vit dans `creative.json#lineage.variant_of`. Le namespace de la variante elle-même reste CRT (notre créa) · seul son parent est RCV (le concurrent décomposé). PAS de suffixe `-competitor` (le namespace RCV porte déjà la sémantique).

## HR-AC-CANON-1 · Entry canonical batch + mkdir-claim (Brique 4 étape E · exécutable)

> Cette règle matérialise l'entrée canonique de la variante adaptée, miroir de compose-creative v1.9.0 (HR-CC-CANON-1) et recompose-creative v1.4.0 (HR-RC-CANON-1). Toute variante adaptée depuis un concurrent DOIT créer son dossier canonique `brands/{slug}/creatives/{batch}/{CRT-NN}/` AVANT tout write, persister le split (genome + creative + sidecar + brief), et interdire tout asset orphelin hors structure. Cross-ref `resources/conventions/creative-storage.md` (D#481).

### Refus AVANT claim (ordre HR1/HR2)

Tous les refus (décompo source `decomposition.json` introuvable au scan cross-batch RCV · brand not cartographié · matching canonical impossible <0.6 sans alternative operator · path C registry-only sans production) s'exécutent **AVANT STEP 0c**. Un run refusé OU un Path C (pas de créa produite) ne doit JAMAIS laisser un dossier `CRT-NN/` réservé vide. La claim atomique ne se prend qu'une fois la production garantie (Path A ou Path B uniquement).

### STEP 0 · mkdir-claim atomique (AVANT tout write_to_context)

Le mkdir-claim s'exécute en **STEP 0** de Phase 4 Path A (ou Path B), juste avant la persist split. **La variante va dans le batch DU JOUR (run courant), PAS dans le batch de la source concurrente** · le RCV source est trouvé par scan cross-batch (HR1), mais le nouveau CRT-NN est écrit dans le `{batch}` du jour par cohérence-de-run.

**STEP 0a · résoudre {batch} du jour.** `{batch}` = run date-stampé du jour, lowercase + chiffres + tirets (regex gate `[a-z0-9-]+`). Default = `$(date +%Y-%m-%d)-NN` où NN = prochain run 2-digit du jour. Résoudre NN · lister `brands/{slug}/creatives/` pour les dossiers matchant `$(date +%Y-%m-%d)-*`, prendre le max suffixe, sinon `01`. Un run PEUT réutiliser le batch de session déjà ouvert. `mkdir -p brands/{slug}/creatives/{batch}/` (idempotent · le dossier-batch n'est PAS la claim).

**STEP 0b · candidat CRT-NN (scan max cross-batch).** Scanner TOUT l'arbre du namespace CRT pour le max existant, PAS juste le batch courant (les id sont globalement uniques dans le namespace CRT, batch-indépendants) ·
```
ls -d brands/{slug}/creatives/*/CRT-* 2>/dev/null | grep -oE 'CRT-[0-9]{2,4}' | sort -t- -k2 -n | tail -1
```
→ N. Candidat = `CRT-(N+1)`, zero-paddé à ≥2 digits. CRT scanné SÉPARÉMENT de RCV (jamais fusionnés · RCV = namespace concurrent decompose-ad · la variante adaptée est dans le namespace CRT, seul son `variant_of` pointe vers RCV).

**STEP 0c · claim atomique.** `mkdir brands/{slug}/creatives/{batch}/CRT-{N+1}/` SANS `-p` sur le segment final (le parent `{batch}/` existe déjà depuis 0a). `mkdir` sur un dossier existant échoue → **c'est le verrou** (la réservation). Sur succès · l'id est à toi, immédiatement `mkdir -p brands/{slug}/creatives/{batch}/CRT-{N+1}/produced/`. Sur EEXIST · `N = N+1`, retry (boucle bornée, ex 50 essais). C'est le SEUL mécanisme de réservation · pas de fichier-index, pas de lock-file, pas d'écrivain privilégié. Les trous d'id sont inoffensifs (unicité requise, pas absence-de-trou).

> **PIÈGE (vérifié source · write-to-context.py L453 `target.parent.mkdir(parents=True, exist_ok=True)`)** · ce mkdir du gate n'est PAS une claim atomique. Si un skill saute STEP 0c et compte sur le mkdir du gate, deux runs concurrents passent tous les deux et écrivent dans le MÊME `CRT-NN`, clobbering silencieux. Le `mkdir` atomique (sans `exist_ok`) DOIT être fait par le skill en STEP 0c.

**STEP 0d · write dans le dossier réservé.** MAINTENANT (HR7) · `write_to_context` les trois `.json` (`genome.json`, `creative.json`, sidecar `produced/{slug}.json`) en mode=proposed. Binaires (.jpg/.mp4) déplacés DIRECT sous `.../produced/` (write_to_context ne gère que le json). `brief.md` écrit DIRECT (outil Write · `.md` exempt de `ALLOWED_PATH_PATTERNS` ET de mutation-guard).

### Lignage 5-refs + variant_of=RCV + adaptation_axes[]

`creative.json#lineage` doit être populé · `angle_ref` (ANG-NN) + `audience_ref` (AUD-NN matched Phase 2) + `product_ref` + `mechanism_ref` + `concept_ref` (miroir descriptif de `concept_id`, SSOT groupage = `creative.concept_id` top-level) + `variant_of` (le `RCV-NN` source · cross-namespace concurrent→nous) + `adaptation_axes[]` (le multi-axe d'adapt · array de valeurs canoniques). Cross-refs many-to-many activés. JAMAIS surcharger le dossier `{RCV-source}/` concurrent (il est sous `competitive-intel/`, on n'y écrit pas · la variante est TOUJOURS un nouveau `{CRT-NN}/` sous `creatives/`, source concurrente read-only).

### Interdit orphelin

JAMAIS sauver un asset JPG/PNG standalone hors structure. TOUT binaire vit sous `creatives/{batch}/{CRT-NN}/produced/` AVEC son sidecar `produced/{slug}.json` (manifest gated). Pas de binaire sans sidecar (anti BUG-ASSET-ORPHAN). Pas d'entry variante sans genome.json + creative.json.

## Cross-refs

- `docs/system/operational-system-doctrine.md` v2.71 (équation maître canonisée · 5 couches grammar)
- `docs/system/compositional-cartography.md` v3.1 (équation v3.1 canon)
- `docs/system/canonical-matrix-reasoning.md` (schema + matrice canon)
- `docs/system/investigation-posture.md` (5 sections IP synthese)
- Upstream sibling · `decompose-ad` v2.3.0+ bras REVERSE (produit `decomposition.json` · decomposition/1.0 · namespace RCV sous `competitive-intel/{batch}/{RCV-NN}/`)
- Sibling écrivains de la maison créa (même split + mkdir-claim + forme batch) · `compose-creative` v1.9.0 (forward ex nihilo · CRT) · `recompose-creative` v1.4.0 (variant interne · CRT, variant_of=CRT)
- Downstream sub-skills · `produce-copy-brief` (Path A) · `compose-creative` (Path A visuel downstream) · `promote-mecanique` future (Path C)
- Schemas cibles (Brique 4 étape E · split écrit) : `resources/schemas/creative.schema.json` v1.4 (lignage · variant_of CRT|RCV + lineage{} avec adaptation_axes[] + variant_axis enum canonique SSOT 5+null), `resources/schemas/genome.schema.json` v1.2 (ADN par-créa · script_id GSC-NN, hook, frames, support, genome_tags), `resources/schemas/produced-asset.schema.json` v1.0 (sidecar manifest binaire · 1 par .jpg)
- Schema source lu : `resources/schemas/decomposition.schema.json` v1.0 (décompo native reverse · decomposition/1.0)
- Convention stockage : `resources/conventions/creative-storage.md` (D#481 · forme batch `creatives/{batch}/{CRT-NN}/` + `competitive-intel/{batch}/{RCV-NN}/` + allocation mkdir-claim atomique · RCV source trouvé cross-batch, variante CRT écrite dans le batch du jour)

## Related canon

- `creative-mechanics-registry.md` (mecanique IDs canoniques · résonance back-end)
- `angle-registry.md` (angle IDs canoniques)
- `proof-registry.md` (proof IDs canoniques)
- `brands/{slug}/_snapshot.md` (brand state digest pré-load Phase 1)