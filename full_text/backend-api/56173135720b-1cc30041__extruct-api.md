---
name: extruct-api
description: Run explicit Extruct API tasks through the bundled Extruct CLI. Covers Deep Search, Deep Research on companies and people, semantic search, lookalike search, company and people tables, column operations, enrichment, and contact finding.
---

# Extruct API

Use `<extruct_api_cli>` for supported Extruct operations. Do not construct raw HTTP requests for operations the CLI already supports.

Extruct AI is a company discovery and research platform for finding, enriching, and evaluating companies. Its core workflows are semantic search, lookalike search, and Deep Search for company discovery, plus AI Tables for repeatable company and people enrichment, scoring, and contact-finding workflows.

## Source Of Truth

Use the bundled CLI and the instructions in this skill as the default path.

When behavior is unclear, when the user asks for a capability that may not be covered here, or when the request may depend on recently changed API behavior, consult the official Extruct API reference as the source of truth:

- https://www.extruct.ai/docs/api-reference/introduction

Decision rule:
- if the CLI already supports the operation, use the CLI
- if the CLI does not cover the operation or the documented behavior here conflicts with the live API, defer to the official API docs

## Resolve The Bundled CLI First

`<extruct_api_cli>` means the absolute path to the bundled CLI script for this skill.

- Resolve it from the directory that contains this `SKILL.md`.
- In shell or Bash tool calls, prefer the resolved absolute path, not `scripts/extruct-api` relative to the workspace root.
- All command examples below use `<extruct_api_cli>` as shorthand for that resolved absolute path.

Example:

```bash
/absolute/path/to/skills/extruct-api/scripts/extruct-api auth user
```

## Core Workflow

This section covers the default operating intent of the skill: identify the Extruct object the user is working with, choose the right execution path, inspect before mutating, and use the CLI to carry the task through to completion.

1. Resolve `<extruct_api_cli>` first, then establish account and billing context. Before the first authenticated CLI call in a conversation, run `<extruct_api_cli> auth user` to get the user and subscription snapshot. If it fails, run `<extruct_api_cli> healthcheck` to distinguish credential problems from connectivity issues.
2. Classify the request into the right Extruct path:
   - if the user provides an Extruct table URL or a raw table UUID, treat it as an existing table operation first
   - if the user provides an Extruct task URL or a raw task UUID, treat it as an existing Deep Search task first
   - known company lookup: fetch the canonical company profile for one domain or UUID
   - company discovery: semantic search, lookalike search, or Deep Search
   - research report: Deep Research for a deep, cited report on one target — a company, a person, or a team
   - existing table operation: inspect, add/update rows or columns, run, poll, read
   - company-table workflow: enrich or score companies in a reusable table
   - people workflow: find people at companies or enrich existing people rows
3. If the user already has a table or task, inspect it before mutating it. Default inspection is `tables get`, `columns list`, and a small `tables data` page. On `company` tables, inspect `company_profile` on the first read before adding standard company-fact columns. When you only need a surgical read, add `--columns` on the first `tables data` call instead of fetching the full row payload.
4. Start from the inline command and payload examples in this file. If a payload spans more than a few lines, prefer `--payload-file`. Read `references/column-guide.md` before designing or changing columns.
5. Carry async work through to completion with `tables poll` or `deep-search poll`, then summarize the final result or API error in plain language, including IDs, counts, and the next relevant object when it matters.

If any request shape, field name, response contract, or endpoint capability is uncertain while executing this workflow, re-check the official API reference before proceeding:

- https://www.extruct.ai/docs/api-reference/introduction

## Plan Access Preflight For Pro-Only Actions

Deep Search mutations and table mutations are Pro-gated unless bypassed by manual or organization access.

Before the first Pro-only action in a conversation, run:

```bash
<extruct_api_cli> auth user
```

Use the response fields:

- `subscription.requires_subscription`
- `subscription.plan_tier`
- `user.organization_id`
- `user.organization_is_active`

