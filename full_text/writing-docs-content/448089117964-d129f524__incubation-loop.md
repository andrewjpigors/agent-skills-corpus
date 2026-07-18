---
name: incubation-loop
description: Autonomous iterative thinking loop - processes active topics using rotating analytical moves (ACH, Bayesian updating, steelmanning, cross-domain bridging, implication checks) and persists reasoning state across scheduled runs
automation: autonomous
schedule: "0 7 * * *"
allowed-tools: Read, Write, Grep, Glob, Bash, WebSearch, Skill
user-invocable: true
argument-hint: "[topic-slug] (optional - processes all active topics if omitted)"
metadata:
  version: "1.1"
  updated: 2026-07-03
  changelog:
    - "1.1: Registry size discipline (Step 8) — single one-line last_incubation_run overwritten in place, no _prior_* history keys, no analytical narrative in the registry; converged rows capped to a one-sentence conclusion + pointer to the topic file's Final Synthesis"
    - "1.0: Initial version"
---

# Incubation Loop

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `incubation-loop vX.Y — recent: <summary>`. Then proceed.

Autonomous thinking engine. Each scheduled run advances all active thinking topics by one analytical move, persisting reasoning state across runs until convergence.

## Purpose

Continuous intellectual iteration on open questions. Uses a rotating set of research-validated analytical moves (ACH, Bayesian updating, dialectical steelmanning, cross-domain bridging) to build toward well-grounded conclusions - without requiring human presence in each cycle.

**Design principle:** Each run does one move per topic. Depth accumulates across runs. No single run tries to "solve" the question.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Thinking Registry | `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` | ✓ | ✓ | Active topics + status |
| Thinking Files | `Brain/05-Meta/Thinking/[topic-slug].md` | ✓ | ✓ | Per-topic reasoning journal |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Semantic search for KB evidence |
| Permanent Notes | `Brain/02-Permanent/` | ✓ | | Primary evidence source |
| Session Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Run log |

## Prerequisites

- Registry file exists at `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`
- At least one active topic seeded (see Seeding section below) - or none, in which case the **Starvation Floor (Step 1a)** self-seeds one from the watched domains
- Local Brain Search index up-to-date

## Composes

- `/domain-watch` - invoked by the Starvation Floor (Step 1a) when the active queue is empty, to formulate and activate a new topic from the domains under surveillance. Called by its unversioned name so its fixes propagate.

---

## Process

### Step 1: Get Date and Load Registry

```bash
date '+%Y-%m-%d'
```

Read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`. Parse all topics with `status: active`.

If registry does not exist, create it:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Thinking Registry

Active questions under continuous analysis.

| Topic Slug | Central Question | Status | Runs | Last Run |
|------------|-----------------|--------|------|----------|
```

If no active topics found, do NOT exit - run the **Starvation Floor (Step 1a)** so the thinking engine never idles.

### Step 1a: Starvation Floor (only if zero active topics)

The thinking engine must never sit idle. If Step 1 found **no active topics**:

