---
name: serve-data
description: Convert a planned (or existing-but-undocumented) consumer-facing serving endpoint into a Serving Surface markdown file under docs/serving-surfaces/, enforcing the Stage 5 dual kill-switch — an accepted surface must name at least one upstream Model Plan (the chain half) AND at least one DGQ it informs (the loop-closure half). Use when the user says "/serve-data", "serve this data", "plan this dashboard/API/sync", "document this Looker dashboard", "we're shipping a reverse-ETL sync to Salesforce", "expose this model as an API", "publish this feature view", "who uses this dashboard", "what decision does this dashboard inform", "is anyone actually looking at this report", or describes a serving surface ("we built three dashboards on the same metric", "the exec board reads stale numbers", "marketing wants churn scores in Salesforce", "this dashboard recomputes revenue instead of reading the model") and wants the serving contract — decision served, upstream model read, surface type, consumer, owner, freshness SLA, access posture, sensitivity, retirement trigger — captured before the BI/serving code is written or after it exists but is undocumented. Dashboard, api, reverse-etl, feature-store, export, and embedded surfaces are equally first-class, and streaming and batch serving are equally first-class; the interview branches on the user's answer rather than defaulting to any. Routes to /write-adr when the decision is a platform-wide serving-tool commitment (BI tool, reverse-ETL platform, feature-store technology) rather than a per-surface fact.
---

# /serve-data — Serving Surface interview

This skill runs a short, branching interview that converts a planned (or existing-but-undocumented) consumer-facing serving endpoint into a **Serving Surface** markdown file at `docs/serving-surfaces/<surface>.md` in the consumer's project. It is the terminal stage of the spine — the one where the lineage chain closes back onto the Stage 0 decision that started it. It is an **interview, not a template** — every surface that lands has been pressure-tested against the *dual* Serving kill-switch (a named upstream Model Plan **and** a named DGQ the surface informs), the freshness-honesty test, the access-model-honesty test (`convention` is earned, not `role-based` asserted aspirationally), the sensitivity-step-down test, and the "is this actually an ADR moment?" routing test.

This skill is self-contained: the vocabulary it leans on is inlined just below, the Serving Surface contract it writes against ships beside it at [`references/serving-surface.md`](references/serving-surface.md), and the linter that enforces that contract ships at [`scripts/lint-serving-surface.sh`](scripts/lint-serving-surface.sh). Read the contract for the artefact's frontmatter fields, enum domains, and body section order before writing — do not duplicate it into the interview; reference it.

**Vocabulary this skill assumes** (the minimum it needs; the full worldview is optional deeper reading, linked at the end):

- **Serving Surface.** The data team's version-controlled model of a single consumer-facing serving endpoint — the decision it informs, the upstream model it reads, the surface type, the consumer and named owner, the freshness contract, the access posture, the sensitivity, and the trigger that would retire it. The operational and contractual model of the surface, *not* a serving-tool config and *not* a project-management plan (it contains no LookML, no Tableau workbook XML, no reverse-ETL sync JSON, no API handler code). Stage 5's deliverable — the terminal stage, where the lineage chain closes back onto the Stage 0 decision; one file per surface at `docs/serving-surfaces/<surface>.md`.
- **Serving kill-switch (dual).** Stage 5 is the only stage with a *two-headed* kill-switch, because it both *continues* the lineage chain and *closes the loop*. An accepted Serving Surface must name at least one upstream Model Plan in `related_model_plans` (the chain half — a surface with no governed upstream recomputes business logic from raw/staging, the forked-revenue-definition failure at the serving layer) *and* at least one DGQ it informs in `serves_dgqs` (the loop-closure half — a surface that informs no decision is the dashboard-nobody-uses). Both halves must hold; this is the soul of the skill — see the next section.
- **`access_model` posture.** The Stage-5-distinctive honesty field — how access is *actually* enforced today (`public`, `sso`, `role-based`, `row-level`, or `convention`). `convention` (granted broadly, policed by trust with no technical enforcement) is an honest, accepted answer; recording `role-based` *aspirationally* when nothing is wired up is the template-mode bias this skill refuses, at the last checkpoint before data leaves the team's boundary.

