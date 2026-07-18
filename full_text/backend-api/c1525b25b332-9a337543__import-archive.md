---
name: import-archive
type: orchestrator
operator_facing: true
isolation_scope: brand_only
layer: territoire
version: 1.0.0
recommended_model: sonnet
subagent_safe: false
mode: interactive
description: >
  v1.0.0 (v2.81). Orchestrator skill pour onboarding porte C (import existant)
  bulk · drop dossier vrac mixed-content sans avoir à invoquer chaque skill
  d'import individuellement. Le skill détecte le type de chaque fichier (text
  document · visuel asset · API config · Notion export · transcript · etc) et
  chain le skill spécialisé correspondant en parallèle. Présente synthèse
  point par point à l'opérateur pour validation gate avant downstream
  consumers (build-atlas-complete · produce-paid-angles · etc) ne consomment.
  FR: "importe ce dossier" "ingère cet archive" "drop ce client folder" "j'ai un dossier client" "importe le portfolio brand"
  EN: "import this folder" "ingest archive" "drop this client folder" "import portfolio"
permissions:
  reads: [brand, product, profile, sources]
  writes: [brand, product, profile, learning, sources]
  mode: proposed
  subagent_safe: false
pipeline:
  preconditions: brand_slug_provided OR can_setup_new_brand
  postconditions: validate-resources triggered post-import sur brand affectée
consumes:
  - brands/{slug}/brand.json
  - path: docs/system/entry-arc-doctrine.md
  - path: docs/system/engagement-disclosure-doctrine.md
  - path: docs/system/decomposition-visibility-doctrine.md
  - path: docs/system/territory-doctrine.md
  - path: docs/system/schema-encoding-doctrine.md
  - path: docs/system/onboarding-holistic-doctrine.md
produces_proposals_for:
  - brands/{slug}/brand.json
  - brands/{slug}/products/{slug}/spec.json
  - brands/{slug}/products/{slug}/offers.json
  - brands/{slug}/audiences/{slug}/profile.json
  - brands/{slug}/assets/{type}-{slug}-{date}.{ext}
  - brands/{slug}/learnings.json
  - brands/{slug}/connected-sources.json
disambiguates_against:
  ingest-resource: "ingest-resource ingère 1 fichier text/notes/transcript spécifique. import-archive orchestre N fichiers mixed-content vrac en autonomie."
  import-asset: "import-asset ingère 1 asset visuel spécifique. import-archive route les visuels détectés vers import-asset en parallèle des autres fichiers."
  onboard-brand: "onboard-brand chain setup→snapshot→ingest sur brand nouvelle depuis URL. import-archive ingère matière préexistante vers brand existante OU nouvelle (route setup-brand si nouvelle)."
  sync-notion-atlas: "sync-notion-atlas pull workspace Notion structuré (11 collections canon). import-archive route exports Notion isolés (.md, .csv) vers ingest-resource OR sync-notion-atlas selon structure détectée."
  connect-source: "connect-source connecte une plateforme externe via credentials. import-archive ingère un dossier de fichiers, route les config files détectés vers connect-source si pertinent."
---

# Skill: import-archive

**CRITICAL:** this is an **Orchestrator** porte C onboarding multi-entry. **YOU MUST NEVER** re-implement ingest-resource, import-asset, connect-source, sync-notion-atlas, or setup-brand logic here. **YOU MUST** delegate to each existing skill via Task tool (when the subskill is `subagent_safe: true`) or inline invocation (when `subagent_safe: false`).

> **Drop dossier vrac mixed-content · détection + chain skills spécialisés + synthèse gate opérateur.** v1.0.0 · v2.81 · orchestrator schema-driven · scan → classify → validate gate → chain parallel → synthesis → validate-resources.

L'opérateur a souvent un dossier client centralisé (brief PDF · sheet Klaviyo export · transcripts SAV · figma frames · captures écran · etc). Au lieu d'invoquer chaque skill d'import individuellement, ce skill détecte le type de chaque fichier et route vers le skill spécialisé correspondant en autonomie · présente synthèse à l'opérateur pour validation gate.

