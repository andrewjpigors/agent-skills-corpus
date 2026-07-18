---
name: model-data
description: Convert a planned (or existing-but-undocumented) transformation into a Model Plan markdown file under docs/model-plans/, enforcing the Stage 4 kill-switch — an accepted plan must name at least one upstream Storage Plan. Use when the user says "/model-data", "model this data", "plan this model", "what's the grain of this table", "design this dbt/SQL model", "document what this fct/dim/staging model produces", "is this metric defined once", "are these tests asserting anything real", or describes a transformation ("we're about to build fct_orders", "three dashboards compute revenue differently", "our tests are all not-null checks", "this mart reads straight from raw") and wants the modelling contract — grain, layer, materialization, convention, assertion posture, lineage, sensitivity, and the canonical definition the model owns — captured before the SQL is written or after it exists but is undocumented. Staging, intermediate, mart, metric, and feature layers are equally first-class, and streaming materialisation is first-class alongside batch; the interview branches on the user's answer rather than defaulting to any. Routes to /write-adr when the decision is a platform-wide modelling-convention commitment rather than a per-model fact.
---

# /model-data — Model Plan interview

This skill runs a short, branching interview that converts a planned (or existing-but-undocumented) transformation into a **Model Plan** markdown file at `docs/model-plans/<model>.md` in the consumer's project. It is an **interview, not a template** — every plan that lands has been pressure-tested against the Transformation kill-switch (a named upstream Storage Plan), the grain-must-resolve-to-a-cardinality test, the assertions-honesty test (`business-invariant` is earned, not asserted aspirationally), the sensitivity-propagation test, and the "is this actually an ADR moment?" routing test.

This skill is self-contained: the vocabulary it leans on is inlined just below, the Model Plan contract it writes against ships beside it at [`references/model-plan.md`](references/model-plan.md), and the linter that enforces that contract ships at [`scripts/lint-model-plan.sh`](scripts/lint-model-plan.sh). Read the contract for the artefact's frontmatter fields, enum domains, and body section order before writing — do not duplicate it into the interview; reference it.

**Vocabulary this skill assumes** (the minimum it needs; the full worldview is optional deeper reading, linked at the end):

- **Model Plan.** The data team's version-controlled model of a single transformation — the grain ("one row per *what*"), the layer, the materialization, the modelling convention it honours, the assertion posture, its intra-stage dependencies, the sensitivity, and the canonical definition it owns for downstream consumers. The operational and contractual model of the transformation, *not* a project-management plan and *not* a dbt/SQL model file (it contains no SQL). Stage 4's deliverable; one file per model at `docs/model-plans/<model>.md`.
- **Transformation kill-switch.** An accepted Model Plan must name at least one upstream Storage Plan in `related_storage_plans`. A model that does not chain back to governed storage is *ungoverned business logic* — the duplicated-revenue-definition failure mode — masquerading as a real table. This is the soul of the skill; see the next section.
- **`assertions` posture.** The Stage-4-distinctive honesty field — `business-invariant` (a test ties to a named business truth), `shape-only` (only `not null` / `unique` / referential checks), or `none` (no tests yet). `business-invariant` is *earned*, not asserted aspirationally; `shape-only` and `none` are honest, accepted answers, not failures to punish.