Treat access as allowed if any of these conditions is true:

- `subscription.requires_subscription == false`
- `subscription.plan_tier` is `pro` or `legacy`
- `user.organization_id` is present and `user.organization_is_active == true`

If none of those conditions is true, stop before running Pro-only commands and tell the user the feature requires Pro.

Pro-only actions in this skill:

- Deep Search mutations: `deep-search create`, `deep-search resume`, `deep-search pause`
- Deep Research mutations: `deep-research create`
- Table mutations: `tables create`, `tables update`, `tables delete`, `tables clone`, `tables run`, `rows create`, `rows update`, `rows delete`, `columns add`, `columns update`, `columns delete`

## Resolve Extruct Identifiers

Users may provide Extruct objects as raw IDs or as dashboard URLs.

Interpret them as follows:

- if the user provides an Extruct table URL such as `https://app.extruct.ai/tables/<table_id>` or `http://app.extruct.ai/tables/<table_id>`, treat the path segment after `/tables/` as the table id
- if the user provides an Extruct task URL such as `https://app.extruct.ai/tasks/<task_id>` or `http://app.extruct.ai/tasks/<task_id>`, treat the path segment after `/tasks/` as the Deep Search task id
- if the URL includes extra path segments, query params, or fragments, still extract the id from the `/tables/<table_id>` or `/tasks/<task_id>` segment
- if the user provides a raw table UUID, use it directly as the table id
- if the user provides a raw task UUID, use it directly as the task id
- do not ask the user to restate an id that is already present in the URL
- when a table URL is present, default to the existing-table workflow unless the user explicitly asks for a new table or a search workflow
- when a task URL is present, default to the Deep Search task workflow unless the user explicitly asks to start a new search task

Example:

User request:

```text
Add a funding column to http://app.extruct.ai/tables/0a1a669a-9a40-497c-bb00-d49dd8ee5b74
```

Resulting table id:

```text
0a1a669a-9a40-497c-bb00-d49dd8ee5b74
```

First CLI reads:

```bash
<extruct_api_cli> tables get 0a1a669a-9a40-497c-bb00-d49dd8ee5b74
<extruct_api_cli> columns list 0a1a669a-9a40-497c-bb00-d49dd8ee5b74
<extruct_api_cli> tables data 0a1a669a-9a40-497c-bb00-d49dd8ee5b74 --limit 20 --offset 0
```

User request:

```text
Check results for https://app.extruct.ai/tasks/d530c3ad-626c-4d7b-ab15-181d4058e4f8
```

Resulting task id:

```text
d530c3ad-626c-4d7b-ab15-181d4058e4f8
```

First CLI reads:

```bash
<extruct_api_cli> deep-search get d530c3ad-626c-4d7b-ab15-181d4058e4f8
<extruct_api_cli> deep-search results d530c3ad-626c-4d7b-ab15-181d4058e4f8 --limit 20 --offset 0
```

## Choose The Right Company-Finding Path

### Semantic Search

Use semantic search when the user describes a market, ICP, category, product, or use case in natural language.

Typical asks:

- "search Extruct for AI procurement startups"
- "find German fintech companies in Extruct"
- "show me B2B treasury automation companies"

Commands:

```bash
<extruct_api_cli> companies search --query "vertical SaaS for logistics procurement" --limit 20

<extruct_api_cli> companies search --query "enterprise sales AI" \
  --filters '{"include":{"country":["United States"]},"range":{"founded":{"min":2018}}}' \
  --offset 20 --limit 20
```

Use `--filters` when the user specifies geography, city, company size, or founded range. Pass a JSON object like one of these as the `--filters` value.

```json
{
  "include": {
    "country": ["United States"],
    "size": ["51-200", "201-500"]
  }
}
```

```json
{
  "range": {
    "founded": {
      "min": 2018,
      "max": 2024
    }
  }
}
```

