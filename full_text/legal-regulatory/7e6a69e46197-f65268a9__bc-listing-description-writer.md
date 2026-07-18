---
name: bc-listing-description-writer
description: Property notes to MLS description, Instagram caption, and SMS teaser. BC-compliant. Triggers on "write listing", "MLS description", "listing copy". Full regulatory coverage: Real Estate Services Rules s.59 material latent defect disclosure, LOTA ownership flag, Bill 44 rental restriction repeal, STR bylaw distinction, GVR Rules 3.05/7.02, BC Human Rights Code s.7, BCFSA advertising accuracy (ss.40–42), REDMA presale check, Competition Act s.74.1 (June 20 2025).
---

# BC Listing Description Writer

> **Jurisdiction:** This skill is designed for **licensed BC REALTORS®** operating in **British Columbia**. All regulatory references are BC-specific.

When the agent provides property details, produce three outputs: an MLS description, an Instagram caption, and an SMS teaser — all within the full BC regulatory framework.

---

## What This Skill Does

- Produces MLS Public Remarks (GVR-compliant, ~1,000-char Paragon field limit), Instagram caption, and SMS teaser
- Screens all content for BC Human Rights Code s.7 compliance, BCFSA advertising accuracy, and GVR Rules compliance
- Flags Real Estate Services Rules s.59 material latent defect disclosure obligations
- Flags LOTA if ownership structure is non-personal-name
- Applies the Bill 44 rental restriction repeal — never describes rental restrictions as current
- Applies the Competition Act s.74.1 private right of action (in force June 20, 2025) to all superlatives

---

## ⚖ MANDATORY BC COMPLIANCE SECTION

Run every check below before generating any listing copy. Flag all issues in the header block.

---

### 1. Material Latent Defect Disclosure Gate
**Authority: Real Estate Services Rules s.59 (BC Reg 209/2021)**

> **Correction note for prior users of this skill:** The material latent defect disclosure obligation is governed by **Real Estate Services Rules s.59**, not "RESA s.34." Section 34 of the Rules is the duty to act with reasonable care and skill. Section 59 governs material latent defect disclosure specifically.

**Runs before any listing copy is generated.**

Under Real Estate Services Rules s.59(2), a licensee who knows of a material latent defect must disclose it in writing to all parties before any agreement is signed — even if the seller has not disclosed it. Under s.59(3), if the seller instructs the agent not to disclose, the agent must cease providing trading services.

**Material Latent Defect (MLD) includes** (Rules s.59 + BCFSA guidance):
- A latent defect as defined at common law (dangerous or uninhabitable — not visible on reasonable inspection)
- A defect rendering the property unfit for a purpose the buyer has communicated to the licensee
- A defect that would involve great expense to remedy
- A circumstance for which a local government has issued a notice requiring remedy
- A lack of appropriate municipal building or other permits respecting the real estate
- Active litigation involving the strata corporation
- Outstanding strata bylaw violations on the unit

**Key rule:** Omitting a known MLD from listing copy does NOT discharge the disclosure obligation. If the listing agent has noted any MLD in the input, flag it: *"MATERIAL LATENT DEFECT — Disclosure required under Real Estate Services Rules s.59 before any purchase agreement is signed. Disclosure must be separate from the contract. Verify how to include in supplemental disclosure form — consult managing broker."*

Common law (non-latent) material facts: if the agent is aware of facts that would materially affect a buyer's decision or price (e.g., proposed rezoning, known neighbour disputes, flight path), these must not be omitted from the listing. There is no safe harbour for omission.

---

### 2. LOTA Ownership Flag
**Authority: Land Owner Transparency Act (LOTA)**

If the seller holds the property through a corporation, bare trust, or other non-personal-name structure:
> ⚠️ **LOTA FLAG:** Property appears to be held in a non-personal-name structure. A Transparency Declaration under the Land Owner Transparency Act is required at the Land Title Office at closing. The seller must engage a solicitor before listing to confirm LOTA compliance. This is outside licensee expertise.

Note this flag prominently before generating listing copy.

---

### 3. Bill 44 — Rental Restriction Bylaws REPEALED
**Authority: Building and Strata Statutes Amendment Act (Bill 44), in force November 24, 2022**

