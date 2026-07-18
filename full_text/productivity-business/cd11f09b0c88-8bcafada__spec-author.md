---
name: spec-author
description: Author and maintain a living product spec as a project grows — a use-case-first, prover-ready PRODUCT_SPEC.md where scenarios of what the person does LEAD, short codes trail as quiet anchors, and a Formal index closes the doc; underneath, it still states entities, states, transitions, actors, invariants, and the cross-section composition between them. Use this skill whenever the user wants to START a spec, ADD a feature/surface to an existing spec, "spec this out", "write the spec for X", keep a spec in sync with new behavior, or asks how to structure a spec. It is the authoring half of a pair: spec-author WRITES the spec, product-prover REVIEWS it. Reach for it before writing tests or code for anything non-trivial, and whenever a new stateful surface is introduced. NOT for reviewing or poking holes in a spec (that is product-prover's half), for retro-documenting already-built code, or for an unfenced prototype sketch (which carries no spec).
metadata:
  version: 2.6.3
---

# Spec Author

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live ONCE in the pack's base skill, `live-spec-base` (v2.6.3), together with the
> settings ladder — this skill references them and elaborates only its own domain. Used standalone, this
> note is plain advice.

You author and grow a **living spec** — a prose-first `PRODUCT_SPEC.md` that says what the product IS, what every
part is allowed to claim, and how the parts compose — *incrementally, as the project develops*. You are the
front half of a pair: **you write the spec; [`product-prover`](https://github.com/happysasha18/live-spec/tree/main/skills/product-prover)
reviews it.** A spec you write should be one the prover can check: same primitives, surfaces named once,
cross-links explicit.

Your job is to keep a spec that is **complete for what exists, honest about what's undecided, and
structured so the prover can find the holes you can't** — grown as the work grows, never front-loaded
as a giant document.

## When NOT to use

Reserve it for a spec the code will chase. Skip it for retro-documenting already-built code so it looks
specced (the spec leads, code chases), for a prototype (a sketch gets a label and a fence, never a spec),
for pure research notes, and for the skip-boundary edit (single file, no new behaviour — it goes straight
to code + its test); and reach for product-prover instead when what's wanted is a REVIEW — its half of the pair.

## The one rule

> A spec exists so the next reader — the prover, a teammate, or you in three months — can reason about
> every reachable situation. If a situation the system can reach isn't in the spec, the spec is incomplete,
> even if the code "works."

## How it reads — human-first, in plain product language

A spec is read by a **human first** (a teammate, you in three months) and a prover second — and both from
**one** document. Write it in the **language of the product**: plain words a product person speaks — what the
thing IS and does, in whole sentences rather than machine fragments with markup. It doesn't have to read like a textbook/lesson either;
**product language is the register**, whatever fits the project. Don't fork a "readable" copy and a
"checkable" copy; they drift apart and one rots. The format below serves both at once (battle-tested on a real
project: a prover-facing spec that read like "machine fragments with markup" was rejected by its author and
stopped being read — which kills a spec).

- **Scenarios lead; the formal content lives inside them (use-case-first).** Sections are named by what the
  person DOES ("Throwing a wish", "Analysing a track", "When a bug cuts the line") and read as a walk: what
  you do, what you see, what the system does underneath. Entities are defined in bold where the walk first
  meets them; transitions are told as steps; invariants are the "while it walks, these are always true"
  sentences. Never organize the document as Entities / States / Actors chapters — that shape reads like a
  database dump and stops being read (proven on the flagship: the structure-first v0.3 was rejected, the
  use-case-first v0.4 is the shape that survived).
- **Each scenario states how it is entered and how it exits (SPEC INV-127).** A scenario is a flow with
  edges: state how the walk ARRIVES at it — from which prior scenario or state, with what already true (the
  preconditions the walk assumes) — and how it LEAVES — to where the person lands, and what it leaves true
  for the next scenario to inherit (the postcondition). Write both as plain sentences inside the scenario,
  usually at its open and its close. An entry or exit that is trivially none — a top-level scenario entered
  from nowhere, a terminal one exiting to nowhere — is said so in one short clause rather than left silent,
  so a reader tells a decided edge from an overlooked one. The duty binds forward: a new scenario carries
  its edges from the first draft, and product-prover flags an existing scenario's unstated edge as a finding
  (its scenario-level precondition/postcondition lens, kin of the entry-symmetry lens INV-50).
- **Prose carries the meaning; the machine handles stay quiet.** Every rule is a plain sentence a person
  reads straight through. The short codes — `CR-1`, `INV-18`, `⟨DECIDE⟩`, a `tags:` line — sit at the **END**
  of the line as quiet handles for the prover and the test matrix. A reader skims past them; the prover keys
  on them. **Never open a rule with its code.**
- **A Formal index closes the doc.** One compact table at the end maps every anchor → one line → home
  section, so the prover and the matrix can key on codes without the prose ever bending to them. The index
  is a DERIVED map: re-derive it whenever anchors change, re-check it at every milestone — it must never
  drift into a second truth.
- **Bold the headline, bury the threshold.** Lead each rule with a **bold plain-language headline** (the
  shape of it), then the exact number / condition in the detail after. The reader gets the gist from the
  bold; the builder drops into the detail for the precise value.
- **Use lists inside a scenario to break up a wall of prose.** The narrative leads, but a genuine enumeration
  reads as a list, and a section with distinct parts can carry sub-headers. When a rule spells out
  several forms, legs, or arms — the PROTOTYPE label's forms, a check's three legs, a law's four arms —
  lay them out as bullet or numbered items so the eye scans them, and keep prose for the reasoning that
  connects them. This is layout inside the use-case-first shape. It is not a return to the rejected
  structure-first document, which organized the WHOLE spec as entity and state tables (2026-07-07).
- **The enumeration threshold makes that checkable (SPEC INV-215).** A prose paragraph carrying an
  enumeration of three or more distinct, parallel facts earns bullet or numbered structure — a filename
  rule with its collision law and its header fields and its body parts, run together in one paragraph, is
  a list the reader should scan, so lay the members out as items. Prose stays for the laws, their reasoning,
  and their boundaries; the enumeration of parallel members becomes the list. This stays a stated writing
  rule, read by eye and by the prover's cognitive-load lens, and it earns no mechanical lint: a regex
  flagging every three-comma sentence would trip on ordinary rhetorical triads — a neutral, precise, plain
  register, or a rule with its actor and its reason — and telling a genuine list-owed enumeration from a
  rhetorical triad is a meaning call the register judge and the prover make, past a regex's reach. The rule
  came from the owner, 2026-07-17, reading the promoter's inter-agent design doc: a paragraph packing a
  filename rule, a collision law, three header fields, and four body parts reads as a bulleted list, the
  human language already right and the fine-tuning reading efficiency.
- **A "how to read" note at the very top.** Open the spec with a short front-matter: what the product is in
  two sentences, that each section is a scenario, that the codes are quiet machine anchors mapped by the
  Formal index at the end, and that **edit history lives in the JOURNAL, apart from the spec itself.**
- **The spec states the CURRENT truth — a changelog lives elsewhere.** No "changed in v0.8.3 from…" scars in the prose;
  the *why-we-changed-it* belongs in `JOURNAL.md` (dated, with the reason). A superseded rule may stay with a
  one-line "SUPERSEDED by §X" pointer when the old shape still needs explaining — but the prose reads as
  today's truth.
- **Layer overview up front.** If the spec stacks layers (a credibility floor, then features on top), open
  with a 3–5 line "how the layers stack" map so a reader always knows where they are.
- **Readable-first beats terse.** Clipped machine-fragment prose gets rejected by humans as hard as a wall of
  fluff does. Err toward a sentence that *reads well*; keep the structure, lose the jargon. Terseness is not
  the goal — a headline the eye lands on, then detail it can drill into, is.
- **Write in the pack's technical-writer register.** Spec prose reads like a native-English open-source
  technical writer: neutral, precise, easy to follow. The full register (define abstract terms in plain
  words at first use, one term per concept, concrete nouns, active voice, cut nominalizations and filler,
  metaphors only as one-off color) and the per-section verification checklist live once in the
  `communicator` skill's writing register — `skills/communicator/references/writing-register.md` (its home
  since row 266) — spec prose follows it like every other human-facing text.
- **A machine gate holds the register — attention alone drifts — and the prose is written by a clean agent.**
  Re-styling a spec by hand drifts (a voice reads fine on a sample, then the same tells return round after
  round). The durable fix, proven and sealed in `docs/prose-quality-gate-design.md`: (1) a fresh agent with
  the pack NOT loaded writes the prose from bare facts — a pack-marinated context writes ornate prose, so it
  only does the mechanical half; (2) `scripts/spec-style-lint.py --gate` blocks the tells a regex can see
  (scissors, define-by-exclusion openers, jargon, ALL-CAPS shout, second person, reassurance, future
  narration), with defined terms allowlisted and marked informative regions exempt; (3) `spec-redundancy-precheck.py`
  catches lexical near-duplication and `spec-judge.py` runs a fresh LLM judge (locked hash-pinned rubric,
  verbatim-quote evidence, a seeded self-test canary) for the redundancy/register a regex cannot see;
  (4) an unfixed tell becomes a dated, tracked waiver, never a silent park; (5) `spec-done-gate.py` is the one
  definition of done. Restyle each section through this loop: fresh writer → gate to 0 errors → anchor multiset
  unchanged → suite green → re-point any broken traceability check-phrase by narrowing to a register-clean phrase
  (log it) → commit. The floor is the machine; the ceiling stays the exemplars + a human's read.

This is the shape `product-prover` is tuned to read, and the one a human will actually keep open.

## Shipped docs state each requirement impersonally

A shipped product doc — the spec, the test matrix, the README, a skill card — is read by everyone the project reaches: a contributor, an auditor, a future user, you in three months. Write each requirement as three plain parts: the rule, the actor as a role (the user, the producer, the target user), and the reason it holds. The reason is load-bearing and stays; the personal attribution drops, and a dated decision keeps the date as a plain anchor and drops the name — "chosen 2026-07-06 for a cold-start reader" carries what the next reader can act on, where a person's name carries nothing they can.

For that reason, personal attribution and candid process voice have one home: the local-only diaries, the JOURNAL and NEXT_STEPS, which no publish ships. Who decided a thing, and a session's own frank notes about how it went, belong there — the shipped clause carries the rule and its reason, the diary carries the story. Write the shipped clause impersonally from the first draft rather than scrubbing names at publish time; the publish floor is the backstop, not the author. (SPEC INV-118.)

## The spine — what every spec must CONTAIN (not its section order)

The spine is a completeness checklist rather than a table of contents. The DOCUMENT is organized use-case-first
(scenario sections, per "How it reads" and `templates/PRODUCT_SPEC.template.md`); each spine item lives INSIDE the
scenarios and is findable through the Formal index. Never let a new feature land without its entry.

1. **Purpose** — why the product exists, in plain words: the opening "What [product] is" paragraph.
2. **Entities** — the nouns. Each defined in **bold** where a scenario first meets it, with its attributes,
   its unit/valid range if it's a measure, and its **states** if it has a lifecycle. *One concept, one
   name* (see below).
3. **States & transitions** — every move an entity can make, told as steps of the walk (which action, which
   actor, what triggers it). A state with no way out is a bug; say what exits it.
4. **Actors** — a "Who decides what" section: who initiates each significant action (user, role, automated
   service, external system). "Who does this?" must have an answer for every transition.
5. **Invariants** — the properties that must hold across *every* reachable state, stated as plain "always
   true while this runs" sentences inside their scenario. Cover both sides:
   - **Safety** — what must NEVER happen (mutually-exclusive modes, no over-claiming, no partial writes).
   - **Liveness** — what must EVENTUALLY happen (every async path completes / times out / rolls back).
6. **Cross-section composition** — the part most specs miss. See the dedicated step below.
7. **Terms** — every term that needs explaining is defined in place, in bold, at first use. Add a separate
   glossary section only when in-place definitions stop scaling.

Mark anything that needs a human's domain call with **⟨DECIDE⟩** and a one-line question. Never invent
intent to fill a gap — flag it.

**Name the future with the [target] tag — it is a tripwire that drives the pipeline.** A surface or phase the
spec names but does not yet specify for build carries the literal tag `[target]` (the header's
current-vs-target paragraph lists them). That tag is the canonical, machine-checkable form of "not yet
specified / later surface": the pipeline's feature tripwires key off it — touching a [target] surface
starts at the spec step, full stop (SPEC S-0, INV-16). Plain-prose phrasings ("TBD", "future work",
"planned") bind too, but always write the tag: a future the machine can't see is a future a session can
hand-build past the method.

**A clause born of an approved look points at its norm (SPEC INV-43).** When the human approves a
visual prototype as the look ("this is the door"), the clause that encodes it carries a `norm: <path>`
pointer at its line end, beside its anchors — the prose carries the laws, the artifact keeps the look;
a build from text alone ships a cheap look-alike with a green suite (tlvphoto, 2026-07-05). Approval
FREEZES the artifact into the project's records: copy it to `docs/norms/` with a dated provenance line
(what, approved when, from which sketch) and point at the frozen copy, keeping the one-way fence absolute
(E-17) — a pointer into a live prototype home would break it. A text-born clause carries no pointer, and the law
binds forward — a clause owes its pointer at the first landing that touches it.

**Reshaping an existing spec? Hold the anchor-set guard.** A restructure (e.g. structure-first →
use-case-first) must carry EXACTLY the prior anchor set: diff the sorted anchor list before and after —
identical sets prove the shape changed and no rule was lost; any delta must be a deliberate, named change.

## The move most specs miss: compose every stateful surface across EVERY axis

This is the highest-value thing you do, and the one a feature-focused author skips.

When a surface (a player, a form, an editor, a panel) carries **state**, the system almost always ALSO has
**global axes** it renders under. This is the **canonical axis list — its home is here; other docs point at it:**

- **view** (compact / detailed) · **mode** (quick / full, read / edit) · **tier** · **viewport size** ·
  **persistence / reopen** (any state that survives a reload — localStorage, a saved file) ·
  **concurrency** where it applies ·
  **every other live surface** — every other surface that can be present at the same time, whether or not
  that other surface holds state: a sibling sharing the screen, or a surface the flow reaches just before
  or after this one (a static end screen counts). For each, state what this surface does while that one is
  present: hold, clear, or hand off.

The bugs that pass every unit test live in the **product** of surface-state × axis, because each was
specified alone. The three authors forget most: viewport size (a grid that reflows below some width),
persistence/reopen (state written last session auto-restoring into a changed UI), and every other live
surface (a caption still naming the previous photo once the closing screen arrives, because "what the
caption shows when the finale is in view" was never written).

So, for every stateful surface, before you call its section done:

- **Enumerate it against each global axis.** For each axis value (each view/mode/tier), state what happens
  to the surface's state and controls. Is the state still *visible*? Still *reversible*? Does the axis
  transition *preserve, reset, or block* the state?
- **Name the composition invariant.** e.g. *"a per-stem mute/solo is reachable only while its control
  surface is visible; entering the compact view resets to the full mix."* Without it, you get the classic
  stranding bug: a state set in one view, hidden by another, with no way to see or undo it.
- **One surface, one name.** If the player's lanes and the `#stemlanes` canvas are the same thing, call
  them the same thing everywhere. A reviewer (human or prover) can only connect a cross-section hole when
  both sides are named identically and present in the same document — two names for one surface hides the
  seam.
- **If the surface persists state, compose the VERSIONS too.** When it writes localStorage/disk, enumerate
  version-N-1 state × version-N code explicitly: what does the current UI do when it reads a stored value
  that's older, partial, or belongs to a since-removed feature? State a migrate / ignore / clear rule — this
  is the seam behind "reopened it and it looked broken".

## Declare the pole when a capability could live in the pack or in each host (SPEC INV-163)

When you author a capability the pack could hold once or each host could hold its own, declare which pole it
takes, so the pack↔host home is a decided sentence rather than a silence. One question decides it: can the
pack ship a single identical body that every host runs? When it can, the body centralizes to one pack home,
adopted by a package update. When the body is host-specific — it names a host's own surfaces, holds a host's
own data, or reads a host's own artifacts — the pack ships the shape (a template and its guidance) and each
host owns the instance it fills. Write the chosen pole into the clause and cite the split [INV-163]; the duty
binds forward [INV-159], so a new host-specific capability names its pole from the first draft while the
bodies that predate the clause stand as they are cited.

## The feature delta, assembled — one home for its mandatory parts

Author in this order; every part below is MANDATORY for a feature and no scope cut may trim it
(scope dials richness, never the safety net — SPEC T-15):

1. **Regression fences** — when the wish touches a live surface (next section; SPEC T-14, INV-19);
2. **The new behaviour itself** — entities, states, transitions, composed across the canonical axes;
3. **The standard-facet sweep** — every facet a spec sentence, decided or `[default]`-tagged (SPEC T-13, INV-18);
4. **The fit walk** — how the feature sits in the person's path, kind-scaled (SPEC INV-29);
5. **The two closing sentences** — non-goals + one success measure (SPEC INV-20, INV-21).

A delta missing any numbered part is incomplete at authoring time — the author catches it before the prover ever sees it.

## The regression fences — run FIRST when the wish touches a surface that already lives (SPEC T-14, INV-19)

Before authoring anything new, preserve the neighbours. The spec-delta opens with one sentence per
existing promise that must stay true through the change ("the catalog still opens on click"), each
citing the spec clause it guards. A fence is not new law and earns NO new matrix row — the cited
clause's row already carries its never-side, and the landing's full-suite run is what proves the fence
held. Split what the delta touches: promises that STAY are fenced; behaviour being CHANGED is
re-authored as new law — a fact is fenced or re-authored, never both. A fence that finds no clause
behind it has discovered an unwritten promise: reconcile it from the shipped truth (like an adopted
claim), write it as its own spec fact with its own row, and surface it as an explicit statement rather than a
silent assumption. If
the cited neighbour claim is adoption-born and still unverified, its reconciliation runs before it can
be fenced — you cannot fence a hope. Name the fences by cited anchor in the wish's queue row
("fences: …") so "untouched and still true" stays greppable. A prototype fences nothing — it promises
nothing.

## The facet sweep — run when a wish's door says FEATURE (SPEC T-13, INV-18)

A person asks for a feature in the words they have; the dimensions below exist whether or not anyone
names them ("add a room where photos hang" never says "and decide what happens on a phone"). When the
door says feature, drafting the spec-delta walks this checklist — the **canonical facet list; its home is
here**, one list for every project.

**Read the project's declared layers, do not assume code (SPEC INV-135).** Which surfaces a facet sweep
reaches, and what a footprint's layer means for this project, come from the host profile's declared
`project.layers` line (SPEC INV-36, INV-135) — a photo site's layers are content, rendering engine, and
deployment, a campaign's are message, channels, and assets, and the pack's own are the rulebook, the
working skills, and the guardrails. The facet dimensions below are kind-abstract; read the declared
layers so the sweep names this project's real surfaces rather than assuming a codebase's.

**Read the kind's declared design principles too (SPEC INV-136).** Beside its layers and proofs a
project kind carries a set of design principles — checkable design rules the kind's products must hold,
homed in the per-kind design-principles table in ARCHITECTURE.md and declared for a visual kind on the
host profile's `project.design-principles` line. When the wish touches a surface a declared design
principle governs, write the principle's answer as a spec sentence the same way a facet ends as a
sentence — the frontend kind's interactive-overlap rule (interactive controls that belong to different
layers occupy separate screen space) is answered wherever a covering overlay opens over floating chrome,
so the delta states which controls retract while the overlay stands. The verify feel pass runs the
declared design principles; the spec names the answer so the pass has something to check.

- **the viewport bands** — width and height both run in bands (narrow, wide, short, tall, and the
  bands a future device adds), so every layout-bearing feature ends the sweep with a decided or
  `[default]` sentence per band its layout law names or excludes, and a law scoped to one band answers
  for the others — the author-side of the viewport-quantifier lens the prover holds, itself the worked
  instance of the range law's general sub-domain duty (a guarantee scoped to a named part of its domain
  answers for the remainder, a user state or a locale drawing the same sweep on its own parts) (SPEC INV-138).
  This folds the old width-only phone facet together with orientation / short viewport: a landscape
  phone is wide and short, a band a width-thinking sweep misses, so a rotated phone meets a stated
  layout rather than a blank (incident: tlvphotos's caption zone printed over the picture on a
  landscape phone — the layout law said "on a phone", the styles mapped phone to width ≤ 640px, and a
  rotated phone fell out of both sentences, 2026-07-16);
