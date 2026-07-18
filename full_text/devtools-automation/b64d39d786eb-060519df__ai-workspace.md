---
name: ai-workspace
description: >-
  Create, review, audit, and validate AI workspaces for agent hosts such as
  Codex, Copilot, Gemini, and similar desktop or CLI runtimes. Use when the user
  asks to design an agent-ready repo, scaffold AGENTS.md and event handlers,
  create an API-backed or domain knowledge workspace, audit AGENTS.md or
  SKILL.md quality, or improve how a repo exposes behavior to coding agents.
---

# AI Workspace

Create or review AI workspaces operated by agent hosts and humans.

An AI workspace makes behavior visible through files:

- `AGENTS.md` or host-equivalent root instructions as the workspace contract;
- `data/` for local evidence, dated snapshots, and layered durable knowledge
  state;
- `process/` for event handlers that create or update state;
- `my-work/` for dated working notes, reports, briefings, and generated
  deliverables when the workspace supports recurring analysis;
- optional `output/` for simple generated views when the repo already uses that
  convention or no dated work area is needed;
- optional `skills/` for host-discoverable reusable workflows;
- optional `scripts/` only for deterministic logic that host tools cannot do
  well;
- a simple validation flow that proves the main event path works.

The default execution model borrows AppRun's event/data/handler shape:

```txt
event + current state -> event handler -> new or updated state
```

Events can come from user requests, cron/timer triggers, scheduled reviews, file
or data changes, API/webhook/input updates, validation runs, audit runs, or
manual decisions. Classify the event, load the smallest relevant
event handler defined under `process/`, read the necessary current state, perform
documented effects, then create or update state in `data/`, render dated work
under `my-work/` or simple output under `output/`, or respond directly.

Prefer `AGENTS.md + data/ + process/ + my-work/` for domain workspaces that use
local records, recurring evidence, domain objects, or briefing outputs. Use
`output/` only for lighter workspaces or existing repo conventions.

Add skills only when host skill discovery, reuse, packaging, or a triggerable
entry point is useful.

## Mode

Classify the request first:

- Create: design, scaffold, patch, or improve a workspace.
- Review/audit: inspect and report gaps. Stay read-only.
- Validate: run or describe checks and say what passed.

Mixed request order:

1. Review current state.
2. Explain gaps.
3. Edit only the requested parts.

## Architecture Choice

Choose the smallest structure that preserves the workspace contract.

Root/process workspace:

```txt
AGENTS.md
data/
process/
my-work/
```

Use this when root instructions, durable data, event handlers, and generated
outputs are enough.

Evidence-backed knowledge workspace:

```txt
AGENTS.md
data/{partition}/{yyyy}/{mm}/{dd}/<object-type>/<id>/<object-id>-data.json
data/{partition}/{yyyy}/{mm}/{dd}/<object-type>/<id>/<object-id>-source.md
data/{partition}/{yyyy}/{mm}/{dd}/<object-type>/<id>/<object-id>-summary.md
data/{partition}/daily-triage/{yyyy}/{mm}/{dd}/accumulated-actions-{yyyy-mm-dd}.json
data/{partition}/daily-triage/{yyyy}/{mm}/{dd}/actions-{yyyy-mm-dd}.md
process/source.md
process/distillation.md
process/summary.md
process/memory.md
process/tension.md
process/insight.md
process/action.md
process/accumulated-actions.md
process/<scenario>.md
my-work/{yyyy}/{mm}/{dd}/
my-work/{yyyy}/{mm}/{dd}/output/
```

Omit `{partition}` only when the domain has no team, tenant, business unit,
source system, workspace, or other durable partition.

When daily distillation is expected, the dated bucket is the canonical write
path for each run. Do not use `current/` as the only record of daily judgment;
use it only as an optional latest view that points to or copies the dated
artifact.

