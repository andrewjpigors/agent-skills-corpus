---
name: digital-you-builder
description: Walk a BC REALTOR® through assembling their Digital You profile — the persistent identity layer that makes every AI output sound like them and know their market. Triggers on "Digital You", "build my profile", "set up my Claude Project", "AI assistant profile". Includes full BCFSA advertising compliance gate, Competition Act 2025 substantiation requirements, BC Human Rights Code s.7 screening, CASL consent framework, BC PIPA voice/biometric data prohibition, and licence/brokerage verification.
---

# Digital You Builder

> **Jurisdiction:** This skill is designed for **licensed BC REALTORS®** operating in **British Columbia**. All regulatory references are BC-specific.

Help a BC REALTOR® build their **Digital You** — a structured set of files they upload to a Claude Project so that every AI output sounds like them, knows their market, and serves their specific clients — within the full BC regulatory framework for advertising, human rights, privacy, and anti-money laundering.

Think of it as onboarding a new, very capable assistant who has never met you. Everything they'd need to know, written down, in the right format, with compliance built in from the start.

---

## What This Skill Does

- Guides the agent through building their professional identity files, step by step
- Produces formatted, ready-to-upload file content for each section
- Screens all content for BCFSA advertising compliance, Competition Act 2025 substantiation requirements, BC Human Rights Code s.7 compliance, and CASL consent obligations
- Enforces a hard prohibition on voice sample uploads (BC PIPA — biometric data)
- Ensures brokerage name, licence number, and required disclaimers are embedded in all files before use

---

## How to Use It

**Mode A — Guided Build (no files provided yet)**
Agent says "help me build my Digital You" or "where do I start." Walk through the question sets below, section by section. After each section, format answers into a ready-to-paste file block.

**Mode B — File Formatter (they paste raw content)**
Agent pastes an existing bio, email, or client list. Reformat it into the correct Digital You file structure, running BC regulatory compliance screening on all content, without asking questions already answered.

Offer Mode A or Mode B at the start if ambiguous.

---

## ⚖ MANDATORY BC COMPLIANCE SECTION

### 1. BCFSA Advertising Standards Gate (RESA ss.40–42, BC Reg 209/2021)

**This gate runs before any public-facing content is finalized.**

All advertising must:
- Be **accurate**, **not misleading**, and **capable of being substantiated** (RESA s.40)
- Include the **brokerage name** — non-negotiable under BCFSA advertising rules
- Include the **agent's BCFSA licence number** in all advertising and promotional content
- Not misrepresent the licensee's **qualifications or experience** (RESA s.42)

**Qualifications and experience — RESA s.42:**
Any claim about the agent's experience, designations, certifications, or expertise must be accurate and not give a false impression. Examples that require scrutiny:
- "Luxury specialist" — what is the basis? Is it a recognized designation or self-description?
- "Expert in presales" — is this based on documented transaction history?
- "Top investment advisor" — investment advice is outside RESA scope entirely (see Referral Triggers)

---

### 2. Competition Act 2025 — Track Record Substantiation

**This gate applies to all performance claims and comparative advertising.**

Under the Competition Act (as amended, in force **June 20, 2025**), misleading comparative claims and unsubstantiated performance representations carry a **private right of action** from competitors. This is new — any agent, brokerage, or board can now sue directly for damages caused by misleading advertising.

**Track record claims — required verification before any claim is included:**

| Claim Type | Required Documentation |
|------------|----------------------|
| "Top agent," "#1 agent," "best in the market" | Prohibited unless from a verifiable industry source; state the ranking body, time period, geographic scope, and measurement criteria |
| Transaction count ("sold X homes") | Must be accurate from the agent's verifiable transaction history; state the time period |
| List-to-sale ratio, average DOM | Must be real figures from the agent's own history; state the time period and data source |
| Award references | State the awarding body, year, and criteria; no invented awards |
| Market share claims | State the source, category, geographic area, and time window |

Every statistic included in `voice/about_me.md` must meet this standard before it becomes part of the working AI identity. Claims that cannot be substantiated must be removed or replaced with placeholders pending verification.

---

### 3. BC Human Rights Code s.7 — Advertising Prohibitions

