---
name: build-pipeline
description: >
  Run a non-trivial change by the book — the spec → prove → architecture → prove architecture → matrix →
  test → code → verify → commit & show pipeline, orchestrating the pack's working skills (spec-author,
  product-prover, test-author). Use this whenever starting a new
  feature, a new stateful surface, or a behaviour change that deserves more than a one-line edit:
  "build X properly", "do this by the method", "spec and ship Y", "new surface for Z". It is also the
  entry point for bugs, refactors, docs-only changes, and feature removals — a bug enters at the matrix
  step with a red-on-bug test. NOT for tiny reversible edits (those shortcut straight to code + a test) or pure research/fact-gathering.
metadata:
  version: 2.6.3
---

# build-pipeline — ship a change by the method

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live ONCE in the pack's base skill, `live-spec-base` (v2.6.3), together with the
> settings ladder — this skill references them and elaborates only its own domain. Used standalone, this
> note is plain advice.

One pipeline, each step has a tool. The order is **spec → prove → architecture → prove architecture →
matrix → test → code → verify → commit & show**. A bug shortcuts to **bug → matrix → test → code** (citing the
existing architecture node it lands in). **Skip the pipeline only if ALL hold:** single
file · no new state / element / user-visible behaviour · an existing test level already covers the touched
fact (still ship a test; the order of test and fix follows test-author's small-fix path — red first by
default, and a one-batch fix owes the mechanical red proof). A skip still owes the door step's spec-backed-literal tripwire: does this edit touch a spec-backed literal or clause? A yes routes the docs and the test into the same session as the fix (SPEC INV-104). Anything touching visibility / layout / colour enters at the matrix step minimum.
Otherwise don't skip a step — the bugs that pass every test hide in the steps you skipped. (The private playbook repo's PLAYBOOK.md holds
the principle behind each step. This skill is its executable projection; keep the two in sync.)

**The craft ladder — whose head you wear at each step (SPEC INV-33).** Each artifact is judged by its
own craft's standards: **spec** — a strong product manager (the user's journey, the
product's words) · **prove / prove architecture** — the prover's formal-methods reviewer ·
**architecture** — a software architect (nodes, seams, one responsibility each) · **matrix** — a QA
automation lead deriving coverage · **test** — the same QA engineer writing it · **code** — a senior
developer · **verify** — the visitor's own fresh eyes, the builder's own view set aside · **commit & show** — a careful
release hand whose reader is the human.

The landing report's step accounting speaks in these standards. The hat each artifact was made under is
namable on ask.

The craft wears the work-KIND's face (SPEC INV-22, INV-33): on a prose product the code step is worked as
a strong writer, on infra as a toolsmith. The ladder names the archetypes, and the kind says what their
standards look like in its medium.

