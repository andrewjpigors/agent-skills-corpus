---
name: low-context-comms
description: >-
  Drafts and reviews low-context communication for James (informing, asking
  for help, escalating risk) per the GitLab handbook's decision-velocity
  guidance and Jamie's April 2026 ProdSec note. Use whenever sending
  cross-functional updates, status posts, MR/issue announcements, escalations,
  Slack broadcasts, or any message someone outside the immediate context
  will read. Pairs with natural-writing-style — this skill enforces the
  low-context structure on top of the writing style. Triggers: low-context,
  broadcast, announce, status update, escalate, escalation, ask for help,
  cross-functional update, ProdSec reporting update, brief the team,
  inform the team.
license: MIT
metadata:
  version: 1.0.0
  author: jhebden
allowed-tools: Read Write Edit AskUserQuestion
---

# Low-Context Communication

Write messages that don't make the reader chase down details. The recipient
might be three time zones away, two contexts behind, and reading on a phone
between meetings — give them everything they need in one pass.

This skill is the structural layer. Tone and prose style come from
[natural-writing-style](../natural-writing-style/SKILL.md); load that skill
alongside this one for any non-trivial draft.

## Quick Start

1. Decide which mode this message is — `Informing`, `Asking for help`, or `Escalating risk`
2. Load the matching template from `references/templates.md`
3. Fill every required slot — if you can't, that's a signal you need more info before sending
4. Run the low-context checklist before publishing
5. Match the channel: Slack thread vs. handbook MR vs. issue comment vs. epic update — each has its own framing rules in `references/channel-fit.md`

## When to Use

- Posting a status update to a Slack channel where most readers don't know your project
- Writing an issue/epic comment that someone outside your team will read
- Drafting a ProdSec Reporting Update entry
- Asking for help across team boundaries
- Escalating a risk to leadership
- Announcing a change that affects other teams
- Reviewing existing draft text for low-context quality

If only one teammate who already knows the full context will see the message,
this skill is overkill. Use natural-writing-style alone.

## Identity & Reference URLs

- **Author:** James Hebden — Product Security, GitLab
- **Handbook source — TeamOps decision velocity:** https://handbook.gitlab.com/teamops/decision-velocity/#low-context-communication
- **Handbook source — communication guidelines:** https://handbook.gitlab.com/handbook/communication/
- **ProdSec Reporting Updates exemplar:** https://internal.gitlab.com/handbook/security/product_security/security-platforms-architecture/product-security-reporting/
- **April 2026 ProdSec note (Jamie):** https://docs.google.com/document/d/16SYAjofflZhk9EUQ66kM21q20KrTGZY6eHR9kUfQRJo/edit

## The four pillars

Every low-context message is:

- **Explicit, not implicit.** State the ask, the status, the impact directly. Don't expect the reader to infer.
- **Direct, not indirect.** Lead with the conclusion. Background goes after, not before.
- **Simple, not complex.** Short sentences. Plain language. Acronyms expanded on first use.
- **Complete, not narrow.** Include the SSoT links, the names, the dates, the prior context. Recipient shouldn't have to ask follow-up questions.

The unifying rule: **say *why*, not just *what*.** Every announcement, update, or
decision needs both. "We're rolling out SAST scanner X" is *what*; "because Mythos-
ready depends on coverage parity by Q2" is *why*. Skipping the why is the
single biggest low-context failure.

## The three modes

Pick one before drafting. Mixing modes in a single message guarantees confusion.

### Mode 1: Informing
*"Here's the thing that happened / is happening / will happen."*

```
[problem / context]
[solution or current state]
[next steps + DRI + timing]
[where to dig deeper]
```

Use for: status posts, change announcements, completed work broadcasts,
ProdSec Reporting Updates entries.

### Mode 2: Asking for help
*"I need a specific thing. Here's what I've already tried."*

```
[problem]
[the specific ask — who / what / by when]
[what I've already tried / ruled out]
```

Use for: cross-team requests, unblocking pings, design review asks.

### Mode 3: Escalating a risk
*"This is bad in this specific way. Here's a path that still satisfies the goal."*

```
[problem]
[why it's bad — exploit path or specific bad outcome, with severity]
[proposed solution that still satisfies the original goal]
```

Use for: leadership escalations, risk register entries, blocked-on-decision
notes. Escalation only after you've genuinely exhausted your own moves —
"escalate as a last move, not a first move" (Jamie, April 2026).

Full templates with worked examples in [references/templates.md](references/templates.md).

## Required slots — fill them all

Regardless of mode, a low-context message needs every one of these:

| Slot | What goes here | Skip-able? |
|---|---|---|
| **Subject / first line** | The point. Read this and stop, you still know the gist. | Never. |
| **Why it matters** | Connection to a goal, risk, customer, or operating-model initiative. | Never. |
| **Acronym expansion** | First mention spells it out: "SAST (Static Application Security Testing)". | Skip only if the channel is exclusively SMEs. |
| **DRI** | Who owns this. Name the human, not just "the team". | Skip only if purely informational with no follow-up needed. |
| **Timing** | Date, deadline, "this week", or "no action needed". | Never. |
| **SSoT link** | GitLab issue/epic, doc, MR, or handbook page. | Skip only if the message *is* the SSoT. |
| **Prior context link** | Previous update, decision, or related thread. | Skip if first communication on this topic. |

