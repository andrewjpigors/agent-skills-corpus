---
name: import-asset
type: orchestrator
recommended_model: sonnet
subagent_safe: true
operator_facing: true
isolation_scope: brand_only
layer: territoire
version: 1.2.0
mode: proposed
permissions:
  reads: [brand, product, visual_identity]
  writes: [visual_identity_sidecar, asset]
  mode: proposed
  subagent_safe: true
  bash_allowlist:
    - "python3"
    - "cp"
    - "mv"
    - "curl"
    - "grep"
    - "magick"
    - "convert"
  emits_events: [asset_imported, asset_validated_canonical, assets_extracted_from_url]
prerequisites:
  - field: brands/{slug}/brand.json
    level: L1
    auto_pull: read_brand_canonical
    freshness_ttl_days: 90
  - field: brands/{slug}/products/{slug}/visual_identity.json
    level: L1
    auto_pull: read_visual_identity_v12
    freshness_ttl_days: 90
  - field: asset_file_path
    level: L2
    options:
      - operator_drop_local_path
      - operator_provides_url_download
      - extract_from_url
  - field: asset_type
    level: L2
    options:
      - logo
      - badge
      - mascotte
      - pattern
      - packshot_variant
      - auto_multi
  - field: brand_url
    level: L2
    note: "required only if mode = extract_from_url. URL homepage OR product page brand."
description: >
  Orchestrator skill · import + tag + valide un asset brand (logo PNG haute-res, badge cert/claim,
  mascotte, pattern background, packshot variant) dans le slot canon visual_identity.assets_canonical
  schema v1.2. Pattern symétrique craft-packshot v1.1 mais SANS génération IA · les brands fournissent
  leurs assets en général (logo officiel, badges certif obtenus, mascotte design agency). Skill guide
  operator pour drop fichier local + tag asset_type + validation 5 critères qualité + persist sidecar
  visual_identity.json avec _validated_by_operator gate. Bridge downstream · compose-creative v1.3+
  HR3b layered multi-layer paste consume packshot + logo + badge en couches pour pubs studio
  photographer avec branding complet pixel-exact.
  FR: "importe un asset", "ajoute le logo brand", "ajoute un badge cert", "ajoute la mascotte", "ajoute un pattern background", "canonise un asset", "drop asset brand", "upload asset visuel".
  EN: "import an asset", "add brand logo", "add cert badge", "add mascotte", "add background pattern", "canonize an asset", "drop brand asset", "upload visual asset".
disambiguates_against:
  craft-packshot: "craft-packshot GÉNÈRE un packshot via fal.ai (besoin = brand n'a pas de photo studio). import-asset STORE un asset déjà fourni (logo SVG/PNG, badge cert PNG, mascotte). Si operator a juste besoin de stocker · import-asset. Si génération nécessaire · craft-packshot."
  define-specs: "define-specs encode visual_identity.json fields textuels (label, container, content, distinctive_features). import-asset peuple visual_identity.assets_canonical avec fichiers images."
  setup-brand: "setup-brand fait le scrape initial brand + populate brand.json. import-asset opère post-setup pour ajouter assets visuels canon."
consumes:
  - path: brands/{slug}/brand.json
    min_version: 2.0.0
    note: identity.language pour translation prompts, meta.sector pour applicability check
  - path: brands/{slug}/products/{slug}/visual_identity.json
    min_version: 1.2.0
    note: target sidecar pour write assets_canonical slots
  - path: resources/schemas/visual_identity.schema.json
    min_version: 1.2.0
produces_proposals_for:
  - brands/{slug}/asset-library/{asset_type}-{slug}-{date}.{ext}
  - brands/{slug}/products/{slug}/assets/{asset_type}-{slug}-{date}.{ext}
  - brands/{slug}/products/{slug}/visual_identity.json#assets_canonical.{slot}
---

# Skill: import-asset

> **Import + canonise un asset brand non-génératif.** v1.0.0 · v2.48 · orchestrator schema-driven · drop → tag → validate → persist canonical. Pattern symétrique craft-packshot mais sans génération IA. Bridge compose-creative v1.3+ layered multi-layer.

Orchestrator, pas générateur. Operator drop son fichier (logo officiel brand, badge cert obtenu, mascotte design, pattern background), skill tag le type + valide 5 critères qualité + persist dans le slot canon visual_identity.assets_canonical (schema v1.2). Pas de fal.ai call · les brands fournissent leurs assets en général. **Opérateur voit langage métier uniquement** · ex *"Logo brand validé, rangé dans tes assets. On peut le poser sur tes prochaines pubs."*. JAMAIS *"schema field consumed"*, *"JSON write_to_context"*, *"_canonical: true flag"*, *"layered paste downstream"*, *"slot peuplé v1.2"*.

