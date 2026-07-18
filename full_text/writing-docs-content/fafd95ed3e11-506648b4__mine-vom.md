---
name: mine-vom
type: producer
version: "1.1.1"
recommended_model: sonnet
layer: territoire
reasoning_pattern: matrix-driven
matrix_mode: coding
consumes:
  - path: resources/frameworks/vom-mining.md
    min_version: 1.0.0
  - path: docs/doctrine/breakthrough-advertising-5-stages.md
description: >
  v1.1.1 (v2.61 doctrine consume) · consumes: enrichi avec refs docs/doctrine/ NEW v2.60 (breakthrough-advertising-5-stages). Skill peut consume ces doctrines canon pour informer production sans dépendre schemas exacts.
  v1.1.0 (v2.58 coverage extend) · brand.market.awareness_distribution write-side · brand.market.regulatory write-side · brand.seasonality write-side · spec.competitive_comparison feature-by-feature write-side. Closes 4 orphans audit v2.57.
  Voice of Market mining. Captures what the broader niche says · competitors'
  customer reviews, niche community forums (Reddit subs, niche Discord),
  comparison content, listicles, niche hashtags, industry analyst videos.
  Extracts vernacular, sophistication signals, white spaces, selective Porter
  forces. Produces a synthesis paragraph naming the niche dynamics that the
  operator's brand must adapt to, plus structured mutations into brand.json
  market.* and audiences profile.json voice.market_vernacular[].
  FR: "vom {brand}", "audit le marché", "scrape ce que dit la niche", "mine les conversations marché", "voice of market".
  EN: "vom {brand}", "audit the market", "mine niche conversations", "voice of market".
permissions:
  reads: [brand, product, profile]
  writes: [brand, profile, learning]
  emits_events: [coherence_check]
  mode: proposed
  subagent_safe: true
pipeline:
  preconditions: brand exists with brand.json filled. market.competitors[] preferably populated; pre-step will offer to discover if empty.
  postconditions: niche synthesis delivered, Layer A corpus in sources/vom/, Layer B mutations proposed, finalize-mutation-batch event emitted
disambiguates_against:
  mine-voc: "route to mine-voc when operator wants brand-bound customer voice (their own customers' reviews), not market-level conversations"
  watch-competitors: "route to watch-competitors when operator wants recurring monitoring of competitors' paid creatives · that's continuous, mine-vom is one-shot qualitative"
  mine-audience: "route to mine-audience when operator wants product-level audience discovery from website scraping, not market-level voice mining"
  ingest-resource: "route to ingest-resource when operator drops a single market report/document"
---

## Tone