- **touch where the design assumed a mouse** — anything hover-only needs a touch answer;
- **the empty, error, and loading states** of each new surface (spelled "empty, error, and loading");
- **accessibility** — reachable by keyboard, readable contrast;
- **the performance envelope** — at what input size it must stay usable; for a user-facing surface
  this facet ends as a MEASURABLE budget sentence ("the first image appears within 2 s on a cold
  visit"), never an unmeasurable "fast enough" — the architecture step pairs the budget with an
  instrumentation home and acceptance asserts it (SPEC INV-41);
- **visual hierarchy** — the gap BETWEEN separate things larger than the gap WITHIN one thing (nesting
  depth drives spacing, never per-element guesswork); a heading never dimmer or smaller than the body it
  heads, sizes from one scale (incident: track-coach's inverted panel margins, 2026-07-05);
- **two windows at once** — the same stored state open in two windows; what one window's change does to
  the other (incident: track-coach's persisted aim auto-swapping cards, 2026-07-02);
- **a missing source** — an input file renamed, moved, or gone: the feature says what it shows and asks
  instead of guessing (incident family: the ask-don't-guess stem/source cases, track-coach 2026-06/07);
- **paired-transition symmetry** — when a surface has a pair of opposite state changes (open/close,
  enter/exit, expand/collapse, show/hide), the exit's motion mirrors the enter's unless a reason is written;
  the default is symmetry, and because motion feel is the human's own gate (SPEC INV-30) an undecidable pair
  is surfaced as a real question rather than shipping a crafted-in and instant-out pair silently; the answer
  ends as a spec sentence — mirror, a named shorter exit, or deliberately instant — decided or
  `[default]`-tagged like any facet (SPEC INV-126; incident: tlvphotos's polaroid room revealed under a soft
  veil in one breath and closed on a hard cut with no transition, found by hand on a real phone, 2026-07-12).
  The facet has a second half, the reversibility of the means: where the surface opens by a
  continuous, reversible gesture — a pinch, a drag, a lift — the same gesture reversed is written among its
  ways to close, or a decided sentence states why it is absent; silence there is a finding, and the rightness
  of the reason stays the human's gate (SPEC INV-126; incident: tlvphotos's pinch-to-zoom layer opened by a
  finger-tracked scale-up and closed only by a control, no reverse pinch, felt on a phone, 2026-07-14).
  The second half asks magnitude beside existence: where the pair rides a continuous, reversible
  quantity — a pinch span, a drag distance, a wheel accumulation — the author writes whether the two
  directions demand the same magnitude, symmetric or a named deliberate asymmetry, decided or
  `[default]`-tagged like any facet (SPEC INV-126; incident: tlvphotos's inspect zoom opened on any
  spread past rest yet closed only at a squeeze to ~0.82× of rest — the reverse existed at a deeper
  cost to the hand, and every prover pass came clean because the lens asked only existence, felt on
  a real phone, 2026-07-16).
- **Edge completeness — both ends of a gate, and the three faces of a wait.** When the surface has a
  behaviour gated on a quantity that runs on a line (elapsed time since a last visit, a count, a distance, a
  size), write what it does at both ends of the range — below the low end and above the high end — not only
  at the one point the wish named; "on return", "after a while", "once there are several" each owe their two
  bounds. And when a slot is filled by asynchronously produced content, write the three faces of a wait —
  pending, arrived, failed — with a visible pending face while the content is in flight; this is the
  empty/error/loading facet above made specific for a reserved slot, its loading state named and shown. Each edge becomes a
  spec sentence, decided or `[default]`-tagged like any facet (SPEC INV-138).

**The list is curated, each facet earning its place by named incident.** A facet joins ONLY with a named real incident it would have
caught — each entry above carries its incident — and the list is re-justified at milestones; a checklist
that grows by taste rots into a forty-row form nobody walks (the Google launch-checklist lesson).

**The declared-laws line rides every new section (SPEC INV-101).** Where the spec keeps a declared-laws home — the one place naming its cross-cutting laws (measurement, accessibility, error handling, a register: what the product declares) — a new surface's section states its line against each declared law, the clause or a dated exemption, before the prover ever reads the delta. Each declared law also carries its net — the review or gate that enforces it — written beside the law in that home, so the assignment lives where the laws are declared (SPEC INV-150); a law is a mechanical gate's where a deterministic guardrail or test decides the violation, the prover's where the violation pins to a stated sentence, and the design review's where the deciding fact lives only in the human's intent. The prover's cross-cutting station then audits instead of discovers; a spec with no such home yet earns the home first, and a declared law with no named net is a finding there.

**Every facet ends as a spec sentence — silence is not an option.** Either the human (or the walk's
batched questions) DECIDED it, or the recommended option is taken so the lane keeps moving and the
sentence is written carrying the literal tag `[default]` at its line end — so a later prover tells a
taken default from a hole, and the matrix derives the facet's test row either way. Every defaulted facet
is then TOLD on the landing report's defaults list as a plain-words tradeoff in the product's terms
("on a phone this gallery stacks into one column — tweakable"), never one ping per facet and never a
confirmation request (SPEC INV-31) — communicator owns the report shape; a veto
simply becomes a new wish. A facet with no sentence is a spec defect the prover flags. The sweep scopes to the feature's VISIBLE
surfaces — a headless feature (new persistent state only) satisfies it with one explicit sentence, "no
visible surface — facets N/A", never a silent skip.

Boundaries, stated once: a wish re-doored to feature mid-work walks the sweep before work resumes — the
late-recognized surface is exactly the one whose facets nobody looked at. A fenced prototype is never
swept (a sketch has no facets to promise); the sweep fires when promotion makes it a feature. On an
adopted or promoted surface that already lives, a default is read from the shipped truth and reconciled
like any re-engineered claim, never invented greenfield. And the sweep versus the canonical axes above:
the sweep AUTHORS the facet sentences when the feature is first specified; the axes COMPOSE and test them
across views once the surface exists — one dimension, split by time, never specified twice.

## The fit walk — run with the facet sweep when the door says FEATURE (SPEC INV-29)

The facets above ask what every visible feature owes its DEVICE; the fit walk asks how the feature
sits in the person's PATH — the questions nobody thinks to ask until a guest is stuck at the tenth
picture with no way on (tlvphoto, 2026-07-06). **The lens lists' home is here**, kind-scaled, curated
with incidents exactly like the facet list:

- **product / UX kind — the visitor's journey:** how does the person ARRIVE here (every entry door,
  not just the main one) · what do they DO here · where do they go NEXT from every state this surface
  can be in (no dead ends — the door↔room loop incident, tlvphoto 2026-07-06) · what does a RETURN
  visit change (seen-state, no-repeat — and the remembered state it implies) · a conditionally-entered
  face (first visit, empty state, onboarding, a one-time banner) names its deliberate re-entry path or
  states the one-way as a decision (SPEC INV-50) · what does the FEEL owe
  against the approved prototype's bar · what next feature does this one invite;
- **infra / backend kind — the flows:** inputs → outputs · the data's lifecycle (created, updated,
  stale, gone) · every failure path and what the caller sees;
- **skill kind — the behaviour:** the trigger · the correction it makes · when it must NOT fire.

The walk interrogates the FEATURE, never the person (SPEC INV-29): derive answers from the existing
spec and shipped truth; close the trivially-closable holes yourself AND WRITE HOW each was closed;
`[default]`-tag the rest; batch only the genuine taste calls with the facet sweep's report. Every
answer lands as a spec sentence — the same silence-is-not-an-option law as the facets.

## The delta's two closing sentences — non-goals and the success measure (SPEC INV-20, INV-21)

Every feature's spec-delta CLOSES with two short sentences, always written — silence is not a legal
state for either. **Non-goals**: what is deliberately left out ("version comparison waits for a later pass");
"nothing deliberately left out this time" is itself valid — only a missing sentence is a hole, and a
non-goal that narrows what the wish asked for rides the batched report, never a silent narrowing.
**A success measure**: how we'd notice the feature worked for its person, a number where one exists;
decided or `[default]`-tagged — the tag marks provenance only, no test row derives from it until the
reading machinery lands. The quantification questions (analytics tag? how measured? A/B worth it?) ride
the facet sweep's batched report. Both bind forward; an adopted feature owes its pair at the first
landing that touches it. A prototype writes neither — it promises nothing.

## The primary unit — one per project type, traced end to end (SPEC E-29, INV-73)

A spec has a PRIMARY UNIT: the thing the reader counts, the product's spine repeated. The unit is a
parameter of the project's TYPE — the way a domain swaps a template — declared once, then it sets the
heading style, the acceptance-criterion shape, and what the coverage check means.

| project type | primary unit | the coverage check validates |
|---|---|---|
| web / app | a user-facing **feature** (a visible flow) | every feature → architecture node(s) + a test |
| CLI / library / API | a **command** / function / endpoint | every surface → its contract, an owning module + a test |
| methodology package | a rule or **guarantee** the pack promises | every guarantee → an enforcing mechanism (a script, a gate, a template) |
| content / book / article | an **argument** / chapter / section | every promised argument → a home in the outline (a structure check; no technical architecture) |

**The mechanic is one, for every type.** Each unit carries a stable inline tag on its heading — the same
family as the anchors, e.g. `[feature: F-wish]` — and the downstream artifacts back-reference it: one
coverage table in ARCHITECTURE.md names the implementer node(s) and a test per unit. The guardrail reads
BOTH directions — every unit has an implementer and a test, and every promised unit carries its tag. This
is the anchor-ownership machinery extended a level up, never a second machine to keep in sync.

**No file explosion.** One PRODUCT_SPEC.md, one ARCHITECTURE.md, one TEST_MATRIX.md; the unit tags live
inline in the prose and the one coverage table binds them. Shard into per-feature files only for a
genuinely huge project, and only by explicit call.

**The source is plain Markdown; the render resolves the links.** The source stays plain Markdown — a
tag plus one table. When a doc is rendered, a relative `.md` cross-link opens its rendered `.html`
neighbour and its `#anchor` lands on the target heading (ROADMAP row 195, shipped 2026-07-10). Linking
a trailing bracket code to its Formal-index row stays an optional later leg; until that lands, a reader
follows a bare tag by searching the source.

**On live-spec itself.** live-spec is a package, but its scenarios ARE the product's features, so it
dogfoods the web/app row: each person-facing scenario heading tags `[feature: F-x]` and the Feature
coverage table maps it to its skills and its test. The machines that work behind the scenes (guardrails,
host contract) implement guarantees rather than user-facing features, and stay outside the feature layer
by the type's own definition of its unit. The decided design note is `docs/spec-format-by-project-type.md`.

**The heading convention makes the reverse direction mechanical (SPEC INV-132).** For the two-way check to
catch a scenario whose tag was forgotten, an untagged heading has to be unambiguous — and it is not on its
own, since the checker cannot tell a new scenario missing its tag from a machinery or reference section
that never had one. So every H3 heading carries either its `[feature: F-x]` tag (a person-facing scenario)
or the explicit `[not a scenario]` marker (a machinery, rules, or reference section, legitimately
untagged), and an untagged, unmarked H3 is unambiguously red. Put the convention on H3 headings, the level
every scenario uses; sub-parts nest under a heading already tagged or marked, so a `####` sub-heading owes
nothing. When you add a section that is not a person-facing scenario, state its `[not a scenario]` marker
in the same edit — a new machinery heading that passes silently is the gap this closes.

## The content contract — when a generic engine is extracted from an instance (SPEC INV-79)

A generic engine carved out of a working project inherits the donor's assumptions silently: an id
format, a hardcoded wordmark, a path, a language default. At extraction the spec opens a **content
contract** section: every donor-specific constant the extraction finds becomes a named entry — what
the engine requires from ANY instance's content, in the engine's own vocabulary — and each entry
owes a test that the engine works without the donor's value (test-author's half of the same law).
An assumption with no entry is a leak the next instance discovers in production.

