---
name: produce-copy-brief
type: producer
version: "1.8.0"
isolation_scope: brand_only
layer: production
recommended_model: sonnet
reasoning_pattern: matrix-driven
matrix_mode: generating
consumes:
  - path: resources/frameworks/voc-coding.md
    min_version: 1.0.0
  - path: resources/registries/angle-registry.md
    min_version: 1.0.0
  - path: resources/registries/proof-registry.md
    min_version: 1.0.0
  - path: resources/quality-specs/hook-quality-spec.md
    min_version: 1.0.0
  - path: resources/templates/hook-formulas.md
    min_version: 1.0.0
  - path: docs/doctrine/angle-anatomy-doctrine.md
  - path: docs/doctrine/hooks-method-doctrine.md
  - path: docs/doctrine/objections-mapping-doctrine.md
  - path: docs/doctrine/pain-benefit-chain-doctrine.md
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
description: >
  v1.8.0 (v2.90.0 distribution fork environnement-aware) · NEW sous-section "Distribution fork" dans Step 7 close · détection silencieuse de l'outil de centralisation de l'opérateur (cascade canon connected-sources → Ecosystem table → credentials keys → MCP vérifiés) puis proposition fondue dans le next-step (push vers l'outil DÉTECTÉ jamais présumé · question de centralisation posée UNE fois par marque puis mémorisée · fork Route A compose-creative vs Route B export humain/partenaire). Doctrine canon `docs/system/brief-distribution-doctrine.md` NEW v2.90.0. Jamais bloquant pour la livraison du brief. Backward compat strict additif.
  v1.7.0 (v2.79.5 engagement disclosure NIVEAU 0 paramètres décomposés) · Section pré-runtime ajoutée AVANT Step 0 · expose 6 paramètres décomposés au runtime (audience target · format brief · angle source · persuasion structure · proof points · hypothèses figées · biais à éviter) avec POURQUOI chacun + close binaire OK ou ajuste. Cross-ref doctrines `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ + `docs/system/engagement-disclosure-doctrine.md` v2.79.5+. Backward compat strict additif (Steps 0-8 runtime preserved · seul l'amont disclosure change).
  v1.6.0 (v2.64 ontologie sémantique pure · pain_points + objections sub-audience) · Step 1 read encoded data refactor · pain_points lus depuis `audiences/{audience-slug}/pain_points/*.json` (sub-audience NEW v2.64 · owned natif par parent path) · objections lues depuis `audiences/{audience-slug}/objections/*.json` (sub-audience NEW v2.64). Section "Objections to neutralize" du brief cite désormais OBJ-NN canonical IDs depuis sub-audience. Section "Pain to activate" cite PNT-NN canonical sub-audience. Backward compat strict additif · fallback top-level v2.63 + profile sub-fields v1.7 preserved.
  v1.5.0 (v2.63 ontologie pure · pain_points + objections collections top-level) · Step 1 read encoded data refactor · pain_points lus depuis `pain_points/*.json filtered by affected_audiences contains audience_slug` (collection top-level NEW v2.63) · objections lues depuis `objections/*.json filtered idem`. Section "Objections to neutralize" du brief cite désormais OBJ-NN canonical IDs + cross-ref objections collection. Section "Pain to activate" cite PNT-NN canonical + cross-ref pain_points collection. Backward compat lecture profile.pain_points[] + profile.objections[] legacy preserved (pre-v2.63 brands).
  v1.4.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (angle-anatomy, hooks-method, objections-mapping, pain-benefit-chain, breakthrough-advertising-5-stages). Skill peut désormais consume ces doctrines canon copywriting/strategy pour informer production sans dépendre schemas exacts.
  v1.4.0 (v2.56 brief.schema activation) : Step 6bis NEW · stage Layer C frontmatter conforme brief.schema v1.0 (BRF-NN id, angle_id ref, audience_slug, product_slug, creative_format enum, intent_mix object, overlay_density, brand_mark_present, validation_status, confidence_chain, status hypothesis, created date). Storage path migré vers `brands/{slug}/briefs/{BRF-NN}.md` (canon brief.schema). Old path `produced/copy-briefs/` deprecated mais lecture backward compat. Closes schema orphan v2.42 (brief.schema designed jamais activée runtime). Downstream skills (compose-creative, recompose-creative, audit-creative-output) consument désormais des briefs au frontmatter typé canonique.
  v1.2.0 (v2.32 alignment) : when a creative_id is passed in input, reads creative.intent_mix in priority over intent for tone calibration. Also reads overlay_density + brand_mark_present (fallback craft_mode) and accepts validation_status oneOf shape.
  Produces a copywriter brief for an audience × chosen angle × channel.
  Consumes encoded brand intelligence (verbatims, pains, objections,
  vernacular, voice) from mine-voc Layer B + optional chosen angle from
  produce-paid-angles. Verbatim-anchored throughout (no inventions).
  Operator-format-respected (operator's agency standard captured in
  profile.json or brand config). Per-channel adapted (Meta vs Email vs
  Landing vs TikTok script). Output: 800-1200 word structured brief
  copy-pasteable for copywriter delivery, plus reasoned next-step
  proposal per no-orphan-output doctrine.
  FR: "brief copywriter pour {audience} {brand}", "brief copy {brand}", "brief Meta pour {audience}", "génère un brief pour {audience} sur {angle}", "brief campagne {brand}".
  EN: "copywriter brief for {audience} {brand}", "copy brief {brand}", "brief Meta for {audience}", "generate brief for {audience} on {angle}".
permissions:
  reads: [brand, product, profile, learning, strategy]
  writes: [learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists with at least one audience profile.json containing pain_points, objections, voice.key_expressions. Ideally mine-voc has run on the audience. If chained from produce-paid-angles, an angle is pre-selected.
  postconditions: brief artifact in brands/{slug}/briefs/{BRF-NN}.md (frontmatter YAML conforme brief.schema v1.0 + body markdown libre), generation trace in sources/produced-briefs/{date}/, learnings appended if pattern detected, finalize-mutation-batch event emitted, recommended next-step persisted as an idempotent In Progress line in brands/{slug}/todos.md (canonical format, auto-ticked when the downstream skill runs), AND any upstream In Progress line naming this skill auto-ticked on artifact write. Legacy path produced/copy-briefs/{date}-{audience-slug}-{angle-slug}-{channel}.md deprecated v1.4.0 (lecture backward compat preserved).
disambiguates_against:
  produce-paid-angles: "route to produce-paid-angles when operator wants ANGLE IDEATION (matrice ranked) · produce-copy-brief is the downstream brief generation on a chosen angle"
  ingest-resource: "route to ingest-resource when operator drops a brief reference doc to digest · that's input ingestion, not output generation"
  mine-voc: "route to mine-voc when audience is thin (no verbatims encoded yet) · copy-brief needs verbatim density to anchor hooks credibly"
  weave-hooks: "weave-hooks produit le paquet structuré machine-lisible du batch (genome-package) · produce-copy-brief produit un brief humain narratif sur UN angle"
prerequisites:
  - field: angles/{angle_id}.json
    level: L1
    auto_pull: read_angle_target
    freshness_ttl_days: 30
  - field: audiences/{slug}/profile.json
    level: L1
    auto_pull: read_audience_profile
    freshness_ttl_days: 60
  - field: resources/canon/copy/hooks
    level: L1
    auto_pull: read_canon_directory
    freshness_ttl_days: 365
  - field: brand.voice
    level: L3
    fallback: proxy_brand_personality
    confidence_default: 0.6
---

# Skill: produce-copy-brief

Synthesizer, not fabricator. Reads the encoded brand substrate, picks the right angle if one was not handed in, and ships a copywriter brief that compresses fifteen years of agency briefing experience into a single document. The copywriter opens it, reads five minutes, starts writing. Every claim about the audience traces back to a real customer verbatim. Every objection has a proof matched to it. Every CTA matches the brand's tone register. The format the operator already uses on agency work is preserved when encoded · the agency standard is the agency value, the skill respects it.

## Tone

Two registers, do not confuse them.

The brief artifact itself is structured agency document. Named sections, technical OK, jargon OK because the reader is a copywriter who needs craft language. That is the deliverable file.

The agent's chat surrounding the brief delivery follows the snapshot-brand Step 7 voice canon strictly. Pure prose. No bold-section anchors. No enumeration of dimensions. No exposed JSON paths. Three implicit movements (what the brief carries → file pointer → reasoned next-step). Read snapshot-brand SKILL.md Step 7 if any uncertainty before writing the surrounding commentary.

Banned in agent commentary: form-fill recap of every section, bold anchors like `**Pain anchored**\n...\n\n**Hooks**\n...`, exposed jargon (`voice.key_expressions[].sample_size`), exposed scores, internal labels, hardcoded `(a)/(b)/(c)/(d) Other` close.

## Expert methodology

Persona: senior agency strategist who has briefed 200+ copywriters and knows that a brief that does not anchor on real customer language produces generic copy. Reads the audience the way a strategist reads a research deck · lands on what matters, drops what dilutes, names the pain that is load-bearing for this angle.

Frameworks consumed (read once at first invocation, then internalized):
- `resources/frameworks/voc-coding.md` · JTBD lens for the brief opening, pain category typology, theme classification.
- `resources/registries/angle-registry.md` · angle naming canon, hook-lever lookup.
- `resources/registries/proof-registry.md` · proof type matched to objection type.
- `resources/quality-specs/hook-quality-spec.md` · 5-criterion hook test, threshold ≥ 4/5.
- `resources/templates/hook-formulas.md` · fallback hook library when verbatim anchor is weak.

The skill consumes these verbatim. No improvisation on hook quality threshold, no improvisation on objection-proof mapping.

---

## Engagement disclosure pré-runtime · NIVEAU 0 paramètres décomposés (canon v2.79.5)

Avant Step 0 (Resolve audience, angle, channel), expose ce disclosure NIVEAU 0 à l'opérateur. Pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5. Le but · rendre les paramètres décomposés que ce skill va mobiliser visibles AVANT exécution, pour que l'opérateur s'engage en conscience et puisse ajuster un paramètre avant de brûler le runtime brief.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Audience target
     {audience_slug_résolu Step 0} · segment atlas brand sélectionné
     POURQUOI · {raison priority · ex "audience demandée explicite"
     OR "match unique tags + identity.label" OR "audience mère
     validée Gate A précédent"}

  2. Format brief
     {short copy / long copy / sales letter DR / VSL script /
     email sequence / landing block / ad copy Meta / autre}
     POURQUOI ce format · {ex "channel Meta default · stack signals"
     OR "operator explicit demand short copy ad" OR "configuration
     agency standard encoded operator/profile.json#preferences"}

  3. Angle source
     {ANG-NN existing atlas brand angles/ OR NEW angle non-encoded}
     POURQUOI cet angle · {ex "top-ranked produce-paid-angles run
     <24h" OR "operator chose Miroir post-grossesse" OR "highest
     verbatim density on this audience pocket"}

  4. Persuasion structure
     {Halbert / Sugarman / StoryBrand / AIDA / PAS / BAB / 4Ps / autre}
     POURQUOI ce framework · {ex "Sugarman slippery slide pour long
     copy DR-aggressive" OR "AIDA short copy Meta feed" OR
     "StoryBrand landing identity-anchor"}. Si lignage canon present
     dans angle.json, framework_canon_id prime · le brief respecte
     ce qui a déjà été choisi en amont.

  5. Proof points
     Inventoriés depuis atlas brand · testimonials · stats · awards ·
     authority endorsements · scientific
     POURQUOI ces preuves · {ex "objection price-skepticism →
     pair avec study clinique souche probiotique"
     OR "objection 'just marketing' → social Trustpilot + authority
     sage-femme"}. Mapping objection-proof per proof-registry canon.

  6. Hypothèses figées
     Stage conscience audience · {unaware → most-aware ·
     lu market_position.awareness_dominant}
     Canal · {landing / email / Meta / TikTok / SMS · default
     INFER depuis stack + brand focus}
     Pricing leverage · {urgency active / bundle / risk-reversal /
     scarcity · lu offers.json active offer matching channel}

  7. Biais à éviter
     · Features-listing (énumérer specs sans translation bénéfice)
     · Benefit flou (promesse vague non-actionnable)
     · Sur-promesses (claims interdits plateforme + trust contract)
     · Clichés DR (registre "secret million", "découverte choc",
       formulations qui flaggent ad review Meta)

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je lance ?
```

ATTENDS confirmation explicite avant de lancer Step 0. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set OR si l'opérateur a flag `--no-disclosure` explicit OR si N usages successifs >= seuil expert (`auto_skip_after_n_calls` true). Sinon · disclosure obligatoire canon v2.79.5.

Cross-ref doctrines racine `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5.

---

## Step 0 · Resolve audience, angle, channel

Three resolutions in one step. The operator should never have to name a slug or a path.

**Audience.** From operator natural-language reference, match against `brands/{slug}/audiences/*/profile.json` using `meta.tags`, `identity.label`, `identity.description`, `pain_points[].formulation` as match surfaces. One match → continue. Multiple matches → AskUserQuestion with the candidate audiences in plain language (*"On part sur la femme post-grossesse ou la femme 40+ pré-ménopause ?"*). Zero matches → audience does not exist yet, route to `mine-audience` first, do not invent.

**Angle.** Three resolution paths in priority order:
- Operator stated explicitly (*"brief sur l'angle miroir"*) → use it, resolve against `angle-registry.md` taxonomy or brand-specific naming.
- Pre-selected from a previous `produce-paid-angles` run within the last 24h on the same audience → use the top-ranked angle from that run, the orchestration layer carries the context.
- Operator silent → auto-select the highest-confidence angle from the encoded verbatims per the paid-angle-scoring lenses (top-1 cell), surface the choice in the opening sentence: *"Je pars sur l'angle miroir post-grossesse, c'est celui qui a la densité verbatim la plus forte sur cette poche. Si tu veux un autre, dis-moi avant que je rentre dans le brief."*

**Channel.** Default = INFER, never hardcode Meta. Read three signals:
- `operator/profile.json#context.stack[]` for active platforms.
- `brand.json#market.current_focus` for the strategic emphasis.
- `learnings.json` filtered to recent campaign patterns if any.

Heuristic: stack with Meta + brand recent focus = paid acquisition → default Meta. Stack heavy on email/Klaviyo + brand focus = retention → default Email. Brand has a landing under refit → default Landing. Stack with TikTok signal + brand market sophistication low → TikTok script. Tie or no signal → AskUserQuestion 3-4 channel options in plain language. Never hardcode Meta as factory default · that fails operators on retention work.

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant assemblage brief (Step 1), scanner prerequisites :

1. L1 silent · `angles/{angle_id}.json` (required) · `audiences/{slug}/profile.json` · `resources/canon/copy/hooks`
2. L3 degraded · si `brand.voice` absent → fallback `brand_personality` · confidence 0.6 · flag _gaps

Output state map + confidence_chain[] init.

---

## Step 0ter · Load canon copy + angle lineage (v2.29.0+)

> **Atlas refs** dans cette skill = atlas canon copy (sense 1, référentiel cross-brand doctrine copywriting). Brand-side enrichment via `validations[]` (sense 2 atlas vivant). Distinct de l'atlas brand (sense 4, cartographie holistique data brand) qui désigne la matière brand structurée navigable via `/phantom`. Pour la distinction lexicale complète : `lexicon.md § Atlas, 4 senses MECE`.

> v1.1.0 (S55 v2.29.0 alignment) : LIGNAGE block uses `lineage.awareness_stage` (renamed from `schwartz_conscience`), `origin_axis` at top-level (renamed from `source`). Drop fields migrated to `creative.schema.json` (`intent`, `mecanique`, `craft_mode`, `execution.*`, `seasonality_trigger`). Optional `creative_id` input for execution-side context.

**Avant Step 1**, charger l'atlas canon copy et lire le lignage canon de l'angle source si disponible.

Si l'angle vient de `produce-paid-angles` v2.29.0+, son fichier `brands/{slug}/angles/{angle_id}.json` (cf. `resources/schemas/angle.schema.json` v1.2 + `_shared/awareness-stage.json`) contient le bloc `lineage` aligné v2.29 :
```
{
  audience_slug,
  origin_axis,
  lineage: {
    awareness_stage,
    schwartz_sophistication,
    hook_canon_id,
    framework_canon_id,
    angle_canon_id,
    archetype_canon_id,
    pain_extract,
    proof_primary,
    cta
  }
}
```

Lire ce lignage pour cadrer le brief : le hook est déjà choisi, le framework est déjà choisi, le registre voix est déjà choisi. Le brief étoffe ce que l'angle a posé, pas le reformule.

**Note couches.** `intent`, `mecanique`, `craft_mode`, `execution.*`, `seasonality_trigger` ont migré vers `creative.schema.json` (couche execution, pas couche stratégique). L'angle pur suffit pour le brief. Si l'opérateur passe un `creative_id` en input (cas test/run d'un format précis), lire en plus `brands/{slug}/creatives/{creative_id}.json` pour récupérer `intent_mix` (priorité, fallback `intent` legacy si absent), `mecanique`, `cta`, `execution.overlay_density` + `execution.brand_mark_present` (fallback `craft_mode` si absent) et calibrer la section CTAs + Format constraints sur ce format spécifique. Sinon, brief opère sur angle pur.

**v2.32 alignment, tone calibration.** Step 0bis lit `creative.intent_mix.primary` (et `secondary` + `weights` si présents) au lieu de `creative.intent` pour calibrer le ton du brief : un mix `{primary: DR, secondary: [Brand], weights: {DR: 0.6, Brand: 0.4}}` pondère le registre entre direct response (urgency, scarcity, CTA hard) et brand-lift (story, identity, association). Si `intent_mix` absent, dériver depuis `intent` legacy (`Hybrid` → `{primary: DR, secondary: [Brand], weights: {DR: 0.5, Brand: 0.5}}`). `validation_status` accepté sous les deux shapes (string legacy ou object composite avec `confidence`) ; si confidence basse (< 0.4), surfacer en footnote brief (*"creative source en confiance faible, brief reste valable, re-validation recommandée"*).

**Couches canon consommées par ce skill** :
- `frameworks` (déjà choisi par l'angle, le brief le respecte section par section)
- `archetypes-voix` (registre maintenu sur tout le brief)
- `formules-titres` (4U, how-to, listicle, secret, commande, question · pour les hooks variants Step 4)
- `objections` (feel-felt-found, reframe-positif, pre-emption, comparaison-cout-inaction · pour la section objections)
- `leads` (offer-led, mechanism-led, story-led, problem-led, proof-led · pour orienter l'ouverture du brief)
- `formats-livrables` (UGC-ad, VSL, landing, email-sequence, ad-statique, advertorial · selon le channel)

**Lecture batch.** `python3 .skills/phantom-canon.py copy {layer}` retourne la liste d'une couche. Cache en mémoire.

Si l'angle n'a pas de lignage canon (angle pre-v2.26 ou produit hors skill), le brief assigne lui-même un hook/framework/archetype canon en se basant sur l'audience + le channel + le format livrable.

---

## Step 1 · Read encoded data (v1.6.0 ontologie sémantique pure)

Load the substrate silently. Never narrate the loading.

**Sub-audience v2.64 (NEW · ontologie sémantique pure)** ·

- `brands/{slug}/audiences/{audience-slug}/pain_points/*.json` · pain canon entity owned natif par parent path (PNT-NN id, formulation, chain functional→emotional→identity, emotion, trigger, awareness_stage, verbatim_quotes[], severity, lifecycle_stage, confidence_chain, derived_angle_refs[]). Source de vérité pour section "Pain to activate" du brief.
- `brands/{slug}/audiences/{audience-slug}/objections/*.json` · objection canon entity owned natif (OBJ-NN id, formulation, type, frequency, severity, lifecycle_stage, response_counter, derived_angle_refs[]). Source de vérité pour section "Objections to neutralize" du brief.

**Backward compat lecture (v2.63 brands)** · si `brands/{slug}/audiences/{audience-slug}/pain_points/` ET `audiences/{audience-slug}/objections/` n'existent pas, fallback top-level `brands/{slug}/pain_points/*.json` + `brands/{slug}/objections/*.json` filtered by `affected_audiences[]` contains `{audience-slug}`.

**Backward compat lecture (pre-v2.63 brands)** · si top-level v2.63 absent aussi, fallback `audiences/{audience-slug}/profile.json#pain_points[]` + `profile.json#objections[]` (legacy sub-fields v1.7). Skill ne refuse jamais sur ce point, route transparent.

**Audience profile (toujours lu)** ·

- `brands/{slug}/audiences/{audience-slug}/profile.json` · `voice.key_expressions[]` (text, frequency, sample_size, platform), `voice.vocabulary_to_avoid[]`, `voice.tone_register`, `psychology.jtbd.{primary, context, emotional_driver}`, `decision_process.trust_anchors[]`, `market_position.awareness_dominant` (RENAME C1 profile/2.3), demographics. **Note v2.64** · `pain_points[]` + `objections[]` sub-fields legacy preserved en lecture pour backward compat, mais sub-audience collections prennent priorité si présentes.
- `brands/{slug}/products/{hero}/spec.json` · `identity.{name, niche, positioning}`, `unique_mechanism`, `problems_solved[]` with `verbatim_quotes[]`, `benefits[].chain` (functional → emotional → identity), `proofs.{social, authority, performance, scientific}`, `compliance`, `market_context.{sophistication, demonstrability, trust_barrier}`.
- `brands/{slug}/products/{hero}/offers.json` · active offer matching the channel, or active offer general if not channel-specific. Pricing, urgency, bonus, duration tier.
- `brands/{slug}/brand.json` · `tone_of_voice.{style, register, banned_words, frequent_words}`, `positioning`, `market.*` if VoM has run (vernacular, white-spaces).
- `brands/{slug}/strategy.json#current_focus` · informs CTA tone calibration.
- `operator/profile.json#preferences.brief_format` · operator's preferred brief structure (decision #1).
- `brands/{slug}/config.json#brief_format` · brand-specific override if exists (white-label / multi-client agencies).

If the operator has no encoded brief format preference, default to the 6-section structure named in Step 3. Ask once at end of first brief delivery whether to lock the format as default, adjust, or stay flexible · persist via `write_to_context`.

---

## Step 2 · Verbatim density floor

Hard gate before composition. Count `voice.key_expressions[]` entries with `sample_size` populated AND total `verbatim_quotes[]` across `pain_points[]` and `problems_solved[]`.

If `voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5 → recommend `mine-voc` first. Do not produce a brief on inferred-only basis. Surface to the operator: *"La voix client est trop fine pour ancrer un brief proprement · j'ai 2 expressions captées sur cette poche, le brief sortirait générique. Le move qui paie c'est de runner mine-voc d'abord, ~20 min, et on revient avec un brief vraiment ancré."* Stop unless operator forces explicitly with awareness of the trade-off.

A brief without real customer language equals generic copy equals zero agency value. The floor is non-negotiable.

---

## Step 3 · Map brief sections per voc-coding lenses

Mandatory sections inside the brief artifact (NOT in the agent's chat). If operator format encoded, adapt section names and ordering to that format. Default 6-section structure when no preference encoded:

- **Header** · brand / audience / angle / channel / date / brief_id.
- **Target audience** · 1 paragraph prose (demographic + psychographic + pain anchor + awareness stage), customer voice not brand voice.
- **Le job (JTBD)** · primary JTBD in 1 sentence per `voc-coding.md` JTBD lens, customer voice. Context if it sharpens.
- **Pain to activate** · formulation in customer language + emotion + trigger + 2-3 verbatim quotes with `sample_size` context inline. **v1.5.0 NEW · cite PNT-NN canonical ID inline** (ex *"Pain principal · PNT-03 'Ras-le-bol des régimes'"*) + cross-ref `pain_points/{PNT-NN}.json` pour le copywriter qui peut drill l'entity canonique downstream. Si pre-v2.63 brand (legacy profile sub-field), skip canonical ID inline (pain text-only).
- **Language to reuse** · 5-10 expressions from `voice.key_expressions[]` ranked by `frequency / sample_size`, each on its own line, each tagged with platform and frequency context. The words to weave into copy.
- **Objections to neutralize** · top 3 by recurrence × severity, each paired with a proof type from `proof-registry.md` that the brand actually carries. Lifecycle stage flagged (awareness / consideration / decision). **v1.5.0 NEW · cite OBJ-NN canonical ID inline** (ex *"OBJ-02 'C'est juste du marketing'"*) + cross-ref `objections/{OBJ-NN}.json` pour le copywriter qui peut drill `response_counter` déjà cristallisé par produce-paid-angles + `derived_angle_refs[]` cross-section. Si pre-v2.63 brand (legacy profile sub-field), skip canonical ID inline (objection text-only).
- **Proofs available** · inventory by type (testimonials, scientific/clinical, authority, social), each entry sourced from `product.proofs[]`, ready to quote.
- **CTAs** · 3 variants tone-aligned per `brand.tone_of_voice` + active offer pricing/urgency/bonus inline (decision #5). One direct-benefit, one risk-reversal, one urgency-anchored if offer carries urgency.
- **Format constraints** · channel-specific: Meta primary text 125 char before "see more" / Email subject 50 char / Landing block structure / TikTok script 60s pacing. Banned claim language per platform policy.
- **Hook examples** · 3 hook variants verbatim-anchored per Step 4 (hook-only, no body opening).
- **Avoid** · `banned_words` from brand tone, banned angles given audience awareness stage, recent objections that backfired in past creative (sourced from `learnings.json` if encoded).

Pain to activate ranks one pain only · the dominant one per `_source_meta.sample_size` AND relevance to the chosen angle. Efficiency angles pair with functional pain. Emotional-identity angles pair with emotional pain. Don't enumerate all pains, the brief activates one.

---

## Step 4 · Hook variants generation

Three hooks, hook-only (decision #3). Body opening is the copywriter's job · the brief calibrates angle and verbatim anchor, the copywriter writes the body.

Per `hook-quality-spec.md` 5-criterion test (Pattern Interrupt, Identification, Open Loop, Spécificité, Awareness Match) at threshold ≥ 4/5:

1. **Exact verbatim** from `voice.key_expressions[]` with `sample_size ≥ 5` → highest priority. The hook IS the verbatim or a 2-4 word adaptation of it.
2. **Semantic verbatim** from `verbatim_quotes[]` with high emotional weight → secondary. The hook adapts the verbatim while preserving the customer voice signature.
3. **Hook formula** from `hook-formulas.md` matched to the angle's hook-lever, when verbatim anchors are exhausted. The brief flags this hook with `(formula)` inline so the copywriter knows it is a starting point not a customer quote.
4. **Never invent a customer quote.** Never paraphrase a verbatim and present it as if it were a real customer quote. The trust contract is non-negotiable.

Hook below 4/5 on the quality spec → retry once with a different anchor or drop. The skill does not negotiate on hook quality.

Each shipped hook tagged in the brief with category (confession / callout / counter-intuitive / question / before-after) and lever (fear / desire / rational). Marked clearly: *"starting point · validate via hook-quality-spec before shipping."*

---

## Step 5 · Brief composition

Compose markdown brief, 800-1200 word target, 1500 hard ceiling (decision #4). Past 1500 → propose splitting into per-channel briefs rather than shipping a mega-brief · past 1500 the copywriter skims and misses load-bearing constraints.

Tone of the brief itself: agency-internal register. Technical OK. Jargon OK because the copywriter is the reader, not the operator's client. NOT operator-facing prose canon · the brief is craft document.

Each verbatim quoted with its `sample_size` context inline (*"redoutait le moment de s'habiller (8 mentions Trustpilot)"*). Gives the copywriter signal of how dense the verbatim is · high frequency = safe to lead with, low frequency = use as supporting beat.

Reads like an agency document. No bullet enumeration of every audience field. No `Field: content. Field: content.` form-fill openers. The brief is prose-first inside each section, with named sections as the structure scaffold.

**Canon lineage block (v2.29.0+).** En tête du brief, sous le header, un bloc explicite qui pose le lignage doctrinal du brief (agency-internal, fields lus depuis `angle.json` v1.2) :

```
Lignage
  audience       {audience_slug}
  awareness      {lineage.awareness_stage} × sophistication {lineage.schwartz_sophistication}
  origin axis    {origin_axis}
  framework      {lineage.framework_canon_id}
  hook           {lineage.hook_canon_id}
  angle narratif {lineage.angle_canon_id}
  archetype voix {lineage.archetype_canon_id}
  pain cible     {lineage.pain_extract}
  proof          {lineage.proof_primary}
  CTA            {lineage.cta}
```

Le copywriter lit le lignage avant le brief. Il sait quel framework respecter, quel registre voix tenir, quel hook ouvrir, quel pain ancrer, quel proof citer, quel CTA fermer. Si le brief diverge du lignage en cours d'écriture, c'est un signal de friction (à flag dans la section *Notes*).

**Pas de `mecanique` ni `intent` dans le bloc Lignage du brief.** Ces dimensions vivent côté `creative.schema.json` (couche execution), pas angle. Si un `creative_id` a été passé en input (cf. Step 0bis), le brief peut surfacer `mecanique` + `intent` du creative dans la section *Format constraints*, mais jamais dans le bloc Lignage qui reste strictement angle-level.

**Section Objections du brief.** Référence un ou plusieurs `canon copy objections` à utiliser (feel-felt-found, reframe-positif, pre-emption, comparaison-cout-inaction). Ne pas inventer de pattern de gestion : piocher dans canon, citer la fiche.

**Section Hook variants (Step 4).** Les variants utilisent `canon copy formules-titres` (4U, how-to, listicle, secret, commande, question) comme grille de génération. Chaque variant déclare implicitement quelle formule il suit.

---

## Step 6 · Layer A trace + Layer B artifact

**Layer A · generation trace** at `brands/{slug}/sources/produced-briefs/{date}/trace.jsonl`:

```json
{
  "id": "BRF-001",
  "produced_at": "2026-04-25T10:14:00Z",
  "audience_anchor": "femmes-30-55-minceur",
  "angle_anchor": "miroir-post-grossesse",
  "channel": "meta",
  "verbatim_anchors_count": 7,
  "verbatim_density_floor_passed": true,
  "operator_format_used": "default-6-section",
  "hook_variants_generated": 3,
  "hook_variants_rejected": 1,
  "rejection_reason": "awareness_mismatch"
}
```

Audit substrate. Operator never reads it. Downstream skills (`audit-creative-output`, `learn-from-session`) read it to detect patterns.

**Layer B · brief artifact** at `brands/{slug}/briefs/{BRF-NN}.md` (canon brief.schema v1.0 path, v1.4.0+). Markdown clean copy-pasteable into Notion / Slack / Doc / email for copywriter delivery. Legacy path `brands/{slug}/produced/copy-briefs/{YYYY-MM-DD}-{audience-slug}-{angle-slug}-{channel}.md` deprecated mais lecture backward compat preserved pour briefs pre-v1.4.0.

The next-step proposal lives in the conversational reply, NOT in the artifact file. The artifact is the pure deliverable. The agent commentary carries the reasoned next move.

---

## Step 6bis · Stage Layer C frontmatter brief.schema v1.0 (v1.4.0 NEW)

Avant write de l'artifact Step 6 Layer B, compose le frontmatter YAML conforme `resources/schemas/brief.schema.json` v1.0 et prepend-le au markdown du brief.

**Génération BRF-NN id.** Scan `brands/{slug}/briefs/*.md`, prendre next dans la séquence BRF-NN (BRF-01, BRF-02, ..., BRF-N+1). Stable, never reassigned.

**Composition frontmatter.** Fields canon brief.schema v1.0 ·

```yaml
---
brief_id: BRF-NN
angle_id: ANG-NN              # ref brands/{slug}/angles/{angle_id}.json
audience_slug: {slug}         # ref brands/{slug}/audiences/{slug}/profile.json
product_slug: {slug}          # ref brands/{slug}/products/{slug}/spec.json (null si brand-wide)
creative_format: meta_ad      # enum: image|carousel|story|reel|vsl|landing|email|sms|ad_copy|blog
intent_mix:                   # ref creative.schema.intent_mix shape
  primary: DR
  secondary: [Brand]
  weights: { DR: 0.6, Brand: 0.4 }
overlay_density: 0.5           # 0-1 si creative_id passé en input, sinon null
brand_mark_present: true       # bool si creative_id passé, sinon null
validation_status:             # ref _shared/validation-status
  state: hypothesis
  confidence: 0.7
confidence_chain:              # ref _shared/validation-state
  - source: audience_mine_voc
    confidence: forte
  - source: angle_canon_lineage
    confidence: forte
status: draft                  # required brief.schema v1.0
created: 2026-MM-DD            # required brief.schema v1.0
language: fr                   # operator preference
_field_types:
  brief_id: structured
  angle_id: structured
  audience_slug: structured
  intent_mix: derived
  validation_status: derived
  confidence_chain: derived
  status: stated
---

# Body markdown libre · section structure per Step 5
{body_markdown_per_step_5}
```

**Stage via stage-proposal.** Le brief markdown complet (frontmatter + body) est staged via :

```bash
python3 .skills/stage-proposal.py \
  --brand-slug {slug} \
  --field-path "briefs/{BRF-NN}" \
  --value-file /tmp/brief-{BRF-NN}.md \
  --source produce-copy-brief \
  --confidence 0.85 \
  --mode proposed
```

Opérateur valide via `pending-validations.md` workflow (accept/reject/correct) selon mutation gate canonical.

**Validation downstream.** `validate-resources` skill (haiku subagent) check frontmatter conforme brief.schema v1.0 post-write. Si invalid → blocking error surfacé via investigation-posture Inconnu section.

**Hard rule activation (v1.4.0).** Tout brief produit en v1.4.0+ DOIT porter frontmatter brief.schema v1.0. Briefs pre-v1.4.0 sans frontmatter restent valides en lecture (backward compat strict) mais flagués _legacy par audit-creative-output downstream pour migration optionnelle.

---

## Step 7 · Operator-facing chat

The agent message that surrounds the brief delivery. Apply snapshot-brand Step 7 voice canon STRICTLY · pure prose, three implicit movements, no bold anchors, no jargon leak.

Structure:

- **Intro 2-3 sentence prose:** what's in the brief, why these choices. Names the angle, the channel, the verbatim density signal, any inferred element flagged. Example: *"Brief sur l'angle miroir post-grossesse pour la femme minceur okr, channel Meta. J'ai ancré sur les trois verbatims les plus denses (le reflet, le ventre gonflé, le ras-le-bol des régimes) et les CTAs intègrent l'urgence du bundle 3 mois actif jusqu'au 15 mai."*
- **File pointer inline:** *"Brief complet dans `produced/copy-briefs/2026-04-25-femmes-30-55-minceur-miroir-meta.md` · 950 mots, prêt à transmettre."* The brief artifact is NEVER pasted twice in the chat · write to file, surface synthesis only (lesson v2.10.0 mini-friction observed live test).
- **Reasoned next-step proposal per no-orphan-output:** one strong recommendation grounded in operator goal × what was just produced × what is runnable. 1 alternative max if genuinely useful. Never a flat menu, never the same three proposals every time.

### Distribution fork (canon `docs/system/brief-distribution-doctrine.md` · v1.8.0)

Before composing the next-step line, resolve the operator's centralization tool silently · detection cascade canon: `operator/connected-sources.json` + `brands/{slug}/connected-sources.json` (type `crm`/`custom`, capability `write`) → brand `CLAUDE.md` Ecosystem table → `credentials.env` keys → session MCP actually verified, never assumed. Then fold distribution INTO the next-step proposal, 1 line, never a menu:

- **Tool detected and connected** → name it: *"J'envoie le brief dans ton ClickUp, liste Briefs créa ? Il reste dispo dans le workspace de toute façon."* Push only on explicit confirm. The workspace file stays the source of truth after push.
- **Tool declared but not wired** (Ecosystem table or env key without active connection) → propose the câblage, not the push: *"je peux me brancher à ton Notion et y pousser les prochains briefs, on le câble ?"* (routes to `connect-source`).
- **Nothing detected, question never asked for this brand** → ONE proactive line at the very end of the close: *"tu centralises tes briefs quelque part : Notion, ClickUp, autre ? je peux m'y brancher"*. Positive answer routes to `connect-source`; negative answer persists `brands/{slug}/config.json#preferences.brief_distribution: "workspace_only"`, never re-asked.
- **Route fork** · if the operator generates by AI → recommend chaining `compose-creative` on this brief (Route A, gated by `qc-creative` before spend). If a human or partner produces (video, UGC partner, copywriter) → recommend the export push + a short accompanying message ready to transmit (Route B). One defended reco based on format and context, alternative in 1 line.

Never block the brief delivery on any of this · the brief is delivered, pointed, consultable first. Push failure or silence = brief shipped anyway.

Examples of valid next-step formulations:

- *"Le move utile derrière, c'est de transmettre le brief à ton copywriter et de revenir dans 2-3 jours pour que je revoie les drafts qu'il sort. Sinon je peux directement sortir le brief Email parallel sur la même angle pour que le funnel reste cohésif."*
- *"Tu peux runner produce-paid-angles --focus=retargeting si tu veux préparer la séquence warm post-prospection avant que ce brief ne tourne."*
- *"L'angle est calibré, le copywriter peut partir tel quel. Je laisse poser, on revoit après les premiers tests Meta pour ajuster les hooks qui ne portent pas."*

Recommendation forte + 1 alternative max. Never *"voilà le brief, autre chose ?"* · that fails the doctrine.

---

## Step 8 · Finalize

Mandatory before shipping the operator-facing summary:

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mechanical Python primitive. Inspects every mutation written in this run (Layer A trace, Layer B artifact, optional learnings append), runs structural checks, emits a `coherence_check` event so `turn-end-audit` sees the loop closed.

Exit code 2 = blocking issue → revise before shipping. Exit code 0 with warnings = log them, ship. Non-negotiable, mechanical, not skippable.

---

## Step 8bis · Persist next-step + tick upstream (v1.8.1, additif strict)

Ce skill est aval de `produce-paid-angles` · son artifact ferme une boucle ouverte en amont, et il ouvre lui-même la boucle suivante. Deux gestes légers idempotents, aucun ne bloque la livraison du brief (Step 6 reste la sortie primaire).

Pattern déjà prouvé par `register-and-flag` Step 6 (write idempotent d'une ligne de tracking dans `brands/{slug}/todos.md`).

**Geste A · tick la ligne amont (fermeture de boucle).** Au finalize, scanner `brands/{slug}/todos.md → ## In Progress`. Si une ligne y désigne `produce-copy-brief` comme skill aval avec la même cible (même angle / même audience que ce run · ex `- [ ] produce-copy-brief sur l'angle #2 Ballonnement | P: 1 | E: low | T: 15 min`), basculer la case `[ ]` → `[x]` (puis archivage selon la doctrine todos racine). C'est l'auto-tick que `produce-paid-angles` Step 12ter attend de l'aval. Aucune ligne ne matche → ne rien faire, continuer (silencieux). Jamais de tick manuel · le downstream ferme la boucle de l'upstream.

**Geste B · persister son propre next-step.** Le close (Step 7) recommande un move (transmettre au copywriter et revoir les drafts · ou chaîner `compose-creative` · ou sortir le brief parallèle d'un autre channel). Cette reco vit dans le chat et meurt au prochain tour si rien ne la fixe. Lui donner une trace · une ligne dans `## In Progress` au **format de ligne canonique** ·

```
- [ ] {Name} | P: {0-3} | E: {low|med|high} | T: {durée}
```

- `Name` · le move A du close verbalisé court (ex `compose-creative sur le brief BRF-04`, `revoir les drafts copywriter dans 2-3 jours`, `produce-copy-brief Email sur la même angle`). Operator-language, nom de skill aval si applicable.
- `P` · priorité dérivée du contexte · brief prêt à produire en créa IA et stack le permet → `P: 1` · move de relecture différé → `P: 2`.
- `E` · effort du move aval (low pour un export, med pour compose-creative, high pour un funnel parallèle complet).
- `T` · ETA aligné `feedback_client_effort_scale` si client-facing (ex `quelques heures`, `2 à 3 jours`).

**Idempotence (dure, comme register-and-flag).** Avant d'écrire, scanner `## In Progress` · si une ligne porte déjà le même `Name`, ne pas dupliquer. Re-run du même brief = zéro nouvelle ligne. Les deux gestes passent par le mutation gate ·

```bash
python3 .skills/write-to-context.py --path "brands/{slug}/todos.md#in-progress" --value "- [ ] {Name} | P: {n} | E: {level} | T: {eta}" --source agent --mode direct --reason "Persist recommended next-step from produce-copy-brief close (idempotent)"
```

Si `write-to-context.py` ne route pas le markdown todos, fallback `register-and-flag` (sous-skill curator) · même réceptacle, même idempotence. Ne JAMAIS hand-editer le markdown hors gate.

**Léger, jamais bloquant.** Échec d'un write (gate refuse, fichier absent) → flag interne silencieux, ne casse pas le ship du brief. La trace todo est un bonus de persistance, pas une précondition de livraison.

**Doctrine.** Report des étapes différées et matérialisation des next-steps comme tâches reprenables avec leur levier · `docs/system/onboarding-setup-flow.md` (sections « Exhaustivité offerte, jamais forcée, reportable » et « La persistance est native »). Référencée ici, pas redupliquée.

---

## Cache strategy

24h TTL on the `(brand, audience, angle, channel)` tuple. Re-running the same brief query within 24h returns the cached output unless invalidated.

**Invalidation triggers (automatic):**
- Any mutation to `brands/{slug}/audiences/{audience-slug}/profile.json`.
- Any mutation to `brands/{slug}/products/{hero}/spec.json` for the hero product in scope.
- Any mutation to `brands/{slug}/brand.json#tone_of_voice` (banned words, register shift).

**Manual override:** `--fresh` flag bypasses cache.

Cache file location: `brands/{slug}/sources/produced-briefs/_cache/{audience-slug}-{angle-slug}-{channel}.json`. Cleared automatically on file watcher trigger (mutation event). Prevents LLM-variance noise on repeated identical queries.

---

## --focus parameter

The skill accepts a focus modifier for narrower runs. The operator says it in plain language (*"brief express juste les hooks pour la femme minceur okr"*) and the agent maps to the flag · never surfaced as `--focus=` syntax in the chat.

- **default** (no flag) · full brief 800-1200 words.
- **`--focus=hooks`** · only the 3 hook variants + verbatim anchors, skip the rest. ~200 words. Useful for quick test ideation.
- **`--focus=objections`** · brief emphasizes objection neutralization + proof matrix, lighter on language section. ~600 words.
- **`--focus=ctas`** · brief focuses on CTA variants for an offer test, skips audience/pain section. ~400 words.
- **`--fresh`** · bypasses cache, forces re-run with current encoded data.

---

## Hard Rules

- **Verbatim density floor mandatory.** `voice.key_expressions[]` < 5 OR cumulative `verbatim_quotes[]` < 5 → recommend `mine-voc`, refuse to produce. A brief without real customer language is generic copy is zero value.
- **Never invent customer quotes.** Never paraphrase a verbatim and present it as such. Either real (sourced from encoded `voice.key_expressions[]` or `verbatim_quotes[]`) or formula-flagged inline. The trust contract breaks irrecoverably on this rule.
- **Hook-only, 3 hooks max.** No body opening (decision #3 · copywriter owns the body, brief calibrates the angle).
- **Brief length 800-1200 target, 1500 hard ceiling.** Past 1500 → propose splitting per-channel rather than shipping a mega-brief.
- **Multi-offer brand = active offer inline in CTAs.** Never enumerate other offers (decision #5) · keeps the brief focused. Active offer's pricing + urgency + bonus woven into the 3 CTA variants.
- **Operator format respected when encoded.** Read `operator/profile.json#preferences.brief_format` + `brands/{slug}/config.json#brief_format` BEFORE defaulting to 6-section. The agency standard is the agency value.
- **Channel inferred or asked, never hardcoded Meta** (decision #2). Read stack + brand focus + recent activity. Tie or silent → AskUserQuestion.
- **Agent commentary follows snapshot Step 7 voice canon.** Pure prose 2-3 sentences + file pointer + reasoned next-step. The brief artifact has structured named sections · that's the deliverable, different register, do not confuse.
- **No-orphan-output mandatory.** Always close on a reasoned next-step proposal per doctrine v2.10.0. Never *"voilà le brief, autre chose ?"*. Never a hardcoded `(a)/(b)/(c)/(d)` menu.
- **Cache invalidation on entity mutation.** No stale results when fresh data lands.
- **Schema field semantics as analytical vocabulary, never JSON path mentions.** *"the words your customers actually use"* · yes. *"voice.key_expressions[].sample_size"* · banned in operator surface.
- **Banned jargon in operator-facing chat.** No `--focus=hooks --channel=meta`, no `verbatim_density_floor_passed`, no `_source_meta.sample_size`, no skill names mentioned in the synthesis.
- **Brief artifact never pasted twice.** Write to file, surface synthesis only in chat. Pasting the full brief in the conversational reply is the friction observed live in v2.10.0 · banned.
- **`finalize-mutation-batch` mandatory at end.** Step 8 runs the Python primitive before any operator-facing summary. Exit code 2 = revise before shipping.
- **Sample_size context preserved in brief.** *"redoutait le moment de s'habiller (8 mentions)"* gives the copywriter signal of how dense the verbatim is. Naked verbatims without frequency context lose signal · the copywriter cannot tell what to lead with.
- **Hook quality spec mandatory.** Every shipped hook passes the 5-criterion test at ≥ 4/5. Below threshold → retry once with a different anchor or drop. Non-negotiable.
- **Direct response only in v1.** Brand storytelling briefs, manifesto pieces, founder-narrative content live under a separate skill type. The agency standard encoded here is direct response: pain → solution → proof → CTA.
- **Brief frontmatter brief.schema v1.0 mandatory (v1.4.0+).** Step 6bis stage frontmatter YAML conforme brief.schema v1.0 (brief_id BRF-NN + angle_id + audience_slug + creative_format + intent_mix + validation_status + status + created required). Storage canonical path `brands/{slug}/briefs/{BRF-NN}.md`. Legacy path `produced/copy-briefs/` deprecated v1.4.0 mais lecture backward compat. Briefs sans frontmatter post-v1.4.0 = doctrine violation, refuse to ship.

---

## Cross-references

- `resources/schemas/brief.schema.json` v1.0 · canon schema frontmatter YAML briefs v1.4.0+. Required fields: brief_id (BRF-NN), status, created. Optional fields: angle_id, audience_slug, product_slug, creative_format, intent_mix, overlay_density, brand_mark_present, validation_status, confidence_chain. Storage `brands/{slug}/briefs/{BRF-NN}.md`. Activé Step 6bis v1.4.0.
- `resources/schemas/angle.schema.json` v1.2 · angle entity shape consumed by Step 0bis (`origin_axis`, `lineage.awareness_stage`, `lineage.*_canon_id`). v2.29.0 alignment, D#391.
- `resources/schemas/creative.schema.json` · execution-layer entity. Optional read in Step 0bis if `creative_id` is passed in input. Holds `intent`, `mecanique`, `craft_mode`, `execution.*`, `seasonality_trigger` (migrated from angle).
- `resources/schemas/_shared/awareness-stage.json` · shared `$ref` for `awareness_stage` enum (Schwartz conscience: unaware → most-aware), used by both angle and creative.
- `resources/frameworks/voc-coding.md` · JTBD + Schwartz + theme typology + pain category lens. Mandatory read at first invocation.
- `resources/registries/angle-registry.md` · angle naming canon, hook-lever lookup.
- `resources/registries/proof-registry.md` · proof type matched to objection type. Drives the objections section proof matrix.
- `resources/quality-specs/hook-quality-spec.md` · 5-criterion hook quality test, mandatory threshold ≥ 4/5.
- `resources/templates/hook-formulas.md` · fallback hook library when verbatim anchor weak.
- `.skills/skills/produce-paid-angles/SKILL.md` · sister upstream skill. Operator picks an angle from the ranked table → this skill turns it into a brief. Chained naturally.
- `.skills/skills/mine-voc/SKILL.md` · upstream Layer B source. Provides the verbatim density that this skill consumes. Prerequisite, not sibling.
- `.skills/skills/snapshot-brand/SKILL.md` · voice canon source for Step 7 agent chat. Read before writing the surrounding commentary if any uncertainty.
- `.skills/finalize-mutation-batch.py` · mandatory Step 8 primitive.
- `.skills/write-to-context.py` · canonical mutation channel for any append to `learnings.json` if a pattern is detected during the run.
- `docs/system/contextual-intelligence.md` · master doctrine. No orphan output rule, contextual reasoning, anti-patterns.
- `docs/system/voice.md` · voice canon, register, banned phrases.

---

## Example output · okr probiotique minceur, femme 30-55, angle Miroir post-grossesse, channel Meta

What the operator triggers: *"brief copywriter pour la femme minceur okr, angle miroir, Meta"*.

What the agent writes to the brief artifact at `brands/okr/produced/copy-briefs/2026-04-25-femmes-30-55-minceur-miroir-meta.md`:

---

```
# Brief · okr / Femme minceur 30-55 / Miroir post-grossesse / Meta
> 2026-04-25 · brief-okr-001

## Target audience

Femmes 30-55, mères, post-grossesse 6 mois à 5 ans, milieu urbain.
Awareness stage : problem-aware basculant solution-aware. Elles savent
qu'elles ont un problème · le ventre gonflé, le poids qui ne part pas,
la silhouette qui ne revient pas · mais n'ont pas encore une solution
catégorielle dont elles soient sûres. Elles ont essayé des régimes,
parfois Anaca3 ou des thés détox, et chaque échec a renforcé une
croyance limitante : "c'est foutu, c'est mon corps maintenant". Le
ressort dominant n'est pas l'esthétique pure, c'est la rupture
identitaire · elles ne se reconnaissent plus dans le miroir.

## Le job (JTBD)

Retrouver un corps qu'elles reconnaissent, sans avoir à se battre
contre lui chaque jour.

## Pain to activate

Pain primaire émotionnel-identitaire avec ancrage somatique quotidien
(ballonnement, ventre gonflé). Émotion : honte silencieuse, repli.
Trigger : moment du miroir le matin, moment d'habillage, photos de
famille où elles évitent l'objectif.

Verbatims à citer dans la créa :
- "Je ne pouvais plus voir mon reflet dans le miroir" (14 mentions Trustpilot)
- "Frustration, échec, culpabilité" (cluster récurrent post-grossesse)
- "Toujours ballonnée, le ventre lourd même à jeun" (9 mentions reviews)

## Language to reuse

Vocabulaire client à intégrer textuellement (priorité haute) :
- "ballonnée" · préféré à "ballonnement" (registre quotidien, pas médical)
- "ventre gonflé" · image visuelle, mieux que "rétention d'eau"
- "j'ai déjà tout essayé, rien ne marche pour moi" (11 mentions, signal d'épuisement)
- "mon reflet" / "le miroir" · ancrage identitaire, à protéger du langage marketing
- "frustration, échec, culpabilité" · la boucle émotionnelle nommée
- "le moment d'habillage" · trigger quotidien, peut ouvrir un hook scène

À éviter : "minceur" comme verbe ("mincir"), "kilos en trop", "corps de
rêve", "silhouette parfaite" · vocabulaire qui renvoie aux régimes
qu'elles associent déjà à l'échec.

## Objections to neutralize

1. **"C'est juste du marketing."** Lifecycle : awareness. Lever via
   proof scientifique attribué (étude clinique sur la souche probiotique,
   institut + n=). Pas via claim générique "cliniquement prouvé" · elles
   ont déjà été échaudées par ça.

2. **"C'est cher pour 1 à 3 kg de différence."** Lifecycle : consideration.
   Lever via reframe : ce n'est pas un produit minceur à l'unité, c'est
   un protocole pour réparer le microbiote post-grossesse. La perte de
   poids est le résultat, pas la promesse. Cost-calculator vs coach +
   régimes ratés sur 5 ans en backup.

3. **"Pourquoi ça plutôt qu'Anaca3, XLS Medical, Nutri&Co."** Lifecycle :
   decision. Lever via parasitic-positioning inversé · Anaca3 = thermogenèse
   (brûle), okr = microbiote (répare). Pas la même catégorie, donc pas la
   même issue. Cite la souche, cite la durée d'action (3 mois vs effet
   immédiat trompeur).

## Proofs available

- **Scientific** : étude clinique sur la souche probiotique [institut + n=]
- **Social** : avis Trustpilot et Judge.me filtrés post-grossesse (mentions
   accouchement, post-partum), ratings 4.6/5 sur 1200+ reviews
- **Authority** : si endorsement sage-femme ou nutritionniste spécialisée
   post-partum disponible, prioritaire en hiérarchie de proof
- **Performance** : avant/après sur la dimension "ventre gonflé" plutôt
   que sur le poids · alignement avec le pain primaire identitaire

## CTAs

1. Direct-benefit : "Retrouver mon reflet"
2. Risk-reversal : "Tester la cure 30 jours, remboursé si rien ne change"
3. Urgency (offre active 3 mois -20% jusqu'au 15 mai) : "Cure 3 mois -20%
   jusqu'au 15 mai"

## Format constraints (Meta)

- Primary text : 125 caractères avant le "voir plus", contenu essentiel
   dans cette portion
- Headline : 27 caractères max recommandé
- Description : 27 caractères
- Image : 1080x1080 ou 1080x1350 pour feed mobile
- Banni Meta policy : claims de perte de poids quantifiée ("perdez 5 kg"),
   avant/après corporels graphiques sans disclaimer, langage de body-shaming
- CTA boutons supportés : "En savoir plus", "Acheter", "S'inscrire"

## Hook examples (starting points · validate via hook-quality-spec)

Hook 1 · confession, fear→desire (verbatim exact, 14 mentions) :
"Il y a deux ans, je ne pouvais plus voir mon reflet dans le miroir."

Hook 2 · callout, fear (verbatim sémantique, 9 mentions) :
"Si tu es toujours ballonnée six mois après ton accouchement, écoute ça."

Hook 3 · counter-intuitive, rational→fear (formula) :
"Ce n'est pas la graisse. C'est ton microbiote intestinal."

## Avoid

- Banni vocabulaire : "mincir", "kilos", "silhouette parfaite", "corps
   de rêve", "régime miracle"
- Banni angles : urgency-only (l'audience est problem-aware, pas most-aware
   · l'urgence sans pédagogie = spam perçu)
- Backfired récemment (learnings.json) : claims "perte de poids garantie"
   rejetés par Meta ad review en mars, formulations esthétiques pures
   sous-performent vs identity-anchored
```

---

What the agent writes in the conversational reply (the chat surrounding the brief delivery, snapshot Step 7 canon applied):

---

Brief sur l'angle miroir post-grossesse pour la femme minceur okr, channel Meta. J'ai ancré sur les trois verbatims les plus denses (le reflet à 14 mentions, le ventre ballonné à 9, la boucle frustration-échec-culpabilité), et les CTAs intègrent l'urgence du bundle 3 mois actif jusqu'au 15 mai. Le hook 3 est une formule contre-intuitive sans verbatim direct, à valider en premier sur les tests parce que c'est lui qui ouvre le repositionnement microbiote vs thermogenèse.

Brief complet dans `produced/copy-briefs/2026-04-25-femmes-30-55-minceur-miroir-meta.md` · 980 mots, prêt à transmettre au copywriter.

Le move utile derrière, c'est de transmettre le brief tel quel et de revenir dans 2-3 jours pour qu'on revoie les drafts. Sinon je peux sortir le brief Email parallèle sur la même angle dans la foulée pour que ton copywriter ait le full funnel d'un coup et garde la cohésion de campagne.

---

The same skill on a skincare brand for women 28-42 with hyperpigmentation surfaces a different brief: pain to activate becomes the post-summer reveal moment, language section pulls *"j'ai la peau qui tire"* and *"taches qui s'installent"*, objections foreground actif scepticism over price, hook formulas shift toward revelation and statistic over confession. Output shape stays identical · same 11 sections, same verbatim-anchoring rule, same 800-1200 word envelope · but no section repeats from the okr brief verbatim. That non-repetition is the proof the skill reasons over the brand and does not template.

On a supplement brand outside the post-partum niche (men's performance, longevity), the awareness stage often shifts to solution-aware, the angle library shifts toward expertise and mechanism over identity, the proof hierarchy puts scientific first and social second instead of the reverse. The brief structure absorbs the shift without breaking · sections reorder when the operator's encoded format demands, the verbatim-anchoring rule stays absolute.
