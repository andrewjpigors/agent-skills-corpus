---
name: lead-listing-agent
description: "Upload CSV lead lists (AI Ark, Prospeo, Store Leads) to Neon Postgres, clean company names, enrich sales reps via AI Ark API, scrape company websites, AI-powered website analysis (competitors, ICP, descriptions, pricing, categorization) via Workers AI, custom enrichment, ICP scoring. Triggers on: upload leads, lead list, lead listing agent, import CSV, clean leads, lead upload, upload list, csv import, lead cleaning, push leads to neon, enrich leads, store leads, find competitors, analyze websites, ICP score, score leads, lead scoring."
---

# Lead Listing Agent

Upload, enrich, and manage lead lists in Neon Postgres with normalized company/contact tables.

## Constants

- **Neon project**: `<YOUR_NEON_PROJECT_ID>`
- **Master database**: `master` (central repository of all enriched data across clients)
- **Connection string**: `mcp__Neon__get_connection_string` with `projectId` + `databaseName`
- **Anthropic API key**: read from environment variable `ANTHROPIC_API_KEY` or a local `.env` file

## Rules (apply to ALL steps)

- **AI Ark = REST API only.** MCP server is broken. See `references/ai-ark-api.md`.
- **Cloudflare Browser Rendering = default scraper.** Fallback: Scrape.do (for blocked sites). See `references/cloudflare-browser-rendering.md` and `references/scrape-do.md`.
- **Cloudflare Workers AI = LLM for scraped content analysis.** Model: `@cf/meta/llama-3.1-70b-instruct`. Same auth as Browser Rendering. Use for any enrichment that requires understanding website content (competitors, descriptions, ICP, pricing, categorization, custom). See `references/cloudflare-browser-rendering.md`.
- **Save JSON backup to `~/Downloads/` before every DB write.** Connections timeout during long API operations. Always open a fresh connection for writes.
- **Flush stdout** in Python scripts (`sys.stdout.flush()` or override print).
- **Company-level enrichment targets `companies` table only** — enrich once per company, not per contact.
- Don't show `postgres` or `master` as client database options.
- **Always strip emoji** from all name fields (contacts: full_name, first_name, last_name; companies: sales_rep_1, sales_rep_2). Run this as part of every cleaning step. Use a Unicode-aware emoji regex to remove emoji characters while preserving accented Latin characters.
- **Always remove non-Latin script contacts.** After every insert or cleaning step, delete contacts whose `full_name` is primarily non-Latin script (Chinese, Arabic, Cyrillic, Korean, Japanese, Thai, Hindi, etc.). Accented Latin characters (Turkish ğ/ş, Vietnamese ễ/ờ, German ö/ü, etc.) are fine — keep those. Use Python `unicodedata` to check if letters are LATIN script. This is a hard rule — these contacts cannot be used in English cold email outreach.
- **Agent parallelization**: For steps processing 50+ items, spawn parallel agents per the "Agent Parallelization" section below. Agents NEVER write to DB or interact with the user — main context handles both.

---

## Agent Parallelization

Spawn parallel `Agent` subagents to split large workloads across independent scripts. Each agent handles a chunk of companies/contacts simultaneously, cutting wall-clock time by 2-4x.

### When to parallelize

- **50+ items to process** — below this, single-context is fast enough
- **Only after hard gates** — get user approval first, then spawn agents
- **Never for interactive steps** — triage, CSV intake, ICP rubric building stay in main context

### Spawn pattern

1. Query full list of items to process
2. Split into N chunks (round-robin by index)
3. Save each chunk as JSON to `~/Downloads/{step}_input_chunk{N}_{timestamp}.json`
4. Spawn N agents in a **single tool-call batch** (all launch simultaneously)
5. Each agent: reads chunk JSON → writes & runs Python script → saves results to `~/Downloads/{step}_results_chunk{N}_{timestamp}.json` → returns summary
6. Main context reads all result JSONs, aggregates, writes to DB

### Agent configuration

- **Type**: `general-purpose` (needs Bash for Python scripts)
- **Mode**: `bypassPermissions` (agents run non-interactively)
- **Default count**: 3 agents (unless rate limits require fewer)
- **Max**: 4 agents

### Rate limit budgets (per agent)

All agents share the same API keys. Divide total rate limits by agent count.

| API | Total Limit | Per agent (2) | Per agent (3) | Per agent (4) |
|-----|-------------|---------------|---------------|---------------|
| AI Ark People Search | 15 req/sec | 7 | 5 | 3 |
| AI Ark Export Single | 5 req/sec | 2 | — | — |
| Serper | 50 req/sec | 25 | 16 | 12 |
| Exa | ~5 concurrent | 2 | 1-2 | 1 |
| CF Browser Rendering | 30 concurrent | 15 | 10 | 7 |
| Workers AI | high | unlimited | unlimited | unlimited |
| Scrape.do | plan-dependent | half | third | quarter |

### JSON handoff protocol

Each agent saves results with a summary header:
```json
{
  "summary": {"chunk": 1, "total_chunks": 3, "processed": 167, "failed": 3, "skipped": 2},
  "results": [...]
}
```

### Hard gate pattern with agents

```
1. Main context: query data, show preview to user
2. Hard gate: AskUserQuestion for approval
3. If approved: split into chunks, spawn agents
4. Agents: process chunks, save JSON (NO DB writes)
5. Main context: read result JSONs, write to DB
6. Main context: show aggregate summary
```

### Agent prompt template

Each agent receives a prompt like:
```
You are processing chunk {N} of {total} for {step_name}.

Your task: process {count} companies from ~/Downloads/{input_file}.
Write a Python script that:
1. Reads the input JSON
2. {step-specific processing logic}
3. Saves results to ~/Downloads/{step}_results_chunk{N}_{timestamp}.json with summary header
4. Prints: "DONE: {processed}/{total} processed, {failed} failed"

Rate limits (YOUR budget, not total):
{per-agent rate limit table}

Rules:
- Save JSON results before exiting
- sys.stdout.flush() after every print
- Do NOT ask the user questions
- Do NOT write to the database
- On 5+ consecutive failures, save partial results and stop
```

### Error handling

- **Agent-internal**: Python scripts use retry/backoff (existing behavior, unchanged)
- **Partial success**: Agent saves completed work to JSON, returns count. Main context reports: "Chunk 2: 120/167 processed, 47 remaining"
- **Full failure**: Main context detects missing result file, reports which chunk failed, offers to retry that chunk with a single new agent