---

## Tone

Posture chef de chantier import · pragma + accessible. Pas inspecteur, pas assistant passif. Output opérateur 6-8 lignes max par étape · synthèse par bucket type (text · visuels · APIs · Notion · transcripts), count fichiers, skill destination, plus validation gate explicite avant exécution. Zéro jargon plumbing en surface opérateur · jamais nommer les skills consumers (`ingest-resource`, `import-asset`) en prose opérateur · l'opérateur voit *"J'ai trouvé 12 docs texte · 8 visuels · 1 export Klaviyo · 3 transcripts SAV"* JAMAIS *"je vais invoquer ingest-resource subagent_safe sur 12 fichiers"*.

Si dossier contient un fichier inattendu (corrupted, format inconnu, suspect), surface honnête langage opérateur (*"3 fichiers que je ne reconnais pas · skip ou tu m'expliques ce que c'est ?"*) sans bloquer le batch.

---

## When to invoke

**Triggers FR.** *"importe ce dossier"* · *"ingère cet archive"* · *"drop ce client folder"* · *"j'ai un dossier client"* · *"importe le portfolio brand"* · *"ingère ce dossier vrac"*.

**Triggers EN.** *"import this folder"* · *"ingest archive"* · *"drop this client folder"* · *"import portfolio"* · *"bulk import folder"*.

**Cas typique opérateur** ·
- Cas agency portfolio Abyss · opérateur reprend client existant avec Drive folder centralisé (brief stratégique PDF · creative briefs passés · screenshots ads gagnantes · export reviews Trustpilot · transcript call onboarding) · veut tout ingérer en un coup vers PhantomOS brand pour démarrer atlas
- Cas founder · dossier Google Drive accumulé 2 ans (notes positioning · audience interviews transcripts · screenshots concurrence · brand book figma · export Mailchimp) · veut consolider dans PhantomOS workspace
- Cas creative strategist · brief PDF client + figma frames + sheet Klaviyo flows + captures Instagram ads → batch import pour démarrer creative-brief-composer en aval

**Quand ne PAS invoquer** ·
- 1 fichier seul à ingérer → route direct ingest-resource (cf disambiguates_against)
- 1 asset visuel seul → route direct import-asset
- Workspace Notion structuré 11 collections canon → route direct sync-notion-atlas
- Brand URL e-commerce → route direct snapshot-brand (onboard-brand orchestrator si pipeline complet)

---

## Engagement disclosure pré-runtime · NIVEAU 0 paramètres décomposés (canon v2.79.5+)

Avant de lancer le scan + chain, expose disclosure à l'opérateur en DEUX phases successives (pattern canon `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5).

**Phase A · NIVEAU 0 paramètres décomposés (v2.79.5)** · expose 6 paramètres décomposés que l'orchestrateur va mobiliser. Import-archive opère sur N fichiers mixed-content · disclosure NIVEAU 0 obligatoire AVANT le plan pour que l'opérateur ajuste un paramètre racine (source · type contenu · brand cible · granularité gate) avant que le batch ne route.

