---
name: setup-brand
type: orchestrator
version: "2.3.0"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
reasoning_pattern: null
description: >
  Guided setup of a new brand in the workspace. Copies _TEMPLATE, sets slug,
  replaces placeholders, creates product and audience folders, initializes status.json.
  FR: "configure cette brand" "setup brand" "nouvelle brand" "ajoute une brand" "crée le workspace pour" "initialise une brand".
  EN: "setup brand" "configure brand" "new brand" "create brand workspace" "initialize brand".
permissions:
  reads: [brand]
  writes: [brand, product, profile]
  mode: direct
  subagent_safe: false
consumes:
  - path: docs/system/scope-extension-doctrine.md
pipeline:
  preconditions: workspace-template deployed and accessible
  postconditions: run ingest-resource to populate brand context
disambiguates_against:
  onboard-brand: "route to onboard-brand when operator wants the full 4-step pipeline (setup + URL scan + ingest + validate) end to end"
  snapshot-brand: "route to snapshot-brand when operator provides a URL and wants product/brand data auto-scraped (not a guided manual setup)"
---

# Skill: Setup Brand

Interactive guide to configure a new brand in the workspace.
Zero manual copy-paste. The agent creates the full structure and guides the operator.

## Engagement disclosure pré-runtime · canon v2.79.3

Avant de lancer le setup, expose ce disclosure à l'opérateur (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.3) ·

```
Setup brand · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Capture brand info (nom · langue · sector · produits · audiences)
  2. Atelier identité brand (archetype · purpose · valeurs · founder story)
  3. Phrase d'ancrage brand (origin story · 1 phrase)
  4. Synthèse demo-value + close Build chantiers
  5. Tour workspace (env brand · capacités · outils)

  ETA           ~8-15 min (selon densité réponses + atelier identité)
  Implication   tu réponds aux questions séquentielles (1 par tour) · valides recaps
  Livrable      brand workspace initialisée + identité encodée + chantiers prêts pour daily use

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite avant de lancer. Court-circuit autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set ou si opérateur a flag `--no-disclosure` explicit. Sinon · disclosure obligatoire canon v2.79.3.

Cross-ref doctrine racine `docs/system/engagement-disclosure-doctrine.md` v2.79.3.

---

## Tone

Talk like a colleague helping with setup. Simple, concrete, zero technical jargon. The operator never sees paths, JSON, or slugs. They see clear questions and plain-language confirmations.

## Suggestions during onboarding · guide-rail regime

Throughout the setup-brand flow, action suggestions follow a restricted regime (override of the daily-use rules in workspace CLAUDE.md):

- **1-2 max.** Never 3 or 4. The operator follows a flow, doesn't navigate a menu.
- **Always oriented to the next step of the current flow.** No lateral pivot ("by the way, want to ingest a brief?"), no broadening ("want to configure X too?"). Only: the expected next step plus optionally a relevant binary choice.
- **Minimalist format.** Often zero explicit suggestion, just the next question. The flow structure provides the guidance.
- **Exception**: at the very end of setup (after Step 5 workspace tour), open to 2-3 normal daily-use options (ingest, validate, learn, another brand).

General rule: in onboarding, less is more. Every additional suggestion invites the operator out of the flow and away from finishing setup.

## Question rule · 1 per turn, never 2

**Non-negotiable hard rule**: ask ONE question per agent message. Never two, even if both seem useful. Reason: stacking two questions turns the conversation into a form and breaks the *"not a questionnaire"* promise.

- If two infos are needed → pick the most structuring, the other will come naturally next turn.
- If the operator gives two infos in their answer → acknowledge both, then continue normally.
- Explicit acknowledge before each new question: rephrase what they just said in strategic language (not system), e.g. *"Noted. Clear target, hero product placed. [one question]"*. Shows it was read, not just recorded.

## Fast-path · zero questions if info already given

**Hard rule**: before asking a Step 1 question, scan the first operator message and previous answers. For each piece of info already given or inferable, **skip the corresponding question**:

- **Brand name**: if already mentioned in previous turns → slug generated silently, no question.
- **Language**: if operator types in FR → default `fr`, no "fr or en?" question. If in EN → default `en`. Ask only if ambiguous (dense franglais or message too short for reliable detection).
- **Sector**: if inferable from the product mentioned (*"niacinamide serum"* → skincare, *"melatonin gummies"* → sleep nutrition, *"steering wheel grip"* → auto/accessories) → infer silently, propose in acknowledge *"sector I'll set to 'skincare', tell me if it's something else"*. No open question.
- **Products**: if already declared in previous turns → slug generated, skip the question. If not mentioned → ask the question once.
- **Audience**: if already described → OK. If the operator hesitates ("I have a mix", "not sure") → DO NOT passively file it as "to dig later". Ask ONE adversarial question that crystallizes the choice instead of deferring it. Match the framing to the operator's stage : if traffic exists, *"Your last 10 orders, more like which of the two?"*. If pre-launch or pre-traction (no orders yet), *"Among the two, which one do you see as your ideal first customer?"*. Never ask a question that assumes traffic when there is none.

Binary rule: **if info known → zero question on that info**. An operator who gave 4 infos in 1 turn does not start over with 4 sequential questions.

### What fast-path NEVER skips

Two mandatory elements even when all Step 1 questions have been skipped:

**(a) The Step 1 recap in visible block format.**
Even in fast-path. Displayed before launching Step 2. Format:
```
Brand    : {name}
Language : {language} {if inferred: "(inferred)"}
Sector   : {sector} {if inferred: "(inferred, tell me if it's something else)"}
Products : {product_names} (or "none for now")
Customers: {audience_names} (or "to set later")
```
For the operator (especially Claude Code novices), this block is the visual proof that "it's filed". Without it, the novice doubts that the agent really captured the info.

**(b) The Step 2 "Level 1/2/3" brief · profile-adapted version.**
Posted systematically after the Step 1 recap, regardless of fast-path. It's the operator's mental map: they know where we are and where we're going.

Two versions based on detected signal:

*Standard version* (Solo DTC, Portfolio, Early-founder):
> I work in 3 context levels.
>
> **Level 1, the basics.** What makes you unique, tone, hero product, audience. You're at [current level]. My answers are already calibrated to you.
>
> **Level 2, finer.** Detailed benefits, competitors, offers. For when you want.
>
> **Level 3, piloting.** Numbers, strategy, seasonality. For when you have more hindsight.

*Creator-led compressed version* (if creator-led profile detected):
> What sharpens my answers on you: your audience DMs (I digest them into objections and language), your 5-10 top-performing posts (I spot your voice that works), your past collabs (what converted). Paste in bulk whenever, I file.

The creator-led version avoids the DTC jargon "positioning / competitors / financials" that doesn't resonate for this profile.

---

## Step 0 · Async mode via URL (default if URL available)

**Trigger**: the operator drops a site/store URL (*"https://brand.com"*, *"peaktrek.com"*) in the first message, or picks (a) from the onboarding menu with URL provided.

**Mechanic**:

1. **Acknowledge + announce background**:
   > *OK, [profile]. I'll launch the scan on [URL] in the background. 3-5 min, I'll ping you when ready. In the meantime, do whatever. Ask me questions, test a capability, connect a tool, challenge me.*

2. **Launch `snapshot-brand` as a subagent via Task tool**. The `snapshot-brand` skill runs in parallel, the main agent continues the conversation.

3. **During the wait**. The main agent stays conversational, answers what the operator asks, uses smart suggests a/b/c/d as usual.

4. **When the snapshot-brand returns** (signal from the subagent). The agent comes back **at a natural break**:
   > *[At a natural break] I have your brand pre-filled from the site. [Summary in 2-3 lines of what was found: hero product, visible customers, active offers]. Want to validate together and complete what's missing? 3-5 min.*

5. **If "yes"** → move to Step 2 (review + completion).
**If "later"** → keep as a dormant task in `brands/{slug}/todos.md → ## Onboarding review pending`, recallable on contextual trigger later.