Synthesis-first, prose-first. The operator reads a strategist's read of the niche, not a competitor benchmark. Three movements of plain prose. No titles, no bold-section anchors, no enumerated "Block 1 · Competitor X / Block 2 · Competitor Y", no `Porter's 5 Forces:` template, no exposed numbers, no internal jargon. Schema field names stay in the agent's head. The operator hears `observé / déduit / déclaré / incertain`, never `confidence: 0.7` or `source_type: forum_thread`.

Reference for synthesis voice: `.skills/skills/snapshot-brand/SKILL.md § Step 7`. Same canon, different domain. Three paragraphs, blank line between, end with one binary question. Read it before shipping.

The skill exists for the synthesis paragraph. Layer A corpus and Layer B mutations are downstream artifacts. If the synthesis reads like a roll call, the run is invalid even if all mutations write cleanly.

## Expert methodology

The agent operates as a senior strategy consultant who has read every active forum thread in the niche and triangulated against competitor reviews and listicles before naming a single market dynamic. The persona matters because it gates output shape. A consultant does not list 47 reviews and call it analysis. A consultant names two or three load-bearing things, grounds each in three independent sources, and tells the operator what to do.

Framework canon: `resources/frameworks/vom-mining.md`. Mandatory read at first invocation. Four lenses applied selectively and in order · vernacular extraction, sophistication signal, white-space identification, selective Porter forces. The agent does not run all four for completeness. It runs the lenses that have signal and skips the ones that do not.

## Step 0 · First-party data ask

**Si MCP youtube-transcript absent** · AskUserQuestion 2 options ·
- (a) "Je te guide pour connecter youtube-transcript maintenant (2 min via connect-mcp-server)"
- (b) "Je bascule en mode manual paste (tu colles les transcripts ou URLs, je structure)"
Default proactif proactif · (a) si l'opérateur a le temps.

Before scraping anything, ask the operator what they already have. Operators routinely have notes from sector conferences, paid Statista or Mintel reports, terrain observations from sales calls, or screenshots of Reddit threads they captured on the fly. Mining public sources when the operator already holds curated material is wasteful and produces weaker synthesis.

Ask, verbatim:

> *"Avant que je scrape la niche, est-ce que tu as :*
> *· Des notes prises en conférence sectorielle ?*
> *· Des reports payants (Statista, Mintel, Euromonitor) à digérer ?*
> *· Des observations terrain ou retours commerciaux sur ce que dit le marché ?*
> *· Des screenshots Reddit / forums / Discord captés à la volée ?*
> *· N'importe quoi de matière marché que tu as déjà collectée.*
>
> *Si oui, drop ici, je le digère en priorité.*
> *Si non, je pars sur les sources publiques (forums, Trustpilot concurrents, listicles, YouTube)."*

Branch on response. If the operator drops first-party material, route through `ingest-resource` first to digest it into structured form, then resume `mine-vom` with the digested intel as a primary corpus anchor and public sources as triangulation. If the operator has nothing, the skill proceeds on public sources only and flags this in the synthesis close so the operator knows the read was constructed from observable discourse alone.

## Step 1 · Pre-step: competitor integrity check

Read `brand.json#market.competitors[]`. If the array is empty or holds fewer than three entries, mining proceeds against the wrong substrate and the entire run produces noise. This is the highest-cost failure mode for the skill, and the doctrine forbids assuming `market.competitors[]` is curated.

Surface the gap to the operator:

> *"Pour mine la voix du marché, j'ai besoin de tes 3-5 concurrents principaux. Tu peux me les nommer, ou je peux les identifier en cherchant 'meilleur {sector} 2026' + listicles concurrentiels (5 min)."*

If the operator names competitors, write them through `.skills/write-to-context.py` in `mode=proposed` and continue. If the operator delegates discovery, run a tight listicle pull · two or three "best {category} {year}" pages, identify recurring names appearing in two or more sources, stage the proposal via `.skills/stage-proposal.py`, and let the checkpoint-resolver hook handle operator confirmation. Never auto-write competitors without operator confirmation. The pre-step exists to close the most expensive failure mode in this skill · mining the wrong competitors poisons every later lens.

## Step 2 · Niche definition

Lock the niche tuple before any crawl. Sector plus sub-vertical plus geography, pulled from `brand.json#identity` and `brand.json#meta`. *Skincare* is not a niche. *Clean beauty for women 30-50 in France* is. *Supplements* is not a niche. *Longevity stack for performance-oriented men 35-55 US* is. The precision matters because every later lens is conditioned on it. Vernacular in clean-beauty FR has nothing to do with vernacular in clean-beauty US ; sophistication stage in mass protein US has nothing to do with sophistication stage in niche longevity stacks.

If the sub-vertical is missing or ambiguous in `brand.json#market.market_overview.category`, ask one targeted question to disambiguate before crawling. If the hero product spec contains the category and `market_overview.category` is empty, infer from `products/{hero}/spec.json#identity.category` and flag the inference in the synthesis close so the operator can correct. Never proceed on a fuzzy niche definition.

## Step 3 · Source crawl plan

Build the crawl plan and surface it to the operator in one sentence per source category, then crawl. The operator should know what surfaces are being read before they are read, because the surface mix conditions the read. A plan reading "Trustpilot, Reddit FR, three listicles, two YouTube comparison videos" is concrete enough for the operator to challenge ("you're missing the Sephora reviews") before the agent burns budget.