Any language that could constitute a "statement, publication, notice, sign, symbol, emblem or other representation that indicates discrimination or an intention to discriminate" based on a protected characteristic is prohibited. **Intent is not required — effect is the test.**

**Mandatory screening — remove from all Digital You content:**
- Do NOT describe the agent's target client base using demographic or national origin identifiers (e.g., "specializing in serving [ethnic community] clients")
- Do NOT describe neighbourhood specialties using language that implies demographic exclusivity or preferences about buyer composition
- Do NOT use language in marketing that steers buyers or sellers toward or away from neighbourhoods based on protected characteristics
- ALL marketing language — including social media content generated using the Digital You profile — must be screened before distribution

**What IS permitted:**
- Describing the agent's own language abilities: "Mandarin-speaking agent" — permitted
- Describing the agent's own cultural background as a personal attribute, not a client service preference
- Describing neighbourhoods by physical attributes, amenities, transit, zoning, walkability, school programs — not demographic composition

**What is prohibited:**
- Using protected characteristics to limit or qualify which clients the agent serves
- Implying a preference in the buyer or seller pool based on protected characteristics
- Any neighbourhood description that signals demographic composition rather than built environment or amenities

---

### 4. CASL — Digital Marketing Consent Framework

Any commercial electronic messages generated using the Digital You profile (newsletters, market updates, follow-up emails, social campaigns) require CASL consent for each recipient.

**CASL-compliant email templates must include ALL of the following:**
- **Consent mechanism:** how express consent was obtained, or the documented basis for implied consent
- **Sender identification:** agent's full name, brokerage name, and mailing address (CASL s.6(2))
- **Unsubscribe mechanism:** a functional one-click unsubscribe that processes requests within **10 business days** (CASL s.11)

**Do not generate email templates for distribution until the CASL consent framework is documented in the compliance.md file:**

Required elements to document:
- Consent management system: [agent to specify — CRM field, spreadsheet, or other]
- Express consent capture method: [sign-in form with consent checkbox, etc.]
- Implied consent tracking: 6-month window from documented inquiry — flagged at expiry
- Unsubscribe mechanism: [agent to specify] — must process requests within 10 business days (CASL s.11)

**Social media advertising note:**
Real estate content promoted on Instagram, Facebook, and other social platforms may trigger **fair housing obligations** under BCFSA standards and, depending on targeting parameters, may raise issues under BC Human Rights Code s.7. Social media audience targeting that uses demographic filters (age, language, geography in a discriminatory pattern) is a compliance risk. All boosted real estate posts must be screened for s.7 compliance before promotion is activated.

---

### 5. BC PIPA — Voice Samples and Biometric Data

> **HARD PROHIBITION — READ CAREFULLY.**

**Do not upload voice samples to any AI project knowledge base, AI assistant, or AI tool.**

Voice recordings are personal communications data. Under **BC PIPA (SBC 2003 c.63)**:
- Processing personal communications data requires the knowledge and consent of the individual (s.7 PIPA)
- Voice recordings carry **biometric implications** — voice patterns can be used for identity verification and are increasingly treated as biometric data in emerging privacy guidance
- Uploading voice samples to an AI platform (including Claude Projects) for tone, style, or "digital voice" replication constitutes collection and processing of biometric-adjacent personal data

**This policy applies regardless of whether the recordings are of the agent themselves.** The agent uploading their own voice cannot consent on behalf of any other individual captured in a recording (clients, counterparties, colleagues).

**What to do instead:**
- Capture writing style through text samples (emails, posts, property descriptions the agent has written)
- Use the `voice/phrase_guide.md` and `voice/writing_samples.md` approach — text only
- If the agent wants to document their communication style, written descriptions of tone, cadence, and word choice are fully compliant

---

### 6. BC PIPA and FINTRAC — Client Data Disclosure

The Digital You profile should reference the **BCREA Form #585** (Privacy Notice and Consent Form) as the vehicle for:
- PIPA collection disclosure (BC PIPA SBC 2003 c.63)
- FINTRAC identity verification notice
- AI processing disclosure — if Claude or other AI tools will handle client data, this must be disclosed in the service agreement before any real client data is entered

