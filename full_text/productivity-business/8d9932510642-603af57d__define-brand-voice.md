---
name: define-brand-voice
type: producer
version: "1.0.0"
recommended_model: sonnet
subagent_safe: true
operator_facing: true
isolation_scope: brand
layer: production
mode: interactive
reasoning_pattern: null
description: >
  v1.0.0 (v2.80 ship) · Produit brand voice chart canonique brand via méthodologie
  Nielsen Norman 4D (Funny↔Serious · Formal↔Casual · Respectful↔Irreverent ·
  Enthusiastic↔Matter-of-fact). Output · voice axes scores -5 à +5 par axe avec
  rationale · do/don't lexique 5-10 entries each sourcés audiences key_expressions
  + pain_metaphors + solution_metaphors · sample sentences per touchpoint
  (paid headline short-form · organic caption mid-form · CRM email subject +
  body · UI microcopy button + tooltip + error). Mute brand.json#/tone_of_voice
  (extend voice_axes + do_lexicon + dont_lexicon + sample_sentences_per_touchpoint)
  + crée brand_voice_chart.md brand-side standalone reference card. Step 0 bridge
  proactif canon v2.77 si territory incomplet (identity + audiences encoded minimum
  requis). Produce upstream consumer pour validate-brand-voice-consistency post-write.
  FR · "define brand voice", "tone of voice", "définit la voix brand", "voice chart",
      "ton de voix", "ancre le tone", "pose le tone of voice {brand}", "cadre la voix de {brand}".
  EN · "define brand voice", "tone of voice", "voice chart", "brand voice chart",
      "anchor brand voice", "set brand voice".
  FR: "define brand voice", "tone of voice", "définit la voix brand", "voice chart", "ton de voix", "ancre le tone", "pose le tone of voice {brand}", "cadre la voix de {brand}".
  EN: "define brand voice", "tone of voice", "voice chart", "brand voice chart", "anchor brand voice", "set brand voice", "define voice for {brand}".
permissions:
  reads:
    - brands/{slug}/brand.json
    - brands/{slug}/audiences/
    - brands/{slug}/products/
  writes:
    - brands/{slug}/brand.json
    - brands/{slug}/brand_voice_chart.md
  mode: interactive
  subagent_safe: true
  emits_events: [voice_chart_proposed, brand_voice_anchored]
consumes:
  - path: brands/{slug}/brand.json
    min_version: 2.0.0
  - path: brands/{slug}/audiences/*/profile.json
    min_version: 1.0.0
  - path: brands/{slug}/products/*/spec.json
    min_version: 1.0.0
  - path: docs/system/investigation-posture.md
  - path: docs/system/skill-routing-doctrine.md
  - path: docs/system/audience-cartography.md
  - path: docs/system/contextual-intelligence.md
  - path: resources/schemas/brand.schema.json
produces_proposals_for:
  - brands/{slug}/brand.json#/tone_of_voice
  - brands/{slug}/brand_voice_chart.md
extension_hooks:
  consumable_by: [brand_entity]
pipeline:
  preconditions: |
    - brand.json populated (identity.name + identity.brand_personality OR positioning.brand_promise present)
    - >= 1 audience profile.json with voice.key_expressions OR voice.pain_metaphors encoded
  postconditions: |
    - brand.json#/tone_of_voice extended via mutation gate (voice_axes + do_lexicon + dont_lexicon + sample_sentences_per_touchpoint)
    - brand_voice_chart.md created brand-side as standalone reference card
    - synthesis 5 sections investigation-posture délivrée
    - voice_chart_proposed event emitted
    - snapshot rebuilt
disambiguates_against:
  snapshot-brand: "snapshot-brand extracts tone_of_voice passively from site scrape (style + register + voice strings). define-brand-voice workshops the tone methodically via 4D Nielsen Norman axes + do/don't lexique + sample sentences per touchpoint. Invoke define-brand-voice AFTER snapshot-brand has anchored the brand passively, to upgrade the voice substrate from declarative strings to operational chart."
  produce-positioning-canvas: "produce-positioning-canvas anchors the positioning identity statement (category + differentiation + promise + market_position). define-brand-voice anchors the brand voice TONALITY cross-touchpoint (how the brand sounds). Sister skills · positioning answers WHAT the brand stands for, voice answers HOW the brand speaks. Both upstream of produce-paid-angles + produce-copy-brief."
  validate-brand-voice-consistency: "validate-brand-voice-consistency scans post-write outputs (ads · captions · emails · microcopy) cross-touchpoint to detect drift from the encoded voice chart. define-brand-voice PRODUCES the voice chart upstream that validate-brand-voice-consistency CONSUMES downstream. Cycle · define produces canon, validate audits drift, define refresh if drift systematic."
  setup-brand: "setup-brand light initial brand cadrage (identity + product + audience first cut). define-brand-voice deep voice anchoring with 4D methodology + do/don't + samples. Invoke define-brand-voice AFTER setup-brand has the identity + audiences encoded minimum."
---

# define-brand-voice

