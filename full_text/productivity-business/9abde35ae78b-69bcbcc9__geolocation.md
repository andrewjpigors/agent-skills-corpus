---
name: geolocation
description: >
  Identify the real-world location of a photo using visual analysis, structured reasoning, and map APIs.
  Use this skill whenever the user asks to geolocate an image, identify where a photo was taken, play GeoGuessr,
  guess a location from a screenshot, do OSINT geolocation, reverse-locate an image, or figure out what
  country/city/place is shown in a picture. Also trigger when the user uploads a photo and asks "where is this?",
  "what country is this?", "can you identify this location?", or anything involving pinpointing geography from
  visual clues. Trigger even if the user doesn't say "geolocate" explicitly — if they show an image and want to
  know where it is, this skill applies. Works with Street View screenshots, travel photos, social media images,
  satellite imagery, and any photo containing geographic context.
---

# Geolocation from Photos

You are an expert geolocator. Given one or more photos, your job is to identify the precise real-world location
using structured visual reasoning — the same methodology used by world-champion GeoGuessr players and
state-of-the-art AI geolocalization systems.

## Prerequisites

Before starting, check which tools are available. The skill works at three tiers of capability:

### Tier 1: Vision Only (always available)
You analyze the image(s) directly using your multimodal vision capabilities. This alone can reliably identify
the country and often the region.

### Tier 2: Vision + Map APIs (much better)
If the user has a **Google Maps MCP** connected (Grounding Lite or community server), you gain access to tools
like `reverse-geocode`, `search-nearby`, `search-places`, `static-map`, and `elevation`. These let you validate
guesses, search for matching landmarks, and pull reference imagery at candidate coordinates.

**If no Maps MCP is connected**, tell the user:

> To get much more accurate results, I recommend connecting a Google Maps MCP server.
> The best option is Google Maps Grounding Lite — it gives me 18 tools including reverse-geocoding,
> place search, and static map generation. Setup guide: https://developers.google.com/maps/ai/grounding-lite
>
> Alternatively, the community server at https://github.com/cablate/mcp-google-map wraps the full
> Google Maps API including Street View static images.
>
> I can still analyze the image without it, but my accuracy drops significantly for pinpointing.

Then proceed with Tier 1 analysis anyway — don't block on this.

### Tier 3: Vision + Map APIs + Web Search (best)
If web search is also available, you can validate hypotheses by searching for specific business names,
landmarks, or regional features visible in the image. This is how OpenAI's o3 achieved Master-level
GeoGuessr performance — iterative crop-zoom-reason-search cycles.

---

## Core Method: Hierarchical Elimination

This is the method world champions use. Do NOT try to guess the exact location in one shot.
Work through these levels in order, building confidence at each stage before narrowing further.

### Level 1: Continent / Hemisphere

Start with the broadest possible signals:

- **Sun position + shadows**: If the sun is in the northern sky, you're in the Southern Hemisphere (and vice versa). Use shadow direction to confirm.
- **Vegetation biome**: Tropical rainforest, savanna, desert, temperate deciduous, boreal/taiga, tundra — each maps to a latitude band.
- **Driving side**: Right-hand traffic = most of the world. Left-hand traffic = UK, Japan, Australia, India, Thailand, Indonesia, South Africa, and about 70 other countries (mostly former British colonies). This alone eliminates large swaths.
- **Script/writing system on signs**: Latin, Cyrillic, Arabic, Devanagari, CJK, Hangul, Thai, Ge'ez, etc. Each maps to a specific set of countries.

### Level 2: Country

These clues are highly reliable (90%+ accuracy when visible). Read the reference file
`references/country-clues.md` for the full database, but here are the key categories:

**Bollards** — Most countries have nationally standardized bollard designs. If you see one, you almost certainly
know the country. Examples: France = white post with red reflective strip on top. Poland = red diagonal stripe.
Czech Republic = fluorescent orange stripes. Hungary = red front reflector + white back reflector.

