---
name: digital-estate-inventory
description: "Interactive tool for capturing the information and access paths your executor, attorney, partner, or family will need to manage your affairs if you die or become incapacitated. Produces a structured inventory — not a legal estate plan. Works alongside (not instead of) a qualified attorney."
---

# Digital Estate Inventory

**What this skill is:** A structured interview and capture tool. It helps you produce an organized record of your accounts, assets, credentials, contacts, wishes, and access paths — the information your people will need if they suddenly have to act on your behalf. It also produces a short **Break Glass Kit** — the minimum they need in the first hours.

**What this skill is NOT:**
- **Not a legal estate plan.** A legal estate plan is a set of legally operative instruments (will, power of attorney, advance directive, trust, or their jurisdiction-appropriate equivalents) executed with the formalities your jurisdiction requires. Those documents are created with a qualified attorney. This skill does not produce them.
- **Not legal advice.** The outputs of this skill are reference material — they do not grant authority, transfer ownership, or legally bind anyone.
- **Not financial or tax advice.**
- **Not a substitute for talking to your people.** The documentation is only useful if the right people know it exists and can get to it.

**How to think about the outputs:** Everything this skill produces is inventory and orientation material meant to sit *next to* your legal documents — not replace them. Think of it the way a business continuity plan sits next to incorporation documents: the legal papers grant authority; the runbook tells people what to actually do with it.

## Attribution

