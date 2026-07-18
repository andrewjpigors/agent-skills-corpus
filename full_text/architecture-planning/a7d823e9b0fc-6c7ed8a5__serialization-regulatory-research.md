---
name: serialization-regulatory-research
description: >
  Research serialization and track & trace (T&T) regulatory requirements for a specific country
  and produce a structured, implementation-ready summary. Use this skill whenever the user asks
  about: serialization obligations, unique identifier/barcode requirements, T&T system setup,
  national repository registration, anti-counterfeiting or tamper-evident requirements,
  point-of-dispensing verification, aggregation, implementation timelines, serialization fees,
  or non-compliance penalties — for any product category in any country. Covers pharmaceutical,
  veterinary, medical device, cosmetic, food supplement, and other regulated categories.
  Trigger for: "serialization requirements in [country]", "track and trace for [product] in
  [country]", "do I need to serialize for [country]", "Tatmeen/EMVS/DSCSA/MDLP requirements",
  "barcode requirements for [country]", "national repository [country]". Always apply the full
  workflow even if the user asks about only one layer (e.g., just barcoding or timelines).
---


# Serialization & Track and Trace Regulatory Research Skill

## Purpose
Produce a structured, implementation-ready summary of serialization and track & trace (T&T)
obligations for a given country and product category. The output supports:
- **Go/no-go market entry decisions** — is serialization required? What does it cost?
- **Implementation planning** — what systems, processes, and registrations are needed?
- **Compliance auditing** — are existing setups meeting every layer of the requirement?
- **Supply chain role clarity** — obligations differ at every node (MAH, manufacturer,
  importer, wholesaler, dispenser); the output covers all roles that bear obligations.

Serialization requirements are binary in the first instance — either a country has a
requirement or it does not. The skill establishes this fact first, then researches every
technical and operational layer that follows.

---

## Product Category Scope

This skill covers all regulated product categories subject to serialization / T&T obligations.
Identifying the correct category is critical — within the same country, pharmaceutical products
may be fully serialized while medical devices or cosmetics face no requirement, or vice versa.

| Category | Examples |
|----------|---------|
| **Pharmaceutical — Prescription (Rx)** | Branded, generic, biosimilar prescription medicines |
| **Pharmaceutical — OTC / Non-prescription** | Over-the-counter drugs, self-medication products |
| **Biological / Advanced Therapy** | Blood products, vaccines, cell/gene therapies |
| **Medical Device** | Class I–III devices, IVDs, combination products |
| **Veterinary Medicine** | Prescription and OTC veterinary drugs, vaccines |
| **Controlled Substances / Narcotics** | Opioids, psychotropics, Schedule II–V equivalents |
| **Cosmetics** | Skincare, makeup, personal care products |
| **Food Supplements / Nutraceuticals** | Vitamins, minerals, botanicals |
| **Medicated / Functional Food** | Fortified foods, medical nutrition |
| **Other** | Capture in user's own words |

---

## Workflow

### Step 1 — Clarify Inputs (ask the user; never assume)

Confirm the following in a single prompt before researching. Product category is required —
it determines whether any obligation exists at all.

**Required:**
- **Country / target market**
- **Product category** — which of the above? If the user has not specified, ask explicitly
  before proceeding. Do not assume pharmaceutical. Different categories may face entirely
  different requirements (or none) under the same national framework.
- **Supply chain role(s) the user occupies** — obligations differ at each node:
  - **MAH / Marketing Authorization Holder** — responsible for placing product on market
  - **Manufacturer** — physically serializes the pack at production line
  - **Importer / parallel importer** — brings product into the country
  - **Wholesaler / distributor** — moves product through the supply chain
  - **Dispenser** — pharmacy, hospital, or clinic performing point-of-care verification
  - **Multiple roles** — describe which combination
- **Serialization status of this product today:**
  - Already serialized for another market (EU FMD, US DSCSA, EAEU MDLP, GCC Tatmeen/Salama)?
  - Not yet serialized anywhere — greenfield implementation
  - Partially serialized (some markets only)

**Helpful (ask; proceed with best assumptions if not provided):**
- **Stage / objective:**
  - New market entry — assessing obligations before launch
  - Existing market — compliance audit or gap assessment
  - Implementation planning — need technical + operational detail
  - Feasibility / cost estimate only — for business case
- **Product count / portfolio size** — relevant for fee estimation at volume

---

### Step 2 — Establish Whether a Requirement Exists (Binary Gate)