## Tone

Posture assistante brand designer · pragma + accessible. Pas inspecteur, pas générateur. Output opérateur 6-8 lignes max · type detected (1 ligne), 5 critères table compacte, slot persist (1 ligne), gate validation explicite. Aucun jargon plumbing en surface. Si fichier source insuffisant (basse résolution, fond bruité, mauvais format), surface honnête langue opérateur ("ton logo est en JPG fond gris, idéalement PNG fond transparent · tu peux uploader une version cleaner ou je tag avec warning pour fallback") sans bloquer si operator insiste.

## Expert methodology

**Persona.** Brand designer + DAM (digital asset management) librarian + ingénieur compositing PIL. Sait qu'un asset canonisé brand-level (logo, badge, mascotte) est l'atome réutilisable cross-products + cross-pubs. Sait que parasites visuels (fond non-transparent, basse résolution, watermark résiduel) brûlent les composites downstream.

**Framework.** Workflow déterministe 6 steps · detect type → lookup target slot schema → file copy vers brand assets directory → quality assessment 5 critères → operator gate → persist sidecar visual_identity.json. Cohérent craft-packshot orchestrator pattern mais sans Step gen IA (skip fal.ai call).

**Pattern position pipeline.** craft-packshot CRÉE asset packshot (génération needed). import-asset STORE assets fournis (logo, badge, mascotte, pattern). compose-creative v1.3+ HR3b layered CONSUME les 2 types (packshot + logo + badge multi-layer paste).

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant import (Step 1), scanner prerequisites :

1. **L1 silent** · `brands/{slug}/brand.json` → extract `meta.sector`, `identity.language`, `identity.brand_personality`.
2. **L1 silent** · `brands/{slug}/products/{slug}/visual_identity.json` v1.2+ → check existing `assets_canonical` slots déjà peuplés (avoid overwrite sans gate explicite).
3. **L2 gate** · operator choice `asset_type` (1 question AskUserQuestion si pas explicite dans la requête initiale) ·
   - `logo` (brand-level, raster PNG complément SVG)
   - `badge` (cert plantes, made in France, vegan, bio, etc.)
   - `mascotte` (personnage récurrent brand, optionnel)
   - `pattern` (background répétitif, texture signature)
   - `packshot_variant` (angle additional · 3/4, back, top, lifestyle si craft-packshot pas applicable)
4. **L2 gate** · `asset_file_path` · operator drop chemin local OR URL download.

Output state map + asset_type selected + path resolved.

---

## HR1 · Detect asset type + variant (si applicable)

Map asset_type → schema slot canon v1.2 ·

| asset_type | Target slot | Variant key | Variant enum |
|---|---|---|---|
| `logo` | `assets_canonical.logo_canonical` | `variants[].name` | primary, monochrome_black, monochrome_white, horizontal, vertical, icon |
| `badge` | `assets_canonical.badge_canonical.{slug}` | slug-style libre | ex cert_plantes_naturelles, bio_eu, made_in_france, vegan_society |
| `mascotte` | `assets_canonical.mascotte_canonical` | `variants[].name` | libre (neutral, happy, pointing, holding_product) |
| `pattern` | `assets_canonical.pattern_canonical.{slug}` | slug-style libre | ex wave_pattern_primary, texture_natural_beige, gradient_brand_sunset |
| `packshot_variant` | `assets_canonical.packshot_3_4` ou `packshot_top` ou `packshot_lifestyle[N]` | angle param | front, back, 3_4, top, lifestyle |

Si asset_type ∈ {badge, pattern}, demander slug key au operator (1 question AskUserQuestion) avec exemples du schema v1.2.

Si asset_type ∈ {logo, mascotte} et schema slot déjà peuplé · demander operator gate · (a) override (overwrite + push old to variants[]), (b) ajouter comme variant supplémentaire, (c) cancel.

---

## HR2 · File handling + path canon

### Step 1 · File acquisition

Mode A · `operator_drop_local_path`
- Operator drop fichier local · skill lit path absolu.
- Verify file existe + readable.

Mode B · `operator_provides_url_download`
- Operator fournit URL externe pointant directement sur le fichier (Drive, Dropbox, CDN, etc.).
- `curl -sL {url} -o /tmp/import-asset/{filename}` download.
- Skill verify download success + non-empty file.

