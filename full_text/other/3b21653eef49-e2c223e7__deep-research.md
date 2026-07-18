---
name: deep-research
description: Multi-platform deep research with reputation-gated sources, two-hop trust expansion, parallel platform fan-out (Web + GitHub + Reddit + X + NotebookLM-YouTube), adversarial review, and a required Disagreement Ledger. Use whenever the user asks for "research", "deep dive", "investigate", "what's the state of", "compare X vs Y", "is there prior art for", "what are people saying about", competitive analysis, technology evaluation, due diligence, or any question needing synthesis from multiple sources with citations. Prefer this over single-platform search even when the user doesn't explicitly say "deep research" — if the question would benefit from GitHub prior-art + community signal + grounded synthesis, use this skill.
---

# Deep Research

> **Drift-prone.** This skill orchestrates external CLIs (`gh`, `notebooklm`, `yt-dlp`) and optional MCPs (Reddit/X). Tool names, quotas, and result shapes change. Treat the platform arms as best-effort, design for graceful degradation, and never promise coverage you can't verify.

Multi-platform research with explicit disagreement surfacing. Inherits the parallel-agent + credibility-tier structure from [ahrav/Gossip-rs/deeper-research](https://github.com/ahrav/Gossip-rs/blob/main/.claude/skills/deeper-research/SKILL.md) and the NotebookLM-as-RAG arm from [manfromtunis/melek-skills/deep-research](https://github.com/manfromtunis/melek-skills/blob/main/deep-research/skill.md), with three additions specific to this skill: triage routing by topic-volatility, two-hop trust expansion to surface unknown-but-important voices, and a required Disagreement Ledger to prevent synthesis from papering over real conflict.

## When to activate

- Explicit: "deep research X", "deep dive into X", "research X thoroughly", "/deep-research"
- Implicit but high-confidence: "what's the state of X", "is there prior art for X", "compare X vs Y", "what are people saying about X", "investigate X", "due diligence on X", "competitive landscape for X"
- Coding-flavored: "has anyone built X already", "what libraries exist for X", "what's the canonical way to do X in 2026"

If the question would benefit from multi-source synthesis with citations, activate even if the user didn't explicitly request "research." Single-platform search (just WebSearch, just a `gh` query) is the wrong response when the user needs grounded confidence across sources.

## What each arm is FOR (purpose-first, not mechanic-first)

Each arm answers a fundamentally different research question. Don't confuse them — using Reddit when you needed documentation, or web search when you needed sentiment, produces bad reports.

| Arm | The question it answers | Why other arms can't |
|---|---|---|
| **Web** (Exa / Firecrawl / WebSearch) | "What does the static published record say?" — documentation, blogs, news, official posts | Slow to capture community execution reality; misses what people *think* |
| **GitHub** | "Has this been built? How does the real implementation work?" — repos as ground truth for what code exists | READMEs lie / oversell. **For reputable-looking repos, READ THE SOURCE.** That's where execution reality lives. |
| **Reddit + X** | "How are practitioners actually deploying this — AND what do they think of it?" — **deployment intelligence** (configs, prompts, workflows, war stories shared in threads) + **sentiment** (hype vs real, what people switched from/back to) | GitHub captures *codified* execution; Reddit/X capture the *unwritten* execution intelligence — the CLAUDE.md someone posted, the hook recipe in a comment, the "after 6 months of using X, here's what works" thread |
| **NotebookLM-YouTube** | "What have specific creators said in long-form (multi-hour) content?" — transcript-grounded RAG over videos/podcasts | In-context reading can hold ~2 videos max; this scales to 30+ with grounded retrieval |
| **Gemini Deep Research** | "What's the macro landscape with full provenance?" — multi-hop autonomous synthesis across 80–160 sources | Single-arm searches can't run their own follow-up loops |

## The five things this skill does that generic web-search doesn't

1. **Triage routes the query** — coding questions hit GitHub first; bleeding-edge AI hits social first; stable topics hit web/academic first. The routing exists because the *same* query "what's new in X" needs different platforms depending on what X is.
2. **GitHub prior-art is a first-class arm with source-code inspection** — for coding queries, the skill scans `gh search repos/code` AND, for repos that look reputable (stars, recent commits, real maintainers), reads the actual source code — not just READMEs. READMEs market; source code reveals.
3. **Sentiment + deployment intelligence from community channels** — Reddit and X aren't just "more sources." They serve two jobs no other arm can: (a) telling you what people actually *think* (hype vs real, what they switched from/back to), and (b) capturing the *unwritten* execution intelligence — the configs, prompts, hooks, and "here's my setup" recipes that practitioners share in threads but never push to a repo.
4. **Two-hop trust expansion** — the trusted-creator allowlist is a *kernel*, not a boundary. If `karpathy` quote-tweets an unknown account, that account is included with a `provisional` tag. Trust propagates one hop via human endorsement, with the chain preserved in output.
5. **Disagreement Ledger is required** — synthesis must enumerate factual claims where sources conflict, name both, and refuse to resolve. Coherent-but-misleading reports are the failure mode; this fights it directly.

## Workflow at a glance

```
Phase 0  Triage             classify query → routing flags
Phase 1  Decompose          3–5 sub-questions, tag platforms per Q
Phase 2  Fan-out (parallel) Web + GitHub + Reddit + X + NotebookLM-YouTube  ← subagents
Phase 3  Reputation gate    pre-filter blocklist, classify each source: trusted | provisional | unverified
Phase 4  Deep read          scrape top-K trusted/provisional; load long-form into NotebookLM
Phase 5  Adversarial review Contrarian Searcher + Devil's Advocate    ← subagents
Phase 6  Synthesize         report with Disagreement Ledger + Prior Art + NotebookLM ID
Phase 7  Persist            save report; notebook stays for follow-up querying
```

Wall-clock target: 8–12 minutes for a substantive query. If the user wants a quick scan, tell them to use plain WebSearch instead — this skill is for questions worth that time.

---

## Phase 0 — Triage

Before decomposing, classify the query along two axes:

**Topic-volatility:**
- **bleeding_edge** — query is about something <12 months old, fast-moving (a new model, a new tool, a new approach). Community signal (Reddit/X/HN) leads.
- **stable** — query is about something established (history, market, science, well-known tech). Web/academic leads.

**Coding-flavor:**
- **coding=true** — query is about libraries, frameworks, implementations, or "has X been built." Forces GitHub arm on.
- **coding=false** — query is about ideas, markets, people, policy.

State the classification explicitly to the user before fan-out: "Triaging this as `bleeding_edge + coding=true` — GitHub arm running first, then social, then web." This makes the routing auditable and gives the user a chance to redirect.

Routing rules (defaults; user can override):

| Triage | GitHub | Reddit/X | Web | NotebookLM-YT |
|---|---|---|---|---|
| `bleeding_edge + coding=true` | priority 1 | priority 2 | priority 3 | priority 3 |
| `bleeding_edge + coding=false` | skip | priority 1 | priority 2 | priority 2 |
| `stable + coding=true` | priority 2 | optional | priority 1 | priority 2 |
| `stable + coding=false` | skip | optional | priority 1 | priority 1 |

`priority 1/2/3` controls source-count budget. `optional` means run only if user asks or sub-question explicitly needs community signal.

---

## Phase 1 — Decompose

Break the topic into **3–5 sub-questions**. Each sub-question must:
- Be answerable from concrete sources (not "what's the meaning of X")
- Tag which arms it most needs (web / github / social / nlm)
- Be diverse — don't ask the same question five ways

Example (query: "current state of multi-agent deep-research systems for Claude Code, open-source"):
1. What open-source multi-agent research skills exist for Claude Code? **[github, web]**
2. What architectures do they use — orchestrator-worker, debate, ReAct? **[web, github]**
3. What benchmarks (GAIA, HLE) measure their performance? **[web, nlm]**
4. What are practitioners saying about strengths/weaknesses on Reddit/X? **[social]**
5. What does Anthropic's own multi-agent research pattern document recommend? **[web]**

Output Phase 1 to the user. Lets them redirect before you burn compute.

---

## Phase 2 — Parallel platform fan-out

**Spawn one subagent per active platform arm via the Agent tool.** Each arm runs independently — no shared state, no waiting on each other. Each gets a hard 90-second wall-clock budget and must return a structured payload:

```json
{
  "arm": "github",
  "status": "ok" | "degraded" | "failed",
  "sources": [{"url": "...", "title": "...", "snippet": "...", "platform_metadata": {...}}],
  "missing": "what we couldn't get and why"
}
```

`status: degraded` means partial results returned; `failed` means nothing usable. Synthesis must explicitly list which arms degraded in the report metadata.

### Web arm
- Tool: WebSearch + WebFetch
- Discover via 2–3 keyword variations of each sub-question
- Output: ~5–10 URLs per sub-question, with snippets

### GitHub arm (if `coding=true`)
- Tool: Bash → `gh search repos <topic> --sort stars --limit 15` and `gh search code <topic> --limit 10`
- For top 3–5 repos by stars + recency: fetch README via `gh api repos/<owner>/<name>/readme`
- **If a repo passes the "looks reputable" filter** (>500 stars OR official org OR commits in last 30 days OR clear license + tests + docs): **inspect the actual source code**, not just the README. Use `gh api repos/<owner>/<name>/contents/<path>` to walk the directory tree, then read the load-bearing files (the main entry point, the core algorithm, the part that's specific to the user's question). READMEs market — source code reveals. Note in the report which repos you source-inspected vs. which you only README-read.
- Classify each repo: **fork-this / study-and-adapt / ignore** with one-sentence justification rooted in what you saw in the *code*, not just claims in the README
- This becomes the **Prior Art** section of the final report — surfaced *before* web research synthesis so the user can decide "stop, I'll just fork that" early

### Reddit arm (if installed: reddit-mcp; else fallback)
**Two jobs, both load-bearing:**
1. **Deployment intelligence** — capture *how* practitioners are actually using the thing. Configs, prompts, workflows, hooks, CLAUDE.md snippets shared in threads, "here's my setup" posts, recipes pasted into comments. This is execution detail that often doesn't make it into formal repos or blog posts.
2. **Sentiment** — capture what people *think*. Hype vs real, what they switched from/back to, postmortems, "is anyone else seeing X" threads.

- Preferred: `mcp__reddit__*` tools from [karanb192/reddit-mcp-buddy](https://github.com/karanb192/reddit-mcp-buddy) or similar — query trusted subs from `references/trusted-creators.yaml`
- **Two distinct search patterns** depending on which job you're doing:
  - For deployment intelligence: search for `"my CLAUDE.md"`, `"my setup"`, `"the hook I wrote"`, `"here's how I"`, `"my workflow"`, configuration-dump posts
  - For sentiment: high-upvote complaints, "I switched back to X" threads, day-N postmortems, comparison posts, "is anyone else seeing X" threads
- Often you want BOTH for the same query — surface the practitioner configs *and* what users think of them
- **Rate-limit guard**: when running in anonymous mode (no `REDDIT_CLIENT_ID`/`SECRET` configured), the MCP is capped at 10 req/min. Pace your calls — pause 7 seconds between consecutive Reddit tool invocations to stay under the limit. Batch multiple subreddit queries into single `search_reddit` calls where possible rather than many `browse_subreddit` calls.
- Fallback: WebSearch with `site:reddit.com <topic>` filtered to trusted sub list
- Note in output which path you took so user knows MCP install would improve fidelity

### X arm (via official xai-sdk — no third-party MCP)
**Same two jobs as Reddit, with a recency bias:**
1. **Deployment intelligence** — practitioners posting their actual configs, prompts, hooks, CLAUDE.md snippets, workflow screenshots. X tends to surface individual-creator setups *the day they ship them*.
2. **Sentiment** — bleeding-edge takes that haven't reached blogs yet. What creators post the day a feature ships, before any longform analysis exists.

X is faster than Reddit for both jobs but more fragmented. Use it to catch the very-recent signal Reddit hasn't aggregated yet.

- Primary: `python scripts/grok_xsearch.py "<query>" --accounts <comma,trusted,handles> --since YYYY-MM-DD`
- Uses the bundled [`scripts/grok_xsearch.py`](scripts/grok_xsearch.py) helper, which calls the official [xai-sdk](https://pypi.org/project/xai-sdk/) with `web_search(allowed_domains=["x.com", "twitter.com"])` — Grok's built-in X search via the Agent Tools API. Trust boundary = xAI itself; no third-party wrapper to audit.
- Required: `XAI_API_KEY` in environment (get one at [console.x.ai](https://console.x.ai))
- The helper returns text answer + citations. **The synthesis text contains the real quoted content; the raw `citations` list often contains X search-URL artifacts that are noise.** Trust the synthesis; treat the URL list as a secondary signal.
- `--accounts karpathy,simonw,...` passes those handles to Grok as a **ranking hint**, NOT as a hard `from:` filter (changed 2026-05-21 — `from:` operators were too restrictive and returned zero hits in initial testing). Grok still finds unknown voices, but prefers trusted accounts when they're present.
- Two-hop trust expansion happens organically: Grok will surface accounts that trusted creators have engaged with, even if those accounts aren't on the list.
- Fallback if `XAI_API_KEY` missing: WebSearch with `site:x.com OR site:twitter.com <topic>` — cruder but functional

### NotebookLM-YouTube arm
This arm is **advisory, not authoritative** — see [references/notebooklm-workflow.md](references/notebooklm-workflow.md) for full mechanics. Briefly:

1. Create a **timestamped notebook**: `notebooklm create "deep-research-<YYYY-MM-DD-HHMM>-<slug>" --json` (one notebook per research run; never reuse to avoid cross-session contamination)
2. Discover candidate YouTube videos via `yt-dlp "ytsearch10:<topic>" --flat-playlist -j`; filter to trusted YouTube channels from the allowlist + provisional list
3. Add long-form sources (videos, dense PDFs, long articles) to the notebook: `notebooklm source add <url> --notebook <id>`
4. Wait for indexing: `notebooklm research wait -n <id> --timeout 300`
5. Query for each sub-question: `notebooklm ask "<sub-question>" --notebook <id>`
6. Returns synthesized answers grounded in the loaded sources

**Why advisory only:** NotebookLM's retriever picks ~5–10 chunks opaquely from the pile — you can't see which, and Gemini synthesizes around them. Unknown-but-important voices loaded into the notebook can be silently under-weighted. Treat its answers as one citation alongside direct scrapes, never as a synthesis substrate.

### Gemini Deep Research arm — macro landscape (paid, slow, optional)
This arm is the **second-order reasoning engine** — it doesn't search a single platform, it runs its own multi-hop research loop with 80–160 sources and produces a comprehensive landscape report. Use it when you want the official-narrative, deeply-cited macro analysis that web/Reddit/X arms aren't built for.

1. Invoke the bundled helper: `python scripts/gemini_deep_research.py "<research query>" --agent <preview|max> --json --output landscape.md`
2. `preview` agent: ~20 min wall-clock, ~80 queries. Default.
3. `max` agent: up to 60 min wall-clock, up to 160 sources. Use only for substantial topics where depth justifies time.
4. Helper polls the background job (Gemini DR is async-only) and writes output to file
5. Requires `GEMINI_API_KEY` env var; **paid tier only** as of April 1, 2026

**When to fire this arm:**
- ✅ `stable + coding=false` queries asking for landscape / state-of-the-art / due diligence — its sweet spot
- ✅ `stable + coding=true` for "what's the official architecture / approach" type queries
- ⚠️ Optional for `bleeding_edge` — it may miss very recent (last 2 weeks) content while other arms catch it
- ❌ Skip for narrow / fast / specific code questions (overkill, expensive, slow)

**How it fits with other arms:**
- Other arms find: community signal, code prior art, bleeding-edge takes, X-native posts, long-form video synthesis
- Gemini DR finds: macro landscape, official narrative, broadly-cited consensus, structural analysis
- These are **complementary, not duplicative.** Surface Gemini DR's findings in their own clearly-marked report section; let the Disagreement Ledger explicitly flag where community signal (other arms) diverges from Gemini DR's macro conclusion.

**Cost & time warning:** This is the most expensive single arm. Tell the user explicitly when you're about to invoke `max` — "I'm about to fire Gemini Deep Research Max (60-min budget, paid tier). OK to proceed?" Skip silently for `--quick` mode.

---

## Phase 3 — Reputation gate (with two-hop trust expansion)

Run this **between fan-out and deep-read**, so cost-heavy scraping only hits trusted/provisional sources.

Read [references/trusted-creators.yaml](references/trusted-creators.yaml). For each candidate source from Phase 2:

### Step 1: blocklist (auto-reject, cheap)
- Match against `blocked_patterns` (slop phrases) and `blocked_domains` (known low-quality sites)
- Rejected sources are dropped silently; logged but not reported

### Step 2: trust kernel (auto-trust)
- If source author/domain is in `trusted_creators.x` / `trusted_blogs` / `trusted_youtube` / `trusted_reddit_users` → tag `trusted`
- If source is on a `trusted_venue` (e.g., `r/MachineLearning`, `r/LocalLLaMA`, HN front page, arXiv) AND meets engagement-velocity threshold (>50 upvotes in <4h, or >100 HN points) → tag `trusted` regardless of author

### Step 3: two-hop trust expansion (provisional)
For unknown sources, check the endorsement chain:
- **X**: did any `trusted_creators.x` account quote-tweet / RT / positively reply to this URL or author in the last 30 days? If yes → tag `provisional[via @creator, YYYY-MM-DD]`
- **Blogs**: did any trusted blog outbound-link to this domain in the last 30 days? If yes → tag `provisional[via blog.com]`
- **Reddit**: did a trusted Reddit user upvote-and-comment on this post? → tag `provisional[via u/user]`

**Implementation note for v1**: full automated endorsement-chain crawling is heavy. v1 approach: when surfacing an unknown source in fan-out, do one targeted WebSearch like `"<unknown-author> <topic>" karpathy OR simonw OR <other trusted name>` and check whether trusted creators have engaged with this person in last 30d. Coarse but cheap. v2 can do real graph crawling.

### Step 4: everything else → `unverified`
- Not rejected — flagged in report with `[unverified]` tag
- User decides whether to include

### Canonical source-quality vocabulary
Use one fixed vocabulary so grades are comparable across runs and reports:
- **Source-quality tier** uses the **S / A / B / C / D** ladder — `S` = primary / authoritative, `A` = strong secondary, `B` = credible, `C` = weak / unconfirmed, `D` = junk. This is distinct from the *trust tier* (trusted / provisional / unverified), which is about provenance, not quality.
- Any assertion not yet verified is tagged **`CLAIMED / not-verified-as-of-<YYYY-MM-DD>`** — never asserted bare (pairs with quality rule #3).

These exact tokens are canonical; don't invent synonyms.

### Output of Phase 3
A categorized source pile:
```
trusted:      [list, scrape all]
provisional:  [list, scrape all, flag in citations]
unverified:   [list, include in report w/ flag, do NOT scrape unless trusted/provisional pile is thin]
blocked:      [list, log only]
```

---

## Phase 4 — Deep read

For `trusted` + `provisional` sources only:
- Top 5–8 by relevance get full-text fetch via WebFetch
- Long-form (>5k words, video, dense PDF) was already routed to NotebookLM in Phase 2 — query that notebook for synthesis instead of fetching
- Extract: key claims, quoted numbers, dated assertions, named entities
- Note source platform + trust tier + date on every extracted claim

---

## Phase 5 — Adversarial review

**Spawn 2 contrarian subagents in parallel** (kept lean vs Gossip-rs's 4 — diminishing returns past 2 for most queries):

### Contrarian Searcher
- Prompt: "The current synthesis claims X, Y, Z. Find counter-evidence. Search for: '<X> debunked', '<X> criticism', '<X> failed', '<X> overhyped'. Return sources that *contradict* the current synthesis, not ones that confirm it. If you find nothing, that's a signal — either the claim is solid or the search terms are wrong."
- Output: list of counter-sources with what they specifically contradict

### Devil's Advocate
- Prompt: "Construct the strongest possible counter-argument to the current synthesis. Steelman the opposition. What would the smartest critic say? Rate your own counter-argument's strength 1–10."
- Output: counter-argument + self-rated strength

If counter-argument self-rating ≥7, loop back to Phase 4 with new searches targeting the weak points. Otherwise proceed to synthesis with the counter-points fed into the Disagreement Ledger.

---

## Phase 6 — Synthesize the report

Output uses the template in [references/report-template.md](references/report-template.md). Required sections:

1. **Header** — date, sources count, confidence, **arm-status line** (which arms ran/degraded)
2. **Executive summary** — 3–5 sentences
3. **Prior Art** (if GitHub arm ran) — repos classified fork-this / study-adapt / ignore, before the rest
4. **Major themes** with inline citations tagged by platform + trust tier: `[Source Title](url) [trusted/web]`, `[Tweet](url) [provisional via @karpathy/x]`
5. **Disagreement Ledger** (REQUIRED, even if empty) — enumerate every factual claim where ≥2 sources conflict. Name both. Refuse to resolve. Empty section with "No material disagreements found" is fine if true.
6. **Key takeaways** — 3–5 actionable insights
7. **Sources** — flat list with platform + tier + one-line summary
8. **Methodology** — what arms ran, which degraded, the NotebookLM ID for follow-up querying, the sub-questions investigated

See full template in references.

---

## Phase 7 — Persist

- Save full report to `<cwd>/deep-research/reports/<YYYY-MM-DD>-<slug>.md` (create dir if missing)
- The NotebookLM notebook stays. User can re-query later: `notebooklm ask "<follow-up>" --notebook <id>`
- Report header always includes the notebook ID so the user can audit which sources fed the RAG answers

For short topics, post the executive summary + Prior Art + Disagreement Ledger inline; tell the user the full report path.

### Subagent file-write gotcha (important)

When this skill runs inside a subagent (via the Agent tool), the harness may block direct writes to `report.md` with the message *"Subagents should return findings as text, not write report files."* This is a hard guardrail, not a bug.

**The pattern**: subagents return the full report content **as text** in their final response; the parent (or the user) saves the file. Save `notes.md` (arms-status + degradations) directly — that's allowed.

**Persistent-state recovery**: long-running async operations live outside the subagent's lifecycle:
- **NotebookLM notebooks** persist on Google's servers — if a subagent crashes after loading sources but before querying, the parent can re-query directly: `notebooklm ask "<question>" --notebook <id>`
- **Gemini Deep Research jobs** persist on Google's servers — if the subagent times out at 25 min while DR is still running, the parent can poll the job ID later: `python scripts/gemini_deep_research.py --poll <job_id> --json`

Always include the notebook ID and any Gemini DR job IDs in your output so the parent can recover state if needed.

---

## Required tools

- **WebSearch** (always, primary)
- **WebFetch** (always, for scraping top hits)
- **Bash** (for `gh`, `yt-dlp`, `notebooklm` CLI)
- **Agent** tool (for parallel subagents in Phase 2 and Phase 5)

## Optional tools (degrades gracefully without)

- **Reddit MCP** ([karanb192/reddit-mcp-buddy](https://github.com/karanb192/reddit-mcp-buddy)) — anonymous mode (10 req/min) needs no credentials; falls back to `site:reddit.com` WebSearch if MCP unavailable
- **exa MCP** ([exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)) — semantic neural search, especially good for finding unknown-but-related sources; needs `EXA_API_KEY`; falls back to WebSearch
- **firecrawl MCP** ([mendableai/firecrawl-mcp-server](https://github.com/mendableai/firecrawl-mcp-server)) — handles JS-heavy SPAs better than WebFetch; needs `FIRECRAWL_API_KEY`; falls back to WebFetch
- **xai-sdk** (Python package) — required for the X arm via `scripts/grok_xsearch.py`; `XAI_API_KEY` needed; if absent, X arm falls back to `site:x.com` WebSearch
- **google-genai** (Python package, ≥2.0.0) — required for the Gemini Deep Research arm via `scripts/gemini_deep_research.py`; `GEMINI_API_KEY` needed (paid tier); if absent, the Gemini DR arm is skipped (other arms compensate)
- **yt-dlp** (Python package) — required for YouTube discovery; if missing, NotebookLM arm can still load article URLs but no video discovery

## Local tools assumed present

- **`gh` CLI** — authenticated; for GitHub arm
- **`notebooklm` CLI** ([notebooklm-py](https://github.com/teng-lin/notebooklm-py)) — authenticated; for NotebookLM-YouTube arm. See user's existing [notebooklm skill](../notebooklm/SKILL.md) for the full command surface.

If `gh` or `notebooklm` is unauthenticated, prompt the user with the exact command to fix (`gh auth login` / `notebooklm login`) — don't try to work around it.

---

## Quality rules (hard)

1. **Every claim needs a source.** No unsourced assertions. If you can't cite it, don't write it.
2. **Tag every citation with platform + trust tier AND date.** `[Title](url) [trusted/web, 2026-04-23]`, `[Tweet by @author](url) [provisional via @karpathy/x, 2026-05-12]`, `[Reddit](url) [trusted/r/LocalLLaMA, 3343↑, 2026-05-10]`. Dates inline are MANDATORY for X and Reddit citations — recency claims must be auditable from the report text alone, not just from methodology.
3. **Single-source claims get flagged as unverified.** If only one source says X, the report says "according to one source [X], …" — never the bare assertion.
4. **Quantify before you intensify.** Avoid superlatives like "single most repeated," "dominant pattern," "everyone is saying" UNLESS you can cite a count. Better: "3 of the 6 deployment threads in r/ClaudeCode mention this pattern" or "Surfaced in 4 of 5 Grok queries." If you can't count, soften: "appears across multiple threads" not "the dominant view." Provisional-tier sources especially must be soft-quantified — they're sampled, not exhaustive.
5. **Recency matters for bleeding_edge queries.** Default 12-month window; relax only if the topic is stable.
6. **Acknowledge gaps explicitly.** "Insufficient data found on <sub-question>" is a valid Phase 6 outcome.
7. **No hallucinated citations.** If a URL doesn't resolve, drop the claim or fetch a different source. Never invent a plausible-sounding URL.
8. **Disagreement Ledger is never empty by omission.** If you write "No material disagreements found," it's because you actively looked and didn't find any, not because you didn't check.
9. **Citations from NotebookLM RAG must map to underlying sources.** NLM's numbered citations [1-N] only mean something if you also include a Citation Map appendix listing each NLM source ID + title + URL. Otherwise readers can't audit which claim came from which video. Run `notebooklm source list --notebook <id> --json` and include the resolved map in the report.
10. **Late-arriving async outputs must be integrated, not orphaned.** When a Gemini DR job finishes after a subagent's wall-clock cutoff, the parent (or follow-up turn) must update the main report to either (a) merge the new findings inline, or (b) explicitly link the addendum from the relevant sections of the main report with a `> [!info] Extended landscape analysis: see [gemini_dr_addendum.md]` callout. Don't leave the main report saying "DR degraded" when DR actually completed.

## Cost expectations (rough)

- ~$1–3/run web scraping (WebFetch + optional firecrawl)
- ~50–80k tokens lead-orchestration + 4–5 subagents × ~15k context each
- ~50 NotebookLM source slots/run (free tier: 50; paid: 300)
- 8–12 min wall-clock realistic; tell the user upfront if they want to wait

## Configuration knobs

The skill accepts these optional flags inline in the user prompt:
- `--quick` → skip Phase 5 adversarial review (saves ~3 min)
- `--no-nlm` → skip NotebookLM arm entirely (faster, no notebook artifact)
- `--no-social` → skip Reddit + X arms (use for stable + non-coding topics)
- `--notebook <id>` → reuse an existing notebook instead of creating a new one (use for ongoing research into the same topic over time; otherwise create new to avoid contamination)
- `--quiet` → reduce inline updates to the user (default is verbose so user can redirect)

---

## Bundled references

- [references/trusted-creators.yaml](references/trusted-creators.yaml) — allowlist + blocklist + venue trust thresholds. Maintained by the user; this skill reads but never writes.
- [references/credibility-tiers.md](references/credibility-tiers.md) — the 4-tier credibility system (forked from Gossip-rs) with example domains and weight formula.
- [references/report-template.md](references/report-template.md) — exact Phase 6 output structure.
- [references/notebooklm-workflow.md](references/notebooklm-workflow.md) — full NotebookLM arm mechanics, forked from melek-skills with the timestamped-notebook + advisory-only adjustments.