**Async benefits**:
- Zero blocking tunnel for the operator
- Setup progresses even if conversation drifts elsewhere
- WOW moment when the agent returns with brand pre-filled at 60%
- No questionnaire, operator just drops a URL

---

## Step 1 · Synchronous mode (if no URL available)

**Trigger**: the operator doesn't have a URL handy, or their brand doesn't yet have a site, or they explicitly prefer to start without scrape.

### Prelim · Operator profile (capture first, at Step 1 OR inferred from WELCOME close)

**Rule**: the operator profile then picks the Build chantiers close variant (see CLAUDE.md § Build → Execute gates). Capture once, store in `/operator/profile.json → identity.profile`. Persistent cross-sessions, never re-asked.

**If already given** at the WELCOME close (a) → skip the question, just acknowledge (*"Noted, {profile}."*).

**If not given** → ONE question at the start of synchronous Step 1:
> "Are you more solo (one brand of your own), portfolio (several brands of yours), agency (working for clients), creator (monetized audience, selling via your content), early (launching, not live yet), or dropshipper (testing products, no long-term brand attachment)?"

**If profile ambiguous or mixed** (e.g. *"a bit solo a bit agency"*) → ONE targeted sharpening question:
> "What we're configuring here, is it more a brand of your own or a client?"

Decide binary. The operator can come back and change later.

### Sequential questions (wait for each answer)