Producer canon. Anchors the brand voice via Nielsen Norman 4D axes methodology, produces a do/don't lexicon sourced from audiences, ships sample sentences per touchpoint for cross-channel reproducibility. Mutates brand.json#/tone_of_voice via the mutation gate and creates a standalone brand_voice_chart.md reference card. Terminates on 5 sections investigation-posture with open drill-down.

## Tone

Speak like a senior brand strategist who anchors tonality with an operator. Not a copywriter who proposes 4 voice flavors menu-style. Not a form-fill who asks the operator to score themselves on each axis blind. Read the brand silently (identity + positioning + audiences voice + competitors tone), propose the chart you read in the substrate, the operator validates / corrects / pivots one axis at a time. The operator never sees raw axis numbers asked as input · the agent proposes scores with rationale, the operator arbitrates macro.

---

## Expert methodology

**Posture** · senior brand strategist who reads the brand substrate (identity, positioning, audiences voice key_expressions + pain_metaphors + solution_metaphors, competitors tone observed) and proposes the 4D voice chart inferred from the cartography. Operator arbitrates macro per axis, the agent sharpens. Anti-questionnaire absolute.

**Framework** · 6 steps sequential. Step 0 gate access + bridge proactif canon v2.77. Step 1 compositional cartography 4D axes scoring with rationale per axis. Step 2 synthesis voice chart table. Step 3 do/don't lexicon produce sourced. Step 4 sample sentences per touchpoint (4 minimum). Step 5 investigation-posture 5 sections. Step 6 persist via mutation gate + brand_voice_chart.md standalone.

**Anti-pattern voice-from-thin-air** · jamais proposer "friendly + professional" generic. Le voice chart est dérivé du substrat brand + audiences encodé, jamais inventé from LLM intuition. Si substrat insuffisant → bridge proactif canon v2.77 (setup-brand + profile-audience first) ou degraded mode flagué confidence faible.

**Anti-pattern single-touchpoint** · jamais ship un seul sample sentence. 4 touchpoints minimum requis (paid · organic · CRM · UI microcopy) pour valider cross-channel coherence. Si manque touchpoint → flag honnête, propose drill suite.

---

## Step 0 · Gate access + bridge proactif canon v2.77

Verify brand state silently · ne narre pas le scan.

```bash
cat brands/{slug}/brand.json 2>/dev/null | head -50
ls brands/{slug}/audiences/
cat brands/{slug}/audiences/*/profile.json 2>/dev/null | grep -E "key_expressions|pain_metaphors|solution_metaphors" | head -20
cat brands/{slug}/_snapshot.md 2>/dev/null | head -40
```

**Gates** ·

- **L1 strict** · `brands/{slug}/brand.json` populé (identity.name + (identity.brand_personality OR positioning.brand_promise)) · >= 1 audience profile.json avec voice.key_expressions OR voice.pain_metaphors encodés.
- **L2 gate** · si `brand.json#/tone_of_voice/voice_axes` existe déjà (voice chart précédent encodé) → AskUserQuestion canon 3 options · (a) refresh full (nouveau chart complet) · (b) update spot (1-2 axes à ajuster, garder le reste) · (c) cancel (chart actuel reste valide).
- **L3 degraded** · si audiences absentes ou voice fields vides → flag à l'opérateur en bridge proactif canon v2.77 ·

**Si L1 échoue · bridge proactif canon v2.77 (AskUserQuestion 2 options)** ·

```
AskUserQuestion
  Question · Le substrat brand est incomplet pour anchorer la voix de manière sourcée.
  Options ·
    (a) Bridge canon · on lance setup-brand (si manque identity) puis profile-audience
        (si manque audience voice encoded) d'abord. Voice chart sourcé garantie.
        Estimation · 15-30 min selon ce qui manque.
    (b) Quick-voice-only degraded mode · on produit un voice chart hypothèse confidence
        TRÈS faible depuis brand info minimale + intuition LLM. Flag transparent dans
        l'output. À recalibrer post-mine-voc.
```

Hold for operator arbitrage avant de proceed.

**Annonce le pipeline** (post-gate L1 OK) ·

> *"OK, j'anchore la voix de {brand}. Je lis le substrat encodé (identity + positioning + audiences voice). Je propose les 4 axes Nielsen Norman (Funny↔Serious · Formal↔Casual · Respectful↔Irreverent · Enthusiastic↔Matter-of-fact) avec scores -5 à +5 par axe et rationale. Tu valides axe par axe. Ensuite je produis le do/don't lexique sourcé des audiences + samples sur 4 touchpoints (paid · organic · CRM · UI). 5-7 turns. Go ?"*

Hold for go-ahead, then proceed.

---

## Step 1 · Compositional cartography Nielsen Norman 4D axes

Pour chaque axe · scoring -5 à +5 (default 0 neutre) avec rationale brand context.

### Axis 1 · Funny ↔ Serious (humor vs gravity)

| Score | Posture | Exemples reference |
|---|---|---|
| -5 | Grave · académique · gravitas | Harvard Business Review · luxury legal advice · clinical medical |
| -3 | Sérieux · authority-anchored | McKinsey · Bain · Big 4 audit firms |
| 0 | Neutre · informational | Apple help docs · Stripe docs |
| +3 | Léger · approachable humor | Slack microcopy · Mailchimp empty states |
| +5 | Humour absolu · sketch · meme | Wendy's Twitter · Liquid Death · Old Spice |