---

## Step 0 — Triage

Use `AskUserQuestion` for every question. Hard gate — don't proceed until all answered.

**Q1: Which client?** Query `SELECT datname FROM pg_database WHERE datistemplate = false AND datname NOT IN ('postgres', 'master') ORDER BY datname;` → single-select from results + "New client" option. New client → freetext name → `CREATE DATABASE`.

**Q2: Lead source?** Single-select:
1. **Upload new CSV** → Q3, then Step 1
2. **Work with existing data** → Next Steps Menu (multi-select, see below)
3. **Find contacts at companies** → AI Ark Contact Finder flow
4. **Search master database** → Master Database Search flow

**Q3: Campaign?** (only for new data or organizing existing) Query `SELECT campaign, COUNT(*) as contacts, COUNT(email) as with_email FROM contacts GROUP BY campaign ORDER BY campaign;` → single-select: New campaign (freetext name) or Existing campaign.

## Step 0.5 — Prerequisites

1. Verify Neon MCP: `mcp__Neon__get_database_tables` against the project with chosen DB name
2. If `companies`/`contacts` tables missing (new client), create them:

```sql
CREATE TABLE companies (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), ai_ark_account_id TEXT, prospeo_company_id TEXT, name TEXT NOT NULL, cleaned_name TEXT, domain TEXT UNIQUE, industry TEXT, size_min INTEGER, size_max INTEGER, linkedin_url TEXT, sales_rep_1 TEXT, sales_rep_2 TEXT, website_summary TEXT, website_raw JSONB, website_scraped_at TIMESTAMP, custom_fields JSONB DEFAULT '{}', raw_data JSONB, created_at TIMESTAMP NOT NULL DEFAULT NOW(), updated_at TIMESTAMP NOT NULL DEFAULT NOW());
CREATE TABLE contacts (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), company_id UUID REFERENCES companies(id), campaign TEXT NOT NULL, ai_ark_person_id TEXT, prospeo_person_id TEXT, first_name TEXT, last_name TEXT, full_name TEXT NOT NULL, email TEXT, email_status TEXT, job_title TEXT, seniority TEXT, department TEXT, linkedin_url TEXT, location_city TEXT, location_state TEXT, location_country TEXT, email_provider TEXT, custom_fields JSONB DEFAULT '{}', raw_data JSONB, created_at TIMESTAMP NOT NULL DEFAULT NOW(), updated_at TIMESTAMP NOT NULL DEFAULT NOW(), UNIQUE(campaign, ai_ark_person_id));
CREATE TABLE campaign_configs (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), campaign TEXT NOT NULL UNIQUE, icp_rubric JSONB DEFAULT '[]', created_at TIMESTAMP NOT NULL DEFAULT NOW(), updated_at TIMESTAMP NOT NULL DEFAULT NOW());
```

---

## Step 1 — CSV Intake

*Skip if user chose "work with existing data".*

1. Ask for file path, read first 30 lines with `Read` tool
2. Show headers + 5 data rows
3. Auto-map columns per `references/csv-column-map.md`
4. **Hard gate** — user confirms mapping before proceeding

## Step 2 — Parse & Insert

Write a Python script: read CSV, auto-detect source + map columns per `references/csv-column-map.md`, group by domain, insert companies first (`ON CONFLICT (domain) DO NOTHING`), then contacts with campaign tag. Batch 500 rows via `psycopg2.extras.execute_values`. Show stats: X companies (Y new), Z contacts inserted.

**Store Leads special handling:**
- Company-only source — no contacts to insert. Skip contact insertion entirely.
- Strip `www.` from `domain` column to normalize.
- Parse `categories` → first segment as `industry` (e.g., `/Food & Drink` → `Food & Drink`).
- Parse sales figures: strip `USD $` and commas → store as numeric in `custom_fields`.
- Store e-commerce signals in `custom_fields`: platform, plan, technologies, estimated_monthly_sales, estimated_yearly_sales, estimated_monthly_visits, estimated_monthly_pageviews, average_product_price_usd, products_sold, region, company_location.
- Store everything else in `raw_data`.

---

# Mandatory Cleaning Steps

Run automatically after every upload. **Store Leads**: only run Step 3 (company name cleaning) — skip Steps 4, 5, 6, 6.5 (no contacts). All three contact steps use the same pattern:
1. Query rows needing cleaning
2. Batch 100 per Anthropic Haiku API call
3. Show 10 before/after samples
4. **Hard gate** — user approves before writing to DB

### Parallel Cleaning Strategy (50+ rows)

Steps 3, 4, 5, and 6 are independent — spawn as **4 parallel agents** (one per step) in a single tool-call batch.

Each cleaning agent:
1. Queries rows needing its specific cleaning
2. Processes via Anthropic Haiku API (batches of 100)
3. Saves results to `~/Downloads/{step}_results_{timestamp}.json` with summary header (NO DB writes)
4. Returns: `{total}` processed, `{cleaned}` modified, 10 before/after sample pairs

Main context then:
1. Reads all 4 result files
2. Shows 10 before/after samples from **each** step
3. Single combined `AskUserQuestion`: "Approve all cleaning results?"
4. If approved: writes all 4 steps to DB in sequence
5. Then runs Step 6.5 (junk detection) in main context — it depends on cleaned data

**Store Leads**: only spawn Step 3 agent (no contacts to clean).
**Under 50 rows**: skip agents, run all steps sequentially in main context (existing behavior).

---

## Next Steps Menu

Shown after mandatory cleaning completes (new upload) OR when user selects "Work with existing data" in Q2. **Multi-select `AskUserQuestion`** — user can pick one or more. Execute selected steps in the order listed below.

**Header:** "What do you want to do?"
**Options:**
1. **Enrich** — "Run enrichments (website intel, sales reps, cold email detection, Apify, custom)"
2. **ICP Scoring** — "Score contacts against ideal customer criteria"
3. **Find contacts at companies** — "Pull contacts from AI Ark for companies in DB"
4. **Sync to master DB** — "Upsert data to the shared master database"
5. **Launch campaign** — "Hand off to /head-of-strategy for email campaign"
6. **Query / export** — "Run a custom query or export to CSV"
7. **Add custom fields** — "Add new custom enrichment fields"
8. **Done** — "Finish up"