## When to run it — and where each kind of change enters
- **Step zero, before ANY tool call: name the door aloud (SPEC T-12, INV-16; base rule 15) — and the human hears the intake line back as the capture echo: heard · door · name · row · place on the map (communicator rule 12; SPEC INV-27, INV-37).**
  - The intake line states size (a wish too big for its worth is negotiated in SCOPE — cut surfaces or
    split into stages, never a time budget or estimate; proposals proceed on the recommended option and
    are surfaced, SPEC T-15) · priority · door: feature · bug · refactor · docs-only · skip · work-kind: product · infra · skill ·
    prose — what the wish BUILDS, one kind per wish, scaling the FORM of every step it walks (the
    work-kind table below; SPEC T-16, INV-22).

    The same line PLACES the wish on the product's feature map — **changes feature X · a new feature ·
    restructure** — spoken in the echo and written in the row's `map:` note. The map is the spec's scenario
    sections plus the architecture's nodes, never a third document. A restructure verdict queues its OWN row
    (refactor door if only structure moves, feature door if behaviour moves too); the re-carve happens only
    through the architecture step and its re-prove (SPEC INV-37). A same-version docs-layout pass rides one sanctioned light vehicle: the pass builds on a clean pushed base, locks the owner's decisions in a checkpoint first, and proves content survived by a word-token multiset check and a punctuation multiset check (SPEC INV-111).
  - **The same line reads the FOOTPRINT — a three-source impact read that decides the route (SPEC INV-128).**
    Beside the door and the work-kind, read the change against three sources at once: the spec (what
    behaviour changes), the architecture (which module owns it), the code (what actually gets touched). Name
    one footprint — **presentation-only** (touches what the audience meets, nothing behind it) · **single-module**
    (stays inside one owned layer) · **cross-cutting** (moves a shared law or several layers) — spoken in the
    echo and written in the row's `footprint:` note beside `door:`, `kind:`, `map:`. **The footprint composes
    with the door, never overriding it:** the door decides which steps run, the footprint decides how far each
    step reaches, and the door's guarantees always hold — a feature never skips the spec step whatever its
    footprint (SPEC INV-16). A cross-cutting change opens the full pipeline from step 1, its architecture and
    matrix work spanning every layer it moves. A single-module change runs the steps its door grants with their
    scope narrowed to the one owned module (its architecture read, its matrix rows, its tests bounded to that
    module's block and interface); a single-module bug or refactor takes the existing matrix-step entry, a
    single-module feature keeps its spec step with the rest scoped down. A presentation-only change takes the
    lightest road its door already grants — the skip boundary or the docs-only door where the door routes it
    there, and the matrix-step minimum focused on the visible layer where it is a visible feature. The
    footprint, not the size, sizes the reach — a heavy process on a light change is as much a defect as the
    reverse. When the three sources DISAGREE (a spec-promised surface with no owning node, code behaviour no
    clause backs, a node pinned to a moved line), name the disagreement and route it to its owner (a bug row, a
    spec fix, a restructure row — SPEC INV-37), never silently trusting one source; the three-source read is
    the verdict derive-before-fork (SPEC INV-121) rests on. The footprint **re-classifies mid-work** the moment
    an edit reaches past its named layer (presentation → single-module, single-module → cross-cutting), the
    landing report recording footprint held or re-classified to X at step N — the sibling of the door's
    mid-work re-fire below. (The mechanical `footprint:`-note suite check [INV-134], the per-kind
    concrete-layers-and-proofs declaration [INV-135], and the cross-cut counter [INV-128 boundary-health,
    `guardrails/crosscut_counter.py`] have landed; the declared-module-interface and interface-level test
    machinery rides its own follow-on row; this step states the read and the routing.)
  - Tripwires decide by rule, ahead of judgment — a new user-visible surface · new persistent state · a new interaction on an existing surface
    · the spec marks the touched surface [target] · behaviour no spec clause backs ⇒ FEATURE, however
    casually asked. The tripwire verdict outranks a casual "bugfix" label, and queue-cutting belongs to the
    bug door alone — a re-doored wish takes no preemption.
  - Re-fire the door mid-work the moment the work is
    about to create a surface or state its door doesn't grant: STOP, reclassify, continue by the right
    door. When the re-door creates a surface or state that did not exist when the lanes opened, the same
    re-check **re-runs the independence edges against every rolling lane (SPEC INV-131)** — the new surface
    can collide with a sibling that was independent a moment ago; a new edge pulls the re-doored lane back
    to serial (waiting behind the lane it now shares a surface with) with a board line, so the departures
    board never asserts a stale independence after the ground moved. The integration re-fence [INV-39]
    still catches the collision at landing; this closes the board's observability gap, not a new net.
  - **A declared mockup-first entry condition is honoured from the row, cancelled only by name (SPEC
    INV-43).** A story whose intake said "show me first, then build" carries the condition WRITTEN in
    its queue row ("entry: mockup-first"); a later general "go build" moves priority, never the
    condition — only by the human naming it does the condition fall. A condition living only in chat
    memory is the defect this line kills (the tlvphoto door was built past its voiced mockup-first word).
  - **One wish = one user story (SPEC T-17):** a wish carrying several distinct things a person will DO and
    SEE splits at intake — each story its own row through the full pipeline (stages slice ONE story's depth,
    T-15's knife; separate stories never fuse into one row). Sub-behaviours (a hover face, a phone face, a
    backpointer) are the story's ACCEPTANCE, folded into the one story. Unclear whether it is one story or
    two ⇒ ask at intake, and every row born of a split cites the one spoken wish it came from. A request to
    merely SEE/TRY with no commitment goes to a labelled prototype home instead (base rule 16) — it stays a
    prototype, outside prod and unshown as product.
- **The door set is CLOSED, and a request enters at the highest document its change reaches (SPEC INV-151).** A request enters at the highest document in the derivation chain — spec → architecture → matrix → code → docs — whose sentences must change to satisfy it; the settings ladder stands beside the chain for a pure value. Walk the chain from the top: after this is done, would any sentence in this document read differently? The first yes is the entry layer, and the request flows down through every step its door grants. The set of entry points is closed — every request kind has a named home and a mandatory back-check, and a request the set cannot place is one plain question, never an improvised route:

  See [references/request-kind-table.md](references/request-kind-table.md) for the full closed set of
  request kinds, their entry step, and mandatory back-check (product behaviour · a technically-phrased request · a defect · docs-only · a tiny reversible edit · a settings/parameter value · an inbox wish · a method/skill change · a sketch · research/a question · a feedback hand-back).

  **A request that matches no kind in this closed set becomes one plain question to the human (base rule 1), never a guessed route.** The closed set is what makes "no gap between the layers" checkable instead of habitual: the landing contract already lists every door-granted step applied or stood down by name (SPEC INV-22), so a request the set cannot place is surfaced rather than improvised. This is the request-side twin of the property net's homeless-item finding (SPEC INV-150), the deferral test's (SPEC INV-152), and the earned message's (SPEC INV-189, INV-191) — one routing principle stated four times (SPEC INV-153): every incoming thing routes to the home whose declared sentence governs it, and a thing that pins to no home is itself the finding. The fourth control carries it across a window's edge: a message to another agent routes to the sender's own blocked work, and a question no work stands on is dropped rather than sent.
- **New feature / new stateful surface / behaviour change:** the full pipeline from step 1.
- **Bug:** enter at the matrix step with a red-on-bug test (`bug → matrix → test → code`); if the fixed fact
  also lives in SPEC prose, update the spec sentence in the same change. **The door step adds one tripwire at the bug door:** does this edit touch a spec-backed literal or clause (a version string, a pinned count, a named vocabulary, a promised wording)? A yes binds the docs-travel-with-the-change rule and the red-first small-fix path into one duty — the docs and the test land in the same session as the fix; the tripwire reads the edit's content, so a one-word change to a spec-cited literal owes the same duty as a full feature (SPEC INV-104). **A confirmed bug drives a class hunt before it closes (SPEC INV-124) —
  four moves, not one:** (1) name the defect abstractly (the KIND of mistake — a scope too narrow, a
  missing guard, an assumption that holds in one place and fails in the neighbour), then actively SEARCH
  every surface where that kind could live and fix all siblings in the same change — the search goes
  finding the siblings not yet seen, the matrix row and the red-on-bug test covering the CLASS beyond the
  single instance (base rule 14); (2) check the architecture — a structural cause (a boundary drawn wrong
  or left silent, a node owning what it should not) updates ARCHITECTURE.md in the same change, a cluster
  in one district reading as an architecture smell; (3) check the spec — a spec silent on or
  under-describing the broken behaviour is the real defect, fixed FIRST so the prover can flag it, then
  the code fix lands under it (the spec-under-describes-composition lesson, generalized); (4) escalate to
  the human when the class boundary needs his read — which behaviours are one class, what the intended
  design was, whether a whole area wants a rethink — the method stops and asks rather than guessing the
  boundary. The four moves are the bug door's close condition; a point fix that leaves the siblings
  standing is a status, never a landing (SPEC INV-26). **A RECURRING bug re-doors to feature:**
  a second bug in the same area within ~30 days is not another patch — the area is missing an INVARIANT,
  so it escalates to the full pipeline from step 1 (spec the invariant, re-prove, then fix under it).
  The journal is how you notice: before taking any bug, grep JOURNAL.md for the area's name and check
  the dates.
- **Removal of a shipped feature is a change too:** spec section → dated REMOVED tombstone · matrix rows
  retired (not left "BUILT") · owning tests deleted · SKILL.md / README swept — all the same session. (This
  is the step that actually got skipped once: an excision cleaned code + tests but left four doc surfaces dangling.)
- **Refactor (behaviour-neutral):** no spec/matrix delta, but enter at step 8 with the FULL suite + the
  visual sample set + a matrix audit of the touched sections (a monolith refactor re-risks everything);
  if the refactor moves node boundaries but leaves the document's shape standing, ARCHITECTURE.md's pins
  update in the same change — the pins-only path is scoped to a boundary shift that leaves the document's
  shape standing. A deliberate redesign (layers restacked, a surface's ownership moved, nodes merged or
  split) is not a pins-only change: the architecture document is re-shaped to the new form and re-proven
  with the architecture lens in the same movement (SPEC INV-113).
- **Docs-only change:** re-read the changed section rendered + one grep that no stale claim contradicts the
  code; no spec/matrix step.
- **A rewrite or restyle accounts for every removal of substance (SPEC INV-109):** the rule's one home is communicator rule 6, which owns the landing report the accounting rides. The docs-only door above and the restyle loop both invoke it — every removed section, argument, rationale, or worked example listed there with its one line of judgment, a removal the rewriter cannot justify raised as a question before the report closes, line-level wording left free.
- **A restructure or migration merged back to main is gated on the delta (SPEC INV-114):** A restructure or migration merge gate judges the delta. It has three parts: load-bearing token identity old-versus-new modulo the per-chunk named deltas plus the punctuation-multiset check (SPEC INV-111); the full suite green on the merged tree (SPEC INV-39); and a full prover pass on both sides whose blocking set is delta-scoped — an unmatched token, a red suite, a new-side finding absent on the old side, or an unnamed meaning change. Pre-existing findings equal on both sides route to queue rows in the same landing and never block. And a session that sharpens a human's spoken bar beyond his words says the sharpened form back and marks it as its own interpretation. The token-identity part scopes to a content-preserving restructure. A deliberate redesign changes content by intent, so it routes by the architecture-redesign law (SPEC INV-113), and its merge stands on the green suite and the delta-scoped prover pass, with no token-identity demand over text the redesign meant to change.
- **Skip entirely** only under the single boundary above (pure research, fact-gathering, a one-file
  no-new-behaviour edit already covered by a test level).

## When NOT to run it

Skip it for the skip-boundary edit (single file · no new state, element, or visible behaviour · an existing
test level already covers the touched fact — it still ships a test, just no pipeline); not for pure
research or fact-gathering (no artifact changes); not for a SEE/TRY ask (that goes to the labelled
prototype home, base rule 16 — and comes BACK through this pipeline only at promotion).

## The work-kind table — WHAT the wish builds scales HOW each step runs (SPEC T-16, INV-22)

The door picks WHICH steps run. The kind picks the FORM each running step takes. The work-kind table
below is the per-kind meanings' ONE normative home (the spec binds the contract around it). The
contract, before the table: at landing, every door-granted step has either **APPLIED in its kind's form
or STOOD DOWN by name** in the landing report ("design-sync — text product, stands down") — a silently
skipped step is a defect. **An unresolved kind scales nothing down** — standing a step down requires a
NAMED kind (the ask rides the row, SPEC INV-12). And no kind ever touches the safety net: the door law
and its tripwires, the delta's mandatory sentences (fences · facets · non-goals · success measure),
ask-at-intake — the same law a scope cut obeys (SPEC T-15).

See [references/work-kind-table.md](references/work-kind-table.md) for the full table of how each step
(1 spec · 2 prove · 3 architecture · 4 prove architecture · 5 matrix · 6 test · 7 code · 8 verify by deed · 9 commit & show · design-sync/snapshot) takes shape under product / infra / skill / prose, including the verify-by-deed VISITOR WALK and FEEL pass (SPEC INV-30, INV-136, INV-139) and the skill-review duty (SPEC INV-99).

## The steps

1. **Spec — invoke `spec-author`.** Write or grow the project `PRODUCT_SPEC.md`: entities, states, transitions,
   actors, invariants, and the cross-section composition between surfaces. One surface = one name. Compose
   every stateful surface across **every** view/mode axis it lives under, not just its own. Real gaps are
   marked `⟨DECIDE⟩` and asked, never guessed. Use human-first language, with codes at line ends.

   A feature-doored wish also walks the **fit walk** — the kind-scaled product-fit interrogation (journey ·
   flows · trigger lenses; lens lists live in spec-author; prover mode FEATURE-FIT; SPEC INV-29) — and the
   **standard-facet sweep** (the canonical list lives in spec-author): phone/narrow layout · touch-vs-hover ·
   empty/error/loading · accessibility · performance. Every facet ends as a spec sentence, decided or
   `[default]`-tagged and TOLD at landing as a plain-words tradeoff, never a confirmation request (SPEC
   INV-31). A mid-work re-door walks the sweep before work resumes (SPEC T-13, INV-18).

   And when the wish touches a surface that already lives, the delta opens with **regression fences** BEFORE
   that sweep — neighbouring promises that must stay true, each citing the clause it guards, named by anchor
   in the wish's row. A fence discharges through the cited clause's existing never-side row, never a new row
   (SPEC T-14, INV-19).

   The delta CLOSES with its two sentences — non-goals ("nothing left out" is valid, a narrowing one is
   surfaced) and one success measure, decided or `[default]`-tagged (SPEC INV-20, INV-21).

2. **Prove — invoke `product-prover`.** The prover only catches a cross-section hole when both sides are
   present and named the same at prove-time — so a surface absent or unlinked then is invisible to it. Two
   modes (see product-prover): **FULL** (all phases, the WHOLE spec — required at MINOR gates and structural
   rewrites) and **CROSS-LINK** (the new surface's seams against the named existing surfaces — on every
   surface add). **Write the findings to the project's `docs/prover/YYYY-MM-DD.md` (in the repo under review, separate from this
   skill's) with a per-finding folded / rejected(+why) column** so "fold every defect" is verifiable after
   a wipe. The next prover run opens by checking the previous file's unfolded rows. Fold every defect by
   the book, and record the recommendations. Resolve every `⟨DECIDE⟩` that the surfaces under change TOUCH (ask
   the human when it's genuinely their call), and list the remaining open ones in the reply so the count is
   visible — don't gate on resolving all of them.

   **Then, when the cadence calls for it, invoke `design-reviewer` over the same proven spec** (SPEC INV-141):
   a second pass right after the prover, judging the design rather than verifying it — it proposes the
   same-kind groupings the text never declared and checks behaviour parity within each. The cadence decides
   whether it runs at all: full on a FULL prover pass, scoped on a surface add, and standing down at
   FEATURE-FIT intake and the push gate (at those two it is not invoked). Every finding is a recommendation or a
   question and never a defect, so it never holds the lane; a confirmed grouping lands as a class clause
   through spec-author, and that class clause **re-enters the prove step** — the prover re-reads it and the
   design review re-reads what it re-partitions, the loop bounded at three progressing rounds and surfaced
   to the human at its cap without holding the lane [INV-154]; only once the loop rests are the tests
   derived. Its strongest likely divergence rides the batched
   questions as one ask with two objects in hand (SPEC INV-142); its record is `docs/design-review/YYYY-MM-DD[-suffix].md`.

3. **Architecture — write or update `ARCHITECTURE.md` from the proven spec** (template:
   `ARCHITECTURE.template.md` — template paths here and in step 5 resolve from the PACK repo,
   github.com/happysasha18/live-spec; a standalone install fetches them there, never from the skill
   dir: the pack is the source, a copy would fork the truth). Named nodes, one responsibility and one name
   each. Every spec fact is OWNED by exactly one node. Named seams run between the nodes. The project's kind
   (`project.kind`, SPEC INV-36) PROPOSES the starting node structure — a fullstack app splits frontend /
   backend / template / store, a CLI one node per command, a skill pack one node per skill — and the
   template's "Node structure by project.kind" table carries the per-kind scaffold; the spec's facts then
   decide the final nodes, a speculative node still being unbacked structure the prover flags.

   In a live codebase every node pins to its owning `file:line`. **This step is where the spec is reconciled
   with reality:** each pin comes from a command you ran, never from the doc's own prose, your memory, or a
   worker's summary — those are leads to verify (base rule 13). Specs drift from code, so fix the spec to the
   shipped truth, always in that one direction.

   A large or surface-class change updates the doc. A bug or small change just cites its existing node and
   skips to the matrix. (Running the pin-greps is junior work; judging what a mismatch MEANS is the senior's.)
   **The architecture owes NUMBERS, not only names (SPEC INV-41):** measurable quality budgets plus
   each budget's instrumentation home — where the real numbers are measured and where a human can
   read them (an export, a debug view, a report). The author also names each budget's watcher: the
   mechanical check that reds past the stated number, or the decided sentence naming why that budget
   is read by eye.

   WHAT is measurable comes from the project's KIND (SPEC INV-36): ask "what does quality MEAN here, in
   numbers?" before writing any. A user-facing product measures paint/interaction times ("first image
   within 2 s on a cold visit"); a backend service latency, throughput, error rate; a CLI or pipeline run
   time on a typical input and per-unit cost; a skill pack its evals' pass rate and suite wall-time; prose
   what honestly HAS a number. A quality with no honest number is SAID by name, never given a vanity metric.

   Each budget is asserted by a matrix-row acceptance, never a hope in prose. A surface with no budget line
   and no instrumentation home is a derivation defect, exactly like an unowned fact. The numbers are the
   host's taste: propose with a recommendation, set on the human's word at the surface's first budget
   landing.

   **The doc owes two more views beside the node map (SPEC INV-74, INV-75), scaled by kind:** the
   **runtime view** walks every flow the spec promises through the nodes — which node serves each step,
   what crosses each hop (citing the seam by name; the payload and format stay the seam table's fact),
   where the flow can fail; a flow the doc cannot walk end to end is a finding. The **placement view**
   states every node's place — build-time on the author's machine · CDN static · client browser · edge
   worker · external service — plus the load-bearing technology choice where one exists, first-class (a
   node-table column or its own small table), so the reader answers "where does this run" at a glance.
   The per-kind flow unit and both section shapes live in the template; a book satisfies each view with
   one sentence.
   **The doc is ITERATIVE, current only to what's shipped or in flight:** it maps the product as it stands
   plus the landing in flight. A node exists for what ships today, or for what the spec already promises
   under an owned queue row (marked [target], pin empty).

   A future feature earns its node when its landing arrives. A speculative node is unbacked structure — the
   prover flags it. "Should I architect the next few milestones now?" is answered NO strictly by the method,
   taste playing no part.

   **Every new or carved node passes a three-question fitness test at its birth (SPEC INV-122):** can it be
   tested alone · does a real second place need it · can it and its neighbour be worked in parallel without
   queuing on shared files — three yes answers make the node right, a single no is a flag to answer (name the plan that turns it to a yes, or fold the carve back), and two or more no make it premature. The
   test's first home is here, the architecture step, where new abstractions are born; a carve that fails it
   is folded back into its caller until a real second need or a real testability gain arrives. Its second
   home is product-prover, extending the speculative-node flag: a node with one caller and no promised
   second is flagged for that answer (the one-no case), never auto-rejected.

   Re-carving the whole node map IS legal: it arrives as a restructure placement's own queue row (SPEC
   INV-37), walks this step, and is re-proven like any structure change. A placement may SAY the shape no
   longer fits; only a landing changes the shape. **When structure is deliberately redesigned — layers
   restacked, a surface's ownership moved, nodes merged or split — the architecture document is re-shaped
   to the new form and re-proven with the architecture lens in the same movement (SPEC INV-113). Updating
   the pins alone is scoped to a boundary shift that leaves the document's shape standing; after a real
   redesign the old shape itself lies, so fresh pins on a stale shape are a defect.**

4. **Prove the architecture — invoke `product-prover` with the architecture lens** whenever the doc
   changed in step 3 — six checks, each at the project's kind scale: every spec fact has an owning node ·
   no node stands without spec backing · every seam names what crosses it and who owns the format · the
   quality budgets are stated with their instrumentation homes, each naming its watcher (INV-41) · the runtime view walks every
   promised flow (INV-74) · the placement view says where every node runs (INV-75). Findings land in the
   same `docs/prover/` record discipline as step 2. A full pass at an M-1 or M-6 gate that proves
   ARCHITECTURE.md beside the spec (INV-116) also **appends its dated row to the Prover record** table in
   ARCHITECTURE.md, so that table tracks the architecture's freshness rule instead of drifting behind it.

5. **Test spec — invoke `test-author` to DERIVE `TEST_MATRIX.md` from the proven spec through the proven architecture (the method's one home, SPEC E-27).** The
   matrix is derived, never just filled: rows organized **architecture node × spec fact** (one block per
   node), every fact gets ≥ 1 row, **every row states BOTH sides — what the fact DOES and what it must
   NEVER do** (the never side IS the regression fence, SPEC INV-6; a row without it is a derivation
   defect), and **every row pins a test LEVEL** (string / DOM-text / browser-computed / pixel). Any fact
   about visibility / layout / colour / interaction gets level ≥ browser-computed.

   It opens with an **artifact inventory** — every file the user receives — and every inventory entry owns at
   least one rendered-level row. Derivation CLOSES with the template's **coverage validation checklist,
   actually walked** (every anchor ≥ 1 row · every node's negative-side rows exist · no stale refs). A fact
   with no row or at a too-weak level is a derivation defect, fixed here.

   The matrix is the bridge: tests come from the matrix, upstream of the code. (The mechanical projection is
   junior work; choosing each row's level + assertion is the senior's.)

6. **Test — with `test-author`, write tests that assert the REAL shipped artifact.** Render the widget / produce the file /
   call the function and inspect the output as real behavior, apart from any source-string match. Watch the new test FAIL first
   (red-on-bug), then implement. Never edit a test just to make a change pass.

7. **Code — implement until green.** Delegate well-scoped, mechanical implementation to a junior worker
   with a precise brief + a persistent checkpoint file (so a cut-off resumes rather than restarts). Keep the hard
   parts (ambiguous specs, design, tricky debugging) on the senior model. Verify the junior's result by deed.

   **A norm-pointered surface builds with the artifact open (SPEC INV-43):** when the surface's spec clauses
   carry a `norm: <path>` pointer, OPEN the artifact before building — the frozen prototype is the norm for
   look and feel, the clause text only its laws — and record a one-line plan-vs-prototype diff in the
   landing's accounting. A missing diff line is a defect at review. The verify step's feel bar (step 8) reads
   the same pointer.

   **Taste-heavy deliverables build smallest-first (SPEC INV-62):** when taste rules the deliverable — voice,
   copy, visual style, spec prose — STOP at the cheapest judgeable sample (one paragraph, one card, two
   sections) and take the human's word on it before the full build spends anything. Five full packs once died
   on a failure a one-paragraph sample would have caught.

   **And a rejected artifact reopens its SOURCE (SPEC INV-63):** the fix starts at the spec clause / card /
   brief that produced it — correct the source, then rebuild from it. Line-patching the rejected output
   against an unchanged source is the five-round trap, banned.

8. **Verify by deed.** Run it and see the result with your own eyes. Only call it done/working after that;
   otherwise label it an assumption.

   Run every check the diff can reach before any push — the reach map's law (SPEC INV-45): a prose-only diff
   runs the doc gates whole and says so. Any code, spec, matrix, skill, or test file in the diff means the
   whole suite.

   **Green = zero failures AND the skip-set is exactly the expected pinned list** — an unexpected skip
   (Chrome absent, a real-data fixture missing) is a FAILURE outright. **If red at a pause / session end:
   never commit; write the failing test name + hypothesis as the top `NEXT_STEPS.md` item** — the checkpoint
   IS the red test.

   **Green also means DETERMINISTIC (SPEC INV-155).** A test that passes only sometimes is a defect, not a
   pass. A flake whose root is in owned code — the test or the product — is fixed at that root: name the
   nondeterminism (wall-clock time, ordering, shared or leaked state, an unseeded random, a missing wait on a
   tool the test drives) and remove it, so the test passes every run for the same reason. It is masked by
   nothing: never a retry, never a rerun-until-green, never a raised timeout that hides the race, never "it
   passed this time" taken as a pass. Only where the nondeterminism is not removable in owned code — the
   external tool itself misbehaving at random — is it workshop noise on the problem ledger [SPEC INV-23], a
   separate home. Green means deterministic.

   **The audit — a second pair of FRESH eyes, REQUIRED where the stakes are high and only the
   author has judged the work (SPEC INV-46).** An audit is adversarial by nature: a whole-read that sets
   out to break the work, refute its claims, and find its holes. Verify runs a fresh-context checker when the change is
   HIGH-STAKES and its only review is the author's own. High-stakes means one of two things: the delta is
   surface-sized (a new surface or a multi-file behaviour change), or the change edits the method itself — a
   rule whose MEANING changed, a new or re-scoped invariant (a wording-only edit that changes no rule's
   meaning is not a method edit). The author's own review means no independent read has happened, where an
   independent read is a differently-contexted head briefed from the primary sources on the "goal missed"
   hypothesis; a prover pass in the author's own context never counts as one, and delegation never makes the
   review independent — the same head that briefed the worker reads the result. One fresh checker per landing
   batch covers every law in the batch (SPEC INV-61 scales the audit's form, never its freshness). Brief the
   checker with the SPEC sentences the landing claims (the anchors) and the artifact paths — primary sources
   only: never the worker's summary, never the senior's own plan. Its opening
   hypothesis is "tasks completed, goal missed". It walks each claimed fact up the ladder exists →
   substantive → wired → flows, and greps for stubs: TODO · FIXME · placeholder · lorem · hardcoded sample ·
   empty function body.

   Findings become rows or red, never a nod, folded before the landing commits. The checker is a worker
   under the full contract (checkpoint, ledger, clock), and its verdict rides the landing report. Anywhere
   else the checker is the senior's option. A skill or prose landing walks the ladder in its kind's form:
   the checker re-reads the SHIPPED text against the spec sentences.

9. **Commit & show.** Commit when green with no regression (unasked) — same or better is enough, never wait for perfect. Where the host has a remote, PUSH accepted work there by rule (SPEC INV-82): every gate the diff reaches ran and passed (the verdict read from the suite log's own line), plus the host's own push lines; the remote is discovered from the tree, and only a host with no remote gets one contextual question at the first push moment (create one — GitHub, GitLab, whatever the human names — or stay local, recorded in the host profile). Every push re-walks the README against the pushed truth — crisp and current, a stale claim fixed before the push (the shopfront law at every-push cadence). After the push the push step reads the remote gate's own verdict (the CI run the push triggered, one `gh run` read), and a red verdict is the pushing session's own immediate bug: fixed and re-pushed the same session before anything else, so the human never meets the red first in a GitHub email; a slow gate is watched to its verdict on the detached-work cadence (SPEC INV-106, INV-35). The human's personally named gates still wait for his word. Bump the version, PATCH by default; the number reports what taking the release costs a host, and the tier is read off that cost — a patch fixes a machine to hold a law already stated (the host does nothing), a minor grows what a host may adopt by re-running its catch-up walk with nothing rewritten, a major forces a host action and ships its dated MIGRATION.md chapter (base rule 32 / SPEC INV-217). The minor-versus-major call is a stated judgment the releasing session makes and names, held by no gate.
   Docs travel with the change — README + CHANGELOG + the skill's own `SKILL.md`, same session. Diary the WHY
   in `JOURNAL.md`.

   **The CHANGELOG speaks to the USER, the journal to the builder:** each entry says what changed for the
   person using the product, with one concrete example from real output, in outcome terms only. Function
   names, internal ids, and row numbers live in the journal instead. And no doc pins a drifting version
   number in prose — "current version: vX.Y" always goes stale. Point at the version's one home (the VERSION
   file, the frontmatter) or omit it.

   The landing report TELLS the taste choices made without asking — the open `[default]`s — each in plain
   words with an example and a tweakable mark. No confirmation is requested; silence is consent, never
   re-asked (SPEC INV-31). The same TELL covers a tunable parameter you set to a sensible default — a
   resolution, a batch size, a timeout, a sampling rate — named with what it trades, tuned together later at
   most, never a stall on a knob you can reasonably pick (SPEC INV-70).

   A landing report, a ROADMAP row, and a decision page are exactly the surfaces where a decision gets
   recorded AS the person's, so base rule 13's writing rule on human authority binds them (SPEC INV-207).
   A `[default]` the seat picked is the SEAT's own judgment and is written in the pack's own voice; it is
   never dressed as the human's word. When a decision genuinely IS the person's, the entry names the
   exchange it came from — a date a reader can check — and an anchored copy goes to `DECISIONS.md`, the
   read-back set the human reads on his own clock and strikes what he never said. An autonomy grant
   authorizes the seat to decide; it never authorizes recording that decision as the human's.

   Show the human the REAL render in a new window; push or deposit only after they've reviewed it. A push
   re-renders all deposited artifacts, and a push shipping a new version walks the publish skill's shopfront
   check — README claims + kind-owed visuals fresh, the outcome line riding the landing report (SPEC INV-44).
   Where the host's design-sync is ON (base defaults; SPEC E-18), the landing's DECLARED components also sync
   to the team's design project — after the human's gate, never instead of the in-session show.

## Guardrails — the pipeline's TEETH (mechanical, every project inherits them)
The eight steps are guidance, and an agent DRIFTS from guidance — that is the failure that stops a project
converging (a whole panel ships empty; a behaviour nobody asked for gets buried; a change lands with no test).
So the pipeline is not trusted, it is ENFORCED: a `guardrails` check the project wires to a **git pre-push
hook** (+ the suite), so a change that fails ANY of these is RED and CANNOT be pushed. `test_traceability`
(below) is the first of these — generalise it to the full set. **Each project INSTANTIATES the checks for its
own surfaces; the pipeline REQUIRES the check exists and is green.** This is a first-class step, applied project-wide
rather than as a per-project patch. See
[references/guardrails-catalog.md](references/guardrails-catalog.md) for the four mechanical guardrails
(Completeness incl. cross-surface policy uniformity SPEC INV-125 · Tests-present · Behaviour-traces-to-spec ·
Conflicts).
**Honest boundary:** guardrails catch STRUCTURAL defects (empty surface, missing test, untraced behaviour,
partial artifact, id/naming conflict). They do NOT catch a subtle SEMANTIC bug (is the number right?) — that
still needs `product-prover` + a human's eyes. Enforce structure mechanically, and reason about meaning with
the prover. Verify-by-deed (step 8) and commit/push (step 9) both run the guardrails first, so guidance and
teeth agree.

## The excuses table — read it the moment one of these crosses your mind

The shortcuts that kill the method never announce themselves; they arrive as one of these thoughts.
Each is a tripwire: thinking it means STOP and take the pipeline door you were about to skip.

See [references/excuses-table.md](references/excuses-table.md) for the full table of six excuse-thoughts
and why each is a trap (SPEC T-12, T-15, INV-4, INV-5, INV-15).

## Gates worth remembering
- **Before a MINOR (0.x.0) bump:** the 3-pass preventive audit — product-prover on the whole spec + a matrix
  audit + a surface-composition check, plus the full design review (SPEC INV-141) and the cross-cut counter
  (SPEC INV-128, INV-37) and code compaction as a station beside doc compaction (SPEC INV-123). See
  [references/minor-bump-gate.md](references/minor-bump-gate.md) for the full gate procedure.
- **Compaction runs every pass, above the milestone gate (SPEC INV-164):** the doc- and code-compaction
  stations run at every push, above the MINOR gate that once held them alone. Every push is held to the
  reached-clean floor by the mechanical gates — the register lint at zero errors, the redundancy gate at
  zero open pairs, and the debt cap that only ratchets down (`scripts/spec-debt-cap.json`) — asserted
  against the live document by the suite, so no bloat accumulates between milestones. The deeper method
  rule (base rule 30): any quality a machine can verify is shipped as a runnable gate a host attaches,
  held by no pass's attention, since a quality left to attention is a defect of the method. This is the
  fix for the spec bloating when compaction ran milestone-only (2026-07-15).
- **Process bookkeeping scales to the delta (SPEC INV-61):** the pre-push re-check keeps its rigor and
  scales its FORM — a small delta (skill/prose/infra kind, no new surface, no structure change) ships a
  three-line SHORT-FORM record (previous records clean · the delta in one line · the verdict). A
  surface-sized or structural delta keeps the full walk. Claims batch per declared lane, and the journal
  chapter and the resume rewrite come once per landing batch. Never scaled: the law's own text, the
  red-first test, the delta's prove, the gates.
- **Order is law:** `spec → prove → architecture → prove architecture → matrix → test → code`;
  `bug → matrix → test → code`. Never code first and back-fill a spec — and never jump from spec straight
  to tests: the two layers between them (architecture, test-spec derivation) are where whole classes of
  holes get caught (SPEC E-14/E-15/INV-15).
- **A row closes only whole (SPEC INV-26):** where a row carries several legs, its Done-when enumerates
  each, and the landing report may close the row only with EVERY leg met —
  half-done is a status, never a landing. An open leg keeps the row in-work, and the resume file's LIVE-STATE restates it at every
  supersession, never compresses it away (still open at compaction ⇒ restated in full).
- **Trains, one pen (SPEC T-18, INV-39):** one session may roll up to the profile-declared lane cap of
  INDEPENDENT build lanes without asking (`lanes.cap`, package default three [E-13]; the owner's
  2026-07-06 value three in his profile; one more opens only on the human's asked word, never silently) —
  pairwise independent: no shared surface, no shared spec section. Opening each lane is narrated, and
  every train rides the departures board, a waiting lane naming whom it waits behind. Only penless
  stages overlap: a later train's code and tests in its own isolated tree (its delta integrates only
  under the pen; the disjoint-file road stays within one lane), read-only analysis free.

  Every shared-doc edit, the integration, and the closing of a row take the pen one lane at a time — a
  pen-stage is never cut mid-edit — and a landing commit carries exactly one row's delta, its gate run
  on a tree clean of the other lanes' unfinished work. After a landing, waiting lanes re-fence and
  re-run their gates on the new truth. Never across sessions, never mid-milestone. A bug takes the pen
  at the end of the current pen-stage and parks every rolling lane, each at its own checkpoint,
  resuming in landing order.
  **Lanes are picked by a graph, never by mood (SPEC INV-49):** at queue-take read the runnable head
  and build the mini dependency graph — an edge wherever two rows share a surface, a spec section, a
  skill file, or a doc region. Open lanes on a pairwise-independent set up to the cap. Rows that
  collide only at integration pre-roll isolated build stages with the landing order DECLARED at claim
  (first-declared lands first, the later re-fences). Tiny rows ride serial — parallel pays only when
  build stages dominate the pen work — and the chosen set, the order, and a said-aloud "serial by the
  graph" are board lines. The same queue-take also re-scans every deferred row's revisit trigger against
  the current moment (SPEC INV-129): a time-bound trigger can come true and lapse between two milestone
  gates, so the milestone re-scan is not its only reader — a fired trigger returns its row to the runnable
  head right then, so a deferred wish never waits on a trigger nobody reads whichever cadence comes first.

  **Opening a lane is an act you PERFORM (SPEC INV-214):** once the graph picks a
  pairwise-independent set of two or more runnable rows with lanes free under the cap, open each one — do
  not fall back to single-file. The act, `scripts/open-lane.sh <row> <slug>` or the same walk by hand:
  stage the row→in-work flip in the queue, run the script to fence-check, refuse a lane past the profile
  cap (`lanes.cap`, default three), commit that flip alone to main under the pen (the one-row claim
  commit), cut `lane/<row>-<slug>` from it into its own worktree under `.claude/worktrees/`, and print the
  worker brief stub naming the branch. Then delegate the lane with the Agent tool's `isolation:
  "worktree"` option (it carries no gate, usable today), the brief naming the branch its work rides. Going
  single-file while independent lanes stand free is a recorded choice: say the "serial by the graph" board
  line and name why (the rows collide, the cap is full, the rows are tiny, or a dependency orders them).
  That recorded reason is a discipline you hold, since no gate can judge whether two rows were independent
  and owed a parallel lane — that judgment is the graph itself, a senior read (SPEC INV-49, INV-214).

  **The drafter-applier pipeline is the standard colliding-rows form (SPEC INV-49):** on colliding rows
  the penless DRAFT stage overlaps the current landing, a drafter worker preparing the next row's exact
  edit strings while the applier lands the current row under the pen. See
  [references/drafter-applier-example.md](references/drafter-applier-example.md) for the drafter's
  self-verify list and the 2026-07-12 worked run [T-18, INV-39, INV-49].
- **Junior delegation (decided from the request, BEFORE the first tool call, SPEC INV-69):** judgment work
  (spec, prove, architecture, matrix-level calls, findings triage, any taste call) stays senior; mechanical
  work (known edit strings, a known command, fan-out fact-gathering, a report or list or dump to produce)
  routes to a worker at the cheapest tier that can pass the brief, proposed and logged, the senior free to
  override aloud. The brief is self-contained (the BMAD story-file lesson) and SIZED, born from reading the
  touched files in full with three recorded lines per file (SPEC INV-53/54/55), and closes on a HALT list
  rather than guessing past ambiguity. The worker contract (SPEC ACT-3) narrows write-ownership to the
  brief's named files; the senior owns write-set disjointness between concurrent same-session workers before
  spawning them, or gives one an isolated worktree (SPEC INV-105). The brief carries the problem-ledger path
  for workshop noise (SPEC INV-23) and the clock for every stamp (SPEC INV-24). And the brief carries the
  cleanup-safety constraint so a worker never reinvents a broad kill: a cleanup acts only on what the run
  provably owns and never a shared resource in current use — a kill targets the test resource uniquely (a
  recorded PID / process group or an install path like `~/.cache/puppeteer/...`), never a broad name pattern
  (`pkill chrome`, `chrome_crashpad_handler`) that can match the human's own program (SPEC INV-162, base
  rule 17; the footgun that once closed the user's real browser). Every delegation reports its
  saving in the landed row's status cell, checked by suite (SPEC INV-103), and names the reads dispatched
  beside the work delegated (SPEC INV-137). See
  [references/delegation-protocol.md](references/delegation-protocol.md) for the full protocol: the routing
  rule, the brief's three birth laws, the worker contract, and the delegation-reporting duty.
- **Traceability is a test, enforced automatically.** A standing `test_traceability.py` fails the suite on a matrix row
  citing a missing test, a duplicate invariant id, a spec invariant with no matrix row, or a ⟨DECIDE⟩ marked
  RESOLVED that still carries the live marker — so drift is caught every commit, continuously rather than once per MINOR.

## How it relates to the other skills
- `spec-author` — writes/grows the spec (step 1). Public.
- `product-prover` — reviews the whole spec with formal-verification thinking (step 2). Public.
- `design-reviewer` — a second pass right after the prover (step 2): judges the design, proposes the
  same-kind groupings the text never declared, and echoes the strongest likely divergence to the human;
  recommendations and questions only, never a block. Public.
- `test-author` — derives the matrix and writes the tests (steps 5–6). Public.
- `build-pipeline` (this) — the orchestrator that sequences them through to a shipped, verified, committed
  change.

> The method, made durable: spec-author and product-prover each own one step; build-pipeline is the spine that
> runs the whole arc from a spec to a shipped, tested, committed change.