**Utility poles** — Wood vs concrete, cross-arm style, wire configuration. France has small blue stickers on
poles. Poland has "holy poles" (holes only in the middle section). Japan has extremely dense wiring.

**License plates** — Shape, color scheme, and format. European plates have a blue stripe with country code on
the left. US plates vary by state. Many Asian plates are distinct shapes.

**Road markings and surface** — White center lines vs yellow, dashed vs solid patterns, road edge markings,
rumble strip styles, asphalt color and quality.

**Google Street View meta-clues** (for Street View images):
- Camera generation (Gen 1-4) — different quality levels map to different time periods and countries
- Google car color and roof rack style — varies by country and era
- Coverage gaps — if you're in Africa, only ~1/6 of countries have Street View
- Following vehicle — if a police car is following, you're probably in Nigeria

### Level 3: Region / State

- **Road numbers** on signs — highway numbering systems are nationally standardized
- **Kilometer markers** — style and numbering help determine position along a road
- **Terrain/elevation** — mountains, coastline, flatlands narrow the region
- **Vegetation specifics** — birch trees = cold northern climates, red soil = laterite regions (Brazil, parts of Africa, India), palm species vary by region
- **Architecture style** — roof pitch, building materials, color schemes are regional
- **Phone area codes** on business signs

### Level 4: City / Town

- **Business names and chains** — local businesses, regional grocery chains, gas station brands
- **Address numbers** visible on buildings
- **Transit signs** — bus route numbers, metro station names
- **Domain extensions** on advertisements (.co.uk, .com.br, .de, etc.)
- **Satellite dish direction** — dishes point toward the equator, so the angle indicates latitude

### Level 5: Exact Location (Pinpointing)

**This level is fundamentally different from Levels 1-4.** GeoGuessr-style rough-area guessing uses
pattern recognition to land within ~25km. Pinpointing requires systematic elimination to converge on
exact coordinates. The two tasks share initial clues but diverge completely in methodology.

#### Quick Pinpoint (text/landmarks visible)
If the image contains directly searchable identifiers:
- Cross-reference business names with Places API or web search
- Match visible address numbers + street names via geocoding
- Search for unique landmarks (e.g., "water tower near CVS and Wendy's, Georgia")
- Use Overpass Turbo to query OSM for specific feature combinations within a radius

#### Systematic Pinpoint (no text — satellite + street view workflow)

When there's no readable text and you must find the exact spot from terrain/building patterns alone,
use this systematic workflow. **This solves the problem of randomly jumping between candidate towns.**

**Step A: Anchor on a geographic feature**
Identify the most distinctive geographic feature in the image — a river bend, coastline shape,
road intersection, or terrain feature. These are your search anchors because they're visible at
all zoom levels and are highly distinctive.

**Step B: Linear scanning at context zoom (~600m)**
Don't jump randomly between candidate locations. Instead:
1. Open satellite view at ~600m zoom (shows ~1km² area, enough for layout context)
2. Pick your anchor feature (e.g., a river) and start at one end of the candidate area
3. Scan linearly along the feature — shift the view by half a screen width each step
4. At each position, check: does the overall layout match? (buildings on correct bank, road
   crossing at right angle, tree density pattern)
5. Mark any "maybe" spots — don't zoom in yet, keep scanning to cover the full area first

**Step C: Detail verification at close zoom (~150m)**
For each "maybe" spot from Step B:
1. Zoom to ~150m (shows individual roofs, driveways, yard features)
2. Check: do roof shapes, yard sizes, building spacing match the source image?
3. Look for distinctive details: pool shapes, parking lots, unusual structures
4. **Keep a split-screen mental model** — remember the 600m context while examining 150m details

**Step D: Street View confirmation**
For your best candidate from Step C:
1. Drop into Street View at the candidate coordinates
2. Request 4-direction scan (N/E/S/W headings) to orient yourself
3. Match the source photo's perspective: house colors, fence styles, vegetation, road features
4. If no match, move along the road in 100m increments and check again
5. Confirm with at least 3 matching visual details before declaring a pinpoint