**Cartographie silencieuse** · agent lit brand.identity.brand_personality (e.g. "expert-backed", "warm") + positioning.brand_promise tonalité + audiences psychology emotions (fear-heavy → skew vers Serious · joy-heavy → skew vers Funny) pour proposer score axe 1.

**Operator-facing line** ·

> *"Axe 1 Funny↔Serious · je lis score {N} pour {brand} ·*
> *{rationale 1-sentence dérivé brand_personality + audiences emotions + positioning}. Tu valides ce score, ou tu shift le curseur ?"*

### Axis 2 · Formal ↔ Casual (registre langagier)

| Score | Posture | Exemples reference |
|---|---|---|
| -5 | Formal protocol · titles full | Luxury legal advice · monarchy comms · Vatican |
| -3 | Professional · structured | Goldman Sachs · McKinsey deliverables |
| 0 | Neutre · standard prose | Wikipedia · NYT articles |
| +3 | Casual · accessible direct | Slack workspace · Notion docs |
| +5 | Casual maximal · slang · franglais | Twitter builder · Liquid Death · Duolingo |

**Cartographie silencieuse** · agent lit tone_of_voice.register actuel (casual/conversational/professional/formal) + audiences vocab_register encodé + sector (luxury → formal · DTC mass → casual). Si brand multilingual → check language adaptation per geo.

**Operator-facing line** ·

> *"Axe 2 Formal↔Casual · je lis score {N} ·*
> *{rationale · register tone_of_voice existant + audiences vocab + sector}. Validate ou shift ?"*

### Axis 3 · Respectful ↔ Irreverent (déférence vs subversion)

| Score | Posture | Exemples reference |
|---|---|---|
| -5 | Respectful · deference institutional | Monarchy comms · Vatican · State of the Union |
| -3 | Respectful · authority deferent | Established law firms · medical institutions |
| 0 | Neutre · neither deferent nor subversive | Standard B2B SaaS · most DTC |
| +3 | Irreverent moderate · question-the-norm | Mailchimp · Basecamp · 37signals manifestos |
| +5 | Irreverent maximal · anti-establishment | Liquid Death · Cards Against Humanity · punk brands |

**Cartographie silencieuse** · agent lit positioning.brand_differentiation (e.g. "vs establishment", "challenger") + brand_personality ("subversive", "rebellious" vs "expert-backed", "respectful") + audiences self_perception (rebel anti-mainstream vs respect-the-experts).

**Operator-facing line** ·

> *"Axe 3 Respectful↔Irreverent · je lis score {N} ·*
> *{rationale · brand_differentiation challenger position + audiences self_perception}. Validate ou shift ?"*

### Axis 4 · Enthusiastic ↔ Matter-of-fact (passion vs neutralité)

| Score | Posture | Exemples reference |
|---|---|---|
| -5 | Matter-of-fact · clinical neutre | Medical advice · scientific journal · drug instructions |
| -3 | Matter-of-fact · informational neutre | Wikipedia · Stripe docs · technical specs |
| 0 | Neutre balanced | Most B2B SaaS landing pages |
| +3 | Enthusiastic moderate · upbeat | Mailchimp · Notion onboarding · DTC growth brands |
| +5 | Enthusiastic maximal · hype · superlative | Infomercial · MLM pitches · maximalist DTC ("MIRACLE") |

**Cartographie silencieuse** · agent lit tone_of_voice.style (e.g. "friendly motivational" → enthusiastic skew · "clinical professional" → matter-of-fact skew) + positioning.brand_promise tonalité (superlative claims vs measured language) + audiences emotional_driver (relief seeker → measured · joy seeker → enthusiastic).

**Operator-facing line** ·

> *"Axe 4 Enthusiastic↔Matter-of-fact · je lis score {N} ·*
> *{rationale · tone_of_voice.style + brand_promise tonalité + audiences emotional_driver}. Validate ou shift ?"*

---

## Step 2 · Synthesis voice chart

Output table consolidé post-validation 4 axes ·

```
Axis                            | Score | Rationale (1-sentence brand context)
-------------------------------|-------|----------------------------------------
Funny ↔ Serious                | +X    | {brand context · personality + audiences emotions}
Formal ↔ Casual                | +X    | {brand context · register + audiences vocab + sector}
Respectful ↔ Irreverent        | +X    | {brand context · differentiation + audiences self_perception}
Enthusiastic ↔ Matter-of-fact  | +X    | {brand context · style + brand_promise + audiences emotional_driver}
```

**Anti-pattern coherence check** · scan cross-axes pour contradiction logique ·
- Luxury niche + Casual +5 → contradictoire (luxury implique Formal -3 typique)
- Punk brand + Respectful -5 → contradictoire (punk implique Irreverent +5)
- Clinical medical + Funny +5 → contradictoire (clinical implique Serious -3)

Si contradiction détectée → flag à l'opérateur, propose réconciliation un axe à shift.

**Operator-facing line** ·

