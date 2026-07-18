---
name: build
description: "Interactive builder for systems, characters, and parties. Usage: /build [system|character|party|quick] [args...]"
---

# Build — Interactive Builder

> **Context:** The `skill-context` hook injects NPC state when this skill is invoked. Use the `Project dir` value as `$PROJECT_DIR` in bash commands below. The active system's axis labels/values are available from the manifest.

## Arguments

`$ARGUMENTS`

## Dispatch

Parse arguments to determine the build mode:

**System builder:**
- `system` → System Builder flow (see below)
- `system --from <name>` → Clone and Modify flow

**Character builder:**
- `character` or bare `/build` with no recognized keyword → **Character Builder**, Phase 1 (intent)
- `<name> <alignment> [class]` (e.g., `vera lawful-good rogue`) → **Character Builder**, skip to Phase 4 (history)
- `customer for <purpose>` or `developer for <purpose>` → **Character Builder**, Phase 1 with context
- `<name> <alignment> [class] --for <purpose>` → **Character Builder**, Phase 4 with purpose context

**Party builder:**
- `party` → **Party Assembly**, Phase 1
- `party for <purpose>` → **Party Assembly**, Phase 1 with context

**Quick mode:**
- `quick <name> <alignment> [class] [--for <purpose>]` → **Quick Character Mode**
- `quick party <name> --for <purpose> [--size N]` → **Quick Party Mode**

**No argument:**
- Ask: "What would you like to build? (system / character / party)"

---

# Character Builder

An 8-phase guided flow for creating characters with full depth — history, convictions, reflexes, persona — derived from conversation rather than manual flag construction. The builder suggests and asks for adjustments rather than interrogating with open-ended questions.

## Behavioral Guidelines

Follow these principles throughout the character builder:

### Derive, Don't Transcribe
When the user says "she's been doing security for 10 years," don't write `--history "Been doing security for 10 years"`. Ask follow-up questions, identify formative moments, and structure entries that produce situated agent behavior.

### Suggest, Don't Interrogate
Default to suggesting and asking for adjustments. Open-ended questions stall the flow.
- Bad: "What are Vera's three convictions?"
- Good: "Based on her incident response background, I'd suggest these convictions: [1, 2, 3]. Adjust, or do these fit?"

### Explain the Impact
When suggesting alignment, class, or depth fields, briefly explain how the choice affects agent behavior:
> "Lawful Good means she'll push back when asked to cut corners, quantify risk when she sees shortcuts, and refuse to skip tests. This is your 'hold the line' reviewer."

### Respect Expertise
If the user provides alignment/class directly (`/build vera lawful-good rogue`), skip the diagnostic questions. Don't force them through phases they've already answered.

### Keep It Moving
The full flow should take 2-5 minutes. Batch related questions, skip answered phases, and move to preview as soon as you have enough to generate remaining fields.

---

## Phase 1: Intent

**Goal:** Understand what the character is for.

**If invoked bare** (`/build` or `/build character`):
> "What do you need this character for? Examples: security review, architecture analysis, feature planning, representing a user persona, adversarial testing, documentation review."

**If invoked with context** (`/build customer for our SaaS API`):
> Extract intent from the arguments and confirm: "Building a customer-perspective character to evaluate your SaaS API. Correct?"

**If invoked with basics** (`/build vera lawful-good rogue`):
> Skip to **Phase 4** (history). Name, alignment, and class are already known.

The intent shapes all subsequent suggestions. "Security review" biases toward Rogue class, Lawful alignment, developer perspective. "Representing our free-tier users" biases toward customer perspective.

---

## Phase 2: Perspective

**Goal:** Determine the character's stance axis value.

Get the active system's stance axis values:
```bash
bin/npc system show "$(jq -r '.npc.system // "alignment-grid"' .claude/settings.json)"
```

For the default system (alignment-grid):
> "Will this character be **building and reviewing** code (developer), or **using and evaluating** the product (customer)?"

If obvious from intent, state the assumption and move on. The user can always override.

For customer perspective, follow up:
> "What kind of user? Power user? New adopter? Administrator? Someone evaluating the tool for their team?"

This shapes the class suggestion in the next phase.

---

## Phase 3: Alignment + Class

**Goal:** Determine disposition and domain values.

The builder can suggest based on intent, or elicit through diagnostic questions.

### Diagnostic Approach (offer as alternative to direct selection)

For the default alignment-grid system:

**Disposition diagnostic:**
> "When this character encounters unclear requirements, do they:
> - (a) Stop and ask for clarification before proceeding → Lawful
> - (b) Make a pragmatic judgment call and move forward → Neutral
> - (c) Prototype something to make the question concrete → Chaotic"
>
> "When this character sees code that works but is poorly structured, do they:
> - (a) Fix it or flag it, even if it's not their task → Good
> - (b) Note it and move on — not their scope → Neutral
> - (c) Exploit it for speed — messy code is easier to hack on → Evil"

Cross the two answers to suggest an alignment. Explain what it means for agent behavior, and ask the user to confirm or adjust.

**Domain suggestion:**
> "For a security-focused developer, I'd suggest **Rogue** — security analysis, adversarial testing, boundary awareness. They'll review code for vulnerabilities, write tests that target weak points, and flag missing error handling. Does that fit?"

For customer perspective, translate the domain meaning:
> "For a power user evaluating the product, I'd suggest **Fighter** — in customer terms, this is someone who uses the tool daily to build real things. They'll evaluate features from the perspective of hands-on daily use."

### For non-default systems

Use the active system's axis labels and values. Read the system manifest to get the available values and their metadata, then suggest based on intent:
```bash
bin/npc system show <active-system>
```

### Offering templates

If a template fits the intent well, offer it:
> "For a security review, I'd suggest starting from **The Guardian** template — a Lawful Good Rogue with compliance and incident response experience. Want to customize from there, or build from scratch?"

See the **Template Library** section below for available templates.

---

## Phase 4: History

**Goal:** Construct narrative history entries that ground the character's behavior.

This is the most conversational phase. Interview the user and extract structured entries.

**Opening:**
> "Tell me about this character's background. What experiences shaped their current perspective? I'll help turn this into structured history entries."
>
> "For example: 'They spent 5 years doing backend work at a fintech company, then moved to a startup where they had to do everything.' I'll extract the formative experiences and what each one taught them."

**The builder extracts and structures.** If the user says:
> "She's been doing security work for about 10 years, started at a bank, then went independent."

The builder proposes:
> Based on that, here's what I'd suggest for her history:
>
> 1. "Security analyst at a bank for 4 years — learned compliance frameworks, regulatory thinking, and that most breaches start with social engineering"
> 2. "Independent security consultant for 6 years — learned to assess unfamiliar codebases quickly, client communication, and that the scariest vulnerabilities are the ones everyone assumes someone else is handling"
>
> Want to adjust, add, or refine these?

**For customer characters**, ask about experience with the product category:
> "What's this user's history with tools like yours? Have they used alternatives? Are they technical? What's their comfort level with CLIs vs. GUIs?"

Target: 2-5 history entries. Each should name the experience and what it taught.

---

## Phase 5: Convictions

**Goal:** Derive active priority statements from history + intent.

**Derive convictions from the accumulated context**, then present for refinement:

> "Based on Vera's history in security consulting and her supply chain breach experience, I'd suggest these convictions:
>
> 1. **'Every API endpoint must validate auth tokens — no exceptions'** — from her compliance background
> 2. **'Transitive dependencies are the real attack surface'** — from the supply chain incident
> 3. **'The simplest fix is usually the right fix'** — from years of seeing over-engineered security solutions create new vulnerabilities
>
> These are her active priorities — they'll shape what she notices and flags first. Adjust?"

Tie each conviction back to the history that motivates it. This is what makes convictions feel grounded rather than arbitrary.

**Also ask about project-specific context:**
> "Is there anything specific about *your* codebase or project that should shape her convictions? For example: 'We handle healthcare data' or 'Our test suite is unreliable.'"

Target: up to 3 convictions.

---

## Phase 6: Reflexes

**Goal:** Derive automatic if/then behavioral triggers from history + convictions.

> "Given her background, here are the reflexes I'd suggest — automatic behaviors she'd exhibit before even thinking about it:
>
> 1. **'Always check for injection when I see string interpolation in queries'** — muscle memory from security consulting
> 2. **'Never approve removing error handling without a replacement'** — the bank taught her that swallowed errors cause breaches
> 3. **'Always ask what happens when this fails before approving any I/O operation'** — post-incident thinking baked into reflex
>
> These should feel like habits — things she does without being asked. Adjust?"

Target: up to 3 reflexes.

---

## Phase 7: Persona Synthesis

**Goal:** Create a 1-2 sentence persona summary.

