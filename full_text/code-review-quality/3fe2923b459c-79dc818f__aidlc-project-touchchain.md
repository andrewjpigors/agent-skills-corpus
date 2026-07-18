---
name: aidlc-project-touchchain
description: >
  Use when the orchestrator wants to run the AI-DLC feature delivery chain in a single
  CLI session — CPO planning through CQO sign-off with hard stop gates at every agent
  transition. Trigger on /touchchain, "run the chain", "start the touchchain", "feature
  delivery chain", or when the orchestrator describes a workflow that moves a ticket from
  planning through CPO, CTO, Code Review, CQO, and back. Also trigger when the orchestrator
  says "run a ticket through the chain", "full cycle on this ticket", or "let's chain this".
  The chain self-classifies ticket complexity at Gate 0 using objective signals — Express
  (6 gates), Standard (8 gates), or Full (10 gates). Classification determines ceremony
  level, coaching output, and token budget. Code review and Jira comments are non-negotiable
  at every tier. No agent proceeds without sign-off. No context moves without verification.
license:
  holder: S3 Technology
  contact: don@s3technology.io
  terms: Apache-2.0 — see LICENSE at suite root
  copyright: "Copyright (c) 2026 S3 Technology"
---

# aidlc-project-touchchain — Epic-Level Delivery Chain
### Hard Stops. Human in the Lead. Every Transition.
*Built for AI-DLC: Full Cycle engagements*

---

## Hand-off Card Entry Contract

This skill is the **back half** of the AIDLC lifecycle. Its entry point is
the **Hand-off Card** produced by `aidlc-kickoff-touchchain` at G10 (Cold
Start) or R3 (Re-entry).

### How to enter

When the orchestrator invokes this skill, your first action is **not** to
start a ticket — it is to locate and read the hand-off card.

1. **Find the card.** Look in this order:
   - Path referenced in `ProjectState.md` under `active_handoff_card`
   - `<project>/handoff/<epic-slug>-handoff-card.md` (most recent mtime)
   - Ask the orchestrator to specify the path
2. **Validate the card.** It must have:
   - `to_skill: aidlc-project-touchchain` in frontmatter
   - `project_state_pointer: ProjectState.md`
   - A non-empty `## Tickets` table
   - An `entry_type` of `cold-start` or `re-entry`
3. **Read `ProjectState.md` first** — it is the authoritative source of
   current state. The hand-off card is a contract snapshot; `ProjectState`
   is live.
4. **Interpret `entry_type`:**
   - `cold-start` → start with the first ticket in the table.
   - `re-entry` → consult `drift_mode` in the card's frontmatter:
     - `lite` → proceed directly to the first unstarted ticket
     - `standard` → re-confirm epic goal with the orchestrator before starting
     - `heavy` → pause, tell the orchestrator R2 already re-planned and
       ask if they want to review the new backlog against the old one
5. **Check the tracker.** If `tracker` is `linear`/`jira`/`github`, call
   `list_granted_applications` and verify the tracker MCP is connected. On
   each ticket close, write the status update back to the tracker via MCP.
   If `tracker: manual`, rely on the `## Manual Tracker Entry` block and
   the orchestrator's manual sync.

### The ticket loop

For each ticket in the card's table, in order:

1. Run it through the full CPO → CTO → (Code Review) → CQO gate sequence
   defined below.
2. At every gate, apply the Covenant: no transition without orchestrator
   approval; every approval produces a written ledger entry.
3. When the ticket closes, **ask the orchestrator: "Ready for the next
   ticket?"** and wait for an explicit "yes" / "continue" / similar.
4. Write the ticket close to `ProjectState.md` and append to
   `kickoff-ledger.md`.
5. If the tracker MCP is connected, update the issue status to closed and
   add a completion comment.

### Epic boundary

When the last ticket in the card closes:

1. Write `current_epic: null` (or the next epic slug if the orchestrator
   has already re-entered) to `ProjectState.md`.
2. Append an **Epic Close** entry to `kickoff-ledger.md` summarizing what
   shipped, what deferred, and any insight-journal entries captured during
   the epic.
3. Tell the orchestrator:
   > Epic `<epic-slug>` is complete. I recommend clearing context before
   > the next epic to keep token usage reasonable. Your next step is to
   > invoke `aidlc-kickoff-touchchain` — its Resume Router will detect
   > EPIC-COMPLETE and run a Re-entry pass (R0 → R1 → ...) for the next
   > epic.
4. Exit cleanly. Do not start the next epic yourself — that's kickoff's
   job, and the context clear is part of the protocol.

### Mid-ticket resume

If the orchestrator returns mid-ticket (session crashed, context cleared
early, etc.), read `ProjectState.md` to find:

- `active_ticket` — the ticket ID currently in flight
- `active_gate` — which gate of the ticket chain was last closed
- `pending_gate` — the next gate to run

Then resume from `pending_gate` without restarting the ticket. Confirm the
resume point with the orchestrator before doing any work.

---

## The Covenant

This skill exists because agents are capable of producing excellent work — and equally
capable of drifting when left unsupervised across role transitions.

The Touchchain is the orchestrator's control mechanism. It enforces a simple, non-negotiable
rule: **no agent transition happens without the orchestrator's explicit approval.** Every
handoff is a hard stop. Every hard stop produces a summary. Every summary gets human eyes
before the chain moves forward.

The orchestrator is not a rubber stamp. They are the person who catches drift, questions
assumptions, spots misalignment with the Epic or Project goal, and redirects before wasted
work compounds. The chain moves at the orchestrator's pace — never the agent's.

---

## How It Works

One CLI session. One agent at a time. The agent loads a role skill (CPO, CTO, CQO, etc.),
does its work, produces a **Gate Card**, and stops. The orchestrator reviews the Gate Card,
captures any insights, and either approves the transition or sends the agent back with notes.

The chain state is tracked in a **Chain Ledger** — a running log that persists for the
session. Every gate produces a ledger entry. At session close, the ledger becomes a KB
artifact.

```
┌─────────────┐
│ SESSION OPEN │
└──────┬──────┘
       ▼
┌─────────────┐     ┌──────────────────────────┐
│  STATE 1    │────▶│ HARD STOP — Orchestrator  │
│  CPO: Plan  │     │ reviews Gate Card         │
└─────────────┘     └────────────┬─────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │ Approved? ──▶ Next State │
                    │ Rejected? ──▶ Same State │
                    └─────────────────────────┘
```

This pattern repeats at every state boundary. No exceptions.

---

## Coaching Mode

The Touchchain serves two audiences: experienced orchestrators running production chains,
and new orchestrators learning the methodology. Coaching mode scales with complexity tier:

- **Full (Tier 3):** Coaching ON by default. Full narrative coaching blocks at every gate.
  This is where orchestrators are making real judgment calls across multiple unknowns.
- **Standard (Tier 2):** Coaching ABBREVIATED by default. One-sentence coaching hint per
  gate — enough to remind, not enough to lecture. Full coaching available on request.
- **Express (Tier 1):** Coaching OFF by default. The orchestrator qualified this ticket
  for Express — they already know the flow. Full coaching available on request.

To override the default at any gate: "coaching on", "coaching off", or "coaching full."
The override persists for the remainder of the session.

Experienced orchestrators will run Express and Standard with coaching off. New orchestrators
should run their first 3-5 chains at Full tier (or override to "coaching full" on any tier)
to build the judgment that makes coaching unnecessary.

---

## Complexity Tiers

Not every ticket deserves the same ceremony. A regex utility module does not need
the same gate count as a payment flow with security implications. The touchchain
self-classifies at Gate 0 using objective, measurable signals — not agent judgment.