Before researching any technical detail, determine:

**Is serialization / T&T legally required for this product category in this country?**

Search specifically:
- `"[country] [product category] serialization requirement [current year]"`
- `"[country] track and trace [product category] mandatory regulation"`
- `"[country] unique identifier barcode [product category] law"`

**Three possible outcomes — handle each differently:**

**A) Requirement is LIVE and enforced:**
Proceed to research all sections in Step 3. Note the enforcement start date and any
products still in a grace period.

**B) Requirement is PUBLISHED but not yet enforced / in transition:**
Flag prominently at the top of the report:
> ⚠️ **Requirement status: Enacted but transitional** — [Regulation name] has been published
> and mandates serialization effective [date], but enforcement/phase-in continues until
> [date]. Products placed on market before [date] may be exempt until [grace period end].
Research all sections as if live — companies must prepare now.

**C) No requirement found:**
State clearly:
> ✅ **No serialization / T&T requirement identified** for [product category] in [country]
> as of [research date]. Note: regulations in this area are evolving rapidly globally.
> Recommend re-checking annually or when market conditions change.
Then note whether a requirement is known to be under development or consultation,
and which regional framework (EU FMD, GCC, EAEU, WHO) the country is aligning toward
if any evidence exists. Do not apply a proxy framework — serialization is a binary
legal obligation, not a guideline to follow by inference.

---

### Step 3 — Research Each Section

Use `web_search` and `web_fetch`. **Always include the current year in time-sensitive queries**
to capture the latest enforcement dates, phase-in schedules, and fee schedules. Track every
source URL and its last-updated date for the References section.

**Source priority rules:**
- **Requirements and technical standards:** Official authority sources, legislation, and
  published guidance first. GS1 standards documentation for technical specs.
- **Fees, system setup costs, implementation timelines:** Official sources first; reputable
  industry / consultancy sources permitted if official sources are silent — label
  `[Unofficial source: name]`.
- **Recency:** Prefer pages updated within the last 18–24 months. Flag older pages.
- **Never fabricate.** If no source found: *"Not publicly available — recommend direct
  inquiry with [Authority Name]."*

---

#### Section 1: Regulatory Framework & Legal Basis

- **Full name of the competent authority** responsible for serialization / T&T oversight
- **Primary legislation** — law/decree/regulation number and year; link to official text
- **Scope of the regulation:**
  - Which product categories are covered?
  - Which pack types / presentation forms (unit of use, hospital pack, sample, export)?
  - Any products explicitly exempted (e.g., OTC exempted while Rx is mandatory;
    radiopharmaceuticals; products below a certain pack size)?
- **National T&T system / repository:**
  - Name of the national system (e.g., Tatmeen, Salama, EMVS, MDLP/Chestny Znak, SNCM)
  - Operator: government-run, industry body, or private third party (name + URL)?
  - Technical connectivity: direct API integration, web portal, batch upload, EPCIS?
- **ICH / GS1 / ISO standards formally adopted** — determines technical spec baseline
- **Regional harmonization:** Is this country part of a regional T&T framework
  (GCC, EAEU, EU/EEA, ASEAN)? If yes, note which common system applies.
- **Recent changes** (last 2–3 years) — flag prominently, especially any deadline extensions,
  scope expansions, or new product categories added

---

#### Section 2: Unique Identifier & Product Coding Requirements

- **Identifier structure** — what data elements must be encoded?
  - GTIN (Global Trade Item Number) — required? Source: GS1 company prefix required?
  - Serial number — required? Length (characters)? Character set (numeric only / alphanumeric)?
    Randomization / uniqueness rules?
  - Batch / lot number — required in identifier?
  - Expiry date — required in identifier? Format (YYMMDD / MMYYYY)?
  - Any country-specific data elements beyond GS1 standard (e.g., national product code,
    customs tariff code, local registration number)?
- **Local product code requirements:**
  - Must the product be assigned a national/local product code by the authority or national
    system in addition to the GTIN?
  - Registration process for local product code (timeline, fee)?
- **Serial number generation:**
  - Company-generated (MAH / manufacturer assigns)?
  - Authority-assigned (national system issues serial numbers)?
  - Third-party system (national repository generates / validates)?
- **Uniqueness scope:**
  - Must serial numbers be unique per GTIN globally, or only within the country?
  - Reuse restriction period (e.g., cannot reuse serial number for X years)?

---

#### Section 3: Barcode & Label Technical Requirements