1. **Brand name**: "What's your brand called?" → generate the slug automatically (`lowercase-with-dashes`, max 20 chars)
2. **Working language**: "Main language: fr or en?" → default `fr`
3. **Sector**: "What sector? (e.g. skincare, nutrition, fashion, home…)" → to orient ingest tags
4. **Product(s) (optional)**: "Do you want to declare your products now or add them as we go?" → If yes: "Give me the names." → generate the slugs. If no: no product folder created (ingest creates them on the fly). **If skipped** → write to `brands/{slug}/todos.md → ## In Progress`:
   ```
   - [ ] Add hero product | P: 0 | E: low | T: 10min | Blocks Level 1
     → "Ingest this product info for {brand}: name, price, target, problem it solves."
   ```
5. **Audience (optional)**: "Do you want to describe your audience now or later? If you have several distinct segments, we can set them one by one." → If yes: "Describe each segment in one line." → generate the slugs. If no: no audience folder created (ingest creates them on the fly). **Write to `brands/{slug}/todos.md → ## In Progress`**:
   ```
   - [ ] Create audience profile | P: 0 | E: low | T: 15min | Blocks Level 1
     → "Ingest this customer profile for {brand}: who they are, main problem, what's holding them back from buying."
   ```

Show a recap before continuing:
```
Brand    : {name}
Language : {language}
Sector   : {sector}
Products : {product_names} (or "none for now")
Customers: {audience_names} (or "none for now")

Creating the structure. Continue?
```

Wait for confirmation.

---

## Step 2 · Onboarding brief

> Goal: set the mental map of how we'll enrich the brand, without falling into a form. Conversational, not bullets to fill.

After confirmation of space creation, talk to the operator in plain language:

> OK, {name}'s space is ready. To become really useful, I'll enrich 3 layers along the way. Nothing to fill now. Just the frame.
>
> **The foundation.** Who the brand is, the hero product, who it speaks to. What makes my answers stop being generic and start resembling you. We start there.
>
> **The sharpening.** Detailed benefits, competitors, active offers, differentiation. What makes the content I produce actually targeted. We get there when you want, not urgent.
>
> **The piloting.** Numbers, goals, seasonality. What enables informed strategic decisions. Useful once you're running.
>
> In practice, you talk freely, I file. Loose text, site link, copy-paste of an existing doc, pre-written brief, transcribed voice, anything passes. I structure. You validate or correct.
>
> And no pressure on the timing. Nothing here is one-shot. You can stop mid-setup and pick up tomorrow, next week, whenever. Everything you've told me stays. You don't re-brief.

Rule: never present this as a bulleted list to fill. No "• Paste your positioning". No ASCII frame. Conversational, chairman posture.

---

## Step 3 · Brand anchoring

Ask one last interactive question:

```
One last thing. Tell me a sentence about {name} you haven't said yet.
Anything: a conviction, a phrase you repeat internally,
what you'd tell a friend to describe the brand.
```

When the operator replies, **run** (Bash, not pseudo-code):

```bash
python3 .skills/write-to-context.py \
  --path "brands/{slug}/brand.json#/origin_story" \
  --value '"{operator's exact sentence, JSON-escaped}"' \
  --source operator \
  --confidence 1.0 \
  --mode direct \
  --reason "Step 3 brand anchoring, operator's own sentence"
```

The script is the ONLY sanctioned channel for writes under `brands/` and `operator/`. Edit, Write, `python -c json.dump`, `echo >`, `sed -i`, `tee` all bypass the mutation gate and are blocked.

Confirm:
```
✓ Got it.

From now on: tell me what you know, I structure.
You don't need to open a file, that's my job.
```

**Why this step**: concretely shows the loop "you talk → I write → the brand enriches". The operator sees the loop working before leaving onboarding.

---

## Step 4 · Brand identity workshop (then demo-value + Build switch)

> Identity workshop methodical (4a archetype + 4b purpose + 4c values + 4d founder story) precedes demo-value synthesis (4e) and Build chantiers close. Each sub-step is a discrete workshop (1 question per turn), uses AskUserQuestion canon with 3 options shortlisted from Step 1-3 context, writes via `write_to_context` mutation gate. Skip rule : if Step 0 async snapshot-brand already populated the field with confidence ≥ medium and operator confirms, skip the sub-step (acknowledge inline). Otherwise run the workshop.

### Step 4a · Brand archetype (Mark+Pearson canon, primary + optional secondary)

**Goal** : anchor the brand's voice DNA in the 12 canonical archetypes (Mark & Pearson, *The Hero and the Outlaw*). Primary obligatoire, secondary optional (max 1).

**12 archetypes canon** :
- Innocent
- Sage
- Explorer
- Outlaw (Rebelle)
- Magician
- Hero (Heros)
- Lover (Amante)
- Jester
- Everyman (Homme-ordinaire)
- Caregiver
- Ruler
- Creator

**Workshop** :

1. **Shortlist 2-3 candidates** from Step 1-3 brand context (sector + audience + anchoring sentence + scraped tone if Step 0 ran). Read 2-3 matching canon files in `resources/canon/copy/archetypes-voix/{archetype}.json` for `principle` + `when_works`.