Use this when the domain has local exports, record-like data, dated snapshots,
object-level evidence, recurring triage, scenario analysis, briefing decks, or
reviewable reports. This is the default when the user asks for a workspace
similar to `../crm-ai-workspace`.

API-backed workspace:

```txt
AGENTS.md
data/
process/api.yaml
process/api.md
process/<event-handler>.md
data/api-responses/
my-work/
```

Use this when event handlers call an external API as a documented effect.
Add `scripts/` only when `AGENTS.md` or `process/*.md` references them.

Optional skill wrapper:

```txt
skills/<skill-name>/SKILL.md
skills/<skill-name>/references/
skills/<skill-name>/scripts/
skills/<skill-name>/fixtures/
```

Use this only when a workflow benefits from host skill discovery, reuse,
packaging, or a triggerable entry point. Do not hide workspace event handlers
inside a skill folder.

Do not create `README.md`.
Use `AGENTS.md` and `process/*.md` for workspace contracts.

Use minimal generated docs:

- base `AGENTS.md` must describe only real workspace folders and handlers;
- add API rules only when API files are created;
- add script rules only when script files are created;
- do not mention `skills/`, `scripts/`, API files, docs, `output/`, or optional
  deliverables unless they exist and are part of the workspace contract.

## Workspace Contract

`AGENTS.md` is the always-on workspace contract: the root agreement that tells
an agent host what this workspace is for, where state lives, which handlers own
behavior, and what outputs or effects are allowed.

It must define:

- workspace purpose and non-goals;
- the workspace shape: `AGENTS.md + data/ + process/ + my-work/` or the
  lighter documented alternative;
- the execution model: `event + current state -> event handler -> new or
  updated state`;
- host assumptions;
- where durable knowledge, behavior rules, and generated views belong;
- how to choose an event handler;
- when handlers may write to `data/`, `my-work/`, or `output/`;
- external effect and write approval boundaries;
- validation expectations.

For evidence-backed knowledge workspaces, `AGENTS.md` must also define:

- the evidence boundary: live systems, local exports, user-supplied files, API
  responses, or generated `source.md` snapshots;
- the domain question or decision every synthesis must support;
- the object types and stable ID source;
- the partition rule, if any;
- the dated storage layout for raw data, `source.md`, and `summary.md`;
- that `summary.md` owns `## Proposed Actions` and no standalone `action.md`
  is created by default;
- whether deterministic accumulated-action snapshots are maintained from
  `summary.md`;
- the large-batch distillation rule: audit target scope, freeze a manifest,
  split into disjoint batches with a deterministic script, and keep each worker
  to its assigned `summary.md` write set;
- the dynamic work path under `my-work/{yyyy}/{mm}/{dd}/`;
- which concrete deterministic scripts own refresh, source generation, indexing,
  validation, accumulated actions, and posting, or which of those are
  explicitly not applicable;
- that semantic distillation is agent-authored from current `source.md`, not
  script-authored;
- the external write boundary, especially when actions are only local
  recommendations.

Host assumptions:

- the agent host can read workspace files;
- the agent host can write workspace files when requested or when required by
  the selected event handler;
- the agent host can create parent folders;
- the agent host can fetch web content when needed;
- the agent host can call documented tools and APIs when available.

Do not assume a database, background worker, web server, browser UI, or external
service unless the workspace explicitly documents it.

Do not create vague "AI memory" workspaces when the request is really about a
repeatable evidence workflow. Name the domain object, evidence boundary,
judgment step, action boundary, and output path directly.

## Event Handlers

Event handlers are process files under `process/`.
They read current state from `data/`, perform documented effects, and produce
new or updated state, usually persisted back to `data/`. They may also render
dated work under `my-work/`, render simple documented output under
`output/`, or respond directly.

`process/` contains event handlers, not passive documentation.

Each handler should make these parts explicit:

- event sources, event names, or trigger language;
- required `data/` reads;
- allowed `data/` writes;
- state created or updated by the handler;
- allowed tool/API effects;
- output render path, if any;
- direct response behavior;
- validation checks;
- escalation or approval gates.