**Before uploading any real client data to AI tools:** confirm Form #585 has been signed and includes AI processing disclosure. If using a non-BCREA service agreement, confirm it covers these obligations.

---

### 7. Licence Number and Brokerage — Required in All Files

The agent's BCFSA licence number and brokerage name must appear in:
- All advertising and promotional content
- The Project system prompt
- The `brokerage/compliance.md` file

**Required format (BCFSA Rule):** "[Agent Name], REALTOR® | [Brokerage Name] | BCFSA Licence #XXXXXXXX"

**Do not finalize the Digital You profile without confirming these fields are populated.** Distributing advertising content without the brokerage name is a BCFSA compliance violation under ss.40–42.

---

### 8. BCFSA AI Guideline — Licensee Responsibility

The licensee is personally responsible for all AI-generated content they distribute, post, or submit — regardless of whether it was produced by the Digital You system. Every file this skill produces is a draft. The agent reviews and approves before uploading or using.

---

## HARD RULES

1. **NEVER** generate a Digital You profile that includes unverifiable track record claims — always include a fill-in placeholder and agent verification prompt for any statistic (Competition Act 2025 + BCFSA ss.40–42)
2. **NEVER** finalize a marketing persona that describes target clients by a protected characteristic (BC Human Rights Code s.7)
3. **NEVER** generate email templates for distribution without confirming the CASL consent framework is documented — and every template must include sender identification, consent basis notation, and a functional unsubscribe mechanism
4. **NEVER** finalize any profile section without confirming brokerage name and licence number are populated
5. **NEVER** invent facts about the agent — if something is not confirmed, ask or leave a clearly labelled placeholder
6. **NEVER** upload real client data to AI tools without first confirming BCREA Form #585 (or equivalent) has been signed with AI processing disclosure
7. **NEVER** accept, request, or include voice samples in any Digital You file or AI knowledge base upload — BC PIPA voice/biometric prohibition applies
8. **ALWAYS** flag advertising claims that require substantiation verification before use (Competition Act 2025)
9. **ALWAYS** rewrite s.7-prohibited content into compliant form before including it in any output
10. **ALWAYS** screen social media content generated using the Digital You profile for s.7 compliance before any paid promotion or demographic targeting is applied

---

## REFERRAL TRIGGERS

| Scenario | Referral | Authority |
|----------|----------|-----------|
| Agent unsure what advertising claims their brokerage allows | Managing Broker / Compliance Officer review before finalizing profile | BCFSA ss.40–42 |
| Agent wants to include "specializing in investment properties" | Note: investment advice is outside RESA scope; describe transaction types (presale, multi-unit, income property transactions) not financial outcomes | RESA s.30(d) |
| Agent wants to describe foreign buyer market expertise | BC Human Rights Code s.7 check — describe the regulatory landscape (PTT, FBTPA, NRST) not buyer demographics | BC Human Rights Code s.7 |
| Any FINTRAC disclosure question about client data in AI tools | Brokerage Compliance Officer | PCMLTFA |
| Agent wants to use voice recordings for AI style training | Decline — direct to text-only approach; BC PIPA voice/biometric prohibition applies | BC PIPA |
| Agent wants to make "#1 agent" or similar ranking claim | Require documented ranking source, time period, geographic scope, criteria — or remove the claim (Competition Act 2025) | Competition Act 2025 |
| Social media content includes demographic audience targeting | Review for BC Human Rights Code s.7 compliance before activating promotion | BC Human Rights Code s.7 |

---

## THE MINIMUM VIABLE DIGITAL YOU (30-minute version)

Minimum = **three files** + system prompt. Everything else is additive.

### File 1: `voice/about_me.md`
Who you are as an agent — verified, compliant, with your licence number confirmed and all track record claims substantiated.

### File 2: `market/my_farm.md`
Your hyperlocal knowledge — reviewed for BC Human Rights Code s.7 compliance (amenities, transit, built environment — not demographics).

### File 3: `clients/active_clients.md`
Your current book — requiring Form #585 confirmation before any real client data entry.

These three files plus the Project system prompt transform generic AI output into output that sounds like you, knows your market, and helps your actual clients.

---

## THE FULL DIGITAL YOU (built over time)

