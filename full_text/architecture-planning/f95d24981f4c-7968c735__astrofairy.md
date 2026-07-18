---
name: astrofairy
description: >
  Investigate how to access and use public astronomical survey/archive data
  for a specified observer task. The skill supports both Survey Mode
  (given a survey/release, explain how to use it) and Position Mode
  (given a coordinate/object, summarize useful survey/archive coverage and
  observation availability across major data services). Use when user asks
  about survey coverage, archive data access, telescope data products,
  image cutout/download, PSF/mask/variance, proposal/program checking,
  multi-wavelength data inventory, or observation availability at a sky coordinate.
license: MIT
compatibility: >
  Designed for Hermes Agent. Requires terminal, file (write/patch),
  and browser tools. Needs curl for API access and python3 for
  astroquery/pyvo (optional). Can be adapted for Claude Code (CLAUDE.md),
  OpenAI Codex (.codex.md), or any agent that accepts markdown instruction files.
metadata:
  version: "0.3"
  author: DenekoW
  repository: https://github.com/DenekoW/AstroFairy
---

# AstroFairy

Observer-oriented research protocol for public astronomical survey/archive data access.
The agent should investigate current official documentation rather than rely on a static survey database.

Version: 0.3

## Modes

### Survey Mode
**Purpose**: Given a survey or release, investigate its public data products, access routes, programmatic interfaces, caveats, and recommended observer workflow.

**Input**: survey, release, desired_products, science_case

**Output**: Survey Access Report

### Position Mode
**Purpose**: Given a coordinate or object name, summarize useful survey/archive coverage and observation availability across major data services, filtered by the user's science case. This mode should avoid returning an unfiltered list of all catalog hits.

**Input required**: coordinate_or_object_name

**Input optional**: radius, science_case, priority_surveys, wavelength_range, required_products, output_format

**Output**: Coordinate Data Inventory Report

**Sub-mode — Proposal Check**: Given a coordinate/object name + aliases, check whether relevant approved observing programs, scheduled/planned observations, executed observations, proprietary data, or public archive products exist. Triggered when user mentions proposal, program ID, "有没有 proposal", "被 JWST/HST/ALMA 覆盖" etc. See `## Proposal Check Protocol` below.

## Trigger Conditions

Load this skill when user asks:
- "Does a survey/release cover my target or field?"
- "How do I query a survey catalog?"
- "How do I download images or cutouts?"
- "Can I get PSF, mask, variance, weight maps, or sky products?"
- "Which release/data product should I use?"
- "Is this survey suitable for my science case?"
- "What is the best programmatic access route?"
- "Compare surveys for a specific observer task."
- "Given this coordinate, what survey/archive data are available?"
- "What observations exist at this sky position?"
- "Which surveys cover this coordinate?"
- "Summarize useful data around this RA/Dec."
- "Check MAST/IRSA/CDS/NED/major surveys for this position."
- "Filter coordinate-search results by usefulness for my science case."
- "Is there an approved JWST/HST/ALMA proposal covering this target?"
- "有没有 proposal / 有没有被 JWST 观测 / 有没有已批准项目"
- "Check if this target has proprietary or planned observations."
- "What JWST programs target this object or field?"
- "Check Subaru/HSC proposals for this target."
- "有没有 HSC/Subaru proposal / 有没有被 Subaru 观测"
- "Check Keck proposals for this target."
- "有没有 Keck proposal / KOA archive for this target"

## Input Parsing

### Required or Inferred
- survey
- release
- task_type
- desired_products
- science_case

### Optional
- target_ra_dec
- radius
- object_name
- field_name
- object_list
- filters
- depth_requirement
- resolution_requirement
- output_format

### Task Types
- coverage
- catalog_query
- image_cutout
- psf_mask_variance_access
- release_status
- science_case_suitability
- programmatic_access
- cross_survey_comparison
- batch_download
- position_data_inventory
- proposal_check

### Position Mode Input Parsing

**Default search radii:**
- Point source: 10 arcsec
- Galaxy or extended source: 30–120 arcsec (depending on apparent size)
- Cluster or large structure: 5–30 arcmin (depending on science case)

**Default services to check:**
- CDS SIMBAD — object identity, aliases, object type, redshift, bibliography
- CDS VizieR — published catalog tables near the coordinate
- CDS Aladin/HiPS — visual inspection of multi-survey sky images
- NED — extragalactic identity, redshift, photometry, cross-IDs
- MAST — UV/optical/NIR space-based obs (HST, JWST, GALEX, TESS, Kepler/K2)
- IRSA — IR all-sky products (WISE, unWISE, 2MASS, Spitzer) + SPHEREx QR2
- SPHEREx QR2 — all-sky NIR spectroscopy (0.75–5.0 μm, R~40–130); check via IRSA/SIA v2
- ESA ESASky — cross-mission discovery and footprint inspection
- Chandra Archive — high-resolution X-ray
- XMM-Newton Archive — X-ray observations and source products
- ALMA Archive (if relevant) — mm/sub-mm
- Major optical imaging surveys (HSC-SSP, DESI-LS, SDSS, Pan-STARRS, DES, Euclid/LSST if public)