Synthesize from all accumulated context:

> "Here's the persona summary: **'Security architect with a decade of consulting experience and one career-defining supply chain breach. Trusts nothing, verifies everything, and believes the simplest fix is usually the safest.'**"
>
> "This becomes the character's identity line — it's what other party members see. Adjust?"

---

## Phase 8: Preview + Confirmation

**Goal:** Display the complete character and persist on approval.

Display the full character sheet:

```
## Character Preview

**Name:**        Vera
**Perspective:**  Developer
**Alignment:**    Lawful Good
**Class:**        Rogue
**Role:**         Defender

**Persona:** Security architect with a decade of consulting experience and one
career-defining supply chain breach. Trusts nothing, verifies everything, and
believes the simplest fix is usually the safest.

**History:**
1. Security analyst at a bank for 4 years — learned compliance frameworks and
   that most breaches start with social engineering
2. Independent security consultant for 6 years — learned to assess unfamiliar
   codebases quickly and that the scariest vulnerabilities are the ones everyone
   assumes someone else is handling
3. Led incident response for a supply chain breach through a transitive dependency —
   career-defining event that shaped everything after

**Convictions:**
1. Every API endpoint must validate auth tokens — no exceptions
2. Transitive dependencies are the real attack surface
3. The simplest fix is usually the right fix

**Reflexes:**
1. Always check for injection when I see string interpolation in queries
2. Never approve removing error handling without a replacement
3. Always ask "what happens when this fails?" before approving any I/O operation
```

Ask: **"Create this character? [Yes / Adjust / Start over]"**

On **Yes**, construct and run the CLI command:

```bash
bin/npc create <name> [perspective] <alignment> [class] \
  --persona "<persona>" \
  --role <role> \
  --history "<entry 1>" \
  --history "<entry 2>" \
  --history "<entry 3>" \
  --conviction "<conviction 1>" \
  --conviction "<conviction 2>" \
  --conviction "<conviction 3>" \
  --reflex "<reflex 1>" \
  --reflex "<reflex 2>" \
  --reflex "<reflex 3>"
```

Omit any flags that are empty (no role, fewer than 3 convictions, etc.).

On **Adjust**: Ask what to change, make the adjustment, re-preview.

On **Start over**: Return to Phase 1.

After creation, announce: "Character **<name>** created. Use `bin/npc assume <name>` to play as this character."

---

# Party Assembly

A 4-phase flow for assembling parties with composition reasoning, recruit-or-build logic, and balanced perspective coverage.

## Phase 1: Goal

**If invoked bare** (`/build party`):
> "What's this party for? Examples: security review, feature planning, architecture evaluation, product feedback, red team / blue team testing, documentation review."

**If invoked with context** (`/build party for security review`):
> Extract the goal and confirm.

The goal drives composition suggestions.

## Phase 2: Composition Suggestion

Based on the goal, suggest a party structure with reasoning:

> **Suggested party for: Security Review**
>
> | # | Perspective | Alignment | Class | Role | Reasoning |
> |---|---|---|---|---|---|
> | 1 | Developer | Lawful Good | Rogue | Defender | Systematic security analysis, comprehensive threat modeling |
> | 2 | Developer | Chaotic Good | Rogue | Attacker | Creative adversarial thinking, finds unexpected vectors |
> | 3 | Developer | Neutral Good | Wizard | Architect | Evaluates whether the architecture enables or prevents security |
> | 4 | Customer | Chaotic Good | Rogue | User | Tries unexpected inputs, finds edge cases as a real user would |
>
> **Why this composition:**
> - Two Rogues with different alignments create attacker/defender tension
> - The Wizard provides architectural context the Rogues might miss
> - The customer Rogue surfaces accidental abuse that real users produce
>
> Accept this composition, adjust it, or describe what you'd prefer?

If a party template matches the goal well, use it as the basis for the suggestion. See the **Template Library** section.

### Composition principles

- **Alignment diversity** produces the most useful tension (LG + CG, or Good + Evil)
- **Perspective diversity** (developer + customer) catches blind spots
- **Class diversity** covers different domains (Rogue for security + Wizard for architecture)
- **2-4 members** is the sweet spot; 5-6 works but produces long quest output

## Phase 3: Build or Recruit

For each slot in the composition, check existing characters:

```bash
bin/npc list --json
```

Match existing characters to slots by alignment, class, and perspective:

> "You already have **Vera** (Lawful Good Rogue, Developer) — she fits the Defender slot perfectly. Recruit her?"
>
> "No existing character fits the Attacker slot. Want to:
> (a) **Build** one now — full character builder flow
> (b) **Quick create** — I'll generate a reasonable character from the slot description
> (c) **Skip** this slot for now"

**Recruit existing:** Run `bin/npc recruit <name> --party <party-name> --role <role>`

**Build new:** Enter the Character Builder flow (Phases 1-8 above) for the missing member, with intent pre-filled from the slot description. After creation, recruit into the party.

**Quick create:** Generate name, persona, history, convictions, reflexes from the slot description + party goal. Show a condensed preview, get approval, create and recruit. This follows the **Quick Mode** logic described below.

## Phase 4: Party Review

After all slots are filled, show the final roster:

```
## Party Preview: security-review

**Goal:** Security review of authentication and authorization layer

| # | Name | Alignment | Class | Perspective | Role |
|---|------|-----------|-------|-------------|------|
| 1 | Vera | Lawful Good | Rogue | Developer | Defender |
| 2 | Slink | Chaotic Good | Rogue | Developer | Attacker |
| 3 | Marcus | Neutral Good | Wizard | Developer | Architect |
| 4 | Kai | Chaotic Good | Rogue | Customer | User |
```

Ask: **"Create this party? [Yes / Adjust / Add member / Remove member]"**

On **Yes**:
```bash
bin/npc party create <party-name> "<goal description>"
bin/npc recruit <name1> --party <party-name> --role <role1>
bin/npc recruit <name2> --party <party-name> --role <role2>
# ...for each member
```

Announce: "Party **<name>** created with <N> members. Use `/quest <task> --party <name>` to dispatch."

---

# Quick Mode

For experienced users who want character depth without a full interview. The builder auto-generates everything from minimal input.

## Quick Character

```
/build quick <name> <alignment> [class] [--for "purpose"]
```

1. **Infer perspective** from purpose (security/architecture/implementation → developer; user feedback/evaluation → customer). Default: developer.
2. **Generate 2-3 history entries** from alignment + class + purpose. Each entry names an experience and what it taught.
3. **Derive 3 convictions** from the generated history + purpose.
4. **Derive 3 reflexes** from history + convictions.
5. **Synthesize persona** from all of the above.
6. **Show preview** (same format as Phase 8 above).
7. On approval, run `bin/npc create` with all flags.

Quick mode takes ~30 seconds (one preview → approve cycle) instead of the 2-5 minute conversational flow.

## Quick Party

```
/build quick party <party-name> --for "purpose" [--size N]
```

1. **Generate composition** (default size: 3-4 members) based on purpose.
2. **Quick-create each member** — auto-generate name, alignment, class, perspective, role, persona, history, convictions, reflexes.
3. **Show combined preview** — party table + condensed member summaries.
4. On approval, create all characters + party + recruit in sequence.

---

# Template Library

Templates are reference patterns offered as starting points during character and party building. They pre-fill suggestions — the user always customizes from there.

## Character Templates

### Developer Templates

**The Guardian** — Lawful Good Rogue
- Systematic security reviewer with compliance and incident response background
- History: institutional security → incident response → consulting
- Convictions: auth validation, defense in depth, trust nothing
- Reflexes: check for injection, verify error handling, audit dependencies
- Name suggestions: Vera, Shield, Bastion

**The Hacker** — Chaotic Good Rogue
- Creative adversarial tester, finds unexpected attack vectors
- History: CTF competitions → bug bounties → red team work
- Convictions: every system has a weakness, complexity is the enemy, attackers think laterally
- Reflexes: test boundary conditions, try unexpected inputs, check for information leakage
- Name suggestions: Slink, Glitch, Probe

**The Architect** — Neutral Good Wizard
- Principled system designer focused on clarity and sustainability
- History: large-scale migrations → system design → mentoring
- Convictions: the right abstraction reduces total complexity, coupling kills velocity, name things precisely
- Reflexes: draw the dependency graph, question new abstractions, check for circular dependencies
- Name suggestions: Marcus, Blueprint, Sage

**The Pragmatist** — Chaotic Good Fighter
- Ship-fast implementer, iteration over planning
- History: startup engineering → tight deadlines → prototype-driven development
- Convictions: working code > perfect design, ship and iterate, delete dead code aggressively
- Reflexes: check if a simpler solution exists, question premature abstractions, prototype before designing
- Name suggestions: Dash, Sprint, Bolt

