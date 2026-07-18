---
name: project-scaffolding-and-docs
description: >
  Use when starting a project, auditing an existing repo, planning a release,
  or writing project docs such as a spec, roadmap, release plan, engineering
  guide, changelog, or decision log. Provides a markdown-only, tool-neutral
  methodology for repo structure and living documentation.
metadata:
  type: methodology
  applies-to: any project, any LLM, any language
---

# Project Scaffolding & Documentation Discipline

A portable system for keeping a project's *intent*, *plan*, *reality*, and
*history* legible — to a newcomer, to a future maintainer, and to an LLM
picking the project up cold. It is markdown-only and tool-neutral: no feature
of any specific agent is required. The litmus test the whole system serves:

> **A competent stranger — human or LLM — can open the repo, read the docs in
> order, and either use the product or correctly implement the next change,
> *and re-evaluate the choices already made*, without asking anyone a question.**

Completeness is the floor, not the bar. A skeleton with every section present
but filled with vague placeholders ("fast", "handles large files well") passes
"all the docs exist" and *fails this test* — the stranger still can't verify a
requirement or judge whether a past decision still holds. The sections below are
the structure; **§10 is the quality bar** that separates a filled-in template
from a document worth trusting. If you only read two things, read §5 (the
decision log) and §10 (the self-check).

---

## 1. The core principles

These are the *why*. The document set and templates are just one good
embodiment of them; if you adapt the layout, keep the principles.

1. **One fact, one home.** Each fact lives in exactly one document; everything
   else *links* to it. Duplication rots — the copies drift and the reader
   can't tell which is true. The spec says *what*; the engineering guide says
   *how here*; the changelog says *what shipped*. Never restate; cross-link.

2. **Separate target design from shipped reality, and mark the gap
   explicitly.** A living spec describes where the product is going; the code
   is where it is now. When they differ, say so *in place* with a visible
   marker (a "shipped reality" callout, a "*shipped (vX.Y)*" tag). Silent
   divergence is how docs become lies.

3. **Record decisions, not just outcomes.** The most valuable, least
   reproducible artifact is *why* a non-obvious choice was made — the
   alternatives, the cost accepted, and (often) the user report or root cause
   that forced it. Keep a **decision log**. Code shows *what*; git shows
   *when*; only the decision log shows *why*, and only if you write it down.

4. **Plans must be cold-start executable.** An implementation plan is for a
   reader who has *none* of your context. It states which files it assumes
   exist and in what shape, the design, the ordered steps, how to verify each,
   and what "done" means. If picking it up requires re-deriving what you
   already know, it isn't finished.

5. **Work in safe pause points.** Order every plan so each completed step
   leaves the project shippable: builds, passes tests, runs. This is what makes
   a project *interruptible* — by a bug report, by a context reset, by a new
   priority — without leaving a half-wired mess.

6. **Verification is part of the artifact, not an afterthought.** Every feature
   carries acceptance criteria; every work step names how it's checked. "Done"
   means *observably* done, not "code written."

7. **The boundary is a feature: write down what's out of scope.** An explicit
   "not doing this, here's why / when later" prevents scope creep and answers
   the reviewer's "but what about…" before it's asked.

8. **Mechanical steps get a checklist, run every time.** Releasing, version
   bumping, doc-syncing — anything done repeatedly and easy to half-do — lives
   as an explicit checklist so it is never partially skipped.

9. **Specific beats vague; numbers beat adjectives.** A requirement that says
   "fast" or "memory-efficient" can be neither verified nor violated — it is
   decoration. Say *how fast* (< 150 ms to first diff), *how much* (< 150 MB
   RSS), *what cap and fallback* (a line repeating > 64× falls back to coarse
   block diff flagged "approximate"), *which threshold* (pair similarity ≥ 0.3).
   Every budget carries units and a mark for whether it is enforced or
   aspirational. An unqualified adjective in a requirement is a bug — replace it
   with the number a test could check, or delete it.

---

## 2. The document set