Use one handler per meaningful workflow boundary. Examples:

```txt
process/ingest.md
process/update.md
process/report.md
process/review.md
process/api.md
process/data.md
process/<object-type>.md
```

For evidence-backed knowledge workspaces, prefer these core handlers:

```txt
process/source.md
process/distillation.md
process/summary.md
process/memory.md
process/tension.md
process/insight.md
process/action.md
```

Add `process/accumulated-actions.md` when proposed actions need deterministic
queue state, carry-forward behavior, removals, triage input, or posting.

Add scenario handlers only when the domain has meaningful recurring lenses:

```txt
process/<scenario>.md
process/daily-triage.md
process/reporting.md
```

Scenario handlers must define trigger language, required evidence, evaluation
rules, questions to answer, layer guidance, and misuse cases. Do not create
empty scenario files to make the tree look complete.

Do not create process files just to fill a tree. Create them when behavior,
state transitions, source policy, output rendering, or external effects need a
stable contract.

## Creation Flow

Treat natural-language creation requests as actionable.
If the request names the domain, use it.
Ask the domain question only when the domain is missing.

Before writing files:

- inspect existing repo conventions;
- identify the host or host family;
- define purpose and non-goals;
- state host capability assumptions;
- map common user requests into events;
- define event handlers for those events;
- ask what domain the knowledge base is for only if missing;
- allow the user to skip domain setup;
- require or infer the domain inputs: object types, stable ID sources, evidence
  sources, partition scheme, scenario lenses, deterministic script needs, and
  external write gates;
- define durable `data/` paths;
- define `my-work/` paths for dated reports, decks, reviews, dynamic analyses,
  and final deliverables;
- define report/deck trigger language and scope mapping when outputs matter;
- define the smallest useful validation flow.

When the user asks for a workspace like `../crm-ai-workspace`, build an
evidence-backed knowledge workspace unless there is a clear reason not to. Use
the other workspace as a structural pattern, not as a domain-specific template:

- source evidence is local and explicit;
- `source.md` is the factual boundary;
- `summary.md` is the combined judgment layer;
- `summary.md` owns supported `## Proposed Actions`; do not create standalone
  `action.md` by default;
- optional `process/accumulated-actions.md` owns deterministic queue state built
  from `summary.md`, including active actions, carries, removals, and readable
  action reports;
- `process/daily-triage.md` reads accumulated-action snapshots and action
  reports, not `*-action.md` files;
- actions are local recommendations, not external tasks or system writes;
- dynamic work lives under dated `my-work/`;
- deterministic scripts are concrete implementation, not vague principles, for
  refresh, source generation, indexing, validation, accumulated actions, and
  posting when those workflows exist;
- large distillation runs use scripts to audit, freeze, split, and load batch
  manifests; agents still author every semantic `summary.md`;
- semantic distillation remains agent-authored from current `source.md`; scripts
  must not draft, template, migrate, or bulk-transform `summary.md`.

When creating a knowledge base:

- use the same human language as the user's request;
- auto-detect vocabulary for category, layer, object type, and object ID labels;
- create `AGENTS.md`, `data/`, `process/`, and `my-work/` for evidence-backed
  workspaces;
- create `output/` only when that is the requested or existing convention;
- create layer event handlers when a domain is known;
- create `process/data.md` with the object-first path formula;
- create a runtime handler when source-to-layer flow matters;
- create object-type handlers when object types are known;
- create seed knowledge files when source docs are domain-level, not
  object-level;
- create a reporting handler when users need natural-language reports, decks, or
  exportable summaries;
- create an accumulated-actions handler when proposed actions need queue,
  removal, carry-forward, triage, or posting state;
- create or name concrete deterministic scripts for refresh, source generation,
  indexing, validation, accumulated actions, and posting when those workflows
  are part of the workspace; document explicit "not applicable" decisions
  instead of generic placeholder script rules;
