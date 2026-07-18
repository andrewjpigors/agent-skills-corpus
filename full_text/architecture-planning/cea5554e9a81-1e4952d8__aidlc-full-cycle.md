---
name: aidlc-full-cycle
description: >
  AI-DLC: Full Cycle is the complete human-led AI development methodology for taking any project
  from zero to shipped — covering feasibility, specs, build planning, execution governance, and
  knowledge continuity. Trigger this skill whenever a user starts a new project from scratch,
  presents an RFP or idea paragraph, asks how to plan an AI-driven build, wants to structure a
  consulting engagement, asks "where do I start", needs a phased build plan, wants to know if
  something can be built, or references AI-DLC. Also trigger when a user says things like
  "we have a new client project", "I have an idea I want to build", "help me plan this out",
  "how do we approach this engagement", or "what's our build plan". This skill governs the
  entire project lifecycle — the Knowledge Base is initialized first and every phase writes to it.
  The human is the orchestrator. The agents execute. This skill keeps it that way.
license:
  holder: S3 Technology
  contact: don@s3technology.io
  terms: Apache-2.0 — see LICENSE at suite root
  copyright: "Copyright (c) 2026 S3 Technology"
---

# AI-DLC: Full Cycle
### The Human-Led AI Development Lifecycle
*Co-authored by S3 Technology & EX Squared*

---

## The Covenant

AI didn't flatten the playing field. It raised the ceiling for people who know what they're doing.

A skilled orchestrator with AI agents has 10x the execution capacity they had before. An unskilled one has 10x the ability to build the wrong thing faster.

**This methodology exists to keep the human in the lead.** The orchestrator sets direction, makes decisions, signs off on gates, and owns the outcome. The agents execute with precision inside boundaries the human defines. Neither works without the other.

Three principles govern everything that follows:

1. **The orchestrator is irreplaceable.** Strategy, judgment, risk tolerance, client relationships, sequencing — these are human skills. AI amplifies them. It does not substitute for them.
2. **Specs are the contract.** Between the human and the agents. Between the consultant and the client. Between today's team and the team that inherits this project in six months.
3. **Every decision leaves a record.** The Knowledge Base is not optional. It is the spine of the methodology. Without it, the project exists only in the memory of the people and agents who built it — and that memory is unreliable.

---

## The Knowledge Base — Initialized First, Lives Forever

**Before any phase begins, the KB is initialized.**

The AI-DLC Knowledge Base is the living memory of the project. Every output of every phase is a KB write. Nothing happens in the project without a KB entry.

### What the KB Is

A semantically searchable, append-only record of everything that happened — in the order it happened — with enough context to reconstruct any decision.

### What Goes In (Everything)

- Every spec version (v1 through vN — superseded entries are tagged, never deleted)
- Every feasibility assessment and Go/No-Go decision
- Every pivot and the reasoning behind it
- Every risk called, and whether it materialized
- Every feature: designed, built, deferred, killed — with why
- Every agent session summary (Knowledge Dump output)
- Every stage gate result — passed, failed, what had to change
- Every Build vs. Integrate decision
- Every client sign-off
- Every blocker, its classification, its resolution

### Two Write Paths — Tagged at Creation

Every KB entry is tagged at the moment it's written:

| Tag | Meaning |
|-----|---------|
| `internal` | Full fidelity — agent dumps, raw pivots, internal risk assessments |
| `deliverable` | Professional artifact — suitable for client-facing KB export |

Never retroactively sanitize. Tag correctly at write time.

### Single-Writer Model

**Only the CLI agent (CTO) writes to the KB.** This is a hard rule across all AI-DLC projects.

All other agents — CPO, CRO, CDO, CQO, CCO — produce session context exports during their session-close. These exports are handed to the CLI agent, who:

1. Reads and parses the strategic agent's context export
2. Compares it to his own session context (reconciliation, not blind merge)
3. Identifies conflicts between strategic and engineering context
4. Resolves conflicts with orchestrator input (or flags them)
5. Writes ONE merged entry to the KB

**Why single-writer:**
- Prevents conflicting KB entries from different agents
- Gives the CTO control over what enters institutional memory
- Ensures technical accuracy (the CTO validates strategic decisions against implementation reality)
- Creates a natural quality gate — context must survive reconciliation to persist

**Enforcement:** Session-close Path A explicitly blocks KB writes. Session-open reports KB authority in the agent brief ("Writer" for CLI, "Exporter" for Desktop). The orchestrator sees this and knows the handoff flow.

### Ownership

**The firm owns the KB.** Always. The client receives the outputs of the project — specs, shipped software, exports. The KB is a firm asset and a premium add-on offering. It grows with the project and outlives any individual engagement.

### Technical Implementation

The KB follows a graduated path — start with markdown, upgrade when the project demands it. The level is selected during Phase 0, Step 0.1.

```
Level 1 — Local Markdown         → docs/kb/ folder, structured entries, no infrastructure
Level 2 — Local Markdown + Search → Light local indexing for faster retrieval
Level 3 — Static Site             → Vitepress/Astro, KB becomes a shareable URL
Level 4 — Hosted Vector DB        → Supabase / Pinecone / pgvector / Weaviate, full FCE
```

Every level uses the same entry format and the same fields. At Levels 1–3, these live in YAML frontmatter. At Level 4, they map to table columns:
`kb_entries(id, project_id, phase, entry_type, visibility, content, embedding, decay, created_at, supersedes, superseded_by, author)`

Migration between levels is forward-compatible — every markdown entry maps directly to a database row. Historical entries are re-embedded on import to Level 4. See `references/kb-static-site.md` for Level 3 setup and `references/kb-schema.md` for Level 4 schema.

### KB Level Selection and Opt-Out

During Phase 0, Step 0.1, the orchestrator selects the KB level. **The default recommendation is Level 4 with FCE.**

The agent presents:

```
KB Level Selection — this project needs a knowledge base.

Recommended: Level 4 (Hosted Vector DB + FCE)
- Semantic search from Day 0
- Session fingerprinting, conflict detection, decay scoring
- Replay anchors for crash recovery
- Dependency tracking across sessions
- Requires: Supabase/pgvector (or equivalent), embedding API key

Alternative: Level 1-2 (Local Markdown)
- File-based KB, no infrastructure
- Manual search only (grep, file browsing)
- No semantic retrieval, no decay scoring, no conflict detection
- Suitable for: short engagements, no-infrastructure constraints

If you want Level 1-2 instead of Level 4, acknowledge with:
"No thanks, we're good with MDs for this project."

This acknowledgement will be tracked in CLAUDE.md.
```

**If the orchestrator chooses Level 4 (default):** Proceed with full FCE. Initialize the KB tables, embedding pipeline, and search functions during Phase 0.

**If the orchestrator opts out ("No thanks, we're good with MDs"):**

1. Record the opt-out in the project's `CLAUDE.md`:

```markdown
## KB Level

**Level:** 1-2 (Local Markdown)
**FCE:** Opted out
**Acknowledged by:** [orchestrator name] on [YYYY-MM-DD]
**Reason:** [brief reason if given, or "No reason provided"]
```