```
Paramètres posés · ce sur quoi je pars
─────────────────────────────────────────────────────────────

  1. Source archive
     Path dossier · {/path/to/folder} OR URL Drive/Dropbox · {url}
     POURQUOI cette source · {ex "dossier client agency reprise"
     OR "Drive accumulé 2 ans founder" OR "brief + figma + sheet
     creative strategist"}

  2. Type contenu attendu
     {text/docs (briefs · transcripts · notes) · visuels (ads ·
     packshots · figma frames) · APIs (config files plateformes) ·
     Notion exports (.md, .csv) · mixed (combinaison)}
     POURQUOI · {ex "agency reprise client = mixed par défaut"
     OR "founder Drive = mostly text + screenshots"
     OR "creative strategist = brief PDF + visuels figma"}

  3. Brand cible
     Brand existante (slug · {brand_slug}) OR NEW à setup
     POURQUOI · {ex "brand déjà cartographiée 80% · enrich avec
     archive client" OR "NEW brand reprise · route setup-brand
     d'abord avant ingestion" OR "operator demand explicit"}

  4. Granularité ingestion
     {per-fichier validation gate (opérateur valide chaque
     proposition · safe pour brand mature) OR bulk autonome
     (skill chain en parallèle · gate synthèse finale uniquement ·
     rapide pour archive vrac premier import)}
     POURQUOI ce niveau · {ex "premier import bulk archive ·
     synthèse finale suffit · gain temps" OR "brand mature ·
     per-fichier gate obligatoire · qualité substrate"
     OR "operator demand explicit"}

  5. Hypothèses figées
     · Formats fichiers acceptés · .md, .txt, .pdf, .docx, .csv,
       .xlsx, .json, .png, .jpg, .webp, .svg, .figma export, .mp4,
       .vtt, .srt (transcripts)
     · Ontologie source · matière préexistante opérateur · pas
       scrape externe · pas génération IA
     · Sourcing tag obligatoire · "import bulk · {timestamp}"
       sur chaque fichier ingéré (audit trail downstream)

  6. Biais à éviter
     · Sourcing flou · ingérer fichiers sans tag origine archive
       (canon HR-EAD-8 entry-arc + schema-encoding-discipline)
     · Doublons existants brand · écraser silent fichier déjà
       ingéré OR property déjà encoded canon (canon HR3)
     · Over-ingestion legacy · ingérer 200 screenshots ads 2 ans
       sans filtre stale · saturate substrate downstream

─────────────────────────────────────────────────────────────

  OK avec ces paramètres ? Tu ajustes lequel avant que je passe
  au plan + ETA ?
```

ATTENDS confirmation explicite Phase A avant d'enchaîner Phase B (plan + ETA + implication + livrable v2.79.3). Si opérateur ajuste un paramètre racine (ex "granularité per-fichier" OR "brand NEW à setup"), recalibrer le plan + ETA en conséquence avant Phase B.

**Phase B · disclosure plan + ETA + implication + livrable (v2.79.3 preserved)** ·

```
Import archive · ce qui va se passer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Plan
  ─────────────────────────────────────────────────────────────────────
  1. Scan archive · détection type per-fichier (~1-2 min)
  2. Classification par skill spécialisé (text/visuel/API/Notion/transcript)
  3. Validation gate opérateur pre-execution (synthèse par bucket)
  4. Chain parallèle skills spécialisés (cap 5 parallel par delegation pattern)
  5. Synthèse post-import (résumé ingestion par bucket + sourcing tags)
  6. Trigger validate-resources sur brand affectée (intégrité substrate)

  ETA           ~10-30 min (selon densité archive · cap 50 fichiers par batch)
  Implication   tu valides au gate pre-execution + arbitres doublons + gates skills consumers per-fichier si choisi
  Livrable      brand enrichie matière archive · sourcing audit trail "import bulk · {timestamp}" · validate-resources pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OK pour lancer ? · ou tu préfères attendre / faire autre chose
```

ATTENDS confirmation explicite Phase B avant de lancer Step 1. Court-circuit (Phase A + Phase B) autorisé UNIQUEMENT si `operator/profile.json#preferences.disclosure_preference: silent` set ou si opérateur a flag `--no-disclosure` explicit OR si N usages successifs >= seuil expert (`auto_skip_after_n_calls` true). Sinon · disclosure 2 phases obligatoire canon v2.79.3 + v2.79.5.

Cross-ref doctrines racine `docs/system/engagement-disclosure-doctrine.md` v2.79.5 + `docs/system/decomposition-visibility-doctrine.md` v2.79.5.

---

## Workflow canon · 6 steps

### Step 1 · Scan archive · détection type per-fichier

Scan dossier source (path local OR download URL Drive/Dropbox si applicable). Build inventaire complet · `find {archive_path} -type f` enumérée tous fichiers récursifs.

Per-fichier · détecter type via extension + content sniff ·