**The principle:** Express must be *earned* by meeting every threshold. One miss and
the ticket is Standard. One red flag and it's Full. The agent cannot talk itself
into Express — the signals are binary.

### Classification Signals

These are measured, not judged. The agent counts and checks; the orchestrator confirms.

| Signal | Measurement | How to Check |
|--------|------------|--------------|
| **Files touched** | Count of files to create + modify | Ticket description + annotation |
| **Existing code modified** | Does this change files already in the repo? | `git ls-files` against file list |
| **Cross-module reach** | How many distinct directories are touched? | File path analysis |
| **Dependency chain** | Blocks or blocked by other tickets? | Jira links |
| **Growth log precedent** | Has this exact pattern been completed with a clean chain? | Growth Log grep for matching pattern tags |
| **Security surface** | Touches auth, PII, payments, secrets, or external APIs? | File path + keyword scan |
| **Test layer depth** | How many test layers does the CTO need to declare? | Annotation test_strategy |

### Classification Rules

```
EXPRESS (Tier 1) — ALL must be true:
  - Files touched: ≤ 3
  - Existing code modified: No (greenfield only)
  - Cross-module reach: 1 directory
  - Dependency chain: Blocks ≤ 2, blocked by 0
  - Growth log precedent: Yes (matching pattern exists)
  - Security surface: None
  - Test layers: L1 + L2 only

FULL (Tier 3) — ANY ONE triggers:
  - Security surface: Yes (auth, PII, payments, secrets, external APIs)
  - Cross-module reach: ≥ 4 directories
  - Files touched: ≥ 10
  - Growth log precedent: No AND existing code modified: Yes
  - Test layers: L4+ required (component, AI eval, or E2E)

STANDARD (Tier 2) — Everything else.
  Standard is the default. If classification is ambiguous, it's Standard.
```

**Orchestrator override:** The orchestrator can upgrade tier (Express → Standard,
Standard → Full) at Gate 0 or at any subsequent gate. Downgrading tier is not
permitted mid-chain — if you started Standard, you finish Standard or upgrade to Full.

### Tier Gate Sequences

Each tier defines which states the chain traverses. States not in the tier's
sequence are skipped entirely — no gate card, no Jira comment, no token spend.

**Express — 6 gates + session close:**

```
Gate 0: Session Open + Complexity Classification
Gate 1: CTO Annotation (ticket description IS the brief — no separate CPO planning)
Gate 2: CTO Execution
Gate 3: Code Review (+ growth log capture)
Gate 4: CTO Post-Review Revision (conditional — skip if review is clean)
Gate 5: CQO Quality Gate + CPO Close (combined)
Session Close
```

Skipped: CPO Strategic Planning (ticket description serves as brief), CPO Go/No-Go
(direction is clear — classification confirmed this), CPO Post-Implementation Review
(scope is isolated — CQO gate provides sufficient verification).

**Standard — 8 gates + session close:**

```
Gate 0: Session Open + Complexity Classification
Gate 1: CPO Strategic Planning (Execution Brief)
Gate 2: CTO Annotation
Gate 3: CPO Go/No-Go
Gate 4: CTO Execution
Gate 5: Code Review (+ growth log capture)
Gate 6: CTO Post-Review Revision (conditional)
Gate 7: CQO Quality Gate + CPO Close (combined)
Session Close
```

Skipped: CPO Post-Implementation Review (merged into combined close gate).

**Full — 10 gates + session close:**

```
Gate 0:  Session Open + Complexity Classification
Gate 1:  CPO Strategic Planning
Gate 2:  CTO Annotation
Gate 3:  CPO Go/No-Go
Gate 4:  CTO Execution
Gate 5:  Code Review (+ growth log capture)
Gate 6:  CTO Post-Review Revision
Gate 7:  CPO Post-Implementation Review
Gate 8:  CQO Quality Gate
Gate 9:  CPO Ticket Close & Summary
Gate 10: Session Close
```

No states skipped. Full ceremony for complex work with multiple unknowns.

### Non-Negotiables Across All Tiers

These hold regardless of classification. No tier exempts them.

1. **Code review is never skipped.** This is the core of agent learning evolution.
   The growth log capture at the review gate is how the system gets smarter.
2. **Every gate used gets a Jira comment.** The comment follows the established
   structure (Stakeholder Summary + Gate Detail + Trace). Express has fewer gates,
   so fewer comments — but every gate that fires produces one.
3. **Ambiguity or questions = hard stop to orchestrator.** Even in AUTO gated
   approval mode, any uncertainty surfaces immediately. Tier does not affect
   the hard stop threshold.
4. **CQO Quality Gate is never skipped.** Tests pass, ratchet maintained, analyzer
   clean — verified independently at every tier.
5. **Velocity readiness is verified at Gate 0.** Every ticket must have story points
   and a sprint assignment before the chain advances past Gate 0. This is a hard stop
   in every tier, including AUTO mode. Missing points or missing sprint = REDIRECT to
   orchestrator before any role work begins. This is conceptually owned by the CIO role
   (environment/operational validation) but executed inline at Gate 0 so the chain never
   spends tokens planning work that won't contribute to velocity measurement.

### Combined Gates

Two gates appear as combined in Express and Standard tiers:

**CQO Quality Gate + CPO Close (Express Gate 5, Standard Gate 7):**
The CQO runs the full quality gate protocol (tests, ratchet, slop check, test layer
coverage). If APPROVED, the agent immediately produces the CPO close summary
(Orchestrator Summary format) in the same gate card. One gate, two deliverables,
one orchestrator decision point. If the CQO returns RETURN, the close does not fire —
the chain loops back to CTO revision as normal.

**Gate 0 + Complexity Classification:**
Session open protocol runs first (context loading, KB, growth log, insight journal).
Classification runs second (signal evaluation, tier determination). Both are presented
in a single gate card. The orchestrator confirms context AND tier in one approval.

---

## The Chain — State by State

The states below define the full chain (Tier 3). Express and Standard tiers use the
subset defined in their Tier Gate Sequence above. State definitions are identical
regardless of tier — only which states are included changes.

**Gate numbering is tier-relative.** The state definitions below use Full tier gate
numbers (Gate 0-10). In Express and Standard tiers, the same states appear at
different gate numbers per the Tier Gate Sequence table. When the text below says
"Gate 5" it means the Code Review state — which is Gate 3 in Express, Gate 5 in
Standard, and Gate 5 in Full. The Tier Gate Sequence is the authoritative mapping.

### State 0 — Session Open

**Action:** Load the `session-open` skill. Identify the project, load KB context,
identify the ticket or Epic being worked. Read the existing Insight Journal file
(default: `docs/aidlc/InsightJournal.md`) to load prior orchestrator observations
and patterns. Read the existing CTO Growth Log (default: `docs/aidlc/CTOGrowthLog.md`)
to load prior agent findings and patterns. If either file doesn't exist, create it
with the header block.

**Velocity readiness query (required before presenting Gate 0 card):**

1. Fetch the ticket from the tracker. Extract: `story_points`, `sprint` (or cycle),
   and `parent_epic` (or parent link). If any tracker field is unknown, ask the
   orchestrator for the field mapping — do not guess.
2. Set `Story points` = the numeric value, or `MISSING` if null/unset/zero.
3. Set `Sprint assigned` = the sprint/cycle name, or `MISSING` if null/unset.
4. If the ticket has a parent epic and a sprint: check that the sprint belongs to
   the parent epic's active cycle. If yes → `CONFIRMED`. If no → `MISMATCH`. If no
   parent epic → `N/A`.
5. Readiness = `READY` only when points and sprint are both present AND epic alignment
   is CONFIRMED or N/A. Otherwise `NOT READY` with the specific reason.