**Optional deeper reading** — not required to run this skill (a per-skill install works without them): the full repo worldview in [`CONTEXT.md`](https://github.com/sleeplessv/relentless-data-skills/blob/main/CONTEXT.md) and the lifecycle reference in [`docs/data-engineering-101.md`](https://github.com/sleeplessv/relentless-data-skills/blob/main/docs/data-engineering-101.md).

A Serving Surface is **not** a serving-tool config and **not** a project-management plan. It contains no LookML, no Tableau workbook XML, no Hightouch sync JSON, no API handler code, no feature-store definition, no dbt `exposure`. It is the operational and contractual model of the surface: the human-authored *commitments* (the decision served, the freshness contract, the access posture, the consumer, the owner, the retirement trigger) that the actual BI/serving/reverse-ETL code should reflect. The code that *implements* those commitments lives in the consumer's BI/serving repo and is out of scope — this skill emits no serving code. The surface is the contract the code should be reviewed against, not a substitute for it. It is the structural analogue of the Model Plan one stage upstream, deliberately human-authored and never inferred from a tool: **no dbt `exposures` parsing, no Looker/Tableau/Mode API introspection, no reverse-ETL-platform query, no dashboard view-count or usage-analytics lookup.**

## Soul of the skill: the dual kill-switch

Stage 5 is the only stage with a **two-headed** kill-switch, because it is the only stage that both *continues* the lineage chain and *closes the loop* back onto the Stage 0 decision. Both halves must hold for an accepted surface; each catches a distinct failure, and a single kill-switch would miss one of them.

**The chain half — Turn 1.** The question:

> **Which Model Plan(s) under `docs/model-plans/` does this surface read from?**

If the user cannot point to at least one accepted-or-draft Model Plan in `related_model_plans`, the surface does not deserve a plan. A surface with no named upstream model is the structural twin of every floating node the chain refuses — and at the serving layer it has a specific, expensive shape: a dashboard or API that **recomputes** business logic from raw/staging instead of reading the model that owns the canonical definition. That is the forked-revenue-definition failure at the last mile — three dashboards, three different revenue numbers, none of them the one the model blessed. A surface reading from a semantic layer, a metrics store, or a BI extract is **not** exempt: it still names the *root* Model Plan(s) its data ultimately derives from. Every surface chains to a governed model eventually.

**The loop-closure half — Turn 2 (the loudest turn).** The question:

> **Which DGQ(s) under `docs/requirements/` does this surface inform — and what does a consumer *do differently* because it exists?**

This is the mirror of Stage 0's `action_change` test, asked at the other end of the pipeline. Stage 0 asks of every incoming ask, *"if the answer flipped, would anything change?"*; Stage 5 asks of every outgoing surface, *"what does a consumer do differently because this surface exists?"* Same question, both ends. A surface that informs no decision is the dashboard-nobody-uses — built because the data was there, not because a decision needed it — and it is retired at Stage 5 exactly as the ask-nobody-acts-on is killed at Stage 0. If the honest answer is *"nothing / it's nice to have / we had the data so we built it"*, that is the kill-switch firing: write the surface with `status: rejected`, record the no-decision rationale in `## Open follow-ups`, and stop. "It gives visibility" / "it informs the business" is the Stage 5 equivalent of `action_change: nothing` dressed up — force a *named* DGQ and a *named* action-change, exactly as Stage 0's interview does.

Do not soften either half. Do not paper over the absence by inventing a plausible-sounding Model Plan path or a plausible decision on the user's behalf. Turns 1 and 2 are the two places in this skill where the user must speak first; a recommendation there would coach them past the very gaps the skill exists to surface.

The linter enforces the structural contract — an `accepted` surface with an empty `related_model_plans` fails the chain half of `scripts/lint-serving-surface.sh`, and an empty `serves_dgqs` fails the loop-closure half, each with its own diagnostic. This skill is the upstream half: it refuses to start the interview without one named upstream Model Plan, and refuses to *accept* a surface that informs no decision.

## Target shape

- **Length.** 7–10 substantive exchanges per surface is typical — comparable to Stage 4 and slightly tighter, because several Stage 5 concerns (surface type, consumer, owner) are crisp single-answer fields, while the depth concentrates in the decision-served turn (Turn 2) and the access-governance turn (Turn 6). Keep going until the decision served, the freshness contract, and the access posture are honestly named — don't truncate to hit the cap, and don't pad to fill it. Sharp, not exhausting.
- **Output.** One markdown file per surface at `docs/serving-surfaces/<surface>.md`. If one serving effort produces a set (a `dashboard` plus the `reverse-etl` sync that operationalises the same metric), write one fully-drilled surface first, the rest queued as `status: draft` so a later run can pick them up.
- **Tone.** Interrogative, not adversarial. The goal is to find the honest contract — including "freshness is best-effort and nobody's watching the gap" and "access is policed by convention" answers — not to make the user feel bad for inheriting an under-governed or stale serving layer.

## Resumability check (run this first)

Before starting a fresh interview, scan `docs/serving-surfaces/` in the consumer's project. If one or more Serving Surface files exist, **pause and ask**:

> I see existing Serving Surfaces in `docs/serving-surfaces/`. Do you want to:
>
> 1. Continue an existing **draft** or **needs-follow-up** surface (resumable)
> 2. Start a **new** surface
> 3. **List** all surfaces and their statuses

Treat `status: accepted`, `status: rejected`, and `status: superseded-by-<path>` files as immutable from this skill's perspective — do not offer to edit them. Superseding an old surface (e.g., a metric rebuilt on a new BI tool) is done by writing a new one and updating the old one's status by hand. If the user picks "continue", load the chosen file and resume from the first unfilled section (commonly the section that corresponds to the next unanswered turn). If they pick "list", print one line per file: `<path> — <status> — <surface> (<surface_type>, consumer: <consumer>)`.

If `docs/serving-surfaces/` does not exist, create it on first write — not before.

## Steps

Carry out the eight turns below in order. **One question per turn**, not a wall of multiple questions, except where the spec explicitly says "combined turn". If the user volunteers material that answers a later turn early, accept it and skip ahead — do not re-ask. Do not deliver multi-paragraph monologues; keep each prompt tight.

Two cross-cutting rules apply to every turn:

- **Recommend before you ask.** For each turn's question, propose a plausible answer first — derived from the named upstream Model Plan(s), the surface name itself, adjacent surfaces/ADRs, or sensible defaults — then ask the user to accept, reject, or refine it. Reacting to a concrete proposal is faster and sharper than generating one cold. If you genuinely have no basis for a recommendation, say so and ask open. Never invent the two kill-switch answers (Turn 1's named upstream Model Plan, Turn 2's named DGQ and action-change) this way — those are the two places the user must speak first. And never inflate the `access_model` (Turn 6) toward `role-based` just because it sounds governed — that default is exactly the template-mode bias this skill exists to refuse.
- **Explore before you ask.** If a turn's question can be answered by looking at the project — existing Model Plans in `docs/model-plans/`, DGQs in `docs/requirements/`, Storage Plans / Ingestion Plans / Source Profiles in their respective directories, ADRs in `docs/adr/`, adjacent Serving Surfaces in `docs/serving-surfaces/`, glossary entries in `CONTEXT.md` — look first, then bring what you found into the turn. In particular, **always read the named upstream Model Plan(s)** once identified in Turn 1; their `## Downstream contract`, `sensitivity`, `grain`, and the canonical definition they own seed Turns 4–6 directly. Do not make the user re-derive what the repo already knows. If a stakeholder term collides with `CONTEXT.md`'s glossary, call it out the moment you notice it.

### Turn 1 — Name the upstream Model Plan(s) (the chain kill-switch)

Ask, verbatim or close:

> Which Model Plan(s) under `docs/model-plans/` does this surface read from? Point me at one or more by filename or by model.

Before asking, scan `docs/model-plans/` and list the available Model Plan files with their `model`/`grain` line and `status` — so the user is choosing from a concrete set, not naming a file from memory. If `docs/model-plans/` is empty or absent, that is itself the answer: there is no governed upstream model; the surface does not deserve a plan yet.

Four branches:

- **One or more named upstream Model Plans.** The user points to one or more files with `status: accepted` or `status: draft`. Record the paths; they go into `related_model_plans`. Read each one before continuing — its `## Downstream contract` (the stable column contract, the canonical definition owned, the freshness expectation, "what Stage 5 must not bypass"), its `sensitivity`, and its `grain` seed the next several turns. Continue to Turn 2.
- **A plan exists but it is `rejected` or `superseded-by-<path>`.** Push back: *"That Model Plan was rejected — what's the live upstream model for this surface?"* / *"That plan was superseded by `<path>` — should we serve from the superseding one instead?"* Do not start the surface against a non-live model path; the upstream link must be a model someone has actually accepted as the contract.
- **A surface reading from a semantic layer / metrics store / BI extract.** The user says "this reads from the metrics layer, not a model directly." That is fine — but the kill-switch still bites: ask which **root** Model Plan(s) the surface's data ultimately derives from, and record those in `related_model_plans`. A surface whose data cannot be traced back to *any* Model Plan is the floating node the kill-switch refuses — and the recompute-from-raw failure in disguise.
- **No Model Plan exists upstream, or the user cannot name one.** **Trigger the chain kill-switch.** Do not write a surface. Tell the user:
  > There's no named upstream Model Plan for this surface. A Serving Surface without a governed upstream recomputes business logic from raw/staging — the forked-revenue-definition failure at the serving layer, three dashboards with three different numbers. I recommend running `/model-data` first to plan the model this surface reads from, then coming back to `/serve-data` once at least one Model Plan under `docs/model-plans/` is in place.

  Then exit cleanly. Do not start drafting a surface "just in case." The chain kill-switch is half the differentiator; surface it without apology.

### Turn 2 — Name the decision served (the loop-closure kill-switch, the loudest turn)

This is the turn where template-mode regression is most likely — the temptation to wave at "it informs the business." The skill is **explicit and slow** here, mirroring Stage 0's `action_change` turn. Ask, in one combined turn (the two halves are inseparable):

> Which DGQ(s) under `docs/requirements/` does this surface inform — and what does a consumer *do differently* because this surface exists? Name the decision and name the action that changes.

Before asking, scan `docs/requirements/` and list the available DGQ files with their question line and `status`, so the user is choosing from a concrete set. Read the named upstream Model Plan(s) from Turn 1 — the DGQ(s) they transitively consume (via Storage → Ingestion → Source Profiles) are strong candidates for what this surface serves.

Two branches:

- **A named DGQ and a named action-change.** The user points to one or more DGQ files *and* states what a consumer does differently — *"the exec board reads this churn dashboard and decides which accounts get a retention call this week"*, *"sales sees the churn score in Salesforce and reprioritises the call list"*. Record the DGQ paths in `serves_dgqs`; the action-change goes into `## Decision & retirement`. Continue to Turn 3.
- **No decision, or "it's nice to have / we had the data / it gives visibility".** **Trigger the loop-closure kill-switch.** This is the dashboard-nobody-uses. Do not accept the surface. Tell the user:
  > This surface informs no decision a consumer acts on — "it gives visibility" is the serving-layer form of `action_change: nothing`. The honest move is to retire it (or not build it). I'll write the surface with `status: rejected` and record the no-decision rationale, so there's a durable record of the deliberate decision not to build.

  Then write the rejected surface (frontmatter with `status: rejected`, `serves_dgqs: []` permitted, the upstream Model Plan(s) from Turn 1 still recorded in `related_model_plans`, all six body sections present, the no-decision rationale in `## Decision & retirement` and `## Open follow-ups`) and stop the interview. Do not drill the remaining turns for a surface that serves nothing.

Force a *named* DGQ and a *named* action-change. "It informs the business", "stakeholders like to see it", "it's a KPI dashboard" are not action-changes — they are the visibility-theatre this turn exists to refuse. If the user can name a real decision but it has no DGQ yet, that is an `## Open follow-ups` item and a `needs-follow-up` status (recommend `/gather-requirements` for the missing DGQ), not an automatic rejection — the decision exists, the artefact for it does not.

### Turn 3 — Identify the surface and its type

Ask:

> What's the surface — a kebab-case `surface` slug — and what type is it: `dashboard`, `api`, `reverse-etl`, `feature-store`, `export`, or `embedded`? Who's the consumer, and who owns it? Is this one surface or several?

Capture four fields:

- **`surface`** — kebab-case slug uniquely naming the surface (`exec-revenue-dashboard`, `churn-scores-to-salesforce`, `customer-360-api`, `marketing-features-view`, `finance-monthly-export`). Aim for a name that reads as "what this surface is and who it's for".
- **`surface_type`** — one of `dashboard | api | reverse-etl | feature-store | export | embedded`. **All six are equally first-class "surfaces".** Do not silently assume "serving means a dashboard". A reverse-ETL sync to Salesforce and an ML feature view are surfaces as much as a BI board is.
- **`consumer`** — who reads it / what consumes it (the exec team, the sales org via Salesforce, the recommendation service, a partner via SFTP export).
- **`owner`** — the named human or team accountable for the surface. **Required**, but may carry the sentinel `unknown` if genuinely not yet assigned — record honestly, with an `## Open follow-ups` item to assign one, rather than inventing a name.

Listen for plural surfaces hiding inside one ask. A serving effort often produces a set: a `dashboard` that shows churn risk to execs **plus** a `reverse-etl` sync that pushes the same churn scores into Salesforce for sales. Each is a separate Serving Surface — they have genuinely different consumers, freshness contracts, access models, and retirement triggers, even when they read the same model.

**Branching rule.** If more than one surface surfaces:

1. Ask the user to pick **one** to drill fully right now.
2. For each of the others, write a stub Serving Surface to `docs/serving-surfaces/<surface>.md` with `status: draft`, frontmatter populated with the upstream Model Plan(s) from Turn 1 in `related_model_plans` and the DGQ(s) from Turn 2 in `serves_dgqs`, the `surface`, `surface_type`, `consumer`, and `owner` identifying the stub, and all other linter-required scalar fields set to safe placeholders (`freshness_sla: best-effort`, `sensitivity: internal`, `access_model: convention`), with a note in `## Open follow-ups` that this surface needs resumption. Body sections present but with TBD bullets, so the linter passes.
3. Tell the user the stubs are saved and this session will drill the chosen surface. Do not abandon them silently.

### Turn 4 — Consumption contract

Ask:

> What does this surface expose — the columns, metrics, or fields the consumer depends on — and what's the stable contract? How does it read the upstream model: does it read the model's blessed output, or does it recompute anything?

Read the named upstream Model Plan's `## Downstream contract` before asking — the stable column contract and the canonical definition it owns seed this turn directly. Capture for the body's `## Consumption contract` section:

- **What the surface exposes, made concrete.** A Looker dashboard / a REST endpoint / a Hightouch reverse-ETL sync to Salesforce / a feature-store view / a scheduled CSV export / an embedded panel — and the columns / metrics / fields the consumer may depend on.
- **The relationship to the Model Plan's downstream contract.** What this surface reads, and the explicit, in-writing commitment that it does **not bypass** the model to recompute the model's logic from raw/staging. This is the Stage 4 → Stage 5 read contract being honoured. If the surface *does* recompute anything the model already owns, surface it as a smell: *"the model owns the `gross_revenue` definition — this dashboard recomputes it from line items, which is exactly the fork the chain kill-switch exists to prevent. Read the model's column instead."* Record, and flag if the recompute was accidental.

### Turn 5 — Freshness & delivery

Ask:

> How fresh must this data be — the `freshness_sla` — and how is it refreshed? What's the latency commitment, and what does the consumer see when freshness is violated?

Capture **`freshness_sla`** (free-text, **required**, e.g. "≤ 5 min", "hourly", "daily by 06:00 UTC", "best-effort") and record in the body's `## Freshness & delivery` section:

- **The refresh mechanism.** Scheduled query, streaming push, on-demand, materialised-view refresh, reverse-ETL sync cadence. **Streaming and batch serving get equal first-class treatment — do not bias toward either.**
- **The latency commitment.** How current the data is and on what cadence it refreshes (or, for streaming, the latency target).
- **Stale-data behaviour (the honesty sub-question).** What the consumer sees when freshness is violated — a stale-data banner, a hard fail, or — the honest bad answer — **silent staleness**. "Real-time" quietly becomes a lie exactly here: a surface promises freshness, the implementation delivers staler, nothing monitors the gap, a decision is made on stale data with full confidence. Surface silent staleness explicitly and record it; it is the Stage 5 application of the "record the honest reality, not the aspiration" posture every prior stage holds. If freshness is unmonitored, that is an `## Open follow-ups` item.

### Turn 6 — Access & governance (the governance-honesty turn)

This is the turn where template-mode regression and aspirational-posture-inflation are most likely. The skill is **explicit and slow** here, mirroring Stage 4's loud `assertions` turn and Stage 3's loud `deletion_mechanism` turn — and it matters most at Stage 5, because a surface is *the last checkpoint before data leaves the data team's boundary*. Capture **`sensitivity`** (one of `public | internal | confidential | regulated`) and **`access_model`** (one of `public | sso | role-based | row-level | convention`).

Before asking, **read the named upstream Model Plan(s)** — their `sensitivity` seeds this turn directly. Ask:

> The upstream model records `sensitivity: <upstream sensitivity>`. What's this surface's sensitivity, how is access actually enforced today, and which PII columns reach the consumer?

Three things to get right:

1. **Sensitivity step-down vs the upstream model.** Stage 5 is where carefully-masked data can leak out. Surface any change from the upstream Model Plan's sensitivity explicitly. A surface whose sensitivity is *lower* than its upstream model's (a `regulated` model exposed through an `internal` dashboard) is the governance-leak failure mode — either a deliberate de-identification step (worth recording: *which columns dropped, which masked, where enforced*) or a leak worth interrogating. Disagreement is **allowed but must be recorded** in `## Access & governance`, never silently accepted.
2. **`access_model` is the Stage-5-distinctive honesty field.** Record how access is *actually* enforced today, not what you wish were true. `convention` — access granted broadly and policed by convention/trust with no technical enforcement — is an **honest, accepted answer**, recorded as such with an `## Open follow-ups` item to wire real enforcement. What is refused is recording `role-based` (or `row-level`) **aspirationally** when nothing is wired up — the exact analogue of Stage 4 refusing aspirational `business-invariant` and Stage 3 refusing aspirational `lifecycle-policy`. Do not inflate the access model just because it sounds governed; that nudge is the template-mode bias this turn refuses.
3. **PII exposure.** Record which sensitive columns reach the consumer and where masking is applied (a view, a policy tag, a BI-tool permission, the application layer). This is the last governance checkpoint before data leaves the team's boundary — name it.

### Turn 7 — Retirement trigger

Ask:

> Under what condition should this surface be retired — and is there a usage or adoption signal you'd watch for it?

Capture for the body's `## Decision & retirement` section (alongside Turn 2's decision-served):