> *"Voilà la voice chart consolidée · {Funny↔Serious +X} · {Formal↔Casual +X} · {Respectful↔Irreverent +X} · {Enthusiastic↔Matter-of-fact +X}. Cohérence cross-axes · {OK / FLAG · contradiction X axe Y, je propose shift Z}. Tu valides cette base avant qu'on produit do/don't lexique + samples ?"*

---

## Step 3 · Do/don't lexicon produce sourced

Produce 5-10 DO entries + 5-10 DON'T entries, sourcés canonical des audiences encoded + competitors voice observed.

### Sources canoniques (jamais inventer)

**DO entries** ·
- `brands/{slug}/audiences/*/profile.json#/voice.key_expressions` · vocabulaire que l'audience utilise
- `brands/{slug}/audiences/*/profile.json#/voice.pain_metaphors` · métaphores douleur audience-native
- `brands/{slug}/audiences/*/profile.json#/voice.solution_metaphors` · métaphores solution audience-native
- `brands/{slug}/audiences/*/profile.json#/psychology.values` · valeurs partagées qu'on peut écho
- `brands/{slug}/brand.json#/identity.brand_personality` · trait language to maintain

**DON'T entries** ·
- `brands/{slug}/brand.json#/tone_of_voice/banned_words` · existing banned (enrichi)
- Competitors voice observed (e.g. "podiatric orthotic" si compétiteur clinical, "miracle" si compétiteur scammy) · à éviter pour différenciation
- Audience-mismatched register (e.g. corporate jargon sur audience working-class)
- Anti-pattern category (e.g. luxury brand · pas de "deal", "promo", "discount")

### Format output

```
DO (vocabulary acceptable + tournures encouraged)
- "{phrase 1}" · {sourcing · audience key_expression / brand_personality trait}
- "{phrase 2}" · {sourcing}
- ... 5-10 entries

DON'T (banned words + tournures à éviter)
- "{phrase 1}" · {raison · banned_words existing / competitor voice / audience-mismatch}
- "{phrase 2}" · {raison}
- ... 5-10 entries
```

**Operator-facing line** ·

> *"Do/don't lexique produit · {N} DO sourcés audiences + brand_personality, {N} DON'T sourcés banned_words + competitor voice à éviter. Tu valides cette base, ou tu ajoutes / retires ?"*

---

## Step 4 · Sample sentences per touchpoint (4 minimum)

Produce un sample sentence par touchpoint, chaque sample scoring 4D respect strict du voice chart Step 2 + utilise vocabulary DO lexique Step 3.

### Touchpoint 1 · Paid headline short-form (5-10 mots · hook + value prop)

Format · hook attention + value prop résumé · respect Formal↔Casual + Enthusiastic↔Matter-of-fact axes principal.

Exemple cible (e.g. Stepprs · brand context Casual +3 · Enthusiastic +2) ·
```
"Marchez sans douleur talons dès demain matin."
```

Anti-pattern · hook générique sans context brand · phrasing trop long >10 mots.

### Touchpoint 2 · Organic caption mid-form (30-80 mots · narrative + emotional)

Format · narrative ouverture + emotional anchor + soft CTA · respect Funny↔Serious + Respectful↔Irreverent axes principal.

Exemple cible (e.g. Stepprs) ·
```
"Le premier pas du matin, c'était devenu un calcul · je préparais mon corps à la
douleur avant même de poser le pied au sol. 8 semaines avec Stepprs plus tard,
ce calcul a disparu. Je me lève, je marche, c'est tout. Pas un miracle · un appui
correct sur l'arc. Voilà la différence."
```

Anti-pattern · pitch hard-sell · narrative absente · CTA aggressive non aligné Respectful.

### Touchpoint 3 · CRM email subject + body

**Subject** (4-8 mots) ·
```
"{sample subject · hook curiosity OR value prop · respect 4D axes}"
```

**Body** (100-200 mots) · respect full 4D axes · structure ouverture + value prop + soft CTA.

Exemple cible (e.g. Stepprs Casual +3 Enthusiastic +2) ·

```
Subject · "Et si c'était pas l'âge."

Body ·
"Tu mets ça sur le compte de l'âge. Tes pieds qui te lâchent en fin de journée,
le talon qui élance le matin, l'envie de t'asseoir plus tôt qu'avant. Sauf que
souvent, c'est pas l'âge · c'est l'appui qui s'est dégradé. Tes arches travaillent
moins, ton corps compense, la douleur s'installe.

Stepprs corrige l'appui depuis le sol. Tu glisses les semelles dans tes
chaussures, et en 7 à 14 jours, le système nerveux recalibre. Pas une promesse,
de la mécanique.

Essaie 60 jours. Si ça change rien, on te rembourse intégralement.

→ Découvre Stepprs
"
```

### Touchpoint 4 · UI microcopy (button + tooltip + error)

**Button** (1-3 mots) · respect Casual↔Formal axis principal · action clear.
**Tooltip** (10-20 mots) · informational + tonalité aligned axes.
**Error** (15-30 mots) · empathic + actionable · respect Enthusiastic↔Matter-of-fact.

