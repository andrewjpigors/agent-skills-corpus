---
name: eval-planning
description: >
  Drafts an evaluation plan for a customer POC or POV — business decision,
  binary success criteria, scope guardrails, stakeholders, validation
  environment, and timeline — co-created with the project sponsor in a single
  90-minute meeting, then pressure-tested against the four ways evals quietly
  fail. Use when scoping a POC, preparing for an eval kickoff, drafting an
  evaluation brief, or sanity-checking a plan a sponsor sent over. Triggers on
  "draft an eval plan", "POV plan", "evaluation brief", "how should I scope
  this POC", "eval kickoff", "success criteria for this eval", or "POC scope".
---

# Eval-Planning

Produce a written evaluation plan for a customer POC or POV — the artifact the project sponsor signs onto before kickoff. The plan is six fields, co-created with the sponsor in a single 90-minute session, then pressure-tested against the four ways evals quietly fail. If the plan takes a second session to land, the planning failed. The deliverable here is something the SE can walk into the meeting with.

## When to Use

Fire on requests like:

- "Help me draft an eval plan for [account]." The SE is preparing for the planning meeting and wants a strong starting point.
- "Sponsor sent over their version of the POV plan — can you sanity-check it?" Review pass against the six fields and the four detectors.
- "How should I scope this POC?" The user is upstream of planning; verify the business decision exists (see Workflow step 1) before drafting.

Do not fire for post-eval recaps, demo planning, or first-call discovery prep. Those are different skills.

## Workflow

Run these steps in order. Each can halt and ask the user a question; halting is the correct behavior when the upstream material isn't there.

### 1. Open the session, then run the upstream questionnaire

Open with a holistic 4-beat paragraph — the SE walking in deserves a teammate's acknowledgment before any structured tool fires. Then run the upstream questionnaire as described below.

**The 4-beat opening.** The four beats are scaffolding for *how to think about* the opener; the SE sees three short paragraphs — situation acknowledgment, outcome, and contract + ready transition — with visible whitespace between them, no labels, no numbers. The four beats are:

1. **Situation acknowledgment.** Name what the SE is doing right now, in their voice. Adapts to context.
2. **Brief outcome.** One sentence — what the SE walks away with.
3. **The contract.** One sentence — what the SE contributes + time estimate.
4. **Ready check with transition.** Yes/no consent moment connected to the first concrete move.