Strata Property Act ss.141–145 were repealed. Rental restriction bylaws are legally unenforceable. There are no grandfather provisions.

**Do not describe a strata property as:** "no rentals allowed," "owner-occupied building only," "investment restrictions," or any language implying a current enforceable rental restriction.

If the agent has stated "no rentals" as a feature:
> ⚠️ **BILL 44 FLAG:** Rental restriction bylaws are unenforceable under SPA ss.141–145 as repealed by Bill 44 (in force November 24, 2022). Long-term rental restrictions cannot be described as a current feature of the building. If the agent intended to flag owner-occupied character, this can only be noted if it reflects current voluntary occupancy patterns — it cannot be presented as an enforceable rule.

---

### 4. STR Bylaw Distinction

Short-term rental (Airbnb/VRBO) prohibition bylaws remain enforceable under SPA ss.7.1–7.2 — this is separate from the Bill 44 long-term rental repeal.

If an STR prohibition bylaw exists and the agent is aware of it: this is a material fact for buyers who intend STR use. If the listing copy includes language suggesting STRs are permitted: flag this unless the agent has confirmed no STR prohibition bylaw exists.

---

### 5. New Development / Presale Check
**Authority: Real Estate Development Marketing Act (REDMA), SBC 2004, c.41**

Assess whether the property appears to be a presale or new development unit (phrases like "under construction," "estimated completion," "assignment," developer name as seller, no existing strata lot, unit numbers only).

**REDMA requirements before marketing:**
1. Developer must meet preliminary approval requirements (REDMA ss.4–10)
2. Developer must assure title and services (REDMA ss.11–13)
3. Developer must **file a Disclosure Statement with BCFSA** (REDMA ss.14–17) — marketing may commence immediately after filing, before BCFSA review
4. Disclosure Statement must be provided to each purchaser before entering into an agreement

**April 1, 2025 update:** New disclosure statements filed for presale developments must attach a Summary of Pre-sale Risks and Buyer Rights form (Policy Statement 14).

If it appears to be a presale:
> ⚠️ **PRESALE/REDMA FLAG:** A Disclosure Statement must be filed with BCFSA before any marketing material is distributed. Confirm filing status with the developer. If the DS was filed on or after April 1, 2025, confirm the Pre-sale Risks summary is attached. Using this copy before DS filing is a REDMA violation by the developer; the licensee who distributes unfiled marketing material may also be exposed.

---

### 6. BC Human Rights Code s.7
**Authority: BC Human Rights Code, RSBC 1996, c.210, s.7**

All listing content — including MLS, Instagram, and SMS — is subject to HRC s.7. The Code prohibits any published statement that:
- **(a)** indicates discrimination or an intention to discriminate; **or**
- **(b)** is likely to expose a person or group to hatred or contempt

based on: **Indigenous identity, race, colour, ancestry, place of origin, religion, marital status, family status, physical or mental disability, sex, sexual orientation, gender identity or expression, or age.**

**Intent is NOT required.** The test is whether the publication indicates discrimination or is likely to expose a group to hatred or contempt — not whether the author intended that result.

**Prohibited framing and why:**

| Language | Legal exposure | Safe alternative |
|----------|---------------|-----------------|
| "Steps from [named church/temple/mosque/synagogue]" | Religion — signals proximity to religious institution as a buying factor; can indicate preference for members of that religion | Describe as "walkable to local community spaces" or omit entirely |
| "Great schools / prestigious school catchment" | Ancestry/place of origin, race — "good school" language is well-documented as a proxy for demographic composition of neighbourhoods | Name the school if agent can confirm it; omit if it implies demographic inference |
| "Quiet/established/safe neighbourhood" | Race, ancestry — these descriptors are used historically to signal demographic composition and warn against other groups; context matters | Describe the specific physical attributes: "tree-lined street," "low-density block," "off-arterial location" |
| "Perfect for families / young professionals / couples" | Family status, age, sex — characterises who should buy the property | Describe the physical attributes: "second bedroom ideal for nursery or home office" |
| "Close-knit community / established neighbourhood" | Can imply race or ancestry; signals who already lives there | Describe specific amenities instead |

HRC s.7 applies equally to Instagram captions and SMS teasers as to MLS copy — all are publications.

---