- create or name large-batch distillation scripts when the workspace may distill
  more objects than one agent should author in one pass: target audit, manifest
  creation/splitting, batch loading, and output validation;
- create concrete object folders only for objects named by the user;
- do not invent object IDs just to fill the tree.

Use:

- `references/creation-rubric.md` for creation checks;
- `references/domain-knowledge-rubric.md` only when a domain is supplied;
- `templates/AGENTS.md` for root instructions, but adapt it to the workspace
  shape;
- `templates/api-guide.md` for API-backed process guidance;
- `templates/domain-knowledge-contract.md` for domain knowledge;
- `templates/data-contract.md` for knowledge folder contracts;
- `templates/source-process.md` for factual evidence snapshots;
- `templates/distillation-process.md` for agent-authored `source.md` to
  `summary.md` orchestration;
- `templates/summary-process.md` for the combined judgment artifact;
- `templates/accumulated-actions-process.md` for deterministic action-queue
  state built from `summary.md`;
- `templates/scenario-process.md` for recurring domain scenarios;
- `templates/daily-triage-process.md` for accumulated-action snapshot
  briefings;
- `templates/runtime-process.md` for source-to-layer workflow handlers;
- `templates/object-process.md` for object-type handlers;
- `templates/reporting-process.md` for natural-language report/deck handlers;
- `templates/report-artifact.md` for readable reports;
- `templates/deck-outline.md` for deck-ready outlines;
- layer templates for semantic layer handlers.

Do not create generic file I/O or web-fetch scripts.
Do not create Python scripts by default.
Use the host's file, shell, and web tools unless a script adds real value.
For CRM-style or other evidence-backed operational workspaces, script value is
real when it provides deterministic refresh, source generation, indexing,
validation, accumulated-action state, or gated posting. Keep judgment out of
scripts.

## Domain Knowledge

Ask:

```txt
What domain should this knowledge base serve?
```

Accept a domain or `skip`.

If the user already supplied a domain, do not ask again.

If skipped:

- do not create layer event handlers.

If supplied, create domain-shaped handlers:

```txt
process/<memory-layer>.md
process/<tension-layer>.md
process/<insight-layer>.md
process/<action-layer>.md
```

Create `process/<runtime-layer>.md` only when source-to-layer flow matters.
Create `process/<object-folder>/<object-type>.md` only when object types are
known and need distinct rules.
Create `process/<reporting-layer>.md` when users can ask for reports,
presentations, reviews, summaries, or exportable status output in natural
language.

Layer meaning:

- `sources`: raw or summarized evidence with provenance.
- `memory`: durable object knowledge.
- `tension`: unresolved pressure, risk, contradiction, or opportunity.
- `insight`: current interpretation and consequence.
- `action`: local recommended next moves.

Use those English names as semantic defaults only.
In created workspaces, localize layer names, object types, categories, section
headings, and path segments to the user's detected language.

For evidence-backed workspaces, keep the semantic layers but default to the
combined artifact model used by `../crm-ai-workspace`:

- `source.md`: factual evidence snapshot with provenance and unknowns.
- `summary.md`: combined judgment containing `Memory`, optional `Tensions`,
  optional `Insight`, optional `Proposed Actions`, `Confidence`, and
  `Review Notes`.
- `process/accumulated-actions.md`: optional deterministic queue state built
  from `summary.md` proposed actions when triage, carry-forward, removals, or
  posting matter.

Use separate `memory.md`, `tension.md`, `insight.md`, and `action.md` process
files as section guides for `summary.md`, not necessarily as separate data
artifacts.

Do not create standalone `action.md` by default. Use it only when the user
explicitly asks for separate action artifacts or the existing workspace already
uses that convention; document the divergence from the CRM-style default.

Keep a vocabulary map in `process/data.md` or the domain contract.
Use stable path names once chosen.