**Service purpose summary:**

| Service | Purpose |
|---|---|
| CDS SIMBAD | Object identity, aliases, object type, redshift, bibliography, basic measurements |
| CDS VizieR | Published catalog tables and value-added catalogs near the coordinate |
| CDS Aladin/HiPS | Visual inspection of multi-survey sky images and overlays |
| NED | Extragalactic object identity, redshift, photometry, literature cross-IDs |
| MAST | UV/optical/NIR space-based obs and HLSPs (HST, JWST, GALEX, TESS, Kepler/K2) |
| IRSA | IR all-sky products (WISE, unWISE, 2MASS, Spitzer, Herschel-related) + SPHEREx QR2 |
| SPHEREx QR2 | All-sky NIR spectroscopy 0.75–5.0 μm, R~40–130; 6.2" pixels; DOIs: QR2=10.26131/IRSA652 |
| ESA ESASky | Cross-mission observation discovery and footprint inspection |
| Chandra Archive | High-resolution X-ray observations |
| XMM-Newton Archive | X-ray observations and source products |
| ALMA Archive | mm/sub-mm (when relevant to science case) |

**Coverage verification levels:**

Use this three-tier system in the multi-wavelength summary table:

| Symbol | Meaning | When to use |
|---|---|---|
| ✅ | Covered | (a) s_region polygon verified for individual exposures, OR (b) published survey footprint map confirms this coordinate falls within the imaged area |
| ❌ | Confirmed gap | s_region verified that individual exposures miss; or documented detector/chip gap at this exact position |
| ⚠️ | Catalog-level only | A catalog entry exists near this coordinate, but no corresponding image product is available (e.g.value-added catalogs without imaging) |

Rules:
- **Do NOT downgrade survey-level coverage to "⚠️" just because individual exposures were not footprint-verified.** If a survey's published footprint map covers the COSMOS field and this coordinate is in the COSMOS field, it's ✅.
- **Do NOT use "likely" without citing a source.** If uncertain, state what is known and what is not.
- For dedicated deep fields (COSMOS, GOODS, EGS, etc.): assume continuous survey products (Spitzer, Herschel, HSC, Chandra, XMM, VLA) cover the entire field unless documented gaps exist.
- For HST/JWST: individual exposures must be s_region verified because detector gaps and mosaic seams are real.
- For wide-area ground surveys (DESI-LS, SDSS, PS1): check the survey's public footprint map; if the coordinate is inside, mark ✅.
- Always cite the survey paper that defines the footprint and depth.
- Depth source: always cite a specific paper reference (author+year+journal).

**Ranking rules:**

High priority:
- Survey-level imaging products
- Archive observation products
- Spectra of the target
- UV/optical/IR/X-ray/radio data relevant to science case
- Products with image cutout or download access
- Products with PSF/mask/variance when image modeling is needed
- Object-targeted observations from space-based archives
- Major all-sky or wide-area surveys relevant to science case

Medium priority:
- Major value-added catalogs
- Photoz or specz catalogs
- Object cross-identification databases
- Literature tables directly targeting the object or field
- Environmental or group/cluster catalogs when relevant

Low priority by default:
- Generic foreground star catalogs
- Proper motion catalogs (unless needed)
- Astrometric catalogs (unless needed)
- Unrelated small catalogs from nearby fields
- Duplicate crossmatch tables
- Catalogs for a different object class than the science case

**Science-case sorting:**

Galaxy SED / photometry:
- Prioritize: UV from GALEX/MAST, optical imaging and catalogs, NIR/MIR from IRSA, reliable spectroscopic redshift, broad-band photometry catalogs
- Deprioritize: unrelated field catalogs, proper motion catalogs

Spectroscopy / redshift:
- Prioritize: spectra of target, spectroscopic redshift catalogs, SDSS/DESI/GAMA/6dF, NED and SIMBAD redshift records
- Deprioritize: imaging-only products (unless needed for context)

Time domain:
- Prioritize: TESS, Kepler, K2, ZTF/other time-domain surveys, epoch-level or lightcurve products
- Deprioritize: static catalogs without epoch information

X-ray / AGN:
- Prioritize: Chandra, XMM-Newton, eROSITA (if public), radio surveys, WISE mid-IR, optical spectroscopy
- Deprioritize: unrelated optical-only catalog hits

**Position mode caveats:**
- Footprint coverage does not guarantee useful depth
- Catalog detection does not guarantee image-level data availability
- Archive observations near the coordinate may miss the target (detector gaps, edges, chip layout, roll angle)
- Extended galaxies require a larger search radius than point sources
- image-level products with PSF, masks, variance/weight maps, sky/background
- Do NOT return an unfiltered CDS/VizieR-style catalog dump; rank and summarize by observer usefulness
- If results are too numerous, collapse low-priority catalogs into a deprioritized section
- **CRITICAL**: A coordinate usually corresponds to a specific astronomical object. Verify that data products actually cover the EXACT coordinate, not just fall within the search cone. 'Present in search radius' ≠ 'covers this target'. Check s_region/footprint for each observation.