## Crossing the instance→engine boundary — provenance and naming (SPEC INV-119)

A feature usually proves itself first on a live instance and then generalizes into the engine. When that history goes into the engine's spec, write it as the engine's own record: the reader is anyone who runs the engine, so every provenance handle points at something that reader can reach, and the spec reads as generic from the first line.

Four conventions carry the boundary:

- **The history reads as a reconciliation.** Head the history section "Reconciliation log — how each behaviour landed in code", and let each entry trace a behaviour to where it landed in the engine's own code. This is a spec-versus-code reconciliation the engine's reader can follow, rather than a fork's delta against an instance's reference implementation.
- **Provenance cites the engine's own public commit.** Each entry names where the behaviour landed in the engine — "landed in engine commit `<hash>`" — a commit any reader can check out in the engine's own history. A private instance's commit is invisible to that reader, so an instance hash stays out of the engine's provenance.
- **One intro sentence states the normal intake path, once.** Open the log with a single sentence naming the usual route — "Most rows record a feature proven first on a live instance and then generalized into the engine" — so no per-entry line re-explains where features come from.
- **A mechanism carries a neutral internal name; a visible instance label is marked as instance copy.** Name a mechanism by what it does in the engine's own vocabulary — "the unfold step", "the show-more control". Where a running instance shows locale-specific words for it, the spec notes that string as instance-supplied copy the instance plugs in [INV-79], and the neutral term stays the mechanism's one name [E-4].