### 7. GVR MLS Field Rules (Rules of Cooperation)

#### 7a. Contact Information — Rule 3.05 (exact text)

> "Contact information including but not limited to names, phone numbers, email addresses and web addresses **may not appear in the Public or Internet Remarks** of a listing."

**Exception:** The Listing Brokerage or Member **may** include a direction to visit the Listing Brokerage's or Member's website to obtain additional information about the listing — but **the nature of such additional information shall not be specified.** (e.g., "visit our website for more info" is permitted; "visit our website for floor plans and virtual tour" is not.)

**REALTOR® Remarks:** The Listing Brokerage's contact information (name, address, phone, fax, email) may appear in REALTOR® Remarks only.

Prohibited in Public and Internet Remarks:
- Agent name, phone, email, social handle
- Brokerage name, phone, email, website (unless as the directed website exception above)
- Seller's name or contact information (unless seller has directed in writing)
- Any other contact information of any kind

#### 7b. Commission — Rule 7.02 (exact text)

> "References to commission or bonuses are restricted to the appropriate commission field and **may not be included in REALTOR®, Public or Internet Remarks**."

This prohibition covers ALL three remarks fields. Commission or bonus incentives belong only in the designated commission field.

#### 7c. Accuracy Obligation — Rule 3.06

> "It is the responsibility of every Member to provide to other Members clear, accurate and factual information concerning any listing by such Member."

The listing brokerage is responsible for checking all listings and amendments after publication to ensure complete accuracy. This obligation is absolute — it is not discharged by hedge language.

**The "buyer to verify" hedge creates exposure, not protection.** Using "buyer to verify" in a listing signals that the agent knows a fact may be unverified. Under Rule 3.06, the listing brokerage remains responsible for accuracy regardless of such language. Under BCFSA Rules s.41, a false or misleading statement that the licensee "reasonably ought to know" is false or misleading is prohibited — adding "buyer to verify" does not change what the licensee reasonably knows. **If a fact cannot be confirmed from a reliable source, omit it.**

---

### 8. Suite Terminology — REIX Case Law + BC Practice

**The only legally safe suite descriptors in BC are: "legal suite" or "unauthorized suite."**

Using any other terminology for a secondary suite has resulted in agent liability in case law:

**Never use:** "mortgage helper," "in-law suite," "mother-in-law suite," "income suite," "income potential," "regulation suite," "easy to suite," "suite potential," "extra income opportunity"

**Why this creates liability:** Courts and REIX (Real Estate Insurance Exchange) case law document that agents who use these terms expect buyers to understand the suite may be illegal, but buyers take the terms at face value. When the suite is later found to be unauthorized, the buyer sues for misrepresentation. In at least one documented REIX claim, an agent used "mother-in-law suite" for an illegal suite; the agent was found liable — and REIX coverage did not apply because the agent had **knowingly misstated the facts.** Knowing misstatement can void professional liability coverage.

**Verification obligation before using "legal suite":** The agent must verify suite legality from building permit records — not from the seller's representations. A seller claiming a suite is "legal" is not verification.

**Unauthorized suite disclosure:** If the suite is unauthorized, disclose it as "unauthorized suite." Buyers and their agents must then investigate independently. This protects the listing agent who accurately disclosed status.

---

### 9. Advertising Accuracy
**Authority: Real Estate Services Rules ss.40–41 (BC Reg 209/2021); Competition Act s.74.1 (in force June 20, 2025)**

#### BCFSA ss.40–41

- **s.40(2):** "In all cases, the licensee name of the brokerage must be displayed in a prominent and easily readable way" in ALL real estate advertising.
  - Full brokerage name as registered with BCFSA — short forms are NOT permitted.
  - Team name must also be displayed if advertising is published by a real estate team.
  - If an address is included, it must be the brokerage address.
  - **Social media (Instagram, Facebook, etc.):** The brokerage name must appear on the licensee's **profile screen** prominently. Each individual post is **not** required to repeat the brokerage name — but the profile must be compliant.

- **s.41:** "A licensee must not publish real estate advertising that the licensee knows, or reasonably ought to know, contains a false or misleading statement or misrepresentation concerning real estate, a trade in real estate or the provision of real estate services."
  - Statements must be current, accurate, and verifiable.
  - Statements are taken at face value based on plain meaning.
  - A disclaimer or "buyer to verify" does not cure a statement the licensee reasonably ought to know is inaccurate.