2. **AskUserQuestion canon** with 3 options :
   - 2 primary candidates ranked (e.g. *"Sage (autorité tranquille, voix qui éclaire, marche pour skincare/santé/dermo)"* vs *"Caregiver (chaleur, protection, marche pour parents/wellness)"*)
   - 1 "drill canon" option (*"montre-moi les 12 archetypes en bref avant de choisir"*) → if picked, read all 12 canon files briefly and re-ask.

3. **On selection** → run :

   ```bash
   python3 .skills/write-to-context.py \
     --path "brands/{slug}/brand.json#/identity.brand_archetype_primary" \
     --value '"{archetype-id}"' \
     --source operator \
     --confidence 1.0 \
     --mode direct \
     --reason "Step 4a brand archetype primary, operator selected"
   ```

4. **Optional secondary** (only if operator signals mix) :
   - *"Une couleur secondaire qui se mixe avec le primaire ? Optionnel, beaucoup de marques n'ont qu'un seul."*
   - If yes → AskUserQuestion 3 compatible secondary options (from `combines_with.archetypes` in primary canon file). Otherwise skip.
   - Write to `brand.json#/identity.brand_archetype_secondary` via same mutation gate.

**Output fields** :
- `brand.json#/identity.brand_archetype_primary` (mandatory, enum 12 canon ids)
- `brand.json#/identity.brand_archetype_secondary` (optional, enum 12 canon ids, ≠ primary)

### Step 4b · Brand purpose (Simon Sinek's "why")

**Goal** : capture pourquoi la brand existe au-delà du business. 1-2 sentences max. Anti-buzzword filter active.

**Workshop** :

1. **Seed 3 candidates** from Step 1-3 context :
   - **Founder origin** angle (*"Tu as construit ça parce qu'il manquait {gap} pour {who}"*)
   - **Pain addressed** angle (*"Tu existes pour résoudre {specific pain} que le marché traite mal"*)
   - **Category transformation** angle (*"Tu existes pour transformer {category} en {aspiration}"*)
   - + free-text custom option

2. **AskUserQuestion canon** with the 3 seeded angles + free-text.

3. **HR4 buzzword filter applied to operator answer** :
   - Banned terms : `innovation`, `excellence`, `customer-centric`, `passion`, `quality`, `integrity`, `teamwork`, `respect`
   - If detected → push back gently : *"`{term}` est générique, toutes les brands disent ça. Qu'est-ce qui rend ton pourquoi spécifique à {brand} ? Ce que tu dirais à un proche, pas dans un pitch."*
   - Re-ask once. If operator insists, log with `confidence: 0.5` and flag in pending-validations.

4. **Length check** : 1-2 sentences max (HR6). If multi-paragraph → compress : *"Pour le filer, on garde la phrase-clé. Laquelle des deux ?"*.

5. **On final answer** → run :

   ```bash
   python3 .skills/write-to-context.py \
     --path "brands/{slug}/brand.json#/identity.brand_purpose" \
     --value '"{operator's purpose sentence, JSON-escaped}"' \
     --source operator \
     --confidence 1.0 \
     --mode direct \
     --reason "Step 4b brand purpose, operator Sinek why"
   ```

**Output field** : `brand.json#/identity.brand_purpose` (string, 1-2 sentences).

### Step 4c · Brand values (3-5 max, anti-buzzword filter strict)

**Goal** : 3-5 ownable values, specific to the brand, memorable. Not a generic corporate list of 10+ diluted nouns.

**Workshop** :

1. **Seed 5 candidates** from Step 1-3 context + archetype primary (Step 4a) + purpose (Step 4b). Pull `principle` + `when_works` from primary archetype canon file to inform candidates. Bias toward verbs/concrete commitments over abstract nouns.

   Example for a Sage skincare brand : *"Pédagogie radicale", "Sourcer chaque claim", "Zéro buzzword marketing", "Formules qu'on comprend", "Refuser le bullshit category"*.

2. **AskUserQuestion canon** with the 5 seeded values + free-text *"j'en propose d'autres"*.

3. **Operator selects 3-5** (HR5 cap). If operator picks 6+ → push back : *"5 max, sinon ça se dilue. Lesquelles tu retires ?"*. If operator picks 1-2 → push back : *"3 min, sinon ça manque de relief. Ajoute 1-2."*.

4. **HR4 buzzword filter applied** :
   - Banned (auto-reject) : `innovation`, `excellence`, `quality`, `customer-centric`, `passion`, `integrity`, `teamwork`, `respect`, `sustainability` (alone, without specificity)
   - If detected → push back : *"`{term}` est générique, ça ne te distingue pas. Reformule en spécifique. Exemple Patagonia : pas `sustainability`, mais `Build the best product, cause no unnecessary harm`."*