## Standard vocabulary — what our house terms map to

The pack's method is its own, but its concepts are the field's, and naming the lineage lets a reader who
knows requirements engineering recognize what a live-spec document is doing. The crosswalk to the field's
vocabulary (ISO/arc42/C4) lives in `docs/spec-format-by-project-type.md`.

Two boundaries the crosswalk does NOT erase: our spec stays a single use-case-first document (never the
Entities/States/Actors chapters a naive reading of the standard invites — that shape gets rejected and
stops being read), and a term joins our vocabulary only when it is measurable or verifiable here, never for
the borrowed authority alone.

## How you work

1. **Author / grow the relevant section** in `PRODUCT_SPEC.md`, use-case-first: find (or open) the scenario the
   change belongs to — the intake placement verdict made real: the scenario IS the wish's place on
   the feature map (SPEC INV-37) — and grow the walk, plain language, anchors at line-ends, the Formal index updated in
   the same edit. Reuse the existing vocabulary; don't introduce a second word for an existing concept.
   Starting fresh? Copy `templates/PRODUCT_SPEC.template.md`. (Template paths resolve from the PACK repo —
   github.com/happysasha18/live-spec; a standalone install of this skill fetches them there. They are
   deliberately NOT copied into the skill dir: the pack is the source, a copy would fork the truth.)