Mode C · `extract_from_url` (NEW v1.1)
- Operator fournit URL **page** brand (homepage OR product page), pas un fichier direct.
- Skill scrape la page + extract candidats multi-types automatiquement (logo + badges + payment_methods + patterns).
- Workflow détaillé HR7 ci-dessous.
- Pour `asset_type: auto_multi` (NEW v1.1) · skill itère sur tous les types détectés et propose chacun à operator.

### Step 2 · Path canon decision

Determine target path selon scope ·

**Brand-level scope (default pour logo, mascotte, pattern, certain badges)** ·
- Target · `brands/{slug}/asset-library/{asset_type}-{variant_or_slug}-{YYYYMMDD}.{ext}`
- Ex · `brands/glowco/asset-library/logo-primary-20260513.png`
- Ex · `brands/glowco/asset-library/badges/cert-plantes-naturelles-20260513.png`
- Ex · `brands/glowco/asset-library/mascotte-primary-20260513.png`
- Ex · `brands/glowco/asset-library/patterns/wave-primary-20260513.png`

**Product-level scope (override produit-spécifique, rare)** ·
- Target · `brands/{slug}/products/{slug}/assets/{asset_type}-override-{YYYYMMDD}.{ext}`
- Ex · `brands/glowco/products/cell-boost/assets/logo-override-20260513.png` (si SKU a un logo spécifique différent du brand-level)

Default · brand-level scope. Switch product-level si operator declare explicit "override pour ce produit" OR si visual_identity.json sidecar product déjà a un slot peuplé qui diverge brand-level.

### Step 3 · File copy + rename canonical

```bash
SOURCE_PATH={operator_drop_path}
TARGET_DIR="brands/{slug}/assets" # ou subdirectory selon type
TARGET_FILENAME="{asset_type}-{variant_or_slug}-{YYYYMMDD}.{ext}"
mkdir -p "${TARGET_DIR}"
cp "${SOURCE_PATH}" "${TARGET_DIR}/${TARGET_FILENAME}"
```

Note · `cp` pas `mv` · preserve source operator pour audit + rollback. Operator peut delete source après gate validation.

---

## HR3 · Quality assessment 5 critères

Pour chaque asset importé, table critère par critère ·

| # | Critère | Source check | Threshold |
|---|---|---|---|
| 1 | Resolution | PIL `Image.size` | Min 1024 dimension longue pour logo/badge · Min 512 pour pattern tile · Min 2048 pour packshot_variant |
| 2 | Format | File extension + PIL `Image.format` | png > webp > jpg (png prioritaire pour alpha) |
| 3 | Background | PIL pixel sampling 4 coins + center | transparent > white > neutral (lifestyle accepted pour packshot_lifestyle only) |
| 4 | Crispness | PIL `getextrema()` + edge detection | text sharpness + no compression artifacts (compression ratio JPEG check) |
| 5 | Content match | Visual inspection via Read tool multimodal | Asset visible correspond au type declared (ex logo declared = wordmark + icon visible · pas un packshot par erreur) |

