---
name: pregnancy-week-companion
description: "Generate a weekly pregnancy update markdown file for a personal Obsidian vault. Use this skill whenever the user asks for 'this week's update', 'week X update', 'pregnancy update for week N', or any variation referring to weekly pregnancy info, fetal development, or guidance for an expecting couple. Trigger this even if the user just says 'let's do this week' in the context of a pregnancy. Produces a single markdown file with six sections — baby development, mum's body, partner support, what to say to her, to-dos, red flags — each with brief highlights and a collapsible detailed breakdown. Three audience modes are supported: combined (default, partner-facing, shared document), partner (rebalanced for the partner reading alone), and pregnant (second-person, addressed to the pregnant person) — pick one per generation from the user's wording or by asking. Synthesises NHS, Mayo Clinic, Cleveland Clinic, ACOG/RCOG, peer-reviewed maternal physiology research, Evidence Based Birth, and the couple's own curated research briefs on diet, exercise, and evidence-based birth interventions — explaining not just what is happening but why, with recurring emphasis on fetal brain and neurological development (neurogenesis, neuronal migration, synaptogenesis, myelination). Presents options, not prescriptions."
---

# Pregnancy Week Companion

Generate one week's pregnancy update at a time as a markdown file ready to drop into an Obsidian vault. The skill captures the format, tone, and section structure agreed with the user so each week feels consistent.

## When to use

Trigger this skill when the user asks for an update for a specific pregnancy week, or asks for "this week's" update in a pregnancy context. If the week number isn't specified, ask before generating.

Do NOT use this skill for:
- General pregnancy questions that aren't structured weekly updates ("is X safe in pregnancy?")
- Generating many weeks at once — this skill is intentionally one-week-at-a-time so the user reads things when they're timely

## Audience mode

The skill produces one of three modes per run. **Pick the mode before drafting** — it changes voice, depth allocation, filename, and (for `pregnant`) the section structure.

- **`combined`** (default) — partner-facing voice, six sections per `references/template.md`. Filename: `Week-XX.md`.
- **`partner`** — six sections, but `Mum's body` is compressed and `For your partner` / `What to say to her` get the deepest treatment. Filename: `Week-XX-partner.md`.
- **`pregnant`** — second-person, addressed to the pregnant person. Sections are restructured (`Your body this week`, `What you might be feeling`, `How your partner can help this week`). Filename: `Week-XX-pregnant.md`.

**How to pick:**

- Infer from wording: "update for me" → `pregnant`; "for my partner" / "for the partner" → `partner`; "for both of us" / "combined" → `combined`.
- If the user says "all three", produce three files in sequence.
- If ambiguous, ask once at the start: "Should I generate this for you, your partner, or a combined version?"

See `references/audience-modes.md` for the full spec on what differs between modes.

## Output

A single markdown file. Filename depends on the audience mode:

- `combined`: `Week-XX.md` (zero-padded, e.g. `Week-08.md`)
- `partner`: `Week-XX-partner.md`
- `pregnant`: `Week-XX-pregnant.md`

**Where to write the file depends on the environment.** Before applying the per-environment defaults below, check whether the user has documented a preferred output path in their CLAUDE.md or elsewhere in the loaded context — if so, use it and don't ask.