| Catégorie | Extensions | Heuristics content sniff | Skill destination |
|---|---|---|---|
| `text_doc` | `.md`, `.txt`, `.pdf`, `.docx`, `.rtf` | First 200 chars lecture · si prose brief/notes/positioning · route ingest-resource | `ingest-resource` |
| `visual_asset` | `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.gif` | Filename heuristics (`logo`, `badge`, `pattern`, `mascotte`) OR ad screenshot detection (1080x1080 / 1080x1350 / 1080x1920) | `import-asset` (logo/badge/mascotte/pattern) OR `craft-packshot` Mode A (carousel scrape adjacent) si packshot detected |
| `api_config` | `.json`, `.env`, `.yml`, `.yaml` | Filename containing `credentials`, `config`, `tokens`, `klaviyo`, `shopify`, `meta`, `ga4` OR content sniff API keys/tokens detected | `connect-source` (route credentials setup) OR `ingest-resource` (route comme learning si pas creds) |
| `notion_export` | `.md` avec front-matter Notion OR `.csv` avec headers Notion DB-style | Heuristics filename pattern `{db_name}-{hash}.csv` OR content `---\n{notion_props}\n---` | `sync-notion-atlas` (route si workspace structuré 11 collections détecté) OR `ingest-resource` (route comme doc isolé sinon) |
| `transcript` | `.vtt`, `.srt`, `.txt` avec timestamps `00:00:00 -->` | Content sniff timestamp pattern OR filename containing `transcript`, `interview`, `call`, `sav` | `ingest-resource` (route comme learning + verbatim_quotes corpus) |
| `data_export` | `.csv`, `.xlsx`, `.tsv` | Filename containing `klaviyo`, `mailchimp`, `meta_export`, `shopify_orders`, `reviews`, `trustpilot` | `ingest-resource` (route comme learning + structured data parse) |
| `figma_export` | `.fig`, `.figma`, `.pdf` export figma | Filename containing `figma`, `frame`, `mockup` OR figma signature | `import-asset` (visual_asset) OR flag inconnu si pas asset-fit |
| `video_audio` | `.mp4`, `.mov`, `.wav`, `.mp3` | Detect par extension | `ingest-resource` (route comme learning · transcript pending) OR flag inconnu si pas transcript-derivable |
| `unknown` | autre | Surface honnête opérateur | Skip OR flag opérateur ("3 fichiers que je ne reconnais pas · skip ou tu m'expliques ?") |

Output Step 1 · `inventory.json` interne avec `[{path, type, destination_skill, confidence, ...}]`.

---

### Step 2 · Classifier par skill spécialisé

Group inventaire Step 1 par skill destination · build `buckets` ·

```json
{
  "buckets": {
    "ingest-resource": [{path, content_type, sub_destination}, ...],
    "import-asset": [{path, asset_type_hint, variant_hint}, ...],
    "connect-source": [{path, platform_hint, credentials_detected}, ...],
    "sync-notion-atlas": [{path, db_hint, structure_detected}, ...],
    "craft-packshot": [{path, mode_a_carousel_scrape_hint}, ...]
  },
  "skipped": [{path, reason}, ...],
  "unknown": [{path, reason}, ...]
}
```

Apply skip rules ·
- Doublons détectés (filename match + content hash match déjà ingéré brand) → flag pour gate Step 3 · propose skip vs override vs versionner
- Stale fichiers (>2 ans timestamp si métadata disponible) → flag pour gate Step 3 · propose skip OR include avec sourcing tag legacy
- Format suspect (corrupted, zero-byte, mime mismatch) → push to `unknown[]` avec reason

---

### Step 3 · Validation gate opérateur pre-execution

**MANDATORY GATE** avant chain skills consumers. Surface synthèse par bucket en langage opérateur, zéro jargon plumbing ·

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Archive scannée · {N_total} fichiers détectés
═══════════════════════════════════════════════════════════════
Source     {archive_path or url}
Timestamp  {YYYY-MM-DD HH:MM}