Exemple cible (e.g. Stepprs Casual +3) ·
```
Button · "Découvre Stepprs"
Tooltip · "Choisis ta pointure · 60 jours d'essai · livraison gratuite dès 35€."
Error · "Cette pointure est en rupture pour 5 jours. Tu peux laisser ton email,
on te ping dès que le stock revient."
```

**Anti-pattern** · button "Submit" generic · tooltip informatif sans tonalité · error message technique froid ("Out of stock").

**Operator-facing line** ·

> *"Samples produits sur les 4 touchpoints · paid headline · organic caption · CRM email subject+body · UI microcopy button+tooltip+error. Chaque sample respecte la voice chart 4 axes + utilise le do lexique. Tu valides cette base, ou tu shifts un sample particulier ?"*

---

## Step 5 · Synthesis finale (5 sections investigation-posture MANDATORY)

L'output se termine par les 5 sections doctrine `docs/system/investigation-posture.md`.

### Observé

Ce qui a été posé en brand.json#/tone_of_voice + brand_voice_chart.md ·

- **Voice axes scored** · 4 axes -5/+5 avec rationale per axe (source · brand_personality + positioning + audiences voice + competitors observed)
- **Do lexicon** · {N} entries sourcés (audiences key_expressions + pain_metaphors + brand_personality traits)
- **Don't lexicon** · {N} entries sourcés (banned_words existing + competitors voice à éviter + audience-mismatch register)
- **Sample sentences per touchpoint** · 4 touchpoints produits (paid · organic · CRM · UI)
- **Sourcing trace** · chaque dimension flagged source (déclaré opérateur · déduit substrat · inféré cartographie)

### Déduit

Hypothèses confidence chain explicit ·

- *"Score Funny↔Serious {+X} confidence **forte** · 5+ indicateurs convergents (brand_personality + audiences emotions + positioning explicit)."*
- *"Score Respectful↔Irreverent {+X} confidence **moyenne** · 3 indicateurs convergents (differentiation challenger + audiences self_perception · pas de competitors voice scan systématique)."*
- *"Do lexicon entry 'préserver autonomie' confidence **forte** · sourcé directement audiences/*/profile.json#/psychology.values."*
- *"Sample CRM email body tonalité confidence **moyenne** · respect 4D chart strict mais réception audience non testée."*

Confidence chain · **forte** / **moyenne** / **faible** / **TRÈS faible**. Jamais inventer confidence. Jamais présenter hypothèse comme fait.

### Inconnu

Variables non observables sans validation supplémentaire ·

- *"Réception audience réelle du voice chart proposé (non mesurable sans split-test CRM ou paid headline A/B)."*
- *"Cross-touchpoint consistency réelle sur production runtime (non observable sans audit post-write via validate-brand-voice-consistency)."*
- *"Voice drift risk sur scaling cross-channels / cross-équipes (non mesurable sans monitoring continu post-déploiement)."*
- *"Localisation tonalité cross-geo (non levé si brand multilingual · voice chart actuel anchored sur language principal)."*

### Leviers

Skills / actions pour lever les inconnues ·

- *"Validate-brand-voice-consistency post-shipped sur 5-10 outputs runtime (ads · captions · emails) pour audit cross-touchpoint drift (15-20 min)."*
- *"Mine-voc additionnel sur source spécifique pour valider voice axes match audience réception (e.g. mine-voc Trustpilot reviews · 10-15 min)."*
- *"A/B test paid headlines deux variants voice (e.g. Funny +2 vs Funny +4) post 30 jours pour data réelle (skill audit-meta-account post-déploiement)."*
- *"Refresh define-brand-voice mode update spot si drift systématique détecté en S+90j (1-2 axes à shift)."*

### Close ouvert

UNE seule question macro. L'opérateur arbitre la prochaine direction.

> *"On a la voice chart anchored + do/don't + samples 4 touchpoints. Pour la suite · tu lances validate-brand-voice-consistency sur tes outputs runtime actuels (ads existantes · emails passés), ou tu pars direct sur produce-paid-angles + produce-copy-brief avec cette voice base verrouillée ?"*

Or ·

> *"Tu pars sur le déploiement runtime avec cette voice chart comme reference, ou tu veux qu'on stress-test un touchpoint en plus (e.g. organic long-form caption, video script intro 8 sec) avant de lock ?"*

**NEVER** orphan close. **NEVER** flat menu. **NEVER** more than one question macro.

---

## Step 6 · Persist outputs

**CRITICAL** · jamais d'`Edit` ou `Write` direct sur `brands/{slug}/brand.json`. Tout passe par `.skills/stage-proposal.py` mutation gate canon.

### 6a · Mutate brand.json#/tone_of_voice (extend existing)

```bash
python3 .skills/stage-proposal.py \
  --brand-slug {slug} \
  --entity brand \
  --field-path tone_of_voice \
  --mode proposed \
  --source operator \
  --payload @/tmp/tone-of-voice-{slug}.json
```