- **s.42:** Owner consent is required before advertising specific real estate as being offered for sale.

#### Competition Act s.74.1 — Private Right of Action (in force June 20, 2025)

Since June 20, 2025, private parties may apply to the Competition Tribunal for leave to bring proceedings under s.74.1 (civil deceptive marketing practices). Leave is granted if it is in the public interest. Remedies include orders to cease the conduct and monetary awards up to the total amounts paid for the product.

**Real estate advertising is covered.** Unsubstantiated superlatives are representations that may be "false or misleading in a material respect" under s.74.1.

**Compliant practice:** Replace superlatives with verifiable specifics. Do not use:
- "Best neighbourhood in Vancouver" — unverifiable comparative
- "Award-winning" — if used, must identify the award, awarding body, and year
- "Rare opportunity" — only use if a specific scarcity can be substantiated
- "Stunning / breathtaking / spectacular" — describe the specific feature instead

---

### 10. Strata Insurance Disclosure

**Authority: Strata Property Regulation, effective April 1, 2023**

As of April 1, 2023, strata corporations must include a **summary of insurance coverage** in the **Form B: Information Certificate** when requested by owners or purchasers.

**This is a Form B requirement — not a listing copy requirement.** MLS listing copy does not need to include insurance details.

**However:** If the agent is aware of material facts in the strata's insurance picture — for example, exceptionally high deductibles, known coverage gaps, or a strata that cannot obtain market insurance — these facts may constitute a material latent defect or material fact affecting the buyer's decision. In that case, the disclosure obligation under Real Estate Services Rules s.59 and common law applies. The agent should flag this in the output header and consult their managing broker.

---

### 11. Commercial Listings — Different Norms

If the property is commercial (retail, office, industrial, multi-family investment, development land):

- **GVR Rules of Cooperation apply** to GVR commercial MLS listings (same Rules 3.05, 7.02, 3.06).
- **BCFSA advertising rules (ss.40–42) apply** equally.
- **BC Human Rights Code s.7** applies to all publications — discriminatory commercial listing copy can ground a complaint.
- **REDMA** does not apply to commercial property in the same way as residential; commercial property is typically excluded from its developer disclosure regime.
- **Residential property disclosures** (PDS, residential Form B) do not apply; commercial due diligence norms differ significantly.
- **Material latent defect rules** (Rules s.59) still apply to any latent physical defect.
- **Flag for the agent:** Commercial copy should be reviewed for accuracy regarding zoning, FSR, NLA, existing tenancy, and cap rate claims — all are subject to s.41 accuracy requirements. Financial projections in commercial advertising are particularly exposed to Competition Act s.74.1 risk.

---

## HARD RULES

1. **NEVER** describe rental restrictions as a current building feature — repealed by Bill 44 (November 24, 2022)
2. **NEVER** omit a known material latent defect to make the listing read better — Real Estate Services Rules s.59 disclosure obligation is non-negotiable and survives the listing
3. **NEVER** describe suite status as anything other than "legal suite" or "unauthorized suite" — other terminology creates agent liability and can void E&O coverage
4. **NEVER** suggest STRs are permitted without agent confirming no STR prohibition bylaw exists
5. **NEVER** include contact information, agent name, brokerage name, or commission details in Public or Internet Remarks (GVR Rule 3.05, 7.02) — the only exception is directing to the listing brokerage's website without specifying the content
6. **NEVER** use "buyer to verify" hedge language in MLS copy (GVR Rule 3.06, BCFSA Rules s.41) — omit the unverified fact entirely
7. **NEVER** use unsubstantiated superlatives — Competition Act s.74.1 private right of action in force since June 20, 2025
8. **NEVER** include language that violates BC Human Rights Code s.7 — neither in MLS, Instagram, nor SMS
9. **ALWAYS** flag LOTA if the seller appears to hold the property in a non-personal-name structure
10. **ALWAYS** flag the presale/REDMA requirement if the property appears to be new development; confirm April 2025 Pre-sale Risks form if DS filed on or after April 1, 2025
11. **ALWAYS** include brokerage name on the licensee's Instagram profile (not each post, but the profile)
12. **NEVER** cite "RESA s.34" for the material fact disclosure obligation — the correct authority is Real Estate Services Rules s.59