```
voice/
  about_me.md              ← Start here (Minimum) — BCFSA-verified, Competition Act compliant
  writing_samples.md       ← Emails, posts, newsletters — text only; HRC s.7 reviewed
  phrase_guide.md          ← Words you always use / never use — text only, NO voice samples
  difficult_conversations.md ← How you handle hard moments

market/
  my_farm.md               ← Start here (Minimum) — HRC s.7 reviewed
  neighbourhood_notes/     ← One file per area: amenities, transit, zoning (NOT demographics)
  data_sources.md          ← Where you get your market intel
  recent_comps.md          ← Comparable sales from Paragon — agent verified

clients/
  active_clients.md        ← Start here — Form #585 required before real client data
  past_clients.md          ← Anonymized history, patterns, outcomes
  referral_sources.md      ← Who sends you business and why
  testimonials.md          ← Real words from real clients

transactions/
  deal_history.md          ← Price ranges, types — agent supplies real numbers only
  common_objections.md     ← Objections and how you handle them
  contract_notes.md        ← Contract types you commonly use

brokerage/
  compliance.md            ← Required disclaimer language, CASL consent framework
  licence_info.md          ← Licence number, brokerage name, contact — REQUIRED
```

---

## GUIDED BUILD — QUESTION SETS

Work through one section at a time. After answers, produce the formatted file content.

---

### SECTION 1: Professional Identity → `voice/about_me.md`

> **Let's start with who you are as an agent — and what you can document.**
>
> 1. What's your name, brokerage, and BCFSA licence number?
>    *(Required — licence number must appear in all advertising content)*
> 2. How many years have you been licensed in BC?
> 3. In one or two sentences, what's your value proposition — what do you offer that another agent doesn't?
> 4. What types of properties do you mostly work with? (Condos, detached, new construction, strata, rural, commercial?)
> 5. What neighbourhoods or cities are your main focus?
> 6. What price ranges do you most commonly work in?
> 7. Do you primarily work with buyers, sellers, investors, or a mix?
> 8. What languages do you work in?
> 9. Is there anything you want every AI output to always include?
> 10. Is there anything you never want an AI to say on your behalf?
>
> **Track record — substantiation required (Competition Act 2025 + BCFSA ss.40–42):**
> 11. Do you have any specific track record claims to include (list-to-sale ratio, average DOM, transaction volume, transaction count)?
>     *(Required: state the time period, the data source, and the measurement method — all three required for Competition Act compliance)*
> 12. Do you have any industry awards or rankings to reference?
>     *(Required: state the awarding body, the year, the ranking category, and the criteria)*
> 13. Do you have any designations or certifications (ABR, SRS, SRES, CNE, etc.)?
>     *(List only confirmed, current designations — RESA s.42 prohibits misrepresentation of qualifications)*

**BCFSA compliance check before finalizing this section:**
- Is the brokerage name included? ☐
- Is the BCFSA licence number included? ☐
- Are all track record claims documented with source, time period, and methodology? ☐
- Are all designations listed current and verifiable? ☐
- Does any language describe target clients using a protected characteristic? ☐ (If yes: rewrite required)
- Does any language misrepresent the licensee's qualifications or experience? ☐ (If yes: rewrite required)

**Output format:**

```markdown
# About [Agent Name] — Digital You Profile

## Identity
- **Name:** [full name]
- **Brokerage:** [name], [city]
- **BCFSA Licence:** [number] (REALTOR®)
- **Experience:** [X] years licensed in BC
- **Languages:** [list]
- **Designations:** [list — confirmed, current only]

## Value Proposition
[1–2 sentences in their own words — reviewed for BCFSA advertising compliance and RESA s.42]

## Market Focus
- **Property types:** [list]
- **Neighbourhoods / cities:** [list]
- **Typical price range:** [range]
- **Clients:** [buyers / sellers / investors / mix — no protected characteristic descriptors]

## Track Record
[Agent-supplied figures with source, time period, and methodology — Competition Act 2025 compliant]
[If not provided: "To be populated — agent must supply verified figures with source, time period, and measurement method before use in any advertising"]

## Voice Rules
**Always include:** [list — must include brokerage name and licence number in all advertising]
**Never say:** [list]

## Brokerage Disclaimer
[INSERT BROKERAGE DISCLAIMER — required by BCFSA ss.40–42]
[INSERT BCFSA LICENCE NUMBER — required in all advertising content]
```

