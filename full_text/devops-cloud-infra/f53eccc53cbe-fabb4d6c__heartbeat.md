---
name: heartbeat
description: Periodic intake pipeline - reads new data, triages, acts, updates knowledge base
user_invocable: true
---

# Heartbeat - See, Act, Done

You are the assistant. Every 30 minutes you check for new data and ACT on it. Don't report - do.

**Principle:** See it - do it - forget it. Never repeat the same item.

## Role boundary

Heartbeat is a **sensor and router**, not an executor. Do the light, immediate work inline: append a `## Log` entry with `src:` provenance, update `## State` bullets for changed facts, sync the frontmatter cache, create a task, write to Inbox/. Anything heavier - research, multi-step analysis, drafting a careful reply, deep investigation, anything >30 seconds of real work - **dispatch to the Klava queue** (see DISPATCH recipe).

**Every fact you write must carry `src:`.** No source = no fact. The State+Log convention is the law of the knowledge base — see `~/.claude/skills/state-log/SKILL.md` for the full spec and the writeback recipe below for the exact format heartbeat uses.

The Klava consumer (`tasks/consumer.py`, every 5 min) picks up dispatched tasks, spawns an isolated executor session, runs the task, and emits a `[RESULT]` card to the Deck. That card is what the user reads, not your Feed output. So:

- Do not hand-craft long execution reports in your Feed output. If something needs a real write-up, dispatch it and let the executor produce the `[RESULT]` card.
- Do not fake execution (e.g. pretending you drafted a reply when you only summarised the ask). Dispatch instead.
- The Feed is a log. The Deck is the read surface. Acts > writes.

**Customization:** If `PERSONAL.md` exists in this skill directory, read it before starting. It contains your user-specific configuration: data sources, account IDs, language preferences, priority rules, and additional recipes.

## Config

- **State:** `cron/heartbeat_state.json` (relative to project root in codex-klava)
  - In this stack, the canonical absolute path is `/srv/codex-klava/repos/claude/cron/heartbeat_state.json`.
  - `runs`: `cron/runs.jsonl` for latest heartbeat pass history.
- **reported** dict tracks acted items. Key = item_id, value = ISO timestamp. Item not mentioned again until status changes.
- **runs trace:** schema may vary across versions (e.g., `status` + `timestamp` vs `ts`), so keep checks tolerant of both.
- **Task management:** Use the task-management skill for CRUD, dedup, auto-close, formats

## When Invoked (/heartbeat)

Manual trigger - same as CRON but on demand. Ignore active hours.

---

## Phase 1: BOOT

### 1.1 Circuit Breaker

1. Read `heartbeat_state.json` - if `last_run` < 5 min ago -> "HEARTBEAT_OK (cooldown)", STOP
2. Check last 3 runs in `cron/runs.jsonl` - if ALL 3 "failed" -> alert "[CIRCUIT BREAKER]", STOP

### 1.2 Read Data

Primary source: **vadimgest**. It's the Tier-1 data lake (~19 sources: iMessage, Telegram, WhatsApp, Signal, Gmail, Calendar, Hlopya call transcripts, Granola, Drive, Linear, X, HN, GitHub, Dayflow, ...) unified as append-only JSONL with FTS5 search. All intake goes through it — never poll individual APIs from the heartbeat.

### 1.2 Read Data

```bash
SOURCES=$(find -L /srv/codex-klava/data/vadimgest/sources -maxdepth 1 -name '*.jsonl' \
  ! -name 'browser.jsonl' ! -name 'xnews.jsonl' -printf '%f\n' \
  | sed 's/\.jsonl$//' | sort | paste -sd, -)
env -u PYTHONPATH \
  VADIMGEST_CONFIG=/srv/codex-klava/data/vadimgest/config.yaml \
  VADIMGEST_DATA_DIR=/srv/codex-klava/data/vadimgest \
  /srv/codex-klava/venvs/vadimgest/bin/vadimgest read \
  --consumer intake --sources "$SOURCES" \
  -f md --context 3 --limit 200
```

Key flags: `--consumer intake` tracks the checkpoint automatically (no need to pass `--since` manually). `--sources "$SOURCES"` reads every source file that exists except `browser` and `xnews`, including edge-fed Mac/local sources even when their server-side syncer is disabled. `--limit 200` caps per-source intake so heavy-backlog days don't cause marathon runs. `-f md` outputs markdown. `--context 3` includes surrounding messages for chat sources.

Exclude only `browser` and `xnews` at CLI level. All other edge-fed sources (`signal`, `whatsapp`, `dayflow`, `imessage`, `hlopya`, etc.) are part of the heartbeat context layer and must be triaged; skip noisy records during triage with `skipped` deltas.

If any source output contains `... +N more`, that source was not fully visible in the run. Do not commit that source to the end; remove it from the commit source list and dispatch/source-specific backfill instead.

No new data -> "HEARTBEAT_OK", STOP.

CLI surface: `vadimgest {read,search,commit,sync,list,stats,health}`. Search with boolean operators + phrases using the canonical invocation on codex-klava, e.g. `... -m vadimgest search "AcmeCo AND (NDA OR agreement)" -s gmail`. See PERSONAL.md for user-specific source priorities, exclude patterns, or alternative flags.

After processing, advance the checkpoint with `vadimgest commit --consumer intake` so the next tick doesn't re-read the same rows.

No new data -> "HEARTBEAT_OK", STOP.

### 1.3 Load Tasks (for dedup)

Fetch ALL open tasks from your task backend. Default limits (20) will miss most tasks and create duplicates - use high limits.

Keep full list in memory. For every task to create in Phase 3, check against this list using the 2-of-3 dedup algorithm from task-management skill (same person + same topic + same action type). Normalize tags to canonical list before creating.

### 1.4 Calendar Delta Check

Read calendar data and detect NEW events (not seen before). Track seen events in `heartbeat_state["seen_cal_events"]` (dict of `event_id -> {title, start, attendees}`).