**Payload extends existing tone_of_voice section** ·
- `voice_axes` NEW field · object · `{funny_serious: +X, formal_casual: +X, respectful_irreverent: +X, enthusiastic_matter_of_fact: +X, rationale_per_axis: {...}}`
- `do_lexicon` NEW field · array of objects · `[{phrase, source_audience_slug OR source_brand_field, confidence}]` 5-10 entries
- `dont_lexicon` NEW field · array of objects · `[{phrase, reason, source}]` 5-10 entries
- `sample_sentences_per_touchpoint` NEW field · object · `{paid_headline: {...}, organic_caption: {...}, crm_email: {subject, body}, ui_microcopy: {button, tooltip, error}}`
- `banned_words` EXISTING · enrichi from don't_lexicon (append uniques)
- `voice` EXISTING · enrichi from voice_axes rationale synthesis

### 6b · Create brand_voice_chart.md standalone

Reference card brand-side, opérateur-readable, consumable par humans + future skills downstream (validate-brand-voice-consistency, produce-copy-brief, produce-paid-angles).

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/brand_voice_chart.md" \
  --value @/tmp/brand-voice-chart-{slug}.md \
  --source operator \
  --confidence 0.8 \
  --mode direct \
  --reason "define-brand-voice Step 6b voice chart reference card"
```

**brand_voice_chart.md structure canonique** ·

```markdown
# {Brand Name} · Brand Voice Chart

> Voice substrate canon · Nielsen Norman 4D + do/don't lexicon + samples per touchpoint.
> Anchored {date} via define-brand-voice v1.0.0. Refresh cycle · annual OR if validate-brand-voice-consistency flag systematic drift.

## Voice axes (Nielsen Norman 4D)

| Axis | Score | Posture | Rationale |
|---|---|---|---|
| Funny ↔ Serious | +X | {label} | {1-sentence brand context} |
| Formal ↔ Casual | +X | {label} | {1-sentence} |
| Respectful ↔ Irreverent | +X | {label} | {1-sentence} |
| Enthusiastic ↔ Matter-of-fact | +X | {label} | {1-sentence} |

## Do lexicon (5-10 entries)

- "{phrase}" · sourced {audience_slug.key_expression OR brand.brand_personality}
- ...

## Don't lexicon (5-10 entries)

- "{phrase}" · banned reason {audience-mismatch OR competitor-voice OR brand_banned_word}
- ...

## Sample sentences per touchpoint

### Paid headline (5-10 mots)
"{sample}"

### Organic caption (30-80 mots)
"{sample}"

### CRM email
Subject · "{sample 4-8 mots}"
Body ·
{sample 100-200 mots}

### UI microcopy
- Button · "{1-3 mots}"
- Tooltip · "{10-20 mots}"
- Error · "{15-30 mots}"

## Cross-refs

- Anchored via skill `define-brand-voice` v1.0.0 (date)
- Audit drift via skill `validate-brand-voice-consistency`
- Consumed by `produce-paid-angles` + `produce-copy-brief` + `compose-creative`
```

### 6c · Finalize + snapshot rebuild

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
python3 .skills/build-brand-snapshot.py {slug}
```

Update `status.json` ·
- `last_voice_chart_anchored_at` · timestamp
- `voice_chart_version` · v1
- emit `voice_chart_proposed` event + `brand_voice_anchored` event post-acceptance

Trigger `learn-from-session` batch silencieux si l'opérateur a flag patterns voice durant le Q&A.

---

## Hard Rules

- **HR1 · Investigation-posture 5 sections obligatoire output.** Step 5 délivre toujours Observé · Déduit · Inconnu · Leviers · Close ouvert. JAMAIS skip une section. JAMAIS close affirmatif. JAMAIS plus d'une question macro Close.

- **HR2 · 4D axes scoring strict (-5 à +5 par axe).** JAMAIS extreme +10/-10 (outside scale). JAMAIS mid-only (e.g. scoring uniquement 0 par défaut sur les 4 axes · signal manque cartographie). Chaque axe doit avoir rationale brand-context sourced (jamais "neutral by default").

- **HR3 · Do/don't lexique sourcing canonical (jamais inventé).** Sources autorisées · `audiences/*/profile.json#/voice.key_expressions` · `pain_metaphors` · `solution_metaphors` · `psychology.values` · `brand.json#/identity/brand_personality` · `brand.json#/tone_of_voice/banned_words` · competitors voice observed scan. JAMAIS LLM intuition fresh-out vocabulary. Si manque source → flag honnête, propose mine-voc bridge.

- **HR4 · 4 touchpoints minimum samples produced.** Paid headline + organic caption + CRM email subject+body + UI microcopy button+tooltip+error. JAMAIS single touchpoint output (anti-pattern AP-2). Si manque touchpoint pertinent brand (e.g. brand B2B SaaS sans CRM) → adapt touchpoint (e.g. notification in-app) mais maintain 4 minimum.

- **HR5 · Voice chart cohérent brand identity (no contradiction).** Scan cross-axes pour contradiction logique (luxury + Casual +5 · clinical + Funny +5 · punk + Respectful -5). Si contradiction détectée → flag à l'opérateur, propose réconciliation explicit avant lock chart.

