---
name: fbb-doc-coauthoring
description: Guide Flat Bay Band Inc. (No'kmaq Village) staff through a rigorous workflow for co-authoring community documents — funding proposals, fundraising strategy memos, funder shortlists, concept notes, progress reports, newsletter articles, annual report sections, council briefs, and programme updates — with every claim grounded in the bundled FBB reference library or web-verified at the time of writing (no invented figures, outcomes, council members, eligibility rules, deadlines, or budgets). Trigger when the user mentions Flat Bay Band, FBB, No'kmaq Village, NARMN (Newfoundland Alliance of Rural Mi'kmaw Nations), the Bay St. George Powwow, the Four Directions Departments (Health & Wellness, Community Development, Social Development, Creative Expressions), Mi'kmaq language preservation, or wants to draft any of the document types above for a rural Mi'kmaw community organisation in Newfoundland. Use in preference to generic doc-coauthoring whenever FBB or No'kmaq Village is in scope.
---

# FBB Doc Co-Authoring Workflow

Flat Bay Band Inc. (No'kmaq Village) is a rural Mi'kmaw community organisation on the west coast of Newfoundland, established 1971 and renamed No'kmaq Village in 2012. It governs the communities of Flat Bay East, Flat Bay West, and St. Teresa's, leads the Newfoundland Alliance of Rural Mi'kmaw Nations (NARMN) and mentors other rural Mi'kmaw bands across the island, hosts the annual Bay St. George Powwow (the largest on the west coast of Newfoundland and Labrador, ~10,000 visitors), and operates the Four Directions Departments — Health & Wellness; Community Development; Social Development; Creative Expressions — alongside cross-cutting work in governance, infrastructure, environmental stewardship, employment & training, youth wellness, and Mi'kmaq language preservation. FBB's documents reach a varied audience: federal and provincial Indigenous funders, Indigenous-led foundations, mainstream foundations with Indigenous portfolios, NARMN partners, the Mi'kmaq Confederacy and Atlantic regional bodies, the band membership, and the general public.

This skill guides the user through four stages — **Orientation → Context Gathering → Refinement & Structure → Reader Testing & Cultural-Fit Review** — tailored to that audience. It extends the generic doc-coauthoring workflow with Indigenous-funder identification (using a three-track eligibility framework — Indian Act bands / Section 35 / self-identified), evidence-grounding rules, and a cultural-fit and rigor audit that catches unsupported claims, eligibility-track mismatches, and tone lapses before a funder reviewer or community member does.

## Before you begin: read the reference folder

The skill ships with a `references/` folder containing six Markdown files. **Read them at the start of every engagement.** This is the single most important thing you do — it's what keeps the output grounded in what FBB actually does rather than plausible-sounding fabrication.

Priority order:

1. **`2026-04-28_FBB_Funding_Landscape_Report.md`** — the funding landscape (federal Indigenous-specific programmes, federal Indigenous streams within general programmes, NL provincial programmes, Atlantic regional bodies, Indigenous-led national foundations, mainstream foundations with Indigenous portfolios, international/cross-border, non-grant revenue channels — sponsorships, social-enterprise, the Bay St. George Powwow as a revenue mechanism, NARMN partnerships). Includes a three-track eligibility framework, an alignment matrix, strategic recommendations split by track, and a URL accessibility appendix flagging stale or changed pages. Read in full for any grant or fundraising document.
2. **`website-flatbaybandinc-home.md`** — community/location overview, contact details, Mi'kmaq tagline (*Ewipkek* — Calm Waters). Read for any document.
3. **`website-flatbaybandinc-about.md`** — history, mission, governance values.
4. **`website-flatbaybandinc-departments.md`** — what each Four Directions department does and how the Human Resources function works.
5. **`website-flatbaybandinc-band-council-and-staff.md`** — Council members and staff names, roles, and biographies. Read whenever a person is to be named in the document.
6. **`website-flatbaybandinc-language-and-culture.md`** — language preservation, Francis-Smith orthography, language-teaching films, cultural revitalisation activities.

Also bundled (informational, not a content reference):

- **`CHANGELOG.md`** — substantive changes to this skill over time. Read if you need to understand why a particular rule or pattern is in place, or before suggesting a change to the skill.

### Provenance: where these files came from

The reference library is a *snapshot*, not a live mirror. Treat the upstream sources as authoritative whenever there is any chance they have moved on:

- **Files `website-flatbaybandinc-*.md`** contain content scraped from the FBB website (flatbayband.ca/fbb-wp/) at the time the skill was packaged. The live website — not the Markdown — is the source of truth. FBB updates its site (council changes, new programmes, powwow news, language-programme additions); for any claim that will appear in a funder-facing or community-facing document, re-fetch the relevant page with `web_fetch` (or have the user check the page) before citing.
- **`2026-04-28_FBB_Funding_Landscape_Report.md`** was generated using a deep-research agent on 2026-04-28. URL accessibility was tested at generation time and a URL accessibility report is appended to the file. The funder websites — not the Markdown — are the source of truth: budget envelopes, deadlines, eligibility rules, eligibility-track tags, and call status all change frequently and need web verification before they appear in a draft.

If a Markdown file disagrees with the live source, the live source wins.

After reading, give the user a brief orientation summary that proves you absorbed the material — e.g., "I've read the references. For a 2026 Mi'kmaq language-programme proposal targeting an Indigenous-led foundation (Track C eligible), the most relevant FBB programme components are the Francis-Smith orthography teaching films and the language-and-culture summer camp; the best-fit funders given the eligibility-track ambiguity around FBB's recognition status are the Indigenous Peoples Resilience Fund, the First Peoples' Cultural Council, and the Inspirit Foundation. Shall we proceed?" — then move to Stage 1.

If the `references/` folder is missing or incomplete, tell the user, ask whether to continue in degraded mode or pause, and be explicit about what grounding you'll be missing.

## When to offer the workflow

Offer the full four-stage workflow when the user wants to produce a substantive document (more than ~300 words, or anything a funder, partner organisation, or external community will see). For shorter outputs (a one-line social post, an internal email), work freeform.

Open with a brief explanation of the stages and ask whether the user wants to proceed structured or freeform. Use `AskUserQuestion` to make this a one-click choice (see the next section). If freeform, still respect the reference-grounding and anti-hallucination rules below — they are non-negotiable regardless of workflow mode.

## Using structured-input prompts (`AskUserQuestion`)

Many decision points in this workflow are inherently multiple-choice — document type, audience, programme area, which funder to target, which section to start with, whether to advance to the next stage. When the `AskUserQuestion` tool is available, prefer it at these points over free-text questions. Structured prompts (a) reduce cognitive load on busy programme staff and Council members, (b) make the workflow feel faster and more deliberate, and (c) produce cleaner decision records that are easy to refer back to.

**Use `AskUserQuestion` at these specific points:**

1. **Workflow mode choice** (top of every engagement) — "structured four-stage workflow" vs. "freeform, I'll steer".
2. **Stage 1 Q1** — document type (12 options below).
3. **Stage 1 Q2** — primary audience (10 options below).
4. **Stage 1 Q3** — FBB programme area(s), multi-select.
5. **Eligibility track confirmation** — `[Track A — Indian Act band]` / `[Track B — Section 35 / self-government / modern-treaty]` / `[Track C — self-identified Mi'kmaq / non-status]` / `[Don't know — show me funders across all tracks]`. This step is mandatory for any grant-related document and is the most consequential single decision in the workflow.
6. **Funder shortlist** — after you present 5–8 verified candidate funders with track tags, use `AskUserQuestion` so the user can pick the primary target (and, for fundraising strategy docs, flag secondary/tertiary targets) in one click rather than typing names back.
7. **Section ordering at the start of Stage 2** — which section to draft first.
8. **Structure approval at the start of Stage 2** — "use the default section structure for [doc type]" vs. "adjust it" vs. "start from scratch".
9. **Stage transition gates** — whenever you reach the boundary between stages (→ Stage 2 drafting, → Stage 3 testing, → Final Review), offer "proceed", "add more context / refine more first", or "pause".
10. **Skip-a-stage confirmations** — if the user signals they want to bypass info-dumping, section-by-section discipline, or Reader Testing, present the skip as a structured choice with the trade-off in the option label (e.g., "Skip funder identification — I'll lose call-specific tailoring and may miss eligibility-track fit").
11. **Exit points** — "document is done", "one more review pass", or "fix specific issues first".

**Do not use `AskUserQuestion` for these:**

- The info-dump in Stage 1 (free-text is the point).
- The 5–10 clarifying questions at the end of Stage 1 context gathering (numbered list with shorthand replies is fine).
- Brainstorm curation in Stage 2 Step 3 (keep/remove/combine is too nuanced for canned options — let the user reply in shorthand like "keep 1, 4, 7; drop 3; combine 2+5").
- The refinement feedback loop in Stage 2 Step 6 (the user's edits are inherently free-form prose).
- Any question that is genuinely open-ended (why, how, what else).

If `AskUserQuestion` isn't available in the session, fall back to numbered options the user can reference by number.

## Stage 1: Context Gathering

**Goal:** close the gap between what the user knows and what you know, and commit to a specific document type, audience, eligibility track (where relevant), and target funder/partner.

### Always ask before drafting (even when the user gave a detailed brief)

Even when the user supplies what looks like a complete spec — document type, length, funder, deadline — **do not skip the clarifying loop**. FBB staff often hand off a one-line ask that hides important context (which Council resolution underpins the proposal, which NARMN partners are involved, which Elder or Knowledge Keeper has been consulted, whether Mi'kmaq orthography needs language-programme review, which prior submission to mirror or distance the new draft from). Producing a polished first draft against an under-specified brief usually wastes more of the user's time than asking 2–3 questions up front.

The minimum bar before you generate any draft text:

1. Run **Q1, Q2, and Q3 below** (document type, audience, programme area) — even if the user already mentioned them, confirm them via `AskUserQuestion` or restate them and ask "is this right?"
2. For grant-related work, confirm the **eligibility track** (Q3a below) before any funder shortlist is drawn.
3. Ask **at least one targeted question** that draws on FBB-specific context the model can't know — e.g., "Which Council members should be named on this proposal? Anyone we should *not* include?", "Which NARMN partner organisations are co-applicants?", "Has the language programme reviewed the Mi'kmaq terminology used in this draft?", "Is the Council resolution number for this initiative on file? What is its date?"
4. If the user explicitly says *"just draft it, I'll edit"*, honour that — but at the top of the draft include a short `## Open questions for the user` block listing the 2–3 questions you would otherwise have asked, so the user can answer them inline during review.

### Initial questions

Ask these early. When the `AskUserQuestion` tool is available, use it for Q1, Q2, and Q3a so the user can pick from options quickly; use free-text for the rest.

**Q1. What type of document are we producing?**

- Funding proposal narrative (full application)
- Letter of intent / concept note / expression of interest
- Fundraising strategy document ("top funders to approach for project X")
- Funder-matching / opportunity shortlist (the deliverable itself is the shortlist)
- Progress / interim report to a current funder
- Final / end-of-grant report
- Newsletter article (e.g., for the Powwow, language camp, programme launch)
- Annual report section or institutional profile
- Council brief / governance memo
- Programme update / community communication
- Press release, blog post, or social-media post
- Language & culture document (curriculum note, film description, orthography brief)
- Other (user specifies)

**Q2. Who is the primary audience?**

- A specific named funder (ask which — e.g., ISC, CIRNAC, Canadian Heritage Indigenous Languages, FNIHB, ESDC ISET, NL Office of Indigenous Affairs and Reconciliation, ArtsNL, ACOA Indigenous, Indspire, Indigenous Peoples Resilience Fund, First Peoples' Cultural Council, McConnell Foundation Indigenous stream, Inspirit Foundation)
- A generic funder (no specific call yet — funder identification happens below)
- Indigenous-led national foundation
- Federal or provincial Indigenous Affairs body
- NARMN partners or Mi'kmaq Confederacy / Atlantic Policy Congress of First Nations Chiefs / Ulnooweg / Atlantic First Nations Water Authority
- Band membership / community
- General public / media
- Internal Council and staff
- Academic / research / cultural partner (university, museum, school board)
- Other (user specifies)

**Q3. Which FBB programme area(s) does this cover?** (multi-select is fine)

Health & Wellness · Community Development (Memberships & Cultural Connections, Employment & Training, Environment & Development) · Social Development (Social Empowerment & Equity) · Creative Expressions · Governance & Self-Determination · Infrastructure · Environment & Land Stewardship · Language & Cultural Revitalisation · Youth & Elders · Capacity Building & Mentorship of NARMN partners · Cross-cutting

**Q3a. Eligibility track** (mandatory for any grant-related document)

- `[Track A]` — Indian Act band recognised by Indigenous Services Canada
- `[Track B]` — Section 35 / self-government / modern-treaty signatory
- `[Track C]` — Self-identified Mi'kmaq / non-status Indigenous organisation
- `[Don't know]` — Show me funders across all three tracks; FBB leadership will narrow later

This determines the funder universe. If the user is uncertain, default to "show me all three tracks" and tag every funder with the track(s) it accepts. Do not pre-narrow; do not assume.

**Q4. Is there a specific programme, project, or initiative this document centres on?**
(e.g., "Bay St. George Powwow 2026 sponsorship pitch", "Francis-Smith orthography teaching films expansion", "Employment & Training programme renewal", "Environment & Development habitat-stewardship project", "language-and-culture summer camp"). If yes, note the name — you will ground claims in the relevant reference file and, where needed, web-verify outputs.

**Q5. Deadline, word/page limit, and any template the funder provides?**

**Q6. What is the desired impact when someone reads this?**
(e.g., "secure renewal funding for the language programme through 2029", "win a sponsorship from Atlantic Canada Opportunities Agency for the Powwow", "convince a new private foundation to partner with FBB", "brief Council on the eligibility-track decision")

### Funder identification (mandatory for grant-related documents)

If Q1 is a funding proposal, letter of intent, concept note, fundraising strategy, or funder-matching document, **and** Q2 did not lock a specific funder, identify candidate funders before drafting anything. This is the step that most distinguishes useful FBB documents from generic ones.

Process:

1. From the **Funding Landscape Report**, shortlist 5–8 funders whose mandate, geography, eligibility-track tag, and funding envelope align with the programme area(s) in Q3 and the work type. The report's alignment matrix is the starting point.
2. **Honour the Q3a eligibility-track decision.** If the user selected a single track, restrict the shortlist to funders accepting that track (and explicitly flag any high-fit funders that the track decision excludes, so the user can reconsider). If the user selected "Don't know", surface candidates from all three tracks and tag each entry clearly.
3. For each shortlisted funder, use `web_search` and/or `web_fetch` (e.g. `mcp__workspace__web_fetch` in Cowork) to verify:
   - The programme is still active and Indigenous-eligibility is intact (federal Indigenous-stream programmes shift between budget cycles; the most recent federal-budget cycle and any provincial NL Indigenous-strategy update should be checked).
   - The specific call or mechanism cited in the reference is currently open or has an announced next cycle.
   - Current budget caps, eligibility rules, and deadlines (these shift frequently; references dated 2026-04-28 should not be trusted for these details without re-verification).
   - **Verbatim eligibility language.** Distinguish "First Nations" from "Indigenous" from "Indigenous-led organisations" — these are not interchangeable in Canadian funder language and the difference can disqualify a proposal.
4. Present the verified shortlist to the user with a one-line rationale per funder, the eligibility-track tag(s), the live URL, the current call status, and the approximate budget/duration. Let the user pick the primary target (and, for fundraising strategy documents, secondary and tertiary).
5. For the chosen primary funder, fetch the current call text and distil it: scope, eligibility (verbatim), budget cap, deadline, required document format, mandatory partnerships, submission portal. This distillation becomes the structural spine for Stage 2.

For a funder-matching or fundraising strategy document, this step **is** the deliverable — Stage 2 will then produce the strategy write-up rather than a full proposal.

### Info dumping

Once Q1–Q6 are answered (and, where relevant, the eligibility track and target funder are locked), invite the user to dump everything else they have: programme concept notes, prior proposals (successful or not), draft aims, lead names and CVs, programme outputs (powwow attendance figures, language-camp enrolments, training participants, films produced), partner letters, community engagement notes, Council resolutions, meeting minutes. Ask them not to worry about organisation.

When the dump slows, ask 5–10 numbered clarifying questions to fill gaps. Let the user answer in shorthand.

**Exit condition:** edge cases and trade-offs can be discussed without needing basics re-explained. Eligibility track is locked or explicitly flagged as ambiguous. Target funder is locked (if grant work). The community context, programme aims, and FBB's specific role are clear. Proceed to Stage 2.

## Stage 2: Refinement & Structure

**Goal:** build the document section by section, with every substantive claim grounded in a reference file or a web-verified source.

### Tone and language guidelines

FBB documents should read as the output of a self-determined, Mi'kmaw-led community organisation — not as generic Indigenous-grant boilerplate, and not as bureaucratic prose that buries the lede. Hold to these standards for every paragraph:

- **Mi'kmaw-led framing.** FBB's tagline is *Ewipkek — Calm Waters*. Lead with FBB's self-determined community work, NARMN partnerships, and language & cultural revitalisation rather than positioning FBB as a passive recipient of Crown or non-Indigenous funding. Avoid phrasing that casts Mi'kmaw communities as objects of intervention.
- **Respect for Mi'kmaq language conventions.** Use Mi'kmaw / Mi'kmaq terms accurately and consistently; spell using the **Francis-Smith orthography** that FBB's language programme uses. When unsure of spelling or usage, leave a `[USER INPUT NEEDED: Mi'kmaq term confirmation from language programme]` placeholder rather than guess.
- **Quantitative specificity.** Use actual numbers from the references where possible — three rural communities governed (Flat Bay East, Flat Bay West, St. Teresa's), 1971 founding year, 2012 renaming as No'kmaq Village, the Bay St. George Powwow as the largest powwow on the west coast of Newfoundland and Labrador (~10,000 visitors), the Four Directions Departments — rather than adjectives like "extensive", "substantial", or "many". If a number is not in the references and cannot be web-verified, do not invent one; either describe the work qualitatively or leave a `[NEEDS SOURCING]` placeholder.
- **Funder-native vocabulary, when it fits.** Mirror the target funder's language where it's accurate, not performative. For an ISC programme, use ISC's own programme name and eligibility framing. For Canada Council Indigenous arts, use the programme's terminology. For an Indigenous-led foundation, mirror the foundation's framing of community-led work. Use these phrases when they are accurate to the call; don't force them.
- **Distinguish Indigenous-only from Indigenous-stream.** Many federal and provincial programmes have an Indigenous priority but accept all applicants; do not present these as Indigenous-only. The Funding Landscape Report tags this distinction explicitly — preserve it in the draft.
- **Respectful tone for Council, Elders, Knowledge Keepers, NARMN partners.** Use full names and titles where accuracy matters; verify against `website-flatbaybandinc-band-council-and-staff.md` and ask the user for any updates. Where a person is named, the name and role should be retrievable from a reference or from the user.
- **No slop.** Every sentence should carry weight. If a sentence could be deleted without the paragraph changing meaning, delete it. Generic aspirational language ("transformative impact", "ground-breaking", "world-class") is a red flag unless you can immediately back it up with an outcome.

### Evidence-grounding rules (anti-hallucination — non-negotiable)

These are the single most important rules in this skill. An FBB document that invents a statistic, a Council member's name, or a funder eligibility rule does more harm than a document that never gets written.

1. **Only reference figures, programme outcomes, council/staff names, partner organisations, funder mandates, budget figures, deadlines, eligibility criteria, eligibility-track tags, or conclusions that are (a) described in the `references/` folder, or (b) retrievable via `web_search` / `web_fetch` at the time of writing.** Do not invent powwow attendance figures, programme participant counts, films produced, training graduates, Council resolution numbers, partner letter dates, funder budget caps, deadlines, or eligibility rules.
2. **Verify before citing — references can be stale.** Funder calls close, budget envelopes change, Council members rotate, programmes end, URLs move. For any claim that will influence a funder reviewer's decision (current deadlines, current budget caps, current eligibility, current track tags, current Council composition), web-verify *before* putting it in the draft. The Funding Landscape Report contains a URL accessibility appendix — it already flags broken or changed links; treat all of them as requiring re-verification.
3. **When sourcing is uncertain, flag — don't fabricate.** If you can't ground a claim, either drop it or draft it with a `[NEEDS SOURCING: <specific claim>]` placeholder and surface it to the user for verification. Never guess a number to fill a gap.
4. **When FBB-specific context is needed (and only the user knows it), use a `[USER INPUT NEEDED: …]` placeholder.** The reference library covers public FBB outputs; it does not know which Council member should sign a letter, which internal programme statistics are shareable, what was decided in last week's Council meeting, which related NL Indigenous-strategy document the brief should align to, or whether the language programme has approved a particular Mi'kmaq term in the draft. For each such gap, write a placeholder like `[USER INPUT NEEDED: name and role of the Council member signing this letter]` or `[USER INPUT NEEDED: most recent Council resolution and date that authorises this submission]` or `[USER INPUT NEEDED: language-programme review of Mi'kmaq terminology in §2]`. Surface a list of these placeholders at the top of the draft.
5. **Cite inline while drafting, with verifiable links wherever possible.** Every substantive claim gets a short source tag in the working draft. Three forms, in order of preference:
   - `(web: <funder programme name>, <https://…>, verified YYYY-MM-DD)` for funder calls, government programmes, FBB website pages, partner-organisation pages, news items — preferred whenever the cited source is a public web page.
   - `(web: <publication title>, DOI 10.xxxx/yyyy)` for any cited evaluation, scholarly output, or report with a DOI.
   - `(ref: <filename>.md)` or `(ref: <filename>.md → <section>)` as the *fallback* when no web-verifiable source exists — for example, internal-only context from the bundled reference summary. A document that cites only `ref:` markers is harder for a funder reviewer or community member to verify than one that cites URLs/DOIs, so prefer the `web:` forms wherever the underlying source is publicly accessible.

   These tags stay in the working draft so the user and the Reader Claude pass in Stage 3 (a fresh, context-free reader — sub-agent or fresh Claude.ai chat; defined at the top of Stage 3) can audit the evidence chain; they get converted to the funder's required citation format only in the final pass.
6. **Always end with a verifiable References section.** Every funding proposal, fundraising strategy, concept note, progress report, council brief, and externally-facing newsletter article with substantive claims should close with a `## References` block that lists each cited source as a clickable URL or DOI — never as a bare `(ref: …)` marker alone. This is what lets the user (and the eventual funder reviewer or community reader) confirm the document in five minutes rather than five hours.

### Default length when the user didn't specify

If the user supplied a length, follow it. Otherwise default a *first* draft to the lower end of what the document type can carry, and offer to expand:

- Letter of intent / concept note: 1 page.
- Fundraising strategy: 1 page (single-pager that the user can share with Council and leadership). Offer to expand to a longer pipeline document if the user wants it.
- Council brief / programme update / newsletter article: 1 page.
- Progress / interim report, programme summary: 1–2 pages.
- Annual report section: per the report's section structure, typically 1–2 pages per section.
- Funding proposal narrative: scope to the funder's word/page limit; if no limit, 6–10 pages.

A leaner first draft is easier to react to than a long one. Once the user has reviewed, ask whether to expand specific sections rather than expanding everything.

### Section structure by document type

If the funder provides a template, use it exactly — funder templates are non-negotiable. Otherwise, use these defaults and confirm with the user before drafting. The bracketed `[…]` items mark sections that almost always require user input on FBB-specific knowledge — leave them as `[USER INPUT NEEDED: …]` placeholders if not supplied.

- **Funding proposal narrative:** Project title → Problem statement & community context → Proposed approach (aims) → Programme area alignment & FBB capacity → Team, governance, and partner engagement (Council, NARMN partners, Elders / Knowledge Keepers, community) → Timeline & milestones → Risk analysis & mitigation → Budget justification → References.
- **Letter of intent / concept note:** Project title → Problem statement → Proposed approach (aims in one paragraph) → Expected impact and alignment with funder priorities (with verbatim eligibility-language match) → FBB & partner capacity → Budget envelope → Next steps → References (with URLs/DOIs to FBB programmes and any cited evaluations).
- **Fundraising strategy document:** Executive summary → FBB programme priorities (mapped to Four Directions areas + cross-cutting workstreams) → Funder landscape (top 5–8 funders with verified eligibility-track tags, current call status, and budget) → Proposal pipeline → Submission calendar → Risk factors (federal-budget shifts, provincial strategy changes, eligibility-track ambiguity) → **Action items & key decisions** (a short, sequenced list of what Council and leadership need to decide and who owns each — this is what makes the doc useful in a meeting) → References / live funder URLs.
- **Funder-matching shortlist:** For each funder: name, mechanism, URL, **eligibility-track tag(s)**, verified call status, budget envelope, deadline, eligibility (verbatim where consequential), fit rationale, FBB lead, required partnerships.
- **Progress / interim report:** Original aims → Progress against each aim → Milestones achieved vs. planned → Outputs (programmes delivered, language films produced, powwow attendance, training graduates, etc., with verified figures) → Budget status → Variances and explanations → Forward plan → Requests to funder.
- **Council brief / governance memo:** Issue in two sentences → **Related Council resolutions and current FBB governance context** (`[USER INPUT NEEDED: most recent Council resolution and date that bears on this issue]` — the model cannot know this) → Options (usually 2–3) → Recommended option → Implementation considerations → Key references.
- **Newsletter article / programme update:** Hook → What's happening → Who's involved (with verified names and titles from the band-council-and-staff reference) → Why it matters to the community → How to participate or learn more → References / URLs.
- **Annual report section:** Section heading → Programme summary → Activities and outputs (with numbers from references or internal data) → Partnerships → Forward plan → Acknowledgements (with verified names of funders, partners, Council, Elders).
- **Language & culture document:** Follow the language programme's existing conventions; ask the user to confirm Mi'kmaq orthography and terminology *before* finalising. Flag any term that has not been reviewed by the language programme with `[CULTURAL REVIEW NEEDED: …]`.

### Section-by-section workflow

For each section, follow the base loop:

1. **Clarifying questions** — ask 5–10 specific questions about what the section should cover.
2. **Brainstorming** — generate 5–20 numbered options (more for complex sections like Aims or Programme Area Alignment, fewer for short sections like Budget Envelope).
3. **Curation** — ask the user which to keep/remove/combine. Accept shorthand ("keep 1, 3, 7; drop 4 (already covered); combine 2+5").
4. **Gap check** — ask if anything important is missing.
5. **Draft** — use `Write` (for new sections) or `Edit` / `str_replace` (for revisions). While drafting, apply the evidence-grounding rules above — every substantive claim gets a source tag or a `[NEEDS SOURCING]` flag.
6. **Iterative refinement** — the user indicates changes; you apply them with Edit. After 3 consecutive iterations with no substantial changes, ask whether anything can be cut without losing information.

Never rewrite whole sections when a surgical edit will do — it wastes tokens and loses earlier refinements.

### Near-completion pass

When 80%+ of sections are drafted, re-read the full document and check:

- Flow and consistency across sections
- Numerical contradictions (e.g., powwow attendance stated differently in two paragraphs; participants count mismatched between Activities and Budget)
- Any open `[NEEDS SOURCING]` or `[CULTURAL REVIEW NEEDED]` flags
- Eligibility-track alignment with the target funder (no Track-C-only funder framed as if FBB had Track A status; no Track-A-only funder targeted from a Track-C posture)
- Verbatim eligibility-language alignment (the draft uses the funder's words where it matters)
- Word/page limit compliance
- Any generic or promotional language that slipped in

Surface issues to the user before moving to Stage 3.

## Stage 3: Reader Testing & Cultural-Fit Review

**Goal:** stress-test the document with a fresh-eyes reviewer pass and audit its evidence, eligibility-track fit, and cultural integrity.

> **What "Reader Claude" means here.** "Reader Claude" is shorthand for a Claude instance reading the document with **no conversation context** — only the document itself plus a question. The point is to simulate how an actual funder reviewer or community reader will encounter the doc: with none of the context built up in this chat. How you run it depends on the client:
> - **Agentic clients with sub-agents** (Claude Code, Cowork, the Claude Agent SDK): spawn a sub-agent via the `Agent` tool with only the document and the question.
> - **Chat-only clients without sub-agents** (e.g., plain Claude.ai): ask the user to open a fresh Claude.ai conversation, paste the document, and ask the reviewer-style questions there. Have them paste the answers back so you can analyse them together.
>
> Either way, missed answers point to gaps in the document, not to limits of the reader.

### Step 1: Predict reviewer questions

Generate 5–10 questions a reviewer at the target funder would realistically ask when reading the document cold. Examples, tailored by funder type:

- ISC: "Which Indian Act band registration applies? What is the agreement number and the band's recognition status?"
- CIRNAC: "How does this strengthen self-government / Section 35 implementation? Which modern-treaty or self-government framework applies?"
- Indigenous-led national foundation (Indspire, Indigenous Peoples Resilience Fund, First Peoples' Cultural Council): "How is this Indigenous-led? Who are the Mi'kmaw partners and what is their role? How is community consent ensured?"
- NL provincial Indigenous Affairs / ArtsNL Indigenous stream: "How does this align with the provincial Indigenous strategy and the Department's mandate? Is there a NARMN-wide rationale?"
- Mainstream foundation Indigenous portfolio (McConnell, Inspirit, Lawson, RBC): "What's the path to community impact? How is this evaluated? Who else funds this work?"
- ACOA Indigenous stream: "How does this contribute to economic development in Atlantic Canada? What's the leverage from FBB and partners?"
- Generic: "Why FBB? Why now? What's novel? What's the risk and mitigation? Who has Council and community sanctioned this work?"

### Step 2: Run the Reader Claude pass

Run the reader pass for each predicted question, using whichever path fits the client (see the note at the top of this stage). In an agentic client, spawn a sub-agent via the `Agent` tool with **only** the document and the question. In a chat-only client, walk the user through running the question in a fresh Claude.ai conversation. Either way, summarise for the user what Reader Claude got right, what it misinterpreted, and what it couldn't answer.

### Step 3: Cultural-fit & rigor audit (FBB-specific addition)

In addition to the standard Reader Claude checks, run a separate rigor-audit pass (sub-agent or fresh chat, same dual-path pattern). Give it the document and ask it to report:

1. **Unsupported claims.** Every statement that reads as a factual claim (a number, a programme outcome, a person's name and role, a funder mandate, an eligibility rule, a deadline, a Council resolution date) without a source tag or citation. List each verbatim.
2. **Tone lapses.** Sentences that read as vague, promotional, or generic rather than precise and evidence-based ("transformative", "ground-breaking", "world-class", "many", "extensive"). Flag with a tighter rewording.
3. **Funder-fit & eligibility-track mismatches.** Anything in the document that doesn't match the target funder's eligibility track, priorities, eligibility language, required format, word limit, or mandatory partnership structure. Flag with the specific funder requirement being missed. This is the single most expensive failure mode — it can disqualify the proposal at intake.
4. **Cultural-fit issues.** Mi'kmaq terminology, Francis-Smith orthography, framing of Elders / Knowledge Keepers, attribution of NARMN partners, or representation of Council that needs review by FBB's language and culture programme. Flag with `[CULTURAL REVIEW NEEDED: …]`.
5. **Internal contradictions.** Numbers that differ across sections, aims that don't match methods, budget items not reflected in the narrative, names spelled differently in different places, dates that don't add up.

### Step 4: Ambiguity and assumptions check

Run the standard sub-agent pass for ambiguity, implicit assumptions, and contradictions from the base doc-coauthoring workflow.

### Step 5: Report and fix

Report all issues found. For each, propose a fix. Loop back to Stage 2 for any section with open issues. Do not advance while any `[NEEDS SOURCING]` or `[CULTURAL REVIEW NEEDED]` flag is still open.

**Exit condition:** Reader Claude answers the reviewer-style questions correctly, the rigor audit reports zero unsupported claims and zero funder-fit / eligibility-track mismatches, the cultural-fit pass is clean (or all flags have been resolved by the language programme), the ambiguity pass is clean, and the user is satisfied.

## Final review

Before declaring the document done:

1. Remind the user they own this document — ask them to do a final read-through themselves.
2. Encourage them to verify every URL, eligibility-track tag, deadline, budget figure, and named individual one more time, especially anything near the submission deadline.
3. For any document with Mi'kmaq language content or cultural framing, confirm the language and culture programme has reviewed and approved.
4. Confirm the document achieves the impact stated in Q6 of Stage 1.
5. For grant submissions: confirm the funder's submission-portal requirements (file format, cover letter, mandatory annexes, required attachments) with the user — references can't be authoritative about portal mechanics.
6. For Council-facing documents: confirm the relevant Council resolution number and date are cited.
7. Offer to save the final document to the user's workspace folder via computer:// link and present it with the `mcp__cowork__present_files` tool so they can open it directly.

## Tips for effective guidance

- **Be direct and procedural.** FBB programme staff and Council members are busy; don't oversell the process, just run it.
- **Explain the "why" when it shapes behaviour.** If you're pushing back on a claim for lack of a source, say so — don't just ask for a rewrite. If a sentence is too promotional, name the funder convention it violates. If a Mi'kmaq term needs review, say which review pathway (the language programme).
- **Respect the user's agency.** If they want to skip a stage, let them, but flag the specific risk ("skipping eligibility-track confirmation means I can't filter funders correctly — fine to proceed?").
- **Never let unsupported claims into the final draft.** This is the single biggest quality risk and the easiest thing for a reviewer or community member to catch.
- **Offer to update the references.** The Funding Landscape Report is dated 2026-04-28 and will age. If the user learns of a new call, a closed mechanism, a new partner organisation, or a Council change, offer to note it and, with permission, append a supplement file to `references/`.

## How this skill differs from generic doc-coauthoring

1. It grounds every engagement in a bundled FBB reference library before drafting.
2. It treats funder identification with the **three-track eligibility framework** (Indian Act / Section 35 / self-identified) as a mandatory early step for grant-related work, with verbatim eligibility-language matching against each funder.
3. It enforces evidence-grounding rules that prohibit invented figures, names, programme outcomes, eligibility rules, deadlines, or budget caps — and requires inline source tags during drafting.
4. It adds a cultural-fit and rigor audit to Reader Testing that catches unsupported claims, tone lapses, eligibility-track mismatches, and Mi'kmaq language/cultural-framing issues.
5. It writes in FBB's institutional voice: Mi'kmaw-led, evidence-dense, quantitatively specific, funder-native but never generic, respectful of Council, Elders, NARMN partners, and the language programme.

## Reference files

The `references/` directory has the FBB knowledge corpus and a CHANGELOG:

- `2026-04-28_FBB_Funding_Landscape_Report.md` — funding landscape across federal Indigenous-specific programmes, federal Indigenous streams within general programmes, NL provincial programmes, Atlantic regional bodies, Indigenous-led national foundations, mainstream foundations with Indigenous portfolios, international/cross-border, and non-grant revenue channels (sponsorships, social-enterprise, Bay St. George Powwow as a revenue mechanism, NARMN partnerships); three-track eligibility framework; alignment matrix; strategic recommendations split by track; URL accessibility appendix. Use for any grant or fundraising document.
- `website-flatbaybandinc-home.md` — community/location overview, contact details, *Ewipkek — Calm Waters* tagline. Use for any document.
- `website-flatbaybandinc-about.md` — history, mission, governance values.
- `website-flatbaybandinc-departments.md` — Four Directions Departments and the Human Resources function.
- `website-flatbaybandinc-band-council-and-staff.md` — Council members and staff names, roles, biographies. Use whenever a person is named.
- `website-flatbaybandinc-language-and-culture.md` — language preservation, Francis-Smith orthography, language-teaching films, cultural revitalisation activities.
- `CHANGELOG.md` — substantive changes to this skill over time.