1. Invoke `/domain-watch` (cross-skill). Its Starvation Floor guarantees at least one new topic is activated into the Thinking Registry, formulated from the domains under surveillance.
2. Re-read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` and parse `status: active` topics again.
3. If one or more active topics now exist, continue to Step 2 and process them this run.
4. Only if `/domain-watch` still produced no topic (e.g. no domains configured), log to changelog and exit cleanly.

This makes topic generation autonomous: when human-seeded questions run out, the agent proactively formulates its own next question from the watched domains rather than going quiet. Crystallization of any resulting conclusion stays manual (human judgment).

### Step 2: For Each Active Topic - Load State

Read `Brain/05-Meta/Thinking/[topic-slug].md`.

Parse frontmatter fields:
- `run_count` (required) - how many iterations completed; drives move rotation
- `last_run` (required) - date of last iteration
- `status` (required) - active / converged / crystallized / retired
- `last_move` (optional, written by loop) - which move was applied in the most recent run; informational
- `convergence_count` (optional, written by loop) - number of consecutive runs at or near convergence criteria; used by framework-exhaustion detection in Step 7
- `topic` (set at seeding) - the central question being analyzed

Parse from body:
- `current_hypotheses` - list with confidence scores (from the most recent run's "Updated Hypotheses" table)
- Last run's "Current Best Answer" and "Open Questions"

### Step 3: Determine Next Thinking Move

Rotate through this sequence. Position = `run_count mod 6`:

| Position | Move | Research Basis |
|----------|------|----------------|
| 0 | **ACH Audit** | Heuer (CIA) - Analysis of Competing Hypotheses |
| 1 | **Bayesian Update** | Information theory - explicit confidence tracking |
| 2 | **Steelman Opposition** | Socratic dialectic - steel-man the opposite |
| 3 | **Cross-Domain Bridge** | Consilience method - what does an unrelated field say? |
| 4 | **Implication Check** | Falsificationism (Popper) - if true, what follows? Is that true? |
| 5 | **Assumption Audit** | Intelligence SAT - which premises are load-bearing and shakiest? |

### Step 4: Run KB Search for Evidence

Use Local Brain Search to find relevant notes:

```bash
cd $PROJECT_ROOT
# --no-track: this is an autonomous loop; its reads must NOT train q-values (scope-primitive learning hygiene)
python3 resources/local-brain-search/search.py "[central question]" --limit 8 --mode spreading --no-track 2>/dev/null
python3 resources/local-brain-search/search.py "[leading hypothesis]" --limit 5 --mode spreading --no-track 2>/dev/null
```

**Environment note (Trinity container):** the bare `python3 .../search.py` form fails on hosts without system-level `faiss` (`ModuleNotFoundError: No module named 'faiss'`) - e.g. the Trinity scheduled-run container. Use the wrapper `./resources/local-brain-search/run_search.sh "[query]" [same flags]` instead; it routes through the running daemon (or a venv fallback) and honors `BRAIN_READ_SCOPE` (defaults fail-closed to `core`). Same flags apply (`--mode static|spreading`, `--threshold`, `--no-track`, `--limit`).

**Mode fallback for narrow technical topics:** Spreading activation propagates through the graph's highest-centrality hubs, so for narrow/technical questions (e.g. AI-architecture, distributed-systems topics) it can return the emotional/neuroscience mega-hubs ([[Dopamine]], [[Flow is a selfless state]], [[In Buddhism - Self is an Illusion]]) as top hits - noise, not evidence. If spreading results are dominated by off-topic hubs, re-run the same queries with `--mode static` (vector similarity), which surfaces the precise topical notes. Use whichever mode yields on-topic evidence; static is often better for technical clusters, spreading for cross-domain/synthesis topics.

**Threshold note (post-2026-06-25 cosine correction):** The corrected `cosine_ip` index lowered raw query→note similarity scores, so the default `--threshold 0.5` now frequently returns "No results found" even for on-topic queries (abstract/technical questions especially). If a search comes back empty, **re-run with `--threshold 0.25` and shorter, keyword-style queries** before concluding the KB has no evidence. Treat 0.25-0.35 hits as candidate evidence to read and judge, not as automatic relevance.

Read the top 3-4 most relevant notes in full. These are the evidence base for this iteration.

### Step 5: Apply the Thinking Move

Execute the move based on what was determined in Step 3. For each move:

#### ACH Audit
- List all current competing hypotheses
- For each piece of KB evidence found: does it support, contradict, or not apply to each hypothesis?
- Build a simple diagnostic matrix (evidence × hypotheses)
- Eliminate any hypothesis that is contradicted by multiple pieces of evidence
- Update confidence scores for surviving hypotheses
- **Output**: Pruned hypothesis list with updated confidence levels

#### Bayesian Update
- State prior confidence in leading hypothesis (from last run)
- Identify new evidence from KB search
- Explicitly reason: "Given this evidence, should I be more or less confident? By how much?"
- Use rough likelihood ratios (e.g., "this evidence is 3x more likely if H1 is true than if H2 is true")
- Compute and record updated posterior confidence
- **Output**: New confidence scores with explicit reasoning for the change

#### Steelman Opposition
- State the current leading hypothesis clearly
- Construct the strongest possible argument AGAINST it - not a strawman
- Search KB explicitly for evidence supporting the opposing view
- Assess: does the steelman change the leading hypothesis, or does it survive?
- If the steelman reveals a genuine weakness, revise the hypothesis
- **Output**: Steel-manned opposition + response + any hypothesis revision

#### Cross-Domain Bridge
- Identify the core mechanism or pattern in the current question
- Run KB search from an unrelated domain (e.g., if topic is about AI, search neuroscience or Buddhism)
- Find analogous patterns or contradictory evidence from that domain
- Extract what the foreign domain implies about the current question
- **Output**: Cross-domain insight + revised framing of the question (if warranted)

#### Implication Check
- Take the current leading hypothesis as given (temporarily)
- Derive 3-5 concrete, testable implications that should be true if the hypothesis holds
- Search KB and reason about whether those implications are actually supported
- **External probe (this move only — no other move uses WebSearch)**: If an implication concerns time-sensitive empirical state the KB cannot resolve, run up to **2 web searches per topic per run** to test it. Restrict queries to reputable sources via `site:` filtering — peer-reviewed (arxiv.org, nature.com, science.org, pubmed.ncbi.nlm.nih.gov), established outlets (economist.com, ft.com, reuters.com, apnews.com, bloomberg.com), analytical (hbr.org, quantamagazine.org). (This is a subset of the canonical allowlist in `resources/SOURCE-AUTHORITY.md` — kept inline for in-query reliability; keep in sync with that file.) **Crawler caveat:** several of these domains (reuters.com, apnews.com, ft.com, economist.com) are *not accessible to the WebSearch user-agent* and an `allowed_domains` probe restricted to them returns a 400 error — wasting one of the 2 probes. Do NOT pass those as a hard `allowed_domains` filter; instead run the query **unrestricted** (or allow only the crawlable reputable domains: bloomberg.com, nature.com, arxiv.org, hbr.org, and analytical trackers like CSIS/RUSI/AEI/Jamestown) and judge source quality manually. Tag each external finding as `[EXTERNAL: source — date]` in the run output so KB-grounded vs. web-augmented evidence is auditable.
- If an implication is clearly false, that is disconfirming evidence for the hypothesis
- **Output**: Implications assessed as supported/unsupported/unknown + impact on hypothesis confidence

#### Assumption Audit
- List the 3-5 key assumptions the current reasoning rests on
- Rank by: (a) how load-bearing for the conclusion, and (b) how uncertain/shaky
- Focus scrutiny on high load-bearing + high uncertainty assumptions
- For the shakiest assumption: search KB for evidence bearing on it
- **Output**: Assumption vulnerability map + revised conclusion if key assumption weakens

### Step 6: Write Updated Thinking File

Append to `Brain/05-Meta/Thinking/[topic-slug].md`:

```markdown
### Run [N]: [Move Name] - [YYYY-MM-DD]