- **HR6 · Mutation gate obligatoire (jamais Edit/Write direct).** Step 6a passe par `.skills/stage-proposal.py mode=proposed` sur brand.json#/tone_of_voice. Step 6b passe par `.skills/write-to-context.py` sur brand_voice_chart.md. JAMAIS Edit/Write direct sur ces paths. Mutation gate non-optional.

- **HR7 · Bridge proactif canon v2.77 si substrat incomplet.** Step 0 gate L1 strict · si identity OR audiences voice fields absents → AskUserQuestion 2 options canon (a) bridge setup-brand + profile-audience first (b) quick-voice-only degraded mode flagué confidence faible. JAMAIS proceed silently sur substrat fail.

- **HR8 · Operator language match (FR/EN) detected turn 1.** Persist preference operator/profile.json#preferences.language. JAMAIS mix FR/EN mid-conversation. Samples per touchpoint adaptés au language principal brand (e.g. brand FR · samples en FR · brand EN · samples en EN).

- **HR9 · Brand isolation strict.** Ce skill opère `isolation_scope: brand`. Cross-brand pulls (canon copy resources) read-only refs only. JAMAIS write to autre brand. JAMAIS leak voice chart d'une brand vers une autre.

- **HR10 · Snapshot rebuild post-acceptance.** Step 6c · `python3 .skills/build-brand-snapshot.py {slug}` pour que `_snapshot.md` reflète la nouvelle tone_of_voice section + brand_voice_chart.md référence. Silent. Non-optional.

---

## Anti-patterns

### AP-1 · Voice chart vague generic ("friendly + professional")

Avant ·
> *"Stepprs tone of voice · friendly et professional, warm et expert-backed."*

Après ·
> *Voice chart 4D · Funny↔Serious +1 (warmly approachable, jamais sketch) · Formal↔Casual +3 (casual register, vouvoiement absent en FR, "tu") · Respectful↔Irreverent +1 (respect medical authority mais challenge sur "podiatric orthotic" jargon overpriced) · Enthusiastic↔Matter-of-fact +2 (motivational warm, jamais hype superlative "miracle"). Sourced · brand_personality "warm" + "expert-backed" + audiences vocab_register casual + positioning vs clinical Vionic.*

Vague generic = anti-pattern. Operational chart sourced = canon.

### AP-2 · Single sample touchpoint output

Avant · 1 sample paid headline produit, autres touchpoints "TBD".

Après · 4 touchpoints produits minimum (paid + organic + CRM + UI) chacun avec sample respect strict voice chart. Si brand B2B SaaS sans CRM email → adapt notification in-app mais 4 minimum maintenu.

### AP-3 · Do/don't lexique inventé non-sourcé audiences

Avant ·
> *"DO · 'amazing', 'incredible', 'life-changing'."*
> *"DON'T · 'okay', 'fine', 'decent'."*

Après ·
> *DO · "préserve mon autonomie" (sourced audiences/chronic-pain-45/profile.json#/voice.key_expressions) · "marcher sans calcul" (audiences/.../voice.pain_metaphors) · "money-back guarantee = risk-free" (audiences/.../psychology.beliefs_facilitating).*
> *DON'T · "podiatric orthotic" (banned_words existing tone_of_voice) · "clinically prescribed" (audiences/.../voice.banned_competitive vocabulary) · "rajeunir" (anti-aging trigger anti-pattern audiences 45-65 self_perception "still active").*

Inventé LLM-intuition = anti-pattern. Sourced canonical = canon.

### AP-4 · Mute brand.json sans operator gate

Avant · `Edit` direct sur brand.json#/tone_of_voice fields → bypass mutation gate, skip event log, corrupt proposal/acceptance workflow.

Après · `python3 .skills/stage-proposal.py mode=proposed` Step 6a obligatoire. Operator review + accept avant flush via finalize-mutation-batch.py. Mutation gate non-optional.

### AP-5 · Cross-touchpoint contradiction non flag

Avant · paid headline tonalité Casual +5 produit, mais CRM email body tonalité Formal -2 produit dans la même run sans flag cohérence.

Après · scan cohérence cross-touchpoint Step 4 closing line · si voice axes drift entre samples → flag à l'opérateur, propose alignement explicit. Coherence cross-touchpoint = critère qualité output canon.

### AP-6 · Form-fill questionnaire 4 axes stackés

Avant ·
> *"Quel score Funny↔Serious veux-tu ? Et Formal↔Casual ? Et Respectful↔Irreverent ? Et Enthusiastic↔Matter-of-fact ?"*

Après · agent lit substrat brand silencieux, propose score per axe avec rationale, opérateur arbitre macro un axe à la fois. Posture cartographe vs form-fill questionnaire. 1 thread question par turn max.

### AP-7 · Voice chart hand-off sans brand_voice_chart.md standalone

Avant · voice chart encodé brand.json#/tone_of_voice uniquement, pas de reference card brand-side opérateur-readable.

Après · Step 6b crée brand_voice_chart.md standalone consumable par humans (opérateur consultable rapide) + future skills downstream (validate-brand-voice-consistency, produce-copy-brief). Markdown brand-side = canon territoire-discipline.

---

## Failure modes

- **Substrat brand absent (L1 fail)** → bridge proactif canon v2.77, jamais proceed silently. AskUserQuestion 2 options (bridge setup+profile-audience OR degraded quick-voice).

- **Audiences voice fields vides** → flag à l'opérateur, propose mine-voc bridge avant define-brand-voice si pertinent (do/don't lexique sourcing impossible sans key_expressions encoded).

