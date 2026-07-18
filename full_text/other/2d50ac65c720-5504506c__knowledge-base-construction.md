---
name: knowledge-base-construction
description: Use when building a research knowledge base on a controversial topic — typically invoked by /research. Builds an argument graph (not just a source pile) by gathering sources, extracting argument nodes, drawing typed edges between them, recursively tracing claims to primary sources, rating argument strength, and surfacing contradictions. Iterative — runs multiple passes until the graph is stable. Optional exploratory mode pulls in fringe/extreme sources with a generous-then-critical-then-realist read.
---

# knowledge-base-construction

Build a knowledge base for a controversial topic. The KB is an **argument graph grounded in primary sources**, not a flat source dump. Output is self-contained and useful on its own — the adversarial-debate skill is one consumer of this KB, but the KB stands alone as a research artifact.

## What the hook handles vs what you handle

The plugin ships a hook system (`scripts/kb-tool.py` + `PostToolUse` / `Stop` hooks in `plugin.json`) that takes the rote, mechanical work off your plate. Treat the split as load-bearing:

**Hook-managed (mechanical, deterministic — DO NOT do these by hand):**

- **Source cache** at `~/.cache/adversarial-research/` (override via `ADVERSARIAL_RESEARCH_CACHE`). Content-addressable storage of raw fetched data, deduped by DOI then by canonical URL. Same paper across multiple research topics is downloaded once.
- **OA discovery** via Unpaywall → PubMed Central → preprint servers, in that order. Legal OA copies only; the cache does not use Sci-Hub.
- **Paywall detection.** When a peer-reviewed source has no legal OA copy, the hook flags it as paywalled in the cache metadata. The source stays in the KB; its limitation becomes visible to the validator and downstream consumers. Do not exclude paywalled major-journal papers.
- **Index maintenance.** When you write a source file under `kb/sources/`, the hook automatically updates `kb/sources/index.md` (or the per-agent index for files under `kb/sources/agents/<agent>/`). When you write an `arg-NNN-*.md` under `kb/arguments/`, the hook updates `kb/arguments/index.md`. When you write a `kb/entities/<slug>.md`, the hook updates `kb/entities/index.md`. **You do not write to these index files yourself** — anything you write there will be overwritten on the next index rebuild.
- **Narrative log (`kb/log.md`).** Append-only chronological record. The hook auto-appends entries on every source ingest, source update, arg create/update, entity create/update, first-time fetch, and lint run. Format: `## [YYYY-MM-DD HH:MM UTC] <kind> | <title>` followed by a one-line summary. Greppable by kind (e.g. `grep '^## \[.*\] ingest '`). You can append your own narrative entries when something happens that the hook doesn't auto-capture (debate-mutation summaries, gap-finding notes, end-of-pass syntheses).
- **Fetch logging.** Every `WebFetch` / `WebSearch` / MCP research-tool call (PubMed, bioRxiv, Consensus) is logged to `kb/.fetch-log.jsonl` and to the global `~/.cache/adversarial-research/fetch-log.jsonl`. Cached responses are stashed in the source cache automatically.
- **Validation.** On `Stop` / `SubagentStop` the hook runs the validator across the run-dir and emits structured findings (errors, warnings, infos). Read the findings and fix any errors before reporting the phase complete.
- **Lint.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/kb-tool.py lint <run-dir>` (or invoke `/kb-lint <run-dir>`) for graph-level mechanical lint: orphan args, dangling-empirical-basis args, unreferenced sources, status-stale candidates. Output goes to `kb/.lint-report.json` and a summary entry to `kb/log.md`. Pair with the `kb-linting` skill for the semantic part of lint (engagement drift, traceback completeness, central-question coverage, contradiction-status drift, entity-page opportunities).

**You-managed (judgment, semantic):**

- The actual content of source files: extracted findings, Author network analysis, Criticism, Quality notes, generous/critical reads in exploratory mode.
- Argument extraction: deciding what claims warrant a node, writing Statement / Evidentiary basis / edge sections / Traceback notes / Strength assessment.
- The argument graph itself: which edges to draw (`supports`, `refutes`, `addresses`, `tangential-to`, `scope-mismatch-with`, `layer-shift-from`, etc.). The hook does not write to `edges.md` or `contradictions.md` — those are pure judgment.
- Strength ratings, layer/scope assignments, traceback completeness assessments.
- Quality summary — narrative description of the graph, central questions, engagement asymmetries.

If the hook ever appears to disagree with you (e.g. flagging a source as missing PDF when you believed it was fine), trust the hook for the mechanical fact (the PDF really isn't downloaded) and fix the underlying issue (find an OA URL or document why it's paywalled). The hook does not make semantic claims.

## Where to look during a run

- `~/.cache/adversarial-research/` — source cache (raw downloaded data, metadata.json with Unpaywall results)
- `<run-dir>/kb/.fetch-log.jsonl` — every fetch this run has done
- `python3 <plugin-root>/scripts/kb-tool.py validate <run-dir>` — invoke the validator manually anytime
- `python3 <plugin-root>/scripts/kb-tool.py cache-status` — cache stats
- `python3 <plugin-root>/scripts/kb-tool.py cache-lookup --doi <doi>` — check what the cache has for a given DOI

## Core principle: claims must trace to primary sources

This is the central discipline of this skill. Read it carefully and apply it everywhere.

**No secondhand claims.** "The AAP says X" is a claim about the AAP, not about X. To use X you must trace through to the **primary source** the AAP relied on — the actual study, the actual data, the actual policy text — and cite that. If the AAP statement doesn't cite a study, that absence is itself a finding worth recording.

**Recursive tracing.** When a source cites another source, follow the chain. Meta-analysis → inclusion criteria + each underlying study. Review article → the primary studies it summarizes. Policy statement → its evidence base. Press release → the underlying paper. Keep going until you hit raw data, an unverifiable assertion, or a dead end. **A dead end is a finding.** If a widely-repeated claim has no primary source you can locate, that's a critical fact about the claim's strength.

**Authority is not evidence.** A prestigious organization endorsing a claim is evidence about the organization's stance, not about the claim's truth. The KB never grants strength based on who said something — only on what the traceback reveals.

**Author/network tracing.** When one author or a tight network of co-authors dominates a position's literature (canonical patterns: a small group of co-authors at one institution generating most of the favorable primary studies; a single high-influence senior author appearing on 5+ supportive papers spanning a decade), explicitly map: who they coauthor with, their institutional/funding ties, what the broader literature and methodological critics have said about them. This goes in the per-source template's `Author network` section. Network concentration is itself a finding — it doesn't refute the work, but it changes how independently-replicated the body of evidence really is.

**Active cross-source criticism.** When source X criticizes source Y, write the criticism into Y's `Criticism` field with a back-pointer to X (and vice versa). The corpus becomes a graph of mutual critique, not a flat list.

This principle applies in every phase below. If at any point you find yourself about to use a claim without a primary-source trace, stop and trace it first.

## Inputs

- A **topic** (and optional subtopic) — passed by the caller.
- A **run directory** — `./research-runs/<topic-slug>/` by convention. The slash command creates `kb/` inside it. All paths below are relative to the run directory.
- An optional **mode flag**: `standard` (default) or `exploratory`. The exploratory mode is described below.

If any of these are missing or unclear, stop and ask the caller.

## Output: the KB

```
kb/
  sources/                        # source files, written-on-access (Phase 1)
    peer-reviewed/
    media/
    media/missing-citation/
    retracted/
    corrected/
    fringe/                       # only used in exploratory mode
    institutional/                # policy statements, official positions
    [other categories as needed]
    index.md                      # source index (HOOK-MANAGED, do not edit)
  arguments/                      # one file per argument node
    arg-001-<slug>.md
    arg-002-<slug>.md
    ...
    index.md                      # argument index (HOOK-MANAGED, do not edit)
  entities/                       # OPTIONAL: profiles for people, orgs, key studies, named concepts
    <slug>.md                     # one file per entity
    index.md                      # entity index (HOOK-MANAGED, do not edit)
  edges.md                        # typed edges between argument nodes
  contradictions.md               # surfaced structural / evidentiary / ethical contradictions
  quality-summary.md              # narrative description of the graph state — your entry point
  log.md                          # narrative chronological log (HOOK-APPENDED)
  .fetch-log.jsonl                # machine fetch log (HOOK-MANAGED)
  .lint-report.json               # machine lint report (HOOK/SCRIPT-MANAGED)
  .arg-state.json                 # internal state for arg-update tracking (HOOK-MANAGED)
  .entity-state.json              # internal state for entity-update tracking (HOOK-MANAGED)