**KB Evidence Consulted:**
- [[Note A]] - [one line on relevance]
- [[Note B]] - [one line on relevance]

**Analysis:**
[2-4 paragraphs of actual reasoning from the move]

**Updated Hypotheses:**
| Hypothesis | Confidence | Change |
|-----------|------------|--------|
| H1: [statement] | X% | ↑/↓/→ from Y% |
| H2: [statement] | X% | ↑/↓/→ from Y% |

**Current Best Answer:** [1-2 sentences - the leading position after this run]

**Open Questions for Next Run:** [What remains unresolved or most worth probing]
```

Update the frontmatter: `updated`, `updated_by`, `run_count`, `last_run`.

### Step 7: Check Convergence

A topic has converged when ANY of the following holds:

**Standard convergence (all four must be true):**
- `run_count >= 4` (minimum 4 cycles)
- Same hypothesis has led for 3+ consecutive runs
- Confidence delta between last two runs < 5 percentage points
- No major open questions flagged in last run

**Framework exhaustion (alternate path - triggers automatic convergence):**
- `run_count >= 10` AND
- The top two hypotheses have not changed relative order for 5+ consecutive runs AND
- Neither leading hypothesis's confidence has moved by more than 2pp across those 5 runs

When framework exhaustion is detected:
1. Apply one final Assumption Audit move on the *framework itself* (not the evidence). Ask: is the analytical framework (hypothesis structure, key distinctions) discriminating between meaningfully different world-states, or producing precision on an empirically-indistinct difference?
2. Note the assessment in the run output explicitly
3. Converge regardless of whether external "open questions" remain — those questions belong to a different topic (often: a parameter or timing question, not the structural question that was asked)

This guards against the "Confirmation Bias as Hyper-Precise Prior" failure mode: an analysis that produces ever-finer confidence scores on a distinction that the evidence has already shown to be analytically empty.

If converged (either path):
- Set `status: converged` in the thinking file frontmatter
- Append the canonical Final Synthesis block (see below)
- Add note: `**CONVERGED** - Ready for crystallization via /manage-thinking-topics crystallize [slug]`
- Update registry status to `converged`

If not converged: continue to next topic.

**Canonical Final Synthesis block** (appended once when status flips to `converged`):

```markdown
---

## Final Synthesis

**Conclusion:** [1-2 paragraphs in plain prose - the substantive answer]

**Confidence:** X% on H[N] (and any co-leading hypotheses)

**Key evidence:**
- [[Note A]] - [why it mattered]
- [[Note B]] - [why it mattered]
- [[Note C]] - [why it mattered]

**Convergence path:** [Standard | Framework exhaustion] after [N] runs