J'ai trouvé dans ton dossier ·
  · {N_text_doc} document(s) texte (briefs · notes · positioning · transcripts)
  · {N_visual_asset} visuel(s) (ads · packshots · logos · badges · figma frames)
  · {N_api_config} fichier(s) config plateforme (Klaviyo · Shopify · Meta · etc)
  · {N_notion_export} export(s) Notion (DBs · pages)
  · {N_transcript} transcript(s) (interviews · calls · SAV)
  · {N_data_export} export(s) data structurée (reviews · orders · flows)
  · {N_unknown} fichier(s) que je ne reconnais pas (à expliquer ou skip)

Doublons détectés · {N_dup} (déjà dans ta brand)
Fichiers stale · {N_stale} (>2 ans timestamp)

───────────────────────────────────────────────────────────────
À toi de valider avant que je lance
───────────────────────────────────────────────────────────────
(a) Go batch complet · je traite tout en parallèle (cap 5 skills parallel)
(b) Granularité per-fichier · tu valides chaque proposition au fur et à mesure
(c) Skip {bucket X} · ex skip visuels, ne traite que les docs texte
(d) Arbitre doublons d'abord · skip / override / versionner
(e) Annule · je relance avec scope différent
```

ATTENDS opérateur explicit avant Step 4. Si granularité per-fichier choisie → pass flag down to chained skills (gates per-fichier preserved).

---

### Step 4 · Chain parallèle skills spécialisés

Per bucket non-skipped, spawn skill consumer avec Task tool si `subagent_safe: true` · inline si `subagent_safe: false` ·

| Skill consumer | subagent_safe | Mode parallel cap | Notes |
|---|---|---|---|
| `ingest-resource` | true | cap 5 parallel | 1 subagent per fichier text/transcript/data_export |
| `import-asset` | true | cap 5 parallel | 1 subagent per visual_asset avec asset_type_hint pré-rempli |
| `connect-source` | false | inline sequential | guided credentials setup · pas parallelizable |
| `sync-notion-atlas` | false | inline sequential | scaffold/pull workspace Notion · pas parallelizable |
| `craft-packshot` | false | inline sequential si Mode A scrape | route mode A carousel scrape pour images packshot-fit |
| `setup-brand` | false | inline sequential | si brand NEW → route en premier avant tout autre skill |

Pour chaque skill spawn, inject context ·
- `brand_slug` · brand cible (de Phase A NIVEAU 0)
- `sourcing_tag` · `"import bulk · {YYYY-MM-DD HH:MM}"` (HR-IA-1 obligatoire)
- `source_archive_path` · path archive original (audit trail)
- `granularity_mode` · `bulk_autonome` OR `per_fichier_gate` (de Phase A NIVEAU 0)

Operator-facing line une seule fois pour le batch entier ·

> *"Je traite {N_text} documents · {N_visual} visuels · {N_other} autres en parallèle. ~{ETA} min en arrière-plan."*

**NEVER** dump raw subagent output verbatim per delegation pattern §synthesis layer. Synthesize at orchestrator level.

---

### Step 5 · Synthèse post-import · résumé ingestion par bucket

Quand tous skills consumers return, build synthèse opérateur-facing par bucket ·

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Archive ingérée · synthèse
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD HH:MM}

Ingéré ·
  · {N_text_ingested}/{N_text_total} documents texte rangés dans
    ton contexte brand · {1-line synthesis quoi}
  · {N_visual_ingested}/{N_visual_total} visuels rangés dans tes
    assets brand · {1-line synthesis quoi}
  · {N_api_ingested}/{N_api_total} plateformes connectées ·
    {1-line synthesis lesquelles}
  · {N_notion_ingested}/{N_notion_total} pages/DBs Notion sync ·
    {1-line synthesis quoi}
  · {N_transcript_ingested}/{N_transcript_total} transcripts
    ingérés comme corpus voix client

Sourcing audit · tous fichiers taggés `import bulk · {timestamp}`
Doublons gérés · {N_dup_skipped} skipped · {N_dup_overridden} overridden · {N_dup_versioned} versionnés
Échecs · {N_failed} (détail dans pending-validations.md)

───────────────────────────────────────────────────────────────
{1 reco soft offer 1 ligne max contextuel · ex "Si tu veux, on peut
maintenant lancer la cartographie audiences avec cette matière fraîche."}
```

