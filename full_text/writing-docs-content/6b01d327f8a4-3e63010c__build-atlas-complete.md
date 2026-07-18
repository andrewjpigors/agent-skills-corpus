---
name: build-atlas-complete
type: orchestrator
version: "1.20.0"
recommended_model: sonnet
reasoning_pattern: null
mode: proposed
operator_facing: true
subagent_safe: false
isolation_scope: brand_only
layer: territoire
extension_hooks:
  - audience_entity
  - angle_entity
  - creative_entity
  - brief_entity
  - territory_entity
  - product_entity
  - friction_entity
description: >
  v1.18.0 (D#520 · beat de restitution sur toutes les frontières de phase) · l'orchestrateur émet désormais le beat décision-d'abord à CHAQUE frontière (scan déjà câblé · `--mode orchestrated` rendu explicite · audiences fin Phase 3 · spectrum Step 2.5 · angles Step 6) via `render-beat.py --mode orchestrated`, présenté tel quel (jamais re-narré), avec filet fail-open → repli prose. Au CLOSE (Step 9), build-atlas est LE producteur · il écrit lui-même `.phantom/beats/{slug}/close.json` (verdict global tranché · lecture 5-axes · top-3 axes prioritaires · inconnus-avec-levier · vue atlas · terminal sans forward-look mais tease = prochaine action opérateur) puis l'émet. Doctrine SSOT `docs/system/restitution-beat-doctrine.md`. Backward compat strict additif, zéro logique de gate/délégation altérée.
  v1.8.0 (Spectre C6 · D#502/D#506) · NEW palier spectre (Step 2.5) inséré entre Gate Intermédiaire 1 (produit validé) et Phase 3 (map-audiences), topologiquement correct (mécanisme → usages → audiences). DEUX NATURES (D#506) · (a) énumération mécanisme→usages TOUJOURS active (délègue à map-audiences mode spectre F1 → spec.use_cases[] peuplé AVANT la dérivation d'audiences) · (b) carte complète CONDITIONNELLE (spectre_mode auto/proposed/off décidé au Step 0 depuis brand.meta.stage + régime · délègue à map-angles mode spectre → spectrum.json). 3 moments · launch/explore-dominant → auto · établi → proposé (gate light) · contre-cas → off si mur dominant ≠ MARCHÉ (consulte la doctrine `docs/doctrine/strategic-diagnostic-doctrine.md` d'abord). Pure orchestration, délègue tout (purity rule). Branche conditionnelle, jamais en dur (préserve le chain 4 paliers + --fast-track). Backward compat strict additif.
  v1.7.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution (entre disclosure pré-runtime NIVEAU 0 et chain Steps 1-10). Action LOURDE orchestrateur · narratif étendu 2 niveaux abstraction (macro brand entière + micro chaînes audiences/angles cross-encoded en prose) pendant handoffs sub-skills. Pose pair senior expert · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  v1.7.0 (v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés) · Section pré-runtime étendue · NIVEAU 0 ajouté en complément du disclosure plan/ETA/implication/livrable v2.79.3 existant · expose 6 paramètres décomposés au runtime (scope cartographier · profondeur cible · audiences à profiler · angles à générer · hypothèses figées · biais à éviter) avec POURQUOI chacun + close binaire OK ou ajuste · adapté au cycle 7 phases orchestrateur. Cross-ref doctrines decomposition-visibility-discipline + engagement-disclosure-discipline v2.79.5+. Backward compat strict additif (Phases 1-9 runtime preserved · seul l'amont disclosure enrichi).
  v1.6.0 (v2.78.2 decomposition visibility refactor) · NEW Phase Output Atlas Visibility Matriciel Multi-niveau obligatoire post-encoding entités (avant Step 9 Close) · 4 niveaux canon obligatoires (Décomposition produit cross-products · Many-to-many pain × audience matrix cross-atlas · Positionnement filtre par stage business · Méthode pédagogique verbale). Cross-ref doctrine `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2. Distinction explicit audience produit-fit (toutes encoded) vs audience ciblage créa (filter sub-set positioning targeting). Backward compat strict additif (Phases 1-7 + Step 8 stage + Step 9 close preserved · NEW phase output insérée entre Step 8 et Step 9). HR-NEW + AP-NEW ajoutés guardrails.
  v1.4.0 (v2.68 progressive cartography refactor) · chain orchestrator avec gates light entre paliers progressive (Phase 1+2 snapshot-brand · gate intermédiaire 1 · Phase 3 map-audiences hiérarchique parent/enfants · gate intermédiaire 2 · Phase 4 mine-voc + profile-audience enrichissement per audience). Mode `--fast-track` opérateur expert bypass gates auto-validate (opt-in flag OR config `auto_validate_after_n_brands` true). Validation operator entre chaque palier territoire (vs dump synthesis bloc canon précédent v1.3.0 où gates étaient Gate A audiences + Gate B angles seulement). Cross-ref doctrine `docs/system/progressive-cartography-doctrine.md` NEW v2.68. Backward compat strict additif sur chain skills (Steps preserved · gates additifs light · fast-track flag opt-in default off · gates A+B angles preserved après Phase 4).
  v1.3.0 (v2.67 territoire-pure refactor) · Steps 8-9 stripped (produce-copy-brief + compose-creative) · align doctrine `docs/system/territory-doctrine.md` shipped v2.67. Orchestrator scope = territoire substrat only · productions briefs+créas via `creative-brief-composer` post-atlas downstream (separate skill, separate invocation). Output explicite · complete strategic atlas substrate (specs + offers + audiences + angles + territoires scorés). BREAKING · operators v1.x qui invoquaient pour briefs+créas doivent invoquer `creative-brief-composer` post-`build-atlas-complete`. Migration documentée CHANGELOG v2.67.0. Backward compat strict additif sur Steps 1-7 unchanged (territoire chain preserved).
  v1.2.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience + frictions sub-product) · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans sub-parent locations · `audiences/{a_slug}/pain_points/` + `audiences/{a_slug}/objections/` + `products/{p_slug}/frictions/` (owned natif par parent path). Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.1.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · Phase 3 deepen-brand-context (chain mine-voc + mine-vom) écrit désormais dans 3 collections séparées (`pain_points/` + `objections/` + `frictions/`) plus `profile.json` clean (identity + psychology + voice + behavior + decision_process restent · pain_points + objections sub-fields legacy supprimés post-v2.63 nouvelles brands). Backward compat preserved (pre-v2.63 brands route fallback profile sub-fields legacy).
  v1.0.2 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (dtc-operator-playbook, audiences-cartography, angle-anatomy, hooks-method, breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  Full-cycle atlas substrate builder. Chains the territoire canon pipeline end-to-end on a
  blank or partially-built brand to produce the complete strategic atlas substrate
  (specs + offers + audiences + angles + territoires scorés) from a single operator intent.
  Single chairman orchestrating specialized skills with explicit gates between phases.
  Resolves the Scenario 4 orchestration gap surfaced in Phase 1 audit, so the agent never
  freestyles strategic prose to fill a multi-skill atlas request.
  FR: "génère l'atlas complet de {brand}", "build atlas {brand}", "lance le pipeline complet", "construis tout pour {brand}", "atlas complet from scratch".
  EN: "build complete atlas", "generate full atlas {brand}", "build everything for {brand}", "run full pipeline", "full atlas from scratch".
permissions:
  reads: [brand, product, offer, profile, learning, strategy]
  writes: [brand, product, offer, profile, learning, strategy]
  emits_events: [coherence_check, atlas_substrate_staged]
consumes:
  - brands/{slug}/brand.json
  - resources/schemas/spec.schema.json
  - resources/schemas/profile.schema.json
  - resources/schemas/angle.schema.json
  - resources/schemas/roadmap.schema.json
  - resources/catalogues/heuristiques-persuasion.json
  - resources/catalogues/niveaux-schwartz.json
  - resources/catalogues/formats-livrables.json
  - resources/catalogues/hooks.json
  - resources/catalogues/angles.json
  - path: docs/system/progressive-cartography-doctrine.md
  - path: docs/system/decomposition-visibility-doctrine.md
  - path: docs/system/territory-doctrine.md
  - path: docs/system/investigation-posture.md
  - path: docs/system/pain-benefit-chain.md
  - path: docs/doctrine/dtc-operator-playbook.md
  - path: docs/doctrine/audiences-cartography-doctrine.md
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/system/output-clarity-doctrine.md
  - path: docs/system/operator-vocabulary-translation.md
produces_proposals_for:
  - brands/{slug}/spec.json
  - brands/{slug}/products/*/offers.json
  - brands/{slug}/audiences/*/profile.json
  - brands/{slug}/audiences/*/pain_points/*.json
  - brands/{slug}/audiences/*/objections/*.json
  - brands/{slug}/products/*/frictions/*.json
  - brands/{slug}/pain_points/*.json (legacy v2.63 backward compat)
  - brands/{slug}/objections/*.json (legacy v2.63 backward compat)
  - brands/{slug}/frictions/*.json (legacy v2.63 backward compat)
  - brands/{slug}/angles/*.json
  - brands/{slug}/strategy.json
  - brands/{slug}/scoring/matrix-{date}.json
pipeline:
  preconditions: operator provides brand_slug AND (URL OR snapshot already completed). MCP tools available (facebook-graph optional, Notion optional).
  postconditions: |
    - brand structure fully populated across spec, offers, profile(s), angles
    - score-matrix territories ranked, top 3 axes créatifs selected
    - territories staged as proposals, ready for downstream production via creative-brief-composer (separate skill, separate invocation)
    - status.json updated, snapshot rebuilt, finalize-mutation-batch event emitted
    - learn-from-session flush proposed at end
disambiguates_against:
  onboard-brand: "route to onboard-brand when operator wants only the structural setup + snapshot + integrity check (no audiences/angles/briefs/créas). onboard-brand stops at the 'context loaded' gate."
  deepen-brand-context: "route to deepen-brand-context when operator wants only VoC + VoM mining on a snapshotted brand (no audiences/angles/briefs/créas downstream)."
  setup-brand: "route to setup-brand for initial identity/structure only."
  snapshot-brand: "route to snapshot-brand for URL scrape only on an existing brand."
  profile-audience: "route to profile-audience standalone when operator wants audiences only, not the full strategic atlas."
  score-matrix: "route to score-matrix standalone when atlas is already populated and operator wants only territory prioritization."
---

# Skill: build-atlas-complete

**CRITICAL:** this is an **Orchestrator**. **YOU MUST NEVER** re-implement setup-brand, snapshot-brand, map-audiences, mine-voc, profile-audience, weight-dimensions, produce-paid-angles, or score-matrix logic here. **YOU MUST** delegate to each existing skill in sequence via Task tool (when the subskill is `subagent_safe: true`) or inline invocation (when `subagent_safe: false`). Any deviation breaks the canon purity rule established by `onboard-brand`. **Scope v1.4.0 progressive cartography** · 4 paliers chain skills avec gates light entre paliers (`docs/system/progressive-cartography-doctrine.md` NEW v2.68) + Gate A audiences + Gate B angles preserved + mode `--fast-track` opérateur expert bypass gates intermédiaires (opt-in). **Scope v1.3.0 territoire-pure preserved** · productions briefs+créas post-atlas via `creative-brief-composer` (separate skill, separate invocation). Voir `docs/system/territory-doctrine.md`.

## Tone

Chairman orchestrating a territoire substrate pipeline that produces the complete strategic atlas substrate. Narrate each handoff in one operator-facing sentence ("structure prête… snapshot lancé… audiences cartographiées, deux gates devant nous… angles ranked…"). Operator never reads skill names, paths, field paths, scoring numbers, or Task tool mechanics. The pipeline is long (30-90 min depending on density), so heartbeat at each gate is non-negotiable.

**Exception · le beat de restitution (D#520).** Une phase qui a abattu un travail lourd et invisible (le deep-scan · ~97 outils, des sources lues, des pistes rejetées) ne se narre PAS en une phrase · elle se RESTITUE en un beat **décision-d'abord** (verdict tranché + second ordre, le raisonnement, ce qui reste prudent, le CTA `/phantom` teasé), rendu mécaniquement par `render-beat.py` depuis le registre que le sous-agent a déposé pendant que son contexte était frais. La règle « une phrase par handoff » vaut pour les transitions légères, jamais pour masquer le travail derrière une météo (« la carte est posée »). **Montrer le travail n'est pas exposer la mécanique** · ce sont les faits trouvés, les rejets argumentés, la confiance-avec-sa-cause · jamais les noms de skills, les chemins ou les scores bruts. Un run mérite son salaire, il ne lit pas le bulletin.

**Registre · pair-expert qui tranche, pas concierge (D#519).** Le ton dur-spécifié à la porte (`/tour` · « confiance sans hyperbole, zéro réassurance de coach, économie, le coup sec qui imprime ») se TIENT sur TOUTE la cascade d'encodage · c'est là, sur la longueur, qu'il se dilue et que le runtime dérive vers le concierge poli (observé run onday). Le report d'une étape est un FAIT posé sec, pas une consolation. La confiance vient du rythme et de la précision, jamais du rassurement · le heartbeat tranche, il ne berce pas. BANNI dans le fil d'encodage · « jamais perdu », « je te ping », « petite note d'honnêteté », « le moment où ça arrête d'être une démo », toute réassurance de coach ou punchline de vente. Le close tranche un verdict (cohérent close D#517 · « tranche quand les lectures convergent »), il ne rassure pas.

---

## Engagement disclosure pré-runtime · canon v2.79.3 + NIVEAU 0 v2.79.5

Avant de lancer l'orchestration, expose ce disclosure à l'opérateur en DEUX phases successives (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.3 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5).

**Phase A · NIVEAU 0 paramètres décomposés (v2.79.5)** · expose les paramètres décomposés que l'orchestrateur va mobiliser. Build-atlas-complete est le skill orchestrateur le plus complexe du canon (7 paliers · 30-90 min · MCP optionnel · gates intermédiaires + Gate A + Gate B). Disclosure NIVEAU 0 obligatoire AVANT le plan/ETA pour que l'opérateur ajuste un paramètre racine (scope · profondeur · cardinalité audiences/angles) avant de brûler 30+ min.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Scope cartographier
     {brand entière (default · all 7 phases) OR scope partiel
     (audience X + angle Y) OR scope mère + sous-poches uniquement}
     POURQUOI · {ex "premier cycle atlas brand · scope complet"
     OR "atlas brand déjà cartographié 80% · refresh partiel
     2 audiences" OR "operator explicit demand subset"}

  2. Profondeur cible
     {substrate light (hypothèse confidence 0.5 valide · doctrine
     progressive-cartography v2.68) OR sourced (5+ verbatims par
     pain canonical · mine-voc enrichissement complet) OR mixte
     (mère sourced + sous-poches light)}
     POURQUOI ce niveau · {ex "premier cycle, hypothèse sourceable
     downstream · progressive cartography" OR "brand mature à
     scale · exige sourced complet pour producer paid"
     OR "MCP signals limités, hypothèse pragmatique"}

  3. Audiences à profiler
     {N audiences · default 3-5 mère + 2-4 sous-poches par mère ·
     cap Phase 6 top-3 par défaut}
     POURQUOI ce nombre · {ex "audience tree 4 mères posées Phase 3,
     enrichissement top-3 par density signal" OR "operator demand
     explicit N audiences" OR "MCP Reddit + Trustpilot mince ·
     scope reduit"}

  4. Angles à générer
     {N par audience · default top-5 angles ranked produce-paid-angles ·
     cap Phase 7 top-3 axes créatifs}
     POURQUOI cette variance · {ex "5 angles ranked par audience
     top-3 puis dédoublonnés cross-audience cluster-deduplication ·
     top-3 axes créatifs sélectionnés" OR "brand mature ·
     scope reduit top-3 angles top audience pour itération
     focus"}

  5. Hypothèses figées
     Positioning canvas en place · {OUI lu brand.json#positioning
     OR NON · canvas inféré spec.market_context + competitors
     ou propose-positioning-canvas suggéré post-atlas}
     Voice 4D définie · {OUI brand.json#tone_of_voice complet
     OR NON · voice inférée + flag inconnu Investigation Posture}
     Territoire whitespace identifié · {OUI lu brand.market.white_spaces
     OR NON · whitespace dérivé Phase 7 score-matrix · top axes
     créatifs = territoires whitespace par construction}

  6. Biais à éviter
     · Sur-engineering atlas premier cycle (encoder 8 audiences ×
       7 angles = 56 angles · canon = top-3 audience × top-5 angles
       puis cap top-3 axes · scope discipline territory-discipline
       v2.67)
     · Cartographier sans données (lancer Phase 6 angles avant
       Phase 4 mine-voc · canon HR4.5 verbatim density floor
       gate strict)
     · Skip phases (sauter Phase 3 map-audiences pour gagner
       temps · audiences inférées sans framework 4 questions =
       audience tree fragile · canon progressive-cartography v2.68
       refuse skip)

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je passe
  au plan + ETA ?
```

ATTENDS confirmation explicite Phase A avant d'enchaîner Phase B (plan + ETA + implication + livrable v2.79.3). Si opérateur ajuste un paramètre racine (ex "scope partiel 2 audiences" OR "profondeur sourced obligatoire"), recalibrer le plan + ETA en conséquence avant Phase B.

**Phase B · disclosure plan + ETA + implication + livrable (v2.79.3 preserved)** ·

```
Build atlas complet · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Structure brand + scan site (palier 1+2 · setup + snapshot)
  2. Cartographie audiences hiérarchique mère + sous-poches (palier 3)
  3. Enrichissement voix client par audience (palier 4 · mine-voc + profile)
  4. Pondérations dimensions audience × angle + angles paid ranked
  5. Scoring matrice brand-wide · top axes créatifs sélectionnés
  6. Synthèse Atlas Visibility Matriciel 4 niveaux canon
  7. Close Investigation Posture · handoff briefs+créas downstream

  ETA           ~30-90 min (selon densité audiences + signal disponible)
  Implication   tu valides aux gates intermédiaires + Gate A audiences + Gate B angles
  Livrable      atlas substrat complet (specs + offers + audiences enrichies + angles ranked + territoires scorés) prêt pour creative-brief-composer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite Phase B avant de lancer Step 0. Court-circuit (Phase A + Phase B) autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set ou si opérateur a flag `--no-disclosure` explicit OR si N usages successifs >= seuil expert (`auto_skip_after_n_calls` true). Sinon · disclosure 2 phases obligatoire canon v2.79.3 + v2.79.5.

Cross-ref doctrines racine `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5.

---

## Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ · orchestrateur 7 paliers · 30-90 min · gates intermédiaires + Gate A + Gate B). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement disclosure pré-engagement NIVEAU 0 en amont et Phase Output Atlas Visibility matricielle (NIVEAUX 1-4) en aval.

Pattern obligatoire · l'agent chairman verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique la brand entière et orchestre les handoffs sub-skills, en prose narrative sobre (zéro matrice ASCII en LIVE · les matrices viennent en Phase Output Atlas Visibility post-Step 8).

**Ordre de lecture canon · la chaîne experte (`docs/doctrine/strategic-diagnostic-doctrine.md`).** Le NIVEAU LIVE macro OUVRE par la lecture de l'échiquier, pas par le produit · où {brand} est sur le spectre de sophistication, ce que les concurrents disent tous et le silence exploitable, AVANT de dériver qui elle vise. L'ordre est position → négatif → audiences-dérivées-du-mécanisme → priorité-imposée-par-l'éco → verdict, chaque maillon fermant le suivant. Dériver les audiences avant d'avoir lu la position, ou les tirer du miroir des avis, est l'anti-pattern banni (listing miroir-des-avis · `audiences-cartography-doctrine` Pitfall 8). Quand les lectures convergent, le close TRANCHE le verdict de positionnement, il ne le laisse pas en question ouverte.

**2 niveaux d'abstraction obligatoires** ·

1. **Macro brand entière** · verbaliser la compréhension du périmètre stratégique global AVANT de rentrer dans le détail palier par palier.
   Exemple build-atlas-complete · "On part d'une brand qui s'adresse à {audience macro depuis brand.json existing ou snapshot}, qui opère sur {marché × stade Schwartz inféré sophistication}, qui propose {portfolio produits N hero + secondaires + entries détectés}. Le pattern catalogue cohérent · {hero positionne sur axe X · secondaires drainent vers Y · entries servent porte d'entrée Z}. Le business model est {DTC pure / subscription / hybrid} parce que {signaux scrape + offers encoded}. Mon hypothèse de territoires créatifs candidats à scorer · {3-5 axes potentiels visibles depuis specs × audiences mère}. Les angles vont probablement se cristalliser autour de {tension principale brand × pain audience-hero détecté reviews tagged Phase 2}."

2. **Micro chaînes audiences/angles cross-encoded phrasé** · verbaliser les chaînes parent/enfants + angle-fit pendant l'orchestration palier par palier.
   Exemple build-atlas-complete · "Cette audience-mère {nom · cardinality broad} se découpe en {N sous-poches détectées · entry doors distinctes · pain × consequence × deep chain phrasé} → pour chaque sous-poche · pain prioritaire {PNT-NN nom phrasé} → mécanisme reframe candidat {angle-formula Obs+Tension+Reframe+Bridge phrasé} → bénéfice 3 couches qui cible {functional · emotional · identity phrasé pourquoi cette couche dominante audience-side} → angle ranked top {score qualitatif phrasé · pas chiffre brut} → territoire créatif qui cristallise {axe macro phrasé · cohérent positioning brand}."

**Calibration narrative** · prose sobre · registre pair senior expert chairman · zéro jargon plumbing (jamais `score-matrix#axe_id`, `angle.lineage.pain_ref`, `_field_types`, Task tool mechanics en LIVE) · zéro tableau ASCII en LIVE (matrices = Phase Output Atlas Visibility post-Step 8 + Step 9 close). Adapter le tonal au registre opérateur détecté (grounded · standard · dense). Le narrating chairman entre paliers reste préservé (cf section Tone "structure prête… snapshot lancé… audiences cartographiées…") · le NIVEAU LIVE l'enrichit en thinking aloud expert substantif spécifique au cas brand, pas seulement transition de phase.

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger entre handoffs sub-skills si l'agent part dans une mauvaise direction d'inférence (mauvaise audience-hero priorisée · mauvais angle-fit détecté · mauvais territoire candidat émergent) AVANT que les paliers downstream consomment 30+ min, (b) pédagogie · il apprend la posture stratégique experte chairman en regardant la manière de penser un atlas paid DTC end-to-end (macro positioning → audiences cartography → angles cristallisés → territoires scorés cohérents).

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

---

## Bandeau de position · accompagnement du parcours (v1.13.0)

L'opérateur ne doit jamais valider une boîte noire qui déroule. À chaque sortie de phase, le rendu PRÉFIXE le no-orphan-output (les deux gestes) par une ligne de position. On n'ajoute pas un rendu, on enrichit celui qui existe · No orphan rend l'aval (le prochain move), le bandeau rend l'amont (où tu es, ce qui vient de s'allumer).

**Gabarit · 3 lignes au-dessus des deux gestes** ·

```
Phase {nom} · {place dans le parcours}          ✓ {faites} posées  ◐ {restantes nommées}
Ce qui vient de se construire · {la pièce qui s'est allumée, une phrase, langage opérateur}.

{puis le no-orphan-output · le VERDICT expert d'abord (le move qui paie, DÉFENDU par l'état de la carte · « vu X, le move est Y parce que Z »), puis « ou creuser {pièce} » en trailing one-liner SI réel · jamais un doublet symétrique « 1 avance / 2 creuse »}
```

Exemple (le verdict tranche, il ne propose pas un menu) ·
```
Phase audiences · 2e palier sur 4               ✓ produit + offres posés  ◐ reste voix client · angles · scoring
Ce qui vient de se construire · l'arbre des audiences, 3 mères + 7 sous-poches, chacune reliée au produit par usage.

Le move qui paie · ta poche « beauté de l'intérieur » est non-occupée par la concurrence ET ta compo la porte (hyaluronique, biotine) · c'est là que je mettrais le premier test, c'est ce qui définit une catégorie au lieu de la disputer. Voilà pourquoi avant les autres.
   (tu peux d'abord creuser une mère pour voir ses sous-poches · mais le move au-dessus est celui qui paie.)
```

**La position se LIT, elle ne s'infère pas.** Le parcours est la structure des paliers + la Matrix de ce skill (miroir des 10 phases de `docs/system/onboarding-setup-flow.md`, source de vérité). « Ce qui reste » se dérive des phases non encore posées + des poches reportées dans `pending-validations.md`. Zéro nouvel état · `session-state.md` porte déjà la position pour la reprise, on la rend en live.

**Parcours UNIFIÉ à travers la couture des deux orchestrateurs.** Quand `onboard-brand` handoff vers ce skill, le compteur NE repart PAS à zéro · le bandeau compte sur le parcours entier (porte → close), pas sur la numérotation locale de chaque orchestrateur. L'opérateur ne doit jamais avoir à recoller deux moitiés mentalement.

**Posture, jamais gate (Master rule · gates au macro seulement).** Le bandeau REND et PROPOSE, il ne demande pas la permission. Les deux gestes restent des affordances toujours disponibles · qui tape « ok » avance, qui veut creuser peut. Ajouter un point de validation par phase violerait « gates au macro seulement » · le bandeau est de la visibilité, pas un gate de plus.

**Le prochain move est une RECOMMANDATION raisonnée, jamais un choix nu (D#514).** « Avancer ou creuser ? » présenté en either/or symétrique est BANNI · c'est reporter la réflexion sur l'opérateur. Le « move qui paie » se DÉRIVE de l'état de la carte · ce qui bloque (l'objection severity-max non traitée, l'audience priorité-1 à confidence faible), ce qui débloque le plus en aval, ce qui est category-defining. L'agent dit « vu que {état stratégique de ta carte}, le move qui paie le plus est {X} parce que {Y débloque / dérisque / définit la catégorie} », puis l'alternative en une ligne SI elle est réelle, avec le pourquoi-X-d'abord. La logique d'enrichissement est portée par l'agent, jamais tirée au sort par l'opérateur. C'est le no-orphan-output de `contextual-intelligence.md` (reco forte défendue, jamais menu plat) réinvoqué à CHAQUE handoff · c'est précisément là que le runtime le saute (observé run onday · close sur « j'enchaîne ou tu creuses ? » symétrique).

**L'orchestrateur POSSÈDE le close (D#519 · le split narrate-puis-écris est la cause).** Le bandeau + la reco se rendent dans le FIL ORCHESTRATEUR (qui porte la lecture stratégique sur les 5 axes), JAMAIS délégués au sous-agent d'écriture · un close émis par un agent qui n'a pas la carte complète retombe mécaniquement sur le menu symétrique ou le « tape valide pour débloquer » (observé run onday · le fil narre le verdict consolidateur-averti, l'agent d'écriture grave un gate procédural dans `pending-validations.md`). Et le close ne s'annonce qu'APRÈS vérification que l'artefact correspondant est écrit (audiences_index réconcilié + `profile.json` non-template), pas seulement narré · sinon le bandeau ment sur une phase « posée » qui n'existe que dans le fil.

**Deux anti-patterns bannis** ·
- **AP-POS-1 · barre N/M graphique rigide.** Le pipeline n'est pas une checklist · l'ordre suit la dépendance, l'exhaustivité est offerte pas forcée, des phases se reportent. Un « 4/10 » en barre de progression mentirait dès qu'une phase est sautée. Le compteur honnête est qualitatif (zones nettes vs zones de brouillard avec levier) plus la position nommée, jamais un dénominateur fixe traité comme une complétion linéaire.
- **AP-POS-2 · doctrine sœur ou viewer re-codé.** Pas de doctrine compagnon de plus (le canon en a assez qui se citent), pas de commande séparée à aller chercher · le bandeau vit dans le fil de l'orchestrateur, en sortie de phase. Re-coder un viewer dupliquerait `/phantom`.

---

## Expert methodology

**Canonical expert persona**: senior strategic director at a paid-acquisition agency, briefing a brand from blank URL to deployable territoire substrate in one sitting. Owns the chain, validates at each gate, lifts the operator's view to project altitude when uncertainty surfaces. Briefs+créas production handed off post-atlas to `creative-brief-composer`.

**Framework**: sequential territoire substrate chain en **4 paliers progressive cartography** (v1.4.0 v2.68 doctrine `docs/system/progressive-cartography-doctrine.md`) avec **gates light entre paliers** + Gate A audiences + Gate B angles preserved après Phase 4. Confidence chain propagated phase-by-phase per `docs/system/confidence-propagation.md`. Investigation Posture enforced on the final operator-facing synthesis per `docs/system/investigation-posture.md`. Scope discipline per `docs/system/territory-doctrine.md` (v2.67).

**Paliers progressive cartography v1.4.0** ·
- **Palier Phase 1+2** · snapshot-brand chain (structure + URL scan · ~10-15 min)
- **Gate intermédiaire 1** · territoire produit + offers + brand identity validation
- **Palier Phase 3** · map-audiences hiérarchique parent/enfants 3 niveaux mère + sous-poches (4 questions framework canon · ~15-20 min)
- **Gate intermédiaire 2** · arbre audiences validation (drop / ajoute / valide avant enrichissement)
- **Palier Phase 4** · mine-voc × N audiences + profile-audience × N (enrichissement per audience · pain_points + objections + JTBD canon V3 8 dimensions · ~30-45 min)
- Phase 5-9 preserved · weight-dimensions, produce-paid-angles (Gate B), score-matrix, stage territories, close

**Matrix**:

| Phase | Skill delegated | Subagent? | Gate before next phase |
|---|---|---|---|
| 0. Pre-flight (DRGFP) | inline | n/a | brand_slug present, URL or snapshot ready, MCP layer detected, `--fast-track` flag check |
| **Palier 1+2** | | | |
| 1. Structure + identity | `setup-brand` | No (conversational) | brand.json filled with name + language + sector |
| 2. URL snapshot | `snapshot-brand` (Task, includes Phase 1 macro + Phase 2 drilling gate) | Yes | spec.json + offers.json + profile.json draft at 60% |
| **GATE INTERMÉDIAIRE 1** (light · v1.4.0) | inline operator validate | n/a | Territoire produit + offers + brand identity posé · validation/correction binaire avant Phase 3 audiences |
| **Palier 2.5 · Spectre** (v1.8.0) | enum → `map-audiences` mode spectre (F1) · carte → `map-angles` mode spectre (conditionnel) | Yes | `spec.use_cases[]` peuplé (toujours) · `spectrum.json` si `spectre_mode` auto/proposed · contre-cas off si mur ≠ marché |
| **Palier 3** | | | |
| 3. Map audiences (hiérarchique parent/enfants) | `map-audiences` (Task brand-wide) | Yes | N audiences mère + sous-poches proposed, 4 questions framework canon |
| **GATE INTERMÉDIAIRE 2** (light · v1.4.0) | inline operator validate | n/a | Arbre audiences validation · drop X / ajoute Y / valide avant Phase 4 enrichissement |
| **Palier 4** | | | |
| 4a. Mine VoC per audience | `mine-voc` (Task per audience validée) | Yes | pain_points + objections sub-audience populated, verbatim_quotes corpus |
| 4b. Profile audience per audience | `profile-audience` (Task per audience validée) | Yes | profile.json enriched JTBD canon V3 8 dimensions + psychology + voice + behavior + decision_process |
| **4c. Mine VoM brand-wide (RESTAURÉ v1.10.0 · OFFERT)** | `mine-vom` (Task brand-wide · // de 4a/4b) | Yes | `brand.json#/market` + profile `voice.market_vernacular[]` + `competitive_comparison` · offert au Gate Inter 2, reportable |
| **4d. Compétitif paid + intel externe (OFFERT v1.10.0)** | `watch-competitors` + `trendtrack-enrich-brand` (Task) | Yes | competitive-intel md + `brand.json#/market` + espace blanc paid sourcé · offert/reportable, skip propre si MCP/API absent (flag inconnu + levier) |
| **GATE A** (preserved v1.3.0) | inline operator validate | n/a | Operator accepts / corrects audiences enrichies |
| 5. Weight dimensions | `weight-dimensions` (Task brand-wide) | Yes | Audience-angle compatibility scores pre-computed (internal) |
| 6. Paid angles | `produce-paid-angles` (Task per top-3 audience) | Yes | Angles ranked per audience (formula Obs+Tension+Reframe+Bridge) |
| **GATE B** (preserved v1.3.0) | inline operator validate | n/a | Operator accepts / corrects ranked angles |
| 7. Score matrix | `score-matrix` (Task brand-wide) | Yes | Profil × Source d'angle matrix, top 3 axes créatifs selected |
| 8. Stage territories | inline (substrate review) | n/a | Territories staged as proposals, ready for downstream production |
| **8.5. Atlas Visibility Matriciel (NEW v1.6.0)** | inline (synthèse cross-atlas) | n/a | 4 niveaux canon · Décomposition produit · Many-to-many pain × audience · Stage business filter · Méthode pédagogique verbale |
| 9. Close | inline (Investigation Posture 5 sections) | No | Synthesis delivered, no orphan close, handoff to `creative-brief-composer` proposed |

**Mode `--fast-track`** · si flag `--fast-track` passed OR `operator/profile.json#preferences.auto_validate_after_n_brands` true détecté → skip Gate intermédiaire 1 + Gate intermédiaire 2 (auto-validate silent log). Gate A + Gate B preserved (structural decisions audiences finales + angles ranked). Default = gates light visible (premier-contact opérateur garde repère cognitif).

**Variables tracked**:
- `url_available` (bool) · drives whether Phase 2 runs or skips with confidence degradation
- `audience_count_validated` (int) · caps Phase 6 and Phase 7 cardinality (top-3 per default)
- `axe_creatif_count_selected` (int) · caps Phase 7 scoring output (top-3 axes créatifs per default)
- `confidence_floor` (float internal) · propagates worst-case across phases; never surfaced
- `mcp_layer` (set: facebook-graph, notion, none) · drives Phase 3 source breadth
- `spectre_mode` (enum: auto / proposed / off) · gouverne le palier Spectre Step 2.5 (carte complète) · décidé au Step 0 depuis `brand.meta.stage` + régime · l'énumération des usages reste TOUJOURS active indépendamment de cette variable
- `function_scope` (profil dérivé · jumelle de `spectre_mode`) · dimensionne quelles couches DÉRIVÉES s'allument et à quelle profondeur selon le POSTE de l'opérateur · dérivé au Step 0ter depuis `operator/profile.json#identity.function` croisé avec `resources/canon/operator/function-pole-map.json` · **vide → FULL** (comportement actuel exact, backward-compat strict) · ne touche JAMAIS le plancher (L0 + atlas-cœur tronc), qui reste inconditionnel pour toute fonction

**Failure modes**:
- Phase 1 (setup-brand) aborts mid-flow → persist `brands/{slug}/session-state.md`, allow resume via `resume-session`. Never restart from zero.
- Phase 2 (snapshot) fails (URL 404, JS-heavy, paywalled) → degrade gracefully: skip Phase 2, surface confidence drop to operator, continue downstream phases with declared-only data.
- Phase 3 (deepen) returns thin material (no Reddit, no Trustpilot reviews available) → flag as "Inconnu" in final synthesis, propose `mine-voc` ticket as Lever.
- Gate A or B operator rejects all proposals → pause pipeline, route to standalone `profile-audience` or `produce-paid-angles` for manual rework, do not silently kill chain.
- Phase 7 (score-matrix) finds zero viable axe créatif → surface honestly, propose alternative routes (expand audiences, re-mine VoC for missed angles).

---

### Step 0 · DRGFP Manifest Registry Scan (NEW v2.75.0)

Pre-flight discovery NEW entities scaffolded via scaffold-extension v1.2.0+ · 
scan `_extensions.json` OR `_manifest.json#extensions` pour entities avec 
`consumable_by: [{skill_name}]` matching CE skill.

Pour chaque NEW entity registered matching extension_hooks frontmatter ·
- Match `entity_type` ∈ frontmatter `extension_hooks` enum
- Match `consumable_by` field registry contains `{skill_name}` 
- Include NEW entity dans inputs Phase 1 pipeline ci-dessous
- Output enrichi avec lineage extension consommée dans frame

Halt si NEW entity registered sans `consumable_by` field flagué (scaffold-extension v1.2.0 legacy) · 
silent skip · pas error · l'opérateur peut patcher manuellement le scaffold-extension Phase 9 register-and-flag pour ajouter `consumable_by`.

Cross-ref doctrine canon · `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW.

---

### Step 0ter · `function_scope` · le POSTE de l'opérateur dimensionne les couches dérivées (D#52x)

**Lis `operator/profile.json#identity.function` AVANT de lancer le pipeline.** C'est le poste opérationnel de l'opérateur sur CETTE marque (paid / creative / studio / conversion / retention / intelligence / ops / finance / growth · liste, multi-fonction normal), distinct de la RELATION (`identity.profile` solo/agency/...). Si `onboard-brand` te passe déjà `function_scope` au handoff (Step 6), utilise-le · sinon dérive-le ici.

**Dérivation (déterministe, calquée sur `spectre_mode`).** `function` non vide → pour chaque pôle, lis `resources/canon/operator/function-pole-map.json#poles[{pôle}]` · multi-fonction = **union par couche (MAX, off < light < full)**. `function` **vide ou inconnu → `function_scope = FULL`** · le pipeline tourne EXACTEMENT comme aujourd'hui (backward-compat strict · c'est le test de non-régression). Croise avec `brand.meta.stage` (un paid en launch ≠ un paid en scale · la map est un défaut, le stage module la profondeur).

**Ce que `function_scope` conditionne (les SOMMETS uniquement)** ·
- **Step 2.5 sous-bloc B (Spectre)** · `effective_spectre = max(spectre_mode_depuis_stage, spectre_push_de_la_fonction)`. La fonction COMPOSE, elle n'override jamais · un poste qui consomme l'axe Marché (creative/growth) pousse vers `auto`, les autres laissent le stage décider.
- **Phase 6 (produce-paid-angles)** · **lis le champ ÉCRIT `operator/awareness.json#function_scope_l2`** (dérivé mécaniquement par le hook `checkpoint-resolver` depuis la fonction × `function-pole-map.json` · tu ne re-dérives PAS la décision en prose, D#520). `off` (intelligence/finance/ops pures · aucune fonction ne consomme la production) → skip produce-paid-angles. `on` (défaut · paid/creative/retention/... OU fonction vide = FULL) → tourne à la cardinalité dérivée.
- **Phase 7 (score-matrix)** · skippée si `function_scope_l2 = off` (pas d'angles à scorer).
- **Step 9 close · chantiers** · `pending-validations.md` priorisé par fonction · un tracker voit « brancher tes comptes » en P0 (`L3_data` full), pas « valider les angles » · un paid voit l'inverse. La `connect_priority` du pôle pilote.

**Le PLANCHER ne se conditionne JAMAIS (garde-fou dur).** L0 (identité + produit + offres) et L1 atlas-cœur tronc (`spec.use_cases[]` ≥1 speculative + arbre audiences avec `jtbd` non-vide) tournent pour TOUTE fonction, multiplicateur ≥ light. Un tracker garde le produit et les audiences (sinon ses chiffres sont aveugles), il skip la PRODUCTION pas l'atlas. Phases 0 à 5 sont inconditionnelles.

**Mécanisme, pas prose (D#520 · Master rule).** Le conditionnement ci-dessus est une PRIORISATION rendue par l'orchestrateur, jamais un gate de pré-validation au write. Les verrous réels sont POST-HOC · (1) le plancher est garanti par la postcondition-sur-artefact du Step 9 + le checkpoint avant map-audiences (`use_cases_missing` / `audience_profile_template_clone` dans `validate-all.py` tirent QUELLE QUE SOIT `function_scope`) · (2) le sur-encodage hors-fonction est signalé advisory par `function_layer_drift` (MED) dans `validate-all.py`, jamais empêché. On ne bride jamais le modèle, on rend la priorisation et on vérifie l'empreinte.

**Fonction inférée (`awareness.json#function_inferred = true`).** Si le poste a été inféré du langage (pas déclaré), expose-le en UNE ligne au premier handoff et laisse corriger d'un mot · *« Je pars sur un encodage {fonction} · atlas-cœur + {ce qui s'allume}, je laisse {les cases ouvertes} en réserve. Ça matche ? »*. Jamais un menu des 9 pôles, jamais un questionnaire. `function` vide reste un inconnu-typé-avec-levier, pas un blanc · le pipeline tourne FULL en attendant.

---

## Step 0 · Pre-flight (DRGFP)

Check operator provided minimum context. Apply Dependency Resolution & Gap-Filling Protocol L1 → L2:

- **brand_slug** required. If absent → ask via AskUserQuestion: *"Sur quelle marque je build l'atlas complet ?"*.
- **URL** or **existing snapshot**. If neither, mark `url_available = false` and warn confidence will degrade. If operator typed *"build atlas {brand}"* without URL on a blank workspace, ask once: *"Tu as une URL pour pré-remplir, ou je travaille en blind (purement déclaratif) ?"*.
- **MCP layer detection**: silent check `.mcp.json` for `facebook-graph` (Meta benchmarks) and `notion` (existing strategic memos). Populate `mcp_layer`. Surface only if operator asks.
- **Fast-track flag check (v1.4.0)** · check si flag `--fast-track` passed dans invocation OR `operator/profile.json#preferences.auto_validate_after_n_brands` true détecté. Si oui → mark `fast_track = true`, log silent ("opérateur expert détecté · gates intermédiaires bypass auto-validate · Gate A audiences + Gate B angles preserved"). Si non → mark `fast_track = false`, gates intermédiaires light visible default.
- **Spectre mode decision (v1.8.0 · D#506)** · lire `brand.json#/meta/stage` (champ schématisé, source unique). Poser `spectre_mode` · `stage == launch` → **`auto`** (le mur est marché-découverte, la carte se lance sans demander). `stage ∈ {scale, mature, growth}` → **`proposed`** (le cœur est la priorité, la carte est offerte au gate light, l'opérateur tranche). `stage` absent → fallback `brand_equity_level` (faible / none → `auto`, établi → `proposed`) + flag l'inférence. NE PAS dépendre de frame-regime (à l'onboarding il n'a pas tourné et renverrait toujours explore · `stage` suffit). **Contre-cas, sans violer la purity rule** · l'orchestrateur ne DIAGNOSTIQUE PAS le mur lui-même (produire de la stratégie inline violerait sa pureté). Le contre-cas est porté par le close ouvert du mode `proposed` · si l'opérateur, ou un signal franc du snapshot (marge cassée, produit indistinct de l'alternative), indique que le vrai mur est l'OFFRE ou l'ANGLE, la carte attend (effectivement `off` pour ce run). L'orchestrateur EXPOSE le choix, il ne tranche pas le mur. N'affecte QUE la carte (sous-bloc B) · l'énumération (sous-bloc A) reste toujours active.

Announce the pipeline (chairman posture, no jargon, no skill names):

> *"OK, atlas complet de {brand}. Pipeline territoire substrat en 4 paliers progressive · Phase 1+2 structure + scan site, Phase 3 cartographie audiences (mère + sous-poches), Phase 4 enrichissement voix client per audience. Gates light entre paliers où tu valides au passage. Puis Phase 5-7 angles paid + scoring. Deux gates structurels (audiences enrichies puis angles ranked). 30 à 90 min selon la densité. Je pilote, tu valides aux gates. Une fois l'atlas posé, on enchaîne sur briefs+créas via `creative-brief-composer` sur l'axe créatif que tu choisis. Go ?"*

Si `fast_track = true` · ajouter une ligne *"Mode opérateur expert détecté · gates intermédiaires bypass auto-validate, on s'arrête seulement sur Gate A (audiences finales) + Gate B (angles ranked)."*

Hold for go-ahead, then proceed.

---

## Step 1 · Delegate `setup-brand` (inline, conversational)

**NEVER** spawn as subagent (`setup-brand.subagent_safe: false`). Invoke inline. Let it run its full conversational flow.

Pass context: operator-provided name/URL, detected profile (from `operator/profile.json`), language preference.

**Gate to Phase 2**: `brands/{slug}/brand.json` exists with `identity.name` and `identity.language` filled, OR operator explicitly deferred structure creation.

---

## Step 2 · Delegate `snapshot-brand` via Task tool

**If** `url_available = true` AND `snapshot-brand.subagent_safe: true`:

Spawn subagent via Task tool:
- `model: sonnet`
- Input: brand slug, URL
- Expected: `brands/{slug}/spec.json`, `brands/{slug}/products/{p}/offers.json`, `brands/{slug}/audiences/{a}/profile.json` drafts via stage-proposal pipeline

**CRITICAL · stage-before-ask is enforced through the subagent.** snapshot-brand SKILL.md mandates `.skills/stage-proposal.py` before any operator-facing proposal. This orchestrator inherits that rule by delegation. If the subagent ever skips staging and tries direct write, it hits the workflow gate. Do not retry a gated write; surface the gate message and wait for operator confirmation.

**Operator-facing line**:

> *"Je scanne le site pendant qu'on continue."*

**Rendu du scan · le BEAT, pas la météo (D#520).** Quand le deep-scan revient, le sous-agent a déposé son registre frais à `.phantom/beats/{slug}/scan.json` (trouvé · analysé · rejeté · encodé · confiance-avec-raison). Émets le beat de restitution en exécutant `python3 .skills/render-beat.py --brand {slug} --phase scan --mode orchestrated` et présente sa sortie TELLE QUELLE · un beat **décision-d'abord** (le verdict tranché + le second ordre, puis le raisonnement, puis ce qui reste prudent, puis le CTA `/phantom` teasé). NE re-narre PAS en une phrase, NE re-résume PAS · le rendu déterministe EST le handoff, il garantit que le travail, les rejets argumentés et la confiance-avec-sa-cause restent visibles (un run paie son scan, il ne lit pas la météo). Le hook `beat-emit` te le rappelle mécaniquement si tu l'oublies. La prose autour du beat reste à toi pour enchaîner vers le gate · le beat montre, ta phrase relie. **Tu es l'orchestrateur (`--mode orchestrated`)** · le beat signale le cap (« _Et après · …_ »), tu enchaînes tout seul vers le gate, tu ne demandes pas la permission de continuer.

**Filet** · si `render-beat` rend du vide (le sous-agent n'a pas déposé le payload), retombe sur la synthèse Step 7 du scan en prose · ne laisse JAMAIS un trou à la place du scan. L'attendu reste le beat, le repli n'est qu'un garde contre la perte sèche.

**Recon d'abord (v1.11.0).** snapshot-brand rend son rapport de recon (Step 1.5) AVANT le deep scan · archétype de cartographie (mono-héros / catalogue resserré / gros catalogue / marketplace), héros candidat, plan dimensionné, axes joignables. Cet archétype alimente directement l'hypothèse de territoires candidats au NIVEAU LIVE macro (cf exemple « le pattern catalogue cohérent · hero positionne sur X · secondaires drainent vers Y ») et dimensionne la profondeur du scan. En pilotage orchestré, snapshot tourne en deux temps · recon (rendu + dimensionnement, gate « valide le chantier » porté par onboard-brand Step 2) puis deep scan dimensionné. Gate Intermédiaire 1 reste le gate territoire · il valide la carte RICHE post-scan, la recon n'étant que le cadrage amont (prose, pas de matrice ASCII en LIVE).

**If `url_available = false`** → skip Phase 2, log `confidence_floor` drop, continue with declared-only context.

---

## GATE INTERMÉDIAIRE 1 · Phase 1+2 drilling validation (light · v1.4.0)

**Gate light** entre Palier Phase 1+2 (snapshot-brand) → Palier Phase 3 (map-audiences). Format canon doctrine `docs/system/progressive-cartography-doctrine.md` Section 8 Pattern gates light · 1-2 lignes synthesis + 1 binaire validation/correction. Pas Q&A verbeux.

**Si `fast_track = true`** · skip ce gate · auto-validate silent log ("Gate 1 bypass auto-validate · territoire produit + offers posé"). Continue direct Palier Phase 3.

**Si `fast_track = false`** (default) · surface synthesis 1-2 lignes + AskUserQuestion binaire ·

> *"Phase 1+2 drilling complete · territoire produit + offers + brand identity posé ({N produits · M offers · positioning détecté). Tu valides ou corriges avant qu'on attaque cartographie audiences ?"*

Options ·
- "Valide, on attaque cartographie audiences"
- "Corrige · {détail produit/offer/identity off}"

Si corrige → route correction inline (write_to_context mode proposed sur field concerné) puis re-surface gate. Si valide → proceed Palier Phase 3.

**NEVER** proceed Palier Phase 3 sans validation (gate light visible default) OR sans `fast_track = true` (opt-in auto-validate).

---

## Step 2.5 · Palier Spectre (v1.8.0 · D#502/D#506)

Inséré entre Gate Intermédiaire 1 (produit + offers + identité validés) et Phase 3 (map-audiences). Topologiquement correct · le mécanisme est encodé et validé, les usages s'énumèrent depuis lui, les audiences se dérivent ensuite par usage. **Purity rule** · ce palier DÉLÈGUE, il n'implémente aucune logique (l'énumération vit dans map-audiences mode spectre, la carte dans map-angles mode spectre).

### Sous-bloc A · Énumération des usages (TOUJOURS actif, indépendant de `spectre_mode`)

**Pré-requis · décompo produit assez profonde (`spec.mechanisms[]` ET `spec.benefits[]` peuplés).** Le pont génératif Mc→U lit le mécanisme, et la chaîne bénéfice 3 couches (functional/emotional/identity) nourrit le recadrage des angles downstream. `snapshot-brand` hand-roll souvent une passe MINCE · c'est le décrochage `define-specs` (l'orchestrateur de décompo profonde · map-mechanisms + map-benefits + map-specs · n'est jamais atteint par l'onboarding, donc snapshot pose un mécanisme nu sans bénéfices). **Garde à ré-poser à cette frontière** · si `mechanisms[]` vide → déléguer `map-mechanisms` · si `benefits[]` vide → déléguer `map-benefits` · si les DEUX sont minces → router vers `define-specs` (Task) qui les chaîne. PUIS seulement F1. Sans cette garde, F1 est mort-né, le pont Mc→U→A naît pauvre, et l'atlas « marche » mais creux. Le verrou réel n'est PAS un gate de pré-validation au write (Master rule) · c'est cette garde orchestrateur + le filet post-hoc miroir (inspecte l'artefact écrit quelle que soit la porte) · `benefits_missing` + `use_cases_missing` dans `resources/scripts/validate-all.py` (MED, même forme que la garde D#519).

Déléguer à `map-audiences` mode spectre, fonction F1 (Task tool, subagent_safe). Entrée · le produit validé + ses mécanismes. Sortie · `spec.use_cases[]` peuplé (mécanisme → usages · evident/adjacent/speculative). Ce nœud nourrit la dérivation d'audiences de la Phase 3 (audiences PAR usage). Coût quasi nul (raisonnement), donc toujours exécuté.

**Garde-fou anti-skip (D#512).** `spec.use_cases[]` peuplé est une PRÉCONDITION DURE de la Phase 3 · sans le pont mécanisme→usage, la dérivation d'audiences retombe sur le miroir des avis (biais du survivant · `docs/doctrine/audiences-cartography-doctrine.md` Pitfall 8), exactement le décrochage observé au run onday (use_cases[] vide → 3 audiences tirées des avis). Un atlas qui atteint la Phase 3 avec `use_cases[]` vide est invalide · le sous-bloc A n'a pas tourné, on le relance avant de dériver. Le verrou réel n'est PAS un gate `write-to-context` au moment d'écrire (pré-valider le raisonnement du modèle = interdit, Master rule) · c'est la **postcondition orchestrateur sur l'ARTEFACT** (Step 9 · refuse de clôturer si `use_cases[]` n'a aucun speculative, quelle que soit la porte qui l'a produit) + le filet post-hoc `use_cases_no_speculative` de `resources/scripts/validate-all.py` (D#518). Ce texte est le garde-fou de prose en amont.

**Profondeur, pas seulement présence (D#514).** `use_cases[]` doit inclure le tier NON-ÉVIDENT · au moins 2-3 `adjacent`/`speculative`, pas seulement les `evident`. Un use_cases tout-evident = exploration avortée · la dérivation d'audiences retombe sur les tiers du même acheteur déjà visible, et les segments non servis (les vraies audiences outside-the-box) ne sortent jamais. Le garde-fou de fond vit dans `map-audiences` F1 (v1.4.1) · ici on refuse de passer en Phase 3 sur un `use_cases[]` sans aucun `speculative`.

### Sous-bloc B · Carte complète (conditionnel `spectre_mode`)

- **`spectre_mode = auto`** (launch / explore-dominant) · lancer la carte sans demander (bypass type fast_track · le mur EST le marché-découverte). Déléguer à `map-angles` mode spectre → `brands/{slug}/spectrum.json`. Carte au crayon assumée (beaucoup d'hypothèses sur une marque neuve, flaggées comme telles). **Auto n'est PAS 'proposé' (D#514)** · la carte RUNS, `spectrum.json` est écrit, ce n'est pas optionnel. Un onboarding launch qui se termine sans `spectrum.json` = sous-bloc B sauté, invalide (observé run onday · spectrum.json absent malgré stage launch · le négatif concurrentiel lu en prose mais jamais cartographié ni persisté, donc non consommable par les angles downstream). Le verrou réel · la **postcondition orchestrateur** (Step 9 · `spectrum.json` doit exister avant que les angles soient opérables, sauf `spectre_mode=off`) + le back-ref optionnel `angle.lineage.use_case_ref`/`spectrum_cell_ref` (schéma D#518) tracé post-hoc par `validate-resources` quand présent · pas un gate de pré-validation au write (Master rule).
- **`spectre_mode = proposed`** (scale / mature) · gate light binaire (réutilise le pattern de Gate Intermédiaire 1) · *"Le cœur de {brand} est posé, c'est lui qu'on rend opérable d'abord. Je peux aussi cartographier tout ton marché adressable, les usages que ton produit peut servir au-delà de ton cœur, ou on garde ça pour quand tu voudras t'étendre ?"*. Si oui → déléguer à map-angles mode spectre. Si non → skip, log que la carte reste disponible à la demande (`/phantom {brand} spectre`).
- **`spectre_mode = off`** (mur ≠ marché) · skip la carte. Surface 1 ligne · *"Avant de cartographier de nouveaux marchés, le vrai blocage de {brand} est {l'offre / l'angle}. On regarde ça d'abord."* (route le diagnostic, pas la carte).

**Rendu de la carte · le BEAT, pas la météo (D#520).** Quand `spectrum.json` est écrit (`spectre_mode = auto`, ou `proposed` accepté au gate light), la carte de marché est du travail lourd · le négatif concurrentiel, les territoires jouables, les zones blanches, ce qui est libre et ce que ça coûte · ça ne se narre PAS en « le spectre est posé ». Le sous-agent map-angles a déposé son registre frais à `.phantom/beats/{slug}/spectrum.json` (doctrine SSOT · `docs/system/restitution-beat-doctrine.md`). Émets le beat en exécutant `python3 .skills/render-beat.py --brand {slug} --phase spectrum --mode orchestrated` et présente sa sortie TELLE QUELLE · le verdict tranché (où le lane est libre et pourquoi, la fragilité du moat) + le second ordre, puis le raisonnement (les territoires lus, les concurrents écartés), puis ce qui reste prudent (les zones blanches `coverage_market: unknown` que le fetch compétitif downstream lèvera · cf le Spectre dirige le fetch, ci-dessous), puis le CTA `/phantom {slug} spectre` teasé. NE re-narre PAS, NE re-résume PAS · le rendu déterministe EST le handoff. Le hook `beat-emit` te le rappelle si tu l'oublies. Mode `orchestrated` · le beat signale le cap, tu enchaînes vers la Phase 3. **Si `spectre_mode = off` (mur ≠ marché) ou carte non lancée, PAS de beat spectrum** · il n'y a pas de carte à restituer, la ligne `off` du sous-bloc B suffit (ne pas émettre un beat vide, le filet fail-open de `render-beat` le couvre de toute façon).

Dégradation propre · si map-audiences/map-angles mode spectre indisponibles au runtime, le palier dégrade (énumération flag inconnu, carte non lançable) plutôt que freestyle. Gate light 1-2 s entre le palier et la Phase 3 (conforme `progressive-cartography-doctrine.md` §8).

**Le Spectre dirige le fetch downstream (D#518).** Une fois `spectrum.json` posé, ses zones blanches (`coverage_market: unknown/blank`) DIRIGENT le fetch marché/concurrentiel · l'orchestrateur route `watch-competitors` vers ces trous (il ne fetch pas lui-même · purity rule), et le pont `watch-competitors → coverage_market` (Step 7 du skill) les remplit. Un artefact qui dirige est rempli, un qui couronne est vide · doctrine `docs/system/scrape-as-allocation.md`.

---

## Step 3 · Delegate `map-audiences` via Task tool (Palier Phase 3 hiérarchique)

**Refactor v1.4.0** · Phase 3 cartographie audiences hiérarchique parent/enfants 3 niveaux mère + sous-poches via `map-audiences` (4 questions framework canon doctrine `docs/system/progressive-cartography-doctrine.md` Section 5). Remplace ancien Step 3 deepen-brand-context (chain mine-voc + mine-vom upfront) qui a été déplacé vers Palier Phase 4 enrichissement per audience validée.

**Précondition dure (chaîne experte · D#512).** La dérivation d'audiences NE COMMENCE PAS tant que `spec.use_cases[]` n'est pas peuplé (Step 2.5 sous-bloc A) · dériver les audiences du miroir des avis sans le pont mécanisme→usage est l'anti-pattern banni (biais du survivant · `docs/doctrine/audiences-cartography-doctrine.md` Pitfall 8). Si `use_cases[]` vide à l'entrée → ne pas dériver depuis les avis, relancer le sous-bloc A d'abord. Ordre canon · position concurrentielle lue (NIVEAU LIVE) → usages énumérés → audiences dérivées par usage, jamais l'inverse.

**Checkpoint-sur-ARTEFACT avant de spawn map-audiences (D#519 · le garde-fou ne vit plus seulement au close).** Le verrou use_cases/spectrum était posé UNIQUEMENT en postcondition de Step 9 · or un run qui pause à un gate opérateur AVANT le close ne le déclenche jamais, et tout le raisonnement narré dans le fil s'évapore (observé run onday · le fil narre la carte mécanisme→usage, `spec.use_cases[]` reste VIDE sur disque, le split narrate-puis-écris a lâché l'écriture). Donc · l'orchestrateur LIT `products/{slug}/spec.json` et REFUSE de scaffolder le moindre dossier audience tant que · `spec.use_cases[]` non-vide AVEC ≥1 `speculative` ET (pour `stage=launch` / `spectre_mode=auto`) `spectrum.json` existe. Si l'un manque, le pont a été parlé mais pas PERSISTÉ · relancer Step 2.5 sous-bloc A/B et VÉRIFIER l'empreinte sur disque avant de continuer, jamais avancer sur la narration. C'est la même postcondition-sur-artefact que Step 9, re-posée à CHAQUE frontière de gate. Filets post-hoc correspondants · `use_cases_missing` + `use_cases_no_speculative` dans `resources/scripts/validate-all.py`.

`map-audiences` is `subagent_safe: true`. Spawn single subagent brand-wide.

Pass context:
- brand slug
- territoire drilling Phase 2 (spec.json + offers.json + brand.json identity)
- mode: `hierarchique` (3 niveaux mère + sous-poches default)

For execution:
- `model: sonnet`
- Input: brand slug, snapshot Phase 2 output
- Expected: arbre audiences mère + sous-poches (hiérarchique parent/enfants 3 niveaux) avec 4 questions framework canon (qui? quoi? pourquoi? quand?) appliquées par audience

**Operator-facing line**:

> *"Je cartographie les audiences hiérarchique mère + sous-poches."*

When map-audiences returns, synthesize at orchestrator level into a single arbre audiences tableau (mère × sous-poches × confidence chain). **NEVER** dump raw subagent output verbatim per delegation pattern §synthesis layer.

**Rendu de l'arbre · le BEAT, pas la météo (D#520).** Cartographier les audiences est du travail lourd et invisible (énumération mécanisme→usage, dérivation par usage, rejets de poches non servies, confiance per audience) · ça ne se narre PAS en « audiences cartographiées ». Le sous-agent map-audiences a déposé son registre frais à `.phantom/beats/{slug}/audiences.json` (doctrine SSOT · `docs/system/restitution-beat-doctrine.md` · contrat payload, décision-d'abord, second ordre, temporalité). Émets le beat en exécutant `python3 .skills/render-beat.py --brand {slug} --phase audiences --mode orchestrated` et présente sa sortie TELLE QUELLE · le verdict tranché (quelle mère est category-defining, quelle poche est non-occupée) + le second ordre, puis le raisonnement (les sous-poches dérivées par usage, les pistes écartées), puis ce qui reste prudent (audiences à confiance faible · le beat peut pointer l'étape voix-client qui les lèvera), puis le CTA `/phantom {slug} audiences` teasé. NE re-narre PAS, NE re-résume PAS · le rendu déterministe EST le handoff. Le hook `beat-emit` te le rappelle si tu l'oublies. Mode `orchestrated` · le beat signale le cap, tu enchaînes vers le Gate Intermédiaire 2, tu ne demandes pas la permission de poursuivre.

**Filet** · si `render-beat` rend du vide (pas de payload déposé), retombe sur la synthèse de l'arbre en prose · ne laisse JAMAIS un trou à la place de la cartographie audiences. L'attendu reste le beat, le repli n'est qu'un garde contre la perte sèche.

---

## GATE INTERMÉDIAIRE 2 · Phase 3 audiences cartography validation (light · v1.4.0)

**Gate light** entre Palier Phase 3 (map-audiences hiérarchique) → Palier Phase 4 (enrichissement per audience). Format canon doctrine `docs/system/progressive-cartography-doctrine.md` Section 8 Pattern gates light.

**Précondition d'ENTRÉE de gate (D#519 · ne jamais surfacer un gate sur une carte vide).** AVANT de rendre ce gate (donc avant toute pause opérateur ici), re-vérifier l'artefact sur disque · (1) `spec.use_cases[]` non-vide avec ≥1 speculative ET `spectrum.json` existe (stage launch) · (2) chaque `audiences/{slug}/profile.json` scaffoldé n'est PAS le template dégénéré (`meta.slug` ≠ `example-audience`, `entry_door` + `psychology.jtbd.primary` non-vides). Si un artefact est vide ou clone-du-template, le raisonnement n'a pas atteint le disque (split narrate-puis-écris) · RÉPARER l'écriture avant de rendre le gate, jamais figer la fuite derrière une pause opérateur (observé run onday · gate surfacé avec `actifs-fatigue` resté octet-pour-octet le template). Filets post-hoc correspondants · `audience_profile_template_clone` + `use_cases_missing` dans `validate-all.py`.

**Si `fast_track = true`** · skip ce gate · auto-validate silent log ("Gate 2 bypass auto-validate · arbre audiences posé"). Continue direct Palier Phase 4.

**Si `fast_track = false`** (default) · surface synthesis 1-2 lignes + AskUserQuestion binaire ·

> *"Phase 3 cartographie audiences complete · {N} audiences mères + sous-poches posées. Tu valides l'arbre · drop X · ajoute Y · ou on attaque Phase 4 enrichissement ?"*

Options ·
- "Valide l'arbre, on attaque Phase 4 enrichissement"
- "Drop {audience X} · re-trim arbre"
- "Ajoute {audience Y} · enrichir arbre"

Si drop/ajoute → route correction inline (map-audiences refine targeted) puis re-surface gate. Si valide → proceed Palier Phase 4.

**NEVER** proceed Palier Phase 4 sans validation (gate light visible default) OR sans `fast_track = true`.

---

## Step 4 · Palier Phase 4 enrichissement per audience (mine-voc × N + profile-audience × N)

**Refactor v1.4.0** · Palier Phase 4 enrichissement per audience validée Gate Intermédiaire 2. Chain `mine-voc` × N audiences + `profile-audience` × N audiences (parallel cap 3 par delegation pattern). Remplace ancien Step 4 profile-audience standalone qui shootait à partir cross-signals upfront (vs audiences validées operator post Gate Intermédiaire 2 v1.4.0).

**Sub-step 4a · `mine-voc` per audience validée** ·

`mine-voc` is `subagent_safe: true`. Spawn one subagent per audience validée Gate Intermédiaire 2 (cap 3 parallel).

For each audience:
- `model: sonnet`
- Input: brand slug, audience id
- Expected: pain_points + objections sub-audience populated · `audiences/{a_slug}/pain_points/*.json` (PNT-NN entities) + `audiences/{a_slug}/objections/*.json` (OBJ-NN entities)

**v1.2.0 ontologie sémantique pure v2.64 · sub-parent locations.** Phase 4 mine-voc écrit dans sub-parent locations (owned natif par parent path) ·

- `brands/{slug}/audiences/{a_slug}/pain_points/*.json` (PNT-NN entities · formulation + verbatim_quotes + emotion + trigger + severity + chain + confidence_chain · audience owner implicite via parent path, pas de array affected_audiences[])
- `brands/{slug}/audiences/{a_slug}/objections/*.json` (OBJ-NN entities · formulation + type + frequency + severity + lifecycle_stage + response_counter + derived_angle_refs · audience owner implicite)
- `brands/{slug}/products/{p_slug}/frictions/*.json` (FRC-NN entities · formulation + type + signals · product owner implicite via parent path · NEW canonical layer for product-bound frictions sub-product)

**Backward compat strict additif** · fallback transparent top-level v2.63 (`pain_points/` + `objections/` + `frictions/` avec affected_audiences[]/affected_products[]) + profile sub-fields v1.7 preserved si brand brownfield.

**Sub-step 4b · `profile-audience` per audience validée** ·

`profile-audience` is `subagent_safe: true`. Spawn one subagent per audience validée (cap 3 parallel · run après mine-voc 4a complete pour enrichir profile avec verbatim_quotes corpus).

For each audience:
- `model: sonnet`
- Input: brand slug, audience id, mine-voc output (pain_points + objections sub-audience)
- Expected: full profile.json with JTBD canon V3 8 dimensions + identity + psychology + voice + behavior + decision_process · confidence chain explicit per axis · observed/déduit/déclaré sourcing tags

**Operator-facing line**:

> *"Je mine la voix client puis enrichis les profils audiences validées en parallèle. ~30-45 min en arrière-plan."*

**Sub-step 4c · `mine-vom` brand-wide (voix marché · RESTAURÉ v1.10.0 · axe marché/compétitif)** ·

Le refactor v1.4.0 avait décroché `mine-vom` (l'ancien Step 3 `deepen-brand-context` chaînait `mine-voc + mine-vom`). On le restaure ici comme palier **brand-wide** (la voix marché n'est pas per-audience · elle pose la sophistication du marché, le vernaculaire, le compétitif), **offert, jamais bloquant**. La règle de doctrine « voix client ET marché » redevient vraie.

`mine-vom` is `subagent_safe: true`. Spawn one subagent brand-wide. **Ordonnancement vs cap parallèle** · 4a/4b sont per-audience et peuvent saturer les 3 slots · 4c et 4d sont brand-wide (1 sous-agent chacun) · ils tournent dans une **vague séparée** une fois que 4a/4b ont libéré leurs slots, ou occupent un slot resté libre · le cap de 3 sous-agents simultanés par phase reste tenu, jamais 4a+4b+4c+4d tous au-delà de 3 en même temps.

- `model: sonnet`
- Input: brand slug, niche/catégorie depuis `spec.json`, concurrents détectés
- Expected: `brand.json#/market/*` (distribution awareness marché, signaux réglementaires, saisonnalité) + `audiences/{a_slug}/profile.json#/voice/market_vernacular[]` + `products/{p_slug}/spec.json#/competitive_comparison` + `sources/vom/*.json` (corpus Layer A avec provenance)

**Offert, pas forcé (cohérent progressive cartography + exhaustivité reportable HR-ONB-3)** · au Gate Intermédiaire 2 (arbre audiences validé), présenter le doublet · *"J'enrichis aussi la voix du marché et le compétitif pendant le mining client, ou je garde ça pour un second temps ?"*. Si oui → 4c tourne en fond après/avec 4a/4b (cap tenu). Si reporté → écrire la poche dans `pending-validations.md` avec levier `mine-vom` ultérieur. En `fast_track`, 4c tourne par défaut (log silencieux). La voix marché nourrit le substrat que le Spectre (Step 2.5) et les angles (Phase 6) consomment · sans elle, l'espace blanc paid de la matrice (NIVEAU 2) reste deviné, pas sourcé.

**Condensation au gate (préserve le format gate light).** Cette offre 4c/4d se **condense avec les autres affordances** du Gate Inter 2 (le doublet agir/creuser HR-ONB-1, l'offre d'exhaustivité HR-ONB-3) en **UNE seule ligne d'offre groupée** après le binaire de validation, jamais en sollicitations empilées. Le gate light reste 1-2 lignes (format canon `progressive-cartography-doctrine.md` §8) · on ne transforme pas un gate binaire en menu à trois questions.

**Sub-step 4d · compétitif paid + intel brand externe (OFFERT · axe marché/compétitif · v1.10.0)** ·

Deux skills réels jamais chaînés jusqu'ici, branchés ici comme enrichissement **offert** (récolte largement faisable sans accès au compte de l'opérateur, par voie publique) ·

- `watch-competitors` (`subagent_safe: true`) · Meta Ads Library des concurrents (copy, créas, timing, angles/mécaniques observés, distribution awareness, espace blanc paid). Sortie · `brands/{brand}/strategy/competitive-intel-{slug}-{date}.md` + agrégat `brand.json#/market/`. Requiert `competitive-reading-doctrine.md` pour l'interprétation des signaux. MCP `facebook-graph` si dispo, sinon fallback paste URL.
- `trendtrack-enrich-brand` (`subagent_safe: true`) · intel brand externe via API TrendTrack (année de création, social, note Trustpilot, visites mensuelles, catégories, sample top ads + patterns de scaling). Sortie · proposals `brand.json#/identity` + `#/proofs` + `#/financials/monthly_visits` + `learnings.json`. Requiert `TRENDTRACK_API_KEY` (sinon skip propre, flag inconnu avec levier `connect-mcp-server`).

Offert au même gate que 4c (ou candidat pré-mine en fond dès Step 1-2). Reporté → poche `pending-validations.md` avec levier. Ces deux skills alimentent l'espace blanc paid (NIVEAU 2) et la section Observé du close avec du sourcé, pas de l'inféré.

When all 4a + 4b (+ 4c/4d si lancés) return, synthesize at orchestrator level into a single audience enrichi tableau (mère × sous-poches × pain_points + objections + JTBD × confidence chain), **plus une ligne marché/compétitif si 4c/4d ont tourné** (sophistication marché · dominant angle/mécanique concurrent · espace blanc). **NEVER** dump raw subagent output verbatim per delegation pattern §synthesis layer.

---

## GATE A · Operator validates audiences enrichies (preserved v1.3.0)

**MANDATORY GATE** before Phase 5. Surface the audience tableau, then AskUserQuestion:

- "Valide les audiences proposées, je continue sur les angles"
- "Corrige/affine d'abord, j'ouvre un drill sur {audience X}"
- "Stop, je veux relancer la voix client avant"
- "Autre"

If operator picks corrige → route to standalone `profile-audience` with focus, hold orchestrator state in `session-state.md`, resume on operator signal.

If operator picks stop → pause chain, route to `mine-voc` standalone.

**NEVER** proceed to Phase 5 without explicit validation. Audiences gate the entire downstream because Phase 5-9 fan out per audience.

---

## Step 5 · Delegate `weight-dimensions` via Task tool (brand-wide)

`weight-dimensions` is `subagent_safe: true`, `operator_facing: false`. Single subagent, brand-wide.

- `model: sonnet`
- Input: brand slug, validated audiences from Gate A
- Expected: internal audience × angle compatibility scores written to brand state (not exposed)

**Operator-facing line**:

> *"Je pré-compute les compatibilités angle × audience."* (one line, no detail)

**NEVER** surface raw numeric scores to operator. Compositional Cartography §7 enforcement.

---

## Step 6 · Delegate `produce-paid-angles` via Task tool (per top-3 audience)

`produce-paid-angles` is `subagent_safe: true`. Spawn one subagent per top-3 validated audience.

For each audience:
- `model: sonnet`
- Input: brand slug, audience id, weight-dimensions output
- Expected: angles ranked per audience using formula Obs + Tension + Reframe + Bridge, sourced from VoC verbatims where possible

**Operator-facing line**:

> *"Je génère les angles paid pour chaque audience top."*

When all return, synthesize into a per-audience angles tableau. Surface the top angle per audience with a 1-line rationale anchored on observed tension. **NEVER** expose internal scoring numbers.

**Rendu des angles · le BEAT, pas la météo (D#520).** Générer les angles paid est du travail lourd · la formule Obs+Tension+Reframe+Bridge appliquée par audience, les angles tirés des verbatims, ceux écartés parce que frontaux ou déjà saturés par la concurrence · ça ne se narre PAS en « angles produits ». Les sous-agents produce-paid-angles ont déposé le registre frais à `.phantom/beats/{slug}/angles.json` (doctrine SSOT · `docs/system/restitution-beat-doctrine.md`). Émets le beat en exécutant `python3 .skills/render-beat.py --brand {slug} --phase angles --mode orchestrated` et présente sa sortie TELLE QUELLE · le verdict tranché (quel angle porte le plus de tension observée, sur quelle audience) + le second ordre, puis le raisonnement (les angles cristallisés par audience, les pistes rejetées avec leur raison), puis ce qui reste prudent (angles à confiance moyenne · sample limité · le beat peut pointer le scoring qui les départagera), puis le CTA `/phantom {slug} matrix` teasé. NE re-narre PAS, NE re-résume PAS · le rendu déterministe EST le handoff. Le hook `beat-emit` te le rappelle si tu l'oublies. Mode `orchestrated` · le beat signale le cap, tu enchaînes vers le Gate B, tu ne demandes pas la permission de poursuivre.

**Filet** · si `render-beat` rend du vide (pas de payload déposé), retombe sur le tableau des angles en prose · ne laisse JAMAIS un trou à la place de la production d'angles. L'attendu reste le beat, le repli n'est qu'un garde contre la perte sèche.

---

## GATE B · Operator validates angles

**MANDATORY GATE** before Phase 7. Surface the angles tableau, then AskUserQuestion:

- "Valide les angles top, je continue sur les territoires + briefs + créas"
- "Corrige/affine, un angle est off sur {audience X}"
- "Stop, je veux re-mine VoC avant de produire les briefs"
- "Autre"

Same rejection logic as Gate A. **NEVER** proceed to Phase 7 without explicit validation. Angles gate briefs+créas because Phase 8-9 fan out per priority angle.

---

## Step 7 · Delegate `score-matrix` via Task tool (brand-wide)

`score-matrix` is `subagent_safe: true`, `operator_facing: true`. Single subagent, brand-wide.

- `model: sonnet`
- Input: brand slug, validated audiences (Gate A), validated angles (Gate B), weight-dimensions output
- Expected: Profil × Source d'angle matrix scored via canonical scoring, top-3 axes créatifs selected

**Operator-facing line**:

> *"Je build la matrice complète et je remonte les axes créatifs prioritaires."*

When subagent returns, surface only the **top-3 axes créatifs named in operator language** with prose rationale per axe (1-2 sentences anchored on audience tension + angle source). **NEVER** expose the full matrix grid with raw numbers. Compositional Cartography §7.

**Disambiguation lexicon v2.67** · "axe créatif" (micro · output score-matrix) vs "territoire" (macro · substrat atlas). Surface "axes créatifs" pour l'output ranking en Step 7. Le territoire macro = l'atlas substrate entier. Voir `docs/system/territory-doctrine.md`.

---

## Step 8 · Review & stage territories for downstream production

Territories prioritized (top-3 axes créatifs par score-matrix Step 7). Substrate complete. Atlas posé.

Next phase (outside this orchestrator) · materialize briefs + creatives via `creative-brief-composer` skill (separate invocation · operator chooses which axe créatif to materialize first).

**Operator-facing line**:

> *"Atlas substrat posé. 3 axes créatifs ranked. Prêt pour la phase production briefs+créas."*

---

## Phase Output Atlas · Visibility Matriciel Multi-niveau (canon v2.78.2)

**MANDATORY** post-encoding entités · présenter synthèse matricielle multi-niveau canon doctrine `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2 AVANT le Step 9 Close (Investigation Posture). Sans cette Phase, l'opérateur ne voit jamais la vue d'ensemble matricielle (product × pain × audience × positionnement × stage business) · output atlas reste prose-only · invalid.

Après encoding toutes entités atlas (brand · products · audiences · pains · objections · frictions · angles · offers · learnings · strategy), présenter OBLIGATOIREMENT synthèse matricielle multi-niveau canon decomposition-visibility-discipline v2.78.2.

### NIVEAU 1 · Décomposition produit cross-products

Pour chaque produit · table compacte décomposition specs · mécanismes · bénéfices 3 couches canon `docs/system/pain-benefit-chain.md` (functional · emotional · identity, layer chargé identifié explicit) ·

```
PRODUCT [name]
SPECS               MÉCANISMES                BÉNÉFICES 3 couches
[atome 1]           [atome action 1]          Functional · [bénéfice]
[atome 2]           [atome action 2]          Emotional  · [bénéfice]
                                              Identity   · [bénéfice]
                                                          ← layer chargé
```

Itérer pour les N produits encoded brand. Si produit unique · une table. Si multi-produits · N tables compactes empilées (séparateur visuel entre).

### NIVEAU 2 · Many-to-many · pain × audience matrix cross-atlas

Matrice ASCII OBLIGATOIRE cross-products + cross-audiences · skip = invalid output. Décompose explicitement quelle douleur frappe quelle audience avec intensité primary vs secondary ·

```
                       Audience-1    Audience-2    Audience-3   Audience-N
                       (slug)        (slug)        (slug)       (slug)
PNT-01 [pain label]      ✓✓ PRIMARY      ·            ✓           ·
PNT-02 [pain label]         ·         ✓✓ PRIMARY      ·           ✓
PNT-03 [pain label]         ✓             ✓        ✓✓ PRIMARY     ·
PNT-NN ...
─────────────────────────────────────────────────────────────────────
Espace blanc paid          ·         INCONTESTÉ      ·            ·
(compétitif intel)                   (5 concurrents
                                      sur axe unique)
```

Légende canon · `✓✓ PRIMARY` (douleur dominante audience) · `✓` (douleur secondaire affecte audience) · `·` (zéro affect). Row `Espace blanc paid` (optional · ship si signal compétitif détecté Phase 6 produce-paid-angles) · pour chaque audience, repère où concurrence est faible/inexistante sur l'angle → opportunité paid prioritaire.

### NIVEAU 3 · Positionnement filtre par stage business

Stage business détecté (signal ARR estimée · proof points · domain age · funding signals) OU opérateur-déclaré. Table canon ·

```
STAGE détecté            [early | growth | scale]
ARR estimée              [signal range]

AUDIENCE PRIORITAIRE     [audience slug + rationale 1 ligne]
ANGLES DOMINANTS         [3-5 angle ids ranked top]
POSITIONING STATEMENT    [Moore format si produce-positioning-canvas
                          shipped v2.80 · sinon stage hypothèse 1 ligne]

Distinction critique opérateur ·
Audience produit-fit     [toutes audiences encoded · ex audience-1 · audience-2 · audience-3]
Audience ciblage créa    [filter sub-set selon positioning targeting · ex audience-2 only stage early]
```

**HR · Stage business filter obligatoire si signal détectable.** ARR signal absent ET proof points absents ET domain age inconnu → flag `stage = inconnu` · ne pas inventer. Sinon · stage déclaré explicit.

**HR · Distinction explicit audience produit-fit vs ciblage créa.** Audience produit-fit = toutes audiences encoded Phase 4 (pertinentes pour le produit). Audience ciblage créa = sub-set filtré par positionnement stage-aware (ex · stage early → ciblage early adopters only, growth/scale audiences seront produit-fit mais pas ciblage créa runtime). Confusion = leak runtime · opérateur dépense paid sur audiences hors ciblage stage.

### NIVEAU 4 · Méthode pédagogique verbale

Verbaliser méthode décomposition canon · l'opérateur sait COMMENT l'atlas a été construit, pas seulement QUOI ·

> *"J'ai cartographié l'atlas {brand} en 4 niveaux canon ·*
> *1. Décomposition produit · specs/mécanismes/bénéfices 3 couches (functional · emotional · identity, layer chargé identifié)*
> *2. Many-to-many · {N} pains × {M} audiences (matrix primary/secondary affectations · espace blanc paid si signal compétitif)*
> *3. Stage business · {stage détecté} → audience prioritaire {slug} · {3-5 angles dominants}*
> *4. Positionnement filter · {produit-fit toutes audiences} vs {ciblage créa sub-set stage-aware}*
>
> *L'atlas est désormais opérable cross-skills downstream · `produce-paid-angles` · `creative-brief-composer` · `compose-creative`. Validation systémique opérée par confidence chain explicit cross-entity."*

**HR · Méthode pédagogique verbale obligatoire post-matrices.** Skip = opérateur ne sait pas comment l'atlas a été construit · runtime downstream skills consomment l'atlas en aveugle · debugging downstream impossible.

---

## Step 9 · Close (Investigation Posture, 5 sections MANDATORY)

**CRITICAL**: this is a strategic deliverable orchestrator, not a setup orchestrator. Investigation Posture is mandatory per `docs/system/investigation-posture.md`. Five sections explicit:

### Observé
What the pipeline produced, sourced. Audiences validated at Gate A, angles validated at Gate B, top-3 axes créatifs selected by score-matrix. Quantify (number of audiences, number of angles per audience, number of axes créatifs ranked). Never expose scoring numbers.

### Déduit
Hypotheses with explicit confidence chain. Examples per atlas type:
- "L'audience mère **{name}** ressort comme prioritaire (confidence **forte** · convergence VoC + VoM)."
- "L'angle **{name}** sur l'audience **{name}** porte le plus de tension observée (confidence **moyenne** · verbatims solides mais sample size limité)."
- "L'axe créatif **{name}** combine audience à haut volume + angle peu exploité par les concurrents (confidence **moyenne** · projection à valider en test)."

Confidence chain: **forte** / **moyenne** / **faible** / **TRÈS faible**. Never invent confidence. Never present hypothesis as fact.

**Le Déduit est à DEUX faces, toujours potentiel (D#517).** Pas seulement les opportunités (le non-vu, la zone blanche dérivée du mécanisme), mais aussi les **faiblesses potentielles** (le fragile, le sous-exploité, le risque dans la marque ou le compte). Les deux sortent en hypothèses-avec-confiance, jamais en faits.
- **Humble-contextuel** · juger AU STADE (`brand.meta.stage`) · une faiblesse n'existe pas dans l'absolu · marge serrée = fatal en scale, OK en land-grab · cible étroite = force pour un focus, faiblesse pour le volume. Ne JAMAIS challenger un cœur prouvé (`is_core`). Chaque faiblesse sort taguée potentielle + remise dans son stade + « voilà ce qui confirmerait que c'est un vrai défaut et pas un choix délibéré ». Jamais un audit de faiblesses générique balancé sur un cœur qui convertit.
- **Trois couches, jamais confondues** · ce que la marque CLAIME (le site) ≠ qui CONVERTIT (le back-end, inconnu tant que le compte n'est pas branché) ≠ l'OPPORTUNITÉ (dérivée du mécanisme, pas du miroir des avis). Une lecture qui ne sépare pas les trois est une transcription, pas une intelligence.

**Proactif par MATÉRIALITÉ, jamais par curiosité (D#517).** Le système ne creuse/ne demande pas plus d'info sur tout · il le fait précisément quand un flou change une conclusion qui paie (valeur d'info = réduction d'incertitude × poids de la décision). Un flou sur une faiblesse anodine reste en réserve · un flou sur le moteur de revenu ou la marge qui décide du break-even déclenche le levier (creuser, demander, ou proposer de brancher un outil).

**Postcondition sur l'ARTEFACT, jamais sur l'invocation (D#517).** À chaque handoff, l'orchestrateur vérifie l'empreinte ÉCRITE du sous-agent, pas le fait de l'avoir lancé · « `spec.use_cases[]` a ≥1 `speculative` ET `spectrum.json` existe » avant la phase 3, pas « j'ai délégué map-audiences ». La précondition teste la QUALITÉ (mechanisms riche, use_cases avec spéculatif), pas seulement l'existence. Artefact manquant ou dégénéré → relancer, ne pas avancer.

### Inconnu
Variables non observables sans test live ou data additionnelle. Examples:
- "Volume réel de l'audience mère sur Meta (non mesurable sans audience-builder test)."
- "Performance comparative des angles sur le marché actif (non mesurable sans déploiement budget test)."
- "Sensibilité prix au-delà du tier offers.json actuel (non mesurable sans split-test landing)."

### Leviers
Skills / actions / sources pour lever les inconnues. Examples:
- "Test campagne Meta sur l'audience mère + 2 angles top (skill `audit-meta-account` post-déploiement)."
- "Mine VoC additionnel sur source spécifique (skill `mine-voc --focus={axis}`)."
- "Refine angles si Gate B a laissé des hypothèses floues (skill `produce-paid-angles --focus={audience}`)."
- **Offre de connexion des outils (v1.10.0 · HR-AXIS-6)** · les inconnus des axes économie, funnel et média se lèvent par le branchement · proposer explicitement à l'opérateur de connecter ses outils, en proposition groupée et en langage opérateur · commerce/CMS (levier `connect-source` · ouvre l'économie réelle + le bas du funnel) · plateformes paid Meta/Google (levier `connect-source` / `import-meta-results` puis `audit-meta-account` · ouvre structure de compte + ROAS réel) · analytique/email/productivité (levier `connect-source` ou `connect-mcp-server` · ouvre rétention + flows + contexte). Affordance qui s'ajoute aux Leviers, pas la question macro du Close ouvert. Report propre vers `pending-validations.md`, jamais imposé.

### Close · le verdict de move
Le close **AFFIRME** un move, il ne rend pas une question à arbitrer. Le move n'est PAS prescrit par une forme · il se PRODUIT en faisant tourner la chaîne diagnostique sur le substrat déjà encodé (position → espace blanc → audiences-du-mécanisme → priorité-éco → verdict · `docs/doctrine/strategic-diagnostic-doctrine.md`), comme au NIVEAU LIVE, mais sur l'atlas refermé. Le move tombe de ce que tu LIS dans le substrat, pas d'un gabarit. Posture du close (affirme par défaut · ouvre un inconnu réel · au plus un gate) · `docs/system/investigation-posture.md` + `docs/system/contextual-intelligence.md`, ne pas re-coller le contrat ici. Affirme ce qu'on FAIT, jamais une hypothèse comme un fait (le move s'appuie sur le Déduit qui porte sa confidence).
**L'out honnête est un move, pas un cop-out.** Quand le substrat ne porte pas encore de move tranché, nomme la SEULE inconnue bloquante + le chemin exact pour la lever, et avance la part faisable en parallèle (« je ne tranche pas la cible sans ta marge réelle · donne-la moi, sinon j'avance sur la page et on chiffrera après »). Ça reste une lecture qui décide. Inventer un verdict pour faire décisif est l'échec, pas l'inverse.

Le drill-down macro (« ou tu préfères enrichir le territoire d'abord ») reste une affordance de redirection offerte en une ligne trailing SI elle est réelle, jamais le défaut · le close tranche, il ne tend pas un menu d'axes. Le worked example (verdict tranché + out honnête vs météo molle) vit dans l'exemplar, pas re-collé ici.

**Auto-critique avant de surfacer le close (D#52x).** Relis ton close contre affirme/ouvre/gate · est-ce qu'il TRANCHE un move défendu, ou est-ce qu'il décrit l'état et rend une question (bulletin météo · « lequel veux-tu creuser ? », menu d'axes symétrique) ? Si c'est la météo, réécris-le en verdict avant de l'émettre.

**Exemplar** · la paire tranché vs mou (le close qui affirme un move défendu vs celui qui décrit et rend un menu) · `resources/canon/exemplars/close.md` (lecture diagnostique · `resources/canon/exemplars/diagnostic.md`).

**NEVER** orphan close. **NEVER** flat menu d'axes symétrique. **NEVER** une question qui n'est pas un gate (un inconnu se OUVRE, il ne s'arbitre pas sur le bureau de l'opérateur).

### Beat de restitution du close · build-atlas EST le producteur (D#520)

Au scan, aux audiences, au spectre et aux angles, un SOUS-AGENT déposait le payload et toi tu l'émettais. Au close il n'y a pas de sous-agent · **c'est TOI le producteur**, tu portes la lecture stratégique sur les 5 axes (cohérent D#519 · l'orchestrateur POSSÈDE le close, jamais délégué). Donc tu fais les DEUX gestes · tu ÉCRIS le payload puis tu l'ÉMETS.

**1. Écris le payload (`Write`, hors gate mutation · c'est sous `.phantom/`, hors `brands/`, donc PAS via `write-to-context`).** Fichier `.phantom/beats/{slug}/close.json`. Doctrine SSOT · `docs/system/restitution-beat-doctrine.md` (contrat, décision-d'abord, richesse second-ordre). Le close est **terminal** · `phase: "close"`, vue `/phantom {slug} atlas`, PAS de forward-look (pas de `_Et après_` · la chaîne d'encodage s'arrête là, le code le sait via `PHASE_NEXT["close"] == ""`). Le `tease` ne tease pas une phase suivante du pipeline mais la **prochaine ACTION opérateur** (le premier brief créa via `creative-brief-composer` sur l'axe top, ou la capture des chiffres éco/le branchement du compte paid pour ouvrir les axes en brouillard). Paramètres de TA phase ·

```json
{
  "phase": "close",
  "verdict": "<le verdict global TRANCHÉ · où va la marque, où ça paie, en une ligne (cohérent close D#517 · tranche quand les lectures convergent, ne laisse pas en question ouverte)>",
  "read": "<2-3 phrases · la lecture sur les CINQ axes (économie unitaire · funnel · média · créa/message · marché-compétitif) · le second ordre, le nerf · ce que l'atlas rend opérable maintenant>",
  "found": ["<les pièces posées de l'atlas · N audiences · M angles · top-3 axes créatifs · amorce grasse possible (la thèse de chaque axe)>"],
  "analyzed": ["<les top-3 axes prioritaires DÉFENDUS · pourquoi cet axe d'abord · ce qu'il débloque / dérisque / définit comme catégorie>"],
  "rejected": [{"what": "<axe ou angle écarté>", "why": "<la raison défendable>"}],
  "blocked": [{"source": "<ex compte paid non branché>", "reason": "<ROAS réel / structure de compte invisible au scan>"}],
  "confidence": [{"claim": "<assertion sur un axe>", "level": "moyenne|faible", "reason": "<la VRAIE cause · projection à valider en test, sample limité, compte non branché>"}],
  "encoded": ["<l'atlas substrat posé · specs + offres + audiences enrichies + angles ranked + territoires scorés>"],
  "basis": "<une ligne · l'étendue du travail · audiences cartographiées, voix client minée, angles produits, matrice scorée>",
  "tease": "<l'accroche vers la prochaine ACTION opérateur · le premier brief créa sur l'axe top, OU la capture des chiffres éco / le branchement du compte pour lever les axes en brouillard · PAS de chemin, le code ajoute /phantom {slug} atlas>"
}
```

Champ vide = omis, jamais inventé. Ce qui reste inconnu (les axes éco/funnel/média en brouillard) vit dans `blocked` + `confidence` non-forte AVEC son levier (le branchement, la capture opérateur) · cohérent avec les cases déjà persistées dans `pending-validations.md` (Principe 2), le beat les restitue, il ne les ré-invente pas.

**2. Émets-le** · `python3 .skills/render-beat.py --brand {slug} --phase close --mode orchestrated` et présente sa sortie TELLE QUELLE. Le renderer réorganise en décision-d'abord (verdict + lecture 5-axes, puis le raisonnement des axes prioritaires, puis ce qui reste prudent avec sa cause, puis « Lu · », puis le CTA `/phantom {slug} atlas` + le tease de la prochaine action). Le close étant terminal, le renderer n'appose AUCUN forward-look · le tease porte seul la suite (l'action opérateur). NE re-narre PAS · le beat est la restitution mécanique de l'Investigation Posture que tu viens de poser, il garantit que le verdict tranché et la confiance-avec-sa-cause ne s'effondrent pas en météo.

**Articulation avec le Close ouvert (5 sections).** La synthèse Investigation Posture 5 sections (Observé / Déduit / Inconnu / Leviers / Close ouvert) reste le rendu opérateur-facing principal · le beat close est sa restitution décision-d'abord pour le record et la cohérence cross-phase (même grammaire que scan/audiences/spectrum/angles). Le verdict de move du close (affirme · ouvre · gate · cf section ci-dessus) n'est pas un forward-look de pipeline · il reste porté par la section close, le `tease` du beat le double en CTA paste-ready vers l'action.

**Filet** · si `render-beat` rend du vide (payload pas écrit ou illisible), retombe sur la synthèse 5 sections en prose · ne laisse JAMAIS un trou à la place du close. L'attendu reste le beat, le repli n'est qu'un garde contre la perte sèche.

---

## Step 10 · Finalize

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
python3 .skills/build-brand-snapshot.py {slug}
```

Update status.json:
- `last_atlas_build_run`: timestamp
- `atlas_substrate_complete`: true
- `audiences_count`, `angles_count`, `axes_creatifs_count`
- emit `atlas_substrate_staged` event

Trigger `learn-from-session` batch (posture adaptive, operational/ship register): briefer 5-7 bullets max sur ce qui a été produit (territoire substrat, pas briefs+créas), close binaire ("1 arbitrage à faire" = Close ouvert macro, ou "RAS, atlas posé, prêt pour `creative-brief-composer`").

---

## Operator cartography (before Phase 0, if complex brief)

If the operator typed a minimal brief ("build atlas {brand}") without context, briefly cartograph the pipeline before executing (~5 lines, operator language, no system jargon):

> *"Analysé. Atlas substrat complet en 4 paliers progressive cartography, voilà comment je vais piloter :*
> *• **Palier 1+2** · structure ta marque + scan le site. **Gate light** entre les paliers : tu valides territoire produit + offers*
> *• **Palier 3** · cartographie audiences hiérarchique mère + sous-poches. **Gate light** : tu valides l'arbre*
> *• **Palier 4** · mine voix client + enrichis les profils audiences validées. **Gate A** : tu valides audiences enrichies*
> *• Produits les angles paid ranked par audience. **Gate B** : tu valides les angles*
> *• Build la matrice complète et remonte les top-3 axes créatifs ranked*
> *• Clôture avec un drill-down · soit on enchaîne briefs+créas via `creative-brief-composer` sur l'axe que tu choisis, soit on enrichit le territoire d'abord"*

Si `fast_track = true` détecté · *"Mode opérateur expert · gates light intermédiaires bypass auto-validate, stop seulement Gate A + Gate B."*

Then AskUserQuestion: *Go / Skip URL scan / Active fast-track / Ajuste le pipeline (skip une phase) / Autre*.

---

## Guardrails

- **HR-NEW · Phase output Atlas Visibility Matriciel obligatoire (v1.6.0)** · post-encoding entités atlas (brand · products · audiences · pains · objections · frictions · angles · offers · learnings · strategy) · Phase Atlas Visibility 4 niveaux canon obligatoire AVANT Step 9 Close. Skip = invalid output (l'opérateur ne voit jamais la vue d'ensemble matricielle product × pain × audience × positionnement × stage business). Doctrine racine · `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2.
- **HR-NEW · 4 niveaux matriciels canon obligatoires (v1.6.0)** · NIVEAU 1 Décomposition produit cross-products · NIVEAU 2 Many-to-many pain × audience matrix cross-atlas · NIVEAU 3 Positionnement filtre par stage business · NIVEAU 4 Méthode pédagogique verbale. Skip 1 = invalid output.
- **HR-NEW · Many-to-many matrix cross-products + cross-audiences obligatoire (v1.6.0)** · ASCII matrix explicite avec `✓✓ PRIMARY` / `✓` / `·` symboles canon · skip = matrix implicite cross-products force opérateur à déduire affectations pain × audience.
- **HR-NEW · Stage business filter obligatoire si signal détectable (v1.6.0)** · ARR estimée + proof points + domain age + funding signals → stage déclaré explicit (early/growth/scale). Aucun signal détectable → flag `stage = inconnu` · NEVER inventer.
- **HR-NEW · Audience produit-fit vs ciblage créa distinction explicit (v1.6.0)** · audience produit-fit = toutes audiences encoded Phase 4 · audience ciblage créa = sub-set filtré par positionnement stage-aware. Confusion = leak runtime · opérateur dépense paid sur audiences hors ciblage stage. Skip = invalid output.
- **HR-NEW · Méthode pédagogique verbale obligatoire post-matrices (v1.6.0)** · verbaliser les 4 niveaux canon de cartographie atlas appliqués · skip = opérateur ne sait pas comment l'atlas a été construit · runtime downstream skills consomment en aveugle · debugging impossible.
- **AP-NEW · Encodage atlas silent sans synthèse matricielle finale (v1.6.0)** · NEVER ship atlas substrat sans Phase Atlas Visibility · `build-atlas-complete` v1.6.0+ MUST surface synthèse matricielle multi-niveau post-encoding entités.
- **AP-NEW · Synthèse prose-only sans Phase Atlas Visibility (v1.6.0)** · NEVER substitute Investigation Posture 5 sections Close (Step 9) en lieu de Phase Atlas Visibility matricielle (Step 8.5). Close consomme la synthèse matricielle en amont, ne la remplace pas.
- **AP-NEW · Many-to-many implicite cross-products (v1.6.0)** · NEVER force opérateur à déduire affectations pain × audience par inférence prose · ASCII matrix explicite obligatoire (NIVEAU 2 canon).
- **AP-NEW · Stage business absent du filtre positionnement (v1.6.0)** · NEVER skip stage filter si signal détectable · stage = inconnu acceptable seulement si zéro signal · NEVER inventer stage.
- **AP-NEW · Méthode pédagogique skip (v1.6.0)** · NEVER ship atlas matriciel sans verbaliser COMMENT l'atlas a été construit · l'opérateur perd la grammaire de raisonnement runtime.
- **HR · Gates entre Phases canon (v1.4.0)** · build-atlas-complete v1.4.0+ doit insérer **gate light entre Phase 2 (drilling) → Phase 3 (audiences hiérarchique) → Phase 4 (enrichissement)**. Anti-pattern · chain skills sans validation operator entre paliers progressive cartography (dump synthesis bloc canon précédent v1.3.0 où seuls Gate A + Gate B existaient). Doctrine `docs/system/progressive-cartography-doctrine.md` Section 8 Pattern gates light · format 1-2 lignes synthesis + 1 binaire validation/correction. Pas Q&A verbeux.
- **HR · Fast-track opt-in opérateur expert (v1.4.0)** · gates intermédiaires auto-validate **seulement si opérateur explicit** (flag `--fast-track` passed dans invocation) OR config opt-in (`operator/profile.json#preferences.auto_validate_after_n_brands` true détecté). Default = gates light visible. Premier-contact opérateur garde gates pour repère cognitif. Gate A + Gate B **toujours preserved** quel que soit le mode (structural decisions audiences finales + angles ranked, jamais bypass).
- **NEVER** run all phases sequentially blocking on one operator without heartbeat. Surface progress at each gate.
- **NEVER** skip Gate A or Gate B silently. Audiences gate angles, angles gate scoring. Skipping = fan-out on unvalidated hypotheses = wasted calls + low-quality atlas substrate.
- **NEVER** skip Gate Intermédiaire 1 or Gate Intermédiaire 2 sans `fast_track = true` opt-in explicit. Gates light visible default · premier-contact opérateur a besoin du repère cognitif entre paliers progressive.
- **NEVER** expose Task tool mechanics, subagent internals, or skill names to the operator ("I spawned profile-audience", "produce-paid-angles returned"). Say what it *does*: "je cartographie les audiences", "je génère les angles".
- **NEVER** re-implement subskill logic. If a subskill has a bug or gap, fix it there, not here. Pure orchestrator per `onboard-brand` precedent.
- **NEVER** expose raw scoring numbers, confidence floats, weight-dimensions matrix values, or internal field paths. Compositional Cartography §7 anti-pattern enforcement.
- **NEVER** freestyle prose for an output where a downstream skill exists. Skill routing canon v2.55 enforcement · invoke `produce-paid-angles`, never write angles in prose. The orchestrator delegates; it does not produce strategic content directly.
- **NEVER** produce briefs copy ou créas in this orchestrator (v1.3.0 territoire-pure scope). Briefs+créas materialization happens downstream via `creative-brief-composer` (separate skill, separate invocation). Voir `docs/system/territory-doctrine.md`.
- **NEVER** dump raw subagent output verbatim. The orchestrator main is the synthesis layer per delegation pattern.
- **ALWAYS** persist `brands/{slug}/session-state.md` rolling update after each phase (crash resumption).
- **ALWAYS** propagate confidence chain phase-by-phase per `docs/system/confidence-propagation.md`. Worst-case floor wins on the final synthesis.
- **ALWAYS** apply Investigation Posture 5 sections on Step 9 close. The audit gap that triggered v1.0.0 was exactly this missing structured close.
- **ALWAYS** respect parallel cap (3 subagents per phase) and depth cap (1 · `deepen-brand-context` already chains its own subagents, that is depth-2 already authorized by the architecture).
- **ALWAYS** Brand isolation: this orchestrator operates `brand_only` per `docs/system/brand-isolation-doctrine.md`. Cross-brand pulls (canon copy resources) are read-only references, never write to other brands.
- **One brand at a time.** No parallel atlas-build on multiple brands. Confuses Layer B mutation scoping.

---

## Doctrine onboarding · 4 principes orchestrateur (canon onboarding-setup-flow · v1.9.0)

Cette section instrumente les quatre principes que la doctrine `docs/system/onboarding-setup-flow.md` (section « Câblage sur l'orchestrateur existant ») désigne comme manquants au niveau orchestrateur. Le pipeline reste celui des Steps 0-10 · cette section AJOUTE des hooks qui se greffent aux gates et caps déjà présents, sans rien retirer. **Ne pas rédupliquer la doctrine · la lire** (les principes 1 à 8 non négociables, l'enchaînement 10 phases, les garde-fous d'audit y vivent). Ce skill couvre déjà 8 des 10 phases · on l'étend, on ne le double pas.

### Principe 0 · PORTE en amont (accepter d'être précédé par onboard-brand)

`build-atlas-complete` accepte d'être **précédé** par le pré-vol, l'inférence de profil et le pacte d'accueil de `onboard-brand` comme **phase 0** (cf doctrine · « brancher le pré-vol... de onboard-brand en amont de build-atlas-complete · délégation, pas duplication »). Quand l'entrée vient d'un froid total (état zéro), `onboard-brand` tient la porte (squelette + scan + validate) puis **handoff explicite** vers ce pipeline pour les phases 4 à 9. **Purity rule préservée** · ce skill n'implémente AUCUNE logique d'accueil · il consomme l'état posé par `onboard-brand` (brand.json identité + snapshot + profil opérateur inféré) et reprend au palier d'enrichissement. Si l'opérateur arrive déjà via `onboard-brand`, NE PAS re-jouer Step 0 disclosure pré-vol ni Step 1 setup (déjà fait amont) · reprendre au Palier Phase 3/4 selon l'état `status.json`. Si l'opérateur invoque ce skill en direct (sans onboard-brand amont), Step 0 + Step 1 tournent normalement (porte interne). La porte est externe OU interne, jamais doublée.

### Principe 1 · DEUX GESTES par pièce (agir / creuser, affordance permanente)

À **chaque sortie de phase** (pas seulement au close), remonter au niveau orchestrateur le **doublet agir/creuser** que les producteurs portent déjà localement (cf doctrine · « remonter au niveau orchestrateur le doublet agir/creuser que les producteurs portent déjà localement, à chaque sortie de phase, pas seulement au close »). Le geste **agir** = le pas concret suivant du pipeline. Le geste **creuser** = drill/décomposition de la pièce qui vient d'être posée, comme affordance omniprésente et indéfiniment disponible, pas une branche réservée.

Câblage sur les gates déjà présents (additif, le close binaire existant est préservé) ·

- **Gate Intermédiaire 1** (territoire produit posé) · agir = *« on attaque la cartographie audiences »* · creuser = *« j'ouvre le produit jusqu'à ses mécanismes / usages adjacents »*.
- **Gate Intermédiaire 2** (arbre audiences posé) · agir = *« on enrichit la voix client »* · creuser = *« j'ouvre une audience-mère pour voir ses sous-poches »*.
- **Gate A** (audiences enrichies) · agir = *« je produis les angles »* · creuser = *« j'ouvre une douleur jusqu'à ses verbatims »*.
- **Gate B** (angles ranked) · agir = *« je lance le scoring »* · creuser = *« j'ouvre un angle jusqu'à son graphe de dépendances »*.
- **Step 8 / Step 9** (territoires scorés + close) · agir = *« on matérialise briefs + créas via creative-brief-composer »* · creuser = *« on enrichit le territoire / on ouvre un inconnu »* (déjà couvert par le Close ouvert, étendu ici en affordance explicite).

Le doublet se formule en langage opérateur (zéro nom de skill, zéro chemin) et s'ajoute APRÈS le binaire de validation du gate, jamais à la place. C'est une affordance offerte, pas une question bloquante de plus.

### Principe 2 · INCONNUS = cases ouvertes navigables avec levier in situ

Chaque **inconnu** (zone blanche d'angles sur une audience, trou de scoring sur une intersection, draft à confiance **faible** ou **TRÈS faible**) devient une **case ouverte navigable avec son levier pré-amorcé**, écrite **au moment où elle surgit** (in situ), pas agrégée en une liste de clôture (cf doctrine · « chaque inconnu devient une case ouverte navigable avec son levier pré-amorcé, pas une liste agrégée en clôture »). Discipline de pré-amorçage héritée des garde-fous d'audit · le levier se **pré-amorce** (la question renvoyée à l'opérateur est d'abord réduite à coût nul par ce qui est tranchable seul · recoupements publics), il ne se propose pas brut.

Câblage (additif · persistance native, cohérent avec la Mutation rule) · dès qu'une phase produit un inconnu, l'écrire comme item dans `brands/{slug}/pending-validations.md` avec · (a) la **case** (ce qui manque, formulée comme champ à remplir), (b) la **confiance** courante si c'est un draft faible, (c) le **levier** pré-amorcé (le geste qui la lèverait · ex re-mine VoC sur source X · audience-builder test · split-test prix). La section **Inconnu** + **Leviers** du Close (Step 9) **agrège ensuite** ces cases déjà persistées · elle ne les invente pas en fin de course, elle référence des cases navigables déjà ouvertes en cours de route. Ne JAMAIS laisser un inconnu vivre uniquement en prose de synthèse · trou muet interdit.

### Principe 3 · EXHAUSTIVITÉ offerte + reportable (à chaque cap)

À **chaque cap** du pipeline (top-3 audiences, top-5 angles par audience, top-3 axes créatifs), **présenter** explicitement le choix · *« tout cartographier maintenant ou je reporte le reste dans la todo »*, **expliquer ce qu'on perd** à sauter (sérieux, vivant, pédagogique · ce que la couverture complète apporte concrètement), et **écrire les poches non couvertes** comme items reprenables vers `pending-validations.md` avec leur levier (cf doctrine · « présenter tout cartographier maintenant ou je reporte le reste dans la todo, expliquer ce qu'on perd, et écrire les poches non couvertes comme items todo reprenables avec leur levier »).

Le pipeline va jusqu'au bout de la dépendance, mais l'opérateur n'est jamais **contraint** d'aller jusqu'au bout en une fois · l'atlas reste utilisable à tout stade de complétude et se densifie quand l'opérateur revient sur les morceaux différés. La poche différée s'écrit dans la todo comme une case reprenable **avec son levier** · persistée, pas laissée en prose.

Câblage sur les caps déjà présents (additif · la cardinalité top-3/top-5/top-3 et la scope discipline territory-doctrine sont préservées) ·

- **Cap audiences** (Phase 3 · top-3 mère retenues pour Phase 6) · les audiences-mère et sous-poches hors top-3 ⇒ poches reportées avec levier `map-audiences --focus` / `profile-audience` ultérieur.
- **Cap angles** (Phase 6 · top-5 ranked par audience puis dédoublonnés) · les angles candidats hors top-5 ⇒ poches reportées avec levier `produce-paid-angles --focus={audience}`.
- **Cap axes créatifs** (Phase 7 · top-3 axes) · les intersections audience × source d'angle non priorisées + les **trous de scoring** ⇒ poches reportées avec levier (expand audiences · re-mine VoC sur angle manqué).

Court-circuit aligné sur le mode existant · `fast_track = true` peut auto-reporter silencieusement (log) les poches sous le cap sans présenter le choix à chaque cap · l'écriture vers `pending-validations.md` reste obligatoire (reportable preservé même en mode expert).

### Fixes runtime hérités de l'audit (additif)

- **Scan en direct, inférence visible** · le scan du site (Step 2 snapshot) tourne avec son **inférence visible dans le fil principal** (produit → mécanisme → bénéfice → pain → audience), **jamais en sous-agent muet** · seul le mécanique brut (fetch, crawl, dump avis) part en silence, pour que l'opérateur corrige une inférence **avant qu'elle soit gravée**. Tout silence agent > 90 s émet un micro-signal de progression (cohérent avec le heartbeat chairman déjà imposé en section Tone). Ce qui n'a pas pu être scrapé est posé comme case à remplir avec son levier (principe 2).
- **Pré-mine en fond pendant l'atelier d'identité** · `mine-voc` et `profile-audience` se **pré-minent en fond** pendant qu'on calibre l'identité avec l'opérateur (Step 1 + Step 2), au lieu d'attendre la fin de Phase 3 · proactivité par parallélisation (sous-agents spécialisés, cap 3 parallel préservé). La durée perçue ≈ le plus long des travaux, pas leur somme. Les profils pré-minés restent des **drafts** consommés/affinés à Phase 4 une fois l'arbre audiences validé au Gate Intermédiaire 2 · ils ne court-circuitent ni Gate Intermédiaire 2 ni Gate A.

### Règles dures (onboarding doctrine · v1.9.0)

- **HR-ONB-1 · Deux gestes à chaque sortie de phase.** Tout gate (Intermédiaire 1, Intermédiaire 2, A, B) et Step 8/9 surface le doublet agir/creuser en langage opérateur, en plus du binaire de validation. Skip = affordance creuser perdue, l'opérateur croit que seul le pas suivant existe.
- **HR-ONB-2 · Inconnu persisté in situ avec levier.** Tout inconnu (zone blanche d'angles, trou de scoring, draft confiance faible/TRÈS faible) s'écrit dans `pending-validations.md` au moment où il surgit, avec son levier pré-amorcé. Le Close (Step 9) agrège ces cases déjà ouvertes · il ne les crée pas en fin de course.
- **HR-ONB-3 · Exhaustivité offerte + reportable à chaque cap.** À chaque cap (top-3 audiences, top-5 angles, top-3 axes), présenter « tout cartographier maintenant ou je reporte le reste dans la todo », expliquer ce qu'on perd, écrire les poches sous le cap vers `pending-validations.md` avec leur levier. En `fast_track`, report silencieux toléré mais écriture toujours obligatoire.
- **HR-ONB-4 · Scan inférence visible + pré-mine en fond.** Le scan tourne avec inférence visible dans le fil (jamais sous-agent muet), micro-signal si silence > 90 s · `mine-voc` + `profile-audience` se pré-minent en fond pendant l'atelier d'identité (drafts, ne court-circuitent aucun gate).
- **AP-ONB-1 · Menu plat de validation sans deux gestes.** NEVER surfacer un gate avec seulement « valide / corrige » sans le doublet agir/creuser · l'affordance de drill omniprésente est canon onboarding.
- **AP-ONB-2 · Inconnu en prose-only agrégé au close.** NEVER laisser un inconnu vivre uniquement en prose de synthèse de fin · trou muet interdit, persistance native obligatoire au moment où il surgit.
- **AP-ONB-3 · Cap silencieux sans offre d'exhaustivité.** NEVER appliquer un cap (top-3/top-5/top-3) en jetant silencieusement les poches sous le cap · présenter le choix (ou reporter en log si `fast_track`) + écrire les poches reprenables avec levier.
- **AP-ONB-4 · Scan en sous-agent muet.** NEVER faire tourner le scan du site comme sous-agent silencieux qui dump une inférence déjà gravée · l'inférence reste visible dans le fil pour correction amont.
- **HR-ONB-5 · Registre pair-expert tenu sur toute la cascade (D#519).** Chaque handoff, heartbeat et close TRANCHE, sépare le vu du déduit, pose les reports comme des faits secs. Le rail de ton de la porte (/tour) se tient jusqu'au close, c'est sur la longueur qu'il faut le tenir.
- **AP-ONB-5 · Close de validation procédurale (D#519).** NEVER fermer une phase sur « valide / corrige / réoriente / type something », et SURTOUT jamais sur « tape valide ou ok pour débloquer l'écriture » (écrit dans `pending-validations.md` comme unlock). Le gate macro valide une PIÈCE, il ne se substitue jamais à la reco · la phrase de déblocage procédural est un orphan-close persisté, banni (observé run onday · `pending-validations.md` « Taper valide ou ok pour débloquer le profil audience »). Le close tranche un verdict de move.
- **AP-ONB-6 · Dérive concierge dans l'encodage (D#519).** NEVER « jamais perdu », « je te ping », « petite note d'honnêteté », « ça arrête d'être une démo », réassurance de coach ou punchline de vente dans le fil d'encodage. Le report est sec, le close tranche · la chaleur ne remplace pas la précision (observé run onday · registre molli en concierge poli sur la cascade).

Cross-ref · `docs/system/onboarding-setup-flow.md` (doctrine source · principes non négociables + enchaînement 10 phases + câblage enrich-pas-create + fixes runtime audit) · `docs/system/progressive-cartography-doctrine.md` §8 (pattern gates light, base des deux gestes) · `docs/system/investigation-posture.md` (Inconnu + Leviers du Close agrègent les cases persistées) · `.skills/skills/onboard-brand/SKILL.md` (porte amont · handoff vers ce pipeline phases 4 à 9).

---

## Câblage des cinq axes de la récolte (canon onboarding-setup-flow · v1.10.0)

Cette section instrumente la grille des **cinq axes de décompo e-com** que la doctrine `docs/system/onboarding-setup-flow.md` (section « Les cinq axes de la récolte » + « Câblage des cinq axes de la récolte ») impose à la récolte d'infos, pour qu'un atlas ne couvre pas seulement la créa. Elle applique `docs/system/open-map-reasoning.md` (raisonnement à carte ouverte) sur la grille e-commerce complète · chaque axe rend la figure ET le fond, route vers un skill réel **ou** se pose en inconnu typé avec son levier, jamais un trou silencieux. **Ne pas rédupliquer la doctrine · la lire.** Cette section dit seulement OÙ chaque axe se branche dans ce pipeline. Le scan ne voit que la devanture · la frontière est nette · ce qui se lit entre en observé, ce qui ne se lit pas (l'économie réelle, la rétention, le ROAS réel) entre en inconnu typé avec levier.

**Axe créa et message (axe 4)** · déjà nativement câblé sur les Steps 1 à 9 (setup-brand, snapshot-brand, map-mechanisms, map-benefits, map-audiences, mine-voc, profile-audience, produce-paid-angles, score-matrix). Colonne vertébrale du pipeline. Rien à ajouter · listé pour rappeler que les quatre autres axes ne le remplacent pas, ils l'entourent.

**Axe marché et compétitif (axe 5)** · câblé en **Sub-step 4c** (`mine-vom` brand-wide, RESTAURÉ v1.10.0) + **Sub-step 4d** (`watch-competitors` + `trendtrack-enrich-brand`, OFFERTS), plus le Spectre Step 2.5 (`map-angles` mode spectre) qui consomme ce substrat. Récolte largement faisable sans branchement, par voie publique. Skills additionnels invocables au close comme enrichissement profond · `study-niche-marketdeepdive`, `decompose-ad`, `produce-positioning-canvas`. Reportable · poche `pending-validations.md` avec levier si non lancé au Gate Inter 2.

**Axe média (axe 3)** · route vers des skills réels **quand le compte est branché** · `audit-meta-account` (setup compte publicitaire · pixel, structure, attribution, sécurité), `audit-google-pmax` (régie search complémentaire), `analyze-perf` (lecture de performance multi-jours · CAC, ROAS, COS). Levier de branchement · `connect-source` (ou `import-meta-results` pour injecter un export). **Compte non branché** · la structure de compte, le budget et le ROAS réel se posent en **inconnu typé** dans `pending-validations.md`, levier `connect-source` sur le compte publicitaire · le compétitif paid se récolte quand même par voie publique via `watch-competitors` (4d). Le ROAS réel n'est JAMAIS inféré depuis le site.

**Axe économie unitaire (axe 1)** · pas-encore-outillé honnête · aucun skill ne calcule une cohorte LTV, un payback ou un CAC depuis un scan. Câblage · le prix et la forme d'offre entrent en **observé** (`snapshot-brand` Step 2 + offres) · l'économie réelle (CAC, LTV, marge brute, payback, repeat/rétention) se pose en **inconnu typé** via `pending-validations.md`, levier `connect-source` sur le commerce + l'analytique puis `analyze-perf` une fois la data branchée, plus une **capture opérateur directe pour la marge brute** (elle décide du break-even ROAS). Surfacé au close de phase 9, jamais inventé en cours de route.

**Axe funnel complet (axe 2)** · partie visible (PDP, landing, offre, réassurance, preuve sociale exposée ou son absence vérifiée) en **observé** via `snapshot-brand` · partie non observable (checkout, abandon par étape, flows email, cadence de rétention, LTV réelle) en **inconnu typé**, levier `connect-source` sur le commerce + l'email. Pas-encore-outillé honnête · aucun skill n'audite aujourd'hui un funnel CRO de bout en bout ni les flows de rétention · nommer l'écart, le poser comme capacité à brancher, ne pas le maquiller. Une friction repérée à l'œil (preuve sociale absente, réassurance faible au checkout visible) entre comme **hypothèse à confiance graduée**, pas comme diagnostic mesuré.

**Lecture au close (Step 9 · application directe d'open-map-reasoning).** La section Observé/Déduit/Inconnu/Leviers du close lit la carte sur les **cinq axes**, pas sur le seul axe créa · les axes outillés rendus en Observé/Déduit, les axes non branchés (économie, funnel, média sans compte) en **Inconnu** avec leur levier pré-amorcé en **Leviers** (brancher le commerce · brancher l'analytique · connecter le compte publicitaire · capture marge brute), tous **déjà écrits dans `pending-validations.md`** au moment où ils ont surgi (HR-ONB-2), jamais inventés en fin de course. La phrase-mécanisme de clôture transforme la liste d'inconnues en lecture économique précisément parce que les cinq axes sont rendus · l'économie unitaire et le funnel posés en inconnu avec levier sont souvent le vrai goulot.

**Offre de connexion des outils au close (v1.10.0).** Les leviers des axes éco, funnel et média sont tous le même geste concret · brancher un outil. Le close ne se contente donc pas de nommer ces inconnus · il **demande explicitement à l'opérateur s'il veut connecter ses outils**, en une proposition groupée et en langage opérateur, posée comme affordance (pas comme la question macro unique du Close ouvert · elle s'ajoute aux Leviers, elle ne la remplace pas). La proposition couvre trois familles · (a) **commerce / CMS** (Shopify, le back-office boutique · ouvre l'économie réelle et le bas du funnel · levier `connect-source`), (b) **plateformes paid** (Meta, Google · ouvre la structure de compte, le budget, le ROAS réel · levier `connect-source` / `import-meta-results` / `audit-meta-account`), (c) **autres outils de contexte et de productivité** (analytique, email/CRM, Notion et assimilés · ouvre la rétention, les flows, la mémoire de travail externe · levier `connect-source` pour les sources data, `connect-mcp-server` pour les outils MCP). Formulation type, zéro jargon · *"Une partie de ta carte reste dans le noir parce qu'elle ne se lit pas sur le site · ton économie réelle, ta rétention, tes perfs paid. Si tu veux, je peux brancher tes outils pour l'éclairer · ta boutique, tes comptes pub, ton analytique ou ton email. Tu veux qu'on en connecte un maintenant, ou je garde ça en réserve ?"*. Refus ou report → chaque connexion non faite reste une poche `pending-validations.md` avec son levier, reprenable à tout moment · jamais re-demandée de façon insistante, jamais imposée à la porte d'entrée. Cette offre est l'incarnation concrète des Leviers du close · elle rend actionnable, en un geste, ce que les axes 1/2/3 ont posé en inconnu typé.

### Règles dures (cinq axes · v1.10.0)

- **HR-AXIS-1 · Voix client ET marché.** Quand l'enrichissement Phase 4 tourne, `mine-vom` (4c) est offert au Gate Inter 2 et tourne par défaut en `fast_track`. Une Phase 4 qui ne mine que la voix client sans jamais offrir la voix marché viole la doctrine « voix client ET marché » · régression v1.4.0 corrigée.
- **HR-AXIS-2 · ROAS et économie jamais inférés du site.** Le CAC, le LTV, la marge, le payback, le ROAS réel ne sont JAMAIS produits depuis un scan de devanture · ils se posent en inconnu typé avec levier (`connect-source` + `analyze-perf`, capture opérateur pour la marge). Inférer un chiffre d'économie depuis le site = freestyle interdit.
- **HR-AXIS-3 · Inconnu typé avec levier, jamais trou muet.** Tout axe non couvert (économie, funnel, média sans compte) s'écrit dans `pending-validations.md` avec son levier pré-amorcé au moment où il surgit (cohérent HR-ONB-2), et le close l'agrège · il ne le crée pas en fin de course.
- **HR-AXIS-4 · Compétitif par voie publique même sans compte.** `watch-competitors` (Meta Ads Library publique) tourne indépendamment de tout accès au compte de l'opérateur · l'absence de compte branché ne justifie jamais de sauter le compétitif paid.
- **HR-AXIS-5 · Close sur cinq axes.** Le close Step 9 lit la carte du connu/inconnu sur les cinq axes, pas sur le seul axe créa · un close qui ne rend que la créa est un close à carte fermée (anti-pattern `open-map-reasoning.md`).
- **HR-AXIS-6 · Offre de connexion des outils au close.** Le close demande explicitement à l'opérateur s'il veut connecter ses outils (commerce/CMS, plateformes paid, analytique/email/productivité), en proposition groupée et en langage opérateur, comme affordance qui s'ajoute aux Leviers. Chaque connexion non faite reste une poche `pending-validations.md` reprenable. L'offre se présente une fois, sans insistance · jamais imposée à la porte d'entrée.
- **AP-AXIS-1 · Atlas créa-only sans offre marché/compétitif.** NEVER livrer un atlas où la voix marché et le compétitif n'ont même pas été offerts · ils sont câblés (4c/4d), offerts au Gate Inter 2, reportables, jamais omis en silence.
- **AP-AXIS-2 · Chiffre d'économie inventé depuis le scan.** NEVER produire un CAC/LTV/marge/ROAS comme s'il était observé alors qu'il n'est pas branché · inconnu typé avec levier obligatoire.
- **AP-AXIS-3 · Skill média invoqué sans compte branché.** NEVER lancer `audit-meta-account` / `audit-google-pmax` / `analyze-perf` sur un compte non connecté · poser l'inconnu avec levier `connect-source`, ne pas simuler une lecture de performance.
- **AP-AXIS-4 · Friction funnel présentée comme diagnostic mesuré.** NEVER présenter une friction CRO repérée à l'œil (réassurance faible, preuve sociale absente) comme un diagnostic de funnel mesuré · hypothèse à confiance graduée, le bas du funnel reste inconnu typé tant que le commerce + l'email ne sont pas branchés.
- **AP-AXIS-5 · Inconnu data posé sans offrir le branchement.** NEVER poser l'économie, la rétention ou les perfs paid en inconnu sans, au close, proposer concrètement de connecter l'outil qui les éclaire (commerce/CMS, paid, analytique/email/productivité) · le levier doit devenir une offre actionnable, pas rester un mot. À l'inverse, NEVER harceler · une offre au close, report propre vers `pending-validations.md`, jamais une relance imposée.

Cross-ref · `docs/system/onboarding-setup-flow.md` (« Les cinq axes de la récolte » + « Câblage des cinq axes ») · `docs/system/open-map-reasoning.md` (raisonnement à carte ouverte · figure et fond, inconnu typé avec levier, l'inconnu génère) · `docs/system/investigation-posture.md` (close 5 sections · lecture des cinq axes) · `.skills/skills/mine-vom/SKILL.md` · `.skills/skills/watch-competitors/SKILL.md` · `.skills/skills/trendtrack-enrich-brand/SKILL.md` · `.skills/skills/audit-meta-account/SKILL.md` · `.skills/skills/analyze-perf/SKILL.md` · `.skills/skills/connect-source/SKILL.md`.

---

## Cross-references

- `.skills/skills/onboard-brand/SKILL.md` · orchestrator pattern reference (purity rule, gate canon)
- `.skills/skills/setup-brand/SKILL.md` · Palier Phase 1 (Step 1)
- `.skills/skills/snapshot-brand/SKILL.md` · Palier Phase 1+2 (Step 2 · includes its own Phase 1 macro + Phase 2 drilling gate v1.4.0)
- `.skills/skills/map-audiences/SKILL.md` · Palier Phase 3 hiérarchique parent/enfants 3 niveaux mère + sous-poches (Step 3 v1.4.0 · 4 questions framework canon)
- `.skills/skills/mine-voc/SKILL.md` · Palier Phase 4 enrichissement per audience (Step 4a v1.4.0 · pain_points + objections sub-audience)
- `.skills/skills/profile-audience/SKILL.md` · Palier Phase 4 enrichissement per audience (Step 4b v1.4.0 · JTBD canon V3 8 dimensions)
- `.skills/skills/deepen-brand-context/SKILL.md` · legacy orchestrator (v1.3.0 Step 3 deepen chain · remplacé par map-audiences Step 3 + mine-voc/profile-audience Phase 4 v1.4.0)
- `.skills/skills/weight-dimensions/SKILL.md` · Phase 5
- `.skills/skills/produce-paid-angles/SKILL.md` · Phase 6
- `.skills/skills/score-matrix/SKILL.md` · Phase 7
- `.skills/skills/produce-strategy/SKILL.md` · invokable en post-Phase 9 close si l'opérateur veut cadrer le focus Q{n} sur la brand atlas-complete (strategy.schema v1.0 canon shipped v2.58)
- `.skills/skills/creative-brief-composer/SKILL.md` · downstream production briefs+créas post-atlas (separate invocation, operator chooses axe créatif)
- `docs/system/onboarding-setup-flow.md` · **doctrine onboarding canon** · 8 principes non négociables + enchaînement 10 phases + câblage enrich-pas-create sur cet orchestrateur + fixes runtime audit · source des 4 principes instrumentés section Doctrine onboarding v1.9.0 (porte amont · deux gestes par pièce · inconnus in situ avec levier · exhaustivité offerte + reportable)
- `docs/system/progressive-cartography-doctrine.md` · **NEW v2.68** · progressive cartography canon (Sections 3-7 phasing · Section 8 Pattern gates light) · doctrine source v1.4.0 refactor
- `docs/system/decomposition-visibility-doctrine.md` · **NEW v2.78.2 + v2.81.1+ NIVEAU LIVE** · doctrine canon racine 3 phases temporelles · AVANT exec NIVEAU 0 paramètres décomposés (v2.79.5) · PENDANT exec NIVEAU LIVE thinking aloud expert action LOURDE orchestrateur 2 niveaux abstraction macro + micro chaînes phrasé (v2.81.1+) · APRÈS exec NIVEAUX 1-4 matrices Atlas Visibility post-Step 8 (Décomposition produit cross-products · Many-to-many pain × audience cross-atlas · Stage business filter · Méthode pédagogique verbale · audience produit-fit vs ciblage créa distinction) · HR-DVD-11 + AP-DVD-11 enforcement
- `docs/system/pain-benefit-chain.md` · canon 3 couches bénéfices (functional · emotional · identity) · consume NIVEAU 1 Décomposition produit
- `.skills/skills/snapshot-brand/SKILL.md` v2.78.2 cohérent · sister skill encoding products + offers + brand identity (Phase 1+2 chain)
- `.skills/skills/profile-audience/SKILL.md` v2.78.2 cohérent · sister skill encoding audiences enrichies JTBD canon V3 8 dimensions (Phase 4b chain)
- `.skills/skills/define-specs/SKILL.md` v2.78.2 cohérent · sister skill décomposition produit specs/mécanismes/bénéfices (consume NIVEAU 1)
- `.skills/skills/produce-positioning-canvas/SKILL.md` (forward-compat v2.80 si shipped) · Moore positioning format pour NIVEAU 3 Positioning Statement
- `.skills/skills/define-brand-voice/SKILL.md` (forward-compat v2.80 si shipped) · 4D brand voice cohérence NIVEAU 3 positionnement
- `docs/system/territory-doctrine.md` · v2.67 · layer territoire scope canon (build-atlas-complete = substrat territoire only, productions briefs+créas downstream)
- `docs/system/investigation-posture.md` · 5-section close canon (Step 9 mandatory) · close ouvert Phase 4 vers production downstream via creative-brief-composer (out of scope build-atlas territoire-pure v1.3.0+)
- `docs/system/scope-extension-doctrine.md` · SED-X v2.65 · skill scope boundaries discipline
- `docs/system/canonical-matrix-reasoning.md` · CMR · production discipline (95% quality on intersectional outputs)
- `docs/system/compositional-cartography.md` · §7 anti-pattern (no raw numeric scoring to operator) · implémentation domaine créatif de CMR
- `docs/system/confidence-propagation.md` · confidence chain algebra
- `docs/system/brand-isolation-doctrine.md` · brand_only scope default
- `docs/system/skill-routing-doctrine.md` · v2.55 routing canon (orchestrator delegates, never freestyles strategic prose)
- `docs/system/delegation-pattern.md` · model routing + parallel caps
- `docs/system/contract-build.md` · Build mode rules + Orchestration gate
- `docs/system/voice.md` · operator-facing prose canon (3 movements, no bold-section anchors on synthesis paragraphs)
- `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW (extension_hooks + manifest registry scan canon)
- `scaffold-extension` v1.2.0+ Phase 9 register-and-flag (upstream registry NEW entities)

---

## Verdict v1.6.0

v1.6.0 ship orchestrator decomposition visibility refactor · NEW Phase Output Atlas Visibility Matriciel Multi-niveau insérée entre Step 8 stage territories et Step 9 Close Investigation Posture · 4 niveaux canon obligatoires (NIVEAU 1 Décomposition produit cross-products specs/mécanismes/bénéfices 3 couches functional/emotional/identity · NIVEAU 2 Many-to-many pain × audience matrix cross-atlas ASCII obligatoire avec espace blanc paid si signal · NIVEAU 3 Positionnement filtre par stage business early/growth/scale audience produit-fit vs ciblage créa distinction explicit · NIVEAU 4 Méthode pédagogique verbale). Doctrine racine `docs/system/decomposition-visibility-doctrine.md` NEW v2.78.2. Sister skills v2.78.2 cohérents (snapshot-brand · profile-audience · define-specs). Forward-compat sister skills v2.80 produce-positioning-canvas (Moore format NIVEAU 3) + define-brand-voice (4D). Backward compat strict additif · Phases 1-7 chain skills preserved · Step 8 stage preserved · Step 9 close preserved (Investigation Posture consomme synthèse matricielle Phase Atlas Visibility en amont · Observé section enrichie cross-niveaux).

## Verdict v1.4.0

v1.4.0 ship orchestrator progressive cartography refactor · chain skills avec gates light entre paliers progressive (Phase 1+2 snapshot-brand · gate intermédiaire 1 · Phase 3 map-audiences hiérarchique · gate intermédiaire 2 · Phase 4 mine-voc + profile-audience enrichissement per audience validée) · mode `--fast-track` opérateur expert bypass gates intermédiaires auto-validate (opt-in) · Gate A audiences + Gate B angles preserved structural · territoire substrat (specs + offers + profiles + pain_points + objections + angles + scoring + frictions + roadmap + strategy) end-to-end · productions briefs+créas via separate `creative-brief-composer` skill post-atlas downstream. Backward compat strict additif sur chain skills (Steps preserved · gates additifs light · fast-track flag opt-in default off).

## Verdict v1.3.0 (legacy)

v1.3.0 ship orchestrator territoire-pure · substrate atlas (specs + offers + profiles + angles + scoring + frictions + roadmap + strategy) end-to-end · productions briefs+créas via separate `creative-brief-composer` skill post-atlas downstream.
