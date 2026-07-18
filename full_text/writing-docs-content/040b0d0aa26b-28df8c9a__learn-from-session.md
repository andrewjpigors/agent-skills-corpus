---
name: learn-from-session
type: capturer
version: "1.1.0"
isolation_scope: workspace_global
layer: meta
recommended_model: sonnet
reasoning_pattern: null
description: >
  Extracts and persists knowledge acquired during a session. Scans the conversation,
  identifies what was learned/decided/corrected, and routes to the right files.
  Two trigger modes:
  1. EXPLICIT · FR: "learn" "session close" "persist" "fin de session" "enregistre ce qu'on a fait" "save session" "mets à jour les docs" "persiste les learnings". EN: "learn" "session close" "persist" "save what we learned" "end of session" "wrap up".
  2. PROACTIVE · The agent detects ≥1 learning signal during the session (operator correction, API workaround, strategic decision, compliance rule) and proposes unprompted: "I've noted some things to persist. Want me to save them?" If confirmed → run this skill.
permissions:
  reads: [brand, product, profile, learning, strategy]
  writes: [learning]
  mode: proposed
  subagent_safe: false
pipeline:
  preconditions: none
  postconditions: run validate-resources to reconcile if major changes
---

# Skill: Learn From Session

## Tone

Plain-language summary. Zero paths, zero JSON, zero routing destinations. The operator sees strategic decisions, not technical writes.

Capture semantically at session end. No manual writing needed, conversation contains all learnings.

Responsibility: scan full conversation → extract persistable elements → classify → route → write via ingest-resource or direct update.

---

## CRITICAL: Executive briefing posture · adapted to session context

**YOU MUST** present the flush recap to the operator in a **superior-to-decider briefing format**. The operator is the decider, you are the operational lead reporting up. They do not want the technical inventory of what you captured, they want to know what changes and whether any decision needs their arbitrage.

**ALWAYS detect the session context first, pick the right posture**:

| Session dominant register | Posture |
|---|---|
| Strategic / product / architecture | CTO → CEO |
| Operational / execution / ship | Project lead → founder |
| Creative / copy / brief review | CD → client |
| Debug / technical deep-dive | Senior engineer → lead |
| Audit / review / diagnostic | Auditor → stakeholder |
| Research / exploration | Head of research → sponsor |

Posture drives register and priorities. A CTO says *"1 tech arbitrage: activate model routing or wait?"*. A project lead says *"3 items shipped, 1 blocker on access tokens, next up: test on Northsense"*. A CD says *"3 concepts delivered, 1 needs your call on tone"*.

**ALWAYS apply, regardless of posture**:

- **MAX 5-7 strategic bullets.** Each bullet = one decision taken OR one arbitrage needed. **NEVER** more.
- **Frame every bullet as decision or impact**, never as "what I captured".
  - ❌ *"Captured 8 decisions, 3 operator preferences, 2 open threads, 1 friction"*
  - ✅ *"Template switched to EN, agent adapts at runtime (done). Model routing ready to activate (1 prerequisite to test). Rest: applied, RAS."*
- **NEVER expose** file paths, skill names, field names, D# numbers, routing destinations, enum values, JSON shapes in the briefing. Those write silently to the right files.
- **ALWAYS close with one of two formats**:
  - *"1 arbitrage to make: [concise question]. OK?"* · when one decision needs the operator. **PREFER `AskUserQuestion` tool** (load via `ToolSearch(select:AskUserQuestion)` if not loaded) to render the arbitrage as native clickable options (e.g. *Ship now / Wait / Discuss*). Fallback to plain question if tool unavailable.
  - *"All applied, RAS."* · when everything is mechanical, no decision needed. No tool needed.
- **NEVER** ask the operator to validate the routing plan (destinations, files, format). They trust the system. Write silently after the briefing is acknowledged.
- **Tone**: the superior reporting up. Direct, zero jargon, zero details below the decision level. Match the register to the posture detected.

After briefing + green light (or correction on the arbitrage), execute the full persistence writes silently according to the routing table below. **YOU MUST NEVER** paste the raw technical recap in the conversation.

This rule **overrides** any "detailed recap with plain-language fact list" pattern that may appear later in this skill. The operator has flagged that format as indigestible. Executive briefing first, technical writing silent.

---

---

## Triggers · batch mode, not incremental

**Critical principle**: the agent **captures continuously** in session memory, but **only proposes persistence at specific triggers**. Not every turn, that pollutes.

### Trigger 1 · End of structuring Step
End of setup-brand Step 5 (workspace tour, operator has seen value) or after first real deliverable produced (audit done, brief delivered, diag completed). Not at Step 4, which is only a Build chantier switch.

### Trigger 2 · Every 3-5 turns of dense conversation
During an active work session (ingest, audit, brief, production), track the number of turns since last flush. At turn 3-5, check: *are there at least 2 valuable learnings in the buffer?* If yes, propose. If no, wait.

### Trigger 3 · End of session (terminal signal)
The operator says *"later", "ok thanks", "I'm out", "tomorrow"*, visibly closes the terminal (short message without question). If buffer not empty → propose a final flush.