```

Phase 1 creates `kb/sources/` subdirs on-demand. Phases 2+ create `kb/arguments/` and the meta files. `kb/entities/` is optional; create it (and entity files in it) when consolidating scattered info about a recurring person/org/study/concept is useful — see "Entity pages" below.

## Phases (iterative)

The phases below describe one **pass** through the KB. The skill is iterative: after Phase 7 you may re-enter at Phase 1 with targeted source hunts to fill gaps the graph revealed. Continue until the **graph is stable** — meaning a full pass produces no new arguments, no rating changes, no new contradictions. Most non-trivial topics need 2–4 passes.

## Traceability discipline (mandatory)

The construction process must be **auditable post hoc from `kb/log.md` alone.** That means decisions and phase boundaries are recorded as they happen, not reconstructed afterward from the resulting files. A reader who has access only to the log should be able to follow the construction's reasoning trail.

The hook auto-logs concrete artifacts (every source ingest, arg create/update, entity create/update, first-time fetch, lint run). What the hook **cannot** capture, you must log explicitly via `kb-tool.py` subcommands:

- **Phase boundaries** — at the start and end of every phase, invoke `phase-mark`:
  ```
  python3 <plugin-root>/scripts/kb-tool.py phase-mark <run-dir> P<N> start --note "<what this phase will do>"
  python3 <plugin-root>/scripts/kb-tool.py phase-mark <run-dir> P<N> end   --note "<what came out>"
  ```
- **Graph-level decisions** — when a non-obvious choice is made (split an arg, merge two args, promote/downgrade a rating, decide a contradiction is C-NNN-worthy, decide an asymmetry is corpus-real-after-search), invoke `log-decision`:
  ```
  python3 <plugin-root>/scripts/kb-tool.py log-decision <run-dir> --gist "<one-line>" --detail "<rationale>"
  ```
- **Rejected paths** — when a source / arg / edge is substantively considered but not adopted (low quality, off-topic, redundant with another source already imported, would-be-arg actually subsumed in existing one), invoke `log-reject`:
  ```
  python3 <plugin-root>/scripts/kb-tool.py log-reject <run-dir> --kind <source|arg|edge> --target "<ref>" --reason "<why>"
  ```
  Don't log every passing-glance reject — only ones a careful auditor would want to know were considered.
- **End-of-pass synthesis** — at the end of every iteration pass, invoke `log-pass` with stats:
  ```
  python3 <plugin-root>/scripts/kb-tool.py log-pass <run-dir> --pass <N> \
    --summary "<what changed in this pass>" \
    --stats '{"sources_added":N,"args_added":M,"edges_added":K,"contradictions_added":J,"ratings_changed":L}'
  ```

These four event kinds (`phase`, `decision`, `reject`, `pass`) are greppable in `kb/log.md` alongside the auto-logged kinds (`ingest`, `arg-create`, `fetch`, `lint`, etc.). The combination forms a reconstructable timeline.

**Why mandatory:** without explicit logging, the construction is a black box — readers see what came out, not how it was built. With the logging discipline in place, the construction is itself a research artifact: the reasoning is preserved, defensible, and reproducible by another researcher who can see what was rejected and why, what was hard, where uncertainty was acknowledged.



### Phase 1: Source gathering (broad on first pass, targeted afterward)

- Search broadly. **First pass** prioritizes peer-reviewed scientific literature and primary-source policy/legal documents, plus reputable science communication. Use available MCP research tools (PubMed, bioRxiv, Consensus) when relevant.
- **Subsequent passes** are targeted: hunt for the primary sources that gap-bearing arguments need, the disconfirming evidence missing from the corpus, the original studies behind widely-repeated secondhand claims, replications of single-study findings.
- **Write-on-access (mandatory).** Every time you fetch a source via `WebFetch`, `WebSearch`, or an MCP tool, **immediately** write the retrieved content to `kb/sources/<subdir>/<slug>.md` using the per-source template (below). Do not batch source writing for later. Context can compress; sessions can end; only what's on disk survives. (The fetch hook also caches the raw response automatically, but the analytical extraction in the source file is your job.)
- **PDF acquisition is hook-managed.** The `PostToolUse` hook on `Write`/`Edit` of `kb/sources/**/*.md` triggers an Unpaywall → PMC → preprint lookup for any source with a DOI or peer-reviewed source_type, downloads the legal OA PDF if found, and stores it in the cache. You don't `WebFetch` the PDF yourself; just write the source file with `doi:` and/or `url:` populated and the hook handles the rest. If no legal OA exists, the cache flags the entry paywalled and the source stays in the KB.
- **Index is hook-managed.** Do not write to `kb/sources/index.md` yourself. The hook rebuilds it on every source-file write. Just include `key_finding:` in your frontmatter — the hook uses it for the index entry.
- For substantive `WebSearch` summary results (not just link lists), write a combined summary file: `kb/sources/<subdir>/search-summary-<topic>.md`.

### Phase 2: Argument extraction

Read what's in `kb/sources/`. For every distinct argument or claim you find that's relevant to the topic, create an argument node file at `kb/arguments/arg-NNN-<slug>.md` using the argument node template (below). Index it in `kb/arguments/index.md`.

What counts as "an argument" worth a node:

- A factual claim about the topic (empirical proposition, e.g. "intervention X reduces outcome Y by ~25% in primary-prevention RCTs of population P")
- A normative / ethical claim (e.g. "informed consent requires disclosing absolute risk reduction, not only relative risk")
- A methodological claim (e.g. "open-label trials with subjective endpoints systematically overstate effect sizes")
- A meta-claim about the literature itself (e.g. "the supportive literature on intervention X is concentrated in a tight author network with shared funding ties")

Granularity: small enough that strength rating is meaningful for the node, large enough that you're not creating a node per sentence. When in doubt, split — refining nodes is easy in later passes.

Each argument can be asserted by a position (pro/con/neutral), be derived (built from other arguments via reasoning), or be factual (a finding most of the literature accepts). Mark this in the node frontmatter.

**Layer and scope** are mandatory frontmatter fields for every argument:

- `layer:` — what *kind* of argument this is. One of:
  - `empirical` — factual claims about what is the case (study findings, statistics, observed phenomena)
  - `methodological` — claims about study design, evidence quality, or how to interpret data
  - `ethical/metaphysical` — claims grounded in ethical principles or philosophical commitments (autonomy, harm, bodily integrity, justice)
  - `cultural/religious` — claims grounded in cultural or religious significance/practice
  - `policy/regulatory` — claims about what should be done by institutions, laws, medical practice
  - `meta` — claims *about* the literature or discourse itself
- `scope:` — what conditions the argument actually claims to apply to. Free-form but structured: population, geography, time period, study design, etc. Examples: `women aged 50–69 in the screening trial's randomized cohort, 1990s–2000s cadence`; `subjects unable to provide informed consent, all populations`; `general principle, scope unbounded`.