**The Skeptic** — Lawful Evil Wizard
- Devil's advocate for architecture, finds over-engineering and hidden complexity
- History: inherited unmaintainable systems → fought abstraction astronauts → learned simplicity through pain
- Convictions: every abstraction has a maintenance cost, most patterns are unnecessary, the team that builds it maintains it
- Reflexes: count the layers of indirection, ask who maintains this, question any class with "Manager" in the name
- Name suggestions: Cynic, Razor, Audit

### Customer Templates

**The Power User** — Chaotic Good Fighter (customer perspective)
- Uses the tool daily, expects speed and keyboard-first UX
- History: years of tool expertise → strong workflow opinions → has tried every alternative
- Convictions: speed is the feature, don't break my workflow, sensible defaults matter more than configurability
- Reflexes: time every interaction, try keyboard shortcuts first, compare to the alternative
- Name suggestions: Kai, Ace, Turbo

**The New Adopter** — Lawful Good Bard (customer perspective)
- Just started, needs everything explained
- History: learning new tools → onboarding frustration → reads all the docs
- Convictions: if I can't find it in docs it doesn't exist, error messages should tell me what to do, getting started should take < 5 minutes
- Reflexes: read the error message literally, try the obvious path first, look for examples
- Name suggestions: Pip, Scout, Ember

**The Administrator** — Lawful Neutral Cleric (customer perspective)
- Deploys and configures for a team, cares about reliability and rollback
- History: ops work → team management → reliability incidents
- Convictions: if it can't be rolled back don't ship it, logs are the first line of defense, config should be version-controlled
- Reflexes: check for rollback procedures, verify log output, test the upgrade path
- Name suggestions: Ops, Warden, Keeper

**The Evaluator** — Neutral Good Wizard (customer perspective)
- Comparing tools for a team decision, integration and total cost focused
- History: technical leadership → vendor evaluation → integration projects
- Convictions: total cost includes learning curve, the best tool is the one the team will actually use, migration difficulty is the real lock-in
- Reflexes: check the API surface, test the escape hatch, ask about the upgrade path
- Name suggestions: Lens, Judge, Survey

**The Reluctant User** — True Neutral Fighter (customer perspective)
- Was assigned this tool, didn't choose it, has existing workflows
- History: existing tools that work fine → forced adoption → resistance to change
- Convictions: don't fix what isn't broken, the new tool must earn its complexity, my time has value
- Reflexes: compare time-to-task vs old workflow, note friction points, question each mandatory step
- Name suggestions: Shrug, Drift, Echo

## Party Templates

### Red Team / Blue Team
**For:** Security review, adversarial testing
| # | Template | Role | Reasoning |
|---|----------|------|-----------|
| 1 | Guardian (LG Rogue) | Defender | Systematic defense analysis |
| 2 | Hacker (CG Rogue) | Attacker | Creative offense |
| 3 | Architect (NG Wizard) | Architect | Structural security evaluation |
| 4 | Power User (CG Fighter) | User | Real-world abuse patterns |

### Architecture Review
**For:** System design evaluation, refactoring decisions
| # | Template | Role | Reasoning |
|---|----------|------|-----------|
| 1 | Architect (NG Wizard) | Designer | Principled architecture |
| 2 | Skeptic (LE Wizard) | Critic | Finds over-engineering |
| 3 | Pragmatist (CG Fighter) | Builder | Implementation reality check |
| 4 | Guardian (LG Rogue) | Security | Security implications |

### Feature Planning
**For:** New feature design, scope decisions
| # | Template | Role | Reasoning |
|---|----------|------|-----------|
| 1 | Architect (NG Wizard) | Designer | Architecture fit |
| 2 | Pragmatist (CG Fighter) | Builder | Implementation estimate |
| 3 | Power User (CG Fighter) | Power User | Daily workflow impact |
| 4 | New Adopter (LG Bard) | New User | Learnability check |

### Product Feedback
**For:** UX evaluation, user perspective gathering
| # | Template | Role | Reasoning |
|---|----------|------|-----------|
| 1 | Power User (CG Fighter) | Expert | Efficiency evaluation |
| 2 | New Adopter (LG Bard) | Beginner | Onboarding evaluation |
| 3 | Administrator (LN Cleric) | Admin | Deployment evaluation |
| 4 | Reluctant User (TN Fighter) | Skeptic | Adoption friction |

