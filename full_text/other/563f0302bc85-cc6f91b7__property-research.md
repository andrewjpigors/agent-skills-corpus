---
name: property-research
description: Property due-diligence workflow for any US state. Runs parallel research tracks, analyzes inspection/septic reports, models offer + financing strategy, and ships a polished single-page dossier site iterated to ≥9.5/10. Trigger words - property research, due diligence, property dossier, house research, property inspection, inspection report, offer strategy, real estate due diligence, contract documents, P&S, purchase and sale, dotloop, inspection contingency, contract status, addendum, DocuSign.
---

# property-research

Full due-diligence workflow for property evaluation in any US state. Runs parallel Sonnet subagent research tracks, folds in professional inspection/septic reports when available, models the offer and financing strategy, and assembles a self-contained dossier — both a markdown master and a **polished single-page website** iterated to ≥9.5/10.

> **Field-tested (691 Dartt Hill Rd, Bethel VT, May 2026 — or Boston MA, 2026).** The patterns below — claim-check scorecard, inspection cost-stack, the convergence test, the financing module, and the build→audit→critique→polish loop — came out of a real engagement. Reuse them; don't reinvent.

> **Privacy note:** Dossiers are saved to `~/Documents/properties/{slug}/` which is gitignored in `~/dispatch/.gitignore`. They contain personal financial research and should never be committed.

## The Through-Line: Verify, Converge, Don't Overpay

Three principles that run the whole engagement:

1. **Treat every input as unverified until checked against a primary source.** Listing copy, a "cheatsheet," even the seller's agent — all unverified. Independently confirm against FEMA / state environmental agency / county assessor / deed records / live routing. Present a **verified vs. unverified** breakdown (see Claim-Check Scorecard).
2. **The convergence test.** Pull value from independent angles — comps, the bank's appraisal reality, the conforming-loan cap, the documented repair cost-stack. When several independent inputs land on the same number, that number is the truth and the ask is noise. Say so explicitly; it's the single most persuasive thing in the dossier.
3. **Financing flexibility is for terms, never for price.** "We can recast / we have a credit line" is never a reason to overpay. Price discipline is the cake; financing is the icing.

---

## Triggering the Workflow

At the start of a new engagement, ask the user: **"Are you evaluating a potential purchase, or researching a property you already own?"** This determines which mode to run (buyer workflow vs. Owner's Dossier — see Mode: Owner's Dossier below). Also handle "Mode B: Town Research" when the user wants a town-level dossier with no specific property address (see Mode B below).

When the user asks for property research, due diligence, or a "property dossier", ask for:

1. **Property address** (street, town, state)
2. **Listing URL** (Zillow, Realtor.com, local MLS) if available
3. **Key concerns** the user wants to prioritize (optional)

Then derive a `slug` from the address using the state abbreviation from the address (e.g., `123-main-st-woodstock-vt`, `456-oak-ave-concord-nh`). Drop any `-vt` default — derive from the actual state.

---

## Directory Structure

```
~/Documents/properties/{slug}/
  dossier.md          ← final assembled markdown master
  tracks/             ← raw outputs from each parallel track
    01-assessor.md … 11-wildcards.md
  inspection/         ← when pro reports are provided
    ANALYSIS.md       ← summary + cost-stack
    *.pdf             ← saved source reports (inspection, septic, disclosures)
  contracts/          ← post-offer documents (P&S, addenda, disclosures)
    manifest.md       ← running log of all received contract docs
    REVIEW-{slug}.md  ← extracted key dates, flags, and cross-references
  site/
    index.html        ← the polished single-page deliverable (deployed)
```

---

## State Adaptation

The research tracks below were developed for Vermont properties but generalize to any US state. Use the following mapping when working outside Vermont:

| VT Source | Generic Equivalent |
|---|---|
| NEMRC town assessor | county assessor / parcel portal |
| VT ANR/DEC wastewater | state environmental agency wastewater/septic permit DB |
| VT ANR contaminated sites | state DEP/DEQ/DNR hazardous sites DB |
| ECFiber | FCC broadband map + ISP lookup (ECFiber is VT-only) |
| Act 250 | state land use / zoning law |
| VT current-use program | state agricultural/forestry current-use/greenbelt program |
| VT smoke/CO seller-cure law | state-specific seller disclosure requirements |
| Rural-VT contractor pricing | local market contractor rates |

Note: FEMA flood maps, EPA EJScreen, Zillow/Realtor comps, drive times, Reddit sentiment, permit history, and well databases are already state-agnostic.

