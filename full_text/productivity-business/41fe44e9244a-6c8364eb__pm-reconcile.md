---
name: pm-reconcile
description: Rebuild playbook for an existing product onboarded to Pureinn. Reconciles the actual codebase against a folder of legacy documents (BRD, FSD, domain/entity models, business rules) that may contain logical, semantic and structural inconsistencies. Runs in two phases - first PLAN (inspect docs + code, define which areas to reconcile, in what order, into which Pureinn artifacts), then per-area EXECUTION (/pm-reconcile domain | rules | features ...) one layer at a time. Produces a living Reconciliation Report and rebuilds the 4 Live Registers + feature inventory clean. A closing verify pass (/pm-reconcile verify) re-reads the source one last time, proves every unit was transposed, incorporates any gaps it finds (not just reports them), and rules whether the legacy source is safe to archive - the source-disposal gate. The source is whatever the user points to (any format), never a hardcoded BRD. Use when a product was built outside the framework, has stale or conflicting docs, and the (often new) team needs one consistent source of truth that matches the code. Multi-session - track progress with pm-reconcile-status.
license: MIT
metadata:
  agent-mode: never
  author: https://github.com/ljucask
  version: "1.2.0"
  domain: product-management
  triggers: reconcile, rebuild, migration, existing product, old docs, BRD reconciliation, team handover, codebase vs docs, onboard existing product, rebuild from code, source coverage, verify transposition, disposal readiness, archive source, specified not implemented, strategic layer, delivery-driven roadmap
  role: specialist
  scope: reconciliation
  output-format: document
  related-skills: pm-reconcile-status, pm-entity-registry, pm-domain-model, pm-business-rules-library, pm-reverse-extract, pm-glossary, pm-stripe
---

# PM - Reconcile (Rebuild from Existing Product)


## Agent mode (`--agent`)

This skill's value is the live dialogue - `--agent` is not supported. If invoked with `--agent`, warn once ("this skill needs interactive back-and-forth; agent mode would hollow it out") and proceed interactively.

---

## What this skill does

Takes an existing product - working code plus a pile of legacy, possibly inconsistent documentation - and rebuilds a clean Pureinn structure that matches reality. It runs in **two phases**:

1. **PLAN** - inspect the old-docs folder and the codebase surface, detect which areas exist, map each to its target Pureinn artifact, and define the order. Output: `reconciliation_plan.md`.
2. **EXECUTE per area** - `/pm-reconcile [area]` reconciles one layer at a time in the planned order, asking about real business-logic conflicts, appending to a living Reconciliation Report, and rebuilding that layer's register.

Reconciliation can span multiple sessions. Progress is held in `state.json` and shown by **`/pm-reconcile-status`**.

This is the **Rebuild playbook** referenced in the `/pureinn` orchestrator. Run it when a product was built outside Pureinn, legacy docs disagree with the code and each other, and the (often new) team needs one trustworthy source of truth.

---

## Invocation modes

| Command | Mode | Does |
|---|---|---|
| `/pm-reconcile` | **Plan / route** | No plan yet → build the Reconciliation Plan. Plan exists → short status + point to the next area (full dashboard via `/pm-reconcile-status`). |
| `/pm-reconcile plan` | **Plan (force)** | Re-inspect and rebuild the plan. |
| `/pm-reconcile domain` | **Execute** | Reconcile entities + attributes + enums + state machine **structure** → `entities.md` (Register 1) + glossary aliases. Offers the cross-domain ERD → `domain-model.md`. |
| `/pm-reconcile rules` | **Execute** | Reconcile business rules + decision models + transition **guard conditions** → `business_rules.md` + `decision_models.md` (Registers 2-3). |
| `/pm-reconcile features` | **Execute** | Reconcile feature inventory → `feature_list.md` + stub Feature Cards Section 1 (Register 4). |
| `/pm-reconcile [other]` | **Execute** | Any extra area the plan defined (e.g. `events`, `integrations`). |
| `/pm-reconcile verify [area]` | **Verify + incorporate** | Re-read the source one more time, prove every unit landed in the registers, **incorporate the gaps it finds** (not just report them), and rule on disposal readiness. The source-disposal gate. Default = all areas; scope with `verify domain \| rules \| features`. |