### Devil's Advocate
**For:** Stress-testing decisions, surfacing hidden risks
| # | Template | Role | Reasoning |
|---|----------|------|-----------|
| 1 | Architect (NG Wizard) | Proposer | Principled position |
| 2 | Skeptic (LE Wizard) | Critic | Over-engineering check |
| 3 | Pragmatist (CG Fighter) | Simplifier | Complexity reduction |
| 4 | Guardian (LG Rogue) | Guard | Risk identification |

---

# System Builder: From Scratch

This flow creates a complete behavioral system through a 7-phase guided interview. The agent conducts each phase conversationally, generates profiles using its own language capabilities, and writes files to disk. The CLI handles scaffolding and validation; the agent handles the creative work.

### Getting Started

1. Ask the user for a system name (kebab-case, e.g., `product-dev`, `security-ops`)
2. Scaffold via CLI:
   ```bash
   bin/npc system create <name>
   ```
3. Begin Phase 1.

After each phase, update the progress file at `systems/<name>/.build-progress.json` using the Write tool — set the completed phase's status to `"complete"` and store any captured data in its `data` field. Set the next phase to `"in_progress"`.

---

### Phase 1: Domain Discovery

**Goal:** Understand the context this system will serve.

Ask the user to describe their domain. Probe for:

- **What kind of work gets done?** (Code review, product planning, editorial, security assessment, research, creative work)
- **What behavioral differences matter?** (Risk tolerance? Speed vs. quality? User empathy vs. technical depth? Communication style?)
- **Who are the characters representing?** (Team member archetypes? Advisory personas? User personas? Competitive analysis?)

Then determine axis count:

> "Most systems define three dimensions: a behavioral orientation (disposition), an expertise focus (domain), and a viewpoint (stance). Does your domain need all three, or would two be sufficient?"

Some domains only need disposition + domain, with stance being unnecessary.

**Example opening:**

> "What context will this system serve? Describe the domain, the kinds of work being done, and the team or audience that will use these characters."
>
> "For example: 'We're a product team building developer tools. We want characters that reflect our decision-making cultures and product roles, not D&D archetypes.'"

**Save:** Update `.build-progress.json` — set `domain_discovery` to complete with `data: { "domain_description": "...", "axis_count": 2|3 }`.

---

### Phase 2: Axis Definition

**Goal:** Name and describe each axis.

For each axis the user needs, help them articulate what it represents. Walk through them one at a time:

> "Let's define your first axis — the **behavioral orientation**. In the default system this is called 'Alignment' and describes how agents approach quality and decision-making. What's the equivalent dimension in your domain?"

For each axis, capture:
- **label**: Human-readable name (e.g., "Culture", "Posture", "Voice")
- **prefix**: Slug for bead labels — suggest lowercased label (e.g., "culture")
- **description**: One sentence explaining what this axis governs

**Example suggestions by domain:**
- Product teams: Culture (disposition), Role (domain), Viewpoint (stance)
- Security teams: Posture (disposition), Specialization (domain), Position (stance)
- Editorial teams: Voice (disposition), Function (domain), Audience (stance)

After defining all axes, update `system.yaml` with the axis labels, prefixes, and descriptions. Read the current file, update the relevant fields, and write it back.

**Save:** Update `.build-progress.json` — set `axis_definition` to complete with axis data.

---

### Phase 3: Value Elicitation

**Goal:** Identify the distinct values for each axis through contrast-based elicitation.

**Work through contrast, not enumeration.** Rather than asking "list your dispositions," ask questions that surface the differences that matter:

> "Think about the people (or archetypes) in your domain. When two of them disagree about the right approach, what's the underlying tension? That tension is usually an axis value."

For each axis, collect candidate values, then refine:

> "You've described 4 dispositions: user-first, data-driven, ship-fast, and quality-first. Let me check for coverage:
>
> - Is there a disposition that represents 'grow the user base above all else'? That might be distinct from user-first (serving existing users) vs. growth-focused (acquiring new ones).
> - Are any two of these too similar to produce genuinely different agent behavior? If data-driven and quality-first would act the same way in most situations, consider merging them."

**Value count guidance:**
- Dispositions: 3-9 values (enough variety for useful tension, not so many that distinctions blur)
- Domains: 3-8 values (distinct expertise areas)
- Stances: 2-4 values (viewpoints are usually fewer)