After all selected steps complete, show the Summary Report (Step 7) and re-show this menu for any additional actions — unless user picked "Done".

---

## Step 3 — Clean Company Names

Query: `SELECT id, name FROM companies WHERE cleaned_name IS NULL`

Rules: remove taglines after -/|, fix ALL CAPS, strip "Powered by X", "A Division of", ".com" when there's a real name. Goal: clean for email personalization ("I saw that {company_name} is...").

## Step 4 — Clean Lead Names

Query: `SELECT id, first_name, last_name, full_name FROM contacts WHERE full_name IS NOT NULL`

Rules:
- **Delete non-Latin contacts first**: remove any contact whose `full_name` is primarily non-Latin script (Chinese/Arabic/Cyrillic/Korean/Japanese/Thai/Hindi). Use Python `unicodedata` — check if letter characters have LATIN in their Unicode name. Accented Latin (Turkish, Vietnamese, German, etc.) is fine.
- **Strip all emoji** from full_name, first_name, last_name before any other cleaning
- ALL CAPS / all lowercase → proper case
- Special surnames: McDonald, O'Brien, de la Cruz, van der Berg, MacArthur
- Strip: Mr./Mrs./Ms. (keep Dr./Prof.), appended company names, extra whitespace
- Standardize suffixes: Jr./III/PhD → consistent format
- Flag junk entries: "N/A", "Test", "Admin", "Info", email-as-name, initials-only

## Step 5 — Clean Job Titles

Query: `SELECT id, job_title FROM contacts WHERE job_title IS NOT NULL`

Rules:
- ALL CAPS → proper case (keep VP, CEO, CTO, SVP)
- Strip "at [Company]", LinkedIn tagline stuffing (keep only primary title before |/-), emojis
- Standardize: "Sr." vs "Senior", "Jr." vs "Junior" — pick one style

## Step 6 — Email Provider Detection

- **Prospeo source**: use `Company MX provider` column directly → google/microsoft/other. Skip MX lookup.
- **AI Ark / other**: query distinct email domains where `email_provider IS NULL`. Python script: `dig +short MX {domain}`, 20 concurrent threads. Classify: google (google/googlemail/aspmx), microsoft (outlook/microsoft/protection.outlook), other, unknown.

Show breakdown: google / microsoft / other / unknown counts.

## Step 6.5 — Junk Lead Detection

Final quality check. Flag contacts matching ANY:
- **Name junk**: "Test", "N/A", "Admin", "Info", "Support", email-as-name, initials-only ("J. S.")
- **Generic inbox**: info@, admin@, support@, hello@, contact@, sales@
- **Title junk**: "N/A", "-", ".", "Employee", "Staff", contains "Retired"/"Former"
- **Name-email mismatch**: name "Sarah" but email starts with "mike@"

Show flagged contacts with reasons. **Hard gate** — AskUserQuestion: Remove / Keep / Mark as low quality (`{quality: low}` in custom_fields).

---

# Optional Enrichment Steps

*Triggered when user selects "Enrich" from the Next Steps Menu.*

Multi-select `AskUserQuestion`: which enrichments to run? (Website Intelligence, Sales Rep Names, Cold Email Detection, Apify, Custom)

### Cost Estimation Gate (runs before ANY enrichment)

**Hard gate — always runs.** After the user selects enrichments but BEFORE executing anything:

1. **Count companies**: Query `SELECT COUNT(*) FROM companies WHERE domain IS NOT NULL` (adapt filter per enrichment)
2. **Estimate cost** per enrichment using this table:

| Enrichment | Cost per company | Formula |
|---|---|---|
| Website Intelligence — Quick | $0.00002 | (CF Browser + Workers AI) |
| Website Intelligence — Deep Research | $0.011 | (3 Serper × $0.001 + 1 Exa × $0.007 + scrapes × $0.001 + Workers AI × $0.0001) |
| Sales Rep Names | $0 | (AI Ark API, no per-call cost) |
| Cold Email Detection | $0 | (HTTP requests only) |
| Apify actors | Varies | (check actor pricing via `fetch-actor-details`) |
| Custom | Varies | (estimate based on tools used) |

3. **Show cost summary** to user via `AskUserQuestion` (single-select):

   **Header:** "Cost estimate"
   **Question:**
   ```
   Enrichment plan for {N} companies:

   • {Enrichment 1}: {N} companies × ${cost_per} = ${total_1}
   • {Enrichment 2}: {N} companies × ${cost_per} = ${total_2}
   ─────────────────────────────
   Estimated total: ${grand_total}
   Estimated time: ~{minutes} min

   This is an estimate — actual cost may vary ±20%.
   ```
   **Options:**
   1. **Proceed** — "Run all {N} companies"
   2. **Test batch first** — "Run on a small batch, review results, then decide" (batch size is cost-adaptive: target ~$1 test spend → `min(100, floor(1.00 / cost_per_company))`. For Quick mode this is 100; for Deep Research ~90; for expensive Apify actors it may be as low as 2-5.)
   3. **Cancel** — "Don't run, go back to enrichment selection"

4. **Auto-flag expensive runs**: If estimated total exceeds **$10**, add a warning line:
   ```
   ⚠️ This run is estimated at ${grand_total}. Consider running a test batch first.
   ```
   If estimated total exceeds **$50**, change the default recommendation:
   ```
   ⚠️ High cost estimate: ${grand_total}. Strongly recommend test batch first.
   ```

5. **Test batch flow**: If user picks test batch, run on 100 companies → show results + actual cost incurred → ask:
   - **Proceed with remaining {N-100}** — "Estimated remaining cost: ${remaining}"
   - **Cancel** — "Stop here, keep the 100 results"

### Apify

AskUserQuestion: which actor? LinkedIn Jobs / BuiltWith-Wappalyzer / Google Maps / Other (freetext). Use Apify MCP tools: `search-actors` → `fetch-actor-details` → `call-actor`. Store results in `custom_fields`.

**LinkedIn Jobs**: Always sort by most recent postings first. After the user selects this actor, use `AskUserQuestion` (freetext) to ask:
- **Header:** "Job filter"
- **Question:** "Which departments or job titles do you want to filter for? (e.g., 'sales and business development', 'engineering', 'all titles')"

Use the user's answer to build a keyword filter. After scraping, only store titles matching their filter. Store as:
- `hiring_{department}`: "yes" or "no" (key named after the filtered department, e.g., `hiring_sales`, `hiring_engineering`)
- `hiring_{department}_titles`: array of matching titles only (omit if none)