Source categories, sized by niche.

**Competitor brand review surfaces.** Trustpilot pages for each top competitor, Amazon reviews on competitor SKUs when SKU-mappable, Sephora or Beauty Insider reviews when beauty, App Store or Play Store reviews when the competitor is app-shaped. These surfaces are gold because reviewers self-select to be specific about what failed and what worked. Cap thirty to fifty verbatims per competitor.

**Niche communities.** Reddit subreddits derived from the sector (`r/SkincareAddiction`, `r/SkincareAddictionFR`, `r/Supplements`, `r/xxfitness`, `r/CrossFit`, `r/Tretinoin`, niche-specific subs). Public Facebook groups when scrapeable. Niche Discord channels when the operator can paste an invite or transcripts. Industry-specific forums (`Bodybuilding.com`, `RealSelf`, `MakeupAlley`) when the niche has a canonical place to talk. Cap fifty to eighty verbatims per community.

**Comparison content.** Listicles ("best {category} {year}"), comparison blog posts ({competitor} vs {operator brand}), comparison YouTube videos chained through `mcp__youtube-transcript`. These surface the questions the market is actually typing · pure top-of-funnel pain language. Cap five to ten URLs per run.

**Industry analyst posts.** Forbes, TechCrunch, Vogue Business, sector-specific press, Substack newsletters. These read the niche from the outside and surface the framing the press has settled on. Cap three to five.

**Niche hashtags.** Twitter/X hashtag-bound threads (`#supplements`, `#skincare`, `#crossfit`), Instagram if accessible. Surface the social-proof shape and the influencer reply patterns.

**Wirecutter or professional review aggregators.** When applicable, the Strategist, NYT Wirecutter, Examine.com, PaulasChoice. These surface the editorial framing of the niche · comparative grids at stage 3-4, user profiles at stage 5.

The crawl plan also includes contrarian queries · `"why {category} doesn't work"`, `"{category} alternatives"`, `"{category} scam"` · to surface what the operator's framing misses. At least 10 percent of corpus must come from contrarian queries. Per `vom-mining.md § Anti-patterns / Filter-bubble queries`, a corpus that only confirms operator framing is a filter-bubbled run.

## Step 4 · Crawl with provenance and caching

Each entry captured carries provenance. URL, capture timestamp, source-type tag (`competitor_review | forum_thread | listicle | comparison_content | hashtag | analyst_post`), platform tag, recency tag (publish or post date). No verbatim ships into Layer A without all four.

Caps are firm. One hundred verbatims or threads per source maximum. Five hundred entries total per run. Larger pulls require explicit `--depth=deep` from the operator. The cap exists because synthesis past five hundred entries dilutes · the agent starts averaging across noise instead of triangulating across signal.

Caching layer at `brands/{slug}/sources/vom/_cache/` keyed by URL plus capture date. TTL seven days on competitor reviews and listicles since niche fundamentals do not shift weekly. Forums are refreshed if recency-sensitive (fast-moving niches like skincare actives or supplements where a 60-day-old thread can already be stale). Re-running `mine-vom` within the TTL reuses cached fetches transparently. Explicit `--fresh` flag forces a full re-pull.

Rate-limit handling uses exponential backoff. Trustpilot, Amazon, Reddit each have separate ceilings. When a source returns 0 results or hits a hard rate limit, the agent logs the failure and continues · no halt, no silent skip. The operator sees a plain-language note in the synthesis close: *"Amazon reviews unreachable today, the read is built on Trustpilot plus Reddit plus listicles, refresh in 24h if you want the Amazon layer."*

Anonymization rule for forum verbatims. Username is anonymized in Layer A and never surfaced to the operator. Thread URL is retained for traceability. Per the privacy posture in the brief · exposing usernames in a brand workspace is a different surface than they consented to.

## Step 5 · Four-lens coding per entry

Apply the canon at `resources/frameworks/vom-mining.md` to each entry. The four lenses are ordered because each conditions the next.