- **The retirement trigger.** The condition under which this surface should be retired: the decision is no longer made, the consumer churned, the metric was consolidated into another surface, usage fell to zero. This is the operational form of the spine's *"if a surface cannot name the decision it informs, retire it"* — written down *before* the surface goes stale, not discovered years later as a zombie dashboard nobody dares delete.
- **The usage/adoption signal, if known.** How you'd *know* the retirement trigger has fired (dashboard view-count, API hit-rate, sync success volume). Record it in prose — `/serve-data` does **not** query usage analytics to measure it; whether the surface is actually used is a runtime DataOps concern. If no usage signal exists, that is an honest `## Open follow-ups` item.

### Turn 8 — Write the surface

Pick a filename: `<surface>.md` under `docs/serving-surfaces/`, the slug kebab-case throughout (lowercase letters, digits, hyphens; single-word slugs are technically valid but a descriptive name like `exec-revenue-dashboard` reads better).

Write the file shaped exactly as the contract in [`references/serving-surface.md`](references/serving-surface.md) specifies — the eleven frontmatter fields and the six body sections in order. The earlier turns already gathered the content each field and section needs: the upstream Model Plan(s) from Turn 1 (`related_model_plans`) and the DGQ(s) from Turn 2 (`serves_dgqs`) — the two halves of the dual kill-switch; `surface`, `surface_type`, `consumer`, and `owner` from Turn 3; the consumption contract from Turn 4; `freshness_sla` from Turn 5; `sensitivity` and `access_model` from Turn 6; and the retirement trigger from Turn 7. Read the contract for the exact field list, enum domains, and section order rather than reproducing them here.