Statuts · `pass` / `pass_partial` / `fail`. Critères 1-2 binaires (resolution above threshold = pass, format png/webp = pass). Critère 3 tolère `pass_partial` si background = white pure (#FFFFFF) au lieu de transparent (acceptable pour logo/badge mais pas optimal). Critère 4 tolère `pass_partial` si compression légère sur jpg. Critère 5 binaire.

Verdict global · `5/5 pass` = ready operator gate. `4/5 avec pass_partial` = ready avec warning explicite. `≤3/5 pass` = surface warnings + propose retry avec asset cleaner.

```python
from PIL import Image
import os

def quality_assess_5_criteria(file_path, asset_type, expected_variant=None):
    img = Image.open(file_path)
    width, height = img.size
    max_dim = max(width, height)
    fmt = img.format.lower()

    # Critère 1 · resolution
    thresholds = {
        "logo": 1024,
        "badge": 1024,
        "mascotte": 1024,
        "pattern": 512,
        "packshot_variant": 2048
    }
    threshold = thresholds.get(asset_type, 1024)
    res_status = "pass" if max_dim >= threshold else "fail"

    # Critère 2 · format
    fmt_status = "pass" if fmt in ("png", "webp") else "pass_partial" if fmt == "jpeg" else "fail"

    # Critère 3 · background (sampling 4 coins)
    img_rgba = img.convert("RGBA")
    corners = [
        img_rgba.getpixel((0, 0)),
        img_rgba.getpixel((width - 1, 0)),
        img_rgba.getpixel((0, height - 1)),
        img_rgba.getpixel((width - 1, height - 1))
    ]
    is_transparent = all(px[3] < 10 for px in corners)
    is_white = all(px[0] > 245 and px[1] > 245 and px[2] > 245 for px in corners)
    if is_transparent:
        bg_status, bg_value = "pass", "transparent"
    elif is_white:
        bg_status, bg_value = "pass_partial", "white"
    else:
        bg_status, bg_value = "fail" if asset_type != "pattern" else "pass", "neutral_or_lifestyle"

    # Critère 4 · crispness (extrema + jpeg artifacts)
    extrema = img.getextrema()
    has_dynamic_range = all(channel[1] - channel[0] > 100 for channel in (extrema if isinstance(extrema[0], tuple) else [extrema]))
    crisp_status = "pass" if has_dynamic_range else "pass_partial"

    # Critère 5 · content match · marquer pending pour Read tool multimodal inspection downstream
    content_status = "pending_operator_inspection"

    return {
        "resolution": {"status": res_status, "value": f"{width}x{height}"},
        "format": {"status": fmt_status, "value": fmt},
        "background": {"status": bg_status, "value": bg_value},
        "crispness": {"status": crisp_status},
        "content_match": {"status": content_status, "note": "operator visual gate Step 5"}
    }
```

---

## HR4 · Operator validation gate (CRITIQUE · BLOCKER canon)

Surface à l'opérateur en langage clair, zéro jargon plumbing ·

```
═══════════════════════════════════════════════════════════════
{BRAND} · Asset récupéré · {label_humain_asset}
═══════════════════════════════════════════════════════════════
{date}

Source · {operator_drop_path or download_url}
Rangé dans · {target_path_relative}

Check qualité ·
  1. Résolution      {width}x{height} · {ok | acceptable | insuffisant}
  2. Format          {png/webp/jpg} · {ok | acceptable | insuffisant}
  3. Fond            {transparent / blanc / décor} · {ok | acceptable | insuffisant}
  4. Netteté         {ok | acceptable}
  5. Contenu         à vérifier visuellement · ouvre {target_path}

  Verdict · {N}/5

  Note · {1-2 lignes si applicable · ex "fond blanc au lieu transparent · ça marche pour collage layered, on auto-détourera"}

───────────────────────────────────────────────────────────────
À toi de valider
───────────────────────────────────────────────────────────────
(a) Validé · marqué comme version officielle réutilisable
(b) Je re-upload une version plus propre (résolution + haute / fond transparent)
(c) Annule
```

`{label_humain_asset}` mapping interne → operator ·
- `logo` → `Logo brand`
- `badge` (avec slug) → `Badge "{claim_text_humain}"` (ex `Badge "100% Plantes Naturelles"`)
- `mascotte` → `Mascotte`
- `pattern` (avec slug) → `Texture / fond "{slug_humain}"` (ex `Texture "vague primary"`)
- `packshot_variant` → `Vue produit additionnelle ({angle_humain})` (ex `Vue produit additionnelle (3/4 perspective)`)

JAMAIS auto-flag canonical sans réponse opérateur explicite (cohérent craft-packshot HR2). JAMAIS exposer field_path, flags techniques, ou nommer le skill en surface operator.

---

## HR5 · Persist visual_identity.json sidecar update

Si Step 4 validé option (a) ·

**Mutation gate decision.** `visual_identity.json` est sidecar (pas core entity dans les 6 core entities canon · brand/product spec/offers/audience profile/learnings/strategy). Edit direct via Write/Edit accepté pour sidecar (cohérent craft-packshot v1.1 convention v2.44).

**Update fields selon asset_type** ·

### asset_type = logo

```json
{
  "assets_canonical": {
    "logo_canonical": {
      "path": "assets/logo-primary-20260513.png",
      "resolution": "2048x512",
      "format": "png",
      "background": "transparent",
      "variants": [
        {"name": "primary", "path": "assets/logo-primary-20260513.png", "resolution": "2048x512"}
      ],
      "_canonical": true,
      "_validated_by_operator": true,
      "_validated_at": "2026-05-13",
      "_imported_via": "import-asset/1.0.0"
    }
  }
}
```

### asset_type = badge

```json
{
  "assets_canonical": {
    "badge_canonical": {
      "cert_plantes_naturelles": {
        "path": "assets/badges/cert-plantes-naturelles-20260513.png",
        "resolution": "1024x1024",
        "format": "png",
        "background": "transparent",
        "claim_text": "100% Plantes Naturelles",
        "regulatory_authority": null,
        "_canonical": true,
        "_validated_by_operator": true,
        "_validated_at": "2026-05-13",
        "_imported_via": "import-asset/1.0.0"
      }
    }
  }
}
```

### asset_type = mascotte

```json
{
  "assets_canonical": {
    "mascotte_canonical": {
      "path": "assets/mascotte-primary-20260513.png",
      "resolution": "1024x1024",
      "format": "png",
      "background": "transparent",
      "_canonical": true,
      "_validated_by_operator": true,
      "_validated_at": "2026-05-13",
      "_imported_via": "import-asset/1.0.0"
    }
  }
}
```

### asset_type = pattern

```json
{
  "assets_canonical": {
    "pattern_canonical": {
      "wave_pattern_primary": {
        "path": "assets/patterns/wave-primary-20260513.png",
        "resolution": "2048x2048",
        "format": "png",
        "tile_repeat": true,
        "dominant_color_hex": "#A3D9B1",
        "_canonical": true,
        "_validated_by_operator": true,
        "_validated_at": "2026-05-13",
        "_imported_via": "import-asset/1.0.0"
      }
    }
  }
}
```

### asset_type = packshot_variant

Mêmes fields que craft-packshot v1.1 Step 6 (packshot_3_4, packshot_top, packshot_lifestyle[N]).

Merge logic · si slot existe déjà, push old entry to `_history[]` array (audit trail), write new entry as canonical current.

### Step 5bis · Trigger validate-resources silently post-write (v2.51 NEW)

Après HR5 persist visual_identity.json sidecar update, trigger `validate-resources` silencieusement sur la brand · même pattern que compose-creative + snapshot-brand + craft-packshot post-mutation.

```bash
# Silent validation pass
python3 .skills/build-brand-snapshot.py {brand_slug}
# validate-resources via Task tool (subagent_safe: true permet inline)
```

Flag MAJOR/CRITICAL à l'opérateur si remonte. Sinon silent. Cohérent doctrine root CLAUDE.md ligne 168 *"ALWAYS after any write under brands/{slug}/custom/ or {entity}.extensions.json : trigger validate-resources on that brand silently."* Évite drift schema sidecar silencieux post-mutation.

---

## HR7 · Mode C extract_from_url workflow (NEW v1.1)

Activé si Mode C `extract_from_url` choisi en Step 0bis L2 gate · operator fournit URL page brand au lieu de fichier direct. Skill auto-extract multi-candidats logo + badges + payment_methods + patterns en 4 sub-steps.

### Step C.1 · Scrape page HTML

```bash
SCRAPE_DIR="/tmp/import-asset/extract-{brand_slug}-{date}"
mkdir -p "${SCRAPE_DIR}"
curl -sL "${BRAND_URL}" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36" \
  -o "${SCRAPE_DIR}/page.html"
```

Verify file non-empty + content-type HTML. Si page protected (Cloudflare challenge, login wall), surface honnête operator + suggest Mode A drop manuel.

### Step C.2 · Extract candidats par type via heuristics

**Heuristics validées S55 fincutmen.com stress test (Shopify Hydrogen oxygen-v2 theme)** ·

| Asset type | Heuristics path/class/alt | Threshold acceptance |
|---|---|---|
| `logo` | path contains `/logo` OR `_logo` OR class=`logo` OR alt=`logo` | Format SVG > PNG > WEBP. SVG vectoriel prioritaire. |
| `badge_trust` | path contains `trustpilot`, `trustbadge`, `trust_pilot`, `stars-`, `rating-` | Third-party trust badges. Stocker dans badge_canonical sous slug semantic (trustpilot_wordmark, trustpilot_stars_5). |
| `badge_cert` | path/alt contains `cert`, `certif`, `approved`, `guarantee`, `garanti`, `vegan`, `organic`, `bio`, `eco_`, `cruelty_free` | Cert / authority badges. |
| `badge_origin` | path/alt contains `made_in_`, `origine_`, `francais`, `french`, `fab_` | Origin / Made in X badges. **Caveat · path token suggère semantique pas garantie · operator visual gate Step 5 BLOCKER (banner_francais.png false-positive fincutmen test · pattern path match `francais` mais image = banner hero produits pas badge Made in France).** |
| `payment_method` | path contains `payment`, `payments_method`, `stripe`, `visa`, `mastercard`, `paypal`, `apple_pay`, `google_pay` | Payment footer methods. Stocker dans pattern_canonical OR badge_canonical selon usage downstream. |
| `pattern` | path contains `pattern`, `texture`, `bg_`, `background_`, `hero_`, banner_ | Hero backgrounds + textures. Operator gate aggressif (souvent false-positives). |

```bash
# Extract all image references depuis HTML
grep -oiE '(src|data-src)="[^"]+\.(png|webp|jpg|jpeg|svg)[^"]*"' "${SCRAPE_DIR}/page.html" | \
  sort -u > "${SCRAPE_DIR}/all_images.txt"

# Extract class="*logo*" refs pour debugging (souvent CSS class indique role)
grep -oE 'class="[^"]*logo[^"]*"' "${SCRAPE_DIR}/page.html" | sort -u > "${SCRAPE_DIR}/logo_classes.txt"

# Extract alt="*" attributes
grep -oiE 'alt="[^"]+"' "${SCRAPE_DIR}/page.html" | sort -u > "${SCRAPE_DIR}/alt_texts.txt"
```

```python
# Filter par heuristics
import re

heuristics = {
    "logo": [r"/logo", r"_logo", r"logo_", r"alt=\"logo"],
    "badge_trust": [r"trustpilot", r"trustbadge", r"trust_pilot", r"stars-", r"rating-"],
    "badge_cert": [r"\bcert\b", r"certif", r"approved", r"guarantee", r"garanti", r"vegan", r"organic", r"\bbio\b", r"eco_", r"cruelty_free"],
    "badge_origin": [r"made_in_", r"origine_", r"francais", r"french", r"fab_"],
    "payment_method": [r"payment", r"payments_method", r"stripe", r"\bvisa\b", r"mastercard", r"paypal", r"apple_pay", r"google_pay"],
    "pattern": [r"\bpattern", r"texture", r"\bbg_", r"background_", r"hero_", r"banner_"]
}

candidates_by_type = {t: [] for t in heuristics}
with open(f"{SCRAPE_DIR}/all_images.txt") as f:
    urls = [line.strip() for line in f]

for url in urls:
    for asset_type, patterns in heuristics.items():
        if any(re.search(p, url, re.IGNORECASE) for p in patterns):
            candidates_by_type[asset_type].append(url)
            break  # 1 type par image priority order
```

### Step C.3 · Download candidats + rasterize SVG si applicable

```bash
for url_line in $(cat "${SCRAPE_DIR}/candidates_filtered.txt"); do
  # Resolve URL · src "/path" → "${BRAND_URL_BASE}/path", absolute keep as-is
  filename=$(basename "${url_line}" | sed 's/?.*//')
  curl -sL "${url_resolved}" -o "${SCRAPE_DIR}/candidates/${filename}"
done

# Rasterize SVG to PNG for visual inspection via Read tool
for svg in "${SCRAPE_DIR}/candidates/"*.svg; do
  output="${svg%.svg}_render.png"
  magick "${svg}" -resize 600x "${output}"
done
```

**SVG rasterizer fallback chain** ·
1. `magick file.svg -resize 600x output.png` (ImageMagick · validé fincutmen test macOS)
2. Si magick fail · `convert file.svg -resize 600x output.png` (legacy ImageMagick)
3. Si les 2 fail · Python cairosvg (peut OSError no libcairo macOS · seulement Linux/CI typically)
4. Fallback ultime · operator inspect SVG code directement (text-based, lisible)

### Step C.4 · Present candidats à operator pour gate validation

Render fiche operator-facing en plain prose, zéro headers cap-lock catégoriques. L'agent fait le job de catégorisation, présente le résultat ·

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Récupération assets depuis ton site
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD} · scan de {brand_url}