- **Barcode symbology required:**
  - 2D DataMatrix (GS1 standard — most common globally)?
  - QR code?
  - Linear barcode (GS1-128, ITF-14) — in addition to 2D, or instead?
  - Any country-specific symbology?
- **GS1 Application Identifiers (AIs) required** — list which AIs must be encoded
  (AI 01 = GTIN, AI 21 = serial, AI 10 = batch, AI 17 = expiry, etc.)
- **Placement requirements:**
  - Which pack level: primary (unit), secondary (carton), tertiary (shipper)?
  - Specific position on pack (face, panel, bottom)?
  - Minimum / maximum label area?
- **Print quality standards:**
  - Minimum ISO/IEC 15415 grade required (e.g., grade C / 1.5 minimum)?
  - Verification equipment / process required before batch release?
- **Human-readable interpretation (HRI):**
  - What text must appear adjacent to the barcode in human-readable form?
  - Language requirements for HRI?
- **Ink / substrate requirements:**
  - Any specific contrast, permanence, or substrate standards?
  - Direct printing vs. label requirements?

---

#### Section 4: Serialization Requirements

- **Is item-level serialization mandatory?**
  - Yes / No / Conditional (by product type, Rx vs. OTC, company size, pack type)?
- **Scope clarification:**
  - Does it apply to all presentations or only specific (e.g., hospital packs exempt)?
  - Exported products: must locally-manufactured products for export be serialized?
  - Parallel imports: must parallel importers re-serialize with local data?
- **Serial number commissioning:**
  - At what point must the serial number be activated / commissioned in the national system?
  - At manufacturing? At import? At entry into national distribution?
- **Decommissioning obligations:**
  - When must a serial number be decommissioned (dispensed, returned, destroyed, exported)?
  - Who performs decommissioning at each point?
- **Returned goods / saleable returns:**
  - Can a decommissioned pack be re-commissioned for resale?
  - If yes, what is the verification / re-commissioning process?
- **Samples and promotional material:**
  - Must samples or non-sale units be serialized or carry a "not for sale" designation?

---

#### Section 5: Aggregation Requirements

- **Is aggregation mandatory?** (linking unit pack → intermediate case → shipper pallet)
  - Yes / No / Conditional (by supply chain role or product type)?
- **Required aggregation levels:**
  - Pack → case (L2)?
  - Case → pallet (L3)?
  - Pallet → higher (L4 / L5, e.g., for cold chain or controlled substances)?
- **Aggregation identifier:**
  - GS1 SSCC (Serial Shipping Container Code) required for cases/pallets?
  - Local aggregation identifier instead?
- **Who must perform aggregation:**
  - Manufacturer only?
  - Importer / repackager also obligated?
  - Wholesaler required to maintain / update aggregation data?
- **Aggregation data transmission:**
  - Must aggregation data be uploaded to the national repository?
  - Format: GS1 EPCIS events? Proprietary XML? Batch file?
  - Timing: real-time, within X hours of dispatch?

---

#### Section 6: Track & Trace — Supply Chain Obligations by Role

Research and state obligations **per supply chain role**. Use a table to summarise,
then provide role-specific detail below.

**Summary table:**

| Role | Serialization Obligation | Aggregation Obligation | T&T Events to Report | System Registration Required? |
|------|------------------------|----------------------|---------------------|-------------------------------|
| MAH | | | | |
| Manufacturer | | | | |
| Importer | | | | |
| Wholesaler / Distributor | | | | |
| Dispenser (Pharmacy / Hospital) | | | | |

**For each role with obligations, detail:**

**Events to be reported to the national T&T system:**
Common events (verify which apply locally):
- Commissioning (activation of serial number)
- Shipping / dispatch (transfer of ownership or custody)
- Receiving / acceptance (confirmation of receipt)
- Verification (check of pack authenticity / status)
- Dispensing / sale to patient
- Decommissioning (product removed from supply chain)
- Returns processing
- Destruction / write-off

**Timing of event reporting:**
- Real-time (at point of event)?
- Within X hours / days of event?
- Batch reporting (daily / weekly)?

**System connectivity:**
- Direct API / EDI connection to national repository required?
- Web portal manual entry accepted (for small volumes)?
- Third-party T&T service provider / LSP connectivity accepted?

---

#### Section 7: Verification & Authentication at Point of Dispensing

- **Is point-of-dispensing verification mandatory?**
  - For all products or specific categories (Rx only, controlled substances)?
  - At pharmacy? Hospital? Both?
