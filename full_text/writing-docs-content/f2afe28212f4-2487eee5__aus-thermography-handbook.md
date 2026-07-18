---
name: aus-thermography-handbook
description: Australian thermography knowledge focused on the electrical-trade intersection — IR camera inspection of switchboards, distribution boards, MCCs, busbars, cable terminations, motors, transformers, solar PV arrays/strings, battery storage, capacitor banks, and EV chargers. Covers physics (emissivity, reflected apparent temperature, NETD, IFOV, D:S ratio), camera classes (LWIR microbolometer vs cooled MWIR), severity classification (ΔT against ambient and against similar-component, NETA MTS / NFPA 70B / IEEE schemes), report conventions, certification (ISO 18436-7 Levels 1/2/3, AINDT, ITC training), insurance-driven inspection programmes (FM Global, IAG, QBE), and the interplay with electrical licensing and AS/NZS 4836 safe-working requirements. Use when writing, editing, or reviewing content about thermal imaging surveys, IR predictive maintenance scans, hotspot reports, infrared switchboard inspections, solar PV thermal surveys, or any electrical thermography context. Activate whenever the work touches IR scanning of energised electrical equipment — service descriptions, careers copy, asset and job-type data, admin UI labels, or technical SEO content.
author: millarelectrics.com.au
---

# Australian Thermography Handbook

Reference for Australian electrical thermography — infrared inspection of energised electrical assets for predictive maintenance and insurance-driven condition monitoring. Scope is deliberately the **intersection of electrical and thermography**: the targets are electrical equipment, the operators are licensed electricians (or work under one), and the language is the trade's. Footnotes mark sections where a full general-scope thermography handbook would expand into building, mechanical, medical, or other domains.

## When to Use This Skill

Activate this skill whenever the work touches infrared / thermal-imaging language for electrical assets, including:

- Writing or editing service pages about thermal imaging, IR inspection, predictive maintenance, hotspot surveys, or condition monitoring
- Drafting careers copy referencing thermography certification or pathways
- Naming variables, fields, or models that mirror IR-survey concepts (e.g. `delta_t_celsius`, `reflected_temp`, `severity_class`)
- Producing technical SEO content ("What is a thermal imaging survey?", "Why does my insurer require IR scanning?")
- Reviewing third-party copy (training providers, equipment vendors, insurance briefs) for technical accuracy
- Drafting admin UI labels or asset/job-type entries that reference IR inspection workflows
- Writing report templates, customer-facing inspection summaries, or quotation copy for IR scopes of work

Default to the precise term in the right capitalisation, with the acronym expanded on first use — rather than a generic synonym.

> **General-scope footnote.** A full thermography handbook would also activate on building envelope surveys (insulation, moisture, air leakage), HVAC/mechanical bearing and bearing-housing scans, refrigeration leak detection, roof moisture mapping, medical/veterinary thermography, refractory and process inspection, civil/structural delamination, and search-and-rescue / firefighting IR. This skill stays inside the electrical perimeter.

## Reference Index

Detailed material lives in [references/](references/). Read on demand:

- [standards-and-procedures.md](references/standards-and-procedures.md) — International and Australian standards relevant to electrical IR inspection, plus survey procedure essentials
- [terminology.md](references/terminology.md) — Physics, camera-spec, and trade-slang glossary
- [severity-and-reporting.md](references/severity-and-reporting.md) — ΔT classification schemes, report-template fields, insurance cycles
- [equipment-and-targets.md](references/equipment-and-targets.md) — What to look for at each electrical asset type, common failure modes
- [practitioner-and-compliance.md](references/practitioner-and-compliance.md) — Certification levels, electrical-licence interplay, safe-working obligations

## Quick Conventions (most important)