---

### SECTION 2: Communication Style → `voice/writing_samples.md` + `voice/phrase_guide.md`

> **Now let's capture your voice — through writing only.**
>
> 1. How would you describe your communication style? (Formal / conversational / data-heavy / relationship-first / direct / warm?)
> 2. Can you paste 2–3 emails or social posts you've written that feel "most like you"?
> 3. Are there specific phrases you find yourself using often?
> 4. Are there phrases or tones you actively avoid?
> 5. How do you handle delivering bad news to a client?
> 6. How do you handle really good news?

> ⚠ **Voice samples:** Do not upload audio or video recordings. **Text samples only.** Voice recordings have biometric implications under BC PIPA and are prohibited from upload to any AI knowledge base.

**BC Human Rights Code s.7 review:** All writing samples and phrase guides will be reviewed before upload. Any s.7-prohibited language will be rewritten into compliant form.

**Output format:**

`voice/writing_samples.md` — paste their text examples with a one-line label for each.

`voice/phrase_guide.md`:
```markdown
# Phrase Guide — [Agent Name]

## Phrases I use (encourage Claude to echo these)
- "[phrase]"

## Phrases I avoid (Claude should not use these)
- "[phrase]"

## Tone notes
- Overall style: [formal / conversational / etc.]
- With buyers: [note]
- With sellers: [note]
- Delivering difficult news: [brief description]

## BC Compliance Notes
- Human Rights Code s.7 reviewed: ☐
- Prohibited language removed or rewritten: ☐
- Voice samples: TEXT ONLY — no audio or video files uploaded
```

---

### SECTION 3: Farm Area and Market Knowledge → `market/my_farm.md`

> **Let's document your market knowledge.**
>
> 1. Which neighbourhoods do you know really well? List them.
> 2. For each one, what are 3–5 things a buyer or seller should know that a general market report wouldn't tell them?
>    *(Describe: transit, amenities, development plans, school programs, building quality patterns, zoning — NOT demographic composition)*
> 3. What's currently happening in your market that you're watching?
> 4. Where do you get your market data?
> 5. What do you wish buyers knew before they started looking?
> 6. What do you wish sellers knew before they listed?

**BC Human Rights Code s.7 review:** All hyperlocal knowledge will be reviewed before formatting. Demographic or national origin descriptions of neighbourhood buyer pools or character will be rewritten into compliant form (describing physical attributes, amenities, transit, zoning, and lifestyle stage instead).

**Social media use:** If this neighbourhood content will be used in social media posts or paid promotion, it must be screened for s.7 compliance before any audience targeting is applied. Geographic targeting combined with demographic filters can create a discriminatory pattern even if the content itself is neutral.

**Output format:**

```markdown
# My Farm Area — [Agent Name]
BC Human Rights Code s.7 reviewed: ☐

## Primary neighbourhoods
[list]

## Neighbourhood notes

### [Neighbourhood 1]
- [Physical attribute / amenity point — specific and named]
- [Transit / walkability point]
- [Development / zoning observation — labelled "agent-observed, confirm with city planning"]

### [Neighbourhood 2]
[repeat]

## What I'm watching right now
[current observations — dated]

## Data sources I trust
- [source and what it's good for]

## What I tell buyers before they start
[their words]

## What I tell sellers before they list
[their words]
```

---

### SECTION 4: Active Clients → `clients/active_clients.md`

**BC PIPA + FINTRAC gate — REQUIRED before entering any real client data:**

> Before entering any real client information:
> - [ ] BCREA Form #585 (Privacy Notice and Consent Form) signed by this client — includes AI processing disclosure
> - [ ] FINTRAC identity verification completed for this client (required before entering any transaction)
> - [ ] If AI platform is hosted outside BC (e.g. US-based servers): cross-border data transfer disclosed in Form #585

> **Demo mode:** If using a fictional buyer (e.g., Marcus Chen from ARC Pro), skip this gate. Demo clients contain no real personal data.

