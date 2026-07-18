---
name: aus-electrical-handbook
description: Australian electrical industry knowledge base covering AS/NZS standards (3000 Wiring Rules, 3760 test-and-tag, 3008 cables, 4777 inverters, 5139 batteries, 5033 PV, 2293 emergency lighting, 3786 smoke alarms), regulators (ESV, ERAC, Clean Energy Council, NECA, Master Electricians Australia, Standards Australia, AEMO, AER), licensing (A-grade, REC, restricted, apprentice), terminology (RCD, RCBO, MCB, MEN, GPO, COES, CCEW, MSB, DB, switchboard, consumer mains, sub-main), and compliance for residential and commercial electrical work in Australia. Use when writing, editing, or reviewing content about electrical services, projects, switchboards, solar, batteries, EV charging, test and tag, safety switches, smoke alarms, emergency lighting, level 2 ASP, or any Australian electrical trade context.
author: millarelectrics.com.au
---

# Australian Electrical Handbook

Comprehensive reference for Australian residential and commercial electrical industry terminology, governing bodies, specifications, and standards. Tailored for Victoria but covers national context, so Claude can confidently produce accurate copy and code for electrical work anywhere in Australia.

## When to Use This Skill

Activate this skill whenever the work touches electrical-domain language, including:

- Writing or editing service descriptions, project case studies, suburb pages, or any public marketing copy
- Drafting admin UI labels, help text, or content fields for electrical work
- Writing software or data models that touch job types, asset types, certifications, testing, or compliance
- Drafting careers/apprenticeship copy referencing licensing pathways
- Naming variables, fields, or models that mirror real-world electrical concepts
- Producing technical SEO content (e.g. "What is AS/NZS 3000?", "RCD vs RCBO?")
- Reviewing third-party copy (suppliers, partner brochures) for technical accuracy

Default to the precise industry term, in the right capitalisation, with the acronym expanded on first use — rather than a generic synonym.

## Reference Index

Detailed material lives in [references/](references/). Read on demand:

- [standards.md](references/standards.md) — AS/NZS standards relevant to residential and commercial installations
- [regulators-and-bodies.md](references/regulators-and-bodies.md) — Regulators, industry associations, accreditation schemes
- [terminology.md](references/terminology.md) — Acronyms and trade jargon (RCD, MEN, GPO, etc.)
- [licensing-and-compliance.md](references/licensing-and-compliance.md) — Licensing classes by state, COES/CCEW certificates, mandatory testing
- [equipment-and-components.md](references/equipment-and-components.md) — Switchboards, protective devices, cables, accessories

## Quick Conventions (most important)

- AS/NZS standard numbers use a slash, never a hyphen: `AS/NZS 3000`, never `AS-NZS 3000` or `AS NZS 3000`.
- The current Wiring Rules edition is **AS/NZS 3000:2018** (with amendments). Do not refer to older or speculative editions unless certain.
- "Safety switch" is the consumer-facing name for an RCD; technical contexts should use **RCD** or **RCBO**.
- "Switchboard" is the umbrella term; "fuse box" and "meter box" are consumer slang.
- "Electrician" without qualification implies unrestricted licence (A-grade in Victoria). A "restricted electrical worker" is licensed only for specific tasks.
- Voltage classes: **ELV** ≤ 50 V AC / 120 V DC; **LV** up to 1000 V AC / 1500 V DC; **HV** above LV.
- Australian nominal supply: **single-phase 230 V**, **three-phase 400 V** line-to-line, **50 Hz**. (Older "240 V / 415 V" labels are still seen on equipment but the harmonised nominal is 230/400 V.)
- For Victoria, the certificate of compliance is **COES** (Certificate of Electrical Safety) lodged with **Energy Safe Victoria (ESV)**. NSW uses **CCEW**, Queensland uses Form 13/14, SA uses CoC, WA uses eNOC.
- The **REC** (Registered Electrical Contractor) is the _business_ registration in Victoria — not the individual licence.

## Common Pitfalls to Avoid

- Do not refer to AS/NZS 3000 as the "BCA" or "NCC" — those are the National Construction Code (separate document; NCC volumes 1, 2, 3 cover building, plumbing, etc.).
- "Test and tag" is shorthand for **AS/NZS 3760** in-service inspection of portable appliances. It is not the same as **AS/NZS 3017** verification testing performed on a new or altered installation.
- Solar accreditation is via the **Clean Energy Council (CEC)** for installers and retailers. The AER and AEMO are market regulators, not installer accreditors.
- "Level 2 ASP" is a **NSW-specific** Accredited Service Provider concept for service-mains/metering work. Victoria has no direct equivalent — service-side work goes through the local distribution network operator's process.
- Never claim a smoke alarm meets compliance simply because it has a battery. Modern compliance under AS/NZS 3000 §7.8 plus AS 3786 plus the relevant NCC clauses requires hardwired and interconnected alarms in many circumstances.
- The **STC** (Small-scale Technology Certificate) rebate scheme is run via the Clean Energy Regulator under federal _Renewable Energy (Electricity) Act 2000_ — not by the CEC, even though installers must be CEC-accredited to claim it.

## House Style for Public Copy

When writing customer-facing copy (websites, brochures, ads):

- Lead with plain-English terms ("safety switch", "power point", "switchboard upgrade") and use technical terms in support, not the other way around.
- Cite AS/NZS standards by number when relevant for trust, but never as the only reason a service is good.
- Avoid implying claims that require accreditation the business may not hold (e.g. CEC-accredited solar) unless verified.
- Distinguish residential vs commercial language: a homeowner does not have an "MSB"; they have a "main switchboard". A facilities manager will know what "MSB" means.
- Australian English spelling (colour, organisation, metres, kilowatt-hour). See `aus-business-english` skill.

## Related Skills

- `aus-business-english` — tone and spelling