2. **Ask, don't silently fill.** When the spec needs a decision only the author can make (a threshold, a
   policy, desired behavior on an edge), ask the leading question or mark ⟨DECIDE⟩, treating intent as
something to confirm rather than infer.
3. **Run the completeness pass** (below) on what you wrote.
4. **Hand off to `product-prover` on the WHOLE spec — your delta included.** The prover catches a
   cross-section hole only when *both* sides of the seam are in the document; a surface you added in
   isolation, or left unlinked, is invisible to it. So re-prove the whole spec whenever a surface is added.
5. **Then walk the two layers to the tests** — the architecture doc (nodes owning the spec's facts,
   proven with the architecture lens), then the matrix DERIVED node × fact (`spec → prove → architecture
   → prove architecture → matrix → test → code`; build-pipeline owns the steps). The spec leads; code
   chases it.

## The completeness pass — run before declaring a section done

Ask each question out loud; a "no" or "don't know" is a gap to fill or mark ⟨DECIDE⟩.

- **Entities:** Is every noun named once? Does each measure carry a unit + valid range? Does each entity
  with a lifecycle list its states?
- **Transitions:** For every state, what action leaves it, and who triggers it? Is there a state with no
  exit?
- **Invariants:** What must never happen here (safety)? What must eventually happen (liveness)? Is each
  stated, not just implied?