5. **Acceptable shape check** :
   - Specific (cites concrete commitment, not abstract noun)
   - Ownable (your brand could die on this hill)
   - Memorable (operator could repeat it in 6 months without re-reading)

6. **On final answer** → run :

   ```bash
   python3 .skills/write-to-context.py \
     --path "brands/{slug}/brand.json#/identity.brand_values" \
     --value '["{value1}", "{value2}", "{value3}"]' \
     --source operator \
     --confidence 1.0 \
     --mode direct \
     --reason "Step 4c brand values, operator selected 3-5 anti-buzzword"
   ```

**Output field** : `brand.json#/identity.brand_values` (array, 3-5 entries).

### Step 4d · Brand story (founder origin, 1 paragraph)

**Goal** : capture l'histoire fondatrice spécifique, 1 paragraph 100-200 words. Pattern qui rend tangible le `brand_purpose` (Step 4b). Évite le corporate generic.

**Workshop** :

1. **AskUserQuestion canon** with 3 framings :
   - *"Pain perso qui a déclenché la création (ce que tu vivais avant de construire ça)"*
   - *"Credentials fondateur (parcours expert qui légitime ton positionnement)"*
   - *"Moment de bascule (l'évènement précis qui a forcé la création)"*
   - + free-text *"j'ai une autre angle"*

2. **Operator répond** en prose libre, 1 paragraph 100-200 words.

3. **HR7 anti-pattern filter** :
   - Banned openings (auto-reject) : *"We were frustrated by..."*, *"We saw an opportunity in..."*, *"Our journey began when..."*, *"After years of..."*
   - If detected → push back : *"`{opening}` est générique, 90% des brands ouvrent comme ça. Sois spécifique : nom propre, lieu, chiffre, sensation physique. Exemple : pas `we saw an opportunity in skincare`, mais `Marie passait 3 mois par an à doser ses sérums pour 2 enfants, on a fait l'ingrédient unique qui marche pour les deux`."*

4. **Length check** : 1 paragraph 100-200 words. If multi-paragraph → compress. If 1 sentence → re-ask : *"Donne-moi le moment précis, pas la version corporate"*.

5. **On final answer** → run :

   ```bash
   python3 .skills/write-to-context.py \
     --path "brands/{slug}/brand.json#/identity.brand_story" \
     --value '"{operator's founder story, JSON-escaped}"' \
     --source operator \
     --confidence 1.0 \
     --mode direct \
     --reason "Step 4d brand story, operator founder origin paragraph"
   ```

**Output field** : `brand.json#/identity.brand_story` (string, 1 paragraph).

### Step 4 identity workshop · close transition

Once 4a + 4b + 4c + 4d complete, acknowledge in plain language and bridge to demo-value :

> *OK. Voix d'archétype {primary}{ + secondary if any}, pourquoi {brand_purpose 1-liner}, {N} valeurs ancrées, histoire {founder_story 1-line summary}. C'est ton ADN encodé. On enchaîne avec ce que je lis du reste de ton contexte pour fermer le setup.*

Then proceed to Step 4e (demo-value context synthesis below).

### Step 4e · Demo-value then Build switch (legacy Step 4)

> Contextual application of the **Build → Execute gates** rule (source of truth: `CLAUDE.md § Build → Execute gates`). Do not redocument the 4 mechanics here.

### What we specifically do here (post-scrape / post-setup)