---

## Research Tracks (Run All in Parallel)

**Address Validation Gate** — Before launching all research tracks in parallel, confirm the address is resolvable: Track 1 (assessor) finds a parcel record, OR a public MLS listing exists, OR the address resolves in the local E911/road database. If none match, stop immediately and surface to the user before continuing. Do not silently spawn parcel-specific tracks. Offer three options:
- **A)** Pause for correct address
- **B)** Area-level only (flood, broadband, drive times, nearby comps, sentiment, environmental — skip parcel-specific)
- **C)** Try neighboring address numbers (±10–50) and variants as best-guesses

Wait for user choice; do not default to B silently.

Spawn one Sonnet subagent per track. Each writes its findings to the corresponding `tracks/NN-name.md` file.

### Track 1: County/Town Assessor
- For Vermont: Search `[town] VT property records` or `[town] NEMRC assessor` (NEMRC is the VT-specific portal)
- For other states: Search `[county] [state] county assessor parcel search` or `[county] GIS portal property records`
- Look up: assessed value, tax history (last 5 years), owner history, last sale price and date
- Note any sudden assessment jumps or ownership transfers
- **Red flags**: recent flip (bought and relisted quickly), large assessment-to-list-price gaps

### Track 2: FEMA Flood Maps
- Go to https://msc.fema.gov/portal/search and enter the address
- Find: flood zone designation (AE, X, etc.), base flood elevation (BFE), whether flood insurance is required
- Check if property is in or near a Special Flood Hazard Area (SFHA)
- **Red flags**: Zone AE, Zone VE (coastal), any history of flooding in the area

### Track 3: Wastewater / Septic Permits
- For Vermont: Search `[town] VT wastewater management division` or ANR Online (Vermont Agency of Natural Resources — anronline.vermont.gov)
- For other states: Search the state environmental agency's wastewater/septic permit database (e.g., `[state] DEP septic permit search`)
- Find: permit status, system type (mound, in-ground, holding tank), permit date, approved capacity (bedrooms)
- Check if the system was permitted for the current use (actual vs. approved bedroom count)
- **Red flags**: no permit found, holding tank only (high ongoing cost), system older than 25 years, undersized for bedrooms

### Track 4: Comparable Sales (Comps)
- Search Zillow, Realtor.com, or local MLS for recent sales in same town/county, same property type
- Pull 5-10 comps from the last 12-24 months within reasonable radius
- Compare: price/sq ft, lot size, bedroom/bath count, age, condition
- **Red flags**: listing price significantly above comps, price reductions, long days-on-market

### Track 5: Drive Times
- Get driving estimates from property address to:
  - Nearest grocery store
  - Nearest hospital / emergency room
  - Nearest ski mountain (if relevant)
  - Town center / downtown
  - Nearest interstate on-ramp
- Include estimated drive times by season (note if roads are seasonal/unpaved)
- ⚠️ **MANDATORY: Verify every drive time with Google Maps before publishing.** The free OSRM engine routes rural Vermont over slow back roads and produced a **67-min** Killington estimate that was actually **~35 min** via state highways (VT-107 → VT-100). We published the wrong number; the client caught it and had to correct us. **This is a blocking step — do not include any drive-time estimate in an outgoing message, report, or site until you have confirmed it in Google Maps (or Google Maps routing via chrome-control). Use the Google Maps result as the canonical figure. If OSRM and Google Maps diverge by more than 10 minutes, note the discrepancy and explain which route each engine used.**
- **Red flags**: >45 min to hospital, no grocery within 20 min