**Vernacular extraction.** Recurring expressions, niche shorthand. A token earns vernacular status only when it survives three binary tests at once · recurrence across at least three independent sources of different types, used without explanation, and the translation test (a beginner reading it cold would have to look it up). Reject any token that surfaces only on brand-controlled surfaces. Reject any token a copywriter could invent in five minutes · *glow*, *hydration*, *wellness* are not vernacular. Vernacular is the highest-leverage output of the skill because the words cannot be invented and they raise creative quality immediately.

**Sophistication signal.** One to five per Schwartz, applied to the niche, not the audience. Read top three players' hero copy, then reviewer vocabulary, then editorial framing. Two of three signals at the same altitude grounds the call. Mixed signals across two adjacent stages mean transit · flag it explicitly. Default skepticism: when in doubt between 4 and 5, write 4. Stage 5 is overclaimed by operators who confuse a vibey brand with a sophisticated one.

**White-space identification.** Recurring need expressed in market verbatims that no current top player addresses frontally as hero positioning. Three-part conjunctive test · recurs across three or more independent sources, no equivalent in any top-three-to-five competitor's hero positioning, phrasing concrete enough to ship as a landing-page H1 next week. A *competitive gap* (someone does this badly) is not a *white space* (no one names it at all). Cap three to five candidates per run.

**Selective Porter.** One or two active forces only. The activation tests live in `vom-mining.md § Section 4` · a force activates only when the verbatim corpus names its dynamic, naming the force changes a positioning recommendation, and a senior strategist looking over the operator's shoulder would mention it unprompted. Two of three yes · invoke. One or zero · skip and move on. The agent never runs Porter as a five-section template. If no force activates, drop Porter from the run entirely and say so.

Layer A entry structure, one row per verbatim:

```json
{
  "id": "VOM-001",
  "run_id": "vom-2026-04-24-001",
  "source_type": "competitor_review|forum_thread|listicle|comparison_content|hashtag|analyst_post",
  "source_platform": "trustpilot|reddit|youtube|sephora|amazon|substack|...",
  "source_url": "...",
  "captured_at": "2026-04-24T14:32:00Z",
  "competitor_anchor": "competitor-slug-or-null",
  "verbatim_or_summary": "raw text or summarized if >280 chars",
  "vernacular_tags": ["slugging", "barrier-repair"],
  "sophistication_signal": 3,
  "awareness_stage": "problem|solution|product|brand|most",
  "porter_force": "rivalry|new_entrants|buyer_power|supplier_power|substitute|null",
  "sentiment_direction": "positive_to_category|negative_to_category|mixed",
  "source_authority": "verified_buyer|expert_reviewer|anonymous_community|journalist|operator_pasted",
  "recency_days": 12
}
```

The operator never sees this structure. It is internal scaffolding. Operator-facing language stays plain · *"the niche uses 'slugging' constantly, this is now table stakes vocabulary"* not *"vernacular_tag with frequency=dominant"*.

## Step 6 · Pattern detection and cross-source triangulation

After coding, pool everything and run the cluster pass. Synthesis, not enumeration. Sonnet for the cluster (cost-justified by output quality). Haiku acceptable for vernacular tagging if cost matters at scale.

The triangulation rules are non-negotiable.

**Recurring vernacular** requires three or more independent sources of different types. Same word appearing five times in one Reddit thread is one source, not five. Independence is the test, not volume.

**Sophistication stage consensus** requires cross-source signal. Hero copy from top three players, reviewer vocabulary from top twenty most-upvoted threads of the last 90 days, editorial framing from three or more outlets. Two of three at the same altitude grounds the call. Mixed across adjacent stages is transit, flagged.

**White spaces** require recurring need (three or more independent sources) cross-referenced against top-three-to-five competitor positioning. The agent reads the competitors' hero copy, category pages, and homepage tagline before promoting a candidate. If any of them carries the claim, it is not white space.