1. **Context synthesis** (operator language, **4-6 sentences of prose, no block format, no enumeration, no field list**). Use the schemas filled by snapshot-brand as analytical vocabulary: name what this brand really is in market terms, who buys and why with the trigger and sophistication signal, what the offer architecture suggests about positioning, and the 1-2 things you noticed the operator likely did not (gaps between brand-stated and observation-based fields, surprises). Flag inferred fields inline with *"(à valider)"* / *"(to validate)"* tags, never as a separate "missing fields" list.

   **Stade de marque (C3 · D#506, silencieux, pas une question).** Inférer `brand.meta.stage` depuis les signaux scrapés, JAMAIS le demander : pas de preuve client / pas d'historique / une seule offre simple → `launch` · traction visible (avis, total_customers, ancienneté) + gamme qui s'étoffe → `growth` · volume de preuve élevé + catalogue large + positionnement installé → `scale`/`mature`. C'est une déduction, donc écrire en `--source agent --confidence 0.6 --mode proposed` et flag `(à valider)` inline + `pending-validations.md`. Si l'opérateur a donné un signal explicite de stade au Step 1 (« je lance », « on fait déjà X par mois ») → `--source operator --confidence 1.0`, pas d'inférence. Ce stade pilote ensuite le curseur explore/exploit du Spectre (build-atlas Step 2.5) · un fallback `brand_equity_level` + richesse atlas existe si le champ reste vide, donc l'inférence est un confort, pas un bloquant.

   Run BEFORE sending:

   ```bash
   python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
   ```

   Mechanical Python primitive · exit code 2 = blocking issue, revise the synthesis. Exit 0 with warnings = log silently, ship. Non-negotiable.

2. **Explicit blind spots** · detailed audience, past learnings, platform access, competitor benchmarks.

3. **Close in 3 Build chantiers** (never audit/brief/diag menu):

> Context is set to ~60%. Before we ship a deliverable, 3 chantiers to arbitrate:
> **(a)** Validate the inferred (customer, positioning). 15 min, becomes source of truth.
> **(b)** Set up platform access ({those mentioned}). Documented once, reusable.
> **(c)** Surface past learnings ({client if agency, personal otherwise}).
> **(d)** Other. Tell me.

4. **Create `brands/{slug}/pending-validations.md`** (from template) with detected items:
   - `[ ]` Review inferred audience
   - `[ ]` Set up access to {each platform mentioned without token}
   - `[ ]` Surface past learnings

These items feed smart suggests (b)/(d) on subsequent turns until ticked (see CLAUDE.md § Build → Execute gates (Gate 4: Ambient todo)).

### Good Step 4 vs Bad Step 4

Good. Operator thinks "he got what I do" AND "he's not firing blind". Chantiers anchored in the specific brand. Inferences signaled. Buffer set.

Bad. Delivering a Meta audit without access. Proposing "3-angle creative brief" without validated audience. Deliverables menu (a audit / b brief / c diag) = premature Execute switch.

---

## Execution · Create the structure (silent)

*The agent executes these steps without exposing them to the operator. No path, no filename in the conversation.*

### E1 · Create the brand structure

1. Copy `brands/_TEMPLATE/` to `brands/{slug}/`
2. Replace `{brand-name}` placeholder with the real brand name in **every** markdown file at brand root: `CLAUDE.md`, `session-state.md`, `pending-validations.md`, `todos.md`. Missing any of these is a bug (the operator will see `{brand-name}` in their own workspace). Data Access fields in CLAUDE.md stay `[TO FILL]` (those are filled in E2).
3. Update `brands/{slug}/status.json`: `brand_slug` → slug, `last_session` → today
4. Update `brands/{slug}/config.json`: `language` → chosen language
5. **Seed `brands/{slug}/pending-validations.md`** with the baseline items under the three gate sections (append after the `<!-- Examples: -->` block of each section, do not remove the comments, they stay as reference):
   - Under **Context gate**: `- [ ] Review inferred audience (segment, pains, objections)` + one line per field stamped in `mode=proposed` by snapshot-brand (positioning, tone, audience). Source tag embedded as plain-language `(inferred from site)` / `(stated by operator)`. Never expose `source` / `confidence` / `mode` keywords.
   - Under **Access gate**: one line per platform mentioned by the operator without a token (e.g. `- [ ] Set up Meta Ads access`).
   - Under **Enrichment**: `- [ ] Surface past learnings (client history, past tests, platform rules learned)`.

### E2 · Configure ecosystem and access

Ask:
> "Which platforms do you use for {name}? (Meta Ads, Shopify, Google Ads, GA4, Klaviyo…)"

For each confirmed platform, collect in two stages:

**1. Public identifiers** (go into the brand's CLAUDE.md, Ecosystem section):

| Platform | Question | Expected format |
|---|---|---|
| Meta Ads | "Your Meta Ad Account ID?" | `act_XXXXXXXXX` |
| Meta BM | "Your Business Manager ID?" | numeric |
| Shopify | "Your Shopify domain?" | `{slug}.myshopify.com` |
| Google Ads | "Your Google Ads Customer ID?" | `XXX-XXX-XXXX` |
| GA4 | "Your GA4 Property ID?" | `G-XXXXXXXXXX` |

→ Update the Ecosystem table in `brands/{slug}/CLAUDE.md` with the identifiers + Status "active".

**2. Tokens / secrets** (go into credentials.env, gitignored):

| Platform | Question | Expected format |
|---|---|---|
| Shopify token | "Your Shopify API token?" | `shpat_...` |
| Klaviyo | "Your Klaviyo API Key?" | `pk_...` |

→ Write to `brands/{slug}/credentials.env`. Only ask for tokens if the operator has them at hand. No blocking if absent.

Signal:
```
Your identifiers are saved. Sensitive tokens are stored locally and won't sync to Git.
When you talk to me about your Meta campaigns or Shopify sales, I'll know where to look.
```

**3. Routing table + Convention files** (automatic, silent):

For each confirmed platform:
- Add a line to the **routing table** in workspace root CLAUDE.md (section `## Routing · Platform conventions`):
  ```
  | {category} | {platform} | `resources/conventions/{platform-slug}.json` |
  ```
  Categories: `paid_media` (Meta, Google, TikTok), `cms` (Shopify), `analytics` (GA4), `workspace` (Slack, ClickUp), `crm` (Klaviyo)

- If the convention file doesn't exist yet → create it from `resources/conventions/_TEMPLATE.json` with:
  - `meta.platform` → platform name
  - `meta.category` → category
  - `access.credential_keys` → the matching keys from credentials.env
  - `access.credentials_location` → "brand" for paid/cms, "shared" for workspace tools
  - Rest stays empty, enriched by learn-from-session over sessions

- If the convention file already exists (platform already configured for another brand) → don't recreate, just add the routing line if absent.

**If no platforms** → "OK. You can add them later. Say 'configure access for {name}' when ready."

### E3 · Create product and audience folders

For each declared product: create `brands/{slug}/products/{product_slug}/`, copy spec.json and offers.json from `_TEMPLATE/products/_example/`, update `meta.slug`.

For each declared audience: create `brands/{slug}/audiences/{audience_slug}/`, copy profile.json from `_TEMPLATE/audiences/_example/`, update `meta.slug`.

### E4 · Initialize CHANGELOG

Add entry to `CHANGELOG.md`:
```
## {date} · Setup Brand

**Brand**: {name} (slug: {slug})
**Action**: CREATED brand structure
**Files**: brand structure initialized, {N} products, {N} audiences
**Next**: ingest-resource to populate brand context
```

---

## Step 5 · Workspace tour (automatic after demo-value)

**Trigger**: right after Step 4 (demo-value + Build chantiers set), when the operator has seen the richness of the inferred context and the upcoming chantiers. At that point they've seen value, they're receptive to an environment map.

**Mix mode (a) automatic + (b) skip option**:

Flow naturally after the deliverable with a subtle exit line:

> *Before we stop, a quick tour of what's around {brand_name} in your folder. 90 seconds max, in case you wonder what's there. If you want to skip, say **skip**.*

If the operator says skip → jump straight to end-of-session recap. Don't push.

Otherwise, deliver the tour in **4 short sub-parts** (not a monolithic block):

### Tour (a) · Your brand data

> *What we just set for {brand_name} is the base. Over time, 6 types of stuff fill around it. Your brand (identity, what makes you unique, tone, already started), your products (specs, mechanism, benefits), your offers (prices, bundles, landing), your audience (segments, objections, language), your learnings (workarounds, platform rules, patterns that work), and your strategy (goals, quarterly focus). You don't fill anything by hand, you talk to me, I file.*

### Tour (b) · Your shared resources

> *On top, you have a cross-brand library. Copywriting frameworks, tested angles, platform rules, Meta/Shopify conventions you accumulate. Fills automatically when I detect that a learning from one brand works for the others.*

### Tour (c) · The skills at your disposal

> *What you can ask me anytime:*
> - *A creative brief, a copy angle, a platform setup audit. Your production capabilities.*
> - *A product scan from a URL. I read, I file.*
> - *A comparison between brands. Compare, aggregate, filter.*
> - *An environment audit. Consistency check, gaps to fill.*
>
> *And if you need a capability that doesn't exist, I can build it custom. You describe what you want, I build the assistant.*

### Tour (d) · Your external tools

> *Your platforms (Meta, Shopify, Klaviyo, GA, Notion, calendar…) connect on the fly. No continuous sync, on demand. When you ask me for a Meta report or a Shopify audit, I ask for your access once, you hand it, I file it locally, next time I'm operational direct. Each platform has its rules file noting how we use it. Reusable across all your brands, shareable if you work in a team.*

### Tour close

> *Want to test one now (a skill, a tool connection), or stop here and come back when you have a real case?*

Strict rules of the tour:
- **≤ 90 seconds total reading** for the 4 sub-parts
- **Adapt to profile**: if operator is agency, push more on multi-brand and shared resources. If creator-led, push on production capabilities and DMs ingestion.
- **If operator cuts** in the middle (*"OK stop that's fine"*) → stop immediately, clean close.
- **Zero jargon**: no `build-agent` mention as a skill name, say *"I can build you a custom assistant"*. Same for other capabilities.

---

## Hard Rules

### Opportunistic sharpening question rule

During the setup flow (Step 1 and on), the "1 question per turn" rule applies to the **structural main thread**. But when the operator gives a **dense signal** in their answer, you can add **ONE targeted sharpening question** on top.

Examples at E1 / Step 1:
- Operator: *"I'm a growth ecom freelancer, I run my stores and clients"*
  → Thread: *"do we start on one of your stores or a client?"*
  → Possible sharpening (ONE only): *"By the way, your personal stores, more like quick DS tests or brands you build long-term? Changes how I help you."*
- Operator: *"I have 3 brands running, the most mature does 8M revenue"*
  → Thread: *"do we start with the most mature to have the most material?"*
  → Sharpening: *"The other 2, same vertical or diversified?"* (clarifies portfolio topology)

**Strict sharpening rules:**
- One sharpening question per turn max, never 2.
- If the operator answered the thread + sharpening last turn → next turn = pure thread only (no spiral).
- Sharpening must **personalize the context**, not extend the scope. If the sharpening leaves the current setup loop, it's parasitic.

---

## Hard Rules (others)

- **Always ask confirmation** before creating files (Step 1 recap)
- **Never overwrite** an existing brand folder, check first
- **Brand.json identity fields filled by Step 3 + Step 4 only** (origin_story via Step 3, brand_archetype_primary + brand_archetype_secondary + brand_purpose + brand_values + brand_story via Step 4a-d). Rest of brand.json filled by ingest-resource via subsequent enrichment loops.
- **Always auto-generate slugs**. Don't ask the operator for the slug.
- **If slug conflict** → flag and propose an alternative slug
- **Never expose file paths, JSON names, or technical terms** in operator messages

### HR4 · Anti-buzzword filter (brand purpose + values)

Applies to Step 4b and Step 4c. Auto-reject any operator answer containing these generic terms (zero-differentiation across brands) :

- `innovation`, `innovative`
- `excellence`
- `customer-centric`, `customer first`
- `passion`, `passionate`
- `quality`
- `integrity`
- `teamwork`
- `respect`
- `sustainability` (alone, without specific commitment)

On detection, push back once with a specific counter-example (e.g. Patagonia's *"Build the best product, cause no unnecessary harm"* vs generic *"sustainability"*). If operator insists after push-back, log with `confidence: 0.5` and flag in `pending-validations.md`.

### HR5 · Max 5 brand values

Step 4c output array is capped at 3-5 entries. Operator picks 6+ → push back compress. Operator picks 1-2 → push back expand to 3 minimum. Rationale : 10+ values dilute, operator cannot remember them, generic corporate list pattern.

### HR6 · Brand purpose 1-2 sentences max

Step 4b output is capped at 1-2 sentences. Multi-paragraph corporate "About us" prose is anti-pattern. If operator provides multi-paragraph → compress : *"Pour le filer, on garde la phrase-clé."*. Rationale : the purpose must fit in operator's head, deployable in 10 seconds of conversation.

### HR7 · Brand story 1 paragraph, specific not generic

Step 4d output is 1 paragraph, 100-200 words. Banned openings auto-rejected :
- *"We were frustrated by..."*
- *"We saw an opportunity in..."*
- *"Our journey began when..."*
- *"After years of..."*

Push back demands specific anchors : proper noun, place, number, physical sensation. Rationale : 90% of brand stories open with these generic phrases, zero differentiation, zero memorability.

### HR8 · Brand archetype primary obligatoire, secondary optional

Step 4a output is :
- `brand_archetype_primary` : mandatory, enum of 12 canonical Mark+Pearson archetypes (Innocent, Sage, Explorer, Outlaw/Rebelle, Magician, Hero/Heros, Lover/Amante, Jester, Everyman/Homme-ordinaire, Caregiver, Ruler, Creator)
- `brand_archetype_secondary` : optional, max 1, must differ from primary

Canon files live in `resources/canon/copy/archetypes-voix/{archetype}.json`. Each file ships `principle`, `structure`, `gabarits`, `when_works`, `when_avoid`, `combines_with`. Step 4a reads candidates from these files to seed the AskUserQuestion shortlist.

If operator hesitates between 3+ archetypes → run drill canon : read all 12 brief `principle` lines and re-ask. Never accept *"je sais pas, choisis"* (zero ownership). Always extract operator's instinct.

---

## Cross-refs · sister skills Sprint v2.80

The Step 4 identity workshop output (brand_archetype + brand_purpose + brand_values + brand_story) feeds downstream skills :

- **`produce-positioning-canvas`** · consumes `brand_archetype_primary` + `brand_purpose` + `brand_values` to generate positioning canvas (category, frame of reference, point of difference, reason to believe).
- **`define-brand-voice`** · consumes `brand_archetype_primary` (+ optional secondary) + `brand_values` to encode voice rules (vocabulary range, register, anti-patterns, gabarits) into `brand.json#/tone_of_voice`.
- **`validate-brand-voice-consistency`** · consumes encoded archetype + voice rules to cross-touchpoint validator (does this copy / ad / email / landing match the encoded archetype + voice?).

Canon references :
- `resources/canon/copy/archetypes-voix/{archetype}.json` · 12 Mark+Pearson archetypes shipped Sprint v2.80 Agent A
- `docs/system/investigation-posture.md` · 5 sections canon (Observé · Déduit · Inconnu · Leviers · Close ouvert) for any strategic synthesis downstream consuming this identity layer
- `resources/schemas/brand.schema.json` · `identity.brand_archetype_primary` + `identity.brand_archetype_secondary` + `identity.brand_purpose` + `identity.brand_values` field definitions