**Deep field recognition (critical for Position Mode):**
- If SIMBAD returns >200 objects within 2 arcmin, check catalog names against `references/famous-deep-fields.md`
- **COSMOS field**: catalog names like COSMOS2020, COSMOS2015, COSMOS 06XXXXX, zCOSMOS, UVISTA
- **HUDF**: HUDF, UDF, XDF catalog names
- **GOODS**: GOODS-N, GOODS-S, HDF-N catalog names
- **If a famous field is identified**: skip generic IRSA/WISE/Chandra cone searches (they will overflow or return redundant data). Instead, go directly to field-specific master catalogs (COSMOS2020 VizieR, 3D-HST, C-COSMOS source catalog, etc.) and skip redundant multi-service queries.
- **If NOT a famous field**: proceed with the standard multi-service Position Mode search.

## Proposal Check Protocol

**Purpose**: Given a coordinate, object name, alias list, or target list, check whether relevant approved observing programs, scheduled/planned observations, executed observations, proprietary data, or public archive products exist. This is a program-level extension of Position Mode.

**Scope by confidence**:
- High confidence: JWST, HST (MAST missions with structured observation metadata), Subaru/HSC (NAOJ per-semester accepted proposals list, publicly available)
- Medium confidence: ALMA, Chandra, XMM-Newton, ESO/NOIRLab archives, Keck (public schedule + KOA archive; no structured per-semester accepted proposals page like Subaru)
- Low confidence / manual: facilities without structured public program search

**Default facilities to check**: JWST, HST, Subaru/HSC, MAST, ALMA (if mm/sub-mm relevance), Keck (if optical/NIR relevance), Chandra (if X-ray relevance), XMM-Newton (if X-ray relevance)

### JWST Proposal Check

JWST is the highest-priority target for proposal checking. Official sources:

| Source | URL | Role |
|---|---|---|
| STScI Approved Programs | `https://www.stsci.edu/jwst/science-execution/approved-programs` | Official list of approved JWST programs by cycle/type |
| STScI Program Information | `https://www.stsci.edu/jwst/science-execution/program-information` | Official program lookup by ID |
| MAST JWST Archive | `https://archive.stsci.edu/missions-and-data/jwst` | Observation metadata and data products |
| ESA JWST Science Archive | ESA archive | Alternative route for European programs |

**Third-party helper**: `https://jwst-search.zhechenghu.com/`

| Property | Detail |
|---|---|
| **Role** | Fast discovery tool for public approved JWST proposal text, target names, abstracts, descriptions, and observation tables |
| **Use for** | Target name search, alias search, proposal keyword search, object list cross-match, candidate program discovery |
| **Limitations** | Not authoritative for execution status; not authoritative for data public status; not sufficient for exact detector footprint containment; extracted from public proposal documents — parsing errors possible |
| **Availability** | Requires a browser (client-side React SPA). In Docker containers or headless environments where no browser is installed, skip this tool and use fallbacks: (1) STScI Approved Programs page grep, (2) arXiv literature search, (3) MAST Name.Lookup + Observations query. See `references/jwst-proposal-check.md` for detailed fallback workflows. |
| **Verification rule** | Treat matches as **candidate** proposal coverage. Verify program status, observation execution, public/proprietary state, data products, and exact spatial coverage using MAST, STScI program information, or ESA JWST Archive. |
| **Fallback: arXiv literature** | When the JWST search tool is unavailable (no browser), search arXiv for `"TOI-XXX" + "JWST"` or `"target_name" + "JWST"` to find papers discussing JWST observations. This confirms observation existence but does NOT provide program IDs. |
| **Verification rule** | Treat matches as **candidate** proposal coverage. Verify program status, observation execution, public/proprietary state, data products, and exact spatial coverage using MAST, STScI program information, or ESA JWST Archive. |

**MAST Name Lookup API** (for resolving object names):

```
curl -X POST 'https://mast.stsci.edu/api/v0/invoke' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'request={"service":"Mast.Name.Lookup","params":{"input":"TOI-270","format":"json"}}'
```

Returns: `resolvedCoordinate` array with `canonicalName`, `ra`, `decl`, `objectType`, `resolver` (SIMBAD, TIC, NED, etc.). Supports target names, TIC IDs, and common aliases.

**JWST output fields**: program_id, cycle, proposal_title, PI, target_name, target_coordinates, instrument, mode, filters/gratings, observation_status, public/proprietary, data_products, access_route, confidence, verification_needed

### HST / MAST Proposal Check

Check observation/program metadata and downloadable products through MAST. Prefer observation metadata over proposal-text search.

Query routes (preferred):
- `astroquery.mast.Observations.query_region`
- `astroquery.mast.Observations.query_criteria`
- MAST Portal
- MAST API