**Active Porter forces** require cross-source naming of the force's dynamic. One thread complaining about price commoditization is not buyer-power signal ; the same complaint recurring across reviews, forums, and listicles is. The agent invokes a force only when the verbatim corpus repeatedly names its dynamic.

**Vocabulary shift detection** compares recent listicles against older ones (12-24 months). A niche moves up the Schwartz ladder when the dominant player's claim shape changes and the rest follow within 6-12 months. A vocabulary turn (the word *clean* becoming ironic in 30 percent of recent threads while *actifs prouvés* rises) is a load-bearing finding.

Hard rule: every claim that lands in the synthesis paragraph is grounded in three independent sources. Single-source claims are flagged as hypotheses or dropped. The agent does not generalize from one thread.

## Step 7 · Synthesis (mandatory format)

The deliverable. Apply `.skills/skills/snapshot-brand/SKILL.md § Step 7` voice canon strictly. Pure prose, three movements, blank line between each, no titles, no bold-section anchors, no labels marking each movement. The structure carries itself through what each paragraph names.

**Movement 1 · market structural shift.** Where the niche sits on the sophistication curve right now, where it is moving, and the load-bearing dynamic the operator's brand must adapt to. Sophistication transit (if the niche is moving), vocabulary evolution (if the niche's words are turning), or consolidation signal (if rivalry or new-entrants pressure is reshaping the field). One movement, three to five sentences. The lead is the most load-bearing finding, not the most procedural one.

**Movement 2 · vernacular extraction.** The vocabulary the niche uses now that the operator should adopt and the vocabulary that has aged out. Concrete tokens with one example sentence each. The operator leaves with five to ten exploitable expressions, not a glossary. Frequency tag stays in the agent's head · operator hears *"slugging is table stakes"*, not *"slugging tagged dominant with frequency 9 across forums"*.

**Movement 3 · white spaces or active Porter force.** Three white spaces named concretely (post-rétinol routines for clean beauty, three-product minimalist bundles, transparent compromise positioning) or the one or two active Porter forces the operator must defend or exploit. Concrete enough that the operator could ship a landing page next week with the claim as the H1. Generic *"opportunities to seize"* fails the test.

End with exactly one binary question:

> *"Want to validate and route these signals into the brand context, or dig into a specific white space?"*

Anti-patterns banned at synthesis. Never produce a "Competitor analysis" section. Never list "5 themes detected per competitor". Never run Porter as a five-section template. Never lead with a roll call. Never expose schema field names, source-type tags, sophistication integers, or recurrence counts. The synthesis is the analysis ; the analysis is not a benchmark.

## Step 8 · Routing to entity files (Layer B)

After the operator validates the synthesis, the agent stages mutations through `.skills/write-to-context.py` in `mode=proposed`. Every mutation carries a source block linking back to the run-id and the Layer A verbatim IDs that grounded it, so the operator can drill into any proposed write and see the evidence.

Routes.

**`brand.json#market.market_overview.sophistication_stage`** · single integer (1-5) computed from average `sophistication_signal` weighted by `recurrence_count`. Proposed update with two-sentence prose justification citing the three signals that grounded the call.

**`brand.json#market.awareness_distribution` (v2.58 write-side P3)** · ratio computed from theme-tagged awareness stages weighted by recurrence dans les verbatims niche. Distribution complète 5 stages canoniques Schwartz (`unaware`, `problem_aware`, `solution_aware`, `product_aware`, `most_aware`), floats sommant à 1.0. Stage en un seul write :

```bash
python3 .skills/write-to-context.py --path "brand.json#/market/awareness_distribution" --value '{"unaware":0.4,"problem_aware":0.3,"solution_aware":0.15,"product_aware":0.1,"most_aware":0.05}' --source agent --confidence 0.6 --mode proposed --reason "VoM analysis niche distribution"
```

Proposed shift cité par evidence (e.g. *"solution_aware 60% → product_aware 55%"* avec 3+ verbatims grounding la migration).