**Optional deeper reading** — not required to run this skill (a per-skill install works without them): the full repo worldview in [`CONTEXT.md`](https://github.com/sleeplessv/relentless-data-skills/blob/main/CONTEXT.md) and the lifecycle reference in [`docs/data-engineering-101.md`](https://github.com/sleeplessv/relentless-data-skills/blob/main/docs/data-engineering-101.md).

A Model Plan is *neither* of the two things its name risks being read as. It is **not** a project-management plan for a modelling effort — no TODO list, owners, or delivery dates. It is **not** a dbt/SQL model file — it contains no SQL, no `ref()`, no Jinja, no Dataform/SQLMesh config. It is the operational and contractual model of the transformation: the human-authored *commitments* (grain, layer, materialization, convention, assertions, canonical definition, downstream contract) that the actual SQL/dbt/Dataform/SQLMesh code should reflect. The code that *implements* those commitments lives in the consumer's transformation repo and is out of scope — this skill emits no SQL, no dbt model, no test YAML. The plan is the contract the code should be reviewed against, not a substitute for it. It is the structural analogue of the Storage Plan one stage upstream, deliberately human-authored and never inferred from a tool: **no `manifest.json` parsing, no `INFORMATION_SCHEMA` scan, no warehouse or dbt/Dataform project introspection.**

## Soul of the skill: the Transformation kill-switch

The single load-bearing question this skill exists to force is:

> **Which Storage Plan(s) under `docs/storage-plans/` does this model read from?**

If the user cannot point to at least one accepted-or-draft Storage Plan in `related_storage_plans`, the model does not deserve a plan. A Model Plan with no named upstream storage is the structural twin of a Storage Plan with no named upstream Ingestion Plan, of an Ingestion Plan with no named upstream Source Profile, of a Source Profile with no consumer DGQ, and of a DGQ with `action_change: nothing` — documentation that floats free of the lineage graph, the failure mode this stage exists to refuse. The Stage 4 floating node is the most insidious of the chain: a model with no governed input is *ungoverned business logic* — the duplicated-revenue-definition failure mode — masquerading as a real table. Surface that conclusion explicitly. Recommend the user run `/plan-storage` first; come back to `/model-data` once the upstream storage is planned.

A model built only on *other models* (a `mart` built on `int_*` models) is not exempt: it still names, in `related_storage_plans`, the **root** Storage Plan(s) its lineage ultimately derives from. Every model chains to stored data eventually; the kill-switch forces the chain to terminate at governed storage, not at another floating model.

Do not soften the kill-switch. Do not paper over the absence by inventing a plausible-sounding Storage Plan path on the user's behalf. The kill-switch (Turn 1) is the one place in this skill where the user must speak first; a recommendation there would coach them past the very gap the skill exists to surface.

The linter enforces the structural contract — an `accepted` plan with an empty `related_storage_plans` fails `scripts/lint-model-plan.sh`. This skill is the upstream half: it refuses to start the interview without one named upstream Storage Plan.

## Target shape

- **Length.** 7–11 substantive exchanges per plan is typical — comparable to Stage 2 and slightly tighter than Stage 3, because several Stage 4 concerns (grain, layer, materialization) are crisp single-answer fields, while the depth concentrates in the assertions turn (Turn 6) and the downstream-contract turn (Turn 8). Keep going until the grain, convention, assertion posture, and downstream contract are honestly named — don't truncate to hit the cap, and don't pad to fill it. Sharp, not exhausting.
- **Output.** One markdown file per model at `docs/model-plans/<model>.md`. If one transformation effort produces a layered set (`stg-orders` → `int-orders` → `fct-orders`), write one fully-drilled plan first, the rest queued as `status: draft` so a later run can pick them up.
- **Tone.** Interrogative, not adversarial. The goal is to find the honest contract — including "we only have `not null` tests" (`assertions: shape-only`) and "no tests yet" (`assertions: none`) answers — not to make the user feel bad for inheriting an under-modelled or under-tested transformation layer.

## Resumability check (run this first)

Before starting a fresh interview, scan `docs/model-plans/` in the consumer's project. If one or more Model Plan files exist, **pause and ask**:

> I see existing Model Plans in `docs/model-plans/`. Do you want to:
>
> 1. Continue an existing **draft** or **needs-follow-up** plan (resumable)
> 2. Start a **new** plan
> 3. **List** all plans and their statuses

Treat `status: accepted`, `status: rejected`, and `status: superseded-by-<path>` files as immutable from this skill's perspective — do not offer to edit them. Superseding an old plan (e.g., a model is re-grained) is done by writing a new one and updating the old one's status by hand. If the user picks "continue", load the chosen file and resume from the first unfilled section (commonly the section that corresponds to the next unanswered turn). If they pick "list", print one line per file: `<path> — <status> — <model> (<layer>, grain: <grain>)`.

If `docs/model-plans/` does not exist, create it on first write — not before.

## Steps

Carry out the nine turns below in order. **One question per turn**, not a wall of multiple questions, except where the spec explicitly says "combined turn" (Turn 8). If the user volunteers material that answers a later turn early, accept it and skip ahead — do not re-ask. Do not deliver multi-paragraph monologues; keep each prompt tight.

Two cross-cutting rules apply to every turn:

- **Recommend before you ask.** For each turn's question, propose a plausible answer first — derived from the named upstream Storage Plan(s), the model name itself, adjacent plans/ADRs, or sensible defaults — then ask the user to accept, reject, or refine it. Reacting to a concrete proposal is faster and sharper than generating one cold. If you genuinely have no basis for a recommendation, say so and ask open. Never invent the kill-switch answer (Turn 1) this way — the named upstream Storage Plan is the one place the user must speak first. And never nudge toward a particular `modelling_convention` (Turn 4) or inflate the `assertions` posture (Turn 6) toward `business-invariant` just because it sounds rigorous — those defaults are exactly the template-mode bias this skill exists to refuse.
- **Explore before you ask.** If a turn's question can be answered by looking at the project — existing Storage Plans in `docs/storage-plans/`, Ingestion Plans in `docs/ingestion-plans/`, Source Profiles in `docs/sources-of-record/`, DGQs in `docs/requirements/`, ADRs in `docs/adr/`, adjacent Model Plans in `docs/model-plans/`, glossary entries in `CONTEXT.md` — look first, then bring what you found into the turn. In particular, **always read the named upstream Storage Plan(s)** once identified in Turn 1, and the Ingestion Plan(s) / Source Profile(s) they chain to; their `sensitivity`, `format`, `access_pattern`, residency notes, and the canonical definition they imply seed Turns 5–8 directly. Do not make the user re-derive what the repo already knows. If a stakeholder term collides with `CONTEXT.md`'s glossary, call it out the moment you notice it.

### Turn 1 — Name the upstream Storage Plan(s) (the kill-switch)

Ask, verbatim or close:

> Which Storage Plan(s) under `docs/storage-plans/` does this model read from? Point me at one or more by filename or by dataset.

Before asking, scan `docs/storage-plans/` and list the available Storage Plan files with their `dataset`/`storage_system` line and `status` — so the user is choosing from a concrete set, not naming a file from memory. If `docs/storage-plans/` is empty or absent, that is itself the answer: there is no planned upstream storage; the model does not deserve a plan yet.

Three branches:

- **One or more named upstream Storage Plans.** The user points to one or more files with `status: accepted` or `status: draft`. Record the paths; they go into `related_storage_plans`. Read each one — and the Ingestion Plan(s) / Source Profile(s) it chains to — before continuing; their `sensitivity`, `format`, `access_pattern`, residency notes, and operational contract seed the next several turns. Continue to Turn 2.
- **A plan exists but it is `rejected` or `superseded-by-<path>`.** Push back: *"That Storage Plan was rejected — what's the live upstream storage for this model?"* / *"That plan was superseded by `<path>` — should we model against the superseding one instead?"* Do not start the plan against a non-live storage path; the upstream link must be a storage someone has actually accepted as the contract.
- **A model built only on other models.** The user says "this reads from `int-orders`, not from storage directly." That is fine — but the kill-switch still bites: ask which **root** Storage Plan(s) the lineage ultimately derives from, and record those in `related_storage_plans` (the upstream Model Plan goes into `depends_on` at Turn 5). A model whose lineage cannot be traced back to *any* Storage Plan is the floating node the kill-switch refuses.
- **No Storage Plan exists upstream, or the user cannot name one.** **Trigger the kill-switch.** Do not write a plan. Tell the user:
  > There's no named upstream Storage Plan for this model. A Model Plan without a governed upstream is ungoverned business logic that floats free of the lineage graph — the duplicated-revenue-definition failure mode masquerading as a real table. I recommend running `/plan-storage` first to plan the storage this model reads from, then coming back to `/model-data` once at least one Storage Plan under `docs/storage-plans/` is in place.

  Then exit cleanly. Do not start drafting a plan "just in case." The kill-switch is the differentiator; surface it without apology.

### Turn 2 — Model and grain

Ask:

> What's the model — a kebab-case `model` slug — and what's its grain: one row per *what*? Is this one model or several?

Capture two fields now:

- **`model`** — kebab-case slug uniquely naming the model (`stg-orders`, `int-orders-enriched`, `fct-orders`, `dim-customer`, `daily-gross-revenue`, `customer-churn-features`). Aim for a name that reads as "what this model is," matching the layer prefix convention the project already uses.
- **`grain`** — free-text, **required**, asked early and explicitly because it is the modelling decision everything else hangs on. It must resolve to a **concrete cardinality**: "one row per order", "one row per customer per day", "one row per source row" (an honest passthrough grain). A vague grain — *"orders-ish"*, *"sort of per customer"* — is **not accepted**. Push back until it resolves: *"one row per what, exactly? If two rows can share every key, the grain isn't pinned down yet."* A fuzzy grain is a model that will be joined at the wrong cardinality and silently double or triple a count — the single most common modelling error, and the one this turn exists to design against.

Listen for plural models hiding inside one ask. A single transformation effort often produces a layered set: `stg-orders` (cleaned passthrough) → `int-orders-enriched` (joined/enriched) → `fct-orders` (analytical fact). Each is a separate Model Plan — they have genuinely different grains, layers, materializations, and test postures.

**Branching rule.** If more than one model surfaces:

1. Ask the user to pick **one** to drill fully right now.
2. For each of the others, write a stub Model Plan to `docs/model-plans/<model>.md` with `status: draft`, frontmatter populated with the upstream Storage Plan(s) from Turn 1 in `related_storage_plans`, the `model` and `grain` identifying the stub, and all other linter-required fields set to safe placeholders (`layer: staging`, `materialization: view`, `modelling_convention: none`, `sensitivity: internal`, `assertions: none`), with a note in `## Open follow-ups` that this plan needs resumption. Body sections present but with TBD bullets, so the linter passes.
3. Tell the user the stubs are saved and this session will drill the chosen model. Do not abandon them silently.

> Queue the *upstream* layer's plan as a stub even if the user only asked about the downstream model — a `fct-orders` plan should reference an `int-orders` Model Plan in `depends_on`, not float above an unwritten intermediate layer.

### Turn 3 — Layer and materialization

Ask:

> What layer is this — `staging`, `intermediate`, `mart`, `metric`, or `feature` — and how is it materialised: `view`, `table`, `incremental`, `materialized-view`, `ephemeral`, or `streaming`?

Capture two fields:

- **`layer`** — one of `staging | intermediate | mart | metric | feature`. **All five are equally first-class.** Recording the layer makes a `mart` reading straight from raw with no intermediate layer a *visible, deliberate* choice rather than an accident.
- **`materialization`** — one of `view | table | incremental | materialized-view | ephemeral | streaming`. **`streaming` is first-class. Do not bias toward batch.** A real-time materialisation and its batch equivalent are both representable here; if both exist for the same definition, that reconciliation is recorded in Turn 5.

**Intermediate-layer sub-question.** If `layer: mart` (or `metric`) reads **directly** from a Storage Plan with no intervening `staging`/`intermediate` model, surface it: *"this mart reads straight from storage with no staging/intermediate layer — is that deliberate (a trivial passthrough) or should a staging model absorb upstream churn so a column rename doesn't break every downstream consumer at once?"* **Record, do not block** — note the relationship and the rationale in `## Lineage & dependencies`. It is a smell the skill surfaces, not a rule it enforces.

### Turn 4 — Modelling convention (the ADR-moment detector)

Ask:

> What modelling convention does this model honour — `star`, `data-vault`, `one-big-table`, `activity-schema`, `normalised`, or `none`? And is that an established platform convention you're following, or one you're deciding right now?

Capture **`modelling_convention`** — one of `star | data-vault | one-big-table | activity-schema | normalised | none`. The second half of the question is the load-bearing one — it routes:

- **Following an established convention.** Record it. If a convention ADR exists in `docs/adr/`, link it via `related_adrs` and reference it from `## Model identity`. This is the common case; one quick turn.
- **Deciding the platform convention here.** If the user says something warehouse-wide — *"we should make everything star-schema"*, *"let's standardise on one-big-table"*, *"data vault for the whole platform"* — **stop and route to `/write-adr`.** A platform-wide convention choice is a cross-cutting commitment, not a per-model fact: it applies across datasets, teams, and future models, exactly the signature of an ADR-moment (see [ADR-moment detection](#adr-moment-detection) below). Say so plainly, recommend `/write-adr`, and record `modelling_convention` as the convention *this* model follows while noting in `## Open follow-ups` that the platform-wide commitment should be promoted to an ADR. Do not bury a warehouse-wide decision in one model's frontmatter.

`none` is an honest answer — a staging passthrough or a one-off feature table need not honour a formal convention. Do not nudge toward `star` or any other convention just because the warehouse "usually" uses it; that nudge is the template-mode bias this turn refuses.

### Turn 5 — Lineage and dependencies

Ask:

> Which other models does this one build on — the upstream Model Plans in `depends_on`? And is the same definition computed anywhere else (a streaming view alongside a batch table)?

Capture **`depends_on`** — a YAML list of paths to upstream Model Plans (the intra-Stage-4 DAG). Empty `[]` is valid for a `staging` model that reads only from storage. Record three things in `## Lineage & dependencies`:

- **The intra-stage DAG.** Which Model Plans this one reads from (`fct-orders` depends_on `int-orders-enriched` depends_on `stg-orders`). The kill-switch still forces the chain to terminate at a governed Storage Plan in `related_storage_plans` — `depends_on` is the *within-stage* graph, `related_storage_plans` is the *root* anchor.
- **The intermediate-layer relationship from Turn 3.** If a `mart` reads directly from storage with no intervening model, record *why* here (and flag it if the absence was accidental, not deliberate).
- **Streaming/batch reconciliation.** If the same definition is computed both as a `streaming` materialisation and a batch `table`/`incremental`, **name the single shared definition both derive from and how drift is prevented.** This is where "last-hour revenue" and "daily revenue" quietly fork; the skill surfaces it so the two are tied to one definition, not written independently.

### Turn 6 — Tests and assertions (the loudest turn)

This is the turn where template-mode regression and aspirational-posture-inflation are most likely. The skill is **explicit and slow** here, mirroring Stage 3's loud `deletion_mechanism` turn. Capture **`assertions`** — one of `business-invariant | shape-only | none`.

Ask:

> What does this model assert about *business correctness*, not just shape? Name one invariant — revenue equals the sum of line items, active customers cannot decrease in a backfill, a daily total equals the sum of its hourly parts. If you can't name one, you have `shape-only`, not `business-invariant`.

Map to:

- **`business-invariant`** — at least one assertion ties to a **named business truth**. The user must be able to *state the invariant in words*. If they cannot, it is not `business-invariant`. Record the specific invariant(s) in `## Tests & assertions`.
- **`shape-only`** — tests exist but only check structural shape (`not null`, `unique`, `accepted_values`, referential integrity). An **honest, accepted answer** — recorded as such, with an `## Open follow-ups` item to add invariant coverage. Record the shape checks present *and the invariants missing*.
- **`none`** — no tests yet. Also **accepted** — an untested draft is a legitimate state — but **never silently glossed**. Record the plan to add tests in `## Open follow-ups`.

Three rules:

1. **`business-invariant` is earned, not asserted.** Recording `business-invariant` because it sounds rigorous when only `not null` and `unique` tests exist is the exact failure this turn exists to catch — the analogue of Stage 3 refusing aspirational `lifecycle-policy`. If the user cannot name the business truth a test asserts, downgrade honestly to `shape-only`.
2. **`shape-only` and `none` are honest, valid answers and must not be punished by the interview.** What *should* be pushed back on is pretending invariant coverage exists. An under-tested model the team inherited is not a moral failing; pretending it is tested is.
3. **Each of `shape-only` and `none` carries a `## Open follow-ups` item** naming the missing coverage. The gap is recorded, not hidden.

### Turn 7 — Sensitivity and PII propagation

Capture **`sensitivity`** — one of `public | internal | confidential | regulated`. This enum is **deliberately identical** to the Source Profile's, Ingestion Plan's, and Storage Plan's; cross-stage enum drift would break the lineage-graph reasoning the kill-switch chain enables.

Before asking, **read the named upstream Storage Plan(s)** — their `sensitivity` seeds this turn directly. Ask:

> The upstream storage records `sensitivity: <upstream sensitivity>`. What's the sensitivity of this model's output, and which columns touch PII?

**Sensitivity step-up / step-down.** Stage 4 is where PII *propagates* — and where it should be *de-identified*. Surface any change from the upstream Storage Plan's sensitivity explicitly:

- **Step-down** (a `regulated` store aggregated to an `internal` mart): *"the upstream store is `regulated`; this model is `internal` — where is the de-identification, and which columns are dropped or masked?"* Either it is a deliberate de-identification step (worth recording, with a pointer to where masking/aggregation is enforced) or a leak worth interrogating.
- **Step-up** (an `internal` store joined with a `regulated` dimension): the model is now propagating regulated columns into a possibly widely-read table — name which columns, and where access is controlled.

Record which columns touch PII and where masking is enforced in `## Downstream contract` (the PII/masking notes) and any step-up/step-down disagreement in `## Tests & assertions` / `## Downstream contract`. Disagreement is **allowed but must be recorded** — never silently accepted.

### Turn 8 — Downstream contract

Ask, in one combined turn:

> What canonical definition does this model own — the single place "gross revenue" or "active customer" is defined? What's the stable column contract and freshness expectation, who reads it, and what must Stage 5 serving *not* bypass?

Capture for the body's `## Downstream contract` section:

- **Canonical definition owned.** The single place a business concept is defined, so downstream serving reads it rather than re-deriving it three different ways. A `staging` model may own nothing canonical — that is an honest answer.
- **Stable column contract.** The columns downstream readers may depend on, and which are internal/unstable.
- **Freshness / refresh expectation.** How current the data is and on what cadence it refreshes (or, for `streaming`, the latency target).
- **Who reads it and how.** Downstream marts, BI tools, reverse-ETL, ML features.
- **What Stage 5 must not bypass.** The contract serving is allowed to assume — and forbidden to circumvent (no reading raw/staging directly to recompute this model's logic).

### Turn 9 — Write the plan

Pick a filename: `<model>.md` under `docs/model-plans/`, the slug kebab-case throughout (lowercase letters, digits, hyphens; single-word slugs are technically valid but a layer-prefixed name like `fct-orders` reads better).

Write the file shaped exactly as the contract in [`references/model-plan.md`](references/model-plan.md) specifies — the twelve frontmatter fields and the six body sections in order. The earlier turns already gathered the content each field and section needs: the upstream Storage Plan(s) from Turn 1 (`related_storage_plans`), `model` and `grain` from Turn 2, `layer` and `materialization` from Turn 3, `modelling_convention` from Turn 4, `depends_on` from Turn 5, `assertions` from Turn 6, `sensitivity` from Turn 7, and the downstream contract from Turn 8. Read the contract for the exact field list, enum domains, and section order rather than reproducing them here.

`related_storage_plans` carries the Storage Plan path(s) from Turn 1; the linter requires at least one entry for `status: accepted`. `depends_on` carries upstream Model Plan paths from Turn 5 (or `[]`). `related_dgqs` and `related_adrs` stay `[]` at first write — populate them later only if cross-links accrue (the upstream chain names a consumer DGQ worth recording transitively, or a convention ADR is linked). Do not invent paths.

After writing, print a one-line confirmation:

```text
Wrote docs/model-plans/<model>.md
  status: <status>
```

No body summary echoed back — the user just answered the questions; reading it back is noise. Then surface the next queued plan (if Turn 2 created stubs): *"You have N draft plans queued from this session — want to drill the next one now?"* If the user declines, exit cleanly.

Run the bundled linter `scripts/lint-model-plan.sh` — it sits beside this `SKILL.md`, in the skill folder's own `scripts/` — as a cheap sanity check after writing. Resolve it relative to this skill folder and invoke it from the consumer project root so it picks up `docs/model-plans/` (or point it elsewhere with `MODEL_PLANS_ROOT=<dir>`). It is **best-effort**: if the script is present in this install, run it; if it is absent — a partial install that dropped the skill's `scripts/`, say — skip it silently and rely on the consumer's pre-commit hook. It is not a CI gate, just a fast structural check that frontmatter, enums, body sections, and the kill-switch are intact. If the schema enforced by the linter drifts from this prompt, **the linter wins** — record a fix-up issue and ship the plan that passes the linter.

## ADR-moment detection

At **any** point in the interview, if the decision being recorded is a **cross-cutting platform commitment** rather than a per-model fact, pause and route. The most common trigger is Turn 4's convention question, but the signal can surface anywhere. Signals that you are looking at an ADR-moment:

- The user states a convention that applies across the whole warehouse, not just this model. Example phrasings to listen for:
  > *"We should make everything star-schema."*
  > *"Let's standardise the whole platform on one-big-table."*
  > *"Data vault for every domain from now on."*
  > *"Every model gets a staging layer, no exceptions."*

  These are platform commitments, not per-model facts.
- The decision is about **a default modelling convention** across a class of models or the whole warehouse.
- The decision is about **a default layering or testing policy** across models (`"every mart must have an intermediate layer"`, `"all regulated columns are masked at the staging layer"`).
- The decision applies **across many models, teams, or domains** rather than to this one model.

When you spot one of these, stop the plan interview and say something like:

> This isn't a per-model fact — it's a cross-cutting platform commitment. The right artefact is an ADR, not a Model Plan. I recommend running `/write-adr` separately to capture this decision in `docs/adr/`. After the ADR lands, you can come back and link it from any related Model Plans via the `related_adrs` frontmatter, and the per-model plan will just *reference* the ADR rather than restate it.

Do **not** inline the ADR scaffold here. One skill, one artefact — the ADR belongs to `/write-adr`. Record `modelling_convention` as the convention this model follows, and note in `## Open follow-ups` that the recorded pattern should be promoted to an ADR if the user does not run `/write-adr` immediately.

## After writing

- Do not summarise the body of the Model Plan back to the user — they just answered the questions; reading it back is noise. The one-line confirmation is sufficient.
- If the conversation surfaced a cross-cutting commitment that the user agreed to record separately, remind them once at the end: *"Run `/write-adr` for `<topic>` when you're ready — it's not part of this plan's scope."*
- If a plan ended `needs-follow-up`, name the specific question the user needs to take to a stakeholder or upstream owner. Vague follow-ups rot; named ones get answered. Common ones here: *"confirm with finance which revenue definition is canonical before this metric model is `accepted`"*, or *"confirm whether an invariant test actually runs, or whether the suite is shape-only."*
- If a plan ended `rejected` — the model was planned and the user decided the upstream storage chain doesn't justify it after all — leave it in place with the rejection rationale in `## Open follow-ups`. The rejection is a durable record of the deliberate decision not to build, not a TODO to revisit.