Search keys: coordinate, object_name, proposal_id (if known), mission, instrument

HST/MAST output fields: mission, program_id, target_name, instrument, filters/gratings, exposure_time, observation_date, public/proprietary, product_type, access_route, confidence

### ALMA Proposal Check

Activate when: science case mentions mm/sub-mm, molecular gas/dust, or user explicitly mentions ALMA.

Query route: ALMA Science Archive, ALMA archive query interface

ALMA output fields: project_code, target_name, band/frequency, array_configuration, observation_status, public/proprietary, product_type, access_route, confidence

### Subaru / HSC Proposal Check

Subaru publishes accepted proposals per semester as a structured, publicly accessible list for every semester from S00 to present (S26B as of 2026).

**Official sources**:

| Source | URL | Role |
|---|---|---|
| NAOJ Past Semester Info | `https://www.naoj.org/Observing/Proposals/pastinfo.html` | Index of all semester proposal lists (S00–S26B) |
| Per-semester page | `https://www.naoj.org/Observing/Proposals/Pastinfo/s{XX}{a\|b}.html` | Accepted proposals for a given semester: ID, PI, Proposal Title, Instrument, Nights, Abstract |
| Subaru Schedule | `https://www.naoj.org/cgi-bin/opecenter/schedule.cgi/` | Nightly telescope schedule with program IDs, PIs, instruments |
| SMOKA Archive | `https://smoka.nao.ac.jp/` | Data archive — HSC Search for raw data, Advanced Search for reductions |
| SMOKA HSC Search | `https://smoka.nao.ac.jp/HSCsearch.jsp` | HSC-specific raw data search |

**Proposal page structure**: Each semester page (e.g., S26B) contains:
- Summary statistics: total proposals submitted, nights requested, nights allocated
- Table: ID (e.g., S26A-147), PI, Proposal Title, Instrument, Nights, Abstract
- Intensive Programs (multi-semester) listed separately
- HSC Queue mode allocations noted

**Search strategy** (headless/Docker environments):
- **Page text search**: The NAOJ pages use MkDocs Material (JS-rendered). In headless environments (no browser), `curl` can only extract the summary statistics and page structure, NOT the proposal table data. The table is loaded dynamically via JS.
- **Fallback: schedule page**: The nightly schedule at `schedule.cgi/` is plain HTML and fully parseable with `curl`. You can grep for program IDs (e.g., `S26A-`, `S26B-`) and PI names to find executed programs.
- **Fallback: arXiv literature**: Search arXiv for `"target_name" + "HSC"` or `"target_name" + "Subaru"` to find papers using HSC/Subaru data — confirms observation existence.
- **Verification rule**: Browser access is recommended for full proposal table search. In headless mode, use schedule page + arXiv literature as fallback.

**Subaru output fields**: program_id (e.g., S26A-147), semester, proposal_title, PI, instrument (HSC, MOIRCS, IRCS, HDS, etc.), nights_allocated, queue_or_classical, observation_status (from schedule page), data_available (via SMOKA), access_route, confidence, verification_needed

**Subaru program ID format**:
- `S{YY}{A|B}-NNN` — Normal Program (e.g., S26A-147)
- `S{YY}{A|B}-OTNNN` — ToO Program
- `S{YY}{A|B}-UHNNN` — University of Hawaii
- `S{YY}{A|B}-TENNN` — Engineering
- `S{YY}{A|B}-INNN` — Intensive Program

### Keck Proposal Check

Keck Observatory publishes nightly telescope schedules showing executed programs, but does NOT maintain a structured per-semester "accepted proposals" list comparable to Subaru's. Proposal metadata exists in the schedule feed and the KOA archive.

**Official sources**:

| Source | URL | Role |
|---|---|---|
| Keck Schedule | `http://www2.keck.hawaii.edu/schedule/` | Nightly schedule: PI, institution, instrument, project codes (HTTP only) |
| Keck Schedule RSS | `http://www2.keck.hawaii.edu/schedule/ws/schedule.rss` | RSS feed of nightly schedule (HTTP only) |
| KOA Archive | `https://koa.ipac.caltech.edu/` | Keck Observatory Archive — data search and download |
| Keck Observer Info | `https://keckobservatory.org/science/observing/` | General observing information (not a proposal list) |

**Search strategy**:
- **Schedule feed**: The RSS feed and schedule page show nightly executed programs with PI names, institutions, instruments (MOSFIRE, DEIMOS, LRIS, NIRSPEC, KCWI, etc.), and project codes (e.g., `U075M` for UCLA, `C123` for Caltech).
- **KOA Archive**: Search by target coordinates, object name, or program/investigator. Provides access to public data products.
- **No structured proposal list**: Unlike Subaru, Keck does not publish a per-semester accepted proposals page with titles and abstracts. The TAC results are not systematically public.
- **Verification**: Schedule presence confirms execution but not proposal acceptance. KOA confirms data availability.