`related_model_plans` carries the Model Plan path(s) from Turn 1; the linter requires at least one entry for `status: accepted` (the chain half). `serves_dgqs` carries the DGQ path(s) from Turn 2; the linter requires at least one entry for `status: accepted` (the loop-closure half) — `[]` is permitted only for `status: rejected`. `related_adrs` is `[]` at first write — populated later if a serving-tool ADR is linked. **There is no `related_dgqs` field** — the DGQ link is promoted to the kill-switched `serves_dgqs`; do not add a soft `related_dgqs`. Do not invent paths.

After writing, print a one-line confirmation:

```text
Wrote docs/serving-surfaces/<surface>.md
  status: <status>
```

No body summary echoed back — the user just answered the questions; reading it back is noise. Then surface the next queued surface (if Turn 3 created stubs): *"You have N draft surfaces queued from this session — want to drill the next one now?"* If the user declines, exit cleanly. Re-confirm any ADR-moment detected during the interview (a platform-wide BI-tool, reverse-ETL-platform, or feature-store choice) and recommend `/write-adr` for the cross-cutting serving-tool commitment.

Run the bundled linter `scripts/lint-serving-surface.sh` — it sits beside this `SKILL.md`, in the skill folder's own `scripts/` — as a cheap sanity check after writing. Resolve it relative to this skill folder and invoke it from the consumer project root so it picks up `docs/serving-surfaces/` (or point it elsewhere with `SERVING_SURFACES_ROOT=<dir>`). It is **best-effort**: if the script is present in this install, run it; if it is absent — a partial install that dropped the skill's `scripts/`, say — skip it silently and rely on the consumer's pre-commit hook. It is not a CI gate, just a fast structural check that frontmatter, enums, body sections, and the dual kill-switch are intact. If the schema enforced by the linter drifts from this prompt, **the linter wins** — record a fix-up issue and ship the surface that passes the linter.