- **Composition:** Does this surface carry state? Under which of the canonical axes (view / mode / tier /
  viewport size / persistence-reopen / concurrency / every other live surface) is it shown? For each, is
  its state still visible and reversible? Is the transition's effect (preserve / reset / block) stated? If
  it persists state, is the older-stored-value × current-code case handled? For every OTHER surface that
  can be present at the same time — a sibling on the screen, the surface one step before or after in the
  flow — is this surface's behaviour stated while that one is present?
- **Facets (feature door):** Did the facet sweep run — does every entry of the canonical facet list end
  in a spec sentence, decided or `[default]`-tagged and reported?
- **Naming:** Is anything in this section also referred to by another name elsewhere? Unify it.
- **Single source of truth:** Does any OTHER document in this repo also claim to be the spec or the matrix
  ("source of truth")? If so, demote it to a pointer — two docs claiming authority is undefined when they disagree.
- **Honesty:** Is any claim here something the system can't actually deliver, or a guess dressed as a fact?
  Mark it ⟨DECIDE⟩ or cut it.
- **Readability (human-first, product language):** Does each rule lead with a plain-language headline a
  non-author grasps in one read? Is it phrased in product words a person would say? Are the codes/tags at
  line-*ends*, never opening the line? Is there any edit-history scar in the prose that belongs in the
  JOURNAL? Does the spec open with a "how to read" note?