If source docs seed the domain but are not object instances, create a flat seed
knowledge path by default:

```txt
data/<localized-layer>.md
```

Mention that multiple knowledge bases are supported.
Use nested seed paths only when the user asks for multiple knowledge bases:

```txt
data/<localized-knowledge-base-a>/<localized-layer>.md
data/<localized-knowledge-base-b>/<localized-layer>.md
```

Each requested knowledge base needs:

- a stable localized name;
- source document rules;
- layer filename mapping;
- update and overwrite rules;
- routing rules for when to read it.

Do not invent an object ID for seed knowledge.

Actions are not external tasks or writes unless the user approves the exact
external write or the selected event handler explicitly permits the local write.

## Reporting And Output

Support natural-language reporting when the workspace has durable knowledge.

Users may ask for reports with phrases such as:

```txt
report the current status
make a presentation
汇报当前情况
做一份复盘
输出给业务看的 deck
```

Treat each report request as an event.
Map the event into an explicit scope before reading files:

- current status: latest maintained `current/` layers or seed knowledge;
- single object: one object type and object ID;
- object group: named objects, watchlists, cohorts, categories, or queues;
- date or period review: dated source and layer files for a time window;
- custom question: the minimum source and layer set needed to answer it.

If the scope is ambiguous, choose the smallest useful scope and state it.
Ask only when the report could materially change audience, object set, or
external write behavior.

Reports, decks, reviews, and summaries belong under `my-work/` for evidence-backed
workspaces. Use `output/` only when that is the existing or requested convention.

Default paths for evidence-backed workspaces:

```txt
my-work/<yyyy>/<mm>/<dd>/<scope>.md
my-work/<yyyy>/<mm>/<dd>/output/<scope>.marp.md
my-work/<yyyy>/<mm>/<dd>/output/<scope>.pdf
```

Use repo-native export routes:

- Markdown report only when no export tooling exists.
- Marp/HTML/PDF when the repo already uses markdown slide export.
- PPTX when the workspace or host has a presentation runtime.
- Script-backed export only when a deterministic exporter exists or is created
  for a real reason.

Create matching process and template files when reporting is part of the
workspace contract:

```txt
process/<reporting-layer>.md
templates/report-artifact.md
templates/deck-outline.md
```

Reporting event handlers must define:

- natural-language trigger phrases;
- scope mapping rules;
- required source and layer reads for each scope;
- audience and visible-language rules;
- report/deck section order;
- `my-work/` or documented `output/` path and format;
- validation checks for readability and generated files.

Do not let reporting become a detached summary. It must preserve the chain:

```txt
sources -> memory -> tension -> insight -> action -> my-work/output
```

## API Workspaces

For API-backed workspaces:

- use `process/api.yaml` as the route and schema source of truth;
- use `process/api.md` for auth, route selection, error handling, effects, and
  writes;
- create `.env.example` for required variable names when env vars are needed;
- add `.env` to `.gitignore` when local secrets are expected;
- do not create a real `.env` unless the user supplies non-secret values;
- load secrets from environment files, not chat history;
- never print or persist tokens or auth headers;
- require explicit approval before external writes unless the event handler
  explicitly documents a safe local write;
- save durable raw responses under a documented `data/` path.

Use scripts only when deterministic code is materially better than host tools,
such as pagination, joins, normalization, validation, artifact generation, or
repeated processing.

Do not require Python. Use the smallest runtime already natural to the repo.

## File Ownership

Workspace-level files:

- `AGENTS.md`: always-on workspace contract.
- `data/`: durable source evidence and knowledge state.
- `process/`: event handlers and workspace-level operating contracts.
- `process/<reporting-layer>.md`: report/deck scope mapping and render flow
  when output workflows exist.
- `my-work/`: dated dynamic work such as briefings, analyses, reports,
  and reviews.
- `my-work/{yyyy}/{mm}/{dd}/output/`: final generated deliverables for that
  dated run.