## ADR-moment detection

At **any** point in the interview, if the decision being recorded is a **cross-cutting platform commitment** rather than a per-surface fact, pause and route. `surface_type` records *what kind* of surface this is; it does not license deciding the platform's serving tool inside a Serving Surface. Signals that you are looking at an ADR-moment:

- The user states a serving-tool standard that applies across the whole platform, not just this surface. Example phrasings to listen for:
  > *"All our BI is Looker from now on."*
  > *"We're standardising reverse-ETL on Hightouch."*
  > *"Every ML feature goes through Feast."*
  > *"All exec dashboards live in one Tableau workbook."*

  These are platform commitments, not per-surface facts.
- The decision is about **a default serving tool** across a class of surfaces or the whole platform (the BI tool, the reverse-ETL platform, the feature-store technology).
- The decision applies **across many surfaces, teams, or domains** rather than to this one surface.

When you spot one of these, stop the surface interview and say something like:

> This isn't a per-surface fact — it's a cross-cutting platform commitment. The right artefact is an ADR, not a Serving Surface. I recommend running `/write-adr` separately to capture this decision in `docs/adr/`. After the ADR lands, you can come back and link it from any related Serving Surfaces via the `related_adrs` frontmatter, and the per-surface plan will just *reference* the ADR rather than restate it.