Tous outputs ingérés portent sourcing tag `"import bulk · {YYYY-MM-DD HH:MM}"` injecté par chaque skill consumer (HR-IA-1).

---

### Step 6 · Trigger validate-resources sur brand affectée

Trigger `validate-resources` silently post-import sur brand affectée. Subagent ·
- `model: haiku` (per validate-resources frontmatter, `subagent_safe: true`)
- Input · brand slug
- Expected · integrity report (blocking errors vs flags vs warnings)

**Si blocking errors OR MAJOR flags** ·
> *"Check intégrité brand post-import flagge {N} points · {1-line résumé}. Je les remonte ?"*
→ AskUserQuestion · *"(a) Walk-through guidé fix maintenant · (b) Skip et accept dette technique · (c) Drill sur un point précis"*

**Si only warnings ou MINOR** → log silently dans `pending-validations.md`, surface uniquement si opérateur demande post-close.

Cohérent doctrine root CLAUDE.md ligne 168 *"ALWAYS after any write under brands/{slug}/custom/ or {entity}.extensions.json · trigger validate-resources on that brand silently."* Évite drift schema substrate post-batch.

---

## Hard Rules

| HR | Règle | Type |
|---|---|---|
| HR-IA-1 | Sourcing tag `"import bulk · {YYYY-MM-DD HH:MM}"` obligatoire sur tout fichier ingéré via cet orchestrator · audit trail downstream (cohérent canon onboarding-holistic-discipline + schema-encoding-discipline mutation rule) | BLOCKER |
| HR-IA-2 | Validation gate opérateur pre-execution obligatoire Step 3 · pas autonome silent · l'opérateur arbitre buckets + doublons + granularité avant que skills consumers ne route | BLOCKER |
| HR-IA-3 | Doublons détectés (filename match + content hash match déjà ingéré brand) → propose skip vs override vs versionner · pas écraser silent · canon append-only mutation rule | BLOCKER |
| HR-IA-4 | Per-fichier sourcing source/confidence injecté dans chaque skill consumer · cohérent schema-encoding-discipline mutation rule (`observed`/`stated`/`derived`/`structured` + confidence chain) | CANON |
| HR-IA-5 | Mutation gate strict via `write-to-context.py mode=proposed` (rien direct JSON) · injecté par chaque skill consumer · NEVER bypass | BLOCKER |
| HR-IA-6 | Trigger `validate-resources` post-import obligatoire Step 6 · intégrité substrate brand après batch ingestion | BLOCKER |
| HR-IA-7 | Si brand NEW (pas de `brands/{slug}/brand.json` existant) → route `setup-brand` orchestrator d'abord avant tout ingestion · pas ingérer dans brand inexistante | BLOCKER |
| HR-IA-8 | Disclosure pré-engagement canon NIVEAU 0 paramètres décomposés (Phase A) + plan + ETA + implication + livrable (Phase B) obligatoire cohérent doctrine decomposition-visibility-discipline v2.79.5+ + engagement-disclosure-discipline v2.79.5 | BLOCKER |

---

## Anti-patterns