These fields are what make relevance, scope-mismatch, and layer-shift detectable. **A claim being true within its scope does not mean it applies outside that scope.** A claim at one layer may inform another layer but does not refute it without an explicit cross-layer argument doing the bridging.

### Phase 3: Edge construction

For each argument node, populate the `Supporting`, `Attacking`, `Refining/derivative`, `Depends-on`, and `Engagement` sections by linking to other arg-IDs. Append every edge to `kb/edges.md` (format below). Edges are typed:

**Logical-relationship edges:**

- `supports` — A provides evidence for B
- `contradicts` — A directly opposes B (mutual)
- `refutes` — A specifically and successfully attacks B (one-directional, stronger than contradicts)
- `depends-on` — A requires B to hold
- `refines` — A is a more nuanced version of B
- `exaggerates` — A overstates B's actual claim
- `confounds` — A conflates separate things, blurring B with something else
- `derived-from-source` — A's evidentiary basis is in a specific source file (treated as an edge for graph purposes)

**Engagement / relevance edges** (these are the ones that catch true-but-irrelevant moves):

- `addresses` — A directly engages B's central question at B's layer and within an applicable scope. Genuine engagement.
- `tangential-to` — A is true (or even well-supported) but does not actually engage B's central question. Common pattern: citing a true peripheral claim while leaving B's core question unaddressed.
- `scope-mismatch-with` — A is true within A's declared `scope:`, but A's scope does not cover the domain B speaks to. Canonical example: a screening RCT enrolling women aged 50–69 is cited to recommend screening women in their 40s, when the trial's scope did not sample that age group.
- `layer-shift-from` — A is at a different `layer:` than B and is being used as if it engaged B without an explicit cross-layer bridging argument. Canonical example: a `policy/regulatory` argument ("agency X recommends Y") being used to dismiss a `methodological` argument about the underlying trial's design.