If a slot is genuinely empty (e.g. no prior context exists), say so explicitly:
"This is the first update on this topic." Don't just leave it out — readers
will assume they missed something.

## Channel-specific framing

Different surfaces need different structures even with the same content.
See [references/channel-fit.md](references/channel-fit.md) for the full guide:

- **Slack post (broadcast):** opener line stands alone, thread holds detail
- **Slack thread reply:** restate the question, then answer
- **GitLab issue/epic comment:** lead with the action verb (Update / Decision / Question)
- **MR description:** problem → solution → impact → testing → rollback
- **Handbook MR:** the diff *is* the message; commit message explains why
- **Email / async announcement:** TL;DR header, then sections
- **ProdSec Reporting Update:** problem / current state / next steps / where to dig

## Style mechanics

These supplement natural-writing-style — read both skills' rules together.

- **Lead with the verb in headlines.** "Decided to..." / "Asking for..." / "Risk: ..." not "Some thoughts on...".
- **Concrete over abstract.** "The Mythos SAST gate blocks merge for findings >= High" beats "We're improving security gates".
- **Numbers over adjectives.** "12 services" not "several services". "By Friday 9 May" not "soon".
- **Names over roles when actionable.** "Reviewing with @jhebden" not "reviewing with the team".
- **Past / present / future, never conditional drift.** "We will" or "we are" — not "we should be".
- **One ask per message.** If you're asking for two unrelated things, send two messages.
- **No buried questions.** If there's a question, it gets its own line, ideally bolded.

## Anti-patterns — review for these before sending

- **Implicit ownership.** "We're tracking this" — who is *we*? Name the DRI.
- **Implicit urgency.** "ASAP" / "soon" / "as a priority" — give a date.
- **Soft asks.** "It would be great if someone could..." — pick a person, set a deadline.
- **Context dumps with no thesis.** Three paragraphs of background and no conclusion.
- **Conclusion buried in line 14.** Move it to line 1 and use the rest as supporting detail.
- **Acronym soup.** Especially bad: NLG, SF, PSIRT, SAST, DAST, SBOM, SLSA, CWE all in two sentences with none expanded.
- **Performative apology / over-hedging.** "Apologies if this has already been raised, just wanted to flag a small thing..." — be direct.
- **Multi-topic messages.** "Also, while I have you..." — that's a separate post.
- **Pings without re-pings.** A single Slack message is not enough; if blocked, re-ping via another channel after 24h (Jamie, April 2026).

## The pre-send checklist

Run these in order. Fix any issue, then re-run from the top.

1. **Mode declared.** Is this Informing, Asking, or Escalating? Single mode only.
2. **First-line test.** Read just the opening line. Does the reader know the gist? If no, rewrite.
3. **Why-not-just-what.** Is the *why* in the message and easy to find? If no, add it.
4. **Slot completeness.** Walk the required slots table. Every slot filled or explicitly noted as empty.
5. **Acronym sweep.** Every acronym expanded on first use? List them and check.
6. **DRI named.** Is there a human name attached to follow-up actions?
7. **Timing concrete.** "Soon" / "ASAP" / "in due course" replaced with dates or "no action needed"?
8. **One ask check.** Is there exactly one ask, or are you smuggling in a second?
9. **Stranger test.** Imagine a competent stranger from another R&D team reading this. Could they act on it without DMing you for context? If no, add what's missing.
10. **Channel-fit check.** Does the framing match the channel (Slack opener, MR description, issue comment, etc.)?
11. **Style pass via natural-writing-style.** Run that skill's quality gate on the prose.

## Reviewing existing drafts

When asked to review (not write) a message:

1. Identify which mode the author intended (or note that no mode is clear)
2. Walk the required-slots table — flag every empty slot
3. Run the pre-send checklist; for each failure, quote the offending text and propose a concrete rewrite
4. Give a final verdict: **ship as-is** / **ship with edits** / **rewrite**

Default to suggesting concrete rewrites, not abstract feedback. "This needs a clearer ask" is unhelpful; "Replace 'someone should look at this' with 'asking @sarah-w to review by Wed 14 May'" is helpful.

## Output format

When drafting:

```markdown
## (｡♥‿♥｡) Low-Context Draft — <Mode>

**Channel:** <slack-channel | issue-link | mr | email>
**Audience:** <who'll see this>
**Mode:** Informing | Asking for help | Escalating risk

---

<the draft message itself, formatted exactly as it would post>

---

### Why it works
- <one or two lines naming which slots are filled and how>

### Pre-send checklist
- [x] Mode declared
- [x] First-line test passes
- ...
```

When reviewing:

```markdown
## (¬‿¬) Low-Context Review

**Verdict:** ship as-is | ship with edits | rewrite

### Issues found
1. **<issue category>** — quoted text → suggested rewrite
2. ...

### Suggested rewrite
<full rewritten message ready to copy>
```

## Tone

Low-context doesn't mean low-warmth. The handbook is explicit: substantive
warmth (specificity, helpfulness, naming who owes what) is what makes
low-context messages feel respectful rather than transactional. Treat the
reader as a capable peer who's busy — give them what they need to act, then
get out of their way.

## References

- [references/templates.md](references/templates.md) — full templates and worked examples for each mode
- [references/channel-fit.md](references/channel-fit.md) — channel-specific framing rules
- [references/banned-phrases.md](references/banned-phrases.md) — vague language to replace