2. The opt-out is tracked — not questioned, not re-asked. The agent respects the decision.
3. Session-open and session-close still run, but they use markdown file loading instead of vector queries.
4. FCE enhancements (fingerprinting, decay, conflict detection, replay anchors) are disabled — they require Level 4.
5. The agent MAY mention the upgrade path once if a relevant situation arises (e.g., "This is the kind of context loss that Level 4 KB prevents"), but does not nag.

**Opt-out is permanent for the engagement unless the orchestrator explicitly requests an upgrade.**

### FCE — FORGE'd Context Engine

The FORGE'd Context Engine (FCE) is the standard knowledge integrity system for all Level 4 AI-DLC projects. It adds five capabilities on top of semantic retrieval:

1. **Session Fingerprinting** — Every session-open generates a hash of loaded KB entries. Session-close compares what was loaded against what was produced to detect silent drift (agent ignoring its own context).

2. **Decision Decay Scoring** — Every KB entry is tagged with a decay class (`permanent`, `long`, `medium`, `short`) reflecting how long it stays relevant. Session-open deprioritizes stale entries automatically. A 4-month-old sprint decision doesn't compete with a 4-month-old architecture invariant.

3. **Conflict Detection on Write** — Before any KB write, the CLI agent runs a similarity search against existing entries. Contradictions are flagged to the orchestrator. Contradictions never enter the KB silently.

4. **Cross-Session Dependency Tracking** — Each session records which KB entries it consumed and which it produced. This creates a provenance graph: if a research finding changes, every downstream implementation decision that depended on it is flagged for re-evaluation. Since only the CTO writes to KB, the dependency chain is clean — no conflicting write sources.

5. **Replay Anchors** — Every session-close writes a compressed checkpoint (git state, work state, open questions, critical context). If a session crashes or is interrupted, the next session-open can resume from the anchor instead of starting cold.

**FCE is the default for all new AI-DLC projects at Level 4.** The five enhancements are lightweight — they add metadata fields to existing writes and queries, not new infrastructure.

### KB Entry Format

```markdown
---
kb_id: KB-YYYYMMDD-HHMM
phase: [0|1|2|3|4]
type: [feasibility|spec|decision|risk|feature|session|gate|blocker|signoff]
visibility: [internal|deliverable|both]
decay: [permanent|long|medium|short]
supersedes: [kb_id or null]
superseded_by: [kb_id or null]
author: [human name or agent name]
---

## [Entry Title]

**Context:** [What situation prompted this entry]

**Content:** [The actual record]

**Decision/Outcome:** [What was decided or what happened]

**Impact:** [What this changes going forward]
```

### Decision Decay Classification

Every KB entry gets a decay class at write time:

| Decay Class | Half-Life | Examples |
|-------------|-----------|---------|
| `permanent` | Never expires | Embedding model choice, legal compliance rules, architectural invariants, methodology rules |
| `long` | 3-6 months | Stack decisions, major component APIs, database schema, permission model |
| `medium` | 1-3 months | Specific component prop APIs, route structures, third-party integration details |
| `short` | 1-4 weeks | Sprint-specific decisions, temporary workarounds, current blockers, WIP state |

If unsure, default to `medium`. The orchestrator can override. `ephemeral` content (debugging noise, transient state) should NOT be written to the KB at all — see "What NOT to Write" in session-close.

---

## KB Schema Reference

**The KB is the spine. Without it the project is paralyzed.** Any agent provisioning the KB on a new engagement must implement this schema exactly. Do not improvise. Do not simplify. This schema is designed to be multi-tenant, portal-ready, and extensible from day one.

### Core Tables

```sql
-- Every human or agent that can access the system
-- Managed by Supabase Auth (auth.users) — do not duplicate
-- Reference auth.uid() in RLS policies

-- Firms / consulting organizations
create table firms (
  id           uuid primary key default gen_random_uuid(),
  name         text not null,
  owner_id     uuid not null references auth.users(id),
  created_at   timestamptz default now()
);

-- Clients belong to a firm
create table clients (
  id               uuid primary key default gen_random_uuid(),
  firm_id          uuid not null references firms(id) on delete cascade,
  name             text not null,
  portal_user_id   uuid references auth.users(id),  -- nullable until portal purchased
  portal_enabled   boolean default false,
  created_at       timestamptz default now()
);

-- Projects belong to a client
create table projects (
  id           uuid primary key default gen_random_uuid(),
  client_id    uuid not null references clients(id) on delete cascade,
  name         text not null,
  status       text default 'active',  -- active | paused | shipped | archived
  current_phase int default 0,
  created_at   timestamptz default now()
);

-- The KB itself — every entry for every project lives here
create table kb_entries (
  id              uuid primary key default gen_random_uuid(),
  project_id      uuid not null references projects(id) on delete cascade,
  phase           int not null,                      -- 0–4
  entry_type      text not null,                     -- see type taxonomy below
  visibility      text not null default 'internal',  -- internal | deliverable | both
  content         text not null,
  embedding       vector(1024),                      -- pgvector, populated on insert (dimension matches project's embedding model)
  decay           text not null default 'medium'     -- permanent | long | medium | short
                  check (decay in ('permanent', 'long', 'medium', 'short')),
  author          text not null,                     -- human name or agent name
  supersedes      uuid references kb_entries(id),    -- points to entry this replaces
  superseded_by   uuid references kb_entries(id),    -- populated when this is replaced
  consumed_ids    uuid[] default '{}',               -- FCE: KB entries consumed to make this decision
  produced_by_session text,                          -- FCE: session ID that created this entry
  created_at      timestamptz default now()
);

-- Indexes for performance
create index kb_entries_project_id_idx on kb_entries(project_id);
create index kb_entries_phase_idx on kb_entries(phase);
create index kb_entries_entry_type_idx on kb_entries(entry_type);
create index kb_entries_decay_idx on kb_entries(decay);
create index kb_entries_embedding_idx on kb_entries
  using ivfflat (embedding vector_cosine_ops) with (lists = 100);
```

**Note on embedding dimensions:** The default is `vector(1024)` for Voyage voyage-3-large. Projects using other embedding models should adjust dimensions accordingly (e.g., 1536 for OpenAI, 3072 for OpenAI large). The model choice is recorded in the project's `CLAUDE.md` and `DECISION_LOG.md`.

### Entry Type Taxonomy

| Type | Phase | Visibility Default | Description |
|------|-------|--------------------|-------------|
| `intake` | 0 | internal | Raw input verbatim + source |
| `feasibility` | 0 | both | Feasibility assessment + Go/No-Go |
| `blocker` | 0–2 | internal | NOT YET / NOT US / NOT RIGHT classification |
| `spec` | 1 | both | Spec version (every version kept) |
| `decision` | 1–3 | both | Build vs. integrate, architecture, product |
| `risk` | 0–3 | both | Risk register entry |
| `dependency` | 1–2 | deliverable | Dependency map entry |
| `build_plan` | 2 | both | Phase architecture, timeline, critical path |
| `gate` | 2–3 | both | Stage gate result — passed/failed + notes |
| `signoff` | 1–3 | deliverable | Human or client sign-off record |
| `session` | 3 | internal | Agent Knowledge Dump — session summary |
| `feature` | 1–3 | both | Feature record — designed/built/deferred/killed |

### Row Level Security

Enable RLS on every table. These policies are the security boundary — not application logic.