A `layer-shift-from` or `scope-mismatch-with` edge does **not** lower A's strength rating — A may be entirely true within its scope/layer. The flaw is in the *application* of A to B. The edge records that misapplication so the debate and the synthesis can see it.

Edges grow over multiple passes — Phase 3 is never "done" until the graph is stable.

### Phase 4: Strength evaluation (the traceback pass)

For each argument node, do the recursive traceback to its evidentiary basis. Then rate:

- **robust** — traces to peer-reviewed primary sources or sound formal reasoning, key empirical findings independently replicated, no successful refutations in the corpus
- **strong** — traces to good primary sources, some open attacks but none decisive
- **contested** — significant attacks and significant support, the corpus does not currently settle this
- **weak** — traceback reveals thin or methodologically compromised primary support
- **refuted** — successfully refuted by traceback or counter-argument(s) in the corpus
- **baseless** — no primary-source evidentiary basis can be located on traceback (the claim circulates but cannot be sourced)

Write the rating into the node's frontmatter, and write a paragraph in the node's `Strength assessment` section explaining *why* and *what would change the rating*. The "what would change it" matters — it tells future passes (and the debate phase) what evidence to hunt for.

**Important:** *nothing gets deleted*. Refuted and baseless arguments remain in the graph. They are a permanent record that someone, somewhere, asserts this. The debate skill needs them — a side may rest on a baseless claim, and the moderator + opposing side need ready access to *why* it's baseless.