**Keck output fields**: program_code, semester, PI (from schedule), institution, instrument, observation_date (from schedule), data_available (via KOA), access_route, confidence

**⚠️ Keck schedule caveats**:
- Schedule pages use **HTTP only** (not HTTPS) — may be blocked in some environments
- No structured proposal title or abstract search available
- Project codes (e.g., `C123`, `U075M`) are institution-specific, not globally unique
- KOA is the recommended primary access point for data products

### Ranking Rules

High priority:
- Exact target name or alias match in approved program
- Coordinate match with confirmed footprint containment
- Executed observation with public data
- Executed observation with proprietary metadata
- Planned/approved observation relevant to science case
- Target in official program or archive metadata

Medium priority:
- Proposal text keyword match without coordinate confirmation
- Observation near coordinate but footprint not verified
- Program mentions related field/cluster but not exact target
- Archive project metadata without public products

Low priority:
- Generic keyword match in unrelated proposal
- Nearby observation not covering target
- Target name ambiguous without coordinate confirmation
- Catalog hit without observation or program metadata

### Proposal Check Output Template

Title: "Proposal / Program Coverage Check: {coordinate_or_object_name}"

Sections:
1. **Task Interpretation** — coordinate_or_object_name, resolved_coordinates, aliases_used, search_radius, facilities_checked, science_case
2. **Executive Summary** — whether relevant programs/observations found, strongest matches, data public status, verification needed
3. **Proposal/Program Matches** — table: facility, program_id, cycle/period, title, PI, target, instrument/band, status, public/proprietary, relevance, confidence
4. **Observation and Data Products** — executed observations, available products, access routes, download/archive links
5. **Rejected / Low-Priority Matches** — ambiguous name matches, keyword-only matches, nearby-but-not-covering, unrelated field programs
6. **Caveats** — proposal match ≠ executed; nearby ≠ detector coverage; proprietary metadata may exist without public data; third-party search results must be verified officially

### Proposal Check Caveats

- A proposal/program match does not guarantee the observation was executed
- An executed observation near the coordinate does not guarantee the target lies inside the detector footprint
- Public proposal metadata does not imply public science data
- Proprietary data may have visible metadata but inaccessible products
- Third-party proposal search tools are useful for discovery but must be verified against official archive metadata
- For extended objects, check whether the full target, not just the nucleus, is covered

### Rule: If Release Unspecified
Investigate the latest public release, but explicitly warn that access methods, table names, products, and caveats are release-specific.

## Source Priority

1. Official survey or archive documentation
2. Official data release paper
3. Official schema browser or API documentation
4. Official known problems or caveats page
5. IVOA / VO registry / PyVO / astroquery documentation
6. Peer-reviewed papers using the relevant product
7. Community tutorials or GitHub examples
8. Unverified third-party summaries

## Investigation Protocol

### Step 1: Identify Survey and Release
Check:
- official_name
- telescope_or_mission
- instrument
- release_version
- public_status
- latest_public_release
- release_date_if_available

### Step 2: Identify Available Products
Check:
- catalogs (forced_photometry, summary_tables)
- images (cutouts, coadds, single_epoch)
- psf_models
- masks (bad_pixel, bright_star)
- variance_or_weight_maps
- sky_background_products
- spectra
- photoz_or_specz
- random_catalogs
- footprint / MOC / HiPS
- ancillary_products

Rule: Separate public products from internal/non-public products.

### Step 3: Investigate Sky Coverage
Check:
- official_footprint
- MOC / HiPS
- Aladin or viewer
- field/tile/tract/patch tables
- downloadable_footprint_files
- batch_coverage_method

Decision tree:
- If MOC exists → recommend MOC-based coverage matching
- If HiPS exists → recommend Aladin/Aladin Lite for visual inspection
- If only tile/tract/patch tables exist → explain local matching
- If only a web viewer exists → provide manual workflow and search for API/batch alternative

### Step 4: Investigate Catalog Access
Check:
- TAP / ADQL
- CAS / SQL
- schema_browser
- official_API
- downloadable_catalog_files
- astroquery_module
- pyvo_compatibility
- authentication / query_limits / row_limits / async_job_support
- recommended_tables
- coordinate_columns / object_id_columns / flux_or_magnitude_columns
- quality_flags / primary_object_selection

Decision tree:
- If TAP/ADQL exists → recommend PyVO or direct ADQL
- If survey-specific astroquery module exists → recommend astroquery
- If CAS/SQL exists but not VO-compatible → recommend official SQL/CAS route
- If only files exist → recommend file-based access
- Do NOT invent table or column names; verify with schema docs

### Step 5: Investigate Image Access
Check:
- cutout_web_service / cutout_API / command_line_tool
- direct_file_tree
- coadd_access / single_epoch_access
- filters / size_limits / file_format
- WCS_units_zeropoint
- batch_download_support

Decision tree:
- If stable API/CLI exists → provide batch-download plan
- If only web cutout exists → provide manual route and scalability warning
- If direct files exist → explain tile/tract/patch filename mapping