**Remaining uncertainty:** [1 paragraph - what's known to be unknown; what could change this]

**Related topics:** [[other-converged-slug]] (if causally connected)
```

This block is the authoritative source for crystallization. Crystallize mode reads this section first, falls back to scanning the last run's "Current Best Answer" only if absent (legacy topics).

### Step 8: Update Registry

Update `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`:
- Increment run count for each processed topic
- Update last_run date
- Update status (active → converged where applicable)
- On convergence, MOVE the topic's row from **Active Topics** to **Converged (Ready for Crystallization)** using this exact row shape:

  ```
  | [slug] | [runs] | [one-sentence conclusion, ≤200 chars] → [[slug]] | [YYYY-MM-DD] |
  ```

**Registry size discipline (hard rules — the registry is an index, not a journal):**

1. Registry frontmatter may contain ONLY: `created`, `updated`, `created_by`, `updated_by`, `agent_version`, and a single `last_incubation_run` field of AT MOST one line (~200 chars): timestamp + topic(s) + move + resulting status. Example:
   `last_incubation_run: 2026-07-03 07:00 UTC — agent-zero-trust-primitive Run 1 ACH Audit, still active`
2. OVERWRITE `last_incubation_run` in place each run. NEVER append `last_incubation_run_prior_*` or any other run-history keys.
3. NEVER write analytical narrative into the registry — full reasoning already lives in the topic file (Step 6) and the session changelog (Step 9). Duplicating it in the registry made it unreadable (~100k tokens) and taxes every skill that loads it.
4. Converged-table conclusion cells stay at ONE sentence; the authoritative synthesis is the topic file's `## Final Synthesis` block, which crystallize mode reads directly.
5. If legacy oversized fields or rows exist in the registry, do NOT imitate them — follow this format.

### Step 9: Write Session Changelog

Write to `Brain/05-Meta/Changelogs/CHANGELOG - Incubation Loop YYYY-MM-DD.md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Incubation Loop Session: YYYY-MM-DD

## Topics Processed

| Topic | Move Applied | Confidence Shift | Status |
|-------|-------------|-----------------|--------|
| [slug] | [move name] | [leading H]: Y% → Z% | active/converged |

## Notable Shifts
[Any hypothesis revisions, convergences, or surprising KB evidence]

## Converged Topics (Ready for Crystallization)
[List any topics that reached convergence this run]
```

---

## Seeding a New Topic

To add a topic to the loop, create `Brain/05-Meta/Thinking/[topic-slug].md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
topic: "[exact question being analyzed]"
run_count: 0
last_run: null
last_move: null            # optional - written by loop after each run
convergence_count: 0       # optional - written by loop; tracks consecutive runs meeting convergence criteria
status: active
---

# Thinking: [Topic Title]

## Central Question
[The exact question. Precise framing matters - ambiguous questions stay ambiguous.]

## Why This Question Matters
[1-2 sentences on stakes or relevance]

## Initial Hypotheses
| Hypothesis | Initial Confidence | Basis |
|-----------|-------------------|-------|
| H1: [statement] | X% | [prior knowledge or intuition] |
| H2: [statement] | X% | [prior knowledge or intuition] |

## Known Evidence (Pre-Run)
[Any notes or sources already known to be relevant]

## Constraints and Assumptions
[What are you taking as given? What's out of scope?]

---
*[Analytical runs will be appended below by the incubation loop]*
```

Then add to `THINKING-REGISTRY.md`:
```
| [topic-slug] | [central question] | active | 0 | null |
```

---

## Crystallization (Manual)

When a topic reaches `status: converged`, the human should:

1. Read the full thinking file
2. Run `/synthesize-insights [topic-slug]` to graduate conclusions to a permanent note
3. Archive thinking file: set `status: crystallized`
4. The permanent note becomes part of the KB for future searches

**Do not automate crystallization** - judgment calls about what conclusions deserve permanence belong to the human.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Registry missing | Create empty registry, log, exit cleanly |
| No active topics | Run Starvation Floor (Step 1a) - invoke `/domain-watch` to self-seed a topic from watched domains; only log and exit cleanly if it too produces nothing |
| KB search returns empty | Try alternate search terms from hypothesis text; if still empty, note in run log and skip KB-grounding for this move |
| Thinking file missing for active topic | Log warning in registry, skip topic |
| Run exceeds 45 minutes | Process topics in order; skip remaining, log which were skipped |

---

## Completion Checklist

- [ ] Registry read - active topics identified
- [ ] Each active topic: KB searched with relevant queries
- [ ] Each active topic: correct move in rotation applied
- [ ] Each active topic: thinking file updated with reasoning + confidence scores
- [ ] Convergence checked for each topic
- [ ] Registry updated (run counts, dates, status changes)
- [ ] Session changelog written to `Brain/05-Meta/Changelogs/`

---

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could the thinking moves, convergence criteria, or file structure be sharper?
- [ ] **Scope check**: Only execution changes - NOT changes to the ACH/Bayesian/dialectic framework itself
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control**:
  - [ ] `git add .claude/skills/incubation-loop/SKILL.md`
  - [ ] `git commit -m "refactor(incubation-loop): <brief improvement>"`