### Phase 5: Contradiction surfacing

Walk the graph. Write findings into `kb/contradictions.md`. Look specifically for:

- **Structural contradictions** — a cycle of `supports`/`depends-on` edges where two members have a `contradicts` edge between them
- **Dangling evidence** — an argument frontmatter-marked as having an empirical basis but Phase-4 traceback found no primary source
- **Within-position incoherence** — a position holding argument A and argument B where A's ethical or factual commitments contradict B's
- **Cross-source factual disagreement** — two primary sources disagreeing on a key empirical question, with no resolution in the corpus
- **Authority/evidence drift** — an authoritative body asserting X while the primary studies it cites do not support X (the AAP-says-Y-but-the-cited-study-shows-Z pattern)

Each contradiction is its own entry in `contradictions.md` with: the involved arg-IDs, the involved source paths, a description of the conflict, and what would resolve it.

### Phase 6: Targeted gap-filling

The graph just told you what it's missing: dangling evidence, contested arguments where one more strong primary source would tip the rating, baseless arguments worth one more search before final-rating. Do targeted Phase-1 sourcing for those specific gaps. Then re-enter Phase 2–5 for the new sources.

**Verify apparent asymmetry before recording it.** If the graph appears one-sided in coverage at a layer (e.g., many methodological critiques of one position and none of the other; one side's arguments cluster at `weak`/`contested` while the other side's cluster at `strong`/`robust`), treat that as a hypothesis to test, not a finding. Do directed search for the strongest-form arguments on the under-represented side: methodological defenses, well-replicated supportive evidence, the most rigorous version of the opposing case, replies to specific named critiques. Look explicitly for what *would* push the under-represented side's nodes upward — the literature very often contains such arguments and they get missed in a first pass.

*Then* conclude. If the asymmetry persists after exhaustive directed search, the asymmetry is itself a finding — record it explicitly in the Phase 7 quality summary as `asymmetric-after-exhaustive-search` rather than leaving it ambiguous between corpus reality and extraction gap. **Do not manufacture junk arguments to fake symmetry — that's exactly the false-balance failure mode the plugin is built to escape.** A controversial topic where one side really does have stronger methodology is a real-world finding; recording it honestly is the point.

When concluding the asymmetry is corpus-real, log the rationale via `log-decision`:
```
python3 <plugin-root>/scripts/kb-tool.py log-decision <run-dir> \
  --gist "asymmetry verified — directed search did not reduce" \
  --detail "Searched for: <list of strongest-form opposing arguments / sources / methodologies attempted>. Found: <what was imported>. Net effect: <how asymmetry changed, e.g. 'deepened via newly surfaced contradictions C-NNN, C-MMM' or 'reduced via import of <source> demonstrating <X>'>. Conclusion: asymmetric-after-exhaustive-search at <layer>."
```
This makes the asymmetry-verification reasoning auditable from the log alone.

### Phase 7: Quality summary

Once the graph is stable, write `kb/quality-summary.md`. This is **narrative**, not just a list. Cover:

- **Central questions** — explicitly identify the deepest layers of the topic question. For most controversial topics there are 2–4 central questions, often at different layers (e.g. for a screening intervention: empirical net-benefit-vs-harm in the screened population; methodological — what populations the trials actually sampled; ethical — what informed consent on absolute-vs-relative risk requires; policy/regulatory — what guidelines should recommend). Name each central question and the arg-IDs that engage it via `addresses` edges. **This anchors what counts as engagement vs. deflection in the debate.**
- The shape of the graph: where the central, robust nodes are; where the weak periphery is; which positions rest on robust foundations and which rest on weak ones
- **Engagement asymmetries** — for each position, note which central questions it actually engages (via `addresses` edges) and which it leaves unaddressed or pivots away from via `tangential-to` / `scope-mismatch-with` / `layer-shift-from` edges. A position that has many strong arguments but engages few central questions is a different finding from a position with weaker arguments that directly engages the central questions.
- **Asymmetries verified by exhaustive search** — when the graph leans heavily one way at a layer (one side's arguments mostly `weak`/`contested`; one side's methodology mostly under critique; one side has many supporting nodes and the other few), state explicitly that Phase 6 directed search for the strongest-form opposing arguments was performed and what it did or did not surface. Asymmetry-after-exhaustive-search is a legitimate finding; asymmetry-because-extraction-was-incomplete is an incomplete graph. Distinguish them in the summary, and never paper over the first to manufacture symmetry.
- What the literature settles vs. what's genuinely open
- Methodological concerns dominating the corpus (small samples, missing controls, lack of blinding, p-hacking, non-preregistered designs, publication bias)
- Author/network concentration findings
- Notable retractions/corrections in the corpus
- Most consequential surfaced contradictions
- What the graph reveals about the *quality* of the public discourse on this topic — where the consensus is well-grounded, where it's repeated authority-as-evidence, where the disagreement is real, and where one or both positions persistently shift layers/scopes to avoid central questions

This summary is the human reader's entry point into the KB. The central-questions section is also what the debate skill loads to anchor cross-examination.

## Termination

The construction phase is complete when a full pass produces no new arguments, no rating changes, and no new contradictions. Note this terminal state in `kb/quality-summary.md` so a downstream consumer (the debate skill, a human reader) knows the graph is stable.

If after 4–5 passes the graph is still churning, write that into the quality summary as well — sometimes a topic is genuinely unstable, and that is itself a finding.

## Exploratory mode

Triggered by the caller passing `--exploratory` (or equivalent). Modifies Phase 1 sourcing and Phase 2 argument extraction.

**What it adds:**

- Reach into **fringe / extreme / advocacy / dissident** sources that standard mode would skip: ideological publications, dissident researchers, retracted-but-influential papers, popular narratives that don't survive scrutiny, "absurd" positions that nonetheless surface real considerations.
- Sources go in `kb/sources/fringe/` (or appropriate non-fringe subdir if a fringe source happens to be peer-reviewed but methodologically weak).

**The discipline (this is what makes it not noise):**

For each fringe source, write the source file with **two reading sections** in the `Content` block:

1. **Generous read** — steelman. What is the strongest version of this source's case? What would have to be true for it to be right? What real considerations is it pointing at, even if its conclusions overreach? This is intellectual honesty: take the position seriously enough to articulate it well.
2. **Critical read** — traceback. Where does the evidence chain break? What primary sources does it lean on, and do those primary sources actually say what's claimed? What does the broader literature say in response? Where are the methodological holes, factual errors, motivated framings?

Then in Phase 7's quality summary: **back out to a realist view**. Acknowledge the inherent uncertainty in the topic, but explicitly note where the fringe positions did and didn't reveal real flaws in the mainstream view, where mainstream consensus is well-grounded, where contradictions remain unresolved. Never collapse into "both sides have a point" if the traceback says one side is better-grounded — but never dismiss either, since dismissal is what fan-out mode exists to avoid.

Exploratory mode pairs especially well with contradiction-surfacing — fringe positions often expose real contradictions in the mainstream that a standard literature review would smooth over.

## Entity pages (`kb/entities/`)

Optional structural layer. Use when consolidating scattered information about a recurring person, organization, key study, or named concept produces real value beyond what fits in the relevant source files' `Author network` and `Criticism` fields.

**When to create an entity page:**

- An author appears as primary or coauthor of 3+ sources, especially if their work concentrates a position's evidence base (canonical pattern: a single senior author whose group produced the majority of the favorable primary studies)
- An organization (Cochrane, USPSTF, WHO, FDA, NICE, etc.) is the source / subject of 3+ sources or arguments
- A specific study is cited / discussed by 3+ arguments — entity page consolidates its methodology, criticism, replications, and how each argument uses it
- A named concept (informed consent, harm principle, network meta-analysis, the precautionary principle) is referenced across the graph and warrants its own page rather than being re-explained in each citing argument

When you create an entity page, the hook auto-rebuilds `kb/entities/index.md`. The validator checks the schema (required frontmatter fields). **You do not write to `kb/entities/index.md` directly.**

### Entity node template