| AP | Anti-pattern | Pourquoi c'est cassé |
|---|---|---|
| AP-IA-1 | Ingestion bulk sans validation gate Step 3 · skill chain en parallèle silent · opérateur découvre l'état brand post-facto | Substrate qualité cassée · opérateur n'arbitre ni buckets ni doublons ni granularité · canon HR-IA-2 violation |
| AP-IA-2 | Sourcing tag absent sur fichier ingéré · pas de `"import bulk · {timestamp}"` injecté dans skill consumer | Origine fichier perdue · audit trail downstream cassé · canon HR-IA-1 violation |
| AP-IA-3 | Doublons écrasés silent · skill consumer override fichier déjà ingéré brand sans gate opérateur | Canon append-only mutation rule violation · perte historique · canon HR-IA-3 violation |
| AP-IA-4 | Skills consumers invoqués sans disclosure pré-engagement Phase A NIVEAU 0 · opérateur valide à l'aveugle | Canon engagement-disclosure-discipline v2.79.5 violation · opérateur ne sait pas sur quels paramètres orchestrateur opère · canon HR-IA-8 violation |
| AP-IA-5 | validate-resources skipped post-import Step 6 · substrate brand drift potentiel non détecté | Canon mutation rule trigger validate-resources post-write violation · canon HR-IA-6 violation |

---

## Cross-refs · skills consumers chained

- `ingest-resource` v1.1.0 (curator · `subagent_safe: true` · text/docs/notes/transcripts/data_export · canonical destination text)
- `import-asset` v1.2.0 (orchestrator · `subagent_safe: true` · visuels brand · logo/badge/mascotte/pattern/packshot_variant)
- `connect-source` (orchestrator · `subagent_safe: false` · APIs externes via credentials · inline sequential)
- `sync-notion-atlas` v2.0.1 (orchestrator · `subagent_safe: false` · workspace Notion 10 collections territoire · inline sequential)
- `setup-brand` v2.1.1 (orchestrator · `subagent_safe: false` · si brand NEW · route en premier inline sequential)
- `validate-resources` v1.3.0 (curator · `subagent_safe: true` · post-import gate intégrité substrate)
- `craft-packshot` (orchestrator · Mode A carousel scrape pour images packshot-fit · adjacent visual scraping)

---

## Cross-refs · doctrines canon

- `docs/system/entry-arc-doctrine.md` v2.81.0 · porte C parent canon · multi-entry onboarding 4 portes MECE · ce skill est consumer porte C `import existant matière préexistante`
- `docs/system/engagement-disclosure-doctrine.md` v2.79.5 · disclosure pré-engagement NIVEAU 0 + plan/ETA/implication/livrable obligatoire
- `docs/system/decomposition-visibility-doctrine.md` v2.79.5+ · NIVEAU 0 paramètres décomposés pré-exécution canon racine
- `docs/system/territory-doctrine.md` v2.67 · substrate vs production · import-archive alimente substrate · pas production runtime
- `docs/system/schema-encoding-doctrine.md` · mutation rule canon · sourcing tags · `_field_types` (`observed`/`stated`/`derived`/`structured`) · confidence chain
- `docs/system/onboarding-holistic-doctrine.md` v2.79.3 · panorama 360° onboarding agnostique · porte C `import existant` couverte par cet orchestrateur

---

## Edge cases

- **Archive vide.** `find` returns zero files · surface honnête *"dossier vide ou inaccessible · vérifie le path"* · abort.
- **Archive énorme (>500 fichiers).** Surface gate spécifique *"archive contient {N} fichiers · au-delà de 50 par batch je propose batch sliced (50 par batch · ingestion progressive). OK ?"*
- **Brand cible NEW (pas de brand.json).** Route `setup-brand` orchestrator d'abord (inline conversational) · puis re-launch import-archive Step 1 quand brand structure posée.
- **Source archive est URL Drive/Dropbox.** Download local d'abord (`curl -sL` ou Drive API si MCP connecté) · puis scan path local · cleanup post-import.
- **Fichier individuel sans extension.** File magic detection · `file {path}` command · si content type identifié → route bucket correspondant · sinon push `unknown[]`.
- **Mixed-content fichier ambigu** (ex .md avec embedded image base64) · route ingest-resource principal + flag visuel embedded pour split optionnel.
- **Doublon detected mais content différent** (filename match, hash diverge) · gate opérateur explicit *"fichier `{name}` déjà ingéré mais contenu différent · skip / versionner (.v2) / override ?"*
- **Stale fichier mais opérateur insiste.** Override silent flag stale → include avec sourcing tag `"import bulk · {timestamp}" + "legacy_archived: true"`.
- **Unknown bucket count >0.** Surface honnête liste opérateur · *"3 fichiers que je ne reconnais pas · {filename1}, {filename2}, {filename3} · skip ou tu m'expliques ce que c'est ?"*