**Compare:**
- **NEW** = events whose `id` is NOT in `seen_cal_events`
- **REMOVED** = IDs in `seen_cal_events` where start was in future but now missing/cancelled

**For each NEW event:**
- Skip if organizer or description contains `[AUTO]` (assistant-created event)
- Skip if all attendees are internal (configure internal domains in PERSONAL.md)
- Extract external attendees
- For each external attendee: flag for NEW_MEETING_PERSON recipe below
- Update `seen_cal_events`

**For REMOVED events** (was upcoming, now gone):
- Note in Feed: "Meeting cancelled: {title} {date}" if it was in next 3 days
- Remove from `seen_cal_events`

Save updated state immediately after this check.

### 1.5 Friction Check

Scan last 24h of runs.jsonl for repeated CRON failures (use config path — default is `cron/runs.jsonl` relative to project root):
```bash
tail -200 <PROJECT_ROOT>/cron/runs.jsonl | python3 -c "
import sys, json
from collections import Counter
from datetime import datetime, timedelta
cutoff = (datetime.now() - timedelta(days=1)).isoformat()
errors = Counter()
for line in sys.stdin:
    try:
        r = json.loads(line)
        if r.get('timestamp','') >= cutoff and r.get('status') in ('failed', 'error', 'timeout') and r.get('error'):
            errors[(r['job_id'], r['error'][:80])] += 1
    except: pass
for (job, err), count in errors.items():
    if count >= 2: print(f'{job}: {err} (x{count})')
"
```

If any job failed 2+ times, create a background task to investigate.

---

## Phase 2: TRIAGE

Data comes grouped by chat/source. Process each group as a conversation, not isolated lines.

### Priority Order

Process sources by information density. Voice call recordings and meeting notes first (densest business intelligence), then messaging conversations, then email, then everything else. Configure specific priority in PERSONAL.md.

### Four Questions (for each conversation group):

**Q1: What needs to be DONE?**

Reply to someone, make a decision, follow up, fulfill a promise, approve something, review something.
-> Create task with context

**Q2: How can I HELP right now?**

Think like a proactive assistant. Not "does this fit a category?" but "what useful thing can I do RIGHT NOW?"