**`brand.json#market.competitors[].positioning`** · one-line synthesis per competitor, derived from their review themes. *"They win on speed, lose on transparency."* Enriched per competitor, never per-competitor blurb dumped into operator-facing output.

**`brand.json#market.external_intelligence[]`** · five to seven new entries per run, hard cap, per `watch-competitors` precedent. Each entry tags the signal type (`white_space_gap`, `vocabulary_shift`, `competitor_positioning_move`, `active_porter_force`), cites the verbatims, includes the one-line strategic implication.

**`brand.json#market.regulatory` (v2.58 write-side P4, objet complet)** · detect mentions regulatory / legal / compliance dans la niche. Trois sub-fields canoniques :

- `constraints[]` · claims interdits ou bornés dans la niche (ex *"ne peut pas claim weight loss"*, *"interdiction de revendiquer la guérison"*).
- `certifications_required[]` · certifications gating l'activité (ex *"EFSA approval"*, *"FDA clearance"*, *"Ecocert pour clean beauty"*).
- `advertising_restrictions[]` · restrictions canaux paid (ex *"Meta ad policy restrictions for {category}"*, *"Google Ads weight-loss policy"*, *"TikTok beauty restrictions FR"*).

Stage en un seul write (objet complet ; skip si zéro signal regulatory) :

```bash
python3 .skills/write-to-context.py --path "brand.json#/market/regulatory" --value '{"constraints":["claim weight loss interdit","claim healing interdit"],"certifications_required":["EFSA approval"],"advertising_restrictions":["Meta ad policy supplements","TikTok beauty FR"]}' --source agent --confidence 0.7 --mode proposed --reason "Regulatory mining niche"
```

Append si regulatory mentions surface (FDA letter referenced in three forum threads, ANSM warning in EU supplements category). Skip si no regulatory signal.

**`brand.json#seasonality` (v2.58 write-side P5, NEW field)** · analyser temporal patterns dans les verbatims niche (références saisonnalité, peaks holidays, troughs post-holiday, fêtes commerciales). Trois sub-fields :

- `peak_periods[]` · fenêtres haute demande (ex *"Q4-holiday"*, *"Q2-mothers-day"*, *"summer-skincare-actives"*).
- `trough_periods[]` · fenêtres basse demande (ex *"Q1-post-holiday"*, *"août-vacances"*).
- `notes` · string libre, contextualise les patterns détectés.

Stage :

```bash
python3 .skills/write-to-context.py --path "brand.json#/seasonality" --value '{"peak_periods":["Q4-holiday","Q2-mothers-day"],"trough_periods":["Q1-post-holiday"],"notes":"Niche skincare actives portée par Q1 resolutions et back-to-school Q3, dip été net"}' --source agent --confidence 0.5 --mode proposed --reason "Seasonality niche analysis"
```

Confidence default 0.5 car saisonnalité hypothèse macro depuis corpus qualitatif (validation chiffres = analyze-perf ou Google Trends pull séparé).

**`products/{slug}/spec.json#competitive_comparison[]` (v2.58 write-side P6, NEW field per produit)** · lors de l'analyse compétitive (déjà couverte par `brand.json#market.competitors[]`), enrichir feature-by-feature par produit vs top-3 competitors. Chaque entrée porte `competitor_product`, `feature`, et le delta observé. Stage par produit :

```bash
python3 .skills/write-to-context.py --path "products/{p_slug}/spec.json#/competitive_comparison" --value '[{"competitor_product":"competitor-A-hero","feature":"rapid-absorption","delta":"+50% faster claim"},{"competitor_product":"competitor-B-hero","feature":"price-tier","delta":"-30% cheaper"},{"competitor_product":"competitor-C-hero","feature":"texture","delta":"more occlusive"}]' --source agent --confidence 0.6 --mode proposed --reason "Feature-by-feature vs competitors mine-vom output"
```

Run par produit, cap 5 features par competitor pour rester actionnable copy-side. Skip si le produit n'a pas de competitor mappable (brand monopoliste niche, ou competitors hors scope hero).