- `my-work/{yyyy}/{mm}/{dd}/output/scratch/`: previews, generated support files,
  and intermediate render artifacts.
- `output/`: optional simple generated views only when the repo already uses
  that convention or the workspace does not need dated work.
- `scripts/`: only when referenced by `AGENTS.md` or `process/*.md`.

Skill-level files:

- `skills/<skill-name>/SKILL.md`: triggerable workflow.
- `skills/<skill-name>/references/`: long skill guidance.
- `skills/<skill-name>/scripts/`: scripts referenced by that skill.
- `skills/<skill-name>/fixtures/`: optional examples or script inputs.

Do not move workspace-level process files, scripts, `data/`, or `my-work/`
artifacts into a skill folder.

Do not move skill-owned artifacts into the repo root.

Generated file maps must be exact.
Do not reference `skills/`, `scripts/`, `.docs/`, or `docs/` unless they exist
and are part of the workspace contract.
Do not create or reference `README.md`.

## Evidence-Backed Knowledge Pattern

Use this pattern when the workspace needs repeatable analysis over local records,
exports, API snapshots, uploaded files, generated source files, or other
reviewable evidence. Keep the pattern domain-generic: it can serve research,
support, education, projects, knowledge bases, audits, content pipelines, or any
object-oriented evidence workflow.

Required decisions:

- domain question: what decision, interpretation, or output every synthesis
  should support;
- object types and stable ID source for each object type;
- partition scheme: team, tenant, business unit, source system, workspace, or
  explicit no-partition decision;
- evidence boundary: local exports, generated sources, API responses, uploaded
  files, or user-supplied evidence;
- source evidence locations and freshness/refresh policy;
- source refresh rule: when to regenerate or reuse `source.md`;
- daily distillation rule: whether every run writes a dated snapshot, what
  counts as "today", and whether `current/` is only a latest view;
- large-batch distillation rule: target audit, manifest path, batch size,
  splitting script, worker write ownership, and parent validation;
- lookup rule: whether domain facts live in file contents or filenames;
- object resolution rule: exact phrase, token variants, stable ID, ambiguity
  handling, and no-match behavior;
- layer chain: `source -> summary`, with `summary.md` owning proposed actions;
- accumulated-action rule: whether proposed actions in `summary.md` feed
  deterministic queue snapshots and readable action reports;
- scenario lenses: recurring domain situations worth their own process files;
- triage rule: whether daily triage reads accumulated snapshots, action reports,
  or no queue state;
- output rule: written brief, Marp/PDF, PPTX, or Markdown only;
- deterministic scripts: concrete refresh, source-generation, index,
  validation, accumulated-action, and posting scripts, or explicit "not
  applicable" decisions for each;
- external write gates: exact routes, payload shape, environment gates, dry-run
  behavior, and approval boundary.

Default dated object layout:

```txt
data/{partition}/{yyyy}/{mm}/{dd}/<object-type>/<id>/<singular-object-type>-<id>-data.json
data/{partition}/{yyyy}/{mm}/{dd}/<object-type>/<id>/<singular-object-type>-<id>-source.md
data/{partition}/{yyyy}/{mm}/{dd}/<object-type>/<id>/<singular-object-type>-<id>-summary.md
```

Omit `{partition}` only when the workspace explicitly has no partition.
Use this layout when local exports or snapshots change over time. Use
`current/` instead only when the domain does not need historical snapshots.
If the workspace needs daily distillation, use dated folders even when a
`current/` view is also maintained.

`source.md` rules:

- factual only;
- generated or refreshed before judgment;
- captures provenance, material fields, evidence inventory, unknowns, and
  limits;
- no unsupported predictions, recommendations, or labels.

`summary.md` rules:

- grounded in the same-run `source.md`;
- contains always-present `Memory`, `Confidence`, and `Review Notes`;
- contains `Tensions`, `Insight`, and `Proposed Actions` only when supported;
- preserves checkbox state for still-supported proposed actions;
- proposed actions are local recommendations inside `summary.md`, not external
  tasks or writes;