6. **Epic backlog audit** — check session state for `audited_epics` (list of epic IDs
   already audited this session). If the ticket's parent epic is not in that list:
   query all tickets under the parent epic, count total, count with points, count
   with sprint, list gaps. After reporting, add the epic ID to `audited_epics`. If
   the epic is already in the list: set Gaps = "Skipped — audit already ran for this
   epic this session" and do not re-query.

The velocity readiness block is populated in the Gate 0 card from these values.
If Readiness = NOT READY, the agent's recommendation on the card is REDIRECT with
a clear statement of what the orchestrator needs to fix in the tracker before the
chain can proceed. The orchestrator may fix the fields and re-run Gate 0, or
OVERRIDE the readiness check with explicit reasoning (e.g., "spike ticket, no points
expected") — but the override must be recorded in the session ledger.

**Role:** None yet — environment setup.

**Produces:** Session brief with project context, ticket ID, Epic/Project goal statement,
and any relevant prior insights surfaced from the journal.

**Gated Approval Mode — ask before presenting Gate 0:**

```
Gated Approval: Manual or Auto?

  MANUAL — Every gate is a hard stop. The orchestrator reviews and explicitly
           approves each Gate Card before the chain advances. This is the default
           and recommended mode for new orchestrators or unfamiliar tickets.

  AUTO   — Gates with a clean APPROVE recommendation proceed automatically.
           The agent presents the Gate Card for visibility, then immediately
           continues to the next state without waiting. The orchestrator is
           tagged in (hard stop) ONLY when:
             • The recommendation is REDIRECT or ESCALATE
             • The agent has a question that requires orchestrator input
             • The Go/No-Go decision (Gate 3) is ambiguous
             • Any RDAI field raises a concern the orchestrator should weigh in on

           Auto mode trusts the chain when artifacts are aligned. The orchestrator
           still sees every Gate Card and can say "hold" at any point to pause
           the chain and switch back to Manual for the remainder of the session.
```

Store the selected mode in session state. Default to MANUAL if the orchestrator
does not specify. The mode can be changed mid-chain — "switch to manual" or
"switch to auto" at any gate.

**HARD STOP — Gate 0:**

```
GATE 0 — SESSION CONTEXT + COMPLEXITY CLASSIFICATION
──────────────────────────────────────────────────────
Project: [name]
Ticket:  [ID] — [title]
Epic/Project Goal: [the goal this ticket serves]
KB Context: [loaded / partial / none — with note]
Session Fingerprint: [hash if FCE is active]
Gated Approval: [MANUAL / AUTO]

COMPLEXITY CLASSIFICATION
  Files touched:          [N] — [list]
  Existing code modified: [YES / NO] — [evidence: git ls-files check]
  Cross-module reach:     [N] directories — [list]
  Dependency chain:       Blocks [N], Blocked by [N] — [ticket IDs]
  Growth log precedent:   [YES — pattern tag / NO]
  Security surface:       [NONE / YES — what it touches]
  Test layers:            [L1+L2 / L1-L3 / L4+ required]

  Classification: [EXPRESS / STANDARD / FULL]
  Reason: [which rule determined the tier — e.g., "All Express thresholds met"
           or "Standard: blocked by 2 tickets" or "Full: touches auth"]
  Coaching: [ON / ABBREVIATED / OFF] (default for this tier)

VELOCITY READINESS (per-ticket — hard stop in every tier)
  Story points:    [N / MISSING]
  Sprint assigned: [Sprint Name / MISSING]
  Epic alignment:  [CONFIRMED — sprint belongs to parent epic's active cycle /
                    MISMATCH — sprint is not associated with this epic /
                    N/A — ticket has no parent epic]
  Readiness:       [READY / NOT READY — reason]

EPIC BACKLOG AUDIT (first ticket of epic per session — warning only)
  Epic: [EPIC-ID] — [title, or "N/A — no parent epic"]
  Total tickets in epic: [N]
  Pointed:    [M] of [N]
  Sprinted:   [K] of [N]
  Gaps: [list of ticket IDs missing points or sprint / "None" / "Skipped — audit already ran for this epic this session"]
  Status: [CLEAN / GAPS PRESENT — orchestrator advised to backfill before committing to velocity targets]

Orchestrator: Confirm context, goal, tier classification, and velocity readiness.
Proceed? [APPROVE / OVERRIDE TIER: ___ / REDIRECT]
```

**COACHING (Gate 0):**
> This is your foundation. Everything the chain produces will be measured against the
> Epic/Project Goal stated here. If the goal is vague ("improve the app") or missing,
> stop and fix it now. A clear goal sounds like: "Enable users to reset their password
> without contacting support." Every future gate will ask: does this work still serve
> that goal? If the goal is wrong here, every gate after this is checking against the
> wrong target.
>
> **On complexity classification:** The agent just measured seven objective signals and
> proposed a tier. Check the evidence, not the conclusion. If it says EXPRESS, verify
> that every threshold is actually met — especially "Growth log precedent: YES." If
> the pattern tag doesn't match what this ticket is actually doing, override to STANDARD.
> When in doubt, go higher. The cost of running Standard on an Express ticket is extra
> gates. The cost of running Express on a Standard ticket is missed strategic alignment.
>
> **On velocity readiness:** Story points and sprint assignment aren't ceremony — they
> are how the team measures whether the methodology is actually working. A ticket with
> no points contributes zero to velocity, even if it ships perfectly. A ticket in no
> sprint never counts in any cycle's burndown. If the velocity readiness line says
> NOT READY, stop the chain and fix the ticket fields before approving. This is a
> five-second field edit in Jira that preserves weeks of velocity data integrity.
>
> **On epic backlog audit:** This fires once per epic per session. If the audit reports
> gaps — say, 12 tickets in the epic but only 4 pointed — that's not a blocker for this
> specific ticket, but it is a signal that the initial backlog wasn't set up for velocity
> measurement. The orchestrator should decide: backfill the gaps now (recommended) or
> note the debt in the Insight Journal and continue. The chain proceeds either way —
> this is information, not a hard stop — but ignoring it means your velocity numbers
> will lie to you for the rest of this epic.

**On APPROVE:** The orchestrator signals the transition — "Load CPO", "Proceed to State 1",
or simply "Go." The agent reads `../aidlc-cpo/SKILL.md` and begins State 1 work. This
same pattern applies at every state transition: the orchestrator's approval message is
the trigger for the agent to load the next role skill.

---

### State 1 — CPO: Strategic Planning

**Action:** Load `aidlc-cpo` SKILL.md. The agent adopts the CPO role.

**Work:**
- Read the ticket and any existing specs
- Build or refine the execution brief (objective, success criteria, scope, constraints)
- Sequence the ticket against the current phase
- Update Jira/Linear: ensure ticket fields are complete, priority is set, acceptance
  criteria are documented

**Produces:** Execution Brief (per CPO Section 5 — Execution Brief Format) and updated ticket.

**HARD STOP — Gate 1:**

Present the RDAI Summary (see Gate Card Format below) plus:
- The Execution Brief for orchestrator review
- Confirmation that Jira/Linear is updated
- Goal alignment statement: "This ticket moves us toward [Epic Goal] because [reason]"

**COACHING (Gate 1):**
> You're reviewing the CPO's plan — the Execution Brief. Ask yourself three things:
> (1) Do the success criteria tell you exactly what "done" looks like? If they're vague,
> send it back. (2) Is the scope section clear on what's IN and what's OUT? Scope
> ambiguity here becomes scope creep in State 4. (3) Does the "why now" make sense —
> why this ticket in this phase, not next phase? A good brief makes you feel confident
> handing it to a developer. A bad one makes you feel like you'd need to explain it
> yourself. Trust that feeling.

**Next:** State 2 (CTO Annotation) on approval.

---

### State 2 — CTO: Annotation

**Action:** Load `aidlc-cto` SKILL.md. The agent adopts the CTO role.

**Work:**
- Read the CPO's Execution Brief (carried forward from Gate 1)
- Read the ticket from Jira/Linear
- Read the CTO Growth Log (`docs/aidlc/CTOGrowthLog.md`) and scan PATTERN TAGs
  for known gotchas relevant to the files being annotated. If the annotation touches
  files or patterns where prior findings exist, include them in `risk_surface`.
- Read the Code Best Practices KB entry (if one exists from a prior Practice Synthesis).
  Check Validated Practices and Proactive items for relevance to the files being
  annotated. Include applicable practices in `risk_surface` or `constrained_decisions`.
- Produce a full CTO annotation per CTO SKILL.md requirements:
  ticket_id, objective, approach, files_to_touch, alternatives_considered,
  risk_surface, test_strategy, constrained_decisions
- **test_strategy must declare which of the 6 test layers apply** to the code being
  written, and what tests will be added at each applicable layer. No layer is skipped
  by default. No layer is "deferred" unless the project's quality ratchet explicitly
  schedules it for a future phase — and even then, only the layers the ratchet defers.
  Every other applicable layer gets tests at time of development.

  **The 6 Test Layers:**
  - **L1 (Static):** Linting, type safety, secrets scanning, RLS verification.
  - **L2 (Unit):** Pure logic — calculations, filters, validators, formatters,
    date logic, permission checks. If logic can be tested in isolation, it gets
    a unit test. No exceptions.
  - **L3 (Integration):** RLS contracts, multi-tenant isolation, RBAC enforcement,
    audit log shape, API contract verification.
  - **L4 (Components):** Render testing, design token compliance, accessibility,
    responsive coverage.
  - **L5 (AI Eval):** LLM-as-judge consistency, evaluation quality scoring.
  - **L6 (E2E):** Full browser paths — registration, workflows, search/filter.

  The annotation's test_strategy lists: (1) which layers apply to this ticket's code,
  (2) what specific tests will be written at each layer, (3) which layers are deferred
  per the project ratchet (with the specific ratchet reference — not "we'll do it later").
  If the CTO cannot identify tests at any applicable layer, that is a risk surface
  entry — the code may be too tightly coupled or the layer analysis is incomplete.

**Produces:** CTO Annotation (per CTO annotation schema).

**HARD STOP — Gate 2:**

Present the RDAI Summary plus:
- The full CTO Annotation for orchestrator review
- Any constrained decisions that need orchestrator awareness
- Goal alignment statement

**COACHING (Gate 2):**
> This is the CTO's technical plan. You don't need to understand every line — you need
> to understand the shape of it. Look at `files_to_touch`: does the list feel
> proportional to the ticket? A one-field UI change touching 15 files is a red flag.
> Look at `alternatives_considered`: if there's only one approach listed, ask why.
> Good annotations show the CTO thought about tradeoffs. Look at `risk_surface`:
> are there risks the CTO didn't mention that you know about from context (other
> teams, upcoming changes, client constraints)? Your job here is strategic gut-check,
> not code review. Does this plan *feel right* for what we're trying to achieve?