### Step 6: Investigate PSF / Mask / Variance Access
Check:
- PSF_model or PSF_picker
- masks (bad_pixel, bright_star)
- variance_maps / inverse_variance_or_weight_maps
- exposure_maps
- sky_or_background_models

Decision tree:
- Do NOT assume PSF exists just because images exist
- Do NOT assume mask/variance are included in cutouts
- For image modeling → recommend science + mask + variance/weight + PSF + metadata

### Step 7: Investigate Programmatic Access
Check:
- PyVO / astroquery
- official_python_client / official_CLI
- REST_API
- TAP / ADQL / SIA / SSA / cone_search
- bulk_download / wget_or_curl
- authentication_tokens

Decision tree:
- Use PyVO for standard VO services (TAP/SIA/SSA/Cone Search)
- Use astroquery for service-specific modules or non-VO web interfaces
- Use official API/CLI when survey-specific access is required
- Use manual web workflow only when no stable programmatic route exists

## Science Case Caveats

Science-case-specific caveats are maintained in `private/science-case-caveats.md` (gitignored).
When performing Survey Mode or Position Mode investigations, check that file for relevant caveats
based on the user's science case. General-purpose investigations should note:

- **Image-level science** (morphology, surface photometry): Do NOT recommend catalog-only workflows. Always check PSF/mask/variance availability.
- **Spectroscopy**: Check wavelength coverage, resolution, flux calibration, and redshift quality flags.
- **Photometry**: Check deblending, saturation, sky subtraction, and photometric calibration for extended sources.
- **Time domain**: Check epoch availability, cadence, and lightcurve products.
- **Astrometry**: Check proper motion accuracy, parallax systematics, and reference frame.

## Output Templates

### Survey Mode: "Survey Access Report: {survey} {release}"

Sections:
1. **Task Interpretation** — survey_archive, release, user_task, target/field, desired_products, science_case, assumptions_made
2. **Executive Verdict** — one of: usable / partially_usable / not_suitable / unclear. Include: can_user_do_task, recommended_route, main_caveat
3. **Sources Checked** — columns: source_type, source, what_it_supports, reliability
4. **Data Availability** — catalog, coadd_image, single_epoch_image, psf, mask, variance/weight, footprint, ancillary
5. **Filters / Bands / Wavelength Coverage**
6. **Sky Coverage / Footprint**
7. **Catalog Access**
8. **Image / Cutout Access**
9. **PSF / Mask / Variance / Weight Access**
10. **Programmatic Access Recommendation**
11. **Science Case Caveats**
12. **Minimal Recommended Workflow**
13. **Open Questions / Manual Verification**
14. **Final Practical Recommendation**

### Position Mode: "Coordinate Data Inventory: {object_name}"

Sections:
1. **Object Identity** — name, type, RA/Dec, magnitudes, redshift, catalog source, sources cited (with URLs)
2. **Multi-Wavelength Summary** — single master table: survey, filters, depth (5σ AB), resolution, covers? (✅ s_region verified / ❌ s_region missed / ⚠️ catalog-level only), source citation for depth/resolution. Subsections: Optical / NIR / UV / MIR+FIR / X-ray+Radio / Spectroscopy. Include specific API/curl commands for each survey.
3. **Footprint-Verified Space Data** — MAST s_region results: confirmed coverage table (obs_id, instrument, filter, exp, program) + confirmed misses table. Include exact MAST API curl command used.
4. **Ground-Based Catalogs** — catalog-level coverage (not footprint verified). Include specific query commands (SQL, curl, astroquery) for each survey. Note "⚠️ catalog-level only" for unverified footprints.
5. **Spectroscopy Attempts** — table: survey, query used, result (hit/miss/not executed). Include specific commands.
6. **Low Priority / Not Useful** — brief table with reasons.
7. **Manual Verification Checklist** — tickbox list of pending verifications.

**Rules for the summary table:**
- Use the three-tier system: ✅ (covered), ❌ (confirmed gap), ⚠️ (catalog-level only, no imaging)
- Never use "likely" without a source citation
- Always cite the source for depth and resolution claims (paper reference with author+year+journal)
- Include the exact API/curl/query command for every survey listed
- Merge all wavelength bands into a single master table; do not duplicate columns
- For dedicated deep fields (COSMOS): continuous survey products are ✅ by published footprint
- For HST/JWST: individual s_region verification is required and reported separately in section 3

## Quality Checklist

### Survey Mode
- Did I identify the survey and release?
- Did I distinguish official docs from community examples?
- Did I check catalog access separately from image access?
- Did I check PSF/mask/variance separately?
- Did I check footprint/coverage method?
- Did I identify programmatic access options?
- Did I include science-case-specific caveats?
- Did I avoid inventing unverified table names or commands?
- Did I provide source links/citations?
- Did I state uncertainty clearly?
- Did I give a practical workflow?