**Default area order is dependency-driven:** `domain` → `rules` → `features`. Entities are the vocabulary everything references, so they become canonical first. Rules operate on entities and guard transitions, so they come next. Features reference rules and entities, so they come last. This mirrors the register numbering 1 → 2 → 3 → 4. The plan can adapt the order (e.g. domain-by-domain on a large product).

---

## The source is whatever the user points to (no hardcoded name)

"BRD" is only one possible source. Another project's source of business intent may be an FSD, a domain model, a Confluence/Notion space, a spec folder, an old wiki, even a spreadsheet - any format, any name. **Never assume the source is a "BRD" or hardcode a filename.** At the start of PLAN (and at the start of VERIFY), ask the user where their source of business intent lives, then deep-ingest whatever they point to. Throughout this skill, "**legacy source**" / "**the source**" means that user-pointed input, not a specific document.

## Source of truth model (read before running any area)

Reconciliation is **asymmetric**. Two layers, two kinds of mismatch. Apply on every comparison:

| Layer | Source of truth | On mismatch |
|---|---|---|
| **Business intent** - rule values, decisions, what a feature should do, *why* | **Legacy docs (BRD / business rules / decision models)** | If code implements a *different business rule* (e.g. refund window 14 vs 30 days) → **business-logic divergence**. Do NOT silently pick a side. Surface via AskUserQuestion; the team rules "code is the bug" or "doc is stale". Record it. |
| **Technical structure** - entity / attribute / enum / state names, state-machine shape, what is implemented | **Codebase** (observed reality) | **Rewrite the docs to match the code. Mechanical, no question.** Old doc name kept as an **alias** in the glossary. |

Two rules that follow:
1. **Never change the codebase.** This skill rebuilds documents only. Code that diverges from intended logic is *flagged*, not edited away.
2. **Docs that run ahead of the code** (described but not implemented) → **carded as `1_Backlog` in `feature_list.md` (Register 4), not just noted in the report.** Distinguish the layers: **R1-3 (entities, rules, decision models) describe only what actually runs** - never fabricate unbuilt logic into them. **R4 (feature_list / cards) is the backlog** - it legitimately holds `1_Backlog` stubs for specified-not-implemented capabilities, marked `specified in source, not yet implemented`. This is what `1_Backlog` is for. The reconciliation report is an audit log, not the backlog: a capability that lives only in the report is invisible backlog that vanishes when the source is discarded. Card it so it survives.

End state: legacy docs become a dead reference. The rebuilt registers are the new single source of truth - structurally aligned to code, carrying business logic from the docs, every divergence visible.

---

## Business logic now, feature design JIT

Migrate all business logic now so the team never mirrors the old docs again - but do not design every feature upfront:

| Layer | When | Lives in |
|---|---|---|
| Entities, states, rules, decision models | **Fully now** | The Live Registers. Old BRD then retired. |
| Feature → rule mapping (Feature Card Section 1) | **Now** | Stub cards link to register BR-IDs |
| Feature technical design (Sections 2-3: ACs, sequence diagram, files) | **JIT** via pm-feature-design | Written when the feature is next worked, with a fresh code scan |

Business logic lives in the registers, not the cards - so deferring Sections 2-3 loses nothing.

---

## Rebuild captures structure, NOT the strategic layer (set expectations)

Rebuild onboards an existing product: it reconciles **code + source** into entities, rules, decision models, feature inventory and a **delivery-driven** view. It deliberately **skips Phase 1-3** (discovery, validation, business model) - you are not re-validating a product that already exists.

The consequence the team must know up front: **the strategic layer never gets captured by reconcile.** Vision, 12-month goal, North Star Metric, business model, and per-phase success criteria (the Phase 1-3 / roadmap-v1 outputs) are simply absent. If you go straight to `/pm-product-roadmap`, it can only build a roadmap whose **phase boundaries are driven by code-readiness and dependencies, not strategy** - and it will ask you for those strategic inputs or mark them TBD.