- **In Claude Code CLI** (running on the user's machine): write to the current working directory by default. The simplest workflow is to launch Claude Code from inside the Obsidian `Weekly/` folder so the file lands where wikilinks resolve. If the cwd doesn't look like a Pregnancy / Weekly folder, ask once at the start: "Where should I write the weekly file? (default: current dir)" and remember the answer for the rest of the session. Do not silently write to a path the user hasn't seen — the file is the deliverable.
- **In Cowork** (desktop app, folder access granted): write the file directly into the granted workspace folder. The user will typically have granted access to either a `Weekly/` folder or its parent — write into `Weekly/` if visible, otherwise into the granted folder root. No `present_files` call is needed in Cowork; the file appearing in the folder is the deliverable. Confirm the path in your closing message.
- **In claude.ai chat** (web/mobile, sandboxed): write to `/mnt/user-data/outputs/Week-XX[-mode].md` and present via `present_files`. The user is responsible for relocating the file to wherever their pregnancy notes live (typically an Obsidian vault's `Weekly/` folder). If they haven't told you their destination, ask once. When presenting, surface the destination path in your closing message so they know where to drop it for the wikilinks to resolve.

**Detecting environment:**
1. If `/mnt/user-data/outputs/` exists and is writeable → claude.ai chat.
2. Else if a workspace folder named `Pregnancy` or `Weekly` is visible in the granted access → Cowork.
3. Otherwise → Claude Code CLI (write to cwd).

When in doubt, ask the user once at the start of the run.

**Either way:** the wikilinks in the file footer (`[[Week-XX]]` etc.) assume sibling files live in the same folder, so the file must end up in `Weekly/` for navigation to work.

## Section structure (mandatory — keep in this order)

Every weekly file MUST contain these six sections in this order, each with a brief highlights view followed by a collapsible Obsidian callout for detail:

1. **Baby this week** — fetal development
2. **Mum's body** — symptoms and physical changes
3. **For your partner** — practical support actions
4. **What to say to her** — partner mental health support, with suggested phrases
5. **This week's to-dos** — appointments, decisions, lifestyle reminders (use `- [ ]` checkboxes)
6. **Red flags — call your doctor** — specific to this week, one short paragraph

Plus header (size comparison, trimester, weeks to go) and footer (wikilinks to previous/next week).

## Format details

- **Filename:** `Week-XX.md` with zero-padded week number
- **Header line:** `**Size:** [Fruit/object] (~X cm [crown-to-rump if ≤~19w, head-to-toe if ≥~20w]) · **Trimester:** [First/Second/Third] · **Weeks to go:** ~XX` — always label which length measurement it is; the convention switches at ~20w (see `references/template.md` Header field rules)
- **Brief view per section:** 3–5 bullet points OR a 2–3 sentence paragraph (use whichever is in the template for that section — see references/template.md)
- **Detailed view:** Inside `> [!info]- Detailed breakdown` callout (the trailing `-` makes it collapsed by default in Obsidian)
- **Wikilinks at footer:** `*Previous: [[Week-XX]] · Next: [[Week-XX]]*` (omit "Previous" for week 4, omit "Next" for week 40)

For the exact template structure with section ordering, see `references/template.md`.

## Tone and voice

The voice is established and consistent. See `references/tone-guide.md` for full guidance, but key principles:

- Warm but not saccharine. Talks to the couple like a knowledgeable friend, not a medical pamphlet
- Direct about hard things (miscarriage anxiety, antenatal depression, partner mental health)
- Practical — every "for your partner" item should be something they can actually do today
- British/international phrasing acceptable (uses "mum" not "mom", metric units primary)
- Avoids: gendered assumptions beyond "her/she" for the pregnant person and "he/him" for the partner (this is the user's preference — adjust if user signals otherwise), toxic positivity, comparison ("at least it's not as bad as...")

## "What to say to her" section — special guidance

This section was added specifically by the user and matters to them. See `references/mental-health/mental-health-section.md` for the format. Key requirements:

- 4–5 suggested phrases the partner can borrow, in quotes
- Brief framing sentence above the phrases describing what she's likely feeling that week
- Detailed breakdown includes: why this week is emotionally specific, what tends to land well, what to avoid, mental health warning signs to watch for, and a brief reminder that the partner's mental health matters too

## "For your partner" section — the reading list

The detailed breakdown of *For your partner* often mentions "the partner reading list" — a curated set of topics the partner reads through over the course of the pregnancy. **The list is canonically defined in `references/partner-reading-list.md`.** Don't refer to it abstractly without grounding it; either:

- Name 1–3 specific items from the list when introducing or pointing toward something this week ("intervention cascade and cord clamping are good first reads"), or
- Reference it generically *only after* the list has been introduced in a prior week ("keep momentum on the reading list" assumes the user has already seen specific items).

The reading list is the spine for partner-prep content the same way `nutrition.md` is the spine for nutrition. Pull from it; don't invent ad-hoc topics.

## Source layers

The weekly file synthesises multiple evidence-based sources. No single source is the spine — the goal is breadth, accuracy, and giving the couple options rather than instructions.

Each domain bundle (`references/diet/`, `references/exercise/`, `references/birth/`) has its own `provenance.md` that documents the methodology, sources consulted, verification rounds, and draft chain that produced the evidence brief in that folder. You don't need to read provenance during normal generation — they exist for transparency and for anyone auditing the underlying research. Every weekly file's footer points to the public repo where these provenance files live (see `references/template.md`).

### Primary: medical sources

`references/medical-sources.md` is the central reference. Read it before drafting any week. It covers:

- **Fetal development** — NHS, Mayo Clinic, Cleveland Clinic, StatPearls (peer-reviewed embryology)
- **Maternal physiology** — peer-reviewed papers explaining the *why* behind symptoms (Soma-Pillay 2016, Jee & Sawal 2024, Chiang 2025). The user explicitly wants the science, not folk wisdom.
- **Birth and intervention decisions** — Evidence Based Birth, Cochrane reviews, ACOG, RCOG, NICE
- **Perinatal mental health** — NHS, Maternal Mental Health Alliance
- **South African / local context** — Soma-Pillay paper is locally authored; SA Maternity Care Guidelines for public-system context

The medical-sources file also has a **decision tree** at the bottom: for each kind of claim (size, milestone, symptom mechanism, decision, mental health, red flag), it tells you which sources to anchor to. Use it.

### Secondary: Vittorio protocol

`references/vittorio-protocol.md` is **one perspective among several**, not the document's spine. It came from a specific book the user read; its timing anchors and pragmatic suggestions are useful, but its prescriptive voice and contested choices (declining standard newborn interventions, etc.) are not the default frame.

Treat Vittorio as you would a knowledgeable but opinionated friend's input:

- **Useful for**: pragmatic week-anchored timings (e.g., "perineal massage tends to start around 34 weeks"), partner-action ideas (e.g., the morning protein-and-fat tray for nausea — this has reasonable physiological grounding around blood sugar and hCG), and the *menu* of decisions a couple faces.
- **Not useful as**: the only source, the source of truth on contested choices, or a prescriptive checklist.
- **When Vittorio and Tier 1 sources conflict**, Tier 1 wins, and the weekly file presents the mainstream evidence. The user-curated research briefs (`diet.md`, `exercise.md`, `interventions-vaginal-birth.md` and their practical/ELI5 companions) also outrank Vittorio — e.g. on raspberry leaf tea or dates, use the interventions review's evidence grading, not Vittorio's stance.
- **For contested choices** (Hep B at birth, vitamin K route, eye ointment, induction timing, cord clamping), present them as decisions to discuss with the care provider, with the evidence on both sides briefly noted. Never frame Vittorio's stance as the recommended one.

### Tone across all sources

- **Translate, don't transplant.** Source material — whether a Cochrane review, an ACOG guideline, or Vittorio — comes in clinical or declarative voice. The weekly file's voice is warm-friend (see `tone-guide.md`).
- **Present options, not prescriptions.** "Here's what tends to happen and what couples often do" — not "do this".
- **Don't moralise.** Mention lifestyle restrictions/choices once, factually.
- **Mechanism in detail, not in brief.** The brief view stays surface-level; the detailed breakdown is where the physiological "why" lives. This protects the page from feeling like a textbook while still respecting the user's preference for science-based content.

### Recurring focus: nutrition

`references/diet/nutrition.md` is the spine for any nutrition content in a weekly file — what to eat, vitamins, minerals, supplements, what to avoid, and the postpartum impact of inadequate diet. It covers the core nutrients with mechanisms (folate, choline, iron, iodine, vitamin D, DHA, calcium, magnesium, B12, zinc, protein, fibre), the evidence-supported supplement spine, what to avoid (with reasons, mentioned factually once not moralised), the first-trimester nausea protocol, trimester-by-trimester nutrient priorities, and a postpartum / 4th-trimester preview including what under-eating or poor diet actually costs.

**Important: there is no standalone "nutrition" section in the template.** Nutrition surfaces *through* the existing six sections when something is week-relevant:

- `Baby this week` detailed breakdown — when a specific nutrient ties to what's developing (folate at 4–6w neural tube, choline through neurogenesis weeks 8–20+, iodine ~14–16w fetal thyroid, DHA through brain growth phases, iron building fetal stores in the third trimester)
- `Mum's body` detailed breakdown — when a symptom has a food/nutrient lever (nausea, constipation, leg cramps, heartburn, fatigue, restless legs)
- `For your partner` — practical food prep (morning tray in first trimester, freezer-stocking in late third, snack stations)
- `This week's to-dos` — supplement check at booking, ferritin retest, GTT, dates from ~36w
- `Red flags` — when an eating-related sign warrants medical attention (hyperemesis especially)

The nutrition file has a "How nutrition surfaces in each section" map at the bottom — use it to keep nutrition content well-placed and proportionate, not crowding the page.

**Companion diet references (user-curated research):** `references/diet/diet.md` is the full evidence brief (ACOG/WHO/NHS/NIH guidelines, nutrient RDA tables with deficiency risks, caloric needs by trimester, food-safety lists with the *reason* for each restriction, caffeine dose-response data, prenatal supplement label guidance including the choline/iodine/DHA gaps, Mediterranean diet evidence). `references/diet/diet-practical-guide.md` is its plain-English action version with trimester-by-trimester action steps, the nausea protocol, heartburn strategies, vegetarian/vegan fixes, and the reassuring "don't worry" framings. Use these alongside `nutrition.md`: nutrition.md remains the spine for *where* nutrition surfaces in the six sections; the diet pair is the cross-check for specific numbers (calorie additions, RDAs, caffeine limits) and the source of practical framings ("you're eating for 1.15, not two"). When the documents differ on a specific dose, prefer diet.md's guideline-sourced figures and keep mechanisms from nutrition.md.

### Recurring focus: exercise

`references/exercise/exercise.md` (full evidence brief) and `references/exercise/exercise-practical-guide.md` (plain-English version with a trimester-by-trimester and week-by-week guide) are the spine for any movement content in a weekly file. They are user-curated research synthesising ACOG 804, WHO 2020, the Canadian CSEP guideline, and multiple meta-analyses. Key facts to keep consistent across weeks: the 150 min/week moderate-activity target and "talk test"; benefits (GDM risk down ~a third, cesarean odds down ~30%, meaningful antenatal/postnatal depression reduction — walking especially); the safety reassurance (no increased miscarriage/preterm/birth-weight risk in uncomplicated pregnancies); the supine-exercise cutoff at ~16–20 weeks; what to avoid (contact sports, fall-risk sports, scuba, hot yoga); the warning-signs-to-stop list; and the absolute/relative contraindications (always deferred to the care provider).

Like nutrition, **there is no standalone exercise section** — exercise surfaces through the six sections when week-relevant:

- `Mum's body` detailed breakdown — when a symptom has a movement lever (back/pelvic girdle pain, constipation, mood, sleep) or when a trimester transition changes what's comfortable or safe (supine cutoff ~16–20w, balance shift in the third trimester)
- `For your partner` — joining the walk or swim, taking over a task so she has time to move, booking the prenatal yoga or aquanatal class
- `This week's to-dos` — trimester-appropriate activity reminders, starting pelvic floor work (~12–20w), transitioning off supine exercises (~17–20w), adapting pace in the third trimester
- `Red flags` — the stop-exercising-and-call list when an exercise-related symptom appears (bleeding, fluid leak, regular painful contractions, calf pain/swelling, dizziness, chest pain)

The practical guide has week-by-week suggestions per trimester — use those to anchor exercise content to the specific week, and keep it proportionate (a bullet or two, not a programme).

### Recurring focus: birth preparation and interventions

`references/birth/interventions-vaginal-birth.md` is the spine for any birth-preparation content — a GRADE-graded evidence review of 18 physical interventions against measurable birth outcomes (perineal trauma, labour duration, mode of delivery, spontaneous onset, pelvic floor outcomes, pain/epidural use), with a tiered one-page summary at the bottom. `references/birth/interventions-vaginal-birth-eli5.md` is its plain-language companion — useful for borrowing warm-friend framings ("like stretching a new leather glove"). These are user-curated research and take precedence over Vittorio for birth-prep timing and evidence claims.

How to use the tiers:

- **Tier 1 (strongly supported)** — aerobic exercise throughout, perineal massage from 34w, warm compresses in second stage, upright positioning/mobility in labour, pelvic floor muscle training from 12–20w, gestational weight management. These can be presented confidently, with their week anchors, still as options ("many couples start...") not prescriptions.
- **Tier 2 (promising, lower-quality evidence)** — dates from ~36w, prenatal yoga, birth ball in labour, water immersion in first stage. Present as "reasonable to try, evidence is weaker"; note the caveat briefly (e.g. the best dates RCT found no benefit).
- **Tier 3/4 (insufficient evidence or possibly harmful)** — raspberry leaf tea, Spinning Babies, EPI-NO devices, evening primrose oil. Don't recommend these. If one is culturally ubiquitous for the week (raspberry leaf in late third trimester), it's fine to name it once as not evidence-supported — factually, without moralising. EPI-NO deserves an explicit caution if devices come up (possible increased severe-tear risk).

Week anchors for surfacing birth-prep content: pelvic floor training from ~12–20w (`to-dos`), perineal massage starting ~34w (`to-dos` + `For your partner` — the protocol details live in the full review), dates from ~36w (`to-dos`, with the GDM caution), labour positioning/warm compresses/water immersion in the birth-plan weeks (~32–36w, as things to discuss with the midwife and put in the birth plan). The integrated tear-prevention strategy section is the best single anchor for a late-third-trimester birth-prep summary.

### Recurring focus: first-trimester overview (weeks 0 → 13+6)

`references/first-trimester/first-trimester.md` is the full evidence brief covering the first trimester as a trimester-level integrator — pregnancy dating (LMP convention, CRL-based dating scan at 7+0–13+6w as the EDD anchor for every later decision), embryonic and early-fetal milestones (implantation week 4, heart activity ~6w, neural tube closure ~6w, embryo → fetus at 8w, organogenesis essentially weeks 3–8), the booking-visit screening package (booking bloods including HIV/syphilis/HBV/rubella/HCV, MSU, mental health screen), genetic-screening options per ACOG/SMFM Consult Series #74 (Nov 2025, endorsed by ACOG Jan 2026) including cfDNA (NIPT) from ~10w with ~99% T21 sensitivity, combined first-trimester NT + biochemistry at 11+0–13+6, and diagnostic CVS / amniocentesis; T1 maternal physiology beyond NVP (fatigue, breast tenderness, urinary frequency, cardiac output already up ~10–15% by end-T1, food aversions, constipation, mood lability); miscarriage epidemiology and the reassurance gradient by GA (~10% at 6w → <1% at 12w after heartbeat detected); ectopic-pregnancy triage; lifestyle decisions with their evidence base (folic acid USPSTF 2023 Grade A, alcohol CDC/ACOG no-safe-amount, caffeine ≤200 mg/day with Chen 2023 dose-response anchor, paracetamol Ahlqvist 2024 *JAMA* sibling-control deflating the ADHD/autism panic, hot tubs/saunas, medication review including teratogen list); mental health in T1 (often the highest-prevalence trimester for antenatal depression, e.g. Shenzhen 110,584-woman cohort T1 ~10.9%); and the T1-specific red flags (heavy bleeding, unilateral pelvic pain → ectopic, severe persistent vomiting + weight loss → HG, fever). `references/first-trimester/first-trimester-eli5.md` is its plain-language companion — useful for borrowing warm-friend framings ("symptoms are a noisy signal, not a thermometer"; "the reassurance gradient"; "the four genuinely consequential T1 levers"; "one-sided pelvic pain in T1 is the emergency you should know about"). These are user-curated research and take precedence over Vittorio for first-trimester timing and evidence claims.

This brief is the spine for weeks 0–13+6 the same way the diet, exercise, birth, and mental-health folders are spines for their domains, and it integrates the existing T1-specific deep-dives (`nausea-pregnancy-first-trimester.md` for the GDF15/GFRAL mechanism, `zofran.md` for ondansetron pharmacology and safety-in-pregnancy framing, `Acrylamide.md` for dietary acrylamide). **There is no standalone first-trimester section in the template** — its content surfaces through the six sections when week-relevant:

- `Baby this week` detailed breakdown — anchor embryonic/fetal milestones to the per-week table (week-4 implantation; week-5–6 gastrulation and heart tube; week-6 cardiac activity + neural tube closure; week-8 end-of-embryonic-period; week-10 organogenesis essentially complete; week-12 intestines back in abdomen; week-13 CRL ~70 mm). Mention the LMP-vs-conception offset gently — "week 6 means roughly 4 weeks since conception" — without making it the centrepiece.
- `Mum's body` detailed breakdown — nausea (with GDF15/GFRAL one-liner from the deep-dive when week-relevant, e.g. "the placental hormone GDF15 binding brainstem GFRAL drives most NVP"), profound fatigue, breast tenderness, urinary frequency, food aversions and metallic taste, constipation, mild cramping/round-ligament-pulling, mood lability. Reinforce: symptom variability is normal; absence of nausea is not a warning sign.
- `For your partner` — practical NVP management (small frequent meals, ginger, pyridoxine + doxylamine as first-line, escalate early rather than late); take over household work where energy allows; emotional patience for mood lability; remember it usually resolves by ~14–16w; *don't* keep saying "it's only X more weeks" (it makes things worse, not better).
- `This week's to-dos` — folic acid (continue from preconception, or start *today* if not already); booking visit attendance; booking bloods; dating scan window 7+0–13+6w with strongest accuracy here; NIPT from ~10w if choosing cfDNA; combined first-trimester screen at 11+0–13+6w if choosing NT-based; carrier screening offer; aspirin start before 16w if any preeclampsia risk factor; medication review against teratogen lists; flu vaccine if in season.
- `Red flags` — T1 has a *different* red-flag profile than T2/T3. Same-day assessment for: heavy vaginal bleeding with clots/cramping → possible miscarriage; **unilateral severe pelvic pain ± shoulder-tip pain → ectopic until proven otherwise**; severe persistent vomiting + inability to keep fluids + weight loss → HG; fever ≥38°C/100.4°F with no obvious cause. Things that do NOT in themselves require urgent review: light spotting without pain (~25% of women), variable nausea day-to-day, mild cramping, profound fatigue.

**How this brief relates to the others:** as with the T2 and T3 briefs, it overlaps with the diet, exercise, birth, and mental-health spines on purpose — it's the *trimester-level integrator* for weeks 0–13+6. When the briefs differ on a specific number, defer to the domain spine (e.g. `references/diet/diet.md` for food-safety detail, `references/exercise/exercise.md` for the 150 min/week target, `references/mental-health/perinatal-emotional-journey.md` for antenatal depression prevalence and treatment options). When the T1 brief adds something the domain spines don't cover (the LMP-vs-conception dating offset, the embryonic-period organogenesis window, NIPT/cfDNA per SMFM Consult #74, miscarriage epidemiology + reassurance gradient, ectopic triage, the Ahlqvist 2024 paracetamol-deflation paper, the Chen 2023 caffeine dose-response data, the T1-specific red-flag triage thresholds), it's the source of truth. For NVP / HG mechanism and Zofran specifics, defer to `nausea-pregnancy-first-trimester.md` and `zofran.md`.

Key trimester-level framings to use consistently across weeks 0–13+6 (anchored, no inline citations):

- **Pregnancy weeks are counted from LMP, not conception** (~2 weeks offset in a 28-day cycle). The dating scan (CRL at 7+0–13+6w) is the most accurate way to set EDD; once set it's rarely revised.
- **Organogenesis = weeks 3–8** post-LMP. Most teratogen-sensitive window — often before the woman knows she's pregnant. Public-health argument for *preconception* folic acid.
- **Heart activity detectable on TVUS ~5.5–6.0w**, always by ~6.5w if pregnancy viable. Neural tube closes ~day 26–28 post-conception (~6w post-LMP).
- **NIPT/cfDNA as the dominant screening tool** per ACOG / SMFM Consult Series #74 (Nov 2025, endorsed by ACOG Jan 2026). Sensitivity ~99% for T21, FPR ~0.1%. From ~10w. **Screening, not diagnostic** — positive cfDNA needs CVS or amnio to confirm.
- **Combined first-trimester screen (NT + free β-hCG + PAPP-A)** at 11+0–13+6w. T21 detection ~85–90%, FPR ~5%. NT measurement still useful even when cfDNA is the primary screen (structural/cardiac signal at NT ≥3.5 mm).
- **Diagnostic testing offered to all** who want it: CVS 10–13w, amnio ≥15w; procedure-related loss ~0.1–0.3% in modern hands.
- **Miscarriage ~10–20% of clinically recognised pregnancies**; ~50% have fetal chromosomal abnormalities. Reassurance gradient after FH detected: ~10% at 6w → ~5% at 7w → ~3% at 8w → ~2% at 9w → ~1% at 10w → <1% at 12w.
- **Ectopic ~1–2% of pregnancies.** Unilateral pelvic pain in T1 → same-day USS + serum hCG. Don't defer.
- **Folic acid 400–800 µg/day** preconception → through first 2–3 months of pregnancy (USPSTF 2023 Grade A). Higher doses for prior NTD, antiepileptics, diabetes.
- **Alcohol:** CDC/ACOG no-safe-amount/no-safe-time/no-safe-type. Position is precautionary — low-dose evidence is noisy and confounded, not a strong positive signal. Counsel cessation, not catastrophising about pre-knowledge exposure.
- **Caffeine ≤200 mg/day** is the universal guideline. Chen 2023 dose-response: RR 1.02 (50–149 mg, NS), 1.16 (150–349 mg, NS), 1.40 (350–699 mg, sig), 1.72 (≥700 mg, sig). 200 mg cutoff is conservative.
- **Paracetamol/acetaminophen remains the first-line analgesic** in pregnancy at lowest effective dose, shortest duration. Ahlqvist 2024 *JAMA* sibling-control analysis (~2.5M Swedish children) found no association with ADHD/autism/intellectual disability after controlling for shared family factors — this is the strongest recent evidence and should be the default framing.
- **NSAIDs avoided ≥20w** (FDA 2020 safety communication); generally avoided throughout pregnancy by most guidelines.
- **Hot tubs/saunas:** avoid sustained core temperature >38.9°C / 102°F especially in organogenesis window.
- **NICE NG126 (Aug 2023 update)** now recommends **mifepristone + misoprostol** for medical management of missed miscarriage (MifeMiso trial), replacing misoprostol-alone protocols.
- **PRISM 2019 (NEJM)** supports vaginal progesterone in women with **prior miscarriage + current first-trimester bleeding** — not a universal recommendation, subgroup-specific.
- **Antenatal depression often peaks in T1** (e.g. Shenzhen 110,584-woman cohort: ~10.9% T1 vs ~6.2–6.3% T2/T3). EPDS + GAD-7 at booking is the modern standard. Untreated antenatal depression itself harms outcomes.

### Recurring focus: second-trimester overview (weeks 13–27)

`references/second-trimester/second-trimester.md` is the full evidence brief covering the second trimester as a whole — maternal physiology (aortocaval/supine, GERD trajectory, round-ligament-pain debate, leg cramps, quickening), fetal milestones week-by-week, the 18–22w anatomy scan (Cochrane 2024 detection rates by organ system, ISUOG standards), GDM screening at 24–28w (USPSTF, ACOG 2024, ADIPS 2025, 1-step vs 2-step), low-dose aspirin for preeclampsia (window, risk factors), cervical-length screening and vaginal progesterone (17-OHPC withdrawal noted), vaccines (Tdap 27–36w, RSV 32–36w in season, flu), sex/travel/daily life, and a symptoms-and-red-flags quick reference. `references/second-trimester/second-trimester-eli5.md` is its plain-language companion — useful for borrowing warm-friend framings ("screening window, not coasting window"; the AFFIRM kick-count caveat; the 17-OHPC withdrawal note; the quickening-by-placenta-and-BMI nuance). These are user-curated research and take precedence over Vittorio for second-trimester timing and evidence claims.

This brief is the spine for weeks 13–27 the same way the diet, exercise, birth, and mental-health folders are spines for their domains. **There is no standalone second-trimester section in the template** — its content surfaces through the six sections when week-relevant:

- `Baby this week` detailed breakdown — anchor fetal milestones to the per-week table (e.g. bones hardening 13–14w; sex visible 15–17w; surfactant production 22–24w; functional hearing onset 24–25w with vibroacoustic-evoked startle; periviability threshold ~22–24w with steeply rising survival-without-major-morbidity by 25–27w).
- `Mum's body` detailed breakdown — GERD rising trajectory (26% T1 → 33% T2 → 56% T3); round-ligament-pain prevalence (10–30%) with the abdominal-wall-neuropathy caveat; leg cramps (magnesium modestly helpful, calcium not, quinine contraindicated); aortocaval/supine physiology from ~20w (side-sleeping habit forming ~24w as low-cost prep for the T3 stillbirth signal, *not* a T2 panic); quickening mean ~19w nullipara / ~17w multipara with anterior placenta and BMI delaying perception.
- `For your partner` — anatomy-scan attendance (~18–22w); GDM-test logistics at 24–28w (fasting/timing); aspirin-prescription follow-through for any risk-factor pregnancy; vaccine-appointment booking (Tdap, RSV); the practical implication of fetal hearing onset ("she can hear you now" — talking and singing isn't sentimental from ~24w, it's biology).
- `This week's to-dos` — anatomy-scan booking and prep (~18–22w); cervical-length ask if any preterm-birth risk; GDM screen at 24–28w; aspirin check ("if started, still taking it; if not started and you have risk factors, ask now — window closes by 16w"); vaccine planning (Tdap 27–36w early-end; RSV 32–36w in season; flu in season any trimester); mid-pregnancy mental-health rescreen.
- `Red flags` — preeclampsia triad (severe headache + visual changes + RUQ pain); regular painful contractions before 37w; vaginal bleeding; sustained absence of established fetal movement; ruptured membranes; unilateral leg swelling/pain (DVT); chest pain or sudden shortness of breath (PE).

**How this brief relates to the others:** it overlaps with the diet, exercise, birth, and mental-health spines on purpose — it's the *trimester-level integrator* that says "here's how all of these fit together in weeks 13–27 and which clinical events are happening when." When the briefs differ on a specific number, defer to the domain spine (e.g. exercise.md for the 150 min/week target detail, diet.md for the +340 kcal/day figure, interventions-vaginal-birth.md for PFMT/perineal-massage week anchors). When the second-trimester brief adds something the domain spines don't cover (anatomy-scan detection rates, GDM screening windows, aspirin window, cervical length and vaginal progesterone, T2-specific vaccine timing, supine/aortocaval physiology, quickening), it's the source of truth.

Key trimester-level framings to use consistently across weeks 13–27 (anchored, no inline citations):

- **Anatomy scan detection rates (Cochrane 2024, ~7M fetuses):** single T2 scan ~51% sensitivity; combined T1+T2 scans ~84%; false-positive rate <0.1%. A normal scan is reassuring but not a guarantee — it doesn't catch most non-structural genetic syndromes.
- **GDM screening at 24–28w (USPSTF Grade B):** universal, not risk-based. The 1-step vs 2-step debate is unresolved (LIGHT trial, NEJM 2021, found 1-step roughly doubles diagnosis without clearly improving outcomes).
- **Aspirin 81 mg/day for preeclampsia prevention** in any high-risk pregnancy, ideally started **before 16 weeks** (acceptable up to 20w); USPSTF B recommendation.
- **Vaginal progesterone for sonographic short cervix (≤25 mm at mid-trimester)** reduces preterm birth <33w by ~38%. **17-OHPC (Makena) was withdrawn from the US market in 2023** — if anyone offers it for preterm-birth prevention, that's outdated practice.
- **Quickening: mean ~19w nullipara, ~17w multipara, range 14–22w**; anterior placenta and higher BMI delay perception. Quickening is not a reliable way to date pregnancies.
- **Supine/stillbirth signal is a T3 finding (≥28w), not T2.** Side-sleeping habit forming around 24w is sensible low-cost prep, not a mid-T2 emergency.
- **Kick-counting protocols do not have strong stillbirth-prevention evidence** (AFFIRM trial, UK, ~400k pregnancies, negative). Awareness of *changes* in established movement is what matters.
- **Tdap 27–36w (early end preferred), RSV 32–36w in season (Sep–Jan in US), flu any trimester in season.** These straddle the late-T2/early-T3 boundary.

### Recurring focus: third-trimester overview (weeks 28 → birth)

`references/third-trimester/third-trimester.md` is the full evidence brief covering the third trimester as a whole — maternal physiology (peaking cardiac output ~30–34w, GERD ~56%, carpal tunnel T3-onset ~63%, insomnia, PGP, oedema differential), fetal milestones week-by-week with brain-development emphasis (synaptogenesis, gyrification, myelination onset, fetal voice/melody recognition), the supine/stillbirth signal from 28w (Cronin 2019 IPD MA, ~2x risk), movement-awareness framing (AFFIRM 2018 negative on formal kick counts; RCOG GTG 57 "sudden change" wording), late-pregnancy screening (anti-D at 28w, FBC recheck, GBS at 36–37w US / risk-factor UK, GBS3 trial flagged), vaccines (Tdap 27–36w early-end, RSV 32–36w seasonal, flu in season), the 39-vs-41w induction debate (ARRIVE / SMFM 2024 / ACOG CPU 2024 vs WHO 2022 / Cochrane 2020 / SWEPIS / INDEX), breech at term (ECV from 36–37w with ~50% success and <1% complication, Hannah Term Breech Trial vs PREMODA-era nuance, current ACOG/RCOG support for maternal choice with strict criteria), birth-prep interventions activating in T3, preeclampsia diagnostic criteria and severe features (ACOG PB 222), intrahepatic cholestasis (Ovadia 2019 ≥100 µmol/L threshold), late-pregnancy red flags, mental health in T3 (T3 anxiety/tokophobia peak, antenatal depression as the strongest predictor of PPD), birth plan content (Lothian 2022 AJOG), and sex/travel/daily life. `references/third-trimester/third-trimester-eli5.md` is its plain-language companion — useful for borrowing warm-friend framings ("the wait-and-see defaults of earlier pregnancy do not apply in T3"; sleep on your side from 28w as "the cheapest intervention in obstetrics"; the AFFIRM null result; the two genuinely-yours decisions of T3). These are user-curated research and take precedence over Vittorio for third-trimester timing and evidence claims.

Like the second-trimester pair, this brief is the spine for weeks 28–40+ the same way the diet, exercise, birth, and mental-health folders are spines for their domains. **There is no standalone third-trimester section in the template** — its content surfaces through the six sections when week-relevant:

- `Baby this week` detailed breakdown — anchor fetal milestones to the per-week table (e.g. eyes open + sleep–wake cycles by 28w; rapid fat deposition 29–30w; bone marrow takes over RBC 31–32w; "early term" 37w / "full term" 39w; voice and melody recognition by late T3). The brain-development thread is dominant in T3 — use the synaptogenesis/gyrification/myelination language consistently.
- `Mum's body` detailed breakdown — GERD ~56%, insomnia ~50%, back/PGP ~50–70%, carpal tunnel ~20–60% (T3 onset ~63%), oedema (with the differential from preeclampsia), Braxton-Hicks vs regular contractions, dyspnoea as physiological, supine going-to-sleep position as the specific Cronin signal from 28w.
- `For your partner` — sleep-position reminder; reduced-movement triage practice ("don't talk her out of calling"); birth-plan participation; postpartum-period planning starting now (who's in the house in week 1/2/6); Tdap and RSV appointment-keeping; "she can hear you" — talking and singing to the bump as part of how the baby learns the voice.
- `This week's to-dos` — anti-D at 28w if RhD-negative; FBC recheck at 28w; EPDS/GAD-7 rescreen at 28–32w; perineal massage start at 34w; presentation check + ECV conversation at 36w if breech; GBS screen 36–37w (US); birth-plan finalisation by 36–37w; hospital bag check; air-travel cut-offs; 39w-induction conversation if relevant; 41w-induction conversation if not yet delivered.
- `Red flags` — T3 has the densest red-flag list of any trimester. The bar drops to *same-day assessment*: severe persistent headache (especially with visual changes or RUQ pain) → preeclampsia; sudden face/hand oedema or rapid weight gain → preeclampsia; generalised itching of palms/soles without rash → ICP; sudden change in baby's movement pattern; any vaginal bleeding; sudden gush or persistent leak of fluid (ROM); regular painful contractions <37w; unilateral leg pain/swelling → DVT; sudden SOB with chest pain → PE.

**How this brief relates to the others:** as with the second-trimester brief, it overlaps with the diet, exercise, birth, and mental-health spines on purpose — it's the *trimester-level integrator* for weeks 28→birth. When the briefs differ on a specific number, defer to the domain spine (e.g. exercise.md for the 150 min/week target detail, interventions-vaginal-birth.md for perineal-massage NNTs and dates evidence, perinatal-emotional-journey.md for antenatal-depression prevalence). When the third-trimester brief adds something the domain spines don't cover (the Cronin 2019 supine signal, AFFIRM movement-awareness framing, ARRIVE-vs-WHO induction debate, ECV success/complication rates, ACOG PB 222 preeclampsia severe features, Ovadia 2019 ICP threshold, US-vs-UK GBS approaches), it's the source of truth.

Key trimester-level framings to use consistently across weeks 28–40+ (anchored, no inline citations):

- **Sleep on your side from 28w.** Cronin 2019 IPD meta-analysis (5 case-control studies, 851 cases / 2,257 controls): going-to-sleep supine ≥2·6× late-stillbirth risk. Either side. Free, easy, no downside. The signal is for *going-to-sleep* position, not waking position.
- **Movements do not slow in T3** (RCOG GTG 57). Awareness of *change* in established pattern is what matters. AFFIRM (Lancet 2018, ~409,000 pregnancies, stepped-wedge cluster RCT) showed a formal kick-count care package did **not** reduce stillbirth — induction and caesarean rates rose without outcome benefit. Don't promote rigid counting protocols; promote same-day contact for any sudden change.
- **GBS: US universal screen 36 0/7–37 6/7w (ACOG CO 797, 2020); UK risk-factor approach (RCOG GTG 36).** GBS3 cluster RCT pending.
- **Tdap 27–36w early-end, RSV (Abrysvo) 32–36w in season (Sep–Jan continental US), flu any trimester in season.** RSV vaccine is genuinely new in T3 since CDC ACIP October 2023; baby alternative is nirsevimab antibody postnatally — only one of the two is needed.
- **39w elective induction: "may offer, not should do"** (SMFM 2019/reaffirmed 2024; ACOG CPU 2024). ARRIVE (NEJM 2018) showed lower caesarean rate (18.6% vs 22.2%) and lower hypertensive-disorders rate in induction arm; not all real-world implementation studies reproduce the size of the effect.
- **41w routine induction: international standard** (WHO 2022 moderate-certainty; Cochrane CD004945 2020; SWEPIS BMJ 2019 stopped early on perinatal-death signal; INDEX/PLOS Med 2020 IPD).
- **ECV ~50% success, <1% complication** (RCOG GTG 20a, ACOG PB 221 2020). Offer from 37+0 multipara / 36+0 nullipara.
- **Term breech mode of delivery:** Hannah Term Breech Trial (Lancet 2000) established planned caesarean as default; PREMODA-era data and *State of the breech* 2020 support planned vaginal breech with strict selection criteria and experienced operator. Skill atrophy is a real systemic concern.
- **Preeclampsia severe features (ACOG PB 222 2020):** BP ≥160/110, platelets <100k, transaminases ≥2× normal with severe RUQ pain, Cr >1.1 or doubled, pulmonary oedema, new cerebral/visual symptoms. Any one → severe preeclampsia → delivery indicated.
- **Intrahepatic cholestasis: bile acids ≥100 µmol/L** is the Ovadia 2019 IPD MA threshold for clinically meaningful stillbirth risk (3.4% vs ~0.4%). Generalised itching especially palms/soles, no rash, worse at night → bile-acid test.
- **Perineal massage from 34w (Cochrane CD005123, 2,497 women):** NNT 15 for perineal trauma requiring suturing; NNT 21 for episiotomy.
- **Air travel: most airlines stop 36–37w singleton (RCOG); ACOG CO 746 occasional air travel safe up to 36w; seatbelt continuously, hydrate, walk every 1–2h, consider compression stockings.**

### Recurring focus: infant vaccinations (post-birth schedule with pregnancy-side hooks)

`references/infant-vaccinations/infant-vaccinations.md` is the full evidence brief covering the routine infant immunisation schedule (birth through ~18 months) across the US (ACIP and AAP), UK (NHS/JCVI), and WHO/EPI, the evidence basis for the timing decisions, and the active 2025 US policy fracture. `references/infant-vaccinations/south-africa.md` is the South-Africa-specific overlay covering EPI-SA (Expanded Programme on Immunisation – South Africa) as revised 2024, the HIV-exposed-uninfected (HEU) infant context (a substantial fraction of the SA birth cohort), the 2024–2026 maternal RSV vaccine landscape (SAHPRA licensure, NAGI April 2025 advisory, Wits-sponsored 13,000-woman Phase 3 trial NCT06955728), and the declining-coverage trend (MCV1 86% → 76% from 2015–2024). Although the schedule is post-birth content, it belongs in the pregnancy spine for two reasons: (a) the maternal Tdap / RSV / flu / HepB decisions made *in pregnancy* directly shape what the infant gets in the first months, and (b) families reasonably want to understand the post-birth schedule *before* delivery so they can make consent decisions calmly rather than at the hospital. `references/infant-vaccinations/infant-vaccinations-eli5.md` is its plain-language companion — useful for borrowing warm-friend framings ("the schedule is the empirical compromise between maternal-antibody interference and disease exposure"; "in the US in 2026 the schedule you actually get depends on which doctor you see"; "more vaccines now, fewer antigens now"; "the autism question has been answered, repeatedly"). These are user-curated research and take precedence over Vittorio for infant-vaccination timing and evidence claims.

**This brief is a domain spine like diet/exercise/birth/mental-health — not a trimester spine.** It activates *late in pregnancy* and at birth, surfacing through the existing six sections when week-relevant:

- `This week's to-dos` — most prominent surface. Use for: maternal Tdap at 27–36w (early-end preferred), maternal RSV (Abrysvo) at 32–36w in season (Sep–Jan continental US), flu any trimester in season, and from ~34–36w onwards the "pick a paediatrician" task includes asking which schedule they follow (AAP vs ACIP) given the December 2025 split. Hospital-side: the birth-dose HepB question is a *real* consent decision in 2026 — mention it in the late-T3 / hospital-bag-week files when generating those.
- `For your partner` — the partner is often the one taking the baby to early well-baby visits (2 mo, 4 mo, 6 mo). Pre-loading the schedule in pregnancy means they can hold the framing instead of being asked at the appointment.
- `Mum's body` — transplacental antibody transfer is the *why* behind maternal Tdap / RSV / flu. When mentioning maternal vaccines, the one-liner is: "these put antibodies across the placenta to protect the baby in their first ~3 months, before they've completed their own primary series."
- `Baby this week` — once in late T3, the framing "the baby is being equipped at birth for their first few months of immune exposure" connects maternal vaccines, breastfeeding-IgA, and the infant's own schedule.
- `Red flags` — no T3-specific red flags from this brief; the infant-vaccine red-flag content (febrile-seizure management, intussusception signs after rotavirus dose 1) is post-birth.

**How this brief relates to the others:** like the diet, exercise, birth, and mental-health spines, it's the source of truth for its domain. When the birth brief or the T3 brief mentions Tdap/RSV/flu vaccines, the *immunology rationale* (maternal-antibody transfer, infant priming-response interference, the 27–36w window logic) defers to this brief. When this brief mentions delivery-time logistics (HepB birth-dose timing at the hospital, what's offered before discharge), the *birth-experience framing* defers to the birth folder.

Key framings to use consistently when this material surfaces (anchored, no inline citations):

- **The 2025 US schedule split is real and live.** December 5, 2025: ACIP voted 8–3 to replace the universal HepB birth dose with "individual decision-making" for infants of HBV-negative mothers. AAP published its own parallel schedule that retains the universal birth dose. AAFP, ACOG, and most US hospital systems explicitly back AAP. *Which schedule a family actually gets depends on their paediatrician.* For most antigens AAP and ACIP are identical — the live divergence is the HepB birth dose.
- **HepB birth dose rationale (pre-2025 ACIP, AAP, WHO position retained):** perinatal HBV transmission has ~90% chronic-infection risk in the infant; chronic infant HBV has ~25% lifetime cirrhosis/HCC risk; birth dose within 24h reduces vertical transmission by ~85–90%; "universal" rather than "selective" because antenatal HBV screening misses some cases (late testing, missed testing, seroconversion in pregnancy).
- **"2/4/6 months" is not arbitrary.** It's the empirical compromise: maternal antibodies blunt infant response (Voysey 2017 IPMA, 7,630 infants 32 studies — inhibition seen for 20 of 21 antigens); pertussis hospitalisation peaks 2–6 months; DTaP needs 3 priming doses with ≥4-week intervals; 2 months is the earliest most infants mount a robust acellular-pertussis response. The WHO 6/10/14-week schedule trades slightly more maternal-antibody interference for earlier protection in high-burden settings.
- **MMR waits until 12 months** because live-attenuated viral vaccines are most affected by maternal antibody, and measles maternal IgG decays slowly. The 2017 Voysey IPMA and the Thai-infants MMR study (PMC 2022) both quantify this. In outbreak/travel situations MMR can be given from 6 months but the dose doesn't count toward the routine series.
- **MMRV vs MMR + varicella at 12–15 months: no preference as of September 2025 ACIP** (was previously preferred for MMRV). ~1 extra febrile seizure per 2,300–2,600 first MMRV doses vs MMR+V given separately; typically simple and self-limiting. Genuine parent/clinician choice now.
- **"Too many vaccines / antigenic overload" was tested directly.** Vaccine Safety Datalink nested case-control (Glanz 2018 *JAMA*): cumulative antigen exposure 0–23 months had no association with non-vaccine-targeted infections 24–47 months (between-group difference −2.3 [95% CI −10.1 to 5.4], p = 0.55). Modern schedule uses ~150 antigens; 1980 schedule used ~3,000+ (dominated by whole-cell pertussis). "More shots" ≠ "more antigens."
- **Vaccines and autism: null, replicated.** Taylor 2014 meta-analysis (5 cohort studies n = 1.26M; 5 case-control n = 9,920): OR 0.99 (95% CI 0.92–1.06). Jain 2015 *JAMA* (~95k including children with autistic siblings): null. Hviid 2019 *Ann Intern Med* (657k Danish children): null. Wakefield 1998 retracted (2010). Thimerosal hypothesis refuted by post-2001-removal trend data.
- **Delayed/alternative schedules: no documented benefit, documented cost.** Robison 2014 *Pediatrics*: timely vs delayed/incomplete first-year vaccination across 42 neuropsychological outcomes at age 7–10 — no advantage to delay. Cumulative time susceptible during peak-disease window is the price.
- **Rotavirus timing is strict for a real reason.** Both currently licensed rotavirus vaccines have a small association with intussusception (~1–7 excess cases per 100,000 doses; ~32% excess in 6–14 weeks post-dose-1) against ~40,000–60,000 hospitalisations prevented per US birth cohort. Strict age limits (first dose by ~15 weeks, last by ~8 months) exist because intussusception risk rises with age of first dose. Missing the window means missing the vaccine.
- **Maternal Tdap blunts infant pertussis priming** (Pediatric Infectious Disease Journal Feb 2025 review formalises this) but net effect on first-3-month pertussis protection is strongly positive (~90% effectiveness against infant pertussis hospitalisation in first 3 months in UK/US data). The blunting matters mostly for booster timing, not first-year protection.
- **UK routine schedule restructured 2025–2026** after Menitorix (Hib/MenC) discontinued: 6-in-1 at 8/12/16 weeks; MMR moved to 12 months; varicella added to UK routine for the first time as MMRV at 12 months from January 2026 birth cohort onwards.
- **WHO EPI 6/10/14 weeks** for low/middle-income countries: faster primary series because disease pressure is higher; trades slightly more maternal-antibody interference for earlier protection. BCG at birth in TB-burden settings; universal HepB birth dose remains WHO standard in 2025–2026 — the US 2025 ACIP departure is an outlier internationally.
- **South Africa (EPI-SA 2024 revision) uses 6/10/14 weeks** with hexavalent (DTaP-IPV-HepB-Hib), BCG + OPV-0 at birth, *selective* HepB birth dose (for HBsAg-positive maternal status only — not universal), Rotarix 2-dose at 6 + 14 weeks, PCV 2+1 (6w/14w/9 mo), Measles-Rubella at 6 + 12 months, and Tdap antenatally (replaced TT in 2024). HEU infants get the same schedule on the same timeline; the SA research literature (Madhi, Cutland, Jones, Klipstein-Grobusch at Wits/NICD) has quantified lower primary-series antibody responses in HEU infants for several antigens, with booster doses largely closing the gap — supporting on-time delivery as the most actionable individual-family intervention. Maternal RSV vaccine (Abrysvo) licensed by SAHPRA in 2024 but not yet routine in the public sector; Wits 13,000-woman Phase 3 trial runs Sep 2025–Feb 2028. MCV1 coverage dropped from 86% (2015) to 76% (2024) — well below the WHO 95% target. See `south-africa.md` for full SA overlay.

### Recurring focus: perinatal mental health

`references/mental-health/perinatal-emotional-journey.md` is the spine for any mental-health content in a weekly file — a research-anchored evidence review covering normal experience (matrescence, ambivalence, baby blues, intrusive thoughts), clinical conditions (perinatal depression, anxiety, OCD, PTSD, tokophobia, postpartum psychosis), the partner's trajectory, and what works (CBT/IPT, exercise, sleep protection, peer support, sertraline as default). `references/mental-health/perinatal-emotional-journey-eli5.md` is its plain-language companion — useful for borrowing warm-friend framings (e.g. "having a baby rewires the brains, bodies, and relationships of *both* parents"). `references/mental-health/mental-health-section.md` is the structural / format guide for the *What to say to her* section's detailed breakdown.

Key numbers and framings to use consistently across weeks (anchored, no inline citations):

- **Perinatal depression: ~12–18% pooled prevalence** (sometimes "1 in 6"). Antenatal depression alone ~10–15%. The strongest predictor of postnatal depression is depression *during* pregnancy.
- **Perinatal anxiety: ~15% antenatal, ~15% postnatal**, often missed by depression-focused screens.
- **Partner perinatal depression: ~8–10% pooled, peaking 3–6 months postpartum**, correlated with maternal depression. An independent predictor of child outcomes — partner mental health is a clinical population, not just support.
- **Baby blues: 50–80%, days 3–5, resolves spontaneously by ~2 weeks.** The two-week rule is the dividing line between blues and PND.
- **Postpartum psychosis: 1–2 per 1,000.** Onset typically within 2 weeks postpartum. Severe insomnia + confusion + believed delusions = emergency. Largest single risk factor: bipolar disorder.
- **Maternal brain remodeling (Hoekzema 2017):** measurable selective gray-matter changes in social-cognition regions, lasting at least 2 years, predict bonding strength. Useful for "you're not crazy, your brain is literally rewiring" reassurance — biology, not folk wisdom.
- **Partner support is the strongest modifiable protective factor** for maternal perinatal mental health (Pilkington 2015). The partner role is clinically significant.
- **The intrusive-thoughts-vs-psychosis distinction:** distressing intrusive thoughts of harm to the baby occur in the *majority* of new mothers and are *not* predictive of harm — distress about the thought is reassuring. The opposite (believed, congruent, often with insomnia and confusion) is the emergency. This is the single most important public-health message in the brief and should be clearly framed in any week that surfaces postpartum-period content.
- **"No treatment" is not the safe default.** Untreated antenatal depression has its own real risks (preterm birth, low birth weight, child outcomes, maternal suicide). Sertraline is generally first-line in pregnancy and lactation when medication is indicated. The weekly file does not advise on medication directly — it can name that this is a both-sides decision and direct to specialist perinatal mental health care.

Like nutrition and exercise, **there is no standalone mental-health section in the template** — mental health surfaces through the existing six sections when week-relevant:

- `Mum's body` detailed breakdown — when the maternal experience has a documented neurobiological or hormonal driver (matrescence brain remodeling, the hormone cliff caveat, sleep-mood interaction). Use anchored numbers, not folk language.
- `What to say to her` detailed breakdown — this is where most mental-health content lives. The *Why this matters now* opener, *What tends to land well*, *What to avoid*, *Watch for warning signs*, and *Look after yourself too* subsections all pull from the brief. See `mental-health/mental-health-section.md` for the format.
- `For your partner` — partner emotional support as the strongest modifiable protective factor (Pilkington 2015), framed practically. Partner perinatal mental health awareness in the *Mental load* and *Look after yourself too* notes.
- `This week's to-dos` — booking-appointment EPDS / GAD-7 mention, partner reading list items on mental health (see `partner-reading-list.md`), peer-support / class enrolments.
- `Red flags` — postpartum-period weeks need the postpartum psychosis red flags (severe insomnia + confusion + delusions in first 2 weeks); any week needs suicidal ideation as a red flag.

**Crisis resources** to surface where appropriate (don't bloat — name once when relevant, e.g. in the *Look after yourself too* note or in the red-flags paragraph for the relevant weeks):

- **UK:** NHS 111 (option 2 for mental health), Samaritans 116 123, PANDAS Foundation 0808 1961 776, Action on Postpartum Psychosis (app-network.org)
- **US:** 988 (Suicide & Crisis Lifeline), Postpartum Support International 1-800-944-4773, National Maternal Mental Health Hotline 1-833-852-6262
- **Always:** emergency department / 999 / 911 for imminent danger.

The user has asked for extra emphasis on brain and neurological development as a recurring theme. Every weekly file should include a dedicated **Brain / nervous system** bullet in the "What's forming" detailed breakdown of `Baby this week`, drawing on the brain-development timeline in `medical-sources.md`. Use specific, accurate language — neurulation, neurogenesis, neuronal migration, synaptogenesis, myelination — and explain what each one means in plain words. Let the awe-inspiring numbers (e.g. 250,000 neurons per minute at peak) come through where they fit, without tipping into saccharine. When senses come online (hearing ~18 weeks LMP), point partners toward the practical implication ("she can hear you now").

### Recurring focus: Expecting Better (Emily Oster)

The user keeps a chapter-by-chapter digest of Emily Oster's *Expecting Better* at:

`/Users/charles/Library/Mobile Documents/iCloud~md~obsidian/Documents/Pregnancy/Research/Feynman/Expecting Better by Emily Oster.md`

Oster is an economist; the book is a published-evidence digest of pregnancy decisions, organised by trimester. Like Evidence Based Birth, she presents the studies and the trade-offs rather than prescribing. **Her framings are part of the user's frame of reference** — when a weekly topic overlaps with one of her chapters, surface the relevant evidence and decision-shape in the weekly file. Don't transplant her snarky voice; translate her conclusions into the warm-friend register.

**How to use her:**

- **As a cross-check on contested first-trimester restrictions** — her chapters on alcohol, caffeine, fish/mercury, food safety (her "Updated Off-limits Food List" is shorter than NHS's), cat litter, hot baths, hair dye, and air travel are more permissive than NHS in places. Where she diverges from Tier 1, present the conservative line *and* note the lower-restriction evidence so the couple can decide. Don't pick a side.
- **For decision-shape on screening and testing** — her treatment of NIPT vs CVS vs amniocentesis (probability comparison, age-adjusted risk tables, the "is X more than 125× worse than a miscarriage?" framing) is genuinely good and can anchor the to-dos in weeks 10–16.
- **For labor-and-delivery trade-offs** — epidural pros/cons, doula evidence, fetal monitoring (continuous vs intermittent), eating in labor, episiotomy, induction timing, low-fluid readings, the "Oster Birth Plan" bullet points. These map cleanly into the birth-plan weeks (~32–36).
- **For day-of-birth choices** — delayed cord clamping, vitamin K route, eye antibiotics, home birth. Use alongside `partner-reading-list.md` and the interventions review.

**Tier ordering when sources conflict:**

1. Tier 1 medical bodies (NHS, ACOG, RCOG, NICE) — clinical standard-of-care wins.
2. User-curated research briefs (`diet.md`, `exercise.md`, `interventions-vaginal-birth.md`) — these are GRADE-graded reviews and win over single-author book digests.
3. Oster — single-author evidence digest. When she's permissive against a Tier 1 restriction, present both. When she's restrictive on the same line as Tier 1, that's just reinforcement.
4. Vittorio — one perspective among several (see above).

**Chapter-to-week map (rough):**

- **Weeks 4–6** (conception / very early): ovulation timing, early pregnancy testing, early miscarriage statistics (~22% before pregnancy would have been detected on the older tech)
- **Weeks 6–13** (first trimester): alcohol/caffeine evidence, food safety (Oster's updated list), fish/mercury/omega-3 IQ trade-off, the nausea ladder (small meals → B6 + ginger → B6 + Unisom/Diclegis → Zofran), genetic screening decision tree (NIPT, NT scan, CVS, amnio), cat litter, hot baths, sex, flying, hair dye
- **Weeks 14–27** (second trimester): weight-gain framing ("a small baby is worse than a large one, on average"), finding out sex on the anatomy scan, exercise + Kegels evidence, sleep-position evidence (back-sleep restrictions overblown in most studies), FDA drug categories A/B/C/D/X and how to think about them
- **Weeks 28–36** (third trimester): prematurity survival statistics by gestational age, bed-rest evidence (against), due-date statistics, cervical checks + Bishop score, induction trade-offs, low-fluid readings (push for the deepest-vertical-pocket measure; hydrate before the scan; ask for a repeat before agreeing to immediate induction), non-stress tests (and the "just keep clapping" hack), natural labor-induction methods (breast stimulation works; tea/sex/oil don't)
- **Weeks 32–40** (birth plan + labor): C-section / breech / ECV, epidural pros/cons (mom-side complications worth knowing), water breaking + 12-hour induction window, eating in labor, doula evidence (halves C-section rate in some studies), intermittent vs continuous fetal monitoring, episiotomy (not routine), Pitocin in third stage (good for hemorrhage prevention), delayed cord clamping (term vs preterm trade-off), vitamin K, eye antibiotics, home birth

If a week's content overlaps with one of these, **read the relevant Oster chapter** before drafting and weave the evidence into the existing six sections. The contested-choice item usually belongs in `This week's to-dos` (under *Decisions to be talking about as a couple*) or in `For your partner` (under *Reading list*).

## Workflow

1. Confirm the week number with the user if not given
2. Pick the audience mode (`combined` / `partner` / `pregnant`) — infer from wording or ask. See `references/audience-modes.md` for what differs between modes.
3. **Check what's already known in this pregnancy.** Before drafting, scan the loaded context (CLAUDE.md, prior weekly files in the same folder, anything the user has volunteered) for couple-specific context. If essentials aren't on the table, ask once: *"Anything I should know before drafting? E.g. NIPT done? Sex known? Anatomy scan booked or done? GTT done? Any complications, medications, or specific decisions I should reflect?"* Adapt the draft to what's known: don't tease decisions already made, don't suggest tests already done, and don't frame the sex-reveal as upcoming if they already know. The user shouldn't have to re-correct context every week — once volunteered, it's part of their CLAUDE.md or is implicit from prior weekly files.
4. Read `references/medical-sources.md` to get oriented on which sources apply to which kinds of claims (use the decision tree at the bottom)
5. Read `references/template.md`, `references/mental-health/mental-health-section.md`, `references/tone-guide.md`, `references/audience-modes.md`, and `references/partner-reading-list.md`
6. Skim `references/diet/nutrition.md` to identify which nutrients, food levers, or supplements are week-relevant — and where they belong across the six sections (see the map at the bottom of that file). Cross-check specific numbers (calorie additions, RDAs, caffeine limits, food-safety items) against `references/diet/diet.md`, and borrow practical framings from `references/diet/diet-practical-guide.md`
7. Skim `references/exercise/exercise-practical-guide.md` for the trimester- and week-relevant movement guidance (target, modifications, what changes this week); pull evidence detail or contraindications from `references/exercise/exercise.md` when needed
8. Check `references/birth/interventions-vaginal-birth.md` for any birth-prep intervention activating this week (PFMT ~12–20w, perineal massage ~34w, dates ~36w, birth-plan items ~32–36w) — use the tiered summary at the bottom, and `references/birth/interventions-vaginal-birth-eli5.md` for plain-language framings
9. Skim `references/mental-health/perinatal-emotional-journey.md` for prevalence, mechanism, and intervention claims relevant to this week's mental-health content. The `-eli5.md` version is a good first read for warm-friend framings. Cross-anchor any mental-health claim against the brief's anchored numbers (depression ~12–18%, partner depression ~8–10% peaking 3–6 months postpartum, etc.) rather than folk numbers.
10. Skim `references/vittorio-protocol.md` for week-anchored timings and pragmatic ideas — but treat it as one input, not the source of truth
11. **If this week is in the first trimester (0 → 13+6),** skim `references/first-trimester/first-trimester-eli5.md` for warm-friend framings, then cross-check specific numbers and timing windows against `references/first-trimester/first-trimester.md`. Dating logic (LMP weeks; CRL-based dating scan 7+0–13+6w is the EDD anchor), embryonic/fetal milestones (organogenesis weeks 3–8; cardiac activity ~6w; neural tube closure ~6w), booking-visit screening package, NIPT/cfDNA per SMFM Consult #74 (Nov 2025, ACOG-endorsed Jan 2026), miscarriage epidemiology and the reassurance gradient, ectopic-pregnancy triage, lifestyle (folic acid USPSTF, alcohol CDC/ACOG, caffeine ≤200 mg/day with Chen 2023 dose-response, paracetamol Ahlqvist 2024), and the T1-specific red flags all anchor here. For NVP/HG mechanism details, defer to `nausea-pregnancy-first-trimester.md`; for Zofran specifics, defer to `zofran.md`. When this brief and a domain spine (diet/exercise/birth/mental-health) cover the same fact, defer to the domain spine for the number and use the first-trimester brief for the trimester-level *integration*.
12. **If this week is in the second trimester (13–27),** skim `references/second-trimester/second-trimester-eli5.md` for warm-friend framings, then cross-check specific numbers and timing windows against `references/second-trimester/second-trimester.md`. Anatomy-scan content (~18–22w), GDM screening (~24–28w), aspirin window (start by 16w), cervical-length / vaginal progesterone, Tdap/RSV vaccine timing, quickening, and supine/aortocaval physiology all anchor here. When this brief and a domain spine (diet/exercise/birth/mental-health) cover the same fact, defer to the domain spine for the number and use the second-trimester brief for the trimester-level *integration*.
13. **If this week is in the third trimester (28 → birth),** skim `references/third-trimester/third-trimester-eli5.md` for warm-friend framings, then cross-check specific numbers and timing windows against `references/third-trimester/third-trimester.md`. The supine/stillbirth signal from 28w (Cronin 2019), movement-awareness framing (AFFIRM 2018 negative on formal kick counts), late-pregnancy screening (anti-D 28w, GBS 36–37w US / risk-factor UK), Tdap/RSV vaccine timing, the 39-vs-41w induction debate, ECV and breech mode-of-delivery choices, preeclampsia severe features (ACOG PB 222), ICP and the Ovadia 2019 ≥100 µmol/L bile-acid threshold, and the T3-specific red-flag escalation thresholds all anchor here. Same precedence rule as for T2: defer to a domain spine when it covers the same fact, and use the T3 brief for trimester-level integration.
14. **If this week is late T2 onwards (≈27w+) or anywhere maternal vaccines (Tdap, RSV, flu) are week-relevant, or any late-T3 "pick a paediatrician / hospital-bag / consent-decisions" week,** skim `references/infant-vaccinations/infant-vaccinations-eli5.md` for warm-friend framings, then cross-check specific numbers and timing windows against `references/infant-vaccinations/infant-vaccinations.md`. Maternal Tdap 27–36w / RSV 32–36w / flu in season → transplacental antibody transfer rationale, the December 2025 ACIP-vs-AAP HepB birth-dose split (AAP retains universal; ACIP moved to individual decision-making for HBV-negative mothers), the maternal-antibody / infant-priming-response interaction (Voysey 2017 IPMA: 20 of 21 antigens), the September 2025 ACIP MMRV de-preferencing (~1 extra febrile seizure per 2,300–2,600 first MMRV doses), the cumulative-antigen-exposure null (Glanz/VSD 2018), the autism literature record (Taylor 2014 / Jain 2015 / Hviid 2019, all null), rotavirus intussusception risk-benefit and the strict age-window rationale, and US/UK/WHO schedule comparison all anchor here. For Tdap/RSV *timing* and the *birth-experience* framing (consent at the hospital, HepB birth-dose conversation, what's offered before discharge), defer to the birth and T3 spines. For *immunology rationale* (why 2/4/6 months, why MMR waits until 12 months, why the schedule is what it is), this is the source of truth.
15. If this week overlaps with one of Oster's chapters (see the chapter-to-week map under *Recurring focus: Expecting Better*), read the relevant section of `/Users/charles/Library/Mobile Documents/iCloud~md~obsidian/Documents/Pregnancy/Research/Feynman/Expecting Better by Emily Oster.md`. Use her evidence and decision-shape, not her voice. When she diverges from Tier 1, present both.
16. Skim `references/example-week-08.md` to calibrate tone and structure — this is the user-approved reference
17. For factual claims about this specific week:
    - Cross-check fetal development across at least two Tier 1 sources (NHS, Mayo, Cleveland, StatPearls)
    - For maternal symptoms, source the *mechanism* from the peer-reviewed physiology papers (Soma-Pillay, Jee & Sawal, Chiang) and put it in the detailed breakdown
    - For nutrition mechanisms and the nutrient–development link, draw on `references/diet/nutrition.md` and cross-check specific dose claims against `references/diet/diet.md` and NHS/NICE/ACOG
    - For exercise claims, anchor to `references/exercise/exercise.md` (guideline-sourced: ACOG 804, WHO 2020, CSEP 2019)
    - For decisions/interventions activating this week, draw on `references/birth/interventions-vaginal-birth.md` (evidence tiers) and Evidence Based Birth, and present options, not prescriptions
18. Generate the file (in `/home/claude/` first if in claude.ai sandbox; directly in working location if in Cowork or CLI)
19. Place the final file in the right destination for the environment (see Output section above)
20. In claude.ai: present with `present_files` and note the destination folder. In Cowork or CLI: confirm the path in your closing message.
21. Briefly note (1–2 sentences) anything notable about this week — major milestone, scan window, decision newly active this week, etc.

## What to avoid

- Do not generate multiple weeks in one invocation
- Do not give medical advice beyond "call your doctor if X" — always defer to their care provider for diagnosis or treatment
- Do not assume circumstances (single parent, twins, IVF, complications) unless user has told you — keep language inclusive but don't over-customise without input
- Do not be preachy about lifestyle (no alcohol, no soft cheese etc.) — mention once in to-dos, don't moralise
- Do not import any single source's voice or stance wholesale — synthesise across sources, translate into the warm-friend register
- Do not present contested choices (declined Hep B at birth, declined eye ointment, induction timing, vitamin K route, etc.) as recommended one way or the other — frame them as conscious decisions for the couple to make with their care provider, briefly noting the evidence on both sides
- Do not include folk wisdom or "old wives' tales" that aren't supported by current evidence (gender by bump shape, heartburn = hairy baby, raspberry leaf tea claims, "eating for two", etc.). The user explicitly wants science-based content.
- Do not cite sources by name inline in the body of the file — the warm-friend voice doesn't have footnotes. Sources inform your reasoning; they don't appear in the body. The static "Sources" footer line (see `references/template.md`) is the single exception, and it's identical across all weeks.