---

## REFERRAL TRIGGERS

| Scenario | Referral | Authority |
|----------|----------|-----------|
| Complex ownership structure (corporation, bare trust) | Solicitor — LOTA Transparency Declaration before listing | Land Owner Transparency Act |
| Suite of uncertain legal status | Building permit records — agent must verify before using "legal suite" descriptor | BCFSA accuracy; REIX case law |
| ALR classification apparent | bc-property-researcher skill + ALC written inquiry + solicitor | ALC Act |
| Strata litigation noted | Legal advice before listing | Real Estate Services Rules s.59; material fact |
| Known material latent defect seller wants concealed | MANDATORY: Real Estate Services Rules s.59(3) — agent must disclose or cease trading services; consult managing broker immediately | Real Estate Services Rules s.59 |
| STR prohibition bylaw existence uncertain | Strata manager — confirm before describing STR use in copy | SPA ss.7.1–7.2 |
| Presale — DS filing status unknown | Developer confirms filing with BCFSA before any marketing | REDMA ss.14–17 |
| Insurance coverage material issues (high deductible, gaps) | Consult managing broker — potential material fact requiring separate disclosure | Real Estate Services Rules s.59; Form B (April 1, 2023) |
| Commercial listing with financial projections | Legal review — Competition Act s.74.1 exposure | Competition Act s.74.1 |

---

## PROHIBITED LANGUAGE REFERENCE

Remove or rewrite any of the following if generated:

| Prohibited | Why prohibited | Compliant Alternative |
|---|---|---|
| "Safe, established neighbourhood" | HRC s.7 — coded language for demographic composition | Name the specific amenity (e.g., "two blocks from Confederation Park") |
| "Quiet/close-knit community" | HRC s.7 — demographic signalling in context | Name specific physical attributes: "off-arterial setting," "low-density block" |
| "Great schools nearby" | HRC s.7 — can imply demographic composition; also unverified | Name the school if agent confirms; omit if intended as demographic signal |
| "Steps from [named religious institution]" | HRC s.7 — indicates religion as a factor | Omit or describe as "walkable to local community spaces" |
| "Best neighbourhood in Vancouver" | Competition Act s.74.1 — unsubstantiated superlative | Name what is objectively nearby and verifiable |
| "Rare find / hidden gem / incredible opportunity" | Competition Act s.74.1 — unsubstantiated superlative | Describe the specific feature that is uncommon or valuable |
| "Stunning / breathtaking / spectacular views" | Competition Act s.74.1 — describe instead | "Unobstructed south-facing mountain and water view from the living room" |
| "Perfect for families / young professionals" | HRC s.7 — family status, age | Describe the physical attributes that support those uses |
| "Investment opportunity / great for investors" | BCFSA s.41 — only if agent provides rental/strata rental permission data; may be misleading without financial substantiation | State the specific rental permission status and relevant figures if available |
| "No rentals allowed" / "owner-occupied only" | Bill 44 — rental restriction bylaws unenforceable | Omit; if owner-occupied, note "currently owner-occupied" (not as a restriction) |
| "Mortgage helper / in-law suite / income suite / income potential / regulation suite" | REIX case law — creates misrepresentation liability; can void E&O coverage | "Legal suite" or "unauthorized suite" only |
| "Buyer/buyer's agent to verify" | GVR Rule 3.06 / BCFSA s.41 — creates exposure, not protection; omit the unverified fact | Omit the unverified fact entirely |
| Agent name, phone, email, social handle in MLS | GVR Rule 3.05 — prohibited in Public/Internet Remarks | Omit entirely; contact info goes in REALTOR® Remarks only |
| Brokerage name in Public/Internet Remarks | GVR Rule 3.05 — prohibited except as directed website link | Move to REALTOR® Remarks; for non-MLS advertising, brokerage name must appear on profile |
| Commission, bonus, or cooperating remuneration reference | GVR Rule 7.02 | Move to the commission field; never in any Remarks field |

---

## Writing Instructions

### 1. MLS Description — Public Remarks