- expires with a documented TTL.

Accumulated-action rules:

- create `process/accumulated-actions.md` only when queue state matters;
- read dated `summary.md` artifacts and their `## Proposed Actions` sections;
- write deterministic snapshots and readable action reports under a documented
  `data/{partition}/daily-triage/{yyyy}/{mm}/{dd}/` path;
- removals require source-backed transitions such as checked actions, inactive
  summaries, summaries with no supported actions, or changed action text;
- do not infer removals from silence;
- checkboxes are local planning state only.

Search rules:

- if the workspace documents that domain facts are stored inside files, search
  contents first and use listings only for known IDs or storage traversal;
- search exact phrases first, then token variants;
- when known sibling layer paths are selected, read them together in one command;
- do not infer missing coverage from absent filenames.

Scripts:

- for evidence-backed operational workspaces, create or require concrete
  deterministic scripts for refresh, source generation, indexing, validation,
  accumulated actions, and posting when those workflows exist;
- allow scripts for deterministic export expansion, source generation,
  normalization, indexing, validation, accumulated-action snapshots, posting
  dry-runs, or repeatable artifact generation;
- use scripts to prepare evidence, audit target coverage, freeze and split
  batch manifests, load assigned batches, validate structure, rebuild
  deterministic state, and perform gated external writes;
- use agents for semantic distillation from `source.md` to `summary.md`;
- never use scripts, templates, migrations, or bulk transforms to draft,
  rewrite, or "seed" judgment inside `summary.md`;
- document the owning handler for every script;
- never create scripts that merely wrap generic file reads, file writes, folder
  creation, or web fetching.

Triage:

- use triage only when the workspace has proposed actions or accumulated queue
  state;
- prefer deterministic accumulated-action snapshots and readable action reports;
- read dated `summary.md` files directly only when accumulated state is missing,
  stale, or the workspace intentionally skipped queue state;
- deduplicate repeated objects by newest supported snapshot or accumulator row;
- rank by domain importance and immediacy;
- create a written brief under `my-work/{yyyy}/{mm}/{dd}/`;
- create a deck/PDF only when the workflow promises one or the user asks.

Create or reference source-doc folders only when the user supplies source docs,
asks for them, or the existing workspace already uses them.

If a folder is optional, omit it from generated docs by default.

## Script Rules

Scripts are behind-the-scenes implementation details. Most small workspaces
should not need them, but evidence-backed operational workspaces often do.

Execution path:

```txt
event + current state -> event handler -> host tool call -> referenced script -> new or updated state
```

Users should not run scripts directly.

Scripts must:

- accept structured inputs;
- be deterministic where feasible;
- be host-invokable;
- document what is script-owned and what remains LLM-owned;
- document which handler invokes them.

For CRM-style evidence workspaces, the standard script ownership split is:

- refresh/download script: fetch or expand local raw evidence;
- source-generation script: create factual `source.md` from raw evidence;
- index script: rebuild routing/search indexes from durable local state;
- validation script: validate `source.md`, `summary.md`, and output contracts;
- distillation-batch scripts: audit missing/stale targets, create a fixed
  manifest, split that manifest into disjoint batches, and load assigned source
  paths for agents;
- accumulated-action script: derive queue snapshots and readable action reports
  from `summary.md`;
- posting script: perform dry-run and gated external writes.

If one of these is not needed, document why. Do not replace concrete scripts
with vague prose when repeatability, scale, validation, or external writes
matter.

## Data And Output Rules

For knowledge bases, use object-first data paths. For evidence-backed workspaces
with dated local snapshots, prefer the dated bucket first:

```txt
data/{partition}/{yyyy}/{mm}/{dd}/<localized-object-type>/<object-id>/<singular-object-type>-<object-id>-source.md
data/{partition}/{yyyy}/{mm}/{dd}/<localized-object-type>/<object-id>/<singular-object-type>-<object-id>-summary.md
```

