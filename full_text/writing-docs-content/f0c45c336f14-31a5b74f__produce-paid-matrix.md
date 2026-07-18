---
name: produce-paid-matrix
type: orchestrator
version: "1.3.1"
recommended_model: sonnet
subagent_safe: false
operator_facing: true
isolation_scope: brand_only
layer: territoire
mode: proposed
reasoning_pattern: matrix-driven
extension_hooks:
  - audience_entity   # NEW audiences custom scaffolded
  - angle_entity      # NEW angle types
  - territory_entity  # NEW territory custom
description: >
  v1.3.0 (v2.75.0 NEW extension_hooks frontmatter declaration · permet manifest registry scan Step 0 DRGFP enrichi · NEW entities scaffolded via scaffold-extension v1.2.0+ avec consumable_by matching ce skill consommées automatiquement runtime. Backward compat strict additif · extension_hooks vide default · legacy v2.74.x comportement hard-coded canon entities preserved. Pattern canon doctrine extension-discovery-doctrine.md NEW v2.75.0.)
  v1.2.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · chain produce-paid-angles v1.10 + weight-dimensions + score-matrix · cohérence read `audiences/{audience_slug}/pain_points/*.json` + `audiences/{audience_slug}/objections/*.json` sub-audience canonical downstream sub-skills. Synthesis territoires top-3 peut référencer pain_points/objections canonical IDs (PNT-NN + OBJ-NN) sub-audience dans rationale Section 2 Déduit. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.1.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · chain produce-paid-angles v1.9 + weight-dimensions + score-matrix · cohérence read `pain_points/*.json` + `objections/*.json` collections top-level downstream sub-skills (au lieu de profile.json sub-fields legacy). Synthesis territoires top-3 peut désormais référencer pain_points/objections canonical IDs (PNT-NN + OBJ-NN) dans rationale Section 2 Déduit. Backward compat lecture profile.pain_points[] + profile.objections[] legacy preserved (pre-v2.63 brands, sub-skills route transparent).
  v1.0.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (territoires-prioritisation, audiences-cartography). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.0.0 (v2.56 ship · audit Phase 1 Scenario 1 gap résolu) · orchestrator chairman qui chain
  produce-paid-angles → weight-dimensions → score-matrix pour produire la matrice paid
  DTC complète d'une marque. Scope · pitch paid sur brand X (cas canon Scenario 1
  audit Phase 1). Pipeline · génère angles ranked par audience (produce-paid-angles
  parallèle top-3 audiences) → pré-compute pondérations dimensions audience × angle
  (weight-dimensions parallèle) → build matrice Sub-cluster × Source d'angle scorée
  Impact × 3 + Vitesse × 2 + Signal × 1 modulée brand (score-matrix brand-wide) →
  synthesis finale 5 sections investigation-posture. Output operator-facing · top-3
  territoires en stars qualitatives (★★★★☆) jamais chiffres bruts, drill-down macro
  ouvert sur UNE question. Scoring numérique reste interne dans audit trail
  matrix-{date}.json, anti-pattern BCG CMR §7 compositional-cartography respecté.
  FR · "matrice paid pour {brand}", "génère la matrice angles audiences", "score
  les territoires paid", "pitch paid DTC".
  EN · "produce paid matrix", "paid pitch matrix", "rank paid territories", "score
  angles by audience".
  FR: "matrice paid pour {brand}", "produit-paid-matrix", "pitch paid DTC", "génère la matrice angles audiences pour {brand}", "score les territoires paid".
  EN: "produce paid matrix", "paid pitch matrix", "rank paid territories", "score angles by audience".
permissions:
  reads: [brand, product, profile, learning, strategy, angles, dimension_weights]
  writes: [angles, dimension_weights, scoring, learning]
  emits_events: [coherence_check, matrix_scored, territories_prioritized]
