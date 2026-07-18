---
name: merch-brief
description: Generate a bespoke branded-merch creative brief plus a complete deliverable — visual tech pack (range grid, product heroes, lookbook, embellishment macros, contextual placement), a cinematic hero image, a branded single-page presentation website with OG card, the real brand logo, and optional GitHub repo + Vercel deploy. Modeled on what a high-end merch agency (e.g. Magnum Opus) hands a client. Trigger when the user asks to "make merch", "design a merch program", "merch tech pack", "branded swag", "tour merch", "event merch", "branded apparel range", "build a merch deck", or names a brand/event and wants ideas/mockups/a shippable concept site for swag, drops, or capsule collections.
---

# merch-brief

End-to-end skill for producing a bespoke branded-merch concept package and shipping it as a live presentation site. Takes a **brand** and an **optional creative direction**, researches the brand into a canonical creative brief, generates a full set of visual artifacts via Higgsfield, composes a branded single-page website, and optionally ships it to GitHub + Vercel.

The full deliverable, end to end, in one pass:

1. **Brand research** — Higgsfield brand-kit fetch + supplementary web research
2. **Creative brief** — `BRIEF.md` (palette, motifs, range plan, embellishment plan, audience persona, commerce notes) — *gated on user approval*
3. **Sequenced image pipeline** — sequential rounds on `nano_banana_pro` (stills) + `seedance_2_0` (video), each one using prior rounds as `medias[]` references:
   0. Cast (portrait refs for male + female stand-in models)
   1. Location plates (empty environments)
   1b. Mood board (composite of brief references)
   2. Brand mnemonics (wordmark / motif / palette tile on swatch)
   3. Piece mockups (each SKU as a flat-lay product hero)
   3b. Hangtag + packaging concept
   4. Line sheet (gridded composite of mockups)
   4b. Wholesale sell-sheet (B2B variant of the line sheet, MOQ/pricing annotated)
   5. Model-in-environment lookbook
   6. Hero image (cinematic 16:9 still)
   7. Hero video (~10s cinematic motion clip)
   8. Social cuts (2× 9:16 video for TikTok / IG Reels)
4. **Real brand logo** — pulled from Higgsfield brand-kit OR Wikimedia Commons fallback
5. **Branded site + supporting docs** — `index.html` (single-page, video embedded), `og.png`, `BRIEF.md`, `TECHPACK.md` (manufacturer-side specs), `INDEX.md` (job-ID gallery)
6. **Ship** *(optional, gated)* — private GitHub repo + Vercel deploy

## When to use

Use this skill when the user wants any of:
- A merch capsule, drop, tour line, event swag, or branded apparel range
- A visual "tech pack" — a gridded line plan showing the SKUs front/back/colorways
- Mockups of branded merchandise (tees, hoodies, caps, totes, accessories, premium objects)
- A creative brief ready to hand to a manufacturer or designer
- A live presentation site (or pitch deck) for any of the above

Do **not** use it for: general logo design (use brand-guidelines), a single one-off mockup with no range thinking, or animation/video (use Higgsfield's video tools directly).

## Inputs

Collect at intake (use AskUserQuestion if any are unclear, but never block on optional fields):

| Field | Required | Notes |
|---|---|---|
| `brand` | yes | Brand or event name. "Bacardi", "Coachella 2026", "Burberry", "Red Bull Air Race" |
| `brand_url` | recommended | Canonical site. If user didn't supply, search for it and confirm with the user once before scraping. |
| `creative_direction` | no | Free-text, layered ON TOP of the brand's intrinsic identity. Examples of how a user might phrase it: "dark vintage washed gothic", "soft refined, no logos screaming", "stadium-giveaway pull-tabs vibe", "archive-era heritage". Preserve verbatim in the brief. |
| `occasion` | no | "Album tour", "Q4 holiday drop", "Stagecoach 2026 staff merch", "Venice Beach edition" |
| `audience` | no | "Streetwear collectors", "festival GA", "international elevated" |
| `tier` | no | `quick` (4 + hero = 5 images) / `standard` (9 + hero = 10, default) / `deluxe` (14 + hero = 15) |
| `ship` | no | `true` if user wants the deck pushed to GitHub + deployed to Vercel. Default `false`. |

If `brand` is missing, ask. Everything else has good defaults.

---

## Phase 1 — Brand kit research

The goal is a structured understanding of the brand's existing visual identity, **before** any generation.

1. If `brand_url` is set or you can confidently identify the canonical site, **kick off Higgsfield's brand-kit fetch immediately** (it's async, takes ~30s):
   ```
   mcp__higgsfield__show_marketing_studio(
     action='fetch', type='brand_kit', scrap_url='<brand_url>'
   )
   ```
   Save the returned `brand_kit_id` — you'll poll it in Phase 5 for the official logo.

2. While the kit is fetching, supplement with a quick web pass using `/browse` or `/defuddle`:
   - Recent campaign/lookbook imagery — what aesthetic moment is the brand in *right now*?
   - Past merch drops (search "<brand> merch drop", "<brand> capsule", "<brand> tour merch")
   - Cultural references the brand leans on (music, sport, subculture, era)

3. If the brand is an **event** (festival, tournament, conference): also pull venue/city motifs, dates, headliners or stars, sponsors, prior-year merch.

4. If `creative_direction` is empty, **derive one** from the research: 2–3 sentences capturing the proposed aesthetic, an era reference, and an embellishment direction.

---

## Phase 2 — Synthesize the creative brief

Write `BRIEF.md` in a working folder `~/Documents/merch-briefs/<brand-slug>-<YYYY-MM-DD>/`. The brief is the contract — it drives every prompt downstream.

**Use [`glossary.md`](./glossary.md) as the controlled vocabulary** when writing this brief and every prompt in Phase 3. The glossary covers fabric weights, weaves, fits, construction, embellishments (embroidery + print), washes, trims/hardware, typography, and photography/lighting — with brand references per section for taste calibration. Pull terms from it instead of inventing vocabulary; the brief should read like a real tech pack, not a fashion blog. Don't keyword-stuff — pick 2–4 specific terms per spec line that actually communicate the choice.

Required sections (markdown):

```markdown
# {{Brand}} — {{Occasion}}
### Merch Brief
*Audience: {{audience}} · Date: {{today}}*

## One-line pillar
{{single sentence: what this drop IS at its core}}

## Creative direction
*(User direction, preserved):* {{user's creative_direction verbatim, or "derived from research" if absent}}

{{2–4 sentences. Era/reference + mood + key tension. Build around the user's direction; never overwrite it.}}

## Palette
- **{{Color name}}** `#xxxxxx` — {{role}}
- ... 5–7 colors total

## Typography
- **Display:** {{family + feel}}
- **Body / labels:** {{family + feel}}
- **Wordmark treatment:** {{embellishment treatment for primary mark}}

## Garment language
{{fabric weight, fit cut, wash, garment-dye notes — 2–4 sentences}}

## Motif library
1. **{{motif}}** — {{where it lives}}
2. ... 4–7 motifs

## Embellishment plan
{{embroidery / chain-stitch / chenille / puff print / silkscreen / heat transfer / patchwork / sublimation — where each goes for each piece}}

## Range plan
| # | SKU | Garment spec | Colorways | Embellishments | Notes |
|---|---|---|---|---|---|
| 1 | **Hero piece** | ... | ... | ... | Hero |
| ... | 6–10 SKUs total per tier |

## Lookbook & context direction
- **Lookbook environment:** {{specific place description}}
- **Contextual placement:** {{specific lifestyle scene}}
- **Embellishment macros:** {{which embellishments to feature}}

## Audience persona  *(include only if selected in scope gate)*
{{3–5 sentences. Who this is FOR, concretely. Age range, taste neighborhood, how they discover brands, what else lives in their wardrobe, what would make them pre-order vs. wait. Pull from the `audience` input + brand research; don't invent demographics that don't fit the brand world.}}