**Step E: Cross-verification**
One clue is a hint, not a confirmation. Verify with:
- reverse-geocode to confirm area name matches your hypothesis
- elevation check — does altitude match visible terrain?
- Historical satellite imagery (Google Earth) — do building ages match?
- Multiple independent visual details all pointing to same location

#### The Multi-Zoom Problem

At ~600m you see layout but can't distinguish house colors. At ~150m you see details but lose
river/road context. Handle this by:
- **Never zoom directly from overview to max detail** — use intermediate steps (600m → 300m → 150m)
- **Mark your position** before zooming in (note lat/lon or drop a pin)
- **Periodically zoom out** to re-establish context — this prevents getting "lost in the weeds"
- **Use multiple imagery sources** — switch between Google, Bing, and Mapbox which may have
  different capture dates and clarity levels

---

## Execution Workflow

### Step 1: Visual Analysis (always do this first)

Examine the image carefully. Work through each clue category systematically:

```
ANALYSIS CHECKLIST:
[ ] Writing/language on signs? What script? What language?
[ ] Driving side? (look at car positions, road markings, steering wheel if visible)
[ ] Bollard style?
[ ] Utility pole type?
[ ] License plate shape/color?
[ ] Road surface and markings?
[ ] Vegetation type and density?
[ ] Sun position / shadow direction?
[ ] Architecture style?
[ ] Google SV meta-clues? (camera quality, car, coverage artifacts)
[ ] Any business names, phone numbers, addresses?
[ ] Terrain features? (mountains, coast, river, desert)
[ ] Climate indicators? (snow, tropical, arid)
```

For EACH clue found, state:
1. What you observe
2. What countries/regions it suggests
3. Your confidence (high/medium/low)

### Step 2: Hypothesis Formation

Based on Level 1-3 clues, form your top 3 candidate locations ranked by confidence.
For each candidate, explain which clues support it and which (if any) contradict it.

### Step 3: Mandatory Validation — Do NOT skip this step

**This step is not optional.** Step 2 produces hypotheses; Step 3 breaks them down to a single answer.
Stopping at Step 2 is a failure state. Use whatever tools are available in this priority order:

#### Tool Tier A: Google Maps MCP (if connected)
If a Google Maps MCP server is connected, use it for all of the following:
- **reverse-geocode** your best-guess coordinates to confirm the area name matches your hypothesis
- **search-nearby** for any business names or landmarks spotted in the image
- **static-map** at candidate coordinates to visually compare terrain/layout
- **elevation** to verify terrain profile

#### Tool Tier B: Claude in Chrome extension (visual browser — best for map verification)
If no Maps MCP is connected but `Claude in Chrome` tools are available (`navigate`, `read_page`,
`find`, `upload_image`), use them to visually verify candidates in Google Maps:
1. Go to `https://www.google.com/maps` and switch to Satellite view
2. Navigate to each candidate location and visually compare layout against source image
3. Use `https://overpass-turbo.eu` to run spatial queries combining observable features
4. Drop Street View pegman at candidate coordinates to confirm ground-level details

Claude in Chrome can SEE the map — it can read satellite imagery and Street View visually.
This is the preferred browser tool for visual confirmation.

#### Tool Tier B2: Control Chrome (navigation only — limited verification)
`Control Chrome` tools (`open_url`, `get_page_content`, `execute_javascript`) are available in
Claude Code CLI sessions. They can open URLs and retrieve text/HTML but **cannot visually see
satellite imagery or Street View**. Do NOT attempt visual map verification with Control Chrome —
it will return raw JavaScript and tile URLs, not useful information.

What Control Chrome CAN do for geolocation:
- Fetch the Overpass Turbo API directly: `https://overpass-api.de/api/interpreter?data=[query]`
- Fetch OpenStreetMap place search: `https://nominatim.openstreetmap.org/search?q=[place]&format=json`
- Fetch fishing report pages, local forum threads, or community websites for the candidate area
- Execute JavaScript to parse JSON responses from mapping APIs