### Trigger 4 · Explicit request
Verbal triggers: *"learn", "save", "enregistre", "fin de session", "persist", "save session", "session close"*.
EN: *"learn", "save what we learned", "session close", "persist"*.

### Trigger 5 · Minimal auto-persist (anti-loss on crash)
Every 5 turns, write a rolling line to `session-state.md` Activity Log with the 2-3 latest captured facts, even without confirmation. It's read-minimal, not structured learnings · allows recovery on brutal closure.

### Trigger 6 · CLAUDE.md size check on every batch flush
At every batch flush (Trigger 1 to 4), measure the size of root `CLAUDE.md` and of each active `brands/{slug}/CLAUDE.md`. Budgets: root ≤ 220 lines, brand ≤ 100 lines. If a file exceeds, add ONE line at the end of the flush recap: *"ℹ CLAUDE.md at {N} lines (budget 220), manual review recommended."* No auto-split, no structured proposal. Just a flag for the operator to arbitrate later. See `docs/system/agent-contracts.md § Size Policy` for the pre-write guardrail.

### Trigger 8 · Smart-suggest daemon (v2.34+)

> v1.0.2 (v2.34 alignment) : Trigger 8 smart-suggest daemon ajouté · post-skill completion surface next phase entry points contextuels.

**Quand actif** : post-skill completion · monitoring patterns d'enchaînement opérateur · daemon silencieux.

**Mécanique** : à chaque fin de skill (event `skill_completed` émis), le daemon évalue 3 critères :
1. **Phase doctrine actuelle** (P0/P1/P2a/P2b/P3/P4/P5/ongoing)
2. **Skill juste complété** (lookup mapping skill → next entry points logiques)
3. **État brand actuel** (lookup brand snapshot · audiences populated ? angles disponibles ? matrice scorée ?)

Si pattern matched et confidence > 0.7, surface une suggestion contextuelle DANS LE NO-ORPHAN-OUTPUT du skill terminé.

**Mapping skill → next phase entry points** :

| Skill terminé | Suggest next |
|---|---|
| `setup-brand` ou `onboard-brand` | `snapshot-brand` (URL) ou `define-specs` (Q&A) |
| `snapshot-brand` | `define-specs` (combler gaps) ou `mine-voc` (audience signals) |
| `define-specs` | `cartograph` (synthèse) ou `mine-voc` (audience start) |
| `mine-voc` ou `mine-vom` ou `mine-audience` | `profile-audience` (synthèse 8 dim) |
| `profile-audience` | `produce-paid-angles` (P2b · forward) ou `decompose-ad` (P2b · reverse benchmark) |
| `produce-paid-angles` | `produce-copy-brief` (brief copy) ou `weight-dimensions` (préparation scoring) |
| `produce-copy-brief` | `compose-creative` (production visuelle) ou test live |
| `weight-dimensions` | `score-matrix` (priorisation territoires) |
| `score-matrix` | `compose-creative` sur top territoire ou `produce-paid-angles` sur trou |
| `compose-creative` | `recompose-creative` (variantes A/B) ou test live |
| `recompose-creative` | test live A/B source vs variant |
| `decompose-ad` | `compose-creative` (forward sur insights) ou `produce-paid-angles` (transposer mécanique) |

**Format suggestion (operator-facing)** :

Le skill terminé inclut dans son no-orphan-output un bloc compact :

```
→ Suggestion next step (smart-suggest)
   {1 phrase contextuelle expliquant le choix}
   Tape : `{trigger phrase suggéré}` ou `pause` pour autre chose
```