- **Verification process:**
  - Scan the 2D barcode — check against national repository for authenticity and status?
  - What is verified: product identity, non-decommissioned status, non-recalled status?
  - Alert if product is unknown, already dispensed, or flagged as suspicious?
- **Decommissioning at dispense:**
  - Must the dispenser decommission the pack in the national system at point of sale?
  - Or does decommissioning happen automatically upon scanning?
- **Equipment obligations:**
  - Must dispensers use approved / certified scanning hardware?
  - Software certification requirements?
- **Offline / connectivity failure:**
  - What is the dispenser's obligation if national system is unavailable?
  - Permitted to dispense and report retrospectively?

---

#### Section 8: National Repository / Database

- **System name and operator:**
  - Government-run, industry association, or private operator?
  - Name, operator entity, official URL
- **Registration requirement:**
  - Must MAHs, manufacturers, importers, wholesalers, dispensers each register separately?
  - Registration process: online, paper, via authority, via system operator?
  - Timeline for registration approval (working days)?
  - Registration fee (see Section 11)
- **Technical connectivity:**
  - API / web service integration: what protocol (REST, SOAP, GS1 EPCIS over AS2/AS4)?
  - Data format: GS1 EPCIS XML, proprietary XML, CSV, other?
  - Accreditation / certification of the connection or solution required?
- **Data retention:**
  - How long must T&T data be retained (in national system and by MAH/company)?
- **Cross-border / interoperability:**
  - Only include this sub-section if research reveals an explicit cross-border or mutual
    recognition framework for T&T data (e.g., GCC cross-recognition, EAEU shared MDLP).
  - State explicitly whether data submitted to another country's system (EU EMVS, EAEU MDLP)
    satisfies any local obligation.

---

#### Section 9: Anti-Counterfeiting & Tamper-Evident Features

Note: these are physical packaging requirements distinct from serialization data. Research both.

- **Tamper-evident seal / closure:**
  - Mandatory? Type specified (breakable seal, shrink sleeve, perforated label, induction seal)?
  - Applies to which product categories / pack types?
  - Standard referenced (ISO, national standard)?
- **Overt anti-counterfeiting features:**
  - Hologram, colour-shifting ink, fluorescent printing, security thread?
  - Authority-issued security features (e.g., official tax stamp, authority hologram)?
  - Required in addition to or instead of serialization for specific product types?
- **Covert anti-counterfeiting features:**
  - Any requirement for covert markers (forensic markers, DNA taggants)?