Do **not** inline the ADR scaffold here. One skill, one artefact — the ADR belongs to `/write-adr`. Record `surface_type` for *this* surface, and note in `## Open follow-ups` that the platform-wide serving-tool commitment should be promoted to an ADR if the user does not run `/write-adr` immediately.

## After writing

- Do not summarise the body of the Serving Surface back to the user — they just answered the questions; reading it back is noise. The one-line confirmation is sufficient.
- If the conversation surfaced a cross-cutting commitment that the user agreed to record separately, remind them once at the end: *"Run `/write-adr` for `<topic>` when you're ready — it's not part of this surface's scope."*
- If a surface ended `needs-follow-up`, name the specific question the user needs to take to a stakeholder or upstream owner. Vague follow-ups rot; named ones get answered. Common ones here: *"confirm with the exec sponsor that this dashboard drives the retention-call decision before it's `accepted`"*, or *"the decision is real but has no DGQ — run `/gather-requirements` to capture it, then move this surface to `accepted`"*, or *"confirm whether access is actually `role-based` or only policed by convention."*
- If a surface ended `rejected` — the loop-closure kill-switch fired and the user accepted that it informs no decision — leave it in place with the rejection rationale in `## Decision & retirement` and `## Open follow-ups`. The rejection is a durable record of the deliberate decision not to build (or to retire), not a TODO to revisit.