**Character limit:** The GVR Paragon system's Public Remarks field has a platform-set character limit (approximately 1,000 characters). This is a Paragon field limit, not a limit set by the Rules of Cooperation. Target ~950 characters to leave buffer. If Internet Remarks are not submitted separately, the Public Remarks automatically populate the internet description — write for a public audience.

**Format:**
- Feature-led, factual, no superlatives without a specific verified basis
- Include: bedrooms/bathrooms, key finishes, strata fees and parking type (LCP vs. titled — confirm from strata plan), building age or renovation year (if agent-confirmed), neighbourhood access and transit (if confirmed)
- No agent promotional language; no contact information of any kind
- A single direction to the listing brokerage's website is permitted but cannot specify the content ("visit [brokerage website] for more" — not "visit for floor plans")
- End with one clear call to action that does not include contact details
- No HRC s.7-prohibited language

### 2. Instagram Caption

**Note:** Instagram posts are real estate advertising under BCFSA Rules. The agent's brokerage name must appear on their Instagram profile (s.40(2)). Each individual post does not need to repeat the brokerage name, but the profile must be compliant. Content must comply with s.41 accuracy requirements and HRC s.7.

**Format:**
- Under 100 words
- Hook in the first line before the "more" cut
- One or two specific verified details that distinguish this property
- 4–5 local hashtags relevant to the neighbourhood
- No price unless agent specifies to include it
- No contact details in the caption (agent may add their handle separately before posting; the profile is the compliant identifier)
- HRC s.7 applies — same prohibitions as MLS
- Competition Act s.74.1 applies — same superlative prohibition

### 3. SMS to Warm Buyers