J'ai trouvé sur ton site ·
  · {N_logo} version(s) de ton logo
  · {N_badge_trust} badge(s) tiers de confiance (Trustpilot, etc.)
  · {N_badge_cert} badge(s) de certification (vegan, bio, cruelty-free, etc.)
  · {N_badge_origin} badge(s) d'origine (Made in France, etc.) · ⚠️ vérifie l'aperçu, faux-positif possible
  · {N_payment} logo(s) de méthodes de paiement
  · {N_pattern} fond(s) ou texture(s) (rare, souvent décor)

Aperçus disponibles · open {render_dir}

On les passe en revue ?

───────────────────────────────────────────────────────────────
À toi de valider, élément par élément
───────────────────────────────────────────────────────────────
Pour chaque ·
(a) Valide · je le range comme version officielle
(b) Rejette · faux-positif, je l'ignore
(c) Mauvais type · dis-moi lequel il devrait être (logo / badge / autre)
(d) Skip celui-là, on passe au suivant
```

Operator inspect Preview macOS chaque candidat (`open {render_path}`), valide chacun individuellement, skill range chaque asset dans le bon slot. Drop un type si count=0 (pas de ligne vide).

**Auto-rasterize PNG aperçu** fournis pour SVG candidats · sinon operator doit ouvrir SVG dans navigateur (lourd). Pour PNG/WEBP/JPG direct · `open {path}` Preview.

**Anti-pattern UX** · jamais nommer le skill (`import-asset`, `Mode C extract_from_url`) en prose operator. Jamais exposer `asset_type` enum interne (`packshot_variant`, `auto_multi`). Jamais surfacer flags techniques (`_validated_by_operator`, `_canonical`). Operator voit langage métier · "valide", "rejette", "logo", "badge", "fond".

### Bridge optionnel post-setup brand

Si operator vient de run `snapshot-brand` (qui a scrapé `brand.identity.website` + populate brand.json) et brand_assets sont vides (aucun logo/badge canonisé), `snapshot-brand` peut suggérer en fin de session, posture facultative ·

> *"Setup terminé sur {brand}. Si tu veux, je peux aussi récupérer le logo et les badges depuis ton site."*

Posture · facultative, soft offer. Jamais pushy. Operator dit oui explicit OU pas, agent passe à autre chose sans relance. Aucun nom de skill mentionné en prose operator-facing. Pas d'auto-execute silencieux.

---

## HR6 · No orphan output

Operator-facing summary final, langage métier zéro jargon technique ·

- Confirmer asset rangé · "{label_humain_asset} validé, rangé dans tes assets brand. Aperçu · `open {path}`".
- 1 reco contextuelle douce (jamais pushy) ·
  - Si logo importé → *"Si tu veux, on peut tester une pub avec ce logo + ton packshot existant."*
  - Si badge importé → *"On peut le placer en haut à gauche sur une pub test si tu veux."*
  - Si pattern importé → *"Si tu veux, on peut tester ce fond comme background sur une pub."*
  - Si premier asset brand importé (logo seul) → *"Tu as ton logo en place. Si pertinent, on peut aussi récupérer un badge (cert, vegan, etc.) ou une mascotte."*
  - Si tous types peuplés → *"Tes assets brand sont au complet. On peut lancer une pub test avec packshot + logo + badge en couches si tu veux."*

**Anti-pattern UX prose operator** ·
- JAMAIS nommer le skill destination (`compose-creative`, `HR3b layered`, `Step 3b.1`)
- JAMAIS nommer concepts internes (`slot`, `schema v1.2`, `pipeline`, `multi-layer paste`)
- JAMAIS push (formule "tu peux faire X, Y, Z. Tape la commande Z" = anti-pattern)
- TOUJOURS soft offer ("si tu veux", "si pertinent")
- TOUJOURS 1 reco max, pas menu

**No orphan close.** Pas de "Done. Want anything else?". Pas de menu hardcoded.

---

## Hard Rules récap

| HR | Règle | Type |
|---|---|---|
| HR1 | Detect asset_type + map slot schema v1.2 (logo/badge/mascotte/pattern/packshot_variant/auto_multi) | BLOCKER |
| HR2 | File handling · cp source preserve + canonical rename + brand-level vs product-level scope · Mode A/B/C input acquisition | CANON |
| HR3 | Quality assessment 5 critères (resolution + format + background + crispness + content match) | CANON |
| HR4 | Operator validation gate explicit avant _canonical: true (cohérent craft-packshot HR2) | BLOCKER |
| HR5 | Persist visual_identity.json sidecar via Write/Edit (sidecar mutation convention v2.44) | CANON |
| HR6 | No orphan output · 1 reco actionnable forte contextuelle downstream | BLOCKER |
| HR7 | Mode C extract_from_url 4 sub-steps · scrape HTML + extract candidats heuristics par type + download + rasterize SVG + present operator gate (v1.1+) | CANON |

---

## Edge cases

- **Operator drop dossier au lieu de fichier.** Bulk import · skill itère sur fichiers du dossier, demande asset_type pour chacun (ou batch tag si pattern naming uniform).
- **URL externe download fail.** curl rate limit ou 404 · surface honnête + propose Mode A (drop local).
- **Asset existe déjà avec même slug/variant.** Demande operator gate (override + push old to `_history[]`, OR ajouter variant suffix, OR cancel).
- **Fichier corrupted ou non-image.** PIL `Image.open()` raise · surface honnête + suggest re-download ou re-export depuis source authority.
- **Resolution under threshold.** Continue avec warning · flag `_low_resolution_acceptable_per_operator: true` si operator insiste. Layered composite peut quand même utiliser, juste qualité dégradée.
- **Format jpg pour logo/badge.** Accept comme `pass_partial` · suggest re-export PNG transparent si dispo pour optimal layered (jpg loss + no alpha = artifacts sur dark backgrounds).
- **Background non-transparent ni white pur.** Pour logo/badge · flag warning. PIL threshold-to-alpha automatic dans compose-creative HR3b Step 3b.3 peut traiter mais résultat dégradé.

---

## Operator output template

### Fiche operator-facing template (canonique v2.51)

Réf canonique · `resources/templates/operator-fiche-output.md`. Header plain language, body en vocabulaire métier, footer soft offer 1 ligne max.

```
═══════════════════════════════════════════════════════════════
{BRAND_HUMAIN} · Asset ajouté · {label_humain_asset}
═══════════════════════════════════════════════════════════════
{date YYYY-MM-DD} · rangé dans tes assets brand, prêt pour réutilisation sur tes pubs