```markdown
---
id: ent-NNN
slug: <kebab-case-slug>
name: <human-readable name>
type: person | organization | study | concept | other
aliases: [list of common alternative names or spellings]
summary: <one-line summary for the index>
---

# <Name>

## Profile

[For person: role, affiliations, training, what they're known for in the broader literature.]
[For organization: what they do, how they're funded, governance.]
[For study: design, sample, year, intervention/observation, key findings as the study reports them, headline statistics.]
[For concept: definition, origin, how the concept is typically used in this topic's discourse.]

## Affiliations / coauthor network / authoring history (people)
## Funding / governance / structure (organizations)
## Methodology / replication status / criticism in subsequent literature (studies)
## Variants / related concepts / common confusions (concepts)

[Pick the section(s) that apply. Cite by source path when you make claims; use the same write-on-access discipline as for source files.]

## Appearances in this corpus

- arg-NNN — how this entity figures in the argument
- arg-MMM — ...
- kb/sources/.../paper.md — ...

## Cross-source criticism

[Bidirectional: when sources X and Y criticize this entity (or each other regarding this entity), summarize and link.]
```

### Frontmatter requirements

- `id` — `ent-NNN` (zero-padded number)
- `slug` — kebab-case stem of the filename
- `name` — human-readable
- `type` — one of `person | organization | study | concept | other`
- `summary` — one-line, used by the index

`aliases` is recommended for searchability.

## Per-source file template

```markdown
---
title: <Article/Page Title>
authors: [if available]
journal_or_source: <journal name or website>
year: <publication year>
doi: [if available]
url: <original URL accessed>
date_accessed: YYYY-MM-DD
source_type: peer-reviewed | media | institutional | reference | fringe | dissident
quality_flags: [methodology, conflict-of-interest, retracted, corrected, etc.]
key_finding: <one-line summary the index will use>
---

# <Title>

- **Authors**: ...
- **Journal/Source**: ...
- **Year**: ...
- **DOI**: ...
- **URL**: ...
- **Date accessed**: ...
- **Source type**: ...
- **Quality notes**: <conflicts of interest, methodology flags, or "none noted">
- **Citations**: <list of citations referenced in the source; copy exactly for academic citations, or construct an APA citation for links and references to title/author>
- **Cites (primary sources this leans on)**: <list of source-file paths in this KB if already imported, or external citations to chase>
- **Cited by (sources in our corpus that lean on this)**: <list of paths — populated as the corpus grows>
- **Author network**: <when the author is part of a tight cluster: coauthors, institutional ties, funding patterns, methodological critiques in the broader literature>
- **Criticism**: <independent criticism — populated when other sources in the corpus criticize this one, with back-pointers>

## Content

[Extracted content: abstract, key findings, methodology, data, conclusions —
whatever was returned by the fetch, exactly as returned. Preserve all specific
statistics, sample sizes, confidence intervals, named findings.]

[In exploratory mode, replace the single Content block with two:]

## Generous read

[Steelman: strongest version of this source's case. What would have to be true. What real considerations it points at.]

## Critical read

[Traceback: evidence-chain analysis, methodological flags, what the broader literature says in response, factual errors, motivated framings.]
```

### Source file naming

Lowercase kebab-case: `<first-author-or-org>-<year>-<brief-topic>.md`
Examples: `<author>-<year>-<study-descriptor>.md`, `<agency>-<year>-<policy-or-guideline>.md`, `<author>-<year>-<review-topic>.md`, `retraction-watch-<year>-<paper-descriptor>.md`.

### Source subdirectory choice

- Has a DOI / from a journal / preprint server → `kb/sources/peer-reviewed/`
- News, popular science, blog → `kb/sources/media/`
- Media citing a study without linking it → `kb/sources/media/missing-citation/`
- Formal policy statement from a medical/government body → `kb/sources/institutional/`
- Source later found retracted/unreliable → move to `kb/sources/retracted/`
- Source corrected post-publication → move to `kb/sources/corrected/` (preserve both versions; never use the uncorrected version to form conclusions)
- Fringe/extreme/advocacy source (exploratory mode) → `kb/sources/fringe/`
- Add additional categories as the topic warrants (e.g. `legal/`, `religious/`)

## Argument node template