This is not a bug - but it is a fork the team should make consciously:

- **Want strategy-driven phasing** (MVP boundary set by what the business must prove, not by what is half-built)? **Backfill the strategic layer first** - it is lean because you already know it: `/pm-business-model` (how it earns - if a PSP like Stripe is wired, the take-rate model is knowable *now*, do not defer it), a North Star Metric, a one-line 12-month goal. Then run roadmap.
- **Fine with a delivery-driven roadmap for now?** Run roadmap directly and let it mark the strategic layer TBD - revisit when it matters.

Surface this fork at the end of reconcile (handoff), so the team is not surprised by it at roadmap time.

---

## What this skill does NOT do

- Change, refactor, or "fix" the codebase - documents only
- Resolve genuine business-logic conflicts on its own - those go to the user via AskUserQuestion
- Write Feature Card Sections 2-3 - that stays JIT in `pm-feature-design`
- Re-run product discovery or validation - this is a rebuild, not a new-product workflow

---

## Dependencies

**Required:**
- `/pureinn` already run - workspace, `state.json`, `pureinn-variables.md` exist
- Codebase accessible (routes / controllers / models / schema / enums / tests)
- A folder containing the legacy docs (any format)

**Recommended:** `/common-ground` (stack, APIs, domain model) - speeds the code scan.

**Produces artifacts used by:** `pm-feature-design` (JIT) and `pm-stripe` (rebuilt registers); the team (Reconciliation Report); `pm-reconcile-status` (progress).

---

# ===== PLAN MODE =====

Runs on `/pm-reconcile` (when no plan exists) or `/pm-reconcile plan`.

## Step P0: Current state check

Show a state table: codebase accessible? old-docs folder found (and which doc types)? do any registers already exist? does `reconciliation_plan.md` exist? If a plan exists, ask whether to keep it (route to status) or rebuild it.