Source     {operator_drop_path or download_url}
Rangé dans {target_path_relative}
Format     {png/webp/jpg} · {width}x{height}

Check qualité ·
  1. Résolution      {WxH} (min {threshold}) · {ok | acceptable | insuffisant}
  2. Format          {png/webp/jpg} · {ok | acceptable | insuffisant}
  3. Fond            {transparent / blanc / décor} · {ok | acceptable | insuffisant}
  4. Netteté         {ok | acceptable}
  5. Contenu         à vérifier visuellement · ouvre Preview

  Verdict · {N}/5

  Note · {1-2 lignes si applicable}

───────────────────────────────────────────────────────────────
À toi de valider
───────────────────────────────────────────────────────────────
(a) Validé · marqué comme version officielle réutilisable
(b) Je re-upload une version plus propre (résolution + haute, fond transparent)
(c) Annule

───────────────────────────────────────────────────────────────
{1 reco soft offer 1 ligne max, langage métier · ex "Si tu veux, on peut tester une pub avec ce logo + ta photo officielle du produit."}
```

**Backstage (visual_identity.json sidecar, NON rendu operator)** · `assets_canonical.{slot}._canonical: true`, `_validated_by_operator: true`, `_validated_at`, `_imported_via`, `_history[]`. Vivent dans le JSON pour audit + retrieval programmatique · operator ne les voit jamais.

`{label_humain_asset}` mappings ·
- `logo` → `Logo brand`
- `badge` → `Badge "{claim_text_humain}"` (ex `Badge "100% Plantes Naturelles"`)
- `mascotte` → `Mascotte`
- `pattern` → `Fond / texture "{slug_humain}"`
- `packshot_variant` → `Vue produit additionnelle ({angle_humain})`

---

## Cross-refs

- Schema cible : `resources/schemas/visual_identity.schema.json` v1.2.0 (v2.48 multi-asset extension).
- Sibling skills : `craft-packshot` v1.1+ (génération packshot upstream · pattern symétrique avec gen IA · Mode A scrape carousel adjacent à HR7 Mode C scrape page), `snapshot-brand` v2.X+ (scrape page brand pour text claims · bridge auto-chain Mode C optionnel post-snapshot pour assets visuels), `compose-creative` v1.3+ (consumer downstream HR3b layered multi-layer paste packshot + logo + badge), `compose-overlay-text` v2.43+ (PIL composite logo SVG · complémentaire avec import-asset logo_canonical PNG raster), `define-specs` (encode visual_identity fields textuels · import-asset peuple champs images).
- Doctrines : `docs/system/contextual-intelligence.md` (operator-facing rule absolue), `docs/system/schema-encoding-doctrine.md` (substrate canon SED · schema-driven obligatoire HR1), `docs/system/visual-identity-doctrine.md` v2.43+ (canonical assets + wordmark_pattern · v2.48 multi-types extension).
- Memory : feedback `extend_before_create` (skills générique pattern operator vs personal hardcode).
- Stress test S55 v1.1 · fincutmen.com Shopify Hydrogen oxygen-v2 theme · 6 candidats extraits validés workflow Mode C (2 logos brand SVG variants primary+white via path `/oxygen-v2/.../assets/logo_*.svg` + Trustpilot wordmark+stars via `/images/stars_trustpilot/` + payment_methods footer SVG + banner hero false-positive rejected via operator visual gate Step 5). Pattern heuristics path/class/alt validé + rasterize SVG ImageMagick fallback chain (cairosvg OSError macOS native lib).