> For each active client, provide:
> 1. First name (or pseudonym)
> 2. What they're trying to do (buy / sell / both)
> 3. Current stage
> 4. Key criteria (budget, area, property type, timeline)
> 5. Anything specific Claude needs to know to serve them well

**Output format (one entry per client):**

```markdown
# Active Clients — [Agent Name]
*Last updated: [date]*

---

## [Client first name or alias]
- **Goal:** [buy / sell / invest]
- **Stage:** [current stage]
- **Criteria:** [budget, area, type, timeline]
- **Notes:** [what Claude needs to know]
- **FINTRAC:** ✓ [method · date] / ⚠ NOT YET COMPLETED
- **PIPA Form #585:** ✓ [date · AI disclosure confirmed] / ⚠ NOT YET SIGNED
- **CASL consent:** [express / implied from: date / not confirmed]
- **Agency:** [buyer agency / seller agency — service agreement date]
- **LOTA flag:** [N/A — personal name / FLAG — corporate/trust structure — refer to solicitor]

---
```

---

### SECTION 5: Transaction History → `transactions/deal_history.md`

*(Optional for the Minimum Viable version — build over time)*

> 1. How many transactions have you completed in the last 3 years?
> 2. What was the typical price range?
> 3. Which neighbourhoods came up most often?
> 4. Were you mostly buy side, sell side, or even split?
> 5. What objections do you hear most often? What's your response?
> 6. Any particularly complex deals that shaped how you work?

All track record statistics included in this file must be verified before use in any advertising or client-facing content. The Competition Act 2025 private right of action applies to any published claims — this file is the source record; verify before exporting to advertising copy.

---

### SECTION 6: Brokerage and Compliance → `brokerage/compliance.md`

> **The compliance layer that protects you.**
>
> 1. What is your brokerage's required disclaimer for advertising and client communications?
> 2. What must always appear in any written content distributed under your name?
> 3. Are there specific topics your brokerage has told you to avoid in AI-generated content?
> 4. Do you have a standard email signature?
> 5. What is your CASL consent management system?
> 6. Has BCREA Form #585 been integrated into your client intake process?

**Output format:**

```markdown
# Compliance and Brokerage Details — [Agent Name]

## Required disclaimer (all advertising and client communications)
[paste brokerage disclaimer verbatim]

## BCFSA Advertising Requirements
- Brokerage name: [name] — appears in all advertising ✓
- BCFSA Licence number: [number] — appears in all advertising ✓
- Standard format: "[Name], REALTOR® | [Brokerage] | BCFSA Licence #[number]"

## CASL Consent Management
- Consent management system: [agent specifies]
- Express consent capture: [method]
- Implied consent tracking: 6-month window from documented inquiry
- Unsubscribe mechanism: [agent specifies] — processes within 10 business days
- Email template requirements: sender identification + consent basis + unsubscribe in every message

## Social Media Advertising
- All promoted/boosted posts screened for BC Human Rights Code s.7 before activation: ☐
- Demographic targeting filters reviewed for discriminatory pattern risk: ☐
- Real estate advertising on Meta/Instagram — fair housing framing applied: ☐

## Client Data and AI Disclosure
- BCREA Form #585 in client intake: [YES / NO — required before real client data in AI tools]
- AI processing disclosed in Form #585: [YES / NO]
- Cross-border transfer disclosed (US-based AI platforms): [YES / NO]

## Voice Sample Policy
- Audio/video samples uploaded to AI knowledge base: PROHIBITED (BC PIPA — biometric risk)
- Style capture method: text samples only (writing_samples.md, phrase_guide.md)

## Topics to avoid in AI-generated content
- [any brokerage-specific restrictions]
- Investment advice (outside RESA scope — refer to licensed financial advisor)
- Forward-looking price guarantees or price appreciation projections

## Standard email signature
[paste]
```

---

## PROJECT SYSTEM PROMPT

Once all files are uploaded, help the agent write their Claude Project system prompt:

```
You are my AI assistant for real estate work. I am [name], a REALTOR® with
[brokerage] in [city], BC. BCFSA Licence #[number].

Everything in this Project — my voice files, market notes, and client records —
is the context you should draw on. When I ask you to write something, sound like
me. When I ask about a neighbourhood, use my market notes. When I reference a
client, check my client files first.

MANDATORY RULES:
- Canadian English in all output
- Every piece of content for distribution is a draft only — flag it clearly
- Always include my brokerage disclaimer when the output is client-facing
- Always include my BCFSA licence number in any advertising content
- Never make up MLS numbers, statistics, or comparables — if you don't have
  the data, say so and ask
- Never make forward-looking price guarantees or use prohibited superlatives
- Never describe neighbourhoods or buyers using demographic or national origin
  language — BC Human Rights Code s.7 applies to all content I distribute
- Never give tax, legal, or investment advice — flag and refer
- For any email campaign: CASL consent must be confirmed before sending; every
  template must include sender identification, consent basis, and unsubscribe
- Never include unverifiable track record claims — flag for my verification first
  (Competition Act 2025 substantiation requirement)
- Never include or request voice recordings — text-only style files only (BC PIPA)
- I am personally responsible for all content I distribute

My licence number: [number]
My brokerage: [name]
My brokerage disclaimer: [paste]
```

---

## COMPLETION CHECKLIST

| File | Created? | Compliance reviewed? | Uploaded to Project? |
|------|----------|---------------------|----------------------|
| `voice/about_me.md` | ☐ | ☐ BCFSA advertising + HRC s.7 + Competition Act 2025 track record substantiation | ☐ |
| `market/my_farm.md` | ☐ | ☐ HRC s.7 reviewed; social media use screened | ☐ |
| `clients/active_clients.md` | ☐ | ☐ Form #585 confirmed; no voice samples | ☐ |
| `brokerage/compliance.md` | ☐ | ☐ Licence # + CASL framework + social media screening + voice sample prohibition | ☐ |
| Project system prompt | ☐ | ☐ All mandatory rules included | ☐ |

**Minimum Viable Digital You complete** when all rows are checked. ✓

---

## Output Disclaimer

```
⚠ DRAFT — Review required before uploading or distributing.
All content produced by this skill is a draft for the licensee's review.

Track record claims must be verified against source records before use.
Competition Act 2025: unsubstantiated performance claims carry a private right of
action. Every statistic needs source, time period, and measurement method documented.

Content reviewed for BC Human Rights Code s.7 compliance — agent to confirm before
distribution. Social media content must be re-screened before paid promotion is activated.

CASL: every email template must include sender identification (name, brokerage, mailing
address), documented consent basis, and a functional unsubscribe mechanism before sending.

BCFSA advertising standards (ss.40–42, BC Reg 209/2021) and RESA s.42 (qualifications)
apply to all content. Brokerage name and licence number must appear in all advertising.

VOICE SAMPLES: Do not upload audio or video recordings to this Project or any AI tool.
BC PIPA and biometric data risk apply. Text-only style files are the compliant alternative.

The licensee is personally responsible for all distributed content — AI-generated or otherwise.
[INSERT BROKERAGE DISCLAIMER — BCFSA ss.40–42]
[INSERT BCFSA LICENCE NUMBER — required in all advertising]
```

---

## Regulatory Sources

| Authority | Document | URL |
|-----------|----------|-----|
| BCFSA | Real Estate Services Act (RESA) ss.40–42 | https://www.bcfsa.ca/industry-resources/real-estate-professional-resources/industry-resources/legislation |
| BC Laws | Real Estate Services Rules (BC Reg 209/2021) | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/209_2021 |
| BC Laws | BC Human Rights Code s.7 | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96210_01 |
| Canada | Competition Act (amended June 20, 2025) | https://laws-lois.justice.gc.ca/eng/acts/C-34/ |
| CRTC | CASL Compliance | https://crtc.gc.ca/eng/internet/anti.htm |
| OIPC BC | BC PIPA | https://www.oipc.bc.ca/legislation/personal-information-protection-act |
| FINTRAC | PCMLTFA Compliance Guidance | https://fintrac-canafe.canada.ca/guidance-directives/overview-apercu/Guide-eng |
| BCFSA | AI Guideline (2024) | https://www.bcfsa.ca/industry-resources/real-estate-professional-resources/guidance/ai-guideline |