**`audiences/{slug}/profile.json#voice.market_vernacular[]`** · append vernacular tokens as proposed entries with `origin: "vom"` and verbatim references. Each token carries one example sentence and the source tag.

**`audiences/{slug}/profile.json#objections[]`** · append market-level objections that the brand-bound `mine-voc` missed. An objection that the brand's own customers do not voice but the broader market debates relentlessly is the highest-value cross-skill find.

**`learnings.json`** · append patterns that generalize beyond this brand. *"In {niche}, social proof type X carries weight, type Y does not."* Per `learnings.json` doctrine, append-only.

Layer A corpus archived in `brands/{slug}/sources/vom/{run_id}/{source-category}.jsonl`. Never auto-loaded per parent CLAUDE.md `sources/` rule. Operator can grep when needed.

## Step 9 · Finalize (mandatory)

Before any operator-facing close ships, run the finalizer:

```bash
python3 .skills/finalize-mutation-batch.py --brand-slug {slug}
```

Mechanical Python primitive. No LLM negotiation, no skip path. Exit code 0 = ship. Exit code 2 = blocking issue, MUST revise before close. The finalizer enforces the mutation gate, validates batch coherence, and emits the `coherence_check` event downstream. Per the v2.7.1 stress-test learning that retired the soft-prescribed `validate-output-coherence` LLM call, this is the replacement and it is non-optional.

After exit 0, trigger `validate-resources` on the brand silently per the parent CLAUDE.md mutation rule. Surface MAJOR or CRITICAL findings to the operator before the synthesis close.

After validate-resources, rebuild the brand snapshot:

```bash
python3 .skills/build-brand-snapshot.py {slug}
```

Silent. Approximately 50ms. Keeps the digest fresh for the next session.

## --focus parameter modes

The skill supports five execution modes via `--focus`. Layer A corpus is always full ; only the synthesis paragraph shape changes.

**default** · full three-movement synthesis. Movement 1 market shift, Movement 2 vernacular, Movement 3 white spaces or Porter. Used when the operator wants the full read.

**`--focus=vernacular`** · synthesis surfaces vernacular extraction only. Movement 1 names the niche's current vocabulary baseline, Movement 2 names the tokens that have aged out and the tokens emerging, Movement 3 names the one or two highest-leverage tokens the operator should adopt this week. Used when the operator is mid-creative-batch and needs vocabulary fast.

**`--focus=white-space`** · synthesis surfaces white-space opportunities only. Three white spaces named concretely with the recurrence evidence, the competitor coverage check, and the H1-readiness test for each. Used when the operator is exploring positioning shifts.

**`--focus=competitor-positioning`** · synthesis surfaces top-player positioning shifts only. One paragraph per top-three competitor naming the move they made in the last 12-18 months, the rationale visible from review and listicle signal, and the implication for the operator. Used when the operator is benchmarking a specific competitor.

**`--focus=sophistication`** · synthesis surfaces niche-stage evolution only. Where the niche sits, where it was 18 months ago, where it is moving, and the altitude implication for the operator's claim shape. Used when the operator suspects a sophistication transit and wants to confirm.

The focus parameter does not change the four-lens coding pass · all lenses are still applied to the corpus. It changes only what the synthesis paragraph surfaces. Layer B mutations are routed normally regardless of focus.

## Hard Rules

**Step 0 first-party ask non-negotiable.** Never crawl public sources before asking the operator what they already have. Wasted budget when the operator holds curated material.

**Pre-step competitor integrity check non-negotiable when `market.competitors[]` thin.** Mining the wrong competitors poisons every later lens. Stage the proposal, never auto-write competitors without operator confirmation.

**Triangulation mandatory.** Every claim in the synthesis grounded in three independent sources of different types. Single-source claims are flagged as hypotheses or dropped.

**Source provenance always tagged.** No verbatim ships into Layer A without URL, capture timestamp, source-type tag, platform tag, and recency tag. Provenance is the audit trail.