**Next:** State 3 (CPO Review) on approval.

---

### State 3 — CPO: Strategic Confirmation (Go/No-Go)

**Action:** Load `aidlc-cpo` SKILL.md. The agent adopts the CPO role.

**Work:**
- Review the CTO Annotation against strategic goals (CPO Protocol 1)
- Answer three questions: phase alignment, long-term risk, scope correctness
- Issue CONFIRMED or REDIRECT
- Update Jira/Linear with the decision

**Produces:** CPO Strategic Confirmation (per CPO Section 5 — Strategic Confirmation Format).

**HARD STOP — Gate 3:**

Present the RDAI Summary plus:
- The Go/No-Go decision with rationale
- If REDIRECT: specific notes on what needs to change
- Jira/Linear update confirmation

**Decision tree:**
- **GO** → State 4 (CTO Execution)
- **REDIRECT** → Return to State 2 (CTO re-annotates with CPO notes)
- Loop continues until GO is issued. Each loop iteration gets its own Gate Card.

**COACHING (Gate 3):**
> This is your most important gate. Go/No-Go is real authority — you are deciding
> whether to commit engineering time to this approach. A "Go" here means you believe
> the CTO's plan will deliver the CPO's brief. If something feels off — even if you
> can't articulate it precisely — that's a valid reason to REDIRECT. Say "something
> about the scope feels too broad" or "I'm not sure the risk surface covers X" and
> let the CTO address it. Redirects are not failures. They are the system working.
> The costliest mistake an orchestrator makes is approving a Go they had doubts about.
> A redirect costs 15 minutes. A bad Go costs hours of rework.

**Next:** State 4 on GO. State 2 on REDIRECT.

---

### State 4 — CTO: Execution

**Action:** Load `aidlc-cto` SKILL.md. The agent adopts the CTO role.

**Work:**
- Implement the approved annotation
- Write code, tests, configuration per the annotation's `files_to_touch`
- Follow the CTO's hard rules: no files outside annotation, ratchet maintained,
  analyzer clean
- **Before presenting the gate:** Self-review against the CTO Growth Log (known
  PATTERN TAGs) and the Code Best Practices KB entry (Validated Practices). The
  Growth Log catches "things I got wrong before." The best practices entry catches
  "things the industry says to watch for this stack." If either applies, fix now —
  before the reviewer sees it. No defensive narration. Just fix.
- **Test layer self-check:** Verify that every layer declared in the annotation's
  test_strategy has corresponding tests in the implementation. If a layer is missing,
  write the tests now — before presenting the gate. Do not present a Delivery Summary
  with test layer gaps and hope the reviewer doesn't notice.
- Produce a CTO Delivery Summary (per CTO Section 9 format)

**Produces:** Working implementation + CTO Delivery Summary.

**HARD STOP — Gate 4:**

Present the RDAI Summary plus:
- CTO Delivery Summary (files modified, tests baseline/final, analyzer status)
- Diff summary of what changed
- Goal alignment: "This implementation delivers [objective from brief]"

**COACHING (Gate 4):**
> The CTO just built something. Your job is not to review the code — that's State 5.
> Your job is to check the Delivery Summary against the annotation from Gate 2.
> Did they touch only the files they said they'd touch? Did tests increase (ratchet)?
> Is the analyzer clean? These are binary checks — yes or no. If the CTO modified
> files not in the original annotation, that's scope creep from the implementation
> side and you should ask why. Also check the Goal Alignment statement — does the
> CTO's description of what was built still sound like the thing the CPO briefed?

**Next:** State 5 (Code Review) on approval.

---

### State 5 — Code Review

**Action:** The CTO role dispatches the `requesting-code-review` skill per the existing
code review protocol. The code review executes fully within this state — the gate presents
the results *after* the review is complete.

**Work (executes before the gate is presented):**
- CTO runs the pre-review self-check (structural integrity, tag matching)
- Dispatches code-reviewer subagent with proper context (SHAs, requirements, description)
  AND the Code Best Practices KB entry (if it exists). The reviewer uses Validated
  Practices as review criteria — findings that violate a Validated Practice are
  automatically Important or Critical, not style preferences.
- Receives review findings
- CTO drafts a response plan for each finding

**Standing Critical finding — test layer coverage gap:** The reviewer checks the
CTO annotation's test_strategy against what was actually delivered. If the annotation
declared an applicable test layer (L1-L6) and the implementation has zero tests at
that layer, this is **Critical** — not Minor, not deferred. The principle: everything
that can have automated testing gets it at time of development. Missing tests at
any non-deferred applicable layer is a gap the CTO fixes at State 6. The reviewer
also flags any applicable layer the annotation failed to identify.