```markdown
---
id: arg-NNN
slug: short-kebab-slug
position: pro-X | con-X | neutral | factual | meta
layer: empirical | methodological | ethical/metaphysical | cultural/religious | policy/regulatory | meta
scope: <free-form structured: population, geography, time, study-design, etc.>
basis_type: empirical | reasoning | metaphysical | mixed
status: robust | strong | contested | weak | refuted | baseless
asserter: <who/what put this forward — paper, advocate, derived from arg-IDs ...>
summary: <one-line statement>
---

# Argument: <Statement>

## Statement

Full claim, precisely worded.

## Evidentiary basis

[List of bases. Each entry has a type prefix:]

- **[empirical]** [source: kb/sources/path/to/file.md] specific finding excerpt
- **[reasoning]** chain: arg-XXX + arg-YYY → this argument, brief explanation
- **[metaphysical]** named principle (e.g. "informed consent"): brief articulation

## Supporting arguments

- arg-XXX (edge: supports) — short note on how
- ...

## Attacking arguments

- arg-XXX (edge: contradicts | refutes | exaggerates | confounds) — short note
- ...

## Refining / derivative arguments

- arg-XXX (edge: refines) — short note

## Depends on

- arg-XXX (edge: depends-on) — must hold for this argument to hold

## Engagement (relevance edges)

- arg-XXX (edge: addresses) — directly engages this argument's central question at its layer
- arg-XXX (edge: tangential-to) — true / well-supported but does not engage this argument's central question
- arg-XXX (edge: scope-mismatch-with) — true within own scope but applied outside it
- arg-XXX (edge: layer-shift-from) — at different layer; used as if it engaged this argument without cross-layer bridging

## Traceback notes

- How deep the recursive traceback has gone
- Open questions / dead ends / dangling evidence
- Where the chain currently breaks

## Strength assessment

- Why the current rating (`robust` | `strong` | ... | `baseless`)
- What would change the rating in either direction
- **Note:** strength is about evidentiary basis within scope. An argument can be `robust` and still be irrelevant (`tangential-to`, `scope-mismatch-with`, `layer-shift-from`) when applied outside its scope. Strength rating and relevance edges are independent dimensions.
```

## Edges file format (`kb/edges.md`)

A flat append-only log of every edge in the graph. Format:

```
arg-001  supports             arg-007  "evidence overlap on the methodology question, see arg-001 strength notes"
arg-018  contradicts          arg-042  "direct factual disagreement on transmission rates"
arg-031  refutes              arg-018  "primary-source traceback shows arg-018 misreads the cited study"
arg-009  depends-on           arg-007  ""
arg-014  exaggerates          arg-007  "overstates effect size"
arg-022  derived-from-source  kb/sources/peer-reviewed/<author>-<year>-<descriptor>.md  ""
arg-007  scope-mismatch-with  arg-099  "arg-007 scope is the screened cohort 50–69; arg-099 concerns the under-50 population"
arg-051  layer-shift-from     arg-099  "arg-051 is policy/regulatory; arg-099 is ethical/metaphysical; no cross-layer bridge"
arg-051  tangential-to        arg-099  "arg-051 true but does not address arg-099's central informed-consent question"
arg-101  addresses            arg-099  "directly engages the informed-consent question at the ethical layer"
```

Four whitespace-aligned columns: source-arg-id, edge-type, target (arg-id or source path), optional comment.

## Contradictions file format (`kb/contradictions.md`)

```markdown
# Contradictions

## C-001: <short title>

- **Type**: structural | dangling-evidence | within-position-incoherence | cross-source-disagreement | authority-evidence-drift
- **Involved arguments**: arg-XXX, arg-YYY, ...
- **Involved sources**: kb/sources/path-1.md, kb/sources/path-2.md, ...
- **Description**: <what conflicts with what, and why this is structurally a contradiction rather than just disagreement>
- **What would resolve it**: <what evidence or reasoning would settle this, if any>
- **Status**: open | resolved-by-arg-NNN | unresolvable-given-current-corpus
```

## Discipline checklist (apply throughout every phase)

- [ ] Every empirical claim has a primary-source path. No secondhand authority claims.
- [ ] Every recursive traceback either hits a primary source or hits a documented dead end (recorded as a finding).
- [ ] Authority statements (AAP, WHO, government body) are treated as evidence about positions, not as evidence about facts.
- [ ] When one author or tight network dominates a position's literature, that's mapped explicitly.
- [ ] Cross-source criticism is bidirectional: if X criticizes Y, both files reflect it.
- [ ] Refuted, weak, baseless arguments are kept in the graph, not deleted.
- [ ] Every argument has `layer:` and `scope:` populated. These are mandatory.
- [ ] Relevance/engagement edges (`addresses`, `tangential-to`, `scope-mismatch-with`, `layer-shift-from`) are drawn deliberately, not just logical-relationship edges. An argument that "supports" position X by being true-but-tangential to the central question gets both the `supports` edge and the `tangential-to` edge.
- [ ] Quality summary names the topic's central questions explicitly and notes which arg-IDs engage each via `addresses` edges.
- [ ] Quality summary names engagement asymmetries between positions (which side engages central questions, which side orbits them).
- [ ] In exploratory mode, every fringe source has both a generous and critical read; the realist landing happens in the quality summary.
- [ ] Iterative passes continue until the graph is stable; instability after many passes is itself documented.