---

## Operator output template

### Fiche operator-facing canonique post-Step 5 synthèse

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Archive ingérée · synthèse
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD HH:MM} · matière archive rangée dans ta brand, prête pour cartographie + production downstream

Source     {archive_path or url}
Brand      {brand_slug}

Ingéré ·
  · {N_text_ingested} documents texte ({1-line ce qui a été appris})
  · {N_visual_ingested} visuels ({1-line types ajoutés})
  · {N_api_ingested} plateformes connectées ({1-line lesquelles})
  · {N_notion_ingested} pages/DBs Notion sync ({1-line quoi})
  · {N_transcript_ingested} transcripts en corpus voix client

Sourcing   import bulk · {timestamp} (tous fichiers taggés)
Doublons   {N_dup_skipped} skipped · {N_dup_overridden} overridden
Échecs     {N_failed} (détail pending-validations.md)
Intégrité  {validate-resources verdict · ok / N flags MAJOR / etc}

───────────────────────────────────────────────────────────────
{1 reco soft offer 1 ligne max contextuel}
```

**Anti-pattern UX prose opérateur** ·
- JAMAIS nommer les skills consumers (`ingest-resource`, `import-asset`, `connect-source`) en prose opérateur
- JAMAIS exposer plumbing (`subagent_safe`, `Task tool`, `write_to_context mode=proposed`, `confidence_chain`)
- JAMAIS dump raw subagent output verbatim
- TOUJOURS langage opérateur (`tes documents`, `tes assets`, `tes plateformes`, `ton corpus voix client`)
- TOUJOURS 1 reco max post-synthèse, pas menu

**Backstage (sourcing audit trail, NON rendu opérateur)** · chaque entity créée porte `_field_types`, `_source: "import bulk"`, `_source_archive_path`, `_imported_via: "import-archive/1.0.0"`, `_imported_at`. Vivent dans le JSON pour audit + retrieval programmatique · opérateur ne les voit jamais.

---

## Operator cartography (avant Step 1, si complex)

Si archive contient signal multi-bucket dense (text + visuel + APIs + Notion), cartograph en 1 ligne ·

> *"OK, je détecte {N_buckets} types dans ton dossier. Je vais lancer en parallèle, tu vas voir une synthèse par catégorie avant que je traite tout."*

Puis enchaîne disclosure NIVEAU 0 Phase A.

---

## Guardrails

- **NEVER** scan archive sans disclosure Phase A NIVEAU 0 préalable (HR-IA-8)
- **NEVER** chain skills consumers sans validation gate Step 3 opérateur (HR-IA-2)
- **NEVER** écraser doublon silent · gate explicit (HR-IA-3)
- **NEVER** skip sourcing tag injection dans skills consumers (HR-IA-1)
- **NEVER** bypass mutation gate `write-to-context.py mode=proposed` (HR-IA-5)
- **NEVER** skip `validate-resources` post-import (HR-IA-6)
- **NEVER** ingérer dans brand inexistante · route setup-brand d'abord (HR-IA-7)
- **NEVER** dump raw subagent output · synthesize at orchestrator level (delegation pattern §synthesis layer)
- **NEVER** expose Task tool mechanics ou subagent internals à l'opérateur ("I spawned a subagent", "validate-resources ran in a subprocess"). Say what it *does* · "j'ai rangé tes documents", "j'ai connecté Klaviyo"
- **NEVER** re-implement subskill logic. Si subskill a un bug, fix dans subskill · pas dans cet orchestrator
- **ALWAYS** surface blocking integrity errors Step 6 avant close synthèse
- **ALWAYS** persist `brands/{slug}/session-state.md` rolling update post-batch (pour crash resumption)