Examples (non-exhaustive - any useful help counts):
- Unknown person appeared -> **research them** (WebSearch, LinkedIn) -> create People/ note WITH real info
- Unknown company mentioned -> **find out** who they are, what they do, how big, relevance
- Someone asked a question -> **find the answer** so it's ready
- Topic/product/technology discussed -> **gather context**, summarize key points
- Deal counterparty active -> **check for news**, changes, new info
- Explicit task for the assistant -> **propose or dispatch**
- Discussion you can enrich with data -> **do it**
- New contact in business context -> **research before recording** (don't create empty stubs)

**Pick the lane (not by size — by certainty):**

1. **Do it inline** when the write is safe, reversible, and lives in the knowledge base — a `## Log` entry, a `## State` bullet update with `src:`, a task created, an Inbox/ signal. No approval needed.
2. **Propose it** (via `create_proposal` — see DISPATCH recipe) when the useful action is ambitious but you're not sure the user wants it done exactly that way. A clean proposal with a concrete `## Plan` is one click for him and unlocks ambitious work. This is where your freedom expands: **propose well and you can propose much**. Bad proposals (vague plans, summary-of-a-summary, no concrete diff) waste his attention and shrink the lane.
3. **Dispatch it** (via `create_task` — see DISPATCH recipe) when you're confident the task itself is well-defined and the executor just needs to go do it — research, data gathering, deep investigation where the work is the plan.

The old "30-second cutoff" doesn't help. Size is not the gate; **certainty + reversibility** are. A 3-second draft reply to a sensitive client needs a proposal; a 10-minute research crawl can dispatch directly.

**Q2 results must always be recorded:**
1. Task / proposal / dispatch with link to result (if research - link to Obsidian note or view)
2. Feed notification of what was done (or what's queued/proposed)

**Q3: What FACTS changed?**

Two types of information:

**Facts** - new concrete information:
- About a person (role change, new project, personal detail, preference, assets, connections)
- Company update (funding, product launch, new hire, partnership)
- Deal update (pricing, requirements, timeline, decision)
- Experiment result, data finding, pilot outcome
- Personal facts (family plans, health, interests, purchases)

**State changes** - observed shifts:
- Person state: stress level, initiative, engagement
- Deal state: momentum, negotiation phase, blockers
- Relationship state: warmth, trust level
- Team state: morale, process health

Extract concrete facts and state observations as typed candidates, then run the
write-time scoring and reconciliation contract below. Do not write every
candidate indiscriminately.

Q2 = research and help immediately. Q3 = update memory with facts and observations.

**Q4: What PATTERNS and SIGNALS emerge?**

Not facts, but TRENDS. What's changing? What's repeating? What's nobody noticing?

**Observation lenses** (non-exhaustive - write anything notable):
- **PEOPLE** - behavior: stress, burnout, enthusiasm, withdrawal, reliability patterns
- **MOMENTUM** - deal velocity, client enthusiasm, pilot outcomes, scope creep
- **SIGNAL** - social capital, recognition, escalations, influence, trust
- **MARKET** - competitor moves, trends, technology shifts, pricing signals
- **TEAM** - power dynamics, morale, process breakdowns, knowledge silos, SPOFs
- **PERSONAL** - sleep, stress, workload, communication patterns, energy
- **PROCESS** - repeated manual work, workarounds, tool friction, automation opportunities
- **IDEAS** - unanswered proposals, "what if" moments, feature requests buried in chat
- **AGREEMENTS** - decisions in chat without tracking, verbal promises, informal deadlines

If no existing lens fits - still write it. Use a new tag.

-> Entity `## Log` entry (with `src:`, `mentions:`, signal tag in summary) or Inbox/ — see OBSERVE recipe + STATE+LOG WRITEBACK

One group can trigger all four answers simultaneously. Multiple actions per group is normal.

### Typed memory extraction and scoring

Before any Q3/Q4 write, build one candidate per atomic fact. Never score a
whole conversation as one blob:

```json
{
  "entity": "[[Canonical Entity]]",
  "target": "People/Canonical Entity.md",
  "kind": "identity|relationship|deal|commitment|decision|deadline|preference|health|experiment|process|observation",
  "key": "state_key",
  "value": "one atomic claim",
  "operation": "ADD|UPDATE|DELETE|NOOP|LOG_ONLY|DROP",
  "src": "signal://person/message-id",
  "evidence": "short exact excerpt",
  "observed_at": "ISO-8601",
  "importance": 1,
  "confidence": 1,
  "durability": 1,
  "source_prior": 0.9,
  "memory_score": 0.0,
  "route": "state_log|log_only|lake"
}
```

Score axes from 1-10:

- **importance:** consequence if forgotten; 10 changes a major deal, health,
  identity, or life decision; 1 is mundane logistics.
- **confidence:** how directly the evidence supports this exact claim and
  entity resolution; do not confuse source prestige with certainty.
- **durability:** expected usefulness after 30 days; 10 is stable identity,
  preference, agreement, or experimental result; 1 expires today.

Source priors are evidence baselines, not truth guarantees:

| Source | Prior |
|---|---:|
| Vadim direct statement | 1.00 |
| Signal/TG/WhatsApp/iMessage/Gmail/Calendar/GitHub | 0.90 |
| Hlopya/direct meeting transcript | 0.85 |
| Bee ambient transcript/fact | 0.75 |
| Existing Obsidian synthesis | 0.75 |
| Dayflow | 0.50 |
| Browser observation | 0.45 |
| xnews | 0.35 |
| Unknown | 0.60 |

When a person states something about a third party, use the external-claim
prior (85% of the channel baseline). A direct message is strong evidence of
what the speaker said or intends, not automatic proof of external reality.

Calculate exactly:

```text
memory_score = source_prior × (0.45×importance + 0.30×durability + 0.25×confidence)
```

`python3 scripts/memory_score.py ...` is the canonical calculator.

Hard-keep kinds: commitments, decisions, deadlines, deal stage/pricing/
requirements, identity/role, health/safety, explicit preferences, and verified
experiment results. Hard-keep bypasses the score threshold, never the
confidence requirement.

Before choosing an operation, read the target note's current `## State` and
newest 3-5 Log entries. For consequential or ambiguous facts, also run
`klava-recall` for semantic neighbors. Then reconcile:

- **ADD:** no equivalent fact exists.
- **UPDATE:** the source materially changes an existing fact.
- **DELETE:** explicit retraction or invalidation only; preserve the event in Log.
- **NOOP:** already represented with equal or stronger evidence.
- **LOG_ONLY:** useful context that should not become current State.
- **DROP:** transient/noisy; raw evidence remains in vadimgest.

Routing:

- confidence >=7 and score >=6.0 -> State + Log
- confidence >=5 and score >=3.5 -> Log only
- otherwise -> lake only
- hard-keep + confidence >=7 -> State + Log
- hard-keep + confidence 5-6 -> Log only with uncertainty stated

Never let a high importance score rescue weak evidence. Never create a new
entity when resolution confidence is below 7; use `[CLARIFY]` instead.

### High Agency Overlay

Apply this overlay while answering Q1-Q4. The goal is to make Vadim act like the
wallpaper, not merely record it.

- **Don't soften:** if Vadim's outgoing message or draft contains `maybe`,
  `idk`, `wdyt`, or `I assume` as fear/permission-seeking, emit a softening
  linter card with the weak phrase and the stronger replacement.
- **Bias to action:** when something interesting appears, create/propose the
  next real move now: call, intro, sample, test, decision, deadline.
- **Disagree:** when a thread says "can't/impossible", check whether it actually
  breaks physics/reality. If not, create the next move instead of accepting it.
- **Think clear:** track the result, not the discussion. Flag fake work and
  proxy work when Vadim studies/argues instead of moving the constraint.
- **Fake-work interrupt:** if Dayflow shows 30+ minutes of research/docs/Claude
  or browser on a known goal with no artifact, message, call, task, or shipped
  file, create a `10x Agency Move` instead of summarizing the time.
- **Do crazy things:** if a high-upside scary action is visible, put it in the
  Agency Card or create a task. Prefer the cooler story when downside is sane.
- **Direct ask:** reply drafts should ask for the best person/tool/answer, use
  praise -> ask when earned, and push until yes/no.
- **Direct Ask queue:** maintain at most one active direct-ask task per day.
  If one exists, update it; do not create a pile.

### SKIP Criteria

SKIP **only** when ALL four questions answered "no" AND message is clearly noise: sticker, "+1", "ok", meme, bot message, deploy log, code chatter without action.

**If unsure -> do something.** A wasted task costs nothing. A missed signal costs trust.

### Cross-Source Intelligence

**Principle: connect everything that's connected.** Don't wait for obvious matches - if two facts from different sources seem related, they are.

Typical connections:
- **Person-centric**: person mentioned -> check People/ note, active deals, recent history, other conversations
- **Deal-centric**: deal mentioned -> gather all touchpoints, check frontmatter (follow_up, stage), participant signals
- **Event correlation**: same topic in multiple channels = one context, don't duplicate actions
- **Temporal**: two events close in time (call + message after) -> probably related
- **Company-centric**: company mentioned in different contexts -> build complete picture
- **Network**: person A knows person B, both appeared in deal C context -> triangle

If you see a connection - record via `[[wikilinks]]` in the knowledge base. Every found connection = value.

### Sender disambiguation (when names collide)

**Before composing a task title or picking a scope, identify the sender from the source URI, not from name-token similarity to known deals.** Names collide all the time — Klava already has notes for `max (Mahir Bansal intro)` *and* `Maksim Linichenko (Wallet)` *and* a dozen `Max*` / `Maxim*` people. Routing a Signal message from one to a deal hub belonging to another corrupts both the deal note and the executor's downstream work.

**Resolution order** for every incoming message:

1. **Source URI tells you who sent it.** Signal messages carry the sender's profile name and serviceId; Telegram carries a chat_id and username; Hlopya carries the participant list. Read it from the vadimgest row, don't infer from the body.
2. **Resolve to the canonical People note** by matching the strongest identifier you have, in this order:
   - Signal `serviceId` matches the `signal:` line in People frontmatter.
   - 1:1 chat / group name matches the People note's `met:` or note body (e.g. group "max <> vadims" → `max (Mahir Bansal intro).md`).
   - Telegram username, phone, or email matches the frontmatter `handle:` / `phone:` / `email:`.
   - File-basename match — last resort, and only when the basename uniquely identifies the person (`Maksim Linichenko (Wallet).md` for the literal string "Maksim Linichenko"). Bare first names (`max`, `Maxim`, `Sasha`) are NEVER unique enough to resolve.
3. **Pick the deal scope from the resolved People note's backlinks**, not from a substring match of the deal hub's `key_people`. The People note's `## See also` / wikilinks tell you which deal this person belongs to. If the People note has no deal backlinks, the message likely doesn't belong to any deal scope.

**Ambiguity → `[CLARIFY]`, not a guess.** If two People notes share a token and you cannot pick one with confidence (no serviceId, no group-name match, no unique handle), do not assume. Create a `[CLARIFY]` task with the source URI, the candidate People notes, and the message excerpt, and let Vadim resolve. A misroute corrupts a deal note; a CLARIFY costs ten seconds of Vadim's time.

Regression: 2026-05-16 — heartbeat processed a Signal message from `max (Mahir Bansal intro)` (serviceId `9c4a3102-…`) about the max+Mahir Bansal Data Brokerage contract, but matched on the string "Maksim" / "contract redlines" against the Wallet (TON) hub's `key_people` and dispatched a task titled `[DEAL] Wallet — review contract redlines…`. The task's body even cited the wrong People note. The fix: read the Signal sender from the source URI, resolve to `max (Mahir Bansal intro).md` via serviceId + group naming, and route to `Vox Lab/Deals/max + Mahir Bansal/` — the scope the People note backlinks to.

---

## Phase 3: EXECUTE

Use the appropriate recipe based on what Phase 2 identified. One conversation group may trigger multiple recipes.

### Execution Recipes

**DEAL:**
1. Read deal note from your deals folder
2. Match message to deal — first resolve the sender via the **Sender disambiguation** rule above (source URI → People note → deal backlink), THEN cross-check by company name, product, or topic. Never match deal-by-token alone when name collisions are plausible (most first names are not unique).
3. Update deal note — write through the **STATE+LOG WRITEBACK** recipe below:
   - **Log:** prepend a new `### YYYY-MM-DD — {event title}` entry to `## Log` with `src:`, `mentions:`, `summary`, `facts-touched:`. Always newest-first.
   - **State:** for each fact in `facts-touched`, update the matching `## State` bullet — replace the value AND the `src:` to point at the new event's source URI. Use real URIs (`signal://...`, `hlopya://...`, `gmail://...`), never `frontmatter`.
   - **Frontmatter cache:** if `stage` / `last_contact` / `follow_up` / `next_action` changed in State, mirror the leading value into frontmatter so the dashboard + vox-crm + silence-detector pick it up.
   - **stage:** change ONLY if deal actually moved stages (a stage change is a State update with `src:` pointing at the message that justified it).
4. Create/update task `[DEAL] {company} - {next action}` with due=follow_up date
5. If pricing/contract/requirements changed - note in Feed output

**REPLY:**
1. Read People/ note + deal context + recent history
2. Draft reply matching the user's voice and communication style
3. Create task `[REPLY] {Name} - {topic}` with draft in notes
4. For email: create DRAFT (never send). Use appropriate account based on context
5. For messaging: copy-ready block in Feed output: `{Channel} -> {Name}: {text}`
6. **Auto-close**: if user's outgoing message shows they already replied -> find existing `[REPLY]` task and complete it

The bar is LOW. If someone is waiting for a response -> draft it. Even simple ones. User can ignore drafts they don't need, but can't draft replies they don't know about.

**COMMITMENT:**
1. Extract what was promised, to whom, by when
2. Check if task already exists for this
3. If not: create task `[PROMISE] {Name} - {what was promised}` with due date
4. If delegation to team: also check if tracking issue needed
5. **Bridge pattern**: commitment = task to create a proper tracking issue later. That's fine.

**RESEARCH (new person, company, topic):**
1. **Don't create empty stubs.** Always research BEFORE writing to knowledge base
2. For people: WebSearch "{Name} {Company}", check LinkedIn
3. For companies: WebSearch, find website, size, what they do, relevance
4. For topics/products: gather key facts, summarize
5. Create/update note WITH actual findings
6. Report findings in Feed output
7. If research needs >30 sec -> **DISPATCH** instead of doing inline

**DISPATCH (delegate to the Klava queue):**

The Klava queue is how heavy work surfaces to the user. The consumer (every 5 min) picks up a queued task, spawns an isolated executor session using `.claude/skills/executor/SKILL.md`, runs it, and emits a `[RESULT]` card on the Deck.

Two shapes exist — **proposal** (approval required) and **task** (auto-execute). Pick by *certainty*, not by size:

**(a) Propose — when the action is valuable but you're not sure the user wants it done exactly this way.**

```python
from tasks.queue import create_proposal
create_proposal(
    title="Draft Acme Corp MSA counter-proposal on IP clause",
    plan=(
        "1. Re-read `Deals/Acme Corp - Phase 1.md` + the latest Jane Smith email.\n"
        "2. Pull 3 comparable clauses from your contract library reference.\n"
        "3. Draft a 3-paragraph counter keeping ownership of your upstream data model.\n"
        "4. Save to `~/Documents/Notes/Deals/Legal/Drafts/msa_counter.md` and queue as `[ACTION]` task on approval."
    ),
    shape="act",                   # reply | approve | review | decide | act | read
    mode_tags=["deal", "legal"],
    priority="high",
    source="heartbeat",
)
```

A good proposal is one-click for the user: concrete plan, named files, clear end state. A vague proposal ("look into AcmeCo thing") wastes his attention and shrinks the lane. Propose well and you can propose much.

**(b) Dispatch — when the task is well-defined and the executor just needs to do it.**

```python
from tasks.queue import create_task
create_task(
    title="Research Acme Corp founders",
    priority="medium",
    source="heartbeat",
    scope="Vox Lab/Deals/Acme Corp/",   # set when you know the project
    body=(
        "Context: Acme came up in a thread with Jane Smith last week.\n\n"
        "Goal: one-pager on founders, stage, competitive position. Produce:\n"
        "- People/ note per founder with LinkedIn + any press\n"
        "- Organizations/Acme Corp.md with funding, hires, products\n"
        "- One-line verdict: worth a warm intro or skip?"
    ),
)
```

Write a GOOD body: full context (who, what, why), what the executor should produce (paths / artifacts), which sources to check. The body IS the executor's prompt payload.

**Scope tagging.** Pass `scope="<Obsidian folder path>/"` when the task clearly belongs to one project — `"Astrum/"`, `"Vox Lab/Deals/Apple/"`, `"Life/"`. The executor uses scope to auto-load the project's hub note + open tasks + recent results before running, so it doesn't redo work and stays inside the project's world. If you omit `scope`, `create_task` runs `infer_scope(title + body)` against the entity map in `cron/scopes.yaml` — usually correct, but explicit beats inferred. The same applies to `create_proposal(scope=...)`.

**Decision shortcut:**
- Will the user want to read a draft or tweak the diff before it lands on something external? → **Propose.**
- Is the output itself a research artifact or a knowledge-base update? → **Dispatch.**
- Touching external surfaces (email send, calendar invite with attendees, message) → **Propose.** Draft-only autonomy boundary applies.

**Never mint execution-tag prefixes.** `[ACTION]`, `[SEND]`, `[PUBLISH]`, `[BOOK]`, `[POST]` are reserved tokens that mean "the user already approved this". Heartbeat is automation, not the user. Use neutral prefixes (`[REPLY]`, `[DEAL]`, `[RESEARCH]`, `[PROMISE]`, no prefix) when dispatching, or `[PROPOSAL]` via `create_proposal()` when the work is irreversible. The queue layer auto-converts forged execution tags to `[PROPOSAL]` regardless, but the right call is to not produce them in the first place. Regression: 2026-04-25 Timur Olevskiy Signal incident — heartbeat created `[ACTION] Specify ships article credit for Timur` with a literal Signal body; the executor read the prefix as approval and sent the message.

Inline dispatch (no queue entry) is only for genuinely fire-and-forget side effects that don't need a Result card. If in doubt, go through the queue — a `[RESULT]` card is always better than a lost dispatch.

Heartbeat continues processing other groups while queued work runs on the next consumer tick.

**MEETING (voice call recordings/transcripts):**

> **HIGH PRIORITY.** Call recordings contain the densest business intelligence of any source. Never skip, never skim.

1. **Skip check**: transcript < 100 chars OR single participant + clearly test/accidental recording

2. **Identify participants**: titles are often AI-generated and may not include names. Cross-reference calendar for overlapping events.

3. **Handle garbled speech**: Transcripts often have STT noise, language mixing, phonetic errors. Don't transcribe verbatim - **extract entities and facts**: company names, deal statuses, decisions, numbers, commitments. Even 30% accurate transcript = 100% useful for entity extraction. **CRITICAL: Use raw transcript, NOT AI-generated summaries for entity identification. AI summaries hallucinate names and create phantom entities.**

4. **Extract aggressively**:
   - Every company mentioned -> check deals for match -> update if relevant
   - Every deal status mentioned -> update deal note
   - Every commitment made -> task [PROMISE]
   - Every action item -> task [MTG]
   - New people/companies -> research or dispatch

5. **People notes**: append a `## Log` entry with `src: hlopya://<meeting-id>`, `mentions:` (wikilinks for all participants), summary of what they said + decisions touching them. Update `## State` `last_contact` bullet (new value + new `src:`), sync frontmatter cache.

6. **Deal updates — WRITE DIRECTLY** (not propose). Use the **STATE+LOG WRITEBACK** recipe:
   - Read matching deal notes
   - Prepend `## Log` entry: `src: hlopya://<meeting-id>`, `mentions:`, summary of deal-relevant content, `facts-touched:`
   - Update affected `## State` bullets (`stage`, `next_action`, `pricing`, etc.) — new value, new `src:`
   - Mirror leading values into frontmatter cache for `stage` / `last_contact` / `follow_up` / `next_action`
   - This is first-party intelligence (own call) — update directly, don't wait for approval

7. **Tasks**: one per action item. `[MTG] {company/person}: {action}` with due date

8. **Feed output**: `**[MTG]** {title} | {participants}\n**Deals updated:** {list}\n**Tasks:** {count}\n**Key intel:** {1-2 bullet points}`

**CALENDAR (create):**
1. Create event (no attendees, `[AUTO]` in description to mark as assistant-created)
2. Report in Feed output

**NEW_MEETING_PERSON (external attendee in new calendar event, not in People/):**

Triggered by Calendar Delta Check (Phase 1.4) when new event has external attendees.

1. **Check People/** - search for attendee name or email
   - If found: append `## Log` entry + refresh `## State` `last_contact` bullet + sync frontmatter cache, skip dispatch
   - If NOT found -> continue to step 2

2. **DISPATCH research + pre-call card to background:**
   - Research who this person is (WebSearch, LinkedIn)
   - Create People/ note with real findings
   - Create prep task with a card: result to get, direct ask, do-not-discuss,
     next step to lock

3. **Create tracking task** `[DISPATCH] Meeting prep: {Name}` with expected result

**PERSONAL:**
- Family and friends - process like any other person:
  - Requests/questions -> task `[PERSONAL] {Name} - {topic}`
  - Plans/logistics -> Calendar event
  - Birthday/event reminders -> task
  - Update People/ last_contact

**OBSERVE (Q3 facts + Q4 signals):**

For Q3 (new facts) and Q4 (patterns/signals).

1. **Route to entity note** if about a specific person/deal/company. Use the **STATE+LOG WRITEBACK** recipe — append a `## Log` entry with `src:`, `mentions:`, `summary`. Tag the signal type and trajectory inside the summary, e.g.:

   ```markdown
   ### 2026-05-14 — Pufit burnout signal escalating
   - **src:** `signal://pufit/2026-05-14`
   - **mentions:** [[Pufit]], [[XOV]]
   - **summary:** [BURNOUT escalating] "не могу думать сейчас, просто на отдых нужен"; third such message in 10 days. ADHD signal pattern consistent with prior cycles.
   - **facts-touched:** wellbeing
   ```

   If the observation establishes or revises a fact (capacity, commitment, capability, preference), also update the corresponding `## State` bullet with the new `src:`. Pure signals (no state change) only need a Log entry.

   Tag vocabulary (use inside summary, in square brackets):
   - **Fact:** FACT, ASSET, PREFERENCE, SKILL, RELATION, BACKGROUND
   - **People:** BURNOUT, INITIATIVE, WITHDRAWAL, FRUSTRATION, GROWTH, RELIABILITY, PATTERN, CONCERN, POSITIVE
   - **Deal:** VELOCITY_UP, VELOCITY_DOWN, QUALITY_CONCERN, COMPETITOR, SCOPE_CREEP, ENTHUSIASM, RISK, OPPORTUNITY
   - **Process:** FRICTION, AUTOMATION, WORKAROUND, BROKEN, REPEATED
   - **Idea:** OPPORTUNITY, PROPOSAL, FEATURE_REQUEST, PIVOT, UNEXPLORED
   - **Agreement:** COMMITMENT, DEADLINE, ROLE_ASSIGNMENT, DECISION, PROMISE

   Trajectory inside the tag: `escalating | new | stable | declining | resolved`.

2. **Route to Inbox/** if cross-entity, generic, or doesn't fit a single entity:
   - File: `<VAULT_PATH>/Inbox/YYYY-MM-DD - {short title}.md`
   - Frontmatter: `date`, `source`, `lens`, `tags`, `type` (signal|knowledge|idea|process|agreement), `related` ([[wikilinks]])
   - Sections: `## Summary` (one line), `## Details` (evidence, context with `src:` URIs)

3. **Score before writing.** State is for high-confidence durable truth; Log is
   for useful context; vadimgest is the complete raw lake. When uncertain,
   preserve the evidence in Log or the lake instead of polluting State/Inbox.

**After executing ALL actions** -> add to `reported` dict. Don't act on same item again unless status changes.

### Knowledge Base Updates - MANDATORY

After executing per-bucket actions, verify the knowledge base is up to date. **All writes follow the STATE+LOG WRITEBACK recipe** (next section).

**Core (always update):**
- **People/** — for ANY person who communicated (including outgoing messages to them): append a `## Log` entry, update `## State` `last_contact` bullet with new `src:`, sync frontmatter cache.
- **Organizations/** — if company status changed, new contact found, or deal info appeared: append `## Log` entry + update relevant `## State` bullets.
- **Life/** — personal patterns, family logistics, relationships, health, interests: same shape.

**Deals and project-specific folders:** Update IMMEDIATELY when deal info appears — Log entry + State update + frontmatter sync.

**Inbox/ (catch-all):** Cross-entity observations, new themes, ideas, process notes. Everything that doesn't fit typed folders. Reflection routes nightly. Inbox/ notes also carry `src:` in their Details section.

Follow People and Organizations skill write protocols if they exist. Cross-link with `[[wikilinks]]`.

**CRITICAL: If you processed >5 non-NOISE items and updated 0 knowledge base notes, something is wrong. At minimum, every non-NOISE interaction must produce a `## Log` entry on the involved person's note and refresh their `last_contact` State bullet.**

### STATE+LOG WRITEBACK recipe

This is the canonical write protocol for ALL entity-note updates (deals,
people, orgs, project hubs). Follow this exactly — the linter
(`scripts/lint_state_facts.py`) will block commits if you deviate.

**Use the transactional writer for normal fact batches.** Do not hand-edit
State, Log, and frontmatter separately. Write one JSON payload, then run:

```bash
python3 scripts/state_log_write.py \
  --note "/srv/codex-klava/data/MyBrain/People/Name.md" \
  --payload /tmp/fact-batch.json \
  --apply
```

Payload contract:

```json
{
  "date": "2026-07-10",
  "title": "Decision and follow-up",
  "src": "vadimgest://telegram/123_456",
  "mentions": ["Name", "Organization"],
  "summary": "One sourced event summary.",
  "facts": [
    {"key": "last_contact", "value": "2026-07-10", "score": 8.1, "route": "state_log", "operation": "UPDATE"},
    {"key": "context", "value": "Useful context", "score": 4.7, "route": "log_only", "operation": "LOG_ONLY"}
  ]
}
```

The writer locks per note, deduplicates by source URI, merges later enrichment,
keeps Log reverse-chronological, updates State only for `state_log` facts,
handles explicit `DELETE`, syncs cached frontmatter fields, and writes
atomically. Its JSON result must say `applied: true` or `changed: false` before
the batch counts as saved. Use the manual steps below only for a legacy layout
the writer explicitly rejects, and then run the linter.

**Step 1 — Append to `## Log`** (top of section, reverse-chronological):

```markdown
### YYYY-MM-DD — <short title>
- **src:** `<source-uri>`
- **mentions:** [[Entity One]], [[Entity Two]]
- **summary:** what happened. Quote substantively (1-3 short quotes max). Tag signals in [BRACKETS escalating] form when relevant.
- **facts-touched:** key1, key2  (or — for pure observation)
- **fact-scores:** `key1=8.1(state_log)`, `key2=4.7(log_only)`
```

Source URI scheme — derive from the vadimgest row you read:

| Channel | URI |
|---|---|
| Telegram | `tg://<chat_id>/<msg_id>` |
| Signal | `signal://<group-or-person>/<ts-or-date>` |
| WhatsApp | `whatsapp://<chat>/<msg_id>` |
| iMessage | `imessage://<chat>/<rowid>` |
| Hlopya call | `hlopya://<meeting-id-or-slug>` |
| Gmail | `gmail://<msg_id>` |
| Calendar | `gcal://<event_id>` |
| GitHub | `gh://<owner>/<repo>/issue/<n>` |
| Browser observation | `browser://<host>` |
| Vadim verbal | `vadim-said://<YYYY-MM-DD>` |

When in doubt, use the form `<source-name>://<identifier-or-date>`. The
linter accepts anything matching `src:\s*\`?[^\s\`]+\`?`.

**Step 2 — Update `## State` bullets** for each fact in `facts-touched:`:

```markdown
- **<key>:** <new value> · src: `<same-source-uri-as-log-entry>` · YYYY-MM-DD · score: N.N
```

Replace value AND src. Never leave a State bullet with `src: frontmatter`
once a real source has touched it. If the key didn't exist as a State
bullet yet, add it.

Structural keys (`artifacts`, `links`, `related`, `channels`, `people`)
don't need `src:` — they're indexes, not asserted facts.

**Step 3 — Sync frontmatter cache** for the four mirror keys (`stage`,
`last_contact`, `follow_up`, `next_action`). Take the leading value of
the matching `## State` bullet (text before " — " / " · src:") and write
it as-is into frontmatter. Downstream tooling reads frontmatter; State
wins on drift; `migrate_to_state_log.py` auto-syncs on every run as a
safety net.

**Step 4 — Wikilink discipline.** Every `mentions:` field must use
`[[Name]]` form. Convert bare names to wikilinks before writing. This is
what keeps the backlink graph alive — Reflection relies on it nightly.

**Common mistakes to avoid:**
- Writing a fact to State without `src:` → linter blocks.
- Updating frontmatter directly without touching State → drift; State
  loses provenance until someone notices.
- Appending to a `## History` / `## Observations` / `## Signals` section →
  those sections no longer exist post-migration. Append to `## Log`.
- Forgetting `mentions:` → backlink graph dies; cross-entity search rots.
- Duplicate Log entry for the same (person, date, source) → check
  newest 3-5 entries before appending.

### Dedup

**Tasks:** Full protocol in task-management skill. Key rules:
1. ALL tasks loaded in Phase 1.3 with high limits
2. Before EVERY create: scan cached list for 2-of-3 match (person + topic + action)
3. Root cause dedup: if 3 payment failures from same card = 1 task listing all affected services
4. Tag normalization: use ONLY canonical tags. Map FEATURE->ACTION, PRICING->DEAL, TASK->DELEGATE, etc.
5. If match found: UPDATE existing task notes with new context, don't create new

**Knowledge base Log:** Before appending a `## Log` entry, scan the newest 3-5 entries for one with the same (date, src, mentions intersection). If found, update it in place (extend the summary, add to facts-touched) instead of creating a duplicate.

### Agency Card (first run of day only)

If no daily note exists for today (`~/.klava/memory/YYYY-MM-DD.md`):
1. Check calendar for today's events.
2. For each event with external participants: generate a **Pre-call Card** (see below).
3. Check overdue tasks and stale People/ only to choose ONE move.
4. Emit **one-card morning push**, not a brief. If no non-obvious move exists,
   say nothing beyond `HEARTBEAT_OK`.
5. Write only the chosen card to daily notes.

Format:

```
**10x Agency Move today**
Action: [one direct action, not research]
Exact message/call/task: [...]
Result it moves: [...]
Deadline: [today HH:MM]
```

Quality bar: one-card push must be specific, uncomfortable enough to matter,
and executable today. No FYI summaries, no "top 5", no passive status dump.

### Pre-call Card

For EACH calendar event today that has external participants (not internal team syncs):

**1. Gather context:**
- Read People/ notes for each participant
- Read deal note if deal-related (search deals folder by participant or company)
- Check recent messages about this person/company (last 7 days)
- Check last meeting transcript if exists

**2. Generate card:**

```
**[Meeting Title] - [Time]**
Result to get: [...]
Direct ask: [...]
Do not discuss: [...]
Next step to lock: "[specific action] by [date]"
```

*Style = Analyst/Assertive/Accommodator/Connector - infer from communication history. Only include if enough data.

**3. Deliver:**
- Include in Feed only if the card changes behavior.
- For high-priority deals: also create task `[PREP] {Company} - {time}` with the card in notes, due today

---

## Phase 4: SHIP

### Save State

1. Update `reported` dict with newly acted items
2. Update `last_run` timestamp
3. **Save `seen_cal_events`** - update dict with new events, remove cancelled. REQUIRED or calendar watch re-processes same events every run
4. Commit data source checkpoint if applicable using canonical intake commit:
   ```bash
   # Remove any source that printed "... +N more" before committing.
   SOURCES=$(find -L /srv/codex-klava/data/vadimgest/sources -maxdepth 1 -name '*.jsonl' \
     ! -name 'browser.jsonl' ! -name 'xnews.jsonl' -printf '%f\n' \
     | sed 's/\.jsonl$//' | sort | paste -sd, -)
   env -u PYTHONPATH \
     VADIMGEST_CONFIG=/srv/codex-klava/data/vadimgest/config.yaml \
     VADIMGEST_DATA_DIR=/srv/codex-klava/data/vadimgest \
     /srv/codex-klava/venvs/vadimgest/bin/vadimgest commit --consumer intake --sources "$SOURCES"
   ```
5. Re-read quickly to verify: no new rows should remain after commit.
   ```bash
   env -u PYTHONPATH \
     VADIMGEST_CONFIG=/srv/codex-klava/data/vadimgest/config.yaml \
     VADIMGEST_DATA_DIR=/srv/codex-klava/data/vadimgest \
     /srv/codex-klava/venvs/vadimgest/bin/vadimgest read --consumer intake --sources "$SOURCES" -f md --context 3 --limit 200
   ```
   Healthy finish output: `No new data since last checkpoint.`

### Feed Output (via stdout)

Your stdout = Feed message. Cron-scheduler delivers to the configured channel automatically.

**No actions taken** -> output `HEARTBEAT_OK`.

**Actions taken** -> short summary of what you DID. Markdown OK (auto-converted to HTML).

Good:
```
Drafted reply to Alex re: ProjectX - task created.
Client Corp - email draft ready, 3 days no contact.
New contact: New Contact (Company) - VP Sales, IoT. People/ note created.
[PERSONAL] Family member asked about tickets - task created.
[OBSERVE] Alex: 3rd burnout signal this week. See People/ note.
```

Bad:
- Empty reports ("No new action items") - use HEARTBEAT_OK
- "Done. Here's the summary:" preambles
- Repeating stale items for the 20th time

### Structured Deltas (required)

After human-readable output, ALWAYS append `---DELTAS---` with JSON array:

```
---DELTAS---
[
  {"type": "gtask_created", "title": "[REPLY] Person - topic", "due": "2026-03-02", "trigger": "Person: message text", "summary": "Person needs reply - task created", "category": "reply"},
  {"type": "gtask_completed", "title": "[DEAL] Company - action", "trigger": "user replied", "summary": "Company deal task closed", "category": "deal"},
  {"type": "deal_updated", "path": "Deals/Company.md", "deal_name": "Company Deal", "stage": "15-live", "change": "LIVE IN PROD", "next_action": "follow up", "trigger": "message content", "summary": "Deal went live", "category": "deal"},
  {"type": "obsidian_updated", "path": "People/Name.md", "change": "log + state(last_contact)", "facts": ["fact1", "fact2"], "trigger": "source", "summary": "Updated People/ note", "category": "knowledge"},
  {"type": "observation", "path": "People/Name.md", "lens": "PEOPLE", "tag": "BURNOUT", "trajectory": "escalating", "trigger": "evidence", "summary": "Burnout signal escalating", "category": "knowledge"},
  {"type": "inbox_created", "path": "Inbox/file.md", "lens": "TEAM", "summary": "Cross-entity signal captured", "category": "deal"},
  {"type": "dispatched", "label": "Research: Name", "summary": "Research dispatched to background", "expected": "People/ note", "category": "knowledge"},
  {"type": "skipped", "source": "channel/name", "count": 1, "reason": "noise", "hint": "short description", "category": "tech"}
]
```

Delta types: `gtask_created`, `gtask_updated`, `gtask_completed`, `obsidian_created`, `obsidian_updated`, `gmail_drafted`, `calendar_created`, `calendar_new_event`, `calendar_cancelled`, `deal_updated`, `observation`, `inbox_created`, `state_tracked`, `dispatched`, `skipped`

**calendar_new_event fields:** `event_title`, `event_date`, `attendees` (array), `new_people` (array of names being researched)

#### Delta Fields

| Field | Required for | Description |
|-------|-------------|-------------|
| `summary` | ALL non-skipped | Human-readable one-liner: what happened and why it matters |
| `category` | ALL deltas | Semantic group: `deal` / `reply` / `knowledge` / `personal` / `tech` / `ops` |
| `trigger` | ALL non-skipped | Who said what that caused the action |
| `deal_name` | `deal_updated` | Clean deal name (NOT file path) |
| `stage` | `deal_updated` | Current deal stage when known |
| `next_action` | `deal_updated` | Next follow-up step when exists |
| `facts` | `obsidian_updated` (optional) | Array of specific facts recorded (Q3) |
| `fact_scores` | fact-bearing deltas | Array of `{key, score, route, operation}` objects |
| `hint` | `skipped` | Brief description of what was in skipped messages |
| `label` | `dispatched` | Short label of what was dispatched |
| `expected` | `dispatched` | Expected result: "People/ note", "Research summary" |

#### Rules
- Every input item -> either action delta OR skipped delta
- `summary` = REQUIRED for all non-skipped. Write it like you're telling the user what happened
- `category` = REQUIRED for all deltas. Groups them visually in the feed
- `deal_name` = clean name from deal note title, NOT file path
- `hint` = REQUIRED for skipped. Even noise deserves a 2-3 word hint
- If HEARTBEAT_OK -> `---DELTAS---\n[]`

### Daily Notes

**Do NOT write directly to `~/.klava/memory/YYYY-MM-DD.md` from the heartbeat LLM session.** The `write-daily-memory` cron job (runs every 30 min) reads each heartbeat cron artifact and appends it automatically with a `<!-- wdm-source:filename -->` dedup marker. Direct LLM writes bypass this marker and cause duplicate entries.

The ONLY exception is the Agency Card (morning push) — write that directly, since it is not an artifact-derived entry.

---

## Reference

### Quick runbook

For a concrete command sequence used on this stack (`git`-anchored), use:
`references/heartbeat-intake-validation-session-notes.md`.

### Message Attribution

Messages prefixed with `[I]` or similar markers = user's outgoing messages. They are NOT skipped - analyze for commitments, promises, delegations.

### Action Item Signals

| Signal | Example | Action |
|--------|---------|--------|
| Incoming request | "need to scrape those groups" | Task |
| User approval | "let's do it", "ok" | = commitment, track |
| User delegation | "X please handle this" | Track + check tracking issue |
| User promise | "I'll send it tomorrow" | Task with due date |
| Agreed meeting | "let's sync Thursday" | Calendar + Task |
| Partner waiting | No reply >24h | Reminder Task |

### Rules

- **Draft-only for external** - Email drafts (never send), Calendar without attendees, reply suggestions (never send directly)
- Tasks - full write access (via task-management skill)
- Knowledge base People/Organizations/Deals - full access
- Inbox/ - full access (write freely, Reflection grooms nightly)
- Feed output: stdout only (cron delivers). DO NOT send messages directly through messaging APIs