consumes:
  - path: brands/{slug}/brand.json
    min_version: 1.0.0
  - path: brands/{slug}/audiences/*/profile.json
    min_version: 1.0.0
  - path: brands/{slug}/audiences/*/pain_points/*.json
    min_version: 1.0.0
    note: "v1.2.0 NEW v2.64 ontologie sémantique pure · pain_points canonical sub-audience (owned natif par parent path). Consumé downstream produce-paid-angles v1.10+. Backward compat fallback top-level v2.63 + profile sub-fields v1.7."
  - path: brands/{slug}/audiences/*/objections/*.json
    min_version: 1.0.0
    note: "v1.2.0 NEW v2.64 ontologie sémantique pure · objections canonical sub-audience (owned natif par parent path). Consumé downstream produce-paid-angles v1.10+. Backward compat fallback top-level v2.63 + profile sub-fields v1.7."
  - path: brands/{slug}/pain_points/*.json
    min_version: 1.0.0
    note: "Legacy v2.63 backward compat read fallback · top-level collection avec affected_audiences[]."
  - path: brands/{slug}/objections/*.json
    min_version: 1.0.0
    note: "Legacy v2.63 backward compat read fallback · top-level collection avec affected_audiences[]."
  - path: brands/{slug}/angles/*.json
    min_version: 1.0.0
  - path: brands/{slug}/products/*/spec.json
    min_version: 1.0.0
  - path: resources/canon/copy/*
    min_version: 1.0.0
  - path: resources/registries/creative-mechanics-registry.md
    min_version: 1.0.0
  - path: resources/frameworks/paid-angle-scoring.md
    min_version: 1.0.0
  - path: docs/doctrine/territoires-prioritisation-doctrine.md
  - path: docs/doctrine/audiences-cartography-doctrine.md
produces_proposals_for:
  - brands/{slug}/angles/*.json (via produce-paid-angles sub-skill)
  - brands/{slug}/audiences/*/dimension_weights.json (via weight-dimensions sub-skill)
  - brands/{slug}/scoring/matrix-{date}.json (via score-matrix sub-skill)
pipeline:
  preconditions: |
    - brand exists with snapshot complete (spec.json + offers.json + at least 2 profile.json)
    - audiences cartographiées (≥ 2 audiences encodées avec 8 dimensions canon V3 populated)
    - canon copy resources loaded (atlas refs accessibles via phantom-canon.py)
  postconditions: |
    - angles ranked par audience top-3 (produce-paid-angles tourné)
    - dimension_weights.json computed par audience traitée (weight-dimensions tourné)
    - matrix-{date}.json scorée Sub-cluster × Source d'angle (score-matrix tourné)
    - top-3 territoires identifiés + trous flaggés
    - synthesis 5 sections investigation-posture délivrée
    - finalize-mutation-batch event emitted, status.json updated
disambiguates_against:
  produce-paid-angles: "route directly to produce-paid-angles when operator wants ranked angles for ONE audience only (single-audience scope, ~15 min). produce-paid-matrix orchestrates the brand-wide matrice across all top audiences."
  score-matrix: "route directly to score-matrix when operator wants ONLY the scoring matrice and dimension_weights + angles already exist on brand (e.g. re-score after brand modulators changed). produce-paid-matrix runs the full upstream pipeline first."
  weight-dimensions: "route directly to weight-dimensions when operator wants ONLY pondérations dimensions for a specific audience × angle pair (debug or audit). Sub-skill of this orchestrator, never operator-facing alone."
  deepen-brand-context: "deepen-brand-context handles brand intelligence deepening (VoC + VoM). produce-paid-matrix consumes that intelligence to produce the paid pitch matrice. Different layers: deepen = encode, paid-matrix = produce."
  produce-copy-brief: "produce-copy-brief turns ONE chosen angle into a copywriter brief (downstream production). produce-paid-matrix is upstream prioritisation: which audience × source territories to invest first, before any copy brief."
  onboard-brand: "onboard-brand sets up the brand from scratch. produce-paid-matrix assumes setup complete and ≥ 2 audiences encodées."
---

# produce-paid-matrix

Chairman orchestrator. Chain les trois producers (produce-paid-angles → weight-dimensions → score-matrix) pour livrer la matrice paid DTC complète d'une brand, puis synthétise en 5 sections investigation-posture. Narrate les handoffs brièvement. Jamais expose Task tool internals à l'opérateur. Synthesis finale strictement doctrine investigation-posture v2.54.

## Engagement disclosure pré-runtime · canon v2.79.3

Avant de lancer la matrice paid, expose ce disclosure à l'opérateur (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.3) ·