**Two contexts for Beat 1 (and Beat 4's transition).** Read the trigger phrasing and the SE's first message together; pick the variant that fits.

- **Planning-meeting prep** — the SE is drafting a plan before the planning meeting with a sponsor. Triggers: *"draft an eval plan," "POV plan," "eval kickoff," "POC scope," "how should I scope this POC," "success criteria for this eval."*
- **Sanity-check on a sponsor draft** — the SE has a draft and wants it pressure-tested. Triggers: *"sanity-check this plan,"* *"evaluation brief"* phrased as a review request, or any phrasing that mentions an existing draft.

If context is ambiguous, lean toward planning-meeting prep — it's the more common case.

**Illustrative full paragraphs.** Adapt language to the SE's actual phrasing but match the shape and register. Emit as one paragraph; do not label the beats in the output.

*For planning-meeting prep:*

> OK, eval planning — you're preparing for the meeting where you and the sponsor co-create the plan live. Let me help you walk in with a strong starting position.
>
> By the end you'll have your eval plan drafted — the business decision, success criteria, scope in and out, named stakeholders, validation environment, and a timeline with checkpoints. Plus the agenda for the planning meeting itself. All paste-ready.
>
> I'll ask short questions as we go; runs about 10–15 minutes. Sound good? Let's start with where you are with the sponsor.

*For sanity-check on a sponsor draft:*

> Got it, sanity-check pass on a draft your sponsor sent over. Let me work through it with you against where evals quietly go off the rails.
>
> By the end you'll have your eval plan — the business decision, success criteria, scope in and out, named stakeholders, validation environment, and a timeline with checkpoints. Plus the agenda for the planning meeting itself. All paste-ready.
>
> I'll ask short questions as we go; runs about 10–15 minutes. Sound good? Let's start by checking what the draft says on the three things every eval has to answer.

Wait for the SE's acknowledgment of the ready check before running the AskUserQuestion below.

The skill needs three answers locked in before drafting: (a) the specific deal outcome a successful eval will drive, (b) the named decision-maker who will drive it, (c) the date or business event the decision is feeding into. Run a two-beat structure — elicit answers from the SE first, then surface a targeted halt for whichever items come back fuzzy. Do not draft until the three items are concrete, or the SE has explicitly acknowledged the gap(s) and asked for a partial plan.

**Say to the SE before the call.** Emit this preamble verbatim before firing the AskUserQuestion tool:

> *Three questions before we draft anything. Without these locked, even a passed eval ends with "interesting results, let's talk again" — they thread through every field that follows.*

**How to elicit.** Use Claude's built-in `AskUserQuestion` tool. It presents 2-4 clickable options per question, automatically appends a free-text "Other" field, and accepts up to four questions in one call. Make a single call with three questions, one per upstream item. `multiSelect` stays off — each question wants one answer. Do not add an "Other" option manually; the tool provides it.

**Suggested question shape.** Concrete options should match the kind of eval the SE described — adapt them. The escape-hatch options are fixed and exist because honest gap-reporting is more useful than guessed answers.

| Question | Concrete options (illustrative — adapt to the eval) | Escape-hatch options |
|---|---|---|
| What specific deal outcome will a successful eval drive? | Sign a contract / master agreement · Fund a rollout / pilot expansion · Replace the incumbent | Sponsor hasn't named the deal outcome yet |
| Who is the named decision-maker — the person who will drive that outcome? | Project sponsor (verbally confirmed) · VP / exec sponsor above the project sponsor | Sponsor likely, not yet confirmed · Decision-maker above sponsor, unnamed |
| What date or business event anchors the decision? | Board review on [date] · Renewal cycle ending [date] · Budget close / Q-end planning | No hard date — eval is open-ended |

**Escape-hatches are gap signals, not approvals.** Selecting one identifies *which* upstream item is gapped; it does not let the SE skip the gate. If the SE picks "Other" and the free-text answer is itself fuzzy — any synonym of "validate the approach," "demonstrate value," "prove the technology," or "build the case" — treat that answer as an escape-hatch selection on that item. Fuzz on the deal-outcome answer is the Unaimed Evaluation trigger arriving early; do not let it through.

**Targeted halt messages.** For each gapped item, surface the corresponding halt verbatim. Multiple gaps → surface multiple halts. Do not summarize, do not soften.

- *Deal outcome gap:* "The eval needs a specific deal outcome before kickoff. Without one, the eval produces results everyone agrees are interesting and no one acts on. The discovery question to bring back to the sponsor and AE: *'What changes for the business if this eval lands — sign what, fund what, replace what?'* Get the answer in their words, not paraphrased. Loop back when you have it."

- *Decision-maker gap:* "The decision-maker isn't pinned. The eval can't safely begin without the named person who walks out of wrap-up with a signed action. The discovery question to bring to the AE: *'If the eval succeeds, who has to be the one to sign — you, or someone above?'* Get them on the wrap-up calendar before kickoff. If authority kicks up, that's the upstream gap — surface it now, not later."

- *Date / business-event gap:* "The eval has no date anchor. Open-ended evals lose momentum, miss the window, and end without deciding anything. The discovery question to bring back to the sponsor: *'What business event forces this decision? A board review, a renewal, a budget cycle?'* If the answer is 'nothing specific,' the deal isn't being prioritized internally — that itself is the finding, and the AE should know."

**Partial-plan fallback.** After surfacing the targeted halt(s), the SE may want a working draft to iterate on while they close the gap offline. Honor that — but surface the gap first; never offer the partial as a way to skip the halt. The partial plan carries the gapped field(s) marked `[NEEDS: <gap statement>]` (the same convention used in Step 2). State at the top of the output that the plan is partial and not ready to walk into the planning meeting with. The Quality Checklist will flag the unfilled field on the way out — that flag is the point.

Only proceed to Step 2 when all three items are answered concretely, or when the SE has explicitly acknowledged the gap(s) and asked for the partial-plan fallback.

**Thread-specifics — two prose questions before per-field drafting.** When all three upstream answers come back concrete, emit:

> *Before we start drafting, two specifics that'll thread through the whole plan.*

Then ask the SE in prose:

- **Q-end specificity — conditional.** Only ask if the anchor-date answer was "Budget close / Q-end planning" or otherwise Q-end-flavored without a specific date. Phrasing: *"Which Q-end? Budget close / Q-end planning could be this quarter or next. Give me the specific budget-close or Q-end date the exec sponsor is feeding this decision into."* If the SE already provided a specific date in the upstream answer, skip this question.
- **Customer name — always ask.** Phrasing: *"Customer name for the plan header (so the artifact is paste-ready when we finish)."*

Both answers come from the SE in plain prose — no AskUserQuestion needed. Once in hand, substitute the customer name into subsequent user-facing prose (replacing any `[customer]` placeholder) and resolve the anchor date to the specific Q-end date in the business-decision sentence.

### 2. Draft the six fields, one consultative beat at a time

Step 2 runs as six consultative beats — one per field. Each beat self-assesses which of three modes to run in: **propose-and-iterate**, **ask-then-draft**, or **hybrid**. The structured option sets for the beats that call AskUserQuestion live in `references/per-field-questions.md`.

**Self-assessment per beat.** Before each per-field beat, Claude assesses how much accumulated context (upstream answers + thread-specifics + the SE's trigger phrasing + deal shape from their first message + prior beat results) it has for this field. Three modes:

**Propose-and-iterate** — accumulated context gives enough signal to draft the field directly. Skill drafts, SE iterates via confirm. No AskUserQuestion call. Beat structure: field intro (which carries the explanation bridge naming context-derived defaults) → draft → confirm.

**Ask-then-draft** — field content depends on org-specific knowledge Claude doesn't have. Skill asks via AskUserQuestion before drafting anything. Beat structure: field intro → AskUserQuestion preamble (≤2 sentences immediately before the tool call — TUI clip constraint, see Step 1) → AskUserQuestion call → detector pre-fire (if triggered) → explanation bridge → draft → confirm.

**Hybrid (propose-default + conditional-ask)** — partial context. Universal defaults are inferable from deal shape or the source's discipline; scenario-specific specifics need SE input. Skill proposes the universal defaults inline AND asks for the scenario-specific gap. Hybrid varies by beat in how the propose-vs-ask split lands. Three sub-shapes:

- **Additive** — propose a universal list inline; ask in prose for additions, removals, or in-scope exceptions. (Beat 2.3.) Fallback to ask-then-draft via `references/per-field-questions.md` §2.3 only when deal shape doesn't suggest universal defaults at all.
- **Posture-vs-details** — propose the discipline-aligned posture inline; ask in prose for sub-item specifics. (Beat 2.5.) No AskUserQuestion call; the propose path is the discipline-aligned default backstopped by the relevant detector pre-fire.
- **Default-vs-override** — propose a discipline-aligned default inline; ask via AskUserQuestion only when override pressure is detected in accumulated context. (Beat 2.6.) Override-pressure signals: AE-driven short kickoff window, anchor date < 4 weeks out, SE-mentioned urgency, any sub-three-week constraint surfaced in trigger or upstream answers.

The three hybrid sub-shapes share the propose-inline + ask-for-gap structure but differ in *what* gets asked and *how*. The propose path doesn't soften the gate — when an SE explicitly overrides a discipline-aligned default, the relevant detector pre-fire (Sandboxed Proof, Two-Week Flame, Empty Chair) backstops at the next step. The discipline runs at two layers: mode propose AND detector pre-fire.

The mode mapping below is the lock for the eval-planning skill. Future skills with additional beats apply the same self-assessment logic.

| Beat | Mode | Routing rationale |
|---|---|---|
| 2.1 Business decision | Propose-and-iterate | Upstream + thread-specifics give 3 of 4 if-then parts; deal shape gives the IF clause. |
| 2.2 Binary success criteria | Propose-and-iterate | Deal shape narrows the criteria space to 2–3 stereotyped picks for this eval type. |
| 2.3 Scope guardrails | Hybrid (additive) | Universal out-of-scope items inferable from vertical and eval type; scenario-specific items need SE input. |
| 2.4 Stakeholders | Ask-then-draft | Customer's org chart is opaque to skill. |
| 2.5 Validation environment | Hybrid (posture-vs-details) | Sandbox-first posture is the discipline-aligned default; sub-item specifics (IdP, apps, test data) need SE input. |
| 2.6 Timeline and checkpoints | Hybrid (default-vs-override) | Three-week default is discipline-aligned (Two-Week Flame backstop); ask only when override pressure exists. |

Across Step 2: one unconditional AskUserQuestion call (Beat 2.4) plus one conditional (Beat 2.6 on override-pressure detection), plus rare fallbacks (Beat 2.3 when deal shape gives no defaults). With the upstream intake from Step 1, the skill makes 2–3 AskUserQuestion calls in a typical session.

**Full re-emit on iteration.** When the SE asks to change part of a drafted multi-element field (criteria, scope items, stakeholders, validation environment sub-items, timeline elements), the skill re-emits the full updated state of that field as a block-quote — not just the changed item. Diff-only emit treats the skill as a patcher; full re-emit treats it as a co-drafter and lets the SE check the items still hang together as a group. Single-sentence fields (business decision) trivially satisfy this since the iteration is the full re-emit.

Each beat applies its mode's structure below.

#### 2.1 Business decision

**Mode.** Propose-and-iterate. Upstream + thread-specifics give the decision-maker, the deal outcome, and the anchor date; deal shape (industry vertical, eval type, customer-side capabilities) gives the fourth part — the observable outcome at wrap-up.

**Field intro + explanation bridge (user-facing).** Emit at the start of the beat, immediately after thread-specifics resolve. This text carries both the bridge (framing the propose-and-iterate move) and the field intro (naming what's non-obvious about the business decision):

> *Got it. Now I'll fold those three answers into one sentence — the business decision. It's the spine of the plan; every other field below exists to make this sentence true or false at wrap-up. The form: If [observable outcome] is true at wrap-up, [decision-maker] will [specific deal outcome] by [date]. Drafting:*

**Draft.** Apply the if-then template. The IF clause comes from inferring the observable outcome from the deal shape — e.g., for an FSI workforce-auth eval with security-led board readout, the IF clause is "passwordless authentication is verified working against [customer]'s top-five enterprise applications and clears security review against the board-readout criteria." Substitute the customer name (from thread-specifics), the decision-maker (from upstream), the deal outcome (from upstream), and the anchor date (from thread-specifics) into the template. Emit as a single block-quoted sentence.

**Anti-pattern halt.** If the deal shape contains fuzzy verbs as the success criterion ("demonstrate value," "validate the approach," "prove the technology," "build the case") and Claude has no concrete observable to anchor the IF clause to, treat as the Unaimed Evaluation trigger arriving inside Step 2: surface the deal-outcome targeted halt from Step 1 and offer to mark the field `[NEEDS: <gap>]`.

**Confirm.** Surface the drafted sentence and ask in prose: *"Sound right, or want to adjust before we move to success criteria?"* If the SE confirms, lock the field and proceed to 2.2. If they want a tightening, emit the full updated sentence as a block-quote (single-sentence fields trivially satisfy the full re-emit requirement), then re-ask. After two non-converging iterations, halt and surface the gap — the field has more upstream work than Step 2 can resolve in this session. The confirm beat is not skippable; do not proceed to 2.2 without an explicit confirmation or an acknowledged NEEDS mark.

#### 2.2 Binary success criteria

**Mode.** Propose-and-iterate. Deal shape narrows the criteria space to 2–3 stereotyped picks for this eval type; skill drafts three by default, SE adjusts via confirm.

**Field intro + explanation bridge (user-facing).** Emit at the start of the beat, after 2.1's confirm clears. The field intro names what binary criteria require; the bridge names the context-derived defaults:

> *Success criteria next. The binary pass/fail items — three to five — you'll run against [customer]'s own data and environment to decide if the eval succeeds. Each needs a specific behavior under named conditions and a measurable threshold that resolves to true or false without interpretation.*
>
> *From the deal shape — [2–3 deal characteristics that anchor the criteria choices, e.g., "passwordless workforce auth at an FSI prospect, security-led board readout as the anchor"] — three earn their place by default:*

**Draft.** Generate three binary criteria from deal shape. Each criterion has three structural dimensions worth comparing across rows — *Behavior*, *Conditions*, and *Pass threshold* — so emit as a block-quoted markdown table with columns `# | Behavior | Conditions | Pass threshold`. Use concrete verbs in Behavior (*completes, rejects, achieves, returns, resolves*) — never fuzzy verbs (*demonstrates, validates, approaches, evaluates, improves*). Conditions names the customer-environment specifics; Pass threshold names the measurable binary outcome.

**Confirm.** Ask in prose: *"Any of these wrong for this deal? Want to swap one out, add a fourth, drop to two?"* If the SE wants a change, emit the full updated list of criteria as a block-quote (full re-emit, not just the changed item), then re-ask. Two-iteration safety valve.

**Edge cases.**
- If the SE proposes more than five total, name the Two-Week Flame trigger explicitly and ask which two should move to post-purchase rollout.
- If the SE accepts fewer than three after iteration, mark `[NEEDS: criterion 2]` (or 3) rather than padding.
- If an SE-proposed criterion uses fuzzy verbs ("demonstrate auth," "validate the approach"), surface the fuzzy-verb anti-pattern in prose and ask for a concrete behavior + measurable threshold.

#### 2.3 Scope guardrails

**Mode.** Hybrid (additive). Universal out-of-scope items for the vertical-and-eval-type are inferable from deal shape; scenario-specific items the customer surfaced in discovery need SE input. Propose the universal list inline; ask in prose for additions, removals, or in-scope-by-exception markers.

**Field intro (user-facing, 3–4 sentences).** Emit at the start of the beat, after 2.2's confirm clears:

> *Scope guardrails next. The out-of-scope list — items the customer asked about during discovery that aren't on the path to the deal outcome, each paired with a one-line reason and where it goes instead (post-purchase rollout, separate workstream). The list does most of its work in the planning meeting: when the sponsor pushes for new scope mid-meeting, the reason is what holds the line. Walking in with this drafted gives you a strong point of view that's hard to dictate against.*

**Explanation bridge (1 sentence).** Emit, naming the count and the deal-shape inference:

> *From the deal shape — [eval type + industry vertical, e.g., "workforce-identity POC in financial services"] — [N] out-of-scope items earn their place by default:*

**Propose-inline (universal defaults from deal shape).** Draft 4–5 universal out-of-scope items as the starting list. For workforce-identity POCs the defaults are: B2B partner authentication, mobile/BYOD endpoints, identity governance/lifecycle automation, custom branding/theming, legacy app migration. For other deal shapes (CIAM, SIEM, EDR, MDM, etc.), adapt the universal defaults to the eval type — Claude infers the 4–5 items most commonly out-of-scope for this kind of eval. Each item has three structural dimensions — *Item*, *Reason*, *Where it goes* — so emit as a block-quoted markdown table:

> | Item | Reason | Where it goes |
> |---|---|---|
> | B2B partner authentication (federated identity) | Outside the IT-pain-reduction storyline driving this eval | Post-purchase rollout workstream |
> | Mobile / BYOD endpoints | Corp-managed devices only for v1 | Phase 2 |
> | Identity governance / lifecycle automation | Separate product line | Separate eval cycle |
> | Custom branding / theming | Post-purchase polish | Separate workstream |
> | Legacy app migration (apps that need rebuilding) | Phase 2 integration scope | Phase 2 |

**Fallback to ask-then-draft.** If deal shape doesn't suggest universal defaults — rare; the SE may have triggered with too little context to infer the vertical and eval type — fall back to ask-then-draft using §2.3 of `references/per-field-questions.md`. The fallback preserves the field's structural shape without runtime improvisation on the option set.

**Ask-for-scenario-specific (prose, NOT AskUserQuestion).** After the inline defaults emit, ask:

> *Anything from your discovery that needs to go on this list — or come off it? Sponsor flagged a legacy app or B2B integration as in-scope-by-exception?*

The SE responds with additions, removals, or in-scope-by-exception markers.

**Draft.** Update the table based on the SE's response:
- Add scenario-specific items as new rows with Item / Reason / Where it goes filled in.
- For in-scope-by-exception items, prefix the Item cell with `**In-scope by exception:**` and put the sponsor's discovery rationale in the Reason cell. Place these rows at the bottom of the table.
- Remove rows for any universal defaults the SE explicitly rejected (e.g., if the deal does cover mobile, drop the Mobile / BYOD endpoints row).

**NEEDS path.** If the SE can't enumerate scenario-specific items because the in-scope picture isn't pinned (e.g., *"sponsor hasn't said what's in, can't say what's out"*), the field carries `[NEEDS: scope boundaries from sponsor]` — the gap is upstream. The universal defaults still ride into the plan; the NEEDS marker says "this list is partial." Empty out-of-scope lists where the SE explicitly removed every universal default without adding anything are a different state: a Two-Week Flame trigger — surface that warning before locking the field.

**Confirm.** Ask in prose: *"Does this cover what the sponsor asked about that doesn't belong in this eval? Anything missing or mis-categorized?"* If the SE wants a change, emit the full updated table as a block-quote (full re-emit, including universal defaults plus SE additions), then re-ask. Two-iteration safety valve. Lock the field and proceed to 2.4 on confirmation.

#### 2.4 Stakeholders

**Mode.** Ask-then-draft. Customer's org chart is opaque to skill without asking.

**Field intro (user-facing, 3–4 sentences).** Emit at the start of the beat, after 2.3's confirm clears:

> *Stakeholders next. Every name on this list needs three attached items: their role label (security, IT, identity, compliance, app owner, exec sponsor), their stated interest (what they need the eval to show before they sign off), and the committed meeting (kickoff/checkpoint/wrap-up they'll be in the room for, on the calendar, accepted). The most common reason a technical win doesn't convert is a missing security or risk owner on this list — IT feels convenience, security owns risk, both need to be there.*

**AskUserQuestion preamble (≤2 sentences immediately before the call).** Emit:

> *Who's in the room for this eval — pick all that apply:*

**Ask.** Read §2.4 of `references/per-field-questions.md`. Make the AskUserQuestion call with the multiSelect setting per the references file (multi-pick is natural here since several roles can be engaged simultaneously).

**Detector pre-fire (Empty Chair).** If the SE's picks roll up through one organizational function (typically IT-only — Project sponsor + App owners but no Security / risk owner), Empty Chair is pre-triggering. Before drafting the stakeholder table, surface the warning in-beat:

> *⚠ One thing to flag before we draft the stakeholder list.*
>
> > *"This eval is being approved by the audience that feels convenience; it will be vetoed by the audience that owns risk. Approval here does not predict purchase."*
>
> *Your stakeholder list rolls up through IT operations. Security has equities in the board review at the anchor date — they will weigh in on whether the eval result is acceptable, whether or not they're in the room today. If you walk into the planning meeting without a named security counterpart, the sponsor may resist naming one ("we don't need them involved yet") — that resistance goes in the plan as a known political risk.*
>
> *The move before the planning meeting: ask the sponsor, in their words, "Before we kick off, who on the security side has to be comfortable for this to convert?" If they can produce a name, the eval has a real chance. If they can't, the eval is testing the wrong thing.*

Then ask the SE: *"I'll draft the stakeholder table with security/risk marked as a gap to close. Want me to also draft the sponsor-facing ask you'd take to your next touch?"*

If the SE accepts, draft both the table and the sponsor-facing ask. If the SE can name a security/risk counterpart on the spot, add them to the draft list and skip the sponsor-facing ask.

If Empty Chair did not pre-fire (security/risk was picked or the engagement spans multiple functions), skip the warning block and proceed directly to the explanation bridge below.

**Explanation bridge.** Emit:

> *Got it. Drafting the stakeholder table with role, stated interest, and committed meeting per named contact.*

**Draft.** Emit the stakeholder table as a block-quoted markdown table with four columns: Role | Name | Stated interest | Committed to. Each row has all four cells filled or marked with explicit gap notation. Any role that fired the Empty Chair detector goes in the table with `**NEEDS: name from sponsor by planning meeting**` in the Name cell; the warning rides into Step 3 (structural failure-mode check) too — defense in depth. If the SE accepted the sponsor-facing ask, emit it after the table as a block-quoted italicized paragraph.

**Confirm.** Ask in prose: *"Each role has a named person, a stated interest, and a meeting they're committed to. Anyone missing or any `TBD` we need to close before kickoff?"* If the SE wants a change, emit the full updated table as a block-quote (full re-emit), then re-ask. Two-iteration safety valve. Lock the field and proceed to 2.5.

#### 2.5 Validation environment

**Mode.** Hybrid (posture-vs-details). Sandbox-first posture is the discipline-aligned default (curated source §3.3, Sandboxed Proof koan); sub-item specifics (integration surface, auth flow path, test data) need SE input. Propose the posture inline; ask in prose for sub-item details. No AskUserQuestion call.

**Field intro (user-facing, 2–3 sentences).** Emit at the start of the beat, after 2.4's confirm clears:

> *Validation environment next. The technical description of the test bed — integration surface (named systems and versions), auth flow path (direction and boundaries), test data (real / test / anonymized / synthetic), and sandbox-vs-production posture. The discipline here: "their stack" is not a description, and a kickoff that hand-waves the environment produces "it works in our lab" meeting "in ours, it does not."*

**Propose-inline POSTURE (sandbox-first as discipline-aligned default).** Emit the explanation bridge naming the posture:

> *Sandbox-first locks in — the eval runs in your mirror of [customer]'s stack before anything touches their production. That discipline is what prevents the production-shortcut failure mode. I'll draft the four sub-items now, marking any specifics you don't have yet as NEEDS:*

**Detector pre-fire branch (Sandboxed Proof).** Sandbox-first is the proposed default. If the SE explicitly overrides the posture in prose (e.g., *"we don't have time for a sandbox, going straight to production"* or *"customer wants this in their prod tenant"*) — Sandboxed Proof is pre-triggering. Surface its warning from `references/anti-patterns.md` §3 in-beat before drafting; the warning rides into the field itself. Do not soften the warning even if the SE asserts production-first; that resistance is exactly what the detector is meant to surface.

**Ask-for-sub-item-specifics (prose, NOT AskUserQuestion).** After the posture lands, draft the four sub-items as a block-quoted markdown table. For each sub-item the SE hasn't specified in accumulated context, ask one prose follow-up incorporated inline — typical asks: *"Which identity provider?"*, *"Which app set?"*, *"Real users or synthetic test accounts?"*. Substitute the SE's answers into the table cells as they arrive. Any sub-item specific the SE can't name carries `[NEEDS: <specific piece>]` inline in its Specifics cell.

**Draft.** Each sub-item has two structural dimensions — *Sub-item* (the labeled aspect) and *Specifics* (the named systems, paths, data, or posture) — so emit as a block-quoted markdown table with columns `Sub-item | Specifics`:

> | Sub-item | Specifics |
> |---|---|
> | Integration surface | [customer]'s identity provider [NEEDS: vendor + version with their IT]; top-five enterprise apps via SAML/OIDC [NEEDS: app list from inventory]; corp-managed Windows + macOS endpoints; SIEM connector [NEEDS: vendor] |
> | Auth flow path | end-user → device passkey → identity provider → app via SAML/OIDC. Boundary crossings: device-to-IdP (cloud), IdP-to-app (cloud) |
> | Test data | pilot cohort of 50 users from a single business unit [NEEDS: which unit]; no production user data; phishing simulation runs against test accounts only |
> | Sandbox vs. production | SE-prepared sandbox mirroring [customer]'s IdP and the top-five apps in their staging tenant. Production only after sandbox passes; staged rollout, never broader during the eval |

**Operational test (post-draft, before confirm).** Surface one line: *"One operational test before the planning meeting — if you can't draw [customer]'s auth flow on a whiteboard from memory, technical discovery isn't finished. Finish it before walking in with this section."*

**Confirm.** Ask in prose: *"Does this match the environment we'll actually be testing in? Anything in the integration surface or auth flow that's still loose?"* If the SE wants a change, emit the full updated table as a block-quote (full re-emit of all four sub-items as table rows), then re-ask. Two-iteration safety valve. Lock the field and proceed to 2.6.

#### 2.6 Timeline and checkpoints

**Mode.** Hybrid (default-vs-override). Three-week default is the discipline-aligned timeline (curated source §3.4, Two-Week Flame koan: "two weeks if possible, three at the outside"). Propose the default inline; ask via AskUserQuestion only when override pressure is detected.

**Field intro (user-facing, 3–4 sentences).** Emit at the start of the beat, after 2.5's confirm clears:

> *Timeline next.*
>
> *Kickoff, checkpoints, wrap-up — each pinned in a real calendar invite before the planning meeting ends, not "scheduled later." The constraints: kickoff within a week of planning, wrap-up at most three weeks after, checkpoints every two-to-three days, decision-maker on the wrap-up invite. An intense eval forces priority and ends in a decision; a slow one breeds amnesia and leaves the sponsor chasing ghosts.*

**Override-pressure detection.** Before deciding propose-default or ask-on-override, check accumulated context for any of these signals:

- AE-driven short kickoff window mentioned in trigger or thread-specifics (e.g., *"AE wants kickoff next Friday"*).
- Anchor date < 4 weeks out from today, leaving little margin for a standard three-week eval.
- SE-mentioned urgency in trigger phrasing or upstream answers (e.g., *"board review in 10 weeks"* alongside *"kickoff next Friday"*).
- Sub-three-week constraint surfaced anywhere in accumulated context.

If any signal present → **ask-on-override branch.** Otherwise → **propose-default branch.**

**Propose-default branch (no override pressure detected).** Emit the explanation bridge naming the three-week default:

> *Three weeks — within the safe range. I'll pin kickoff [date, within one week of planning meeting], wrap-up three weeks later with [decision-maker] on the invite, checkpoints every two-to-three days, and the same-day AE recap. Then surface two phrases you'll need to bring into the planning meeting verbatim.*

Skip to the Draft block below. No AskUserQuestion call.

**Ask-on-override branch (override pressure detected).** Emit the AskUserQuestion preamble (≤2 sentences):

> *AE pressure on this one is real. What shape do you want to plan for?*

Then make the AskUserQuestion call: read §2.6 of `references/per-field-questions.md`, fire with `multiSelect: false`.

**Detector pre-fire (Two-Week Flame).** If the SE picked the four-weeks option or longer (or, in the propose-default branch, the SE explicitly pushes back to a longer timeline), Two-Week Flame is pre-triggering. Surface its warning and remediation from `references/anti-patterns.md` §4 in-beat before drafting any dates; ask which scope items can move to a post-purchase rollout list to cut the timeline. If the SE picked open-ended, the Step 1 date-anchor halt re-surfaces here — Step 2 is not the place to drift past a Step 1 gap.

**Explanation bridge (ask-on-override branch only).** After SE picks a timeline shape, emit (adapt to picked option — example for three-weeks):

> *Three weeks — within the safe range. I'll pin kickoff, the checkpoint cadence, the wrap-up with the exec sponsor on the invite, and the same-day AE recap. Then surface two phrases you'll need to bring into the planning meeting verbatim.*

**Draft.** Emit the timeline as a block-quoted bullet list (kickoff date, checkpoint cadence with named days where possible, wrap-up date with decision-maker attending, same-day AE recap). If specific dates are still fuzzy beyond the Step 1 anchor (e.g., *"wrap-up date depends on procurement, no fixed date yet"*), draft with placeholder dates relative to the anchor and mark the unfilled specifics — for example, `[NEEDS: procurement-dependent wrap-up date]`.

Then emit the two protective phrases for the planning meeting. Each as a block-quoted italicized sentence with one sentence of context:

- The timeline-protection phrase: *"We've found that evals longer than two to three weeks lose momentum and end inconclusively — let's design this one to decide."* Said once, calmly, in response to the first scope expansion or timeline stretch.
- The scheduling-in-the-room phrase: *"Let's get these on the calendar now so we don't have to chase them later."* If the sponsor offers to send invites afterward, offer to do it together right now. Resistance to scheduling-in-the-room is itself a signal.

**Confirm.** Ask in prose: *"Kickoff date, checkpoint cadence, wrap-up date with decision-maker, AE recap same day. Anything stretching past three weeks, or any date that needs a calendar check before we run detectors?"* If the SE wants a change, emit the full updated timeline as a block-quote (full re-emit, including the protective phrases), then re-ask. Two-iteration safety valve. Once locked, proceed to Step 3 — run the four detectors against the completed draft.

### 3. Run the four failure-mode checks

Walk the draft against each failure-mode check in `references/anti-patterns.md` and surface any that fire. Each check has a trigger condition, a warning to put in front of the user, and a concrete remediation — surface all three when a check fires. Do not soften the warning text; the bluntness is the point. The four checks (with their internal-traceability koan names in parentheses):

- **Decision gap** *(unaimed eval)* — the plan has no business-decision sentence.
- **Risk audience gap** *(empty chair)* — the stakeholder list shows only one organizational function.
- **Production-shortcut** *(sandboxed proof)* — non-trivial deployment goes straight to customer production.
- **Slipping timeline** *(two-week flame)* — timeline exceeds three weeks, or criteria exceed five.

In the markdown emit, the descriptive labels are primary; the koan parenthetical accompanies only the two less-self-descriptive labels (Decision gap, Risk audience gap) for source-traceability. Production-shortcut and Slipping timeline stand alone.

**Failure-mode check status values.** Each check resolves to one of four statuses, recorded in the plan's Failure-mode check section:

- **PASS** — no trigger condition met; the discipline this detector enforces is intact in the draft.
- **FAIL** — trigger condition met; emit the warning + remediation. The plan ships with this finding visible.
- **PASS (qualified)** — discipline-aligned posture present, but contingent on sub-item specifics still loose (e.g., sandbox-first stated but IdP/app list/test data still NEEDS). The qualifier names what makes the pass contingent.
- **PASS (watch)** — currently passing but a live risk could flip it during execution (e.g., timeline within three weeks but AE pressure plus a near-term board window could push it past). The watch note names the live risk.

Use the qualified/watch statuses when honest assessment requires nuance beyond pure pass/fail.

### 4. Attach the planning-meeting agenda

The plan lands in the eval-management tool with the sponsor watching, inside a 90-minute working session with a specific shape. Pull the three-part agenda and the signal markers (what tells the SE the plan is going to land vs. die quietly) from `references/planning-meeting.md` and attach them to the plan output as a separate **Planning meeting** section. Don't paste the whole reference inline — summarize the agenda and pick the signal markers most likely to surface for this specific plan.

### 5. Emit the plan

Use the Output Format below. After the plan, write the Planning meeting section. Then run the Quality Checklist before delivering. Once the markdown plan emits and the SE confirms, proceed to Step 6 — the PDF render offer.

### 6. Offer the shareable PDF render

After the markdown plan emits and the SE has confirmed, the skill offers a *shareable* PDF render via Typst. **Shareable is the load-bearing word.** The markdown above is the SE's internal-working copy — pasted into the eval-management tool, NEEDS markers visible, failure-mode check rides along for the SE's own QA. The PDF is the artifact the SE actually sends to the sponsor, the security counterpart, or the exec audience — different audience, different content.

What the shareable PDF differs from the markdown on:

- **Cover block** at the top: customer name, plan status (Draft pre-kickoff, Final post-kickoff), prepared date, planning-meeting date, plan version. None of this is in the markdown.
- **NEEDS markers** in body prose become `TBD`; the gaps move to an **Open Items** appendix at the end of the PDF. The inline `[NEEDS: <what>]` form is internal-only.
- **Failure-mode check section** is **omitted entirely** from the PDF. That section is the SE's internal QA; showing it to the sponsor signals doubt about a plan the sponsor is being asked to sign onto.
- **Descriptive labels only** (Decision gap, Risk audience gap, Production-shortcut, Slipping timeline) wherever they appear at all in the PDF — typically only in the Open Items appendix if a failure-mode-related action item rides along. **Never** koan names (Empty Chair, Two-Week Flame, Sandboxed Proof, Unaimed Evaluation) in a doc the sponsor sees.
- **Fixed table column widths**, especially stakeholder (Role narrow, Name medium, Stated interest wide, Committed to narrow) — sized to prevent paragraph-shape content wrapping into vertical-letter-stacks.
- **Single-page stakeholder block** where possible; if it must break, audience-grouped (sponsor + decision-maker on page 1, security + compliance on page 2), not row-broken.

**Check typst availability first.** Run `command -v typst` via Bash. Branch on the result:

- **If typst is installed** (command returns a path, exit 0): emit the offer (text below).
- **If typst is absent** (command returns nothing, exit 1): do not emit the render offer. Instead, append one short line to the conversation, after the markdown plan: *"Shareable PDF render via Typst is available if you install typst — see [typst.app](https://typst.app) for install instructions."* The skill is complete; the markdown plan stands on its own as the internal-working copy.

**If typst is available, emit the offer:**

> *Want a shareable PDF version too? The markdown above is your internal-working copy (paste into the eval-management tool, NEEDS markers stay visible, failure-mode check rides along). The PDF is what you'd actually send to the sponsor or share with the exec audience — cover block, NEEDS-markers cleaned up as TBD-with-open-items, no internal QA section. I can render it via Typst.*

**If the SE accepts, render:**

1. Read the Typst template at `references/plan-template.typ`.
2. Derive the customer slug from the customer name captured in Step 1's thread-specifics:
   - Lowercase the customer name.
   - Replace whitespace and non-alphanumeric characters with hyphens (`-`).
   - Collapse multiple consecutive hyphens into one.
   - Strip leading and trailing hyphens.
   - Example: *"Globex Federal Bank"* → `globex-federal-bank`.
3. **Fallback.** If the customer name is missing or thread-specifics didn't capture it, derive the slug from today's date as `eval-plan-YYYY-MM-DD` (e.g., `eval-plan-2026-05-11`). Do not block the render on a missing customer name.
4. **Determine plan status.** Default to *"Draft — to be confirmed at planning meeting on [planning-meeting-date]"* for any first emit before kickoff. If the SE indicates kickoff has happened and they're re-rendering a finalized plan, use *"Final — agreed at planning meeting [planning-meeting-date]"*.
5. **Substitute cover-block fields** into the template: `{{customer_name}}`, `{{status_line}}`, `{{prepared_date}}` (today's date), `{{planning_meeting_date}}` (from thread-specifics + AE context; if unknown, leave as `[TBD]`), `{{plan_version}}` (default `v0.1 — Draft`).
6. **Substitute body fields**: `{{business_decision}}`, `{{criteria}}` (success criteria rows), `{{scope_items}}` (scope rows), `{{stakeholder_table}}` (stakeholder rows), `{{validation_env}}` (validation env rows), `{{timeline}}` (timeline bullets). **Do not substitute any failure-mode-check content** — the template omits that section entirely.
7. **Transform NEEDS markers in body cells.** For every `[NEEDS: <what>]` in the markdown's field contents, replace with `TBD` in the corresponding PDF cell. Collect each gap into the Open Items appendix data with three fields: *Field of origin*, *Item* (the `<what>`), *Action to close* (derived from the related discovery question or detector remediation if any; otherwise the SE's stated path to close, or "Confirm with [appropriate party]" as a generic fallback).
8. **Substitute `{{open_items}}`** with the collected gap table. If zero NEEDS markers were collected, substitute the marker with an empty string — the template's Open Items section omits entirely when empty.
9. Save the substituted source as `eval-plan-<customer-slug>.typ`.
10. Run `typst compile eval-plan-<customer-slug>.typ eval-plan-<customer-slug>.pdf` via Bash.
11. **On success,** confirm: *"Done. `eval-plan-<customer-slug>.pdf` is saved alongside this conversation — cover, body, Open Items appendix. The markdown above stays as your internal-working copy."*
12. **On `typst compile` failure** (template syntax error, missing fonts, etc.), surface the stderr and offer to share the `.typ` source: *"typst compile failed: [error]. The `.typ` source is saved if you'd like to compile it elsewhere, or share me the error and I can adjust. The markdown above is still paste-ready as your internal-working copy."*

### 7. Close with specific next moves and the landing signal

After the markdown plan emits (Step 5) and the PDF render either completes, is declined, or is skipped because typst is absent (Step 6), emit two short paragraphs to close the session. This closing is unconditional — it runs whether or not the PDF render fired.

**Paragraph 1 — Specific next moves.** Pull from:

- Any `[NEEDS: ...]` markers in the plan (each becomes a "close before kickoff" action item).
- Any detector findings with status FAIL or PASS (qualified) — the remediation is the action item.
- Any sub-item specifics still loose (validation environment NEEDS, decision-maker name TBD, etc.).

Emit as an ordered list under a heading naming the count: "Two things to close before the planning meeting:", "Three things to close...", etc. Each item is one line stating the specific action + (where relevant) where the discovery question for it lives in the plan ("The discovery question is above"). Items that pull from FAILed detectors reference the warning + remediation from `references/anti-patterns.md` indirectly via the action language, not by detector name.

**Paragraph 2 — Landing signal.** One sentence naming the live signal the SE should watch for in the planning meeting itself. Pick from `references/planning-meeting.md` the "landing" signal most relevant to this specific plan's NEEDS markers and detector findings — typically the marker that would close the biggest open gap.

Example (for a plan with a risk-audience gap + validation NEEDS markers):

> *Two things to close before the planning meeting:*
>
> *1. Bring back the sponsor's named security counterpart. The discovery question is above.*
> *2. Confirm [customer]'s IdP version and the top-five app names in the validation environment section.*
>
> *You'll know the planning meeting is landing when the sponsor names that security counterpart unprompted and edits the plan live in the eval-management tool, rather than asking for time to review. Good luck.*

The closing prose is not an AskUserQuestion or confirm beat — it's a session-end emission. No iteration, no two-iteration safety valve. The skill ends here.

## Output Format

Produce the plan as a markdown block the SE can paste into the eval-management tool. Sections in this order:

```markdown
# Eval Plan — [Customer]

## Business decision
If [observable outcome] is true at wrap-up, [named decision-maker] will [specific deal outcome] by [date].

## Binary success criteria
| # | Behavior | Conditions | Pass threshold |
|---|---|---|---|
| 1 | [Specific behavior] | [Named customer-environment conditions] | [Measurable threshold] |
| 2 | [...] | [...] | [...] |
| 3 | [...] | [...] | [...] |

(Three to five rows total. More than five risks stretching the eval past the safe window.)

## Scope guardrails (out of scope)
| Item | Reason | Where it goes |
|---|---|---|
| [Item] | [One-line reason it's excluded] | [Post-purchase rollout / Phase 2 / separate workstream] |
| [Item] | [Reason] | [Where] |
| **In-scope by exception:** [Item] | [Sponsor's discovery rationale] | In-scope — verify integration |

## Stakeholders
| Role | Name | Stated interest | Committed to |
|---|---|---|---|
| Project sponsor | [Name] | [What they need to see] | Kickoff, all checkpoints, wrap-up |
| Security / risk owner | [Name] | [What they need to see] | Kickoff, wrap-up |
| Decision-maker (exec sponsor) | [Name] | [Business decision above] | Wrap-up |
| [Other role] | [Name] | [Stated interest] | [Meetings] |

## Validation environment
| Sub-item | Specifics |
|---|---|
| Integration surface | [Named systems, categories, versions] |
| Auth flow path | [Direction, credentials, boundaries crossed] |
| Test data | [Real / test / anonymized / synthetic — named] |
| Sandbox vs. production | Sandbox first, SE-prepared, mirroring the customer's stack. Production only after sandbox passes, in stages. |

## Timeline
- Kickoff: [date, within one week of planning meeting].
- Checkpoint cadence: every 2–3 days.
- Wrap-up: [date, ≤3 weeks after kickoff], decision-maker attending.
- Internal AE recap: same day as planning meeting.

## Failure-mode check
| Check | Status | Detail |
|---|---|---|
| Decision gap (unaimed eval) | [PASS / FAIL / PASS (qualified) / PASS (watch)] | [Note: what's intact or what fired] |
| Risk audience gap (empty chair) | [PASS / FAIL / PASS (qualified) / PASS (watch)] | [Note] |
| Production-shortcut | [PASS / FAIL / PASS (qualified) / PASS (watch)] | [Note] |
| Slipping timeline | [PASS / FAIL / PASS (qualified) / PASS (watch)] | [Note] |
```

Then append:

```markdown
## Planning meeting
- **Who's in the room:** project sponsor + SE, AE supporting. Not the broader customer team — that comes back at kickoff.
- **Length:** 90 minutes minimum. Shorter is an agenda review, not a planning session.
- **Three parts:** (1) confirm success criteria (~30 min), (2) edit the plan live in the eval-management tool with the sponsor watching (~40 min), (3) schedule kickoff, checkpoints, and wrap-up with invites going out before the meeting ends (~20 min).
- **Signals to watch for:** [pull 2–3 markers from references/planning-meeting.md that match this specific plan — typically a mix of one "landing" signal and one "dying" signal to watch].
- **Same-day follow-ups:** AE recap; internal note that planning is complete. Customer does not get access to the plan in the eval-management tool until kickoff.
```

## Quality Checklist

Verify each item before delivering. If any fails, fix it or surface the gap to the user with a halt message — do not silently ship a plan with a hole.

- The business decision is present and contains all four parts: observable outcome, decision-maker, deal outcome, date.
- If the plan carries any `[NEEDS: ...]` markers, the output explicitly states it is partial and not ready for the planning meeting. The gap statement matches the targeted halt the SE acknowledged in Step 1.
- Every success criterion is binary. No "improve," "demonstrate," "validate," "approach," or "evaluate" verbs.
- Success criteria list has 3–5 entries.
- Scope-out list is non-empty. An empty list is a Two-Week Flame trigger.
- Stakeholder table contains a named security or risk owner. If absent, the Empty Chair detector fires and its warning runs.
- Project sponsor commitment is verbal-confirmed, not "scheduled to confirm."
- Validation environment specifies sandbox vs. production explicitly.
- Timeline from kickoff to wrap-up is ≤3 weeks.
- Checkpoint cadence is ≤3 days.
- Wrap-up has the decision-maker on the calendar invite.
- All four detectors have run and their results are noted in the plan.
- No identifying customer names appear in the plan beyond the customer the SE is working with on this specific eval.

## Resources

- `references/anti-patterns.md` — the four detectors with trigger, warning, and remediation. Read in full before running Workflow step 3.
- `references/planning-meeting.md` — the 90-minute meeting structure plus the signal markers that distinguish a plan that will land from one that will die quietly. Read when preparing the agenda in Workflow step 4.
- `references/per-field-questions.md` — structured AskUserQuestion option sets for the ask-then-draft beats (2.3–2.6). Read the corresponding section before each AskUserQuestion call in Step 2.
- `references/plan-template.typ` — Typst source template for the PDF render. Used in Workflow step 6 when typst is available and the SE accepts the render offer. Carries placeholder markers (`{{customer_name}}`, `{{business_decision}}`, etc.) for substitution from the plan's field values.