Do NOT store raw job counts, all titles, or scrape timestamps — only the filtered signal the user asked for.

### Website Intelligence

Scrapes company websites and extracts structured intelligence using Cloudflare Workers AI (Llama 3.1 70B). This is a single unified enrichment — the user picks what to extract and the research depth.

**Step 1 — Ask what to extract** (`AskUserQuestion`, multi-select):

1. **Competitor identification** — top 3-5 competitors with reasoning
2. **Company description** — what they do, who they sell to, in 2-3 sentences
3. **ICP / target market** — who this company sells to (industry, size, persona)
4. **Pricing model** — free tier, pricing tiers, enterprise, usage-based, etc.
5. **Product categorization** — categorize into a market/vertical
6. **Custom** — freetext: user describes what to extract

**Step 2 — Ask research depth** (`AskUserQuestion`, single-select):

1. **Quick** — "Scrape company website only. Fast, nearly free (~$0.01 per 500 companies). Best for: descriptions, product categorization, info visible on the site."
2. **Deep Research** — "Multi-source: Google search + semantic search + company website + review/comparison pages. Much more accurate for competitors, ICP, pricing, anything requiring market context. ~$0.01 per company ($5 per 500)."

**Step 2.5 — Ask output format** (`AskUserQuestion`, single-select):

Ask this for ANY text-generating enrichment (descriptions, ICP, competitors, pricing, custom). The output format dramatically affects usability.

1. **Cold email ready** — "Output completes a sentence like 'I saw that you...' — lowercase, conversational, describes what the company does for customers. Max 20 words."
2. **Analytical** — "Factual 2-3 sentence description. Good for research, internal notes, or CRM fields."
3. **Custom** — freetext: user describes exactly how they want the output formatted.

Use the chosen format to adapt the Workers AI system/user prompts in both Quick and Deep Research modes. For cold email format, the system prompt should instruct: "Output a short phrase that completes 'I saw that you...' — lowercase, conversational, no preamble, max 20 words."

**Step 3 (Quick mode only) — Ask scraping depth** (`AskUserQuestion`, single-select):
- Homepage only / Homepage + About / Deeper crawl

**After Steps 1-3**: If user chose **Quick** → proceed to the **Quick Mode** section below. If user chose **Deep Research** → skip Step 3 and proceed to the **Deep Research Mode** section below.

**Scraping infrastructure (both modes):**

1. **Cloudflare Browser Rendering** (default) — see `references/cloudflare-browser-rendering.md`
2. **Detect blocks**: HTML < 500 chars, contains "Access Denied" / "403 Forbidden" / "Just a moment" / "Enable JavaScript", or job status `errored` / `cancelled_due_to_timeout`
3. **Scrape.do fallback** (blocked sites only) — see `references/scrape-do.md`. `GET https://api.scrape.do?token={token}&url={url}&render=true`
4. **Flag as unscrapeable**: if both fail, set `custom_fields.scrape_status = "blocked"` and skip

Store raw HTML in `website_raw`, set `website_scraped_at`. Resumable — only processes unscraped companies.

---

#### Quick Mode

**Prerequisites**: Website must be scraped first (`website_raw` populated). If not, run the scraping infrastructure step above first.

Query (adapt `custom_fields` filter based on selected preset to skip already-enriched companies):
`SELECT id, domain, cleaned_name, website_raw FROM companies WHERE website_scraped_at IS NOT NULL AND domain IS NOT NULL AND custom_fields->>'{ preset_key }' IS NULL`

**Flow per company:**
1. Extract text from `website_raw`: strip `<script>`, `<style>`, HTML tags, collapse whitespace, truncate to ~6,000 chars
2. Build prompt based on user's selection (can combine multiple presets in one call)
3. Call Workers AI (`@cf/meta/llama-3.1-70b-instruct`), `max_tokens: 500`
4. Parse response → store in `custom_fields` with descriptive keys

**Batch strategy**: 10 concurrent requests to Workers AI. ~1-2 sec per response.

> **PARALLEL (50+ companies)**: Split company list into 3 chunks, spawn 3 agents in a single tool-call batch.
> Each agent writes a Python script that: reads its chunk, scrapes unscraped websites (CF Browser, 10 concurrent per agent), then runs Workers AI analysis (10 concurrent per agent).
> Agents save results to `~/Downloads/quick_mode_results_chunk{N}_{timestamp}.json` (NO DB writes).
> Main context reads all result JSONs, writes to DB, shows aggregate summary.
> **Under 50 companies**: skip agents, run in main context with existing batch strategy.

---

#### Deep Research Mode

Multi-source research pipeline. Searches the web, reads multiple pages, and synthesizes — like a research agent but with predictable cost and speed.

**Prerequisites**: None — this mode handles its own scraping. Company just needs a `domain` and `cleaned_name`.

Query: `SELECT id, domain, cleaned_name FROM companies WHERE domain IS NOT NULL`
(Adapt WHERE clause to skip companies already enriched for the selected preset.)

**Flow per company (3 phases):**

**Phase 1 — Gather (parallel, ~3 sec)**

Run all searches and scrapes simultaneously using Python threads:

| Source | Tool | Query template | What it returns |
|---|---|---|---|
| Google search #1 | `mcp__serper__google_search` | *See adaptive queries table below* | Top 10 organic results (titles + snippets + URLs) |
| Google search #2 | `mcp__serper__google_search` | *See adaptive queries table below* | Top 10 organic results |
| Google search #3 | `mcp__serper__google_search` | *See adaptive queries table below* | Top 10 organic results |
| Google reviews | `mcp__serper__google_search_reviews` | "{cleaned_name}" | Review snippets from G2, Capterra, etc. |
| Semantic search | `mcp__exa__web_search_exa` | *See adaptive queries table below* | Semantically related companies + page content |
| Company website | Cloudflare Browser Rendering (→ Scrape.do fallback) | "https://{domain}" | Raw HTML of homepage |

**Adaptive search queries per preset** — use the queries matching the user's selected preset:

| Preset | Search #1 | Search #2 | Search #3 | Exa query |
|---|---|---|---|---|
| Competitors | "{company} competitors" | "{company} alternatives" | "{company} vs" | "companies similar to {company}" |
| ICP / target market | "{company} customers" | "{company} case studies" | "{company} use cases" | "who uses {company}" |
| Pricing model | "{company} pricing" | "{company} pricing plans cost" | "{company} free trial" | "{company} pricing review" |
| Product category | "{company} category" | "{company} market segment" | "what type of software is {company}" | "tools like {company}" |
| Description | "{company} overview" | "what does {company} do" | "{company} company profile" | "company like {company}" |
| Custom | Adapt to user's question | Adapt | Adapt | Adapt |

**Serper searches**: Use the Serper MCP tools directly. Each returns structured JSON with titles, snippets, URLs. Cost: ~$0.001 per search.

**Exa search**: Use `mcp__exa__web_search_exa` with `numResults: 5`. Returns semantically similar pages with content. Cost: ~$0.007 per search. Rate limit: start with 3 concurrent requests; if 429 errors, back off 2s and retry once. If second failure, skip Exa for that company and continue.

**Phase 2 — Deep dive (selective, ~3 sec)**

From Phase 1 search results, score and pick the **top 3-5 most valuable URLs** to scrape fully. Prioritize:
- G2/Capterra comparison pages (e.g., "X vs Y", "X alternatives")
- "Best [category] tools" listicle posts
- Industry analyst or review pages
- Competitor homepages (to understand what they do)

**Skip**: the company's own site (already scraped), social media links, job boards, news articles.

Scrape selected URLs using `mcp__serper__webpage_scrape` (fast, included in Serper plan) or Cloudflare Browser Rendering for JS-heavy pages. Extract text, truncate each to ~2,000 chars.

**Phase 3 — Synthesize (Workers AI, ~2 sec)**

Combine all gathered context into a single Workers AI call:

```
CONTEXT BLOCK (sent to LLM):
---
COMPANY WEBSITE ({domain}):
{stripped homepage text, ~3000 chars}

GOOGLE SEARCH RESULTS:
{titles + snippets from all 3 searches, ~1500 chars}

REVIEW SITE DATA:
{G2/Capterra snippets, ~1000 chars}

DEEP DIVE PAGES:
Page 1 ({url}): {stripped text, ~2000 chars}
Page 2 ({url}): {stripped text, ~2000 chars}
Page 3 ({url}): {stripped text, ~2000 chars}

SEMANTIC SEARCH RESULTS (Exa):
{similar companies + snippets, ~1500 chars}
---
```

Total context: ~12,000-15,000 chars. Well within Llama 70B limits.

System prompt: "You are a senior business analyst. You have been given research from multiple sources about a company. Synthesize the information to answer the question accurately. Cross-reference sources — if multiple sources agree, high confidence. If only one source mentions something, note lower confidence. Only name real companies and real facts."

User prompt: built from the selected preset(s), same as Quick mode but referencing "the research below" instead of "this website content."

`max_tokens: 800` (more room for multi-source synthesis).

**Storage**: Same `custom_fields` keys as Quick mode, plus:
```json
{
  "research_mode": "deep",
  "research_sources_count": 8,
  "research_sources": ["company_website", "serper:competitors", "serper:alternatives", "serper:vs", "serper:reviews", "exa:similar", "g2.com/compare/...", "capterra.com/..."]
}
```

---

#### Preset prompts and storage (both modes)

| Preset | System prompt addition | User prompt (template) | Stored as |
|---|---|---|---|
| Competitors | "Specializing in competitive intelligence. Only name real companies." | "Identify {company}'s top 3-5 competitors. For each, one-line explanation of why they compete." | `competitors` (array), `competitors_raw` (string) |
| Description | "Be concise and factual." | "Write a 2-3 sentence description of what {company} does and who they serve." | `company_description` |
| ICP / target market | "Specializing in market segmentation." | "Identify {company}'s target customer: industry, company size, buyer persona, and use case." | `target_market` |
| Pricing model | "Only state what's supported by the research. Say 'not found' if pricing isn't available." | "Describe {company}'s pricing model (free tier, tiers, enterprise, usage-based, etc.)." | `pricing_model` |
| Product category | "Respond with just the category name." | "Categorize {company} into a market/vertical (e.g., 'Sales Engagement', 'CRM', 'Marketing Automation')." | `product_category` |
| Custom | Adapt based on user's freetext | Adapt based on user's freetext | Key agreed with user |

**Combining presets**: If user picks multiple, combine into a single prompt with numbered sections. Works in both modes.

---

#### Deep Research — Batch strategy

> **PARALLEL (50+ companies)**: Split company list into 3 chunks, spawn 3 agents in a single tool-call batch.

**Per-agent budgets (3 agents):**
- 2 companies concurrent (each runs ~6 parallel searches internally)
- Serper: 16 req/sec per agent (total 48, under 50 limit)
- Exa: 1-2 concurrent per agent (total ~5, use backoff on 429)
- CF Browser: 10 concurrent per agent (total 30)
- Workers AI: unlimited

Each agent writes a Python script that:
1. Reads its chunk from `~/Downloads/deep_research_input_chunk{N}_{timestamp}.json`
2. Processes companies through all 3 phases (Gather → Deep dive → Synthesize)
3. Saves results to `~/Downloads/deep_research_results_chunk{N}_{timestamp}.json` every 50 companies
4. Returns summary: processed/failed/skipped counts

Main context: reads all result JSONs after agents finish → writes to DB → shows aggregate summary.

**Under 50 companies**: skip agents, run in main context with 5 concurrent companies.