Six documents. Small projects can fold some together (see §2.7); the *roles*
are what matter, not the file count. Each answers exactly one question.

| Document | Answers | Volatility | Primary reader |
|---|---|---|---|
| `README.md` | "What is this and where do I start?" | low | newcomer |
| `SPEC.md` | "What is it, and *why* is it built this way?" | low, living | anyone |
| `docs/ROADMAP.md` | "What's next, in what order, and how do interruptions work?" | medium | planner |
| `docs/plans/<ver>-<name>.md` | "How do I build this one slice, cold?" | high → frozen | implementer |
| `docs/ENGINEERING.md` | "How do I build/test/release *in this repo*?" | low | implementer |
| `CHANGELOG.md` | "What actually shipped, and when?" | append-only | user |

A clean default layout:

```
repo/
├── README.md            # entry point + index + current scope
├── SPEC.md              # product + technical spec + default decision log (the what/why)
├── CHANGELOG.md         # what shipped, newest first, dated
├── docs/
│   ├── ROADMAP.md       # release train + versioning/interruption policy
│   ├── DECISIONS.md     # optional: standalone decision log when SPEC gets large
│   ├── ENGINEERING.md   # build/test/release reality for THIS repo
│   └── plans/
│       ├── 0.2.0-<theme>.md
│       ├── 0.3.0-<theme>.md
│       └── …            # one self-contained, executable plan per release
├── src/ …               # match the module boundaries the spec declares
└── tests/ …             # tests encode WHY each behavior matters (see §6)
```

The cross-link web that makes "one fact, one home" navigable:
- `README` → links to all of SPEC, ROADMAP, ENGINEERING, CHANGELOG.
- `SPEC` → roadmap detail lives in ROADMAP; build reality in ENGINEERING.
- `ROADMAP` → each row links its plan in `docs/plans/`; back-links to SPEC.
- each `plan` → cites SPEC sections (`§N`) for the *what*, defers *how-to-build*
  to ENGINEERING.
