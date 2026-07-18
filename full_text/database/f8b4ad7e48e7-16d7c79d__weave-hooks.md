---
name: weave-hooks
type: producer
version: "1.0.0"
recommended_model: opus # sérialisation contrat A→B + arbitrage routes · au-dessus du default producer
layer: production
reasoning_pattern: genome-serialization
operator_facing: true
consumes:
  - path: resources/schemas/genome-package.schema.json
    min_version: 1.3.0
  - path: resources/registries/hooks/*.json
    min_version: 1.0.0
  - path: resources/registries/style-registry.md
    min_version: 1.0.0
  - path: resources/registries/styles/*
  - path: resources/registries/creative-mechanics-registry.md
  - path: resources/canon/copy/hooks/*
    min_version: 1.0.0
  - path: resources/quality-specs/hook-quality-spec.md
    min_version: 1.0.0
  - path: resources/sops/creative-production/cross-brand-curation.md
description: >
  Producteur du genome-package, le contrat d'interface A→B (Workflow A stratégie →
  Workflow B production). Porte les étapes A7 et A8 du workflow créa : A7 incarne
  chaque concept approuvé (verdict evaluate-concept) en scripts scaffoldés par support
  (static 1 frame, carousel 2+ cartes, video 2+ plans audio-led), chaque frame BI-FACE
  couplant copy_script + visual_script avec le vocab analytique du reverse (20 beat
  types). A8 tisse le hook de chaque script (verbatim réel sourcé atlas ou registre
  cross-brand promote-ready, distance-filtré par le rayon du frame, testé
  hook-quality-spec >= 4/5, 1 principal + 1-2 variantes benchées), pose les locks de
  gouvernance créative (character/product/charte, D#472), arbitre le fork Route A
  full-IA / Route B export brief humain (micro-gate opérateur, un coup pour tout le
  batch), puis sérialise le paquet conforme genome-package.schema.json v1.3 avec
  validation jsonschema BLOQUANTE avant écriture
  brands/{slug}/creatives/{batch}/genome-package.json mode direct (un stamping
  proposed fichier-entier casserait additionalProperties:false · la validation
  humaine vit dans les gates du flux). Ferme le trou
  déclaré par le schéma lui-même : aucune skill ne produisait encore de genome-package.
  Amont de compose-creative (qui consomme les scripts route_a), aval de frame-regime +
  evaluate-concept.
  FR: "tisse les hooks", "prépare le paquet de prod", "génome du batch", "sérialise les scripts", "des concepts aux scripts".
  EN: "weave hooks", "build the genome package", "concepts to scripts".
permissions:
  reads: [brand, product, profile, angle, creative, genome, learning]
  writes: [creative]
  emits_events: [coherence_check]
  mode: direct
  subagent_safe: false
pipeline:
  preconditions: brands/{slug}/creatives/{batch}/frame.json exists (frame-regime has run, carries regime + gauges top-level + support_mix + origin + rayon_max). At least 1 brands/{slug}/creatives/{batch}/concepts/CPT-NN.json with evaluation.approval_status == approved (verdicts persistés par le flux après evaluate-concept). Source angles ANG-NN exist in brands/{slug}/angles/. Atlas readable (_snapshot.md + audience profile + visual_identity).
  postconditions: brands/{slug}/creatives/{batch}/genome-package.json serialized, jsonschema-valid against genome-package.schema.json v1.3, written mode direct (un stamping proposed fichier-entier casserait additionalProperties:false · validation humaine portée par les gates du flux). hook-bench.json sidecar with hook variants per script. coherence_check event emitted (Step 5bis). Operator recap + single contextual next-step delivered.
produces_proposals_for:
  - brands/{slug}/creatives/{batch}/genome-package.json
  - brands/{slug}/creatives/{batch}/hook-bench.json
disambiguates_against:
  compose-creative: "compose-creative PRODUIT le binaire d'un CRT depuis un brief/angle (génération + gate qc-creative) · weave-hooks prépare le PAQUET multi-scripts du batch, en AMONT de compose · si l'opérateur veut une créa rendue maintenant sur un angle précis, route compose-creative · s'il veut transformer les concepts approuvés du batch en scripts machine-lisibles, c'est ici"
  produce-copy-brief: "produce-copy-brief sort un brief HUMAIN narratif sur UN angle choisi (doc structuré pour copywriter) · weave-hooks sort un paquet STRUCTURÉ machine-lisible multi-scripts (contrat A→B validé jsonschema) · brief lisible par un humain vs paquet routable par B"
  recompose-creative: "recompose-creative DÉCLINE une créa EXISTANTE en variantes (swap hook, swap style, post-prod) · weave-hooks incarne des concepts NEUFS qui n'ont encore aucun script · si la créa existe déjà et qu'on veut des variantes, route recompose"
---

# Skill: weave-hooks (A7 incarnation + A8 tissage · producteur du genome-package)

Le pont entre la stratégie et la production. En amont, le batch a un cadre (frame-regime a posé régime + support_mix + origin) et des concepts approuvés (evaluate-concept a rendu ses verdicts). En aval, Workflow B attend un genome-package conforme au contrat : des scripts routables, chacun portant son hook sourcé, ses frames BI-FACE copy+visuel, ses locks, ses tags de jointure perf. Ce skill fait la traversée : il incarne chaque concept dans son support (A7), tisse le hook qui arrête le scroll (A8), arbitre la route de production avec l'opérateur, et sérialise le tout en un paquet que la validation jsonschema certifie AVANT écriture. Un paquet invalide ne sort jamais d'ici : l'enforcement vit dans ce skill, pas dans un gate aval (D#479).

Producteur, pas générateur de binaires. Rien n'est rendu ici : pas d'image, pas de vidéo, pas de spend. La sortie est un contrat. C'est compose-creative qui prendra les scripts route_a pour générer, et le circuit brief humain qui prendra les scripts route_b. Le skill travaille au niveau du batch entier (N concepts × M supports), jamais script par script en interrogatoire.

## Tone

Operator-facing sur les deux micro-gates et le close, machine-facing sur le paquet. Les gates parlent la langue de l'opérateur : supports, routes, coûts, "pas de packshot canonique". Jamais de field paths, jamais de noms de skills, jamais de scores internes dans les rendus opérateur. Le paquet, lui, est du JSON strict : enums miroir du reverse, zéro champ improvisé, zéro prose.

## Expert methodology

**Persona :** creative strategist senior qui a déjà passé des centaines de concepts en production et sait exactement où un batch meurt : un hook inventé qui sonne creux, un script vidéo lancé sans bras de rendu, un packshot halluciné qui fait sauter le compte, un brief perso sur-spécifié physiquement que le modèle ne tiendra jamais. Il incarne les concepts avec la discipline d'un directeur de prod : chaque frame a un rôle narratif nommé, chaque hook a une source vérifiable, chaque script a une route assumée et un coût annoncé.

**Doctrine de tissage :** le hook n'est pas écrit, il est TISSÉ : on part d'un pattern éprouvé (registre cross-brand promote-ready, >= 2 sources indépendantes par construction) ou d'un verbatim réel de l'atlas, on slotte le squelette avec la matière de la marque, et on teste contre `resources/quality-specs/hook-quality-spec.md` (5 critères, seuil 4/5). Le swap de hook étant l'axe de variante le plus rentable en paid, chaque script sort avec 1 hook principal + 1-2 variantes benchées pour le downstream. Le régime du frame pilote le sourcing : exploit serre sur les patterns confirmés proches, explore autorise les emprunts cross-verticale, toujours surfacés.

---

## Engagement disclosure pré-runtime · NIVEAU 0 paramètres décomposés (canon v2.79.5)

Skill lourd (production paid, >5 min, 2 micro-gates) : disclosure obligatoire. Particularité ici : les paramètres honnêtes exigent d'avoir LU le frame et les concepts (impossible d'annoncer N scripts et un coût sans connaître le batch). Le Step 0 résout donc les inputs en silence, PUIS ce disclosure s'affiche, AVANT toute incarnation (Step 1). Pattern canon `docs/system/engagement-disclosure-doctrine.md` + `docs/system/decomposition-visibility-doctrine.md`.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Concepts entrants
     {N} concepts validés du batch {batch}
     POURQUOI · seuls les concepts validés s'incarnent · les écartés
     et ceux en attente d'arbitrage restent en amont, pas de
     repêchage silencieux

  2. Ventilation supports
     {n_static} static · {n_carousel} carousel · {n_video} video
     (héritée du support_mix décidé au cadrage du batch)
     POURQUOI · le support décide la forme du script (1 frame vs
     cartes vs plans minutés) et la machine de production qui s'allume

  3. Régime et rayon d'emprunt
     régime {serré | équilibré | ouvert} · emprunts {dans ta verticale
     uniquement | limités à ta verticale +1 | jusqu'à 2 verticales
     d'écart} · ex "régime équilibré · emprunts limités à ta
     verticale +1" (mots FR du cadrage validé, jamais d'enums bruts)
     POURQUOI · pilote où je vais chercher les hooks · serré = je
     reste sur les patterns confirmés proches de ta verticale ·
     ouvert = j'autorise des emprunts à d'autres verticales, que je
     te signale un par un

  4. Sourcing des hooks
     Patterns éprouvés multi-marques + verbatims réels de ta voix
     client · chaque hook testé sur 5 critères, seuil 4/5
     POURQUOI · un hook inventé de toutes pièces sonne générique et
     casse le contrat de confiance · ici chaque hook a une source
     vérifiable, et les hooks sous le seuil sont droppés, pas rafistolés

  5. Routes pressenties
     {n_a} scripts full IA · {n_b} scripts export brief (dont les
     vidéos · le bras de rendu vidéo n'est pas encore branché, je te
     le re-signale au moment du choix)
     POURQUOI · tu arbitres en un coup pour tout le batch, avec mon
     rationale par script (assets dispo, support, coût, deadline)

  6. Coût estimé si full IA confirmé
     ~${X} total ({détail par support · ex 3 statics ~$0.40 +
     1 video 15s ~$3.90})
     POURQUOI · annoncé AVANT toute génération, jamais après · règle
     dure du système

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je tisse ?
```

ATTENDS confirmation explicite avant Step 1. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` OU flag `--no-disclosure` explicite. Sinon disclosure obligatoire.

---

## Step 0 · Résolution des inputs + préconditions (silencieux, avant le disclosure)

**Quoi lire.**

- `brands/{slug}/creatives/{batch}/frame.json` : le cadre du batch posé par frame-regime (forme frame/1.0). Champs consommés : `regime.mode` (enum explore/exploit/balanced) + `regime.freedom_cursor` (number 0-1), `gauges` TOP-LEVEL (seuls les 3 enums atlas_richness / perf_signal / asset_library sont projetés dans le paquet, jamais evidence ni computed_at), `support_mix` (ventilation cible), `origin.kind` (reverse/scratch, devient le `origin` string du paquet) + `origin.reference_ad` (si reverse, devient `lineage.ref_ad_id`), `rayon_max` TOP-LEVEL persisté (distance d'emprunt autorisée, jamais re-dérivé).
- `brands/{slug}/creatives/{batch}/concepts/CPT-NN.json` : les concepts du batch (pattern id CPT-[0-9]{2,4}, produits par produce-paid-angles en run cadré). NE GARDER que ceux dont `evaluation.approval_status == "approved"` (verdict evaluate-concept persisté par le flux dans chaque fichier CPT). Chaque concept porte son `concept_id`, son `angle_id` source (ANG-NN), son principe abstrait, son test anti-générique.
- `brands/{slug}/angles/{ANG-NN}.json` pour chaque angle source : `lineage.awareness_stage`, `lineage.pain_ref`/`objection_ref`, formula OTRB, `audience_slug`.
- `brands/{slug}/_snapshot.md` puis drill : `audiences/{audience_slug}/profile.json` (voice.key_expressions[], psychology), `audiences/{audience_slug}/pain_points/*.json#verbatim_quotes[]`, `brand.json#brand_da` + `tone_of_voice`, `products/{product_slug}/spec.json#visual_identity` (assets_canonical : packshot, logo, charte).
- `resources/schemas/genome-package.schema.json` : le contrat cible. Lu EN ENTIER à la première invocation : le paquet doit produire exactement cette forme, `additionalProperties: false` à tous les niveaux (un champ improvisé = paquet invalide).

**Préconditions (refus doux, jamais de stub).**

- `frame.json` absent → le batch n'a pas de cadre. Surface : *"Ce batch n'a pas encore son cadrage (régime, mix de supports). Le move c'est de le poser d'abord, ~5 min, et on revient tisser."* Router vers frame-regime. STOP.
- Aucun `concepts/CPT-NN.json` avec `evaluation.approval_status: approved` → rien à incarner. Surface l'état des verdicts en clair (*"3 concepts en attente de validation, 1 rejeté"*) et router vers la chaîne d'évaluation (production des concepts candidats par produce-paid-angles, puis gate evaluate-concept porté par le flux). STOP. Ne JAMAIS incarner un concept non approuvé pour remplir le paquet, ne jamais invoquer evaluate-concept depuis ce skill.
- Angles sources introuvables → flag, continuer en mode dégradé (lineage.angle_id absent, tracé dans le recap), ne pas inventer un ANG-NN.

Calculer la ventilation supports pressentie (concepts × support_mix), les routes pressenties et le coût estimé → alimenter le disclosure ci-dessus. Afficher le disclosure. Attendre le OK.

---

## Step 1 · A7 · Incarnation par support (scaffold des scripts)

Pour chaque concept approuvé × chaque support qui lui est affecté dans le `support_mix` : scaffolder UN script. Allocation des ids : `GSC-01`, `GSC-02`, ... séquentiels dans le paquet (pattern `^GSC-[0-9]{2,4}$`, never reassigned, PAS de préfixe CRT : ce n'est pas une instance creative.json brand-side).

**Règles par support (la forme du schéma, if/then non négociables) :**

| Support | Frames | Timing | Spécifique |
|---|---|---|---|
| `static` | exactement 1 | aucun | le couple copy+visuel unique porte tout |
| `carousel` | 2+ (cartes swipe ordonnées) | aucun | chaque carte = 1 frame avec son role narratif |
| `video` | 2+ (plans ordonnés) | `timing.duration_s` OBLIGATOIRE par frame | `video_settings` OBLIGATOIRE au niveau script |

**`video_settings` (audio-led, D#476) quand support=video :**

- `language` : langue du script (BCP-47, ex `fr`), cohérente avec `copy_meta.language`
- `words_per_second_budget` : 2.2 FR posé. La VO de chaque plan doit tenir dans `duration_s × 2.2` mots. Déborde = couper des mots, jamais accélérer la voix.
- `master_aspect_ratio` : `9:16` (doctrine D#475 9:16-master/4:5-safe), cohérent avec `script.aspect_ratio`
- `voice_design_brief` : description texte FR de la voix, castée au perso (ex *"voix française 45 ans, chaleureuse, légèrement éraillée"*)
- `mux_never_shortest` : `true` (const, hard rule D#476)
- `captions_required` : `true` (const, 85% scrollent muet)
- `unify_grade_grain` : `true` recommandé (harmonise les plans IA multi-source)
- `estimated_cost_usd` : calculé (~$3.90 pour 15s / 5 plans : Nano Banana frame ~$0.12 + Seedance 1080p 5s ~$0.65/clip)

La vidéo est DÉCLARABLE dans le paquet (le schéma la porte entièrement) mais le bras de rendu n'est PAS câblé côté B (seul slot-1 image l'est, D#254). Conséquence : un script video est scaffoldé normalement ici, et sa route s'explicite au Step 3 (reco par défaut : Route B tant que les slots 3/4/5/6 ne sont pas branchés).

**Chaque frame = BI-FACE first-class (D#472).** Une frame couple TOUJOURS :

```json
{
  "role": "<un des 20 beat types analytiques>",
  "copy_script": { "vo_text | headline | overlay_text | body_text | cta_text": "..." },
  "visual_script": {
    "visual_concept": "ce qu'on montre + plan d'assemblage (composition, sujet, action, mood)",
    "style_id": "<style-registry, enum miroir reverse>",
    "first_frame_prompt": "prompt image prêt slot-1, full-bleed explicite (anti-letterbox D#475)",
    "char_ref_attached": true,
    "packshot_required": true
  },
  "timing": { "duration_s": 3 }
}
```

- `role` : vocab analytique du reverse, 20 termes, LE SEUL vocab de rôle (mirror exact `body_arc.beat_type`) : `hook`, `pain-litany`, `pain-amplification`, `authority-demolition`, `false-solution-rebuttal`, `mechanism-reveal`, `solution-direction`, `ingredients-pillars`, `competitor-comparison`, `product-reveal`, `product-specs`, `resolution-timeline`, `benefit-lifestyle`, `social-proof`, `scientific-claim`, `guarantee-statement`, `cta`, `disclaimer`, `transition`, `loop-callback`. La SÉQUENCE des roles = la signature structurelle qui apprend. L'ancien rôle `turn-xray` n'existe plus : c'est le flag `visual_script.is_xray_cutaway: true`.
- `copy_script` : MECE par support. Video → `vo_text` (la ligne dite, finit avant la coupe, montrer PUIS dire). Static/carousel → `headline`/`overlay_text`/`body_text`. Dernière frame role=`cta` → `cta_text`. Un plan muet b-roll = `copy_script: {}` présent mais vide (la présence de l'objet matérialise le couplage).
- `visual_script` : requis `visual_concept` + `style_id`. Le `style_id` sort de `resources/registries/style-registry.md` (+ fiches `resources/registries/styles/`), enum miroir du reverse. Si origin=reverse : remplir `ref_ad_as_image` ({ref_image_path, ref_ad_id, transfer_mode}) avec `transfer_mode: structure-only` par défaut (garde-fou surface-bleed D#474 : on copie le plan d'assemblage, JAMAIS les props de la ref). `packshot_required: true` sur toute frame qui montre le produit.
- "UNE idée = UNE frame = UNE respiration" (D#476) : la copy d'une frame finit avant la coupe ou le swipe. Une frame qui porte deux idées se splitte.

L'arc complet d'un script se construit depuis l'angle source : la formula OTRB de l'ANG-NN donne le squelette narratif (Observation → frames pain, Tension → amplification, Reframe → mechanism-reveal/solution-direction, Bridge → product-reveal/benefit/cta), le concept donne le parti-pris visuel, l'audience donne le registre.

---

## Step 2 · A8 · Tissage des hooks

Pour chaque script, la frame `role: hook` (toujours frames[0]) reçoit son hook first-class, dupliqué au niveau `script.hook` (le schéma le porte en first-class pour le routage diffusion + le test de hooks concurrents).

**Sourcing, dans cet ordre :**

1. **Registre cross-brand** `resources/registries/hooks/*.json` : si `regime.mode = exploit`, ne considérer QUE les fiches `promote_status: promote-ready`. Filtrer par la distance d'emprunt UNIQUE définie dans `resources/sops/creative-production/cross-brand-curation.md` : distance(pattern, marque) = 0 si la verticale de la marque ∈ `vertical_scope.origins` du pattern OU (`vertical_scope.breadth: universal` ET `promote_status: promote-ready`) · 1 si une origin est verticale VOISINE de la marque · 2 sinon. Ne garder que les patterns dont la distance <= `rayon_max` lu dans frame.json (top-level persisté : 0 exploit · 1 balanced · 2 explore). Tout emprunt à distance > 0 (pattern venu d'une autre verticale que celle de la marque) est SURFACÉ à l'opérateur dans le recap (*"hook emprunté au telehealth US, jamais vu sur ta verticale : pari mesuré"*), jamais glissé en silence.
2. **Canon copy** `resources/canon/copy/hooks/*` : les 6 familles d'ouverture canoniques, avec leurs `when_works[]` / `when_avoid[]` filtrés contre l'awareness_stage de l'angle source.
3. **Atlas brand** : verbatims réels de `audiences/{audience_slug}/profile.json#voice.key_expressions[]` et `audiences/{audience_slug}/pain_points/*.json#verbatim_quotes[]`.

**Construction du hook (objet schéma) :**

```json
{
  "mechanic_id": "<enum 25 valeurs, miroir reverse hook-mechanics>",
  "hook_text": "<VERBATIM réel sourcé atlas, ou squelette registre slotté avec matière réelle de la marque>",
  "hook_skeleton": "[squelette paramétrique de la fiche registre]",
  "visual": {
    "style_id": "<style-registry>",
    "visual_hook_description": "ce que montre le premier frame (le stop-scroll)",
    "first_frame_prompt": "prompt slot-1 prêt, full-bleed"
  }
}
```

**Mapping registre → enum (piège de nommage, la validation tranche).** Les fiches registre portent un `pattern_id` préfixé `HOK-` dont le nom diverge parfois de l'enum `mechanic_id` du schéma. L'ENUM DU SCHÉMA FAIT FOI (le paquet doit valider). Correspondances divergentes connues :

| Fiche registre | mechanic_id schéma |
|---|---|
| `HOK-category-of-one-reframe` | `category-of-one-claim` |
| `HOK-symptom-shock-question` | `rhetorical-shock-question` |
| `HOK-visceral-testimony` | `visceral-specific-testimony` |
| `HOK-resolution-promise-effortless` | `resolution-promise` |
| `HOK-if-then-conditional` | `if-then-conditional-hook` |
| `HOK-competitor-comparison` | `competitor-comparison-explicit` |

Les autres fiches mappent à l'identique (strip du préfixe `HOK-`). Une fiche sans correspondance enum → `other-uncategorized` + flag dans le recap (candidat extension enum, pas d'improvisation).

**Qualité, non négociable.** Chaque hook candidat passe `resources/quality-specs/hook-quality-spec.md` : Pattern Interrupt, Identification, Open Loop, Spécificité, Awareness Match, seuil >= 4/5. Sous le seuil → un retry avec une autre source d'ancrage, sinon DROP du candidat. Jamais de rafistolage pour passer le seuil.

**1 principal + 1-2 variantes.** Le swap de hook est le variant_axis le plus rentable du paid : chaque script sort avec son hook principal (sérialisé dans le paquet) ET 1-2 variantes qui passent le même seuil. Le schéma porte UN hook par script (`additionalProperties: false` interdit d'embarquer un tableau de variantes) : les variantes vivent dans le sidecar `brands/{slug}/creatives/{batch}/hook-bench.json`, hors contrat A→B, structuré `{script_id, variants: [{mechanic_id, hook_text, source, quality_score}]}`. C'est la matière première de recompose-creative pour le swap post-prod, et des `hook.visual.variant_index` concurrents si l'opérateur teste plusieurs first-frames sur un même tronc.

---

## Step 3 · Le fork Route A / Route B (micro-gate opérateur n°1)

Chaque script porte une `route` que B lira comme un gate : `route_a_full_ia` (compose-creative prend le relais, binaire généré, gate qc-creative avant tout spend) ou `route_b_export_brief` (export d'un brief humain : partenaire créa, UGC creator, motion designer · c'est AUSSI le chemin d'amorçage de l'asset-library, `production_status: export-to-human-route-b`).

**Proposer, par script, une route avec rationale court :**

- **Assets dispo** : packshot canonique présent + style photoréaliste simple → Route A solide. Asset-library `empty` + produit complexe → Route B amorce la library.
- **Support** : `video` → Route B par défaut TANT QUE le bras de rendu n'est pas câblé (slots 3/4/5/6 non branchés, D#254). Le script video reste entièrement déclaré dans le paquet (le contrat est prêt pour le jour où le bras se branche), mais le rendu passe par un humain aujourd'hui. Le dire tel quel à l'opérateur, sans enrober.
- **Coût** : Route A statics ~$0.12-0.25/image, carousel ~N cartes × $0.12. Annoncer le total AVANT confirmation (hard rule).
- **Deadline** : deadline serrée + assets prêts → Route A. Besoin d'authentique UGC → Route B sans débat.

**L'opérateur arbitre EN UN COUP pour tout le batch.** Présenter une table compacte (script · support · route reco · pourquoi · coût si A), une seule question, jamais script par script en interrogatoire. Chaque GSC-NN est TOUJOURS couplé à son libellé métier (le concept incarné, ex *"GSC-03 · Le secret du podologue (vidéo)"*) : un id nu ne dit rien à l'opérateur.

```
  Script                              Support    Route reco     Pourquoi                      Coût si full IA
  ───────────────────────────────────────────────────────────────────────────────────────────
  GSC-01 · Matins récupérés           static     full IA        packshot canon dispo,         ~$0.25
                                                                style studio simple
  GSC-02 · La chaussure du dimanche   carousel   full IA        5 cartes, charte posée        ~$0.60
  GSC-03 · Le secret du podologue     video      export brief   rendu vidéo pas branché ·     (humain)
                                                                brief UGC prêt à distribuer
  ───────────────────────────────────────────────────────────────────────────────────────────
  Tu valides ces routes, ou tu bascules lesquelles ?
```

La réponse opérateur fige `scripts[].route`. Un override opérateur contre la reco est respecté ET tracé (le rationale de la reco reste dans le recap).

---

## Step 4 · Locks (gouvernance créative D#472)

Les locks sont les contraintes dures que B doit TENIR sans les inventer. Trois blocs par script :

**`character_lock`** ·
- `brief` : description TONALE et de ciblage, JAMAIS physique (*"grand-mère chronic-pain, fatiguée mais digne"* ✓ · *"femme 52 ans cheveux gris yeux bleus 1m65"* ✗). Exception UNIQUE : mascotte récurrente en `consistency_strategy: lora-recurring-mascot`, où la précision physique EST le lock.
- `consistency_strategy` : `char-ref-attached-per-shot` (défaut video/carousel multi-frames : la char-ref se ré-attache par plan, flag `visual_script.char_ref_attached: true` sur les frames concernées) · `frame-chaining` (alternative) · `lora-recurring-mascot` (mascotte seulement) · `none` (pas de perso).
- `char_ref_id` : ref character-sheet si elle existe dans l'asset-library, vide sinon (= B la produit).

**`product_lock`** ·
- `packshot_ref` : chemin/URL du VRAI packshot scrapé ou validé (`products/{product_slug}/spec.json#visual_identity.assets_canonical.packshot_*`), JAMAIS halluciné (D#473 : un packshot se colle, ne se génère pas).
- `photoreal_exact` : `false` par défaut (reconnaissable-dans-le-style suffit), `true` SEULEMENT si le style de la frame est photoréaliste.
- **Micro-gate opérateur n°2 (flag-avant) :** si une frame porte `packshot_required: true` et qu'aucun packshot canonique n'existe dans `visual_identity.assets_canonical` ni dans l'asset-library → STOP avant sérialisation, question unique : *"Pas de packshot canonique pour {produit}. Je le scrape depuis {URL produit}, ou ce script passe en export brief ?"* Jamais sérialiser un `packshot_ref` vide sur un script route_a avec packshot requis sans cet arbitrage.

**`brand_charter_ref`** · pointeur vers la charte (`products/{product_slug}/spec.json#visual_identity`, fallback `brand.json#brand_da`). Le concept de ref S'ADAPTE à la charte, il ne s'y colle pas (D#473).

---

## Step 5 · Sérialisation genome-package + validation jsonschema BLOQUANTE

Construire l'objet conforme à `resources/schemas/genome-package.schema.json` v1.3. Forme racine STRICTE (`additionalProperties: false` : exactement ces champs, rien d'autre, pas de `_schema_version` ni de `batch_id` dans l'instance) :

```json
{
  "genome_version": "1.1.0",
  "mirror_of": "video-ad-analysis-v1.0.schema.json",
  "brand_slug": "{slug}",
  "generated_at": "{ISO 8601}",
  "origin": "{frame.json#origin.kind · reverse | scratch}",
  "regime": {
    "mode": "{frame.json#regime.mode}",
    "freedom_cursor": 0.3,
    "gauges": { "atlas_richness": "...", "perf_signal": "...", "asset_library": "..." }
  },
  "scripts": [ "..." ]
}
```

`genome_version` est un const `"1.1.0"` (version du CONTRAT, distincte de la version du fichier schéma) : toute autre valeur invalide le paquet.

**Projection depuis frame.json (stricte, forme frame/1.0) :** `regime.gauges` du paquet = UNIQUEMENT les 3 enums `{atlas_richness, perf_signal, asset_library}` lus dans les `gauges` TOP-LEVEL du frame, jamais `evidence` ni `computed_at` (additionalProperties:false les refuserait). `origin` (string du paquet) = `frame.json#origin.kind`. `lineage.ref_ad_id` (par script, si reverse) = `frame.json#origin.reference_ad`. `rayon_max` se lit persisté au top-level du frame, jamais re-dérivé du curseur.

**Par script, assemblage des champs (cœur requis en premier) :**

| Champ | Source | Règle |
|---|---|---|
| `script_id` | alloué Step 1 | `GSC-NN`, séquentiel, never reassigned |
| `support` | support_mix | static/carousel/video |
| `route` | arbitrage Step 3 | figé par l'opérateur |
| `hook` | tissage Step 2 | principal seulement (variantes → hook-bench) |
| `frames[]` | scaffold Step 1 | if/then support respectés (1 / 2+ / 2+ avec timing) |
| `genome_tags` | dérivation ci-dessous | le pont A=B |
| `aspect_ratio` | `9:16` défaut | cohérent `video_settings.master_aspect_ratio` si video |
| `video_settings` | Step 1 | REQUIS si support=video, absent sinon |
| `lineage` | concept + angle source | `{concept_id, angle_id, ref_ad_id?, persona_label, anti_generic_passed}` |
| `locks` | Step 4 | character_lock + product_lock + brand_charter_ref |
| `copy_meta` | transverse script | `language`, `compliance_disclaimers_required[]` (hérités de l'angle/verticale, enum miroir reverse), `anti_surface_bleed_note` si origin=reverse |
| `required_assets[]` | dérivé frames | liste pré-résolue contre les 8 capability slots · `to-generate` (route A) / `exists-in-asset-library` / `export-to-human-route-b` (route B) · `frame_index` relie chaque asset à sa frame |

**`genome_tags`, dérivation mécanique (jamais à la main) :**

- `support` : recopie de `script.support`
- `mechanic_id` : recopie de `hook.mechanic_id`
- `primary_style_id` : le style_id dominant des `frames[].visual_script` (le plus fréquent, hook prioritaire à égalité)
- `beat_type_sequence` : **PROJECTION EXACTE 1:1 de `frames[].role`, dans l'ordre.** Construite par code (`[f["role"] for f in frames]`), jamais rédigée. C'est le fix dual-vocab v1.1 : la timeline que B construit EST la signature qui apprend.
- `mecanique_id` : le concept ad-level si mappable à `resources/registries/creative-mechanics-registry.md` (distinct du mechanic_id HOOK)
- `angle_id` + `audience_slug` : dénormalisés depuis lineage (D#492, jointure perf plate)
- `awareness_level` : hérité de l'angle source (`lineage.awareness_stage`)
- `regime_at_generation` : recopie de `regime.mode` (ou `regime_override` script si posé)
- `atlas_link_status` : `linked` si hook + pains sourcés atlas, `new-to-atlas` sinon

**Validation jsonschema, ICI, bloquante (D#479 : l'enforcement vit dans la skill, pas dans le gate).** Draft du paquet dans `/tmp/genome-package-{batch}.json`, puis :

```bash
python3 - <<'PY'
import json, sys
from jsonschema import Draft7Validator
schema = json.load(open("resources/schemas/genome-package.schema.json"))
pkg = json.load(open("/tmp/genome-package-{batch}.json"))
errors = sorted(Draft7Validator(schema).iter_errors(pkg), key=lambda e: list(e.absolute_path))
for e in errors:
    print("✗", "/".join(map(str, e.absolute_path)) or "(root)", "·", e.message[:160])
# Vérification d'identité beat_type_sequence == frames[].role (1:1, ordre inclus)
for s in pkg.get("scripts", []):
    seq = s.get("genome_tags", {}).get("beat_type_sequence")
    roles = [f["role"] for f in s.get("frames", [])]
    if seq is not None and seq != roles:
        errors.append(True)
        print("✗", s.get("script_id"), "· beat_type_sequence != projection de frames[].role")
sys.exit(2 if errors else 0)
PY
```

Exit 2 = paquet invalide → CORRIGER et re-valider. La skill REFUSE de sérialiser un paquet invalide : pas d'écriture brand-side, pas de "je l'écris quand même et on verra". Erreurs récurrentes à chasser : champ hors `additionalProperties`, enum hors miroir (mechanic_id/style_id/beat_type), video sans `video_settings` ou frame video sans `timing`, static avec 2 frames, `genome_version` ≠ "1.1.0".

**Écriture (mode direct, canal canonique) :**

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/creatives/{batch}/genome-package.json" \
  --value "$(cat /tmp/genome-package-{batch}.json)" \
  --source agent --confidence 0.9 --mode direct \
  --reason "Genome package batch {batch} · {N} scripts · A7+A8 weave-hooks"
python3 .skills/write-to-context.py --path "brands/{slug}/creatives/{batch}/hook-bench.json" \
  --value "$(cat /tmp/hook-bench-{batch}.json)" \
  --source agent --confidence 0.9 --mode direct \
  --reason "Hook variants bench batch {batch} · swap downstream"
```

`--mode direct` assumé : le gate refuse le proposed fichier-entier, et un stamping `_proposed` casserait `additionalProperties: false` du genome-package. La validation humaine est portée par les gates du flux (disclosure NIVEAU 0 + micro-gates routes/packshot), pas par un stamping.

Puis fermer la boucle mutation :

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Exit code 2 = blocking → réviser avant le recap opérateur. Non skippable.

---

## Step 5bis · Émettre l'event coherence_check (obligatoire, avant le close)

```bash
python3 .skills/emit-event.py \
  --kind coherence_check \
  --payload '{"brand_slug":"{slug}","batch":"{batch}","n_scripts":{N},"valid":true}'
```

Émis APRÈS validation jsonschema (exit 0) + écriture + finalize, AVANT le recap opérateur (modèle qc-creative Step 8). `valid` reflète le résultat de la validation Step 5 (toujours true au moment de l'émission : un paquet invalide ne s'écrit pas, donc n'émet pas). Skipper = le hook traite le paquet comme non vérifié.

---

## Step 6 · Close opérateur (investigation-posture compacte + next-step unique)

Recap en langue opérateur, format compact. Jamais de field paths, jamais de noms de skills, jamais de scores hook exposés. Tout GSC-NN cité est couplé à son libellé métier (*"GSC-03 · Le secret du podologue (vidéo)"*), jamais un id nu.

```
Paquet de prod prêt · {batch} · {N} scripts
─────────────────────────────────────────────
  ✓ {n_static} statics · {n_carousel} carousels · {n_video} vidéos
  ✓ Routes : {n_a} full IA · {n_b} export brief
  ◐ Coût génération full IA : ~${X} ({détail})
  ⚠ {flags s'il y en a : emprunt cross-verticale sur GSC-03 · Le secret
     du podologue · packshot scrapé à valider · 1 hook candidat droppé
     sous le seuil}

  ✓ complet  ◐ partiel  ○ vide  ✗ absent  ⚠ critique
```

Puis les 5 sections, version compacte (2-3 lignes chacune, prose) :

- **Observé** · ce qui est ancré : N hooks sur verbatims réels de ta voix client, M sur patterns confirmés multi-marques · packshot et charte sourcés du canon.
- **Déduit** · les choix portés en hypothèse : routes recommandées (avec les overrides opérateur notés), emprunts cross-verticale signalés un par un avec leur origine (*"le hook de GSC-03 · Le secret du podologue vient du telehealth US, jamais testé sur ta verticale"*), confiance héritée de l'angle source quand elle est faible.
- **Inconnu** · ce que seul le terrain dira : la perf réelle de chaque hook (les variantes benchées servent exactement à ça), le rendu IA sur les scripts full IA avant le gate qualité.
- **Leviers** · ce qui est prêt à tirer : génération des scripts full IA (gate qualité avant tout spend inclus), distribution des briefs export, swap de hook si un principal fatigue.
- **Close ouvert** · UN next-step contextuel, jamais un menu plat :
  - Si `n_a > 0` : *"Je lance la génération des {n_a} scripts full IA maintenant ? Coût ~${X}, et rien ne part en spend sans le gate qualité."* (routage interne : compose-creative sur chaque script route_a, qui invoque qc-creative.)
  - Si route B uniquement : *"Je prépare les {n_b} briefs d'export pour distribution ? L'envoi suit ta préférence de distribution habituelle."* (sans nommer d'outil en dur : l'export suit `operator/profile.json#context.stack[]` et la préférence per-brand `brands/{slug}/config.json#preferences.brief_distribution` · `workspace_only` = les briefs restent dans le workspace, demandé une fois par marque.)
  - Si flags bloquants restants (packshot à valider) : le next-step est la levée du flag, pas la génération.

---

## Hard Rules

- **Never sérialiser un genome-package qui échoue la validation jsonschema.** Exit 2 au Step 5 = pas d'écriture brand-side, correction puis re-validation. L'enforcement vit ICI, pas dans un gate aval (D#479). Aucune exception, y compris sous deadline opérateur.
- **Always `beat_type_sequence` = projection 1:1 de `frames[].role`.** Construite par code, vérifiée par le check d'identité explicite du Step 5 (ordre inclus). Un écart = paquet invalide, même si le jsonschema seul laisserait passer.
- **Never un `hook_text` inventé.** Verbatim réel de l'atlas ou squelette du registre slotté avec matière réelle de la marque, source tracée dans hook-bench. Un hook sans source vérifiable ne sort pas, quelle que soit sa qualité apparente.
- **Always surfacer les emprunts cross-verticale (distance > 0).** Tout pattern venu d'une autre verticale que celle de la marque est nommé à l'opérateur avec son origine, dans le recap ET au moment du tissage. Jamais d'emprunt silencieux.
- **Never de précision physique dans un `character_lock.brief`.** Brief tonal et de ciblage uniquement. Exception unique : `consistency_strategy: lora-recurring-mascot`, où le physique EST le lock.
- **Always cost-warning avant Route A sur video ou volume.** Le coût estimé total s'annonce au disclosure ET se re-confirme au fork Step 3 avant de figer les routes. Jamais de génération confirmée sans chiffre annoncé.

---

## Cross-references

- `resources/schemas/genome-package.schema.json` (v1.3) · LE contrat cible. Lu en entier à la première invocation. Ce skill est son producteur unique côté A.
- `.skills/skills/compose-creative/SKILL.md` · downstream Route A : consomme les scripts `route_a_full_ia`, génère les binaires, invoque qc-creative avant spend-eligible.
- `.skills/skills/recompose-creative/SKILL.md` · downstream variantes : consomme `hook-bench.json` pour le swap de hook sur créas existantes.
- `.skills/skills/qc-creative/SKILL.md` · gate de sortie sur les binaires rendus (pas sur ce paquet : ici le gate est la validation jsonschema).
- frame-regime (skill amont, même vague) · produit `brands/{slug}/creatives/{batch}/frame.json` forme frame/1.0 (regime, gauges top-level, support_mix, origin.kind + origin.reference_ad, rayon_max persisté). Précondition dure de ce skill.
- evaluate-concept (skill amont, même vague) · retourne ses verdicts au flux, qui les persiste dans `brands/{slug}/creatives/{batch}/concepts/CPT-NN.json#evaluation`. Seuls les `evaluation.approval_status: approved` s'incarnent. weave-hooks n'invoque pas ce gate : il exige des concepts déjà gatés.
- `.skills/emit-event.py` · canal d'audit (Step 5bis, kind coherence_check).
- `resources/registries/hooks/*.json` + `resources/registries/hooks/README.md` · bibliothèque cross-brand des patterns hook (promote-ready = >= 2 sources indépendantes).
- `resources/sops/creative-production/cross-brand-curation.md` · fonction de distance d'emprunt UNIQUE (vertical_scope.origins + breadth + promote_status, comparée au rayon_max persisté du frame).
- `resources/canon/copy/hooks/*` · familles d'ouverture canon copy (when_works / when_avoid).
- `resources/quality-specs/hook-quality-spec.md` · test 5 critères, seuil 4/5, non négociable.
- `resources/registries/style-registry.md` + `resources/registries/styles/` · fiches style_id (enum miroir reverse).
- `resources/registries/creative-mechanics-registry.md` · mécaniques ad-level (`genome_tags.mecanique_id`, distinct du mechanic_id hook).
- `.skills/write-to-context.py` · canal de mutation canonique (écriture du paquet + du bench, mode direct · le stamping proposed fichier-entier casserait additionalProperties:false).
- `.skills/finalize-mutation-batch.py` · primitive de clôture mutation, obligatoire avant le recap.
- `docs/system/engagement-disclosure-doctrine.md` + `docs/system/decomposition-visibility-doctrine.md` · canon du disclosure NIVEAU 0 pré-runtime.
- `docs/system/investigation-posture.md` · forme du close Step 6 (5 sections compactes, close ouvert).
- D#472 (BI-FACE, locks, régime) · D#473 (concept visuel, packshot réel, ref en image) · D#474 (surface-bleed) · D#475 (9:16-master, char-ref par plan) · D#476 (audio-led) · D#477 (fusion A7+A8) · D#479 (enforcement dans la skill) · D#254 (8 capability slots, seul slot-1 câblé) · D#492 (angle_id/audience_slug dénormalisés).