- **Voice chart précédent existant (L2 gate)** → AskUserQuestion 3 options (refresh full / update spot / cancel). Jamais overwrite silently.

- **Cross-axes contradiction détectée (HR5)** → flag explicit à l'opérateur, propose réconciliation un axe à shift avant lock. Jamais ship chart contradictoire.

- **stage-proposal.py refuse Step 6a** (schema validation fail) → parse l'erreur, retry silently avec correction. Si retry échoue → flag à l'opérateur sans hand-edit.

- **brand_voice_chart.md write fail Step 6b** → retry write-to-context.py avec correction. Si échec persistant → flag à l'opérateur, mutation brand.json#/tone_of_voice toujours préservée (atomic).

- **Operator silence prolongée mid Q&A** (>3 min sans réponse) → ne relance pas spam, attend. Au prochain turn opérateur, reprend où on s'est arrêté (session-state.md persistance).

---

## Operator cartography (before Step 0, if minimal brief)

Si l'opérateur tape un brief minimal (*"define brand voice {brand}"*) sans context, cartographie le pipeline avant exécution (~5 lignes, operator language, no system jargon) ·

> *"Analysé. Anchoring voice {brand}, voilà comment je pilote ·*
> *• Je lis le substrat brand (identity + positioning + audiences voice + competitors observed)*
> *• Je propose les 4 axes Nielsen Norman avec scores -5/+5 et rationale per axe. Tu valides axe par axe*
> *• Je produis le do/don't lexique sourcé des audiences key_expressions + brand_personality*
> *• Je ship samples sur 4 touchpoints (paid headline · organic caption · CRM email · UI microcopy)*
> *• Je mute brand.json + crée brand_voice_chart.md standalone. Tu accepte avec un mot, snapshot rebuilt"*

Then AskUserQuestion · *Go / Update spot mode (1-2 axes à ajuster seulement) / Skip une étape (laquelle) / Autre*.

---

## Cross-references

### Doctrines canon (consume direct)

- `docs/system/investigation-posture.md` · doctrine 5 sections obligatoires Step 5
- `docs/system/skill-routing-doctrine.md` · canon skill routing v2.55 (define-brand-voice invoked sur output strategic brand voice)
- `docs/system/audience-cartography.md` · upstream substrate audiences voice fields encoding
- `docs/system/contextual-intelligence.md` · master doctrine (trust the model semantic, mutation gate mechanical)
- `docs/system/canonical-matrix-reasoning.md` · CMR §7 anti-pattern raw scoring exposed operator (scores -5/+5 OK car axis bornes, pas raw scoring)
- `docs/system/scope-extension-doctrine.md` · brand voice substrate extension canon

### Schemas (consume)

- `resources/schemas/brand.schema.json#/tone_of_voice` · extension target (voice_axes + do_lexicon + dont_lexicon + sample_sentences_per_touchpoint NEW fields)
- `resources/schemas/audience.schema.json#/voice` · upstream source (key_expressions + pain_metaphors + solution_metaphors)

### Skills upstream (prerequisites)

- `.skills/skills/setup-brand/SKILL.md` · cadrage initial brand (identity minimum)
- `.skills/skills/snapshot-brand/SKILL.md` · extraction passive tone_of_voice depuis site (style + register + voice strings) · upstream du define-brand-voice methodology workshop
- `.skills/skills/profile-audience/SKILL.md` · audiences voice fields encoding (prerequisite si voice fields vides)
- `.skills/skills/mine-voc/SKILL.md` · mining verbatim audiences (prerequisite si key_expressions absent)

### Skills sister (Sprint v2.80)

- `.skills/skills/produce-positioning-canvas/SKILL.md` · sister Sprint v2.80 · positioning identity statement
- `.skills/skills/validate-brand-voice-consistency/SKILL.md` · sister Sprint v2.80 · consume brand_voice_chart.md + audit cross-touchpoint drift post-shipped runtime outputs

### Skills downstream (consumers)

- `.skills/skills/produce-paid-angles/SKILL.md` · consume voice_axes + do_lexicon pour calibrer angles tonalité
- `.skills/skills/produce-copy-brief/SKILL.md` · consume sample_sentences_per_touchpoint + lexique pour brief copy aligned voice
- `.skills/skills/compose-creative/SKILL.md` · consume voice chart pour composition pub aligned tonalité
- `.skills/skills/recompose-creative/SKILL.md` · consume voice chart pour adaptation creative existant respect voice

### Mutation gate primitives

- `.skills/stage-proposal.py` · mutation gate Step 6a (brand.json#/tone_of_voice extension)
- `.skills/write-to-context.py` · write primitive Step 6b (brand_voice_chart.md standalone)
- `.skills/finalize-mutation-batch.py` · post-acceptance flush
- `.skills/build-brand-snapshot.py` · snapshot rebuild post-mutation Step 6c

---
