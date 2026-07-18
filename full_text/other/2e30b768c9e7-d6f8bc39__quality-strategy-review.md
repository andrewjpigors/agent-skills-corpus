---
name: quality-strategy-review
description: Audit a quality strategy document. Applies seven indicators of a good strategy plus mechanical oracle checks, and asks "where is this strong, where is this weak?". Use after /quality-strategy completes, or to audit an existing quality/strategy.md cold.
---

# Quality Strategy Review

This skill audits a quality strategy document. It is the source of truth for *"is this strategy any good?"*. Run it as the final step of `/quality-strategy`, or on its own against any existing `quality/strategy.md`.

The skill uses an **expansion-and-collapse** pattern:

- **Expansion.** Three subagents run in parallel, each with its own review lens. Their briefs tell them to be aggressive — flag freely, dig for specifics, raise anything that feels off — because the main agent will filter their output. In review work, missing a real issue is worse than raising a false alarm.
- **Collapse.** The main agent reads all three outputs, drops false or trivial findings, looks for findings that share a root cause, separates blockers from flags, and writes one consolidated report.

This is brainstorm-then-curate, not one-pass judgement. One-pass review tends to miss things or drown the reader in trivia; two stages avoid both.

## Resolving file paths — do this first

This skill is part of the `quality-strategy` plugin. Before anything else, resolve two absolute paths and use them throughout:

- **PLUGIN_ROOT** — the plugin's install directory: `${CLAUDE_PLUGIN_ROOT}` (Claude Code expands this to an absolute path when it loads this file; read it off and note it down). The grounding and framework files this skill reads live under it.
- **PROJECT_DIR** — the absolute path of the project whose strategy you're reviewing (normally the current working directory; confirm with the user if it's ambiguous). The strategy docs normally live under `$PROJECT_DIR/quality/` — but `/quality-strategy` asks at session start where the strategy should be saved, so they may live elsewhere. If `$PROJECT_DIR/quality/` is absent, get the docs home instead of assuming: from the orchestrator's brief when this skill was dispatched, else by asking the user; if the path you're given ends in `/quality`, its parent is the home. From then on treat `$PROJECT_DIR` as that docs home wherever a path below says `$PROJECT_DIR/quality/...` — one substitution, made once, before you act on any path.

File references below use the `$PLUGIN_ROOT` and `$PROJECT_DIR` placeholders. **Substitute the resolved absolute paths before you act on them** — both when you Read a file yourself and when you put a path into a subagent brief. The Read tool does not expand variables, and it resolves relative paths against the current working directory — not this skill's directory. A dispatched subagent starts with none of your context. So an unexpanded placeholder or a bare relative path will fail. Always pass full absolute paths.

## Before you start

Read `$PLUGIN_ROOT/PHILOSOPHY.md`. The disciplines and the framework grounding are the foundation of the review.

## What you need

The strategy doc to review at `quality/strategy.md`. If `quality/pre-read.md` exists, also read its summary and discrepancies sections — pre-read findings the strategy didn't address are themselves review findings.

If `quality/archive/` holds prior versions of the strategy (files whose names start with `strategy-`), the newest may be the instrument for a **revision review**: subagent A diffs it against the current doc (check 22) rather than trusting the revision's own account of what changed. An archive alone does not make the doc a revision — fresh-replace and new-release runs archive too; check 22 detects which this is.

If `quality/strategy.md` doesn't exist, tell the user: *"There's no strategy doc to review. Run `/quality-strategy` first."*

## The work, in order

### 1. Read the strategy

Read `quality/strategy.md` end-to-end. Note which parts are present, which are missing, which look thin.

If `quality/pre-read.md` exists, read its summary and discrepancies sections.

### 2. Contextual-fit gate (Pass 0)

**Run this before the indicators, and carry its verdict into the collapse step.** If you hold a pre-implementation or deliberately thin strategy to the full production-grade scale, you get the wrong answer: deliberate scope control reads as weakness, and quality strategy turns into ceremony. The framework's spirit is *contextual* quality. So first work out what this strategy is *for*, then judge whether it's fit for that job.

**Read the `## Strategy job` paragraph** at the top of the doc. If it's present, take its job classification. If it's **missing**, that is itself a finding — the producer skill should have written it. Infer the job from the content (no code yet + mostly-Unknown actuals ⇒ pre-implementation; "one-shot" / "agentic implementation attempt" language ⇒ agentic one-shot; thin slice with many deliberate Nones ⇒ lightweight slice; otherwise durable production) and flag the missing paragraph.

Classify on these axes:

- **Lifecycle stage** — pre-implementation / implementation / alpha / beta / production / maintenance.
- **Intended use** — one-shot brief / release alignment / test planning / stakeholder alignment / operational dashboard.
- **Evidence available** — no code yet / runnable prototype / production telemetry / user feedback.
- **Expected weight** — lightweight decision aid / full durable strategy.
- **Allowed to ignore** — what this strategy explicitly says is out of scope.

This produces one of four **jobs**: durable production / pre-implementation / agentic one-shot / lightweight slice.

**What the gate changes — and what it doesn't.** The seven indicators and the oracle checks apply to *every* job; the gate does **not** switch indicators on or off. What it adapts is **severity** — where the line sits between a blocker and a deferral. Specifically:

- **Pre-implementation** — unknown actuals (the "where are we now" side of the risk map) are *normal*, not a weakness. Don't score situational awareness harshly for unknown actuals. The question becomes: *does the strategy name what evidence the first implementation must produce?* A missing production-observability section is a deliberate deferral, not a blocker.
- **Agentic one-shot** — additionally check the strategy captures: one-shot success / partial-success / failure criteria; final-report evidence requirements (spec gaps, judgment calls, commands run, environment issues, human steering); predictable agent failure modes (scope substitution, fake tests, overbuilding integrations, skipping hard e2e, silent redesign) with decision rules; and explicit Nones to keep the implementation thin. *Absence of these is a blocker for this job*; absence of production machinery is not.
- **Lightweight slice** — missing production observability, mature process, broad compatibility, and long-term reporting are **not** blockers *if* the strategy explicitly makes them non-goals. If they're silently absent (not declared Nones), that's a flag, not a blocker.
- **Durable production** — full machinery enforced; the standard severity rules below apply unchanged.