```sql
alter table kb_entries enable row level security;

-- Firm owner sees all entries across all their clients and projects
create policy "firm_owner_full_access"
on kb_entries for all
using (
  project_id in (
    select p.id from projects p
    join clients c on c.id = p.client_id
    join firms f on f.id = c.firm_id
    where f.owner_id = auth.uid()
  )
);

-- Client portal user sees only deliverable/both entries for their project
-- Only active when portal_enabled = true
create policy "client_portal_read"
on kb_entries for select
using (
  project_id in (
    select p.id from projects p
    join clients c on c.id = p.client_id
    where c.portal_user_id = auth.uid()
    and c.portal_enabled = true
  )
  and visibility in ('deliverable', 'both')
);
```

Apply the same pattern to `projects`, `clients`, and `firms`.

### Enabling a Client Portal

When a client purchases KB access:

```sql
-- 1. Create their auth account (Supabase Auth invite or manual)
-- 2. Link and enable
update clients
set portal_user_id = '[their auth.users uuid]',
    portal_enabled = true
where id = '[client_id]';
```

No schema migration. No new tables. The access tier was always there, dormant until purchased.

---

## KB Memory Model — FCE (FORGE'd Context Engine)

**The Internal/Deliverable tags control who sees what. The FCE controls how agents find what they need — and how knowledge maintains its integrity over time.**

These are separate concerns. Visibility is a filter. Retrieval is a ranked search. Integrity is the set of checks (conflict detection, drift detection, decay scoring) that keep the KB trustworthy. All three must work correctly for the KB to be useful.

### What FCE Means in This Context

Standard RAG (Retrieval Augmented Generation) fetches semantically similar entries and hands them to the agent. That's the floor, not the ceiling.

FCE adds **integrity and awareness layers on top of semantic similarity** so agents get the most relevant, most current, most contextually appropriate entries — not just the most lexically similar ones — and so the KB detects and prevents knowledge corruption.

### The Retrieval Stack

Every KB query passes through these layers in order:

```
1. SEMANTIC SIMILARITY   — vector cosine search against the query embedding
2. DECAY-AWARE SCORING   — entries scored by decay class (permanent > long > medium > short)
3. RECENCY WEIGHTING     — newer entries score higher within the same decay class
4. PHASE PROXIMITY       — entries from the current/adjacent phases score higher
5. SUPERSESSION FILTER   — superseded entries are flagged, not hidden
6. DEPENDENCY CHAIN      — entries upstream of current intent are boosted
7. VISIBILITY FILTER     — Internal / Deliverable gate applied last
                        ↓
                    RESULTS + SESSION FINGERPRINT
```

Superseded entries are never hidden — they surface with a `[SUPERSEDED by KB-xxx]` tag. An agent that reads "Spec v1 said X" needs to also see "Spec v3 superseded this, now says Y." Hiding old entries produces hallucinations.

### Two Memory Types — Agents Must Distinguish

| Memory Type | Scope | Query At | Content |
|-------------|-------|----------|---------|
| **Project Memory** | Permanent, full project history | Session open, always | All KB entry types |
| **Agent Memory** | Session-scoped, this agent's recent work | Session open, filtered by author | `session` entries by this agent |

**Project memory** answers: "What has been decided on this project?"
**Agent memory** answers: "What did I personally work on last time, and where did I leave off?"

Both are stored in `kb_entries`. Agent memory is just a filtered view: `where author = '[this agent]' order by created_at desc limit 10`.

### Standard Session Open Query

Every agent runs this query pattern at session open. Adapt the embedding to your session context string.

```sql
-- Step 1: Project memory with decay-aware scoring
SELECT
  id, phase, entry_type, visibility, content, created_at,
  superseded_by, decay,
  1 - (embedding <=> '[session context embedding]') AS raw_similarity,
  -- Decay-adjusted effective similarity
  (1 - (embedding <=> '[session context embedding]'))
  * CASE decay
      WHEN 'permanent' THEN 1.0
      WHEN 'long' THEN GREATEST(0.5, 1.0 - (EXTRACT(EPOCH FROM now() - created_at) / (180 * 86400)) * 0.5)
      WHEN 'medium' THEN GREATEST(0.5, 1.0 - (EXTRACT(EPOCH FROM now() - created_at) / (90 * 86400)) * 0.5)
      WHEN 'short' THEN GREATEST(0.3, 1.0 - (EXTRACT(EPOCH FROM now() - created_at) / (30 * 86400)) * 0.7)
      ELSE 0.8
    END
  * 0.6                                                                   -- 60% semantic relevance (decay-adjusted)
  + (1 / (EXTRACT(EPOCH FROM now() - created_at) / 86400 + 1)) * 0.3     -- 30% recency
  + CASE WHEN phase >= [current_phase] - 1 THEN 0.1 ELSE 0 END           -- 10% phase proximity
  AS effective_score
FROM kb_entries
WHERE project_id = '[project_id]'
  AND superseded_by IS NULL
  AND visibility IN ('internal', 'both')
  AND embedding IS NOT NULL
ORDER BY effective_score DESC
LIMIT 20;

-- Step 2: Agent memory — what this agent did last session
SELECT id, content, created_at
FROM kb_entries
WHERE project_id = '[project_id]'
  AND entry_type = 'session'
  AND author = '[agent_name]'
ORDER BY created_at DESC
LIMIT 3;

-- Step 3: Generate session fingerprint (collect loaded entry IDs)
-- Store hash of all loaded IDs for drift detection at session-close
```

### What Agents Do With the Results

After querying, the agent synthesizes the results into a session brief before reporting to the orchestrator:

```
Project context: [2-3 sentences from top project memory hits]
Recent decisions: [any decision entries in top results]
Stale entries: [any entries flagged as possibly stale by decay scoring]
Context chain: [upstream decisions that inform current intent]
Active risks: [any open risk entries]
My last session: [summary from agent memory query]
Session fingerprint: [short hash of loaded entry IDs]
Current phase: [from projects.current_phase]
```

This is what the orchestrator sees at session open. Not a raw dump of KB entries — a synthesized brief. The agent does the synthesis, not the human.

### Embedding on Write

Every `kb_entries` insert must trigger embedding generation. On Supabase, implement this as an Edge Function triggered on insert:

```
on insert → kb_entries
  → generate embedding(content) via project's configured embedding model
    (default: Voyage voyage-3-large, 1024 dims — or as specified in CLAUDE.md)
  → update kb_entries set embedding = [vector] where id = new.id
  → run conflict detection (similarity search against existing entries)
  → flag contradictions if detected
```

**Embedding model is project-configurable.** The default recommendation is Voyage voyage-3-large (1024 dimensions) for best retrieval quality at optimal index size. Projects may use other models. The model choice is recorded in `CLAUDE.md` and `DECISION_LOG.md`.

**Never insert a KB entry without triggering embedding.** An entry without an embedding is invisible to semantic search. It exists in the database but cannot be found by agents.

### Conflict Detection on Write

Before any KB write, the CTO (single-writer) runs a similarity search against existing entries:

1. Generate embedding for the new entry's content
2. Query: `search_kb(embedding, threshold: 0.75, match_count: 20)`
3. For each high-similarity result, compare semantically:
   - **Extends** existing entry → tag as `extends: [existing_id]`
   - **Supersedes** existing entry → tag with `supersedes`, update old entry's `superseded_by`
   - **Contradicts** existing entry without acknowledging change → **flag for orchestrator**

**Contradictions never enter the KB silently.** The CTO reports the conflict, the orchestrator decides.

### Replay Anchors

Every session-close writes a compressed checkpoint — the minimum context needed to resume the session state if it's interrupted.

```markdown
## Replay Anchor — [YYYY-MM-DD]

### Git State
- Branch: [current branch]
- Last commit: [hash] — [message]
- Uncommitted changes: [list or "clean"]

### Work State
- Current task: [ticket ID + what's in progress]
- Next task: [ticket ID + what's next]
- Block position: [e.g., "Block 2, Task 6 of 8"]

### Open Questions
[Numbered list of unresolved questions]

### Test State
- Passing: [N] / Failing: [N]
- New tests this session: [N]

### Critical Context
[2-5 bullets: non-obvious things a new session MUST know]
```

Session-open checks for replay anchors before loading KB context. A found anchor is presented to the orchestrator: "Resume from anchor, or start fresh?"

---

## Phase 0 — Intake & Feasibility

*Cold start. Raw input. Nothing assumed. The human makes the first call.*

### Input
Accepts any of: a paragraph of an idea, an RFP document, a client email, a napkin sketch, meeting notes. No format required.

### Step 0.1 — Initialize the KB

**Start writing. Upgrade when the project demands it.**

The KB is the spine of the methodology. It starts as markdown files in `docs/kb/` — no infrastructure required, no setup friction, no barriers. Every entry you write at Level 1 migrates forward when you're ready to upgrade.

**Default path — Level 4 (FCE) is recommended.** Present the KB Level Selection prompt (see "KB Level Selection and Opt-Out" above). If the orchestrator opts out, proceed with Level 1. If the orchestrator accepts the default (or explicitly requests Level 4), proceed to provision.

**If Level 1 (opted out or cold start):**

Create the KB structure and start writing immediately:

```
docs/
  kb/
    KB-INDEX.md          ← Master index, updated as entries are added
    KB-YYYYMMDD-HHMM-phase0-intake.md
    KB-YYYYMMDD-HHMM-phase0-feasibility.md
    ...
  exports/
    YYYY-MM-DD/
```

No warnings. No friction. Write the first entry and move to Step 0.2.

---

**If Level 4 (default recommendation):** Proceed to provision. See `references/kb-schema.md` for the full schema, RLS policies, and embedding configuration. Write the first KB entry once the connection is confirmed.

**If Level 3 (Static Site):** See `references/kb-static-site.md` for Vitepress setup, deployment, and visibility filtering.

**When upgrading from Level 1 to Level 4 later:** The markdown files map directly to `kb_entries` rows. YAML frontmatter fields match the table columns. Historical entries are re-embedded on import. The migration path is documented in `references/kb-static-site.md`.

---

**Once KB path is confirmed (any level), write the first entry:**
```
kb_id: KB-[timestamp]-phase0-intake
type: intake
visibility: internal
decay: permanent
content: Raw input verbatim + source type + KB level decision
```

### Step 0.2 — Idea Compression

Compress the input to three sentences. No more.

```
Problem:   [One sentence. What is broken or missing?]
Solution:  [One sentence. What does this build do about it?]
Who cares: [One sentence. Who needs this and why do they pay for it?]
```

Present to the human. Do not proceed until they confirm or correct this compression. **If you can't compress it to three sentences, the idea isn't clear enough yet.** Keep asking.

### Step 0.3 — Feasibility Assessment

Evaluate on three axes. Be direct. Do not soften.

**Axis 1: Technical**
- Can this be built with current technology?
- Are there unproven technical assumptions? Name them.
- What is the hardest technical problem in this build?
- Does the team have the required skill sets? (See Skills Inventory below)

**Axis 2: Commercial**
- Is there a clear value proposition?
- Who pays, and why?
- Is the market timing defensible?
- What does the competitive landscape look like?

**Axis 3: Organizational**
- Does the team have the capacity to execute?
- Are there regulatory, compliance, or legal dependencies?
- Are there third-party dependencies outside the team's control?
- Is the timeline realistic given the scope?

### Step 0.4 — Skills Inventory

Based on the project type detected from the input, list the human skill sets required:

| Skill Set | Required | Present | Gap |
|-----------|----------|---------|-----|
| [e.g. Backend engineering] | Yes | ? | ? |
| [e.g. UI/UX design] | Yes | ? | ? |
| [e.g. Data engineering] | ? | ? | ? |

Ask the human to confirm what's present. Gaps become risks.

### Step 0.5 — The Can't-Build Protocol

If any feasibility axis fails, classify the blocker. This is a hard call, not a soft exit.

**NOT YET** — A dependency isn't resolved. The build is sound but something must happen first.
→ Name the blocker explicitly
→ Assign it an owner
→ Define the exact condition that unlocks the build
→ Set a review date
→ Write to KB as `type: blocker`
→ This becomes a pre-work ticket, not a stop

**NOT US** — A capability gap exists that the current team can't fill.
→ Document the gap
→ Define what hiring, partnering, or subcontracting resolves it
→ Escalate to leadership
→ Write to KB as `type: blocker`
→ This becomes a staffing decision, not a stop

**NOT RIGHT** — The idea itself has a fatal flaw that no amount of execution fixes.
→ This is the rare one. Reserve it for genuine fatal flaws.
→ Document the flaw with evidence, not opinion
→ Present to the client with specificity
→ Offer to redirect toward what would work
→ Write to KB as `type: decision, visibility: deliverable`
→ No project dies quietly. Every stop has a paper trail and a named decision-maker.

**"NOT RIGHT" should be rare.** If you're reaching for it, pressure-test whether this is actually "NOT YET" or "NOT US" first. With modern HITL AI orchestration, genuine capability blockers are uncommon — most "can't build" instincts are actually sequencing or staffing problems in disguise.

### Step 0.6 — Go / No-Go

Present the assessment to the human:

```
FEASIBILITY SUMMARY
───────────────────
Technical:       [GO / CONDITIONAL / BLOCKED]
Commercial:      [GO / CONDITIONAL / BLOCKED]
Organizational:  [GO / CONDITIONAL / BLOCKED]

Blockers identified: [N]
Skills gaps: [N]

Recommendation: [GO / CONDITIONAL GO / STOP]
Reasoning: [2-3 sentences]
```

**Human signs off here.** No phase begins without a Go decision.

Write Go/No-Go to KB: `type: feasibility, visibility: both, decay: permanent`

---

## Phase 1 — Discovery & Spec

*From approved idea to signed-off documentation.*

**Read `/mnt/skills/user/aidlc-specs/SKILL.md` before executing this phase.**

The aidlc-specs skill executes here in full — but it now has Phase 0 context feeding it. Pre-populate the discovery interview with everything already known from feasibility. Only ask about gaps.

### Additions to aidlc-specs Output

Beyond the standard aidlc-specs deliverables (PRD, Glossary, Risks, Acceptance Criteria, Feature Specs), Phase 1 produces:

**Dependency Map** — `docs/DEPENDENCY_MAP.md`
What must exist before what. Explicit sequencing. Format:
```
[Feature/Component] → depends on → [Feature/Component/External]
[External dependency] → owned by → [party] → status → [confirmed/assumed/unknown]
```

**Build vs. Integrate Decisions** — section in PRD or `docs/BUILD_VS_INTEGRATE.md`
For each major component: is this a custom build or an existing tool/API/platform?

| Component | Decision | Rationale | Risk if Wrong |
|-----------|----------|-----------|---------------|
| Auth | Integrate (Supabase Auth) | Commodity problem, solved | Low |
| Matching algorithm | Build | Core IP, no off-shelf fit | High |

**Skills Inventory Update** — update the Phase 0 table with spec-informed requirements

### KB Writes — Phase 1

Every spec version is a KB entry. When Spec v1 is superseded by Spec v2:
- Spec v1 entry gets `superseded_by: [v2 kb_id]`
- Spec v2 entry gets `supersedes: [v1 kb_id]`
- Both remain in the KB. Nothing is deleted.

Every Build vs. Integrate decision is a KB entry: `type: decision, decay: long`

### Human Gate — Phase 1

Client or stakeholder signs off on specs before Phase 2 begins.

Sign-off is a KB entry: `type: signoff, visibility: deliverable, decay: permanent`

---

## Phase 2 — Build Planning

*From signed-off specs to an executable, phased roadmap.*

This is the phase that determines whether the project succeeds or fails. Specs tell you what to build. The build plan tells you in what order, by whom, at what risk, and how you'll know each phase is done.

### Step 2.1 — Phase Architecture

Sequence the build foundation-first. The rule is absolute: **you do not build the roof before the walls.**

Ask: what has to be true in Phase N before Phase N+1 can start?

```
Phase 1: [Name] — Foundation
  Delivers: [what exists that didn't before]
  Required before Phase 2: [specific conditions]
  Exit criteria: [verifiable checklist]

Phase 2: [Name] — [Theme]
  Delivers: [what exists]
  Required before Phase 3: [specific conditions]
  Exit criteria: [verifiable checklist]
  ...
```

Common foundation-first sequencing rules:
- Auth and permissions before any user-facing feature
- Data model and storage before business logic
- Core API contracts before UI
- Third-party integrations before features that depend on them
- Instrumentation (logging, error tracking) before going to production

### Step 2.2 — Timeline Estimation

Size effort per feature, per phase. Use confidence ranges — not fake precision.

| Feature | Effort Estimate | Confidence | Phase | Notes |
|---------|----------------|------------|-------|-------|
| Auth | 3–5 days | High | 1 | Using existing auth library |
| Core data model | 5–8 days | Medium | 1 | Schema design needs review |
| [Feature] | 8–15 days | Low | 2 | Technical approach unproven |

**Confidence levels:**
- **High** — we've built this before, dependencies are clear, no unknowns
- **Medium** — generally familiar territory, some assumptions
- **Low** — new problem, unproven approach, or external dependencies

Low-confidence items are risks by definition. Flag them.

Phase timeline = sum of estimates + risk buffer per phase (15% minimum, 30% if low-confidence items present)

### Step 2.3 — Risk Register

Every risk from Phase 0 and Phase 1 carries forward. Add new risks identified during planning.

Each risk entry:

| ID | Risk | Likelihood | Impact | Owner | Mitigation | Trigger | Status |
|----|------|-----------|--------|-------|-----------|---------|--------|
| R-001 | [risk] | H/M/L | H/M/L | [name] | [action] | [what signals this is happening] | Open |

Write Risk Register to KB: `type: risk, visibility: both, decay: long`

### Step 2.4 — Critical Path

Which items block everything else? These get done first, no exceptions.

```
CRITICAL PATH
─────────────
[Item] → blocks → [Item] → blocks → [Item]

Critical path length: [N] days
Float available: [N] days
```

### Step 2.5 — Agent Allocation Plan

Which agents work which tracks? What runs in parallel? What can't?

| Agent/Role | Track | Phase | Owns | Cannot touch |
|-----------|-------|-------|------|-------------|
| [Agent name] | A | 1–2 | [files/features] | [explicit exclusions] |
| [Agent name] | B | 1 | [files/features] | [explicit exclusions] |

Parallelization rules:
- Parallel tracks must have non-overlapping file ownership
- Shared files require a designated owner and explicit merge protocol
- No agent works without a ticket

### Step 2.6 — Stage Gates

Each phase ends with a stage gate. The gate is a checklist. The phase does not close until the checklist passes. The human signs off.

```
PHASE [N] STAGE GATE
────────────────────
Technical:
  [ ] All features in scope are complete
  [ ] Test baseline is green
  [ ] Analyzer/linter passes (0 errors)
  [ ] No open critical bugs

Product:
  [ ] All Gherkin ACs for this phase pass
  [ ] Stakeholder demo complete
  [ ] Sign-off received

Knowledge:
  [ ] All session Knowledge Dumps written to KB
  [ ] All decisions documented
  [ ] KB-INDEX updated
  [ ] Risk Register updated
```

Write Build Plan to KB: `type: decision, visibility: both, decay: long`

### Step 2.7 — Velocity Anchor Tuning

Before any ticket is written, the project needs its own calibration reference
for story point sizing. The CPO ticket sizing protocol requires three anchor
tickets — one at 1 point, one at 3 points, one at 8 points — that the
orchestrator and CPO agree represent those sizes *for this specific project*.
Without anchors, point assignments drift and velocity becomes unmeasurable.

**Why this is a Phase 2 step, not a Phase 3 activity.** Phase 2 closes the
planning loop. Phase 3 is where tickets get written and sized. If anchors
don't exist before Phase 3 begins, the first handful of tickets get sized
against an implicit reference that shifts as the CPO calibrates — and every
ticket written before calibration stabilized produces corrupt velocity data.
Anchors must exist before the first ticket.

**Seed → Tune → Project file.** The CPO skill ships with generic anchors at
`references/velocity-anchors-seed.md` (a 1pt copy change, a 3pt add-a-column,
an 8pt background job queue). The orchestrator and CPO use the seeds as a
relative-sizing reference and produce three **project-specific** anchors using
real or realistic work from this project's domain. The project anchors must
match the relative sizing of the seeds: a 1pt must feel as trivial as the
seed 1pt, an 8pt must feel as substantial as the seed 8pt.

**Procedure:**

1. **Load the seeds.** CPO reads
   `[aidlc-cpo skill]/references/velocity-anchors-seed.md`.
2. **Draft three project anchors** — one 1pt, one 3pt, one 8pt — using the
   Scope/Complexity/Uncertainty rubric in
   `[aidlc-cpo skill]/references/story-point-rubric.md`. Each anchor must
   include:
   - A real or realistic example ticket from this project's domain
   - The three rubric scores (Low/Medium/High) with one-line evidence each
   - A "what a N feels like" coaching line using the project's idioms
3. **Orchestrator review.** The orchestrator reads the three proposed anchors
   and answers one question for each: "does this match my intuition for what
   an N-point ticket looks like on this project?" If no, the CPO revises
   using the orchestrator's correction as the new calibration signal.
4. **Write the project anchor file** to `docs/aidlc/VelocityAnchors.md`. This
   file is the operational reference for every ticket sizing call from this
   point forward. The seed file is training wheels only and is not used once
   the project anchors exist.