**Result limits and paging.** A single request returns at most 250 results (the page size); read deeper by holding `--limit` near 250 and walking `--offset` in steps. Paid plans (Starter, Pro) can page through up to 2,000 results per query; the free tier is capped at 25. To assemble a full list, keep paging until you reach the plan ceiling or a page returns fewer rows than `--limit`.

If search filters or pagination behavior appear different from the guidance here, verify current request and response details in the official API reference before guessing.

### Lookalike Search

Use lookalike search when the user already has a reference company and wants similar companies. Prefer domains for `--company-identifier` unless a prior Extruct response already gives you a UUID.

Typical asks:

- "find companies similar to Stripe in Extruct"
- "lookalike search from ramp.com"

Commands:

```bash
<extruct_api_cli> companies similar --company-identifier extruct.ai --limit 20

<extruct_api_cli> companies similar --company-identifier stripe.com \
  --filters '{"include":{"country":["United Kingdom"]}}'
```

Pagination uses the same `--offset` and `--limit` behavior as semantic search.

If identifier handling is unclear for a specific seed company or the live API behavior differs, verify the current lookalike-search request contract in the official API reference.

### Company Lookup

Use company lookup when the user has one known company and wants its full canonical Extruct company profile. This is not a discovery tool.

Use lookup for:

- "pull up Stripe's profile"
- "get the Extruct profile for ramp.com"
- "fetch details for this company profile UUID"

Do not use lookup when:

- the user describes a category or market — use semantic search
- the user asks for similar companies — use lookalike search
- the user wants a scored shortlist — use Deep Search

Command:

```bash
<extruct_api_cli> companies lookup --company-identifier stripe.com
```

`--company-identifier` accepts a domain or Extruct company profile UUID. A ready profile response returns `id`, `domain`, `company_name`, and the rich company profile in `context`. If Extruct accepts the lookup and starts enrichment, the response has `status: "enriching"`, `domain`, and `message`; retry the same lookup later. Company lookup currently consumes 0 credits, but successful and accepted lookups may appear in usage analytics.

### Deep Search

Use Deep Search when the user wants a higher-precision asynchronous company search, wants explicit criteria, or is comfortable waiting for a task.

Deep Search mutations (`create`, `resume`, `pause`) are Pro-gated. Run the plan-access preflight before those commands.

Typical asks:

- "run Deep Search for B2B revenue intelligence vendors"
- "find high-conviction AI procurement startups and show me the first result"

Create a task:

```bash
<extruct_api_cli> deep-search create --payload '{"query":"AI procurement startups serving enterprise finance teams","desired_num_results":25}'
```

Create a task with explicit criteria:

```bash
<extruct_api_cli> deep-search create --payload-file criteria.json
```

`criteria.json`:

```json
{
  "query": "vertical SaaS companies serving freight forwarding",
  "desired_num_results": 25,
  "criteria": [
    {
      "key": "has_logistics_focus",
      "name": "Logistics Focus",
      "criterion": "Company serves freight forwarding or logistics operations."
    },
    {
      "key": "b2b_fit",
      "name": "B2B Fit",
      "criterion": "Company sells primarily to business buyers."
    }
  ]
}
```

Inspect, poll, read results, or request more:

```bash
<extruct_api_cli> deep-search list --limit 20
<extruct_api_cli> deep-search get <task_id>
<extruct_api_cli> deep-search poll <task_id>
<extruct_api_cli> deep-search results <task_id> --limit 20 --offset 0
<extruct_api_cli> deep-search resume <task_id> --payload '{"desired_new_results":25}'
```

Deep Search pipeline:

A task progresses through four stages, each tracked by a counter on the task object:

1. **Discovery** (`num_results_discovered`) — candidates are gathered from data sources
2. **Enrichment** (`num_results_enriched`) — candidates are filtered for relevance and enhanced with company profiles
3. **Evaluation** (`num_results_evaluated`) — enriched candidates are scored against criteria
4. **Qualification** (`num_results`) — evaluated candidates that meet the fit threshold become final results