**Produces:** Code review results (Critical / Important / Minor findings) + CTO response plan.

**Growth Log:** After the review completes, append all Critical and Important findings
to the CTO Growth Log (see `references/cto-growth-log.md`). Minor/Suggestion findings
are not logged. The FIX APPLIED field is left blank — it gets filled at State 6.

**HARD STOP — Gate 5:**

Present the RDAI Summary plus:
- Code review findings summary
- Classification of each finding (Critical / Important / Minor)
- CTO's response plan: which findings to fix, which to push back on (with reasoning)

The orchestrator reviews the findings AND the response plan. If the orchestrator
disagrees with a push-back or wants a finding reclassified, that's addressed here
before moving to State 6.

**COACHING (Gate 5):**
> You're looking at code review findings — and more importantly, at how the CTO
> responded to them. This is where you learn to evaluate technical judgment. When the
> CTO says "fix" on a Critical finding, that's expected. When they say "push back" on
> an Important finding, read their reasoning. Does it make sense to you? You don't
> need to be a developer to evaluate whether a push-back is reasoned or defensive.
> A good push-back explains *why* the reviewer's concern doesn't apply here. A bad
> one says "it's fine" or "that's how we always do it." If you're unsure, approve
> and watch what happens at the CQO gate — the quality gate will catch it if the
> push-back was wrong. Over time, you'll develop instincts for which push-backs
> to challenge.

**Next:** State 6 (CTO Revision) on approval.

---

### State 6 — CTO: Post-Review Revision

**Action:** Load `aidlc-cto` SKILL.md. The agent adopts the CTO role.

**Work:**
- Address code review findings per the approved response plan
- Fix Critical and Important issues
- Document any push-backs with reasoning
- Annotate the changes (what was modified and why)
- **Update the CTO Growth Log:** Fill in the FIX APPLIED and PATTERN TAG fields for
  each finding logged at State 5. This completes the finding→fix pair.
- Produce an updated CTO Delivery Summary

**Produces:** Updated implementation + change annotation + revised Delivery Summary.

**HARD STOP — Gate 6:**

Present the RDAI Summary plus:
- Change annotation (what changed since Gate 4)
- Updated Delivery Summary with new test counts
- Confirmation that all Critical/Important review findings are addressed

**COACHING (Gate 6):**
> The CTO just fixed what the code review found. Compare this Gate Card to Gate 4's.
> Did the test count go up? Did new files appear that weren't in the original
> annotation? The change annotation should tell you exactly what changed and why.
> If the CTO says "addressed all Critical/Important findings" — verify that against
> the Gate 5 findings list. Agents sometimes miss items or mark them resolved when
> they've only partially addressed them. This is not distrust — it's verification.
> The same discipline you'd apply to any team member's work.

**Next:** State 7 (CPO Post-Implementation Review) on approval.

---

### State 7 — CPO: Post-Implementation Review

**Action:** Load `aidlc-cpo` SKILL.md. The agent adopts the CPO role.

**Work:**
- Review the CTO's delivery against the original Execution Brief
- Verify scope was maintained (no creep, no shortfall)
- Update Jira/Linear with implementation status
- Prepare handoff to CQO

**Produces:** CPO Implementation Review + Jira/Linear update.

**HARD STOP — Gate 7:**

Present the RDAI Summary plus:
- Scope verification: did the implementation match the brief?
- Any deviations noted and their strategic impact
- Jira/Linear update confirmation
- Handoff recommendation to CQO