- **Shape (use-case-first):** Is every section a scenario named by what the person does — no
  Entities/States/Actors chapters? Is every spine item present INSIDE the scenarios? Does every anchor in
  the prose appear in the Formal index (and every index row point at a real section)? After a restructure:
  is the anchor set identical to before (or every delta named)?

## What you produce

A `PRODUCT_SPEC.md` (or an updated section of one) that is use-case-first — scenarios lead, anchors trail, the
Formal index closes the doc — complete against the spine, with surfaces named once and their cross-axis
composition stated — ready for `product-prover` to review and for a test matrix to be derived from. You also surface, in your reply, the ⟨DECIDE⟩ points you couldn't
resolve and the leading questions behind them.

## Anti-patterns (refuse these)

- **Speccing a surface on one axis only** — the player described as play/mute/solo with no word on what the
  compact view does to it. Always compose.
- **Two names for one surface** — "the lanes" and "#stemlanes" as if separate. Unify.
- **Filling a gap silently** — inventing a threshold or a behavior the author never decided. Ask or
  ⟨DECIDE⟩.
- **Speccing after the code** — writing the spec to match what was built, rather than letting the spec lead
  and the prover find the holes before code exists.
- **Pinning a drifting version number in prose** — "current version: vX.Y" in a header or README always
  goes stale; the version has one home (the VERSION file, the frontmatter) — point there or omit it.
  This binds a **derived doc's header** too (ARCHITECTURE.md, TEST_MATRIX.md): a derived doc's header
  carries no frozen spec-version number — it names what it derives from, points at the version's one
  home (VERSION), and carries a dated "Last reconciled" provenance line instead of a version string, so
  a reader never meets a stale number that reads as the current version. The lint `tests/test_derived_doc_header_policy.py` holds the two headers to this (row 265).