### Track 6: Broadband Connectivity
- For Vermont: Check https://www.ecfiber.net/service-area/ for ECFiber availability at the address (ECFiber is VT-only)
- For all states (universal primary): Check FCC broadband map (https://broadbandmap.fcc.gov) for all available providers and advertised speeds
- Search `[address] internet` or `[town] [state] internet options` for real-world experience
- **Red flags**: no fiber available, only satellite (Starlink only), speeds under 25 Mbps download

### Track 7: Pond / Water / Easement Rights
- If property has a pond or waterfront: research who owns the water rights
- For Vermont: Search Vermont ANR online for any wetland delineations, shoreland permits, or Act 250 permits (Act 250 is VT's land use law — check the equivalent state land-use permit system for other states)
- Look for right-of-way or easement language in property description
- Search town/county records for any shared access easements, utility easements, or neighbor disputes
- **Red flags**: pond owned by HOA/third party, ROW crossing the lot, Act 250 or state land-use restrictions limiting use

### Track 8: Reddit / Google Sentiment
- Search Reddit: `site:reddit.com "[town name] [state]"`, `"[town name] [state abbr]" living`, `moving to [town name]`
- Search Google: `"[town name] [state]" neighborhood reviews`, `"[town name] [state]" problems`, local news outlets
- Check Nextdoor, local Facebook groups if accessible
- Summarize community vibe, known issues, recurring complaints
- **Red flags**: recurring infrastructure complaints, crime mentions, contentious local politics, school quality concerns

### Track 9: Permit History
- Search `[town/county] [state] building permits` or town's/county's online permit database
- List all building permits pulled on this property: additions, renovations, electrical, plumbing, HVAC
- Check if major renovations were permitted (unpermitted work is a liability)
- **Red flags**: evidence of unpermitted additions, open/expired permits, permits suggesting major issues (structural, mold)

### Track 10: Environmental
- Check EPA EJScreen (https://ejscreen.epa.gov) for proximity to industrial sites, contamination
- Check state environmental agency contaminated/hazardous sites database (VT ANR contaminated sites; for other states use state DEP/DEQ/DNR equivalent)
- Search for nearby landfills, gas stations (UST leaks), agricultural chemical use
- Look for wetland boundaries on the lot (restricts building)
- **Red flags**: brownfield within 0.5 miles, wetlands on lot limiting buildable area, PFAS contamination in area

### Track 11: Things You Wouldn't Have Thought Of
- **(VT)** Search for any Act 250 permits (Vermont's land use law — can restrict what you do with the property); for other states, look up the equivalent state land-use permit
- Check if town has zoning that affects short-term rentals (STR restrictions increasing in many markets)
- Look for any HOA or deed restrictions in the listing or town records
- Search for the specific property address + "lawsuit", "dispute", "lien"
- Check if the road is town-maintained or private (private road = maintenance cost)
- Look for nearby cell towers, wind turbines, or planned development
- Check local school district quality and enrollment trends
- **(VT)** Note any Vermont "current use" tax program enrollment (affects future development rights); for other states, check equivalent agricultural/forestry current-use or greenbelt program
- **All-electric heating cost model** — If the property is all-electric heat (heat pumps, baseboard), pull the state utility rate (e.g., Green Mountain Power for VT) and model annual heating cost for the square footage at typical usage in that climate zone (heating degree days). Flag if no propane/wood backup exists. Buyers consistently underestimate all-electric heating bills in cold climates.
- **Pond dam liability** — If the property has a pond with a dam, check the state dam safety registry (VT: anr.vermont.gov dam registry; other states: state dam safety program). Dam ownership = maintenance liability + potential state inspection requirements. Note the dam safety class.
- **Mud season road access** — Check if the property's primary access road is a Class 4 or private road. In Vermont, Class 4 roads are not maintained in winter/mud season (typically mid-March to mid-May) and some are impassable. Check the town's road classification records. For other states, check equivalent unimproved road designation.
- **Well permit / water source** — Check the state well completion report database (VT: maps.vermont.gov/DEC/wellsearch; other states: state geological survey or environmental agency). Look for permit existence, drilled depth, and yield. No well record on file is a red flag.
- **Seller motivation signals** — Beyond days-on-market as a single red flag, actively report: total DOM, number and amount of price reductions, original list price vs. current, and seasonal patterns (listed in spring, still sitting through summer = motivated by fall). Cross-check with assessor last-sale date.
- **Nearby noise sources** — Search for major highways, active rail lines, flight paths, and industrial operations within 1 mile using OSM + FAA sectional charts. Rural properties can be surprisingly close to interstate corridors (e.g., I-89/I-91 in VT) or freight lines.
- **Red flags**: private road with no maintenance agreement, deed restrictions limiting use, active liens, major planned development nearby, all-electric heat with no heating cost model provided, dam present with no state registration, Class 4 road as primary access (mud season = weeks of impassability), no well permit on record

---

## Track 12: Professional Inspection & Septic Report Analysis (when documents are provided)

Not parallel — runs whenever the client sends a home-inspection PDF, septic/wastewater eval, water test, or disclosure. **Read every page in full** (PDFs via the Read tool, ≤20 pages/request; chunk large reports). Never skim or truncate.

Produce these, saved to `~/Documents/properties/{slug}/inspection/`:

1. **`ANALYSIS.md`** — source list, the headline severity tally (minor / recommendation / safety-critical), each safety-critical item verbatim, septic verdict, "what checked out clean," and the open items still pending (e.g., well water test).
2. **The cost-stack table** — the highest-value artifact. For every documented defect, a class (`Critical` / `Structural` / `Health` / `Safety` / `Repair` / `Minor`) and a **directional cost range** at local market contractor pricing. Sum to a realistic near-term total. **Always label ranges as models, not quotes.** This converts a vague "needs work" into a hard, negotiable number.
3. **Separate the buildings.** If there's an unfinished/second structure, assess its build *quality* separately from its *legality*. The inspector speaks to framing/quality; the legal question (state wastewater permit for a second dwelling, certificate of occupancy) is separate and usually still unresolved — say so explicitly.

**Cost-stack lesson:** the pre-inspection dossier carried a ~$40–70k repair *estimate*. The real inspection roughly *doubled and documented* it (~$90–150k). A documented cost-stack is far stronger leverage than an estimate — it directly resets the offer.

**Seller disclosure note:** Many states require the **seller** to cure specific deficiencies (e.g., VT law requires seller to cure smoke/CO detector issues). Check the state-specific seller disclosure requirements. Flag any seller-cure items — they're free leverage.

---

## Module A: Claim-Check Scorecard

When the client provides a "cheatsheet," listing claims, or prior analysis, build an explicit verified-vs-unverified table. This is one of the most trust-building artifacts in the dossier.

| Claim | Status | What's actually true |
|---|---|---|
| (the claim verbatim) | `True` / `Stale` / `Worse` / `Per disclosure` / `Unconfirmed` | the primary-source finding + citation |

Rules:
- Every status backed by a primary source (FEMA panel #, NEMRC record (VT) or county assessor portal, VT DEC permit DB or state environmental agency, deed book/page, live routing).
- **Own corrections loudly.** When a later source overturns an earlier claim of *yours*, retract it in writing in the scorecard ("my earlier 67-min figure used a bad routing engine — retracted"). Credibility comes from visible self-correction.
- Update statuses as new evidence (inspection, septic) arrives — e.g., septic `Per disclosure` → `Confirmed worse`.

---

## Module G: GIS Setback & Parcel Geometry Analysis

Triggered when: user asks about setbacks, parcel geometry, how close a structure is to a property line/road/water, or when a property has physical features near boundaries (pond, structure, road edge).

### Pattern (state-agnostic)

1. **Geocode the address** to get lat/lon coordinates
2. **Fetch parcel geometry** from the county/state GIS portal (returns a polygon)
3. **Identify the feature** to measure against (shoreline, road centerline, property line)
4. **Compute point-to-polyline distances** using haversine formula
5. **Compare against regulatory setbacks** for that jurisdiction
6. **Flag** if any structure or feature is within 10ft of a setback limit → RED FLAG

### Vermont Worked Example (VCGI endpoints)

```python
# Geocode via VT E911 geocoder
base = "https://maps.vcgi.vermont.gov/arcgis/rest/services/EGC_services/PROD_VCGI_GEOCODER_WM_BEST/GeocodeServer"
r = requests.get(f"{base}/findAddressCandidates", params={"SingleLine": address, "f": "json", "outFields": "*"})
lat, lon = r.json()["candidates"][0]["location"]["y"], r.json()["candidates"][0]["location"]["x"]

# Fetch parcel geometry from VTPARCELS
parcels_url = "https://maps.vcgi.vermont.gov/arcgis/rest/services/EGC_services/PROD_VCGI_BASEMAP_SP_WM/MapServer/13/query"
r = requests.get(parcels_url, params={"geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "spatialRel": "esriSpatialRelIntersects", "outFields": "*", "outSR": "4326", "f": "json"})
parcel = r.json()["features"][0]
```

**VT-specific setback rules (as worked example — verify locally):**
- Shoreland: 35ft from mean high water
- Road centerline: 50ft from state highway centerline
- Property line: varies by town (check zoning bylaws)

### Address Discrepancy Pattern

Rural/informal road names often differ from official E911 registered names. If geocoder returns zero results:
1. Try nearby numeric variants (±10-50 on house number)
2. Search by town + owner name via NEMRC assessor
3. Note discrepancy in Track 1 findings

### Python: Haversine Point-to-Polyline Distance

```python
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def point_to_polyline_distance_ft(pt_lat, pt_lon, ring):
    """ring = list of [lon, lat] pairs from GIS geometry"""
    min_dist = float('inf')
    for i in range(len(ring) - 1):
        seg_lat = (ring[i][1] + ring[i+1][1]) / 2
        seg_lon = (ring[i][0] + ring[i+1][0]) / 2
        d = haversine(pt_lat, pt_lon, seg_lat, seg_lon)
        min_dist = min(min_dist, d)
    return min_dist * 3.28084  # meters to feet
```

### Red flags
- Structure within 10ft of any setback limit
- Parcel geometry shows structure crossing property line
- No parcel record found at the E911 address (address discrepancy)
- Setback violation on existing structure (affects insurability and resale)

---

## Module B: Offer Strategy

After research + inspection, model three scenarios. Anchor to comps, not the ask.

| Scenario | Price band | Trigger |
|---|---|---|
| **Best case** | top band | only if the deal-defining contingency clears (e.g., wastewater designer confirms build-out legal) **and** seller cures/credits the critical list |
| **Base / target** | comp-supported band | the recommended target; documented punch list comes off the price |
| **Walk-away** | floor — or walk | systems fail, or the core thesis (e.g., second dwelling) proves impossible |

Then provide: a recommended **opening number** (below target, anchored to comps + cost-stack), the **settle band**, hard contingencies that must not be waived, and a **ready-to-paste negotiation script** in the client's voice. Equipment/personal property never conveys unless itemized on a bill-of-sale schedule attached to the P&S — state this.

---

## Module C: Financing Strategy (when the client raises mortgage/financing)

Translate financing into plain English (assume first-time-buyer literacy unless told otherwise). Concepts seen in the field and worth knowing:

- **Conforming loan cap as a convergence point.** If the client's "magic number" loan ceiling lands near the comp-supported value, *name the convergence* — comps + appraisal reality + conforming cap all agreeing on one price is the most persuasive argument against the ask.
- **Appraisal-gap risk.** An over-ask contract on a hard-to-value rural property will likely appraise low; a financed buyer then covers the gap in cash or renegotiates. A **cash purchase removes the appraisal entirely** — major leverage.
- **Securities-backed line / pledged-asset (LAL/PAL/SBLOC).** Lets the client buy as cash without selling stock (no cap-gains hit). It's a *bridge*: variable rate, margin-callable, interest usually **not** tax-deductible. Plan: cash-buy low → refinance into a conforming mortgage fast → pay the line back (locks rate, frees the stock, makes interest deductible up to $750k acquisition debt).
- **Recast.** Close at the conforming amount, wire a lump sum to pay principal down, lender re-amortizes → same rate/term, lower payment. Confirm the product *allows* recast (most conforming fixed do; some ARMs/jumbos don't).
- **ARM vs fixed.** Compute P&I at each quoted rate (`L*r*(1+r)^n/((1+r)^n−1)`, `n=360`). The decision pivot is the **realistic hold timeline** vs the fixed period — a hard-to-finish/renovate property argues for more rate certainty.
- **Risk guardrail to always state:** borrowing against a concentrated portfolio to buy a heavy-renovation house is double leverage. Keep the punch-list money as real cash *outside* the line; don't max it.

**The one-liner that anchors every financing conversation:** *financing flexibility is for terms, never a reason to overpay on price.*

---

## Module P: Post-Offer / Contract Phase

Triggered when: offer is accepted, P&S received, addenda arrive, inspection contingency waiver, or dotloop/DocuSign completion emails land.

### a) Document Intake & Manifest

Save every contract PDF to `~/Documents/properties/{slug}/contracts/` with a descriptive filename. Append to `contracts/manifest.md`:

```
| Date | Document | Parties | Key Dates | Status |
|------|----------|---------|-----------|--------|
| 2026-05-22 | purchase-and-sale.pdf | Buyer ↔ Seller | Closing: Jul 15 | Signed |
| 2026-05-23 | personal-property-addendum.pdf | — | — | Signed |
```

Never let the user re-send a document because it wasn't saved. If a Gmail dotloop/DocuSign completion email arrives, auto-intake: download attachment or follow chrome-control link, save with descriptive name, run Step b immediately, notify with flags.

### b) Contract Review

Read each document in full. Extract:
- Purchase price
- Closing date
- Contingency deadlines (inspection, financing, title)
- Personal property inclusions/exclusions
- Repair credits or seller concessions
- Financing status

Cross-reference against Track 12 cost-stack and Module A claim-check scorecard. Flag any contradictions. Save findings to `contracts/REVIEW-{slug}.md`.

### c) Site Update

Update `site/index.html` to add a Contract Status milestone table:

| Milestone | Status | Date |
|-----------|--------|------|
| Offer Accepted | ✅ | May 20 |
| P&S Signed | ✅ | May 22 |
| Inspection Contingency | ⏳ Due Jun 1 | — |
| Financing Contingency | ⏳ Due Jun 5 | — |
| Closing | 📅 Jul 15 | — |

Rerun the build→audit→critique→polish loop after updating.

### d) Consolidated Brief

On "all the PDFs" / "consolidated brief" / "send me a summary of everything" request:
1. Fact-check across all docs in contracts/ (use fact-check skill as subagent)
2. Assemble `contracts/CONSOLIDATED-BRIEF-{slug}.md` with cross-referenced key facts
3. Convert via md2pdf
4. Send PDF via `reply --file`

### e) Auto-Intake from Email

Gmail dotloop/DocuSign completion emails = automatic intake trigger:
1. Download attachment or follow chrome-control link
2. Save to contracts/ with descriptive filename
3. Run Steps b and c immediately
4. Notify user: "📄 New contract doc: [name] — [key flags]"

---

## Mode: Owner's Dossier

Triggered when the user says "I own this property", "owner's dossier", or otherwise indicates they are researching a property they already own rather than evaluating a purchase.

Skip Module B (Offer Strategy) and Module C (Financing Strategy). Replace them with:

- **Module O1 — Tax Optimization:** Residential/homestead exemption status, AVM vs. assessed value comparison, appeal window dates, estimated savings if any exemption is missing or incorrect.
- **Module O2 — Permit Resolution:** Open or expired permits on record, resolution steps for each, cost estimates for closing them out.
- **Module O3 — Market Position:** AVM vs. assessed vs. recent comps, equity estimate, neighborhood trend (appreciating / flat / declining).
- **Module O4 — Utility & Risk Register:** Lead service line status, flood zone designation, environmental flags within 0.5 miles, any open liens.

In owner mode:
- Hero box in the site shows **"Your Position"** instead of "Ask vs Comp-supported vs Target"
- Actionable items are framed as **"Quick Wins"** (easy, high-value) and **"To Resolve"** (permit/legal items)
- PII policy and all other Key Rules still apply

---

## Mode B: Town Research

Triggered when the user requests a town dossier with no specific property address, asks for an explicit "deep dive on [town]", or says "adapt property-research for town research".

Run parallel Sonnet subagents for each town research track:

- **T1: Disaster / Flood History** — FEMA NFHL, NOAA storm events database, historical flooding incidents
- **T2: Town Ordinances & Zoning** — STR rules, building codes, variance history, selectboard minutes
- **T3: Infrastructure** — Class 4/seasonal road coverage, broadband (FCC broadband map + ECFiber for VT), water/sewer district availability
- **T4: Recreational Amenities** — parks, courts, trails, ski proximity, water access
- **T5: Regulatory Environment** — Act 250 permits or state equivalent, conservation land %, recent permit controversies
- **T6: Community Sentiment** — Reddit, local Facebook groups, Nextdoor, local news
- **T7: Town Fiscal Health** — property tax rate history, town budget trends, school enrollment trends, recent selectboard controversies

Output: `~/Documents/towns/{slug}/dossier.md` + `site/index.html`, published via sven-pages under `/{slug}/`. Reuse the existing build→audit→critique→polish loop (≥9.5/10) and ACL logic. Omit all parcel/buyer modules (comps, septic, offer strategy, financing). Address Validation Gate does not apply.

---

## Assembly: Dossier Format

After all parallel tracks complete, assemble `~/Documents/properties/{slug}/dossier.md` using this structure:

```markdown
# Property Dossier: {Address}

**Prepared:** {date}
**Source:** 11-track parallel research

---

## RED FLAGS

> This section leads with anything that warrants serious caution or could kill the deal.

- [List each red flag with the track that found it]
- [If none found: "No major red flags identified — see details below for minor concerns"]

---

## Property Overview

- **Address:** ...
- **Listing Price:** ...
- **Last Sale:** {date} for ${price}
- **Assessed Value:** ${value} ({year})
- **Lot Size / Sq Ft:** ...
- **Bedrooms / Bathrooms:** ...
- **Year Built:** ...

---

## Track Findings

### 1. Assessor & Tax History
[Summary from Track 1]

### 2. Flood Risk
[Summary from Track 2]

### 3. Septic / Wastewater
[Summary from Track 3]

### 4. Comparable Sales
[Summary from Track 4 — include a table of comps if possible]

### 5. Drive Times
[Summary from Track 5 — include a table of key destinations]

### 6. Broadband / Connectivity
[Summary from Track 6]

### 7. Water Rights & Easements
[Summary from Track 7]

### 8. Community Sentiment
[Summary from Track 8]

### 9. Permit History
[Summary from Track 9]

### 10. Environmental
[Summary from Track 10]

### 11. Things You Wouldn't Have Thought Of
[Summary from Track 11 — this section should surface anything surprising or non-obvious]

### 12. Inspection & Septic (if provided)
[Severity tally, safety-critical items, the cost-stack table, septic verdict, open items]

---

## Claim-Check Scorecard
[Module A table — every cheatsheet/listing claim vs primary source]

## Offer Strategy
[Module B — 3-scenario table, opening number, contingencies, negotiation script]

## Financing Strategy (if raised)
[Module C — plain-English plan, the convergence callout, risk guardrail]

---

## Summary Scorecard

| Category | Status | Notes |
|----------|--------|-------|
| Flood Risk | 🟢 / 🟡 / 🔴 | |
| Septic | 🟢 / 🟡 / 🔴 | |
| Broadband | 🟢 / 🟡 / 🔴 | |
| Access / Drive Times | 🟢 / 🟡 / 🔴 | |
| Environmental | 🟢 / 🟡 / 🔴 | |
| Market Pricing | 🟢 / 🟡 / 🔴 | |
| Legal / Title | 🟢 / 🟡 / 🔴 | |
| Community | 🟢 / 🟡 / 🔴 | |

---

*This dossier is for personal due-diligence purposes. Verify all findings with licensed professionals before making financial decisions.*
```

**PII policy:** Never include buyer names, emails, or other personal details in `dossier.md`, track files, or `index.html`. Always refer to buyers as "the buyers" or "you" (when writing for the buyer to read). Apply from the first track output — do not wait for assembly.

---

## Publishing: The Polished Single-Page Site

A markdown→"simple HTML" dump is not the deliverable. The client wants a **designed single-page site** they can read on a phone, hand to an agent, and trust. The proven structure (one self-contained `index.html`, no build step, in `~/Documents/properties/{slug}/site/`):

- **Sticky nav** + smooth-scroll anchors to every section
- **Hero**: address, key meta, and a **Verdict box** with price chips (Ask vs Comp-supported vs Target)
- Numbered sections: Snapshot → Decision Point → Inspection (cost-stack table) → Claim-Check → Overlooked → Flood/Access (timeline) → Price & Comps → Offer Strategy (3-scenario grid + negotiation script) → Questions → Photo gallery (lazy-loaded lightbox)
- Self-contained: inline `<style>`, system fonts or one webfont, no external JS deps. `<meta name="robots" content="noindex,nofollow">`.
- Footer: sources grid + dated preparer/disclaimer line; re-date it on every update.

When updating after new info (e.g., inspection): insert the new section, **renumber section labels in order**, update the verdict + claim-check rows + offer numbers, and bump the footer date.

### The build → audit → critique → polish loop (iterate to ≥9.5/10)

Do not ship the first draft. Loop until an honest self-score is **≥9.5/10**:

1. **Build/update** the `index.html`.
2. **Audit** structurally: `uv run python` to check balanced `<section>`/`<div>` counts, sequential `sh` labels, nav anchors all resolve.
3. **Critique** as a skeptical reader: is the verdict honest? do numbers reconcile? is the good news given fair weight alongside the bad? epistemics labeled (estimates vs facts, open items flagged)?
4. **Polish**, re-score, repeat. Track the scores (the Dartt Hill build ran 7.5 → 9.0 → 9.4 → 9.6 before shipping).
5. Deploy, then **verify live**: `curl -o /dev/null -s -w '%{http_code}'` returns 200, fetched bytes match local, key new content present.

### Publishing command + ACL (context-dependent)

`publish` needs the worker URL; set it explicitly if the script errors on config:

```bash
SVEN_PAGES_URL="https://<worker-subdomain>.workers.dev" \
  ~/.claude/skills/sven-pages/scripts/publish ~/Documents/properties/{slug}/site --name {slug} [ACL FLAG]
```

`--name {slug}` controls the URL path (`/{slug}/`) regardless of the source folder name.

**ACL is context-dependent — follow the explicit instruction:**
- **Default / no instruction:** admin-only (no flags). Verify with `publish --list`.
- **Group-chat deliverable, participants named:** `--acl "a@gmail.com,b@gmail.com"`.
- **Client explicitly says "no password" / "make it public":** `--public`. (Dartt Hill: client asked for no password — honored.)

After any deploy, verify the ACL behaves as intended (public → 200 without auth; private → 401/403). Note the dossier contains personal financial + negotiation strategy — if public, confirm the client accepts that the named owners/strategy are exposed to anyone with the link.

See `~/.claude/skills/sven-pages/SKILL.md` for full publishing docs.

---

## Key Rules

1. **RED FLAGS / decision-point section always comes first** — before any positive content
2. **Track 11 ("Things You Wouldn't Have Thought Of") is mandatory** — surface non-obvious issues
3. **All research tracks run in parallel** — do not wait for one to finish before starting the next
4. **Self-contained dossier** — readable without any prior context or the listing URL
5. **Read inspection/septic PDFs in full** — never skim or truncate; produce the cost-stack table
6. **Verify everything against primary sources** — claim-check scorecard; retract your own errors loudly
7. **Name the convergence** — when comps + appraisal + loan cap + cost-stack agree, say so explicitly
8. **Financing flexibility is for terms, never for price** — never let it justify overpaying
9. **Iterate the site to ≥9.5/10** via the build→audit→critique→polish loop; verify live (HTTP 200, content present) after deploy
10. **ACL follows the explicit instruction** — admin-only by default, `--acl` in group chats, `--public` only when the client asks
11. **Save raw track outputs + inspection analysis** to subdirectories for later reference
12. **Do not truncate findings** — if a track finds a lot, include all of it
13. **Re-date the footer/preparer line** on every site update
14. **Never include buyer names or personal details in the dossier or site** — refer to buyers as "the buyers" or "you" (when writing for the buyer to read). This is the default; do not wait to be asked. Strip any buyer PII (names, emails, phone numbers) from all markdown files and the deployed site.

---

## Mode C: Seller-Side CMA

Triggered when the user asks for a CMA, listing price analysis, "what's my home worth", or is preparing to sell a property they own.

Run comps-first (Track 4 logic), pull 6-10 sold comps from the last 6-12 months, apply a standard adjustment grid (sq ft, beds/baths, garage, condition, lot), and produce a price-range opinion — not a single number. Always state: "This is a broker price opinion, not an appraisal."

### Output Format Menu

Default to **Kitchen-Table Prep** unless the user specifies otherwise.

| Format | Audience | Content |
|--------|----------|---------|
| Kitchen-Table Prep (default) | Seller face-to-face | 1-page: price range, top 3 comps, 2 adjustment rows, 90-day absorption |
| Pre-Listing Audit | Seller + listing agent | Full comp table, adjustment grid, pricing rationale, condition notes |
| HNW Concierge | High-net-worth seller | Narrative format, wealth-management framing, tax/1031 angle if relevant |
| Off-Market Brief | Buyer's agent / pocket listing | Comp range only, no list-price opinion, no agent attribution |
| Past-Client Equity Card | Past client outreach | "Your home is worth ~$X today" 1-liner with 2 comps, CTA |

### Condo Due-Diligence Checklist

For condo/association properties, also check:

- **STR restrictions**: Does the association allow short-term rentals (Airbnb/VRBO)? Many newer MA associations prohibit them — flag if banned, since it affects buyer pool and value.
- **Special assessment risk**: Any pending or recently completed special assessments? Large assessments (roof, elevator, HVAC) reduce net proceeds. Ask for HOA meeting minutes if available.
- **Insurance type**: All-in (walls-in) vs bare-walls. Bare-walls means buyer needs HO-6 for interior — affects financing and appraisal.
- **FNMA warrantability**: Flag if association has >35% non-owner-occupied units or >15% dues delinquency — loan options shrink to non-conforming/portfolio, which limits buyer pool.

### MA Excise-Tax Verification Formula

To cross-check MLS closed price against registry deed stamps:

```
MA excise tax = ceil(price / 500) × $4.56
```

Example: $742,000 sale → ceil(742000/500) = 1484 stamps × $4.56 = **$6,767.04**

Look up the deed at the registry (masslandrecords.com or registry site) and verify the documentary stamps match. A >2% divergence between MLS price and stamp-implied price means the MLS price may be a list price or partial sale — flag as 'registry-unconfirmed'.

**Barnstable/Dukes/Nantucket surcharge**: These counties add a land-bank surcharge (2% on amounts over $100k for Dukes/Nantucket, 3% for Barnstable). Always note the county when doing MA excise verification.