- **Per-company wall time**: ~8-10 sec
- **500 companies with agents**: ~8-9 min (down from ~25 min)
- **Cost per company**: ~$0.011 (3 Serper: $0.003, 1 Exa: $0.007, scrapes: $0.001, Workers AI: $0.0001)
- **Cost per 500**: ~$5.50 (unchanged — parallelization doesn't affect cost)
- **Save incrementally**: each agent saves JSON backup every 50 companies

#### Deep Research — Resumability

Deep Research is resumable. Use per-preset `custom_fields` keys to skip already-enriched companies:
`SELECT id, domain, cleaned_name FROM companies WHERE domain IS NOT NULL AND custom_fields->>'{ preset_key }' IS NULL`

Example for competitors: `WHERE domain IS NOT NULL AND custom_fields->>'competitors' IS NULL`

### Sales Rep Names

Query: `SELECT id, ai_ark_account_id FROM companies WHERE sales_rep_1 IS NULL AND ai_ark_account_id IS NOT NULL`

Use AI Ark REST API per `references/ai-ark-api.md` — batch 20 UUIDs/request, 12 threads. Filter by sales departments. Update `sales_rep_1`, `sales_rep_2`.

> **PARALLEL (50+ companies)**: Split company list into 3 chunks, spawn 3 agents.
> Each agent: 4 threads at 5 req/sec (total: 12 threads, 15 req/sec across all agents).
> Agents save results to `~/Downloads/sales_rep_results_chunk{N}_{timestamp}.json` (NO DB writes).
> Main context aggregates and writes to DB.

### Cold Email Detection

Detect companies running cold email by checking redirect domains. For each company domain, generate ~50 variants (prefixes: try/get/go/use/hey/meet/join/hello/start..., suffixes: hq/app/mail/team/now/labs..., alternate TLDs, hyphenated forms). Curl each with `-sI -L -o /dev/null -w "%{url_effective}" --max-time 4`, 20 concurrent threads. Count how many redirect to the main domain.

Store in `custom_fields`: `cold_email_redirect_count`, `cold_email_redirect_domains`, `cold_email_signal` (strong: 5+, moderate: 2-4, weak: 1, none: 0).

**Note:** For 1,000 companies this is ~50,000 HTTP requests. Save results incrementally.

> **PARALLEL (50+ companies)**: Split company list into 3 chunks, spawn 3 agents.
> Each agent: ~7 concurrent HTTP threads (total ~21 across all agents).
> Agents save results to `~/Downloads/cold_email_results_chunk{N}_{timestamp}.json` (NO DB writes).
> Main context aggregates and writes to DB.

### Custom Enrichment

Always store in `custom_fields` JSONB — never add new columns. Use descriptive keys. After every company-level enrichment, sync to contacts:
```sql
UPDATE contacts SET custom_fields = COALESCE(contacts.custom_fields, '{}'::jsonb) || COALESCE(companies.custom_fields, '{}'::jsonb), updated_at = NOW() FROM companies WHERE contacts.company_id = companies.id AND companies.custom_fields IS NOT NULL AND companies.custom_fields != '{}'::jsonb;
```

---

## Step 7 — Summary Report

Show totals: companies (total, cleaned, with reps, scraped), contacts (total, with email). Campaign breakdown with email provider counts (google/microsoft/other).

**Store Leads**: show companies (total, cleaned) + e-commerce breakdown: platform distribution (Shopify/Shopify Plus/other), top categories, region split. No contact stats.

## Step 8 — Sync to Master Database

**Hard gate** — `AskUserQuestion` before executing: show record counts ("Sync X companies and Y contacts to master DB. This will update shared records used across all clients. Proceed?"). Then upsert from client DB → master DB:
- Companies: `ON CONFLICT (domain) DO UPDATE` — newer `updated_at` wins per field, `custom_fields` merge with `||` (client wins on conflicts)
- Contacts: `ON CONFLICT (campaign, ai_ark_person_id) DO UPDATE` — same timestamp logic

Show sync summary: X companies (Y new, Z updated), A contacts synced.

---

## AI Ark Contact Finder

*Triggered by "Find contacts at companies" in Q2.*

Conversational flow — the user describes who they want, you build the API filters and pull contacts with verified emails from AI Ark into the `contacts` table.

### Step A — Scope the search

Use `AskUserQuestion` to gather criteria. Ask conversationally — don't dump all options at once. Start with:

1. **Which companies?** Options:
   - All companies in DB
   - Filter by industry / size / custom_fields (e.g., `platform = 'Shopify'`)
   - Specific domains (freetext list)

   Show a count after filtering: "Found X companies matching your criteria."

2. **Who are you looking for?** Freetext — let the user describe in natural language. Examples:
   - "Sales leaders — directors and VPs"
   - "Marketing managers"
   - "Founders and C-suite"
   - "Account executives"

   Map their answer to AI Ark filters:
   - **Department**: match to AI Ark department codes (see `references/ai-ark-api.md`)
   - **Seniority**: match to AI Ark seniority values
   - **Title**: use smart match for specific titles
   - Combine multiple filters as needed

3. **Campaign name?** Ask what campaign to tag these contacts with.

4. **With or without emails?** Single-select AskUserQuestion:
   - **Names only** — "Search only. Faster, no credit cost. Gets name, title, company, LinkedIn, seniority. No emails."
   - **Names + verified emails** — "Export with email. Async, uses credits (1 per contact). Gets everything above plus BounceBan-verified email."

   This choice determines whether Step C uses the **People Search** endpoint (names only) or **Export People with Email** endpoint (names + emails).

### Step B — Resolve company UUIDs

Query companies that need UUID resolution:
```sql
SELECT id, domain FROM companies WHERE ai_ark_account_id IS NULL AND domain IS NOT NULL
```

For companies missing `ai_ark_account_id`, use the AI Ark Company Search endpoint:
- `POST https://api.ai-ark.com/api/developer-portal/v1/companies`
- Search by domain to get the AI Ark company UUID
- Update `companies.ai_ark_account_id` with the result
- Batch and throttle per `references/ai-ark-api.md` (12 threads, rate limit: 15 req/sec)
- Save JSON backup before DB writes

Show progress: "Resolved X/Y company UUIDs (Z not found in AI Ark)."

### Step C — Pull contacts

**Before running at scale**, offer test batch:
- "Want to test with 50 companies first to see the results?"
- Show 10 sample contacts with name, title, company (+ email if export mode)
- **Hard gate** — user approves before running the rest

**Building the request:** Company UUIDs go inside `contact.company.current` (**not** `account.current`):
```json
{
  "contact": {
    "company": {
      "current": {"any": {"include": ["<company-uuid-1>", "<company-uuid-2>", "..."]}}
    },
    "departmentAndFunction": {"any": {"include": ["master_sales"]}},
    "seniority": {"any": {"include": ["director", "vp"]}}
  },
  "page": 0,
  "size": 100
}
```

**Both paths use People Search first** (`POST /v1/people`). The email path adds a second step.

---

#### Path 1: Names only (People Search)

Use the **People Search** endpoint — synchronous, no credit cost, no emails.

**Endpoint:** `POST https://api.ai-ark.com/api/developer-portal/v1/people`
- Batch 20 company UUIDs per request via `contact.company.current`, `size: 100`
- 12 concurrent threads (rate limit: 15 req/sec)
- Paginate if `totalPages > 1` — **stop when a page returns empty content**
- Cap at 10,000 results (100 pages)

Results come back immediately with name, title, seniority, department, LinkedIn.

---

#### Path 2: Names + verified emails (People Search → Export Single)

Two-step process. The bulk export/email-finder endpoints require a webhook, so we use the sync **Export Single Person** endpoint instead.

**Step 1: People Search** — same as Path 1 above. Collect all person IDs.

**Step 2: Export Single Person with Email** — for each person found:
- `POST https://api.ai-ark.com/api/developer-portal/v1/people/export/single`
- Body: `{"id": "<person-ai-ark-id>"}`
- Returns full profile + verified email synchronously
- 1 credit per contact (0 credits if no email found)
- Emails verified in real-time by BounceBan
- Response includes `email.output[0].address`, `email.output[0].status` (VALID/INVALID), `email.output[0].mx.provider` (microsoft/google/null)
- Returns `404` if no email found for that person
- Rate limit: 5 req/sec — use 4 concurrent threads with 0.3s delay
- Save JSON backup incrementally every 100 contacts

> **PARALLEL (100+ person IDs)**: After People Search completes (stays in main context),
> split person IDs into 2 chunks, spawn 2 agents.
> Each agent: 2 threads at ~2 req/sec (total: 4 req/sec, safely under 5 limit).
> Each agent saves to `~/Downloads/email_export_results_chunk{N}_{timestamp}.json` every 100 contacts (NO DB writes).
> Main context reads all result JSONs, proceeds to Step C.2 for insert.

---

### Step C.2 — Insert contacts

**Save JSON backup** of all results to `~/Downloads/` before DB writes.

Map response to `contacts` table:

| AI Ark field | DB column | Notes |
|---|---|---|
| `profile.first_name` | first_name | |
| `profile.last_name` | last_name | |
| `profile.full_name` | full_name | |
| `profile.title` | job_title | |
| `department.seniority` | seniority | |
| `department.departments[0]` | department | |
| `link.linkedin` | linkedin_url | |
| `email.output[0].address` | email | Path 2 only — NULL for names-only |
| `email.output[0].status` | email_status | Path 2 only — "VALID" / "INVALID" / NULL |
| `email.output[0].mx.provider` | email_provider | Path 2 only — "microsoft" / "google" / NULL |
| `id` | ai_ark_person_id | |
| `company.id` | company_id | Match via ai_ark_account_id → companies.id |

Insert with `ON CONFLICT (campaign, ai_ark_person_id) DO NOTHING`.

### Step D — Post-processing

After contact pull:
1. Show summary: X contacts found across Y companies (Z had no matches). If export mode: W with verified email, V without.
2. Run mandatory cleaning steps 4, 5 (name + title cleaning) on new contacts
3. Run junk lead detection (Step 6.5) on new contacts
4. If export mode: run email provider detection (Step 6) on new contacts
5. If search-only mode: offer to upgrade to export for emails — "Want to enrich these contacts with verified emails now?"
6. Sync company `custom_fields` to new contacts

---

## Master Database Search Flow

*Triggered by "Search master database" in Q2.*

1. Ask user for ICP criteria (industry, size, location, seniority, department, email provider, custom fields)
2. Query `master` DB with criteria + 90-day freshness filter
3. Show results with freshness indicators. Data >90 days flagged as stale.
4. **Hard gate** — user confirms which records to import
5. Upsert selected companies + contacts into client DB with chosen campaign name
6. If stale records imported, offer to re-enrich just those

---

## Step 9 — ICP Scoring

*Triggered by "ICP Scoring" under "Work with existing data" in Q2, or offered after enrichment steps complete.*

Score contacts against campaign-specific criteria to rank lead quality. Fully deterministic — no API calls, $0 cost, instant.

### Step 9A — Select campaign

Query campaigns with counts:
```sql
SELECT campaign, COUNT(*) as contacts, COUNT(email) as with_email
FROM contacts GROUP BY campaign ORDER BY campaign;
```

`AskUserQuestion` (single-select): which campaign to score?

### Step 9B — Define or load rubric

Check for existing rubric:
```sql
SELECT icp_rubric FROM campaign_configs WHERE campaign = '{campaign}';
```

**If rubric exists** → show it as a readable table, then `AskUserQuestion` (single-select):
1. **Use this rubric** — proceed to Step 9C
2. **Modify** — edit criteria, then save
3. **Start fresh** — discard and rebuild

**If no rubric** → conversational rubric builder:

1. `AskUserQuestion` (freetext) — **Header:** "ICP criteria" — **Question:** "Describe your ideal customer for this campaign. What makes a lead more qualified? (e.g., C-level exec, 100+ employees, based in the US, uses Salesforce)"

2. `AskUserQuestion` (single-select) — **Header:** "Weighting" — **Question:** "Should all criteria be worth equal points, or do you want to weight some higher?"
   - **Equal weights** — "Each criterion = 1 point. Score is count of criteria met (e.g., 3/5)."
   - **Variable weights** — "Assign different point values. More important criteria count more."

3. Claude translates the natural language description into structured criteria. For each criterion, determine:
   - Which table (`contacts` or `companies`) and field to check
   - Which operator to use
   - What values to match against

   **Available fields for criteria:**

   | Table | Field | Example values |
   |---|---|---|
   | contacts | seniority | c_suite, founder, owner, vp, director, head, manager, senior, mid-level, entry, intern, partner |
   | contacts | department | sales, marketing, engineering, finance, hr, operations, etc. |
   | contacts | job_title | freetext — use `contains` operator |
   | contacts | location_city | freetext |
   | contacts | location_state | freetext |
   | contacts | location_country | freetext (inconsistent — warn user: "US" vs "United States" etc.) |
   | contacts | email_provider | google, microsoft, other |
   | companies | size_min / size_max | integer |
   | companies | industry | freetext — use `contains` operator |
   | companies | custom_fields | any enrichment key (e.g., `has_crm`, `hiring_sales`, `cold_email_signal`, `product_category`, `platform`) |

   **Criterion types:**
   - `field_match` — check a standard column. Operators: `eq`, `in`, `gte`, `lte`, `contains`, `not_null`
   - `custom_field_match` — check a `custom_fields` JSONB key. Same operators, accesses via `custom_fields->>'key'`

4. If variable weights: ask point value per criterion via `AskUserQuestion` (freetext).

5. Show proposed rubric as readable table:
   ```
   ICP Scoring Rubric for "{campaign}":

   #  Criterion                Points  Type         Check
   1  C-Level or Founder       1       field_match  seniority IN (c_suite, founder, owner)
   2  100+ employees           2       field_match  size_min >= 100
   3  Based in US              1       field_match  location_country IN (United States, US)
   4  Uses Salesforce          1       custom_field field_match  crm_primary IN (Salesforce)
   ─────────────────────────────────────────────────────
   Max score: 5 points
   ```

6. **Hard gate** — `AskUserQuestion` (single-select): "Approve this rubric?"
   - **Approve** — save and proceed
   - **Modify** — edit criteria
   - **Add more criteria** — append additional criteria

7. Save rubric to `campaign_configs`:
   ```sql
   INSERT INTO campaign_configs (campaign, icp_rubric) VALUES ('{campaign}', '{rubric_json}')
   ON CONFLICT (campaign) DO UPDATE SET icp_rubric = '{rubric_json}', updated_at = NOW();
   ```

   **Rubric JSON format:**
   ```json
   [
     {"name": "C-Level or Founder", "points": 1, "type": "field_match", "table": "contacts", "field": "seniority", "operator": "in", "values": ["c_suite", "founder", "owner"]},
     {"name": "100+ employees", "points": 2, "type": "field_match", "table": "companies", "field": "size_min", "operator": "gte", "values": [100]},
     {"name": "Based in US", "points": 1, "type": "field_match", "table": "contacts", "field": "location_country", "operator": "in", "values": ["United States", "US"]},
     {"name": "Uses Salesforce", "points": 1, "type": "custom_field_match", "table": "companies", "field": "crm_primary", "operator": "in", "values": ["Salesforce"]}
   ]
   ```

### Step 9C — Dry run

Score 10 contacts as a preview. Write a Python script that:

1. Loads the rubric from `campaign_configs`
2. Queries 10 contacts in the campaign joined with their company:
   ```sql
   SELECT c.*, co.size_min, co.size_max, co.industry, co.custom_fields as company_custom_fields
   FROM contacts c
   LEFT JOIN companies co ON c.company_id = co.id
   WHERE c.campaign = '{campaign}'
   LIMIT 10;
   ```
3. Evaluates each criterion per contact in Python:
   - `field_match`: check the column value against operator + values
   - `custom_field_match`: check `custom_fields->key` against operator + values
   - NULL field = 0 points (criterion not met)
4. Shows results:

   ```
   Preview — 10 contacts scored:

   Name              Company         Score  C-Level  100+emp  US-based  Salesforce
   Sarah Chen        Acme Corp       4/5    YES(1)   YES(2)   YES(1)    NO(0)
   Mike Johnson      Beta LLC        2/5    NO(0)    YES(2)   NO(0)     NO(0)
   ...
   ```

**Hard gate** — `AskUserQuestion` (single-select): "Results look right?"
- **Proceed** — score all contacts
- **Modify rubric** — go back to Step 9B
- **Cancel** — stop

### Step 9D — Score all contacts

Write a Python script that:

1. Loads rubric from `campaign_configs`
2. Queries all unscored contacts in the campaign:
   ```sql
   SELECT c.id, c.full_name, c.seniority, c.department, c.job_title,
          c.location_city, c.location_state, c.location_country,
          c.email_provider, c.custom_fields,
          co.size_min, co.size_max, co.industry, co.custom_fields as company_cf
   FROM contacts c
   LEFT JOIN companies co ON c.company_id = co.id
   WHERE c.campaign = '{campaign}'
     AND (c.custom_fields->>'icp_scored_at') IS NULL;
   ```
3. For each contact, evaluate all criteria in Python:
   - **Operator logic:**
     - `eq`: `str(field_value).lower() == str(target).lower()`
     - `in`: `str(field_value).lower() in [str(v).lower() for v in values]`
     - `gte`: `float(field_value) >= float(values[0])` (NULL = fail)
     - `lte`: `float(field_value) <= float(values[0])` (NULL = fail)
     - `contains`: `str(target).lower() in str(field_value).lower()`
     - `not_null`: `field_value is not None and field_value != ''`
   - Build breakdown dict: `{criterion_name: points_awarded}`
   - Compute `icp_score` (sum of awarded points), `icp_max` (sum of all possible points), `icp_percentage` (round(score/max * 100))

4. **Save JSON backup** to `~/Downloads/icp_scores_{campaign}_{timestamp}.json` before DB write

5. Update contacts:
   ```sql
   UPDATE contacts SET
     custom_fields = COALESCE(custom_fields, '{}'::jsonb) || '{
       "icp_score": {score},
       "icp_max": {max},
       "icp_percentage": {pct},
       "icp_breakdown": {breakdown_json},
       "icp_scored_at": "{timestamp}"
     }'::jsonb,
     updated_at = NOW()
   WHERE id = '{contact_id}';
   ```
   Batch 500 updates via `psycopg2.extras.execute_values`.

6. Show progress: "Scored X/Y contacts..."

### Step 9E — Summary report

```
ICP Scoring Complete — "{campaign}"

Scored: {N} contacts
Rubric: {M} criteria, max {max_pts} points

Score Distribution:
  {max}/{max} (Perfect):  {n} contacts ({pct}%)
  {max-1}/{max}:          {n} contacts ({pct}%)
  ...
  0/{max}:                {n} contacts ({pct}%)

Criteria Hit Rates:
  {criterion_1}:  {pct}% of contacts met this
  {criterion_2}:  {pct}%
  ...
```

Then `AskUserQuestion` (single-select):
- **Filter/export by score** — "Show or export contacts above a score threshold"
- **Done** — return to main menu

If filter/export: `AskUserQuestion` (freetext): "Minimum score to include? (e.g., 3)" → query and show/export.

### Rescoring

When the user modifies a rubric (Step 9B with existing rubric), after saving the updated rubric:

1. Clear existing scores:
   ```sql
   UPDATE contacts SET
     custom_fields = custom_fields - 'icp_score' - 'icp_max' - 'icp_percentage' - 'icp_breakdown' - 'icp_scored_at',
     updated_at = NOW()
   WHERE campaign = '{campaign}' AND custom_fields ? 'icp_scored_at';
   ```
2. Re-run Step 9D automatically