For simpler knowledge bases, use:

```txt
data/<localized-object-type>/<object-id>/<yyyy>/<mm>/<dd>/<localized-layer>.md
data/<localized-object-type>/<object-id>/current/<localized-layer>.md
```

Use dated folders only when the workspace needs history:

- source evidence changes over time;
- the workspace needs daily distillation or daily auditability;
- snapshots must be preserved;
- time windows affect interpretation;
- `current/` needs a traceable source snapshot.

If date tracking is not needed, use the stable seed path or `current/` path and
document why dated snapshots are omitted.

Required semantic layers:

```txt
sources
memory
tension
insight
action
```

Localize filenames for those meanings unless the user or existing repo uses
English.

Do not use:

```txt
data/<object>/<yyyy>/<mm>/<dd>/<localized-category>.md
```

That path loses object type, object ID, and layer meaning.

If category is needed, treat it as a view:

```txt
data/<localized-category>/<localized-object-type>/<object-id>/<yyyy>/<mm>/<dd>/<localized-layer>.md
```

Always define:

- path formula;
- whether date tracking is required;
- date source when dated folders are used;
- partition rule or explicit no-partition decision;
- object type and ID source;
- detected language;
- vocabulary map;
- allowed layers;
- proposed-action storage rule inside `summary.md`;
- accumulated-action queue paths when queue state exists;
- parent folder creation;
- overwrite or version rule.

For reports and decks, always define:

- natural-language trigger phrases;
- scope mapping;
- source/layer read set;
- output format;
- export chain;
- `my-work/` or documented `output/` path;
- validation check.

## Review / Audit

Classify the target:

- file: one `AGENTS.md`, `SKILL.md`, prompt, script, or reference;
- process: one or more `process/` files;
- output flow: report/deck scope mapping, templates, and export chain;
- skill: one skill directory;
- workspace: full repo-level agent surface.

Inspect only what the target requires.

Use `references/audit-rubric.md` when it is relevant, but audit against this
workspace contract first.

Report findings first.

Audit for these workspace invariants:

- `AGENTS.md` defines `AGENTS.md + data/ + process/ + my-work/` or a lighter
  documented shape;
- user requests, cron/timer triggers, scheduled reviews, data changes, API
  updates, validation runs, audit runs, and manual decisions are
  treated as events when they drive workspace behavior;
- `process/` files act as handlers, not generic docs;
- event handlers define event source or trigger language, data reads, state
  writes, effects, output paths, direct response behavior, and validation;
- durable knowledge is in `data/`;
- behavior rules are in `process/`;
- generated work and deliverables are in `my-work/` unless a documented
  `output/` convention applies;
- external services are not assumed unless documented;
- external writes require explicit approval or a documented safe handler rule;
- file maps list only existing folders;
- validation proves an event-to-handler-to-state path, not just static
  structure.

Do not redesign unless the user asks.

## Validation

Validation is stronger than inspection.

Do not say validated unless behavior was checked.

Levels:

- structural: required files exist;
- contract: instructions, handlers, data paths, and output paths agree;
- execution: the main event ran through the selected event handler under
  `process/`;
- data: expected `data/` files were read or updated;
- output: expected `my-work/` or `output/` files were created in the documented
  format and path;
- export: report/deck files were created in the documented export format and
  path.

Say:

- what was inspected;
- what event path was checked;
- what ran;
- what passed;
- what remains unverified.

## Reports

Audit report:

```txt
Summary
Scope
Inspected Files
Findings
Gaps
Validation Status
Recommended Next Steps
```

Creation report:

```txt
Summary
Files Created Or Changed
Host Capability Assumptions
Workspace Layout
Event Model
Event Handlers
Data And Output Paths
Optional Skills
Validation Status
Remaining Gaps
```