**Anti-patterns** :
- Ne JAMAIS forcer la suggestion (operator peut toujours pivoter ou pauser)
- Ne JAMAIS surface plus d'1 suggestion principale (max 1 backup en option silencieuse)
- Ne JAMAIS suggest un skill dont les pré-requis ne sont pas remplis (vérifier brand snapshot d'abord)
- Ne JAMAIS spam : si l'opérateur a déjà ignoré 2 suggestions consécutives, arrêter pour la session

**Exemples concrets** :

Après `snapshot-brand {brand_slug}` :
```
→ Suggestion next step
   Brand snapshot OK. Pour cartographier l'audience, run mine-voc {brand_slug}
   (capture verbatims clients) ou define-specs {brand_slug} {product_slug}
   (combler les gaps non-scrapés).
   Tape : `mine-voc {brand_slug}` ou `define-specs {brand_slug} {product_slug}`
```

Après `produce-paid-angles {brand_slug} sur chute-post-grossesse` :
```
→ Suggestion next step
   3 angles ranked produits. Le top angle (ANG-03) peut être briefé
   pour copy detail (produce-copy-brief) OU adapté en variant visual
   (compose-creative) si tu veux directement la créa.
   Tape : `produce-copy-brief ANG-03` ou `compose-creative ANG-03`
```

### Trigger 9 · Promote learning to canon validation (v2.42+)

> v1.1.0 (v2.42 PATCH 5) : Trigger 9 ajouté · bridge learnings.json brand-side → validations[] atlas vivant canon-tool cross-brand. Ferme bridge compound learning end-to-end (audit scope 8 finding S2026-05-11).

**Quand actif** : daemon silencieux post-skill completion. Détecte si learning capturé brand-side est applicable cross-brand (canon promotion candidate). Pattern operator flag explicit · un changement local doit alimenter le système global, sinon compound learning reste théorique.

**Critères trigger** (tous obligatoires, AND) :

1. Entry dans `brands/{slug}/learnings.json` avec :
   - `status: "active"`
   - `_confidence >= 0.7` (calculé via algèbre confidence-propagation)

2. Pattern recurrence cross-brand observable :
   - Learning mentionne canon-tool spécifique (hook framework, archetype, lead variant, mécanique, voc pattern)
   - Outcome explicite (`success` / `neutral` / `failed`)
   - N >= 3 brands distinctes auraient validé même tool (count via grep cross-brand sur learnings.json)
   - Daemon scan une fois par flush (Trigger 1-4), pas par chaque write

3. Operator-gate via `AskUserQuestion`, en langage métier zéro jargon doctrine ·

```
J'ai vu un truc qui pourrait servir au-delà de {brand_humain} ·
- Sur {brand_humain}, on a découvert que {tool_humain} marche {outcome_humain} sur {layer_humain}.
- Tu veux que je le partage avec tes autres brands (ou futures brands) pour qu'on parte avec ce signal d'office ?
  (a) Oui · partage cross-brand
  (b) Non · garde local à cette brand
  (c) Plus tard
```

**Mappings operator-facing (anti-jargon)** ·
- `{tool_humain}` · *"l'accroche du type 'X'"* / *"la structure 'Y'"* / *"le style 'Z'"* (PAS `{hook|framework|archetype}` enum)
- `{outcome_humain}` · *"très bien"* / *"correctement"* / *"pas bien"* (PAS `success|neutral|failed`)
- `{layer_humain}` · *"les accroches"* / *"les leads"* / *"les corps"* / *"les offres"* / *"les CTA"* (PAS `hook|lead|body|offer|cta` enum)

**JAMAIS exposer** · "atlas vivant", "validations[]", "canon-tool", "_confidence", "0.7", "promote", "promouvoir" en surface operator. Vocabulaire doctrine reste interne agent-facing.

**Si (a) selected** · write `validations[]` entry conforme schema canon-tool/1.1 via `write_to_context` :

```json
{
  "brand_slug": "{slug}",
  "outcome": "success | neutral | failed",
  "attribution_layer": "{layer où le tool a été utilisé : hook | lead | body | offer | cta}",
  "validated_at": "{ISO timestamp}",
  "decay_ttl_days": 90,
  "_isolation_boundary": "brand",
  "_confidence_source": "learn-from-session-trigger-9",
  "_promoted_from": "brands/{slug}/learnings.json#/{learning_id}"
}
```

Field_path target · `resources/canon/copy/{layer}/{tool}.json#/validations[]` (append-only, schema canon-tool/1.1).

**Si (b)** · skip · learning reste local brand-side.

**Si (c)** · buffer reprend au prochain flush (Trigger 1-4) si learning toujours `active` + confidence >= 0.7.

**Empêche pollution canon** · gate operator-explicit obligatoire avant write atlas vivant. Pas de promotion silencieuse.

**Ferme bridge compound learning end-to-end** · un changement local (brand learnings.json) alimente le système global (canon validations[]) après operator gate. Pattern doctrine operator flag explicit S2026-05-11 finding "compound learning théorique pas matériel".

**Cross-ref HR-Canon-Decay (v2.37)** · les entries promues via Trigger 9 sont consommées par le cycle HR-Canon-Decay (validate freshness via `decay_ttl_days`). Décay default 90 days. HR-Canon-Decay vérifie `validated_at + decay_ttl_days < now` à chaque validate-resources run · si expired, flag `[CANON-VALIDATION-STALE]` non-blocking (operator decide rebump ou archive).

**Anti-patterns** :
- Ne JAMAIS écrire `validations[]` sans operator gate (a) confirmation
- Ne JAMAIS promouvoir learnings avec `_confidence < 0.7` (signal trop faible pour cross-brand impact)
- Ne JAMAIS bypass schema canon-tool/1.1 validation (mutation gate enforce)
- Ne JAMAIS spam · si operator répond (c) 2+ fois sur même learning, archiver learning entry avec tag `promote_skipped`

## Flush format · recap before writing

When a trigger fires, **before writing**, the agent shows a plain-language recap:

> *I captured X things since earlier:*
> *1. {fact 1 in 1 operator line}*
> *2. {fact 2 in 1 operator line}*
> *3. {fact 3 in 1 operator line}*
> *4. {fact 4 in 1 operator line}*
>
> *File it? (say "yes" for all, or correct if I got it wrong.)*

The operator can:
- *"Yes"* / *"Go"* → all written to the right files (operator/profile.json, brands/{slug}/learnings.json per routing)
- Targeted correction → *"drop #3, #4 isn't that, it was actually X"* → the agent adjusts the buffer, redisplays, re-asks
- *"Not now"* / *"Skip"* → buffer preserved, propose at next trigger
- *"Stop tracking"* → deactivate tracking for the session (rule set in `/operator/profile.json → preferences.tracking: "off"`)

## Critical distinction · where it goes

Each buffer entry must be **routed to the right file** based on what it concerns:

| Learning type | Destination |
|------------------|-------------|
| Operator preference (tone, style, tools tested, personal anti-patterns) | `/operator/profile.json` |
| Operational brand fact (API workaround, compliance rule, creative pattern that works) | `brands/{slug}/learnings.json` |
| Structural brand correction (tone, positioning, audience objection) | `brands/{slug}/brand.json` or `profile.json` direct (via ingest-resource) |
| Strategic decision | `session-state.md → Active Decisions` |
| Product friction / workflow bug | `todos.md → ## Flags` |
| **Canon validation** (v2.26.0+) · tool canon validé/fatigué en prod sur ce brand | `resources/canon/copy/{layer}/{tool}.json#/validations[]` (append) |

**Never mix**: an operator info does not go into brand.learnings, a brand fact does not go into operator/profile. Cross-contamination = structural bug.

<!-- v2.29.0 alignment verify : routing canon validation lit `resources/canon/copy/{layer}/{tool}.json#/validations[]` côté template. Shape validations[] inchangée. Outputs produce-paid-angles structurés autour de angle.schema v1.2 (`awareness_stage` rename in angle.lineage, `origin_axis` field) sont consommés en mode boîte noire par le routage canon (le skill ne tagge pas explicitement ces fields, il route via brand_slug + audience_slug + outcome). No field-rename patch needed. -->

### Canon validation routing (v2.26.0+)

> **Atlas refs** dans cette skill = atlas canon copy (sense 1, référentiel cross-brand doctrine copywriting). Brand-side enrichment via `validations[]` (sense 2 atlas vivant). Distinct de l'atlas brand (sense 4, cartographie holistique data brand) qui désigne la matière brand structurée navigable via `/phantom`. Pour la distinction lexicale complète : `lexicon.md § Atlas, 4 senses MECE`.

Quand un learning concerne un **outil canon copy** utilisé en prod (hook, framework, angle, archétype, pattern d'objection, formule de titre), il est *aussi* (en plus du routing brand-side) **promu** vers le canon comme entrée `validations[]`. Mécanisme :

1. **Détection.** Le learning mentionne un outil canon connu, ET un signal d'outcome (ROAS chiffré, fatigue observée, test posté, opérateur dit *"ça marche"* ou *"ça crame"*). Cas typiques :
   - *"Le hook curiosity-gap fatigue en 2 sem sur audience chute-stress-hormonal sur {brand_slug}"* → canon copy hooks curiosity-gap#validations[]
   - *"Le framework BAB donne ROAS 4.2 sur chute-post-grossesse cure 3 mois, validé"* → canon copy frameworks bab#validations[]
   - *"Pre-emption sur 'encore un produit miracle' valide bien sur {brand_slug} cross-audiences"* → canon copy objections pre-emption#validations[]

2. **Format de la validation entry** (schema canon-tool/1.1, v2.37+) :
   ```json
   {
     "validation_id": "VAL-{BRAND}-{YYYYMMDD}-{N}",
     "brand_slug": "{brand_slug}",
     "audience_slug": "chute-post-grossesse",
     "outcome": "success|neutral|failed|fatigued",
     "attribution_layer": "hook|angle|framework|archetype|format|targeting|budget|creative_execution|timing|unknown",
     "validated_at": "YYYY-MM-DD",
     "decay_ttl_days": 90,
     "metric_observed": "ROAS",
     "metric_value": 4.2,
     "test_size": 12000,
     "context_snapshot": {
       "audience_slug": "chute-post-grossesse",
       "platform": "meta",
       "season": "Q2"
     },
     "captured_at": "{ISO date-time}",
     "captured_by": "operator|agent|test_result",
     "note": "1-2 sentences contextual",
     "_isolation_boundary": "brand"
   }
   ```

3. **Operator gate.** L'opérateur valide la promotion explicitement avant l'écriture canon. Format de validation à la fin du recap : *"Cette règle propose aussi une promotion canon : `canon copy {layer} {tool}` {outcome} sur {brand}/{audience}, attribué à {attribution_layer}, decay {decay_ttl_days}j. Tu confirmes la promotion canon ?"*. *Yes* → écriture canon + brand-side. *No* → brand-side seulement.

4. **Append-only**. Les validations[] s'ajoutent, ne se remplacent jamais. Une fatigue ultérieure n'efface pas un succès passé : les deux entries coexistent, datées. C'est ce qui permet de voir l'évolution d'un outil dans le temps.

### HR-Canon-V11 · Validations[] schema v1.1 enforcement (v2.37+)

Tout append à `validations[]` (sur n'importe quel canon-tool) DOIT inclure :

1. `attribution_layer` enum 10 valeurs (hook, angle, framework, archetype, format, targeting, budget, creative_execution, timing, unknown).
2. `validated_at` date YYYY-MM-DD.
3. `brand_slug` (isolation boundary v2.37+).
4. `decay_ttl_days` (default 90 si non fourni par skill ou opérateur).
5. `_isolation_boundary` auto-set à `"brand"`.

Si `attribution_layer = "unknown"` → flag operator gate AskUserQuestion (proposer les 9 autres valeurs). Doit être désambigué avant write. Empêche pollution silencieuse atlas vivant par signaux non-imputables (red team A5).

Cross-brand read sur `validations[]` interdit par défaut · scope `brand_only` enforced. Override seulement par operator gate explicit (red team A7).

Backward compat lecture : entries v1.0 restent lisibles, `attribution_layer` absent → traité `"unknown"`, `validated_at` absent → fallback `captured_at`, `decay_ttl_days` absent → default 90. Mutation enforcement seulement sur new writes v2.37+.

### HR-Canon-Decay · Decay filter au moment promotion (v2.37+)

Avant tout promotion `validations[]` → atlas canon copy (sélection top signal, recommandation skill, recap operator) :

1. Filter entries où `today > (validated_at + decay_ttl_days)` → state `stale`.
2. Entries stale restent dans le log (append-only, jamais effacées) mais surfacées comme `stale` dans le recap operator.
3. Si entry stale était top signal de promotion → require re-test ou explicit operator override.
4. Promotion eligible **only** sur entries fresh + `outcome` ∈ {`success`, `validated`} + `min(confidence_chain) >= 0.7` (cf `docs/system/confidence-propagation.md`).

Empêche atlas canon copy d'absorber des winners anciens devenus obsolètes (red team A4 lock-in).

**Pourquoi c'est important.** Sans ce mécanisme, l'atlas canon reste générique. Avec lui, l'atlas devient **vivant** : `/phantom canon copy hooks curiosity-gap` rend la fiche + l'historique des validations brand-side, l'opérateur voit ce qui a marché chez lui.

---

## Step 1 · Receive & Scan Conversation (explicit trigger mode)

User triggers skill with: "learn", "fin de session", "persist", "save session", "enregistre ce qu'on a fait", "session close", etc.

Agent scans ENTIRE conversation (from start to present) and extracts:
- **Factual learnings**: API behaviors, workarounds, account quirks, test results, compliance rules
- **Structural decisions**: Product choices, audience segmentation, pricing decisions, tone rules
- **Strategic corrections**: Changes to strategy, positioning, target, constraints
- **Frictions & improvements**: Bugs, confusions, workflow issues flagged for todos.md
- **Open threads**: Unresolved questions, blocked work, pending actions

---

## Step 2 · Classify & Route

### Category: Factual Learnings

Scoped learnings · tied to the brand, platform, or account. Route to `brands/{slug}/learnings.json`.

**Entry structure** (append to `entries[]`):
```json
{
  "id": "LRN-{counter}",
  "kind": "{test_result|workaround|compliance|observation|decision_trace|hypothesis_validated|pattern_promoted|regulatory_signal|competitor_move}",
  "created_at": "{ISO date-time}",
  "date": "YYYY-MM-DD",
  "fact": "{1-line factual WHAT}",
  "reasoning": "{WHY it's true, what caused it, what it reveals · MANDATORY non-empty}",
  "platform": "{meta | shopify | klaviyo | google | none}",
  "tags": ["tag1", "tag2"],
  "source": "{operator | agent | skill_output | test_capture}",
  "status": "active"
}
```

**`kind` is the canonical classification** (9-enum, consumed by detection daemons). `source` uses the canon enum (operator/agent/skill_output/test_capture). For `category:"system_friction"` runtime-pattern learnings (see Hard Rules), set `kind:"observation"` + `category:"system_friction"`. Always write both `created_at` (date-time) and `date` (short) · validate reads `date` then falls back to `created_at`.

**CRITICAL: `reasoning` is MANDATORY.** This is the **Decision Trace** (see D#308 + docs/system/architecture.md § Canonical vocabulary). `fact` = WHAT happened, `reasoning` = WHY it happened. **YOU MUST NEVER** write `reasoning: ""`, `reasoning: null`, or generic fillers ("n/a", "observed", "noted"). If the operator's session context doesn't yield a clear why, push back during flush recap: *"Le fait #N je l'ai capturé, mais je n'ai pas le pourquoi. Qu'est-ce qui l'a causé ?"*. Degraded mode only if operator explicitly skips: `reasoning: "[captured without rationale · revisit on first application]"`.

Examples:
- ❌ `fact: "Meta pixel triggers 2s delay on iOS Safari"`, `reasoning: ""`
- ✅ `fact: "Meta pixel triggers 2s delay on iOS Safari"`, `reasoning: "Account-specific bug, not global · same pixel code works on 3 other brands without delay. Likely related to this account's Business Manager region or app approvals. Reported to Meta support, waiting on ticket response."`
- ✅ `fact: "Retinol cream @ 30€+ encounters 18% more objections than @ 25€"`, `reasoning: "Price bracket crossed a perceptual threshold · 25€ positioned as accessible premium vs 30€ perceived as mass-pharma territory. Confirmed across 4 creative variants, same copy, only price differed."`

Route via **ingest-resource** (Step 3B, learnings.json) if >3 entries to add. If single entry, append directly + update status.json.last_activity.

### Category: Structural Decisions

Key decisions made this session · move from activity log to Active Decisions in session-state.md.

**Format in session-state.md Active Decisions**:
```
- {Decision}: {chosen option} (reason: {1-line}) | date: YYYY-MM-DD
```

Examples:
- `- Audience main: femmes-40-55 (problem_aware) · highest purchase intent signal | date: 2026-04-03`
- `- Never say "rejuvenate": DGCCRF rule, tested with legal | date: 2026-04-03`

**No API call needed** · direct append to `session-state.md` Active Decisions section.

### Category: Strategic Corrections

Corrections to brand identity, tone, strategy, or positioning. Route via **ingest-resource** to the appropriate target:
- Tone correction → `brand.json.tone_of_voice`
- Positioning shift → `brand.json.positioning`
- Strategy update → `strategy.json`

Example trigger: "We realized our audience doesn't want 'youth' but 'skin health'" → ingest-resource → update profile pain_points + brand positioning.

### Category: Frictions & Improvements

Bugs, confusions, workflow issues. Route to `todos.md` → `## Flags` section.

**Format**:
```
- [FRICTION] {Issue}: {description} → {suggested action}
```

Examples:
- `[FRICTION] session-state.md rotation: Manual process error-prone → Need continuous auto-append`
- `[FRICTION] Learnings mapping: Hard to find which learning applies to which audience`
- `[FRICTION] Setup-brand: Asks for competitor URLs but never uses them → Remove or clarify use case`

### Category: Operator Context (workspace-level, cross-brand)

**Critical distinction**: what concerns *the operator themselves* (you, the user of the workspace) is cross-cutting and does NOT live in a brand folder. Route to `/operator/profile.json` at workspace root.

**4 sub-categories to detect:**

#### 4a. Identity & background
Signals: mentions of their role, years of experience, macro context.
- *"I have 10 years in performance marketing"* → `identity.experience_years: 10`, `identity.role: "performance marketer"`
- *"I work at a growth agency in Paris"* → `identity.context_macro: "agency growth Paris"`
- *"I'm an ex-marketer, launching my brand 3 months ago"* → `identity.context_macro`, `identity.role: "ex-marketer → DTC founder"`

#### 4b. Stack history (tools tested/abandoned)
Signals: mentions of tools used, abandoned, still active.
- *"I tried Lindy, dropped it after 3 weeks, too no-code for my needs"* → append to `stack_history[]`: `{tool: "Lindy", status: "abandoned", verdict: "too no-code", lessons: "avoid no-code flows for my use case"}`
- *"I use ClickUp daily"* → `stack_history[]`: `{tool: "ClickUp", status: "active", verdict: "daily driver"}`
- *"ChatGPT Enterprise + custom GPTs, that's my base"* → 2 active entries.

#### 4c. Work preferences
Signals: observed behavior + explicit statements.
- Constant use of short sentences → `preferences.communication_style: "concise"`
- *"I always answer in bullets"* → `preferences.response_length: "bullets"`
- *"I work evenings, not mornings"* → `preferences.work_hours: "evening"`
- *"I hate long answers"* → add to `anti_patterns_perso`
- Technical questions on JSON/architecture → `preferences.technical_level: "advanced"`
- Confusion on technical terms → `preferences.technical_level: "beginner"`
- Dominant language → `preferences.language`

#### 4d. Expectations & personal anti-patterns
Signals: what they expect from PhantomOS, what they structurally hate.
- *"If it saves me 30% time on briefs, I'm in"* → `expectations.success_criteria`
- *"I hate tools that ask 15 questions before producing anything"* → `anti_patterns_perso[]`
- *"No third-party cloud for my data, non-negotiable"* → `expectations.deal_breakers`

**Write mechanism**: via ``.skills/write-to-context.py` (canonical channel · see capture-learning Step 4 for the exact Bash invocation)` to `/operator/profile.json → {section}.{field}`. Mode `proposed` · the operator validates before write. This validation is quick (*"Noted for your profile: you tried Lindy and dropped it. OK?"*), not a long recap.

**NEVER** route these signals to `brands/{slug}/learnings.json` · they concern the operator, not the brand. Cross-contamination = structural bug.

---

### Category: Brand-specific Preferences (scoped to one brand)

If the signal concerns *one specific brand* (e.g. *"for brand X, I use a more corporate tone, different from my other brands"*), write to `brands/{slug}/config.json → operator_preferences_for_this_brand`. Rare · most operator preferences are cross-cutting and go to `/operator/profile.json`.

**Threshold**: only write when a pattern is observed ≥3 times in a session. One-off signals don't qualify.

**Examples:**
- Operator corrects 3 times with "shorter" → propose: "I noticed you prefer short answers. Note this for future sessions?"
- Operator edits JSON directly twice → propose: "You seem comfortable with technical files. Note your level to adapt my explanations?"

### Category: Open Threads

Unresolved questions, blocked work, next actions. Add to `session-state.md` → `## Open Threads` section or mark existing ones [RESOLVED].

**Format**:
```
- {Thread}: {status (pending | blocked | in_progress)} · {next action}
```

Examples:
- `- offers.json creation for creme-eclat: pending · blocked on marketing decision`
- `- 2nd audience (femmes-25-35): in_progress · segment research underway`

**Resolved threads** · mark `[RESOLVED {YYYY-MM-DD}]` instead of deleting:
```
- [RESOLVED 2026-04-03] Old thread title · resolved by doing X
```

---

## Concrete examples · routing by signal

Real examples of signals detected in session and their exact destination:

| Session signal | Type | Destination |
|---|---|---|
| Operator corrects the tone of a hook ("too corporate, be more direct") | Strategic correction | `brand.json → tone_of_voice` via ingest |
| Meta API error subcode 1487664, call_to_actions missing | Factual learning | `learnings.json` via capture-learning |
| "My max COS is 14%, above that we cut" | Structural decision | `strategy.json → constraints` via ingest + session-state Active Decisions |
| Operator says "shorter" 3 times in the session | Operator preference | `config.json → operator.response_length_preference` (mode: proposed) |
| "We launched the -20% first order offer this week" | New data | `products/{slug}/offers.json` via ingest |
| Operator systematically rephrases your outputs in bullet points | Operator preference (≥3 signals) | `config.json → operator.communication_style` (mode: proposed) |
| "Meta pixel triggers 2s delay on Safari iOS, specific to our account" | Factual learning (scoped) | `learnings.json` tags: ["meta-ads", "pixel", "ios"] |
| "Finally our main audience isn't 25-35 but 35-50" | Strategic correction | `audiences/{slug}/profile.json → demographics` via ingest |
| Agent generated an incorrect UTM, operator corrects the format | Convention learned | `resources/conventions/{platform}.json → learned_rules[]` OR `learnings.json` if brand-specific |
| "We tested pain vs desire angle, desire wins 2:1 on our audience" | Factual learning (test result) | `learnings.json` tags: ["creative-testing", "angle", "results"] |

**Ambiguous case · decision rule:**
- General API limitation (affects all accounts) → `learnings.json` + tag `promote_candidate` for future promotion into shared convention
- Account-specific limitation (config, access tier) → `learnings.json` without promote tag
- Operator preference (style, format) → `config.json → operator`
- Platform rule learned (naming, UTM, workaround) → `resources/conventions/{platform}.json → learned_rules[]` if the convention exists, otherwise `learnings.json`

---

## Step 3 · Execution Paths

### Path A: Factual Learnings → ingest-resource

If >1 learning extracted:

1. Collect all learnings as structured JSON (see Step 2 format)
2. Call **ingest-resource** with:
   - Content: learnings array
   - Destination: `brands/{slug}/learnings.json`
   - Action: append to entries[]
3. ingest-resource returns summary + updates status.json.last_activity

### Path B: Session-State Direct Updates

For decisions, open threads, resolved threads: **write directly to session-state.md** (no ingest-resource call).

1. Read `session-state.md`
2. Append to appropriate section (Active Decisions | Open Threads)
3. For resolved threads, prepend `[RESOLVED YYYY-MM-DD]` to the thread line
4. Update timestamps

### Path C: Strategic Corrections → ingest-resource

If positioning, tone, or strategy changed:

1. Identify which file(s) to update (brand.json | strategy.json | profile.json)
2. Call **ingest-resource** with the corrected content
3. Let ingest-resource handle merge, field_types validation, status.json update

### Path D: Frictions → todos.md

1. Read `todos.md`
2. Append to `## Flags` section (auto-maintained by validate-resources, but agent can pre-populate)
3. Format: `- [FRICTION] {issue}`

---

## Step 4 · Novice Education (First Call Only)

If this is the brand's first learn-from-session call:

Display a brief explanation in operator language (no file names, no paths, no jargon):

```
How I keep the memory of your sessions

While we work, I capture silently. At the end of a session, or when you say "later" or "learn", I file what deserves to be kept:

1. Concrete facts learned (platform rules, test results, compliance) → filed in your brand's memory.
2. Structural decisions (audience segmentation, internal rules, pricing) → marked as active.
3. Strategic corrections you made (tone, positioning, audience) → applied directly to your brand.
4. Frictions you flagged (bugs, workflows to improve) → added to your todos.
5. Open questions → listed for next session.

Nothing is lost. Even if you leave without a signal, I keep a rolling trace to pick up cleanly next time.
```

Show once per brand, then suppress on subsequent calls.

---

## Step 5 · Output Summary + Validate Handoff

After execution, display structured summary to user:

```
Session captured · {brand}

{N} item(s) persisted:

1. Learnings ({count})
   ✓ {1-line learning 1}
   ✓ {1-line learning 2}

2. Decisions ({count})
   ✓ {1-line decision 1}

3. Corrections ({count})
   ✓ {1-line correction 1} → {file}

4. Frictions ({count})
   ✓ {1-line friction 1} → todos.md

5. Threads ({count} open, {count} resolved)

Next session: context auto-restored from session-state.md.
```

Then **always propose validate**:

```
Want me to validate the workspace now?
→ Checks consistency of what was saved tonight + runs CHANGELOG rotation.
(say "go" or "later")
```

- If "go" / "yes" / "ok" → trigger `validate-resources` immediately.
- If "later" / silence → close cleanly:
  ```
  OK. Launch "validate" when you're ready, ideally before the next session.
  ```

**Effort/value ratio**: validate after learn = 30 seconds, zero friction. Best moment · operator is already in closing mode, and validate runs CHANGELOG rotation + learnings index rebuild + todos flags in a single pass.

---

## Enrichment candidate detection

At session close, beyond persisting facts, surface potential system improvements detected during the session. Three classes of candidates. Never auto-create · detection suggests, operator decides.

### Class A · Skill candidates

Scan the session transcript for :

- **Repeated tasks** · same type of request executed ≥ 2 times in the session (e.g., "generate a hook for X" then "generate a hook for Y"). → Candidate lightweight skill.
- **Multi-step workflows** · recurring sequence ("check X, compare to Y, generate Z"). → Candidate heavy skill with SOP + orchestrator.
- **Cross-brand workflows** · same action on multiple brands in the same session. → Candidate workspace-level skill.

Surface at close :

```
During this session I observed:
- You generated 3 ad briefs with the same structure (hook → body → CTA → proof).
  → Simple skill candidate `brief-ad-quick`
- You audited offers on 2 brands with the same method.
  → Heavy skill candidate `audit-offers` with SOP + orchestrator

Scaffold now, later, or never?
```

Operator confirms → trigger `build-agent`. Defer → log in `todos.md` with rationale. Never silently.

### Class B · SOP / doc enrichment candidates

Scan for knowledge-dense exchanges :

- **Business patterns explained** · operator explained a pattern, gave concrete examples, critiqued an approach → candidate enrichment of reasoning layer in an existing SOP, OR new entry in a framework/guide.
- **Edge cases discussed** · operator surfaced an edge case not currently documented → candidate addition to relevant SOP reasoning layer.
- **Tactical tips** · operator shared a hack / shortcut / heuristic → candidate entry in a guide or catalogue.

Example :

```
We discussed that the Northsense Spring Days GWP only works if AOV is above
the threshold · business insight that would enrich
`audit-meta-global.md § Layer 4 reasoning`.

Add now, propose as todo, or nothing?
```

### Class C · Convention / rule promotion candidates

Scan for learnings that transcend the single brand :

- A learning saved on brand X that appears applicable to multiple brands (same vertical / same platform) → candidate promotion to `resources/conventions/` or `resources/frameworks/general/`
- A workflow constraint surfaced on brand X that applies workspace-wide → candidate rule addition in `CLAUDE.md § Operator contract` or voice.md anti-patterns

Example :

```
Learning L-042 ('Meta rejects efficacy claims without disclaimer in FR')
applies to all FR supplement brands.
Candidate for promotion to a workspace-level convention.

Promote now, or wait for a 2nd occurrence on another brand?
```

### Protocol

- Surface AT MOST 3 candidates per class per session close · don't spam.
- Each candidate = 1 line hook + route to decision.
- Default answer space: `yes / no / later`. Never open-ended.
- On refusal or defer → log in `todos.md` with rationale so pattern doesn't disappear.
- On acceptance → trigger `build-agent` (for skills), direct write via canonical channel (for docs/SOPs), or `promote-learning` primitive (for conventions).

---

## Hard Rules

- **Dedup before appending** · before adding a new learning to learnings.json, scan existing `entries[].fact` for semantic overlap (same platform + same behavior described). If match found → skip, do not add duplicate. If similar but different nuance → add with a `see_also: ["LRN-XX"]` pointer. Never create two entries saying the same thing.
- **Never delete learnings or decisions** · only archive (mark status: "superseded" for learnings, prepend [RESOLVED] for threads)
- **Always scan full conversation** · don't just look at recent messages
- **Classify semantically, not syntactically** · user may not say "this is a learning" explicitly. You infer.
- **Respect _field_types** · never inject strategy into brand.json context fields
- **Route via ingest-resource for shared resource changes** · maintain integrity
- **Direct write only for session-state.md updates** · those are append-only logs
- **Novice education once per brand** · suppress on repeat calls
- **Always show what was learned** · summary is mandatory, not optional
- **If conflict detected** (two opposing facts/decisions), surface to user: "Decision X contradicts Y. Which version is correct?" · wait for clarification before writing
- **Log runtime patterns observed during the session** · beyond business facts, capture *agent-side frictions* (recurring tool errors, schema enum rejections, hook refusals self-corrected, doctrine drift detected) as `category: "system_friction"` learnings when ≥2 occurrences in the session. Example: enum classifier `--source system` rejected 2× → log as `LRN-{n} category:system_friction fact:"agent attempted --source=system, classifier strict on agent/import/inference/operator/scrape, self-corrected to agent. If pattern persists across sessions, propose enum extension."`. These learnings feed system-wide doctrine maintenance, not brand-specific copy. Persisted at workspace-level if cross-brand pattern, brand-level if brand-specific.
- **Append session journal entry to `operator/session-state.md`** when session produced significant artifacts (any `produced/*` file written, ≥2 learnings persisted, or operator confirmed strategic decision). Format: `## YYYY-MM-DD · {brand_slug or "cross-brand"}` heading + 3 sentences max · what was the session goal, what was produced, what's the next thread to pick up. Append-only, never edit prior entries. This is the *operator's navigation across sessions* · different from learnings (facts) and decisions (locked choices).