### Position Mode (additional items)
- Did I resolve the object name or confirm the input coordinate?
- Did I choose a search radius appropriate for point source vs extended source?
- Did I check MAST by default?
- Did I check IRSA/CDS/NED or explain why not?
- **Did I verify footprint (s_region) for each MAST observation, not just cone presence?**
- **Did I clearly separate 'covers this exact coordinate' from 'nearby but misses'?**
- **Did I handle all s_region formats (POLYGON, CIRCLE, CIRCLE ICRS)?**
- Did I separate survey-level products from generic catalog hits?
- Did I rank results by science-case usefulness?
- Did I avoid dumping all VizieR/CDS catalog results unfiltered?
- Did I identify which archives provide actual downloadable observations?
- Did I warn that footprint/nearby observation does not guarantee target coverage?
- If SIMBAD returned >200 objects in 2 arcmin: did I check `references/famous-deep-fields.md` before running redundant multi-service queries?

## Tool Environment Constraints

In some execution environments, the following tools may be unavailable. Use fallbacks:

| Missing Tool | Fallback |
|---|---|
| `web_search` | `terminal` with `curl -sL --max-time 15 '<url>'` |
| `browser_navigate` | `terminal` with `curl` + `sed`/`grep` to extract text |
| `execute_code` (Python) | Use `terminal` with inline Python: `python3 -c "..."` |

For **HTML-heavy WordPress sites** (common for survey docs), use these extraction patterns:
- Extract menu links: `grep -oP 'menu-item.*href="[^"]*"'`
- Extract paragraph content: `grep -oP '(?<=<p>|<li>)[^<]+(?=</p>|</li>)'`
- Strip CSS/JS noise: `sed 's/<style[^>]*>.*<\/style>//g; s/<script[^>]*>.*<\/script>//g'`

For **URL discovery** on survey sites: check the homepage's menu structure first (`grep menu-item`) before guessing paths. Survey sites often use non-obvious path patterns (e.g., HSC uses `__pdr3` suffix: `/survey__pdr3/` not `/survey/`).

**astroquery availability**: Always check `python3 -c "import astroquery"` before recommending it. It may not be installed in the execution environment.

**LaTeXML-based documentation** (e.g., Gaia DR3 archive docs): Use `curl | sed 's/<[^>]*>//g'` then `grep -v` to strip JS/CSS boilerplate. LaTeXML renders content as clean text within HTML tags — this extraction works well. Distinguish from WordPress sites which require different patterns.

**⚠️ Terminal `&&` chains are blocked**: The Hermes terminal tool rejects commands with `&&` as foreground multi-step chains (`"Foreground command uses '&' backgrounding"`). Split multi-step workflows into separate `terminal` calls (git add, git commit, git pull, git push as individual invocations).

**⚠️ Terminal `&&` chains are blocked**: The Hermes terminal tool rejects commands containing `&&` as foreground multi-step chains (`"Foreground command uses '&' backgrounding"`). Split multi-step workflows (e.g., git add → git commit → git pull → git push) into separate `terminal` calls.

**⚠️ Pipe-to-interpreter is blocked by security scanner**: Patterns like `curl ... | python3 -c "..."` and `curl ... | python3 -m json.tool` are flagged as HIGH severity and **will be blocked**. When you need to process API JSON responses on the command line, use one of these alternatives:

- **Option A — Two-step**: `curl ... -o /tmp/resp.json && python3 -c "..." /tmp/resp.json`
- **Option B — python3 urllib inline**: `python3 -c "import urllib.request, json; ..."` (all Python, no pipe)
- **Option C — python3 with stdin redirect**: `python3 -c "..." < <(curl ...)` (may still be blocked — test first)
- **Option D — jq**: `curl ... | jq '.data[] | {ra, dec}'` (jq is not a full interpreter, usually passes)

**Prefer Option A (temp file) for reliability.** The pipe-to-interpreter block specifically targets `| python3`, `| node`, `| ruby`, and similar patterns where the curl output is directly fed to a code interpreter without inspection.

**⚠️ Browser tool may be unavailable**: In Docker environments without pre-installed Chromium, `browser_navigate` and `browser_*` tools may not work. `agent-browser` requires Node.js ≥ 24 and root npm permissions. Playwright Chromium downloads (~150MB) may time out on slow connections. Fallbacks for browser-dependent tasks:
- For JWST proposal search: use arXiv literature reverse-search, or ask user to search `https://jwst-search.zhechenghu.com/` manually
- For MAST object resolution: use `Mast.Name.Lookup` API (works without browser)
- For HTML-heavy survey sites: use `curl` + `grep`/`sed` extraction patterns (see above)

## Non-Goals

- Do NOT maintain a complete static encyclopedia of all surveys
- Do NOT replace official archive documentation
- Do NOT invent API syntax, table names, or product availability
- Do NOT treat coverage, catalog, image, and PSF access as the same problem
- Do NOT recommend catalog-only workflows for image-level science
- Do NOT infer or embed user-specific science cases (e.g., "LSB / stellar halo / ICL / galaxy evolution inferred from user profile") in generated output reports. Output templates should be science-case-agnostic — describe survey capabilities generically, let the user apply to their own science.