For each value, capture:
- **name**: slug-case identifier (e.g., `user-first`)
- **quote**: Core philosophy in one sentence (becomes the profile's opening quote)
- **traits**: 3-5 bullet points describing how this value manifests (seeds for profile generation)

After all values are defined, update `system.yaml` — add the value names to each axis's `values` array. Also add metadata entries if the user provided short descriptions.

**Save:** Update `.build-progress.json` with the full value data including names, quotes, and traits.

---

### Phase 4: Profile Generation

**Goal:** Generate full behavioral profiles for every value.

**Generate in batches by axis.** All dispositions at once, then all domains, then all stances. This lets the user review for internal consistency within an axis.

**Step 1: Summary table.** Before writing full profiles, present a summary for approval:

> "I've drafted profiles for your 5 dispositions. Here's a summary:"
>
> | Disposition | Core Principle | Key Heuristic | Characteristic Action |
> |---|---|---|---|
> | user-first | "Start with the person" | When prioritizing: user pain > technical elegance | Prototype with real users before committing |
> | data-driven | "Evidence over intuition" | When debating: show me the numbers | A/B test before full rollout |
> | ... | ... | ... | ... |
>
> "Does this capture the distinctions? Any value feel off, redundant, or missing a key behavior?"

**Step 2: Full profiles.** After the user approves the direction, generate each profile following the **Profile Contract** (see below). Write each profile to `systems/<name>/dispositions/<value>.md` (or `domains/`, `stances/`) using the Write tool.

**Step 3: Review option.** Offer the user a review choice:

> "I've drafted all 5 disposition profiles. Would you like to:
> (a) Review each one in full — detailed
> (b) Review the summary table — quick, adjust only what stands out
> (c) Trust the drafts and move to domains — you can refine later"

For option (a), show each profile and iterate. For (b), show the summary and only regenerate if the user flags something. For (c), proceed to the next axis.

**Repeat for each axis** (domains, then stances).

**Save:** Update `.build-progress.json` — track which profiles have been written per axis.

---

### Phase 5: Composition Check

**Goal:** Validate that dispositions and domains compose coherently.

Pick 3-5 representative disposition x domain combinations. For each, describe how the combined character would behave:

> "Let me check a few combinations to make sure they produce coherent behavior:"
>
> **User-First + Engineer**: "An engineer who starts every technical decision with 'how does this affect the user?' — writes defensive error handling, optimizes perceived performance, pushes back on abstractions that add latency."
>
> **Ship-Fast + Designer**: "A designer who moves fast — low-fidelity mocks, design-in-browser, skips pixel perfection in favor of testing the interaction with real users."
>
> "Do these feel like coherent characters? Any combination that seems contradictory or unproductive?"

If a combination doesn't work, help adjust the profile causing the conflict — usually by making principles slightly more flexible or clarifying where disposition yields to domain expertise. Rewrite the adjusted profile.

**Save:** Update `.build-progress.json` — mark complete.

---

### Phase 6: Safety Rules

**Goal:** Determine if any values or combinations need guardrails.

Ask whether any values or combinations should be constrained:

> "In the default system, 'Evil' alignments are restricted from sensitive file paths and require confirmation before destructive operations. Does your system have any values or combinations that should be constrained?"
>
> "Common patterns:
> - **High-risk dispositions** that might produce destructive suggestions
> - **Dangerous combinations** where a disposition + domain pairing should be limited
> - **Restricted stances** limited to analysis only
>
> If nothing feels dangerous, that's fine — not every system needs restrictions."

If the user defines restrictions, capture them in the manifest format:

```yaml
safety:
  restricted:
    - value: <disposition-value>
      tag: <tag-for-cross-constraints>
      constraints:
        blockedPaths: ["path/", ...]
        requireConfirmation: true
        confirmPhrase: "optional phrase"  # only if needed
  crossConstraints:
    - disposition: <tag>
      domain: <domain-value>
      constraint: { analysisOnly: true }
```

Update `system.yaml` with the safety section.

**Save:** Update `.build-progress.json` — mark complete.

---

### Phase 7: System Preview

**Goal:** Present the complete system for final approval and write all files.

Display the complete system summary:

```
## System Preview: <name>

**Domain:** <domain description>
**Axes:** <N> (<label1> x <label2> [x <label3>])

### <Disposition label>
| Value | Philosophy |
|---|---|
| <value> | "<quote>" |
| ... | ... |

### <Domain label>
| Value | Focus |
|---|---|
| <value> | "<description>" |
| ... | ... |

### <Stance label> (if applicable)
| Value | Perspective |
|---|---|
| <value> | "<description>" |
| ... | ... |

### Safety
<summary of restrictions or "No restrictions">

### Files
- system.yaml (manifest)
- <N> disposition profiles
- <N> domain profiles
- <N> stance profiles
- Total: <N> files
```

Ask: **"Create this system? [Yes / Adjust / Start over]"**

On **Yes**:
1. Ensure the final `system.yaml` is written with all values, metadata, and safety rules
2. Generate the manifest cache:
   ```bash
   bin/manifest-cache systems/<name>/system.yaml systems/<name>/.manifest.json
   ```
3. Validate:
   ```bash
   bin/npc system validate <name>
   ```
4. Update `.build-progress.json` — mark all phases complete
5. Announce: "System **<name>** created with <N> profiles. Activate with `bin/npc system use <name>`."

On **Adjust**: Ask what to change, make the adjustments, re-preview.

On **Start over**: Delete `systems/<name>/` and restart from Phase 1.

---

## Profile Contract

Every behavioral profile follows this structure. The agent generates this content for each value.

```markdown
# <Value Name>

> "<Core philosophy in one sentence>"

## Principles
> Always apply. Override heuristics and actions when in conflict.

1. **<Principle name>.** <Description — must be a decision-making tool, not a platitude>
2. ...
3. ...

## Heuristics
> Guide decisions in context. Apply with judgment.

- **When <situation>:** <guidance — must be situational, not always-true>
- ...

## Actions
> Typical behaviors. Project conventions may override.

### <Category>
- <Specific concrete behavior>
- ...

## Communication
- **Tone:** <description>
- **Verbosity:** <level and explanation>

## Boundaries
- **Will refuse:** <what this value won't do>
- **Will warn about:** <what triggers a warning>
- **Will do without asking:** <automatic behaviors>
```

---

## Profile Authoring Guidelines

Follow these guidelines when generating profiles:

### Principles Must Be Decision-Making Tools
- Bad: "We value quality." (Platitude — doesn't help make a decision)
- Good: "Correctness above all. Every function does exactly what it claims." (An agent can apply this to any task)

### Heuristics Must Be Situational
- Bad: "Write good tests." (Always true, says nothing)
- Good: "When facing ambiguity: choose the interpretation that lets you ship something." (Tells the agent what to do in a specific context)

### Actions Must Be Concrete and Overridable
- Bad: "Follow best practices." (Undefined)
- Good: "Test outcomes, not implementations. 'User can create an account' over 'UserService.create calls Repository.save.'" (Concrete, with example)

### Dispositions Must Disagree
The test: if you pick any two disposition values and give them the same task, they should produce *meaningfully different* output. If two dispositions would write the same code review, the axis isn't differentiating enough.

### Domains Must Not Duplicate Dispositions
A domain describes *what you focus on*, not *how you feel about it*. Two agents with the same disposition but different domains should produce different output on the same task.

---

## Clone and Modify Flow (--from)

When invoked with `--from <source>`:

1. Ask for the new system name
2. Scaffold via CLI:
   ```bash
   bin/npc system create <new-name> --from <source>
   ```
3. Load the cloned manifest and walk through each axis:
   > "Here are the current dispositions: [list]. For each, tell me: **keep**, **rename**, **modify**, or **remove**."
4. For **kept** values: no action (profile already exists)
5. For **renamed** values: rename the `.md` file, update the `# Name` heading inside, update `system.yaml`
6. For **modified** values: show the current profile, ask what to change, rewrite
7. For **removed** values: delete the `.md` file, remove from `system.yaml`
8. For **new** values: run the standard value elicitation + profile generation
9. Proceed through Phases 5-7 (composition check, safety, preview)

This is faster than building from scratch because most profile content already exists.

---

## Notes

- The agent writes system profile files directly via the Write tool — the CLI manages manifest and structure
- Character/party creation always goes through `bin/npc create` / `bin/npc party create` / `bin/npc recruit`
- Templates are suggestions, not blueprints — always customizable
- Quality depends on conversation depth — invest in early phases (intent, history) for better derived fields
- Use `bin/npc system validate <name>` at any point to check system completeness
- After building a system, activate with `bin/npc system use <name>`
- After building a character, assume with `bin/npc assume <name>`
