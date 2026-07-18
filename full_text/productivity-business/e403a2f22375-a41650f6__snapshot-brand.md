---
name: snapshot-brand
type: producer
version: "1.9.1"
isolation_scope: brand_only
layer: territoire
recommended_model: sonnet
reasoning_pattern: null
operator_facing: true
description: >
  v1.6.0 (v2.91 recon & cadrage) · NEW Step 1.5 recon · photo de devanture plafonnée (4 requêtes / 60s) qui classe l'archétype de cartographie (mono-héros · catalogue resserré · gros catalogue · edge marketplace), dimensionne le scan, et rend un rapport de recon que l'orchestrateur déplie en clair avant le gate "valide le chantier". Résout la contradiction Step 2 onboard-brand (inférence visible = raisonnement SUR le rapport, pas re-dérivation inline). Backward compat strict additif.
  v1.5.1 (v2.81.1 decomposition visibility NIVEAU LIVE) · NEW section Niveau LIVE thinking aloud obligatoire pendant exécution. Action LOURDE · narratif étendu 2 niveaux abstraction (macro contexte boutique + micro produit many-to-many phrasé spec → mécanisme → bénéfice → pain → audience en prose). Pose pair senior expert · audit temps réel + pédagogie indissociables. Cross-ref `decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 + AP-DVD-11. Backward compat strict additif (cycle runtime préservé).
  v1.5.0 (v2.78.2 decomposition visibility) · Phase output NEW section Decomposition Visibility matricielle obligatoire APRÈS 5 sections IP · 4 niveaux canon (décomposition produit specs/mécanismes/bénéfices 3 couches · many-to-many pain × audience matrix · stage business filter · méthode pédagogique verbale). Additif strict · existing Phase output preserved.
  v1.4.0 (v2.68 progressive cartography refactor) · Phase 1 macro confirmation light (3-5 lignes produit+offer+positionning · gate binaire valide/corrige) puis Phase 2 drilling autonome (drill PDP details + reviews verbatims tagged + funnel signals · synthesis 5 sections investigation-posture). Drop 4 closed questions about audience anti-pattern · drill-down autonome reviews + verbatims tagged remplace Q&A audience.
  v1.3.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (breakthrough-advertising-5-stages, audiences-cartography). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.3.0 (v2.58 coverage extend) · 4 sub-steps additifs · brand_equity_level heuristic auto · creative_zone init heuristic · sustainability HTML scraping (eco_claims, certifications, packaging_type) · price_per_unit auto-calc depuis variants. Closes 4 orphans audit v2.57.
  v1.2.0 (v2.57 alignment) · auto-detect business_model heuristique scrape · stage proposal via mutation gate · surface contextuel + AskUserQuestion si ambiguous.
  Automatically fills spec.json, offers.json and the base of profile.json
  from a product URL. Scrapes the page, deploys drill-down autonome reviews + verbatims tagged
  (no operator questionnaire pre-action), computes a completeness score, lists missing fields,
  runs progressive cartography Phase 1 macro confirmation light then Phase 2 drilling autonome.
  Scope: one product per run (spec + offers + profile draft). Does not replace VoC/VoM, it complements them.
  FR: "snapshot", "snapshot ce produit", "remplis le workspace", "onboard ce produit",
  "crée la fiche produit depuis l'URL", "remplit spec.json depuis le site".
  EN: "snapshot", "snapshot this product", "populate workspace from URL", "onboard product".
permissions:
  reads: [brand]
  writes: [product, offer, profile]
  mode: proposed
  subagent_safe: true
consumes:
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
  - path: docs/doctrine/audiences-cartography-doctrine.md
  - path: docs/system/scope-extension-doctrine.md
  - path: docs/system/progressive-cartography-doctrine.md
  - path: docs/system/territory-doctrine.md
  - path: docs/system/contextual-intelligence.md
  - path: docs/system/investigation-posture.md
pipeline:
  preconditions: brands/{slug}/ must exist (run setup-brand if needed)
  postconditions: run validate-resources to check completeness, ingest-resource to enrich
disambiguates_against:
  setup-brand: "route to setup-brand when operator wants manual guided setup without URL scraping"
  onboard-brand: "route to onboard-brand when operator wants the full multi-step pipeline from scratch, not just a URL scrape"
---

## Tone

Present the results as a product summary, not a data dump. "Here's what I found on your product", not "spec.json filled at 73%".
---

## Niveau LIVE · raisonnement thinking aloud pendant exécution (canon v2.81.1+)

Action classée **LOURDE** (cf table calibration `docs/system/decomposition-visibility-doctrine.md` v2.81.1+). NIVEAU LIVE thinking aloud expert OBLIGATOIRE pendant exécution · pas seulement disclosure pré-engagement en amont et Phase Output Decomposition Visibility matricielle (NIVEAUX 1-4) en aval.

Pattern obligatoire · l'agent verbalise son raisonnement EN TEMPS RÉEL pendant qu'il décortique le produit scrapé, en prose narrative sobre (zéro matrice ASCII en LIVE · les matrices viennent en Phase Output Decomposition Visibility post-exec).

**2 niveaux d'abstraction obligatoires** ·

1. **Macro contexte boutique** · verbaliser la compréhension du périmètre AVANT de rentrer dans le détail produit.
   Exemple snapshot-brand · "On part d'une boutique qui s'adresse à des {audience macro depuis brand.json + scrape signaux}, qui propose {N produits détectés via sitemap / collections}, qui fait probablement {volume estimé via reviews count · social proof · pricing range}. Le pattern catalogue semble être {hero / secondaires / entries} parce que {signaux pricing × densité reviews × position homepage}. Le business model est probablement {DTC pure / subscription / hybrid} parce que {signaux scrape · subscription widgets · services pages · marketplace markers}. Le positionnement macro tape sur {axe stade Schwartz inféré · sophistication marché}."

2. **Micro produit many-to-many phrasé** · verbaliser la chaîne produit en prose narrative pendant l'encoding.
   Exemple snapshot-brand · "Ce produit {nom} a {spec composition extraite PDP} comme spec dominante → tel mécanisme {comment ça agit · physiologique ou technique inféré du claim PDP} → tel bénéfice fonctionnel {ce que ça résout extérieurement} + tel bénéfice émotionnel {ce que ça change subjectivement} + tel bénéfice identitaire {ce que ça projette socialement} → tel pain {douleur cible déduite reviews verbatims tagged si Phase 2 lance} → telle audience {sub-cluster product-fit inféré scrape + reviews demographics)."

**Calibration narrative** · prose sobre · registre pair senior expert · zéro jargon plumbing (jamais `spec.json#field_path`, `confidence chain`, `_field_types` en LIVE) · zéro tableau ASCII en LIVE (matrices = Phase Output Decomposition Visibility post-exec). Adapter le tonal au registre opérateur détecté (grounded · standard · dense).

**Audit + pédagogie indissociables** · le thinking aloud sert l'opérateur sur 2 axes en même temps · (a) audit temps réel · il peut corriger si l'agent part dans une mauvaise direction d'inférence (mauvais business model détecté · mauvaise audience inférée · mauvais mécanisme physiologique projeté) AVANT que le scrape consomme tokens supplémentaires Phase 2 drilling, (b) pédagogie · il apprend la posture professionnelle experte en regardant la manière de décortiquer un produit DTC (spec → mécanisme → 3 couches bénéfice → pain → audience).

Cross-ref · `docs/system/decomposition-visibility-doctrine.md` v2.81.1+ HR-DVD-11 (NIVEAU LIVE obligatoire actions lourdes) + AP-DVD-11 (opacité pendant action lourde = bug invalid).

---

# Skill: Snapshot

Fills spec.json + offers.json + base of profile.json from a product URL.
One run = one product. Shopify JSON API prioritized over HTML. Zero hallucination: if a field is not in the page or the operator's answers, it stays `null`.

Relation to other skills:
- **setup-brand** → creates the structure. Snapshot fills it.
- **ingest-resource** → deep enrichment (VoC, arguments, competitors). Snapshot = surface.
- **validate-resources** → to run after, to check quality.

---

## Step 0 · Pre-flight: check workspace state

Before anything, two checks:

**Check 1 · Does the brand exist?**
Check that `brands/{slug}/brand.json` is filled (`identity.name` field non-empty).
- If empty or absent → tell the operator: "The brand isn't configured yet. Run `setup-brand` first, then come back here." Stop.
- If filled → continue.

**Check 2 · Product already snapshotted?**
Check if `brands/{slug}/products/{product_slug}/spec.json` exists and has `meta.slug` filled.
- If yes → flag: "This product already has a sheet. Update it (merge) or start fresh?" Wait for reply. Merge = keep existing non-null fields, overwrite with new scraped values. Fresh = overwrite everything.
- If no → continue.

---

## Step 1 · Product URL

Ask:
> "URL of the product to snapshot?"

**URL type detection before validation:**

| URL type received | Behavior |
|---|---|
| Product URL (`/products/{handle}`, `/p/`, `/shop/product/`) | Go direct → Step 2 |
| Brand or homepage URL (`example-brand.com`, `example-brand.com/`) | Read HTML navigation FIRST (see "Hero detection" below). Only if nav gives no clear signal → try `{base_url}/products.json?limit=50` to list the catalogue. |
| Collection URL (`/collections/{handle}`) | Try `{collection_url}/products.json?limit=50`. List products. Same flow as brand URL. |

**Large catalogue (>1000 SKUs):** `products.json` is paginated 50 max per page; fully enumerating a 1000+ catalogue burns tokens and time. When the catalogue exceeds ~200 products (detected via collection counts in nav, or after first page if `products.json` returns 50 with continuation tokens), do NOT enumerate · sample: read pages 1, 2, and the most recent (sort by `published_at desc`) for hero candidates, surface the volume to the operator (*"this catalogue has 1000+ products, I'm sampling featured + hero, paste a specific URL if you want a different one"*), and let them choose. Snapshot remains one product per run.
| Ambiguous URL (can't type) | Ask: "Is this the URL of a specific product or the brand homepage?" |

One run = one product. If the operator wants several, relaunch the skill for each.

**Hero detection · always before API:**

When the URL is a homepage or brand URL → read the page HTML to detect the product highlighted in the navigation:
- Dedicated tab with visual emphasis (color, position) → strong hero signal
- Product on homepage banner or "featured" → medium signal

⚠️ Some hero products are **not returned by the** Shopify API (`products.json`). The HTML nav is the source of truth for hero, not the API.

**Mandatory confirmation before scraping · stage + ask:**

After detection, stage the proposal BEFORE asking the operator. The stage call records that a confirmation is pending; the next operator turn flows through the `checkpoint-resolver` hook and promotes the checkpoint based on the literal text of their reply.

**Order of operations** (hard rule):

1. Call stage-proposal with the detected product:
   ```bash
   python3 .skills/stage-proposal.py \
     --brand {slug} \
     --checkpoint confirmed_products \
     --product-slug {detected product slug} \
     --summary "Hero detected: {product name} · {url}"
   ```
2. Show the operator:
   ```
   I detected as hero product: {detected product name}
   URL: {product url}

   Is this the product you want to snapshot? Or prefer another one?
   ```
3. **Wait for the operator turn.** The `checkpoint-resolver` hook reads their reply and resolves the pending proposal:
   - `"oui"`, `"yes"`, `"go"`, `"ok"`, `"valide"` etc. → `confirmed_products` gains `{slug}` → Step 2 unlocked.
   - `"non"`, `"no"`, `"pas bon"`, correction like `"non, it's X"` → rejection logged, pending cleared → re-detect, re-stage with the corrected product, re-ask.
   - Free-form correction without confirm/reject marker (`"Glow Boost"`) → no automatic resolution. Clear pending manually by re-staging with the corrected slug (pending existing blocks new stage · surface gracefully to the operator).
4. **Never start scraping until stage-proposal is resolved.** Writing `products/{slug}/spec.json` or `products/{slug}/offers.json` without the slug in `confirmed_products` is blocked by the write-to-context gate.

**Validate the retained product URL:**
- Accessible (HTTP 200) → continue
- HTTP 301/302 → follow redirect, flag: "URL redirects to [new URL]. Is this the right product?"
- HTTP 403/401 or redirect to /login → stop cleanly:
  ```
  Protected page (member access required).
  Options:
  1. Provide a public URL of the product
  2. Paste the page content manually
  3. Use a Shopify API key if you have one
  ```
- HTTP 404 → "URL not found. Check the URL and relaunch."

---

## Step 1.5 · Recon & cadrage du chantier (v1.6.0 NEW)

**Avant de creuser, on dimensionne.** Le scan profond n'est pas le même travail sur un mono-produit en abonnement et sur un catalogue 200 références. La recon est une PHOTO de devanture, pas un second scan · elle classe l'archétype, propose une stratégie de scan dimensionnée, et rend un RAPPORT que l'orchestrateur déplie en clair (l'inférence visible se fait SUR ce rapport, pas en re-dérivant le scan brut).