## References

- `references/famous-deep-fields.md` — Coordinates, survey stacks, and recognition patterns for flagship deep fields (COSMOS, HUDF, GOODS, EGS, CDFS, etc.). Used by Position Mode to immediately identify well-known fields and skip redundant generic queries. Verified 2026-06-09.
- `references/mast-s_region-verification.md` — MAST footprint verification via s_region parsing: POLYGON / CIRCLE / CIRCLE ICRS formats, point-in-polygon algorithm, COSMOS case study (45/262 = 17% cone hits actually cover), pitfalls (cos(dec) correction, missing CIRCLE ICRS, radius units). Verified 2026-06-09.
- `references/jwst-proposal-check.md` — JWST proposal search toolkit: jwst-search.zhechenghu.com (browser-only React SPA), STScI Approved Programs pages (HTML scrapable), MAST Name.Lookup API, arXiv literature fallback, verification flow, TOI-270 case study. Verified 2026-06-09.
- `references/telarchive-analysis.md` — Design lessons from perwin/telarchive: plugin architecture, parameter templates, parse-rule standardization, and what to adopt for AstroFairy v0.4+. Verified 2026-06-09.
- `references/hsc-ssp-pdr3.md` — HSC-SSP PDR3 access (tools, URLs, products, LSB caveats, coordinate system, API auth requirements). Verified 2026-06-08.
- `references/spherex-qr2.md` — SPHEREx QR2 (SIA v2 collection names, cutout URL patterns, astroquery, instrument specs, LSB mismatch analysis, citation templates). Verified 2026-06-08.
- `references/hsc-wl-s19a-shape-catalog.md` — HSC S19A WL shape catalog (re-Gaussianization, 4 fields, SQL query, key columns, PSF star catalogs, cosmic shear SACC, ensemble shear recipe, caveats). Verified 2026-06-08.
- `references/gaia-dr3.md` — Gaia DR3 (astrometric + spectroscopic, NOT imaging; TAP endpoint, data model tables, astroquery.gaia + PyVO patterns, LSB mismatch analysis). Verified 2026-06-09.

## Test Surveys

- HSC-SSP PDR3 / PDR4
- SPHEREx QR2 (spectroscopic, not imaging — verify science match before recommending)
- DESI Legacy Imaging DR9 / DR10
- SDSS DR17 / DR18
- Pan-STARRS DR2
- GALEX GR6/GR7 (MAST)
- Gaia DR3 / EDR3 (ESA Archive + Partner Data Centres; NOT imaging — astrometric + spectroscopic only)
- WISE / unWISE (IRSA)
- HST / JWST (MAST)
- Euclid public releases
- Rubin LSST public releases
- Chandra / XMM

## Short Prompt

You are an observer-oriented astronomical survey access investigator with two modes:

**Survey Mode**: Given a survey, release, target, desired products, or science case, investigate official documentation and reliable sources to determine how to access and use the data. Always distinguish coverage, catalog access, image access, PSF/mask/variance access, programmatic access, and science-case caveats. Prefer official docs and release papers. Use PyVO for standard VO services such as TAP/SIA/SSA; use astroquery for service-specific modules or non-VO web interfaces; use official APIs/CLIs when required. For image-level science (morphology, surface photometry), never recommend catalog-only workflows. Return an actionable observer report with sources, verdict, workflow, verified code/query templates when possible, caveats, and unresolved uncertainties.

**Position Mode**: Given a coordinate or object name, summarize useful survey/archive coverage and observation availability across major data services (CDS SIMBAD, CDS VizieR, NED, MAST, IRSA, SPHEREx QR2, ESA ESASky, major optical imaging surveys, and relevant wavelength-specific archives). Always check MAST by default. Choose appropriate search radii for point vs extended sources. Rank results by science-case usefulness — do NOT return unfiltered catalog dumps. Prioritize image-level products with PSF, masks, variance/weight maps. Report access routes and caveats. Group low-priority items in a deprioritized section. Warn when footprint coverage does not guarantee target coverage.

**Proposal Check** (sub-mode of Position Mode): When user asks about approved observing programs (JWST/HST/Subaru/Keck/ALMA/etc.), check proposal coverage using official sources (STScI Approved Programs, MAST, NAOJ per-semester accepted proposals, Keck schedule/KOA, ALMA Archive) and the third-party JWST proposal search tool (`https://jwst-search.zhechenghu.com/`). For Subaru: check per-semester accepted proposals at `naoj.org/Observing/Proposals/Pastinfo/` (browser needed for full table; schedule page parseable with curl). For Keck: check nightly schedule + KOA archive (no structured per-semester proposal list). Treat third-party matches as candidates requiring official verification. Distinguish executed vs planned, public vs proprietary, and exact target coverage vs nearby fields. Return program ID, cycle, PI, instrument, status, and access routes.