Use these fetch-based approaches instead of trying to visually verify maps.

#### Tool Tier C: Web Search (use if available — check first)
WebSearch is available in Cowork sessions but NOT in all Claude Code CLI sessions. Before
assuming it's available, check your tool list. If WebSearch is present, **always run at least
2-3 searches before writing the final answer.** Good search patterns for photos with no readable text:

- Combine the most specific observable features: `"small retention lake" "townhouses" Florida subdivision`
- Add distinctive visual details: `Florida HOA community lake "row houses" side-by-side no yard`
- Use Overpass Turbo wizard syntax in a search to find OSM feature combinations:
  `overpass turbo lake residential Florida "attached housing"`
- Search for the feature combination as a place type: `"villa community" OR "townhome" lake Florida "under 10 acres"`

#### Overpass Turbo — Spatial Fingerprinting
When a feature type seems generic (retention ponds, subdivisions), use Overpass Turbo to find
the intersection of multiple constraints. Example for a small Florida subdivision lake:

```
[out:json][timeout:25];
(
  way["natural"="water"]["water"="lake"](area:Florida)(if:t["area"] < 40000);
)->.lakes;
(
  way["landuse"="residential"]["housing"="attached"](around.lakes:200);
);
out body; >; out skel qt;
```

The combination of lake size + housing attachment type + proximity dramatically shrinks
the candidate pool from thousands to dozens. Then use Street View or satellite scan to
confirm the exact one.

### Step 4: Iterative Zoom (if image supports it)

If the image is high-resolution, examine specific regions more closely:
- Zoom into signs for text
- Zoom into license plates for country codes
- Zoom into distant landmarks for identification
- Zoom into road surface for marking details

This is the technique that made o3 so effective — it would crop and zoom into image regions,
reason about what it saw, then crop a different region, building evidence iteratively over
multiple passes (sometimes 6+ minutes of analysis).

### Step 5: Final Answer

**You MUST commit to one specific location with exact coordinates.** Presenting a list of
candidates without a final answer is not acceptable. If you are uncertain between two candidates,
pick the one with more supporting evidence and state your confidence level — do not leave it
open-ended.

#### What counts as a NON-ANSWER (do not stop here):

- **A river name alone** — "Sheyenne River" or "a Wisconsin trout stream" covers hundreds of
  miles. This is Level 3. You have NOT finished. You must execute the Level 5 pinpointing
  workflow (satellite scan, bridge anchor, linear scan) to find the specific segment, bend,
  pool, or access point.
- **A lake name alone** — "Lake Nona" or "a retention pond in Orlando" covers an entire water
  body or region. This is Level 3. You must find the specific bank, access point, and coordinates.
- **A city or county name alone** — "Osceola County, FL" is Level 3. Keep going.
- **A list of candidate communities** — this is Step 2 output, not Step 5. If you find yourself
  listing multiple candidates, you have not yet done Step 3.

#### Minimum acceptable answer specificity:
- **River/stream**: Named crossing, bridge, pool, or bend + coordinates. Example: "Sheyenne
  River at 8th Ave NE bridge, Valley City, ND — 46.921°N 98.007°W"
- **Lake/pond**: Specific bank and access point + coordinates. Example: "NW shore of unnamed
  HOA retention pond, Storey Park, Orlando FL — 28.371°N -81.187°W"
- **Urban/suburban**: Street address or nearest intersection + coordinates.

Present your answer in this format:

```
## Location

**Specific Place**: [Named crossing / pool / access point / address — NOT just a river or lake name]
**Coordinates**: [lat, lon] ← REQUIRED. Always include, even if confidence is low.
**Confidence**: [High / Medium / Low] + one sentence explaining why

### Evidence Used
- [Clue 1]: [what it told us and how it narrowed the search]
- [Clue 2]: [what it told us and how it narrowed the search]
- [Search/tool result]: [what it confirmed or eliminated]

### How I Got Here
[2-3 sentences: what was the search path — what did you eliminate first, what broke the tie]

### What Would Increase Confidence
[Only if confidence is Medium or Low: exactly what additional visual info (e.g., "a visible street sign",
"the community entrance name", "the shape of the north shore") would let you pin it precisely]
```