## Commerce  *(include only if selected in scope gate)*
- **Distribution:** {{DTC drop / wholesale / pop-up / limited numbered run / open run / pre-order window — pick one or two, justify briefly}}
- **Pricing tier:** {{rough MSRP per piece — e.g. Tee $58, Hoodie $148, Cap $48, Cardigan $245. Reflect the brief's quality register (heavyweight + hand-embroidered + small batch = higher; standard production = lower)}}
- **Drop calendar:** {{sample → bulk production → QC → drop date → restock window → close. Concrete dates if known, relative weeks if not.}}
- **Inventory depth (optional):** {{rough buy depth per SKU × size if the brief is for a production run, not just a concept}}

## References
- ... 3–6 references (other brands, eras, specific past collections, films, music, places)

## Trademark fidelity note
The {{brand}} mark and wordmark in generated images will be approximate — these are concept renders for direction approval. Real artwork applied by a designer with the official brand kit.
```

### Brief → glossary section map

When filling each `BRIEF.md` section, pull vocabulary from these specific [`glossary.md`](./glossary.md) sections:

| BRIEF.md section | Glossary sections to pull from |
|---|---|
| `## Palette` | §7 (Washes & finishes) — for surface-treatment vocabulary that accompanies color names |
| `## Typography` | §9 (Typography & display) — display family, label/mono family, wordmark treatment |
| `## Garment language` | §1 (Fabric weights), §2 (Weaves & knit structures), §3 (Fits & silhouettes), §7 (Washes & finishes) |
| `## Motif library` | freeform — pull light rendering vocabulary from §5 (Embroidery) / §6 (Print methods) when describing how each motif lives on the garment |
| `## Embellishment plan` | §5 (Embroidery), §6 (Print methods), §8 (Trims & hardware) |
| `## Range plan` | per row: §1 (weight), §2 (weave), §3 (fit), §5/§6 (embellishment), §7 (wash) |
| `## Lookbook & context direction` | §10 (Photography & lighting) for the lighting + lens grammar |
| `## Audience persona` | freeform — describe the wardrobe in glossary-grade vocabulary (§1–§3 for what else they wear) |
| `## Commerce` | freeform — pricing tier reflects glossary-grade choices (heavyweight §1 + hand-embroidered §5 = premium tier) |

### Brief sign-off gate

After writing the draft, show the user the brief and ask:

```
AskUserQuestion(questions=[{
  question: "Sign off on the brief and proceed to scope selection?",
  header: "Approve brief",
  multiSelect: false,
  options: [
    { label: "Approve — proceed to scope selection",
      description: "Accept the brief as drafted. Next step is the scope-selection gate (which optional rounds / artifacts to include)." },
    { label: "Tweak the brief first",
      description: "Pause for you to revise the brief — palette, motifs, range plan, audience, commerce, or creative direction." },
    { label: "Stop here",
      description: "Accept the brief but skip all generation. Deliverable = BRIEF.md only." }
  ]
}])
```

Generation costs credits — don't burn them on the wrong direction.

---

## Phase 3 — Sequenced image generation pipeline

**This is the most important part of the skill.** Each round builds on the last. Earlier rounds become *reference inputs* for later rounds via Higgsfield's `medias[]` parameter — passing prior `job_id`s in by reference keeps the visual world (location, fabric, embellishments, model identity) coherent across the whole deliverable.

### Scope-selection gate — granular control over what to generate

Before Preflight, ask the user which optional rounds and artifacts to include. The **core pipeline** (Rounds 0, 1, 2, 3, 4, 5, 6 + Phase 5 site composition) always runs once the brief is signed off. Everything else is opt-in.

**Tier defaults** (these are the answer-pre-fills, not hard rules — the user can override anything):

| Optional artifact | `quick` default | `standard` default | `deluxe` default |
|---|---|---|---|
| Round 1b — Mood board | ✓ | ✓ | ✓ |
| Round 3b — Hangtag + packaging | — | ✓ | ✓ |
| Round 4b — Wholesale sell-sheet | — | ✓ | ✓ |
| Round 7 — Hero video | ✓ | ✓ | ✓ |
| Round 8 — Social cuts (2× 9:16) | — | ✓ | ✓ |
| `TECHPACK.md` (manufacturer-side spec doc) | — | ✓ | ✓ |

Always-included regardless of selection: Rounds 0, 1, 2, 3, 4, 5, 6 + `BRIEF.md` + `INDEX.md` + `index.html` + `og.png` + real brand logo. The new BRIEF.md sections (`## Audience persona`, `## Commerce`) ride along with TECHPACK selection — if the user wants the production doc, they get the strategy sections too; if they don't, those sections are omitted to keep the brief lean.

**The scope-selection question** (call this immediately after the brief sign-off):

```
AskUserQuestion(questions=[
  {
    question: "Optional image rounds to include?",
    header: "Image rounds",
    multiSelect: true,
    options: [
      { label: "Mood board (visualize references)",
        description: "Round 1b — single composite image of the brief's References pinned to a studio wall. ~3 credits." },
      { label: "Hangtag + packaging concept",
        description: "Round 3b — first customer touchpoint. Tag macro + box / poly bag arrangement. ~4 credits." },
      { label: "Wholesale sell-sheet variant",
        description: "Round 4b — B2B framing of the line sheet with MSRP / MOQ / lead-time annotations. ~4 credits." }
    ]
  },
  {
    question: "Motion / video output?",
    header: "Video",
    multiSelect: false,
    options: [
      { label: "Hero video + 2 social cuts (full motion)",
        description: "Round 7 hero video (5s, 16:9) + Round 8 social cuts (2× 9:16 verticals for TikTok / IG Reels). ~45 credits." },
      { label: "Hero video only",
        description: "Round 7 only — 5s cinematic clip for the website hero. ~15 credits." },
      { label: "Skip video — stills only",
        description: "No video output. Website hero uses the Round 6 still as a static image." }
    ]
  },
  {
    question: "Production + strategy artifacts?",
    header: "Production",
    multiSelect: true,
    options: [
      { label: "TECHPACK.md — manufacturer-side production spec",
        description: "Per-SKU production document (measurements, BOM, embellishment placements, labels, hardware, hangtag, packaging, est. FOB, regulatory). Zero generation credits — markdown only." },
      { label: "BRIEF.md ## Audience persona section",
        description: "3-5 sentence paragraph describing the customer concretely. Zero credits." },
      { label: "BRIEF.md ## Commerce section",
        description: "Distribution strategy / pricing tier (MSRP per SKU) / drop calendar. Zero credits." }
    ]
  }
])
```

After the user answers, **surface the resulting cost estimate** (preflight section below uses the selected scope) and proceed with only the selected rounds. Rounds the user did not select are silently skipped in Phase 3 — don't fire them and don't include them in `INDEX.md`.

If the user re-prompts mid-run with "skip the wholesale sheet" or "add a hangtag after all," honor it inline without re-asking — they've shown they want granular control.

**Do not fire everything in parallel.** Each round must complete before the next starts. Within a round, fire calls in parallel; between rounds, poll the previous round to completion first.

```
Round 0  — Cast              (portrait refs, male + female) ──┐
Round 1  — Locations         (env. plates)                  ──┤
Round 1b — Mood board        (composite of brief refs)      ──┤
Round 2  — Brand mnemonics   (motifs, palette)              ──┼─→ medias[] in Round 3, 3b
Round 3  — Piece mockups     (flat-lay heroes)              ──┼─→ medias[] in 4, 4b, 5, 6
Round 3b — Hangtag + packaging concept                      ──┤
Round 4  — Line sheet        (gridded composite)            ──┼─→ medias[] in 4b
Round 4b — Wholesale sell-sheet (B2B variant of 4)          ──┤
Round 5  — Model in env.     (Cast + Location + Mockup)     ──┤
Round 6  — Hero image still  (Cast + Location + hero Mock)  ──┼─→ medias[] in 7, 8
Round 7  — Hero video        (motion from Round 6 still)    ──┤
Round 8  — Social cuts       (2× 9:16 from Rounds 0,3,6)    ──┘
```

**Sub-rounds (1b, 3b, 4b) fire in parallel with their parent** when their references are ready:
- Round 1b mood board has no upstream dependencies → fires alongside Round 1
- Round 3b hangtag/packaging needs Round 2 mnemonics → fires alongside Round 3
- Round 4b wholesale sheet needs Round 4 line sheet → fires immediately after Round 4 (alone — different prompt)
- Rounds 7 + 8 (video) need Round 6 still done → fire after Round 6, in parallel with each other

**One model handles all of it: `nano_banana_pro`.** It accepts unlimited references via `medias[]` and is provably good at compositing — Round 4 pulls every Round 3 mockup into one coherent line sheet, and Rounds 5/6 pull a Cast portrait + Round 1 location + Round 3 mockup into one coherent lookbook frame. Same trick, same model, top to bottom.

(`soul_2` and Soul Character training are not used. They're a viable alternative if you want trained reusable identities across many decks, but for a single deck the nano_banana_pro `medias[]` compositing approach is faster, cheaper, and avoids the 10-minute training wait.)

### Tier counts

| Round | Component | quick | standard | deluxe |
|---|---|---|---|---|
| 0 | Cast — portrait refs *per character × 2 characters* | 2 + 2 | 3 + 3 | 4 + 4 |
| 1 | Location plates | 1 | 2 | 3 |
| 1b | Mood board | 1 | 1 | 1 |
| 2 | Brand mnemonics | 2 | 3 | 4 |
| 3 | Piece mockups | 4 | 6 | 9 |
| 3b | Hangtag + packaging | 1 | 2 | 2 |
| 4 | Line sheet *(4k)* | 1 | 1 | 1 |
| 4b | Wholesale sell-sheet | 0 | 1 | 1 |
| 5 | Model in environment | 1 | 2 | 3 |
| 6 | Hero still *(4k)* | 1 | 1 | 1 |
| 7 | Hero video *(`seedance_2_0`, 5s)* | 1 | 1 | 1 |
| 8 | Social cuts *(`seedance_2_0`, 5s 9:16)* | 0 | 2 | 2 |
| **Total stills** | | **15** | **23** | **31** |
| **Total videos** | | **1** | **3** | **3** |
| **Credits — default res policy** | | **~50** | **~95** | **~115** |
| **Credits — max res (every still at 4k)** | | **~74** | **~133** | **~173** |

Video is ~15 credits per 5-second clip on `seedance_2_0`, image stills as before. The default policy keeps every still at `2k` (same cost as 1k), bumps line sheet + hero + wholesale to `4k`, and fires the video rounds with `seedance_2_0` at 5s. If the user says "max quality", push every still to `4k` and budget accordingly.

### Model routing (applies to all rounds)

- **Use `nano_banana_pro` for everything.** Empty environments, swatches, flat-lay garments, gridded composites, *and* on-figure shots. It accepts unlimited references via `medias[]` and composites them reliably — the line sheet is the proof.
- `marketing_studio_image` requires a linked product object via Marketing Studio — only use when the user has an actual SKU URL/upload, not for concept renders.
- `soul_2` and Soul Character training are *available* if a project genuinely needs a reusable trained identity across many future decks — but for any single deck, `nano_banana_pro` with portrait refs in `medias[]` is the recommended path.

### Resolution defaults (uplevel quality, credits are not the constraint)

`nano_banana_pro` accepts `resolution: '1k' | '2k' | '4k'` (per `models_explore`). Pricing is **flat at 1k and 2k (2 credits), doubled at 4k (4 credits)** — confirmed via `get_cost`. There is no reason to ever ship at 1k.

Defaults the skill uses:

| Round | Resolution | Why |
|---|---|---|
| 0 — Cast | `2k` | Face detail matters; 2k costs the same as 1k |
| 1 — Locations | `2k` | Reference plate, not a hero |
| 2 — Brand mnemonics | `2k` | Macro fabric/thread detail benefits from 2k |
| 3 — Piece mockups | `2k` | Catalog-grade flat-lays |
| 4 — Line sheet | **`4k`** | Most-shared single image, busiest composition, worth the +2c |
| 5 — Model in env. | `2k` | Portrait fidelity at 2k is more than enough |
| 6 — Hero | **`4k`** | The website's primary visual, worth the +2c |

Pass `resolution: '2k'` (or `'4k'`) as a top-level param inside `params` on every `generate_image` call. If the user explicitly says *"max quality"* or *"render everything at the top tier"*, push every round to `4k`. The cost roughly doubles but every artifact will be print-grade.

### Speed

`nano_banana_pro` jobs typically complete in 10–20s at 1k/2k and 20–30s at 4k. Higgsfield's `job_status(sync: true)` blocks ~25s server-side, so a 4k job may need one extra poll. That's fine — fire the round, then issue `job_status` calls in parallel for every job in the round; the harness is notified per completion.

The skill never uses `soul_2`'s `use_relax: true` mode (which trades wait time for cheaper credits). For this skill, latency is the more valuable resource — keep `use_relax: false` if `soul_2` ever does come into play.

### Image-to-image referencing

Higgsfield's `generate_image(params={...})` accepts `medias: [{value, role}]` where:
- `value` = a prior generation's `job_id` (preferred — server resolves to CDN URL)
- `role` = `"image"` for `nano_banana_pro`. If uncertain, call `models_explore(action='get', model_id='nano_banana_pro')` and inspect `medias[].roles`.

Passing references **does not lock the output to the reference** — it conditions the generation. Multiple references compound (mnemonic + mockup, or portrait + location + mockup → grounded lookbook). There's no hard upper bound documented; the line sheet round routinely passes 6+ refs without issue.

### Preflight

After the scope-selection gate, **preflight cost** on representative calls (`get_cost: true`):
- `nano_banana_pro` 4:5 2k (most still rounds)
- `nano_banana_pro` 16:9 4k (line sheet, hero, wholesale)
- `seedance_2_0` 16:9 5s (hero video) — only if video was selected
- `seedance_2_0` 9:16 5s (social cuts) — only if social was selected

Check `balance`. **Compute the total spend estimate from the scope-selection answers** (not the full tier counts) — adding up only the rounds the user actually selected. Surface the number to the user and get a final go-ahead before firing any generation.

Every `generate_image` call in every round should include `resolution` per the table above — `'2k'` is the default for most rounds, `'4k'` for Round 4 (line sheet), Round 4b (wholesale), and Round 6 (hero). If the user said "max quality", set every still call to `'4k'` and bump the credit estimate accordingly. Video uses `seedance_2_0` at default settings.

**Use [`glossary.md`](./glossary.md) for every prompt's technical vocabulary.** Embellishments come from §5–6, fabrics from §1–2, fits from §3, construction from §4, finishes from §7, trims from §8. Lighting/lens clauses for portrait and lookbook prompts come from §10. Don't keyword-stuff — 2–4 specific terms per prompt clause is the sweet spot.

---

### Round 0 — Cast

Generate clean portrait references for two stand-in models — one male, one female. These become `medias[]` inputs in Rounds 5 and 6 so the same person appears across every shot they're in.

Default to **one male + one female** so the lookbook can show the line on both. Adapt to the brand if it's clearly gendered (menswear-only, womenswear-only) or has a single fronting persona.

- **Model:** `nano_banana_pro`
- **Aspect:** `1:1` (clean square reference, no body context)
- **Cost:** ~2 credits each
- **Count:** 2–4 per character × 2 characters by tier (just enough variety in angle/expression to give the compositing room to work — we are NOT training Soul Characters here)
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §10 (Photography & lighting) for the studio lighting clause and backdrop tone.

For each character, use the *same* identity description across all their refs — vary only angle and expression. Keep the descriptions concrete: age, build, hair color/length, skin tone, distinguishing features, vibe. **Pull the character archetype from the brief's audience and brand world** — Stagecoach characters look different from Burberry characters.

**Prompt template:**
> Studio portrait, {{angle — front-facing / three-quarter left / three-quarter right}}, {{expression — neutral / soft smile / serious}}. A {{age}}-year-old {{gender}} with {{hair description}}, {{skin tone}}, {{build}}, {{distinguishing features}}, {{vibe — "old-money European taste" / "weathered ranch worker" / "downtown art-school" / etc.}}. Wearing a plain {{neutral color}} t-shirt. Plain {{light grey / cream / sky}} studio backdrop. Soft directional light from upper-left, even tone. Sharp focus on the face. No props, no styling beyond the plain tee. Clean catalog reference quality.

Fire all male + female ref prompts in parallel. **Poll to completion.** Save the `job_id`s — these are the character references for Rounds 5 and 6.

---

### Round 1 — Locations

Generate the physical world(s) the line lives in. **These plates have no garments and no models** — they're empty environmental references the rest of the pipeline will inhabit. Pulled directly from the `## Lookbook & context direction` section of `BRIEF.md`.

- **Model:** `nano_banana_pro`
- **Aspect:** `16:9` (so they double as hero-backdrop candidates)
- **Cost:** ~2 credits each
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §10 (Photography & lighting) — pull time-of-day, light direction, film stock, focal-length equivalent, grain notes. This round IS the lighting grammar reference for Rounds 5 and 6.

Each location plate should be a single specific place at a single specific time of day, captured the way a photographer scouts it: clean composition, all the environmental cues present, but no action happening yet.

**Prompt template:**
> Cinematic empty-set establishing photograph of {{specific location from brief}}, {{time of day}}. No people, no garments, no models in frame. The setting shows: {{1–3 concrete environmental elements from brief — boardwalk, hangar floor, rattan beach chairs, dirt two-track, stage trusses, etc.}}. {{Light direction and quality, color cast}}. Shot on {{35mm film stock / medium-format feel}}, {{grain notes}}, {{focal length}} equivalent. Wide composition with negative space where a subject could later stand. Editorial location scout quality.

Fire 1–3 location prompts in parallel. **Poll all to completion** before Round 2.

---

### Round 1b — Mood board *(optional — skip if not selected in scope gate)*

A single composite image that *visualizes* the brief's `## References` section. The Magnum-Opus wallpaper move: a grid of reference imagery (other brands' pieces, archival photography, vintage media, landscape, type specimens, fabric swatches) arranged like a moodboard pinned to a studio wall. **Does NOT depend on prior rounds** — fires in parallel with Round 1.

This is the round where the brand-world references stop being a bullet list and become a single image you can hand to a designer.

- **Model:** `nano_banana_pro`
- **Aspect:** `4:3`
- **Resolution:** `2k`
- **Cost:** ~2–4 credits
- **Count:** 1
- **References:** none — pure prompt-driven composite
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §10 for the "shot on a studio wall" framing if used; §1–§2 for any visible fabric swatches; §9 for any visible type specimens.

**Prompt template:**
> Studio mood-board composite, top-down photograph of a corkboard or studio wall covered in pinned references for the {{brand}} {{occasion}} merch capsule. Arranged in a loose grid: {{6–10 specific references from the brief's `## References` list — describe each concretely, not by brand name where possible: "vintage 1970s racing-paddock photograph", "Mediterranean leisure editorial spread", "raw selvedge denim swatch", "weathered enamel pin", "italic condensed type specimen", "palm-shadow film still", etc.}}. Pins, masking tape corners, slight overlap between cards, soft top-down studio light. The board reads as the visual brain of the line — neutral background, no logos, no people centered. Editorial design-studio quality.

Fire as a single call. **Poll to completion.**

---

### Round 2 — Brand mnemonics

The design system, rendered as physical artifacts. These set the visual language — fabric color, thread texture, motif rendering, embellishment treatment — that Round 3 will use as `medias[]` references for piece-level consistency.

- **Model:** `nano_banana_pro`
- **Aspect:** `1:1`
- **Cost:** ~2 credits each
- **Count:** 2–4 mnemonics depending on tier
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §1–§2 (material — fabric weight + weave/knit), §5 (Embroidery) or §6 (Print methods) for the rendering technique, §8 (Trims & hardware — woven label / jacron / leather patch / hangtag), §9 (Typography & display — wordmark treatment), §10 (Photography & lighting — light direction, raked vs top-down).

Each mnemonic is a single artifact shown at macro scale on a clean ground. Pull from the brief's `## Motif library`, `## Embellishment plan`, and `## Typography` sections. A representative set:

1. **Wordmark on a swatch** — the property name (not the brand's real wordmark) embroidered / chain-stitched / silkscreened on the brand's hero fabric in the brand's display treatment.
2. **Signature motif on a swatch** — the brief's #1 motif rendered in the brief's chosen embellishment technique on a small piece of the hero fabric.
3. **Palette tile** — a row of fabric squares in the brief's 4–6 palette colors, with mono color names lettered below each.
4. **Hangtag macro** *(deluxe only)* — the brand's hangtag rendered as a paper/leather/woven artifact with mono data, stitching/grommet visible.

**Prompt template:**
> Macro studio photograph of {{mnemonic — wordmark on fabric / motif on fabric / palette tile / hangtag}}. {{Specific material — brushed merino-cotton, supplex nylon, raw cotton canvas, etc.}} in {{specific color}}. The {{wordmark / motif / pattern}} is {{embellishment technique — chain-stitch / woven label / discharge silkscreen / sublimation}} in {{thread/ink colors}}, reading {{exact text or motif description}}. {{Detail of the technique — visible thread loops, merrowed edge, fiber detail}}. {{Light direction, raked or top-down}}. Tight square crop. Like a sample card from a heritage merch atelier.

Fire all mnemonics in parallel. **Poll to completion.** Save the job_ids — they're the reference library for Round 3.

---

### Round 3 — Piece mockups

Each SKU as an individual flat-lay product hero on a clean seamless backdrop. **This is where `medias[]` starts paying off** — reference one or more Round 2 mnemonics so the embellishment technique, thread color, and fabric language stay consistent across every piece.

- **Model:** `nano_banana_pro`
- **Aspect:** `4:5`
- **Cost:** ~2 credits each
- **Count:** 4 / 6 / 9 SKUs by tier
- **References:** pass the relevant Round 2 mnemonic job_id(s) via `medias`
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §1 (Fabric weights — oz / GSM), §2 (Weaves & knit structures), §3 (Fits & silhouettes — boxy / cropped / oversized / raglan / etc.), §4 (Seams & construction — flatlock / bartack / topstitch / single-needle / piping), §5 (Embroidery technique), §6 (Print method), §7 (Washes & finishes — garment-dyed / pigment / sun-faded / etc.), §8 (Trims & hardware — labels, patches, closures), §10 (Photography & lighting — soft directional light clause). **Pick 2–4 specific terms per prompt clause** — don't keyword-stuff or the model produces a confused composite.

Pull from `## Range plan` in the brief — generate one mockup per row, ordered hero pieces first.

**Prompt template:**
> Studio product photograph of a single {{garment}} laid flat on a clean {{neutral backdrop color from brief}} seamless backdrop. {{Fabric weight + technique — 8oz garment-dyed jersey, 14oz brushed-back fleece, paneled supplex nylon, brushed merino-cotton knit, etc.}} in {{specific colorway}}, {{fit notes — cropped boxy, oversized dropped-shoulder, regular fit with horn buttons, etc.}}. Embellishments per brief: {{precise description — placement, technique, color, scale, exact wordmark text matching the brief}}. Soft directional light from upper-left, gentle shadow under the garment, no model, no hands, no other props. Editorial catalog quality, sharp focus on every embellishment loop and seam.

**MCP call shape:**
```
mcp__higgsfield__generate_image(params={
  model: 'nano_banana_pro',
  aspect_ratio: '4:5',
  resolution: '2k',
  prompt: '<built from template>',
  medias: [
    { value: '<Round 2 wordmark mnemonic job_id>', role: 'image' },
    { value: '<Round 2 motif mnemonic job_id>',    role: 'image' }
  ]
})
```

Fire all SKU mockups in parallel. **Poll to completion.** These job_ids become the input library for Rounds 4, 5, and 6.

---

### Round 3b — Hangtag + packaging concept *(optional — skip if not selected in scope gate)*

The first physical touchpoint a customer has with the brand. Currently most merch decks mention the hangtag in the brief but never render it — this round closes that gap. Generates the hangtag plus a packaging concept (poly bag with woven label, branded box, tissue paper, sticker pack — pick what fits the brief's tier).

Fires in parallel with Round 3 (mockups). Both depend on Round 2 mnemonics.

- **Model:** `nano_banana_pro`
- **Aspect:** `1:1`
- **Resolution:** `2k`
- **Cost:** ~2 credits each
- **Count:** 1 (quick) / 2 (standard, deluxe) — first image is the hangtag, second is the packaging arrangement
- **References:** Round 2 wordmark mnemonic + Round 2 motif mnemonic (in `medias[]`) so the typography and colors carry through
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §8 (Trims & hardware — hangtag, jacron, leather patch, debossing, woven label, grosgrain), §9 (Typography & display — wordmark treatment), §1 (paper / fabric weights if the tag is a heavy stock), §10 (raked side-light for the embellishment macro feel).

**Prompt template — hangtag:**
> Macro studio photograph of a single {{material — kraft card / coated card / leather / canvas-and-jacron / woven}} hangtag for the {{brand}} {{occasion}} merch capsule, lying on a {{neutral backdrop color from brief}} seamless backdrop. The tag is {{shape — rectangular / die-cut diamond / rounded-corner}}, {{size — 5×8cm / 6×10cm}}, attached to a {{cotton string / waxed-cotton cord / metal split-ring}}. Front side reads {{exact text from brief — brand wordmark + property name + edition mark + coordinates if applicable}} in {{display family from brief}}. Back side (visible at an angle) shows {{mono spec line from §1: fabric · weight · made-in}}. {{Surface treatment — debossed / hot-foil / printed / embroidered}} where appropriate. Raked side-light from upper-left for depth. Sharp focus on every letterform. Editorial catalog quality.

**Prompt template — packaging arrangement** *(standard/deluxe only):*
> Studio photograph of the {{brand}} {{occasion}} packaging arrangement on a {{neutral}} seamless backdrop, slightly angled overhead view. The composition shows: {{tier-appropriate package — e.g. a folded garment inside an open branded box with tissue paper, a poly bag with a woven label, a sticker pack, a wrapped care card / a heritage-tier wooden crate with branded tissue / a paddock-style courier mailer with sponsor strip}}. Brand wordmark visible on the box lid / poly bag / tissue paper. Tonal palette pulled from the brief — no extra colors. Soft directional light, editorial product styling. The arrangement reads as if the customer just opened it. No hands, no people.

Fire in parallel with Round 3 mockups. **Poll to completion** with the rest of that batch.

---

### Round 4 — Line sheet

The gridded composite. One image, all SKUs visible. References all Round 3 mockups via `medias[]` so the line sheet *matches* the individual pieces instead of drifting into a different visual rendering of them.

- **Model:** `nano_banana_pro`
- **Aspect:** `4:3`
- **Cost:** ~2 credits
- **References:** all Round 3 mockup job_ids in `medias[]`
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §1–§2 (vocabulary for the mono spec callouts under each piece — `fabric · weight` line), §7 (backdrop tone description if the brief calls for a specific wash-coded neutral). The composition itself is described prose-style in the target-structure block below — not pulled from the glossary.

**Prompt template:**
> Tech-pack flat-lay line sheet of the {{brand}} {{occasion}} merch capsule on a {{neutral backdrop color from brief}} seamless backdrop, soft top-down studio light, catalog presentation. Show {{N}} garments gridded in a {{4-across-by-2-down / 3×3 / etc.}} layout: {{list each piece with one-line spec}}. Each garment sits with even spacing, faint mono spec text below it (fabric · colorway · embellishment hint). No models, no hands, subtle drop shadows only. Wholesale line sheet quality.

**Target structure** for the line sheet image — read this carefully and bake every element into the prompt:

- **Grid:** clean and regular. 4-across-by-2-down for 8 SKUs; 3×3 for 9; 3×2 for 6. Even spacing, generous margins around each piece.
- **Backdrop:** a single neutral tone from the brief's palette (cream, bone, paper, off-white, etc.). No textures, no gradients.
- **Light:** even top-down studio light, soft drop shadows only, no harsh raking.
- **Spec callouts:** under each piece, three short lines of mono text — `fabric · weight`, `colorway`, `embellishment hint`. Faint and tonal, never loud.
- **Range across silhouettes:** the cells should cover different garment categories — a knit, a button-up, a tee, an outerwear piece, a footwear piece, an accessory or hat, plus whatever pieces are specific to the brief. Don't put eight tees in the grid.
- **Hierarchy:** all garments at the same scale and centered in their cells. No piece is hero in the line sheet — that's what the product hero shots are for.
- **Restraint:** zero stylization on the image itself. The garments do the talking; the grid is utility infrastructure.

The reference quality bar: a wholesale tech-pack page from a heritage merch agency — clean enough to send to a manufacturer.

Fire as a single call. **Poll to completion.**

---

### Round 4b — Wholesale sell-sheet *(optional — skip if not selected in scope gate)*

A B2B variant of the line sheet for retail-buyer conversations. Same composition language as Round 4 but annotated with wholesale pricing, MOQ, lead time, and SKU codes. Buyers care about different information than customers — this round gives the deck a sell-in surface alongside the sell-through one.

Fires immediately after Round 4 completes, taking the Round 4 line sheet as a `medias[]` reference so the composition matches.

- **Model:** `nano_banana_pro`
- **Aspect:** `4:3`
- **Resolution:** `4k` (B2B PDF readability)
- **Cost:** ~4 credits
- **Count:** 1
- **References:** Round 4 line sheet job_id in `medias[]`
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §1 (weight for the spec callouts), §2 (weave), §7 (wash) — same vocabulary as Round 4, with commerce annotations from `BRIEF.md` `## Commerce` (MSRP × 0.5 = rough wholesale; MOQ = brief-specified or 24 units default).

**Prompt template:**
> Wholesale sell-sheet for the {{brand}} {{occasion}} merch capsule, formatted as a B2B trade-show document. Same flat-lay grid composition as the reference line sheet, on a {{neutral backdrop from brief}} seamless backdrop, but with **expanded mono spec annotations under each piece**: SKU code (e.g. "RBAR-001-RJ-FOR"), wholesale price USD, MOQ, lead time in weeks, available colorways, available sizes. A small header bar at the top reads "{{Brand}} {{Occasion}} · Wholesale Line Sheet · {{Season}}" in mono. A footer line reads "Contact: {{contact placeholder}} · MOQ subject to availability · Lead time from PO". No models, no hands, even top-down studio light. Buyer-grade reference quality, designed to be printed at A4 / Letter.

Fire as a single call after Round 4 lands. **Poll to completion.**

---

### Round 5 — Model in environment

Lookbook portraits. Each shot composites three references via `medias[]`:
1. A Round 0 Cast portrait (the *person* — same character across all shots they're in)
2. A Round 3 mockup (the *garment* — same fabric, fit, embellishments as the flat-lay)
3. A Round 1 location plate (the *world* — same physical place as the establishing shot)

This is the round that needed the prior context most — without it, the lookbook drifts into generic AI-fashion territory, the garment drifts off-brief, and the man in shot A is a different man from the man in shot B.

- **Model:** `nano_banana_pro`
- **Aspect:** `4:5`
- **Cost:** ~2 credits each
- **Count:** 1 / 2 / 3 by tier
- **References:** Cast portrait + Round 3 mockup + Round 1 location (all in `medias[]`)
- **Cast assignment:** alternate which character wears which piece. Don't put the menswear hero piece on the female character and vice versa unless the line is genuinely unisex.
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §10 (Photography & lighting) — the lighting + film stock + focal-length clauses must echo the Round 1 location plate the shot is set in. Everything else (fabric, fit, embellishments) is carried into the composite by the Round 3 mockup reference in `medias[]` and doesn't need to be re-described in prose.

**Prompt template:**
> Editorial lookbook portrait, {{full-body / three-quarter / mid-shot}}. The character from the portrait reference wears the {{specific Round 3 garment}} in {{colorway}}, styled with {{trouser/shoe/accessory}}. Setting: the {{Round 1 location — described again concretely, not just referenced}}. {{Lighting matching the Round 1 plate — golden hour low side-light, hangar fluorescent overhead, etc.}}. Shot on {{35mm film stock / digital with medium-format feel}}, {{focal length}} equivalent compression. Subject {{posture / gaze}}. The {{garment}} is the hero; every embellishment readable. Composite the three references so the person matches the portrait, the garment matches the mockup, and the environment matches the location plate.

**MCP call shape:**
```
mcp__higgsfield__generate_image(params={
  model: 'nano_banana_pro',
  aspect_ratio: '4:5',
  resolution: '2k',
  prompt: '<built from template>',
  medias: [
    { value: '<best Round 0 cast portrait job_id for this character>', role: 'image' },
    { value: '<Round 3 specific mockup job_id>',                       role: 'image' },
    { value: '<Round 1 location job_id>',                              role: 'image' }
  ]
})
```

Fire all lookbook portraits in parallel. **Poll to completion.**

---

### Round 6 — Hero image

The cinematic 16:9 wide that anchors the website. Composites the same three reference types as Round 5 — but selects the strongest of each: the best Round 1 location plate, the hero-piece Round 3 mockup, and the Round 0 portrait of the character who wears the hero piece in the lookbook. The website then reads as "one consistent person, multiple shots, one consistent world."

- **Model:** `nano_banana_pro`
- **Aspect:** `16:9`
- **Cost:** ~2 credits
- **References:** Cast portrait (of the hero-piece wearer) + Round 1 best location + Round 3 hero-piece mockup (all in `medias[]`)
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §10 (Photography & lighting) — lighting + film stock + focal-length clauses must echo the chosen Round 1 location plate. The hero garment language is carried by the Round 3 mockup reference and doesn't need re-describing.

**Hero composition rule (unchanged from prior version of this skill):**

The hero tells the brand-world story in one frame. **Derive every element from `BRIEF.md`** — palette, setting, character archetype, embellishment, and a single brand-world cue. The recipe:

1. **Character** — one stand-in (never a named real person) fitting the brand's audience, in the hero piece + hero colorway. Pose relaxed, in motion or about-to-move — never posed-static or aspirational-staring-into-distance.
2. **Setting** — the single Round 1 location that anchors the brand world best. One place, not a mash-up.
3. **One atmospheric brand cue** — a single environmental detail that reads as "this is *that* brand's world" without being the subject. Treat it small, distant, in-shadow, or peripheral. Whatever the brief established as the brand-world anchor lands here, atmospheric not literal.
4. **Light + film stock** — golden hour or first light by default unless the brief says otherwise. Specify film stock or "medium-format feel" to push away from AI gloss.
5. **No literal collisions.** If the brief intersects two worlds (e.g. aviation × surf), the hero never composites them — pick the stronger one for the location and let the other live only in the merch on the character.

**Worked examples are illustrative of the RECIPE only — the cue type varies entirely with the brand.** Look at the *shape* of each example, not the vocabulary:

- Aviation/sport brand: character walks toward camera in hero piece; *small aircraft high overhead*. Cue = peripheral, aspirational, distant.
- Heritage country brand: character on a dirt road at sunset in hero piece; *taillights of a vehicle far behind them*. Cue = distant, atmospheric, narrative.
- Sponsorship/match brand: character near a venue entrance in hero piece; *rolled banners or signage propped against a wall behind them*. Cue = peripheral, ambient, contextual.
- Touring/music brand: character in a loading-dock alley at first light in hero piece; *road cases deep in shadow*. Cue = in-shadow, suggestive, behind-the-scenes.

Note what's consistent: character + setting from the brief's world + a single cue treated atmospheric (small / distant / shadowed / peripheral). The cue is **never** the subject. The merch is. The specific cue type is whatever the brief's brand-world dictates — vehicle, building element, equipment, signage, landscape detail — never imposed by the skill.

**Prompt template:**
> Cinematic wide editorial photograph, {{time of day}} at {{location — matching Round 1 plate}}. A {{age, vibe}} stand-in model {{action — walking, leaning, standing}} {{specific staging}}. They wear the {{brand}} {{hero garment from Round 3}} in {{colorway}}, {{embellishments described concretely}}. Styled with {{trouser/shoe/accessory specifics}}. The setting includes: {{1–3 environmental elements matching the Round 1 plate}}. {{ONE atmospheric brand cue — small, distant, peripheral, never centered. Phrase as "in the distance / high above / deep in shadow / far behind, a single ___"}}. {{Light direction matching Round 1}}. Shot on {{film stock}}, {{grain notes}}, {{focal length}}. Subject {{posture}}, looking {{direction}}. Editorial lookbook quality. Wide cinematic framing. The merch is the hero; the cue is atmospheric.

**MCP call shape:**
```
mcp__higgsfield__generate_image(params={
  model: 'nano_banana_pro',
  aspect_ratio: '16:9',
  resolution: '4k',
  prompt: '<built from template>',
  medias: [
    { value: '<Cast portrait job_id of hero-piece wearer>', role: 'image' },
    { value: '<best Round 1 location job_id>',              role: 'image' },
    { value: '<Round 3 hero-piece mockup job_id>',          role: 'image' }
  ]
})
```

Fire. Poll to completion.

---

### Round 7 — Hero video *(optional — skip if "Skip video" was selected in scope gate)*

A 5-second cinematic motion clip animating the Round 6 hero still. This is what plays as the website's full-bleed hero (autoplay, muted, loop). Subtle motion only — a slow push-in / dolly / horizontal pan / gentle wind through the garment / model continuing a walk-cycle. **Never a literal cut or camera move that breaks the still's composition.** If the still works, the video should feel like the still came alive.

- **Model:** `seedance_2_0` (reference-driven, strong identity preservation — uses the hero still as `start_image`)
- **Aspect:** `16:9`
- **Duration:** `5` seconds
- **Cost:** ~15 credits
- **Count:** 1
- **References:** Round 6 hero still job_id as `start_image` in `medias[]`
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §10 for the motion grammar (slow push-in, subtle parallax, golden-hour breeze, walk-cycle continuation).

**Prompt template:**
> {{Motion type — gentle slow push-in toward the subject / horizontal dolly tracking with the subject / subtle parallax of foreground vs background / soft breeze rippling the garment / model continues mid-step from the still}}. Hold the same composition, lighting, palette, and subject as the start image. Keep the {{atmospheric brand cue from the hero — small aircraft / vehicle in distance / signage / road cases — described as appearing in its original position}} stable through the clip. Subtle film grain throughout, no harsh cuts, no zoom-bursts, no camera shake. 5-second clip designed to loop seamlessly. Editorial cinematic register.

**MCP call shape:**
```
mcp__higgsfield__generate_video(params={
  model: 'seedance_2_0',
  aspect_ratio: '16:9',
  duration: 5,
  prompt: '<built from template>',
  medias: [
    { value: '<Round 6 hero still job_id>', role: 'start_image' }
  ]
})
```

Fire after Round 6 completes. **Poll to completion.** Video jobs take 60–180s — much longer than image jobs.

---

### Round 8 — Social cuts *(optional — only if "full motion package" was selected in scope gate)*

Two 9:16 vertical clips for TikTok / Instagram Reels. Same motion grammar as Round 7 but in vertical framing, designed for thumb-stopping social. **Composite from the same references** — the Cast portrait, the Round 6 hero (as a still + intent reference), and a Round 1 location.

Variants:
1. **Clip A — character-in-motion**: hero garment in vertical frame, character walks toward camera in the Round 1 location with the atmospheric brand cue visible. Short 5s loop.
2. **Clip B — embellishment macro motion**: tight 9:16 crop on the signature embellishment (chain-stitch detail / sponsor patches / chenille / etc.), slight push-in or tilt revealing the depth of the thread.

- **Model:** `seedance_2_0`
- **Aspect:** `9:16`
- **Duration:** `5` seconds each
- **Cost:** ~15 credits each (~30 total)
- **Count:** 2
- **References:**
  - **Clip A:** Cast portrait + Round 1 location + Round 3 hero mockup
  - **Clip B:** Round 3 hero mockup (or whichever piece carries the signature embellishment)
- **Vocabulary sources** ([`glossary.md`](./glossary.md)): §10 for the motion + lens grammar; §5/§6 for the embellishment vocabulary in Clip B.

**Prompt template — Clip A (character-in-motion):**
> Vertical 9:16 cinematic 5-second clip. The character from the portrait reference walks toward camera in {{Round 1 location described concretely}}, wearing the {{Round 3 hero piece described from the mockup}}. {{Motion type — gentle slow push-in / handheld walk-cycle / static frame with subject approaching}}. {{Light direction matching Round 1 plate}}. The atmospheric brand cue from the brief — {{small / distant / peripheral cue}} — visible behind the subject. Subtle film grain, no zoom-bursts, no harsh cuts. Designed to loop. Editorial register.

**Prompt template — Clip B (embellishment macro):**
> Vertical 9:16 macro motion clip, 5 seconds. Tight close-up on {{the signature embellishment from the brief — chain-stitch roundel / sponsor-patch constellation / chenille letterforms / discharge-print graphic / etc.}} on the {{fabric from the hero piece}}. {{Motion type — slow push-in / slight horizontal tilt / raked-light gradient passing across the surface}} revealing the depth of the thread loops / weave / ink layer. Soft directional light from the {{light direction}}. Sharp focus throughout. No cuts. Designed to loop. Editorial atelier macro register.

**MCP call shape (per clip):**
```
mcp__higgsfield__generate_video(params={
  model: 'seedance_2_0',
  aspect_ratio: '9:16',
  duration: 5,
  prompt: '<built from template>',
  medias: [
    /* Clip A: cast portrait + location + mockup */
    /* Clip B: mockup of the piece carrying the embellishment */
  ]
})
```

Fire both in parallel after Round 6 completes. **Poll to completion** — video jobs take 60–180s.

---

### Polling pattern (every round)

After issuing the round's parallel calls, poll each `job_id` with:
```
mcp__higgsfield__job_status(jobId='<id>', sync=true)
```
in parallel. `sync: true` blocks up to ~25s server-side and returns on terminal state. For image jobs (10–20s typical) this usually completes in a single poll round. If any return non-terminal, wait the `poll_after_seconds` value and try again.

**Save every `results.rawUrl` and `job_id` as you go** — write them into a working state structure (in your head or a scratch file). You'll need:
- `job_id`s for `medias[]` references in later rounds
- `rawUrl`s for `<img src>` values in the final `index.html`

---

## Phase 4 — Real brand logo

For the site nav and any "real-brand" lockups, use the **actual** logo file, not the AI-rendered approximations.

1. **First try the Higgsfield brand kit** (queued in Phase 1, almost certainly done by now after Phase 3 finishes):
   ```
   mcp__higgsfield__show_marketing_studio(
     action='get', type='brand_kit', brand_kit_id='<from phase 1>'
   )
   ```
   Check `data.logo` — but **inspect it visually before using**. The scraped logo from a brand's homepage is often a *campaign lockup* (e.g. "Dance Your Style Qualifier Northeast USA"), not the primary mark. If it's a campaign asset, skip to step 2.

2. **Fallback: Wikimedia Commons.** For major brands, the primary SVG mark almost always lives on Wikipedia. Find it by:
   ```bash
   curl -sL -A "Mozilla/5.0" "https://en.wikipedia.org/wiki/<Brand>" | \
     grep -oE 'upload\.wikimedia\.org/[^"]+\.svg' | head -10
   ```
   Then download the SVG. SVGs scale crisply at any size — preferred over PNGs.

3. **Last resort:** search via `/browse` or WebSearch for "<brand> logo SVG site:wikimedia.org" or "<brand> brand assets press".

4. Save as `logo-<brand-slug>.svg` (or `.png`) in the working folder.

---

## Phase 5 — Compose the deliverable

In the working folder, write these files plus the logo:

```
~/Documents/merch-briefs/<brand-slug>-<YYYY-MM-DD>/
├── BRIEF.md           ← from Phase 2 (palette, motifs, range, audience, commerce)
├── TECHPACK.md        ← manufacturer-side production spec (this phase)
├── INDEX.md           ← gallery of all job IDs + prompts (incl. video clips)
├── index.html         ← branded single-page site (video embedded in hero)
├── og.png             ← 1200×630 social share card (= cropped Round 6 hero still)
├── build_og.py        ← tiny script that builds og.png
└── logo-<brand>.svg   ← from Phase 4
```

The site loads display + label fonts via the **Google Fonts CDN** in the HTML's `<link>` tag — no local TTFs needed. The OG card is just a cropped version of the hero still, so no fonts are needed for the build step either.

### 5a — `TECHPACK.md` (manufacturer-side production spec) *(optional — only if selected in scope gate)*

Where `BRIEF.md` is creative-side (the contract with the design team), `TECHPACK.md` is production-side (the contract with the cut-and-sew factory). It's the document a manufacturer can quote against and start sampling from.

**Skip this file entirely if the user did not select TECHPACK.md in the scope gate.** Don't write a half-baked version.

Required sections:

```markdown
# {{Brand}} — {{Occasion}} · Tech Pack

*Produced from BRIEF.md · Date: {{today}} · Status: concept (not approved for bulk)*

## Production approach
- **Construction tier:** {{premium / mid / value — based on the brief's quality register}}
- **Country of make:** {{suggested COO based on materials — Portugal for premium knits, US for heavyweight tees, Vietnam for technical outerwear, etc.}}
- **Sampling:** {{1 sample per SKU per colorway, 2-week turnaround target}}

## Per-SKU spec sheets

### SKU 01 — {{Piece name}}
- **Fabric:** {{exact weight + composition — "320 GSM 100% organic cotton, garment-dyed loopback"}}
- **Mill reference:** {{placeholder — "to be sourced from heritage Italian/Japanese/American mill"}}
- **Fit profile:** {{boxy / cropped / relaxed — from §3 of glossary}}
- **Size run:** {{XS–XXL standard; or specified buy depth from BRIEF.md `## Commerce`}}
- **Measurements (Size M, chest-pit-to-pit / body length / sleeve / shoulder):** {{cm — placeholder for designer to fill}}
- **Seams & construction:** {{from §4 of glossary — flatlock at side seams, bartack at pocket corners, coverstitched hem, etc.}}
- **Embellishment placements:**
  - Position 1 (e.g. left chest, 4cm down from collar, 5cm from placket): {{technique from §5/§6 of glossary — "chain-stitch embroidery, 3-thread, tonal cream-on-cream, motif: {{name}}, 8cm wide"}}
  - Position 2 (e.g. back yoke, centered, 12cm down from collar): {{...}}
- **Labels:**
  - Inside-neck: {{satin woven label from §8 of glossary, dimensions, attachment method}}
  - Sleeve / hem flag: {{if applicable}}
  - Care label: {{stitched into side seam at hem, regulatory wash + COO info}}
- **Hardware:** {{horn buttons / corozo / YKK metal zipper / etc. from §8}}
- **Hangtag:** {{material + dimensions + attachment from §8}}
- **Packaging:** {{poly bag with woven label / branded box / tissue paper — from Round 3b output}}
- **Estimated FOB:** {{rough manufacturer-side cost per unit, USD — placeholder for sourcing team}}

### SKU 02 — {{...}}
{{repeat per piece}}

## Color & material reference
- **Pantone matches (placeholder):** {{Cream — Pantone 11-0907 TCX; Forest — Pantone 19-5511 TCX; etc.}}
- **Thread colors:** {{cream chain-stitch thread, yellow chain-stitch thread, etc.}}
- **Fabric supplier reference numbers:** {{placeholder for designer to source}}

## Bill of materials (rolled up across SKUs)
| Material | SKUs that use it | Estimated yardage / units per drop |
|---|---|---|
| 320 GSM organic cotton loopback | 01, 02 | ~{{yards}} |
| Heavy cotton piqué | 04 | ~{{yards}} |
| ... | | |

## Regulatory notes
- Care label content (wash + COO + fiber composition) must be permanent and bilingual where applicable.
- All zippers / snaps / hardware lead-content compliant with destination market regulations (CPSIA for US children's lines, REACH for EU, etc.).
- Tariff classification (HTS code) per garment category to be confirmed by freight forwarder.

## Quality control checkpoints
- **Pre-production sample (PPS):** approved before bulk cut.
- **Top-of-production (TOP):** first 10 units inspected before full bulk runs.
- **AQL inspection:** 2.5 major / 4.0 minor for final shipment.

## Open questions for the manufacturer
- ...
- ...
```

This is **explicitly a concept tech pack** — measurements, mill references, and Pantone codes are placeholders for the user's designer / sourcing team to fill in for real production. The skill's job is to produce a document with the right *structure* and the right *technical vocabulary* (pulled from `glossary.md`), not to invent measurements that don't apply to the actual brand.

### 5b — `INDEX.md`

Gallery linking the brief sections to each generated artifact, with the prompt and Higgsfield job ID for each. Format:

```markdown
# {{Brand}} — Visual Tech Pack

[Read the brief →](./BRIEF.md)

*Generated YYYY-MM-DD · {{tier}} tier · {{N}} images · {{credits}} credits*

To re-display any artifact: `mcp__higgsfield__job_display` with the job ID.

## 1 · Range Grid (Hero)
- **Job:** `<id>`
- **Model:** `nano_banana_pro` · **Aspect:** 4:3 · **Resolution:** 1k
- **Prompt:** > {{full prompt}}

... etc. for each artifact ...
```

### 5c — Pick fonts for the site

Pick a **display family** and a **label/mono family** based on the brief's `## Typography` section. The choice is brand-driven — examples of valid pairings, not a prescription:

| Brand type | Display family (example) | Label/mono (example) |
|---|---|---|
| Sport / paddock / aviation | A condensed italic grotesque (e.g. Barlow Condensed Black Italic) | A clean technical mono (e.g. JetBrains Mono) |
| Heritage / country / archive | A wide serif or slab (e.g. Recoleta, Domaine Display) | A typewriter mono (e.g. IBM Plex Mono) |
| Luxury / restraint | A high-contrast serif (e.g. Editorial New, Canela) | A geometric sans (e.g. Söhne) |
| Streetwear / festival | A heavy display sans (e.g. Druk Wide, ABC Diatype) | A condensed mono (e.g. Berkeley Mono) |

Use **Google Fonts** families so the HTML can load them via the standard `<link>` CDN tag — no local TTFs required:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=<DisplayFamily>:ital,wght@0,400;0,900;1,700;1,900&family=<MonoFamily>:wght@400;500;700&display=swap" rel="stylesheet">
```

The OG card doesn't render any text, so no font files are needed for the build step. Anything outside Google Fonts is fine for the site if you self-host it, but Google Fonts is the path of least resistance.

### 5d — `index.html` (branded single-page site)

**Structural sections (top to bottom). Each section has a *role*; the brand picks the noun-phrase title to put on it.**

1. **Optional top ornament** — a thin marquee strip / sponsor band / news-ticker / data-band, only if it fits the brand vibe. Skip for restrained / luxury brands; include for sport / festival / streetwear.
2. **Sticky nav** — `[real brand logo SVG] | [property name set in the brief's display family]` on the left; small mono stamp on the right (coordinates, date, edition number — whatever the brief established).
3. **Full-bleed hero** — Round 7 hero video at native 16:9 (autoplay, muted, loop, `playsinline`), with the Round 6 still as the `poster` attribute so the hero shows instantly on slow connections. Overlaid:
   - Small mono kicker (top-left or top-center)
   - Title in the brief's display family (bottom-left over a gentle gradient overlay)
   - Up to 3 short mono meta chips beneath the title

   HTML pattern:
   ```html
   <header class="hero">
     <video autoplay muted loop playsinline poster="<Round 6 still CDN URL>">
       <source src="<Round 7 video CDN URL>" type="video/mp4">
     </video>
     <div class="hero-overlay">
       <p class="kicker">...</p>
       <h1>...</h1>
       <ul class="meta-chips">...</ul>
     </div>
   </header>
   ```
4. **§01 Range** — the line sheet (Round 4 image), full-width inside a tonal frame, single-line mono caption below.
5. **§02 Featured pieces** — 2- or 3-column grid of product hero cards. Each card = a Round 3 mockup + a spec sheet (mono key/value pairs).
6. **§03 Lookbook** — Round 5 portraits in a 1- or 2-column grid. Often a darker / inverted-palette section so the figures pop.
7. **§04 Detail** — Round 2 mnemonics in a 2-column macro grid (the embellishment / motif / palette-tile close-ups).
8. **§05 Context** — wide contextual placement, often a 5:3 image+copy split. One image, one short caption.
9. **§06 Brief** — palette swatches + range table side-by-side. No prose.
10. **Footer** — 3–4 short mono columns (brief metadata, coordinates, render stack, note), small colophon line.

**Section titles are noun-phrases derived from the brief.** Defaults are *Range / Featured / Lookbook / Detail / Context / Brief* — but a brand might call its Context section "On the road" or "Off-season" depending on its world. Never use the example titles literally if the brand wants different ones.

**Copy discipline (this is non-negotiable):**
- Section heads are nouns or short noun-phrases derived from the brand's world. One or two words preferred.
- No "ledes" or "subtitles" under section heads. The image and the spec card do the talking.
- No agency-speak: never use "fluid medium", "smart-not-literal", "the proof the line is real", "two X one Y", "elevated international register", "the day after the night before", "carries the line / throws it back / softens it", or any other tortured "X meets Y" / "where A meets B" formulation.
- Caption format: `<noun-phrase>` · `<technical detail>`. Plain factual phrases, not literary.
- Spec cards: 4 fields max (Fabric / Fit / Color / Detail). Each field is a noun phrase, not a sentence.
- Hero meta: max 3 chips. Avoid "pillar / audience / drop window" pseudo-fields — use concrete chips like piece count, season, location.

**CSS design tokens — role-based, populated from the brief's palette.** Use these *role names* in the stylesheet, not stylized palette names. The hex values come from the brief; the roles stay constant across brands.

```css
:root {
  --bg:           #__;  /* primary neutral / page background */
  --bg-card:      #__;  /* tonal depth for cards (slightly darker/warmer than --bg) */
  --bg-shadow:   #__;   /* hairline border tone */
  --depth:        #__;  /* depth color used for dark sections (often a navy/ink) */
  --hero:         #__;  /* the brand's hero color — most prominent garment color */
  --secondary:    #__;  /* secondary brand color */
  --accent:       #__;  /* single bright accent, used sparingly */
  --sigil:        #__;  /* brand red / signature color, sigil-only (never a field) */
  --hardware:     #__;  /* neutral grey for labels / hardware tone */
  --ink:          #__;  /* body text / deepest neutral */
}
```

Populate from the brief's `## Palette` section. The number of fields can shrink (a 4-color brief uses fewer role tokens) but the names stay the same so the rest of the CSS is portable.

**Typography stack — two families chosen per Section 5b:**

- **Display family**: drives titles, section heads, the hero word, big numeric callouts. Reach for the weight/style the brief calls for (italic black, condensed bold, high-contrast serif, etc.).
- **Label/mono family**: drives kickers, captions, spec-sheet key/value pairs, footer columns, the marquee strip if present.

Generic CSS pattern:
```css
.display-title  { font-family: var(--display); font-weight: 900; }
.display-sub    { font-family: var(--display); font-weight: 700; }
.label, .mono   { font-family: var(--mono); letter-spacing: 0.18em; text-transform: uppercase; }
.spec-key       { font-family: var(--mono); font-size: 9.5px; letter-spacing: 0.18em; }
.spec-val       { font-family: var(--mono); font-size: 11px; }
```

Letter-spacing for tracked all-caps mono labels: `0.18em–0.28em` (tighter for body mono, looser for tracked all-caps).

**Open Graph + Twitter meta** in `<head>`:
```html
<meta property="og:type" content="website">
<meta property="og:title" content="{{Brand}} · {{Occasion}}">
<meta property="og:description" content="{{1 short sentence}}">
<meta property="og:image" content="og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="og.png">
<meta name="theme-color" content="{{forest or hero color}}">
```

### 5e — `build_og.py` (OG card builder)

The OG card is **just the Round 6 hero still, resized and center-cropped to 1200×630**. No text overlay, no left band, no ornaments. The image is the message. This keeps the OG card consistent with what the user already sees on the website hero and removes any drift between rendered text and the rest of the brand.

A tiny Python script — drop it in the working folder, run with `uv run --with Pillow build_og.py`:

```python
"""Build og.png (1200×630) from the Round 6 hero still.

The OG card is just a cropped version of the hero. No text overlay.
"""
import io, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / "og.png"
HERO_URL = "<Round 6 hero still CDN URL>"

W, H = 1200, 630

with urllib.request.urlopen(HERO_URL, timeout=30) as r:
    hero = Image.open(io.BytesIO(r.read())).convert("RGB")

# Cover-crop to 1200×630 (16:9 hero ≈ 1.78:1; OG is 1.905:1, so a slight
# horizontal crop happens. Center the crop.)
src_w, src_h = hero.size
scale = max(W / src_w, H / src_h)
new_w, new_h = int(src_w * scale), int(src_h * scale)
scaled = hero.resize((new_w, new_h), Image.LANCZOS)
x0, y0 = (new_w - W) // 2, (new_h - H) // 2
og = scaled.crop((x0, y0, x0 + W, y0 + H))

og.save(OUT, format="PNG", optimize=True)
print(f"wrote {OUT}")
```

After writing the file, run `uv run --with Pillow build_og.py` and confirm `og.png` lands in the working folder. The whole thing is ~25 lines of Python, no fonts dependency.

If the brief explicitly asks for an OG card *with* text overlay (e.g. for a launch announcement that needs the date + CTA visible in share previews), that's a deliberate override — but the default is image-only.

### 5f — Important: don't download generated images or videos

Higgsfield's CDN serves the 9 + 1 generated images directly. **Embed them in the HTML by CDN URL** — don't `curl` them into the repo. The site references `https://d8j0ntlcm91z4.cloudfront.net/...` URLs and stays small. The only image committed to the repo is `og.png` (which is built from one CDN asset by `build_og.py`).

### 5g — `README.md` and `.gitignore`

Always add a brief `README.md` explaining the deliverable and a `.gitignore` (default: `.DS_Store .vercel/ __pycache__/ *.pyc .venv/ venv/ node_modules/`).

The `Launch preview` hook will surface `index.html` to the user as soon as it's written. No need to `open` it manually.

---

## Phase 6 — Ship *(optional, gated)*

Only execute Phase 6 if the user explicitly says "ship", "deploy", "publish", "push it live", or sets `ship=true`. **Always gate before pushing or deploying** — these are externally-visible actions.

### 6a — GitHub: private repo + push

```bash
cd ~/Documents/merch-briefs/<brand-slug>-<YYYY-MM-DD>
git init -q -b main
git add -A
git commit -q -m "Initial concept deck — <Brand> · <Occasion>"
gh repo create <repo-name> \
  --private \
  --source=. \
  --remote=origin \
  --description "Concept merch tech-pack deck — <Brand> × <Occasion>" \
  --push
```

Pick a short, distinctive `<repo-name>` (e.g. `rbar-venice-beach`, not the long dated folder name).

### 6b — Vercel: deploy under the right team

1. Confirm the user's Vercel team slug: `vercel teams list`
2. Deploy to production:
   ```bash
   vercel --prod --scope <team-slug> --yes --name <repo-name>
   ```
3. Connect the deployment to the GitHub repo for auto-deploy on push:
   ```bash
   vercel git connect --scope <team-slug> --yes
   ```

Surface the production URL (e.g. `https://<repo-name>.vercel.app`) and the inspector URL to the user.

### 6c — Future iteration

Any subsequent change (new image, copy tweak, new section) becomes:
```bash
git add . && git commit -m "..." && git push
```
Vercel auto-deploys on push to `main`. Preview URLs come from PR branches.

---

## Iteration loop

After delivery, common iteration asks:

| Ask | Move |
|---|---|
| "Show more variants of piece X" | Reuse the prompt from `INDEX.md`, tweak the colorway/material/embellishment, regenerate via `generate_image` |
| "Different model in the lookbook" | Re-run Round 0 with the new character description, then re-run the affected Round 5 shots passing the new Cast `job_id` |
| "Add a new piece (e.g. boardshort)" | Add a row to the range plan in `BRIEF.md` + the table in `index.html`, generate one new product hero |
| "Different content in the top ornament strip" | Adjust the `.strip-inner` text in the HTML; also adjust the OG card's bottom-right ornament strip if used |
| "Change palette" | Edit the CSS custom properties in `index.html` + the RGB tuples in `build_og.py`, re-run the OG script |
| "Different hero image" | Re-issue the Phase 4 prompt with adjustments, swap the `<img src>` in the hero section |
| "Add the real logo" | Phase 5 — Wikimedia → `logo-<brand>.svg` → add to nav, replacing any homemade glyph |
| "Ship it" | Phase 6 |

If the user wants a re-rendered OG card after a brand change, **regenerate** by re-running `build_og.py` — don't try to edit the existing PNG.

---

## Guardrails

- **Real-person likeness:** never name a real public figure as the model in any prompt. If the brand is associated with an artist/athlete, describe a stylistic stand-in ("a young athlete with comparable energy"), not the person.
- **Trademark fidelity:** wordmarks in generated images are approximate. **The real logo only lives in `logo-<brand>.svg` in the nav** — never composite the real logo onto a generated image. Always note in the brief and footer that this is a concept deck, not production artwork.
- **Credit spend:** standard tier = 9 + 1 = ~17 credits. Deluxe = ~23 credits. Always preflight cost and confirm before bulk generation.
- **Don't edit images.** When the user asks to "use the real logo on the site" or similar, that means **the HTML**, not the AI-generated images. The 9 tech-pack images and the hero stay as Higgsfield generated them. Compose around them, never on top of them.
- **Originality:** when researching a brand's past merch, treat it as reference, not template — the deliverable should feel like the *next* drop, not a copy of last year's.
- **Ship gating:** Phase 6 publishes externally visible artifacts (GitHub repo, Vercel URL). Always confirm before running. A `--private` repo is the default for personal accounts.
- **Brand-kit logo scrutiny:** Higgsfield's brand-kit fetch often returns a *campaign lockup* rather than the primary mark. Always inspect visually before using. Wikimedia Commons is the canonical source for primary brand marks.

---

## Example invocations

> "Make merch for Bacardi for the Puerto Rico vs. Mexico football match."
→ brand=Bacardi, occasion="Puerto Rico vs Mexico football, 2026", creative_direction derived, tier=standard, ship=false.

> "Burberry restaurant pop-up merch, soft and refined, no logos screaming. Build the deck and ship it."
→ brand=Burberry, occasion="restaurant pop-up", creative_direction preserved verbatim, tier=standard, **ship=true** (run Phase 7).

> "Tour merch for Keshi's Requiem tour — dark gothic vintage washed."
→ brand="Keshi", occasion="Requiem Tour 2026", creative_direction="dark gothic vintage washed", tier=deluxe, ship=false.

> "Red Bull Air Race in Venice Beach. Aviation + surf where it's smart. Elevated international. Standard. Ship it."
→ brand="Red Bull Air Race", brand_url="https://www.redbull.com", occasion="Venice Beach edition", creative_direction preserved, tier=standard, **ship=true**.

> "Stagecoach Archive Edition merch — country heritage, warm wash, derive a palette from the brand."
→ brand="Stagecoach", occasion="Archive Edition", creative_direction preserved, tier=standard.

> "Tour merch for an indie band — backstage / road-case aesthetic. Deluxe."
→ brand="<artist name>", occasion="<tour name> Tour 2026", creative_direction="backstage / road-case aesthetic", tier=deluxe.