5. **Write anchors to KB:** `type: decision, visibility: internal, decay: permanent`.
   Tag: `velocity-anchors`, `sizing`, `phase-2`.

**Human Gate — Anchor Tuning:**

Orchestrator confirms all three anchors are accurate for the project before
Phase 2 closes. Tuning is not optional and not deferrable — a project without
anchors cannot produce trustworthy velocity data, and every ticket sized before
anchors exist will need to be resized or discarded for velocity purposes.

**Retuning:** Anchors are revisited when the team's sense of "what a 3 feels
like" has drifted — usually signaled by repeated sizing disputes at touchchain
Gate 0, or by a phase retrospective where the team realizes points stopped
meaning what they used to mean. Retuning is a deliberate act documented in the
KB, not a silent drift.

### Human Gate — Phase 2

Build plan approved by the orchestrator before any agent touches code.
Velocity anchors written and approved.

Approval is a KB entry: `type: signoff, visibility: deliverable, decay: permanent`

---

## Phase 3 — Execution Governance

*From approved build plan to shipped software.*

The human approved the plan. The agents execute it. This phase defines how agents behave — and how the human stays in control without micromanaging.

### The Session Ritual

Every agent session follows this structure. No exceptions.

**Session Open:**
1. Agent reads KB — query for project context, recent decisions, current phase (using FCE-enhanced query on Level 4)
2. Agent checks for replay anchor — if found, present to orchestrator for resume/fresh decision
3. **Handoff Detection** — if the opening message contains `HANDOFF →`, this is an agent-to-agent handoff. Run Fast-Start instead of cold-start:
   - Parse the Handoff Card (sending agent, ticket, what shipped, what you're picking up, files touched)
   - Acknowledge the handoff in the agent's voice (1 sentence)
   - Confirm the ticket and state the first action
   - Begin work — skip KB context loading, the context arrived with the card
   - If the Handoff Card is malformed: flag it ("I see a partial handoff card but can't parse it — can you confirm the ticket?"), fall back to normal cold-start. Never hard-fail.
4. Agent reads current ticket
5. Agent establishes test baseline (the ratchet starts here)
6. Agent generates session fingerprint (hash of loaded KB entry IDs)
7. Agent reports status to the orchestrator

**During Session:**
- Annotation Hard Stop (see below) — before any code
- Scope boundary enforcement — only touch listed files
- Ticket-first — no ticket, no work

**Session Close:**
1. Agent verifies test baseline held (or improved)
2. Agent writes Knowledge Dump — but ONLY the CLI agent writes to KB. Desktop agents export context.
3. CLI agent runs conflict detection before writing
4. CLI agent tags entries with decay classification
5. CLI agent generates replay anchor
6. CLI agent records dependency chain (consumed/produced)
7. CLI agent compares session fingerprint for drift detection
8. **Delivery Closing** — if the session produced deliverables and a next agent is known, the agent generates a Handoff Card:
   ```
   HANDOFF → [Receiving Agent Name]
   From: [Current Agent Name]
   Ticket: [ID] — [Title]
   What shipped: [1-2 sentence summary]
   What you're picking up: [1 sentence — next agent's immediate task]
   Files touched: [list]
   Read first: [SKILL.md or doc path if relevant]
   Session context: [link to KB entry, ticket, or session record]
   ```
   The outgoing agent generates the card — never the orchestrator. Format is fixed — the orchestrator pastes it verbatim into the next agent's opening message. If the next agent is unknown, generate a generic "Ready for handoff" card with just the delivery summary and files touched.
9. Agent reports completion to orchestrator
10. Orchestrator reviews and signs off

### The Annotation Hard Stop

**This rule is non-negotiable. It applies to every agent, every session, every project.**

Before writing a single line of code, the agent must:
1. Read the ticket and the relevant specs
2. Search the codebase for every file relevant to the work
3. List every file it will touch, with line numbers and what will change
4. Post the plan to the orchestrator
5. **Wait for explicit approval before writing code**

This prevents scope hallucination. It prevents rework. It keeps the orchestrator informed without requiring them to read every line. An agent that skips this step is an agent that cannot be trusted.

### The Test Ratchet

Tests are a one-way ratchet. They go up. They never go down.

- Baseline is established at session open
- Session does not close with fewer tests passing than the baseline
- If tests drop, the agent stops and reports — it does not ship
- Adapt "tests" to your stack: Jest, pytest, RSpec, JUnit, Vitest, or any test runner — the principle is universal

### Ticket-First Discipline

No Linear ticket (or equivalent PM tool ticket) = no work. No exceptions.

The only exception: a broken main that blocks the entire team. Fix it, document it, write the ticket retroactively.

**Every ticket carries a sizing block.** Story points (1, 2, 3, 5, 8) and a
sprint assignment are mandatory fields at ticket creation time, not bolted on
later. The CPO scores each ticket against the project's velocity anchors
(produced in Phase 2, Step 2.7) using the rubric in the CPO skill
(`references/story-point-rubric.md`). Tickets without points or sprint will
hard-stop the touchchain at Gate 0 in every tier, including AUTO mode.

**Story points measure human-equivalent effort, not AI cost.** An Express-tier
ticket may be a 5 (mechanical but large scope). A Full-tier ticket may be a 1
(one-line auth change). Tier and points are independent measurements and
neither is derived from the other. See the CPO skill for the full sizing
protocol.

### Scope Boundary Enforcement

Every ticket must list explicitly:
- Files the agent may touch
- Files the agent may read but not modify
- Files the agent must not touch

If an agent discovers it needs to touch a file not on the list, it stops, annotates the discovery, and requests approval. It does not proceed on its own judgment.

### KB Writes — Phase 3

Every session close is a KB entry: `type: session, visibility: internal`

**Remember: only the CLI agent writes.** Desktop agents export context to be merged.

Knowledge Dump format:
```markdown
---
kb_id: KB-[timestamp]
phase: 3
type: session
visibility: internal
decay: short
author: [agent name]
---

## Session Summary — [Agent] — [Date]

**Ticket:** [ID and title]
**Session focus:** [1-2 sentences]

### Work Completed
### Decisions Made
### Files Changed
### Tests: Baseline → Final
### Open Questions / Blockers
### Next Session Recommendation
### Replay Anchor
[Git state, work state, critical context — see FCE Replay Anchor format]
### Dependencies
- Consumed: [KB entry IDs loaded at session-open]
- Produced: [KB entry IDs written this session]
- Superseded: [KB entry IDs replaced]
### Drift Report
- Fingerprint match: [yes/no]
- Context contradicted: [list or "none"]
```

---

## Phase 4 — Knowledge Continuity

*The project's memory. Maintained continuously, not at the end.*

Phase 4 is not a cleanup step. It runs in parallel with every other phase. Its job is to ensure that the project can survive the loss of any single person or agent and keep moving.

### Onboarding Protocol — New Human

When a new human joins the project:
1. They read `docs/kb/KB-INDEX.md` — the master index
2. They query the KB: "What are the most important decisions made so far?"
3. They review the current Risk Register
4. They review the current phase's stage gate status
5. They are briefed by the orchestrator on the three things they most need to know

A new human should be productive within one session. If they're not, the KB isn't being maintained properly.

### Onboarding Protocol — New Agent

When a new agent starts on the project:
1. Agent queries KB at session open (semantic search: "project context current phase recent decisions")
2. Agent checks for replay anchor from previous agent's last session
3. Agent reads current CLAUDE.md or equivalent project constants file
4. Agent reads current ticket
5. Agent runs the standard session open protocol (including fingerprint generation)

A new agent should never ask "what is this project?" — the KB answers that.

### The Non-Negotiables

- **Append-only.** Nothing is deleted. Entries are superseded, not removed.
- **Write at the moment, not at the end.** KB entries written after the fact are less reliable.
- **Every decision is documented.** If it wasn't written down, it didn't officially happen.
- **Single writer.** Only the CLI agent writes to KB. Everyone else exports.
- **Conflict detection before write.** Contradictions are flagged, never silent.
- **The KB outlives the engagement.** It is a firm asset. Treat it that way.

---

## Prescriptive Standards (HIT-52)

### Session Validation Checklist — Required Before Any Phase Advances

Every session open must confirm these conditions. If any condition fails, the session does not proceed to implementation — it addresses the failure first.

```
SESSION VALIDATION (all must pass):
───────────────────────────────────
- [ ] KB is accessible — query returns results, not errors
- [ ] Current phase is confirmed — projects.current_phase matches the work being done
- [ ] Main branch is GREEN — full test suite passing, 0 analyzer errors
- [ ] No unresolved CRITICAL blockers exist in the current ticket backlog
- [ ] Ratchet baseline is recorded — test count at session open: ___
- [ ] Agent identity is loaded — the agent knows its role, authority, and boundaries
- [ ] KB authority confirmed — Writer (CLI) or Exporter (Desktop)
- [ ] Ticket is assigned — no ticket, no work
- [ ] Prior session KB entry exists — if this is not the first session, the prior session's knowledge dump must be in the KB
- [ ] Session fingerprint generated — loaded KB entry IDs hashed for drift detection
- [ ] Replay anchor checked — resume or fresh start confirmed
- [ ] Handoff Card parsed (if present) — if opening message contains HANDOFF →, all fields are extracted and confirmed
```

**Output:** SESSION VALIDATED — [agent], [ticket], baseline [N] tests, Phase [N], fingerprint [hash]
or: SESSION BLOCKED — [specific condition that failed, what must be resolved]

Never output "ready to go" without the checklist. The checklist IS the readiness confirmation.

---

### Phase Gate Schema — Required Fields for Every Phase Exit

No phase closes without this schema completed. Every field is required. Missing fields = the phase is not done.

```
PHASE GATE RESULT (all required — phase does not close if any missing):
───────────────────────────────────────────────────────────────────────
- phase: integer (0-4)
- phase_name: string
- date: YYYY-MM-DD
- gate_status: PASSED | FAILED | CONDITIONAL

TECHNICAL GATE:
- [ ] all_features_complete: boolean — every feature scoped for this phase is merged
- [ ] test_baseline_held: boolean — ratchet floor maintained or exceeded
- [ ] test_count_start: integer
- [ ] test_count_end: integer
- [ ] test_delta: integer (must be >= 0)
- [ ] analyzer_clean: boolean — 0 errors on main
- [ ] no_critical_bugs_open: boolean — no P0/P1 bugs unresolved

PRODUCT GATE:
- [ ] acceptance_criteria_met: boolean — all Gherkin ACs for this phase verified
- [ ] stakeholder_demo_complete: boolean
- [ ] signoff_received: boolean — CPO or orchestrator has explicitly signed off
- [ ] signoff_kb_id: string — KB entry ID for the sign-off record

QUALITY GATE:
- [ ] cqo_gate_passed: boolean — CQO quality gate for all features in this phase
- [ ] cdo_gate_passed: boolean — CDO design gate for all UI features in this phase
- [ ] no_slop_patterns_detected: boolean — CQO confirms clean
- [ ] manual_test_debt_logged: boolean — any manual tests logged as automation debt with review dates

KNOWLEDGE GATE:
- [ ] all_session_dumps_written: boolean — every session in this phase has a KB entry
- [ ] all_decisions_documented: boolean — no undocumented decisions
- [ ] kb_index_updated: boolean — KB-INDEX.md reflects all new entries
- [ ] risk_register_updated: boolean — new risks added, resolved risks closed
- [ ] no_unresolved_drift: boolean — all drift detections resolved or acknowledged
- [ ] replay_anchor_current: boolean — latest replay anchor reflects end-of-phase state

CARRIED FORWARD (if gate_status = CONDITIONAL):
- carried_items: array of {item, reason_not_closed, target_phase, owner}
```

**Decision logic:**
- All gates TRUE → PASSED
- Any gate FALSE but non-blocking per orchestrator approval → CONDITIONAL (with `carried_items` documented)
- Any CRITICAL gate FALSE → FAILED (phase does not close)

**CRITICAL gates (always blocking):** `test_baseline_held`, `analyzer_clean`, `no_critical_bugs_open`, `all_session_dumps_written`

---

### KB Entry Required Fields — Enforced at Write Time

Every KB entry must contain these fields. An entry missing any required field is rejected.

```
KB ENTRY REQUIRED FIELDS (reject if any missing):
─────────────────────────────────────────────────
- kb_id: string — format KB-YYYYMMDD-HHMM, auto-generated
- phase: integer (0-4) — the phase this entry belongs to
- type: enum — one of: intake, feasibility, blocker, spec, decision, risk, dependency, build_plan, gate, signoff, session, feature
- visibility: enum — one of: internal, deliverable, both
- decay: enum — one of: permanent, long, medium, short
- author: string — human name or agent name, never blank
- content: string — minimum 3 sentences for decision/risk/session types
- context: string — what situation prompted this entry, minimum 1 sentence
- impact: string — what this changes going forward, minimum 1 sentence

CONDITIONAL FIELDS:
- supersedes: kb_id — required when this entry replaces a prior entry
- superseded_by: kb_id — populated when this entry is replaced (not at creation)
- consumed_ids: uuid[] — FCE: KB entries consumed to produce this entry (Level 4 only)
```

**Validation:** If `type` = "decision" and `content` is fewer than 3 sentences, REJECT. Decisions require explanation.
**Validation:** If `type` = "session" and `author` is blank, REJECT. Every session has an author.
**Validation:** If `visibility` = "deliverable" and content contains internal jargon, agent names, or methodology-specific terms, flag for review — deliverable content must be client-appropriate.
**Validation:** If `decay` is missing, default to `medium` and log a warning.

---

### Anti-Rationalization Upgrade — What Rationalization Looks Like vs. Honest Assessment

Each trigger from the anti-rationalization table now includes concrete examples of what the rationalization sounds like vs. what the honest assessment sounds like.

| # | Rationalization (what gets said) | Honest Assessment (what should be said) |
|---|--------------------------------|----------------------------------------|
| 1 | "This is just a small change, no annotation needed — it's literally one line." | "One line that touches the auth middleware. I'll annotate it because scope doesn't determine risk — surface area does." |
| 2 | "We know what we're building, the client was really clear — skip Phase 0." | "The client described what they want, not what they need. Phase 0 validates assumptions. Running it." |
| 3 | "The tests are passing, 47 green checks, that's good enough." | "47 tests pass but 3 of the spec's critical-path cases aren't covered. Passing tests ≠ verified behavior. Writing the missing tests." |
| 4 | "We can write the KB entry later, I want to keep momentum." | "The KB entry is part of the step. If I skip it now, the decision context exists only in my session memory, which expires. Writing it now." |
| 5 | "The staging environment is close enough to prod, just a few minor differences." | "Staging differs from prod in [specific ways]. Each difference is a vector for 'it worked in staging' failures. Documenting the delta and flagging to CIO." |
| 6 | "The client doesn't need to know about this yet, it's not a big deal." | "The client doesn't know about [specific issue]. If they find out later, their trust is damaged more by the delay than by the issue itself. Surfacing now." |
| 7 | "It's close enough to the mockup, the spacing is just slightly off." | "The left margin is 16px, the mockup specifies 24px. That's not 'slightly off' — it's a design system violation. Fixing it." |
| 8 | "The CTO already reviewed the security aspects as part of the architecture review." | "The CTO reviewed architecture. Security is a separate discipline. The CSO reviews auth flows, PII handling, and secrets. Requesting CSO review." |
| 9 | "We'll add the tests in the next sprint, we need to ship this feature." | "Tests written after implementation are tests written to pass, not to verify. The TDD sequence exists because the order matters. Writing the spec first." |
| 10 | "I also fixed a typo in the header component while I was in there, saved us a ticket." | "I found a typo in header.tsx which is not in my scope. Creating a ticket for it. Not touching files outside my declared file list." |

**The detection rule:** If any agent or orchestrator uses language from the left column, the framework surfaces the corresponding right-column response. This is not enforcement — it is awareness. The orchestrator always has the final say. But the decision to skip a non-negotiable is made deliberately, not accidentally.

---

## Commands Reference

| Command | Phase | Triggers |
|---------|-------|---------|
| `/aidlc-full-cycle` | Any | Starts the full lifecycle from intake |
| `/aidlc-feasibility` | 0 | Runs feasibility assessment only |
| `/aidlc-specs` | 1 | Runs full spec generation (reads aidlc-specs skill) |
| `/aidlc-build-plan` | 2 | Generates phased build plan |
| `/aidlc-gate` | 3 | Runs stage gate checklist for current phase |
| `/aidlc-kb-write` | Any | Writes a new KB entry (prompts for type/visibility) |
| `/aidlc-kb-query` | Any | Semantic search of the KB |
| `/knowledge-dump` | 3 | Agent session close — writes session summary to KB |
| `/spec-export` | 1 | Exports specs to DOCX/XLSX (reads aidlc-specs skill) |

---

## The Framework in One Page

```
KB INITIALIZED (Level 4 + FCE recommended, Level 1 with opt-out acknowledgement)
      │
      ▼
PHASE 0 — INTAKE & FEASIBILITY
  Input: paragraph / RFP / idea
  Output: Idea Compression, Feasibility Assessment, Go/No-Go
  Human gate: Go decision
  Can't build? → NOT YET (pre-work) / NOT US (staffing) / NOT RIGHT (redirect)
      │
      ▼
PHASE 1 — DISCOVERY & SPEC
  Input: Approved Go, raw project input
  Output: PRD, Glossary, Risks, Feature Specs, Dependency Map, Build vs. Integrate
  Human gate: Client/stakeholder spec sign-off
      │
      ▼
PHASE 2 — BUILD PLANNING
  Input: Signed-off specs
  Output: Phase architecture, Timeline, Risk Register, Critical Path, Agent Allocation, Stage Gates
  Human gate: Orchestrator build plan approval
      │
      ▼
PHASE 3 — EXECUTION GOVERNANCE
  Input: Approved build plan + tickets
  Process: Session ritual → Annotation Hard Stop → Implement → Test ratchet → Knowledge Dump
  Agent rule: No ticket, no work. No approval, no code. Single writer to KB.
  FCE: Fingerprint → Work → Conflict detect → Decay tag → Replay anchor → Drift check
      │
      ▼
PHASE 4 — KNOWLEDGE CONTINUITY (runs throughout)
  KB append-only, always current, single writer (CTO)
  FCE: Decay scoring, dependency graph, replay anchors, conflict detection
  New humans onboard from KB in one session
  New agents query KB at session open, check replay anchors
      │
      ▼
STAGE GATE → next phase or SHIPPED
```

---

## Adapting AI-DLC: Full Cycle to Your Project

This framework is stack-agnostic and team-size agnostic. Adapt these elements per project:

| Element | Adapt To |
|---------|---------|
| Test ratchet command | Your stack's test runner |
| Ticket system | Linear, Jira, Asana, GitHub Issues |
| KB infrastructure | Supabase (with FCE) or markdown files (with opt-out) |
| Embedding model | Voyage voyage-3-large (default), OpenAI, Jina, Cohere |
| Agent names | Your team's naming convention |
| Stage gate criteria | Your project's definition of done |
| Export formats | DOCX/XLSX (default) or client-specified |

What you do not adapt: the non-negotiables.

*See `01_aidlc-full-cycle/references/non-negotiables.md` for the complete, canonical list. These are what makes the methodology defensible.*

---

*AI-DLC: Full Cycle — Co-authored by S3 Technology & EX Squared*
*The orchestrator leads. The agents execute. The KB remembers everything.*

---

## Suite References

| File | Load When |
|------|----------|
| `references/kb-schema.md` | Provisioning the KB, writing queries, enabling client portal |
| `references/phase-templates.md` | Running any phase gate, writing sign-offs, onboarding |
| `references/production-ops.md` | Phase 5 post-ship: incident response, hotfix protocol |
| `references/observability.md` | Writing operational logs, querying the audit trail |
| `references/change-management.md` | Modifying existing work: change requests, spec deltas |
| `references/hooks-config.md` | SessionStart hooks, skill routing, anti-rationalization triggers |
| `references/kb-static-site.md` | Level 3 KB: Vitepress setup, deployment, visibility filtering |
| `references/phase-retrospective.md` | Phase close retrospective: 15-minute format, KB entry |
| `references/non-negotiables.md` | Canonical non-negotiables: rules, owners, consequences, override protocol |
| `references/spec-drift-protocol.md` | Spec drift vs scope change vs gold-plating — immediate protocol |
| `references/surface-compatibility.md` | Using AI-DLC on Claude Code, claude.ai, Claude Desktop |
| `../02_aidlc-agent-team/SKILL.md` | Initializing the team, understanding the feature flow |
| `../03_aidlc-cpo/SKILL.md` | Activating the CPO role |
| `../04_aidlc-cto/SKILL.md` | Activating the CTO role |
| `../05_aidlc-cqo/SKILL.md` | Activating the CQO role |
| `../06_aidlc-cdo/SKILL.md` | Activating the CDO role |
| `../07_aidlc-cco/SKILL.md` | Activating the CCO role |
| `../08_aidlc-execution-agent/SKILL.md` | Activating any execution agent |
| `../09_aidlc-cio/SKILL.md` | Activating the CIO role — release management |
| `../10_aidlc-cso/SKILL.md` | Activating the CSO role — security reviews |