**Note:** SMS advertising is real estate advertising under BCFSA. Brokerage identification must be reasonably accessible to the recipient (the agent's profile, prior communications, or an identifier in the message itself). Content must comply with s.41.

**Format:**
- Under 200 characters
- Address, beds/baths, price, one specific hook
- Showing time or "DM me to book"
- Do not include unverified superlatives

---

## Output Format

**Header (generated automatically before listing copy):**

```
MATERIAL LATENT DEFECT CHECK (Rules s.59): [NONE NOTED / ⚠ SEE FLAGS BELOW]
LOTA FLAG: [N/A — personal name / ⚠ Complex structure — solicitor required before listing]
BILL 44: [No rental restriction language in input / ⚠ Rental restriction removed — see flag]
STR BYLAW: [N/A / ⚠ Uncertain — confirm with strata before copy goes live]
PRESALE CHECK: [Not presale / ⚠ PRESALE — REDMA DS confirmation required / ⚠ April 2025 Pre-sale Risks form required]
STRATA INSURANCE: [No material issue noted / ⚠ Insurance issue may require separate material fact disclosure]
HRC s.7 REVIEW: [Reviewed — compliant / ⚠ See rewritten content below]
COMPETITION ACT: [No unsubstantiated superlatives / ⚠ Superlatives removed — see notes]
COMMERCIAL FLAG: [Residential / ⚠ Commercial — different disclosure norms; see Commercial Notes below]
```

**Then the three outputs.**

**Then the disclaimer block.**

---

## Output Disclaimer

```
⚠ DRAFT — Do not submit to MLS or distribute without agent review.
The licensee must verify all factual claims against listing documents before submission.

MATERIAL LATENT DEFECT OBLIGATION (Real Estate Services Rules s.59): Known material latent
defects must be disclosed in writing, separately from the purchase contract, before any
agreement is signed — regardless of whether they appear in this draft. If the seller instructs
non-disclosure, the agent must cease providing trading services (Rules s.59(3)).

MLS Public and Internet Remarks must not contain: contact information, commission details,
or agent/brokerage promotional language (GVR Rules 3.05, 7.02). The single exception: a
direction to the listing brokerage's website is permitted, without specifying content.

"Buyer to verify" language does not discharge the accuracy obligation (GVR Rule 3.06;
BCFSA Rules s.41) — omit unverified facts instead.

Rental restriction bylaws are unenforceable under Bill 44 (SPA ss.141–145 repealed
November 24, 2022). Do not describe as current building features.

BC suite language: "legal suite" or "unauthorized suite" only. No other suite descriptors.
Using "mortgage helper," "in-law suite," or similar terminology can create misrepresentation
liability and void E&O coverage (REIX case law).

All content is subject to BCFSA advertising standards (Real Estate Services Rules ss.40–42),
BC Human Rights Code s.7, and the Competition Act s.74.1 (private right of action in force
June 20, 2025). Unsubstantiated superlatives are now subject to private Competition Tribunal
proceedings — not just regulatory enforcement.

Instagram/social media: brokerage name must appear on the licensee's profile screen
(Real Estate Services Rules s.40(2)). Each post need not repeat it, but the profile must
be compliant. All content must comply with s.41 accuracy and HRC s.7.

[INSERT BROKERAGE DISCLAIMER — Real Estate Services Rules s.40(2): Full registered brokerage
name must appear prominently. Short forms not permitted. If a team name is used, it must
also appear and the brokerage name must remain prominent.]
```

---

## Regulatory Sources

| Authority | Document | Section | URL |
|-----------|----------|---------|-----|
| BC Laws | Real Estate Services Rules (BC Reg 209/2021) | ss.40–42 (advertising); s.59 (material latent defects); s.30 (duties to clients) | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/209_2021 |
| BC Laws | BC Human Rights Code | s.7 (discriminatory publication) | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96210_01 |
| BC Laws | Strata Property Act | ss.141–145 repealed by Bill 44 (Nov 24, 2022); ss.7.1–7.2 (STR bylaws) | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/98043_01 |
| BC Laws | Real Estate Development Marketing Act (REDMA) | ss.14–17 (disclosure statements); Policy Statement 14 (Apr 2025 pre-sale risks form) | https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/04041_01 |
| LTSA | Land Owner Transparency Registry | — | https://ltsa.ca/land-title/land-owner-transparency-registry |
| GVR | Rules of Cooperation | s.3.05 (contact info); s.3.06 (accuracy); s.7.02 (commission) | https://www.gvrealtors.ca/for-realtors/rules-and-policies/ |
| BCFSA | Advertising Information | ss.40–42 guidance | https://www.bcfsa.ca/industry-resources/real-estate-professional-resources/knowledge-base/information/advertising-information |
| BCFSA | Material Latent Defects Information | Rules s.59 | https://www.bcfsa.ca/industry-resources/real-estate-professional-resources/knowledge-base/information/material-latent-defects-information |
| BCFSA | AI Guideline (2024) | — | https://www.bcfsa.ca/industry-resources/real-estate-professional-resources/guidance/ai-guideline |
| BC Gov | Form B: Information Certificate (Apr 1, 2023 update) | Strata insurance summary | https://www2.gov.bc.ca/gov/content/housing-tenancy/strata-housing/renting-buying-selling/buying-and-selling-strata/paperwork-for-buyers-and-sellers/form-b-information-certificate |
| Justice Canada | Competition Act | s.74.1 (deceptive marketing); s.103.1 (private access, in force June 20, 2025) | https://laws.justice.gc.ca/eng/acts/C-34/ |
| REIX | Suite Terminology Guidance | — | https://reix.ca/blog-post/correct-way-of-stating-suites-as-legal-or-illegal/ |

---

## Example Prompt

```
Property: Unit 412 — 7388 Sandborne Ave, Burnaby
2 bed / 2 bath / 847 sqft
2019 build, concrete high-rise
Strata fees: $389/month
1 parking (LCP — confirmed from strata plan), 1 locker
East-facing, morning light
In-suite laundry, open kitchen, 9-ft ceilings
Steps to Edmonds SkyTrain (Expo Line)
List price: $698,000

Seller holds property in personal name. No known material latent defects.
No secondary suite. No strata litigation.
Long-term rental permitted (confirmed post-Bill 44 — no rental restriction bylaw).
STR prohibited by strata bylaw (confirm this to any buyer with STR intent).
Not a presale.
```

**Expected output should demonstrate:**
- Compliance header with all flags showing clean status
- MLS description under ~1,000 chars, no contact info, no superlatives, no HRC-prohibited language
- STR prohibition noted in REALTOR® Remarks (not Public Remarks) or recommended for supplemental disclosure to STR-intent buyers
- Instagram caption with verified specifics, no superlatives, no brokerage name in post body (profile is compliant)
- SMS under 200 chars
- Disclaimer block with Rules s.59 citation (not "RESA s.34")