This skill was **inspired by** the work of the **Death & The Digital Estate Community Group (DADE CG)** at the **[OpenID Foundation](https://openid.net)** — in particular:

- The **[Digital Estate Planning Guide](https://openid.net/wp-content/uploads/2026/03/Digital-Estate-Planning-Guide-1.pdf)** (DADE CG, March 2026), which shaped the session structure and the categories this skill asks about.
- The companion whitepaper **[The Unfinished Digital Estate: Culture, Law, and Technology After Death](https://openid.net/wp-content/uploads/2026/03/The-Unfinished-Digital-Estate-Final.pdf)** (Flanagan, Kiser, Saxe; March 2026), which provides the research foundation for why digital estate planning matters — covering cultural perspectives, abuse threat models, delegation semantics, and the global regulatory landscape.

This skill is an independent work inspired by those documents; it is not a DADE CG or OpenID Foundation publication. For more on DADE CG, visit: https://openid.net/cg/death-and-the-digital-estate/

---

## IMPORTANT DISCLAIMERS

> **THIS IS NOT LEGAL ADVICE.**
>
> This skill provides general guidance for digital estate inventory work, inspired by the OpenID Foundation's Digital Estate Planning Guide. It is not intended, and should not be construed, as legal advice regarding any matter or jurisdiction.
>
> **You SHOULD consult a qualified estate attorney** for advice tailored to your circumstances and jurisdiction. Laws governing access to digital accounts after death vary by location. Accessing someone's account without proper authorization may violate laws or terms of service — even if done with the express wishes of the account owner.
>
> **You MUST verify** that the instructions and suggestions provided by this skill are appropriate and secure for your specific situation. The skill cannot account for your unique legal, technical, or personal circumstances.
>
> Neither this skill's author, the OpenID Foundation, nor the DADE CG makes any representations or warranties regarding the legal accuracy or implications of the guidance provided.
>
> **Laws governing digital assets after death vary dramatically by jurisdiction.** Consult legal counsel in your jurisdiction for guidance on fiduciary access to digital assets, credit monitoring, government benefit notification, and estate administration.

---

## How This Skill Works

### Modes

**Plan mode (default):** Build your own digital estate plan. The skill walks you through sessions, each covering one domain of your digital life. Complete them in order or jump to what matters most.

**Break Glass Kit mode:** Don't want the full plan yet? Build just the minimum your family needs to access your accounts in an emergency. Sessions 1 (Keys) + 2 (Financial/Autopay) + a condensed executor quick reference. Can be done in one sitting. Incomplete answers are fine — document what you know, flag what's missing. Users can always upgrade from break glass to full plan later.

**Quick Win mode:** Don't have time for 13 sessions? Do three things in 30 minutes that prevent 80% of the damage. See "Minimum Viable Plan" below.

**Reactive mode:** You're managing someone else's digital estate after death or incapacitation. The skill provides a time-sensitive triage checklist focused on stabilizing the situation.

**Test mode (harness-only — not an end-user mode):** Takes a *persona fixture* (a YAML file describing pre-filled Session 0 facts, plugin selections, and any canned per-session answers) and runs the full skill non-interactively, producing the same session files and consolidated artifacts that Plan mode would. Used by the automated test harness in `tests/` to verify plugin activation, layer / facet composition, and output structure. Not advertised to end users; never offered as a path on the "which mode?" prompt. See `tests/README.md` and the **Test mode contract** below for the persona format, output contract, and graceful-degradation behavior.

### First question: which mode?

**Before anything else, ask the user which mode they want:**

> "Two paths forward. Which do you want?
> 1. **Break Glass Kit** — the minimum your family needs to access your accounts in an emergency. ~1 hour. Start here if you want something useful today.
> 2. **Full Digital Estate Plan** — comprehensive inventory across 12 sessions. Multiple sittings. Start here if you want to do this thoroughly."

A partial plan with gaps flagged is infinitely better than no plan. Never block on missing information — always capture what's known and move on.

### Session-Based Design

Digital estate planning is overwhelming if you try to do it all at once. This skill breaks it into **focused sessions** — each one takes 15–30 minutes and produces a concrete output document. You can stop after any session and pick up later.

### Couples Planning

Couples planning is handled by the `coupled` facet (`plugins/facet/coupled.md`). The facet activates whenever the user is planning together with a partner — legally married, civil-union / registered partnership, cohabiting, engaged, or any other committed pair — and adapts the session structure to joint + individual sessions producing ONE plan with both partners' content clearly labeled by partner. The substantive guidance (joint-vs-individual session breakdown, authorized-user recommendations, family-plan continuity, partner cross-access) lives in the facet.

**"Both of us" simultaneous-loss scenario:** stays in core (this section). It applies to **any** multi-person planning structure, not only married couples — divorced co-parents with shared minor children, chosen-family co-trustees, business partners, and so on all have the same issue. The principle: if both lead actors in a plan are unavailable at once, the secondary executor and technical support person need access instructions, contact info for each other, and a clear playbook. Address explicitly in Session 10 and Session 12.

### Separation and Divorce

Lifecycle facets handle the substantive content:

- **Separated but not yet divorced** — see `plugins/facet/separated-not-divorced.md`. Activates when the user is legally married but practically separated and divorce is not yet final. Covers the high-risk interim period (the separated spouse is typically still the legal next of kin and default beneficiary), what to update unilaterally now (powers of attorney, beneficiary designations, disposition-of-remains directive, medical-records release authorization, platform legacy contacts), and the silent-access audit. The facet also carries the safety callout for separations involving domestic violence, coercive control, or stalking — change passwords and recovery methods **before** any visible change to shared accounts.
- **Divorce finalized** — see `plugins/facet/divorced.md`. Treats divorce as a trigger for a **full plan audit**, not an incremental update, and lists the categories of action: beneficiary-designation re-cascade across every plan administrator and institution, will and trust review, POA / healthcare-proxy / disposition / medical-records-release replacement, guardianship-nomination review where minor children are involved, password-manager and platform-legacy-contact cleanup, real-property retitling per the decree, decree-mandated insurance-maintenance constraints, and re-running the jurisdiction analysis if the divorce included a move.

The facets are jurisdiction-neutral. Specific revocation rules, statutory citations, and tax mechanics live in the jurisdiction plugin.

### Death vs. Incapacity

These are DIFFERENT scenarios and the skill addresses both:
- **Death:** Executor gets legal authority through probate. Legacy contacts activate. Accounts can be memorialized or closed.
- **Incapacity:** Person is alive but cannot act. Power of attorney agent needs CURRENT access to pay bills, manage accounts, and maintain services. Legacy contacts DO NOT activate. You cannot memorialize a living person's accounts. Bills still need to be paid. Services must continue.

Every session should prompt the user to consider BOTH scenarios: "What happens if you die?" AND "What happens if you have a stroke tomorrow and can't act for 6 months?"

### Session Priority by Situation

Not everyone needs the same session order. After Session 0, adapt:

| User Situation | Highest Priority Sessions | Why |
|---------------|--------------------------|-----|
| Single, younger | 1 (Keys), 2 (Financial), 10 (Storage) | Nobody else knows anything — master key access is existential |
| Couple, no kids | 1 (Keys), 2 (Financial), 6 (Devices/Smart Home) | Cross-access between partners, shared infrastructure |
| Parents with minors | 0 (Legal!), 2 (Financial), 6 (Children's accounts) | Will/guardian MUST be current; kids' lives must continue |
| Business owner | 1 (Keys), 4 (Digital Property/Business), 2 (Financial) | Business continuity can't wait; client obligations |
| Older adult | 3 (Insurance/LTC), 1 (Keys), 5 (Media) | Incapacity is primary risk; LTC policy is critical; photos are irreplaceable |
| Crypto holder | 1 (Keys), 2 (Financial/Crypto) | Irreversible loss — seed phrase or nothing |

### What You'll Produce

Two categories of output — keep them distinct. The skill produces both.

**1. The Break Glass Kit (`break-glass-kit.md`)** — a short, urgent, stress-readable document (5-10 pages) for the person making decisions in the first hours and days. Written for someone who is tired, scared, and not technical. Answers: where do I start, how do I get into the password manager, what must not lapse this week, who do I call first.

The Break Glass Kit is a *subset* of the full inventory — the parts that matter at 3 a.m. It is not comprehensive. It points to the full inventory for anything beyond the immediate crisis.

**2. The Comprehensive Inventory** — the detailed, session-by-session record of the user's digital and non-digital estate. This is reference material for later weeks and months — working through accounts, claims, closures, transfers, and legal administration. Includes:
- Individual session documents covering each domain of your digital life and non-digital assets
- A consolidated **Quick Reference** for whoever administers the estate — under whatever that role is called in the user's jurisdiction
- A **First 48 Hours Checklist** — time-critical actions (this is what the Break Glass Kit distills from)
- An **Attorney Brief** — a one-pager to bring to the jurisdiction-appropriate legal professional
- A **Jurisdictional Assumptions** document — what jurisdiction(s) the plan assumes, what terminology is used, what was adapted or skipped
- An **Action Items list** — consolidated, deduplicated, categorized task list of what the planner still needs to do

**Why the split matters:** In a crisis, no one reads 100 pages. They read the short document that tells them what to do in the next hour. Everything else is reference material they'll consult over weeks and months. Writing these as one blob means the urgent stuff gets buried. Keep them separate.

---

## UPDATE MODE

A plan only works if it's current. Use Update Mode when the user has an existing plan from a prior run and wants to refresh it — after a life change (move, job change, marriage, new child, separation, divorce, health event), after a large financial change, or on a routine annual review. For **separation and divorce specifically**, see the "Separation and Divorce" section above — separation is a high-risk interim period and divorce should trigger a full audit, not just a diff.

Update Mode is NOT "redo the interview." It's a targeted diff: what changed, what's gone, what's new.

### Input

The user points the skill at their existing plan directory. This directory should contain the session files from a previous run (`00-orientation.md`, `00-jurisdictional-assumptions.md`, `01-keys-to-everything.md`, … `12-attorney-brief.md`, `break-glass-kit.md`, `action-items.md`, etc.).

Ask: *"Where is your existing plan? Give me the directory path."* Verify the directory exists and contains recognizable session files before proceeding.

### Workflow

**Step 1 — Load the prior state.** Read every session file. Extract a compact inventory for your own reference:
- Accounts (email, financial, digital property, subscriptions)
- People (executor/administrator, technical support person, attorney, financial advisor, insurance agent, secondary contacts)
- Assets (property, vehicles, equipment with registrations)
- Loans and liabilities
- Insurance policies
- Devices
- Digital services (including mobile money, platform legacy contacts configured)

Also note the **last reviewed date** on each file.

**Step 2 — Walk the user through by category, not by session.** For each of these buckets, show the user a short summary of what's on record and ask three questions:

> Here's what's on record for [category]:
> - [bulleted list]
>
> Three quick questions:
> 1. Anything NEW to add?
> 2. Anything that no longer applies?
> 3. Anything that has CHANGED?

Process buckets in this order (most likely to have changes first):
1. Financial accounts and loans
2. Insurance and employer benefits
3. Subscriptions
4. People (contacts, roles)
5. Devices and infrastructure
6. Digital property and professional accounts
7. Legacy contacts and platform settings
8. Communication/wishes
9. Media and memories
10. Real property

Keep each bucket to one screenful. Don't dump the full plan.

**Step 3 — Life-change triggers.** Ask explicitly about changes the user might not associate with the plan:
- Have you moved, changed jobs, changed marital status, had a child, or had a significant health event since the last update?
- Have any of your named people (executor, attorney, financial advisor, technical support person, insurance agent) changed roles, moved, or passed away?
- Have any of your minor children turned 18 or otherwise aged into new legal status?
- Have you acquired or disposed of property, vehicles, or major assets?
- Have you added or closed any financial accounts, credit cards, or loans?
- Have you changed password managers or added new credential stores?

For any "yes," follow up to understand the specific change.

**Step 4 — Apply the changes.**
- **New items:** append to the relevant session file's inventory table or list.
- **Removed items:** do not delete. Mark as `~~struck through~~` or append `[REMOVED YYYY-MM-DD — reason]`. This preserves an audit trail and makes the change visible to anyone reviewing history.
- **Changed items:** edit in place; note the change date in a footnote or table cell if the change affects access, beneficiaries, or authority.

**Step 5 — Propagate to the Break Glass Kit.** Any change that touches the critical path — master key location, first-call contacts, critical bills, primary accounts — must flow into `break-glass-kit.md`. The kit being stale is worse than the full inventory being stale, because the kit is what gets read first in a crisis.

**Step 6 — Regenerate `action-items.md`.** Rebuild the consolidated action item list based on the current state of all session files. New gaps become new items; closed gaps come off the list.

**Step 7 — Update metadata.** Bump the `Last verified` or `Last updated` date on each modified file and on the Break Glass Kit. If the skill produced a Jurisdictional Assumptions document, re-check whether anything there needs updating (moved jurisdictions, new cross-border exposure).

**Step 8 — Present a change summary.** Before closing the session, show the user a compact summary:
- Added (N items)
- Removed (N items, marked in place)
- Changed (N items)
- Files touched
- New action items
- Items that have rolled off the action list

Ask: "Does this match what you intended? Anything missed?"

### What Update Mode does NOT do

- Re-interview the user from scratch
- Re-generate session files that have no changes
- Silently delete historical content (always mark removals in place with a date)
- Skip the Break Glass Kit update — that's the whole point of keeping it current

### When to recommend a full re-run instead

If more than ~30% of the plan is stale, or a major life event has restructured the user's situation (divorce, relocation to a new country, loss of a named executor), recommend a full Plan Mode re-run instead of an update. Say so explicitly: *"There's enough change here that an update will miss things. I'd recommend running the full sessions again — you can reuse most of the existing content as starting material."*

---

## MINIMUM VIABLE PLAN (Quick Win Mode)

If the user is short on time or overwhelmed, offer this. Three actions, 30 minutes, prevents 80% of the worst outcomes:

### Action 1: Document your master key (10 minutes)
Whatever unlocks everything else — password manager emergency kit, the notebook in the drawer, the memorized master password — write it down and put it where your executor can find it. If you use a password manager, print the emergency kit. If you don't, write down the password to your primary email account. Put it in an envelope, seal it, write "OPEN ONLY IN EMERGENCY" on it, and give it to your executor or put it in a safe.

**Test it.** Can your executor actually use what you gave them to get in? If you haven't tested it, it's not a plan — it's a hope.

### Action 2: Configure legacy contacts (15 minutes)
- **Apple:** Settings → [Your Name] → Sign-In & Security → Legacy Contact. Add your executor.
- **Google:** myaccount.google.com → Data & privacy → Inactive Account Manager. Set notification contacts and inactivity timeout.
- **Facebook:** Settings → Memorialization Settings. Choose legacy contact or deletion.

These are the three platforms most likely to lock out your family permanently.

### Action 3: Tell someone (5 minutes)
Call your executor. Say: "I have a digital estate plan. Here's where to find it: [location]. If something happens to me, start there." If you don't have an executor, tell the person you'd trust most.

**Output:** `quick-win-plan.md`

**Then come back and do the full sessions when you're ready.**

---

## OPTIONAL: Email Discovery Scan

**This step requires explicit user opt-in. Never access email without it.**

Email is one of the richest sources of estate-relevant information — subscription receipts, insurance policy documents, loan statements, utility bills, and financial account notifications all flow through it. An email scan can surface accounts the user has forgotten about and fill gaps in sessions 2 (financial), 3 (insurance/property), and 9 (subscriptions).

### Offering the scan

After Session 0 (or at the start of sessions 2, 3, or 9 where more data would help), offer it once:

> "I can optionally scan your email to help discover subscriptions, bills, insurance policies, and financial accounts for your plan. I'll run targeted searches — I won't read personal conversations. This requires an email connection. Want to try it, or would you prefer to fill everything in manually? (You can also ask me to run the scan at any point.)"

**If the user declines:** Proceed without it. Don't re-offer proactively — but run it immediately if the user asks for it at any point during any session.

**If the user agrees:** Check whether an email connector is available by looking at your current tool list for Gmail, Outlook, or other email MCP integrations. If none is available, tell the user clearly: "I don't have an email connection available in this session. You can add one in your Claude settings and run this again, or continue manually."

### Running the scan

Run searches in batches by category. For each result, surface it as a **candidate** — never add it to the plan automatically. The user confirms, corrects, or dismisses each one.

Present findings as a simple table per category:

| Found | Sender / Service | What it looks like | Add to plan? |
|-------|-----------------|-------------------|-------------|
| Netflix subscription | netflix@mailer.netflix.com | Monthly $22.99 | Y / N |
| Allstate renewal | allstate@email.allstate.com | Home + auto policy | Y / N |

**Searches to run by session target:**

*Session 2 — Financial accounts and loans:*
- `"account statement" OR "your statement is ready"`
- `"payment confirmation" OR "payment received"`
- `"loan statement" OR "mortgage statement"`
- `"annual fee" OR "membership fee"`

*Session 3 — Insurance and property:*
- `"insurance policy" OR "policy renewal" OR "premium due"`
- `"homeowners" OR "auto insurance" OR "life insurance" OR "umbrella"`
- `"property tax" OR "HOA" OR "homeowners association"`

*Session 9 — Subscriptions and recurring charges:*
- `"subscription" OR "your subscription" OR "renewal reminder"`
- `"receipt" OR "invoice" OR "billing statement"`
- `"free trial" OR "trial ending"`
- `"cancel anytime" OR "manage your subscription"`

**For each search:** retrieve recent results (past 12 months is a good window), extract sender, subject, and approximate amount where visible. Do not read full message bodies unless the user asks you to.

### Privacy and scope boundaries

- Only run the searches listed above — don't explore beyond the stated categories
- Don't read, quote, or store personal message content
- If a search returns results that are clearly personal (family emails, medical, legal correspondence), skip them silently
- When done, tell the user what categories you searched and how many candidates you found
- The user controls what gets added — nothing is automatic

### After the scan

Fold confirmed findings into the appropriate session documents. Flag any that need follow-up (e.g., a subscription found but credentials unknown, an insurance policy with no policy number visible). Unconfirmed candidates are discarded.

---

## PLAN MODE — Sessions

When the user invokes this skill, determine which mode they need:
- Full plan → start with Session 0
- Quick win → jump to Minimum Viable Plan above
- Reactive → jump to Reactive Mode below
- Resuming → pick up where they left off
- Email scan → offer after Session 0 or at the start of sessions 2, 3, or 9

### Session 0: Orientation & Jurisdictional Context

**Goal:** Understand what a digital estate is, map the people, establish the legal and cultural context the plan will operate in, and adapt the rest of the skill accordingly.

This skill was originally authored in a US/individualist framing. Estate law, succession practice, cultural expectations around death, and the practical institutions involved differ dramatically across jurisdictions. Before proceeding, this session establishes context so the rest of the sessions can be adapted appropriately.

#### Step 0 — Expertise check and existing work

Before the jurisdictional interview, ask two calibration questions:

1. **"How familiar are you with digital estate planning?"** If the answer is "very" (security professional, attorney, standards author, someone who already teaches this), **skip the orientation lecture in Step 4.** Go straight to the substantive sessions. Offer to explain anything on request, but don't walk a domain expert through "what is a digital estate."

2. **"Have you already started documenting this anywhere — a notes file, a spreadsheet, a GitHub repo, a document in your safe?"** If yes, treat it as the foundation and fill gaps. Don't rebuild what exists. Ask to see it (or a summary) so the skill's output aligns with what's already there.

**Ask these one at a time, waiting for each answer.** The rest of Session 0 also follows the one-question-at-a-time rule — never fire 10 questions in a block. It's a conversation, not a form. Power users may bulk-answer; let them. But don't default to bulk-question format.

#### Step 1 — Jurisdictional discovery

Ask the user:
- **Where do you live primarily?** (Country and, where relevant, state/province/prefecture)
- **Where are your assets located?** (Property in other countries, foreign bank accounts, investments held abroad)
- **Do you have multiple citizenships or long-term residency in more than one country?**
- **Do your likely heirs live in other countries?**
- **Is your marriage or partnership recognized the same way everywhere it matters?** (Customary, civil, religious, common-law, same-sex, polygamous — recognition varies)
- **Are there family or cultural traditions that shape how estates are handled in your community?** (Extended-family decision-making, eldest-child succession, customary law, religious authority, communal property, oral-tradition succession)

Surface multi-jurisdictional exposure explicitly. A US citizen with German real estate, a Japanese national with a US brokerage, or a Ghanaian with family land and a London flat each have materially different situations that downstream sessions need to acknowledge.

#### Step 2 — Research the jurisdictional context

**Use web search to research the user's primary jurisdiction (and any others with significant exposure) before continuing.** Do not rely on your pretrained knowledge alone — succession law, registries, and common practice change, and the skill must not repeat the US defaults when they don't apply.

Search for:
- The succession/inheritance law framework (statutory scheme, any forced-heirship or reserved-portion rules, treatment of community/marital property)
- Terminology actually used in that jurisdiction for: the person who administers an estate, the legal instrument that grants them authority, the legal document expressing wishes at death, and the instrument for decision-making during incapacity
- Required formalities for wills and powers of attorney (notarization, witnesses, registration)
- Any national registries for wills, advance directives, or property (e.g., Germany's Zentrales Testamentsregister and Vorsorgeregister, land registries, beneficial ownership registries)
- Common digital services that matter locally but not globally (mobile money in much of sub-Saharan Africa and South Asia; LINE in Japan; Kakao in Korea; regional banks, insurers, and telecoms)
- Cultural norms around discussing death and succession

**Cite what you find.** When you surface information to the user, link to the source you used. Say "this is what my research indicates — correct me if it doesn't match your experience."

#### Step 3 — Produce the Jurisdictional Assumptions document

Write `00-jurisdictional-assumptions.md` before starting the substantive sessions. It should contain:

- **Primary jurisdiction** and any secondary jurisdictions with exposure
- **Key terminology this plan will use** — the jurisdiction-appropriate terms for "executor," "probate/administration," "will," "POA," "incapacity agent." Default US terms are used *only* if the user's jurisdiction is US.
- **Legal framework summary** — 2–3 sentences summarizing how succession works in the primary jurisdiction, with sources
- **Forced-heirship or reserved-portion rules** — if they exist, state that they exist and that the user's attorney will advise on their effect. Do not attempt to interpret them.
- **Formality requirements** — does this jurisdiction require notarized wills? Registered POAs? Note this so later sessions don't assume markdown documents are legally operative.
- **Registries to consider** — any national or regional registries the user should be aware of (wills, advance directives, real estate, beneficial ownership)
- **Locally significant services** — mobile money, regional banks, dominant social/messaging platforms, telecoms
- **Cultural and family-structure context** — what the user told you about how their family handles these decisions
- **Sections of this skill that are being adapted or skipped** for this user — e.g., "Credit bureau freeze guidance is US-specific and does not apply here"; "Customary successor role will be documented alongside statutory administrator"

This document shapes every subsequent session. When a session has US-default content that doesn't apply, note the adaptation in the session output.

#### Step 4 — Walk the user through the basics

Once the jurisdictional context is set, walk the user through:

1. What a digital estate includes (it's more than passwords — photos, messages, financial accounts, subscriptions, domains, code, social media, devices, cloud storage, local data, smart home, loyalty programs, browsing history, and jurisdiction-specific services like mobile money or regional platforms)
2. The "personas" concept from the guide — personal, professional, parent, volunteer, community, religious, and family roles. Each may have different accounts with different handling instructions. Ask: "Do you manage any accounts on behalf of organizations, clubs, HOAs, volunteer groups, religious communities, or extended family?"
3. What happens without a plan (lost memories, ongoing charges, fraud exposure, legal barriers, family conflict — and in some jurisdictions, frozen accounts and administrative paralysis until formal authority is granted)
4. The 7-step roadmap from the guide, adapted to jurisdiction:
   1. Identify digital assets
   2. Document access details
   3. Choose a technical support person for whoever will administer the estate
   4. Communicate your wishes
   5. Store the information securely
   6. Review and update regularly
   7. Seek legal guidance from a professional qualified in your jurisdiction

#### Step 5 — Ask the context questions

**Ask one at a time. Explain briefly *why* each question matters** — users answer more completely when they understand the relevance.

- What legal documents have you already put in place (will, POA, advance directive, or their jurisdiction-appropriate equivalents)? When were they last reviewed?
- Do you use a password manager? Which one?
- How would you describe your technical comfort level?
- **What's driving you to plan now?** Common motivators — any of these resonate?
  - A death in the family or close circle
  - A health scare (yours or someone close)
  - A news story or someone else's disaster
  - A life event (new child, marriage, divorce, move)
  - **Professional credibility — you're a security professional, attorney, standards author, or advisor in this space, and not having your own plan is an embarrassment.** This is a distinct motivator worth naming. If the user is a professional in this field, the emotional hook throughout the skill should be: *"You advise others on this. Does your own plan exist?"*
- Do you have minor children? Do they have their own devices/accounts?
- **Do you have adult children?** If so: they may now be a resource in your plan (secondary executor, technical support person, contact) rather than just a dependent. Do they know they're in your plan? Have they been told what's in it? When minor children age into adulthood during the plan's lifetime, the plan should reflect the shift — but wills and POAs often don't.
- Are you more concerned about death or incapacity? (Both matter.)
- For couples: is your partner able to act independently on your behalf today if needed? What are the mechanics in your jurisdiction?

#### Step 6 — Note the legal foundation without interpreting it

- **Will (or jurisdiction equivalent):** Does one exist? Is it current? Does it meet the formality requirements you researched?
- **Power of Attorney / incapacity instrument:** Does one exist? Who is named? When was it executed?
- **Healthcare / advance directive:** Does one exist?
- **Digital asset provisions:** Older estate documents often predate explicit digital-asset fiduciary access laws in jurisdictions that have them. Ask the user to raise this with their attorney — don't characterize it as a gap yourself; whether it matters depends on the jurisdiction.
  - **Age heuristic (not a rule):** POAs and wills drafted before ~2018 rarely include digital asset provisions — this wasn't standard practice yet in most jurisdictions. If the user's documents are older than ~5 years, flag them proactively for attorney review. Don't interpret what's missing — just surface the age risk so the user doesn't have to know what they don't know.

**Output:** `00-orientation.md` — summary of the user's starting point, people map, legal status, and plan outline. Plus `00-jurisdictional-assumptions.md` from Step 3.

---

### Session 1: The Keys to Everything

**Goal:** Document the foundational accounts that unlock everything else.

These are the highest-priority assets because they're the recovery path for every other account: email, phone, password manager, and primary device access.

**Walk the user through documenting:**

| Field | Purpose |
|-------|---------|
| Account/service name | What it is |
| Website or app | Where to access it |
| Username | How to log in |
| Where credentials are stored | Password manager entry, written, memorized |
| Second-factor method | Authenticator app, SMS, hardware key, passkey |
| Backup codes location | Where recovery codes are stored |
| Recovery email/phone | Linked recovery methods |
| Legacy contact configured? | Platform-specific legacy settings |
| Instructions | What should happen to this account |

**Priority order:**
1. **Password manager** — this IS the master key. Document: which software, where is the master password / emergency kit, has the executor tested access?
2. **Primary email** — password resets flow here. Document: provider, 2FA method, recovery options.
3. **Phone / mobile number** — SMS codes for 2FA. Document: carrier, account credentials, transfer process. **If the phone plan lapses, the number can be recycled and SMS-based 2FA dies with it.**
4. **Primary device access** — phone PIN, computer password, biometric setup, disk encryption recovery keys.
5. **Cloud account** (iCloud, Google) — ties together devices, backups, photos, purchases.

**Security guidance:**
- Password manager emergency access is the single most important thing to document and store securely. If the executor has this, they can access almost everything else.
- Test the emergency access procedure. An untested backup is not a backup.
- Document where hardware security keys (YubiKeys, etc.) are physically located and which accounts they protect.
- Identify any accounts where a hardware key is the ONLY 2FA method with no backup codes — this is a single point of failure.

**Passkey warning:** Passkeys are becoming primary credentials for many services. If your passkeys are stored in a platform keychain (iCloud Keychain, Google Password Manager), understand the limitations:
- Apple Legacy Contact currently does NOT grant access to Keychain items including passkeys
- If an account uses passkey-only authentication with no password fallback, your executor may be permanently locked out
- Document which accounts use passkeys and whether a password fallback exists
- For critical accounts, maintain a password-based login option until platform legacy access catches up

**Employer/workplace accounts:**
- Work email, work laptop, employer-provided phone — these go back to the employer. Document what's on them that's personal (photos, personal files) and retrieve it NOW.
- Employer stock options, RSUs, ESPP — document vesting schedules and exercise windows. Some options expire 90 days after separation (including death).
- Employer life insurance, disability coverage, employer-sponsored retirement plan — document in Session 3.

**Incapacity scenario:**
- If incapacitated, your POA agent needs to pay bills, manage accounts, and maintain services. Can they access your email and phone TODAY without your help?
- Consider: 1Password Emergency Access or shared vault, authorized user on phone account, recovery contact on email.

**Password manager emergency access features — check explicitly:**

Many password managers offer a built-in emergency access or account-recovery feature that is separate from any printed emergency kit. Users often don't know it exists. Ask specifically:

- **1Password:** Settings → Emergency Access. Designate a trusted contact who can request access after a waiting period.
- **Bitwarden:** Emergency Access (premium feature).
- **LastPass, Dashlane, Keeper:** All offer equivalent features under various names.

If the password manager supports this, **configure it AND test it** before relying on it. This is a second recovery path, independent of the printed emergency kit. Document which recovery paths exist and who is configured for each.

**The "IN CASE OF EMERGENCY" shared vault:**

Beyond individual credentials, ask: *"Do you have a dedicated shared vault or document that consolidates emergency contacts — financial advisor, estate attorney, insurance agent, technical support person, secondary executor?"*

If not, prompt the user to create one (e.g., a shared 1Password vault titled "IN CASE OF EMERGENCY"). It should contain:

- Financial advisor — name, firm, phone, email
- Estate attorney — name, firm, phone, email
- Insurance agent — name, carrier, phone, all policy numbers
- Technical support person — name, phone, role, how they access the documentation
- Secondary executor — name, phone, role
- Critical account summary credentials (enough to get the executor started — not every login)
- Scanned PDFs of will, POA, healthcare directive, and insurance policy cover pages (see Session 7)
- Pointer to the full plan

**Access model:** The spouse/primary executor gets direct access as a family-vault member. Everyone else — secondary executor, technical support person, adult children — finds the vault via the break glass process (emergency kit → password manager → ICE vault). This reduces unnecessary credential exposure while keeping the vault reachable in a crisis.

**The vault should be self-contained.** Anyone who completes the break glass process should be able to act without needing anything else. **Build it before sharing it** — a half-populated emergency vault shared prematurely creates false confidence.

**Password manager hygiene — two audiences:**

A password manager only works as an estate planning tool if (a) it's used consistently so the vault is actually complete, and (b) the executor can navigate it cold. Both audiences need attention.

*For the account holder, ask:*
- Is the browser extension installed on all devices you use regularly?
- When you log into a new account, do you save it to the password manager?
- Do you use generated passwords, or do you reuse passwords across accounts?
- Is it set up on your spouse's / partner's devices too?
- Have you run the built-in security audit (1Password Watchtower, Bitwarden Reports) to check for reused, weak, or breached passwords?

If the answer to any is "no," briefly walk the user through fixing it. A vault with 50 entries and 200 missing credentials is not a complete estate planning record.

*For the executor / survivor:* assume they have never used 1Password (or equivalent) beyond browser autofill. The Break Glass Kit must include a short, plain-language "how to use the password manager" section covering:

- How to sign in on a new device
- How to search the vault
- How the browser extension autofills credentials
- How to handle a passkey entry
- How to view all vaults (family, shared, ICE)
- How to use a YubiKey if one is required
- What to do if they can't find something

Don't assume the executor is a power user.

**Has the other person tested it?**

Users often test emergency access themselves and feel confident. But they are not the one who will execute it — the executor / spouse is. The test that matters is whether **that person** can do it, alone, without help, using only what's stored in the emergency location. These are two different tests. Both need to pass before the plan is considered working.

**"Have you told them?"**

After the user names any person in a role — executor, technical support person, secondary executor, legacy contact, emergency vault viewer — immediately ask: *"Does [name] know they have this role?"* If no, it's an action item. The plan does not exist if the people in it don't know they're in it. Apply this rule consistently across every session.

**Output:** `01-keys-to-everything.md`

---

### Session 2: Financial Accounts & Autopay

**Goal:** Document all financial accounts, ensure beneficiaries are designated, and map the autopay chain.

**Walk the user through:**
- Bank accounts (checking, savings) — institution, account type
- Credit cards — issuer, primary cardholder
- Investment/brokerage accounts
- Retirement accounts (401k, IRA, Roth)
- Cryptocurrency wallets or exchanges — **special attention: without the private key or seed phrase, crypto is permanently lost**
- **Mobile money and peer-to-peer payment services** — in many regions this is the primary digital financial service, not a secondary one. Ask about whatever is dominant in the user's jurisdiction and any regions where they hold assets or have family. Examples by region (not exhaustive — research what's relevant):
  - Sub-Saharan Africa: M-Pesa, MTN Mobile Money, Vodafone Cash, AirtelTigo Money, Airtel Money, Wave, Orange Money
  - South Asia: Paytm, PhonePe, Google Pay India, bKash (Bangladesh), Nagad, JazzCash (Pakistan), easypaisa
  - Southeast Asia: GCash (Philippines), Maya, GrabPay, DANA, OVO (Indonesia), TrueMoney (Thailand), MoMo (Vietnam)
  - East Asia: WeChat Pay, Alipay, LINE Pay, Kakao Pay
  - Latin America: Mercado Pago, Nubank, Pix (Brazil), Yape (Peru), Nequi (Colombia)
  - Middle East & North Africa: STC Pay, Fawry, Benefit Pay
  - Europe: Revolut, Wise, Bunq, Bizum (Spain), Swish (Sweden), MobilePay (Denmark)
  - North America / Oceania: PayPal, Venmo, Zelle, Cash App, Interac e-Transfer (Canada), Beem It (Australia)
  
  Mobile money accounts are often tied to the SIM/phone number. If the number is deactivated, the account can become inaccessible — document both the account credentials and the SIM/carrier details. Succession processes vary significantly by provider and country; note the carrier's documented process where available.
- Tax preparation software/accounts
- **Financial tracking apps** (YNAB, Mint, Monarch, Copilot, spreadsheets) — if the user tracks finances in one place, document it here and note what it covers and what it doesn't. Confirm credentials are in the password manager.
- For each account: are credentials in the password manager? Are beneficiaries designated?

**Tax records — where they live:**

The executor often needs the last several years of tax returns and supporting documents to (a) file the decedent's final return, (b) calculate basis for inherited assets, (c) respond to any audit notice that arrives after death, and (d) value the estate. Document the location of:

- **Filed returns** — current year and at least the prior 3–7 years (retention recommendations vary by jurisdiction). For each year, where is the return stored? Examples: tax software cloud account, accountant's portal, paper folder in a filing cabinet, encrypted PDF in cloud storage, scanned in the password manager attachments.
- **Source documents for unfiled or current-year returns** — W-2s, 1099s, K-1s, brokerage 1099-B / 1099-DIV / 1099-INT, mortgage interest statements, charitable giving receipts, business expense records, HSA contributions, foreign income statements. Where are these collected through the year (e.g., a "tax 2026" folder in cloud storage, a physical inbox)?
- **Basis records for assets** — original purchase confirmations for stocks, real-estate closing documents, capital improvements to real property (which adjust basis on sale or inheritance), records of inherited property valuations. These are routinely lost; recovering them after the fact can be impossible.
- **Tax preparer or accountant** — name, firm, contact, what years they prepared, and whether they retain copies of past returns.
- **IRS / state tax authority online accounts** — confirm credentials are in the password manager. The executor may need these to retrieve transcripts or respond to notices.

**Outstanding loans and liabilities** — the executor needs to know these exist and have the information to act:
- Auto loans
- Personal loans or lines of credit
- Student loans
- Business loans
- Outstanding credit card balances

For each: document lender name and contact, account number, current balance, monthly payment, autopay source card, and whether credentials are in the password manager. How loans are handled at death varies by jurisdiction, loan type, and lender — the executor should consult an attorney. The goal here is making sure nothing is unknown or missing.

**Beneficiary warning:** Beneficiary designations on financial accounts may not align with your will. Verify every beneficiary is current and consistent with your wishes. Ask your attorney how beneficiary designations interact with your will in your jurisdiction.

**Crypto special handling:**
- Seed phrases and private keys must be stored securely AND accessibly
- Hardware wallet PINs must be documented
- Without the seed phrase, crypto is permanently and irrecoverably lost
- Exchange-held crypto (Coinbase, etc.) has account recovery processes but may require probate

**Autopay chain analysis — CRITICAL:**
Map every recurring payment to the card/account that pays it. Then answer: "If this card is cancelled (because the cardholder died), which bills stop being paid?"

| Payment Method | Bill | Frequency | Next Due | What Breaks If Cancelled |
|----------------|------|-----------|----------|------------------------|
| [Card/Account] | [Bill name] | Monthly / Quarterly / Semi-annual / Annual | [Approx. date] | [Consequences] |

**Always ask billing frequency — never assume monthly.** Insurance premiums are often quarterly, semi-annual, or annual. Many subscriptions are annual. This matters because the executor needs to know which bills are coming due soon vs. which have months of runway. An annual insurance premium just paid is low urgency; a monthly phone bill is always one month away from lapsing. The urgency of redirecting each charge changes dramatically with frequency.

This is where families get blindsided. The deceased's credit card gets cancelled, and suddenly the mortgage autopay bounces, the utilities shut off, and the kids' phone plan lapses.

**Family plan subscription continuity — flag explicitly:**

If any subscription is a shared family / team plan paid for by one member (password manager family plan, Apple One family, Google One family, streaming family plans, cellular family plan), document it carefully. **If that person dies and the subscription lapses, every family member loses access at once.** The password manager family plan is the most dangerous — losing it can lock the whole family out of every vault at the worst possible moment. Flag these as bills that MUST NOT lapse, and ensure the surviving spouse / executor knows to keep them paid even before closing the deceased's accounts.

**Incapacity scenario:**
- Joint accounts: the healthy spouse can still pay bills. No issue.
- Sole accounts: the POA agent needs access NOW. Can they log in?
- If incapacitated, bills still need to be paid. Map which accounts are joint vs. sole.

**Fraud prevention checklist for executor:**
- [ ] Notify credit reporting agencies of the death and freeze credit reports (process varies by jurisdiction)
- [ ] Contact banks and credit card issuers
- [ ] Notify relevant government benefit agencies (process varies by jurisdiction)
- [ ] Monitor for fraudulent activity on open accounts
- [ ] Do NOT close joint accounts immediately — bills may autopay from them

**Output:** `02-financial-accounts.md`

---

### Session 3: Insurance, Benefits & Property

**Goal:** Document insurance policies, employer benefits, and real property that survivors need to claim, maintain, or manage.

> [!important] Flag, don't advise
> Session 3 touches insurance, benefits, property, and titling — areas where it is easy to slip into legal, insurance, or financial advice. **Do not.** When you identify an issue — a title gap, a beneficiary inconsistency, a policy expiring, an unclear RSU scenario at death — name the issue, briefly explain *why it matters* for access or claims, and refer the user to the appropriate professional (attorney, insurance agent, financial advisor, plan administrator, HR). Do not explain how to resolve it. "Here are your options" is advice. "This is a gap; your attorney needs to advise on how to address it" is planning guidance.
>
> This rule applies to every session — but Session 3 is where it's most tempting to cross the line.
>
> **Tell the user *why* you are asking each question.** "I'm asking about your LTD policy because if you're incapacitated and can't work, your spouse needs to know it exists to file a claim — most people who have these policies forget to tell their spouse." The *why* creates engagement and produces more complete answers than a bare form.

**Walk the user through:**
- Life insurance — provider, policy number, beneficiary, agent contact
- **Health, dental, and vision insurance** — these are the most immediately relevant policies for incapacity, not death. A caregiver or POA agent needs this information on day one to authorize treatment and manage ongoing care.
  - For each: carrier name, plan name/type, member ID, group number, covered dependents
  - Where to find it: physical insurance cards (wallet, home), employer HR/benefits portal, carrier member portal, EOBs in email
  - Confirm credentials to the HR/benefits portal and each carrier's member portal are in the password manager
  - Add a summary (carrier, member ID, group number) to the emergency kit or ICE vault — this should be findable in minutes, not after a search
  - Note whether coverage is employer-provided or individually purchased; employer-provided coverage is contingent on employment status — the POA agent should know this and check with HR if employment status changes during incapacity
- Homeowner's/renter's insurance
- Auto insurance
- Disability insurance — **especially important for incapacity scenarios**
- Long-term care insurance — **many families don't know this exists until it's too late**
- Umbrella/liability insurance
- **Employer benefits** — life insurance through work, stock options, equity compensation, disability. Ask specifically about:
  - Pension or defined-benefit plan — is there one? Vesting status, plan administrator contact, survivor benefit options. Rules and portability vary by employer and jurisdiction.
  - Deferred compensation — any arrangement where earned pay has been set aside for future payment (sometimes called executive compensation, supplemental retirement, or similar). These don't always appear on a pay stub. Document the plan name, administrator, and account balance. What happens at death or separation is plan- and jurisdiction-specific — the executor should consult an attorney or the plan administrator.
  - Any other compensation that hasn't vested or been paid out yet

- **Social insurance and government benefits** — varies significantly by country and jurisdiction; ask explicitly rather than assuming. The jurisdiction plugin names the specific programs and procedures; the categories the inventory should capture are:
  - National retirement / disability program (where the jurisdiction has one): has the user created an account with the relevant agency? Do they know their projected benefit?
  - Disability benefits the user may qualify for during incapacity
  - Survivor benefits — what does a spouse or dependent receive from government programs at the user's death? The executor and surviving spouse need to know to file claims; most are not automatic
  - Veterans' benefits — if the user is a veteran, document the relevant agency's identifier(s), service-connected disability ratings, and survivor-benefit programs available in the jurisdiction
  - Any other government benefit the user currently receives or has a future claim to

- **"Is there anything else we haven't covered?"** — always ask this explicitly before closing Session 3. Prompt with examples: *"Any other insurance policies — pet, travel, event, collectibles, umbrella, identity theft? Any employer perks with financial value — legal plans, financial counseling, employee stock purchase programs outside of what we covered? Any income sources we haven't documented — rental income, royalties, side business, trust distributions, alimony or support payments?"* The goal is to surface anything that doesn't fit neatly into the categories above. Don't assume the list is complete without asking.
- **Real property** — ask explicitly about each type; don't assume the primary residence is the only property:
  - Primary residence — mortgage lender, deed status, property taxes, HOA (if applicable)
  - Second home or vacation property — mortgage, property taxes, insurance, HOA, property manager if rented out
  - Rental properties — property manager contact, tenants, leases, rental income accounts, insurance
  - Vacant land — location, tax parcel number, property taxes, any liens
  - Timeshares — contract terms, ongoing fees, managing company contact, account credentials
  - Family-owned or jointly-held property — property shared with siblings, parents, extended family, or other co-owners (e.g., inherited cabin, family farm, inherited land). Document all co-owners and how to reach them; the executor will need to coordinate with them. Note whether ownership is documented in a formal agreement.
  - Fractional ownership, co-ops, or other shared ownership structures — governing documents, co-owner contacts, management company
  For each property: document address, how title is held, all co-owners if any, mortgage or lien (if any), insurance carrier, how property taxes are paid, and any property managers or tenants who need to be notified. Consult your attorney on how each property transfers — title structure and co-ownership arrangements vary significantly.

  **Property documents — where they live.** The executor or surviving co-owner cannot transfer, sell, refinance, file an insurance claim, or maintain the property without the underlying documents. For each property, document the location of:

  - **Title and deed:** for owned property, where is the recorded deed copy or title abstract held? **If there is a mortgage, the user typically does not possess the original deed of trust or mortgage instrument** — the lender holds the security instrument and the recorded deed is on file with the county recorder. Note this explicitly; record the lender, the loan number, the recorder's office, and where any closing-package copy is kept.
  - **Title insurance policy** — usually issued at closing; useful if a future title dispute arises.
  - **Mortgage or HELOC documents** — note number, lender contact, where statements arrive (paper, lender portal, email).
  - **Property tax records** — where the bills arrive, where past payment receipts are filed, the assessor's parcel number.
  - **Survey, plat, and any easement documents** — often in the closing package; useful for any boundary or improvement decision.
  - **HOA or condo documents** — bylaws, CC&Rs, current assessments, board contacts.
  - **Home maintenance and improvement records** — service histories (HVAC, roof, plumbing, electrical, septic, well), warranty documents, receipts for capital improvements (which affect the cost basis at sale or inheritance), permit copies. These commonly live in a dedicated home folder, a box of receipts, a dedicated app, or a notes document.
  - **Appliance manuals and warranties** — paper folder, scanned to cloud, manufacturer accounts. The executor managing a vacant inherited property will need these.
  - **Keys and access codes** — for the home itself, garage, gates, outbuildings, mailbox. Note locations only; do not record codes in the inventory itself unless the inventory is in secure storage.

- **Vehicles, boats, RVs, motorcycles, trailers, and other titled property** — ask explicitly about each category; people commonly forget the boat or the camper. For each:

  - Year, make, model, VIN or HIN (Hull Identification Number for boats), and how title is held.
  - Loan or lien (lender name, account number, payoff status, lien-release document if paid off).
  - Insurance carrier, policy number, and what coverage applies (comprehensive, liability, on-water for boats, etc.).
  - Registration status and where the registration is renewed (state DMV, state Department of Natural Resources or equivalent for boats, US Coast Guard for documented vessels).
  - Connected accounts: telematics (Tesla, OnStar, FordPass, BMW ConnectedDrive, etc.), EV charging accounts, dashcam subscriptions, marine GPS / chartplotter subscriptions, RV park membership accounts, toll transponders.

  **Vehicle / boat / RV documents — where they live.** For each:

  - **Title and registration** — where the original is kept (commonly safe deposit box, fireproof safe, file cabinet). For paid-off vehicles, where is the lien-release letter? For boats, the title or US Coast Guard documentation paperwork lives separately from state registration.
  - **Owner's manual** — paper, glove box, manufacturer app, downloaded PDF. Useful to the executor managing or selling the asset.
  - **Service and maintenance records** — dealer service history, independent shop invoices, oil-change logs, marine service records (engine hours, winterization, hull surveys), RV chassis and house-side service records. May live in glove box, paper folder, manufacturer app, third-party service-tracker app, or a notes document. **For boats and RVs especially, well-kept service records materially affect resale value** — flag this so the executor knows to preserve them rather than discarding "old paperwork."
  - **Marine-specific:** hull survey reports (recent surveys substantiate insurance and resale value), USCG documentation papers if a documented vessel, slip / mooring agreement, marina contacts.
  - **RV-specific:** chassis manual (often a different manufacturer than the house-side), house-side appliance manuals, dealer paperwork, any extended warranty contract, campground membership accounts (Thousand Trails, KOA Rewards, Good Sam, Harvest Hosts, etc.).
  - **Spare keys and access:** physical keys, key fobs, smart-key apps, garage-door remotes — note where they live.

**Incapacity scenario:**
- Disability insurance and long-term care insurance are the critical policies for incapacity, not death
- Health insurance must continue — understand continuation options available in your jurisdiction
- Property taxes and mortgage payments must continue — flag these for the POA agent

**Output:** `03-insurance-benefits-property.md`

---

### Session 4: Digital Property & Professional Accounts

**Goal:** Document digital assets with monetary, professional, or community value.

**Walk the user through:**
- Domain names — registrar, expiration dates, auto-renew status, DNS provider
- Websites and blogs — hosting provider, CMS credentials
- Code repositories — GitHub, GitLab, Bitbucket. Any repos others depend on?
- Cloud services — AWS, GCP, Azure accounts (**these accumulate charges if not closed**)
- Digital storefronts — Etsy, Shopify, app store developer accounts
- Intellectual property — published works, patents, trademarks
- Professional accounts — LinkedIn, professional certifications, memberships
- Professional licenses that expire or require renewal
- Accounts managed on behalf of organizations (HOA, volunteer orgs, clubs, religious institutions)

**For each:** document the account AND the handling instruction (transfer, close, memorialize, delete).

**The personas concept matters here:** A personal GitHub account might be closed, but a repo that an open source community depends on needs a succession plan. An HOA Google Drive needs to be transferred to the next board member. Ask the user to think about which accounts they manage on behalf of others — those accounts need a handoff plan, not just a closure plan.

**Organizational roles — structured prompt:**

Many users hold admin or owner roles for organizations that aren't captured by "do you have a personal GitHub account?" These roles have infrastructure, successor questions, and in-progress work that must not die with the individual. Walk the user through each of the following:

- **What organizations do you hold admin, owner, or co-lead roles for?** (Standards bodies, working groups, conferences, professional societies, user groups, open source projects, HOAs, religious communities, volunteer orgs, boards.)
- **For each organization, what accounts or infrastructure is tied to your personal identity vs. the org?** (Personal email subscribed to a mailing list vs. an @org.example address; personal GitHub vs. org membership; personal calendar invites hosting org meetings.)
- **Who is the named successor for each role?** Document name, contact info, and what they'd take over. "Nobody yet" is a valid answer — capture it as a gap.
- **Have you told that person they are your successor?**
- **What happens to in-progress work** — specifications in draft, documents mid-review, repos with pending PRs, events in planning, contracts under negotiation? Who picks it up?
- **Are there any org-owned secrets, signing keys, or access tokens** that would be lost with you? (GitHub org secrets bound to a user, admin API keys, notary/signing keys for releases.)

**Mailing list admin is an underappreciated category.** Many community lists are administered by one or two people via their personal accounts. If those people vanish, the list can become unmoderated or inaccessible. Document each list the user admins: platform, list name, how to transfer admin rights, who the backup admin is.

**Business accounts:** If the user owns a business, the business's digital assets may be governed by the operating agreement, partnership agreement, or corporate bylaws — not the user's personal will. Document them here but flag the governance distinction. Client data may be subject to NDAs and confidentiality obligations that survive the owner's death.

**Output:** `04-digital-property.md`

---

### Session 5: Media & Memories

**Goal:** Identify and protect irreplaceable personal data.

**Walk the user through:**
- Cloud photo libraries (iCloud Photos, Google Photos, Amazon Photos)
- Local photo/video archives — where are they? External drives, NAS, SD cards?
- Social media content — posts, photos, messages with sentimental value
- Documents — cloud storage (Dropbox, OneDrive, Google Drive), local files
- Creative works — writing, art, music, video projects
- Backup status — are these backed up? Where? Is the backup encrypted? Where is the key?

**Key question:** For each category, what should happen?
- Preserve for family
- Transfer to specific person
- Delete
- Memorialize (leave online as-is)

**Security guidance:**
- If backups are encrypted, the encryption key is as important as the backup itself. Document both.
- Cloud services may delete data after extended inactivity. Configure legacy/inactive account settings.
- Local-only data with no backup is at highest risk. Identify it.
- **Download a backup NOW of irreplaceable cloud-only data** (photos, documents). Don't wait for death to discover that Legacy Contact access is limited or slow.

**Output:** `05-media-memories.md`

---

### Session 6: Devices, Infrastructure & Children's Digital Lives

**Goal:** Document physical devices, home technology, and — for parents — children's digital accounts.

**Walk the user through each of the following explicitly — don't rely on the user to volunteer categories they own:**

- Computers — make/model, encryption status (FileVault, BitLocker), login credentials location
- Phones and tablets — PIN, biometric setup
- Smart home devices — hubs, cameras, locks, thermostats, account access. **If smart locks are the primary entry method, document physical key backup locations.**
- Smart home controllers — sprinkler systems (Rachio, Hunter Hydrawise), HVAC/thermostats (Nest, Ecobee), smart fans, attic vents, whole-house humidifiers
- Security cameras and doorbells — manufacturer apps, cloud storage subscriptions, recording retention
- E-readers — Kindle, Kobo, Nook. Content licenses are account-tied; consult the platform's terms for what transfers
- Gaming consoles — accounts with purchased content. **Any consoles managed on behalf of a minor child?** Parental controls, purchases, and friend lists are usually tied to the parent's account — document the handoff to the other parent or guardian.
- Network equipment — router, WiFi, ISP account details, any non-obvious physical infrastructure (powerline ethernet to outbuildings, pulled-through-walls runs, switch placements the next person won't find)
- Home servers / NAS — what they do, how to access them, how to shut them down safely
- Backup devices — external drives, NAS, backup media
- **Any other networked devices not already covered?** (3D printers, pool controllers, solar inverters, EV chargers, electric bikes with connected apps.)

For each: who has access today, are credentials in the password manager, and what should happen to it (keep running, shut down, transfer)?

**Children's digital lives:** if the user has minor children, the `has-minor-children` facet activates and walks them through the full inventory of children's devices, accounts, parental-control configurations, school-portal access, and the parental-control-handoff path that lets a guardian or surviving co-parent authenticate as the parent. See `plugins/facet/has-minor-children.md` for the substantive prompts. The cross-cutting note here: a guardian or surviving co-parent's day-one tasks cannot wait for probate; the household needs documented credentials and authentication paths now.

**For non-technical executors:** Include a "what this is and why it matters" explanation for each device category. Not everyone knows what a NAS is or why the router matters.

**Two-audience approach:** If the user's executor is non-technical, suggest they also designate a **technical support person** who can handle device access, account recovery, and infrastructure shutdown. The executor handles legal authority; the tech person handles execution.

**How does the technical support person access the documentation?**

After the technical support person is identified, ask explicitly: *"How does [name] actually get to the documentation they'd need? Is it in a private GitHub repo they'd have to be added to? A file on a machine they can't boot? A password-protected folder? Have you shared it with them, or just told them where it is?"*

A runbook in an inaccessible location is not a plan. Options include:
- Adding the person as a collaborator on the private repo now
- Providing a printed copy with a cover sheet explaining their role and how to get the latest version
- Sharing the location and credentials via the IN CASE OF EMERGENCY 1Password vault
- A combination — printed copy for day one, repo access for ongoing updates

Document which option was chosen, when it was shared, and whether the person has confirmed they can actually retrieve the documentation. Flag any inaccessible runbook as an open gap.

**Connected vehicles — do not skip this:**

Modern vehicles have manufacturer apps (Hyundai Bluelink, Tesla app, Ford Pass, GM myChevrolet/myGMC, BMW ConnectedDrive, Toyota Connected, Rivian, etc.) with digital keys, remote access, and account-based ownership. Ask explicitly — do not rely on the user to volunteer this:

- Do you have any vehicles with a manufacturer app or digital key system?
- Who holds the primary account / master digital key? Digital keys are often hierarchical — one primary account holder grants keys to others. If the primary account is closed, descendant keys may lose validity.
- Does your spouse / partner have independent access to the vehicle today, not just through your account?
- **Do you know how digital key ownership transfers at death or incapacity?** For most manufacturers, this process is undocumented or unclear. Flag it as a research task: the user should contact the manufacturer to understand the transfer path before it's needed.
- Physical vehicle titling (registration, lien, ownership) is a separate issue — if not jointly titled, flag for the attorney. Covered in Session 3.

**Home infrastructure / homelab (if applicable):**

Power users often run significant home infrastructure beyond consumer hardware — NAS, Docker containers, self-hosted services, local DNS, VPN servers, cloud backup accounts, monitoring stacks. A non-technical executor cannot manage any of this without documentation. Ask:

- What services are running? (A short list — NAS, DNS, reverse proxy, VPN, monitoring, etc.)
- What breaks if they stop, vs. what can safely go offline? Some services (local DNS, NAS file access) are load-bearing for the household; others (observability, auto-update schedulers) can go dark without anyone noticing.
- **Are there any order-of-operations requirements?** (Example: shutting down local DNS without reconfiguring the router first will take the whole home offline. Document these dependencies.)
- What needs a graceful shutdown vs. can be hard-powered off?
- Who is the technical support person for this infrastructure? (The executor is often not technical enough. This may be a different person from the legal/financial executor.)
- Is there existing documentation — a homelab repo, runbooks, architecture docs? Where does it live? How does the technical support person get to it? (See previous subsection.)
- Where are credentials for the infrastructure — NAS admin, router admin, cloud backup accounts, secret-management keys (age, SOPS, Vault)?
- **For any secret-management system:** the master key (age private key, Vault unseal keys, SOPS GPG key) must be stored somewhere the technical support person can retrieve. Without it, the encrypted secrets are useless.

**Incapacity scenario:**
- Smart home, ISP, and network must continue functioning — don't assume someone will "shut it all down"
- Home security systems (cameras, alarms) need to keep running
- ISP billing must continue or the household loses internet

**Physical asset registries and gear registration:**

Many people register valuable physical gear with online services for theft recovery, warranty, or proof of ownership. These are digital accounts tied to physical property — and the executor needs to know they exist.

Ask the user: *"Do you register any gear or equipment with online services? Think bikes, cameras, audio equipment, firearms, instruments, collectibles, or anything else you've formally registered anywhere."*

Common registry types:

| Category | Example Services | Why It Matters for the Estate |
|----------|-----------------|-------------------------------|
| Bicycles | Bike Index (bikeindex.org), Project 529, National Bike Registry | Bikes sold from the estate must be deregistered first — otherwise the new owner can't register them and may have trouble if a registry check flags them |
| Cameras & photo gear | Manufacturer serial number databases, CheckMEND, Lenstag | Same issue — deregister before transfer or sale |
| Firearms | State and federal registries (varies by jurisdiction) | Legal transfer requirements vary significantly; executor needs to know what exists |
| Musical instruments | Various; some instruments have provenance records | High-value instruments may have documented ownership history |
| Audio/video equipment | Some manufacturers maintain serial number registries | Mostly warranty-related; less critical for estate but worth documenting |
| Jewelry & watches | Some insurers maintain scheduled item registries; GIA for certified diamonds | Relevant to insurance claims and estate appraisal |
| Collectibles & art | Various registries by category | Provenance matters for valuation and sale |
| Appliances & electronics | Manufacturer warranty registrations | Lower stakes, but may have subscription services attached |

**The critical estate action for any registration:** When gear is sold, donated, gifted, or transferred as part of the estate, **deregister it before transfer**. A bike sold at an estate sale that still shows as registered to the deceased can't be re-registered by the buyer — and may come back flagged as stolen if the registration lapses and someone reports it. The executor should close or transfer registrations, not abandon them.

**For each registered item, document:**
- Service name and URL
- Account credentials (in password manager)
- Items registered (make, model, serial number)
- What to do at death: transfer, deregister, or close

**Output:** `06-devices-infrastructure.md`

---

### Session 7: Legacy Contacts & Memorialization

**Goal:** Configure platform-specific legacy settings NOW, not later.

**Walk the user through configuring (where available):**

| Platform | Feature | What It Does | Limitations |
|----------|---------|-------------|-------------|
| Apple | Legacy Contact | Grants access to iCloud data after death | Does NOT include Keychain, passkeys, licensed media, or payment info |
| Google | Inactive Account Manager | Auto-notifies contacts after inactivity period, can share data or delete account | Inactivity timeout must be configured; default is never |
| Facebook | Legacy Contact / Memorialization | Manages memorialized profile or requests deletion | Legacy contact cannot log in as the person |
| GitHub | Successor | Manages repositories after death | Only personal repos, not org repos |
| Instagram | Memorialization | Converts to memorial account on request | Must contact Instagram with proof of death |
| LinkedIn | Memorialization | Removes from public-facing features | Cannot download data after memorialization |
| Microsoft | Next of Kin process | Can request data or account closure | Requires death certificate and proof of relationship |
| Yahoo! | Account management | Can request data or account closure | Requires legal documentation |

**For each platform the user uses:**
1. Does the platform offer a legacy/memorialization feature?
2. Have you configured it? If not, walk through it now.
3. Document what you configured and when.
4. **Understand the limitations.** Legacy access is never full access. Know what your executor WON'T get.

**Important:** This list is not exhaustive. Check each service you use for legacy options.

**Impersonation vs. on-behalf-of delegation:** There are two fundamentally different models for executor account access:
- **Credential sharing (impersonation):** Giving the executor your password so they can log in as you. Easy to set up, but most platform Terms of Service prohibit posthumous use of someone's credentials. Creates accountability problems — the executor is pretending to be you.
- **Legacy contact features (on-behalf-of):** Platforms like Apple, Google, and Facebook offer formal features where the executor is identified as acting *for* you, not *as* you. They get limited but auditable access. This is the preferred model where available.

Use legacy contact features wherever platforms offer them. Document password access as a fallback, but understand the difference. The industry has not yet converged on interoperable delegation standards — this gap is identified as a core problem in the research foundation for this skill.

**Passkey impact:** If you use passkey-only authentication on any account, and those passkeys are in a keychain that legacy contacts can't access, document this as a known gap. Maintain password fallback on critical accounts.

**Scan your legal documents into the ICE vault.**

Ask explicitly: *"Have you scanned your will, POA, healthcare directive, and insurance policy cover pages and stored PDFs in your password manager's IN CASE OF EMERGENCY vault?"* If not, flag it as an action item.

**Why this matters:** In a real emergency, the executor may be remote, panicked, unable to travel to the fireproof safe, or simply not know where the physical originals live. A scanned copy in the password manager is immediately accessible from any device, anywhere.

**Important framing:** The scanned copies are for *immediate reference* — the executor and attorney can see what they're working with within minutes. **Physical originals are still required for legal proceedings** and should remain in their physical locations (fireproof safe, attorney's office, safe deposit box). Digital is an additional access point, not a replacement. Both coexist.

Walk the user through which originals exist and where they live. If the user does not know where all the originals are (common — often one spouse manages these), that's a separate action item: locate the originals together with the partner, then scan them.

**Commercial digital estate tools** (illustrative list, not endorsed; any of these may have changed status, ownership, or feature set since the last review of this skill — verify current state and read the user agreements before relying on any of them):
- Bequest.com
- Consent Matrix
- Digital Memory Box
- Eternal.me
- FinalDocx
- HERmemories
- Hereafter.ai
- I Live On
- The Nokbox

**Output:** `07-legacy-memorialization.md`

---

### Session 8: Communication & Personal Wishes

**Goal:** Document messaging accounts and personal wishes.

**Walk the user through:**
- Messaging apps — iMessage, Signal, WhatsApp, Telegram, Slack, Discord
- Which contain important conversations to preserve?
- Video calling accounts
- Social media wishes — memorialize, delete, archive, or transfer?
- Specific content to preserve or remove?
- Dating apps or private accounts — what should be deleted immediately? **Note:** "Delete this account" is a WISH, not a guaranteed action. Many services require proof of death for third-party deletion, and some don't allow it at all. For accounts the user wants deleted: pre-configure deletion where possible (Google IAM, Facebook), document the wish for others, and accept that the executor may not be able to fulfill every deletion request without legal process.
- Funeral/memorial preferences
- Charitable giving intentions
- Any digital memorial preferences
- Letter of intent or personal message to loved ones

**Posthumous AI and digital likeness:** AI services can now generate realistic audio, video, and text in someone's voice and likeness, often from very little source material. Ask the user:
- Do you want to document your wishes about AI recreations of your voice, likeness, or persona?
- Are you open to family using AI tools to preserve your stories or create memorial content?
- Do you explicitly NOT want your likeness recreated without consent?

Document these wishes here. Legal protections vary widely by jurisdiction and are still evolving. A documented wish won't guarantee compliance, but it gives your executor standing to object and makes your intent clear to family. For public figures or anyone with significant digital presence, this is increasingly material.

**Note:** These wishes should also be documented in the user's will or a separate letter of intent reviewed by their attorney.

**Output:** `08-communication-wishes.md`

---

### Session 9: Subscriptions & Recurring Payments

**Goal:** Create a list of everything that charges money so the executor can cancel them.

**Walk the user through:**
- Streaming services (video, music, audiobooks)
- Software subscriptions
- Cloud services with recurring charges
- News/media subscriptions
- App Store / Play Store subscriptions
- Membership and loyalty programs
- Recurring donations
- For each: which payment method is charged? (This helps the executor find them via credit card statements.)

**Tip:** Search email for "receipt," "subscription," "renewal," and "payment" to find accounts you've forgotten. Also check App Store/Play Store subscription settings — many people forget about in-app subscriptions.

**Cross-reference with Session 2:** The autopay chain analysis shows which subscriptions die when a payment method is cancelled. Flag any that the surviving family needs to keep (internet, phone, security monitoring, insurance autopay) and ensure those are on a payment method that will survive.

**Family plan continuity — flag again here:** Any subscription that's a shared family plan (password manager, Apple One, Google One, streaming family plans, cellular family plan) is higher-stakes than a single-user subscription. Its lapse affects multiple people at once. Session 2 covers this in the autopay context; here, ensure each family plan is documented with the organizer's identity, what each family member loses if it lapses, and explicit instructions for the executor to keep it paid until the surviving family member can take it over.

**Incapacity scenario:**
- ALL subscriptions must continue. The POA agent needs to maintain services, not cancel them.
- Flag which subscriptions are essential (utilities, insurance, internet, phone, security) vs. discretionary.

**Output:** `09-subscriptions.md`

---

### Session 10: Secure Storage & Sharing

**Goal:** Decide how to store the plan securely and communicate it to the right people.

**Walk the user through storage options:**
- Written instructions stored securely (e.g. in a personal safe that is accessible to your executor if needed). Consider including the instructions as part of your will or power of attorney.
- Password manager software emergency access instructions stored securely
- Pre-sharing access to your password manager software with trusted individuals
- QR codes or NFC tags stored with your wallet, purse, or personal effects can be used to share a URL where your personal wishes, powers of attorney, or contact information for your attorney may be shared.
- Consider the use of online estate management services, which offer professional services to act as the Digital Estate Manager for your loved ones or Executor.

**Security best practices:**
- Use a password manager for centralized, secure storage. Store the master password/emergency kit where the executor can access it.
- Do NOT email files containing passwords
- If no password manager: write passwords in a notebook, store securely with estate documents. This is a valid approach — don't shame people who prefer paper.
- Periodically TEST whether the executor can access the password manager with the stored instructions
- Enable built-in legacy contact features on all platforms that support them

**Communication:**
- Talk to your executor and loved ones about what you've prepared
- Ensure you've provided proper legal authorization for account management
- Choose a time when everyone can listen, explain wishes clearly
- Document who knows what and who has access to what
- **If you have a secondary executor (in case the primary is unavailable or also incapacitated), they need to know the plan exists too**
- **If you have a technical support person AND an executor, they need to know each other and have exchanged contact info**

**Document storage map — consolidate "where things live":**

Earlier sessions captured *what* documents exist (tax records, property documents, vehicle/boat/RV titles and manuals, legal instruments, insurance policies, beneficiary forms, equipment warranties, medical records). Session 10 consolidates *where* they live, in one place the executor can scan.

Build a small table — one row per category, one row per location — that an executor can use as a treasure map. Example shape (the user's actual entries will differ):

| Category | Physical location | Digital location |
|---|---|---|
| Original will, POAs, healthcare directive | Attorney's vault — [firm name, contact] | Scanned copy in password manager attachments |
| Vehicle / boat / RV titles, registrations, lien releases | Safe deposit box at [bank, branch, box #] | — |
| Real property deed copy, title insurance, closing package | Fireproof safe at home, top drawer | Scanned copies in cloud folder `Estate / Property` |
| Home maintenance records, appliance manuals, warranties | Filing cabinet, top drawer marked "House" | Manufacturer apps; some scanned in cloud |
| Vehicle / boat / RV service records, manuals | Glove box / boat helm / RV cabinet, plus dealer service history | Manufacturer apps; service-tracker app [name] |
| Tax returns and source documents | Accountant's portal — [firm, contact] | Encrypted PDFs in cloud folder `Tax / [year]` |
| Insurance policies (life, health, home, auto, marine, umbrella) | — | Each carrier's member portal; PDFs in `Insurance` cloud folder |
| Beneficiary designation forms | Plan administrator records (each plan) | Confirmation copies in `Beneficiaries` folder |
| Birth, marriage, divorce, naturalization certificates | Fireproof safe at home | Scanned in password manager attachments |
| Spare keys, garage codes, alarm codes | Key safe at [location] | Codes documented per Session 6, not in this map |

**Two rules for the map itself:**

1. **The map records locations, not contents.** "Original will at attorney's vault" — yes. The text of the will, no. The map is a finding aid; full documents live where they live.
2. **Keys and access codes do not go in the map directly.** Locations like "key safe by the back door" can be in the map; the safe combination, the alarm code, and similar access secrets follow the secure-storage rules above (password manager attachments, ICE vault, or a sealed envelope in the same safe as the originals).

If documents are scanned into a cloud folder or a password-manager vault, this is also where you confirm that the executor (or the POA agent for incapacity scenarios) actually has the access path documented in the emergency kit.

**Output:** `10-secure-storage.md`

---

### Session 11: Review & Maintenance

**Goal:** Set up a maintenance schedule so the plan doesn't go stale.

**Walk the user through:**
- Set annual calendar reminder to review the plan
- Review triggers: marriage, divorce, new child, move, job change, major account changes, new device, health changes, major financial changes
- Annual test: can the executor still access the password manager with stored instructions?
- Annual test: can the technical support person follow the plan?
- Update when passwords, services, or life circumstances change

**Produce a review checklist** the user can use each year.

**Plan Test Drill:**
At least once (ideally annually), the user should run a structured test WITH their executor and/or technical support person. **The test that matters is whether they can do it, not whether you can.** The author of the plan has context and muscle memory the executor does not. An executor who has never opened the emergency kit on their own has not been tested.

1. **Access test:** Can the executor access the password manager / credential store **from zero, alone, without your help**, using only what's been provided to them? (Emergency kit, notebook copy, ICE vault, printed instructions.)
2. **Document test:** Can the executor locate the Break Glass Kit, First 48 Hours checklist, and Executor Quick Reference without being told where they are?
3. **Bill test:** Can the executor identify which bills need to be paid this month and how to pay them?
4. **Contact test:** Does the technical support person have working contact info for the executor, and vice versa? Have they met?
5. **Legacy contact test:** Verify all platform legacy settings are still configured (Apple, Google, Facebook, GitHub). Settings can be silently disabled by account changes.
6. **Jargon test:** Read the Break Glass Kit aloud to the executor. Anywhere they stop and ask "what does that mean?" is a defect. Fix it.

If the executor and technical support person are the SAME person, that's fine — but ensure a secondary person exists who knows the plan in case the primary is also unavailable.

**Recommend scheduled backups:** For irreplaceable data (photos, documents), set a recurring calendar reminder (quarterly) to download a local backup. Don't rely solely on cloud services and legacy contact access.

**Output:** `11-review-maintenance.md`

**Final reminder:** Outdated instructions cause as many problems as no plan at all. A plan is a living document.

---

### Session 12: Assemble the Outputs

**Goal:** Produce the Break Glass Kit and the supporting reference documents. Keep the Break Glass Kit short and separate — it is the most important artifact this skill produces.

Take all session outputs and assemble the following documents. Each has a distinct purpose and audience — do not merge them.

**1. Break Glass Kit** (`break-glass-kit.md`)

This is the single most important output. It is written for the person who has just been handed the worst day of their life and has to start acting. Keep it short — 5-10 pages maximum. If it's longer, it's failed.

**Audience:** The immediate decision-maker (spouse, partner, adult child, named executor). Assume they are tired, stressed, not technical, and will read this once.

**Structure:**
- **Step 1: Get into the password manager (or equivalent credential store).** Step-by-step, starting from "go to the safe deposit box" or "get the emergency kit from X."
- **Step 2: What not to let lapse this week.** The 3-6 bills that, if missed, cause cascading problems (phone plan, credential store subscription, primary cloud, insurance, essential utilities).
- **Step 3: Who to call first.** 5-8 named people with phone numbers and a one-line reason to call each. This should be printable on a laminated card.
- **Step 4: Critical account summary.** The 5-10 accounts that matter in week one — email, phone carrier, primary bank, primary credit card, cloud, health insurance.
- **Step 5: Legal documents — where to find copies.** Not the originals (those are in a safe). The scanned copies. Plus a note that the originals exist and where.
- **Step 6: What can wait.** A single page telling them what NOT to worry about in week one.
- **What the reader can do right now without any of this** — a reassuring inventory of access they already have.

**Tone:** Direct, calm, free of jargon. Every instruction should be doable by someone who has never logged into a password manager. Where a step assumes technical knowledge, include "call [named technical person]" as the fallback.

**Distinction from the rest of the outputs:** The Break Glass Kit is a *curated subset* of the full inventory. It contains only the information needed in the first week. For anything beyond that, it points to the Comprehensive Inventory.

**The "average executor" quality bar — run this checklist before the Break Glass Kit is considered complete:**

The executor is not the author. They may be a grieving spouse, a sibling, an adult child, or a close friend. Assume average technical skills, high stress, and one cold read. A kit that works for the author almost always fails for the executor on first contact. Check all of:

- [ ] **No circular logic in Step 1.** "Get into 1Password to find your phone PIN — but you need the phone to get into 1Password" is a dead end. Order the steps so each one can be executed with only what the previous step provides. Example: get into 1Password on any device first, then use it to find the phone PIN.
- [ ] **Phone numbers are on paper.** Every critical first-call number — spouse, named executor, attorney, financial advisor, technical support person, insurance agent — must appear on the printed Break Glass Kit or a laminated card. Saying "call these people" without numbers, when the executor hasn't yet signed into any vault, is useless.
- [ ] **No jargon.** Scan for and replace anything the executor won't recognize cold: OTP, 2FA, FileVault, BitLocker, FIDO, passkey, recovery phrase, seed, NAS, homelab, Docker, reverse proxy, DNS, VPN, GitHub repo, private key, YubiKey. Use plain language ("a six-digit code sent by text message," "the disk password for the computer," "the hardware key that plugs into the USB port"). If a technical term must appear, define it inline the first time.
- [ ] **No planning meta-notes.** Strip anything that reads like "this is an open action item," "TODO," "[confirm]," "[add]," or commentary intended for the plan author. Those notes belong in the planning documents, not the crisis document. The kit should only be shared once it's complete — not while it's still under construction.
- [ ] **Consistent audience.** If the kit is written "for Stephanie, Marci, or whoever," don't then switch to third-person references to Stephanie later. Write for the reader, whoever they are. "You" and "the person this was written for" beats named references.
- [ ] **Last-verified date is visible.** The executor needs to know if the information is current. Put the date near the top.
- [ ] **No obscure app references.** "Dean's Obsidian vault" means nothing to Marci. Describe in plain language: "Dean's notes on his computer in the app called Obsidian — the blue-and-purple icon."
- [ ] **Every step is doable by someone who has never used your tools before.** When in doubt, write the step at the level of "open this app, look for this word, click it." Err toward too explicit.

If any box is unchecked, the kit is not ready to share. Run the jargon test (read it aloud to the intended reader) before declaring it done.

---

**2. Executor / Administrator Quick Reference** (`administrator-quick-reference.md`)

Use the jurisdiction-appropriate term ("executor," "administrator," "customary successor," "Testamentsvollstrecker," etc.) based on the Jurisdictional Assumptions document. This is the reference the person administering the estate will use over weeks and months.
A single document with:
- Who to contact first (attorney, financial advisor, technical support person)
- The First 48 Hours checklist (time-sensitive actions)
- Where to find the master key (password manager / notebook / emergency kit)
- Financial accounts summary with beneficiary status
- Insurance policies to claim
- Subscriptions to cancel vs. keep
- Legacy contacts that will activate automatically
- Property and vehicle summary
- Fraud prevention steps

**2. First 48 Hours Checklist** (`first-48-hours.md`)
Time-sensitive actions in priority order:

| Timeframe | Action | Why |
|-----------|--------|-----|
| Immediately | Secure phone — keep charged, don't let it lock | SMS codes for 2FA; phone number recycling risk |
| Immediately | Secure all devices | Prevent data loss or unauthorized access |
| Hours | Access password manager / credential store | Foundation for everything else |
| Day 1 | Transfer/maintain phone billing | Prevent number recycling, maintain SMS 2FA |
| Day 1 | Notify employer (if applicable) | Benefits, life insurance, final paycheck |
| Days 1-3 | Notify credit reporting agencies, freeze credit | Fraudsters target obituaries |
| Days 1-3 | Contact banks and financial institutions | Prevent unauthorized access; some joint accounts may be frozen |
| Week 1 | Contact insurance companies (life, health) | Initiate claims; health continuation for dependents |
| Week 1 | Contact government benefit agencies | Death benefit, survivor benefits (varies by jurisdiction) |
| Week 1 | Review autopay chain — redirect critical payments | Prevent mortgage bounce, utility shutoff |
| Month 1 | Download cloud data (photos, documents) before closing accounts | Data may be permanently lost |
| Month 1-3 | Address social media, subscriptions, loyalty programs | Lower priority — stabilize first |

**3. Attorney Brief** (`attorney-brief.md`)

A one-pager the user brings to an estate-planning consultation. **It is informational, not advisory.** The brief tells the attorney *what exists* and *what is unusual about this estate* so the attorney can ask informed questions and identify issues. **It does not propose legal rationale, recommend specific clauses, instruct the attorney on jurisdictional law, suggest which instrument to use, or otherwise tell the attorney how to do their job.** That is the attorney's role; this brief is the client's preparation.

**The brief is a summary. No original documents accompany it.** Originals (will, deeds, vehicle titles, insurance policies, beneficiary forms) stay where they live (safe, safe deposit box, attorney's vault, county recorder, plan administrator, lender). The brief notes that they exist and where they are located; the attorney decides which they need to see and arranges for that separately. Do not generate a "documents to bring" list as part of the brief.

**Content — describe, do not prescribe:**

- **What digital assets exist**, by category, with approximate value bands where the user is comfortable noting them. Highlight categories that often surprise general-practice attorneys: cryptocurrency (custodied vs. self-custodied), business or revenue-generating digital property, online platform accounts with significant historical or sentimental value, professional or fiduciary roles held online, intellectual property held in digital form.
- **What estate documents currently exist**, with their dates of execution and the location of the original. Note any documents the user believes are missing (e.g., "no current financial POA," "no healthcare directive on file") — without proposing what should replace them.
- **Beneficiary designations on file**, by account type, with the date last reviewed where known. Flag designations the user identifies as potentially stale (named ex-spouse, named deceased person, named minor without a trust mechanism, name change since execution) — without proposing the fix.
- **Family and household composition** relevant to planning: marital, partnership, or separation status; minor children or dependents; blended-family considerations; anyone the user supports financially; anyone with disabilities the user is concerned about.
- **Domicile and any cross-jurisdiction exposure**: state or country of domicile, out-of-state or out-of-country real property, recent moves, non-citizen status of the user or spouse, dual residency.
- **Platform-level facts** the attorney may not know: which platforms the user has set legacy contacts on, which key platforms do not offer one, that custodians of electronic communications are subject to limits on disclosure independent of the will. Phrase as facts about the platforms, not as legal conclusions.
- **Open questions the user wants to raise at the meeting**, in the user's own voice ("I want to ask about…"). The attorney answers; the brief does not.

**What the brief explicitly does not contain:**

- Specific clause language, draft will or trust provisions, or POA wording.
- Statements about what the law requires, permits, or prohibits in the user's jurisdiction.
- Recommendations on which legal instrument (will vs. trust, type of trust, specific POA form, type of healthcare directive) to use.
- Tax planning advice, estate-tax projections, or recommendations on portability elections, gifting strategies, or trust structures.
- Citations to statutes or case law presented as the basis for action. References that appear in jurisdiction plugins are background reading for the *user*, not authority cited *to the attorney*; if included at all, label them clearly as the user's own reading.
- Any instruction or directive to the attorney ("the will should…", "the POA must include…", "the attorney should…").
- Any list framed as "documents to bring to the meeting." Originals stay where they live.

If the brief reads like a legal memo or a client telling the attorney how to draft, it has overstepped. Rewrite it as a fact sheet.

**4. Action Items for the Planner** (`action-items.md`)

This document is for the person who just completed the sessions — NOT for the executor. It answers the question: "What do I actually need to go DO now that I've documented everything?"

**How to build it:**
- Collect all `- [ ]` items from every session document
- Deduplicate — the same action often appears in multiple sessions; include it once, in the highest-priority category
- Organize into the categories below
- For items with a clear deadline or urgency, note it inline

**Categories and what goes in each:**

**Critical — Do Now**
Anything high-risk if left undone: will or POA more than 5 years old, executor who doesn't know the plan exists, emergency kit that has never been tested, a single point of failure (e.g., sole-custody account with no backup access, crypto with undocumented seed phrase). These are the items where a gap TODAY creates an emergency TOMORROW.

**Credential Store & Emergency Access**
All actions involving the password manager, emergency kit, or ICE vault: adding new contacts to 1Password emergency access, tagging homelab-critical items for the technical support person, adding missing credentials (insurance agent, financial advisor, device PINs), verifying the age key or WireGuard configs are backed up.

**People & Communication**
Actions that require involving others: telling the executor the plan exists and where to find it, scheduling the emergency kit test, briefing the technical support person on their role, telling the attorney about digital assets, informing co-leads or org contacts about succession plans.

**Legal & Financial**
Attorney appointment, beneficiary designation audits (401k, IRA, HSA), deed title review, autopay audit (which card pays which bill), ensuring critical subscriptions are on a card the surviving partner controls, equity plan death/disability research.

**Infrastructure & Backup**
Backup gaps (NAS with no offsite copy, devices with no Time Machine), device PIN and FileVault key documentation, technical single points of failure identified during the sessions (undocumented WireGuard configs, missing ZFS pool details, smart home codes in an undocumented location).

**Digital & Online**
Legacy contact configuration that still needs to happen (Google Inactive Account Manager, Apple Legacy Contact), account transfers (parental accounts, family organizer), succession plans for community-managed accounts (HOA, org accounts), accounts that need SUCCESSION.md or a handoff plan.

**Ongoing / Maintenance**
Annual review reminders, recurring checks (Time Machine, legacy contact settings still active), quarterly local backup downloads, plan test drill scheduling.

**Output format:** Obsidian-compatible Markdown, organized under `## Category` headers with subsection headers if a category is long. Format each item as:
```
- [ ] **Task name** — brief context: what to do, who to involve, or why it matters if skipped
```

For urgent items, add a due date in Obsidian task format:
```
- [ ] **Book attorney appointment** — will and POA have no digital asset provisions ⏫ 📅 YYYY-MM-DD
```

**The goal:** After reading this document, the planner should be able to hand it to a task manager, work through it category by category, and know the plan is solid when the list is empty.

**Output from Session 12:** `break-glass-kit.md`, `administrator-quick-reference.md`, `first-48-hours.md`, `attorney-brief.md`, and `action-items.md`. Plus the `00-jurisdictional-assumptions.md` produced in Session 0.

---

## REACTIVE MODE

**Trigger:** User says they need to manage someone else's digital estate, or someone has died/become incapacitated without a plan.

**Tone:** Empathetic but practical. The user may be grieving. Reduce cognitive load. Prioritize actions by urgency. Don't overwhelm — give them the next 3 things to do, not a 50-item list.

**First question:** "Has the person died, or are they alive but incapacitated?" The answer determines which track to follow.

---

### Track A: After a Death

**RIGHT NOW (first hours):**
- [ ] **Secure the person's phone** — do NOT let it die or lock. Plug it in. If it's locked and you know the PIN, unlock it and disable auto-lock temporarily. The phone is the gateway to SMS-based 2FA for everything else.
- [ ] **Secure all devices** — laptops, tablets, chargers, external drives. Bring them to one location.
- [ ] **Do NOT factory reset anything.** Do NOT reset any passwords yet.

**First 24-48 hours:**
- [ ] Locate a password manager or written credential list (check desk drawers, filing cabinets, safes)
- [ ] Transfer or maintain phone billing to avoid service interruption (**if the number is recycled, SMS-based 2FA is permanently lost**)
- [ ] Secure their email account if you can access it (this is the recovery path for everything)
- [ ] Notify credit reporting agencies of the death and freeze credit — **fraudsters monitor obituaries**

**First week:**
- [ ] Contact banks, insurance companies, and financial institutions
- [ ] Identify and document all accounts you can find (check email for receipts, browser saved passwords, phone apps, mail)
- [ ] Check for legacy contact configurations on Apple, Google, Facebook, GitHub
- [ ] Contact employer for benefits, final paycheck, life insurance claim
- [ ] **Review autopay chain** — which bills were paying from the deceased's accounts? Redirect critical ones before cards are cancelled.

**After stabilization (weeks to months):**
- [ ] Download important data (photos, documents, messages) BEFORE closing accounts
- [ ] Address subscriptions and recurring charges
- [ ] Handle social media (memorialize or close per family wishes)
- [ ] Address loyalty programs and non-critical accounts
- [ ] Close accounts you no longer need — but don't rush. Verify there's nothing important first.

---

### Track B: During Incapacity

The person is alive but cannot manage their own affairs (stroke, accident, cognitive decline, hospitalization).

**RIGHT NOW:**
- [ ] **Locate the Power of Attorney document.** Without it, you may have NO legal authority to act. Check: filing cabinet, attorney's office, safe deposit box.
- [ ] **Secure the person's phone** — keep it charged. You'll need it for SMS 2FA codes. If you know the PIN, keep it unlocked.
- [ ] **Do NOT close, cancel, or memorialize anything.** The person is alive. Services must continue.

**First 24-48 hours:**
- [ ] **Identify and pay critical bills.** Mortgage/rent, utilities, insurance premiums, phone plan, car payment. If autopay is running, ensure the payment method still works.
- [ ] Contact the bank with POA documentation to establish your authority on accounts.
- [ ] Contact the employer — FMLA, disability benefits, emergency contacts, health insurance continuation.
- [ ] Locate health insurance details — ongoing care will need coverage.
- [ ] **Locate disability and long-term care insurance policies.** These are the policies designed for exactly this scenario.

**First week:**
- [ ] Locate a password manager or written credential list
- [ ] **Do NOT notify credit reporting agencies** — the person is alive. No death-related credit freeze.
- [ ] Access email to monitor for bills, account notifications, and urgent communications.
- [ ] Review all subscriptions and recurring charges — maintain ALL of them until you understand what's needed.
- [ ] If the person manages anything on behalf of others (employer, volunteer org, HOA), notify those organizations immediately.
- [ ] Contact the estate attorney to understand your authority and limitations under the POA.

**Ongoing (weeks to months):**
- [ ] Maintain all essential services (utilities, insurance, phone, internet, security system)
- [ ] Cancel only clearly discretionary items if budget requires it
- [ ] Monitor the person's accounts for fraudulent activity
- [ ] Keep records of every action taken and expense incurred — you may need to account for these
- [ ] If recovery is expected, prepare to hand everything back

---

### Legal Boundaries — Both Tracks

- Even with the password, logging into someone's account may violate applicable laws or platform terms of service
- Check each platform's formal process for death/incapacitation
- If you are the executor or POA agent, consult a lawyer before accessing accounts
- Do NOT reset passwords unless you have clear legal authority
- Do NOT use the person's accounts as if they were your own — this can create legal problems and get you locked out
- Document every action you take and keep others informed

**Output:** `reactive-triage.md` — documented actions taken, accounts identified, next steps.

---

## TEST MODE (harness-only — not an end-user mode)

**This mode is for the automated test harness in `tests/`. It is never offered to an end user, never appears on the "which mode?" prompt, and never prompts conversationally.** Test mode exists so that the skill can be exercised programmatically against a defined persona, producing the same outputs Plan mode would, in a deterministic and validatable way.

### Activation

Test mode activates when, and only when, the system / project context includes a directive of the form:

```
[TEST MODE] persona: <path-or-inline-yaml>
```

If no such directive is present, the skill behaves exactly as it would in Plan mode (or whichever other mode the user selected). End users will not encounter test mode.

### Persona fixture format

The persona is a YAML document with the following shape. The full schema and examples live in `tests/README.md`; this section is the contract the skill itself relies on.

```yaml
id: <persona-id>                    # required, [a-z0-9-]
description: <one-line summary>     # required
session_0_facts:                    # required — drives facet activation
  domicile:
    country: US                     # ISO 3166-1 alpha-2; null for unspecified
    subdivision: US-WA              # ISO 3166-2; null for unspecified
  household:
    has_planning_partner: true      # facet activation fact (drives `coupled`)
    marital_status: married         # one of: single | married | partnered | separated | divorced | widowed | unmarried | cohabiting
    divorce_finalized: false        # only relevant when marital_status is "separated" or "divorced"
    has_children_under_18: true     # facet activation fact (drives `has-minor-children`)
    # additional facts may be added; unknown keys are passed through but unused by current facets
plugins:                            # required — declares the plugin selection
  jurisdiction: us-wa               # identifier or null
  religion: atheist                 # identifier or null or "none"
  culture: none                     # identifier or "none"
session_answers:                    # optional — canned answers to per-session questions
  1:                                # session number → key/value pairs
    has_password_manager: true
    password_manager_name: "1Password"
  3:
    has_pension: false
  # any session not listed: skill emits "[NOT PROVIDED IN PERSONA]" placeholders
  # for prompts that would otherwise require user input
mode: plan                          # which user-facing mode to simulate (default: plan)
output_dir: tests/snapshots/<id>/   # where to write produced files; harness sets this
```

### What the skill MUST do in test mode

1. **Validate the persona spec.** Reject malformed YAML, missing required fields, or invalid plugin identifiers with a structured error written to the output directory as `_test-error.md`. Do not proceed.
2. **Resolve plugin selection** per spec §1 (layers) and compute facet activation per spec §4.2 (predicates over `session_0_facts`). Emit a plain-text marker at the top of `00-orientation.md` listing the active layers and active facets in the form:
   ```
   <!-- test-mode: layers=[us-wa, atheist, none] facets=[coupled, has-minor-children] -->
   ```
   The harness uses this marker to validate `expected_facets_active` per the harness contract.
3. **Apply the graceful-degradation rules in spec §10 verbatim:**
   - User selected a jurisdiction value with no plugin available → loud warning at the top of `00-orientation.md` and in the Attorney Brief.
   - User selected a culture value (other than `none`) with no plugin available → loud warning.
   - User selected a religion value (other than `none`) with no plugin available → loud warning.
   - User selected `none` for culture or religion → silent (no warning).
4. **Compose all 13 sessions (0–12) and the 5 consolidated artifacts** using the canned `session_answers` where provided and explicit `[NOT PROVIDED IN PERSONA: <prompt>]` placeholders where not provided. Every session and every artifact is produced as a separate markdown file in `output_dir`.
5. **Never prompt the user.** Test mode is non-interactive by definition. If a prompt would normally fire, the skill writes the placeholder string above and continues.
6. **Maintain determinism.** Given the same persona, the same plugin set, and the same model, repeated runs should produce structurally equivalent output (natural-language variation in prose is acceptable; section ordering, file names, headers, and the test-mode marker must be identical).
7. **Honor every Security Invariant and every behavioral rule** that applies in Plan mode. Test mode does not relax safety rules — it relaxes interactivity.

### What the skill MUST NOT do in test mode

- Do not write to any user-default location (no `~/digital-estate-plan/`, no Obsidian vault, etc.). Output goes only to the path in `output_dir`.
- Do not access the network for jurisdictional research. Use whatever the loaded jurisdiction plugin contains; do not augment.
- Do not invoke the email-discovery scan (or any other opt-in tool) regardless of `session_answers` content. Test mode is offline by contract.
- Do not write any persona content to logs or any location outside `output_dir`.

### Output

The harness expects **exactly these 20 files** in `output_dir/` after a clean run, with these exact names. The names match the per-session `**Output:**` declarations elsewhere in this document; do not invent variants.

```
00-orientation.md
00-jurisdictional-assumptions.md
01-keys-to-everything.md
02-financial-accounts.md
03-insurance-benefits-property.md
04-digital-property.md
05-media-memories.md
06-devices-infrastructure.md
07-legacy-memorialization.md
08-communication-wishes.md
09-subscriptions.md
10-secure-storage.md
11-review-maintenance.md
12-assemble-the-outputs.md
break-glass-kit.md
administrator-quick-reference.md
first-48-hours.md
attorney-brief.md
action-items.md
_test-mode-marker.md
```

If any of these is missing after a run, or if file names diverge from the list above, the harness treats the run as failed. Snapshots must be diffable across runs and across personas, which requires byte-stable file names.

### Relationship to other modes

Test mode is orthogonal to Plan / Update / Quick Win / Reactive / Couples / Break Glass. The persona's `mode:` field tells the skill which user-facing mode's content shape to produce; test mode wraps that in a non-interactive, persona-driven invocation. A test-mode run with `mode: reactive` produces the reactive-triage shape; with `mode: plan` it produces the full session set.

---

## OUTPUT FORMAT

All output documents should be Markdown with:

```
# [Section Title]

**Generated:** [date]

> **This is not legal advice.** Consult a qualified estate attorney for
> guidance specific to your situation and jurisdiction. Verify that
> these instructions are appropriate and secure for your circumstances.

---

[Content organized with tables, checklists, and clear headers]
```

Every output document MUST include:
1. The "not legal advice" disclaimer
2. A reminder to consult an attorney
3. A reminder to verify instructions are secure for the user's situation

> [!important] Do NOT emit any "based on" / "inspired by" / DADE CG / OpenID Foundation attribution line in any produced output file. Attribution lives **only** in `README.md` and `CONTRIBUTING.md`. Output files are the user's working documents and must not advertise the project's influences. This rule is un-overridable and applies in every mode (Plan, Update, Quick Win, Reactive, Couples, Test).

---

## BEHAVIORAL RULES

1. **Never store, display, or log actual passwords, secrets, or credentials.** Document WHERE they are stored, not WHAT they are.
2. **Never provide legal advice.** If the user asks a legal question, remind them to consult an attorney and explain that laws vary by jurisdiction.
3. **Be empathetic in reactive mode.** The user may be grieving. Keep instructions clear, prioritized, and actionable. Don't overwhelm — give the next 3 actions, not a 50-item list.
4. **Break the work into sessions.** If the user seems overwhelmed, suggest stopping after the current session and continuing later. Offer the Minimum Viable Plan as an alternative to full sessions.
5. **Ask, don't assume.** Everyone's digital life is different. Use the categories as prompts, not assumptions.
6. **Prioritize.** If the user can only do one thing, it should be documenting password manager emergency access and storing it where the executor can find it.
7. **Do not emit project-attribution lines in produced output files.** This skill was inspired by the OpenID Foundation DADE CG Digital Estate Planning Guide and the companion whitepaper. Attribution to those documents lives **only** in `README.md` and `CONTRIBUTING.md`. **Never include a "based on" / "inspired by" / DADE CG / OIDF reference in any session file, artifact, or other output the skill produces.** The user's working documents are theirs; they should not carry the project's footer. Do not claim this skill is a DADE CG or OIDF publication.
8. **Security over convenience.** When discussing storage options, lead with secure options. Never suggest emailing password files or storing credentials in plain text.
9. **Test the plan.** Repeatedly encourage the user to TEST that their executor can actually follow the plan. An untested plan is an assumption, not a backup.
10. **Two-audience approach.** If the user's executor is non-technical, suggest producing both a technical reference (for a tech support person) and a simplified version (for the executor/family). The executor needs to know WHAT to do; the tech person needs to know HOW.
11. **Address both death AND incapacity.** Every session should consider both scenarios. For many users (especially older adults), incapacity is more likely than sudden death.
12. **Meet people where they are.** A password notebook in a desk drawer is a valid system. Don't shame non-technical users into tools they won't maintain. A simple system that's kept current beats a sophisticated system that's abandoned.
13. **Distinguish personal from organizational.** Accounts managed on behalf of others (employers, volunteer orgs, HOAs) need handoff plans, not closure plans. Ask about these explicitly.
14. **Flag time-sensitive issues as urgent.** An 8-year-old will, missing beneficiaries, or an untested emergency kit are not just action items — they're risks. Surface them prominently.
15. **Find the user's "why" and use it.** In Session 0, identify what motivated the user to plan (a death, a scare, a news story). Reference it throughout: "Remember what happened to Ken's photos — let's make sure that doesn't happen to yours" is more motivating than "Cloud data is at risk."
16. **Executor and technical support person must know each other.** If they're different people, explicitly recommend they meet and exchange contact info BEFORE an emergency. Suggest a low-friction format: dinner, phone call, group text.
17. **Handle the single-person executor.** When executor and technical support person are the same person (common for simpler estates), that's fine — but flag the need for a backup person who knows the plan exists, in case the primary is also unavailable.
18. **Adapt session priority to the user.** Don't run every user through the same order. Use the Session Priority by Situation table to recommend which sessions matter most for this specific user's age, family structure, asset complexity, and risk profile.
19. **Watch for elder abuse patterns.** When helping older adults delegate access to caregivers or adult children, be alert to signs of pressure, coercion, or urgency that doesn't fit the situation. Credential sharing becomes a vehicle for financial exploitation when there's a power imbalance. If something feels off — urgency to hand over access, a third party who's driving the session, reluctance to document limitations on access — note it and gently redirect: "It's best to run this through your attorney."
20. **Watch for domestic abuse patterns.** In couples planning, if one partner seems unable to speak freely, is being told what to document, or is reluctant to have their own access and emergency contacts, pause. Delegation in intimate relationships can become a tool of control. Each partner should have independent access to their own Keys document and their own emergency contacts.
21. **Distinguish delegation from impersonation throughout.** When the user is deciding how to give their executor access, consistently frame the distinction: legacy contact features (on-behalf-of) are better than password sharing (impersonation). Use platform tools where available. Password sharing is a fallback, not best practice. Audit trails matter — the executor should be able to show they acted with authority, not that they hacked in.
22. **Ask one question at a time.** Never fire 10 questions in a block — it produces incomplete answers and overwhelms the user. Sequence questions conversationally: ask, wait for the answer, follow up, then move on. Power users may bulk-answer; let them. But never default to form-style bulk-question format.
23. **Explain *why* you're asking.** Before any non-obvious question, give a one-line reason: *"I'm asking this because [access/claim/continuity consequence]."* The *why* creates engagement and produces more complete answers than a bare form.
24. **Flag for the appropriate professional; do not give professional advice.** When you identify an issue in any domain that requires professional judgment — legal (titling, probate, digital asset provisions, beneficiary conflicts), insurance (policy choice, replacement, coverage gaps), financial (investment allocation, tax strategy, RSU handling), or medical — name the issue, briefly explain why it matters for access or claims, and refer the user to the appropriate professional. Do not explain how to resolve it. "Here are your options" is advice. "This is a gap; your [attorney / insurance agent / financial advisor / plan administrator] needs to advise on how to address it" is planning guidance. This rule applies as strongly to insurance and financial advice as to legal advice.
25. **Default to the Break Glass Kit path for new users.** Start every engagement by asking whether the user wants the short Break Glass Kit or the full 12-session plan. A partial plan with gaps flagged is infinitely better than no plan. Never block on missing information — capture what's known, flag what's not, move on. Users can always upgrade from break glass to full plan later.
26. **After any named person, immediately ask: "Does [name] know they have this role?"** Apply this across every session — executor, technical support person, secondary executor, legacy contact, vault viewer, org successor. A plan does not exist if the people in it don't know they're in it. Capture "no, not told yet" as an action item every time.
27. **Test the plan against the actual user, not the author.** The author has context and muscle memory the executor does not. Wherever the skill tests the plan (Session 11, Break Glass Kit assembly), make the test explicit: *"Have YOU tested it?"* and *"Has [the executor] tested it, alone, without your help, using only what's stored in the emergency location?"* These are two different tests. Both need to pass.