**Synthesis follows snapshot Step 7 canon strictly.** Three movements, blank line between, no titles, no bold-section anchors, end with one binary question. Read `.skills/skills/snapshot-brand/SKILL.md § Step 7` before shipping if uncertain.

**Cap `external_intelligence[]` at five to seven new entries per run.** Per `watch-competitors` precedent. More than seven and operator attention disperses.

**Forum verbatim citation rule.** Anonymize username in Layer A, retain thread URL. Operator never sees usernames. Privacy posture is firm.

**Schema field semantics stay internal.** Operator never hears `source_type`, `confidence`, `sophistication_signal`, `awareness_stage`, `porter_force`, `mode`, `_proposed`. Operator-facing language is plain.

**`finalize-mutation-batch` mandatory at end.** No skip path. Exit 0 to ship. Exit 2 to revise.

**Cap per session 100 verbatims per source, 500 total.** Larger requires explicit `--depth=deep`. Past 500 entries the synthesis dilutes.

**Cache TTL 7 days on competitor reviews and listicles.** Forums refreshed if recency-sensitive. `--fresh` flag forces full re-pull.

**Contrarian queries mandatory.** At least 10 percent of corpus from contrarian queries (`"why {category} doesn't work"`, `"{category} alternatives"`, `"{category} scam"`). A filter-bubbled corpus is an invalid run.

**Recency filter 540 days default.** Loosen for slow-moving categories (cookware, hardware tools). Tighten for fast niches (skincare actives, supplements) where a 60-day-old thread can already be stale.

**Porter selectivity.** Never run Porter as a five-section template. One or two active forces or skip the framework entirely. If no force activates, drop Porter from the run.

**Vernacular source rule.** Reject any token that surfaces only on brand-controlled surfaces (competitor packaging, brand SEO titles, paid ads). Circular evidence, low leverage, often wrong.

**Stage 5 default skepticism.** When in doubt between sophistication 4 and 5, write 4. Stage 5 is overclaimed.

**Synthesis-as-roll-call ban.** If the operator-facing close leads with "Block 1 · Competitor X / Block 2 · Competitor Y", the run is invalid even if all mutations write cleanly. Rewrite.

## Cross-references

- **`resources/frameworks/vom-mining.md`** · analytical canon, mandatory read at first invocation. Defines the four lenses, their tests, and the coding rules.
- **`.skills/skills/snapshot-brand/SKILL.md`** · voice canon for synthesis (Step 7). Three-movement format, no titles, blank lines, binary close.
- **`.skills/skills/mine-voc/SKILL.md`** · sister skill, brand-bound. Captures the operator's own customers' voice. Run first when sequencing · `mine-voc → mine-vom` · so brand-customer vocabulary is the diff anchor for market vocabulary.
- **`.skills/skills/watch-competitors/SKILL.md`** · sibling, recurring monitoring of competitors' paid Meta creatives. NOT mine-vom's job. Routing is firm: continuous paid creative → watch-competitors, one-shot qualitative organic discourse → mine-vom.
- **`.skills/skills/mine-audience/SKILL.md`** · product-level audience discovery from website scraping. NOT mine-vom's job. Routing is firm: product-bound audience candidates → mine-audience, brand-level market context → mine-vom.
- **`.skills/skills/ingest-resource/SKILL.md`** · first-party data path. Routes operator-pasted reports, conference notes, terrain observations through the digest gate before mine-vom resumes.
- **`.skills/finalize-mutation-batch.py`** · Step 9 mechanical primitive. Mandatory before any synthesis close ships.
- **`.skills/write-to-context.py`** · canonical mutation channel. Every Layer B write goes through this gate in `mode=proposed`.
- **`.skills/stage-proposal.py`** · proposal staging primitive used in Step 1 competitor integrity check.
- **`docs/system/contextual-intelligence.md`** · master doctrine. Read before designing any extension. The form-fill failure mode (filling `market.*` fields instead of producing synthesis) is the anti-pattern this skill polices in itself.
- **`docs/system/voice.md`** · voice canon. Read before editing operator-facing strings.