- **Thermography** is the discipline; **thermal imaging**, **IR inspection**, **infrared survey** are interchangeable customer-facing terms. **Thermogram** is the resulting image.
- The Australian electrical-thermography spectrum is **LWIR (long-wave infrared, ~7.5–14 µm)** using **uncooled microbolometer** cameras. Cooled MWIR (~3–5 µm) cameras exist but are research/aerospace gear, not switchboard tools.
- There is **no dedicated AS/NZS standard for thermography**. Australian electrical IR surveys reference international standards (ISO 18434, ISO 18436-7, IEC 62446-3) and US-derived severity schemes (NETA MTS, NFPA 70B, IEEE) inside an AS/NZS-compliant safe-work framework (primarily **AS/NZS 4836** for safe working on or near LV).
- A useful IR survey requires the equipment to be **under load** — typical guidance is **at least 40 % of normal operating load** for a meaningful scan; below that, faults stay cool. Always record the load condition with the image.
- **Emissivity** for most painted/oxidised switchgear surfaces is **~0.95**; bare polished copper or aluminium drops below 0.10 and is effectively un-readable without an emissivity tape, paint, or angle change. Treat shiny metal readings as suspect by default.
- **Two ΔT axes matter**, not one: ΔT against ambient air *and* ΔT against a similar component on the same phase or adjacent circuit. Severity classification (see [severity-and-reporting.md](references/severity-and-reporting.md)) uses both.
- Operator certification is **non-statutory in Australia** but commonly required by clients and insurers. The international hierarchy is **Level 1 / Level 2 / Level 3** under **ISO 18436-7** (condition monitoring of machines — thermography); the local certifying body is **AINDT** (Australian Institute for Non-Destructive Testing).
- The act of opening an energised switchboard to perform an IR scan is **electrical work** under state legislation — it requires an unrestricted electrical licence (A-grade in Victoria) or direct supervision by one. A thermographer ticket alone does not authorise switchboard access.

## Common Pitfalls to Avoid

- Do not treat a thermal image as a measurement unless emissivity, reflected apparent temperature, distance, and atmospheric correction have been entered correctly. An uncalibrated reading off a shiny busbar is **qualitative** at best.
- Severity classifications (Level 1–4 / minor / serious / critical) are **not interchangeable between sources**. NETA, NFPA 70B, and IEEE schemes use overlapping but not identical bands. Cite the scheme used.
- A "thermal imaging certificate" or "Level 1 thermographer" qualification does **not** authorise the holder to perform live electrical work. The electrical licence is a separate prerequisite.
- IR-window inspection ports (ClirVu, IRISS, Fluke ClickSafe) **do not eliminate the electrical hazard** — they reduce the access requirement under risk assessment but the work is still on energised gear and AS/NZS 4836 still applies.
- Solar PV cell-level "hotspot" findings sometimes mean a single shaded cell, not a fault. Distinguish **operational shading**, **PID (potential-induced degradation)**, **bypass-diode failure**, and **string-level connector heating** before quoting a remediation.
- Reflected temperature is **not ambient temperature**. In a switchboard with a hot transformer above, the reflected apparent temperature can be 10–20 K above the air temperature and skew measurements on shiny surfaces.
- "FLIR" is a brand (FLIR Systems / Teledyne FLIR), not a generic term — use **thermal camera** or **IR camera** in neutral copy. Other major brands in the AU electrical market: **Fluke**, **Testo**, **HIKMICRO**, **InfraTec**.
- Drone-based aerial PV thermography is a separate discipline with **CASA RPAS** licensing requirements on top of electrical and thermography credentials. Don't conflate ground-based with aerial scope.

## House Style for Public Copy

When writing customer-facing copy (websites, brochures, ads):

- Lead with plain-English value ("find loose connections before they fail", "infrared switchboard scan") and use technical terms in support, not the other way around.
- Quote a **realistic temperature finding** rather than a marketing superlative — "a 45 °C delta over ambient on a main-switch lug" lands harder than "we find serious faults".
- When citing severity classifications, name the scheme: "rated Class 3 against the NETA MTS scale" rather than "rated critical".
- Distinguish residential (rare for thermography — usually only switchboard scans pre-sale or after a fault) from commercial (the bread-and-butter case: annual MSB scans, MCC scans, solar PV string surveys, insurance-mandated cycles).
- Don't imply an insurance discount unless the customer's specific insurer offers one — practices vary by carrier and by site rating.
- Australian English spelling (colour, organisation, metres, fibre). See `aus-business-english` skill.

## Related Skills

- `aus-electrical-handbook` — the broader electrical-trade reference. Most thermography copy needs both: the equipment vocabulary comes from there, the inspection vocabulary comes from here.
- `aus-business-english` — tone and spelling