**Interaction:** Group related questions (2-4 per round) and confirm before moving on. For any A/B/C/D choice, use the AskUserQuestion tool with one option marked **(Recommended)** - never print options as plain text. Keep open-ended questions free-text (don't fake options). If the user is unsure, propose 3-4 concrete options plus "Other". Surface an assumption the moment you make one; never fabricate to fill a gap. (Full standard: CLAUDE.md.)

## Step P1: Inspect (do not deep-reconcile yet)

- Catalogue the old-docs folder **recursively** (per the Deep source ingestion standard) - walk every subfolder, list every document, not just the top level. An overview/master table (e.g. a business-rules CSV) is a pointer: note that its detail lives in the referenced files / subfolder and that those will be read in full during execution. Record what each document covers (domain model, internal/external entities, state machines, business rules, decision tables, FSDs, feature lists).
- Skim the codebase surface: top-level structure, models/schema, route map, enums - enough to know what areas exist. Do NOT diff yet.
- Report the catalogue: "Found N documents across M folders" - so a missed subfolder is visible before the plan is built.

## Step P2: Define the plan

For each detected area:
- Map it to its target Pureinn artifact (entities.md / business_rules.md / decision_models.md / feature_list.md + cards / extra)
- Set its order (default `domain → rules → features`, adapt if the product is large or multi-domain)
- Note its primary source docs and the relevant code locations

Then use AskUserQuestion to confirm:
- Question 1: "Source-of-truth policy?" - A: "Code wins structure, docs win business logic, ask on conflicts (Recommended)" / B: "Code wins everything" / C: "Docs win everything, flag code"
- Question 2: "Reconcile the whole product, or domain-by-domain?" - A: "Domain-by-domain (Recommended for large products)" / B: "Whole product per layer"

Surface this inline if the product is large:
```
Assumption: a whole-product layer pass on a large codebase produces a large Reconciliation Report
and a long AskUserQuestion queue. Domain-by-domain keeps each pass reviewable.
If this is wrong, tell me - it affects how I batch the areas.
```

## Step P3: Write the plan + initialize status

Write `reconcile/reconciliation_plan.md` (template below) and initialize `state.json` `reconcile.areas[]` (schema below) with every area at `status: pending`.

Close with the ordered list of commands to run, e.g.:
```
PLAN READY - [N] areas.
Run in order:
  1. /pm-reconcile domain
  2. /pm-reconcile rules
  3. /pm-reconcile features
Check progress any time with /pm-reconcile-status.
```

---

# ===== PER-AREA EXECUTION =====

Runs on `/pm-reconcile [area]`.

## Step A0: Load plan & confirm

Read `reconciliation_plan.md` + `state.json reconcile`. Confirm the requested area exists in the plan. If an earlier area in the order is still `pending`, warn (dependencies may be unsettled) but allow override if the user insists. Mark this area `in_progress`.

## Step A1: Scoped code scan

Scan only the slice relevant to this area:
- **domain:** models / schema / migrations / enums / status fields + transition logic → real entities, attributes, enums, and state-machine **structure** (which states & transitions exist)
- **rules:** validation / guard / computed-condition logic + the conditions gating each state transition → rules the code actually enforces
- **features:** routes / controllers / services / tests → what the system actually does

## Step A2: Scoped doc parse

Read the source docs the plan tied to this area **in full and to the depth** (per the Deep source ingestion standard) - if an overview/master table references per-item detail files or a `/details` subfolder, read every one of them, not just the summary row. Extract the intended business picture for this layer only (with provenance: doc + section/file). State coverage: "Read N source files for this area" so a skipped detail file is visible. Never reconcile from the overview table alone.

## Step A3: Reconcile

Diff code (A1) vs intent (A2), applying the source-of-truth model. Classify every mismatch:

| Type | Resolution |
|---|---|
| Naming drift (same thing, different name) | Auto: canonical = code name; alias → glossary |
| Structural drift (attribute/enum/state shape differs) | Auto: register reflects code; doc term as alias or `not implemented` |
| **Business-logic divergence** (the rule itself differs) | **AskUserQuestion** - team rules code-bug vs stale-doc; record |
| Doc-only / aspirational (described, not built) | Mark `specified, not implemented` → backlog; not added as real |
| Code-only / undocumented (built, not in docs) | Capture as real; flag "confirm intent" |
| Internal doc contradiction (docs disagree) | **AskUserQuestion** - which is authoritative |

Use the **grouped question pattern** (CLAUDE.md): batch related conflicts (2-4 per group), present code behavior + doc statement(s) + a recommended resolution, confirm, continue. Never silently resolve a business-logic conflict. Assign `DIV-NN` IDs to divergences.

**High-volume batching (checkpointed) - required when an area is large:** When a single area pass has many items to reconcile (roughly **>15** rules / decision tables / features - common in legacy systems with dozens of each), do NOT process them all in one sitting. Batch and checkpoint:

1. Split the area's items into batches by a natural grouping - rules and decision tables by **feature set or rule category**, features by **feature set**, entities by **cluster**. Aim for ~10-15 items per batch. Business rules and decision tables can be batched as separate runs if both are large.
2. Process one batch fully: auto-reconcile the matches, raise AskUserQuestion only on **that batch's** divergences. Then **checkpoint** - append the batch's findings to the report, confirm the writes actually landed (Step A5b - re-read the target file or `git diff --stat`, do not report from intent), record progress in `state.json` (`reconcile.areas[].batches_done` / `batches_total`), and report: `batch N/M done - X divergences resolved, Y open`.
3. The user can stop after any batch. `/pm-reconcile-status` shows batch progress; re-running `/pm-reconcile [area]` **resumes at the next un-done batch** and does not re-reconcile completed batches.

This bounds the AskUserQuestion load per batch (not by the whole area's volume) and keeps each sitting reviewable. The area's `status` becomes `done` only when its last batch is checkpointed.

## Step A4: Append to the Reconciliation Report

Append this area's section to the living `reconcile/reconciliation_report.md` (do not overwrite other areas' sections).

## Step A5: Rebuild this area's register (reconciled mode)

Drive the existing skill - do not duplicate its template:
- **domain** → `/pm-entity-registry` (reconciled mode) → `entities.md` (entities, attributes, state-machine structure) + `/pm-glossary` for aliases.
  **Also offer the higher-level map:** ask via AskUserQuestion (default **Yes** for a rebuild - a new team benefits) whether to generate `domain-model.md` too via `/pm-domain-model` (reconciled mode) - the cross-domain ERD and domain boundaries, derived from the same reconciled entities. The two are complementary: the Reconciliation Report is the audit ("what conflicted, how we ruled"); the domain model is the structural map ("how it all fits together"). Skip only if the user declines.
- **rules** → `/pm-business-rules-library` (reconciled mode) → `business_rules.md` + `decision_models.md`; also writes the reconciled guard conditions onto the transitions in `entities.md`. Rules with an open `DIV-NN` stay `Draft` linked to the report; divergence-free rules go `Final`.
- **features** → `/pm-reverse-extract` (reconciled mode) → `feature_list.md` + stub cards. Features normalized to FDD grammar, grouped into `FS-NN`, Section 1 linked to register BR-IDs; code-only features included; **doc-only / specified-not-implemented capabilities are carded as `1_Backlog` stubs** (marked `specified in source, not yet implemented`) so the backlog is complete and survives source disposal - recorded in the report too, but the card in feature_list is the durable home, not the report. Aspirational notes that are not a real client-valued capability stay report-only.

  **Right-sizing legacy features (apply the semantic atomicity test):** legacy systems are often mis-granular. Reconcile each to one coherent client-valued function:
  - **Too granular** (several legacy "features" are really nuances of one capability, e.g. *login*, *register*, *reset password* under *authenticate user*) → consolidate them under one rightful Feature and capture the granular bits as **Subtasks** (helper notes) on that card. They are not lost, not kept as pseudo-features.
  - **Too big** (a legacy feature carries two independent results) → split into separate Features.
  - Record every merge/split in the Reconciliation Report (Section: feature regrouping) so the team can trace where each legacy item went.

## Step A5b: Confirm the write landed (mandatory gate before any "done" claim)

Never report a batch, area, or file as updated based on stated intent. After driving a downstream skill's write in Step A5, re-read back the actual target file(s) (`entities.md` / `business_rules.md` / `decision_models.md` / `feature_list.md` / cards / `domain-model.md`) or run `git diff --stat` against the workspace and confirm the expected files actually show as changed with the expected content. If a claimed write did not land, redo it before proceeding - do not move on and do not checkpoint. This applies at every granularity: per-batch checkpoints (Step A3) and per-area completion (Step A6) both require this confirmation, not a memory of what was planned.

## Step A6: Update status + Notion

Set this area `status: done` in `state.json reconcile.areas[]` (record `divergences_open` count) and tick it in `reconciliation_plan.md` - only after Step A5b confirms the writes actually landed. Push this slice to Notion via the downstream skill's existing logic if a target is configured (`notion_ids.<key>` convention; never invent columns).

Close with: what this area produced, open divergences, and the next area command (or "all areas done - run /pm-reconcile-status").

---

# ===== VERIFY MODE (source-disposal gate) =====

Runs on `/pm-reconcile verify [area]`. The closing pass of a rebuild: before the team throws the legacy source away, prove that **everything in it survived the transposition** - and **incorporate whatever did not**. This is not a fresh report for its own sake; the report is the orientation layer, the value is closing the gaps. Without this pass the source is discarded on faith that the earlier reconcile was perfect.

**Run it when** all reconcile areas are `done` and the team is about to retire the legacy source. Re-runnable - re-running after fixes re-checks and shrinks the gap list.

## Step V0: Locate source + registers, set scope

- Ask where the legacy source lives (source-agnostic - see "The source is whatever the user points to"). Default to the source folder recorded in `reconciliation_plan.md` if present, but let the user redirect or add to it.
- Confirm the rebuilt registers exist (`entities.md`, `business_rules.md`, `decision_models.md`, `feature_list.md` + cards). If a register is missing, that area was never reconciled - say so and route back to `/pm-reconcile [area]` first; do not "verify" a non-existent target.
- Determine scope (default all; `verify domain | rules | features` scopes to one layer).

**Interaction:** Group related questions (2-4 per round) and confirm before moving on. For any A/B/C/D choice, use the AskUserQuestion tool with one option marked **(Recommended)** - never print options as plain text. Keep open-ended questions free-text (don't fake options). If the user is unsure, propose 3-4 concrete options plus "Other". Surface an assumption the moment you make one; never fabricate to fill a gap. (Full standard: CLAUDE.md.)

## Step V1: Deep re-ingest the source

Re-read the source **to full depth** (Deep source ingestion standard) - recursively, following every overview/master table down to its per-item detail files. Do not lean on the earlier reconcile's notes; read the source itself again. State coverage: "Re-read N source files across M folders." This independent re-read is the whole point - it catches what the first pass skipped.

## Step V2: Enumerate source units + 3-way diff

Break the source into its atomic units in scope - each business rule, decision, constraint, entity/state, requirement, feature. For every unit, locate where it landed and check it against the **asymmetric truth** (same model as reconcile):

| Dimension | Checked against | Truth |
|---|---|---|
| **Business logic** (rule values, decisions, constraints, *what/why*) | `business_rules.md` / `decision_models.md` / entity states | **Source wins** - a missing or altered rule is a gap/divergence |
| **Structure** (entity/attribute/enum/state names, what exists) | the codebase | **Code wins** - register must match code |
| **Technical accuracy** (does the transposed artifact match how the code really behaves) | the codebase | **Code wins** - flag transposed logic the code contradicts |

Classify every unit:

| Status | Meaning |
|---|---|
| ✅ **Covered** | Carded / transposed and consistent: a built capability with its card, a rule in the register, **or a specified-not-implemented capability carded as `1_Backlog`**. Built or backlog - either way it has a durable home. |
| ❌ **Not transposed** | In the source, absent from the registers **and from feature_list** - a real gap. **A capability that exists only in the reconciliation report (not carded) counts as a gap**, not as covered: the report is an audit log, the backlog is feature_list. |
| ⚠️ **Transposed but conflicts code** | Landed, but the code does something else → `DIV-NN` |
| 🔄 **Transposed but altered/incomplete** | Landed with wrong value or partial logic vs source |
| ⛔ **Intentionally dropped** | The team explicitly confirmed this is out of scope / abandoned - not a gap. **Not to be confused with `specified, not implemented`** (that is real backlog → card it `1_Backlog`, status ✅). ⛔ is only for things deliberately not carried forward. |

Batch by feature set / rule category for large sources (reuse Step A3 checkpointed batching - bound the question load per batch, record `verify.batches_done/total`).

## Step V3: Coverage report (informational layer)

Write `reconcile/coverage_report.md` (template below) - the traceability surface: every source unit → where it landed or why it did not. This is read-only orientation; it does **not** replace incorporation.

```
COVERAGE: [N] source units - ✅ [x] covered  ❌ [x] gaps  ⚠️ [x] conflicts  🔄 [x] altered  ⛔ [x] dropped
```

## Step V4: Incorporate the gaps (the point of this mode)

A report alone changes nothing. For every non-covered unit, close it - with confirmation, never silently:

| Finding | Incorporation |
|---|---|
| ❌ **Not transposed** | Propose the artifact it should become - business logic that runs → new `BR-NN` / `TBL-NN` / entity state; a **specified-not-implemented capability → a `FEAT-ID` card at `1_Backlog`** (marked `specified in source, not yet implemented`); a nuance → a Subtask on an existing card. Confirm via AskUserQuestion, then **write it into the register / feature_list / card**. Carding the unbuilt capability in feature_list (not just the report) is what makes it safe to discard the source. |
| 🔄 **Altered / incomplete** | Show source value vs transposed value, propose the correction, confirm, **fix the register/card** to match the source's intent. |
| ⚠️ **Conflicts code** | Assign `DIV-NN`, surface via AskUserQuestion (code-bug vs source-stale), record the ruling in the Reconciliation Report. Code is never changed - only the doc/register, per policy. |
| ⛔ **Dropped** | Confirm once it was an intentional drop; record it so it is not re-flagged next run. |

Use the grouped AskUserQuestion pattern (2-4 per round). Apply the same write-paths as reconcile: registers via their owning skills (`pm-business-rules-library`, `pm-entity-registry`, `pm-reverse-extract`), feature_list + cards kept in parity, Notion synced via `notion_ids.<key>`. **Never change the codebase.** Append every incorporation and every `DIV-NN` to `reconciliation_report.md`.

## Step V5: Disposal-readiness verdict

After incorporation, re-run V2 on the affected units and render the verdict:

```
SOURCE-DISPOSAL READINESS - [source name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source units:   [N]
Covered:        [x]   Incorporated this pass: [x]
Open gaps:      [x]   (listed in coverage_report.md)
Open DIV-NN:    [x]   (team must rule before disposal)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERDICT: [✅ Source fully captured - safe to archive
        | ⚠️ NOT safe - [x] gaps / [x] divergences open, resolve then re-run /pm-reconcile verify]
```

Only a **fully covered, zero-open-gap, zero-open-divergence** state earns "safe to archive". Anything else: the source stays, list what is open, point at re-running verify after the team rules on the divergences. The gate never says "safe" on faith.

---

## Reconciliation Plan template

Save to: `pureinn-workspace/[project-slug]/reconcile/reconciliation_plan.md`

```markdown
# Reconciliation Plan - [Product Name]

> **Scope:** [whole product / domain-by-domain]
> **Source-of-truth policy:** [chosen]
> **Generated:** [date]  **By:** pm-reconcile v[version]

## Areas (in execution order)

| # | Area | Command | Source docs | Code locations | Target artifact | Status |
|---|---|---|---|---|---|---|
| 1 | domain | `/pm-reconcile domain` | [domain_model.md, entities.md] | [app/models, db/schema] | domain/entities.md (R1) + domain-model.md (ERD, offered) | pending |
| 2 | rules | `/pm-reconcile rules` | [BRD.md §rules, decision_tables.md] | [services, validators] | business_rules.md + decision_models.md (R2-3) | pending |
| 3 | features | `/pm-reconcile features` | [FSD/*, feature_list.xlsx] | [routes, controllers] | features/feature_list.md + cards (R4) | pending |

## Notes
- [anything that affects ordering or batching]
```

## Reconciliation Report structure (living, appended per area)

Save to: `pureinn-workspace/[project-slug]/reconcile/reconciliation_report.md`

Header (written by Plan mode): purpose, scope, policy, date. Then one section appended per area pass:

```markdown
## [Area] reconciliation - [date]

### Naming & structure drift (auto, code = truth)
| Concept | Old doc name | Canonical (code) | Alias |
### Business-logic divergences
| ID | Topic | Doc says | Code does | Ruling | Action for team |
| DIV-01 | ... | ... | ... | [code bug / doc stale] | [fix code / update rule] |
### Decisions made (AskUserQuestion log)
### Specified but not implemented (→ backlog)
### Undocumented in code (→ confirm intent)
### Feature regrouping (features area only - merges/splits, where each legacy item went)
### Open questions for the team
```

## Coverage Report structure (verify mode)

Save to: `pureinn-workspace/[project-slug]/reconcile/coverage_report.md`

```markdown
# Source Coverage Report - [Product Name]

> **Source verified:** [name / folder the user pointed to]
> **Scope:** [all / domain / rules / features]
> **Generated:** [date]  **By:** pm-reconcile verify v[version]
> Re-read [N] source files across [M] folders.

## Verdict: [✅ safe to archive / ⚠️ not safe - N open]
Covered [x] / [N]  ·  gaps [x]  ·  conflicts [x]  ·  altered [x]  ·  dropped [x]

## Traceability
| Source unit (doc §) | Status | Landed at | Action |
|---|---|---|---|
| [BRD §4.2 refund window] | ✅ covered | BR-ORD-003 | - |
| [BRD §7 loyalty tiers] | ❌ not transposed | - | incorporated → TBL-LOY-01 (confirmed) |
| [FSD §3 cancel flow] | ⚠️ conflicts code | BR-ORD-009 | DIV-12 → team rules |
| [spec §2 grace period] | 🔄 altered | BR-ORD-005 | corrected 7d → 14d (source) |
| [old wiki: SMS reminders] | ⛔ dropped | - | intentional (not implemented) |

## Open before disposal
- [gaps + DIV-NN that must be closed first]
```

## state.json schema

```json
"reconcile": {
  "plan_created": true,
  "policy": "code-structure/docs-business/ask-conflicts",
  "scope": "domain-by-domain | whole-product",
  "areas": [
    {"area": "domain",   "order": 1, "target": "domain/entities.md",        "status": "done",        "divergences_open": 0, "batches_done": 1, "batches_total": 1},
    {"area": "rules",    "order": 2, "target": "domain/business_rules.md",   "status": "in_progress", "divergences_open": 2, "batches_done": 2, "batches_total": 5},
    {"area": "features", "order": 3, "target": "features/feature_list.md",   "status": "pending",     "divergences_open": 0, "batches_done": 0, "batches_total": 0}
  ],
  "verify": {
    "last_run": "2026-06-28",
    "scope": "all",
    "units_total": 0, "covered": 0, "gaps_open": 0, "divergences_open": 0,
    "batches_done": 0, "batches_total": 0,
    "disposal_ready": false
  }
}
```
`status` ∈ `pending | in_progress | done`. On full completion also set `registers.reconciled: true`, `registers.feature_list_initialized: true`, `current_phase_index: 6`. The `verify` block is written by VERIFY MODE; `disposal_ready: true` only when gaps and divergences are both 0.

---

## Handoff

---
**Čo si teraz má:** [Po PLANE] plán rekonciliácie - ktoré oblasti, v akom poradí, do akej Pureinn štruktúry. [Po oblasti] tá vrstva je zladená s kódom, jej sekcia je v Reconciliation Reporte, register prestavaný.

**Ďalší krok:** `/pm-reconcile [ďalšia oblasť podľa plánu]` — pokračuj v poradí.
Stav kedykoľvek cez `/pm-reconcile-status`.

**Po dokončení všetkých oblastí - obsah pred formou:** najprv **`/pm-reconcile verify`** → posledná kontrola voči zdroju: dokáže že všetko zo zdroja je preklopené, **medzery doplní** (pridá nové BR/TBL/entity/FEAT), a vynesie verdikt či môžeš zdroj zahodiť (source-disposal gate). Až keď je obsah kompletný → `/pm-product-roadmap` (fázy nad celým setom) → `/pm-audit` (forma, naming, metadata, descriptions - **vrátane toho čo verify dorobil**) → `/pm-stripe` (JIT delivery).
Reconciliation Report prejdi s tímom kvôli otvoreným divergenciám.

**Prečo verify pred auditom:** verify **mení obsah** (zapracováva medzery), audit je forma nad stabilným setom. Audit-first by znamenal auditovať neúplnú množinu a po verify auditovať znova. Poradie: **obsah (`verify`) → plán (`roadmap`) → forma (`audit`) → archív zdroja** (disposal verdikt padá na verify - audit zdroj nečíta, nič z neho nestratí).

**Pozor - Rebuild nezachytil strategickú vrstvu:** preskočil si Phase 1-3, takže vízia / NSM / biznis model / success kritériá fáz neexistujú. `/pm-product-roadmap` ti preto postaví **delivery-driven** roadmapu (hranice fáz diktuje rozostavanosť kódu, nie stratégia). Ak chceš **strategy-driven** fázovanie (MVP hranica podľa toho čo biznis musí dokázať), backfilluj strategickú vrstvu lean **pred** roadmapou: `/pm-business-model` (ak je zapojený PSP ako Stripe, take-rate model je knowable teraz - nedeferuj ho) + NSM + 12-mes. cieľ. Inak pusti roadmapu rovno a strategickú vrstvu nechaj TBD.

**Môžeš preskočiť ak:** žiadne staré docs neexistujú (len kód) — vtedy stačí naivná migračná cesta (`/pm-entity-registry` + `/pm-business-rules-library` + `/pm-reverse-extract`) bez rekonciliácie.