- `CHANGELOG` → prose only; no design rationale (that's the decision log).

### 2.1 README — the front door

Shortest useful path from "never seen this" to "building it / using it." Keep
it to: one-paragraph pitch, a **status line** (current version + maturity), a
**documentation index** (links to the five other docs with one-line hooks), a
build/run quickstart, a directory map, and a **"current scope"** section split
into *working now* vs *deferred (with pointers to where each deferred item is
scheduled)*. Everything deeper is a link, not a copy.

### 2.2 SPEC — the what & why (living)

The anchor document. A dated, versioned **status header** stating it is a
*living* spec and defining the convention for "shipped vs target" (see
principle 2). Then, typically three parts:

- **Product spec** — positioning, core principles, the feature set in
  behavioral detail, and an explicit **out-of-scope** list (principle 7).
- **UX/UI spec** — information architecture, interaction details, the
  platform-native behaviors and accessibility requirements that are
  release-blocking rather than best-effort.
- **Technical spec** — build system, architecture, per-module
  responsibilities and public interfaces, performance/resource budgets (mark
  which are enforced), normative error-handling and edge cases, distribution.

Two devices make the spec trustworthy as it ages:

- **"Shipped reality" callouts.** Where the implemented reality diverges from
  the clean design (a workaround, a not-yet-built module), a blockquote callout
  states the divergence and links to the detail. The design stays
  authoritative; the reader is never misled about today.
- **Inline shipped markers.** Tag behaviors that exist now (e.g. *"shipped
  (0.1.x)"*) so target design and current behavior are distinguishable
  sentence by sentence. Keep only the useful delta visible: after a major
  release or other stabilization point, normalize old minor/patch markers into
  plain present-tense text and leave markers only where current shipped reality
  still differs from the active target design. Git history and CHANGELOG keep
  the older release detail.

End the SPEC with the **decision log** by default — see §5. If it grows large
enough to interrupt spec readability, move it to `docs/DECISIONS.md` and leave
a pointer in SPEC. Keep exactly one log; splitting decisions across two places
violates "one fact, one home." This is the single most valuable section for
long-term maintenance.

### 2.3 ROADMAP — what's next and how interruptions work

An *index*, not a plan. It holds:
- A **release train table**: version · theme · link-to-plan · status.
- The **versioning & interruption policy** (see §7): what minor vs patch
  releases mean, and the rules that keep the project interruptible.
- **Ordering rationale**: why the releases are sequenced as they are
  (dependencies between them) — the reasoning a re-planner needs.
- The unscheduled-candidates list (future work not yet on the train).

### 2.4 Plans — one executable file per release/slice

The workhorse. Each plan is **self-contained and cold-start executable**
(principle 4). Required sections:

- **Header:** status · theme (one sentence) · rough effort.
- **Assumptions about current code** — the exact files/shapes the plan
  expects, *to be re-checked after any interrupting change* (principle 5).
  This is the guard against drift: when reality moves, you re-read this section
  and update the plan instead of executing a stale design.
- **Goals / non-goals** — what this slice does and explicitly does *not* do.
- **Feature sections**, each with: *UX requirements* (observable behavior),
  *technical design* (how, with the tradeoffs named), and *acceptance*
  (what proves it works).
- **Work breakdown** — an ordered list where **each step is a safe pause
  point** and names its verification.
- **Risks** — what's most likely to go wrong and the mitigation/fallback.

A plan is *frozen* once its release ships; the CHANGELOG records the result and
the next plan begins. Don't retro-edit shipped plans except to mark status. Keep
active work in `docs/plans/`; move shipped or superseded plans to
`docs/plans/archive/` when the active directory gets noisy. Update the ROADMAP
as the primary plan index so retrieval tools and humans see current work first;
avoid relying on deep historic links to plan subheadings because archived files
may move or be renamed.

### 2.5 ENGINEERING — how to build/test/release *here*

The repo-specific operational truth that doesn't belong in the product spec:
exact build/test/run commands, **toolchain workarounds** (with a "do not
'clean up' without testing" warning and the root cause), code conventions,
the **versioning checklist** (§7), the **interruption protocol** (§7), and the
**manual verification pass** for anything that can't be checked automatically.
The SPEC says the product should be fast and native; ENGINEERING says *here is
the command, here is the broken tool and its workaround, here is the 10-minute
manual pass before you tag a release*.

### 2.6 CHANGELOG — what actually shipped

Newest-first, one dated section per version. **User-facing wording**, not
commit messages. Each entry says *what changed* and *why it mattered to the
user*, ideally with concrete cases and measured impact where relevant. Design
rationale does **not** go here — it goes in the SPEC decision log; the
changelog links to it if needed. (Format guidance: Keep a Changelog +
Semantic Versioning are good defaults.)

### 2.7 Scaling down and up

For a small or early project, collapse — but keep the roles. The **minimal
viable set for a tiny prototype** is:

- `README.md` — pitch, status, quickstart, current scope.
- `SPEC.md` — observable requirements, explicit out-of-scope, and a short
  decision log.
- `CHANGELOG.md` — dated record of what actually shipped.

Then expand only when the project earns the extra files:
- Merge ROADMAP into the SPEC's roadmap section until you have >2 planned
  releases.
- Skip `docs/plans/` until a release is big enough to need a cold-start plan;
  a short checklist in the roadmap row suffices before then.
- Merge ENGINEERING into the README until build/test reality outgrows it.
- Keep the decision log in SPEC until it gets too large, then move it whole to
  `docs/DECISIONS.md` and link to it.
- **Never** drop: the changelog, the out-of-scope list, and the decision log.
  Those are cheap to start and impossible to reconstruct later.

For a growing project, split before the anchor becomes a bottleneck. Treat any
of these as a signal that `SPEC.md` should become a router plus summary rather
than the only spec file: repeated merge conflicts, multiple engineers editing
UX and architecture independently, SPEC passing roughly 1,500–2,000 lines, or an
LLM routinely needing only one spec slice but receiving the whole file. A common
large-project layout is:

```text
SPEC.md                  # status, conventions, scope, links, high-level summary
docs/specs/product.md    # product behavior and out-of-scope details
docs/specs/ux.md         # IA, flows, accessibility, platform behavior
docs/specs/technical.md  # architecture, module contracts, budgets, edge cases
docs/DECISIONS.md        # one decision log, if SPEC no longer holds it
```

Keep `SPEC.md` as the structural anchor: it states the shipped-vs-target
convention, current status, and where each fact lives. Do not duplicate facts
across split files; move the section wholesale, leave a pointer, and update
**all** cross-references that pointed at the old section. At minimum,
check README project-doc links, ROADMAP release rows and plan index entries,
active plan assumptions/links, ENGINEERING context bundles, CHANGELOG entries,
decision-log entries that reference moved spec sections or plan sections, and
any header anchors. Treat this as part of the same
change; a split spec with stale links is worse than an oversized but truthful
SPEC.

For monorepos or microservice systems, use a two-level pattern: a root
`SPEC.md` / `docs/specs/system-architecture.md` owns cross-service behavior,
interfaces, data contracts, and release coordination; each service or package
keeps only the local docs it needs (`README`, local `SPEC` or `ENGINEERING`,
and plans for service-local changes). Root docs override only system-level
contracts; local docs own implementation details. Cross-service decisions go in
the root decision log, while service-local choices stay with the service.

Plans follow the same boundary. A **root plan** owns orchestration: interface
changes, rollout sequencing, compatibility windows, release coordination, and
links to affected service-local plans. A **service-local plan** owns the local
implementation slice: files, tests, migration steps, and service-specific
verification. Do not duplicate the same fact in both; the root plan should point
to the service plan for local details, and the service plan should point back to
the root plan for system-level contracts. Example: root plan
`docs/plans/0.4.0-auth-contract.md` defines the `/session` contract and links to
`services/api/docs/plans/0.4.0-session-endpoints.md` and
`services/web/docs/plans/0.4.0-login-flow.md`; those service plans link back to
the root plan instead of restating the shared contract.

---

## 3. Workflow: writing a good spec

1. **Positioning first.** One table: what it is, what it competes with, who
   it's for, the wedge. If you can't fill this in, you're not ready to spec
   features.
2. **Principles before features.** A short numbered list of the non-negotiable
   properties (e.g. "speed is the feature," "native or nothing"). Every later
   decision cites these; they are the tie-breakers.
3. **Features as observable behavior**, not implementation. "Results stream as
   the tree is walked; no modal wait" — a reader can *verify* that. Tables for
   enumerable facts; prose for behavior.
4. **Write the out-of-scope list in the same pass.** It's easiest to see the
   boundary while specifying what's inside it.
5. **Technical spec: declare module boundaries and budgets.** Name each module,
   its single responsibility, and its public surface. State resource/perf
   budgets as numbers and mark which are enforced vs aspirational.
6. **Normative edge cases.** List the nasty ones (permission denied, file
   changed under you, oversized input) and the *required* behavior. "Selected,
   normative" — you don't enumerate everything, you pin the ones that matter.
7. **Seed the decision log** with the foundational choices (build system,
   core architecture, key tradeoffs) even before any code — these are the ones
   future-you will most want explained.

Quality bar: every requirement is *observable* (you could write a test or do a
manual check that passes or fails on it), and every non-obvious choice has a
decision-log entry explaining the cost it bought.

---

## 4. Workflow: from spec to roadmap to plan to code

### 4.1 Derive the roadmap

Group the spec's features into **release themes**, each a coherent capability
slice. Order them by *dependency* (what must exist before what) and state the
ordering rationale. Decide your versioning scheme (§7). Put it in the release
train table. Identify cross-cutting concerns (accessibility, security, perf)
that are cheap to honor early and expensive to retrofit — make them *acceptance
criteria in every plan*, not a release of their own.

### 4.2 Write the plan for the next release

Use the plan template (`templates/release-plan.md`). The discipline that makes
it executable:
- Pin **assumptions about current code** by actually reading the code now —
  name the types/files/functions the plan will touch and their current shape.
- For each feature, separate *UX requirements* (what the user observes) from
  *technical design* (how you'll build it). Name the tradeoffs and the
  fallback ("if the incremental approach proves fiddly, full recompute under
  the size cap is an acceptable first version").
- Make the **work breakdown** a sequence of safe pause points. A good test:
  could you ship after step 3 and resume at step 4 a week later? If step 3
  leaves the build broken, re-split it.
- Give every step a **verification** clause and every feature an **acceptance**
  block.

### 4.3 Execute, updating docs as you go (the critical, oft-skipped part)

Documentation is updated *as part of* the implementation, not after. Per step:

1. Implement the slice for the current safe pause point.
2. **Verify** it per the step's verification clause (run the narrowest test,
   then broaden; actually run the thing for behavior/UI changes).
3. **Update docs in the same change:**
   - SPEC: flip the relevant behavior's marker to *shipped*; remove or update
     any "shipped reality" callout the change resolved.
   - If a non-obvious choice was made, **add a decision-log entry now** (§5) —
     while the reasoning and the triggering report are fresh. This is the
     entry you will never reconstruct as well later.
   - Tests: add/adjust so the new behavior is covered, with a header comment
     encoding *why* it matters (§6).
4. At a **release** boundary, run the full versioning checklist (§7): bump
   version everywhere it appears, write the CHANGELOG entry, update README
   "current scope," mark the plan/roadmap row shipped, run the manual pass.

The rule: **a behavior change and its doc change are one unit of work.** A diff
that changes behavior but not docs is incomplete; a reviewer should reject it
the same way they'd reject one with no tests.

---

## 5. Change records: the decision log

Two records, different jobs. The **changelog** (§2.6) is *what shipped*, for
users. The **decision log** is *why we chose this*, for maintainers. Keep both;
don't conflate them.

A decision-log entry is a numbered, append-only item (lives at the end of the
SPEC, or its own `docs/DECISIONS.md` if it grows large). The strongest entries
have this shape:

> **N. <decision in a sentence> (<version/date>)** — <the trigger: a user
> report, a measured problem, or a constraint>. <root cause or the real
> reason, if the trigger had a subtle one>. <what was chosen, and crucially
> what was *rejected* and the cost accepted>. <where it's enforced/tested>.

What makes it worth the keystrokes:
- **The trigger and root cause.** "User reported X; the real cause was
  structural, not cosmetic — Y" is worth ten times "we use histogram diff."
- **The rejected alternative and its cost.** A decision without its discarded
  options is a fact, not a decision; the next person can't tell if it's still
  right.
- **Measured-before-designed.** When a choice was made by measuring (surveyed
  the corpus, profiled, prototyped), record the measurement — it lets a
  successor re-evaluate when conditions change.
- **Name the regression fixture.** When a real input drove the decision, name
  it in the entry (a specific file, a named corpus, a reproduction case) and add
  it as a permanent test (§6). The entry explains *why*; the fixture *proves it
  stays fixed*, and the name lets a successor find both.
- **Newest wins, but keep the old.** When a later decision overrides an
  earlier one, add a new entry referencing the old number; don't silently edit
  history — the supersession *is* information.

A worked contrast — the *same* decision written two ways:

> *Weak:* **17. Improved item matching (0.1.8)** — similar items sometimes paired
> incorrectly, so small edits looked like removals plus additions. Switched to a
> similarity-based matcher; works better now.

> *Strong:* **17. Similarity pairing inside changed regions (0.1.8)** — reports
> from three anonymized regression cases showed renamed records rendering as one
> removed item beside one added item. Root cause was *structural, not cosmetic*:
> rows inside a changed region paired purely by position, so one inserted row
> shifted every following pair off by one. Replaced positional pairing with a
> monotonic maximum-similarity matcher (token-bag Dice ≥ 0.3, DP capped at
> 65,536 cells); a gap with rows on both sides stays one positional replace so
> genuine rewrites keep the compact rendering — *rejected* re-segmenting every
> region because it made unrelated rewrites harder to read, the common case.
> Regression fixtures: `case-renamed-field`, `case-inserted-row`,
> `case-nested-block`. Anonymized corpus: unrelated pairings 867 → 522; placeholder
> alignment rows 6,301 → 3,409.

Both describe the same change. The weak one is a *fact* a successor must take on
faith; the strong one lets them re-evaluate it when conditions change — because
it names the root cause as structural, the rejected alternative and its cost,
the fixtures that pin it, and the measured before/after. That delta *is* the
value of the log. (This is the bar §10 checks for.)

This log is also the ideal **handoff/continuity artifact**: an LLM resuming the
project reads it to recover the reasoning it would otherwise re-derive
(usually worse). Treat it as the project's long-term memory of *why*.

---

## 6. Tests as documentation

Tests are executable spec. Two habits make them documentation, not just gates:

- **Encode *why* in the test, not just *what*.** A header comment per test
  group stating the consequence of getting it wrong ("these offsets become
  UI ranges; an off-by-one crashes or highlights the wrong characters")
  turns a red test into a *diagnosis*.
- **Capture real regressions as named fixtures.** When a bug report drives a
  fix, add the triggering input as a permanent test case named for the case.
  The decision log explains the *why*; the fixture *proves* it stays fixed.

Match the project's existing test framework and conventions; don't introduce a
second style. Where some verification can't be automated (GUI, manual perceptual
checks, hardware-dependent behavior, accessibility review), the ENGINEERING
manual-pass checklist (§2.5) is its documented substitute. Treat that checklist
like a test suite: name the screens/flows, the fixture data, the expected
observation, and the release-blocking failures. Release summaries must state
plainly what was machine-verified, what was manually verified, and what remains
unverified.

---

## 6.1 LLM ingestion strategy

Optimize for both direct reading and retrieval. The default cold-start path is
README → SPEC → ROADMAP → active plan → ENGINEERING as needed; a human or LLM
should not need to ingest every file for every task. For small repos, reading
the full set is fine. For larger repos, keep the docs retrieval-friendly:

- Put routing summaries and links in README/SPEC/ROADMAP so the right slice is
  discoverable without scanning the whole tree.
- Keep active plans in `docs/plans/` and older plans in `docs/plans/archive/` so
  retrieval tools do not overweight stale implementation history. If using a
  vector store or repo indexer, give archived plans lower priority or exclude
  them from default task bundles; include them only for history, audits, or
  regression archaeology.
- Split large specs into `docs/specs/` once readers routinely need one slice,
  not the whole monolith (§2.7).
- In ENGINEERING, document the expected prompt/context bundle for common work
  modes: bug fix, feature plan, release verification, and architecture audit.

---

## 7. Versioning, releasing, and interruptions

**Versioning scheme.** Pick one and write it in the ROADMAP. The project may
use any scheme that makes ordering and compatibility legible; document the
tradeoff. Common choices:

- **0.x minor/patch discipline** — useful for an evolving product: minor
  releases (`0.x.0`) carry planned feature themes; patch releases (`0.x.y`) are
  reserved for *interruptions* — bug reports, small UX corrections, user
  requests — and take priority over the active plan.
- **Strict SemVer** — best when other code depends on your public API; major
  means breaking changes, minor means backward-compatible features, patch means
  backward-compatible fixes. It is heavier if the product has no stable API.
- **Date-based versions** (`YYYY.MM.DD` or `YYYY.MM.N`) — useful for data,
  content, research, or internal tools where chronology matters more than API
  compatibility. It is less expressive about breakage.

Hybrid/project-specific schemes are acceptable when documented: for example, a
0.x product may still reserve major-like milestones for public API stability, or
an internal tool may pair date versions with compatibility labels. The rule is
legibility, not ceremony.

Whichever scheme you choose, the release train still needs a clear distinction
between planned work and interrupting work.

**Rules that keep the project interruptible** (so a patch never strands a
half-built feature):
1. The main branch must *always* build, pass tests, and run. Land plan work in
   verifiable slices, never half-wired.
2. Every plan's work breakdown is ordered into safe pause points.
3. After any interrupting release, **re-check the active plan's "assumptions
   about current code"** and update the plan if the interruption changed
   something it depended on.
4. The version bump + changelog + any in-app version string are part of *every*
   release, patch or minor.

**The versioning checklist** (lives in ENGINEERING, run every release):
1. Bump the version everywhere it appears (build config, in-app/UI string,
   package metadata).
2. Write the CHANGELOG entry (user-facing wording, dated).
3. Update README "current scope" if scope changed; update SPEC markers if
   behavior diverged from what was written.
4. Build + test green; run the manual verification pass; mark the plan/roadmap
   row shipped.
5. Move shipped/superseded plans out of the active lane when useful:
   `docs/plans/archive/<version>-<theme>.md`. Update the primary plan index in
   `docs/ROADMAP.md`; historic CHANGELOG/decision-log links should point to the
   archived file or archive directory, not volatile header-level anchors. If a
   decision-log entry linked deeply into the old active plan path, update it to
   the archived file or to the ROADMAP index.
6. At major/stabilization releases, normalize old inline shipped markers so the
   spec shows the current system cleanly and only live target-vs-shipped deltas
   remain marked.

**The interruption protocol** (also in ENGINEERING):
1. Stop at the current safe pause point; make the main branch shippable
   (commit or set aside the in-progress plan work).
2. Implement the interrupting request as the next patch release, following the
   versioning checklist.
3. Re-read the active plan's assumptions; update the plan doc if the patch
   invalidated anything.
4. Resume the plan; note the interruption in its status line.

**Dynamic prototyping / R&D.** In 0.x discovery work, safe pause points can be
shorter and plan certainty can be lower, but the plan must still remain honest.
If a spike invalidates the design, do not quietly overwrite history. Mark the
old section or plan `superseded`, record the trigger/root cause in the decision
log if the change is non-obvious, and either add a new plan section titled
`Revised approach after spike <date>` or create a replacement plan. Very early,
disposable spikes may live in `docs/spikes/` as evidence, but the decision log
should point to the spike and the active plan should still contain only one
execution path.

---

## 8. Anti-patterns (and the fix)

- **Duplicated facts across docs.** → One home, links elsewhere (principle 1).
- **Docs describe the design as if it's all built.** → Shipped markers +
  shipped-reality callouts; periodically normalize old markers so the spec does
  not become a release-history scrapbook.
- **Decisions live only in someone's head or a closed PR thread.** → Decision
  log (§5).
- **A plan that only its author can execute.** → Assumptions section + ordered,
  verifiable steps (principle 4).
- **"Big bang" branches that break main for days.** → Safe pause points
  (principle 5).
- **Docs updated "later" (i.e. never).** → Behavior change and doc change are
  one unit of work (§4.3).
- **Scope creep from an unstated boundary.** → Explicit out-of-scope list
  (principle 7).
- **The changelog turned into a design diary, or `git log` dumped verbatim.**
  → User-facing prose; rationale goes to the decision log (§2.6, §5).
- **The decision log used as a changelog substitute.** → Record durable choices,
  rejected alternatives, and accepted costs; shipped user-visible changes belong
  in CHANGELOG, with links back only when the rationale matters.
- **Stale archived-plan links in decision logs or CHANGELOG.** → When archiving
  plans, update links to the archived file or ROADMAP plan index; avoid brittle
  old active-path header anchors.
- **A "DONE/NEXT" scratch file committed as if it were a spec.** → Task scratch
  is disposable and separate from durable docs; the plan + decision log are the
  durable record.

---

## 9. Templates

Fill-in-the-blank starting points are in `templates/`:

- `templates/readme.md`
- `templates/spec.md` (includes the default decision-log section)
- `templates/decisions.md` (optional standalone decision log for large projects)
- `templates/roadmap.md`
- `templates/release-plan.md`
- `templates/engineering.md`
- `templates/changelog.md`

Each has inline `<!-- guidance -->` comments explaining what goes where and
why; delete them as you fill the template in.

---

## 10. The quality bar — self-check before you call a doc "done"

The templates and §2 give you the *structure*. This section is what separates a
filled-in skeleton from a document the litmus test (top of file) actually
passes. **Filling every section is necessary, not sufficient.** Run the relevant
list below before you consider an artifact finished; an item that fails is not a
style nit, it's an unfinished doc.

### 10.1 Applies to every document

- **No unqualified vague adjective in a requirement.** "Fast", "efficient",
  "robust", "handles large files well" — each is either a number with units or
  it's deleted (principle 9). If you can't put a number on it, you don't yet
  understand the requirement well enough to write it.
- **Reality is marked.** Every statement about *current* behavior carries a
  shipped marker; every statement about *target* behavior is visibly
  not-yet-built (principle 2). A reader must never have to guess which is which.
- **Cross-references are links to a specific anchor** (`§N`, a file path), not
  "see the spec". One fact, one home; everything else links to it (principle 1).

### 10.2 Per-artifact checks

**SPEC feature** — each requirement is *observable*: you could write a check
that passes or fails on it ("results stream as the tree is walked; no modal
wait"), not an implementation detail. The out-of-scope list was written in the
*same pass* as the features, not bolted on later.

**Decision-log entry** — has all of: the trigger (report / measurement /
constraint), the root cause *and whether it was structural or cosmetic*, the
chosen option, **the rejected alternative and the cost accepted**, where it's
enforced, and — when a measurement or a real input drove it — the numbers and
the named fixture. *Missing the rejected alternative ⇒ it's a fact, not a
decision, and a successor can't tell if it still holds.* (Full contrast in §5.)

**Plan** — names the *exact* existing files/types it will touch and their
current shape (not "the diff code"); every feature separates observable UX from
technical design; the **highest-risk item has a named fallback that still ships
something**; every work-breakdown step is a safe pause point with its own
verification clause.

**CHANGELOG entry** — user-facing wording; states the symptom removed or the
capability added; **anchored by a concrete real case**, not a commit subject;
measured impact where it exists; carries *no* design rationale (that lives in
the decision log).

### 10.3 Two more weak → strong contrasts

(The decision-log contrast — the highest-leverage one — is in §5.)

**A SPEC feature requirement:**

> *Weak:* The import flow is fast and handles large files well.

> *Strong:* Importing a 1 MB sample file completes in < 150 ms on CI hardware
> (CI-enforced ⏱). Input is streamed in 64 KB chunks, never fully materialized
> as a single string. A record type that repeats > 64× falls back to grouped
> processing, and the result is flagged "approximate".

The weak version can't pass or fail; the strong version is three checks a
reviewer (or a test) can run.

**A plan's technical-design section:**

> *Weak:* Add inline editing — make the records editable and refresh on change.

> *Strong:* `<EditorController>` currently owns one read-only `<RecordListView>`
> and rebuilds its rendered model through `<RenderBuilder>` after every load. On
> first edit, switch the selected record into edit mode, preserve the selection
> as `(recordId, fieldOffset)`, and restore it after refresh. Recompute the
> derived preview on a 150 ms debounce through the existing generation-token
> path; for ≤ 8 MB input, a full recompute is acceptable (target: p95 < 75 ms).
> *Fallback if p95 exceeds 75 ms:* recompute only the changed record group and
> validate it with a property test that partial output equals full output for the
> affected range. Selection preservation is the highest-risk requirement —
> mitigation: after entering edit mode, update attributes in place instead of
> replacing the editable node.

The weak version is a wish; the strong version names the type, the trade, the
number, and the fallback — a stranger could execute it cold. That is the whole
difference between docs that *look* complete and docs that *are*.