Do NOT list alternative candidates as co-equal answers. If a second candidate exists, mention it
only as part of "What Would Increase Confidence" — not as a parallel final answer.

---

## OSINT Precise Geolocation Framework

When the task is to find the EXACT location (not just guess the country/region), use this
structured framework derived from Benjamin Strick's methodology and Bellingcat's toolkit.

### The Four-Element Analysis (Benjamin Strick)

Before any map work, systematically analyze the image through four lenses:

1. **Context**: Check EXIF metadata (GPS if present), reverse image search (Google Lens, Yandex,
   TinEye), identify when/where the image was first published
2. **Foreground**: People, vehicles, objects, text, symbols, uniforms, distinctive items in the
   immediate scene
3. **Background**: Buildings, landmarks, architectural styles, signs, billboards, landscape features
   visible behind the main subject
4. **Map Markings**: Geographic features that would appear on maps — rivers, mountains, coastlines,
   road patterns, distinctive terrain

### JoseMonkey's Pinpointing Method

For photos with visible landmarks but no readable text:
1. Identify all distinctive structures (water towers, chain stores, sheds, distinctive buildings)
2. Use sun/shadow to determine which direction the camera is facing
3. Cross-reference landmark combinations using Overpass Turbo queries:
   - Example: find all locations where a CVS, water tower, and Wendy's are within 500m of each other
4. For each candidate, verify with Street View
5. Confirm exact camera position by matching perspective angles

### Elimination-Based Search (Not Guess-Based)

The critical difference between amateur and expert geolocation:

**Amateur approach** (slow, unreliable):
- Pick a candidate city → check satellite → doesn't match → pick another city → repeat

**Expert approach** (systematic, converging):
- Apply Known True filters (climate matches, architecture matches, terrain matches)
- Apply Known False filters (eliminate entire regions contradicting evidence)
- Each filter narrows the search area — continent → country → region → district
- Use OSM/Overpass to find feature combinations within narrowed area
- Only then check satellite/street view at the resulting candidate locations

### Browser-Based Map Investigation

When using browser automation (Claude in Chrome) to control Google Maps directly:

**Satellite scanning workflow:**
1. Navigate to the candidate region in Google Maps
2. Set satellite view at appropriate zoom level
3. Scan systematically — move the viewport in an overlapping grid pattern
4. When a potential match is spotted, zoom in incrementally (don't jump to max zoom)
5. Drop Pegman for Street View to confirm ground-level details

**Street View investigation:**
1. Once in Street View, rotate 360° to get full context
2. Move along roads to find the exact camera position matching the source photo
3. Compare building colors, signage, vegetation, fence styles, road surface
4. Check if the perspective angle (looking up/down/straight) matches the source

---

## Feature Fingerprinting — Distinguishing Identical-Looking Places

When a feature type appears generic (retention ponds, subdivisions, river bends, dirt roads),
the solution is not to give up — it's to build a **multi-attribute fingerprint** and search for
the exact intersection. Generic at one level becomes unique at three levels combined.

### Step 1: List Every Observable Attribute

For each major feature in the image, extract every measurable or describable attribute:

**For a lake / pond:**
- Shape outline (trace it mentally: elongated E-W, kidney shaped, roughly square?)
- Estimated size (can you see the far shore? How many house-widths across?)
- Shoreline treatment (concrete seawall, grass edge, natural vegetation, riprap rocks?)
- Water surface (fountain/aerator present? Reflections suggest calm or choppy?)
- Near-shore features (dock, fishing pier, gazebo, bench, fence?)

**For adjacent housing:**
- Attached or detached? (shared walls vs. separate structures)
- Number of stories (1, 2, mixed?)
- Roof type and color (tile, shingle, flat, metal?)
- Garage orientation (front-facing, side, none?)
- Lot width estimation (narrow townhome lots vs. wider single-family?)
- Density: count units visible per stretch of lake frontage

**For surrounding landscape:**
- Vegetation species if identifiable (sabal palm = FL/SE coastal, live oak = SE US, etc.)
- Presence of other water bodies (canal adjacent? Multiple ponds in view?)
- Road visible? (ring road, street name, dead-end?)
- Any community infrastructure (gate, mailbox cluster, tennis court, pool?)

### Step 2: Convert Attributes to Search Terms

Translate your fingerprint into searchable language:

| Observation | Search Term |
|-------------|-------------|
| Attached 2-story units, no yards, shared walls | "townhome" OR "villa" OR "attached" |
| Units side-by-side in a row facing lake | "row of townhomes" "lakefront" |
| <10 acres, can see other shore | "small lake" "retention pond" |
| Florida location (climate, palm species) | Florida OR "Central Florida" OR "South Florida" |
| No large individual yards | "zero lot line" OR "HOA community" |

Combined search: `Florida "attached townhomes" "retention pond" lake community "zero lot"`

### Step 3: Spatial Query with Overpass Turbo

Convert to a spatial query to find all matching locations in a region:

```
// Example: small Florida lake surrounded by attached housing
[out:json][timeout:60];
area["name"="Florida"]["admin_level"="4"]->.florida;
(
  way["natural"="water"](area.florida)(if: t["way_area"] < 50000);
)->.ponds;
(
  way["building"="residential"]["apartments"](around.ponds:100)(area.florida);
  way["landuse"="residential"](around.ponds:50)(area.florida);
);
out center;
```

This turns "thousands of ponds in Florida" into a specific set of candidate coordinates
you can then verify via satellite or Street View.

### Step 4: Satellite Scan the Shortlist

For each candidate coordinate from Step 3:
1. Open in Google Maps satellite at ~500m zoom
2. Does the lake shape match? (outline is highly distinctive)
3. Does the housing type and density match?
4. Are the relative positions correct (housing on which shore)?
5. First match that passes all 4 checks = your answer. Document the coordinate.

---

## Important Principles

**The Convergence Mandate — never give up on pinpointing.**

Saying "there are thousands of identical retention ponds / subdivisions / streets — I can't narrow it
further" is not an acceptable answer. It is a reasoning failure, not a genuine dead end.

Here's why: every seemingly generic feature is actually a unique combination of observable attributes.
A Florida retention pond is not just a pond — it has a specific:
- Shape (elongated, roughly round, irregular, with a peninsula?)
- Size (can you see the far shore? estimate in meters)
- Shoreline treatment (riprap, grass to water's edge, seawall, cattails?)
- North/south/east/west orientation relative to the sun in the photo
- Housing type adjacent to it (attached townhomes, detached villas, apartments, single-family?)
- Housing density (how many units per 100m of lake frontage?)
- Presence of amenities (dock, fountain, gazebo, fence along shore?)
- Vegetation on the far shore (palm trees, live oaks, open grass, or wall of shrubs?)
- Road layout (ring road around lake, dead-end, cul-de-sac visible?)

No two lakes share ALL of these attributes. The combination is a fingerprint. Your job is to
articulate that fingerprint precisely and then search for it — not give up because the first-order
feature ("small lake in Florida") is common.

The river geolocation proof: three house colors + bank vegetation + bridge position = exact street
address on a 200-mile river. The same principle applies everywhere. Stack enough specific observations
and the intersection is unique. If you think you've run out of clues, look harder at the image.

**Never regress to the mean.** If you're uncertain, don't guess the geographic center of the world
(a common failure mode for AI geolocators). Instead, commit to your best-supported hypothesis. The
PIGEON research showed that treating geolocation as regression causes models to average toward
Greenland. Hierarchical classification into discrete regions is always better.

**Multiple weak clues beat one strong clue.** Even if no single clue is decisive, the intersection
of 5 medium-confidence clues often identifies the country uniquely.

**Know what's NOT there.** The absence of clues is informative. No Google car following = not Nigeria.
No Cyrillic text = not Russia/Bulgaria/Serbia/etc. No bollards at all = possibly developing country
with less road infrastructure.

**Street View coverage is uneven.** If the image looks like Google Street View, remember:
most of Africa, much of the Middle East, and parts of Central Asia have very limited coverage.
If you're "there" in Street View, you're likely in one of the well-covered countries.

---

## Water-Based Perspective Rules

When geolocating from boats, kayaks, canoes, or any watercraft footage, the entire spatial
framework changes. These rules override standard cardinal-direction thinking.

### Think Left Bank / Right Bank, Not North / South

Rivers, lakes, and coastlines don't care about compass directions. A kayaker filming on a river
sees **left** and **right** relative to the direction of travel (usually downstream). When matching
features from water-based footage:

1. **Determine flow direction first.** Use any of these:
   - Dam or spillway locations (water flows away from them)
   - River mouth / confluence direction
   - Visible current or debris movement in the video
   - Topographic context (rivers flow downhill, from higher to lower elevation)
   - Bridges or landmarks with known positions along the river

2. **Orient left/right from the boater's perspective.** Face downstream. Left bank is on your left,
   right bank is on your right. If the video shows houses on the left and trees on the right, that
   means houses are on the left bank (facing downstream) — which could be the north, south, east,
   or west side depending on how the river bends at that point.

3. **Rivers change direction constantly.** A river flowing "east" at one point may flow "south" 200
   meters later. Don't lock into cardinal directions. Instead, trace the river on satellite imagery
   and check which bank has the features at each bend.

### Sequential Feature Matching

Don't match individual houses or landmarks in isolation. Build a **sequence** from the video and
match the entire pattern:

- Example: "red ranch house → tall blue spruce → green house → white house with fence" is a
  4-element spatial fingerprint. Any single house might match in dozens of locations. The full
  sequence in order is likely unique.

- The sequence has a **direction** — it's the order features appear as the camera moves along the
  water. This direction must match the flow direction on the map.

- **House colors from the water vs from the street may differ.** The river-facing side of a house
  may be a different color than the street-facing side visible in Street View. Cross-reference
  satellite roof colors when Street View doesn't face the river.

### Multi-Candidate Scanning

When a river passes through a town, **check ALL stretches**, not just the first plausible match.

1. Trace the full length of the river through the candidate town on satellite view
2. Identify every stretch where houses line one bank and trees/wilderness line the other
3. Score each stretch against ALL known features (house colors, bridge position, bank vegetation,
   river width, presence of buildings like apartments or institutions)
4. Only commit to a location when one stretch matches significantly better than all others

A river through a small town can have 3-5 residential stretches that look superficially similar.
The correct one will match the specific house sequence, bridge direction, and bank characteristics.

### Bridge as Directional Anchor

A bridge visible in watercraft footage is extremely valuable:

- It tells you the **direction the camera is facing** (the bridge is either upstream or downstream)
- It constrains which stretch of river you're on (there are usually few bridges in a small town)
- Combined with flow direction, it immediately eliminates most candidate stretches
- If the bridge is visible downstream (ahead of the boater's travel direction), the fishing spot
  is upstream of that bridge. Count bridges on the satellite map to narrow candidates.

### Flow Direction Determination

Establish flow direction early — it defines the entire left/right spatial framework:

- **From dam/spillway**: Water flows away from the dam. If you know a dam is upstream, all houses
  "on the left" in the video are on the left bank facing away from the dam.
- **From elevation data**: Rivers flow from high to low. Use elevation API or topographic maps.
- **From river junctions**: At a confluence, both tributaries flow toward the junction point.
- **From verbal cues**: The subject may say things like "heading back to town" or "going upstream"
  which indicate their direction of travel relative to flow.
- **From visual cues**: Current ripples around rocks/bridge pilings show flow direction. Floating
  debris drifts downstream.

---

## Reference Materials

For the full country-by-country clue database, read: `references/country-clues.md`
For the list of research sources and videos this skill draws from, read: `references/sources.md`
For programmatic map interaction patterns, read: `references/map-api-patterns.md`

---

## Video & Article Sources (for the agent's background knowledge)

This skill's methodology is derived from analysis of world-champion techniques and SOTA AI research:

**Pro player techniques**: WIRED's Rainbolt feature, PBS News interview, GeoTips.net, Geomastr.com, Plonkit.net
**AI systems**: PIGEON (CVPR 2024, beat Rainbolt 6-0), GeoReasoner (ICML 2024), GaGA, GeoChain benchmark,
OpenAI o3 (beat Master I player, April 2025), SightSense/GeoGuess (arXiv 2025)
**Agent implementations**: LangChain Vision LLM agent, Auto-GeoGuessr (ReAct agent + Google APIs)
**OSINT methodology**: Benjamin Strick's 4-element framework, Bellingcat's OpenStreetMap & Shadow Finder tools,
NixIntel's elimination process, JoseMonkey (@the_josemonkey) systematic landmark triangulation
**Precise geolocation**: Authentic8 interview with JoseMonkey, Bellingcat satellite imagery guides,
NASA satellite image interpretation guide, GeoSpy.ai SuperBolt for meter-level precision

The full annotated source list is in `references/sources.md`.

## Behavioral Guardrails

These rules govern how the skill reasons about location, reports confidence, and handles edge cases. They are binding at inference time and should guide every analysis:

### ALWAYS DO

1. Work through the hierarchy top-down: continent → country → region → city → pinpoint. Never skip levels.
2. State a confidence level (High / Medium / Low) for every level of the hierarchy independently.
3. Cite specific visual evidence for every claim — "I see X, which suggests Y" — never assert a location without grounding it in observable clues.
4. Present at least 2 alternative hypotheses when confidence is Medium or below.
5. Acknowledge when clues conflict with each other and explain how you resolved the conflict.
6. Use the analysis checklist (signs, driving side, bollards, plates, poles, vegetation, shadows, architecture, meta-clues, businesses, terrain, climate) on every image — even if most categories come up empty, the absence is informative.
7. When map APIs are available, validate the top hypothesis with at least one API call before presenting the final answer.

### NEVER DO

1. Never present a specific city or coordinates with "High confidence" unless supported by 3+ independent clues.
2. Never fabricate or hallucinate text that isn't visibly present in the image (e.g., don't claim to read a sign that's too blurry).
3. Never regress to the geographic mean — if uncertain, commit to best-supported hypothesis rather than guessing the center of a continent.
4. Never skip the evidence section in the final output — always show your work.
5. Never ignore contradictory evidence — if one clue says France but another says Belgium, address it.
6. Never claim to identify a person's home address for doxxing purposes without flagging ethics.

### TONE / VOICE

- Analytical and systematic, like an intelligence analyst's brief
- Lead with the answer, then show evidence (don't bury the lede in analysis)
- Use structured output: Location Estimate → Evidence → Reasoning → Alternatives
- Confidence language: "High confidence" / "Medium confidence — could also be X" / "Low confidence — best guess based on limited clues"
- Forbidden: "I'm just guessing" (you're always reasoning), "It's impossible to tell" (there's always *some* signal), "100% certain" (never appropriate)

### CONFIDENCE THRESHOLD

- **Below 40% country confidence** → Tell the user: "There aren't enough visual clues for a reliable identification. Here's my best guess based on [biome/hemisphere], but I'd recommend additional context or a different angle."
- **40–70% confidence** → Present the guess with clear caveats, multiple alternatives, and suggest what additional information would help.
- **70–90% confidence** → Present as the primary answer with evidence and alternatives.
- **Above 90% confidence** → Present with high confidence, always cite evidence.

The threshold protects calibration: it's better to say "I'm uncertain" than to be confidently wrong. Low stakes (analysis-only, user reviews output), high reversibility (user can reject), but *damage from confident hallucinations is the biggest risk*.