- **A wall of undifferentiated prose** — paragraphs with no headline to land on. The fix is a **bold
  headline per rule + the detail beneath**, so the eye lands, then drills in — machine-terse fragments
  are the opposite failure and get rejected just as hard (see "How it reads").
- **Codes opening the line / edit-history in the prose** — `INV-18:` as a sentence's first word, or "in v0.8
  we changed…" baked into a rule. Codes go at line-ends; history goes in the JOURNAL.
- **Structure-first layout** — a document organized as Entities / States / Actors / Invariants chapters.
  That's the checklist wearing the reader's hat: it reads like a database dump and stops being read.
  Scenarios lead; the primitives live inside them; the Formal index serves the machine.
- **An index that drifts** — a Formal index edited by hand into claims the prose doesn't make (or missing
  anchors the prose has). The index is derived from the prose, re-checked at milestones, never a second truth.

## Pairing with product-prover

| | spec-author | product-prover |
|---|---|---|
| role | writes & grows the spec | reviews the spec |
| output | structured `PRODUCT_SPEC.md` sections | findings: gaps, contradictions, missing invariants |
| when | starting / adding a feature / a new surface | spec drafted or changed, before tests/code |

Author with this skill, review with the prover, then derive matrix + tests. Same primitives on both sides
so the handoff is clean.