**The blocker rule the collapse step uses:** *a missing section is a blocker only if its absence prevents the strategy from doing its stated job in this context. If the missing section belongs to a later lifecycle stage, classify it as a deliberate deferral or a suggested future revision, not a current blocker.* Every review finding goes in one of three buckets: **current blockers**, **useful pre-implementation/now refinements**, and **later-lifecycle deferrals**.

Record the job classification and the resulting severity lens; pass them into the subagent briefs (so subagents judge against the right job) and apply them in the collapse step.

### 3. Dispatch three review subagents in parallel

Use the `Agent` tool with three calls in a single message.

#### Subagent A — Mechanical oracle checks

> You are subagent A, running mechanical oracle checks against a quality strategy document. **You are a backstop**, not the primary line of defence — the writing process should already have enforced these checks via per-sub-step DONE checklists. Your job is to verify nothing slipped through.
>
> **This strategy's job is: `<JOB — durable production / pre-implementation / agentic one-shot / lightweight slice, from Pass 0>`.** Mechanical checks still run regardless of job, but when you flag a missing-section check (non-goals, risk-map coverage, rating justification), note whether the gap looks like a *deliberate deferral* appropriate to this job rather than a true failure — the main agent decides severity per the contextual-fit gate.
>
> Be aggressive about flagging — false negatives (missing real issues) are much worse than false positives (the main agent will filter what you flag).
>
> **Meta-flag.** A failing oracle check is also evidence that the relevant sub-step's DONE checklist was never really enforced — the agent ticked a box without doing the check. So when you flag a failure, add to your explanation: *"this should have been caught in sub-step X.Y's DONE checklist, but wasn't."* The user wants to know that.
>
> First, read `$PLUGIN_ROOT/PHILOSOPHY.md` and `$PLUGIN_ROOT/skills/quality-strategy/SKILL.md` to ground yourself.
>
> Then read `$PROJECT_DIR/quality/strategy.md`.
>
> Run the following oracle checks. For each, classify as **PASS / FLAG / FAIL** and write one line of explanation. For FLAGs and FAILs, also include a one-line "what to fix" suggestion plus the meta-note about which sub-step's DONE should have caught this.
>
> 1. **Non-goals not empty.** Part 4 has at least 3 non-goals, each with a reason.
> 1a. **Non-goals are quality bars, not feature exclusions (the kind bar).** Each Part 4 entry names a quality dimension deliberately not being reached for this release's in-scope work — not a capability or feature the roadmap already defers. FAIL a Part 4 whose entries are *entirely* feature exclusions or unmodified roadmap deferrals with no quality-bar decision among them ("no Windows support" restated with nothing about what quality bar that implies is not a quality non-goal — that's the roadmap's job, and restating it doesn't count toward the minimum). A deferral-derived entry is fine when it's re-expressed as the bar it implies for in-scope work (e.g. "scalability beyond small files" citing a deferred bulk-import feature as its reason) — the check is on the entry's *kind* (a bar, not a feature), not on whether a deferral is mentioned in the reason.
> 1b. **Non-goals reasoned forward, not from absence (no status-quo bias).** Each Part 4 non-goal's reason names an *intentional tradeoff traced to a stated goal*, not the mere fact that the capability isn't built. FLAG any non-goal whose stated reason is status-quo — "not built", "no code for it", "doesn't currently support" — with no goal-traced tradeoff behind it: an absence is a fact about the repo, never on its own a decision the user made. FAIL a non-goal that a **named event in Part 2** (a launch, a campaign, an onboarding spike) would plausibly pull back into scope — e.g. "no custom email / SMTP" recorded as a non-goal alongside a Part-2 Twitter launch that implies a signup spike: that is a buried gap wearing a non-goal's label. (This is the doc-visible half of sub-step 4.1's two disciplines; the confirmation half — was each cut named back and confirmed? — isn't visible on disk, so subagent C carries it as a consistency lens.)
> 2. **No percentages in confidence ratings.** Grep for "%" in confidence contexts (Parts 5 and 6). Confidences should be H/M/L only.
> 3. **Ratings grounded in the anchor.** Ratings use the H/M/None model. Every H rating's rationale names a stakeholder **Dealbreaker** bar from Part 3; every M rating's rationale names a non-Dealbreaker bar (Good Enough or Delight). A rating that doesn't cite the bar the anchor rests on is a FAIL.
> 4. **None ratings reasoned.** Every None rating in Part 5 has explicit reasoning, not blank.
> 4a. **Floors and default-ins.** Read `$PROJECT_DIR/quality/pre-read.md`'s floor-predicate section (and any predicates confirmed in the interview). For every floor whose predicate holds — handles secrets, holds PII, holds entrusted data a user would want back, ships to others' machines, licensing/data-protection law — the matching floor dimension must be present in Part 5 and **not rated None** (FAIL if a holding predicate has no dimension, or its dimension is None: a floor can't be voted off). For each default-in — **security always**, **data integrity / loss where the system holds user data**, **unbounded spend where the system can spend money** — Part 5 must either carry the dimension or the doc must carry an explicit, recorded eyes-open **accepted-risk** for it; a default-in that is *silently* absent (no dimension and no accepted-risk note) is a FAIL. The failure this catches: a sweep that produced no security dimension on a project whose headline risk was forgeable client-writable data. (If `pre-read.md` is absent or its floor-predicate section is missing, FLAG and judge the floors from the strategy body's own description of what the system holds and ships.)
> 5. **Three lenses populated.** Every stakeholder in Part 3 has Delight, Good Enough, and Dealbreaker captured for the release the strategy covers (the header's `*Release:*` line).
> 6. **Risk map covers all H/M dimension rows, scope preserved.** Every dimension **row** rated H or M in Part 5 — keyed by dimension **and scope**, per Part 5's Scope column — has its own row in Part 6. FAIL if two same-named, differently-scoped Part 5 rows collapse into one Part 6 row (a dev-tool's "usability" for its own UI and "usability" for its API are two rows, two required levels, two actuals — never one shared row because the name matches). Where this doc's negotiated structure (2.1) covers more than one release, also FAIL a Part 6 row with no explicit release tag when more than one release's rows appear near each other — a bare "relevant release" is not sufficient.
> 6a. **Document structure recorded, and every later Part honours it (multi-release docs only).** If the doc's content shows more than one release with real depth beyond purpose-level (check Part 2, and whether Parts 3–7 carry material for more than one release), Part 2 must carry a **"Document structure:"** field naming the negotiated choice (per-release doc + bank / light sections / two releases in parallel / fully separate documents) — FAIL if that content exists but the field is missing or blank; a doc structure can't be inferred reliably after the fact and its absence means a cold reader (or a later session) has no way to know how the doc was meant to be organised. Then check the chosen structure was actually honoured: under **"two releases in parallel,"** Parts 3 through 7 (and Part 6 per check 6) show clearly separated per-release sections/tables/headers for both releases — FAIL a blended pass that mixes both releases' content with no separation. Under every other structure, only one release should carry real depth in Parts 3–7 of *this* document — FAIL any Part 3–7 content that is clearly about a different release and was folded into this release's tables/lists rather than routed to its bank entry, light section, or separate document (the tell: a stakeholder, non-goal, dimension, risk-map row, or action whose content plainly describes a different release's context, sitting unmarked among this release's rows). This is the doc-visible half of the routing discipline each sub-step's text now carries — SKILL.md → "Scope of this skill".
> 7. **Risk map confidence on both sides.** Every Part 6 row has confidence-in-required and confidence-in-actual (or "—" for Unknown).
> 8. **Confidence vocabulary correct.** All confidences are H/M/L (or "—" for Unknown actuals).
> 9. **Unknowns have resolution notes.** Every Unknown actual in Part 6 has a "to resolve" note (test / ask / review / instrument / build).
> 10. **High justification — not distribution.** Ratings use the H/M/None model (no L). Do **not** flag a High-dominated distribution by count alone: by rating time the low-stakes material was already deliberately cut (dropped at the inventory, excluded as a non-goal, rated None), so Highs dominating what remains is the expected shape, and doubting the count fires on exactly the strategies that pruned correctly. Flag instead: any High whose rationale doesn't cite a named stakeholder Dealbreaker bar (the pattern-level companion to check 3's per-rating rule — challenge those Highs individually); an H/M split where the Medium anchor appears never to have been applied (every bar read as a Dealbreaker); zero None entries where some are expected. When every High is justified, report that plainly — *"every High cites a real dealbreaker; this is a genuinely high-stakes surface"* is a PASS verdict, not a hedge. Also flag prose anywhere in the doc that uses "High" to mean *in trouble* or *at risk* rather than *important*: importance (the Part 5 rating) and current state (the Part 6 actual and gap) are orthogonal axes — a High at bar is a success story — and conflating them misreads the whole map. (Aligned with sub-step 5.5's Check 1.)
> 10a. **Adequacy vocabulary and feature-as-dimension (Part 5).** Part 5 answers only "how much does this matter" — never "how good is it currently" (that's Part 6). FLAG any dimension name or rating rationale in Part 5 carrying state-verdict language, either direction — pessimistic: "problem", "broken", "inconsistent", "lacking", "missing", "bad", "weak", "a concern"; reassuring: "good", "solid", "fine", "probably fine", "well covered", "no worries" — in place of an importance ground (a rationale may *reference* an observation that prompted the dimension, but must ground importance in a stakeholder bar, not restate the observation as the reason). FLAG any Dimension cell that names a feature or component ("remote operability", "the export flow", "onboarding") rather than a quality axis (reliability, usability, performance...) — the feature belongs in the scope column, not the Dimension cell. If Part 5 carries a "Deficiency observations parked for actual-state review" table, cross-check it against the inventory: an entry there with no corresponding dimension row, or a dimension row that silently absorbed the observation as its rationale instead of parking it, is a FAIL either way. (Aligned with sub-step 5.5's Check 7.)
> 11. **Actions classified.** Every Part 7 action is classified as testing / stakeholder / fixing / process-change. A process-change action (changes the team, org, or workflow itself, not the product) is not required to name a risk-map row it closes — that absence is the discriminator for this type, not a defect; don't FLAG a process-change action for lacking a gap citation the way you would a fixing action. If Part 7 is a **recorded deferral** — a short section explicitly deferring the plan of work to the follow-on lanes and naming where each slice will live (`/test-strategy`, `/evaluation-strategy`, `/process-strategy`, builds via `/tooling-strategy`) — checks 11 and 12 PASS automatically. A Part 7 that is missing, empty, or vague *without* that explicit deferral note is a FAIL as before.
> 12. **Plan has phases.** Plan of work in Part 7 has distinct phases; Phase 0 (blockers) is either populated or explicitly empty with reasoning. (Recorded deferral: see check 11.)
> 13. **Pre-read sources cited.** Sub-step output sections cite pre-read sources where the agent did pre-read work.
> 14. **Stakeholder coverage.** Every Part 3 stakeholder has at least one H or M dimension whose rationale connects to their bars.
> 15. **Sub-group heuristic applied.** Each Part 3 stakeholder either has sub-groups, or a "considered, no meaningful split" note.
> 16. **Old/new-world evidence.** Where trap dimensions (readability, maintainability, documentation, diagnosability, observability, ramp-up-ability) are present in the inventory — either by their original name or as sub-dimensions from unpacking — evidence the audience question was considered (split into human/agent versions, or rationale notes the choice).
> 17. **Unpack evidence.** Where commonly-composite dimensions (performance, reliability, security, maintainability, usability, observability) are present, evidence of unpacking (sub-dimensions present) or a note that they were considered atomic for this project.
> 18. **Strategy job stated.** There is a `## Strategy job` paragraph near the top naming the strategy's job (durable production / pre-implementation / agentic one-shot / lightweight slice, or the user's framing), what evidence it must produce, and what's deliberately out of scope. FAIL if absent **and** the job cannot be inferred from the content (a strategy produced by this skill must state it). FLAG if absent but the job is clearly inferable (e.g. an older or external doc being audited cold) — the fix is to add the paragraph, not to block. Also expect the header to name the release the strategy covers (the `*Release:*` line, or the release named in Part headings) — the strategy is per-release; FLAG if missing, and treat the Step-1 placeholder left unstamped ("to be named at Step 2") as missing (older docs predate the release stamp; the fix is to add or fill the line).
> 19. **None ratings have a contextual reason.** Every dimension rated None carries a reason tied to the strategy's job/context (e.g. "out of scope for this lightweight slice"), not a blank. (Overlaps check 4; here specifically the *contextual* justification.)
> 20. **Scratch-file audit.** Every sealed-context subagent dispatch (a subagent run in a fresh context, isolated from the main conversation) that the strategy's *structure* says was REQUIRED has its scratch file under `$PROJECT_DIR/quality/.scratch/`. **Audit required dispatches, not merely claimed ones.** Work out which dispatches *should* have run from which Parts and step boundaries the doc contains — not from what the doc says it ran. A dispatch that was silently skipped leaves no mention behind, so it must not escape detection just because the doc never names it. (A step-boundary `/contradiction-check` is the classic loophole: skip it and there's no claim in the doc *and* no scratch file, so an audit that only checks "what the strategy claims it ran" never flags it.)
>
> Derive the REQUIRED set from doc structure. (This list mirrors the dispatch set in `/quality-strategy` SKILL.md "Sealed-context dispatch and scratch files" — keep the two in sync when dispatches are added or renamed.)
>
> - **Pre-read** — if `$PROJECT_DIR/quality/pre-read.md` exists, expect `0-pre-read-*.md` (e.g. `0-pre-read-docs.md`, `0-pre-read-code.md`, `0-pre-read-design.md`). A **multi-repo scope** — read the repo list (with each repo's scratch slug) from `quality/.scratch/session-config.md`; that note is the independent record, so only if it carries no scope may you fall back to inferring the list from the digest's `## Repo:` sections, and then FLAG that the scope could not be independently verified (a silently-skipped repo leaves no `## Repo:` section, so digest-derived lists can't catch it) — expects one `0-pre-read-<repo>-{docs,code,design}.md` triple **per in-scope repo**; an in-scope repo with no triple is a silently-skipped dispatch, a FAIL.
> - **Dimension scout** — if Part 5 is present, expect `5.1-dimension-scout.md`.
> - **Dimension rating** — if Part 5 dimension ratings are present, expect `5.4-dimension-rating.md`. A missing `5.4-dimension-rating.md` when Part 5 ratings exist is a **FAIL** — the rating dispatch was silently skipped or fabricated.
> - **Design deep-dive (conditional)** — if Part 6's actual-state assessment is present, expect `6.2-design-deep-dive.md` *or* an explicit skip note in the doc saying no thin-evidence dimension was design-shaped; neither present is a silently-skipped dispatch.
> - **Step-boundary contradiction checks** — for EACH completed step boundary the doc has reached, expect a `<boundary>-contradiction-check.md`. The boundaries are 1.5, 2.1, 3.2, 4.1, 5.5, 6.3, 7.3 — i.e. for each Part present in the doc, the corresponding boundary check should have run (Part 1 → 1.5, Part 2 → 2.1, Part 3 → 3.2, Part 4 → 4.1, Part 5 → 5.5, Part 6 → 6.3, Part 7 → 7.3). A missing boundary contradiction-check scratch file for a Part that IS present is a **FAIL** — a required dispatch was silently skipped — regardless of whether the strategy claims it.
> - **Distillation** — if the Operational TL;DR / triage rubric is present at the top of the doc, expect `7.3-operational-distillation.md`.
> - **Revision look-forward passes (revision runs only)** — if the doc is a revision (it carries a `## Since the last revision` section, or check 22's diff detection says it is one), expect `revision-defect-recon.md` and `revision-context-scan.md` — the deliberately-blind look-forward dispatches. Missing when the revision re-asserted the risk map's actuals is a FAIL; a skip note recorded in `## Since the last revision` (the edit made no claim about the project's current state, or it was a named-row re-assessment after a tooling build landed) stands in. Also expect `revision-contradiction-check.md` — the whole-doc contradiction check every revision or correction close runs; missing is a FAIL (no skip note applies). Check freshness too: a look-forward scratch file older than the newest archived prior version belongs to an earlier revision, not this one — FLAG.
>
> A required dispatch (derived as above) with **no** scratch file is a FAIL — hard evidence the dispatch was fabricated or silently skipped rather than run. A scratch file that's empty or a stub is a FLAG (audit theatre). Also still FAIL any dispatch the strategy *explicitly claims* it ran that's missing its file, even if structure wouldn't otherwise have required it. List which scratch files are present, missing, or stub.
>
> **Verify on disk — never green-check from the doc's narration.** Actually list `$PROJECT_DIR/quality/.scratch/` and read the files to establish what is present; mark a required file PRESENT only if you have *seen it in that directory*. Do not report "all required dispatch files present" because the strategy *says* a dispatch ran — a file the doc claims but that is absent from the directory is a FAIL, not a pass. **If you cannot access the filesystem at all** (no Read/list access in this environment), report this check **INCONCLUSIVE** and say so plainly — never PASS it on faith. Note the distinction: *no filesystem access* → INCONCLUSIVE; *filesystem access but the `.scratch/` directory is absent or empty when required dispatches should have written to it* → **FAIL** (those required files are genuinely missing), not INCONCLUSIVE. Tell the user an INCONCLUSIVE result as "the scratch-file audit could not be run" — never present it as a clean pass. (A green check must be backed by a real directory listing: reporting "all required dispatch files present" when none are on disk is the failure this guards against.)
>
> **No-repo / pre-implementation sessions still write scratch files.** Running with no codebase to scan is normal and first-class (see `/quality-strategy` SKILL.md → "Running without a repo is first-class"), but the dispatches that ran still write their scratch files — the pre-read writes its scratch documenting the LIMITED / interview-derived pre-read rather than skipping the file because there was nothing to scan. So "there was no repo" does **not** excuse a missing required scratch file: the file should exist, carrying the honest-degradation note instead of scan findings. Judge presence exactly the same way; only the file's *contents* differ.
> 21. **No process-note leak.** The strategy doc contains no first-person-about-the-skill commentary (e.g. "this sub-step was awkward", "the skill asked me to…"). FLAG any that leaked in. Also FLAG, with the same severity, the further leak patterns the strategy body must be clean of: **(i) dispatch / scratch / sealed-pass narration** — e.g. "[ran <dispatch> inline]", "Subagent dispatched: …", "scratch would be `quality/.scratch/…`", **and the sealed-context merge vocabulary** "sealed pass landed M", "surfaced to the user", "merged to H because…", "the sealed dispatch returned…" (keep the *decision* — the rating and its reason — but the *mechanism* that produced it must be gone); **(ii) sub-step / turn lineage references** — both *turn* refs ("corrected, turn-23", "the turn-22 binding test") and *sub-step-number* refs ("split out at 5.2", "Action 6 from 7.1", "folded in from 7.1", "(Pulled out of non-goals at turn 16)") — the final doc has no "turn 23" and no "7.1"; cross-references to the doc's own *Parts* ("see Part 6") are fine, references to the *process* that built it are not; **(iii) inferred-as-scanned pre-read lines** — facts the body presents as if a scan was run when no code was actually read (e.g. "no X detected" with no corresponding scan); **(iv) provenance / source-column vocabulary** — in the dimension inventory's source/evidence column and in rating rationales, the *name of the internal pass* that surfaced or rated a dimension: "Subagent pass", "reference-list pass", "subagent C('s) …", "the per-stakeholder pass returned … merged to H", "the oracle-adequacy pass as direct inputs", a bare "`dimension-scout`" cited as a source (keep the real grounding — the stakeholder bar, the pre-read observation, the named file — drop the pass name); **(v) scratch-file path citations** — a `quality/.scratch/<…>.md` path listed as a "source consulted" or as what a rating "rests on" (cite the real underlying source or drop it; `.scratch/` is working state the reader does not have). These are process / provenance / lineage artifacts: they belong in scratch or `.skill-feedback.md`, never in `quality/strategy.md`. Stripping **all** of them is a required clean-up — a strategy peppered with turn-refs, sub-step-number refs, sealed-pass narration, provenance-column pass-names, or `.scratch/` citations should FLAG even when each instance is individually minor, and the producer must **remove** what this check surfaces before the strategy is declared done (this check is a strip, not just a note). Run this scan as an actual pass over the **whole** doc — **including any content inherited from a prior version in a revision or resumption run, which the per-Part boundary scans never saw** — before declaring the strategy done; do not assume it is clean. Three exemptions: (1) a `## Since the last revision` section is content, not machinery — its what-happened verdicts and newly-found items compare the project against its prior strategy, which the reader wants; leave it. (2) A **pointer to the release bank or the ideas ledger** (`quality/releases/<slug>.md`, `quality/ideas.md`) is content — both are durable, reader-visible files, unlike `.scratch/`; leave the pointer (capture *narration* — "banked for X", "noted in the ideas ledger" — still strips). (3) The header **version stamp** (`*Generated by the quality-strategy skill — quality-strategy-skills (tollens-ai) v<version> · …*`) is deliberate provenance attribution, like a document footer — it is what lets a bug report trace back to the skill version that generated the doc. Leave it intact; do not strip it as a process-note leak. (If `<version>` is still the literal placeholder rather than a resolved number, that *is* a flag — the stamp was written but never filled in.)
> 22. **Revision integrity (revised strategies only).** First detect whether this doc is a *revision* of an archived prior version. The signal is the doc's own `## Since the last revision` section — or, if that section is missing, a diff against the newest prior version under `$PROJECT_DIR/quality/archive/` (files whose names start with `strategy-`) showing substantial carried-over content: same release, Parts inherited largely unchanged. An archive alone is NOT the signal — fresh-replace and new-release runs archive too, and a genuinely fresh doc (new release, rewritten throughout) makes this check PASS (n/a). A doc that IS a revision by diff but has no `## Since the last revision` section is itself a FAIL — a silent revision. If you cannot access the filesystem to read `quality/archive/`, report INCONCLUSIVE — never PASS on faith. For a detected revision — and this is the rationale for everything below: *a revision anchored on last time verifies the past instead of assessing the present; the gaps have moved* — **diff, don't trust**: the diff is your instrument; the revision's own account of what changed is a claim to verify against it, not a source. Check two things against the diff. **(a) Look-back integrity** — every H/M risk-map row, open question, and planned action in the *prior* version, within the revision's recorded scope (a scoped revision names its scope in `## Since the last revision` — for a correction, that means the recorded **union**, not just the touched sections; an unscoped revision is held to the whole doc), carries a what-happened verdict, and every "fixed" / "resolved" / "closed" claim cites evidence (a commit, a test, a measurement) or is honestly marked *believed fixed* at a stated confidence. An unevidenced "fixed" is a FAIL — the same failure as a high-confidence actual whose oracle can't support it; closure claims need grounding exactly as ratings do (check 3's rule, applied to the past tense). **(b) Look-forward presence** — the revision contains genuinely NEW findings (dimensions, risks, defects, open questions) that are not derivable from the prior doc. A revision whose diff shows only closures of prior items is the **anchoring signature** — treat "zero new problems found" with exactly the same suspicion as "everything at bar": FAIL on a closures-only diff; FLAG when new findings exist but are thin relative to how much the project changed. A recorded look-forward skip note (the edit made no claim about the project's current state, or it was a named-row re-assessment after a tooling build landed) stands in — n/a, not a FAIL. Also FLAG if the doc carries a `## Since the last revision` section but `quality/archive/` holds no prior version — the producer skills archive before revising, so a missing archive means history was silently rewritten.
> 23. **Effective Comms backstop.** The producing skill runs an `/effective-comms` pass before finalizing; this is the review's backstop for the reader-facing failure modes that check 21's process-note scan does *not* cover. Scan the whole doc for: **(i) numbered references without meaning** — an oracle / dimension / strategy-item / Part referenced only by number or ID where the reader cannot tell what it is about ("Oracle 2 fails here" with no plain-English name); **(ii) coordinate-before-name** — a file path, ticket ID, or internal label leading where a human-readable name should ("`src/auth/x.ts` is the risk" with no statement of *what* it is); **(iii) retained rejected ideas** — an option the strategy *rejected* still carried in the body with a rejection note, when this doc is the current accepted strategy rather than an audit/decision-history artifact. FLAG any found, with a one-line "name it / lead with the name / cut it." (Check 21 already covers hidden-scratch-context and process-history leakage; this check adds the reader-legibility modes ECS guards that the leak scan misses. Severity: FLAG, matching the leak check — the producer should have caught these in its Effective Comms pass.)
> 24. **Correction-scope integrity (correction-mode revisions only).** Applies when `## Since the last revision` records a **correction** (a triage verdict of genuine-correction or drift-handled-as-correction, with touched section(s) and a computed downstream union — the producer records these per SKILL.md → "Correction path (b)"). Diff the newest archive against the current doc and check three things. **(a) The diff stays inside the union**: every changed Part/section must lie inside the recorded union — plus the always-refreshed items (header stamp, Operational TL;DR/triage rubric, `## Since the last revision` itself), which don't count against it. Content changes outside the union are a **FAIL** — the revision wandered; untouched sections are preserved by construction, and an out-of-union edit is exactly the silent re-opening the correction protocol forbids. **(b) The union is the true closure**: recompute the downstream tree of the recorded touched section(s) from `$PLUGIN_ROOT/skills/quality-strategy/SECTION-DEPENDENCIES.md` — an under-computed union (a dependent section missing from the recorded scope) is a **FAIL** even if nothing outside was edited, because the missing dependents were never examined against the correction. **(c) Every union section carries an outcome** in `## Since the last revision`: *changed* (with what) or *examined-unchanged* (user-confirmed keep) — a union member with no recorded outcome is a FLAG (the walk may have skipped it). A revision with no recorded correction scope is judged by check 22 alone (n/a here); a doc whose `## Since the last revision` claims a correction but records no union is itself a FLAG — the protocol wasn't followed, so this check has nothing to hold the diff to.
>
> Output format: a markdown list of checks 1–24 with PASS/FLAG/FAIL classification and explanation. For FLAGs and FAILs, include a one-line "what to fix."

#### Subagent B — Qualitative indicator assessment

> You are subagent B, applying the seven indicators of a good quality strategy with creative depth. Your output will be filtered by the main agent — don't be polite. If a section feels weak, say why. If something is off but you can't fully articulate why, say that too. The main agent has a second pass to filter out anything spurious.
>
> **This strategy's job is: `<JOB — durable production / pre-implementation / agentic one-shot / lightweight slice, from Pass 0>`.** Apply all seven indicators regardless of job — but judge against the job, not against a production ideal. For a pre-implementation or lightweight-slice strategy, unknown actuals and deliberate Nones are *correct scope control*, not weaknesses; mark the indicator on whether the strategy does *its* job well. Do not score "situational awareness" or "instrumentation" harshly just because actuals are unknown when there is no implementation yet.
>
> First, read `$PLUGIN_ROOT/PHILOSOPHY.md` and `$PLUGIN_ROOT/skills/quality-strategy/SKILL.md` to ground yourself.
>
> Then read `$PROJECT_DIR/quality/strategy.md` end-to-end.
>
> Apply the seven indicators of a good quality strategy. For each, decide **STRONG / MEDIUM / WEAK** and write 2–4 sentences explaining your judgement. Quote specific sentences from the strategy that show the strength or weakness — concrete is better than abstract.
>
> 1. **Org-wide clarity.** Could a new engineer or agent read this and quickly understand what's going on, what matters, what success looks like? Or is it dense, jargon-heavy, missing the through-line?
> 2. **Instrumentation from the start.** Are quality proxies chosen, and is there evidence they'll be measurable from day one rather than retrofitted? Or has measurement been deferred?
> 3. **Legible work plan.** Is the plan of work ordered by *why*, not just *what*? Can you tell from reading it why each item is sequenced where it is? Are dependencies visible? (If Part 7 is a recorded deferral to the follow-on skills, judge this indicator on the deferral instead: does it name where each slice of the work will live, and do the risk map's hottest items make the first investigation obvious? Don't dock the strategy for the absence of a sketch it deliberately deferred.)
> 4. **Precision over comfort.** Is the strategy specific enough to be wrong-able? Vague claims that nobody could disagree with are useless. A sharp claim that turns out to be wrong is valuable. Where is the strategy hiding behind generality?
> 5. **Decision support at the edges.** Could an engineer or agent encountering a new finding (a bug, a feature request, a complaint, an unexpected result) quickly map it to this strategy and triage it without escalation? Or would the strategy fail the "is this in scope?" question?
> 6. **Quick re-orientation.** Could someone lost in the weeds re-read this and rapidly re-anchor to what matters and for whom? Or does it require reading end-to-end every time?
> 7. **Explicit non-goals.** Is it clear what's deliberately not being done? Is the reasoning visible? Are the non-goals real (concrete things excluded) or theatrical (vague avoidances)?
>
> For each WEAK indicator, suggest one or two concrete improvements.
>
> Output format: a structured assessment, one section per indicator, with STRONG/MEDIUM/WEAK classification, explanation with quoted evidence, and improvement suggestions for any WEAK ones.

#### Subagent C — Cross-cutting consistency checks

> You are subagent C, checking the genuinely **end-to-end** consistency of a quality strategy — the things that can only be checked once the whole document exists. The per-section consistency checks (each H rating grounded; non-goals aligned with ratings; risk map covers H/M dimensions; risk map → action list) are enforced at write time by per-sub-step DONE checklists; you don't need to re-run those.
>
> **This strategy's job is: `<JOB — durable production / pre-implementation / agentic one-shot / lightweight slice, from Pass 0>`.** Consistency is judged against the job. In particular, check that the `## Strategy job` paragraph is *consistent with the body*: a stated out-of-scope item (e.g. "production observability is a non-goal") that a later Part treats as an in-scope Dealbreaker is a contradiction worth surfacing. Don't flag unknown actuals or deliberate Nones as inconsistencies when the job makes them appropriate.
>
> Your output will be filtered by the main agent. Be aggressive about flagging misalignments — false negatives are worse than false positives.
>
> First, read `$PLUGIN_ROOT/PHILOSOPHY.md` and `$PLUGIN_ROOT/skills/quality-strategy/SKILL.md` to ground yourself.
>
> Then read `$PROJECT_DIR/quality/strategy.md` and (if it exists) `$PROJECT_DIR/quality/pre-read.md`.
>
> Check the following end-to-end consistencies:
>
> - **Pre-read discrepancies addressed.** If `pre-read.md` flagged docs/code discrepancies or load-bearing design observations, has the strategy addressed them — either by acknowledging them in some part of the doc, or by including them in the action list? An unaddressed pre-read finding is a gap worth surfacing.
> - **Release purpose ↔ rating distribution.** Does the rating distribution actually reflect what the release is for? An alpha release for "test the core technique" should have very different ratings from a GA release. If the release purpose says "test the technique" but accessibility is rated High, something is off.
> - **Internal contradictions across the doc.** Anywhere in the strategy where two claims appear to contradict each other, or where one part assumes something another part denies. Examples: a stakeholder dealbreaker in Part 3 that contradicts a non-goal in Part 4; a workflow described in Part 1 that the plan of work in Part 7 implicitly assumes is different.
> - **Non-goals vs named events (forward-reasoning check).** Walk each Part 4 non-goal against the named events and stated goals in Parts 1–3. A non-goal is a decision about what the user doesn't care about — so a cut that a stated event would actually demand is status-quo bias dressed as scope control. Flag any non-goal that a launch, campaign, or growth event elsewhere in the doc would plausibly pull back into scope (the canonical case: "no rate-limiting / no email-at-scale / no abuse-prevention" sitting beside a public launch). These are the cuts that look settled but hide a gap.
> - **Non-goals confirmation trail (the unconfirmed-cut check).** Whether each non-goal was actually *confirmed* by the user isn't visible on disk, but the batching failure leaves a signature: several distinct capabilities collapsed behind one shared boilerplate reason, or a row whose reason restates the cut instead of giving an intentional tradeoff ("X is out of scope — we're not doing X"). Flag a block of Part 4 non-goals that share a single generic reason, or any non-goal whose reason names no tradeoff traceable to a stated goal — both are the signature of cuts batched behind a one-liner rather than proposed and confirmed one at a time. (This is the on-doc proxy for sub-step 4.1's propose-and-confirm discipline, which the on-disk mechanical checks can't see directly.)
> - **Coherence across releases.** If sub-steps mention future releases (Part 2's roadmap, future-release stakeholder notes in 3.1), do those mentions hang together — or do different parts assume different futures?
> - **Voice and confidence consistency.** Check two separate scales, each of which must stay consistent: **confidence** is H/M/L across Parts 5 and 6, and dimension **ratings** are H/M/None (no L). Does any Part quietly use different confidence vocabulary than the others? Does the doc read in one voice, or does the writing shift in ways that suggest some sections were rushed? Also check the **importance/state axes stay separate**: a dimension's rating (High = important to stakeholders) and its current state (Part 6's actual and gap) are orthogonal — flag any prose that treats "High" as meaning *in trouble*, or that reads a High-at-bar row as a contradiction (it's a success story).
>
> If you spot something the per-sub-step DONE checklists *should* have caught (e.g. a Part 5 H rating with no stakeholder bar in its rationale), flag it as a "backstop catch" — it indicates the writing process didn't enforce its own gates, which is itself useful information.
>
> For each finding, write a one-line description of the misalignment plus a suggestion for resolving it.
>
> Output format: a markdown list of consistency findings.

### 4. Collapse and filter (main agent)

When all three subagents return, run the collapse pass.

For each finding from each subagent, decide:

- **Real and important** → surface as a review finding.
- **Real but minor** → surface, marked low-priority.
- **Spurious / off-base** → drop. **Note dropped findings briefly** so the user can spot if you over-filtered.

Three guidelines:

1. **Trust subagents but verify.** A finding that says *"non-goals look thin"* is worth surfacing; one that says *"the wording in section 3.2 is clunky"* probably isn't.
2. **Look for compounding patterns.** Three weak indicators that all point at the same root cause (e.g. *"rationale is generally vague throughout"*) are stronger together than apart. Surface the pattern.
3. **Distinguish blockers from flags.** Some findings should block declaring the strategy done. Others are judgement calls.

#### Severity rules

**Apply the contextual-fit gate (Pass 0) to severity.** The lists below are the *durable-production* defaults. For other jobs, adapt per the gate: *a missing section is a blocker only if its absence prevents the strategy from doing its stated job in this context.* Example: a missing production-observability or mature-process section is a blocker for a durable strategy. For a pre-implementation or lightweight-slice strategy that declares it a non-goal, it's a **deliberate deferral**, not a blocker. If it's silently absent — not declared — it's a **flag**. Sort every finding into one of three buckets: **current blocker**, **useful now/pre-implementation refinement**, or **later-lifecycle deferral**.

**Blockers** (must fix before declaring strategy done — durable-production defaults):

- Part 4 (Non-goals) empty or fewer than 3 entries with reasons.
- Part 6 (Risk Map) missing any H or M dimension from Part 5.
- Any oracle FAIL in subagent A. This includes a `## Strategy job` paragraph that is missing *and* can't be inferred (check 18; missing-but-inferable is only a flag), and a missing scratch file for a *required* dispatch (check 20) — hard evidence the dispatch was fabricated or silently skipped. Remember check 20 derives "required" from doc structure: a silently-skipped required dispatch — e.g. a step-boundary `/contradiction-check` for a Part that is present — is a blocker even though the strategy never claimed it ran. It also includes check 22's revision failures: an unevidenced "fixed" claim, or a revision whose diff against the archived prior version shows only closures of prior items — a revision anchored on last time verified the past instead of assessing the present, and the gaps have moved. And check 24's correction-scope failures: a correction whose diff strays outside its recorded union, or whose recorded union under-computes the dependency graph's closure.
- Any hard contradiction surfaced by subagent C (e.g. a non-goal that contradicts an H rating; a Strategy-job out-of-scope item the body treats as in-scope).
- Three lenses missing for any stakeholder.
- **(Agentic one-shot job only)** missing one-shot success/partial/failure criteria, final-report evidence requirements, agent-failure-mode decision rules, or explicit scope-control Nones.

**Flags** (judgement — review and decide):

- Highs with missing or generic Dealbreaker citations, or a Medium anchor that was never applied (check 10). *(A High-dominated distribution is not, by itself, a flag — the low-stakes material was already cut by rating time. For a lightweight slice, a low-H / many-None distribution is the expected shape.)*
- Stakeholder coverage gap (a stakeholder with no H/M dimension touching their bars).
- Subagent A FLAGs (borderline oracle results; stub scratch files; leaked process notes).
- **Scratch-file audit INCONCLUSIVE** (check 20 could not be performed — no filesystem access or no `.scratch/` directory). Say so explicitly as "the dispatch audit could not be run"; never silently record the audit as passed. It is not a blocker on its own, but if the dispatch evidence couldn't be checked, report that — don't report the strategy as clean.
- Subagent B WEAK indicators (judged against the job, not a production ideal).
- Subagent C consistency findings that aren't outright contradictions.
- Production machinery silently absent (not declared a non-goal) in a non-durable strategy.

### 5. Produce the report

**Write every finding for both readers — names before coordinates** (PHILOSOPHY: *write for both readers*). A review is read by people who don't have the strategy open and may not have written it. Every blocker, flag, and deferral must be self-contained: at first mention of any doc element, give its human name and a few words of what it is, with the label as a trailing pointer — *"the planned payment-divergence simulation (Action F)"*, not *"Action F"*; *"the docs-describe-today's-code dimension (14)"*, not *"dim 14"*. A bare coordinate is never the subject of a sentence. Gloss framework vocabulary (*"Gated"*, *"the anchor rule"*, *"over-confident actual"*) in plain English on first use. The test for each finding: could a teammate who never wrote this strategy act on it without opening the doc to decode references? This is the same bar the review holds the strategy to in indicator 1 (org-wide clarity) — the review's own output has to clear it. And keep the prose **plain** (PHILOSOPHY: *say it plainly*): short words, active verbs, one idea per sentence; framework terms glossed, everything else everyday English.

Write the consolidated report and surface it in the conversation. Format:

```markdown
# Quality Strategy Review for <project>

*Reviewed <YYYY-MM-DD>*

## Strategy job & contextual fit

<1–2 sentences: what job this strategy is for (durable production / pre-implementation / agentic one-shot / lightweight slice — and whether the `## Strategy job` paragraph stated it or it was inferred), and the severity lens this review applied as a result. Say outright if a gap that would normally block was reclassified as a deliberate deferral because of the job.>

## Headline

<2–3 sentences: is this strategy in good shape, mixed, or weak *for its job*? Where is it strong and where is it weak?>

## Blockers (must fix before declaring strategy done)

- **<blocker title>** — <one or two lines describing the issue>. Suggested fix: <…>.

(Or "None.")

## Flags (judgement — review and decide)

- **<flag title>** — <one or two lines>. Why it matters: <…>. Suggested action: <…>.

## Deferrals (correct for this job, not blockers)

<Sections that would be blockers for a durable production strategy but are deliberate deferrals or out of scope for *this* strategy's job. Naming them shows the review applied the gate on purpose — not that it missed them.>

(Or "None — this is a durable production strategy; full machinery is expected." / "None noted.")

## The seven indicators

| Indicator | Strength | Note |
|---|---|---|
| Org-wide clarity | Strong/Medium/Weak | <one-line> |
| Instrumentation from start | … | … |
| Legible work plan | … | … |
| Precision over comfort | … | … |
| Decision support at edges | … | … |
| Quick re-orientation | … | … |
| Explicit non-goals | … | … |

## What's strong

- <3–5 concrete things this strategy does well>

## What's weak

- <3–5 concrete things to improve, prioritised>

## Filtered out

<bullets of subagent findings the main agent dropped as spurious or trivial, with brief reasoning. Lets the user spot over-filtering.>

---

*If you want the full unfiltered subagent outputs for reference, they are available below.*

<details>
<summary>Subagent A (oracle) full output</summary>
…
</details>

<details>
<summary>Subagent B (indicators) full output</summary>
…
</details>

<details>
<summary>Subagent C (consistency) full output</summary>
…
</details>
```

### 6. Offer walkthrough

After the report, ask the user:

> *"Want to walk through the blockers and flags one at a time, or are you good to take it from here?"*

If walkthrough: go through each blocker and flag in order. For each, dig in if needed, suggest concrete fixes, and capture the user's decision. The user resolves each.

To fix a blocker, the usual move is to re-run the relevant `/quality-strategy` sub-step in revision mode. Suggest that as the action.

## Push back when

- The user wants to skip fixing a blocker. *"That blocker is one of the things that makes this strategy actually load-bearing. Skipping produces a strategy that looks complete but isn't."*
- The user dismisses all flags without examining them. *"There were N flags — let's at least walk through them before closing out."*
- The user wants to mark a clearly-weak indicator as resolved without changes. *"What specifically is going to be different now that you've thought about it?"*

## This skill is DONE when

- [ ] The contextual-fit gate (Pass 0) has run: the strategy's job is classified (from the `## Strategy job` paragraph, or inferred + flagged if missing) and the severity lens recorded and passed into the subagent briefs.
- [ ] Three subagents have been dispatched in parallel and returned findings.
- [ ] The main agent has run the collapse pass and produced a consolidated report, sorting findings into current blockers / now-refinements / later-lifecycle deferrals per the job.
- [ ] The report has been shared with the user.
- [ ] All blockers have been resolved (typically by re-running the relevant `/quality-strategy` sub-step).
- [ ] The user has reviewed flags and either resolved them or actively confirmed they're acceptable as-is.

## Output

The consolidated review report is shared in the conversation. By default it's not written to a file. If the user wants the report persisted, write it to `quality/review-<YYYY-MM-DD>.md`.

If the strategy passes (no unresolved blockers, flags reviewed), confirm to the user:

> *"Strategy review passed. The strategy is feature-complete and ready to use. Decision support, plan execution, and updates can now happen against it."*

Then **recommend the next step — and let the risk map pick it.** The pack's follow-on order is a branch, not a fixed sequence (Q2 before Q3: you can only investigate what you can judge):

- Risk map **dominated by Unknowns whose to-resolve notes say nothing can judge them yet** → recommend **`/evaluation-strategy`** first (with `/tooling-strategy` planning agreed builds): decide how the project will judge those dimensions, then `/test-strategy` once the means of judging exist.
- Risk map **mostly answerable** → recommend **`/test-strategy`** first; its blocked questions sharpen the tooling demand (via `/tooling-adequacy`), and `/tooling-strategy` then plans the combined build. Risks concentrated in how work gets done → put **`/process-strategy`** early.

Say which branch this strategy is on and why (cite the risk map you just reviewed — you have it in hand). Never present *quality strategy → test strategy* as "the designed sequence"; the designed sequence is this branch.

And — since the strategy just passed review and is now in its shareable, final form — **offer `/quality-artefacts` alongside the analytical branch**: *"it's also ready to turn into something you can share — `/quality-artefacts` builds a dashboard, a risk heatmap, or a social card from it."* This is the payoff moment for the work; name it next to the lanes, not as an afterthought.

If this review ran as part of `/quality-strategy` itself, return control to the orchestrator and report either pass or remaining work.