- **Brand owner vs. authority responsibility:**
  - Who specifies the anti-counterfeiting feature (brand owner's choice vs. authority mandate)?
- **Verification by authorities:**
  - Are anti-counterfeiting features tested or inspected at import / market surveillance?

---

#### Section 10: Implementation Timeline & Phase-in Schedule

This section is critical for new or transitional requirements. Research thoroughly.

- **Regulation publication date** — when was the legislation / guideline officially published?
- **Mandatory compliance date(s):**
  - Is there a single compliance date or a phased rollout?
  - Phase-in by product category (e.g., Rx before OTC)?
  - Phase-in by company size (large MAH / manufacturer first, then SMEs)?
  - Phase-in by supply chain role (manufacturer → wholesaler → dispenser sequentially)?
  - Phase-in by pack type or therapeutic area?
- **Enforcement date** — when does the authority begin penalising non-compliance?
  (May differ from mandatory compliance date)
- **Grace period provisions:**
  - Can products manufactured / imported before the compliance date continue to circulate
    without serialization? Until when?
  - Parallel inventory / sell-through provisions?
- **Products currently exempted or deferred:**
  - Any product categories, pack sizes, or supply chain segments still exempt?
  - Is exemption temporary (with a future compliance date) or permanent?
- **Current status as of research date:**
  Present a clear timeline graphic description, e.g.:
  > [Publication: Month Year] → [Phase 1 compliance: Month Year — Rx products, large MAHs]
  > → [Phase 2 compliance: Month Year — OTC, SMEs] → [Full enforcement: Month Year]

---

#### Section 11: Fees

Research all applicable fees. Use official fee schedules where available; label unofficial
estimates clearly as `[Unofficial source: name]`. Present in local currency and USD.

| Fee Item | Amount (Local Currency) | Amount (USD) | Frequency | Who Pays | Source |
|----------|------------------------|--------------|-----------|----------|--------|
| National system / repository registration | | | One-time | | |
| Product / GTIN registration in national system | | | Per product | | |
| Annual system access / maintenance fee | | | Annual | | |
| Per-transaction / per-event reporting fee | | | Per event | | |
| Software / system certification fee (if required) | | | One-time | | |
| GS1 company prefix (if not already held) | | | Annual | | |
| Authority application / registration fee | | | One-time | | |
| **TOTAL estimated (one-time setup)** | | | | | |
| **TOTAL estimated (annual recurring)** | | | | | |

Note: system implementation costs (ERP/MES integration, serialization hardware at production
line, label verification equipment) are operational costs, not regulatory fees — state this
distinction clearly and flag that these can be significant (typically >[USD range] per
production line) but are outside the scope of this regulatory research.

---

#### Section 12: Penalties & Non-Compliance Consequences

- **Administrative penalties:**
  - Fines — per violation? Per non-compliant pack? Per day? Maximum cap?
  - Amount in local currency and USD equivalent
- **Criminal liability:**
  - Is non-compliance a criminal offence? Who is liable (company, individual, QPPV/RP)?
- **Supply chain block:**
  - Can non-serialized or non-verified products be refused entry, seized, or blocked
    from sale at pharmacy level (system-level enforcement)?
- **Licence / MA consequences:**
  - Can the marketing authorization or import licence be suspended or revoked?
- **Public disclosure:**
  - Are violations published (authority website, public database)?
- **Recall obligations for non-compliant products:**
  - Must non-serialized products already on market be recalled once deadline passes?
- **Enforcement history:**
  - Has the authority issued any public warnings, fines, or enforcement actions to date?
    (Indicates seriousness of enforcement — search `"[country] serialization penalty
    enforcement [current year]"`)

---

### Step 4 — Format the Output

Produce the final report in this structure:

---

## Serialization & Track and Trace Requirements: [Country]
**Product Category:** [as specified]
**Supply Chain Role(s):** [as specified]
**Regulatory Authority:** [Name + official website]
**National T&T System:** [Name + operator + URL]
**Requirement Status:** [LIVE / TRANSITIONAL (effective [date]) / NO REQUIREMENT FOUND]
**Research Date:** [today's date]

---

### 1. Regulatory Framework & Legal Basis
### 2. Unique Identifier & Product Coding Requirements
### 3. Barcode & Label Technical Requirements
### 4. Serialization Requirements
### 5. Aggregation Requirements
### 6. Track & Trace — Supply Chain Obligations by Role
### 7. Verification & Authentication at Point of Dispensing
### 8. National Repository / Database
### 9. Anti-Counterfeiting & Tamper-Evident Features
### 10. Implementation Timeline & Phase-in Schedule
### 11. Fees Summary Table
### 12. Penalties & Non-Compliance
### 13. T&T Obligations Summary Table (see below)
### 14. Business / Implementation Considerations
### 15. Confidence & Caveats
### References

---

#### Section 13: T&T Obligations Summary Table

Produce a single consolidated table for at-a-glance planning:

| Obligation | Required? | Standard / Format | Deadline | System / Portal | Source |
|------------|-----------|------------------|----------|-----------------|--------|
| Unique identifier (GTIN + serial) | | | | | |
| 2D DataMatrix barcode | | | | | |
| Item-level serialization | | | | | |
| Aggregation (pack→case→pallet) | | | | | |
| National repository registration | | | | | |
| Commissioning event reporting | | | | | |
| Shipping event reporting | | | | | |
| Receiving event reporting | | | | | |
| Point-of-dispense verification | | | | | |
| Decommissioning at dispense | | | | | |
| Tamper-evident seal | | | | | |
| Anti-counterfeiting feature | | | | | |

#### Section 14: Business / Implementation Considerations

Concise (4–6 bullet) summary tailored to the stated supply chain role(s):
- Overall implementation complexity for this market (low / moderate / high) and why
- Most operationally demanding obligation (line-level serialization, national system
  integration, dispenser equipment rollout, etc.)
- Any obligation that differs significantly from EU FMD / US DSCSA baseline — flag ⚠️
- For products already serialized for another market: are existing serial numbers /
  barcodes / data elements reusable, or does local re-serialization apply?
- Estimated time to achieve compliance from a standing start (rough range)
- Key cost drivers beyond regulatory fees (production line hardware, IT integration, etc.)

#### Section 15: Confidence & Caveats
- Distinguish confirmed (official source) vs. estimated (unofficial source) data
- Flag any transitional / grace period provision that may affect current compliance status
- Flag any section where data was unavailable and direct inquiry is recommended
- State that serialization regulations evolve rapidly — re-verify before implementation

---

## Role-Based Tailoring (apply throughout)

Each supply chain role has a distinct obligation profile. Focus depth where the user operates:

- **MAH** — ultimately responsible for ensuring all downstream obligations are met; must
  register in national system, commission serial numbers, ensure label compliance, and manage
  product-level T&T data. If MAH ≠ manufacturer, a data flow agreement governs who commissions
  serials and who reports events.

- **Manufacturer** — physically applies barcode to pack; must have serialization-capable
  production line; responsible for print quality, pack commissioning, and aggregation at factory.
  If contract manufacturer (CMO), clarify whether MAH or CMO registers in national system.

- **Importer / parallel importer** — may need to verify incoming serials are valid for the
  market; parallel importers may face re-labelling or re-serialization obligations in some
  markets (especially EU FMD). Customs clearance may be linked to T&T status in some systems.

- **Wholesaler / distributor** — must report shipping and receiving events; maintain aggregation
  data integrity; cannot knowingly distribute non-compliant or non-verified packs. System
  integration with national repository often required for volume operators.

- **Dispenser (pharmacy / hospital)** — must scan at point of dispense; must decommission;
  must report suspicious packs; needs certified scanning hardware and connectivity. Dispenser
  obligations are often the last phase implemented and carry the most operational change impact.

If the user occupies multiple roles, research all relevant obligation sets and note where
they overlap or create dual-compliance requirements.

---

## Regional Reference Tables

### EU / EEA — Falsified Medicines Directive (FMD / EMVS)

| Element | Detail |
|---------|--------|
| **Legislation** | Directive 2011/62/EU (FMD) + Delegated Regulation (EU) 2016/161 |
| **Authority** | EMA (policy); national competent authorities (enforcement) |
| **National system** | European Medicines Verification System (EMVS), operated by EMVO (emvo-asso.com); national verification systems (NVS) in each member state |
| **Scope** | Rx medicines; certain OTC products on positive list; exemptions for hospitals in some MS |
| **Unique identifier** | GTIN + serial + batch + expiry; GS1 DataMatrix 2D |
| **Serialization** | Item-level; serial number company-generated |
| **Aggregation** | Not mandated by FMD but required by some member states |
| **Verification** | At point of dispense by pharmacy; decommission upon dispensing |
| **Anti-counterfeiting** | Tamper-evident closure mandatory on all Rx packs |
| **Repository** | Upload at commissioning; national NVS verify at dispense |
| **Fees** | MAH pays EMVO upload fees + national NVS fees (vary by MS) |
| **Cross-border** | EMVS is shared across EU/EEA; not interoperable with non-EU systems |
| **URL** | emvo-asso.com; ema.europa.eu |

---

### US — Drug Supply Chain Security Act (DSCSA)

| Element | Detail |
|---------|--------|
| **Legislation** | Drug Supply Chain Security Act (DSCSA) 2013; FDA DSCSA guidance |
| **Authority** | FDA (CDER / CBER) |
| **National system** | No single national repository; interoperable exchange between trading partners; FDA DSCSA pilot programs |
| **Scope** | Prescription drugs (finished dosage forms); biologics; excludes: OTC, devices, veterinary |
| **Unique identifier** | Serialized NDC (sNDC); GTIN + serial + lot + expiry; GS1 DataMatrix 2D |
| **Serialization** | Item-level; full enforcement from November 2023 for manufacturers; wholesalers and dispensers phased |
| **Aggregation** | Required for manufacturers and repackagers; GS1 EPCIS standard |
| **Verification** | Saleable returns verification; authorized trading partners only |
| **Anti-counterfeiting** | Tamper-evident packaging required (21 CFR 211.132) |
| **Repository** | No centralized national repository; FDA exploring interoperable system (DSCSA pilot) |
| **Fees** | No government repository fee; GS1 prefix costs apply |
| **URL** | fda.gov/drugs/drug-supply-chain-security-act-dscsa |

---

### EAEU — MDLP / Chestny Znak (Honest Mark)

| Element | Detail |
|---------|--------|
| **Legislation** | Federal Law No. 61-FZ (Russia); EAEU agreements on labelling |
| **Authority** | Roszdravnadzor (Russia — medicines oversight); CRPT (system operator) |
| **National system** | MDLP (Medicine Drug Labeling and Tracking) operated by CRPT (Chestny Znak / chestnyznak.ru) |
| **Scope** | All medicines circulating in Russia mandatory since 2020; Kazakhstan, Belarus, Armenia, Kyrgyzstan at varying stages — verify per country |
| **Unique identifier** | DataMatrix 2D with crypto-protection code (KIZ); GTIN + serial + crypto-key issued by CRPT |
| **Serialization** | Item-level mandatory; CRPT issues / validates the crypto-code — company cannot generate independently |
| **Aggregation** | Mandatory; must reflect in MDLP system |
| **Verification** | At pharmacy; MDLP check via Chestny Znak app or integrated POS |
| **Anti-counterfeiting** | Crypto-protection code is the primary anti-counterfeiting mechanism |
| **Repository** | CRPT MDLP — all events reported in real time; foreign manufacturers must register via local representative |
| **Fees** | Registration with CRPT required; per-code fee applies; pricing published at chestnyznak.ru |
| **Cross-border** | EAEU members moving toward shared system; Russia MDLP data does not satisfy EU/US obligations |
| **URL** | chestnyznak.ru; roszdravnadzor.gov.ru |

---

### GCC — Tatmeen (UAE) & Salama (Saudi Arabia)

**UAE — Tatmeen**

| Element | Detail |
|---------|--------|
| **Legislation** | EDE / MOHAP circulars on track and trace; Federal Decree-Law No. 38 of 2024 |
| **Authority** | EDE (Emirates Drug Establishment) |
| **National system** | Tatmeen (operated by Farasha Healthcare Solutions; tatmeen.ae) |
| **Scope** | Registered human medicines (Rx priority); phased expansion |
| **Unique identifier** | GS1 DataMatrix; GTIN + serial + batch + expiry |
| **Serialization** | Item-level; MAH / importer commissions in Tatmeen |
| **Aggregation** | Required for full T&T; SSCC-based |
| **Verification** | At pharmacy via Tatmeen-connected scan |
| **Repository** | Tatmeen — all supply chain events; registration required for MAH, wholesaler, pharmacy |
| **Fees** | Tatmeen registration and annual fees — verify current schedule at tatmeen.ae |
| **URL** | tatmeen.ae; ede.gov.ae |

**Saudi Arabia — Salama**

| Element | Detail |
|---------|--------|
| **Legislation** | SFDA Drug Track and Trace System regulations |
| **Authority** | SFDA (Saudi Food and Drug Authority) |
| **National system** | Salama (SFDA-operated; salama.sfda.gov.sa) |
| **Scope** | Human medicines; phased by product type and company size |
| **Unique identifier** | GS1 DataMatrix; GTIN + serial + batch + expiry; local product code (SFDA registration number) also required |
| **Serialization** | Item-level; serial number registered in Salama before market entry |
| **Aggregation** | Required |
| **Verification** | At pharmacy / point of dispense |
| **Repository** | Salama — all supply chain events; MAH must register and connect |
| **Fees** | SFDA Salama registration fees — verify current schedule at sfda.gov.sa |
| **URL** | salama.sfda.gov.sa; sfda.gov.sa |

**Other GCC states:** Kuwait, Qatar, Bahrain, Oman are at varying stages of T&T implementation,
often aligned with the GCC Standardization Organization (GSO) framework. Search per country —
do not assume GCC-wide uniformity.

---

### LATAM

| Country | Authority | System | Scope | Status | Key Feature | URL |
|---------|-----------|--------|-------|--------|-------------|-----|
| **Brazil** | ANVISA | SNCM (Sistema Nacional de Controle de Medicamentos) | Rx medicines; phased by therapeutic area and company size | Live; phased rollout per RDC 653/2022 | DataMatrix 2D; GS1 standard; ANVISA issues authorization codes; SNCM upload required | anvisa.gov.br |
| **Mexico** | COFEPRIS | National T&T system (in development) | Rx medicines | Requirement evolving — verify current status | Serialization mandated in concept; implementation guidance developing | gob.mx/cofepris |
| **Colombia** | INVIMA | INVIMA T&T system | Priority medicines (antibiotics, biologics, controlled substances) | Phased rollout underway | DataMatrix; national INVIMA portal reporting | invima.gov.co |

**LATAM-specific notes:**
- Brazil's SNCM requires ANVISA to issue product authorization codes (CNPJ-linked) before
  commissioning — this is not a company-generated serial; allow lead time for registration
- Local language requirements for human-readable information (Spanish / Portuguese)
- Customs integration with T&T status is developing in several LATAM markets — verify
  import clearance implications per country

---

### Africa

| Country | Authority | System / Framework | Status | URL |
|---------|-----------|-------------------|--------|-----|
| **Nigeria** | NAFDAC | mPedigree / SafetyNET+ authentication; NAFDAC e-registration | Overt anti-counterfeiting mandatory (scratch-and-verify); full serialization in development | nafdac.gov.ng |
| **South Africa** | SAHPRA | Serialization framework under development; GS1 alignment | Early stages; monitoring EU/GS1 standards for adoption | sahpra.org.za |
| **Kenya** | PPB / KEBS | Product authentication (mPedigree-aligned); track and trace developing | Authentication system live; full T&T in progress | pharmacyboardkenya.org |
| **Egypt** | EDA | EDA serialization requirements in development | Monitor EDA circulars for implementation dates | edaegypt.gov.eg |

**Africa-specific notes:**
- Mobile-based authentication (SMS scratch-and-verify via mPedigree or similar) is a common
  interim anti-counterfeiting measure in markets without full serialization — may coexist with
  or precede barcode-based systems
- GS1 Africa actively working with national authorities on harmonized adoption; check
  gs1.org/africa for country-level readiness maps

---

### India — CDSCO Track and Trace

| Element | Detail |
|---------|--------|
| **Legislation** | Drugs and Cosmetics Act; Schedule M (GMP); CDSCO barcode notification |
| **Authority** | CDSCO (Central Drugs Standard Control Organization) |
| **Scope** | All drugs manufactured in India; exports have had barcode requirement since 2011; domestic track and trace phased |
| **Unique identifier** | 2D DataMatrix; GS1 preferred; GTIN + batch + expiry + serial (Rx); batch + expiry (OTC) |
| **Serialization** | Item-level serialization for Rx domestic — phased by company size; export serialization long-standing |
| **Aggregation** | Required for exports; domestic: phased |
| **Repository** | National T&T system under development; state-level variation in enforcement |
| **Anti-counterfeiting** | Hologram requirement for certain products (CDSCO-issued hologram stickers for specific categories) |
| **Fees** | CDSCO registration fees; GS1 India prefix fees (gs1india.org) |
| **URL** | cdsco.gov.in; gs1india.org |

---

## Research Quality Standards

- **Official sources first.** Legislation, authority circulars, and national system operator
  documentation are primary. GS1 technical standards are authoritative for barcode specs.
- **Unofficial sources permitted** for fees, implementation timelines, and system integration
  detail when official sources are silent — label `[Unofficial source: name]`. Reputable
  serialization sources: GS1 (gs1.org), RAPS, ISPE GAMP, Rfxcel, TraceLink, Antares Vision,
  Arvato Systems, pharma industry press (PharmaVoice, Fierce Pharma).
- **Track every URL** in the References section, with last-updated dates where visible.
- **Currency conversion.** State the rate and date; verify by search rather than assuming.
- **Recency.** Include the current year in all queries. Implementation deadlines and fee
  schedules change frequently — flag any page older than 18 months.
- **Binary gate is non-negotiable.** Establish whether a requirement exists before researching
  technical detail. Do not research technical specs for a country where no requirement exists.
- **Role specificity.** The summary table and Section 6 must address every supply chain role
  that bears an obligation — not just the MAH.
- **Don't fabricate.** If no source found: *"Not publicly available — recommend direct
  inquiry with [Authority Name] or national system operator."*
- **Cite sources** for every requirement, deadline, and fee figure.

---

## Output Format Notes

- Lead with the **Requirement Status banner** (LIVE / TRANSITIONAL / NO REQUIREMENT FOUND)
  so any reader knows immediately where the country stands
- Use ⚠️ to flag obligations that deviate from GS1 / EU FMD baseline, new deadlines within
  12 months, or enforcement actions already underway
- Use the **T&T Obligations Summary Table** (Section 13) as the at-a-glance anchor for
  business readers
- Use tables for identifier structure, fees, role obligations, and the summary
- Use numbered steps for procedural sequences (e.g., national system registration process)
- Distinguish regulatory fees from operational implementation costs — both matter for
  business cases but must not be conflated
- Keep Business Considerations concise — it is for decision-makers, not technical implementers
- If producing as a document (Word/PDF), use the docx or pdf skill accordingly