**COACHING (Gate 7):**
> The CPO is checking: did we build what we said we'd build? This is a scope gate,
> not a quality gate (that's next). Read the scope verification carefully. "Exact
> match" is ideal. "Minor adjustments" is normal — implementation always reveals
> things the plan didn't anticipate. "Significant changes" is a yellow flag that
> needs your attention: why did the implementation diverge from the brief? Was it
> a legitimate discovery or did someone drift? This is also a good gate to check
> the Jira/Linear thread — does the ticket comment history tell a coherent story
> so far?

**Next:** State 8 (CQO Quality Gate) on approval.

---

### State 8 — CQO: Quality Gate

**Action:** Load `aidlc-cqo` SKILL.md. The agent adopts the CQO role.

**Work:**
- Review implementation against test spec
- Run the quality gate: tests pass, ratchet maintained, analyzer clean
- Check for slop patterns
- Check implementation against Code Best Practices KB entry (if it exists).
  Violations of **Validated Practices** are gate failures — same weight as test
  failures or ratchet regressions. Emerging and Proactive items are noted but
  do not fail the gate.
- **6-layer test coverage check:** Verify the CTO annotation's test_strategy (State 2)
  against delivered tests. Every layer the annotation declared as applicable must
  have corresponding tests in the implementation. A ticket that declares L1, L2, and
  L3 as applicable but only delivers L2 tests is a gate failure — RETURN. The only
  acceptable reason for a missing layer is an explicit project ratchet deferral with
  a specific phase reference. "We'll add it later" is not a deferral. The ratchet
  counts total tests; this check verifies the *right layers* are covered, not just
  that the number went up.
- Issue APPROVED or RETURN

**Produces:** CQO Quality Gate result.

**HARD STOP — Gate 8:**

Present the RDAI Summary plus:
- Quality gate result: APPROVED or RETURN
- Test results: pass count, coverage, ratchet delta
- Any slop patterns detected
- If RETURN: specific issues the CTO must address

**Growth Log:** If the CQO returns work (RETURN verdict), append the specific quality
issues to the CTO Growth Log as new findings with the CQO Quality Gate as the source.
These are especially valuable — they represent issues that survived the code review
and made it to the quality gate. The FIX APPLIED field gets filled when the CTO
Post-Review Revision state repeats.

**Decision tree:**
- **APPROVED** → CPO Close (next state per tier — State 9 in Full, combined gate in Express/Standard)
- **RETURN** → CTO Post-Review Revision (loops through revision → quality gate per tier sequence)
- Each CQO-CTO loop gets its own Gate Cards at each step.

**COACHING (Gate 8):**
> The CQO is your quality safety net. If the CQO says APPROVED, the work has passed
> an independent quality check — tests pass, ratchet is maintained, no slop detected.
> If the CQO says RETURN, pay attention to why. This is where you learn what "quality"
> actually means in practice. The CQO's specific issues teach you what to watch for
> earlier in future chains. Common patterns: tests that pass but don't test the right
> thing, coverage numbers that look good but miss the critical path, code that works
> but uses patterns that will break at scale. If the CQO returns work, the CTO-CQO
> loop begins — you'll see Gates 6, 7, and 8 repeat. Each loop should be shorter
> than the last. If the third loop is as long as the first, something structural
> is wrong and you should escalate.

**Next:** State 9 on APPROVED. State 6 on RETURN.

---

### State 9 — CPO: Ticket Close & Summary

**Action:** Load `aidlc-cpo` SKILL.md. The agent adopts the CPO role.

**Work:**
- Update Jira/Linear: move ticket to Done, add resolution summary
- Produce an Orchestrator Summary covering the full chain:
  what was planned, what was built, what was learned, what to watch
- Capture lessons learned and any process improvements identified
- Identify follow-up tickets if any emerged during execution

**Produces:** Orchestrator Summary + updated ticket + follow-up recommendations.

**HARD STOP — Gate 9:**

Present the RDAI Summary plus:
- Orchestrator Summary (see format below)
- Jira/Linear final status confirmation
- Lessons learned
- Follow-up ticket recommendations

**COACHING (Gate 9):**
> This is your retrospective. The Orchestrator Summary tells you the story of what
> just happened. Read the DELTA section: planned vs built. If they match, the chain
> worked well. If they diverged, the lessons learned section should explain why.
> The WHAT TO WATCH section is your early warning system for future tickets. Write
> down anything that surprised you in the Insight Journal — even small things like
> "the CTO annotation was faster this time" or "the CQO caught something I missed
> at Gate 4." These observations compound. After 5-10 chains, you'll start seeing
> patterns that make you a sharper orchestrator. This is where the learning happens.

**Next:** State 10 (Session Close) on approval.

---

### State 10 — Session Close

**Action:** Execute the session close protocol. Generate the full Chain Ledger as a
KB artifact. Capture all insights from the Insight Journal.

**Work:**
- Compile the Chain Ledger into a KB entry using the Chain Ledger KB format:

```yaml
---
kb_id: KB-[YYYYMMDD]-[HHMM]-chain-ledger
phase: [current phase]
type: session
visibility: internal
tags: [touchchain, chain-ledger, delivery]
ticket_id: [ticket ID]
chain_tier: [EXPRESS / STANDARD / FULL]
chain_gates_total: [N]
go_nogo_loops: [N]
cqo_cto_loops: [N]
story_points: [N]
sprint: [sprint name]
parent_epic: [epic ID or null]
---

[Full Chain Ledger content]
```

- Verify the persistent Insight Journal file has all entries from this session appended
  (each entry was written at the gate — confirm the session block is complete)
- Verify the persistent CTO Growth Log file has all findings from this session appended
  (findings written at Code Review and CQO gates, fixes completed at Post-Review Revision gate — confirm all pairs are complete)
- Compile the session's Insight Journal entries into a KB entry (see references/insight-journal.md)
- Compile the session's CTO Growth Log entries into a KB entry:

```yaml
---
kb_id: KB-[YYYYMMDD]-[HHMM]-cto-growth
phase: [current phase]
type: session
visibility: internal
tags: [touchchain, cto-growth, findings, patterns]
ticket_id: [ticket ID]
findings_logged: [N]
pattern_tags: [list of unique PATTERN TAGs from this session]
---

[Session's Growth Log entries]
```

- All KB entries (Chain Ledger + Insights + CTO Growth) are cross-referenced by
  ticket_id and written together
- **Practice Synthesis check:** If the CTO Growth Log has new entries since the last
  synthesis (or has never been synthesized), the agent evaluates synthesis urgency:

  **Urgency Assessment (ask at every ticket close with new findings):**
  1. Do any of this ticket's new pattern tags apply to the *next* tickets in the Epic?
     (Check the next ticket's files_to_touch, approach, and dependencies.)
  2. Would the next CTO benefit from having these patterns validated and authoritative
     *before* they start annotating?

  If YES to both → **Recommend immediate synthesis.** The learnings are perishable —
  they prevent mistakes on the very next ticket. Waiting for Epic close loses value.

  If NO (patterns are general, next tickets are unrelated) → **Recommend defer to
  Epic close.** Standard cadence. The Growth Log entries are still read by the CTO
  at States 2 and 4 regardless — synthesis adds industry validation, not awareness.

  Present to the orchestrator:
  "Growth Log has [N] new findings ([N] total, [N] unique pattern tags) since last
  synthesis. [URGENCY: immediate — patterns X, Y apply to next ticket / defer —
  next tickets are unrelated]. Run Practice Synthesis now? (yes / no / defer)"
  - If **yes**: execute the Practice Synthesis protocol (see references/practice-synthesis.md).
    Sonnet 4.6 evaluates the Growth Log against industry standards for the stack.
    Present the draft KB entry to the orchestrator for review. On approval, write the
    Code Best Practices KB entry. On rejection, note "synthesis deferred" and move on.
  - If **no** or **defer**: record the decision, move on. The Growth Log entries are
    still written — they'll be available for the next synthesis.
- Produce the session close deliverables

**Produces:** KB entries (Chain Ledger + Insight Journal + CTO Growth Log + optionally
Code Best Practices) + session close confirmation.

**HARD STOP — Gate 10 (Final):**

```
GATE 10 — SESSION CLOSE
────────────────────────
Chain completed: [YES / PARTIAL]
States traversed: [list with gate numbers]
Total gates passed: [N]
Loops: [any Go/No-Go or CQO-CTO loops, with count]

KB entries written: [list of kb_ids]
Insight Journal entries: [count]
Growth Log findings: [count] ([list of PATTERN TAGs])
Practice Synthesis: [RAN — kb_id / DEFERRED / NOT TRIGGERED (no new findings)]

Orchestrator: Confirm session close.
```

---

## Gate Card Format — RDAI Summary

Every gate produces this card. This is what the orchestrator sees at every hard stop.
The agent MUST present this card and STOP. No proceeding without orchestrator approval.

```
═══════════════════════════════════════════════════
  GATE [N] — [State Name]
  Role: [Active Role]
  Ticket: [ID] — [Title]
═══════════════════════════════════════════════════

RISKS
  [R1] [description — new or carried from prior gate]
  [R2] [description]
  (none identified)

DECISIONS
  [D1] [what was decided and why]
  [D2] [what was decided and why]
  (none — information only)

ACTIONS
  [A1] [what was done in this state]
  [A2] [what was done]

IMPACT
  [I1] [how this state's work affects the product, timeline, or quality]
  [I2] [downstream effects on subsequent states]

GOAL ALIGNMENT
  Epic/Project Goal: [restated from Gate 0]
  This state moves us toward that goal: [YES / CONCERN]
  Drift detected: [NONE / description of drift]

TICKET COMMENT
  Status: [PENDING — will write on approval]

ORCHESTRATOR DECISION
  [ ] APPROVE — proceed to State [N+1]: [next state name]
  [ ] REDIRECT — return to State [N] with notes: ___
  [ ] ESCALATE — decision needed on: ___

───────────────────────────────────────────────────
RECOMMENDATION
  Based on: [spec / brief / annotation / prior gate decisions]
  Journal: [relevant PATTERN or DECISION ref, if any — or "No applicable entries"]
  [The call + the basis. One line when aligned. More detail only when
   something needs the orchestrator's attention.
   Examples:
     "Recommend APPROVE — annotation matches brief scope and risk surface."
     "Recommend APPROVE with note — artifacts aligned. Orchestrator PATTERN
      (3 sessions) flags CTO scope underestimation on frontend work
      (ref EXSQAIASST-24/INSIGHT-2). Verify files_to_touch is complete."
     "Recommend REDIRECT — annotation adds 3 files not in the brief.
      CPO should confirm scope expansion before execution."
   Journal references follow read rules in references/insight-journal.md.
   Journal context informs — it never overrides current gate artifacts.]
───────────────────────────────────────────────────

═══════════════════════════════════════════════════
```

**Non-negotiable rules for Gate Cards:**

1. The agent produces the Gate Card and STOPS. Does not continue. Does not "assume approval."
2. Every field is filled. "None identified" is acceptable for Risks. Blank fields are not.
3. Goal Alignment is checked at every gate. If drift is detected, it is named explicitly.
4. The orchestrator's response is the ONLY thing that moves the chain forward.
5. The Jira comment header includes tier and tier-specific gate numbering:
   `[TOUCHCHAIN] Gate N of M — Role: Action` where M is the tier's total gate count
   (Express: 6, Standard: 8, Full: 10). The first comment also includes the tier:
   `[TOUCHCHAIN-EXPRESS]`, `[TOUCHCHAIN-STANDARD]`, or `[TOUCHCHAIN-FULL]`.
6. If the orchestrator raises a concern not in the RDAI, the agent addresses it before
   the gate is re-presented.
7. After approval, the agent writes the ticket comment BEFORE swapping roles. If the
   write fails, the agent reports the failure to the orchestrator immediately.
8. The RECOMMENDATION is always filled. One line when aligned. More detail only when
   something needs attention. Always references a specific artifact (spec, brief,
   annotation, prior gate decision). The agent checks the Insight Journal for
   applicable PATTERN or DECISION entries (3+ sessions for patterns) — journal
   context informs but never overrides current gate artifacts. See Journal Read
   Rules in references/insight-journal.md. If recommending REDIRECT or ESCALATE,
   states the specific conflict.

**Mandatory gate sequence — the agent presents these IN ORDER after every Gate Card:**

```
Step 1: Present the Gate Card (RDAI + all fields above)
Step 2: Present the COACHING block for this gate (if coaching mode is ON)
Step 3: Ask the gate-specific reflection question (if coaching mode is ON)
        (see references/insight-journal.md — Gate-Specific Reflection Questions)
Step 4: Ask "Anything to capture in the Insight Journal?"
Step 5: STOP. Wait for orchestrator response.
Step 6: On APPROVE — execute the post-approval writes, then swap roles:
        a. Write the ticket comment to Jira/Linear.
        b. If this is the Code Review or CQO Quality Gate state with findings:
           append findings to the CTO Growth Log (docs/aidlc/CTOGrowthLog.md).
           FIX APPLIED left blank — gets filled at Post-Review Revision state.
        c. If this is the CTO Post-Review Revision state: update Growth Log
           entries from Code Review (or CQO loop) with FIX APPLIED and
           PATTERN TAG fields.
        d. If the orchestrator provided an Insight Journal entry: append it to
           the Insight Journal (docs/aidlc/InsightJournal.md).
        e. Confirm all writes succeeded before swapping roles. If any write
           fails, report immediately — do not proceed.
```

Skipping any step is a protocol violation. Steps 2 and 3 are skipped ONLY when
coaching mode is explicitly OFF. Steps 1, 4, 5, and 6 are never skipped.
Step 6 sub-steps (a-e) execute in order. The Growth Log writes (b, c) only apply
at their specified gates — they are skipped at other gates. The Insight Journal
write (d) only executes if the orchestrator provided an entry. The ticket comment
write (a) and the completion check (e) happen at every gate.

If the agent catches itself about to swap roles without having completed Steps 1-6,
it stops and re-presents the gate. This is the same discipline as verification-before-
completion: evidence before assertions, sequence before shortcuts.

---

## Orchestrator Summary Format (State 9)

```
ORCHESTRATOR SUMMARY — [Ticket ID]
═══════════════════════════════════

WHAT WE PLANNED
  [1-2 sentences from the Execution Brief]

WHAT WE BUILT
  [1-2 sentences on what was actually delivered]

DELTA (planned vs built)
  [Exact match / Minor adjustments / Significant changes — with details]

WHAT WE LEARNED
  [Lessons from the chain — process, technical, strategic]

WHAT TO WATCH
  [Risks, tech debt, deferred items that need future attention]

FOLLOW-UPS
  [Recommended follow-up tickets, if any]

CHAIN METRICS
  Tier: [EXPRESS / STANDARD / FULL]
  States traversed: [N]
  Go/No-Go loops: [N]
  CQO-CTO fix loops: [N]
  Total gates: [N]
  Story points delivered: [N — from ticket at Gate 0]
  Sprint: [sprint name — from ticket at Gate 0]

ORCHESTRATOR GROWTH (coaching mode only)
  Decisions I made with confidence: [list]
  Decisions I was unsure about: [list — and what happened]
  Patterns I'm starting to see: [observations across this chain]
  What I'd do differently next run: [specific changes]
```

The ORCHESTRATOR GROWTH section only appears when coaching mode is ON. It's generated
by reviewing the Insight Journal entries — especially LEARNING entries — and compiling
them into a growth snapshot. This section is written to the KB as part of the session
close, tagged `internal`, so the orchestrator can track their development over time.

---

## Chain Ledger

The Chain Ledger is a running log maintained for the session. Each gate appends an entry.
At session close, the full ledger becomes a KB artifact.

```
CHAIN LEDGER — [Ticket ID] — [Date]
────────────────────────────────────

[Gate 0] SESSION OPEN — [timestamp]
  Status: APPROVED
  Orchestrator note: [any note, or "—"]

[Gate 1] CPO PLANNING — [timestamp]
  Status: APPROVED
  RDAI: [compressed 1-liner per category]
  Orchestrator note: [any note]
  Insight captured: [yes/no — ref insight-journal entry if yes]

[Gate 2] CTO ANNOTATION — [timestamp]
  Status: APPROVED
  ...

(continues for all gates)
```

---

## Skill-Swap Protocol

At each state transition, the agent performs a clean role swap:

1. **Produce the Gate Card** for the current state
2. **STOP and wait** for orchestrator approval
3. On approval, the orchestrator says something like: "Approved. Load CTO." or "Go."
4. **Read the next role's SKILL.md** from the project skill directory
5. **Adopt the new role identity** — the agent IS now the CPO, CTO, or CQO
6. **Read the previous Gate Card** as the incoming context (this is the handoff)
7. **Begin work** in the new role

**Critical:** The agent does not carry forward the previous role's reasoning or perspective.
Each role swap is a clean break. The only context that crosses the boundary is:
- The Gate Card (structured handoff)
- The Chain Ledger (running log)
- The Insight Journal (orchestrator observations)
- The ticket state in Jira/Linear
- The ticket comment thread (written at each gate — the external chain of custody)

Role bleed — where the CTO starts making CPO-style strategic calls, or the CPO starts
thinking about implementation — is a chain failure. If the orchestrator detects role bleed,
they call it at the gate and the agent re-does the work from a clean role perspective.

---

## Insight Journal Protocol

See `references/insight-journal.md` for the full protocol, entry types, and KB format.

At every hard stop, the orchestrator has the opportunity to record observations. These
are not the agent's observations — they are the human's. Pattern recognition, gut feelings,
strategic concerns, process notes, things the agent missed.

The Insight Journal is a **persistent, append-only markdown file** that lives at the
project's docs directory (default: `docs/aidlc/InsightJournal.md`). It grows across
sessions — each touchchain run appends a new session block with its entries. Over time,
this file becomes the orchestrator's institutional memory across every ticket in the
project. At session close, the current session's entries are also written to the KB
for retrieval and decay scoring.

The agent reads the journal at **State 0** to load full context, and checks it at
**every gate** when forming the Recommendation. Journal Read Rules (see
`references/insight-journal.md`) govern which entries the agent may reference —
only established PATTERNs (3+ sessions) and relevant DECISIONs. The journal informs
Recommendations; it never overrides current gate artifacts.

### Reflection Questions (coaching mode ON — ask at each gate)

| Gate | Question |
|------|----------|
| 0 | "Does the goal statement feel specific enough that you'd know if we missed it?" |
| 1 | "After reading the Execution Brief, could you explain what we're building and why to someone who just walked in?" |
| 2 | "Did anything in the CTO's annotation surprise you — a file you didn't expect, or a risk you hadn't considered?" |
| 3 | "What's your confidence level on this Go decision — high, medium, or gut says something's off?" |
| 4 | "Does the scope of what was built feel proportional to what was planned?" |
| 5 | "Which code review finding taught you something new about what to watch for?" |
| 6 | "Comparing Gate 4 to Gate 6 — did the revisions make the work better, or just different?" |
| 7 | "If you had to summarize this ticket's journey in one sentence for a teammate, what would you say?" |
| 8 | "Did the CQO catch anything that should have been caught earlier in the chain? If so, where?" |
| 9 | "What would you do differently if you ran this same ticket through the chain again?" |

After the reflection question, always follow with:
`"Anything to capture in the Insight Journal? (Observations, decisions, patterns, concerns — or 'none' to proceed)"`

---

## Practice Synthesis — Validated Best Practices

See `references/practice-synthesis.md` for the full protocol, KB entry format,
and agent read rules.

The CTO Growth Log captures raw findings. Practice Synthesis validates them against
industry standards for the project's stack and produces an authoritative KB entry:
**Code Best Practices — [Project] — [Stack]**. This is triggered by the orchestrator
at Epic boundaries or on-demand (`/synthesize-practices`).

The synthesis uses Sonnet 4.6 to evaluate Growth Log patterns against industry
standards (OWASP, framework docs, language best practices). The orchestrator reviews
and approves the output before it becomes authoritative. No synthesis goes live
without human sign-off.

Once approved, the KB entry is read by ALL agents:
- **CTO** at States 2 and 4 — build better code from the start
- **Reviewer** at State 5 — benchmark findings against validated project standards
- **CQO** at State 8 — gate on Validated Practices (not Emerging or Proactive)

This closes the full learning loop: agent mistakes → Growth Log findings → validated
best practices → all agents learn → fewer mistakes → Growth Log finds new things →
next synthesis extends the KB.

---

## Ticket Comment Protocol

**The chain does not exist if the ticket doesn't show it.** Every gate that the orchestrator
approves produces a comment on the ticket. This is non-negotiable. The ticket is the
external record of the chain — it's what stakeholders, future agents, and the orchestrator
see when they pull up the ticket in six months.

### Tracker Detection

The project's `CLAUDE.md` specifies which tracker is in use (Jira or Linear) and provides
the necessary identifiers (project key, cloud ID for Jira, team for Linear). The agent
reads this at State 0 and uses the correct MCP tool for the rest of the chain.

| Tracker | MCP Tool | Key Parameters |
|---------|----------|---------------|
| Jira | `addCommentToJiraIssue` | `cloudId` (from CLAUDE.md), `issueIdOrKey`, `commentBody`, `contentFormat: "markdown"` |
| Linear | `save_comment` | `issueId` (ticket identifier), `body` (markdown) |

If the tracker is not specified in CLAUDE.md, the agent asks the orchestrator at Gate 0.

### When to Write

A ticket comment is written **after the orchestrator approves each gate** — not before.
The comment records what happened and what was decided. It is written as part of the
gate closing sequence, before the agent swaps to the next role.

| Gate | Comment Written By | What It Records |
|------|--------------------|-----------------|
| Gate 0 | Agent (pre-role) | Session opened, context loaded, goal stated |
| Gate 1 | CPO | Execution brief delivered, Jira/Linear fields verified |
| Gate 2 | CTO | Annotation delivered, files_to_touch listed, risk surface noted |
| Gate 3 | CPO | Go/No-Go decision with rationale. If REDIRECT: what needs to change |
| Gate 4 | CTO | Implementation complete, delivery summary (files, tests, analyzer) |
| Gate 5 | CTO | Code review findings summary, response plan |
| Gate 6 | CTO | Post-review revisions, what changed and why |
| Gate 7 | CPO | Scope verification, implementation matches brief |
| Gate 8 | CQO | Quality gate result — APPROVED or RETURN with specifics |
| Gate 9 | CPO | Ticket closed, orchestrator summary, lessons learned, Growth Log pattern summary |

### Comment Format

Every ticket comment follows this structure. Keep it scannable — this is for humans
reading a ticket thread, not a KB entry.

```markdown
**[TOUCHCHAIN] Gate [N] — [State Name]**
Role: [CPO / CTO / CQO]
Date: [YYYY-MM-DD HH:MM]

**Stakeholder Summary:** [2-3 sentences in plain language — no jargon, no agent
role names, no technical internals. Written for a project manager, client, or
teammate who opened this ticket and wants to know what's happening. What did we
do, what did we decide, and are we on track? Example: "We reviewed the technical
plan for the AI test case generation feature and confirmed it covers all the
requirements. Two additional backend functions were needed to connect to Jira
securely — the team approved the scope addition. Development starts next."]

**Summary:** [1-2 sentences — what happened in this state]

**Key Decisions:**
- [Decision and rationale, or "None"]

**Risks:**
- [Active risks, or "None identified"]

**Growth Log Patterns (Gate 9 only — include in closing comment):**
- NEW: [pattern tags added this ticket, or "None"]
- APPLIED PROACTIVELY: [pattern tags from prior tickets that were applied during development]
- PREVENTED: [findings the proactive patterns caught before code review, or "None — patterns are new"]
- TOTAL: [N patterns across M tickets]

**Next:** [What happens next in the chain]

---
_Touchchain Gate [N] of [total] — [ticket_id]_
```

### Comment Rules

1. **Write after approval, not before.** The comment reflects the approved state, not a proposal.
2. **One comment per gate.** Do not combine multiple gates into one comment. The thread
   should read as a chronological chain of custody.
3. **If a gate loops (Go/No-Go or CQO-CTO), each pass gets its own comment.** The ticket
   thread shows the full history — redirects, fixes, re-reviews. Nothing is hidden.
4. **Keep it concise.** The ticket comment is a summary, not a dump. Full details live
   in the Chain Ledger and KB. The comment points to the gate number for traceability.
5. **If the comment write fails (MCP error, auth issue), the agent flags it to the
   orchestrator immediately.** The chain does not silently drop ticket documentation.

### Gate Card Addition

The Gate Card now includes a ticket comment confirmation line. After the RDAI summary
and before the orchestrator decision:

```
TICKET COMMENT
  Status: [WRITTEN — link/ref / PENDING — awaiting approval / FAILED — reason]
```

On approval, the agent writes the comment and updates the Gate Card status to WRITTEN
before swapping roles.

---

## Escalation Protocol

Some decisions cannot be made by the active agent. When this happens:

1. The agent flags it in the Gate Card under ESCALATE
2. The orchestrator makes the call
3. The decision is recorded in the Insight Journal with full rationale
4. The chain resumes from the current state with the decision applied

Escalation triggers:
- Any decision that impacts product direction or feature scope
- Any decision that changes quality standards or testing approach
- Any deviation from the approved annotation
- Any risk that was not identified in the original Execution Brief
- Any dependency on external teams or systems not previously known

---

## Red Flags — Chain Integrity

The orchestrator should watch for these at every gate:

- **Scope drift**: The implementation is solving a different problem than the brief defined
- **Role bleed**: The agent is making decisions outside its role authority
- **Goal misalignment**: The work no longer clearly serves the Epic/Project goal
- **Rubber-stamping**: The orchestrator is approving gates without reading the RDAI
- **Context loss**: The agent doesn't seem to know what happened in prior states
- **Missing RDAI fields**: Any blank or skipped field in the Gate Card
- **Assumed approval**: The agent continues past a gate without explicit sign-off

If any red flag is detected, the chain pauses. The orchestrator addresses it before
the chain resumes.

---

## Suite References

| File | Load When |
|------|----------|
| `references/insight-journal.md` | Every gate — for insight capture protocol |
| `references/cto-growth-log.md` | States 2, 4, 5, 6, 8 — CTO learning from review/CQO findings |
| `references/practice-synthesis.md` | Epic close / on-demand — validate Growth Log against industry standards |
| `../aidlc-cpo/SKILL.md` | States 1, 3, 7, 9 — CPO role states |
| `../aidlc-cto/SKILL.md` | States 2, 4, 6 — CTO role states |
| `../aidlc-cqo/SKILL.md` | State 8 — CQO quality gate |
| `../requesting-code-review/SKILL.md` | State 5 — Code review dispatch |
| `../session-open/SKILL.md` | State 0 — Session initialization |
| `../session-close/SKILL.md` | State 10 — Session close and KB write |

---

*Touchchain — Co-authored by S3 Technology & EX Squared*
*Hard stops. Human in the lead. Every transition.*