`is_exhausted` means the candidate pool is depleted (enrichment has caught up with discovery). It does **not** mean the task is done — evaluation and qualification continue after `is_exhausted` becomes true. A task can be `is_exhausted: true` + `status: "in_progress"` for a significant period while the remaining candidates are scored.

`status` is the only reliable completion indicator:
- `done` — task completed successfully
- `failed` — task did not complete (inspect error details)

`deep-search poll` blocks until `status` reaches `done` or `failed`.

Deep Search notes:

- `deep-search results` can be read while the task is still running
- `is_exhausted: true` means resume will fail (no more candidates to discover) — to get more results, create a new task
- if the user wants follow-on enrichment, move shortlisted domains into a company table
- if the payload spans more than a few lines or includes `criteria`, prefer `--payload-file` over inline `--payload`

If Deep Search payload fields, task states, or resume behavior are unclear, verify them against the official API reference before constructing raw fallback requests.

Read `references/finding-companies.md` when the task is a fuller company-discovery workflow instead of a single search command.

### Deep Research

Use Deep Research when the user wants a deep, cited report on one research target — a company, a person, or a team: account planning, buyer research, researching a lead before outreach, initiative summaries, diligence. For discovering many companies, use Deep Search; for repeatable enrichment across a list, use tables.

`deep-research create` is Pro-gated. Run the plan-access preflight before it.

Typical asks:

- "research Shell for me: buying centers, initiatives, sales angles"
- "build an account plan brief for Stripe"
- "research this lead and the team they work with before my call"
- "do diligence on this company and give me a sourced report"

Write the brief as a detailed paragraph, not a one-liner. Pack in everything you know
from the conversation: what the user sells or researches, who the target buyer is, what
decision the report supports, constraints, and time windows. The more context and
specifics the brief carries, the better the report. If the user's ask is thin, ask one
or two clarifying questions before creating the task.

Create a task (markdown report):

```bash
<extruct_api_cli> deep-research create --payload '{"brief":"We sell a cloud cost-optimization platform to large enterprises; typical buyers are VPs of Infrastructure and FinOps leads. I am preparing outreach to Shell. Research how Shell'"'"'s IT and digital organization is structured, who owns cloud infrastructure and FinOps decisions, which cloud, data, or efficiency initiatives they announced in the last 18 months, and which vendors or system integrators they already work with. I want practical conversation angles tied to live initiatives, plus any signals of cost-cutting programs or budget pressure.","depth":"medium"}'
```

People are first-class targets — include the user's own context and the profile to research:

```bash
<extruct_api_cli> deep-research create --payload '{"brief":"Here is my company: example.com. We sell AI-powered sales-enablement software to mid-market B2B teams. Research this person and the team they work with: https://www.linkedin.com/in/example-profile. I want their role and scope, what their team owns, recent initiatives or public statements, tools they already use, and the best angle to open a conversation.","depth":"medium"}'
```

Create a task with structured output (`--payload-file` preferred for schemas):

```bash
<extruct_api_cli> deep-research create --payload-file research.json
```

`research.json`:

```json
{
  "brief": "We provide fraud-prevention APIs for fintech platforms and are building an account plan for Stripe. Summarize Stripe's enterprise product initiatives from the last 12 months (payments, billing, risk, AI), identify concrete product or partnership angles where a fraud-prevention vendor could plug in, and flag risks that could stall a deal, such as in-house solutions, recent vendor consolidation, or compliance constraints.",
  "depth": "high",
  "output_schema": {
    "type": "object",
    "properties": {
      "summary": {"type": "string"},
      "recommended_angles": {"type": "array", "items": {"type": "string"}},
      "risks": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["summary", "recommended_angles", "risks"]
  }
}
```

Inspect, list, and wait for completion:

```bash
<extruct_api_cli> deep-research list --limit 20
<extruct_api_cli> deep-research get <task_id>
<extruct_api_cli> deep-research poll <task_id>
```

Depth and billing:

- `depth` sets the research-agent budget: `medium` = 25, `high` = 50, `xhigh` = 75.
- Creating a task requires the full budget in available credits; the user is billed only for agents that actually run (1 credit each). Failed tasks refund all charges.
- If create returns `insufficient_credits` with `required_credits`/`available_credits`, a lower depth may still fit — offer it.

Reading the result:

- Tasks take minutes. `deep-research poll` blocks until `status` is `done` or `failed`; progress counters are `iterations`, `agents`, `sources`.
- `report.kind` is `markdown` (citations like `[1]` resolve against `report.sources`) or `schema` (`fields` conforming to the output schema, `basis` mapping each field to supporting source ids, plus `sources`).
- **Always surface `report.degradation_reasons` to the user** — plain-language notes when coverage was reduced (early finalization, failed research agents). Empty means a clean run.
- On `failed`, read `failure_reason` and relay it: a rejected brief includes suggestions for fixing it. Failed tasks are refunded.

Read `references/deep-research.md` for brief-writing, depth choice, and output-schema design guidance.

## Operate Existing Tables

Use these commands when the user already has a table and wants to inspect it, change rows or columns, run new work, or read results.

Table mutations are Pro-gated. Run the plan-access preflight before create, edit, delete, clone, run, row mutation, or column mutation commands.

Typical asks:

- "add a funding column to this Extruct table"
- "poll this Extruct table until it finishes"
- "show me the first 20 rows from this table"
- "rerun only the new columns on this table"

If table payload shape, row schema, or run behavior is unclear, check the official API reference before mutating live tables:

- https://www.extruct.ai/docs/api-reference/introduction

### Create A Table

Use this when the user needs a new table before doing anything else.

```bash
<extruct_api_cli> tables create --payload '{
  "name":"Target Accounts",
  "kind":"company"
}'
```

### Inspect Before Mutating

If the user supplied a table URL, extract the table id first and use that id for all CLI commands below.

```bash
<extruct_api_cli> tables list --limit 20
<extruct_api_cli> tables list --scope organization --search acme --tags portfolio --tags priority --sort -num_rows --limit 20 --offset 0
<extruct_api_cli> tables get <table_id>
<extruct_api_cli> columns list <table_id>
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0 --columns company_name,company_website
<extruct_api_cli> rows get <table_id> <row_id>
```

`tables list` notes:

- the API returns root tables only
- `--scope personal` is a subset of `--scope organization`
- `--scope organization` includes the caller's tables plus other users' tables in the same organization
- `--search` filters by text
- repeat `--tags` to match any selected tag
- `--sort` supports `-created_at`, `created_at`, `name`, `-name`, `num_rows`, and `-num_rows`
- put `--sort` after `list`; use either `--sort -num_rows` or `--sort=-num_rows`
- the API default limit is `50`; requests above `100` are invalid

### Update, Clone, Or Delete A Table

Update metadata:

```bash
<extruct_api_cli> tables update <table_id> --payload '{
  "name":"Target Accounts - Updated",
  "description":"High-priority accounts for enrichment"
}'
```

Clone or delete:

```bash
<extruct_api_cli> tables clone <table_id> --schema-only
<extruct_api_cli> tables delete <table_id> --yes
```

`--schema-only` clones the columns and structure without copying row data.
Without `--schema-only`, clone copies both schema and rows.

### Add, Update, Or Delete Rows

Use company domains or URLs as the safest `input` on company tables.
Default to `"run": false` while iterating so you can inspect rows and columns before spending more work. Only switch to `"run": true` when the user explicitly wants add-and-run in one step.
Before deleting, inspect either the specific row with `rows get` or a small `tables data` page so you only remove the intended records.

Create rows:

```bash
<extruct_api_cli> rows create <table_id> --payload '{
  "rows":[
    {"data":{"input":"extruct.ai"}},
    {"data":{"input":"stripe.com"}}
  ],
  "run":false
}'
```

Update rows:

```bash
<extruct_api_cli> rows update <table_id> --payload '{
  "rows":[
    {
      "id":"<row_id>",
      "data":{"input":"https://extruct.ai"}
    }
  ],
  "run":false
}'
```