```
Matrice paid DTC · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Pre-flight DRGFP (L1 strict + L2 voc density gate + L3 brand context)
  2. Angles ranked par audience top-3 parallèle (produce-paid-angles × 3)
  3. Pondérations dimensions audience × angle parallèle (weight-dimensions × 3)
  4. Scoring matrice brand-wide Sub-cluster × Source d'angle (score-matrix)
  5. Synthèse 5 sections Investigation Posture · top-3 territoires stars qualitatives
  6. Close drill-down macro · opérateur arbitre

  ETA           ~10-15 min (mode parallèle · cap top-3 audiences)
  Implication   tu choisis mode briefing (en cours · à la fin · skip scoring)
  Livrable      matrice paid scorée · top-3 territoires en stars · 5 sections + close ouvert

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite avant de lancer. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set ou si opérateur a flag `--no-disclosure` explicit. Sinon · disclosure obligatoire canon v2.79.3.

Cross-ref doctrine racine `docs/system/engagement-disclosure-doctrine.md` v2.79.3.

## Expert methodology

**Posture** · senior agency lead pilote un pitch paid sur un nouveau client DTC. Délègue trois producers spécialisés (angles par audience · pondérations dimensions · scoring matrice brand-wide), lit les outputs en cartographe, et synthétise les top-3 territoires en hypothèses opérables (jamais en faits affirmés). L'opérateur arbitre au macro où creuser ensuite.

**Framework** · chain séquentielle avec parallélisation interne. Step 1 = produce-paid-angles déployé en sous-agents parallèles sur top-3 audiences (limite cardinalité ≤ 5 par run, doctrine compositional-cartography). Step 2 = weight-dimensions déployé en sous-agents parallèles sur même top-3 audiences. Step 3 = score-matrix tourné brand-wide (consume outputs Steps 1-2). Step 4 = synthesis finale investigation-posture par l'orchestrator lui-même.

**Règle de pureté** · l'orchestrator ne ré-implémente jamais la logique des sub-skills. Délègue, écoute, synthétise. Per onboard-brand precedent.

**Anti-pattern BCG (CMR §7 + compositional-cartography)** · le scoring numérique brut (Impact 7, Vitesse 6, score_dynamique 44) reste interne dans `brands/{slug}/scoring/matrix-{date}.json` pour audit trail. **Jamais surfacé en chiffres bruts à l'opérateur.** Output structuré par stars qualitatives (★★★★☆) ou tier qualitatif (top tier · mid tier · low tier · trou détecté). Compositional output, jamais quantitative ranking sec.

---

## Step 0 · DRGFP Manifest Registry Scan (NEW v2.75.0)

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

## Step 0bis · Pre-flight (DRGFP gates)

Verify brand state silently · ne narre pas le scan.

```bash
cat brands/{slug}/status.json
ls brands/{slug}/audiences/
ls brands/{slug}/angles/ 2>/dev/null || echo "no angles yet"
cat brands/{slug}/spec.json | head -20
```

Gates · 

- **L1 strict** · spec.json non-vide · offers.json ≥ 1 offer · ≥ 2 `audiences/*/profile.json` populées (8 dimensions canon V3) · snapshot.md existe (snapshot-brand a tourné).
- **L2 gate** · si audiences cartographiées MAIS aucune avec mine-voc dense (`voice.key_expressions[]` < 5 sur toutes) → AskUserQuestion 3 options · (a) lancer la matrice sur audiences hypothèse `TRÈS faible` confidence (output transparent flagué pour test budget calibré) · (b) router vers mine-voc d'abord sur top-2 audiences (~25-40 min, on revient avec matrice ancrée verbatim) · (c) hybride · lancer matrice ET déclencher mine-voc en background sur audience principale.
- **L3 degraded** · si `brand.strategic_context` absent (modulateurs score-matrix) → fallback proxy `brand_equity_level`, confidence 0.6, flag `_gaps`.

**Si gate L1 échoue** → stop. Router opérateur vers `onboard-brand` (setup pas terminé) ou `setup-brand` + `mine-audience` (audiences manquantes). Ne lance pas la chaîne sur une brand demi-construite.

**Annonce le pipeline** ·

> *"OK, matrice paid complète sur {brand}. Je chain · angles ranked par audience top-3 (~15-20 min parallèle), pondérations dimensions par audience (~5 min parallèle), scoring matrice brand-wide (~10 min). Total ~30-40 min. Tu choisis comment je te briefe ?"*

AskUserQuestion 3 paths ·

- *"Briefe-moi en cours"* · mode interactif, chaque sub-skill remonte son output dès qu'il atterrit.
- *"Je reviens à la fin"* · mode silencieux, seul le synthesis final 5 sections est délivré.
- *"Lance seulement les angles top-3 audiences (skip scoring)"* · bypass orchestrator, hand-off direct à produce-paid-angles (pertinent si opérateur veut juste l'ideation angles sans la prio territoires).

Si opérateur pick option 3 → exit orchestrator, route vers produce-paid-angles sur top-3 audiences. L'orchestrator ne procède full chain qu'avec options 1 ou 2.

---

## Step 1 · Delegate produce-paid-angles (parallèle top-3 audiences)

Sélectionne **top-3 audiences** par signal density (verbatim_density desc, sinon completeness desc, sinon sample_size desc). Hard cap 3 audiences (cardinalité compositional-cartography ≤ 5, marge sécurité pour Step 2 + 3).

Spawn **3 sous-agents parallèles** via Task tool, un par audience cible. Chaque sous-agent invoque `produce-paid-angles` avec ·

- brand slug
- audience slug (résolu en pre-flight)
- run mode (interactif / silencieux per Step 0)
- pas de `--focus` par défaut (full ranked table 5 angles par audience)

Expected return par sous-agent ·

- Ranked table 5 angles avec confidence chain inheritée (audience + brand → claim_confidence agrégée per produce-paid-angles v1.6.0+)
- Layer A scoring trace dans `sources/produced-angles/{date}/scoring-trace.jsonl`
- Layer B artifact dans `produced/paid-angles/{date}-{audience-slug}.md`
- Persistance brand-side `angles/{ANG-N}.json` aligné schema v1.2+

Operator-facing line pendant le run ·

> *"Je dig les angles paid sur tes 3 audiences principales en parallèle · {audience-1}, {audience-2}, {audience-3}. ~15-20 min."*

Orchestrator stays available pendant le run, returns au natural break (toutes audiences atterrissent).

**Gate parallélisation** · cap depth 1, max 3 sub-agents simultanés (per delegation-pattern.md). Allocate disjoint scopes (1 audience par sub-agent, pas de race condition sur angle files).

---

## Step 2 · Delegate weight-dimensions (parallèle top-3 audiences)

Pour chaque audience traitée en Step 1, spawn sous-agent `weight-dimensions` (operator-facing: false, sub-skill machine-facing par défaut).

Inputs par sous-agent ·

- brand slug
- audience slug (même top-3 que Step 1)
- angles list (output Step 1 brand-side `angles/{ANG-N}.json`)

Expected return par sous-agent ·

- `audiences/{audience-slug}/dimension_weights.json` computed avec sum check 1.0 ±0.01
- 8 weights par angle compatible + dominant_top3
- Event `weights_computed` emitted

Operator-facing line ·

> *"Je calcule les pondérations dimensions audience × angle (silent, ~5 min)."*

**Gate cohérence** · si une audience sur trois a `profile.json#completeness < 0.7`, weight-dimensions L3 degraded → biais initiaux par origin_axis, confidence 0.5. Flag `_gaps` propagé downstream.

---

## Step 3 · Delegate score-matrix (brand-wide, séquentiel après Step 2)

Spawn **un seul** sous-agent `score-matrix` (brand-wide, opère sur tout l'output Steps 1-2 consolidé).

Inputs ·

- brand slug
- audiences traitées Steps 1-2 (top-3)
- `dimension_weights.json` computés Step 2
- `angles/*.json` brand-wide (incl. angles produits Step 1)
- `brand.json#strategic_context` (ou proxy `brand_equity_level` si absent)

Expected return ·

- `brands/{slug}/scoring/matrix-{YYYY-MM-DD}.json` matrice Sub-cluster × Source d'angle scorée
- Top-3 territoires identifiés (rank descendant)
- Trous détectés (cellules compatibles mais aucun angle activable)
- Output operator-facing ASCII via score-matrix HR7 (matrice compacte 🔥 top par ligne)

Operator-facing line ·

> *"Je build la matrice brand-wide · Sub-cluster × Source d'angle scorée Impact × 3 + Vitesse × 2 + Signal × 1, modulée brand. ~10 min."*

**Note** · score-matrix opère séquentiellement (pas parallélisable, raisonne brand-wide sur cardinalité full top-3 audiences × 5 sources d'angle = 15 cellules max, ≤ 25 cap canon).

---

## Step 4 · Synthesis finale (operator-facing, 5 sections investigation-posture MANDATORY)

L'orchestrator livre la synthèse finale en 5 sections explicites doctrine `docs/system/investigation-posture.md`. Pas concaténation des outputs sub-skills · synthèse cross-skill par l'orchestrator.

**Apply voice canon** · prose-first sur Déduit/Leviers/Close · listes / matrice qualitative sur Observé/Inconnu · aucune section bold-anchor théâtrale · aucune mention sub-skill names ni Task tool · aucun chiffre brut scoring · aucun em-dash. Si incertitude voice, relire `docs/system/voice.md` + snapshot-brand SKILL.md Step 7.

### Section 1 · Observé (faits sourcés)

Format · liste à puces. Chaque fait avec source.

```
Observé · pipeline matrice paid {brand} ({date}, ~{duration} min)

- Audiences cartographiées · {audience-1} ({verbatim_density} verbatims · validation {confidence}) · {audience-2} ({verbatim_density} verbatims · validation {confidence}) · {audience-3} ({verbatim_density} verbatims · validation {confidence})
- Angles produits · {N_audience-1} angles ranked top sur {audience-1} · {N_audience-2} sur {audience-2} · {N_audience-3} sur {audience-3}
- Pondérations computed · {N_combinaisons} combinaisons audience × angle pondérées sur 8 dimensions canon V3
- Matrice scorée · {N_cells} cellules Sub-cluster × Source d'angle · modulateurs brand appliqués · coefficient cumulé {coeff} ({stade_brand}, {moment_strategique}, {contexte_marche}, {etat_atlas})
- Trous détectés · {N_trous} cellules compatibles sans angle activable

Pas observé directement (ne pas affirmer) · performance terrain réelle CAC/ROAS, gross margin par audience, audience démographique réelle si verbatim_density thin, intent réel acheteur si pas de mine-voc dense
```

### Section 2 · Déduit (hypothèses avec confidence chain)

**Top-3 territoires** présentés en stars qualitatives, JAMAIS chiffres bruts. Chaque hypothèse → question opérateur, confidence chain explicite.

```
Déduit · top-3 territoires hypothèses (confidence chain inheritée)

★★★★☆ Territoire 1 · {sub_cluster} × {source_angle}
  Hypothèse · {1 phrase pourquoi ce territoire ranke top}
  Confidence chain · {forte | moyenne | faible | TRÈS faible} ({raison · ex "audience mine-voc dense + brand sourcing direct" ou "audience hypothèse intuition, anchor formula-derived"})
  Angles activables · {ANG-N1, ANG-N2}
  Question opérateur · {ce territoire mérite un brief copywriter direct, ou tu veux upgrade confidence audience d'abord ?}

★★★☆☆ Territoire 2 · {sub_cluster} × {source_angle}
  Hypothèse · ...
  Confidence chain · ...
  Angles activables · ...
  Question opérateur · ...

★★★☆☆ Territoire 3 · ...
```

**Hard rules Section 2** ·

- Stars qualitatives ★★★★★ / ★★★★☆ / ★★★☆☆ / ★★☆☆☆ / ★☆☆☆☆ ou tier qualitatif ("top tier", "mid tier", "low tier"). JAMAIS chiffres bruts scoring (anti-pattern BCG CMR §7).
- Confidence chain EXPLICITE par territoire (héritée des sub-skills, MIN audience × brand × anchor_type per `docs/system/confidence-propagation.md`).
- Hypothèse présentée comme question, pas comme fait affirmé.
- Si claim_confidence majoritaire `TRÈS faible` → flag explicit "à tester sur budget calibré, pas à scaler avant validation terrain".
- **v1.2.0 NEW v2.64 · canonical IDs PNT-NN + OBJ-NN sub-audience dans rationale** · si les angles ranked top sur le territoire référencent pain_points/objections canonical sub-audience (lineage.pain_ref + objection_ref populés produce-paid-angles v1.10+), le rationale peut citer inline les canonical IDs · *"audience source mine-voc dense (3 PNT-NN canon sub-audience · PNT-01 ras-le-bol régimes, PNT-03 miroir post-grossesse, PNT-07 ballonnement) · 2 angles ancrés sur OBJ-02 scepticisme cliniquement prouvé"*. Surface enrichit traçabilité opérateur drill-down. Backward compat (v2.63 + pre-v2.63 brands) · fallback canonical IDs depuis top-level v2.63 ou skip rationale text-only legacy.

### Section 3 · Inconnu (variables non observables)

Variables que la matrice ne peut PAS résoudre. Posée explicit pour ouvrir leviers.

```
Inconnu

- Gross margin réelle par audience (pas dans schema brand, capture opérateur nécessaire)
- CAC actuel par canal si compte Meta non audité (audit-meta-account permet)
- Audience démographique réelle (âge, geo, RFM) si mine-voc < 5 verbatims sur audience source
- Intent réel acheteur (DR pur vs Brand vs Hybrid) si pas de mine-voc + tests perf préalables
- Saisonnalité brand-spécifique si pas dans `brand.json#seasonality`
```

### Section 4 · Leviers (skills / actions / sources pour lever les inconnues)

Pas un menu plat · l'orchestrator recommande 2-3 leviers max, le plus load-bearing en premier.

```
Leviers actionnables

1. mine-voc deeper sur {audience-target} (~10-15 min) · upgrade verbatim_density {current} → 15+, confidence audience source `forte`, claim_confidence agrégée territoires top-2 et top-3 upgrade `TRÈS faible` → `moyenne` minimum.
2. audit-meta-account (si compte Meta accessible) · ground CAC réel par audience cible, valide volume estimé Impact axis de la matrice.
3. capture opérateur explicit · gross margin par audience, deadline lancement, budget test calibré par territoire. Permet ranking action vs ranking théorique.
```

### Section 5 · Close drill-down macro ouvert (UNE question)

Anti-pattern AP-5 BANNI · close affirmatif qui ferme la conversation. Toujours close ouvert drill-down macro avec UNE question opérateur arbitre.

```
On creuse audience {top-1 score} en premier (territoire le plus solide, confidence chain {forte | moyenne}) · ou on lance brief créa sur angle {top-2 quick-win} (territoire activable rapide même si confidence inférieure) · ou on remonte à mine-voc pour upgrade confidence sur audience {weakest-confidence} avant tout test paid ?
```

**Hard rules Section 5** ·

- UNE question macro, pas 4-5 options diluées.
- Trois choix réels avec rationale court par choix (1 ligne max).
- Pas de "Mon avis" mou. Si le LLM a une reco load-bearing, la pose au début de la question · *"Mon move premier · {choix 1}. Justification · {1 phrase}. Sinon · {choix 2 ou 3}."*
- Opérateur arbitre · l'orchestrator enchaîne le drill-down sur axe choisi (silencieusement vers produce-copy-brief / mine-voc / audit-meta-account selon choix).

---

## Step 5 · Finalize

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Si les sub-skills ont déjà finalize-mutation-batch individuellement (chacun emits son propre `coherence_check`), ce final pass valide l'emission orchestrator-level pour la chain comme whole.

Update `status.json` ·

- `last_paid_matrix_run` · timestamp
- `paid_matrix_run_id`, `angles_run_ids[]`, `weights_run_ids[]`, `matrix_run_id`
- snapshot rebuild triggered si `angles/*.json` ou `dimension_weights.json` mutations promues
- Trigger silent `python3 .skills/build-brand-snapshot.py {slug}` (digest stays fresh)

---

## Hard Rules

- **Never re-implement subskill logic.** Orchestrator delegates. Per onboard-brand + deepen-brand-context precedent · purity rule absolue.
- **Never expose Task tool mechanics.** Say *"Je dig les angles paid sur tes 3 audiences en parallèle"* not *"I spawned 3 Task subagents on produce-paid-angles"*.
- **Never expose raw scoring numbers.** Anti-pattern BCG CMR §7 + compositional-cartography invariant. Output operator-facing TOUJOURS en stars qualitatives ★★★★☆ ou tier qualitatif. Scoring numérique brut reste interne dans `matrix-{date}.json` (audit trail).
- **Always run score-matrix at end of chain.** La valeur de l'orchestrator est dans la matrice scorée brand-wide, pas dans la concaténation des angles par audience. Skip score-matrix = wrapper, pas orchestrator.
- **Confidence chain MANDATORY explicit dans Déduit.** Hérité des sub-skills (audience source × brand source × anchor type → MIN conservative per `docs/system/confidence-propagation.md`). Si claim_confidence majoritaire `TRÈS faible`, flag explicit dans Section 5 ("à tester sur budget calibré").
- **Cardinalité top-3 audiences max par run.** Cap canonique compositional-cartography. Si brand a 5+ audiences encodées, sélection par signal density (verbatim_density desc), surface batch propose les autres pour run suivant. Ne PAS scorer 4+ audiences silently.
- **Operator chooses brief mode at Step 0.** Never assume. AskUserQuestion 3 paths mandatory.
- **finalize-mutation-batch at end of full chain.** Même si sub-skills ont finalize individuellement.
- **One brand at a time.** Pas de parallel paid-matrix sur multiple brands · confuses Layer B mutation scoping et brand isolation discipline.
- **Snapshot must be complete.** Brand demi-construites routent vers onboard-brand / setup-brand, pas vers produce-paid-matrix.
- **Audiences ≥ 2 obligatoire.** Matrice nécessite ≥ 2 audiences encodées (sinon plus une matrice mais un single-audience analysis · route directly vers produce-paid-angles).
- **DTC-bounded in v1.** SaaS, B2B lead-gen, agency services portent différentes sources d'angle et modulateurs. v1 ship DTC-only. SaaS/B2B adaptation = v2 mode ou sibling skill, jamais default branch.
- **No orphan output mandatory.** Close drill-down macro Section 5 toujours présent. Pas de *"voilà la matrice, autre chose ?"*. Pas de hardcoded menu `(a)/(b)/(c)/(d) Other`. UNE question macro arbitre opérateur.
- **Backward compat strict additif.** Skill nouveau v2.56, n'override aucun existant. produce-paid-angles, weight-dimensions, score-matrix restent invocables directement (disambiguates_against documente quand).
- **No em-dash anywhere.** Ni dans synthesis, ni dans matrice, ni dans confidence chain prose. Substituer par `·`, virgule, parenthèses, deux-points. Voice canon non-négociable.

---

## --focus parameter (optional)

```
produce-paid-matrix {brand}                       # default full chain top-3 audiences
produce-paid-matrix {brand} --skip=scoring        # angles + weights only, no matrix (debug mode)
produce-paid-matrix {brand} --audiences=2         # cap top-2 audiences au lieu top-3 (quick mode)
produce-paid-matrix {brand} --fresh               # bypass cache, force re-run pipeline complet
```

Focus modifiers internes, jamais surfacés `--focus=` syntax à l'opérateur. Operator peut dire *"matrice paid sur {brand} mais cap à 2 audiences"* → agent map à `--audiences=2`.

---

## Example output operator-facing

Ce que l'opérateur voit après *"matrice paid pour stepprs"* (brand pilote canonique) ·

---

```
Observé · pipeline matrice paid stepprs (2026-05-12, 35 min)

- Audiences cartographiées · marathoniens-amateurs (28 verbatims · validation forte) · debutants-trail (12 verbatims · validation moyenne) · runners-confirmés-blessés (4 verbatims · validation TRÈS faible)
- Angles produits · 5 angles ranked sur marathoniens-amateurs · 4 angles sur debutants-trail · 3 angles sur runners-confirmés-blessés
- Pondérations computed · 12 combinaisons audience × angle pondérées sur 8 dimensions canon V3
- Matrice scorée · 15 cellules Sub-cluster × Source d'angle · modulateurs brand appliqués · coefficient cumulé 1.1 (early-growth, sustain, mature, partiel)
- Trous détectés · 4 cellules compatibles sans angle activable (signal pour produce-paid-angles vague 2)

Pas observé directement (ne pas affirmer) · CAC réel par audience (compte Meta non audité), gross margin par produit, intent acheteur DR vs Brand sur runners-confirmés-blessés (verbatim density TRÈS faible)
```

```
Déduit · top-3 territoires hypothèses

★★★★★ Territoire 1 · marathoniens-amateurs × audience-derived
  Hypothèse · le territoire le plus solide · audience source mine-voc dense, sub-cluster volume premier, 3 angles activables ancrés verbatim direct.
  Confidence chain · forte (audience validée terrain + brand sourcing direct site + anchors verbatim exact match).
  Angles activables · ANG-01 "Verdict balance après marathon", ANG-02 "Pieds détruits semaine après semaine", ANG-03 "Inconfort 21e km"
  Question · ce territoire mérite un brief copywriter direct sur ANG-01 (top score), ou tu veux pousser test 2-3 angles parallèle d'abord ?

★★★☆☆ Territoire 2 · debutants-trail × product-derived
  Hypothèse · territoire mid tier · mechanism brand load-bearing sur cette audience, mais verbatim_density moyenne. Brief activable mais à valider sur premiers tests.
  Confidence chain · moyenne (audience partial mining + brand sourcing direct + anchors mix verbatim/formula).
  Angles activables · ANG-04 "Premier trail sans douleur", ANG-05 "Découverte technique pied"
  Question · brief créa sur ANG-04 budget calibré (~80€ par angle, 7 jours data avant verdict), ou upgrade confidence audience d'abord (mine-voc deeper, ~10 min) ?

★★☆☆☆ Territoire 3 · runners-confirmés-blessés × category-derived
  Hypothèse · territoire emerging · sub-cluster identifié mais verbatim density TRÈS faible. Angles formula-derived majoritaires.
  Confidence chain · TRÈS faible (audience hypothèse intuition + brand sourcing direct + anchors formula-derived).
  Angles activables · ANG-06 "Alternative aux orthèses", ANG-07 "Retour course après blessure"
  Question · à tester budget calibré seul (~50€ par angle, 5 jours data), ou skip ce territoire vague 1 et lance mine-voc deeper avant ?
```

```
Inconnu

- Gross margin par produit (pas dans schema brand, capture opérateur nécessaire)
- CAC actuel par canal Meta + Google (compte non audité)
- Audience démographique réelle runners-confirmés-blessés (verbatim_density < 5 sur cette audience)
- Saisonnalité brand-spécifique (printemps marathon vs automne trail)
```

```
Leviers actionnables

1. mine-voc deeper sur runners-confirmés-blessés (~10 min) · upgrade verbatim_density 4 → 15+, confidence audience source `TRÈS faible` → `moyenne`, claim_confidence agrégée territoire 3 upgrade.
2. audit-meta-account si compte Meta accessible · ground CAC réel par audience, valide volume estimé Impact axis territoires 1 et 2.
3. capture opérateur explicit · gross margin par produit, deadline lancement, budget test calibré par territoire.
```

```
Mon move premier · brief créa direct sur territoire 1 (ANG-01 marathoniens-amateurs), confidence chain forte, justifie le ship sans plus de mining. Sinon · mine-voc deeper sur runners-confirmés-blessés en parallèle si tu veux scaler les 3 territoires plus tard. Tu choisis · brief copywriter ANG-01 direct, ou on lance mine-voc en parallèle d'abord ?
```

---

The matrice paid sur une fashion brand DTC (différent vertical) surface différents top territoires · `pain.trigger` thins, `audience.JTBD.social` becomes load-bearing, le top-1 sortirait probablement brand-derived plutôt qu'audience-derived. Output shape stays identical (5 sections investigation-posture, stars qualitatives, drill-down macro) mais aucun territoire ne se répète. La non-répétition est la preuve que l'orchestrator raisonne sur la brand et ne template pas.

---

## Cross-references

- `docs/system/investigation-posture.md` · doctrine canon v2.54+ · 5 sections obligatoires (Observé · Déduit · Inconnu · Leviers · Close ouvert) · confidence chain explicit · drill-down macro · opérateur arbitre.
- `docs/system/compositional-cartography.md` · §4 matrice Sub-cluster × Source d'angle · §7 anti-pattern BCG scoring brut · cardinalité cap ≤ 5 · 4 modulateurs brand.
- `docs/system/canonical-matrix-reasoning.md` · invariants compositionnels · modulator-vs-cell pattern · cardinalité cap.
- `docs/system/confidence-propagation.md` · algèbre cascade confidence cross-skill · MIN conservative audience × brand × anchor → claim_confidence agrégée.
- `docs/system/contextual-intelligence.md` · master doctrine · no orphan output rule · contextual reasoning · anti-patterns AP-5 close affirmatif banni.
- `docs/system/voice.md` · voice canon · register · banned phrases · no em-dash · prose-first.
- `docs/system/delegation-pattern.md` · sub-agent delegation · cap depth 1 · max 3 sub-agents parallèles · disjoint scopes.
- `docs/system/dependency-resolution-protocol.md` · DRGFP L1/L2/L3 gap-filling · Step 0 pre-flight gates canon.
- `docs/system/extension-discovery-doctrine.md` v2.75.0 NEW (extension_hooks + manifest registry scan canon)
- `scaffold-extension` v1.2.0+ Phase 9 register-and-flag (upstream registry NEW entities)
- `docs/system/brand-isolation-doctrine.md` · isolation_scope brand_only · pas de cross-brand sur paid-matrix.
- `.skills/skills/produce-paid-angles/SKILL.md` · sub-skill consumé Step 1 · angles ranked par audience.
- `.skills/skills/weight-dimensions/SKILL.md` · sub-skill consumé Step 2 · pondérations dimensions audience × angle.
- `.skills/skills/score-matrix/SKILL.md` · sub-skill consumé Step 3 · matrice Sub-cluster × Source d'angle scorée.
- `.skills/skills/deepen-brand-context/SKILL.md` · orchestrator pattern reference (chairman chain N specialists + synthesis finale).
- `.skills/skills/onboard-brand/SKILL.md` · orchestrator pattern reference (purity rule, never re-implement sub-skill logic).
- `.skills/skills/produce-copy-brief/SKILL.md` · downstream production skill · opérateur pick un angle d'un territoire top → brief copywriter complet.
- `.skills/skills/mine-voc/SKILL.md` · upstream upgrade levier · confidence chain audience source.
- `.skills/skills/audit-meta-account/SKILL.md` · levier ground CAC réel par audience cible.
- `.skills/finalize-mutation-batch.py` · primitive Step 5 finalize.
- `resources/frameworks/paid-angle-scoring.md` · analytical canon produce-paid-angles.
- `resources/templates/creative-formula.md` v3.1 · registry vivant sources d'angle canoniques colonnes matrice.
- `resources/registries/creative-mechanics-registry.md` · mécaniques persuasives canon.