**L'enjeu d'abord (D#518).** Avant de dimensionner, poser ce que ce scan doit TRANCHER · la décision qui paie, la question de l'opérateur (cf `docs/doctrine/strategic-diagnostic-doctrine.md` · où la marque veut aller, où ça coince). « Pertinent » se mesure contre cet enjeu, jamais contre la couverture du site. Le scan est une **allocation d'effort sous contrainte** (doctrine · `docs/system/scrape-as-allocation.md`), pas un crawl exhaustif · on fetch là où la réduction d'incertitude sur la décision est haute, on s'arrête quand elle tombe.

**Plafond dur · 4 requêtes, 60 secondes.** La recon ne réutilise QUE des lectures déjà mandatées · nav HTML (Step 1 hero detection), `/sitemap.xml` ou `/robots.txt` (HR-v1.4.1-NEW-4), `{base}/products.json?limit=50` (count + continuation token), indices homepage déjà dans le HTML. Elle n'ouvre AUCUNE PDP, ne tague AUCUN review, ne fetch aucune collection entière. Une 5e requête ou un dépassement 60s = elle a glissé dans le deep scan · violation.

**Classification (réutilise le classifieur Step 2bis, en avance de phase).** Calcule `products_detected / subscription_signals / marketplace_signals` sur les signaux légers (cf Step 2bis table de sourcing) et mappe en archétype de cartographie. Ce calcul early sert au CADRAGE uniquement · l'écriture canonique de `brand.json#identity.business_model` reste au Step 2bis post-scrape (ne pas dupliquer le write ici).

| Archétype | Bascule (`products_detected`) | Stratégie de scan (conditionne Steps 2-7) | ETA |
|---|---|---|---|
| **Mono-héros** | ≤ ~8, ou 1 héros nav dominant | scan PROFOND sur le héros · PDP complète + reviews tagged + funnel signals · décompo NIVEAU 1-2 dense post-scan sur 1 produit | 12-18 min |
| **Catalogue resserré** | ~8 à ~40 · collections nav lisibles | héros profond + cartographie de la GAMME en surface (rôles hero/secondaires/entries via pricing × densité reviews) · pas de drill par SKU | 18-25 min |
| **Gros catalogue / Shopping** | > ~40 (plafond canon ~200 = échantillon Step 1) | par COLLECTIONS, zéro énumération · héros demandé à l'opérateur si nav ambiguë | 20-30 min |
| **Edge · marketplace** | `marketplace_signals` truthy | la recon S'ARRÊTE à la photo · pas de héros cohérent à encoder · pose le périmètre en inconnu typé, demande quel vendor/segment encoder | 8-12 min |

**Le rapport de recon (artefact rendu) ·**

```
RECON · {url} · {durée}
  Archétype       · {mono-héros | catalogue-resserré | gros-catalogue | marketplace} (products_detected={N} · subscription={bool} · marketplace={bool})
  Héros candidat  · {nom · url} (source nav HTML)  OU  "ambigu · à confirmer"
  Volume gamme    · {N produits · M collections}
  Plan proposé    · scan {profond héros | gamme surface | échantillon collections}
  Axes joignables · créa ✓ · marché ◐ public · éco ○ branchement · funnel ○ branchement · média ○ compte
  Pré-amorces     · {2 à 4 inconnus typés, hypothèse déjà remplie}
```

**Pré-amorces (les inconnus à fort levier, hypothèse déjà posée · cf Step 7 Leviers).** La recon pré-remplit 2 à 4 questions que seul l'opérateur tranche · vrai héros économique (la structure du site peut mentir sur le produit moteur), vraie raison d'achat (hypothèse sourcée des avis, pas un blanc), gamme ou segment hors-site, contrainte économique ou compliance (marge, abonnement, stock, réglementaire · structurellement invisibles au scan). Jamais un blanc renvoyé · toujours une lecture à confirmer ou corriger (canon open-map · le manque devient une lecture, pas un trou). **Les pré-amorces ne sont pas qu'un appendice du rapport · elles DEVIENNENT le plan du scan profond (D#518)** · chaque pré-amorce nomme le fetch ciblé qui la résoudrait. Le Spectre (carte mécanisme→usage) dirige le fetch vers les zones blanches, il ne le couronne pas à la fin · doctrine `docs/system/scrape-as-allocation.md`.

**Cadrage orchestré vs standalone.** Quand snapshot-brand est piloté par un orchestrateur (onboard-brand / build-atlas-complete) · la recon est rendue D'ABORD et la skill S'ARRÊTE après ce Step 1.5 (return le rapport) · l'orchestrateur la déplie en clair, fait valider le chantier (gate « valide le chantier »), PUIS re-spawn snapshot-brand pour le deep scan (Steps 2-7) dimensionné à l'archétype validé. En standalone (l'opérateur a collé l'URL directement) · la recon enchaîne sur le deep scan avec la stratégie dimensionnée, sans gate intermédiaire (l'URL collée vaut validation du périmètre).

---

## Step 2 · Platform detection + scraping

**Shopify detection** (in this order):
1. URL contains `.myshopify.com` or `/products/` → Shopify likely
2. Try `{base_url}/products/{handle}.js` → if HTTP 200 + valid JSON → **SHOPIFY CONFIRMED**
3. Try `{collection_url}/products.json?limit=50` for the catalogue if needed

**If Shopify confirmed → scrape the Shopify JSON**:
```
GET {base_url}/products/{handle}.js
```
Extract:
- `title` → spec.name
- `body_html` (strip HTML) → spec.description_raw
- `product_type` → spec.category
- `variants[]` → each variant = a candidate offer in offers.json
  - `variant.price` (in cents → divide by 100)
  - `variant.compare_at_price` (crossed price if non null)
  - `variant.title` (e.g. "3 months", "6 bottles")
  - `variant.available`
- `selling_plan_groups[]` → if present: subscription detected, note `subscription_detected: true`
- `tags[]` → note for categorization

**If non-Shopify → HTML scraping**:
Extract from HTML (in this order of priority):
1. `<script type="application/ld+json">` (structured data Product schema) → priority
2. Open Graph tags (`og:title`, `og:description`, `og:price:amount`)
3. `<h1>` → product name
4. Price: patterns `€X`, `$X`, `X.XX €` in the DOM
5. Description: `<meta name="description">` + first visible paragraph

**Product detail page scraping (HTML after API, always):**

Even if Shopify JSON returns the data, read the product page HTML to capture what the API doesn't see (note: this is HTML scraping in complement to the API, not the doctrinal Layer 2 of connected tools):

| Element | HTML location | Target field |
|---|---|---|
| Trust badges / authority claims ("Clinically Tested", "Podiatrist Recommended") | Title zone → ATC | spec.proofs.authority |
| Review count displayed | Reviews widget (Judge.me, Loox, Okendo) | `_snapshot.reviews_displayed` |
| Quantity break selector (1 pair / 2 pairs / 3 pairs…) | Offer section, before ATC | offers.json · type `quantity_break` |
| Urgency / bonus ("OFFER ENDS SOON", "FREE eBook") | ATC zone | offers.json · `urgency`, `bonus_included` |
| Payment methods | Footer or ATC zone | brand.json · market confirmation |

⚠️ **WebFetch limit**: WebFetch returns only static HTML. Front-end apps (quantity breaks, review widgets) are rendered via JavaScript after load, invisible to WebFetch. If these elements are suspected but not visible in HTML → note `[app-rendered · requires Chrome capture]` and continue. Never invent unconfirmed price tiers.

**Conditions d'arrêt du fetch (D#518 · rendement, pas couverture).** Le scan profond n'est pas « tout lire » · c'est lire jusqu'à ce que le rendement tombe. On arrête dès qu'UNE est vraie (doctrine `docs/system/scrape-as-allocation.md`) ·
1. **Confiance-cible atteinte pour l'enjeu** · la décision qui paie est déjà tranchable, une PDP de plus ne la change pas.
2. **Saturation** · les nouvelles lectures répètent les mêmes signaux (mêmes proofs, mêmes objections).
3. **Inconnu non-tranchable-par-scrape** · structurellement invisible au scan (marge, abonnement réel, contrainte compliance) · le TYPER avec son levier (zéro fetch de plus), ne pas s'acharner.
4. **Budget d'attention épuisé** · le plafond dimensionné par l'archétype (Step 1.5) est atteint · le reste part en inconnu typé, pas en sur-crawl.

**Sustainability signals scraping (v1.3.0 NEW · v2.58)**

En complément du scraping PDP standard, scanner additionnellement les signaux sustainability per produit. Ces signaux peuplent `spec.sustainability.*` (sidecar entité product) ·

| Field | Heuristique HTML | Confidence |
|---|---|---|
| `spec.sustainability.eco_claims[]` | Scan mentions textuelles · "bio", "vegan", "cruelty-free", "upcycled", "recyclé", "natural", "organic", "sustainably-sourced", "carbon-neutral", "fairtrade" dans body_html, meta description, tags Shopify, sections produit. | 0.7 si claim explicit dans PDP (mention texte directe), 0.4 si déduit visuellement (badge sans texte associé OU inference depuis catégorie). |
| `spec.sustainability.certifications[]` | Scan badges/logos · "Ecocert", "COSMOS", "USDA Organic", "Fair Trade", "B-Corp", "1% for the planet", "Leaping Bunny". Texte alt-tag images + texte explicite. | 0.7 si certification explicit nommée, 0.4 si badge image sans texte machine-readable. |
| `spec.sustainability.packaging_type` | Enum `[glass · plastic · aluminum · cardboard · biodegradable · refillable · zero-waste]`. Scan mentions packaging dans description, specs, tags. | 0.7 si déclaration explicit, 0.4 si inférée depuis visuel produit ou catégorie. |

Stage per spec produit via mutation gate ·

```bash
python3 .skills/write-to-context.py \
  --path "products/{product_slug}/spec.json#/sustainability/eco_claims" \
  --value '["{claim_1}", "{claim_2}"]' \
  --source agent \
  --confidence {0.7 si explicit, 0.4 si déduit} \
  --mode proposed \
  --reason "HTML scraping eco_claims mentions"

python3 .skills/write-to-context.py \
  --path "products/{product_slug}/spec.json#/sustainability/certifications" \
  --value '["{cert_1}"]' \
  --source agent \
  --confidence {0.7 si explicit, 0.4 si déduit} \
  --mode proposed \
  --reason "HTML scraping certifications badges"

python3 .skills/write-to-context.py \
  --path "products/{product_slug}/spec.json#/sustainability/packaging_type" \
  --value "{enum_value}" \
  --source agent \
  --confidence {0.7 si explicit, 0.4 si déduit} \
  --mode proposed \
  --reason "HTML scraping packaging mentions"
```

Si zéro signal sustainability détecté → ne pas stage (laisser fields null, ne pas créer de bruit `proposed` vide).

**Review triangulation · 3 sources, always note provenance:**

| Source | How to get it | What it measures |
|---|---|---|
| Native Shopify | `products/{handle}.js` metafields | Reviews on this specific product |
| Onsite app (Judge.me, Loox…) | HTML page · displayed widget | Aggregated reviews cross-product, potentially imported |
| Trustpilot | `trustpilot.com/review/{domain}` | Independent verified reviews |

Rule: always note all 3 in `_snapshot.reviews_sources`. Never use the highest number without noting its source, the on-page number may come from an app with imported reviews (unverified). Significant gap between sources = flag `[review_source_conflict]` in `_snapshot`.

**Posture générale · scrapé ≠ fait (D#518 · D6).** La triangulation des reviews est un cas d'une règle plus large · toute valeur scrapée porte un `reliability_tier` qui PLAFONNE sa confiance d'entrée par nature de source (doctrine `docs/system/scrape-as-allocation.md`, germe `resources/schemas/_shared/extraction-provenance.json`) · revealed/back-end ≤0.8 · behavioral-soft (volume, spend inféré) ≤0.5 · verbatim ≤0.5 · structural = hypothèse · declared (claim marque) ≤0.3. **Un chiffre sans procédé de mesure (« 60k clients ») n'entre jamais comme nombre nu** · il porte son marqueur ou reste hypothèse (garde-fou mécanique correspondant · `naked_number_unsourced` dans `resources/scripts/validate-all.py`). Là où on s'apprête à faire payer, trianguler cross-nature (≥2 natures dont une revealed/verbatim).

**Confidence score calculation** after scraping:
```
Expected spec.json fields: name, category, price, description, ingredients/composition, format/size
Score = (fields_non_null / 6) × 100

≥ 70% → proceed normally
40-69% → proceed with warning, list missing fields
< 40% → INCOMPLETE, list blocking questions before continuing
```

If score < 40%: the page doesn't have enough info to generate a useful sheet. Display:

```
Page too thin for auto-scan.

Your product page doesn't contain enough info (score: {X}/100).
Answer these questions and I'll build the sheet from your answers:

1. What problem does your product concretely solve?
2. Who is it for?
3. What's the mechanism or key ingredient?
4. What's the format / size / cure duration?
```

Wait for answers. Generate spec.json from answers + partial scraped data. Do not save an empty spec.json.

---

## Step 2bis · Business model auto-detection (v1.2.0 NEW · v2.57)

**Objectif** · auto-detect `brand.json#identity.business_model` (NEW v2.4 schema field) depuis les signaux scrape. Évite que l'opérateur doive le déclarer manuellement. Stage proposal via mutation gate, surface contextuel à la synthèse Step 7, AskUserQuestion fallback si ambigu.

**Logique de détection (à coder)** ·

```python
def detect_business_model(scrape_signals):
    """
    Auto-detect business_model from URL scrape heuristics.
    Returns enum: DTC | service | hybrid | subscription | marketplace
    """
    physical_locations = count_physical_locations(scrape_signals)  # /locations/, /clinics/, /stores/
    services_detected = count_services(scrape_signals)  # /services/, /consulting/, /packages/
    products_detected = count_products(scrape_signals)  # /products/, /shop/, /collections/
    subscription_signals = detect_subscription_core(scrape_signals)  # /subscribe/, recurring pricing primary
    marketplace_signals = detect_marketplace(scrape_signals)  # /vendors/, /sellers/, multi-brand listings

    # Priority rules
    if marketplace_signals:
        return "marketplace"
    if subscription_signals and products_detected == 0:
        return "subscription"  # SaaS pure ou abonnement-only
    if physical_locations > 0 and products_detected > 0:
        return "hybrid"  # clinic + product line (innerskin), restaurant + ecom, etc.
    if services_detected > 0 and products_detected == 0:
        return "service"  # agency, consulting, freelance
    if products_detected > 0 and services_detected == 0:
        return "DTC"  # DTC pure
    if products_detected > 0 and services_detected > 0:
        # Ambiguous · check revenue cues
        return "hybrid"  # mix
    # Default fallback
    return "DTC"
```

**Sourcing signals (heuristiques scrape)** ·

| Signal | Heuristique scrape | Sources HTML/URL |
|---|---|---|
| `physical_locations` | Scan URLs paths physiques | `/clinic`, `/clinique`, `/cabinet`, `/store`, `/location`, `/find-us`, `/find-a-store`, `/where-to-buy`, geolocation widgets, opening hours blocks, booking flows |
| `services_detected` | Scan URLs + sections services | `/services`, `/consulting`, `/agency`, `/packages`, `/coaching`, `/freelance`, sections titrées "Services" / "Packages" / "What we do" / "How we work", pricing tiers per-hour or per-project |
| `products_detected` | Scan URLs + schema.org/Product | `/products`, `/shop`, `/collections`, `/store`, PDP patterns, schema.org/Product markup |
| `subscription_signals` | Scan URLs + pricing recurring | `/subscribe/`, `/pricing/` avec tiers monthly/yearly, schema.org/SubscriptionPlan, copy "monthly access", "recurring" |
| `marketplace_signals` | Scan URLs + multi-brand listings | `/vendors/`, `/sellers/`, "shop our brands", "from {N} vendors", multi-brand listings explicit |

**Output workflow (4 sub-steps)** ·

**2bis.1 · Compute heuristique** depuis URL scrape data collected in Step 2 (Shopify JSON + HTML scraping + nav HTML). Apply priority rules table above. Output enum `DTC | service | hybrid | subscription | marketplace`.

**2bis.2 · Stage proposal via mutation gate** ·

```bash
python3 .skills/write-to-context.py \
  --path "brand.json#/identity/business_model" \
  --value "{detected_value}" \
  --source agent \
  --confidence 0.7 \
  --mode proposed \
  --reason "Auto-detected from scrape signals · {brief rationale}"
```

**2bis.3 · Stage business_model_signals object** (le contexte sourcing pour traçabilité) ·

```bash
python3 .skills/write-to-context.py \
  --path "brand.json#/identity/business_model_signals" \
  --value '{"physical_locations_detected": N, "services_detected": N, "products_detected": N, "declared_by_operator": false}' \
  --source agent \
  --confidence 0.7 \
  --mode proposed
```

**2bis.4 · Fallback AskUserQuestion si ambiguous** · si `products_detected > 0 AND services_detected > 0 AND products_detected < 3 AND services_detected < 3` (les deux non-zero mais faibles, classification incertaine), invoke AskUserQuestion avec 4 options ·

- **DTC pur** · acquisition produits uniquement
- **Hybrid** · réseau physique + ligne e-com (clinique, restaurant, magasin + produits)
- **Service B2B** · consulting, agency, coaching
- **Subscription** · accès récurrent / SaaS

L'opérateur arbitre, agent re-stage proposal avec la valeur confirmée (source=operator, confidence=1.0, mode=accepted) au lieu de la valeur heuristique.

**Surface contextuel à Step 7 Section 1 (Observé)** · 1 ligne contextuelle ajoutée à la synthèse ·

> *Modèle business · `{detected}` (basé sur · {N} produits + {N} services + {N} locations détectés). Override si pertinent dans setup-brand.*

**Backward compat** ·
- Brands pre-v2.57 sans `business_model.scraped` → next snapshot-brand run détecte et stage proposal automatiquement.
- Brands setup déjà v2.6 avec `business_model` déclaré manuellement (source=operator) restent inchangées tant que l'opérateur ne re-snapshot pas explicitement.
- Si `brand.json#/identity/business_model` already filled avec `source=operator` → SKIP stage proposal (operator declaration > agent heuristic).

---

## Step 3 · Generate spec.json (delegated encoding)

Before generating, read `brands/{slug}/brand.json` → sections `tone_of_voice` and `positioning`.
If these fields are filled → use the brand tone and positioning to align the product description.
If `brand.json` is empty (first product) → generate from the page alone, without inference.

**Encoding is delegated to `encode-batch` (Haiku sub-agent) so the main thread stays responsive.**

Build the observations list from scraped data, then launch encode-batch via Task tool:

```
Task tool call:
  subagent_type: shared
  skill: encode-batch
  model: haiku
  prompt: |
    {
      "brand_slug": "{slug}",
      "target_entities": [
        {"file_path": "brands/{slug}/products/{product_slug}/spec.json", "schema": "resources/schemas/spec.schema.json"}
      ],
      "observations": [
        {"semantic_kind": "product_name", "raw_value": "{title}", "evidence": "scrape: products/{handle}.js title", "source": "scrape", "confidence_signal": "literal"},
        {"semantic_kind": "product_category", "raw_value": "{product_type}", "evidence": "scrape: product_type", "source": "scrape", "confidence_signal": "literal"},
        {"semantic_kind": "product_description", "raw_value": "{stripped body_html, max 500 chars}", "evidence": "scrape: body_html stripped", "source": "scrape", "confidence_signal": "literal"},
        ... one observation per non-null scraped field ...
      ],
      "default_mode": "proposed"
    }
```

Producer (snapshot-brand) extracts the semantic signals from the scrape. encode-batch maps each signal to a `field_path`, runs `write-to-context.py` per mutation, rebuilds the snapshot, runs `finalize-mutation-batch.py`. Returns a structured summary (not operator-facing).

Absolute rule: **never invent a field**. If the info isn't in the page → don't include the observation. No creative inference. encode-batch refuses unmapped `semantic_kind` values rather than guessing.

Fields filled from scraping:
```json
{
  "meta": {
    "slug": "{product_slug}",
    "updated": "{today}"
  },
  "identity": {
    "name": "{title}",
    "category": "{product_type or inferred}",
    "format": "{extracted from variant title or description}"
  },
  "pricing": {
    "price": {main price},
    "price_original": {compare_at_price or null},
    "currency": "{EUR|USD detected}"
  },
  "description": "{stripped body_html, max 500 chars}",
  "_snapshot": {
    "source_url": "{url}",
    "scraped_at": "{datetime}",
    "platform": "shopify|html",
    "confidence_score": {0-100},
    "missing_fields": ["{field1}", "{field2}"]
  }
}
```

The `_snapshot` block is a technical block (non-schema official). Documents data provenance for traceability. Never manually deleted.

---

## Step 4 · Generate offers.json

Each Shopify variant = one candidate offer.

**Automatic typing logic** (apply in order):
0. **Group variants by price** before typing. If all variants share the same price → **1 single offer**. Variants (sizes, colors) are selection options, not distinct commercial offers. Never create N offers for N size/color variants at the same price.
1. If `selling_plan_groups` detected → at least one `type: "subscription"` offer
2. If variant title contains "mois", "month", "months", "cure" → `type: "prepay"` + fill `contents.duration`
3. If variant title contains several different products (e.g. "2 HB + 1 CB") → `type: "bundle"` + fill `contents.included_items`
4. If a single variant without explicit duration, or group of variants same price without duration → `type: "single"`
5. If `compare_at_price > price` → compute `savings_percent` and `savings_amount`

Fill `brands/{slug}/products/{product_slug}/offers.json` using the v2 `offer_groups[]` shape. Group-of-1 is valid and is the default for single-product offer files · only split into multiple groups if offers share distinct defaults (shipping, returns, warranty, payment_methods, active_window).

```json
{
  "_schema": "offers",
  "_version": "2.0",
  "meta": {
    "product_slug": "{product_slug}",
    "scope": "pre_cart",
    "updated": "{today}"
  },
  "offer_groups": [
    {
      "group_id": "GRP-01",
      "name": "Default group",
      "active": true,
      "shared": {
        "pricing": {
          "model": "one_shot",
          "currency": "{EUR|USD}"
        },
        "tags": []
      },
      "offers": [
        {
          "offer_id": "OFR-01",
          "name": "{variant.title}",
          "type": "{auto typing}",
          "product_refs": [
            {"slug": "{product_slug}", "quantity": {extracted or 1}}
          ],
          "pricing": {
            "model": "one_shot",
            "price": {variant.price / 100},
            "price_original": {variant.compare_at_price / 100 or null},
            "savings_percent": {computed or null},
            "currency": "{EUR|USD}"
          },
          "contents": {
            "quantity": {extracted or null},
            "unit_name": {extracted or null},
            "duration": {extracted or null},
            "duration_unit": {extracted or null},
            "is_prepay": {true if prepay or multi-month bundle, else null}
          },
          "subscription": null,
          "active": {variant.available},
          "tags": []
        }
      ]
    }
  ]
}
```

**Hard rules:**
- `_version: "2.0"` is mandatory. Never write `_version: "1.x"` or omit it.
- Always wrap offers in `offer_groups[].offers[]`. A flat `offers[]` at root is the legacy v1.x shape and is rejected by validate-resources.
- Use `product_refs: [{slug, quantity}]`, not legacy `product_ids: [slug]`.
- Group-of-1 is the default for single-product offer files. Only add more groups when shared defaults genuinely differ.

If subscription detected (selling_plan_groups): create a `type: "subscription"` offer with subscription fields filled to null (to complete via ingest-resource).

**Price per unit auto-calc (v1.3.0 NEW · v2.58)**

Pour chaque variant offre extraite, calculer automatiquement `spec.pricing.price_per_unit` (calcul mathématique direct depuis variants) ·

| Field | Calcul | Source |
|---|---|---|
| `value` | `price ÷ pack_quantity` (e.g. 39€ ÷ 30 caps = 1.30€/capsule, 130€ ÷ 30ml = 4.33€/ml) | `pricing.price` ÷ `specs.package_quantity` (ou `specs.weight` / `specs.volume`) |
| `unit` | Depuis specs (cap · ml · g · piece) | `specs.weight.unit` OR `specs.volume.unit` OR `specs.package_quantity.unit` |
| `currency` | Hérité de pricing | `pricing.currency` |

Stage via mutation gate (confidence 0.9 · calcul mathématique direct, pas d'inférence) ·

```bash
python3 .skills/write-to-context.py \
  --path "products/{product_slug}/spec.json#/pricing/price_per_unit" \
  --value '{"value": {calculated_value}, "unit": "{unit}", "currency": "{currency}"}' \
  --source agent \
  --confidence 0.9 \
  --mode proposed \
  --reason "Auto-calc price÷pack_quantity depuis variants extraction"
```

Si `pack_quantity` non détectable (variant unique sans specs structurés) → skip le stage, laisser le field null. Ne pas inventer un dénominateur.

**App-driven quantity break (frequent case):**

If the HTML page shows a quantity selector with tiered prices (1 unit / 2 units / 3 units…) but the API returns a flat price identical on all variants → the price structure is handled by a front-end app (Bundler, Bold Bundles, custom script). The API doesn't see it.

Behavior:
- Create an offer `type: "quantity_break"` with `pricing.tiers: null` and note `_snapshot.offer_note: "quantity_break app detected · tiers not accessible via API, requires HTML/Chrome capture"`
- Never invent unconfirmed price tiers
- Flag to the operator: "I detected a per-quantity price structure on the page, but it's handled by an app I can't read automatically. Can you confirm the tiers? (e.g. 1 pair = X€, 2 pairs = Y€ each…)"

**Geo-detection · note currency context:**

Price scraping always in a known context. The API returns the base currency (USD/GBP). The site may display a different currency based on geo.
- Always note the API currency (`_snapshot.api_currency`) and displayed currency if different (`_snapshot.display_currency`)
- Flag `[geo_detection_active]` if the two differ

---

## Step 5 · Audience cartography (4 movements)

**Doctrinal contract (v1.7.0 · D#517 · SONDE, pas carte).** Read `docs/system/audience-cartography.md`. Au scan, Step 5 produit une **SONDE D'AUDIENCE** · une lecture grossière, dérivée du CLAIM (ce que la page dit), au plus une à deux mères-hypothèses, pour valider le territoire et donner à l'opérateur un truc à corriger. **Il ne construit PAS l'arbre validé** (mère → sous-poches, découpe par porte d'entrée, test de splitting, scaffolding des dossiers). Cette carte STRUCTURÉE appartient à `map-audiences` en phase 3, STRICTEMENT APRÈS le pont mécanisme→usage (`build-atlas-complete` Step 2.5) · les vraies audiences se dérivent des JOBS (`spec.use_cases[]`, dont les spéculatifs = le marché non vu), pas du miroir du claim. Construire l'arbre ici = le bug du pré-emptage · il fige les audiences sur les déjà-servis avant que les usages aient fait émerger le marché non vu.

**Règle dure (D#517) · le scan ne grave pas d'arbre.** Au scan on rend · Movement 1 (observations brutes, neutre) + au plus une à deux **mères-hypothèses CLAIM en prose** (`validation_status: hypothesis`), puis on passe la main. Les Movements 2-3 (découpages alternatifs, hiérarchie mère/sous-poches, gate `audience_q1q4_answered`, scaffolding des dossiers) sont **REPORTÉS en phase 3** (`map-audiences`, après le pont 2.5) · ils ne tournent PAS au scan. C'est exactement le comportement du thin-page fallback ci-dessous · on le généralise à TOUT scan, pas seulement la page maigre. Garde-fou mécanique correspondant (maintainer) · la dent `use_cases[]` (≥1 `speculative`) côté `write-to-context` s'applique AUSSI à cette porte, pas seulement à la phase 3, sinon un agent littéral re-construit l'arbre ici.

The agent does NOT extract `pain_points[]`, `psychology.beliefs_limiting[]`, `voice.key_expressions[]` from the product page. Those fields belong to `mine-voc` verbatim. snapshot-brand fills only the cartography skeleton listed in `audience-cartography.md § Field-level contract`.

### Movement 1 · Raw observations (operator-facing)

Before any classification, name what the page literally said. No interpretation, just observation with source. **Zero internal jargon in the operator output** : never say "Movement", "cartography axis", "validation_status", "hypothesis-grade", "field path". Plain words.

Format example:

> *"Voilà ce que la page m'a dit côté audience, brut.*
>
> *La marque s'adresse à des femmes (mention 'pour elle' visible plusieurs fois). Le mot 'chute' revient 8 fois dans la description. Le mot 'pousse' 4 fois. Pas d'âge cité, pas de profession, pas de contexte de vie. Les tags produit pointent sur biotine, post-grossesse, cheveux abîmés.*
>
> *Trois signaux clairs (femmes, chute, pousse), le reste est silencieux. Je vais te proposer plusieurs manières de découper là-dedans, et tu trancheras."*

If the page is thin, say so plainly:

> *"La page m'a quasiment rien dit côté audience : juste 'pour elle' et deux tags génériques. Tout ce que je vais proposer après est à prendre comme une hypothèse de travail, pas une vérité. Tu corrigeras."*

Movement 1 is **never skipped**. Empty observations are a valid output, and more useful than a fabricated profile.

### Movement 2 · Découpages possibles (operator-facing)

> ⚠ **REPORTÉ EN PHASE 3 (D#517).** Au scan, on ne déroule PAS ce mouvement · les découpages alternatifs se travaillent dans `map-audiences` (phase 3), après que le pont mécanisme→usage a fait émerger les jobs spéculatifs. Au scan, on se contente d'une mère-hypothèse CLAIM (cf thin-page fallback, généralisé). La spec ci-dessous reste la référence du COMMENT, mais elle s'exécute en phase 3, pas ici.

Propose 2 to 3 alternative ways to slice the audience. Always mark one as the default hypothesis with a one-line rationale tied to a Movement 1 observation. Always invite override. **Operator-facing language**: "manières de découper", "découpages", "axes". Never "cartography axes".

The three canonical axes (skill-author vocabulary, NOT operator vocabulary):

- **Pain-driven** · slice by emotional state. Dominant when pain register diverges by segment.
- **Situational** · slice by life moment / context. Dominant when the same pain has different trigger contexts.
- **Demographic / cultural** · slice by who they are. Rarely dominant for paid acquisition; usually a modulator within pain or situational.

Operator-facing format example:

> *"Trois manières de découper cette audience, je te les pose toutes les trois et tu me dis laquelle colle à ce que tu vois en perfs.*
>
> *(1) Découpage par ressenti : 'je veux pousser' (longueur, densité, projet beauté positif) vs 'je perds mes cheveux' (chute active, charge émotionnelle, urgence). C'est le découpage qui colle quand le registre copy diverge fort entre les deux états.*
>
> *(2) Découpage par moment de vie : 'post-grossesse' vs 'stress longue durée' vs 'saisonnier'. Adapté quand le même pain est déclenché dans des contextes très différents.*
>
> *(3) Découpage par profil : 'voilées' vs 'non voilées'. Adapté quand le casting créa et le canal d'acquisition divergent par profil.*
>
> *Mon hypothèse à corriger franchement : (1) découpage par ressenti, parce que la page parle à la fois de chute et de pousse avec deux registres distincts (urgence vs projet). Si tu vois autre chose en perfs, dis-le."*

Wait for the operator's choice before Movement 3.

### Movement 3 · Hierarchy proposée (operator-facing)

> ⚠ **REPORTÉ EN PHASE 3 (D#517).** La construction de l'arbre validé (mère → sous-poches), le gate `audience_q1q4_answered` et le scaffolding des dossiers d'audiences vivent dans `map-audiences` (phase 3), APRÈS le pont 2.5 · jamais au scan. Le scan ne grave aucun dossier d'audience. La spec ci-dessous est la référence du COMMENT, exécutée en phase 3.

Once the operator picks an axis, propose 2 to 3 **groupes principaux** with 1 to 3 **sous-groupes** each. Skill-author terms: mother audiences and sub-audiences. **Operator-facing terms**: "groupe principal" et "sous-groupe", or just "groupe" et "sous". Never "mother audience", never `meta.parent_slug`, never "validation_status: hypothesis".

Operator-facing format example:

> *"Sur le découpage par ressenti que t'as choisi, voilà la structure que je propose, en deux niveaux.*
>
> *Groupe 1 : pousse-projet · longueur ou densité jugées insuffisantes, démarche beauté positive, pas d'urgence.*
> *  Sous-groupes : pousse-jeune-adulte (18-30, projet esthétique), pousse-recovery (post-coloration ou post-lissage, casse récente).*
>
> *Groupe 2 : chute-active · chute en cours, charge émotionnelle, urgence.*
> *  Sous-groupes : chute-post-grossesse (25-35, hormonal aigu), chute-hormonale-stress (22-32, diffuse longue durée), chute-traction (zones d'appui voile / tissages / tresses).*
>
> *Tous les sous-groupes sont à valider · c'est volontaire, ça veut dire qu'on les pose comme hypothèses de travail et qu'on les confirmera avec du vrai verbatim client juste après. Tu valides cette structure, ou tu veux qu'on en garde moins pour démarrer plus serré ?"*

Single-question gate. Wait for operator confirmation. Once confirmed, scaffold the audience folders (Step 6) and explicitly tell the operator they can visualize the result via `/phantom {brand_slug}`.

> *"Validé. Je grave les 5 audiences (2 groupes principaux + 3 sous-groupes). La commande `/phantom {brand_slug}` ouvre à tout moment le cockpit avec la liste, le statut de chacune, et ce qu'il manque pour passer de l'hypothèse au validé."*

**Avant le grave : binding produit.** Pour chaque audience validée (groupes principaux + sous-groupes), l'agent demande quel(s) produit(s) elle achète. C'est la passerelle multi-produit. Question opérateur-facing :

> *"Dernière question avant que je grave : pour chaque audience, quel(s) produit(s) elle achète chez {brand_name} ? Tu peux cocher un seul, plusieurs, ou laisser vide si l'audience est plus large que tes produits actuels (genre une persona brand-wide qui pourrait acheter n'importe lequel).*
>
> *Mes hypothèses par défaut, à corriger franchement :*
> *  pousse-projet → glow-boost (le hero, vise la pousse)*
> *  pousse-jeune-adulte → glow-boost*
> *  pousse-recovery → glow-boost*
> *  chute-active → glow-boost + cell-boost (les deux, c'est la cible naturelle du bundle)*
> *  chute-post-grossesse → glow-boost + cell-boost*
> *  chute-stress-hormonal → glow-boost + cell-boost*
> *  chute-traction → glow-boost*
>
> *Tu valides cette répartition ou tu veux ajuster ?"*

L'opérateur valide ou corrige. Encoder via `meta.applies_to_products: ["glow-boost"]` ou `["glow-boost", "cell-boost"]` ou `[]` (brand-wide). Le champ `meta.product_id` legacy reste null (ne pas écrire ce champ pour les nouvelles audiences post-v2.24.0).

Cette question débloque la navigation cross-référencée dans `/phantom` : *"voir les audiences sur glow-boost"* devient une commande naturelle (`/phantom {brand_slug} products glow-boost` rend la fiche produit avec les audiences cibles dessous).

### Movement 4 · Hand-off vers approfondissement (operator-facing)

Before closing Step 5, explicitly tell the operator how the audience encoding will be **used next**. Anchors why the work matters and proposes the next move in plain language métier · jamais nommer les skills internes en surface operator.

Format example (FR · canonique v2.51) ·

> *"Voilà comment ces audiences vont servir à partir de maintenant.*
>
> *Ce qu'on vient de poser est volontairement minimal · un nom, un découpage, une hypothèse. Pas de douleurs détaillées, pas d'objections, pas de citations clientes. C'est exprès · ces choses-là, je ne vais pas les inventer depuis une page produit, ils doivent venir de ce que disent vraiment tes clientes.*
>
> *Deux étapes enrichissent ça naturellement ·*
>
> *D'abord, on va écouter tes vrais clients · Trustpilot, widgets onsite, threads Reddit pertinents. On remplit pour chaque sous-groupe les douleurs exactes (le vrai mot qu'elles utilisent), les objections récurrentes, les expressions clés. C'est ce qui passe les audiences de l'hypothèse au validé sourcé. ~30 min en arrière-plan, tu n'attends pas.*
>
> *Ensuite, on consomme ces audiences enrichies pour sortir un set d'angles ranked, prêt à brief créa. Sans l'écoute clients d'abord, les angles sortent au mot près de mon chapeau, pas de tes clientes · c'est pour ça que je recommande cet ordre.*
>
> *Tu as aussi `/phantom {brand_slug}` à tout moment pour voir ces audiences avec leur niveau d'enrichissement.*
>
> *Mon avis · on lance l'écoute clients maintenant et on enchaîne sur les angles. Si t'as une deadline créa cette semaine et tu pousses direct sur les angles en hypothèse, dis-le, on ajuste. Et si t'as déjà des données existantes (reviews exportées, analytics, retours SAV) à m'injecter avant, donne-moi le fact le plus dense en 1-2 phrases · ça nourrit le travail."*

The closing question fuses three options · lance l'écoute clients maintenant, pousse direct sur angles, ou existe data à injecter d'abord. Routing interne (vers `mine-voc` → `produce-paid-angles`) se fait silencieusement à l'agent · operator ne voit jamais ces skill names en surface.

**Anti-pattern UX** · JAMAIS dire `mine-voc fait X` ou `produce-paid-angles consomme Y` en prose operator. Reformuler en langue métier · *"on va écouter tes vrais clients"*, *"on consomme ces audiences enrichies pour sortir un set d'angles"*, soft offer chemin recommandé.

### Movement gate (technical)

Stage the proposal once Movement 3 is confirmed by the operator (after they pick the hierarchy). Movement 1 and Movement 2 are conversational, not gated:

```bash
python3 .skills/stage-proposal.py \
  --brand {slug} \
  --checkpoint audience_q1q4_answered \
  --summary "Audience hierarchy: {N parents} ({slugs}) + {M sub-audiences} ({slugs}). Axis: {pain-driven|situational|demographic}."
```

The `checkpoint-resolver` hook resolves the pending:
- Confirmation (`"oui"`, `"go"`, `"valide"`) → `audience_q1q4_answered = true` → Step 6 write unlocked.
- Rejection (`"non"`, `"on revoit"`) → pending cleared, re-propose hierarchy.
- Free-form corrections (`"on enlève chute-traction"`) → no automatic resolve. Apply correction in memory, re-stage, re-ask.

**Writing `audiences/{slug}/profile.json` is blocked by write-to-context until `audience_q1q4_answered = true`.**

### Thin-page fallback

If Movement 1 returns near-empty observations AND the operator skips Movement 2 (e.g. *"je sais pas, propose"*) → ask **one** single question:

> *"En une phrase : à qui tu vends et quel problème tu résous pour eux ?"*

Extract one mother audience from the answer. Skip Movement 3's sub-audiences entirely. Mark the single audience `validation_status: "hypothesis"`. Move to Movement 4. Resilience over completeness when the page is empty.

**Final rule**: Do not create an audience folder if both Movement 1 observations and Movement 2 operator input are empty. Block the write, surface the gap, suggest the operator paste a brief or run mine-voc on a competitor.

---

## Step 6 · Generate profile.json (base, delegated encoding)

Fill `brands/{slug}/audiences/{audience_slug}/profile.json` with:
- What comes directly from the product page (gender apparent in copy, problem addressed in title/description)
- What comes from Step 5 movements 1-3 operator input (axis choice + hierarchy validation + product binding)
- Nothing else

**Hierarchy = N audience folders.** The Step 5 hierarchy validated by the operator typically yields 2-3 mother audiences + 1-3 sub-audiences each = 4-12 audience folders to scaffold. Scaffold each one. Mother audiences carry `meta.parent_slug: null` and `meta.scope: "broad"`. Sub-audiences carry `meta.parent_slug: "{mother-slug}"` and `meta.scope: "segment"` (or `"micro"` for hyper-niches).

**Encoding delegated to `encode-batch`.** Producer assembles per-audience observations from Step 5 (label, slug, scope, parent_slug, validation_status, gender, age_range, primary_problem, namespace-prefixed tags) and ships one encode-batch call per audience. Sub-agent maps and writes; producer continues to Step 7 synthesis without blocking.

**Field-level contract.** snapshot-brand fills only the cartography skeleton (full doctrine in `docs/system/audience-cartography.md § Field-level contract`):

```
meta.name              → human-readable label
meta.slug              → kebab-case slug
meta.scope             → broad | segment | micro
meta.parent_slug       → null for mother, slug-of-mother for sub
meta.validation_status → "hypothesis"
meta.audience_type     → "primary" | "secondary"
meta.applies_to_products → array of product slugs (multi-product binding, see audience-cartography.md § Audience binding par produit)
meta.tags              → ["problem:hair-loss", "context:post-pregnancy", ...] (namespaced)
identity.gender        → male | female | all (only if explicit on page)
identity.age_range     → {min, max} (only if explicit on page)
pain.primary_problem   → one-line statement (only if explicit on page or operator-stated)
```

Everything else stays null until `mine-voc` (verbatim → pain_points[].formulation, objections[], voice.key_expressions[], psychology.beliefs_limiting[]) or operator-driven enrichment.

**Hard rule.** snapshot-brand NEVER fills `pain_points[]`, `psychology.beliefs_limiting[]`, `psychology.beliefs_facilitating[]`, `voice.key_expressions[]`, `objections[]`, `behavior.*`, `psychology.emotions[]`. Inferring those fields from a product page is hallucination, even when the page mentions emotional language. Those fields are mine-voc territory.

---

## Step 7a · Phase 1 Macro confirmation light (v1.4.0 NEW · v2.68 progressive cartography)

**Doctrinal contract.** Phase 1 of progressive cartography per `docs/system/progressive-cartography-doctrine.md` (NEW v2.68, Sections 3-4). After Steps 1-6 scrape complete (territoire chain preserved), surface a light macro synthesis (3-5 lines) covering produit hero + offer macro + positionning + tone. Operator runs a binary gate (valide / corrige). No Q&A, no questionnaire, no open-ended audience questions. Anti-friction · max 2 minutes wall-clock total Phase 1.

Phase 1 replaces the prior "4 closed questions about audience" anti-pattern (canon Contextual Intelligence · No questionnaire before action). The agent does not ask Q1-Q4 audience demographic prompts before action. It synthesizes what scrape revealed at the macro level and lets the operator correct the base before drilling autonome in Phase 2.

### Phase 1 output · 3-5 lines macro synthesis

Format example (FR · canonique v2.68) ·

> *Produit hero · {product_name}, {price}{currency}, {category}.*
> *Offer macro · {N} offres détectées · {main offer type · ex single / bundle / subscription} · {N variants si pertinent}.*
> *Positionning observé · {1 ligne · ex "DTC supplément capillaire post-grossesse" depuis tags + copy}.*
> *Tone détecté · {register · ex "informatif scientifique / casual punchy / editorial premium"} (depuis copy + nav HTML).*
> *Plateforme · {Shopify confirmed / HTML scraping fallback}.*

Plain language, zero internal jargon (no `_snapshot.confidence_score`, no `business_model_signals`, no `validation_status: hypothesis`). 3 to 5 lines maximum. No bullet menu, no audience hypotheses surfaced (Phase 2 territory).

### Phase 1 gate light · binaire (valide / corrige)

Single-line close ·

> *Tu valides la base, ou tu corriges ?*

Operator answers binary ·
- **`"valide"`, `"go"`, `"OK"`, `"yes"`, `"spot on"`** → Phase 1 gate passes → Phase 2 drilling autonome unlocked.
- **Free-form correction** (e.g. *"le produit hero c'est plutôt X"*, *"non, le positionning c'est plutôt premium clinique"*) → apply correction silently in memory, regenerate Phase 1 synthesis with the correction baked in, re-ask the same binary gate.
- **Rejection without correction** (e.g. *"non c'est pas ça"*) → ask ONE sharpening question (cf root CLAUDE.md questions protocol · 1 thread question per turn) to identify the wrong fact, re-stage Phase 1.

**Hard rules Phase 1** ·
- **3-5 lines max.** Phase 1 is light. Surface produit + offer + positionning + tone. Nothing else. No audience hypotheses, no funnel signals, no business_model verbose, no investigation-posture 5 sections. Those live in Phase 2.
- **Binary gate only.** One line close. No menu, no Q&A, no four-questions enumeration. Anti-pattern AP · `4 closed questions about audience` BANNI.
- **Wall-clock budget** · target 2 min max Phase 1 (light synthesis + gate light). If the agent spends 5+ min crafting Phase 1, the Phase 1 contract is broken (too much detail leaking from Phase 2).
- **Fast-track bypass** · if `/operator/profile.json#preferences.auto_validate_after_n_brands` is `true` AND operator has run snapshot-brand on N+ brands prior (expert user opt-in config), skip Phase 1 gate light and auto-proceed to Phase 2. Reason · expert operator doesn't need the macro check, has internalized the pattern, wants speed. Default config = `false` (gate always shown).

---

## Step 7b · Phase 2 Drilling autonome (v1.4.0 NEW · v2.68 progressive cartography)

**Invoked if and only if Phase 1 gate passes.** Phase 2 of progressive cartography per `docs/system/progressive-cartography-doctrine.md` (Sections 3-4). Agent drill-downs autonomously across PDP details + reviews verbatims tagged + FAQ + cross-sells + trust badges + funnel signals (lead magnets + popups + scarcity) WITHOUT asking the operator any audience demographic question. Audience hypotheses are DEDUCED from verbatims clients (profession · pain points · objections traités copy site · use cases · hashtags) with explicit confidence chain. The agent presents its drill-down findings structured in 5 sections investigation-posture canon. The operator never answers Q1-Q4 ; Section 5 closes on an affirmed move (affirm the next move, open unknowns the agent carries itself, gate at most one blocking question), the operator only arbitrates if they choose to redirect.

### Drill-down autonome scope (Phase 2 input)

Agent autonomously drills across the following surfaces (no operator question · drill-down autonome from scrape data already collected in Steps 1-6 + targeted re-fetch if needed) ·

| Surface | Drill objective | Audience signal extracted |
|---|---|---|
| PDP details (ingredients, posology, contraindications, claims) | Identify product mechanism precision + target demographic implicit | Audience hypothesis from posology age range, contraindications (pregnant / breastfeeding signals female 25-40), claims (anti-aging signals 35+) |
| Reviews verbatims (Trustpilot + Judge.me/Loox/Okendo widget if accessible) | Tag verbatims by use_case + pain expressed + profession mentioned + life context | Audience hypothesis from verbatims tagged · "post-grossesse" mentions, "voilée" mentions, profession mentions, age implicit |
| FAQ section | Identify objections traités explicitly | Audience hypothesis from objections type · "is it for X profile" answered = X profile is a target |
| Cross-sells / "frequently bought with" | Identify product bundles + complementary use cases | Audience hypothesis from cross-sell pattern (e.g. anti-chute + shampoo gentle = post-pregnancy bundle pattern) |
| Trust badges / authority claims | Verify positioning Phase 1 + identify proof type used | Confidence boost on positioning hypothesis · clinical badges = medical positioning, celebrity = aspirational |
| Funnel signals (lead magnet popups, scarcity timers, exit-intent) | Identify funnel stage maturity + acquisition strategy | Acquisition hypothesis · aggressive DR funnel vs editorial funnel vs subscription-first |

**Hard rule** · drill-down autonome from scrape data first. ONLY surface a question to the operator if a variable is NOT accessible via drill-down autonome (e.g. first-party insight operator knows · seasonality patterns, LTV cohort data internal, gross margin, current paid stack). See Hard Rule "No Q&A premature" below.

### Phase 2 output · 5 sections investigation-posture canon

Before writing files, deliver the synthesis structured in 5 explicit sections per `docs/system/investigation-posture.md`. Cartographier avant affirmer · jamais affirmer une hypothèse comme un fait · jamais inventer des audiences/positionings présentés comme analytiques · le close affirme le MOVE (le défendu), porte les inconnus lui-même, ne gate qu'un éventuel bloquant · jamais un bulletin météo qui rend une question.

The 5 sections replace the prior 3-movements prose pattern (v1.0.1 ←) which mixed observed + deduced + projection as confident assertions. Reading the synthesis now lands like an analyst's note · faits sourcés, hypothèses avec confidence chain, inconnus listés, leviers proposés, opérateur arbitre.

### Section 1 · Observé (faits sourcés)

Structured list of what scrape + drill-down autonome (PDP details, reviews verbatims tagged, FAQ, cross-sells, funnel signals) revealed. Each fact carries its source. Pure observation, zero interpretation.

Format example (FR · canonique v2.54) ·

> *Observé · scan {URL} ({date}, {durée scan})*
>
> *Produit hero · {product_name}, prix {price}{currency} ({variant info if any})*
> *Catégorie · {product_type from API or HTML}*
> *Description site · {1-line summary stripped body_html}*
> *Preuves exposées sur fiche · {trust badges / authority claims observés ou "aucune visible"}*
> *Preuves sociales revendiquées · {claims trouvés site type "X familles", "Y reviews"}*
> *Reviews widget embarqué · {Judge.me / Loox / Okendo détecté} OR "aucun widget vérifié"*
> *Offres détectées · {N offres · types · paliers de prix}*
> *Plateforme · {Shopify confirmed / HTML scraping fallback}*
> *Drill-down autonome reviews · {N verbatims taggués · {tags fréquence top-3 ex "post-grossesse x12 · stress x8 · post-coloration x5"} OR "widget inaccessible"}*
> *Drill-down PDP details · {posology implicit demographic signals · contraindications · claims}*
> *Drill-down funnel signals · {lead magnets · popups · scarcity · cross-sells observés OR "none visible"}*
>
> *Pas observé directement (ne pas affirmer) · {liste explicite · audience démographique précise hors verbatims, gross margin, base mail, plateforme analytics, structure paid, base trafic, autres selon scan}*

**Hard rules Section 1** ·
- Liste à puces ou format structuré. JAMAIS prose narrative.
- Chaque fait avec son ancrage source (scrape URL · API Shopify · HTML · drill-down autonome reviews verbatims tagged · widget vérifié · Phase 1 correction opérateur si applicable).
- Bloc explicite "Pas observé directement" liste les variables non accessibles depuis le scan (anti-pattern AP-4 doctrine · affirmer ce qu'on n'a pas observé).
- Zéro adjectif évaluatif (*"impressionnant"*, *"unique"*, *"premium"*). Faits bruts uniquement.

### Section 2 · Déduit (hypothèses avec confidence chain)

3-5 hypotheses derived from Observé + sector knowledge. Each hypothesis carries · titre court · confidence explicite · indicateurs sources · question à l'opérateur (jamais conclusion posée).

Confidence chain · `forte` (5+ indicateurs convergents internes + externes), `moyenne` (3-5 indicateurs convergents majoritairement internes), `faible` (1-2 indicateurs partiels), `TRÈS faible` (intuition modèle sans support externe).

Format example (FR · canonique v2.54) ·

> *Déduit · {N} hypothèses à valider*
>
> *H1 · {hypothèse courte 1 ligne}*
> *  Confidence · {forte | moyenne | faible | TRÈS faible}*
> *  Indicateurs · {ce qui justifie l'hypothèse · 2-4 signaux observés}*
> *  À valider · {question(s) opérateur · jamais affirmation}*
>
> *H2 · {hypothèse courte}*
> *  Confidence · {niveau}*
> *  Indicateurs · {signaux}*
> *  À valider · {question}*
>
> *(... H3, H4, H5 selon densité corpus ...)*
>
> *Hypothèses avec confidence TRÈS faible · à valider OBLIGATOIREMENT avant utilisation stratégique (décision budget / positioning / brief créa). Intuition modèle, pas data terrain.*

**Hard rules Section 2** ·
- Chaque hypothèse formulée comme question, jamais comme conclusion posée.
- Confidence chain explicite et calibrée selon indicateurs réels (anti-pattern AP-1 doctrine · affirmer une hypothèse comme un fait).
- Hypothèses audience (qui achète) · confidence DEFAULT `TRÈS faible` sans mining client réel (anti-pattern AP-2 · personas inventés présentés comme analytiques). Indicateurs site / copy / partenaires influence = signaux faibles, JAMAIS sourced.
- Si projection chiffrée (ROAS, gross margin assumé, break-even) · marquer `projection conditionnelle` + variable assumed + sensibilité.

### Section 3 · Inconnu (variables non observables)

Explicit list of variables critiques pour la stratégie qui ne peuvent pas être levées depuis le scan initial. Pas de deviner ces variables. Liste explicite.

**Persistance in situ (D#518 · D5).** Un inconnu porteur + son levier ne s'écrit pas SEULEMENT ici au close · il se note AU MOMENT OÙ IL SURGIT pendant le scan (chaque pré-amorce non résolue, chaque condition d'arrêt 3 déclenchée · cf `docs/system/scrape-as-allocation.md`). Cette Section AGRÈGE des inconnus déjà repérés en cours de route, elle ne les invente pas à la fin. La carte garde son fond visible tout du long, pas seulement dans la synthèse finale.

Format example (FR · canonique v2.54) ·

> *Inconnu · {N} variables à creuser*
>
> *1. {variable critique 1} → {méthode pour lever}*
> *2. {variable 2} → {méthode}*
> *3. {variable 3} → {méthode}*
> *(... typiquement 5-8 variables sur un scan brand neuf ...)*

Typical inconnus list (adapter selon brand) ·
- Audience démographique réelle (vs hypothèses copy site)
- Gross margin réelle
- Taux conversion + abandon panier par page
- Plateforme email + segmentation existante
- Search volume FR/EN sur les keywords cibles
- Compétitif paid · qui run sur la niche
- Stack analytics installé (GA4, Hotjar, Mixpanel, etc.)
- Volume CA actuel + AOV historique + ROAS break-even réel

### Section 4 · Leviers (drill-down options · opérateur arbitre)

Pour chaque inconnue importante, quel skill / action permet de la lever. Options par axe d'investigation. Pas de "voici le plan complet", l'opérateur arbitre où on dépense le temps.

Format example (FR · canonique v2.54) ·

> *Leviers · {N} axes d'investigation prioritaires*
>
> *Axe A · {nom axe humain · ex Audience réelle} (lève {H#} + Inconnu {#})*
> *  → {action 1 en langage métier · ex "écoute clients Trustpilot + forums maternité"} ({durée})*
> *  → {action 2 si pertinent · ex "cross-référence avec analytics si dispo"}*
>
> *Axe B · {nom axe · ex Structure économique} (lève {H#} + Inconnu {#})*
> *  → {action · ex "1 question opérateur · gross margin, AOV, distribution"} ({durée})*
> *  → {action · ex "calibrage ROAS targets après"}*
>
> *Axe C · {nom axe · ex Structure paid compétitive} (lève Inconnu {#})*
> *  → {action · ex "audit compte Meta si dispo OU scan Meta Ads Library sur la niche"} ({durée})*
>
> *Axe D · {nom axe · ex Preuve sociale terrain} (lève {H#})*
> *  → {action · ex "écoute reviews Google + influenceurs déjà collaborateurs"} ({durée})*

**Hard rules Section 4** ·
- Action en langage métier opérateur. JAMAIS nommer le skill interne (`mine-voc`, `audit-meta-account`, `mine-vom`) en surface · operator-facing rule absolue cf root CLAUDE.md.
- Routing interne vers les skills se fait silencieusement à l'agent après le choix opérateur.
- Durée estimée pour chaque action (donne à l'opérateur la matière pour arbitrer).

### Section 5 · Close (verdict de move · affirme, ouvre, gate)

Le close ne se prescrit pas dans une forme, il se PRODUIT en faisant tourner la chaîne diagnostique sur le substrat encodé · position → négatif concurrentiel → audiences dérivées du mécanisme → priorité économique → verdict (`docs/doctrine/strategic-diagnostic-doctrine.md`, maillons a→e). C'est ce raisonnement sur le modèle de la marque qui sort le move, pas une consigne d'« interpréter ». Posture du close (faits → lecture experte → mouvement proactif, plancher anti-météo) · `docs/system/investigation-posture.md` + master `contextual-intelligence.md`. Few-shot sharp vs mushy, le noticing (ce que l'expert a vu de non-évident) et l'out honnête · `resources/canon/exemplars/close.md` (émuler, ne pas re-coller la forme ici).

**L'out honnête est un move, pas une dérobade.** Quand la data ne porte pas encore de verdict, nomme le SEUL inconnu bloquant + le chemin exact pour le lever ; inventer un verdict pour paraître décisif est l'échec, pas l'inverse.

La carte des axes de drill-down reste une affordance de REDIRECT (si l'opérateur veut piloter la priorité, on la lui pose), jamais le close par défaut.

**Self-critique avant de rendre ·** est-ce que ça tranche un move défendu, ou est-ce que ça décrit un état puis tend une question (le bulletin météo) ? Météo → réécris · affirme le move, porte les inconnus toi-même, ne garde qu'un éventuel gate bloquant.

Si le close affirme un move et que l'opérateur veut piloter la priorité, l'agent déplie alors les axes de drill-down (l'ancienne carte macro, désormais une affordance de redirect) et enchaîne sur l'axe choisi en respectant à nouveau les 5 sections (cycle itératif).

**Gate Phase 2 → Phase 3 (downstream audiences)** · le routage vers la phase audiences s'AFFIRME, il ne se demande pas en blanc · *"prochain move · on enrichit les audiences à partir des vrais clients (Trustpilot, widgets onsite, forums), ~30 min en arrière-plan · je lance, sauf si tu veux pivoter sur autre chose (audit perf, brief créa direct)."* (la phase suivante de progressive cartography enrichit le layer audience via drill autonome sur verbatims tagged · routage interne silencieux vers `map-audiences` ou `profile-audience` downstream). Si operator répond `oui` / `go` ou ne pivote pas → agent invoque le skill audience downstream silencieusement. Si operator pivote sur un autre axe → respecter le pivot, le routage Phase 3 attend.

## Phase Output · Decomposition Visibility (canon v2.78.2)

Après la synthèse 5 sections investigation-posture (Observé · Déduit · Inconnu · Leviers · Close ouvert), présenter OBLIGATOIREMENT matrices ASCII canon · 4 niveaux décomposition. Cette phase NE remplace PAS la synthèse 5 sections IP, elle s'ajoute APRÈS, en cohérence canon `decomposition-visibility-doctrine.md` v2.78.2. Objectif · rendre visible la décomposition logique du produit (specs · mécanismes · bénéfices 3 couches), expliciter le many-to-many produit × pain × audience, filtrer le positionnement par stage business, verbaliser la méthode pédagogique pour que l'opérateur comprenne *comment* l'agent a raisonné.

### NIVEAU 1 · Décomposition produit (specs · mécanismes · bénéfices)

Pattern matriciel obligatoire ·

```
SPECS (ce qu'il EST)       MÉCANISMES (ce qu'il FAIT)
[atomes objectifs]         [atomes action mesurable]

BÉNÉFICES 3 couches canon pain-benefit-chain
Functional   [bénéfice visible mesurable]
Emotional    [bénéfice ressenti subjectif]
Identity     [bénéfice qui je suis · identitaire]
             ← layer le plus chargé sur audience cible
```

`SPECS` = atomes objectifs (matériau, taille, prix, composition, certifications, durée). Sourcés Step 2 scrape PDP + Step 3 spec.json. `MÉCANISMES` = atomes action mesurable (ce que le produit *fait* matériellement · "absorbe l'humidité 3x plus", "réduit la friction de 60%", "diffuse 8 heures"). Distinction stricte · une spec décrit, un mécanisme agit. Si tu écris "matériau respirant" c'est une spec (passive) · "évacue la transpiration" est un mécanisme (action). `BÉNÉFICES 3 couches` canon `pain-benefit-chain.md` · Functional = mesurable extérieur ("pieds secs toute la journée") · Emotional = ressenti subjectif ("confort apaisant qui détend") · Identity = projection identitaire ("je suis quelqu'un qui prend soin de soi"). Marquer le layer le plus chargé sur l'audience cible (souvent Identity sur DTC mature, Functional sur fresh brand pain-driven).

### NIVEAU 2 · Many-to-many (pain × audience)

Matrice ASCII obligatoire si ≥2 pains AND ≥2 audiences identifiées (drill Section 2 Déduit · hypothèses audiences + Section 1 Observé · pains sourcés reviews/verbatims). Exemple format ·

```
                Audience1   Audience2   Audience3
Pain-1            ✓✓ PRIMARY    ·         ✓
Pain-2              ·       ✓✓ PRIMARY    ·
Pain-3              ·           ✓       ✓✓ PRIMARY
Espace blanc paid (si compétitif intel disponible)
```

`✓✓ PRIMARY` = pain dominant pour cette audience (volume verbatims, intensité émotionnelle). `✓` = pain présent mais secondaire. `·` = pain absent ou non observé. `Espace blanc paid` (ligne optionnelle si veille concurrentielle disponible) · zones de la matrice non occupées par les compétiteurs (territoire wedge paid potentiel). Si <2 pains OR <2 audiences identifiées dans cette run · skip la matrice et annoter explicit *"matrice many-to-many skippée · signaux insuffisants (1 pain identifié OR 1 audience)"*. Ne jamais produire une matrice 1×1 qui simule le many-to-many sans signal.

### NIVEAU 3 · Positionnement filtre par stage business

Si stage business inférable depuis context (ARR · domain age · proof points · reviews count · press mentions) · table obligatoire ·

```
STAGE              AUDIENCE PRIORITAIRE       ANGLE DOMINANT
Early (0-500k)     1 audience focus           Identity heavy
Growth (500k-3M)   2 audiences                Identity + Functional
Scale (3M+)        3-4 audiences              Diversifier
```

Marquer la ligne stage détecté (e.g. **Early** si domain <12 mois + reviews <100 + zero press tier-1 · **Growth** si 100-1000 reviews + national press + Trustpilot rating cohérent · **Scale** si tier-1 press + 1000+ reviews + multi-marché). Si stage non-inférable depuis signaux observés · skip la table et annoter explicit *"stage business non-inférable · signaux financials + proofs insuffisants"*. Ne jamais hardcoder un stage par defaults.

Plus distinction explicit · `audience produit-fit` ≠ `audience ciblage créa` (si opérateur déclare positioning targeting strategy). L'audience produit-fit est qui utilise et bénéficie réellement (sourcing reviews). L'audience ciblage créa est qui on adresse en paid (intent + acquisition cost + LTV cohort). Les deux peuvent diverger sur DTC mature · une audience produit-fit large peut être ciblée via une niche précise haute LTV en paid. Distinguer explicitement si signaux le permettent.

### NIVEAU 4 · Méthode pédagogique verbale

Toujours verbaliser comment l'agent a décomposé. Verbatim canon obligatoire (adapté langue opérateur) ·

> *"J'ai décomposé {brand} en 4 niveaux logiques · ce que le produit EST, ce qu'il FAIT, ce que ça CHANGE, à QUI ça répond. Puis filtre positionnement par stage business [détecté {stage}] · [audience prioritaire {audience}]. Le produit est many-to-many · 1 produit · N pains · M audiences."*

Cette verbalisation explicite la méthode de décomposition pour l'opérateur (transparency canon · agent qui montre comment il raisonne, pas seulement ce qu'il produit). Posture · pédagogique brève, jamais "voici mes étapes en 12 sous-points". Une phrase dense canon. Adapter `{brand}`, `{stage}`, `{audience}` aux signaux observés. Si stage non-inférable · drop la mention stage et garder uniquement "J'ai décomposé en 4 niveaux logiques · EST · FAIT · CHANGE · QUI · le produit est many-to-many".

**Hard rules Phase Decomposition Visibility** ·
- 4 niveaux obligatoires · skip un niveau = output invalid (downgrader sortie + flag).
- NIVEAU 1 toujours présent (specs + mécanismes + 3 couches bénéfices canon).
- NIVEAU 2 many-to-many matrix obligatoire si ≥2 pains AND ≥2 audiences identifiées · sinon annotation explicit skip.
- NIVEAU 3 stage business filter obligatoire si inférable depuis ARR/proofs/reviews · sinon annotation explicit skip.
- NIVEAU 4 méthode pédagogique verbale toujours présente · verbatim canon adapté langue opérateur.

**Anti-patterns Phase Decomposition Visibility** ·
- AP-DV-1 · Synthèse prose-only sans Phase Decomposition Visibility (5 sections IP seules · 4 niveaux skip silencieusement) → VIOLATION canon v2.78.2 systémique.
- AP-DV-2 · Many-to-many implicite (opérateur doit déduire la matrice depuis prose) → toujours expliciter en matrice ASCII si signaux suffisants.
- AP-DV-3 · 3 niveaux au lieu de 4 (skip bénéfices 3 couches functional/emotional/identity OR skip stage business filter OR skip méthode pédagogique) → invalid output.

### Sub-step · brand_equity_level heuristic auto (v1.3.0 NEW · v2.58)

Avant le rendu des 5 sections operator-facing, compute `brand.brand_equity_level` (enum `[low | medium | high]`) depuis heuristique combinée ·

| Level | Critères (ANY triggers level) |
|---|---|
| `high` | `financials.monthly_revenue > 500k€/mois` OR `proofs.press_mentions` top-tier (Vogue, Forbes, Elle, Wired, NYT) OR `partnerships` brand prestige (luxury houses, celebrity endorsements established) |
| `medium` | `financials.monthly_revenue` 50k-500k€/mois OR `proofs.press_mentions` national OR `Trustpilot rating > 4.5` AND `500+ reviews` |
| `low` | Sinon · fresh brand, niche, peu de proofs, no press, no high revenue |

Stage via mutation gate (confidence 0.6 · heuristique multi-signaux, validation opérateur recommandée) ·

```bash
python3 .skills/write-to-context.py \
  --path "brand.json#/brand_equity_level" \
  --value "{level}" \
  --source agent \
  --confidence 0.6 \
  --mode proposed \
  --reason "Heuristic depuis financials.monthly_revenue + proofs.press_mentions + market.sophistication"
```

Si signaux insuffisants pour discriminer (e.g. brand neuve, zéro revenue déclaré, zéro press, zéro reviews) → default `low` avec confidence 0.4 et reason explicit · *"Default low · signaux insuffisants pour discriminer medium/high"*.

### Sub-step · creative_zone init heuristic (v1.3.0 NEW · v2.58)

Compute initial `brand.creative_zone.{min, max, dominant, _observed_on_n_creatives}` depuis `brand.json#identity.brand_personality` + `tone_of_voice.register` + `sector` ·

| Profil détecté | dominant | min | max |
|---|---|---|---|
| Premium-clinique (luxe skincare, suppléments scientifiques) | `high-craft` ou `authoritative` | `informative` | `authoritative` |
| DTC-aggressive (direct response, urgency-driven) | `punchy` ou `casual` | `casual` | `punchy` |
| Luxury (mode, joaillerie, beauté prestige) | `editorial` ou `elegant` | `elegant` | `editorial` |
| Wellness mainstream (compléments OTC, beauty mainstream) | `friendly` | `casual` | `informative` |
| Tech / SaaS B2B | `informative` | `informative` | `authoritative` |
| Hybrid / undefined | `friendly` (default safe) | `casual` | `informative` |

`_observed_on_n_creatives` · `0` initial (incrémenté par `decompose-ad` cumul après chaque ad reverse-engineered, doctrine atlas vivant).

Stage via mutation gate (confidence 0.5 · init heuristique, refinable par observation réelle créas) ·

```bash
python3 .skills/write-to-context.py \
  --path "brand.json#/creative_zone" \
  --value '{"min":"{min}","max":"{max}","dominant":"{dominant}","_observed_on_n_creatives":0}' \
  --source agent \
  --confidence 0.5 \
  --mode proposed \
  --reason "Init heuristic depuis brand_personality + tone_of_voice"
```

Si `brand_personality` + `tone_of_voice` tous deux null (brand fresh post-setup sans enrichissement) → skip le stage, laisser field null. `creative_zone` sera initialisé au premier `decompose-ad` ou enrichissement manuel.

(EN equivalent · adapt to operator language detected) ·

> *The dominant wall here is {wall}, not {false lead} · {Observé + Déduit anchor in 1 line, confidence carried}.*
>
> *The move · priority 1, we {defended action}, because {reason · the exact point where it breaks down}. In parallel I'll {feasible part of the open unknown}, I'll bring it back without you having to dig.*
>
> *The one thing blocking me from {quantifying / calibrating} is {unknown that is both unknowable from data and blocking}. Give it to me and I'll calibrate, otherwise I move on {the move} and we'll quantify after.*
>
> *Redirect affordance (if you'd rather steer the priority yourself) · "I've got {N} axes ready ({names}), tell me which one."*

**Hard rules Section 5** ·
- Close = verdict de move (affirme défaut · ouvre porté soi-même · gate au plus 1 question bloquante). Le bulletin météo (montrer l'état SANS le lire puis tendre une question passive / « lequel veux-tu creuser ? ») est BANNI · montrer les faits et lister les inconnus est BON, c'est l'absence de lecture plus le hand-off passif qui plante · une question qui n'est pas un gate est OUVERTE, pas posée.
- On affirme le MOVE, jamais une hypothèse comme un fait · le move s'appuie sur le Déduit qui porte sa confidence (AP-1 / AP-2 tiennent).
- Le menu d'axes priorisés reste disponible UNIQUEMENT comme affordance de redirect si l'opérateur choisit de piloter · jamais comme close par défaut.
- Exemplar de référence (sharp vs mushy) · `resources/canon/exemplars/close.md`.

**Visual assets soft mention (v2.50 · pull-not-push pattern) :**

After the synthesis (default close OR trust-and-deepen close), if the brand has no visual assets canonized yet (brand-level `assets_canonical.logo_canonical` empty AND no `badge_canonical` entries AND no `mascotte_canonical`), add **at most one short line** mentioning visual assets as a *purely optional* next path the operator can pull when relevant downstream :

> *"Si tu veux préparer tes visuels (logo, badges) pour les pubs, on peut le faire en récupérant depuis ton site."*

Rules (strict, anti-push) :
- One line max. Never a menu, never bullets, never a "tape commande X" suffix.
- Never name the skill (`import-asset`, `extract_from_url`) in operator prose.
- Posture · *soft offer*, not directive. Use "Si tu veux" / "If you want" framing.
- If operator skips or pivots, the agent moves on without relance. No "are you sure?", no "this is recommended".
- Drop the line entirely if assets already canonized (no value-add to repeat).

**Bridge code (v2.51 NEW · câblage explicite Task tool params)** ·

Si operator répond positivement (*"oui"*, *"go"*, *"vas-y"*, *"OK"* après la mention visuelle), invoke `import-asset` skill via Task tool · params concrets ·

```
Task tool invocation ·
- description · "Récupère assets visuels brand depuis site"
- subagent_type · "general-purpose" (import-asset recommended_model: sonnet, subagent_safe: true)
- prompt · "Run import-asset Mode C extract_from_url pour {brand_slug}. Brand URL · {brand.identity.website} (depuis brand.json post-snapshot). Asset type · auto_multi (skill itère sur tous types détectés · logo + badges + payment_methods + patterns). Workflow standard HR7 4 sub-steps (C.1 scrape HTML curl User-Agent moderne, C.2 extract candidats heuristics par type, C.3 download + rasterize SVG fallback chain magick > convert > cairosvg, C.4 operator gate validation par type). Return inventory peuplé visual_identity.json#assets_canonical post-validation."
```

Wait completion. Skill retourne inventaire des assets canonisés. Snapshot-brand continue son no-orphan close standard (deep paths Voice of Customer / Voice of Market / etc.) sans relance sur les visuels (operator a déjà décidé).

Si operator répond négatif ou pivote (*"non merci"*, *"plus tard"*, *"on verra après"*, OU change directement de sujet), agent abandon silencieusement la mention visuelle. Pas de relance, pas de "are you sure?".

**Bridge code reste instruction agent-facing**, jamais leak operator. L'operator voit uniquement la mention soft 1 ligne et son own choice.

Rationale · onboarding completion (jauge "brand prête à X%" backlog v2.51+) consume canonical assets as one dimension of brand readiness. v2.50 ships the soft mention upstream so the operator becomes aware of the path without pressure, and the actual import is triggered later when a downstream skill (e.g. `compose-creative` mode layered) needs the asset and offers to fetch it then. v2.51 ajoute le bridge code câblé pour que l'option (a) "Récupère depuis site" déclenche concrètement import-asset Mode C sans que l'agent improvise les params.

If the page was thin (`_snapshot.confidence_score` internal flag low), say so explicitly in Section 1 (Observé) · list reduit + bloc "Pas observé directement" enrichi. JAMAIS exposer le score comme un nombre. La thin-page se reflète dans la Section 2 (Déduit) · hypothèses majoritairement `faible` ou `TRÈS faible` avec validation OBLIGATOIRE flag.

**Hard rules cross-section** ·
- **5 sections explicites, jamais fusionnées en prose continue.** Anti-pattern AP-6 doctrine · prose narrative continue qui mélange Observé + Déduit + projection + reco.
- Each section a son rôle distinct · Observé = faits sourcés · Déduit = hypothèses avec confidence · Inconnu = variables à creuser · Leviers = options drill-down · Close ouvert = UNE question macro.
- Use schema field semantics as analytical vocabulary (e.g. *"le pain principal observé est X"*, not *"pain_points[].formulation: X"*).
- **NEVER name a file, a path, a skill, a confidence number (0.7, 73%), or an internal flag in operator surface.** Confidence chain exposed as `forte / moyenne / faible / TRÈS faible` qualitatifs uniquement.
- Anti-pattern AP-3 doctrine BANNI · copywriting narratif déguisé en analyse (*"C'est pas une marque de mobilier enfant, c'est une réponse artisanale à une contradiction..."*) → toujours réécrire en posture analyste · faits + indicateurs + hypothèse formulée comme question.

**Decisive test before sending** · read the synthesis as a stranger to the brand. Test binaire ·
- (1) Est-ce qu'une affirmation prose mélange dans la même phrase observé + déduit sans signaler la nature ? Si oui → AP-1 violation, réécrire en Section 1 (Observé) vs Section 2 (Déduit) séparées.
- (2) Y a-t-il une audience / persona présenté comme analytique sans data verbatim ? Si oui → AP-2 violation, downgrade à hypothèse Section 2 confidence `TRÈS faible` avec flag validation OBLIGATOIRE.
- (3) Le close affirme-t-il *"Je passe au next step"* / *"Save this snapshot"* / *"Want anything else"* ? Si oui → AP-5 violation, réécrire en Section 5 (Close ouvert) avec UNE question macro drill-down.

**Behavior on operator response:**
- **Confirm** (*"yes"*, *"go"*, *"spot on"*, *"ok"*) → write spec.json + offers.json + profile.json.
- **Correction** (*"price is 39€"*, *"audience is more men"*) → apply, regenerate the synthesis incorporating the correction, ask again.
- **Never write files before explicit confirmation.**

Once saved, run three silent post-writes before talking:

1. **Append to `brands/{slug}/pending-validations.md § Context gate`** one `[ ]` line per inferred field that was stamped with `mode=proposed` during this run. Wording in the operator's language, plain-language source tag (`(inferred from site)`, `(deduced)`), never `source` / `confidence` / `mode` jargon. Typical entries: audience(s) inferred, positioning inferred, tone inferred, compliance gaps detected (e.g. missing contraindications on a medical device).
2. **Trigger `validate-resources` silently** on the brand. This refreshes `status.json` (completeness per entity, freshness stamps, `wedge_complete`), rebuilds `learnings-index.json` if present, and re-runs the snapshot digest. Surface its result only if it flags MAJOR/CRITICAL · otherwise stay silent.
3. **Run `finalize-mutation-batch`** · single bash command, replaces the prior LLM-based coherence check (which was systematically skipped under load):

   ```bash
   python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
   ```

   Reads `_field_types`, inspects every mutation written in this run, runs structural checks (unmapped paths, manual derived writes, tone misclassification, missing entity files), emits a `coherence_check` event so `turn-end-audit` sees the loop closed.

   Exit code 2 = blocking issue → revise before shipping the summary. Exit code 0 with warnings = log them, ship. **Non-negotiable, mechanical, not skippable.**

4. **Déposer le beat de restitution du scan (D#520).** Doctrine SSOT · `docs/system/restitution-beat-doctrine.md` (contrat, règles décision-d'abord, richesse, temporalité, mode). Écris (`Write` · c'est sous `.phantom/`, hors `brands/`, donc hors gate mutation) le fichier `.phantom/beats/{slug}/scan.json` qui capture CE QUE TU VIENS DE FAIRE pendant que ton contexte est frais. C'est la matière que l'orchestrateur RENDRA à l'opérateur · tu ne résumes pas en une phrase, tu déposes le registre (anti double-compression · le raisonnement meurt quand on le compresse ici puis qu'on demande au fil de le re-broder). Forme ·

   ```json
   {
     "phase": "scan",
     "verdict": "<lecture experte top-line, tranchée, une ligne>",
     "read":     "<2-3 phrases de lecture experte · le pourquoi, en prose · le report ouvre en prose avant les bullets>",
     "found":    ["<sources lues + faits bruts saillants>"],
     "blocked":  [{"source": "<ex · Trustpilot>", "reason": "<ex · 403, fallback forums>"}],
     "analyzed": ["<déductions, recoupements, ce que le site dit vraiment>"],
     "rejected": [{"what": "<piste écartée>", "why": "<la raison, défendable>"}],
     "encoded":  ["<artefacts posés · spec, offres, positionnement>"],
     "confidence": [{"claim": "<assertion>", "level": "forte|moyenne|faible", "reason": "<la VRAIE cause · une source bloquée n'est pas une audience faible>"}],
     "basis":    "<une ligne sobre · les sources lues, la largeur du travail · rendue en « Lu · ... »>",
     "tease": "<une ligne qui tease la valeur DANS la vue · ce qu'il va voir de surprenant ou utile · une invitation · NE mets pas de chemin, le code ajoute la commande paste-ready et choisit la vue selon la phase>"
   }
   ```

   **Le renderer réorganise en décision-d'abord** (pas dans l'ordre du process) · ouverture `verdict` + `read`, puis le raisonnement qui flue (`analyzed` + `found` + `rejected`), puis **Ce sur quoi je reste prudent** (`blocked` + confiance non-forte, avec leur cause), puis `basis` (« Lu · »), puis le CTA `tease`. La confiance **forte** n'est pas affichée séparément, elle vit dans le verdict (on flague l'incertain, on ne caveat pas ce dont on est sûr). Tu déposes les champs, le code décide la forme.

   **Format report (cf Shape of Key) · prose + bullets + `/phantom`.** Le `verdict` + `read` ouvrent en prose, puis les listes se rendent en bullets. Chaque entrée de `found` / `analyzed` / `encoded` peut porter une **amorce grasse** suivie de sa justification (`**la thèse.** le pourquoi en clair`).

   **Richesse · le second ordre, pas le constat.** `read` et `analyzed` ne s'arrêtent pas au fait, ils déroulent sa **conséquence** · l'implication économique (« business d'abonnement → pilotage à la LTV → CAC acceptable plus haut → mais tout ride sur la rétention M2 »), la texture concurrentielle (pourquoi le lane est libre, ce qu'il coûte, à quoi il est fragile), et **le nerf** (la tension non-évidente qui décide tout). C'est la densité d'insight qui fait l'expert 360, pas la longueur. Registre **sharp, pair-expert, jamais météo** · chaque rejet porte sa raison (le travail de rejet est le plus défendable et le plus invisible), chaque confiance porte SA cause.

   **CTA · `tease` propose, le code exécute.** Le `tease` est l'accroche (la valeur dans la vue) · le renderer y appose la commande `/phantom {slug} {vue}` paste-ready et **choisit la vue selon la phase** (au scan, la décompo produit `products`, PAS le spectre qui n'existe pas encore). Champ vide = omis, jamais inventé. C'est un état système (restitution), pas de la donnée de marque · il ne transite pas par `write-to-context`, et un hook (`beat-emit`) garantit qu'il sera montré.

Then propose enrichment without waiting:

```
Saved.

Want to enrich now?
Paste anything: brief, customer reviews, positioning doc, support returns.
I sort and file automatically.

(Nothing now → say "later".)
```

- If the operator pastes content → **trigger ingest-resource immediately** on that content.
- If "later" / "no" / silence → close:
  ```
  OK. Run "validate" when you're ready to check consistency.
  ```

---

## Hard Rules

- **Stage before asking · always.** Hero confirmation (Step 1) and audience confirmation (Step 5B) MUST call `.skills/stage-proposal.py` before showing the question to the operator. The checkpoint-resolver hook promotes checkpoints from the literal operator reply · agent self-declaration is not accepted. Writes to `products/*/spec.json`, `products/*/offers.json`, `audiences/*/profile.json` are blocked by the write-to-context workflow gate until checkpoints resolve.
- **Never invent** a field not present in the page or answers. Null > approximation.
- **Hero detection = nav HTML first, API second.** Some hero products are absent from `products.json`. The site nav is the source of truth, read the homepage HTML before any API call when the URL is a brand URL.
- **Confirmation before scraping · always.** Show the detected product to the operator and wait for an explicit "go" before starting the scraping. Never assume.
- **Shopify JSON API priority** over HTML for product data. Do not scrape HTML if `/products/{handle}.js` returns 200. Exception: product detail page scraping (above-the-fold, reviews, quantity breaks) always runs in complement to the API.
- **Review triangulation mandatory.** Capture the 3 sources separately (native Shopify, onsite app, Trustpilot). Never use a single number without noting its source. Significant gap = flag `[review_source_conflict]`.
- **Quantity breaks = app-driven, invisible to API.** If HTML shows per-quantity price tiers but API is flat → `type: "quantity_break"`, tiers null, ask the operator. Never invent tiers.
- **Geo-detection.** API currency ≠ display currency → note both, flag `[geo_detection_active]`.
- **Confidence score mandatory**. If < 40% → block before saving spec.json, ask for missing fields.
- **No Q&A premature on audience.** Agent MUST drill-down autonome reviews + PDP details + verbatims tagged before posing ANY question to the operator about audience. Questions opérateur uniquement si data n'est PAS accessible via drill-down autonome (e.g. first-party insight opérateur connaît · seasonality, LTV cohort interne, gross margin réelle, current paid stack). Canon Contextual Intelligence "No questionnaire before action" + Progressive Cartography Phase 2 (cf `docs/system/progressive-cartography-doctrine.md`). Anti-pattern legacy v1.3.x · "4 closed questions about audience" → DROPPED v1.4.0. Audience hypotheses are deduced from verbatims with explicit confidence chain (Section 2 Déduit), jamais demandés en Q&A pre-action.
- **Phase 1 + Phase 2 gate light binaire.** Gate intermédiaire entre Phase 1 macro confirmation (Step 7a) et Phase 2 drilling autonome (Step 7b) DOIT être binaire (1 ligne `valide` / `corrige`). Pas de Q&A verbeux, pas de menu, pas de quatre options equal-weight. Anti-friction. Mode fast-track auto-validate via `/operator/profile.json#preferences.auto_validate_after_n_brands true` pour expert operator config opt-in (default `false`, gate always shown).
- **Never overwrite brand.json**. This skill doesn't touch brand.json.
- **Setup-brand first**. If `brands/{slug}/` doesn't exist → stop and route to setup-brand.
- **One product per run**. Multi-product = relaunch the skill for each product.
- **`_snapshot` block always present** in spec.json and profile.json. Documents provenance.
- **Do not create audience folder** if Q1 + Q2 are both null, not enough to identify audience.
- **Write modes.** Never call `write_to_context` on a whole file path with `mode=proposed` · the proposal wrapper stamps `_proposed/_source/_confidence` at the root object and corrupts consumers. Always scaffold the file in `mode=direct` (full structure with null placeholders), then stamp inferred fields one by one with `mode=proposed` using a JSONPointer fragment (e.g. `file.json#/pricing/price`). The tool enforces this guard since 2.6.20.
- **Offers.json = v2 `offer_groups[]` only.** Never write the legacy flat `offers[]` at root. `_version: "2.0"` is mandatory. Single-product files use a group-of-1. Use `product_refs: [{slug, quantity}]`, not `product_ids`.
- **`finalize-mutation-batch` is mandatory before any operator-facing summary.** Step 7 post-write #3 runs `python3 .skills/finalize-mutation-batch.py --brand-slug {slug}`. Mechanical Python primitive · no LLM negotiation, no skip path. Exit code 2 = blocking issue, MUST revise. Soft-prescribed `validate-output-coherence` LLM call (prior version) was skipped 100% of the time under load on the v2.7.1 stress test; this is the replacement.

### Hard Rules v1.4.1 NEW (v2.69.1)

- **HR-v1.4.1-NEW-1 · No anticipatory output before scrape data sourced.** Avant que Step 2-3 scrape ait completed et retourné data factuelle PDP/homepage · l'agent NE DOIT PAS produire output anticipatif sur identity produit · category · positionning · audience cible depuis le nom de brand seul. Violation directe Contextual Intelligence master · "PhantomOS reasons over a business universe · structure serves intelligence". Pattern observé · Stepprs name suggère sport (steps) · agent halluciné "grip socks athlétiques" pré-scrape · réalité = foot care insoles pain relief. Anti-hallucination canon · output muet sur identity produit jusqu'à Step 3 done. Output autorisé pré-scrape · acknowledge URL pasted + 1 line "scrape en cours · 30-60s" sans deviner identity.
- **HR-v1.4.1-NEW-2 · No defaults inferred · workspace fresh premier contact.** Quand brand_slug non-existing AND workspace identity vide (no operator/profile.json hint) · l'agent NE DOIT PAS inférer defaults (langue · register · scope solo/équipe/agency) depuis le contexte conversation OR session cross-references. L'agent runtime sur workspace vraiment vierge premier contact n'a PAS contexte cross-session valide. Doit demander explicit 2-3 questions setup minimal (langue outputs · scope) avant scrape OR setup mutations. Exception · /operator/profile.json#preferences populated (operator déjà confirmé brands antérieures) · alors fast-track defaults OK. Pattern observé · agent commité "agency multi-client + outputs EN" defaults sans confirmation operator runtime vierge · violation transparency canon.
- **HR-v1.4.1-NEW-3 · URL intake · proactive chain canon · scrape async + setup Q&A en parallèle.** Quand opérateur paste URL e-com (Shopify · homepage · PDP) en premier OR mi-session message · agent DOIT déclencher proactive chain · (1) lancer scrape URL en async background via Task tool snapshot-brand · (2) EN PARALLÈLE poser 2-3 questions setup minimal si workspace fresh · (3) quand setup Q&A done · synthese scrape déjà prêt · enchaîner Phase 1 macro confirmation immédiate. Anti-pattern · attendre setup Q&A complet avant lancer scrape (séquentiel · perd 1-2 min wall-time inutile). Canon root CLAUDE.md "Proactive multi-skill deployment" · obvious chain ≥2 sub-skills = deploy silently parallèle.
- **HR-v1.4.1-NEW-4 · Sitemap discovery before guessing pages.** Avant fetch pages additionnelles devinées au-delà de PDP/homepage (about · faq · reviews · etc.) · l'agent DOIT essayer `/sitemap.xml` OR `/robots.txt` parse OR scan homepage navigation links pour discoverability paths réels. Évite 404 silencieux qui perdent context utile. Pattern observé · agent fetch `/pages/about` direct sur Stepprs.com · 404 · about page existe ailleurs (vérifier sitemap d'abord). Si sitemap absent · fallback navigation crawl homepage anchor links pour discoverability.

### Hard Rules v1.5.0 NEW (v2.78.2 · Decomposition Visibility Discipline)

- **HR-v1.5.0-NEW-1 · Phase output Decomposition Visibility obligatoire après 5 sections IP.** Tout output Phase 2 (Step 7b synthesis) DOIT enchaîner avec Phase Decomposition Visibility (4 niveaux matriciels canon) APRÈS la synthèse 5 sections investigation-posture (Observé · Déduit · Inconnu · Leviers · Close ouvert). La Phase Decomposition Visibility ne remplace PAS les 5 sections IP, elle s'ajoute en aval. Output qui termine sur Section 5 Close ouvert sans présenter les 4 niveaux décomposition = VIOLATION canon v2.78.2. Anti-pattern legacy v1.4.x · "synthèse prose-only sans visualisation matricielle décomposition" → DROPPED v1.5.0.
- **HR-v1.5.0-NEW-2 · 4 niveaux matriciels canon obligatoires · skip 1 = invalid output.** NIVEAU 1 décomposition produit (specs · mécanismes · bénéfices 3 couches functional/emotional/identity canon `pain-benefit-chain.md`) · NIVEAU 2 many-to-many pain × audience matrix ASCII si signaux suffisants · NIVEAU 3 positionnement filtre par stage business (Early/Growth/Scale) si inférable · NIVEAU 4 méthode pédagogique verbale toujours présente. Skip un niveau silencieusement (sans annotation explicit raison signaux insuffisants) = output invalid · downgrader sortie + flag à l'opérateur.
- **HR-v1.5.0-NEW-3 · Many-to-many matrix obligatoire si ≥2 pains AND ≥2 audiences identifiées.** Si Section 1 Observé sourcing pains ≥2 (verbatims reviews · forums · PDP) AND Section 2 Déduit audiences ≥2 (hypothèses avec confidence chain) · présenter matrice ASCII NIVEAU 2 obligatoirement. Marquer PRIMARY pain × audience dominante + relations secondaires + espace blanc paid (si veille concurrentielle disponible). Ne jamais laisser le many-to-many implicite en prose · canon visibilité décomposition exige matrice explicite.
- **HR-v1.5.0-NEW-4 · Stage business filter obligatoire si inférable depuis ARR signals.** Si signaux financials (monthly_revenue) OR proofs.press_mentions OR reviews count OR domain age OR market.sophistication permettent d'inférer stage business (Early 0-500k · Growth 500k-3M · Scale 3M+) · présenter table NIVEAU 3 obligatoirement avec ligne stage détecté marquée. Distinguer audience produit-fit (reviews observed) vs audience ciblage créa (intent + LTV declared) si signaux le permettent. Si signaux insuffisants · skip avec annotation explicit *"stage non-inférable · signaux insuffisants"* · jamais hardcode default stage.
- **HR-v1.5.0-NEW-5 · Méthode pédagogique verbale obligatoire · verbatim canon adapté langue opérateur.** NIVEAU 4 doit toujours verbaliser comment l'agent a décomposé · verbatim canon *"J'ai décomposé {brand} en 4 niveaux logiques · ce que le produit EST, ce qu'il FAIT, ce que ça CHANGE, à QUI ça répond. Puis filtre positionnement par stage business [détecté {stage}] · [audience prioritaire {audience}]. Le produit est many-to-many · 1 produit · N pains · M audiences."* (adapté langue opérateur · EN équivalent runtime detection). Transparency canon · agent montre comment il raisonne, pas seulement ce qu'il produit. Posture pédagogique brève · une phrase dense canon, jamais une décomposition en 12 sous-points.

---

## v1.8 Field Awareness (2026-04)

The `_TEMPLATE` is at v1.8. When scraping a product page, you must look for and fill these new fields if the info is present. Null > invention.

**spec.json · blocks to populate when applicable:**

- `specs.composition[]` · structured list (ingredient, pct, organic_certified, class, origin, inci). Accepts string for legacy too.
- `specs.posology` · recommended_daily_servings, serving_unit, timing, duration_recommended, max_daily_dose, notes. Relevant: supplements, skincare, cures.
- `specs.contraindications` · conditions[], medications[], age_min/max, pregnancy, breastfeeding, warnings[]. Relevant: supplements, cosmetics, food.
- `specs.origin` · country, region, facility, local_supply_pct, made_in_claim, supply_chain_transparency.
- `specs.production_method` · type, batch_size, frequency, method_notes. Relevant: artisanal, made-to-order.
- `specs.preparation` · cooking_required, method, time_minutes, temperature, serving_suggestions[]. Relevant: food.
- `specs.external_databases` · open_food_facts_id, yuka_id, inci_beauty_id, ciqual_id, ean, gtin.
- `specs.target_suitability` · skin_types[], hair_types[], body_areas[], use_cases[], demographics[]. Relevant: beauty, skincare.
- `specs.durability` · warranty_years, warranty_type, repairable, spare_parts_available, repair_program, lifespan_estimate, repairability_index. Relevant: apparel, hardware, electronics.
- `nutrition_facts.allergen_sources[]` · allergen → ingredient source mapping.
- `nutrition_facts.nutri_score_grade` · A-E enum (FR 2025+).
- `perishability.period_after_opening_months` · PAO (cosmetics EU mandatory).
- `perishability.expiry_date_required` · boolean.

**New dietary_tags available:** caffeine_free, bio, raw, chicory_based, clean_beauty, cruelty_free.
**Allergen "oats" added to the EU14 enum.**

**offers.json · new fields:**

- `contents.duration_type` · calendar | usage_days | servings.
- `contents.duration_servings` · number.
- `contents.cure_metadata` · cure_name, is_premade, target_concern, phases[]. Relevant: pre-built cures.
- `incentives.duration_tiers[]` · discount per engagement (1/3/6/12 months).
- `incentives.loyalty` · loyalty program (points, tiers, sign_up_bonus).
- `offer_groups[].offers[].tags[]` · free tags at offer level (v2 schema; legacy `offers[].tags[]` is v1.x).

**Automatic stamping:** each entity file carries its own `_version` field matching the schema it was built against. Current baseline (read live from `_TEMPLATE`): `brand.json _version=2.2`, `products/{slug}/spec.json _version=1.8`, `products/{slug}/offers.json _version=2.0`, `audiences/{slug}/profile.json _version=1.2`. After a fresh scaffold via `cp -r _TEMPLATE brands/{slug}`, these values are inherited automatically. Never hardcode version expectations · always read from `_TEMPLATE` first.

---

## Cross-references

- `docs/system/decomposition-visibility-doctrine.md` (NEW v2.78.2 · canon racine · v2.81.1+ NEW NIVEAU LIVE thinking aloud) · doctrine 3 phases temporelles · AVANT exec NIVEAU 0 paramètres décomposés · PENDANT exec NIVEAU LIVE thinking aloud expert (2 niveaux abstraction macro + micro many-to-many phrasé) · APRÈS exec NIVEAUX 1-4 matrices post-synthèse 5 sections IP (NIVEAU 1 décomposition produit specs · mécanismes · bénéfices 3 couches · NIVEAU 2 many-to-many matrix · NIVEAU 3 stage business filter · NIVEAU 4 méthode pédagogique verbale). Implémenté ici · NIVEAU LIVE section pré-Step 0 (v1.5.1) + Phase Output Decomposition Visibility Step 7b extend (v1.5.0). Sister skills consumers cohérents · `build-atlas-complete` + `profile-audience` + `define-specs` (tous patches v2.78.2 + v2.81.1+ parallèles).
- `docs/system/pain-benefit-chain.md` · canon 3 couches bénéfices · Functional (mesurable extérieur) · Emotional (ressenti subjectif) · Identity (projection identitaire). Consommé NIVEAU 1 décomposition produit Phase Decomposition Visibility v1.5.0.
- `docs/system/progressive-cartography-doctrine.md` (NEW v2.68) · Phase 1 Macro confirmation + Phase 2 Drilling autonome implémenté ici dans Steps 7a + 7b. Doctrine canon · drop questionnaire pre-action, drill-down autonome, gate light binaire entre phases. Sections 3-4 spécifient le contrat opérationnel des deux phases.
- `docs/system/territory-doctrine.md` (v2.67) · layer territoire pattern · snapshot-brand classified `layer: territoire` (cf frontmatter). Steps 1-6 scrape produisent substrat canonisé · spec.json + offers.json + profile.json draft. Steps 7a+7b livrent synthèse macro+drill autonome operator-facing sans corrompre cycle promotion canon.
- `docs/system/contextual-intelligence.md` (master doctrine) · "No questionnaire before action" canon · agent reasons not form-fills. Hard Rule "No Q&A premature on audience" enforce ce canon spécifique au layer audience.
- `docs/system/investigation-posture.md` (v2.54 doctrine canon) · cartographier avant affirmer · confidence chain explicit · drill-down macro = opérateur · 5 sections obligatoires Step 7b (Observé / Déduit / Inconnu / Leviers / Close ouvert).
- `docs/system/audience-cartography.md` · doctrinal contract Step 5 (4 movements audience).
- `docs/system/voice.md` · voice canon, register, banned phrases.
- `resources/templates/operator-fiche-output.md` · canonical template fiche output.
- `.skills/skills/mine-voc/SKILL.md` · downstream pour lever hypothèses audience confidence `TRÈS faible`.
- `.skills/skills/mine-vom/SKILL.md` · downstream pour lever inconnus vernacular marché + compétitif.
- `.skills/skills/produce-paid-angles/SKILL.md` · downstream pour produire angles avec confidence chain héritée audience + brand.
- `.skills/skills/map-audiences/SKILL.md` · downstream Phase 3 audiences (routé depuis Step 7b close ouvert "on attaque Phase 3 audiences ?").
- `.skills/skills/profile-audience/SKILL.md` · downstream Phase 3 audiences alt-route depuis Step 7b.
- `.skills/skills/build-atlas-complete/SKILL.md` · sister skill consumer patches parallèle v2.78.2 (Decomposition Visibility cohérent atlas pipeline).
- `.skills/skills/define-specs/SKILL.md` · sister skill consumer patches parallèle v2.78.2 (NIVEAU 1 décomposition produit cohérent specs production).