Delete rows:

```bash
<extruct_api_cli> rows delete <table_id> --yes --payload '{
  "rows":[
    "<row_id_1>",
    "<row_id_2>"
  ]
}'
```

Row-deletion notes:

- deletion is bulk and row-ID based
- `rows delete` requires `--yes`
- a successful response returns the deleted row IDs

### Add, Update, Or Delete Columns

Read `references/column-guide.md` before designing or changing columns. Prefer built-in column kinds before custom prompts.

On `company` tables, inspect `company_profile` before creating duplicate firmographic columns. The most common mistakes are adding columns for founding year, employee count, and HQ fields even though those are usually already present in the profile. Reuse those profile values unless the user needs a typed extraction, normalization, or another derived field. Freshness-sensitive research such as funding, revenue, pricing, or recent news can still justify dedicated columns.

If a column kind, payload field, or validation rule in this skill looks stale, verify the current table and column contract in the official API reference before retrying.

Add a custom research column:

```bash
<extruct_api_cli> columns add <table_id> --payload '{
  "column_configs":[
    {
      "kind":"agent",
      "name":"Expansion Signals",
      "key":"expansion_signals",
      "value":{
        "agent_type":"research_pro",
        "prompt":"Identify and summarize the company's expansion signals using job postings, press releases, new office mentions, executive hires, and product launches. Focus on geographic, product, or market expansion. Return a short evidence-dense summary with dates when available.",
        "output_format":"text"
      }
    }
  ]
}'
```

Update a column:

```bash
<extruct_api_cli> columns update <table_id> <column_id> --payload '{
  "kind":"agent",
  "name":"Expansion Signals",
  "key":"expansion_signals",
  "value":{
    "agent_type":"research_pro",
    "prompt":"Identify and summarize the company's expansion signals using job postings, press releases, new office mentions, executive hires, and product launches. Focus on geographic, product, or market expansion. Return a short evidence-dense summary with dates when available.",
    "output_format":"text"
  }
}'
```

Delete a column:

```bash
<extruct_api_cli> columns delete <table_id> <column_id> --yes
```

### Run And Poll

Default incremental run:

```bash
<extruct_api_cli> tables run <table_id>

<extruct_api_cli> tables run <table_id> --payload '{
  "mode":"new",
  "columns":["<column_id_1>","<column_id_2>"]
}'
```

Poll and then read a small result page:

```bash
<extruct_api_cli> tables poll <table_id>
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0
<extruct_api_cli> tables data <table_id> --limit 20 --offset 0 --columns company_name,expansion_signals
```

Table-operation defaults:

- prefer `mode: "new"` when iterating on an existing table
- bare `tables run <table_id>` is shorthand for `{"mode":"new"}`
- supported run modes are `new`, `all`, and `failed`
- pass explicit column ids when the user only wants new work
- inspect a small result page before scaling out, and use `--columns` whenever you only need a surgical slice of the data
- do not rerun the whole table unless the user explicitly wants that

### Choose The Right Table Kind

When creating a table, choose the kind from the entity the rows represent:

- `company`: use when rows are companies and the user wants company research, enrichment, scoring, or company-to-people branching
- `people`: use when rows are people or contacts and the user wants email, phone, LinkedIn, or derived people fields
- `generic`: use only when rows are neither companies nor people

For `generic` tables:

- the CLI fully supports create, update, run, and read operations
- this skill gives less prescriptive guidance because there are no company/people built-ins to lean on
- use `references/column-guide.md` more directly and design prompts, dependencies, and output formats explicitly

## Research Companies With Tables

Use company tables when the user wants custom enrichment over a set of companies or wants to run repeatable company research workflows.

Company table notes:

- `company` tables automatically include `input`, `company_profile`, `company_name`, and `company_website`
- `company_profile` commonly already contains descriptions, product/use-case summaries, founding year, employee count, HQ fields, social profile URLs, and supporting sources
- use domains or URLs as row inputs whenever possible
- built-in company columns usually remove the need to create basic identity fields yourself
- the most common duplicate-column mistakes are `founding_year`, `employee_count`, and HQ fields such as `hq_country`, `hq_state_province`, `hq_city`, and `hq_full_address`
- if those values already exist directly in `company_profile`, do not create another research column just to restate them; read them directly or extract them into a typed field if the table needs that shape
- freshness-sensitive facts such as funding, revenue, pricing, and recent news are different: even when partially present in `company_profile`, it often still makes sense to create dedicated columns because the user usually wants fresher or more structured outputs

If the user needs a fresh company table, create one:

```bash
<extruct_api_cli> tables create --payload '{
  "name":"Target Accounts",
  "kind":"company"
}'
```

Then use the existing-table commands above to:

1. add company rows
2. add custom research columns from `references/column-guide.md`
3. run only the new column ids with `mode: "new"`
4. poll and inspect a small results page

Read `references/researching-companies.md` when the task is a full company-research workflow instead of a single table operation.

## Find People At Companies

Use this path when the user starts from companies and wants decision-makers, leadership, or contactable people.

If child-table behavior, finder output shape, or workflow handoff details differ from what this skill expects, verify the current API behavior in the official API reference.

Start from a `company` table, then add a `company_people_finder` column:

```bash
<extruct_api_cli> columns add <company_table_id> --payload '{
  "column_configs":[
    {
      "kind":"company_people_finder",
      "name":"Decision Makers",
      "key":"decision_makers",
      "value":{
        "roles":["VP Sales","sales leadership","revenue operations"]
      }
    }
  ]
}'
```

Run only the new finder column and poll:

```bash
<extruct_api_cli> tables run <company_table_id> --payload '{
  "mode":"new",
  "columns":["<people_finder_column_id>"]
}'
<extruct_api_cli> tables poll <company_table_id>
```

Then inspect the parent table to find the generated child `people` table in `child_relationships`, and continue there:

```bash
<extruct_api_cli> tables get <company_table_id>
```

The parent company table will also show the people-finder cell result, but the child `people` table is the place to continue downstream enrichment.

Use broader role families for coverage, such as `sales leadership`, and exact titles for narrower targeting, such as `VP Sales`. Read `references/finding-people-at-companies.md` when the task is a full company-to-people workflow.

## Research People

Use this path when the user already has people rows or already has a generated child `people` table and now wants enrichment, contact data, or derived fields.

For a deep one-off report on a single person or team (rather than repeatable table enrichment), use Deep Research instead — see the Deep Research section above.

Typical asks:

- "find work emails for these people"
- "add phone numbers to this people table"
- "classify these contacts by department and seniority"

People-table notes:

- `people` tables automatically include `input`, `full_name`, `role`, and `profile_url`
- full name, current role, and LinkedIn URL is the safest `input`
- include current role when available
- for `email_finder` or `phone_finder`, `company_website` must exist under the exact key `company_website`
- on `people` tables, custom `agent` columns can use `llm`, `research_reasoning`, and `linkedin`; `research_pro` is not allowed

If people-table capabilities, supported column kinds, or enrichment requirements appear to have changed, verify them in the official API reference before proceeding.

Create a standalone people table with local website context:

```bash
<extruct_api_cli> tables create --payload '{
  "name":"Target Contacts",
  "kind":"people",
  "column_configs":[
    {
      "kind":"input",
      "name":"Company Website",
      "key":"company_website"
    }
  ]
}'
```

Add people rows:

```bash
<extruct_api_cli> rows create <people_table_id> --payload '{
  "rows":[
    {
      "data":{
        "input":"Jane Doe, VP Sales, https://linkedin.com/in/jane-doe",
        "company_website":"extruct.ai"
      }
    }
  ],
  "run":false
}'
```

Add contact or derived columns:

```bash
<extruct_api_cli> columns add <people_table_id> --payload '{
  "column_configs":[
    {
      "kind":"email_finder",
      "name":"Work Email",
      "key":"work_email"
    },
    {
      "kind":"phone_finder",
      "name":"Direct Phone",
      "key":"direct_phone"
    }
  ]
}'
```

Run, poll, and inspect:

```bash
<extruct_api_cli> tables run <people_table_id> --payload '{
  "mode":"new",
  "columns":["<column_id_1>","<column_id_2>"]
}'
<extruct_api_cli> tables poll <people_table_id>
<extruct_api_cli> tables data <people_table_id> --limit 20 --offset 0
```

Read `references/researching-people.md` when the task is a full people-research workflow.

## Troubleshooting And Recovery

### Auth Or Connectivity Fails

Run:

```bash
<extruct_api_cli> auth user
<extruct_api_cli> healthcheck
```

`auth user` should return both `user` and `subscription` objects.

If `auth user` fails, the token or account context is wrong. If `healthcheck` fails too, treat it as connectivity or service health.

If the auth flow, expected status codes, or healthcheck contract has changed, defer to the official API reference.

### Search Results Are Too Broad

- add `--filters` for country, city, size, or founded range
- switch from semantic search to lookalike if a reference company exists
- switch from semantic search or lookalike to Deep Search if the user wants a tighter, higher-conviction shortlist

### Lookalike Results Feel Wrong

- use a domain or UUID instead of a company name when possible
- confirm the seed company is the correct one before judging the output

### Column Creation Fails

Common causes:

- unresolved prompt references such as `{pricing_notes}` pointing at a missing key
- wrong table kind for the column kind
- invalid `json` columns without an `output_schema`

Check `references/column-guide.md` before retrying.

### Cells Never Start Or Stay Idle

Common causes:

- upstream dependency cells are not done yet
- the table is missing required context
- the run targeted the wrong columns

Checks:

- inspect the table header and current columns
- verify the same rows have `done` cells in any upstream dependency columns
- keep dependency chains short
- rerun only the intended new columns with `mode: "new"`

### Email Or Phone Enrichment Fails On People Tables

Check that:

- the row has strong person context in `input`
- `company_website` exists under the exact key `company_website`
- the row belongs to the intended company

### Results Are Hard To Use Downstream

- split multi-job prompts into separate columns
- use `select`, `multiselect`, `numeric`, `money`, `date`, `grade`, or `json` instead of defaulting to `text`
- use the simplest format that captures the business value; do not pack Extruct explanation or source metadata into `json` unless the user explicitly wants those fields as table data
- derive downstream classifications with `llm` after researching the source fact once

### Plan Or Billing Gates (402)

- if the CLI returns `402` with `detail.error = "plan_required"`, explain that the action requires Pro and do not blind-retry
- if the CLI returns `402` with `detail.error = "payment_failed"`, explain payment recovery is required before paid features can run
- if the CLI returns `402` with `detail.error = "insufficient_credits"`, treat it as billing/quota and guide the user to top up or wait for reset

### Retry Behavior

- if the CLI returns `429`, treat it as billing or quota rejection, not a tight-loop retry signal
- if the CLI returns a `5xx`, wait 5-10 seconds and retry once

## Global Flags

- `--pretty` for human-readable JSON
- `--timeout <seconds>` to override request timeout
- `--base-url <url>` to override the API base URL
- only these global flags can be placed before the resource, after the resource, or after the final action; resource-specific flags such as `tables list --sort` must stay with that action

## References

- `references/column-guide.md`: column design rules plus a comprehensive library of good column configs
- `references/finding-companies.md`: choose and operate semantic search, lookalike, and Deep Search
- `references/deep-research.md`: write briefs, choose depth, and design output schemas for Deep Research
- `references/researching-companies.md`: build or extend company research tables safely
- `references/finding-people-at-companies.md`: branch from company tables into people workflows
- `references/researching-people.md`: enrich standalone or generated people tables
- official Extruct API reference: https://www.extruct.ai/docs/api-reference/introduction
